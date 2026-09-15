"""Regressions for the second NON OK. All approvals and transports are OFFLINE FIXTURES."""
from contextlib import closing, redirect_stdout
from copy import deepcopy
import io
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from studio2.fase03.harness import runtime, test_revisions as fixtures
from studio2.fase03.harness.common import HarnessError, canonical_json, sha256_text
from studio2.fase03.harness.gate_rules import evaluate_stability_gate
from studio2.fase03.harness.ledger import PilotLedger, digest
from studio2.fase03.harness.offline_fixtures import Trial

rp = fixtures.rp
ROOT = fixtures.ROOT


class AlternatePrecedence(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)

    def test_C01_all_started_alternate_states_block_probe_until_pass(self):
        for state in ('bound', 'INTENT', 'FAILED', 'ZERO_TOKEN_PROVEN', 'completed', 'FAIL'):
            with self.subTest(state=state):
                t = Trial(self.home/state)
                t.finish()
                t.bind('alternate_conformity')
                if state != 'bound':
                    for i in range(8 if state in ('completed', 'FAIL') else 1):
                        r = t.reserve(i, 'alternate_conformity')
                        if state == 'FAILED': t.ledger.complete_request(r, status='FAILED')
                        elif state == 'ZERO_TOKEN_PROVEN': t.zero(r)
                        elif state in ('completed', 'FAIL'): t.complete(r, valid=state != 'FAIL')
                    if state == 'FAIL': t.outcome('alternate_conformity', 'FAIL')
                t.ledger = PilotLedger(t.ledger.path, pilot_id=t.ledger.pilot_id)
                before = t.ledger.snapshot()
                with self.assertRaises(HarnessError): t.bind('budget_probe', 3)
                self.assertEqual(t.ledger.snapshot(), before)
                self.assertIsNone(t.ledger.event('frozen_gate'))
        t = Trial(self.home/'positive')
        t.finish(); t.finish('alternate_conformity'); t.finish('budget_probe', 3)
        self.assertEqual(t.ledger.event('outcome:budget_probe')['outcome'], 'PASS')

    def test_C01_alternate_started_after_probe_binding_blocks_reservation(self):
        t = Trial(self.home); t.finish(); t.bind('budget_probe', 3)
        t.bind('alternate_conformity'); t.reserve(0, 'alternate_conformity')
        with self.assertRaises(HarnessError): t.reserve(0, 'budget_probe')
        self.assertEqual(t.ledger.snapshot()['requests_by_stage']['budget_probe'], 0)

    def test_C01_real_process_race_alternate_binding_and_probe_reservation(self):
        t = Trial(self.home); t.finish(); t.bind('budget_probe', 3)
        code = '''import sys
from pathlib import Path
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness.common import HarnessError
t=Trial(sys.argv[1])
try:
    if sys.argv[2]=='alternate':t.bind('alternate_conformity')
    else:t.reserve(0,'budget_probe')
except HarnessError:sys.exit(17)
'''
        procs = [subprocess.Popen([sys.executable, '-c', code, str(self.home), role], cwd=ROOT,
                                 env=dict(os.environ, PYTHONPATH=str(ROOT), PYTHONDONTWRITEBYTECODE='1'))
                 for role in ('alternate', 'probe')]
        self.assertEqual(sorted(p.wait() for p in procs), [0, 17])
        with closing(sqlite3.connect(t.ledger.path)) as c:
            alternate = c.execute("select count(*) from stages where stage='alternate_conformity'").fetchone()[0]
        self.assertEqual(alternate + t.ledger.snapshot()['requests_by_stage']['budget_probe'], 1)


class RunnerCorrections(unittest.TestCase):
    def setUp(self):
        self.t = fixtures.RunnerRevisions()
        self.t.setUp()
        self.addCleanup(self.t.doCleanups)

    def timeout_stub(self, positions):
        t = self.t
        original = rp.Provider
        class Stub(original):
            def call(inner, **kwargs):
                # Positions are first-attempt gate ordinals, after the three probe calls.
                if len(t.consumer_calls)-2 in positions:
                    t.consumer_calls.append('FIXTURE_TRANSPORT_FAILURE')
                    raise TimeoutError('OFFLINE timeout without token evidence')
                return super().call(**kwargs)
        return Stub

    def prepare_gate(self):
        t = self.t
        t.prepare()
        rp.run_budget_stage(t.prepared, t.results, ledger=t.ledger)

    def test_C01_failed_alternate_blocks_cli_probe_without_consumer_sends(self):
        t = self.t
        t.config['d9']['alternate_placement']='pilot'; t.approve_config()  # Explicit D9 fixture choice, before any binding.
        t.prepare(); t.fail_at = 9
        with self.assertRaises(HarnessError): t.producer(stage='alternate_conformity')
        argv = ['fixture', '--execute', '--acknowledge', rp.ACK, '--stage', 'budget',
                '--prepared-dir', str(t.prepared), '--results-dir', str(t.results),
                '--ledger', str(t.ledger.path), '--pilot-id', t.ledger.pilot_id]
        with patch.object(sys, 'argv', argv), self.assertRaises(HarnessError): rp.main()
        self.assertEqual(t.consumer_calls, [])
        self.assertIsNone(t.ledger.event('frozen_gate'))
        r = t.ledger.leaf('alternate_conformity', 'agent_1')['request_id']
        helper = Trial(t.home/'helper'); helper.ledger = t.ledger; helper.zero(r)
        result = t.producer(stage='alternate_conformity', resume=True, retry_requests=[r])
        self.assertEqual(result['provider_requests'], 9)
        self.assertEqual(rp.run_budget_stage(t.prepared, t.results, ledger=t.ledger)['status'], 'FROZEN_FOR_STABILITY_GATE')

    def test_C02_N48_single_timeout_is_119_of_120_and_replays_without_sends(self):
        t = self.t; self.prepare_gate()
        with patch.object(rp, 'Provider', self.timeout_stub({2})):
            result = rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger)
        self.assertEqual(result['provider_requests'], 120)
        self.assertEqual(result['valid_first_attempts'], 119)
        self.assertEqual(result['invalid_first_attempts'], 1)
        self.assertEqual(result['status'], 'R3_REQUIRED_PENDING_FEASIBILITY')
        self.assertEqual(result['divergent_prompt_count'], 1)
        self.assertFalse(result['go_final'])
        self.assertEqual(len(t.consumer_calls), 123)
        self.assertEqual(t.ledger.snapshot()['requests_cumulative'], 131)
        self.assertEqual(t.ledger.snapshot()['transport_calls'], 0)  # retry reserve, not failed originals
        records = t.ledger.stage_records('stability_gate'); invalid = records[1]
        self.assertEqual(len(records), 120)
        self.assertEqual(invalid['record_kind'], 'transport_invalidity')
        self.assertIsNone(invalid['identity_valid'])
        self.assertIsNone(invalid['total_tokens'])
        self.assertIsNone(t.ledger.response(invalid['request_id']))
        self.assertEqual(t.ledger.request(invalid['request_id'])['status'], 'FAILED')
        self.assertEqual(t.ledger.event('outcome:stability_gate')['records_sha256'], digest(records))
        t.ledger.verify_stage_success('stability_gate')
        self.assertFalse(any(e.startswith('suspended:') for e in t.ledger.snapshot()['events']))
        # Evidence can later prove zero tokens; the invalidity and evaluation must not change.
        helper = Trial(t.home/'proof'); helper.ledger = t.ledger; helper.zero(invalid['request_id'])
        self.assertEqual(t.ledger.stage_records('stability_gate'), records)
        with self.assertRaises(HarnessError): helper.retry(invalid['request_id'], 'forbidden-gate-retry')
        t.ledger = PilotLedger(t.ledger.path, pilot_id=t.ledger.pilot_id)
        (t.results/'stability_summary.json').unlink()
        self.assertEqual(rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger, resume=True), result)
        self.assertEqual(len(t.consumer_calls), 123)

    def test_C02_three_timeouts_same_prompt_make_T6_unevaluable(self):
        t = self.t; self.prepare_gate()
        with patch.object(rp, 'Provider', self.timeout_stub({1, 2, 3})):
            result = rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger)
        self.assertEqual(result['valid_first_attempts'], 117)
        self.assertTrue(result['t3_pass'])
        self.assertFalse(result['t6_evaluable'])
        self.assertEqual(len(result['all_invalid_prompt_ids']), 1)
        self.assertEqual(result['status'], 'NO_GO_TECHNICAL')
        self.assertEqual(t.ledger.event('outcome:stability_gate')['outcome'], 'FAIL')
        self.assertEqual(len(t.consumer_calls), 123)

    def test_C02_seven_scattered_timeouts_fail_T3(self):
        t = self.t; self.prepare_gate()
        with patch.object(rp, 'Provider', self.timeout_stub(set(range(1, 20, 3)))):
            result = rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger)
        self.assertEqual(result['valid_first_attempts'], 113)
        self.assertFalse(result['t3_pass'])
        self.assertTrue(result['t6_evaluable'])
        self.assertEqual(result['status'], 'NO_GO_TECHNICAL')
        self.assertEqual(len(t.consumer_calls), 123)

    def test_C02_cli_all_timeouts_are_120_invalid_first_attempts(self):
        t = self.t; self.prepare_gate()
        argv = ['fixture', '--execute', '--acknowledge', rp.ACK, '--stage', 'stability',
                '--prepared-dir', str(t.prepared), '--results-dir', str(t.results),
                '--ledger', str(t.ledger.path), '--pilot-id', t.ledger.pilot_id]
        with patch.object(rp, 'Provider', self.timeout_stub(set(range(1,121)))), patch.object(sys, 'argv', argv), redirect_stdout(io.StringIO()):
            rp.main()
        result = json.loads((t.results/'stability_summary.json').read_text())
        self.assertEqual(result['invalid_first_attempts'], 120)
        self.assertEqual(len(result['all_invalid_prompt_ids']), 40)
        self.assertEqual(len(t.consumer_calls), 123)
        self.assertEqual(t.ledger.snapshot()['durable_responses'], 11)
        self.assertEqual(t.ledger.event('outcome:stability_gate')['outcome'], 'FAIL')

    def test_C02_crash_INTENT_blocks_until_proof_then_enters_T3_without_retry(self):
        t = self.t; self.prepare_gate(); t.consumer_fail = 5
        with self.assertRaises(KeyboardInterrupt): rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger)
        with self.assertRaises(HarnessError): rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger, resume=True)
        self.assertEqual(len(t.consumer_calls), 5)
        spec = t.ledger.binding('stability_gate')['requests'][1]
        request = t.ledger.leaf('stability_gate', spec['logical_id'])
        self.assertIsNone(t.ledger.gate_transport_record(request['request_id']))
        helper = Trial(t.home/'proof'); helper.ledger = t.ledger; helper.zero(request['request_id'])
        t.ledger = PilotLedger(t.ledger.path, pilot_id=t.ledger.pilot_id)
        result = rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger, resume=True)
        self.assertEqual(result['valid_first_attempts'], 119)
        self.assertEqual(result['status'], 'R3_REQUIRED_PENDING_FEASIBILITY')
        self.assertEqual(len(t.consumer_calls), 123)
        self.assertEqual(t.ledger.snapshot()['transport_calls'], 0)

    def test_C02_failure_event_and_status_are_atomic_and_resume_after_journal_crash(self):
        t = self.t; self.prepare_gate()
        original = t.ledger._event
        def rollback(c, name, sha, detail):
            original(c, name, sha, detail)
            if name.startswith('transport_invalidity:'): raise KeyboardInterrupt('before commit')
        with patch.object(t.ledger, '_event', side_effect=rollback), patch.object(rp, 'Provider', self.timeout_stub({1})), self.assertRaises(KeyboardInterrupt):
            rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger)
        r = t.ledger.leaf('stability_gate', t.ledger.binding('stability_gate')['requests'][0]['logical_id'])
        self.assertEqual(r['status'], 'INTENT')
        self.assertIsNone(t.ledger.gate_transport_record(r['request_id']))
        helper = Trial(t.home/'proof'); helper.ledger = t.ledger; helper.zero(r['request_id'])
        original_journal = runtime.export_journal
        def stop(ledger, stage, path):
            original_journal(ledger, stage, path)
            if stage == 'stability_gate' and len(ledger.stage_records(stage)) == 2: raise KeyboardInterrupt('after failure commit')
        with patch.object(runtime, 'export_journal', side_effect=stop), patch.object(rp, 'Provider', self.timeout_stub({2})), self.assertRaises(KeyboardInterrupt):
            rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger, resume=True)
        self.assertEqual(len(t.ledger.stage_records('stability_gate')), 2)
        result = rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger, resume=True)
        self.assertEqual(result['invalid_first_attempts'], 2)
        self.assertEqual(len(t.consumer_calls), 123)

    def test_C02_response_identity_mismatch_cannot_be_masked_as_transport(self):
        t = self.t; self.prepare_gate(); t.consumer_identity = 5
        with patch.object(rp, 'Provider', self.timeout_stub({1})), self.assertRaises(HarnessError):
            rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger)
        row = t.ledger.leaf('stability_gate', t.ledger.binding('stability_gate')['requests'][1]['logical_id'])
        self.assertIsNone(t.ledger.gate_transport_record(row['request_id']))
        self.assertEqual(t.ledger.response(row['request_id'])['raw']['model'], 'WRONG')
        with self.assertRaises(HarnessError): rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger, resume=True)
        self.assertEqual(len(t.consumer_calls), 5)
        self.assertIsNone(t.ledger.event('outcome:stability_gate'))

    def test_C02_transport_event_tamper_or_unobserved_FAILURE_cannot_pass(self):
        t = self.t; self.prepare_gate()
        def stop(ledger, stage, path):
            if stage == 'stability_gate': raise KeyboardInterrupt('after invalidity persisted')
        with patch.object(runtime, 'export_journal', side_effect=stop), patch.object(rp, 'Provider', self.timeout_stub({1})), self.assertRaises(KeyboardInterrupt):
            rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger)
        r = t.ledger.stage_records('stability_gate')[0]
        with closing(sqlite3.connect(t.ledger.path)) as c, c:
            c.execute("update events set detail_json='{}' where event=?", ('transport_invalidity:'+r['request_id'],))
        with self.assertRaises(HarnessError): rp.run_stability_stage(t.prepared, t.results, ledger=t.ledger, resume=True)
        self.assertEqual(len(t.consumer_calls), 4)
        with self.assertRaises(HarnessError): t.ledger.record_event('transport_invalidity:forged', artifact_sha256='a'*64, detail={})

    def test_C02_real_process_death_after_failure_commit_and_new_process_resume(self):
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

    def test_C03_retry_summary_counts_attempts_separately_and_survives_restart(self):
        t = self.t; t.fail_at = 2
        with self.assertRaises(HarnessError): t.producer()
        r = t.ledger.leaf('producer_conformity', 'agent_2')['request_id']
        helper = Trial(t.home/'proof'); helper.ledger = t.ledger; helper.zero(r)
        t.ledger = PilotLedger(t.ledger.path, pilot_id=t.ledger.pilot_id)
        result = t.producer(resume=True, retry_requests=[r])
        self.assertEqual(result['provider_requests'], 9)
        self.assertEqual(result['provider_requests'], len(t.calls))
        self.assertEqual(result['provider_requests'], t.ledger.snapshot()['requests_by_stage']['producer_conformity'])
        self.assertEqual(result['evaluable_calls'], 8)
        self.assertEqual(result['valid_first_attempts'], 8)
        summary = t.home/'results/producer_conformance_fixture_producer_conformity_summary.json'
        self.assertEqual(json.loads(summary.read_text()), result)
        summary.unlink()
        self.assertEqual(t.producer(resume=True), result)
        self.assertEqual(len(t.calls), 9)
        handoff = json.loads((t.home/'results/validated_insight_library_fixture_producer_conformity.json').read_text())
        self.assertEqual(len(handoff['library']), 16)


if __name__ == '__main__': unittest.main()
