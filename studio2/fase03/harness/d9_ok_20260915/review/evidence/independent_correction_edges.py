"""Independent bounded D9 correction checks; all metadata, approvals and SDK are fixtures."""
import os,sys,json,sqlite3,shutil,unittest
from pathlib import Path
from copy import deepcopy
sys.path.insert(0,os.environ['FOT_D9_TARGET'])
from studio2.fase03.harness import test_revisions as scaffolding
from studio2.fase03.harness.common import HarnessError,sha256_file,sha256_text,canonical_json
from studio2.fase03.harness.ledger import PilotLedger,digest
from unittest.mock import patch
from studio2.fase03 import run_pilot as rp
class Edges(unittest.TestCase):
 def setUp(self):
  self.t=scaffolding.RunnerRevisions();self.t.setUp();self.observations=[]
 def tearDown(self):
  dest=Path(os.environ['EDGE_OUTPUT'])/self._testMethodName
  shutil.copytree(self.t.home,dest)
  (dest/'edge_observations.json').write_text(json.dumps(self.observations,indent=2)+'\n')
  self.t.doCleanups()
 def state(self):
  with sqlite3.connect(self.t.ledger.path) as c:db=list(c.iterdump())
  return db,{str(p.relative_to(self.t.home)):sha256_file(p) for folder in ('results','consumer_results','prepared') for p in (self.t.home/folder).rglob('*') if p.is_file()},len(self.t.calls),len(self.t.consumer_calls)
 def reject(self,fn):
  before=self.state()
  with self.assertRaisesRegex(HarnessError,'tokenizer|chat[_ ]template') as cm:fn()
  self.assertEqual(self.state(),before);self.observations.append({'rejected':str(cm.exception),'db_artifacts_sends_unchanged':True})
 def install_distinct(self):
  t=self.t;self.paths={}
  for role,provider_path in [('122B',t.provider),('27B',t.alternate_provider)]:
   p=t.home/('chat-'+role)/('revision-'+role);p.mkdir(parents=True)
   (p/'tokenizer.json').write_text(json.dumps({'fixture_role':role}));template='FIXTURE TEMPLATE '+role
   (p/'tokenizer_config.json').write_text(json.dumps({'chat_template':template}))
   token=dict(revision=p.name,tokenizer_json_sha256=sha256_file(p/'tokenizer.json'),tokenizer_config_sha256=sha256_file(p/'tokenizer_config.json'),chat_template_sha256=sha256_text(template))
   provider=json.loads(provider_path.read_text());provider['tokenizer']=deepcopy(token);provider_path.write_text(json.dumps(provider))
   service=t.config['d9']['services'][role];service['tokenizer']=deepcopy(token)
   ref=service['documentation'];docpath=Path(ref['path']);doc=json.loads(docpath.read_text());doc['service']={k:deepcopy(v) for k,v in service.items() if k!='documentation'};docpath.write_text(json.dumps(doc));ref['sha256']=sha256_file(docpath)
   t.config['d9']['producer_configs'][role]=sha256_file(provider_path);self.paths[role]=p
  t.config['tokenizer']=deepcopy(t.config['d9']['services']['122B']['tokenizer']);t.config['approved_producer_config_sha256']=list(t.config['d9']['producer_configs'].values());t.config['d9']['alternate_placement']='pilot';t.approve_config()
  self.observations.append({'r4':t.config['d9']['r4_tokenizer'],'122B':t.config['d9']['services']['122B']['tokenizer'],'27B':t.config['d9']['services']['27B']['tokenizer']})
 def test_distinct_role_pins_closed_rebind_and_mutation(self):
  t=self.t;self.install_distinct()
  for role,stage in [('122B','producer_conformity'),('27B','alternate_conformity')]:
   t.snapshot=self.paths[role];self.assertEqual(t.producer(stage=stage)['status'],'PASS')
   b=t.ledger.binding(stage);self.assertEqual(b['tokenizer_snapshot'],str(self.paths[role].resolve()))
   before=self.state();t.ledger.bind_stage(stage,b);self.assertEqual(self.state(),before)
  self.assertEqual(len(t.calls),16)
  alt=t.ledger.binding('alternate_conformity');p=self.paths['27B']/'tokenizer.json';raw=p.read_bytes();p.write_bytes((self.paths['122B']/'tokenizer.json').read_bytes())
  self.reject(lambda:t.ledger.binding('alternate_conformity'))
  self.reject(lambda:t.ledger.bind_stage('alternate_conformity',alt))
  t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id);self.reject(lambda:t.ledger.binding('alternate_conformity'));p.write_bytes(raw)
  self.assertEqual(t.ledger.binding('alternate_conformity'),alt)
 def test_persisted_legacy_missing_field_no_backfill_restart(self):
  t=self.t;t.prepare()
  with patch.object(rp,'execute_request',side_effect=HarnessError('stop')):
   with self.assertRaisesRegex(HarnessError,'stop'):rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
  b=t.ledger.binding('budget_probe');self.assertIn('tokenizer_snapshot',b);del b['tokenizer_snapshot']
  with sqlite3.connect(t.ledger.path) as c:c.execute('UPDATE stages SET binding_json=?,binding_sha256=? WHERE stage=?',(canonical_json(b),digest(b),'budget_probe'))
  self.reject(lambda:t.ledger.binding('budget_probe'))
  t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
  self.reject(lambda:t.ledger.binding('budget_probe'))
  spec=b['requests'][0]
  self.reject(lambda:t.ledger.reserve_request(request_id='legacy',logical_id=spec['logical_id'],model=spec['model'],producer=spec['producer'],stage='budget_probe',stage_run=digest(b)))
  with sqlite3.connect(t.ledger.path) as c:self.assertNotIn('tokenizer_snapshot',json.loads(c.execute("SELECT binding_json FROM stages WHERE stage='budget_probe'").fetchone()[0]))
if __name__=='__main__':unittest.main(verbosity=2)
