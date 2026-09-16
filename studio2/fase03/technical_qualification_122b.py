#!/usr/bin/env python3
"""One-call fail-closed technical qualification for the 122B successor.

The stage is not T9 and its output is never a scientific insight.  This module
does not authorize itself: both direct and CLI execution require the ordinary
exact execution authorization before a ledger or client is constructed.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness.common import (HarnessError, canonical_json, load_json,
                                            sha256_file, sha256_text)
from studio2.fase03.harness.ledger import (PilotLedger, TECHNICAL_STAGE, digest,
                                            load_tokenizer_accounting_guard)
from studio2.fase03.harness.runtime import durable_write


ACK = "EXECUTE_PHASE03_122B_TECHNICAL_QUALIFICATION"
TECHNICAL_PROMPT = (
    'Return exactly the JSON object {"status":"NO_THINKING_OK"}. '
    "This is a non-scientific interface test; do not analyze data."
)
EXPECTED_CONTENT = {"status": "NO_THINKING_OK"}
TECHNICAL_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["status"],
    "properties": {"status": {"const": "NO_THINKING_OK"}},
}
NO_THINKING_EXTRA_BODY = {"chat_template_kwargs": {"enable_thinking": False}}
TECHNICAL_MAX_TOKENS = 32
CAP_JUSTIFICATION = {
    "snapshot": "Qwen/Qwen3.5-122B-A10B-FP8@a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9",
    "canonical_expected_content_tokens": 9,
    "fixed_syntax_whitespace_reserve_tokens": 23,
    "rule": "9 exact payload tokens + 23 fixed reserve = 32; no post-response adjustment",
}


def technical_contract() -> dict[str, Any]:
    return {
        "artifact_version": "122B_TECHNICAL_QUALIFICATION_1",
        "stage": TECHNICAL_STAGE,
        "scientific_use": "FORBIDDEN",
        "prompt": TECHNICAL_PROMPT,
        "prompt_sha256": sha256_text(TECHNICAL_PROMPT),
        "schema": deepcopy(TECHNICAL_SCHEMA),
        "schema_sha256": digest(TECHNICAL_SCHEMA),
        "expected_content": deepcopy(EXPECTED_CONTENT),
        "max_tokens": TECHNICAL_MAX_TOKENS,
        "cap_justification": deepcopy(CAP_JUSTIFICATION),
        "extra_body": deepcopy(NO_THINKING_EXTRA_BODY),
        "reasoning_rule": "both reasoning and reasoning_content must be absent, null or empty string",
        "finish_reason": "stop",
        "retries": 0,
    }


def evaluate_response(raw: dict[str, Any], expected_identity: dict[str, Any]) -> dict[str, Any]:
    from studio2.fase03.harness.guards import response_identity_valid
    choices = raw.get("choices") if isinstance(raw, dict) else None
    choice = choices[0] if isinstance(choices, list) and len(choices) == 1 and isinstance(choices[0], dict) else {}
    message = choice.get("message") if isinstance(choice.get("message"), dict) else {}
    content = message.get("content")
    parsed = None
    schema_valid = False
    if isinstance(content, str):
        try:
            parsed = json.loads(content)
        except (TypeError, ValueError):
            parsed = None
        schema_valid = parsed == EXPECTED_CONTENT and type(parsed) is dict
    reasoning_values = [message.get(key) for key in ("reasoning", "reasoning_content")
                        if key in message]
    reasoning_empty = all(value is None or value == "" for value in reasoning_values)
    usage = raw.get("usage") if isinstance(raw.get("usage"), dict) else {}
    record = {
        "returned_model": raw.get("model"),
        "system_fingerprint": raw.get("system_fingerprint"),
        "response_id": raw.get("id"),
        "raw_output": content,
        "schema_valid_first_attempt": schema_valid,
        "reasoning_empty": reasoning_empty,
        "rendering_control_accepted": reasoning_empty,
        "finish_reason": choice.get("finish_reason"),
        "prompt_tokens": usage.get("prompt_tokens"),
        "completion_tokens": usage.get("completion_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "scientific_use": "FORBIDDEN",
    }
    record["identity_valid"] = response_identity_valid(record, expected_identity)
    record["technical_pass"] = bool(
        record["identity_valid"] and reasoning_empty and schema_valid
        and record["finish_reason"] == "stop"
    )
    failures = []
    if not record["identity_valid"]:
        failures.append("identity")
    if not reasoning_empty:
        failures.append("reasoning")
    if not schema_valid:
        failures.append("schema")
    if record["finish_reason"] != "stop":
        failures.append("finish_reason")
    record["failure_reasons"] = failures
    return record


def _validate_contract(config: dict[str, Any]) -> dict[str, Any]:
    configured = config.get("d9", {}).get("technical_qualification_122b")
    expected = technical_contract()
    if not isinstance(configured, dict):
        raise HarnessError("technical qualification contract differs from the prespecified bytes")
    from studio2.fase03.harness.d9 import require_122b_no_thinking
    require_122b_no_thinking(
        configured.get("extra_body"), context="technical qualification contract")
    if configured != expected:
        raise HarnessError("technical qualification contract differs from the prespecified bytes")
    return expected


def _materialize_technical_pass(ledger: PilotLedger, results_dir: Path) -> dict[str, Any]:
    """Idempotently close derived PASS evidence from the complete technical record."""
    records = ledger.stage_records(TECHNICAL_STAGE)
    summary = {
        "artifact_version": "1",
        "status": "PASS",
        "stage": TECHNICAL_STAGE,
        "records_sha256": digest(records),
        "provider_requests": 1,
        "scientific_use": "FORBIDDEN",
    }
    ledger.record_stage_outcome(
        TECHNICAL_STAGE, outcome="PASS", artifact_sha256=digest(summary),
        artifact=summary)
    durable_write(Path(results_dir) / "technical_qualification_122b_summary.json",
                  json.dumps(summary, indent=2, sort_keys=True) + "\n")
    return summary


def run(*, config_path: Path, provider_path: Path, ledger_path: Path, pilot_id: str,
        snapshot: Path, results_dir: Path,
        transport: Callable[[dict[str, Any]], dict[str, Any]] | None = None,
        resume: bool = False) -> dict[str, Any]:
    """Execute at most one authorized technical call; injected transport is test-only."""
    config = load_json(Path(config_path))
    from studio2.fase03.harness.guards import (require_execution, require_pilot_ledger,
                                               verify_tokenizer)
    # These checks intentionally precede ledger construction, provider reads and client creation.
    require_execution(config)
    contract = _validate_contract(config)
    ledger = PilotLedger(Path(ledger_path), pilot_id=pilot_id)
    require_pilot_ledger(config, ledger)
    from studio2.fase03.producer_probe import provider_config
    provider = provider_config(Path(provider_path))
    from studio2.fase03.harness.d9 import require_122b_no_thinking
    require_122b_no_thinking(
        provider.get("extra_body"), context="technical qualification provider")
    if provider.get("max_tokens") != 2560:
        raise HarnessError("successor producer max_tokens must remain 2560")
    from studio2.fase03.harness.d9 import validate_provider
    role = validate_provider(config, provider, TECHNICAL_STAGE,
                             file_sha256=sha256_file(Path(provider_path)))
    if role != "122B":
        raise HarnessError("technical qualification requires the documented 122B role")
    verify_tokenizer(Path(snapshot), **provider["tokenizer"])
    messages = [{"role": "user", "content": TECHNICAL_PROMPT}]
    guard = load_tokenizer_accounting_guard(
        Path(snapshot), template_kwargs=NO_THINKING_EXTRA_BODY["chat_template_kwargs"])
    spec = {
        "logical_id": "technical_qualification_122b_once",
        "model": provider["model"],
        "producer": provider["name"],
        "prompt_sha256": sha256_text(TECHNICAL_PROMPT),
        "case_sha256": digest("NON_SCIENTIFIC_INTERFACE_TEST"),
        "contract_sha256": digest(contract),
        "condition": "technical",
        "group": "technical_qualification_122b",
        "repetition": 1,
    }
    binding = {
        "requests": [spec],
        "template_text": TECHNICAL_PROMPT,
        "inventory_sha256": digest("NO_SCIENTIFIC_INPUT"),
        "provider": provider,
        "tokenizer": provider["tokenizer"],
        "execution_config": config,
        "tokenizer_snapshot": str(Path(snapshot).resolve()),
        "provider_file_sha256": sha256_file(Path(provider_path)),
        "provider_reference": {"path": str(Path(provider_path).resolve()),
                               "sha256": sha256_file(Path(provider_path))},
        "technical_contract": contract,
        "chat_template_kwargs": deepcopy(NO_THINKING_EXTRA_BODY["chat_template_kwargs"]),
    }
    ledger.validate_tokenizer_accounting_evidence(
        guard, expected_messages={spec["logical_id"]: messages})
    ledger.bind_stage(TECHNICAL_STAGE, binding)
    leaf = ledger.leaf(TECHNICAL_STAGE, spec["logical_id"])
    if leaf and not resume:
        raise HarnessError("existing technical qualification requires explicit --resume; no resend")
    if leaf is None:
        request_id = digest([ledger.pilot_id, TECHNICAL_STAGE, spec["logical_id"]])
        ledger.reserve_technical_request(
            request_id=request_id, logical_id=spec["logical_id"], model=spec["model"],
            producer=spec["producer"], stage_run=digest(binding))
        leaf = ledger.request(request_id)
    request_id = leaf["request_id"]
    stored = ledger.response(request_id)
    if stored is not None and stored.get("record") is not None:
        ledger.validate_tokenizer_accounting_record(request_id, record=stored["record"])
        if stored["record"].get("technical_pass") is not True:
            raise HarnessError("successor remains suspended by persisted technical STOP")
        _materialize_technical_pass(ledger, Path(results_dir))
        ledger.verify_stage_success(TECHNICAL_STAGE)
        return stored["record"]
    if stored is None and leaf["status"] != "INTENT":
        raise HarnessError("technical qualification has inconsistent durable state")
    if stored is None and resume:
        raise HarnessError("uncertain technical request blocks resume; no retry is permitted")
    payload = {
        "model": provider["model"],
        "messages": messages,
        "max_tokens": TECHNICAL_MAX_TOKENS,
        "response_format": {"type": "json_schema", "json_schema": {
            "name": "technical_no_thinking_122b", "strict": True,
            "schema": deepcopy(TECHNICAL_SCHEMA)}},
        "extra_body": deepcopy(NO_THINKING_EXTRA_BODY),
    }
    if stored is None:
        if transport is None:
            from openai import OpenAI
            client = OpenAI(api_key=os.environ.get("STUDIO2_PRODUCER_API_KEY", "local-vllm"),
                            base_url=provider["base_url"], max_retries=0, timeout=600.0)
            transport = lambda value: client.chat.completions.create(**value).model_dump(mode="json")
        begin = time.monotonic()
        try:
            raw = transport(deepcopy(payload))
        except Exception as exc:
            ledger.complete_request(
                request_id, status="FAILED", latency_ms=(time.monotonic() - begin) * 1000,
                detail={"error_type": type(exc).__name__, "message": str(exc)},
                transport_failure=True)
            raise HarnessError("technical qualification transport failed; no retry is permitted") from exc
        ledger.save_raw(request_id, raw, latency_ms=(time.monotonic() - begin) * 1000)
    else:
        raw = stored["raw"]
    ledger.account_producer_response(request_id, messages=messages, guard=guard)
    record = evaluate_response(raw, provider["expected_response"])
    record.update(request_id=request_id, prompt_sha256=spec["prompt_sha256"])
    ledger.bind_tokenizer_accounting_record(request_id, record=record)
    ledger.complete_request(
        request_id, status="COMPLETED", record=record,
        prompt_tokens=record.get("prompt_tokens"),
        completion_tokens=record.get("completion_tokens"),
        total_tokens=record.get("total_tokens"))
    journal = {"stage": TECHNICAL_STAGE, "request_id": request_id,
               "record_sha256": digest(record), "scientific_use": "FORBIDDEN"}
    durable_write(Path(results_dir) / "technical_qualification_122b_journal.json",
                  json.dumps(journal, indent=2, sort_keys=True) + "\n")
    if record["technical_pass"] is not True:
        if record["identity_valid"] is True:
            ledger.suspend_technical(request_id, reason=";".join(record["failure_reasons"]))
        raise HarnessError("successor suspended by technical qualification STOP")
    _materialize_technical_pass(ledger, Path(results_dir))
    return record


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--provider-config", type=Path, required=True)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--pilot-id", required=True)
    parser.add_argument("--model-snapshot", type=Path, required=True)
    parser.add_argument("--results-dir", type=Path, required=True)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    args = parser.parse_args()
    if not args.execute or args.acknowledge != ACK:
        raise SystemExit(f"execution requires --execute --acknowledge {ACK}")
    record = run(config_path=args.config, provider_path=args.provider_config,
                 ledger_path=args.ledger, pilot_id=args.pilot_id,
                 snapshot=args.model_snapshot, results_dir=args.results_dir,
                 resume=args.resume)
    print(canonical_json(record))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
