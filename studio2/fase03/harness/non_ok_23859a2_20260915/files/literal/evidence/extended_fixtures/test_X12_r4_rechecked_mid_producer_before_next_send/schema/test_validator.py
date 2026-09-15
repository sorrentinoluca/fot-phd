"""Synthetic contract fixtures only; fake counts never qualify scientific budgets."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import unittest
from unittest.mock import patch
from studio2.fase03.schema_insight import validator as v


REPO = Path(__file__).resolve().parents[3]
PSEUDOLABEL_MAIN_COMMIT = 'a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155'
PSEUDOLABEL_TAG = 'studio2-fase03-pseudolabel-frozen-001'
PSEUDOLABEL_TAG_COMMIT = 'c16b533016db4617deb1ba96853253f117e8e32b'
PSEUDOLABEL_SOURCES = {
    'studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json':
        'b0ce81d53f11038ddf51c9ec964a1e838a7045e2e57b8ac3368f05e9a215bbc6',
    'studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json':
        'df7434230dcd1d5460cd19e0d27e909efd40289f64d89a4b3fee2a0e55b79fcf',
}


def git(*args):
    return subprocess.run(['git', *args], cwd=REPO, check=True, capture_output=True).stdout


def contract_037():
    tag_commit = git('rev-parse', f'{PSEUDOLABEL_TAG}^{{}}').decode().strip()
    if tag_commit != PSEUDOLABEL_TAG_COMMIT:
        raise AssertionError('03.7 frozen tag points to an unexpected commit')
    git('merge-base', '--is-ancestor', PSEUDOLABEL_TAG_COMMIT, PSEUDOLABEL_MAIN_COMMIT)
    documents = {}
    for path, expected_sha256 in PSEUDOLABEL_SOURCES.items():
        raw = git('show', f'{PSEUDOLABEL_MAIN_COMMIT}:{path}')
        if raw != git('show', f'{PSEUDOLABEL_TAG}^{{}}:{path}'):
            raise AssertionError(f'{path} differs between recorded main and the 03.7 tag')
        if hashlib.sha256(raw).hexdigest() != expected_sha256:
            raise AssertionError(f'{path} differs from its recorded 03.7 fingerprint')
        documents[path] = json.loads(raw)
    mapping = documents['studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json']
    assignment = documents['studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json']
    owners = {row['local_fault_label']: agent for agent, row in assignment['agents'].items()}
    fault_labels = set(mapping['label_by_identifier'].values()) - {'Normal'}
    if set(owners) != fault_labels or mapping['label_space'] != sorted(fault_labels) + ['Normal']:
        raise AssertionError('03.7 map and agent assignment disagree')
    return owners, mapping['label_by_identifier']['Normal']


def fixture():
    owners, normal_label = contract_037()
    items = []
    for i, (label, agent) in enumerate(owners.items()):
        for j in range(2):
            items.append({'insight_id': f'S2-INS-{2*i+j+1:03d}', 'source_agent': agent,
                          'pseudolabel': label, 'evidence_scope': 'Across development windows.',
                          'variable_ids': ['XMEAS(7)', 'XMV(11)'],
                          'observed_pattern': 'XMEAS(7) remains elevated across windows; XMV(11) is stable.'})
    context = {'owners': owners, 'normal_label': normal_label,
               'fixed': [{k: x[k] for k in v.FIXED} for x in copy.deepcopy(items)]}
    return items, context


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.items, self.context = fixture()
        self.count = lambda text: len(text.split())

    def check(self, item, fixed=None, count=None):
        return v.validate(item, fixed=fixed or self.context['fixed'][0], count=count or self.count)

    def reject(self, code, fn):
        with self.assertRaises(v.ContractError) as result:
            fn()
        self.assertEqual(result.exception.code, code)

    def test_valid_schema_and_library(self):
        from jsonschema import Draft202012Validator
        Draft202012Validator.check_schema(v.loads((v.HERE/'insight_v1.schema.json').read_bytes()))
        self.assertEqual(len(v.validate_library(self.items, context=self.context, count=self.count)), 16)
        self.assertGreater(self.check(self.items[0])['record_tokens'], 0)

    def test_context_uses_frozen_037_labels_and_literal_normal(self):
        fixed = v.context_check(self.context)
        self.assertEqual(len(fixed), 16)
        self.assertEqual(self.context['normal_label'], 'Normal')
        self.assertEqual(set(self.context['owners'].values()), {f'agent_{i}' for i in range(1, 9)})

    def test_context_rejects_nonliteral_normal_label(self):
        for normal_label in ['S2-CLS-ZZZZZ', 'normal', 'NORMAL', 'Normal ']:
            with self.subTest(normal_label=normal_label):
                context = copy.deepcopy(self.context)
                context['normal_label'] = normal_label
                self.reject('context', lambda: v.context_check(context))

    def test_context_rejects_normal_as_owner(self):
        context = copy.deepcopy(self.context)
        label, agent = next(iter(context['owners'].items()))
        del context['owners'][label]
        context['owners']['Normal'] = agent
        self.reject('context', lambda: v.context_check(context))

    def test_every_field_missing_wrong_type_and_extra(self):
        for field in self.items[0]:
            for operation in ('missing','type'):
                with self.subTest(field=field, operation=operation):
                    item = copy.deepcopy(self.items[0])
                    if operation == 'missing': del item[field]
                    else: item[field] = 5
                    self.reject('schema', lambda: self.check(item))
        item = dict(self.items[0], extra='x')
        self.reject('schema', lambda: self.check(item))

    def test_invalid_formats_each_field(self):
        bad = {'insight_id': 'F1', 'source_agent': 'agent_9', 'pseudolabel': 'Unknown',
               'evidence_scope': ' ', 'variable_ids': ['reactor temperature'], 'observed_pattern': '\n'}
        for field, value in bad.items():
            with self.subTest(field=field):
                item = dict(self.items[0], **{field: value})
                self.reject('schema', lambda: self.check(item))

    def test_all_fixed_fields_immutable(self):
        replacements = {'insight_id':'S2-INS-900', 'source_agent':'agent_2', 'pseudolabel':'S2-CLS-ABCDE',
                        'evidence_scope':'Across other windows.', 'variable_ids':['XMV(1)']}
        for field, value in replacements.items():
            with self.subTest(field=field):
                self.reject('fixed', lambda: self.check(dict(self.items[0], **{field:value})))

    def test_character_caps(self):
        for field, cap in [('observed_pattern',800), ('evidence_scope',240)]:
            item = dict(self.items[0], **{field:'x'*(cap+1)})
            self.reject('cap', lambda: self.check(item))

    def test_token_caps_and_exact_boundary(self):
        for text, cap in [(self.items[0]['observed_pattern'],192),(self.items[0]['evidence_scope'],64),
                          (v.canonical(self.items[0]).decode(),384)]:
            self.check(self.items[0], count=lambda s: cap if s == text else 1)
            self.reject('cap', lambda: self.check(self.items[0], count=lambda s: cap+1 if s == text else 1))

    def test_record_character_cap_with_json_escaping(self):
        item = dict(self.items[0], observed_pattern='XMEAS(7) '+ '\t'*790)
        self.reject('cap', lambda: self.check(item, count=lambda s: 1))

    def test_variable_ranges_duplicates_cardinality(self):
        for ids in [[], ['XMEAS(7)']*2, ['XMEAS(42)'], ['XMV(13)'], ['XMEAS(01)'],
                    ['xmeas(7)'], ['XMEAS (7)'], [f'XMEAS({i})' for i in range(1,10)]]:
            self.reject('schema', lambda: self.check(dict(self.items[0], variable_ids=ids)))
        for ident in ['XMEAS(41)','XMV(12)','XMEAS(1)','XMV(1)']:
            item = dict(self.items[0], variable_ids=[ident], observed_pattern=ident+' is elevated.')
            self.check(item, fixed={k:item[k] for k in v.FIXED})

    def test_narrative_references(self):
        for text in ['Persistently elevated.', 'XMEAS(8) is elevated.', 'XMEAS(7) and xmeas(8).',
                     'XMEAS (7) rises.', 'XMEAS(07) rises.']:
            self.reject('variable', lambda: self.check(dict(self.items[0], observed_pattern=text)))

    def test_paraphrases(self):
        for text in ['reactor temperature rises', 'temperatura del reattore sale', 'feed flow rises']:
            self.reject('leakage', lambda: self.check(dict(self.items[0], observed_pattern='XMEAS(7) '+text)))

    def test_all_d1_fault_ids_and_mechanisms(self):
        for fault in [1,2,3,8,10,13,14,15]:
            for alias in [f'F{fault}',f'IDV({fault})',f'fault {fault}',f'guasto {fault}']:
                self.reject('leakage', lambda: self.check(dict(self.items[0], observed_pattern='XMEAS(7) '+alias)))
        for term in ['step','random variation','slow drift','sticking valve','gradino','incollamento',
                     'reaction kinetics','ratio_ac_s4']:
            self.reject('leakage', lambda: self.check(dict(self.items[0], observed_pattern='XMEAS(7) '+term)))

    def test_scan_every_field_and_label_neutrality(self):
        for field in v.FIXED + ('observed_pattern',):
            item = dict(self.items[0], **{field:['fault 14'] if field=='variable_ids' else 'fault 14'})
            self.assertTrue(v.scan(item))
        for label in ['S2-CLS-ABCDE','Normal','Unknown']:
            self.reject('leakage', lambda: self.check(dict(self.items[0], observed_pattern='XMEAS(7) '+label)))
        self.assertEqual(v.scan({'pseudolabel': 'Normal'}), [])

    def test_library_integrity(self):
        self.reject('cardinality', lambda: v.validate_library(self.items[:-1], context=self.context, count=self.count))
        items = copy.deepcopy(self.items); items[-1]=items[0]
        self.reject('cardinality', lambda: v.validate_library(items, context=self.context, count=self.count))
        items, context = fixture()
        items[0]['source_agent']='agent_2'; context['fixed'][0]['source_agent']='agent_2'
        self.reject('ownership', lambda: v.validate_library(items, context=context, count=self.count))
        items, context = fixture()
        items[0]['pseudolabel']=context['normal_label']; context['fixed'][0]['pseudolabel']=context['normal_label']
        self.reject('schema', lambda: v.validate_library(items, context=context, count=self.count))

    def test_all_receivers_and_diff(self):
        for agent in self.context['owners'].values():
            b=v.peers(self.items, agent=agent, context=self.context, count=self.count)
            self.assertEqual(len(b),14)
            self.assertTrue(all(x['source_agent']!=agent for x in b))
            labels=sorted({x['pseudolabel'] for x in b})
            mapping=dict(zip(labels, labels[1:]+labels[:1]))
            e=[dict(x,pseudolabel=mapping[x['pseudolabel']]) for x in b]
            result=v.diff_be(v.canonical(b),v.canonical(e),mapping=mapping,context=self.context,count=self.count,agent=agent)
            self.assertEqual(result['records'],14)
            self.assertTrue(result['changed_byte_offsets'])

    def test_diff_rejects_second_field_reorder_whitespace_and_bad_mapping(self):
        b=self.items; labels=list(self.context['owners']); mapping=dict(zip(labels,labels[1:]+labels[:1]))
        e=[dict(x,pseudolabel=mapping[x['pseudolabel']]) for x in b]
        def diff(after, m=mapping):
            return v.diff_be(v.canonical(b),after,mapping=m,context=self.context,count=self.count)
        self.assertTrue(diff(v.canonical(e))['valid'])
        changed=copy.deepcopy(e); changed[0]['observed_pattern']+=' altered'
        self.reject('diff',lambda:diff(v.canonical(changed)))
        self.reject('diff',lambda:diff(v.canonical(e[::-1])))
        self.reject('bytes',lambda:diff(v.canonical(e)+b'\n'))
        self.reject('mapping',lambda:diff(v.canonical(e),dict(zip(labels,labels))))
        self.reject('mapping',lambda:diff(v.canonical(e),{x:labels[0] for x in labels}))

    def test_strict_json(self):
        for raw in ['{"a":1,"a":2}', '{"a":NaN}', '{', b'\xff']:
            self.reject('json',lambda:v.loads(raw))

    def test_missing_tokenizer_fails_closed(self):
        self.reject('tokenizer',lambda:v.offline_counter('/nonexistent/snapshot'))

    def test_metrics_retry_failure_truncation_and_request_dedup(self):
        ident=self.items[0]['insight_id']
        def event(item, attempt, raw, request):
            return {'producer':'synthetic-test', 'condition':'probe', 'insight_id':item,
                    'attempt':attempt, 'raw':raw, 'truncated':False, 'prompt_tokens':100,
                    'request_id':request}
        events=[event(ident,1,'{','r1'),event(ident,2,v.canonical(self.items[0]).decode(),'r2'),
                event(self.items[1]['insight_id'],1,v.canonical(self.items[1]).decode(),'r1')]
        events[0]['truncated']=True
        result=v.conformity_metrics(events,context=self.context,count=self.count)[0]
        self.assertEqual(result['first_attempt_valid_rate'],.5)
        self.assertEqual(result['retries_to_valid'][ident],1)
        self.assertEqual(result['unmeasurable_insights'],1)
        self.assertEqual(result['truncated_attempts'],1)
        self.assertEqual(result['prompt_tokens_by_request'],{'r1':100,'r2':100})
        events.append(event(ident,3,v.canonical(self.items[0]).decode(),'r3'))
        self.reject('log',lambda:v.conformity_metrics(events,context=self.context,count=self.count))

    def test_metrics_invalid_log(self):
        self.reject('log',lambda:v.conformity_metrics([{}],context=self.context,count=self.count))
        self.assertEqual(v.conformity_metrics([],context=self.context,count=self.count),[])

    def test_malformed_identifiers_alongside_valid_reference(self):
        for alias in ['XMEAS7', 'XMV11', 'ＸＭＥＡＳ(7)', 'ＸＭＶ(11)',
                      'XMEAS(７)', 'X\u200bMEAS(7)', 'XMEAS\u200b7']:
            with self.subTest(alias=alias):
                self.reject('variable', lambda: self.check(dict(
                    self.items[0], observed_pattern='XMEAS(7) rises; '+alias+' is stable.')))
        self.check(dict(self.items[0], observed_pattern='XMEAS(7) rises; XMV(11) is stable.'))

    def test_singular_plural_and_invisible_leakage(self):
        for text in ['variazione casuale', 'variazioni casuali', 'F\u200b1',
                     'IDV\u200b(14)', 'slow\u200b drift', 'S2-CLS-\u200bABCDE']:
            with self.subTest(text=text):
                self.reject('leakage', lambda: self.check(dict(
                    self.items[0], observed_pattern='XMEAS(7) '+text)))
        item=dict(self.items[0], observed_pattern='XMEAS(7) rises across 10 samples.')
        self.check(item)

    def assert_counter_probes(self, counter):
        # Empty text and a single ASCII vocabulary token have known counts.
        # The variable probe additionally rejects constant/word-count substitutes.
        probes = {text: counter(text) for text in ['', 'a', 'XMEAS(7)']}
        self.assertEqual(probes[''], 0)
        self.assertEqual(probes['a'], 1)
        self.assertGreater(probes['XMEAS(7)'], 2)
        return probes

    def test_qwen_probe_rejects_broken_counters(self):
        for counter in [lambda text: 0, lambda text: 2, lambda text: len(text.split())]:
            with self.assertRaises(AssertionError):
                self.assert_counter_probes(counter)

    @unittest.skipUnless(os.environ.get('QWEN_TOKENIZER_SNAPSHOT'), 'pinned Qwen tokenizer absent; real-budget qualification pending')
    def test_real_offline_qwen(self):
        with patch('socket.socket', side_effect=AssertionError('network forbidden')):
            counter=v.offline_counter(Path(os.environ['QWEN_TOKENIZER_SNAPSHOT']))
            probes=self.assert_counter_probes(counter)
            metrics=v.validate_library(self.items,context=self.context,count=counter)
            self.assertEqual(len(metrics),16)
            self.assertTrue(counter.metadata['revision_verified'])
            for metric in metrics:
                self.assertGreater(metric['observed_pattern_tokens'], 2)
                self.assertGreater(metric['record_tokens'], metric['observed_pattern_tokens'])
            print('\nQWEN_TOKENIZER_QUALIFICATION '+json.dumps({
                'tokenizer': counter.metadata, 'probe_counts': probes,
                'fixture_metrics': [dict(insight_id=item['insight_id'],
                    record_tokens=metric['record_tokens'],
                    observed_pattern_tokens=metric['observed_pattern_tokens'],
                    evidence_scope_tokens=metric['evidence_scope_tokens'])
                    for item, metric in zip(self.items, metrics)],
            }, sort_keys=True), flush=True)

if __name__ == '__main__':
    unittest.main()
