"""Offline rendering of the whole final inventory (protocol §4-§5, point 6 of 7.4-FIX).

SACRIFICIAL FIXTURES ONLY: the neutral case texts here are synthetic placeholders, not
test evidence.  What is exercised is the renderer over the real 2,244 stable identifiers,
the real agent assignment and the real derangements: counts per block, the B<->E diff on
the sole ``pseudolabel``, and B-noLF as B-LF minus the policy block.
"""

from __future__ import annotations

import json
import unittest

from studio2.fase03 import protocol, protocol_bnolf
from . import final_inventory, final_prompts
from .common import HarnessError, load_json

ROOT = final_inventory.ROOT


def frozen_manifest() -> dict:
    assignment = load_json(final_inventory.ASSIGNMENT_PATH)["assignment"]
    mapping = load_json(final_inventory.PSEUDOLABEL_MAP_PATH)
    derangements = load_json(ROOT / "pseudolabel" / "CONDITION_E_DERANGEMENTS.json")["derangements"]
    labels = list(mapping["label_by_identifier"].values())
    labels = [label for label in labels if label != "Normal"] + ["Normal"]
    return {
        "label_space": labels,
        "agents": {agent: {"local_fault_label": row["local_fault_label"]}
                   for agent, row in assignment.items()},
        "local_examples": {
            agent: [
                {"example_id": f"{agent}-local", "pseudolabel": row["local_fault_label"],
                 "neutral_text": f"SYNTHETIC OFFLINE ONLY local example for {agent}"},
                {"example_id": f"{agent}-normal", "pseudolabel": "Normal",
                 "neutral_text": f"SYNTHETIC OFFLINE ONLY normal example for {agent}"},
            ]
            for agent, row in assignment.items()
        },
        "derangements": derangements,
    }


def library(tag: str) -> list[dict]:
    assignment = load_json(final_inventory.ASSIGNMENT_PATH)["assignment"]
    rows = []
    for index, (agent, row) in enumerate(sorted(assignment.items())):
        for slot in (1, 2):
            rows.append({
                "insight_id": f"S2-INS-{index * 2 + slot:03d}",
                "source_agent": agent,
                "pseudolabel": row["local_fault_label"],
                "evidence_scope": "local labeled examples",
                "observed_pattern": f"SYNTHETIC {tag} observation {index}{slot} without diagnosis",
                "variable_ids": ["XMEAS(1)", "XMEAS(7)"],
            })
    return rows


def cases(inventory) -> dict:
    return {entry["case_id"]: {
        "case_id": entry["case_id"],
        "neutral_text": f"SYNTHETIC OFFLINE ONLY neutral description for {entry['case_id']}",
    } for entry in inventory}


class FinalPromptRendering(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inventory = final_inventory.build_inventory()
        cls.rendered = final_prompts.render_all(
            inventory=cls.inventory, manifest=frozen_manifest(),
            libraries={"122B": library("G_P"), "27B": library("G_A")},
            cases=cases(cls.inventory))

    def test_every_unique_prompt_of_section_five_is_renderable(self):
        summary = self.rendered["summary"]
        self.assertEqual(summary["unique_total"], 2244)
        self.assertEqual(summary["unique_by_block"],
                         {"nucleus": 1728, "producer_swap": 224,
                          "ablation_b_no_lf": 148, "ood": 144})
        self.assertEqual(summary["requests_total"], 6732)

    def test_counts_by_condition_cover_the_four_arms(self):
        by_condition = self.rendered["summary"]["unique_by_condition"]
        self.assertEqual(set(by_condition), {"A", "B-LF", "E-LF", "B-noLF"})
        self.assertEqual(by_condition["B-noLF"], 148)
        self.assertEqual(by_condition["B-LF"], by_condition["E-LF"] + 224)

    def test_be_diff_touches_only_the_peer_insight_pseudolabels(self):
        diff = self.rendered["summary"]["be_pseudolabel_diff"]
        self.assertEqual(diff["status"], "PASS")
        self.assertEqual(diff["paired_cells"], 624)
        self.assertEqual(diff["identical_pairs"], 0)
        self.assertEqual(diff["changed_outside_peer_insights"], 0)

    def test_every_ablation_prompt_lost_the_policy_and_only_that(self):
        diff = self.rendered["summary"]["bnolf_policy_diff"]
        self.assertEqual(diff["status"], "PASS")
        self.assertEqual(diff["ablation_prompts"], 148)
        self.assertEqual(diff["still_carrying_the_policy"], 0)

    def test_an_ablation_prompt_equals_its_b_lf_twin_minus_the_policy(self):
        rows = {(row["condition"], row["case_id"], row["agent_id"], row["library_role"]): row
                for row in self.rendered["rows"]}
        checked = 0
        for key, row in rows.items():
            if key[0] != "B-noLF":
                continue
            twin = rows.get(("B-LF", key[1], key[2], key[3]))
            if twin is None:
                continue
            self.assertEqual(twin["text"].replace(protocol_bnolf.POLICY_BLOCK, "", 1),
                             row["text"])
            checked += 1
        self.assertGreater(checked, 0)

    def test_identifiers_and_prompt_bytes_are_one_to_one(self):
        rows = self.rendered["rows"]
        self.assertEqual(len({row["prompt_id"] for row in rows}), 2244)
        self.assertEqual(len({row["prompt_sha256"] for row in rows}), 2244)

    def test_rendering_is_deterministic(self):
        again = final_prompts.render_all(
            inventory=final_inventory.build_inventory(), manifest=frozen_manifest(),
            libraries={"122B": library("G_P"), "27B": library("G_A")},
            cases=cases(self.inventory))
        self.assertEqual(again["summary"]["prompts_sha256"],
                         self.rendered["summary"]["prompts_sha256"])

    def test_a_missing_case_stops_the_render(self):
        partial = dict(cases(self.inventory))
        partial.pop("test-primary-F1-r01")
        with self.assertRaisesRegex(HarnessError, "no consumer input"):
            final_prompts.render_all(
                inventory=self.inventory, manifest=frozen_manifest(),
                libraries={"122B": library("G_P"), "27B": library("G_A")}, cases=partial)

    def test_a_prompt_over_the_qualified_context_stops_the_render(self):
        with self.assertRaisesRegex(HarnessError, "exceed the qualified context"):
            final_prompts.render_all(
                inventory=self.inventory, manifest=frozen_manifest(),
                libraries={"122B": library("G_P"), "27B": library("G_A")},
                cases=cases(self.inventory),
                token_count=lambda text: len(text) // 4, context_limit=10,
                reserved_output_tokens=2)

    def test_token_budget_is_reported_when_a_counter_is_supplied(self):
        value = final_prompts.render_all(
            inventory=self.inventory, manifest=frozen_manifest(),
            libraries={"122B": library("G_P"), "27B": library("G_A")},
            cases=cases(self.inventory),
            token_count=lambda text: len(text.split()), context_limit=131072,
            reserved_output_tokens=2560)
        self.assertGreater(value["summary"]["max_prompt_tokens"], 0)
        self.assertEqual(value["summary"]["context_limit"], 131072)


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
