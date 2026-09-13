#!/usr/bin/env python3
"""03.12 offline contract; no inference, HTTP, repair, or automatic retry."""
from __future__ import annotations
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

HERE = Path(__file__).resolve().parent
VERSION = '1.0.0'
FIXED = ('insight_id', 'source_agent', 'pseudolabel', 'evidence_scope', 'variable_ids')
LABEL = re.compile(r'S2-CLS-[A-Z0-9]{5}')
VARIABLE = re.compile(r'X(?:MEAS\((?:[1-9]|[1-3][0-9]|4[01])\)|MV\((?:[1-9]|1[0-2])\))')
REVISION = '017b9c7af6b5689d5dd426a76e0bc077eb5ca20a'

class ContractError(ValueError):
    def __init__(self, code, field, message):
        self.code, self.field = code, field
        super().__init__(message)
    def as_dict(self):
        return {'code': self.code, 'field': self.field, 'message': str(self)}

def fail(code, field, message):
    raise ContractError(code, field, message)

def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':'), allow_nan=False).encode('utf-8')

def digest(data):
    return hashlib.sha256(data).hexdigest()

def loads(raw):
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                fail('json', key, 'duplicate JSON key')
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda x: fail('json', '', 'non-finite JSON number'))
    except (ValueError, UnicodeError) as exc:
        if isinstance(exc, ContractError):
            raise
        fail('json', '', str(exc))

def offline_counter(snapshot):
    snapshot = Path(snapshot)
    if not snapshot.is_dir():
        fail('tokenizer', '', 'local Qwen snapshot missing')
    for name in ('tokenizer.json', 'tokenizer_config.json'):
        if not (snapshot / name).is_file():
            fail('tokenizer', name, 'local tokenizer asset missing')
    expected_hashes = {
        'tokenizer.json': '0997f410c57a1f4e53b09e4be8f4a172d90edd9564368fb0847030937229b9f3',
        'tokenizer_config.json': 'b11349aafa7cdc6a320767cf7ceb29ed82f7eda5d65e8e0819e76f0ce947bf27',
    }
    if any(digest((snapshot / name).read_bytes()) != sha for name, sha in expected_hashes.items()):
        fail('tokenizer', '', 'tokenizer hash differs from pinned preflight assets')
    try:
        from transformers import AutoTokenizer
        tokenizer = AutoTokenizer.from_pretrained(str(snapshot), local_files_only=True, trust_remote_code=False)
    except Exception as exc:
        fail('tokenizer', '', str(exc))
    def count(text):
        return len(tokenizer.encode(text, add_special_tokens=False))
    count.metadata = {'model': 'Qwen/Qwen3.8-27B-FP8', 'expected_revision': REVISION,
                      'snapshot': str(snapshot.resolve()),
                      'revision_verified': snapshot.name == REVISION,
                      'sha256': {name: digest((snapshot / name).read_bytes())
                                 for name in ('tokenizer.json', 'tokenizer_config.json')}}
    if snapshot.name != REVISION:
        fail('tokenizer', '', 'snapshot directory must identify the pinned Qwen revision')
    return count

def scan(value):
    rules = loads((HERE / 'leakage_rules_v1.json').read_bytes())
    findings = []
    for field, content in value.items():
        text = ' '.join(content) if isinstance(content, list) else content
        text = unicodedata.normalize('NFKC', text)
        for pattern in rules['forbidden_patterns']:
            for match in re.finditer(pattern, text, re.I):
                findings.append({'field': field, 'rule': pattern, 'match': match.group()})
        if field != 'pseudolabel' and re.search(r'S2-CLS-[A-Z0-9]{5}|\b(?:Normal|Unknown)\b', text, re.I):
            findings.append({'field': field, 'rule': 'label_neutral', 'match': text})
    return findings

def validate(value, *, fixed, count):
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        fail('dependency', '', 'jsonschema is required')
    schema = loads((HERE / 'insight_v1.schema.json').read_bytes())
    errors = list(Draft202012Validator(schema).iter_errors(value))
    if errors:
        error = errors[0]
        fail('cap' if error.validator == 'maxLength' else 'schema', '.'.join(map(str, error.path)), error.message)
    if not isinstance(fixed, dict) or set(fixed) != set(FIXED):
        fail('fixed', '', 'expected exactly five trusted fixed fields')
    for field in FIXED:
        if value[field] != fixed[field]:
            fail('fixed', field, 'producer changed deterministic field')
    findings = scan(value)
    if findings:
        fail('leakage', findings[0]['field'], json.dumps(findings, ensure_ascii=False))
    narrative = value['observed_pattern']
    refs = VARIABLE.findall(narrative)
    residue = VARIABLE.sub('', narrative)
    if re.search(r'\bX\s*(?:MEAS|MV)\b', residue, re.I):
        fail('variable', 'observed_pattern', 'malformed variable identifier')
    if not refs or not set(refs) <= set(value['variable_ids']):
        fail('variable', 'observed_pattern', 'literal references required and must be declared')
    encoded = canonical(value)
    metrics = {'observed_pattern_tokens': count(narrative),
               'evidence_scope_tokens': count(value['evidence_scope']),
               'record_tokens': count(encoded.decode('utf-8')),
               'record_characters': len(encoded.decode('utf-8')), 'record_bytes': len(encoded)}
    for key, cap in [('observed_pattern_tokens', 192), ('evidence_scope_tokens', 64),
                     ('record_tokens', 384), ('record_characters', 1400)]:
        if metrics[key] > cap:
            fail('cap', key, f'{metrics[key]} > {cap}')
    return metrics

def context_check(context):
    if not isinstance(context, dict) or set(context) != {'owners', 'normal_label', 'fixed'}:
        fail('context', '', 'context requires owners, normal_label, fixed')
    owners = context['owners']
    if not isinstance(owners, dict) or len(owners) != 8 or any(not isinstance(x, str) for x in owners.values()) or set(owners.values()) != {f'agent_{i}' for i in range(1, 9)}:
        fail('context', 'owners', 'eight distinct fault labels and agent owners required')
    labels = [*owners, context['normal_label']]
    if any(not isinstance(x, str) or not LABEL.fullmatch(x) for x in labels) or len(set(labels)) != 9:
        fail('context', 'owners', 'nine distinct opaque labels required')
    fixed = context['fixed']
    if not isinstance(fixed, list) or len(fixed) != 16 or any(not isinstance(x, dict) or set(x) != set(FIXED) for x in fixed):
        fail('context', 'fixed', '16 five-field contracts required')
    ids = [x['insight_id'] for x in fixed]
    if any(not isinstance(x, str) for x in ids) or len(set(ids)) != 16:
        fail('context', 'fixed', 'unique IDs required')
    return {x['insight_id']: x for x in fixed}

def validate_library(values, *, context, count):
    fixed = context_check(context)
    if not isinstance(values, list) or len(values) != 16:
        fail('cardinality', '', 'library requires 16 insights')
    metrics = []
    for value in values:
        if not isinstance(value, dict) or not isinstance(value.get('insight_id'), str) or value['insight_id'] not in fixed:
            fail('fixed', 'insight_id', 'unknown or missing insight ID')
        metrics.append(validate(value, fixed=fixed[value['insight_id']], count=count))
    if len({v['insight_id'] for v in values}) != 16:
        fail('cardinality', 'insight_id', 'duplicate IDs')
    owners = context['owners']
    if Counter(v['pseudolabel'] for v in values) != Counter({x: 2 for x in owners}):
        fail('cardinality', 'pseudolabel', 'two insights per fault required; Normal excluded')
    if any(owners[v['pseudolabel']] != v['source_agent'] for v in values):
        fail('ownership', 'source_agent', 'source must own the original label')
    return metrics

def peers(values, *, agent, context, count):
    validate_library(values, context=context, count=count)
    if agent not in context['owners'].values():
        fail('context', 'agent', 'unknown receiver')
    result = [v for v in values if v['source_agent'] != agent]
    if len(result) != 14:
        fail('cardinality', '', '14 peers required')
    return result

def diff_be(before, after, *, mapping, context, count, agent=None):
    b, e = loads(before), loads(after)
    if before != canonical(b) or after != canonical(e):
        fail('bytes', '', 'B and E must be canonical JSON bytes, without trailing newline')
    if agent is None:
        validate_library(b, context=context, count=count)
    else:
        fixed = context_check(context)
        if agent not in context['owners'].values() or not isinstance(b, list) or len(b) != 14:
            fail('cardinality', '', 'known receiver and 14 B peers required')
        for item in b:
            if not isinstance(item, dict) or not isinstance(item.get('insight_id'), str) or item.get('insight_id') not in fixed:
                fail('fixed', '', 'unknown B insight')
            validate(item, fixed=fixed[item['insight_id']], count=count)
        expected_ids = {x['insight_id'] for x in context['fixed'] if x['source_agent'] != agent}
        if len({x['insight_id'] for x in b}) != 14 or {x['insight_id'] for x in b} != expected_ids:
            fail('cardinality', '', 'B must contain exactly receiver peers')
        expected_labels = {label for label, owner in context['owners'].items() if owner != agent}
        if Counter(x['pseudolabel'] for x in b) != Counter({label: 2 for label in expected_labels}):
            fail('cardinality', '', 'invalid peer label multiplicities')
        if any(context['owners'].get(x['pseudolabel']) != x['source_agent'] for x in b):
            fail('ownership', '', 'invalid B ownership')
    labels = {x['pseudolabel'] for x in b}
    if not isinstance(mapping, dict) or any(not isinstance(x, str) for x in mapping.values()) or set(mapping) != labels or set(mapping.values()) != labels or any(k == v for k, v in mapping.items()):
        fail('mapping', '', 'mapping must be a zero-fixed-point bijection on B labels')
    expected = [dict(x, pseudolabel=mapping[x['pseudolabel']]) for x in b]
    if after != canonical(expected):
        fail('diff', '', 'E differs from the pseudolabel-only transformation')
    for item in expected:
        validate(item, fixed={k: item[k] for k in FIXED}, count=count)
    return {'valid': True, 'changed_field': 'pseudolabel', 'records': len(b),
            'b_sha256': digest(before), 'e_sha256': digest(after),
            'changed_byte_offsets': [i for i, (x, y) in enumerate(zip(before, after)) if x != y]}

def conformity_metrics(events, *, context, count):
    fixed = context_check(context)
    groups = defaultdict(list)
    for event in events:
        required = {'producer', 'condition', 'insight_id', 'attempt', 'raw', 'truncated', 'prompt_tokens', 'request_id'}
        if not isinstance(event, dict) or set(event) != required:
            fail('log', '', 'invalid event fields')
        if any(not isinstance(event[k], str) or not event[k] for k in ['producer', 'condition', 'insight_id', 'raw', 'request_id']):
            fail('log', '', 'nonempty string metadata required')
        if type(event['truncated']) is not bool or type(event['attempt']) is not int or event['attempt'] < 1:
            fail('log', '', 'invalid attempt/truncation metadata')
        if event['prompt_tokens'] is not None and (type(event['prompt_tokens']) is not int or event['prompt_tokens'] < 0):
            fail('log', '', 'invalid prompt token count')
        if event['insight_id'] not in fixed:
            fail('log', '', 'unknown insight ID')
        groups[(event['producer'], event['condition'])].append(event)
    result = []
    for (producer, condition), rows in sorted(groups.items()):
        attempts = defaultdict(list)
        requests = {}
        measured = []
        for row in rows:
            request = row['request_id']
            if request in requests and requests[request] != row['prompt_tokens']:
                fail('log', '', 'inconsistent prompt tokens for request')
            requests[request] = row['prompt_tokens']
            error, tokens = None, None
            try:
                value = loads(row['raw'])
                if isinstance(value, dict) and isinstance(value.get('observed_pattern'), str):
                    tokens = {'observed_pattern_tokens': count(value['observed_pattern']),
                              'record_tokens': count(canonical(value).decode('utf-8'))}
                validate(value, fixed=fixed[row['insight_id']], count=count)
            except ContractError as exc:
                error = exc.as_dict()
            item = {'insight_id': row['insight_id'], 'attempt': row['attempt'],
                    'valid': error is None, 'error': error, 'tokens': tokens,
                    'truncated': row['truncated']}
            attempts[row['insight_id']].append(item)
            measured.append(item)
        retries_to_valid = {}
        first_valid = 0
        for ident, sequence in attempts.items():
            sequence.sort(key=lambda x: x['attempt'])
            if [x['attempt'] for x in sequence] != list(range(1, len(sequence) + 1)):
                fail('log', '', 'attempts must be unique and contiguous from 1')
            valid = [x['attempt'] for x in sequence if x['valid']]
            if valid and valid[0] != len(sequence):
                fail('log', '', 'attempt after first valid output')
            first_valid += bool(valid and valid[0] == 1)
            retries_to_valid[ident] = valid[0] - 1 if valid else None
        result.append({'producer': producer, 'condition': condition, 'insights_attempted': len(attempts),
                       'first_attempt_valid': first_valid, 'first_attempt_valid_rate': first_valid / len(attempts),
                       'attempts': len(rows), 'valid_attempts': sum(x['valid'] for x in measured),
                       'valid_attempt_rate': sum(x['valid'] for x in measured) / len(rows),
                       'retries': len(rows) - len(attempts), 'retries_to_valid': retries_to_valid,
                       'truncated_attempts': sum(x['truncated'] for x in measured),
                       'cap_failures': sum(bool(x['error'] and x['error']['code'] == 'cap') for x in measured),
                       'record_tokens_measured': sum(x['tokens']['record_tokens'] for x in measured if x['tokens'] is not None),
                       'narrative_tokens_measured': sum(x['tokens']['observed_pattern_tokens'] for x in measured if x['tokens'] is not None),
                       'unmeasurable_insights': sum(x['tokens'] is None for x in measured),
                       'prompt_tokens_by_request': requests, 'per_attempt': measured})
    return result

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('mode', choices=['insight', 'library', 'diff', 'metrics'])
    parser.add_argument('input', type=Path)
    parser.add_argument('--context', required=True, type=Path)
    parser.add_argument('--tokenizer-snapshot', required=True, type=Path)
    parser.add_argument('--after', type=Path)
    parser.add_argument('--mapping', type=Path)
    parser.add_argument('--agent')
    args = parser.parse_args()
    try:
        count = offline_counter(args.tokenizer_snapshot)
        context = loads(args.context.read_bytes())
        raw = args.input.read_bytes()
        if args.mode == 'diff':
            if not args.after or not args.mapping:
                fail('arguments', '', 'diff needs --after and --mapping')
            result = diff_be(raw, args.after.read_bytes(), mapping=loads(args.mapping.read_bytes()), context=context, count=count, agent=args.agent)
        elif args.mode == 'library':
            result = validate_library(loads(raw), context=context, count=count)
        elif args.mode == 'metrics':
            result = conformity_metrics(loads(raw), context=context, count=count)
        else:
            fixed = context_check(context)
            value = loads(raw)
            if not isinstance(value, dict) or not isinstance(value.get('insight_id'), str) or value['insight_id'] not in fixed:
                fail('fixed', '', 'unknown insight')
            result = validate(value, fixed=fixed[value['insight_id']], count=count)
        print(json.dumps({'valid': True, 'version': VERSION, 'tokenizer': count.metadata, 'result': result}, ensure_ascii=False, indent=2))
        return 0
    except (ContractError, OSError) as exc:
        error = exc.as_dict() if isinstance(exc, ContractError) else {'code': 'io', 'message': str(exc)}
        print(json.dumps({'valid': False, 'error': error}, ensure_ascii=False))
        return 1

if __name__ == '__main__':
    sys.exit(main())
