#!/usr/bin/env python3
"""Run the isolated post-hoc EXP2 Qwen 4096-token capped-case follow-up."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import time
from typing import Any, Iterable
from urllib.parse import urlparse
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[5]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase_b.conditions.parser import OutputValidationError, parse_diagnostic_output  # noqa: E402
from phase_b.conditions.retry import PARSE_FAILURE_OUTPUT  # noqa: E402
from phase_b.exp2.qwen.adapter import QwenOpenAICompatibleAdapter  # noqa: E402
from phase_b.exp2.qwen.common import (  # noqa: E402
    FrozenPromptInputs,
    SCHEMA_PATH,
    SCHEDULE_PATH,
    canonical_json,
    load_json,
    original_prompt_hashes,
    sha256_file,
    tokenize_prompt,
)
from phase_b.exp2.qwen.sensitivity.run import (  # noqa: E402
    cap_reached,
    extract_reasoning_tokens,
    frozen_qwen_prompt_hashes,
    select_condition_entries,
    verify_prompt_hash,
)

FOLLOWUP_DIR = Path(__file__).resolve().parent
CONFIG_PATH = FOLLOWUP_DIR / "config.json"
RECORDS_PATH = FOLLOWUP_DIR / "records.jsonl"
RESULTS_PATH = FOLLOWUP_DIR / "results.json"
SOURCE_DIR = FOLLOWUP_DIR.parent
SOURCE_CONFIG_PATH = SOURCE_DIR / "config.json"
SOURCE_RECORDS_PATH = SOURCE_DIR / "records.jsonl"
PREFLIGHT_HASHES_PATH = SOURCE_DIR / "preflight_frozen_hashes.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def assert_followup_output_path(path: Path) -> None:
    try:
        path.resolve().relative_to(FOLLOWUP_DIR.resolve())
    except ValueError as exc:
        raise RuntimeError(f"refusing to write outside capped follow-up: {path}") from exc


def atomic_write(path: Path, content: bytes) -> None:
    assert_followup_output_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(content)
    os.replace(temporary, path)


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    assert_followup_output_path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(canonical_json(value) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def _proc_cmdline(pid: str) -> list[str]:
    try:
        data = (Path("/proc") / pid / "cmdline").read_bytes()
    except (OSError, PermissionError):
        return []
    return [part.decode("utf-8", "replace") for part in data.split(b"\0") if part]


def _proc_environ(pid: str) -> dict[str, str]:
    try:
        data = (Path("/proc") / pid / "environ").read_bytes()
    except (OSError, PermissionError):
        return {}
    result: dict[str, str] = {}
    for part in data.split(b"\0"):
        if b"=" in part:
            key, value = part.split(b"=", 1)
            result[key.decode("utf-8", "replace")] = value.decode("utf-8", "replace")
    return result


def _arg_value(command: list[str], flag: str) -> str | None:
    try:
        return command[command.index(flag) + 1]
    except (ValueError, IndexError):
        return None


def find_server_process(config: dict[str, Any]) -> dict[str, Any]:
    matches: list[dict[str, Any]] = []
    for proc in Path("/proc").iterdir():
        if not proc.name.isdigit():
            continue
        command = _proc_cmdline(proc.name)
        if not command or "vllm" not in " ".join(command):
            continue
        if _arg_value(command, "--port") != str(config["expected_port"]):
            continue
        environment = _proc_environ(proc.name)
        matches.append(
            {
                "pid": int(proc.name),
                "command": command,
                "cuda_visible_devices": environment.get("CUDA_VISIBLE_DEVICES"),
                "hf_home": environment.get("HF_HOME"),
                "vllm_use_flashinfer_sampler": environment.get("VLLM_USE_FLASHINFER_SAMPLER"),
            }
        )
    if len(matches) != 1:
        raise RuntimeError("expected exactly one vLLM API process on sensitivity port 8001")
    process = matches[0]
    command = process["command"]
    expected_values = {
        "--revision": config["expected_model_revision"],
        "--served-model-name": config["requested_model"],
        "--host": "127.0.0.1",
        "--port": str(config["expected_port"]),
        "--tensor-parallel-size": "1",
        "--max-model-len": str(config["expected_max_model_len"]),
        "--max-num-seqs": "1",
        "--gpu-memory-utilization": "0.97",
        "--reasoning-parser": config["reasoning_parser"],
        "--seed": str(config["seed"]),
        "--generation-config": "vllm",
    }
    for flag, expected in expected_values.items():
        if _arg_value(command, flag) != expected:
            raise RuntimeError(f"live server process argument mismatch: {flag}")
    for required_flag in (
        "--language-model-only",
        "--enforce-eager",
        "--no-enable-prefix-caching",
    ):
        if required_flag not in command:
            raise RuntimeError(f"live server process lacks required flag: {required_flag}")
    if config["expected_model_root"] not in command:
        raise RuntimeError("live server process model root mismatch")
    if process["cuda_visible_devices"] != str(config["expected_gpu_physical_index"]):
        raise RuntimeError("live server is not isolated to physical GPU 0")
    if process["vllm_use_flashinfer_sampler"] != config["vllm_use_flashinfer_sampler"]:
        raise RuntimeError("live server sampler configuration differs from the source sensitivity server")
    process["command_sha256"] = hashlib.sha256(
        "\0".join(command).encode("utf-8")
    ).hexdigest()
    return process


def verify_server(base_url: str, config: dict[str, Any]) -> dict[str, Any]:
    parsed = urlparse(base_url)
    if (
        parsed.scheme != "http"
        or parsed.hostname != "127.0.0.1"
        or parsed.port != config["expected_port"]
        or parsed.path.rstrip("/") != "/v1"
    ):
        raise RuntimeError("base URL must be the prescribed localhost sensitivity endpoint")
    origin = base_url.rstrip("/").removesuffix("/v1")
    with urlopen(f"{origin}/health", timeout=5) as response:
        if response.status != 200:
            raise RuntimeError("vLLM health endpoint did not return HTTP 200")
    with urlopen(f"{origin}/version", timeout=5) as response:
        version = json.loads(response.read())
    with urlopen(f"{base_url.rstrip('/')}/models", timeout=5) as response:
        models = json.loads(response.read())
    if version.get("version") != config["expected_vllm_version"]:
        raise RuntimeError("vLLM version mismatch")
    data = models.get("data")
    if not isinstance(data, list) or len(data) != 1:
        raise RuntimeError("server must expose exactly one model")
    model = data[0]
    if model.get("id") != config["requested_model"]:
        raise RuntimeError("served model alias mismatch")
    if model.get("root") != config["expected_model_root"]:
        raise RuntimeError("served model root mismatch")
    if model.get("max_model_len") != config["expected_max_model_len"]:
        raise RuntimeError("live max_model_len differs from the follow-up contract")
    process = find_server_process(config)
    snapshot = (
        Path("/home/luca/fot-exp2/cache/huggingface/hub")
        / "models--Qwen--Qwen3.8-27B-FP8"
        / "snapshots"
        / config["expected_model_revision"]
        / "config.json"
    )
    if sha256_file(snapshot) != config["model_snapshot_config_sha256"]:
        raise RuntimeError("model snapshot config hash mismatch")
    server = {
        "health_http_status": 200,
        "vllm_version": version["version"],
        "model_id": model["id"],
        "model_root": model["root"],
        "model_revision": config["expected_model_revision"],
        "model_snapshot_config_sha256": sha256_file(snapshot),
        "max_model_len": model["max_model_len"],
        "api_pid": process["pid"],
        "cuda_visible_devices": process["cuda_visible_devices"],
        "hf_home": process["hf_home"],
        "vllm_use_flashinfer_sampler": process["vllm_use_flashinfer_sampler"],
        "server_process_command_sha256": process["command_sha256"],
    }
    server["fingerprint_sha256"] = hashlib.sha256(
        canonical_json(server).encode("utf-8")
    ).hexdigest()
    return server


def verify_frozen_integrity(config: dict[str, Any]) -> dict[str, str]:
    if sha256_file(SCHEDULE_PATH) != config["schedule_sha256"]:
        raise RuntimeError("frozen schedule hash mismatch")
    if sha256_file(SOURCE_CONFIG_PATH) != config["source_sensitivity_config_sha256"]:
        raise RuntimeError("source sensitivity config changed")
    if sha256_file(SOURCE_RECORDS_PATH) != config["source_sensitivity_records_sha256"]:
        raise RuntimeError("source sensitivity records changed")
    snapshot = load_json(PREFLIGHT_HASHES_PATH)["artifacts"]
    current = {relative: sha256_file(ROOT / relative) for relative in snapshot}
    differences = {
        relative: {"expected": snapshot[relative], "actual": current[relative]}
        for relative in snapshot
        if current[relative] != snapshot[relative]
    }
    if differences:
        raise RuntimeError(f"frozen artifact hash mismatch: {differences}")
    return current


def select_target_entries(
    schedule: list[dict[str, Any]], config: dict[str, Any]
) -> list[dict[str, Any]]:
    condition_b = select_condition_entries(schedule, "B", 1)
    target_order = [tuple(value) for value in config["target_pairs"]]
    if len(target_order) != 5 or len(set(target_order)) != 5:
        raise RuntimeError("follow-up target list must contain exactly five unique pairs")
    counts = Counter(
        (row["agent_id"], row["physical_case_id"])
        for row in schedule
        if row.get("condition") == "B" and row.get("repetition") == 1
    )
    if any(counts[key] != 1 for key in target_order):
        raise RuntimeError("each target must have exactly one condition-B repetition-1 observation")
    lookup = {(row["agent_id"], row["physical_case_id"]): row for row in condition_b}
    selected = [dict(lookup[key]) for key in target_order]
    for index, row in enumerate(selected):
        row["followup_sequence_index"] = index
    return selected


def verify_source_caps(config: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    rows = [
        json.loads(line)
        for line in SOURCE_RECORDS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    budget_rows = [
        row
        for row in rows
        if row.get("condition") == "B"
        and row.get("repetition") == 1
        and row.get("thinking_token_budget") == 3072
    ]
    if len(budget_rows) != 60:
        raise RuntimeError("source sensitivity must contain exactly 60 budget-3072 B/R=1 rows")
    keys = [(row["agent_id"], row["physical_case_id"]) for row in budget_rows]
    if len(set(keys)) != 60:
        raise RuntimeError("source budget-3072 rows contain duplicate agent-case pairs")
    capped = {
        (row["agent_id"], row["physical_case_id"]): row
        for row in budget_rows
        if row.get("cap_reached") is True
    }
    expected = {tuple(value) for value in config["target_pairs"]}
    if set(capped) != expected or len(capped) != 5:
        raise RuntimeError(f"budget-3072 capped set differs from declared targets: {sorted(capped)}")
    for key, row in capped.items():
        if row.get("reasoning_tokens") < 3071:
            raise RuntimeError(f"invalid source cap token count: {key}")
    return capped


def max_tokens(config: dict[str, Any]) -> int:
    expected = config["thinking_token_budget"] + config["final_output_allowance"]
    if config["max_tokens"] != expected or expected != 4608:
        raise RuntimeError("follow-up max_tokens contract mismatch")
    return expected


def validate_record_contract(
    record: dict[str, Any], config: dict[str, Any], expected: dict[str, Any] | None = None
) -> None:
    fixed = {
        "requested_model": config["requested_model"],
        "model_root": config["expected_model_root"],
        "model_revision": config["expected_model_revision"],
        "vllm_version": config["expected_vllm_version"],
        "max_model_len": config["expected_max_model_len"],
        "temperature": config["temperature"],
        "seed": config["seed"],
        "condition": "B",
        "repetition": 1,
        "thinking_token_budget": 4096,
        "max_tokens": 4608,
        "stateless": True,
        "message_count": 1,
        "structured_outputs_strict": True,
        "previous_response_id_used": False,
    }
    for field, value in fixed.items():
        if record.get(field) != value:
            raise RuntimeError(f"incompatible existing record field: {field}")
    if (record.get("agent_id"), record.get("physical_case_id")) not in {
        tuple(value) for value in config["target_pairs"]
    }:
        raise RuntimeError("existing record is outside the exact follow-up target set")
    for field in (
        "prompt_tokens",
        "completion_tokens",
        "reasoning_tokens",
        "final_non_reasoning_tokens",
        "total_tokens",
        "latency_monotonic_ns",
    ):
        if type(record.get(field)) is not int or record[field] < 0:
            raise RuntimeError(f"invalid token/latency field: {field}")
    if record["final_non_reasoning_tokens"] != record["completion_tokens"] - record["reasoning_tokens"]:
        raise RuntimeError("final non-reasoning token accounting mismatch")
    if record.get("cap_reached") is not cap_reached(record["reasoning_tokens"], 4096):
        raise RuntimeError("cap detection mismatch")
    if not isinstance(record.get("raw_output"), str):
        raise RuntimeError("raw output is missing")
    if record.get("reasoning_content") is not None and not isinstance(record["reasoning_content"], str):
        raise RuntimeError("reasoning content has invalid type")
    if not isinstance(record.get("server_fingerprint_sha256"), str):
        raise RuntimeError("server fingerprint is missing")
    if expected is not None:
        for field in (
            "agent_id",
            "physical_case_id",
            "condition",
            "repetition",
            "frozen_schedule_sequence_index",
            "sensitivity_sequence_index",
            "followup_sequence_index",
            "prompt_hash",
            "input_hash",
        ):
            if record.get(field) != expected.get(field):
                raise RuntimeError(f"existing record differs from expected input: {field}")


def record_key(record: dict[str, Any]) -> tuple[str, str, str, int, int]:
    return (
        record.get("agent_id"),
        record.get("physical_case_id"),
        record.get("condition"),
        record.get("thinking_token_budget"),
        record.get("repetition"),
    )


def load_existing_records(
    path: Path, config: dict[str, Any]
) -> dict[tuple[str, str, str, int, int], dict[str, Any]]:
    if not path.exists():
        return {}
    result: dict[tuple[str, str, str, int, int], dict[str, Any]] = {}
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise RuntimeError(f"blank record line: {line_number}")
        record = json.loads(line)
        validate_record_contract(record, config)
        key = record_key(record)
        if key in result:
            raise RuntimeError(f"duplicate follow-up record: {key}")
        result[key] = record
    return result


def verify_context_fit(
    entries: list[dict[str, Any]],
    frozen: FrozenPromptInputs,
    config: dict[str, Any],
    server: dict[str, Any],
    source_caps: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    per_case: list[dict[str, Any]] = []
    for entry in entries:
        prompt_tokens_live_raw = tokenize_prompt(config, frozen.render(entry).text)
        key = (entry["agent_id"], entry["physical_case_id"])
        prompt_tokens_request = source_caps[key].get("prompt_tokens")
        if type(prompt_tokens_request) is not int or prompt_tokens_request < prompt_tokens_live_raw:
            raise RuntimeError(f"invalid frozen provider prompt-token count for {key}")
        required = prompt_tokens_request + max_tokens(config)
        if required > server["max_model_len"]:
            raise RuntimeError(
                f"context does not fit without truncation for {entry['agent_id']}/{entry['physical_case_id']}: "
                f"{prompt_tokens_request} + {config['max_tokens']} > {server['max_model_len']}"
            )
        per_case.append(
            {
                "agent_id": entry["agent_id"],
                "physical_case_id": entry["physical_case_id"],
                "prompt_tokens_live_raw": prompt_tokens_live_raw,
                "prompt_tokens_request": prompt_tokens_request,
                "chat_framing_tokens": prompt_tokens_request - prompt_tokens_live_raw,
                "max_tokens": config["max_tokens"],
                "required_context": required,
                "server_max_model_len": server["max_model_len"],
            }
        )
    maximum = max(item["required_context"] for item in per_case)
    if maximum > config["minimum_required_max_model_len"]:
        raise RuntimeError("observed required context exceeds the declared 6997-token bound")
    return {
        "status": "PASS",
        "minimum_prompt_tokens_live_raw": min(item["prompt_tokens_live_raw"] for item in per_case),
        "maximum_prompt_tokens_live_raw": max(item["prompt_tokens_live_raw"] for item in per_case),
        "minimum_prompt_tokens_request": min(item["prompt_tokens_request"] for item in per_case),
        "maximum_prompt_tokens_request": max(item["prompt_tokens_request"] for item in per_case),
        "maximum_required_context": maximum,
        "per_case": per_case,
    }


def execute_one(
    *,
    entry: dict[str, Any],
    rendered: Any,
    config: dict[str, Any],
    server: dict[str, Any],
    adapter: QwenOpenAICompatibleAdapter,
    schema: dict[str, Any],
    label_space: Iterable[str],
    expected_prompt_tokens: int,
) -> dict[str, Any]:
    started = time.monotonic_ns()
    response = adapter.create_chat_completion(
        prompt=rendered.text,
        schema=schema,
        temperature=config["temperature"],
        seed=config["seed"],
        max_tokens=max_tokens(config),
        thinking_token_budget=config["thinking_token_budget"],
    )
    latency = time.monotonic_ns() - started
    attempt = response.to_dict()
    parsing_error: str | None = None
    try:
        parsed = parse_diagnostic_output(
            response.raw_output,
            label_space=label_space,
            allowed_insight_ids=rendered.available_insight_ids,
        )
        parse_failure = False
    except OutputValidationError as exc:
        parsing_error = str(exc)
        parsed = dict(PARSE_FAILURE_OUTPUT)
        parse_failure = True
    reasoning_tokens = extract_reasoning_tokens(attempt)
    for name, value in (
        ("prompt_tokens", response.prompt_tokens),
        ("completion_tokens", response.completion_tokens),
        ("total_tokens", response.total_tokens),
    ):
        if type(value) is not int or value < 0:
            raise RuntimeError(f"provider omitted {name}")
    if response.returned_model != config["requested_model"]:
        raise RuntimeError("provider returned unexpected model alias")
    if response.prompt_tokens != expected_prompt_tokens:
        raise RuntimeError("provider prompt-token count differs from the frozen identical request")
    if reasoning_tokens > response.completion_tokens:
        raise RuntimeError("reasoning tokens exceed completion tokens")
    record = {
        **entry,
        "requested_model": config["requested_model"],
        "returned_model": response.returned_model,
        "model_root": server["model_root"],
        "model_revision": server["model_revision"],
        "vllm_version": server["vllm_version"],
        "max_model_len": server["max_model_len"],
        "server_process_command_sha256": server["server_process_command_sha256"],
        "server_fingerprint_sha256": server["fingerprint_sha256"],
        "base_url": config["base_url"],
        "temperature": config["temperature"],
        "seed": config["seed"],
        "thinking_token_budget": config["thinking_token_budget"],
        "max_tokens": max_tokens(config),
        "prompt_hash": rendered.prompt_hash,
        "input_hash": rendered.input_hash,
        "prompt_character_count": rendered.character_count,
        "available_insight_ids": list(rendered.available_insight_ids),
        "prompt_tokens": response.prompt_tokens,
        "completion_tokens": response.completion_tokens,
        "reasoning_tokens": reasoning_tokens,
        "final_non_reasoning_tokens": response.completion_tokens - reasoning_tokens,
        "total_tokens": response.total_tokens,
        "finish_reason": response.finish_reason,
        "latency_monotonic_ns": latency,
        "latency_seconds": latency / 1_000_000_000,
        "raw_output": response.raw_output,
        "reasoning_content": response.reasoning_content,
        "parsed_final_output": parsed,
        "prediction": None if parsed.get("abstain") else parsed.get("predicted_label"),
        "parse_failure": parse_failure,
        "parsing_error": parsing_error,
        "retry_count": 0,
        "provider_attempts": [attempt],
        "raw_attempts": [response.raw_output],
        "response_raw": response.response_raw,
        "cap_reached": cap_reached(reasoning_tokens, config["thinking_token_budget"]),
        "structured_outputs_strict": True,
        "stateless": True,
        "message_count": 1,
        "previous_response_id_used": False,
        "timestamp": utc_now(),
    }
    expected = {**entry, "prompt_hash": rendered.prompt_hash, "input_hash": rendered.input_hash}
    validate_record_contract(record, config, expected)
    return record


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--condition", required=True, choices=["B"])
    parser.add_argument("--thinking-budget", required=True, type=int)
    parser.add_argument("--repetitions", required=True, type=int)
    parser.add_argument("--execute", action="store_true")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if not args.execute:
        raise SystemExit("Refusing inference without --execute")
    if args.condition != "B" or args.repetitions != 1 or args.thinking_budget != 4096:
        raise SystemExit("Follow-up is frozen at condition B, budget 4096, R=1")
    config = load_json(CONFIG_PATH)
    config["base_url"] = args.base_url.rstrip("/")
    if config.get("stateless") is not True or config.get("message_count") != 1:
        raise RuntimeError("follow-up must remain stateless with exactly one user message")
    verify_frozen_integrity(config)
    source_caps = verify_source_caps(config)
    schedule = load_json(SCHEDULE_PATH)
    entries = select_target_entries(schedule, config)
    if {(row["agent_id"], row["physical_case_id"]) for row in entries} != set(source_caps):
        raise RuntimeError("schedule selection and source capped set differ")

    frozen = FrozenPromptInputs()
    qwen_hashes = frozen_qwen_prompt_hashes()
    rendered_by_index: dict[int, Any] = {}
    for entry in entries:
        rendered = frozen.render(entry)
        verify_prompt_hash(entry, rendered, qwen_hashes)
        if rendered.prompt_hash != original_prompt_hashes().get(
            (entry["physical_case_id"], entry["agent_id"], "B")
        ):
            raise RuntimeError("rendered prompt differs from original frozen prompt")
        rendered_by_index[entry["followup_sequence_index"]] = rendered

    server = verify_server(config["base_url"], config)
    context_check = verify_context_fit(entries, frozen, config, server, source_caps)
    existing = load_existing_records(RECORDS_PATH, config)
    adapter = QwenOpenAICompatibleAdapter(
        base_url=config["base_url"],
        requested_model=config["requested_model"],
        timeout_seconds=420.0,
    )
    schema = load_json(SCHEMA_PATH)
    for entry in entries:
        rendered = rendered_by_index[entry["followup_sequence_index"]]
        expected = {**entry, "prompt_hash": rendered.prompt_hash, "input_hash": rendered.input_hash}
        key = (entry["agent_id"], entry["physical_case_id"], "B", 4096, 1)
        if key in existing:
            validate_record_contract(existing[key], config, expected)
            continue
        record = execute_one(
            entry=entry,
            rendered=rendered,
            config=config,
            server=server,
            adapter=adapter,
            schema=schema,
            label_space=frozen.protocol["label_space"],
            expected_prompt_tokens=source_caps[(entry["agent_id"], entry["physical_case_id"])]["prompt_tokens"],
        )
        append_jsonl(RECORDS_PATH, record)
        existing[key] = record
        print(
            canonical_json(
                {
                    "agent_id": entry["agent_id"],
                    "physical_case_id": entry["physical_case_id"],
                    "completed": len(existing),
                    "remaining": 5 - len(existing),
                }
            ),
            flush=True,
        )

    if len(existing) != 5:
        raise RuntimeError(f"follow-up is incomplete: {len(existing)}/5")
    from phase_b.exp2.qwen.sensitivity.capped_followup.evaluate import evaluate_and_write

    results = evaluate_and_write(server=server, context_check=context_check)
    print(canonical_json({"status": "COMPLETE", "records": len(existing), "budget": 4096}), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
