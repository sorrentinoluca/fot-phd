#!/usr/bin/env python3
"""Build and verify the immutable normal_dev generation plan."""

from __future__ import annotations

import argparse
import csv
import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
FIELDS = (
    "run_id", "set_name", "agent_id", "agent_run_index", "run_index_uint64",
    "stream_id", "seed_namespace", "seed_descriptor", "stream_lo32",
    "stream_hi32", "burn_in_h", "stop_time_h", "window_position",
    "development_start_h", "development_end_h", "window_h",
    "useful_windows_expected", "use",
)
NAMESPACE = "fot-tep/fase03/normal_dev/v1"
KEY = "0x464f545445503032"


def build_rows() -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for agent_index in range(1, 9):
        for local_index in range(1, 6):
            stream = 60000 + 5 * (agent_index - 1) + local_index - 1
            rows.append({
                "run_id": f"normal-dev-agent-{agent_index}-r{local_index:02d}",
                "set_name": "normal_dev",
                "agent_id": f"agent_{agent_index}",
                "agent_run_index": local_index,
                "run_index_uint64": stream,
                "stream_id": stream,
                "seed_namespace": NAMESPACE,
                "seed_descriptor": f"{KEY}:{stream:016x}",
                "stream_lo32": stream & 0xFFFFFFFF,
                "stream_hi32": stream >> 32,
                "burn_in_h": 20,
                "stop_time_h": 65,
                "window_position": 0,
                "development_start_h": 25,
                "development_end_h": 65,
                "window_h": 5,
                "useful_windows_expected": 8,
                "use": "development_only",
            })
    return rows


def validate_plan(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if tuple(reader.fieldnames or ()) != FIELDS:
            raise ValueError("normal_dev columns differ from the frozen specification")
        actual = list(reader)
    expected = [{key: str(value) for key, value in row.items()} for row in build_rows()]
    if actual != expected:
        raise ValueError("normal_dev rows or ordering differ from the frozen specification")
    return actual


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    if output.parent != HERE / "plans":
        parser.error("plan must be written directly under baseline_numerica/plans")
    if output.exists():
        parser.error(f"refusing to overwrite {output}")
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(build_rows())
    rows = validate_plan(output)
    print(f"rows={len(rows)} sha256={hashlib.sha256(output.read_bytes()).hexdigest()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
