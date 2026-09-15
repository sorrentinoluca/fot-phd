"""R-D9-01/02: final identical tests on rejected/corrected code, synthetic only."""
import os
import sys
from pathlib import Path
if os.environ.get('FOT_D9_TARGET'):
    sys.path.insert(0, os.environ['FOT_D9_TARGET'])
import json
import shutil
import sqlite3
import unittest
from unittest.mock import patch
from studio2.fase03.harness import test_revisions as scaffolding
from studio2.fase03.harness.common import HarnessError, sha256_file
from studio2.fase03.harness.ledger import PilotLedger, digest
from studio2.fase03.harness.runtime import execute_request
from studio2.fase03 import run_pilot as rp


class D9Corrections(unittest.TestCase):
    def setUp(self):
        self.t = scaffolding.RunnerRevisions()
        self.t.setUp()
        self.addCleanup(self.t.doCleanups)

    def database(self):
        with sqlite3.connect(self.t.ledger.path) as c:
            return tuple(c.iterdump())

    def artifacts(self):
        return {str(p.relative_to(self.t.home)): sha256_file(p)
                for folder in ('results', 'consumer_results', 'prepared')
                for p in (self.t.home / folder).rglob('*') if p.is_file()}

    def no_effect(self, operation, pattern='tokenizer|chat template'):
        before = self.database(), self.artifacts(), len(self.t.calls), len(self.t.consumer_calls)
        with self.assertRaisesRegex(HarnessError, pattern):
            operation()
        self.assertEqual((self.database(), self.artifacts(), len(self.t.calls), len(self.t.consumer_calls)), before)

    def metadata(self, value, role='122B'):
        ref = self.t.config['d9']['services'][role]['documentation']
        p = Path(ref['path']); doc = json.loads(p.read_text()); doc['weights_revision'] = value
        p.write_text(json.dumps(doc)); ref['sha256'] = sha256_file(p); self.t.approve_config()

    def test_01_whitespace_sentinels_prevent_client_and_intents(self):
        for role in ('122B', '27B'):
            for value in (' PENDING ', '\tunknown\n', '\u00a0UnDeCiDeD\u00a0'):
                with self.subTest(role=role, value=value):
                    self.metadata(value, role)
                    self.no_effect(self.t.producer, 'missing service metadata: weights_revision')
                    self.t.server_mock.assert_not_called()
                    self.metadata('fixture-immutable-revision', role)

    def test_02_valid_metadata_and_resume_preserve_outputs(self):
        self.metadata(' fixture-immutable-revision ')
        self.assertEqual(self.t.producer()['status'], 'PASS')
        before = self.database(), self.artifacts()
        self.t.producer(resume=True)
        self.assertEqual((self.database(), self.artifacts()), before)
        self.assertEqual(len(self.t.calls), 8)

    def split_snapshots(self):
        self.canonical = self.t.snapshot
        self.chat = self.t.home / 'service-tokenizer' / self.canonical.name
        shutil.copytree(self.canonical, self.chat)
        self.t.snapshot = self.chat
        self.assertNotEqual(str(self.chat), self.t.config['d9']['r4_snapshot'])

    def binding(self):
        self.split_snapshots(); self.t.prepare()
        with patch.object(rp, 'execute_request', side_effect=HarnessError('stop before reserve')):
            with self.assertRaisesRegex(HarnessError, 'stop before reserve'):
                rp.run_budget_stage(self.t.prepared, self.t.results, ledger=self.t.ledger)
        return self.t.ledger.binding('budget_probe')

    def reserve(self, b, ledger=None):
        spec = b['requests'][0]
        (ledger or self.t.ledger).reserve_request(request_id='correction-test-intent',
            logical_id=spec['logical_id'], model=spec['model'], producer=spec['producer'],
            stage='budget_probe', stage_run=digest(b))

    def test_03_distinct_snapshots_positive_direct_reserve(self):
        b = self.binding(); self.reserve(b)
        self.assertEqual(self.t.ledger.snapshot()['requests_cumulative'], 9)

    def test_04_missing_or_changed_files_direct_and_restart(self):
        b = self.binding()
        for snapshot in (self.canonical, self.chat):
            for filename in ('tokenizer.json', 'tokenizer_config.json', 'chat_template.jinja'):
                p = snapshot / filename; original = p.read_bytes()
                for mutation in ('missing', 'changed'):
                    for restart in (False, True):
                        with self.subTest(snapshot=snapshot.parent.name, file=filename, mutation=mutation, restart=restart):
                            if mutation == 'missing': p.unlink()
                            else: p.write_bytes(original + b' changed')
                            ledger = PilotLedger(self.t.ledger.path, pilot_id=self.t.ledger.pilot_id) if restart else self.t.ledger
                            try: self.no_effect(lambda: self.reserve(b, ledger))
                            finally: p.write_bytes(original)

    def test_05_success_then_new_fault_same_instance(self):
        b = self.binding(); self.reserve(b)
        (self.chat / 'tokenizer.json').unlink()
        spec = b['requests'][1]
        self.no_effect(lambda: self.t.ledger.reserve_request(request_id='second',
            logical_id=spec['logical_id'], model=spec['model'], producer=spec['producer'],
            stage='budget_probe', stage_run=digest(b)))

    def test_06_rebind_and_binding_reuse_require_current_files(self):
        b = self.binding(); (self.canonical / 'tokenizer.json').unlink()
        self.no_effect(lambda: self.t.ledger.bind_stage('budget_probe', b))
        self.no_effect(lambda: self.t.ledger.binding('budget_probe'))

    def test_07_execute_request_no_transport_or_journal_after_loss(self):
        b = self.binding(); (self.chat / 'tokenizer.json').unlink(); sent=[]
        self.no_effect(lambda: execute_request(ledger=self.t.ledger, stage='budget_probe',
            spec=b['requests'][0], transport=lambda: sent.append('SENT'), evaluate=lambda raw: {},
            expected_identity={}, journal_path=self.t.results/'new-journal.jsonl'))
        self.assertEqual(sent, [])
        self.assertFalse((self.t.results/'new-journal.jsonl').exists())

    def test_08_closed_producer_reuse_requires_recoverable_tokenizer(self):
        self.split_snapshots(); self.t.producer(); (self.chat / 'tokenizer.json').unlink()
        self.no_effect(lambda: self.t.ledger.binding('producer_conformity'))
        self.no_effect(lambda: self.t.producer(resume=True))

    def test_09_missing_service_snapshot_binding_fails_closed(self):
        b = self.binding(); b.pop('tokenizer_snapshot', None)
        # An unbound copy is checked before insertion; no historical binding is backfilled.
        self.no_effect(lambda: self.t.ledger.bind_stage('budget_probe', b), 'tokenizer')

    def test_10_alternate_producer_reuse_checks_its_chat_snapshot(self):
        self.split_snapshots(); self.t.config['d9']['alternate_placement']='pilot'; self.t.approve_config()
        self.t.producer(); self.t.producer(stage='alternate_conformity')
        (self.chat / 'tokenizer.json').unlink()
        self.no_effect(lambda: self.t.ledger.binding('alternate_conformity'))

if __name__ == '__main__':
    unittest.main(verbosity=2)
