"""Pre-specified R=3 aggregation for Phase B diagnostic outcomes."""

from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass
from typing import Any, Iterable

from .records import RunRecord


@dataclass(frozen=True)
class AggregatePrediction:
    agent_id: str
    condition: str
    physical_case_id: str
    parsed_output: dict[str, Any]
    repetition_outcomes: tuple[dict[str, Any], ...]


def aggregate_run_records(
    values: Iterable[RunRecord | dict[str, Any]], *, label_space: Iterable[str]
) -> list[AggregatePrediction]:
    """Aggregate exactly three repetitions; two equal valid labels are required."""
    labels = set(label_space)
    groups: dict[tuple[str, str, str], list[RunRecord]] = defaultdict(list)
    for value in values:
        record = value if isinstance(value, RunRecord) else RunRecord.from_dict(value)
        groups[(record.agent_id, record.condition, record.physical_case_id)].append(record)

    aggregates: list[AggregatePrediction] = []
    for (agent_id, condition, case_id), records in sorted(groups.items()):
        records.sort(key=lambda record: record.repetition)
        if [record.repetition for record in records] != [1, 2, 3]:
            raise ValueError(
                f"R=3 aggregation requires repetitions 1,2,3 exactly for "
                f"{agent_id}/{condition}/{case_id}"
            )
        if len({record.input_hash for record in records}) != 1:
            raise ValueError("repetitions for one aggregate must use the same input_hash")
        votes = Counter(
            parsed["predicted_label"]
            for parsed in (record.parsed_output for record in records)
            if not parsed.get("abstain") and parsed.get("predicted_label") in labels
        )
        winners = [label for label, count in votes.items() if count >= 2]
        if len(winners) == 1:
            parsed_output = {
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
        repetition_outcomes = tuple(
            {
                "repetition": record.repetition,
                "predicted_label": record.parsed_output.get("predicted_label"),
                "abstain": bool(record.parsed_output.get("abstain")),
                "parse_failure": record.parsed_output.get("reasoning_summary") == "parse_failure",
            }
            for record in records
        )
        aggregates.append(
            AggregatePrediction(
                agent_id=agent_id,
                condition=condition,
                physical_case_id=case_id,
                parsed_output=parsed_output,
                repetition_outcomes=repetition_outcomes,
            )
        )
    return aggregates
