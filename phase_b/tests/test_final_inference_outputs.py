from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import unittest

from phase_b.evaluation.aggregation import aggregate_run_records
from phase_b.final_evaluation import run_frozen_inference as runner


ROOT = Path(__file__).resolve().parents[2]
INFERENCE_DIR = ROOT / "phase_b/final_evaluation/inference"


def load_jsonl(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if any(not line.strip() for line in lines):
        raise AssertionError(f"blank JSONL line in {path}")
    return [json.loads(line) for line in lines]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def nested_keys(value):
    if isinstance(value, dict):
        for key, child in value.items():
            yield key
            yield from nested_keys(child)
    elif isinstance(value, list):
        for child in value:
            yield from nested_keys(child)


class FinalInferenceOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.schedule = json.loads(runner.SCHEDULE_PATH.read_text(encoding="utf-8"))
        cls.records = load_jsonl(INFERENCE_DIR / "repetition_records.jsonl")
        cls.aggregates = load_jsonl(INFERENCE_DIR / "aggregate_records.jsonl")
        cls.metadata = json.loads(
            (INFERENCE_DIR / "execution_metadata.json").read_text(encoding="utf-8")
        )
        cls.manifest = json.loads(
            (INFERENCE_DIR / "inference_output_hash_manifest.json").read_text(
                encoding="utf-8"
            )
        )
        cls.frozen = runner.FrozenInputs()

    def test_frozen_inputs_and_schedule_are_unchanged(self) -> None:
        head = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True
        ).strip()
        tag_target = subprocess.check_output(
            ["git", "rev-parse", "phase-b-execution-schedule-frozen^{}"],
            cwd=ROOT,
            text=True,
        ).strip()
        ancestry = subprocess.run(
            ["git", "merge-base", "--is-ancestor", runner.EXPECTED_HEAD, head],
            cwd=ROOT,
            check=False,
        )
        self.assertEqual(ancestry.returncode, 0)
        self.assertEqual(tag_target, runner.EXPECTED_HEAD)
        runner.validate_schedule(self.schedule)
        self.assertEqual(
            sha256_file(runner.SCHEDULE_PATH), runner.EXPECTED_SCHEDULE_SHA
        )
        protocol_manifest = json.loads(
            runner.PROTOCOL_HASH_MANIFEST_PATH.read_text(encoding="utf-8")
        )["artifacts"]
        for relative_path, expected_hash in protocol_manifest.items():
            self.assertEqual(sha256_file(ROOT / relative_path), expected_hash)
        insight_hashes = json.loads(
            runner.FINAL_INSIGHT_HASHES_PATH.read_text(encoding="utf-8")
        )["sha256"]
        self.assertEqual(
            sha256_file(runner.GLOBAL_INSIGHTS_PATH),
            insight_hashes["final_local_insights"],
        )
        for name, expected_hash in insight_hashes["peer_libraries"].items():
            self.assertEqual(
                sha256_file(ROOT / f"phase_b/insights/peer_libraries/{name}.json"),
                expected_hash,
            )

    def test_repetition_completeness_and_schedule_adherence(self) -> None:
        self.assertEqual(len(self.records), 540)
        self.assertEqual(
            Counter(record["condition"] for record in self.records),
            Counter({"A": 180, "B": 180, "E": 180}),
        )
        self.assertEqual(
            [record["sequence_index"] for record in self.records], list(range(540))
        )
        keys = [
            (
                record["physical_case_id"],
                record["agent_id"],
                record["condition"],
                record["repetition"],
            )
            for record in self.records
        ]
        self.assertEqual(len(set(keys)), 540)
        combinations = Counter(
            (
                record["physical_case_id"],
                record["agent_id"],
                record["condition"],
            )
            for record in self.records
        )
        self.assertEqual(len(combinations), 180)
        self.assertEqual(set(combinations.values()), {3})
        runner.validate_complete(self.records, self.schedule, self.frozen)

    def test_each_record_has_valid_schema_provenance_tokens_and_statelessness(self) -> None:
        forbidden_ground_truth_keys = {
            "class_offline",
            "fault_id",
            "ground_truth",
            "true_class",
            "true_label",
            "correct",
            "correctness",
        }
        for record, entry in zip(self.records, self.schedule):
            rendered = self.frozen.render(entry)
            runner.validate_record(record, entry, rendered, self.frozen)
            self.assertTrue(record["structured_outputs_strict"])
            self.assertTrue(record["stateless"])
            self.assertFalse(record["store"])
            self.assertFalse(record["previous_response_id_used"])
            self.assertFalse(record["parse_failure"])
            self.assertEqual(
                record["total_tokens"],
                record["input_tokens"] + record["output_tokens"],
            )
            self.assertEqual(
                record["cumulative_total_tokens"],
                record["cumulative_input_tokens"]
                + record["cumulative_output_tokens"],
            )
            self.assertEqual(
                record["retry_count"], len(record["provider_attempts"]) - 1
            )
            used_ids = set(record["parsed_final_output"]["used_insight_ids"])
            self.assertTrue(used_ids.issubset(set(record["available_insight_ids"])))
            if record["condition"] == "A":
                self.assertEqual(used_ids, set())
            self.assertTrue(
                forbidden_ground_truth_keys.isdisjoint(set(nested_keys(record)))
            )

    def test_retry_and_execution_metadata_accounting(self) -> None:
        retry_by_condition = Counter()
        for record in self.records:
            retry_by_condition[record["condition"]] += record["retry_count"]
        self.assertEqual(sum(retry_by_condition.values()), 1)
        self.assertEqual(
            {condition: retry_by_condition[condition] for condition in ("A", "B", "E")},
            self.metadata["structural_retries_by_condition"],
        )
        self.assertEqual(self.metadata["structural_retries_total"], 1)
        self.assertEqual(self.metadata["provider_network_failures"], 0)
        self.assertEqual(self.metadata["final_parse_failures"], 0)
        self.assertTrue(self.metadata["schedule_adherence"])
        self.assertTrue(self.metadata["stateless_calls"])
        self.assertTrue(self.metadata["token_accounting_complete"])
        self.assertTrue(self.metadata["provenance_complete"])
        self.assertFalse(self.metadata["ground_truth_joined"])
        self.assertFalse(self.metadata["metrics_calculated"])
        self.assertEqual(
            self.metadata["cumulative_total_tokens"],
            sum(record["cumulative_total_tokens"] for record in self.records),
        )

    def test_frozen_r3_aggregation_matches_saved_artifact(self) -> None:
        frozen_records = [runner.record_to_frozen_run_record(item) for item in self.records]
        recomputed = aggregate_run_records(
            frozen_records, label_space=self.frozen.protocol["label_space"]
        )
        recomputed_values = [
            {
                "physical_case_id": item.physical_case_id,
                "agent_id": item.agent_id,
                "condition": item.condition,
                "parsed_output": item.parsed_output,
                "repetition_outcomes": list(item.repetition_outcomes),
                "aggregation_rule": "frozen_valid_label_majority_2_of_3_else_abstain",
            }
            for item in recomputed
        ]
        self.assertEqual(len(self.aggregates), 180)
        self.assertEqual(self.aggregates, recomputed_values)
        aggregate_keys = {
            (
                item["physical_case_id"],
                item["agent_id"],
                item["condition"],
            )
            for item in self.aggregates
        }
        self.assertEqual(len(aggregate_keys), 180)

    def test_output_hash_manifest_is_complete_and_current(self) -> None:
        self.assertEqual(self.manifest["status"], "IMMUTABLE_BEFORE_OFFLINE_EVALUATION")
        self.assertFalse(self.manifest["ground_truth_included"])
        self.assertEqual(self.manifest["repetition_record_count"], 540)
        self.assertEqual(self.manifest["aggregate_record_count"], 180)
        self.assertEqual(
            self.manifest["schedule_reference"],
            {
                "path": "phase_b/final_evaluation/inference_schedule.json",
                "sha256": runner.EXPECTED_SCHEDULE_SHA,
            },
        )
        expected_paths = {
            "phase_b/final_evaluation/inference/repetition_records.jsonl",
            "phase_b/final_evaluation/inference/aggregate_records.jsonl",
            "phase_b/final_evaluation/inference/execution_metadata.json",
        }
        self.assertEqual(set(self.manifest["artifacts"]), expected_paths)
        for relative_path, expected_hash in self.manifest["artifacts"].items():
            self.assertEqual(sha256_file(ROOT / relative_path), expected_hash)


if __name__ == "__main__":
    unittest.main()
