"""D9 role and prerequisite contract. Documentation is not service qualification.

No network, automatic migration, scientific approval or zero-token proof is created here.
"""
from copy import deepcopy
from pathlib import Path
import json
import re

from .common import HarnessError, canonical_json, sha256_bytes

ROLES = {'producer': '122B', 'consumer': '122B', 'alternate': '27B'}
STAGE_MODELS = {'producer_conformity': '122B', 'producer_remediation': '122B',
                'alternate_conformity': '27B', 'budget_probe': '122B',
                'stability_gate': '122B', 'technical_qualification_122b': '122B'}
R4_TOKENIZER = {
    'revision': '017b9c7af6b5689d5dd426a76e0bc077eb5ca20a',
    'tokenizer_json_sha256': '0997f410c57a1f4e53b09e4be8f4a172d90edd9564368fb0847030937229b9f3',
    'tokenizer_config_sha256': 'b11349aafa7cdc6a320767cf7ceb29ed82f7eda5d65e8e0819e76f0ce947bf27',
    'chat_template_sha256': 'c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041'}
HISTORY_SOURCE = {'sha256': 'c9adf2a8f07d9058257cc2c51a00064662874611875a715c716a1f1ea4828368',
                  'reported_requests': 4, 'completed_inferences': 3}
RECOVERY_PROPOSAL_FILE_SHA256 = '77d72204d53e4706d7e93dc579532a9f148175e3d7daff75d0467c93eee03624'
APPROVED_122B_IDENTITY_SHA256 = 'd180061348b15bb0322cb75ae700bb97b1328994c8d572c98741455d5b0ef579'
QUALIFICATION_SUPPLEMENT_FILE_SHA256 = 'dd9c53f0e4262fffe592a04298f8d7a4cfd428ccf5c487faacfe68ca357decb7'
QUALIFICATION_SUPPLEMENT_CANONICAL_SHA256 = '79515feb95b1048f67e8c01446be580dcbb73def188a13175b842b58a5356a40'
IDENTITY_SHA256_SEMANTICS = (
    'CANONICAL_JSON_SHA256_OF_SOURCE_PROPOSAL_QUALIFICATION_SUPPLEMENT_CANDIDATE')


def fail(message):
    raise HarnessError('D9: ' + message)


def model_for_stage(stage):
    if stage not in STAGE_MODELS:
        fail('unsupported stage/arm')
    return STAGE_MODELS[stage]


def _text(value):
    return isinstance(value, str) and bool(value.strip()) and value.strip().upper() not in {'PENDING', 'UNDECIDED', 'UNKNOWN'}


def _hash(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


def _digest(value):
    return sha256_bytes(canonical_json(value).encode())


def read_reference(ref, role):
    if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'} or not _hash(ref.get('sha256')):
        fail(role + ' reference missing')
    path = Path(ref['path'])
    if not path.is_absolute() or not path.is_file():
        fail(role + ' file missing')
    data = path.read_bytes()
    if sha256_bytes(data) != ref['sha256']:
        fail(role + ' bytes changed')
    try:
        value = json.loads(data)
    except (ValueError, UnicodeError) as exc:
        raise HarnessError('D9: invalid ' + role) from exc
    if not isinstance(value, dict):
        fail(role + ' must be an object')
    return value


def read_bytes_reference(ref, role):
    if not isinstance(ref, dict) or set(ref) != {'path', 'sha256'} or not _hash(ref.get('sha256')):
        fail(role + ' reference missing')
    path = Path(ref['path'])
    if not path.is_absolute() or not path.is_file():
        fail(role + ' file missing')
    data = path.read_bytes()
    if sha256_bytes(data) != ref['sha256']:
        fail(role + ' bytes changed')
    return data


def _validate_response_identity_binding(binding, service):
    """Authenticate identity_sha256 to one named source object, not a file digest."""
    required = {
        'artifact_version', 'identity_sha256_semantics', 'source_proposal',
        'source_object_key', 'identity_sha256', 'qualification_supplement_file',
        'qualification_supplement_canonical_sha256',
    }
    if not isinstance(binding, dict) or set(binding) != required:
        fail('response identity binding fields are incomplete')
    if (binding.get('artifact_version') != 'RESPONSE_IDENTITY_BINDING_1'
            or binding.get('identity_sha256_semantics') != IDENTITY_SHA256_SEMANTICS
            or binding.get('source_object_key') != 'qualification_supplement_candidate'):
        fail('response identity binding semantics differ from the reviewed proposal')
    proposal_ref = binding.get('source_proposal')
    if (not isinstance(proposal_ref, dict)
            or proposal_ref.get('sha256') != RECOVERY_PROPOSAL_FILE_SHA256):
        fail('response identity source proposal is not the reviewed file')
    proposal = read_reference(proposal_ref, 'response identity source proposal')
    candidate = proposal.get(binding['source_object_key'])
    identity_sha256 = binding.get('identity_sha256')
    if (not isinstance(candidate, dict)
            or identity_sha256 != APPROVED_122B_IDENTITY_SHA256
            or proposal.get('qualification_supplement_canonical_sha256') != identity_sha256
            or _digest(candidate) != identity_sha256
            or service.get('identity_sha256') != identity_sha256
            or candidate.get('allowed_identity_update') != service.get('expected_response')):
        fail('identity_sha256 does not authenticate the reviewed proposal object')
    supplement_ref = binding.get('qualification_supplement_file')
    if (not isinstance(supplement_ref, dict)
            or supplement_ref.get('sha256') != QUALIFICATION_SUPPLEMENT_FILE_SHA256):
        fail('qualification supplement file digest differs from the reviewed bytes')
    supplement = read_reference(supplement_ref, 'qualification supplement')
    if (binding.get('qualification_supplement_canonical_sha256')
            != QUALIFICATION_SUPPLEMENT_CANONICAL_SHA256
            or _digest(supplement) != QUALIFICATION_SUPPLEMENT_CANONICAL_SHA256
            or {key: supplement.get(key) for key in ('returned_model', 'system_fingerprint')}
            != service.get('expected_response')):
        fail('qualification supplement canonical object differs from reviewed evidence')
    return binding


def _read_once(reference_or_path, role):
    if isinstance(reference_or_path, dict):
        return read_bytes_reference(reference_or_path, role)
    path = Path(reference_or_path)
    if not path.is_absolute() or not path.is_file():
        fail(role + ' file missing')
    return path.read_bytes()


def _json_from_bytes(data, role):
    try:
        value = json.loads(data)
    except (ValueError, UnicodeError) as exc:
        raise HarnessError('D9: invalid ' + role) from exc
    if not isinstance(value, dict):
        fail(role + ' must be an object')
    return value


def _jsonl_from_bytes(data, role):
    try:
        lines = data.decode('utf-8').splitlines()
        values = [json.loads(line) for line in lines]
    except (ValueError, UnicodeError) as exc:
        raise HarnessError('D9: invalid ' + role) from exc
    if not lines or any(not isinstance(value, dict) for value in values):
        fail(role + ' must contain JSON objects')
    return values


def _completed_history_row_valid(row):
    raw = row.get('raw_output')
    response = row.get('response_raw')
    usage = response.get('usage') if isinstance(response, dict) else None
    choices = response.get('choices') if isinstance(response, dict) else None
    choice = choices[0] if isinstance(choices, list) and len(choices) == 1 and isinstance(choices[0], dict) else None
    message = choice.get('message') if isinstance(choice, dict) else None
    token_keys = ('prompt_tokens', 'completion_tokens', 'total_tokens')
    tokens = [row.get(key) for key in token_keys]
    return (isinstance(raw, str) and _hash(row.get('raw_output_sha256'))
            and sha256_bytes(raw.encode()) == row['raw_output_sha256']
            and _text(row.get('response_id')) and _text(row.get('returned_model'))
            and _text(row.get('system_fingerprint')) and _text(row.get('finish_reason'))
            and all(type(value) is int and value >= 0 for value in tokens)
            and tokens[0] + tokens[1] == tokens[2]
            and isinstance(usage, dict)
            and all(usage.get(key) == row.get(key) for key in token_keys)
            and response.get('id') == row['response_id']
            and response.get('model') == row['returned_model']
            and response.get('system_fingerprint') == row['system_fingerprint']
            and isinstance(message, dict) and message.get('content') == raw
            and choice.get('finish_reason') == row['finish_reason'])


def validate_external_history_artifacts(package_ref, approval_ref, *, expected_ledger):
    """Read and validate one reviewed external-history package and its authorization.

    Every referenced file is read once per decision. Returned normalized rows are
    derived from those bytes and can be inserted by the caller in the same transaction.
    """
    package_bytes = _read_once(package_ref, 'external history package')
    approval_bytes = _read_once(approval_ref, 'external history approval')
    package = _json_from_bytes(package_bytes, 'external history package')
    approval = _json_from_bytes(approval_bytes, 'external history approval')
    required_package = {'artifact_version', 'status', 'source', 'pilot_ledger',
                        'source_files', 'request_imports', 'review'}
    if set(package) != required_package or package.get('artifact_version') != '1' or package.get('status') != 'MAPPING_REVIEWED':
        fail('external history package contract mismatch')
    if package.get('source') != HISTORY_SOURCE or package.get('pilot_ledger') != expected_ledger:
        fail('external history package belongs to another source or ledger')
    if set(package.get('source_files', {})) != {'summary', 'attempts', 'records'}:
        fail('external history source inventory is incomplete')
    source_bytes = {key: read_bytes_reference(ref, 'external history ' + key)
                    for key, ref in package['source_files'].items()}
    if sha256_bytes(source_bytes['summary']) != HISTORY_SOURCE['sha256']:
        fail('external history summary differs from the approved source')
    summary = _json_from_bytes(source_bytes['summary'], 'external history summary')
    reported = summary.get('reported_requests', summary.get('provider_requests_total'))
    completed = summary.get('completed_inferences', summary.get('completed_model_inferences'))
    if (reported, completed) != (
            HISTORY_SOURCE['reported_requests'], HISTORY_SOURCE['completed_inferences']):
        fail('external history source counts changed')
    if (summary.get('attempt_journal_sha256') not in {None, package['source_files']['attempts']['sha256']}
            or summary.get('records_sha256') not in {None, package['source_files']['records']['sha256']}):
        fail('external history summary no longer binds attempts and records')
    source_rows = {'attempts': _jsonl_from_bytes(source_bytes['attempts'], 'external history attempts'),
                   'records': _jsonl_from_bytes(source_bytes['records'], 'external history records')}
    if len(source_rows['attempts']) != 1 or len(source_rows['records']) != HISTORY_SOURCE['completed_inferences']:
        fail('external history source cardinality changed')
    review = package.get('review')
    if not isinstance(review, dict) or set(review) != {'reviewer', 'path', 'sha256'} or not _text(review.get('reviewer')):
        fail('external history mapping lacks independent review')
    if not read_bytes_reference({'path': review['path'], 'sha256': review['sha256']},
                                'external history review').strip():
        fail('external history review is empty')
    required_approval = {'artifact_version', 'author', 'decision', 'package_sha256',
                         'pilot_ledger', 'source'}
    if (set(approval) != required_approval or approval.get('artifact_version') != '1'
            or not _text(approval.get('author')) or approval.get('decision') != 'IMPORT_AUTHORIZED'
            or approval.get('package_sha256') != sha256_bytes(package_bytes)
            or approval.get('pilot_ledger') != expected_ledger
            or approval.get('source') != HISTORY_SOURCE):
        fail('external history import lacks exact author authorization')
    mappings = package.get('request_imports')
    if not isinstance(mappings, list) or len(mappings) != HISTORY_SOURCE['reported_requests']:
        fail('external history mapping must contain exactly four requests')
    normalized = []
    required_mapping = {'historical_ordinal', 'request_id', 'identity', 'identity_sha256',
                        'source_binding', 'disposition'}
    for position, mapping in enumerate(mappings, 1):
        if not isinstance(mapping, dict) or set(mapping) != required_mapping:
            fail('external history mapping fields are incomplete')
        ordinal = mapping.get('historical_ordinal')
        if type(ordinal) is not int or ordinal != position:
            fail('external history ordinal is missing, duplicated or out of order')
        request_id, identity = mapping.get('request_id'), mapping.get('identity')
        if not _text(request_id) or not isinstance(identity, dict) or mapping.get('identity_sha256') != sha256_bytes(canonical_json(identity).encode()):
            fail('external history assigned identity is invalid')
        binding = mapping.get('source_binding')
        expected_key, expected_line = ('attempts', 1) if ordinal == 1 else ('records', ordinal - 1)
        if (not isinstance(binding, dict) or set(binding) != {'source_key', 'line', 'record_sha256'}
                or binding.get('source_key') != expected_key or type(binding.get('line')) is not int
                or binding.get('line') != expected_line or not _hash(binding.get('record_sha256'))):
            fail('external history source binding is incomplete or swapped')
        row = source_rows[expected_key][expected_line - 1] if expected_line <= len(source_rows[expected_key]) else None
        if row is None or _digest(row) != binding['record_sha256']:
            fail('external history source row changed')
        required_identity = {'assignment': 'ASSIGNED_DURING_RECONCILIATION',
                             'historical_ordinal': ordinal, 'request_id': request_id,
                             'source_binding_sha256': _digest(binding)}
        if identity != required_identity:
            fail('external history identity must disclose its reconciliation assignment')
        disposition = mapping.get('disposition')
        if ordinal == 1:
            if (disposition != 'HISTORICAL_OUTCOME_UNCERTAIN'
                    or row.get('outcome') != 'REJECTED_BEFORE_INFERENCE'
                    or row.get('inference_completed') is not False):
                fail('S1 has no durable D03 zero-token proof')
        elif disposition != 'COMPLETED' or not _completed_history_row_valid(row):
            fail('completed external history mapping differs from source')
        normalized.append(deepcopy(mapping))
    if len({row['request_id'] for row in normalized}) != len(normalized) or len({row['identity_sha256'] for row in normalized}) != len(normalized):
        fail('external history identities must be unique')
    return {'package_sha256': sha256_bytes(package_bytes), 'approval_sha256': sha256_bytes(approval_bytes),
            'package': package, 'approval': approval, 'rows': normalized}


def generation_kwargs(generation, *, model_role):
    if model_role not in {'122B', '27B'}:
        fail('unknown generation role')
    allowed = {'max_tokens', 'seed', 'thinking_token_budget'} | ({'temperature'} if model_role == '27B' else set())
    if not isinstance(generation, dict) or set(generation) - allowed:
        fail('generation fields not authorized; 122B temperature must be absent')
    if type(generation.get('max_tokens')) is not int or generation['max_tokens'] <= 0:
        fail('positive output budget required')
    result = {'max_tokens': generation['max_tokens']}
    for key in ('seed', 'temperature'):
        value = generation.get(key)
        if value is not None:
            if key == 'seed' and type(value) is not int:
                fail('seed must be an integer or explicitly unavailable')
            if key == 'temperature' and (type(value) not in (int, float) or not 0 <= value <= 2):
                fail('invalid configured temperature')
            result[key] = value
    thinking = generation.get('thinking_token_budget')
    if thinking is not None:
        if type(thinking) is not int or thinking <= 0 or thinking > generation['max_tokens']:
            fail('invalid thinking budget')
        result['extra_body'] = {'thinking_token_budget': thinking}
    return result


def no_thinking_template_kwargs(value):
    """Validate the reviewed control without Python's bool/int equivalence."""
    if (not isinstance(value, dict)
            or set(value) != {'enable_thinking'}
            or value.get('enable_thinking') is not False
            or type(value.get('enable_thinking')) is not bool):
        fail('chat_template_kwargs must be exactly enable_thinking=false')
    return {'enable_thinking': False}


def producer_extra_body(value, *, model_role):
    """Allow one reviewed rendering control on the 122B producer, never a pass-through."""
    if value is None:
        return None
    if (model_role != '122B' or not isinstance(value, dict)
            or set(value) != {'chat_template_kwargs'}):
        fail('producer extra_body must be exactly chat_template_kwargs.enable_thinking=false for 122B')
    no_thinking_template_kwargs(value['chat_template_kwargs'])
    return {'chat_template_kwargs': {'enable_thinking': False}}


def require_122b_no_thinking(value, *, context):
    """Make the caller-specific 122B producer requirement explicit."""
    if value is None:
        fail(context + ' requires extra_body.chat_template_kwargs.enable_thinking=false')
    return producer_extra_body(value, model_role='122B')


def validate_config(config):
    d = config.get('d9')
    if not isinstance(d, dict) or d.get('roles') != ROLES:
        fail('approved fixed roles required')
    if d.get('missing_requirements') != [] or d.get('status') != 'DOCUMENTED_FOR_AUTHORIZED_STAGE':
        fail('prerequisites remain incomplete')
    if d.get('alternate_placement') not in {'pilot', 'deferred'}:
        fail('alternate placement requires an explicit decision')
    if d.get('r4_tokenizer') != R4_TOKENIZER or not Path(d.get('r4_snapshot', '')).is_absolute():
        fail('canonical R4 tokenizer must remain separate and pinned')
    from .guards import require_presentation
    require_presentation({'presentation':{'author_decision':'accepted','ordered_labels':d.get('presentation_order',[])}}, config.get('presentation_approval',{}))
    successor = d.get('successor_lineage') is not None
    services = d.get('services')
    if not isinstance(services, dict) or set(services) != {'122B', '27B'}:
        fail('exactly two documented services required')
    for role, service in services.items():
        required = {'model', 'base_url', 'identity_sha256', 'tokenizer', 'expected_response',
                    'max_model_len', 'max_output_tokens', 'documentation'}
        if not isinstance(service, dict) or set(service) != required:
            fail('service fields incomplete')
        if not all(_text(service[k]) for k in ('model', 'base_url')) or not _hash(service['identity_sha256']):
            fail('service identity missing')
        if not service['base_url'].startswith(('http://', 'https://')):
            fail('service URL missing')
        for k in ('max_model_len', 'max_output_tokens'):
            if type(service[k]) is not int or service[k] <= 0:
                fail('service limits missing')
        token = service['tokenizer']
        if not isinstance(token, dict) or set(token) != set(R4_TOKENIZER) or not _text(token['revision']) or not all(_hash(v) for k,v in token.items() if k != 'revision'):
            fail('service tokenizer/template pins incomplete')
        doc = read_reference(service['documentation'], role + ' documentation')
        if doc.get('status') != 'documented' or doc.get('nominal_model') != role:
            fail('service documentation is not an attestation of this nominal model')
        for key in ('source', 'validity_date', 'weights_repository', 'weights_revision', 'quantization',
                    'serving', 'parser', 'thinking', 'limit_semantics', 'sampling', 'error_policy', 'availability'):
            if not _text(doc.get(key)):
                fail('missing service metadata: ' + key)
        expected = {k:v for k,v in service.items() if k != 'documentation'}
        if doc.get('service') != expected:
            fail('documented service differs from execution configuration')
        if successor and role == '122B':
            _validate_response_identity_binding(doc.get('identity_binding'), service)
        from .guards import response_identity_valid
        response_identity_valid({}, service['expected_response'])
    c = services['122B']; candidate = config.get('candidate', {})
    for key, value in [('requested_model', c['model']), ('base_url', c['base_url']),
                       ('expected_max_model_len', c['max_model_len'])]:
        if candidate.get(key) != value:
            fail('consumer must use the documented 122B service')
    if config.get('tokenizer') != c['tokenizer'] or config.get('expected_response') != c['expected_response']:
        fail('consumer tokenizer/response identity differs from 122B')
    if 'temperature' in config.get('generation_budget', {}):
        fail('122B temperature must be omitted, not null/default')
    providers = d.get('producer_configs')
    if not isinstance(providers, dict) or set(providers) != {'122B', '27B'} or not all(_hash(v) for v in providers.values()):
        fail('producer configurations must be separately pinned by role')
    if set(config.get('approved_producer_config_sha256', [])) != set(providers.values()):
        fail('producer allowlist differs from D9 roles')
    lineage_ref = d.get('successor_lineage')
    if lineage_ref is not None:
        if 'history_reconciliation' in d or 'history_approval' in d:
            fail('successor lineage cannot be combined with historical reconciliation')
        approval_ref = d.get('successor_lineage_approval')
        read_bytes_reference(lineage_ref, 'successor lineage package')
        read_bytes_reference(approval_ref, 'successor lineage approval')
        from .successor import validate_successor_lineage_artifacts
        validate_successor_lineage_artifacts(
            Path(lineage_ref['path']), Path(approval_ref['path']),
            expected_ledger=config.get('pilot_ledger'))
        return d
    history_ref = d.get('history_reconciliation')
    history = read_reference(history_ref, 'historical consumption reconciliation')
    if history.get('status') == 'RECONCILED':
        if not _text(history.get('reviewer')) or history.get('source') != HISTORY_SOURCE:
            fail('historical S consumption requires reviewed reconciliation')
        if history.get('pilot_ledger') != config.get('pilot_ledger'):
            fail('historical reconciliation belongs to another ledger')
        mappings = history.get('request_identities')
        if not isinstance(mappings, dict) or len(mappings) != HISTORY_SOURCE['reported_requests'] or not all(_text(k) and _hash(v) for k,v in mappings.items()):
            fail('each historical request must map once to durable identity')
    elif history.get('status') == 'MAPPING_REVIEWED':
        validate_external_history_artifacts(history_ref, d.get('history_approval'),
                                            expected_ledger=config.get('pilot_ledger'))
    else:
        fail('historical S consumption requires reviewed reconciliation')
    return d


def validate_history(config, ledger, connection):
    d = validate_config(config)
    if d.get('successor_lineage') is not None:
        lineage_ref, approval_ref = d['successor_lineage'], d.get('successor_lineage_approval')
        read_bytes_reference(lineage_ref, 'successor lineage package')
        read_bytes_reference(approval_ref, 'successor lineage approval')
        successor, _ = ledger._classified_successor_lineage(
            connection, package_path=Path(lineage_ref['path']),
            approval_path=Path(approval_ref['path']))
        if not successor:
            fail('successor lineage was not durably classified')
        return
    h = read_reference(d['history_reconciliation'], 'historical consumption reconciliation')
    if h.get('status') == 'MAPPING_REVIEWED':
        validated = validate_external_history_artifacts(
            d['history_reconciliation'], d.get('history_approval'),
            expected_ledger={'path': str(ledger.identity_path), 'pilot_id': ledger.pilot_id})
        rows = ledger._validated_external_history(connection)
        if len(rows) != HISTORY_SOURCE['reported_requests']:
            fail('external historical consumption has not been reconciled')
        expected = {row['request_id']: row for row in validated['rows']}
        event = next((row for name, row in ledger._events(connection).items()
                      if name.startswith('history_reconciliation:')), None)
        if event is None or json.loads(event['detail_json']).get('approval_sha256') != validated['approval_sha256']:
            fail('external historical approval differs from the reconciled decision')
        for row in rows:
            mapping = expected.get(row['request_id'])
            if (mapping is None or row['historical_ordinal'] != mapping['historical_ordinal']
                    or row['identity_json'] != canonical_json(mapping['identity'])
                    or row['identity_sha256'] != mapping['identity_sha256']
                    or row['source_binding_json'] != canonical_json(mapping['source_binding'])
                    or row['source_binding_sha256'] != _digest(mapping['source_binding'])
                    or row['disposition'] != mapping['disposition']
                    or row['package_sha256'] != validated['package_sha256']):
                fail('external historical ledger binding differs from reviewed package')
        return
    # Read in the caller's decision transaction. No migration, reset, new row or backfill.
    rows = {r['request_id']:r for r in ledger._rows(connection)}
    for request_id, identity_hash in h['request_identities'].items():
        if request_id not in rows or sha256_bytes(rows[request_id]['identity_json'].encode()) != identity_hash:
            fail('historical request is not represented in this ledger')


def validate_provider(config, provider, stage, *, file_sha256):
    d = validate_config(config); role = model_for_stage(stage)
    if stage not in {'technical_qualification_122b', 'producer_conformity',
                     'producer_remediation', 'alternate_conformity'}:
        fail('not a producer stage')
    if stage == 'alternate_conformity' and d['alternate_placement'] != 'pilot':
        fail('alternate conformance is deferred; no pilot calls authorized')
    if file_sha256 != d['producer_configs'][role]:
        fail('provider configuration is not pinned to this stage role')
    service = d['services'][role]
    for key, expected in [('model',service['model']),('base_url',service['base_url']),
                          ('identity_sha256',service['identity_sha256']),('tokenizer',service['tokenizer']),
                          ('expected_response',service['expected_response']),('expected_max_model_len',service['max_model_len'])]:
        if provider.get(key) != expected:
            fail('producer does not match its documented role: ' + key)
    generation = {k:provider[k] for k in ('max_tokens','temperature','seed','thinking_token_budget') if k in provider}
    generation_kwargs(generation, model_role=role)
    successor_122b = role == '122B' and d.get('successor_lineage') is not None
    if successor_122b and stage in {
            'technical_qualification_122b', 'producer_conformity', 'producer_remediation'}:
        require_122b_no_thinking(provider.get('extra_body'), context=stage)
    else:
        producer_extra_body(provider.get('extra_body'), model_role=role)
    if provider['max_tokens'] > service['max_output_tokens']:
        fail('producer output exceeds documented limit')
    return role


def validate_binding(binding, stage, ledger, connection):
    # Generic v2 ledgers remain available as offline/forensic objects. Scientific runners
    # always attach execution_config; their real providers separately require D9 authorization.
    if 'execution_config' not in binding:
        return
    config = binding['execution_config']
    from .guards import require_execution
    require_execution(config)
    expected_ledger = {'path':str(ledger.identity_path), 'pilot_id':ledger.pilot_id}
    if config.get('pilot_ledger') != expected_ledger:
        fail('binding belongs to another pilot ledger')
    validate_history(config, ledger, connection)
    d = config['d9']; role = model_for_stage(stage); service = d['services'][role]
    if stage == 'alternate_conformity' and d['alternate_placement'] != 'pilot':
        fail('alternate is not authorized in this pilot')
    if stage in {'budget_probe', 'stability_gate'} and d['alternate_placement'] == 'pilot':
        ledger._successful(connection, 'alternate_conformity')
    if any(s['model'] != service['model'] for s in binding.get('requests', [])):
        fail('persisted request model differs from the stage role')
    producer_stage = stage in {'technical_qualification_122b', 'producer_conformity',
                               'producer_remediation', 'alternate_conformity'}
    if producer_stage and 'provider' not in binding:
        fail('producer binding lacks its certified provider')
    if not producer_stage and any(spec['producer'] != 'consumer' for spec in binding['requests']):
        fail('consumer request has an invalid role')
    if 'provider' in binding:
        provider=binding['provider']
        reference=binding.get('provider_reference')
        if read_reference(reference, 'persisted producer configuration') != provider or reference['sha256'] != binding.get('provider_file_sha256'):
            fail('persisted producer content differs from certified bytes')
        if any(spec['producer'] != provider['name'] for spec in binding['requests']):
            fail('producer request role differs from provider binding')
        # The runner carries the exact file hash as well as parsed content.
        validate_provider(config, provider, stage, file_sha256=binding.get('provider_file_sha256'))
    # Reconfirm recoverable bytes at each decision, including direct reservations,
    # restart and reuse. Neither declared pins nor a previously created counter suffice.
    # Use the same file/template contract as the runner; R4 and service chat are distinct.
    from .guards import verify_tokenizer
    verify_tokenizer(Path(d['r4_snapshot']), **R4_TOKENIZER)
    chat_snapshot = binding.get('tokenizer_snapshot')
    if not isinstance(chat_snapshot, str) or not Path(chat_snapshot).is_absolute():
        fail('binding lacks its recoverable service tokenizer snapshot')
    verify_tokenizer(Path(chat_snapshot), **service['tokenizer'])
    for row in connection.execute('SELECT stage,binding_json FROM stages'):
        other=json.loads(row['binding_json'])
        if 'execution_config' in other and other['execution_config'] != config:
            fail('configuration changed between stages; no implicit ledger reset/rebinding')


def r4_counter(config, counter_factory):
    from .guards import verify_tokenizer
    d = validate_config(config); snapshot=Path(d['r4_snapshot'])
    verify_tokenizer(snapshot, **R4_TOKENIZER)
    return counter_factory(snapshot, chat_template=False)


def accounting(ledger):
    """Validated counts of intents, not proof of receipt at the service."""
    by_role={key:0 for key in ROLES}; by_model={'122B':0, '27B':0}
    with ledger._transaction() as c:
        rows=ledger._validated_attempt_inventory(c)
        historical=ledger._quota_predecessors(c)
        for row in rows:
            binding=ledger._binding(c,row['stage'])
            if 'execution_config' not in binding:
                fail('unmapped historical ledger requires separate reviewed reconciliation')
            role=('technical_qualification' if row['stage']=='technical_qualification_122b'
                  else 'alternate' if row['stage']=='alternate_conformity'
                  else 'consumer' if row['stage'] in {'budget_probe','stability_gate'}
                  else 'producer')
            if role == 'technical_qualification' and role not in by_role:
                by_role[role] = 0
            by_role[role] += 1
            by_model['122B' if role == 'technical_qualification' else ROLES[role]] += 1
    return {'requests_cumulative':len(rows)+len(historical),'native_requests':len(rows),
            'historical_external':len(historical),'by_role':by_role,'by_nominal_model':by_model,
            'unit':'durable intents, including uncertain and retry attempts'}


def swap_manifest(primary_manifest, *, primary_handoff, alternate_handoff, config, ledger, schema_dir, token_count):
    """Authenticate both libraries and replace only insights; no scientific selection or calls.

    The caller supplies the already selected same cases. Pilot preparation continues to
    require the primary library; this helper does not create another gate or consumer.
    """
    from .guards import require_execution, require_pilot_ledger
    from .inputs import _insights
    require_execution(config); require_pilot_ledger(config, ledger)
    primary, _, p = _insights(primary_handoff, ledger=ledger, token_count=token_count, schema_dir=schema_dir)
    alternate, _, a = _insights(alternate_handoff, ledger=ledger, token_count=token_count, schema_dir=schema_dir, library_role='alternate')
    for provenance in (p, a):
        if ledger.binding(provenance['stage']).get('execution_config') != config:
            fail('swap library does not belong to this D9 configuration')
    if primary_manifest.get('insights') != primary:
        fail('swap source is not the authenticated primary library')
    result = deepcopy(primary_manifest); result['insights'] = alternate
    return result, {'primary':p, 'alternate':a, 'consumer':deepcopy(config['d9']['services']['122B']),
                    'scope':'same supplied cases; no new case selection or execution authorization'}
