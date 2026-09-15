"""Independent D03 audit. SQL and crash injection only on new sacrificial fixtures."""
from pathlib import Path
import sys,os,json,sqlite3,subprocess,shutil,unittest
from contextlib import closing
from unittest.mock import patch
E=Path(__file__).resolve().parent;C=E.parent/'candidate';sys.path.insert(0,str(C))
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness.ledger import PilotLedger,digest
from studio2.fase03.harness.common import HarnessError,canonical_json,sha256_bytes
from studio2.fase03.harness.test_revisions import RunnerRevisions
OBS={}
def logical(l):
 with closing(sqlite3.connect(l.path)) as c:return '\n'.join(c.iterdump())
def sql(l,query,args=()):
 with closing(sqlite3.connect(l.path)) as c,c:c.execute(query,args)
def alter(l,r,fun):
 with closing(sqlite3.connect(l.path)) as c,c:
  old=c.execute('select detail_json from events where event=?',('reconciled:'+r,)).fetchone()[0];d=json.loads(old);fun(d)
  c.execute('update events set detail_json=? where event=?',(canonical_json(d),'reconciled:'+r))
 return dict(before=json.loads(old),after=d)
class Audit(unittest.TestCase):
 def setUp(self):
  self.home=E/'independent_fixtures'/self._testMethodName;self.home.mkdir(parents=True,exist_ok=False)
 def test_V01_real_crash_reconciliation_is_atomic_before_and_after_commit(self):
  results=[]
  for point in ('reconciled','reconciled_integrity','after_state','after_commit'):
   t=Trial(self.home/point);t.finish();t.finish('budget_probe',3);t.bind('stability_gate');r=t.reserve(0,'stability_gate');before=logical(t.ledger)
   code="""import sys,os
from pathlib import Path
from studio2.fase03.harness.offline_fixtures import Trial
t=Trial(Path(sys.argv[1]));point=sys.argv[2];orig=t.ledger._event;save=t.ledger._save_gate_transport_record
def event(c,name,h,d):
 orig(c,name,h,d)
 if name.split(':')[0]==point:os._exit(83)
def invalid(c,r):
 save(c,r)
 if point=='after_state':os._exit(83)
t.ledger._event=event;t.ledger._save_gate_transport_record=invalid
t.zero('stability_gate-0')
os._exit(84)
"""
   run=subprocess.run([sys.executable,'-c',code,str(t.home),point],cwd=C,env=dict(os.environ,PYTHONPATH=str(C),PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
   self.assertEqual(run.returncode,84 if point=='after_commit' else 83,run.stderr)
   t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
   if point!='after_commit':
    self.assertEqual(logical(t.ledger),before);self.assertEqual(t.ledger.request(r)['status'],'INTENT');t.zero(r)
   self.assertIsNotNone(t.ledger.event('reconciled:'+r));self.assertIsNotNone(t.ledger.event('reconciled_integrity:'+r))
   self.assertEqual(t.ledger.request(r)['status'],'ZERO_TOKEN_PROVEN');self.assertEqual(t.ledger.gate_transport_record(r)['record_kind'],'transport_invalidity')
   self.assertEqual(t.ledger.snapshot()['requests_cumulative'],12);self.assertEqual(t.ledger.snapshot()['durable_responses'],11)
   results.append(dict(point=point,returncode=run.returncode,snapshot=t.ledger.snapshot(),rollback_before_commit=point!='after_commit'))
  OBS[self._testMethodName]=results
 def test_V02_acquisition_reads_same_bytes_once_and_seals_opaque_content(self):
  source=Trial(self.home/'source');source.bind();r=source.reserve(0);source.zero(r)
  eb=(source.home/'evidence.json').read_bytes();e=json.loads(eb);e['provider_evidence']={'receipt':'FIXTURE','nested':{'captured':'T0'}}
  eb=json.dumps(e,indent=4).encode();a=json.loads((source.home/'approval.json').read_bytes());a['evidence_sha256']=sha256_bytes(eb);ab=json.dumps(a,indent=2).encode()
  class Once:
   def __init__(self,b):self.b=b;self.calls=0
   def read_bytes(self):
    self.calls+=1
    if self.calls>1:raise AssertionError('reopened input bytes')
    return self.b
  t=Trial(self.home/'target');t.bind();t.reserve(0);ep,ap=Once(eb),Once(ab);t.ledger.reconcile_zero_token(r,evidence_path=ep,approval_path=ap)
  self.assertEqual((ep.calls,ap.calls),(1,1));d=t.ledger.event('reconciled:'+r)
  self.assertEqual(d['artifact_sha256'],sha256_bytes(eb));self.assertEqual(d['approval_sha256'],sha256_bytes(ab));self.assertNotEqual(d['evidence_content_sha256'],d['artifact_sha256'])
  t.bind();before=logical(t.ledger);self.assertEqual(t.ledger.snapshot()['transport_calls'],0)
  alter(t.ledger,r,lambda d:d['evidence']['provider_evidence']['nested'].update(captured='T1'));fault=logical(t.ledger)
  with self.assertRaises(HarnessError):t.bind()
  with self.assertRaises(HarnessError):t.retry(r,'must-not-reserve')
  self.assertEqual(logical(t.ledger),fault);OBS[self._testMethodName]=dict(reads=[ep.calls,ap.calls],file_hash=d['artifact_sha256'],content_hash=d['evidence_content_sha256'],nested_tamper_refused=True)
 def test_V03_failed_gate_reconciled_preserves_invalid_and_holds_real_writer_lock(self):
  t=Trial(self.home/'gate');t.finish();t.finish('budget_probe',3);t.bind('stability_gate');r=t.reserve(0,'stability_gate')
  t.ledger.complete_request(r,status='FAILED',transport_failure=True,detail={'error_type':'TimeoutError','message':'FIXTURE'},latency_ms=1)
  old=t.ledger.event('transport_invalidity:'+r);t.zero(r);self.assertEqual(t.ledger.event('transport_invalidity:'+r),old)
  code="""import sqlite3,sys
c=sqlite3.connect(sys.argv[1],timeout=.05)
try:c.execute('BEGIN IMMEDIATE');print('ACQUIRED');c.rollback()
except sqlite3.OperationalError:print('LOCKED')
finally:c.close()
"""
  seen=[];original=t.ledger._validate_zero_token_evidence
  def validate(*args):
   p=subprocess.run([sys.executable,'-c',code,str(t.ledger.path)],capture_output=True,text=True);self.assertEqual(p.returncode,0,p.stderr);seen.append(p.stdout.strip());return original(*args)
  with patch.object(t.ledger,'_validate_zero_token_evidence',side_effect=validate):self.assertEqual(t.ledger.gate_transport_record(r),old['record'])
  self.assertTrue(seen);self.assertEqual(set(seen),{'LOCKED'})
  p=subprocess.run([sys.executable,'-c',code,str(t.ledger.path)],capture_output=True,text=True);self.assertEqual(p.stdout.strip(),'ACQUIRED')
  proof=alter(t.ledger,r,lambda d:d['evidence'].update(prompt_tokens=1));before=logical(t.ledger)
  with self.assertRaises(HarnessError):t.ledger.gate_transport_record(r)
  with self.assertRaises(HarnessError):t.bind('stability_gate')
  self.assertEqual(logical(t.ledger),before);self.assertEqual(t.ledger.event('transport_invalidity:'+r),old);self.assertIsNone(t.ledger.response(r))
  OBS[self._testMethodName]=dict(writer_during=seen,writer_after=p.stdout.strip(),invalid_unchanged=True,proof=proof,snapshot=t.ledger.snapshot())
 def test_V04_open_producer_corrupt_proof_refuses_before_client_or_retry(self):
  t=RunnerRevisions();t.setUp();self.addCleanup(t.doCleanups);self.addCleanup(lambda:shutil.copytree(t.home,self.home/'captured'));t.fail_at=1
  with self.assertRaises(HarnessError):t.producer()
  r=t.ledger.leaf('producer_conformity','agent_1')['request_id'];h=Trial(self.home/'helper');h.ledger=t.ledger;h.zero(r)
  proof=alter(t.ledger,r,lambda d:d['approval'].update(author='OTHER VALID LOOKING AUTHOR'));before=logical(t.ledger);calls=len(t.calls)
  with patch.object(sys.modules['openai'],'OpenAI',side_effect=AssertionError('client must not be built')) as client:
   with self.assertRaises(HarnessError):t.producer(resume=True,retry_requests=[r])
   client.assert_not_called()
  t.server_mock.assert_not_called();self.assertEqual(len(t.calls),calls);self.assertEqual(logical(t.ledger),before)
  OBS[self._testMethodName]=dict(proof=proof,new_sends=0,client_calls=0,snapshot=t.ledger.snapshot())
 def test_V05_open_stage_quota_fault_cannot_authorize_eighth_retry(self):
  t=Trial(self.home/'open');t.bind();r=t.reserve(0)
  for i in range(7):t.zero(r);r=t.retry(r,'retry-'+str(i))
  t.zero(r);before=logical(t.ledger)
  with self.assertRaises(HarnessError):t.retry(r,'eighth-positive-control')
  self.assertEqual(logical(t.ledger),before);self.assertIsNone(t.ledger.event('remediation_waived'))
  sql(t.ledger,"update requests set quota_kind='base' where request_id='retry-0'");t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
  fault=logical(t.ledger);binding_error=None;retry_error=None
  try:t.bind()
  except HarnessError as ex:binding_error=str(ex)
  try:t.retry(r,'eighth-after-fault')
  except HarnessError as ex:retry_error=str(ex)
  with closing(sqlite3.connect(t.ledger.path)) as c:actual=c.execute('select count(*) from requests where retry_of is not null').fetchone()[0]
  OBS[self._testMethodName]=dict(single_changed_field='retry-0.quota_kind: transport -> base',binding_error=binding_error,retry_error=retry_error,actual_retry_attempts=actual,unchanged_after_refusal=logical(t.ledger)==fault,snapshot=t.ledger.snapshot())
  self.assertIsNotNone(retry_error,'eighth retry must be refused after single normative quota field corruption')
  self.assertEqual(logical(t.ledger),fault)
 def test_V06_real_runner_quota_fault_cannot_send_eighth_retry(self):
  t=RunnerRevisions();t.setUp();self.addCleanup(t.doCleanups);self.addCleanup(lambda:shutil.copytree(t.home,self.home/'captured'));t.fail_at=1
  with self.assertRaises(HarnessError):t.producer()
  h=Trial(self.home/'helper');h.ledger=t.ledger
  for i in range(7):
   r=t.ledger.leaf('producer_conformity','agent_1')['request_id'];h.zero(r);t.fail_at=len(t.calls)+1
   with self.assertRaises(HarnessError):t.producer(resume=True,retry_requests=[r])
  r=t.ledger.leaf('producer_conformity','agent_1')['request_id'];h.zero(r);before=logical(t.ledger);calls=len(t.calls)
  with self.assertRaises(HarnessError):t.producer(resume=True,retry_requests=[r])
  self.assertEqual(len(t.calls),calls);self.assertEqual(logical(t.ledger),before)
  with closing(sqlite3.connect(t.ledger.path)) as c:first=c.execute('select request_id from requests where retry_of is not null order by rowid limit 1').fetchone()[0]
  sql(t.ledger,"update requests set quota_kind='base' where request_id=?",(first,));t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id);fault=logical(t.ledger);t.fail_at=len(t.calls)+1;error=None
  try:t.producer(resume=True,retry_requests=[r])
  except HarnessError as ex:error=str(ex)
  with closing(sqlite3.connect(t.ledger.path)) as c:actual=c.execute('select count(*) from requests where retry_of is not null').fetchone()[0]
  OBS[self._testMethodName]=dict(error=error,single_changed_field=first+'.quota_kind: transport -> base',new_sends=len(t.calls)-calls,actual_retry_attempts=actual,no_waiver=t.ledger.event('remediation_waived') is None,unchanged_after_refusal=logical(t.ledger)==fault,snapshot=t.ledger.snapshot())
  self.assertEqual(len(t.calls),calls,'normative quota fault must not reach producer transport')
  self.assertEqual(logical(t.ledger),fault)
if __name__=='__main__':
 with (E/'independent_d03_probes.log').open('w') as f:r=unittest.TextTestRunner(stream=f,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Audit))
 (E/'independent_d03_probes.json').write_text(json.dumps(dict(tests=r.testsRun,failures=[dict(test=str(t),traceback=s) for t,s in r.failures],errors=[dict(test=str(t),traceback=s) for t,s in r.errors],observations=OBS),indent=2)+'\n')
 print(r.testsRun,len(r.failures),len(r.errors))
