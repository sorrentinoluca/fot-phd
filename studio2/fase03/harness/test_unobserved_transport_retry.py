"""7.4-FIX-RETRY-RETE: retry without proof of an unobserved transport failure.

Author decision 2026-09-18. A failure in which no byte of a response was received --
connection lost or refused, 5xx, 429 -- is retried up to three times, then the slot is a
definitive technical failure and the batch continues. Timeout, authentication errors and
every received response keep their D3 treatment.

The provider raises the real ``openai`` exception classes, because the ledger classifies a
failure by the persisted ``type(exc).__name__`` exactly as ``runtime.execute_request``
records it on the real path. No test opens a socket.
"""

from __future__ import annotations

import json
import unittest

import openai

from .common import HarnessError
from .ledger import (FINAL_BATCH_PROFILE, FINAL_PASS_STAGES, UNOBSERVED_TRANSPORT_ERRORS,
                     PilotLedger, digest)
from .test_final_batch import FakeProvider, FinalBatchBase
from studio2.fase03 import run_final_batch


def sdk_error(cls, message):
    """A real SDK exception instance without an HTTP response object behind it."""
    error = cls.__new__(cls)
    Exception.__init__(error, message)
    return error


class RetryProvider(FakeProvider):
    """``FakeProvider`` plus failures by real SDK class; ``once:`` fails the first call only."""

    failures: dict = {}

    def call(self, *, prompt, schema, generation, messages=None, ledger=None, stage=None,
             spec=None):
        behaviour = self.script.get(spec["logical_id"])
        if isinstance(behaviour, str) and behaviour.startswith(("sdk:", "once:")):
            self.calls.append(spec["logical_id"])
            name = behaviour.split(":", 1)[1]
            if behaviour.startswith("once:"):
                seen = RetryProvider.failures.get(spec["logical_id"], 0)
                RetryProvider.failures[spec["logical_id"]] = seen + 1
                if seen:
                    return super().call(prompt=prompt, schema=schema, generation=generation,
                                        messages=messages, ledger=ledger, stage=stage,
                                        spec={**spec, "logical_id": "__valid__"})
            raise sdk_error(getattr(openai, name), "FIXTURE ONLY " + name)
        return super().call(prompt=prompt, schema=schema, generation=generation,
                            messages=messages, ledger=ledger, stage=stage, spec=spec)


class Interrupt(Exception):
    """Stands for Ctrl-C during the backoff wait."""


class UnobservedTransportRetry(FinalBatchBase):
    def setUp(self):
        super().setUp()
        RetryProvider.failures = {}
        RetryProvider.script = {}  # a class attribute of its own: reset it, not only FakeProvider's
        self.stage = FINAL_PASS_STAGES[0]
        self.first = self.schedule[0]["logical_id"]
        self.pass_canary_day()

    def batch(self, **kwargs):
        kwargs.setdefault("provider_factory", RetryProvider)
        kwargs.setdefault("sleep", self.waits.append)
        return self.run_pass(**kwargs)

    @property
    def waits(self):
        if not hasattr(self, "_waits"):
            self._waits = []
        return self._waits

    def test_the_admitted_set_names_real_sdk_classes_and_excludes_the_timeout(self):
        for name in UNOBSERVED_TRANSPORT_ERRORS:
            self.assertTrue(issubclass(getattr(openai, name), openai.APIError), name)
        # The timeout is a subclass of the connection error: matching the persisted class
        # name, not isinstance, is what keeps it out.
        self.assertTrue(issubclass(openai.APITimeoutError, openai.APIConnectionError))
        self.assertNotIn("APITimeoutError", UNOBSERVED_TRANSPORT_ERRORS)
        self.assertNotIn("AuthenticationError", UNOBSERVED_TRANSPORT_ERRORS)
        self.assertEqual(FINAL_BATCH_PROFILE.unobserved_transport_retries, 3)

    def test_a_lost_connection_is_retried_in_the_same_run_and_the_batch_completes(self):
        RetryProvider.script = {self.first: "once:APIConnectionError"}
        summary = self.batch()
        self.assertEqual(summary["status"], "COMPLETE")
        self.assertEqual(summary["completed"], self.rows_per_pass)
        self.assertEqual(summary["retries_this_run"], 1)
        self.assertEqual(summary["abandoned_unobserved_transport"], [])
        self.assertEqual(self.waits, [run_final_batch.RETRY_BACKOFF_BASE_SECONDS])
        original = digest([self.pilot_id, self.stage, self.first])
        self.assertEqual(self.ledger.request(original)["status"], "FAILED")
        leaf = self.ledger.leaf(self.stage, self.first)
        self.assertEqual((leaf["status"], leaf["retry_of"], leaf["quota_kind"]),
                         ("COMPLETED", original, "transport"))
        snapshot = self.ledger.snapshot()
        self.assertEqual(snapshot["retry_quota_used"], 1)
        self.assertEqual(snapshot["requests_by_stage"][self.stage], self.rows_per_pass + 1)
        self.assertEqual(max(self.ledger.consecutive_technical_failures().values()), 0)

    def test_5xx_and_429_are_in_the_admitted_set(self):
        RetryProvider.script = {self.schedule[0]["logical_id"]: "once:InternalServerError",
                                self.schedule[1]["logical_id"]: "once:RateLimitError"}
        summary = self.batch()
        self.assertEqual(summary["status"], "COMPLETE")
        self.assertEqual(summary["retries_this_run"], 2)

    def test_three_failed_retries_make_the_slot_definitive_and_the_batch_continues(self):
        RetryProvider.script = {self.first: "sdk:APIConnectionError"}
        summary = self.batch()
        self.assertEqual(summary["abandoned_unobserved_transport"], [self.first])
        self.assertEqual(summary["retries_this_run"], 3)
        self.assertEqual(self.waits, [30.0, 60.0, 120.0])
        self.assertEqual(summary["completed"], self.rows_per_pass)
        self.assertEqual(summary["sent_this_run"], self.rows_per_pass - 1)
        attempts = self.ledger.attempts(self.stage, self.first)
        self.assertEqual([a["status"] for a in attempts], ["FAILED"] * 4)
        leaf = self.ledger.leaf(self.stage, self.first)
        self.assertEqual(self.ledger.unobserved_transport_disposition(leaf["request_id"]),
                         "exhausted")
        note = self.ledger.event("note:unobserved_transport_abandoned:" + leaf["request_id"])
        self.assertEqual(note["attempts"], [a["request_id"] for a in attempts])
        # Resuming never tries the abandoned slot again, and records the note only once.
        RetryProvider.script = {}
        again = self.batch(resume=True)
        self.assertEqual(again["sent_this_run"], 0)
        self.assertEqual(again["retries_this_run"], 0)
        self.assertEqual(again["abandoned_unobserved_transport"], [self.first])

    def test_the_ledger_refuses_a_fourth_retry_on_its_own(self):
        RetryProvider.script = {self.first: "sdk:APIConnectionError"}
        self.batch(max_requests=1)
        leaf = self.ledger.leaf(self.stage, self.first)
        spec = next(s for s in self.ledger.binding(self.stage)["requests"]
                    if s["logical_id"] == self.first)
        with self.assertRaisesRegex(HarnessError, "are exhausted"):
            self.ledger.reserve_transport_retry(
                request_id="f" * 64, logical_id=self.first, model=spec["model"],
                producer=spec["producer"], stage=self.stage,
                stage_run=digest(self.ledger.binding(self.stage)), retry_of=leaf["request_id"])

    def test_a_failure_left_by_an_interrupted_run_is_retried_on_resume(self):
        """The real stop of 2026-09-18: a FAILED connection slot waiting in the ledger."""
        RetryProvider.script = {self.first: "once:APIConnectionError"}

        def interrupt(_):
            raise Interrupt

        with self.assertRaises(Interrupt):
            self.batch(sleep=interrupt)
        original = digest([self.pilot_id, self.stage, self.first])
        self.assertEqual(self.ledger.leaf(self.stage, self.first)["request_id"], original)
        self.assertEqual(self.ledger.request(original)["status"], "FAILED")
        reopened = PilotLedger(self.ledger.path, pilot_id=self.pilot_id, profile="final_batch")
        reopened.profile = self.ledger.profile
        self.ledger = reopened
        summary = self.batch(resume=True)
        self.assertEqual(summary["status"], "COMPLETE")
        self.assertEqual(summary["retries_this_run"], 1)
        self.assertEqual(self.ledger.leaf(self.stage, self.first)["retry_of"], original)

    def test_a_timeout_still_stops_and_is_never_resent(self):
        RetryProvider.script = {self.first: "sdk:APITimeoutError"}
        with self.assertRaisesRegex(HarnessError, "uncertain outcome"):
            self.batch()
        self.assertEqual(len(self.ledger.attempts(self.stage, self.first)), 1)
        RetryProvider.script = {}
        with self.assertRaises(run_final_batch.BatchStop):
            self.batch(resume=True)
        self.assertEqual(len(self.ledger.attempts(self.stage, self.first)), 1)

    def test_an_authentication_error_still_stops(self):
        RetryProvider.script = {self.first: "sdk:AuthenticationError"}
        with self.assertRaises(HarnessError):
            self.batch()
        with self.assertRaises(run_final_batch.BatchStop):
            self.batch(resume=True)
        self.assertEqual(len(self.ledger.attempts(self.stage, self.first)), 1)

    def test_a_retry_that_times_out_leaves_the_admitted_set_and_stops(self):
        calls = {"n": 0}
        original_call = RetryProvider.call

        def mixed(provider, **kwargs):
            if kwargs["spec"]["logical_id"] == self.first:
                calls["n"] += 1
                name = "APIConnectionError" if calls["n"] == 1 else "APITimeoutError"
                raise sdk_error(getattr(openai, name), "FIXTURE ONLY " + name)
            return original_call(provider, **kwargs)

        RetryProvider.call = mixed
        self.addCleanup(setattr, RetryProvider, "call", original_call)
        with self.assertRaisesRegex(HarnessError, "uncertain outcome"):
            self.batch()
        self.assertEqual(len(self.ledger.attempts(self.stage, self.first)), 2)
        with self.assertRaises(run_final_batch.BatchStop):
            self.batch(resume=True)

    def test_five_consecutive_failures_still_stop_the_campaign(self):
        RetryProvider.script = {self.schedule[0]["logical_id"]: "sdk:APIConnectionError",
                                self.schedule[1]["logical_id"]: "sdk:APIConnectionError"}
        with self.assertRaisesRegex(HarnessError, "consecutive technical"):
            self.batch()
        # Four attempts on the first slot, the fifth failure on the second one.
        self.assertEqual(len(self.ledger.attempts(self.stage, self.schedule[1]["logical_id"])), 1)
        self.assertEqual(max(self.ledger.consecutive_technical_failures().values()), 5)

    def test_the_failure_detail_keeps_status_code_and_cause(self):
        original_call = RetryProvider.call

        def disconnected(provider, **kwargs):
            if kwargs["spec"]["logical_id"] == self.first:
                try:
                    raise ConnectionError("Server disconnected without sending a response.")
                except ConnectionError as cause:
                    raise sdk_error(openai.APIConnectionError, "Connection error.") from cause
            return original_call(provider, **kwargs)

        RetryProvider.call = disconnected
        self.addCleanup(setattr, RetryProvider, "call", original_call)
        self.batch(max_requests=1)
        detail = json.loads(self.ledger.request(
            digest([self.pilot_id, self.stage, self.first]))["detail_json"])
        self.assertEqual(detail["error_type"], "APIConnectionError")
        self.assertIsNone(detail["status_code"])
        self.assertEqual(detail["cause_type"], "ConnectionError")
        self.assertIn("Server disconnected", detail["cause_message"])

    def test_a_5xx_keeps_its_status_code(self):
        original_call = RetryProvider.call

        def server_error(provider, **kwargs):
            if kwargs["spec"]["logical_id"] == self.first:
                error = sdk_error(openai.InternalServerError, "Error code: 502")
                error.status_code = 502
                raise error
            return original_call(provider, **kwargs)

        RetryProvider.call = server_error
        self.addCleanup(setattr, RetryProvider, "call", original_call)
        self.batch(max_requests=1)
        detail = json.loads(self.ledger.request(
            digest([self.pilot_id, self.stage, self.first]))["detail_json"])
        self.assertEqual(detail["status_code"], 502)

    def test_max_requests_counts_answered_calls_not_failed_attempts(self):
        RetryProvider.script = {self.first: "once:APIConnectionError"}
        summary = self.batch(max_requests=2)
        self.assertEqual(summary["sent_this_run"], 2)
        self.assertEqual(summary["status"], "PARTIAL")


if __name__ == "__main__":
    unittest.main()
