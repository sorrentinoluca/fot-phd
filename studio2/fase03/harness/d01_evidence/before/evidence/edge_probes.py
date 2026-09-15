"""Independent supplemental review. All transports and approvals are disposable fixtures."""
from pathlib import Path
import sys,json,subprocess,os,sqlite3,unittest,shutil,types
from unittest.mock import patch
from contextlib import closing
E=Path(__file__).resolve().parent;C=E.parent/'candidate';sys.path.insert(0,str(C))
from studio2.fase03.harness.test_revisions import RunnerRevisions,rp,pp,pg
from studio2.fase03.harness import runtime
from studio2.fase03.harness.ledger import PilotLedger,digest
from studio2.fase03.harness.common import HarnessError
from studio2.fase03.harness.offline_fixtures import Trial
OLD=Path('/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate')
OBS={}
class Edges(unittest.TestCase):
 def setUp(self):
  self.home=E/'edge_fixtures'/self._testMethodName;self.home.mkdir(parents=True,exist_ok=False)
  self.addCleanup(patch.stopall)
 def note(self,**v):OBS[self._testMethodName]=v
 def runner(self):
  t=RunnerRevisions();t.setUp();self.addCleanup(t.doCleanups);self.addCleanup(lambda:shutil.copytree(t.home,self.home/'captured',dirs_exist_ok=True));return t
 def test_Y01_legacy_closed_unsafe_gate_is_rejected_by_real_resume(self):
  code='''import sys,os,tempfile,json
from pathlib import Path
from unittest.mock import patch
from studio2.fase03.harness.test_revisions import RunnerRevisions,rp
home=Path(sys.argv[1]);original=tempfile.TemporaryDirectory
with patch.object(tempfile,'TemporaryDirectory',side_effect=lambda **kw:original(dir=home,**kw)):
 t=RunnerRevisions();t.setUp()
(home/'locator').write_text(str(t.home))
t.prepare();t.fail_at=9
try:t.producer(stage='alternate_conformity')
except ValueError:pass
rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
result=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
(home/'old_result.json').write_text(json.dumps(result))
os._exit(0)
'''
  proc=subprocess.run([sys.executable,'-c',code,str(self.home)],cwd=OLD,env=dict(os.environ,PYTHONPATH=str(OLD),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
  (self.home/'old_process.stderr').write_text(proc.stderr);self.assertEqual(proc.returncode,0,proc.stderr)
  home=Path((self.home/'locator').read_text());t=self.runner();t.home=home;t.config_path=home/'config.json';t.prepared=home/'prepared';t.results=home/'consumer_results';t.ledger=PilotLedger(home/'pilot.sqlite3',pilot_id='runner-fixture')
  for m in (pp,rp,pg):t.stack.enter_context(patch.object(m,'PREFLIGHT_CONFIG_PATH',t.config_path))
  error=None;result=None
  try:result=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
  except HarnessError as exc:error=str(exc)
  self.note(error=error,result=result,new_sends=len(t.consumer_calls),alternate=t.ledger.request(t.ledger.leaf('alternate_conformity','agent_1')['request_id']),snapshot=t.ledger.snapshot())
  self.assertIsNotNone(error,'Unsafe legacy outcome must not be reconfirmed with failed alternate')
 def test_Y02_legacy_closed_unsafe_gate_verification_is_rejected(self):
  code='''import sys
from studio2.fase03.harness.offline_fixtures import Trial
t=Trial(sys.argv[1]);t.finish();t.bind('alternate_conformity');t.reserve(0,'alternate_conformity');t.finish('budget_probe',3);t.finish('stability_gate')
'''
  p=subprocess.run([sys.executable,'-c',code,str(self.home)],cwd=OLD,env=dict(os.environ,PYTHONPATH=str(OLD),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr)
  t=Trial(self.home);errors=[]
  for name,call in [('verify_success',lambda:t.ledger.verify_stage_success('stability_gate')),('replay_outcome',lambda:t.outcome('stability_gate'))]:
   error=None
   try:call()
   except HarnessError as exc:error=str(exc)
   errors.append([name,error])
  self.note(checks=errors,snapshot=t.ledger.snapshot());self.assertTrue(all(e for _,e in errors),'Both success verification and outcome replay must reject unresolved alternate')
 def test_Y03_raw_identity_cannot_be_reclassified_as_absent(self):
  t=Trial(self.home);t.finish();t.finish('budget_probe',3);t.bind('stability_gate');r=t.reserve(0,'stability_gate');t.ledger.save_raw(r,{'model':'WRONG','usage':{'total_tokens':17}})
  with self.assertRaises(HarnessError):t.ledger.complete_request(r,status='FAILED',transport_failure=True,detail={'error_type':'TimeoutError'})
  self.assertIsNone(t.ledger.gate_transport_record(r));self.assertEqual(t.ledger.response(r)['raw']['model'],'WRONG');self.note(snapshot=t.ledger.snapshot())
 def test_Y04_journal_io_failure_after_invalidity_commit_recovers(self):
  t=self.runner();t.prepare();rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger);stub=rp.Provider
  class Fail(stub):
   def call(inner,**kw):t.consumer_calls.append('TIMEOUT');raise TimeoutError('fixture')
  original=runtime.export_journal
  def broken(ledger,stage,path):
   if stage=='stability_gate' and ledger.stage_records(stage):raise OSError('FIXTURE disk write failure')
   return original(ledger,stage,path)
  with patch.object(rp,'Provider',Fail),patch.object(runtime,'export_journal',side_effect=broken),self.assertRaises(OSError):rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
  self.assertEqual(len(t.consumer_calls),4);records=t.ledger.stage_records('stability_gate');self.assertEqual(len(records),1)
  result=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
  self.assertEqual(len(t.consumer_calls),123);self.assertEqual(result['invalid_first_attempts'],1);self.assertEqual(result['status'],'R3_REQUIRED_PENDING_FEASIBILITY');self.note(result=result,snapshot=t.ledger.snapshot())
 def test_Y05_guard_failure_is_not_converted_to_gate_invalidity(self):
  t=self.runner();t.prepare();rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger);stub=rp.Provider
  class Guard(stub):
   def call(inner,**kw):raise HarnessError('FIXTURE pretransport guard')
  with patch.object(rp,'Provider',Guard),self.assertRaises(HarnessError):rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
  self.assertEqual(len(t.consumer_calls),3);self.assertEqual(t.ledger.snapshot()['unresolved_intents'],1);self.assertEqual(t.ledger.stage_records('stability_gate'),[]);self.note(snapshot=t.ledger.snapshot())
 def test_Y06_gate_invalidity_same_identity_cannot_be_retried(self):
  t=Trial(self.home);t.finish();t.finish('budget_probe',3);t.bind('stability_gate');r=t.reserve(0,'stability_gate')
  t.ledger.complete_request(r,status='FAILED',transport_failure=True,detail={'error_type':'TimeoutError'})
  before=t.ledger.gate_transport_record(r);t.zero(r)
  self.assertEqual(t.ledger.gate_transport_record(r),before)
  with self.assertRaises(HarnessError):t.retry(r,'illegal-retry')
  self.note(record=before,snapshot=t.ledger.snapshot())
 def test_Y07_alternate_summary_restart_preserves_stage_not_pilot_denominator(self):
  t=self.runner();t.prepare();t.fail_at=10
  with self.assertRaises(HarnessError):t.producer(stage='alternate_conformity')
  r=t.ledger.leaf('alternate_conformity','agent_2')['request_id'];helper=Trial(self.home/'helper');helper.ledger=t.ledger;helper.zero(r)
  result=t.producer(stage='alternate_conformity',resume=True,retry_requests=[r]);self.assertEqual(result['provider_requests'],9);self.assertEqual(result['evaluable_calls'],8);self.assertEqual(t.ledger.snapshot()['requests_cumulative'],17)
  path=t.home/'results/producer_conformance_fixture_alternate_conformity_summary.json';path.unlink();again=t.producer(stage='alternate_conformity',resume=True)
  self.assertEqual(again,result);self.assertEqual(len(t.calls),17);self.assertEqual(t.ledger.event('outcome:alternate_conformity')['artifact'],result);self.note(summary=result,snapshot=t.ledger.snapshot())
if __name__=='__main__':
 with (E/'edge_probes.log').open('w') as f:r=unittest.TextTestRunner(stream=f,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Edges))
 (E/'edge_probes.json').write_text(json.dumps(dict(tests=r.testsRun,failures=[{'test':str(t),'traceback':s} for t,s in r.failures],errors=[{'test':str(t),'traceback':s} for t,s in r.errors],observations=OBS),indent=2)+'\n')
 print(r.testsRun,len(r.failures),len(r.errors))
