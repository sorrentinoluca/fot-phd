"""Strict JSON parsing for diagnostic and insight-generation outputs."""

from __future__ import annotations

import json
from typing import Any, Iterable

from phase_b.insights import Insight
from phase_b.insights.library import validate_label_neutral_fields


DIAGNOSTIC_KEYS = {
    "predicted_label",
    "abstain",
    "used_insight_ids",
    "reasoning_summary",
}


class OutputValidationError(ValueError):
    pass


def _no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise OutputValidationError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_loads(raw: str) -> Any:
    if not isinstance(raw, str) or not raw.strip():
        raise OutputValidationError("output is empty or not text")
    try:
        return json.loads(raw.strip(), object_pairs_hook=_no_duplicate_object)
    except OutputValidationError:
        raise
    except json.JSONDecodeError as exc:
        raise OutputValidationError(f"invalid JSON: {exc.msg}") from exc


def parse_diagnostic_output(
    raw: str,
    *,
    label_space: Iterable[str],
    allowed_insight_ids: Iterable[str],
) -> dict[str, Any]:
    value = strict_json_loads(raw)
    if not isinstance(value, dict) or set(value) != DIAGNOSTIC_KEYS:
        raise OutputValidationError(f"diagnostic keys must be exactly {sorted(DIAGNOSTIC_KEYS)}")
    abstain = value["abstain"]
    if type(abstain) is not bool:
        raise OutputValidationError("abstain must be a JSON Boolean")
    labels = set(label_space)
    predicted = value["predicted_label"]
    if predicted is not None and predicted not in labels:
        raise OutputValidationError(f"unknown predicted_label: {predicted!r}")
    if not abstain and predicted not in labels:
        raise OutputValidationError("non-abstaining output requires one exact supplied label")
    if abstain and predicted is not None:
        raise OutputValidationError("abstaining output requires predicted_label to be null")
    used = value["used_insight_ids"]
    if not isinstance(used, list) or any(not isinstance(item, str) for item in used):
        raise OutputValidationError("used_insight_ids must be a string array")
    if len(used) != len(set(used)):
        raise OutputValidationError("used_insight_ids must not contain duplicates")
    allowed = set(allowed_insight_ids)
    unknown = sorted(set(used) - allowed)
    if unknown:
        raise OutputValidationError(f"unknown or unavailable insight IDs: {unknown}")
    reasoning = value["reasoning_summary"]
    if not isinstance(reasoning, str) or not reasoning.strip():
        raise OutputValidationError("reasoning_summary must be non-empty text")
    return value


def parse_insight_generation_output(
    raw: str,
    *,
    expected_ids: Iterable[str],
    source_agent: str,
    pseudolabel: str,
    evidence_scope: str,
    label_space: Iterable[str],
) -> list[Insight]:
    value = strict_json_loads(raw)
    if not isinstance(value, list) or len(value) != 2:
        raise OutputValidationError("insight generation must return exactly two objects")
    try:
        insights = [Insight.from_dict(item) for item in value]
    except (TypeError, ValueError) as exc:
        raise OutputValidationError(str(exc)) from exc
    ids = list(expected_ids)
    if [item.insight_id for item in insights] != ids:
        raise OutputValidationError("insight IDs or order differ from the supplied order")
    for item in insights:
        if (
            item.source_agent != source_agent
            or item.pseudolabel != pseudolabel
            or item.evidence_scope != evidence_scope
        ):
            raise OutputValidationError("fixed insight provenance fields were changed")
        try:
            validate_label_neutral_fields(item, label_space=label_space)
        except ValueError as exc:
            raise OutputValidationError(str(exc)) from exc
    return insights
