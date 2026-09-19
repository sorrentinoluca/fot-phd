#!/usr/bin/env python3
"""Rebuild, from the development runs only, the per-window feature tables E5-C2 needs.

Development data only: the 40 runs of ``fault_runs/MANIFEST_FAULT_DEV.csv``. The test lot
is never opened here. Geometry and pipeline are the frozen ones of 03.6
(``ONSET_H = 25``, ``END_H = 65``, ``window = 5 h``, eight complete post-onset windows per
run), computed with ``code/tep_features.analyze_case_windows`` over the legacy Normal
baseline, exactly as ``evidence/extract_evidence.py`` does. Nothing is written inside the
repository: the cache lives wherever ``--output`` points, by default outside it.

No model call, no network, no write to any frozen artifact.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
for candidate in (REPO_ROOT, REPO_ROOT / "code"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

import pandas as pd  # noqa: E402

import tep_verbalize_v2 as verbalizer  # noqa: E402
from tep_features import analyze_case_windows, load_case  # noqa: E402

ONSET_H = 25.0
END_H = 65.0
WINDOW_H = 5.0
EXPECTED_WINDOWS_PER_RUN = 8

DEV_MANIFEST = REPO_ROOT / "studio2/fase03/fault_runs/MANIFEST_FAULT_DEV.csv"
NORMAL_WORKBOOK = REPO_ROOT / "code/tep_cache/mode1_normal_500.xlsx"


def sha256_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def read_dev_manifest(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = [row for row in csv.DictReader(handle)]
    complete = []
    for row in rows:
        if row.get("status") != "complete":
            continue
        if int(row.get("useful_windows_complete", "-1")) != EXPECTED_WINDOWS_PER_RUN:
            continue
        complete.append(row)
    if not complete:
        raise SystemExit("no complete development run in the manifest")
    return complete


def resolve_source(row: dict[str, str], runs_root: Path | None) -> Path:
    recorded = Path(row["output_path"])
    candidates = [recorded]
    if runs_root is not None:
        candidates.append(runs_root / recorded.name)
    candidates.append(REPO_ROOT / "studio2/fase03/fault_runs/runs/fault_dev_001" / recorded.name)
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"run CSV not found for {row['run_id']}: tried {candidates}")


def build(output: Path, *, runs_root: Path | None, limit: int | None) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    config = verbalizer.load_config()
    baseline = verbalizer.load_development_baseline(NORMAL_WORKBOOK, config)
    rows = read_dev_manifest(DEV_MANIFEST)
    if limit:
        rows = rows[:limit]
    index = []
    for row in rows:
        run_id = row["run_id"]
        target = output / f"{run_id}.features.csv"
        if not target.is_file():
            source = resolve_source(row, runs_root)
            observed = sha256_file(source)
            if observed != row["output_sha256"]:
                raise SystemExit(f"{run_id}: run CSV hash mismatch ({observed})")
            features = analyze_case_windows(
                load_case(source), baseline,
                start_h=ONSET_H, end_h=END_H, window_h=WINDOW_H)
            starts = sorted(float(v) for v in features.window_start_h.unique())
            if len(starts) != EXPECTED_WINDOWS_PER_RUN:
                raise SystemExit(f"{run_id}: {len(starts)} windows, expected eight")
            features.to_csv(target, index=False, lineterminator="\n")
        index.append({
            "run_id": run_id,
            "idv": int(row["idv"]),
            "fault": f"F{int(row['idv'])}",
            "stream_id": row["stream_id"],
            "features_path": str(target),
            "features_sha256": sha256_file(target),
        })
    summary = {
        "artifact_version": "E5_DEV_UNITS_1",
        "scope": "development runs only; test lot never opened",
        "onset_h": ONSET_H, "end_h": END_H, "window_h": WINDOW_H,
        "windows_per_run": EXPECTED_WINDOWS_PER_RUN,
        "run_count": len(index),
        "verbalizer_config_version": config["version"],
        "normal_workbook_sha256": sha256_file(NORMAL_WORKBOOK),
        "runs": index,
    }
    (output / "DEV_UNITS_INDEX.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True,
                        help="cache directory for the per-run feature tables (outside the repo)")
    parser.add_argument("--runs-root", type=Path, default=None)
    parser.add_argument("--limit", type=int, default=None)
    arguments = parser.parse_args(argv)
    summary = build(arguments.output, runs_root=arguments.runs_root, limit=arguments.limit)
    print(json.dumps({key: value for key, value in summary.items() if key != "runs"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
