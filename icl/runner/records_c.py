"""Validated run-record representation for Condition C inference."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
import json
import re
from typing import Any


HASH = re.compile(r"^[0-9a-f]{64}$")
CASE_ID = re.compile(r"^PBH-\d{3}$")
LABEL_SPACE = {"CLS-ZOGAA", "CLS-OJNSG", "CLS-R463B", "CLS-Z3ISU", "Normal"}
INS_ID = re.compile(r"^INS-\d{3}$")


@dataclass(frozen=True)
class CRunRecord:
    # Identity fields
    agent_id: str               # always "central"
    condition: str              # always "C"
    physical_case_id: str       # PBH-XXX
    repetition: int             # 1..3
    sequence_index: int         # 0..44

    # Prediction (full structured output)
    parsed_output: dict[str, Any]
    valid: bool

    # Provenance
    prompt_sha256: str
    raw_attempts: list[dict[str, Any]]
    retry_count: int
    model_requested: str
    model_returned: str
    reasoning_effort: str
    timestamp_iso: str
    stateless: bool = True

    def validate(self) -> None:
        # Identity
        if self.agent_id != "central":
            raise ValueError(f"C records require agent_id='central', got {self.agent_id!r}")
        if self.condition != "C":
            raise ValueError(f"C records require condition='C', got {self.condition!r}")
        if not CASE_ID.fullmatch(self.physical_case_id):
            raise ValueError(f"invalid physical_case_id: {self.physical_case_id!r}")
        if self.repetition not in {1, 2, 3}:
            raise ValueError(f"repetition must be 1, 2, or 3, got {self.repetition}")
        if not isinstance(self.sequence_index, int) or not 0 <= self.sequence_index <= 44:
            raise ValueError(f"sequence_index must be 0..44, got {self.sequence_index}")

        # Parsed output structure
        if not isinstance(self.parsed_output, dict):
            raise ValueError("parsed_output must be a dict")
        required_keys = {"predicted_label", "abstain", "used_insight_ids", "reasoning_summary"}
        if set(self.parsed_output) != required_keys:
            raise ValueError(f"parsed_output keys must be exactly {sorted(required_keys)}")
        abstain = self.parsed_output["abstain"]
        if not isinstance(abstain, bool):
            raise ValueError("parsed_output.abstain must be bool")
        predicted = self.parsed_output["predicted_label"]
        if not abstain:
            if predicted not in LABEL_SPACE:
                raise ValueError(f"invalid predicted_label: {predicted!r}")
        else:
            if predicted is not None:
                raise ValueError("abstaining output requires predicted_label=null")
        used = self.parsed_output["used_insight_ids"]
        if not isinstance(used, list) or any(not isinstance(i, str) for i in used):
            raise ValueError("used_insight_ids must be a list of strings")
        # Insight ID format and uniqueness (R5 review point 12).
        for ins_id in used:
            if not INS_ID.fullmatch(ins_id):
                raise ValueError(
                    f"invalid insight ID format: {ins_id!r} (expected INS-NNN)"
                )
        if len(used) != len(set(used)):
            raise ValueError("used_insight_ids contains duplicates")
        reasoning = self.parsed_output["reasoning_summary"]
        if not isinstance(reasoning, str) or not reasoning.strip():
            raise ValueError("reasoning_summary must be non-empty")

        if not isinstance(self.valid, bool):
            raise ValueError("valid must be bool")

        # Provenance
        if not HASH.fullmatch(self.prompt_sha256):
            raise ValueError("prompt_sha256 must be lowercase SHA-256")
        if not isinstance(self.raw_attempts, list) or not self.raw_attempts:
            raise ValueError("raw_attempts must be a non-empty list")
        for i, attempt in enumerate(self.raw_attempts):
            if not isinstance(attempt, dict):
                raise ValueError(f"raw_attempts[{i}] must be a dict")
            required_attempt = {"attempt_index", "raw_response", "parse_success",
                                "error_type", "request_id", "response_id", "token_usage"}
            if set(attempt) != required_attempt:
                raise ValueError(
                    f"raw_attempts[{i}] keys must be exactly {sorted(required_attempt)}, "
                    f"got {sorted(attempt)}"
                )
            if attempt["attempt_index"] != i:
                raise ValueError(f"raw_attempts[{i}].attempt_index must be {i}")
            if not isinstance(attempt["raw_response"], str):
                raise ValueError(f"raw_attempts[{i}].raw_response must be string")
            if not isinstance(attempt["parse_success"], bool):
                raise ValueError(f"raw_attempts[{i}].parse_success must be bool")
            if attempt["error_type"] is not None and attempt["error_type"] not in {
                "network", "parse", "schema"
            }:
                raise ValueError(f"raw_attempts[{i}].error_type invalid: {attempt['error_type']}")
            # request_id and response_id can be str or None
            tu = attempt["token_usage"]
            if tu is not None:
                if not isinstance(tu, dict):
                    raise ValueError(f"raw_attempts[{i}].token_usage must be dict or null")
                for key in ("prompt_tokens", "completion_tokens", "total_tokens"):
                    if key not in tu:
                        raise ValueError(f"raw_attempts[{i}].token_usage missing {key}")
                    if not isinstance(tu[key], int):
                        raise ValueError(f"raw_attempts[{i}].token_usage.{key} must be int")
                    if tu[key] < 0:
                        raise ValueError(f"raw_attempts[{i}].token_usage.{key} must be non-negative")
                if tu["total_tokens"] != tu["prompt_tokens"] + tu["completion_tokens"]:
                    raise ValueError(
                        f"raw_attempts[{i}].token_usage: total_tokens must equal "
                        f"prompt_tokens + completion_tokens"
                    )

        if not isinstance(self.retry_count, int) or self.retry_count < 0:
            raise ValueError("retry_count must be a non-negative integer")
        # retry_count consistency (R5 review point 12).
        if self.retry_count != len(self.raw_attempts) - 1:
            raise ValueError(
                f"retry_count ({self.retry_count}) must equal "
                f"len(raw_attempts) - 1 ({len(self.raw_attempts) - 1})"
            )
        # valid/parse_success coherence (R5 review point 12).
        final_attempt = self.raw_attempts[-1]
        if self.valid:
            if not final_attempt["parse_success"]:
                raise ValueError(
                    "valid=True requires final attempt parse_success=True"
                )
            if final_attempt["error_type"] is not None:
                raise ValueError(
                    "valid=True requires final attempt error_type=None"
                )
        if not self.model_requested.strip():
            raise ValueError("model_requested is required")
        if not self.model_returned.strip():
            raise ValueError("model_returned is required")
        if self.reasoning_effort not in {"low", "medium", "high"}:
            raise ValueError(f"invalid reasoning_effort: {self.reasoning_effort!r}")
        try:
            parsed_time = datetime.fromisoformat(self.timestamp_iso.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("timestamp_iso must be ISO-8601") from exc
        if parsed_time.tzinfo is None:
            raise ValueError("timestamp_iso must include a timezone")
        if self.stateless is not True:
            raise ValueError("stateless must be true for Condition C")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    def to_jsonl_line(self) -> str:
        """Serialize to a single JSON line for append to c_records.jsonl."""
        return json.dumps(self.to_dict(), ensure_ascii=False, separators=(",", ":"))

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "CRunRecord":
        record = cls(**value)
        record.validate()
        return record

    @classmethod
    def from_jsonl_line(cls, line: str) -> "CRunRecord":
        return cls.from_dict(json.loads(line))
