from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest

import jsonschema

from phase_b.conditions.builders import RenderedPrompt
from phase_b.conditions.parser import parse_diagnostic_output
from phase_b.execution.openai_adapter import OpenAIAdapter
from phase_b.exp3_v2 import build_exp3v2_inference_schedule as scheduler
from phase_b.exp3_v2 import run_exp3v2_inference as runner
from phase_b.exp3_v2 import validate_exp3v2_inference_runtime as runtime_validator
from phase_b.exp3_v2 import verify_exp3v2_inference as verifier


ROOT = Path(__file__).resolve().parents[2]
SCHEDULE = ROOT / "phase_b/exp3_v2/exp3v2_inference_schedule_001.json"
CONTRACT = ROOT / "phase_b/exp3_v2/exp3v2_inference_schedule_contract_001.json"
RUNTIME_LOCK = ROOT / "phase_b/exp3_v2/EXP3_V2_INFERENCE_RUNTIME_LOCK_001.json"
HARNESS_MANIFEST = ROOT / "phase_b/exp3_v2/EXP3_V2_INFERENCE_HARNESS_MANIFEST_001.json"


class FakeUsage:
    input_tokens = 11
    output_tokens = 7
    total_tokens = 18

    def model_dump(self, *, mode: str) -> dict:
        del mode
        return {"input_tokens": 11, "output_tokens": 7, "total_tokens": 18}


class FakeResponse:
    def __init__(self, raw: str, index: int) -> None:
        self.output_text = raw
        self.model = runner.MODEL
        self.id = f"synthetic-response-{index}"
        self._request_id = f"synthetic-request-{index}"
        self.usage = FakeUsage()

    def model_dump(self, *, mode: str) -> dict:
        del mode
        return {
            "id": self.id,
            "model": self.model,
            "output_text": self.output_text,
            "usage": self.usage.model_dump(mode="json"),
        }


class FakeResponses:
    def __init__(
        self, outputs: list[str] | None = None, error: Exception | None = None
    ) -> None:
        self.outputs = list(outputs or [])
        self.error = error
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        raw = self.outputs.pop(0) if self.outputs else valid_output()
        return FakeResponse(raw, len(self.calls))


class FailIfCalledResponses(FakeResponses):
    def create(self, **kwargs):
        raise AssertionError(f"resume unexpectedly submitted a request: {kwargs}")


def valid_output(*, insight_ids: list[str] | None = None) -> str:
    return json.dumps(
        {
            "predicted_label": "Normal",
            "abstain": False,
            "used_insight_ids": insight_ids or [],
            "reasoning_summary": "Synthetic structural response.",
        },
        separators=(",", ":"),
    )


class FakeAssets:
    provider_schema = {
        "type": "object",
        "additionalProperties": False,
        "required": [
            "predicted_label",
            "abstain",
            "used_insight_ids",
            "reasoning_summary",
        ],
        "properties": {
            "predicted_label": {"type": ["string", "null"]},
            "abstain": {"type": "boolean"},
            "used_insight_ids": {"type": "array", "items": {"type": "string"}},
            "reasoning_summary": {"type": "string"},
        },
    }
    protocol = {
        "label_space": [
            "CLS-ZOGAA",
            "CLS-OJNSG",
            "CLS-R463B",
            "CLS-Z3ISU",
            "Normal",
        ]
    }

    def render(self, entry: dict) -> RenderedPrompt:
        peer_ids = () if entry["condition"] == "A" else ("INS-001",)
        text = (
            "Synthetic diagnostic prompt.\n"
            "CASE TO DIAGNOSE\n"
            "Neutral synthetic observations only."
        )
        digest = hashlib.sha256(text.encode()).hexdigest()
        input_hash = hashlib.sha256(b"Neutral synthetic observations only.").hexdigest()
        return RenderedPrompt(
            agent_id=entry["agent_id"],
            condition=entry["condition"],
            text=text,
            prompt_hash=digest,
            input_hash=input_hash,
            available_insight_ids=peer_ids,
            character_count=len(text),
        )

    def parse(self, raw: str, available_insight_ids: tuple[str, ...]) -> dict:
        return parse_diagnostic_output(
            raw,
            label_space=self.protocol["label_space"],
            allowed_insight_ids=available_insight_ids,
        )


def adapter(responses: FakeResponses) -> OpenAIAdapter:
    return OpenAIAdapter(
        requested_model=runner.MODEL,
        client=SimpleNamespace(responses=responses),
    )


def git(path: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=path, text=True).strip()


class Exp3V2InferenceHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
        cls.schedule = json.loads(SCHEDULE.read_text(encoding="utf-8"))
        cls.schedule_sha = hashlib.sha256(SCHEDULE.read_bytes()).hexdigest()
        cls.assets = FakeAssets()

    def test_schedule_has_all_1080_positions_without_rng(self) -> None:
        expected = scheduler.build_schedule(self.contract)
        self.assertEqual(self.schedule, expected)
        scheduler.validate_schedule(self.schedule)
        self.assertEqual(len(self.schedule), 1080)
        self.assertEqual(len({item["block_index"] for item in self.schedule}), 360)
        self.assertEqual(
            Counter(item["condition"] for item in self.schedule),
            Counter({"A": 360, "B": 360, "E": 360}),
        )
        self.assertEqual(
            Counter(
                (item["condition"], item["position_in_block"]) for item in self.schedule
            ),
            Counter({(c, p): 120 for c in "ABE" for p in (1, 2, 3)}),
        )
        source = (
            ROOT / "phase_b/exp3_v2/build_exp3v2_inference_schedule.py"
        ).read_text()
        self.assertNotIn("import random", source)
        self.assertIsNone(self.contract["schedule_seed"])

    def test_exact_canonical_case_agent_repetition_rotation(self) -> None:
        self.assertEqual(
            list(dict.fromkeys(item["physical_case_id"] for item in self.schedule)),
            scheduler.EXPECTED_CASES,
        )
        for entry in self.schedule:
            expected = scheduler.EXPECTED_ROTATION[entry["block_index"] % 3]
            self.assertEqual(
                entry["condition"], expected[entry["position_in_block"] - 1]
            )

    def test_all_schemas_are_valid_draft_2020_12(self) -> None:
        for path in sorted(runner.SCHEMA_DIR.glob("*.schema.json")):
            schema = json.loads(path.read_text(encoding="utf-8"))
            jsonschema.Draft202012Validator.check_schema(schema)

    def test_review_manifest_is_non_self_referential_and_binds_every_artifact(
        self,
    ) -> None:
        manifest = json.loads(HARNESS_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], "HARNESS_FROZEN_FOR_INFERENCE")
        self.assertTrue(manifest["tag_created"])
        self.assertEqual(
            manifest["human_freeze_approval"],
            "APPROVO IL FREEZE PUBBLICO DELL’HARNESS DI INFERENZA EXP3_V2",
        )
        self.assertEqual(
            manifest["prospective_tag"],
            "exp3-v2-inference-harness-frozen-001",
        )
        self.assertFalse(
            manifest["non_self_referential"]["manifest_sha256_recorded_in_manifest"]
        )
        self.assertNotIn(
            manifest["manifest_path"],
            {item["path"] for item in manifest["harness_artifacts"]},
        )
        self.assertEqual(manifest["freeze_commit_allowlist"]["count"], 24)
        self.assertEqual(len(manifest["inputs"]["cases"]), 30)
        self.assertEqual(
            [item["physical_case_id"] for item in manifest["inputs"]["cases"]],
            scheduler.EXPECTED_CASES,
        )
        for artifact in manifest["harness_artifacts"]:
            path = ROOT / artifact["path"]
            self.assertEqual(path.stat().st_size, artifact["size_bytes"])
            self.assertEqual(runner.sha256_file(path), artifact["sha256"])

    def test_runtime_candidate_is_exact_and_does_not_inspect_credentials(self) -> None:
        result = runtime_validator.validate_runtime(RUNTIME_LOCK)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["packages"]["openai"], "3.6.0")
        self.assertEqual(result["packages"]["jsonschema"], "4.25.0")
        self.assertFalse(result["credential_environment_inspected"])

    def test_runtime_extra_missing_or_altered_dependencies_fail_closed(self) -> None:
        lock = json.loads(RUNTIME_LOCK.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as raw:
            root = Path(raw)
            for name, mutate in (
                ("missing", lambda env: env.__setitem__("not-installed", "1")),
                ("altered", lambda env: env.__setitem__("openai", "0.0.0")),
                ("extra", lambda env: env.pop("sniffio")),
            ):
                candidate = json.loads(json.dumps(lock))
                mutate(candidate["complete_environment"])
                path = root / f"{name}.json"
                path.write_text(json.dumps(candidate), encoding="utf-8")
                with self.assertRaises(RuntimeError):
                    runtime_validator.validate_runtime(path)

    def test_condition_isolation_with_frozen_builder_and_synthetic_text(self) -> None:
        texts = {
            case_id: "Neutral synthetic observations only."
            for case_id in scheduler.EXPECTED_CASES
        }
        assets = runner.FrozenAssets(ROOT, texts)
        base = self.schedule[0]
        rendered = {
            condition: assets.render({**base, "condition": condition})
            for condition in ("A", "B", "E")
        }
        self.assertEqual(rendered["A"].available_insight_ids, ())
        self.assertEqual(len(rendered["B"].available_insight_ids), 6)
        self.assertEqual(len(rendered["E"].available_insight_ids), 6)
        self.assertNotIn(base["physical_case_id"], rendered["A"].text)
        source = (ROOT / "phase_b/exp3_v2/run_exp3v2_inference.py").read_text().lower()
        self.assertNotIn("pseudolabel_mapping.json", source)

    def test_retry_is_limited_to_two_structural_corrections(self) -> None:
        responses = FakeResponses(["not-json", "still-not-json", valid_output()])
        with tempfile.TemporaryDirectory() as raw:
            record = runner.execute_job(
                self.schedule[0],
                self.assets.render(self.schedule[0]),
                self.assets,
                Path(raw),
                adapter(responses),
            )
        self.assertEqual(record["retry_count"], 2)
        self.assertFalse(record["parse_failure"])
        self.assertEqual(len(responses.calls), 3)
        for call in responses.calls:
            self.assertFalse(call["store"])
            self.assertEqual(call["model"], runner.MODEL)
            self.assertEqual(call["reasoning"], {"effort": "medium"})
            self.assertEqual(call["max_output_tokens"], 512)
            self.assertNotIn("temperature", call)
            self.assertNotIn("seed", call)
            self.assertNotIn("previous_response_id", call)

    def test_third_structural_failure_becomes_abstention(self) -> None:
        responses = FakeResponses(["bad-one", "bad-two", "bad-three"])
        with tempfile.TemporaryDirectory() as raw:
            record = runner.execute_job(
                self.schedule[0],
                self.assets.render(self.schedule[0]),
                self.assets,
                Path(raw),
                adapter(responses),
            )
        self.assertTrue(record["parse_failure"])
        self.assertEqual(record["parsed_final_output"], runner.PARSE_FAILURE_OUTPUT)
        self.assertEqual(len(responses.calls), 3)

    def test_infrastructure_failure_leaves_ambiguous_intent_and_stops_resume(
        self,
    ) -> None:
        responses = FakeResponses(
            error=RuntimeError("synthetic infrastructure failure")
        )
        with tempfile.TemporaryDirectory() as raw:
            output = Path(raw)
            with self.assertRaisesRegex(RuntimeError, "synthetic infrastructure"):
                runner.execute_job(
                    self.schedule[0],
                    self.assets.render(self.schedule[0]),
                    self.assets,
                    output,
                    adapter(responses),
                )
            paths = runner.journal_paths(output, 0, 1)
            self.assertTrue(paths.intent.exists())
            self.assertFalse(paths.response.exists())
            self.assertTrue(runner.failure_path(output, 0, 1).exists())
            with self.assertRaisesRegex(RuntimeError, "AMBIGUOUS"):
                runner.scan_ambiguous_state([self.schedule[0]], self.assets, output)
            self.assertEqual(len(responses.calls), 1)

    def test_crash_only_intent_is_recorded_ambiguous_before_adapter_creation(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            output = Path(raw) / "output"
            output.mkdir()
            entry = self.schedule[0]
            rendered = self.assets.render(entry)
            intent = runner.make_intent(entry, rendered, 1, rendered.text)
            paths = runner.journal_paths(output, 0, 1)
            runner.atomic_write_immutable(
                paths.intent, runner.canonical_json_bytes(intent)
            )
            factory_called = False

            def forbidden_factory():
                nonlocal factory_called
                factory_called = True
                raise AssertionError("adapter factory must not run")

            with self.assertRaisesRegex(RuntimeError, "AMBIGUOUS"):
                runner.run_execution(
                    self.schedule,
                    self.assets,
                    output,
                    None,
                    self.schedule_sha,
                    forbidden_factory,
                )
            self.assertFalse(factory_called)
            failure = json.loads(
                runner.failure_path(output, 0, 1).read_text(encoding="utf-8")
            )
            self.assertEqual(failure["failure_kind"], "ambiguous_request_state")

    def test_exclusive_lock_refuses_second_process_and_is_not_auto_removed(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            lock = Path(raw) / "execution.lock"
            lock.write_text("stale\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "human removal"):
                with runner.ExclusiveLock(lock):
                    pass
            self.assertTrue(lock.exists())

    def test_full_1080_fake_responses_resume_tamper_and_deterministic_finalization(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            output = Path(raw) / "output"
            responses = FakeResponses()
            first = runner.run_execution(
                self.schedule,
                self.assets,
                output,
                adapter(responses),
                self.schedule_sha,
            )
            self.assertEqual(len(responses.calls), 1080)
            self.assertEqual(first["repetition_record_count"], 1080)
            self.assertEqual(first["aggregate_record_count"], 360)
            verification = verifier.verify_output_set(
                self.schedule, self.assets, output, self.schedule_sha
            )
            self.assertEqual(verification["status"], "PASS")
            first_manifest_bytes = (
                output / "inference_output_hash_manifest.json"
            ).read_bytes()

            second = runner.run_execution(
                self.schedule,
                self.assets,
                output,
                adapter(FailIfCalledResponses()),
                self.schedule_sha,
            )
            self.assertEqual(second, first)
            self.assertEqual(
                (output / "inference_output_hash_manifest.json").read_bytes(),
                first_manifest_bytes,
            )

            record = runner.record_path(output, 17)
            original = record.read_bytes()
            value = json.loads(original)
            value["prompt_hash"] = "0" * 64
            record.write_text(json.dumps(value), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "prompt/input hash"):
                verifier.verify_output_set(
                    self.schedule, self.assets, output, self.schedule_sha
                )
            record.write_bytes(original)

            response_path = runner.journal_paths(output, 17, 1).response
            response_original = response_path.read_bytes()
            response = json.loads(response_original)
            response["response"]["raw_output"] = valid_output(insight_ids=["INS-001"])
            response_path.write_text(json.dumps(response), encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "durable provider response"):
                verifier.verify_output_set(
                    self.schedule, self.assets, output, self.schedule_sha
                )
            response_path.write_bytes(response_original)

    def test_verify_boundaries_requires_annotated_tags_detached_heads_and_cleanliness(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as raw:
            base = Path(raw)
            repo = base / "harness"
            repo.mkdir()
            git(repo, "init")
            git(repo, "config", "user.name", "Synthetic Test")
            git(repo, "config", "user.email", "synthetic@example.invalid")
            artifact = repo / "artifact.txt"
            artifact.write_text("synthetic\n", encoding="utf-8")
            git(repo, "add", "artifact.txt")
            git(repo, "commit", "-m", "synthetic upstream")
            upstream = []
            names = [
                "exp3-v2-heldout-frozen-002",
                "exp3-v2-heldout-data-frozen-001",
                "exp3-v2-verbalization-harness-frozen-001",
                "exp3-v2-verbalizations-frozen-001",
            ]
            for name in names:
                git(repo, "tag", "-a", name, "-m", name)
                upstream.append(
                    {
                        "name": name,
                        "tag_object": git(repo, "rev-parse", name),
                        "peeled_commit": git(repo, "rev-parse", f"{name}^{{commit}}"),
                    }
                )
            data = base / "verbalizations"
            subprocess.run(
                ["git", "clone", "--quiet", str(repo), str(data)], check=True
            )
            git(data, "checkout", "--detach", "exp3-v2-verbalizations-frozen-001^{}")

            manifest_dir = repo / "phase_b/exp3_v2"
            manifest_dir.mkdir(parents=True)
            manifest = {
                "manifest_path": "phase_b/exp3_v2/manifest.json",
                "status": "HARNESS_FROZEN_FOR_INFERENCE",
                "tag_created": True,
                "prospective_tag": "synthetic-inference-harness",
                "upstream_tags": upstream,
                "harness_artifacts": [
                    {
                        "path": "artifact.txt",
                        "size_bytes": artifact.stat().st_size,
                        "sha256": runner.sha256_file(artifact),
                    }
                ],
            }
            manifest_path = manifest_dir / "manifest.json"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            git(repo, "add", "phase_b/exp3_v2/manifest.json")
            git(repo, "commit", "-m", "synthetic harness")
            git(repo, "tag", "-a", "synthetic-inference-harness", "-m", "synthetic")
            git(repo, "checkout", "--detach", "synthetic-inference-harness^{}")
            roots = {name: data for name in names}
            root = runner.verify_boundaries(manifest, manifest_path, roots)
            self.assertEqual(root, repo.resolve())

            artifact.write_text("tampered\n", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "not clean"):
                runner.verify_boundaries(manifest, manifest_path, roots)

    def test_production_cli_exposes_no_security_bypass(self) -> None:
        source = (ROOT / "phase_b/exp3_v2/run_exp3v2_inference.py").read_text().lower()
        self.assertNotIn("--disable", source)
        self.assertNotIn("--skip", source)
        self.assertNotIn("enforce_boundaries=false", source.replace(" ", ""))
        self.assertIn("--authorization-manifest", source)
        self.assertIn("--authorization-root", source)
        self.assertEqual(runner.TIMEOUT_SECONDS, 120.0)


if __name__ == "__main__":
    unittest.main()
