"""Create-once canary expectations and behavior-change checks."""

from __future__ import annotations

from datetime import datetime, timezone
import json
import os
from pathlib import Path
from typing import Any, Iterable

from .common import HarnessError, canonical_json, sha256_text


def freeze_expectations(path: Path, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = list(records)
    if len(rows) != 10 or len({row["prompt_id"] for row in rows}) != 10:
        raise HarnessError("canary freeze requires ten unique prompt results")
    expected = []
    for row in rows:
        parsed = row.get("parsed_output")
        raw = row.get("raw_response")
        if not isinstance(parsed, dict) or not isinstance(raw, str):
            raise HarnessError("canary result requires parsed_output and raw_response")
        expected.append(
            {
                "prompt_id": row["prompt_id"],
                "abstain": parsed.get("abstain"),
                "predicted_label": parsed.get("predicted_label"),
                "raw_response_sha256": sha256_text(raw),
            }
        )
    artifact = {
        "artifact_version": "1",
        "status": "FROZEN_AT_FIRST_CANARY_RUN",
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "expectations": sorted(expected, key=lambda row: row["prompt_id"]),
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
    try:
        os.write(descriptor, (json.dumps(artifact, indent=2, ensure_ascii=False) + "\n").encode("utf-8"))
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    return artifact


def compare_run(expectation_path: Path, records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    expected = json.loads(expectation_path.read_text(encoding="utf-8"))
    expected_by_id = {row["prompt_id"]: row for row in expected["expectations"]}
    observed = list(records)
    if set(expected_by_id) != {row.get("prompt_id") for row in observed}:
        raise HarnessError("canary run does not match the frozen prompt set")
    details = []
    for row in observed:
        parsed = row.get("parsed_output")
        if not isinstance(parsed, dict) or not isinstance(row.get("raw_response"), str):
            raise HarnessError("invalid canary observation")
        reference = expected_by_id[row["prompt_id"]]
        pair_changed = (parsed.get("abstain"), parsed.get("predicted_label")) != (
            reference["abstain"],
            reference["predicted_label"],
        )
        raw_changed = sha256_text(row["raw_response"]) != reference["raw_response_sha256"]
        details.append(
            {"prompt_id": row["prompt_id"], "behavior_changed": pair_changed, "raw_changed": raw_changed}
        )
    return {
        "marked_day": any(row["behavior_changed"] for row in details),
        "behavior_changes": sum(row["behavior_changed"] for row in details),
        "raw_hash_changes": sum(row["raw_changed"] for row in details),
        "details": details,
        "forensic_note": "raw hash changes do not decide behavioral variation",
        "comparison_sha256": sha256_text(canonical_json(details)),
    }


def suspension_required(
    daily_reports: Iterable[dict[str, Any]], *, returned_model_changed: bool
) -> dict[str, Any]:
    marked_days = sum(report.get("marked_day") is True for report in daily_reports)
    return {
        "marked_days": marked_days,
        "returned_model_changed": returned_model_changed,
        "suspend": bool(marked_days >= 2 or returned_model_changed),
        "rule": "suspend after two marked days or one returned-model ID change",
    }

