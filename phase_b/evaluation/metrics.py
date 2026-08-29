"""Deterministic offline metrics using evaluator-side pseudolabel truth."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Iterable

from .records import RunRecord


def _records(values: Iterable[RunRecord | dict[str, Any]]) -> list[RunRecord]:
    return [value if isinstance(value, RunRecord) else RunRecord.from_dict(value) for value in values]


def is_correct(record: RunRecord, true_label: str) -> bool:
    parsed = record.parsed_output
    return bool(not parsed["abstain"] and parsed["predicted_label"] == true_label)


def _scope(record: RunRecord, true_label: str, config: dict[str, Any]) -> str:
    local = config["agents"][record.agent_id]["local_fault_label"]
    return "seen" if true_label == "Normal" or true_label == local else "unseen"


def _accuracy(rows: list[tuple[RunRecord, str]]) -> dict[str, float | int | None]:
    n = len(rows)
    correct = sum(is_correct(record, truth) for record, truth in rows)
    abstained = sum(bool(record.parsed_output["abstain"]) for record, _ in rows)
    return {
        "n": n,
        "correct": correct,
        "accuracy": correct / n if n else None,
        "abstentions": abstained,
        "abstention_rate": abstained / n if n else None,
    }


def _paired_transfer(
    lookup: dict[tuple[str, int, str, str], RunRecord],
    *,
    left_condition: str,
    right_condition: str,
    case_truth: dict[str, str],
    config: dict[str, Any],
    agent_id: str | None = None,
) -> dict[str, int | float | None]:
    left_keys = {
        (agent, repetition, case_id)
        for agent, repetition, case_id, condition in lookup
        if condition == left_condition
    }
    right_keys = {
        (agent, repetition, case_id)
        for agent, repetition, case_id, condition in lookup
        if condition == right_condition
    }
    if left_keys != right_keys:
        raise ValueError("paired conditions do not contain identical agent/case/repetition keys")
    helped = harmed = unchanged = 0
    left_correct = right_correct = 0
    n = 0
    for agent, repetition, case_id in sorted(left_keys):
        if agent_id is not None and agent != agent_id:
            continue
        truth = case_truth[case_id]
        left = lookup.get((agent, repetition, case_id, left_condition))
        right = lookup.get((agent, repetition, case_id, right_condition))
        if left is None or right is None:
            raise AssertionError("paired key validation failed")
        if _scope(left, truth, config) != "unseen":
            continue
        lc, rc = is_correct(left, truth), is_correct(right, truth)
        n += 1
        left_correct += lc
        right_correct += rc
        if not lc and rc:
            helped += 1
        elif lc and not rc:
            harmed += 1
        else:
            unchanged += 1
    return {
        "n_pairs": n,
        "left_correct": left_correct,
        "right_correct": right_correct,
        "delta_unseen": (right_correct - left_correct) / n if n else None,
        "helped": helped,
        "harmed": harmed,
        "unchanged": unchanged,
    }


def evaluate_run_records(
    values: Iterable[RunRecord | dict[str, Any]],
    *,
    case_truth: dict[str, str],
    config: dict[str, Any],
) -> dict[str, Any]:
    records = _records(values)
    labels = set(config["label_space"])
    if set(case_truth.values()) - labels:
        raise ValueError("case_truth contains labels outside the frozen label space")
    if any(record.physical_case_id not in case_truth for record in records):
        raise ValueError("run record missing evaluator-side case truth")
    lookup: dict[tuple[str, int, str, str], RunRecord] = {}
    for record in records:
        key = (record.agent_id, record.repetition, record.physical_case_id, record.condition)
        if key in lookup:
            raise ValueError(f"duplicate run record: {key}")
        lookup[key] = record

    condition_metrics: dict[str, Any] = {}
    per_repetition: dict[str, Any] = {}
    recall: dict[str, Any] = {}
    confusion: dict[str, Any] = {}
    insight_usage: dict[str, Any] = {}
    for condition in config["conditions"]:
        selected = [record for record in records if record.condition == condition]
        classified = [(record, case_truth[record.physical_case_id]) for record in selected]
        condition_metrics[condition] = {
            scope: _accuracy(
                [
                    pair
                    for pair in classified
                    if scope == "overall" or _scope(pair[0], pair[1], config) == scope
                ]
            )
            for scope in ("overall", "seen", "unseen")
        }
        per_repetition[condition] = {
            str(repetition): {
                scope: _accuracy(
                    [
                        pair
                        for pair in classified
                        if pair[0].repetition == repetition
                        and (scope == "overall" or _scope(pair[0], pair[1], config) == scope)
                    ]
                )
                for scope in ("overall", "seen", "unseen")
            }
            for repetition in (1, 2, 3)
        }
        recall[condition] = {}
        for label in config["label_space"]:
            label_rows = [pair for pair in classified if pair[1] == label]
            recall[condition][label] = _accuracy(label_rows)
        matrix: dict[str, Counter[str]] = defaultdict(Counter)
        for record, truth in classified:
            predicted = "__ABSTAIN__" if record.parsed_output["abstain"] else record.parsed_output["predicted_label"]
            matrix[truth][str(predicted)] += 1
        confusion[condition] = {
            truth: dict(sorted(counts.items())) for truth, counts in sorted(matrix.items())
        }
        used = sum(bool(record.parsed_output["used_insight_ids"]) for record in selected)
        insight_usage[condition] = {
            "n": len(selected),
            "records_using_insights": used,
            "usage_rate": used / len(selected) if selected else None,
        }

    b_vs_a = _paired_transfer(
        lookup,
        left_condition="A",
        right_condition="B",
        case_truth=case_truth,
        config=config,
    )
    e_vs_a = _paired_transfer(
        lookup,
        left_condition="A",
        right_condition="E",
        case_truth=case_truth,
        config=config,
    )
    per_agent = {
        agent_id: _paired_transfer(
            lookup,
            left_condition="A",
            right_condition="B",
            case_truth=case_truth,
            config=config,
            agent_id=agent_id,
        )
        for agent_id in config["agents"]
    }
    b_delta, e_delta = b_vs_a["delta_unseen"], e_vs_a["delta_unseen"]
    return {
        "unit_warning": "agent-case observations are clustered within physical_case_id; they are not independent physical runs",
        "conditions": condition_metrics,
        "per_repetition": per_repetition,
        "comparisons": {
            "B_vs_A_primary_unseen": b_vs_a,
            "E_vs_A_unseen": e_vs_a,
            "delta_FoT_minus_delta_E": (
                b_delta - e_delta if b_delta is not None and e_delta is not None else None
            ),
            "B_vs_A_per_agent": per_agent,
        },
        "per_pseudolabel_recall": recall,
        "confusion_matrix": confusion,
        "insight_usage": insight_usage,
    }
