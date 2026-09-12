#!/usr/bin/env python3
"""Build a guarded, deterministic Normal-run plan from the frozen specification."""

from __future__ import annotations

import argparse
import csv
import json
import random
from pathlib import Path


FIELDS = (
    "run_id",
    "set_name",
    "stream_id",
    "legacy_seed",
    "stop_time_h",
    "burn_in_h",
    "window_position",
)
STREAM_RANGES = {
    "burnin_qual": range(0, 10),
    "prefix_qual": range(100, 110),
    "philox_legacy_qual": range(200, 210),
    "legacy_generator_qual": range(200, 210),
    "pilot": range(1000, 1010),
    "baseline_fit_new": range(2000, 2100),
    "cal_thr": range(10000, 10350),
    "far_ver": range(20000, 20150),
}


def build_rows(set_name: str, burn_in_h: int, full_length: bool) -> list[dict[str, int | str]]:
    streams = STREAM_RANGES[set_name]
    position_rng = random.Random(0x464F5454 + streams.start)
    rows = []
    if set_name == "prefix_qual":
        for ordinal, stream_id in enumerate(streams, start=1):
            common = {
                "set_name": set_name,
                "stream_id": stream_id,
                "legacy_seed": "",
                "burn_in_h": burn_in_h,
            }
            rows.append(
                {
                    **common,
                    "run_id": f"prefix_qual-{ordinal:03d}-full",
                    "stop_time_h": burn_in_h + 50,
                    "window_position": 0,
                }
            )
            for position in range(1, 11):
                rows.append(
                    {
                        **common,
                        "run_id": f"prefix_qual-{ordinal:03d}-j{position:02d}",
                        "stop_time_h": burn_in_h + 5 * position,
                        "window_position": position,
                    }
                )
        return rows
    for ordinal, stream_id in enumerate(streams, start=1):
        if set_name == "burnin_qual":
            stop_time_h = 70
            position = 0
        elif set_name in {
            "pilot",
            "baseline_fit_new",
            "far_ver",
            "philox_legacy_qual",
            "legacy_generator_qual",
        }:
            stop_time_h = burn_in_h + 50
            position = position_rng.randint(1, 10) if set_name == "far_ver" else 0
        elif set_name == "cal_thr":
            position = position_rng.randint(1, 10)
            stop_time_h = burn_in_h + (50 if full_length else 5 * position)
        else:
            raise ValueError(f"unsupported set: {set_name}")
        rows.append(
            {
                "run_id": f"{set_name}-{ordinal:03d}",
                "set_name": set_name,
                "stream_id": stream_id,
                "legacy_seed": (
                    1431655765 + ordinal
                    if set_name == "legacy_generator_qual"
                    else ""
                ),
                "stop_time_h": stop_time_h,
                "burn_in_h": burn_in_h,
                "window_position": position,
            }
        )
    return rows


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("set_name", choices=tuple(STREAM_RANGES))
    parser.add_argument("output", type=Path)
    parser.add_argument("--burn-in-hours", type=int, required=True)
    parser.add_argument("--full-length", action="store_true")
    args = parser.parse_args()
    if args.burn_in_hours < 0:
        parser.error("--burn-in-hours must be non-negative")

    repo_root = Path(__file__).resolve().parents[2]
    output = args.output.resolve()
    try:
        output.relative_to(repo_root / "studio2")
    except ValueError:
        parser.error("output must remain below studio2/")
    if output.exists():
        parser.error(f"refusing to overwrite {output}")

    spec = json.loads((Path(__file__).with_name("generation_spec.json")).read_text())
    if spec["ts_base_hours"] != 0.0005:
        parser.error("unexpected Ts_base in generation_spec.json")
    rows = build_rows(args.set_name, args.burn_in_hours, args.full_length)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"OK: {len(rows)} rows written to {output.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
