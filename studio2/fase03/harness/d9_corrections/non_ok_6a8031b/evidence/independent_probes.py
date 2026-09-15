"""Independent D9 probes; synthetic RunnerRevisions scaffolding, no live services."""
import os,sys,json,sqlite3,shutil,unittest
from pathlib import Path
from copy import deepcopy
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,os.environ.get('FOT_D9_TARGET',str(ROOT/'work/candidate')))
from studio2.fase03.harness import test_revisions as scaffolding
from studio2.fase03.harness.common import HarnessError,sha256_file,canonical_json
from studio2.fase03.harness.ledger import PilotLedger,digest
from studio2.fase03 import run_pilot as rp
EV=Path(__file__).parent
class Independent(unittest.TestCase):
 def setUp(self):
  self.t=scaffolding.RunnerRevisions();self.t.setUp()
 def tearDown(self):
  dest=EV/os.environ.get('PROBE_OUTPUT','probe_fixtures')/self._testMethodName
  if dest.exists():raise RuntimeError('refuse overwrite')
  shutil.copytree(self.t.home,dest)
  (dest/'observations.json').write_text(json.dumps({'producer_stub_calls':len(self.t.calls),'consumer_stub_calls':len(self.t.consumer_calls),'snapshot':self.t.ledger.snapshot()},indent=2))
  self.t.doCleanups()
 def metadata(self,value):
  t=self.t;p=Path(t.config['d9']['services']['122B']['documentation']['path']);doc=json.loads(p.read_text());doc['weights_revision']=value;p.write_text(json.dumps(doc));t.config['d9']['services']['122B']['documentation']['sha256']=sha256_file(p);t.approve_config()
 def test_U01_positive_metadata_and_resume(self):
  t=self.t;self.metadata('fixture-immutable-revision-123');self.assertEqual(t.producer()['status'],'PASS');t.producer(resume=True);self.assertEqual(len(t.calls),8)
 def test_U02_exact_pending_metadata_refuses(self):
  self.metadata('PENDING')
  with self.assertRaisesRegex(HarnessError,'missing service metadata: weights_revision'):self.t.producer()
  self.assertEqual(self.t.calls,[]);self.assertEqual(self.t.ledger.snapshot()['requests_cumulative'],0)
 def test_U03_whitespace_pending_metadata_must_refuse(self):
  self.metadata(' PENDING ')
  with self.assertRaisesRegex(HarnessError,'missing service metadata: weights_revision'):self.t.producer()
  self.assertEqual(self.t.calls,[]);self.assertEqual(self.t.ledger.snapshot()['requests_cumulative'],0)
 def prepare_binding(self):
  t=self.t;t.prepare()
  with patch.object(rp,'execute_request',side_effect=HarnessError('probe stop before reserve')):
   with self.assertRaisesRegex(HarnessError,'probe stop before reserve'):rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
  return t.ledger.binding('budget_probe')
 def reserve(self,binding,ledger=None):
  l=ledger or self.t.ledger;s=binding['requests'][0]
  return l.reserve_request(request_id='independent-consumer-intent',logical_id=s['logical_id'],model=s['model'],producer=s['producer'],stage='budget_probe',stage_run=digest(binding))
 def test_U04_positive_direct_reserve(self):
  b=self.prepare_binding();self.reserve(b);self.assertEqual(self.t.ledger.snapshot()['requests_cumulative'],9);self.assertEqual(self.t.consumer_calls,[])
 def test_U05_missing_r4_snapshot_direct_reserve_must_refuse(self):
  t=self.t;b=self.prepare_binding();(t.snapshot/'tokenizer.json').unlink()
  with self.assertRaisesRegex(HarnessError,'tokenizer'):self.reserve(b)
  self.assertEqual(t.ledger.snapshot()['requests_cumulative'],8)
 def test_U06_missing_r4_snapshot_restart_reserve_must_refuse(self):
  t=self.t;b=self.prepare_binding();(t.snapshot/'tokenizer.json').unlink();l=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
  with self.assertRaisesRegex(HarnessError,'tokenizer'):self.reserve(b,l)
  self.assertEqual(l.snapshot()['requests_cumulative'],8)
 def test_U07_missing_snapshot_ordinary_runner_refuses(self):
  t=self.t;self.prepare_binding();(t.snapshot/'tokenizer.json').unlink()
  with self.assertRaisesRegex(HarnessError,'tokenizer'):rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
  self.assertEqual(t.ledger.snapshot()['requests_cumulative'],8);self.assertEqual(t.consumer_calls,[])
 def test_U08_document_change_other_stage_reservation_refuses(self):
  t=self.t;b=self.prepare_binding();p=Path(t.config['d9']['services']['27B']['documentation']['path']);p.write_bytes(p.read_bytes()+b' ')
  with self.assertRaisesRegex(HarnessError,'bytes changed'):self.reserve(b)
  self.assertEqual(t.ledger.snapshot()['requests_cumulative'],8)
if __name__=='__main__':unittest.main(verbosity=2)
