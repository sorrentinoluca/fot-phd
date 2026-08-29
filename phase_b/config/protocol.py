"""Strict, dependency-free validation of the Phase B protocol config."""

from __future__ import annotations

import json
import base64
import hashlib
from pathlib import Path
from typing import Any


DEFAULT_CONFIG = Path(__file__).with_name("protocol_config.json")
OPAQUE_PREFIX = "CLS-"


def derive_opaque_pseudolabel(real_identifier: str, namespace: str) -> str:
    """Derive a fixed opaque token without encoding semantic order or identity."""
    digest = hashlib.sha256((namespace + real_identifier).encode("utf-8")).digest()
    suffix = base64.b32encode(digest).decode("ascii").rstrip("=")[:5]
    return OPAQUE_PREFIX + suffix


def load_protocol_config(path: str | Path = DEFAULT_CONFIG) -> dict[str, Any]:
    config = json.loads(Path(path).read_text(encoding="utf-8"))
    required = {
        "protocol_version",
        "status",
        "label_space",
        "agents",
        "local_examples",
        "insights",
        "conditions",
        "execution",
        "metrics",
        "data_boundaries",
    }
    missing = sorted(required - set(config))
    if missing:
        raise ValueError(f"Phase B config missing keys: {missing}")

    labels = config["label_space"]
    if len(labels) != 5 or len(set(labels)) != 5 or labels[-1] != "Normal":
        raise ValueError("label_space must contain four unique opaque labels plus Normal")
    opaque = labels[:-1]
    if any(not isinstance(label, str) or not label.startswith(OPAQUE_PREFIX) for label in opaque):
        raise ValueError("fault pseudolabels must use the opaque CLS- prefix")
    if len({len(label) for label in opaque}) != 1:
        raise ValueError("opaque pseudolabels must have equal length for condition E")

    agents = config["agents"]
    if set(agents) != {f"agent_{index}" for index in range(1, 5)}:
        raise ValueError("exactly agent_1 through agent_4 are required")
    local_labels = [entry["local_fault_label"] for entry in agents.values()]
    if set(local_labels) != set(opaque) or len(local_labels) != len(set(local_labels)):
        raise ValueError("each opaque fault label must belong to exactly one agent")
    if any(entry.get("normal_label") != "Normal" for entry in agents.values()):
        raise ValueError("Normal must be local to every agent")

    local = config["local_examples"]
    if local.get("examples_per_class") != 2 or local.get("development_batches") != [1, 2]:
        raise ValueError("local examples are frozen to two examples from batches 1 and 2")
    if local.get("include_structured_json_in_diagnostic_prompt") is not False:
        raise ValueError("diagnostic prompts must not receive structured JSON")

    insights = config["insights"]
    if insights.get("insights_per_fault") != 2:
        raise ValueError("exactly two insights per fault are required")
    if not insights.get("peer_only") or insights.get("include_self") or insights.get("include_normal"):
        raise ValueError("federation must be peer-only with no self or Normal insights")
    if config["conditions"] != ["A", "B", "E"]:
        raise ValueError("conditions must be exactly A, B, E")

    execution = config["execution"]
    if execution.get("provider") != "openai":
        raise ValueError("Phase B provider is fixed to openai")
    if execution.get("requested_model") != "gpt-5.6-terra":
        raise ValueError("requested model is fixed to gpt-5.6-terra")
    if execution.get("reasoning_effort") not in {None, "medium"}:
        raise ValueError("reasoning effort must be medium or null after technical rejection")
    if execution.get("repetitions") != 3:
        raise ValueError("R is frozen to 3")
    if execution.get("temperature") not in {None, 0.0}:
        raise ValueError("temperature must be null or capability-verified zero")
    if execution.get("seed") is not None and not isinstance(execution.get("seed"), int):
        raise ValueError("seed must be null or a capability-verified integer")
    if execution.get("max_retries") != 2:
        raise ValueError("retry policy is frozen to initial attempt plus two retries")
    if config["metrics"].get("epsilon_seen") != 0.0:
        raise ValueError("H2 epsilon is frozen to zero")
    if config["metrics"].get("abstain_is_incorrect") is not True:
        raise ValueError("abstention must count as incorrect in primary accuracy")
    metrics = config["metrics"]
    if metrics.get("bootstrap_iterations") != 10_000:
        raise ValueError("primary bootstrap is frozen to 10,000 draws")
    if not isinstance(metrics.get("bootstrap_seed"), int):
        raise ValueError("bootstrap seed must be a frozen integer")
    if metrics.get("physical_cluster_key") != "physical_case_id":
        raise ValueError("primary bootstrap cluster must be physical_case_id")
    if metrics.get("bootstrap_stratify_by_true_pseudolabel") is not True:
        raise ValueError("primary bootstrap must be stratified by true pseudoclass")
    return config


def validate_execution_ready(config: dict[str, Any]) -> None:
    """Refuse definitive execution until the capability probe is complete."""
    execution = config["execution"]
    if execution.get("capability_probe_status") != "COMPLETE":
        raise ValueError("Researcher decision required before inference: capability_probe_status")
    missing = [
        field
        for field in (
            "provider",
            "requested_model",
            "returned_model",
            "model_version",
            "sdk_version",
            "token_accounting_source",
        )
        if not isinstance(execution.get(field), str) or not execution[field].strip()
    ]
    if missing:
        raise ValueError(
            "Researcher decision required before inference: " + ", ".join(missing)
        )
