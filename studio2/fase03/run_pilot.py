#!/usr/bin/env python3
"""Explicitly gated runner for the pre-gate budget probe and 40x3 stability gate.

Running without ``--execute`` only prints the call plan.  The budget stage must
finish and write ``frozen_gate_config.json`` before the stability stage can run.
"""

from __future__ import annotations

import argparse
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from typing import Any
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.protocol import (  # noqa: E402
    DIAGNOSTIC_SCHEMA_PATH,
    PREFLIGHT_CONFIG_PATH,
    ContractError,
    canonical_json,
    load_json,
    parse_diagnostic_output,
    sha256_file,
    sha256_text,
)
from studio2.fase03.harness.gate_rules import (  # noqa: E402
    evaluate_stability_gate,
    semantic_signature,
)
from studio2.fase03.harness.ledger import PilotLedger, digest
from studio2.fase03.harness.guards import require_execution, response_identity_valid, require_pilot_ledger
from studio2.fase03.harness.runtime import execute_request, durable_write  # noqa: E402


ACK = "EXECUTE_PHASE03_PRELIMINARY_PILOT"
PROVISIONAL_STRESS_ACK = "EXECUTE_PHASE03_PROVISIONAL_STRESS_PROBE"
DEFAULT_PREPARED = ROOT / "studio2/fase03/prepared"
DEFAULT_RESULTS = ROOT / "studio2/fase03/results"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def vllm_grammar_schema(schema: dict[str, Any]) -> dict[str, Any]:
    """Adapt only the server grammar; the canonical local contract stays strict."""
    grammar_schema = json.loads(canonical_json(schema))
    used_ids = grammar_schema.get("properties", {}).get("used_insight_ids", {})
    if used_ids.get("uniqueItems") is not True:
        raise RuntimeError("canonical diagnostic schema must require unique insight IDs")
    # vLLM 0.28.0 rejects this keyword before inference.  The local parser below
    # independently rejects duplicate IDs, so removing it here does not relax
    # acceptance of a provider response.
    del used_ids["uniqueItems"]
    return grammar_schema


def http_json(url: str, *, timeout: float = 30.0) -> dict[str, Any]:
    request = Request(url, method="GET")
    with urlopen(request, timeout=timeout) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"expected JSON object from {url}")
    return value


def process_provenance(config: dict[str, Any], vllm_version: str) -> dict[str, Any]:
    candidate = config["candidate"]
    port = candidate["base_url"].split(":")[-1].split("/")[0]
    matches: list[tuple[int, str]] = []
    for entry in Path("/proc").iterdir():
        if not entry.name.isdigit():
            continue
        try:
            command = (entry / "cmdline").read_bytes().replace(b"\0", b" ").decode().strip()
        except (OSError, UnicodeDecodeError):
            continue
        required = (
            "vllm serve",
            candidate["expected_model_root"],
            f"--revision {candidate['expected_model_revision']}",
            f"--port {port}",
            f"--served-model-name {candidate['requested_model']}",
            f"--max-model-len {candidate['expected_max_model_len']}",
            "--max-num-seqs 1",
        )
        if all(token in command for token in required):
            matches.append((int(entry.name), command))
    if len(matches) != 1:
        raise RuntimeError(f"expected exactly one matching vLLM process, found {len(matches)}")
    pid, command = matches[0]
    environment: dict[str, str] = {}
    for item in (Path("/proc") / str(pid) / "environ").read_bytes().split(b"\0"):
        if not item or b"=" not in item:
            continue
        key_raw, value_raw = item.split(b"=", 1)
        key = key_raw.decode("utf-8")
        if key.startswith(("VLLM_", "CUDA_")):
            environment[key] = value_raw.decode("utf-8")
    child_pids = [
        int(value)
        for value in (Path("/proc") / str(pid) / "task" / str(pid) / "children")
        .read_text(encoding="utf-8")
        .split()
    ]
    engine_core = []
    for child_pid in child_pids:
        try:
            child_command = (
                (Path("/proc") / str(child_pid) / "cmdline")
                .read_bytes()
                .replace(b"\0", b" ")
                .decode()
                .strip()
            )
        except (OSError, UnicodeDecodeError):
            continue
        if "VLLM::EngineCore" in child_command:
            engine_core.append(child_pid)
    if len(engine_core) != 1:
        raise RuntimeError(f"expected exactly one EngineCore child, found {len(engine_core)}")
    fingerprint_fields = {
        "api_server_pid": pid,
        "engine_core_pid": engine_core[0],
        "command": command,
        "environment": environment,
        "vllm_version": vllm_version,
    }
    observed = {
        **fingerprint_fields,
        "command_sha256": sha256_text(command),
        "environment_sha256": sha256_text(canonical_json(environment)),
        "fingerprint_sha256": sha256_text(canonical_json(fingerprint_fields)),
    }
    expected = candidate["expected_process"]
    checks = {
        "api_server_pid": observed["api_server_pid"],
        "engine_core_pid": observed["engine_core_pid"],
        "command": observed["command"],
        "command_sha256": observed["command_sha256"],
        "environment": observed["environment"],
        "environment_sha256": observed["environment_sha256"],
        "vllm_version": observed["vllm_version"],
        "fingerprint_sha256": observed["fingerprint_sha256"],
    }
    if checks != expected:
        raise RuntimeError(f"vLLM process fingerprint mismatch: observed={checks}, expected={expected}")
    return observed


def server_contract(config: dict[str, Any]) -> dict[str, Any]:
    require_execution(config)
    candidate = config["candidate"]
    origin = candidate["base_url"].removesuffix("/v1")
    version = http_json(f"{origin}/version")
    models = http_json(f"{candidate['base_url']}/models")
    openapi = http_json(f"{origin}/openapi.json")
    found = [
        item
        for item in models.get("data", [])
        if item.get("id") == candidate["requested_model"]
    ]
    if len(found) != 1:
        raise RuntimeError("requested model alias is missing or ambiguous")
    model = found[0]
    props = (
        openapi.get("components", {})
        .get("schemas", {})
        .get("ChatCompletionRequest", {})
        .get("properties", {})
    )
    observed = {
        "vllm_version": version.get("version"),
        "model_id": model.get("id"),
        "model_root": model.get("root"),
        "max_model_len": model.get("max_model_len"),
        "temperature_advertised": "temperature" in props,
        "seed_advertised": "seed" in props,
        "thinking_token_budget_advertised": "thinking_token_budget" in props,
        "reasoning_effort_advertised": "reasoning_effort" in props,
    }
    expected = {
        "vllm_version": candidate["expected_vllm_version"],
        "model_id": candidate["requested_model"],
        "model_root": candidate["expected_model_root"],
        "max_model_len": candidate["expected_max_model_len"],
    }
    if any(observed[key] != value for key, value in expected.items()):
        raise RuntimeError(f"server contract mismatch: observed={observed}, expected={expected}")
    observed["process"] = process_provenance(config, observed["vllm_version"])
    return observed


class Provider:
    def __init__(self, config: dict[str, Any]) -> None:
        require_execution(config)
        self.config = config
        try:
            import openai
            from openai import OpenAI
        except ImportError as exc:
            raise RuntimeError(
                "openai SDK is required; use /home/luca/fot-exp2/env-vllm/bin/python"
            ) from exc
        candidate = config["candidate"]
        self.sdk_version = openai.__version__
        self.model = candidate["requested_model"]
        self.client = OpenAI(
            api_key="local-vllm",
            base_url=candidate["base_url"],
            max_retries=0,
            timeout=600.0,
        )
        self.requests = 0
        self.hard_stop = config["call_budget"]["hard_stop_provider_requests"]

    def call(
        self,
        *,
        prompt: dict[str, Any],
        schema: dict[str, Any],
        generation: dict[str, Any],
    ) -> dict[str, Any]:
        require_execution(self.config)
        if self.requests >= self.hard_stop:
            raise RuntimeError("hard provider-request stop reached")
        self.requests += 1
        started_at = utc_now()
        begin = time.monotonic()
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt["text"]}],
            temperature=generation["temperature"],
            seed=generation["seed"],
            max_tokens=generation["max_tokens"],
            extra_body={"thinking_token_budget": generation["thinking_token_budget"]},
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "study2_diagnostic_output",
                    "strict": True,
                    "schema": schema,
                },
            },
        )
        return response.model_dump(mode="json")


def consumer_record(raw, prompt, generation):
    choices = raw.get('choices', [])
    choice = choices[0] if len(choices) == 1 else {}
    content = choice.get('message', {}).get('content') or ''
    parsed, error = None, None
    try:
        if len(choices) != 1:
            raise ContractError('provider must return exactly one choice')
        parsed = parse_diagnostic_output(content, label_space=prompt['label_space'], allowed_insight_ids=prompt['available_insight_ids'])
    except ContractError as exc:
        error = str(exc)
    usage = raw.get('usage') or {}
    return dict(**{k: prompt[k] for k in ('prompt_id','agent_id','case_id','condition','sample_role','prompt_sha256')},
                generation=generation, returned_model=raw.get('model'), system_fingerprint=raw.get('system_fingerprint'),
                response_id=raw.get('id'), finish_reason=choice.get('finish_reason'), raw_output=content,
                raw_output_sha256=sha256_text(content), parsed_output=parsed, parse_valid_first_attempt=error is None,
                parse_error=error, retry_count=0, **{k: usage.get(k) for k in ('prompt_tokens','completion_tokens','total_tokens')})


def load_prepared(prepared_dir: Path, *, expected_status='READY_FOR_PRE_GATE_GENERATION_PROBE', ledger=None):
    from studio2.fase03.harness.preparation import authenticate
    from studio2.fase03.prepare_gate import offline_token_counter
    from studio2.fase03.harness.render import build_real_pilot_sample
    from studio2.fase03.harness.guards import verify_tokenizer
    config = load_json(PREFLIGHT_CONFIG_PATH)
    require_execution(config)
    plan_path, prompt_path = prepared_dir/'pre_gate_plan.json', prepared_dir/'pilot_prompts.jsonl'
    hashes = load_json(prepared_dir/'pre_gate_hashes.json')['files']
    for path in (plan_path, prompt_path, PREFLIGHT_CONFIG_PATH):
        if hashes.get(str(path.resolve())) != sha256_file(path):
            raise RuntimeError('prepared hash mismatch: ' + str(path))
    plan = load_json(plan_path)
    source = Path(plan['source_manifest'])
    if sha256_file(source) != plan['source_manifest_sha256'] or hashes.get(str(source.resolve())) != sha256_file(source):
        raise RuntimeError('source manifest hash mismatch')
    if plan['status'] != expected_status or ledger is None or plan.get('pilot_id') != ledger.pilot_id:
        raise RuntimeError('prepared plan is not approved for this pilot')
    snapshot = Path(plan['tokenizer_snapshot'])
    verify_tokenizer(snapshot, **config['tokenizer'])
    counter = offline_token_counter(snapshot)
    raw_counter = offline_token_counter(snapshot, chat_template=False)
    inventory, manifest = load_json(Path(plan['source_inventory'])), load_json(source)
    authenticate(manifest, inventory, config=config, ledger=ledger, handoff=Path(plan['insight_handoff']),
                 schema_dir=Path(plan['schema_dir']), snapshot=snapshot, token_count=raw_counter)
    regenerated = build_real_pilot_sample(manifest, config, token_count=counter, insight_token_count=raw_counter,
                                         schema_dir=Path(plan['schema_dir']), source_inventory=inventory)
    prompts = read_jsonl(prompt_path)
    if prompts != regenerated:
        raise RuntimeError('prepared prompts differ from authenticated renderer output')
    from studio2.fase03.protocol import context_feasibility
    from types import SimpleNamespace
    if plan['context_feasibility'] != context_feasibility([SimpleNamespace(**r) for r in regenerated], config):
        raise RuntimeError('prepared generation budgets changed')
    for prompt in prompts:
        prompt['label_space'] = manifest['label_space']
    return plan, prompts


def request_spec(prompt, generation, *, config, logical_id, group, repetition):
    return dict(logical_id=logical_id, model=config['candidate']['requested_model'], producer='consumer',
                prompt_sha256=prompt['prompt_sha256'], case_sha256=digest([prompt['agent_id'],prompt['case_id']]),
                contract_sha256=digest(generation), condition=prompt['condition'], group=group, repetition=repetition)


def _tracked_call(provider, ledger, *, prompt, schema, generation, stage, stage_run, logical_id,
                  request_id=None, return_error_record=False, config=None, journal_path=None,
                  resume=False, retry_requests=(), repetition=1, pre_reserved=()):
    config = load_json(PREFLIGHT_CONFIG_PATH) if config is None else config
    require_execution(config)
    require_pilot_ledger(config, ledger)
    binding = ledger.binding(stage)
    if stage_run != digest(binding):
        raise RuntimeError('tracked call binding mismatch')
    spec = next(s for s in binding['requests'] if s['logical_id'] == logical_id)
    if spec['prompt_sha256'] != sha256_text(prompt['text']) or spec['contract_sha256'] != digest(generation):
        raise RuntimeError('tracked prompt/generation bytes changed')
    def evaluate(raw):
        return dict(consumer_record(raw, prompt, generation), repetition=repetition)
    return execute_request(ledger=ledger, stage=stage, spec=spec,
                           transport=lambda: provider.call(prompt=prompt, schema=schema, generation=generation),
                           evaluate=evaluate, expected_identity=config['expected_response'],
                           journal_path=journal_path or ledger.path.with_suffix('.journal.jsonl'),
                           resume=resume, retry_requests=retry_requests, pre_reserved=pre_reserved)


def _probe_retry(ledger, stage, retry_requests):
    selected = []
    for request_id in retry_requests:
        row = ledger.request(request_id)
        if row is None or row['stage'] != stage or row['status'] != 'ZERO_TOKEN_PROVEN':
            raise RuntimeError('explicit probe retry is not a proven zero-token original')
        spec = json.loads(row['identity_json'])
        selected.append(dict(request_id=digest([ledger.pilot_id, stage, spec['logical_id'], request_id]),
                             logical_id=spec['logical_id'], model=spec['model'], producer=spec['producer'],
                             stage_run=row['stage_run'], retry_of=request_id, condition=spec['condition']))
    if selected:
        ledger.reserve_probe_transport_triplet(selected)
    return [r['request_id'] for r in selected]


def run_budget_stage(prepared_dir: Path, results_dir: Path, *, ledger: PilotLedger, resume=False, retry_requests=()):
    config = load_json(PREFLIGHT_CONFIG_PATH)
    require_execution(config)
    require_pilot_ledger(config, ledger)
    response_identity_valid({}, config.get('expected_response', {}))
    plan, prompts = load_prepared(prepared_dir, ledger=ledger)
    schema = vllm_grammar_schema(load_json(DIAGNOSTIC_SCHEMA_PATH))
    stress = {condition: max((p for p in prompts if p['condition']==condition), key=lambda p:p['input_tokens']) for condition in ('A','B-LF','E-LF')}
    specs, jobs = [], []
    for candidate in plan['context_feasibility']['feasible_candidates']:
        generation = dict(temperature=config['generation_budget']['temperature'], seed=config['generation_budget']['seed'], **candidate)
        # Only the two probed generation fields are admissible here.
        generation = {k:generation[k] for k in ('temperature','seed','thinking_token_budget','max_tokens')}
        group = str(candidate['thinking_token_budget'])
        for condition in ('A','B-LF','E-LF'):
            logical = f'budget:{group}:{condition}'
            spec = request_spec(stress[condition], generation, config=config, logical_id=logical, group=group, repetition=1)
            specs.append(spec); jobs.append((spec,stress[condition],generation))
    binding = dict(requests=specs, config_sha256=digest(config), prompts_sha256=digest(prompts), schema_sha256=digest(schema))
    ledger.bind_stage('budget_probe', binding)
    reserved = _probe_retry(ledger, 'budget_probe', retry_requests) if resume else []
    server = server_contract(config)
    provider = Provider(config)
    records, selected = [], None
    for offset in range(0,len(jobs),3):
        transport_failures = []
        for spec, prompt, generation in jobs[offset:offset+3]:
            try:
                records.append(_tracked_call(provider, ledger, prompt=prompt, schema=schema, generation=generation,
                                             stage='budget_probe', stage_run=digest(binding), logical_id=spec['logical_id'],
                                             config=config, journal_path=results_dir/'budget_probe_journal.jsonl',
                                             resume=resume, retry_requests=retry_requests, pre_reserved=reserved))
            except Exception:
                leaf = ledger.leaf('budget_probe', spec['logical_id'])
                if not resume and leaf and leaf['status'] == 'FAILED':
                    # Finish only the remaining original members of this planned triplet.
                    # No request is resent and no following budget group is started.
                    transport_failures.append(leaf['request_id'])
                else:
                    raise
        if transport_failures:
            raise RuntimeError('probe transport triplet unresolved; explicit evidence/retry triplet required: ' + ','.join(transport_failures))
        if all(r['finish_reason']=='stop' and r['parse_valid_first_attempt'] for r in records[-3:]):
            selected = jobs[offset][2]
            break
    frozen = dict(artifact_version='2', status='FROZEN_FOR_STABILITY_GATE' if selected else 'NO_GO_GENERATION_BUDGET',
                  generation=selected, candidate=config['candidate'], config_sha256=digest(config), server=server,
                  prompt_file_sha256=sha256_file(prepared_dir/'pilot_prompts.jsonl'),
                  pre_gate_plan_sha256=sha256_file(prepared_dir/'pre_gate_plan.json'), schema_sha256=digest(schema),
                  records_sha256=digest(records), prompt_sample=prompts, pilot_id=ledger.pilot_id,
                  go_scope='Only authenticated configuration; no pilot GO or scientific qualification')
    summary = dict(records_sha256=digest(records), frozen_sha256=digest(frozen))
    ledger.record_stage_outcome('budget_probe', outcome='PASS' if selected else 'FAIL', artifact_sha256=digest(summary), artifact=summary, frozen=frozen)
    durable_write(results_dir/'budget_probe_records.jsonl', ''.join(canonical_json(r)+'\n' for r in records))
    durable_write(results_dir/'frozen_gate_config.json', json.dumps(frozen,indent=2,ensure_ascii=False)+'\n')
    return frozen


def run_provisional_stress_budget_stage(
    prepared_dir: Path, results_dir: Path
) -> dict[str, Any]:
    """Historical path disabled, including direct Python callers."""
    raise RuntimeError('historical synthetic stress transport is disabled')


def divergence_signature(record: dict[str, Any]) -> str:
    return sha256_text(canonical_json(semantic_signature(record)))


def run_stability_stage(prepared_dir: Path, results_dir: Path, *, ledger: PilotLedger, resume=False):
    config = load_json(PREFLIGHT_CONFIG_PATH)
    require_execution(config)
    require_pilot_ledger(config, ledger)
    response_identity_valid({}, config.get('expected_response', {}))
    plan, prompts = load_prepared(prepared_dir, ledger=ledger)
    path = results_dir/'frozen_gate_config.json'
    frozen = load_json(path)
    ledger.authenticate_frozen(frozen)
    if path.read_bytes() != (json.dumps(frozen,indent=2,ensure_ascii=False)+'\n').encode():
        raise RuntimeError('frozen configuration bytes changed')
    schema = vllm_grammar_schema(load_json(DIAGNOSTIC_SCHEMA_PATH))
    if frozen['status'] != 'FROZEN_FOR_STABILITY_GATE' or frozen['config_sha256'] != digest(config) or frozen['prompt_sample'] != prompts or frozen['schema_sha256'] != digest(schema) or frozen['pre_gate_plan_sha256'] != sha256_file(prepared_dir/'pre_gate_plan.json'):
        raise RuntimeError('frozen gate provenance mismatch')
    specs = [request_spec(p, frozen['generation'], config=config, logical_id=f"{p['prompt_id']}:r{r}", group=p['prompt_id'], repetition=r) for p in prompts for r in (1,2,3)]
    binding = dict(requests=specs, frozen_sha256=digest(frozen), config_sha256=digest(config))
    ledger.bind_stage('stability_gate', binding)
    server = server_contract(config)
    if server != frozen['server']:
        raise RuntimeError('server identity changed since probe')
    provider = Provider(config)
    records = []
    for spec in specs:
        prompt = next(p for p in prompts if p['prompt_id'] == spec['group'])
        records.append(_tracked_call(provider, ledger, prompt=prompt, schema=schema, generation=frozen['generation'],
                                     stage='stability_gate', stage_run=digest(binding), logical_id=spec['logical_id'], config=config,
                                     repetition=spec['repetition'], journal_path=results_dir/'stability_journal.jsonl', resume=resume))
    gate = evaluate_stability_gate(records, expected_prompts=frozen['prompt_sample'])
    summary = dict(artifact_version='2', **gate, records_sha256=digest(records), frozen_gate_config_sha256=digest(frozen))
    ledger.record_stage_outcome('stability_gate', outcome='PASS' if gate['t3_pass'] and gate['t4_pass'] and gate['t6_evaluable'] else 'FAIL', artifact_sha256=digest(summary), artifact=summary)
    durable_write(results_dir/'stability_records.jsonl', ''.join(canonical_json(r)+'\n' for r in records))
    durable_write(results_dir/'stability_summary.json',json.dumps(summary,indent=2)+'\n')
    return summary


def print_plan(config: dict[str, Any]) -> None:
    calls = config["call_budget"]
    print(
        json.dumps(
            {
                "status": "PLAN_ONLY_NO_PROVIDER_CALLS",
                "script": str(Path(__file__).resolve()),
                "pre_gate_budget_calls_max": calls["pre_gate_generation_budget_max"],
                "pre_gate_budget_calls_per_candidate": 3,
                "budget_candidates_in_order": config["generation_budget"][
                    "thinking_token_budget_candidates"
                ],
                "budget_selection_rule": (
                    "Select the first candidate whose A, B-LF and E-LF stress calls all "
                    "finish without length truncation and parse validly on the first attempt."
                ),
                "provisional_stress_probe": {
                    "scope": "synthetic cap-stress fixture only",
                    "maximum_calls": calls["pre_gate_generation_budget_max"],
                    "writes_gate_freeze": False,
                    "real_prompt_repeat_required": True,
                    "stability_gate_authorized": False,
                },
                "stability_gate_calls": calls["stability_gate"],
                "qwen_producer_conformance_calls": calls["qwen_producer_conformance"],
                "alternate_producer_calls_deferred": calls[
                    "alternate_producer_conformance_deferred"
                ],
                "base_total_without_alternate_range": calls["base_total_without_alternate_range"],
                "base_total_with_alternate_range": calls["base_total_with_alternate_range"],
                "shared_reserve": calls["shared_reserve"],
                "planned_max_without_alternate": calls["planned_max_without_alternate"],
                "planned_max_with_alternate": calls["planned_max_with_alternate"],
                "hard_stop_provider_requests": calls["hard_stop_provider_requests"],
                "persistent_ledger": calls["persistent_ledger"],
                "temporal_feasibility": "NOT_VERIFIED_OFFLINE; measure on the D9-selected and qualified configuration with 20% margin",
                "d9_model_roles": "UNDECIDED",
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--stage",
        choices=("budget", "stability", "provisional-stress-budget"),
    )
    parser.add_argument("--prepared-dir", type=Path, default=DEFAULT_PREPARED)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retry-request", action="append", default=[])
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--pilot-id")
    args = parser.parse_args()
    config = load_json(PREFLIGHT_CONFIG_PATH)
    if not args.execute:
        print_plan(config)
        return 0
    if args.stage is None:
        raise SystemExit(
            "execution requires --stage budget, stability or provisional-stress-budget"
        )
    required_ack = (
        PROVISIONAL_STRESS_ACK
        if args.stage == "provisional-stress-budget"
        else ACK
    )
    if args.acknowledge != required_ack:
        raise SystemExit(f"execution requires --acknowledge {required_ack}")
    if args.stage == "provisional-stress-budget":
        raise SystemExit(
            "the historical synthetic stress execution path is disabled; rev.10 requires real frozen prompts and cumulative accounting"
        )
    if args.ledger is None or args.pilot_id is None:
        raise SystemExit("execution requires --ledger ABSOLUTE_PATH and --pilot-id")
    ledger = PilotLedger(args.ledger, pilot_id=args.pilot_id)
    if args.stage == "budget":
        result = run_budget_stage(args.prepared_dir, args.results_dir, ledger=ledger, resume=args.resume, retry_requests=args.retry_request)
    elif args.stage == "stability":
        result = run_stability_stage(args.prepared_dir, args.results_dir, ledger=ledger, resume=args.resume)
    else:  # unreachable: retained only so historical artifacts remain readable
        raise AssertionError("disabled provisional stage")
    print(canonical_json(result))
    return 0 if not result["status"].startswith("NO_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
