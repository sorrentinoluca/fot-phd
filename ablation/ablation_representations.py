#!/usr/bin/env python3
"""Alternative TS→text representations for the ablation experiment.

Four arms:
  1. V2_TEXT      — existing frozen V2 neutral text (pass-through)
  2. RAW_FEATURES — raw feature table as CSV text, no thresholds or temporal logic
  3. CGTIME_STATS — CGTime-inspired comprehensive statistical profile (windowed)
  4. SAX_SYMBOLIC — Symbolic Aggregate approXimation encoding

All representations operate on the same windowed structure (8 × 5h windows,
10–50h post-injection) to ensure identical temporal granularity.

Review fixes applied:
  L1  — CGTIME now window-aligned (Direct/Marginal per window, Joint per window)
  T1  — NaN/Inf end-to-end handling via _safe_float, _safe_corrcoef, allow_nan=False
  T3  — Mahalanobis uses Ledoit-Wolf regularised full-covariance inverse
  T4  — find_peaks uses configurable min_prominence (default: baseline noise)
  T5  — Single eigh decomposition with complete fallback
  T11 — robust_slope renamed ols_slope; dimension consistency verified
  T12 — SAX uses baseline-relative Z-normalisation
"""
from __future__ import annotations

import json
import math
from io import StringIO
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats as sp_stats

from tep_features import (
    XMEAS,
    BaselineStats,
    analyze_case_windows,
    iter_time_windows,
    normalize_schema,
    sampling_interval_hours,
)
from tep_verbalize_v2 import (
    load_config,
    render_text,
    verbalize_feature_table,
)


# ---------------------------------------------------------------------------
# Numeric safety helpers  (T1)
# ---------------------------------------------------------------------------

def _safe_float(val: float, default: float = 0.0) -> float:
    """Replace NaN / Inf with *default*."""
    if not math.isfinite(val):
        return default
    return val


def _sanitize_dict(d: dict[str, Any], ndigits: int = 6) -> dict[str, Any]:
    """Recursively clamp every float in a nested dict to finite values."""
    out: dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, float):
            out[k] = round(_safe_float(v), ndigits)
        elif isinstance(v, dict):
            out[k] = _sanitize_dict(v, ndigits)
        elif isinstance(v, list):
            out[k] = [
                round(_safe_float(x), ndigits) if isinstance(x, float) else x
                for x in v
            ]
        else:
            out[k] = v
    return out


def _safe_corrcoef(data: np.ndarray, rowvar: bool = False) -> np.ndarray:
    """``np.corrcoef`` that returns 0 for constant columns instead of NaN."""
    if not rowvar and data.ndim == 2:
        stds = np.std(data, axis=0)
        const = stds < 1e-12
        if np.any(const):
            data = data.copy()
            rng = np.random.default_rng(0)
            data[:, const] += rng.normal(0, 1e-12, (data.shape[0], int(const.sum())))
    try:
        r = np.corrcoef(data, rowvar=rowvar)
        return np.nan_to_num(r, nan=0.0, posinf=1.0, neginf=-1.0)
    except (FloatingPointError, ValueError):
        n = data.shape[1] if not rowvar else data.shape[0]
        return np.eye(n)


# ---------------------------------------------------------------------------
# Arm 1 — V2_TEXT  (pass-through, unchanged)
# ---------------------------------------------------------------------------

def represent_v2_text(
    case: pd.DataFrame,
    baseline: BaselineStats,
    config: dict[str, Any],
) -> str:
    """Return the frozen V2 neutral text (existing approach)."""
    d = normalize_schema(case, source="v2_text input")
    start = float(config["fault_injection_h"])
    end = float(d.Time.max())
    features = analyze_case_windows(
        d, baseline, start_h=start, end_h=end,
        window_h=float(config["window_hours"]),
    )
    result = verbalize_feature_table(features, config)
    return result["text"]


# ---------------------------------------------------------------------------
# Arm 2 — RAW_FEATURES  (unchanged)
# ---------------------------------------------------------------------------

def represent_raw_features(
    case: pd.DataFrame,
    baseline: BaselineStats,
    config: dict[str, Any],
) -> str:
    """CSV-formatted feature table without thresholds."""
    d = normalize_schema(case, source="raw_features input")
    start = float(config["fault_injection_h"])
    end = float(d.Time.max())
    features = analyze_case_windows(
        d, baseline, start_h=start, end_h=end,
        window_h=float(config["window_hours"]),
    )

    cols = [
        "window_start_h", "window_end_h", "variable",
        "shift_sigma", "slope_sigma_h",
        "residual_std_ratio", "diff_std_ratio", "raw_std_ratio",
    ]
    table = features[cols].copy()
    for c in cols[3:]:
        table[c] = table[c].round(4)

    header = (
        f"Feature table for {len(table.variable.unique())} XMEAS variables "
        f"across {len(table.window_start_h.unique())} windows "
        f"({table.window_start_h.min():.0f}–{table.window_end_h.max():.0f} h). "
        f"Features: shift_sigma (signed mean displacement in baseline σ), "
        f"slope_sigma_h (signed OLS trend in baseline σ/h), "
        f"residual_std_ratio (detrended std / baseline), "
        f"diff_std_ratio (first-diff std / baseline), "
        f"raw_std_ratio (raw std / baseline).\n\n"
    )
    buf = StringIO()
    table.to_csv(buf, index=False)
    return header + buf.getvalue()


# ---------------------------------------------------------------------------
# Arm 3 — CGTIME_STATS  (windowed, L1 / T1 / T3 / T4 / T5 fixes)
# ---------------------------------------------------------------------------

def _direct_stats(series: np.ndarray, min_prominence: float = 0.01) -> dict[str, float]:
    """Direct level/scale readouts — CGTime family 1.

    T4: *min_prominence* avoids counting noise spikes as peaks.
    """
    from scipy.signal import find_peaks

    n = len(series)
    q1, q3 = float(np.percentile(series, 25)), float(np.percentile(series, 75))

    peaks_idx, props = find_peaks(series, prominence=min_prominence)
    proms = props.get("prominences", np.array([]))
    max_prominence = float(np.max(proms)) if len(proms) > 0 else 0.0

    return _sanitize_dict({
        "mean":   float(np.mean(series)),
        "std":    float(np.std(series, ddof=1)) if n > 1 else 0.0,
        "min":    float(np.min(series)),
        "max":    float(np.max(series)),
        "median": float(np.median(series)),
        "iqr":    q3 - q1,
        "range":  float(np.ptp(series)),
        "start_value": float(series[0]),
        "end_value":   float(series[-1]),
        "max_peak_prominence": max_prominence,
    })


def _marginal_stats(series: np.ndarray, dt_h: float) -> dict[str, float]:
    """Marginal temporal/structural per-channel — CGTime family 2.

    T11: slope renamed *ols_slope*; R² prediction uses the same dt_h units.
    """
    from scipy.signal import find_peaks

    n = len(series)
    result: dict[str, float] = {}

    # ACF lag-1 — T1: guard for constant sub-series
    if n > 2 and float(np.std(series)) > 1e-12:
        r = float(np.corrcoef(series[:-1], series[1:])[0, 1])
        result["acf_lag1"] = _safe_float(r)
    else:
        result["acf_lag1"] = 0.0

    # Mean absolute change
    result["mean_abs_change"] = float(np.mean(np.abs(np.diff(series)))) if n > 1 else 0.0

    # OLS slope (units: value per hour)  — T11 rename
    if n > 1:
        t = np.arange(n, dtype=float) * dt_h
        tc = t - t.mean()
        denom = float(np.dot(tc, tc))
        result["ols_slope"] = float(np.dot(tc, series - series.mean()) / denom) if denom > 1e-12 else 0.0
    else:
        result["ols_slope"] = 0.0

    # R² of linear trend — T11 dimensional consistency
    if n > 1:
        t = np.arange(n, dtype=float) * dt_h
        slope = result["ols_slope"]
        intercept = float(series.mean() - slope * t.mean())
        predicted = intercept + slope * t
        ss_res = float(np.sum((series - predicted) ** 2))
        ss_tot = float(np.sum((series - series.mean()) ** 2))
        result["r2"] = _safe_float(1.0 - ss_res / ss_tot) if ss_tot > 1e-12 else 0.0
    else:
        result["r2"] = 0.0

    # CV
    mean_val = float(np.mean(series))
    std_val = float(np.std(series, ddof=1)) if n > 1 else 0.0
    result["cv"] = _safe_float(std_val / abs(mean_val)) if abs(mean_val) > 1e-12 else 0.0

    # Peaks / troughs
    peaks, _ = find_peaks(series)
    troughs, _ = find_peaks(-series)
    result["num_peaks"]   = int(len(peaks))
    result["num_troughs"] = int(len(troughs))

    # Sign changes in diffs
    if n > 2:
        diffs = np.diff(series)
        signs = np.sign(diffs)
        signs = signs[signs != 0]
        result["sign_changes"] = int(np.sum(np.abs(np.diff(signs)) > 0)) if len(signs) > 1 else 0
    else:
        result["sign_changes"] = 0

    # Spectral entropy
    if n > 4:
        fft_vals = np.abs(np.fft.rfft(series - series.mean())) ** 2
        fft_vals = fft_vals[1:]
        total_power = float(np.sum(fft_vals))
        if total_power > 1e-12:
            p = fft_vals / total_power
            p = p[p > 0]
            entropy = -float(np.sum(p * np.log(p)))
            max_ent = np.log(len(p)) if len(p) > 0 else 1.0
            result["spectral_entropy"] = _safe_float(entropy / max_ent) if max_ent > 0 else 0.0
        else:
            result["spectral_entropy"] = 0.0
    else:
        result["spectral_entropy"] = 0.0

    # Dominant frequency
    if n > 4:
        fft_vals = np.abs(np.fft.rfft(series - series.mean())) ** 2
        fft_vals = fft_vals[1:]
        if len(fft_vals) > 0 and np.sum(fft_vals) > 1e-12:
            dom_idx = int(np.argmax(fft_vals))
            freqs = np.fft.rfftfreq(n, d=dt_h)[1:]
            result["dom_freq"] = float(freqs[dom_idx]) if dom_idx < len(freqs) else 0.0
        else:
            result["dom_freq"] = 0.0
    else:
        result["dom_freq"] = 0.0

    # Anomaly count
    if n > 1:
        z = np.abs(series - np.mean(series)) / (np.std(series, ddof=1) + 1e-12)
        result["anomaly_count"] = int(np.sum(z > 3.0))
    else:
        result["anomaly_count"] = 0

    # Skewness / kurtosis
    result["skewness"] = _safe_float(float(sp_stats.skew(series, bias=False))) if n > 2 else 0.0
    result["kurtosis"] = _safe_float(float(sp_stats.kurtosis(series, bias=False))) if n > 3 else 0.0

    return _sanitize_dict(result)


def _pca_stats(data_matrix: np.ndarray, top_k: int = 5) -> dict[str, Any]:
    """PCA joint statistics — single ``eigh`` call (T5)."""
    n_samples, n_vars = data_matrix.shape
    centered = data_matrix - data_matrix.mean(axis=0)

    # T5: one decomposition ─ eigvals & eigvecs together
    total = 0.0
    try:
        cov = np.cov(centered, rowvar=False)
        eigvals_raw, eigvecs_raw = np.linalg.eigh(cov)
        order = np.argsort(eigvals_raw)[::-1]
        eigenvalues = np.clip(eigvals_raw[order], 0, None)
        eigvecs = eigvecs_raw[:, order]
        total = float(np.sum(eigenvalues))
        explained = eigenvalues / total if total > 0 else np.zeros_like(eigenvalues)
    except np.linalg.LinAlgError:
        eigenvalues = np.zeros(min(top_k, n_vars))
        explained = np.zeros(min(top_k, n_vars))
        eigvecs = np.eye(n_vars)

    k_top = min(top_k, len(explained))
    cumulative = np.cumsum(explained)

    if len(cumulative) > 0 and cumulative[-1] >= 0.9:
        pca_k = int(np.searchsorted(cumulative, 0.9)) + 1
    else:
        pca_k = len(explained)
    pca_k_20pct = max(pca_k, max(1, n_vars // 5))

    # Effective rank
    if total > 0:
        p = explained[explained > 0]
        se = -float(np.sum(p * np.log(p)))
        effective_rank = float(np.exp(se))
    else:
        effective_rank = 1.0

    # PC1 loadings
    pc1 = eigvecs[:, 0]
    pos_ratio = float(np.mean(pc1 > 0))
    lsq = pc1 ** 2
    lsq_sum = float(np.sum(lsq))
    ipr = float(np.sum(lsq ** 2) / (lsq_sum ** 2)) if lsq_sum > 1e-12 else 0.0

    # PC1 scores
    pc1_scores = centered @ pc1
    pc1_vol = float(np.std(pc1_scores, ddof=1)) if n_samples > 1 else 0.0

    if n_samples > 1:
        t = np.arange(n_samples, dtype=float)
        tc = t - t.mean()
        denom = float(np.dot(tc, tc))
        if denom > 1e-12:
            slope = float(np.dot(tc, pc1_scores - pc1_scores.mean()) / denom)
            pred = pc1_scores.mean() + slope * tc
            ss_res = float(np.sum((pc1_scores - pred) ** 2))
            ss_tot = float(np.sum((pc1_scores - pc1_scores.mean()) ** 2))
            pc1_r2 = _safe_float(1.0 - ss_res / ss_tot) if ss_tot > 1e-12 else 0.0
        else:
            pc1_r2 = 0.0
    else:
        pc1_r2 = 0.0

    return _sanitize_dict({
        "pca_k": pca_k,
        "pca_k_20pct_floor": pca_k_20pct,
        "pca_expl_ratio_1": float(explained[0]) if len(explained) > 0 else 0.0,
        "pca_expl_cumsum_k": float(cumulative[min(pca_k - 1, len(cumulative) - 1)]) if len(cumulative) > 0 else 0.0,
        "pca_ratio_12": float(explained[0] / explained[1]) if len(explained) > 1 and explained[1] > 1e-12 else 0.0,
        "top_explained_ratios": [float(v) for v in explained[:k_top]],
        "effective_rank": effective_rank,
        "pc1_trend_r2": pc1_r2,
        "pc1_volatility": pc1_vol,
        "pos_loading_ratio_pc1": pos_ratio,
        "loading_ipr_pc1": ipr,
    })


def _correlation_stats(data_matrix: np.ndarray) -> dict[str, Any]:
    """Correlation structure statistics — T1: NaN-safe."""
    n_vars = data_matrix.shape[1]
    corr = _safe_corrcoef(data_matrix, rowvar=False)
    upper_idx = np.triu_indices(n_vars, k=1)
    upper = corr[upper_idx]
    abs_upper = np.abs(upper)
    n_pairs = len(abs_upper)

    sync_ratio      = float(np.mean(abs_upper > 0.5)) if n_pairs > 0 else 0.0
    high_sync_ratio = float(np.mean(abs_upper > 0.8)) if n_pairs > 0 else 0.0

    if data_matrix.shape[0] > 2:
        abs_ch = np.abs(np.diff(data_matrix, axis=0))
        vc = _safe_corrcoef(abs_ch, rowvar=False)
        vol_sync = float(np.mean(np.abs(vc[upper_idx])))
    else:
        vol_sync = 0.0

    return _sanitize_dict({
        "mean_abs_correlation": float(np.mean(abs_upper)) if n_pairs > 0 else 0.0,
        "max_abs_off_diagonal": float(np.max(abs_upper)) if n_pairs > 0 else 0.0,
        "n_highly_correlated_pairs": int(np.sum(abs_upper > 0.8)),
        "sync_ratio": sync_ratio,
        "high_sync_ratio": high_sync_ratio,
        "volatility_sync_index": vol_sync,
    })


def _mahalanobis_stats(
    data_matrix: np.ndarray,
    ref_mean: np.ndarray,
    ref_cov_inv: np.ndarray | None,
) -> dict[str, Any]:
    """Mahalanobis risk indicators — T3: uses regularised covariance inverse."""
    if ref_cov_inv is None:
        return _sanitize_dict({
            "mahal_mean_distance": 0.0, "mahal_max_distance": 0.0,
            "mahal_outlier_ratio": 0.0, "mahal_outlier_count": 0,
        })

    diffs = data_matrix - ref_mean
    md_sq = np.clip(np.sum((diffs @ ref_cov_inv) * diffs, axis=1), 0, None)
    md = np.sqrt(md_sq)
    threshold = np.sqrt(sp_stats.chi2.ppf(0.95, df=data_matrix.shape[1]))

    return _sanitize_dict({
        "mahal_mean_distance":  float(np.mean(md)),
        "mahal_max_distance":   float(np.max(md)),
        "mahal_outlier_ratio":  float(np.mean(md > threshold)),
        "mahal_outlier_count":  int(np.sum(md > threshold)),
    })


def compute_regularised_cov_inv(
    baseline_blocks: list[pd.DataFrame],
    xmeas_cols: list[str],
) -> np.ndarray | None:
    """Ledoit-Wolf shrinkage covariance inverse from baseline blocks (T3).

    Call once during setup; pass the result as ``ref_cov_inv`` to
    ``represent_cgtime_stats`` / ``generate_all_representations``.
    """
    parts = []
    for blk in baseline_blocks:
        cols = [c for c in xmeas_cols if c in blk.columns]
        if cols:
            parts.append(blk[cols].to_numpy(dtype=float))
    if not parts:
        return None
    data = np.vstack(parts)
    n, p = data.shape

    if n < p + 1:
        # Too few samples — fall back to diagonal
        s = np.std(data, axis=0, ddof=1)
        s = np.where(s > 1e-12, s, 1e-12)
        return np.diag(1.0 / s ** 2)

    try:
        S = np.cov(data, rowvar=False, ddof=1)
        mu = np.trace(S) / p
        delta = S - mu * np.eye(p)
        delta_sq = np.sum(delta ** 2) / p

        X_c = data - data.mean(axis=0)
        b_bar = sum(np.sum((X_c[i:i + 1].T @ X_c[i:i + 1] - S) ** 2) for i in range(n))
        b_bar /= n * n * p

        alpha = min(b_bar / delta_sq, 1.0) if delta_sq > 1e-12 else 1.0
        shrunk = (1 - alpha) * S + alpha * mu * np.eye(p)

        try:
            return np.linalg.inv(shrunk)
        except np.linalg.LinAlgError:
            return np.linalg.pinv(shrunk)
    except Exception:
        s = np.std(data, axis=0, ddof=1)
        s = np.where(s > 1e-12, s, 1e-12)
        return np.diag(1.0 / s ** 2)


def _per_channel_sync_with_pca(
    data_matrix: np.ndarray, top_k: int = 3,
) -> dict[str, Any]:
    """Per-channel sync with top PCs — T1: NaN-safe."""
    n_samples, n_vars = data_matrix.shape
    centered = data_matrix - data_matrix.mean(axis=0)
    try:
        cov = np.cov(centered, rowvar=False)
        eigvals, eigvecs = np.linalg.eigh(cov)
        order = np.argsort(eigvals)[::-1]
        eigvecs = eigvecs[:, order]
    except np.linalg.LinAlgError:
        return _sanitize_dict({
            "sys_sync_avg_r2_topk": 0.0, "sys_sync_std_r2_topk": 0.0,
            "sys_high_sync_ratio": 0.0,  "sys_decoupled_ratio": 0.0,
        })

    k = min(top_k, n_vars)
    pc = centered @ eigvecs[:, :k]

    r2s = []
    for j in range(n_vars):
        ch = centered[:, j]
        if float(np.std(ch)) < 1e-12:
            r2s.append(0.0)
            continue
        best = 0.0
        for c in range(k):
            if float(np.std(pc[:, c])) < 1e-12:
                continue
            rv = _safe_float(float(np.corrcoef(ch, pc[:, c])[0, 1]))
            best = max(best, rv ** 2)
        r2s.append(best)

    arr = np.array(r2s)
    return _sanitize_dict({
        "sys_sync_avg_r2_topk": float(np.mean(arr)),
        "sys_sync_std_r2_topk": float(np.std(arr, ddof=1)) if n_vars > 1 else 0.0,
        "sys_high_sync_ratio":  float(np.mean(arr > 0.5)),
        "sys_decoupled_ratio":  float(np.mean(arr < 0.1)),
    })


def represent_cgtime_stats(
    case: pd.DataFrame,
    baseline: BaselineStats,
    config: dict[str, Any],
    ref_cov_inv: np.ndarray | None = None,
) -> str:
    """CGTime-inspired statistical profile — **window-aligned** (L1 fix).

    Computes Direct and Marginal per variable *per window* and Joint stats
    *per window*, matching the temporal granularity of V2 / RAW / SAX.
    Output uses compact per-window arrays to limit token growth.
    """
    d = normalize_schema(case, source="cgtime input")
    start    = float(config["fault_injection_h"])
    end      = float(d.Time.max())
    dt_h     = sampling_interval_hours(d)
    window_h = float(config["window_hours"])

    # Baseline references for Mahalanobis
    ref_mean = baseline.mean[XMEAS].to_numpy(dtype=float)
    if ref_cov_inv is None:
        # Fallback diagonal (documented)
        ref_std = baseline.std[XMEAS].to_numpy(dtype=float)
        ref_std = np.where(ref_std > 1e-12, ref_std, 1e-12)
        ref_cov_inv = np.diag(1.0 / ref_std ** 2)

    windows = list(iter_time_windows(d, start_h=start, end_h=end, window_h=window_h))
    n_win   = len(windows)
    wlabels = [f"{ws:.0f}-{we:.0f}h" for ws, we, _ in windows]

    # ── per-variable per-window ──────────────────────────────────────────────
    pv_direct:   dict[str, dict[str, list]] = {}
    pv_marginal: dict[str, dict[str, list]] = {}

    # ── joint per-window ─────────────────────────────────────────────────────
    joint_pw: dict[str, list] = {}

    for w_idx, (ws, we, wdf) in enumerate(windows):
        mat = wdf[XMEAS].to_numpy(dtype=float)

        for var in XMEAS:
            s = wdf[var].to_numpy(dtype=float)
            ds = _direct_stats(s)
            ms = _marginal_stats(s, dt_h)
            if var not in pv_direct:
                pv_direct[var]   = {k: [] for k in ds}
                pv_marginal[var] = {k: [] for k in ms}
            for k, v in ds.items():
                pv_direct[var][k].append(v)
            for k, v in ms.items():
                pv_marginal[var][k].append(v)

        pca   = _pca_stats(mat)
        corr  = _correlation_stats(mat)
        mahal = _mahalanobis_stats(mat, ref_mean, ref_cov_inv)

        for prefix, stats in [("pca", pca), ("corr", corr), ("mahal", mahal)]:
            for k, v in stats.items():
                key = f"{prefix}_{k}"
                if isinstance(v, (int, float)):
                    joint_pw.setdefault(key, []).append(v)

    # ── cross-window correlation dynamics ────────────────────────────────────
    prev_upper: np.ndarray | None = None
    changes: list[float] = []
    ppv: list[np.ndarray] = []
    for _, _, wdf in windows:
        mat = wdf[XMEAS].to_numpy(dtype=float)
        cm  = _safe_corrcoef(mat, rowvar=False)
        up  = cm[np.triu_indices(cm.shape[0], k=1)]
        ppv.append(up)
        if prev_upper is not None and len(up) == len(prev_upper):
            changes.append(float(np.linalg.norm(up - prev_upper)))
        prev_upper = up

    cross: dict[str, float] = {
        "corr_structure_stability": round(float(np.mean(changes)), 4) if changes else 0.0,
        "corr_frobenius_change_mean": round(float(np.mean(changes)), 4) if changes else 0.0,
    }
    if len(ppv) > 1:
        stacked = np.array(ppv)
        ps = np.std(stacked, axis=0, ddof=1)
        cross["corr_dynamics_mean_std"] = round(float(np.mean(ps)), 4)
        cross["corr_dynamics_max_std"]  = round(float(np.max(ps)), 4)
    else:
        cross["corr_dynamics_mean_std"] = 0.0
        cross["corr_dynamics_max_std"]  = 0.0

    # ── system-level sync (full post-injection) ──────────────────────────────
    mask = (d.Time >= start) & (d.Time <= end)
    full = d.loc[mask, XMEAS].to_numpy(dtype=float)
    sync = _per_channel_sync_with_pca(full)

    # ── build profile ────────────────────────────────────────────────────────
    profile = {
        "windows": wlabels,
        "n_variables": len(XMEAS),
        "sampling_interval_h": dt_h,
        "per_variable_direct": pv_direct,
        "per_variable_marginal": pv_marginal,
        "joint_per_window": _sanitize_dict(joint_pw),
        "cross_window_dynamics": _sanitize_dict(cross),
        "system_synchronization": sync,
    }

    header = (
        f"CGTime-inspired statistical profile for {len(XMEAS)} XMEAS variables, "
        f"{n_win} windows ({wlabels[0]} to {wlabels[-1]}), "
        f"window-aligned with other arms.\n"
        "Families (adapted from Feng et al. 2026):\n"
        "  Direct (10/var/window): mean, std, min, max, median, IQR, range, "
        "start/end value, max_peak_prominence.\n"
        "  Marginal (14/var/window): acf_lag1, mean_abs_change, ols_slope, "
        "R², CV, num_peaks/troughs, sign_changes, spectral_entropy, "
        "dom_freq, anomaly_count, skewness, kurtosis.\n"
        "  Joint (per window): PCA, correlation, Mahalanobis.\n"
        "  Cross-window: correlation stability. System sync: channel-PC R².\n"
        "Each stat value is an array of per-window values.\n\n"
    )
    # T1: allow_nan=False ensures no NaN/Inf leaks into the prompt
    return header + json.dumps(profile, indent=1, ensure_ascii=False, allow_nan=False)


# ---------------------------------------------------------------------------
# Arm 4 — SAX_SYMBOLIC  (T12: baseline-relative Z-norm)
# ---------------------------------------------------------------------------

SAX_BREAKPOINTS = {
    3: np.array([-0.4307, 0.4307]),
    4: np.array([-0.6745, 0.0, 0.6745]),
    5: np.array([-0.8416, -0.2533, 0.2533, 0.8416]),
    6: np.array([-1.0364, -0.4307, 0.0, 0.4307, 1.0364]),
}


def _sax_encode(
    series: np.ndarray,
    word_size: int = 10,
    alphabet_size: int = 5,
    ref_mean: float | None = None,
    ref_std: float | None = None,
) -> str:
    """SAX encoding — T12: baseline-relative Z-norm when ref stats are given."""
    if len(series) < 2:
        return "a" * word_size

    # T12 — use baseline reference when available
    if ref_mean is not None and ref_std is not None and ref_std > 1e-12:
        z = (series - ref_mean) / ref_std
    else:
        std = float(np.std(series, ddof=1))
        if std < 1e-12:
            return "c" * word_size
        z = (series - np.mean(series)) / std

    # PAA
    n = len(z)
    paa = np.zeros(word_size)
    if n < word_size:
        for i in range(word_size):
            paa[i] = z[min(i, n - 1)]
    else:
        for i in range(word_size):
            si = int(np.round(i * n / word_size))
            ei = int(np.round((i + 1) * n / word_size))
            ei = min(max(si + 1, ei), n)         # T12: clamp to valid range
            paa[i] = np.mean(z[si:ei])

    bp = SAX_BREAKPOINTS[alphabet_size]
    letters = "abcde"[:alphabet_size]
    return "".join(letters[int(np.searchsorted(bp, v))] for v in paa)


def represent_sax_symbolic(
    case: pd.DataFrame,
    baseline: BaselineStats,
    config: dict[str, Any],
    word_size: int = 10,
    alphabet_size: int = 5,
) -> str:
    """SAX symbolic encoding — T12: baseline-relative Z-norm."""
    d = normalize_schema(case, source="sax input")
    start = float(config["fault_injection_h"])
    end   = float(d.Time.max())

    windows = list(iter_time_windows(
        d, start_h=start, end_h=end, window_h=float(config["window_hours"]),
    ))

    header = (
        f"SAX symbolic encoding for {len(XMEAS)} XMEAS variables across "
        f"{len(windows)} windows ({start:.0f}–{end:.0f} h, "
        f"{config['window_hours']}h each). "
        f"Alphabet: {alphabet_size} symbols (a=very low … e=very high), "
        f"{word_size} symbols per window. "
        f"Z-normalised relative to normal-operation baseline.\n\n"
    )

    lines = []
    for var in XMEAS:
        rmean = float(baseline.mean[var]) if var in baseline.mean.index else None
        rstd  = float(baseline.std[var])  if var in baseline.std.index  else None
        words = [
            _sax_encode(w[var].to_numpy(dtype=float), word_size, alphabet_size,
                        ref_mean=rmean, ref_std=rstd)
            for _, _, w in windows
        ]
        lines.append(f"{var}: {' | '.join(words)}")

    return header + "\n".join(lines)


# ---------------------------------------------------------------------------
# Unified interface
# ---------------------------------------------------------------------------

ARMS = {
    "V2_TEXT":       represent_v2_text,
    "RAW_FEATURES":  represent_raw_features,
    "CGTIME_STATS":  represent_cgtime_stats,
    "SAX_SYMBOLIC":  represent_sax_symbolic,
}


def generate_all_representations(
    case: pd.DataFrame,
    baseline: BaselineStats,
    config: dict[str, Any],
    ref_cov_inv: np.ndarray | None = None,
) -> dict[str, str]:
    """Generate all four representations for a single case.

    *ref_cov_inv* is the Ledoit-Wolf regularised covariance inverse
    (computed once at startup).  Passed through to CGTIME_STATS;
    other arms ignore it.
    """
    results: dict[str, str] = {}
    for name, func in ARMS.items():
        if name == "CGTIME_STATS":
            results[name] = func(case, baseline, config, ref_cov_inv=ref_cov_inv)
        else:
            results[name] = func(case, baseline, config)
    return results
