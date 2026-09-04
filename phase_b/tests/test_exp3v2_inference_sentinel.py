from __future__ import annotations

import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

from phase_b.execution.openai_adapter import OpenAIAdapter
from phase_b.exp3_v2 import run_exp3v2_inference as runner
from phase_b.exp3_v2 import run_exp3v2_inference_sentinel as sentinel
from phase_b.exp3_v2 import verify_exp3v2_inference_sentinel as sentinel_verifier


ROOT = Path(__file__).resolve().parents[2]
HARNESS_MANIFEST = ROOT / "phase_b/exp3_v2/EXP3_V2_INFERENCE_HARNESS_MANIFEST_001.json"


class FakeUsage:
    def __init__(self, input_tokens=11, output_tokens=7, total_tokens=18) -> None:
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_tokens = total_tokens

    def model_dump(self, *, mode: str) -> dict:
        del mode
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
        }


class FakeResponse:
    def __init__(
        self,
        raw_output: str,
        *,
        returned_model: str = runner.MODEL,
        usage: FakeUsage | None = None,
    ) -> None:
        self.output_text = raw_output
        self.model = returned_model
        self.id = "synthetic-sentinel-response"
        self._request_id = "synthetic-sentinel-request"
        self.usage = usage or FakeUsage()

    def model_dump(self, *, mode: str) -> dict:
        del mode
        return {
            "id": self.id,
            "model": self.model,
            "output_text": self.output_text,
            "usage": self.usage.model_dump(mode="json"),
        }


class FakeResponses:
    def __init__(self, response: FakeResponse | None = None, error=None) -> None:
        self.response = response or FakeResponse(valid_output())
        self.error = error
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return self.response


def valid_output(*, label: str = sentinel.EXPECTED_LABEL) -> str:
    return json.dumps(
        {
            "predicted_label": label,
            "abstain": False,
            "used_insight_ids": [],
            "reasoning_summary": "Synthetic sentinel response.",
        },
        separators=(",", ":"),
    )


def make_adapter(responses: FakeResponses) -> OpenAIAdapter:
    return OpenAIAdapter(
        requested_model=runner.MODEL,
        client=SimpleNamespace(responses=responses),
    )


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


class Exp3V2InferenceSentinelTests(unittest.TestCase):
    def run_fake(self, root: Path, responses: FakeResponses | None = None):
        fake = responses or FakeResponses()
        evidence = sentinel.run_sentinel(root, make_adapter(fake))
        return evidence, fake

    def test_fixed_prompt_and_exact_provider_parameters_are_synthetic(self) -> None:
        sentinel.assert_prompt_is_synthetic()
        lowered = sentinel.SENTINEL_PROMPT.lower()
        for forbidden in (
            "exp3",
            "case to diagnose",
            "insight",
            "derangement",
            "fault",
            "normal",
            "cls-",
        ):
            self.assertNotIn(forbidden, lowered)
        with tempfile.TemporaryDirectory() as raw:
            evidence, fake = self.run_fake(Path(raw) / "sentinel")
        self.assertEqual(evidence["status"], "PASS")
        self.assertEqual(len(fake.calls), 1)
        call = fake.calls[0]
        self.assertEqual(call["model"], "gpt-5.6-terra")
        self.assertEqual(call["reasoning"], {"effort": "medium"})
        self.assertEqual(call["max_output_tokens"], 512)
        self.assertFalse(call["store"])
        self.assertTrue(call["text"]["format"]["strict"])
        self.assertNotIn("temperature", call)
        self.assertNotIn("seed", call)
        self.assertNotIn("previous_response_id", call)

    def test_pass_evidence_and_portable_verifier(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "sentinel"
            evidence, fake = self.run_fake(root)
            result = sentinel_verifier.verify_sentinel(root)
            self.assertEqual(evidence["status"], "PASS")
            self.assertEqual(result["status"], "PASS")
            self.assertEqual(result["provider_submission_count"], 1)
            self.assertEqual(len(fake.calls), 1)
            self.assertEqual(
                {path.name for path in root.iterdir()},
                {
                    sentinel.INTENT_NAME,
                    sentinel.RECEIPT_NAME,
                    sentinel.EVIDENCE_NAME,
                },
            )
            for forbidden in (
                "request_journal",
                "records",
                "failures",
                "aggregate_records.jsonl",
                "repetition_records.jsonl",
            ):
                self.assertFalse((root / forbidden).exists())

    def test_wrong_returned_model_exhausts_identity(self) -> None:
        fake = FakeResponses(
            FakeResponse(valid_output(), returned_model="gpt-5.6-terra-alias")
        )
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "sentinel"
            with self.assertRaisesRegex(sentinel.SentinelFailedError, "exhausted"):
                sentinel.run_sentinel(root, make_adapter(fake))
            evidence = runner.load_json(root / sentinel.EVIDENCE_NAME)
            self.assertEqual(evidence["status"], "FAIL")
            self.assertEqual(len(fake.calls), 1)
            with self.assertRaises(Exception):
                sentinel_verifier.verify_sentinel(root)

    def test_invalid_schema_and_wrong_synthetic_label_fail(self) -> None:
        responses = (
            FakeResponse("not-json"),
            FakeResponse(valid_output(label="SYNTHETIC-BETA")),
            FakeResponse(valid_output(label="REAL-LABEL-NOT-ALLOWED")),
        )
        for index, response in enumerate(responses):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as raw:
                fake = FakeResponses(response)
                root = Path(raw) / "sentinel"
                with self.assertRaises(sentinel.SentinelFailedError):
                    sentinel.run_sentinel(root, make_adapter(fake))
                self.assertEqual(len(fake.calls), 1)
                self.assertEqual(
                    runner.load_json(root / sentinel.EVIDENCE_NAME)["status"],
                    "FAIL",
                )

    def test_invalid_token_accounting_fails(self) -> None:
        for usage in (
            FakeUsage(11, 7, 19),
            FakeUsage(11, 7, None),
            FakeUsage(True, 7, 8),
        ):
            with self.subTest(
                usage=usage.__dict__
            ), tempfile.TemporaryDirectory() as raw:
                fake = FakeResponses(FakeResponse(valid_output(), usage=usage))
                root = Path(raw) / "sentinel"
                with self.assertRaises(sentinel.SentinelFailedError):
                    sentinel.run_sentinel(root, make_adapter(fake))
                evidence = runner.load_json(root / sentinel.EVIDENCE_NAME)
                self.assertFalse(evidence["token_accounting_pass"])
                self.assertEqual(len(fake.calls), 1)

    def test_second_submission_is_prevented(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "sentinel"
            _, first = self.run_fake(root)
            second = FakeResponses()
            with self.assertRaisesRegex(RuntimeError, "may not be submitted again"):
                sentinel.run_sentinel(root, make_adapter(second))
            self.assertEqual(len(first.calls), 1)
            self.assertEqual(len(second.calls), 0)

    def test_ambiguous_crash_leaves_intent_and_prevents_retry(self) -> None:
        first = FakeResponses(error=RuntimeError("synthetic crash after submission"))
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "sentinel"
            with self.assertRaisesRegex(RuntimeError, "synthetic crash"):
                sentinel.run_sentinel(root, make_adapter(first))
            intent, receipt, evidence = sentinel.sentinel_paths(root)
            self.assertTrue(intent.exists())
            self.assertFalse(receipt.exists())
            self.assertFalse(evidence.exists())
            second = FakeResponses()
            with self.assertRaisesRegex(RuntimeError, "AMBIGUOUS"):
                sentinel.run_sentinel(root, make_adapter(second))
            self.assertEqual(len(first.calls), 1)
            self.assertEqual(len(second.calls), 0)

    def test_tampered_evidence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw) / "sentinel"
            self.run_fake(root)
            evidence_path = root / sentinel.EVIDENCE_NAME
            evidence = runner.load_json(evidence_path)
            evidence["input_tokens"] += 1
            evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "evidence mismatch"):
                sentinel_verifier.verify_sentinel(root)

    def test_batch_refuses_absent_final_authorization(self) -> None:
        manifest = runner.load_json(HARNESS_MANIFEST)
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            manifest_path = root / "harness.json"
            authorization_root = root / "authorization"
            authorization_manifest = authorization_root / "authorization.json"
            output_root = root / "scientific-output"
            source_root = root / "source"
            data_root = root / "data"
            verbalization_harness_root = root / "verbalization-harness"
            verbalizations_root = root / "verbalizations"
            manifest["future_execution"] = {
                "manifest_path": str(manifest_path.resolve()),
                "source_root": str(source_root.resolve()),
                "data_root": str(data_root.resolve()),
                "verbalization_harness_root": str(verbalization_harness_root.resolve()),
                "verbalizations_root": str(verbalizations_root.resolve()),
                "authorization_manifest_path": str(authorization_manifest.resolve()),
                "authorization_root": str(authorization_root.resolve()),
                "output_root": str(output_root.absolute()),
                "command": "synthetic-test-only",
            }
            manifest["execution_authorization"]["manifest_path"] = str(
                authorization_manifest.resolve()
            )
            manifest["execution_authorization"]["checkout_root"] = str(
                authorization_root.resolve()
            )
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            poison_client = SimpleNamespace(
                responses=SimpleNamespace(
                    create=lambda **_: self.fail("provider client was called")
                )
            )
            with mock.patch.object(runner, "verify_boundaries", return_value=ROOT):
                with self.assertRaisesRegex(RuntimeError, "absent"):
                    runner.main(
                        [
                            "--manifest",
                            str(manifest_path),
                            "--source-root",
                            str(source_root),
                            "--data-root",
                            str(data_root),
                            "--verbalization-harness-root",
                            str(verbalization_harness_root),
                            "--verbalizations-root",
                            str(verbalizations_root),
                            "--authorization-manifest",
                            str(authorization_manifest),
                            "--authorization-root",
                            str(authorization_root),
                            "--output-root",
                            str(output_root),
                        ],
                        client=poison_client,
                    )
            self.assertFalse(output_root.exists())

    def test_synthetic_final_authorization_tag_unlocks_preflight(self) -> None:
        additions = [
            "phase_b/exp3_v2/EXP3_V2_INFERENCE_EXECUTION_AUTHORIZATION_MANIFEST_001.json",
            "phase_b/exp3_v2/inference_sentinel_001/EXP3_V2_INFERENCE_SENTINEL_EVIDENCE_001.json",
            "phase_b/exp3_v2/inference_sentinel_001/sentinel_intent.json",
            "phase_b/exp3_v2/inference_sentinel_001/sentinel_receipt.json",
        ]
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw).resolve()
            git(root, "init")
            git(root, "config", "user.name", "Synthetic Test")
            git(root, "config", "user.email", "synthetic@example.invalid")
            manifest_path = (
                root / "phase_b/exp3_v2/EXP3_V2_INFERENCE_HARNESS_MANIFEST_001.json"
            )
            manifest_path.parent.mkdir(parents=True)
            runner_hash = runner.sha256_file(Path(runner.__file__))
            runtime_hash = (
                "8c2fbb68bda87621b37dab65fc54be26ed09cd1ca0e56b8a18a9a02613d70d6c"
            )
            harness = {
                "manifest_path": str(manifest_path.relative_to(root)),
                "prospective_tag": "exp3-v2-inference-harness-frozen-001",
                "schedule": {"sha256": "e" * 64},
                "sentinel": {
                    "prompt_sha256": runner.sha256_bytes(
                        sentinel.SENTINEL_PROMPT.encode("utf-8")
                    )
                },
                "harness_artifacts": [
                    {
                        "path": "phase_b/exp3_v2/run_exp3v2_inference.py",
                        "sha256": runner_hash,
                    },
                    {
                        "path": "phase_b/exp3_v2/EXP3_V2_INFERENCE_RUNTIME_LOCK_001.json",
                        "sha256": runtime_hash,
                    },
                ],
                "execution_authorization": {
                    "prospective_tag": "exp3-v2-inference-execution-frozen-001",
                    "manifest_path": str(
                        root
                        / "phase_b/exp3_v2/EXP3_V2_INFERENCE_EXECUTION_AUTHORIZATION_MANIFEST_001.json"
                    ),
                    "checkout_root": str(root),
                    "authorization_commit_additions": additions,
                    "sentinel_artifact_directory": "phase_b/exp3_v2/inference_sentinel_001",
                },
            }
            manifest_path.write_text(json.dumps(harness), encoding="utf-8")
            git(root, "add", str(manifest_path.relative_to(root)))
            git(root, "commit", "-m", "synthetic harness")
            git(
                root,
                "tag",
                "-a",
                "exp3-v2-inference-harness-frozen-001",
                "-m",
                "synthetic harness",
            )
            harness_commit = git(root, "rev-parse", "HEAD")

            sentinel_root = root / "phase_b/exp3_v2/inference_sentinel_001"
            self.run_fake(sentinel_root)
            verified = sentinel_verifier.verify_sentinel(sentinel_root)
            authorization_path = root / additions[0]
            authorization = {
                "schema_version": "1.0",
                "manifest_kind": "EXP3_V2_INFERENCE_EXECUTION_AUTHORIZATION",
                "status": "FROZEN_BEFORE_INFERENCE",
                "prospective_tag": "exp3-v2-inference-execution-frozen-001",
                "tag_created": True,
                "manifest_path": additions[0],
                "human_approval": {
                    "approved": True,
                    "approved_at": "2026-09-04T00:00:00+00:00",
                    "approval_text_sha256": "a" * 64,
                    "scope": "EXP3_V2_1080_JOB_INFERENCE_EXECUTION",
                },
                "harness_binding": {
                    "tag": "exp3-v2-inference-harness-frozen-001",
                    "commit": harness_commit,
                    "manifest_path": str(manifest_path.relative_to(root)),
                    "manifest_sha256": runner.sha256_file(manifest_path),
                },
                "sentinel_binding": {
                    "sentinel_id": sentinel.SENTINEL_ID,
                    "provider_submission_count": 1,
                    "evidence_path": additions[1],
                    "evidence_sha256": verified["evidence_sha256"],
                    "intent_path": additions[2],
                    "intent_sha256": verified["intent_sha256"],
                    "receipt_path": additions[3],
                    "receipt_sha256": verified["receipt_sha256"],
                    "returned_model": runner.MODEL,
                    "token_accounting_pass": True,
                    "verifier_pass": True,
                },
                "integrity_bindings": {
                    "schedule_sha256": "e" * 64,
                    "runner_sha256": runner_hash,
                    "runtime_lock_sha256": runtime_hash,
                },
                "non_self_referential": {
                    "manifest_sha256_recorded": False,
                    "authorization_commit_recorded": False,
                    "tag_object_recorded": False,
                },
            }
            authorization_path.write_text(json.dumps(authorization), encoding="utf-8")
            git(root, "add", *additions)
            git(root, "commit", "-m", "synthetic execution authorization")
            git(
                root,
                "tag",
                "-a",
                "exp3-v2-inference-execution-frozen-001",
                "-m",
                "synthetic authorization",
            )
            git(
                root,
                "checkout",
                "--detach",
                "exp3-v2-inference-execution-frozen-001^{}",
            )
            result = runner.verify_execution_authorization(
                harness,
                manifest_path,
                root,
                authorization_path,
                root,
            )
            self.assertEqual(result["status"], "FROZEN_BEFORE_INFERENCE")

    def test_no_production_cli_security_bypass_or_sentinel_retry(self) -> None:
        source = Path(sentinel.__file__).read_text(encoding="utf-8").lower()
        self.assertNotIn("--disable", source)
        self.assertNotIn("--skip", source)
        self.assertNotIn("max_structural_retries", source)
        self.assertEqual(source.count("adapter.create_response("), 1)


if __name__ == "__main__":
    unittest.main()
