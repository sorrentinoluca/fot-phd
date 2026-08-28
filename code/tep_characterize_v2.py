#!/usr/bin/env python3
"""Development-only TEP characterization for the FoT verbalization layer.

Dataset snapshot: mv-per/tennessee-eastman-dataset @ 309b944f35ac440ff0c70616947ffe723c766e14

Hard guardrails:
- only fault batches 1..5 are read;
- validation batches 6..7 and test batches 8..10 are never requested;
- fault injection is fixed at 10 h because this value is derived from the
  pinned simulator snapshot (auto_run.m -> VariableTransportDelay=10 h).

The script writes threshold-free feature tables. It does not optimize or freeze
classification thresholds.
"""
from __future__ import annotations

from collections import Counter
from pathlib import Path
import urllib.request

import pandas as pd

from tep_features import (
    XMEAS,
    analyze_case_windows,
    analyze_window,
    compute_baseline_stats_from_blocks,
    load_case,
    sampling_interval_hours,
    top_variables,
)

COMMIT = "309b944f35ac440ff0c70616947ffe723c766e14"
BASE = (
    "https://media.githubusercontent.com/media/"
    f"mv-per/tennessee-eastman-dataset/{COMMIT}/simulations/mode_1/"
)
CACHE_DIR = Path("tep_cache")
OUTPUT_DIR = Path("tep_analysis_v2")

FAULTS = (1, 8, 10, 13)
DEV_BATCHES = (1, 2, 3, 4, 5)
FORBIDDEN_BATCHES = set(range(6, 11))
NORMAL_FILE = "mode1_normal_500.xlsx"
FAULT_INJECT_H = 10.0
FAULT_END_H = 50.0
WINDOW_H = 5.0
NORMAL_BLOCK_H = 50.0

METRICS = (
    "abs_shift_sigma",
    "abs_slope_sigma_h",
    "raw_std_ratio",
    "diff_std_ratio",
    "residual_std_ratio",
)


def _is_real_xlsx(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            return handle.read(4) == b"PK\x03\x04"
    except OSError:
        return False


def fetch(rel_path: str) -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    name = Path(rel_path).name
    local = CACHE_DIR / name
    if local.exists() and _is_real_xlsx(local):
        return local
    url = BASE + rel_path
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    if not data.startswith(b"PK\x03\x04"):
        raise ValueError(f"Downloaded content is not an XLSX workbook: {url}")
    temporary = local.with_suffix(local.suffix + ".tmp")
    temporary.write_bytes(data)
    temporary.replace(local)
    return local


def fault_path(fault: int, batch: int) -> Path:
    if batch in FORBIDDEN_BATCHES:
        raise RuntimeError(
            f"Refusing to read batch {batch}: validation/test batches are locked."
        )
    if batch not in DEV_BATCHES:
        raise ValueError(f"Unexpected development batch: {batch}")
    return fetch(f"faults/mode1_{fault}_{batch}.xlsx")


def normal_blocks(normal: pd.DataFrame) -> dict[int, pd.DataFrame]:
    blocks = {}
    for i in range(10):
        left = i * NORMAL_BLOCK_H
        right = (i + 1) * NORMAL_BLOCK_H
        block = normal[(normal.Time >= left) & (normal.Time < right)].copy()
        if len(block) == 0:
            raise ValueError(f"Normal block N{i+1} is empty")
        blocks[i + 1] = block
    return blocks


def audit_sampling(normal: pd.DataFrame, fault_cases: list[pd.DataFrame]) -> None:
    dt = sampling_interval_hours(normal)
    print(f"Normal sampling interval: {dt:.12f} h ({dt*60:.6f} min)")
    for i, f in enumerate(fault_cases[:3], start=1):
        dti = sampling_interval_hours(f)
        if abs(dti - dt) > 1e-12:
            raise ValueError(f"Sampling mismatch in fault case {i}: {dti} vs {dt}")


def top1_table(case_features: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for (fault, batch), g in case_features.groupby(["fault", "batch"]):
        row = {"fault": fault, "batch": batch}
        for metric in METRICS:
            idx = g[metric].idxmax()
            hit = g.loc[idx]
            row[f"{metric}_var"] = hit.variable
            row[f"{metric}_value"] = hit[metric]
            if metric == "abs_shift_sigma":
                row["shift_sigma_signed"] = hit.shift_sigma
            if metric == "abs_slope_sigma_h":
                row["slope_sigma_h_signed"] = hit.slope_sigma_h
        rows.append(row)
    return pd.DataFrame(rows)


def recurrence_table(case_features: pd.DataFrame, k: int = 5) -> pd.DataFrame:
    rows = []
    for fault, fg in case_features.groupby("fault"):
        for metric in METRICS:
            counts = Counter()
            for batch, bg in fg.groupby("batch"):
                for var in top_variables(bg, metric, k=k):
                    counts[var] += 1
            for var, n in counts.most_common():
                rows.append({"fault": fault, "metric": metric, "variable": var, "batches_in_top5": n})
    return pd.DataFrame(rows)


def normal_loo_features(blocks: dict[int, pd.DataFrame]) -> pd.DataFrame:
    rows = []
    dev_ids = set(DEV_BATCHES)
    for held in DEV_BATCHES:
        baseline_ids = sorted(dev_ids - {held})
        baseline = compute_baseline_stats_from_blocks(
            [blocks[index] for index in baseline_ids]
        )
        f = analyze_window(blocks[held], baseline)
        f.insert(0, "normal_block", held)
        rows.append(f)
    return pd.concat(rows, ignore_index=True)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    normal = load_case(fetch(NORMAL_FILE))
    blocks = normal_blocks(normal)
    baseline = compute_baseline_stats_from_blocks(
        [blocks[index] for index in DEV_BATCHES]
    )

    loaded_cases = []
    per_case = []
    per_window = []

    for fault in FAULTS:
        for batch in DEV_BATCHES:
            d = load_case(fault_path(fault, batch))
            loaded_cases.append(d)

            # Whole post-injection segment: descriptive, not interpreted as oscillation.
            post = d[(d.Time >= FAULT_INJECT_H) & (d.Time < FAULT_END_H)].copy()
            f = analyze_window(post, baseline)
            f.insert(0, "batch", batch)
            f.insert(0, "fault", fault)
            per_case.append(f)

            # Temporal windows are the primary object for distinguishing transient vs persistent behavior.
            wf = analyze_case_windows(
                d,
                baseline,
                start_h=FAULT_INJECT_H,
                end_h=FAULT_END_H,
                window_h=WINDOW_H,
            )
            wf.insert(0, "batch", batch)
            wf.insert(0, "fault", fault)
            per_window.append(wf)

    audit_sampling(normal, loaded_cases)

    case_df = pd.concat(per_case, ignore_index=True)
    window_df = pd.concat(per_window, ignore_index=True)
    normal_loo = normal_loo_features(blocks)

    case_df.to_csv(OUTPUT_DIR / "development_case_features.csv", index=False)
    window_df.to_csv(OUTPUT_DIR / "development_window_features.csv", index=False)
    normal_loo.to_csv(OUTPUT_DIR / "development_normal_loo_features.csv", index=False)

    top1 = top1_table(case_df)
    top1.to_csv(OUTPUT_DIR / "development_top1.csv", index=False)

    recurrence = recurrence_table(case_df, k=5)
    recurrence.to_csv(OUTPUT_DIR / "development_top5_recurrence.csv", index=False)

    # Compact distribution summary of per-case maxima across the five independent runs.
    maxima = []
    for (fault, batch), g in case_df.groupby(["fault", "batch"]):
        row = {"fault": fault, "batch": batch}
        for metric in METRICS:
            row[metric] = float(g[metric].max())
        maxima.append(row)
    maxima = pd.DataFrame(maxima)
    summary_rows = []
    for fault, fg in maxima.groupby("fault"):
        for metric in METRICS:
            s = fg[metric]
            summary_rows.append(
                {
                    "fault": fault,
                    "metric": metric,
                    "median": s.median(),
                    "q1": s.quantile(0.25),
                    "q3": s.quantile(0.75),
                    "min": s.min(),
                    "max": s.max(),
                }
            )
    summary = pd.DataFrame(summary_rows)
    summary.to_csv(OUTPUT_DIR / "development_maxima_summary.csv", index=False)

    print("\nDevelopment-only analysis complete.")
    print(f"Pinned dataset commit: {COMMIT}")
    print(f"Fault injection time: {FAULT_INJECT_H} h (source-derived)")
    print(f"Read fault batches: {DEV_BATCHES}; batches 6-10 are locked")
    print(f"Outputs: {OUTPUT_DIR.resolve()}")
    print("\nTop-1 per fault/batch:")
    print(top1.to_string(index=False))
    print("\nRecurring top-5 variables (>=4/5 development batches):")
    print(recurrence[recurrence.batches_in_top5 >= 4].to_string(index=False))


if __name__ == "__main__":
    main()
