"""Contract evaluation for the single 40x3 stability gate (rev.10)."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable

from .common import HarnessError


CONDITIONS = ("A", "B-LF", "E-LF")


def semantic_signature(record: dict[str, Any]) -> tuple[Any, ...]:
    """Validity plus parsed decision pair; raw/JSON/finish differences are forensic."""
    valid = record.get("parse_valid_first_attempt") is True
    if not valid:
        return (False, "INVALID")
    parsed = record.get("parsed_output")
    if not isinstance(parsed, dict):
        raise HarnessError("valid gate record lacks parsed_output")
    abstain = parsed.get("abstain")
    predicted = parsed.get("predicted_label")
    if type(abstain) is not bool or (abstain and predicted is not None) or (
        not abstain and not isinstance(predicted, str)
    ):
        raise HarnessError("valid gate record has an invalid abstain/predicted_label pair")
    return (True, abstain, predicted)


def evaluate_stability_gate(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(records)
    if len(rows) != 120:
        raise HarnessError("the stability gate requires exactly 120 first attempts")
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        prompt_id = row.get("prompt_id")
        if not isinstance(prompt_id, str) or row.get("condition") not in CONDITIONS:
            raise HarnessError("gate record lacks a valid prompt or condition")
        grouped[prompt_id].append(row)
    if len(grouped) != 40 or any(len(group) != 3 for group in grouped.values()):
        raise HarnessError("the stability gate requires forty complete triplets")

    valid = sum(row.get("parse_valid_first_attempt") is True for row in rows)
    truncations = sum(
        row.get("finish_reason") == "length" or row.get("truncated") is True for row in rows
    )
    abstention_coverage = {
        condition: any(
            row["condition"] == condition
            and semantic_signature(row) == (True, True, None)
            for row in rows
        )
        for condition in CONDITIONS
    }
    all_invalid = sorted(
        prompt_id
        for prompt_id, group in grouped.items()
        if all(signature[0] is False for signature in map(semantic_signature, group))
    )
    divergent = sorted(
        prompt_id
        for prompt_id, group in grouped.items()
        if prompt_id not in all_invalid
        and len({semantic_signature(row) for row in group}) > 1
    )
    t3 = valid >= 114 and all(abstention_coverage.values())
    t4 = truncations == 0
    t6_evaluable = not all_invalid
    if not t3 or not t4 or not t6_evaluable:
        status = "NO_GO_TECHNICAL"
    elif divergent:
        status = "R3_REQUIRED_PENDING_FEASIBILITY"
    else:
        status = "PASS_R1_PENDING_T5_AND_OTHER_PREREQUISITES"
    return {
        "status": status,
        "go_final": False,
        "provider_requests": 120,
        "valid_first_attempts": valid,
        "invalid_first_attempts": 120 - valid,
        "t3_pass": t3,
        "abstention_coverage": abstention_coverage,
        "length_truncations": truncations,
        "t4_pass": t4,
        "t6_evaluable": t6_evaluable,
        "all_invalid_prompt_ids": all_invalid,
        "divergent_prompt_ids": divergent,
        "divergent_prompt_count": len(divergent),
        "t5_temporal_feasibility": "NOT_MEASURED_BY_OFFLINE_EVALUATION",
    }
