"""D9 discriminating probes. Offline fixture approvals are never scientific authorization."""
import importlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
from copy import deepcopy
from unittest.mock import patch

# Same test file can target exact prior bytes, without modifying that checkout.
if os.environ.get('FOT_D9_TARGET'):
    sys.path.insert(0, os.environ['FOT_D9_TARGET'])
from studio2.fase03.harness.common import HarnessError, canonical_json, sha256_text
from studio2.fase03.harness.guards import require_execution


class D9Contract(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.home=Path(self.tmp.name)

    def approved(self, config):
        value=deepcopy(config); p=self.home/'approval.json'
        p.write_text(json.dumps({'author':'FIXTURE ONLY','decision':'accepted',
                                'configuration_sha256':sha256_text(canonical_json(value))}))
        value['execution_authorization']={'path':str(p),'sha256':sha256_text(p.read_text())}
        return value

    def test_legacy_nominal_approval_is_not_d9(self):
        config=self.approved({'study_model_decision':'APPROVED','status':'APPROVED_FOR_PHASE03_EXECUTION'})
        with self.assertRaisesRegex(HarnessError,'D9'):
            require_execution(config)

    def test_fixed_roles_and_pending_configuration(self):
        d9=importlib.import_module('studio2.fase03.harness.d9')
        self.assertEqual(d9.ROLES,{'producer':'122B','consumer':'122B','alternate':'27B'})
        path=Path(d9.__file__).parents[1]/'config/pilot_d9_pending.json'
        config=json.loads(path.read_text())
        self.assertEqual(config['d9']['roles'],d9.ROLES)
        self.assertEqual(config['d9']['alternate_placement'],'PENDING')
        with self.assertRaises(HarnessError):require_execution(config)

    def test_payload_122b_omits_temperature_and_preserves_controls(self):
        d9=importlib.import_module('studio2.fase03.harness.d9')
        generation={'max_tokens':100,'seed':None,'thinking_token_budget':None}
        self.assertEqual(d9.generation_kwargs(generation,model_role='122B'),{'max_tokens':100})
        self.assertEqual(d9.generation_kwargs(dict(generation,seed=17,thinking_token_budget=50),model_role='122B'),
                         {'max_tokens':100,'seed':17,'extra_body':{'thinking_token_budget':50}})
        for value in (None,0,0.6,''):
            with self.subTest(value=value),self.assertRaises(HarnessError):
                d9.generation_kwargs(dict(generation,temperature=value),model_role='122B')

    def test_role_stage_mapping_rejects_extra_arms(self):
        d9=importlib.import_module('studio2.fase03.harness.d9')
        for stage in ('producer_conformity','producer_remediation','budget_probe','stability_gate'):
            self.assertEqual(d9.model_for_stage(stage),'122B')
        self.assertEqual(d9.model_for_stage('alternate_conformity'),'27B')
        for stage in ('terra','consumer_27b','fallback','swap_gate'):
            with self.subTest(stage=stage),self.assertRaises(HarnessError):d9.model_for_stage(stage)


class D9Runners(unittest.TestCase):
    def setUp(self):
        from studio2.fase03.harness.test_revisions import RunnerRevisions
        self.t=RunnerRevisions(); self.t.setUp(); self.addCleanup(self.t.doCleanups)
        from studio2.fase03.harness import d9
        self.d9=d9

    def test_configuration_mutations_refuse_before_client_and_intent(self):
        t=self.t; baseline=deepcopy(t.config)
        mutations=[lambda c:c['d9']['roles'].update(consumer='27B'),
                   lambda c:c['d9'].update(alternate_placement='PENDING'),
                   lambda c:c['d9'].update(missing_requirements=['weights revision']),
                   lambda c:c['d9'].pop('history_reconciliation'),
                   lambda c:c['d9']['services']['122B'].update(model='27B'),
                   lambda c:c['generation_budget'].update(temperature=None)]
        for mutate in mutations:
            t.config=deepcopy(baseline);mutate(t.config);t.approve_config()
            with self.subTest(mutation=mutations.index(mutate)),self.assertRaises(HarnessError):t.producer()
            self.assertEqual(t.ledger.snapshot()['requests_cumulative'],0);self.assertEqual(t.calls,[])
        t.config=baseline;t.approve_config();self.assertEqual(t.producer()['status'],'PASS')
        self.assertTrue(all('temperature' not in k for k in t.calls));self.assertEqual(len(t.calls),8)

    def test_swapped_provider_or_unapproved_alternate_is_rejected(self):
        t=self.t
        with self.assertRaises(HarnessError):t.producer(stage='alternate_conformity')
        t.config['d9']['alternate_placement']='pilot';t.approve_config()
        from studio2.fase03 import producer_probe as pp
        with self.assertRaises(HarnessError):
            pp.run(source_inventory=t.source,results_dir=t.home/'results',provider_path=t.provider,snapshot=t.snapshot,
                   schema_dir=Path(pp.__file__).parent/'schema_insight',ledger=t.ledger,stage='alternate_conformity')
        self.assertEqual(t.calls,[]);self.assertEqual(t.ledger.snapshot()['requests_cumulative'],0)

    def test_document_changes_after_binding_block_resume_without_sends(self):
        t=self.t;t.producer();before=t.ledger.snapshot()['requests_cumulative']
        path=Path(t.config['d9']['services']['122B']['documentation']['path']);path.write_bytes(path.read_bytes()+b' ')
        with self.assertRaisesRegex(HarnessError,'bytes changed'):t.producer(resume=True)
        self.assertEqual(len(t.calls),8);self.assertEqual(t.ledger.snapshot()['requests_cumulative'],before)
        from studio2.fase03.harness.ledger import PilotLedger
        ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
        with self.assertRaisesRegex(HarnessError,'bytes changed'):ledger.binding('producer_conformity')

    def test_r4_counter_distinct_from_service_counter(self):
        t=self.t;seen=[]
        def counter(snapshot,*,chat_template=True):
            seen.append((str(snapshot),chat_template));return lambda text:10000 if not chat_template else 1
        from studio2.fase03 import producer_probe as pp
        with patch.object(pp,'offline_token_counter',side_effect=counter):
            result=t.producer()
        self.assertEqual(result['status'],'FAIL')
        self.assertIn((str(t.snapshot),False),seen);self.assertIn((str(t.snapshot),True),seen)
        self.assertEqual(len(t.calls),8)  # Valid chat capacity does not waive canonical insight caps.

    def test_service_output_limit_rejects_before_client(self):
        t=self.t;t.provider_value['max_tokens']=20000;t.provider.write_text(json.dumps(t.provider_value))
        from studio2.fase03.harness.common import sha256_file
        t.config['d9']['producer_configs']['122B']=sha256_file(t.provider)
        t.config['approved_producer_config_sha256']=list(t.config['d9']['producer_configs'].values());t.approve_config()
        with self.assertRaisesRegex(HarnessError,'output exceeds'):t.producer()
        self.assertEqual(t.calls,[])

    def test_history_mapping_cannot_reset_consumption(self):
        t=self.t;from_source=deepcopy(self.d9.HISTORY_SOURCE);from_source['reported_requests']=1
        path=Path(t.config['d9']['history_reconciliation']['path']);value=json.loads(path.read_text())
        value['source']=from_source;value['request_identities']={'historical-missing':'a'*64};path.write_text(json.dumps(value))
        from studio2.fase03.harness.common import sha256_file
        t.config['d9']['history_reconciliation']['sha256']=sha256_file(path);t.approve_config()
        with patch.object(self.d9,'HISTORY_SOURCE',from_source),self.assertRaisesRegex(HarnessError,'not represented'):t.producer()
        self.assertEqual(t.calls,[]);self.assertEqual(t.ledger.snapshot()['requests_cumulative'],0)

    def test_direct_consumer_transport_requires_reservation(self):
        t=self.t
        from studio2.fase03.harness.test_revisions import REAL_PROVIDER
        import types
        # Actual Provider, only SDK factory stubbed; no socket transport.
        with patch.dict(sys.modules,{'openai':types.SimpleNamespace(__version__='fixture',OpenAI=lambda **kw:object())}):
            provider=REAL_PROVIDER(t.config)
        with self.assertRaisesRegex(HarnessError,'reserved durable'):
            provider.call(prompt={'text':'fixture'},schema={},generation={'max_tokens':10})

        # Positive: real consumer adapter on ordinary ledger path, captured SDK kwargs.
        from studio2.fase03 import run_pilot as rp
        t.prepare(); captured=[]
        def create(**kw):
            captured.append(kw)
            raw={'id':f'captured-{len(captured)}','model':kw['model'],'system_fingerprint':None,
                 'choices':[{'message':{'content':json.dumps({'predicted_label':None,'abstain':True,
                   'used_insight_ids':[],'reasoning_summary':'Fixture.'})},'finish_reason':'stop'}]}
            return types.SimpleNamespace(model_dump=lambda **unused:raw)
        client=types.SimpleNamespace(chat=types.SimpleNamespace(completions=types.SimpleNamespace(create=create)))
        with patch.dict(sys.modules,{'openai':types.SimpleNamespace(__version__='fixture',OpenAI=lambda **kw:client)}), patch.object(rp,'Provider',REAL_PROVIDER):
            rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        self.assertEqual(len(captured),3)
        self.assertTrue(all('temperature' not in kw and kw['model']=='fixture-model' for kw in captured))
        self.assertEqual(self.d9.accounting(t.ledger)['by_role']['consumer'],3)

    def test_resume_counts_once_by_role_and_model(self):
        t=self.t;t.producer();t.producer(resume=True)
        result=self.d9.accounting(t.ledger)
        self.assertEqual(result['requests_cumulative'],8)
        self.assertEqual(result['by_role'],{'producer':8,'consumer':0,'alternate':0})
        self.assertEqual(result['by_nominal_model'],{'122B':8,'27B':0});self.assertEqual(len(t.calls),8)



    def test_alternate_pilot_full_library_and_same_case_swap(self):
        t=self.t
        from studio2.fase03 import run_pilot as rp
        t.config['d9']['alternate_placement']='pilot';t.approve_config();t.prepare()
        with self.assertRaisesRegex(HarnessError,'alternate_conformity'):
            rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        self.assertEqual(t.consumer_calls,[])
        result=t.producer(stage='alternate_conformity');self.assertEqual(result['status'],'PASS')
        primary=t.home/'results/validated_insight_library_fixture_producer_conformity.json'
        alternate=t.home/'results/validated_insight_library_fixture-alternate_alternate_conformity.json'
        before=json.loads(t.manifest.read_text())
        swapped,provenance=self.d9.swap_manifest(before,primary_handoff=primary,alternate_handoff=alternate,
            config=t.config,ledger=t.ledger,schema_dir=Path(rp.__file__).parent/'schema_insight',token_count=lambda s:len(s.split()))
        self.assertEqual(len(swapped['insights']),16)
        self.assertEqual({k:v for k,v in swapped.items() if k!='insights'},{k:v for k,v in before.items() if k!='insights'})
        self.assertEqual(provenance['consumer'],t.config['d9']['services']['122B'])
        self.assertEqual(provenance['alternate']['stage'],'alternate_conformity')
        rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        counts=self.d9.accounting(t.ledger)
        self.assertEqual(counts['by_nominal_model'],{'122B':11,'27B':8})
        self.assertEqual(counts['requests_cumulative'],19)
        value=json.loads(alternate.read_text());value['library'].pop();alternate.write_text(json.dumps(value))
        with self.assertRaises(HarnessError):
            self.d9.swap_manifest(before,primary_handoff=primary,alternate_handoff=alternate,
                config=t.config,ledger=t.ledger,schema_dir=Path(rp.__file__).parent/'schema_insight',token_count=lambda s:len(s.split()))

    def test_persisted_provider_mutation_and_direct_reservation(self):
        t=self.t;t.fail_at=1
        with self.assertRaises(HarnessError):t.producer()
        import sqlite3
        from studio2.fase03.harness.ledger import digest, PilotLedger
        with sqlite3.connect(t.ledger.path) as c:
            binding=json.loads(c.execute('SELECT binding_json FROM stages').fetchone()[0])
            binding['provider']['max_tokens']+=1
            c.execute('UPDATE stages SET binding_json=?,binding_sha256=?',(canonical_json(binding),digest(binding)))
        ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
        with self.assertRaisesRegex(HarnessError,'certified bytes'):ledger.binding('producer_conformity')
        with self.assertRaises(HarnessError):
            ledger.reserve_request(request_id='new',logical_id='agent_2',model='fixture-model',producer='fixture',
                stage='producer_conformity',stage_run=digest(binding))
        self.assertEqual(ledger.snapshot()['requests_cumulative'],1);self.assertEqual(len(t.calls),1)

    def test_pending_cli_does_not_create_ledger(self):
        t=self.t
        from studio2.fase03 import run_pilot as rp, producer_probe as pp
        pending=Path(rp.__file__).parent/'config/pilot_d9_pending.json'
        for module,extra in [(rp,['--stage','budget']),(pp,['--source-inventory',str(t.source),'--provider-config',str(t.provider)])]:
            ledger=t.home/(module.__name__.split('.')[-1]+'_never.sqlite3')
            argv=['fixture','--config',str(pending),'--execute','--acknowledge',module.ACK,
                  '--ledger',str(ledger),'--pilot-id','unapproved-fixture',*extra]
            with patch.object(sys,'argv',argv),self.assertRaises(HarnessError):module.main()
            self.assertFalse(ledger.exists())

class D9PriorBehavior(unittest.TestCase):
    """Behavioral differential using each target's ordinary complete offline fixture."""
    def setUp(self):
        from studio2.fase03.harness.test_revisions import RunnerRevisions
        self.t=RunnerRevisions();self.t.setUp();self.addCleanup(self.t.doCleanups)

    def test_122b_temperature_is_rejected_before_any_send(self):
        t=self.t
        from studio2.fase03.harness.common import sha256_file
        t.provider_value['temperature']=0.6;t.provider.write_text(json.dumps(t.provider_value))
        if 'd9' in t.config:
            t.config['d9']['producer_configs']['122B']=sha256_file(t.provider)
            t.config['approved_producer_config_sha256']=list(t.config['d9']['producer_configs'].values())
        else:t.config['approved_producer_config_sha256']=[sha256_file(t.provider)]
        t.approve_config()
        with self.assertRaises(HarnessError):t.producer()
        self.assertEqual(t.calls,[]);self.assertEqual(t.ledger.snapshot()['requests_cumulative'],0)

    def test_primary_provider_cannot_execute_alternate_role(self):
        t=self.t
        from studio2.fase03 import producer_probe as pp
        with self.assertRaises(HarnessError):
            pp.run(source_inventory=t.source,results_dir=t.home/'results',provider_path=t.provider,snapshot=t.snapshot,
                   schema_dir=Path(pp.__file__).parent/'schema_insight',ledger=t.ledger,stage='alternate_conformity')
        self.assertEqual(t.calls,[]);self.assertEqual(t.ledger.snapshot()['requests_cumulative'],0)

if __name__=='__main__':unittest.main(verbosity=2)
