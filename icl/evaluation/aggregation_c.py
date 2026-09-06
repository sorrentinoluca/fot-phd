"""Condition C aggregation — R=3 majority voting over CRunRecords.

Mirrors the Phase B aggregation pattern (phase_b/evaluation/aggregation.py)
adapted for the Condition C record schema.  Groups CRunRecords by
physical_case_id (agent_id is always "central", condition always "C"),
validates that each group has exactly repetitions {1, 2, 3} with a
consistent prompt_sha256, then applies majority-≥2 voting.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Iterable

from icl.runner.records_c import CRunRecord, LABEL_SPACE as _RECORD_LABEL_SPACE


@dataclass(frozen=True)
class CAggregatePrediction:
    """Aggregated prediction for one physical case under Condition C."""

    agent_id: str                   # always "central"
    condition: str                  # always "C"
    physical_case_id: str           # PBH-XXX
    parsed_output: dict[str, Any]   # majority-voted prediction
    repetition_outcomes: tuple[dict[str, Any], ...]  # per-repetition detail


def aggregate_c_records(
    values: Iterable[CRunRecord | dict[str, Any]],
    *,
    label_space: Iterable[str] | None = None,
    expected_case_ids: set[str] | None = None,
) -> list[CAggregatePrediction]:
    """Aggregate Condition C run records via R=3 majority voting.

    Parameters
    ----------
    values:
        CRunRecord instances or raw dicts (deserialized JSONL lines).
    label_space:
        Valid label set.  Defaults to the canonical Condition C labels.
    expected_case_ids:
        When provided, the set of physical_case_ids in the input must
        match exactly (fail-fast on incomplete or extraneous data).

    Returns
    -------
    Sorted list of CAggregatePrediction, one per physical_case_id,
    ordered by physical_case_id ascending.

    Raises
    ------
    ValueError
        If any group does not have exactly repetitions {1, 2, 3}, if
        repetitions within a group have inconsistent prompt_sha256,
        or if *expected_case_ids* is given and the actual set differs.
    """
    labels = set(label_space) if label_space is not None else set(_RECORD_LABEL_SPACE)

    # --- group by physical_case_id ---
    groups: dict[str, list[CRunRecord]] = defaultdict(list)
    for value in values:
        record = (
            value
            if isinstance(value, CRunRecord)
            else CRunRecord.from_dict(value)
        )
        groups[record.physical_case_id].append(record)

    # --- validate completeness (when expected set provided) ---
    if expected_case_ids is not None:
        actual_ids = set(groups)
        if actual_ids != expected_case_ids:
            missing = sorted(expected_case_ids - actual_ids)
            extra = sorted(actual_ids - expected_case_ids)
            raise ValueError(
                f"aggregate completeness check failed: "
                f"missing={missing}, extra={extra}"
            )

    # --- aggregate each group ---
    aggregates: list[CAggregatePrediction] = []

    for case_id in sorted(groups):
        records = groups[case_id]
        records.sort(key=lambda r: r.repetition)

        # Validate repetition completeness.
        reps = [r.repetition for r in records]
        if reps != [1, 2, 3]:
            raise ValueError(
                f"aggregate for {case_id}: expected repetitions [1, 2, 3], "
                f"got {reps}"
            )

        # Validate prompt_sha256 consistency across repetitions.
        hashes = {r.prompt_sha256 for r in records}
        if len(hashes) != 1:
            raise ValueError(
                f"repetitions for {case_id} must use the same "
                f"prompt_sha256, got {sorted(hashes)}"
            )

        # Majority voting: count non-abstaining, valid predicted_labels.
        # Only valid=True records contribute votes (R5 review point 13).
        votes: Counter[str] = Counter(
            r.parsed_output["predicted_label"]
            for r in records
            if r.valid
            and not r.parsed_output.get("abstain")
            and r.parsed_output.get("predicted_label") in labels
        )

        winners = [lbl for lbl, count in votes.items() if count >= 2]

        if len(winners) == 1:
            parsed_output: dict[str, Any] = {
                "predicted_label": winners[0],
                "abstain": False,
                "used_insight_ids": [],
                "reasoning_summary": "aggregate_majority_2_of_3",
            }
        else:
            parsed_output = {
                "predicted_label": None,
                "abstain": True,
                "used_insight_ids": [],
                "reasoning_summary": "aggregate_no_label_majority",
            }

        # Per-repetition detail.
        repetition_outcomes = tuple(
            {
                "repetition": r.repetition,
                "predicted_label": r.parsed_output.get("predicted_label"),
                "abstain": bool(r.parsed_output.get("abstain")),
                "parse_failure": (
                    r.parsed_output.get("reasoning_summary") == "parse_failure"
                ),
            }
            for r in records
        )

        aggregates.append(
            CAggregatePrediction(
                agent_id="central",
                condition="C",
                physical_case_id=case_id,
                parsed_output=parsed_output,
                repetition_outcomes=repetition_outcomes,
            )
        )

    return aggregates
