from __future__ import annotations

import csv
import json
import unittest

from phase_b.baselines.c02b_supervisor_model_suite.run_suite import (
    CONFIG_PATH,
    MODEL_ORDER,
    LSTMAttentionClassifier,
    sequence_rows,
    sha256_file,
    verify_protocol,
)
from phase_b.baselines.c02b_shared_numeric_prototypes.run_baseline import normal_blocks


ROOT = CONFIG_PATH.parents[3]
RESULTS = CONFIG_PATH.parent / "results"


class SupervisorModelSuiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    def test_protocol_and_parent_hashes(self) -> None:
        verified = verify_protocol()
        self.assertEqual(verified["protocol_id"], "c02b-supervisor-model-suite-1.0.0")
        self.assertFalse(verified["results_accessed_before_freeze"])

    def test_requested_model_coverage(self) -> None:
        self.assertEqual(set(self.config["models"]), set(MODEL_ORDER))
        self.assertIn("elasticnet", self.config["models"]["linear_elastic_net"]["penalty"])
        self.assertFalse(self.config["models"]["lstm_causal_attention"]["bidirectional"])
        self.assertTrue(self.config["models"]["bilstm_attention"]["bidirectional"])
        self.assertEqual(
            len(self.config["models"]["multimodal_bilstm_attention_tfidf"]["modalities"]),
            2,
        )

    def test_causal_and_bidirectional_architectures_are_distinct(self) -> None:
        causal = LSTMAttentionClassifier(41, 32, 5, bidirectional=False)
        bidirectional = LSTMAttentionClassifier(41, 24, 5, bidirectional=True)
        self.assertFalse(causal.lstm.bidirectional)
        self.assertTrue(bidirectional.lstm.bidirectional)

    def test_sequence_contract(self) -> None:
        path = ROOT / "code/tep_cache/mode1_normal_500.xlsx"
        blocks = normal_blocks(path)
        sequence = sequence_rows(blocks["N1"], self.config)
        self.assertEqual(sequence.shape, (120, 41))

    def test_completed_outputs(self) -> None:
        metrics = json.loads((RESULTS / "metrics.json").read_text(encoding="utf-8"))
        self.assertEqual(metrics["status"], "COMPLETE")
        self.assertEqual(set(metrics["metrics"]), set(MODEL_ORDER))
        for model in MODEL_ORDER:
            item = metrics["metrics"][model]
            self.assertEqual(item["physical_cases"]["n"], 15)
            self.assertEqual(item["projected_local_unseen"]["n"], 36)
            self.assertEqual(item["projected_local_seen"]["n"], 12)

    def test_predictions_are_written_unscored(self) -> None:
        with (RESULTS / "predictions_unscored.csv").open(newline="", encoding="utf-8") as stream:
            unscored = list(csv.DictReader(stream))
        self.assertEqual(len(unscored), 8 * 15)
        self.assertNotIn("true_pseudolabel", unscored[0])
        self.assertNotIn("correct", unscored[0])
        with (RESULTS / "predictions.csv").open(newline="", encoding="utf-8") as stream:
            scored = list(csv.DictReader(stream))
        self.assertEqual(len(scored), len(unscored))
        self.assertIn("true_pseudolabel", scored[0])

    def test_output_hash_manifest(self) -> None:
        manifest = json.loads(
            (RESULTS / "output_hash_manifest.json").read_text(encoding="utf-8")
        )
        for relative, expected in manifest["artifacts"].items():
            self.assertEqual(sha256_file(ROOT / relative), expected)


if __name__ == "__main__":
    unittest.main()
