from __future__ import annotations

from dataclasses import asdict
import json
import unittest
from pathlib import Path

from phase_b.conditions import render_diagnostic_prompt, render_insight_prompt
from phase_b.insights import (
    build_fixed_derangements,
    corrupt_peer_insights,
    peer_only_insights,
    validate_global_insights,
)
from phase_b.prompts.leakage import assert_no_leakage, scan_text
from phase_b.tests.helpers import fixture_insights, load_config, load_local_examples


ROOT = Path(__file__).resolve().parents[2]


class InsightsAndConditionsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = load_config()
        cls.insights = fixture_insights(cls.config)
        cls.examples = load_local_examples()["agents"]
        cls.derangements = build_fixed_derangements(cls.config)

    def test_exactly_two_insights_per_fault_and_opaque_ids(self) -> None:
        validated = validate_global_insights(self.insights, self.config)
        for label in self.config["label_space"][:-1]:
            self.assertEqual(sum(item.pseudolabel == label for item in validated), 2)
        for insight in validated:
            self.assertRegex(insight.insight_id, r"^INS-[0-9]{3}$")
            self.assertNotIn(insight.pseudolabel, insight.insight_id)
            self.assertNotIn(insight.source_agent, insight.insight_id)

    def test_peer_only_filter_has_six_no_self_no_normal(self) -> None:
        for agent_id in self.config["agents"]:
            peer = peer_only_insights(self.insights, agent_id, self.config)
            self.assertEqual(len(peer), 6)
            self.assertFalse(any(item.source_agent == agent_id for item in peer))
            self.assertFalse(any(item.pseudolabel == "Normal" for item in peer))

    def test_fixed_derangement_has_no_fixed_points(self) -> None:
        frozen = json.loads(
            (ROOT / "phase_b/config/evaluator_side/condition_e_derangements.json").read_text()
        )["derangements"]
        self.assertEqual(self.derangements, frozen)
        for mapping in frozen.values():
            self.assertEqual(set(mapping), set(mapping.values()))
            self.assertTrue(all(source != target for source, target in mapping.items()))

    def test_e_preserves_order_text_and_all_fields_except_label(self) -> None:
        for agent_id in self.config["agents"]:
            peer = peer_only_insights(self.insights, agent_id, self.config)
            corrupted = corrupt_peer_insights(
                peer, agent_id=agent_id, derangements=self.derangements
            )
            self.assertEqual(len(peer), len(corrupted))
            self.assertEqual([item.insight_id for item in peer], [item.insight_id for item in corrupted])
            for before, after in zip(peer, corrupted):
                changes = {
                    key
                    for key in asdict(before)
                    if asdict(before)[key] != asdict(after)[key]
                }
                self.assertEqual(changes, {"pseudolabel"})

    def test_condition_rendering_and_leakage(self) -> None:
        case_text = "Intervallo osservato in otto finestre; nessuna conclusione diagnostica."
        for agent_id in self.config["agents"]:
            prompts = {
                condition: render_diagnostic_prompt(
                    agent_id=agent_id,
                    condition=condition,
                    case_text=case_text,
                    local_examples=self.examples[agent_id],
                    config=self.config,
                    global_insights=None if condition == "A" else self.insights,
                    derangements=self.derangements if condition == "E" else None,
                )
                for condition in ("A", "B", "E")
            }
            self.assertEqual(prompts["A"].available_insight_ids, ())
            self.assertEqual(len(prompts["B"].available_insight_ids), 6)
            self.assertEqual(prompts["B"].available_insight_ids, prompts["E"].available_insight_ids)
            self.assertNotIn("PEER INSIGHTS", prompts["A"].text)
            self.assertIn("PEER INSIGHTS", prompts["B"].text)
            self.assertEqual(prompts["B"].character_count, prompts["E"].character_count)
            self.assertEqual(scan_text(prompts["A"].text), [])
            self.assertEqual(scan_text(prompts["B"].text), [])
            self.assertEqual(scan_text(prompts["E"].text), [])

    def test_insight_prompt_requests_exactly_two_fixed_ids(self) -> None:
        for agent_id in self.config["agents"]:
            prompt = render_insight_prompt(
                agent_id=agent_id,
                local_examples=self.examples[agent_id],
                config=self.config,
            )
            self.assertEqual(len(prompt.available_insight_ids), 2)
            self.assertEqual(scan_text(prompt.text), [])

    def test_all_prompt_facing_artifacts_are_leak_free(self) -> None:
        assert_no_leakage(
            [
                ROOT / "phase_b/prompts",
                ROOT / "phase_b/local_knowledge",
                ROOT / "phase_b/insights",
            ]
        )


if __name__ == "__main__":
    unittest.main()
