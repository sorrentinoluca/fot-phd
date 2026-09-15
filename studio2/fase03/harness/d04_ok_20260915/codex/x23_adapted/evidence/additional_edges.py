"""Additional independent edge cases needed to substantiate original-test mapping."""
import extended_probes as m
from pathlib import Path
from copy import deepcopy
from contextlib import closing
from unittest.mock import patch
import json,unittest,subprocess,sys,os,sqlite3
m.E=m.E/'additional_edges';m.E.mkdir(exist_ok=False)

class Edges(m.Extended):
    # Inherited tests are not loaded; only the explicitly selected X19+ methods below run.
    def test_X19_alternate_base_quota_cannot_fund_transport(self):
        self.t.bind();r=self.t.reserve(0);self.t.zero(r)
        self.l.waive_remediation(approval_sha256='a'*64)
        for i in range(15):
            r=self.t.retry(r,f'transport-{i}')
            if i<14:self.t.zero(r)
            else:self.t.complete(r)
        for i in range(1,8):self.t.complete(self.t.reserve(i))
        self.t.outcome('producer_conformity');self.t.bind('alternate_conformity')
        ar=self.t.reserve(0,'alternate_conformity');self.t.zero(ar)
        before=self.l.snapshot()
        with self.assertRaises(m.HarnessError):self.t.retry(ar,'alternate-as-transport-16')
        self.assertEqual(before,self.l.snapshot());self.note(snapshot=before)
    def test_X20_first_remediation_binding_rejects_changed_cases_and_contract(self):
        for key in ('case_sha256','contract_sha256','model','producer','inventory_sha256','template_text'):
            t=m.Trial(self.home/key);t.finish(valid=False);t.remediation(bind=False)
            b=t.ledger.binding('producer_conformity');b['template_text']=(t.home/'template.txt').read_text()
            if key in ('case_sha256','contract_sha256'):b['requests'][0][key]='b'*64
            elif key in ('model','producer'):b['requests'][0][key]='CHANGED'
            else:b[key]='UNAPPROVED'
            with self.subTest(key=key),self.assertRaises(m.HarnessError):t.ledger.bind_stage('producer_remediation',b)
            self.assertEqual(t.ledger.snapshot()['requests_by_stage']['producer_remediation'],0)
        self.note(rejected_first_bindings=6)
    def test_X21_cli_reconciliation_and_real_restart_use_same_intent(self):
        self.t.bind();r=self.t.reserve(0);row=self.l.request(r)
        e=self.home/'provider_proof.json';e.write_text(json.dumps(dict(request_id=r,request_identity_sha256=m.sha256_text(row['identity_json']),disposition='not_generated',provider_request_id='FIXTURE-CLI',provider_evidence='offline fixture only',prompt_tokens=0,completion_tokens=0,total_tokens=0)))
        a=self.home/'author.json';a.write_text(json.dumps(dict(author='FIXTURE ONLY',decision='accepted',evidence_sha256=m.sha256_file(e))))
        args=[sys.executable,'-m','studio2.fase03.harness.ledger_cli','--ledger',str(self.l.path),'--pilot-id',self.l.pilot_id]
        result=subprocess.run(args+['reconcile-zero-token','--request-id',r,'--evidence',str(e),'--approval',str(a)],cwd=m.C,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
        (self.home/'cli.stdout').write_text(result.stdout);(self.home/'cli.stderr').write_text(result.stderr)
        self.assertEqual(result.returncode,0);self.t.ledger=m.PilotLedger(self.l.path,pilot_id=self.l.pilot_id)
        self.t.complete(self.t.retry(r,'after-cli-reconciliation'))
        self.assertEqual(self.l.snapshot()['requests_cumulative'],2);self.assertEqual(self.l.snapshot()['transport_calls'],1)
        self.note(returncode=result.returncode,snapshot=self.l.snapshot())
    def test_X22_identity_mismatch_in_budget_blocks_whole_pilot(self):
        t=self.runner();t.prepare();t.consumer_identity=1
        with self.assertRaises(m.HarnessError):m.rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        self.assertEqual(len(t.consumer_calls),1);self.assertEqual(t.ledger.snapshot()['requests_by_stage']['budget_probe'],1)
        with self.assertRaises(m.HarnessError):m.rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
        self.assertEqual(len(t.consumer_calls),1);self.note(snapshot=t.ledger.snapshot())
    def test_X23_failed_gate_resume_and_zero_token_do_not_erase_failure(self):
        t=self.runner();t.prepare();m.rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        stub=m.rp.Provider
        class Fail(stub):
            def call(inner,**kwargs):t.consumer_calls.append('FAILED-FIXTURE');raise TimeoutError('unknown transport')
        with patch.object(m.rp,'Provider',Fail):result=m.rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
        self.assertEqual(result['invalid_first_attempts'],120)
        self.assertEqual(result['provider_requests'],120)
        self.assertFalse(result['t3_pass']);self.assertFalse(result['t6_evaluable'])
        self.assertEqual(result['status'],'NO_GO_TECHNICAL')
        self.assertEqual(len(t.consumer_calls),123)
        records=t.ledger.stage_records('stability_gate')
        row=t.ledger.leaf('stability_gate',t.ledger.binding('stability_gate')['requests'][0]['logical_id'])
        self.assertIsNone(t.ledger.response(row['request_id']))
        self.assertIsNone(records[0]['identity_valid']);self.assertIsNone(records[0]['total_tokens'])
        helper=m.Trial(self.home/'helper');helper.ledger=t.ledger;helper.zero(row['request_id'])
        t.ledger=m.PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
        resumed=m.rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
        self.assertEqual(resumed,result);self.assertEqual(t.ledger.stage_records('stability_gate'),records)
        self.assertEqual(len(t.consumer_calls),123);self.assertEqual(t.ledger.snapshot()['requests_cumulative'],131)
        self.assertEqual(t.ledger.event('outcome:stability_gate')['outcome'],'FAIL')
        self.note(snapshot=t.ledger.snapshot(),raw_count=0,invalid_records=len(records),result=result)
    def test_X24_primary_structure_envelope_defect_is_remediable(self):
        t=self.runner()
        # Reuse the actual R4 runner but return valid JSON with the wrong envelope.
        original=sys.modules['openai'].OpenAI
        def factory(**kwargs):
            client=original(**kwargs);create=client.chat.completions.create
            def malformed(**kw):
                response=create(**kw);raw=response.model_dump(mode='json')
                if len(t.calls)==1:raw['choices'][0]['message']['content']='{"unexpected": []}'
                import types
                return types.SimpleNamespace(model_dump=lambda **kw:raw)
            client.chat.completions.create=malformed;return client
        with patch.object(sys.modules['openai'],'OpenAI',side_effect=factory):result=t.producer(diagnosis='structure')
        self.assertEqual(result['valid_first_attempts'],7)
        helper=m.Trial(self.home/'helper');helper.ledger=t.ledger;helper.remediation(bind=False)
        out=t.producer(stage='producer_remediation',template_path=helper.home/'template.txt')
        self.assertEqual(out['status'],'PASS');self.assertEqual(len(t.calls),16)
        self.note(first=result,remediation=out,snapshot=t.ledger.snapshot())

names=['test_X23_failed_gate_resume_and_zero_token_do_not_erase_failure']
with (m.E/'additional.log').open('w') as f:r=unittest.TextTestRunner(stream=f,verbosity=2).run(unittest.TestSuite(Edges(n) for n in names))
(m.E/'additional.json').write_text(json.dumps(dict(tests=r.testsRun,failures=[{'id':t.id(),'traceback':s} for t,s in r.failures],errors=[{'id':t.id(),'traceback':s} for t,s in r.errors],observations=m.OBS),indent=2)+'\n')
print(r.testsRun,len(r.failures),len(r.errors))
