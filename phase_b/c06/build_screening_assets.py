"""Build deterministic, pre-inference C06 screening artifacts."""

from __future__ import annotations

import difflib
import json
from pathlib import Path

from .constants import (
    C06_ROOT,
    FROZEN_WORKTREE_HASHES,
    HARNESS_COMMIT,
    LOCAL_CASES,
    REPETITIONS,
    ROOT,
    VARIANT,
)
from .prompt_variant import (
    PromptAssets,
    canonical_json,
    git_show,
    insert_local_first,
    sha256_bytes,
)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    base = (ROOT / "phase_b/prompts/fot_B.txt").read_text(encoding="utf-8")
    tagged_base = git_show(HARNESS_COMMIT, "phase_b/prompts/fot_B.txt")
    if sha256_bytes(tagged_base) != FROZEN_WORKTREE_HASHES["phase_b/prompts/fot_B.txt"]:
        raise RuntimeError("frozen B prompt does not match the harness tag")
    if tagged_base.decode("utf-8") != base:
        raise RuntimeError("worktree B prompt differs from the frozen harness")
    write_text(C06_ROOT / "prompts/B_FROZEN_RECONSTRUCTED.txt", base)
    variant = insert_local_first(base)
    write_text(C06_ROOT / "prompts/B_LOCAL_FIRST_V1.txt", variant)
    diff = "".join(
        difflib.unified_diff(
            base.splitlines(keepends=True),
            variant.splitlines(keepends=True),
            fromfile="a/phase_b/prompts/fot_B.txt",
            tofile="b/phase_b/c06/prompts/B_LOCAL_FIRST_V1.txt",
        )
    )
    write_text(C06_ROOT / "prompts/B_LOCAL_FIRST_V1.diff", diff)

    schedule = []
    index = 0
    for agent_id, case_ids in LOCAL_CASES.items():
        for case_id in case_ids:
            for repetition in range(1, REPETITIONS + 1):
                schedule.append(
                    {
                        "sequence_index": index,
                        "agent_id": agent_id,
                        "physical_case_id": case_id,
                        "condition": VARIANT,
                        "repetition": repetition,
                    }
                )
                index += 1
    write_text(
        C06_ROOT / "screening_schedule.json",
        json.dumps(schedule, ensure_ascii=False, indent=2) + "\n",
    )

    assets = PromptAssets()
    prompts = []
    for agent_id, case_ids in LOCAL_CASES.items():
        for case_id in case_ids:
            rendered = assets.render(agent_id, case_id)
            prompts.append(
                {
                    "agent_id": agent_id,
                    "physical_case_id": case_id,
                    "prompt_sha256": rendered.prompt_hash,
                    "input_sha256": rendered.input_hash,
                    "prompt_character_count": rendered.character_count,
                    "available_insight_ids": list(rendered.available_insight_ids),
                }
            )
    prompt_manifest = {
        "variant": VARIANT,
        "prompt_count": len(prompts),
        "template_sha256": sha256_bytes(variant.encode("utf-8")),
        "prompts": prompts,
    }
    write_text(
        C06_ROOT / "prompt_hash_manifest.json",
        json.dumps(prompt_manifest, ensure_ascii=False, indent=2) + "\n",
    )
    print(canonical_json({"schedule_records": len(schedule), "prompts": len(prompts)}))


if __name__ == "__main__":
    main()
