from __future__ import annotations

from pathlib import Path
import unittest

from phase_b.exp2.qwen.common import CONFIG_PATH, LANE_DIR, load_json


class ProbeArtifactTests(unittest.TestCase):
    def test_probe_is_capability_only_and_matches_execution_contract(self):
        probe_path = LANE_DIR / "probe/capability_probe.json"
        self.assertTrue(probe_path.exists())
        probe = load_json(probe_path)
        config = load_json(CONFIG_PATH)
        self.assertIn(probe["status"], {"PASS", "FAIL"})
        self.assertFalse(probe["heldout_predictions_generated"])
        self.assertFalse(probe["ground_truth_accessed"])
        self.assertFalse(probe["performance_metrics_calculated"])
        self.assertEqual(probe["full_experiment_calls_made"], 0)
        self.assertEqual(probe["prompt_budget"]["unique_prompts"], 180)
        self.assertTrue(probe["prompt_budget"]["all_prompt_hashes_match_original"])
        self.assertEqual(probe["config"]["temperature"], 0.0)
        self.assertEqual(probe["config"]["seed"], 20260829)
        self.assertEqual(probe["config"]["max_tokens"], 512)
        self.assertEqual(probe["server"]["model_id"], config["requested_model"])
        self.assertEqual(probe["server"]["model_root"], config["expected_model_root"])

    def test_complete_experiment_outputs_do_not_exist(self):
        inference = LANE_DIR / "inference"
        self.assertFalse((inference / "repetition_records.jsonl").exists())
        self.assertFalse((inference / "aggregate_records.jsonl").exists())


if __name__ == "__main__":
    unittest.main()
