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


ACK = "EXECUTE_PHASE03_PRELIMINARY_PILOT"
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
        latency = time.monotonic() - begin
        raw = response.model_dump(mode="json")
        if len(response.choices) != 1:
            raise RuntimeError("provider must return exactly one choice")
        choice = response.choices[0]
        content = choice.message.content if isinstance(choice.message.content, str) else ""
        parse_error = None
        parsed = None
        try:
            parsed = parse_diagnostic_output(
                content,
                label_space=prompt["label_space"],
                allowed_insight_ids=prompt["available_insight_ids"],
            )
        except ContractError as exc:
            parse_error = str(exc)
        usage = response.usage
        return {
            "timestamp": started_at,
            "prompt_id": prompt["prompt_id"],
            "prompt_sha256": prompt["prompt_sha256"],
            "agent_id": prompt["agent_id"],
            "case_id": prompt["case_id"],
            "condition": prompt["condition"],
            "sample_role": prompt["sample_role"],
            "generation": generation,
            "returned_model": response.model,
            "response_id": response.id,
            "system_fingerprint": getattr(response, "system_fingerprint", None),
            "finish_reason": choice.finish_reason,
            "latency_seconds": latency,
            "prompt_tokens": getattr(usage, "prompt_tokens", None),
            "completion_tokens": getattr(usage, "completion_tokens", None),
            "total_tokens": getattr(usage, "total_tokens", None),
            "raw_output": content,
            "raw_output_sha256": sha256_text(content),
            "parsed_output": parsed,
            "parse_valid_first_attempt": parse_error is None,
            "parse_error": parse_error,
            "retry_count": 0,
            "response_raw": raw,
            "sdk_version": self.sdk_version,
        }


def load_prepared(prepared_dir: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    plan_path = prepared_dir / "pre_gate_plan.json"
    prompt_path = prepared_dir / "pilot_prompts.jsonl"
    hashes = load_json(prepared_dir / "pre_gate_hashes.json")["files"]
    for path in (plan_path, prompt_path, PREFLIGHT_CONFIG_PATH):
        key = str(path.relative_to(ROOT))
        if hashes.get(key) != sha256_file(path):
            raise RuntimeError(f"prepared hash mismatch: {key}")
    plan = load_json(plan_path)
    if plan["status"] != "READY_FOR_PRE_GATE_GENERATION_PROBE":
        raise RuntimeError("static context preparation did not pass")
    prompts = read_jsonl(prompt_path)
    if len(prompts) != 40:
        raise RuntimeError("prepared pilot must contain forty prompts")
    label_space = load_json(Path(plan["source_manifest"]))["label_space"]
    for prompt in prompts:
        prompt["label_space"] = label_space
    return plan, prompts


def run_budget_stage(prepared_dir: Path, results_dir: Path) -> dict[str, Any]:
    config = load_json(PREFLIGHT_CONFIG_PATH)
    plan, prompts = load_prepared(prepared_dir)
    server = server_contract(config)
    schema = load_json(DIAGNOSTIC_SCHEMA_PATH)
    provider = Provider(config)
    stress: dict[str, dict[str, Any]] = {}
    for condition in ("A", "B-LF", "E-LF"):
        candidates = [item for item in prompts if item["condition"] == condition]
        stress[condition] = max(candidates, key=lambda item: item["input_tokens"])
    records: list[dict[str, Any]] = []
    selected = None
    for candidate in plan["context_feasibility"]["feasible_candidates"]:
        generation = {
            "temperature": config["generation_budget"]["temperature"],
            "seed": config["generation_budget"]["seed"],
            "thinking_token_budget": candidate["thinking_token_budget"],
            "max_tokens": candidate["max_tokens"],
        }
        batch = [
            provider.call(prompt=stress[condition], schema=schema, generation=generation)
            for condition in ("A", "B-LF", "E-LF")
        ]
        records.extend(batch)
        if all(
            item["finish_reason"] == "stop" and item["parse_valid_first_attempt"]
            for item in batch
        ):
            selected = generation
            break
    write_atomic(
        results_dir / "budget_probe_records.jsonl",
        "".join(canonical_json(item) + "\n" for item in records),
    )
    frozen = {
        "artifact_version": "1",
        "status": "FROZEN_FOR_STABILITY_GATE" if selected else "NO_GO_GENERATION_BUDGET",
        "scope": "PRELIMINARY_QWEN27B_CONFIGURATION_ONLY",
        "frozen_at": utc_now(),
        "study_model_decision": "UNDECIDED",
        "candidate": config["candidate"],
        "server": server,
        "generation": selected,
        "determinism_policy": config["determinism_policy"],
        "prompt_file_sha256": sha256_file(prepared_dir / "pilot_prompts.jsonl"),
        "pre_gate_plan_sha256": sha256_file(prepared_dir / "pre_gate_plan.json"),
        "diagnostic_schema_sha256": sha256_file(DIAGNOSTIC_SCHEMA_PATH),
        "budget_probe_records_sha256": sha256_file(results_dir / "budget_probe_records.jsonl"),
        "budget_probe_provider_requests": provider.requests,
        "stability_gate_provider_requests": 120,
        "go_scope": (
            "Only this model root, model revision, server contract, prompt sample, "
            "schemas and generation configuration. No claim about a definitive Study 2 "
            "model, diagnostic performance, other endpoints, other budgets, the final "
            "catalog, OOD behavior, or an alternate producer."
        ),
    }
    write_atomic(
        results_dir / "frozen_gate_config.json",
        json.dumps(frozen, indent=2, ensure_ascii=False) + "\n",
    )
    return frozen


def divergence_signature(record: dict[str, Any]) -> str:
    fields = {
        "abstain": (record["parsed_output"] or {}).get("abstain"),
        "predicted_label": (record["parsed_output"] or {}).get("predicted_label"),
        "parsed_output": record["parsed_output"],
        "finish_reason": record["finish_reason"],
        "parse_valid_first_attempt": record["parse_valid_first_attempt"],
        "raw_output_sha256": record["raw_output_sha256"],
    }
    return sha256_text(canonical_json(fields))


def run_stability_stage(prepared_dir: Path, results_dir: Path) -> dict[str, Any]:
    config = load_json(PREFLIGHT_CONFIG_PATH)
    plan, prompts = load_prepared(prepared_dir)
    frozen_path = results_dir / "frozen_gate_config.json"
    frozen = load_json(frozen_path)
    if frozen["status"] != "FROZEN_FOR_STABILITY_GATE" or not frozen["generation"]:
        raise RuntimeError("generation configuration is not frozen for the stability gate")
    if frozen["prompt_file_sha256"] != sha256_file(prepared_dir / "pilot_prompts.jsonl"):
        raise RuntimeError("pilot prompts changed after generation-budget freeze")
    if frozen["candidate"] != config["candidate"]:
        raise RuntimeError("candidate configuration changed after freeze")
    server = server_contract(config)
    if server["process"]["fingerprint_sha256"] != frozen["server"]["process"]["fingerprint_sha256"]:
        raise RuntimeError("server process configuration changed after freeze")
    schema = load_json(DIAGNOSTIC_SCHEMA_PATH)
    provider = Provider(config)
    records: list[dict[str, Any]] = []
    for prompt in prompts:
        for repetition in range(1, 4):
            record = provider.call(
                prompt=prompt,
                schema=schema,
                generation=frozen["generation"],
            )
            record["repetition"] = repetition
            records.append(record)
    if provider.requests != 120:
        raise AssertionError(f"stability gate made {provider.requests} requests, expected 120")
    record_path = results_dir / "stability_records.jsonl"
    write_atomic(record_path, "".join(canonical_json(item) + "\n" for item in records))
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        grouped[record["prompt_id"]].append(record)
    divergent = sorted(
        prompt_id
        for prompt_id, group in grouped.items()
        if len({divergence_signature(item) for item in group}) != 1
    )
    invalid = sum(not item["parse_valid_first_attempt"] for item in records)
    truncated = sum(item["finish_reason"] == "length" for item in records)
    status = "PASS_R1_WITH_CONTINUOUS_AUDIT" if not divergent else "PASS_SWITCH_TO_R3"
    if invalid or truncated:
        status = "NO_GO_CONFIGURATION"
    summary = {
        "artifact_version": "1",
        "status": status,
        "scope": frozen["go_scope"],
        "completed_at": utc_now(),
        "unique_prompts": len(grouped),
        "provider_requests": provider.requests,
        "divergent_prompt_count": len(divergent),
        "divergent_prompt_ids": divergent,
        "invalid_first_attempts": invalid,
        "length_truncations": truncated,
        "stability_records_sha256": sha256_file(record_path),
        "frozen_gate_config_sha256": sha256_file(frozen_path),
        "rule_of_three_upper_bound_note": (
            "With zero divergent prompts, 3/40 is approximately 7.5%; this is a "
            "technical gate and does not demonstrate determinism or instability below 1%."
        ),
        "accuracy_calculated": False,
        "ground_truth_accessed": False,
        "final_test_accessed": False,
    }
    write_atomic(
        results_dir / "stability_summary.json",
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
    )
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
                "stability_gate_calls": calls["stability_gate"],
                "qwen_producer_conformance_calls": calls["qwen_producer_conformance"],
                "alternate_producer_calls_deferred": calls[
                    "alternate_producer_conformance_deferred"
                ],
                "planned_total_with_both_producers": calls[
                    "planned_total_with_both_producers"
                ],
                "planned_total_with_retry_reserve": (
                    calls["planned_total_with_both_producers"] + calls["retry_reserve"]
                ),
                "retry_reserve_authorized": calls["retry_reserve_authorized"],
                "hard_stop_provider_requests": calls["hard_stop_provider_requests"],
                "duration_estimate_basis": (
                    "Only sequential 8001@16384 is verified. Extrapolation from 49.4 s/call "
                    "at thinking=1024, scaled linearly by the selected thinking cap with a "
                    "25% planning allowance for prompts up to 9875 input tokens."
                ),
                "estimated_budget_probe_wall_time": "25-40 minutes for the nine-call maximum",
                "estimated_stability_gate_wall_time_by_budget": {
                    "2048": "4-5 hours",
                    "3072": "6-7.5 hours",
                    "4096": "8-10 hours",
                },
                "estimated_probe_plus_gate_wall_time": "approximately 4.5-10.7 hours sequential",
                "direct_local_api_cost": "EUR 0; electricity/opportunity cost not priced",
                "alternate_producer_cost": "unknown until provider, model and tariff are frozen",
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("budget", "stability"))
    parser.add_argument("--prepared-dir", type=Path, default=DEFAULT_PREPARED)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    args = parser.parse_args()
    config = load_json(PREFLIGHT_CONFIG_PATH)
    if not args.execute:
        print_plan(config)
        return 0
    if args.acknowledge != ACK:
        raise SystemExit(f"execution requires --acknowledge {ACK}")
    if args.stage is None:
        raise SystemExit("execution requires --stage budget or --stage stability")
    result = (
        run_budget_stage(args.prepared_dir, args.results_dir)
        if args.stage == "budget"
        else run_stability_stage(args.prepared_dir, args.results_dir)
    )
    print(canonical_json(result))
    return 0 if not result["status"].startswith("NO_GO") else 2


if __name__ == "__main__":
    raise SystemExit(main())
