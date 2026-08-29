"""Deterministic prompt builders; no provider calls or inference live here."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable

from phase_b.insights import Insight, corrupt_peer_insights, peer_only_insights
from phase_b.prompts.leakage import scan_text


ROOT = Path(__file__).resolve().parents[2]
PROMPTS = ROOT / "phase_b" / "prompts"
TEMPLATE_BY_CONDITION = {
    "A": PROMPTS / "isolated_A.txt",
    "B": PROMPTS / "fot_B.txt",
    "E": PROMPTS / "corrupted_E.txt",
}


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class RenderedPrompt:
    agent_id: str
    condition: str
    text: str
    prompt_hash: str
    input_hash: str
    available_insight_ids: tuple[str, ...]
    character_count: int


def _validate_local_examples(
    agent_id: str, examples: Iterable[dict[str, Any]], config: dict[str, Any]
) -> list[dict[str, str]]:
    items = list(examples)
    if len(items) != 4:
        raise ValueError(f"{agent_id} requires four examples: two local and two Normal")
    required = {"example_id", "pseudolabel", "neutral_text"}
    if any(set(item) != required for item in items):
        raise ValueError("prompt-facing examples must contain only ID, pseudolabel, neutral_text")
    local_label = config["agents"][agent_id]["local_fault_label"]
    counts = {
        label: sum(item["pseudolabel"] == label for item in items)
        for label in (local_label, "Normal")
    }
    if counts != {local_label: 2, "Normal": 2}:
        raise ValueError(f"invalid local-example counts for {agent_id}: {counts}")
    if any(item["pseudolabel"] not in {local_label, "Normal"} for item in items):
        raise ValueError("locally unseen pseudolabel leaked into local examples")
    if any(not isinstance(item["neutral_text"], str) or not item["neutral_text"].strip() for item in items):
        raise ValueError("neutral_text must be a non-empty string")
    return items


def _insight_block(insights: list[Insight]) -> str:
    if not insights:
        return ""
    payload = [item.to_dict() for item in insights]
    return "PEER INSIGHTS\n" + json.dumps(payload, ensure_ascii=False, indent=2) + "\n\n"


def _load_equivalent_template(condition: str) -> str:
    if condition not in TEMPLATE_BY_CONDITION:
        raise ValueError(f"unknown condition: {condition}")
    contents = {
        name: path.read_text(encoding="utf-8") for name, path in TEMPLATE_BY_CONDITION.items()
    }
    if len(set(contents.values())) != 1:
        raise RuntimeError("A/B/E diagnostic templates diverged outside peer insights")
    return contents[condition]


def render_diagnostic_prompt(
    *,
    agent_id: str,
    condition: str,
    case_text: str,
    local_examples: Iterable[dict[str, Any]],
    config: dict[str, Any],
    global_insights: Iterable[Insight | dict[str, Any]] | None = None,
    derangements: dict[str, dict[str, str]] | None = None,
) -> RenderedPrompt:
    if agent_id not in config["agents"]:
        raise ValueError(f"unknown agent: {agent_id}")
    if not isinstance(case_text, str) or not case_text.strip():
        raise ValueError("case_text must be frozen V2 neutral text")
    examples = _validate_local_examples(agent_id, local_examples, config)

    peer: list[Insight] = []
    if condition == "A":
        if global_insights not in (None, [], ()):
            raise ValueError("condition A must not receive an insight library")
    elif condition in {"B", "E"}:
        if global_insights is None:
            raise ValueError(f"condition {condition} requires the global local-insight library")
        peer = peer_only_insights(global_insights, agent_id, config)
        if condition == "E":
            if derangements is None:
                raise ValueError("condition E requires frozen evaluator-side derangements")
            peer = corrupt_peer_insights(peer, agent_id=agent_id, derangements=derangements)
    else:
        raise ValueError(f"unknown condition: {condition}")

    template = _load_equivalent_template(condition)
    rendered = (
        template.replace("<<LABEL_SPACE>>", json.dumps(config["label_space"], ensure_ascii=False))
        .replace("<<LOCAL_EXAMPLES>>", json.dumps(examples, ensure_ascii=False, indent=2))
        .replace("<<PEER_INSIGHTS_BLOCK>>", _insight_block(peer))
        .replace("<<CASE_TEXT>>", case_text.strip())
    )
    leftovers = [token for token in ("<<LABEL_SPACE>>", "<<LOCAL_EXAMPLES>>", "<<PEER_INSIGHTS_BLOCK>>", "<<CASE_TEXT>>") if token in rendered]
    if leftovers:
        raise RuntimeError(f"unrendered prompt placeholders: {leftovers}")
    findings = scan_text(rendered, source=f"rendered:{agent_id}:{condition}")
    if findings:
        raise ValueError(f"prompt leakage: {findings[0]}")
    return RenderedPrompt(
        agent_id=agent_id,
        condition=condition,
        text=rendered,
        prompt_hash=sha256_text(rendered),
        input_hash=sha256_text(case_text.strip()),
        available_insight_ids=tuple(item.insight_id for item in peer),
        character_count=len(rendered),
    )


def render_insight_prompt(
    *,
    agent_id: str,
    local_examples: Iterable[dict[str, Any]],
    config: dict[str, Any],
) -> RenderedPrompt:
    examples = _validate_local_examples(agent_id, local_examples, config)
    agent_number = int(agent_id.split("_")[1])
    ids = [f"INS-{2 * agent_number - 1:03d}", f"INS-{2 * agent_number:03d}"]
    local_label = config["agents"][agent_id]["local_fault_label"]
    evidence_scope = "two labeled local development examples plus two local Normal references"
    template = (PROMPTS / "insight_generation.txt").read_text(encoding="utf-8")
    rendered = (
        template.replace("<<LOCAL_LABEL>>", local_label)
        .replace("<<LOCAL_EXAMPLES>>", json.dumps(examples, ensure_ascii=False, indent=2))
        .replace("<<SOURCE_AGENT>>", agent_id)
        .replace("<<EVIDENCE_SCOPE>>", evidence_scope)
        .replace("<<INSIGHT_IDS>>", json.dumps(ids))
    )
    if "<<" in rendered or ">>" in rendered:
        raise RuntimeError("unrendered insight prompt placeholder")
    findings = scan_text(rendered, source=f"insight:{agent_id}")
    if findings:
        raise ValueError(f"insight prompt leakage: {findings[0]}")
    return RenderedPrompt(
        agent_id=agent_id,
        condition="INSIGHT_GENERATION",
        text=rendered,
        prompt_hash=sha256_text(rendered),
        input_hash=sha256_text(json.dumps(examples, ensure_ascii=False, sort_keys=True)),
        available_insight_ids=tuple(ids),
        character_count=len(rendered),
    )
