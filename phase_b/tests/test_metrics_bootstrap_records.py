from __future__ import annotations

import json
import unittest
from dataclasses import replace

import numpy as np

from phase_b.evaluation.bootstrap import (
    draw_stratified_physical_clusters,
    expand_cluster_sample,
    paired_unseen_rows,
    stratified_cluster_paired_bootstrap,
)
from phase_b.evaluation.aggregation import aggregate_run_records
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
        self.assertEqual(result["conditions"]["A"]["overall"]["n"], 60)
        self.assertEqual(result["conditions"]["A"]["unseen"]["n"], 36)
        self.assertEqual(result["conditions"]["A"]["local_fault_seen"]["n"], 12)
        self.assertEqual(result["conditions"]["A"]["normal"]["n"], 12)
        for repetition in ("1", "2", "3"):
            self.assertEqual(result["per_repetition"]["A"][repetition]["unseen"]["n"], 36)
        primary = result["comparisons"]["B_vs_A_primary_unseen"]
        self.assertEqual(primary["n_pairs"], 36)
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
        self.assertEqual(len(rows), 36)
        self.assertEqual(len({row["physical_case_id"] for row in rows}), 12)
        per_case = {
            case_id: sum(row["physical_case_id"] == case_id for row in rows)
            for case_id in {row["physical_case_id"] for row in rows}
        }
        self.assertEqual(set(per_case.values()), {3})
        sampled = draw_stratified_physical_clusters(rows, np.random.default_rng(7))
        expanded = expand_cluster_sample(rows, sampled)
        self.assertEqual(len(sampled), 12)
        self.assertEqual(len(expanded), 36)
        for case_id in set(sampled):
            self.assertEqual(
                sum(row["physical_case_id"] == case_id for row in expanded),
                3 * sampled.count(case_id),
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
        self.assertEqual(result["n_agent_case_rows"], 36)
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

    def test_r3_aggregation_rule_including_three_way_tie(self) -> None:
        base = next(
            item for item in self.records
            if item.agent_id == "agent_1" and item.condition == "A"
        )
        labels = self.config["label_space"][:3]

        def group(case_id: str, outcomes: list[str | None]) -> list[RunRecord]:
            rows: list[RunRecord] = []
            for repetition, label in enumerate(outcomes, start=1):
                parsed = {
                    "predicted_label": label,
                    "abstain": label is None,
                    "used_insight_ids": [],
                    "reasoning_summary": "fixture",
                }
                rows.append(
                    replace(
                        base,
                        repetition=repetition,
                        physical_case_id=case_id,
                        parsed_output=parsed,
                        raw_output=json.dumps(parsed),
                        raw_attempts=(json.dumps(parsed),),
                    )
                )
            return rows

        rows = [
            *group("AGG-1", [labels[0], labels[0], labels[1]]),
            *group("AGG-2", [labels[0], labels[0], None]),
            *group("AGG-3", [labels[0], labels[1], labels[2]]),
            *group("AGG-4", [labels[0], labels[1], None]),
            *group("AGG-5", [None, None, labels[0]]),
        ]
        aggregates = {
            item.physical_case_id: item
            for item in aggregate_run_records(rows, label_space=self.config["label_space"])
        }
        self.assertEqual(aggregates["AGG-1"].parsed_output["predicted_label"], labels[0])
        self.assertEqual(aggregates["AGG-2"].parsed_output["predicted_label"], labels[0])
        for case_id in ("AGG-3", "AGG-4", "AGG-5"):
            self.assertTrue(aggregates[case_id].parsed_output["abstain"])
            self.assertIsNone(aggregates[case_id].parsed_output["predicted_label"])


if __name__ == "__main__":
    unittest.main()
