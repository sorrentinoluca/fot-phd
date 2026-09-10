"""Build deterministic, pre-inference full-test assets.

Generates:
  - full_test_schedule.json              (360 entries)
  - full_test_prompt_hash_manifest.json  (120 prompts)
  - evaluator_side/full_test_targets.json
"""

from __future__ import annotations

import json
from pathlib import Path

from phase_b.c06.prompt_variant import PromptAssets, canonical_json, sha256_bytes

from .constants import (
    AGENT_IDS,
    AGENT_LOCAL_FAULT,
    ALL_CASE_IDS,
    FAULT_TO_PSEUDOLABEL,
    FULL_TEST_ROOT,
    PLANNED_AGENT_CASES,
    PLANNED_CALLS,
    REPETITIONS,
    VARIANT,
    case_fault_prefix,
    expected_label,
    stratum,
)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    # ── Schedule: 120 agent-cases × 3 reps = 360 entries ──
    schedule = []
    index = 0
    for agent_id in AGENT_IDS:
        for case_id in ALL_CASE_IDS:
            for repetition in range(1, REPETITIONS + 1):
                schedule.append(
                    {
                        "sequence_index": index,
                        "agent_id": agent_id,
                        "physical_case_id": case_id,
                        "condition": VARIANT,
                        "repetition": repetition,
                        "stratum": stratum(agent_id, case_id),
                    }
                )
                index += 1

    if len(schedule) != PLANNED_CALLS:
        raise RuntimeError(
            f"schedule has {len(schedule)} entries, expected {PLANNED_CALLS}"
        )

    write_text(
        FULL_TEST_ROOT / "full_test_schedule.json",
        json.dumps(schedule, ensure_ascii=False, indent=2) + "\n",
    )

    # ── Prompt hash manifest: 120 unique prompts ──
    assets = PromptAssets()
    prompts = []
    for agent_id in AGENT_IDS:
        for case_id in ALL_CASE_IDS:
            rendered = assets.render(agent_id, case_id)
            prompts.append(
                {
                    "agent_id": agent_id,
                    "physical_case_id": case_id,
                    "stratum": stratum(agent_id, case_id),
                    "prompt_sha256": rendered.prompt_hash,
                    "input_sha256": rendered.input_hash,
                    "prompt_character_count": rendered.character_count,
                    "available_insight_ids": list(rendered.available_insight_ids),
                }
            )

    if len(prompts) != PLANNED_AGENT_CASES:
        raise RuntimeError(
            f"manifest has {len(prompts)} prompts, expected {PLANNED_AGENT_CASES}"
        )

    prompt_manifest = {
        "variant": VARIANT,
        "scope": "full_test",
        "prompt_count": len(prompts),
        "template_sha256": sha256_bytes(
            (FULL_TEST_ROOT.parent / "prompts/B_LOCAL_FIRST_V1.txt")
            .read_text(encoding="utf-8")
            .encode("utf-8")
        ),
        "prompts": prompts,
    }
    write_text(
        FULL_TEST_ROOT / "full_test_prompt_hash_manifest.json",
        json.dumps(prompt_manifest, ensure_ascii=False, indent=2) + "\n",
    )

    # ── Evaluator-side targets ──
    # Ground truth for all 120 agent-cases, plus frozen-B baselines
    targets = {
        "scope": "EVALUATOR_SIDE_ONLY",
        "analysis_kind": "full test of B_LOCAL_FIRST_V1 across all strata",
        "expected_labels": {
            case_id: expected_label(case_id) for case_id in ALL_CASE_IDS
        },
        "agent_local_labels": {
            agent_id: FAULT_TO_PSEUDOLABEL[AGENT_LOCAL_FAULT[agent_id]]
            for agent_id in AGENT_IDS
        },
        "strata": {
            f"{agent_id}/{case_id}": stratum(agent_id, case_id)
            for agent_id in AGENT_IDS
            for case_id in ALL_CASE_IDS
        },
    }
    write_text(
        FULL_TEST_ROOT / "evaluator_side/full_test_targets.json",
        json.dumps(targets, ensure_ascii=False, indent=2) + "\n",
    )

    print(
        canonical_json(
            {
                "schedule_records": len(schedule),
                "prompts": len(prompts),
                "strata": {
                    s: sum(1 for p in prompts if p["stratum"] == s)
                    for s in ("local-seen", "local-unseen", "normal")
                },
            }
        )
    )


if __name__ == "__main__":
    main()
