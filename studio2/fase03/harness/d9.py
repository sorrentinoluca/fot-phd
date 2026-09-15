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
                'alternate_conformity': '27B', 'budget_probe': '122B', 'stability_gate': '122B'}
R4_TOKENIZER = {
    'revision': '017b9c7af6b5689d5dd426a76e0bc077eb5ca20a',
    'tokenizer_json_sha256': '0997f410c57a1f4e53b09e4be8f4a172d90edd9564368fb0847030937229b9f3',
    'tokenizer_config_sha256': 'b11349aafa7cdc6a320767cf7ceb29ed82f7eda5d65e8e0819e76f0ce947bf27',
    'chat_template_sha256': 'c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041'}
HISTORY_SOURCE = {'sha256': 'c9adf2a8f07d9058257cc2c51a00064662874611875a715c716a1f1ea4828368',
                  'reported_requests': 4, 'completed_inferences': 3}


def fail(message):
    raise HarnessError('D9: ' + message)


def model_for_stage(stage):
    if stage not in STAGE_MODELS:
        fail('unsupported stage/arm')
    return STAGE_MODELS[stage]


def _text(value):
    return isinstance(value, str) and bool(value.strip()) and value.upper() not in {'PENDING', 'UNDECIDED', 'UNKNOWN'}


def _hash(value):
    return isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value) is not None


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
    history = read_reference(d.get('history_reconciliation'), 'historical consumption reconciliation')
    if history.get('status') != 'RECONCILED' or not _text(history.get('reviewer')) or history.get('source') != HISTORY_SOURCE:
        fail('historical S consumption requires reviewed reconciliation')
    if history.get('pilot_ledger') != config.get('pilot_ledger'):
        fail('historical reconciliation belongs to another ledger')
    mappings = history.get('request_identities')
    if not isinstance(mappings, dict) or len(mappings) != HISTORY_SOURCE['reported_requests'] or not all(_text(k) and _hash(v) for k,v in mappings.items()):
        fail('each historical request must map once to durable identity')
    return d


def validate_history(config, ledger, connection):
    d = validate_config(config)
    h = read_reference(d['history_reconciliation'], 'historical consumption reconciliation')
    # Read in the caller's decision transaction. No migration, reset, new row or backfill.
    rows = {r['request_id']:r for r in ledger._rows(connection)}
    for request_id, identity_hash in h['request_identities'].items():
        if request_id not in rows or sha256_bytes(rows[request_id]['identity_json'].encode()) != identity_hash:
            fail('historical request is not represented in this ledger')


def validate_provider(config, provider, stage, *, file_sha256):
    d = validate_config(config); role = model_for_stage(stage)
    if stage not in {'producer_conformity', 'producer_remediation', 'alternate_conformity'}:
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
    expected_ledger = {'path':str(ledger.path), 'pilot_id':ledger.pilot_id}
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
    producer_stage = stage in {'producer_conformity', 'producer_remediation', 'alternate_conformity'}
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
        for row in rows:
            binding=ledger._binding(c,row['stage'])
            if 'execution_config' not in binding:
                fail('unmapped historical ledger requires separate reviewed reconciliation')
            role='alternate' if row['stage']=='alternate_conformity' else ('consumer' if row['stage'] in {'budget_probe','stability_gate'} else 'producer')
            by_role[role]+=1;by_model[ROLES[role]]+=1
    return {'requests_cumulative':len(rows),'by_role':by_role,'by_nominal_model':by_model,
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
