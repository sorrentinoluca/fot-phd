"""Offline regression for the 122B producer tokenizer-accounting hard stop."""
import tempfile
import unittest
from pathlib import Path

from studio2.fase03.harness.common import HarnessError
from studio2.fase03.harness.ledger import PilotLedger, TokenizerAccountingGuard
from studio2.fase03.harness.runtime import execute_request


class FakeTokenizer:
    def apply_chat_template(self, messages, *, tokenize, add_generation_prompt):
        self.last_messages = messages
        assert tokenize is True and add_generation_prompt is True
        return list(range(sum(len(message['content']) for message in messages)))


class TokenizerAccounting(unittest.TestCase):
    def setUp(self):
        self.work = tempfile.TemporaryDirectory()
        self.ledger = PilotLedger(Path(self.work.name, 'ledger.sqlite3'), pilot_id='accounting-fixture')
        self.messages = [{'role': 'user', 'content': 'abc'}]
        self.guard = TokenizerAccountingGuard(FakeTokenizer())
        self.binding = {'requests': [
            {'logical_id': f'agent_{n}', 'model': '122b-fixture', 'producer': '122B',
             'prompt_sha256': f'{n:064x}', 'case_sha256': 'a' * 64,
             'contract_sha256': 'b' * 64, 'condition': 'producer', 'group': f'agent_{n}',
             'repetition': 1}
            for n in range(1, 9)
        ]}
        self.ledger.bind_stage('producer_conformity', self.binding)

    def tearDown(self):
        self.work.cleanup()

    def _execute(self, index, response, calls):
        spec = self.binding['requests'][index]
        def transport():
            calls.append(spec['logical_id'])
            return response
        def evaluate(raw):
            return {'returned_model': '122b-fixture', 'system_fingerprint': None,
                    'schema_valid_first_attempt': True, 'prompt_tokens': raw['usage']['prompt_tokens'],
                    'completion_tokens': 1, 'total_tokens': raw['usage']['prompt_tokens'] + 1}
        return execute_request(
            ledger=self.ledger, stage='producer_conformity', spec=spec, transport=transport,
            evaluate=evaluate, expected_identity={'returned_model': '122b-fixture', 'system_fingerprint': None}, journal_path=Path(self.work.name, 'journal.jsonl'),
            messages=self.messages, accounting_guard=self.guard)

    @staticmethod
    def _response(prompt_tokens):
        response = {'id': 'offline', 'model': '122b-fixture', 'choices': [], 'usage': {}}
        if prompt_tokens == 'no_usage':
            response.pop('usage')
            return response
        if prompt_tokens != 'absent':
            response['usage']['prompt_tokens'] = prompt_tokens
        return response

    def test_eight_distinct_valid_responses_are_bound_before_evaluation(self):
        calls = []
        for index in range(8):
            self._execute(index, self._response(3), calls)
        self.assertEqual(calls, [f'agent_{n}' for n in range(1, 9)])
        self.ledger.validate_tokenizer_accounting_evidence(self.guard)

    def test_invalid_usage_hard_stops_before_any_later_request_and_survives_restart(self):
        for bad in ('no_usage', 'absent', None, True, '3', -1, 4):
            with self.subTest(bad=bad):
                with tempfile.TemporaryDirectory() as work:
                    ledger = PilotLedger(Path(work, 'ledger.sqlite3'), pilot_id='accounting-fixture')
                    ledger.bind_stage('producer_conformity', self.binding)
                    original_ledger, original_work = self.ledger, self.work
                    self.ledger, self.work = ledger, type('W', (), {'name': work})()
                    try:
                        calls = []
                        with self.assertRaisesRegex(HarnessError, 'FATAL_ACCOUNTING_ERROR'):
                            self._execute(0, self._response(bad), calls)
                        self.assertEqual(calls, ['agent_1'])
                        leaf = self.ledger.leaf('producer_conformity', 'agent_1')
                        self.assertIsNone(self.ledger.response(leaf['request_id'])['record'])
                        self.assertIsNotNone(self.ledger.event('stop:tokenizer_accounting'))
                        restarted = PilotLedger(self.ledger.path, pilot_id='accounting-fixture')
                        with self.assertRaisesRegex(HarnessError, 'FATAL_ACCOUNTING_ERROR'):
                            restarted.bind_stage('producer_conformity', self.binding)
                    finally:
                        self.ledger, self.work = original_ledger, original_work

    def test_changed_messages_snapshot_or_raw_cannot_reauthorize_evidence(self):
        calls = []
        self._execute(0, self._response(3), calls)
        changed_messages = [{'role': 'user', 'content': 'changed'}]
        with self.assertRaisesRegex(HarnessError, 'messages'):
            self.ledger.validate_tokenizer_accounting_evidence(self.guard, expected_messages={'agent_1': changed_messages})
        with self.assertRaisesRegex(HarnessError, 'snapshot'):
            TokenizerAccountingGuard(FakeTokenizer(), snapshot='Qwen/Qwen3.5-122B-A10B-FP8@wrong')
        import sqlite3
        with sqlite3.connect(self.ledger.path) as connection:
            connection.execute("UPDATE responses SET raw_json=?", ('{"usage":{"prompt_tokens":3}}',))
        with self.assertRaisesRegex(HarnessError, 'binding'):
            self.ledger.validate_tokenizer_accounting_evidence(self.guard)
