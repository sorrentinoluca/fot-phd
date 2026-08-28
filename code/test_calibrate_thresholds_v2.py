#!/usr/bin/env python3
"""Regression tests for the frozen V2 calibration reproduction."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd

from calibrate_thresholds_v2 import (
    DEFAULT_CONFIG,
    DEFAULT_REFERENCE,
    SCORE_COLUMNS,
    compute_window_scores,
    expected_thresholds,
    load_normal_development,
    thresholds_from_scores,
    verify_thresholds,
)

ROOT = Path(__file__).resolve().parent
COMMITTED_MAXIMA = ROOT / "tep_analysis_v2" / "normal_5h_window_maxima.csv"


def test_committed_order_statistics() -> None:
    scores = pd.read_csv(COMMITTED_MAXIMA)
    calculated, rank = thresholds_from_scores(scores)
    config_values, reference_values = expected_thresholds(
        DEFAULT_CONFIG, DEFAULT_REFERENCE
    )
    assert rank == 49
    verify_thresholds(calculated, config_values, reference_values)


def test_end_to_end(normal_path: str | Path) -> None:
    _, blocks = load_normal_development(normal_path)
    recalculated_scores = compute_window_scores(blocks)
    committed = pd.read_csv(COMMITTED_MAXIMA)
    assert len(recalculated_scores) == len(committed) == 50
    for feature, column in SCORE_COLUMNS.items():
        np.testing.assert_allclose(
            recalculated_scores[column].to_numpy(float),
            committed[column].to_numpy(float),
            rtol=0.0,
            atol=1e-12,
            err_msg=f"Window maxima differ for {feature}",
        )
    calculated, rank = thresholds_from_scores(recalculated_scores)
    config_values, reference_values = expected_thresholds(
        DEFAULT_CONFIG, DEFAULT_REFERENCE
    )
    assert rank == 49
    verify_thresholds(calculated, config_values, reference_values)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--normal",
        help="optional mode1_normal_500.xlsx for full end-to-end regression",
    )
    args = parser.parse_args()
    test_committed_order_statistics()
    print("Committed maxima/order-statistic regression: PASS")
    if args.normal:
        test_end_to_end(args.normal)
        print("End-to-end Normal N1-N5 calibration regression: PASS")
    else:
        print("End-to-end workbook regression: SKIPPED (pass --normal to run)")


if __name__ == "__main__":
    main()
