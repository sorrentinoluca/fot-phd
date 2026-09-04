#!/usr/bin/env python3
"""Portable mechanical verifier for the one-call EXP3_V2 API sentinel."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from phase_b.exp3_v2 import run_exp3v2_inference as runner  # noqa: E402
from phase_b.exp3_v2 import run_exp3v2_inference_sentinel as sentinel  # noqa: E402


def verify_sentinel(
    sentinel_root: Path,
    *,
    expected_prompt_sha256: str | None = None,
) -> dict[str, Any]:
    if not sentinel_root.is_dir() or sentinel_root.is_symlink():
        raise RuntimeError("sentinel evidence root is missing or symlinked")
    intent_path, receipt_path, evidence_path = sentinel.sentinel_paths(sentinel_root)
    expected_names = {path.name for path in (intent_path, receipt_path, evidence_path)}
    entries = list(sentinel_root.iterdir())
    observed_names = {path.name for path in entries}
    if observed_names != expected_names or any(
        path.is_symlink() or not path.is_file() for path in entries
    ):
        raise RuntimeError(
            "sentinel root contains missing, extra, or symlinked artifacts"
        )

    intent = runner.load_json(intent_path)
    receipt = runner.load_json(receipt_path)
    evidence = runner.load_json(evidence_path)
    runner.validate_json(intent, "exp3v2_inference_sentinel_journal.schema.json")
    runner.validate_json(receipt, "exp3v2_inference_sentinel_journal.schema.json")
    runner.validate_json(evidence, "exp3v2_inference_sentinel_evidence.schema.json")
    if (
        intent["record_type"] != "sentinel_request_intent"
        or receipt["record_type"] != "sentinel_provider_receipt"
    ):
        raise RuntimeError("sentinel journal record order is invalid")
    linked_fields = (
        "schema_version",
        "sentinel_id",
        "prompt_sha256",
        "requested_model",
        "request_parameters",
        "provider_submission_count",
    )
    for field in linked_fields:
        if receipt[field] != intent[field]:
            raise RuntimeError(f"sentinel receipt differs from intent: {field}")
    prompt_sha256 = runner.sha256_bytes(sentinel.SENTINEL_PROMPT.encode("utf-8"))
    if intent["prompt_sha256"] != prompt_sha256:
        raise RuntimeError("sentinel prompt hash differs from fixed synthetic prompt")
    if expected_prompt_sha256 is not None and prompt_sha256 != expected_prompt_sha256:
        raise RuntimeError("sentinel prompt hash differs from harness manifest")
    if evidence["intent_sha256"] != runner.sha256_file(intent_path):
        raise RuntimeError("sentinel evidence intent hash mismatch")
    if evidence["receipt_sha256"] != runner.sha256_file(receipt_path):
        raise RuntimeError("sentinel evidence receipt hash mismatch")

    response = receipt["response"]
    if response is None:
        raise RuntimeError("sentinel receipt has no provider response")
    parsed = sentinel.parse_diagnostic_output(
        response["raw_output"],
        label_space=sentinel.SYNTHETIC_LABEL_SPACE,
        allowed_insight_ids=(),
    )
    expected_parsed = {
        "predicted_label": sentinel.EXPECTED_LABEL,
        "abstain": False,
        "used_insight_ids": [],
        "reasoning_summary": parsed["reasoning_summary"],
    }
    if parsed != expected_parsed:
        raise RuntimeError("sentinel parsed output violates synthetic-label contract")
    tokens = (
        response["input_tokens"],
        response["output_tokens"],
        response["total_tokens"],
    )
    if not all(type(value) is int and value >= 0 for value in tokens):
        raise RuntimeError("sentinel tokens are not non-negative integers")
    if tokens[0] + tokens[1] != tokens[2]:
        raise RuntimeError("sentinel token accounting mismatch")

    expected_evidence_fields = {
        "sentinel_id": sentinel.SENTINEL_ID,
        "status": "PASS",
        "provider_submission_count": 1,
        "prompt_sha256": prompt_sha256,
        "requested_model": runner.MODEL,
        "returned_model": runner.MODEL,
        "request_parameters": sentinel.SENTINEL_REQUEST_PARAMETERS,
        "http_success": True,
        "strict_schema_pass": True,
        "synthetic_label_pass": True,
        "token_accounting_pass": True,
        "input_tokens": tokens[0],
        "output_tokens": tokens[1],
        "total_tokens": tokens[2],
        "parsed_output": parsed,
        "failure_reason": None,
        "scientific_input_used": False,
        "scientific_output_created": False,
    }
    for field, expected in expected_evidence_fields.items():
        if evidence[field] != expected:
            raise RuntimeError(f"sentinel evidence mismatch: {field}")
    if response["returned_model"] != runner.MODEL:
        raise RuntimeError("sentinel returned model mismatch")
    if response["requested_model"] != runner.MODEL:
        raise RuntimeError("sentinel requested model mismatch")
    if evidence["returned_model"] != response["returned_model"]:
        raise RuntimeError("sentinel evidence model differs from receipt")
    return {
        "status": "PASS",
        "sentinel_id": sentinel.SENTINEL_ID,
        "provider_submission_count": 1,
        "returned_model": runner.MODEL,
        "token_accounting": "PASS",
        "intent_sha256": runner.sha256_file(intent_path),
        "receipt_sha256": runner.sha256_file(receipt_path),
        "evidence_sha256": runner.sha256_file(evidence_path),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--sentinel-root", type=Path, required=True)
    args = parser.parse_args(argv)
    manifest = runner.load_json(args.manifest)
    expected = manifest["sentinel"]
    if args.manifest.resolve() != Path(expected["manifest_path"]):
        raise RuntimeError(
            "manifest argument differs from frozen sentinel verifier command"
        )
    if args.sentinel_root.absolute() != Path(expected["output_root"]):
        raise RuntimeError(
            "sentinel-root differs from frozen sentinel verifier command"
        )
    sentinel.verify_frozen_harness(manifest, args.manifest)
    result = verify_sentinel(
        args.sentinel_root,
        expected_prompt_sha256=expected["prompt_sha256"],
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
