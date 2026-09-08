from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import unittest

from phase_b.exp2.qwen.common import (
    CONFIG_PATH,
    ROOT,
    SCHEDULE_PATH,
    FrozenPromptInputs,
    load_json,
    original_prompt_hashes,
    sha256_file,
    verify_frozen_hashes,
)


class FrozenContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config = load_json(CONFIG_PATH)

    def test_qwen_execution_contract(self):
        self.assertEqual(self.config["base_url"], "http://127.0.0.1:8000/v1")
        self.assertEqual(self.config["requested_model"], "fot-exp2-consumer")
        self.assertEqual(self.config["temperature"], 0.0)
        self.assertEqual(self.config["seed"], 20260829)
        self.assertEqual(self.config["max_tokens"], 512)
        self.assertEqual(self.config["repetitions"], 3)
        self.assertIsNone(self.config["reasoning_effort"])

    def test_frozen_hashes_are_unchanged(self):
        verify_frozen_hashes(self.config)

    def test_entire_original_protocol_hash_manifest_is_unchanged(self):
        manifest = load_json(ROOT / "phase_b/PHASE_B_PROTOCOL_HASHES.json")
        for relative, expected in manifest["artifacts"].items():
            with self.subTest(relative=relative):
                self.assertEqual(sha256_file(ROOT / relative), expected)

    def test_schedule_cardinality_and_r3(self):
        schedule = load_json(SCHEDULE_PATH)
        self.assertEqual(len(schedule), 540)
        self.assertEqual(
            Counter(item["condition"] for item in schedule),
            Counter({"A": 180, "B": 180, "E": 180}),
        )
        groups = Counter(
            (item["physical_case_id"], item["agent_id"], item["condition"])
            for item in schedule
        )
        self.assertEqual(len(groups), 180)
        self.assertEqual(set(groups.values()), {3})

    def test_all_rendered_prompts_match_original_frozen_hashes(self):
        schedule = load_json(SCHEDULE_PATH)
        originals = original_prompt_hashes()
        frozen = FrozenPromptInputs()
        checked = set()
        for entry in schedule:
            key = (entry["physical_case_id"], entry["agent_id"], entry["condition"])
            if key in checked:
                continue
            checked.add(key)
            self.assertEqual(frozen.render(entry).prompt_hash, originals[key])
        self.assertEqual(len(checked), 180)

    def test_lane_does_not_shadow_frozen_artifacts(self):
        lane = CONFIG_PATH.parent
        forbidden_names = {
            "isolated_A.txt",
            "fot_B.txt",
            "corrupted_E.txt",
            "final_local_insights.json",
            "inference_schedule.json",
            "protocol_config.json",
        }
        self.assertFalse(
            forbidden_names.intersection(path.name for path in lane.rglob("*"))
        )

    def test_runner_requires_explicit_full_run_acknowledgement(self):
        runner = (CONFIG_PATH.parent / "run_frozen_inference.py").read_text(encoding="utf-8")
        self.assertIn("--execute-full-run", runner)
        self.assertIn("Refusing to run", runner)

    def test_qwen_evaluator_binds_existing_evaluator(self):
        binding = (CONFIG_PATH.parent / "evaluate_qwen.py").read_text(encoding="utf-8")
        self.assertIn("phase_b.final_evaluation.evaluate_frozen_predictions", binding)
        self.assertNotIn("def bootstrap_primary", binding)
        self.assertNotIn("def aggregate_run_records", binding)


if __name__ == "__main__":
    unittest.main()
