"""The two things the first real canary day proved were untested.

1. The label space is not in a rendered prompt row: the loaders bind it from the frozen
   manifest. A fixture that adds it by hand hides the gap, which is how a KeyError landed
   *after* a paid call.
2. An ``INTENT`` slot whose raw response is already durable is not uncertain consumption:
   it closes by evaluating the stored bytes, with no transport. Uncertainty without a
   stored raw keeps D3 row 2 exactly as it was.

SACRIFICIAL FIXTURES ONLY: no approval here is scientific and no test opens a socket.
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import patch

from .common import HarnessError
from .ledger import FINAL_CANARY_STAGE, FINAL_PASS_STAGES, digest
from . import final_prompts as final_prompts_module
from . import test_final_batch as base
from studio2.fase03 import run_final_batch, run_final_canary, run_pilot


# Captured before any fixture patches it: the real default-path derivation.
REAL_MANIFEST_PATH = run_final_batch.pilot_manifest_path


class RefusingProvider:
    """Any transport attempt is a test failure: the recovery must consume no call."""

    def __init__(self, config):
        self.config = config

    def call(self, **_):
        raise AssertionError("the recovery from a stored response must not call the model")


class LabelSpaceBinding(base.FinalBatchBase):
    def test_a_rendered_row_carries_no_label_space_and_the_loader_binds_it(self):
        raw = [line for line in self.prompts_path.read_text(encoding="utf-8").splitlines() if line]
        self.assertTrue(raw)
        for line in raw:
            self.assertNotIn("label_space", line)
        for prompt in self.prompts.values():
            self.assertEqual(prompt["label_space"], base.LABELS)
            self.assertEqual(prompt["available_insight_ids"], base.INSIGHTS)

    def test_a_manifest_that_is_not_the_frozen_one_is_refused(self):
        with patch.object(final_prompts_module, "PILOT_INPUT_MANIFEST_SHA256", "0" * 64):
            with self.assertRaises(run_final_batch.BatchStop) as caught:
                run_final_batch.target_label_space(self.target)
        self.assertIn("label space", str(caught.exception))

    def test_a_missing_manifest_is_refused(self):
        with patch.object(run_final_batch, "pilot_manifest_path",
                          lambda target, override=None: self.home / "absent.json"):
            with self.assertRaises(run_final_batch.BatchStop):
                run_final_batch.target_label_space(self.target)

    def test_the_default_path_sits_beside_the_tokenizer_snapshot(self):
        target = {"tokenizer_snapshot": "/runtime/pilot-03/tokenizers/abcdef"}
        self.assertEqual(REAL_MANIFEST_PATH(target),
                         Path("/runtime/pilot-03/execution/PILOT_INPUT_MANIFEST.frozen.json"))
        self.assertEqual(REAL_MANIFEST_PATH(target, "/elsewhere/m.json"), Path("/elsewhere/m.json"))

    def test_a_canary_day_runs_from_prompts_that_carry_no_label_space(self):
        outcome = self.pass_canary_day()
        self.assertEqual(outcome["verdict"], "PASS")
        self.assertEqual(len(outcome["identity"]), 10)

    def test_the_canary_plan_stops_before_any_call_when_the_manifest_is_absent(self):
        with patch.object(run_final_batch, "pilot_manifest_path",
                          lambda target, override=None: self.home / "absent.json"):
            with self.assertRaises(run_final_batch.BatchStop):
                run_final_canary.run_day(
                    target=self.target, ledger=self.ledger, config=self.config,
                    generation=self.generation, schema=self.schema, day="2026-09-18",
                    results_dir=self.results, execute=False, now=self.noon("2026-09-18"))
        self.assertEqual(self.ledger.snapshot()["requests_by_stage"].get(FINAL_CANARY_STAGE, 0), 0)


class StoredResponseRecovery(base.FinalBatchBase):
    """The situation of 2026-09-18: raw saved, record missing, slot INTENT."""

    def crash_after_transport(self, call):
        """Reproduce it: ``consumer_record`` raises after ``save_raw`` has committed."""
        def explode(*_, **__):
            raise KeyError("label_space")
        with patch.object(run_pilot, "consumer_record", explode):
            with self.assertRaises(KeyError):
                call()

    def test_a_canary_slot_with_a_durable_raw_closes_without_transport(self):
        self.crash_after_transport(lambda: self.run_day())
        logical_id = f"canary:day1:{self.canary_prompts[0]['prompt_id']}"
        request_id = digest([self.pilot_id, FINAL_CANARY_STAGE, logical_id])
        self.assertEqual(self.ledger.request(request_id)["status"], "INTENT")
        stored = self.ledger.response(request_id)
        self.assertIsNotNone(stored["raw"])
        self.assertIsNone(stored["record"])
        self.assertTrue(run_final_batch.stored_without_record(self.ledger, request_id))

        outcome = run_final_canary.run_day(
            target=self.target, ledger=self.ledger, config=self.config,
            generation=self.generation, schema=self.schema, day="2026-09-18",
            results_dir=self.results, execute=True, provider_factory=base.FakeProvider,
            now=self.noon("2026-09-18"))
        self.assertEqual(outcome["verdict"], "PASS")
        self.assertEqual(self.ledger.request(request_id)["status"], "COMPLETED")
        self.assertIsNotNone(self.ledger.event("note:stored_response_evaluated:" + request_id))
        # The slot was not paid for twice: one request, one receipt.
        self.assertEqual(len(self.ledger.attempts(FINAL_CANARY_STAGE, logical_id)), 1)

    def test_the_recovered_canary_slot_needs_no_provider_at_all(self):
        self.crash_after_transport(lambda: self.run_day())
        # Nine of the ten prompts are still unsent, so a provider is needed for them; here the
        # first slot alone is replayed by restricting the day to its own recovery.
        logical_id = f"canary:day1:{self.canary_prompts[0]['prompt_id']}"
        request_id = digest([self.pilot_id, FINAL_CANARY_STAGE, logical_id])
        prompt = dict(self.canary_prompts[0], label_space=base.LABELS)
        spec = next(s for s in self.ledger.binding(FINAL_CANARY_STAGE)["requests"]
                    if s["logical_id"] == logical_id)
        from studio2.fase03.harness.runtime import execute_request
        record = execute_request(
            ledger=self.ledger, stage=FINAL_CANARY_STAGE, spec=spec,
            transport=lambda: RefusingProvider(self.config).call(),
            evaluate=lambda raw: dict(run_pilot.consumer_record(raw, prompt, self.generation),
                                      repetition=1),
            expected_identity=self.config["expected_response"],
            messages=[{"role": "user", "content": prompt["text"]}],
            resume=True, retry_requests=())
        self.assertEqual(record["request_id"], request_id)
        self.assertEqual(self.ledger.request(request_id)["status"], "COMPLETED")

    def test_a_batch_slot_with_a_durable_raw_closes_without_transport(self):
        self.pass_canary_day()
        self.crash_after_transport(lambda: self.run_pass())
        stage = FINAL_PASS_STAGES[0]
        logical_id = self.schedule[0]["logical_id"]
        request_id = digest([self.pilot_id, stage, logical_id])
        self.assertEqual(self.ledger.request(request_id)["status"], "INTENT")

        summary = self.run_pass(resume=True)
        self.assertEqual(summary["recovered_from_stored_response"], 1)
        self.assertEqual(summary["sent_this_run"], self.rows_per_pass - 1)
        self.assertEqual(self.ledger.request(request_id)["status"], "COMPLETED")
        self.assertIsNotNone(self.ledger.event("note:stored_response_evaluated:" + request_id))
        self.assertEqual(len(self.ledger.attempts(stage, logical_id)), 1)

    def test_an_unresolved_slot_without_a_stored_raw_still_stops(self):
        """D3 row 2 is untouched: no raw, no recovery, author decision."""
        self.pass_canary_day()
        base.FakeProvider.script = {self.schedule[0]["logical_id"]: "raise"}
        with self.assertRaises(HarnessError):
            self.run_pass()
        stage = FINAL_PASS_STAGES[0]
        request_id = digest([self.pilot_id, stage, self.schedule[0]["logical_id"]])
        self.assertEqual(self.ledger.request(request_id)["status"], "FAILED")
        self.assertFalse(run_final_batch.stored_without_record(self.ledger, request_id))
        base.FakeProvider.script = {}
        with self.assertRaises(run_final_batch.BatchStop):
            self.run_pass(resume=True)
