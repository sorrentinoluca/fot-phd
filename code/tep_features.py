#!/usr/bin/env python3
"""Core feature extraction for the TEP verbalization layer.

The module deliberately separates four concepts:
- level shift: signed mean displacement in baseline sigma units;
- drift/trend: signed OLS slope in baseline sigma per hour;
- raw dispersion: std ratio (descriptive only, not called oscillation);
- residual/differential variability: complementary instability descriptors.

No diagnostic thresholds or fault labels live here. This is intentional: thresholds
must be selected on development batches and frozen before validation/test.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, Mapping

import numpy as np
import pandas as pd

XMEAS = [f"XMEAS-{i}" for i in range(1, 42)]
EPS = 1e-12


@dataclass(frozen=True)
class BaselineStats:
    mean: pd.Series
    std: pd.Series
    diff_std: pd.Series
    residual_std: pd.Series


def _read_table(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    if suffix == ".csv":
        return pd.read_csv(path)
    raise ValueError(f"Unsupported file type: {path}")


def normalize_schema(df: pd.DataFrame, *, source: str = "<dataframe>") -> pd.DataFrame:
    """Return Time + XMEAS columns with strict validation.

    The normal workbook in mv-per/tennessee-eastman-dataset has misleading
    xmv-1..xmv-41 headers. We rename those only when the shape is exactly
    Time + 41 signals. Fault workbooks may contain additional XMV/cost columns;
    they are ignored after validation.
    """
    d = df.copy()
    d = d.rename(columns={"Time (h)": "Time"})

    if "Time" not in d.columns:
        raise ValueError(f"{source}: missing Time/Time (h) column")

    if not set(XMEAS).issubset(d.columns):
        # Known upstream normal schema: Time + 41 mislabeled signal columns.
        if len(d.columns) == 42:
            rest = list(d.columns[1:])
            looks_like_mislabeled_normal = all(
                str(c).lower().startswith("xmv-") for c in rest
            )
            if looks_like_mislabeled_normal:
                d.columns = ["Time"] + XMEAS
            else:
                missing = sorted(set(XMEAS) - set(map(str, d.columns)))
                raise ValueError(
                    f"{source}: expected XMEAS-1..41; missing {missing[:5]}..."
                )
        else:
            missing = sorted(set(XMEAS) - set(map(str, d.columns)))
            raise ValueError(
                f"{source}: expected XMEAS-1..41; missing {missing[:5]}...; "
                f"column count={len(d.columns)}"
            )

    out = d[["Time"] + XMEAS].copy()
    out["Time"] = pd.to_numeric(out["Time"], errors="raise")
    for c in XMEAS:
        out[c] = pd.to_numeric(out[c], errors="raise")

    if out[XMEAS].isna().any().any():
        bad = out[XMEAS].columns[out[XMEAS].isna().any()].tolist()
        raise ValueError(f"{source}: NaN values in {bad}")
    if out["Time"].isna().any():
        raise ValueError(f"{source}: NaN values in Time")
    if out["Time"].duplicated().any():
        raise ValueError(f"{source}: duplicated timestamps")
    if not out["Time"].is_monotonic_increasing:
        raise ValueError(f"{source}: Time must be strictly increasing")
    return out


def load_case(path: str | Path) -> pd.DataFrame:
    return normalize_schema(_read_table(path), source=str(path))


def sampling_interval_hours(d: pd.DataFrame, *, rtol: float = 1e-9) -> float:
    dt = d["Time"].diff().dropna().to_numpy(dtype=float)
    if len(dt) == 0:
        raise ValueError("Need at least two timestamps")
    med = float(np.median(dt))
    if med <= 0:
        raise ValueError("Non-positive sampling interval")
    if not np.allclose(dt, med, rtol=rtol, atol=max(1e-12, abs(med) * rtol)):
        raise ValueError("Sampling interval is not constant")
    return med


def _ols_slope(time_h: np.ndarray, values: np.ndarray) -> float:
    if len(values) < 2:
        return 0.0
    t = np.asarray(time_h, dtype=float)
    x = np.asarray(values, dtype=float)
    tc = t - t.mean()
    denom = float(np.dot(tc, tc))
    if denom <= EPS:
        return 0.0
    return float(np.dot(tc, x - x.mean()) / denom)


def _linear_residuals(time_h: np.ndarray, values: np.ndarray) -> np.ndarray:
    t = np.asarray(time_h, dtype=float)
    x = np.asarray(values, dtype=float)
    slope = _ols_slope(t, x)
    intercept = float(x.mean() - slope * t.mean())
    return x - (intercept + slope * t)


def _linear_residual_std(time_h: np.ndarray, values: np.ndarray) -> float:
    if len(values) < 3:
        return 0.0
    return float(np.std(_linear_residuals(time_h, values), ddof=1))


def _validate_baseline_stats(
    mean: pd.Series,
    std: pd.Series,
    diff_std: pd.Series,
    residual_std: pd.Series,
) -> BaselineStats:
    invalid = []
    for c in XMEAS:
        if not np.isfinite(std[c]) or std[c] <= EPS:
            invalid.append(f"{c}:std={std[c]}")
        if not np.isfinite(diff_std[c]) or diff_std[c] <= EPS:
            invalid.append(f"{c}:diff_std={diff_std[c]}")
        if not np.isfinite(residual_std[c]) or residual_std[c] <= EPS:
            invalid.append(f"{c}:residual_std={residual_std[c]}")
    if invalid:
        raise ValueError("Degenerate baseline statistics: " + ", ".join(invalid[:8]))

    return BaselineStats(
        mean=mean,
        std=std,
        diff_std=diff_std,
        residual_std=residual_std,
    )


def compute_baseline_stats(normal: pd.DataFrame) -> BaselineStats:
    """Compute baseline statistics on a development-only normal pool."""
    d = normalize_schema(normal, source="baseline")
    mean = d[XMEAS].mean()
    std = d[XMEAS].std(ddof=1)
    diff_std = d[XMEAS].diff().std(ddof=1)

    t = d["Time"].to_numpy(dtype=float)
    residual_std = pd.Series(
        {c: _linear_residual_std(t, d[c].to_numpy(dtype=float)) for c in XMEAS},
        dtype=float,
    )

    return _validate_baseline_stats(mean, std, diff_std, residual_std)


def compute_baseline_stats_from_blocks(
    blocks: Iterable[pd.DataFrame],
) -> BaselineStats:
    """Pool normal blocks without inventing boundaries or cross-block trends."""
    normalized = [
        normalize_schema(block, source=f"baseline block {index}")
        for index, block in enumerate(blocks, start=1)
    ]
    if not normalized:
        raise ValueError("At least one baseline block is required")
    if any(len(block) < 3 for block in normalized):
        raise ValueError("Every baseline block must contain at least 3 samples")

    pooled = pd.concat([block[XMEAS] for block in normalized], ignore_index=True)
    mean = pooled.mean()
    std = pooled.std(ddof=1)

    local_differences = pd.concat(
        [block[XMEAS].diff().iloc[1:] for block in normalized],
        ignore_index=True,
    )
    diff_std = local_differences.std(ddof=1)

    residual_std = pd.Series(index=XMEAS, dtype=float)
    for c in XMEAS:
        residuals = [
            _linear_residuals(
                block["Time"].to_numpy(dtype=float),
                block[c].to_numpy(dtype=float),
            )
            for block in normalized
        ]
        residual_std[c] = float(np.std(np.concatenate(residuals), ddof=1))

    return _validate_baseline_stats(mean, std, diff_std, residual_std)


def analyze_window(window: pd.DataFrame, baseline: BaselineStats) -> pd.DataFrame:
    """Return one row per XMEAS with threshold-free numeric descriptors."""
    w = normalize_schema(window, source="analysis window")
    t = w["Time"].to_numpy(dtype=float)

    rows = []
    for c in XMEAS:
        x = w[c].to_numpy(dtype=float)
        sb = float(baseline.std[c])
        signed_shift_sigma = float((x.mean() - baseline.mean[c]) / sb)
        slope_sigma_h = float(_ols_slope(t, x) / sb)
        raw_std_ratio = float(np.std(x, ddof=1) / sb)

        if len(x) >= 2:
            diff_std = float(np.std(np.diff(x), ddof=1)) if len(x) >= 3 else 0.0
        else:
            diff_std = 0.0
        diff_std_ratio = float(diff_std / baseline.diff_std[c])

        resid_std = _linear_residual_std(t, x)
        residual_std_ratio = float(resid_std / baseline.residual_std[c])

        rows.append(
            {
                "variable": c,
                "shift_sigma": signed_shift_sigma,
                "abs_shift_sigma": abs(signed_shift_sigma),
                "slope_sigma_h": slope_sigma_h,
                "abs_slope_sigma_h": abs(slope_sigma_h),
                "raw_std_ratio": raw_std_ratio,
                "diff_std_ratio": diff_std_ratio,
                "residual_std_ratio": residual_std_ratio,
            }
        )
    return pd.DataFrame(rows)


def iter_time_windows(
    d: pd.DataFrame,
    *,
    start_h: float | None = None,
    end_h: float | None = None,
    window_h: float = 5.0,
) -> Iterator[tuple[float, float, pd.DataFrame]]:
    """Yield left-closed/right-open windows using actual Time values."""
    x = normalize_schema(d, source="window source")
    if window_h <= 0:
        raise ValueError("window_h must be > 0")

    start = float(x["Time"].min()) if start_h is None else float(start_h)
    end = float(x["Time"].max()) if end_h is None else float(end_h)
    left = start
    while left < end - EPS:
        right = min(left + window_h, end)
        mask = (x["Time"] >= left) & (x["Time"] < right)
        w = x.loc[mask]
        if not w.empty:
            yield left, right, w
        left = right


def analyze_case_windows(
    d: pd.DataFrame,
    baseline: BaselineStats,
    *,
    start_h: float,
    end_h: float,
    window_h: float = 5.0,
) -> pd.DataFrame:
    frames = []
    for left, right, w in iter_time_windows(
        d, start_h=start_h, end_h=end_h, window_h=window_h
    ):
        f = analyze_window(w, baseline)
        f.insert(0, "window_end_h", right)
        f.insert(0, "window_start_h", left)
        frames.append(f)
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def top_variables(features: pd.DataFrame, metric: str, k: int = 5) -> list[str]:
    if metric not in features.columns:
        raise KeyError(metric)
    score = features[metric].abs() if metric in {"shift_sigma", "slope_sigma_h"} else features[metric]
    idx = score.nlargest(k).index
    return features.loc[idx, "variable"].tolist()
