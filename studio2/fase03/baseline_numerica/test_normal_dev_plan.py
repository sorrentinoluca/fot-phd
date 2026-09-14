from __future__ import annotations

import csv
import tempfile
import unittest
from pathlib import Path

from .build_normal_dev_plan import build_rows, validate_plan
from .preflight_normal_dev import validate_no_collisions


class NormalDevPlanTests(unittest.TestCase):
    def test_assignment_streams_and_windows(self) -> None:
        rows = build_rows()
        self.assertEqual(len(rows), 40)
        self.assertEqual({int(row["stream_id"]) for row in rows}, set(range(60000, 60040)))
        for agent_index in range(1, 9):
            selected = [row for row in rows if row["agent_id"] == f"agent_{agent_index}"]
            self.assertEqual(len(selected), 5)
            self.assertEqual({int(row["agent_run_index"]) for row in selected}, set(range(1, 6)))
        self.assertEqual({row["useful_windows_expected"] for row in rows}, {8})

    def test_frozen_csv_and_collision_check(self) -> None:
        source = Path(__file__).with_name("plans") / "normal_dev.csv"
        rows = validate_plan(source)
        repo_root = Path(__file__).resolve().parents[3]
        own_manifest = (
            Path(__file__).with_name("runs")
            / "normal_dev_001"
            / "generation_manifest.csv"
        )
        validate_no_collisions(
            rows,
            repo_root,
            excluded_manifests={own_manifest},
        )

    def test_changed_plan_is_rejected(self) -> None:
        source = Path(__file__).with_name("plans") / "normal_dev.csv"
        with tempfile.TemporaryDirectory() as directory:
            changed = Path(directory) / "normal_dev.csv"
            changed.write_bytes(source.read_bytes().replace(b"60000", b"30000", 1))
            with self.assertRaises(ValueError):
                validate_plan(changed)

    def test_derived_index_is_not_a_stream_allocation(self) -> None:
        rows = build_rows()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            derived = root / "studio2" / "fase03" / "evidence" / "EVALUATOR_INDEX.csv"
            derived.parent.mkdir(parents=True)
            with derived.open("w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=("evidence_id", "stream_id"))
                writer.writeheader()
                writer.writerow({"evidence_id": "NDEV-EVD-0001", "stream_id": "60000"})
            validate_no_collisions(rows, root)

            manifest = root / "studio2" / "fase03" / "other" / "generation_manifest.csv"
            manifest.parent.mkdir(parents=True)
            manifest.write_text("run_id,stream_id\nother,60000\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "stream collision"):
                validate_no_collisions(rows, root)


if __name__ == "__main__":
    unittest.main()
