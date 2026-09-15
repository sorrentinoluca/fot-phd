"""D02: deliberate database faults in sacrificial offline fixtures, never scientific inputs."""
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from studio2.fase03.harness.common import HarnessError, canonical_json, sha256_text
from studio2.fase03.harness.ledger import PilotLedger, digest
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness.test_d01_replay import logical_database
from studio2.fase03.harness import test_revisions as fixtures

rp = fixtures.rp


class DurablePredecessors(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.addClassCleanup(cls.tmp.cleanup)
        cls.source = Trial(Path(cls.tmp.name)/'valid')
        cls.source.finish(); cls.source.finish('alternate_conformity')
        cls.source.finish('budget_probe', 9); cls.source.finish('stability_gate')

    def setUp(self):
        self.tmp_case = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp_case.cleanup)
        self.home = Path(self.tmp_case.name)
        self.serial = 0

    def copy(self):
        self.serial += 1
        t = Trial(self.home/str(self.serial))
        with closing(sqlite3.connect(self.source.ledger.path)) as src, closing(sqlite3.connect(t.ledger.path)) as dst:
            src.backup(dst)
        return t

    def fault(self, ledger, sql, params=()):
        with closing(sqlite3.connect(ledger.path)) as c, c:
            c.execute(sql, params)
        return PilotLedger(ledger.path, pilot_id=ledger.pilot_id)

    def entries(self, ledger, stage):
        binding = ledger.binding(stage); outcome = ledger.event('outcome:'+stage)
        frozen = ledger.event('frozen_gate')['frozen'] if stage == 'budget_probe' else None
        return [(stage+'/binding', lambda: ledger.bind_stage(stage, binding)),
                (stage+'/success', lambda: ledger.verify_stage_success(stage)),
                (stage+'/outcome', lambda: ledger.record_stage_outcome(stage, outcome=outcome['outcome'],
                    artifact_sha256=outcome['artifact_sha256'], artifact=outcome['artifact'], frozen=frozen))]

    def rejected(self, ledger, own_stage=None):
        checks = self.entries(ledger, 'stability_gate')
        checks.append(('freeze', lambda: ledger.authenticate_frozen(ledger.event('frozen_gate')['frozen'])))
        if own_stage: checks += self.entries(ledger, own_stage)
        before = logical_database(ledger)
        for name, call in checks:
            with self.subTest(entry=name), self.assertRaises(HarnessError): call()
            self.assertEqual(logical_database(ledger), before)
        # Normative refusal preserves the stored event and the forensic counters.
        self.assertEqual(ledger.event('outcome:stability_gate')['outcome'], 'PASS')

    def test_D02_raw_and_record_hash_faults_reject_all_confirmation_entries(self):
        for stage in ('producer_conformity','alternate_conformity','budget_probe'):
            for column in ('raw_json','record_json'):
                with self.subTest(stage=stage, column=column):
                    t = self.copy()
                    for _, call in self.entries(t.ledger, 'stability_gate'): call()
                    ledger = self.fault(t.ledger, f"UPDATE responses SET {column}='{{}}' WHERE request_id=?", (stage+'-0',))
                    with self.assertRaises(HarnessError): ledger.response(stage+'-0')
                    self.rejected(ledger, stage)

    def test_D02_missing_coverage_raw_or_evaluation_rejects_predecessors(self):
        for stage in ('producer_conformity','alternate_conformity','budget_probe'):
            for sql in ('DELETE FROM requests WHERE request_id=?', 'DELETE FROM responses WHERE request_id=?',
                        'UPDATE responses SET record_json=NULL,record_sha256=NULL WHERE request_id=?'):
                with self.subTest(stage=stage, fault=sql):
                    t = self.copy(); ledger = self.fault(t.ledger, sql, (stage+'-0',))
                    self.rejected(ledger, stage)

    def test_D02_probe_cannot_shrink_to_an_allowed_prefix_after_closure(self):
        t = self.copy()
        # Six remaining bases are a legal *new* probe size, but not this closed nine-case result.
        ledger = self.fault(t.ledger, "DELETE FROM requests WHERE stage='budget_probe' AND logical_id IN ('case-6','case-7','case-8')")
        self.assertEqual(ledger.snapshot()['requests_by_stage']['budget_probe'], 6)
        self.rejected(ledger, 'budget_probe')

    def test_D02_record_digest_binding_and_frozen_evidence_are_reauthenticated(self):
        for stage in ('producer_conformity','alternate_conformity','budget_probe'):
            t = self.copy(); record = t.ledger.response(stage+'-0')['record']
            record['raw_output'] = 'CORRUPTED FIXTURE WITH RECOMPUTED RECORD HASH'
            text = canonical_json(record)
            ledger = self.fault(t.ledger, 'UPDATE responses SET record_json=?,record_sha256=? WHERE request_id=?',
                                (text, sha256_text(text), stage+'-0'))
            self.rejected(ledger, stage)  # Old closure digest still binds the original record.
        for event, key, replacement in [('outcome:alternate_conformity','records_sha256','f'*64),
                                        ('outcome:producer_conformity','artifact',{}),
                                        ('frozen_gate','frozen',{'generation':{'max_tokens':999}})]:
            t = self.copy()
            with closing(sqlite3.connect(t.ledger.path)) as c:
                detail = json.loads(c.execute('SELECT detail_json FROM events WHERE event=?',(event,)).fetchone()[0])
            detail[key] = replacement
            self.rejected(self.fault(t.ledger, 'UPDATE events SET detail_json=? WHERE event=?', (canonical_json(detail),event)))
        t = self.copy()
        self.rejected(self.fault(t.ledger, "UPDATE requests SET identity_json='{}' WHERE request_id='alternate_conformity-0'"))

    def test_D02_retry_replay_preserves_nine_attempts_and_rejects_missing_ancestor(self):
        t = Trial(self.home/'retry'); t.bind()
        r = t.reserve(0); t.zero(r); t.complete(t.retry(r, 'retry-0'))
        for i in range(1,8): t.complete(t.reserve(i))
        t.outcome('producer_conformity'); t.finish('budget_probe',3); t.finish('stability_gate')
        before = logical_database(t.ledger)
        for stage in ('producer_conformity','budget_probe','stability_gate'):
            for _, call in self.entries(t.ledger, stage): call()
        self.assertEqual(logical_database(t.ledger), before)
        self.assertEqual(t.ledger.snapshot()['requests_by_stage']['producer_conformity'], 9)
        ledger = self.fault(t.ledger, 'DELETE FROM events WHERE event=?', ('reconciled:'+r,))
        self.rejected(ledger, 'producer_conformity')

    def test_D02_remediation_and_new_probe_validate_durable_active_producer(self):
        t = Trial(self.home/'remediation'); t.finish(valid=False); t.remediation()
        for i in range(8): t.complete(t.reserve(i,'producer_remediation'))
        t.outcome('producer_remediation'); t.finish('budget_probe',3); t.finish('stability_gate')
        self.rejected(self.fault(t.ledger, "UPDATE responses SET raw_json='{}' WHERE request_id='producer_remediation-0'"), 'producer_remediation')
        # A new probe cannot proceed through the same corrupted predecessor either.
        t = Trial(self.home/'new-probe'); t.finish()
        t.ledger = self.fault(t.ledger, "UPDATE responses SET raw_json='{}' WHERE request_id='producer_conformity-0'")
        before = logical_database(t.ledger)
        with self.assertRaisesRegex(HarnessError, 'corruption'): t.bind('budget_probe',3)
        self.assertEqual(logical_database(t.ledger), before)

    def test_D02_runner_and_CLI_resume_refuse_before_server_calls_or_output_writes(self):
        t = fixtures.RunnerRevisions(); t.setUp(); self.addCleanup(t.doCleanups)
        t.config['d9']['alternate_placement'] = 'pilot'
        t.approve_config()
        t.prepare(); t.producer(stage='alternate_conformity')
        rp.run_budget_stage(t.prepared,t.results,ledger=t.ledger)
        rp.run_stability_stage(t.prepared,t.results,ledger=t.ledger)
        request = t.ledger.leaf('alternate_conformity','agent_1')['request_id']
        t.ledger = self.fault(t.ledger, "UPDATE responses SET raw_json='{}' WHERE request_id=?", (request,))
        before = logical_database(t.ledger)
        files = {p:p.read_bytes() for p in t.results.rglob('*') if p.is_file()}
        calls = len(t.consumer_calls); t.server_mock.reset_mock()
        for stage, run in [('budget',rp.run_budget_stage),('stability',rp.run_stability_stage)]:
            with self.subTest(entry=stage+'/runner'), self.assertRaisesRegex(HarnessError,'corruption'):
                run(t.prepared,t.results,ledger=t.ledger,resume=True)
            argv = ['fixture','--execute','--acknowledge',rp.ACK,'--stage',stage,'--resume',
                    '--prepared-dir',str(t.prepared),'--results-dir',str(t.results),
                    '--ledger',str(t.ledger.path),'--pilot-id',t.ledger.pilot_id]
            with self.subTest(entry=stage+'/CLI'), patch.object(sys,'argv',argv), self.assertRaisesRegex(HarnessError,'corruption'):
                rp.main()
        self.assertEqual(len(t.consumer_calls), calls); t.server_mock.assert_not_called()
        self.assertEqual(logical_database(t.ledger), before)
        self.assertEqual({p:p.read_bytes() for p in t.results.rglob('*') if p.is_file()}, files)
        self.assertEqual(t.ledger.snapshot()['requests_cumulative'],139)

    def test_D02_durable_predecessor_reads_hold_the_confirmation_lock(self):
        ledger = self.copy().ledger
        code = '''import sqlite3,sys
c=sqlite3.connect(sys.argv[1],timeout=.1)
try:c.execute('BEGIN IMMEDIATE');c.rollback();print('unlocked')
except sqlite3.OperationalError as e:print(str(e))
finally:c.close()
'''
        for name, call in self.entries(ledger,'stability_gate') + [('freeze', lambda:ledger.authenticate_frozen(ledger.event('frozen_gate')['frozen']))]:
            before = logical_database(ledger); seen = []
            original = ledger._evaluated_record
            def read(c, row):
                if not seen and row['stage'] == 'alternate_conformity':
                    self.assertTrue(c.in_transaction)
                    p = subprocess.run([sys.executable,'-c',code,str(ledger.path)],capture_output=True,text=True,timeout=5)
                    self.assertEqual(p.returncode,0,p.stderr); self.assertIn('locked',p.stdout); self.assertNotIn('unlocked',p.stdout); seen.append(True)
                return original(c,row)
            with self.subTest(entry=name), patch.object(ledger,'_evaluated_record',side_effect=read): call()
            self.assertTrue(seen); self.assertEqual(logical_database(ledger),before)
            p = subprocess.run([sys.executable,'-c',code,str(ledger.path)],capture_output=True,text=True,timeout=5)
            self.assertEqual(p.stdout.strip(),'unlocked')


if __name__ == '__main__': unittest.main()
