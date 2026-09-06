"""Tests for icl.evaluation.aggregation_c — Condition C R=3 majority voting."""

from __future__ import annotations

import hashlib
import unittest
from typing import Any

from icl.evaluation.aggregation_c import (
    CAggregatePrediction,
    aggregate_c_records,
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


if __name__ == "__main__":
    unittest.main()
