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
    required = {"name", "base_url", "model", "temperature", "seed", "max_tokens",
                "thinking_token_budget", "expected_max_model_len", "identity_sha256"}
    if not isinstance(value, dict) or set(value) != required:
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
    return examples, contracts


def run(*, source_inventory: Path, results_dir: Path, provider_path: Path, snapshot: Path,
        schema_dir: Path, ledger: PilotLedger, stage: str) -> dict[str, Any]:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError("openai SDK is required in the future qualified runtime") from exc
    if stage not in {"producer_conformity", "producer_remediation", "alternate_conformity"}:
        raise HarnessError("invalid producer conformance stage")
    preflight = load_json(PREFLIGHT_CONFIG_PATH)
    inventory = load_json(source_inventory)
    examples, contracts = _conformance_inputs(inventory)
    owners = sorted(row["source_agent"] for row in contracts)
    if owners != sorted(f"agent_{index}" for index in range(1, 9) for _ in range(2)):
        raise HarnessError("fixed contracts must assign exactly two insights to every agent")
    provider = provider_config(provider_path)
    count = offline_token_counter(snapshot, chat_template=False)
    prepared = []
    for index in range(1, 9):
        agent_id = f"agent_{index}"
        prompt = build_producer_prompt(agent_id=agent_id, local_examples=examples[agent_id], fixed_contracts=contracts)
        fixed = sorted((row for row in contracts if row["source_agent"] == agent_id), key=lambda row: row["insight_id"])
        input_tokens = count(prompt)
        margin = provider["expected_max_model_len"] - input_tokens - provider["max_tokens"]
        if margin < preflight["generation_budget"]["context_safety_margin_tokens"]:
            raise HarnessError(f"producer prompt does not fit the frozen context for {agent_id}")
        prepared.append((agent_id, prompt, fixed, input_tokens, margin))

    client = OpenAI(api_key=os.environ.get("STUDIO2_PRODUCER_API_KEY", "local-vllm"),
                    base_url=provider["base_url"], max_retries=0, timeout=600.0)
    stage_run = f"{stage}:{sha256_file(source_inventory)}:{provider['identity_sha256']}"
    records, library = [], []
    for agent_id, prompt, fixed, input_tokens, margin in prepared:
        logical_id, request_id = f"{stage}:{agent_id}", f"{stage_run}:{agent_id}"
        reservation = {"request_id": request_id, "logical_id": logical_id, "model": provider["model"],
                       "producer": provider["name"], "stage_run": stage_run}
        if stage == "producer_remediation":
            ledger.reserve_remediation_request(**reservation)
        else:
            ledger.reserve_request(stage=stage, **reservation)
        kwargs: dict[str, Any] = {
            "model": provider["model"], "messages": [{"role": "user", "content": prompt}],
            "max_tokens": provider["max_tokens"],
            "response_format": {"type": "json_schema", "json_schema": {
                "name": "study2_insight_pair", "strict": True, "schema": response_schema(fixed, preflight)}},
        }
        if provider["temperature"] is not None:
            kwargs["temperature"] = provider["temperature"]
        if provider["seed"] is not None:
            kwargs["seed"] = provider["seed"]
        if provider["thinking_token_budget"] is not None:
            kwargs["extra_body"] = {"thinking_token_budget": provider["thinking_token_budget"]}
        begin = time.monotonic()
        try:
            response = client.chat.completions.create(**kwargs)
        except Exception as exc:
            ledger.complete_request(request_id, status="FAILED", latency_ms=(time.monotonic() - begin) * 1000,
                                    detail={"error_type": type(exc).__name__, "message": str(exc)})
            raise RuntimeError("producer transport failed and was recorded; retry requires independent zero-token proof") from exc
        latency = time.monotonic() - begin
        if len(response.choices) != 1:
            ledger.complete_request(request_id, status="FAILED", latency_ms=latency * 1000, detail={"error": "choice_count"})
            raise RuntimeError("provider must return exactly one choice")
        content = response.choices[0].message.content or ""
        validation_error, pair = None, []
        try:
            parsed = strict_json_loads(content)
            if not isinstance(parsed, dict) or set(parsed) != {"insights"}:
                raise HarnessError("producer response must contain only insights")
            pair = parsed["insights"]
            validate_produced_pair(pair, inventory=inventory, agent_id=agent_id, token_count=count, schema_dir=schema_dir)
        except Exception as exc:
            validation_error = str(exc)
        usage = response.usage
        prompt_tokens, completion_tokens = getattr(usage, "prompt_tokens", None), getattr(usage, "completion_tokens", None)
        total_tokens = getattr(usage, "total_tokens", None)
        ledger.complete_request(request_id, status="COMPLETED", prompt_tokens=prompt_tokens,
                                completion_tokens=completion_tokens, total_tokens=total_tokens,
                                latency_ms=latency * 1000,
                                detail={"response_id": response.id, "schema_valid_first_attempt": validation_error is None})
        if validation_error is None:
            library.extend(pair)
        records.append({
            "timestamp": datetime.now(timezone.utc).isoformat(), "producer": provider["name"], "agent_id": agent_id,
            "prompt_sha256": sha256_text(prompt), "input_tokens_offline": input_tokens, "context_margin_tokens": margin,
            "returned_model": response.model, "response_id": response.id,
            "system_fingerprint": getattr(response, "system_fingerprint", None),
            "finish_reason": response.choices[0].finish_reason, "latency_seconds": latency,
            "raw_output": content, "raw_output_sha256": sha256_text(content),
            "schema_valid_first_attempt": validation_error is None, "validation_error": validation_error,
            "retry_count": 0, "response_raw": response.model_dump(mode="json"),
        })
    output = results_dir / f"producer_conformance_{provider['name']}_{stage}.jsonl"
    write_atomic(output, "".join(canonical_json(item) + "\n" for item in records))
    passed = len(library) == 16 and all(item["schema_valid_first_attempt"] for item in records)
    summary = {"artifact_version": "2", "status": "PASS" if passed else "FAIL", "stage": stage,
               "producer_identity_sha256": provider["identity_sha256"], "provider_requests": len(records),
               "valid_first_attempts": sum(item["schema_valid_first_attempt"] for item in records),
               "records_path": str(output.resolve()), "records_sha256": sha256_file(output),
               "r4_target_commit": SCHEMA_TARGET_COMMIT, "r4_manifest_sha256": SCHEMA_MANIFEST_SHA256,
               "scope": "R4 producer conformance only; no diagnostic or accuracy claim"}
    summary_path = results_dir / f"producer_conformance_{provider['name']}_{stage}_summary.json"
    write_atomic(summary_path, json.dumps(summary, indent=2, ensure_ascii=False) + "\n")
    if stage in {"producer_conformity", "producer_remediation"}:
        ledger.record_stage_outcome(stage, outcome=summary["status"], artifact_sha256=sha256_file(summary_path))
    if passed:
        ordered = sorted(library, key=lambda row: row["insight_id"])
        handoff = {"schema_commit": SCHEMA_TARGET_COMMIT, "schema_manifest_sha256": SCHEMA_MANIFEST_SHA256,
                   "library": ordered, "library_sha256": sha256_text(canonical_json(ordered)), "validated": True}
        write_atomic(results_dir / f"validated_insight_library_{provider['name']}_{stage}.json",
                     json.dumps(handoff, indent=2, ensure_ascii=False) + "\n")
    return summary


def print_plan(preflight: dict[str, Any]) -> None:
    print(json.dumps({"status": "PLAN_ONLY_NO_PROVIDER_CALLS", "calls_per_producer": 8,
                      "insights_per_call": 2, "global_insights_checked": 16,
                      "contract": {"revision": 4, "target_commit": SCHEMA_TARGET_COMMIT,
                                   "manifest_sha256": SCHEMA_MANIFEST_SHA256},
                      "producer_inputs": "verified development examples plus fixed contracts; no insight library",
                      "resulting_library": "written only after 16/16 first-attempt R4 validation",
                      "provider_config": "required separately after D9; no canonical role is assumed",
                      "automatic_retries": 0, "persistent_ledger_required": True,
                      "fixed_fields": preflight["insight_contract"]["fixed_fields"],
                      "generated_field": preflight["insight_contract"]["producer_field"]},
                     indent=2, ensure_ascii=False))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-inventory", type=Path)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--provider-config", type=Path)
    parser.add_argument("--model-snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--schema-dir", type=Path, default=DEFAULT_SCHEMA_DIR)
    parser.add_argument("--stage", choices=("producer_conformity", "producer_remediation", "alternate_conformity"), default="producer_conformity")
    parser.add_argument("--ledger", type=Path)
    parser.add_argument("--pilot-id")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    args = parser.parse_args()
    preflight = load_json(PREFLIGHT_CONFIG_PATH)
    if not args.execute:
        print_plan(preflight)
        return 0
    if args.acknowledge != ACK:
        raise SystemExit(f"execution requires --acknowledge {ACK}")
    if any(value is None for value in (args.source_inventory, args.provider_config, args.ledger, args.pilot_id)):
        raise SystemExit("execution requires source inventory, provider config, absolute ledger and pilot id")
    ledger = PilotLedger(args.ledger, pilot_id=args.pilot_id)
    summary = run(source_inventory=args.source_inventory, results_dir=args.results_dir,
                  provider_path=args.provider_config, snapshot=args.model_snapshot, schema_dir=args.schema_dir,
                  ledger=ledger, stage=args.stage)
    print(canonical_json(summary))
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
