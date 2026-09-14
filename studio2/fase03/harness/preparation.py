"""Authenticate all sources before ordinary real-prompt preparation and reloading."""
from pathlib import Path
from copy import deepcopy

from .common import HarnessError, load_json, require_sha256, sha256_text
from .inputs import (verified_pending_inventory, _insights, PSEUDOLABEL_SHA256,
                     ASSIGNMENT_SHA256, DERANGEMENT_SHA256)
from .guards import require_execution, verify_tokenizer, require_presentation, require_pilot_ledger


def authenticate(manifest, inventory, *, config, ledger, handoff, schema_dir, snapshot, token_count):
    require_execution(config)
    require_pilot_ledger(config, ledger)
    verify_tokenizer(snapshot, **config['tokenizer'])
    require_presentation(inventory, config['presentation_approval'])
    pending = verified_pending_inventory()
    expected = deepcopy(pending)
    expected.update(status='COMPLETE_READY_TO_FREEZE', provenance_kind='study2_scientific', missing_requirements=[])
    expected['presentation']['author_decision'] = 'accepted'
    library, _, provenance = _insights(handoff, ledger=ledger, token_count=token_count, schema_dir=schema_dir)
    expected['sources']['insight_validation'] = provenance
    if inventory != expected:
        raise HarnessError('source inventory changed from authenticated development inputs')
    base = Path(__file__).resolve().parents[1]
    for name, pin in [('PSEUDOLABEL_MAP.json', PSEUDOLABEL_SHA256), ('AGENT_ASSIGNMENT.json', ASSIGNMENT_SHA256), ('CONDITION_E_DERANGEMENTS.json', DERANGEMENT_SHA256)]:
        require_sha256(base/'pseudolabel'/name, pin, role='03.7 canonical input')
    labels = load_json(base/'pseudolabel/PSEUDOLABEL_MAP.json')
    agents = load_json(base/'pseudolabel/AGENT_ASSIGNMENT.json')['agents']
    derangements = load_json(base/'pseudolabel/CONDITION_E_DERANGEMENTS.json')['derangements']
    expected_manifest = dict(artifact_version='1', status='FROZEN_FOR_PHASE03_PRE_GATE', provenance_kind='study2_scientific',
                             source_commit=pending['assembly_base_commit'], catalog_id=labels['namespace'],
                             label_space=labels['label_space'], agents=agents, development_cases=manifest.get('development_cases'),
                             local_examples=pending['producer_conformance_inputs']['local_examples'], insights=library,
                             derangements=derangements, transfer_case_by_agent=pending['selection']['transfer_case_by_agent'])
    if manifest != expected_manifest:
        raise HarnessError('executable manifest changed from canonical sources/producer cycle')
    cases = manifest.get('development_cases', [])
    if len(cases) != 320 or len({r.get('case_id') for r in cases}) != 320:
        raise HarnessError('development coverage mismatch')
    frozen = {r['case_id']: r for r in pending['development_cases']}
    for r in cases:
        source = frozen.get(r.get('case_id'))
        if source is None or r.get('split') != 'development' or r.get('fault_label') != labels['label_by_identifier'][source['evaluator']['fault']] or r.get('neutral_text_sha256') != source['neutral_text_sha256'] or sha256_text(r.get('neutral_text','')) != source['neutral_text_sha256']:
            raise HarnessError('development prompt bytes/provenance mismatch')
