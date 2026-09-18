"""Closing a final pass (7.4-CHIUSURA-PASSAGGIO): ``outcome:final_batch_rN`` = PASS.

SACRIFICIAL FIXTURES ONLY. Every case goes through the real ``run_pass`` /
``execute_request`` path with a synthetic provider; no test opens a socket. The reduced
profile of ``FinalBatchBase`` changes ``base_limits``: any closure logic bound to the
module constant ``FINAL_PASS_LIMIT`` would fail here, which is the point.
"""

from __future__ import annotations

import json
import sqlite3
import unittest
from unittest.mock import patch

from .common import HarnessError
from .ledger import (FINAL_PASS_STAGES, UNOBSERVED_ABANDONED_PREFIX, PilotLedger, digest)
from .test_final_batch import FakeProvider, FinalBatchBase
from .test_unobserved_transport_retry import RetryProvider
from studio2.fase03 import run_final_batch


class KillSwitch(BaseException):
    """Ctrl-C between reservation and response: leaves an INTENT, nothing else."""


class KillProvider(RetryProvider):
    def call(self, *, spec=None, **kwargs):
        if self.script.get(spec["logical_id"]) == "kill":
            self.calls.append(spec["logical_id"])
            raise KillSwitch
        return super().call(spec=spec, **kwargs)


class FinalPassClosure(FinalBatchBase):
    def setUp(self):
        super().setUp()
        RetryProvider.failures = {}
        RetryProvider.script = {}
        KillProvider.script = {}
        self.stage = FINAL_PASS_STAGES[0]
        self.ids = [row["logical_id"] for row in self.schedule if row["repetition"] == 1]
        self.pass_canary_day()

    def batch(self, **kwargs):
        kwargs.setdefault("provider_factory", RetryProvider)
        kwargs.setdefault("sleep", lambda _: None)
        return self.run_pass(**kwargs)

    def complete_pass_with_every_terminal_kind(self):
        RetryProvider.script = {self.ids[0]: "sdk:APIConnectionError",
                                self.ids[1]: "invalid", self.ids[2]: "abstain"}
        summary = self.batch()
        self.assertEqual(summary["status"], "COMPLETE")
        self.assertEqual(summary["abandoned_unobserved_transport"], [self.ids[0]])
        return summary

    def event_names(self):
        with sqlite3.connect(self.ledger_path) as c:
            return [r[0] for r in c.execute("SELECT event FROM events ORDER BY rowid")]

    # 1. closure with invalid, abstaining and one abandoned slot

    def test_a_complete_pass_closes_with_invalid_abstained_and_abandoned_slots(self):
        self.complete_pass_with_every_terminal_kind()
        artifact = self.ledger.close_final_pass(self.stage)
        self.assertEqual(artifact["judgement"], "none")
        self.assertEqual((artifact["planned"], artifact["completed"]), (self.rows_per_pass, self.rows_per_pass - 1))
        self.assertEqual((artifact["invalid"], artifact["abstained"]), (1, 1))
        self.assertEqual([a["logical_id"] for a in artifact["abandoned"]], [self.ids[0]])
        self.assertEqual(len(artifact["abandoned"][0]["attempts"]), 4)
        self.assertEqual(artifact["retries"], {"zero_token_proven": 0, "unobserved_transport": 3})
        self.assertEqual(artifact["stage_run"], digest(self.ledger.binding(self.stage)))
        event = self.ledger.event("outcome:" + self.stage)
        self.assertEqual(event["outcome"], "PASS")
        self.assertEqual(event["artifact_sha256"], digest(artifact))
        self.assertEqual(event["records_sha256"], artifact["records_sha256"])
        self.ledger.verify_stage_success(self.stage)

    def test_the_closure_writes_a_missing_abandonment_note_only_from_durable_proof(self):
        self.complete_pass_with_every_terminal_kind()
        leaf = self.ledger.leaf(self.stage, self.ids[0])
        name = UNOBSERVED_ABANDONED_PREFIX + leaf["request_id"]
        expected = self.ledger.event(name)
        with sqlite3.connect(self.ledger_path) as c:
            c.execute("DELETE FROM events WHERE event=?", (name,))
        self.assertIsNone(self.ledger.event(name))
        self.ledger.close_final_pass(self.stage)
        self.assertEqual(self.ledger.event(name), expected)
        self.assertEqual(self.event_names().count(name), 1)
        # A note whose digest contradicts the chain is refused, never rewritten.
        with sqlite3.connect(self.ledger_path) as c:
            c.execute("UPDATE events SET artifact_sha256=? WHERE event=?", ("a" * 64, name))
        fresh = PilotLedger(self.ledger.path, pilot_id=self.pilot_id, profile="final_batch")
        fresh.profile = self.ledger.profile
        with self.assertRaisesRegex(HarnessError, "lacks an authentic abandonment note"):
            fresh.verify_stage_success(self.stage)

    def interrupted_first_failure(self):
        """One unobserved FAILED left by a run interrupted during the backoff: retries left."""
        RetryProvider.script = {self.ids[0]: "sdk:APIConnectionError"}

        def interrupt(_):
            raise KillSwitch

        with self.assertRaises(KillSwitch):
            self.batch(sleep=interrupt)
        leaf = self.ledger.leaf(self.stage, self.ids[0])
        self.assertEqual(self.ledger.unobserved_transport_disposition(leaf["request_id"]), "retry")

    def test_an_abandonment_is_never_invented(self):
        self.interrupted_first_failure()
        leaf = self.ledger.leaf(self.stage, self.ids[0])
        with self.assertRaisesRegex(HarnessError, "not a proven abandoned slot"):
            self.ledger.record_unobserved_abandonment(leaf["request_id"])
        self.assertEqual([n for n in self.event_names() if n.startswith(UNOBSERVED_ABANDONED_PREFIX)], [])

    # 2. refusals

    def test_an_uncertain_failure_keeps_the_pass_open(self):
        FakeProvider.script = {self.ids[1]: "raise"}
        with self.assertRaises(HarnessError):
            self.run_pass()
        with self.assertRaisesRegex(HarnessError, "uncertain FAILED") as ctx:
            self.ledger.close_final_pass(self.stage)
        self.assertIn(self.ids[1] + " -> ", str(ctx.exception))
        self.assertIn("never reserved", str(ctx.exception))
        self.assertNotIn("outcome:" + self.stage, self.event_names())

    def test_an_intent_keeps_the_pass_open(self):
        KillProvider.script = {self.ids[2]: "kill"}
        with self.assertRaises(KillSwitch):
            self.batch(provider_factory=KillProvider)
        self.assertEqual(self.ledger.leaf(self.stage, self.ids[2])["status"], "INTENT")
        with self.assertRaisesRegex(HarnessError, "unresolved intent") as ctx:
            self.ledger.close_final_pass(self.stage)
        self.assertIn(self.ids[2] + " -> unresolved intent", str(ctx.exception))
        self.assertNotIn("outcome:" + self.stage, self.event_names())

    def test_partial_coverage_is_refused_naming_the_missing_slots(self):
        self.batch(max_requests=2)
        with self.assertRaisesRegex(HarnessError, "4 open slot") as ctx:
            self.ledger.close_final_pass(self.stage)
        for logical_id in self.ids[2:]:
            self.assertIn(logical_id + " -> never reserved", str(ctx.exception))
        self.assertNotIn("outcome:" + self.stage, self.event_names())

    def test_retries_still_available_keep_the_pass_open(self):
        self.interrupted_first_failure()
        with self.assertRaisesRegex(HarnessError, "retries left") as ctx:
            self.ledger.close_final_pass(self.stage)
        self.assertEqual(str(ctx.exception).count(" -> "), self.rows_per_pass)

    # 3. replay

    def test_closing_again_is_a_replay_that_writes_nothing(self):
        self.complete_pass_with_every_terminal_kind()
        first = self.ledger.close_final_pass(self.stage)
        before = self.event_names()
        fresh = PilotLedger(self.ledger.path, pilot_id=self.pilot_id, profile="final_batch")
        fresh.profile = self.ledger.profile
        self.assertEqual(fresh.close_final_pass(self.stage), first)
        self.assertEqual(self.event_names(), before)

    # 4. pass two

    def test_pass_two_unlocks_only_after_the_closure(self):
        self.complete_pass_with_every_terminal_kind()
        with self.assertRaisesRegex(HarnessError, "cannot start before"):
            self.run_pass(2)
        self.ledger.close_final_pass(self.stage)
        summary = self.run_pass(2)
        self.assertEqual(summary["status"], "COMPLETE")

    def test_pass_two_refuses_an_outcome_event_that_does_not_authenticate(self):
        self.batch(max_requests=2)  # pass one open
        artifact = {"records_sha256": digest([]), "forged": True}
        with sqlite3.connect(self.ledger_path) as c:
            c.execute("INSERT INTO events VALUES (?,?,?,?)", (
                "outcome:" + self.stage, "2026-09-18T00:00:00Z", digest(artifact),
                json.dumps({"outcome": "PASS", "diagnosis": None,
                            "records_sha256": digest([]), "artifact": artifact})))
        self.assertIn("outcome:" + self.stage, self.event_names())
        with self.assertRaises(HarnessError):
            self.run_pass(2)
        self.assertEqual(self.ledger.snapshot()["requests_by_stage"][FINAL_PASS_STAGES[1]], 0)

    def test_the_closure_is_authenticated_once_per_process_not_once_per_call(self):
        """``Provider.call`` rebinds the stage before every transport (D9): the full
        re-validation of pass one must not ride on that path, or the per-call cost of
        pass two grows with the 2.244 records of pass one."""
        self.complete_pass_with_every_terminal_kind()
        self.ledger.close_final_pass(self.stage)
        calls = []
        original = PilotLedger._successful

        def counted(ledger, c, stage):
            calls.append(stage)
            return original(ledger, c, stage)

        with patch.object(PilotLedger, "_successful", counted):
            summary = self.run_pass(2)
        self.assertEqual(summary["sent_this_run"], self.rows_per_pass)
        self.assertEqual(calls, [self.stage])

    def test_a_new_process_re_authenticates_the_closure(self):
        self.complete_pass_with_every_terminal_kind()
        self.ledger.close_final_pass(self.stage)
        self.run_pass(2, max_requests=1)
        with sqlite3.connect(self.ledger_path) as c:
            c.execute("UPDATE events SET artifact_sha256=? WHERE event=?", ("b" * 64, "outcome:" + self.stage))
        fresh = PilotLedger(self.ledger.path, pilot_id=self.pilot_id, profile="final_batch")
        fresh.profile = self.ledger.profile
        self.ledger = fresh
        with self.assertRaises(HarnessError):
            self.run_pass(2, resume=True)

    # 5. the closed stage still binds

    def test_binding_the_closed_pass_holds_and_resends_nothing(self):
        self.complete_pass_with_every_terminal_kind()
        self.ledger.close_final_pass(self.stage)
        RetryProvider.script = {}
        again = self.batch(resume=True)
        self.assertEqual((again["sent_this_run"], again["retries_this_run"]), (0, 0))
        self.assertEqual(again["abandoned_unobserved_transport"], [self.ids[0]])
        self.assertEqual(self.event_names().count("outcome:" + self.stage), 1)

    # 6. the runner adapter

    def test_close_pass_adapter_writes_the_artifact_and_reports_open_slots(self):
        self.batch(max_requests=2)
        with self.assertRaises(run_final_batch.BatchStop) as ctx:
            run_final_batch.close_pass(target=self.target, ledger=self.ledger, pass_index=1)
        self.assertIn("never reserved", str(ctx.exception))
        self.assertFalse((self.results / f"{self.stage}_closure.json").exists())
        self.batch(resume=True)
        artifact = run_final_batch.close_pass(target=self.target, ledger=self.ledger, pass_index=1)
        written = json.loads((self.results / f"{self.stage}_closure.json").read_text(encoding="utf-8"))
        self.assertEqual(written, artifact)
        self.assertEqual(self.ledger.event("outcome:" + self.stage)["artifact_sha256"], digest(artifact))


if __name__ == "__main__":
    unittest.main()
