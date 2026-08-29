"""Deterministic insight-library operations for conditions B and E."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, replace
import re
from typing import Any, Iterable

from phase_b.prompts.leakage import scan_text


INSIGHT_ID = re.compile(r"^INS-[0-9]{3}$")
REQUIRED_KEYS = {
    "insight_id",
    "source_agent",
    "pseudolabel",
    "evidence_scope",
    "observed_pattern",
}


@dataclass(frozen=True)
class Insight:
    insight_id: str
    source_agent: str
    pseudolabel: str
    evidence_scope: str
    observed_pattern: str

    @classmethod
    def from_dict(cls, value: dict[str, Any]) -> "Insight":
        if set(value) != REQUIRED_KEYS:
            raise ValueError(f"insight keys must be exactly {sorted(REQUIRED_KEYS)}")
        if not all(isinstance(value[key], str) for key in REQUIRED_KEYS):
            raise ValueError("every insight field must be a string")
        insight = cls(**value)
        insight.validate()
        return insight

    def validate(self) -> None:
        if not INSIGHT_ID.fullmatch(self.insight_id):
            raise ValueError(f"non-opaque insight_id: {self.insight_id!r}")
        if not re.fullmatch(r"agent_[1-4]", self.source_agent):
            raise ValueError(f"invalid source_agent: {self.source_agent!r}")
        if not re.fullmatch(r"CLS-[A-Z0-9]{5}", self.pseudolabel):
            raise ValueError(f"invalid opaque pseudolabel: {self.pseudolabel!r}")
        if not self.evidence_scope.strip() or not self.observed_pattern.strip():
            raise ValueError("evidence_scope and observed_pattern must be non-empty")

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


def _as_insights(values: Iterable[Insight | dict[str, Any]]) -> list[Insight]:
    return [value if isinstance(value, Insight) else Insight.from_dict(value) for value in values]


def validate_label_neutral_fields(
    insight: Insight, *, label_space: Iterable[str]
) -> None:
    """Ensure that only ``pseudolabel`` carries class identity prompt-side."""
    labels = tuple(label_space)
    for field_name in ("insight_id", "source_agent", "evidence_scope", "observed_pattern"):
        value = getattr(insight, field_name)
        leaked = [label for label in labels if label in value]
        if leaked:
            raise ValueError(
                f"{field_name} must be label-neutral; found configured label(s): {leaked}"
            )
        findings = scan_text(value, source=f"insight:{insight.insight_id}:{field_name}")
        if findings:
            raise ValueError(f"{field_name} contains evaluator-only class information")


def validate_global_insights(
    values: Iterable[Insight | dict[str, Any]], config: dict[str, Any]
) -> list[Insight]:
    insights = sorted(_as_insights(values), key=lambda item: item.insight_id)
    if len({item.insight_id for item in insights}) != len(insights):
        raise ValueError("insight IDs must be globally unique")
    labels = set(config["label_space"][:-1])
    if any(item.pseudolabel not in labels for item in insights):
        raise ValueError("Normal or unknown-label insight detected")
    for item in insights:
        validate_label_neutral_fields(item, label_space=config["label_space"])
    required_count = config["insights"]["insights_per_fault"]
    counts = Counter(item.pseudolabel for item in insights)
    if counts != Counter({label: required_count for label in labels}):
        raise ValueError(f"expected exactly {required_count} insights per fault: {counts}")
    owner = {
        entry["local_fault_label"]: agent_id
        for agent_id, entry in config["agents"].items()
    }
    if any(item.source_agent != owner[item.pseudolabel] for item in insights):
        raise ValueError("insight source_agent does not own its pseudolabel")
    return insights


def peer_only_insights(
    values: Iterable[Insight | dict[str, Any]], agent_id: str, config: dict[str, Any]
) -> list[Insight]:
    insights = validate_global_insights(values, config)
    if agent_id not in config["agents"]:
        raise ValueError(f"unknown agent: {agent_id}")
    self_label = config["agents"][agent_id]["local_fault_label"]
    peers = [
        item
        for item in insights
        if item.source_agent != agent_id and item.pseudolabel != self_label
    ]
    if len(peers) != 6:
        raise ValueError(f"condition B requires exactly six peer insights, got {len(peers)}")
    if any(item.pseudolabel == "Normal" or item.source_agent == agent_id for item in peers):
        raise ValueError("self or Normal insight escaped the peer-only filter")
    return peers


def build_fixed_derangements(config: dict[str, Any]) -> dict[str, dict[str, str]]:
    ordered_labels = config["label_space"][:-1]
    result: dict[str, dict[str, str]] = {}
    for agent_id, agent in config["agents"].items():
        peers = [label for label in ordered_labels if label != agent["local_fault_label"]]
        rotated = peers[1:] + peers[:1]
        result[agent_id] = dict(zip(peers, rotated))
    return result


def corrupt_peer_insights(
    peer_insights: Iterable[Insight | dict[str, Any]],
    *,
    agent_id: str,
    derangements: dict[str, dict[str, str]],
) -> list[Insight]:
    peers = _as_insights(peer_insights)
    mapping = derangements.get(agent_id)
    if mapping is None:
        raise ValueError(f"missing condition-E derangement for {agent_id}")
    labels = {item.pseudolabel for item in peers}
    if set(mapping) != labels or set(mapping.values()) != labels:
        raise ValueError("derangement domain/codomain must equal the three peer labels")
    if any(source == target for source, target in mapping.items()):
        raise ValueError("condition-E mapping has a fixed point")
    corrupted = [replace(item, pseudolabel=mapping[item.pseudolabel]) for item in peers]
    for before, after in zip(peers, corrupted):
        before_dict, after_dict = before.to_dict(), after.to_dict()
        changed = {key for key in before_dict if before_dict[key] != after_dict[key]}
        if changed != {"pseudolabel"}:
            raise AssertionError(f"condition E changed fields other than pseudolabel: {changed}")
    return corrupted
