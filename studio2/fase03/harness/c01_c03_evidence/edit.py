from pathlib import Path
root=Path('/Users/luker/fot-tep-harness-0310-c01-c03/studio2/fase03')
p=root/'harness/ledger.py';s=p.read_text()
s=s.replace("        if stage == 'budget_probe':\n            if any(r['stage'] == 'stability_gate' for r in rows):", "        if stage in {'budget_probe', 'stability_gate'}:\n            # Binding the optional alternate starts a cycle: it cannot be silently abandoned.\n            if c.execute(\"SELECT 1 FROM stages WHERE stage='alternate_conformity'\").fetchone():\n                self._successful(c, 'alternate_conformity')\n        if stage == 'budget_probe':\n            if any(r['stage'] == 'stability_gate' for r in rows):")
s=s.replace('proof_sha256=None, detail=None, record=None):','proof_sha256=None, detail=None, record=None, transport_failure=False):')
s=s.replace("            if status == 'COMPLETED' and (raw is None or record is None):", "            if transport_failure and (status != 'FAILED' or raw is not None or record is not None or not detail or not detail.get('error_type')):\n                raise HarnessError('transport failure requires an explicit error and no response')\n            if record is not None and raw is None:\n                raise HarnessError('response record requires durable raw')\n            if status == 'COMPLETED' and (raw is None or record is None):")
s=s.replace("            if record and record.get('identity_valid') is not True:","            if transport_failure and row['stage'] == 'stability_gate':\n                self._save_gate_transport_record(c, request_id)\n            if record and record.get('identity_valid') is not True:")
anchor='    def reconcile_zero_token(self, request_id, *, evidence_path: Path, approval_path: Path):'
methods='''    def _save_gate_transport_record(self, c, request_id):
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
        event = self._events(c).get('transport_invalidity:' + row['request_id'])
        if event is None:
            return None
        from .gate_rules import is_transport_invalidity
        record = json.loads(event['detail_json'])['record']
        if (row['stage'] != 'stability_gate' or row['status'] not in {'FAILED','ZERO_TOKEN_PROVEN'}
                or row['retry_of'] is not None or digest(record) != event['artifact_sha256']
                or record.get('request_id') != row['request_id']
                or record.get('request_identity_sha256') != sha256_text(row['identity_json'])
                or not is_transport_invalidity(record)
                or c.execute('SELECT 1 FROM responses WHERE request_id=?', (row['request_id'],)).fetchone()):
            raise HarnessError('persisted transport invalidity is not authentic')
        return record

    def gate_transport_record(self, request_id):
        with closing(self._connect()) as c:
            row = c.execute('SELECT * FROM requests WHERE request_id=?', (request_id,)).fetchone()
            return None if row is None else self._gate_transport_record(c, row)

    def _evaluated_record(self, c, row):
        raw = c.execute('SELECT * FROM responses WHERE request_id=?', (row['request_id'],)).fetchone()
        if raw and raw['record_json']:
            if sha256_text(raw['record_json']) != raw['record_sha256'] or sha256_text(raw['raw_json']) != raw['raw_sha256']:
                raise HarnessError('raw/record corruption')
            return json.loads(raw['record_json'])
        return self._gate_transport_record(c, row)

'''
s=s.replace(anchor,methods+anchor)
s=s.replace("(sha256_file(evidence_path), _utc_now(), request_id))\n\n    def stage_records", "(sha256_file(evidence_path), _utc_now(), request_id))\n            if row['stage'] == 'stability_gate':\n                self._save_gate_transport_record(c, request_id)\n\n    def stage_records")
a=s.index('        result = []\n',s.index('    def stage_records'))
b=s.index('    def record_stage_outcome',a)
s=s[:a]+'''            return [record for row in rows if (record := self._evaluated_record(c, row)) is not None]

'''+s[b:]
a=s.index('            records = []\n',s.index('    def record_stage_outcome'))
b=s.index("                if stage in {'producer_conformity'",a)
s=s[:a]+'''            records = [record for row in leaves if (record := self._evaluated_record(c, row)) is not None]
            if stage == 'stability_gate':
                if len(records) != n or any(r['status'] != 'COMPLETED' and self._gate_transport_record(c, r) is None for r in leaves):
                    raise HarnessError('gate requires a response or durable transport invalidity for every attempt')
            if outcome == 'PASS':
                if len(records) != n or (stage != 'stability_gate' and (
                        any(r['status'] != 'COMPLETED' for r in leaves)
                        or any(r.get('identity_valid') is not True for r in records))):
                    raise HarnessError("PASS requires resolved authenticated responses")
'''+s[b:]
p.write_text(s)
p=root/'harness/gate_rules.py';s=p.read_text();a=s.index('\ndef semantic_signature')
s=s[:a]+'''
def is_transport_invalidity(record):
    """An absent response is invalid, never an identity-verified model response.

    The ledger authenticates the event; this evaluator checks its shape and still checks
    frozen prompt metadata/repetitions below. Arbitrary missing identities remain errors.
    """
    return (record.get('record_kind') == 'transport_invalidity'
            and record.get('response_received') is False
            and record.get('parse_valid_first_attempt') is False
            and all(k in record and record[k] is None for k in (
                'identity_valid','returned_model','system_fingerprint','response_id',
                'raw_output','raw_output_sha256','received_utc','parsed_output','finish_reason',
                'prompt_tokens','completion_tokens','total_tokens'))
            and isinstance(record.get('transport_error'), dict)
            and bool(record['transport_error'].get('error_type'))
            and isinstance(record.get('request_identity_sha256'), str)
            and len(record['request_identity_sha256']) == 64)

'''+s[a:]
s=s.replace("if r.get('retry_count', 0) != 0 or r.get('identity_valid') is not True:","if r.get('retry_count', 0) != 0 or (r.get('identity_valid') is not True and not is_transport_invalidity(r)):")
s=s.replace("'gate requires first attempts and verified response identity'","'gate requires first attempts with verified response identity or explicit transport invalidity'")
p.write_text(s)
p=root/'harness/runtime.py';s=p.read_text()
s=s.replace('rows.append(dict(request=leaf, response=response))',"rows.append(dict(request=leaf, response=response, transport_invalidity=ledger.gate_transport_record(leaf['request_id'])))")
s=s.replace("    if leaf and leaf['status'] == 'ZERO_TOKEN_PROVEN':", "    if leaf and stage == 'stability_gate':\n        invalidity = ledger.gate_transport_record(leaf['request_id'])\n        if invalidity is not None:\n            export_journal(ledger, stage, journal_path)\n            return invalidity\n    if leaf and leaf['status'] == 'ZERO_TOKEN_PROVEN':")
s=s.replace("        except Exception as exc:\n            ledger.complete_request", "        except HarnessError:\n            # A pre-transport guard failure is not a model transport observation.\n            raise\n        except Exception as exc:\n            ledger.complete_request")
s=s.replace("detail={'error_type': type(exc).__name__, 'message': str(exc)})", "detail={'error_type': type(exc).__name__, 'message': str(exc)}, transport_failure=True)")
s=s.replace("            raise HarnessError('transport failed; uncertain outcome needs explicit reconciliation') from exc", "            if stage == 'stability_gate':\n                return ledger.gate_transport_record(request_id)\n            raise HarnessError('transport failed; uncertain outcome needs explicit reconciliation') from exc")
p.write_text(s)
p=root/'run_pilot.py';s=p.read_text().replace('request_id=None, return_error_record=False, config=None, journal_path=None,','request_id=None, config=None, journal_path=None,');p.write_text(s)
p=root/'producer_probe.py';s=p.read_text().replace("artifact_version='3', status='PASS' if passed else 'FAIL', stage=stage,", "artifact_version='4', status='PASS' if passed else 'FAIL', stage=stage,")
s=s.replace('producer_identity_sha256=digest(provider), provider_requests=len(records),',"producer_identity_sha256=digest(provider), provider_requests=ledger.snapshot()['requests_by_stage'][stage],\n                   evaluable_calls=len(records),")
p.write_text(s)
