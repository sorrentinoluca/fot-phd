from __future__ import annotations

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
        validate_no_collisions(rows, repo_root)

    def test_changed_plan_is_rejected(self) -> None:
        source = Path(__file__).with_name("plans") / "normal_dev.csv"
        with tempfile.TemporaryDirectory() as directory:
            changed = Path(directory) / "normal_dev.csv"
            changed.write_bytes(source.read_bytes().replace(b"60000", b"30000", 1))
            with self.assertRaises(ValueError):
                validate_plan(changed)


if __name__ == "__main__":
    unittest.main()
