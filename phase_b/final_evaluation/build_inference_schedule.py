#!/usr/bin/env python3
"""Build the deterministic Phase B request schedule from Amendment 001."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
AMENDMENT_PATH = ROOT / "phase_b/config/phase_b_protocol_amendment_001.json"
SCHEDULE_PATH = ROOT / "phase_b/final_evaluation/inference_schedule.json"
EXPECTED_CASES = [f"PBH-{index:03d}" for index in range(1, 16)]
EXPECTED_AGENTS = [f"agent_{index}" for index in range(1, 5)]
EXPECTED_REPETITIONS = [1, 2, 3]
EXPECTED_CONDITIONS = ["A", "B", "E"]
EXPECTED_ROTATION = [
    ["A", "B", "E"],
    ["B", "E", "A"],
    ["E", "A", "B"],
]


def load_amendment(path: Path = AMENDMENT_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_schedule(amendment: dict[str, Any]) -> list[dict[str, Any]]:
    inputs = amendment["schedule_inputs"]
    if inputs["physical_case_ids"] != EXPECTED_CASES:
        raise ValueError("case sequence differs from Amendment 001")
    if inputs["agent_ids"] != EXPECTED_AGENTS:
        raise ValueError("agent sequence differs from Amendment 001")
    if inputs["repetitions"] != EXPECTED_REPETITIONS:
        raise ValueError("repetition sequence differs from Amendment 001")
    if inputs["conditions"] != EXPECTED_CONDITIONS:
        raise ValueError("condition set differs from Amendment 001")
    if amendment["condition_rotation"] != EXPECTED_ROTATION:
        raise ValueError("condition rotation differs from Amendment 001")
    if amendment["randomized"] is not False or amendment["stateless_calls"] is not True:
        raise ValueError("schedule must be deterministic and calls must be stateless")

    entries: list[dict[str, Any]] = []
    block_index = 0
    for case_id in EXPECTED_CASES:
        for agent_id in EXPECTED_AGENTS:
            for repetition in EXPECTED_REPETITIONS:
                rotation = EXPECTED_ROTATION[block_index % 3]
                for position, condition in enumerate(rotation, start=1):
                    entries.append(
                        {
                            "sequence_index": len(entries),
                            "block_index": block_index,
                            "position_in_block": position,
                            "physical_case_id": case_id,
                            "agent_id": agent_id,
                            "repetition": repetition,
                            "condition": condition,
                        }
                    )
                block_index += 1
    if block_index != 180 or len(entries) != 540:
        raise AssertionError("Amendment 001 schedule cardinality mismatch")
    return entries


def canonical_schedule_bytes(entries: list[dict[str, Any]]) -> bytes:
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
        raise RuntimeError("inference schedule already exists; refusing overwrite")
    amendment = load_amendment()
    first = canonical_schedule_bytes(build_schedule(amendment))
    second = canonical_schedule_bytes(build_schedule(amendment))
    if first != second:
        raise RuntimeError("schedule regeneration is not byte-identical")
    SCHEDULE_PATH.write_bytes(first)
    print(
        json.dumps(
            {
                "schedule_entries": 540,
                "blocks": 180,
                "sha256": hashlib.sha256(first).hexdigest(),
                "deterministic_regeneration": "PASS",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
