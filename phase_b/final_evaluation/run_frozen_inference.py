#!/usr/bin/env python3
"""Run the frozen Phase B schedule without evaluator-side truth or metrics."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any


ROOT = Path("/Users/luker/fot-tep")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase_b.conditions.builders import (  # noqa: E402
    condition_peer_insights,
    render_diagnostic_prompt,
)
from phase_b.conditions.parser import parse_diagnostic_output  # noqa: E402
from phase_b.conditions.retry import execute_with_retry  # noqa: E402
from phase_b.config import load_protocol_config, validate_execution_ready  # noqa: E402
from phase_b.evaluation.aggregation import aggregate_run_records  # noqa: E402
from phase_b.evaluation.records import RunRecord  # noqa: E402
from phase_b.execution.openai_adapter import OpenAIAdapter  # noqa: E402
from phase_b.insights import Insight, validate_global_insights  # noqa: E402
from phase_b.prompts.leakage import scan_text  # noqa: E402


EXPECTED_HEAD = "eef0bc58e5ab14fb0cd2aece180fb5b1b5a7962b"
EXPECTED_SCHEDULE_SHA = "d30cdf6a6c622c1653176b393114073b447fdde69729086f6399291d776c0c9b"
SCHEDULE_PATH = ROOT / "phase_b/final_evaluation/inference_schedule.json"
VERBALIZATION_MANIFEST_PATH = (
    ROOT / "phase_b/final_evaluation/heldout_verbalizations_manifest.json"
)
PROTOCOL_HASH_MANIFEST_PATH = ROOT / "phase_b/PHASE_B_PROTOCOL_HASHES.json"
FINAL_INSIGHT_HASHES_PATH = ROOT / "phase_b/insights/final_insight_hashes.json"
GLOBAL_INSIGHTS_PATH = ROOT / "phase_b/insights/final_local_insights.json"
DERANGEMENT_PATH = (
    ROOT / "phase_b/config/evaluator_side/condition_e_derangements.json"
)
LOCAL_EXAMPLES_PATH = ROOT / "phase_b/local_knowledge/local_examples.json"
PROVIDER_SCHEMA_PATH = (
    ROOT / "phase_b/conditions/diagnostic_output.openai.schema.json"
)
EXECUTION_CONFIG_PATH = ROOT / "phase_b/config/execution_config.json"
OUTPUT_DIR = ROOT / "phase_b/final_evaluation/inference"
RECORDS_PATH = OUTPUT_DIR / "repetition_records.jsonl"
INFRA_FAILURES_PATH = OUTPUT_DIR / "infrastructure_failures.jsonl"
AGGREGATES_PATH = OUTPUT_DIR / "aggregate_records.jsonl"
METADATA_PATH = OUTPUT_DIR / "execution_metadata.json"
OUTPUT_HASH_MANIFEST_PATH = OUTPUT_DIR / "inference_output_hash_manifest.json"
AGENT_PACK = {
    "agent_1": "LKP-001",
    "agent_2": "LKP-002",
    "agent_3": "LKP-003",
    "agent_4": "LKP-004",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def canonical_json_bytes(value: Any) -> bytes:
    return (canonical_json(value) + "\n").encode("utf-8")


def append_jsonl(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = canonical_json(value) + "\n"
    with path.open("a", encoding="utf-8") as stream:
        stream.write(line)
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
    temporary.replace(path)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_value(*args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=True
    ).strip()


def verify_frozen_inputs(initial: bool) -> None:
    if git_value("rev-parse", "HEAD") != EXPECTED_HEAD:
        raise RuntimeError("HEAD differs from execution-schedule freeze")
    if git_value("rev-parse", "phase-b-execution-schedule-frozen^{}") != EXPECTED_HEAD:
        raise RuntimeError("execution-schedule tag target mismatch")
    if initial and git_value("status", "--porcelain=v1"):
        raise RuntimeError("initial inference requires a clean working tree")
    if sha256_file(SCHEDULE_PATH) != EXPECTED_SCHEDULE_SHA:
        raise RuntimeError("frozen schedule SHA-256 mismatch")

    protocol_manifest = load_json(PROTOCOL_HASH_MANIFEST_PATH)["artifacts"]
    for relative, expected in protocol_manifest.items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"frozen protocol hash mismatch: {relative}")

    insight_hashes = load_json(FINAL_INSIGHT_HASHES_PATH)["sha256"]
    if sha256_file(GLOBAL_INSIGHTS_PATH) != insight_hashes["final_local_insights"]:
        raise RuntimeError("final insight library hash mismatch")
    for name, expected in insight_hashes["peer_libraries"].items():
        path = ROOT / f"phase_b/insights/peer_libraries/{name}.json"
        if sha256_file(path) != expected:
            raise RuntimeError(f"peer library hash mismatch: {name}")

    verbalization_manifest = load_json(VERBALIZATION_MANIFEST_PATH)
    for item in verbalization_manifest["cases"]:
        if sha256_file(ROOT / item["neutral_text_path"]) != item["neutral_text_sha256"]:
            raise RuntimeError(
                f"neutral-text hash mismatch: {item['physical_case_id']}"
            )


def validate_schedule(schedule: list[dict[str, Any]]) -> None:
    if len(schedule) != 540:
        raise RuntimeError("schedule must contain exactly 540 entries")
    if [item["sequence_index"] for item in schedule] != list(range(540)):
        raise RuntimeError("schedule sequence_index must be 0..539")
    expected_keys = {
        "sequence_index",
        "block_index",
        "position_in_block",
        "physical_case_id",
        "agent_id",
        "repetition",
        "condition",
    }
    if any(set(item) != expected_keys for item in schedule):
        raise RuntimeError("schedule entry schema mismatch")
    keys = [
        (
            item["physical_case_id"],
            item["agent_id"],
            item["condition"],
            item["repetition"],
        )
        for item in schedule
    ]
    if len(set(keys)) != 540:
        raise RuntimeError("schedule contains duplicate experimental keys")
    if Counter(item["condition"] for item in schedule) != Counter(
        {"A": 180, "B": 180, "E": 180}
    ):
        raise RuntimeError("schedule condition counts mismatch")


class FrozenInputs:
    def __init__(self) -> None:
        self.protocol = load_protocol_config()
        validate_execution_ready(self.protocol)
        self.execution = load_json(EXECUTION_CONFIG_PATH)
        self.provider_schema = load_json(PROVIDER_SCHEMA_PATH)
        self.global_insights = validate_global_insights(
            load_json(GLOBAL_INSIGHTS_PATH), self.protocol
        )
        self.derangements = load_json(DERANGEMENT_PATH)["derangements"]
        artifact = load_json(LOCAL_EXAMPLES_PATH)
        self.local_examples = {
            agent_id: artifact["packs"][pack_id]
            for agent_id, pack_id in AGENT_PACK.items()
        }
        verbalization_manifest = load_json(VERBALIZATION_MANIFEST_PATH)
        self.case_text: dict[str, str] = {}
        for item in verbalization_manifest["cases"]:
            path = ROOT / item["neutral_text_path"]
            text = path.read_text(encoding="utf-8").strip()
            if not text:
                raise RuntimeError(
                    f"empty frozen neutral text: {item['physical_case_id']}"
                )
            self.case_text[item["physical_case_id"]] = text
        self.verify_peer_libraries()

    def verify_peer_libraries(self) -> None:
        for agent_id in AGENT_PACK:
            for condition in ("B", "E"):
                derived = condition_peer_insights(
                    agent_id=agent_id,
                    condition=condition,
                    config=self.protocol,
                    global_insights=self.global_insights,
                    derangements=self.derangements,
                )
                frozen = load_json(
                    ROOT
                    / f"phase_b/insights/peer_libraries/{agent_id}_{condition}.json"
                )
                if [item.to_dict() for item in derived] != frozen:
                    raise RuntimeError(
                        f"derived condition {condition} differs from frozen peer library"
                    )

    def render(self, entry: dict[str, Any]):
        condition = entry["condition"]
        rendered = render_diagnostic_prompt(
            agent_id=entry["agent_id"],
            condition=condition,
            case_text=self.case_text[entry["physical_case_id"]],
            local_examples=self.local_examples[entry["agent_id"]],
            config=self.protocol,
            global_insights=(None if condition == "A" else self.global_insights),
            derangements=(self.derangements if condition == "E" else None),
        )
        if scan_text(
            rendered.text,
            source=f"runtime:{entry['sequence_index']}",
        ):
            raise RuntimeError("runtime prompt leakage detected")
        lowered = rendered.text.lower()
        forbidden = ("mode1_", "class_offline", "fault_id", "pbh-")
        if any(token in lowered for token in forbidden):
            raise RuntimeError("runtime prompt contains forbidden metadata")
        return rendered


def parsed_output_is_valid(
    value: dict[str, Any], *, labels: list[str], allowed_ids: tuple[str, ...]
) -> None:
    parsed = parse_diagnostic_output(
        canonical_json(value),
        label_space=labels,
        allowed_insight_ids=allowed_ids,
    )
    if parsed != value:
        raise RuntimeError("parsed output normalization mismatch")


def record_to_frozen_run_record(record: dict[str, Any]) -> RunRecord:
    return RunRecord(
        agent_id=record["agent_id"],
        condition=record["condition"],
        repetition=record["repetition"],
        model=record["requested_model"],
        model_version=record["returned_model"],
        prompt_hash=record["prompt_hash"],
        input_hash=record["input_hash"],
        raw_output=record["raw_output"],
        raw_attempts=tuple(record["raw_attempts"]),
        parsed_output=record["parsed_final_output"],
        physical_case_id=record["physical_case_id"],
        temperature=record["temperature"],
        seed=record["seed"],
        timestamp=record["timestamp"],
        prompt_tokens=record["input_tokens"],
        completion_tokens=record["output_tokens"],
        token_count_method="response.usage",
    )


def validate_record(
    record: dict[str, Any], entry: dict[str, Any], rendered, frozen: FrozenInputs
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
            raise RuntimeError(f"run record schedule mismatch: {field}")
    if record.get("prompt_hash") != rendered.prompt_hash:
        raise RuntimeError("completed run prompt hash mismatch")
    if record.get("input_hash") != rendered.input_hash:
        raise RuntimeError("completed run input hash mismatch")
    if record.get("requested_model") != "gpt-5.6-terra":
        raise RuntimeError("completed run requested model mismatch")
    if record.get("returned_model") != "gpt-5.6-terra":
        raise RuntimeError("completed run returned model mismatch")
    if record.get("reasoning_effort") != "medium":
        raise RuntimeError("completed run reasoning effort mismatch")
    if record.get("temperature") is not None or record.get("seed") is not None:
        raise RuntimeError("completed run temperature/seed mismatch")
    if record.get("stateless") is not True:
        raise RuntimeError("completed run is not marked stateless")
    if record.get("previous_response_id_used") is not False:
        raise RuntimeError("completed run used response chaining")
    attempts = record.get("provider_attempts")
    raw_attempts = record.get("raw_attempts")
    if not isinstance(attempts, list) or not attempts:
        raise RuntimeError("provider attempts missing")
    if not isinstance(raw_attempts, list) or not raw_attempts:
        raise RuntimeError("raw attempts missing")
    if raw_attempts != [item["response"]["raw_output"] for item in attempts]:
        raise RuntimeError("raw-attempt preservation mismatch")
    if record.get("raw_output") != raw_attempts[-1]:
        raise RuntimeError("final raw output mismatch")
    if record.get("retry_count") != len(attempts) - 1:
        raise RuntimeError("structural retry accounting mismatch")
    for name in ("input_tokens", "output_tokens", "total_tokens"):
        value = record.get(name)
        if type(value) is not int or value < 0:
            raise RuntimeError(f"token accounting missing: {name}")
    if record["total_tokens"] != record["input_tokens"] + record["output_tokens"]:
        raise RuntimeError("final token total mismatch")
    parsed_output_is_valid(
        record["parsed_final_output"],
        labels=frozen.protocol["label_space"],
        allowed_ids=rendered.available_insight_ids,
    )
    if record["condition"] == "A" and record["parsed_final_output"]["used_insight_ids"]:
        raise RuntimeError("condition A used an insight ID")
    record_to_frozen_run_record(record).validate()


def load_existing_records(
    schedule: list[dict[str, Any]], frozen: FrozenInputs
) -> dict[int, dict[str, Any]]:
    if not RECORDS_PATH.exists():
        return {}
    records: dict[int, dict[str, Any]] = {}
    for line_number, line in enumerate(
        RECORDS_PATH.read_text(encoding="utf-8").splitlines(), start=1
    ):
        if not line.strip():
            raise RuntimeError(f"blank run-record line: {line_number}")
        value = json.loads(line)
        sequence_index = value.get("sequence_index")
        if type(sequence_index) is not int or not 0 <= sequence_index < 540:
            raise RuntimeError(f"invalid sequence_index at line {line_number}")
        if sequence_index in records:
            raise RuntimeError(f"duplicate completed sequence_index: {sequence_index}")
        rendered = frozen.render(schedule[sequence_index])
        validate_record(value, schedule[sequence_index], rendered, frozen)
        records[sequence_index] = value
    return records


def infrastructure_failures() -> list[dict[str, Any]]:
    if not INFRA_FAILURES_PATH.exists():
        return []
    return [
        json.loads(line)
        for line in INFRA_FAILURES_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def execute_one(
    *,
    entry: dict[str, Any],
    rendered,
    frozen: FrozenInputs,
    adapter: OpenAIAdapter,
) -> dict[str, Any]:
    provider_attempts: list[dict[str, Any]] = []

    def call(current_prompt: str, attempt: int) -> str:
        try:
            response = adapter.create_response(
                prompt=current_prompt,
                reasoning_effort="medium",
                schema=frozen.provider_schema,
                max_output_tokens=int(frozen.execution["dry_run_max_output_tokens"]),
            )
        except Exception as exc:
            append_jsonl(
                INFRA_FAILURES_PATH,
                {
                    "sequence_index": entry["sequence_index"],
                    "attempt": attempt,
                    "prompt_hash": rendered.prompt_hash,
                    "input_hash": rendered.input_hash,
                    "timestamp": utc_now(),
                    "error_type": type(exc).__name__,
                    "status_code": getattr(exc, "status_code", None),
                    "request_id": getattr(exc, "request_id", None),
                    "message": str(exc),
                    "prior_provider_attempts": provider_attempts,
                },
            )
            raise
        item = {
            "attempt": attempt,
            "received_at": utc_now(),
            "response": response.to_dict(),
        }
        provider_attempts.append(item)
        return response.raw_output

    retry_result = execute_with_retry(
        call=call,
        prompt=rendered.text,
        parse=lambda raw: parse_diagnostic_output(
            raw,
            label_space=frozen.protocol["label_space"],
            allowed_insight_ids=rendered.available_insight_ids,
        ),
        max_retries=2,
    )
    final = provider_attempts[-1]["response"]
    input_tokens = final["input_tokens"]
    output_tokens = final["output_tokens"]
    total_tokens = final["total_tokens"]
    if any(type(value) is not int for value in (input_tokens, output_tokens, total_tokens)):
        raise RuntimeError("provider token accounting is unavailable")
    if final["returned_model"] != "gpt-5.6-terra":
        raise RuntimeError("provider returned model differs from frozen identity")
    record = {
        **entry,
        "requested_model": final["requested_model"],
        "returned_model": final["returned_model"],
        "reasoning_effort": "medium",
        "temperature": None,
        "seed": None,
        "structured_outputs_strict": True,
        "max_structural_retries": 2,
        "prompt_hash": rendered.prompt_hash,
        "input_hash": rendered.input_hash,
        "prompt_character_count": rendered.character_count,
        "available_insight_ids": list(rendered.available_insight_ids),
        "response_id": final["response_id"],
        "request_id": final["request_id"],
        "provider_attempts": provider_attempts,
        "raw_attempts": list(retry_result.raw_attempts),
        "raw_output": retry_result.raw_output,
        "parsed_final_output": retry_result.parsed_output,
        "parse_failure": retry_result.parse_failure,
        "structural_validation_errors": list(retry_result.validation_errors),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "cumulative_input_tokens": sum(
            item["response"]["input_tokens"] for item in provider_attempts
        ),
        "cumulative_output_tokens": sum(
            item["response"]["output_tokens"] for item in provider_attempts
        ),
        "cumulative_total_tokens": sum(
            item["response"]["total_tokens"] for item in provider_attempts
        ),
        "retry_count": retry_result.attempts - 1,
        "timestamp": utc_now(),
        "stateless": True,
        "store": False,
        "previous_response_id_used": False,
    }
    validate_record(record, entry, rendered, frozen)
    return record


def validate_complete(
    records: list[dict[str, Any]], schedule: list[dict[str, Any]], frozen: FrozenInputs
) -> None:
    if len(records) != 540:
        raise RuntimeError("completed repetition record count is not 540")
    if Counter(item["condition"] for item in records) != Counter(
        {"A": 180, "B": 180, "E": 180}
    ):
        raise RuntimeError("completed condition counts mismatch")
    keys = [
        (
            item["physical_case_id"],
            item["agent_id"],
            item["condition"],
            item["repetition"],
        )
        for item in records
    ]
    if len(set(keys)) != 540:
        raise RuntimeError("completed records contain duplicate keys")
    combinations = Counter(
        (item["physical_case_id"], item["agent_id"], item["condition"])
        for item in records
    )
    if len(combinations) != 180 or set(combinations.values()) != {3}:
        raise RuntimeError("every case-agent-condition must contain three repetitions")
    for record, entry in zip(records, schedule):
        if record["sequence_index"] != entry["sequence_index"]:
            raise RuntimeError("records do not adhere to schedule order")
        validate_record(record, entry, frozen.render(entry), frozen)


def finalize(
    records: list[dict[str, Any]], schedule: list[dict[str, Any]], frozen: FrozenInputs
) -> dict[str, Any]:
    validate_complete(records, schedule, frozen)
    frozen_records = [record_to_frozen_run_record(item) for item in records]
    aggregates = aggregate_run_records(
        frozen_records,
        label_space=frozen.protocol["label_space"],
    )
    if len(aggregates) != 180:
        raise RuntimeError("aggregate record count is not 180")
    aggregate_values = [
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
    aggregate_bytes = b"".join(canonical_json_bytes(item) for item in aggregate_values)
    write_immutable(AGGREGATES_PATH, aggregate_bytes)

    failures = infrastructure_failures()
    retries_by_condition = Counter()
    for item in records:
        retries_by_condition[item["condition"]] += item["retry_count"]
    metadata = {
        "status": "FROZEN_HELDOUT_INFERENCE_COMPLETE",
        "planned_repetition_records": 540,
        "completed_repetition_records": 540,
        "condition_counts": dict(Counter(item["condition"] for item in records)),
        "aggregate_records": 180,
        "schedule_path": str(SCHEDULE_PATH.relative_to(ROOT)),
        "schedule_sha256": sha256_file(SCHEDULE_PATH),
        "schedule_adherence": True,
        "stateless_calls": True,
        "provider": "openai",
        "requested_model": "gpt-5.6-terra",
        "returned_models": sorted({item["returned_model"] for item in records}),
        "reasoning_effort": "medium",
        "temperature": None,
        "seed": None,
        "structured_outputs_strict": True,
        "max_structural_retries": 2,
        "structural_retries_total": sum(item["retry_count"] for item in records),
        "structural_retries_by_condition": {
            condition: retries_by_condition[condition] for condition in ("A", "B", "E")
        },
        "provider_network_failures": len(failures),
        "provider_network_resume_attempts": sum(
            failure["sequence_index"] in {item["sequence_index"] for item in records}
            for failure in failures
        ),
        "final_parse_failures": sum(item["parse_failure"] for item in records),
        "provider_attempts": sum(len(item["provider_attempts"]) for item in records),
        "cumulative_input_tokens": sum(item["cumulative_input_tokens"] for item in records),
        "cumulative_output_tokens": sum(item["cumulative_output_tokens"] for item in records),
        "cumulative_total_tokens": sum(item["cumulative_total_tokens"] for item in records),
        "token_accounting_complete": True,
        "provenance_complete": True,
        "ground_truth_joined": False,
        "metrics_calculated": False,
        "completed_at": utc_now(),
    }
    write_immutable(METADATA_PATH, canonical_json_bytes(metadata))

    artifacts = {
        str(RECORDS_PATH.relative_to(ROOT)): sha256_file(RECORDS_PATH),
        str(AGGREGATES_PATH.relative_to(ROOT)): sha256_file(AGGREGATES_PATH),
        str(METADATA_PATH.relative_to(ROOT)): sha256_file(METADATA_PATH),
    }
    if INFRA_FAILURES_PATH.exists():
        artifacts[str(INFRA_FAILURES_PATH.relative_to(ROOT))] = sha256_file(
            INFRA_FAILURES_PATH
        )
    output_manifest = {
        "artifact_version": "1",
        "status": "IMMUTABLE_BEFORE_OFFLINE_EVALUATION",
        "schedule_reference": {
            "path": str(SCHEDULE_PATH.relative_to(ROOT)),
            "sha256": EXPECTED_SCHEDULE_SHA,
        },
        "repetition_record_count": 540,
        "aggregate_record_count": 180,
        "execution_metadata_path": str(METADATA_PATH.relative_to(ROOT)),
        "artifacts": artifacts,
        "ground_truth_included": False,
    }
    write_immutable(
        OUTPUT_HASH_MANIFEST_PATH,
        canonical_json_bytes(output_manifest),
    )
    return metadata


def main() -> int:
    initial = not RECORDS_PATH.exists()
    verify_frozen_inputs(initial)
    schedule = load_json(SCHEDULE_PATH)
    validate_schedule(schedule)
    frozen = FrozenInputs()
    existing = load_existing_records(schedule, frozen)
    if not os.environ.get("OPENAI_API_KEY") and len(existing) < 540:
        raise RuntimeError("OPENAI_API_KEY is required in the environment")

    adapter = OpenAIAdapter(requested_model="gpt-5.6-terra") if len(existing) < 540 else None
    completed = len(existing)
    for entry in schedule:
        sequence_index = entry["sequence_index"]
        if sequence_index in existing:
            continue
        rendered = frozen.render(entry)
        if adapter is None:
            raise AssertionError("adapter missing for incomplete execution")
        record = execute_one(
            entry=entry,
            rendered=rendered,
            frozen=frozen,
            adapter=adapter,
        )
        append_jsonl(RECORDS_PATH, record)
        existing[sequence_index] = record
        completed += 1
        if completed % 10 == 0 or completed == 540:
            retries = sum(item["retry_count"] for item in existing.values())
            tokens = sum(item["cumulative_total_tokens"] for item in existing.values())
            print(
                canonical_json(
                    {
                        "completed": completed,
                        "remaining": 540 - completed,
                        "current_sequence_index": sequence_index,
                        "structural_retries": retries,
                        "cumulative_tokens": tokens,
                    }
                ),
                flush=True,
            )

    records = [existing[index] for index in range(540)]
    metadata = finalize(records, schedule, frozen)
    print(
        canonical_json(
            {
                "completed": 540,
                "aggregates": 180,
                "structural_retries": metadata["structural_retries_total"],
                "provider_network_failures": metadata["provider_network_failures"],
                "parse_failures": metadata["final_parse_failures"],
                "output_hash_manifest": "COMPLETE",
            }
        ),
        flush=True,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
