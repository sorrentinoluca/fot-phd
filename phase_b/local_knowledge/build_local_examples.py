#!/usr/bin/env python3
"""Build two V2-neutral development examples per local class and agent."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "code"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from phase_b.config import load_protocol_config  # noqa: E402
from phase_b.guard import project_guard  # noqa: E402
from tep_features import normalize_schema  # noqa: E402
from tep_verbalize_v2 import (  # noqa: E402
    load_config as load_v2_config,
    load_development_baseline,
    verbalize_case,
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normal_blocks(normal_path: Path) -> dict[int, pd.DataFrame]:
    raw = pd.read_excel(normal_path, nrows=6_000)
    normal = normalize_schema(raw, source="Phase B local Normal N1-N2")
    if len(normal) != 6_000 or float(normal.Time.max()) >= 100.0:
        raise RuntimeError("Expected exactly Normal N1-N2 in the bounded read")
    blocks: dict[int, pd.DataFrame] = {}
    for block_number, left in ((1, 0.0), (2, 50.0)):
        block = normal[(normal.Time >= left) & (normal.Time < left + 50.0)].copy()
        if len(block) != 3_000:
            raise RuntimeError(f"Normal N{block_number} has {len(block)} samples")
        block["Time"] = block["Time"] - left
        blocks[block_number] = block
    return blocks


def build(
    *,
    cache_dir: Path,
    normal_path: Path,
    output_path: Path,
    metadata_path: Path,
) -> tuple[dict[str, Any], dict[str, Any]]:
    guard = project_guard(ROOT)
    cache_dir = guard.assert_allowed(cache_dir)
    normal_path = guard.assert_allowed(normal_path)
    output_path = guard.assert_allowed(output_path)
    metadata_path = guard.assert_allowed(metadata_path)

    protocol = load_protocol_config()
    mapping_path = ROOT / "phase_b" / "config" / "evaluator_side" / "pseudolabel_mapping.json"
    mapping = json.loads(mapping_path.read_text(encoding="utf-8"))["real_to_opaque"]
    reverse = {opaque: real for real, opaque in mapping.items()}
    if set(reverse) != set(protocol["label_space"][:-1]):
        raise RuntimeError("Evaluator pseudolabel mapping disagrees with protocol config")

    v2_config_path = CODE / "verbalizer_config_v2.json"
    v2_config = load_v2_config(v2_config_path)
    baseline = load_development_baseline(normal_path, v2_config)
    normal = normal_blocks(normal_path)

    # IDs are assigned once in deterministic protocol-label order. They carry
    # no real class, fault, agent, or batch token.
    example_counter = 1
    fault_examples: dict[str, list[dict[str, str]]] = {}
    source_rows: list[dict[str, Any]] = []
    for opaque_label in protocol["label_space"][:-1]:
        real_label = reverse[opaque_label]
        real_number = int(real_label[1:])
        examples: list[dict[str, str]] = []
        for batch in protocol["local_examples"]["development_batches"]:
            source = guard.assert_allowed(cache_dir / f"mode1_{real_number}_{batch}.xlsx")
            result = verbalize_case(
                pd.read_excel(source), baseline, config=v2_config, end_h=50.0
            )
            example_id = f"EXM-{example_counter:03d}"
            example_counter += 1
            examples.append(
                {
                    "example_id": example_id,
                    "pseudolabel": opaque_label,
                    "neutral_text": result["text"],
                }
            )
            source_rows.append(
                {
                    "example_id": example_id,
                    "real_class": real_label,
                    "batch": batch,
                    "source_filename": source.name,
                }
            )
        fault_examples[opaque_label] = examples

    normal_examples: list[dict[str, str]] = []
    for block_number in (1, 2):
        result = verbalize_case(
            normal[block_number], baseline, config=v2_config, start_h=10.0, end_h=50.0
        )
        example_id = f"EXM-{example_counter:03d}"
        example_counter += 1
        normal_examples.append(
            {
                "example_id": example_id,
                "pseudolabel": "Normal",
                "neutral_text": result["text"],
            }
        )
        source_rows.append(
            {
                "example_id": example_id,
                "real_class": "Normal",
                "normal_block": f"N{block_number}",
                "source_filename": normal_path.name,
            }
        )

    packs: dict[str, list[dict[str, str]]] = {}
    agent_to_pack: dict[str, str] = {}
    for pack_number, (agent_id, agent) in enumerate(protocol["agents"].items(), start=1):
        local_label = agent["local_fault_label"]
        pack_id = f"LKP-{pack_number:03d}"
        packs[pack_id] = [*fault_examples[local_label], *normal_examples]
        agent_to_pack[agent_id] = pack_id

    prompt_facing = {
        "artifact_version": "1",
        "scope": "PROMPT_FACING_DEVELOPMENT_ONLY",
        "selection_rule": "exactly batches 1 and 2; no cherry-picking",
        "examples_per_local_class": 2,
        "contains_structured_numerical_json": False,
        "v2_frozen_hashes": {
            "verbalizer_config_v2.json": sha256_file(v2_config_path),
            "tep_verbalize_v2.py": sha256_file(CODE / "tep_verbalize_v2.py"),
            "tep_features.py": sha256_file(CODE / "tep_features.py"),
        },
        "packs": packs,
    }
    evaluator_metadata = {
        "scope": "EVALUATOR_SIDE_ONLY",
        "selection_rule": {"fault_batches": [1, 2], "normal_blocks": ["N1", "N2"]},
        "agent_to_pack": agent_to_pack,
        "sources": source_rows,
    }
    output_path.write_text(
        json.dumps(prompt_facing, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    metadata_path.write_text(
        json.dumps(evaluator_metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    return prompt_facing, evaluator_metadata


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=CODE / "tep_cache")
    parser.add_argument(
        "--normal", type=Path, default=CODE / "tep_cache" / "mode1_normal_500.xlsx"
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).with_name("local_examples.json"),
    )
    parser.add_argument(
        "--metadata-output",
        type=Path,
        default=ROOT / "phase_b" / "config" / "evaluator_side" / "local_example_sources.json",
    )
    args = parser.parse_args()
    prompt_facing, _ = build(
        cache_dir=args.cache_dir,
        normal_path=args.normal,
        output_path=args.output,
        metadata_path=args.metadata_output,
    )
    count = sum(len(examples) for examples in prompt_facing["packs"].values())
    print(f"Wrote {count} agent-example assignments from 10 unique development examples.")


if __name__ == "__main__":
    main()
