"""Deterministic offline metrics using evaluator-side pseudolabel truth."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any, Iterable

from .aggregation import AggregatePrediction, aggregate_run_records
from .records import RunRecord


def _records(values: Iterable[RunRecord | dict[str, Any]]) -> list[RunRecord]:
    return [value if isinstance(value, RunRecord) else RunRecord.from_dict(value) for value in values]


def is_correct(record: RunRecord | AggregatePrediction, true_label: str) -> bool:
    parsed = record.parsed_output
    return bool(not parsed["abstain"] and parsed["predicted_label"] == true_label)


def _scope(record: RunRecord | AggregatePrediction, true_label: str, config: dict[str, Any]) -> str:
    local = config["agents"][record.agent_id]["local_fault_label"]
    if true_label == "Normal":
        return "normal"
    if true_label == local:
        return "local_fault_seen"
    return "unseen"


def _in_scope(
    record: RunRecord | AggregatePrediction,
    truth: str,
    scope: str,
    config: dict[str, Any],
) -> bool:
    atomic = _scope(record, truth, config)
    return scope == "overall" or scope == atomic or (
        scope == "seen" and atomic in {"normal", "local_fault_seen"}
    )


def _accuracy(rows: list[tuple[RunRecord | AggregatePrediction, str]]) -> dict[str, float | int | None]:
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
    lookup: dict[tuple[str, str, str], AggregatePrediction],
    *,
    left_condition: str,
    right_condition: str,
    case_truth: dict[str, str],
    config: dict[str, Any],
    agent_id: str | None = None,
) -> dict[str, int | float | None]:
    left_keys = {(agent, case_id) for agent, case_id, condition in lookup if condition == left_condition}
    right_keys = {(agent, case_id) for agent, case_id, condition in lookup if condition == right_condition}
    if left_keys != right_keys:
        raise ValueError("paired conditions do not contain identical aggregate agent/case keys")
    helped = harmed = unchanged = left_correct = right_correct = n = 0
    for agent, case_id in sorted(left_keys):
        if agent_id is not None and agent != agent_id:
            continue
        truth = case_truth[case_id]
        left = lookup[(agent, case_id, left_condition)]
        right = lookup[(agent, case_id, right_condition)]
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
    aggregates = aggregate_run_records(records, label_space=config["label_space"])
    lookup: dict[tuple[str, str, str], AggregatePrediction] = {}
    for aggregate in aggregates:
        key = (aggregate.agent_id, aggregate.physical_case_id, aggregate.condition)
        if key in lookup:
            raise ValueError(f"duplicate aggregate prediction: {key}")
        lookup[key] = aggregate

    condition_metrics: dict[str, Any] = {}
    per_repetition: dict[str, Any] = {}
    recall: dict[str, Any] = {}
    confusion: dict[str, Any] = {}
    insight_usage: dict[str, Any] = {}
    scopes = ("overall", "seen", "unseen", "local_fault_seen", "normal")
    for condition in config["conditions"]:
        selected = [item for item in aggregates if item.condition == condition]
        classified = [(item, case_truth[item.physical_case_id]) for item in selected]
        condition_metrics[condition] = {
            scope: _accuracy([pair for pair in classified if _in_scope(pair[0], pair[1], scope, config)])
            for scope in scopes
        }

        repetition_selected = [record for record in records if record.condition == condition]
        repetition_classified = [(record, case_truth[record.physical_case_id]) for record in repetition_selected]
        per_repetition[condition] = {
            str(repetition): {
                scope: _accuracy(
                    [pair for pair in repetition_classified if pair[0].repetition == repetition and _in_scope(pair[0], pair[1], scope, config)]
                )
                for scope in scopes
            }
            for repetition in (1, 2, 3)
        }
        recall[condition] = {
            label: _accuracy([pair for pair in classified if pair[1] == label])
            for label in config["label_space"]
        }
        matrix: dict[str, Counter[str]] = defaultdict(Counter)
        for aggregate, truth in classified:
            parsed = aggregate.parsed_output
            predicted = "__ABSTAIN__" if parsed["abstain"] else parsed["predicted_label"]
            matrix[truth][str(predicted)] += 1
        confusion[condition] = {truth: dict(sorted(counts.items())) for truth, counts in sorted(matrix.items())}
        used = sum(bool(record.parsed_output["used_insight_ids"]) for record in repetition_selected)
        insight_usage[condition] = {
            "unit": "repetition_level",
            "n": len(repetition_selected),
            "records_using_insights": used,
            "usage_rate": used / len(repetition_selected) if repetition_selected else None,
        }

    b_vs_a = _paired_transfer(lookup, left_condition="A", right_condition="B", case_truth=case_truth, config=config)
    e_vs_a = _paired_transfer(lookup, left_condition="A", right_condition="E", case_truth=case_truth, config=config)
    per_agent = {
        agent_id: _paired_transfer(
            lookup, left_condition="A", right_condition="B", case_truth=case_truth,
            config=config, agent_id=agent_id,
        )
        for agent_id in config["agents"]
    }
    b_delta, e_delta = b_vs_a["delta_unseen"], e_vs_a["delta_unseen"]
    positive_agents = sum(
        value["delta_unseen"] is not None and value["delta_unseen"] > 0
        for value in per_agent.values()
    )

    def scope_delta(scope: str) -> float | None:
        left = condition_metrics["A"][scope]["accuracy"]
        right = condition_metrics["B"][scope]["accuracy"]
        return None if left is None or right is None else right - left

    return {
        "primary_unit": "R=3 aggregate agent-case prediction",
        "unit_warning": "agent-case observations are clustered within physical_case_id; only 12 unseen physical fault-runs are independent clusters",
        "conditions": condition_metrics,
        "per_repetition": per_repetition,
        "comparisons": {
            "B_vs_A_primary_unseen": b_vs_a,
            "E_vs_A_unseen": e_vs_a,
            "delta_FoT_minus_delta_E": b_delta - e_delta if b_delta is not None and e_delta is not None else None,
            "H3_accuracy_B_unseen_gt_E_unseen": condition_metrics["B"]["unseen"]["accuracy"] > condition_metrics["E"]["unseen"]["accuracy"],
            "B_vs_A_per_agent": per_agent,
            "primary_support": {
                "delta_unseen_positive": b_delta is not None and b_delta > 0,
                "positive_agents": positive_agents,
                "positive_at_least_3_of_4_agents": positive_agents >= 3,
                "helped_gt_harmed": b_vs_a["helped"] > b_vs_a["harmed"],
                "delta_unseen_gt_delta_E": b_delta is not None and e_delta is not None and b_delta > e_delta,
            },
            "secondary_seen_deltas": {
                "epsilon": 0.0,
                "local_fault_seen_B_minus_A": scope_delta("local_fault_seen"),
                "normal_B_minus_A": scope_delta("normal"),
            },
        },
        "per_pseudolabel_recall": recall,
        "confusion_matrix": confusion,
        "insight_usage": insight_usage,
    }
