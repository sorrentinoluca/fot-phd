"""Offline tests for the D1 run->window assignment. No model call, no test data."""

from __future__ import annotations

import json
import unittest

from . import window_assignment as module
from .common import HarnessError


def _plan_rows(groups):
    rows = []
    for key, count in groups:
        for index in range(1, count + 1):
            rows.append({"run_id": f"{key}-r{index:02d}", "useful_windows_expected": "8"})
    return rows


REAL_GROUPS = [(f"test-primary-{fault}", 8) for fault in
               ("F1", "F2", "F3", "F8", "F10", "F13", "F14", "F15", "Normal")]
REAL_GROUPS += [("test-ood-F4", 3), ("test-ood-F5", 3)]


class WindowAssignmentTest(unittest.TestCase):
    def setUp(self):
        self.artifact = module.assignment_artifact()

    def test_assignment_is_reproducible_byte_for_byte(self):
        again = module.assignment_artifact()
        self.assertEqual(module.artifact_sha256(self.artifact), module.artifact_sha256(again))
        self.assertEqual(self.artifact["assignment_sha256"], again["assignment_sha256"])

    def test_one_window_per_run_and_every_position_once_per_fault(self):
        assignment = self.artifact["assignment"]
        self.assertEqual(len(assignment), 78)
        self.assertEqual(len({row["case_id"] for row in assignment}), 78)
        for group, table in self.artifact["position_table"].items():
            positions = sorted(int(value) for value in table)
            if len(positions) == module.POSITIONS:
                self.assertEqual(positions, list(range(1, 9)), group)
            else:
                self.assertEqual(len(positions), 3, group)
                self.assertEqual(len(set(positions)), 3, group)
                self.assertTrue(all(1 <= value <= 8 for value in positions), group)

    def test_spares_are_never_assigned(self):
        self.assertEqual(self.artifact["counts"]["excluded_spares"], 11)
        self.assertFalse([row for row in self.artifact["assignment"]
                          if row["case_id"].startswith(module.SPARE_PREFIX)])

    def test_window_bounds_follow_the_frozen_geometry(self):
        for row in self.artifact["assignment"]:
            start, end = module.window_bounds(row["window_ordinal"])
            self.assertEqual((row["window_start_h"], row["window_end_h"]), (start, end))
            self.assertGreaterEqual(start, module.ONSET_H)
            self.assertLessEqual(end, module.END_H)

    def test_sealed_sources_are_authenticated_and_chained(self):
        seal, audit, rows, sources = module.sealed_sources()
        self.assertEqual(seal["test_batch"]["audit"]["sha256"], module.AUDIT_SHA256)
        self.assertEqual(audit["plan"]["sha256"], module.PLAN_SHA256)
        self.assertEqual(len(rows), 89)
        self.assertEqual(set(sources), {"seal", "audit", "plan"})

    def test_a_changed_identifier_source_is_refused(self):
        with self.assertRaises(HarnessError):
            module._read_source(module.PLAN_PATH, "0" * 64)

    def test_stop_when_a_run_does_not_carry_eight_windows(self):
        rows = _plan_rows(REAL_GROUPS)
        rows[0]["useful_windows_expected"] = "7"
        seal = {"test_batch": {"counts": {"total": len(rows), "complete": len(rows),
                                          "physical_trip": 0, "technical_failure": 0,
                                          "not_run": 0, "complete_windows": 623}}}
        audit = {"generic_campaign_audit": {"manifest_count": len(rows),
                                            "useful_windows_complete": 623,
                                            "hashes_verified": True, "accepted": True}}
        outcome = module.verify_useful_windows(seal, audit, rows)
        self.assertEqual(outcome["status"], "STOP")
        self.assertTrue(outcome["problems"])

    def test_stop_when_the_sealed_window_total_is_short(self):
        rows = _plan_rows(REAL_GROUPS)
        seal = {"test_batch": {"counts": {"total": len(rows), "complete": len(rows),
                                          "physical_trip": 0, "technical_failure": 0,
                                          "not_run": 0, "complete_windows": 700}}}
        audit = {"generic_campaign_audit": {"manifest_count": len(rows),
                                            "useful_windows_complete": 700,
                                            "hashes_verified": True, "accepted": True}}
        outcome = module.verify_useful_windows(seal, audit, rows)
        self.assertEqual(outcome["status"], "STOP")

    def test_real_lot_passes_the_precondition(self):
        self.assertEqual(self.artifact["useful_windows_check"]["status"], "PASS")
        self.assertEqual(self.artifact["useful_windows_check"]["useful_windows_sealed_total"], 712)

    def test_assignment_does_not_depend_on_condition_or_recipient(self):
        """The artifact carries no condition, agent, library or repetition field."""
        text = json.dumps(self.artifact["assignment"])
        for token in ("B-LF", "E-LF", "B-noLF", "agent_", "G_P", "G_A", "repetition"):
            self.assertNotIn(token, text)

    def test_committed_artifact_matches_the_generator(self):
        path = module.REPO_ROOT / "studio2/fase03/batch_finale/ASSEGNAZIONE_FINESTRE_7_4.json"
        if not path.is_file():
            self.skipTest("assignment artifact is not committed in this tree")
        stored = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(stored["assignment"], self.artifact["assignment"])
        self.assertEqual(stored["assignment_sha256"], self.artifact["assignment_sha256"])


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
