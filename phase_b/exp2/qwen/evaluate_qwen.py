#!/usr/bin/env python3
"""Bind Qwen aggregates to the unchanged Experiment 1 offline evaluator core."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import phase_b.final_evaluation.evaluate_frozen_predictions as frozen_evaluator  # noqa: E402
from phase_b.exp2.qwen.common import LANE_DIR, canonical_json, load_json, sha256_file  # noqa: E402


INFERENCE_DIR = LANE_DIR / "inference"
AGGREGATE_PATH = INFERENCE_DIR / "aggregate_records.jsonl"
METADATA_PATH = INFERENCE_DIR / "execution_metadata.json"
INFERENCE_MANIFEST_PATH = INFERENCE_DIR / "inference_output_hash_manifest.json"
SCHEDULE_PATH = ROOT / "phase_b/final_evaluation/inference_schedule.json"
FROZEN_EVALUATOR_PATH = (
    ROOT / "phase_b/final_evaluation/evaluate_frozen_predictions.py"
)
OUTPUT_DIR = LANE_DIR / "evaluation"

QWEN_PREDICTIONS_FREEZE_TAG = "phase-b-exp2-qwen-predictions-frozen-001"
QWEN_PREDICTIONS_FREEZE_COMMIT = "a4f264c210873536c989ebd99aa2c6cf9857c85c"
INFERENCE_MANIFEST_STATUS = "IMMUTABLE_BEFORE_OFFLINE_EVALUATION"
METADATA_STATUS = "EXP2_QWEN_INFERENCE_COMPLETE_AWAITING_FREEZE"
SCHEDULE_RELATIVE_PATH = "phase_b/final_evaluation/inference_schedule.json"
SCHEDULE_SHA256 = "d30cdf6a6c622c1653176b393114073b447fdde69729086f6399291d776c0c9b"
INFERENCE_MANIFEST_SHA256 = (
    "da0eb0085ed42342b9d8fbabfbb9f50e3231e5311015fbbdfe6961c1aa4fd88b"
)
FROZEN_EVALUATOR_SHA256 = (
    "fbbc159a0e61e92723f46d4a97e59244a129741bffbf84acd433416bc74d567e"
)
CANONICAL_INFERENCE_ARTIFACTS = {
    "phase_b/exp2/qwen/inference/aggregate_records.jsonl": (
        "73ace46655ef1e3bce2b6491e489fd303780341eeadf7be2e972ce121c9f9e0a"
    ),
    "phase_b/exp2/qwen/inference/execution_metadata.json": (
        "7ec4719d6a7294440568273b6a2afd4abadf96f9283950857079db6fd082468e"
    ),
    "phase_b/exp2/qwen/inference/repetition_records.jsonl": (
        "20fdc8e3fac4ac37f2d993bdcacd526bd5927d5c599cb1fcbeef6a08e7372198"
    ),
}


def canonical_bytes(value: Any) -> bytes:
    return (canonical_json(value) + "\n").encode("utf-8")


def git_output(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        ).strip()
    except (OSError, subprocess.CalledProcessError) as exc:
        raise RuntimeError("Qwen predictions freeze tag is missing") from exc


def verify_qwen_inference() -> dict[str, Any]:
    tag_target = git_output(
        "rev-parse", "--verify", f"refs/tags/{QWEN_PREDICTIONS_FREEZE_TAG}^{{}}"
    )
    if tag_target != QWEN_PREDICTIONS_FREEZE_COMMIT:
        raise RuntimeError("Qwen predictions freeze tag target mismatch")
    if subprocess.run(
        [
            "git",
            "merge-base",
            "--is-ancestor",
            QWEN_PREDICTIONS_FREEZE_COMMIT,
            "HEAD",
        ],
        cwd=ROOT,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    ).returncode != 0:
        raise RuntimeError("current HEAD does not derive from Qwen predictions freeze")

    manifest = load_json(INFERENCE_MANIFEST_PATH)
    if sha256_file(INFERENCE_MANIFEST_PATH) != INFERENCE_MANIFEST_SHA256:
        raise RuntimeError("Qwen inference output manifest hash mismatch")
    if manifest.get("artifact_version") != "1":
        raise RuntimeError("Qwen inference output manifest version mismatch")
    if manifest.get("status") != INFERENCE_MANIFEST_STATUS:
        raise RuntimeError("Qwen inference output manifest status mismatch")
    if manifest.get("ground_truth_included") is not False:
        raise RuntimeError("Qwen inference manifest declares ground truth")
    if manifest.get("repetition_record_count") != 540:
        raise RuntimeError("Qwen repetition record count must be 540")
    if manifest.get("aggregate_record_count") != 180:
        raise RuntimeError("Qwen aggregate record count must be 180")
    if manifest.get("artifacts") != CANONICAL_INFERENCE_ARTIFACTS:
        raise RuntimeError("Qwen inference manifest artifact set or hash mismatch")
    for relative, expected in CANONICAL_INFERENCE_ARTIFACTS.items():
        if sha256_file(ROOT / relative) != expected:
            raise RuntimeError(f"Qwen inference artifact hash mismatch: {relative}")
    expected_schedule = {
        "path": SCHEDULE_RELATIVE_PATH,
        "sha256": SCHEDULE_SHA256,
    }
    if manifest.get("schedule_reference") != expected_schedule:
        raise RuntimeError("Qwen inference schedule reference mismatch")
    if sha256_file(SCHEDULE_PATH) != SCHEDULE_SHA256:
        raise RuntimeError("Qwen inference schedule hash mismatch")

    metadata = load_json(METADATA_PATH)
    if metadata.get("status") != METADATA_STATUS:
        raise RuntimeError("Qwen execution metadata status mismatch")
    if metadata.get("repetition_records") != 540:
        raise RuntimeError("Qwen metadata repetition count must be 540")
    if metadata.get("aggregate_records") != 180:
        raise RuntimeError("Qwen metadata aggregate count must be 180")
    if metadata.get("schedule_sha256") != SCHEDULE_SHA256:
        raise RuntimeError("Qwen metadata schedule hash mismatch")
    if metadata.get("ground_truth_joined") is not False:
        raise RuntimeError("Qwen metadata declares ground truth access")
    if metadata.get("metrics_calculated") is not False:
        raise RuntimeError("Qwen metadata declares metrics calculation")

    evaluator_path = Path(frozen_evaluator.__file__).resolve()
    if evaluator_path != FROZEN_EVALUATOR_PATH.resolve():
        raise RuntimeError("Qwen evaluator core path mismatch")
    if sha256_file(evaluator_path) != FROZEN_EVALUATOR_SHA256:
        raise RuntimeError("Qwen evaluator core hash mismatch")

    return {
        "qwen_predictions_freeze_tag": QWEN_PREDICTIONS_FREEZE_TAG,
        "qwen_predictions_freeze_commit": QWEN_PREDICTIONS_FREEZE_COMMIT,
        "qwen_inference_manifest_sha256": INFERENCE_MANIFEST_SHA256,
        "aggregate_predictions_sha256": sha256_file(AGGREGATE_PATH),
        "schedule_sha256": SCHEDULE_SHA256,
        "frozen_evaluator_code_path": str(FROZEN_EVALUATOR_PATH.relative_to(ROOT)),
        "frozen_evaluator_code_sha256": FROZEN_EVALUATOR_SHA256,
        "evaluator_binding": "phase_b.final_evaluation.evaluate_frozen_predictions",
    }


def render_qwen_report(results: dict[str, Any]) -> str:
    report = frozen_evaluator.render_report(results)
    original_title = "# Phase B final offline evaluation"
    original_freeze = (
        f"- Inference freeze: `{frozen_evaluator.INFERENCE_TAG}` at "
        f"`{frozen_evaluator.INFERENCE_COMMIT}`."
    )
    if report.count(original_title) != 1 or report.count(original_freeze) != 1:
        raise RuntimeError("frozen evaluator report template changed unexpectedly")
    report = report.replace(
        original_title, "# Phase B EXP2 Qwen final offline evaluation", 1
    ).replace(
        original_freeze,
        "- EXP2 Qwen predictions freeze: "
        f"`{QWEN_PREDICTIONS_FREEZE_TAG}` at `{QWEN_PREDICTIONS_FREEZE_COMMIT}`.",
        1,
    )
    if (
        frozen_evaluator.INFERENCE_TAG in report
        or frozen_evaluator.INFERENCE_COMMIT in report
    ):
        raise RuntimeError("Terra inference provenance leaked into Qwen report")
    return report


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
    results["reproducibility"].update(provenance)
    results["reproducibility"]["evaluator_code_sha256"] = FROZEN_EVALUATOR_SHA256
    artifacts["evaluation_results.json"] = canonical_bytes(results)
    artifacts["EVALUATION_REPORT.md"] = render_qwen_report(results).encode("utf-8")

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
        **provenance,
        "primary_prediction_source": relative_source,
        "input_aggregate_predictions_sha256": sha256_file(AGGREGATE_PATH),
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
