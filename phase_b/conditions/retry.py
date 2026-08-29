"""Provider-neutral deterministic retry policy for invalid JSON outputs."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from .parser import OutputValidationError


CORRECTION_SUFFIX = """

CORRECTION REQUIRED
The previous response failed strict schema validation. Return only one valid JSON object with exactly: predicted_label, abstain, used_insight_ids, reasoning_summary. Do not add markdown, confidence, or any other key.
""".rstrip()


@dataclass(frozen=True)
class RetryResult:
    raw_output: str
    parsed_output: dict[str, Any]
    attempts: int
    validation_errors: tuple[str, ...]
    raw_attempts: tuple[str, ...]
    parse_failure: bool


PARSE_FAILURE_OUTPUT: dict[str, Any] = {
    "predicted_label": None,
    "abstain": True,
    "used_insight_ids": [],
    "reasoning_summary": "parse_failure",
}


def execute_with_retry(
    *,
    call: Callable[[str, int], str],
    prompt: str,
    parse: Callable[[str], dict[str, Any]],
    max_retries: int,
) -> RetryResult:
    if max_retries != 2:
        raise ValueError("Phase B retry policy requires exactly two retries")
    current_prompt = prompt
    errors: list[str] = []
    raw_attempts: list[str] = []
    for attempt in range(1, max_retries + 2):
        raw = call(current_prompt, attempt)
        raw_attempts.append(raw)
        try:
            parsed = parse(raw)
            return RetryResult(
                raw, parsed, attempt, tuple(errors), tuple(raw_attempts), False
            )
        except OutputValidationError as exc:
            errors.append(str(exc))
            if attempt > max_retries:
                return RetryResult(
                    raw,
                    dict(PARSE_FAILURE_OUTPUT),
                    attempt,
                    tuple(errors),
                    tuple(raw_attempts),
                    True,
                )
            current_prompt = prompt + CORRECTION_SUFFIX
    raise AssertionError("unreachable retry state")
