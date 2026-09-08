#!/usr/bin/env python3
"""Bind Qwen aggregates to the unchanged Experiment 1 offline evaluator core."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import phase_b.final_evaluation.evaluate_frozen_predictions as frozen_evaluator  # noqa: E402
from phase_b.exp2.qwen.common import LANE_DIR, canonical_json, load_json, sha256_file  # noqa: E402


INFERENCE_DIR = LANE_DIR / "inference"
AGGREGATE_PATH = INFERENCE_DIR / "aggregate_records.jsonl"
INFERENCE_MANIFEST_PATH = INFERENCE_DIR / "inference_output_hash_manifest.json"
OUTPUT_DIR = LANE_DIR / "evaluation"


def canonical_bytes(value: Any) -> bytes:
    return (canonical_json(value) + "\n").encode("utf-8")


def verify_qwen_inference() -> dict[str, Any]:
    manifest = load_json(INFERENCE_MANIFEST_PATH)
    if manifest.get("status") != "IMMUTABLE_BEFORE_OFFLINE_EVALUATION":
        raise RuntimeError("Qwen inference outputs are not frozen for evaluation")
    for relative, expected in manifest["artifacts"].items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"Qwen inference artifact hash mismatch: {relative}")
    return {
        "qwen_inference_manifest_sha256": sha256_file(INFERENCE_MANIFEST_PATH),
        "aggregate_predictions_sha256": sha256_file(AGGREGATE_PATH),
        "schedule_sha256": manifest["schedule_reference"]["sha256"],
        "evaluator_binding": "unchanged_phase_b_final_evaluation_evaluator_core",
    }


def evaluate() -> dict[str, Any]:
    provenance = verify_qwen_inference()
    original_aggregate = frozen_evaluator.AGGREGATE_PATH
    original_verify = frozen_evaluator.verify_frozen_inputs
    try:
        frozen_evaluator.AGGREGATE_PATH = AGGREGATE_PATH
        frozen_evaluator.verify_frozen_inputs = lambda: provenance
        results, artifacts = frozen_evaluator.build_results()
    finally:
        frozen_evaluator.AGGREGATE_PATH = original_aggregate
        frozen_evaluator.verify_frozen_inputs = original_verify

    relative_source = str(AGGREGATE_PATH.relative_to(ROOT))
    results["evaluation_status"] = "EXP2_QWEN_OFFLINE_EVALUATION_OF_FROZEN_AGGREGATES"
    results["primary_prediction_source"] = relative_source
    results["reproducibility"]["evaluator_code_sha256"] = sha256_file(
        Path(frozen_evaluator.__file__)
    )
    artifacts["evaluation_results.json"] = canonical_bytes(results)
    artifacts["EVALUATION_REPORT.md"] = frozen_evaluator.render_report(results).encode("utf-8")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, content in artifacts.items():
        frozen_evaluator.write_if_identical_or_absent(OUTPUT_DIR / name, content)
    output_hashes = {
        str((OUTPUT_DIR / name).relative_to(ROOT)): sha256_file(OUTPUT_DIR / name)
        for name in sorted(artifacts)
    }
    manifest = {
        "artifact_version": "1",
        "status": "EXP2_QWEN_OFFLINE_EVALUATION_COMPLETE",
        "input_aggregate_predictions_sha256": sha256_file(AGGREGATE_PATH),
        "frozen_evaluator_code_sha256": sha256_file(Path(frozen_evaluator.__file__)),
        "evaluation_artifacts": output_hashes,
    }
    frozen_evaluator.write_if_identical_or_absent(
        OUTPUT_DIR / "evaluation_hash_manifest.json", canonical_bytes(manifest)
    )
    return results


def main() -> int:
    results = evaluate()
    print(
        json.dumps(
            {
                "status": "COMPLETE",
                "primary_n_per_condition": results["primary"]["n_per_condition"],
                "physical_clusters": results["primary"]["physical_clusters"],
                "integrity": results["integrity_checks"]["status"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
