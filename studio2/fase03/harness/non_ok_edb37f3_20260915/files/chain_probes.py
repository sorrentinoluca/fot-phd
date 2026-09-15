"""Independent D01 extension: authenticated predecessors and coherent confirmation.
Only sacrificial fixtures; SQL fault injection is separate from original legacy Y tests.
"""
from pathlib import Path
import sys,json,sqlite3,subprocess,os,unittest,shutil
from contextlib import closing
from unittest.mock import patch
E=Path(__file__).resolve().parent;C=E.parent/'candidate';sys.path.insert(0,str(C))
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness.ledger import PilotLedger,digest
from studio2.fase03.harness.common import HarnessError
from studio2.fase03.harness.test_revisions import RunnerRevisions,rp
OBS={}
def logical(l):
 with closing(sqlite3.connect(l.path)) as c:return '\n'.join(c.iterdump())
class Chain(unittest.TestCase):
 def setUp(self):
  self.home=E/'chain_fixtures'/self._testMethodName;self.home.mkdir(parents=True,exist_ok=False);self.addCleanup(patch.stopall)
 def note(self,**v):OBS[self._testMethodName]=v
 def ready(self,home):
  t=Trial(home);t.finish();t.finish('alternate_conformity');t.finish('budget_probe',3);t.finish('stability_gate');return t
 def entries(self,l):
  b=l.binding('stability_gate');o=l.event('outcome:stability_gate');f=l.event('frozen_gate')['frozen']
  return [('binding',lambda:l.bind_stage('stability_gate',b)),('success',lambda:l.verify_stage_success('stability_gate')),('outcome',lambda:l.record_stage_outcome('stability_gate',outcome='PASS',artifact_sha256=o['artifact_sha256'],artifact=o['artifact'])),('frozen',lambda:l.authenticate_frozen(f))]
 def test_Z01_corrupted_predecessor_raw_blocks_normative_confirmation(self):
  observations=[]
  for stage in ('producer_conformity','alternate_conformity','budget_probe'):
   t=self.ready(self.home/stage);l=t.ledger
   for _,call in self.entries(l):call() # Valid positive chain first.
   request=stage+'-0'
   with closing(sqlite3.connect(l.path)) as c,c:c.execute("update responses set raw_json='{}' where request_id=?",(request,))
   with self.assertRaises(HarnessError):l.response(request) # Prove the fault is real.
   before=logical(l);errors=[]
   for name,call in self.entries(l):
    error=None
    try:call()
    except HarnessError as exc:error=str(exc)
    errors.append(dict(entry=name,error=error))
   self.assertEqual(logical(l),before);observations.append(dict(stage=stage,checks=errors,snapshot=l.snapshot()))
  self.note(observations=observations)
  self.assertTrue(all(x['error'] for r in observations for x in r['checks']),'Normative confirmation must reject corrupted predecessor raw, not merely retain COMPLETED/PASS flags')
 def test_Z02_missing_predecessor_coverage_is_not_a_successful_chain(self):
  t=self.ready(self.home/'missing');l=t.ledger
  with closing(sqlite3.connect(l.path)) as c,c:c.execute("delete from requests where request_id='alternate_conformity-7'")
  before=logical(l);checks=[]
  for name,call in self.entries(l):
   error=None
   try:call()
   except HarnessError as exc:error=str(exc)
   checks.append(dict(entry=name,error=error))
  self.assertEqual(logical(l),before);self.note(checks=checks,snapshot=l.snapshot())
  self.assertTrue(all(r['error'] for r in checks),'Seven surviving COMPLETED alternate requests must not reconfirm an eight-case predecessor')
 def test_Z03_real_runner_rejects_corrupted_alternate_predecessor(self):
  t=RunnerRevisions();t.setUp();self.addCleanup(t.doCleanups);self.addCleanup(lambda:shutil.copytree(t.home,self.home/'captured',dirs_exist_ok=True))
  t.prepare();t.producer(stage='alternate_conformity');rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger);old=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
  req=t.ledger.leaf('alternate_conformity','agent_1')['request_id']
  with closing(sqlite3.connect(t.ledger.path)) as c,c:c.execute("update responses set raw_json='{}' where request_id=?",(req,))
  with self.assertRaises(HarnessError):t.ledger.response(req)
  before=logical(t.ledger);sends=len(t.consumer_calls);error=None;result=None
  t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
  try:result=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
  except HarnessError as exc:error=str(exc)
  self.assertEqual(logical(t.ledger),before);self.assertEqual(len(t.consumer_calls),sends)
  self.note(error=error,result=result,same_as_valid_result=result==old,new_sends=len(t.consumer_calls)-sends,corrupted_request=req,snapshot=t.ledger.snapshot())
  self.assertIsNotNone(error,'Ordinary gate resume must reject corrupted raw from its alternate predecessor')
 def test_Z04_each_confirmation_holds_a_real_write_lock_for_all_predecessor_reads(self):
  t=self.ready(self.home/'lock');l=t.ledger;before=logical(l);observations=[]
  code='''import sqlite3,sys,json
c=sqlite3.connect(sys.argv[1],timeout=.15)
try:
 c.execute('BEGIN IMMEDIATE');c.rollback();print(json.dumps({'blocked':False}))
except sqlite3.OperationalError as e:print(json.dumps({'blocked':True,'error':str(e)}))
finally:c.close()
'''
  for name,call in self.entries(l):
   original=l._prerequisites;seen=[]
   def during(c,stage):
    if not seen:
     self.assertTrue(c.in_transaction)
     p=subprocess.run([sys.executable,'-c',code,str(l.path)],capture_output=True,text=True,timeout=5)
     self.assertEqual(p.returncode,0,p.stderr);r=json.loads(p.stdout);seen.append(r);self.assertTrue(r['blocked']);self.assertIn('locked',r['error'])
    return original(c,stage)
   with patch.object(l,'_prerequisites',side_effect=during):call()
   # After return the same process can acquire the lock; no intended writes are inserted.
   p=subprocess.run([sys.executable,'-c',code,str(l.path)],capture_output=True,text=True,timeout=5);self.assertEqual(p.returncode,0);after=json.loads(p.stdout);self.assertFalse(after['blocked'])
   observations.append(dict(entry=name,during=seen,after=after))
  self.assertEqual(logical(l),before);self.note(observations=observations)
 def test_Z05_closed_failed_gate_replays_without_promoting_outcome(self):
  t=Trial(self.home/'invalid');t.finish();t.finish('budget_probe',3);t.bind('stability_gate')
  for i in range(120):
   r=t.reserve(i,'stability_gate');t.ledger.complete_request(r,status='FAILED',transport_failure=True,detail={'error_type':'TimeoutError'})
  t.outcome('stability_gate','FAIL');before=logical(t.ledger);t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
  t.outcome('stability_gate','FAIL')
  with self.assertRaises(HarnessError):t.ledger.verify_stage_success('stability_gate')
  self.assertEqual(logical(t.ledger),before);self.assertEqual(len(t.ledger.stage_records('stability_gate')),120);self.note(snapshot=t.ledger.snapshot(),outcome=t.ledger.event('outcome:stability_gate'))
if __name__=='__main__':
 with (E/'chain_probes.log').open('w') as f:r=unittest.TextTestRunner(stream=f,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Chain))
 (E/'chain_probes.json').write_text(json.dumps(dict(tests=r.testsRun,failures=[{'test':str(t),'traceback':s} for t,s in r.failures],errors=[{'test':str(t),'traceback':s} for t,s in r.errors],observations=OBS),indent=2)+'\n')
 print(r.testsRun,len(r.failures),len(r.errors))
