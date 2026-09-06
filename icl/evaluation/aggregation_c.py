"""Condition C aggregation — R=3 majority voting over CRunRecords.

Mirrors the Phase B aggregation pattern (phase_b/evaluation/aggregation.py)
adapted for the Condition C record schema.  Groups CRunRecords by
physical_case_id (agent_id is always "central", condition always "C"),
validates that each group has exactly repetitions {1, 2, 3} with a
consistent prompt_sha256, then applies majority-≥2 voting.
"""

from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
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
    aggregation_rule: str = "majority_2_of_3"  # R7 P1-4

    def to_dict(self) -> dict[str, Any]:
        """Serialize to a plain dict (repetition_outcomes becomes a list)."""
        d = asdict(self)
        # asdict converts tuples to lists already, which is what we want.
        return d

    def to_jsonl_line(self) -> str:
        """Serialize to a single JSON line."""
        return json.dumps(self.to_dict(), ensure_ascii=False, separators=(",", ":"))


def aggregate_c_records(
    values: Iterable[CRunRecord | dict[str, Any]],
    *,
    label_space: Iterable[str] | None = None,
    expected_case_ids: set[str],
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

    # --- validate completeness (mandatory) ---
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
                aggregation_rule="majority_2_of_3",
            )
        )

    return aggregates


# ------------------------------------------------------------------
# Writer / manifest  (R7 review P1-4)
# ------------------------------------------------------------------

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_AGGREGATE_PATH = ROOT / "icl" / "inference" / "c_aggregate_records.jsonl"
DEFAULT_AGGREGATE_MANIFEST_PATH = (
    ROOT / "icl" / "full_evaluation" / "c_aggregate_manifest.json"
)


def write_c_aggregates(
    aggregates: list[CAggregatePrediction],
    output_path: Path | None = None,
) -> str:
    """Write aggregate records to JSONL and return file SHA-256."""
    path = output_path if output_path is not None else DEFAULT_AGGREGATE_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [agg.to_jsonl_line() for agg in aggregates]
    content = "\n".join(lines) + "\n"
    path.write_text(content, encoding="utf-8")
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_aggregate_manifest(
    aggregate_sha256: str,
    record_count: int,
    c_records_sha256: str,
    schedule_sha256: str,
    *,
    manifest_path: Path | None = None,
    schedule_ref_path: str = "icl/full_evaluation/c_schedule.json",
) -> None:
    """Write the aggregate predictions manifest (R7 P1-4)."""
    path = (
        manifest_path
        if manifest_path is not None
        else DEFAULT_AGGREGATE_MANIFEST_PATH
    )
    manifest = {
        "c_aggregate_records_sha256": aggregate_sha256,
        "record_count": record_count,
        "aggregation_rule": "majority_2_of_3",
        "source_c_records_sha256": c_records_sha256,
        "schedule_reference": {
            "path": schedule_ref_path,
            "sha256": schedule_sha256,
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def verify_aggregate_freeze(
    *,
    aggregate_path: Path | None = None,
    manifest_path: Path | None = None,
) -> dict[str, Any]:
    """Verify aggregate records against their manifest.  Fail-closed."""
    agg_path = aggregate_path if aggregate_path is not None else DEFAULT_AGGREGATE_PATH
    man_path = manifest_path if manifest_path is not None else DEFAULT_AGGREGATE_MANIFEST_PATH

    manifest = json.loads(man_path.read_text(encoding="utf-8"))

    _REQUIRED = {
        "c_aggregate_records_sha256", "record_count",
        "aggregation_rule", "source_c_records_sha256",
        "schedule_reference",
    }
    missing = _REQUIRED - set(manifest)
    if missing:
        raise RuntimeError(
            f"c_aggregate_manifest.json missing required keys: {sorted(missing)}"
        )

    expected_sha = manifest["c_aggregate_records_sha256"]
    actual_sha = hashlib.sha256(agg_path.read_bytes()).hexdigest()
    if actual_sha != expected_sha:
        raise RuntimeError(
            f"c_aggregate_records.jsonl hash mismatch: "
            f"expected {expected_sha[:16]}…, got {actual_sha[:16]}…"
        )

    raw_text = agg_path.read_text(encoding="utf-8")
    lines = [ln for ln in raw_text.strip().split("\n") if ln.strip()]
    if len(lines) != manifest["record_count"]:
        raise RuntimeError(
            f"aggregate record count mismatch: "
            f"expected {manifest['record_count']}, got {len(lines)}"
        )

    if manifest["aggregation_rule"] != "majority_2_of_3":
        raise RuntimeError(
            f"unexpected aggregation_rule: {manifest['aggregation_rule']!r}"
        )

    return {
        "c_aggregate_manifest_verified": True,
        "c_aggregate_records_sha256": actual_sha,
        "record_count": len(lines),
        "aggregation_rule": manifest["aggregation_rule"],
        "source_c_records_sha256": manifest["source_c_records_sha256"],
    }
