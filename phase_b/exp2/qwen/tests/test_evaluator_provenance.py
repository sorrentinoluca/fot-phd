from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import subprocess
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from phase_b.exp2.qwen import evaluate_qwen as evaluator


TERRA_FREEZE_TAG = "phase-b-inference-frozen"
TERRA_FREEZE_COMMIT = "11c34358e28e875cd5c7249061ac2b89ffcd42f4"


def valid_manifest() -> dict:
    return {
        "aggregate_record_count": 180,
        "artifact_version": "1",
        "artifacts": deepcopy(evaluator.CANONICAL_INFERENCE_ARTIFACTS),
        "ground_truth_included": False,
        "repetition_record_count": 540,
        "schedule_reference": {
            "path": evaluator.SCHEDULE_RELATIVE_PATH,
            "sha256": evaluator.SCHEDULE_SHA256,
        },
        "status": evaluator.INFERENCE_MANIFEST_STATUS,
    }


def valid_metadata() -> dict:
    return {
        "aggregate_records": 180,
        "ground_truth_joined": False,
        "metrics_calculated": False,
        "repetition_records": 540,
        "schedule_sha256": evaluator.SCHEDULE_SHA256,
        "status": evaluator.METADATA_STATUS,
    }


class QwenEvaluatorProvenanceTests(unittest.TestCase):
    def mocked_verify(
        self,
        manifest: dict | None = None,
        metadata: dict | None = None,
        hash_overrides: dict[Path, str] | None = None,
    ):
        manifest = valid_manifest() if manifest is None else manifest
        metadata = valid_metadata() if metadata is None else metadata
        hashes = {
            (evaluator.ROOT / relative).resolve(): expected
            for relative, expected in evaluator.CANONICAL_INFERENCE_ARTIFACTS.items()
        }
        hashes.update(
            {
                evaluator.SCHEDULE_PATH.resolve(): evaluator.SCHEDULE_SHA256,
                evaluator.FROZEN_EVALUATOR_PATH.resolve(): (
                    evaluator.FROZEN_EVALUATOR_SHA256
                ),
                evaluator.INFERENCE_MANIFEST_PATH.resolve(): (
                    evaluator.INFERENCE_MANIFEST_SHA256
                ),
            }
        )
        if hash_overrides:
            hashes.update(
                {Path(path).resolve(): value for path, value in hash_overrides.items()}
            )

        def load(path: Path):
            if path == evaluator.INFERENCE_MANIFEST_PATH:
                return manifest
            if path == evaluator.METADATA_PATH:
                return metadata
            raise AssertionError(f"unexpected JSON access: {path}")

        def sha(path: Path):
            resolved = Path(path).resolve()
            if resolved not in hashes:
                raise AssertionError(f"unexpected hash access: {resolved}")
            return hashes[resolved]

        return (
            patch.object(
                evaluator,
                "git_output",
                return_value=evaluator.QWEN_PREDICTIONS_FREEZE_COMMIT,
            ),
            patch.object(
                evaluator.subprocess,
                "run",
                return_value=SimpleNamespace(returncode=0),
            ),
            patch.object(evaluator, "load_json", side_effect=load),
            patch.object(evaluator, "sha256_file", side_effect=sha),
        )

    def assert_mocked_verify_fails(
        self,
        manifest: dict | None = None,
        metadata: dict | None = None,
        hash_overrides: dict[Path, str] | None = None,
    ) -> None:
        patches = self.mocked_verify(manifest, metadata, hash_overrides)
        with patches[0], patches[1], patches[2], patches[3]:
            with self.assertRaises(RuntimeError):
                evaluator.verify_qwen_inference()

    def test_current_qwen_predictions_freeze_verifies(self):
        provenance = evaluator.verify_qwen_inference()
        self.assertEqual(
            provenance["qwen_predictions_freeze_tag"],
            evaluator.QWEN_PREDICTIONS_FREEZE_TAG,
        )
        self.assertEqual(
            provenance["qwen_predictions_freeze_commit"],
            evaluator.QWEN_PREDICTIONS_FREEZE_COMMIT,
        )

    def test_pre_evaluation_verification_has_no_evaluator_side_data_access(self):
        with patch.object(evaluator, "load_json", wraps=evaluator.load_json) as load:
            evaluator.verify_qwen_inference()
        self.assertEqual(
            [call.args[0] for call in load.call_args_list],
            [evaluator.INFERENCE_MANIFEST_PATH, evaluator.METADATA_PATH],
        )
        source = Path(evaluator.__file__).read_text(encoding="utf-8")
        self.assertNotIn("MAPPING_PATH", source)
        self.assertNotIn("HELDOUT_MANIFEST_PATH", source)
        self.assertNotIn("load_case_truth", source)

    def test_missing_or_wrong_freeze_tag_is_rejected(self):
        with patch.object(
            evaluator,
            "git_output",
            side_effect=RuntimeError("Qwen predictions freeze tag is missing"),
        ):
            with self.assertRaises(RuntimeError):
                evaluator.verify_qwen_inference()

        with patch.object(evaluator, "git_output", return_value="0" * 40):
            with self.assertRaisesRegex(RuntimeError, "tag target mismatch"):
                evaluator.verify_qwen_inference()

    def test_git_output_converts_missing_tag_to_runtime_error(self):
        with patch.object(
            evaluator.subprocess,
            "check_output",
            side_effect=subprocess.CalledProcessError(128, ["git"]),
        ):
            with self.assertRaisesRegex(RuntimeError, "freeze tag is missing"):
                evaluator.git_output("rev-parse", "missing")

    def test_non_ancestor_freeze_commit_is_rejected(self):
        patches = self.mocked_verify()
        with patches[0], patch.object(
            evaluator.subprocess,
            "run",
            return_value=SimpleNamespace(returncode=1),
        ):
            with self.assertRaisesRegex(RuntimeError, "does not derive"):
                evaluator.verify_qwen_inference()

    def test_manifest_status_counts_paths_and_hashes_are_fail_closed(self):
        mutations = []

        manifest = valid_manifest()
        manifest["status"] = "MUTABLE"
        mutations.append(manifest)

        manifest = valid_manifest()
        manifest["artifact_version"] = "2"
        mutations.append(manifest)

        manifest = valid_manifest()
        manifest["ground_truth_included"] = True
        mutations.append(manifest)

        manifest = valid_manifest()
        manifest["repetition_record_count"] = 539
        mutations.append(manifest)

        manifest = valid_manifest()
        manifest["aggregate_record_count"] = 179
        mutations.append(manifest)

        manifest = valid_manifest()
        manifest["artifacts"].pop(
            "phase_b/exp2/qwen/inference/repetition_records.jsonl"
        )
        mutations.append(manifest)

        manifest = valid_manifest()
        artifact = "phase_b/exp2/qwen/inference/aggregate_records.jsonl"
        manifest["artifacts"][artifact] = "0" * 64
        mutations.append(manifest)

        manifest = valid_manifest()
        manifest["schedule_reference"]["path"] = "wrong/schedule.json"
        mutations.append(manifest)

        manifest = valid_manifest()
        manifest["schedule_reference"]["sha256"] = "0" * 64
        mutations.append(manifest)

        for index, mutated in enumerate(mutations):
            with self.subTest(mutation=index):
                self.assert_mocked_verify_fails(manifest=mutated)

        self.assert_mocked_verify_fails(
            hash_overrides={evaluator.AGGREGATE_PATH: "0" * 64}
        )
        self.assert_mocked_verify_fails(
            hash_overrides={evaluator.SCHEDULE_PATH: "0" * 64}
        )
        self.assert_mocked_verify_fails(
            hash_overrides={evaluator.INFERENCE_MANIFEST_PATH: "0" * 64}
        )

    def test_metadata_ground_truth_or_metrics_declarations_are_rejected(self):
        for field in ("ground_truth_joined", "metrics_calculated"):
            metadata = valid_metadata()
            metadata[field] = True
            with self.subTest(field=field):
                self.assert_mocked_verify_fails(metadata=metadata)

    def test_metadata_status_counts_and_schedule_are_rejected_when_incoherent(self):
        for field, invalid in (
            ("status", "WRONG"),
            ("repetition_records", 539),
            ("aggregate_records", 179),
            ("schedule_sha256", "0" * 64),
        ):
            metadata = valid_metadata()
            metadata[field] = invalid
            with self.subTest(field=field):
                self.assert_mocked_verify_fails(metadata=metadata)

    def test_future_results_manifest_and_report_use_only_qwen_provenance(self):
        provenance = {
            "qwen_predictions_freeze_tag": evaluator.QWEN_PREDICTIONS_FREEZE_TAG,
            "qwen_predictions_freeze_commit": (
                evaluator.QWEN_PREDICTIONS_FREEZE_COMMIT
            ),
            "qwen_inference_manifest_sha256": evaluator.INFERENCE_MANIFEST_SHA256,
            "aggregate_predictions_sha256": (
                evaluator.CANONICAL_INFERENCE_ARTIFACTS[
                    "phase_b/exp2/qwen/inference/aggregate_records.jsonl"
                ]
            ),
            "schedule_sha256": evaluator.SCHEDULE_SHA256,
            "frozen_evaluator_code_path": str(
                evaluator.FROZEN_EVALUATOR_PATH.relative_to(evaluator.ROOT)
            ),
            "frozen_evaluator_code_sha256": evaluator.FROZEN_EVALUATOR_SHA256,
            "evaluator_binding": (
                "phase_b.final_evaluation.evaluate_frozen_predictions"
            ),
        }
        synthetic_results = {"reproducibility": {}}
        synthetic_artifacts = {"primary_metrics.csv": b"synthetic\n"}
        terra_report = (
            "# Phase B final offline evaluation\n\n"
            f"- Inference freeze: `{TERRA_FREEZE_TAG}` at "
            f"`{TERRA_FREEZE_COMMIT}`.\n"
        )

        with tempfile.TemporaryDirectory(
            prefix="qwen-evaluator-test-", dir=evaluator.LANE_DIR
        ) as temporary:
            output_dir = Path(temporary)
            with (
                patch.object(
                    evaluator, "verify_qwen_inference", return_value=provenance
                ),
                patch.object(
                    evaluator.frozen_evaluator,
                    "build_results",
                    return_value=(synthetic_results, synthetic_artifacts),
                ),
                patch.object(
                    evaluator.frozen_evaluator,
                    "render_report",
                    return_value=terra_report,
                ),
                patch.object(evaluator, "OUTPUT_DIR", output_dir),
            ):
                evaluator.evaluate()

            results = json.loads(
                (output_dir / "evaluation_results.json").read_text(encoding="utf-8")
            )
            manifest = json.loads(
                (output_dir / "evaluation_hash_manifest.json").read_text(
                    encoding="utf-8"
                )
            )
            report = (output_dir / "EVALUATION_REPORT.md").read_text(
                encoding="utf-8"
            )

            for key, expected in provenance.items():
                with self.subTest(artifact="results", key=key):
                    self.assertEqual(results["reproducibility"][key], expected)
                with self.subTest(artifact="manifest", key=key):
                    self.assertEqual(manifest[key], expected)

            self.assertIn("EXP2 Qwen", report)
            self.assertIn(evaluator.QWEN_PREDICTIONS_FREEZE_TAG, report)
            self.assertIn(evaluator.QWEN_PREDICTIONS_FREEZE_COMMIT, report)
            self.assertNotIn(TERRA_FREEZE_TAG, report)
            self.assertNotIn(TERRA_FREEZE_COMMIT, report)


if __name__ == "__main__":
    unittest.main()
