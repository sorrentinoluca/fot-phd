"""Validated rendering adapter for the forty real pilot prompts."""

from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

from studio2.fase03.protocol import (
    build_pilot_sample,
    peer_insights,
    validate_insight_library,
    validate_pilot_input_manifest,
)

from .common import HarnessError
from .insight_adapter import validate_be_diff, validate_library
from .ordering import presentation_order


def build_real_pilot_sample(
    manifest: dict[str, Any],
    preflight_config: dict[str, Any],
    *,
    token_count: Callable[[str], int],
    schema_dir: Path,
    source_inventory: dict[str, Any],
) -> list[dict[str, Any]]:
    if source_inventory.get("status") != "COMPLETE_READY_TO_FREEZE":
        raise HarnessError("source inventory is incomplete")
    if source_inventory.get("presentation", {}).get("author_decision") != "accepted":
        raise HarnessError("presentation order has not been accepted by the author")
    value = deepcopy(manifest)
    presented_labels = presentation_order(value["label_space"])
    validate_pilot_input_manifest(value, preflight_config)
    validate_library(
        value["insights"],
        inventory=source_inventory,
        token_count=token_count,
        schema_dir=schema_dir,
    )
    parsed = validate_insight_library(
        value["insights"],
        agents=value["agents"],
        label_space=value["label_space"],
        config=preflight_config,
    )
    for agent_id, agent in value["agents"].items():
        before = peer_insights(
            parsed,
            agent_id=agent_id,
            local_label=agent["local_fault_label"],
            condition="B-LF",
            derangements=value["derangements"],
        )
        after = peer_insights(
            parsed,
            agent_id=agent_id,
            local_label=agent["local_fault_label"],
            condition="E-LF",
            derangements=value["derangements"],
        )
        validate_be_diff(
            [row.to_dict() for row in before],
            [row.to_dict() for row in after],
            mapping=value["derangements"][agent_id],
            agent_id=agent_id,
            inventory=source_inventory,
            token_count=token_count,
            schema_dir=schema_dir,
        )
    truth = {row["case_id"]: row["fault_label"] for row in value["development_cases"]}
    prompts = build_pilot_sample(
        value,
        preflight_config,
        token_count=token_count,
        presentation_label_space=presented_labels,
    )
    return [dict(row.to_dict(), true_pseudolabel=truth[row.case_id]) for row in prompts]
