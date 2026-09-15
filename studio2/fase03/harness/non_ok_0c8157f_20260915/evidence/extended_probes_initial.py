"""Independent assertions on the corrected candidate. SACRIFICIAL OFFLINE FIXTURES.
No transport boundary can open sockets; expected failures remain uncorrected.
Uses supplied Trial/RunnerRevisions setup as fixture builders, never their assertions.
"""
from pathlib import Path
import sys, os, json, shutil, unittest, sqlite3, subprocess, types
from contextlib import closing
from copy import deepcopy
from unittest.mock import patch
E=Path(__file__).resolve().parent; C=E.parent/'candidate'
sys.path.insert(0,str(C))
os.environ['PYTHONDONTWRITEBYTECODE']='1'
from studio2.fase03.harness.offline_fixtures import Trial, sample
from studio2.fase03.harness.ledger import PilotLedger, digest
from studio2.fase03.harness.common import HarnessError, sha256_file, sha256_text
from studio2.fase03.harness.gate_rules import evaluate_stability_gate
from studio2.fase03.harness import runtime
from studio2.fase03.harness.test_revisions import RunnerRevisions, rp, pp, pg, SCHEMA
OBS={}

class Extended(unittest.TestCase):
    def setUp(self):
        self.home=E/'extended_fixtures'/self._testMethodName
        self.home.mkdir(parents=True,exist_ok=False)
        self.net=patch('socket.socket',side_effect=AssertionError('NETWORK FORBIDDEN'));self.net.start();self.addCleanup(self.net.stop)
        self.t=Trial(self.home);self.l=self.t.ledger
    def note(self,**values):OBS.setdefault(self._testMethodName,{}).update(values)
    def runner(self):
        t=RunnerRevisions();t.setUp()
        self.addCleanup(t.doCleanups)
        self.addCleanup(lambda:shutil.copytree(t.home,self.home/'runner',dirs_exist_ok=True))
        return t
    def test_X01_incomplete_alternate_blocks_probe(self):
        self.t.finish();self.t.bind('alternate_conformity');self.t.reserve(0,'alternate_conformity')
        self.l=PilotLedger(self.l.path,pilot_id=self.l.pilot_id);self.t.ledger=self.l
        caught=None
        try:self.t.finish('budget_probe',3)
        except HarnessError as exc:caught=str(exc)
        self.note(error=caught,snapshot=self.l.snapshot())
        self.assertIsNotNone(caught,'budget PASS must not strand an unresolved producer stage')
    def test_X02_failed_alternate_blocks_real_consumer(self):
        t=self.runner();t.prepare();t.fail_at=9
        with self.assertRaises(HarnessError):t.producer(stage='alternate_conformity')
        caught=None
        try:result=rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        except HarnessError as exc:caught=str(exc);result=None
        self.note(error=caught,budget_status=result and result['status'],calls=len(t.consumer_calls),snapshot=t.ledger.snapshot())
        self.assertEqual(t.consumer_calls,[],'an unresolved alternate attempt must block transition')
    def test_X03_gate_transport_invalidity_remains_in_T3_T6(self):
        t=self.runner();t.prepare();rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        stub=rp.Provider
        class TimeoutOnce(stub):
            def call(inner,**kw):
                if len(t.consumer_calls)==4:
                    t.consumer_calls.append('FAILED_TRANSPORT_FIXTURE');raise TimeoutError('single gate transport failure')
                return super().call(**kw)
        caught=None;result=None
        with patch.object(rp,'Provider',TimeoutOnce):
            try:result=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
            except HarnessError as exc:caught=str(exc)
        self.note(error=caught,result=result,calls=len(t.consumer_calls),snapshot=t.ledger.snapshot(),records=t.ledger.stage_records('stability_gate'))
        self.assertIsNotNone(result,'N48 normative invalidity must remain in a 120-attempt T3/T6 evaluation')
        self.assertEqual(result['invalid_first_attempts'],1);self.assertEqual(result['provider_requests'],120)
        self.assertEqual(result['status'],'R3_REQUIRED_PENDING_FEASIBILITY')
    def test_X04_late_retry_is_rejected_before_and_after_restart(self):
        self.t.bind();r=self.t.reserve(0);self.t.zero(r);self.t.complete(self.t.retry(r,'successful-retry'))
        for i in range(1,8):self.t.complete(self.t.reserve(i))
        self.t.outcome('producer_conformity')
        for _ in range(2):
            with self.assertRaises(HarnessError):self.t.retry(r,'late-retry')
            self.t.ledger=PilotLedger(self.l.path,pilot_id=self.l.pilot_id)
        self.t.finish('budget_probe',3);self.note(snapshot=self.l.snapshot())
        self.assertEqual(self.l.snapshot()['unresolved_intents'],0)
    def test_X05_interrupted_primary_cannot_be_closed_or_skipped(self):
        self.t.bind()
        for i in range(8):
            r=self.t.reserve(i)
            if i<7:self.t.complete(r)
        for outcome in ('PASS','FAIL','BLOCKED'):
            with self.assertRaises(HarnessError):self.t.outcome('producer_conformity',outcome)
        with self.assertRaises(HarnessError):self.t.bind('budget_probe',3)
        self.note(snapshot=self.l.snapshot())
    def test_X06_real_concurrent_base_reservation_12_writers(self):
        self.t.bind()
        code="""import sys
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness.common import HarnessError
t=Trial(sys.argv[1])
try:t.reserve(0,request_id=sys.argv[2])
except HarnessError:sys.exit(17)
"""
        procs=[subprocess.Popen([sys.executable,'-c',code,str(self.home),f'writer-{i}'],env=dict(os.environ,PYTHONPATH=str(C))) for i in range(12)]
        codes=sorted(p.wait() for p in procs);self.note(returncodes=codes,snapshot=self.l.snapshot())
        self.assertEqual(codes,[0]+[17]*11);self.assertEqual(self.l.snapshot()['requests_cumulative'],1)
    def test_X07_outcome_transaction_excludes_writer_while_closing(self):
        self.t.bind()
        for i in range(8):self.t.complete(self.t.reserve(i))
        marker=self.home/'writer-attempted';done=self.home/'writer-done'
        code="""import sys
from pathlib import Path
from studio2.fase03.harness.ledger import PilotLedger
from studio2.fase03.harness.common import HarnessError
p=Path(sys.argv[1]);l=PilotLedger.__new__(PilotLedger);l.path=p/'pilot.sqlite3';l.pilot_id='offline-fixture'
(p/'writer-attempted').write_text('started')
try:l.bind_stage('producer_conformity',{'requests':[]})
except HarnessError:pass
# The actual writer transaction must wait for the outcome transaction.
with l._transaction() as c:
    state=c.execute("select count(*) from events where event='outcome:producer_conformity'").fetchone()[0]
(p/'writer-done').write_text(str(state))
"""
        original=self.l._event;procs=[]
        def at_commit(c,event,sha,detail):
            if event=='outcome:producer_conformity':
                p=subprocess.Popen([sys.executable,'-c',code,str(self.home)],env=dict(os.environ,PYTHONPATH=str(C)));procs.append(p)
                import time
                deadline=time.monotonic()+5
                while not marker.exists() and time.monotonic()<deadline:time.sleep(.01)
                self.assertTrue(marker.exists());self.assertFalse(done.exists())
            return original(c,event,sha,detail)
        with patch.object(self.l,'_event',side_effect=at_commit):self.t.outcome('producer_conformity')
        self.assertEqual(procs[0].wait(),0);self.assertEqual(done.read_text(),'1')
        self.note(writer_saw_committed_outcome=done.read_text())
    def test_X08_retry_triplet_rollback_after_one_insertion_at_quota(self):
        self.t.bind();r=self.t.reserve(0);self.t.zero(r)
        for i in range(6):
            r=self.t.retry(r,f'producer-retry-{i}')
            if i<5:self.t.zero(r)
            else:self.t.complete(r)
        for i in range(1,8):self.t.complete(self.t.reserve(i))
        self.t.outcome('producer_conformity');self.t.bind('budget_probe',3)
        ids=[self.t.reserve(i,'budget_probe') for i in range(3)]
        for r in ids:self.t.zero(r)
        values=[]
        for i,r in enumerate(ids):
            v=self.l.request(r);values.append(dict(request_id=f'probe-retry-{i}',logical_id=v['logical_id'],model=v['model'],producer=v['producer'],stage_run=v['stage_run'],retry_of=r,condition=('A','B-LF','E-LF')[i]))
        before=self.l.snapshot()
        with self.assertRaises(HarnessError):self.l.reserve_probe_transport_triplet(values)
        self.assertEqual(self.l.snapshot(),before);self.note(snapshot=before,rollback='all three absent')
    def test_X09_zero_token_proof_rejects_positive_tokens_wrong_identity_missing_author(self):
        self.t.bind();r=self.t.reserve(0);row=self.l.request(r)
        good=dict(request_id=r,request_identity_sha256=sha256_text(row['identity_json']),disposition='not_generated',provider_request_id='FIXTURE',provider_evidence='offline fixture',prompt_tokens=0,completion_tokens=0,total_tokens=0)
        changes=[{'total_tokens':1},{'completion_tokens':True},{'request_identity_sha256':'a'*64},{'provider_evidence':''},{'request_id':'another'}]
        for change in changes+[{}]:
            value=dict(good,**change);e=self.home/'proof.json';e.write_text(json.dumps(value));a=self.home/'approval.json'
            a.write_text(json.dumps(dict(author='FIXTURE' if change else '',decision='accepted',evidence_sha256=sha256_file(e))))
            with self.assertRaises(HarnessError):self.l.reconcile_zero_token(r,evidence_path=e,approval_path=a)
            self.assertEqual(self.l.request(r)['status'],'INTENT')
        self.note(rejected_variants=len(changes)+1)
    def test_X10_remediation_concrete_diff_diagnosis_template_coverage(self):
        self.t.finish(valid=False);self.t.remediation()
        original=self.l.binding('producer_remediation')
        for key in ('case_sha256','contract_sha256','model','producer'):
            value=deepcopy(original);value['requests'][0][key]='b'*64 if key.endswith('sha256') else 'different'
            with self.assertRaises(HarnessError):self.l.bind_stage('producer_remediation',value)
        with self.assertRaises(HarnessError):self.t.remediation()
        self.note(snapshot=self.l.snapshot(),rejected_changes=4)
    def test_X11_gate_boolean_repetitions_bad_roles_and_frozen_text(self):
        def rows(prompts):return [dict(p,request_id=f"{p['prompt_id']}-{r}",repetition=r,identity_valid=True,parse_valid_first_attempt=True,parsed_output={'abstain':True,'predicted_label':None},finish_reason='stop') for p in prompts for r in (1,2,3)]
        for variant in ('bool','role','agent','hash','text','retry'):
            ps=sample();rs=rows(ps)
            if variant=='bool':rs[0]['repetition']=True
            if variant=='role':ps[0]['sample_role']='context_stress';rs=rows(ps)
            if variant=='agent':ps[0]['agent_id']='agent_9';rs=rows(ps)
            if variant=='hash':ps[1]['prompt_sha256']=ps[0]['prompt_sha256'];rs=rows(ps)
            if variant=='text':ps[0]['text']='changed';rs=rows(ps)
            if variant=='retry':rs[0]['retry_count']=1
            with self.subTest(variant=variant),self.assertRaises(HarnessError):evaluate_stability_gate(rs,expected_prompts=ps)
        self.note(rejected_variants=6)
    def test_X12_r4_rechecked_mid_producer_before_next_send(self):
        t=self.runner();schema=self.home/'schema';shutil.copytree(SCHEMA,schema)
        original=runtime.export_journal
        def tamper(ledger,stage,path):
            original(ledger,stage,path)
            if ledger.stage_records(stage):
                with (schema/'validator.py').open('a') as f:f.write('\n')
        with patch.object(runtime,'export_journal',side_effect=tamper),self.assertRaises(HarnessError):t.producer(schema_dir=schema)
        self.note(calls=len(t.calls),snapshot=t.ledger.snapshot());self.assertEqual(len(t.calls),1)
    def test_X13_changed_fingerprint_preserves_tokens_and_suspends(self):
        t=self.runner();p=json.loads(t.provider.read_text());p['expected_response']['system_fingerprint']='EXPECTED';t.provider.write_text(json.dumps(p))
        t.config['approved_producer_config_sha256']=[sha256_file(t.provider)];t.approve_config()
        with self.assertRaises(HarnessError):t.producer()
        r=t.ledger.leaf('producer_conformity','agent_1');raw=t.ledger.response(r['request_id'])
        self.note(request=r,raw=raw,snapshot=t.ledger.snapshot())
        self.assertEqual(r['total_tokens'],5);self.assertIsNone(raw['raw']['system_fingerprint'])
        self.assertFalse(raw['record']['identity_valid']);self.assertEqual(len(t.calls),1)
        with self.assertRaises(HarnessError):t.producer(resume=True)
        self.assertEqual(len(t.calls),1)
    def test_X14_corrupted_durable_record_cannot_resume_or_pass(self):
        self.t.bind();r=self.t.reserve(0);self.t.complete(r)
        with closing(sqlite3.connect(self.l.path)) as c,c:c.execute("update responses set record_json='{}' where request_id=?",(r,))
        with self.assertRaises(HarnessError):self.l.response(r)
        for i in range(1,8):self.t.complete(self.t.reserve(i))
        with self.assertRaises(HarnessError):self.t.outcome('producer_conformity')
        self.note(snapshot=self.l.snapshot())
    def test_X15_producer_summary_counts_retry_provider_requests(self):
        t=self.runner();t.fail_at=2
        with self.assertRaises(HarnessError):t.producer()
        r=t.ledger.leaf('producer_conformity','agent_2')['request_id'];helper=Trial(self.home/'helper');helper.ledger=t.ledger;helper.zero(r)
        result=t.producer(resume=True,retry_requests=[r]);self.note(summary=result,snapshot=t.ledger.snapshot(),stub_calls=len(t.calls))
        self.assertEqual(result['provider_requests'],9,'provider_requests must retain the separate call denominator after retry')
    def test_X16_gate_raw_crash_and_closed_file_resume(self):
        t=self.runner();t.prepare();rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        original=runtime.export_journal
        def stop(ledger,stage,path):
            original(ledger,stage,path)
            if stage=='stability_gate':raise KeyboardInterrupt('after saved raw')
        with patch.object(runtime,'export_journal',side_effect=stop),self.assertRaises(KeyboardInterrupt):rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
        self.assertEqual(len(t.consumer_calls),4)
        result=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
        self.assertEqual(len(t.consumer_calls),123)
        p=t.results/'stability_summary.json';p.unlink()
        again=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
        self.assertEqual(again,result);self.assertTrue(p.is_file());self.assertEqual(len(t.consumer_calls),123)
        self.note(summary=result,snapshot=t.ledger.snapshot())
    def test_X17_approval_hash_and_presentation_order_binding(self):
        t=self.runner();t.config['candidate']['requested_model']='UNAPPROVED';t.config_path.write_text(json.dumps(t.config))
        with self.assertRaises(HarnessError):t.producer()
        self.assertEqual(t.calls,[])
        t.config['candidate']['requested_model']='fixture-model';t.approve_config();t.prepare()
        approval=Path(t.config['presentation_approval']['path']);value=json.loads(approval.read_text());value['ordered_labels_sha256']='a'*64;approval.write_text(json.dumps(value))
        t.config['presentation_approval']['sha256']=sha256_file(approval);t.approve_config()
        with self.assertRaises((HarnessError,RuntimeError)):rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        self.note(consumer_calls=t.consumer_calls);self.assertEqual(t.consumer_calls,[])
    def test_X18_frozen_reformatted_bytes_rejected_without_call(self):
        t=self.runner();t.prepare();rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        p=t.results/'frozen_gate_config.json';v=json.loads(p.read_text());p.write_text(json.dumps(v,separators=(',',':')))
        with self.assertRaisesRegex(RuntimeError,'bytes changed'):rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
        self.note(calls=len(t.consumer_calls));self.assertEqual(len(t.consumer_calls),3)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(Extended)
    with (E/'extended.log').open('w') as stream:result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    summary=dict(tests=result.testsRun,failures=[{'id':t.id(),'traceback':s} for t,s in result.failures],errors=[{'id':t.id(),'traceback':s} for t,s in result.errors],observations=OBS)
    (E/'extended.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(dict(tests=result.testsRun,failures=len(result.failures),errors=len(result.errors))))
    sys.exit(not result.wasSuccessful())
