from __future__ import annotations

import json
from pathlib import Path
import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
import unittest

from studio2.fase03 import producer_probe, run_pilot
from studio2.fase03.harness.common import HarnessError, load_json
from studio2.fase03.harness.gate_rules import evaluate_stability_gate, semantic_signature
from studio2.fase03.harness.inputs import (
    AGENTS,
    SCHEMA_MANIFEST_SHA256,
    SCHEMA_TARGET_COMMIT,
)
from studio2.fase03.harness.insight_adapter import (
    context_from_inventory,
    load_validator,
)
from studio2.fase03.harness.ledger import PilotLedger
from studio2.fase03.harness.producer import build_producer_prompt
from studio2.fase03.protocol import ContractError, render_diagnostic_prompt


ROOT = Path(__file__).resolve().parents[3]
SCHEMA_DIR = ROOT / "studio2/fase03/schema_insight"
INVENTORY_PATH = ROOT / "studio2/fase03/harness/PILOT_INPUT_SOURCES.pending.json"
H = "a" * 64


def contracts() -> list[dict[str, object]]:
    labels = load_json(ROOT / "studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json")["label_space"][:-1]
    return [
        {
            "insight_id": f"S2-INS-{index + 1:03d}",
            "source_agent": AGENTS[index // 2],
            "pseudolabel": labels[index // 2],
            "evidence_scope": "one 5 h development window",
            "variable_ids": ["XMEAS(1)"],
            "source_example_id": f"S2-EXM-{index + 1:03d}",
        }
        for index in range(16)
    ]


def gate_rows(*, invalid: set[tuple[int, int]] | None = None, truncate: tuple[int, int] | None = None):
    invalid = invalid or set()
    rows = []
    for prompt in range(40):
        condition = ("A", "B-LF", "E-LF")[prompt % 3]
        for repetition in range(3):
            valid = (prompt, repetition) not in invalid
            abstain = valid and prompt in {0, 1, 2}
            rows.append(
                {
                    "prompt_id": f"P-{prompt:02d}",
                    "condition": condition,
                    "repetition": repetition + 1,
                    "parse_valid_first_attempt": valid,
                    "parsed_output": (
                        {"abstain": True, "predicted_label": None}
                        if abstain
                        else ({"abstain": False, "predicted_label": "S2-CLS-3ZGWQ"} if valid else None)
                    ),
                    "finish_reason": "length" if truncate == (prompt, repetition) else "stop",
                    "truncated": truncate == (prompt, repetition),
                    "raw_output_sha256": str(prompt + repetition),
                }
            )
    return rows


class R4AndInputContractTests(unittest.TestCase):
    def test_published_r4_pin_and_literal_normal_context(self):
        validator = load_validator(SCHEMA_DIR)
        self.assertEqual(validator.VERSION, "1.0.0")
        context = context_from_inventory({"fixed_insight_contracts": contracts()})
        fixed = validator.context_check(context)
        self.assertEqual(context["normal_label"], "Normal")
        self.assertEqual(len(fixed), 16)

    def test_schema_byte_incompatibility_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            copy = Path(directory)
            for name in ("validator.py", "insight_v1.schema.json", "leakage_rules_v1.json", "SCHEMA_FREEZE.json"):
                shutil.copy2(SCHEMA_DIR / name, copy / name)
            (copy / "validator.py").write_text((copy / "validator.py").read_text() + "\n", encoding="utf-8")
            with self.assertRaisesRegex(HarnessError, "SHA-256 mismatch"):
                load_validator(copy)

    def test_real_inventory_connects_inputs_without_inventing_library(self):
        value = load_json(INVENTORY_PATH)
        self.assertEqual(value["status"], "INCOMPLETE")
        self.assertEqual(value["missing_requirements"], ["16 real schema-valid producer insights"])
        schema = value["sources"]["schema_contract"]
        self.assertEqual(schema["target_commit"], SCHEMA_TARGET_COMMIT)
        self.assertEqual(schema["manifest_sha256"], SCHEMA_MANIFEST_SHA256)
        self.assertEqual(len(value["development_cases"]), 320)
        self.assertEqual(len(value["fixed_insight_contracts"]), 16)
        normal = [row for rows in value["producer_conformance_inputs"]["local_examples"].values() for row in rows if row["pseudolabel"] == "Normal"]
        self.assertEqual(len(normal), 8)
        self.assertFalse(value["producer_conformance_inputs"]["scientific_library_present"])
        producer_probe._conformance_inputs(value)

    def test_missing_normal_or_extra_missing_dependency_is_rejected(self):
        value = load_json(INVENTORY_PATH)
        changed = json.loads(json.dumps(value))
        changed["missing_requirements"].insert(0, "normal_dev examples frozen by 03.9")
        with self.assertRaisesRegex(HarnessError, "other than its output library"):
            producer_probe._conformance_inputs(changed)
        examples = value["producer_conformance_inputs"]["local_examples"]["agent_1"][:2]
        with self.assertRaisesRegex(HarnessError, "fault and Normal"):
            build_producer_prompt(agent_id="agent_1", local_examples=examples, fixed_contracts=value["fixed_insight_contracts"])

    def test_execution_never_defaults_to_historical_model(self):
        with self.assertRaisesRegex(HarnessError, "after D9"):
            producer_probe.provider_config(None)

    def test_presentation_order_does_not_mutate_canonical_label_space(self):
        source = load_json(INVENTORY_PATH)
        canonical = source["presentation"]["catalog_order_labels_evaluator_side"] + ["Normal"]
        presented = source["presentation"]["ordered_labels"]
        manifest = {
            "label_space": canonical,
            "agents": {"agent_1": {"local_fault_label": canonical[0]}},
            "local_examples": {
                "agent_1": [
                    {"example_id": "fault", "pseudolabel": canonical[0], "neutral_text": "fault"},
                    {"example_id": "normal", "pseudolabel": "Normal", "neutral_text": "normal"},
                ]
            },
            "derangements": {},
        }
        text, _ = render_diagnostic_prompt(
            agent_id="agent_1",
            condition="A",
            case={"neutral_text": "case"},
            manifest=manifest,
            insights=[],
            presentation_label_space=presented,
        )
        self.assertIn(json.dumps(tuple(presented)), text)
        self.assertEqual(manifest["label_space"], canonical)
        with self.assertRaisesRegex(ContractError, "permutation"):
            render_diagnostic_prompt(
                agent_id="agent_1",
                condition="A",
                case={"neutral_text": "case"},
                manifest=manifest,
                insights=[],
                presentation_label_space=presented[:-1],
            )


class LedgerContractTests(unittest.TestCase):
    def make(self):
        temporary = tempfile.TemporaryDirectory()
        path = Path(temporary.name).resolve() / "pilot.sqlite3"
        return temporary, path, PilotLedger(path, pilot_id="phase03-test")

    @staticmethod
    def reserve(ledger: PilotLedger, index: int, *, stage="producer_conformity", run="c1"):
        ledger.reserve_request(request_id=f"r-{stage}-{index}", logical_id=f"l-{stage}-{index}",
                               model="model", producer="producer", stage=stage, stage_run=run)

    def complete_conformity(self, ledger: PilotLedger):
        for index in range(8):
            self.reserve(ledger, index)
            ledger.complete_request(f"r-producer_conformity-{index}", status="COMPLETED")
        ledger.record_stage_outcome("producer_conformity", outcome="PASS", artifact_sha256=H)

    def complete_probe(self, ledger: PilotLedger):
        for index in range(3):
            self.reserve(ledger, index, stage="budget_probe", run="p1")
            ledger.complete_request(f"r-budget_probe-{index}", status="COMPLETED")
        ledger.record_stage_outcome("budget_probe", outcome="PASS", artifact_sha256=H)

    def test_intent_survives_restart_and_directory_change(self):
        temporary, path, ledger = self.make()
        try:
            self.reserve(ledger, 0)
            reopened = PilotLedger(path, pilot_id="phase03-test")
            self.assertEqual(reopened.snapshot()["requests_cumulative"], 1)
            self.assertEqual(reopened.snapshot()["unresolved_intents"], 1)
            with self.assertRaisesRegex(HarnessError, "duplicate"):
                self.reserve(reopened, 0)
        finally:
            temporary.cleanup()

    def test_two_writers_cannot_duplicate_one_logical_attempt(self):
        temporary, path, _ = self.make()
        barrier = Barrier(2)

        def attempt(index: int) -> str:
            contender = PilotLedger(path, pilot_id="phase03-test")
            barrier.wait()
            try:
                contender.reserve_request(
                    request_id=f"concurrent-{index}", logical_id="same-logical-attempt",
                    model="model", producer="producer", stage="producer_conformity",
                    stage_run="concurrent-run",
                )
                return "accepted"
            except HarnessError:
                return "rejected"

        try:
            with ThreadPoolExecutor(max_workers=2) as executor:
                outcomes = list(executor.map(attempt, range(2)))
            self.assertEqual(sorted(outcomes), ["accepted", "rejected"])
            self.assertEqual(PilotLedger(path, pilot_id="phase03-test").snapshot()["requests_cumulative"], 1)
        finally:
            temporary.cleanup()

    def test_timeout_without_zero_token_proof_never_retries(self):
        temporary, _, ledger = self.make()
        try:
            self.reserve(ledger, 0)
            ledger.complete_request("r-producer_conformity-0", status="FAILED", detail={"error": "timeout"})
            with self.assertRaisesRegex(HarnessError, "zero-token proof"):
                ledger.reserve_transport_retry(request_id="retry", logical_id="retry-l", model="m", producer="p",
                                               stage="producer_conformity", stage_run="c1", retry_of="r-producer_conformity-0")
        finally:
            temporary.cleanup()

    def test_zero_token_proof_allows_only_documented_transport(self):
        temporary, _, ledger = self.make()
        try:
            self.reserve(ledger, 0)
            ledger.complete_request("r-producer_conformity-0", status="ZERO_TOKEN_PROVEN", completion_tokens=0,
                                    total_tokens=0, proof_sha256=H)
            ledger.reserve_transport_retry(request_id="retry", logical_id="retry-l", model="m", producer="p",
                                           stage="producer_conformity", stage_run="c1", retry_of="r-producer_conformity-0")
            self.assertEqual(ledger.snapshot()["transport_calls"], 1)
        finally:
            temporary.cleanup()

    def test_remediation_limits_and_stage_order(self):
        temporary, _, ledger = self.make()
        try:
            for index in range(8):
                self.reserve(ledger, index)
                ledger.complete_request(f"r-producer_conformity-{index}", status="COMPLETED")
            ledger.record_stage_outcome("producer_conformity", outcome="FAIL", artifact_sha256=H)
            ledger.authorize_remediation(diff_sha256=H, approval_sha256="b" * 64, template_sha256="c" * 64)
            for index in range(8):
                ledger.reserve_remediation_request(request_id=f"m{index}", logical_id=f"ml{index}", model="m",
                                                   producer="p", stage_run="rem1")
            with self.assertRaisesRegex(HarnessError, "at most one complete set"):
                ledger.reserve_remediation_request(request_id="m8", logical_id="ml8", model="m", producer="p", stage_run="rem1")
            with self.assertRaisesRegex(HarnessError, "create-once"):
                ledger.authorize_remediation(diff_sha256=H, approval_sha256="d" * 64, template_sha256="e" * 64)
        finally:
            temporary.cleanup()

    def test_zero_token_remediation_retry_counts_as_transport(self):
        temporary, _, ledger = self.make()
        try:
            for index in range(8):
                self.reserve(ledger, index)
                ledger.complete_request(f"r-producer_conformity-{index}", status="COMPLETED")
            ledger.record_stage_outcome("producer_conformity", outcome="FAIL", artifact_sha256=H)
            ledger.authorize_remediation(diff_sha256=H, approval_sha256="b" * 64, template_sha256="c" * 64)
            for index in range(8):
                ledger.reserve_remediation_request(
                    request_id=f"m{index}", logical_id=f"ml{index}", model="m",
                    producer="p", stage_run="rem1"
                )
                ledger.complete_request(
                    f"m{index}",
                    status="ZERO_TOKEN_PROVEN" if index == 0 else "COMPLETED",
                    total_tokens=0 if index == 0 else None,
                    proof_sha256=H if index == 0 else None,
                )
            ledger.reserve_transport_retry(
                request_id="m0-retry", logical_id="ml0-retry", model="m", producer="p",
                stage="producer_remediation", stage_run="rem1", retry_of="m0"
            )
            ledger.complete_request("m0-retry", status="COMPLETED")
            ledger.record_stage_outcome("producer_remediation", outcome="PASS", artifact_sha256=H)
            snapshot = ledger.snapshot()
            self.assertEqual(snapshot["remediation_calls"], 8)
            self.assertEqual(snapshot["transport_calls"], 1)
            self.assertEqual(snapshot["reserve_equation_value"], 9)
        finally:
            temporary.cleanup()

    def test_probe_triplet_retry_is_atomic_and_capped(self):
        temporary, _, ledger = self.make()
        try:
            self.complete_conformity(ledger)
            originals = []
            for index, condition in enumerate(("A", "B-LF", "E-LF")):
                self.reserve(ledger, index, stage="budget_probe", run="p1")
                request = f"r-budget_probe-{index}"
                ledger.complete_request(request, status="ZERO_TOKEN_PROVEN", total_tokens=0, proof_sha256=H)
                originals.append((request, condition))
            with self.assertRaisesRegex(HarnessError, "complete A/B-LF/E-LF triplet"):
                ledger.reserve_probe_transport_triplet([])
            def triplet(number):
                return [{"request_id": f"pt{number}-{i}", "logical_id": f"ptl{number}-{i}", "model": "m", "producer": "p",
                         "stage_run": "p1", "retry_of": original, "condition": condition}
                        for i, (original, condition) in enumerate(originals)]
            ledger.reserve_probe_transport_triplet(triplet(1))
            ledger.reserve_probe_transport_triplet(triplet(2))
            with self.assertRaisesRegex(HarnessError, "capped at seven"):
                ledger.reserve_probe_transport_triplet(triplet(3))
        finally:
            temporary.cleanup()

    def test_gate_is_not_repeatable_and_has_no_retry(self):
        temporary, _, ledger = self.make()
        try:
            self.complete_conformity(ledger)
            self.complete_probe(ledger)
            self.reserve(ledger, 0, stage="stability_gate", run="gate-one")
            with self.assertRaisesRegex(HarnessError, "create-once"):
                self.reserve(ledger, 1, stage="stability_gate", run="gate-two")
            ledger.complete_request("r-stability_gate-0", status="ZERO_TOKEN_PROVEN", total_tokens=0, proof_sha256=H)
            with self.assertRaisesRegex(HarnessError, "no retry|never repeatable"):
                ledger.reserve_transport_retry(request_id="g-retry", logical_id="g-retry-l", model="m", producer="p",
                                               stage="stability_gate", stage_run="gate-one", retry_of="r-stability_gate-0")
        finally:
            temporary.cleanup()


class GateRuleContractTests(unittest.TestCase):
    def test_forensic_differences_do_not_change_semantic_signature(self):
        left = gate_rows()[3]
        right = dict(left, raw_output_sha256="different", finish_reason="other")
        self.assertEqual(semantic_signature(left), semantic_signature(right))
        right["parsed_output"] = {"abstain": False, "predicted_label": "S2-CLS-3ZGWQ"}
        self.assertNotEqual(semantic_signature(left), semantic_signature(right))

    def test_114_valid_pass_t3_but_113_does_not(self):
        six = {(index, 0) for index in range(6)}
        seven = {(index, 0) for index in range(7)}
        self.assertTrue(evaluate_stability_gate(gate_rows(invalid=six))["t3_pass"])
        self.assertFalse(evaluate_stability_gate(gate_rows(invalid=seven))["t3_pass"])

    def test_mixed_validity_is_divergence_not_automatic_no_go(self):
        result = evaluate_stability_gate(gate_rows(invalid={(5, 0)}))
        self.assertIn("P-05", result["divergent_prompt_ids"])
        self.assertEqual(result["status"], "R3_REQUIRED_PENDING_FEASIBILITY")
        self.assertFalse(result["go_final"])

    def test_all_invalid_triplet_makes_t6_not_evaluable(self):
        result = evaluate_stability_gate(gate_rows(invalid={(5, 0), (5, 1), (5, 2)}))
        self.assertFalse(result["t6_evaluable"])
        self.assertEqual(result["status"], "NO_GO_TECHNICAL")
        self.assertIn("P-05", result["all_invalid_prompt_ids"])

    def test_length_truncation_fails_t4_separately(self):
        result = evaluate_stability_gate(gate_rows(truncate=(8, 1)))
        self.assertFalse(result["t4_pass"])
        self.assertTrue(result["t3_pass"])
        self.assertEqual(result["t5_temporal_feasibility"], "NOT_MEASURED_BY_OFFLINE_EVALUATION")


class PlanOnlyTests(unittest.TestCase):
    def test_plan_reports_rev10_without_claiming_d9_or_time(self):
        config = load_json(ROOT / "studio2/fase03/config/pilot_preflight.json")
        self.assertEqual(config["call_budget"]["planned_max_without_alternate"], 152)
        self.assertEqual(config["call_budget"]["planned_max_with_alternate"], 160)
        self.assertEqual(config["call_budget"]["hard_stop_provider_requests"], 200)
        self.assertEqual(config["study_model_decision"], "UNDECIDED")
        self.assertNotIn("parsed JSON", config["determinism_policy"]["divergence_event"])
        self.assertEqual(run_pilot.semantic_signature(gate_rows()[0]), semantic_signature(gate_rows()[0]))


if __name__ == "__main__":
    unittest.main()
