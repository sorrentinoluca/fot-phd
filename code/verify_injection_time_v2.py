#!/usr/bin/env python3
"""Empirical consistency check for the pinned 10 h TEP disturbance delay.

Only already-consumed development data are accepted: F1/F8/F10/F13 batches
1-5 and the frozen Normal N1-N5 baseline. This is not a new injection-time
estimator and does not modify FAULT_INJECT_H or any V2 artifact.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from tep_features import analyze_window, load_case
from tep_verbalize_v2 import load_config, load_development_baseline

ROOT = Path(__file__).resolve().parent
DATASET_COMMIT = "309b944f35ac440ff0c70616947ffe723c766e14"
FAULTS = (1, 8, 10, 13)
BATCHES = (1, 2, 3, 4, 5)
INTERVALS = ((0.0, 5.0), (5.0, 10.0), (10.0, 15.0))
FEATURES = (
    "abs_shift_sigma",
    "abs_slope_sigma_h",
    "residual_std_ratio",
    "diff_std_ratio",
)
FEATURE_LABELS = {
    "abs_shift_sigma": "level",
    "abs_slope_sigma_h": "trend",
    "residual_std_ratio": "residual",
    "diff_std_ratio": "diff",
}


def analyze_development(
    cache_dir: Path, normal_path: Path, config: dict[str, Any]
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    baseline = load_development_baseline(normal_path, config)
    thresholds = config["thresholds"]
    score_rows: list[dict[str, Any]] = []
    recurrence: dict[tuple[int, str, str], Counter[str]] = {}

    for fault in FAULTS:
        for batch in BATCHES:
            path = cache_dir / f"mode1_{fault}_{batch}.xlsx"
            if not path.is_file():
                raise FileNotFoundError(f"Required development workbook missing: {path}")
            case = load_case(path)
            for start, end in INTERVALS:
                interval = f"{start:g}-{end:g}h"
                window = case[(case.Time >= start) & (case.Time < end)].copy()
                if len(window) != 300:
                    raise RuntimeError(
                        f"F{fault} B{batch} {interval}: expected 300 rows, found {len(window)}"
                    )
                features = analyze_window(window, baseline)
                any_primary = False
                for feature in FEATURES:
                    threshold = float(thresholds[feature])
                    active = features[feature] > threshold
                    active_variables = features.loc[active, "variable"].tolist()
                    any_primary = any_primary or bool(active.any())
                    key = (fault, interval, feature)
                    recurrence.setdefault(key, Counter()).update(active_variables)
                    dominant_index = features[feature].idxmax()
                    score_rows.append({
                        "fault": fault,
                        "batch": batch,
                        "interval": interval,
                        "window_start_h": start,
                        "window_end_h": end,
                        "feature": FEATURE_LABELS[feature],
                        "feature_column": feature,
                        "window_score_max_41": float(features[feature].max()),
                        "frozen_threshold": threshold,
                        "score_over_threshold": float(features[feature].max() / threshold),
                        "positive": bool(active.any()),
                        "n_active_variables": int(active.sum()),
                        "active_variables": ";".join(active_variables),
                        "dominant_variable": str(features.loc[dominant_index, "variable"]),
                    })
                score_rows.append({
                    "fault": fault,
                    "batch": batch,
                    "interval": interval,
                    "window_start_h": start,
                    "window_end_h": end,
                    "feature": "any-primary",
                    "feature_column": "any-primary",
                    "window_score_max_41": np.nan,
                    "frozen_threshold": np.nan,
                    "score_over_threshold": np.nan,
                    "positive": any_primary,
                    "n_active_variables": np.nan,
                    "active_variables": "",
                    "dominant_variable": "",
                })

    scores = pd.DataFrame(score_rows)
    summaries = []
    for (fault, interval, feature), group in scores.groupby(
        ["fault", "interval", "feature"], sort=False
    ):
        finite = group.score_over_threshold.dropna()
        summaries.append({
            "fault": fault,
            "interval": interval,
            "feature": feature,
            "positive_batches": int(group.positive.sum()),
            "batches": len(group),
            "positive_fraction": float(group.positive.mean()),
            "median_score_over_threshold": (
                float(finite.median()) if len(finite) else np.nan
            ),
            "maximum_score_over_threshold": (
                float(finite.max()) if len(finite) else np.nan
            ),
        })
    summary = pd.DataFrame(summaries)

    recurrence_rows = []
    for (fault, interval, feature), counts in sorted(recurrence.items()):
        for variable, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            recurrence_rows.append({
                "fault": fault,
                "interval": interval,
                "feature": FEATURE_LABELS[feature],
                "variable": variable,
                "active_batches": count,
                "batches": len(BATCHES),
            })
    return scores, summary, pd.DataFrame(recurrence_rows)


def _value(summary: pd.DataFrame, fault: int, interval: str, feature: str, column: str) -> Any:
    row = summary[
        (summary.fault == fault)
        & (summary.interval == interval)
        & (summary.feature == feature)
    ]
    if len(row) != 1:
        raise RuntimeError(f"Missing summary row: F{fault} {interval} {feature}")
    return row.iloc[0][column]


def make_report(summary: pd.DataFrame, recurrence: pd.DataFrame) -> str:
    lines = [
        "# Injection time verification", "",
        "This document separates source evidence from an empirical consistency check.", "",
        "## Scope", "",
        f"- Dataset snapshot: `{DATASET_COMMIT}`.",
        "- Empirical data: F1/F8/F10/F13 development batches 1–5 only.",
        "- Normal baseline: development blocks N1–N5 only.",
        "- Windows compared: `[0,5 h)`, `[5,10 h)`, and `[10,15 h)`.",
        "- Features and thresholds are the frozen V2 definitions; no value was tuned.",
        "- No claim of statistical identity is made; no hypothesis test is performed.",
        "", "## Source evidence", "",
        "At the pinned dataset commit:", "",
        "1. `simulator/auto_run.m:8-16` creates `dist=zeros(1,28)`, sets "
        "`dist(faultNum)=1`, and calls `sim(modelName)`.",
        "2. `simulator/MultiLoop_mode1.mdl:7774-7778` defines SID 3, a Constant "
        "named `Disturbances`, with value `dist` and sample time `Inf`.",
        "3. `simulator/MultiLoop_mode1.mdl:7849-7854` defines SID 250 as a "
        "`VariableTransportDelay` with two inputs and `MaximumDelay=20`. The "
        "maximum is a capacity parameter, not the applied delay.",
        "4. `simulator/MultiLoop_mode1.mdl:7769-7773` defines SID 249 as a "
        "Constant with value `10`; lines `8046-8051` connect SID 249 output 1 "
        "to SID 250 input 2, proving the applied delay signal is 10.",
        "5. Lines `8063-8067` connect SID 3 output 1 (`dist`) to SID 250 input 1. "
        "Lines `8057-8062` connect SID 250 output 1 to plant subsystem SID 31 "
        "input 13; the plant `Disturbances` inport is port 13 at lines `4800-4804`.",
        "6. `InitialOutput` is not serialized in this R2024b model. The compatible "
        "Simulink default is zero, as recorded in the pre-validation source audit. "
        "Together with the explicit delay-input signal, this yields zero disturbance "
        "output before 10 simulation-time units.",
        "7. `auto_run.m:18-21,37` identifies elapsed time and the saved `Time (h)` "
        "column in hours. The dataset has one-minute sampling and a 50 h stop time, "
        "so the delay value corresponds to 10 h.",
        "", "The documented routing is therefore:", "",
        "`dist -> VariableTransportDelay data input; Constant(10) -> delay input; delayed output -> plant input 13`.",
        "", "## Empirical consistency check", "",
        "Each table entry is the number of development batches whose maximum over "
        "41 XMEAS strictly exceeds the already-frozen feature threshold.", "",
        "| Fault | Interval | Level | Trend | Residual | Diff | Any primary |", "|---|---|---:|---:|---:|---:|---:|",
    ]
    for fault in FAULTS:
        for interval in ["0-5h", "5-10h", "10-15h"]:
            counts = {
                feature: int(_value(summary, fault, interval, feature, "positive_batches"))
                for feature in ["level", "trend", "residual", "diff", "any-primary"]
            }
            lines.append(
                f"| F{fault} | {interval} | {counts['level']}/5 | {counts['trend']}/5 "
                f"| {counts['residual']}/5 | {counts['diff']}/5 | {counts['any-primary']}/5 |"
            )

    lines += ["", "### Score magnitude relative to frozen thresholds", "",
              "Median and maximum refer to the five batch-level maxima; 1.0 is the frozen activation boundary.", "",
              "| Fault | Interval | Feature | Median score/threshold | Maximum score/threshold |",
              "|---|---|---|---:|---:|"]
    for fault in FAULTS:
        for interval in ["0-5h", "5-10h", "10-15h"]:
            for feature in ["level", "trend", "residual", "diff"]:
                median = _value(summary, fault, interval, feature, "median_score_over_threshold")
                maximum = _value(summary, fault, interval, feature, "maximum_score_over_threshold")
                lines.append(
                    f"| F{fault} | {interval} | {feature} | {median:.3f} | {maximum:.3f} |"
                )

    lines += ["", "### Variables active in at least four of five batches", ""]
    recurrent = recurrence[recurrence.active_batches >= 4]
    if recurrent.empty:
        lines.append("No variable reaches this descriptive recurrence count.")
    else:
        for (fault, interval, feature), group in recurrent.groupby(
            ["fault", "interval", "feature"], sort=True
        ):
            values = ", ".join(
                f"{row.variable} ({row.active_batches}/5)"
                for row in group.itertuples(index=False)
            )
            lines.append(f"- F{fault}, {interval}, {feature}: {values}")

    pre = summary[summary.interval.isin(["0-5h", "5-10h"])]
    post_any = summary[
        (summary.interval == "10-15h") & (summary.feature == "any-primary")
    ]
    no_pre_all_batches = not bool((pre.positive_batches == 5).any())
    post_all_batches = bool((post_any.positive_batches == 5).all())
    lines += ["", "## Conclusion", ""]
    if no_pre_all_batches and post_all_batches:
        lines += [
            "Across the frozen feature thresholds, no feature produces a recurring "
            "five-of-five fault response in either pre-10 h window, whereas every "
            "fault has an any-primary response in five of five batches in `[10,15 h)`.",
            "",
            "No systematic fault signature is detectable before 10 h, while the "
            "expected disturbance response appears after 10 h, consistent with the "
            "10 h transport-delay path documented in the simulator.",
        ]
    else:
        lines.append(
            "The empirical pattern does not support the pre-registered consistency "
            "statement without qualification; inspect the tables above."
        )
    lines += ["", "This empirical result is a consistency check, not the primary proof of injection time."]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", default=str(ROOT / "tep_cache"))
    parser.add_argument(
        "--normal", default=str(ROOT / "tep_cache" / "mode1_normal_500.xlsx")
    )
    parser.add_argument("--config", default=str(ROOT / "verbalizer_config_v2.json"))
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()

    config = load_config(args.config)
    if float(config["fault_injection_h"]) != 10.0:
        raise RuntimeError("Frozen config no longer records fault_injection_h=10")
    scores, summary, recurrence = analyze_development(
        Path(args.cache_dir), Path(args.normal), config
    )
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    scores.to_csv(output_dir / "injection_time_window_scores.csv", index=False)
    summary.to_csv(output_dir / "injection_time_summary.csv", index=False)
    recurrence.to_csv(output_dir / "injection_time_active_variable_recurrence.csv", index=False)
    Path(args.report).write_text(make_report(summary, recurrence), encoding="utf-8")
    print(summary.to_string(index=False))
    print(f"Report written to {args.report}")


if __name__ == "__main__":
    main()
