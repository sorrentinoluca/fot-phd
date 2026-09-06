"""Tests for icl.evaluation.aggregation_c — Condition C R=3 majority voting."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any

from icl.evaluation.aggregation_c import (
    CAggregatePrediction,
    aggregate_c_records,
    verify_aggregate_freeze,
    write_aggregate_manifest,
    write_c_aggregates,
    write_c_predictions_manifest,
)
from icl.runner.records_c import CRunRecord, LABEL_SPACE


# ------------------------------------------------------------------ helpers

_PROMPT_HASH = hashlib.sha256(b"test-prompt").hexdigest()


def _make_record(
    case_id: str = "PBH-001",
    repetition: int = 1,
    predicted_label: str | None = "Normal",
    abstain: bool = False,
    parse_failure: bool = False,
    prompt_sha256: str = _PROMPT_HASH,
    sequence_index: int | None = None,
) -> CRunRecord:
    """Build a minimal valid CRunRecord for testing."""
    if sequence_index is None:
        sequence_index = repetition - 1

    if parse_failure:
        parsed = {
            "predicted_label": None,
            "abstain": True,
            "used_insight_ids": [],
            "reasoning_summary": "parse_failure",
        }
    elif abstain:
        parsed = {
            "predicted_label": None,
            "abstain": True,
            "used_insight_ids": [],
            "reasoning_summary": "abstain_no_label",
        }
    else:
        parsed = {
            "predicted_label": predicted_label,
            "abstain": False,
            "used_insight_ids": ["INS-001"],
            "reasoning_summary": "some reasoning",
        }

    return CRunRecord(
        agent_id="central",
        condition="C",
        physical_case_id=case_id,
        repetition=repetition,
        sequence_index=sequence_index,
        parsed_output=parsed,
        valid=not parse_failure,
        prompt_sha256=prompt_sha256,
        raw_attempts=[{
            "attempt_index": 0,
            "raw_response": '{"predicted_label":"Normal"}',
            "parse_success": True,
            "error_type": None,
            "request_id": "req-1",
            "response_id": "resp-1",
            "token_usage": {
                "prompt_tokens": 1000,
                "completion_tokens": 50,
                "total_tokens": 1050,
            },
        }],
        retry_count=0,
        model_requested="gpt-5.6-terra",
        model_returned="gpt-5.6-terra",
        reasoning_effort="medium",
        timestamp_iso="2026-09-06T12:00:00+00:00",
        openai_sdk_version="3.6.0",
        stateless=True,
    )


def _triplet(
    case_id: str = "PBH-001",
    labels: tuple[str | None, str | None, str | None] = (
        "Normal", "Normal", "Normal"
    ),
    abstains: tuple[bool, bool, bool] = (False, False, False),
    parse_failures: tuple[bool, bool, bool] = (False, False, False),
    prompt_sha256: str = _PROMPT_HASH,
) -> list[CRunRecord]:
    """Build a (rep=1, rep=2, rep=3) triplet for a single case."""
    records = []
    for i in range(3):
        records.append(
            _make_record(
                case_id=case_id,
                repetition=i + 1,
                predicted_label=labels[i],
                abstain=abstains[i],
                parse_failure=parse_failures[i],
                prompt_sha256=prompt_sha256,
                sequence_index=i,
            )
        )
    return records


# ================================================================== tests


class TestCAggregatePrediction(unittest.TestCase):
    """Smoke tests for the dataclass itself."""

    def test_frozen(self) -> None:
        agg = CAggregatePrediction(
            agent_id="central",
            condition="C",
            physical_case_id="PBH-001",
            parsed_output={"predicted_label": "Normal", "abstain": False,
                           "used_insight_ids": [],
                           "reasoning_summary": "aggregate_majority_2_of_3"},
            repetition_outcomes=(),
        )
        with self.assertRaises(AttributeError):
            agg.agent_id = "other"  # type: ignore[misc]


class TestMajorityVoting(unittest.TestCase):
    """Core majority voting logic."""

    def test_unanimous(self) -> None:
        """3/3 same label → majority winner."""
        records = _triplet(labels=("CLS-ZOGAA", "CLS-ZOGAA", "CLS-ZOGAA"))
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertEqual(len(aggs), 1)
        self.assertEqual(aggs[0].parsed_output["predicted_label"], "CLS-ZOGAA")
        self.assertFalse(aggs[0].parsed_output["abstain"])
        self.assertEqual(
            aggs[0].parsed_output["reasoning_summary"],
            "aggregate_majority_2_of_3",
        )

    def test_two_of_three(self) -> None:
        """2/3 same label → majority winner."""
        records = _triplet(labels=("Normal", "CLS-OJNSG", "Normal"))
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertEqual(len(aggs), 1)
        self.assertEqual(aggs[0].parsed_output["predicted_label"], "Normal")
        self.assertFalse(aggs[0].parsed_output["abstain"])

    def test_no_majority_three_different(self) -> None:
        """3 different labels → no majority, abstain."""
        records = _triplet(
            labels=("CLS-ZOGAA", "CLS-OJNSG", "CLS-R463B"),
        )
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertEqual(len(aggs), 1)
        self.assertIsNone(aggs[0].parsed_output["predicted_label"])
        self.assertTrue(aggs[0].parsed_output["abstain"])
        self.assertEqual(
            aggs[0].parsed_output["reasoning_summary"],
            "aggregate_no_label_majority",
        )

    def test_all_abstain(self) -> None:
        """All 3 abstain → no majority, aggregate abstains."""
        records = _triplet(
            labels=(None, None, None),
            abstains=(True, True, True),
        )
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertEqual(len(aggs), 1)
        self.assertTrue(aggs[0].parsed_output["abstain"])
        self.assertIsNone(aggs[0].parsed_output["predicted_label"])

    def test_two_abstain_one_label(self) -> None:
        """2 abstain + 1 label → no majority (only 1 vote)."""
        records = _triplet(
            labels=(None, "Normal", None),
            abstains=(True, False, True),
        )
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertTrue(aggs[0].parsed_output["abstain"])

    def test_one_abstain_two_agree(self) -> None:
        """1 abstain + 2 same label → majority wins."""
        records = _triplet(
            labels=(None, "CLS-R463B", "CLS-R463B"),
            abstains=(True, False, False),
        )
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertEqual(
            aggs[0].parsed_output["predicted_label"], "CLS-R463B"
        )
        self.assertFalse(aggs[0].parsed_output["abstain"])

    def test_one_abstain_two_differ(self) -> None:
        """1 abstain + 2 different labels → no majority."""
        records = _triplet(
            labels=(None, "CLS-ZOGAA", "CLS-OJNSG"),
            abstains=(True, False, False),
        )
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertTrue(aggs[0].parsed_output["abstain"])


class TestParseFailure(unittest.TestCase):
    """Parse-failure handling in aggregation."""

    def test_one_parse_failure_two_agree(self) -> None:
        """1 parse failure + 2 agree → majority wins."""
        records = _triplet(
            labels=(None, "Normal", "Normal"),
            parse_failures=(True, False, False),
        )
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertEqual(aggs[0].parsed_output["predicted_label"], "Normal")

    def test_two_parse_failures(self) -> None:
        """2 parse failures + 1 label → no majority (single vote)."""
        records = _triplet(
            labels=(None, None, "CLS-Z3ISU"),
            parse_failures=(True, True, False),
        )
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertTrue(aggs[0].parsed_output["abstain"])

    def test_all_parse_failures(self) -> None:
        """3 parse failures → no votes, aggregate abstains."""
        records = _triplet(
            labels=(None, None, None),
            parse_failures=(True, True, True),
        )
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertTrue(aggs[0].parsed_output["abstain"])
        self.assertEqual(
            aggs[0].parsed_output["reasoning_summary"],
            "aggregate_no_label_majority",
        )


class TestRepetitionOutcomes(unittest.TestCase):
    """Verify per-repetition detail in repetition_outcomes."""

    def test_outcomes_structure(self) -> None:
        records = _triplet(labels=("Normal", "CLS-ZOGAA", "Normal"))
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        outcomes = aggs[0].repetition_outcomes
        self.assertEqual(len(outcomes), 3)
        for i, out in enumerate(outcomes):
            self.assertEqual(out["repetition"], i + 1)
            self.assertIn("predicted_label", out)
            self.assertIn("abstain", out)
            self.assertIn("parse_failure", out)

    def test_parse_failure_flagged(self) -> None:
        records = _triplet(
            labels=(None, "Normal", "Normal"),
            parse_failures=(True, False, False),
        )
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        outcomes = aggs[0].repetition_outcomes
        self.assertTrue(outcomes[0]["parse_failure"])
        self.assertFalse(outcomes[1]["parse_failure"])
        self.assertFalse(outcomes[2]["parse_failure"])

    def test_outcome_labels_match_input(self) -> None:
        labels = ("CLS-ZOGAA", "CLS-OJNSG", "CLS-ZOGAA")
        records = _triplet(labels=labels)
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        for i, out in enumerate(aggs[0].repetition_outcomes):
            self.assertEqual(out["predicted_label"], labels[i])
            self.assertFalse(out["abstain"])


class TestMultipleCases(unittest.TestCase):
    """Aggregation across multiple physical cases."""

    def test_two_cases_sorted(self) -> None:
        """Two cases → two aggregates, sorted by case_id."""
        hash_a = hashlib.sha256(b"prompt-a").hexdigest()
        hash_b = hashlib.sha256(b"prompt-b").hexdigest()
        records = (
            _triplet("PBH-004", ("CLS-ZOGAA",) * 3, prompt_sha256=hash_a)
            + _triplet("PBH-001", ("Normal",) * 3, prompt_sha256=hash_b)
        )
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001", "PBH-004"})
        self.assertEqual(len(aggs), 2)
        self.assertEqual(aggs[0].physical_case_id, "PBH-001")
        self.assertEqual(aggs[1].physical_case_id, "PBH-004")
        self.assertEqual(
            aggs[0].parsed_output["predicted_label"], "Normal"
        )
        self.assertEqual(
            aggs[1].parsed_output["predicted_label"], "CLS-ZOGAA"
        )

    def test_identity_fields(self) -> None:
        """agent_id and condition are always "central" / "C"."""
        records = _triplet()
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertEqual(aggs[0].agent_id, "central")
        self.assertEqual(aggs[0].condition, "C")


class TestValidationErrors(unittest.TestCase):
    """Error paths: missing repetitions, inconsistent hashes."""

    def test_missing_repetition(self) -> None:
        """Only 2 repetitions → ValueError."""
        records = [
            _make_record(repetition=1, sequence_index=0),
            _make_record(repetition=3, sequence_index=2),
        ]
        with self.assertRaises(ValueError) as ctx:
            aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertIn("[1, 2, 3]", str(ctx.exception))

    def test_duplicate_repetition(self) -> None:
        """Two records with same repetition → ValueError."""
        records = [
            _make_record(repetition=1, sequence_index=0),
            _make_record(repetition=1, sequence_index=1),
            _make_record(repetition=3, sequence_index=2),
        ]
        with self.assertRaises(ValueError) as ctx:
            aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertIn("[1, 2, 3]", str(ctx.exception))

    def test_inconsistent_prompt_sha256(self) -> None:
        """Different prompt hashes across repetitions → ValueError."""
        hash_a = hashlib.sha256(b"a").hexdigest()
        hash_b = hashlib.sha256(b"b").hexdigest()
        records = [
            _make_record(repetition=1, prompt_sha256=hash_a, sequence_index=0),
            _make_record(repetition=2, prompt_sha256=hash_b, sequence_index=1),
            _make_record(repetition=3, prompt_sha256=hash_a, sequence_index=2),
        ]
        with self.assertRaises(ValueError) as ctx:
            aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertIn("prompt_sha256", str(ctx.exception))

    def test_four_records_for_case(self) -> None:
        """Four records for one case → ValueError (not [1,2,3])."""
        records = [
            _make_record(repetition=r, sequence_index=r - 1)
            for r in [1, 2, 3, 3]
        ]
        with self.assertRaises(ValueError):
            aggregate_c_records(records, expected_case_ids={"PBH-001"})


class TestDictInput(unittest.TestCase):
    """Accept raw dicts as well as CRunRecord instances."""

    def test_from_dicts(self) -> None:
        records_as_dicts = [r.to_dict() for r in _triplet()]
        aggs = aggregate_c_records(records_as_dicts, expected_case_ids={"PBH-001"})
        self.assertEqual(len(aggs), 1)
        self.assertEqual(aggs[0].parsed_output["predicted_label"], "Normal")

    def test_mixed_input(self) -> None:
        """Mix of CRunRecord and dict is accepted."""
        triplet = _triplet()
        mixed: list[Any] = [triplet[0], triplet[1].to_dict(), triplet[2]]
        aggs = aggregate_c_records(mixed, expected_case_ids={"PBH-001"})
        self.assertEqual(len(aggs), 1)


class TestCustomLabelSpace(unittest.TestCase):
    """The label_space parameter filters valid votes."""

    def test_label_outside_space_ignored(self) -> None:
        """A label not in label_space is excluded from voting."""
        # Only "Normal" is in the custom space; CLS-ZOGAA votes discarded.
        records = _triplet(
            labels=("Normal", "CLS-ZOGAA", "CLS-ZOGAA"),
        )
        aggs = aggregate_c_records(records, label_space=["Normal"], expected_case_ids={"PBH-001"})
        # Only 1 vote for "Normal", 0 counted for CLS-ZOGAA → no majority.
        self.assertTrue(aggs[0].parsed_output["abstain"])

    def test_default_label_space(self) -> None:
        """Default label_space covers all five canonical labels."""
        for label in LABEL_SPACE:
            records = _triplet(labels=(label, label, label))
            aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
            self.assertEqual(
                aggs[0].parsed_output["predicted_label"], label
            )


class TestValidFlagExclusion(unittest.TestCase):
    """R5 review point 13: valid=False records excluded from voting."""

    def test_valid_false_excluded_from_majority(self) -> None:
        """valid=False record with a label is excluded from vote count."""
        # Rep 1: valid=True, CLS-ZOGAA
        # Rep 2: valid=False (parse_failure), but has label CLS-OJNSG in
        #        parsed_output — would normally count as a vote.
        # Rep 3: valid=True, CLS-ZOGAA
        #
        # Without the valid check, rep 2 would introduce a vote for CLS-OJNSG.
        # With the valid check, only reps 1 and 3 count → CLS-ZOGAA wins 2-of-3.
        r1 = _make_record(
            repetition=1, predicted_label="CLS-ZOGAA", sequence_index=0,
        )
        # Manually build a record where valid=False but parsed_output has a label.
        r2 = CRunRecord(
            agent_id="central", condition="C",
            physical_case_id="PBH-001", repetition=2, sequence_index=1,
            parsed_output={
                "predicted_label": None, "abstain": True,
                "used_insight_ids": [],
                "reasoning_summary": "parse_failure",
            },
            valid=False,
            prompt_sha256=_PROMPT_HASH,
            raw_attempts=[{
                "attempt_index": 0, "raw_response": "{}",
                "parse_success": False, "error_type": "parse",
                "request_id": "r1", "response_id": "r1",
                "token_usage": {
                    "prompt_tokens": 1000,
                    "completion_tokens": 50,
                    "total_tokens": 1050,
                },
            }],
            retry_count=0,
            model_requested="gpt-5.6-terra",
            model_returned="gpt-5.6-terra",
            reasoning_effort="medium",
            timestamp_iso="2026-09-06T12:00:00+00:00",
            openai_sdk_version="3.6.0",
            stateless=True,
        )
        r3 = _make_record(
            repetition=3, predicted_label="CLS-ZOGAA", sequence_index=2,
        )

        aggs = aggregate_c_records([r1, r2, r3], expected_case_ids={"PBH-001"})
        self.assertEqual(len(aggs), 1)
        # CLS-ZOGAA has 2 valid votes → majority.
        self.assertEqual(aggs[0].parsed_output["predicted_label"], "CLS-ZOGAA")
        self.assertFalse(aggs[0].parsed_output["abstain"])

    def test_two_valid_false_one_valid_no_majority(self) -> None:
        """2 valid=False + 1 valid → only 1 vote, no majority."""
        r1 = _make_record(
            repetition=1, predicted_label="CLS-ZOGAA", sequence_index=0,
        )
        r2 = CRunRecord(
            agent_id="central", condition="C",
            physical_case_id="PBH-001", repetition=2, sequence_index=1,
            parsed_output={
                "predicted_label": None, "abstain": True,
                "used_insight_ids": [],
                "reasoning_summary": "parse_failure",
            },
            valid=False,
            prompt_sha256=_PROMPT_HASH,
            raw_attempts=[{
                "attempt_index": 0, "raw_response": "{}",
                "parse_success": False, "error_type": "parse",
                "request_id": "r1", "response_id": "r1",
                "token_usage": {
                    "prompt_tokens": 1000,
                    "completion_tokens": 50,
                    "total_tokens": 1050,
                },
            }],
            retry_count=0,
            model_requested="gpt-5.6-terra",
            model_returned="gpt-5.6-terra",
            reasoning_effort="medium",
            timestamp_iso="2026-09-06T12:00:00+00:00",
            openai_sdk_version="3.6.0",
            stateless=True,
        )
        r3 = CRunRecord(
            agent_id="central", condition="C",
            physical_case_id="PBH-001", repetition=3, sequence_index=2,
            parsed_output={
                "predicted_label": None, "abstain": True,
                "used_insight_ids": [],
                "reasoning_summary": "parse_failure",
            },
            valid=False,
            prompt_sha256=_PROMPT_HASH,
            raw_attempts=[{
                "attempt_index": 0, "raw_response": "{}",
                "parse_success": False, "error_type": "parse",
                "request_id": "r1", "response_id": "r1",
                "token_usage": {
                    "prompt_tokens": 1000,
                    "completion_tokens": 50,
                    "total_tokens": 1050,
                },
            }],
            retry_count=0,
            model_requested="gpt-5.6-terra",
            model_returned="gpt-5.6-terra",
            reasoning_effort="medium",
            timestamp_iso="2026-09-06T12:00:00+00:00",
            openai_sdk_version="3.6.0",
            stateless=True,
        )

        aggs = aggregate_c_records([r1, r2, r3], expected_case_ids={"PBH-001"})
        self.assertEqual(len(aggs), 1)
        # Only 1 valid vote — no majority → abstain.
        self.assertTrue(aggs[0].parsed_output["abstain"])


class TestOutputContract(unittest.TestCase):
    """Verify the parsed_output contract matches CRunRecord's structure."""

    def test_majority_keys(self) -> None:
        records = _triplet()
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        keys = set(aggs[0].parsed_output)
        self.assertEqual(
            keys,
            {"predicted_label", "abstain", "used_insight_ids", "reasoning_summary"},
        )

    def test_no_majority_keys(self) -> None:
        records = _triplet(labels=("CLS-ZOGAA", "CLS-OJNSG", "CLS-R463B"))
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        keys = set(aggs[0].parsed_output)
        self.assertEqual(
            keys,
            {"predicted_label", "abstain", "used_insight_ids", "reasoning_summary"},
        )

    def test_used_insight_ids_empty_in_aggregate(self) -> None:
        """Aggregate always has empty used_insight_ids."""
        records = _triplet()
        aggs = aggregate_c_records(records, expected_case_ids={"PBH-001"})
        self.assertEqual(aggs[0].parsed_output["used_insight_ids"], [])

    def test_empty_input(self) -> None:
        """No records → empty list (not an error)."""
        aggs = aggregate_c_records([], expected_case_ids=set())
        self.assertEqual(aggs, [])


class TestExpectedCaseIds(unittest.TestCase):
    """P1-3: aggregate completeness validation via expected_case_ids."""

    def test_matching_ids_passes(self) -> None:
        """When expected matches actual, no error."""
        records = _triplet("PBH-001") + _triplet("PBH-002",
            labels=("CLS-ZOGAA", "CLS-ZOGAA", "CLS-ZOGAA"),
            prompt_sha256=hashlib.sha256(b"prompt-b").hexdigest())
        aggs = aggregate_c_records(
            records, expected_case_ids={"PBH-001", "PBH-002"},
        )
        self.assertEqual(len(aggs), 2)

    def test_missing_case_raises(self) -> None:
        """Expected has a case not in records → ValueError."""
        records = _triplet("PBH-001")
        with self.assertRaises(ValueError) as ctx:
            aggregate_c_records(
                records, expected_case_ids={"PBH-001", "PBH-002"},
            )
        self.assertIn("missing", str(ctx.exception))
        self.assertIn("PBH-002", str(ctx.exception))

    def test_extra_case_raises(self) -> None:
        """Records have a case not in expected → ValueError."""
        records = _triplet("PBH-001") + _triplet("PBH-002",
            labels=("CLS-ZOGAA", "CLS-ZOGAA", "CLS-ZOGAA"),
            prompt_sha256=hashlib.sha256(b"prompt-b").hexdigest())
        with self.assertRaises(ValueError) as ctx:
            aggregate_c_records(
                records, expected_case_ids={"PBH-001"},
            )
        self.assertIn("extra", str(ctx.exception))
        self.assertIn("PBH-002", str(ctx.exception))

    def test_empty_expected_empty_records(self) -> None:
        """Both empty → no error, empty result."""
        aggs = aggregate_c_records([], expected_case_ids=set())
        self.assertEqual(aggs, [])

    def test_empty_expected_nonempty_records_raises(self) -> None:
        """Records present but expected is empty → ValueError."""
        records = _triplet("PBH-001")
        with self.assertRaises(ValueError) as ctx:
            aggregate_c_records(records, expected_case_ids=set())
        self.assertIn("extra", str(ctx.exception))


# ================================================================== R8 tests


# 15 canonical case IDs.
_CASE_IDS = [f"PBH-{i:03d}" for i in range(1, 16)]


def _outcome_to_crunrecord_dict(
    case_id: str,
    outcome: dict[str, Any],
    seq_index: int,
) -> dict[str, Any]:
    """Create a full CRunRecord-compliant dict from an aggregate outcome.

    R10: raw records must survive ``CRunRecord.from_jsonl_line()`` so that
    integral recomputation in ``verify_aggregate_freeze`` works.
    """
    abstain = bool(outcome.get("abstain", False))
    label = None if abstain else outcome["predicted_label"]
    parse_failure = outcome.get("parse_failure", False)
    valid = not parse_failure and (not abstain or True)
    # CRunRecord validation: valid=True requires parse_success=True
    # and error_type=None.  For parse failures: valid=False,
    # parse_success=False, error_type="parse".
    if parse_failure:
        valid = False
        parse_success = False
        error_type: str | None = "parse"
        # parse_failure records are abstain=True, label=None
        abstain = True
        label = None
        reasoning = "parse_failure"
    else:
        valid = True
        parse_success = True
        error_type = None
        reasoning = "test_stub"
    return {
        "agent_id": "central",
        "condition": "C",
        "physical_case_id": case_id,
        "repetition": outcome["repetition"],
        "sequence_index": seq_index,
        "parsed_output": {
            "predicted_label": label,
            "abstain": abstain,
            "used_insight_ids": [],
            "reasoning_summary": reasoning,
        },
        "valid": valid,
        "prompt_sha256": "a" * 64,
        "raw_attempts": [{
            "attempt_index": 0,
            "raw_response": "test",
            "parse_success": parse_success,
            "error_type": error_type,
            "request_id": "req_test",
            "response_id": "resp_test",
            "token_usage": {
                "prompt_tokens": 100,
                "completion_tokens": 50,
                "total_tokens": 150,
            },
        }],
        "retry_count": 0,
        "model_requested": "gpt-5.6-terra",
        "model_returned": "gpt-5.6-terra",
        "reasoning_effort": "high",
        "timestamp_iso": "2026-09-06T00:00:00+00:00",
        "openai_sdk_version": "3.6.0",
        "stateless": True,
        "network_retries": [],
    }


def _make_raw_records_jsonl(
    aggs: list[CAggregatePrediction] | None = None,
) -> str:
    """Build JSONL content for c_records.jsonl matching aggregates' outcomes.

    Each aggregate's repetition_outcomes are expanded into one full
    CRunRecord per repetition.  R10: records must pass
    ``CRunRecord.from_jsonl_line()`` for integral recomputation.
    """
    if aggs is None:
        aggs = _make_standard_aggregates()
    lines: list[str] = []
    seq = 0
    for agg in aggs:
        for outcome in agg.repetition_outcomes:
            raw = _outcome_to_crunrecord_dict(
                agg.physical_case_id, outcome, seq,
            )
            lines.append(json.dumps(raw, separators=(",", ":")))
            seq += 1
    return "\n".join(lines) + "\n"


def _make_standard_aggregates() -> list[CAggregatePrediction]:
    """Build 15 CAggregatePrediction objects, one per case."""
    aggs = []
    for cid in sorted(_CASE_IDS):
        aggs.append(CAggregatePrediction(
            agent_id="central",
            condition="C",
            physical_case_id=cid,
            parsed_output={
                "predicted_label": "Normal",
                "abstain": False,
                "used_insight_ids": [],
                "reasoning_summary": "aggregate_majority_2_of_3",
            },
            repetition_outcomes=(
                {"repetition": 1, "predicted_label": "Normal",
                 "abstain": False, "parse_failure": False},
                {"repetition": 2, "predicted_label": "Normal",
                 "abstain": False, "parse_failure": False},
                {"repetition": 3, "predicted_label": "Normal",
                 "abstain": False, "parse_failure": False},
            ),
            aggregation_rule="majority_2_of_3",
        ))
    return aggs


class TestWriteCPredictionsManifest(unittest.TestCase):
    """R8: write_c_predictions_manifest writer."""

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.manifest_path = self.tmpdir / "c_predictions_manifest.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_roundtrip_structure(self) -> None:
        """Written manifest contains the three required keys."""
        write_c_predictions_manifest(
            c_records_sha256="a" * 64,
            record_count=45,
            schedule_sha256="b" * 64,
            manifest_path=self.manifest_path,
        )
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(manifest["c_records_sha256"], "a" * 64)
        self.assertEqual(manifest["record_count"], 45)
        self.assertIn("schedule_reference", manifest)
        self.assertEqual(manifest["schedule_reference"]["sha256"], "b" * 64)
        self.assertEqual(
            manifest["schedule_reference"]["path"],
            "icl/full_evaluation/c_schedule.json",
        )

    def test_custom_schedule_ref_path(self) -> None:
        write_c_predictions_manifest(
            c_records_sha256="c" * 64,
            record_count=15,
            schedule_sha256="d" * 64,
            manifest_path=self.manifest_path,
            schedule_ref_path="custom/path.json",
        )
        manifest = json.loads(self.manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(
            manifest["schedule_reference"]["path"],
            "custom/path.json",
        )


class TestVerifyAggregateFreezeR8(unittest.TestCase):
    """R8: hardened verify_aggregate_freeze with 10 checks."""

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.agg_path = self.tmpdir / "c_aggregate_records.jsonl"
        self.manifest_path = self.tmpdir / "c_aggregate_manifest.json"
        self.c_records_path = self.tmpdir / "c_records.jsonl"
        self.schedule_path = self.tmpdir / "c_schedule.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write_cross_verify_files(
        self,
        aggs: list[CAggregatePrediction] | None = None,
    ) -> tuple[str, str]:
        """Write c_records.jsonl and c_schedule.json, return their SHA-256.

        R9: raw records now match the aggregate repetition_outcomes so that
        check 11 (cross-verify against raw records) passes on the happy path.
        """
        c_content = _make_raw_records_jsonl(aggs)
        self.c_records_path.write_text(c_content, encoding="utf-8")
        c_sha = hashlib.sha256(self.c_records_path.read_bytes()).hexdigest()

        s_content = '[{"dummy":"schedule"}]'
        self.schedule_path.write_text(s_content, encoding="utf-8")
        s_sha = hashlib.sha256(self.schedule_path.read_bytes()).hexdigest()

        return c_sha, s_sha

    def _write_good_setup(self) -> tuple[str, str, str]:
        """Write aggregates + manifest + cross-verify files. Returns (agg_sha, c_sha, s_sha)."""
        c_sha, s_sha = self._write_cross_verify_files()
        aggs = _make_standard_aggregates()
        agg_sha = write_c_aggregates(aggs, output_path=self.agg_path)
        write_aggregate_manifest(
            aggregate_sha256=agg_sha,
            record_count=len(aggs),
            c_records_sha256=c_sha,
            schedule_sha256=s_sha,
            manifest_path=self.manifest_path,
        )
        return agg_sha, c_sha, s_sha

    def test_happy_path(self) -> None:
        """Full 10-check verification passes."""
        self._write_good_setup()
        result = verify_aggregate_freeze(
            aggregate_path=self.agg_path,
            manifest_path=self.manifest_path,
            c_records_path=self.c_records_path,
            schedule_path=self.schedule_path,
        )
        self.assertTrue(result["c_aggregate_manifest_verified"])
        self.assertEqual(result["record_count"], 15)

    def test_missing_status_key_raises(self) -> None:
        """Check 1: missing 'status' key → RuntimeError."""
        c_sha, s_sha = self._write_cross_verify_files()
        aggs = _make_standard_aggregates()
        agg_sha = write_c_aggregates(aggs, output_path=self.agg_path)
        # Write manifest manually without status.
        manifest = {
            "c_aggregate_records_sha256": agg_sha,
            "record_count": 15,
            "aggregation_rule": "majority_2_of_3",
            "source_c_records_sha256": c_sha,
            "schedule_reference": {"path": "x", "sha256": s_sha},
        }
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        self.assertIn("missing required keys", str(ctx.exception))

    def test_wrong_status_raises(self) -> None:
        """Check 2: status != IMMUTABLE_BEFORE_EVALUATION → RuntimeError."""
        c_sha, s_sha = self._write_cross_verify_files()
        aggs = _make_standard_aggregates()
        agg_sha = write_c_aggregates(aggs, output_path=self.agg_path)
        manifest = {
            "c_aggregate_records_sha256": agg_sha,
            "record_count": 15,
            "aggregation_rule": "majority_2_of_3",
            "source_c_records_sha256": c_sha,
            "schedule_reference": {"path": "x", "sha256": s_sha},
            "status": "MUTABLE",
        }
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        self.assertIn("IMMUTABLE_BEFORE_EVALUATION", str(ctx.exception))

    def test_source_c_records_sha_mismatch_raises(self) -> None:
        """Check 9: source_c_records_sha256 doesn't match actual → RuntimeError."""
        c_sha, s_sha = self._write_cross_verify_files()
        aggs = _make_standard_aggregates()
        agg_sha = write_c_aggregates(aggs, output_path=self.agg_path)
        write_aggregate_manifest(
            aggregate_sha256=agg_sha,
            record_count=len(aggs),
            c_records_sha256="0" * 64,  # wrong c_records hash
            schedule_sha256=s_sha,
            manifest_path=self.manifest_path,
        )
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        self.assertIn("source_c_records_sha256 mismatch", str(ctx.exception))

    def test_schedule_sha_mismatch_raises(self) -> None:
        """Check 10: schedule_reference.sha256 doesn't match actual → RuntimeError."""
        c_sha, s_sha = self._write_cross_verify_files()
        aggs = _make_standard_aggregates()
        agg_sha = write_c_aggregates(aggs, output_path=self.agg_path)
        write_aggregate_manifest(
            aggregate_sha256=agg_sha,
            record_count=len(aggs),
            c_records_sha256=c_sha,
            schedule_sha256="0" * 64,  # wrong schedule hash
            manifest_path=self.manifest_path,
        )
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        self.assertIn("schedule_reference.sha256 mismatch", str(ctx.exception))

    def test_wrong_aggregation_rule_raises(self) -> None:
        """Check 8: aggregation_rule != majority_2_of_3 → RuntimeError."""
        c_sha, s_sha = self._write_cross_verify_files()
        aggs = _make_standard_aggregates()
        agg_sha = write_c_aggregates(aggs, output_path=self.agg_path)
        manifest = {
            "c_aggregate_records_sha256": agg_sha,
            "record_count": 15,
            "aggregation_rule": "simple_majority",
            "source_c_records_sha256": c_sha,
            "schedule_reference": {"path": "x", "sha256": s_sha},
            "status": "IMMUTABLE_BEFORE_EVALUATION",
        }
        self.manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        self.assertIn("aggregation_rule", str(ctx.exception))

    def test_wrong_record_count_raises(self) -> None:
        """Check 4: record_count mismatch in manifest → RuntimeError."""
        c_sha, s_sha = self._write_cross_verify_files()
        aggs = _make_standard_aggregates()
        agg_sha = write_c_aggregates(aggs, output_path=self.agg_path)
        write_aggregate_manifest(
            aggregate_sha256=agg_sha,
            record_count=10,  # wrong count
            c_records_sha256=c_sha,
            schedule_sha256=s_sha,
            manifest_path=self.manifest_path,
        )
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        err = str(ctx.exception)
        self.assertTrue(
            "record count" in err.lower(),
            f"unexpected error: {err}",
        )


class TestVerifyAggregateFreezeR10(unittest.TestCase):
    """R10: integral recomputation cross-verification in verify_aggregate_freeze.

    Raw records are loaded via CRunRecord.from_jsonl_line(), recomputed
    via aggregate_c_records(), and the result is compared integrally
    against the frozen aggregate file.  Any semantic drift — agent_id,
    condition, label, abstain, repetition number — is caught.
    """

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.agg_path = self.tmpdir / "c_aggregate_records.jsonl"
        self.manifest_path = self.tmpdir / "c_aggregate_manifest.json"
        self.c_records_path = self.tmpdir / "c_records.jsonl"
        self.schedule_path = self.tmpdir / "c_schedule.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    # ---- helpers ----

    def _write_schedule(self) -> str:
        s_content = '[{"dummy":"schedule"}]'
        self.schedule_path.write_text(s_content, encoding="utf-8")
        return hashlib.sha256(self.schedule_path.read_bytes()).hexdigest()

    def _write_setup_from_dicts(
        self,
        agg_dicts: list[dict[str, Any]],
        *,
        raw_records_content: str | None = None,
    ) -> tuple[str, str, str]:
        """Write aggregates (from raw dicts), manifest, schedule, raw records.

        If *raw_records_content* is not None it is used verbatim for
        ``c_records.jsonl``; otherwise matching raw records are derived
        from *agg_dicts*' repetition_outcomes as full CRunRecords.

        Returns ``(agg_sha, c_sha, s_sha)``.
        """
        s_sha = self._write_schedule()

        # --- raw records (full CRunRecord-compliant) ---
        if raw_records_content is None:
            raw_lines: list[str] = []
            seq = 0
            for d in agg_dicts:
                for outcome in d["repetition_outcomes"]:
                    raw = _outcome_to_crunrecord_dict(
                        d["physical_case_id"], outcome, seq,
                    )
                    raw_lines.append(json.dumps(raw, separators=(",", ":")))
                    seq += 1
            raw_content = "\n".join(raw_lines) + "\n"
        else:
            raw_content = raw_records_content

        self.c_records_path.write_text(raw_content, encoding="utf-8")
        c_sha = hashlib.sha256(self.c_records_path.read_bytes()).hexdigest()

        # --- aggregate JSONL ---
        agg_content = "\n".join(
            json.dumps(d, ensure_ascii=False, separators=(",", ":"))
            for d in agg_dicts
        ) + "\n"
        self.agg_path.write_text(agg_content, encoding="utf-8")
        agg_sha = hashlib.sha256(self.agg_path.read_bytes()).hexdigest()

        # --- manifest ---
        write_aggregate_manifest(
            aggregate_sha256=agg_sha,
            record_count=len(agg_dicts),
            c_records_sha256=c_sha,
            schedule_sha256=s_sha,
            manifest_path=self.manifest_path,
        )
        return agg_sha, c_sha, s_sha

    def _standard_agg_dicts(self) -> list[dict[str, Any]]:
        return [agg.to_dict() for agg in _make_standard_aggregates()]

    # ---- tests ----

    def test_wrong_agent_id_rejected(self) -> None:
        """R10: agent_id='rogue_agent' in frozen → differs from recomputation."""
        dicts = self._standard_agg_dicts()
        dicts[5]["agent_id"] = "rogue_agent"
        self._write_setup_from_dicts(dicts)
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        err = str(ctx.exception)
        self.assertIn("R10 recomputation", err)
        self.assertIn("agent_id", err)

    def test_wrong_condition_rejected(self) -> None:
        """R10: condition='B' in frozen → differs from recomputation."""
        dicts = self._standard_agg_dicts()
        dicts[3]["condition"] = "B"
        self._write_setup_from_dicts(dicts)
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        err = str(ctx.exception)
        self.assertIn("R10 recomputation", err)
        self.assertIn("condition", err)

    def test_majority_label_inconsistency_rejected(self) -> None:
        """R10: parsed_output.predicted_label tampered → recomputation mismatch."""
        dicts = self._standard_agg_dicts()
        # All 3 outcomes say "Normal" but parsed_output says "CLS-ZOGAA".
        dicts[7]["parsed_output"]["predicted_label"] = "CLS-ZOGAA"
        self._write_setup_from_dicts(dicts)
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        err = str(ctx.exception)
        self.assertIn("R10 recomputation", err)
        self.assertIn("parsed_output", err)

    def test_no_majority_without_abstain_rejected(self) -> None:
        """R10: 3 different labels but abstain=False → recomputation says abstain=True."""
        dicts = self._standard_agg_dicts()
        # Make all 3 outcomes different labels — no majority possible.
        dicts[0]["repetition_outcomes"][0]["predicted_label"] = "Normal"
        dicts[0]["repetition_outcomes"][1]["predicted_label"] = "CLS-ZOGAA"
        dicts[0]["repetition_outcomes"][2]["predicted_label"] = "CLS-OJNSG"
        # Keep parsed_output claiming a definite prediction (not abstain).
        dicts[0]["parsed_output"]["abstain"] = False
        self._write_setup_from_dicts(dicts)
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        err = str(ctx.exception)
        self.assertIn("R10 recomputation", err)

    def test_raw_label_mismatch_rejected(self) -> None:
        """R10: raw c_records differ from frozen outcomes → recomputation mismatch."""
        dicts = self._standard_agg_dicts()

        # Build raw records that differ from the aggregates on one case.
        raw_lines: list[str] = []
        seq = 0
        for d in dicts:
            for outcome in d["repetition_outcomes"]:
                out = dict(outcome)
                # Tamper: PBH-001, rep 1 → different label in raw records.
                if d["physical_case_id"] == "PBH-001" and out["repetition"] == 1:
                    out["predicted_label"] = "CLS-ZOGAA"
                raw = _outcome_to_crunrecord_dict(
                    d["physical_case_id"], out, seq,
                )
                raw_lines.append(json.dumps(raw, separators=(",", ":")))
                seq += 1
        tampered_raw = "\n".join(raw_lines) + "\n"

        self._write_setup_from_dicts(dicts, raw_records_content=tampered_raw)
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        err = str(ctx.exception)
        self.assertIn("R10 recomputation", err)
        self.assertIn("PBH-001", err)

    def test_repetition_number_mismatch_rejected(self) -> None:
        """R10: frozen repetition_outcomes has repetition=99 → recomputation mismatch."""
        dicts = self._standard_agg_dicts()
        # Tamper frozen aggregate: change repetition number in outcome.
        dicts[2]["repetition_outcomes"][0]["repetition"] = 99
        self._write_setup_from_dicts(dicts)
        with self.assertRaises((RuntimeError, ValueError)) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        # May fail during recomputation (invalid repetitions) or during
        # the integral comparison.
        err = str(ctx.exception)
        self.assertTrue(
            "repetition" in err.lower() or "R10 recomputation" in err,
            f"unexpected error: {err}",
        )

    def test_abstain_per_rep_mismatch_rejected(self) -> None:
        """R10: frozen outcome claims abstain=True but raw record has abstain=False."""
        dicts = self._standard_agg_dicts()
        # Tamper frozen aggregate: mark rep 1 as abstain in outcomes.
        dicts[4]["repetition_outcomes"][0]["abstain"] = True
        dicts[4]["repetition_outcomes"][0]["predicted_label"] = None
        # Raw records are derived from the UNTAMPERED outcomes (all Normal).
        # But _write_setup_from_dicts derives raw from tampered dicts,
        # so we override raw_records_content to use the correct ones.
        correct_dicts = self._standard_agg_dicts()
        raw_lines: list[str] = []
        seq = 0
        for d in correct_dicts:
            for outcome in d["repetition_outcomes"]:
                raw = _outcome_to_crunrecord_dict(
                    d["physical_case_id"], outcome, seq,
                )
                raw_lines.append(json.dumps(raw, separators=(",", ":")))
                seq += 1
        correct_raw = "\n".join(raw_lines) + "\n"

        self._write_setup_from_dicts(dicts, raw_records_content=correct_raw)
        with self.assertRaises(RuntimeError) as ctx:
            verify_aggregate_freeze(
                aggregate_path=self.agg_path,
                manifest_path=self.manifest_path,
                c_records_path=self.c_records_path,
                schedule_path=self.schedule_path,
            )
        err = str(ctx.exception)
        self.assertIn("R10 recomputation", err)


if __name__ == "__main__":
    unittest.main()
