"""Strict, provider-free contracts for the Study 2 Phase 03 pilot.

This module performs no HTTP requests and imports no model runtime.  It validates
a separately frozen Study 2 pilot-input hand-off, renders the exact 40-prompt technical sample, and checks
the context arithmetic with a caller-supplied offline tokenizer.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict, dataclass, replace
import hashlib
import json
from pathlib import Path
import re
from typing import Any, Callable, Iterable


ROOT = Path(__file__).resolve().parents[2]
PHASE_DIR = ROOT / "studio2/fase03"
PREFLIGHT_CONFIG_PATH = PHASE_DIR / "config/pilot_preflight.json"
INSIGHT_SCHEMA_PATH = PHASE_DIR / "schemas/insight.schema.json"
DIAGNOSTIC_SCHEMA_PATH = PHASE_DIR / "schemas/diagnostic_output.schema.json"

AGENT_IDS = tuple(f"agent_{index}" for index in range(1, 9))
CONDITIONS = ("A", "B-LF", "E-LF")
INSIGHT_KEYS = {
    "insight_id",
    "source_agent",
    "pseudolabel",
    "evidence_scope",
    "variable_ids",
    "observed_pattern",
}
DIAGNOSTIC_KEYS = {
    "predicted_label",
    "abstain",
    "used_insight_ids",
    "reasoning_summary",
}
VARIABLE_ID = re.compile(r"^X(?:MEAS|MV)\([1-9][0-9]*\)$")
INSIGHT_ID = re.compile(r"^S2-INS-[0-9]{3}$")
PSEUDOLABEL = re.compile(r"^S2-CLS-[A-Z0-9]{5}$")

BASE_INSTRUCTION = (
    "You are a diagnostic reasoning agent. Use only the supplied local labeled "
    "examples, optional peer observations, and the neutral case description. "
    "Choose from the supplied label space. The neutral description contains "
    "observations, not a diagnosis. Return strict JSON only, without markdown "
    "or extra keys."
)
LOCAL_FIRST_POLICY = (
    "First compare the case with the local labeled examples. Prefer a local "
    "match supported by specific variables and temporal behavior; use peer "
    "observations mainly when the local examples do not provide a good match. "
    "Do not choose a peer-supported label from global counts or generic "
    "persistence alone. If local and peer evidence are both plausible and "
    "neither is clearly stronger, abstain."
)


class ContractError(ValueError):
    """A frozen input or provider output violates the pilot contract."""


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _no_duplicate_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ContractError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def strict_json_loads(raw: str) -> Any:
    if not isinstance(raw, str) or not raw.strip():
        raise ContractError("JSON value is empty or not text")
    try:
        return json.loads(raw.strip(), object_pairs_hook=_no_duplicate_object)
    except ContractError:
        raise
    except json.JSONDecodeError as exc:
        raise ContractError(f"invalid JSON: {exc.msg}") from exc


@dataclass(frozen=True)
class Insight:
    insight_id: str
    source_agent: str
    pseudolabel: str
    evidence_scope: str
    variable_ids: tuple[str, ...]
    observed_pattern: str

    @classmethod
    def from_dict(cls, value: dict[str, Any], *, max_characters: int) -> "Insight":
        if not isinstance(value, dict) or set(value) != INSIGHT_KEYS:
            raise ContractError(f"insight keys must be exactly {sorted(INSIGHT_KEYS)}")
        if not isinstance(value.get("variable_ids"), list):
            raise ContractError("variable_ids must be an array")
        insight = cls(
            insight_id=value.get("insight_id"),
            source_agent=value.get("source_agent"),
            pseudolabel=value.get("pseudolabel"),
            evidence_scope=value.get("evidence_scope"),
            variable_ids=tuple(value["variable_ids"]),
            observed_pattern=value.get("observed_pattern"),
        )
        insight.validate(max_characters=max_characters)
        return insight

    def validate(self, *, max_characters: int) -> None:
        string_fields = (
            self.insight_id,
            self.source_agent,
            self.pseudolabel,
            self.evidence_scope,
            self.observed_pattern,
        )
        if any(not isinstance(value, str) for value in string_fields):
            raise ContractError("every scalar insight field must be text")
        if not INSIGHT_ID.fullmatch(self.insight_id):
            raise ContractError(f"invalid insight_id: {self.insight_id!r}")
        if self.source_agent not in AGENT_IDS:
            raise ContractError(f"invalid source_agent: {self.source_agent!r}")
        if not PSEUDOLABEL.fullmatch(self.pseudolabel):
            raise ContractError(f"invalid pseudolabel: {self.pseudolabel!r}")
        if not self.evidence_scope.strip() or len(self.evidence_scope) > 240:
            raise ContractError("evidence_scope must contain 1..240 characters")
        if not self.observed_pattern.strip() or len(self.observed_pattern) > max_characters:
            raise ContractError(
                f"observed_pattern must contain 1..{max_characters} characters"
            )
        if not 1 <= len(self.variable_ids) <= 8:
            raise ContractError("variable_ids must contain 1..8 identifiers")
        if len(set(self.variable_ids)) != len(self.variable_ids):
            raise ContractError("variable_ids must be unique")
        if any(not isinstance(value, str) or not VARIABLE_ID.fullmatch(value) for value in self.variable_ids):
            raise ContractError("variable_ids must use exact XMEAS(n) or XMV(n) identifiers")

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["variable_ids"] = list(self.variable_ids)
        return value


@dataclass(frozen=True)
class RenderedPrompt:
    prompt_id: str
    agent_id: str
    case_id: str
    condition: str
    sample_role: str
    text: str
    prompt_sha256: str
    available_insight_ids: tuple[str, ...]
    input_tokens: int | None = None

    def to_dict(self) -> dict[str, Any]:
        value = asdict(self)
        value["available_insight_ids"] = list(self.available_insight_ids)
        return value


def _validate_label_space(value: Any) -> tuple[str, ...]:
    if not isinstance(value, list) or len(value) != 9 or len(set(value)) != 9:
        raise ContractError("label_space must contain nine unique labels")
    if value[-1] != "Normal" or any(
        not isinstance(label, str) or not PSEUDOLABEL.fullmatch(label)
        for label in value[:-1]
    ):
        raise ContractError("label_space must contain eight opaque labels followed by Normal")
    return tuple(value)


def _validate_local_examples(
    examples: Any, *, agent_id: str, local_label: str
) -> list[dict[str, str]]:
    if not isinstance(examples, list) or len(examples) < 2:
        raise ContractError(f"{agent_id} requires at least one local and one Normal example")
    required = {"example_id", "pseudolabel", "neutral_text"}
    if any(not isinstance(item, dict) or set(item) != required for item in examples):
        raise ContractError("local examples must contain only example_id, pseudolabel, neutral_text")
    if any(
        not all(isinstance(item[key], str) and item[key].strip() for key in required)
        for item in examples
    ):
        raise ContractError("local-example fields must be non-empty text")
    counts = Counter(item["pseudolabel"] for item in examples)
    if set(counts) - {local_label, "Normal"}:
        raise ContractError(f"{agent_id} local examples contain a locally-unseen label")
    if counts[local_label] < 1 or counts["Normal"] < 1:
        raise ContractError(f"{agent_id} requires both local-fault and Normal examples")
    return examples


def validate_pilot_input_manifest(
    value: Any,
    config: dict[str, Any],
    *,
    allow_synthetic: bool = False,
) -> dict[str, Any]:
    required = {
        "artifact_version",
        "status",
        "provenance_kind",
        "source_commit",
        "catalog_id",
        "label_space",
        "agents",
        "development_cases",
        "local_examples",
        "insights",
        "derangements",
        "transfer_case_by_agent",
    }
    if not isinstance(value, dict) or set(value) != required:
        raise ContractError(f"pilot input manifest keys must be exactly {sorted(required)}")
    if value["artifact_version"] != "1":
        raise ContractError("pilot input manifest must be version 1")
    status = value["status"]
    provenance_kind = value["provenance_kind"]
    if status == "SYNTHETIC_OFFLINE_FIXTURE":
        if provenance_kind != "synthetic_offline_only" or not allow_synthetic:
            raise ContractError("synthetic fixtures are permitted only in explicit offline verification")
    elif status == "FROZEN_FOR_PHASE03_PRE_GATE":
        if provenance_kind != "study2_scientific":
            raise ContractError("frozen pilot inputs require Study 2 scientific provenance")
    else:
        raise ContractError("pilot input status is not executable")
    if not isinstance(value["source_commit"], str) or not re.fullmatch(
        r"[0-9a-f]{40}", value["source_commit"]
    ):
        raise ContractError("source_commit must be a full lowercase Git object ID")
    if not isinstance(value["catalog_id"], str) or not value["catalog_id"].strip():
        raise ContractError("catalog_id must be non-empty")
    labels = _validate_label_space(value["label_space"])
    agents = value["agents"]
    if not isinstance(agents, dict) or tuple(sorted(agents)) != AGENT_IDS:
        raise ContractError("agents must be exactly agent_1 through agent_8")
    local_labels: list[str] = []
    for agent_id in AGENT_IDS:
        entry = agents[agent_id]
        if not isinstance(entry, dict) or set(entry) != {"local_fault_label"}:
            raise ContractError(f"invalid agent contract for {agent_id}")
        label = entry["local_fault_label"]
        if label not in labels[:-1]:
            raise ContractError(f"invalid local fault label for {agent_id}")
        local_labels.append(label)
    if set(local_labels) != set(labels[:-1]):
        raise ContractError("the eight agents must own the eight fault pseudolabels one-to-one")

    cases = value["development_cases"]
    case_keys = {"case_id", "split", "fault_label", "neutral_text", "neutral_text_sha256"}
    if not isinstance(cases, list) or len(cases) < 9:
        raise ContractError("development_cases must contain at least nine cases")
    by_case: dict[str, dict[str, Any]] = {}
    for case in cases:
        if not isinstance(case, dict) or set(case) != case_keys:
            raise ContractError(f"development case keys must be exactly {sorted(case_keys)}")
        if case["split"] != "development" or case["fault_label"] not in labels:
            raise ContractError("pilot cases must be development-only and in-catalog")
        if not isinstance(case["neutral_text"], str) or not case["neutral_text"].strip():
            raise ContractError("neutral_text must be non-empty")
        if sha256_text(case["neutral_text"].strip()) != case["neutral_text_sha256"]:
            raise ContractError(f"neutral-text hash mismatch: {case['case_id']}")
        if case["case_id"] in by_case:
            raise ContractError(f"duplicate development case: {case['case_id']}")
        by_case[case["case_id"]] = case

    examples = value["local_examples"]
    if not isinstance(examples, dict) or tuple(sorted(examples)) != AGENT_IDS:
        raise ContractError("local_examples must be keyed by all eight agents")
    for agent_id in AGENT_IDS:
        _validate_local_examples(
            examples[agent_id],
            agent_id=agent_id,
            local_label=agents[agent_id]["local_fault_label"],
        )

    validate_insight_library(
        value["insights"],
        agents=agents,
        label_space=labels,
        config=config,
    )
    _validate_derangements(value["derangements"], agents=agents, label_space=labels)

    transfer = value["transfer_case_by_agent"]
    if not isinstance(transfer, dict) or tuple(sorted(transfer)) != AGENT_IDS:
        raise ContractError("transfer_case_by_agent must cover all eight agents")
    transfer_labels: list[str] = []
    for agent_id, case_id in transfer.items():
        if case_id not in by_case:
            raise ContractError(f"unknown transfer development case: {case_id}")
        label = by_case[case_id]["fault_label"]
        if label in {"Normal", agents[agent_id]["local_fault_label"]}:
            raise ContractError(f"transfer case for {agent_id} must be locally unseen")
        transfer_labels.append(label)
    if Counter(transfer_labels) != Counter(labels[:-1]):
        raise ContractError("transfer triplets must cover each catalog fault exactly once")
    return value


def validate_insight_library(
    values: Any,
    *,
    agents: dict[str, dict[str, str]],
    label_space: Iterable[str],
    config: dict[str, Any],
) -> list[Insight]:
    contract = config["insight_contract"]
    if not isinstance(values, list):
        raise ContractError("insights must be an array")
    insights = [
        Insight.from_dict(item, max_characters=contract["observed_pattern_max_characters"])
        for item in values
    ]
    if len(insights) != contract["global_insights"]:
        raise ContractError("global insight library must contain exactly sixteen insights")
    if len({item.insight_id for item in insights}) != len(insights):
        raise ContractError("insight IDs must be globally unique")
    labels = tuple(label_space)[:-1]
    owners = {entry["local_fault_label"]: agent for agent, entry in agents.items()}
    counts = Counter(item.pseudolabel for item in insights)
    expected = Counter({label: contract["insights_per_fault"] for label in labels})
    if counts != expected:
        raise ContractError(f"expected two insights for each fault label: {counts}")
    if any(item.source_agent != owners[item.pseudolabel] for item in insights):
        raise ContractError("insight source_agent must own its pseudolabel")
    return sorted(insights, key=lambda item: item.insight_id)


def validate_produced_insight(
    raw: str,
    *,
    expected_fixed_fields: dict[str, Any],
    token_count: Callable[[str], int],
    config: dict[str, Any],
) -> Insight:
    """Validate a producer response while keeping five fields deterministic."""
    value = strict_json_loads(raw)
    insight = Insight.from_dict(
        value,
        max_characters=config["insight_contract"]["observed_pattern_max_characters"],
    )
    for field in config["insight_contract"]["fixed_fields"]:
        actual = insight.to_dict()[field]
        if actual != expected_fixed_fields[field]:
            raise ContractError(f"producer changed deterministic field {field}")
    tokens = token_count(insight.observed_pattern)
    if tokens > config["insight_contract"]["observed_pattern_max_tokens"]:
        raise ContractError(
            f"observed_pattern uses {tokens} tokens; cap is "
            f"{config['insight_contract']['observed_pattern_max_tokens']}"
        )
    return insight


def validate_produced_insights(
    raw: str,
    *,
    expected_fixed_fields: Iterable[dict[str, Any]],
    token_count: Callable[[str], int],
    config: dict[str, Any],
) -> list[Insight]:
    """Validate one producer response containing exactly two ordered insights."""
    value = strict_json_loads(raw)
    if not isinstance(value, dict) or set(value) != {"insights"}:
        raise ContractError("producer output must contain only the insights array")
    items = value["insights"]
    expected = list(expected_fixed_fields)
    if not isinstance(items, list) or len(items) != 2 or len(expected) != 2:
        raise ContractError("producer output and fixed contract must contain two insights")
    return [
        validate_produced_insight(
            canonical_json(item),
            expected_fixed_fields=fixed,
            token_count=token_count,
            config=config,
        )
        for item, fixed in zip(items, expected)
    ]


def _validate_derangements(
    value: Any,
    *,
    agents: dict[str, dict[str, str]],
    label_space: Iterable[str],
) -> None:
    if not isinstance(value, dict) or tuple(sorted(value)) != AGENT_IDS:
        raise ContractError("derangements must be keyed by all eight agents")
    faults = set(tuple(label_space)[:-1])
    for agent_id in AGENT_IDS:
        peers = faults - {agents[agent_id]["local_fault_label"]}
        mapping = value[agent_id]
        if not isinstance(mapping, dict) or set(mapping) != peers or set(mapping.values()) != peers:
            raise ContractError(f"{agent_id} derangement domain/codomain must be its seven peers")
        if any(source == target for source, target in mapping.items()):
            raise ContractError(f"{agent_id} derangement contains a fixed point")


def peer_insights(
    insights: Iterable[Insight],
    *,
    agent_id: str,
    local_label: str,
    condition: str,
    derangements: dict[str, dict[str, str]],
) -> list[Insight]:
    if condition not in {"B-LF", "E-LF"}:
        raise ContractError("peer insights exist only for B-LF and E-LF")
    peer = [
        item
        for item in insights
        if item.source_agent != agent_id and item.pseudolabel != local_label
    ]
    if len(peer) != 14:
        raise ContractError(f"{agent_id} requires exactly fourteen peer insights")
    if condition == "B-LF":
        return peer
    mapping = derangements[agent_id]
    corrupted = [replace(item, pseudolabel=mapping[item.pseudolabel]) for item in peer]
    for before, after in zip(peer, corrupted):
        changed = {
            key
            for key in before.to_dict()
            if before.to_dict()[key] != after.to_dict()[key]
        }
        if changed != {"pseudolabel"}:
            raise AssertionError(f"E-LF changed fields other than pseudolabel: {changed}")
    return corrupted


def render_diagnostic_prompt(
    *,
    agent_id: str,
    condition: str,
    case: dict[str, Any],
    manifest: dict[str, Any],
    insights: list[Insight],
    presentation_label_space: Iterable[str] | None = None,
) -> tuple[str, tuple[str, ...]]:
    if condition not in CONDITIONS:
        raise ContractError(f"unknown condition: {condition}")
    local_label = manifest["agents"][agent_id]["local_fault_label"]
    examples = _validate_local_examples(
        manifest["local_examples"][agent_id], agent_id=agent_id, local_label=local_label
    )
    selected: list[Insight] = []
    if condition != "A":
        selected = peer_insights(
            insights,
            agent_id=agent_id,
            local_label=local_label,
            condition=condition,
            derangements=manifest["derangements"],
        )
    displayed_labels = tuple(
        manifest["label_space"]
        if presentation_label_space is None
        else presentation_label_space
    )
    canonical_labels = tuple(manifest["label_space"])
    if (
        len(displayed_labels) != len(canonical_labels)
        or set(displayed_labels) != set(canonical_labels)
        or displayed_labels[-1] != "Normal"
    ):
        raise ContractError(
            "presentation_label_space must be a permutation of the canonical labels "
            "with Normal last"
        )
    sections = [BASE_INSTRUCTION]
    if condition != "A":
        sections.extend(("DECISION POLICY", LOCAL_FIRST_POLICY))
    sections.extend(
        (
            "LABEL SPACE",
            json.dumps(displayed_labels, ensure_ascii=False),
            "LOCAL LABELED EXAMPLES",
            json.dumps(examples, ensure_ascii=False, indent=2),
        )
    )
    if selected:
        sections.extend(
            (
                "PEER INSIGHTS",
                json.dumps([item.to_dict() for item in selected], ensure_ascii=False, indent=2),
            )
        )
    sections.extend(
        (
            "CASE TO DIAGNOSE",
            case["neutral_text"].strip(),
            "OUTPUT SCHEMA",
            '{"predicted_label":"one supplied label or null only when abstaining",'
            '"abstain":false,"used_insight_ids":[],"reasoning_summary":'
            '"one to three concise sentences"}',
            "If abstain is false, predicted_label must be exactly one supplied label. "
            "If abstain is true, predicted_label must be null. Use only supplied peer "
            "insight IDs; when none are supplied, used_insight_ids must be empty. "
            "Do not output confidence.",
        )
    )
    return "\n\n".join(sections).strip() + "\n", tuple(
        item.insight_id for item in selected
    )


def _build_pilot_sample(
    manifest: dict[str, Any],
    config: dict[str, Any],
    *,
    token_count: Callable[[str], int],
    allow_synthetic: bool = False,
    presentation_label_space: Iterable[str] | None = None,
) -> list[RenderedPrompt]:
    validate_pilot_input_manifest(manifest, config, allow_synthetic=allow_synthetic)
    insights = validate_insight_library(
        manifest["insights"],
        agents=manifest["agents"],
        label_space=manifest["label_space"],
        config=config,
    )
    by_case = {item["case_id"]: item for item in manifest["development_cases"]}
    rows: list[RenderedPrompt] = []
    sequence = 0

    def append(agent_id: str, case: dict[str, Any], condition: str, role: str) -> None:
        nonlocal sequence
        sequence += 1
        text, available = render_diagnostic_prompt(
            agent_id=agent_id,
            condition=condition,
            case=case,
            manifest=manifest,
            insights=insights,
            presentation_label_space=presentation_label_space,
        )
        rows.append(
            RenderedPrompt(
                prompt_id=f"S2-P03-{sequence:03d}",
                agent_id=agent_id,
                case_id=case["case_id"],
                condition=condition,
                sample_role=role,
                text=text,
                prompt_sha256=sha256_text(text),
                available_insight_ids=available,
                input_tokens=token_count(text),
            )
        )

    for agent_id in AGENT_IDS:
        transfer = by_case[manifest["transfer_case_by_agent"][agent_id]]
        for condition in CONDITIONS:
            append(agent_id, transfer, condition, "matched_transfer")

        eligible = [
            case
            for case in manifest["development_cases"]
            if case["case_id"] != transfer["case_id"]
            and case["fault_label"] not in {
                "Normal",
                manifest["agents"][agent_id]["local_fault_label"],
            }
        ]
        if not eligible:
            raise ContractError(f"no context-stress candidate for {agent_id}")

        scored: list[tuple[int, str, dict[str, Any]]] = []
        for case in eligible:
            text, _ = render_diagnostic_prompt(
                agent_id=agent_id,
                condition="B-LF",
                case=case,
                manifest=manifest,
                insights=insights,
                presentation_label_space=presentation_label_space,
            )
            scored.append((token_count(text), case["case_id"], case))
        stress = max(scored, key=lambda item: (item[0], item[1]))[2]
        for condition in ("B-LF", "E-LF"):
            append(agent_id, stress, condition, "context_stress")

    if len(rows) != 40 or len({item.prompt_sha256 for item in rows}) != 40:
        raise ContractError("pilot sample must contain forty distinct rendered prompts")
    counts = Counter(item.condition for item in rows)
    if counts != Counter({"A": 8, "B-LF": 16, "E-LF": 16}):
        raise AssertionError(f"unexpected pilot condition counts: {counts}")
    return rows


def context_feasibility(
    prompts: Iterable[RenderedPrompt], config: dict[str, Any]
) -> dict[str, Any]:
    rows = list(prompts)
    if not rows or any(item.input_tokens is None for item in rows):
        raise ContractError("offline token counts are required for context feasibility")
    budget = config["generation_budget"]
    maximum = max(int(item.input_tokens) for item in rows)
    context = config["candidate"]["expected_max_model_len"]
    answer = budget["answer_reserve_tokens"]
    margin = budget["context_safety_margin_tokens"]
    candidates = []
    for thinking in budget["thinking_token_budget_candidates"]:
        max_tokens = thinking + answer
        remaining = context - maximum - max_tokens
        candidates.append(
            {
                "thinking_token_budget": thinking,
                "max_tokens": max_tokens,
                "maximum_input_tokens": maximum,
                "required_context_tokens": maximum + max_tokens + margin,
                "context_margin_tokens": remaining,
                "fits_with_required_safety_margin": remaining >= margin and (
                    "d9" not in config or max_tokens <= config["d9"]["services"]["122B"]["max_output_tokens"]),
            }
        )
    feasible = [
        item
        for item in candidates
        if item["fits_with_required_safety_margin"]
        and item["thinking_token_budget"] >= budget["minimum_acceptable_thinking_token_budget"]
    ]
    return {
        "expected_max_model_len": context,
        "minimum_input_tokens": min(int(item.input_tokens) for item in rows),
        "maximum_input_tokens": maximum,
        "answer_reserve_tokens": answer,
        "required_safety_margin_tokens": margin,
        "candidates": candidates,
        "feasible_candidates": feasible,
        "static_context_gate": "PASS" if feasible else "FAIL",
        "generation_budget_frozen": False,
        "note": (
            "Static fit is necessary but not sufficient. A candidate becomes frozen only "
            "after the pre-gate generation probe shows no length truncation on every "
            "A/B-LF/E-LF stress fixture."
        ),
    }


def parse_diagnostic_output(
    raw: str,
    *,
    label_space: Iterable[str],
    allowed_insight_ids: Iterable[str],
) -> dict[str, Any]:
    value = strict_json_loads(raw)
    if not isinstance(value, dict) or set(value) != DIAGNOSTIC_KEYS:
        raise ContractError(f"diagnostic keys must be exactly {sorted(DIAGNOSTIC_KEYS)}")
    labels = set(label_space)
    allowed = set(allowed_insight_ids)
    abstain = value["abstain"]
    predicted = value["predicted_label"]
    used = value["used_insight_ids"]
    reasoning = value["reasoning_summary"]
    if type(abstain) is not bool:
        raise ContractError("abstain must be a JSON Boolean")
    if abstain and predicted is not None:
        raise ContractError("abstaining output requires predicted_label=null")
    if not abstain and predicted not in labels:
        raise ContractError("non-abstaining output requires one exact supplied label")
    if not isinstance(used, list) or any(not isinstance(item, str) for item in used):
        raise ContractError("used_insight_ids must be a string array")
    if len(used) > 14 or len(set(used)) != len(used) or set(used) - allowed:
        raise ContractError("used_insight_ids contains duplicates, unavailable IDs, or more than 14 items")
    if not isinstance(reasoning, str) or not reasoning.strip() or len(reasoning) > 1200:
        raise ContractError("reasoning_summary must contain 1..1200 characters")
    return value


def build_pilot_sample(manifest, config, *, token_count, allow_synthetic=False,
                       presentation_label_space=None, source_inventory=None, schema_dir=None):
    """Public ordinary entrypoint enforces the real renderer's approval and R4 checks."""
    if allow_synthetic:
        return _build_pilot_sample(manifest, config, token_count=token_count, allow_synthetic=True,
                                   presentation_label_space=presentation_label_space)
    if source_inventory is None or schema_dir is None:
        raise ContractError('real prompts require approved inventory and R4 renderer')
    from studio2.fase03.harness.render import build_real_pilot_sample
    return build_real_pilot_sample(manifest, config, token_count=token_count,
                                   schema_dir=schema_dir, source_inventory=source_inventory)
