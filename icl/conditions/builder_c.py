"""Deterministic prompt builder for Condition C (centralized pooled ICL)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from phase_b.prompts.leakage import scan_text


ROOT = Path(__file__).resolve().parents[2]

# C uses the same template as A/B/E — byte-identical copy.
TEMPLATE_C = ROOT / "icl" / "prompts" / "pooled_C.txt"
TEMPLATES_ABE = {
    "A": ROOT / "phase_b" / "prompts" / "isolated_A.txt",
    "B": ROOT / "phase_b" / "prompts" / "fot_B.txt",
    "E": ROOT / "phase_b" / "prompts" / "corrupted_E.txt",
}

POOLED_EXAMPLES = ROOT / "icl" / "pooled_libraries" / "pooled_examples.json"
POOLED_INSIGHTS = ROOT / "icl" / "pooled_libraries" / "pooled_insights.json"

LABEL_SPACE = ["CLS-ZOGAA", "CLS-OJNSG", "CLS-R463B", "CLS-Z3ISU", "Normal"]
FAULT_LABELS = set(LABEL_SPACE[:-1])
ALL_INSIGHT_IDS = tuple(f"INS-{i:03d}" for i in range(1, 9))


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class RenderedPromptC:
    """Immutable rendered prompt for Condition C."""

    __slots__ = (
        "agent_id", "condition", "text", "prompt_hash", "input_hash",
        "available_insight_ids", "character_count",
    )

    def __init__(
        self,
        *,
        text: str,
        input_hash: str,
        available_insight_ids: tuple[str, ...],
    ) -> None:
        self.agent_id = "central"
        self.condition = "C"
        self.text = text
        self.prompt_hash = _sha256(text)
        self.input_hash = input_hash
        self.available_insight_ids = available_insight_ids
        self.character_count = len(text)


def _validate_pooled_examples(examples: list[dict[str, Any]]) -> None:
    """Validate exactly 10 examples: 2 per fault label + 2 Normal."""
    if len(examples) != 10:
        raise ValueError(f"pooled examples must contain exactly 10 records, got {len(examples)}")
    required_keys = {"example_id", "pseudolabel", "neutral_text"}
    for ex in examples:
        if set(ex) != required_keys:
            raise ValueError(
                f"each example must have exactly {sorted(required_keys)}, "
                f"got {sorted(ex)}"
            )
        if not isinstance(ex["neutral_text"], str) or not ex["neutral_text"].strip():
            raise ValueError("neutral_text must be a non-empty string")
    from collections import Counter
    counts = Counter(ex["pseudolabel"] for ex in examples)
    expected = {label: 2 for label in LABEL_SPACE}
    if counts != expected:
        raise ValueError(f"expected 2 examples per label, got {dict(counts)}")


def _validate_pooled_insights(insights: list[dict[str, Any]]) -> None:
    """Validate exactly 8 insights with IDs INS-001..INS-008."""
    if len(insights) != 8:
        raise ValueError(f"pooled insights must contain exactly 8 records, got {len(insights)}")
    ids = tuple(ins["insight_id"] for ins in insights)
    if ids != ALL_INSIGHT_IDS:
        raise ValueError(f"insight IDs must be {ALL_INSIGHT_IDS}, got {ids}")


def _insight_block(insights: list[dict[str, Any]]) -> str:
    """Format insights identically to phase_b builders._insight_block."""
    if not insights:
        return ""
    return "PEER INSIGHTS\n" + json.dumps(insights, ensure_ascii=False, indent=2) + "\n\n"


def _verify_template_identity() -> str:
    """Load pooled_C.txt and verify it is byte-identical to A/B/E templates."""
    template_c = TEMPLATE_C.read_text(encoding="utf-8")
    for name, path in TEMPLATES_ABE.items():
        other = path.read_text(encoding="utf-8")
        if other != template_c:
            raise RuntimeError(
                f"pooled_C.txt diverges from {name} template ({path})"
            )
    return template_c


def load_pooled_examples() -> list[dict[str, Any]]:
    """Load and validate the 10 pooled examples."""
    examples = json.loads(POOLED_EXAMPLES.read_text(encoding="utf-8"))
    _validate_pooled_examples(examples)
    return examples


def load_pooled_insights() -> list[dict[str, Any]]:
    """Load and validate the 8 pooled insights."""
    insights = json.loads(POOLED_INSIGHTS.read_text(encoding="utf-8"))
    _validate_pooled_insights(insights)
    return insights


def render_condition_c_prompt(
    *,
    case_text: str,
    examples: list[dict[str, Any]] | None = None,
    insights: list[dict[str, Any]] | None = None,
    label_space: list[str] | None = None,
) -> RenderedPromptC:
    """Render a complete Condition C diagnostic prompt.

    The prompt is receiver-independent: identical for any case_text,
    regardless of which "agent" invokes it.
    """
    if not isinstance(case_text, str) or not case_text.strip():
        raise ValueError("case_text must be frozen V2 neutral text")

    template = _verify_template_identity()

    if examples is None:
        examples = load_pooled_examples()
    else:
        _validate_pooled_examples(examples)

    if insights is None:
        insights = load_pooled_insights()
    else:
        _validate_pooled_insights(insights)

    if label_space is None:
        label_space = LABEL_SPACE

    rendered = (
        template
        .replace("<<LABEL_SPACE>>", json.dumps(label_space, ensure_ascii=False))
        .replace("<<LOCAL_EXAMPLES>>", json.dumps(examples, ensure_ascii=False, indent=2))
        .replace("<<PEER_INSIGHTS_BLOCK>>", _insight_block(insights))
        .replace("<<CASE_TEXT>>", case_text.strip())
    )

    # Verify no unrendered placeholders remain.
    placeholders = ("<<LABEL_SPACE>>", "<<LOCAL_EXAMPLES>>",
                    "<<PEER_INSIGHTS_BLOCK>>", "<<CASE_TEXT>>")
    leftovers = [ph for ph in placeholders if ph in rendered]
    if leftovers:
        raise RuntimeError(f"unrendered prompt placeholders: {leftovers}")

    # Anti-leakage scan.
    findings = scan_text(rendered, source="rendered:central:C")
    if findings:
        raise ValueError(f"prompt leakage: {findings[0]}")

    return RenderedPromptC(
        text=rendered,
        input_hash=_sha256(case_text.strip()),
        available_insight_ids=ALL_INSIGHT_IDS,
    )
