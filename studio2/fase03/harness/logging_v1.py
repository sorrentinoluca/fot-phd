"""Append-only forensic call logging for §8.7."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import json
import os
from pathlib import Path
import re
from typing import Any

from .common import HarnessError, canonical_json, sha256_text


HASH = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class CallRecord:
    prompt_id: str
    agent_id: str
    physical_case_id: str
    condition: str
    repetition: int
    attempt: int
    timestamp_utc: str
    provider: str
    requested_model: str
    returned_model: str
    returned_model_revision: str | None
    request_id: str
    system_fingerprint: str | None
    temperature_supported: bool | None
    seed_supported: bool | None
    generation: dict[str, Any]
    prompt_sha256: str
    prompt_bytes: int
    raw_response: str
    raw_response_sha256: str
    raw_response_bytes: int
    latency_ms: float
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    token_source: str
    finish_reason: str | None
    truncated: bool
    parse_valid: bool
    schema_valid: bool | None
    parsed_output: dict[str, Any] | None
    error: dict[str, Any] | None

    @classmethod
    def create(cls, **value: Any) -> "CallRecord":
        raw = value.get("raw_response")
        if not isinstance(raw, str):
            raise HarnessError("raw_response must be text")
        value.setdefault("raw_response_sha256", sha256_text(raw))
        value.setdefault("raw_response_bytes", len(raw.encode("utf-8")))
        record = cls(**value)
        record.validate()
        return record

    def validate(self) -> None:
        if not self.prompt_id or not re.fullmatch(r"agent_[1-8]", self.agent_id):
            raise HarnessError("invalid prompt or agent identity")
        if self.condition not in {"A", "B-LF", "E-LF", "PRODUCER"}:
            raise HarnessError("invalid call condition")
        if self.repetition < 1 or self.attempt < 1:
            raise HarnessError("repetition and attempt are one-based")
        try:
            timestamp = datetime.fromisoformat(self.timestamp_utc.replace("Z", "+00:00"))
        except ValueError as exc:
            raise HarnessError("timestamp_utc must be ISO-8601") from exc
        if timestamp.tzinfo is None:
            raise HarnessError("timestamp_utc requires a timezone")
        required_text = (
            self.provider,
            self.requested_model,
            self.returned_model,
            self.request_id,
            self.token_source,
        )
        if any(not isinstance(item, str) or not item.strip() for item in required_text):
            raise HarnessError("provider/model/request/token metadata must be non-empty")
        if not HASH.fullmatch(self.prompt_sha256) or not HASH.fullmatch(self.raw_response_sha256):
            raise HarnessError("prompt and response hashes must be lowercase SHA-256")
        if self.raw_response_sha256 != sha256_text(self.raw_response):
            raise HarnessError("raw response hash mismatch")
        if self.raw_response_bytes != len(self.raw_response.encode("utf-8")):
            raise HarnessError("raw response byte count mismatch")
        if self.prompt_bytes < 1 or self.latency_ms < 0:
            raise HarnessError("invalid prompt bytes or latency")
        tokens = (self.prompt_tokens, self.completion_tokens, self.total_tokens)
        if any(value is not None and (type(value) is not int or value < 0) for value in tokens):
            raise HarnessError("token counts must be non-negative integers or null")
        if self.total_tokens is not None:
            if self.prompt_tokens is None or self.completion_tokens is None:
                raise HarnessError("total tokens require prompt and completion counts")
            if self.total_tokens != self.prompt_tokens + self.completion_tokens:
                raise HarnessError("total token count is inconsistent")
        if type(self.truncated) is not bool or type(self.parse_valid) is not bool:
            raise HarnessError("truncated and parse_valid must be booleans")
        if self.schema_valid not in {True, False, None}:
            raise HarnessError("schema_valid must be boolean or null")
        if self.parse_valid and self.parsed_output is None:
            raise HarnessError("a parse-valid call requires parsed_output")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)


class JsonlCallLogger:
    """Create-once JSONL logger. Existing logs are never appended implicitly."""

    def __init__(self, path: Path, *, create: bool = True) -> None:
        self.path = path
        if create:
            path.parent.mkdir(parents=True, exist_ok=True)
            descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
            os.close(descriptor)
        elif not path.is_file():
            raise HarnessError(f"log does not exist: {path}")

    def append(self, record: CallRecord) -> None:
        line = canonical_json(record.to_dict()) + "\n"
        with self.path.open("a", encoding="utf-8") as stream:
            stream.write(line)
            stream.flush()
            os.fsync(stream.fileno())


def read_records(path: Path) -> list[CallRecord]:
    records: list[CallRecord] = []
    with path.open("r", encoding="utf-8") as stream:
        for number, line in enumerate(stream, start=1):
            try:
                value = json.loads(line)
                record = CallRecord(**value)
                record.validate()
                records.append(record)
            except (json.JSONDecodeError, TypeError, HarnessError) as exc:
                raise HarnessError(f"invalid call log line {number}: {exc}") from exc
    return records

