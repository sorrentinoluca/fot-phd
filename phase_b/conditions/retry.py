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


def execute_with_retry(
    *,
    call: Callable[[str, int], str],
    prompt: str,
    parse: Callable[[str], dict[str, Any]],
    max_retries: int,
) -> RetryResult:
    if max_retries < 0:
        raise ValueError("max_retries must be non-negative")
    current_prompt = prompt
    errors: list[str] = []
    for attempt in range(1, max_retries + 2):
        raw = call(current_prompt, attempt)
        try:
            parsed = parse(raw)
            return RetryResult(raw, parsed, attempt, tuple(errors))
        except OutputValidationError as exc:
            errors.append(str(exc))
            if attempt > max_retries:
                raise OutputValidationError(
                    f"output invalid after {attempt} deterministic attempts: {exc}"
                ) from exc
            current_prompt = prompt + CORRECTION_SUFFIX
    raise AssertionError("unreachable retry state")
