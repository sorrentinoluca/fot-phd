"""Shared offline-testable request lifecycle. No implicit retries or lost raw outputs."""
from pathlib import Path
import json
import os
import time
import tempfile

from .common import HarnessError, canonical_json
from .ledger import digest, TOKENIZER_ACCOUNTING_MODEL, TokenizerAccountingGuard
from .guards import response_identity_valid


def durable_write(path, text):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, prefix=path.name+'.', delete=False) as f:
        temporary = Path(f.name)
        f.write(text)
        f.flush()
        os.fsync(f.fileno())
    os.replace(temporary, path)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def export_journal(ledger, stage, path):
    # SQLite is authoritative, including responses that have not yet been evaluated.
    binding = ledger.binding(stage)
    rows = []
    for spec in binding['requests']:
        leaf = ledger.leaf(stage, spec['logical_id'])
        if leaf:
            response = ledger.response(leaf['request_id'])
            rows.append(dict(request=leaf, response=response, transport_invalidity=ledger.gate_transport_record(leaf['request_id'])))
    durable_write(path, ''.join(canonical_json(r) + '\n' for r in rows))


def execute_request(*, ledger, stage, spec, transport, evaluate, expected_identity, journal_path,
                    messages=None, accounting_guard=None, resume=False, retry_requests=(), pre_reserved=()):
    binding = ledger.binding(stage)
    stage_run = digest(binding)
    accounting_required = spec.get('model') == TOKENIZER_ACCOUNTING_MODEL
    if accounting_required:
        if not isinstance(accounting_guard, TokenizerAccountingGuard):
            raise HarnessError('FATAL_ACCOUNTING_ERROR: qwen3.5-122b requires TokenizerAccountingGuard')
        from .common import sha256_text
        if (not isinstance(messages, list) or len(messages) != 1
                or not isinstance(messages[0], dict) or set(messages[0]) != {'role', 'content'}
                or messages[0].get('role') != 'user' or not isinstance(messages[0].get('content'), str)
                or spec.get('prompt_sha256') != sha256_text(messages[0]['content'])):
            raise HarnessError('FATAL_ACCOUNTING_ERROR: qwen3.5-122b messages differ from frozen prompt')
    leaf = ledger.leaf(stage, spec['logical_id'])
    if leaf and not resume:
        raise HarnessError('existing stage requires explicit --resume; no automatic resend')
    if leaf and stage == 'stability_gate':
        invalidity = ledger.gate_transport_record(leaf['request_id'])
        if invalidity is not None:
            export_journal(ledger, stage, journal_path)
            return invalidity
    if leaf and leaf['status'] == 'COMPLETED' and leaf['request_id'] in retry_requests:
        # 03.13-REV27B: one explicit resend of a reconciled identity suspension.
        request_id = digest([ledger.pilot_id, stage, spec['logical_id'], leaf['request_id']])
        ledger.reserve_requalification_retry(request_id=request_id, logical_id=spec['logical_id'], model=spec['model'], producer=spec['producer'], stage=stage, stage_run=stage_run, retry_of=leaf['request_id'])
        leaf = ledger.request(request_id)
        fresh = True
    elif leaf and leaf['status'] == 'ZERO_TOKEN_PROVEN':
        if leaf['request_id'] not in retry_requests:
            raise HarnessError('proven zero-token request requires explicit retry selection')
        request_id = digest([ledger.pilot_id, stage, spec['logical_id'], leaf['request_id']])
        ledger.reserve_transport_retry(request_id=request_id, logical_id=spec['logical_id'], model=spec['model'], producer=spec['producer'], stage=stage, stage_run=stage_run, retry_of=leaf['request_id'])
        leaf = ledger.request(request_id)
        fresh = True
    else:
        fresh = leaf is None or leaf["request_id"] in pre_reserved
    if fresh and leaf is None:
        request_id = digest([ledger.pilot_id, stage, spec['logical_id']])
        reservation = dict(request_id=request_id, logical_id=spec['logical_id'], model=spec['model'], producer=spec['producer'], stage_run=stage_run)
        if stage == 'producer_remediation':
            ledger.reserve_remediation_request(**reservation)
        else:
            ledger.reserve_request(stage=stage, **reservation)
        leaf = ledger.request(request_id)
    request_id = leaf['request_id']
    stored = ledger.response(request_id)
    if accounting_required and stored is not None:
        ledger.account_producer_response(request_id, messages=messages, guard=accounting_guard)
    if stored and stored['record']:
        if accounting_required:
            ledger.validate_tokenizer_accounting_record(request_id, record=stored['record'])
        export_journal(ledger, stage, journal_path)
        if stored['record'].get('identity_valid') is not True:
            raise HarnessError('pilot suspended by persisted response identity mismatch')
        return stored['record']
    if not fresh and stored is None:
        raise HarnessError('uncertain request blocks resume; reconcile evidence before any resend')
    if stored is None:
        begin = time.monotonic()
        try:
            raw = transport(messages) if accounting_required else transport()
        except HarnessError:
            # A pre-transport guard failure is not a model transport observation.
            raise
        except Exception as exc:
            ledger.complete_request(request_id, status='FAILED', latency_ms=(time.monotonic()-begin)*1000, detail={'error_type': type(exc).__name__, 'message': str(exc)}, transport_failure=True)
            export_journal(ledger, stage, journal_path)
            if stage == 'stability_gate':
                return ledger.gate_transport_record(request_id)
            raise HarnessError('transport failed; uncertain outcome needs explicit reconciliation') from exc
        ledger.save_raw(request_id, raw, latency_ms=(time.monotonic()-begin)*1000)
        export_journal(ledger, stage, journal_path)
    else:
        raw = stored['raw']
    if accounting_required:
        ledger.account_producer_response(request_id, messages=messages, guard=accounting_guard)
    capture = ledger.response(request_id)['capture']
    record = evaluate(raw)
    record['received_utc'] = capture['received_utc']
    record['latency_seconds'] = None if capture['latency_ms'] is None else capture['latency_ms']/1000
    record.update(request_id=request_id, prompt_sha256=spec['prompt_sha256'])
    record['identity_valid'] = response_identity_valid(record, expected_identity)
    if accounting_required:
        ledger.bind_tokenizer_accounting_record(request_id, record=record)
    ledger.complete_request(request_id, status='COMPLETED', record=record,
                            prompt_tokens=record.get('prompt_tokens'), completion_tokens=record.get('completion_tokens'),
                            total_tokens=record.get('total_tokens'), latency_ms=capture['latency_ms'])
    export_journal(ledger, stage, journal_path)
    if not record['identity_valid']:
        raise HarnessError('pilot suspended: returned model/fingerprint missing or changed; raw and consumption preserved')
    return record
