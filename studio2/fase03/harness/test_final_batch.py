"""Offline tests of the final-batch runner and of the daily canary.

SACRIFICIAL FIXTURES ONLY. No fixture is a scientific approval, a quota authorization or
a result. Every provider here is synthetic and no test ever opens a socket.
"""

from __future__ import annotations

from contextlib import ExitStack
import dataclasses
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from .common import HarnessError, sha256_text
from .ledger import (FINAL_BATCH_PROFILE, FINAL_CANARY_STAGE, FINAL_PASS_STAGES, PilotLedger,
                     digest)
from . import final_inventory
from studio2.fase03 import run_final_batch, run_final_canary

MODEL = "fixture-consumer-model"
FINGERPRINT = "fixture-0.0.0-000000"
LABELS = ["S2-CLS-AAAAA", "S2-CLS-BBBBB", "Normal"]
INSIGHTS = ["S2-INS-001", "S2-INS-002"]
SMALL = 6


def small_profile(rows_per_pass: int, canary_slots: int = 70):
    limits = {stage: rows_per_pass for stage in FINAL_PASS_STAGES}
    limits[FINAL_CANARY_STAGE] = canary_slots
    limits["technical_verification"] = 100
    total = sum(limits.values())
    return dataclasses.replace(FINAL_BATCH_PROFILE, base_limits=limits,
                               planned_maximum=total, hard_stop=total)


def fixture_config(ledger_path: Path, pilot_id: str) -> dict:
    return {
        "candidate": {"provider": "fixture", "requested_model": MODEL,
                      "expected_model_revision": "FIXTURE"},
        "expected_response": {"returned_model": MODEL, "system_fingerprint": FINGERPRINT},
        "pilot_ledger": {"path": str(ledger_path), "pilot_id": pilot_id},
        "call_budget": {"hard_stop_provider_requests": 10_000},
    }


def fixture_prompt(stable_id: str) -> dict:
    text = f"FIXTURE ONLY prompt {stable_id}"
    return {"prompt_id": stable_id, "text": text, "prompt_sha256": sha256_text(text),
            "agent_id": "agent_1", "case_id": "fixture-case", "condition": "A",
            "sample_role": "matched_transfer", "label_space": LABELS,
            "available_insight_ids": INSIGHTS}


def answer(*, abstain=False, label="Normal", reasoning="FIXTURE ONLY reasoning."):
    return json.dumps({"predicted_label": None if abstain else label, "abstain": abstain,
                       "used_insight_ids": [], "reasoning_summary": reasoning})


def envelope(content, *, model=MODEL, fingerprint=FINGERPRINT, usage=(11, 7)):
    prompt_tokens, completion_tokens = usage
    return {"id": "fixture-" + sha256_text(content)[:16], "model": model,
            "system_fingerprint": fingerprint,
            "choices": [{"finish_reason": "stop", "message": {"content": content}}],
            "usage": {"prompt_tokens": prompt_tokens, "completion_tokens": completion_tokens,
                      "total_tokens": prompt_tokens + completion_tokens}}


class FakeProvider:
    """Synthetic transport. Records every call and never touches the network."""

    script: dict = {}

    def __init__(self, config):
        self.config = config
        self.calls = []

    def call(self, *, prompt, schema, generation, messages=None, ledger=None, stage=None, spec=None):
        self.calls.append(spec["logical_id"])
        behaviour = self.script.get(spec["logical_id"], "valid")
        if behaviour == "raise":
            raise RuntimeError("FIXTURE ONLY transport failure")
        if behaviour == "invalid":
            return envelope("not json at all")
        if behaviour == "identity":
            return envelope(answer(), fingerprint="fixture-changed")
        if behaviour == "abstain":
            return envelope(answer(abstain=True))
        if behaviour == "canary-drift":
            return envelope(answer(label="S2-CLS-BBBBB"))
        return envelope(answer())


_PASS_BINDING = run_final_batch.pass_binding
_CANARY_BINDING = run_final_canary.canary_binding


def binding_without_config(rows, prompts, generation, *, config, target, schema, stage):
    """Sacrificial binding: a real execution_config requires the whole D9 approval chain."""
    value = _PASS_BINDING(rows, prompts, generation, config=config, target=target,
                          schema=schema, stage=stage)
    value.pop("execution_config")
    return value


def canary_binding_without_config(specs, *, config, schema, target):
    value = _CANARY_BINDING(specs, config=config, schema=schema, target=target)
    value.pop("execution_config")
    return value


class FinalBatchBase(unittest.TestCase):
    rows_per_pass = SMALL

    def setUp(self):
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.home = Path(self.stack.enter_context(tempfile.TemporaryDirectory()))
        self.pilot_id = "studio2-fase03-batch-fixture"
        self.ledger_path = self.home / "ledger.sqlite3"
        self.ledger = PilotLedger(self.ledger_path, pilot_id=self.pilot_id, profile="final_batch")
        self.ledger.profile = small_profile(self.rows_per_pass)
        self.config = fixture_config(self.ledger_path, self.pilot_id)
        self.generation = {"max_tokens": 2560, "seed": 20260829, "thinking_token_budget": 2048}
        self.schema = {"type": "object"}
        self.results = self.home / "results"
        self.schedule = self.make_schedule()
        self.prompts = {row["stable_id"]: fixture_prompt(row["stable_id"]) for row in self.schedule}
        self.target = {"schedule": {"sha256": "0" * 64}, "prompts": {"sha256": "1" * 64},
                       "canary_expectations": {"path": str(self.home / "canary.json"),
                                               "sha256": "2" * 64},
                       "tokenizer_snapshot": str(self.home), "generation": self.generation,
                       "results_dir": str(self.results)}
        FakeProvider.script = {}
        self.stack.enter_context(patch.object(run_final_batch, "pass_binding", binding_without_config))
        self.stack.enter_context(patch.object(run_final_canary, "canary_binding",
                                              canary_binding_without_config))
        self.install_canary_fixture()

    def make_schedule(self):
        rows = []
        for repetition in (1, 2, 3):
            for index in range(self.rows_per_pass):
                stable = f"nucleus|A|fixture-case-{index}|agent_1|none"
                rows.append({"position": len(rows) + 1, "repetition": repetition,
                             "stable_id": stable, "logical_id": f"{stable}|r{repetition}",
                             "block": "nucleus", "condition": "A",
                             "case_id": f"fixture-case-{index}", "recipient_agent": "agent_1",
                             "library_role": "none", "fault": "F1", "run_index": index + 1,
                             "locality": "local-unseen", "true_pseudolabel": "S2-CLS-AAAAA"})
        return rows

    def install_canary_fixture(self):
        self.canary_prompts = [dict(fixture_prompt(f"S2-P03-{index:03d}"),
                                    prompt_id=f"S2-P03-{index:03d}") for index in range(1, 11)]
        prompts_path = self.home / "canary_prompts.jsonl"
        prompts_path.write_text("".join(json.dumps(row) + "\n" for row in self.canary_prompts),
                                encoding="utf-8")
        expectations = {"artifact_version": "CANARY_ATTESI_7_4_1",
                        "expectations": [{"prompt_id": row["prompt_id"], "abstain": False,
                                          "predicted_label": "Normal",
                                          "prompt_sha256": row["prompt_sha256"],
                                          "raw_response_sha256": sha256_text(answer())}
                                         for row in self.canary_prompts]}
        expectations_path = self.home / "canary.json"
        expectations_path.write_text(json.dumps(expectations), encoding="utf-8")
        self.target["canary_expectations"] = {"path": str(expectations_path), "sha256": "2" * 64}
        self.target["canary_prompts"] = {"path": str(prompts_path), "sha256": "3" * 64}

    def run_day(self, day="2026-09-18"):
        return run_final_canary.run_day(
            target=self.target, ledger=self.ledger, config=self.config,
            generation=self.generation, schema=self.schema, day=day,
            results_dir=self.results, execute=True, provider_factory=FakeProvider)

    def pass_canary_day(self, day="2026-09-18"):
        outcome = self.run_day(day)
        assert outcome["verdict"] == "PASS", outcome
        return outcome

    def run_pass(self, pass_index=1, **kwargs):
        options = dict(target=self.target, ledger=self.ledger, schedule=self.schedule,
                       prompts=self.prompts, config=self.config, generation=self.generation,
                       schema=self.schema, pass_index=pass_index, results_dir=self.results,
                       execute=True, max_requests=None, provider_factory=FakeProvider)
        options.update(kwargs)
        return run_final_batch.run_pass(**options)


class BatchExecution(FinalBatchBase):
    def test_complete_small_batch_records_every_slot_once(self):
        self.pass_canary_day()
        summary = self.run_pass()
        self.assertEqual(summary["status"], "COMPLETE")
        self.assertEqual(summary["completed"], self.rows_per_pass)
        self.assertEqual(summary["sent_this_run"], self.rows_per_pass)
        self.assertEqual(summary["invalid"], 0)
        rows = self.ledger.snapshot()["requests_by_stage"]
        self.assertEqual(rows[FINAL_PASS_STAGES[0]], self.rows_per_pass)

    def test_interruption_and_resume_replay_the_same_schedule_without_resending(self):
        self.pass_canary_day()
        first = self.run_pass(max_requests=2)
        self.assertEqual(first["sent_this_run"], 2)
        self.assertEqual(first["status"], "PARTIAL")
        second = self.run_pass(resume=True)
        self.assertEqual(second["sent_this_run"], self.rows_per_pass - 2)
        self.assertEqual(second["completed"], self.rows_per_pass)
        stage = FINAL_PASS_STAGES[0]
        order = [json.loads(self.ledger.request(
            digest([self.pilot_id, stage, row["logical_id"]]))["identity_json"])["logical_id"]
            for row in self.schedule[:self.rows_per_pass]]
        self.assertEqual(order, [row["logical_id"] for row in self.schedule[:self.rows_per_pass]])

    def test_resume_is_explicit_and_never_implicit(self):
        self.pass_canary_day()
        self.run_pass(max_requests=1)
        with self.assertRaises(run_final_batch.BatchStop):
            self.run_pass()

    def test_terminal_invalid_response_is_never_replaced(self):
        self.pass_canary_day()
        FakeProvider.script = {self.schedule[1]["logical_id"]: "invalid"}
        summary = self.run_pass()
        self.assertEqual(summary["invalid"], 1)
        self.assertEqual(summary["completed"], self.rows_per_pass)
        again = self.run_pass(resume=True)
        self.assertEqual(again["sent_this_run"], 0)

    def test_zero_token_is_reconciled_and_not_resent(self):
        self.pass_canary_day()
        FakeProvider.script = {self.schedule[0]["logical_id"]: "raise"}
        with self.assertRaises(HarnessError):
            self.run_pass()
        stage = FINAL_PASS_STAGES[0]
        request_id = digest([self.pilot_id, stage, self.schedule[0]["logical_id"]])
        self.assertEqual(self.ledger.request(request_id)["status"], "FAILED")
        with self.assertRaises(run_final_batch.BatchStop):
            self.run_pass(resume=True)
        self.reconcile_zero_token(request_id)
        FakeProvider.script = {}
        summary = self.run_pass(resume=True)
        self.assertEqual(summary["sent_this_run"], self.rows_per_pass - 1)
        self.assertEqual(self.ledger.request(request_id)["status"], "ZERO_TOKEN_PROVEN")
        # The reconciled slot stays terminal and alone: Q=0 authorizes no replacement.
        self.assertEqual(self.ledger.snapshot()["requests_by_stage"][stage], self.rows_per_pass)
        self.assertEqual(self.ledger.leaf(stage, self.schedule[0]["logical_id"])["request_id"],
                         request_id)
        self.assertEqual(self.run_pass(resume=True)["sent_this_run"], 0)

    def reconcile_zero_token(self, request_id):
        row = self.ledger.request(request_id)
        evidence = {"request_id": request_id,
                    "request_identity_sha256": sha256_text(row["identity_json"]),
                    "disposition": "not_generated", "provider_request_id": "FIXTURE-" + request_id,
                    "provider_evidence": "SACRIFICIAL STUB REPORT",
                    "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
        evidence_path = self.home / f"evidence_{request_id[:8]}.json"
        evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
        from .common import sha256_file
        approval_path = self.home / f"approval_{request_id[:8]}.json"
        approval_path.write_text(json.dumps({"author": "FIXTURE ONLY", "decision": "accepted",
                                             "evidence_sha256": sha256_file(evidence_path)}),
                                 encoding="utf-8")
        self.ledger.reconcile_zero_token(request_id, evidence_path=evidence_path,
                                         approval_path=approval_path)

    def test_identity_suspension_stops_the_batch(self):
        self.pass_canary_day()
        FakeProvider.script = {self.schedule[2]["logical_id"]: "identity"}
        with self.assertRaises(HarnessError) as error:
            self.run_pass()
        self.assertIn("suspended", str(error.exception))

    def test_stage_quota_exhaustion_stops_the_batch(self):
        self.pass_canary_day()
        self.ledger.profile = small_profile(self.rows_per_pass)
        narrow = dataclasses.replace(self.ledger.profile,
                                     base_limits=dict(self.ledger.profile.base_limits))
        narrow.base_limits[FINAL_PASS_STAGES[0]] = self.rows_per_pass
        self.ledger.profile = narrow
        self.run_pass()
        # The binding is exactly the stage quota: one further slot cannot be reserved.
        with self.assertRaises(HarnessError):
            self.ledger.reserve_request(
                request_id="extra", logical_id=self.schedule[0]["logical_id"],
                model=MODEL, producer="consumer", stage=FINAL_PASS_STAGES[0],
                stage_run=digest(self.ledger.binding(FINAL_PASS_STAGES[0])))

    def test_batch_without_a_passed_canary_is_refused(self):
        # The ledger refuses the binding before the runner even reaches its own check.
        with self.assertRaises(HarnessError) as error:
            self.run_pass()
        self.assertIn("canary", str(error.exception))

    def test_second_marked_canary_day_blocks_the_batch(self):
        self.pass_canary_day("2026-09-18")
        FakeProvider.script = {f"canary:day2:{self.canary_prompts[0]['prompt_id']}": "canary-drift"}
        self.run_day("2026-09-19")
        FakeProvider.script = {f"canary:day3:{self.canary_prompts[1]['prompt_id']}": "canary-drift"}
        with self.assertRaises(run_final_canary.BatchStop):
            self.run_day("2026-09-20")
        FakeProvider.script = {}
        with self.assertRaises(HarnessError) as error:
            self.run_pass()
        self.assertIn("canary STOP", str(error.exception))

    def test_pass_two_cannot_start_before_pass_one_is_closed(self):
        self.pass_canary_day()
        self.run_pass(1)
        with self.assertRaises(HarnessError):
            self.run_pass(2)


class ScheduleContract(unittest.TestCase):
    def test_counts_match_protocol_section_five(self):
        inventory = final_inventory.build_inventory()
        counts = final_inventory.verify_counts(inventory)
        self.assertEqual(counts["unique_total"], 2244)
        self.assertEqual(counts["unique_by_block"],
                         {"nucleus": 1728, "producer_swap": 224, "ablation_b_no_lf": 148, "ood": 144})
        self.assertEqual(counts["requests_total"], 6732)

    def test_schedule_is_reproducible_and_covers_each_prompt_three_times(self):
        inventory = final_inventory.build_inventory()
        first = final_inventory.build_schedule(inventory)
        second = final_inventory.build_schedule(final_inventory.build_inventory())
        self.assertEqual(first, second)
        from collections import Counter
        repetitions = Counter(row["repetition"] for row in first)
        self.assertEqual(dict(repetitions), {1: 2244, 2: 2244, 3: 2244})
        self.assertEqual(len({row["logical_id"] for row in first}), 6732)

    def test_unsupported_condition_is_refused_rather_than_reinterpreted(self):
        schedule = [{"condition": "B-noLF", "stable_id": "x", "logical_id": "x|r1"}]
        with self.assertRaises(run_final_batch.BatchStop):
            run_final_batch.executable_rows(schedule, {"x": {}})


class CanaryDay(FinalBatchBase):
    def test_passing_day_is_recorded_and_unlocks_the_batch(self):
        outcome = self.run_day()
        self.assertEqual(outcome["verdict"], "PASS")
        self.assertFalse(outcome["marked"])
        self.assertEqual(self.ledger.snapshot()["requests_by_stage"][FINAL_CANARY_STAGE], 10)
        self.assertEqual(self.run_pass()["status"], "COMPLETE")

    def test_behavioural_drift_marks_the_day_and_two_marks_stop_the_batch(self):
        FakeProvider.script = {f"canary:day1:{self.canary_prompts[0]['prompt_id']}": "canary-drift"}
        first = self.run_day("2026-09-18")
        self.assertTrue(first["marked"])
        self.assertEqual(first["verdict"], "MARKED")
        FakeProvider.script = {f"canary:day2:{self.canary_prompts[1]['prompt_id']}": "canary-drift"}
        with self.assertRaises(run_final_canary.BatchStop):
            self.run_day("2026-09-19")
        FakeProvider.script = {}
        with self.assertRaises(HarnessError) as error:
            self.run_pass()
        self.assertIn("canary STOP", str(error.exception))

    def test_identity_change_stops_before_any_further_call(self):
        FakeProvider.script = {f"canary:day1:{self.canary_prompts[3]['prompt_id']}": "identity"}
        with self.assertRaises(run_final_canary.BatchStop):
            self.run_day()
        self.assertTrue(any(event.startswith("canary_stop:identity")
                            for event in self.ledger.snapshot()["events"]))
        with self.assertRaises(HarnessError):
            self.run_pass()


if __name__ == "__main__":
    unittest.main()
