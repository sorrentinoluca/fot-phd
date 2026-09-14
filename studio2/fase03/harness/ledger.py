"""Persistent, process-safe accounting for every Phase 03 pilot request.

An INTENT row is committed before transport starts and counts permanently, even
after a crash.  The SQLite file must be an absolute, shared path so changing the
checkout, results directory, runner, or producer cannot reset the budget.
"""

from __future__ import annotations

from contextlib import closing, contextmanager
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sqlite3
from typing import Any, Iterable

from .common import HarnessError, canonical_json


HASH = re.compile(r"^[0-9a-f]{64}$")
STAGES = {
    "producer_conformity",
    "producer_remediation",
    "alternate_conformity",
    "budget_probe",
    "stability_gate",
}
BASE_LIMITS = {
    "producer_conformity": 8,
    "producer_remediation": 8,
    "alternate_conformity": 8,
    "budget_probe": 9,
    "stability_gate": 120,
}


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


class PilotLedger:
    """Single source of truth for cumulative request and reserve accounting."""

    def __init__(self, path: Path, *, pilot_id: str) -> None:
        if not path.is_absolute():
            raise HarnessError("pilot ledger path must be absolute and shared across worktrees")
        if not re.fullmatch(r"[A-Za-z0-9_.-]{8,120}", pilot_id):
            raise HarnessError("invalid pilot_id")
        self.path = path
        self.pilot_id = pilot_id
        path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as connection:
            connection.executescript(
                """
                PRAGMA journal_mode=WAL;
                PRAGMA synchronous=FULL;
                CREATE TABLE IF NOT EXISTS requests (
                    pilot_id TEXT NOT NULL,
                    request_id TEXT NOT NULL,
                    logical_id TEXT NOT NULL,
                    model TEXT NOT NULL,
                    producer TEXT NOT NULL,
                    stage TEXT NOT NULL,
                    stage_run TEXT NOT NULL,
                    quota_kind TEXT NOT NULL,
                    retry_of TEXT,
                    status TEXT NOT NULL,
                    intent_utc TEXT NOT NULL,
                    completed_utc TEXT,
                    prompt_tokens INTEGER,
                    completion_tokens INTEGER,
                    total_tokens INTEGER,
                    latency_ms REAL,
                    proof_sha256 TEXT,
                    detail_json TEXT,
                    PRIMARY KEY (pilot_id, request_id)
                );
                CREATE UNIQUE INDEX IF NOT EXISTS request_logical_once
                    ON requests(pilot_id, logical_id, quota_kind, stage_run);
                CREATE TABLE IF NOT EXISTS events (
                    pilot_id TEXT NOT NULL,
                    event TEXT NOT NULL,
                    created_utc TEXT NOT NULL,
                    artifact_sha256 TEXT NOT NULL,
                    detail_json TEXT NOT NULL,
                    PRIMARY KEY (pilot_id, event)
                );
                """
            )

    @contextmanager
    def _transaction(self):
        connection = self._connect()
        try:
            connection.execute("BEGIN IMMEDIATE")
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path, timeout=30.0)
        connection.row_factory = sqlite3.Row
        return connection

    def _rows(self, connection: sqlite3.Connection) -> list[sqlite3.Row]:
        return list(
            connection.execute(
                "SELECT * FROM requests WHERE pilot_id=? ORDER BY intent_utc, request_id",
                (self.pilot_id,),
            )
        )

    def _events(self, connection: sqlite3.Connection) -> dict[str, sqlite3.Row]:
        return {
            row["event"]: row
            for row in connection.execute(
                "SELECT * FROM events WHERE pilot_id=?", (self.pilot_id,)
            )
        }

    @staticmethod
    def _require_hash(value: str, role: str) -> None:
        if not HASH.fullmatch(value):
            raise HarnessError(f"{role} must be a lowercase SHA-256")

    def record_event(self, event: str, *, artifact_sha256: str, detail: dict[str, Any]) -> None:
        self._require_hash(artifact_sha256, "event artifact")
        with self._transaction() as connection:
            try:
                connection.execute(
                    "INSERT INTO events VALUES (?,?,?,?,?)",
                    (self.pilot_id, event, _utc_now(), artifact_sha256, canonical_json(detail)),
                )
            except sqlite3.IntegrityError as exc:
                raise HarnessError(f"event is create-once: {event}") from exc

    def authorize_remediation(
        self, *, diff_sha256: str, approval_sha256: str, template_sha256: str
    ) -> None:
        for value, role in (
            (diff_sha256, "remediation diff"),
            (approval_sha256, "author approval"),
            (template_sha256, "remediated template"),
        ):
            self._require_hash(value, role)
        with closing(self._connect()) as connection:
            rows = self._rows(connection)
            events = self._events(connection)
            if any(row["stage"] in {"budget_probe", "stability_gate"} for row in rows):
                raise HarnessError("remediation is forbidden after probe or gate start")
            outcome = events.get("outcome:producer_conformity")
            if outcome is None or json.loads(outcome["detail_json"])["outcome"] != "FAIL":
                raise HarnessError("remediation requires a recorded failed conformity stage")
        self.record_event(
            "remediation_authorized",
            artifact_sha256=approval_sha256,
            detail={"diff_sha256": diff_sha256, "template_sha256": template_sha256},
        )

    def waive_remediation(self, *, approval_sha256: str) -> None:
        """Explicitly close remediation before spending transport calls 8..15."""
        self.record_event(
            "remediation_waived",
            artifact_sha256=approval_sha256,
            detail={"effect": "no later producer remediation is admissible"},
        )

    def record_stage_outcome(self, stage: str, *, outcome: str, artifact_sha256: str) -> None:
        if stage not in {
            "producer_conformity",
            "producer_remediation",
            "alternate_conformity",
            "budget_probe",
        }:
            raise HarnessError("unsupported stage outcome")
        if outcome not in {"PASS", "FAIL", "BLOCKED"}:
            raise HarnessError("unsupported stage outcome value")
        with closing(self._connect()) as connection:
            rows = [row for row in self._rows(connection) if row["stage"] == stage]
        if stage in {"producer_conformity", "alternate_conformity"}:
            base = sum(row["quota_kind"] == "base" for row in rows)
            if base != 8:
                raise HarnessError(f"{stage} outcome requires exactly 8 base requests")
        if stage == "producer_remediation":
            remediation = sum(row["quota_kind"] == "remediation" for row in rows)
            if remediation != 8:
                raise HarnessError("producer_remediation outcome requires exactly 8 remediation requests")
        if stage == "budget_probe":
            base = sum(row["quota_kind"] == "base" for row in rows)
            if base not in {3, 6, 9}:
                raise HarnessError("budget probe outcome requires 3, 6 or 9 base requests")
        if any(row["status"] == "INTENT" for row in rows):
            raise HarnessError("stage outcome cannot hide unresolved request intents")
        self.record_event(
            f"outcome:{stage}", artifact_sha256=artifact_sha256, detail={"outcome": outcome}
        )

    def _insert_intent(
        self,
        connection: sqlite3.Connection,
        *,
        request_id: str,
        logical_id: str,
        model: str,
        producer: str,
        stage: str,
        stage_run: str,
        quota_kind: str,
        retry_of: str | None,
    ) -> None:
        if stage not in STAGES or quota_kind not in {"base", "remediation", "transport"}:
            raise HarnessError("invalid stage or quota kind")
        if not all(isinstance(value, str) and value.strip() for value in (
            request_id, logical_id, model, producer, stage_run
        )):
            raise HarnessError("request identity fields must be non-empty")
        rows = self._rows(connection)
        events = self._events(connection)
        total_after = len(rows) + 1
        if total_after > 200:
            raise HarnessError("pilot cumulative hard stop 200 reached")

        alternate_used = stage == "alternate_conformity" or any(
            row["stage"] == "alternate_conformity" for row in rows
        )
        planned_max = 160 if alternate_used else 152
        if total_after > planned_max:
            raise HarnessError(f"planned request maximum {planned_max} reached before hard stop 200")

        if stage == "producer_remediation":
            if "remediation_authorized" not in events or "remediation_waived" in events:
                raise HarnessError("producer remediation lacks the required written authorization")
            if any(row["stage"] in {"budget_probe", "stability_gate"} for row in rows):
                raise HarnessError("producer remediation is forbidden after probe or gate")
            if quota_kind == "base":
                raise HarnessError("producer remediation requests must use remediation quota")
        elif quota_kind == "remediation":
            raise HarnessError("remediation quota is exclusive to producer_remediation")

        if stage in {"producer_conformity", "alternate_conformity"} and any(
            row["stage"] in {"budget_probe", "stability_gate"} for row in rows
        ):
            raise HarnessError("producer conformity must precede probe and gate")

        if stage == "budget_probe":
            if any(row["stage"] == "stability_gate" for row in rows):
                raise HarnessError("budget probe cannot run after the gate has started")
            source = "producer_remediation" if "remediation_authorized" in events else "producer_conformity"
            outcome = events.get(f"outcome:{source}")
            if outcome is None or json.loads(outcome["detail_json"])["outcome"] != "PASS":
                raise HarnessError("budget probe requires successful producer conformity/remediation")
        if stage == "stability_gate":
            outcome = events.get("outcome:budget_probe")
            if outcome is None or json.loads(outcome["detail_json"])["outcome"] != "PASS":
                raise HarnessError("stability gate requires a successful frozen budget probe")
            runs = {row["stage_run"] for row in rows if row["stage"] == "stability_gate"}
            if runs and runs != {stage_run}:
                raise HarnessError("the stability gate is create-once and cannot be repeated")
            if quota_kind != "base":
                raise HarnessError("the stability gate has no retry or remediation path")

        stage_base = sum(
            row["stage"] == stage and row["quota_kind"] == "base" for row in rows
        )
        if quota_kind == "base" and stage_base >= BASE_LIMITS[stage]:
            raise HarnessError(f"base request limit reached for {stage}")

        remediation_calls = sum(row["quota_kind"] == "remediation" for row in rows)
        transport_calls = sum(row["quota_kind"] == "transport" for row in rows)
        if quota_kind == "remediation":
            remediation_calls += 1
        if quota_kind == "transport":
            transport_calls += 1
            if stage == "stability_gate":
                raise HarnessError("gate requests are never repeatable")
        if remediation_calls not in range(0, 9):
            raise HarnessError("remediation requires at most one complete set of eight")
        if 8 * int(remediation_calls > 0) + transport_calls > 15:
            raise HarnessError("shared reserve constraint 8r+t<=15 violated")
        if stage == "budget_probe" and transport_calls > 7:
            raise HarnessError("budget-probe transport is capped at seven cumulative calls")
        if transport_calls > 7 and "remediation_waived" not in events:
            raise HarnessError("transport beyond seven requires explicit waiver of remediation")

        try:
            connection.execute(
                "INSERT INTO requests VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (
                    self.pilot_id, request_id, logical_id, model, producer, stage,
                    stage_run, quota_kind, retry_of, "INTENT", _utc_now(), None,
                    None, None, None, None, None, None,
                ),
            )
        except sqlite3.IntegrityError as exc:
            raise HarnessError("duplicate request or logical attempt") from exc

    def reserve_request(
        self,
        *,
        request_id: str,
        logical_id: str,
        model: str,
        producer: str,
        stage: str,
        stage_run: str,
    ) -> None:
        with self._transaction() as connection:
            self._insert_intent(
                connection,
                request_id=request_id,
                logical_id=logical_id,
                model=model,
                producer=producer,
                stage=stage,
                stage_run=stage_run,
                quota_kind="base",
                retry_of=None,
            )

    def reserve_transport_retry(
        self,
        *,
        request_id: str,
        logical_id: str,
        model: str,
        producer: str,
        stage: str,
        stage_run: str,
        retry_of: str,
    ) -> None:
        if stage == "budget_probe":
            raise HarnessError("budget-probe transport must reserve a complete triplet atomically")
        with self._transaction() as connection:
            original = connection.execute(
                "SELECT * FROM requests WHERE pilot_id=? AND request_id=?",
                (self.pilot_id, retry_of),
            ).fetchone()
            if original is None or original["status"] != "ZERO_TOKEN_PROVEN":
                raise HarnessError("transport retry requires documented zero-token proof")
            if original["stage"] != stage:
                raise HarnessError("transport retry must remain in the original stage")
            self._insert_intent(
                connection,
                request_id=request_id,
                logical_id=logical_id,
                model=model,
                producer=producer,
                stage=stage,
                stage_run=stage_run,
                quota_kind="transport",
                retry_of=retry_of,
            )

    def reserve_probe_transport_triplet(self, requests: Iterable[dict[str, str]]) -> None:
        values = list(requests)
        if len(values) != 3 or len({row.get("logical_id") for row in values}) != 3:
            raise HarnessError("probe transport retry requires exactly one complete A/B-LF/E-LF triplet")
        if {row.get("condition") for row in values} != {"A", "B-LF", "E-LF"}:
            raise HarnessError("probe transport retry must contain A, B-LF and E-LF")
        with self._transaction() as connection:
            for row in values:
                original = connection.execute(
                    "SELECT * FROM requests WHERE pilot_id=? AND request_id=?",
                    (self.pilot_id, row["retry_of"]),
                ).fetchone()
                if original is None or original["stage"] != "budget_probe" or original["status"] != "ZERO_TOKEN_PROVEN":
                    raise HarnessError("every repeated probe member requires zero-token proof")
            for row in values:
                self._insert_intent(
                    connection,
                    request_id=row["request_id"],
                    logical_id=row["logical_id"],
                    model=row["model"],
                    producer=row["producer"],
                    stage="budget_probe",
                    stage_run=row["stage_run"],
                    quota_kind="transport",
                    retry_of=row["retry_of"],
                )

    def reserve_remediation_request(self, **value: str) -> None:
        with self._transaction() as connection:
            self._insert_intent(
                connection, stage="producer_remediation", quota_kind="remediation",
                retry_of=None, **value
            )

    def complete_request(
        self,
        request_id: str,
        *,
        status: str,
        prompt_tokens: int | None = None,
        completion_tokens: int | None = None,
        total_tokens: int | None = None,
        latency_ms: float | None = None,
        proof_sha256: str | None = None,
        detail: dict[str, Any] | None = None,
    ) -> None:
        if status not in {"COMPLETED", "FAILED", "ZERO_TOKEN_PROVEN"}:
            raise HarnessError("invalid terminal request status")
        if status == "ZERO_TOKEN_PROVEN":
            if proof_sha256 is None:
                raise HarnessError("zero-token status requires a proof artifact hash")
            self._require_hash(proof_sha256, "zero-token proof")
            if completion_tokens not in {0, None} or total_tokens not in {0, None}:
                raise HarnessError("zero-token proof conflicts with positive token counts")
        values = (prompt_tokens, completion_tokens, total_tokens)
        if any(value is not None and (type(value) is not int or value < 0) for value in values):
            raise HarnessError("token counts must be non-negative integers or null")
        if total_tokens is not None and prompt_tokens is not None and completion_tokens is not None:
            if total_tokens != prompt_tokens + completion_tokens:
                raise HarnessError("inconsistent token accounting")
        with self._transaction() as connection:
            row = connection.execute(
                "SELECT status FROM requests WHERE pilot_id=? AND request_id=?",
                (self.pilot_id, request_id),
            ).fetchone()
            if row is None or row["status"] != "INTENT":
                raise HarnessError("request completion requires one unresolved intent")
            connection.execute(
                """UPDATE requests SET status=?,completed_utc=?,prompt_tokens=?,
                   completion_tokens=?,total_tokens=?,latency_ms=?,proof_sha256=?,detail_json=?
                   WHERE pilot_id=? AND request_id=?""",
                (
                    status, _utc_now(), prompt_tokens, completion_tokens, total_tokens,
                    latency_ms, proof_sha256,
                    None if detail is None else canonical_json(detail),
                    self.pilot_id, request_id,
                ),
            )

    def snapshot(self) -> dict[str, Any]:
        with closing(self._connect()) as connection:
            rows = self._rows(connection)
            events = self._events(connection)
        by_stage = {stage: sum(row["stage"] == stage for row in rows) for stage in sorted(STAGES)}
        remediation = sum(row["quota_kind"] == "remediation" for row in rows)
        transport = sum(row["quota_kind"] == "transport" for row in rows)
        alternate = by_stage["alternate_conformity"] > 0
        return {
            "pilot_id": self.pilot_id,
            "ledger_path": str(self.path),
            "requests_cumulative": len(rows),
            "requests_by_stage": by_stage,
            "unresolved_intents": sum(row["status"] == "INTENT" for row in rows),
            "remediation_calls": remediation,
            "transport_calls": transport,
            "reserve_equation_value": 8 * int(remediation > 0) + transport,
            "reserve_limit": 15,
            "planned_maximum": 160 if alternate else 152,
            "hard_stop": 200,
            "events": sorted(events),
        }
