from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from phase_b.final_evaluation import evaluate_frozen_predictions as evaluator


ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "phase_b/final_evaluation"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


class FinalOfflineEvaluationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.results = json.loads(
            (OUTPUT_DIR / "evaluation_results.json").read_text(encoding="utf-8")
        )
        cls.hash_manifest = json.loads(
            (OUTPUT_DIR / "evaluation_hash_manifest.json").read_text(encoding="utf-8")
        )

    def test_primary_uses_only_frozen_aggregate_predictions(self) -> None:
        self.assertEqual(
            self.results["primary_prediction_source"],
            "phase_b/final_evaluation/inference/aggregate_records.jsonl",
        )
        self.assertFalse(self.results["aggregation_recomputed"])
        self.assertEqual(
            self.hash_manifest["inference_freeze_commit"], evaluator.INFERENCE_COMMIT
        )
        self.assertEqual(
            self.hash_manifest["inference_freeze_tag"], evaluator.INFERENCE_TAG
        )
        inference_manifest = json.loads(
            evaluator.INFERENCE_HASH_MANIFEST_PATH.read_text(encoding="utf-8")
        )
        self.assertEqual(
            self.hash_manifest["input_aggregate_predictions_sha256"],
            inference_manifest["artifacts"][
                "phase_b/final_evaluation/inference/aggregate_records.jsonl"
            ],
        )

    def test_offline_evaluator_has_no_provider_dependency(self) -> None:
        source = Path(evaluator.__file__).read_text(encoding="utf-8")
        self.assertNotIn("OpenAIAdapter", source)
        self.assertNotIn("OPENAI_API_KEY", source)
        self.assertNotIn("create_response", source)

    def test_ground_truth_join_and_denominators(self) -> None:
        self.assertEqual(self.results["ground_truth_join"]["physical_cases_mapped"], 15)
        self.assertTrue(self.results["ground_truth_join"]["unique_mapping"])
        for condition in evaluator.CONDITIONS:
            condition_metrics = self.results["condition_metrics"][condition]
            self.assertEqual(condition_metrics["unseen"]["n"], 36)
            self.assertEqual(condition_metrics["local_fault_seen"]["n"], 12)
            self.assertEqual(condition_metrics["normal"]["n"], 12)
            self.assertEqual(condition_metrics["overall"]["n"], 60)
        for value in self.results["primary"]["per_agent"].values():
            self.assertEqual(value["n"], 9)
        transfer = self.results["primary"]["transfer_B_vs_A"]
        self.assertEqual(
            transfer["helped"] + transfer["harmed"] + transfer["unchanged"], 36
        )
        self.assertEqual(self.results["primary"]["physical_clusters"], 12)
        self.assertEqual(
            set(self.results["bootstrap"]["clusters_per_pseudolabel"].values()),
            {3},
        )
        self.assertEqual(self.results["integrity_checks"]["status"], "PASS")
        self.assertTrue(
            all(
                value
                for key, value in self.results["integrity_checks"].items()
                if key != "status"
            )
        )

    def test_confusion_and_abstention_accounting(self) -> None:
        confusion = self.results["secondary"]["confusion_matrices"]
        for condition in evaluator.CONDITIONS:
            self.assertEqual(
                sum(
                    sum(predictions.values())
                    for predictions in confusion[condition].values()
                ),
                60,
            )
            overall = self.results["condition_metrics"][condition]["overall"]
            abstentions = sum(
                predictions[evaluator.ABSTAIN_TOKEN]
                for predictions in confusion[condition].values()
            )
            self.assertEqual(overall["abstentions"], abstentions)

    def test_bootstrap_settings_are_frozen(self) -> None:
        bootstrap = self.results["bootstrap"]
        self.assertEqual(bootstrap["draws"], 10000)
        self.assertEqual(bootstrap["seed"], 20260829)
        self.assertEqual(bootstrap["n_physical_clusters"], 12)
        self.assertEqual(bootstrap["n_agent_case_rows"], 36)
        self.assertFalse(bootstrap["independence_claim"])

    def test_evaluation_hash_manifest_is_current(self) -> None:
        self.assertEqual(
            self.hash_manifest["status"],
            "OFFLINE_EVALUATION_COMPLETE_AWAITING_RESULTS_REVIEW",
        )
        self.assertEqual(
            self.hash_manifest["evaluator_code_sha256"],
            sha256_file(Path(evaluator.__file__)),
        )
        self.assertEqual(
            self.hash_manifest["metrics_code_sha256"],
            sha256_file(evaluator.METRICS_CODE_PATH),
        )
        self.assertEqual(
            self.hash_manifest["bootstrap_code_sha256"],
            sha256_file(evaluator.BOOTSTRAP_CODE_PATH),
        )
        self.assertEqual(
            self.hash_manifest["mapping_sha256"], sha256_file(evaluator.MAPPING_PATH)
        )
        for relative_path, expected_hash in self.hash_manifest[
            "evaluation_artifacts"
        ].items():
            self.assertEqual(sha256_file(ROOT / relative_path), expected_hash)

    def test_recomputation_is_byte_identical(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            evaluator.evaluate(Path(first))
            evaluator.evaluate(Path(second))
            first_files = {
                path.name: path.read_bytes()
                for path in Path(first).iterdir()
                if path.is_file()
            }
            second_files = {
                path.name: path.read_bytes()
                for path in Path(second).iterdir()
                if path.is_file()
            }
            self.assertEqual(first_files, second_files)
            self.assertEqual(
                set(first_files),
                {
                    "EVALUATION_REPORT.md",
                    "bootstrap_results.json",
                    "confusion_matrices.json",
                    "evaluation_hash_manifest.json",
                    "evaluation_results.json",
                    "per_agent_metrics.csv",
                    "primary_metrics.csv",
                    "secondary_metrics.csv",
                    "transfer_counts.csv",
                },
            )


if __name__ == "__main__":
    unittest.main()
