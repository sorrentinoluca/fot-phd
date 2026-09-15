"""Same final real-adapter/fake-SDK regression on both runtimes; no live services."""
import sys,json,types,os,sqlite3,unittest,hashlib
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,os.environ['FOT_D9_TARGET'])
from studio2.fase03.harness import test_revisions as scaffolding
from studio2.fase03 import run_pilot as rp
from studio2.fase03.harness.common import HarnessError
from studio2.fase03.harness.ledger import digest

class TransportBoundary(unittest.TestCase):
 def scenario(self, missing):
  t=scaffolding.RunnerRevisions();t.setUp();captured=[];result={}
  try:
   import shutil
   canonical=t.snapshot;chat=t.home/'chat'/canonical.name;shutil.copytree(canonical,chat);t.snapshot=chat
   t.prepare()
   with patch.object(rp,'execute_request',side_effect=HarnessError('stop before reserve')):
    with self.assertRaisesRegex(HarnessError,'stop before reserve'):rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
   b=t.ledger.binding('budget_probe');plan,prompts=rp.load_prepared(t.prepared,ledger=t.ledger);spec=b['requests'][0]
   prompt=next(p for p in prompts if p['prompt_sha256']==spec['prompt_sha256']);candidate=plan['context_feasibility']['feasible_candidates'][0]
   generation={k:t.config['generation_budget'][k] for k in ('seed',) if k in t.config['generation_budget']};generation.update({k:candidate[k] for k in ('thinking_token_budget','max_tokens')})
   schema=rp.vllm_grammar_schema(rp.load_json(rp.DIAGNOSTIC_SCHEMA_PATH))
   def create(**kw):
    captured.append(kw)
    raw={'id':'fake-response','model':kw['model'],'system_fingerprint':None,'choices':[{'message':{'content':json.dumps({'predicted_label':None,'abstain':True,'used_insight_ids':[],'reasoning_summary':'Fixture.'})},'finish_reason':'stop'}]}
    return types.SimpleNamespace(model_dump=lambda **unused:raw)
   client=types.SimpleNamespace(chat=types.SimpleNamespace(completions=types.SimpleNamespace(create=create)))
   def db():
    with sqlite3.connect(t.ledger.path) as c:return '\n'.join(c.iterdump())
   before=db();journal=t.results/'boundary.jsonl'
   if missing:(canonical if missing=='R4' else chat).joinpath('tokenizer.json').unlink()
   with patch.dict(sys.modules,{'openai':types.SimpleNamespace(__version__='fixture',OpenAI=lambda **kw:client)}):
    provider=scaffolding.REAL_PROVIDER(t.config)
    def call():return rp._tracked_call(provider,t.ledger,prompt=prompt,schema=schema,generation=generation,stage='budget_probe',stage_run=digest(b),logical_id=spec['logical_id'],config=t.config,journal_path=journal)
    if missing:
     with self.assertRaisesRegex(HarnessError,'tokenizer'):call()
     self.assertEqual(captured,[]);self.assertEqual(before,db());self.assertFalse(journal.exists())
    else:
     call();self.assertEqual(len(captured),1);self.assertTrue(journal.exists());self.assertEqual(t.ledger.snapshot()['requests_cumulative'],9)
  finally:
   result.update(missing=missing,fake_sdk_calls=len(captured),requests_cumulative=t.ledger.snapshot()['requests_cumulative'],database_sha256=hashlib.sha256(db().encode()).hexdigest())
   out=Path(os.environ['TRANSPORT_RESULTS']);out.mkdir(parents=True,exist_ok=True);(out/(self._testMethodName+'.json')).write_text(json.dumps(result,indent=2)+'\n');t.doCleanups()
 def test_positive_real_adapter_fake_sdk(self):self.scenario(None)
 def test_missing_canonical_before_tracked_call(self):self.scenario('R4')
 def test_missing_service_before_tracked_call(self):self.scenario('chat')

if __name__=='__main__':unittest.main(verbosity=2)
