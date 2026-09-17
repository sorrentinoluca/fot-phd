"""Offline tests for the ``B-noLF`` ablation renderer (author decision D2)."""

from __future__ import annotations

import unittest

from studio2.fase03 import protocol, protocol_bnolf
from studio2.fase03.protocol import ContractError, Insight
from .logging_v1 import CallRecord
from .common import HarnessError, sha256_text

LABELS = [f"S2-CLS-A{index:04d}" for index in range(1, 9)] + ["Normal"]
AGENTS = [f"agent_{index}" for index in range(1, 9)]


def manifest() -> dict:
    return {
        "label_space": LABELS,
        "agents": {agent: {"local_fault_label": LABELS[index]} for index, agent in enumerate(AGENTS)},
        "local_examples": {
            agent: [
                {"example_id": f"{agent}-fault", "pseudolabel": LABELS[index],
                 "neutral_text": f"local fault example for {agent}"},
                {"example_id": f"{agent}-normal", "pseudolabel": "Normal",
                 "neutral_text": f"local normal example for {agent}"},
            ]
            for index, agent in enumerate(AGENTS)
        },
        "derangements": {},
    }


def insights() -> list[Insight]:
    rows = []
    for index, agent in enumerate(AGENTS):
        for slot in (1, 2):
            rows.append(Insight(
                insight_id=f"S2-INS-{index * 2 + slot:03d}",
                source_agent=agent,
                pseudolabel=LABELS[index],
                evidence_scope="local labeled examples",
                variable_ids=("XMEAS(1)", "XMEAS(7)"),
                observed_pattern=f"observed pattern {index}{slot} without any diagnosis",
            ))
    return rows


CASE = {"neutral_text": "neutral case description with observations only"}


def pair(agent: str = "agent_3") -> dict:
    return protocol_bnolf.render_pair(agent_id=agent, case=CASE, manifest=manifest(),
                                      insights=insights())


class BNoLFTests(unittest.TestCase):
    def test_frozen_renderer_hash_is_checked(self):
        self.assertEqual(protocol_bnolf.verify_frozen_renderer(),
                         protocol_bnolf.FROZEN_PROTOCOL_SHA256)

    def test_bnolf_is_blf_minus_the_policy_block_and_nothing_else(self):
        value = pair()
        base, ablated = value["b_lf_text"], value["b_nolf_text"]
        self.assertNotEqual(base, ablated)
        self.assertEqual(base.replace(protocol_bnolf.POLICY_BLOCK, "", 1), ablated)
        offset = base.index(protocol_bnolf.POLICY_BLOCK)
        self.assertEqual(ablated[:offset] + protocol_bnolf.POLICY_BLOCK + ablated[offset:], base)

    def test_the_policy_text_does_not_survive(self):
        value = pair()
        self.assertNotIn("DECISION POLICY", value["b_nolf_text"])
        self.assertNotIn(protocol.LOCAL_FIRST_POLICY, value["b_nolf_text"])
        self.assertIn("DECISION POLICY", value["b_lf_text"])

    def test_every_other_section_is_byte_identical(self):
        value = pair()
        for section in ("LABEL SPACE", "LOCAL LABELED EXAMPLES", "PEER INSIGHTS",
                        "CASE TO DIAGNOSE", "OUTPUT SCHEMA", protocol.BASE_INSTRUCTION):
            self.assertIn(section, value["b_nolf_text"])
        head_base = value["b_lf_text"].split("DECISION POLICY", 1)[0]
        tail_base = value["b_lf_text"].split(protocol.LOCAL_FIRST_POLICY, 1)[1]
        self.assertTrue(value["b_nolf_text"].startswith(head_base))
        self.assertTrue(value["b_nolf_text"].endswith(tail_base.lstrip("\n")))

    def test_peer_insights_are_unchanged_by_the_ablation(self):
        value = pair()
        self.assertEqual(len(value["used_insight_ids"]), 14)
        for insight_id in value["used_insight_ids"]:
            self.assertIn(insight_id, value["b_nolf_text"])

    def test_diff_touches_only_the_policy_block(self):
        value = pair()
        self.assertTrue(protocol_bnolf.diff_is_policy_only(value))
        diff = protocol_bnolf.policy_diff(value)
        self.assertIn("-DECISION POLICY", diff)
        self.assertFalse([line for line in diff.splitlines()
                          if line.startswith("+") and not line.startswith("+++")])

    def test_removed_byte_count_equals_the_policy_block(self):
        value = pair()
        self.assertEqual(value["removed_bytes"],
                         len(protocol_bnolf.POLICY_BLOCK.encode("utf-8")))

    def test_the_ablation_is_stable_across_agents(self):
        for agent in AGENTS:
            value = pair(agent)
            self.assertEqual(value["removed_bytes"],
                             len(protocol_bnolf.POLICY_BLOCK.encode("utf-8")), agent)

    def test_only_the_ablation_token_is_rendered_here(self):
        for condition in ("A", "B-LF", "E-LF"):
            with self.assertRaises(ContractError):
                protocol_bnolf.render_diagnostic_prompt(
                    agent_id="agent_1", condition=condition, case=CASE,
                    manifest=manifest(), insights=insights())

    def test_frozen_protocol_is_not_modified_in_place(self):
        self.assertEqual(protocol.CONDITIONS, ("A", "B-LF", "E-LF"))
        self.assertEqual(protocol_bnolf.FINAL_CONDITIONS, ("A", "B-LF", "E-LF", "B-noLF"))

    def _record(self, condition: str) -> CallRecord:
        raw = '{"predicted_label":null,"abstain":true,"used_insight_ids":[],"reasoning_summary":"x"}'
        return CallRecord.create(
            prompt_id="ablation_b_no_lf|B-noLF|test-primary-F1-r01|agent_1|G_P|r1",
            agent_id="agent_1", physical_case_id="test-primary-F1-r01", condition=condition,
            repetition=1, attempt=1, timestamp_utc="2026-09-17T10:00:00+00:00",
            provider="enea", requested_model="qwen3.5-122b", returned_model="qwen3.5-122b",
            returned_model_revision=None, request_id="req-1",
            system_fingerprint="fp-1", temperature_supported=None, seed_supported=False,
            generation={"max_tokens": 512}, prompt_sha256=sha256_text("p"), prompt_bytes=1,
            raw_response=raw, latency_ms=1.0, prompt_tokens=1, completion_tokens=1,
            total_tokens=2, token_source="provider_usage", finish_reason="stop",
            truncated=False, parse_valid=True, schema_valid=True,
            parsed_output={"predicted_label": None, "abstain": True,
                           "used_insight_ids": [], "reasoning_summary": "x"},
            error=None)

    def test_call_record_admits_the_ablation_token(self):
        record = self._record("B-noLF")
        self.assertEqual(record.condition, "B-noLF")
        self.assertEqual(record.to_dict()["condition"], "B-noLF")

    def test_call_record_still_refuses_an_unknown_token(self):
        with self.assertRaises(HarnessError):
            self._record("B-noLocalFirst")


if __name__ == "__main__":  # pragma: no cover
    unittest.main()
