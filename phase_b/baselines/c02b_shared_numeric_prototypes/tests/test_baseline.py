from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
import csv

import numpy as np

from phase_b.baselines.c02b_shared_numeric_prototypes.run_baseline import (
    CONFIG_PATH,
    classify,
    emit_payloads,
    scope,
    sha256_file,
    validate_vector,
    verify_protocol,
)


class C02bBaselineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    def test_protocol_freeze_and_input_hashes(self) -> None:
        verified = verify_protocol()
        self.assertEqual(verified["protocol_id"], "c02b-shared-numeric-prototypes-1.0.0")
        self.assertFalse(verified["results_accessed_before_freeze"])

    def test_vector_validation(self) -> None:
        vector = validate_vector(np.zeros(697), 697)
        self.assertEqual(vector.shape, (697,))
        with self.assertRaises(RuntimeError):
            validate_vector(np.zeros(696), 697)
        invalid = np.zeros(697)
        invalid[0] = np.nan
        with self.assertRaises(RuntimeError):
            validate_vector(invalid, 697)

    def test_nearest_prototype_and_tie_abstention(self) -> None:
        prototypes = {"A": np.zeros(3), "B": np.ones(3)}
        predicted, abstain, _ = classify(
            np.array([0.0, 0.0, 0.2]), prototypes, ["A", "B"], 1e-12
        )
        self.assertEqual(predicted, "A")
        self.assertFalse(abstain)
        predicted, abstain, _ = classify(
            np.full(3, 0.5), prototypes, ["A", "B"], 1e-12
        )
        self.assertIsNone(predicted)
        self.assertTrue(abstain)

    def test_scope_contract(self) -> None:
        self.assertEqual(scope("agent_1", "Normal", self.config), "normal")
        self.assertEqual(scope("agent_1", "CLS-ZOGAA", self.config), "local_seen")
        self.assertEqual(scope("agent_1", "CLS-OJNSG", self.config), "local_unseen")

    def test_payload_exact_bytes(self) -> None:
        prototypes = {
            label: np.full(697, index / 10.0)
            for index, label in enumerate(self.config["task"]["labels"])
        }
        with tempfile.TemporaryDirectory() as directory:
            manifest = emit_payloads(Path(directory), prototypes, self.config)
            self.assertEqual(manifest["total_peer_fault_prototype_transmissions"], 12)
            self.assertEqual(manifest["total_transmitted_scalar_values"], 8364)
            self.assertEqual(manifest["total_payload_bytes"], 67020)
            for item in manifest["delivery"].values():
                path = Path(item["payload_path"])
                if not path.is_absolute():
                    # emit_payloads reports repo-relative paths only for repository outputs.
                    path = Path(directory) / "payloads" / (path.stem + ".bin")
                self.assertEqual(item["payload_bytes"], 16755)
                self.assertEqual(len(item["payload_sha256"]), 64)

    def test_completed_results_contract(self) -> None:
        results = CONFIG_PATH.parent / "results"
        metrics = json.loads((results / "metrics.json").read_text(encoding="utf-8"))
        primary = metrics["metrics"]["shared_prototypes"]["local_unseen"]
        self.assertEqual((primary["correct"], primary["n"], primary["accuracy"]), (36, 36, 1.0))
        self.assertEqual(metrics["metrics"]["local_only"]["local_unseen"]["correct"], 0)
        self.assertEqual(metrics["communication"]["total_payload_bytes"], 67020)

        with (results / "predictions_unscored.csv").open(encoding="utf-8", newline="") as stream:
            unscored = list(csv.DictReader(stream))
        self.assertEqual(len(unscored), 180)
        self.assertNotIn("true_pseudolabel", unscored[0])
        self.assertNotIn("correct", unscored[0])

        with (results / "predictions.csv").open(encoding="utf-8", newline="") as stream:
            scored = list(csv.DictReader(stream))
        shared = {
            (row["agent_id"], row["physical_case_id"]): row["predicted_pseudolabel"]
            for row in scored if row["arm"] == "shared_prototypes"
        }
        centralized = {
            (row["agent_id"], row["physical_case_id"]): row["predicted_pseudolabel"]
            for row in scored if row["arm"] == "centralized_reference"
        }
        self.assertEqual(shared, centralized)

    def test_output_hash_manifest(self) -> None:
        manifest_path = CONFIG_PATH.parent / "results/output_hash_manifest.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for relative, expected in manifest["artifacts"].items():
            self.assertEqual(sha256_file(CONFIG_PATH.parents[3] / relative), expected)


if __name__ == "__main__":
    unittest.main()
