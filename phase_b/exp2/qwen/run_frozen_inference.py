#!/usr/bin/env python3
"""Execute the 540-call EXP2 Qwen schedule only with an explicit acknowledgement."""

from __future__ import annotations

import argparse
from collections import Counter
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

from phase_b.conditions.parser import parse_diagnostic_output  # noqa: E402
from phase_b.evaluation.aggregation import aggregate_run_records  # noqa: E402
from phase_b.evaluation.records import RunRecord  # noqa: E402
from phase_b.exp2.qwen.adapter import QwenOpenAICompatibleAdapter  # noqa: E402
from phase_b.exp2.qwen.common import (  # noqa: E402
    CONFIG_PATH,
    LANE_DIR,
    SCHEMA_PATH,
    SCHEDULE_PATH,
    FrozenPromptInputs,
    canonical_json,
    discover_server,
    load_json,
    original_prompt_hashes,
    sha256_file,
    verify_frozen_hashes,
)


PROBE_PATH = LANE_DIR / "probe/capability_probe.json"
OUTPUT_DIR = LANE_DIR / "inference"
RECORDS_PATH = OUTPUT_DIR / "repetition_records.jsonl"
AGGREGATES_PATH = OUTPUT_DIR / "aggregate_records.jsonl"
METADATA_PATH = OUTPUT_DIR / "execution_metadata.json"
HASH_MANIFEST_PATH = OUTPUT_DIR / "inference_output_hash_manifest.json"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_bytes(value: Any) -> bytes:
    return (canonical_json(value) + "\n").encode("utf-8")


def append_jsonl(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as stream:
        stream.write(canonical_json(value) + "\n")
        stream.flush()
        os.fsync(stream.fileno())


def write_immutable(path: Path, content: bytes) -> None:
    if path.exists():
        if path.read_bytes() != content:
            raise RuntimeError(f"immutable output differs: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_bytes(content)
    os.replace(temporary, path)


def validate_schedule(schedule: list[dict[str, Any]], repetitions: int) -> None:
    if len(schedule) != 540:
        raise RuntimeError("schedule must contain exactly 540 entries")
    if [item["sequence_index"] for item in schedule] != list(range(540)):
        raise RuntimeError("schedule sequence indices must be 0..539")
    if Counter(item["condition"] for item in schedule) != Counter(
        {"A": 180, "B": 180, "E": 180}
    ):
        raise RuntimeError("schedule condition counts differ from A/B/E frozen design")
    groups = Counter(
        (item["physical_case_id"], item["agent_id"], item["condition"])
        for item in schedule
    )
    if len(groups) != 180 or set(groups.values()) != {repetitions}:
        raise RuntimeError("schedule does not contain R=3 for every aggregate")


def verify_ready(config: dict[str, Any]) -> dict[str, Any]:
    verify_frozen_hashes(config)
    if not PROBE_PATH.exists():
        raise RuntimeError("capability probe is missing")
    probe = load_json(PROBE_PATH)
    if probe.get("status") != "PASS" or not all(probe.get("checks", {}).values()):
        raise RuntimeError("capability probe did not pass every gate")
    server = discover_server(config)
    for key, expected in (
        ("vllm_version", config["expected_vllm_version"]),
        ("model_id", config["requested_model"]),
        ("model_root", config["expected_model_root"]),
    ):
        if server.get(key) != expected:
            raise RuntimeError(f"live server differs from probe/config: {key}")
    if server["max_model_len"] != probe["server"]["max_model_len"]:
        raise RuntimeError("live context length differs from capability probe")
    return probe


def record_to_run_record(record: dict[str, Any]) -> RunRecord:
    return RunRecord(
        agent_id=record["agent_id"],
        condition=record["condition"],
        repetition=record["repetition"],
        model=record["requested_model"],
        model_version=record["model_root"],
        prompt_hash=record["prompt_hash"],
        input_hash=record["input_hash"],
        raw_output=record["raw_output"],
        raw_attempts=tuple(record["raw_attempts"]),
        parsed_output=record["parsed_final_output"],
        physical_case_id=record["physical_case_id"],
        temperature=record["temperature"],
        seed=record["seed"],
        timestamp=record["timestamp"],
        prompt_tokens=record["prompt_tokens"],
        completion_tokens=record["completion_tokens"],
        token_count_method="chat_completion.usage",
    )


def validate_record(
    record: dict[str, Any],
    entry: dict[str, Any],
    rendered: Any,
    config: dict[str, Any],
) -> None:
    for field in (
        "sequence_index",
        "block_index",
        "position_in_block",
        "physical_case_id",
        "agent_id",
        "condition",
        "repetition",
    ):
        if record.get(field) != entry[field]:
            raise RuntimeError(f"record differs from schedule: {field}")
    expected = {
        "requested_model": config["requested_model"],
        "model_root": config["expected_model_root"],
        "temperature": config["temperature"],
        "seed": config["seed"],
        "max_tokens": config["max_tokens"],
        "thinking_token_budget": config["thinking_token_budget"],
        "prompt_hash": rendered.prompt_hash,
        "input_hash": rendered.input_hash,
    }
    for field, value in expected.items():
        if record.get(field) != value:
            raise RuntimeError(f"record contract mismatch: {field}")
    if record.get("returned_model") != config["requested_model"]:
        raise RuntimeError("provider returned unexpected model alias")
    if record.get("stateless") is not True or record.get("message_count") != 1:
        raise RuntimeError("record is not a stateless single-message request")
    attempts = record.get("provider_attempts")
    if not isinstance(attempts, list) or not attempts:
        raise RuntimeError("provider attempts are missing")
    if record["raw_attempts"] != [item["raw_output"] for item in attempts]:
        raise RuntimeError("raw attempts were not preserved exactly")
    if record["raw_output"] != record["raw_attempts"][-1]:
        raise RuntimeError("final raw output is inconsistent")
    for field in ("prompt_tokens", "completion_tokens", "total_tokens"):
        if type(record.get(field)) is not int or record[field] < 0:
            raise RuntimeError(f"token accounting missing: {field}")
    parse_diagnostic_output(
        canonical_json(record["parsed_final_output"]),
        label_space=load_json(ROOT / "phase_b/config/protocol_config.json")["label_space"],
        allowed_insight_ids=rendered.available_insight_ids,
    )
    record_to_run_record(record).validate()


def execute_one(
    *,
    entry: dict[str, Any],
    rendered: Any,
    frozen: FrozenPromptInputs,
    config: dict[str, Any],
    adapter: QwenOpenAICompatibleAdapter,
) -> dict[str, Any]:
    execution = adapter.execute_diagnostic(
        prompt=rendered.text,
        label_space=frozen.protocol["label_space"],
        allowed_insight_ids=rendered.available_insight_ids,
        schema=load_json(SCHEMA_PATH),
        temperature=config["temperature"],
        seed=config["seed"],
        max_tokens=config["max_tokens"],
        thinking_token_budget=config["thinking_token_budget"],
        max_structural_retries=config["max_structural_retries"],
    )
    attempts = [item.to_dict() for item in execution.provider_attempts]
    final = attempts[-1]
    record = {
        **entry,
        "requested_model": config["requested_model"],
        "returned_model": final["returned_model"],
        "model_root": config["expected_model_root"],
        "model_revision": config["expected_model_revision"],
        "api_family": config["api_family"],
        "endpoint": config["endpoint"],
        "reasoning_effort": config["reasoning_effort"],
        "reasoning_mode": config["reasoning_mode"],
        "temperature": config["temperature"],
        "seed": config["seed"],
        "max_tokens": config["max_tokens"],
        "thinking_token_budget": config["thinking_token_budget"],
        "structured_outputs_strict": True,
        "max_structural_retries": config["max_structural_retries"],
        "prompt_hash": rendered.prompt_hash,
        "input_hash": rendered.input_hash,
        "prompt_character_count": rendered.character_count,
        "available_insight_ids": list(rendered.available_insight_ids),
        "provider_attempts": attempts,
        "raw_attempts": list(execution.result.raw_attempts),
        "raw_output": execution.result.raw_output,
        "parsed_final_output": execution.result.parsed_output,
        "parse_failure": execution.result.parse_failure,
        "structural_validation_errors": list(execution.result.validation_errors),
        "prompt_tokens": final["prompt_tokens"],
        "completion_tokens": final["completion_tokens"],
        "total_tokens": final["total_tokens"],
        "retry_count": execution.result.attempts - 1,
        "timestamp": utc_now(),
        "stateless": True,
        "message_count": 1,
        "previous_response_id_used": False,
    }
    validate_record(record, entry, rendered, config)
    return record


def load_existing(
    schedule: list[dict[str, Any]],
    frozen: FrozenPromptInputs,
    config: dict[str, Any],
) -> dict[int, dict[str, Any]]:
    if not RECORDS_PATH.exists():
        return {}
    records: dict[int, dict[str, Any]] = {}
    for line_number, line in enumerate(RECORDS_PATH.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            raise RuntimeError(f"blank record line: {line_number}")
        record = json.loads(line)
        index = record.get("sequence_index")
        if type(index) is not int or not 0 <= index < 540 or index in records:
            raise RuntimeError(f"invalid or duplicate record index: {index}")
        rendered = frozen.render(schedule[index])
        validate_record(record, schedule[index], rendered, config)
        records[index] = record
    return records


def finalize(
    records: list[dict[str, Any]],
    config: dict[str, Any],
    probe: dict[str, Any],
) -> None:
    if len(records) != 540:
        raise RuntimeError("full inference requires exactly 540 records")
    aggregates = aggregate_run_records(
        [record_to_run_record(record) for record in records],
        label_space=load_json(ROOT / "phase_b/config/protocol_config.json")["label_space"],
    )
    if len(aggregates) != 180:
        raise RuntimeError("aggregation must produce 180 records")
    values = [
        {
            "physical_case_id": item.physical_case_id,
            "agent_id": item.agent_id,
            "condition": item.condition,
            "parsed_output": item.parsed_output,
            "repetition_outcomes": list(item.repetition_outcomes),
            "aggregation_rule": "frozen_valid_label_majority_2_of_3_else_abstain",
        }
        for item in aggregates
    ]
    write_immutable(AGGREGATES_PATH, b"".join(canonical_bytes(item) for item in values))
    metadata = {
        "status": "EXP2_QWEN_INFERENCE_COMPLETE_AWAITING_FREEZE",
        "repetition_records": 540,
        "aggregate_records": 180,
        "condition_counts": dict(Counter(item["condition"] for item in records)),
        "requested_model": config["requested_model"],
        "model_root": config["expected_model_root"],
        "model_revision": config["expected_model_revision"],
        "temperature": config["temperature"],
        "seed": config["seed"],
        "max_tokens": config["max_tokens"],
        "thinking_token_budget": config["thinking_token_budget"],
        "repetitions": config["repetitions"],
        "schedule_sha256": config["schedule_sha256"],
        "capability_probe_sha256": sha256_file(PROBE_PATH),
        "server_process_command_sha256": probe["server_process"]["command_sha256"],
        "ground_truth_joined": False,
        "metrics_calculated": False,
        "completed_at": utc_now(),
    }
    write_immutable(METADATA_PATH, canonical_bytes(metadata))
    manifest = {
        "artifact_version": "1",
        "status": "IMMUTABLE_BEFORE_OFFLINE_EVALUATION",
        "schedule_reference": {
            "path": str(SCHEDULE_PATH.relative_to(ROOT)),
            "sha256": config["schedule_sha256"],
        },
        "repetition_record_count": 540,
        "aggregate_record_count": 180,
        "artifacts": {
            str(RECORDS_PATH.relative_to(ROOT)): sha256_file(RECORDS_PATH),
            str(AGGREGATES_PATH.relative_to(ROOT)): sha256_file(AGGREGATES_PATH),
            str(METADATA_PATH.relative_to(ROOT)): sha256_file(METADATA_PATH),
        },
        "ground_truth_included": False,
    }
    write_immutable(HASH_MANIFEST_PATH, canonical_bytes(manifest))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--execute-full-run",
        action="store_true",
        help="Required acknowledgement for the 540-call experiment.",
    )
    args = parser.parse_args()
    if not args.execute_full_run:
        raise SystemExit(
            "Refusing to run: pass --execute-full-run only after the Qwen lane is frozen."
        )

    config = load_json(CONFIG_PATH)
    probe = verify_ready(config)
    schedule = load_json(SCHEDULE_PATH)
    validate_schedule(schedule, config["repetitions"])
    frozen = FrozenPromptInputs()
    original_hashes = original_prompt_hashes()
    existing = load_existing(schedule, frozen, config)
    adapter = QwenOpenAICompatibleAdapter(
        base_url=config["base_url"], requested_model=config["requested_model"]
    )
    for entry in schedule:
        index = entry["sequence_index"]
        if index in existing:
            continue
        rendered = frozen.render(entry)
        key = (entry["physical_case_id"], entry["agent_id"], entry["condition"])
        if rendered.prompt_hash != original_hashes[key]:
            raise RuntimeError(f"prompt hash differs before call: {key}")
        record = execute_one(
            entry=entry,
            rendered=rendered,
            frozen=frozen,
            config=config,
            adapter=adapter,
        )
        append_jsonl(RECORDS_PATH, record)
        existing[index] = record
        if len(existing) % 10 == 0:
            print(canonical_json({"completed": len(existing), "remaining": 540 - len(existing)}))
    records = [existing[index] for index in range(540)]
    finalize(records, config, probe)
    print(canonical_json({"status": "COMPLETE", "records": 540, "aggregates": 180}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
