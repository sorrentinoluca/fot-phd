"""Unit tests for the Condition C schedule builder."""

from __future__ import annotations

import unittest
from collections import Counter
from pathlib import Path

from icl.runner.build_c_schedule import (
    build_schedule,
    canonical_schedule_bytes,
    load_manifest,
    load_pseudolabel_mapping,
)


ROOT = Path(__file__).resolve().parents[2]


EXPECTED_PILOT_CASES = frozenset({
    "PBH-001",   # first Normal
    "PBH-004",   # first fault class 1
    "PBH-007",   # first fault class 2
    "PBH-010",   # first fault class 3
    "PBH-013",   # first fault class 4
})


class TestBuildCSchedule(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.mapping = load_pseudolabel_mapping()
        cls.schedule = build_schedule(cls.manifest, cls.mapping)

    def test_exact_cardinality(self) -> None:
        self.assertEqual(len(self.schedule), 45)

    def test_sequential_sequence_index(self) -> None:
        indices = [e["sequence_index"] for e in self.schedule]
        self.assertEqual(indices, list(range(45)))

    def test_uniqueness(self) -> None:
        keys = {
            (e["physical_case_id"], e["repetition"])
            for e in self.schedule
        }
        self.assertEqual(len(keys), 45)

    def test_all_condition_C(self) -> None:
        for e in self.schedule:
            self.assertEqual(e["condition"], "C")

    def test_all_receiver_central(self) -> None:
        for e in self.schedule:
            self.assertEqual(e["receiver_id"], "central")

    def test_pilot_count_and_cases(self) -> None:
        pilot_entries = [e for e in self.schedule if e["pilot"]]
        non_pilot_entries = [e for e in self.schedule if not e["pilot"]]
        self.assertEqual(len(pilot_entries), 15)
        self.assertEqual(len(non_pilot_entries), 30)
        pilot_case_ids = {e["physical_case_id"] for e in pilot_entries}
        self.assertEqual(pilot_case_ids, EXPECTED_PILOT_CASES)

    def test_pilot_entries_first(self) -> None:
        """Pilot entries occupy sequence_index 0..14."""
        for e in self.schedule[:15]:
            self.assertTrue(
                e["pilot"],
                f"sequence_index {e['sequence_index']} should be pilot",
            )
        for e in self.schedule[15:]:
            self.assertFalse(
                e["pilot"],
                f"sequence_index {e['sequence_index']} should not be pilot",
            )

    def test_ordering_within_pilot_block(self) -> None:
        """Within pilot block: (physical_case_id ASC, repetition ASC)."""
        pilot = self.schedule[:15]
        for i in range(len(pilot) - 1):
            a, b = pilot[i], pilot[i + 1]
            key_a = (a["physical_case_id"], a["repetition"])
            key_b = (b["physical_case_id"], b["repetition"])
            self.assertLess(key_a, key_b)

    def test_ordering_within_non_pilot_block(self) -> None:
        """Within non-pilot block: (physical_case_id ASC, repetition ASC)."""
        non_pilot = self.schedule[15:]
        for i in range(len(non_pilot) - 1):
            a, b = non_pilot[i], non_pilot[i + 1]
            key_a = (a["physical_case_id"], a["repetition"])
            key_b = (b["physical_case_id"], b["repetition"])
            self.assertLess(key_a, key_b)

    def test_repetition_coverage(self) -> None:
        """Each case has exactly repetitions 1, 2, 3."""
        case_reps: dict[str, list[int]] = {}
        for e in self.schedule:
            case_reps.setdefault(e["physical_case_id"], []).append(e["repetition"])
        for case_id, reps in case_reps.items():
            self.assertEqual(
                sorted(reps), [1, 2, 3], f"{case_id} missing repetitions"
            )

    def test_all_15_cases_present(self) -> None:
        case_ids = {e["physical_case_id"] for e in self.schedule}
        expected = {f"PBH-{i:03d}" for i in range(1, 16)}
        self.assertEqual(case_ids, expected)

    def test_deterministic_regeneration(self) -> None:
        first = canonical_schedule_bytes(
            build_schedule(self.manifest, self.mapping)
        )
        second = canonical_schedule_bytes(
            build_schedule(self.manifest, self.mapping)
        )
        self.assertEqual(first, second)

    def test_output_is_label_blind(self) -> None:
        """Schedule output must not contain class, fault, or pseudolabel info."""
        forbidden_keys = {"class_offline", "fault_id", "pseudolabel", "label"}
        for e in self.schedule:
            overlap = set(e.keys()) & forbidden_keys
            self.assertEqual(
                overlap, set(),
                f"entry contains forbidden key(s): {overlap}",
            )

    def test_entry_keys_are_exact(self) -> None:
        expected_keys = {
            "sequence_index", "physical_case_id", "repetition",
            "condition", "receiver_id", "pilot",
        }
        for e in self.schedule:
            self.assertEqual(set(e.keys()), expected_keys)

    def test_pilot_one_per_class(self) -> None:
        """Each pilot case represents a different class in the manifest."""
        manifest_classes = {r["case_id"]: r["class_offline"] for r in self.manifest}
        pilot_classes = {manifest_classes[c] for c in EXPECTED_PILOT_CASES}
        self.assertEqual(len(pilot_classes), 5)

    def test_per_case_repetition_balance(self) -> None:
        counts = Counter(
            (e["physical_case_id"], e["repetition"])
            for e in self.schedule
        )
        self.assertTrue(all(v == 1 for v in counts.values()))
        self.assertEqual(len(counts), 45)


class TestBuildCScheduleRejections(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.mapping = load_pseudolabel_mapping()

    def test_reject_truncated_manifest(self) -> None:
        with self.assertRaises(ValueError):
            build_schedule(self.manifest[:10], self.mapping)

    def test_reject_incomplete_mapping(self) -> None:
        bad_mapping = {"F1": "CLS-ZOGAA"}
        with self.assertRaises(ValueError):
            build_schedule(self.manifest, bad_mapping)

    def test_reject_mismatched_mapping_keys(self) -> None:
        bad_mapping = {
            "F1": "CLS-ZOGAA",
            "F2": "CLS-WRONG",
            "F3": "CLS-WRONG",
            "F4": "CLS-WRONG",
        }
        with self.assertRaises(ValueError):
            build_schedule(self.manifest, bad_mapping)


if __name__ == "__main__":
    unittest.main()
