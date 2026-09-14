#!/usr/bin/env python3
"""Fail-closed preflight for the normal_dev campaign."""

from __future__ import annotations

import argparse
import csv
import subprocess
from pathlib import Path

try:
    from .build_normal_dev_plan import validate_plan
except ImportError:  # Direct script execution.
    from build_normal_dev_plan import validate_plan


PLAN_REVISION = "a572d1c"
RESERVED_RANGES = (
    range(0, 10), range(100, 110), range(200, 210), range(1000, 1010),
    range(2000, 2100), range(10000, 10350), range(20000, 20150),
    range(30000, 30040), range(40000, 40350), range(49900, 49902),
    range(50000, 50150),
)


def plan_revision_is_published(repo_root: Path) -> bool:
    result = subprocess.run(
        ["git", "merge-base", "--is-ancestor", PLAN_REVISION, "refs/remotes/origin/main"],
        cwd=repo_root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def validate_no_collisions(
    rows: list[dict[str, str]],
    repo_root: Path,
    *,
    excluded_manifests: set[Path] | None = None,
) -> None:
    target = {int(row["stream_id"]) for row in rows}
    if target != set(range(60000, 60040)):
        raise ValueError("normal_dev must reserve exactly streams 60000-60039")
    occupied = set().union(*(set(values) for values in RESERVED_RANGES)) | {999999}
    collision = sorted(target & occupied)
    if collision:
        raise ValueError(f"reserved stream collision: {collision}")
    excluded = {path.resolve() for path in (excluded_manifests or set())}
    for path in repo_root.glob("studio2/**/*.csv"):
        # A stream identifier is reserved by an execution plan or by a produced
        # generation manifest.  Derived evaluator indexes repeat provenance
        # identifiers and must not be mistaken for a second allocation.
        if path.parent.name != "plans" and path.name != "generation_manifest.csv":
            continue
        if path.name == "normal_dev.csv":
            continue
        if path.resolve() in excluded:
            continue
        try:
            with path.open(newline="", encoding="utf-8-sig") as handle:
                reader = csv.DictReader(handle)
                if "stream_id" not in (reader.fieldnames or ()):
                    continue
                seen = {int(row["stream_id"]) for row in reader if row.get("stream_id")}
        except (OSError, UnicodeError, ValueError, csv.Error):
            continue
        overlap = sorted(target & seen)
        if overlap:
            raise ValueError(f"stream collision with {path}: {overlap}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plan", type=Path)
    parser.add_argument("destination", type=Path)
    parser.add_argument("--allow-unpublished-plan-for-test", action="store_true")
    args = parser.parse_args()
    here = Path(__file__).resolve().parent
    repo_root = here.parents[2]
    rows = validate_plan(args.plan.resolve())
    validate_no_collisions(rows, repo_root)
    if args.destination.exists():
        raise SystemExit(f"refusing existing destination: {args.destination}")
    try:
        args.destination.resolve().relative_to(here / "runs")
    except ValueError as exc:
        raise SystemExit("destination must remain below baseline_numerica/runs") from exc
    if not args.allow_unpublished_plan_for_test and not plan_revision_is_published(repo_root):
        raise SystemExit(
            "batch NON lanciabile: origin/main does not contain plan revision 7 a572d1c"
        )
    print(f"preflight accepted rows={len(rows)} streams=60000-60039")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
