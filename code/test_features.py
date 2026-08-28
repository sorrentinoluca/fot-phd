#!/usr/bin/env python3
"""Synthetic regression tests for the TEP feature layer.

These tests do not tune TEP thresholds. They establish qualitative invariants:
- raw std is not a valid synonym for oscillation;
- first differences capture fast variability but can miss slow oscillations;
- linear detrending removes a linear drift but not an internal step;
- a step at the window boundary should look like level shift, not variability.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from tep_features import (
    XMEAS,
    analyze_window,
    compute_baseline_stats,
    compute_baseline_stats_from_blocks,
)

SEED = 7
N = 300
DT_H = 1.0 / 60.0


def make_frame(signal: np.ndarray, *, start_h: float = 0.0) -> pd.DataFrame:
    time = start_h + np.arange(len(signal)) * DT_H
    data = {"Time": time}
    # Put the synthetic signal in XMEAS-1 and independent normal noise in the rest.
    rng = np.random.default_rng(SEED + 100)
    data["XMEAS-1"] = signal
    for c in XMEAS[1:]:
        data[c] = rng.normal(0.0, 1.0, len(signal))
    return pd.DataFrame(data)


def metrics(signal: np.ndarray, baseline) -> dict[str, float]:
    row = analyze_window(make_frame(signal), baseline).set_index("variable").loc["XMEAS-1"]
    return {
        "shift": float(row.shift_sigma),
        "slope": float(row.slope_sigma_h),
        "raw": float(row.raw_std_ratio),
        "diff": float(row.diff_std_ratio),
        "residual": float(row.residual_std_ratio),
    }


def main() -> None:
    rng = np.random.default_rng(SEED)
    base_signal = rng.normal(0.0, 1.0, N * 20)
    baseline = compute_baseline_stats(make_frame(base_signal))

    rng = np.random.default_rng(SEED + 1)
    noise = rng.normal(0.0, 1.0, N)
    t = np.arange(N)

    cases = {
        "normal": noise,
        "step_mid": noise + np.where(t >= N // 2, 6.0, 0.0),
        "drift_0_to_6": noise + np.linspace(0.0, 6.0, N),
        "osc_slow_P300": noise + 3.0 * np.sin(2 * np.pi * t / 300.0),
        "osc_fast_P10": noise + 3.0 * np.sin(2 * np.pi * t / 10.0),
        "noise_std_x3": 3.0 * noise,
        "step_plus_slow": noise + np.where(t >= N // 2, 3.0, 0.0) + 2.0 * np.sin(2*np.pi*t/300.0),
        "drift_plus_slow": noise + np.linspace(0.0, 3.0, N) + 2.0 * np.sin(2*np.pi*t/300.0),
        # Entire window is post-step: the discontinuity is outside the window.
        "step_at_boundary": noise + 6.0,
    }

    results = {name: metrics(sig, baseline) for name, sig in cases.items()}
    df = pd.DataFrame(results).T
    print(df.round(3).to_string())

    # Qualitative invariants. These are deliberately broad and not TEP thresholds.
    assert abs(results["normal"]["shift"]) < 0.5
    assert abs(results["step_at_boundary"]["shift"]) > 4.0
    assert results["step_at_boundary"]["diff"] < 1.5
    assert results["step_at_boundary"]["residual"] < 1.5

    # Raw std confounds non-stationarity with variability.
    assert results["step_mid"]["raw"] > 2.0
    assert results["drift_0_to_6"]["raw"] > 1.5

    # Linear detrend removes a linear drift effectively.
    assert results["drift_0_to_6"]["residual"] < 1.5

    # First differences capture fast oscillation/noise variance more than slow oscillation.
    assert results["osc_fast_P10"]["diff"] > results["osc_slow_P300"]["diff"]
    assert results["noise_std_x3"]["diff"] > 2.0

    # Residual variability recovers slow oscillation better than first differences.
    assert results["osc_slow_P300"]["residual"] > results["osc_slow_P300"]["diff"]

    # Pooling blocks must not create a synthetic first difference at a boundary,
    # and linear detrending must be performed independently inside each block.
    block_rng = np.random.default_rng(20260828)
    block_1 = make_frame(
        np.linspace(0.0, 5.0, N) + block_rng.normal(0.0, 0.2, N),
        start_h=0.0,
    )
    block_2 = make_frame(
        100.0 + np.linspace(0.0, 5.0, N) + block_rng.normal(0.0, 0.2, N),
        start_h=50.0,
    )
    block_baseline = compute_baseline_stats_from_blocks([block_1, block_2])
    expected_diff = np.std(
        np.concatenate(
            [np.diff(block_1["XMEAS-1"]), np.diff(block_2["XMEAS-1"])]
        ),
        ddof=1,
    )
    assert np.isclose(block_baseline.diff_std["XMEAS-1"], expected_diff)

    expected_residuals = []
    for block in (block_1, block_2):
        time = block["Time"].to_numpy(dtype=float)
        values = block["XMEAS-1"].to_numpy(dtype=float)
        slope, intercept = np.polyfit(time, values, 1)
        expected_residuals.append(values - (intercept + slope * time))
    expected_residual_std = np.std(np.concatenate(expected_residuals), ddof=1)
    assert np.isclose(
        block_baseline.residual_std["XMEAS-1"], expected_residual_std
    )

    concatenated_baseline = compute_baseline_stats(
        pd.concat([block_1, block_2], ignore_index=True)
    )
    assert concatenated_baseline.diff_std["XMEAS-1"] > 5 * expected_diff

    print("\nSynthetic feature invariants: PASS")


if __name__ == "__main__":
    main()
