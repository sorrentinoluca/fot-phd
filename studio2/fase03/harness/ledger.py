"""Durable, fail-closed pilot state machine. All decisions use one SQLite transaction.

A new ledger must be shared by all runners of one pilot. Legacy ledgers are
read-only evidence: migration requires an independently reviewed reconciliation.
No uncertain request is ever resent implicitly.
"""
from __future__ import annotations

from contextlib import closing, contextmanager
from dataclasses import dataclass
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

# 7.4: the final scientific batch runs on its own target with its own quota envelope.
# The pilot numbers above stay exactly as they are; a ledger declares which envelope it
# lives under once, at creation, and can never be reopened under another one.
FINAL_PASS_STAGES = ("final_batch_r1", "final_batch_r2", "final_batch_r3")
FINAL_PASS_LIMIT = 2244
FINAL_CANARY_STAGE = "final_canary"
TECHNICAL_VERIFICATION_STAGE = "technical_verification"
FINAL_BATCH_STAGES = set(FINAL_PASS_STAGES) | {FINAL_CANARY_STAGE, TECHNICAL_VERIFICATION_STAGE}
# Author decision 2026-09-17 (7.4-FIX-2): X = 0. No technical verification is planned, so
# the stage stays defined with quota zero and every reservation on it is refused. A future
# technical verification requires a declared protocol revision, not a local widening.
TECHNICAL_VERIFICATION_QUOTA = 0
FINAL_BATCH_LIMITS = {**{stage: FINAL_PASS_LIMIT for stage in FINAL_PASS_STAGES},
                      FINAL_CANARY_STAGE: 70,
                      TECHNICAL_VERIFICATION_STAGE: TECHNICAL_VERIFICATION_QUOTA}
# Author decision D3 (2026-09-17) replaces the absolute Q=0 of the candidate: a retry is
# admitted only against proof that no token was generated. The cumulative ceiling is a
# quota of its own, separate from the scientific stage quotas, so a transport storm can
# never finance itself on scientific slots. Order of magnitude from the pilot: 8 pre-
# generation failures out of 156 requests (5.13%); on 6,802 planned calls that is ~349
# expected, and 400 leaves ~15% headroom while costing at most ~4.9 h at the gate p95.
# (The pilot rate is computed on 6,802 planned calls; with X = 0 the planned calls are
# 6,802 as well: 6,732 scientific plus 70 canary.)
FINAL_RETRY_QUOTA = 400
# Five consecutive failed technical attempts on the same service, retries included.
# Protection against an unavailable service; no statistical meaning (D3).
FINAL_CONSECUTIVE_FAILURE_STOP = 5
TECHNICAL_FAILURE_STOP_PREFIX = "technical_failure_stop:"
PROFILE_EVENT_PREFIX = "ledger_profile:"
CANARY_PASS_PREFIX = "canary_pass:"
CANARY_MARKED_PREFIX = "canary_marked:"
CANARY_STOP_PREFIX = "canary_stop:"
CANARY_MAX_DAYS = 7
CANARY_DAILY_CALLS = 10


@dataclass(frozen=True)
class LedgerProfile:
    """Immutable quota envelope of one ledger."""

    name: str
    stages: frozenset
    base_limits: dict
    planned_maximum: int
    hard_stop: int
    quota_kinds: frozenset
    # D3: cumulative ceiling of proven-zero-token retries, counted apart from the
    # per-stage scientific quotas. Zero keeps the historical behaviour.
    retry_quota: int = 0
    # D3: consecutive failed technical attempts on one service that stop the campaign.
    consecutive_failure_stop: int = 0


PILOT_PROFILE = LedgerProfile(
    name="pilot", stages=frozenset(ACTIVE_STAGES), base_limits=dict(BASE_LIMITS),
    planned_maximum=160, hard_stop=200,
    quota_kinds=frozenset({"base", "remediation", "transport", "technical", "requalification"}))
FINAL_BATCH_PROFILE = LedgerProfile(
    name="final_batch", stages=frozenset(FINAL_BATCH_STAGES), base_limits=dict(FINAL_BATCH_LIMITS),
    planned_maximum=sum(FINAL_BATCH_LIMITS.values()) + FINAL_RETRY_QUOTA,
    hard_stop=sum(FINAL_BATCH_LIMITS.values()) + FINAL_RETRY_QUOTA,
    quota_kinds=frozenset({"base", "transport"}),
    retry_quota=FINAL_RETRY_QUOTA,
    consecutive_failure_stop=FINAL_CONSECUTIVE_FAILURE_STOP)
PROFILES = {profile.name: profile for profile in (PILOT_PROFILE, FINAL_BATCH_PROFILE)}
DIAGNOSES = {"structure", "identifiers", "cap", "leakage"}
TOKENIZER_ACCOUNTING_SNAPSHOT = "Qwen/Qwen3.5-122B-A10B-FP8@a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9"
TOKENIZER_ACCOUNTING_MODEL = "qwen3.5-122b"
TOKENIZER_ACCOUNTING_ARTIFACT_VERSION = "TOKENIZER_ACCOUNTING_2"
ACCOUNTING_STOP_EVENT = "stop:tokenizer_accounting"
ACCOUNTING_STOP_RECONCILED_EVENT = "stop_reconciled:tokenizer_accounting"
ACCOUNTING_STOP_APPROVAL_KEYS = {"decision", "author", "stop_artifact_sha256", "stop_request_id",
                                 "cause", "fixed_commit", "ledger_sha256_before"}
COMMIT = re.compile(r"^[0-9a-f]{40}$")
CONFIG_REVISION_PREFIX = "config_revision:"
STAGE_REBINDING_PREFIX = "stage_rebinding:"
SUSPENSION_RECONCILED_PREFIX = "suspension_reconciled:"
IDENTITY_SUSPENSION_REASON = "response identity missing or changed"
REQUALIFICATION_STAGES = {"alternate_conformity"}
REQUALIFICATION_LIMIT = 1
# Flattened configuration paths an approved revision may change (03.13-REV27B).
CONFIG_REVISION_ALLOWED = (
    ("d9", "producer_configs", "27B"),
    ("d9", "services", "27B", "expected_response", "system_fingerprint"),
    ("d9", "services", "27B", "documentation"),
    ("approved_producer_config_sha256",),
    ("execution_authorization",),
)
CONFIG_REVISION_APPROVAL_KEYS = {"decision", "author", "previous_sha256", "new_sha256", "reason"}
SUSPENSION_APPROVAL_KEYS = {"decision", "author", "request_id", "suspension_artifact_sha256",
                            "observed_identity", "config_content_sha256"}
REBINDING_BINDING_KEYS = {"execution_config", "provider", "provider_file_sha256", "provider_reference"}
REBINDING_PROVIDER_KEYS = {"extra_body", "expected_response", "thinking_token_budget"}


def _diff_paths(before, after, prefix=()):
    """Smallest changed paths; a changed list or scalar is one leaf."""
    if isinstance(before, dict) and isinstance(after, dict):
        paths = []
        for key in sorted(set(before) | set(after)):
            if key not in before or key not in after:
                paths.append(prefix + (key,))
            elif before[key] != after[key]:
                paths.extend(_diff_paths(before[key], after[key], prefix + (key,)))
        return paths
    return [] if before == after else [prefix]


def _embedded_json(stored, role):
    """Rebuild approval bytes embedded in an event and verify their three bindings."""
    if (not isinstance(stored, dict) or set(stored) != {"path", "sha256", "content", "utf8"}
            or not isinstance(stored.get("path"), str) or not Path(stored["path"]).is_absolute()
            or not isinstance(stored.get("utf8"), str)):
        raise HarnessError(role + " approval copy is incomplete")
    data = stored["utf8"].encode("utf-8")
    try:
        value = json.loads(data)
    except ValueError as exc:
        raise HarnessError(role + " approval copy is not JSON") from exc
    if value != stored["content"] or sha256_bytes(data) != stored["sha256"]:
        raise HarnessError(role + " approval copy is corrupted")
    return value


def _read_embedded_json(path, role):
    path = Path(path).resolve()
    try:
        data = path.read_bytes()
        text = data.decode("utf-8")
        value = json.loads(text)
    except (OSError, UnicodeError, ValueError) as exc:
        raise HarnessError(role + " file is unavailable or invalid") from exc
    return value, {"path": str(path), "sha256": sha256_bytes(data), "content": value, "utf8": text}


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
    def __init__(self, path: Path, *, pilot_id: str, identity_path: Path | None = None,
                 profile: str = "pilot"):
        if profile not in PROFILES:
            raise HarnessError("unknown ledger profile")
        self.profile = PROFILES[profile]
        if not path.is_absolute():
            raise HarnessError("pilot ledger path must be absolute and shared across worktrees")
        if identity_path is not None and not Path(identity_path).is_absolute():
            raise HarnessError("pilot ledger identity path must be absolute")
        if not re.fullmatch(r"[A-Za-z0-9_.-]{8,120}", pilot_id):
            raise HarnessError("invalid pilot_id")
        self.path, self.pilot_id = path.resolve(), pilot_id
        self.identity_path = (Path(identity_path).resolve()
                              if identity_path is not None else self.path)
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
            self._bind_profile(c)

    def _bind_profile(self, c):
        """Create-once declaration of the quota envelope.

        A ledger written before 7.4 carries no declaration and is, by definition, a pilot
        ledger: it is never rewritten here. Any other profile records its name once and
        every later open is refused if it does not match.
        """
        declared = [row[0] for row in c.execute("SELECT event FROM events")
                    if row[0].startswith(PROFILE_EVENT_PREFIX)]
        if len(declared) > 1:
            raise HarnessError("ledger declares more than one quota profile")
        if declared:
            if declared[0] != PROFILE_EVENT_PREFIX + self.profile.name:
                raise HarnessError("ledger profile differs from the declared quota envelope")
            return
        if self.profile.name == "pilot":
            return
        if c.execute("SELECT count(*) FROM requests").fetchone()[0]:
            raise HarnessError("a ledger with requests cannot adopt a new quota envelope")
        detail = {"profile": self.profile.name,
                  "base_limits": dict(sorted(self.profile.base_limits.items())),
                  "planned_maximum": self.profile.planned_maximum,
                  "hard_stop": self.profile.hard_stop,
                  "quota_kinds": sorted(self.profile.quota_kinds),
                  "retry_quota": self.profile.retry_quota,
                  "consecutive_failure_stop": self.profile.consecutive_failure_stop}
        self._event(c, PROFILE_EVENT_PREFIX + self.profile.name, digest(detail), detail)

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
            if stage not in self.profile.stages:
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
                expected_ledger={'path': str(self.identity_path), 'pilot_id': self.pilot_id})
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

    def _validated_predecessor_lineage(
            self, c, *, package_path=None, approval_path=None,
            source_package_path=None, source_approval_path=None):
        """Reauthenticate every durable lineage field against its approved artifacts."""
        rows = self._lineage_rows(c)
        version = c.execute("PRAGMA user_version").fetchone()[0]
        events = [row for name, row in self._events(c).items()
                  if name.startswith("successor_lineage:")]
        if not rows and version in {2, 3} and not events:
            if (package_path is not None or approval_path is not None
                    or source_package_path is not None or source_approval_path is not None):
                raise HarnessError("successor lineage import is required before D9 use")
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
        validation_package_path = (Path(source_package_path).resolve()
                                   if source_package_path is not None else stored_package_path)
        validation_approval_path = (Path(source_approval_path).resolve()
                                    if source_approval_path is not None else stored_approval_path)
        from .successor import validate_successor_lineage_artifacts
        validated = validate_successor_lineage_artifacts(
            validation_package_path, validation_approval_path,
            expected_ledger={"path": str(self.identity_path), "pilot_id": self.pilot_id})
        if (validated["package_sha256"] != package_ref["sha256"]
                or validated["approval_sha256"] != approval_ref["sha256"]):
            raise HarnessError("successor lineage staged bytes differ from durable references")
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

    def _classified_successor_lineage(
            self, c, *, package_path=None, approval_path=None,
            source_package_path=None, source_approval_path=None):
        """Classify from durable evidence, then authenticate the complete successor lineage.

        ``user_version`` is only one consistency field.  It cannot hide durable rows or
        events, and caller-required successor artifacts cannot fall back to generic mode.
        """
        rows = self._lineage_rows(c)
        version = c.execute("PRAGMA user_version").fetchone()[0]
        events = [name for name in self._events(c)
                  if name.startswith("successor_lineage:")]
        requested = (package_path is not None or approval_path is not None
                     or source_package_path is not None or source_approval_path is not None)
        if rows or events or version == 4 or requested:
            return True, self._validated_predecessor_lineage(
                c, package_path=package_path, approval_path=approval_path,
                source_package_path=source_package_path,
                source_approval_path=source_approval_path)
        if version not in {2, 3}:
            raise HarnessError("ledger version is incompatible with durable lineage")
        return False, []

    def _quota_context(self, c):
        successor, rows = self._classified_successor_lineage(c)
        if successor:
            if self._historical_rows(c):
                raise HarnessError("successor lineage cannot coexist with external history rows")
            return successor, rows
        return successor, self._validated_external_history(c)

    def _quota_predecessors(self, c):
        return self._quota_context(c)[1]

    def reconcile_successor_lineage(
            self, *, package_path: Path, approval_path: Path,
            durable_package_path: Path | None = None,
            durable_approval_path: Path | None = None):
        """Import the reviewed predecessor S=5 once; never copy predecessor rows."""
        package_path, approval_path = Path(package_path).resolve(), Path(approval_path).resolve()
        durable_package_path = (Path(durable_package_path).resolve()
                                if durable_package_path is not None else package_path)
        durable_approval_path = (Path(durable_approval_path).resolve()
                                 if durable_approval_path is not None else approval_path)
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
                expected_ledger={"path": str(self.identity_path), "pilot_id": self.pilot_id})
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
                          "path": str(durable_package_path),
                          "sha256": validated["package_sha256"]},
                      "approval_reference": {
                          "path": str(durable_approval_path),
                          "sha256": validated["approval_sha256"]}}
            self._event(c, "successor_lineage:" + validated["package_sha256"],
                        validated["package_sha256"], detail)
            c.execute("PRAGMA user_version=4")
            self._validated_predecessor_lineage(
                c, package_path=durable_package_path,
                approval_path=durable_approval_path,
                source_package_path=package_path,
                source_approval_path=approval_path)
            return {"status": "RECONCILED", "predecessor_requests": 5}

    def _events(self, c):
        return {r['event']: r for r in c.execute("SELECT * FROM events")}

    # --- 03.13-REV27B: approved configuration revisions -------------------------------
    @staticmethod
    def _validate_config_revision_content(previous, new):
        if not isinstance(previous, dict) or not isinstance(new, dict):
            raise HarnessError('config revision requires two JSON objects')
        changed = _diff_paths(previous, new)
        if not changed:
            raise HarnessError('config revision changes nothing')
        allowed = lambda path: any(path[:len(a)] == a for a in CONFIG_REVISION_ALLOWED)
        outside = [".".join(map(str, path)) for path in changed if not allowed(path)]
        if outside:
            raise HarnessError('config revision changes keys outside the approved set: ' + ", ".join(outside))
        old_d9, new_d9 = previous.get('d9') or {}, new.get('d9') or {}
        if (old_d9.get('producer_configs', {}).get('122B') != new_d9.get('producer_configs', {}).get('122B')
                or sorted(new.get('approved_producer_config_sha256', []))
                != sorted(new_d9.get('producer_configs', {}).values())):
            raise HarnessError('config revision must keep the producer allowlist equal to the D9 roles')
        return sorted(".".join(map(str, path)) for path in changed)

    def _config_chain(self, c):
        """Return [C0, C1, ..., Cn] after re-authenticating every revision, or []."""
        events = sorted(((int(name[len(CONFIG_REVISION_PREFIX):]), row)
                         for name, row in self._events(c).items()
                         if name.startswith(CONFIG_REVISION_PREFIX)), key=lambda item: item[0])
        chain = []
        for position, (number, row) in enumerate(events, 1):
            try:
                detail = json.loads(row['detail_json'])
                if (number != position
                        or set(detail) != {'revision', 'previous', 'new', 'changed_keys', 'approval'}
                        or detail['revision'] != number):
                    raise HarnessError('fields')
                previous, new = detail['previous'], detail['new']
                for side in (previous, new):
                    if (not isinstance(side, dict)
                            or set(side) != {'file_sha256', 'content_sha256', 'content'}
                            or side['content_sha256'] != digest(side['content'])
                            or not HASH.fullmatch(side['file_sha256'])):
                        raise HarnessError('side')
                approval = _embedded_json(detail['approval'], 'config revision')
                if (not isinstance(approval, dict) or set(approval) != CONFIG_REVISION_APPROVAL_KEYS
                        or approval['decision'] != 'accepted'
                        or not isinstance(approval['author'], str) or not approval['author'].strip()
                        or not isinstance(approval['reason'], str) or not approval['reason'].strip()
                        or approval['previous_sha256'] != previous['file_sha256']
                        or approval['new_sha256'] != new['file_sha256']
                        or row['artifact_sha256'] != new['content_sha256']
                        or detail['changed_keys'] != self._validate_config_revision_content(
                            previous['content'], new['content'])
                        or (chain and previous['content'] != chain[-1])):
                    raise HarnessError('binding')
            except (HarnessError, KeyError, TypeError, ValueError, AttributeError) as exc:
                raise HarnessError('FATAL: config revision chain is corrupted') from exc
            if not chain:
                chain.append(previous['content'])
            chain.append(new['content'])
        return chain

    def config_revisions(self):
        with self._transaction() as c:
            return self._config_chain(c)

    def _require_accepted_config(self, c, stored, current=None):
        """A stored execution_config is valid if equal to the current one or, once revisions
        exist, if it is a member of the recorded chain whose head is the current one."""
        chain = self._config_chain(c)
        if not chain:
            if current is not None and stored != current:
                raise HarnessError('execution configuration differs and no approved config revision exists')
            return
        if stored not in chain:
            raise HarnessError('execution configuration is not a recorded config revision')
        if current is not None and current != chain[-1]:
            raise HarnessError('execution configuration is not the head of the recorded config revision chain')

    def require_current_config(self, config, connection=None):
        def check(c):
            chain = self._config_chain(c)
            if chain and config != chain[-1]:
                raise HarnessError(
                    'execution configuration is not the head of the recorded config revision chain')
        if connection is not None:
            return check(connection)
        with self._transaction() as c:
            check(c)

    def config_accepted(self, stored, current):
        with self._transaction() as c:
            self._require_accepted_config(c, stored, current)
        return True

    def record_config_revision(self, *, previous_config_path: Path, new_config_path: Path,
                               approval_path: Path):
        """Record one author-approved revision; existing bindings and requests stay unchanged."""
        previous, previous_ref = _read_embedded_json(previous_config_path, 'previous configuration')
        new, new_ref = _read_embedded_json(new_config_path, 'new configuration')
        approval, approval_ref = _read_embedded_json(approval_path, 'config revision approval')
        with self._transaction() as c:
            chain = self._config_chain(c)
            if chain and chain[-1] == new:
                event = self._events(c)[f'{CONFIG_REVISION_PREFIX}{len(chain) - 1}']
                if json.loads(event['detail_json'])['approval']['sha256'] != approval_ref['sha256']:
                    raise HarnessError('config revision already recorded with another approval')
                return {'status': 'ALREADY_RECORDED', 'revision': len(chain) - 1}
            changed = self._validate_config_revision_content(previous, new)
            if (not isinstance(approval, dict) or set(approval) != CONFIG_REVISION_APPROVAL_KEYS
                    or approval.get('decision') != 'accepted'
                    or not isinstance(approval.get('author'), str) or not approval['author'].strip()
                    or not isinstance(approval.get('reason'), str) or not approval['reason'].strip()
                    or approval.get('previous_sha256') != previous_ref['sha256']
                    or approval.get('new_sha256') != new_ref['sha256']):
                raise HarnessError('config revision approval does not bind these two configurations')
            if chain and chain[-1] != previous:
                raise HarnessError('config revision must start from the current head')
            stored = [json.loads(r['binding_json']).get('execution_config')
                      for r in c.execute('SELECT binding_json FROM stages')]
            if not chain and any(value is not None and value != previous for value in stored):
                raise HarnessError('config revision must start from the configuration of every durable binding')
            if any(r['status'] == 'INTENT' for r in self._rows(c)):
                raise HarnessError('config revision requires no unresolved intent')
            from .guards import require_execution
            require_execution(previous)
            require_execution(new)
            number = len(chain) if chain else 1
            detail = {'revision': number,
                      'previous': {'file_sha256': previous_ref['sha256'],
                                   'content_sha256': digest(previous), 'content': previous},
                      'new': {'file_sha256': new_ref['sha256'],
                              'content_sha256': digest(new), 'content': new},
                      'changed_keys': changed, 'approval': approval_ref}
            self._event(c, f'{CONFIG_REVISION_PREFIX}{number}', digest(new), detail)
            self._config_chain(c)
            return {'status': 'RECORDED', 'revision': number, 'changed_keys': changed}

    # --- stage rebinding after an approved revision -----------------------------------
    def _stage_runs(self, c, stage):
        """Every binding digest a persisted attempt of this stage may carry."""
        row = c.execute("SELECT binding_sha256 FROM stages WHERE stage=?", (stage,)).fetchone()
        prefix = f'{STAGE_REBINDING_PREFIX}{stage}:'
        events = sorted(((int(name[len(prefix):]), r) for name, r in self._events(c).items()
                         if name.startswith(prefix)), key=lambda item: item[0])
        runs = []
        chain = self._config_chain(c) if events else []
        for position, (number, event) in enumerate(events, 1):
            try:
                detail = json.loads(event['detail_json'])
                if (number != position
                        or set(detail) != {'stage', 'revision', 'previous_binding',
                                           'previous_sha256', 'new_sha256'}
                        or detail['stage'] != stage or detail['revision'] != number
                        or digest(detail['previous_binding']) != detail['previous_sha256']
                        or event['artifact_sha256'] != detail['new_sha256']
                        or detail['previous_binding'].get('execution_config') not in chain
                        or (runs and runs[-1] != detail['previous_sha256'])):
                    raise HarnessError('fields')
            except (HarnessError, KeyError, TypeError, ValueError, AttributeError) as exc:
                raise HarnessError('FATAL: stage rebinding history is corrupted') from exc
            if not runs:
                runs.append(detail['previous_sha256'])
            runs.append(detail['new_sha256'])
        if runs and (row is None or runs[-1] != row['binding_sha256']):
            raise HarnessError('FATAL: stage rebinding history differs from the current binding')
        return runs or ([row['binding_sha256']] if row else [])

    def _rebind_stage(self, c, stage, old, new):
        if stage not in REQUALIFICATION_STAGES:
            raise HarnessError("stage inputs changed across alias, directory or restart")
        chain = self._config_chain(c)
        if not chain:
            raise HarnessError("stage inputs changed and no approved config revision exists")
        from .d9 import model_for_stage, no_thinking_template_kwargs
        role = model_for_stage(stage)
        changed = {k for k in set(old) | set(new) if old.get(k) != new.get(k)}
        if set(old) != set(new) or not changed <= REBINDING_BINDING_KEYS:
            raise HarnessError("stage rebinding may change only configuration and provider")
        if old['execution_config'] not in chain[:-1] or new['execution_config'] != chain[-1]:
            raise HarnessError("stage rebinding must move a recorded revision to the current head")
        old_provider, new_provider = old['provider'], new['provider']
        provider_changed = {k for k in set(old_provider) | set(new_provider)
                            if old_provider.get(k) != new_provider.get(k)}
        extra = new_provider.get('extra_body')
        strip = lambda value: {k: v for k, v in value.items() if k != 'system_fingerprint'}
        if (not provider_changed <= REBINDING_PROVIDER_KEYS
                or not isinstance(extra, dict) or set(extra) != {'chat_template_kwargs'}
                or no_thinking_template_kwargs(extra['chat_template_kwargs']) != extra['chat_template_kwargs']
                or new_provider.get('thinking_token_budget') is not None
                or strip(old_provider['expected_response']) != strip(new_provider['expected_response'])
                or old['provider_file_sha256'] != old['execution_config']['d9']['producer_configs'][role]
                or new['provider_file_sha256'] != new['execution_config']['d9']['producer_configs'][role]):
            raise HarnessError("stage rebinding provider change is outside the approved 27B requalification")
        events = self._events(c)
        if 'outcome:' + stage in events:
            raise HarnessError("closed stage cannot be rebound")
        if any(r['status'] == 'INTENT' for r in self._rows(c) if r['stage'] == stage):
            raise HarnessError("stage rebinding requires no unresolved intent")
        prefix = f'{STAGE_REBINDING_PREFIX}{stage}:'
        number = sum(name.startswith(prefix) for name in events) + 1
        self._event(c, f'{prefix}{number}', digest(new),
                    {'stage': stage, 'revision': number, 'previous_binding': old,
                     'previous_sha256': digest(old), 'new_sha256': digest(new)})
        c.execute("UPDATE stages SET binding_json=?, binding_sha256=? WHERE stage=?",
                  (canonical_json(new), digest(new), stage))
        self._stage_runs(c, stage)

    # --- identity suspension reconciliation --------------------------------------------
    def _suspension_identity_check(self, c, request_id, observed, config_content_sha256):
        row = c.execute('SELECT * FROM requests WHERE request_id=?', (request_id,)).fetchone()
        response = c.execute('SELECT * FROM responses WHERE request_id=?', (request_id,)).fetchone()
        if (row is None or row['status'] != 'COMPLETED' or response is None
                or response['record_json'] is None):
            raise HarnessError('suspension reconciliation requires a completed request with a durable record')
        if (sha256_text(response['raw_json']) != response['raw_sha256']
                or sha256_text(response['record_json']) != response['record_sha256']):
            raise HarnessError('suspended response hash mismatch')
        raw, record = json.loads(response['raw_json']), json.loads(response['record_json'])
        durable = {'returned_model': raw.get('model'), 'system_fingerprint': raw.get('system_fingerprint')}
        if (observed != durable or record.get('identity_valid') is not False
                or record.get('returned_model') != durable['returned_model']
                or record.get('system_fingerprint') != durable['system_fingerprint']):
            raise HarnessError('observed identity differs from the durable suspended response')
        configs = [value for value in self._config_chain(c) if digest(value) == config_content_sha256]
        if not configs:
            raise HarnessError('suspension reconciliation requires a recorded config revision')
        from .d9 import model_for_stage
        from .guards import response_identity_valid
        expected = configs[0]['d9']['services'][model_for_stage(row['stage'])]['expected_response']
        if not response_identity_valid(observed, expected):
            raise HarnessError('observed identity is not accepted by the config revision')
        return row

    def _validated_suspension_reconciliation(self, c, suspended, event):
        request_id = suspended['event'].split(':', 1)[1]
        try:
            stop = json.loads(suspended['detail_json'])
            detail = json.loads(event['detail_json'])
            if (stop != {'reason': IDENTITY_SUSPENSION_REASON}
                    or set(detail) != {'request_id', 'suspension_artifact_sha256', 'observed_identity',
                                       'config_content_sha256', 'approval'}
                    or detail['request_id'] != request_id
                    or detail['suspension_artifact_sha256'] != suspended['artifact_sha256']
                    or event['artifact_sha256'] != suspended['artifact_sha256']):
                raise HarnessError('fields')
            approval = _embedded_json(detail['approval'], 'suspension reconciliation')
            if (not isinstance(approval, dict) or set(approval) != SUSPENSION_APPROVAL_KEYS
                    or approval['decision'] != 'accepted'
                    or not isinstance(approval['author'], str) or not approval['author'].strip()
                    or any(approval[k] != detail[k] for k in (
                        'request_id', 'suspension_artifact_sha256',
                        'observed_identity', 'config_content_sha256'))):
                raise HarnessError('approval')
            self._suspension_identity_check(c, request_id, detail['observed_identity'],
                                            detail['config_content_sha256'])
        except (HarnessError, KeyError, TypeError, ValueError, AttributeError) as exc:
            raise HarnessError('FATAL: suspension reconciliation is corrupted or no longer valid') from exc
        return detail

    def _unreconciled_suspensions(self, c):
        events = self._events(c)
        pending = []
        for name, row in events.items():
            if not name.startswith('suspended:'):
                continue
            event = events.get(SUSPENSION_RECONCILED_PREFIX + name.split(':', 1)[1])
            if event is None:
                pending.append(name)
            else:
                self._validated_suspension_reconciliation(c, row, event)
        return sorted(pending)

    def unreconciled_suspensions(self):
        with self._transaction() as c:
            return self._unreconciled_suspensions(c)

    def reconcile_suspension(self, request_id, *, approval_path: Path):
        """Lift one response-identity suspension once a recorded revision accepts that identity.

        The ``suspended:`` event and the invalid record stay; nothing is re-evaluated.
        """
        approval, approval_ref = _read_embedded_json(approval_path, 'suspension reconciliation')
        with self._transaction() as c:
            events = self._events(c)
            suspended = events.get('suspended:' + request_id)
            if (suspended is None
                    or json.loads(suspended['detail_json']) != {'reason': IDENTITY_SUSPENSION_REASON}):
                raise HarnessError('only a response-identity suspension can be reconciled')
            name = SUSPENSION_RECONCILED_PREFIX + request_id
            if name in events:
                detail = self._validated_suspension_reconciliation(c, suspended, events[name])
                if detail['approval']['sha256'] != approval_ref['sha256']:
                    raise HarnessError('suspension already reconciled with another approval')
                return {'status': 'ALREADY_RECONCILED', 'request_id': request_id}
            chain = self._config_chain(c)
            if not chain:
                raise HarnessError('suspension reconciliation requires a recorded config revision')
            rows = self._rows(c)
            if any(r['status'] == 'INTENT' for r in rows):
                raise HarnessError('suspension reconciliation requires no unresolved intent')
            created = datetime.fromisoformat(suspended['created_utc'])
            if any(datetime.fromisoformat(r['intent_utc']) > created for r in rows):
                raise HarnessError('a request was created after the suspension; reconciliation refused')
            if (not isinstance(approval, dict) or set(approval) != SUSPENSION_APPROVAL_KEYS
                    or approval.get('decision') != 'accepted'
                    or not isinstance(approval.get('author'), str) or not approval['author'].strip()
                    or approval.get('request_id') != request_id
                    or approval.get('suspension_artifact_sha256') != suspended['artifact_sha256']
                    or approval.get('config_content_sha256') != digest(chain[-1])):
                raise HarnessError('suspension approval does not bind this suspension and the current revision')
            self._suspension_identity_check(c, request_id, approval.get('observed_identity'),
                                            approval['config_content_sha256'])
            detail = {k: approval[k] for k in ('request_id', 'suspension_artifact_sha256',
                                                'observed_identity', 'config_content_sha256')}
            detail['approval'] = approval_ref
            self._event(c, name, suspended['artifact_sha256'], detail)
            self._validated_suspension_reconciliation(c, suspended, self._events(c)[name])
            return {'status': 'RECONCILED', 'request_id': request_id}

    def _validated_requalification_parent(self, c, row):
        events = self._events(c)
        suspended = events.get('suspended:' + row['request_id'])
        event = events.get(SUSPENSION_RECONCILED_PREFIX + row['request_id'])
        if suspended is None or event is None:
            raise HarnessError("requalification requires a reconciled identity suspension")
        self._validated_suspension_reconciliation(c, suspended, event)

    def reserve_requalification_retry(self, **value):
        """One explicit resend of a reconciled identity suspension, outside 8r+t<=15."""
        with self._transaction() as c:
            self._insert_intent(c, quota_kind='requalification', **value)

    def _accounting_stops(self, c):
        return list(c.execute(
            "SELECT * FROM events WHERE event=? OR substr(event,1,?)=? ORDER BY rowid",
            (ACCOUNTING_STOP_EVENT, len(ACCOUNTING_STOP_EVENT) + 1, ACCOUNTING_STOP_EVENT + '#')))

    @staticmethod
    def _validate_accounting_stop_approval(approval, stop, stop_detail, fixed_commit):
        if (not isinstance(approval, dict) or set(approval) != ACCOUNTING_STOP_APPROVAL_KEYS
                or approval.get('decision') != 'accepted'
                or not isinstance(approval.get('author'), str) or not approval['author'].strip()
                or approval.get('stop_artifact_sha256') != stop['artifact_sha256']
                or approval.get('stop_request_id') != stop_detail.get('request_id')
                or approval.get('cause') != 'harness_defect'
                or not isinstance(fixed_commit, str) or not COMMIT.fullmatch(fixed_commit)
                or approval.get('fixed_commit') != fixed_commit
                or not isinstance(approval.get('ledger_sha256_before'), str)
                or not HASH.fullmatch(approval['ledger_sha256_before'])):
            raise HarnessError(
                'FATAL_ACCOUNTING_ERROR: accounting STOP approval does not match the durable STOP')

    def _validated_accounting_stop_reconciliation(self, c, stop, event):
        """Re-authenticate the embedded approval bytes on every use; never trust a marker."""
        try:
            stop_detail = json.loads(stop['detail_json'])
            detail = json.loads(event['detail_json'])
            stored = detail['approval']
            if (set(detail) != {'stop_event', 'stop_request_id', 'stop_created_utc', 'stop_reason',
                                'fixed_commit', 'revalidated_accounting_events', 'approval'}
                    or not isinstance(stored, dict)
                    or set(stored) != {'path', 'sha256', 'content', 'utf8'}
                    or not Path(stored['path']).is_absolute()):
                raise HarnessError('reconciliation fields are invalid')
            approval_bytes = stored['utf8'].encode('utf-8')
            approval = json.loads(approval_bytes)
            if (approval != stored['content']
                    or sha256_bytes(approval_bytes) != stored['sha256']
                    or event['artifact_sha256'] != stop['artifact_sha256']
                    or detail['stop_event'] != stop['event']
                    or detail['stop_request_id'] != stop_detail.get('request_id')
                    or detail['stop_created_utc'] != stop['created_utc']
                    or detail['stop_reason'] != stop_detail.get('reason')
                    or not isinstance(detail['revalidated_accounting_events'], list)
                    or 'tokenizer_accounting:' + stop_detail.get('request_id', '')
                    not in detail['revalidated_accounting_events']):
                raise HarnessError('reconciliation binding is invalid')
            self._validate_accounting_stop_approval(
                approval, stop, stop_detail, detail['fixed_commit'])
        except (AttributeError, KeyError, TypeError, ValueError, UnicodeError, HarnessError) as exc:
            raise HarnessError(
                'FATAL_ACCOUNTING_ERROR: accounting STOP reconciliation is corrupted') from exc
        return detail

    def _tokenizer_accounting_stop(self, c):
        """Return the first durable STOP that still blocks; only the original may be reconciled."""
        events = self._events(c)
        reconciliation = events.get(ACCOUNTING_STOP_RECONCILED_EVENT)
        stops = self._accounting_stops(c)
        if reconciliation is not None and (not stops or stops[0]['event'] != ACCOUNTING_STOP_EVENT):
            raise HarnessError(
                'FATAL_ACCOUNTING_ERROR: accounting STOP reconciliation has no original STOP')
        for stop in stops:
            if stop['event'] == ACCOUNTING_STOP_EVENT and reconciliation is not None:
                self._validated_accounting_stop_reconciliation(c, stop, reconciliation)
                continue
            return stop
        return None

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
            'artifact_version': TOKENIZER_ACCOUNTING_ARTIFACT_VERSION,
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

    def _requires_no_thinking_accounting(self, c, request):
        """Authenticate durable lineage and request identity before classifying accounting."""
        successor, _ = self._classified_successor_lineage(c)
        binding = self._binding(c, request['stage'])
        specs = [spec for spec in binding['requests']
                 if spec['logical_id'] == request['logical_id']]
        if (request['stage_run'] != digest(binding) or len(specs) != 1
                or request['identity_json'] != canonical_json(specs[0])
                or (request['model'], request['producer'])
                != (specs[0]['model'], specs[0]['producer'])):
            raise HarnessError(
                'FATAL_ACCOUNTING_ERROR: request differs from its durable producer binding')
        return (request['stage'] == TECHNICAL_STAGE
                or successor
                and request['stage'] in {'producer_conformity', 'producer_remediation'}
                and request['model'] == TOKENIZER_ACCOUNTING_MODEL)

    def _validate_accounting_contract(
            self, c, request, detail, raw_json, *, expected_messages=None):
        """Validate one complete accounting contract for acquisition and every reuse."""
        required = {
            'artifact_version', 'request_id', 'request_identity_sha256', 'messages',
            'messages_sha256', 'snapshot', 'raw_response_sha256',
            'local_prompt_tokens', 'server_prompt_tokens', 'outcome',
        }
        allowed = required | {'chat_template_kwargs'}
        if not isinstance(detail, dict) or set(detail) != required and set(detail) != allowed:
            raise HarnessError('FATAL_ACCOUNTING_ERROR: persisted accounting fields are invalid')
        try:
            identity = json.loads(request['identity_json'])
            raw = json.loads(raw_json)
        except (TypeError, ValueError, UnicodeError) as exc:
            raise HarnessError('FATAL_ACCOUNTING_ERROR: accounting contract JSON is invalid') from exc
        messages = detail.get('messages')
        if (not isinstance(messages, list) or len(messages) != 1
                or not isinstance(messages[0], dict)
                or set(messages[0]) != {'role', 'content'}
                or messages[0].get('role') != 'user'
                or not isinstance(messages[0].get('content'), str)
                or identity.get('prompt_sha256') != sha256_text(messages[0]['content'])
                or detail.get('messages_sha256') != sha256_text(canonical_json(messages))
                or expected_messages is not None and messages != expected_messages):
            raise HarnessError('FATAL_ACCOUNTING_ERROR: persisted accounting messages are invalid')
        usage = raw.get('usage') if isinstance(raw, dict) else None
        server_usage = usage.get('prompt_tokens') if isinstance(usage, dict) else None
        local_count = detail.get('local_prompt_tokens')
        server_count = detail.get('server_prompt_tokens')
        if (detail.get('artifact_version') != TOKENIZER_ACCOUNTING_ARTIFACT_VERSION
                or detail.get('request_id') != request['request_id']
                or detail.get('request_identity_sha256') != sha256_text(request['identity_json'])
                or detail.get('snapshot') != TOKENIZER_ACCOUNTING_SNAPSHOT
                or detail.get('raw_response_sha256') != sha256_text(raw_json)
                or type(local_count) is not int or local_count < 0
                or type(server_count) is not int or server_count < 0
                or type(server_usage) is not int or server_usage < 0
                or local_count != server_count or server_count != server_usage
                or detail.get('outcome') != 'PASS'):
            raise HarnessError('FATAL_ACCOUNTING_ERROR: persisted accounting contract is invalid')
        kwargs = detail.get('chat_template_kwargs')
        requires_no_thinking = self._requires_no_thinking_accounting(c, request)
        if requires_no_thinking and kwargs is None:
            raise HarnessError(
                'FATAL_ACCOUNTING_ERROR: 122B producer accounting lacks no-thinking control')
        if kwargs is not None:
            try:
                from .d9 import no_thinking_template_kwargs
                no_thinking_template_kwargs(kwargs)
            except HarnessError as exc:
                raise HarnessError(
                    'FATAL_ACCOUNTING_ERROR: persisted chat-template kwargs are invalid') from exc
        return detail

    def _persist_accounting_stop(self, c, request_id, reason, artifact_sha256):
        if self._tokenizer_accounting_stop(c) is None:
            count = len(self._accounting_stops(c))
            name = ACCOUNTING_STOP_EVENT if count == 0 else f'{ACCOUNTING_STOP_EVENT}#{count + 1}'
            self._event(c, name, artifact_sha256,
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
        self._validate_accounting_contract(
            c, request, detail, response['raw_json'], expected_messages=messages)
        counts = guard.validate_producer_response(messages, raw)
        expected = self._accounting_commitment(
            request, messages, guard.snapshot, response['raw_json'],
            counts['local_prompt_tokens'], counts['server_prompt_tokens'],
            guard.template_kwargs)
        self._validate_accounting_contract(
            c, request, expected, response['raw_json'], expected_messages=messages)
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
                    self._validate_accounting_contract(
                        c, request, result, response['raw_json'], expected_messages=messages)
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

    def validate_tokenizer_accounting_evidence(
            self, guard, *, expected_stage=None, expected_messages=None):
        """Recompute evidence; caller messages apply only to their named stage."""
        if (expected_stage is None) != (expected_messages is None):
            raise HarnessError(
                'FATAL_ACCOUNTING_ERROR: expected messages require an explicit stage')
        if expected_stage is not None and (expected_stage not in self.profile.stages
                or not isinstance(expected_messages, dict)
                or not all(isinstance(key, str) and key for key in expected_messages)):
            raise HarnessError(
                'FATAL_ACCOUNTING_ERROR: expected accounting stage/messages are invalid')
        failure = None
        with self._transaction() as c:
            self._require_no_tokenizer_accounting_stop(c)
            failed = self._revalidate_accounting_events(
                c, guard, expected_stage=expected_stage,
                expected_messages=expected_messages)[1]
            if failed is not None:
                request_id, failure, artifact = failed
                self._persist_accounting_stop(c, request_id, failure, artifact)
        if failure is not None:
            raise HarnessError(failure)

    def _revalidate_accounting_events(self, c, guard, *, expected_stage=None,
                                      expected_messages=None):
        """Return validated event names and the first failure, without writing."""
        validated = []
        for name, row in self._events(c).items():
            if not name.startswith('tokenizer_accounting:'):
                continue
            request_id = name.split(':', 1)[1]
            request = c.execute('SELECT * FROM requests WHERE request_id=?', (request_id,)).fetchone()
            try:
                detail = json.loads(row['detail_json'])
                messages = detail.get('messages')
                if request is not None and request['stage'] == expected_stage:
                    if request['logical_id'] not in expected_messages:
                        raise HarnessError(
                            'FATAL_ACCOUNTING_ERROR: expected messages omit a stage request')
                    messages = expected_messages[request['logical_id']]
                # The rendering rule is an attribute of this authenticated durable
                # request, not of the caller that happens to revalidate the ledger.
                # Classify only after lineage, binding and request identity agree.
                requires_no_thinking = self._requires_no_thinking_accounting(c, request)
                event_guard = TokenizerAccountingGuard(
                    guard.tokenizer, snapshot=guard.snapshot,
                    template_kwargs=({'enable_thinking': False}
                                     if requires_no_thinking else None))
                self._validate_accounting_event(
                    c, request, messages=messages, guard=event_guard)
                validated.append(name)
            except Exception as exc:
                reason = str(exc) if str(exc).startswith('FATAL_ACCOUNTING_ERROR') else (
                    f'FATAL_ACCOUNTING_ERROR: accounting evidence revalidation failed: {type(exc).__name__}: {exc}')
                artifact = row['artifact_sha256'] if HASH.fullmatch(row['artifact_sha256'] or '') else '0' * 64
                return validated, (request_id, reason, artifact)
        return validated, None

    def reconcile_accounting_stop(self, *, approval_path: Path, fixed_commit: str, guard):
        """Reconcile the original spurious accounting STOP with a durable author approval.

        The STOP is never deleted.  Every persisted accounting event must pass the
        corrected validator with its own durable messages, and no request may have
        been created after the STOP.  A later STOP is never covered.
        """
        approval_path = Path(approval_path).resolve()
        try:
            approval_bytes = approval_path.read_bytes()
            approval_utf8 = approval_bytes.decode('utf-8')
            approval = json.loads(approval_utf8)
        except (OSError, ValueError, UnicodeError) as exc:
            raise HarnessError('accounting STOP approval is unavailable or invalid') from exc
        approval_sha256 = sha256_bytes(approval_bytes)
        with self._transaction() as c:
            events = self._events(c)
            stop = events.get(ACCOUNTING_STOP_EVENT)
            if stop is None:
                raise HarnessError('no tokenizer accounting STOP to reconcile')
            existing = events.get(ACCOUNTING_STOP_RECONCILED_EVENT)
            if existing is not None:
                detail = self._validated_accounting_stop_reconciliation(c, stop, existing)
                if (detail['approval']['sha256'] != approval_sha256
                        or detail['fixed_commit'] != fixed_commit):
                    raise HarnessError('accounting STOP is already reconciled with another approval')
                blocking = self._tokenizer_accounting_stop(c)
                if blocking is not None:
                    raise HarnessError('FATAL_ACCOUNTING_ERROR: durable STOP blocks probes, gates, '
                                       'retries and new requests: a later STOP is not reconcilable')
                return {'status': 'ALREADY_RECONCILED', 'stop_request_id': detail['stop_request_id'],
                        'approval_sha256': approval_sha256}
            if [row['event'] for row in self._accounting_stops(c)] != [ACCOUNTING_STOP_EVENT]:
                raise HarnessError('accounting STOP inventory is inconsistent')
            try:
                stop_detail = json.loads(stop['detail_json'])
            except (TypeError, ValueError) as exc:
                raise HarnessError('accounting STOP detail is corrupted') from exc
            if (not isinstance(stop_detail, dict)
                    or set(stop_detail) != {'reason', 'request_id', 'accounting_event'}
                    or stop_detail['accounting_event'] != 'tokenizer_accounting:' + str(stop_detail['request_id'])):
                raise HarnessError('accounting STOP detail is corrupted')
            self._validate_accounting_stop_approval(approval, stop, stop_detail, fixed_commit)
            wal = Path(str(self.path) + '-wal')
            if wal.exists() and wal.stat().st_size:
                raise HarnessError('accounting STOP reconciliation requires a checkpointed ledger')
            if sha256_file(self.path) != approval['ledger_sha256_before']:
                raise HarnessError('accounting STOP approval is bound to another ledger state')
            stop_time = datetime.fromisoformat(stop['created_utc'])
            for row in self._rows(c):
                if row['status'] == 'INTENT':
                    raise HarnessError('accounting STOP reconciliation refused: unresolved INTENT exists')
                if datetime.fromisoformat(row['intent_utc']) > stop_time:
                    raise HarnessError('accounting STOP reconciliation refused: request created after the STOP')
            validated, failed = self._revalidate_accounting_events(c, guard)
            if failed is not None:
                raise HarnessError('accounting STOP reconciliation refused: ' + failed[1])
            if stop_detail['accounting_event'] not in validated:
                raise HarnessError('accounting STOP reconciliation refused: STOP request lacks valid accounting')
            detail = {
                'stop_event': ACCOUNTING_STOP_EVENT,
                'stop_request_id': stop_detail['request_id'],
                'stop_created_utc': stop['created_utc'],
                'stop_reason': stop_detail['reason'],
                'fixed_commit': fixed_commit,
                'revalidated_accounting_events': sorted(validated),
                'approval': {'path': str(approval_path), 'sha256': approval_sha256,
                             'content': approval, 'utf8': approval_utf8},
            }
            self._event(c, ACCOUNTING_STOP_RECONCILED_EVENT, stop['artifact_sha256'], detail)
            self._validated_accounting_stop_reconciliation(
                c, stop, self._events(c)[ACCOUNTING_STOP_RECONCILED_EVENT])
            if self._tokenizer_accounting_stop(c) is not None:
                raise HarnessError('accounting STOP reconciliation did not clear the original STOP')
            return {'status': 'RECONCILED', 'stop_request_id': stop_detail['request_id'],
                    'revalidated_accounting_events': len(validated),
                    'approval_sha256': approval_sha256}

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
        self._validate_accounting_contract(
            c, request, accounting_detail, response['raw_json'])
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

    def _canary_days(self, c):
        events = self._events(c)
        passed = [e[len(CANARY_PASS_PREFIX):] for e in events if e.startswith(CANARY_PASS_PREFIX)]
        marked = [e[len(CANARY_MARKED_PREFIX):] for e in events if e.startswith(CANARY_MARKED_PREFIX)]
        stops = [e for e in events if e.startswith(CANARY_STOP_PREFIX)]
        return sorted(passed), sorted(marked), sorted(stops)

    def _canary_day_slot(self, c, day):
        """Validate that exactly one complete, unrecorded canary day is being closed."""
        if self.profile.name != 'final_batch':
            raise HarnessError("canary verdicts belong to the final-batch profile")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(day)):
            raise HarnessError("canary day must be an ISO civil date")
        passed, marked, stops = self._canary_days(c)
        if stops:
            raise HarnessError("a canary stop is already in force")
        if day in passed or day in marked:
            raise HarnessError("canary day already recorded")
        index = len(passed) + len(marked) + 1
        if index > CANARY_MAX_DAYS:
            raise HarnessError(f"canary allowance of {CANARY_MAX_DAYS} days is exhausted")
        prefix = f"canary:day{index}:"
        rows = [r for r in self._rows(c)
                if r['stage'] == FINAL_CANARY_STAGE and r['logical_id'].startswith(prefix)]
        return index, rows, passed, marked

    def record_canary_day(self, day, *, verdict, comparison, expectations_sha256, identity=None,
                          observed_day=None):
        """Create-once verdict of one canary day (§6). Ten complete calls, no rewriting.

        ``observed_day`` is the Europe/Rome day read from the clock when the day was run.
        A canary opens the day it belongs to, so the two must coincide: a declared day that
        does not match the observed one is refused here as well as in the runner, and both
        values stay in the event (review rilievo B1).
        """
        if verdict not in {'PASS', 'MARKED'}:
            raise HarnessError("canary verdict must be PASS or MARKED")
        if not isinstance(comparison, dict) or 'marked_day' not in comparison:
            raise HarnessError("canary verdict requires its comparison artifact")
        if bool(comparison['marked_day']) != (verdict == 'MARKED'):
            raise HarnessError("canary verdict contradicts its comparison")
        self._require_hash(expectations_sha256, 'canary expectations')
        if observed_day is not None and observed_day != day:
            raise HarnessError(
                f"canary day {day} was declared but the observed Europe/Rome day is "
                f"{observed_day}; a canary never crosses midnight")
        with self._transaction() as c:
            index, rows, passed, marked = self._canary_day_slot(c, day)
            if len(rows) != CANARY_DAILY_CALLS or any(r['status'] != 'COMPLETED' for r in rows):
                raise HarnessError("a canary day closes only on ten complete calls")
            detail = dict(day=day, day_index=index, verdict=verdict,
                          declared_day=day, observed_day=observed_day or day,
                          expectations_sha256=expectations_sha256, comparison=comparison,
                          request_ids=sorted(r['request_id'] for r in rows))
            if identity is not None:
                # §6 identity control: returned_model AND system_fingerprint observed on
                # every canary call of the day, persisted with the verdict.
                if not isinstance(identity, dict) or not identity:
                    raise HarnessError("canary identity evidence must be a non-empty mapping")
                detail['identity'] = identity
            prefix = CANARY_PASS_PREFIX if verdict == 'PASS' else CANARY_MARKED_PREFIX
            self._event(c, prefix + day, digest(detail), detail)
            if verdict == 'MARKED' and len(marked) + 1 >= 2:
                stop = dict(day=day, marked_days=sorted(marked + [day]),
                            rule="second marked day: author decision before any resumption")
                self._event(c, CANARY_STOP_PREFIX + 'second_marked_day:' + day, digest(stop), stop)
            return detail

    def record_canary_stop(self, day, *, reason, detail, observed_day=None):
        """Immediate canary stop (§6.3): identity change before any further call.

        A stop is always recordable, so a mismatch between declared and observed day is
        preserved here rather than refused: the evidence must survive.
        """
        if self.profile.name != 'final_batch':
            raise HarnessError("canary stops belong to the final-batch profile")
        if not isinstance(reason, str) or not reason.strip():
            raise HarnessError("a canary stop requires a written reason")
        value = dict(day=day, declared_day=day, observed_day=observed_day or day,
                     reason=reason, detail=detail)
        with self._transaction() as c:
            self._event(c, CANARY_STOP_PREFIX + 'identity:' + str(day), digest(value), value)
            return value

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
        if stage not in self.profile.stages:
            raise HarnessError("invalid stage")
        specs = binding.get('requests', [])
        required = {'logical_id', 'model', 'producer', 'prompt_sha256', 'case_sha256', 'contract_sha256', 'condition', 'group', 'repetition'}
        if not isinstance(specs, list) or len({s.get('logical_id') for s in specs}) != len(specs):
            raise HarnessError("request plan requires unique logical identities")
        expected = self.profile.base_limits[stage]
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
            if 'execution_config' in binding:
                self._require_accepted_config(
                    c, binding['execution_config'], binding['execution_config'])
            from .d9 import validate_binding
            validate_binding(binding, stage, self, c)
            old = c.execute("SELECT binding_sha256 FROM stages WHERE stage=?", (stage,)).fetchone()
            if old:
                if old[0] != digest(binding):
                    self._rebind_stage(c, stage, self._binding(c, stage), binding)
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
                nxt = children[row['request_id']]
                if row['request_id'] in visited or not (
                        row['status'] == 'ZERO_TOKEN_PROVEN'
                        or row['status'] == 'COMPLETED' and nxt['quota_kind'] == 'requalification'):
                    raise HarnessError("invalid retry chain")
                visited.add(row['request_id'])
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

    def _consecutive_technical_failures(self, c):
        """Consecutive failed technical attempts per service, retries included (D3).

        Derived from the request table in insertion order, so the counter is persistent
        by construction: restarting the runner, renaming a directory or opening the
        ledger again cannot reset it. A request that reaches ``COMPLETED`` -- a response
        was received, valid or not -- resets its service; ``FAILED`` and the reconciled
        ``ZERO_TOKEN_PROVEN`` both record that the attempt failed technically.
        """
        counters: dict = {}
        for row in self._rows(c):
            if row['status'] == 'INTENT':
                continue
            service = row['model']
            if row['status'] == 'COMPLETED':
                counters[service] = 0
            else:
                counters[service] = counters.get(service, 0) + 1
        return counters

    def consecutive_technical_failures(self):
        with closing(self._connect()) as c:
            return self._consecutive_technical_failures(c)

    def _technical_failure_stop(self, c):
        limit = self.profile.consecutive_failure_stop
        if not limit:
            return {}
        return {service: count for service, count
                in self._consecutive_technical_failures(c).items() if count >= limit}

    def technical_failure_stop(self):
        with closing(self._connect()) as c:
            return self._technical_failure_stop(c)

    def _prerequisites(self, c, stage):
        """Validate the dependency chain for both new work and reuse of closed results.

        These checks never require the requested stage to be open. Keeping them separate
        from mutation ordering permits valid replay after downstream stages have run,
        without grandfathering outcomes created by an earlier, unsafe implementation.
        """
        events = self._events(c)
        if self._unreconciled_suspensions(c):
            raise HarnessError("pilot suspended; requires a new reviewed disposition")
        successor, _ = self._classified_successor_lineage(c)
        if successor:
            if stage == TECHNICAL_STAGE:
                pass
            elif stage == 'producer_conformity':
                try:
                    self._successful(c, TECHNICAL_STAGE)
                except HarnessError as exc:
                    raise HarnessError(
                        "successor producer conformity requires successful technical qualification"
                    ) from exc
        if self.profile.name == 'final_batch':
            if any(event.startswith(CANARY_STOP_PREFIX) for event in events):
                raise HarnessError("canary STOP blocks every further call of the final batch")
            stopped = self._technical_failure_stop(c)
            if stopped:
                raise HarnessError(
                    f"STOP: {self.profile.consecutive_failure_stop} consecutive technical "
                    f"failures on {sorted(stopped)}; the campaign is suspended with results "
                    "and pending requests preserved")
            if stage in FINAL_PASS_STAGES:
                if not any(event.startswith(CANARY_PASS_PREFIX) for event in events):
                    raise HarnessError("the scientific batch requires a passed canary day first")
                index = FINAL_PASS_STAGES.index(stage)
                if index and 'outcome:' + FINAL_PASS_STAGES[index - 1] not in events:
                    raise HarnessError(
                        f"pass {index + 1} cannot start before {FINAL_PASS_STAGES[index - 1]} is closed")
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
        successor, predecessors = self._quota_context(c)
        profile = self.profile
        if quota_kind not in profile.quota_kinds:
            raise HarnessError(f"quota kind {quota_kind} is not admitted by profile {profile.name}")
        if len(rows) + len(predecessors) >= profile.hard_stop:
            raise HarnessError(f"cumulative hard stop {profile.hard_stop} reached")
        if profile.name == 'pilot':
            successor_extra = int(successor)
            requalification_extra = (sum(r['quota_kind'] == 'requalification' for r in rows)
                                     + int(quota_kind == 'requalification'))
            max_calls = (160 if stage == 'alternate_conformity' or any(
                r['stage'] == 'alternate_conformity' for r in rows) else 152) + successor_extra + requalification_extra
            if len(rows) >= max_calls:
                raise HarnessError(f"planned request maximum {max_calls + len(predecessors)} reached")
        else:
            # Protocol §7.2 with author decision D3: exceeding a per-stage quota, the
            # separate retry ceiling or the total is a batch STOP. Scientific slots are
            # counted on the base requests alone, so a retry never consumes one.
            if len(rows) >= profile.planned_maximum:
                raise HarnessError(f"planned request maximum {profile.planned_maximum} reached")
            limit = profile.base_limits.get(stage)
            if limit is None:
                raise HarnessError(f"stage {stage} has no quota in profile {profile.name}")
            if limit == 0:
                raise HarnessError(
                    f"stage {stage} has quota 0 in profile {profile.name}; a call on it "
                    "requires a declared protocol revision")
            if quota_kind == 'transport':
                used = sum(r['quota_kind'] == 'transport' for r in rows) + 1
                if used > profile.retry_quota:
                    raise HarnessError(
                        f"cumulative retry quota {profile.retry_quota} is exhausted")
            elif sum(r['stage'] == stage and r['retry_of'] is None for r in rows) >= limit:
                raise HarnessError(f"stage quota {limit} for {stage} is exhausted")
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
        if quota_kind == 'requalification':
            original = next((r for r in rows if r['request_id'] == retry_of), None)
            if (not retry_of or original is None or original['status'] != 'COMPLETED'
                    or original['stage'] != stage or stage not in REQUALIFICATION_STAGES
                    or original['identity_json'] != identity):
                raise HarnessError("requalification retry requires the matching completed suspended request")
            self._validated_requalification_parent(c, original)
            if sum(r['quota_kind'] == 'requalification' for r in rows) >= REQUALIFICATION_LIMIT:
                raise HarnessError("requalification quota is exhausted")
            if any(r['retry_of'] == retry_of for r in rows):
                raise HarnessError("requalification original already has a retry")
        elif retry_of:
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
        if profile.name == 'pilot':
            # The pilot shared reserve (8r + t <= 15) is a pilot envelope: the final batch
            # has its own separate retry quota and never borrows from a remediation
            # reserve it does not own.
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

    def completion_instants(self, stage):
        """Read-only: the completion instants of one stage, oldest first.

        Used by the runner to prove that a lot which now runs past midnight really began
        on the civil day it declares (review rilievo B1).
        """
        if stage not in self.profile.stages:
            raise HarnessError("unknown stage for this quota profile")
        with closing(self._connect()) as c:
            return [row[0] for row in c.execute(
                "SELECT completed_utc FROM requests WHERE stage=? AND completed_utc IS NOT NULL"
                " ORDER BY completed_utc", (stage,))]

    def attempts(self, stage, logical_id):
        """Every attempt recorded for one logical request, in insertion order."""
        with closing(self._connect()) as c:
            return [dict(r) for r in self._rows(c)
                    if r['stage'] == stage and r['logical_id'] == logical_id]

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
        runs = {stage: set(self._stage_runs(c, stage)) | {digest(binding)}
                for stage in {r['stage'] for r in rows}}
        if sum(r['quota_kind'] == 'requalification' for r in self._rows(c)) > REQUALIFICATION_LIMIT:
            raise HarnessError('requalification quota exceeded')
        for row in rows:
            spec = specs.get(row['logical_id'])
            if (spec is None or row['identity_json'] != canonical_json(spec)
                    or row['stage_run'] not in runs[row['stage']]
                    or (row['model'], row['producer']) != (spec['model'], spec['producer'])):
                raise HarnessError('persisted request differs from immutable plan')
            requalification = bool(row['retry_of']) and row['quota_kind'] == 'requalification'
            expected_quota = ('requalification' if requalification else
                              'transport' if row['retry_of'] else
                              'remediation' if row['stage'] == 'producer_remediation' else
                              'technical' if row['stage'] == TECHNICAL_STAGE else 'base')
            if row['quota_kind'] != expected_quota:
                raise HarnessError('persisted attempt quota differs from its role')
            if requalification:
                parent = by_id.get(row['retry_of'])
                if (parent is None or parent['status'] != 'COMPLETED'
                        or row['stage'] not in REQUALIFICATION_STAGES
                        or parent['identity_json'] != row['identity_json']):
                    raise HarnessError('orphan or inconsistent requalification attempt')
                self._validated_requalification_parent(c, parent)
            elif row['retry_of']:
                parent = by_id.get(row['retry_of'])
                if (parent is None or parent['status'] != 'ZERO_TOKEN_PROVEN'
                        or parent['identity_json'] != row['identity_json']
                        or row['quota_kind'] != 'transport'):
                    raise HarnessError('orphan or inconsistent retry attempt')
            if row['status'] == 'ZERO_TOKEN_PROVEN':
                self._validated_reconciliation(c, row)
            if row['status'] == 'COMPLETED' and row['model'] == TOKENIZER_ACCOUNTING_MODEL:
                if self._evaluated_record(c, row) is None:
                    raise HarnessError(
                        'FATAL_ACCOUNTING_ERROR: completed 122B request lacks a durable record')
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
        if stage not in self.profile.stages or outcome not in {'PASS','FAIL','BLOCKED'}:
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

    def _diagnosed_producer_failure(self, c, records_sha256):
        event = self._events(c).get('diagnosis:producer_conformity')
        if event is None:
            return None
        try:
            detail = json.loads(event['detail_json'])
            stored_approval = detail.get('approval')
            if (not isinstance(stored_approval, dict)
                    or not Path(stored_approval.get('path', '')).is_absolute()):
                raise HarnessError('producer failure diagnosis lacks its approval reference')
            if set(stored_approval) == {'path', 'sha256'}:
                # Compatibility for the one pre-correction event: it remains fail-closed
                # and still requires its externally authenticated approval bytes.
                approval_bytes = Path(stored_approval['path']).read_bytes()
                approval = json.loads(approval_bytes)
            elif set(stored_approval) == {'path', 'sha256', 'content', 'utf8'}:
                approval_bytes = stored_approval['utf8'].encode('utf-8')
                approval = json.loads(approval_bytes)
                if approval != stored_approval['content']:
                    raise HarnessError('producer failure diagnosis approval copy is corrupted')
            else:
                raise HarnessError('producer failure diagnosis lacks its approval content')
        except (OSError, AttributeError, TypeError, ValueError, UnicodeError) as exc:
            raise HarnessError('producer failure diagnosis approval is unavailable or invalid') from exc
        diagnosis = detail.get('diagnosis')
        expected = {
            'diagnosis': diagnosis,
            'records_sha256': records_sha256,
            'approval': stored_approval,
        }
        if (diagnosis not in DIAGNOSES or detail != expected
                or event['artifact_sha256'] != stored_approval['sha256']
                or sha256_bytes(approval_bytes) != stored_approval['sha256']
                or not isinstance(approval, dict)
                or set(approval) != {'decision', 'author', 'diagnosis', 'records_sha256'}
                or approval.get('decision') != 'accepted'
                or not isinstance(approval.get('author'), str)
                or not approval['author'].strip()
                or approval.get('diagnosis') != diagnosis
                or approval.get('records_sha256') != records_sha256):
            raise HarnessError('producer failure diagnosis event is corrupted')
        return diagnosis

    def diagnose_producer_failure(self, *, diagnosis, approval_path,
                                  approval_sha256=None):
        """Attach one approved diagnosis to a closed undiagnosed producer FAIL."""
        if diagnosis not in DIAGNOSES:
            raise HarnessError('inadmissible producer remediation diagnosis')
        approval_path = Path(approval_path).resolve()
        try:
            approval_bytes = approval_path.read_bytes()
            approval_utf8 = approval_bytes.decode('utf-8')
            approval = json.loads(approval_utf8)
        except (OSError, TypeError, ValueError, UnicodeError) as exc:
            raise HarnessError('producer failure diagnosis approval is unavailable or invalid') from exc
        actual_sha256 = sha256_bytes(approval_bytes)
        if approval_sha256 is not None:
            self._require_hash(approval_sha256, 'producer failure diagnosis approval')
            if actual_sha256 != approval_sha256:
                raise HarnessError('producer failure diagnosis approval hash mismatch')
        with self._transaction() as c:
            events = self._events(c)
            rows = self._rows(c)
            if ('remediation_authorized' in events or 'remediation_waived' in events
                    or any(row['stage'] in {'budget_probe', 'stability_gate'} for row in rows)):
                raise HarnessError('producer failure diagnosis is forbidden after remediation disposition or probe/gate')
            failed = events.get('outcome:producer_conformity')
            detail = json.loads(failed['detail_json']) if failed else {}
            if detail.get('outcome') != 'FAIL' or detail.get('diagnosis') is not None:
                raise HarnessError('producer failure diagnosis requires an undiagnosed closed FAIL')
            self._closed_outcome(c, 'producer_conformity')
            producer_rows = [row for row in rows if row['stage'] == 'producer_conformity']
            failed_records = [
                record for row in self._chain_leaves(producer_rows)
                if (record := self._evaluated_record(c, row)) is not None
            ]
            if not any(record.get('schema_valid_first_attempt') is False
                       and record.get('validation_class') == diagnosis
                       for record in failed_records):
                raise HarnessError(
                    'producer failure diagnosis must match a recorded producer validation defect')
            records_sha256 = detail.get('records_sha256')
            if (not isinstance(approval, dict)
                    or set(approval) != {'decision', 'author', 'diagnosis', 'records_sha256'}
                    or approval.get('decision') != 'accepted'
                    or not isinstance(approval.get('author'), str)
                    or not approval['author'].strip()
                    or approval.get('diagnosis') != diagnosis
                    or approval.get('records_sha256') != records_sha256):
                raise HarnessError(
                    'producer failure diagnosis approval must bind author, diagnosis and records')
            event_detail = {
                'diagnosis': diagnosis,
                'records_sha256': records_sha256,
                'approval': {
                    'path': str(approval_path),
                    'sha256': actual_sha256,
                    'content': approval,
                    'utf8': approval_utf8,
                },
            }
            existing = events.get('diagnosis:producer_conformity')
            if existing is not None:
                stored = self._diagnosed_producer_failure(c, records_sha256)
                if existing['artifact_sha256'] != actual_sha256 or stored != diagnosis:
                    raise HarnessError('another producer failure diagnosis already exists')
                return json.loads(existing['detail_json'])
            self._event(c, 'diagnosis:producer_conformity', actual_sha256, event_detail)
            return event_detail

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
            diagnosis = detail.get('diagnosis')
            if diagnosis is None:
                diagnosis = self._diagnosed_producer_failure(
                    c, detail.get('records_sha256'))
            rows = [r for r in self._rows(c) if r['stage'] == 'producer_conformity']
            failed_records = [self.response(r['request_id'])['record'] for r in self._chain_leaves(rows) if r['status'] == 'COMPLETED']
            if not any(r.get('schema_valid_first_attempt') is False and r.get('validation_class') == diagnosis for r in failed_records):
                raise HarnessError('remediation diagnosis must match a recorded producer validation defect')
            if detail.get('outcome') != 'FAIL' or diagnosis not in DIAGNOSES or any(r['status'] != 'COMPLETED' for r in self._chain_leaves(rows)):
                raise HarnessError("remediation requires diagnosed prompt defect; unresolved timeout is not admissible")
            binding = self._binding(c, 'producer_conformity')
            expected_diff = ''.join(difflib.unified_diff(binding['template_text'].splitlines(True), template.splitlines(True), fromfile='before', tofile='after'))
            if not expected_diff or diff != expected_diff or approval.get('decision') != 'accepted' or not approval.get('author') or approval.get('diff_sha256') != sha256_text(diff) or approval.get('template_sha256') != sha256_text(template) or approval.get('initial_binding_sha256') != digest(binding) or approval.get('diagnosis') != diagnosis:
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
            successor, predecessors = self._quota_context(c)
            consecutive = self._consecutive_technical_failures(c)
            raw_count = c.execute("SELECT count(*) FROM responses").fetchone()[0]
        by_stage = {s: sum(r['stage'] == s for r in rows) for s in sorted(self.profile.stages)}
        remediation = sum(r['quota_kind'] == 'remediation' for r in rows)
        transport = sum(r['quota_kind'] == 'transport' for r in rows)
        requalification = sum(r['quota_kind'] == 'requalification' for r in rows)
        planned_without_alternate = 152 + int(successor) + len(predecessors) + requalification
        planned_with_alternate = 160 + int(successor) + len(predecessors) + requalification
        planned_maximum = self.profile.planned_maximum
        return dict(pilot_id=self.pilot_id, ledger_path=str(self.identity_path),
                    requests_cumulative=len(rows)+len(predecessors), native_requests=len(rows),
                    historical_requests=len(predecessors),
                    predecessor_lineage_requests=len(predecessors) if successor else 0,
                    requests_by_stage=by_stage,
                    unresolved_intents=sum(r['status'] == 'INTENT' for r in rows),
                    remediation_calls=remediation, transport_calls=transport,
                    requalification_calls=requalification,
                    reserve_equation_value=8*int(remediation>0)+transport, reserve_limit=15,
                    planned_maximum=(planned_maximum if self.profile.name != 'pilot' else
                                     (planned_with_alternate if by_stage['alternate_conformity']
                                      else planned_without_alternate)),
                    planned_maximum_without_alternate=planned_without_alternate,
                    planned_maximum_with_alternate=planned_with_alternate,
                    profile=self.profile.name,
                    stage_quota=dict(sorted(self.profile.base_limits.items())),
                    retry_quota=self.profile.retry_quota,
                    retry_quota_used=transport if self.profile.retry_quota else 0,
                    consecutive_technical_failures=dict(sorted(consecutive.items())),
                    consecutive_failure_stop=self.profile.consecutive_failure_stop,
                    hard_stop=self.profile.hard_stop,
                    hard_stop_margin_at_planned_maximum=self.profile.hard_stop - (
                        planned_maximum if self.profile.name != 'pilot' else planned_with_alternate),
                    durable_responses=raw_count, events=sorted(events))
