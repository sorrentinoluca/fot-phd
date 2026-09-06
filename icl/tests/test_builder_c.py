"""Unit tests for the Condition C prompt builder."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from icl.conditions.builder_c import (
    ALL_INSIGHT_IDS,
    LABEL_SPACE,
    RenderedPromptC,
    load_pooled_examples,
    load_pooled_insights,
    render_condition_c_prompt,
)


ROOT = Path(__file__).resolve().parents[2]
SAMPLE_CASE_TEXT = "Intervallo osservato 10.0-50.0 h in 8 finestre da 5.0 h. Nessuna XMEAS supera la soglia di spostamento."


class TestPooledExamples(unittest.TestCase):
    def test_count_and_labels(self) -> None:
        examples = load_pooled_examples()
        self.assertEqual(len(examples), 10)
        labels = {ex["pseudolabel"] for ex in examples}
        self.assertEqual(labels, set(LABEL_SPACE))
        from collections import Counter
        counts = Counter(ex["pseudolabel"] for ex in examples)
        for label in LABEL_SPACE:
            self.assertEqual(counts[label], 2, f"{label} count mismatch")

    def test_keys_are_minimal(self) -> None:
        for ex in load_pooled_examples():
            self.assertEqual(set(ex), {"example_id", "pseudolabel", "neutral_text"})

    def test_ordered_by_example_id(self) -> None:
        examples = load_pooled_examples()
        ids = [ex["example_id"] for ex in examples]
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(ids, [f"EXM-{i:03d}" for i in range(1, 11)])


class TestPooledInsights(unittest.TestCase):
    def test_count_and_ids(self) -> None:
        insights = load_pooled_insights()
        self.assertEqual(len(insights), 8)
        ids = tuple(ins["insight_id"] for ins in insights)
        self.assertEqual(ids, ALL_INSIGHT_IDS)


class TestRenderConditionCPrompt(unittest.TestCase):
    def setUp(self) -> None:
        self.examples = load_pooled_examples()
        self.insights = load_pooled_insights()

    def test_basic_render(self) -> None:
        result = render_condition_c_prompt(
            case_text=SAMPLE_CASE_TEXT,
            examples=self.examples,
            insights=self.insights,
        )
        self.assertIsInstance(result, RenderedPromptC)
        self.assertEqual(result.agent_id, "central")
        self.assertEqual(result.condition, "C")
        self.assertGreater(result.character_count, 0)

    def test_all_examples_in_prompt(self) -> None:
        result = render_condition_c_prompt(
            case_text=SAMPLE_CASE_TEXT,
            examples=self.examples,
            insights=self.insights,
        )
        for ex in self.examples:
            self.assertIn(ex["example_id"], result.text)
        for label in LABEL_SPACE:
            self.assertIn(label, result.text)

    def test_all_insights_in_prompt(self) -> None:
        result = render_condition_c_prompt(
            case_text=SAMPLE_CASE_TEXT,
            examples=self.examples,
            insights=self.insights,
        )
        for ins_id in ALL_INSIGHT_IDS:
            self.assertIn(ins_id, result.text)

    def test_no_unrendered_placeholders(self) -> None:
        result = render_condition_c_prompt(
            case_text=SAMPLE_CASE_TEXT,
            examples=self.examples,
            insights=self.insights,
        )
        for placeholder in ("<<LABEL_SPACE>>", "<<LOCAL_EXAMPLES>>",
                            "<<PEER_INSIGHTS_BLOCK>>", "<<CASE_TEXT>>"):
            self.assertNotIn(placeholder, result.text)

    def test_case_text_in_prompt(self) -> None:
        result = render_condition_c_prompt(
            case_text=SAMPLE_CASE_TEXT,
            examples=self.examples,
            insights=self.insights,
        )
        self.assertIn(SAMPLE_CASE_TEXT.strip(), result.text)

    def test_prompt_hash_deterministic(self) -> None:
        r1 = render_condition_c_prompt(
            case_text=SAMPLE_CASE_TEXT,
            examples=self.examples,
            insights=self.insights,
        )
        r2 = render_condition_c_prompt(
            case_text=SAMPLE_CASE_TEXT,
            examples=self.examples,
            insights=self.insights,
        )
        self.assertEqual(r1.prompt_hash, r2.prompt_hash)
        self.assertEqual(r1.text, r2.text)

    def test_receiver_independence(self) -> None:
        """The prompt is identical regardless of which 'agent' invokes it."""
        r1 = render_condition_c_prompt(
            case_text=SAMPLE_CASE_TEXT,
            examples=self.examples,
            insights=self.insights,
        )
        r2 = render_condition_c_prompt(
            case_text=SAMPLE_CASE_TEXT,
            examples=self.examples,
            insights=self.insights,
        )
        self.assertEqual(r1.text, r2.text)
        self.assertEqual(r1.prompt_hash, r2.prompt_hash)

    def test_available_insight_ids(self) -> None:
        result = render_condition_c_prompt(
            case_text=SAMPLE_CASE_TEXT,
            examples=self.examples,
            insights=self.insights,
        )
        self.assertEqual(result.available_insight_ids, ALL_INSIGHT_IDS)

    def test_empty_case_text_rejected(self) -> None:
        with self.assertRaises(ValueError):
            render_condition_c_prompt(
                case_text="",
                examples=self.examples,
                insights=self.insights,
            )

    def test_wrong_example_count_rejected(self) -> None:
        with self.assertRaises(ValueError):
            render_condition_c_prompt(
                case_text=SAMPLE_CASE_TEXT,
                examples=self.examples[:4],
                insights=self.insights,
            )

    def test_wrong_insight_count_rejected(self) -> None:
        with self.assertRaises(ValueError):
            render_condition_c_prompt(
                case_text=SAMPLE_CASE_TEXT,
                examples=self.examples,
                insights=self.insights[:6],
            )

    def test_no_leakage(self) -> None:
        """Leakage scanner should not trigger on a valid C prompt."""
        result = render_condition_c_prompt(
            case_text=SAMPLE_CASE_TEXT,
            examples=self.examples,
            insights=self.insights,
        )
        from phase_b.prompts.leakage import scan_text
        findings = scan_text(result.text, source="test")
        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
