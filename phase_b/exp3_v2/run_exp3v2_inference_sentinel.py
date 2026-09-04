#!/usr/bin/env python3
"""One-call synthetic live API sentinel for the frozen EXP3_V2 harness.

This program never reads verbalizations, schedules, insights, derangements,
workbooks, evaluator mappings, or scientific output roots. A durable intent
without a receipt is permanently ambiguous; every received response exhausts
this sentinel identity whether validation passes or fails.
"""

from __future__ import annotations

import argparse
import importlib
from pathlib import Path
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from phase_b.conditions.parser import parse_diagnostic_output  # noqa: E402
from phase_b.exp3_v2 import run_exp3v2_inference as runner  # noqa: E402


SENTINEL_ID = "EXP3V2-INFERENCE-SENTINEL-001"
SYNTHETIC_LABEL_SPACE = (
    "SYNTHETIC-ALPHA",
    "SYNTHETIC-BETA",
    "SYNTHETIC-GAMMA",
)
EXPECTED_LABEL = "SYNTHETIC-ALPHA"
SENTINEL_PROMPT = """You are validating a synthetic structured-output transport.
This is not an experiment case and contains no empirical observation.
Return one JSON diagnostic object that classifies the token ALPHA as
SYNTHETIC-ALPHA. Set abstain to false and provide a short synthetic
reasoning_summary. Use no other label and include no auxiliary identifiers."""
INTENT_NAME = "sentinel_intent.json"
RECEIPT_NAME = "sentinel_receipt.json"
EVIDENCE_NAME = "EXP3_V2_INFERENCE_SENTINEL_EVIDENCE_001.json"
SENTINEL_REQUEST_PARAMETERS = {
    **runner.REQUEST_PARAMETERS,
    "sdk_automatic_retries": 0,
}


class SentinelFailedError(RuntimeError):
    """The single permitted submission returned but did not validate."""


def sentinel_paths(root: Path) -> tuple[Path, Path, Path]:
    return root / INTENT_NAME, root / RECEIPT_NAME, root / EVIDENCE_NAME


def assert_prompt_is_synthetic() -> None:
    lowered = SENTINEL_PROMPT.lower()
    forbidden = (
        "exp3",
        "exp3v2",
        "case to diagnose",
        "insight",
        "derangement",
        "fault",
        "normal",
        "cls-",
        ".txt",
        ".xlsx",
        "/private/",
        "/users/",
    )
    found = [token for token in forbidden if token in lowered]
    if found:
        raise RuntimeError(f"sentinel prompt violates synthetic boundary: {found}")


def verify_frozen_harness(manifest: dict[str, Any], manifest_path: Path) -> Path:
    harness_root = Path(
        runner.git_output(manifest_path.parent, "rev-parse", "--show-toplevel")
    ).resolve()
    if manifest_path.resolve() != harness_root / manifest["manifest_path"]:
        raise RuntimeError("sentinel manifest path differs from harness contract")
    if manifest.get("status") != "HARNESS_FROZEN_FOR_INFERENCE":
        raise RuntimeError("sentinel requires the frozen inference harness")
    if manifest.get("tag_created") is not True:
        raise RuntimeError("sentinel requires the recorded harness tag")
    head = runner.git_output(harness_root, "rev-parse", "HEAD")
    runner.verify_annotated_tag(harness_root, manifest["prospective_tag"], None, head)
    runner.verify_detached_clean_checkout(harness_root, head)
    for artifact in manifest["harness_artifacts"]:
        path = harness_root / artifact["path"]
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(
                f"missing or symlinked harness artifact: {artifact['path']}"
            )
        if (
            path.stat().st_size != artifact["size_bytes"]
            or runner.sha256_file(path) != artifact["sha256"]
        ):
            raise RuntimeError(f"harness artifact mismatch: {artifact['path']}")
    return harness_root


def assert_unused_sentinel_root(root: Path) -> None:
    if not root.exists():
        return
    if not root.is_dir() or root.is_symlink():
        raise RuntimeError(
            "sentinel root already exists and is not a regular directory"
        )
    intent, receipt, evidence = sentinel_paths(root)
    if intent.exists() and not receipt.exists():
        raise RuntimeError(
            f"AMBIGUOUS sentinel intent without receipt; {SENTINEL_ID} is exhausted"
        )
    present = [path.name for path in (intent, receipt, evidence) if path.exists()]
    raise RuntimeError(
        f"sentinel root already exists; {SENTINEL_ID} may not be submitted again: {present}"
    )


def make_intent() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "record_type": "sentinel_request_intent",
        "sentinel_id": SENTINEL_ID,
        "timestamp": runner.utc_now(),
        "prompt_sha256": runner.sha256_bytes(SENTINEL_PROMPT.encode("utf-8")),
        "requested_model": runner.MODEL,
        "request_parameters": SENTINEL_REQUEST_PARAMETERS,
        "provider_submission_count": 1,
        "response": None,
    }


def make_receipt(intent: dict[str, Any], response: dict[str, Any]) -> dict[str, Any]:
    return {
        **{
            key: value
            for key, value in intent.items()
            if key not in {"record_type", "timestamp", "response"}
        },
        "record_type": "sentinel_provider_receipt",
        "timestamp": runner.utc_now(),
        "response": response,
    }


def evaluate_response(
    intent_path: Path,
    receipt_path: Path,
    receipt: dict[str, Any],
) -> dict[str, Any]:
    response = receipt["response"]
    returned_model = response["returned_model"]
    model_pass = returned_model == runner.MODEL
    parsed: dict[str, Any] | None = None
    parse_error: str | None = None
    try:
        parsed = parse_diagnostic_output(
            response["raw_output"],
            label_space=SYNTHETIC_LABEL_SPACE,
            allowed_insight_ids=(),
        )
    except Exception as exc:
        parse_error = f"strict schema or synthetic label validation failed: {exc}"
    strict_schema_pass = parsed is not None
    synthetic_label_pass = parsed == {
        "predicted_label": EXPECTED_LABEL,
        "abstain": False,
        "used_insight_ids": [],
        "reasoning_summary": parsed["reasoning_summary"] if parsed else "",
    }
    token_values = [
        response["input_tokens"],
        response["output_tokens"],
        response["total_tokens"],
    ]
    token_types_pass = all(type(value) is int and value >= 0 for value in token_values)
    token_accounting_pass = (
        token_types_pass and token_values[0] + token_values[1] == token_values[2]
    )
    failures = []
    if not model_pass:
        failures.append("returned model mismatch")
    if parse_error:
        failures.append(parse_error)
    elif not synthetic_label_pass:
        failures.append("synthetic label contract mismatch")
    if not token_accounting_pass:
        failures.append("token accounting mismatch")
    status = "PASS" if not failures else "FAIL"
    return {
        "schema_version": "1.0",
        "sentinel_id": SENTINEL_ID,
        "status": status,
        "completed_at": runner.utc_now(),
        "provider_submission_count": 1,
        "intent_sha256": runner.sha256_file(intent_path),
        "receipt_sha256": runner.sha256_file(receipt_path),
        "prompt_sha256": receipt["prompt_sha256"],
        "requested_model": runner.MODEL,
        "returned_model": returned_model,
        "request_parameters": SENTINEL_REQUEST_PARAMETERS,
        "http_success": True,
        "strict_schema_pass": strict_schema_pass,
        "synthetic_label_pass": synthetic_label_pass,
        "token_accounting_pass": token_accounting_pass,
        "input_tokens": response["input_tokens"],
        "output_tokens": response["output_tokens"],
        "total_tokens": response["total_tokens"],
        "parsed_output": parsed,
        "failure_reason": "; ".join(failures) if failures else None,
        "scientific_input_used": False,
        "scientific_output_created": False,
    }


def run_sentinel(root: Path, adapter: Any) -> dict[str, Any]:
    assert_prompt_is_synthetic()
    assert_unused_sentinel_root(root)
    root.mkdir(parents=True, exist_ok=False)
    runner.fsync_directory(root.parent)
    intent_path, receipt_path, evidence_path = sentinel_paths(root)
    intent = make_intent()
    runner.validate_json(intent, "exp3v2_inference_sentinel_journal.schema.json")
    runner.atomic_write_immutable(intent_path, runner.canonical_json_bytes(intent))

    # There is deliberately one call site and no loop, correction, retry, or resume.
    response = runner.normalize_provider_response(
        adapter.create_response(
            prompt=SENTINEL_PROMPT,
            reasoning_effort=runner.REASONING_EFFORT,
            schema=runner.load_json(
                HERE.parent / "conditions/diagnostic_output.openai.schema.json"
            ),
            max_output_tokens=runner.MAX_OUTPUT_TOKENS,
        )
    )
    receipt = make_receipt(intent, response)
    runner.validate_json(receipt, "exp3v2_inference_sentinel_journal.schema.json")
    runner.atomic_write_immutable(receipt_path, runner.canonical_json_bytes(receipt))

    evidence = evaluate_response(intent_path, receipt_path, receipt)
    runner.validate_json(evidence, "exp3v2_inference_sentinel_evidence.schema.json")
    runner.atomic_write_immutable(evidence_path, runner.canonical_json_bytes(evidence))
    if evidence["status"] != "PASS":
        raise SentinelFailedError(
            f"{SENTINEL_ID} failed and is exhausted: {evidence['failure_reason']}"
        )
    return evidence


def main(argv: list[str] | None = None, *, client: Any | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--sentinel-root", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = runner.load_json(args.manifest)
    expected = manifest["sentinel"]
    if args.manifest.resolve() != Path(expected["manifest_path"]):
        raise RuntimeError("manifest argument differs from frozen sentinel command")
    if args.sentinel_root.absolute() != Path(expected["output_root"]):
        raise RuntimeError("sentinel-root differs from frozen sentinel command")
    assert_unused_sentinel_root(args.sentinel_root)

    runtime_validator = importlib.import_module(
        "phase_b.exp3_v2.validate_exp3v2_inference_runtime"
    )
    runtime_validator.validate_runtime(Path(manifest["runtime"]["lock_path"]))
    verify_frozen_harness(manifest, args.manifest)
    if (
        runner.sha256_bytes(SENTINEL_PROMPT.encode("utf-8"))
        != expected["prompt_sha256"]
    ):
        raise RuntimeError("synthetic sentinel prompt hash mismatch")

    adapter_module = importlib.import_module("phase_b.execution.openai_adapter")
    adapter = adapter_module.OpenAIAdapter(
        requested_model=runner.MODEL,
        timeout_seconds=runner.TIMEOUT_SECONDS,
        **({} if client is None else {"client": client}),
    )
    evidence = run_sentinel(args.sentinel_root, adapter)
    print(
        runner.canonical_json(
            {
                "status": "PASS",
                "sentinel_id": SENTINEL_ID,
                "provider_submission_count": 1,
                "evidence_sha256": runner.sha256_bytes(
                    runner.canonical_json_bytes(evidence)
                ),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
