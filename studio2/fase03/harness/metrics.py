"""Study 2 endpoint metrics and pending 03.8 statistical procedures."""

from __future__ import annotations

from collections import Counter, defaultdict
import math
import random
from statistics import NormalDist
from typing import Any, Callable, Iterable

from .common import HarnessError


BOOTSTRAP_SEED = 20260913
BOOTSTRAP_NAMESPACE = "studio2-fase03-piano-statistico-v1"


def _correct(row: dict[str, Any]) -> bool:
    return bool(
        row.get("valid") is True
        and row.get("abstain") is False
        and row.get("predicted_label") == row.get("true_pseudolabel")
    )


def _abstained(row: dict[str, Any]) -> bool:
    return bool(row.get("valid") is True and row.get("abstain") is True)


def three_numbers(rows: Iterable[dict[str, Any]]) -> dict[str, int | float | None]:
    values = list(rows)
    total = len(values)
    correct = sum(_correct(row) for row in values)
    abstained = sum(_abstained(row) for row in values)
    invalid = sum(row.get("valid") is not True for row in values)
    non_abstained = total - abstained
    return {
        "total": total,
        "correct": correct,
        "abstained": abstained,
        "non_abstained": non_abstained,
        "invalid": invalid,
        "accuracy_all": correct / total if total else None,
        "abstention_rate": abstained / total if total else None,
        "accuracy_non_abstained": correct / non_abstained if non_abstained else None,
    }


def _clustered(rows: list[dict[str, Any]]) -> dict[str, dict[str, list[dict[str, Any]]]]:
    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for row in rows:
        label, case_id = row.get("true_pseudolabel"), row.get("physical_case_id")
        if not isinstance(label, str) or not isinstance(case_id, str):
            raise HarnessError("metric rows require true_pseudolabel and physical_case_id")
        grouped[label][case_id].append(row)
    return grouped


def _validate_strata(
    grouped: dict[str, dict[str, list[dict[str, Any]]]], *, expected_rows_per_cluster: int
) -> dict[str, int]:
    if "Normal" in grouped or len(grouped) != 8:
        raise HarnessError("fault bootstrap requires exactly eight non-Normal strata")
    cluster_counts = {label: len(cases) for label, cases in grouped.items()}
    if len(set(cluster_counts.values())) != 1:
        raise HarnessError("all fault strata require the same number of physical clusters")
    for label, cases in grouped.items():
        for case_id, rows in cases.items():
            if len(rows) != expected_rows_per_cluster:
                raise HarnessError(
                    f"{label}/{case_id} has {len(rows)} rows; expected {expected_rows_per_cluster}"
                )
    return dict(sorted(cluster_counts.items()))


def _quantile(values: list[float], probability: float) -> float:
    if not values or not 0.0 <= probability <= 1.0:
        raise HarnessError("invalid quantile request")
    ordered = sorted(values)
    position = (len(ordered) - 1) * probability
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return ordered[lower]
    return ordered[lower] + (ordered[upper] - ordered[lower]) * (position - lower)


def stratified_cluster_bootstrap_endpoint(
    rows: Iterable[dict[str, Any]],
    *,
    statistic: Callable[[list[dict[str, Any]]], float | None],
    expected_rows_per_cluster: int,
    iterations: int = 10_000,
    seed: int = BOOTSTRAP_SEED,
) -> dict[str, Any]:
    values = list(rows)
    grouped = _clustered(values)
    counts = _validate_strata(grouped, expected_rows_per_cluster=expected_rows_per_cluster)
    if iterations < 1:
        raise HarnessError("bootstrap iterations must be positive")
    generator = random.Random(seed)
    draws: list[float] = []
    null_denominator = 0
    for _ in range(iterations):
        expanded: list[dict[str, Any]] = []
        for label in sorted(grouped):
            cases = sorted(grouped[label])
            for _ in cases:
                selected = cases[generator.randrange(len(cases))]
                expanded.extend(grouped[label][selected])
        result = statistic(expanded)
        if result is None:
            null_denominator += 1
        else:
            draws.append(float(result))
    if not draws:
        raise HarnessError("every bootstrap replicate has a null denominator")
    point = statistic(values)
    return {
        "point_estimate": point,
        "ci_lower": _quantile(draws, 0.025),
        "ci_upper": _quantile(draws, 0.975),
        "q05": _quantile(draws, 0.05),
        "iterations": iterations,
        "seed": seed,
        "namespace": BOOTSTRAP_NAMESPACE,
        "null_denominator_replicates": null_denominator,
        "n_physical_clusters": sum(counts.values()),
        "n_agent_case_rows": len(values),
        "clusters_per_pseudolabel": counts,
        "independence_claim": False,
    }


def endpoint_statistic(name: str) -> Callable[[list[dict[str, Any]]], float | None]:
    keys = {"accuracy_all", "abstention_rate", "accuracy_non_abstained"}
    if name not in keys:
        raise HarnessError(f"unknown endpoint statistic: {name}")
    return lambda rows: three_numbers(rows)[name]  # type: ignore[return-value]


def paired_rows(
    rows: Iterable[dict[str, Any]], *, left_condition: str, right_condition: str
) -> list[dict[str, Any]]:
    values = list(rows)
    lookup: dict[tuple[str, str, str], dict[str, Any]] = {}
    for row in values:
        key = (row["agent_id"], row["physical_case_id"], row["condition"])
        if key in lookup:
            raise HarnessError(f"duplicate condition row: {key}")
        lookup[key] = row
    left_keys = {(a, c) for a, c, condition in lookup if condition == left_condition}
    right_keys = {(a, c) for a, c, condition in lookup if condition == right_condition}
    if left_keys != right_keys:
        raise HarnessError("paired conditions do not contain identical agent/case keys")
    result = []
    for agent, case_id in sorted(left_keys):
        left = lookup[(agent, case_id, left_condition)]
        right = lookup[(agent, case_id, right_condition)]
        if left["true_pseudolabel"] != right["true_pseudolabel"]:
            raise HarnessError("paired rows disagree on evaluator-side truth")
        result.append(
            {
                "agent_id": agent,
                "physical_case_id": case_id,
                "true_pseudolabel": left["true_pseudolabel"],
                "left_correct": int(_correct(left)),
                "right_correct": int(_correct(right)),
                "delta": int(_correct(right)) - int(_correct(left)),
            }
        )
    return result


def bootstrap_paired_delta(
    rows: Iterable[dict[str, Any]],
    *,
    left_condition: str,
    right_condition: str,
    expected_rows_per_cluster: int,
    iterations: int = 10_000,
    seed: int = BOOTSTRAP_SEED,
) -> dict[str, Any]:
    pairs = paired_rows(rows, left_condition=left_condition, right_condition=right_condition)
    result = stratified_cluster_bootstrap_endpoint(
        pairs,
        statistic=lambda selected: sum(row["delta"] for row in selected) / len(selected),
        expected_rows_per_cluster=expected_rows_per_cluster,
        iterations=iterations,
        seed=seed,
    )
    result["definition"] = f"paired {right_condition}-{left_condition} accuracy delta"
    return result


def hoeffding_superiority(cluster_means: Iterable[float], *, alpha: float = 0.05) -> dict[str, Any]:
    values = [float(value) for value in cluster_means]
    if not values or any(value < -1.0 or value > 1.0 for value in values):
        raise HarnessError("cluster means must be non-empty and in [-1, 1]")
    if not 0.0 < alpha < 1.0:
        raise HarnessError("alpha must be in (0, 1)")
    threshold = math.sqrt(2.0 * math.log(1.0 / alpha) / len(values))
    estimate = sum(values) / len(values)
    return {
        "test": "Hoeffding weak-null superiority",
        "mean_cluster_delta": estimate,
        "threshold": threshold,
        "alpha": alpha,
        "reject": estimate >= threshold,
        "status": "PENDING_AUTHOR_FREEZE_03_8",
    }


def tango_noninferiority(
    left_correct: Iterable[bool],
    right_correct: Iterable[bool],
    *,
    margin: float = 0.125,
    alpha: float = 0.05,
) -> dict[str, Any]:
    left, right = list(left_correct), list(right_correct)
    if not left or len(left) != len(right) or not 0.0 < margin < 1.0:
        raise HarnessError("Tango requires equal non-empty paired arrays and margin in (0, 1)")
    # right-left is the effect; b is right correct/left wrong, c the reverse.
    b = sum(bool(r) and not bool(l) for l, r in zip(left, right))
    c = sum(bool(l) and not bool(r) for l, r in zip(left, right))
    n = len(left)
    delta0 = -margin
    quadratic_b = -(b + c) + delta0 * (2.0 * n - b + c)
    quadratic_c = -c * delta0 * (1.0 - delta0)
    discriminant = max(quadratic_b * quadratic_b - 8.0 * n * quadratic_c, 0.0)
    p21 = (-quadratic_b + math.sqrt(discriminant)) / (4.0 * n)
    variance = n * (2.0 * p21 + delta0 * (1.0 - delta0))
    if b == 0 and c == 0:
        z = math.inf
    elif variance <= 0.0:
        raise HarnessError("Tango restricted variance is not positive")
    else:
        z = (b - c - n * delta0) / math.sqrt(variance)
    critical = NormalDist().inv_cdf(1.0 - alpha)
    return {
        "test": "Tango paired-score non-inferiority",
        "n_pairs": n,
        "b_right_only_correct": b,
        "c_left_only_correct": c,
        "margin": margin,
        "alpha": alpha,
        "z": z,
        "critical_z": critical,
        "reject_noninferiority_null": z > critical,
        "zero_discordant_pairs": b == 0 and c == 0,
        "status": "PENDING_AUTHOR_FREEZE_03_8",
    }


def divergence_summary(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    by_prompt: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in records:
        by_prompt[row["prompt_id"]].append(row)
    divergent = []
    raw_only = []
    for prompt_id, rows in sorted(by_prompt.items()):
        if len(rows) != 3 or Counter(row["repetition"] for row in rows) != Counter({1: 1, 2: 1, 3: 1}):
            raise HarnessError(f"{prompt_id} does not have repetitions 1, 2, 3")
        pairs = {
            (row.get("parse_valid"), (row.get("parsed_output") or {}).get("abstain"), (row.get("parsed_output") or {}).get("predicted_label"))
            for row in rows
        }
        hashes = {row.get("raw_response_sha256") for row in rows}
        if len(pairs) > 1:
            divergent.append(prompt_id)
        elif len(hashes) > 1:
            raw_only.append(prompt_id)
    return {
        "prompt_count": len(by_prompt),
        "divergent_prompt_count": len(divergent),
        "divergent_prompt_ids": divergent,
        "raw_only_difference_prompt_count": len(raw_only),
        "raw_only_difference_prompt_ids": raw_only,
        "gate_action": "R=1_WITH_CONTINUOUS_AUDIT" if not divergent else "R=3_ENTIRE_STUDY",
        "rule_of_three_upper_bound_if_zero": 3.0 / len(by_prompt) if by_prompt and not divergent else None,
    }


def _binomial_cdf(k: int, n: int, probability: float) -> float:
    return sum(
        math.comb(n, index)
        * probability**index
        * (1.0 - probability) ** (n - index)
        for index in range(k + 1)
    )


def _decreasing_root(function: Callable[[float], float], target: float) -> float:
    low, high = 0.0, 1.0
    for _ in range(80):
        middle = (low + high) / 2.0
        if function(middle) > target:
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def clopper_pearson(successes: int, total: int, *, confidence_level: float = 0.95) -> tuple[float, float]:
    if total < 1 or not 0 <= successes <= total or not 0.0 < confidence_level < 1.0:
        raise HarnessError("invalid exact-binomial interval inputs")
    tail = (1.0 - confidence_level) / 2.0
    lower = 0.0 if successes == 0 else _decreasing_root(
        lambda probability: _binomial_cdf(successes - 1, total, probability),
        1.0 - tail,
    )
    upper = 1.0 if successes == total else _decreasing_root(
        lambda probability: _binomial_cdf(successes, total, probability),
        tail,
    )
    return lower, upper


def audit_divergence_report(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    result = divergence_summary(records)
    lower, upper = clopper_pearson(
        result["divergent_prompt_count"], result["prompt_count"]
    )
    result.update(
        {
            "divergence_rate": result["divergent_prompt_count"] / result["prompt_count"],
            "clopper_pearson_95_lower": lower,
            "clopper_pearson_95_upper": upper,
            "primary_repetition": 1,
            "majority_r3_role": "pre-specified sensitivity only",
        }
    )
    return result


def sign_flip_pvalue(
    cluster_means: Iterable[float], *, draws: int = 10_000, seed: int = BOOTSTRAP_SEED
) -> float:
    values = [float(value) for value in cluster_means]
    if not values or any(value < -1.0 or value > 1.0 for value in values):
        raise HarnessError("sign-flip inputs must be non-empty and in [-1, 1]")
    observed = sum(values) / len(values)
    if len(values) <= 20:
        exceed = 0
        total = 1 << len(values)
        for mask in range(total):
            value = sum(item if mask & (1 << index) else -item for index, item in enumerate(values)) / len(values)
            exceed += value >= observed - 1e-15
        return exceed / total
    if draws < 1:
        raise HarnessError("sign-flip draws must be positive")
    generator = random.Random(seed)
    exceed = 0
    for _ in range(draws):
        value = sum(item if generator.randrange(2) else -item for item in values) / len(values)
        exceed += value >= observed
    return (exceed + 1.0) / (draws + 1.0)
