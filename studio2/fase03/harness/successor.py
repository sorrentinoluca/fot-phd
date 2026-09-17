"""Reviewed successor-lineage contract for the suspended 122B predecessor.

This module performs no migration and no provider call.  It reads the predecessor
with SQLite ``mode=ro&immutable=1`` and returns normalized rows only after every
source, semantic field and hash has been checked from the same bytes.
"""
from __future__ import annotations

from contextlib import closing
from copy import deepcopy
import json
from pathlib import Path
import sqlite3

from .common import HarnessError, canonical_json, sha256_bytes, sha256_file, sha256_text


LINEAGE_ARTIFACT_VERSION = "SUCCESSOR_LINEAGE_1"
LINEAGE_COUNT = 5
LINEAGE_EVIDENCE_KEYS = {
    "stop_review_v2", "proposal_md", "proposal_json", "proposal_review", "author_decision"
}
NATIVE_DISPOSITION = "COMPLETED_IDENTITY_INVALID_ANTECEDENT_CONFIGURATION"


def _hash(value) -> bool:
    return isinstance(value, str) and len(value) == 64 and all(c in "0123456789abcdef" for c in value)


def _read_ref(ref, role: str) -> bytes:
    if not isinstance(ref, dict) or set(ref) != {"path", "sha256"} or not _hash(ref.get("sha256")):
        raise HarnessError(f"successor lineage {role} reference is incomplete")
    path = Path(ref["path"])
    if not path.is_absolute() or not path.is_file():
        raise HarnessError(f"successor lineage {role} file is missing")
    data = path.read_bytes()
    if sha256_bytes(data) != ref["sha256"]:
        raise HarnessError(f"successor lineage {role} bytes changed")
    return data


def _parse_object(data: bytes, role: str) -> dict:
    try:
        value = json.loads(data)
    except (UnicodeError, ValueError) as exc:
        raise HarnessError(f"successor lineage {role} is not valid JSON") from exc
    if not isinstance(value, dict):
        raise HarnessError(f"successor lineage {role} must be a JSON object")
    return value


def _validate_author_decision(data: bytes, *, text_sha256: str,
                              predecessor_sha256: str, review_sha256: str) -> None:
    decision = _parse_object(data, "author decision")
    selection = decision.get("selection")
    review = decision.get("independent_review")
    authorization = decision.get("authorization")
    expected_selection = {
        "t9_classification": "ANTECEDENT_QUALIFICATION_CONFIGURATION_FAILURE",
        "predecessor_sha256": predecessor_sha256,
        "cumulative_lineage_requests": 5,
        "lineage_import": "EXACTLY_ONCE_SUCCESSOR_ONLY",
        "technical_qualification_calls": 1,
        "producer_rendering_control": {
            "chat_template_kwargs": {"enable_thinking": False}},
        "consumer_probe_gate": "UNCHANGED",
        "t9": "UNCHANGED_AND_NOT_CONSUMED_BY_TECHNICAL_STAGE",
        "remediation": "NOT_CONSUMED_NOT_AUTHORIZED",
        "cumulative_planned_maximum": 166,
        "hard_stop": 200,
        "non_spendable_margin": 34,
    }
    if (decision.get("status") != "AUTHOR_DECISION_ACQUIRED"
            or not isinstance(decision.get("decision_text"), str)
            or sha256_text(decision["decision_text"]) != text_sha256
            or selection != expected_selection
            or not isinstance(review, dict) or review.get("sha256") != review_sha256
            or not isinstance(authorization, dict)
            or authorization.get("implementation_and_offline_materialization") is not True
            or authorization.get("provider_calls") is not False
            or authorization.get("execution_authorization_created") is not False):
        raise HarnessError("successor lineage author decision does not authorize this exact offline recovery")


def _predecessor_rows(path: Path, *, pilot_id: str, expected_sha256: str) -> tuple[list[dict], str]:
    path = Path(path).resolve()
    if not path.is_file() or not _hash(expected_sha256):
        raise HarnessError("successor lineage predecessor reference is invalid")
    before = sha256_file(path)
    if before != expected_sha256:
        raise HarnessError("successor lineage predecessor SHA-256 changed")
    uri = f"file:{path}?mode=ro&immutable=1"
    with closing(sqlite3.connect(uri, uri=True)) as connection:
        connection.row_factory = sqlite3.Row
        tables = {row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'")}
        if "predecessor_lineage" in tables:
            raise HarnessError("transitive successor lineage is forbidden")
        required = {"pilot", "external_history", "requests", "responses", "events", "stages"}
        if not required <= tables:
            raise HarnessError("successor lineage predecessor schema is incomplete")
        pilots = [row[0] for row in connection.execute("SELECT id FROM pilot")]
        if pilots != [pilot_id]:
            raise HarnessError("successor lineage predecessor pilot id changed")
        events = {row["event"]: row for row in connection.execute("SELECT * FROM events")}
        if any(name.startswith("successor_lineage:") for name in events):
            raise HarnessError("transitive successor lineage is forbidden")
        history = list(connection.execute(
            "SELECT * FROM external_history ORDER BY historical_ordinal"))
        history_events = [row for name, row in events.items()
                          if name.startswith("history_reconciliation:")]
        if len(history) != 4 or len(history_events) != 1:
            raise HarnessError("successor lineage predecessor historical S=4 is incomplete")
        history_event = history_events[0]
        try:
            history_detail = json.loads(history_event["detail_json"])
        except (TypeError, ValueError) as exc:
            raise HarnessError("successor lineage predecessor history event is invalid") from exc
        if (history_detail.get("status") != "RECONCILED"
                or history_detail.get("count") != 4
                or history_detail.get("package_sha256") != history_event["artifact_sha256"]
                or not _hash(history_detail.get("approval_sha256"))):
            raise HarnessError("successor lineage predecessor history event is inconsistent")
        normalized = []
        for ordinal, row in enumerate(history, 1):
            if (row["historical_ordinal"] != ordinal
                    or sha256_text(row["identity_json"]) != row["identity_sha256"]
                    or sha256_text(row["source_binding_json"]) != row["source_binding_sha256"]
                    or row["package_sha256"] != history_event["artifact_sha256"]
                    or row["disposition"] not in {"HISTORICAL_OUTCOME_UNCERTAIN", "COMPLETED"}
                    or (ordinal == 1) != (row["disposition"] == "HISTORICAL_OUTCOME_UNCERTAIN")):
                raise HarnessError("successor lineage predecessor historical row is corrupted")
            normalized.append({
                "ordinal": ordinal,
                "request_id": row["request_id"],
                "source_kind": "external_history",
                "identity": json.loads(row["identity_json"]),
                "identity_sha256": row["identity_sha256"],
                "source_binding_sha256": row["source_binding_sha256"],
                "disposition": row["disposition"],
                "raw_sha256": None,
                "record_sha256": None,
            })
        requests = list(connection.execute("SELECT * FROM requests ORDER BY rowid"))
        responses = list(connection.execute("SELECT * FROM responses ORDER BY rowid"))
        if len(requests) != 1 or len(responses) != 1:
            raise HarnessError("successor lineage predecessor must contain exactly one native attempt")
        request, response = requests[0], responses[0]
        if (request["request_id"] != response["request_id"]
                or request["stage"] != "producer_conformity"
                or request["quota_kind"] != "base" or request["retry_of"] is not None
                or request["status"] != "COMPLETED"
                or not response["record_json"]
                or sha256_text(response["raw_json"]) != response["raw_sha256"]
                or sha256_text(response["record_json"]) != response["record_sha256"]):
            raise HarnessError("successor lineage predecessor native attempt is inconsistent")
        record = json.loads(response["record_json"])
        if (record.get("request_id") != request["request_id"]
                or record.get("identity_valid") is not False
                or "suspended:" + request["request_id"] not in events
                or any(name.startswith("outcome:") for name in events)):
            raise HarnessError("successor lineage predecessor is not the required suspended STOP")
        source_binding = {
            "request_id": request["request_id"],
            "stage": request["stage"],
            "stage_run": request["stage_run"],
            "quota_kind": request["quota_kind"],
        }
        normalized.append({
            "ordinal": 5,
            "request_id": request["request_id"],
            "source_kind": "native_predecessor",
            "identity": json.loads(request["identity_json"]),
            "identity_sha256": sha256_text(request["identity_json"]),
            "source_binding_sha256": sha256_text(canonical_json(source_binding)),
            "disposition": NATIVE_DISPOSITION,
            "raw_sha256": response["raw_sha256"],
            "record_sha256": response["record_sha256"],
        })
        suspended_request_id = request["request_id"]
    after = sha256_file(path)
    if after != before:
        raise HarnessError("successor lineage predecessor changed during immutable read")
    return normalized, suspended_request_id


def build_successor_lineage_package(*, predecessor_path: Path, predecessor_pilot_id: str,
                                    successor_ledger: dict, evidence: dict,
                                    author_decision_text_sha256: str) -> dict:
    """Build a deterministic package from a suspended predecessor without writing it."""
    predecessor_path = Path(predecessor_path).resolve()
    predecessor_sha256 = sha256_file(predecessor_path)
    if (not isinstance(successor_ledger, dict)
            or set(successor_ledger) != {"path", "pilot_id"}
            or not Path(successor_ledger["path"]).is_absolute()
            or not isinstance(successor_ledger["pilot_id"], str)):
        raise HarnessError("successor lineage target is incomplete")
    if not isinstance(evidence, dict) or set(evidence) != LINEAGE_EVIDENCE_KEYS:
        raise HarnessError("successor lineage evidence inventory is incomplete")
    evidence_bytes = {role: _read_ref(ref, role) for role, ref in evidence.items()}
    if not _hash(author_decision_text_sha256):
        raise HarnessError("successor lineage author decision text digest is missing")
    rows, suspended_request_id = _predecessor_rows(
        predecessor_path, pilot_id=predecessor_pilot_id,
        expected_sha256=predecessor_sha256)
    _validate_author_decision(
        evidence_bytes["author_decision"],
        text_sha256=author_decision_text_sha256,
        predecessor_sha256=predecessor_sha256,
        review_sha256=evidence["proposal_review"]["sha256"])
    return {
        "artifact_version": LINEAGE_ARTIFACT_VERSION,
        "status": "REVIEWED_AUTHOR_SELECTED_ANTECEDENT",
        "predecessor": {
            "path": str(predecessor_path),
            "pilot_id": predecessor_pilot_id,
            "sha256": predecessor_sha256,
            "suspended_request_id": suspended_request_id,
        },
        "successor_ledger": deepcopy(successor_ledger),
        "cumulative_count": LINEAGE_COUNT,
        "requests": rows,
        "evidence": deepcopy(evidence),
        "author_decision_text_sha256": author_decision_text_sha256,
        "transitive_import": False,
    }


def validate_successor_lineage_artifacts(package_path: Path, approval_path: Path, *,
                                         expected_ledger: dict) -> dict:
    """Validate package, approval, sources and predecessor from bytes read once."""
    package_path, approval_path = Path(package_path).resolve(), Path(approval_path).resolve()
    package_bytes = package_path.read_bytes()
    approval_bytes = approval_path.read_bytes()
    package = _parse_object(package_bytes, "package")
    approval = _parse_object(approval_bytes, "approval")
    required_package = {"artifact_version", "status", "predecessor", "successor_ledger",
                        "cumulative_count", "requests", "evidence",
                        "author_decision_text_sha256", "transitive_import"}
    if (set(package) != required_package
            or package.get("artifact_version") != LINEAGE_ARTIFACT_VERSION
            or package.get("status") != "REVIEWED_AUTHOR_SELECTED_ANTECEDENT"
            or package.get("successor_ledger") != expected_ledger
            or package.get("cumulative_count") != LINEAGE_COUNT
            or package.get("transitive_import") is not False
            or not _hash(package.get("author_decision_text_sha256"))):
        raise HarnessError("successor lineage package contract mismatch")
    evidence = package.get("evidence")
    if not isinstance(evidence, dict) or set(evidence) != LINEAGE_EVIDENCE_KEYS:
        raise HarnessError("successor lineage evidence inventory is incomplete")
    evidence_bytes = {role: _read_ref(ref, role) for role, ref in evidence.items()}
    required_approval = {"artifact_version", "author", "decision", "package_sha256",
                         "successor_ledger", "author_decision"}
    if (set(approval) != required_approval or approval.get("artifact_version") != "1"
            or not isinstance(approval.get("author"), str) or not approval["author"].strip()
            or approval.get("decision") != "SUCCESSOR_LINEAGE_IMPORT_AUTHORIZED"
            or approval.get("package_sha256") != sha256_bytes(package_bytes)
            or approval.get("successor_ledger") != expected_ledger
            or approval.get("author_decision") != evidence["author_decision"]):
        raise HarnessError("successor lineage import lacks exact author approval")
    predecessor = package.get("predecessor")
    if (not isinstance(predecessor, dict)
            or set(predecessor) != {"path", "pilot_id", "sha256", "suspended_request_id"}
            or not Path(predecessor.get("path", "")).is_absolute()
            or not isinstance(predecessor.get("pilot_id"), str)
            or not _hash(predecessor.get("sha256"))
            or not isinstance(predecessor.get("suspended_request_id"), str)):
        raise HarnessError("successor lineage predecessor reference is incomplete")
    _validate_author_decision(
        evidence_bytes["author_decision"],
        text_sha256=package["author_decision_text_sha256"],
        predecessor_sha256=predecessor["sha256"],
        review_sha256=evidence["proposal_review"]["sha256"])
    observed_rows, suspended_request_id = _predecessor_rows(
        Path(predecessor["path"]), pilot_id=predecessor["pilot_id"],
        expected_sha256=predecessor["sha256"])
    rows = package.get("requests")
    if (not isinstance(rows, list) or len(rows) != LINEAGE_COUNT
            or rows != observed_rows
            or predecessor["suspended_request_id"] != suspended_request_id
            or [row.get("ordinal") for row in rows] != list(range(1, LINEAGE_COUNT + 1))
            or len({row.get("request_id") for row in rows}) != LINEAGE_COUNT
            or len({row.get("identity_sha256") for row in rows}) != LINEAGE_COUNT):
        raise HarnessError("successor lineage import is selective, duplicated or altered")
    return {
        "package": package,
        "approval": approval,
        "rows": deepcopy(rows),
        "package_sha256": sha256_bytes(package_bytes),
        "approval_sha256": sha256_bytes(approval_bytes),
        "predecessor_sha256": predecessor["sha256"],
    }
