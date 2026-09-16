"""Durable, fail-closed pilot state machine. All decisions use one SQLite transaction.

A new ledger must be shared by all runners of one pilot. Legacy ledgers are
read-only evidence: migration requires an independently reviewed reconciliation.
No uncertain request is ever resent implicitly.
"""
from __future__ import annotations

from contextlib import closing, contextmanager
from datetime import datetime, timezone
import difflib
import json
from pathlib import Path
import re
import sqlite3
from typing import Any, Iterable

from .common import (HarnessError, canonical_json, load_json, sha256_bytes,
                     sha256_file, sha256_text, tokenized_length)

HASH = re.compile(r"^[0-9a-f]{64}$")
TECHNICAL_STAGE = "technical_qualification_122b"
STAGES = {"producer_conformity", "producer_remediation", "alternate_conformity",
          "budget_probe", "stability_gate"}
ACTIVE_STAGES = STAGES | {TECHNICAL_STAGE}
BASE_LIMITS = {TECHNICAL_STAGE: 1, "producer_conformity": 8,
               "producer_remediation": 8, "alternate_conformity": 8,
               "budget_probe": 9, "stability_gate": 120}
DIAGNOSES = {"structure", "identifiers", "cap", "leakage"}
TOKENIZER_ACCOUNTING_SNAPSHOT = "Qwen/Qwen3.5-122B-A10B-FP8@a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9"
TOKENIZER_ACCOUNTING_MODEL = "qwen3.5-122b"


def digest(value):
    return sha256_text(canonical_json(value))


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


class TokenizerAccountingGuard:
    """The one 122B accounting rule, deliberately bound to its frozen client snapshot."""

    def __init__(self, local_tokenizer, *, snapshot=TOKENIZER_ACCOUNTING_SNAPSHOT,
                 template_kwargs=None):
        if snapshot != TOKENIZER_ACCOUNTING_SNAPSHOT:
            raise HarnessError("FATAL_ACCOUNTING_ERROR: tokenizer snapshot is not the frozen 122B client")
        if template_kwargs not in (None, {}):
            try:
                from .d9 import no_thinking_template_kwargs
                template_kwargs = no_thinking_template_kwargs(template_kwargs)
            except HarnessError as exc:
                raise HarnessError(
                    "FATAL_ACCOUNTING_ERROR: unsupported chat-template kwargs") from exc
        self.tokenizer = local_tokenizer
        self.snapshot = snapshot
        self.template_kwargs = dict(template_kwargs or {})

    def validate_producer_response(self, messages, api_response):
        if not isinstance(messages, list):
            raise HarnessError("FATAL_ACCOUNTING_ERROR: messages transmitted to provider are not a list")
        try:
            local = self.tokenizer.apply_chat_template(
                messages, tokenize=True, add_generation_prompt=True,
                **self.template_kwargs)
            local_prompt_tokens = tokenized_length(local)
        except Exception as exc:
            raise HarnessError(
                "FATAL_ACCOUNTING_ERROR: tokenizer output is not one unambiguous token-id sequence: "
                f"{type(exc).__name__}: {exc}") from exc
        usage = api_response.get("usage") if isinstance(api_response, dict) else None
        if not isinstance(usage, dict):
            raise HarnessError("FATAL_ACCOUNTING_ERROR: campo usage assente o non oggetto")
        server_prompt_tokens = usage.get("prompt_tokens")
        if type(server_prompt_tokens) is not int or server_prompt_tokens < 0:
            raise HarnessError("FATAL_ACCOUNTING_ERROR: usage.prompt_tokens assente, non intero o negativo")
        if local_prompt_tokens != server_prompt_tokens:
            raise HarnessError(
                "FATAL_ACCOUNTING_ERROR: Mismatch contabilità token: "
                f"locale={local_prompt_tokens}, server={server_prompt_tokens}")
        return {"local_prompt_tokens": local_prompt_tokens, "server_prompt_tokens": server_prompt_tokens}


def load_tokenizer_accounting_guard(snapshot: Path, *, template_kwargs=None):
    """Load only local frozen assets; callers remain responsible for file-hash guards."""
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            str(snapshot), local_files_only=True, trust_remote_code=False)
    except Exception as exc:
        raise HarnessError(f"FATAL_ACCOUNTING_ERROR: cannot load frozen tokenizer/template: {exc}") from exc
    return TokenizerAccountingGuard(tokenizer, template_kwargs=template_kwargs)


class PilotLedger:
    def __init__(self, path: Path, *, pilot_id: str):
        if not path.is_absolute():
            raise HarnessError("pilot ledger path must be absolute and shared across worktrees")
        if not re.fullmatch(r"[A-Za-z0-9_.-]{8,120}", pilot_id):
            raise HarnessError("invalid pilot_id")
        self.path, self.pilot_id = path.resolve(), pilot_id
        path.parent.mkdir(parents=True, exist_ok=True)
        with closing(self._connect()) as c:
            version = c.execute("PRAGMA user_version").fetchone()[0]
            if version not in {0, 2, 3, 4}:
                raise HarnessError("unsupported ledger version")
            if version == 0 and c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                raise HarnessError("legacy ledger requires explicit reviewed migration; preserved without changes")
            if version == 0:
                c.executescript('''
                PRAGMA journal_mode=WAL;
                CREATE TABLE IF NOT EXISTS pilot (id TEXT PRIMARY KEY);
                CREATE TABLE IF NOT EXISTS stages (
                    stage TEXT PRIMARY KEY, binding_json TEXT NOT NULL, binding_sha256 TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS requests (
                    request_id TEXT PRIMARY KEY, logical_id TEXT NOT NULL, stage TEXT NOT NULL,
                    stage_run TEXT NOT NULL, model TEXT NOT NULL, producer TEXT NOT NULL,
                    quota_kind TEXT NOT NULL, retry_of TEXT UNIQUE, identity_json TEXT NOT NULL,
                    status TEXT NOT NULL, intent_utc TEXT NOT NULL, completed_utc TEXT,
                    prompt_tokens INTEGER, completion_tokens INTEGER, total_tokens INTEGER,
                    latency_ms REAL, proof_sha256 TEXT, detail_json TEXT);
                CREATE UNIQUE INDEX IF NOT EXISTS base_once ON requests(stage,logical_id)
                    WHERE retry_of IS NULL;
                CREATE TABLE IF NOT EXISTS events (
                    event TEXT PRIMARY KEY, created_utc TEXT NOT NULL,
                    artifact_sha256 TEXT NOT NULL, detail_json TEXT NOT NULL);
                CREATE TABLE IF NOT EXISTS responses (
                    request_id TEXT PRIMARY KEY, raw_json TEXT NOT NULL, raw_sha256 TEXT NOT NULL,
                    record_json TEXT, record_sha256 TEXT);
                CREATE TABLE IF NOT EXISTS receipts (request_id TEXT PRIMARY KEY, capture_json TEXT NOT NULL);
                PRAGMA user_version=2;
                ''')
        with self._transaction() as c:
            c.execute("INSERT OR IGNORE INTO pilot VALUES (?)", (pilot_id,))
            if [r[0] for r in c.execute("SELECT id FROM pilot")] != [pilot_id]:
                raise HarnessError("ledger belongs to a different pilot; counters cannot be reset by renaming")

    def _connect(self):
        c = sqlite3.connect(self.path, timeout=30)
        c.row_factory = sqlite3.Row
        c.execute("PRAGMA synchronous=FULL")
        return c

    @contextmanager
    def _transaction(self):
        c = self._connect()
        try:
            c.execute("BEGIN IMMEDIATE")
            yield c
            c.commit()
        except BaseException:
            c.rollback()
            raise
        finally:
            c.close()

    def _rows(self, c):
        return list(c.execute("SELECT * FROM requests ORDER BY rowid"))

    def _validated_attempt_inventory(self, c):
        """Validate every quota contributor before reuse or reservation, including open stages.

        This checks partial attempt chains without requiring a closed outcome or complete
        coverage. All stages contribute to the shared reserve, not only the requested one.
        The caller holds the transaction through its decision and any insertion.
        """
        self._quota_predecessors(c)
        rows = self._rows(c)
        for stage in sorted({row['stage'] for row in rows}):
            if stage not in ACTIVE_STAGES:
                raise HarnessError('persisted attempt has an unknown stage')
            self._validate_attempts(c, self._binding(c, stage),
                                    [row for row in rows if row['stage'] == stage])
        return rows

    def _historical_rows(self, c):
        exists = c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='external_history'").fetchone()
        return [] if exists is None else list(c.execute(
            "SELECT * FROM external_history ORDER BY historical_ordinal"))

    def _validated_external_history(self, c):
        rows = self._historical_rows(c)
        version = c.execute("PRAGMA user_version").fetchone()[0]
        events = [row for name, row in self._events(c).items()
                  if name.startswith('history_reconciliation:')]
        if not rows and version == 2 and not events:
            return []
        if version != 3 or len(rows) != 4 or len(events) != 1:
            raise HarnessError('external history reconciliation is partial or corrupted')
        event = events[0]
        detail = json.loads(event['detail_json'])
        package_sha256 = event['artifact_sha256']
        self._require_hash(package_sha256, 'external history package')
        if detail != {'status': 'RECONCILED', 'count': 4,
                      'package_sha256': package_sha256,
                      'approval_sha256': detail.get('approval_sha256')}:
            raise HarnessError('external history reconciliation event is corrupted')
        self._require_hash(detail.get('approval_sha256'), 'external history approval')
        for position, row in enumerate(rows, 1):
            if (row['historical_ordinal'] != position
                    or sha256_text(row['identity_json']) != row['identity_sha256']
                    or sha256_text(row['source_binding_json']) != row['source_binding_sha256']
                    or row['package_sha256'] != package_sha256
                    or row['disposition'] not in {'HISTORICAL_OUTCOME_UNCERTAIN', 'COMPLETED'}
                    or (position == 1) != (row['disposition'] == 'HISTORICAL_OUTCOME_UNCERTAIN')):
                raise HarnessError('external history row is corrupted')
        return rows

    def _insert_external_history(self, c, row, package_sha256):
        c.execute("INSERT INTO external_history VALUES (?,?,?,?,?,?,?,?)", (
            row['request_id'], row['historical_ordinal'], canonical_json(row['identity']),
            row['identity_sha256'], canonical_json(row['source_binding']),
            digest(row['source_binding']), row['disposition'], package_sha256))

    def reconcile_external_history(self, *, package_path: Path, approval_path: Path):
        """Explicitly import four external quota contributors; never provider requests."""
        package_path, approval_path = Path(package_path).resolve(), Path(approval_path).resolve()
        with self._transaction() as c:
            from .d9 import validate_external_history_artifacts
            validated = validate_external_history_artifacts(
                package_path, approval_path,
                expected_ledger={'path': str(self.path), 'pilot_id': self.pilot_id})
            existing = self._historical_rows(c)
            if existing:
                checked = self._validated_external_history(c)
                event = next(row for name, row in self._events(c).items()
                             if name.startswith('history_reconciliation:'))
                event_detail = json.loads(event['detail_json'])
                if (any(row['package_sha256'] != validated['package_sha256'] for row in checked)
                        or event_detail.get('approval_sha256') != validated['approval_sha256']):
                    raise HarnessError('another external history package is already reconciled')
                return {'status': 'ALREADY_RECONCILED', 'historical_requests': len(checked)}
            if c.execute("PRAGMA user_version").fetchone()[0] != 2:
                raise HarnessError('external history import requires an unreconciled v2 ledger')
            if self._rows(c):
                raise HarnessError('external history must be reconciled before native request intents')
            if any(name.startswith('history_reconciliation:') for name in self._events(c)):
                raise HarnessError('external history event exists without complete rows')
            c.execute('''CREATE TABLE external_history (
                request_id TEXT PRIMARY KEY,
                historical_ordinal INTEGER NOT NULL UNIQUE CHECK(historical_ordinal BETWEEN 1 AND 4),
                identity_json TEXT NOT NULL,
                identity_sha256 TEXT NOT NULL UNIQUE,
                source_binding_json TEXT NOT NULL,
                source_binding_sha256 TEXT NOT NULL UNIQUE,
                disposition TEXT NOT NULL,
                package_sha256 TEXT NOT NULL)''')
            for row in validated['rows']:
                self._insert_external_history(c, row, validated['package_sha256'])
            detail = {'status': 'RECONCILED', 'count': len(validated['rows']),
                      'package_sha256': validated['package_sha256'],
                      'approval_sha256': validated['approval_sha256']}
            self._event(c, 'history_reconciliation:' + validated['package_sha256'],
                        validated['package_sha256'], detail)
            c.execute("PRAGMA user_version=3")
            self._validated_external_history(c)
            return {'status': 'RECONCILED', 'historical_requests': len(validated['rows'])}

    def _lineage_rows(self, c):
        exists = c.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='predecessor_lineage'"
        ).fetchone()
        return [] if exists is None else list(c.execute(
            "SELECT * FROM predecessor_lineage ORDER BY ordinal"))

    def _validated_predecessor_lineage(self, c, *, package_path=None, approval_path=None):
        """Reauthenticate every durable lineage field against its approved artifacts."""
        rows = self._lineage_rows(c)
        version = c.execute("PRAGMA user_version").fetchone()[0]
        events = [row for name, row in self._events(c).items()
                  if name.startswith("successor_lineage:")]
        if not rows and version in {2, 3} and not events:
            return []
        if version != 4 or len(rows) != 5 or len(events) != 1:
            raise HarnessError("successor lineage is partial or corrupted")
        event = events[0]
        detail = json.loads(event["detail_json"])
        package_ref = detail.get("package_reference")
        approval_ref = detail.get("approval_reference")
        if (not isinstance(package_ref, dict) or set(package_ref) != {"path", "sha256"}
                or not isinstance(approval_ref, dict) or set(approval_ref) != {"path", "sha256"}
                or not Path(package_ref.get("path", "")).is_absolute()
                or not Path(approval_ref.get("path", "")).is_absolute()
                or not HASH.fullmatch(package_ref.get("sha256", ""))
                or not HASH.fullmatch(approval_ref.get("sha256", ""))):
            raise HarnessError("successor lineage event is corrupted")
        stored_package_path = Path(package_ref["path"]).resolve()
        stored_approval_path = Path(approval_ref["path"]).resolve()
        if package_path is not None and Path(package_path).resolve() != stored_package_path:
            raise HarnessError("successor lineage package reference differs from durable import")
        if approval_path is not None and Path(approval_path).resolve() != stored_approval_path:
            raise HarnessError("successor lineage approval reference differs from durable import")
        from .successor import validate_successor_lineage_artifacts
        validated = validate_successor_lineage_artifacts(
            stored_package_path, stored_approval_path,
            expected_ledger={"path": str(self.path), "pilot_id": self.pilot_id})
        expected_detail = {
            "status": "RECONCILED", "count": 5,
            "package_sha256": validated["package_sha256"],
            "approval_sha256": validated["approval_sha256"],
            "predecessor_sha256": validated["predecessor_sha256"],
            "package_reference": {
                "path": str(stored_package_path), "sha256": validated["package_sha256"]},
            "approval_reference": {
                "path": str(stored_approval_path), "sha256": validated["approval_sha256"]},
        }
        if (event["event"] != "successor_lineage:" + validated["package_sha256"]
                or event["artifact_sha256"] != validated["package_sha256"]
                or detail != expected_detail):
            raise HarnessError("successor lineage event differs from approved artifacts")
        for row, approved in zip(rows, validated["rows"]):
            expected_row = {
                "ordinal": approved["ordinal"],
                "request_id": approved["request_id"],
                "source_kind": approved["source_kind"],
                "identity_json": canonical_json(approved["identity"]),
                "identity_sha256": approved["identity_sha256"],
                "source_binding_sha256": approved["source_binding_sha256"],
                "disposition": approved["disposition"],
                "raw_sha256": approved["raw_sha256"],
                "record_sha256": approved["record_sha256"],
                "package_sha256": validated["package_sha256"],
                "predecessor_sha256": validated["predecessor_sha256"],
            }
            if any(row[key] != value for key, value in expected_row.items()):
                raise HarnessError("successor lineage row differs from approved artifacts")
        return rows

    def _quota_predecessors(self, c):
        version = c.execute("PRAGMA user_version").fetchone()[0]
        if version == 4:
            if self._historical_rows(c):
                raise HarnessError("successor lineage cannot coexist with external history rows")
            return self._validated_predecessor_lineage(c)
        return self._validated_external_history(c)

    def reconcile_successor_lineage(self, *, package_path: Path, approval_path: Path):
        """Import the reviewed predecessor S=5 once; never copy predecessor rows."""
        package_path, approval_path = Path(package_path).resolve(), Path(approval_path).resolve()
        with self._transaction() as c:
            if self._lineage_rows(c) or any(
                    name.startswith("successor_lineage:") for name in self._events(c)):
                raise HarnessError("successor lineage is already reconciled")
            if c.execute("PRAGMA user_version").fetchone()[0] != 2:
                raise HarnessError("successor lineage import requires a fresh v2 ledger")
            if self._rows(c) or self._historical_rows(c):
                raise HarnessError("successor lineage must precede every native intent and history import")
            from .successor import validate_successor_lineage_artifacts
            validated = validate_successor_lineage_artifacts(
                package_path, approval_path,
                expected_ledger={"path": str(self.path), "pilot_id": self.pilot_id})
            c.execute("""CREATE TABLE predecessor_lineage (
                ordinal INTEGER PRIMARY KEY CHECK(ordinal BETWEEN 1 AND 5),
                request_id TEXT NOT NULL UNIQUE,
                source_kind TEXT NOT NULL,
                identity_json TEXT NOT NULL,
                identity_sha256 TEXT NOT NULL UNIQUE,
                source_binding_sha256 TEXT NOT NULL UNIQUE,
                disposition TEXT NOT NULL,
                raw_sha256 TEXT,
                record_sha256 TEXT,
                package_sha256 TEXT NOT NULL,
                predecessor_sha256 TEXT NOT NULL)""")
            for row in validated["rows"]:
                c.execute("INSERT INTO predecessor_lineage VALUES (?,?,?,?,?,?,?,?,?,?,?)", (
                    row["ordinal"], row["request_id"], row["source_kind"],
                    canonical_json(row["identity"]), row["identity_sha256"],
                    row["source_binding_sha256"], row["disposition"],
                    row["raw_sha256"], row["record_sha256"],
                    validated["package_sha256"], validated["predecessor_sha256"]))
            detail = {"status": "RECONCILED", "count": 5,
                      "package_sha256": validated["package_sha256"],
                      "approval_sha256": validated["approval_sha256"],
                      "predecessor_sha256": validated["predecessor_sha256"],
                      "package_reference": {
                          "path": str(package_path),
                          "sha256": validated["package_sha256"]},
                      "approval_reference": {
                          "path": str(approval_path),
                          "sha256": validated["approval_sha256"]}}
            self._event(c, "successor_lineage:" + validated["package_sha256"],
                        validated["package_sha256"], detail)
            c.execute("PRAGMA user_version=4")
            self._validated_predecessor_lineage(c)
            return {"status": "RECONCILED", "predecessor_requests": 5}

    def _events(self, c):
        return {r['event']: r for r in c.execute("SELECT * FROM events")}

    def _tokenizer_accounting_stop(self, c):
        return self._events(c).get('stop:tokenizer_accounting')

    def _require_no_tokenizer_accounting_stop(self, c):
        stop = self._tokenizer_accounting_stop(c)
        if stop is not None:
            detail = json.loads(stop['detail_json'])
            raise HarnessError('FATAL_ACCOUNTING_ERROR: durable STOP blocks probes, gates, retries and new requests: '
                               + detail['reason'])

    @staticmethod
    def _accounting_commitment(request, messages, snapshot, raw_json,
                               local_prompt_tokens, server_prompt_tokens,
                               template_kwargs=None):
        result = {
            'artifact_version': 'TOKENIZER_ACCOUNTING_2',
            'request_id': request['request_id'],
            'request_identity_sha256': sha256_text(request['identity_json']),
            'messages': messages,
            'messages_sha256': sha256_text(canonical_json(messages)),
            'snapshot': snapshot,
            'raw_response_sha256': sha256_text(raw_json),
            'local_prompt_tokens': local_prompt_tokens,
            'server_prompt_tokens': server_prompt_tokens,
            'outcome': 'PASS',
        }
        if template_kwargs:
            result['chat_template_kwargs'] = dict(template_kwargs)
        return result

    def _persist_accounting_stop(self, c, request_id, reason, artifact_sha256):
        if self._tokenizer_accounting_stop(c) is None:
            self._event(c, 'stop:tokenizer_accounting', artifact_sha256,
                        {'reason': reason, 'request_id': request_id,
                         'accounting_event': 'tokenizer_accounting:' + request_id})

    def _validate_accounting_event(self, c, request, *, messages, guard):
        response = c.execute('SELECT raw_json,raw_sha256 FROM responses WHERE request_id=?',
                             (request['request_id'],)).fetchone()
        event = self._events(c).get('tokenizer_accounting:' + request['request_id'])
        if response is None or event is None:
            raise HarnessError('FATAL_ACCOUNTING_ERROR: persisted accounting evidence is missing')
        if sha256_text(response['raw_json']) != response['raw_sha256']:
            raise HarnessError('FATAL_ACCOUNTING_ERROR: raw response hash mismatch')
        try:
            detail = json.loads(event['detail_json'])
            raw = json.loads(response['raw_json'])
        except (ValueError, TypeError, UnicodeError) as exc:
            raise HarnessError('FATAL_ACCOUNTING_ERROR: persisted accounting JSON is invalid') from exc
        if detail.get('messages') != messages:
            raise HarnessError('FATAL_ACCOUNTING_ERROR: persisted accounting messages differ from the request')
        counts = guard.validate_producer_response(messages, raw)
        expected = self._accounting_commitment(
            request, messages, guard.snapshot, response['raw_json'],
            counts['local_prompt_tokens'], counts['server_prompt_tokens'],
            guard.template_kwargs)
        if 'chat_template_kwargs' in expected:
            try:
                from .d9 import no_thinking_template_kwargs
                no_thinking_template_kwargs(detail.get('chat_template_kwargs'))
            except HarnessError as exc:
                raise HarnessError(
                    'FATAL_ACCOUNTING_ERROR: persisted chat-template kwargs are invalid') from exc
        expected_commitment = digest(expected)
        persisted_commitment = digest(detail)
        if (detail != expected or event['artifact_sha256'] != persisted_commitment
                or persisted_commitment != expected_commitment
                or request['proof_sha256'] != persisted_commitment
                or response['raw_sha256'] != expected['raw_response_sha256']):
            raise HarnessError('FATAL_ACCOUNTING_ERROR: persisted accounting evidence binding is corrupted')
        return expected

    def account_producer_response(self, request_id, *, messages, guard):
        """Persist or revalidate 122B accounting before parsing/materializing output.

        The raw response has already been durably captured by ``save_raw``.  Both
        pass and failure evidence are create-once events; failure also writes a
        durable global STOP in this same transaction.
        """
        failure = result = None
        with self._transaction() as c:
            self._require_no_tokenizer_accounting_stop(c)
            response = c.execute('SELECT raw_json,raw_sha256 FROM responses WHERE request_id=?',
                                 (request_id,)).fetchone()
            if response is None or sha256_text(response['raw_json']) != response['raw_sha256']:
                raise HarnessError('FATAL_ACCOUNTING_ERROR: raw response missing or hash mismatch')
            request = c.execute('SELECT * FROM requests WHERE request_id=?', (request_id,)).fetchone()
            if request is None or request['model'] != TOKENIZER_ACCOUNTING_MODEL:
                raise HarnessError('FATAL_ACCOUNTING_ERROR: accounting requires a persisted 122B request')
            try:
                existing = self._events(c).get('tokenizer_accounting:' + request_id)
                if existing is not None:
                    result = self._validate_accounting_event(c, request, messages=messages, guard=guard)
                else:
                    if request['status'] != 'INTENT' or request['proof_sha256'] is not None:
                        raise HarnessError('FATAL_ACCOUNTING_ERROR: completed/legacy 122B request lacks accounting evidence')
                    raw = json.loads(response['raw_json'])
                    counts = guard.validate_producer_response(messages, raw)
                    result = self._accounting_commitment(
                        request, messages, guard.snapshot, response['raw_json'],
                        counts['local_prompt_tokens'], counts['server_prompt_tokens'],
                        guard.template_kwargs)
                    commitment = digest(result)
                    self._event(c, 'tokenizer_accounting:' + request_id, commitment, result)
                    c.execute('UPDATE requests SET proof_sha256=? WHERE request_id=? AND proof_sha256 IS NULL',
                              (commitment, request_id))
            except Exception as exc:
                reason = str(exc) if str(exc).startswith('FATAL_ACCOUNTING_ERROR') else (
                    f'FATAL_ACCOUNTING_ERROR: tokenizer/template accounting failed: {type(exc).__name__}: {exc}')
                self._persist_accounting_stop(c, request_id, reason, response['raw_sha256'])
                failure = reason
        if failure is not None:
            raise HarnessError(failure)
        return result

    def validate_tokenizer_accounting_evidence(self, guard, *, expected_messages=None):
        """Recompute all persisted accounting links before evidence is reused."""
        failure = None
        with self._transaction() as c:
            self._require_no_tokenizer_accounting_stop(c)
            for name, row in self._events(c).items():
                if not name.startswith('tokenizer_accounting:'):
                    continue
                request_id = name.split(':', 1)[1]
                request = c.execute('SELECT * FROM requests WHERE request_id=?', (request_id,)).fetchone()
                try:
                    detail = json.loads(row['detail_json'])
                    messages = detail.get('messages')
                    if expected_messages is not None:
                        expected = expected_messages.get(request['logical_id']) if request else None
                        if expected is not None:
                            messages = expected
                    self._validate_accounting_event(c, request, messages=messages, guard=guard)
                except Exception as exc:
                    reason = str(exc) if str(exc).startswith('FATAL_ACCOUNTING_ERROR') else (
                        f'FATAL_ACCOUNTING_ERROR: accounting evidence revalidation failed: {type(exc).__name__}: {exc}')
                    artifact = row['artifact_sha256'] if HASH.fullmatch(row['artifact_sha256'] or '') else '0' * 64
                    self._persist_accounting_stop(c, request_id, reason, artifact)
                    failure = reason
                    break
        if failure is not None:
            raise HarnessError(failure)

    @staticmethod
    def _record_consumed_fields(raw, record):
        if not isinstance(raw, dict) or not isinstance(record, dict):
            raise HarnessError('FATAL_ACCOUNTING_ERROR: raw and evaluated record must be objects')
        usage = raw.get('usage')
        if not isinstance(usage, dict):
            raise HarnessError('FATAL_ACCOUNTING_ERROR: raw usage is missing during record binding')
        expected = {
            'response_id': raw.get('id'), 'returned_model': raw.get('model'),
            'system_fingerprint': raw.get('system_fingerprint'),
            'prompt_tokens': usage.get('prompt_tokens'),
            'completion_tokens': usage.get('completion_tokens'), 'total_tokens': usage.get('total_tokens'),
        }
        choices = raw.get('choices')
        if isinstance(choices, list) and len(choices) == 1 and isinstance(choices[0], dict):
            message = choices[0].get('message')
            if isinstance(message, dict):
                expected.update(finish_reason=choices[0].get('finish_reason'), raw_output=message.get('content'))
        for key, value in expected.items():
            if record.get(key) != value:
                raise HarnessError('FATAL_ACCOUNTING_ERROR: evaluated record differs from raw field ' + key)
        if 'raw_output_sha256' in record and (
                not isinstance(record.get('raw_output'), str)
                or record['raw_output_sha256'] != sha256_text(record['raw_output'])):
            raise HarnessError('FATAL_ACCOUNTING_ERROR: evaluated raw-output digest is invalid')
        return expected

    def _accounting_record_link(self, c, request, record):
        response = c.execute('SELECT * FROM responses WHERE request_id=?', (request['request_id'],)).fetchone()
        accounting = self._events(c).get('tokenizer_accounting:' + request['request_id'])
        if response is None or accounting is None:
            raise HarnessError('FATAL_ACCOUNTING_ERROR: record lacks independent accounting commitment')
        try:
            accounting_detail = json.loads(accounting['detail_json'])
        except (TypeError, ValueError, UnicodeError) as exc:
            raise HarnessError(
                'FATAL_ACCOUNTING_ERROR: persisted accounting commitment is invalid') from exc
        if 'chat_template_kwargs' in accounting_detail:
            try:
                from .d9 import no_thinking_template_kwargs
                no_thinking_template_kwargs(accounting_detail['chat_template_kwargs'])
            except HarnessError as exc:
                raise HarnessError(
                    'FATAL_ACCOUNTING_ERROR: persisted chat-template kwargs are invalid') from exc
        if (accounting['artifact_sha256'] != digest(accounting_detail)
                or request['proof_sha256'] != accounting['artifact_sha256']):
            raise HarnessError(
                'FATAL_ACCOUNTING_ERROR: persisted accounting commitment is corrupted')
        consumed = self._record_consumed_fields(json.loads(response['raw_json']), record)
        return {
            'artifact_version': 'TOKENIZER_ACCOUNTING_RECORD_1',
            'request_id': request['request_id'],
            'request_identity_sha256': sha256_text(request['identity_json']),
            'accounting_commitment_sha256': request['proof_sha256'],
            'raw_response_sha256': sha256_text(response['raw_json']),
            'record_sha256': digest(record),
            'consumed_fields_sha256': digest(consumed),
        }

    def bind_tokenizer_accounting_record(self, request_id, *, record):
        """Create/reconfirm the raw-to-record semantic link before request completion."""
        with self._transaction() as c:
            self._require_no_tokenizer_accounting_stop(c)
            request = c.execute('SELECT * FROM requests WHERE request_id=?', (request_id,)).fetchone()
            if request is None or request['model'] != TOKENIZER_ACCOUNTING_MODEL:
                raise HarnessError('FATAL_ACCOUNTING_ERROR: record binding requires a 122B request')
            link = self._accounting_record_link(c, request, record)
            name = 'tokenizer_accounting_record:' + request_id
            existing = self._events(c).get(name)
            if existing is None:
                self._event(c, name, digest(link), link)
            elif existing['artifact_sha256'] != digest(link) or json.loads(existing['detail_json']) != link:
                raise HarnessError('FATAL_ACCOUNTING_ERROR: evaluated record differs across resume')
            return link

    def _validate_tokenizer_accounting_record(self, c, request, record):
        link = self._accounting_record_link(c, request, record)
        event = self._events(c).get('tokenizer_accounting_record:' + request['request_id'])
        if event is None or event['artifact_sha256'] != digest(link) or json.loads(event['detail_json']) != link:
            raise HarnessError('FATAL_ACCOUNTING_ERROR: raw-to-record accounting link is missing or corrupted')
        return link

    def validate_tokenizer_accounting_record(self, request_id, *, record):
        with self._transaction() as c:
            self._require_no_tokenizer_accounting_stop(c)
            request = c.execute('SELECT * FROM requests WHERE request_id=?', (request_id,)).fetchone()
            return self._validate_tokenizer_accounting_record(c, request, record)

    @staticmethod
    def _require_hash(value, role):
        if not isinstance(value, str) or not HASH.fullmatch(value):
            raise HarnessError(f"{role} must be a lowercase SHA-256")

    def _event(self, c, event, artifact_sha256, detail):
        self._require_hash(artifact_sha256, 'event artifact')
        try:
            c.execute("INSERT INTO events VALUES (?,?,?,?)", (event, _utc_now(), artifact_sha256, canonical_json(detail)))
        except sqlite3.IntegrityError as exc:
            raise HarnessError(f"event is create-once: {event}") from exc

    def record_event(self, event, *, artifact_sha256, detail):
        if not event.startswith('note:'):
            raise HarnessError("public events may only be non-normative notes")
        with self._transaction() as c:
            self._event(c, event, artifact_sha256, detail)

    def event(self, name):
        with closing(self._connect()) as c:
            row = self._events(c).get(name)
            return None if row is None else dict(artifact_sha256=row['artifact_sha256'], **json.loads(row['detail_json']))

    def _binding(self, c, stage):
        row = c.execute("SELECT * FROM stages WHERE stage=?", (stage,)).fetchone()
        if row is None:
            raise HarnessError(f"stage {stage} requires an immutable request plan")
        value = json.loads(row['binding_json'])
        if digest(value) != row['binding_sha256']:
            raise HarnessError("stage binding corrupted")
        from .d9 import validate_binding
        validate_binding(value, stage, self, c)
        return value

    def binding(self, stage):
        with self._transaction() as c:
            return self._binding(c, stage)

    def bind_stage(self, stage, binding):
        """Freeze exact requests, provider, prompts, inputs and template before reservation."""
        if stage not in ACTIVE_STAGES:
            raise HarnessError("invalid stage")
        specs = binding.get('requests', [])
        required = {'logical_id', 'model', 'producer', 'prompt_sha256', 'case_sha256', 'contract_sha256', 'condition', 'group', 'repetition'}
        if not isinstance(specs, list) or len({s.get('logical_id') for s in specs}) != len(specs):
            raise HarnessError("request plan requires unique logical identities")
        expected = BASE_LIMITS[stage]
        if (stage == 'budget_probe' and len(specs) not in {3, 6, 9}) or (stage != 'budget_probe' and len(specs) != expected):
            raise HarnessError("request plan has wrong coverage")
        for s in specs:
            if set(s) != required or not all(isinstance(s[k], str) and s[k] for k in ('logical_id', 'model', 'producer', 'group')):
                raise HarnessError("incomplete request identity")
            for k in ('prompt_sha256', 'case_sha256', 'contract_sha256'):
                self._require_hash(s[k], k)
        if stage == 'budget_probe':
            groups = {}
            for s in specs:
                groups.setdefault(s['group'], []).append(s)
            if any(len(g) != 3 or {s['condition'] for s in g} != {'A', 'B-LF', 'E-LF'} for g in groups.values()):
                raise HarnessError("probe plan requires distinct complete condition triplets")
        with self._transaction() as c:
            self._require_no_tokenizer_accounting_stop(c)
            from .d9 import validate_binding
            validate_binding(binding, stage, self, c)
            old = c.execute("SELECT binding_sha256 FROM stages WHERE stage=?", (stage,)).fetchone()
            if old:
                if old[0] != digest(binding):
                    raise HarnessError("stage inputs changed across alias, directory or restart")
                self._prerequisites(c, stage)
                self._validated_attempt_inventory(c)
                if 'outcome:' + stage in self._events(c):
                    self._closed_outcome(c, stage)
                return
            self._ready(c, stage)
            self._validated_attempt_inventory(c)
            if stage == 'producer_remediation':
                auth = self._events(c).get('remediation_authorized')
                if auth is None:
                    raise HarnessError("remediation lacks written approval")
                detail = json.loads(auth['detail_json'])
                first = self._binding(c, 'producer_conformity')
                coverage = lambda b: sorted((s['logical_id'], s['case_sha256'], s['contract_sha256'], s['model'], s['producer']) for s in b['requests'])
                if coverage(first) != coverage(binding) or binding.get('template_text') != detail['template_text']:
                    raise HarnessError("remediation must use approved template and the same eight cases/contracts/provider")
                # Only the producer template may differ.
                for key in set(first) - {'requests', 'template_text'}:
                    if binding.get(key) != first[key]:
                        raise HarnessError("remediation changed a non-template contract")
            c.execute("INSERT INTO stages VALUES (?,?,?)", (stage, canonical_json(binding), digest(binding)))

    def _chain_leaves(self, rows):
        children = {r['retry_of']: r for r in rows if r['retry_of']}
        leaves = []
        for base in (r for r in rows if not r['retry_of']):
            row = base
            visited = set()
            while row['request_id'] in children:
                if row['request_id'] in visited or row['status'] != 'ZERO_TOKEN_PROVEN':
                    raise HarnessError("invalid retry chain")
                visited.add(row['request_id'])
                nxt = children[row['request_id']]
                if nxt['identity_json'] != row['identity_json']:
                    raise HarnessError("retry changed complete request identity")
                row = nxt
            leaves.append(row)
        return leaves

    def _frozen(self, c):
        event = self._events(c).get('frozen_gate')
        frozen = None if event is None else json.loads(event['detail_json']).get('frozen')
        if not isinstance(frozen, dict) or digest(frozen) != event['artifact_sha256']:
            raise HarnessError('persisted probe freeze is missing or corrupted')
        return frozen

    def _closed_outcome(self, c, stage):
        """Authenticate stored closure with the same validator used to create it.

        The caller validates prerequisites in this transaction. Raw event()/snapshot()
        remain forensic reads; a stored PASS is never sufficient for confirmation.
        """
        event = self._events(c).get('outcome:' + stage)
        if event is None:
            raise HarnessError(f'{stage} has no closed outcome')
        detail = json.loads(event['detail_json'])
        outcome = detail.get('outcome')
        if outcome not in {'PASS', 'FAIL', 'BLOCKED'}:
            raise HarnessError('persisted stage outcome is invalid')
        frozen = self._frozen(c) if stage == 'budget_probe' and outcome == 'PASS' else None
        records = self._validate_outcome(c, stage, outcome=outcome,
            artifact_sha256=event['artifact_sha256'], artifact=detail.get('artifact'),
            diagnosis=detail.get('diagnosis'), frozen=frozen)
        if detail.get('records_sha256') != digest(records):
            raise HarnessError('persisted outcome records digest mismatch')
        return detail

    def _successful(self, c, stage):
        self._prerequisites(c, stage)
        event = self._events(c).get('outcome:' + stage)
        if event is None or json.loads(event['detail_json']).get('outcome') != 'PASS':
            raise HarnessError(f"{stage} has no successful closed outcome")
        self._closed_outcome(c, stage)

    def verify_stage_success(self, stage):
        with self._transaction() as c:
            self._successful(c, stage)

    def _prerequisites(self, c, stage):
        """Validate the dependency chain for both new work and reuse of closed results.

        These checks never require the requested stage to be open. Keeping them separate
        from mutation ordering permits valid replay after downstream stages have run,
        without grandfathering outcomes created by an earlier, unsafe implementation.
        """
        events = self._events(c)
        if any(k.startswith('suspended:') for k in events):
            raise HarnessError("pilot suspended; requires a new reviewed disposition")
        successor = c.execute("PRAGMA user_version").fetchone()[0] == 4
        if successor:
            self._validated_predecessor_lineage(c)
            if stage == TECHNICAL_STAGE:
                pass
            elif stage == 'producer_conformity':
                try:
                    self._successful(c, TECHNICAL_STAGE)
                except HarnessError as exc:
                    raise HarnessError(
                        "successor producer conformity requires successful technical qualification"
                    ) from exc
        if stage == 'producer_remediation' and ('remediation_authorized' not in events or 'remediation_waived' in events):
            raise HarnessError("remediation is not authorized")
        if stage in {'budget_probe', 'stability_gate'}:
            if c.execute("SELECT 1 FROM stages WHERE stage='alternate_conformity'").fetchone():
                self._successful(c, 'alternate_conformity')
        if stage == 'budget_probe':
            self._successful(c, 'producer_remediation' if 'remediation_authorized' in events else 'producer_conformity')
        if stage == 'stability_gate':
            self._successful(c, 'budget_probe')
            if 'frozen_gate' not in events:
                raise HarnessError("gate configuration is not authenticated by the probe")

    def _ready(self, c, stage):
        self._require_no_tokenizer_accounting_stop(c)
        self._prerequisites(c, stage)
        events, rows = self._events(c), self._rows(c)
        if 'outcome:' + stage in events:
            raise HarnessError("closed stage cannot be reopened")
        if stage in {'producer_conformity', 'producer_remediation', 'alternate_conformity'}:
            if any(r['stage'] in {'budget_probe', 'stability_gate'} for r in rows):
                raise HarnessError("producer stages must precede probe/gate")
        if stage == 'budget_probe' and any(r['stage'] == 'stability_gate' for r in rows):
            raise HarnessError("probe cannot follow gate")

    def _insert_intent(self, c, *, request_id, logical_id, model, producer, stage, stage_run, quota_kind, retry_of):
        rows = self._rows(c)
        predecessors = self._quota_predecessors(c)
        if len(rows) + len(predecessors) >= 200:
            raise HarnessError("pilot cumulative hard stop 200 reached")
        successor_extra = int(c.execute("PRAGMA user_version").fetchone()[0] == 4)
        max_calls = (160 if stage == 'alternate_conformity' or any(
            r['stage'] == 'alternate_conformity' for r in rows) else 152) + successor_extra
        if len(rows) >= max_calls:
            raise HarnessError(f"planned request maximum {max_calls + len(predecessors)} reached")
        predecessor_request_ids = {row["request_id"] for row in predecessors}
        if request_id in predecessor_request_ids or retry_of in predecessor_request_ids:
            raise HarnessError("predecessor lineage cannot be reused as a native request or retry")
        self._ready(c, stage)
        rows = self._validated_attempt_inventory(c)
        binding = self._binding(c, stage)
        if stage_run != digest(binding):
            raise HarnessError("stage_run must identify the exact immutable request plan")
        specs = [s for s in binding['requests'] if s['logical_id'] == logical_id]
        if len(specs) != 1 or (model, producer) != (specs[0]['model'], specs[0]['producer']):
            raise HarnessError("request differs from complete frozen identity")
        identity = canonical_json(specs[0])
        if not retry_of:
            base_rows = [r for r in rows if r['stage'] == stage and r['retry_of'] is None]
            if len(base_rows) >= len(binding['requests']) or binding['requests'][len(base_rows)]['logical_id'] != logical_id:
                raise HarnessError('duplicate or out-of-order logical base')
        if retry_of:
            original = next((r for r in rows if r['request_id'] == retry_of), None)
            if original is None or original['status'] != 'ZERO_TOKEN_PROVEN' or original['stage'] != stage or original['identity_json'] != identity:
                raise HarnessError("retry requires matching original and documented zero-token proof")
            self._validated_reconciliation(c, original)
            if any(r['retry_of'] == retry_of for r in rows):
                raise HarnessError("original already has a retry; retry only the proven zero-token leaf")
            if stage == 'stability_gate':
                raise HarnessError("gate requests are never repeatable")
            if stage == TECHNICAL_STAGE:
                raise HarnessError("technical qualification is never retryable")
        elif any(r['stage'] == stage and r['logical_id'] == logical_id for r in rows):
            raise HarnessError("duplicate logical base across restart/alias/directory")
        remediation = sum(r['quota_kind'] == 'remediation' for r in rows) + (quota_kind == 'remediation')
        transport = sum(r['quota_kind'] == 'transport' for r in rows) + (quota_kind == 'transport')
        if remediation > 8 or 8 * int(remediation > 0) + transport > 15:
            raise HarnessError("shared reserve constraint 8r+t<=15 violated")
        events = self._events(c)
        if transport > 7 and (stage == 'budget_probe' or 'remediation_waived' not in events):
            raise HarnessError("transport beyond seven requires waiver and is never available to probe")
        if quota_kind == 'remediation' and stage != 'producer_remediation':
            raise HarnessError("remediation quota is exclusive")
        if stage == 'producer_remediation' and quota_kind == 'base':
            raise HarnessError("remediation cannot use base quota")
        if (stage == TECHNICAL_STAGE) != (quota_kind == 'technical'):
            raise HarnessError("technical qualification requires its separate quota kind")
        if not isinstance(request_id, str) or not request_id:
            raise HarnessError("request id required")
        try:
            c.execute("INSERT INTO requests VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (request_id, logical_id, stage, stage_run, model, producer, quota_kind, retry_of, identity, 'INTENT', _utc_now(), None, None, None, None, None, None, None))
        except sqlite3.IntegrityError as exc:
            raise HarnessError("duplicate request or logical attempt") from exc

    def reserve_request(self, **value):
        with self._transaction() as c:
            self._insert_intent(c, quota_kind='base', retry_of=None, **value)

    def reserve_remediation_request(self, **value):
        with self._transaction() as c:
            self._insert_intent(c, stage='producer_remediation', quota_kind='remediation', retry_of=None, **value)

    def reserve_technical_request(self, **value):
        with self._transaction() as c:
            self._insert_intent(c, stage=TECHNICAL_STAGE, quota_kind='technical',
                                retry_of=None, **value)

    def reserve_transport_retry(self, **value):
        if value['stage'] == 'budget_probe':
            raise HarnessError("probe retries require an atomic complete triplet")
        if value['stage'] == TECHNICAL_STAGE:
            raise HarnessError("technical qualification is never retryable")
        with self._transaction() as c:
            self._insert_intent(c, quota_kind='transport', **value)

    def suspend_technical(self, request_id, *, reason):
        if not isinstance(reason, str) or not reason.strip():
            raise HarnessError("technical suspension requires a reason")
        with self._transaction() as c:
            row = c.execute("SELECT * FROM requests WHERE request_id=?", (request_id,)).fetchone()
            if row is None or row['stage'] != TECHNICAL_STAGE or row['status'] != 'COMPLETED':
                raise HarnessError("technical suspension requires one completed technical request")
            name = 'suspended:' + request_id
            if name in self._events(c):
                return
            response = c.execute("SELECT record_sha256 FROM responses WHERE request_id=?",
                                 (request_id,)).fetchone()
            if response is None or not HASH.fullmatch(response['record_sha256'] or ''):
                raise HarnessError("technical suspension requires a durable evaluated record")
            self._event(c, name, response['record_sha256'],
                        {'reason': reason, 'classification': 'technical_qualification_stop'})

    def reserve_probe_transport_triplet(self, requests: Iterable[dict[str, str]]):
        values = list(requests)
        if len(values) != 3 or len({v['retry_of'] for v in values}) != 3 or {v['condition'] for v in values} != {'A', 'B-LF', 'E-LF'}:
            raise HarnessError("probe retry requires three distinct original A/B-LF/E-LF requests")
        with self._transaction() as c:
            originals = []
            for v in values:
                r = c.execute("SELECT * FROM requests WHERE request_id=?", (v['retry_of'],)).fetchone()
                if r is None or json.loads(r['identity_json'])['condition'] != v['condition']:
                    raise HarnessError("probe original condition mismatch")
                originals.append(json.loads(r['identity_json']))
            if len({r['group'] for r in originals}) != 1:
                raise HarnessError("probe retry must preserve one original budget group")
            for v in values:
                self._insert_intent(c, stage='budget_probe', quota_kind='transport', **{k: v[k] for k in ('request_id','logical_id','model','producer','stage_run','retry_of')})

    def request(self, request_id):
        with closing(self._connect()) as c:
            r = c.execute("SELECT * FROM requests WHERE request_id=?", (request_id,)).fetchone()
            return dict(r) if r else None

    def leaf(self, stage, logical_id):
        with closing(self._connect()) as c:
            rows = [r for r in self._rows(c) if r['stage'] == stage and r['logical_id'] == logical_id]
            leaves = self._chain_leaves(rows)
            return dict(leaves[0]) if leaves else None

    def save_raw(self, request_id, raw, *, latency_ms=None):
        """First operation after transport returns; commits raw before parsing/identity checks."""
        text = canonical_json(raw)
        with self._transaction() as c:
            r = c.execute("SELECT status FROM requests WHERE request_id=?", (request_id,)).fetchone()
            if r is None or r[0] != 'INTENT':
                raise HarnessError("raw response needs unresolved intent")
            old = c.execute("SELECT raw_json FROM responses WHERE request_id=?", (request_id,)).fetchone()
            if old and old[0] != text:
                raise HarnessError("raw response cannot be overwritten")
            c.execute("INSERT OR IGNORE INTO responses VALUES (?,?,?,?,?)", (request_id, text, sha256_text(text), None, None))
            c.execute("INSERT OR IGNORE INTO receipts VALUES (?,?)", (request_id, canonical_json({'received_utc': _utc_now(), 'latency_ms': latency_ms})))

    def response(self, request_id):
        with closing(self._connect()) as c:
            row = c.execute("SELECT * FROM responses WHERE request_id=?", (request_id,)).fetchone()
            if row is None:
                return None
            if sha256_text(row['raw_json']) != row['raw_sha256'] or (row['record_json'] and sha256_text(row['record_json']) != row['record_sha256']):
                raise HarnessError("persisted response hash mismatch")
            return {'raw': json.loads(row['raw_json']), 'record': json.loads(row['record_json']) if row['record_json'] else None, 'capture': json.loads(c.execute('SELECT capture_json FROM receipts WHERE request_id=?', (request_id,)).fetchone()[0])}

    def complete_request(self, request_id, *, status, prompt_tokens=None, completion_tokens=None, total_tokens=None, latency_ms=None, proof_sha256=None, detail=None, record=None, transport_failure=False):
        if status not in {'COMPLETED', 'FAILED'}:
            raise HarnessError("zero-token status requires explicit reconcile_zero_token evidence")
        values = (prompt_tokens, completion_tokens, total_tokens)
        if any(x is not None and (type(x) is not int or x < 0) for x in values) or (all(x is not None for x in values) and total_tokens != prompt_tokens + completion_tokens):
            raise HarnessError("inconsistent token accounting")
        with self._transaction() as c:
            row = c.execute("SELECT * FROM requests WHERE request_id=?", (request_id,)).fetchone()
            raw = c.execute("SELECT * FROM responses WHERE request_id=?", (request_id,)).fetchone()
            if row is None or row['status'] != 'INTENT':
                raise HarnessError("completion requires unresolved intent")
            if transport_failure and (status != 'FAILED' or raw is not None or record is not None or not detail or not detail.get('error_type')):
                raise HarnessError('transport failure requires an explicit error and no response')
            if record is not None and raw is None:
                raise HarnessError('response record requires durable raw')
            if status == 'COMPLETED' and (raw is None or record is None):
                raise HarnessError("completed request requires durable raw and evaluated record")
            if record is not None:
                identity = json.loads(row['identity_json'])
                if record.get('request_id') != request_id or record.get('prompt_sha256') != identity['prompt_sha256']:
                    raise HarnessError("response record identity mismatch")
                if row['model'] == TOKENIZER_ACCOUNTING_MODEL:
                    self._validate_tokenizer_accounting_record(c, row, record)
                text = canonical_json(record)
                c.execute("UPDATE responses SET record_json=?,record_sha256=? WHERE request_id=?", (text, sha256_text(text), request_id))
            if row['proof_sha256'] is not None:
                if proof_sha256 is not None and proof_sha256 != row['proof_sha256']:
                    raise HarnessError('persisted proof/accounting commitment cannot be overwritten')
                proof_sha256 = row['proof_sha256']
            c.execute("UPDATE requests SET status=?,completed_utc=?,prompt_tokens=?,completion_tokens=?,total_tokens=?,latency_ms=?,proof_sha256=?,detail_json=? WHERE request_id=?", (status, _utc_now(), *values, latency_ms, proof_sha256, canonical_json(detail or {}), request_id))
            if transport_failure and row['stage'] == 'stability_gate':
                self._save_gate_transport_record(c, request_id)
            if record and record.get('identity_valid') is not True:
                self._event(c, 'suspended:' + request_id, digest(record), {'reason': 'response identity missing or changed'})

    def _save_gate_transport_record(self, c, request_id):
        """Persist invalidity from an observed transport failure or approved reconciliation.

        No SDK response is fabricated. Request metadata comes from the frozen plan/sample;
        usage and returned identity remain unknown. The immutable event survives restart.
        """
        row = c.execute("SELECT * FROM requests WHERE request_id=?", (request_id,)).fetchone()
        if row['stage'] != 'stability_gate' or row['status'] not in {'FAILED', 'ZERO_TOKEN_PROVEN'}:
            raise HarnessError('gate invalidity requires a resolved transport event')
        if c.execute("SELECT 1 FROM responses WHERE request_id=?", (request_id,)).fetchone():
            raise HarnessError('a received response cannot become a transport invalidity')
        events = self._events(c)
        if 'transport_invalidity:' + request_id in events:
            return
        spec = json.loads(row['identity_json'])
        frozen = json.loads(events['frozen_gate']['detail_json'])['frozen']
        prompts = [p for p in frozen['prompt_sample'] if p['prompt_id'] == spec['group']]
        if len(prompts) != 1 or prompts[0]['prompt_sha256'] != spec['prompt_sha256']:
            raise HarnessError('transport invalidity differs from frozen sample')
        prompt = prompts[0]
        error = json.loads(row['detail_json'] or '{}')
        reconciliation = events.get('reconciled:' + request_id)
        if not error.get('error_type') and reconciliation is None:
            raise HarnessError('missing transport observation or reconciliation')
        record = dict(
            record_kind='transport_invalidity', request_id=request_id,
            request_identity_sha256=sha256_text(row['identity_json']),
            **{k: prompt[k] for k in ('prompt_id','agent_id','case_id','condition','sample_role','prompt_sha256')},
            repetition=spec['repetition'], retry_count=0, generation=frozen['generation'],
            response_received=False, identity_valid=None, returned_model=None, system_fingerprint=None,
            response_id=None, raw_output=None, raw_output_sha256=None, received_utc=None,
            parsed_output=None, parse_valid_first_attempt=False, finish_reason=None,
            prompt_tokens=None, completion_tokens=None, total_tokens=None,
            latency_seconds=None if row['latency_ms'] is None else row['latency_ms']/1000,
            transport_error=error or {'error_type':'ReconciledNoResponse', 'message':'No response captured; zero-token proof accepted'},
            observed_utc=row['completed_utc'],
            reconciliation_sha256=None if reconciliation is None else reconciliation['artifact_sha256'])
        self._event(c, 'transport_invalidity:' + request_id, digest(record), {'record': record})

    def _gate_transport_record(self, c, row):
        if row['status'] == 'ZERO_TOKEN_PROVEN':
            self._validated_reconciliation(c, row)
        event = self._events(c).get('transport_invalidity:' + row['request_id'])
        if event is None:
            return None
        from .gate_rules import is_transport_invalidity
        record = json.loads(event['detail_json']).get('record')
        if not isinstance(record, dict):
            raise HarnessError('persisted transport invalidity is missing its record')
        if (row['stage'] != 'stability_gate' or row['status'] not in {'FAILED','ZERO_TOKEN_PROVEN'}
                or row['retry_of'] is not None or digest(record) != event['artifact_sha256']
                or record.get('request_id') != row['request_id']
                or record.get('request_identity_sha256') != sha256_text(row['identity_json'])
                or not is_transport_invalidity(record)
                or c.execute('SELECT 1 FROM responses WHERE request_id=?', (row['request_id'],)).fetchone()):
            raise HarnessError('persisted transport invalidity is not authentic')
        return record

    def gate_transport_record(self, request_id):
        with self._transaction() as c:
            row = c.execute('SELECT * FROM requests WHERE request_id=?', (request_id,)).fetchone()
            return None if row is None else self._gate_transport_record(c, row)

    def _evaluated_record(self, c, row):
        raw = c.execute('SELECT * FROM responses WHERE request_id=?', (row['request_id'],)).fetchone()
        if raw and raw['record_json']:
            if json.loads(raw['record_json']).get('record_kind') == 'transport_invalidity':
                raise HarnessError('a received response cannot be relabeled as transport invalidity')
            if sha256_text(raw['record_json']) != raw['record_sha256'] or sha256_text(raw['raw_json']) != raw['raw_sha256']:
                raise HarnessError('raw/record corruption')
            record = json.loads(raw['record_json'])
            identity = json.loads(row['identity_json'])
            if record.get('request_id') != row['request_id'] or record.get('prompt_sha256') != identity['prompt_sha256']:
                raise HarnessError('persisted record identity mismatch')
            if row['model'] == TOKENIZER_ACCOUNTING_MODEL:
                self._validate_tokenizer_accounting_record(c, row, record)
            return record
        return self._gate_transport_record(c, row)

    @staticmethod
    def _validate_zero_token_evidence(evidence, approval, row):
        """One content contract for acquisition, retry ancestors and reconciled gate.

        State eligibility belongs to callers. The returned IDs are an audit of checks
        actually passed, used by the contract guard; no caller supplies a subset.
        """
        if not isinstance(evidence, dict) or not isinstance(approval, dict):
            raise HarnessError('zero-token evidence and approval must be objects')
        checked = set()
        def require(field, condition):
            if not condition:
                raise HarnessError('zero-token content contract: ' + field)
            checked.add(field)
        nonempty_text = lambda value: isinstance(value, str) and bool(value.strip())
        require('evidence.request_id', evidence.get('request_id') == row['request_id'])
        require('evidence.request_identity_sha256', evidence.get('request_identity_sha256') == sha256_text(row['identity_json']))
        require('evidence.disposition', evidence.get('disposition') == 'not_generated')
        require('evidence.provider_request_id', nonempty_text(evidence.get('provider_request_id')))
        provider_evidence = evidence.get('provider_evidence')
        require('evidence.provider_evidence', nonempty_text(provider_evidence) or isinstance(provider_evidence, dict) and bool(provider_evidence))
        for field in ('prompt_tokens', 'completion_tokens', 'total_tokens'):
            require('evidence.' + field, type(evidence.get(field)) is int and evidence[field] == 0)
        require('approval.author', nonempty_text(approval.get('author')))
        require('approval.decision', approval.get('decision') == 'accepted')
        require('approval.evidence_sha256', approval.get('evidence_sha256') == row['proof_sha256'])
        return frozenset(checked)

    @staticmethod
    def _zero_token_content_digest(value):
        # Literal contract formula; distinct from the original file's byte hash.
        return digest(canonical_json(value))

    def _reconciliation_link(self, detail, row):
        return dict(request_id=row['request_id'], evidence_file_sha256=row['proof_sha256'],
                    approval_file_sha256=detail['approval_sha256'],
                    evidence_content_sha256=detail['evidence_content_sha256'],
                    approval_content_sha256=detail['approval_content_sha256'],
                    previous_status=detail['previous_status'])

    def _validated_reconciliation(self, c, row):
        events = self._events(c)
        event = events.get('reconciled:' + row['request_id'])
        marker = events.get('reconciled_integrity:' + row['request_id'])
        if row['status'] != 'ZERO_TOKEN_PROVEN' or event is None or marker is None:
            raise HarnessError('zero-token proof lacks durable content binding; reviewed reconciliation required')
        try:
            detail = json.loads(event['detail_json'])
            stored_link = json.loads(marker['detail_json'])
        except (ValueError, TypeError) as exc:
            raise HarnessError('zero-token persisted proof is not valid JSON') from exc
        required = {'evidence','approval','approval_sha256','previous_status',
                    'evidence_content_sha256','approval_content_sha256'}
        if not isinstance(detail, dict) or not required <= detail.keys():
            raise HarnessError('zero-token proof lacks durable content binding; reviewed reconciliation required')
        self._validate_zero_token_evidence(detail['evidence'], detail['approval'], row)
        for value in (row['proof_sha256'], detail['approval_sha256']):
            self._require_hash(value, 'zero-token original file')
        if (event['artifact_sha256'] != row['proof_sha256']
                or detail['previous_status'] not in {'INTENT','FAILED'}
                or c.execute('SELECT 1 FROM responses WHERE request_id=?', (row['request_id'],)).fetchone()):
            raise HarnessError('zero-token proof does not bind the recorded attempt')
        for key in ('evidence','approval'):
            if detail[key + '_content_sha256'] != self._zero_token_content_digest(detail[key]):
                raise HarnessError('zero-token persisted content digest mismatch')
        link = self._reconciliation_link(detail, row)
        if stored_link != link or marker['artifact_sha256'] != digest(link):
            raise HarnessError('zero-token durable integrity link mismatch')
        return detail

    def reconcile_zero_token(self, request_id, *, evidence_path: Path, approval_path: Path):
        # Hash and parse the same bytes; never reopen a file between those operations.
        try:
            evidence_bytes, approval_bytes = evidence_path.read_bytes(), approval_path.read_bytes()
            evidence, approval = json.loads(evidence_bytes), json.loads(approval_bytes)
        except (OSError, UnicodeError, ValueError) as exc:
            raise HarnessError('cannot read zero-token evidence/approval') from exc
        evidence_hash, approval_hash = sha256_bytes(evidence_bytes), sha256_bytes(approval_bytes)
        with self._transaction() as c:
            row = c.execute("SELECT * FROM requests WHERE request_id=?", (request_id,)).fetchone()
            if row is None or row['status'] not in {'INTENT', 'FAILED'}:
                raise HarnessError("reconciliation requires uncertain intent/failure")
            if c.execute("SELECT 1 FROM responses WHERE request_id=?", (request_id,)).fetchone():
                raise HarnessError("raw response exists; zero-token reconciliation forbidden")
            proof_row = dict(row, proof_sha256=evidence_hash)
            self._validate_zero_token_evidence(evidence, approval, proof_row)
            detail = dict(evidence=evidence, approval=approval, approval_sha256=approval_hash,
                          previous_status=row['status'],
                          evidence_content_sha256=self._zero_token_content_digest(evidence),
                          approval_content_sha256=self._zero_token_content_digest(approval))
            link = self._reconciliation_link(detail, proof_row)
            self._event(c, 'reconciled:' + request_id, evidence_hash, detail)
            self._event(c, 'reconciled_integrity:' + request_id, digest(link), link)
            c.execute("UPDATE requests SET status='ZERO_TOKEN_PROVEN',proof_sha256=?,completed_utc=? WHERE request_id=?", (evidence_hash, _utc_now(), request_id))
            if row['stage'] == 'stability_gate':
                self._save_gate_transport_record(c, request_id)

    def stage_records(self, stage):
        with closing(self._connect()) as c:
            rows = self._chain_leaves([r for r in self._rows(c) if r['stage'] == stage])
            return [record for row in rows if (record := self._evaluated_record(c, row)) is not None]

    def _validate_attempts(self, c, binding, rows):
        """Check every attempt against its plan, including non-leaf retry ancestors."""
        specs = {s['logical_id']: s for s in binding['requests']}
        by_id = {r['request_id']: r for r in rows}
        children = {r['retry_of']: r for r in rows if r['retry_of']}
        for row in rows:
            spec = specs.get(row['logical_id'])
            if (spec is None or row['identity_json'] != canonical_json(spec)
                    or row['stage_run'] != digest(binding)
                    or (row['model'], row['producer']) != (spec['model'], spec['producer'])):
                raise HarnessError('persisted request differs from immutable plan')
            expected_quota = ('transport' if row['retry_of'] else
                              'remediation' if row['stage'] == 'producer_remediation' else
                              'technical' if row['stage'] == TECHNICAL_STAGE else 'base')
            if row['quota_kind'] != expected_quota:
                raise HarnessError('persisted attempt quota differs from its role')
            if row['retry_of']:
                parent = by_id.get(row['retry_of'])
                if (parent is None or parent['status'] != 'ZERO_TOKEN_PROVEN'
                        or parent['identity_json'] != row['identity_json']
                        or row['quota_kind'] != 'transport'):
                    raise HarnessError('orphan or inconsistent retry attempt')
            if row['status'] == 'ZERO_TOKEN_PROVEN':
                self._validated_reconciliation(c, row)
        # _chain_leaves checks cycles reachable from bases; account for disconnected cycles too.
        reached = set()
        for row in (r for r in rows if not r['retry_of']):
            while row['request_id'] not in reached:
                reached.add(row['request_id'])
                row = children.get(row['request_id'])
                if row is None:
                    break
        if reached != set(by_id):
            raise HarnessError('retry attempts are disconnected from base coverage')

    def _validate_outcome(self, c, stage, *, outcome, artifact_sha256, artifact, diagnosis, frozen):
        """Shared closure/reconfirmation validation, without writes or nested connections."""
        binding = self._binding(c, stage)
        rows = [r for r in self._rows(c) if r['stage'] == stage]
        bases = [r for r in rows if not r['retry_of']]
        n = len(bases)
        if (stage == 'budget_probe' and n not in {3,6,9}) or (stage != 'budget_probe' and n != BASE_LIMITS[stage]):
            raise HarnessError("stage outcome requires complete distinct base coverage")
        if [r['logical_id'] for r in bases] != [s['logical_id'] for s in binding['requests'][:n]]:
            raise HarnessError("stage does not match frozen request order/coverage")
        self._validate_attempts(c, binding, rows)
        leaves = self._chain_leaves(rows)
        if any(r['status'] == 'INTENT' for r in leaves):
            raise HarnessError("stage cannot hide unresolved intents")
        records = [record for row in leaves if (record := self._evaluated_record(c, row)) is not None]
        if stage == 'stability_gate':
            if len(records) != n or any(r['status'] != 'COMPLETED' and self._gate_transport_record(c, r) is None for r in leaves):
                raise HarnessError('gate requires a response or durable transport invalidity for every attempt')
        if outcome == 'PASS':
            if len(records) != n or (stage != 'stability_gate' and (
                    any(r['status'] != 'COMPLETED' for r in leaves)
                    or any(r.get('identity_valid') is not True for r in records))):
                raise HarnessError("PASS requires resolved authenticated responses")
            if stage in {'producer_conformity','producer_remediation','alternate_conformity'} and not all(r.get('schema_valid_first_attempt') is True for r in records):
                raise HarnessError("producer PASS requires all R4-valid pairs")
            if stage == TECHNICAL_STAGE and not all(
                    r.get('technical_pass') is True
                    and r.get('reasoning_empty') is True
                    and r.get('rendering_control_accepted') is True
                    and r.get('scientific_use') == 'FORBIDDEN'
                    and r.get('finish_reason') == 'stop'
                    for r in records):
                raise HarnessError("technical qualification PASS contradicts its durable record")
            if stage == 'stability_gate':
                from .gate_rules import evaluate_stability_gate
                frozen_event = self._frozen(c)
                gate = evaluate_stability_gate(records, expected_prompts=frozen_event['prompt_sample'])
                if not all(gate[k] for k in ('t3_pass','t4_pass','t6_evaluable')):
                    raise HarnessError('gate outcome contradicts durable records')
            if stage == 'budget_probe':
                if any(all(r.get('parse_valid_first_attempt') is True and r.get('finish_reason') == 'stop' for r in records[i:i+3]) for i in range(0,len(records)-3,3)):
                    raise HarnessError('probe must select the first successful budget triplet')
                if frozen is None or frozen.get('generation') != records[-1].get('generation') or not all(r.get('generation') == frozen['generation'] and r.get('parse_valid_first_attempt') is True and r.get('finish_reason') == 'stop' for r in records[-3:]):
                    raise HarnessError("probe PASS must authenticate selected budget and complete successful triplet")
        if not isinstance(artifact, dict) or digest(artifact) != artifact_sha256 or artifact.get('records_sha256') != digest(records):
            raise HarnessError("outcome artifact must bind durable stage records")
        if diagnosis is not None and diagnosis not in DIAGNOSES:
            raise HarnessError("inadmissible producer remediation diagnosis")
        return records

    def record_stage_outcome(self, stage, *, outcome, artifact_sha256, artifact=None, diagnosis=None, frozen=None):
        if stage not in ACTIVE_STAGES or outcome not in {'PASS','FAIL','BLOCKED'}:
            raise HarnessError("unsupported stage outcome")
        self._require_hash(artifact_sha256, 'outcome artifact')
        with self._transaction() as c:
            previous = self._events(c).get('outcome:' + stage)
            replay = previous and previous['artifact_sha256'] == artifact_sha256 and json.loads(previous['detail_json'])['outcome'] == outcome
            if replay:
                self._prerequisites(c, stage)
            else:
                self._ready(c, stage)
            if replay:
                self._closed_outcome(c, stage)
            records = self._validate_outcome(c, stage, outcome=outcome,
                artifact_sha256=artifact_sha256, artifact=artifact, diagnosis=diagnosis, frozen=frozen)
            if replay:
                # Revalidate predecessors, coverage and durable records before rematerializing.
                # A replay must not insert events or reopen requests.
                if stage == 'budget_probe' and outcome == 'PASS':
                    event = self._events(c).get('frozen_gate')
                    if event is None or event['artifact_sha256'] != digest(frozen):
                        raise HarnessError('replayed freeze differs from the recorded probe')
                return
            self._event(c, 'outcome:' + stage, artifact_sha256, {'outcome': outcome, 'diagnosis': diagnosis, 'records_sha256': digest(records), 'artifact': artifact})
            if stage == 'budget_probe' and outcome == 'PASS':
                self._event(c, 'frozen_gate', digest(frozen), {'frozen': frozen})

    def authenticate_frozen(self, frozen):
        with self._transaction() as c:
            self._successful(c, 'budget_probe')
            event = self._events(c).get('frozen_gate')
            if event is None or event['artifact_sha256'] != digest(frozen):
                raise HarnessError("gate configuration differs from authenticated probe result")

    def authorize_remediation(self, *, diff_sha256=None, approval_sha256=None, template_sha256=None, diff_path=None, approval_path=None, template_path=None):
        if any(p is None for p in (diff_path, approval_path, template_path)):
            raise HarnessError("remediation requires concrete diff, approval and template bytes")
        diff, template, approval = Path(diff_path).read_bytes().decode('utf-8'), Path(template_path).read_bytes().decode('utf-8'), load_json(Path(approval_path))
        for p, expected in ((diff_path,diff_sha256),(approval_path,approval_sha256),(template_path,template_sha256)):
            if expected is not None and sha256_file(Path(p)) != expected:
                raise HarnessError("remediation artifact hash mismatch")
        with self._transaction() as c:
            events = self._events(c)
            if any(r['stage'] in {'budget_probe','stability_gate'} for r in self._rows(c)) or 'remediation_waived' in events:
                raise HarnessError("remediation forbidden after probe/gate or waiver")
            failed = events.get('outcome:producer_conformity')
            detail = json.loads(failed['detail_json']) if failed else {}
            rows = [r for r in self._rows(c) if r['stage'] == 'producer_conformity']
            failed_records = [self.response(r['request_id'])['record'] for r in self._chain_leaves(rows) if r['status'] == 'COMPLETED']
            if not any(r.get('schema_valid_first_attempt') is False and r.get('validation_class') == detail.get('diagnosis') for r in failed_records):
                raise HarnessError('remediation diagnosis must match a recorded producer validation defect')
            if detail.get('outcome') != 'FAIL' or detail.get('diagnosis') not in DIAGNOSES or any(r['status'] != 'COMPLETED' for r in self._chain_leaves(rows)):
                raise HarnessError("remediation requires diagnosed prompt defect; unresolved timeout is not admissible")
            binding = self._binding(c, 'producer_conformity')
            expected_diff = ''.join(difflib.unified_diff(binding['template_text'].splitlines(True), template.splitlines(True), fromfile='before', tofile='after'))
            if not expected_diff or diff != expected_diff or approval.get('decision') != 'accepted' or not approval.get('author') or approval.get('diff_sha256') != sha256_text(diff) or approval.get('template_sha256') != sha256_text(template) or approval.get('initial_binding_sha256') != digest(binding) or approval.get('diagnosis') != detail['diagnosis']:
                raise HarnessError("approval must bind exact diff, template, diagnosis and original eight-case plan")
            self._event(c, 'remediation_authorized', sha256_file(Path(approval_path)), {'diff_sha256': sha256_text(diff), 'template_sha256': sha256_text(template), 'template_text': template, 'approval': approval})

    def waive_remediation(self, *, approval_sha256):
        with self._transaction() as c:
            if 'remediation_authorized' in self._events(c):
                raise HarnessError("remediation already authorized")
            self._event(c, 'remediation_waived', approval_sha256, {'effect': 'no later remediation'})

    def snapshot(self):
        with closing(self._connect()) as c:
            rows, events = self._rows(c), self._events(c)
            predecessors = self._quota_predecessors(c)
            successor = c.execute("PRAGMA user_version").fetchone()[0] == 4
            raw_count = c.execute("SELECT count(*) FROM responses").fetchone()[0]
        by_stage = {s: sum(r['stage'] == s for r in rows) for s in sorted(ACTIVE_STAGES)}
        remediation = sum(r['quota_kind'] == 'remediation' for r in rows)
        transport = sum(r['quota_kind'] == 'transport' for r in rows)
        planned_without_alternate = 152 + int(successor) + len(predecessors)
        planned_with_alternate = 160 + int(successor) + len(predecessors)
        return dict(pilot_id=self.pilot_id, ledger_path=str(self.path),
                    requests_cumulative=len(rows)+len(predecessors), native_requests=len(rows),
                    historical_requests=len(predecessors),
                    predecessor_lineage_requests=len(predecessors) if successor else 0,
                    requests_by_stage=by_stage,
                    unresolved_intents=sum(r['status'] == 'INTENT' for r in rows),
                    remediation_calls=remediation, transport_calls=transport,
                    reserve_equation_value=8*int(remediation>0)+transport, reserve_limit=15,
                    planned_maximum=(planned_with_alternate if by_stage['alternate_conformity']
                                     else planned_without_alternate),
                    planned_maximum_without_alternate=planned_without_alternate,
                    planned_maximum_with_alternate=planned_with_alternate,
                    hard_stop=200,
                    hard_stop_margin_at_planned_maximum=200-planned_with_alternate,
                    durable_responses=raw_count, events=sorted(events))
