#!/usr/bin/env python3
"""Reproduce the frozen Normal-only V2 threshold calibration.

This script is verification-only. It never writes verbalizer_config_v2.json or
the original threshold_calibration.json. Feature formulas are delegated to the
frozen tep_features module.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from tep_features import (
    XMEAS,
    analyze_window,
    compute_baseline_stats_from_blocks,
    iter_time_windows,
    normalize_schema,
    sampling_interval_hours,
)

ROOT = Path(__file__).resolve().parent
DEFAULT_CONFIG = ROOT / "verbalizer_config_v2.json"
DEFAULT_REFERENCE = ROOT / "tep_analysis_v2" / "threshold_calibration.json"

DATASET_COMMIT = "309b944f35ac440ff0c70616947ffe723c766e14"
ALPHA = 0.05
WINDOW_H = 5.0
BLOCK_H = 50.0
N_BLOCKS = 5
SAMPLES_PER_HOUR = 60
ROWS_PER_BLOCK = int(BLOCK_H * SAMPLES_PER_HOUR)
DEVELOPMENT_ROWS = N_BLOCKS * ROWS_PER_BLOCK

SCORE_COLUMNS = {
    "abs_shift_sigma": "max_abs_shift",
    "abs_slope_sigma_h": "max_abs_slope",
    "residual_std_ratio": "max_residual_ratio",
    "diff_std_ratio": "max_diff_ratio",
}
REFERENCE_KEYS = {
    "abs_shift_sigma": "shift_sigma_threshold",
    "abs_slope_sigma_h": "slope_sigma_h_threshold",
    "residual_std_ratio": "residual_std_ratio_threshold",
    "diff_std_ratio": "diff_std_ratio_threshold",
}


def load_normal_development(path: str | Path) -> tuple[pd.DataFrame, list[pd.DataFrame]]:
    """Read exactly Normal N1-N5 and return five non-overlapping 50 h blocks."""
    raw = pd.read_excel(path, nrows=DEVELOPMENT_ROWS)
    normal = normalize_schema(raw, source="Normal N1-N5 calibration input")
    if len(normal) != DEVELOPMENT_ROWS:
        raise ValueError(f"Expected {DEVELOPMENT_ROWS} rows, found {len(normal)}")
    if float(normal.Time.min()) != 0.0 or float(normal.Time.max()) >= 250.0:
        raise ValueError("Calibration input must contain exactly [0, 250 h)")
    dt = sampling_interval_hours(normal)
    if not np.isclose(dt, 1.0 / 60.0, rtol=0.0, atol=1e-12):
        raise ValueError(f"Expected one-minute sampling, found {dt} h")

    blocks = []
    for index in range(N_BLOCKS):
        left, right = index * BLOCK_H, (index + 1) * BLOCK_H
        block = normal[(normal.Time >= left) & (normal.Time < right)].copy()
        if len(block) != ROWS_PER_BLOCK:
            raise ValueError(f"N{index + 1} has {len(block)} rows")
        blocks.append(block)
    return normal, blocks


def compute_window_scores(blocks: list[pd.DataFrame]) -> pd.DataFrame:
    """Compute 50 leave-one-block-out maxima using frozen feature functions."""
    if len(blocks) != N_BLOCKS:
        raise ValueError(f"Expected {N_BLOCKS} Normal blocks")
    rows: list[dict[str, Any]] = []
    window_id = 0
    for held_index, held_block in enumerate(blocks):
        baseline = compute_baseline_stats_from_blocks(
            block for index, block in enumerate(blocks) if index != held_index
        )
        for window_in_block, (left, right, window) in enumerate(
            iter_time_windows(
                held_block,
                start_h=held_index * BLOCK_H,
                end_h=(held_index + 1) * BLOCK_H,
                window_h=WINDOW_H,
            ),
            start=1,
        ):
            window_id += 1
            features = analyze_window(window, baseline)
            row: dict[str, Any] = {
                "normal_window_id": window_id,
                "normal_block": f"N{held_index + 1}",
                "window_in_block": window_in_block,
                "window_start_h": float(left),
                "window_end_h": float(right),
            }
            for feature, score_column in SCORE_COLUMNS.items():
                row[score_column] = float(features[feature].max())
            row["max_raw_std_ratio"] = float(features["raw_std_ratio"].max())
            rows.append(row)
    scores = pd.DataFrame(rows)
    if len(scores) != 50 or scores.normal_block.value_counts().to_dict() != {
        f"N{i}": 10 for i in range(1, 6)
    }:
        raise RuntimeError("Expected 5 blocks x 10 windows = 50 scores")
    return scores


def thresholds_from_scores(
    scores: pd.DataFrame, *, alpha: float = ALPHA
) -> tuple[dict[str, float], int]:
    """Return the pre-registered upper order statistic without silent clipping."""
    n = len(scores)
    rank = math.ceil((n + 1) * (1.0 - alpha))
    if rank > n:
        raise ValueError(
            f"Rank {rank} exceeds n={n}; a finite threshold is undefined"
        )
    thresholds = {
        feature: float(np.sort(scores[score_column].to_numpy(dtype=float))[rank - 1])
        for feature, score_column in SCORE_COLUMNS.items()
    }
    return thresholds, rank


def expected_thresholds(
    config_path: str | Path, reference_path: str | Path
) -> tuple[dict[str, float], dict[str, float]]:
    config = json.loads(Path(config_path).read_text(encoding="utf-8"))
    reference = json.loads(Path(reference_path).read_text(encoding="utf-8"))
    config_values = {
        feature: float(config["thresholds"][feature]) for feature in SCORE_COLUMNS
    }
    reference_values = {
        feature: float(reference[key]) for feature, key in REFERENCE_KEYS.items()
    }
    return config_values, reference_values


def verify_thresholds(
    calculated: dict[str, float],
    config_values: dict[str, float],
    reference_values: dict[str, float],
    *,
    atol: float = 1e-12,
) -> dict[str, dict[str, float | bool]]:
    comparisons: dict[str, dict[str, float | bool]] = {}
    for feature in SCORE_COLUMNS:
        actual = calculated[feature]
        config_value = config_values[feature]
        reference_value = reference_values[feature]
        config_ok = bool(np.isclose(actual, config_value, rtol=0.0, atol=atol))
        reference_ok = bool(
            np.isclose(actual, reference_value, rtol=0.0, atol=atol)
        )
        comparisons[feature] = {
            "calculated": actual,
            "frozen_config": config_value,
            "calibration_reference": reference_value,
            "abs_error_vs_config": abs(actual - config_value),
            "abs_error_vs_reference": abs(actual - reference_value),
            "matches_with_atol_1e-12": config_ok and reference_ok,
        }
    if not all(item["matches_with_atol_1e-12"] for item in comparisons.values()):
        raise RuntimeError("Recalculated thresholds do not match frozen references")
    return comparisons


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--normal", required=True, help="mode1_normal_500.xlsx")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--reference", default=str(DEFAULT_REFERENCE))
    parser.add_argument(
        "--output",
        required=True,
        help="new verification JSON; frozen config/reference are never overwritten",
    )
    parser.add_argument("--maxima-output", help="optional new CSV with 50 window maxima")
    args = parser.parse_args()

    output = Path(args.output).resolve()
    protected = {Path(args.config).resolve(), Path(args.reference).resolve()}
    if output in protected:
        raise ValueError("Verification output cannot overwrite a frozen/reference file")
    if args.maxima_output and Path(args.maxima_output).resolve() in protected:
        raise ValueError("Maxima output cannot overwrite a frozen/reference file")

    normal, blocks = load_normal_development(args.normal)
    scores = compute_window_scores(blocks)
    calculated, rank = thresholds_from_scores(scores)
    config_values, reference_values = expected_thresholds(args.config, args.reference)
    comparisons = verify_thresholds(calculated, config_values, reference_values)

    result = {
        "verification_only": True,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "dataset_commit": DATASET_COMMIT,
        "normal_blocks": ["N1", "N2", "N3", "N4", "N5"],
        "normal_rows_loaded": len(normal),
        "window_hours": WINDOW_H,
        "calibration_windows": len(scores),
        "variables_per_window": len(XMEAS),
        "baseline": "leave-one-block-out; each Ni window uses the other four blocks",
        "score": "maximum over 41 XMEAS",
        "alpha": ALPHA,
        "rank_formula": "ceil((n+1)*(1-alpha))",
        "rank_1_based": rank,
        "threshold": "49th ordered value",
        "activation": "score > threshold",
        "comparisons": comparisons,
        "all_match": True,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    if args.maxima_output:
        maxima_output = Path(args.maxima_output)
        maxima_output.parent.mkdir(parents=True, exist_ok=True)
        scores.to_csv(maxima_output, index=False)

    for feature, item in comparisons.items():
        print(
            f"{feature}: recalculated={item['calculated']:.17g} "
            f"frozen={item['frozen_config']:.17g} "
            f"abs_error={item['abs_error_vs_config']:.3g}"
        )
    print(f"Calibration reproduction: PASS (n={len(scores)}, rank={rank})")


if __name__ == "__main__":
    main()
