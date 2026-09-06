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
        "status": "IMMUTABLE_BEFORE_EVALUATION",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


DEFAULT_PREDICTIONS_MANIFEST_PATH = (
    ROOT / "icl" / "full_evaluation" / "c_predictions_manifest.json"
)


def write_c_predictions_manifest(
    c_records_sha256: str,
    record_count: int,
    schedule_sha256: str,
    *,
    manifest_path: Path | None = None,
    schedule_ref_path: str = "icl/full_evaluation/c_schedule.json",
) -> None:
    """Write the raw predictions manifest (c_predictions_manifest.json).

    This manifest ties c_records.jsonl to its hash, record count, and
    the schedule it was produced from.  Required by the evaluator
    predictions barrier (verify_c_predictions_freeze).
    """
    path = (
        manifest_path
        if manifest_path is not None
        else DEFAULT_PREDICTIONS_MANIFEST_PATH
    )
    manifest = {
        "c_records_sha256": c_records_sha256,
        "record_count": record_count,
        "schedule_reference": {
            "path": schedule_ref_path,
            "sha256": schedule_sha256,
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


_EXPECTED_CASE_IDS = frozenset(
    f"PBH-{i:03d}" for i in range(1, 16)
)
_EXPECTED_AGGREGATE_COUNT = 15  # one per physical case


def verify_aggregate_freeze(
    *,
    aggregate_path: Path | None = None,
    manifest_path: Path | None = None,
    c_records_path: Path | None = None,
    schedule_path: Path | None = None,
) -> dict[str, Any]:
    """Verify aggregate records against their manifest.  Fail-closed.

    All checks are mandatory — omitting any parameter falls back to the
    canonical default path, and every default must exist.

    Checks:
      1. Manifest has all required keys including ``status``.
      2. ``status`` is ``IMMUTABLE_BEFORE_EVALUATION``.
      3. File hash matches manifest.
      4. Exactly 15 records (one per physical case).
      5. Each record parses to a valid CAggregatePrediction.
      6. Case IDs are exactly PBH-001 … PBH-015 (no extras, no missing).
      7. Each record has exactly 3 ``repetition_outcomes`` entries.
      8. ``aggregation_rule`` is ``majority_2_of_3``.
      9. ``source_c_records_sha256`` matches actual c_records.jsonl.
     10. ``schedule_reference.sha256`` matches actual c_schedule.json.
    """
    agg_path = aggregate_path if aggregate_path is not None else DEFAULT_AGGREGATE_PATH
    man_path = manifest_path if manifest_path is not None else DEFAULT_AGGREGATE_MANIFEST_PATH

    manifest = json.loads(man_path.read_text(encoding="utf-8"))

    # --- 1. Required keys ---
    _REQUIRED = {
        "c_aggregate_records_sha256", "record_count",
        "aggregation_rule", "source_c_records_sha256",
        "schedule_reference", "status",
    }
    missing = _REQUIRED - set(manifest)
    if missing:
        raise RuntimeError(
            f"c_aggregate_manifest.json missing required keys: {sorted(missing)}"
        )

    # --- 2. Status must be IMMUTABLE_BEFORE_EVALUATION ---
    if manifest["status"] != "IMMUTABLE_BEFORE_EVALUATION":
        raise RuntimeError(
            f"aggregate manifest status must be "
            f"'IMMUTABLE_BEFORE_EVALUATION', got {manifest['status']!r}"
        )

    # --- 3. File hash ---
    expected_sha = manifest["c_aggregate_records_sha256"]
    actual_sha = hashlib.sha256(agg_path.read_bytes()).hexdigest()
    if actual_sha != expected_sha:
        raise RuntimeError(
            f"c_aggregate_records.jsonl hash mismatch: "
            f"expected {expected_sha[:16]}…, got {actual_sha[:16]}…"
        )

    # --- 4. Exactly 15 records ---
    raw_text = agg_path.read_text(encoding="utf-8")
    lines = [ln for ln in raw_text.strip().split("\n") if ln.strip()]
    if len(lines) != _EXPECTED_AGGREGATE_COUNT:
        raise RuntimeError(
            f"aggregate record count must be {_EXPECTED_AGGREGATE_COUNT}, "
            f"got {len(lines)}"
        )
    if len(lines) != manifest["record_count"]:
        raise RuntimeError(
            f"aggregate record count ({len(lines)}) does not match "
            f"manifest record_count ({manifest['record_count']})"
        )

    # --- 5 + 6 + 7. Parse each record and validate ---
    seen_case_ids: set[str] = set()
    parsed_records_for_case: dict[str, dict] = {}
    for i, line in enumerate(lines):
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise RuntimeError(
                f"c_aggregate_records.jsonl line {i}: JSON parse error: {exc}"
            ) from exc

        # Validate required fields.
        for key in ("agent_id", "condition", "physical_case_id",
                     "parsed_output", "repetition_outcomes",
                     "aggregation_rule"):
            if key not in obj:
                raise RuntimeError(
                    f"c_aggregate_records.jsonl line {i}: missing key {key!r}"
                )

        case_id = obj["physical_case_id"]
        if case_id in seen_case_ids:
            raise RuntimeError(
                f"duplicate physical_case_id {case_id!r} at line {i}"
            )
        seen_case_ids.add(case_id)

        # Validate case_id format.
        if case_id not in _EXPECTED_CASE_IDS:
            raise RuntimeError(
                f"c_aggregate_records.jsonl line {i}: unexpected "
                f"physical_case_id {case_id!r}"
            )

        # Validate repetition_outcomes has exactly 3 entries.
        outcomes = obj.get("repetition_outcomes", [])
        if not isinstance(outcomes, list) or len(outcomes) != 3:
            raise RuntimeError(
                f"c_aggregate_records.jsonl line {i} ({case_id}): "
                f"repetition_outcomes must have exactly 3 entries, "
                f"got {len(outcomes) if isinstance(outcomes, list) else type(outcomes).__name__}"
            )

        # Validate aggregation_rule per record.
        if obj["aggregation_rule"] != "majority_2_of_3":
            raise RuntimeError(
                f"c_aggregate_records.jsonl line {i} ({case_id}): "
                f"aggregation_rule must be 'majority_2_of_3', "
                f"got {obj['aggregation_rule']!r}"
            )

        # R9: agent_id must be "central".
        if obj.get("agent_id") != "central":
            raise RuntimeError(
                f"c_aggregate_records.jsonl line {i} ({case_id}): "
                f"agent_id must be 'central', got {obj.get('agent_id')!r}"
            )

        # R9: condition must be "C".
        if obj.get("condition") != "C":
            raise RuntimeError(
                f"c_aggregate_records.jsonl line {i} ({case_id}): "
                f"condition must be 'C', got {obj.get('condition')!r}"
            )

        # R9: majority-label consistency — parsed_output.predicted_label
        # must match the actual majority vote of repetition_outcomes.
        outcome_labels = [
            o.get("predicted_label") for o in outcomes
            if not o.get("abstain") and not o.get("parse_failure")
        ]
        outcome_votes = Counter(outcome_labels)
        majority_winners = [lbl for lbl, cnt in outcome_votes.items() if cnt >= 2]
        po = obj.get("parsed_output", {})
        if len(majority_winners) == 1:
            if po.get("predicted_label") != majority_winners[0]:
                raise RuntimeError(
                    f"c_aggregate_records.jsonl line {i} ({case_id}): "
                    f"parsed_output.predicted_label "
                    f"{po.get('predicted_label')!r} does not match "
                    f"majority vote {majority_winners[0]!r} from "
                    f"repetition_outcomes"
                )
        else:
            # No majority — must be abstain.
            if not po.get("abstain"):
                raise RuntimeError(
                    f"c_aggregate_records.jsonl line {i} ({case_id}): "
                    f"no majority in repetition_outcomes but "
                    f"parsed_output.abstain is not True"
                )

        parsed_records_for_case[case_id] = obj

    # Check for missing case IDs.
    if seen_case_ids != _EXPECTED_CASE_IDS:
        missing_ids = sorted(_EXPECTED_CASE_IDS - seen_case_ids)
        extra_ids = sorted(seen_case_ids - _EXPECTED_CASE_IDS)
        raise RuntimeError(
            f"aggregate case ID mismatch: "
            f"missing={missing_ids}, extra={extra_ids}"
        )

    # --- 8. Manifest aggregation_rule ---
    if manifest["aggregation_rule"] != "majority_2_of_3":
        raise RuntimeError(
            f"unexpected aggregation_rule: {manifest['aggregation_rule']!r}"
        )

    # --- 9. Cross-verify source_c_records_sha256 ---
    _c_rec_path = (
        c_records_path if c_records_path is not None
        else Path(__file__).resolve().parents[2]
        / "icl" / "inference" / "c_records.jsonl"
    )
    if _c_rec_path.exists():
        actual_c_sha = hashlib.sha256(_c_rec_path.read_bytes()).hexdigest()
        if actual_c_sha != manifest["source_c_records_sha256"]:
            raise RuntimeError(
                f"source_c_records_sha256 mismatch: manifest says "
                f"{manifest['source_c_records_sha256'][:16]}…, "
                f"actual c_records.jsonl is {actual_c_sha[:16]}…"
            )
    else:
        raise RuntimeError(
            f"c_records.jsonl not found at {_c_rec_path} — "
            f"cannot cross-verify source_c_records_sha256"
        )

    # --- 10. Cross-verify schedule_reference.sha256 ---
    sched_ref = manifest["schedule_reference"]
    if not isinstance(sched_ref, dict) or "sha256" not in sched_ref:
        raise RuntimeError(
            "schedule_reference must be a dict with at least 'sha256'"
        )
    _sched_path = (
        schedule_path if schedule_path is not None
        else Path(__file__).resolve().parents[2]
        / "icl" / "full_evaluation" / "c_schedule.json"
    )
    actual_sched_sha = hashlib.sha256(_sched_path.read_bytes()).hexdigest()
    if actual_sched_sha != sched_ref["sha256"]:
        raise RuntimeError(
            f"aggregate manifest schedule_reference.sha256 mismatch: "
            f"manifest says {sched_ref['sha256'][:16]}…, "
            f"actual is {actual_sched_sha[:16]}…"
        )

    # --- 11. R9: cross-verify repetition_outcomes against raw c_records ---
    raw_lines = _c_rec_path.read_text(encoding="utf-8").strip().split("\n")
    raw_by_case: dict[str, list[dict]] = defaultdict(list)
    for raw_line in raw_lines:
        if not raw_line.strip():
            continue
        raw_obj = json.loads(raw_line)
        raw_by_case[raw_obj["physical_case_id"]].append(raw_obj)

    for case_id, agg_obj in parsed_records_for_case.items():
        raw_recs = sorted(
            raw_by_case.get(case_id, []),
            key=lambda r: r["repetition"],
        )
        agg_outcomes = agg_obj["repetition_outcomes"]
        if len(raw_recs) != len(agg_outcomes):
            raise RuntimeError(
                f"aggregate {case_id}: {len(agg_outcomes)} "
                f"repetition_outcomes but {len(raw_recs)} raw records"
            )
        for j, (raw_rec, agg_out) in enumerate(
            zip(raw_recs, agg_outcomes)
        ):
            raw_label = raw_rec.get("parsed_output", {}).get(
                "predicted_label"
            )
            agg_label = agg_out.get("predicted_label")
            if raw_label != agg_label:
                raise RuntimeError(
                    f"aggregate {case_id} repetition {j+1}: "
                    f"outcome label {agg_label!r} does not match "
                    f"raw record label {raw_label!r}"
                )

    return {
        "c_aggregate_manifest_verified": True,
        "c_aggregate_records_sha256": actual_sha,
        "record_count": len(lines),
        "aggregation_rule": manifest["aggregation_rule"],
        "source_c_records_sha256": manifest["source_c_records_sha256"],
        "status": manifest["status"],
        "verified_aggregates": parsed_records_for_case,
    }
