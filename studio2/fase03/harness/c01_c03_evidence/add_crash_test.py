from pathlib import Path
p=Path('/Users/luker/fot-tep-harness-0310-c01-c03/studio2/fase03/harness/test_c01_c03.py');s=p.read_text()
anchor="    def test_C03_retry_summary_counts_attempts_separately_and_survives_restart(self):"
method='''    def test_C02_real_process_death_after_failure_commit_and_new_process_resume(self):
        locator = self.t.home/'crash_home.txt'
        crash_code = """import os,sys
from pathlib import Path
from unittest.mock import patch
from studio2.fase03.harness.test_revisions import RunnerRevisions,rp
from studio2.fase03.harness import runtime
t=RunnerRevisions();t.setUp();Path(sys.argv[1]).write_text(str(t.home))
t.prepare();rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
original=rp.Provider
class Fail(original):
    def call(self,**kw):
        if len(t.consumer_calls)==4:
            t.consumer_calls.append('TRANSPORT');raise TimeoutError('OFFLINE process crash after observation')
        return super().call(**kw)
def stop(ledger,stage,path):
    if stage=='stability_gate' and len(ledger.stage_records(stage))==2:os._exit(27)
with patch.object(rp,'Provider',Fail),patch.object(runtime,'export_journal',side_effect=stop):
    rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
os._exit(31)
"""
        proc = subprocess.run([sys.executable, '-c', crash_code, str(locator)], cwd=ROOT,
                              env=dict(os.environ, PYTHONPATH=str(ROOT), PYTHONDONTWRITEBYTECODE='1'), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 27, proc.stderr)
        home = Path(locator.read_text()); self.addCleanup(shutil.rmtree, home)
        ledger = PilotLedger(home/'pilot.sqlite3', pilot_id='runner-fixture')
        records = ledger.stage_records('stability_gate')
        self.assertEqual(len(records), 2)
        self.assertEqual(records[1]['record_kind'], 'transport_invalidity')
        self.assertIsNone(ledger.response(records[1]['request_id']))
        self.assertEqual(ledger.snapshot()['requests_cumulative'], 13)
        resume_code = """import sys,json
from pathlib import Path
from unittest.mock import patch
from studio2.fase03.harness.test_revisions import RunnerRevisions,rp,pp,pg
from studio2.fase03.harness.ledger import PilotLedger
t=RunnerRevisions();t.setUp()
# Fresh process, same approved paths/ledger. Fixture boundary stubs alone are recreated.
t.home=Path(sys.argv[1]);t.config_path=t.home/'config.json'
t.config=json.loads(t.config_path.read_text());t.prepared=t.home/'prepared';t.results=t.home/'consumer_results'
t.ledger=PilotLedger(t.home/'pilot.sqlite3',pilot_id='runner-fixture')
for module in (pp,rp,pg):t.stack.enter_context(patch.object(module,'PREFLIGHT_CONFIG_PATH',t.config_path))
result=rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger,resume=True)
print(json.dumps(dict(result=result,new_stub_sends=len(t.consumer_calls),snapshot=t.ledger.snapshot())))
t.doCleanups()
"""
        proc = subprocess.run([sys.executable, '-c', resume_code, str(home)], cwd=ROOT,
                              env=dict(os.environ, PYTHONPATH=str(ROOT), PYTHONDONTWRITEBYTECODE='1'), capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        observation = json.loads(proc.stdout)
        self.assertEqual(observation['new_stub_sends'], 118)
        self.assertEqual(observation['result']['invalid_first_attempts'], 1)
        self.assertEqual(observation['result']['status'], 'R3_REQUIRED_PENDING_FEASIBILITY')
        self.assertEqual(observation['snapshot']['requests_cumulative'], 131)

'''
assert anchor in s;s=s.replace(anchor,method+anchor);p.write_text(s)
