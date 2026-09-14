"""Strict 03.9 numeric-baseline to 03.10 harness metric adapter."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any, Mapping

from .common import HarnessError, load_json, require_sha256


BASELINE_THREE_NUMBERS = (
    "accuracy",
    "abstention_rate",
    "accuracy_non_abstained",
)
HARNESS_THREE_NUMBERS = (
    "accuracy_all",
    "abstention_rate",
    "accuracy_non_abstained",
)
BASELINE_COUNT_FIELDS = ("n", "correct", "abstentions", "non_abstained")
HARNESS_COUNT_FIELDS = (
    "total",
    "correct",
    "abstained",
    "non_abstained",
    "invalid",
)

_BASELINE_METRIC_FIELDS = frozenset(BASELINE_COUNT_FIELDS + BASELINE_THREE_NUMBERS)
_SUMMARY_POPULATIONS = frozenset(("all", "local_unseen", "local_seen", "normal"))
_CONDITIONS = frozenset(("numeric_global", "numeric_local"))
_CLUSTER_METADATA_FIELDS = frozenset(
    ("condition", "physical_case_id", "independence_claim")
)


def _count(value: Any, *, field: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise HarnessError(f"03.9 metric {field} must be a non-negative integer")
    return value


def _ratio(value: Any, *, field: str, expected: float | None) -> float | None:
    if expected is None:
        if value is not None:
            raise HarnessError(f"03.9 metric {field} must be null for a zero denominator")
        return None
    if (
        isinstance(value, bool)
        or not isinstance(value, (int, float))
        or not math.isfinite(value)
        or value != expected
    ):
        raise HarnessError(
            f"03.9 metric {field} is inconsistent with its frozen numerator/denominator"
        )
    return value


def adapt_baseline_metric(source: Mapping[str, Any]) -> dict[str, int | float | None]:
    """Rename one valid-only 03.9 metric record without recomputing its values.

    The 03.9 evaluator fails on invalid inputs and writes only rows with ``valid=true``.
    Consequently its metric record has no invalid counter.  The adapter makes that
    contract explicit as ``invalid=0``; it never derives invalidity from abstentions or
    from a missing prediction.
    """

    keys = set(source)
    if keys != _BASELINE_METRIC_FIELDS:
        missing = sorted(_BASELINE_METRIC_FIELDS - keys)
        extra = sorted(str(key) for key in keys - _BASELINE_METRIC_FIELDS)
        raise HarnessError(
            f"03.9 metric fields do not match the frozen contract; missing={missing}, extra={extra}"
        )

    total = _count(source["n"], field="n")
    correct = _count(source["correct"], field="correct")
    abstained = _count(source["abstentions"], field="abstentions")
    non_abstained = _count(source["non_abstained"], field="non_abstained")
    if abstained > total or non_abstained != total - abstained:
        raise HarnessError("03.9 non_abstained must equal n - abstentions")
    if correct > non_abstained:
        raise HarnessError("03.9 correct cannot exceed non_abstained")

    accuracy_all = _ratio(
        source["accuracy"],
        field="accuracy",
        expected=correct / total if total else None,
    )
    abstention_rate = _ratio(
        source["abstention_rate"],
        field="abstention_rate",
        expected=abstained / total if total else None,
    )
    accuracy_non_abstained = _ratio(
        source["accuracy_non_abstained"],
        field="accuracy_non_abstained",
        expected=correct / non_abstained if non_abstained else None,
    )

    return {
        "total": total,
        "correct": correct,
        "abstained": abstained,
        "non_abstained": non_abstained,
        "invalid": 0,
        "accuracy_all": accuracy_all,
        "abstention_rate": abstention_rate,
        "accuracy_non_abstained": accuracy_non_abstained,
    }


def _adapt_cluster(source: Mapping[str, Any]) -> dict[str, Any]:
    expected_fields = _CLUSTER_METADATA_FIELDS | _BASELINE_METRIC_FIELDS
    if set(source) != expected_fields:
        raise HarnessError("03.9 cluster metric fields do not match the frozen contract")
    condition = source["condition"]
    case_id = source["physical_case_id"]
    if condition not in _CONDITIONS or not isinstance(case_id, str) or not case_id:
        raise HarnessError("03.9 cluster identity is invalid")
    if source["independence_claim"] is not False:
        raise HarnessError("03.9 cluster independence_claim must be false")
    metric = adapt_baseline_metric(
        {field: source[field] for field in _BASELINE_METRIC_FIELDS}
    )
    return {
        "condition": condition,
        "physical_case_id": case_id,
        "independence_claim": False,
        **metric,
    }


def adapt_baseline_metrics_document(source: Mapping[str, Any]) -> dict[str, Any]:
    """Validate and adapt every metric leaf in a frozen-shape 03.9 metrics document."""

    if source.get("schema_version") != 1:
        raise HarnessError("unsupported 03.9 metrics schema_version")
    if source.get("status") != "TECHNICAL_OUTPUT_NOT_A_PERFORMANCE_ESTIMATE":
        raise HarnessError("unexpected 03.9 metrics status")
    if source.get("statistical_unit") != "physical_case_id":
        raise HarnessError("unexpected 03.9 statistical unit")
    if source.get("independence_claim") is not False:
        raise HarnessError("03.9 independence_claim must be false")
    if source.get("three_numbers") != list(BASELINE_THREE_NUMBERS):
        raise HarnessError("03.9 three_numbers do not match the frozen contract")

    summary = source.get("summary")
    if not isinstance(summary, Mapping) or set(summary) != _CONDITIONS:
        raise HarnessError("03.9 summary requires numeric_global and numeric_local")
    adapted_summary: dict[str, dict[str, Any]] = {}
    for condition in sorted(_CONDITIONS):
        populations = summary[condition]
        if not isinstance(populations, Mapping) or set(populations) != _SUMMARY_POPULATIONS:
            raise HarnessError(f"03.9 summary populations are invalid for {condition}")
        adapted_summary[condition] = {}
        for population in sorted(_SUMMARY_POPULATIONS):
            metric = populations[population]
            if not isinstance(metric, Mapping):
                raise HarnessError(
                    f"03.9 summary metric is not an object for {condition}/{population}"
                )
            adapted_summary[condition][population] = adapt_baseline_metric(metric)

    clusters = source.get("clusters")
    if not isinstance(clusters, list) or any(not isinstance(item, Mapping) for item in clusters):
        raise HarnessError("03.9 clusters must be a list of metric records")
    adapted_clusters = [_adapt_cluster(item) for item in clusters]
    identities = [
        (item["condition"], item["physical_case_id"]) for item in adapted_clusters
    ]
    if len(identities) != len(set(identities)):
        raise HarnessError("03.9 cluster identities must be unique")

    result = dict(source)
    result["three_numbers"] = list(HARNESS_THREE_NUMBERS)
    result["summary"] = adapted_summary
    result["clusters"] = adapted_clusters
    result["metric_interface"] = {
        "contract": "phase03_9_baseline_to_phase03_10_harness_v1",
        "name_mapping": {
            "accuracy": "accuracy_all",
            "n": "total",
            "abstentions": "abstained",
        },
        "non_abstained": "preserved_and_checked_equal_to_total_minus_abstained",
        "invalid": "explicit_zero_from_03_9_valid_true_only_fail_closed_contract",
    }
    return result


def load_baseline_metrics(path: Path, *, expected_sha256: str) -> dict[str, Any]:
    """Read one 03.9 ``metrics.json`` and return the validated harness view."""

    require_sha256(path, expected_sha256, role="03.9 metrics.json")
    source = load_json(path)
    if not isinstance(source, Mapping):
        raise HarnessError("03.9 metrics document must be a JSON object")
    return adapt_baseline_metrics_document(source)
