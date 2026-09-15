"""Independent D04 decision-boundary probes. Offline sacrificial fixtures only."""
from pathlib import Path
import sys,os,json,sqlite3,subprocess,time,unittest
from contextlib import closing
from unittest.mock import patch,Mock
E=Path(__file__).resolve().parent;C=E.parent/'candidate';sys.path.insert(0,str(C))
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness.ledger import PilotLedger,digest
from studio2.fase03.harness.common import HarnessError
from studio2.fase03.harness.runtime import execute_request
OBS={}
def logical(l):
 with closing(sqlite3.connect(l.path)) as c:return '\n'.join(c.iterdump())
def sql(l,q,v=()):
 with closing(sqlite3.connect(l.path)) as c,c:c.execute(q,v)
def triplet(t,ids,prefix):
 out=[]
 for i,r in enumerate(ids):
  row=t.ledger.request(r);out.append(dict(request_id=prefix+str(i),retry_of=r,logical_id=row['logical_id'],model=row['model'],producer=row['producer'],stage_run=row['stage_run'],condition=json.loads(row['identity_json'])['condition']))
 return out
LOCK_CODE="""import sqlite3,sys
c=sqlite3.connect(sys.argv[1],timeout=.04)
try:c.execute('BEGIN IMMEDIATE');print('ACQUIRED');c.rollback()
except sqlite3.OperationalError:print('LOCKED')
finally:c.close()
"""
class Edges(unittest.TestCase):
 def setUp(self):
  self.home=E/'decision_edge_fixtures'/self._testMethodName;self.home.mkdir(parents=True,exist_ok=False)
 def fixture(self,route):
  t=Trial(self.home/route)
  if route=='remediation':
   t.finish(valid=False);t.remediation();action=lambda:t.reserve(0,'producer_remediation')
  elif route=='triplet':
   t.finish();t.bind('budget_probe',3);ids=[t.reserve(i,'budget_probe') for i in range(3)]
   for r in ids:t.zero(r)
   action=lambda:t.ledger.reserve_probe_transport_triplet(triplet(t,ids,'retry-'))
  else:
   t.bind();r=t.reserve(0)
   if route=='new_binding':action=lambda:t.bind('alternate_conformity')
   elif route=='resume_binding':action=t.bind
   elif route=='base':action=lambda:t.reserve(1)
   elif route=='retry':t.zero(r);action=lambda:t.retry(r,'retry-0')
  return t,action
 def test_U01_every_decision_reuses_validator_under_real_lock(self):
  results=[]
  for route in ('new_binding','resume_binding','base','retry','remediation','triplet'):
   t,action=self.fixture(route);seen=[];original=t.ledger._validate_attempts
   def validated(c,b,rows):
    self.assertTrue(c.in_transaction);p=subprocess.run([sys.executable,'-c',LOCK_CODE,str(t.ledger.path)],capture_output=True,text=True)
    self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(p.stdout.strip(),'LOCKED');seen.append(dict(stages=sorted({r['stage'] for r in rows}),transaction=True,writer=p.stdout.strip()));return original(c,b,rows)
   with patch.object(t.ledger,'_validate_attempts',side_effect=validated):action()
   self.assertTrue(seen,route);p=subprocess.run([sys.executable,'-c',LOCK_CODE,str(t.ledger.path)],capture_output=True,text=True);self.assertEqual(p.stdout.strip(),'ACQUIRED')
   results.append(dict(route=route,checks=seen,writer_after=p.stdout.strip(),snapshot=t.ledger.snapshot()))
  OBS[self._testMethodName]=results
 def test_U02_mid_triplet_fault_rolls_back_all_then_legal_retry_succeeds(self):
  t,action=self.fixture('triplet');before=logical(t.ledger);original=t.ledger._insert_intent;calls=[]
  def insert(c,**kw):
   original(c,**kw);calls.append(kw['request_id'])
   if len(calls)==2:raise HarnessError('INJECTED after second insertion')
  with patch.object(t.ledger,'_insert_intent',side_effect=insert):
   with self.assertRaisesRegex(HarnessError,'INJECTED'):action()
  self.assertEqual(len(calls),2);self.assertEqual(logical(t.ledger),before);t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id);self.assertEqual(logical(t.ledger),before)
  action();self.assertEqual(t.ledger.snapshot()['transport_calls'],3);self.assertEqual(t.ledger.snapshot()['requests_cumulative'],14)
  OBS[self._testMethodName]=dict(injected_after=calls,rollback=True,snapshot=t.ledger.snapshot())
 def test_U03_two_processes_compete_for_last_shared_waived_transport(self):
  t=Trial(self.home/'shared');t.bind();t.bind('alternate_conformity');t.ledger.waive_remediation(approval_sha256='a'*64);last=[]
  for stage in ('producer_conformity','alternate_conformity'):
   r=t.reserve(0,stage)
   for i in range(7):t.zero(r);r=t.retry(r,stage+'-retry-'+str(i))
   t.zero(r);last.append(r)
  self.assertEqual(t.ledger.snapshot()['transport_calls'],14)
  gate=self.home/'go';code="""import sys,time,json
from pathlib import Path
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness.common import HarnessError
t=Trial(Path(sys.argv[1]));Path(sys.argv[4]).write_text('ready')
while not Path(sys.argv[5]).exists():time.sleep(.01)
try:t.retry(sys.argv[2],sys.argv[3]);print(json.dumps({'accepted':True}))
except HarnessError as e:print(json.dumps({'accepted':False,'error':str(e)}))
"""
  procs=[]
  for i,r in enumerate(last):
   ready=self.home/('ready-'+str(i));procs.append(subprocess.Popen([sys.executable,'-c',code,str(t.home),r,'last-slot-'+str(i),str(ready),str(gate)],cwd=C,env=dict(os.environ,PYTHONPATH=str(C),PYTHONDONTWRITEBYTECODE='1'),stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True))
  deadline=time.monotonic()+10
  while len(list(self.home.glob('ready-*')))<2 and time.monotonic()<deadline:time.sleep(.01)
  self.assertEqual(len(list(self.home.glob('ready-*'))),2);gate.write_text('go');results=[]
  for p in procs:
   out,err=p.communicate(timeout=20);self.assertEqual(p.returncode,0,err);results.append(json.loads(out))
  self.assertEqual(sum(r['accepted'] for r in results),1);self.assertEqual(t.ledger.snapshot()['transport_calls'],15);self.assertEqual(t.ledger.snapshot()['requests_cumulative'],17)
  OBS[self._testMethodName]=dict(processes=results,snapshot=t.ledger.snapshot())
 def test_U04_other_open_stage_orphan_unknown_stage_or_missing_proof_refused(self):
  results=[]
  for fault in ('unknown_stage','missing_parent','missing_proof'):
   t=Trial(self.home/fault);t.bind();t.reserve(0);t.bind('alternate_conformity');r=t.reserve(0,'alternate_conformity');t.zero(r);child=t.retry(r,'alternate-retry')
   t.bind();t.reserve(1)
   if fault=='unknown_stage':sql(t.ledger,"update requests set stage='UNKNOWN' where request_id=?",(child,))
   elif fault=='missing_parent':sql(t.ledger,"update requests set retry_of='MISSING' where request_id=?",(child,))
   else:sql(t.ledger,'delete from events where event=?',('reconciled_integrity:'+r,))
   before=logical(t.ledger)
   for restart in (False,True):
    if restart:t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
    for action in (t.bind,lambda:t.reserve(2)):
     with self.assertRaises(HarnessError):action()
     self.assertEqual(logical(t.ledger),before)
   results.append(dict(fault=fault,refused_before_and_after_restart=True,snapshot=t.ledger.snapshot()))
  OBS[self._testMethodName]=results
 def test_U05_execute_request_without_prior_rebind_rejects_cross_stage_quota(self):
  t=Trial(self.home/'runtime');t.bind();t.reserve(0);t.bind('alternate_conformity');r=t.reserve(0,'alternate_conformity')
  sql(t.ledger,"update requests set quota_kind='transport' where request_id=?",(r,));before=logical(t.ledger);spec=t.ledger.binding('producer_conformity')['requests'][1]
  send=Mock(side_effect=AssertionError('must not reach transport'));journal=self.home/'must-not-exist.jsonl'
  with patch.object(t.ledger,'snapshot',side_effect=AssertionError('diagnostic dump must not authorize')):
   with self.assertRaises(HarnessError):execute_request(ledger=t.ledger,stage='producer_conformity',spec=spec,transport=send,evaluate=Mock(),expected_identity={},journal_path=journal)
  send.assert_not_called();self.assertFalse(journal.exists());self.assertEqual(logical(t.ledger),before)
  OBS[self._testMethodName]=dict(new_sends=0,journal_created=False,diagnostic_snapshot_not_used=True,unchanged=True,snapshot=t.ledger.snapshot())
if __name__=='__main__':
 with (E/'decision_edge_probes.log').open('w') as f:r=unittest.TextTestRunner(stream=f,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Edges))
 (E/'decision_edge_probes.json').write_text(json.dumps(dict(tests=r.testsRun,failures=[dict(test=str(t),traceback=s) for t,s in r.failures],errors=[dict(test=str(t),traceback=s) for t,s in r.errors],observations=OBS),indent=2)+'\n');print(r.testsRun,len(r.failures),len(r.errors))
