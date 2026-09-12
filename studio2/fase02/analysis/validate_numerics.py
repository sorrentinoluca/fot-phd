#!/usr/bin/env python3
"""Apply the pre-registered burn-in, generator, replay, and prefix gates."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from combined_score import (
    FEATURES,
    RobustParameters,
    ScoreFit,
    fit_score,
    load_n1_n5,
    score_case_windows,
    score_feature_table,
)
from tep_features import BaselineStats, analyze_window, iter_time_windows, load_case


@dataclass(frozen=True)
class ComparisonLimits:
    median_shift_mad: float = 0.5
    mad_ratio_low: float = 0.5
    mad_ratio_high: float = 2.0


def median_and_mad(values: np.ndarray) -> tuple[float, float]:
    median = float(np.median(values))
    mad = float(np.median(np.abs(values - median)))
    return median, mad


def compare_values(
    candidate: np.ndarray,
    reference: np.ndarray,
    limits: ComparisonLimits = ComparisonLimits(),
) -> dict[str, float | bool]:
    candidate_median, candidate_mad = median_and_mad(candidate)
    reference_median, reference_mad = median_and_mad(reference)
    if not np.isfinite(reference_mad) or reference_mad <= 0:
        return {
            "candidate_median": candidate_median,
            "candidate_mad": candidate_mad,
            "reference_median": reference_median,
            "reference_mad": reference_mad,
            "median_shift_in_reference_mad": float("inf"),
            "mad_ratio": float("inf"),
            "pass": False,
        }
    median_shift = abs(candidate_median - reference_median) / reference_mad
    mad_ratio = candidate_mad / reference_mad
    passed = bool(
        np.isfinite(candidate_mad)
        and median_shift <= limits.median_shift_mad
        and limits.mad_ratio_low <= mad_ratio <= limits.mad_ratio_high
    )
    return {
        "candidate_median": candidate_median,
        "candidate_mad": candidate_mad,
        "reference_median": reference_median,
        "reference_mad": reference_mad,
        "median_shift_in_reference_mad": median_shift,
        "mad_ratio": mad_ratio,
        "pass": passed,
    }


def evaluate_burn_in(
    paths: list[Path], baseline: BaselineStats, fit: ScoreFit
) -> dict[str, object]:
    del fit  # feature families, rather than S, are the frozen burn-in criterion
    candidate_hours = (10, 20, 30, 40)
    reference = _feature_only_values(paths, baseline, 60, 70)
    candidates: dict[str, object] = {}
    pass_by_hour: dict[int, bool] = {}
    for hour in candidate_hours:
        candidate = _feature_only_values(paths, baseline, hour, hour + 10)
        comparisons = {
            feature: compare_values(candidate[feature], reference[feature])
            for feature in FEATURES
        }
        passed = all(bool(item["pass"]) for item in comparisons.values())
        pass_by_hour[hour] = passed
        candidates[str(hour)] = {"pass": passed, "features": comparisons}
    selected = next(
        (
            hour
            for hour in (20, 30)
            if pass_by_hour[hour]
            and pass_by_hour[candidate_hours[candidate_hours.index(hour) + 1]]
        ),
        None,
    )
    return {
        "run_count": len(paths),
        "reference_interval_hours": [60, 70],
        "candidates": candidates,
        "selected_burn_in_hours": selected,
        "pass": selected is not None,
    }


def _feature_only_values(
    paths: list[Path], baseline: BaselineStats, start_h: float, end_h: float
) -> dict[str, np.ndarray]:
    values = {feature: [] for feature in FEATURES}
    for path in paths:
        case = load_case(path)
        for _, _, window in iter_time_windows(
            case, start_h=start_h, end_h=end_h, window_h=5.0
        ):
            table = analyze_window(window, baseline)
            for feature in FEATURES:
                values[feature].extend(table[feature].to_numpy(dtype=float))
    return {feature: np.asarray(items) for feature, items in values.items()}


def evaluate_generator_comparison(
    philox_paths: list[Path],
    legacy_paths: list[Path],
    baseline: BaselineStats,
    fit: ScoreFit,
    burn_in_h: float,
) -> dict[str, object]:
    def all_values(paths: list[Path]) -> dict[str, np.ndarray]:
        values = _feature_only_values(paths, baseline, burn_in_h, burn_in_h + 50)
        scores = []
        for path in paths:
            score_table = score_case_windows(
                path,
                baseline,
                fit,
                start_h=burn_in_h,
                end_h=burn_in_h + 50,
            )
            scores.extend(score_table.S.to_numpy(dtype=float))
        values["S"] = np.asarray(scores)
        return values

    philox = all_values(philox_paths)
    legacy = all_values(legacy_paths)
    comparisons = {
        metric: compare_values(philox[metric], legacy[metric])
        for metric in (*FEATURES, "S")
    }
    return {
        "philox_run_count": len(philox_paths),
        "legacy_run_count": len(legacy_paths),
        "burn_in_hours": burn_in_h,
        "metrics": comparisons,
        "pass": all(bool(item["pass"]) for item in comparisons.values()),
    }


def evaluate_r2_guard(
    pilot_paths: list[Path],
    historical_blocks: list[pd.DataFrame],
    baseline: BaselineStats,
    fit: ScoreFit,
    burn_in_h: float,
) -> dict[str, object]:
    pilot = _feature_only_values(pilot_paths, baseline, burn_in_h, burn_in_h + 50)
    historical_tables = []
    for block_index, block in enumerate(historical_blocks):
        historical_tables.extend(
            analyze_window(window, baseline)
            for _, _, window in iter_time_windows(
                block,
                start_h=block_index * 50,
                end_h=(block_index + 1) * 50,
                window_h=5,
            )
        )
    historical = {
        feature: np.concatenate(
            [table[feature].to_numpy(dtype=float) for table in historical_tables]
        )
        for feature in FEATURES
    }
    historical["S"] = np.asarray(
        [score_feature_table(table, fit.parameters)[0] for table in historical_tables]
    )
    pilot_scores = []
    for path in pilot_paths:
        pilot_scores.extend(
            score_case_windows(
                path,
                baseline,
                fit,
                start_h=burn_in_h,
                end_h=burn_in_h + 50,
            ).S.to_numpy(dtype=float)
        )
    pilot["S"] = np.asarray(pilot_scores)
    comparisons = {
        metric: compare_values(pilot[metric], historical[metric])
        for metric in (*FEATURES, "S")
    }
    passed = all(bool(item["pass"]) for item in comparisons.values())
    return {
        "pilot_run_count": len(pilot_paths),
        "historical_block_count": len(historical_blocks),
        "burn_in_hours": burn_in_h,
        "metrics": comparisons,
        "fallback": None if passed else "baseline_fit_new_100_runs_and_cal_thr_300",
        "pass": passed,
    }
def evaluate_prefixes(
    runs_dir: Path,
    baseline: BaselineStats,
    fit: ScoreFit,
    burn_in_h: float,
) -> dict[str, object]:
    manifest = pd.read_csv(runs_dir / "generation_manifest.csv")
    required_manifest = {
        "run_id",
        "stream_id",
        "rng_algorithm",
        "rng_key_hex",
        "counter_start",
        "counter_end",
        "mex_sha256",
        "model_sha256",
        "ts_base_h",
        "output_interval_h",
        "status",
    }
    missing_manifest = sorted(required_manifest - set(manifest.columns))
    if missing_manifest:
        raise ValueError(f"prefix manifest missing columns: {missing_manifest}")
    comparisons: list[dict[str, object]] = []
    counter_checks: list[dict[str, object]] = []
    for ordinal in range(1, 11):
        stream_id = 99 + ordinal
        stream_manifest = manifest[manifest.stream_id == stream_id].copy()
        short_manifest = stream_manifest[
            stream_manifest.run_id.str.match(r"^prefix_qual-\d{3}-j\d{2}$")
        ].sort_values("window_position")
        full_manifest = stream_manifest[
            stream_manifest.run_id == f"prefix_qual-{ordinal:03d}-full"
        ]
        configuration_exact = bool(
            len(stream_manifest) == 11
            and len(short_manifest) == 10
            and len(full_manifest) == 1
            and set(stream_manifest.status) == {"complete"}
            and set(stream_manifest.rng_algorithm) == {"Philox4x32-10"}
            and set(stream_manifest.rng_key_hex) == {"0x464f545445503032"}
            and len(set(stream_manifest.mex_sha256)) == 1
            and len(set(stream_manifest.model_sha256)) == 1
            and set(stream_manifest.ts_base_h) == {0.0005}
            and np.allclose(stream_manifest.output_interval_h, 1 / 60)
            and set(stream_manifest.counter_start) == {0}
        )
        counters = short_manifest.counter_end.to_numpy(dtype=np.uint64)
        counter_monotonic = bool(len(counters) == 10 and np.all(counters[1:] > counters[:-1]))
        final_counter_equal = bool(
            len(counters) == 10
            and len(full_manifest) == 1
            and counters[-1] == np.uint64(full_manifest.iloc[0].counter_end)
        )
        counter_checks.append(
            {
                "stream_id": stream_id,
                "configuration_exact": configuration_exact,
                "short_counter_strictly_increasing": counter_monotonic,
                "j10_counter_equals_full": final_counter_equal,
                "pass": bool(configuration_exact and counter_monotonic and final_counter_equal),
            }
        )
        full_path = runs_dir / f"prefix_qual-{ordinal:03d}-full.xlsx"
        full = load_case(full_path)
        full_scores = score_case_windows(
            full_path, baseline, fit, start_h=burn_in_h, end_h=burn_in_h + 50
        )
        for position in range(1, 11):
            short_path = runs_dir / f"prefix_qual-{ordinal:03d}-j{position:02d}.xlsx"
            short = load_case(short_path)
            stop_h = burn_in_h + 5 * position
            full_common = full[full.Time < stop_h].reset_index(drop=True)
            short_common = short[short.Time < stop_h].reset_index(drop=True)
            grid_equal = bool(
                len(full_common) == len(short_common)
                and np.array_equal(
                    full_common.Time.to_numpy(), short_common.Time.to_numpy()
                )
            )
            raw_close = bool(
                grid_equal
                and np.allclose(
                    full_common.iloc[:, 1:].to_numpy(),
                    short_common.iloc[:, 1:].to_numpy(),
                    atol=1e-10,
                    rtol=1e-9,
                )
            )

            feature_close = grid_equal
            max_feature_abs = 0.0
            if grid_equal:
                for window_index in range(position):
                    left = burn_in_h + 5 * window_index
                    right = left + 5
                    full_window = full_common[
                        (full_common.Time >= left) & (full_common.Time < right)
                    ]
                    short_window = short_common[
                        (short_common.Time >= left) & (short_common.Time < right)
                    ]
                    full_features = analyze_window(full_window, baseline)[list(FEATURES)]
                    short_features = analyze_window(short_window, baseline)[list(FEATURES)]
                    difference = np.abs(
                        full_features.to_numpy() - short_features.to_numpy()
                    )
                    max_feature_abs = max(max_feature_abs, float(np.max(difference)))
                    feature_close = bool(
                        feature_close
                        and np.allclose(
                            full_features.to_numpy(),
                            short_features.to_numpy(),
                            atol=1e-10,
                            rtol=1e-8,
                        )
                    )

            short_scores = score_case_windows(
                short_path,
                baseline,
                fit,
                start_h=burn_in_h,
                end_h=stop_h,
            )
            score_abs = (
                abs(float(full_scores.iloc[position - 1].S) - float(short_scores.iloc[-1].S))
                if len(short_scores) == position
                else float("inf")
            )
            score_close = bool(np.isfinite(score_abs) and score_abs <= 1e-8)
            item_pass = bool(grid_equal and raw_close and feature_close and score_close)
            raw_max_abs = (
                float(
                    np.max(
                        np.abs(
                            full_common.iloc[:, 1:].to_numpy()
                            - short_common.iloc[:, 1:].to_numpy()
                        )
                    )
                )
                if grid_equal
                else float("inf")
            )
            comparisons.append(
                {
                    "stream_id": stream_id,
                    "position": position,
                    "stop_time_h": stop_h,
                    "rows_half_open": len(short_common),
                    "time_grid_exact": grid_equal,
                    "raw_close": raw_close,
                    "raw_max_abs_difference": raw_max_abs,
                    "features_close": feature_close,
                    "feature_max_abs_difference": max_feature_abs,
                    "score_absolute_difference": score_abs,
                    "pass": item_pass,
                }
            )
    failures = [item for item in comparisons if not bool(item["pass"])]
    counter_failures = [item for item in counter_checks if not bool(item["pass"])]
    return {
        "stream_count": 10,
        "comparisons": len(comparisons),
        "burn_in_hours": burn_in_h,
        "score_variant": fit.variant,
        "failures": len(failures),
        "counter_check_failures": len(counter_failures),
        "counter_check_scope": (
            "same key/stream, counter starts at zero, short-run endpoints increase, "
            "and J=10 endpoint equals the independently executed full-run endpoint"
        ),
        "fallback": "full_length_calibration_runs" if failures or counter_failures else None,
        "pass": not failures and not counter_failures,
        "counter_checks": counter_checks,
        "details": comparisons,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    burn = subparsers.add_parser("burn-in")
    burn.add_argument("--runs", required=True, type=Path)
    compare = subparsers.add_parser("generators")
    compare.add_argument("--philox", required=True, type=Path)
    compare.add_argument("--legacy", required=True, type=Path)
    compare.add_argument("--burn-in-hours", required=True, type=float)
    prefixes = subparsers.add_parser("prefixes")
    prefixes.add_argument("--runs", required=True, type=Path)
    prefixes.add_argument("--burn-in-hours", required=True, type=float)
    r2 = subparsers.add_parser("r2-guard")
    r2.add_argument("--runs", required=True, type=Path)
    r2.add_argument("--burn-in-hours", required=True, type=float)
    for subparser in (burn, compare, prefixes, r2):
        subparser.add_argument("--normal", required=True, type=Path)
        subparser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    output = args.output.resolve()
    repo_root = Path(__file__).resolve().parents[3]
    try:
        output.relative_to(repo_root / "studio2")
    except ValueError:
        parser.error("output must remain below studio2/")
    if output.exists():
        parser.error(f"refusing to overwrite {output}")

    baseline, fit = fit_score(load_n1_n5(args.normal))
    if args.command == "burn-in":
        paths = sorted(args.runs.glob("*.xlsx"))
        result = evaluate_burn_in(paths, baseline, fit)
    elif args.command == "generators":
        philox_paths = sorted(args.philox.glob("*.xlsx"))
        legacy_paths = sorted(args.legacy.glob("*.xlsx"))
        result = evaluate_generator_comparison(
            philox_paths, legacy_paths, baseline, fit, args.burn_in_hours
        )
    elif args.command == "prefixes":
        result = evaluate_prefixes(args.runs, baseline, fit, args.burn_in_hours)
    else:
        result = evaluate_r2_guard(
            sorted(args.runs.glob("*.xlsx")),
            load_n1_n5(args.normal),
            baseline,
            fit,
            args.burn_in_hours,
        )
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(f"pass={result['pass']} output={output.relative_to(repo_root)}")
    return 0 if result["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
