#!/usr/bin/env python3
"""Regression tests for the descriptive FoT payload characterization."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
for path in (ROOT, CODE):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from characterize_fot_communication_payload import (  # noqa: E402
    TOKEN_UNAVAILABLE,
    build_report,
    text_size,
)


class CommunicationPayloadCharacterizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.report = build_report()

    def test_utf8_byte_count_is_not_assumed_equal_to_char_count(self) -> None:
        self.assertEqual(text_size("ASCII"), {"chars": 5, "utf8_bytes": 5})
        self.assertEqual(text_size("variabilità"), {"chars": 11, "utf8_bytes": 12})

    def test_peer_routing_is_six_insights_without_self(self) -> None:
        rows = self.report["actual_fot_textual_payload"]["receivers"]
        self.assertEqual(len(rows), 4)
        for row in rows:
            self.assertEqual(row["n_insights"], 6)
            self.assertNotIn(row["receiver"], row["source_agents"])
            self.assertEqual(len(row["source_agents"]), 3)

    def test_unique_insights_and_transmission_counts(self) -> None:
        payload = self.report["actual_fot_textual_payload"]
        self.assertEqual(payload["unique_knowledge_stored"]["n_unique_insights"], 8)
        self.assertEqual(payload["all_receiver_unit"]["total_insight_transmissions"], 24)
        self.assertEqual(
            set(payload["all_receiver_unit"]["per_unique_insight_receiver_count"].values()),
            {3},
        )

    def test_evidence_counts_follow_frozen_windowing(self) -> None:
        rows = self.report["local_evidence_reference"]["per_source_agent"]
        for row in rows:
            self.assertEqual(row["n_development_batches"], 5)
            self.assertEqual(row["post_injection_samples_consumed_per_batch"], [2400])
            self.assertEqual(row["analysis_windows_total"], 40)
            self.assertEqual(row["xmeas_variables"], 41)
            self.assertEqual(row["raw_observation_values"], 492000)
            self.assertEqual(row["structured_numerical_feature_values"], 8200)

    def test_token_count_is_not_estimated(self) -> None:
        self.assertEqual(self.report["token_count"]["status"], TOKEN_UNAVAILABLE)
        self.assertIsNone(self.report["token_count"]["tokenizer_recorded"])


if __name__ == "__main__":
    unittest.main()
