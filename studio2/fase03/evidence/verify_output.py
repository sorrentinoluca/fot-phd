#!/usr/bin/env python3
"""Verify a complete 03.6 evidence tree without using evaluator labels as features."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

try:
    from .extract_evidence import (
        EXPECTED_BASELINE_SHA256,
        EXPECTED_R2_GUARD_SHA256,
        EXPECTED_RUNS,
        EXPECTED_WINDOWS_PER_RUN,
        SIGNATURE_DIMENSION,
        sha256_file,
    )
    from .leakage import assert_no_leakage
except ImportError:
    from extract_evidence import (
        EXPECTED_BASELINE_SHA256,
        EXPECTED_R2_GUARD_SHA256,
        EXPECTED_RUNS,
        EXPECTED_WINDOWS_PER_RUN,
        SIGNATURE_DIMENSION,
        sha256_file,
    )
    from leakage import assert_no_leakage


EXPECTED_UNITS = EXPECTED_RUNS * EXPECTED_WINDOWS_PER_RUN
EXPECTED_FAULTS = {"F1", "F2", "F3", "F8", "F10", "F13", "F14", "F15"}


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def verify(output_dir: Path) -> dict[str, object]:
    manifest_path = output_dir / "EVIDENCE_MANIFEST.csv"
    index_path = output_dir / "EVALUATOR_INDEX.csv"
    summary_path = output_dir / "EXTRACTION_SUMMARY.json"
    manifest = _csv_rows(manifest_path)
    index = _csv_rows(index_path)
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    if len(manifest) != EXPECTED_UNITS or len(index) != EXPECTED_UNITS:
        raise RuntimeError("Expected 320 rows in both evidence manifest and evaluator index")
    evidence_ids = [row["evidence_id"] for row in manifest]
    if evidence_ids != [f"EVD-{value:04d}" for value in range(1, EXPECTED_UNITS + 1)]:
        raise RuntimeError("Evidence IDs are not the exact ordered EVD-0001..EVD-0320 set")
    if evidence_ids != [row["evidence_id"] for row in index]:
        raise RuntimeError("Evaluator index and evidence manifest IDs disagree")

    files_verified = 0
    bytes_verified = 0
    visible_paths: list[Path] = []
    for row in manifest:
        if row["baseline_sha256"] != EXPECTED_BASELINE_SHA256:
            raise RuntimeError("Unexpected baseline hash in evidence manifest")
        if row["r2_guard_sha256"] != EXPECTED_R2_GUARD_SHA256:
            raise RuntimeError("Unexpected R2 guard hash in evidence manifest")
        if row["regenerate_if_r2_fails"] != "true" or row["leakage_pass"] != "true":
            raise RuntimeError("Conditional validity or leakage marker is not fail-closed")
        for label in ("feature", "json", "text", "signature"):
            path = output_dir / row[f"{label}_path"]
            if not path.is_file():
                raise RuntimeError(f"Missing artifact: {path}")
            if path.stat().st_size != int(row[f"{label}_bytes"]):
                raise RuntimeError(f"Byte count mismatch: {path}")
            if sha256_file(path) != row[f"{label}_sha256"]:
                raise RuntimeError(f"SHA-256 mismatch: {path}")
            files_verified += 1
            bytes_verified += path.stat().st_size
        json_path = output_dir / row["json_path"]
        text_path = output_dir / row["text_path"]
        visible_paths.extend((json_path, text_path))
        if json.loads(json_path.read_text(encoding="utf-8"))["n_windows"] != 1:
            raise RuntimeError(f"JSON is not a single-window unit: {json_path}")
        signature_rows = _csv_rows(output_dir / row["signature_path"])
        if len(signature_rows) != SIGNATURE_DIMENSION:
            raise RuntimeError(f"Signature dimension mismatch for {row['evidence_id']}")
        values = [float(item["value"]) for item in signature_rows]
        if any(value < 0.0 or value > 1.0 for value in values):
            raise RuntimeError(f"Signature outside [0,1] for {row['evidence_id']}")
    assert_no_leakage(visible_paths)

    fault_counts = Counter(row["fault"] for row in index)
    run_counts = Counter(row["run_id"] for row in index)
    stream_counts = Counter(row["stream_id"] for row in index)
    if set(fault_counts) != EXPECTED_FAULTS or set(fault_counts.values()) != {40}:
        raise RuntimeError(f"Unexpected evaluator-side fault counts: {fault_counts}")
    if len(run_counts) != EXPECTED_RUNS or set(run_counts.values()) != {8}:
        raise RuntimeError("Expected eight indexed windows for each of 40 runs")
    if len(stream_counts) != EXPECTED_RUNS or set(stream_counts.values()) != {8}:
        raise RuntimeError("Expected eight indexed windows for each of 40 streams")
    if sha256_file(manifest_path) != summary["evidence_manifest_sha256"]:
        raise RuntimeError("Summary evidence-manifest hash mismatch")
    if sha256_file(index_path) != summary["evaluator_index_sha256"]:
        raise RuntimeError("Summary evaluator-index hash mismatch")

    actual_files = sum(1 for path in output_dir.rglob("*") if path.is_file())
    if actual_files != files_verified + 3:
        raise RuntimeError(
            f"Unexpected extra/missing files: expected {files_verified + 3}, got {actual_files}"
        )
    return {
        "status": "PASS",
        "manifest_rows": len(manifest),
        "index_rows": len(index),
        "artifact_files_verified": files_verified,
        "control_files": 3,
        "total_files": actual_files,
        "artifact_bytes_verified": bytes_verified,
        "total_bytes": sum(
            path.stat().st_size for path in output_dir.rglob("*") if path.is_file()
        ),
        "signature_dimension": SIGNATURE_DIMENSION,
        "leakage": "PASS",
        "fault_counts_evaluator_side": dict(sorted(fault_counts.items())),
        "evidence_manifest_sha256": sha256_file(manifest_path),
        "evaluator_index_sha256": sha256_file(index_path),
        "extraction_summary_sha256": sha256_file(summary_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    parser.add_argument("--check-output", type=Path)
    args = parser.parse_args()
    result = verify(args.output)
    rendered = json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.check_output:
        args.check_output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
