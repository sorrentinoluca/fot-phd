"""Validated provider-neutral run-record representation."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
import re
from typing import Any


HASH = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True)
class RunRecord:
    agent_id: str
    condition: str
    repetition: int
    model: str
    model_version: str
    prompt_hash: str
    input_hash: str
    raw_output: str
    parsed_output: dict[str, Any]
    physical_case_id: str
    temperature: float | None
    seed: int | None
    timestamp: str
    prompt_tokens: int | None = None
    completion_tokens: int | None = None
    token_count_method: str = "provider_not_available"

    def validate(self) -> None:
        if not re.fullmatch(r"agent_[1-4]", self.agent_id):
            raise ValueError(f"invalid agent_id: {self.agent_id}")
        if self.condition not in {"A", "B", "E"}:
            raise ValueError(f"invalid condition: {self.condition}")
        if self.repetition not in {1, 2, 3}:
            raise ValueError("repetition must be 1, 2, or 3")
        if not self.model.strip() or not self.model_version.strip():
            raise ValueError("model and model_version are mandatory for run records")
        if not HASH.fullmatch(self.prompt_hash) or not HASH.fullmatch(self.input_hash):
            raise ValueError("prompt_hash and input_hash must be lowercase SHA-256")
        if not isinstance(self.raw_output, str) or not isinstance(self.parsed_output, dict):
            raise ValueError("raw_output must be text and parsed_output must be an object")
        if not self.physical_case_id.strip():
            raise ValueError("physical_case_id is required")
        if type(self.seed) not in {int, type(None)}:
            raise ValueError("seed must be an integer or null")
        for name, value in (
            ("prompt_tokens", self.prompt_tokens),
            ("completion_tokens", self.completion_tokens),
        ):
            if value is not None and (type(value) is not int or value < 0):
                raise ValueError(f"{name} must be a non-negative integer or null")
        try:
            parsed_time = datetime.fromisoformat(self.timestamp.replace("Z", "+00:00"))
        except ValueError as exc:
            raise ValueError("timestamp must be ISO-8601") from exc
        if parsed_time.tzinfo is None:
            raise ValueError("timestamp must include a timezone")
        if not self.token_count_method.strip():
            raise ValueError("token_count_method is required")

    def to_dict(self) -> dict[str, Any]:
        self.validate()
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "RunRecord":
        record = cls(**value)
        record.validate()
        return record
