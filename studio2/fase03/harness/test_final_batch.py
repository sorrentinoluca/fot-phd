"""Offline tests of the final-batch runner and of the daily canary.

SACRIFICIAL FIXTURES ONLY. No fixture is a scientific approval, a quota authorization or
a result. Every provider here is synthetic and no test ever opens a socket.
"""

from __future__ import annotations

from contextlib import ExitStack
import dataclasses
from datetime import datetime
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from .common import HarnessError, sha256_file, sha256_text
from .ledger import (FINAL_BATCH_PROFILE, FINAL_CANARY_STAGE, FINAL_PASS_STAGES, PilotLedger,
                     digest)
from . import canary_marking, final_inventory
from studio2.fase03 import run_final_batch, run_final_canary

MODEL = "fixture-consumer-model"
FINGERPRINT = "fixture-0.0.0-000000"
LABELS = ["S2-CLS-AAAAA", "S2-CLS-BBBBB", "Normal"]
INSIGHTS = ["S2-INS-001", "S2-INS-002"]
SMALL = 6


def small_profile(rows_per_pass: int, canary_slots: int = 300):
    limits = {stage: rows_per_pass for stage in FINAL_PASS_STAGES}
    limits[FINAL_CANARY_STAGE] = canary_slots
    limits["technical_verification"] = FINAL_BATCH_PROFILE.base_limits["technical_verification"]
    total = sum(limits.values()) + FINAL_BATCH_PROFILE.retry_quota
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
    """A rendered row with exactly the keys ``final_prompts.render_all`` writes.

    No ``label_space`` and no ``sample_role``: both are bound by ``load_prompts``. Twice a
    fixture added by hand a field the renderer does not emit, and twice the real campaign
    paid a call to find out (7.4-FIX-RUNNER, 7.4-FIX-CONTRATTO-RECORD). The key set is
    asserted against ``RENDERED_ROW_KEYS`` in ``test_record_contract``.
    """
    from .final_prompts import RENDERED_ROW_KEYS
    text = f"FIXTURE ONLY prompt {stable_id}"
    row = {"prompt_id": stable_id, "stable_id": stable_id, "block": "nucleus", "condition": "A",
           "case_id": "fixture-case", "agent_id": "agent_1", "library_role": "none",
           "available_insight_ids": INSIGHTS, "text": text, "prompt_sha256": sha256_text(text),
           "prompt_bytes": len(text.encode("utf-8"))}
    assert tuple(row) == RENDERED_ROW_KEYS, "fixture row drifted from the renderer"
    return row


def fixture_pilot_prompt(prompt_id: str) -> dict:
    """A pilot row (``protocol.RenderedPrompt.to_dict``): what ``canary_prompts.jsonl`` holds.

    Built through the production dataclass, so a pilot field added or removed there changes
    this fixture with it. It carries ``sample_role`` because the pilot sampled its cases;
    it carries no ``label_space``.
    """
    from studio2.fase03.protocol import RenderedPrompt
    text = f"FIXTURE ONLY prompt {prompt_id}"
    return RenderedPrompt(prompt_id=prompt_id, agent_id="agent_1", case_id="fixture-case",
                          condition="A", sample_role="matched_transfer", text=text,
                          prompt_sha256=sha256_text(text),
                          available_insight_ids=tuple(INSIGHTS), input_tokens=5).to_dict()


def install_frozen_manifest(stack, home: Path) -> Path:
    """A sacrificial stand-in for the frozen pilot input manifest, authenticated as the real one."""
    from . import final_prompts as final_prompts_module
    path = home / "pilot" / "execution" / "PILOT_INPUT_MANIFEST.frozen.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"artifact_version": "FIXTURE", "label_space": LABELS}),
                    encoding="utf-8")
    stack.enter_context(patch.object(final_prompts_module, "PILOT_INPUT_MANIFEST_SHA256",
                                     sha256_file(path)))
    stack.enter_context(patch.object(run_final_batch, "pilot_manifest_path",
                                     lambda target, override=None: Path(override or path)))
    return path


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
        self.manifest_path = install_frozen_manifest(self.stack, self.home)
        self.prompts_path = self.home / "final_prompts.jsonl"
        self.prompts_path.write_text(
            "".join(json.dumps(fixture_prompt(row["stable_id"])) + "\n"
                    for row in self.schedule if row["repetition"] == 1), encoding="utf-8")
        self.target = {"schedule": {"sha256": "0" * 64},
                       "prompts": {"sha256": "1" * 64, "path": str(self.prompts_path)},
                       "canary_expectations": {"path": str(self.home / "canary.json"),
                                               "sha256": "2" * 64},
                       "tokenizer_snapshot": str(self.home), "generation": self.generation,
                       "results_dir": str(self.results)}
        # The loader binds the label space, exactly as the command does before any call.
        self.prompts = run_final_batch.load_prompts(
            self.target, label_space=run_final_batch.target_label_space(self.target))
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
        self.canary_prompts = [fixture_pilot_prompt(f"S2-P03-{index:03d}") for index in range(1, 11)]
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

    @staticmethod
    def noon(day):
        """A UTC instant whose Europe/Rome civil day is exactly ``day``."""
        return datetime.fromisoformat(day + "T10:00:00+00:00")

    def run_day(self, day="2026-09-18", now=None):
        return run_final_canary.run_day(
            target=self.target, ledger=self.ledger, config=self.config,
            generation=self.generation, schema=self.schema, day=day,
            results_dir=self.results, execute=True, provider_factory=FakeProvider,
            now=now if now is not None else self.noon(day))

    def pass_canary_day(self, day="2026-09-18"):
        outcome = self.run_day(day)
        assert outcome["verdict"] == "PASS", outcome
        return outcome

    def run_pass(self, pass_index=1, **kwargs):
        options = dict(target=self.target, ledger=self.ledger, schedule=self.schedule,
                       prompts=self.prompts, config=self.config, generation=self.generation,
                       schema=self.schema, pass_index=pass_index, results_dir=self.results,
                       execute=True, max_requests=None, provider_factory=FakeProvider,
                       day="2026-09-18")
        options.update(kwargs)
        options.setdefault("now", self.noon(options["day"]) if options["day"] else None)
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

    def test_uncertain_transport_is_suspended_and_never_resent_automatically(self):
        """D3 row 2: a failure without proof suspends the slot; no automatic resend."""
        self.pass_canary_day()
        FakeProvider.script = {self.schedule[0]["logical_id"]: "raise"}
        with self.assertRaises(HarnessError):
            self.run_pass()
        stage = FINAL_PASS_STAGES[0]
        request_id = digest([self.pilot_id, stage, self.schedule[0]["logical_id"]])
        self.assertEqual(self.ledger.request(request_id)["status"], "FAILED")
        FakeProvider.script = {}
        with self.assertRaises(run_final_batch.BatchStop):
            self.run_pass(resume=True)
        self.assertEqual(self.ledger.snapshot()["requests_by_stage"][stage], 1)

    def test_proven_zero_token_is_retried_once_within_the_separate_quota(self):
        """D3 row 1: the only admitted retry, after proof linked to the request."""
        self.pass_canary_day()
        FakeProvider.script = {self.schedule[0]["logical_id"]: "raise"}
        with self.assertRaises(HarnessError):
            self.run_pass()
        stage = FINAL_PASS_STAGES[0]
        logical_id = self.schedule[0]["logical_id"]
        request_id = digest([self.pilot_id, stage, logical_id])
        self.reconcile_zero_token(request_id)
        self.assertEqual(self.ledger.request(request_id)["status"], "ZERO_TOKEN_PROVEN")
        FakeProvider.script = {}
        waits = []
        summary = self.run_pass(resume=True, sleep=waits.append)
        self.assertEqual(summary["retries_this_run"], 1)
        self.assertEqual(waits, [run_final_batch.RETRY_BACKOFF_BASE_SECONDS])
        self.assertEqual(summary["completed"], self.rows_per_pass)
        # The retry lives on its own quota: the scientific slots stay at one per row.
        snapshot = self.ledger.snapshot()
        self.assertEqual(snapshot["requests_by_stage"][stage], self.rows_per_pass + 1)
        self.assertEqual(snapshot["retry_quota_used"], 1)
        self.assertEqual(snapshot["retry_quota"], 400)
        leaf = self.ledger.leaf(stage, logical_id)
        self.assertEqual(leaf["retry_of"], request_id)
        self.assertEqual(leaf["status"], "COMPLETED")
        self.assertEqual(self.run_pass(resume=True)["sent_this_run"], 0)

    def test_a_retry_never_consumes_a_scientific_stage_slot(self):
        self.pass_canary_day()
        FakeProvider.script = {self.schedule[0]["logical_id"]: "raise"}
        with self.assertRaises(HarnessError):
            self.run_pass()
        stage = FINAL_PASS_STAGES[0]
        request_id = digest([self.pilot_id, stage, self.schedule[0]["logical_id"]])
        self.reconcile_zero_token(request_id)
        FakeProvider.script = {}
        self.run_pass(resume=True, sleep=lambda _: None)
        base = [row for row in self.ledger.attempts(stage, self.schedule[0]["logical_id"])
                if row["retry_of"] is None]
        self.assertEqual(len(base), 1)

    def failing_cycle(self, index, *, first):
        """One technical failure on the same logical row, then its zero-token proof."""
        stage = FINAL_PASS_STAGES[0]
        logical_id = self.schedule[0]["logical_id"]
        with self.assertRaises(HarnessError):
            self.run_pass(resume=not first, sleep=lambda _: None)
        leaf = self.ledger.leaf(stage, logical_id)
        self.assertEqual(leaf["status"], "FAILED")
        self.reconcile_zero_token(leaf["request_id"])

    def test_five_consecutive_technical_failures_stop_the_campaign(self):
        """D3: persistent per-service counter, retries included, threshold five."""
        self.pass_canary_day()
        FakeProvider.script = {self.schedule[0]["logical_id"]: "raise"}
        for index in range(4):
            self.failing_cycle(index, first=index == 0)
        self.assertEqual(max(self.ledger.consecutive_technical_failures().values()), 4)
        self.assertFalse(self.ledger.technical_failure_stop())
        self.failing_cycle(4, first=False)
        self.assertEqual(max(self.ledger.consecutive_technical_failures().values()), 5)
        self.assertTrue(self.ledger.technical_failure_stop())
        FakeProvider.script = {}
        with self.assertRaisesRegex(HarnessError, "consecutive technical"):
            self.run_pass(resume=True, sleep=lambda _: None)

    def test_the_failure_counter_survives_reopening_the_ledger(self):
        self.pass_canary_day()
        stage = FINAL_PASS_STAGES[0]
        FakeProvider.script = {self.schedule[0]["logical_id"]: "raise"}
        with self.assertRaises(HarnessError):
            self.run_pass()
        before = self.ledger.consecutive_technical_failures()
        reopened = PilotLedger(self.ledger.path, pilot_id=self.pilot_id, profile="final_batch")
        self.assertEqual(reopened.consecutive_technical_failures(), before)
        self.assertEqual(max(before.values()), 1)

    def test_a_completed_call_resets_the_service_counter(self):
        self.pass_canary_day()
        stage = FINAL_PASS_STAGES[0]
        FakeProvider.script = {self.schedule[0]["logical_id"]: "raise"}
        with self.assertRaises(HarnessError):
            self.run_pass()
        request_id = digest([self.pilot_id, stage, self.schedule[0]["logical_id"]])
        self.reconcile_zero_token(request_id)
        FakeProvider.script = {}
        self.run_pass(resume=True, sleep=lambda _: None)
        self.assertEqual(max(self.ledger.consecutive_technical_failures().values()), 0)

    def test_technical_verification_is_closed_at_x_zero(self):
        """X = 0: the stage exists, its quota is zero, every call on it is refused."""
        from .ledger import FINAL_BATCH_PROFILE as real

        self.assertEqual(real.base_limits["technical_verification"], 0)
        self.assertEqual(real.planned_maximum, 7432)
        self.assertEqual(real.hard_stop, 7432)
        self.assertEqual(sum(real.base_limits.values()) + real.retry_quota, 7432)
        self.pass_canary_day()
        binding = {"requests": [dict(logical_id="tv-1", model=MODEL, producer="consumer",
                                     prompt_sha256="0" * 64, case_sha256="1" * 64,
                                     contract_sha256="2" * 64, condition="A", group="g",
                                     repetition=1)],
                   "stage": "technical_verification"}
        # The stage cannot even be bound: a plan of any size exceeds a quota of zero.
        with self.assertRaises(HarnessError):
            self.ledger.bind_stage("technical_verification", binding)
        self.assertNotIn("technical_verification",
                         [row for row in self.ledger.snapshot()["requests_by_stage"]
                          if self.ledger.snapshot()["requests_by_stage"][row]])

    def test_the_total_ceiling_is_refused_on_its_own_path(self):
        """B6: the refusal on the overall maximum, not only the per-stage one."""
        from .ledger import FINAL_BATCH_PROFILE as real

        self.assertEqual(real.planned_maximum, real.hard_stop)
        self.assertEqual(real.planned_maximum, 7432)
        self.assertEqual(sum(real.base_limits.values()) + real.retry_quota, 7432)
        self.pass_canary_day()
        # Per-stage quotas stay wide; only the total is narrow, so the refusal can come
        # from the total branch alone, which 7.432 would reach after the whole campaign.
        # The total counts every request of the target, the ten canary calls included.
        already = sum(self.ledger.snapshot()["requests_by_stage"].values())
        admitted = self.rows_per_pass - 1
        total = already + admitted
        self.ledger.profile = dataclasses.replace(
            self.ledger.profile, planned_maximum=total, hard_stop=total + 10)
        with self.assertRaisesRegex(HarnessError, f"planned request maximum {total} reached"):
            self.run_pass()
        self.assertEqual(self.ledger.snapshot()["requests_by_stage"][FINAL_PASS_STAGES[0]],
                         admitted)
        # The cumulative hard stop answers on its own branch, before the planned maximum.
        self.ledger.profile = dataclasses.replace(
            self.ledger.profile, planned_maximum=total + 10, hard_stop=total)
        with self.assertRaisesRegex(HarnessError, f"cumulative hard stop {total} reached"):
            self.run_pass(resume=True)

    def test_retry_backoff_increases_and_is_capped(self):
        waits = [run_final_batch.retry_backoff_seconds(n) for n in range(1, 8)]
        self.assertEqual(waits[:4], [30.0, 60.0, 120.0, 240.0])
        self.assertEqual(waits, sorted(waits))
        self.assertLessEqual(max(waits), run_final_batch.RETRY_BACKOFF_CAP_SECONDS)
        self.assertEqual(run_final_batch.retry_backoff_seconds(0), 0.0)

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

    def test_the_four_protocol_arms_are_renderable(self):
        for condition in ("A", "B-LF", "E-LF", "B-noLF"):
            schedule = [{"condition": condition, "stable_id": "x", "logical_id": "x|r1"}]
            run_final_batch.executable_rows(schedule, {"x": {}})

    def test_an_unknown_condition_is_refused_rather_than_reinterpreted(self):
        schedule = [{"condition": "B-noLocalFirst", "stable_id": "x", "logical_id": "x|r1"}]
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


class CivilDayBinding(FinalBatchBase):
    """B1: the declared day is bound to the clock, and both values are persisted."""

    def test_a_lot_declared_for_another_day_is_refused(self):
        self.pass_canary_day("2026-09-18")
        with self.assertRaisesRegex(run_final_batch.BatchStop,
                                    "declared day 2026-09-18 differs from the observed"):
            self.run_pass(day="2026-09-18", now=self.noon("2026-09-20"))

    def test_a_lot_that_crosses_midnight_continues_and_is_flagged(self):
        self.pass_canary_day("2026-09-18")
        first = self.run_pass(day="2026-09-18", max_requests=2)
        self.assertFalse(first["midnight_crossing"])
        # The clock moves to the next day; the stage already ran on the declared day.
        second = self.run_pass(day="2026-09-18", resume=True,
                               now=datetime.fromisoformat("2026-09-19T00:30:00+01:00"))
        self.assertTrue(second["midnight_crossing"])
        self.assertEqual(second["declared_day"], "2026-09-18")
        self.assertEqual(second["observed_day"], "2026-09-19")
        self.assertEqual(second["status"], "COMPLETE")

    def test_the_crossing_is_refused_without_evidence_that_the_lot_began_that_day(self):
        self.pass_canary_day("2026-09-18")
        with self.assertRaisesRegex(run_final_batch.BatchStop,
                                    "differs from the observed Europe/Rome day 2026-09-19"):
            self.run_pass(day="2026-09-18", now=self.noon("2026-09-19"))

    def test_the_crossing_never_reaches_a_second_day(self):
        self.pass_canary_day("2026-09-18")
        self.run_pass(day="2026-09-18", max_requests=2)
        with self.assertRaises(run_final_batch.BatchStop):
            self.run_pass(day="2026-09-18", resume=True, now=self.noon("2026-09-20"))

    def test_both_days_are_persisted_in_every_batch_record(self):
        self.pass_canary_day("2026-09-18")
        self.run_pass(day="2026-09-18")
        stage = FINAL_PASS_STAGES[0]
        leaf = self.ledger.leaf(stage, self.schedule[0]["logical_id"])
        record = self.ledger.response(leaf["request_id"])["record"]
        self.assertEqual(record["declared_day"], "2026-09-18")
        self.assertEqual(record["observed_day"], "2026-09-18")
        self.assertIs(record["midnight_crossing"], False)

    def test_a_canary_never_crosses_midnight(self):
        with self.assertRaisesRegex(run_final_batch.BatchStop,
                                    "differs from the observed Europe/Rome day 2026-09-19"):
            self.run_day("2026-09-18", now=self.noon("2026-09-19"))
        self.assertFalse([event for event in self.ledger.snapshot()["events"]
                          if event.startswith("canary_")])

    def test_both_days_are_persisted_in_the_canary_event(self):
        outcome = self.pass_canary_day("2026-09-18")
        self.assertEqual(outcome["declared_day"], "2026-09-18")
        self.assertEqual(outcome["observed_day"], "2026-09-18")
        detail = self.ledger.event("canary_pass:2026-09-18")
        self.assertEqual(detail["declared_day"], "2026-09-18")
        self.assertEqual(detail["observed_day"], "2026-09-18")

    def test_the_ledger_refuses_a_canary_day_that_contradicts_the_clock(self):
        """Belt and braces: the fail-closed layer repeats the check of the runner."""
        self.pass_canary_day("2026-09-18")
        with self.assertRaisesRegex(HarnessError, "never crosses midnight"):
            self.ledger.record_canary_day("2026-09-19", verdict="PASS",
                                          comparison={"marked_day": False},
                                          expectations_sha256="2" * 64,
                                          observed_day="2026-09-20")

    def test_an_invalid_day_string_is_refused(self):
        with self.assertRaisesRegex(run_final_batch.BatchStop, "is not an ISO civil date"):
            run_final_batch.resolve_civil_day("18-09-2026", now=self.noon("2026-09-18"))


class RomeDayWithoutTzdata(unittest.TestCase):
    """B5: no tzdata, no guess."""

    def test_rome_day_refuses_when_the_time_zone_database_is_missing(self):
        import builtins

        real_import = builtins.__import__

        def without_zoneinfo(name, *args, **kwargs):
            if name == "zoneinfo":
                raise ImportError("FIXTURE ONLY: no tzdata")
            return real_import(name, *args, **kwargs)

        with patch.object(builtins, "__import__", without_zoneinfo):
            with self.assertRaisesRegex(HarnessError, "requires the IANA time-zone database"):
                canary_marking.rome_day(datetime.fromisoformat("2026-10-26T00:30:00+00:00"))

    def test_rome_day_is_exact_across_the_2026_dst_switch(self):
        # The old fallback used 27 October; the real switch is on the 25th.
        self.assertEqual(
            canary_marking.rome_day(datetime.fromisoformat("2026-10-25T23:30:00+00:00")),
            "2026-10-26")
        self.assertEqual(
            canary_marking.rome_day(datetime.fromisoformat("2026-10-24T23:30:00+00:00")),
            "2026-10-25")


if __name__ == "__main__":
    unittest.main()


class CanaryBarrierAndMarking(FinalBatchBase):
    """§6 barrier, persisted identity, C4 marking and C5 invalid-canary handling."""

    def test_a_lot_is_refused_on_a_day_whose_canary_has_not_passed(self):
        self.pass_canary_day("2026-09-18")
        with self.assertRaisesRegex(run_final_batch.BatchStop, "no canary PASS recorded for 2026-09-19"):
            self.run_pass(day="2026-09-19")
        self.assertEqual(self.run_pass(day="2026-09-18")["status"], "COMPLETE")

    def test_the_barrier_is_checked_before_every_request_not_only_at_the_start(self):
        self.pass_canary_day("2026-09-18")
        state = run_final_batch.require_canary_ok(self.ledger, "2026-09-18")
        self.assertEqual(state["barrier_day"], "2026-09-18")
        with self.assertRaises(run_final_batch.BatchStop):
            run_final_batch.require_canary_ok(self.ledger, "2026-09-20")

    def test_identity_of_every_canary_call_is_persisted_with_the_verdict(self):
        outcome = self.pass_canary_day("2026-09-18")
        self.assertEqual(len(outcome["identity"]), 10)
        detail = self.ledger.event("canary_pass:2026-09-18")
        self.assertEqual(len(detail["identity"]), 10)
        for value in detail["identity"].values():
            self.assertEqual(value["returned_model"], MODEL)
            self.assertEqual(value["system_fingerprint"], FINGERPRINT)

    def test_a_fingerprint_change_stops_the_canary_and_is_persisted(self):
        FakeProvider.script = {"canary:day1:S2-P03-004": "identity"}
        with self.assertRaises(run_final_batch.BatchStop):
            self.run_day("2026-09-18")
        stops = [event for event in self.ledger.snapshot()["events"]
                 if event.startswith("canary_stop:")]
        self.assertEqual(len(stops), 1)
        detail = self.ledger.event(stops[0])
        self.assertIn("identity", detail["detail"])
        with self.assertRaises(HarnessError):
            self.run_pass(day="2026-09-18")

    def test_an_invalid_canary_response_leaves_the_day_unclosed(self):
        """C5 under D3: received but invalid; never regenerated, the day cannot close."""
        FakeProvider.script = {"canary:day1:S2-P03-006": "invalid"}
        with self.assertRaisesRegex(run_final_batch.BatchStop, "invalid responses"):
            self.run_day("2026-09-18")
        events = self.ledger.snapshot()["events"]
        self.assertFalse([event for event in events if event.startswith("canary_pass:")])
        self.assertFalse([event for event in events if event.startswith("canary_marked:")])
        with self.assertRaisesRegex(HarnessError, "requires a passed canary day"):
            self.run_pass(day="2026-09-18")
        self.assertTrue((self.results / "canary_2026-09-18_invalid.json").is_file())

    def test_an_invalid_canary_call_is_not_resent_when_the_day_is_retried(self):
        FakeProvider.script = {"canary:day1:S2-P03-006": "invalid"}
        with self.assertRaises(run_final_batch.BatchStop):
            self.run_day("2026-09-18")
        before = self.ledger.snapshot()["requests_by_stage"][FINAL_CANARY_STAGE]
        FakeProvider.script = {}
        with self.assertRaises(run_final_batch.BatchStop):
            self.run_day("2026-09-18")
        after = self.ledger.snapshot()["requests_by_stage"][FINAL_CANARY_STAGE]
        self.assertEqual(before, after)

    def test_marking_is_empty_while_every_canary_passes(self):
        self.pass_canary_day("2026-09-18")
        self.run_pass(day="2026-09-18")
        value = canary_marking.marking(self.ledger)
        self.assertEqual(value["failed_canaries"], [])
        self.assertEqual(value["primary_mask_requests"], 0)
        self.assertEqual(value["forensic_mask_requests"], 0)
        self.assertEqual(value["union_descriptive_requests"], 0)
        self.assertEqual(value["scientific_requests"], self.rows_per_pass)

    def test_a_marked_day_marks_the_lots_that_precede_it_and_those_of_the_day(self):
        self.pass_canary_day("2026-09-18")
        self.run_pass(day="2026-09-18")
        FakeProvider.script = {f"canary:day2:{row['prompt_id']}": "canary-drift"
                               for row in self.canary_prompts[:3]}
        outcome = self.run_day("2026-09-19")
        self.assertEqual(outcome["verdict"], "MARKED")
        value = canary_marking.marking(self.ledger)
        self.assertEqual(value["failed_canaries"], ["2026-09-19"])
        # B2: the two masks are named and kept apart; the union is descriptive only.
        self.assertNotIn("marked_request_ids", value)
        self.assertEqual(value["forensic_mask_requests"], self.rows_per_pass)
        self.assertEqual(value["forensic_mask_source"],
                         "PROTOCOLLO_FINALE_CANDIDATE.md §6.5 — exposure interval")
        self.assertEqual(value["primary_mask_source"],
                         "PIANO_STATISTICO.md §10.5 — marked civil day")
        self.assertEqual(
            set(value["union_descriptive_request_ids"]),
            set(value["primary_mask_request_ids"]) | set(value["forensic_mask_request_ids"]))
        self.assertIn("descriptive", value["union_scope"])
        self.assertEqual(value["intervals"][0]["after_last_passed_canary"], "2026-09-18")
        self.assertTrue(value["equivalent_sql"])

    def test_marking_is_read_only_over_terminal_records(self):
        self.pass_canary_day("2026-09-18")
        self.run_pass(day="2026-09-18")
        FakeProvider.script = {f"canary:day2:{row['prompt_id']}": "canary-drift"
                               for row in self.canary_prompts[:3]}
        self.run_day("2026-09-19")
        before = self.ledger.snapshot()
        canary_marking.marking(self.ledger)
        self.assertEqual(self.ledger.snapshot(), before)
