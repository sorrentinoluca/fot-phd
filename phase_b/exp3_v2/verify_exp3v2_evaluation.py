#!/usr/bin/env python3
"""Portable verifier for the minimal EXP3_V2 confirmatory evaluation."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys
from typing import Iterable


sys.dont_write_bytecode = True


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase_b.exp3_v2 import (  # noqa: E402
    evaluate_exp3v2_frozen_predictions as evaluator,
)


OUTPUT_NAMES = {
    "exp3v2_confirmatory_bootstrap.json",
    "exp3v2_confirmatory_results.json",
    "exp3v2_evaluation_output_hash_manifest.json",
}


def verify(args: argparse.Namespace) -> dict[str, object]:
    manifest, _ = evaluator.validate_harness_boundary(args.harness_manifest.resolve())
    roots = {
        "source": args.source_root.resolve(),
        "data": args.data_root.resolve(),
        "verbalization_harness": args.verbalization_harness_root.resolve(),
        "verbalizations": args.verbalizations_root.resolve(),
        "inference_harness": args.inference_harness_root.resolve(),
        "execution_authorization": args.authorization_root.resolve(),
        "inference_outputs": args.inference_root.resolve(),
    }
    evaluator.validate_upstream_checkouts(manifest, roots)
    evaluator.verify_runtime()

    output_root = args.output_root.resolve()
    if output_root.is_symlink() or not output_root.is_dir():
        raise RuntimeError("evaluation output root is missing or symlinked")
    observed = {path.name for path in output_root.iterdir()}
    if observed != OUTPUT_NAMES:
        raise RuntimeError("evaluation output root has missing or extra entries")
    if any(path.is_symlink() or not path.is_file() for path in output_root.iterdir()):
        raise RuntimeError("evaluation outputs must be regular non-symlink files")

    inputs = manifest["inputs"]
    paths = {
        "case_plan": roots["source"] / inputs["case_plan"]["path"],
        "pseudolabel_mapping": roots["source"] / inputs["pseudolabel_mapping"]["path"],
        "data_manifest": roots["data"] / inputs["data_manifest"]["path"],
        "aggregate_records": roots["inference_outputs"]
        / inputs["aggregate_records"]["path"],
    }
    for key, path in paths.items():
        evaluator.verify_file(path, inputs[key])
    with paths["data_manifest"].open(encoding="utf-8", newline="") as stream:
        data_rows = list(csv.DictReader(stream))
    truth = evaluator.validate_case_sources(
        evaluator.load_json(paths["case_plan"]),
        data_rows,
        evaluator.load_json(paths["pseudolabel_mapping"]),
    )
    aggregates = evaluator.load_jsonl(paths["aggregate_records"])
    expected_results, expected_bootstrap = evaluator.confirmatory_bundle(
        aggregates,
        truth,
        aggregate_sha256=inputs["aggregate_records"]["sha256"],
    )
    expected_result_bytes = evaluator.canonical_json_bytes(expected_results)
    expected_bootstrap_bytes = evaluator.canonical_json_bytes(expected_bootstrap)
    evaluator.validate_schema(expected_results, "exp3v2_evaluation_results.schema.json")
    evaluator.validate_schema(
        expected_bootstrap, "exp3v2_evaluation_bootstrap.schema.json"
    )
    for contrast in ("B_minus_A", "B_minus_E"):
        if len(expected_bootstrap[contrast]["distribution"]) != 10000:
            raise RuntimeError("bootstrap distribution does not contain 10,000 draws")
    for condition in evaluator.CONDITIONS:
        metrics = expected_results["condition_metrics"][condition]
        if {name: value["n"] for name, value in metrics.items()} != {
            "unseen": 72,
            "local_seen": 24,
            "normal": 24,
            "overall": 120,
        }:
            raise RuntimeError("evaluation population denominator mismatch")
        for population, metric in metrics.items():
            if metric["correct"] + metric["incorrect"] != metric["n"]:
                raise RuntimeError(
                    f"outcome counts do not cover {condition}/{population}"
                )
            if metric["abstentions"] > metric["incorrect"]:
                raise RuntimeError(
                    f"abstentions are not a subset of errors for {condition}/{population}"
                )
            if population != "unseen" and any(
                key.startswith("ci_") or "success" in key for key in metric
            ):
                raise RuntimeError("secondary descriptive metric contains inference")
    expected_manifest = evaluator.output_manifest(
        expected_result_bytes, expected_bootstrap_bytes
    )
    expected = {
        "exp3v2_confirmatory_results.json": expected_result_bytes,
        "exp3v2_confirmatory_bootstrap.json": expected_bootstrap_bytes,
        "exp3v2_evaluation_output_hash_manifest.json": evaluator.canonical_json_bytes(
            expected_manifest
        ),
    }
    for name, content in expected.items():
        if (output_root / name).read_bytes() != content:
            raise RuntimeError(
                f"evaluation output differs from deterministic result: {name}"
            )
    return {
        "status": "PASS",
        "output_files": 3,
        "aggregate_source_only": True,
        "optional_analyses": 0,
        "metrics_reported": False,
    }


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--harness-manifest", type=Path, required=True)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--verbalization-harness-root", type=Path, required=True)
    parser.add_argument("--verbalizations-root", type=Path, required=True)
    parser.add_argument("--inference-harness-root", type=Path, required=True)
    parser.add_argument("--authorization-root", type=Path, required=True)
    parser.add_argument("--inference-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    result = verify(parse_args(argv))
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
