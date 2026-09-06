"""Tests for icl.evaluation.evaluate_c_predictions — Condition C evaluator.

Rewritten for the R5-compliant paired-delta evaluator (R5 §5.2/§5.3).
"""

from __future__ import annotations

import csv
import hashlib
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch
from pathlib import Path
from typing import Any

from icl.evaluation.aggregation_c import CAggregatePrediction
from icl.evaluation.evaluate_c_predictions import (
    ABSTAIN_TOKEN,
    EVALUATOR_FREEZE_MANIFEST_PATH,
    bootstrap_paired_delta,
    build_paired_rows,
    condition_c_metrics,
    delta_c_minus_b,
    evaluate_c_predictions,
    is_correct,
    load_agents_config,
    load_case_truth,
    unseen_agents,
    verify_c_predictions_freeze,
    verify_evaluator_freeze,
)
from icl.runner.records_c import CRunRecord, LABEL_SPACE


# ------------------------------------------------------------------ helpers

_PROMPT_HASH = hashlib.sha256(b"test-prompt").hexdigest()

# 15 held-out case IDs.
_CASE_IDS = [f"PBH-{i:03d}" for i in range(1, 16)]

# 5 classes × 3 runs each = 15 cases.
_CLASS_ASSIGNMENT = {
    "PBH-001": "Normal", "PBH-002": "Normal", "PBH-003": "Normal",
    "PBH-004": "CLS-ZOGAA", "PBH-005": "CLS-ZOGAA", "PBH-006": "CLS-ZOGAA",
    "PBH-007": "CLS-OJNSG", "PBH-008": "CLS-OJNSG", "PBH-009": "CLS-OJNSG",
    "PBH-010": "CLS-R463B", "PBH-011": "CLS-R463B", "PBH-012": "CLS-R463B",
    "PBH-013": "CLS-Z3ISU", "PBH-014": "CLS-Z3ISU", "PBH-015": "CLS-Z3ISU",
}

# Canonical agents config (mirrors protocol_config.json).
_AGENTS_CONFIG = {
    "agent_1": "CLS-ZOGAA",
    "agent_2": "CLS-OJNSG",
    "agent_3": "CLS-R463B",
    "agent_4": "CLS-Z3ISU",
}

_FAULT_CASE_IDS = [cid for cid in _CASE_IDS if _CLASS_ASSIGNMENT[cid] != "Normal"]


def _make_c_record(
    case_id: str,
    repetition: int,
    predicted_label: str | None = "Normal",
    abstain: bool = False,
    parse_failure: bool = False,
    sequence_index: int = 0,
) -> CRunRecord:
    """Build a minimal valid CRunRecord."""
    if parse_failure:
        parsed = {
            "predicted_label": None, "abstain": True,
            "used_insight_ids": [], "reasoning_summary": "parse_failure",
        }
    elif abstain:
        parsed = {
            "predicted_label": None, "abstain": True,
            "used_insight_ids": [], "reasoning_summary": "abstain_label",
        }
    else:
        parsed = {
            "predicted_label": predicted_label, "abstain": False,
            "used_insight_ids": ["INS-001"], "reasoning_summary": "reasoning",
        }

    return CRunRecord(
        agent_id="central", condition="C",
        physical_case_id=case_id, repetition=repetition,
        sequence_index=sequence_index,
        parsed_output=parsed, valid=not parse_failure,
        prompt_sha256=_PROMPT_HASH,
        raw_attempts=[{
            "attempt_index": 0, "raw_response": "{}",
            "parse_success": True, "error_type": None,
            "request_id": "r1", "response_id": "r1",
            "token_usage": {"prompt_tokens": 100,
                            "completion_tokens": 10,
                            "total_tokens": 110},
        }],
        retry_count=0, model_requested="gpt-5.6-terra",
        model_returned="gpt-5.6-terra", reasoning_effort="medium",
        timestamp_iso="2026-09-06T12:00:00+00:00", stateless=True,
    )


def _make_triplet(
    case_id: str,
    predicted_label: str | None = "Normal",
    abstain: bool = False,
) -> list[CRunRecord]:
    """Build 3 repetitions for one case, all predicting the same label."""
    return [
        _make_c_record(case_id, rep, predicted_label, abstain,
                       sequence_index=(rep - 1))
        for rep in (1, 2, 3)
    ]


def _all_correct_records() -> list[CRunRecord]:
    """Build 45 records (15 cases × 3 reps), all predicting correctly."""
    records = []
    seq = 0
    for case_id in _CASE_IDS:
        truth = _CLASS_ASSIGNMENT[case_id]
        for rep in (1, 2, 3):
            records.append(_make_c_record(case_id, rep, truth,
                                          sequence_index=seq))
            seq += 1
    return records


def _make_aggregate(
    case_id: str,
    predicted_label: str | None,
    abstain: bool = False,
) -> CAggregatePrediction:
    """Build a CAggregatePrediction directly."""
    if abstain:
        parsed = {
            "predicted_label": None, "abstain": True,
            "used_insight_ids": [],
            "reasoning_summary": "aggregate_no_label_majority",
        }
    else:
        parsed = {
            "predicted_label": predicted_label, "abstain": False,
            "used_insight_ids": [],
            "reasoning_summary": "aggregate_majority_2_of_3",
        }
    return CAggregatePrediction(
        agent_id="central", condition="C",
        physical_case_id=case_id, parsed_output=parsed,
        repetition_outcomes=(
            {"repetition": 1, "predicted_label": predicted_label,
             "abstain": abstain, "parse_failure": False},
            {"repetition": 2, "predicted_label": predicted_label,
             "abstain": abstain, "parse_failure": False},
            {"repetition": 3, "predicted_label": predicted_label,
             "abstain": abstain, "parse_failure": False},
        ),
    )


def _phase_b_aggregate(
    agent_id: str,
    case_id: str,
    predicted_label: str | None,
    abstain: bool = False,
) -> dict[str, Any]:
    """Build a Phase B-style aggregate record dict (condition='B')."""
    if abstain:
        parsed = {
            "predicted_label": None, "abstain": True,
            "used_insight_ids": [],
            "reasoning_summary": "aggregate_no_label_majority",
        }
    else:
        parsed = {
            "predicted_label": predicted_label, "abstain": False,
            "used_insight_ids": [],
            "reasoning_summary": "aggregate_majority_2_of_3",
        }
    return {
        "agent_id": agent_id,
        "condition": "B",
        "physical_case_id": case_id,
        "parsed_output": parsed,
        "repetition_outcomes": [
            {"repetition": r, "predicted_label": predicted_label,
             "abstain": abstain, "parse_failure": False}
            for r in (1, 2, 3)
        ],
        "aggregation_rule": "frozen_valid_label_majority_2_of_3_else_abstain",
    }


def _full_b_records(
    all_correct: bool = True,
) -> list[dict[str, Any]]:
    """Build Phase B aggregate records for all 4 agents × 15 cases.

    Only condition='B' records, as required by the paired delta.
    """
    records = []
    for agent_id, local_fault in _AGENTS_CONFIG.items():
        for cid in _CASE_IDS:
            truth = _CLASS_ASSIGNMENT[cid]
            if all_correct:
                predicted = truth
            else:
                predicted = "Normal"  # Wrong for all fault cases.
            records.append(
                _phase_b_aggregate(agent_id, cid, predicted)
            )
    return records


# ================================================================== tests


class TestIsCorrect(unittest.TestCase):

    def test_correct(self) -> None:
        agg = _make_aggregate("PBH-001", "Normal")
        self.assertTrue(is_correct(agg, "Normal"))

    def test_incorrect_label(self) -> None:
        agg = _make_aggregate("PBH-001", "CLS-ZOGAA")
        self.assertFalse(is_correct(agg, "Normal"))

    def test_abstain_is_incorrect(self) -> None:
        agg = _make_aggregate("PBH-001", None, abstain=True)
        self.assertFalse(is_correct(agg, "Normal"))

    def test_dict_input(self) -> None:
        rec = {"parsed_output": {"predicted_label": "Normal", "abstain": False}}
        self.assertTrue(is_correct(rec, "Normal"))


class TestUnseenAgents(unittest.TestCase):
    """Test unseen_agents() against canonical agents config."""

    def test_fault_label_zogaa(self) -> None:
        """CLS-ZOGAA truth → agent_1 is the sighted agent, rest unseen."""
        result = unseen_agents("CLS-ZOGAA", _AGENTS_CONFIG)
        self.assertEqual(result, ["agent_2", "agent_3", "agent_4"])

    def test_fault_label_ojnsg(self) -> None:
        result = unseen_agents("CLS-OJNSG", _AGENTS_CONFIG)
        self.assertEqual(result, ["agent_1", "agent_3", "agent_4"])

    def test_normal_returns_all_four(self) -> None:
        """Normal has no matching local_fault_label → all 4 unseen."""
        result = unseen_agents("Normal", _AGENTS_CONFIG)
        self.assertEqual(len(result), 4)

    def test_sorted_output(self) -> None:
        for label in _AGENTS_CONFIG.values():
            result = unseen_agents(label, _AGENTS_CONFIG)
            self.assertEqual(result, sorted(result))


class TestConditionCMetrics(unittest.TestCase):

    def test_perfect_accuracy(self) -> None:
        aggregates = [
            _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        result = condition_c_metrics(aggregates, _CLASS_ASSIGNMENT)
        self.assertEqual(result["overall"]["n"], 15)
        self.assertEqual(result["overall"]["correct"], 15)
        self.assertAlmostEqual(result["overall"]["accuracy"], 1.0)

    def test_accuracy_c_fault_and_normal(self) -> None:
        """R5 §3.8: accuracy_C_fault (n=12), accuracy_C_normal (n=3)."""
        aggregates = [
            _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        result = condition_c_metrics(aggregates, _CLASS_ASSIGNMENT)
        self.assertEqual(result["accuracy_C_fault"]["n"], 12)
        self.assertAlmostEqual(result["accuracy_C_fault"]["accuracy"], 1.0)
        self.assertEqual(result["accuracy_C_normal"]["n"], 3)
        self.assertAlmostEqual(result["accuracy_C_normal"]["accuracy"], 1.0)

    def test_fault_normal_split(self) -> None:
        """All predict Normal → fault accuracy=0, normal accuracy=1."""
        aggregates = [_make_aggregate(cid, "Normal") for cid in _CASE_IDS]
        result = condition_c_metrics(aggregates, _CLASS_ASSIGNMENT)
        self.assertEqual(result["accuracy_C_fault"]["correct"], 0)
        self.assertAlmostEqual(result["accuracy_C_fault"]["accuracy"], 0.0)
        self.assertEqual(result["accuracy_C_normal"]["correct"], 3)
        self.assertAlmostEqual(result["accuracy_C_normal"]["accuracy"], 1.0)

    def test_per_class_breakdown(self) -> None:
        aggregates = [
            _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        result = condition_c_metrics(aggregates, _CLASS_ASSIGNMENT)
        for label in LABEL_SPACE:
            self.assertEqual(result["per_class"][label]["n"], 3)
            self.assertEqual(result["per_class"][label]["correct"], 3)

    def test_abstentions_counted(self) -> None:
        aggregates = [
            _make_aggregate(cid, None, abstain=True) if cid == "PBH-001"
            else _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        result = condition_c_metrics(aggregates, _CLASS_ASSIGNMENT)
        self.assertEqual(result["overall"]["abstentions"], 1)
        self.assertEqual(result["overall"]["correct"], 14)

    def test_confusion_matrix_structure(self) -> None:
        aggregates = [
            _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        result = condition_c_metrics(aggregates, _CLASS_ASSIGNMENT)
        confusion = result["confusion_matrix"]
        for truth in sorted(LABEL_SPACE):
            self.assertIn(truth, confusion)
            self.assertIn(ABSTAIN_TOKEN, confusion[truth])

    def test_confusion_matrix_sums(self) -> None:
        aggregates = [
            _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        result = condition_c_metrics(aggregates, _CLASS_ASSIGNMENT)
        total = sum(
            count
            for row in result["confusion_matrix"].values()
            for count in row.values()
        )
        self.assertEqual(total, 15)

    def test_empty_aggregates(self) -> None:
        result = condition_c_metrics([], _CLASS_ASSIGNMENT)
        self.assertEqual(result["overall"]["n"], 0)
        self.assertIsNone(result["overall"]["accuracy"])


class TestBuildPairedRows(unittest.TestCase):
    """R5 §5.2: paired rows for the 12 fault cases."""

    def test_all_c_correct_all_b_correct(self) -> None:
        """Both C and B all correct → every paired_delta_i = 0."""
        c_aggs = [
            _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        b_recs = _full_b_records(all_correct=True)
        rows = build_paired_rows(
            c_aggs, b_recs, _CLASS_ASSIGNMENT, _AGENTS_CONFIG
        )
        self.assertEqual(len(rows), 12)
        for row in rows:
            self.assertAlmostEqual(row["paired_delta_i"], 0.0)

    def test_c_correct_b_all_wrong(self) -> None:
        """C correct, B unseen agents all wrong → delta = 1."""
        c_aggs = [
            _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        b_recs = _full_b_records(all_correct=False)
        rows = build_paired_rows(
            c_aggs, b_recs, _CLASS_ASSIGNMENT, _AGENTS_CONFIG
        )
        self.assertEqual(len(rows), 12)
        for row in rows:
            self.assertEqual(row["c_correct"], 1)
            # B all predict "Normal" → for fault cases, b_unseen_mean = 0.
            self.assertAlmostEqual(row["b_unseen_mean"], 0.0)
            self.assertAlmostEqual(row["paired_delta_i"], 1.0)

    def test_c_wrong_b_correct(self) -> None:
        """C all wrong, B all correct → delta = -1."""
        c_aggs = [
            _make_aggregate(cid, "Normal")  # Wrong for all fault cases.
            for cid in _CASE_IDS
        ]
        b_recs = _full_b_records(all_correct=True)
        rows = build_paired_rows(
            c_aggs, b_recs, _CLASS_ASSIGNMENT, _AGENTS_CONFIG
        )
        for row in rows:
            self.assertEqual(row["c_correct"], 0)
            self.assertAlmostEqual(row["b_unseen_mean"], 1.0)
            self.assertAlmostEqual(row["paired_delta_i"], -1.0)

    def test_only_fault_cases(self) -> None:
        """Normal cases are excluded from paired rows."""
        c_aggs = [
            _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        b_recs = _full_b_records(all_correct=True)
        rows = build_paired_rows(
            c_aggs, b_recs, _CLASS_ASSIGNMENT, _AGENTS_CONFIG
        )
        for row in rows:
            self.assertNotEqual(row["true_pseudolabel"], "Normal")

    def test_unseen_mean_partial(self) -> None:
        """If 1 of 3 unseen B agents is correct, b_unseen_mean = 1/3."""
        c_aggs = [
            _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        # For PBH-004 (truth=CLS-ZOGAA), unseen = agent_2, agent_3, agent_4.
        # Make agent_2 correct, agent_3 and agent_4 wrong.
        b_recs = []
        for agent_id in _AGENTS_CONFIG:
            for cid in _CASE_IDS:
                truth = _CLASS_ASSIGNMENT[cid]
                if cid == "PBH-004" and agent_id in ("agent_3", "agent_4"):
                    predicted = "Normal"  # Wrong.
                else:
                    predicted = truth  # Correct.
                b_recs.append(_phase_b_aggregate(agent_id, cid, predicted))

        rows = build_paired_rows(
            c_aggs, b_recs, _CLASS_ASSIGNMENT, _AGENTS_CONFIG
        )
        row_004 = [r for r in rows if r["physical_case_id"] == "PBH-004"][0]
        # agent_2 correct, agent_3 wrong, agent_4 wrong → 1/3.
        self.assertAlmostEqual(row_004["b_unseen_mean"], 1.0 / 3.0)
        self.assertAlmostEqual(row_004["paired_delta_i"], 1.0 - 1.0 / 3.0)

    def test_missing_c_aggregate_raises(self) -> None:
        """Missing C aggregate for a fault case → ValueError."""
        # Only aggregate for PBH-001..003 (Normal).
        c_aggs = [
            _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS[:3]
        ]
        b_recs = _full_b_records(all_correct=True)
        with self.assertRaises(ValueError) as ctx:
            build_paired_rows(
                c_aggs, b_recs, _CLASS_ASSIGNMENT, _AGENTS_CONFIG
            )
        self.assertIn("missing C aggregate", str(ctx.exception))

    def test_missing_b_agent_raises(self) -> None:
        """Missing B record for an unseen agent → ValueError."""
        c_aggs = [
            _make_aggregate(cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        # Only agent_1 records — missing agent_2, 3, 4.
        b_recs = [
            _phase_b_aggregate("agent_1", cid, _CLASS_ASSIGNMENT[cid])
            for cid in _CASE_IDS
        ]
        with self.assertRaises(ValueError) as ctx:
            build_paired_rows(
                c_aggs, b_recs, _CLASS_ASSIGNMENT, _AGENTS_CONFIG
            )
        self.assertIn("missing B aggregate", str(ctx.exception))


class TestDeltaCMinusB(unittest.TestCase):
    """R5 §5.2: paired delta point estimate."""

    def _make_paired_rows(
        self,
        c_correct: list[int],
        b_unseen_means: list[float],
    ) -> list[dict[str, Any]]:
        """Build paired rows from parallel c_correct/b_unseen_mean lists."""
        labels = ["CLS-ZOGAA"] * 3 + ["CLS-OJNSG"] * 3 + \
                 ["CLS-R463B"] * 3 + ["CLS-Z3ISU"] * 3
        rows = []
        for i in range(12):
            rows.append({
                "physical_case_id": _FAULT_CASE_IDS[i],
                "true_pseudolabel": labels[i],
                "c_correct": c_correct[i],
                "b_unseen_mean": b_unseen_means[i],
                "paired_delta_i": c_correct[i] - b_unseen_means[i],
            })
        return rows

    def test_delta_zero(self) -> None:
        rows = self._make_paired_rows([1] * 12, [1.0] * 12)
        result = delta_c_minus_b(rows)
        self.assertAlmostEqual(result["delta_C_minus_B"], 0.0)

    def test_delta_positive(self) -> None:
        rows = self._make_paired_rows([1] * 12, [0.0] * 12)
        result = delta_c_minus_b(rows)
        self.assertAlmostEqual(result["delta_C_minus_B"], 1.0)

    def test_delta_negative(self) -> None:
        rows = self._make_paired_rows([0] * 12, [1.0] * 12)
        result = delta_c_minus_b(rows)
        self.assertAlmostEqual(result["delta_C_minus_B"], -1.0)

    def test_delta_mixed(self) -> None:
        """C gets 6/12 correct, B unseen mean = 1/3 each."""
        c = [1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0]
        b = [1/3] * 12
        rows = self._make_paired_rows(c, b)
        result = delta_c_minus_b(rows)
        expected = sum(c[i] - b[i] for i in range(12)) / 12.0
        self.assertAlmostEqual(result["delta_C_minus_B"], expected)

    def test_wrong_count_raises(self) -> None:
        with self.assertRaises(ValueError):
            delta_c_minus_b([{"paired_delta_i": 0.0}] * 10)

    def test_structure(self) -> None:
        rows = self._make_paired_rows([1] * 12, [0.5] * 12)
        result = delta_c_minus_b(rows)
        self.assertEqual(result["estimand"], "paired_delta_C_minus_B_fault_only")
        self.assertEqual(result["formula"], "R5_§5.2")
        self.assertEqual(result["n_fault_cases"], 12)
        self.assertIn("per_case", result)
        self.assertEqual(len(result["per_case"]), 12)


class TestBootstrapPairedDelta(unittest.TestCase):
    """R5 §5.3: stratified cluster bootstrap on paired delta."""

    def _make_uniform_rows(self, delta: float) -> list[dict[str, Any]]:
        """12 rows with uniform paired_delta_i."""
        labels = ["CLS-ZOGAA"] * 3 + ["CLS-OJNSG"] * 3 + \
                 ["CLS-R463B"] * 3 + ["CLS-Z3ISU"] * 3
        return [
            {
                "physical_case_id": _FAULT_CASE_IDS[i],
                "true_pseudolabel": labels[i],
                "c_correct": 1 if delta > 0 else 0,
                "b_unseen_mean": 1.0 - delta if delta > 0 else 1.0,
                "paired_delta_i": delta,
            }
            for i in range(12)
        ]

    def test_uniform_positive_delta(self) -> None:
        """All delta=1 → CI = [1.0, 1.0]."""
        rows = self._make_uniform_rows(1.0)
        result = bootstrap_paired_delta(rows, iterations=500, seed=42)
        self.assertAlmostEqual(result["point_estimate"], 1.0)
        self.assertAlmostEqual(result["ci_lower"], 1.0)
        self.assertAlmostEqual(result["ci_upper"], 1.0)

    def test_uniform_zero_delta(self) -> None:
        """All delta=0 → CI = [0.0, 0.0]."""
        rows = self._make_uniform_rows(0.0)
        result = bootstrap_paired_delta(rows, iterations=500, seed=42)
        self.assertAlmostEqual(result["point_estimate"], 0.0)
        self.assertAlmostEqual(result["ci_lower"], 0.0)
        self.assertAlmostEqual(result["ci_upper"], 0.0)

    def test_ci_bounds_order(self) -> None:
        """ci_lower ≤ point_estimate ≤ ci_upper."""
        # Mixed deltas for some variance.
        labels = ["CLS-ZOGAA"] * 3 + ["CLS-OJNSG"] * 3 + \
                 ["CLS-R463B"] * 3 + ["CLS-Z3ISU"] * 3
        rows = [
            {
                "physical_case_id": _FAULT_CASE_IDS[i],
                "true_pseudolabel": labels[i],
                "c_correct": 1 if i % 2 == 0 else 0,
                "b_unseen_mean": 0.5,
                "paired_delta_i": (1 if i % 2 == 0 else 0) - 0.5,
            }
            for i in range(12)
        ]
        result = bootstrap_paired_delta(rows, iterations=500, seed=123)
        self.assertLessEqual(result["ci_lower"], result["point_estimate"])
        self.assertLessEqual(result["point_estimate"], result["ci_upper"])

    def test_deterministic_seed(self) -> None:
        rows = self._make_uniform_rows(0.5)
        r1 = bootstrap_paired_delta(rows, iterations=200, seed=99)
        r2 = bootstrap_paired_delta(rows, iterations=200, seed=99)
        self.assertEqual(r1["ci_lower"], r2["ci_lower"])
        self.assertEqual(r1["ci_upper"], r2["ci_upper"])

    def test_structure(self) -> None:
        rows = self._make_uniform_rows(0.5)
        result = bootstrap_paired_delta(rows, iterations=100, seed=42)
        self.assertEqual(result["n_physical_clusters"], 12)
        self.assertEqual(result["iterations"], 100)
        self.assertEqual(result["seed"], 42)
        self.assertAlmostEqual(result["confidence_level"], 0.95)
        self.assertEqual(result["statistic"], "paired_delta_C_minus_B")
        self.assertFalse(result["independence_claim"])
        # 4 fault strata × 3 clusters each.
        self.assertEqual(
            set(result["clusters_per_pseudolabel"].values()),
            {3},
        )
        self.assertEqual(len(result["clusters_per_pseudolabel"]), 4)

    def test_empty_raises(self) -> None:
        with self.assertRaises(ValueError):
            bootstrap_paired_delta([])

    def test_wrong_count_raises(self) -> None:
        rows = self._make_uniform_rows(0.5)[:10]
        with self.assertRaises(ValueError):
            bootstrap_paired_delta(rows)


class TestVerifyEvaluatorFreeze(unittest.TestCase):
    """Evaluator-side freeze guard."""

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write(self, rel_path: str, content: str) -> str:
        p = self.tmpdir / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def test_pass(self) -> None:
        """All files present and well-formed → no error."""
        mapping_content = json.dumps({
            "real_to_opaque": {"F1": "CLS-ZOGAA"},
            "normal_label": "Normal",
        })
        mapping_hash = self._write("mapping.json", mapping_content)
        csv_hash = self._write("manifest.csv", "case_id,class_offline\n")
        b_agg_content = '{"agent_id":"agent_1"}\n'
        b_hash = self._write("b_agg.jsonl", b_agg_content)
        hash_manifest = json.dumps({
            "artifacts": {"b_agg.jsonl": b_hash},
        })
        self._write("hash_manifest.json", hash_manifest)

        # Create a real evaluator freeze manifest (fail-closed requires it).
        eval_manifest = json.dumps({
            "artifact_hashes": {
                "mapping.json": mapping_hash,
                "manifest.csv": csv_hash,
            },
        })
        self._write("eval_freeze.json", eval_manifest)

        result = verify_evaluator_freeze(
            manifest_path=self.tmpdir / "eval_freeze.json",
            heldout_manifest_path=self.tmpdir / "manifest.csv",
            mapping_path=self.tmpdir / "mapping.json",
            b_aggregate_path=self.tmpdir / "b_agg.jsonl",
            hash_manifest_path=self.tmpdir / "hash_manifest.json",
            root=self.tmpdir,
        )
        self.assertIn("pseudolabel_mapping_sha256", result)
        self.assertIn("heldout_manifest_sha256", result)
        self.assertIn("b_aggregate_sha256", result)
        self.assertTrue(result.get("b_aggregate_hash_verified"))
        self.assertTrue(result.get("evaluator_manifest_verified"))

    def test_missing_manifest_raises(self) -> None:
        """P1-4: missing evaluator manifest → FileNotFoundError (fail-closed)."""
        mapping_content = json.dumps({
            "real_to_opaque": {"F1": "CLS-ZOGAA"},
            "normal_label": "Normal",
        })
        self._write("mapping.json", mapping_content)
        self._write("manifest.csv", "")
        self._write("b_agg.jsonl", "")
        with self.assertRaises(FileNotFoundError):
            verify_evaluator_freeze(
                manifest_path=self.tmpdir / "nonexistent_manifest.json",
                heldout_manifest_path=self.tmpdir / "manifest.csv",
                mapping_path=self.tmpdir / "mapping.json",
                b_aggregate_path=self.tmpdir / "b_agg.jsonl",
                hash_manifest_path=self.tmpdir / "hash_manifest.json",
                root=self.tmpdir,
            )

    def test_missing_mapping_raises(self) -> None:
        csv_hash = self._write("manifest.csv", "")
        self._write("b_agg.jsonl", "")
        eval_manifest = json.dumps({"artifact_hashes": {
            "manifest.csv": csv_hash,
        }})
        self._write("eval_freeze.json", eval_manifest)
        with self.assertRaises(FileNotFoundError):
            verify_evaluator_freeze(
                manifest_path=self.tmpdir / "eval_freeze.json",
                heldout_manifest_path=self.tmpdir / "manifest.csv",
                mapping_path=self.tmpdir / "nonexistent.json",
                b_aggregate_path=self.tmpdir / "b_agg.jsonl",
                hash_manifest_path=self.tmpdir / "hash_manifest.json",
                root=self.tmpdir,
            )

    def test_bad_mapping_keys_raises(self) -> None:
        mapping_hash = self._write("mapping.json", json.dumps({"wrong": "keys"}))
        csv_hash = self._write("manifest.csv", "")
        self._write("b_agg.jsonl", "")
        eval_manifest = json.dumps({"artifact_hashes": {
            "mapping.json": mapping_hash,
            "manifest.csv": csv_hash,
        }})
        self._write("eval_freeze.json", eval_manifest)
        with self.assertRaises(ValueError):
            verify_evaluator_freeze(
                manifest_path=self.tmpdir / "eval_freeze.json",
                heldout_manifest_path=self.tmpdir / "manifest.csv",
                mapping_path=self.tmpdir / "mapping.json",
                b_aggregate_path=self.tmpdir / "b_agg.jsonl",
                hash_manifest_path=self.tmpdir / "hash_manifest.json",
                root=self.tmpdir,
            )

    def test_b_aggregate_hash_mismatch(self) -> None:
        mapping = json.dumps({
            "real_to_opaque": {"F1": "CLS-ZOGAA"},
            "normal_label": "Normal",
        })
        mapping_hash = self._write("mapping.json", mapping)
        csv_hash = self._write("manifest.csv", "")
        self._write("b_agg.jsonl", '{"data":"value"}\n')
        self._write("hash_manifest.json", json.dumps({
            "artifacts": {"b_agg.jsonl": "0" * 64},
        }))
        eval_manifest = json.dumps({"artifact_hashes": {
            "mapping.json": mapping_hash,
            "manifest.csv": csv_hash,
        }})
        self._write("eval_freeze.json", eval_manifest)
        with self.assertRaises(RuntimeError) as ctx:
            verify_evaluator_freeze(
                manifest_path=self.tmpdir / "eval_freeze.json",
                heldout_manifest_path=self.tmpdir / "manifest.csv",
                mapping_path=self.tmpdir / "mapping.json",
                b_aggregate_path=self.tmpdir / "b_agg.jsonl",
                hash_manifest_path=self.tmpdir / "hash_manifest.json",
                root=self.tmpdir,
            )
        self.assertIn("hash mismatch", str(ctx.exception))

    def test_manifest_based_verification(self) -> None:
        """When evaluator manifest file exists, verify all hashes."""
        mapping = json.dumps({
            "real_to_opaque": {"F1": "CLS-ZOGAA"},
            "normal_label": "Normal",
        })
        mapping_hash = self._write("mapping.json", mapping)
        csv_hash = self._write("manifest.csv", "case_id,class_offline\n")
        b_hash = self._write("b_agg.jsonl", '{"agent_id":"agent_1"}\n')
        self._write("hash_manifest.json", json.dumps({
            "artifacts": {"b_agg.jsonl": b_hash},
        }))

        # Create evaluator freeze manifest with correct hashes
        eval_manifest = {
            "artifact_hashes": {
                "mapping.json": mapping_hash,
                "manifest.csv": csv_hash,
            },
        }
        self._write("eval_freeze.json", json.dumps(eval_manifest))

        result = verify_evaluator_freeze(
            manifest_path=self.tmpdir / "eval_freeze.json",
            heldout_manifest_path=self.tmpdir / "manifest.csv",
            mapping_path=self.tmpdir / "mapping.json",
            b_aggregate_path=self.tmpdir / "b_agg.jsonl",
            hash_manifest_path=self.tmpdir / "hash_manifest.json",
            root=self.tmpdir,
        )
        self.assertTrue(result.get("evaluator_manifest_verified"))

    def test_manifest_hash_mismatch_raises(self) -> None:
        """When evaluator manifest has wrong hash, raise RuntimeError."""
        mapping = json.dumps({
            "real_to_opaque": {"F1": "CLS-ZOGAA"},
            "normal_label": "Normal",
        })
        self._write("mapping.json", mapping)
        self._write("manifest.csv", "case_id,class_offline\n")
        self._write("b_agg.jsonl", '{"agent_id":"agent_1"}\n')

        eval_manifest = {
            "artifact_hashes": {
                "mapping.json": "0" * 64,
            },
        }
        self._write("eval_freeze.json", json.dumps(eval_manifest))

        with self.assertRaises(RuntimeError) as ctx:
            verify_evaluator_freeze(
                manifest_path=self.tmpdir / "eval_freeze.json",
                heldout_manifest_path=self.tmpdir / "manifest.csv",
                mapping_path=self.tmpdir / "mapping.json",
                b_aggregate_path=self.tmpdir / "b_agg.jsonl",
                hash_manifest_path=self.tmpdir / "hash_manifest.json",
                root=self.tmpdir,
            )
        self.assertIn("evaluator freeze guard", str(ctx.exception))


class TestEvaluatorManifestPath(unittest.TestCase):
    """Verify EVALUATOR_FREEZE_MANIFEST_PATH points to the right file."""

    def test_path_name(self) -> None:
        self.assertEqual(
            EVALUATOR_FREEZE_MANIFEST_PATH.name,
            "freeze_manifest_evaluator.json",
        )

    def test_path_under_full_evaluation(self) -> None:
        self.assertTrue(
            str(EVALUATOR_FREEZE_MANIFEST_PATH).endswith(
                "icl/full_evaluation/freeze_manifest_evaluator.json"
            ),
            f"unexpected path: {EVALUATOR_FREEZE_MANIFEST_PATH}",
        )


class TestFirewall(unittest.TestCase):
    """Verify the evaluator-side firewall contract."""

    def test_evaluator_does_not_import_runner_internals(self) -> None:
        import icl.evaluation.evaluate_c_predictions as mod
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertNotIn("from icl.runner.run_c_inference", source)
        self.assertNotIn("from phase_b.execution", source)
        self.assertNotIn("OpenAIAdapter", source)

    def test_evaluator_reads_pseudolabel_mapping(self) -> None:
        import icl.evaluation.evaluate_c_predictions as mod
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertIn("pseudolabel_mapping.json", source)

    def test_runner_does_not_import_pseudolabel_mapping(self) -> None:
        import icl.runner.run_c_inference as mod
        source = Path(mod.__file__).read_text(encoding="utf-8")
        self.assertNotIn("pseudolabel_mapping", source)


@patch(
    "icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze",
    return_value={"c_predictions_manifest_verified": True, "c_records_sha256": "a" * 64, "record_count": 45},
)
@patch(
    "icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze",
    return_value={"evaluator_manifest_verified": True},
)
class TestEvaluateCPredictions(unittest.TestCase):
    """Integration tests for the full pipeline."""

    def test_full_pipeline_all_correct(self, mock_freeze, mock_pred_freeze) -> None:
        """C all correct + B all correct → delta = 0."""
        records = _all_correct_records()
        b_recs = _full_b_records(all_correct=True)
        result = evaluate_c_predictions(
            records,
            case_truth=_CLASS_ASSIGNMENT,
            agents_config=_AGENTS_CONFIG,
            b_records=b_recs,
            bootstrap_iterations=100,
            bootstrap_seed=42,
        )
        self.assertEqual(
            result["evaluation_status"],
            "OFFLINE_EVALUATION_CONDITION_C",
        )
        self.assertEqual(result["primary_unit"], "physical_case_id")
        self.assertEqual(result["abstain_treatment"], "incorrect")
        self.assertAlmostEqual(
            result["condition_c_metrics"]["overall"]["accuracy"], 1.0,
        )
        self.assertIn("delta_c_minus_b", result)
        self.assertAlmostEqual(
            result["delta_c_minus_b"]["delta_C_minus_B"], 0.0,
        )
        self.assertIn("bootstrap", result)

    def test_pipeline_c_better_than_b(self, mock_freeze, mock_pred_freeze) -> None:
        """C all correct, B all wrong → delta = 1.0."""
        records = _all_correct_records()
        b_recs = _full_b_records(all_correct=False)
        result = evaluate_c_predictions(
            records,
            case_truth=_CLASS_ASSIGNMENT,
            agents_config=_AGENTS_CONFIG,
            b_records=b_recs,
            bootstrap_iterations=100,
            bootstrap_seed=42,
        )
        self.assertAlmostEqual(
            result["delta_c_minus_b"]["delta_C_minus_B"], 1.0,
        )

    def test_pipeline_no_b_records(self, mock_freeze, mock_pred_freeze) -> None:
        """No B records → no delta or bootstrap in output."""
        records = _all_correct_records()
        result = evaluate_c_predictions(
            records,
            case_truth=_CLASS_ASSIGNMENT,
            agents_config=_AGENTS_CONFIG,
            b_records=[],
            bootstrap_iterations=100,
            bootstrap_seed=42,
        )
        self.assertIn("condition_c_metrics", result)
        self.assertNotIn("delta_c_minus_b", result)
        self.assertNotIn("bootstrap", result)

    def test_invalid_truth_labels_raises(self, mock_freeze, mock_pred_freeze) -> None:
        records = _all_correct_records()
        bad_truth = {cid: "INVALID_LABEL" for cid in _CASE_IDS}
        with self.assertRaises(ValueError) as ctx:
            evaluate_c_predictions(
                records,
                case_truth=bad_truth,
                agents_config=_AGENTS_CONFIG,
                b_records=[],
                bootstrap_iterations=10,
                bootstrap_seed=1,
            )
        self.assertIn("outside the label space", str(ctx.exception))

    def test_agents_config_validation_wrong_count(self, mock_freeze, mock_pred_freeze) -> None:
        """Not 4 agents → ValueError."""
        bad = {"agent_1": "CLS-ZOGAA", "agent_2": "CLS-OJNSG"}
        with self.assertRaises(ValueError) as ctx:
            evaluate_c_predictions(
                _all_correct_records(),
                case_truth=_CLASS_ASSIGNMENT,
                agents_config=bad,
                b_records=[],
            )
        self.assertIn("4 agents", str(ctx.exception))

    def test_agents_config_validation_duplicate_labels(self, mock_freeze, mock_pred_freeze) -> None:
        """Duplicate local_fault_labels → ValueError."""
        bad = {
            "agent_1": "CLS-ZOGAA", "agent_2": "CLS-ZOGAA",
            "agent_3": "CLS-R463B", "agent_4": "CLS-Z3ISU",
        }
        with self.assertRaises(ValueError) as ctx:
            evaluate_c_predictions(
                _all_correct_records(),
                case_truth=_CLASS_ASSIGNMENT,
                agents_config=bad,
                b_records=[],
            )
        self.assertIn("distinct", str(ctx.exception))


@patch(
    "icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze",
    return_value={"c_predictions_manifest_verified": True, "c_records_sha256": "a" * 64, "record_count": 45},
)
@patch(
    "icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze",
    return_value={"evaluator_manifest_verified": True},
)
class TestIntegrationWithAggregation(unittest.TestCase):
    """Verify aggregation + evaluation work together from raw CRunRecords."""

    def test_aggregation_feeds_evaluator(self, mock_freeze, mock_pred_freeze) -> None:
        records = _all_correct_records()
        b_recs = _full_b_records(all_correct=True)
        result = evaluate_c_predictions(
            records,
            case_truth=_CLASS_ASSIGNMENT,
            agents_config=_AGENTS_CONFIG,
            b_records=b_recs,
            bootstrap_iterations=50,
            bootstrap_seed=42,
        )
        metrics = result["condition_c_metrics"]
        self.assertEqual(metrics["overall"]["n"], 15)
        self.assertEqual(metrics["overall"]["correct"], 15)
        # accuracy_C_fault from metrics.
        self.assertEqual(metrics["accuracy_C_fault"]["n"], 12)


@patch(
    "icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze",
    return_value={"c_predictions_manifest_verified": True, "c_records_sha256": "a" * 64, "record_count": 45},
)
@patch(
    "icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze",
    return_value={"evaluator_manifest_verified": True},
)
class TestEndToEndEvaluatorSide(unittest.TestCase):
    """End-to-end test using real frozen manifests (read-only, evaluator side).

    This test validates against the actual project files to ensure the
    evaluator correctly reads phase_b heldout manifest and pseudolabel mapping
    without modification.  Skipped if the project files are not available.
    """

    def setUp(self) -> None:
        self.root = Path(__file__).resolve().parents[2]
        self.heldout_path = (
            self.root / "phase_b" / "heldout" / "phase_b_heldout_manifest.csv"
        )
        self.mapping_path = (
            self.root / "phase_b" / "config"
            / "evaluator_side" / "pseudolabel_mapping.json"
        )
        self.config_path = (
            self.root / "phase_b" / "config" / "protocol_config.json"
        )
        if not all(p.exists() for p in (
            self.heldout_path, self.mapping_path, self.config_path
        )):
            self.skipTest("project phase_b files not available")

    def test_load_case_truth_from_real_files(self, mock_freeze, mock_pred_freeze) -> None:
        """load_case_truth reads the real manifest and mapping correctly."""
        case_truth, integrity = load_case_truth(
            heldout_manifest_path=self.heldout_path,
            mapping_path=self.mapping_path,
        )
        self.assertEqual(len(case_truth), 15)
        # All 15 case IDs present.
        for i in range(1, 16):
            self.assertIn(f"PBH-{i:03d}", case_truth)
        # All pseudolabels are in the label space.
        for label in case_truth.values():
            self.assertIn(label, LABEL_SPACE)
        # Integrity info.
        self.assertEqual(integrity["physical_cases_mapped"], 15)
        self.assertTrue(integrity["unique_mapping"])
        self.assertEqual(integrity["fault_pseudoclass_count"], 4)

    def test_load_agents_config_from_real_file(self, mock_freeze, mock_pred_freeze) -> None:
        """load_agents_config returns 4 agents with distinct labels."""
        config = load_agents_config(self.config_path)
        self.assertEqual(len(config), 4)
        self.assertEqual(len(set(config.values())), 4)
        # All labels are fault pseudolabels (not Normal).
        for label in config.values():
            self.assertIn(label, LABEL_SPACE)
            self.assertNotEqual(label, "Normal")

    def test_full_pipeline_with_real_truth(self, mock_freeze, mock_pred_freeze) -> None:
        """Full pipeline using real truth, synthetic C records."""
        case_truth, _ = load_case_truth(
            heldout_manifest_path=self.heldout_path,
            mapping_path=self.mapping_path,
        )
        agents_config = load_agents_config(self.config_path)

        # Build synthetic all-correct C records from real truth.
        records = []
        seq = 0
        for cid in sorted(case_truth):
            truth = case_truth[cid]
            for rep in (1, 2, 3):
                records.append(
                    _make_c_record(cid, rep, truth, sequence_index=seq)
                )
                seq += 1

        result = evaluate_c_predictions(
            records,
            case_truth=case_truth,
            agents_config=agents_config,
            b_records=[],  # No delta without B records.
            bootstrap_iterations=50,
            bootstrap_seed=42,
        )
        self.assertAlmostEqual(
            result["condition_c_metrics"]["overall"]["accuracy"], 1.0,
        )
        self.assertEqual(
            result["condition_c_metrics"]["accuracy_C_fault"]["n"], 12,
        )
        self.assertEqual(
            result["condition_c_metrics"]["accuracy_C_normal"]["n"], 3,
        )



class TestVerifyCPredictionsFreeze(unittest.TestCase):
    """Tests for the predictions integrity barrier (P1-3)."""

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.records_path = self.tmpdir / "c_records.jsonl"
        self.manifest_path = self.tmpdir / "c_predictions_hash_manifest.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_records(self, n: int = 3) -> str:
        """Write n dummy record lines and return file SHA-256."""
        lines = []
        for i in range(n):
            rec = _make_c_record("PBH-001", repetition=(i % 3) + 1, sequence_index=i)
            lines.append(json.dumps(rec.to_dict(), ensure_ascii=False))
        self.records_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        import hashlib
        return hashlib.sha256(
            self.records_path.read_bytes()
        ).hexdigest()

    def _write_manifest(self, sha256: str, record_count: int | None = None) -> None:
        manifest = {"c_records_sha256": sha256}
        if record_count is not None:
            manifest["record_count"] = record_count
        self.manifest_path.write_text(
            json.dumps(manifest), encoding="utf-8"
        )

    def test_pass_hash_only(self) -> None:
        sha = self._write_records(3)
        self._write_manifest(sha)
        result = verify_c_predictions_freeze(
            c_records_path=self.records_path,
            manifest_path=self.manifest_path,
        )
        self.assertTrue(result["c_predictions_manifest_verified"])
        self.assertEqual(result["c_records_sha256"], sha)

    def test_pass_with_record_count(self) -> None:
        sha = self._write_records(3)
        self._write_manifest(sha, record_count=3)
        result = verify_c_predictions_freeze(
            c_records_path=self.records_path,
            manifest_path=self.manifest_path,
        )
        self.assertTrue(result["c_predictions_manifest_verified"])
        self.assertEqual(result["record_count"], 3)

    def test_hash_mismatch_raises(self) -> None:
        self._write_records(3)
        self._write_manifest("0" * 64)
        with self.assertRaises(RuntimeError) as ctx:
            verify_c_predictions_freeze(
                c_records_path=self.records_path,
                manifest_path=self.manifest_path,
            )
        self.assertIn("hash mismatch", str(ctx.exception))

    def test_record_count_mismatch_raises(self) -> None:
        sha = self._write_records(3)
        self._write_manifest(sha, record_count=99)
        with self.assertRaises(RuntimeError) as ctx:
            verify_c_predictions_freeze(
                c_records_path=self.records_path,
                manifest_path=self.manifest_path,
            )
        self.assertIn("record count mismatch", str(ctx.exception))

    def test_missing_records_file_raises(self) -> None:
        self._write_manifest("0" * 64)
        with self.assertRaises(FileNotFoundError):
            verify_c_predictions_freeze(
                c_records_path=self.tmpdir / "nonexistent.jsonl",
                manifest_path=self.manifest_path,
            )

    def test_missing_manifest_raises(self) -> None:
        self._write_records(3)
        with self.assertRaises(FileNotFoundError):
            verify_c_predictions_freeze(
                c_records_path=self.records_path,
                manifest_path=self.tmpdir / "nonexistent.json",
            )


class TestPipelineInvokesGuard(unittest.TestCase):
    """P1-5: evaluate_c_predictions must call verify_evaluator_freeze."""

    @patch("icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze",
           return_value={"c_predictions_manifest_verified": True, "c_records_sha256": "a" * 64, "record_count": 45})
    @patch("icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze")
    def test_guard_is_called(self, mock_guard, mock_pred_guard) -> None:
        mock_guard.return_value = {"evaluator_manifest_verified": True}
        records = _all_correct_records()
        evaluate_c_predictions(
            records,
            case_truth=_CLASS_ASSIGNMENT,
            agents_config=_AGENTS_CONFIG,
            b_records=[],
        )
        mock_guard.assert_called_once()

    @patch("icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze",
           return_value={"c_predictions_manifest_verified": True, "c_records_sha256": "a" * 64, "record_count": 45})
    @patch("icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze")
    def test_guard_failure_blocks_pipeline(self, mock_guard, mock_pred_guard) -> None:
        mock_guard.side_effect = RuntimeError("hash mismatch")
        records = _all_correct_records()
        with self.assertRaises(RuntimeError) as ctx:
            evaluate_c_predictions(
                records,
                case_truth=_CLASS_ASSIGNMENT,
                agents_config=_AGENTS_CONFIG,
                b_records=[],
            )
        self.assertIn("hash mismatch", str(ctx.exception))

    @patch("icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze",
           return_value={"c_predictions_manifest_verified": True, "c_records_sha256": "a" * 64, "record_count": 45})
    @patch("icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze")
    def test_guard_missing_manifest_blocks(self, mock_guard, mock_pred_guard) -> None:
        mock_guard.side_effect = FileNotFoundError("manifest not found")
        with self.assertRaises(FileNotFoundError):
            evaluate_c_predictions(
                _all_correct_records(),
                case_truth=_CLASS_ASSIGNMENT,
                agents_config=_AGENTS_CONFIG,
                b_records=[],
            )

    @patch("icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze",
           return_value={"c_predictions_manifest_verified": True, "c_records_sha256": "a" * 64, "record_count": 45})
    @patch("icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze")
    def test_custom_manifest_path_forwarded(self, mock_guard, mock_pred_guard) -> None:
        mock_guard.return_value = {"evaluator_manifest_verified": True}
        custom = Path("/tmp/custom_eval_manifest.json")
        evaluate_c_predictions(
            _all_correct_records(),
            case_truth=_CLASS_ASSIGNMENT,
            agents_config=_AGENTS_CONFIG,
            b_records=[],
            evaluator_manifest_path=custom,
        )
        call_kwargs = mock_guard.call_args
        self.assertEqual(call_kwargs[1]["manifest_path"], custom)



class TestPipelineInvokesPredictionsGuard(unittest.TestCase):
    """P1-3: evaluate_c_predictions must call verify_c_predictions_freeze."""

    @patch("icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze")
    @patch("icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze",
           return_value={"evaluator_manifest_verified": True})
    def test_predictions_guard_is_called(self, mock_eval_guard, mock_pred_guard) -> None:
        mock_pred_guard.return_value = {
            "c_predictions_manifest_verified": True,
            "c_records_sha256": "a" * 64, "record_count": 45,
        }
        evaluate_c_predictions(
            _all_correct_records(),
            case_truth=_CLASS_ASSIGNMENT,
            agents_config=_AGENTS_CONFIG,
            b_records=[],
        )
        mock_pred_guard.assert_called_once()

    @patch("icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze")
    @patch("icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze",
           return_value={"evaluator_manifest_verified": True})
    def test_predictions_guard_failure_blocks(self, mock_eval_guard, mock_pred_guard) -> None:
        mock_pred_guard.side_effect = RuntimeError("c_records hash mismatch")
        with self.assertRaises(RuntimeError) as ctx:
            evaluate_c_predictions(
                _all_correct_records(),
                case_truth=_CLASS_ASSIGNMENT,
                agents_config=_AGENTS_CONFIG,
                b_records=[],
            )
        self.assertIn("c_records hash mismatch", str(ctx.exception))

    @patch("icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze")
    @patch("icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze",
           return_value={"evaluator_manifest_verified": True})
    def test_predictions_guard_missing_manifest_blocks(self, mock_eval_guard, mock_pred_guard) -> None:
        mock_pred_guard.side_effect = FileNotFoundError("predictions manifest not found")
        with self.assertRaises(FileNotFoundError):
            evaluate_c_predictions(
                _all_correct_records(),
                case_truth=_CLASS_ASSIGNMENT,
                agents_config=_AGENTS_CONFIG,
                b_records=[],
            )

    @patch("icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze")
    @patch("icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze",
           return_value={"evaluator_manifest_verified": True})
    def test_custom_predictions_manifest_forwarded(self, mock_eval_guard, mock_pred_guard) -> None:
        mock_pred_guard.return_value = {
            "c_predictions_manifest_verified": True,
            "c_records_sha256": "a" * 64, "record_count": 45,
        }
        custom = Path("/tmp/custom_pred_manifest.json")
        evaluate_c_predictions(
            _all_correct_records(),
            case_truth=_CLASS_ASSIGNMENT,
            agents_config=_AGENTS_CONFIG,
            b_records=[],
            c_predictions_manifest_path=custom,
        )
        call_kwargs = mock_pred_guard.call_args
        self.assertEqual(call_kwargs[1]["manifest_path"], custom)

    @patch("icl.evaluation.evaluate_c_predictions.verify_c_predictions_freeze")
    @patch("icl.evaluation.evaluate_c_predictions.verify_evaluator_freeze",
           return_value={"evaluator_manifest_verified": True})
    def test_result_includes_predictions_integrity(self, mock_eval_guard, mock_pred_guard) -> None:
        pred_integrity = {
            "c_predictions_manifest_verified": True,
            "c_records_sha256": "a" * 64, "record_count": 45,
        }
        mock_pred_guard.return_value = pred_integrity
        result = evaluate_c_predictions(
            _all_correct_records(),
            case_truth=_CLASS_ASSIGNMENT,
            agents_config=_AGENTS_CONFIG,
            b_records=[],
        )
        self.assertIn("predictions_freeze_integrity", result)
        self.assertEqual(result["predictions_freeze_integrity"], pred_integrity)


if __name__ == "__main__":
    unittest.main()
