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

from .common import HarnessError, canonical_json, sha256_text, sha256_file, sha256_bytes, load_json

HASH = re.compile(r"^[0-9a-f]{64}$")
STAGES = {"producer_conformity", "producer_remediation", "alternate_conformity", "budget_probe", "stability_gate"}
BASE_LIMITS = dict(producer_conformity=8, producer_remediation=8, alternate_conformity=8, budget_probe=9, stability_gate=120)
DIAGNOSES = {"structure", "identifiers", "cap", "leakage"}


def digest(value):
    return sha256_text(canonical_json(value))


def _utc_now():
    return datetime.now(timezone.utc).isoformat()


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
            if version not in {0, 2}:
                raise HarnessError("unsupported ledger version")
            if version == 0 and c.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchone():
                raise HarnessError("legacy ledger requires explicit reviewed migration; preserved without changes")
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
        rows = self._rows(c)
        for stage in sorted({row['stage'] for row in rows}):
            if stage not in STAGES:
                raise HarnessError('persisted attempt has an unknown stage')
            self._validate_attempts(c, self._binding(c, stage),
                                    [row for row in rows if row['stage'] == stage])
        return rows

    def _events(self, c):
        return {r['event']: r for r in c.execute("SELECT * FROM events")}

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
        return value

    def binding(self, stage):
        with closing(self._connect()) as c:
            return self._binding(c, stage)

    def bind_stage(self, stage, binding):
        """Freeze exact requests, provider, prompts, inputs and template before reservation."""
        if stage not in STAGES:
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
        if len(rows) >= 200:
            raise HarnessError("pilot cumulative hard stop 200 reached")
        max_calls = 160 if stage == 'alternate_conformity' or any(r['stage'] == 'alternate_conformity' for r in rows) else 152
        if len(rows) >= max_calls:
            raise HarnessError(f"planned request maximum {max_calls} reached")
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

    def reserve_transport_retry(self, **value):
        if value['stage'] == 'budget_probe':
            raise HarnessError("probe retries require an atomic complete triplet")
        with self._transaction() as c:
            self._insert_intent(c, quota_kind='transport', **value)

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
                text = canonical_json(record)
                c.execute("UPDATE responses SET record_json=?,record_sha256=? WHERE request_id=?", (text, sha256_text(text), request_id))
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
            expected_quota = 'transport' if row['retry_of'] else 'remediation' if row['stage'] == 'producer_remediation' else 'base'
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
        if stage not in STAGES or outcome not in {'PASS','FAIL','BLOCKED'}:
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
            raw_count = c.execute("SELECT count(*) FROM responses").fetchone()[0]
        by_stage = {s: sum(r['stage'] == s for r in rows) for s in sorted(STAGES)}
        remediation = sum(r['quota_kind'] == 'remediation' for r in rows)
        transport = sum(r['quota_kind'] == 'transport' for r in rows)
        return dict(pilot_id=self.pilot_id, ledger_path=str(self.path), requests_cumulative=len(rows), requests_by_stage=by_stage, unresolved_intents=sum(r['status'] == 'INTENT' for r in rows), remediation_calls=remediation, transport_calls=transport, reserve_equation_value=8*int(remediation>0)+transport, reserve_limit=15, planned_maximum=160 if by_stage['alternate_conformity'] else 152, hard_stop=200, durable_responses=raw_count, events=sorted(events))
