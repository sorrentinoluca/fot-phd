"""Marking of the scientific lots that sit between two canaries (§6.5 rev3, plan §10.5).

Protocol §6.5 rev3 settles the relation between the two sets, and this module reproduces
that hierarchy instead of collapsing it:

* ``primary_mask_request_ids`` -- **the primary mask**. Statistical plan §10.5: every
  scientific request completed inside the marked civil day, Europe/Rome, including the
  calls that follow the failed canary on the same day. This is the set that leaves the
  pre-specified sensitivity analysis.
* ``forensic_mask_request_ids`` -- **forensic only**. Protocol §6.5: every scientific
  request completed after the last canary PASS that precedes a marked (or stopped) canary
  and before that canary's first call. It documents the exposure interval; it does not
  decide the sensitivity analysis.
* ``union_descriptive_request_ids`` -- **descriptive only**, and labelled as such. §6.5
  rev3 forbids the union from silently replacing the plan's sensitivity mask, so it is
  published under its own name and never as *the* marked set.

Nothing is mutated: this is a read-only query over the ledger.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any, Iterable

from .common import HarnessError
from .ledger import (
    CANARY_MARKED_PREFIX, CANARY_PASS_PREFIX, CANARY_STOP_PREFIX, FINAL_CANARY_STAGE,
    FINAL_PASS_STAGES,
)

EQUIVALENT_SQL = """
-- Equivalent hand query (the events carry the canary request ids; the requests carry the
-- timestamps). Read-only.
SELECT r.request_id, r.stage, r.logical_id, r.completed_utc
  FROM requests r
 WHERE r.stage IN ('final_batch_r1','final_batch_r2','final_batch_r3')
   AND r.completed_utc IS NOT NULL
   AND (   r.completed_utc BETWEEN :last_pass_end AND :failed_canary_start
        OR date(r.completed_utc, '+2 hours') = :marked_civil_day )
 ORDER BY r.completed_utc;
""".strip()


def rome_day(moment: datetime) -> str:
    """Civil date in Europe/Rome. Without tzdata it refuses rather than guess.

    The civil day is the unit of both the canary barrier and the primary mask, so an
    approximate answer is worse than none: a fixed-date fallback puts the DST switch on
    the wrong day in most years (review rilievo B5). Install tzdata on the machine that
    runs the batch; ``pip install tzdata`` is enough where the OS database is missing.
    """
    moment = moment.astimezone(timezone.utc)
    try:
        from zoneinfo import ZoneInfo

        zone = ZoneInfo("Europe/Rome")
    except Exception as exc:
        raise HarnessError(
            "Europe/Rome civil day requires the IANA time-zone database; install tzdata "
            "before running the canary or the batch") from exc
    return moment.astimezone(zone).date().isoformat()


def _moment(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def canary_days(ledger) -> list[dict[str, Any]]:
    """Every recorded canary day with its verdict and its time span, in day order."""
    snapshot = ledger.snapshot()
    rows = {}
    for name in snapshot["events"]:
        for prefix, verdict in ((CANARY_PASS_PREFIX, "PASS"), (CANARY_MARKED_PREFIX, "MARKED")):
            if name.startswith(prefix):
                detail = ledger.event(name) or {}
                day = name[len(prefix):]
                moments = []
                for request_id in detail.get("request_ids", []):
                    request = ledger.request(request_id)
                    moment = _moment((request or {}).get("completed_utc"))
                    if moment is not None:
                        moments.append(moment)
                rows[day] = {
                    "day": day, "verdict": verdict,
                    "day_index": detail.get("day_index"),
                    "request_ids": detail.get("request_ids", []),
                    "identity": detail.get("identity"),
                    "first_utc": min(moments).isoformat() if moments else None,
                    "last_utc": max(moments).isoformat() if moments else None,
                }
    for name in snapshot["events"]:
        if name.startswith(CANARY_STOP_PREFIX):
            detail = ledger.event(name) or {}
            day = str(detail.get("day") or "")
            entry = rows.setdefault(day, {"day": day, "request_ids": [], "day_index": None,
                                          "first_utc": None, "last_utc": None, "identity": None})
            entry["verdict"] = "STOP"
            entry["stop_event"] = name
    return [rows[day] for day in sorted(rows)]


def scientific_requests(ledger) -> list[dict[str, Any]]:
    """Every terminal scientific request of the three passes, with its timestamp."""
    rows = []
    for stage in FINAL_PASS_STAGES:
        binding = None
        try:
            binding = ledger.binding(stage)
        except Exception:
            continue
        for spec in binding["requests"]:
            for attempt in ledger.attempts(stage, spec["logical_id"]):
                if attempt["completed_utc"]:
                    rows.append({"request_id": attempt["request_id"], "stage": stage,
                                 "logical_id": attempt["logical_id"],
                                 "status": attempt["status"],
                                 "completed_utc": attempt["completed_utc"]})
    rows.sort(key=lambda row: (row["completed_utc"], row["request_id"]))
    return rows


def marking(ledger) -> dict[str, Any]:
    """The marked set, its two components and the evidence each one rests on."""
    days = canary_days(ledger)
    requests = scientific_requests(ledger)
    failed = [day for day in days if day["verdict"] in {"MARKED", "STOP"}]
    intervals: list[dict[str, Any]] = []
    interval_ids: set[str] = set()
    day_ids: set[str] = set()
    for entry in failed:
        previous = [row for row in days
                    if row["verdict"] == "PASS" and row["day"] < entry["day"]]
        start = _moment(previous[-1]["last_utc"]) if previous else None
        end = _moment(entry["first_utc"])
        selected = []
        for row in requests:
            moment = _moment(row["completed_utc"])
            if end is not None and moment > end:
                continue
            if start is not None and moment <= start:
                continue
            selected.append(row["request_id"])
        intervals.append({
            "canary_day": entry["day"], "verdict": entry["verdict"],
            "after_last_passed_canary": previous[-1]["day"] if previous else None,
            "window_start_utc": start.isoformat() if start else None,
            "window_end_utc": end.isoformat() if end else None,
            "request_ids": selected,
        })
        interval_ids.update(selected)
        for row in requests:
            if rome_day(_moment(row["completed_utc"])) == entry["day"]:
                day_ids.add(row["request_id"])
    primary = sorted(day_ids)
    forensic = sorted(interval_ids)
    union = sorted(interval_ids | day_ids)
    return {
        "artifact_version": "MARCATURA_CANARY_7_4_2",
        "rule": "primary mask = marked civil day (plan §10.5); forensic mask = interval "
                "between the last PASS and the failed canary (§6.5); their union is "
                "descriptive only and never replaces the plan's sensitivity mask",
        "canary_days": days,
        "failed_canaries": [entry["day"] for entry in failed],
        "intervals": intervals,
        "primary_mask_request_ids": primary,
        "primary_mask_requests": len(primary),
        "primary_mask_source": "PIANO_STATISTICO.md §10.5 — marked civil day",
        "forensic_mask_request_ids": forensic,
        "forensic_mask_requests": len(forensic),
        "forensic_mask_source": "PROTOCOLLO_FINALE_CANDIDATE.md §6.5 — exposure interval",
        "forensic_only_request_ids": sorted(interval_ids - day_ids),
        "primary_only_request_ids": sorted(day_ids - interval_ids),
        "union_descriptive_request_ids": union,
        "union_descriptive_requests": len(union),
        "union_scope": "descriptive; §6.5 rev3 forbids using it as the sensitivity mask",
        "scientific_requests": len(requests),
        "derivation": "read-only over the ledger; terminal records are never rewritten",
        "equivalent_sql": EQUIVALENT_SQL,
    }
