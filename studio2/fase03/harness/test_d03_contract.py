"""D03 contract-first matrix. Deliberate faults only in disposable SQLite fixtures."""
from contextlib import closing
from copy import deepcopy
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
TARGET = Path(os.environ.get('FOT_HARNESS_TARGET', str(HERE.parents[2])))
if os.environ.get('FOT_HARNESS_TARGET'): sys.path.insert(0, str(TARGET))
from studio2.fase03.harness.common import HarnessError, canonical_json, sha256_text, sha256_file
from studio2.fase03.harness.ledger import PilotLedger, digest
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness import test_revisions as fixtures

CONTRACT = json.loads((HERE/'DURABLE_FIELD_CONTRACT.json').read_text())
FIELDS = [f for f in CONTRACT['fields'] if f['scope'] == 'zero_token']
OBS = {}


def logical(ledger):
    with closing(sqlite3.connect(ledger.path)) as c: return '\n'.join(c.iterdump())


def change(value, key, mutation):
    if mutation == 'missing': value.pop(key, None)
    else: value[key] = {'wrong_text':'INVALID FIXTURE', 'wrong_hash':'f'*64, 'empty':'',
                       'null':None, 'false':False, 'positive':1, 'negative':-1, 'string_zero':'0'}[mutation]


def content_digest(value): return digest(canonical_json(value))


class ProofContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(); cls.addClassCleanup(cls.tmp.cleanup)
        cls.sources = {}
        for route in ('retry','gate'):
            t = Trial(Path(cls.tmp.name)/route)
            if route == 'retry':
                t.bind(); r=t.reserve(0);t.zero(r);t.complete(t.retry(r,'retried-0'))
                for i in range(1,8):t.complete(t.reserve(i))
                t.outcome('producer_conformity');t.finish('budget_probe',3);t.finish('stability_gate')
                request='producer_conformity-0'
            else:
                t.finish();t.finish('budget_probe',3);t.bind('stability_gate')
                for i in range(120):
                    r=t.reserve(i,'stability_gate')
                    if i==0:t.zero(r)
                    else:t.complete(r)
                t.outcome('stability_gate');request='stability_gate-0'
            t.ledger.record_event('note:fixture',artifact_sha256='a'*64,detail={'note':'FORENSIC ONLY'})
            cls.sources[route]=(t,request)

    def setUp(self):
        self.tmp_case=tempfile.TemporaryDirectory();self.addCleanup(self.tmp_case.cleanup)
        self.home=Path(self.tmp_case.name);self.serial=0

    def copy(self, route='retry'):
        self.serial+=1;t=Trial(self.home/str(self.serial));src,request=self.sources[route]
        with closing(sqlite3.connect(src.ledger.path)) as a,closing(sqlite3.connect(t.ledger.path)) as b:a.backup(b)
        return t,request

    def execute(self, ledger, sql, values=()):
        with closing(sqlite3.connect(ledger.path)) as c,c:c.execute(sql,values)

    def detail(self, ledger, request):
        with closing(sqlite3.connect(ledger.path)) as c:return json.loads(c.execute('SELECT detail_json FROM events WHERE event=?',('reconciled:'+request,)).fetchone()[0])

    def write_detail(self, ledger, request, detail, *, align_digests=False):
        # Align local hashes only to exercise semantic rejection, never to claim cryptographic resistance.
        if align_digests:
            for key in ('evidence','approval'):
                if key+'_content_sha256' in detail:detail[key+'_content_sha256']=content_digest(detail[key])
            marker=ledger.event('reconciled_integrity:'+request)
            if marker:
                marker.pop('artifact_sha256')
                for key in ('evidence_content_sha256','approval_content_sha256'):marker[key]=detail[key]
                self.execute(ledger,'UPDATE events SET detail_json=?,artifact_sha256=? WHERE event=?',
                             (canonical_json(marker),digest(marker),'reconciled_integrity:'+request))
        self.execute(ledger,'UPDATE events SET detail_json=? WHERE event=?',(canonical_json(detail),'reconciled:'+request))

    def confirm(self, ledger, route):
        if route=='retry':ledger.verify_stage_success('stability_gate')
        else:self.assertIsNotNone(ledger.gate_transport_record('stability_gate-0'))

    def acquisition(self, evidence, approval):
        self.serial+=1;t=Trial(self.home/('acquire-'+str(self.serial)));t.bind();r=t.reserve(0)
        # Keep the evidence identity identical to the existing producer fixture.
        e=self.home/'input-evidence.json';a=self.home/'input-approval.json'
        e.write_text(json.dumps(evidence,indent=4));a.write_text(json.dumps(approval))
        before=logical(t.ledger)
        try:t.ledger.reconcile_zero_token(r,evidence_path=e,approval_path=a)
        finally:self.assertEqual(logical(t.ledger),before)

    def test_D03_generated_symmetric_content_matrix(self):
        results=[]
        for f in FIELDS:
            for mutation in f['mutations']:
                row=dict(field=f['path'],mutation=mutation,routes={})
                # Acquisition receives exact file binding, except when testing that binding itself.
                src,req=self.sources['retry'];d=self.detail(src.ledger,req)
                evidence,approval=deepcopy(d['evidence']),deepcopy(d['approval'])
                change(evidence if f['section']=='evidence' else approval,f['field'],mutation)
                if not (f['section']=='approval' and f['field']=='evidence_sha256'):
                    approval['evidence_sha256']=sha256_text(json.dumps(evidence,indent=4))
                try:self.acquisition(evidence,approval)
                except HarnessError:row['routes']['acquisition']=True
                else:row['routes']['acquisition']=False
                for route in ('retry','gate'):
                    t,req=self.copy(route);d=self.detail(t.ledger,req)
                    change(d[f['section']],f['field'],mutation)
                    self.write_detail(t.ledger,req,d,align_digests=True)
                    before=logical(t.ledger)
                    try:self.confirm(t.ledger,route)
                    except HarnessError:row['routes'][route]=True
                    else:row['routes'][route]=False
                    self.assertEqual(logical(t.ledger),before)
                results.append(row)
        OBS['symmetric']=results
        self.assertTrue(all(all(r['routes'].values()) for r in results),json.dumps([r for r in results if not all(r['routes'].values())]))

    def test_D03_three_paths_invoke_the_same_content_control_set(self):
        self.assertTrue(hasattr(PilotLedger,'_validate_zero_token_evidence'),'shared content validator absent')
        expected={f['section']+'.'+f['field'] for f in FIELDS};observed={}
        t=Trial(self.home/'acquisition');t.bind();req=t.reserve(0)
        scenarios=[('acquisition',t,lambda:t.zero(req))]
        for route in ('retry','gate'):
            fixture,_=self.copy(route);scenarios.append((route,fixture,lambda r=route,x=fixture:self.confirm(x.ledger,r)))
        for route,t,call in scenarios:
            seen=[];original=t.ledger._validate_zero_token_evidence
            def checked(evidence,approval,row):
                result=original(evidence,approval,row);seen.append(set(result));return result
            with patch.object(t.ledger,'_validate_zero_token_evidence',side_effect=checked):call()
            self.assertTrue(seen,route);self.assertTrue(all(s==expected for s in seen),route)
            observed[route]=sorted(seen[0])
        self.assertEqual(len({tuple(x) for x in observed.values()}),1);OBS['shared_controls']=observed

    def test_D03_content_digests_and_independent_link_reject_valid_looking_changes(self):
        results=[]
        for route in ('retry','gate'):
            for field in ('provider_request_id','provider_evidence','author','evidence_content_sha256','approval_content_sha256','previous_status','approval_sha256'):
                t,req=self.copy(route);d=self.detail(t.ledger,req)
                if field=='author':d['approval'][field]='A DIFFERENT VALID AUTHOR'
                elif field.startswith('provider_'):d['evidence'][field]='DIFFERENT NONEMPTY FIXTURE'
                else:d[field]='f'*64
                self.write_detail(t.ledger,req,d);before=logical(t.ledger);refused=False
                try:self.confirm(t.ledger,route)
                except HarnessError:refused=True
                results.append(dict(route=route,field=field,refused=refused));self.assertEqual(logical(t.ledger),before)
        OBS['digest_matrix']=results;self.assertTrue(all(r['refused'] for r in results),results)

    def test_D03_generated_sql_field_matrix_and_forensic_positive_controls(self):
        results=[]
        targets={'pilot':('id','offline-fixture'),'stages':('stage','producer_conformity'),
                 'requests':('request_id','producer_conformity-0'),'events':('event','reconciled:producer_conformity-0'),
                 'responses':('request_id','producer_conformity-1'),'receipts':('request_id','producer_conformity-1')}
        for f in (f for f in CONTRACT['fields'] if f['scope']=='sql'):
            t,_=self.copy();table,col=f['table'],f['column'];key,value=targets[table]
            replacement='{}' if col.endswith('_json') else 'ALTERED FIXTURE'
            if col in ('prompt_tokens','completion_tokens','total_tokens','latency_ms'):replacement=42
            self.execute(t.ledger,f'UPDATE {table} SET {col}=? WHERE {key}=?',(replacement,value))
            before=logical(t.ledger);refused=False
            try:
                t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
                self.confirm(t.ledger,'retry')
            except HarnessError:refused=True
            results.append(dict(field=f['path'],classification=f['kind'],refused=refused,expected_refusal=f['kind']=='N'))
            self.assertEqual(logical(t.ledger),before)
        # note:* payload, timestamp and hash remain wholly forensic.
        t,_=self.copy();self.execute(t.ledger,"UPDATE events SET detail_json='{}',artifact_sha256=?,created_utc=? WHERE event='note:fixture'",('f'*64,'different timestamp'))
        self.confirm(t.ledger,'retry')
        OBS['sql_matrix']=results
        self.assertTrue(all(r['refused']==r['expected_refusal'] for r in results),[r for r in results if r['refused']!=r['expected_refusal']])

    def test_D03_inventory_covers_schema_and_new_fields_default_to_uncovered(self):
        t,_=self.copy()
        def uncovered():
            missing=[]
            with closing(sqlite3.connect(t.ledger.path)) as c:
                for table in [r[0] for r in c.execute("SELECT name FROM sqlite_master WHERE type='table'")]:
                    for col in c.execute(f'PRAGMA table_info({table})'):
                        if col[1] not in CONTRACT['sql_tables'].get(table,{}):missing.append(table+'.'+col[1])
                for event,payload in c.execute('SELECT event,detail_json FROM events'):
                    kind=event.split(':')[0];spec=CONTRACT['event_payloads'].get(kind,{})
                    if '*' not in spec:
                        missing += [kind+'.'+key for key in json.loads(payload) if key not in spec]
            return missing
        self.assertEqual(uncovered(),[])
        self.execute(t.ledger,'ALTER TABLE requests ADD COLUMN future_field TEXT')
        self.assertIn('requests.future_field',uncovered())
        d=self.detail(t.ledger,'producer_conformity-0');d['future_proof_field']='unknown';self.write_detail(t.ledger,'producer_conformity-0',d)
        self.assertIn('reconciled.future_proof_field',uncovered());self.assertEqual(CONTRACT['default'],'DA_COPRIRE')

    def test_D03_missing_digest_is_fail_closed_without_backfill_even_before_retry(self):
        results=[]
        for route in ('retry','gate'):
            t,req=self.copy(route);d=self.detail(t.ledger,req)
            d.pop('evidence_content_sha256',None);d.pop('approval_content_sha256',None)
            self.write_detail(t.ledger,req,d)
            self.execute(t.ledger,'DELETE FROM events WHERE event=?',('reconciled_integrity:'+req,))
            before=logical(t.ledger);refused=False
            try:self.confirm(t.ledger,route)
            except HarnessError:refused=True
            results.append(dict(route=route,refused=refused));self.assertEqual(logical(t.ledger),before)
        t=Trial(self.home/'new-retry');t.bind();req=t.reserve(0);t.zero(req);d=self.detail(t.ledger,req)
        d.pop('evidence_content_sha256',None);self.write_detail(t.ledger,req,d);before=logical(t.ledger)
        try:t.retry(req,'must-not-send')
        except HarnessError:refused=True
        else:refused=False
        results.append(dict(route='new_retry',refused=refused));self.assertEqual(logical(t.ledger),before)
        OBS['legacy_policy']=results;self.assertTrue(all(r['refused'] for r in results),results)

    def test_D03_generated_reconciliation_envelope_matrix(self):
        results=[]
        fields=[f for f in CONTRACT['fields'] if f['scope']=='event_payload' and f['event'] in ('reconciled','reconciled_integrity')]
        for f in fields:
            t,req=self.copy();name=f['event']+':'+req
            with closing(sqlite3.connect(t.ledger.path)) as c:
                event=c.execute('SELECT detail_json FROM events WHERE event=?',(name,)).fetchone()
            if event is None:
                results.append(dict(field=f['path'],present=False,refused=False));continue
            d=json.loads(event[0]);d.pop(f['field'],None)
            self.execute(t.ledger,'UPDATE events SET detail_json=? WHERE event=?',(canonical_json(d),name))
            before=logical(t.ledger);refused=False
            try:self.confirm(t.ledger,'retry')
            except HarnessError:refused=True
            results.append(dict(field=f['path'],present=True,refused=refused));self.assertEqual(logical(t.ledger),before)
        OBS['envelope_matrix']=results;self.assertTrue(all(r['present'] and r['refused'] for r in results),results)

    def test_D03_real_legacy_proofs_rejected_without_rewriting_history(self):
        old=Path('/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate')
        self.assertEqual(subprocess.check_output(['git','-C',str(old),'rev-parse','HEAD'],text=True).strip(),'0c8157f23bee49a3a5a2df648525c34706da29d7')
        self.assertEqual(subprocess.check_output(['git','-C',str(old),'status','--porcelain=v1'],text=True),'')
        code="""import sys
from studio2.fase03.harness.offline_fixtures import Trial
t=Trial(sys.argv[1]);t.bind();r=t.reserve(0);t.zero(r);t.complete(t.retry(r,'legacy-retry'))
for i in range(1,8):t.complete(t.reserve(i))
t.outcome('producer_conformity');t.finish('budget_probe',3);t.finish('stability_gate')
"""
        home=self.home/'legacy'
        process=subprocess.run([sys.executable,'-c',code,str(home)],cwd=old,env=dict(os.environ,PYTHONPATH=str(old),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
        self.assertEqual(process.returncode,0,process.stderr)
        ledger=PilotLedger(home/'pilot.sqlite3',pilot_id='offline-fixture');before=logical(ledger)
        with self.assertRaises(HarnessError):ledger.verify_stage_success('stability_gate')
        self.assertEqual(logical(ledger),before);self.assertIsNone(ledger.event('reconciled_integrity:producer_conformity-0'))
        self.assertEqual(ledger.snapshot()['requests_cumulative'],132)

    def test_D03_real_runner_and_CLI_refuse_before_stub_and_preserve_outputs(self):
        t=fixtures.RunnerRevisions();t.setUp();self.addCleanup(t.doCleanups);t.fail_at=2
        with self.assertRaises(HarnessError):t.producer()
        req=t.ledger.leaf('producer_conformity','agent_2')['request_id'];helper=Trial(self.home/'helper');helper.ledger=t.ledger;helper.zero(req)
        t.producer(resume=True,retry_requests=[req]);t.prepare(producer=False)
        rp=fixtures.rp;rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger);rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
        d=self.detail(t.ledger,req);d['evidence'].update(prompt_tokens=1,total_tokens=1);self.write_detail(t.ledger,req,d)
        before=logical(t.ledger);files={p:p.read_bytes() for p in t.results.rglob('*') if p.is_file()};calls=len(t.consumer_calls);t.server_mock.reset_mock()
        t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id);errors=[]
        for stage,run in [('budget',rp.run_budget_stage),('stability',rp.run_stability_stage)]:
            try:run(t.prepared,t.results,ledger=t.ledger,resume=True)
            except HarnessError:errors.append(stage+'/runner')
            argv=['fixture','--execute','--acknowledge',rp.ACK,'--stage',stage,'--resume','--prepared-dir',str(t.prepared),'--results-dir',str(t.results),'--ledger',str(t.ledger.path),'--pilot-id',t.ledger.pilot_id]
            with patch.object(sys,'argv',argv):
                try:rp.main()
                except HarnessError:errors.append(stage+'/CLI')
        OBS['runner']=dict(refused=errors,server_calls=t.server_mock.call_count,new_sends=len(t.consumer_calls)-calls,snapshot=t.ledger.snapshot())
        self.assertEqual(len(errors),4);t.server_mock.assert_not_called();self.assertEqual(len(t.consumer_calls),calls)
        self.assertEqual(logical(t.ledger),before);self.assertEqual({p:p.read_bytes() for p in t.results.rglob('*') if p.is_file()},files);self.assertEqual(t.ledger.snapshot()['requests_cumulative'],132)


if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(ProofContract))
    output=os.environ.get('FOT_D03_OBSERVATIONS')
    if output:Path(output).write_text(json.dumps(dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),observations=OBS),indent=2)+'\n')
    sys.exit(not result.wasSuccessful())
