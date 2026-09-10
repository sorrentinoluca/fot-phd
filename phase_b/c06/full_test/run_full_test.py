"""Fail-closed runner for the 360-call B_LOCAL_FIRST_V1 full test."""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import argparse
import json
import os
from pathlib import Path

from phase_b.conditions.parser import parse_diagnostic_output
from phase_b.c06.constants import (
    CORRECTION_SUFFIX,
    MAX_OUTPUT_TOKENS,
    MAX_STRUCTURAL_RETRIES,
    MODEL,
    REASONING_EFFORT,
    SDK_VERSION,
    VARIANT,
)
from phase_b.c06.prompt_variant import PromptAssets, canonical_json, sha256_bytes, sha256_file

from .constants import (
    FULL_TEST_ROOT,
    PLANNED_AGENT_CASES,
    PLANNED_CALLS,
    REPETITIONS,
    C06_ROOT,
    ROOT,
)


OUTPUT_ROOT = FULL_TEST_ROOT / "inference"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def atomic_write(path: Path, value: object) -> None:
    content = (canonical_json(value) + "\n").encode("utf-8")
    if path.exists():
        if path.read_bytes() != content:
            raise RuntimeError(f"immutable artifact differs: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("xb") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


def atomic_write_bytes(path: Path, content: bytes) -> None:
    if path.exists():
        if path.read_bytes() != content:
            raise RuntimeError(f"immutable artifact differs: {path}")
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    with temporary.open("xb") as stream:
        stream.write(content)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)


class ExclusiveLock:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.owned = False

    def __enter__(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        try:
            descriptor = os.open(
                self.path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600
            )
        except FileExistsError as exc:
            raise RuntimeError(
                f"exclusive execution lock exists; remove it only after human review: {self.path}"
            ) from exc
        with os.fdopen(descriptor, "w", encoding="utf-8") as stream:
            stream.write(canonical_json({"pid": os.getpid(), "created_at": utc_now()}) + "\n")
            stream.flush()
            os.fsync(stream.fileno())
        self.owned = True
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        del exc_type, exc, traceback
        if self.owned and self.path.exists():
            self.path.unlink()
            self.owned = False


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def verify_input_freeze() -> None:
    manifest = load_json(FULL_TEST_ROOT / "C06_FULL_TEST_FREEZE_MANIFEST.json")
    if manifest["status"] != "FROZEN_BEFORE_INFERENCE":
        raise RuntimeError("C06 full test manifest is not frozen")
    for item in manifest["experiment_artifacts"]:
        path = ROOT / item["path"]
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"frozen full-test artifact missing: {item['path']}")
        if sha256_file(path) != item["sha256"]:
            raise RuntimeError(f"frozen full-test artifact hash mismatch: {item['path']}")


def preflight() -> tuple[list[dict], PromptAssets]:
    verify_input_freeze()
    schedule = load_json(FULL_TEST_ROOT / "full_test_schedule.json")
    if len(schedule) != PLANNED_CALLS:
        raise RuntimeError(
            f"full test schedule must contain exactly {PLANNED_CALLS} entries"
        )
    if Counter(item["repetition"] for item in schedule) != Counter(
        {r: PLANNED_AGENT_CASES for r in range(1, REPETITIONS + 1)}
    ):
        raise RuntimeError("full test repetition counts mismatch")
    if any(item["condition"] != VARIANT for item in schedule):
        raise RuntimeError("unexpected condition in full test schedule")
    if [item["sequence_index"] for item in schedule] != list(range(PLANNED_CALLS)):
        raise RuntimeError(
            f"full test sequence indices must be exactly 0..{PLANNED_CALLS - 1}"
        )

    prompt_manifest = load_json(FULL_TEST_ROOT / "full_test_prompt_hash_manifest.json")
    expected = {
        (item["agent_id"], item["physical_case_id"]): item
        for item in prompt_manifest["prompts"]
    }
    if len(expected) != PLANNED_AGENT_CASES or prompt_manifest["prompt_count"] != PLANNED_AGENT_CASES:
        raise RuntimeError(
            f"prompt manifest must bind exactly {PLANNED_AGENT_CASES} unique prompts"
        )

    scheduled_keys = {
        (item["agent_id"], item["physical_case_id"]) for item in schedule
    }
    if scheduled_keys != set(expected):
        raise RuntimeError("schedule and prompt-manifest agent-case sets differ")

    assets = PromptAssets()
    for item in schedule:
        rendered = assets.render(item["agent_id"], item["physical_case_id"])
        frozen = expected[(item["agent_id"], item["physical_case_id"])]
        if rendered.prompt_hash != frozen["prompt_sha256"]:
            raise RuntimeError("rendered prompt differs from pre-inference prompt manifest")
        if rendered.input_hash != frozen["input_sha256"]:
            raise RuntimeError("rendered case differs from pre-inference prompt manifest")

    return schedule, assets


def validate_existing_record(
    record: dict, entry: dict, assets: PromptAssets
) -> None:
    rendered = assets.render(entry["agent_id"], entry["physical_case_id"])
    for key, value in entry.items():
        if record.get(key) != value:
            raise RuntimeError(f"existing record schedule mismatch: {key}")
    invariants = {
        "requested_model": MODEL,
        "returned_model": MODEL,
        "reasoning_effort": REASONING_EFFORT,
        "temperature": None,
        "seed": None,
        "store": False,
        "stateless": True,
        "previous_response_id_used": False,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "max_structural_retries": MAX_STRUCTURAL_RETRIES,
        "structured_outputs_strict": True,
        "prompt_hash": rendered.prompt_hash,
        "input_hash": rendered.input_hash,
    }
    for key, value in invariants.items():
        if record.get(key) != value:
            raise RuntimeError(f"existing record invariant mismatch: {key}")
    attempts = record.get("provider_attempts")
    if not isinstance(attempts, list) or not 1 <= len(attempts) <= 3:
        raise RuntimeError("existing record has invalid provider-attempt count")
    if record.get("retry_count") != len(attempts) - 1:
        raise RuntimeError("existing record retry count mismatch")
    for attempt in attempts:
        if attempt.get("returned_model") != MODEL:
            raise RuntimeError("existing record contains a different returned model")
        if attempt.get("sdk_version") != SDK_VERSION:
            raise RuntimeError("existing record contains a different SDK version")
        for name in ("input_tokens", "output_tokens", "total_tokens"):
            if type(attempt.get(name)) is not int or attempt[name] < 0:
                raise RuntimeError(f"existing record token accounting invalid: {name}")
            if attempt["total_tokens"] != attempt["input_tokens"] + attempt["output_tokens"]:
                raise RuntimeError("existing record token accounting mismatch")
    if not record.get("parse_failure"):
        parsed = parse_output(
            record["raw_attempts"][-1], assets, rendered.available_insight_ids
        )
        if parsed != record.get("parsed_final_output"):
            raise RuntimeError("existing record parsed output mismatch")


def parse_output(raw: str, assets: PromptAssets, allowed: tuple[str, ...]) -> dict:
    return parse_diagnostic_output(
        raw,
        label_space=assets.protocol["label_space"],
        allowed_insight_ids=allowed,
    )


def execute_record(entry: dict, assets: PromptAssets, adapter) -> dict:
    rendered = assets.render(entry["agent_id"], entry["physical_case_id"])
    raw_attempts = []
    provider_attempts = []
    validation_errors = []
    parsed = None
    for attempt in range(1, MAX_STRUCTURAL_RETRIES + 2):
        prompt = rendered.text if attempt == 1 else rendered.text + CORRECTION_SUFFIX
        intent_path = OUTPUT_ROOT / "request_journal" / f"{entry['sequence_index']:04d}.attempt-{attempt}.intent.json"
        response_path = OUTPUT_ROOT / "request_journal" / f"{entry['sequence_index']:04d}.attempt-{attempt}.response.json"
        intent = {
            "record_type": "request_intent",
            "timestamp": utc_now(),
            "sequence_index": entry["sequence_index"],
            "attempt": attempt,
            "prompt_sha256": sha256_bytes(prompt.encode("utf-8")),
            "base_prompt_sha256": rendered.prompt_hash,
            "input_sha256": rendered.input_hash,
            "requested_model": MODEL,
            "reasoning_effort": REASONING_EFFORT,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "store": False,
            "temperature_sent": False,
            "seed_sent": False,
        }
        if intent_path.exists() or response_path.exists():
            raise RuntimeError(
                f"pre-existing journal without an accepted record requires human review: {intent_path}"
            )
        atomic_write(intent_path, intent)
        response = adapter.create_response(
            prompt=prompt,
            reasoning_effort=REASONING_EFFORT,
            schema=assets.provider_schema,
            max_output_tokens=MAX_OUTPUT_TOKENS,
        )
        response_value = response.to_dict()
        atomic_write(
            response_path,
            {"record_type": "provider_response", "intent": intent, "response": response_value},
        )
        if response_value["returned_model"] != MODEL:
            raise RuntimeError("provider returned a model other than frozen gpt-5.6-terra")
        if response_value["sdk_version"] != SDK_VERSION:
            raise RuntimeError("provider SDK version differs from frozen 3.6.0")
        for name in ("input_tokens", "output_tokens", "total_tokens"):
            if type(response_value[name]) is not int or response_value[name] < 0:
                raise RuntimeError(f"provider token accounting unavailable: {name}")
        if response_value["total_tokens"] != (
            response_value["input_tokens"] + response_value["output_tokens"]
        ):
            raise RuntimeError("provider token accounting mismatch")
        raw_attempts.append(response_value["raw_output"])
        provider_attempts.append(response_value)
        try:
            parsed = parse_output(
                response_value["raw_output"], assets, rendered.available_insight_ids
            )
            break
        except Exception as exc:
            validation_errors.append(str(exc))

    parse_failure = parsed is None
    if parse_failure:
        parsed = {
            "predicted_label": None,
            "abstain": True,
            "used_insight_ids": [],
            "reasoning_summary": "parse_failure",
        }

    return {
        **entry,
        "requested_model": MODEL,
        "returned_model": provider_attempts[-1]["returned_model"],
        "reasoning_effort": REASONING_EFFORT,
        "temperature": None,
        "seed": None,
        "store": False,
        "stateless": True,
        "previous_response_id_used": False,
        "max_output_tokens": MAX_OUTPUT_TOKENS,
        "max_structural_retries": MAX_STRUCTURAL_RETRIES,
        "structured_outputs_strict": True,
        "prompt_hash": rendered.prompt_hash,
        "input_hash": rendered.input_hash,
        "prompt_character_count": rendered.character_count,
        "available_insight_ids": list(rendered.available_insight_ids),
        "provider_attempts": provider_attempts,
        "raw_attempts": raw_attempts,
        "parsed_final_output": parsed,
        "parse_failure": parse_failure,
        "structural_validation_errors": validation_errors,
        "retry_count": len(provider_attempts) - 1,
        "input_tokens": sum(item["input_tokens"] for item in provider_attempts),
        "output_tokens": sum(item["output_tokens"] for item in provider_attempts),
        "total_tokens": sum(item["total_tokens"] for item in provider_attempts),
        "timestamp": utc_now(),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="C06 B_LOCAL_FIRST_V1 full test runner")
    parser.add_argument("--preflight", action="store_true",
                        help="Validate all frozen inputs and prompt hashes, then exit")
    parser.add_argument("--execute", action="store_true",
                        help="Run inference on all 360 calls")
    args = parser.parse_args()

    if args.preflight == args.execute:
        parser.error("choose exactly one of --preflight or --execute")

    schedule, assets = preflight()
    if args.preflight:
        print(canonical_json({"status": "PASS", "scheduled_calls": len(schedule)}))
        return

    if not os.environ.get("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is required; no inference was started")

    import openai
    from phase_b.execution.openai_adapter import OpenAIAdapter

    if openai.__version__ != SDK_VERSION:
        raise RuntimeError(
            f"OpenAI SDK {SDK_VERSION} is required; found {openai.__version__}; "
            "no inference was started"
        )

    OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    lock = OUTPUT_ROOT / "execution.lock"
    with ExclusiveLock(lock):
        adapter = OpenAIAdapter(requested_model=MODEL)
        records = []
        completed = 0
        skipped = 0
        for entry in schedule:
            record_path = OUTPUT_ROOT / "records" / f"{entry['sequence_index']:04d}.json"
            if record_path.exists():
                record = load_json(record_path)
                validate_existing_record(record, entry, assets)
                skipped += 1
            else:
                record = execute_record(entry, assets, adapter)
                atomic_write(record_path, record)
                completed += 1
            records.append(record)
            total = len(records)
            label = record["parsed_final_output"]["predicted_label"] or "ABSTAIN"
            print(
                f"{total:03d}/{PLANNED_CALLS} "
                f"[{entry['stratum']:12s}] "
                f"{entry['agent_id']} {entry['physical_case_id']} "
                f"R{entry['repetition']} -> {label}"
                + (" (cached)" if record_path.exists() and skipped > 0 and completed == 0 or total <= skipped else "")
            )

        jsonl = "".join(canonical_json(item) + "\n" for item in records)
        atomic_write_bytes(
            OUTPUT_ROOT / "repetition_records.jsonl", jsonl.encode("utf-8")
        )

        metadata = {
            "variant": VARIANT,
            "scope": "full_test",
            "status": "FULL_TEST_INFERENCE_COMPLETE",
            "completed_at": utc_now(),
            "planned_repetition_records": PLANNED_CALLS,
            "completed_repetition_records": len(records),
            "new_calls": completed,
            "cached_calls": skipped,
            "provider_attempts": sum(len(item["provider_attempts"]) for item in records),
            "parse_failures": sum(item["parse_failure"] for item in records),
            "input_tokens": sum(item["input_tokens"] for item in records),
            "output_tokens": sum(item["output_tokens"] for item in records),
            "total_tokens": sum(item["total_tokens"] for item in records),
            "model": MODEL,
            "reasoning_effort": REASONING_EFFORT,
        }
        atomic_write(OUTPUT_ROOT / "execution_metadata.json", metadata)

    print(f"\nInference complete: {completed} new calls, {skipped} cached.")
    print(f"Total tokens: {metadata['total_tokens']:,}")


if __name__ == "__main__":
    main()
