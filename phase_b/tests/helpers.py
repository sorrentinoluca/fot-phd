from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from phase_b.evaluation.records import RunRecord
from phase_b.insights import Insight


ROOT = Path(__file__).resolve().parents[2]


def load_config() -> dict[str, Any]:
    return json.loads((ROOT / "phase_b/config/protocol_config.json").read_text())


def fixture_insights(config: dict[str, Any]) -> list[Insight]:
    insights: list[Insight] = []
    counter = 1
    for agent_id, agent in config["agents"].items():
        for local_index in (1, 2):
            insights.append(
                Insight(
                    insight_id=f"INS-{counter:03d}",
                    source_agent=agent_id,
                    pseudolabel=agent["local_fault_label"],
                    evidence_scope="synthetic software-test fixture",
                    observed_pattern=f"Observable pattern fixture {local_index}.",
                )
            )
            counter += 1
    return insights


def load_local_examples() -> dict[str, Any]:
    return json.loads((ROOT / "phase_b/local_knowledge/local_examples.json").read_text())


def local_examples_by_agent() -> dict[str, list[dict[str, str]]]:
    artifact = load_local_examples()
    metadata = json.loads(
        (ROOT / "phase_b/config/evaluator_side/local_example_sources.json").read_text()
    )
    return {
        agent_id: artifact["packs"][pack_id]
        for agent_id, pack_id in metadata["agent_to_pack"].items()
    }


def synthetic_run_records(
    config: dict[str, Any], *, abstain_one: bool = False
) -> tuple[list[RunRecord], dict[str, str]]:
    case_truth: dict[str, str] = {}
    labels = config["label_space"]
    for label_index, label in enumerate(labels):
        for run in (1, 2, 3):
            case_truth[f"PHY-{label_index + 1}-{run}"] = label

    records: list[RunRecord] = []
    timestamp = datetime(2026, 8, 29, tzinfo=timezone.utc).isoformat()
    for condition in config["conditions"]:
        for repetition in (1, 2, 3):
            for agent_id, agent in config["agents"].items():
                local = agent["local_fault_label"]
                for case_id, truth in case_truth.items():
                    unseen = truth != "Normal" and truth != local
                    if condition == "B" or not unseen:
                        predicted = truth
                    else:
                        predicted = "Normal"
                    abstain = bool(
                        abstain_one
                        and condition == "A"
                        and repetition == 1
                        and agent_id == "agent_1"
                        and case_id == "PHY-2-1"
                    )
                    parsed = {
                        "predicted_label": None if abstain else predicted,
                        "abstain": abstain,
                        "used_insight_ids": [] if condition == "A" else ["INS-001"],
                        "reasoning_summary": "Synthetic software-test output.",
                    }
                    records.append(
                        RunRecord(
                            agent_id=agent_id,
                            condition=condition,
                            repetition=repetition,
                            model="fixture-model",
                            model_version="fixture-version",
                            prompt_hash="a" * 64,
                            input_hash="b" * 64,
                            raw_output=json.dumps(parsed, separators=(",", ":")),
                            raw_attempts=(json.dumps(parsed, separators=(",", ":")),),
                            parsed_output=parsed,
                            physical_case_id=case_id,
                            temperature=0.0,
                            seed=20260829,
                            timestamp=timestamp,
                        )
                    )
    return records, case_truth
