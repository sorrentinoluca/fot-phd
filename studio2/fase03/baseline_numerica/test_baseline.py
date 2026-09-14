from __future__ import annotations

import csv
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

from .baseline import DIMENSIONS, build_prototypes, classify, evaluate


LABELS = [
    "S2-CLS-3ZGWQ", "S2-CLS-4AMS4", "S2-CLS-FD3GZ", "S2-CLS-GSX3L",
    "S2-CLS-HEW25", "S2-CLS-MHMU4", "S2-CLS-QRCCB", "S2-CLS-TYFPG",
]
IDENTIFIERS = ["F15", "F14", "F13", "F2", "F8", "F10", "F3", "F1"]


def write_csv(path: Path, fields: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def make_evidence(root: Path, values: list[tuple[str, float]]) -> None:
    manifest = []
    for evidence_id, value in values:
        signature = root / "units" / f"{evidence_id}.signature.csv"
        write_csv(signature, ["component", "value"], [
            {"component": index, "value": format(value, ".17g")} for index in range(DIMENSIONS)
        ])
        manifest.append({
            "evidence_id": evidence_id,
            "signature_dimension": DIMENSIONS,
            "leakage_pass": "true",
            "baseline_sha256": "synthetic",
            "r2_guard_sha256": "synthetic",
            "signature_path": str(signature.relative_to(root)),
            "signature_sha256": hashlib.sha256(signature.read_bytes()).hexdigest(),
        })
    write_csv(root / "EVIDENCE_MANIFEST.csv", list(manifest[0]), manifest)


class BaselineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.fault_root = self.root / "fault"
        self.normal_root = self.root / "normal"
        fault_values = [(f"EVD-X-{index}", 0.12 + index * 0.09) for index in range(8)]
        normal_values = [(f"EVD-N-{index}", 0.02 + index * 0.001) for index in range(8)]
        make_evidence(self.fault_root, fault_values)
        make_evidence(self.normal_root, normal_values)
        write_csv(self.root / "fault_index.csv", ["evidence_id", "fault"], [
            {"evidence_id": f"EVD-X-{index}", "fault": identifier}
            for index, identifier in enumerate(IDENTIFIERS)
        ])
        write_csv(
            self.root / "normal_index.csv",
            ["evidence_id", "agent_id", "class_identifier"],
            [
                {"evidence_id": f"EVD-N-{index}", "agent_id": f"agent_{index + 1}", "class_identifier": "Normal"}
                for index in range(8)
            ],
        )
        mapping = {
            "label_by_identifier": {**dict(zip(IDENTIFIERS, LABELS)), "Normal": "Normal"},
            "label_space": LABELS + ["Normal"],
        }
        assignment = {
            "assignment": {
                f"agent_{index + 1}": {"local_fault_label": LABELS[index]}
                for index in range(8)
            }
        }
        (self.root / "mapping.json").write_text(json.dumps(mapping), encoding="utf-8")
        (self.root / "assignment.json").write_text(json.dumps(assignment), encoding="utf-8")

    def tearDown(self) -> None:
        self.temp.cleanup()

    def build(self, destination: Path) -> dict[str, object]:
        return build_prototypes(
            fault_root=self.fault_root,
            fault_index_path=self.root / "fault_index.csv",
            normal_root=self.normal_root,
            normal_index_path=self.root / "normal_index.csv",
            mapping_path=self.root / "mapping.json",
            assignment_path=self.root / "assignment.json",
            output_dir=destination,
            strict_campaign=False,
        )

    def test_tie_abstains(self) -> None:
        predicted, abstain, _ = classify(
            [0.5] * DIMENSIONS,
            {"S2-CLS-AAAAA": [0.0] * DIMENSIONS, "S2-CLS-BBBBB": [1.0] * DIMENSIONS},
        )
        self.assertIsNone(predicted)
        self.assertTrue(abstain)

    def test_deterministic_build_and_no_f_numbers(self) -> None:
        first = self.root / "build_a"
        second = self.root / "build_b"
        self.build(first)
        self.build(second)
        for name in ("PROTOTYPES.json", "PROTOTYPES_MANIFEST.json"):
            self.assertEqual((first / name).read_bytes(), (second / name).read_bytes())
            self.assertNotRegex((first / name).read_text(), r"(?<![A-Za-z0-9_])F\d+")

    def test_end_to_end_three_numbers_and_local_absent_classes(self) -> None:
        built = self.root / "built"
        prototypes = self.build(built)
        local = prototypes["local"]["agent_1"]["prototypes"]
        self.assertEqual(set(local), {"Normal", LABELS[0]})
        test_root = self.root / "test_evidence"
        make_evidence(test_root, [("TST-001", 0.12), ("TST-002", 0.39)])
        write_csv(
            self.root / "test_index.csv",
            ["physical_case_id", "evidence_id", "agent_id", "true_pseudolabel"],
            [
                {"physical_case_id": "CASE-001", "evidence_id": "TST-001", "agent_id": "agent_1", "true_pseudolabel": LABELS[0]},
                {"physical_case_id": "CASE-002", "evidence_id": "TST-002", "agent_id": "agent_1", "true_pseudolabel": LABELS[3]},
            ],
        )
        output = self.root / "evaluation"
        metrics = evaluate(
            prototypes_path=built / "PROTOTYPES.json",
            test_evidence_root=test_root,
            test_index_path=self.root / "test_index.csv",
            output_dir=output,
        )
        repeated = self.root / "evaluation_repeated"
        evaluate(
            prototypes_path=built / "PROTOTYPES.json",
            test_evidence_root=test_root,
            test_index_path=self.root / "test_index.csv",
            output_dir=repeated,
        )
        self.assertEqual(
            metrics["three_numbers"],
            ["accuracy", "abstention_rate", "accuracy_non_abstained"],
        )
        self.assertEqual(len(metrics["clusters"]), 4)
        predictions = read_rows(output / "predictions.csv")
        local_unseen = [
            row for row in predictions
            if row["condition"] == "numeric_local" and row["physical_case_id"] == "CASE-002"
        ][0]
        self.assertNotEqual(local_unseen["predicted_label"], LABELS[3])
        for path in output.iterdir():
            self.assertNotRegex(path.read_text(), r"(?<![A-Za-z0-9_])F\d+")
            self.assertEqual(path.read_bytes(), (repeated / path.name).read_bytes())

    def test_manifest_tampering_fails_closed(self) -> None:
        signature = next((self.fault_root / "units").glob("*.csv"))
        signature.write_text(signature.read_text() + "\n", encoding="utf-8")
        with self.assertRaises(RuntimeError):
            self.build(self.root / "tampered")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    unittest.main()
