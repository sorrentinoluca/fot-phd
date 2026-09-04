#!/usr/bin/env python3
"""Create the deterministic EXP3_V2 inference schedule without RNG."""

from __future__ import annotations

from collections import Counter
import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
DEFAULT_CONTRACT = HERE / "exp3v2_inference_schedule_contract_001.json"
DEFAULT_OUTPUT = HERE / "exp3v2_inference_schedule_001.json"
EXPECTED_CASES = [
    *(f"EXP3V2-N-{index:03d}" for index in range(1, 7)),
    *(f"EXP3V2-F1-{index:03d}" for index in range(1, 7)),
    *(f"EXP3V2-F8-{index:03d}" for index in range(1, 7)),
    *(f"EXP3V2-F10-{index:03d}" for index in range(1, 7)),
    *(f"EXP3V2-F13-{index:03d}" for index in range(1, 7)),
]
EXPECTED_AGENTS = [f"agent_{index}" for index in range(1, 5)]
EXPECTED_REPETITIONS = [1, 2, 3]
EXPECTED_CONDITIONS = ["A", "B", "E"]
EXPECTED_ROTATION = [
    ["A", "B", "E"],
    ["B", "E", "A"],
    ["E", "A", "B"],
]


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def load_contract(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("schedule contract must be a JSON object")
    return value


def build_schedule(contract: dict[str, Any]) -> list[dict[str, Any]]:
    if contract.get("physical_case_ids") != EXPECTED_CASES:
        raise ValueError("case order differs from the canonical EXP3_V2 order")
    if contract.get("agent_ids") != EXPECTED_AGENTS:
        raise ValueError("agent order must be agent_1 through agent_4")
    if contract.get("repetitions") != EXPECTED_REPETITIONS:
        raise ValueError("repetitions must be 1, 2, 3")
    if contract.get("conditions") != EXPECTED_CONDITIONS:
        raise ValueError("conditions must be exactly A, B, E")
    if contract.get("condition_rotation") != EXPECTED_ROTATION:
        raise ValueError("condition rotation differs from the frozen rule")
    if (
        contract.get("randomized") is not False
        or contract.get("schedule_seed") is not None
    ):
        raise ValueError("the EXP3_V2 schedule must use no RNG and no seed")
    if contract.get("stateless_calls") is not True:
        raise ValueError("all scheduled calls must be stateless")

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

    validate_schedule(entries)
    return entries


def validate_schedule(entries: list[dict[str, Any]]) -> None:
    if len(entries) != 1080:
        raise ValueError("schedule must contain exactly 1,080 jobs")
    if [item.get("sequence_index") for item in entries] != list(range(1080)):
        raise ValueError("sequence_index must be exactly 0 through 1,079")
    if {item.get("block_index") for item in entries} != set(range(360)):
        raise ValueError("block_index must be exactly 0 through 359")
    keys = [
        (
            item.get("physical_case_id"),
            item.get("agent_id"),
            item.get("condition"),
            item.get("repetition"),
        )
        for item in entries
    ]
    if len(set(keys)) != 1080:
        raise ValueError("schedule contains duplicate experimental jobs")
    if Counter(item["condition"] for item in entries) != Counter(
        {"A": 360, "B": 360, "E": 360}
    ):
        raise ValueError("condition counts are not exactly balanced")
    positions = Counter(
        (item["condition"], item["position_in_block"]) for item in entries
    )
    expected_positions = Counter(
        {
            (condition, position): 120
            for condition in EXPECTED_CONDITIONS
            for position in (1, 2, 3)
        }
    )
    if positions != expected_positions:
        raise ValueError("condition positions are not exactly balanced")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--contract", type=Path, default=DEFAULT_CONTRACT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args(argv)
    if args.output.exists():
        raise RuntimeError(f"refusing to overwrite schedule: {args.output}")
    contract = load_contract(args.contract)
    first = canonical_json_bytes(build_schedule(contract))
    second = canonical_json_bytes(build_schedule(contract))
    if first != second:
        raise RuntimeError("schedule construction was not byte-identical")
    args.output.write_bytes(first)
    print(
        json.dumps(
            {
                "blocks": 360,
                "jobs": 1080,
                "condition_counts": {"A": 360, "B": 360, "E": 360},
                "condition_position_counts": 120,
                "sha256": hashlib.sha256(first).hexdigest(),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
