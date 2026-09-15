"""Bounded fake-SDK check through actual execute_request and Provider adapter."""
import sys,json,types,shutil,os
from pathlib import Path
from unittest.mock import patch
root=Path(__file__).resolve().parents[3];sys.path.insert(0,str(root/'work/candidate'))
from studio2.fase03.harness import test_revisions as scaffolding
from studio2.fase03 import run_pilot as rp
from studio2.fase03.harness.common import HarnessError
from studio2.fase03.harness.ledger import digest
out=Path(__file__).parent/'transport_snapshot_probe';out.mkdir(exist_ok=False)
t=scaffolding.RunnerRevisions();t.setUp();captured=[]
try:
 t.prepare()
 # Real runner prepares/authenticates the plan and binds it; stop before its first reserve.
 with patch.object(rp,'execute_request',side_effect=HarnessError('independent stop')):
  try:rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
  except HarnessError as ex:assert str(ex)=='independent stop'
 b=t.ledger.binding('budget_probe');plan,prompts=rp.load_prepared(t.prepared,ledger=t.ledger);s=b['requests'][0]
 prompt=next(p for p in prompts if p['prompt_sha256']==s['prompt_sha256'])
 candidate=plan['context_feasibility']['feasible_candidates'][0]
 generation={k:t.config['generation_budget'][k] for k in ('seed',) if k in t.config['generation_budget']};generation.update({k:candidate[k] for k in ('thinking_token_budget','max_tokens')})
 schema=rp.vllm_grammar_schema(rp.load_json(rp.DIAGNOSTIC_SCHEMA_PATH))
 def create(**kw):
  captured.append(kw)
  raw={'id':'independent-fake-response','model':kw['model'],'system_fingerprint':None,'choices':[{'message':{'content':json.dumps({'predicted_label':None,'abstain':True,'used_insight_ids':[],'reasoning_summary':'Fixture.'})},'finish_reason':'stop'}]}
  return types.SimpleNamespace(model_dump=lambda **unused:raw)
 client=types.SimpleNamespace(chat=types.SimpleNamespace(completions=types.SimpleNamespace(create=create)))
 (t.snapshot/'tokenizer.json').unlink()
 with patch.dict(sys.modules,{'openai':types.SimpleNamespace(__version__='fixture',OpenAI=lambda **kw:client)}):
  provider=scaffolding.REAL_PROVIDER(t.config)
  record=rp._tracked_call(provider,t.ledger,prompt=prompt,schema=schema,generation=generation,stage='budget_probe',stage_run=digest(b),logical_id=s['logical_id'],config=t.config,journal_path=t.results/'independent_journal.jsonl')
 result={'actual_provider_class':str(type(provider)),'actual_execute_request_module':rp.execute_request.__module__,'fake_sdk_calls':len(captured),'tokenizer_exists':(t.snapshot/'tokenizer.json').exists(),'requests_cumulative':t.ledger.snapshot()['requests_cumulative'],'record':record,'payloads':captured}
 (out/'result.json').write_text(json.dumps(result,indent=2));shutil.copytree(t.home,out/'fixture');print(json.dumps({k:v for k,v in result.items() if k not in ('record','payloads')},indent=2))
finally:t.doCleanups()
