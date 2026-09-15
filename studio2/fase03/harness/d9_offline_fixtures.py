"""Explicit D9 fixture adaptation. Never imported by production modules.

Patches only unavailable canonical tokenizer assets and prior consumption source with
synthetic zero-history fixtures. Real D9 configuration always requires the four S requests.
"""
from copy import deepcopy
from unittest.mock import patch
import json
from .common import sha256_file
from . import d9


def install(owner):
    owner.stack.enter_context(patch.object(d9,'R4_TOKENIZER',deepcopy(owner.tokenizer)))
    history_source={'sha256':'f'*64,'reported_requests':0,'completed_inferences':0}
    owner.stack.enter_context(patch.object(d9,'HISTORY_SOURCE',history_source))
    owner.provider_value.pop('temperature',None)
    owner.provider.write_text(json.dumps(owner.provider_value))
    alternate=deepcopy(owner.provider_value);alternate['name']='fixture-alternate';alternate['model']='fixture-alternate-model'
    alternate['expected_response']['returned_model']='fixture-alternate-model'
    owner.alternate_provider=owner.home/'alternate_provider.json';owner.alternate_provider.write_text(json.dumps(alternate))
    services={}
    for role,provider in [('122B',owner.provider_value),('27B',alternate)]:
        service={k:deepcopy(provider[k]) for k in ('model','base_url','identity_sha256','tokenizer','expected_response')}
        service.update(max_model_len=provider['expected_max_model_len'],max_output_tokens=16384)
        doc={k:'FIXTURE ONLY' for k in ('source','validity_date','weights_repository','weights_revision','quantization',
                'serving','parser','thinking','limit_semantics','sampling','error_policy','availability')}
        doc.update(status='documented',nominal_model=role,service=deepcopy(service))
        path=owner.home/(role+'_metadata.json');path.write_text(json.dumps(doc))
        service['documentation']={'path':str(path),'sha256':sha256_file(path)};services[role]=service
    history=owner.home/'history.json';history.write_text(json.dumps({'status':'RECONCILED','reviewer':'FIXTURE ONLY',
        'source':history_source,'pilot_ledger':owner.config['pilot_ledger'],'request_identities':{}}))
    owner.config['d9']={'roles':deepcopy(d9.ROLES),'status':'DOCUMENTED_FOR_AUTHORIZED_STAGE','missing_requirements':[],
        'alternate_placement':'deferred','presentation_order':list(owner.inventory['presentation']['ordered_labels']),'r4_tokenizer':deepcopy(owner.tokenizer),'r4_snapshot':str(owner.snapshot),
        'services':services,'producer_configs':{'122B':sha256_file(owner.provider),'27B':sha256_file(owner.alternate_provider)},
        'history_reconciliation':{'path':str(history),'sha256':sha256_file(history)}}
    owner.config['approved_producer_config_sha256']=list(owner.config['d9']['producer_configs'].values())
    owner.config['generation_budget'].pop('temperature',None)
