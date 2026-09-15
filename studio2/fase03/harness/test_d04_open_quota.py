"""D04 contract-first probes. All mutations/approvals are disposable offline fixtures."""
from contextlib import closing, redirect_stdout
import io
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
TARGET = Path(os.environ.get('FOT_HARNESS_TARGET', str(HERE.parents[2])))
sys.path.insert(0, str(TARGET))
from studio2.fase03.harness.common import HarnessError
from studio2.fase03.harness.ledger import PilotLedger, STAGES, digest
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness import test_revisions as fixtures

CONTRACT = json.loads((HERE / 'D04_DECISION_CONTRACT.json').read_text())
OBS = {}


def logical(ledger):
    with closing(sqlite3.connect(ledger.path)) as c:
        return '\n'.join(c.iterdump())


def sql(ledger, statement, values=()):
    with closing(sqlite3.connect(ledger.path)) as c, c:
        c.execute(statement, values)


def tree_bytes(path):
    return {str(p.relative_to(path)): p.read_bytes() for p in path.rglob('*')
            if p.is_file() and not p.name.startswith('pilot.sqlite3')}


class OpenQuotaContract(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.serial = 0

    def copy(self, source):
        self.serial += 1
        t = Trial(self.home / ('copy-' + str(self.serial)))
        with closing(sqlite3.connect(source.ledger.path)) as a, closing(sqlite3.connect(t.ledger.path)) as b:
            a.backup(b)
        return t

    def source(self, stage, role):
        t = Trial(self.home / (stage + '-' + role))
        if stage == 'producer_remediation':
            t.finish(valid=False)
            t.remediation()
        else:
            if stage in {'budget_probe', 'stability_gate'}:
                t.finish()
            if stage == 'stability_gate':
                t.finish('budget_probe', 3)
            t.bind(stage, 6 if stage == 'budget_probe' else None)
        r = t.reserve(0, stage)
        if role == 'transport':
            if stage == 'budget_probe':
                originals = [r] + [t.reserve(i, stage) for i in (1, 2)]
                for original in originals:
                    t.zero(original)
                t.ledger.reserve_probe_transport_triplet(self.triplet(t, originals, 'first'))
                r = 'first-0'
            else:
                t.zero(r)
                r = t.retry(r, 'retry-0')
        return t, r

    def triplet(self, t, originals, prefix):
        result = []
        for i, original in enumerate(originals):
            row = t.ledger.request(original)
            result.append(dict(request_id=f'{prefix}-{i}', retry_of=original,
                               logical_id=row['logical_id'], model=row['model'], producer=row['producer'],
                               stage_run=row['stage_run'], condition=json.loads(row['identity_json'])['condition']))
        return result

    def state(self, t, request, status):
        if status == 'FAILED':
            t.ledger.complete_request(request, status='FAILED', transport_failure=True,
                                      detail={'error_type': 'TimeoutError', 'message': 'FIXTURE'})
        elif status == 'ZERO_TOKEN_PROVEN':
            t.zero(request)
        elif status == 'COMPLETED':
            t.complete(request)

    def entry(self, t, stage, entry):
        if entry == 'bind_stage':
            t.ledger.bind_stage(stage, t.ledger.binding(stage))
        else:
            if stage == 'budget_probe':
                with closing(sqlite3.connect(t.ledger.path)) as c:
                    next_base = c.execute("SELECT count(*) FROM requests WHERE stage='budget_probe' AND retry_of IS NULL").fetchone()[0]
                t.reserve(next_base, stage, request_id='next-base')
            else:
                t.reserve(1, stage, request_id='next-base')

    def test_D04_inventory_covers_stages_roles_and_normative_dependencies(self):
        fields = json.loads((HERE / CONTRACT['field_inventory']).read_text())
        self.assertEqual(set(CONTRACT['stages']), STAGES)
        self.assertEqual(fields['sql_tables']['requests']['quota_kind'], 'N')
        for field in CONTRACT['role_dependencies']:
            self.assertEqual(fields['sql_tables']['requests'][field], 'N')
        self.assertEqual(set(CONTRACT['statuses']), {'INTENT', 'FAILED', 'ZERO_TOKEN_PROVEN', 'COMPLETED'})
        for stage, roles in CONTRACT['stages'].items():
            self.assertEqual(roles, (['remediation'] if stage == 'producer_remediation' else ['base'])
                             + ([] if stage == 'stability_gate' else ['transport']))

    def test_D04_generated_quota_matrix_open_stages_states_and_entries(self):
        results = []
        OBS['quota_matrix'] = results
        for stage, roles in CONTRACT['stages'].items():
            for role in roles:
                source, request = self.source(stage, role)
                for status in CONTRACT['statuses']:
                    state = self.copy(source)
                    self.state(state, request, status)
                    for entry in CONTRACT['entry_points']:
                        positive = self.copy(state)
                        self.entry(positive, stage, entry)
                        for value in CONTRACT['quota_values']:
                            if value == role:
                                continue
                            row = dict(stage=stage, role=role, status=status, entry=entry, mutation=value)
                            with self.subTest(**row):
                                t = self.copy(state)
                                sql(t.ledger, 'UPDATE requests SET quota_kind=? WHERE request_id=?', (value, request))
                                t.ledger = PilotLedger(t.ledger.path, pilot_id=t.ledger.pilot_id)
                                before = logical(t.ledger)
                                try:
                                    self.entry(t, stage, entry)
                                except HarnessError:
                                    row['refused'] = True
                                else:
                                    row['refused'] = False
                                row['unchanged'] = logical(t.ledger) == before
                                results.append(row)
                                self.assertTrue(row['refused'])
                                self.assertTrue(row['unchanged'])

    def test_D04_eighth_retry_and_new_fault_after_previous_success(self):
        t = Trial(self.home / 'eighth')
        t.bind()
        r = t.reserve(0)
        for i in range(7):
            t.zero(r)
            r = t.retry(r, f'retry-{i}')
        t.zero(r)
        before = logical(t.ledger)
        with self.assertRaises(HarnessError):
            t.retry(r, 'eighth-control')
        self.assertEqual(logical(t.ledger), before)
        t.bind()
        sql(t.ledger, "UPDATE requests SET quota_kind='base' WHERE request_id='retry-0'")
        before = logical(t.ledger)
        results = []
        for restart in (False, True):
            if restart:
                t.ledger = PilotLedger(t.ledger.path, pilot_id=t.ledger.pilot_id)
            for entry, action in [('bind', t.bind), ('retry', lambda: t.retry(r, 'eighth-fault'))]:
                with self.subTest(restart=restart, entry=entry):
                    with self.assertRaises(HarnessError):
                        action()
                    self.assertEqual(logical(t.ledger), before)
                    results.append(dict(restart=restart, entry=entry, refused=True))
        OBS['eighth'] = results

    def test_D04_role_dependencies_are_validated_before_new_reservation(self):
        source, request = self.source('producer_conformity', 'transport')
        results = []
        OBS['role_dependencies'] = results
        for field, value in CONTRACT['role_dependencies'].items():
            for entry in CONTRACT['entry_points']:
                row = dict(field=field, entry=entry)
                with self.subTest(**row):
                    t = self.copy(source)
                    sql(t.ledger, f'UPDATE requests SET {field}=? WHERE request_id=?', (value, request))
                    before = logical(t.ledger)
                    try:
                        self.entry(t, 'producer_conformity', entry)
                    except HarnessError:
                        row['refused'] = True
                    else:
                        row['refused'] = False
                    row['unchanged'] = logical(t.ledger) == before
                    results.append(row)
                    self.assertTrue(row['refused'])
                    self.assertTrue(row['unchanged'])

    def test_D04_probe_triplet_refuses_atomically_then_accepts_legal_retry(self):
        t, r = self.source('budget_probe', 'transport')
        originals = [f'first-{i}' for i in range(3)]
        for original in originals:
            t.zero(original)
        values = self.triplet(t, originals, 'second')
        sql(t.ledger, "UPDATE requests SET quota_kind='base' WHERE request_id=?", (r,))
        before = logical(t.ledger)
        with self.assertRaises(HarnessError):
            t.ledger.reserve_probe_transport_triplet(values)
        self.assertEqual(logical(t.ledger), before)
        sql(t.ledger, "UPDATE requests SET quota_kind='transport' WHERE request_id=?", (r,))
        t.ledger.reserve_probe_transport_triplet(values)
        self.assertEqual(t.ledger.snapshot()['transport_calls'], 6)
        for original in ['second-0', 'second-1', 'second-2']:
            t.zero(original)
        t.ledger.waive_remediation(approval_sha256='a' * 64)
        before = logical(t.ledger)
        with self.assertRaises(HarnessError):
            t.ledger.reserve_probe_transport_triplet(self.triplet(t, ['second-0', 'second-1', 'second-2'], 'third'))
        self.assertEqual(logical(t.ledger), before)
        OBS['triplet'] = dict(legal_transport=6, corrupt_refused=True, over_seven_refused_atomically=True)

    def test_D04_shared_attempt_validation_covers_other_open_stage_and_holds_lock(self):
        t = Trial(self.home / 'all-stages')
        t.bind()
        r = t.reserve(0)
        t.bind('alternate_conformity')
        t.reserve(0, 'alternate_conformity')
        seen = []
        original = t.ledger._validate_attempts
        code = """import sqlite3,sys
c=sqlite3.connect(sys.argv[1],timeout=.03)
try:c.execute('BEGIN IMMEDIATE');print('ACQUIRED');c.rollback()
except sqlite3.OperationalError:print('LOCKED')
finally:c.close()
"""
        def validate(c, binding, rows):
            self.assertTrue(c.in_transaction)
            result = subprocess.run([sys.executable, '-c', code, str(t.ledger.path)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(result.stdout.strip(), 'LOCKED')
            seen.extend(row['stage'] for row in rows)
            return original(c, binding, rows)
        for route, action in [('bind', t.bind), ('reserve', lambda: t.reserve(1))]:
            seen.clear()
            with self.subTest(route=route), patch.object(t.ledger, '_validate_attempts', side_effect=validate):
                action()
                self.assertEqual(set(seen), {'producer_conformity', 'alternate_conformity'})
        sql(t.ledger, "UPDATE requests SET quota_kind='transport' WHERE request_id='alternate_conformity-0'")
        before = logical(t.ledger)
        for action in (t.bind, lambda: t.reserve(2)):
            with self.assertRaises(HarnessError):
                action()
            self.assertEqual(logical(t.ledger), before)
        OBS['shared'] = dict(stages=['producer_conformity', 'alternate_conformity'], real_writer_blocked=True)

    def test_D04_explicit_waiver_preserves_valid_eighth_and_limit_fifteen(self):
        t = Trial(self.home / 'waiver')
        t.bind()
        r = t.reserve(0)
        for i in range(7):
            t.zero(r)
            r = t.retry(r, f'retry-{i}')
        t.zero(r)
        t.ledger.waive_remediation(approval_sha256='b' * 64)
        for i in range(7, 15):
            r = t.retry(r, f'retry-{i}')
            t.zero(r)
        self.assertEqual(t.ledger.snapshot()['transport_calls'], 15)
        before = logical(t.ledger)
        with self.assertRaises(HarnessError):
            t.retry(r, 'sixteenth')
        self.assertEqual(logical(t.ledger), before)
        OBS['waiver'] = dict(transport_calls=15, sixteenth_refused=True)

    def test_D04_runner_and_CLI_refuse_before_client_server_send_and_outputs(self):
        results = []
        OBS['runner'] = results
        for cli in (False, True):
            with self.subTest(cli=cli):
                t = fixtures.RunnerRevisions()
                t.setUp()
                try:
                    t.fail_at = 1
                    with self.assertRaises(HarnessError):
                        t.producer()
                    helper = Trial(self.home / ('helper-' + str(cli)))
                    helper.ledger = t.ledger
                    for i in range(7):
                        r = t.ledger.leaf('producer_conformity', 'agent_1')['request_id']
                        helper.zero(r)
                        t.fail_at = len(t.calls) + 1
                        with self.assertRaises(HarnessError):
                            t.producer(resume=True, retry_requests=[r])
                    r = t.ledger.leaf('producer_conformity', 'agent_1')['request_id']
                    helper.zero(r)
                    with closing(sqlite3.connect(t.ledger.path)) as c:
                        first = c.execute('SELECT request_id FROM requests WHERE retry_of IS NOT NULL ORDER BY rowid LIMIT 1').fetchone()[0]
                    sql(t.ledger, "UPDATE requests SET quota_kind='base' WHERE request_id=?", (first,))
                    t.ledger = PilotLedger(t.ledger.path, pilot_id=t.ledger.pilot_id)
                    before, outputs, calls = logical(t.ledger), tree_bytes(t.home), len(t.calls)
                    with patch.object(sys.modules['openai'], 'OpenAI', side_effect=AssertionError('client must not be constructed')) as client:
                        if cli:
                            args = ['producer_probe.py', '--execute', '--acknowledge', fixtures.pp.ACK,
                                    '--source-inventory', str(t.source), '--results-dir', str(t.home / 'results'),
                                    '--provider-config', str(t.provider), '--model-snapshot', str(t.snapshot),
                                    '--schema-dir', str(fixtures.SCHEMA), '--ledger', str(t.ledger.path),
                                    '--pilot-id', t.ledger.pilot_id, '--resume', '--retry-request', r]
                            with patch.object(sys, 'argv', args), redirect_stdout(io.StringIO()), self.assertRaises(HarnessError):
                                fixtures.pp.main()
                        else:
                            with self.assertRaises(HarnessError):
                                t.producer(resume=True, retry_requests=[r])
                        client.assert_not_called()
                    t.server_mock.assert_not_called()
                    self.assertEqual(len(t.calls), calls)
                    self.assertEqual(logical(t.ledger), before)
                    self.assertEqual(tree_bytes(t.home), outputs)
                    results.append(dict(cli=cli, client_calls=0, server_calls=0, new_sends=0, unchanged=True))
                finally:
                    t.doCleanups()


if __name__ == '__main__':
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(OpenQuotaContract))
    if os.environ.get('FOT_D04_OBSERVATIONS'):
        Path(os.environ['FOT_D04_OBSERVATIONS']).write_text(json.dumps(dict(tests=result.testsRun,
            failures=[dict(test=str(t), traceback=s) for t, s in result.failures],
            errors=[dict(test=str(t), traceback=s) for t, s in result.errors], observations=OBS), indent=2) + '\n')
    sys.exit(not result.wasSuccessful())
