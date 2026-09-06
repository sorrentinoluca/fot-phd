"""Unit tests for CRunRecord and its JSON Schema."""

from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path

from icl.runner.records_c import CRunRecord, VALID_INSIGHT_IDS


ROOT = Path(__file__).resolve().parents[2]


def _valid_attempt(index: int = 0) -> dict:
    return {
        "attempt_index": index,
        "raw_response": '{"predicted_label":"CLS-ZOGAA","abstain":false,"used_insight_ids":["INS-001"],"reasoning_summary":"test"}',
        "parse_success": True,
        "error_type": None,
        "request_id": "req-abc123",
        "response_id": "resp-xyz789",
        "token_usage": {
            "prompt_tokens": 1000,
            "completion_tokens": 50,
            "total_tokens": 1050,
        },
    }


def _valid_record_dict(**overrides) -> dict:
    base = {
        "agent_id": "central",
        "condition": "C",
        "physical_case_id": "PBH-001",
        "repetition": 1,
        "sequence_index": 0,
        "parsed_output": {
            "predicted_label": "CLS-ZOGAA",
            "abstain": False,
            "used_insight_ids": ["INS-001"],
            "reasoning_summary": "Synthetic test output.",
        },
        "valid": True,
        "prompt_sha256": "a" * 64,
        "raw_attempts": [_valid_attempt(0)],
        "retry_count": 0,
        "model_requested": "gpt-5.6-terra",
        "model_returned": "gpt-5.6-terra",
        "reasoning_effort": "medium",
        "timestamp_iso": "2026-09-06T12:00:00+00:00",
        "openai_sdk_version": "3.6.0",
        "stateless": True,
    }
    base.update(overrides)
    return base


class TestCRunRecordValid(unittest.TestCase):
    def test_valid_record_roundtrip(self) -> None:
        d = _valid_record_dict()
        record = CRunRecord.from_dict(d)
        self.assertEqual(record.agent_id, "central")
        self.assertEqual(record.condition, "C")
        result = record.to_dict()
        self.assertEqual(result["agent_id"], "central")
        self.assertEqual(result["condition"], "C")

    def test_jsonl_roundtrip(self) -> None:
        d = _valid_record_dict()
        record = CRunRecord.from_dict(d)
        line = record.to_jsonl_line()
        restored = CRunRecord.from_jsonl_line(line)
        self.assertEqual(record.to_dict(), restored.to_dict())

    def test_abstention(self) -> None:
        d = _valid_record_dict(
            parsed_output={
                "predicted_label": None,
                "abstain": True,
                "used_insight_ids": [],
                "reasoning_summary": "parse_failure",
            },
            valid=False,
        )
        record = CRunRecord.from_dict(d)
        self.assertTrue(record.parsed_output["abstain"])

    def test_multiple_attempts_with_retry(self) -> None:
        attempts = [
            {**_valid_attempt(0), "parse_success": False, "error_type": "parse"},
            _valid_attempt(1),
        ]
        d = _valid_record_dict(raw_attempts=attempts, retry_count=1)
        record = CRunRecord.from_dict(d)
        self.assertEqual(len(record.raw_attempts), 2)
        self.assertEqual(record.retry_count, 1)


class TestCRunRecordRejections(unittest.TestCase):
    def test_reject_agent_id_not_central(self) -> None:
        for bad in ("agent_1", "agent_2", "pooled", ""):
            with self.assertRaises(ValueError, msg=f"should reject agent_id={bad!r}"):
                CRunRecord.from_dict(_valid_record_dict(agent_id=bad))

    def test_reject_condition_not_C(self) -> None:
        for bad in ("A", "B", "E", "D"):
            with self.assertRaises(ValueError, msg=f"should reject condition={bad!r}"):
                CRunRecord.from_dict(_valid_record_dict(condition=bad))

    def test_reject_bad_case_id(self) -> None:
        for bad in ("PBH-0001", "PBH-AB1", "PHY-001", ""):
            with self.assertRaises(ValueError):
                CRunRecord.from_dict(_valid_record_dict(physical_case_id=bad))

    def test_reject_bad_repetition(self) -> None:
        for bad in (0, 4, -1):
            with self.assertRaises(ValueError):
                CRunRecord.from_dict(_valid_record_dict(repetition=bad))

    def test_reject_bad_sequence_index(self) -> None:
        for bad in (-1, 45, 100):
            with self.assertRaises(ValueError):
                CRunRecord.from_dict(_valid_record_dict(sequence_index=bad))

    def test_reject_bad_prompt_hash(self) -> None:
        with self.assertRaises(ValueError):
            CRunRecord.from_dict(_valid_record_dict(prompt_sha256="not-a-hash"))

    def test_reject_stateless_false(self) -> None:
        with self.assertRaises(ValueError):
            CRunRecord.from_dict(_valid_record_dict(stateless=False))

    def test_reject_empty_sdk_version(self) -> None:
        with self.assertRaises(ValueError):
            CRunRecord.from_dict(_valid_record_dict(openai_sdk_version=""))

    def test_reject_missing_sdk_version(self) -> None:
        d = _valid_record_dict()
        d.pop("openai_sdk_version", None)
        # from_dict will use the default "" which fails validation
        with self.assertRaises(ValueError):
            CRunRecord.from_dict(d)

    def test_valid_sdk_version_accepted(self) -> None:
        rec = CRunRecord.from_dict(_valid_record_dict(openai_sdk_version="3.6.0"))
        self.assertEqual(rec.openai_sdk_version, "3.6.0")

    def test_reject_bad_parsed_output_keys(self) -> None:
        bad = {"predicted_label": "CLS-ZOGAA", "abstain": False}
        with self.assertRaises(ValueError):
            CRunRecord.from_dict(_valid_record_dict(parsed_output=bad))

    def test_reject_non_abstain_with_invalid_label(self) -> None:
        po = {
            "predicted_label": "FAKE-LABEL",
            "abstain": False,
            "used_insight_ids": [],
            "reasoning_summary": "test",
        }
        with self.assertRaises(ValueError):
            CRunRecord.from_dict(_valid_record_dict(parsed_output=po))

    def test_reject_empty_raw_attempts(self) -> None:
        with self.assertRaises(ValueError):
            CRunRecord.from_dict(_valid_record_dict(raw_attempts=[]))

    def test_reject_attempt_missing_keys(self) -> None:
        bad_attempt = {"attempt_index": 0, "raw_response": "x"}
        with self.assertRaises(ValueError):
            CRunRecord.from_dict(_valid_record_dict(raw_attempts=[bad_attempt]))

    def test_reject_bad_attempt_index(self) -> None:
        attempt = _valid_attempt(0)
        attempt["attempt_index"] = 1  # should be 0
        with self.assertRaises(ValueError):
            CRunRecord.from_dict(_valid_record_dict(raw_attempts=[attempt]))


class TestRetryCountConsistency(unittest.TestCase):
    """R5 review point 12: retry_count == len(raw_attempts) - 1."""

    def test_retry_count_matches_attempts(self) -> None:
        """retry_count=1 with 2 attempts is valid."""
        attempts = [
            {**_valid_attempt(0), "parse_success": False, "error_type": "parse"},
            _valid_attempt(1),
        ]
        d = _valid_record_dict(raw_attempts=attempts, retry_count=1)
        record = CRunRecord.from_dict(d)
        self.assertEqual(record.retry_count, 1)

    def test_retry_count_mismatch_too_high(self) -> None:
        """retry_count=2 with 1 attempt → ValueError."""
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(_valid_record_dict(retry_count=2))
        self.assertIn("retry_count", str(ctx.exception))

    def test_retry_count_mismatch_too_low(self) -> None:
        """retry_count=0 with 2 attempts → ValueError."""
        attempts = [
            {**_valid_attempt(0), "parse_success": False, "error_type": "parse"},
            _valid_attempt(1),
        ]
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(_valid_record_dict(
                raw_attempts=attempts, retry_count=0,
            ))
        self.assertIn("retry_count", str(ctx.exception))


class TestValidParseSuccessCoherence(unittest.TestCase):
    """R5 review point 12: valid=True ⟹ final attempt parse_success=True."""

    def test_valid_true_final_parse_failure(self) -> None:
        """valid=True but final attempt parse_success=False → ValueError."""
        attempt = _valid_attempt(0)
        attempt["parse_success"] = False
        attempt["error_type"] = "parse"
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(_valid_record_dict(
                raw_attempts=[attempt], valid=True,
            ))
        self.assertIn("parse_success", str(ctx.exception))

    def test_valid_true_final_error_type_set(self) -> None:
        """valid=True but final attempt error_type='parse' → ValueError."""
        attempt = _valid_attempt(0)
        attempt["error_type"] = "parse"
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(_valid_record_dict(
                raw_attempts=[attempt], valid=True,
            ))
        self.assertIn("error_type", str(ctx.exception))

    def test_valid_false_final_parse_failure_ok(self) -> None:
        """valid=False with final attempt parse_success=False is fine."""
        attempt = _valid_attempt(0)
        attempt["parse_success"] = False
        attempt["error_type"] = "parse"
        d = _valid_record_dict(
            raw_attempts=[attempt], valid=False,
            parsed_output={
                "predicted_label": None, "abstain": True,
                "used_insight_ids": [],
                "reasoning_summary": "parse_failure",
            },
        )
        record = CRunRecord.from_dict(d)
        self.assertFalse(record.valid)


class TestTokenArithmetic(unittest.TestCase):
    """R5 review point 12: token numerics must be int, non-negative, sum."""

    def test_non_int_prompt_tokens(self) -> None:
        attempt = _valid_attempt(0)
        attempt["token_usage"]["prompt_tokens"] = 10.5
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(_valid_record_dict(raw_attempts=[attempt]))
        self.assertIn("must be int", str(ctx.exception))

    def test_negative_completion_tokens(self) -> None:
        attempt = _valid_attempt(0)
        attempt["token_usage"]["completion_tokens"] = -1
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(_valid_record_dict(raw_attempts=[attempt]))
        self.assertIn("non-negative", str(ctx.exception))

    def test_total_not_sum(self) -> None:
        attempt = _valid_attempt(0)
        attempt["token_usage"]["total_tokens"] = 9999
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(_valid_record_dict(raw_attempts=[attempt]))
        self.assertIn("total_tokens must equal", str(ctx.exception))

    def test_correct_token_arithmetic(self) -> None:
        attempt = _valid_attempt(0)
        attempt["token_usage"] = {
            "prompt_tokens": 500,
            "completion_tokens": 200,
            "total_tokens": 700,
        }
        d = _valid_record_dict(raw_attempts=[attempt])
        record = CRunRecord.from_dict(d)
        tu = record.raw_attempts[0]["token_usage"]
        self.assertEqual(tu["total_tokens"],
                         tu["prompt_tokens"] + tu["completion_tokens"])


class TestInsightIdValidation(unittest.TestCase):
    """R5 review point 12: insight ID format and uniqueness."""

    def test_valid_insight_ids(self) -> None:
        d = _valid_record_dict()
        d["parsed_output"]["used_insight_ids"] = ["INS-001", "INS-002"]
        record = CRunRecord.from_dict(d)
        self.assertEqual(
            record.parsed_output["used_insight_ids"],
            ["INS-001", "INS-002"],
        )

    def test_invalid_format_rejects(self) -> None:
        d = _valid_record_dict()
        d["parsed_output"]["used_insight_ids"] = ["BAD-001"]
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(d)
        self.assertIn("insight ID format", str(ctx.exception))

    def test_missing_dash_rejects(self) -> None:
        d = _valid_record_dict()
        d["parsed_output"]["used_insight_ids"] = ["INS001"]
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(d)
        self.assertIn("insight ID format", str(ctx.exception))

    def test_duplicate_ids_rejects(self) -> None:
        d = _valid_record_dict()
        d["parsed_output"]["used_insight_ids"] = ["INS-001", "INS-001"]
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(d)
        self.assertIn("duplicates", str(ctx.exception))

    def test_empty_list_ok(self) -> None:
        d = _valid_record_dict()
        d["parsed_output"]["used_insight_ids"] = []
        record = CRunRecord.from_dict(d)
        self.assertEqual(record.parsed_output["used_insight_ids"], [])



class TestNetworkRetriesValidation(unittest.TestCase):
    """Validate network_retries field (list of per-retry dicts) in CRunRecord."""

    def _valid_retry_entry(self, attempt: int = 0) -> dict:
        return {
            "attempt": attempt,
            "error_type": "ConnectionError",
            "error_message": "Connection refused",
            "backoff_seconds": 2.0 * (2 ** attempt),
            "timestamp_iso": "2026-09-06T12:00:00+00:00",
        }

    def test_default_empty_list(self) -> None:
        """Omitting network_retries defaults to []."""
        d = _valid_record_dict()
        record = CRunRecord.from_dict(d)
        self.assertEqual(record.network_retries, [])

    def test_valid_with_retries(self) -> None:
        retries = [self._valid_retry_entry(0), self._valid_retry_entry(1)]
        d = _valid_record_dict(network_retries=retries)
        record = CRunRecord.from_dict(d)
        self.assertEqual(len(record.network_retries), 2)

    def test_roundtrip_preserves(self) -> None:
        retries = [self._valid_retry_entry(0)]
        d = _valid_record_dict(network_retries=retries)
        record = CRunRecord.from_dict(d)
        line = record.to_jsonl_line()
        restored = CRunRecord.from_jsonl_line(line)
        self.assertEqual(len(restored.network_retries), 1)
        self.assertEqual(restored.network_retries[0]["attempt"], 0)

    def test_reject_non_list(self) -> None:
        d = _valid_record_dict(network_retries=3)
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(d)
        self.assertIn('network_retries', str(ctx.exception))

    def test_reject_entry_not_dict(self) -> None:
        d = _valid_record_dict(network_retries=["not_a_dict"])
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(d)
        self.assertIn('network_retries', str(ctx.exception))

    def test_reject_missing_keys(self) -> None:
        bad_entry = {"attempt": 0, "error_type": "ConnectionError"}
        d = _valid_record_dict(network_retries=[bad_entry])
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(d)
        self.assertIn('network_retries', str(ctx.exception))

    def test_reject_negative_attempt(self) -> None:
        entry = self._valid_retry_entry(0)
        entry["attempt"] = -1
        d = _valid_record_dict(network_retries=[entry])
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(d)
        self.assertIn('network_retries', str(ctx.exception))

    def test_reject_negative_backoff(self) -> None:
        entry = self._valid_retry_entry(0)
        entry["backoff_seconds"] = -1.0
        d = _valid_record_dict(network_retries=[entry])
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(d)
        self.assertIn('network_retries', str(ctx.exception))

    def test_reject_bad_timestamp(self) -> None:
        entry = self._valid_retry_entry(0)
        entry["timestamp_iso"] = "not-a-date"
        d = _valid_record_dict(network_retries=[entry])
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(d)
        self.assertIn('network_retries', str(ctx.exception))

    def test_reject_empty_error_type(self) -> None:
        entry = self._valid_retry_entry(0)
        entry["error_type"] = ""
        d = _valid_record_dict(network_retries=[entry])
        with self.assertRaises(ValueError) as ctx:
            CRunRecord.from_dict(d)
        self.assertIn('network_retries', str(ctx.exception))


class TestCRunRecordSchema(unittest.TestCase):
    def test_schema_loads(self) -> None:
        schema_path = ROOT / "icl" / "schemas" / "c_run_record.schema.json"
        schema = json.loads(schema_path.read_text())
        self.assertEqual(schema["properties"]["agent_id"]["const"], "central")
        self.assertEqual(schema["properties"]["condition"]["const"], "C")
        self.assertTrue(schema["properties"]["stateless"]["const"])

    def test_schema_validates_valid_record(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema_path = ROOT / "icl" / "schemas" / "c_run_record.schema.json"
        schema = json.loads(schema_path.read_text())
        record = CRunRecord.from_dict(_valid_record_dict())
        jsonschema.validate(record.to_dict(), schema)

    def test_schema_rejects_agent_id(self) -> None:
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        schema_path = ROOT / "icl" / "schemas" / "c_run_record.schema.json"
        schema = json.loads(schema_path.read_text())
        d = _valid_record_dict()
        d["agent_id"] = "agent_1"
        with self.assertRaises(jsonschema.ValidationError):
            jsonschema.validate(d, schema)


if __name__ == "__main__":
    unittest.main()
