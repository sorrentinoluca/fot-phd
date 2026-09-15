"""Independent offline contract probes; expected behavior asserted, defects fail.

All provider objects are in-memory stubs. Network is disabled at socket level.
Fake token counts test control flow only, never scientific capacity or inference.
Only evidence/fixtures is writable. No candidate source is modified.
"""
import copy, json, os, pathlib, shutil, socket, sqlite3, subprocess, sys, types, unittest
from unittest.mock import patch

OUT=pathlib.Path(__file__).resolve().parent
ROOT=OUT.parent/'candidate'
sys.path.insert(0,str(ROOT))
from studio2.fase03.harness.common import HarnessError, sha256_file, canonical_json, sha256_text
from studio2.fase03.harness.ledger import PilotLedger
from studio2.fase03.harness.gate_rules import evaluate_stability_gate
from studio2.fase03.harness.insight_adapter import load_validator, validate_produced_pair, FIXED
from studio2.fase03.harness import inputs, render, ordering, guards, canary, sampling, logging_v1
from studio2.fase03 import producer_probe as pp, run_pilot as rp, prepare_gate as pg

H='a'*64
INVENTORY=json.loads((ROOT/'studio2/fase03/harness/PILOT_INPUT_SOURCES.pending.json').read_text())
CONFIG=json.loads(rp.PREFLIGHT_CONFIG_PATH.read_text())
SCHEMA=ROOT/'studio2/fase03/schema_insight'
OBS={}

def rows():
    values=[]
    for i in range(40):
        condition='A' if i<8 else ('B-LF' if i<24 else 'E-LF')
        for rep in range(1,4):
            abstain=i in {0,8,24}
            values.append(dict(prompt_id=f'p{i}',condition=condition,repetition=rep,
                parse_valid_first_attempt=True,parsed_output={'abstain':abstain,'predicted_label':None if abstain else 'S2-CLS-3ZGWQ'},finish_reason='stop',truncated=False))
    return values

class Base(unittest.TestCase):
    def setUp(self):
        self.home=OUT/'fixtures'/self._testMethodName
        if self.home.exists(): shutil.rmtree(self.home)
        self.home.mkdir(parents=True)
        self.ledger=PilotLedger(self.home/'pilot.sqlite3',pilot_id='independent-pilot')
        self.socket_guard=patch('socket.socket',side_effect=AssertionError('NETWORK FORBIDDEN'))
        self.socket_guard.start();self.addCleanup(self.socket_guard.stop)
    def observe(self,**value):OBS[self._testMethodName]=value
    def reserve(self,i,stage='producer_conformity',run='run1',ledger=None):
        (ledger or self.ledger).reserve_request(request_id=f'{stage}-{i}',logical_id=f'{stage}-{i}',model='fixture-model',producer='fixture-producer',stage=stage,stage_run=run)
        return f'{stage}-{i}'
    def complete(self,r,status='COMPLETED'):
        self.ledger.complete_request(r,status=status,proof_sha256=H if status=='ZERO_TOKEN_PROVEN' else None,total_tokens=0 if status=='ZERO_TOKEN_PROVEN' else None)
    def conformity(self,outcome='PASS',status='COMPLETED'):
        for i in range(8):self.complete(self.reserve(i),status)
        self.ledger.record_stage_outcome('producer_conformity',outcome=outcome,artifact_sha256=H)
    def probe(self):
        self.conformity()
        for i in range(3): self.complete(self.reserve(i,'budget_probe'))
        self.ledger.record_stage_outcome('budget_probe',outcome='PASS',artifact_sha256=H)
    def retry(self,i,original,stage='producer_conformity'):
        self.ledger.reserve_transport_retry(request_id=f'retry-{i}',logical_id=f'retry-{i}',model='fixture-model',producer='fixture-producer',stage=stage,stage_run='retry-run',retry_of=original)
        return f'retry-{i}'

class LedgerProbes(Base):
    def test_01_crash_intent_survives_real_process_exit(self):
        code="""import os,sys
from pathlib import Path
from studio2.fase03.harness.ledger import PilotLedger
l=PilotLedger(Path(sys.argv[1]),pilot_id='independent-pilot')
l.reserve_request(request_id='crash',logical_id='crash',model='m',producer='p',stage='producer_conformity',stage_run='run1')
os._exit(23)
"""
        env=dict(os.environ,PYTHONPATH=str(ROOT),PYTHONDONTWRITEBYTECODE='1')
        p=subprocess.run([sys.executable,'-c',code,str(self.ledger.path)],cwd=self.home,env=env)
        snap=PilotLedger(self.ledger.path,pilot_id='independent-pilot').snapshot()
        self.observe(exit=p.returncode,snapshot=snap)
        self.assertEqual((p.returncode,snap['requests_cumulative'],snap['unresolved_intents']),(23,1,1))
        with self.assertRaises(HarnessError):self.ledger.record_stage_outcome('producer_conformity',outcome='PASS',artifact_sha256=H)

    def test_02_two_processes_same_logical_request(self):
        code="""import sys,time
from pathlib import Path
from studio2.fase03.harness.ledger import PilotLedger
from studio2.fase03.harness.common import HarnessError
l=PilotLedger(Path(sys.argv[1]),pilot_id='independent-pilot')
try:l.reserve_request(request_id=sys.argv[2],logical_id='same',model='m',producer='p',stage='producer_conformity',stage_run='same')
except HarnessError:sys.exit(17)
"""
        env=dict(os.environ,PYTHONPATH=str(ROOT),PYTHONDONTWRITEBYTECODE='1')
        procs=[subprocess.Popen([sys.executable,'-c',code,str(self.ledger.path),str(i)],cwd=self.home,env=env) for i in range(2)]
        exits=sorted(p.wait() for p in procs);self.observe(exits=exits,snapshot=self.ledger.snapshot())
        self.assertEqual(exits,[0,17]);self.assertEqual(self.ledger.snapshot()['requests_cumulative'],1)

    def test_03_restart_changed_stage_run_cannot_duplicate_logical_request(self):
        self.reserve(0)
        reopened=PilotLedger(self.ledger.path,pilot_id='independent-pilot')
        with self.assertRaises(HarnessError):
            reopened.reserve_request(request_id='new-id',logical_id='producer_conformity-0',model='new-alias',producer='new-producer',stage='producer_conformity',stage_run='new-run')

    def test_04_failed_transport_cannot_be_promoted_to_pass(self):
        for i in range(8):self.complete(self.reserve(i),'FAILED' if i==0 else 'COMPLETED')
        with self.assertRaises(HarnessError): self.ledger.record_stage_outcome('producer_conformity',outcome='PASS',artifact_sha256=H)

    def test_05_zero_token_original_without_successful_retry_cannot_pass(self):
        for i in range(8):self.complete(self.reserve(i),'ZERO_TOKEN_PROVEN' if i==0 else 'COMPLETED')
        with self.assertRaises(HarnessError):self.ledger.record_stage_outcome('producer_conformity',outcome='PASS',artifact_sha256=H)

    def test_06_closed_stage_cannot_acquire_new_retry(self):
        for i in range(8):self.complete(self.reserve(i),'ZERO_TOKEN_PROVEN' if i==0 else 'COMPLETED')
        r=self.retry(0,'producer_conformity-0');self.complete(r)
        self.ledger.record_stage_outcome('producer_conformity',outcome='PASS',artifact_sha256=H)
        with self.assertRaises(HarnessError):self.retry(1,'producer_conformity-0')

    def test_07_pending_late_retry_blocks_next_stage_after_restart(self):
        for i in range(8):self.complete(self.reserve(i),'ZERO_TOKEN_PROVEN' if i==0 else 'COMPLETED')
        self.complete(self.retry(0,'producer_conformity-0'))
        self.ledger.record_stage_outcome('producer_conformity',outcome='PASS',artifact_sha256=H)
        self.retry(1,'producer_conformity-0')
        self.ledger=PilotLedger(self.ledger.path,pilot_id='independent-pilot')
        self.observe(before=self.ledger.snapshot())
        with self.assertRaises(HarnessError):self.reserve(0,'budget_probe')

    def test_08_public_event_api_cannot_forge_gate_prerequisite(self):
        self.ledger.record_event('outcome:budget_probe',artifact_sha256=H,detail={'outcome':'PASS'})
        with self.assertRaises(HarnessError):self.reserve(0,'stability_gate')

    def test_09_remediation_cannot_replace_eight_cases_by_one_case(self):
        self.conformity('FAIL');self.ledger.authorize_remediation(diff_sha256=H,approval_sha256=H,template_sha256=H)
        for i in range(8):
            r=f'rem-{i}';self.ledger.reserve_remediation_request(request_id=r,logical_id='same-agent-same-case',model='m',producer='p',stage_run=f'rem-run-{i}');self.complete(r)
        with self.assertRaises(HarnessError):self.ledger.record_stage_outcome('producer_remediation',outcome='PASS',artifact_sha256=H)

    def test_10_unknown_timeout_cannot_authorize_prompt_remediation(self):
        for i in range(8):self.complete(self.reserve(i),'FAILED' if i==0 else 'COMPLETED')
        self.ledger.record_stage_outcome('producer_conformity',outcome='FAIL',artifact_sha256=H)
        with self.assertRaises(HarnessError):self.ledger.authorize_remediation(diff_sha256=H,approval_sha256=H,template_sha256=H)

    def test_11_same_original_cannot_fund_concurrent_retries(self):
        self.complete(self.reserve(0),'ZERO_TOKEN_PROVEN');self.retry(0,'producer_conformity-0')
        with self.assertRaises(HarnessError):self.retry(1,'producer_conformity-0')

    def test_12_probe_triplet_cannot_reuse_one_original_three_times(self):
        self.conformity();self.complete(self.reserve(0,'budget_probe'),'ZERO_TOKEN_PROVEN')
        values=[dict(request_id=f't{i}',logical_id=f't{i}',model='m',producer='p',stage_run='p',retry_of='budget_probe-0',condition=c) for i,c in enumerate(['A','B-LF','E-LF'])]
        with self.assertRaises(HarnessError):self.ledger.reserve_probe_transport_triplet(values)

    def test_13_probe_triplet_rollback_at_quota_boundary(self):
        self.conformity()
        for i in range(3):self.complete(self.reserve(i,'budget_probe'),'ZERO_TOKEN_PROVEN')
        def values(n):return [dict(request_id=f't{n}-{i}',logical_id=f't{n}-{i}',model='m',producer='p',stage_run='p',retry_of=f'budget_probe-{i}',condition=c) for i,c in enumerate(['A','B-LF','E-LF'])]
        for n in range(2):self.ledger.reserve_probe_transport_triplet(values(n))
        before=self.ledger.snapshot()
        with self.assertRaises(HarnessError):self.ledger.reserve_probe_transport_triplet(values(2))
        self.assertEqual(self.ledger.snapshot(),before);self.assertEqual(before['transport_calls'],6)

    def test_14_waiver_boundary_15_and_no_alternate_quota_theft(self):
        self.complete(self.reserve(0),'ZERO_TOKEN_PROVEN');original='producer_conformity-0'
        for i in range(7):original=self.retry(i,original);self.complete(original,'ZERO_TOKEN_PROVEN')
        before=self.ledger.snapshot()
        with self.assertRaises(HarnessError):self.retry(7,original)
        self.assertEqual(self.ledger.snapshot(),before)
        self.ledger.waive_remediation(approval_sha256=H)
        for i in range(7,15):original=self.retry(i,original);self.complete(original,'ZERO_TOKEN_PROVEN')
        with self.assertRaises(HarnessError):self.retry(15,original)
        with self.assertRaises(HarnessError):self.retry(16,original,stage='alternate_conformity')
        self.assertEqual(self.ledger.snapshot()['transport_calls'],15)

    def test_15_gate_create_once_no_retry_and_no_return_to_probe(self):
        self.probe();self.complete(self.reserve(0,'stability_gate'),'ZERO_TOKEN_PROVEN')
        with self.assertRaises(HarnessError):self.reserve(1,'stability_gate',run='other')
        with self.assertRaises(HarnessError):self.retry(0,'stability_gate-0',stage='stability_gate')
        with self.assertRaises(HarnessError):self.reserve(3,'budget_probe')
        with self.assertRaises(HarnessError):self.ledger.authorize_remediation(diff_sha256=H,approval_sha256=H,template_sha256=H)

    def test_16_planned_maxima_152_160_with_valid_quota_chain(self):
        snapshots=[]
        for alternate in [False,True]:
            self.ledger=PilotLedger(self.home/f'max-{alternate}.sqlite3',pilot_id='independent-pilot')
            self.conformity('FAIL');self.ledger.authorize_remediation(diff_sha256=H,approval_sha256=H,template_sha256=H)
            for i in range(8):
                r=f'm{i}';self.ledger.reserve_remediation_request(request_id=r,logical_id=f'agent_{i+1}',model='m',producer='p',stage_run='rem');self.complete(r,'ZERO_TOKEN_PROVEN' if i==0 else 'COMPLETED')
            original='m0'
            for i in range(7):original=self.retry(i,original,'producer_remediation');self.complete(original,'ZERO_TOKEN_PROVEN' if i<6 else 'COMPLETED')
            self.ledger.record_stage_outcome('producer_remediation',outcome='PASS',artifact_sha256=H)
            if alternate:
                for i in range(8):self.complete(self.reserve(i,'alternate_conformity'))
                self.ledger.record_stage_outcome('alternate_conformity',outcome='PASS',artifact_sha256=H)
            for i in range(9):self.complete(self.reserve(i,'budget_probe'))
            self.ledger.record_stage_outcome('budget_probe',outcome='PASS',artifact_sha256=H)
            for i in range(120):self.complete(self.reserve(i,'stability_gate'))
            snap=self.ledger.snapshot();snapshots.append(snap)
            self.assertEqual(snap['requests_cumulative'],160 if alternate else 152)
            self.assertEqual(snap['reserve_equation_value'],15)
            with self.assertRaisesRegex(HarnessError,'planned request maximum'):self.reserve(120,'stability_gate')
        self.observe(snapshots=snapshots)

    def test_17_hard_200_separate_for_imported_historical_fixture(self):
        self.reserve(0)
        with sqlite3.connect(self.ledger.path) as c:
            row=c.execute('select * from requests').fetchone()
            for i in range(1,200):
                value=list(row);value[1]=f'historical-{i}';value[2]=f'historical-{i}'
                c.execute('insert into requests values ('+','.join('?'*18)+')',value)
        with self.assertRaisesRegex(HarnessError,'hard stop 200'):self.reserve(201)
        self.assertEqual(self.ledger.snapshot()['requests_cumulative'],200)

    def test_18_outcome_validation_and_write_are_atomic(self):
        for i in range(8):self.complete(self.reserve(i),'ZERO_TOKEN_PROVEN' if i==0 else 'COMPLETED')
        self.complete(self.retry(0,'producer_conformity-0'))
        original=self.ledger.record_event
        def interleave(*args,**kwargs):
            self.retry(1,'producer_conformity-0')
            return original(*args,**kwargs)
        with patch.object(self.ledger,'record_event',side_effect=interleave):
            with self.assertRaises(HarnessError):self.ledger.record_stage_outcome('producer_conformity',outcome='PASS',artifact_sha256=H)

class GateProbes(Base):
    def test_20_thresholds_and_missing_abstention(self):
        v=rows()
        for i in [9,12,15,18,21,27]:v[i].update(parse_valid_first_attempt=False,parsed_output=None)
        self.assertTrue(evaluate_stability_gate(v)['t3_pass'])
        v[30].update(parse_valid_first_attempt=False,parsed_output=None)
        self.assertFalse(evaluate_stability_gate(v)['t3_pass'])
        v=rows()
        for x in v:
            if x['condition']=='E-LF':x['parsed_output']={'abstain':False,'predicted_label':'S2-CLS-3ZGWQ'}
        self.assertFalse(evaluate_stability_gate(v)['t3_pass'])

    def test_21_forensic_vs_semantic_truncation_all_invalid(self):
        v=rows();v[0].update(raw_output='different',raw_output_sha256=H,finish_reason='other')
        v[0]['parsed_output']['explanation']='different JSON field'
        self.assertEqual(evaluate_stability_gate(v)['divergent_prompt_count'],0)
        v[0]['finish_reason']='length';self.assertFalse(evaluate_stability_gate(v)['t4_pass'])
        v=rows();v[9].update(parse_valid_first_attempt=False,parsed_output=None)
        self.assertEqual(evaluate_stability_gate(v)['status'],'R3_REQUIRED_PENDING_FEASIBILITY')
        v[10].update(parse_valid_first_attempt=False,parsed_output=None);v[11].update(parse_valid_first_attempt=False,parsed_output=None)
        self.assertFalse(evaluate_stability_gate(v)['t6_evaluable']);self.assertFalse(evaluate_stability_gate(v)['go_final'])

    def test_22_duplicate_repetitions_are_not_three_first_attempts(self):
        v=rows()
        for row in v:row['repetition']=1
        with self.assertRaises(HarnessError):evaluate_stability_gate(v)

    def test_23_triplet_cannot_mix_conditions(self):
        v=rows();v[0]['condition']='B-LF'
        with self.assertRaises(HarnessError):evaluate_stability_gate(v)

    def test_24_gate_condition_sample_must_match_8_16_16(self):
        v=rows()
        for row in v:
            if row['prompt_id']=='p7':row['condition']='B-LF'
        with self.assertRaises(HarnessError):evaluate_stability_gate(v)

class InputProbes(Base):
    def inventory_args(self):
        return dict(evidence_root=(OUT/'reference/studio2/fase03/evidence/output'),pseudolabel_path=ROOT/'studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json',assignment_path=ROOT/'studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json',derangement_path=ROOT/'studio2/fase03/pseudolabel/CONDITION_E_DERANGEMENTS.json',normal_handoff=ROOT/'studio2/fase03/baseline_numerica/NORMAL_DEV_HANDOFF.json',assembly_base_commit='a00605862f627710347bd63c49f79a6d0a00135f')
    def test_30_all_four_r4_byte_tamper_rejected(self):
        for name in ['validator.py','insight_v1.schema.json','leakage_rules_v1.json','SCHEMA_FREEZE.json']:
            target=self.home/name.replace('.','_');target.mkdir()
            for file in ['validator.py','insight_v1.schema.json','leakage_rules_v1.json','SCHEMA_FREEZE.json']:shutil.copyfile(SCHEMA/file,target/file)
            with (target/name).open('ab') as f:f.write(b'\n')
            with self.assertRaises(HarnessError):load_validator(target)

    def test_31_r4_pair_ids_fields_caps_leakage(self):
        fixed=[x for x in INVENTORY['fixed_insight_contracts'] if x['source_agent']=='agent_1']
        pair=[{**{k:x[k] for k in FIXED},'observed_pattern':x['variable_ids'][0]+' remains elevated.'} for x in fixed]
        def valid(p):return validate_produced_pair(p,inventory=INVENTORY,agent_id='agent_1',token_count=lambda s:len(s.split()),schema_dir=SCHEMA)
        self.assertEqual(len(valid(pair)),2)
        for field,value in [('insight_id','S2-INS-999'),('evidence_scope','Different windows.'),('observed_pattern','x'*801),('observed_pattern',fixed[0]['variable_ids'][0]+' fault 1')]:
            changed=copy.deepcopy(pair);changed[0][field]=value
            with self.assertRaises(Exception):valid(changed)

    def test_32_producer_inventory_cannot_accept_changed_source_text(self):
        inv=copy.deepcopy(INVENTORY);inv['producer_conformance_inputs']['local_examples']['agent_1'][0]['neutral_text']='UNTRUSTED TEST OR OOD BYTES'
        with self.assertRaises(HarnessError):pp._conformance_inputs(inv)

    def test_33_insight_handoff_self_declared_valid_is_insufficient(self):
        value=dict(schema_commit=inputs.SCHEMA_TARGET_COMMIT,schema_manifest_sha256=inputs.SCHEMA_MANIFEST_SHA256,library=[{}]*16,validated=True)
        value['library_sha256']=sha256_text(canonical_json(value['library']))
        p=self.home/'invalid_handoff.json';p.write_text(json.dumps(value))
        with self.assertRaises(HarnessError):inputs._insights(p)

    def test_34_renderer_refuses_pending_label_order(self):
        inv=copy.deepcopy(INVENTORY);inv['status']='COMPLETE_READY_TO_FREEZE'
        with self.assertRaisesRegex(HarnessError,'accepted'):render.build_real_pilot_sample({},CONFIG,token_count=lambda s:1,schema_dir=SCHEMA,source_inventory=inv)
        expected=INVENTORY['presentation']['ordered_labels']
        self.assertEqual(ordering.presentation_order(expected),expected)
        for labels in [expected[:-1],expected[1:]+expected[:1],expected[:-2]+[expected[0],'Normal']]:
            with self.assertRaises(HarnessError):ordering.presentation_order(labels)

    def test_35_builder_preserves_canonical_label_space(self):
        handoff=self.home/'handoff.json'
        library=[{**{k:x[k] for k in FIXED},'observed_pattern':x['variable_ids'][0]+' remains elevated.'} for x in INVENTORY['fixed_insight_contracts']]
        handoff.write_text(json.dumps(dict(schema_commit=inputs.SCHEMA_TARGET_COMMIT,schema_manifest_sha256=inputs.SCHEMA_MANIFEST_SHA256,library=library,library_sha256=sha256_text(canonical_json(library)),validated=True)))
        _,executable=inputs.build_inventory(evidence_root=(OUT/'reference/studio2/fase03/evidence/output'),pseudolabel_path=ROOT/'studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json',assignment_path=ROOT/'studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json',derangement_path=ROOT/'studio2/fase03/pseudolabel/CONDITION_E_DERANGEMENTS.json',normal_handoff=ROOT/'studio2/fase03/baseline_numerica/NORMAL_DEV_HANDOFF.json',insight_handoff=handoff,assembly_base_commit='a00605862f627710347bd63c49f79a6d0a00135f')
        canonical=json.loads((ROOT/'studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json').read_text())['label_space']
        self.observe(canonical=canonical,executable_labels=executable['label_space'],executable_status=executable['status'])
        self.assertEqual(executable['label_space'],canonical)

    def test_36_endpoint_and_tokenizer_guards_reject_tampering(self):
        expected={k:'fixture' for k in ['returned_model_root','returned_model_revision','vllm_version','command_sha256','environment_sha256','fingerprint_sha256','max_model_len']}
        for k in expected:
            changed=dict(expected);changed[k]='changed'
            with self.assertRaises(HarnessError):guards.verify_endpoint(changed,expected)

    def test_37_frozen_pseudolabel_assignment_derangement_bytes_are_enforced(self):
        for key in ['pseudolabel_path','assignment_path','derangement_path']:
            args=self.inventory_args();p=self.home/(key+'.json');p.write_bytes(args[key].read_bytes()+b'\n');args[key]=p
            with self.subTest(key=key):
                with self.assertRaises(HarnessError):inputs.build_inventory(**args)

    def test_38_evidence_json_hash_is_verified_before_contract_extraction(self):
        args=self.inventory_args();dest=self.home/'evidence-copy';shutil.copytree(args['evidence_root'],dest);args['evidence_root']=dest
        # Change one JSON byte without touching the pinned text or CSV manifests.
        import csv
        manifest=list(csv.DictReader((dest/'EVIDENCE_MANIFEST.csv').open()))
        for row in manifest:
            p=dest/row['json_path']
            with p.open('ab') as f:f.write(b'\n')
        with self.assertRaises(HarnessError):inputs.build_inventory(**args)

    def test_39_pending_label_order_cannot_reach_real_prepare_entrypoint(self):
        lib=[{**{k:x[k] for k in FIXED},'observed_pattern':x['variable_ids'][0]+' remains elevated.'} for x in INVENTORY['fixed_insight_contracts']]
        h=self.home/'handoff.json';h.write_text(json.dumps(dict(schema_commit=inputs.SCHEMA_TARGET_COMMIT,schema_manifest_sha256=inputs.SCHEMA_MANIFEST_SHA256,library=lib,library_sha256=sha256_text(canonical_json(lib)),validated=True)))
        args=self.inventory_args();args['insight_handoff']=h
        inventory,executable=inputs.build_inventory(**args)
        manifest=self.home/'manifest.json';manifest.write_text(json.dumps(executable))
        tok=self.home/'tokenizer';tok.mkdir();(tok/'tokenizer.json').write_text('{}');(tok/'tokenizer_config.json').write_text('{}')
        # Redirect only artifact-relative path bookkeeping to the fixture root.
        config=self.home/'config.json';shutil.copyfile(pg.PREFLIGHT_CONFIG_PATH,config)
        with patch.object(pg,'ROOT',self.home),patch.object(pg,'PREFLIGHT_CONFIG_PATH',config),patch.object(pg,'offline_token_counter',return_value=lambda s:len(s.split())):
            result=pg.prepare(manifest,tok,self.home/'prepared')
        self.observe(author_decision=inventory['presentation']['author_decision'],prepare_status=result['status'],prompt_count=result['prompt_count'])
        self.assertNotEqual(result['status'],'READY_FOR_PRE_GATE_GENERATION_PROBE')

class RunnerProbes(Base):
    def setup_producer(self, mutate_inventory=None, schema_dir=None, fail_at=None, malformed_at=None):
        inv=copy.deepcopy(INVENTORY)
        if mutate_inventory:mutate_inventory(inv)
        source=self.home/'inventory.json';source.write_text(json.dumps(inv))
        provider=self.home/'provider.json';provider.write_text(json.dumps(dict(name='fixture',base_url='https://offline.invalid/v1',model='approved-fixture',temperature=0,seed=1,max_tokens=1024,thinking_token_budget=None,expected_max_model_len=100000,identity_sha256=H)))
        self.calls=[]
        def create(**kwargs):
            self.calls.append(kwargs)
            n=len(self.calls)
            self.assertEqual(self.ledger.snapshot()['requests_cumulative'],n + (8 if self.producer_stage=='producer_remediation' else 0))
            if n==fail_at:raise TimeoutError('OFFLINE injected transport failure')
            fixed=kwargs['response_format']['json_schema']['schema']['properties']['insights']['prefixItems']
            pair=[]
            for schema in fixed:
                item={k:schema['properties'][k]['const'] for k in FIXED};item['observed_pattern']=item['variable_ids'][0]+' remains elevated.';pair.append(item)
            content='not JSON' if n==malformed_at else json.dumps({'insights':pair})
            raw={'id':f'fixture-{n}','model':'UNEXPECTED-MODEL','choices':[{'message':{'content':content},'finish_reason':'stop'}]}
            response=types.SimpleNamespace(id=raw['id'],model=raw['model'],choices=[types.SimpleNamespace(message=types.SimpleNamespace(content=content),finish_reason='stop')],usage=None,system_fingerprint='UNEXPECTED-FINGERPRINT',model_dump=lambda **kw:raw)
            return response
        def factory(**kw):
            self.assertEqual(kw['max_retries'],0)
            return types.SimpleNamespace(chat=types.SimpleNamespace(completions=types.SimpleNamespace(create=create)))
        self.fake=types.SimpleNamespace(OpenAI=factory)
        self.producer_stage='producer_conformity'
        self.run_kwargs=dict(source_inventory=source,results_dir=self.home/'results',provider_path=provider,snapshot=self.home/'fake-tokenizer',schema_dir=schema_dir or SCHEMA,ledger=self.ledger)
    def run_producer(self):
        with patch.dict(sys.modules,{'openai':self.fake}),patch.object(pp,'offline_token_counter',return_value=lambda s:len(s.split())):
            return pp.run(**self.run_kwargs,stage=self.producer_stage)

    def test_40_producer_validates_all_pairs_and_writes_only_full_library(self):
        self.setup_producer(malformed_at=3);result=self.run_producer()
        self.assertEqual((len(self.calls),result['status'],result['valid_first_attempts']),(8,'FAIL',7))
        self.assertFalse(list((self.home/'results').glob('validated_insight_library*')))

    def test_41_r4_tamper_must_block_before_any_transport(self):
        target=self.home/'bad-schema';target.mkdir()
        for name in ['validator.py','insight_v1.schema.json','leakage_rules_v1.json','SCHEMA_FREEZE.json']:shutil.copyfile(SCHEMA/name,target/name)
        with (target/'validator.py').open('ab') as f:f.write(b'\n')
        self.setup_producer(schema_dir=target)
        try:self.run_producer()
        except Exception:pass
        self.observe(transport_stub_calls=len(self.calls),ledger=self.ledger.snapshot())
        self.assertEqual(len(self.calls),0)

    def test_42_producer_changed_identity_suspends(self):
        self.setup_producer();result=self.run_producer()
        self.observe(summary=result,transport_stub_calls=len(self.calls))
        self.assertNotEqual(result['status'],'PASS')

    def test_43_producer_failure_preserves_completed_raw_before_restart(self):
        self.setup_producer(fail_at=2)
        with self.assertRaises(RuntimeError):self.run_producer()
        snap=self.ledger.snapshot();files=list((self.home/'results').glob('*'))
        self.observe(snapshot=snap,result_files=[str(p) for p in files])
        self.assertEqual(snap['requests_cumulative'],2)
        self.assertTrue(any('fixture-1' in p.read_text() for p in files),'successful raw response lost on later transport failure')

    def test_44_producer_resume_skips_completed_requests(self):
        self.setup_producer(fail_at=2)
        with self.assertRaises(RuntimeError):self.run_producer()
        self.run_kwargs['ledger']=PilotLedger(self.ledger.path,pilot_id='independent-pilot')
        try:self.run_producer()
        except Exception as e:
            self.observe(restart_error=type(e).__name__+': '+str(e),calls=len(self.calls))
            self.assertNotIn('duplicate',str(e),'restart re-enters first already-completed request')

    def test_45_remediation_must_bind_approved_template_hash(self):
        self.conformity('FAIL');self.ledger.authorize_remediation(diff_sha256='b'*64,approval_sha256='c'*64,template_sha256='0'*64)
        self.setup_producer();self.producer_stage='producer_remediation'
        result=self.run_producer();self.observe(summary=result,actual_prompt_hash=sha256_text(self.calls[0]['messages'][0]['content']))
        self.assertNotEqual(result['status'],'PASS','arbitrary authorized template hash was never compared')

    def test_46_consumer_rejects_undecided_before_historical_server_contact(self):
        # Stop at the first attempted server discovery, before all networking.
        touched=[]
        def stop(config):touched.append(config['candidate']);raise RuntimeError('OFFLINE boundary')
        with patch.object(rp,'load_prepared',return_value=({},[])),patch.object(rp,'server_contract',side_effect=stop):
            try:rp.run_budget_stage(self.home,self.home,ledger=self.ledger)
            except Exception:pass
        self.observe(study_model_decision=CONFIG['study_model_decision'],attempted_server_contract=touched)
        self.assertEqual(touched,[],'UNDECIDED still reaches historical 27B endpoint')

    def test_47_load_prepared_checks_source_manifest_hash(self):
        prompt=self.home/'pilot_prompts.jsonl';prompt.write_text(''.join(json.dumps({'prompt_id':f'p{i}'})+'\n' for i in range(40)))
        source=self.home/'source.json';source.write_text(json.dumps({'label_space':['ORIGINAL']}))
        plan=self.home/'pre_gate_plan.json';plan.write_text(json.dumps(dict(status='READY_FOR_PRE_GATE_GENERATION_PROBE',source_manifest=str(source),source_manifest_sha256=sha256_file(source))))
        (self.home/'pre_gate_hashes.json').write_text(json.dumps({'files':{str(plan.relative_to(OUT)):sha256_file(plan),str(prompt.relative_to(OUT)):sha256_file(prompt),str(pathlib.Path('config.json')):sha256_file(rp.PREFLIGHT_CONFIG_PATH),str(source):sha256_file(source)}}))
        config=self.home/'config.json';shutil.copyfile(rp.PREFLIGHT_CONFIG_PATH,config)
        hashes=json.loads((self.home/'pre_gate_hashes.json').read_text());hashes['files'][str(config.relative_to(OUT))]=sha256_file(config);(self.home/'pre_gate_hashes.json').write_text(json.dumps(hashes))
        source.write_text(json.dumps({'label_space':['TAMPERED']}))
        with patch.object(rp,'ROOT',OUT),patch.object(rp,'PREFLIGHT_CONFIG_PATH',config):
            with self.assertRaises(RuntimeError):rp.load_prepared(self.home)

    def test_48_tracked_transport_failure_remains_invalid_in_denominator(self):
        self.probe()
        class Stub:
            model='fixture';sdk_version='fixture'
            def call(self,**kwargs):raise TimeoutError('offline fixture')
        prompt=dict(prompt_id='p1',agent_id='agent_1',case_id='c1',condition='A',sample_role='transfer')
        record=rp._tracked_call(Stub(),self.ledger,prompt=prompt,schema={},generation={},stage='stability_gate',stage_run='gate',logical_id='g1',request_id='g1',return_error_record=True)
        self.assertIs(record['parse_valid_first_attempt'],False);self.assertIsNone(record['parsed_output'])
        self.assertEqual(self.ledger.snapshot()['requests_cumulative'],12)

    def test_49_changed_producer_input_cannot_become_validated_library(self):
        def mutate(inv):inv['producer_conformance_inputs']['local_examples']['agent_1'][0]['neutral_text']='UNVERIFIED OOD/TEST FIXTURE'
        self.setup_producer(mutate_inventory=mutate)
        result=self.run_producer();self.observe(summary=result,altered_text_sent=any('UNVERIFIED OOD/TEST FIXTURE' in x['messages'][0]['content'] for x in self.calls))
        self.assertNotEqual(result['status'],'PASS')

    def setup_consumer(self,fail_at=None):
        self.prepared=self.home/'prepared';self.prepared.mkdir()
        self.results=self.home/'results';self.results.mkdir()
        (self.prepared/'pilot_prompts.jsonl').write_text('OFFLINE FIXTURE IDENTITY\n')
        (self.prepared/'pre_gate_plan.json').write_text('{}')
        self.prompt_rows=[dict(prompt_id=f'p{i}',agent_id=f'agent_{i%8+1}',case_id=f'c{i}',condition='A' if i<8 else ('B-LF' if i<24 else 'E-LF'),sample_role='transfer',input_tokens=i+1) for i in range(40)]
        self.stub_calls=[]
        owner=self
        class Stub:
            model='fixture-consumer';sdk_version='fixture-sdk'
            def __init__(self,config):self.requests=0
            def call(self,*,prompt,**kwargs):
                self.requests+=1;owner.stub_calls.append(prompt['prompt_id'])
                if self.requests==fail_at:raise KeyboardInterrupt('offline crash after completed first call')
                return dict(prompt,parse_valid_first_attempt=True,parsed_output={'abstain':True,'predicted_label':None},finish_reason='stop',latency_seconds=0.01,raw_output='RAW MUST SURVIVE',response_id=f'fake-{self.requests}',returned_model='WRONG-ID',system_fingerprint='WRONG-FINGERPRINT')
        self.server={'process':{'fingerprint_sha256':H}}
        self.plan={'context_feasibility':{'feasible_candidates':[{'thinking_token_budget':2048,'max_tokens':2560}]}}
        self.patches=[patch.object(rp,'load_prepared',return_value=(self.plan,self.prompt_rows)),patch.object(rp,'server_contract',return_value=self.server),patch.object(rp,'Provider',Stub)]
        for p in self.patches:p.start();self.addCleanup(p.stop)

    def test_50_budget_crash_preserves_partial_raw_and_stage_count(self):
        self.conformity();self.setup_consumer(fail_at=2)
        with self.assertRaises(KeyboardInterrupt):rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger)
        snap=PilotLedger(self.ledger.path,pilot_id='independent-pilot').snapshot()
        self.observe(snapshot=snap,files=[p.name for p in self.results.iterdir()])
        self.assertEqual(snap['requests_by_stage']['budget_probe'],2);self.assertEqual(snap['unresolved_intents'],1)
        self.assertTrue(any('RAW MUST SURVIVE' in p.read_text() for p in self.results.iterdir()))

    def test_51_gate_crash_preserves_raw_without_duplicate_on_restart(self):
        self.probe();self.setup_consumer(fail_at=2)
        frozen=dict(status='FROZEN_FOR_STABILITY_GATE',generation={'thinking_token_budget':2048,'max_tokens':2560},prompt_file_sha256=sha256_file(self.prepared/'pilot_prompts.jsonl'),candidate=CONFIG['candidate'],server=self.server,vllm_grammar_schema_sha256=sha256_text(canonical_json(rp.vllm_grammar_schema(json.loads(rp.DIAGNOSTIC_SCHEMA_PATH.read_text())))),go_scope='OFFLINE FIXTURE')
        (self.results/'frozen_gate_config.json').write_text(json.dumps(frozen))
        with self.assertRaises(KeyboardInterrupt):rp.run_stability_stage(self.prepared,self.results,ledger=self.ledger)
        snap=PilotLedger(self.ledger.path,pilot_id='independent-pilot').snapshot()
        self.observe(snapshot=snap,files=[p.name for p in self.results.iterdir()])
        self.assertEqual(snap['requests_by_stage']['stability_gate'],2);self.assertEqual(snap['unresolved_intents'],1)
        self.assertTrue(any('RAW MUST SURVIVE' in p.read_text() for p in self.results.iterdir()))

    def test_52_gate_rejects_frozen_generation_changed_after_probe(self):
        self.conformity();self.setup_consumer()
        rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger)
        path=self.results/'frozen_gate_config.json';frozen=json.loads(path.read_text());frozen['generation']['max_tokens']=9999;path.write_text(json.dumps(frozen))
        calls_before=len(self.stub_calls)
        try:rp.run_stability_stage(self.prepared,self.results,ledger=self.ledger)
        except (RuntimeError,HarnessError):pass
        self.observe(additional_calls=len(self.stub_calls)-calls_before)
        self.assertEqual(len(self.stub_calls),calls_before)

    def test_53_gate_rejects_changed_returned_model(self):
        self.conformity();self.setup_consumer()
        rp.run_budget_stage(self.prepared,self.results,ledger=self.ledger)
        result=rp.run_stability_stage(self.prepared,self.results,ledger=self.ledger)
        self.observe(summary=result)
        self.assertFalse(result['status'].startswith('PASS_R1'))

class RecoveredModuleProbes(Base):
    def test_60_sampling_and_canary_forensic_separation(self):
        prompts=[dict(prompt_id=f'{a}-{f}-{c}',prompt_sha256=sha256_text(f'{a}-{f}-{c}'),agent_id=f'agent_{a}',true_pseudolabel=f'label-{f}',condition=c) for a in range(1,9) for f in range(1,9) for c in ['A','B-LF','E-LF']]
        selected=sampling.select_canaries(prompts)
        self.assertEqual(selected,sampling.select_canaries(reversed(prompts)))
        self.assertEqual(len(selected),10);self.assertEqual(len({x['agent_id'] for x in selected}),8)
        self.assertEqual(len(sampling.select_audit(prompts)),20)
        v=[dict(prompt_id=x['prompt_id'],parsed_output={'abstain':False,'predicted_label':'label'},raw_response='original') for x in selected]
        path=self.home/'canary.json';canary.freeze_expectations(path,v)
        with self.assertRaises(FileExistsError):canary.freeze_expectations(path,v)
        v[0]['raw_response']='different forensic bytes';report=canary.compare_run(path,v)
        self.assertFalse(report['marked_day']);self.assertEqual(report['raw_hash_changes'],1)
        v[0]['parsed_output']['predicted_label']='changed';report=canary.compare_run(path,v)
        self.assertTrue(report['marked_day']);self.assertTrue(canary.suspension_required([report,report],returned_model_changed=False)['suspend'])
        self.assertTrue(canary.suspension_required([],returned_model_changed=True)['suspend'])

    def test_61_recovered_logger_persists_and_detects_tamper(self):
        record=logging_v1.CallRecord.create(prompt_id='p',agent_id='agent_1',physical_case_id='c',condition='A',repetition=1,attempt=1,timestamp_utc='2026-09-14T22:00:00Z',provider='fixture',requested_model='fixture',returned_model='fixture',returned_model_revision=None,request_id='r',system_fingerprint=None,temperature_supported=None,seed_supported=None,generation={},prompt_sha256=H,prompt_bytes=1,raw_response='raw',latency_ms=1,prompt_tokens=1,completion_tokens=2,total_tokens=3,token_source='fixture',finish_reason='stop',truncated=False,parse_valid=True,schema_valid=None,parsed_output={'abstain':True,'predicted_label':None},error=None)
        path=self.home/'calls.jsonl';logger=logging_v1.JsonlCallLogger(path);logger.append(record)
        self.assertEqual(len(logging_v1.read_records(path)),1)
        with self.assertRaises(FileExistsError):logging_v1.JsonlCallLogger(path)
        bad=json.loads(path.read_text());bad['raw_response']='corrupted';path.write_text(json.dumps(bad)+'\n')
        with self.assertRaises(HarnessError):logging_v1.read_records(path)

    def test_62_tokenizer_byte_guards(self):
        snapshot=self.home/'pinned-revision';snapshot.mkdir()
        (snapshot/'tokenizer.json').write_text('{}');(snapshot/'tokenizer_config.json').write_text(json.dumps({'chat_template':'template'}))
        params=dict(revision='pinned-revision',tokenizer_json_sha256=sha256_file(snapshot/'tokenizer.json'),tokenizer_config_sha256=sha256_file(snapshot/'tokenizer_config.json'),chat_template_sha256=sha256_text('template'))
        guards.verify_tokenizer(snapshot,**params)
        (snapshot/'tokenizer.json').write_text('{}\n')
        with self.assertRaises(HarnessError):guards.verify_tokenizer(snapshot,**params)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromModule(sys.modules[__name__])
    with (OUT/'negative_probes.log').open('w') as log:
        result=unittest.TextTestRunner(stream=log,verbosity=2).run(suite)
    failed_methods=sorted({getattr(t,'test_case',t).id() for t,tb in result.failures+result.errors})
    report=dict(tests=result.testsRun,failed_methods=failed_methods,passed_methods=result.testsRun-len(failed_methods),failures=[{'test':str(t),'traceback':tb} for t,tb in result.failures],errors=[{'test':str(t),'traceback':tb} for t,tb in result.errors],observations=OBS)
    (OUT/'negative_probes.json').write_text(json.dumps(report,indent=2))
    print(json.dumps({'tests':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'failed_method_count':len(failed_methods),'passed_method_count':result.testsRun-len(failed_methods)},indent=2))
    sys.exit(0 if result.wasSuccessful() else 1)
