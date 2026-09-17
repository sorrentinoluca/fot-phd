#!/usr/bin/env python3
"""Technical leave-one-batch-out smoke for the frozen FedAvg implementation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

try:
    from .fedavg import (
        CLIENTS, DIMENSION, LABELS, Config, Dataset, concatenate, evaluate_all_modes,
        load_evidence_bundle, sha256_file, split_leave_one_batch_out, train_all_modes,
        write_metrics, write_weight_hashes,
    )
except ImportError:  # esecuzione diretta dalla cartella fedavg/
    from fedavg import (
        CLIENTS, DIMENSION, LABELS, Config, Dataset, concatenate, evaluate_all_modes,
        load_evidence_bundle, sha256_file, split_leave_one_batch_out, train_all_modes,
        write_metrics, write_weight_hashes,
    )


def synthetic_development_fixture(*, null: bool = False, seed: int = 20260914) -> Dataset:
    """Five balanced run-batches/client, with two windows per physical run."""
    rng = np.random.Generator(np.random.PCG64(seed))
    xs: list[np.ndarray] = []
    ys: list[int] = []
    owners: list[str] = []
    clusters: list[str] = []
    batches: list[str] = []
    for batch in range(1, 6):
        for client_index, client in enumerate(CLIENTS):
            for label, kind in (("Normal", "normal"), (client, "fault")):
                center = np.zeros(DIMENSION, dtype=np.float64)
                if not null:
                    if label == "Normal":
                        center[:8] = -2.0
                    else:
                        center[client_index] = 8.0
                run_id = f"fixture-{kind}-{client}-b{batch:02d}"
                for _window in range(2):
                    noise = np.zeros(DIMENSION)
                    if not null:
                        noise[:8] = rng.normal(0.0, 0.15, 8)
                    xs.append(center + noise)
                    ys.append(LABELS.index(label))
                    owners.append(client)
                    clusters.append(run_id)
                    batches.append(str(batch))
    return Dataset(
        np.stack(xs), np.asarray(ys), np.asarray(owners), np.asarray(clusters), np.asarray(batches)
    )


def _aggregate(rows: list[dict[str, object]]) -> dict[str, float]:
    result: dict[str, float] = {}
    for mode in ("local", "fedavg", "centralized"):
        selected = [row for row in rows if row["mode"] == mode]
        result[mode] = sum(int(row["correct"]) for row in selected) / sum(
            int(row["n_attempts"]) for row in selected
        )
    return result


def run_smoke(dataset: Dataset, output_dir: Path, config: Config = Config()) -> dict[str, object]:
    train, validation = split_leave_one_batch_out(dataset, "5")
    models = train_all_modes(train, config)
    rows = evaluate_all_modes(models, validation)
    output_dir.mkdir(parents=True, exist_ok=True)
    metrics_path = output_dir / "cluster_metrics.csv"
    hashes_path = output_dir / "weight_hashes.json"
    write_metrics(metrics_path, rows)
    write_weight_hashes(hashes_path, models)
    summary = {
        "schema_version": 1,
        "status": "PASS",
        "scope": "technical_leave_one_batch_out_not_a_performance_estimate",
        "held_out_batch": "5",
        "config": config.__dict__,
        "train_samples": len(train.x),
        "validation_samples": len(validation.x),
        "validation_clusters": len(set(validation.clusters.tolist())),
        "aggregate_accuracy": _aggregate(rows),
        "abstention_rate": 0.0,
        "metrics_sha256": sha256_file(metrics_path),
        "weight_hashes_sha256": sha256_file(hashes_path),
    }
    (output_dir / "SMOKE_SUMMARY.json").write_text(
        json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    return summary


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--fault-root", type=Path)
    parser.add_argument("--fault-manifest-sha256")
    parser.add_argument("--fault-index-sha256")
    parser.add_argument("--normal-root", type=Path)
    parser.add_argument("--normal-manifest-sha256")
    parser.add_argument("--normal-index-sha256")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    real_values = (
        args.fault_root, args.fault_manifest_sha256, args.fault_index_sha256,
        args.normal_root, args.normal_manifest_sha256, args.normal_index_sha256,
    )
    if any(real_values) and not all(real_values):
        raise SystemExit("real smoke requires both roots and all four expected SHA-256 values")
    if all(real_values):
        fault = load_evidence_bundle(
            args.fault_root,
            expected_manifest_sha256=args.fault_manifest_sha256,
            expected_index_sha256=args.fault_index_sha256,
        )
        normal = load_evidence_bundle(
            args.normal_root,
            expected_manifest_sha256=args.normal_manifest_sha256,
            expected_index_sha256=args.normal_index_sha256,
        )
        dataset = concatenate((fault, normal))
    else:
        dataset = synthetic_development_fixture()
    summary = run_smoke(dataset, args.out)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
