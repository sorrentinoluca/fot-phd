from __future__ import annotations

import json
import unittest

from phase_b.c06.constants import (
    C06_ROOT,
    LOCAL_FIRST_BLOCK,
    LOCAL_CASES,
    ROOT,
)
from phase_b.c06.prompt_variant import PromptAssets, insert_local_first


class C06ScreeningTests(unittest.TestCase):
    def test_variant_is_only_one_insertion(self) -> None:
        base = (C06_ROOT.parent / "prompts/fot_B.txt").read_text(encoding="utf-8")
        variant = (C06_ROOT / "prompts/B_LOCAL_FIRST_V1.txt").read_text(encoding="utf-8")
        self.assertEqual(variant, insert_local_first(base))
        self.assertEqual(variant.count(LOCAL_FIRST_BLOCK), 1)
        reconstructed = (
            C06_ROOT / "prompts/B_FROZEN_RECONSTRUCTED.txt"
        ).read_text(encoding="utf-8")
        self.assertEqual(reconstructed, base)

    def test_instruction_has_no_target_or_answer_leakage(self) -> None:
        lowered = LOCAL_FIRST_BLOCK.lower()
        forbidden = (
            "exp3v2",
            "f8",
            "f13",
            "cls-",
            "ins00",
            "local-seen",
            "original error",
            "ground truth",
        )
        for token in forbidden:
            self.assertNotIn(token, lowered)

    def test_schedule_is_exactly_24_times_three(self) -> None:
        schedule = json.loads((C06_ROOT / "screening_schedule.json").read_text())
        self.assertEqual(len(schedule), 72)
        keys = {(item["agent_id"], item["physical_case_id"]) for item in schedule}
        self.assertEqual(len(keys), 24)
        for agent_id, case_ids in LOCAL_CASES.items():
            for case_id in case_ids:
                repetitions = sorted(
                    item["repetition"]
                    for item in schedule
                    if item["agent_id"] == agent_id
                    and item["physical_case_id"] == case_id
                )
                self.assertEqual(repetitions, [1, 2, 3])

    def test_all_rendered_prompts_are_clean_and_frozen(self) -> None:
        assets = PromptAssets()
        manifest = json.loads((C06_ROOT / "prompt_hash_manifest.json").read_text())
        frozen = {
            (item["agent_id"], item["physical_case_id"]): item
            for item in manifest["prompts"]
        }
        for agent_id, case_ids in LOCAL_CASES.items():
            for case_id in case_ids:
                rendered = assets.render(agent_id, case_id)
                self.assertEqual(
                    rendered.prompt_hash,
                    frozen[(agent_id, case_id)]["prompt_sha256"],
                )

    def test_prompt_and_runner_do_not_read_evaluator_side(self) -> None:
        for relative in ("prompt_variant.py", "run_screening.py"):
            source = (C06_ROOT / relative).read_text(encoding="utf-8").lower()
            self.assertNotIn("evaluator_side", source)
            self.assertNotIn("screening_targets", source)

    def test_original_frozen_sources_are_untouched(self) -> None:
        self.assertTrue((ROOT / "phase_b/prompts/fot_B.txt").is_file())


if __name__ == "__main__":
    unittest.main()
