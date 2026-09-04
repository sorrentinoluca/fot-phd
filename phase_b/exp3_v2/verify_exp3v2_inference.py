#!/usr/bin/env python3
"""Portable mechanical verifier for completed EXP3_V2 inference outputs."""

from __future__ import annotations

from collections import Counter
import argparse
import importlib
import json
from pathlib import Path
import sys


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from phase_b.exp3_v2 import run_exp3v2_inference as runner  # noqa: E402


def expected_metadata(
    records: list[dict], schedule_sha256: str, failure_count: int
) -> dict:
    return {
        "status": "COMPLETE_PENDING_INFERENCE_DATA_FREEZE",
        "planned_repetition_records": 1080,
        "completed_repetition_records": 1080,
        "condition_counts": {"A": 360, "B": 360, "E": 360},
        "aggregate_records": 360,
        "schedule_sha256": schedule_sha256,
        "schedule_adherence": True,
        "stateless_calls": True,
        "single_process_sequential": True,
        "provider": "openai",
        "requested_model": runner.MODEL,
        "returned_models": [runner.MODEL],
        "reasoning_effort": runner.REASONING_EFFORT,
        "temperature": None,
        "seed": None,
        "max_output_tokens": runner.MAX_OUTPUT_TOKENS,
        "structured_outputs_strict": True,
        "max_structural_retries": runner.MAX_STRUCTURAL_RETRIES,
        "structural_retries_total": sum(item["retry_count"] for item in records),
        "provider_network_failures": failure_count,
        "ambiguous_request_states": 0,
        "final_parse_failures": sum(item["parse_failure"] for item in records),
        "provider_attempts": sum(len(item["provider_attempts"]) for item in records),
        "cumulative_input_tokens": sum(
            item["cumulative_input_tokens"] for item in records
        ),
        "cumulative_output_tokens": sum(
            item["cumulative_output_tokens"] for item in records
        ),
        "cumulative_total_tokens": sum(
            item["cumulative_total_tokens"] for item in records
        ),
        "token_accounting_complete": True,
        "ground_truth_joined": False,
        "metrics_calculated": False,
        "completed_at": max(item["timestamp"] for item in records),
    }


def verify(
    manifest_path: Path,
    authorization_manifest_path: Path,
    authorization_root: Path,
    source_root: Path,
    data_root: Path,
    verbalization_harness_root: Path,
    verbalizations_root: Path,
    output_root: Path,
) -> dict[str, object]:
    manifest = runner.load_json(manifest_path)
    runtime_validator = importlib.import_module(
        "phase_b.exp3_v2.validate_exp3v2_inference_runtime"
    )
    runtime_validator.validate_runtime(Path(manifest["runtime"]["lock_path"]))
    harness_root = runner.verify_boundaries(
        manifest,
        manifest_path,
        {
            "exp3-v2-heldout-frozen-002": source_root,
            "exp3-v2-heldout-data-frozen-001": data_root,
            "exp3-v2-verbalization-harness-frozen-001": verbalization_harness_root,
            "exp3-v2-verbalizations-frozen-001": verbalizations_root,
        },
    )
    runner.verify_execution_authorization(
        manifest,
        manifest_path,
        harness_root,
        authorization_manifest_path,
        authorization_root,
    )
    schedule_path = harness_root / manifest["schedule"]["path"]
    schedule = runner.load_json(schedule_path)
    schedule_sha256 = manifest["schedule"]["sha256"]
    runner.validate_schedule(schedule, schedule_sha256)
    case_texts = runner.load_case_texts(manifest, verbalizations_root)
    assets = runner.FrozenAssets(harness_root, case_texts)

    return verify_output_set(schedule, assets, output_root, schedule_sha256)


def verify_output_set(
    schedule: list[dict], assets: object, output_root: Path, schedule_sha256: str
) -> dict[str, object]:

    if not output_root.is_dir() or output_root.is_symlink():
        raise RuntimeError("completed output root is missing or symlinked")
    if (output_root / "execution.lock").exists():
        raise RuntimeError("execution lock exists; output is not quiescent")
    runner.scan_ambiguous_state(schedule, assets, output_root)
    records_by_index = runner.load_validated_records(schedule, assets, output_root)
    if set(records_by_index) != set(range(1080)):
        raise RuntimeError("validated repetition record set is incomplete")
    records = [records_by_index[index] for index in range(1080)]
    if Counter(item["condition"] for item in records) != Counter(
        {"A": 360, "B": 360, "E": 360}
    ):
        raise RuntimeError("validated repetition condition counts mismatch")

    repetition_path = output_root / "repetition_records.jsonl"
    expected_repetition_bytes = b"".join(
        runner.canonical_json_bytes(item) for item in records
    )
    if repetition_path.read_bytes() != expected_repetition_bytes:
        raise RuntimeError("deterministic repetition JSONL mismatch")

    aggregates = runner.aggregate_records(records, assets)
    aggregate_path = output_root / "aggregate_records.jsonl"
    expected_aggregate_bytes = b"".join(
        runner.canonical_json_bytes(item) for item in aggregates
    )
    if aggregate_path.read_bytes() != expected_aggregate_bytes:
        raise RuntimeError("deterministic aggregate JSONL mismatch")

    failure_paths = (
        sorted((output_root / "failures").glob("*.json"))
        if (output_root / "failures").exists()
        else []
    )
    for path in failure_paths:
        runner.validate_json(
            runner.load_json(path), "exp3v2_inference_failure.schema.json"
        )
    metadata_path = output_root / "execution_metadata.json"
    metadata = runner.load_json(metadata_path)
    runner.validate_json(metadata, "exp3v2_inference_execution_metadata.schema.json")
    if metadata != expected_metadata(records, schedule_sha256, len(failure_paths)):
        raise RuntimeError(
            "execution metadata differs from deterministic reconstruction"
        )

    final_paths = [repetition_path, aggregate_path, metadata_path]
    journal_paths = sorted((output_root / "request_journal").glob("*.json"))
    record_paths = sorted((output_root / "records").glob("*.json"))
    artifacts, inventory_sha = runner.output_inventory(
        output_root,
        journal_paths + record_paths + failure_paths + final_paths,
    )
    output_manifest_path = output_root / "inference_output_hash_manifest.json"
    output_manifest = runner.load_json(output_manifest_path)
    runner.validate_json(
        output_manifest, "exp3v2_inference_output_hash_manifest.schema.json"
    )
    if output_manifest["artifacts"] != artifacts:
        raise RuntimeError("output artifact inventory mismatch")
    if output_manifest["inventory_sha256"] != inventory_sha:
        raise RuntimeError("output inventory digest mismatch")
    if output_manifest["schedule_sha256"] != schedule_sha256:
        raise RuntimeError("output manifest schedule hash mismatch")

    expected_files = {item["path"] for item in artifacts} | {
        "inference_output_hash_manifest.json"
    }
    observed_files = {
        str(path.relative_to(output_root))
        for path in output_root.rglob("*")
        if path.is_file()
    }
    if observed_files != expected_files:
        raise RuntimeError("output root contains unmanifested or missing files")
    return {
        "status": "PASS",
        "repetition_records": 1080,
        "aggregate_records": 360,
        "condition_counts": {"A": 360, "B": 360, "E": 360},
        "schedule_sha256": schedule_sha256,
        "output_inventory_sha256": inventory_sha,
        "ground_truth_joined": False,
        "metrics_calculated": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--authorization-manifest", type=Path, required=True)
    parser.add_argument("--authorization-root", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--verbalization-harness-root", type=Path, required=True)
    parser.add_argument("--verbalizations-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args(argv)
    print(
        json.dumps(
            verify(
                args.manifest,
                args.authorization_manifest,
                args.authorization_root,
                args.source_root,
                args.data_root,
                args.verbalization_harness_root,
                args.verbalizations_root,
                args.output_root,
            ),
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
