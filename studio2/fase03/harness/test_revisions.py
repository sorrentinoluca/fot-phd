"""R01–R10 regression probes. All approvals/responses are SACRIFICIAL FIXTURES.

External dependency boundaries only: local token counter and model SDK/server.
Sockets are prohibited. No test fixture qualifies scientific inputs or services.
"""
from contextlib import ExitStack, closing, redirect_stdout
from copy import deepcopy
import json
import io
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch

from studio2.fase03 import producer_probe as pp, run_pilot as rp, prepare_gate as pg, protocol
from studio2.fase03.harness import inputs
from studio2.fase03.harness.common import HarnessError, canonical_json, sha256_file, sha256_text
from studio2.fase03.harness.ledger import PilotLedger, digest
from studio2.fase03.harness.offline_fixtures import Trial, sample
from studio2.fase03.harness.gate_rules import evaluate_stability_gate
from studio2.fase03.harness.runtime import execute_request
from studio2.fase03.harness.insight_adapter import FIXED

ROOT=Path(__file__).resolve().parents[3]
SCHEMA=ROOT/'studio2/fase03/schema_insight'
REAL_PROVIDER, REAL_SERVER = rp.Provider, rp.server_contract
REFERENCE=Path(os.environ.get('FOT_HARNESS_TEST_EVIDENCE','/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/studio2/fase03/evidence/output'))


class LedgerRevisions(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.t=Trial(self.tmp.name);self.l=self.t.ledger

    def test_R04_failed_and_zero_token_cannot_pass(self):
        self.t.bind()
        for i in range(8):
            r=self.t.reserve(i)
            if i==0:self.l.complete_request(r,status='FAILED')
            else:self.t.complete(r)
        with self.assertRaises(HarnessError):self.t.outcome('producer_conformity')
        self.t.zero('producer_conformity-0')
        with self.assertRaises(HarnessError):self.t.outcome('producer_conformity')

    def test_R04_public_normative_event_forbidden(self):
        for name in ('outcome:budget_probe','remediation_authorized','frozen_gate'):
            with self.subTest(name=name),self.assertRaises(HarnessError):self.l.record_event(name,artifact_sha256='a'*64,detail={'outcome':'PASS'})
        self.assertEqual(self.l.snapshot()['events'],[])

    def test_R04_closed_stage_cannot_reopen_retry(self):
        self.t.bind()
        for i in range(8):
            r=self.t.reserve(i)
            if i==0:self.t.zero(r);self.t.complete(self.t.retry(r,'retry'))
            else:self.t.complete(r)
        self.t.outcome('producer_conformity')
        with self.assertRaises(HarnessError):self.t.retry('producer_conformity-0','late')
        self.assertEqual(self.l.snapshot()['unresolved_intents'],0)

    def test_R04_outcome_atomic_with_real_concurrent_writer(self):
        self.t.bind()
        for i in range(8):self.t.complete(self.t.reserve(i))
        code="""import sys
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness.common import HarnessError
t=Trial(sys.argv[1])
try:t.retry('producer_conformity-0','late')
except HarnessError:sys.exit(17)
"""
        proc=subprocess.Popen([sys.executable,'-c',code,self.tmp.name],env=dict(os.environ,PYTHONPATH=str(ROOT)))
        self.t.outcome('producer_conformity')
        self.assertEqual(proc.wait(),17)
        self.assertEqual(self.l.snapshot()['unresolved_intents'],0)
        with patch.object(self.l,'record_event',side_effect=AssertionError('non-atomic event API')):
            # A separate admissible stage also closes through the internal transaction.
            self.t.finish('budget_probe',3)

    def test_R05_changed_alias_run_pilot_id_and_duplicate_original(self):
        self.t.bind();r=self.t.reserve(0)
        b=self.t.binding('producer_conformity');b['requests'][0]['model']='another-alias'
        with self.assertRaises(HarnessError):self.l.bind_stage('producer_conformity',b)
        with self.assertRaises(HarnessError):PilotLedger(self.l.path,pilot_id='renamed-pilot')
        with self.assertRaises(HarnessError):self.t.reserve(0,request_id='other-directory-id')
        self.t.zero(r);self.t.retry(r,'retry')
        with self.assertRaises(HarnessError):self.t.retry(r,'concurrent-retry')

    def test_R05_two_processes_reserve_one_original_once(self):
        self.t.bind();r=self.t.reserve(0);self.t.zero(r)
        code="""import sys
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness.common import HarnessError
t=Trial(sys.argv[1])
try:t.retry('producer_conformity-0',sys.argv[2])
except HarnessError:sys.exit(17)
"""
        procs=[subprocess.Popen([sys.executable,'-c',code,self.tmp.name,f'r{i}'],env=dict(os.environ,PYTHONPATH=str(ROOT))) for i in range(2)]
        self.assertEqual(sorted(p.wait() for p in procs),[0,17])
        self.assertEqual(self.l.snapshot()['transport_calls'],1)

    def test_R05_triplet_cannot_reuse_original_or_mix_budget(self):
        self.t.finish();self.t.bind('budget_probe',6)
        originals=[self.t.reserve(i,'budget_probe') for i in range(6)]
        for r in originals:self.t.zero(r)
        def values(ids):
            return [dict(request_id=f'retry-{i}',logical_id=self.l.request(r)['logical_id'],model='fixture-model',producer='fixture-producer',stage_run=self.l.request(r)['stage_run'],retry_of=r,condition=('A','B-LF','E-LF')[i]) for i,r in enumerate(ids)]
        for ids in ([originals[0]]*3,[originals[0],originals[1],originals[5]]):
            with self.assertRaises(HarnessError):self.l.reserve_probe_transport_triplet(values(ids))
        self.assertEqual(self.l.snapshot()['transport_calls'],0)

    def test_R06_timeout_and_missing_concrete_approval_cannot_remediate(self):
        self.t.bind()
        for i in range(8):
            r=self.t.reserve(i)
            if i==0:self.l.complete_request(r,status='FAILED')
            else:self.t.complete(r)
        self.t.outcome('producer_conformity','FAIL',diagnosis='structure')
        with self.assertRaises(HarnessError):self.t.remediation()
        with self.assertRaises(HarnessError):self.l.authorize_remediation(diff_sha256='a'*64,approval_sha256='b'*64,template_sha256='c'*64)

    def test_R06_same_case_cannot_replace_eight_and_non_template_contracts_immutable(self):
        self.t.finish(valid=False);self.t.remediation()
        r=self.t.reserve(0,'producer_remediation');self.t.complete(r)
        with self.assertRaises(HarnessError):self.t.reserve(0,'producer_remediation','second')
        b=self.l.binding('producer_remediation');b['inventory_sha256']='a'*64
        with self.assertRaises(HarnessError):self.l.bind_stage('producer_remediation',b)

    def test_R07_real_crashes_intent_raw_and_completed_restart(self):
        for point in ('intent','transport','raw','completed'):
            home=Path(self.tmp.name)/point;t=Trial(home);t.bind()
            code="""import os,sys
from studio2.fase03.harness.offline_fixtures import Trial
t=Trial(sys.argv[1]);r=t.reserve(0)
if sys.argv[2] in ('intent','transport'):os._exit(23)
t.ledger.save_raw(r,{'model':'fixture-model','system_fingerprint':None,'payload':'RAW SURVIVES'})
if sys.argv[2]=='raw':os._exit(23)
row=t.ledger.request(r)
import json
t.ledger.complete_request(r,status='COMPLETED',record={'request_id':r,'prompt_sha256':json.loads(row['identity_json'])['prompt_sha256'],'identity_valid':True})
os._exit(23)
"""
            result=subprocess.run([sys.executable,'-c',code,str(home),point],env=dict(os.environ,PYTHONPATH=str(ROOT)))
            self.assertEqual(result.returncode,23)
            t=Trial(home);self.assertEqual(t.ledger.snapshot()['requests_cumulative'],1)
            stored=t.ledger.response('producer_conformity-0')
            self.assertEqual(stored is not None,point in ('raw','completed'))
            if stored:self.assertEqual(stored['raw']['payload'],'RAW SURVIVES')
            calls=[]
            def transport():calls.append(1);raise AssertionError('resend forbidden')
            kwargs=dict(ledger=t.ledger,stage='producer_conformity',spec=t.ledger.binding('producer_conformity')['requests'][0],transport=transport,
                        evaluate=lambda raw:dict(returned_model=raw['model'],system_fingerprint=None),expected_identity=dict(returned_model='fixture-model',system_fingerprint=None),journal_path=home/'journal.jsonl',resume=True)
            if point in ('intent','transport'):
                with self.assertRaises(HarnessError):execute_request(**kwargs)
            else:execute_request(**kwargs)
            self.assertEqual(calls,[])

    def test_R07_reconciliation_requires_matching_evidence_preserves_counts(self):
        self.t.bind();r=self.t.reserve(0);self.l.complete_request(r,status='FAILED')
        self.t.zero(r);self.t.complete(self.t.retry(r,'retry'))
        self.assertEqual(self.l.snapshot()['requests_cumulative'],2)
        self.assertIn('reconciled:'+r,self.l.snapshot()['events'])
        with self.assertRaises(HarnessError):self.t.zero('retry')

    def test_R07_legacy_ledger_is_preserved_not_reset(self):
        path=Path(self.tmp.name)/'legacy.sqlite3'
        with closing(sqlite3.connect(path)) as c, c:c.execute('create table old_counter(n)');c.execute('insert into old_counter values(7)')
        before=path.read_bytes()
        with self.assertRaises(HarnessError):PilotLedger(path,pilot_id='legacy-pilot')
        self.assertEqual(path.read_bytes(),before)

    def test_R08_arbitrary_freeze_is_not_authenticated(self):
        self.t.finish();self.t.finish('budget_probe',3)
        frozen=self.l.event('frozen_gate')['frozen'];self.l.authenticate_frozen(frozen)
        frozen['generation']['max_tokens']=9999
        with self.assertRaises(HarnessError):self.l.authenticate_frozen(frozen)

    def test_reserve_15_waiver_and_maxima_152_160(self):
        self.t.bind();r=self.t.reserve(0);self.t.zero(r)
        for i in range(7):r=self.t.retry(r,f'r{i}');self.t.zero(r)
        with self.assertRaises(HarnessError):self.t.retry(r,'eighth')
        self.l.waive_remediation(approval_sha256='a'*64)
        for i in range(7,15):r=self.t.retry(r,f'r{i}');self.t.zero(r)
        with self.assertRaises(HarnessError):self.t.retry(r,'sixteenth')
        self.assertEqual(self.l.snapshot()['reserve_equation_value'],15)
        for alt in (False,True):
            t=Trial(Path(self.tmp.name)/str(alt));t.finish(valid=False);t.remediation()
            for i in range(8):
                r=t.reserve(i,'producer_remediation')
                if i==0:t.zero(r)
                else:t.complete(r)
            r='producer_remediation-0'
            for i in range(7):
                r=t.retry(r,f'r{i}')
                if i<6:t.zero(r)
                else:t.complete(r)
            t.outcome('producer_remediation')
            if alt:t.finish('alternate_conformity')
            t.finish('budget_probe',9);t.bind('stability_gate')
            for i in range(120):t.complete(t.reserve(i,'stability_gate'))
            self.assertEqual(t.ledger.snapshot()['requests_cumulative'],160 if alt else 152)
            with self.assertRaisesRegex(HarnessError,'planned request maximum'):t.reserve(0,'stability_gate','extra')

    def test_hard_200_on_explicit_imported_fixture(self):
        self.t.bind();self.t.reserve(0)
        with closing(sqlite3.connect(self.l.path)) as c, c:
            row=list(c.execute('select * from requests').fetchone())
            for i in range(1,200):
                r=list(row);r[0]=f'historical-{i}';r[1]=f'historical-{i}'
                c.execute('insert into requests values('+','.join('?'*18)+')',r)
        with self.assertRaisesRegex(HarnessError,'hard stop 200'):self.t.reserve(1)


class GateRevisions(unittest.TestCase):
    def rows(self):
        return [dict(p,request_id=f"{p['prompt_id']}-{r}",repetition=r,identity_valid=True,parse_valid_first_attempt=True,
                     parsed_output={'abstain':True,'predicted_label':None},finish_reason='stop') for p in sample() for r in (1,2,3)]

    def test_R10_repetition_condition_hash_uniqueness_and_distribution(self):
        self.assertTrue(evaluate_stability_gate(self.rows(),expected_prompts=sample())['t3_pass'])
        for change in ('repetition','condition','hash','request','sample'):
            rows=self.rows();expected=sample()
            if change=='repetition':rows[1]['repetition']=1
            if change=='condition':rows[0]['condition']='B-LF'
            if change=='hash':rows[0]['prompt_sha256']='a'*64
            if change=='request':rows[1]['request_id']=rows[0]['request_id']
            if change=='sample':
                expected[7]['condition']='B-LF'
                for r in rows:
                    if r['prompt_id']==expected[7]['prompt_id']:r['condition']='B-LF'
            with self.subTest(change=change),self.assertRaises(HarnessError):evaluate_stability_gate(rows,expected_prompts=expected)
        with self.assertRaises(HarnessError):evaluate_stability_gate(self.rows())


class RunnerRevisions(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.home=Path(self.tmp.name)
        self.stack=ExitStack();self.addCleanup(self.stack.close)
        self.stack.enter_context(patch('socket.socket',side_effect=AssertionError('NETWORK FORBIDDEN')))
        self.inventory=inputs.verified_pending_inventory();self.source=self.home/'inventory.json';self.source.write_text(json.dumps(self.inventory))
        self.ledger=PilotLedger(self.home/'pilot.sqlite3',pilot_id='runner-fixture')
        self.snapshot=self.home/'fixture-revision';self.snapshot.mkdir()
        (self.snapshot/'tokenizer.json').write_text('{}');(self.snapshot/'tokenizer_config.json').write_text(json.dumps({'chat_template':'FIXTURE TEMPLATE'}))
        self.tokenizer=dict(revision=self.snapshot.name,tokenizer_json_sha256=sha256_file(self.snapshot/'tokenizer.json'),tokenizer_config_sha256=sha256_file(self.snapshot/'tokenizer_config.json'),chat_template_sha256=sha256_text('FIXTURE TEMPLATE'))
        self.provider=self.home/'provider.json'
        self.provider_value=dict(name='fixture',base_url='https://offline.invalid/v1',model='fixture-model',temperature=0,seed=1,max_tokens=1024,thinking_token_budget=None,expected_max_model_len=100000,identity_sha256='a'*64,
                                 expected_response=dict(returned_model='fixture-model',system_fingerprint=None),tokenizer=self.tokenizer)
        self.provider.write_text(json.dumps(self.provider_value))
        approval=self.home/'order_approval.json';approval.write_text(json.dumps(dict(author='FIXTURE ONLY',decision='accepted',ordered_labels_sha256=digest(self.inventory['presentation']['ordered_labels']))))
        self.config=json.loads(rp.PREFLIGHT_CONFIG_PATH.read_text());self.config.update(study_model_decision='APPROVED',status='APPROVED_FOR_PHASE03_EXECUTION',tokenizer=self.tokenizer,
                            presentation_approval=dict(path=str(approval),sha256=sha256_file(approval)),approved_producer_config_sha256=[sha256_file(self.provider)],expected_response=dict(returned_model='fixture-model',system_fingerprint=None))
        self.config['candidate']['requested_model']='fixture-model';self.config['candidate']['base_url']='https://offline.invalid/v1';self.config['candidate']['expected_max_model_len']=100000
        self.config['pilot_ledger']=dict(path=str(self.ledger.path),pilot_id=self.ledger.pilot_id)
        self.config_path=self.home/'config.json'
        from studio2.fase03.harness.d9_offline_fixtures import install
        install(self)  # D9 metadata/tokenizer fixtures; original behavioral assertions preserved.
        self.approve_config()
        for module in (pp,rp,pg):self.stack.enter_context(patch.object(module,'PREFLIGHT_CONFIG_PATH',self.config_path))
        for module in (pp,pg):self.stack.enter_context(patch.object(module,'offline_token_counter',return_value=lambda s:len(s.split())))
        self.calls=[];self.fail_at=None;self.bad_at=None;self.identity_at=None;self.crash_at=None
        def create(**kwargs):
            self.calls.append(kwargs);n=len(self.calls)
            if n==self.fail_at:raise TimeoutError('FIXTURE timeout')
            if n==self.crash_at:raise KeyboardInterrupt('FIXTURE crash')
            fixed=kwargs['response_format']['json_schema']['schema']['properties']['insights']['prefixItems']
            pair=[]
            for schema in fixed:
                value={k:schema['properties'][k]['const'] for k in FIXED};value['observed_pattern']=value['variable_ids'][0]+' remains elevated.';pair.append(value)
            raw=dict(id=f'fixture-{n}',model='WRONG' if n==self.identity_at else kwargs['model'],system_fingerprint=None,
                     choices=[dict(message=dict(content='invalid' if n==self.bad_at else json.dumps({'insights':pair})),finish_reason='stop')],usage=dict(prompt_tokens=2,completion_tokens=3,total_tokens=5))
            return types.SimpleNamespace(model_dump=lambda **kw:raw)
        def factory(**kw):
            self.assertEqual(kw['max_retries'],0)
            return types.SimpleNamespace(chat=types.SimpleNamespace(completions=types.SimpleNamespace(create=create)))
        self.stack.enter_context(patch.dict(sys.modules,{'openai':types.SimpleNamespace(OpenAI=factory)}))
        self.consumer_calls=[];self.consumer_fail=None;self.consumer_identity=None
        owner=self
        class Stub:
            model='fixture-model'
            def __init__(self,config):self.requests=0
            def call(self,*,prompt,**kw):
                self.requests+=1;owner.consumer_calls.append(prompt['prompt_id']);n=len(owner.consumer_calls)
                if n==owner.consumer_fail:raise KeyboardInterrupt('FIXTURE consumer crash')
                return dict(id=f'consumer-{n}',model='WRONG' if n==owner.consumer_identity else 'fixture-model',system_fingerprint=None,
                            choices=[dict(message=dict(content=json.dumps(dict(predicted_label=None,abstain=True,used_insight_ids=[],reasoning_summary='Fixture.'))),finish_reason='stop')])
        self.stack.enter_context(patch.object(rp,'Provider',Stub));self.server= {'process':{'fingerprint_sha256':'b'*64}}
        self.server_mock=self.stack.enter_context(patch.object(rp,'server_contract',return_value=self.server))

    def approve_config(self):
        payload={k:v for k,v in self.config.items() if k!='execution_authorization'}
        path=self.home/'execution_approval.json';path.write_text(json.dumps(dict(author='FIXTURE ONLY',decision='accepted',configuration_sha256=digest(payload))))
        self.config['execution_authorization']=dict(path=str(path),sha256=sha256_file(path));self.config_path.write_text(json.dumps(self.config))

    def producer(self,**kwargs):
        stage=kwargs.pop('stage','producer_conformity')
        provider=self.alternate_provider if stage=='alternate_conformity' else self.provider
        return pp.run(source_inventory=self.source,results_dir=self.home/'results',provider_path=provider,snapshot=self.snapshot,schema_dir=kwargs.pop('schema_dir',SCHEMA),ledger=self.ledger,stage=stage,**kwargs)

    def inventory_args(self):
        return dict(evidence_root=REFERENCE,pseudolabel_path=ROOT/'studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json',assignment_path=ROOT/'studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json',derangement_path=ROOT/'studio2/fase03/pseudolabel/CONDITION_E_DERANGEMENTS.json',normal_handoff=ROOT/'studio2/fase03/baseline_numerica/NORMAL_DEV_HANDOFF.json',assembly_base_commit=self.inventory['assembly_base_commit'])

    def prepare(self, producer=True):
        if producer:self.producer()
        handoff=self.home/'results/validated_insight_library_fixture_producer_conformity.json'
        inv,manifest=inputs.build_inventory(**self.inventory_args(),insight_handoff=handoff,ledger=self.ledger,token_count=lambda s:len(s.split()),schema_dir=SCHEMA,presentation_approval=self.config['presentation_approval'])
        self.complete_inventory=self.home/'complete_inventory.json';self.complete_inventory.write_text(json.dumps(inv))
        self.manifest=self.home/'manifest.json';self.manifest.write_text(json.dumps(manifest))
        self.prepared=self.home/'prepared';self.results=self.home/'consumer_results'
        pg.prepare(self.manifest,self.snapshot,self.prepared,source_inventory_path=self.complete_inventory,insight_handoff=handoff,ledger=self.ledger)

    def test_R01_undecided_and_suspended_all_entries_zero_sends(self):
        self.config['study_model_decision']='UNDECIDED';self.approve_config()
        for f in (self.producer,lambda:rp.run_budget_stage(self.home,self.home,ledger=self.ledger),lambda:rp.run_stability_stage(self.home,self.home,ledger=self.ledger),lambda:rp.run_provisional_stress_budget_stage(self.home,self.home)):
            with self.assertRaises((HarnessError,RuntimeError)):f()
        self.assertEqual(self.calls,[]);self.assertEqual(self.consumer_calls,[]);self.server_mock.assert_not_called()
        with self.assertRaises(HarnessError):REAL_PROVIDER(self.config)
        with self.assertRaises(HarnessError):REAL_SERVER(self.config)
        self.config.update(study_model_decision='APPROVED',status='SUSPENDED');self.approve_config()
        with self.assertRaises(HarnessError):self.producer()

    def test_R01_CLI_with_transport_stub_rejects_historical_preflight(self):
        self.config['study_model_decision']='UNDECIDED';self.approve_config()
        for module,args in [(pp,['--source-inventory',str(self.source),'--provider-config',str(self.provider),'--model-snapshot',str(self.snapshot)]),(rp,['--stage','budget'])]:
            argv=['fixture','--execute','--acknowledge',module.ACK,'--ledger',str(self.ledger.path),'--pilot-id',self.ledger.pilot_id]+args
            with patch.object(sys,'argv',argv),self.assertRaises(HarnessError):module.main()
        self.assertEqual(self.calls,[]);self.assertEqual(self.consumer_calls,[])

    def test_R02_inventory_tamper_r4_and_tokenizer_zero_sends(self):
        bad=deepcopy(self.inventory);bad['producer_conformance_inputs']['local_examples']['agent_1'][0]['neutral_text']='UNVERIFIED OOD'
        self.source.write_text(json.dumps(bad))
        with self.assertRaises(HarnessError):self.producer()
        self.source.write_text(json.dumps(self.inventory))
        for name in ('validator.py','insight_v1.schema.json','SCHEMA_FREEZE.json','leakage_rules_v1.json'):
            dest=self.home/name.replace('.','_');shutil.copytree(SCHEMA,dest)
            with (dest/name).open('ab') as f:f.write(b'\n')
            with self.subTest(name=name),self.assertRaises(HarnessError):self.producer(schema_dir=dest)
        (self.snapshot/'tokenizer.json').write_text('tamper')
        with self.assertRaises(HarnessError):self.producer()
        self.assertEqual(self.calls,[]);self.assertEqual(self.ledger.snapshot()['requests_cumulative'],0)

    def test_R02_dependency_failure_is_pretransport_and_not_prompt_diagnosis(self):
        with patch.dict(sys.modules, {'jsonschema':None}),self.assertRaisesRegex(HarnessError,'dependency'):
            self.producer()
        self.assertEqual(self.calls,[])
        self.assertEqual(self.ledger.snapshot()['requests_cumulative'],0)

    def test_R02_frozen_037_and_evidence_json_tamper(self):
        for key in ('pseudolabel_path','assignment_path','derangement_path'):
            args=self.inventory_args();p=self.home/(key+'.json');p.write_bytes(args[key].read_bytes()+b'\n');args[key]=p
            with self.subTest(key=key),self.assertRaises(HarnessError):inputs.build_inventory(**args)
        dest=self.home/'evidence';shutil.copytree(REFERENCE,dest)
        import csv
        with (dest/'EVIDENCE_MANIFEST.csv').open() as stream:row=next(csv.DictReader(stream))
        with (dest/row['json_path']).open('ab') as f:f.write(b'\n')
        args=self.inventory_args();args['evidence_root']=dest
        with self.assertRaises(HarnessError):inputs.build_inventory(**args)

    def test_R02_handoff_cannot_self_certify_or_change_library(self):
        path=self.home/'fake.json';path.write_text(json.dumps(dict(validated=True,library=[{}]*16)))
        with self.assertRaises(HarnessError):inputs._insights(path)
        self.producer();path=self.home/'results/validated_insight_library_fixture_producer_conformity.json'
        value=json.loads(path.read_text());value['library'][0]['observed_pattern']='Forged narrative.';value['library_sha256']=digest(value['library']);path.write_text(json.dumps(value))
        with self.assertRaises(HarnessError):inputs._insights(path,ledger=self.ledger,token_count=lambda s:1,schema_dir=SCHEMA)

    def test_R03_real_pipeline_labels_preserved_and_pending_rejected(self):
        self.prepare();manifest=json.loads(self.manifest.read_text())
        canonical=json.loads((ROOT/'studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json').read_text())['label_space']
        self.assertEqual(manifest['label_space'],canonical)
        self.assertNotEqual(canonical,self.inventory['presentation']['ordered_labels'])
        inv=json.loads(self.complete_inventory.read_text());inv['presentation']['author_decision']='pending';self.complete_inventory.write_text(json.dumps(inv))
        with self.assertRaises(HarnessError):rp.load_prepared(self.prepared,ledger=self.ledger)
        with self.assertRaises(HarnessError):pg.prepare(self.manifest,self.snapshot,self.home/'other-prepared',source_inventory_path=self.complete_inventory,insight_handoff=self.home/'results/validated_insight_library_fixture_producer_conformity.json',ledger=self.ledger)
        with self.assertRaises(protocol.ContractError):protocol.build_pilot_sample(manifest,self.config,token_count=lambda s:1)
        self.assertEqual(self.consumer_calls,[])

    def test_R02_source_manifest_and_prompt_rehash_cannot_bypass(self):
        self.prepare();value=json.loads(self.manifest.read_text());value['label_space'].reverse();self.manifest.write_text(json.dumps(value))
        with self.assertRaises(RuntimeError):rp.load_prepared(self.prepared,ledger=self.ledger)
        plan=self.prepared/'pre_gate_plan.json';p=json.loads(plan.read_text());p['source_manifest_sha256']=sha256_file(self.manifest);plan.write_text(json.dumps(p))
        hashes=self.prepared/'pre_gate_hashes.json';h=json.loads(hashes.read_text());h['files'][str(self.manifest.resolve())]=sha256_file(self.manifest);h['files'][str(plan.resolve())]=sha256_file(plan);hashes.write_text(json.dumps(h))
        with self.assertRaises(HarnessError):rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger)
        self.assertEqual(self.consumer_calls,[])

    def test_R09_producer_identity_mismatch_preserves_raw_and_suspends(self):
        self.identity_at=1
        with self.assertRaises(HarnessError):self.producer()
        self.assertEqual(len(self.calls),1);self.assertEqual(self.ledger.snapshot()['durable_responses'],1)
        self.assertTrue(any(e.startswith('suspended:') for e in self.ledger.snapshot()['events']))
        self.assertIn('WRONG',(self.home/'results/producer_producer_conformity_journal.jsonl').read_text())

    def test_R07_producer_timeout_resume_no_resend_and_explicit_reconciliation(self):
        self.fail_at=2
        with self.assertRaises(HarnessError):self.producer()
        journal=self.home/'results/producer_producer_conformity_journal.jsonl'
        self.assertIn('fixture-1',journal.read_text());self.assertEqual(self.ledger.snapshot()['requests_cumulative'],2)
        with self.assertRaises(HarnessError):self.producer(resume=True)
        self.assertEqual(len(self.calls),2)
        r=self.ledger.leaf('producer_conformity','agent_2')['request_id']
        t=Trial(self.home/'reconcile-helper');t.ledger=self.ledger;t.zero(r)
        result=self.producer(resume=True,retry_requests=[r])
        self.assertEqual(result['status'],'PASS');self.assertEqual(self.ledger.snapshot()['requests_cumulative'],9)
        self.assertEqual(self.ledger.snapshot()['transport_calls'],1)

    def test_R06_real_runner_remediation_approved_bytes_and_old_handoff(self):
        self.bad_at=2;result=self.producer(diagnosis='structure');self.assertEqual(result['valid_first_attempts'],7)
        self.assertFalse(list((self.home/'results').glob('validated_insight_library*')))
        t=Trial(self.home/'remediation-helper');t.ledger=self.ledger;t.remediation(bind=False)
        template=t.home/'template.txt'
        # A second/changed template cannot reach transport even with a previous approval.
        before=len(self.calls)
        with self.assertRaises(HarnessError):self.producer(stage='producer_remediation')
        self.assertEqual(len(self.calls),before)
        result=self.producer(stage='producer_remediation',template_path=template)
        self.assertEqual(result['status'],'PASS')
        path=self.home/'results/validated_insight_library_fixture_producer_remediation.json'
        value=json.loads(path.read_text());value['stage']='producer_conformity';path.write_text(json.dumps(value))
        with self.assertRaises(HarnessError):inputs._insights(path,ledger=self.ledger,token_count=lambda s:1,schema_dir=SCHEMA)

    def test_R07_consumer_budget_crash_and_resume_preserve_raw(self):
        self.prepare();self.consumer_fail=2
        with self.assertRaises(KeyboardInterrupt):rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger)
        self.assertEqual(self.ledger.snapshot()['requests_by_stage']['budget_probe'],2)
        self.assertIn('consumer-1',(self.results/'budget_probe_journal.jsonl').read_text())
        with self.assertRaises(HarnessError):rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger,resume=True)
        self.assertEqual(len(self.consumer_calls),2)

    def test_R07_gate_crash_retains_raw_and_blocks_uncertain_resume(self):
        self.prepare();rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger);self.consumer_fail=5
        with self.assertRaises(KeyboardInterrupt):rp.run_stability_stage(self.prepared,self.results,ledger=self.ledger)
        self.assertEqual(self.ledger.snapshot()['requests_by_stage']['stability_gate'],2)
        self.assertIn('consumer-4',(self.results/'stability_journal.jsonl').read_text())
        with self.assertRaises(HarnessError):rp.run_stability_stage(self.prepared,self.results,ledger=self.ledger,resume=True)
        self.assertEqual(len(self.consumer_calls),5)

    def test_R08_frozen_budget_tamper_first_gate_zero_additional_calls(self):
        self.prepare();rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger)
        path=self.results/'frozen_gate_config.json';f=json.loads(path.read_text());f['generation']['max_tokens']=9999;path.write_text(json.dumps(f))
        with self.assertRaises(HarnessError):rp.run_stability_stage(self.prepared,self.results,ledger=self.ledger)
        self.assertEqual(len(self.consumer_calls),3)

    def test_R09_consumer_identity_change_during_gate_suspends(self):
        self.prepare();rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger);self.consumer_identity=5
        with self.assertRaises(HarnessError):rp.run_stability_stage(self.prepared,self.results,ledger=self.ledger)
        self.assertEqual(len(self.consumer_calls),5)
        self.assertEqual(self.ledger.snapshot()['durable_responses'],13)

    def test_ordinary_complete_producer_prepare_probe_gate_offline(self):
        self.prepare();rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger)
        result=rp.run_stability_stage(self.prepared,self.results,ledger=self.ledger)
        self.assertEqual(len(self.consumer_calls),123);self.assertFalse(result['go_final'])
        self.assertEqual(result['status'],'PASS_R1_PENDING_T5_AND_OTHER_PREREQUISITES')
        self.assertEqual(self.ledger.snapshot()['requests_cumulative'],131)

    def test_R01_changed_ledger_directory_cannot_reset_pilot(self):
        replacement=PilotLedger(self.home/'other-directory/ledger.sqlite3',pilot_id=self.ledger.pilot_id)
        original=self.ledger;self.ledger=replacement
        with self.assertRaises(HarnessError):self.producer()
        self.assertEqual(len(self.calls),0);self.ledger=original

    def test_R07_cli_successful_producer_and_budget_use_shared_ledger(self):
        argv=['fixture','--execute','--acknowledge',pp.ACK,'--source-inventory',str(self.source),'--provider-config',str(self.provider),
              '--model-snapshot',str(self.snapshot),'--results-dir',str(self.home/'results'),'--ledger',str(self.ledger.path),'--pilot-id',self.ledger.pilot_id]
        with patch.object(sys,'argv',argv),redirect_stdout(io.StringIO()):self.assertEqual(pp.main(),0)
        self.assertEqual(len(self.calls),8)
        self.prepare(producer=False)
        argv=['fixture','--execute','--acknowledge',rp.ACK,'--stage','budget','--prepared-dir',str(self.prepared),'--results-dir',str(self.results),
              '--ledger',str(self.ledger.path),'--pilot-id',self.ledger.pilot_id]
        with patch.object(sys,'argv',argv),redirect_stdout(io.StringIO()):self.assertEqual(rp.main(),0)
        self.assertEqual(self.ledger.snapshot()['requests_cumulative'],11)

    def test_R07_resume_saved_raw_and_closed_artifact_without_new_sends(self):
        self.prepare()
        from studio2.fase03.harness import runtime
        original=runtime.export_journal
        def crash(ledger,stage,path):
            original(ledger,stage,path)
            if stage=='budget_probe':raise KeyboardInterrupt('after durable raw before evaluation')
        with patch.object(runtime,'export_journal',side_effect=crash),self.assertRaises(KeyboardInterrupt):rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger)
        self.assertEqual(len(self.consumer_calls),1)
        frozen=rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger,resume=True)
        self.assertEqual(len(self.consumer_calls),3)
        path=self.results/'frozen_gate_config.json';path.unlink()
        self.assertEqual(rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger,resume=True),frozen)
        self.assertEqual(len(self.consumer_calls),3);self.assertTrue(path.is_file())

    def test_R07_probe_explicit_zero_token_triplet_retry(self):
        self.prepare()
        stub=rp.Provider
        class Fail(stub):
            def call(self, **kwargs):raise TimeoutError('FIXTURE zero-token transport pending proof')
        with patch.object(rp,'Provider',Fail),self.assertRaises(RuntimeError):rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger)
        self.assertEqual(self.ledger.snapshot()['requests_by_stage']['budget_probe'],3)
        ids=[];t=Trial(self.home/'reconcile-triplet');t.ledger=self.ledger
        for spec in self.ledger.binding('budget_probe')['requests'][:3]:
            request=self.ledger.leaf('budget_probe',spec['logical_id'])['request_id'];t.zero(request);ids.append(request)
        frozen=rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger,resume=True,retry_requests=ids)
        self.assertEqual(frozen['status'],'FROZEN_FOR_STABILITY_GATE')
        self.assertEqual(len(self.consumer_calls),3)
        self.assertEqual(self.ledger.snapshot()['transport_calls'],3)

    def test_R07_producer_and_consumer_real_process_crashes(self):
        for stage in ('producer','budget','gate'):
            locator=self.home/(stage+'.path')
            code="""import os,sys
from pathlib import Path
from studio2.fase03.harness.test_revisions import RunnerRevisions,pp,rp
from unittest.mock import patch
t=RunnerRevisions();t.setUp();Path(sys.argv[2]).write_text(str(t.home))
stage=sys.argv[1]
try:
    if stage=='producer':
        t.crash_at=2;t.producer()
    else:
        t.prepare()
        if stage=='budget':t.consumer_fail=2;rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        else:
            rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
            t.consumer_fail=5;rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
except KeyboardInterrupt:os._exit(23)
os._exit(31)
"""
            result=subprocess.run([sys.executable,'-c',code,stage,str(locator)],env=dict(os.environ,PYTHONPATH=str(ROOT),PYTHONDONTWRITEBYTECODE='1'))
            self.assertEqual(result.returncode,23)
            home=Path(locator.read_text());self.addCleanup(shutil.rmtree,home)
            ledger=PilotLedger(home/'pilot.sqlite3',pilot_id='runner-fixture')
            actual={'producer':'producer_conformity','budget':'budget_probe','gate':'stability_gate'}[stage]
            self.assertEqual(ledger.snapshot()['requests_by_stage'][actual],2)
            self.assertEqual(ledger.snapshot()['unresolved_intents'],1)
            self.assertEqual(len(ledger.stage_records(actual)),1)
            self.assertEqual(ledger.stage_records(actual)[0]['identity_valid'],True)



if __name__=='__main__':unittest.main()
