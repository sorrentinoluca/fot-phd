"""Build the deterministic Condition C request schedule.

Input:
  - phase_b held-out manifest (15 cases, class_offline for pilot selection)
  - pseudolabel mapping (validates fault class coverage)

Output:
  - c_schedule.json — 45 request-level entries, pilot-tagged.

The pseudolabel mapping is used internally for pilot selection only;
no class or pseudolabel information appears in the output (opacity
toward the runner is maintained).
"""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = ROOT / "phase_b" / "heldout" / "phase_b_heldout_manifest.csv"
MAPPING_PATH = ROOT / "phase_b" / "config" / "evaluator_side" / "pseudolabel_mapping.json"
SCHEDULE_PATH = ROOT / "icl" / "full_evaluation" / "c_schedule.json"

EXPECTED_CASE_IDS = tuple(f"PBH-{i:03d}" for i in range(1, 16))
EXPECTED_REPETITIONS = (1, 2, 3)
EXPECTED_CLASS_COUNT = 5  # 4 fault classes + Normal


def load_manifest(path: Path = MANIFEST_PATH) -> list[dict[str, str]]:
    """Load and validate the held-out manifest CSV (15 rows)."""
    with path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    case_ids = tuple(r["case_id"] for r in rows)
    if case_ids != EXPECTED_CASE_IDS:
        raise ValueError(f"manifest case_ids differ from expected: {case_ids}")
    return rows


def load_pseudolabel_mapping(path: Path = MAPPING_PATH) -> dict[str, str]:
    """Load the fault→pseudolabel mapping for internal pilot selection."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    mapping = raw.get("real_to_opaque", raw)
    if not isinstance(mapping, dict) or len(mapping) != 4:
        raise ValueError("pseudolabel mapping must contain exactly 4 fault→pseudolabel entries")
    return mapping


def _select_pilot_cases(
    manifest_rows: list[dict[str, str]],
    mapping: dict[str, str],
) -> frozenset[str]:
    """Select one pilot case per class (first case_id per class, sorted).

    Uses class_offline from the manifest and validates against the
    pseudolabel mapping.  The pseudolabel itself is NOT propagated
    to the schedule output.
    """
    class_to_cases: dict[str, list[str]] = {}
    for row in manifest_rows:
        cls = row["class_offline"]
        class_to_cases.setdefault(cls, []).append(row["case_id"])

    if len(class_to_cases) != EXPECTED_CLASS_COUNT:
        raise ValueError(
            f"expected {EXPECTED_CLASS_COUNT} classes, "
            f"got {len(class_to_cases)}: {sorted(class_to_cases)}"
        )

    # Validate that fault classes match the pseudolabel mapping keys.
    fault_classes = sorted(cls for cls in class_to_cases if cls != "Normal")
    if fault_classes != sorted(mapping):
        raise ValueError(
            f"fault classes {fault_classes} don't match "
            f"pseudolabel mapping keys {sorted(mapping)}"
        )

    # Pick first case per class (case_ids are already sorted in manifest).
    pilot_cases: set[str] = set()
    for cls in class_to_cases:
        cases = sorted(class_to_cases[cls])
        pilot_cases.add(cases[0])

    if len(pilot_cases) != EXPECTED_CLASS_COUNT:
        raise ValueError(
            f"expected {EXPECTED_CLASS_COUNT} pilot cases, got {len(pilot_cases)}"
        )

    return frozenset(pilot_cases)


def build_schedule(
    manifest_rows: list[dict[str, str]] | None = None,
    mapping: dict[str, str] | None = None,
) -> list[dict[str, Any]]:
    """Build the 45-entry request-level C schedule.

    Ordering: ``(pilot DESC, physical_case_id ASC, repetition ASC)``.
    Pilot entries occupy sequence_index 0..14, non-pilot 15..44.
    """
    if manifest_rows is None:
        manifest_rows = load_manifest()
    if mapping is None:
        mapping = load_pseudolabel_mapping()

    # Validate case_ids even when rows are supplied externally.
    case_ids = tuple(r["case_id"] for r in manifest_rows)
    if case_ids != EXPECTED_CASE_IDS:
        raise ValueError(f"case_ids differ from expected: {case_ids}")

    pilot_cases = _select_pilot_cases(manifest_rows, mapping)
    pilot_ids = sorted(c for c in case_ids if c in pilot_cases)
    non_pilot_ids = sorted(c for c in case_ids if c not in pilot_cases)

    entries: list[dict[str, Any]] = []

    # Pilot first (pilot DESC: True before False).
    for case_id in pilot_ids:
        for rep in EXPECTED_REPETITIONS:
            entries.append({
                "sequence_index": len(entries),
                "physical_case_id": case_id,
                "repetition": rep,
                "condition": "C",
                "receiver_id": "central",
                "pilot": True,
            })

    # Then non-pilot.
    for case_id in non_pilot_ids:
        for rep in EXPECTED_REPETITIONS:
            entries.append({
                "sequence_index": len(entries),
                "physical_case_id": case_id,
                "repetition": rep,
                "condition": "C",
                "receiver_id": "central",
                "pilot": False,
            })

    if len(entries) != 45:
        raise AssertionError(f"expected 45 schedule entries, got {len(entries)}")

    return entries


def canonical_schedule_bytes(entries: list[dict[str, Any]]) -> bytes:
    """Deterministic JSON serialization for hash comparison."""
    return (
        json.dumps(
            entries,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def main() -> int:
    if SCHEDULE_PATH.exists():
        raise RuntimeError("C schedule already exists; refusing overwrite")
    first = canonical_schedule_bytes(build_schedule())
    second = canonical_schedule_bytes(build_schedule())
    if first != second:
        raise RuntimeError("schedule regeneration is not byte-identical")
    SCHEDULE_PATH.parent.mkdir(parents=True, exist_ok=True)
    SCHEDULE_PATH.write_bytes(first)
    print(
        json.dumps(
            {
                "schedule_entries": 45,
                "pilot_entries": 15,
                "non_pilot_entries": 30,
                "sha256": hashlib.sha256(first).hexdigest(),
                "deterministic_regeneration": "PASS",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
