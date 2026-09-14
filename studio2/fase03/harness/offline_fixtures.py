"""SACRIFICIAL TEST HELPERS ONLY. No fixture is a scientific approval or result."""
from copy import deepcopy
from pathlib import Path
import difflib
import json

from .common import sha256_text, sha256_file
from .ledger import PilotLedger, digest


def sample():
    return [dict(prompt_id=f'P-{i:02d}', condition='A' if i<8 else 'B-LF' if i<24 else 'E-LF',
                 agent_id=f'agent_{i%8+1}', case_id=f'case-{i%8}-' + ('transfer' if i<16 or 24<=i<32 else 'stress'), sample_role='matched_transfer' if i<16 or 24<=i<32 else 'context_stress',
                 text=f'FIXTURE ONLY prompt {i}', prompt_sha256=sha256_text(f'FIXTURE ONLY prompt {i}')) for i in range(40)]


class Trial:
    def __init__(self, home, pilot_id='offline-fixture'):
        self.home=Path(home); self.home.mkdir(parents=True,exist_ok=True)
        self.ledger=PilotLedger(self.home/'pilot.sqlite3', pilot_id=pilot_id)

    def binding(self, stage, n=None):
        n=n or (9 if stage=='budget_probe' else 120 if stage=='stability_gate' else 8)
        specs=[]
        for i in range(n):
            p=sample()[i//3] if stage=='stability_gate' else None
            specs.append(dict(logical_id=f'case-{i}',model='fixture-model',producer='fixture-producer',
                              prompt_sha256=p['prompt_sha256'] if p else sha256_text(f'prompt-{i}'),
                              case_sha256=digest(i),contract_sha256=digest(i),
                              condition=p['condition'] if p else ('A','B-LF','E-LF')[i%3] if stage=='budget_probe' else 'producer',
                              group=p['prompt_id'] if p else str(i//3) if stage=='budget_probe' else str(i), repetition=i%3+1 if p else 1))
        return dict(requests=specs,template_text='original fixture template\n',inventory_sha256=digest('fixture'))

    def bind(self, stage='producer_conformity', n=None):
        b=self.binding(stage,n);self.ledger.bind_stage(stage,b);return b

    def reserve(self,i,stage='producer_conformity',request_id=None):
        b=self.ledger.binding(stage);spec=b['requests'][i]
        kw=dict(request_id=request_id or f'{stage}-{i}', logical_id=spec['logical_id'],model=spec['model'],producer=spec['producer'],stage_run=digest(b))
        if stage=='producer_remediation':self.ledger.reserve_remediation_request(**kw)
        else:self.ledger.reserve_request(stage=stage,**kw)
        return kw['request_id']

    def complete(self, request_id, valid=True, raw=None):
        row=self.ledger.request(request_id);spec=json.loads(row['identity_json'])
        record=dict(request_id=request_id,prompt_sha256=spec['prompt_sha256'],identity_valid=True,
                    schema_valid_first_attempt=valid,validation_class=None if valid else 'structure',parse_valid_first_attempt=valid,finish_reason='stop',
                    generation={'max_tokens':2560},raw_output='FIXTURE RAW')
        if row['stage']=='budget_probe' and int(spec['logical_id'].split('-')[1]) < len(self.ledger.binding('budget_probe')['requests'])-3:
            record['finish_reason']='length'
        if row['stage']=='stability_gate':
            record.update(sample()[int(spec['logical_id'].split('-')[1])//3],repetition=spec['repetition'],parsed_output={'abstain':True,'predicted_label':None})
        self.ledger.save_raw(request_id,raw or {'fixture':'raw'})
        self.ledger.complete_request(request_id,status='COMPLETED',record=record)
        return record

    def zero(self, request_id):
        row=self.ledger.request(request_id)
        evidence=dict(request_id=request_id,request_identity_sha256=sha256_text(row['identity_json']),
                      disposition='not_generated',provider_request_id='FIXTURE-'+request_id, provider_evidence='SACRIFICIAL STUB REPORT',
                      prompt_tokens=0,completion_tokens=0,total_tokens=0)
        e=self.home/'evidence.json';e.write_text(json.dumps(evidence))
        a=self.home/'approval.json';a.write_text(json.dumps(dict(author='FIXTURE ONLY',decision='accepted',evidence_sha256=sha256_file(e))))
        self.ledger.reconcile_zero_token(request_id,evidence_path=e,approval_path=a)

    def retry(self, original, request_id):
        r=self.ledger.request(original)
        self.ledger.reserve_transport_retry(request_id=request_id,logical_id=r['logical_id'],model=r['model'],producer=r['producer'],stage=r['stage'],stage_run=r['stage_run'],retry_of=original)
        return request_id

    def outcome(self, stage, outcome='PASS',diagnosis=None):
        records=self.ledger.stage_records(stage);artifact=dict(records_sha256=digest(records))
        frozen=dict(generation={'max_tokens':2560},prompt_sample=sample()) if stage=='budget_probe' else None
        self.ledger.record_stage_outcome(stage,outcome=outcome,artifact_sha256=digest(artifact),artifact=artifact,diagnosis=diagnosis,frozen=frozen)

    def finish(self,stage='producer_conformity',n=None,valid=True):
        self.bind(stage,n)
        for i in range(n or len(self.ledger.binding(stage)['requests'])):self.complete(self.reserve(i,stage),valid=valid)
        self.outcome(stage,'PASS' if valid else 'FAIL',diagnosis='structure' if not valid else None)

    def remediation(self, bind=True):
        initial=self.ledger.binding('producer_conformity');template=initial['template_text']+'Approved FIXTURE change\n'
        diff=''.join(difflib.unified_diff(initial['template_text'].splitlines(True),template.splitlines(True),fromfile='before',tofile='after'))
        t=self.home/'template.txt';t.write_text(template);d=self.home/'diff.txt';d.write_text(diff)
        a=self.home/'remediation_approval.json';a.write_text(json.dumps(dict(author='FIXTURE ONLY',decision='accepted',diff_sha256=sha256_text(diff),template_sha256=sha256_text(template),initial_binding_sha256=digest(initial),diagnosis='structure')))
        self.ledger.authorize_remediation(diff_path=d,template_path=t,approval_path=a)
        b=deepcopy(initial);b['template_text']=template
        if bind:self.ledger.bind_stage('producer_remediation',b)
