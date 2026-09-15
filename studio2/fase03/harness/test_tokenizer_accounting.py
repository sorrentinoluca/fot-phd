"""Adversarial offline regressions for mandatory 122B tokenizer accounting."""
from copy import deepcopy
from pathlib import Path
from contextlib import closing
import json
import tempfile
import unittest

from studio2.fase03.harness.common import HarnessError, canonical_json, sha256_text
from studio2.fase03.harness.ledger import PilotLedger, TokenizerAccountingGuard, digest
from studio2.fase03.harness.offline_fixtures import Trial
from studio2.fase03.harness.runtime import execute_request


MODEL_122B = 'qwen3.5-122b'
MESSAGES = [{'role': 'user', 'content': 'abc'}]


class FakeTokenizer:
    def __init__(self, error=None):
        self.error = error

    def apply_chat_template(self, messages, *, tokenize, add_generation_prompt):
        if self.error:
            raise self.error
        assert tokenize is True and add_generation_prompt is True
        return list(range(sum(len(message['content']) for message in messages)))


def response(prompt_tokens=3, *, response_id='offline'):
    return {
        'id': response_id,
        'model': MODEL_122B,
        'system_fingerprint': None,
        'choices': [{'message': {'content': '{}'}, 'finish_reason': 'stop'}],
        'usage': {'prompt_tokens': prompt_tokens, 'completion_tokens': 1,
                  'total_tokens': prompt_tokens + 1 if type(prompt_tokens) is int else 1},
    }


def evaluate(raw):
    usage = raw.get('usage') or {}
    choices = raw.get('choices') or []
    choice = choices[0] if len(choices) == 1 else {}
    return {
        'returned_model': raw.get('model'), 'system_fingerprint': raw.get('system_fingerprint'),
        'response_id': raw.get('id'), 'finish_reason': choice.get('finish_reason'),
        'raw_output': choice.get('message', {}).get('content'), 'schema_valid_first_attempt': True,
        'prompt_tokens': usage.get('prompt_tokens'), 'completion_tokens': usage.get('completion_tokens'),
        'total_tokens': usage.get('total_tokens'),
    }


class TokenizerAccounting(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory(); self.addCleanup(self.work.cleanup)
        self.home = Path(self.work.name)
        self.guard = TokenizerAccountingGuard(FakeTokenizer())
        self.ledger = PilotLedger(self.home / 'producer.sqlite3', pilot_id='accounting-producer')
        self.producer_binding = self._binding('producer', MODEL_122B, 8)
        self.ledger.bind_stage('producer_conformity', self.producer_binding)

    @staticmethod
    def _binding(producer, model, count, *, budget=False):
        return {'requests': [
            {'logical_id': f'case-{n}', 'model': model, 'producer': producer,
             'prompt_sha256': sha256_text(MESSAGES[0]['content']),
             'case_sha256': digest(['case', n]), 'contract_sha256': digest(['contract', n]),
             'condition': ('A', 'B-LF', 'E-LF')[n % 3] if budget else 'producer',
             'group': 'budget' if budget else f'case-{n}', 'repetition': 1}
            for n in range(count)
        ], 'template_text': 'fixture\n', 'inventory_sha256': digest('fixture')}

    def _execute(self, *, ledger=None, binding=None, stage='producer_conformity', index=0,
                 model=MODEL_122B, messages=MESSAGES, guard='default', resume=False,
                 raw=None, calls=None):
        ledger = ledger or self.ledger; binding = binding or self.producer_binding
        spec = binding['requests'][index]; calls = [] if calls is None else calls
        raw = response() if raw is None else raw

        def transport(*transmitted):
            calls.append(deepcopy(transmitted)); return deepcopy(raw)

        kwargs = dict(ledger=ledger, stage=stage, spec=spec, transport=transport, evaluate=evaluate,
                      expected_identity={'returned_model': model, 'system_fingerprint': None},
                      journal_path=self.home / f'{stage}.jsonl', resume=resume)
        if messages is not None: kwargs['messages'] = messages
        if guard == 'default': kwargs['accounting_guard'] = self.guard
        elif guard is not None: kwargs['accounting_guard'] = guard
        return execute_request(**kwargs)

    def _consumer(self):
        trial = Trial(self.home / 'consumer-prerequisite'); trial.finish('producer_conformity')
        binding = self._binding('consumer', MODEL_122B, 3, budget=True)
        trial.ledger.bind_stage('budget_probe', binding)
        return trial.ledger, binding

    @staticmethod
    def _counts(ledger):
        snap = ledger.snapshot()
        with closing(ledger._connect()) as connection:
            records = connection.execute('SELECT count(*) FROM responses WHERE record_json IS NOT NULL').fetchone()[0]
        return dict(intents=snap['requests_cumulative'], raw=snap['durable_responses'], records=records,
                    stopped='stop:tokenizer_accounting' in snap['events'])

    def test_A01_missing_guard_producer_refuses_before_intent_and_transport(self):
        calls = []; before = self._counts(self.ledger)
        with self.assertRaisesRegex(HarnessError, 'FATAL_ACCOUNTING_ERROR'):
            self._execute(guard=None, calls=calls)
        self.assertEqual(calls, []); self.assertEqual(self._counts(self.ledger), before)

    def test_A02_missing_guard_consumer_refuses_before_intent_and_transport(self):
        ledger, binding = self._consumer(); calls = []; before = self._counts(ledger)
        with self.assertRaisesRegex(HarnessError, 'FATAL_ACCOUNTING_ERROR'):
            self._execute(ledger=ledger, binding=binding, stage='budget_probe', messages=None, guard=None, calls=calls)
        self.assertEqual(calls, []); self.assertEqual(self._counts(ledger), before)

    def test_A03_completed_record_revalidates_messages_without_transport(self):
        self._execute()
        with closing(self.ledger._connect()) as connection, connection:
            row = connection.execute("SELECT detail_json FROM events WHERE event LIKE 'tokenizer_accounting:%'").fetchone()
            detail = json.loads(row[0]); detail['messages'] = [{'role': 'user', 'content': 'xyz'}]
            detail['messages_sha256'] = sha256_text(canonical_json(detail['messages']))
            connection.execute("UPDATE events SET detail_json=? WHERE event LIKE 'tokenizer_accounting:%'", (canonical_json(detail),))
        calls = []
        with self.assertRaisesRegex(HarnessError, 'FATAL_ACCOUNTING_ERROR'):
            self._execute(resume=True, calls=calls)
        self.assertEqual(calls, []); self.assertTrue(self._counts(self.ledger)['stopped'])

    def test_A04_coherent_raw_and_internal_hash_tamper_is_rejected(self):
        self._execute()
        with closing(self.ledger._connect()) as connection, connection:
            raw = json.loads(connection.execute('SELECT raw_json FROM responses').fetchone()[0])
            raw['id'] = 'forged'; raw_json = canonical_json(raw); raw_sha = sha256_text(raw_json)
            connection.execute('UPDATE responses SET raw_json=?,raw_sha256=?', (raw_json, raw_sha))
            event = connection.execute("SELECT detail_json FROM events WHERE event LIKE 'tokenizer_accounting:%'").fetchone()
            detail = json.loads(event[0]); detail['raw_response_sha256'] = raw_sha
            connection.execute("UPDATE events SET artifact_sha256=?,detail_json=? WHERE event LIKE 'tokenizer_accounting:%'",
                               (raw_sha, canonical_json(detail)))
        calls = []
        with self.assertRaisesRegex(HarnessError, 'FATAL_ACCOUNTING_ERROR'):
            self._execute(resume=True, calls=calls)
        self.assertEqual(calls, []); self.assertTrue(self._counts(self.ledger)['stopped'])

    def test_A05_tokenizer_value_error_persists_raw_and_stop_before_record(self):
        calls = []; broken = TokenizerAccountingGuard(FakeTokenizer(ValueError('template exploded')))
        with self.assertRaisesRegex(HarnessError, 'FATAL_ACCOUNTING_ERROR'):
            self._execute(guard=broken, calls=calls)
        self.assertEqual(len(calls), 1)
        self.assertEqual(self._counts(self.ledger), {'intents': 1, 'raw': 1, 'records': 0, 'stopped': True})

    def test_A06_pass_event_without_record_resumes_idempotently(self):
        spec = self.producer_binding['requests'][0]
        request_id = digest([self.ledger.pilot_id, 'producer_conformity', spec['logical_id']])
        self.ledger.reserve_request(request_id=request_id, logical_id=spec['logical_id'], model=spec['model'],
                                    producer=spec['producer'], stage='producer_conformity',
                                    stage_run=digest(self.producer_binding))
        self.ledger.save_raw(request_id, response(), latency_ms=1.0)
        self.ledger.account_producer_response(request_id, messages=MESSAGES, guard=self.guard)
        calls = []; restarted = PilotLedger(self.ledger.path, pilot_id=self.ledger.pilot_id)
        record = self._execute(ledger=restarted, resume=True, calls=calls)
        self.assertTrue(record['identity_valid']); self.assertEqual(calls, [])
        self.assertEqual(self._counts(restarted), {'intents': 1, 'raw': 1, 'records': 1, 'stopped': False})

    def test_positive_producer_and_consumer_first_resume_restart(self):
        first = self._execute()
        for ledger in (self.ledger, PilotLedger(self.ledger.path, pilot_id=self.ledger.pilot_id)):
            calls = []; self.assertEqual(self._execute(ledger=ledger, resume=True, calls=calls), first)
            self.assertEqual(calls, [])
        consumer, binding = self._consumer()
        first_consumer = self._execute(ledger=consumer, binding=binding, stage='budget_probe')
        restarted = PilotLedger(consumer.path, pilot_id=consumer.pilot_id); calls = []
        self.assertEqual(self._execute(ledger=restarted, binding=binding, stage='budget_probe', resume=True, calls=calls), first_consumer)
        self.assertEqual(calls, [])

    def test_invalid_usage_variants_stop_after_one_transport_without_record(self):
        bad_responses = []; no_usage = response(); no_usage.pop('usage'); bad_responses.append(no_usage)
        no_prompt = response(); no_prompt['usage'].pop('prompt_tokens'); bad_responses.append(no_prompt)
        bad_responses.extend(response(value) for value in (None, True, '3', -1, 4))
        for index, bad in enumerate(bad_responses):
            with self.subTest(index=index), tempfile.TemporaryDirectory() as directory:
                ledger = PilotLedger(Path(directory) / 'ledger.sqlite3', pilot_id='accounting-invalid')
                ledger.bind_stage('producer_conformity', self.producer_binding); calls = []
                with self.assertRaisesRegex(HarnessError, 'FATAL_ACCOUNTING_ERROR'):
                    self._execute(ledger=ledger, raw=bad, calls=calls)
                self.assertEqual(len(calls), 1)
                self.assertEqual(self._counts(ledger), {'intents': 1, 'raw': 1, 'records': 0, 'stopped': True})

    def test_non_122b_remains_compatible_without_guard(self):
        ledger = PilotLedger(self.home / 'other.sqlite3', pilot_id='other-model-fixture')
        binding = self._binding('producer', 'other-model', 8); ledger.bind_stage('producer_conformity', binding)
        raw = response(); raw['model'] = 'other-model'; calls = []
        record = self._execute(ledger=ledger, binding=binding, model='other-model', messages=None,
                               guard=None, raw=raw, calls=calls)
        self.assertTrue(record['identity_valid']); self.assertEqual(len(calls), 1)
        self.assertFalse(self._counts(ledger)['stopped'])


if __name__ == '__main__':
    unittest.main()
