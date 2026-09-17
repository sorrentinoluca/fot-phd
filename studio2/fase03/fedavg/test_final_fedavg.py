#!/usr/bin/env python3
"""Structural checks for the persisted final FedAvg execution."""

from __future__ import annotations

import csv
import json
import unittest
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).with_name("final")


def rows(name: str) -> list[dict[str, str]]:
    with (ROOT / name).open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


class FinalFedAvgChecks(unittest.TestCase):
    def test_preflight_and_execution_are_single_pass(self) -> None:
        preflight = json.loads((ROOT / "INPUT_PREFLIGHT.json").read_text(encoding="utf-8"))
        state = json.loads((ROOT / "EXECUTION_STATE.json").read_text(encoding="utf-8"))
        self.assertEqual(preflight["status"], "PASS")
        self.assertEqual(state["status"], "completed")
        self.assertEqual(state["training_attempt"], 1)
        self.assertEqual(state["evaluation_attempt"], 1)
        self.assertFalse(state["rerun_allowed"])

    def test_final_evidence_partition(self) -> None:
        evidence = rows("FINAL_EVIDENCE_MANIFEST.csv")
        self.assertEqual(len(evidence), 624)
        self.assertEqual(len({row["evidence_id"] for row in evidence}), 624)
        self.assertEqual(
            Counter(row["evaluation_scope"] for row in evidence),
            Counter(primary=576, ood=48),
        )
        self.assertTrue(all(int(row["signature_dimension"]) == 697 for row in evidence))

    def test_primary_denominators(self) -> None:
        metrics = rows("primary_cluster_metrics.csv")
        self.assertEqual(
            Counter(row["mode"] for row in metrics),
            Counter(local=576, fedavg=72, centralized=72),
        )
        self.assertTrue(all(int(row["n_attempts"]) == 8 for row in metrics))
        self.assertTrue(all(int(row["abstentions"]) == 0 for row in metrics))

    def test_ood_has_counts_but_no_accuracy(self) -> None:
        ood = rows("ood_forced_attributions.csv")
        self.assertEqual(len(ood), 180)
        self.assertNotIn("accuracy", ood[0])
        self.assertNotIn("correct", ood[0])
        totals: defaultdict[tuple[str, str, str], int] = defaultdict(int)
        for row in ood:
            totals[(row["mode"], row["receiver"], row["ood_fault"])] += int(row["count"])
            self.assertEqual(int(row["abstentions"]), 0)
            self.assertEqual(float(row["abstention_rate"]), 0.0)
        self.assertEqual(len(totals), 20)
        self.assertEqual(set(totals.values()), {24})


if __name__ == "__main__":
    unittest.main()
