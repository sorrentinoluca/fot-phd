from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest

from phase_b.exp2.qwen.common import FrozenPromptInputs, SCHEDULE_PATH, load_json
from phase_b.exp2.qwen.sensitivity.capped_followup.run import (
    CONFIG_PATH,
    FOLLOWUP_DIR,
    assert_followup_output_path,
    load_existing_records,
    max_tokens,
    select_target_entries,
    validate_record_contract,
    verify_source_caps,
)
from phase_b.exp2.qwen.sensitivity.run import frozen_qwen_prompt_hashes, verify_prompt_hash


def valid_record(**updates):
    record = {
        "agent_id": "agent_2",
        "physical_case_id": "PBH-007",
        "condition": "B",
        "repetition": 1,
        "frozen_schedule_sequence_index": 1,
        "sensitivity_sequence_index": 0,
        "followup_sequence_index": 0,
        "requested_model": "fot-exp2-consumer",
        "model_root": "Qwen/Qwen3.8-27B-FP8",
        "model_revision": "017b9c7af6b5689d5dd426a76e0bc077eb5ca20a",
        "vllm_version": "0.28.0",
        "max_model_len": 7168,
        "temperature": 0.0,
        "seed": 20260829,
        "thinking_token_budget": 4096,
        "max_tokens": 4608,
        "prompt_hash": "p",
        "input_hash": "i",
        "prompt_tokens": 100,
        "completion_tokens": 4200,
        "reasoning_tokens": 4095,
        "final_non_reasoning_tokens": 105,
        "total_tokens": 4300,
        "latency_monotonic_ns": 1,
        "raw_output": "{}",
        "reasoning_content": "reasoning",
        "server_fingerprint_sha256": "fingerprint",
        "cap_reached": True,
        "stateless": True,
        "message_count": 1,
        "structured_outputs_strict": True,
        "previous_response_id_used": False,
    }
    record.update(updates)
    return record


class SelectionAndProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_json(CONFIG_PATH)
        cls.entries = select_target_entries(load_json(SCHEDULE_PATH), cls.config)

    def test_selects_exact_five_declared_pairs_in_order(self):
        self.assertEqual(
            [(row["agent_id"], row["physical_case_id"]) for row in self.entries],
            [tuple(value) for value in self.config["target_pairs"]],
        )

    def test_each_target_is_unique_condition_b_repetition_one(self):
        self.assertEqual(len(self.entries), 5)
        self.assertEqual({row["condition"] for row in self.entries}, {"B"})
        self.assertEqual({row["repetition"] for row in self.entries}, {1})

    def test_declared_targets_are_exactly_source_caps_at_3072(self):
        capped = verify_source_caps(self.config)
        self.assertEqual(set(capped), {tuple(value) for value in self.config["target_pairs"]})

    def test_prompt_hashes_match_frozen_qwen(self):
        frozen = FrozenPromptInputs()
        reference = frozen_qwen_prompt_hashes()
        for entry in self.entries:
            verify_prompt_hash(entry, frozen.render(entry), reference)

    def test_budget_and_allowance_map_to_4608(self):
        self.assertEqual(max_tokens(self.config), 4608)
        self.assertEqual(self.config["thinking_token_budget"], 4096)


class ResumeAndWriteSafetyTests(unittest.TestCase):
    def setUp(self):
        self.config = load_json(CONFIG_PATH)

    def test_refuses_write_outside_followup(self):
        with self.assertRaises(RuntimeError):
            assert_followup_output_path(FOLLOWUP_DIR.parent / "records.jsonl")

    def test_resume_loads_one_record_without_duplication(self):
        with tempfile.TemporaryDirectory(dir=FOLLOWUP_DIR / "tests") as directory:
            path = Path(directory) / "records.jsonl"
            path.write_text(json.dumps(valid_record()) + "\n", encoding="utf-8")
            self.assertEqual(len(load_existing_records(path, self.config)), 1)

    def test_resume_rejects_duplicates(self):
        with tempfile.TemporaryDirectory(dir=FOLLOWUP_DIR / "tests") as directory:
            path = Path(directory) / "records.jsonl"
            line = json.dumps(valid_record()) + "\n"
            path.write_text(line + line, encoding="utf-8")
            with self.assertRaises(RuntimeError):
                load_existing_records(path, self.config)

    def test_rejects_wrong_budget_and_stateful_record(self):
        with self.assertRaisesRegex(RuntimeError, "thinking_token_budget"):
            validate_record_contract(valid_record(thinking_token_budget=3072), self.config)
        with self.assertRaisesRegex(RuntimeError, "stateless"):
            validate_record_contract(valid_record(stateless=False), self.config)


class CompletedArtifactTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_json(CONFIG_PATH)
        cls.records_path = FOLLOWUP_DIR / "records.jsonl"
        cls.results_path = FOLLOWUP_DIR / "results.json"
        if not cls.records_path.exists() or not cls.results_path.exists():
            raise unittest.SkipTest("completed inference artifacts are not present")
        cls.records = [
            json.loads(line)
            for line in cls.records_path.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        cls.results = load_json(cls.results_path)

    def test_records_are_exactly_five_target_budget_rows(self):
        self.assertEqual(len(self.records), 5)
        self.assertEqual(
            {(row["agent_id"], row["physical_case_id"]) for row in self.records},
            {tuple(value) for value in self.config["target_pairs"]},
        )
        self.assertEqual(
            {(row["condition"], row["repetition"], row["thinking_token_budget"]) for row in self.records},
            {("B", 1, 4096)},
        )

    def test_records_preserve_required_diagnostics(self):
        for row in self.records:
            self.assertIsInstance(row["raw_output"], str)
            self.assertIn("reasoning_content", row)
            self.assertIsInstance(row["reasoning_tokens"], int)
            self.assertIn("prediction", row)
            self.assertIsInstance(row["cap_reached"], bool)
            self.assertIsInstance(row["latency_seconds"], float)
            self.assertTrue(row["server_fingerprint_sha256"])

    def test_results_contain_complete_five_budget_trajectories(self):
        self.assertEqual(len(self.results["trajectories"]), 5)
        for item in self.results["trajectories"]:
            self.assertEqual(set(item["budgets"]), {"1024", "1536", "2048", "3072", "4096"})

    def test_results_do_not_claim_overall_accuracy(self):
        def keys(value):
            if isinstance(value, dict):
                for key, child in value.items():
                    yield key
                    yield from keys(child)
            elif isinstance(value, list):
                for child in value:
                    yield from keys(child)

        self.assertNotIn("accuracy", set(keys(self.results)))
        self.assertIn("not_global_accuracy_estimate", self.results["design"])


if __name__ == "__main__":
    unittest.main()
