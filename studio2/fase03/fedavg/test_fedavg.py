from __future__ import annotations

import csv
import hashlib
import tempfile
import unittest
from pathlib import Path

import numpy as np

try:
    from .fedavg import (
        CLIENTS, DIMENSION, LABELS, Config, aggregate_parameter_sets, evaluate_all_modes,
        initialize, load_evidence_bundle, predict, split_leave_one_batch_out, train_all_modes,
        weights_sha256,
    )
    from .smoke_fedavg import synthetic_development_fixture
except ImportError:  # esecuzione diretta dalla cartella fedavg/
    from fedavg import (
        CLIENTS, DIMENSION, LABELS, Config, aggregate_parameter_sets, evaluate_all_modes,
        initialize, load_evidence_bundle, predict, split_leave_one_batch_out, train_all_modes,
        weights_sha256,
    )
    from smoke_fedavg import synthetic_development_fixture


FAST = Config(hidden_dim=32, learning_rate=0.08, batch_size=16, local_epochs=2, rounds=40)


class FedAvgTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.separable = synthetic_development_fixture()
        cls.train, cls.validation = split_leave_one_batch_out(cls.separable, "5")
        cls.models = train_all_modes(cls.train, FAST)

    def test_separable_fixture_is_learned(self) -> None:
        for mode in ("fedavg", "centralized"):
            predictions = predict(self.models[mode], self.validation.x)
            self.assertGreaterEqual(float(np.mean(predictions == self.validation.y)), 0.95)

    def test_null_fixture_does_not_match_separable_case(self) -> None:
        null_train, null_validation = split_leave_one_batch_out(
            synthetic_development_fixture(null=True), "5"
        )
        null_model = train_all_modes(null_train, FAST)["centralized"]
        null_accuracy = float(np.mean(predict(null_model, null_validation.x) == null_validation.y))
        separable_accuracy = float(np.mean(
            predict(self.models["centralized"], self.validation.x) == self.validation.y
        ))
        self.assertLess(null_accuracy, separable_accuracy)
        self.assertLessEqual(null_accuracy, 0.5)

    def test_deterministic_weight_hashes(self) -> None:
        repeated = train_all_modes(self.train, FAST)
        self.assertEqual(weights_sha256(self.models["fedavg"]), weights_sha256(repeated["fedavg"]))
        self.assertEqual(
            {client: weights_sha256(self.models["local"][client]) for client in CLIENTS},
            {client: weights_sha256(repeated["local"][client]) for client in CLIENTS},
        )

    def test_weighted_parameter_aggregation(self) -> None:
        first = {name: np.full_like(value, 1.0) for name, value in initialize(FAST).items()}
        second = {name: np.full_like(value, 5.0) for name, value in initialize(FAST).items()}
        aggregated = aggregate_parameter_sets((first, second), (1, 3))
        for value in aggregated.values():
            np.testing.assert_array_equal(value, np.full_like(value, 4.0))

    def test_local_floor_masks_seven_absent_faults(self) -> None:
        model = self.models["local"]["F1"]
        predictions = predict(model, self.validation.x)
        self.assertTrue(set(predictions.tolist()).issubset({0, LABELS.index("F1")}))
        self.assertEqual(len(model.visible_labels), 2)

    def test_metrics_have_three_numbers_and_no_abstention(self) -> None:
        rows = evaluate_all_modes(self.models, self.validation)
        self.assertTrue(rows)
        for row in rows:
            self.assertEqual(row["abstention_rate"], 0.0)
            self.assertEqual(row["accuracy"], row["accuracy_non_abstained"])
            self.assertEqual(row["n_attempts"], row["non_abstained"])

    def test_loader_verifies_hashes_and_one_to_one_join(self) -> None:
        with tempfile.TemporaryDirectory(prefix="fedavg_fixture_dev_") as temp:
            root = Path(temp) / "development_bundle"
            units = root / "units"
            units.mkdir(parents=True)
            signature = units / "EVD-0001.signature.csv"
            with signature.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.writer(handle, lineterminator="\n")
                writer.writerow(("component", "value"))
                writer.writerows((index, float(index == 0)) for index in range(DIMENSION))
            signature_hash = _sha(signature)
            manifest = root / "EVIDENCE_MANIFEST.csv"
            with manifest.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=(
                    "evidence_id", "signature_dimension", "leakage_pass", "signature_path",
                    "signature_sha256",
                ), lineterminator="\n")
                writer.writeheader()
                writer.writerow({
                    "evidence_id": "EVD-0001", "signature_dimension": DIMENSION,
                    "leakage_pass": "true", "signature_path": "units/EVD-0001.signature.csv",
                    "signature_sha256": signature_hash,
                })
            index = root / "EVALUATOR_INDEX.csv"
            with index.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(
                    handle, fieldnames=("evidence_id", "run_id", "fault", "batch"),
                    lineterminator="\n",
                )
                writer.writeheader()
                writer.writerow({
                    "evidence_id": "EVD-0001", "run_id": "fault-dev-F1-b01",
                    "fault": "F1", "batch": 1,
                })
            loaded = load_evidence_bundle(
                root, expected_manifest_sha256=_sha(manifest), expected_index_sha256=_sha(index)
            )
            self.assertEqual(loaded.x.shape, (1, DIMENSION))
            with self.assertRaises(RuntimeError):
                load_evidence_bundle(
                    root, expected_manifest_sha256="0" * 64, expected_index_sha256=_sha(index)
                )

    def test_test_directory_guard_is_fail_closed(self) -> None:
        with self.assertRaises(ValueError):
            load_evidence_bundle(
                Path("campaign/test/output"),
                expected_manifest_sha256="0" * 64,
                expected_index_sha256="0" * 64,
            )


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    unittest.main()
