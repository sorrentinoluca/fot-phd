"""Test mirati del raccordo metriche per il candidato locale d'integrazione.

Classe MetricTests estratta VERBATIM da
studio2/fase03/harness/test_harness.py @ caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae
(delta verificato 5116087..caf5bfb). Le costanti LABELS e AGENTS sono riprodotte identiche
alle fonti verificate (test_harness.py e inputs.py @ caf5bfb) per rendere il test
autosufficiente: gli import sono ridotti al perimetro minimo del raccordo (common,
metric_adapter, metrics), evitando di trascinare i componenti harness/pilot esclusi da questo
candidato (inputs, guards, insight_adapter, canary, logging_v1, producer, sampling, ordering).
Il test_harness.py completo resta conservato nella sua fonte (caf5bfb), non importato qui.
Copre mapping, conteggi, denominatori, astensioni, invalidi, casi limite, rifiuti fail-closed
e controllo SHA-256.
"""
from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import tempfile
import unittest

from studio2.fase03.harness.common import HarnessError, sha256_text
from studio2.fase03.harness.metric_adapter import (
    adapt_baseline_metric,
    load_baseline_metrics,
)
from studio2.fase03.harness.metrics import (
    bootstrap_paired_delta,
    clopper_pearson,
    divergence_summary,
    hoeffding_superiority,
    sign_flip_pvalue,
    tango_noninferiority,
    three_numbers,
)


# Costanti riprodotte verbatim dalle fonti verificate @caf5bfb:
#   LABELS  <- test_harness.py (righe 33-43)
#   AGENTS  <- inputs.py (riga 25)
LABELS = [
    "S2-CLS-3ZGWQ",
    "S2-CLS-4AMS4",
    "S2-CLS-FD3GZ",
    "S2-CLS-GSX3L",
    "S2-CLS-HEW25",
    "S2-CLS-MHMU4",
    "S2-CLS-QRCCB",
    "S2-CLS-TYFPG",
    "Normal",
]
AGENTS = tuple(f"agent_{index}" for index in range(1, 9))


class MetricTests(unittest.TestCase):
    @staticmethod
    def _baseline_metric(
        *, total: int, correct: int, abstained: int
    ) -> dict[str, int | float | None]:
        non_abstained = total - abstained
        return {
            "n": total,
            "correct": correct,
            "abstentions": abstained,
            "non_abstained": non_abstained,
            "accuracy": correct / total if total else None,
            "abstention_rate": abstained / total if total else None,
            "accuracy_non_abstained": (
                correct / non_abstained if non_abstained else None
            ),
        }

    def test_baseline_metric_adapter_renames_without_numeric_changes(self):
        source = self._baseline_metric(total=7, correct=3, abstained=2)
        adapted = adapt_baseline_metric(source)
        self.assertEqual(
            adapted,
            {
                "total": 7,
                "correct": 3,
                "abstained": 2,
                "non_abstained": 5,
                "invalid": 0,
                "accuracy_all": source["accuracy"],
                "abstention_rate": source["abstention_rate"],
                "accuracy_non_abstained": source["accuracy_non_abstained"],
            },
        )
        self.assertIs(adapted["accuracy_all"], source["accuracy"])
        self.assertIs(adapted["abstention_rate"], source["abstention_rate"])
        self.assertIs(
            adapted["accuracy_non_abstained"], source["accuracy_non_abstained"]
        )

    def test_baseline_metric_adapter_all_abstained_and_empty(self):
        all_abstained = adapt_baseline_metric(
            self._baseline_metric(total=4, correct=0, abstained=4)
        )
        self.assertEqual(all_abstained["non_abstained"], 0)
        self.assertEqual(all_abstained["abstention_rate"], 1.0)
        self.assertIsNone(all_abstained["accuracy_non_abstained"])

        empty = adapt_baseline_metric(
            self._baseline_metric(total=0, correct=0, abstained=0)
        )
        self.assertEqual(empty["invalid"], 0)
        self.assertIsNone(empty["accuracy_all"])
        self.assertIsNone(empty["abstention_rate"])
        self.assertIsNone(empty["accuracy_non_abstained"])

    def test_baseline_metric_adapter_rejects_invalid_or_inconsistent_source(self):
        source = self._baseline_metric(total=3, correct=1, abstained=1)
        with self.assertRaisesRegex(HarnessError, "extra=\\['invalid'\\]"):
            adapt_baseline_metric({**source, "invalid": 1})
        with self.assertRaisesRegex(HarnessError, "non_abstained"):
            adapt_baseline_metric({**source, "non_abstained": 1})
        with self.assertRaisesRegex(HarnessError, "accuracy"):
            adapt_baseline_metric({**source, "accuracy": 0.5})

    def test_load_baseline_metrics_adapts_every_consumer_leaf(self):
        ordinary = self._baseline_metric(total=5, correct=2, abstained=1)
        empty = self._baseline_metric(total=0, correct=0, abstained=0)
        summary = {
            condition: {
                population: dict(ordinary if population == "all" else empty)
                for population in ("all", "local_unseen", "local_seen", "normal")
            }
            for condition in ("numeric_global", "numeric_local")
        }
        cluster = {
            "condition": "numeric_global",
            "physical_case_id": "CASE-001",
            "independence_claim": False,
            **ordinary,
        }
        document = {
            "schema_version": 1,
            "status": "TECHNICAL_OUTPUT_NOT_A_PERFORMANCE_ESTIMATE",
            "three_numbers": [
                "accuracy",
                "abstention_rate",
                "accuracy_non_abstained",
            ],
            "statistical_unit": "physical_case_id",
            "independence_claim": False,
            "test_evidence_manifest_sha256": "synthetic",
            "summary": summary,
            "clusters": [cluster],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "metrics.json"
            path.write_text(json.dumps(document), encoding="utf-8")
            adapted = load_baseline_metrics(
                path, expected_sha256=sha256_text(path.read_text(encoding="utf-8"))
            )
            with self.assertRaisesRegex(HarnessError, "SHA-256 mismatch"):
                load_baseline_metrics(path, expected_sha256="0" * 64)

        self.assertEqual(
            adapted["three_numbers"],
            ["accuracy_all", "abstention_rate", "accuracy_non_abstained"],
        )
        leaves = [
            value
            for condition in adapted["summary"].values()
            for value in condition.values()
        ] + adapted["clusters"]
        self.assertEqual(len(leaves), 9)
        self.assertTrue(all(value["invalid"] == 0 for value in leaves))
        self.assertTrue(all("n" not in value for value in leaves))
        self.assertTrue(all("abstentions" not in value for value in leaves))
        self.assertEqual(adapted["summary"]["numeric_global"]["all"]["total"], 5)
        self.assertEqual(
            adapted["summary"]["numeric_global"]["all"]["accuracy_all"],
            ordinary["accuracy"],
        )
        self.assertEqual(
            adapted["metric_interface"]["invalid"],
            "explicit_zero_from_03_9_valid_true_only_fail_closed_contract",
        )

    def test_three_numbers_keep_invalid_in_nonabstained_denominator(self):
        rows = [
            {"valid": True, "abstain": False, "predicted_label": "L", "true_pseudolabel": "L"},
            {"valid": True, "abstain": True, "predicted_label": None, "true_pseudolabel": "L"},
            {"valid": False, "abstain": False, "predicted_label": None, "true_pseudolabel": "L"},
        ]
        value = three_numbers(rows)
        self.assertEqual(value["correct"], 1)
        self.assertEqual(value["invalid"], 1)
        self.assertEqual(value["abstained"], 1)
        self.assertEqual(value["non_abstained"], 2)
        self.assertAlmostEqual(value["accuracy_all"], 1 / 3)
        self.assertEqual(value["accuracy_non_abstained"], 0.5)

    def test_three_numbers_never_turns_invalid_into_abstention_or_correct(self):
        rows = [
            {
                "valid": False,
                "abstain": True,
                "predicted_label": "L",
                "true_pseudolabel": "L",
            }
        ]
        value = three_numbers(rows)
        self.assertEqual(value["total"], 1)
        self.assertEqual(value["correct"], 0)
        self.assertEqual(value["abstained"], 0)
        self.assertEqual(value["non_abstained"], 1)
        self.assertEqual(value["invalid"], 1)
        self.assertEqual(value["accuracy_all"], 0.0)
        self.assertEqual(value["abstention_rate"], 0.0)
        self.assertEqual(value["accuracy_non_abstained"], 0.0)

    def test_three_numbers_empty_and_all_valid_abstained_edges(self):
        empty = three_numbers([])
        self.assertEqual(
            empty,
            {
                "total": 0,
                "correct": 0,
                "abstained": 0,
                "non_abstained": 0,
                "invalid": 0,
                "accuracy_all": None,
                "abstention_rate": None,
                "accuracy_non_abstained": None,
            },
        )
        all_abstained = three_numbers(
            [
                {
                    "valid": True,
                    "abstain": True,
                    "predicted_label": None,
                    "true_pseudolabel": "L",
                }
                for _ in range(2)
            ]
        )
        self.assertEqual(all_abstained["abstained"], 2)
        self.assertEqual(all_abstained["non_abstained"], 0)
        self.assertIsNone(all_abstained["accuracy_non_abstained"])

    def _paired_panel(self):
        rows = []
        for label_index, label in enumerate(LABELS[:-1]):
            for run in range(2):
                case = f"C-{label_index}-{run}"
                for agent_index in range(7):
                    agent = AGENTS[agent_index]
                    for condition, correct in (("A", False), ("B-LF", True)):
                        rows.append(
                            {
                                "agent_id": agent,
                                "physical_case_id": case,
                                "condition": condition,
                                "true_pseudolabel": label,
                                "valid": True,
                                "abstain": False,
                                "predicted_label": label if correct else "Normal",
                            }
                        )
        return rows

    def test_cluster_bootstrap_and_tests(self):
        result = bootstrap_paired_delta(
            self._paired_panel(),
            left_condition="A",
            right_condition="B-LF",
            expected_rows_per_cluster=7,
            iterations=200,
        )
        self.assertEqual(result["point_estimate"], 1.0)
        self.assertEqual(result["n_physical_clusters"], 16)
        self.assertFalse(result["independence_claim"])
        self.assertTrue(hoeffding_superiority([1.0] * 64)["reject"])
        tango = tango_noninferiority([True] * 64, [True] * 64)
        self.assertTrue(tango["zero_discordant_pairs"])
        self.assertTrue(tango["reject_noninferiority_null"])
        lower, upper = clopper_pearson(0, 40)
        self.assertEqual(lower, 0.0)
        self.assertAlmostEqual(upper, 1 - 0.025 ** (1 / 40))
        self.assertEqual(sign_flip_pvalue([1.0, 1.0]), 0.25)

    def test_divergence_ignores_raw_only_difference(self):
        records = []
        for repetition, raw_hash in enumerate(("a", "b", "c"), start=1):
            records.append(
                {
                    "prompt_id": "P1",
                    "repetition": repetition,
                    "parse_valid": True,
                    "parsed_output": {"abstain": False, "predicted_label": "L"},
                    "raw_response_sha256": raw_hash,
                }
            )
        value = divergence_summary(records)
        self.assertEqual(value["divergent_prompt_count"], 0)
        self.assertEqual(value["raw_only_difference_prompt_count"], 1)




if __name__ == "__main__":
    unittest.main()
