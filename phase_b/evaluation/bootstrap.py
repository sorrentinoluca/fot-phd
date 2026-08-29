"""Stratified paired bootstrap that resamples physical runs, not agent rows."""

from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable

import numpy as np

from .aggregation import AggregatePrediction, aggregate_run_records
from .metrics import is_correct
from .records import RunRecord


def paired_unseen_rows(
    records: Iterable[RunRecord | dict[str, Any]],
    *,
    case_truth: dict[str, str],
    config: dict[str, Any],
    left_condition: str = "A",
    right_condition: str = "B",
) -> list[dict[str, Any]]:
    aggregates = aggregate_run_records(records, label_space=config["label_space"])
    lookup: dict[tuple[str, str, str], AggregatePrediction] = {}
    for record in aggregates:
        key = (record.agent_id, record.physical_case_id, record.condition)
        if key in lookup:
            raise ValueError(f"duplicate aggregate prediction: {key}")
        lookup[key] = record
    rows: list[dict[str, Any]] = []
    for (agent, case_id, condition), left in sorted(lookup.items()):
        if condition != left_condition:
            continue
        truth = case_truth[case_id]
        local = config["agents"][agent]["local_fault_label"]
        if truth == "Normal" or truth == local:
            continue
        right = lookup.get((agent, case_id, right_condition))
        if right is None:
            raise ValueError("paired bootstrap requires matching condition records")
        rows.append(
            {
                "physical_case_id": case_id,
                "true_pseudolabel": truth,
                "agent_id": agent,
                "left_correct": int(is_correct(left, truth)),
                "right_correct": int(is_correct(right, truth)),
                "delta": int(is_correct(right, truth)) - int(is_correct(left, truth)),
            }
        )
    return rows


def draw_stratified_physical_clusters(
    rows: list[dict[str, Any]], rng: np.random.Generator
) -> list[str]:
    by_label: dict[str, list[str]] = defaultdict(list)
    for row in rows:
        case_id = row["physical_case_id"]
        label = row["true_pseudolabel"]
        if case_id not in by_label[label]:
            by_label[label].append(case_id)
    sampled: list[str] = []
    for label in sorted(by_label):
        clusters = sorted(by_label[label])
        sampled.extend(rng.choice(clusters, size=len(clusters), replace=True).tolist())
    return sampled


def expand_cluster_sample(
    rows: list[dict[str, Any]], sampled_clusters: list[str]
) -> list[dict[str, Any]]:
    by_case: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_case[row["physical_case_id"]].append(row)
    expanded: list[dict[str, Any]] = []
    for case_id in sampled_clusters:
        expanded.extend(by_case[case_id])
    return expanded


def stratified_cluster_paired_bootstrap(
    records: Iterable[RunRecord | dict[str, Any]],
    *,
    case_truth: dict[str, str],
    config: dict[str, Any],
    left_condition: str = "A",
    right_condition: str = "B",
    iterations: int | None = None,
    seed: int | None = None,
    confidence_level: float = 0.95,
) -> dict[str, Any]:
    rows = paired_unseen_rows(
        records,
        case_truth=case_truth,
        config=config,
        left_condition=left_condition,
        right_condition=right_condition,
    )
    if not rows:
        raise ValueError("no paired unseen rows available for bootstrap")
    iterations = iterations or int(config["metrics"]["bootstrap_iterations"])
    seed = int(config["metrics"]["bootstrap_seed"] if seed is None else seed)
    if iterations <= 0 or not 0.0 < confidence_level < 1.0:
        raise ValueError("invalid bootstrap settings")
    clusters = sorted({row["physical_case_id"] for row in rows})
    strata = clusters_per_label(rows)
    expected_labels = set(config["label_space"][:-1])
    if set(strata) != expected_labels or set(strata.values()) != {3} or len(clusters) != 12:
        raise ValueError("primary bootstrap requires four fault strata with three physical runs each")
    rows_per_cluster = {
        case_id: sum(row["physical_case_id"] == case_id for row in rows)
        for case_id in clusters
    }
    if set(rows_per_cluster.values()) != {3}:
        raise ValueError("each physical run must retain exactly three unseen aggregate agent rows")
    rng = np.random.default_rng(seed)
    draws = np.empty(iterations, dtype=float)
    for index in range(iterations):
        sampled_clusters = draw_stratified_physical_clusters(rows, rng)
        expanded = expand_cluster_sample(rows, sampled_clusters)
        draws[index] = float(np.mean([row["delta"] for row in expanded]))
    alpha = 1.0 - confidence_level
    return {
        "definition": f"paired {right_condition}-{left_condition} accuracy delta; stratified resampling of physical_case_id",
        "point_estimate": float(np.mean([row["delta"] for row in rows])),
        "confidence_level": confidence_level,
        "ci_lower": float(np.quantile(draws, alpha / 2.0)),
        "ci_upper": float(np.quantile(draws, 1.0 - alpha / 2.0)),
        "iterations": iterations,
        "seed": seed,
        "n_physical_clusters": len(clusters),
        "n_agent_case_rows": len(rows),
        "clusters_per_pseudolabel": strata,
        "independence_claim": False,
    }


def clusters_per_label(rows: list[dict[str, Any]]) -> dict[str, int]:
    by_label: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        by_label[row["true_pseudolabel"]].add(row["physical_case_id"])
    return {label: len(cases) for label, cases in sorted(by_label.items())}
