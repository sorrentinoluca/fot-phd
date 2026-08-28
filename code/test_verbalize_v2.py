#!/usr/bin/env python3
"""Synthetic and development-only regression tests for verbalizer V2."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

from tep_features import XMEAS, compute_baseline_stats
from tep_verbalize_v2 import (
    load_config,
    load_development_baseline,
    verbalize_case,
)

ROOT = Path(__file__).resolve().parent
CACHE = ROOT / "tep_cache"
DT_H = 1.0 / 60.0


def make_frame(target: np.ndarray, *, seed: int, start_h: float = 0.0) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    data: dict[str, np.ndarray] = {
        "Time": start_h + np.arange(len(target)) * DT_H,
        "XMEAS-1": target,
    }
    for variable in XMEAS[1:]:
        data[variable] = rng.normal(0.0, 1.0, len(target))
    return pd.DataFrame(data)


def synthetic_tests(config) -> None:
    baseline_rng = np.random.default_rng(1701)
    baseline = compute_baseline_stats(
        make_frame(baseline_rng.normal(0.0, 1.0, 15000), seed=1702)
    )
    n = 40 * 60
    time = np.arange(n) * DT_H
    rng = np.random.default_rng(1703)
    noise = rng.normal(0.0, 1.0, n)
    fast = 3.0 * np.sin(2.0 * np.pi * np.arange(n) / 10.0)
    slow = 3.0 * np.sin(2.0 * np.pi * time / 10.0)
    step = np.where(time >= 10.0, 6.0, 0.0)
    drift = 0.9 * time

    cases = {
        "normal": noise,
        "step": noise + step,
        "drift": noise + drift,
        "slow_variability": noise + slow,
        "fast_variability": noise + fast,
        "noise_std_x3": 3.0 * noise,
        "step_plus_variability": noise + step + fast,
        "drift_plus_variability": noise + drift + fast,
    }
    results = {
        name: verbalize_case(
            make_frame(values, seed=1800 + index),
            baseline,
            config=config,
            start_h=0.0,
            end_h=40.0,
        )
        for index, (name, values) in enumerate(cases.items())
    }

    normal = results["normal"]["structured"]["variables"]["XMEAS-1"]
    assert normal["level"]["n_active_windows"] == 0

    step_result = results["step"]["structured"]["variables"]["XMEAS-1"]
    assert step_result["level"]["longest_same_sign_run"] >= 6
    assert step_result["level"]["late_regime_active"]

    drift_result = results["drift"]["structured"]["variables"]["XMEAS-1"]
    assert drift_result["trend"]["longest_same_sign_run"] == 8
    assert drift_result["trend"]["strict_global_drift"]

    slow_result = results["slow_variability"]["structured"]["variables"]["XMEAS-1"]
    assert slow_result["residual_variability"]["n_active_windows"] > 0
    assert (
        slow_result["residual_variability"]["n_active_windows"]
        > slow_result["rapid_variability"]["n_active_windows"]
    )

    fast_result = results["fast_variability"]["structured"]["variables"]["XMEAS-1"]
    normal_diff = np.median(
        [row["diff_std_ratio"] for row in normal["per_window"]]
    )
    fast_diff = np.median(
        [row["diff_std_ratio"] for row in fast_result["per_window"]]
    )
    assert fast_diff > normal_diff
    assert (
        fast_result["sample_to_sample_variation"]["n_active_windows"]
        >= normal["sample_to_sample_variation"]["n_active_windows"]
    )

    noise_result = results["noise_std_x3"]["structured"]["variables"]["XMEAS-1"]
    assert (
        noise_result["residual_variability"]["n_active_windows"]
        > normal["residual_variability"]["n_active_windows"]
    )

    # The step begins exactly at a 5 h boundary. Its discontinuity is outside
    # the post-step window and must not create sustained rapid evidence.
    assert step_result["rapid_variability"]["longest_run"] < 2

    normal_slope = np.median(
        [abs(row["slope_sigma_h"]) for row in normal["per_window"]]
    )
    drift_slope = np.median(
        [abs(row["slope_sigma_h"]) for row in drift_result["per_window"]]
    )
    assert drift_slope > normal_slope

    combined_step = results["step_plus_variability"]["structured"]["variables"]["XMEAS-1"]
    assert combined_step["level"]["late_regime_active"]
    combined_step_diff = np.median(
        [row["diff_std_ratio"] for row in combined_step["per_window"]]
    )
    step_diff = np.median(
        [row["diff_std_ratio"] for row in step_result["per_window"]]
    )
    assert combined_step_diff > step_diff

    combined_drift = results["drift_plus_variability"]["structured"]["variables"]["XMEAS-1"]
    assert combined_drift["trend"]["late_regime_active"]
    combined_drift_diff = np.median(
        [row["diff_std_ratio"] for row in combined_drift["per_window"]]
    )
    drift_diff = np.median(
        [row["diff_std_ratio"] for row in drift_result["per_window"]]
    )
    assert combined_drift_diff > drift_diff

    forbidden = [term.lower() for term in config["vocabulary"]["forbidden_automatic"]]
    for result in results.values():
        text = result["text"].lower()
        assert not any(term in text for term in forbidden)
        assert not any(label in text for label in ("guasto a", "guasto b", "guasto c", "guasto d"))
        assert "fault" not in text
        assert "rapporto tra deviazioni standard" in text

    # Structured schema and temporal counters must agree with the per-window
    # evidence used by the renderer.
    structured = results["step"]["structured"]
    assert {"time_range_h", "variables", "system_summary"} <= set(structured)
    required = {
        "n_active_windows", "active_fraction", "positive_count",
        "negative_count", "sign_consistency", "longest_same_sign_run",
        "first_active_window", "last_active_window", "early_active",
        "late_active",
    }
    assert required <= set(step_result["level"])
    observed = sum(row["level_candidate"] for row in step_result["per_window"])
    assert step_result["level"]["n_active_windows"] == observed
    assert f"{observed}/{structured['n_windows']} finestre" in results["step"]["text"]


def normal_calibration_tolerance_test(config) -> None:
    features = pd.read_csv(ROOT / "tep_analysis_v2" / "normal_5h_variable_features.csv")
    thresholds = config["thresholds"]
    flags = features.assign(
        level=features.abs_shift_sigma > thresholds["abs_shift_sigma"],
        trend=features.abs_slope_sigma_h > thresholds["abs_slope_sigma_h"],
        residual=features.residual_std_ratio > thresholds["residual_std_ratio"],
        diff=features.diff_std_ratio > thresholds["diff_std_ratio"],
    )
    by_window = flags.groupby("normal_window_id")[["level", "trend", "residual", "diff"]].any()
    assert by_window.sum().to_dict() == {
        "level": 1, "trend": 1, "residual": 1, "diff": 1
    }
    assert int(by_window.any(axis=1).sum()) == 3


def development_tests(config) -> dict[int, str]:
    baseline = load_development_baseline(CACHE / "mode1_normal_500.xlsx", config)
    examples: dict[int, str] = {}
    for fault in (1, 8, 10, 13):
        for batch in range(1, 6):
            path = CACHE / f"mode1_{fault}_{batch}.xlsx"
            result = verbalize_case(
                pd.read_excel(path), baseline, config=config, end_h=50.0
            )
            structured = result["structured"]
            variables = structured["variables"]
            system = structured["system_summary"]
            assert "fault" not in result["text"].lower()
            assert not any(
                label in result["text"].lower()
                for label in ("guasto a", "guasto b", "guasto c", "guasto d")
            )
            assert not any(
                term.lower() in result["text"].lower()
                for term in config["vocabulary"]["forbidden_automatic"]
            )
            if batch == 1:
                examples[fault] = result["text"]

            if fault == 1:
                x1 = variables["XMEAS-1"]
                assert x1["level"]["strict_global_persistence"]
                assert x1["level"]["dominant_sign"] == "+"
                assert x1["settling_transient"]
                assert not x1["rapid_variability"]["late_regime_active"]
                assert not system["window_activity"]["rapid"]["late_regime_active"]

            elif fault == 8:
                assert len(system["sustained_residual_variables"]) >= 2
                assert system["window_activity"]["residual"]["late_regime_active"]
                assert not system["strict_global_drift_variables"]

            elif fault == 10:
                assert "XMEAS-18" in system["dominant_variables"]["residual"]
                assert "XMEAS-18" in system["dominant_variables"]["diff"]
                x18 = variables["XMEAS-18"]
                assert x18["residual_variability"]["strict_global_persistence"]
                assert x18["level"]["sign_consistency"] < 1.0
                assert x18["trend"]["sign_consistency"] < 1.0

            elif fault == 13:
                assert len(system["sustained_residual_variables"]) >= 4
                x7 = variables["XMEAS-7"]
                assert x7["level"]["negative_count"] > x7["level"]["positive_count"]
                assert not x7["trend"]["strict_global_drift"]

    return examples


def main() -> None:
    config = load_config()
    calibration = json.loads(
        (ROOT / "tep_analysis_v2" / "threshold_calibration.json").read_text()
    )
    calibration_keys = {
        "abs_shift_sigma": "shift_sigma_threshold",
        "abs_slope_sigma_h": "slope_sigma_h_threshold",
        "residual_std_ratio": "residual_std_ratio_threshold",
        "diff_std_ratio": "diff_std_ratio_threshold",
    }
    for config_key, calibration_key in calibration_keys.items():
        assert np.isclose(
            config["thresholds"][config_key],
            calibration[calibration_key],
            rtol=0.0,
            atol=1e-9,
        )
    source = (ROOT / "tep_verbalize_v2.py").read_text()
    for threshold in config["thresholds"].values():
        assert str(threshold) not in source
    synthetic_tests(config)
    print("Synthetic V2 tests: PASS")
    normal_calibration_tolerance_test(config)
    print("Normal calibration tolerance test: PASS")
    examples = development_tests(config)
    print("Development-only V2 regression tests: PASS")
    for fault, text in examples.items():
        print(f"EXAMPLE_F{fault}: {text}")


if __name__ == "__main__":
    main()
