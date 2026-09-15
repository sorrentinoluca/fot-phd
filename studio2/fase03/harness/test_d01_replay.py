"""D01/C01/R04: legacy fixtures are created by the exact old code, never scientific runs."""
from contextlib import closing, redirect_stdout
import io
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

from studio2.fase03.harness import test_revisions as fixtures
from studio2.fase03.harness.common import HarnessError
from studio2.fase03.harness.ledger import PilotLedger, digest
from studio2.fase03.harness.offline_fixtures import Trial

OLD = Path(os.environ.get('FOT_HARNESS_LEGACY_CANDIDATE', '/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate'))
ROOT = fixtures.ROOT
rp = fixtures.rp

LEGACY_LEDGER = '''import sys
from studio2.fase03.harness.offline_fixtures import Trial
t=Trial(sys.argv[1]);t.finish();state=sys.argv[2]
if state!='absent':
 t.bind('alternate_conformity')
 if state!='bound':
  for i in range(8 if state in ('PASS','completed','FAIL') else 1):
   r=t.reserve(i,'alternate_conformity')
   if state=='FAILED':t.ledger.complete_request(r,status='FAILED')
   elif state=='ZERO_TOKEN_PROVEN':t.zero(r)
   elif state in ('PASS','completed','FAIL'):t.complete(r,valid=state!='FAIL')
  if state in ('PASS','FAIL'):t.outcome('alternate_conformity',state)
t.finish('budget_probe',3);t.finish('stability_gate')
'''

LEGACY_RUNNER = '''import sys,os,tempfile,json
from pathlib import Path
from unittest.mock import patch
from studio2.fase03.harness.test_revisions import RunnerRevisions,rp
home=Path(sys.argv[1]);original=tempfile.TemporaryDirectory
with patch.object(tempfile,'TemporaryDirectory',side_effect=lambda **kw:original(dir=home,**kw)):
 t=RunnerRevisions();t.setUp()
(home/'locator').write_text(str(t.home));t.prepare()
if sys.argv[2]=='FAILED':t.fail_at=9
if sys.argv[2]!='absent':
 try:t.producer(stage='alternate_conformity')
 except ValueError:pass
rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
result=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
(home/'old_result.json').write_text(json.dumps(result));os._exit(0)
'''


def logical_database(ledger):
    with closing(sqlite3.connect(ledger.path)) as c:
        return '\n'.join(c.iterdump())


class ReplayPrerequisites(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        observed = subprocess.check_output(['git', '-C', str(OLD), 'rev-parse', 'HEAD', 'HEAD^{tree}'], text=True).splitlines()
        if observed != ['0c8157f23bee49a3a5a2df648525c34706da29d7', 'a1573b49615a875f24ee97f9f1cd4bab399be93d']:
            raise AssertionError('legacy fixture generator must be the exact 0c8157f candidate')
        if subprocess.check_output(['git', '-C', str(OLD), 'status', '--porcelain=v1'], text=True):
            raise AssertionError('legacy fixture generator must be clean')

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)

    def legacy(self, state, *, runner=False):
        home = self.home/state; home.mkdir()
        proc = subprocess.run([sys.executable, '-c', LEGACY_RUNNER if runner else LEGACY_LEDGER, str(home), state],
                              cwd=OLD, env=dict(os.environ, PYTHONPATH=str(OLD), PYTHONDONTWRITEBYTECODE='1'),
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        return Path((home/'locator').read_text()) if runner else home

    def confirmations(self, ledger):
        for stage in ('budget_probe', 'stability_gate'):
            binding = ledger.binding(stage)
            outcome = ledger.event('outcome:'+stage)
            frozen = ledger.event('frozen_gate')['frozen'] if stage == 'budget_probe' else None
            yield stage+'/binding', lambda s=stage,b=binding: ledger.bind_stage(s,b)
            yield stage+'/success', lambda s=stage: ledger.verify_stage_success(s)
            yield stage+'/outcome', lambda s=stage,o=outcome,f=frozen: ledger.record_stage_outcome(
                s, outcome=o['outcome'], artifact_sha256=o['artifact_sha256'], artifact=o['artifact'], frozen=f)
        yield 'frozen', lambda: ledger.authenticate_frozen(ledger.event('frozen_gate')['frozen'])

    def reopen_runner(self, home):
        t = fixtures.RunnerRevisions(); t.setUp(); self.addCleanup(t.doCleanups)
        t.home=home; t.config_path=home/'config.json'; t.prepared=home/'prepared'; t.results=home/'consumer_results'
        t.ledger=PilotLedger(home/'pilot.sqlite3', pilot_id='runner-fixture')
        for module in (fixtures.pp,rp,fixtures.pg):
            t.stack.enter_context(patch.object(module,'PREFLIGHT_CONFIG_PATH',t.config_path))
        return t

    def test_D01_legacy_nonpass_alternate_rejected_by_all_confirmation_entries(self):
        for state in ('bound','INTENT','FAILED','ZERO_TOKEN_PROVEN','completed','FAIL'):
            ledger = Trial(self.legacy(state)).ledger
            before = logical_database(ledger)
            for name, call in self.confirmations(ledger):
                with self.subTest(state=state, entry=name), self.assertRaisesRegex(HarnessError, 'alternate_conformity'):
                    call()
                self.assertEqual(logical_database(ledger), before)
            # Introspection remains available for forensic inspection of rejected state.
            self.assertEqual(ledger.event('outcome:stability_gate')['outcome'], 'PASS')
            self.assertEqual(ledger.snapshot()['requests_by_stage']['stability_gate'], 120)

    def test_D01_valid_legacy_chain_replays_after_gate_without_reopening(self):
        for state in ('absent', 'PASS'):
            ledger = Trial(self.legacy(state)).ledger
            before = logical_database(ledger)
            for name, call in self.confirmations(ledger):
                with self.subTest(state=state, entry=name): call()
            self.assertEqual(logical_database(ledger), before)
            t = Trial(ledger.path.parent)
            with self.assertRaisesRegex(HarnessError, 'closed stage'): t.reserve(0, 'stability_gate', 'second-gate')
            self.assertEqual(logical_database(ledger), before)

    def test_D01_real_legacy_runner_and_cli_refuse_before_server_or_file_writes(self):
        t = self.reopen_runner(self.legacy('FAILED', runner=True))
        before = logical_database(t.ledger)
        file_bytes = {p:p.read_bytes() for p in t.results.iterdir() if p.is_file()}
        for stage, run in [('budget',rp.run_budget_stage),('stability',rp.run_stability_stage)]:
            with self.subTest(entry=stage+'/runner'), self.assertRaisesRegex(HarnessError, 'D9'):
                run(t.prepared, t.results, ledger=t.ledger, resume=True)
            argv=['fixture','--execute','--acknowledge',rp.ACK,'--stage',stage,'--resume',
                  '--prepared-dir',str(t.prepared),'--results-dir',str(t.results),
                  '--ledger',str(t.ledger.path),'--pilot-id',t.ledger.pilot_id]
            with self.subTest(entry=stage+'/CLI'), patch.object(sys,'argv',argv), self.assertRaisesRegex(HarnessError, 'D9'):
                rp.main()
        self.assertEqual(t.consumer_calls, []); t.server_mock.assert_not_called()
        self.assertEqual(logical_database(t.ledger), before)
        self.assertEqual({p:p.read_bytes() for p in t.results.iterdir() if p.is_file()}, file_bytes)
        self.assertEqual(t.ledger.snapshot()['requests_cumulative'], 132)

    def test_D01_real_legacy_D9_blocks_rematerialization_without_rewriting(self):
        t = self.reopen_runner(self.legacy('PASS', runner=True))
        result = json.loads((t.results/'stability_summary.json').read_text())
        frozen = json.loads((t.results/'frozen_gate_config.json').read_text())
        before = logical_database(t.ledger)
        (t.results/'stability_summary.json').unlink()
        # D9 does not backfill authorization over historical scientific runner fixtures.
        # Generic v2 legacy replay is still checked above; this boundary now requires D9.
        with self.assertRaisesRegex(HarnessError, 'D9'):
            rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
        with self.assertRaisesRegex(HarnessError, 'D9'):
            rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
        self.assertFalse((t.results/'stability_summary.json').exists())
        self.assertEqual(t.consumer_calls, []); self.assertEqual(logical_database(t.ledger), before)

    def test_D01_current_remediation_and_C02_invalidity_survive_checked_replay(self):
        t=Trial(self.home/'current'); t.finish(valid=False); t.remediation()
        for i in range(8): t.complete(t.reserve(i,'producer_remediation'))
        t.outcome('producer_remediation'); t.finish('budget_probe',3); t.bind('stability_gate')
        for i in range(120):
            r=t.reserve(i,'stability_gate')
            if i==1: t.ledger.complete_request(r,status='FAILED',transport_failure=True,detail={'error_type':'TimeoutError','message':'OFFLINE FIXTURE'})
            else: t.complete(r)
        t.outcome('stability_gate'); before=logical_database(t.ledger)
        t.ledger=PilotLedger(t.ledger.path,pilot_id=t.ledger.pilot_id)
        for _,call in self.confirmations(t.ledger):call()
        self.assertEqual(logical_database(t.ledger),before)
        self.assertEqual(len(t.ledger.stage_records('stability_gate')),120)
        self.assertEqual(t.ledger.stage_records('stability_gate')[1]['record_kind'],'transport_invalidity')
        self.assertEqual(t.ledger.snapshot()['transport_calls'],0)

    def test_D01_matching_outcome_hash_does_not_skip_durable_record_validation(self):
        ledger=Trial(self.legacy('PASS')).ledger
        outcome=ledger.event('outcome:stability_gate')
        with closing(sqlite3.connect(ledger.path)) as c,c:
            c.execute("update responses set raw_json='{}' where request_id='stability_gate-0'")
        before=logical_database(ledger)
        with self.assertRaisesRegex(HarnessError,'corruption'):
            ledger.record_stage_outcome('stability_gate',outcome='PASS',artifact_sha256=outcome['artifact_sha256'],artifact=outcome['artifact'])
        self.assertEqual(logical_database(ledger),before)

    def test_D01_confirmation_transaction_excludes_concurrent_writer(self):
        ledger=Trial(self.legacy('PASS')).ledger
        for entry in ('verify','frozen'):
            marker=self.home/(entry+'.started'); done=self.home/(entry+'.done'); procs=[]
            code='''import sys
from pathlib import Path
from studio2.fase03.harness.ledger import PilotLedger
Path(sys.argv[2]).write_text('started')
l=PilotLedger(Path(sys.argv[1]),pilot_id='offline-fixture')
l.record_event('note:'+sys.argv[4],artifact_sha256='a'*64,detail={'fixture':True})
Path(sys.argv[3]).write_text('done')
'''
            original=ledger._prerequisites
            def during(c,stage):
                if not procs:
                    procs.append(subprocess.Popen([sys.executable,'-c',code,str(ledger.path),str(marker),str(done),entry],
                                                  cwd=ROOT,env=dict(os.environ,PYTHONPATH=str(ROOT),PYTHONDONTWRITEBYTECODE='1')))
                    deadline=time.monotonic()+5
                    while not marker.exists() and time.monotonic()<deadline:time.sleep(.01)
                    self.assertTrue(marker.exists());self.assertFalse(done.exists())
                return original(c,stage)
            with patch.object(ledger,'_prerequisites',side_effect=during):
                if entry=='verify':ledger.verify_stage_success('stability_gate')
                else:ledger.authenticate_frozen(ledger.event('frozen_gate')['frozen'])
            self.assertEqual(procs[0].wait(timeout=10),0);self.assertTrue(done.exists())


if __name__=='__main__': unittest.main()
