#!/usr/bin/env python3
"""R4 producer-conformance runner; plan-only unless explicitly acknowledged."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness.common import HarnessError, canonical_json, load_json, sha256_file, sha256_text  # noqa: E402
from studio2.fase03.harness.inputs import SCHEMA_MANIFEST_SHA256, SCHEMA_TARGET_COMMIT  # noqa: E402
from studio2.fase03.harness.insight_adapter import validate_produced_pair  # noqa: E402
from studio2.fase03.harness.ledger import PilotLedger  # noqa: E402
from studio2.fase03.harness.producer import build_producer_prompt  # noqa: E402
from studio2.fase03.prepare_gate import DEFAULT_SNAPSHOT, offline_token_counter  # noqa: E402
from studio2.fase03.protocol import PREFLIGHT_CONFIG_PATH, strict_json_loads  # noqa: E402


ACK = "EXECUTE_PHASE03_PRODUCER_CONFORMANCE"
DEFAULT_RESULTS = ROOT / "studio2/fase03/results"
DEFAULT_SCHEMA_DIR = ROOT / "studio2/fase03/schema_insight"


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def response_schema(expected: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    properties = []
    for fixed in expected:
        properties.append({
            "type": "object", "additionalProperties": False,
            "required": [*config["insight_contract"]["fixed_fields"], "observed_pattern"],
            "properties": {
                "insight_id": {"const": fixed["insight_id"]},
                "source_agent": {"const": fixed["source_agent"]},
                "pseudolabel": {"const": fixed["pseudolabel"]},
                "evidence_scope": {"const": fixed["evidence_scope"]},
                "variable_ids": {"const": fixed["variable_ids"]},
                "observed_pattern": {"type": "string", "minLength": 1,
                    "maxLength": config["insight_contract"]["observed_pattern_max_characters"]},
            },
        })
    return {"type": "object", "additionalProperties": False, "required": ["insights"],
            "properties": {"insights": {"type": "array", "minItems": 2, "maxItems": 2,
                                           "prefixItems": properties, "items": False}}}


def provider_config(path: Path | None) -> dict[str, Any]:
    if path is None:
        raise HarnessError("execution requires a separately frozen provider config after D9; the historical 27B record is not a default")
    value = load_json(path)
    required = {"name", "base_url", "model", "max_tokens",
                "expected_max_model_len", "identity_sha256", "expected_response", "tokenizer"}
    if not isinstance(value, dict) or not required <= set(value) or set(value) - required - {'temperature','seed','thinking_token_budget'}:
        raise HarnessError(f"producer provider config keys must be {sorted(required)}")
    if not isinstance(value["identity_sha256"], str) or len(value["identity_sha256"]) != 64:
        raise HarnessError("provider identity requires a full SHA-256")
    return value


def _conformance_inputs(inventory: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    if inventory.get("status") != "INCOMPLETE":
        raise HarnessError("producer input inventory must remain incomplete until insights are produced")
    if inventory.get("missing_requirements") != ["16 real schema-valid producer insights"]:
        raise HarnessError("producer inventory has unresolved requirements other than its output library")
    schema = inventory.get("sources", {}).get("schema_contract", {})
    if schema.get("target_commit") != SCHEMA_TARGET_COMMIT or schema.get("manifest_sha256") != SCHEMA_MANIFEST_SHA256:
        raise HarnessError("producer inventory does not pin the published R4 contract")
    inputs = inventory.get("producer_conformance_inputs")
    if not isinstance(inputs, dict) or inputs.get("scientific_library_present") is not False:
        raise HarnessError("producer inputs must not contain a pre-existing scientific insight library")
    examples, contracts = inputs.get("local_examples"), inputs.get("fixed_insight_contracts")
    if not isinstance(examples, dict) or not isinstance(contracts, list) or len(contracts) != 16:
        raise HarnessError("producer conformance inputs are incomplete")
    from studio2.fase03.harness.inputs import verify_conformance_inventory
    verify_conformance_inventory(inventory)
    return examples, contracts


def run(*, source_inventory: Path, results_dir: Path, provider_path: Path, snapshot: Path,
        schema_dir: Path, ledger: PilotLedger, stage: str, resume=False, retry_requests=(),
        template_path: Path | None = None, diagnosis: str | None = None) -> dict[str, Any]:
    from studio2.fase03.harness.guards import require_execution, verify_tokenizer, require_pilot_ledger, response_identity_valid
    from studio2.fase03.harness.insight_adapter import load_validator, context_from_inventory, assert_context_compatible
    from studio2.fase03.harness.ledger import digest
    from studio2.fase03.harness.runtime import execute_request, durable_write
    preflight = load_json(PREFLIGHT_CONFIG_PATH)
    require_execution(preflight)
    require_pilot_ledger(preflight, ledger)
    inventory = load_json(source_inventory)
    examples, contracts = _conformance_inputs(inventory)
    provider = provider_config(provider_path)
    response_identity_valid({}, provider['expected_response'])
    if sha256_file(provider_path) not in preflight.get('approved_producer_config_sha256', []):
        raise HarnessError('producer config is not covered by execution approval')
    from studio2.fase03.harness.d9 import validate_provider, r4_counter, generation_kwargs
    role = validate_provider(preflight, provider, stage, file_sha256=sha256_file(provider_path))
    verify_tokenizer(snapshot, **provider['tokenizer'])
    validator = load_validator(schema_dir)
    assert_context_compatible(validator, context_from_inventory(inventory))
    count = r4_counter(preflight, offline_token_counter)
    chat_count = offline_token_counter(snapshot, chat_template=True)
    from studio2.fase03.harness.producer import PRODUCER_TEMPLATE
    template = PRODUCER_TEMPLATE if template_path is None else template_path.read_bytes().decode('utf-8')
    if stage != 'producer_remediation' and template != PRODUCER_TEMPLATE:
        raise HarnessError('only authorized remediation may change producer template')
    prepared, specs = [], []
    for i in range(1, 9):
        agent_id = f'agent_{i}'
        prompt = build_producer_prompt(agent_id=agent_id, local_examples=examples[agent_id], fixed_contracts=contracts, template=template)
        fixed = sorted((r for r in contracts if r['source_agent'] == agent_id), key=lambda r: r['insight_id'])
        margin = provider['expected_max_model_len'] - chat_count(prompt) - provider['max_tokens']
        if margin < preflight['generation_budget']['context_safety_margin_tokens']:
            raise HarnessError('producer prompt does not fit frozen context')
        spec = dict(logical_id=agent_id, model=provider['model'], producer=provider['name'],
                    prompt_sha256=sha256_text(prompt), case_sha256=digest(examples[agent_id]),
                    contract_sha256=digest(fixed), condition='producer', group=agent_id, repetition=1)
        specs.append(spec)
        prepared.append((spec, prompt, fixed))
    binding = dict(requests=specs, template_text=template, inventory_sha256=digest(inventory),
                   provider=provider, tokenizer=provider['tokenizer'], schema_manifest_sha256=SCHEMA_MANIFEST_SHA256,
                   execution_config=preflight, provider_file_sha256=sha256_file(provider_path),
                   provider_reference={'path':str(provider_path.resolve()),'sha256':sha256_file(provider_path)})
    ledger.bind_stage(stage, binding)
    # Reject any uncertain restart before constructing a client or sending later requests.
    from openai import OpenAI
    client = OpenAI(api_key=os.environ.get('STUDIO2_PRODUCER_API_KEY', 'local-vllm'),
                    base_url=provider['base_url'], max_retries=0, timeout=600.0)
    records = []
    journal = results_dir / f'producer_{stage}_journal.jsonl'
    for spec, prompt, fixed in prepared:
        require_execution(preflight)
        verify_tokenizer(snapshot, **provider['tokenizer'])
        load_validator(schema_dir)
        _conformance_inputs(load_json(source_inventory))
        if provider_config(provider_path) != provider:
            raise HarnessError('producer provider config changed during stage')
        kwargs = dict(model=provider['model'], messages=[dict(role='user', content=prompt)], max_tokens=provider['max_tokens'],
                      response_format={'type': 'json_schema', 'json_schema': {'name': 'study2_insight_pair', 'strict': True, 'schema': response_schema(fixed, preflight)}})
        validate_provider(preflight, provider, stage, file_sha256=sha256_file(provider_path))
        count = r4_counter(preflight, offline_token_counter)
        kwargs.update(generation_kwargs({k:provider[k] for k in ('max_tokens','temperature','seed','thinking_token_budget') if k in provider}, model_role=role))
        def transport():
            ledger.bind_stage(stage, binding)
            require_execution(preflight)
            response = client.chat.completions.create(**kwargs)
            return response.model_dump(mode='json')
        def evaluate(raw):
            choices = raw.get('choices', [])
            content = choices[0].get('message', {}).get('content') if len(choices) == 1 else None
            error, error_class = None, None
            try:
                parsed = strict_json_loads(content)
                if not isinstance(parsed, dict) or set(parsed) != {'insights'}:
                    raise HarnessError('producer response must contain only insights')
                validate_produced_pair(parsed['insights'], inventory=inventory, agent_id=spec['logical_id'], token_count=count, schema_dir=schema_dir)
            except Exception as exc:
                error = str(exc)
                code = getattr(exc, 'code', None)
                error_class = {'cap':'cap','leakage':'leakage','fixed':'identifiers','variable':'identifiers','schema':'structure','json':'structure','cardinality':'structure'}.get(code)
                if code is None and isinstance(exc, (ValueError, TypeError)):
                    error_class = 'structure'
            usage = raw.get('usage') or {}
            return dict(agent_id=spec['logical_id'], returned_model=raw.get('model'), system_fingerprint=raw.get('system_fingerprint'),
                        response_id=raw.get('id'), raw_output=content, schema_valid_first_attempt=error is None,
                        validation_error=error, validation_class=error_class, finish_reason=choices[0].get('finish_reason') if len(choices)==1 else None,
                        **{k: usage.get(k) for k in ('prompt_tokens','completion_tokens','total_tokens')})
        records.append(execute_request(ledger=ledger, stage=stage, spec=spec, transport=transport, evaluate=evaluate,
                                      expected_identity=provider['expected_response'], journal_path=journal,
                                      resume=resume, retry_requests=retry_requests))
    passed = all(r['schema_valid_first_attempt'] for r in records)
    summary = dict(artifact_version='4', status='PASS' if passed else 'FAIL', stage=stage,
                   producer_identity_sha256=digest(provider), provider_requests=ledger.snapshot()['requests_by_stage'][stage],
                   evaluable_calls=len(records),
                   valid_first_attempts=sum(r['schema_valid_first_attempt'] for r in records), records_sha256=digest(records),
                   binding_sha256=digest(binding), r4_target_commit=SCHEMA_TARGET_COMMIT)
    ledger.record_stage_outcome(stage, outcome=summary['status'], artifact_sha256=digest(summary), artifact=summary, diagnosis=diagnosis)
    durable_write(results_dir / f'producer_conformance_{provider["name"]}_{stage}_summary.json', json.dumps(summary, indent=2)+'\n')
    if passed:
        library = sorted([x for r in records for x in json.loads(r['raw_output'])['insights']], key=lambda r: r['insight_id'])
        handoff = dict(schema_commit=SCHEMA_TARGET_COMMIT, schema_manifest_sha256=SCHEMA_MANIFEST_SHA256,
                       library=library, library_sha256=digest(library), validated=True, pilot_id=ledger.pilot_id,
                       stage=stage, binding_sha256=digest(binding), records_sha256=digest(records))
        durable_write(results_dir / f'validated_insight_library_{provider["name"]}_{stage}.json', json.dumps(handoff, indent=2)+'\n')
    return summary


def print_plan(preflight: dict[str, Any]) -> None:
    if 'd9' in preflight:
        print(json.dumps({'status':'PLAN_ONLY_NO_PROVIDER_CALLS', 'roles':preflight['d9']['roles'],
                          'alternate_placement':preflight['d9']['alternate_placement'],
                          'missing_requirements':preflight['d9']['missing_requirements'],
                          'calls_per_producer':8, 'insights_per_library':16, 'pilot_go':False}, indent=2))
        return
    print(json.dumps({"status": "PLAN_ONLY_NO_PROVIDER_CALLS", "calls_per_producer": 8,
                      "insights_per_call": 2, "global_insights_checked": 16,
                      "contract": {"revision": 4, "target_commit": SCHEMA_TARGET_COMMIT,
                                   "manifest_sha256": SCHEMA_MANIFEST_SHA256},
                      "producer_inputs": "verified development examples plus fixed contracts; no insight library",
                      "resulting_library": "written only after 16/16 first-attempt R4 validation",
                      "provider_config": "D9: 122B primary, 27B alternate; separately documented and authorized",
                      "automatic_retries": 0, "persistent_ledger_required": True,
                      "fixed_fields": preflight["insight_contract"]["fixed_fields"],
                      "generated_field": preflight["insight_contract"]["producer_field"]},
                     indent=2, ensure_ascii=False))


def main() -> int:
    global PREFLIGHT_CONFIG_PATH
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-inventory", type=Path)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--provider-config", type=Path)
    parser.add_argument("--model-snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--schema-dir", type=Path, default=DEFAULT_SCHEMA_DIR)
    parser.add_argument("--stage", choices=("producer_conformity", "producer_remediation", "alternate_conformity"), default="producer_conformity")
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--pilot-id")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retry-request", action="append", default=[])
    parser.add_argument("--template", type=Path)
    parser.add_argument("--diagnosis", choices=("structure", "identifiers", "cap", "leakage"))
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    parser.add_argument("--config", type=Path, help="Explicit D9 execution configuration; historical default remains suspended")
    args = parser.parse_args()
    if args.config is not None:
        PREFLIGHT_CONFIG_PATH = args.config.resolve()
    preflight = load_json(PREFLIGHT_CONFIG_PATH)
    if not args.execute:
        print_plan(preflight)
        return 0
    if args.acknowledge != ACK:
        raise SystemExit(f"execution requires --acknowledge {ACK}")
    if any(value is None for value in (args.source_inventory, args.provider_config, args.ledger, args.pilot_id)):
        raise SystemExit("execution requires source inventory, provider config, absolute ledger and pilot id")
    from studio2.fase03.harness.guards import require_execution
    require_execution(preflight)
    ledger = PilotLedger(args.ledger, pilot_id=args.pilot_id)
    summary = run(source_inventory=args.source_inventory, results_dir=args.results_dir,
                  provider_path=args.provider_config, snapshot=args.model_snapshot, schema_dir=args.schema_dir,
                  ledger=ledger, stage=args.stage, resume=args.resume, retry_requests=args.retry_request, template_path=args.template, diagnosis=args.diagnosis)
    print(canonical_json(summary))
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
