"""Declared synthetic inputs for offline-only Phase 03 verification.

Nothing in this module is a fault selection, simulation output, calibrated
feature, scientific evidence, or candidate for promotion to a real pilot input.
"""

from __future__ import annotations

from typing import Any

from studio2.fase03.protocol import AGENT_IDS, sha256_text


SYNTHETIC_SOURCE_COMMIT = "0" * 40


def _words(prefix: str, count: int) -> str:
    return " ".join(f"{prefix}{index % 11}" for index in range(count))


def build_synthetic_manifest(profile: str) -> dict[str, Any]:
    if profile not in {"nominal", "cap_stress"}:
        raise ValueError("synthetic profile must be nominal or cap_stress")
    labels = [f"S2-CLS-{index:05d}" for index in range(1, 9)] + ["Normal"]
    agents = {
        agent_id: {"local_fault_label": labels[index]}
        for index, agent_id in enumerate(AGENT_IDS)
    }
    case_words = 180 if profile == "nominal" else 900
    example_words = 55 if profile == "nominal" else 140
    insight_words = 38 if profile == "nominal" else 105

    development_cases = []
    for fault_index, label in enumerate(labels[:-1], start=1):
        for run in (1, 2):
            neutral = (
                f"SYNTHETIC OFFLINE ONLY case fault-slot {fault_index} run {run}. "
                + _words(f"signal{fault_index}_", case_words + fault_index * run)
            )
            development_cases.append(
                {
                    "case_id": f"SYN-DEV-F{fault_index:02d}-R{run}",
                    "split": "development",
                    "fault_label": label,
                    "neutral_text": neutral,
                    "neutral_text_sha256": sha256_text(neutral),
                }
            )
    normal = "SYNTHETIC OFFLINE ONLY Normal slot. " + _words("normal_", case_words)
    development_cases.append(
        {
            "case_id": "SYN-DEV-N-R1",
            "split": "development",
            "fault_label": "Normal",
            "neutral_text": normal,
            "neutral_text_sha256": sha256_text(normal),
        }
    )

    local_examples = {}
    for index, agent_id in enumerate(AGENT_IDS, start=1):
        local_examples[agent_id] = []
        for kind, label in (
            ("fault-1", labels[index - 1]),
            ("fault-2", labels[index - 1]),
            ("normal-1", "Normal"),
            ("normal-2", "Normal"),
        ):
            local_examples[agent_id].append(
                {
                    "example_id": f"SYN-{agent_id}-{kind}",
                    "pseudolabel": label,
                    "neutral_text": (
                        f"SYNTHETIC OFFLINE ONLY local example {kind}. "
                        + _words(f"example{index}_", example_words)
                    ),
                }
            )

    insights = []
    insight_index = 0
    for index, agent_id in enumerate(AGENT_IDS, start=1):
        for ordinal in (1, 2):
            insight_index += 1
            insights.append(
                {
                    "insight_id": f"S2-INS-{insight_index:03d}",
                    "source_agent": agent_id,
                    "pseudolabel": labels[index - 1],
                    "evidence_scope": "SYNTHETIC OFFLINE ONLY; no simulated or measured evidence",
                    "variable_ids": [f"XMEAS({index})", f"XMV({index})"],
                    "observed_pattern": (
                        f"SYNTHETIC pattern {ordinal}. "
                        + " ".join(["signal"] * insight_words)
                    ),
                }
            )

    derangements = {}
    for index, agent_id in enumerate(AGENT_IDS):
        peers = [label for label in labels[:-1] if label != labels[index]]
        derangements[agent_id] = dict(zip(peers, peers[1:] + peers[:1]))
    transfer_case_by_agent = {
        agent_id: f"SYN-DEV-F{((index + 1) % 8) + 1:02d}-R1"
        for index, agent_id in enumerate(AGENT_IDS)
    }
    return {
        "artifact_version": "1",
        "status": "SYNTHETIC_OFFLINE_FIXTURE",
        "provenance_kind": "synthetic_offline_only",
        "source_commit": SYNTHETIC_SOURCE_COMMIT,
        "catalog_id": f"SYNTHETIC-NOT-A-CATALOG-{profile.upper()}",
        "label_space": labels,
        "agents": agents,
        "development_cases": development_cases,
        "local_examples": local_examples,
        "insights": insights,
        "derangements": derangements,
        "transfer_case_by_agent": transfer_case_by_agent,
    }
