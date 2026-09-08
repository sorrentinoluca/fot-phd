#!/usr/bin/env python3
"""Run the EXP2 Qwen capability probe; never evaluate held-out correctness."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase_b.conditions.builders import render_diagnostic_prompt  # noqa: E402
from phase_b.exp2.qwen.adapter import QwenOpenAICompatibleAdapter  # noqa: E402
from phase_b.exp2.qwen.common import (  # noqa: E402
    CONFIG_PATH,
    LANE_DIR,
    SCHEMA_PATH,
    SCHEDULE_PATH,
    FrozenPromptInputs,
    canonical_json,
    discover_server,
    http_json,
    load_json,
    original_prompt_hashes,
    tokenize_prompt,
    verify_frozen_hashes,
)


DEFAULT_JSON = LANE_DIR / "probe/capability_probe.json"
DEFAULT_REPORT = LANE_DIR / "probe/CAPABILITY_PROBE.md"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def process_provenance(config: dict[str, Any]) -> dict[str, Any]:
    candidates: list[tuple[int, str]] = []
    proc = Path("/proc")
    if proc.exists():
        for entry in proc.iterdir():
            if not entry.name.isdigit():
                continue
            try:
                command = (entry / "cmdline").read_bytes().replace(b"\0", b" ").decode().strip()
            except (OSError, UnicodeDecodeError):
                continue
            if (
                "vllm" in command
                and "serve" in command
                and config["requested_model"] in command
                and config["expected_model_root"] in command
            ):
                candidates.append((int(entry.name), command))
    if len(candidates) != 1:
        raise RuntimeError(f"expected one matching vLLM server process, found {len(candidates)}")
    pid, command = candidates[0]
    revision_flag = f"--revision {config['expected_model_revision']}"
    if revision_flag not in command:
        raise RuntimeError("vLLM command does not contain the pinned model revision")
    return {
        "pid": pid,
        "command": command,
        "command_sha256": hashlib.sha256(command.encode()).hexdigest(),
        "expected_revision_present": True,
    }


def synthetic_case(target_characters: int) -> str:
    seed = (
        "Synthetic capability-only observation over eight five-hour windows. "
        "XMEAS-4 exceeds a generic threshold in three windows, with two early "
        "activations and none in the final two windows. No true class is assigned."
    )
    filler = (
        " XMEAS-17 remains within its reference range while XMEAS-22 shows one "
        "isolated transient that does not persist."
    )
    value = seed
    while len(value) < target_characters:
        value += filler
    return value[:target_characters]


def prompt_budget_audit(
    config: dict[str, Any], frozen: FrozenPromptInputs
) -> tuple[dict[str, Any], int]:
    schedule = load_json(SCHEDULE_PATH)
    originals = original_prompt_hashes()
    seen: set[tuple[str, str, str]] = set()
    rows: list[dict[str, Any]] = []
    for entry in schedule:
        key = (entry["physical_case_id"], entry["agent_id"], entry["condition"])
        if key in seen:
            continue
        seen.add(key)
        rendered = frozen.render(entry)
        if rendered.prompt_hash != originals[key]:
            raise RuntimeError(f"rendered prompt differs from original frozen prompt: {key}")
        rows.append(
            {
                "physical_case_id": key[0],
                "agent_id": key[1],
                "condition": key[2],
                "prompt_hash": rendered.prompt_hash,
                "characters": rendered.character_count,
                "raw_prompt_tokens": tokenize_prompt(config, rendered.text),
            }
        )
    if len(rows) != 180:
        raise RuntimeError("prompt budget audit must cover 180 unique prompts")
    maximum = max(item["raw_prompt_tokens"] for item in rows)
    return {
        "unique_prompts": len(rows),
        "all_prompt_hashes_match_original": True,
        "minimum_raw_prompt_tokens": min(item["raw_prompt_tokens"] for item in rows),
        "maximum_raw_prompt_tokens": maximum,
        "maximum_prompt_characters": max(item["characters"] for item in rows),
        "maximum_plus_output_budget": maximum + config["max_tokens"],
        "note": "Raw /tokenize count; live Chat Completions usage is recorded separately.",
    }, max(len(text) for text in frozen.case_text.values())


def execution_summary(execution: Any) -> dict[str, Any]:
    return {
        "schema_valid": not execution.result.parse_failure,
        "parse_failure": execution.result.parse_failure,
        "structural_attempts": execution.result.attempts,
        "validation_errors": list(execution.result.validation_errors),
        "parsed_output": execution.result.parsed_output,
        "raw_attempts": list(execution.result.raw_attempts),
        "provider_attempts": [item.to_dict() for item in execution.provider_attempts],
    }


def run_probe() -> dict[str, Any]:
    config = load_json(CONFIG_PATH)
    verify_frozen_hashes(config)
    server = discover_server(config)
    process = process_provenance(config)
    origin = config["base_url"].removesuffix("/v1")
    openapi = http_json(f"{origin}/openapi.json")
    paths = openapi.get("paths", {})
    advertised = {
        "chat_completions": "/v1/chat/completions" in paths,
        "responses": "/v1/responses" in paths,
        "tokenize": "/tokenize" in paths,
    }
    frozen = FrozenPromptInputs()
    budget, max_case_characters = prompt_budget_audit(config, frozen)
    case_text = synthetic_case(max_case_characters)

    fixture_agent = max(
        frozen.local_examples,
        key=lambda agent: len(canonical_json(frozen.local_examples[agent])),
    )
    fixture_prompts = {
        condition: render_diagnostic_prompt(
            agent_id=fixture_agent,
            condition=condition,
            case_text=case_text,
            local_examples=frozen.local_examples[fixture_agent],
            config=frozen.protocol,
            global_insights=None if condition == "A" else frozen.global_insights,
            derangements=frozen.derangements if condition == "E" else None,
        )
        for condition in ("A", "B", "E")
    }
    schema = load_json(SCHEMA_PATH)
    adapter = QwenOpenAICompatibleAdapter(
        base_url=config["base_url"],
        requested_model=config["requested_model"],
    )

    dry_run: dict[str, Any] = {}
    executions: dict[str, Any] = {}
    for condition in ("A", "B", "E"):
        rendered = fixture_prompts[condition]
        execution = adapter.execute_diagnostic(
            prompt=rendered.text,
            label_space=frozen.protocol["label_space"],
            allowed_insight_ids=rendered.available_insight_ids,
            schema=schema,
            temperature=config["temperature"],
            seed=config["seed"],
            max_tokens=config["max_tokens"],
            max_structural_retries=config["max_structural_retries"],
        )
        executions[condition] = execution
        dry_run[condition] = execution_summary(execution)

    replay = adapter.execute_diagnostic(
        prompt=fixture_prompts["B"].text,
        label_space=frozen.protocol["label_space"],
        allowed_insight_ids=fixture_prompts["B"].available_insight_ids,
        schema=schema,
        temperature=config["temperature"],
        seed=config["seed"],
        max_tokens=config["max_tokens"],
        max_structural_retries=config["max_structural_retries"],
    )
    replay_summary = execution_summary(replay)
    deterministic = (
        executions["B"].result.raw_output == replay.result.raw_output
        and executions["B"].result.parsed_output == replay.result.parsed_output
    )

    provider_responses = [
        response
        for execution in [*executions.values(), replay]
        for response in execution.provider_attempts
    ]
    live_max_input = max(
        response.prompt_tokens or 0 for response in provider_responses
    )
    max_model_len = server["max_model_len"]
    checks = {
        "vllm_version_matches": server["vllm_version"] == config["expected_vllm_version"],
        "model_alias_matches": server["model_id"] == config["requested_model"],
        "model_root_matches": server["model_root"] == config["expected_model_root"],
        "model_revision_matches_process": process["expected_revision_present"],
        "required_paths_advertised": all(advertised.values()),
        "frozen_prompt_hashes_match": budget["all_prompt_hashes_match_original"],
        "raw_prompt_budget_fits": budget["maximum_plus_output_budget"] <= max_model_len,
        "live_fixture_budget_fits": live_max_input + config["max_tokens"] <= max_model_len,
        "all_outputs_schema_valid": all(item["schema_valid"] for item in dry_run.values())
        and replay_summary["schema_valid"],
        "no_length_truncation": all(
            response.finish_reason != "length" for response in provider_responses
        ),
        "returned_model_matches": all(
            response.returned_model == config["requested_model"]
            for response in provider_responses
        ),
        "token_accounting_complete": all(
            type(response.prompt_tokens) is int
            and type(response.completion_tokens) is int
            and type(response.total_tokens) is int
            for response in provider_responses
        ),
        "deterministic_replay": deterministic,
    }
    status = "PASS" if all(checks.values()) else "FAIL"
    return {
        "artifact_version": "1",
        "status": status,
        "scope": "CAPABILITY_AND_PLUMBING_ONLY",
        "executed_at": utc_now(),
        "config": config,
        "server": server,
        "server_process": process,
        "advertised_paths": advertised,
        "prompt_budget": budget,
        "fixture": {
            "agent_id": fixture_agent,
            "synthetic_case_characters": len(case_text),
            "contains_heldout_case_text": False,
            "contains_ground_truth": False,
            "prompt_characters": {
                key: value.character_count for key, value in fixture_prompts.items()
            },
        },
        "dry_run": dry_run,
        "deterministic_replay": {
            "condition": "B",
            "identical_raw_output": deterministic,
            "replay": replay_summary,
        },
        "checks": checks,
        "heldout_predictions_generated": False,
        "ground_truth_accessed": False,
        "performance_metrics_calculated": False,
        "full_experiment_calls_made": 0,
    }


def render_report(result: dict[str, Any]) -> str:
    checks = "\n".join(
        f"- {name}: **{'PASS' if passed else 'FAIL'}**"
        for name, passed in result["checks"].items()
    )
    dry = result["dry_run"]
    return f"""# EXP2 Qwen capability probe

Status: **{result['status']}**

- Scope: capability and plumbing only
- Model alias: `{result['server']['model_id']}`
- Model root: `{result['server']['model_root']}`
- vLLM: `{result['server']['vllm_version']}`
- Context: `{result['server']['max_model_len']}` tokens
- Temperature / seed / max tokens: `0` / `20260829` / `512`
- Unique frozen prompt hashes checked: `{result['prompt_budget']['unique_prompts']}`
- Maximum raw prompt tokens: `{result['prompt_budget']['maximum_raw_prompt_tokens']}`
- Live fixture A/B/E attempts: `{dry['A']['structural_attempts']}` / `{dry['B']['structural_attempts']}` / `{dry['E']['structural_attempts']}`
- Deterministic B replay: `{result['deterministic_replay']['identical_raw_output']}`

## Gates

{checks}

No held-out prediction, ground-truth join, accuracy, condition ranking, or full
540-call experiment was performed.
"""


def write_output(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(content)
    os.replace(temporary, path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_JSON)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    args = parser.parse_args()
    result = run_probe()
    write_output(
        args.output.resolve(),
        (json.dumps(result, indent=2, ensure_ascii=False) + "\n").encode("utf-8"),
    )
    write_output(args.report.resolve(), render_report(result).encode("utf-8"))
    print(canonical_json({"status": result["status"], "output": str(args.output)}))
    return 0 if result["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
