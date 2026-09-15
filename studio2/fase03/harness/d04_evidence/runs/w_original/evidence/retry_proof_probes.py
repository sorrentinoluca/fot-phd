"""Independent supplemental audit of durable zero-token proof and replay. Fixtures only."""
from pathlib import Path
import sys,json,sqlite3,shutil,unittest
from contextlib import closing
from unittest.mock import patch
E=Path(__file__).resolve().parent;C=E.parent/'candidate';sys.path.insert(0,str(C))
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness.ledger import PilotLedger,digest
from studio2.fase03.harness.common import HarnessError,canonical_json
from studio2.fase03.harness.test_revisions import RunnerRevisions,rp
OBS={}
def logical(l):
 with closing(sqlite3.connect(l.path)) as c:return '\n'.join(c.iterdump())
def mutate_proof(l,request,change):
 with closing(sqlite3.connect(l.path)) as c,c:
  old=c.execute('select artifact_sha256,detail_json from events where event=?',('reconciled:'+request,)).fetchone()
  detail=json.loads(old[1]);change(detail)
  c.execute('update events set detail_json=? where event=?',(canonical_json(detail),'reconciled:'+request))
 return dict(artifact_sha256=old[0],before=json.loads(old[1]),after=detail)
class Proofs(unittest.TestCase):
 def setUp(self):
  self.home=E/'retry_proof_fixtures'/self._testMethodName;self.home.mkdir(parents=True,exist_ok=False);self.addCleanup(patch.stopall)
 def entries(self,l):
  b=l.binding('stability_gate');o=l.event('outcome:stability_gate');f=l.event('frozen_gate')['frozen'];p=l.binding('producer_conformity')
  return [('gate_binding',lambda:l.bind_stage('stability_gate',b)),('gate_success',lambda:l.verify_stage_success('stability_gate')),('gate_outcome',lambda:l.record_stage_outcome('stability_gate',outcome=o['outcome'],artifact_sha256=o['artifact_sha256'],artifact=o['artifact'])),('frozen',lambda:l.authenticate_frozen(f)),('own_producer_binding',lambda:l.bind_stage('producer_conformity',p))]
 def closed(self,home,hops=1):
  t=Trial(home);t.bind();r=t.reserve(0);base=r
  for i in range(hops):t.zero(r);r=t.retry(r,f'retry-{i}')
  t.complete(r)
  for i in range(1,8):t.complete(t.reserve(i))
  t.outcome('producer_conformity');t.finish('budget_probe',3);t.finish('stability_gate');return t,base
 def test_W01_changed_zero_token_proof_must_not_reconfirm_closed_chain(self):
  source,request=self.closed(self.home/'source');checks=[]
  mutations={
   'positive_prompt_tokens':lambda d:d['evidence'].update(prompt_tokens=1),
   'positive_total_tokens':lambda d:d['evidence'].update(total_tokens=1),
   'missing_completion_tokens':lambda d:d['evidence'].pop('completion_tokens'),
   'boolean_zero_tokens':lambda d:d['evidence'].update(total_tokens=False),
   'missing_provider_receipt':lambda d:d['evidence'].update(provider_request_id=''),
   'missing_provider_evidence':lambda d:d['evidence'].update(provider_evidence=''),
   'missing_approval_author':lambda d:d['approval'].update(author='')}
  for _,call in self.entries(source.ledger):call()
  for name,change in mutations.items():
   t=Trial(self.home/name)
   with closing(sqlite3.connect(source.ledger.path)) as src,closing(sqlite3.connect(t.ledger.path)) as dst:src.backup(dst)
   proof=mutate_proof(t.ledger,request,change);before=logical(t.ledger);errors=[]
   for entry,call in self.entries(t.ledger):
    error=None
    try:call()
    except HarnessError as exc:error=str(exc)
    errors.append(dict(entry=entry,error=error))
   self.assertEqual(logical(t.ledger),before)
   checks.append(dict(fault=name,proof=proof,checks=errors,snapshot=t.ledger.snapshot()))
  OBS[self._testMethodName]=dict(checks=checks)
  self.assertTrue(all(x['error'] for r in checks for x in r['checks']),'The stored proof must still satisfy zero-token evidence and approval requirements during reconfirmation')
 def test_W02_real_runner_rejects_positive_tokens_in_durable_retry_proof(self):
  t=RunnerRevisions();t.setUp();self.addCleanup(t.doCleanups);self.addCleanup(lambda:shutil.copytree(t.home,self.home/'captured',dirs_exist_ok=True))
  t.fail_at=2
  with self.assertRaises(HarnessError):t.producer()
  request=t.ledger.leaf('producer_conformity','agent_2')['request_id'];helper=Trial(self.home/'helper');helper.ledger=t.ledger;helper.zero(request)
  producer=t.producer(resume=True,retry_requests=[request]);self.assertEqual(producer['provider_requests'],9);self.assertEqual(producer['evaluable_calls'],8)
  t.prepare(producer=False);rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger);old=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
  proof=mutate_proof(t.ledger,request,lambda d:d['evidence'].update(prompt_tokens=1,total_tokens=1))
  before=logical(t.ledger);n=len(t.consumer_calls);t.server_mock.reset_mock();error=None;result=None
  t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
  try:result=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
  except HarnessError as exc:error=str(exc)
  self.assertEqual(logical(t.ledger),before);self.assertEqual(len(t.consumer_calls),n)
  OBS[self._testMethodName]=dict(error=error,result=result,unchanged_valid_result=result==old,proof=proof,new_sends=len(t.consumer_calls)-n,server_calls=t.server_mock.call_count,snapshot=t.ledger.snapshot())
  self.assertIsNotNone(error,'A proof with positive tokens must not justify a retry in the reconfirmed producer chain')
 def test_W03_multihop_retry_valid_then_missing_proof_rejected_same_instance(self):
  t,request=self.closed(self.home/'multi',hops=2);before=logical(t.ledger)
  for _,call in self.entries(t.ledger):call()
  self.assertEqual(logical(t.ledger),before);self.assertEqual(t.ledger.snapshot()['requests_by_stage']['producer_conformity'],10)
  with closing(sqlite3.connect(t.ledger.path)) as c,c:c.execute('delete from events where event=?',('reconciled:retry-0',))
  before=logical(t.ledger)
  for _,call in self.entries(t.ledger):
   with self.assertRaises(HarnessError):call()
  self.assertEqual(logical(t.ledger),before);OBS[self._testMethodName]=dict(snapshot=t.ledger.snapshot(),same_instance_rejected=True)
 def test_W04_same_instance_does_not_cache_predecessor_validation(self):
  t,request=self.closed(self.home/'cache')
  for _,call in self.entries(t.ledger):call()
  with closing(sqlite3.connect(t.ledger.path)) as c,c:c.execute("update responses set raw_json='{}' where request_id='producer_conformity-1'")
  before=logical(t.ledger)
  for _,call in self.entries(t.ledger):
   with self.assertRaisesRegex(HarnessError,'corruption'):call()
  self.assertEqual(logical(t.ledger),before);OBS[self._testMethodName]=dict(snapshot=t.ledger.snapshot(),same_instance_rejected=True)
if __name__=='__main__':
 with (E/'retry_proof_probes.log').open('w') as f:r=unittest.TextTestRunner(stream=f,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Proofs))
 (E/'retry_proof_probes.json').write_text(json.dumps(dict(tests=r.testsRun,failures=[{'test':str(t),'traceback':s} for t,s in r.failures],errors=[{'test':str(t),'traceback':s} for t,s in r.errors],observations=OBS),indent=2)+'\n')
 print(r.testsRun,len(r.failures),len(r.errors))
