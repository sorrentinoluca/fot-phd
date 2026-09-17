from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from studio2.fase03.protocol import (
    AGENT_IDS,
    ContractError,
    build_pilot_sample,
    context_feasibility,
    load_json,
    parse_diagnostic_output,
    peer_insights,
    validate_insight_library,
    validate_pilot_input_manifest,
    validate_produced_insights,
)
from studio2.fase03.prepare_gate import tokenized_length


ROOT = Path(__file__).resolve().parents[3]
CONFIG = load_json(ROOT / "studio2/fase03/config/pilot_preflight.json")


def digest(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def fixture_manifest():
    labels = [f"S2-CLS-{index:05d}" for index in range(1, 9)] + ["Normal"]
    agents = {
        agent: {"local_fault_label": labels[index]}
        for index, agent in enumerate(AGENT_IDS)
    }
    cases = []
    for index, label in enumerate(labels[:-1], start=1):
        for run in (1, 2):
            text = f"Development evidence for opaque fault {index}, run {run}. " + "signal " * (index + run)
            cases.append(
                {
                    "case_id": f"DEV-F{index:02d}-R{run}",
                    "split": "development",
                    "fault_label": label,
                    "neutral_text": text,
                    "neutral_text_sha256": digest(text.strip()),
                }
            )
    normal = "Development Normal evidence."
    cases.append(
        {
            "case_id": "DEV-N-R1",
            "split": "development",
            "fault_label": "Normal",
            "neutral_text": normal,
            "neutral_text_sha256": digest(normal),
        }
    )
    local_examples = {
        agent: [
            {
                "example_id": f"{agent}-fault",
                "pseudolabel": agents[agent]["local_fault_label"],
                "neutral_text": "Local development fault evidence.",
            },
            {
                "example_id": f"{agent}-normal",
                "pseudolabel": "Normal",
                "neutral_text": "Local development Normal evidence.",
            },
        ]
        for agent in AGENT_IDS
    }
    insights = []
    insight_index = 0
    for index, agent in enumerate(AGENT_IDS):
        for item in range(2):
            insight_index += 1
            insights.append(
                {
                    "insight_id": f"S2-INS-{insight_index:03d}",
                    "source_agent": agent,
                    "pseudolabel": labels[index],
                    "evidence_scope": "frozen development evidence",
                    "variable_ids": [f"XMEAS({index + 1})"],
                    "observed_pattern": f"Opaque pattern {item + 1} for agent {index + 1}.",
                }
            )
    derangements = {}
    for index, agent in enumerate(AGENT_IDS):
        peers = [label for label in labels[:-1] if label != labels[index]]
        derangements[agent] = dict(zip(peers, peers[1:] + peers[:1]))
    transfer = {
        agent: f"DEV-F{((index + 1) % 8) + 1:02d}-R1"
        for index, agent in enumerate(AGENT_IDS)
    }
    return {
        "artifact_version": "1",
        "status": "SYNTHETIC_OFFLINE_FIXTURE",
        "provenance_kind": "synthetic_offline_only",
        "source_commit": "a" * 40,
        "catalog_id": "synthetic-test-catalog",
        "label_space": labels,
        "agents": agents,
        "development_cases": cases,
        "local_examples": local_examples,
        "insights": insights,
        "derangements": derangements,
        "transfer_case_by_agent": transfer,
    }


class ManifestTests(unittest.TestCase):
    def test_manifest_and_exact_sample_shape(self):
        manifest = fixture_manifest()
        validate_pilot_input_manifest(manifest, CONFIG, allow_synthetic=True)
        prompts = build_pilot_sample(
            manifest, CONFIG, token_count=len, allow_synthetic=True
        )
        self.assertEqual(len(prompts), 40)
        self.assertEqual(sum(item.condition == "A" for item in prompts), 8)
        self.assertEqual(sum(item.condition == "B-LF" for item in prompts), 16)
        self.assertEqual(sum(item.condition == "E-LF" for item in prompts), 16)
        self.assertTrue(all(len(item.available_insight_ids) == 0 for item in prompts if item.condition == "A"))
        self.assertTrue(all(len(item.available_insight_ids) == 14 for item in prompts if item.condition != "A"))

    def test_synthetic_manifest_is_rejected_by_executable_path(self):
        with self.assertRaisesRegex(ContractError, "explicit offline verification"):
            validate_pilot_input_manifest(fixture_manifest(), CONFIG)

    def test_final_test_split_is_rejected(self):
        manifest = fixture_manifest()
        manifest["development_cases"][0]["split"] = "test"
        with self.assertRaisesRegex(ContractError, "development-only"):
            validate_pilot_input_manifest(manifest, CONFIG, allow_synthetic=True)

    def test_transfer_cases_cover_catalog_once(self):
        manifest = fixture_manifest()
        manifest["transfer_case_by_agent"]["agent_8"] = manifest["transfer_case_by_agent"]["agent_1"]
        with self.assertRaisesRegex(ContractError, "each catalog fault exactly once"):
            validate_pilot_input_manifest(manifest, CONFIG, allow_synthetic=True)


class InsightTests(unittest.TestCase):
    def test_e_changes_only_pseudolabel(self):
        manifest = fixture_manifest()
        insights = validate_insight_library(
            manifest["insights"],
            agents=manifest["agents"],
            label_space=manifest["label_space"],
            config=CONFIG,
        )
        local = manifest["agents"]["agent_1"]["local_fault_label"]
        before = peer_insights(
            insights,
            agent_id="agent_1",
            local_label=local,
            condition="B-LF",
            derangements=manifest["derangements"],
        )
        after = peer_insights(
            insights,
            agent_id="agent_1",
            local_label=local,
            condition="E-LF",
            derangements=manifest["derangements"],
        )
        for left, right in zip(before, after):
            changed = {
                key
                for key in left.to_dict()
                if left.to_dict()[key] != right.to_dict()[key]
            }
            self.assertEqual(changed, {"pseudolabel"})

    def test_producer_cannot_change_fixed_variable_ids(self):
        expected = fixture_manifest()["insights"][:2]
        value = {"insights": [dict(item) for item in expected]}
        value["insights"][1]["variable_ids"] = ["XMEAS(99)"]
        fixed = [
            {key: item[key] for key in CONFIG["insight_contract"]["fixed_fields"]}
            for item in expected
        ]
        with self.assertRaisesRegex(ContractError, "deterministic field variable_ids"):
            validate_produced_insights(
                json.dumps(value),
                expected_fixed_fields=fixed,
                token_count=lambda text: len(text.split()),
                config=CONFIG,
            )

    def test_producer_narrative_token_cap(self):
        expected = fixture_manifest()["insights"][:2]
        value = {"insights": [dict(item) for item in expected]}
        value["insights"][0]["observed_pattern"] = "x " * 193
        fixed = [
            {key: item[key] for key in CONFIG["insight_contract"]["fixed_fields"]}
            for item in expected
        ]
        with self.assertRaisesRegex(ContractError, "cap is 192"):
            validate_produced_insights(
                json.dumps(value),
                expected_fixed_fields=fixed,
                token_count=lambda text: len(text.split()),
                config=CONFIG,
            )


class DiagnosticAndBudgetTests(unittest.TestCase):
    def test_batch_encoding_counts_input_ids_not_mapping_keys(self):
        encoded = {"input_ids": [10, 20, 30, 40], "attention_mask": [1, 1, 1, 1]}
        self.assertEqual(tokenized_length(encoded), 4)
        self.assertEqual(tokenized_length([10, 20, 30]), 3)
        self.assertEqual(tokenized_length({"input_ids": [[10, 20, 30]]}), 3)

    def test_tokenized_length_rejects_ambiguous_or_invalid_shapes(self):
        invalid = (
            {"attention_mask": [1]},
            {"input_ids": [[10], [20]]},
            {"input_ids": [10, [20]]},
            {"input_ids": [10, "20"]},
            {"input_ids": [True]},
            {"input_ids": [-1]},
            {"input_ids": object()},
        )
        for encoded in invalid:
            with self.subTest(encoded=encoded), self.assertRaises(RuntimeError):
                tokenized_length(encoded)

    def test_abstention_contract(self):
        result = parse_diagnostic_output(
            '{"predicted_label":null,"abstain":true,"used_insight_ids":[],"reasoning_summary":"Insufficient evidence."}',
            label_space=fixture_manifest()["label_space"],
            allowed_insight_ids=[],
        )
        self.assertTrue(result["abstain"])
        with self.assertRaisesRegex(ContractError, "predicted_label=null"):
            parse_diagnostic_output(
                '{"predicted_label":"Normal","abstain":true,"used_insight_ids":[],"reasoning_summary":"No."}',
                label_space=fixture_manifest()["label_space"],
                allowed_insight_ids=[],
            )

    def test_diagnostic_contract_rejects_duplicate_insight_ids_locally(self):
        raw = json.dumps(
            {
                "predicted_label": None,
                "abstain": True,
                "used_insight_ids": ["S2-INS-001", "S2-INS-001"],
                "reasoning_summary": "Insufficient evidence.",
            }
        )
        with self.assertRaisesRegex(ContractError, "duplicates"):
            parse_diagnostic_output(
                raw,
                label_space=fixture_manifest()["label_space"],
                allowed_insight_ids=["S2-INS-001"],
            )

    def test_context_gate_requires_margin_and_does_not_freeze(self):
        prompts = build_pilot_sample(
            fixture_manifest(),
            CONFIG,
            token_count=lambda text: 3000,
            allow_synthetic=True,
        )
        result = context_feasibility(prompts, CONFIG)
        self.assertEqual(result["static_context_gate"], "PASS")
        self.assertFalse(result["generation_budget_frozen"])
        self.assertEqual(
            [item["thinking_token_budget"] for item in result["feasible_candidates"]],
            [2048, 3072, 4096],
        )
        self.assertEqual(result["candidates"][-1]["required_context_tokens"], 7864)

    def test_d11_is_not_determinism_decision_11(self):
        policy = CONFIG["determinism_policy"]
        self.assertIn("D11 is the local-first ablation subset", policy["d11_disambiguation"])
        self.assertIn("decision 11", policy["plan_reference"])
        self.assertFalse(policy["absence_of_both_controls_alone_activates_r3"])


if __name__ == "__main__":
    unittest.main()
