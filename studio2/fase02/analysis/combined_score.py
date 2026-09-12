#!/usr/bin/env python3
"""Fit and apply the executable Studio 2 combined Normal score."""

from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

from tep_features import (
    XMEAS,
    BaselineStats,
    analyze_window,
    compute_baseline_stats_from_blocks,
    iter_time_windows,
    load_case,
    normalize_schema,
    sampling_interval_hours,
)


FEATURES = (
    "abs_shift_sigma",
    "abs_slope_sigma_h",
    "residual_std_ratio",
    "diff_std_ratio",
)
ROWS_PER_BLOCK = 3000
BLOCK_HOURS = 50.0
WINDOW_HOURS = 5.0


def _sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


@dataclass(frozen=True)
class RobustParameters:
    center: dict[str, float]
    mad: dict[str, float]
    offset: dict[str, float] | None


@dataclass(frozen=True)
class ScoreFit:
    variant: str
    parameters: RobustParameters
    dominance: dict[str, float]
    dominance_max: float
    baseline_windows: int
    baseline_values_per_feature: int


def load_n1_n5(path: str | Path) -> list[pd.DataFrame]:
    normal = normalize_schema(
        pd.read_excel(path, nrows=5 * ROWS_PER_BLOCK), source=str(path)
    )
    if len(normal) != 5 * ROWS_PER_BLOCK:
        raise ValueError(f"expected 15000 rows for N1-N5, found {len(normal)}")
    interval = sampling_interval_hours(normal)
    if not np.isclose(interval, 1 / 60, rtol=0, atol=1e-12):
        raise ValueError(f"expected one-minute sampling, found {interval}")
    blocks = []
    for index in range(5):
        left = index * BLOCK_HOURS
        right = left + BLOCK_HOURS
        block = normal[(normal.Time >= left) & (normal.Time < right)].copy()
        if len(block) != ROWS_PER_BLOCK:
            raise ValueError(f"N{index + 1}: expected 3000 rows, found {len(block)}")
        blocks.append(block)
    return blocks


def baseline_window_features(
    blocks: Iterable[pd.DataFrame], baseline: BaselineStats
) -> list[pd.DataFrame]:
    feature_tables = []
    for block_index, block in enumerate(blocks):
        for _, _, window in iter_time_windows(
            block,
            start_h=block_index * BLOCK_HOURS,
            end_h=(block_index + 1) * BLOCK_HOURS,
            window_h=WINDOW_HOURS,
        ):
            feature_tables.append(analyze_window(window, baseline))
    if len(feature_tables) != 50:
        raise RuntimeError(f"expected 50 baseline windows, found {len(feature_tables)}")
    return feature_tables


def _mad(values: np.ndarray) -> float:
    center = float(np.median(values))
    return float(np.median(np.abs(values - center)))


def fit_parameters(feature_tables: list[pd.DataFrame], variant: str) -> RobustParameters:
    center: dict[str, float] = {}
    mad: dict[str, float] = {}
    offset: dict[str, float] | None = {} if variant == "A_prime" else None
    for feature in FEATURES:
        values = np.concatenate(
            [table[feature].to_numpy(dtype=float) for table in feature_tables]
        )
        if len(values) != len(feature_tables) * len(XMEAS):
            raise RuntimeError(f"unexpected value count for {feature}")
        if not np.isfinite(values).all() or np.any(values < 0):
            raise ValueError(f"{feature}: values must be finite and non-negative")
        transformed = values
        if variant == "A_prime":
            positive = values[values > 0]
            if not len(positive):
                raise ValueError(f"{feature}: c_f is undefined; no positive values")
            scale = float(np.median(positive))
            assert offset is not None
            offset[feature] = scale
            transformed = np.log1p(values / scale)
        feature_center = float(np.median(transformed))
        feature_mad = _mad(transformed)
        if not np.isfinite(feature_mad) or feature_mad <= 0:
            raise ValueError(f"{feature}: MAD is zero or non-finite")
        center[feature] = feature_center
        mad[feature] = feature_mad
    return RobustParameters(center=center, mad=mad, offset=offset)


def score_feature_table(
    table: pd.DataFrame, parameters: RobustParameters
) -> tuple[float, np.ndarray]:
    family_maxima = []
    for feature in FEATURES:
        values = table[feature].to_numpy(dtype=float)
        if parameters.offset is not None:
            values = np.log1p(values / parameters.offset[feature])
        z_values = (values - parameters.center[feature]) / parameters.mad[feature]
        if not np.isfinite(z_values).all():
            raise ValueError(f"{feature}: non-finite standardized value")
        family_maxima.append(float(np.max(z_values)))
    maxima = np.asarray(family_maxima)
    return float(np.max(maxima)), maxima


def dominance(
    feature_tables: list[pd.DataFrame], parameters: RobustParameters
) -> tuple[dict[str, float], float]:
    weights = np.zeros(len(FEATURES), dtype=float)
    for table in feature_tables:
        _, maxima = score_feature_table(table, parameters)
        winners = np.flatnonzero(maxima == np.max(maxima))
        weights[winners] += 1.0 / len(winners)
    fractions = weights / len(feature_tables)
    result = {feature: float(fractions[index]) for index, feature in enumerate(FEATURES)}
    return result, float(np.max(fractions))


def fit_score(blocks: list[pd.DataFrame]) -> tuple[BaselineStats, ScoreFit]:
    baseline = compute_baseline_stats_from_blocks(blocks)
    tables = baseline_window_features(blocks, baseline)
    parameters_a = fit_parameters(tables, "A")
    dominance_a, maximum_a = dominance(tables, parameters_a)
    if maximum_a <= 0.70:
        return baseline, ScoreFit(
            variant="A",
            parameters=parameters_a,
            dominance=dominance_a,
            dominance_max=maximum_a,
            baseline_windows=len(tables),
            baseline_values_per_feature=len(tables) * len(XMEAS),
        )

    parameters_ap = fit_parameters(tables, "A_prime")
    dominance_ap, maximum_ap = dominance(tables, parameters_ap)
    if maximum_ap < maximum_a:
        return baseline, ScoreFit(
            variant="A_prime",
            parameters=parameters_ap,
            dominance=dominance_ap,
            dominance_max=maximum_ap,
            baseline_windows=len(tables),
            baseline_values_per_feature=len(tables) * len(XMEAS),
        )
    return baseline, ScoreFit(
        variant="A",
        parameters=parameters_a,
        dominance=dominance_a,
        dominance_max=maximum_a,
        baseline_windows=len(tables),
        baseline_values_per_feature=len(tables) * len(XMEAS),
    )


def score_case_windows(
    path: str | Path,
    baseline: BaselineStats,
    fit: ScoreFit,
    *,
    start_h: float,
    end_h: float,
) -> pd.DataFrame:
    case = load_case(path)
    rows = []
    for position, (left, right, window) in enumerate(
        iter_time_windows(
            case, start_h=start_h, end_h=end_h, window_h=WINDOW_HOURS
        ),
        start=1,
    ):
        table = analyze_window(window, baseline)
        score, maxima = score_feature_table(table, fit.parameters)
        row = {
            "position": position,
            "window_start_h": left,
            "window_end_h": right,
            "S": score,
        }
        row.update(
            {f"max_z_{feature}": maxima[index] for index, feature in enumerate(FEATURES)}
        )
        rows.append(row)
    return pd.DataFrame(rows)


def serializable_fit(fit: ScoreFit) -> dict[str, object]:
    result = asdict(fit)
    result["feature_order"] = list(FEATURES)
    result["mad_definition"] = "median(abs(x - median(x))); no consistency scaling"
    result["dominance_ties"] = "exact cross-family ties share one window equally"
    result["selection_rule"] = (
        "A if dominance_max(A)<=0.70; otherwise A_prime only if its dominance "
        "strictly decreases; ties or worsening keep A"
    )
    return result


def serializable_baseline(baseline: BaselineStats) -> dict[str, dict[str, float]]:
    return {
        "mean": {key: float(value) for key, value in baseline.mean.items()},
        "std": {key: float(value) for key, value in baseline.std.items()},
        "diff_std": {key: float(value) for key, value in baseline.diff_std.items()},
        "residual_std": {
            key: float(value) for key, value in baseline.residual_std.items()
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--normal", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[3]
    output = args.output.resolve()
    try:
        output.relative_to(repo_root / "studio2")
    except ValueError:
        parser.error("output must remain below studio2/")
    if output.exists():
        parser.error(f"refusing to overwrite {output}")

    baseline, fit = fit_score(load_n1_n5(args.normal))
    result = serializable_fit(fit)
    result["baseline_reference"] = serializable_baseline(baseline)
    result["baseline_source_sha256"] = _sha256(args.normal)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"variant={fit.variant} dominance_max={fit.dominance_max:.6f}")
    print(f"OK: {output.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
