from __future__ import annotations

import json
import unittest

import numpy as np

from phase_b.evaluation.bootstrap import (
    draw_stratified_physical_clusters,
    expand_cluster_sample,
    paired_unseen_rows,
    stratified_cluster_paired_bootstrap,
)
from phase_b.evaluation.metrics import evaluate_run_records, is_correct
from phase_b.evaluation.records import RunRecord
from phase_b.evaluation.token_logging import make_token_log
from phase_b.tests.helpers import load_config, synthetic_run_records


class MetricsBootstrapRecordsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_config()
        self.records, self.truth = synthetic_run_records(self.config, abstain_one=True)

    def test_abstain_is_counted_incorrect(self) -> None:
        record = next(
            item
            for item in self.records
            if item.condition == "A" and item.parsed_output["abstain"]
        )
        self.assertFalse(is_correct(record, self.truth[record.physical_case_id]))

    def test_metrics_counts_and_pairing(self) -> None:
        result = evaluate_run_records(self.records, case_truth=self.truth, config=self.config)
        self.assertEqual(result["conditions"]["A"]["overall"]["n"], 180)
        self.assertEqual(result["conditions"]["A"]["unseen"]["n"], 108)
        for repetition in ("1", "2", "3"):
            self.assertEqual(result["per_repetition"]["A"][repetition]["unseen"]["n"], 36)
        primary = result["comparisons"]["B_vs_A_primary_unseen"]
        self.assertEqual(primary["n_pairs"], 108)
        self.assertGreater(primary["delta_unseen"], 0)
        self.assertGreater(primary["helped"], primary["harmed"])
        self.assertGreater(result["comparisons"]["delta_FoT_minus_delta_E"], 0)
        self.assertGreaterEqual(
            result["conditions"]["B"]["seen"]["accuracy"],
            result["conditions"]["A"]["seen"]["accuracy"],
        )

    def test_cluster_rows_preserve_all_agent_repetition_members(self) -> None:
        rows = paired_unseen_rows(
            self.records, case_truth=self.truth, config=self.config
        )
        self.assertEqual(len(rows), 108)
        self.assertEqual(len({row["physical_case_id"] for row in rows}), 12)
        per_case = {
            case_id: sum(row["physical_case_id"] == case_id for row in rows)
            for case_id in {row["physical_case_id"] for row in rows}
        }
        self.assertEqual(set(per_case.values()), {9})
        sampled = draw_stratified_physical_clusters(rows, np.random.default_rng(7))
        expanded = expand_cluster_sample(rows, sampled)
        self.assertEqual(len(sampled), 12)
        self.assertEqual(len(expanded), 108)
        for case_id in set(sampled):
            self.assertEqual(
                sum(row["physical_case_id"] == case_id for row in expanded),
                9 * sampled.count(case_id),
            )

    def test_stratified_cluster_bootstrap_reports_twelve_physical_fault_runs(self) -> None:
        result = stratified_cluster_paired_bootstrap(
            self.records,
            case_truth=self.truth,
            config=self.config,
            iterations=200,
            seed=17,
        )
        self.assertEqual(result["n_physical_clusters"], 12)
        self.assertEqual(result["n_agent_case_repetition_rows"], 108)
        self.assertEqual(set(result["clusters_per_pseudolabel"].values()), {3})
        self.assertFalse(result["independence_claim"])

    def test_run_record_and_token_logging(self) -> None:
        record = self.records[0]
        self.assertEqual(RunRecord.from_dict(record.to_dict()), record)
        token_log = make_token_log(
            prompt="abc", completion="de", prompt_tokens=2, completion_tokens=1,
            method="provider_reported",
        )
        self.assertEqual(token_log.total_tokens, 3)
        unavailable = make_token_log(prompt="abc", completion="de")
        self.assertIsNone(unavailable.total_tokens)
        self.assertEqual(unavailable.prompt_characters, 3)


if __name__ == "__main__":
    unittest.main()
