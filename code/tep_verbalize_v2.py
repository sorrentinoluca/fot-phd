#!/usr/bin/env python3
"""Neutral, threshold-frozen TEP time-series verbalizer (V2).

This module converts Time + 41 XMEAS signals into quantitative temporal
signatures and an observational Italian description. It does not classify a
fault and does not contain diagnostic prototypes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

import numpy as np
import pandas as pd

from tep_features import (
    BaselineStats,
    XMEAS,
    analyze_case_windows,
    compute_baseline_stats_from_blocks,
    load_case,
    normalize_schema,
)

DEFAULT_CONFIG = Path(__file__).with_name("verbalizer_config_v2.json")


def load_config(path: str | Path = DEFAULT_CONFIG) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        config = json.load(handle)
    required = {
        "version",
        "dataset_commit",
        "sampling_minutes",
        "fault_injection_h",
        "window_hours",
        "thresholds",
        "temporal_logic",
        "vocabulary",
    }
    missing = sorted(required - set(config))
    if missing:
        raise ValueError(f"V2 config is missing keys: {missing}")
    if config["version"] != "2.0":
        raise ValueError(f"Unsupported verbalizer config: {config['version']}")
    threshold_keys = {
        "abs_shift_sigma",
        "abs_slope_sigma_h",
        "residual_std_ratio",
        "diff_std_ratio",
    }
    if set(config["thresholds"]) != threshold_keys:
        raise ValueError("Frozen V2 threshold set has changed")
    return config


def load_development_baseline(
    normal_path: str | Path,
    config: dict[str, Any] | None = None,
) -> BaselineStats:
    """Load only Normal N1-N5 and build the frozen development baseline."""
    cfg = load_config() if config is None else config
    samples_per_hour = 60 // int(cfg["sampling_minutes"])
    rows_per_block = 50 * samples_per_hour
    development_rows = 5 * rows_per_block
    raw = pd.read_excel(normal_path, nrows=development_rows)
    normal = normalize_schema(raw, source="Normal N1-N5 only")
    if len(normal) != development_rows or float(normal["Time"].max()) >= 250.0:
        raise ValueError("Expected exactly Normal N1-N5 in [0, 250 h)")
    blocks = []
    for index in range(5):
        left, right = 50.0 * index, 50.0 * (index + 1)
        block = normal[(normal.Time >= left) & (normal.Time < right)].copy()
        if len(block) != rows_per_block:
            raise ValueError(f"Normal N{index + 1} has {len(block)} samples")
        blocks.append(block)
    return compute_baseline_stats_from_blocks(blocks)


def _runs(
    active: Iterable[bool],
    starts: Iterable[float],
    ends: Iterable[float],
    signed_values: Iterable[float] | None = None,
) -> list[dict[str, Any]]:
    flags = list(map(bool, active))
    lefts, rights = list(starts), list(ends)
    signs = None
    if signed_values is not None:
        signs = [int(np.sign(value)) for value in signed_values]
    runs: list[dict[str, Any]] = []
    begin: int | None = None
    current_sign = 0
    for index in range(len(flags) + 1):
        is_active = index < len(flags) and flags[index]
        sign = signs[index] if is_active and signs is not None else 0
        continues = is_active and (
            begin is None or signs is None or sign == current_sign
        )
        if continues:
            if begin is None:
                begin = index
                current_sign = sign
            continue
        if begin is not None:
            last = index - 1
            runs.append(
                {
                    "start_h": float(lefts[begin]),
                    "end_h": float(rights[last]),
                    "n_windows": int(last - begin + 1),
                    "sign": (
                        "+" if current_sign > 0 else "-" if current_sign < 0 else None
                    ),
                }
            )
            begin = None
            current_sign = 0
        if is_active:
            begin = index
            current_sign = sign
    return runs


def _phase_masks(n_windows: int, config: dict[str, Any]) -> dict[str, np.ndarray]:
    phase = config["temporal_logic"]["phase_partition"]
    initial_n = min(int(phase["initial_windows"]), n_windows)
    late_n = min(int(phase["late_windows"]), max(0, n_windows - initial_n))
    index = np.arange(n_windows)
    return {
        "initial": index < initial_n,
        "late": index >= n_windows - late_n if late_n else np.zeros(n_windows, bool),
        "intermediate": (index >= initial_n) & (index < n_windows - late_n),
    }


def _signed_summary(
    active: np.ndarray,
    values: np.ndarray,
    starts: np.ndarray,
    ends: np.ndarray,
    late_mask: np.ndarray,
) -> dict[str, Any]:
    active_values = values[active]
    positive = int(np.sum(active_values > 0))
    negative = int(np.sum(active_values < 0))
    total = positive + negative
    runs = _runs(active, starts, ends, values)
    sign_consistency = max(positive, negative) / total if total else None
    active_indices = np.flatnonzero(active)
    strict_global = bool(
        len(active) > 0
        and np.all(active)
        and sign_consistency == 1.0
        and np.any(active & late_mask)
    )
    return {
        "n_active_windows": int(np.sum(active)),
        "active_fraction": float(np.mean(active)) if len(active) else 0.0,
        "positive_count": positive,
        "negative_count": negative,
        "sign_consistency": sign_consistency,
        "dominant_sign": (
            "+" if positive > negative else "-" if negative > positive else "mixed"
        ),
        "longest_same_sign_run": max(
            (run["n_windows"] for run in runs), default=0
        ),
        "sustained_episodes": [run for run in runs if run["n_windows"] >= 2],
        "first_active_window": (
            float(starts[active_indices[0]]) if len(active_indices) else None
        ),
        "last_active_window": (
            float(starts[active_indices[-1]]) if len(active_indices) else None
        ),
        "late_regime_active": bool(np.any(active & late_mask)),
        "late_active_fraction": (
            float(np.mean(active[late_mask])) if np.any(late_mask) else 0.0
        ),
        "strict_global_persistence": strict_global,
    }


def _unsigned_summary(
    active: np.ndarray,
    starts: np.ndarray,
    ends: np.ndarray,
    late_mask: np.ndarray,
) -> dict[str, Any]:
    runs = _runs(active, starts, ends)
    active_indices = np.flatnonzero(active)
    return {
        "n_active_windows": int(np.sum(active)),
        "active_fraction": float(np.mean(active)) if len(active) else 0.0,
        "longest_run": max((run["n_windows"] for run in runs), default=0),
        "sustained_episodes": [run for run in runs if run["n_windows"] >= 2],
        "first_active_window": (
            float(starts[active_indices[0]]) if len(active_indices) else None
        ),
        "last_active_window": (
            float(starts[active_indices[-1]]) if len(active_indices) else None
        ),
        "late_regime_active": bool(np.any(active & late_mask)),
        "late_active_fraction": (
            float(np.mean(active[late_mask])) if np.any(late_mask) else 0.0
        ),
        "strict_global_persistence": bool(
            len(active) > 0 and np.all(active) and np.any(active & late_mask)
        ),
    }


def _coherent_drift_runs(
    trend_active: np.ndarray,
    slopes: np.ndarray,
    shifts: np.ndarray,
    starts: np.ndarray,
    ends: np.ndarray,
) -> list[dict[str, Any]]:
    runs: list[dict[str, Any]] = []
    begin: int | None = None
    previous: int | None = None
    sign = 0
    for index in range(len(trend_active)):
        current_sign = int(np.sign(slopes[index]))
        continues = bool(trend_active[index])
        if begin is not None and continues:
            continues = bool(
                current_sign == sign
                and previous is not None
                and int(np.sign(shifts[index] - shifts[previous])) == sign
            )
        if not continues:
            if begin is not None and previous is not None:
                runs.append(
                    {
                        "start_h": float(starts[begin]),
                        "end_h": float(ends[previous]),
                        "n_windows": int(previous - begin + 1),
                        "sign": "+" if sign > 0 else "-",
                    }
                )
            begin = None
            previous = None
            sign = 0
        if trend_active[index]:
            if begin is None:
                begin = index
                sign = current_sign
            previous = index
    if begin is not None and previous is not None:
        runs.append(
            {
                "start_h": float(starts[begin]),
                "end_h": float(ends[previous]),
                "n_windows": int(previous - begin + 1),
                "sign": "+" if sign > 0 else "-",
            }
        )
    return [run for run in runs if run["n_windows"] >= 2]


def _median_for_mask(values: np.ndarray, mask: np.ndarray) -> float | None:
    return float(np.median(values[mask])) if np.any(mask) else None


def _variable_signature(
    group: pd.DataFrame,
    config: dict[str, Any],
    phase_masks: dict[str, np.ndarray],
) -> dict[str, Any]:
    g = group.sort_values("window_start_h")
    starts = g.window_start_h.to_numpy(float)
    ends = g.window_end_h.to_numpy(float)
    shifts = g.shift_sigma.to_numpy(float)
    slopes = g.slope_sigma_h.to_numpy(float)
    residual = g.residual_std_ratio.to_numpy(float)
    diff = g.diff_std_ratio.to_numpy(float)
    raw = g.raw_std_ratio.to_numpy(float)
    thresholds = config["thresholds"]
    level_active = np.abs(shifts) > thresholds["abs_shift_sigma"]
    trend_active = np.abs(slopes) > thresholds["abs_slope_sigma_h"]
    residual_active = residual > thresholds["residual_std_ratio"]
    diff_active = diff > thresholds["diff_std_ratio"]
    rapid_active = residual_active & diff_active
    late = phase_masks["late"]

    level = _signed_summary(level_active, shifts, starts, ends, late)
    trend = _signed_summary(trend_active, slopes, starts, ends, late)
    coherent_runs = _coherent_drift_runs(
        trend_active, slopes, shifts, starts, ends
    )
    trend["coherent_drift_episodes"] = coherent_runs
    trend["strict_global_drift"] = bool(
        trend["strict_global_persistence"]
        and len(coherent_runs) == 1
        and coherent_runs[0]["n_windows"] == len(g)
    )

    residual_summary = _unsigned_summary(residual_active, starts, ends, late)
    diff_summary = _unsigned_summary(diff_active, starts, ends, late)
    rapid_summary = _unsigned_summary(rapid_active, starts, ends, late)
    initial = phase_masks["initial"]
    intermediate = phase_masks["intermediate"]
    for summary, active in (
        (level, level_active),
        (trend, trend_active),
        (residual_summary, residual_active),
        (diff_summary, diff_active),
        (rapid_summary, rapid_active),
    ):
        summary["early_active"] = bool(np.any(active & initial))
        summary["late_active"] = bool(np.any(active & late))
        summary["initial_active_count"] = int(np.sum(active & initial))
        summary["intermediate_active_count"] = int(
            np.sum(active & intermediate)
        )
        summary["late_active_count"] = int(np.sum(active & late))
    phase_values = {
        "initial": {
            "residual_median": _median_for_mask(residual, initial),
            "diff_median": _median_for_mask(diff, initial),
            "residual_active_windows": int(np.sum(residual_active & initial)),
            "diff_active_windows": int(np.sum(diff_active & initial)),
        },
        "intermediate": {
            "residual_median": _median_for_mask(residual, intermediate),
            "diff_median": _median_for_mask(diff, intermediate),
            "residual_active_windows": int(
                np.sum(residual_active & intermediate)
            ),
            "diff_active_windows": int(np.sum(diff_active & intermediate)),
        },
        "late": {
            "residual_median": _median_for_mask(residual, late),
            "diff_median": _median_for_mask(diff, late),
            "residual_active_windows": int(np.sum(residual_active & late)),
            "diff_active_windows": int(np.sum(diff_active & late)),
        },
    }
    initial_residual = phase_values["initial"]["residual_median"]
    late_residual = phase_values["late"]["residual_median"]
    settling_transient = bool(
        np.any(residual_active & initial)
        and not np.any((residual_active | diff_active) & late)
        and initial_residual is not None
        and late_residual is not None
        and initial_residual > late_residual
    )

    per_window = []
    for row, la, ta, ra, da, qa in zip(
        g.itertuples(index=False),
        level_active,
        trend_active,
        residual_active,
        diff_active,
        rapid_active,
    ):
        per_window.append(
            {
                "start_h": float(row.window_start_h),
                "end_h": float(row.window_end_h),
                "shift_sigma": float(row.shift_sigma),
                "slope_sigma_h": float(row.slope_sigma_h),
                "residual_std_ratio": float(row.residual_std_ratio),
                "diff_std_ratio": float(row.diff_std_ratio),
                "raw_std_ratio": float(row.raw_std_ratio),
                "level_candidate": bool(la),
                "trend_candidate": bool(ta),
                "residual_candidate": bool(ra),
                "diff_candidate": bool(da),
                "rapid_candidate": bool(qa),
            }
        )
    return {
        "per_window": per_window,
        "level": level,
        "trend": trend,
        "residual_variability": residual_summary,
        "sample_to_sample_variation": diff_summary,
        "rapid_variability": rapid_summary,
        "dispersion": {
            "raw_std_ratio_median": float(np.median(raw)),
            "raw_std_ratio_max": float(np.max(raw)),
            "description": "dispersione complessiva; rapporto tra deviazioni standard",
        },
        "phase_values": phase_values,
        "settling_transient": settling_transient,
    }


def _top_names(
    variables: dict[str, dict[str, Any]],
    section: str,
    count_key: str,
    limit: int = 4,
) -> list[str]:
    metric_by_section = {
        "level": ("shift_sigma", True),
        "trend": ("slope_sigma_h", True),
        "residual_variability": ("residual_std_ratio", False),
        "sample_to_sample_variation": ("diff_std_ratio", False),
        "rapid_variability": ("residual_std_ratio", False),
    }
    metric, absolute = metric_by_section[section]

    def magnitude(name: str) -> float:
        values = [window[metric] for window in variables[name]["per_window"]]
        return max(map(abs, values)) if absolute else max(values)

    ranked = sorted(
        variables,
        key=lambda name: (
            variables[name][section][count_key],
            int(variables[name][section]["late_active"]),
            variables[name][section].get("longest_run", 0),
            variables[name][section].get("longest_same_sign_run", 0),
            magnitude(name),
        ),
        reverse=True,
    )
    return [
        name
        for name in ranked
        if variables[name][section][count_key] > 0
    ][:limit]


def _system_summary(
    variables: dict[str, dict[str, Any]],
    starts: np.ndarray,
    phase_masks: dict[str, np.ndarray],
) -> dict[str, Any]:
    activity_keys = {
        "level": ("level", "level_candidate"),
        "trend": ("trend", "trend_candidate"),
        "residual": ("residual_variability", "residual_candidate"),
        "diff": ("sample_to_sample_variation", "diff_candidate"),
        "rapid": ("rapid_variability", "rapid_candidate"),
    }
    window_activity: dict[str, Any] = {}
    for label, (_, candidate_key) in activity_keys.items():
        flags = np.array(
            [
                any(v["per_window"][index][candidate_key] for v in variables.values())
                for index in range(len(starts))
            ],
            dtype=bool,
        )
        window_activity[label] = {
            "n_active_windows": int(np.sum(flags)),
            "active_fraction": float(np.mean(flags)),
            "initial_active_windows": int(np.sum(flags & phase_masks["initial"])),
            "intermediate_active_windows": int(
                np.sum(flags & phase_masks["intermediate"])
            ),
            "late_active_windows": int(np.sum(flags & phase_masks["late"])),
            "late_regime_active": bool(np.any(flags & phase_masks["late"])),
        }
    return {
        "window_activity": window_activity,
        "strict_global_level_variables": [
            name for name, value in variables.items()
            if value["level"]["strict_global_persistence"]
        ],
        "strict_global_drift_variables": [
            name for name, value in variables.items()
            if value["trend"]["strict_global_drift"]
        ],
        "strict_global_residual_variables": [
            name for name, value in variables.items()
            if value["residual_variability"]["strict_global_persistence"]
        ],
        "strict_global_rapid_variables": [
            name for name, value in variables.items()
            if value["rapid_variability"]["strict_global_persistence"]
        ],
        "sustained_level_variables": [
            name for name, value in variables.items()
            if value["level"]["sustained_episodes"]
        ],
        "sustained_trend_variables": [
            name for name, value in variables.items()
            if value["trend"]["sustained_episodes"]
        ],
        "sustained_residual_variables": [
            name for name, value in variables.items()
            if value["residual_variability"]["sustained_episodes"]
        ],
        "sustained_rapid_variables": [
            name for name, value in variables.items()
            if value["rapid_variability"]["sustained_episodes"]
        ],
        "settling_transient_variables": [
            name for name, value in variables.items()
            if value["settling_transient"]
        ],
        "dominant_variables": {
            "level": _top_names(variables, "level", "n_active_windows"),
            "trend": _top_names(variables, "trend", "n_active_windows"),
            "residual": _top_names(
                variables, "residual_variability", "n_active_windows"
            ),
            "diff": _top_names(
                variables, "sample_to_sample_variation", "n_active_windows"
            ),
            "rapid": _top_names(
                variables, "rapid_variability", "n_active_windows"
            ),
        },
    }


def _join(names: list[str], limit: int = 3) -> str:
    chosen = names[:limit]
    if not chosen:
        return "nessuna variabile"
    if len(chosen) == 1:
        return chosen[0]
    return ", ".join(chosen[:-1]) + " e " + chosen[-1]


def _signed_fact(
    name: str,
    label: str,
    summary: dict[str, Any],
    n_windows: int,
) -> str:
    active = summary["n_active_windows"]
    if active == 0:
        return f"{name} non supera la soglia di {label} in alcuna finestra."
    if summary["positive_count"] == active:
        signs = "sempre con segno positivo"
    elif summary["negative_count"] == active:
        signs = "sempre con segno negativo"
    else:
        signs = (
            f"con segno positivo in {summary['positive_count']} e negativo in "
            f"{summary['negative_count']}"
        )
    run_length = summary["longest_same_sign_run"]
    run_unit = "finestra" if run_length == 1 else "finestre"
    return (
        f"{name} supera la soglia di {label} in {active}/{n_windows} finestre, "
        f"{signs}; il run più lungo con segno coerente comprende "
        f"{run_length} {run_unit}, dalla prima attivazione "
        f"a {summary['first_active_window']:.1f} h all'ultima a "
        f"{summary['last_active_window']:.1f} h."
    )


def _unsigned_fact(
    name: str,
    label: str,
    summary: dict[str, Any],
    n_windows: int,
    initial_windows: int,
    late_windows: int,
) -> str:
    return (
        f"{name}: {label} sopra soglia in "
        f"{summary['n_active_windows']}/{n_windows} finestre; "
        f"{summary['initial_active_count']}/{initial_windows} nella fase iniziale "
        f"e {summary['late_active_count']}/{late_windows} nelle ultime finestre."
    )


def render_text(structured: dict[str, Any]) -> str:
    """Render numerical evidence without adding a diagnostic interpretation."""
    variables = structured["variables"]
    system = structured["system_summary"]
    n = structured["n_windows"]
    start, end = structured["time_range_h"]
    initial_n = structured["phase_window_counts"]["initial"]
    late_n = structured["phase_window_counts"]["late"]
    sentences = [
        f"Intervallo osservato {start:.1f}–{end:.1f} h in {n} finestre da "
        f"{structured['window_hours']:.1f} h."
    ]

    level_names = system["dominant_variables"]["level"]
    if level_names:
        sentences.append(
            _signed_fact(
                level_names[0], "spostamento", variables[level_names[0]]["level"], n
            )
        )
    else:
        sentences.append("Nessuna XMEAS supera la soglia di spostamento.")

    trend_names = system["dominant_variables"]["trend"]
    if trend_names:
        sentences.append(
            _signed_fact(
                trend_names[0], "pendenza", variables[trend_names[0]]["trend"], n
            )
        )
    else:
        sentences.append("Nessuna XMEAS supera la soglia di pendenza.")

    residual_names = system["dominant_variables"]["residual"]
    if residual_names:
        sentences.append(
            _unsigned_fact(
                residual_names[0],
                "variabilità residua dopo rimozione del trend lineare",
                variables[residual_names[0]]["residual_variability"],
                n,
                initial_n,
                late_n,
            )
        )
    else:
        sentences.append("Nessuna XMEAS supera la soglia di variabilità residua.")

    diff_names = system["dominant_variables"]["diff"]
    if diff_names:
        sentences.append(
            _unsigned_fact(
                diff_names[0],
                "variazioni campione-campione",
                variables[diff_names[0]]["sample_to_sample_variation"],
                n,
                initial_n,
                late_n,
            )
        )
    else:
        sentences.append(
            "Nessuna XMEAS supera la soglia delle variazioni campione-campione."
        )

    rapid_names = system["dominant_variables"]["rapid"]
    if rapid_names:
        lead = rapid_names[0]
        info = variables[lead]["rapid_variability"]
        sentences.append(
            f"Su {lead}, residual e diff superano simultaneamente le rispettive "
            f"soglie in {info['n_active_windows']}/{n} finestre, incluse "
            f"{info['late_active_count']}/{late_n} finestre finali."
        )

    dispersion = max(
        variables,
        key=lambda name: variables[name]["dispersion"]["raw_std_ratio_max"],
    )
    value = variables[dispersion]["dispersion"]["raw_std_ratio_max"]
    sentences.append(
        f"La massima dispersione complessiva osservata è su {dispersion} "
        f"(rapporto tra deviazioni standard {value:.2f})."
    )
    return " ".join(sentences)


def verbalize_feature_table(
    features: pd.DataFrame,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cfg = load_config() if config is None else config
    required = {
        "window_start_h", "window_end_h", "variable", "shift_sigma",
        "slope_sigma_h", "raw_std_ratio", "diff_std_ratio",
        "residual_std_ratio",
    }
    missing = sorted(required - set(features.columns))
    if missing:
        raise ValueError(f"Feature table missing columns: {missing}")
    starts = np.sort(features.window_start_h.unique().astype(float))
    if len(starts) < 1:
        raise ValueError("At least one window is required")
    if set(features.variable.unique()) != set(XMEAS):
        raise ValueError("Feature table must contain all 41 XMEAS")
    expected_rows = len(starts) * len(XMEAS)
    if len(features) != expected_rows:
        raise ValueError(f"Expected {expected_rows} rows, got {len(features)}")
    ends = (
        features[["window_start_h", "window_end_h"]]
        .drop_duplicates()
        .sort_values("window_start_h")
        .window_end_h.to_numpy(float)
    )
    phase_masks = _phase_masks(len(starts), cfg)
    variables = {
        name: _variable_signature(
            features[features.variable == name], cfg, phase_masks
        )
        for name in XMEAS
    }
    structured = {
        "verbalizer_version": cfg["version"],
        "dataset_commit": cfg["dataset_commit"],
        "time_range_h": [float(starts[0]), float(ends[-1])],
        "window_hours": float(cfg["window_hours"]),
        "n_windows": len(starts),
        "phase_definition": {
            "initial": [
                float(starts[phase_masks["initial"]][0]),
                float(ends[phase_masks["initial"]][-1]),
            ] if np.any(phase_masks["initial"]) else None,
            "intermediate": [
                float(starts[phase_masks["intermediate"]][0]),
                float(ends[phase_masks["intermediate"]][-1]),
            ] if np.any(phase_masks["intermediate"]) else None,
            "late": [
                float(starts[phase_masks["late"]][0]),
                float(ends[phase_masks["late"]][-1]),
            ] if np.any(phase_masks["late"]) else None,
        },
        "phase_window_counts": {
            name: int(np.sum(mask)) for name, mask in phase_masks.items()
        },
        "thresholds": dict(cfg["thresholds"]),
        "variables": variables,
    }
    structured["system_summary"] = _system_summary(
        variables, starts, phase_masks
    )
    return {"structured": structured, "text": render_text(structured)}


def verbalize_case(
    case: pd.DataFrame,
    baseline: BaselineStats,
    *,
    config: dict[str, Any] | None = None,
    start_h: float | None = None,
    end_h: float | None = None,
) -> dict[str, Any]:
    cfg = load_config() if config is None else config
    d = normalize_schema(case, source="verbalizer input")
    start = float(cfg["fault_injection_h"] if start_h is None else start_h)
    end = float(d.Time.max() if end_h is None else end_h)
    features = analyze_case_windows(
        d,
        baseline,
        start_h=start,
        end_h=end,
        window_h=float(cfg["window_hours"]),
    )
    return verbalize_feature_table(features, cfg)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", help="XLSX/CSV containing Time + 41 XMEAS")
    parser.add_argument(
        "--normal",
        required=True,
        help="mode1_normal_500.xlsx; only N1-N5 are loaded",
    )
    parser.add_argument("--config", default=str(DEFAULT_CONFIG))
    parser.add_argument("--json-output", help="optional structured JSON path")
    args = parser.parse_args()
    config = load_config(args.config)
    baseline = load_development_baseline(args.normal, config)
    result = verbalize_case(load_case(args.case), baseline, config=config)
    if args.json_output:
        with Path(args.json_output).open("w", encoding="utf-8") as handle:
            json.dump(result["structured"], handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    print(result["text"])


if __name__ == "__main__":
    main()
