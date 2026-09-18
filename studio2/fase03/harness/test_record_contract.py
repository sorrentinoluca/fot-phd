"""The call-record contract, closed as a whole (7.4-FIX-CONTRATTO-RECORD).

The first scientific lot of 2026-09-18 died after its first paid response with
``KeyError: 'sample_role'``: ``consumer_record`` copies a fixed set of prompt fields and the
rendered rows of ``render_all`` do not carry that one. Twice a hand-built fixture had hidden
the gap. Here every prompt comes from the real renderer or from rows with exactly its keys,
passes through the real loader, and a provider fails the test if it is ever called where it
must not be. The last class fails the day someone adds a field to ``consumer_record``
without binding it at load time.

Also the reference environment guard: NumPy is read from the frozen schedule artifact and a
different version stops every ``main()`` of the pipeline before it does anything.

SACRIFICIAL FIXTURES ONLY: no approval here is scientific and no test opens a socket.
"""

from __future__ import annotations

import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from .common import HarnessError, sha256_text
from .ledger import FINAL_CANARY_STAGE, FINAL_PASS_STAGES, digest
from . import final_inventory, final_prompts, guards
from . import test_final_batch as base
from . import test_final_prompts as rendering
from studio2.fase03 import protocol, run_final_batch, run_final_canary, run_pilot
from studio2.fase03.harness.logging_v1 import CallRecord

BUILD_MAINS = ("build_final_inventory", "build_window_assignment", "build_final_prompts",
               "prepare_final_target_inputs", "materialize_final_target",
               "run_final_canary", "run_final_batch")


class RefusingProvider:
    def __init__(self, config):
        self.config = config

    def call(self, **_):
        raise AssertionError("no call may be made where the contract is only being checked")


class TrackingPrompt(dict):
    """A prompt that records every key read from it and refuses none."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.read: set = set()

    def __getitem__(self, key):
        self.read.add(key)
        return super().__getitem__(key)

    def get(self, key, default=None):
        self.read.add(key)
        return super().get(key, default)


class RealRendererRows(unittest.TestCase):
    """Rows of the real ``render_all`` over the real inventory, through the real loader."""

    @classmethod
    def setUpClass(cls):
        cls.inventory = final_inventory.build_inventory()
        cls.rendered = final_prompts.render_all(
            inventory=cls.inventory, manifest=rendering.frozen_manifest(),
            libraries={"122B": rendering.library("G_P"), "27B": rendering.library("G_A")},
            cases=rendering.cases(cls.inventory))["rows"]

    def test_every_rendered_row_has_exactly_the_declared_keys(self):
        for row in self.rendered:
            self.assertEqual(tuple(row), final_prompts.RENDERED_ROW_KEYS)
            self.assertNotIn("label_space", row)
            self.assertNotIn("sample_role", row)

    def test_the_fixture_row_has_the_renderer_keys(self):
        self.assertEqual(tuple(base.fixture_prompt("x")), final_prompts.RENDERED_ROW_KEYS)

    def test_real_rows_load_and_carry_every_field_consumer_record_reads(self):
        with tempfile.TemporaryDirectory() as home:
            path = Path(home) / "final_prompts.jsonl"
            sample = self.rendered[:5] + self.rendered[-5:]
            path.write_text("".join(json.dumps(row) + "\n" for row in sample), encoding="utf-8")
            prompts = run_final_batch.load_prompts({"prompts": {"path": str(path)}},
                                                   label_space=base.LABELS)
        self.assertEqual(len(prompts), 10)
        for prompt in prompts.values():
            for key in run_final_batch.REQUIRED_PROMPT_FIELDS:
                self.assertIn(key, prompt)
            self.assertEqual(prompt["sample_role"], run_final_batch.FINAL_BATCH_SAMPLE_ROLE)
            self.assertEqual(prompt["label_space"], base.LABELS)
            record = run_pilot.consumer_record(base.envelope(base.answer()), prompt, {})
            self.assertEqual(record["sample_role"], "final_batch")
            self.assertEqual(record["prompt_sha256"], prompt["prompt_sha256"])


class LoaderCompleteness(base.FinalBatchBase):
    def write_rows(self, rows):
        self.prompts_path.write_text("".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")

    def test_a_row_missing_a_renderer_key_stops_the_loader_naming_it(self):
        rows = [base.fixture_prompt(r["stable_id"]) for r in self.schedule if r["repetition"] == 1]
        del rows[2]["prompt_bytes"]
        self.write_rows(rows)
        with self.assertRaises(run_final_batch.BatchStop) as caught:
            run_final_batch.load_prompts(self.target, label_space=base.LABELS)
        self.assertIn("prompt_bytes", str(caught.exception))
        self.assertEqual(sum(self.ledger.snapshot()["requests_by_stage"].values()), 0)

    def test_a_row_that_already_carries_a_bound_field_is_refused(self):
        for key in run_final_batch.BOUND_AT_LOAD_FIELDS:
            rows = [base.fixture_prompt(r["stable_id"]) for r in self.schedule if r["repetition"] == 1]
            rows[0][key] = "hand-written"
            self.write_rows(rows)
            with self.assertRaises(run_final_batch.BatchStop) as caught:
                run_final_batch.load_prompts(self.target, label_space=base.LABELS)
            self.assertIn(key, str(caught.exception))

    def test_require_prompt_fields_names_every_missing_field(self):
        prompt = {"prompt_id": "p", "text": "t"}
        with self.assertRaises(run_final_batch.BatchStop) as caught:
            run_final_batch.require_prompt_fields(prompt, source="rendered")
        message = str(caught.exception)
        for key in run_final_batch.REQUIRED_PROMPT_FIELDS:
            if key not in prompt:
                self.assertIn(key, message)

    def test_the_batch_plan_stops_at_zero_calls_on_an_incomplete_file(self):
        rows = [base.fixture_prompt(r["stable_id"]) for r in self.schedule if r["repetition"] == 1]
        del rows[0]["available_insight_ids"]
        self.write_rows(rows)
        with self.assertRaises(run_final_batch.BatchStop):
            run_final_batch.load_prompts(
                self.target, label_space=run_final_batch.target_label_space(self.target))
        self.assertEqual(sum(self.ledger.snapshot()["requests_by_stage"].values()), 0)

    def test_a_canary_row_without_sample_role_stops_the_plan_at_zero_calls(self):
        rows = [dict(row) for row in self.canary_prompts]
        del rows[3]["sample_role"]
        Path(self.target["canary_prompts"]["path"]).write_text(
            "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        with self.assertRaises(run_final_batch.BatchStop) as caught:
            run_final_canary.run_day(
                target=self.target, ledger=self.ledger, config=self.config,
                generation=self.generation, schema=self.schema, day="2026-09-18",
                results_dir=self.results, execute=False, now=self.noon("2026-09-18"))
        self.assertIn("sample_role", str(caught.exception))
        self.assertEqual(self.ledger.snapshot()["requests_by_stage"].get(FINAL_CANARY_STAGE, 0), 0)

    def test_a_canary_row_carrying_label_space_is_refused(self):
        rows = [dict(row, label_space=base.LABELS) for row in self.canary_prompts]
        Path(self.target["canary_prompts"]["path"]).write_text(
            "".join(json.dumps(r) + "\n" for r in rows), encoding="utf-8")
        with self.assertRaises(run_final_batch.BatchStop):
            run_final_canary.run_day(
                target=self.target, ledger=self.ledger, config=self.config,
                generation=self.generation, schema=self.schema, day="2026-09-18",
                results_dir=self.results, execute=False, provider_factory=RefusingProvider,
                now=self.noon("2026-09-18"))

    def test_the_canary_rows_are_pilot_rows_and_run_unchanged(self):
        self.assertEqual(set(self.canary_prompts[0]),
                         set(protocol.RenderedPrompt.__dataclass_fields__))
        outcome = self.pass_canary_day()
        self.assertEqual(outcome["verdict"], "PASS")
        leaf = self.ledger.leaf(FINAL_CANARY_STAGE, f"canary:day1:{self.canary_prompts[0]['prompt_id']}")
        record = self.ledger.response(leaf["request_id"])["record"]
        self.assertEqual(record["sample_role"], "matched_transfer")


class BatchRecordsAndLog(base.FinalBatchBase):
    def test_every_batch_record_carries_the_constant_and_the_t7_log_is_complete(self):
        self.pass_canary_day()
        summary = self.run_pass()
        self.assertEqual(summary["status"], "COMPLETE")
        stage = FINAL_PASS_STAGES[0]
        for row in self.schedule:
            if row["repetition"] != 1:
                continue
            record = self.ledger.response(self.ledger.leaf(stage, row["logical_id"])["request_id"])["record"]
            self.assertEqual(record["sample_role"], run_final_batch.FINAL_BATCH_SAMPLE_ROLE)
            for key in run_pilot.CONSUMER_RECORD_PROMPT_FIELDS:
                self.assertIn(key, record)
            self.assertEqual(record["block"], row["block"])
            self.assertEqual(record["library_role"], row["library_role"])
        log_lines = [json.loads(l) for l in (self.results / f"{stage}_call_log.jsonl").read_text().splitlines() if l]
        self.assertEqual(len(log_lines), self.rows_per_pass)
        for line in log_lines:
            self.assertEqual(set(line), set(CallRecord.__dataclass_fields__))
            self.assertNotIn("sample_role", line)

    def test_the_stored_intent_of_2026_09_18_closes_from_raw_with_the_closed_contract(self):
        """The real situation: raw saved, KeyError after the response, slot INTENT."""
        self.pass_canary_day()

        def explode(*_, **__):
            raise KeyError("sample_role")
        with patch.object(run_pilot, "consumer_record", explode):
            with self.assertRaises(KeyError):
                self.run_pass()
        stage = FINAL_PASS_STAGES[0]
        request_id = digest([self.pilot_id, stage, self.schedule[0]["logical_id"]])
        self.assertEqual(self.ledger.request(request_id)["status"], "INTENT")

        base.FakeProvider.script = {}
        summary = self.run_pass(resume=True)
        self.assertEqual(summary["recovered_from_stored_response"], 1)
        self.assertEqual(summary["sent_this_run"], self.rows_per_pass - 1)
        record = self.ledger.response(request_id)["record"]
        self.assertEqual(record["sample_role"], "final_batch")
        self.assertEqual(self.ledger.request(request_id)["status"], "COMPLETED")

    def test_the_single_stored_slot_needs_no_provider(self):
        self.pass_canary_day()

        def explode(*_, **__):
            raise KeyError("sample_role")
        with patch.object(run_pilot, "consumer_record", explode):
            with self.assertRaises(KeyError):
                self.run_pass(max_requests=1)
        base.FakeProvider.script = {}
        summary = self.run_pass(resume=True, max_requests=0, provider_factory=RefusingProvider)
        self.assertEqual(summary["recovered_from_stored_response"], 1)
        self.assertEqual(summary["sent_this_run"], 0)


class ConsumerRecordGuard(unittest.TestCase):
    """Fails the day ``consumer_record`` reads a prompt field nobody binds at load time."""

    def test_consumer_record_reads_only_declared_fields(self):
        prompt = TrackingPrompt(base.fixture_prompt("guard"), label_space=base.LABELS,
                                sample_role=run_final_batch.FINAL_BATCH_SAMPLE_ROLE)
        run_pilot.consumer_record(base.envelope(base.answer()), prompt, {})
        run_pilot.consumer_record(base.envelope("not json"), prompt, {})
        run_pilot.consumer_record({"choices": []}, prompt, {})
        self.assertTrue(prompt.read <= set(run_pilot.CONSUMER_RECORD_REQUIRED_FIELDS),
                        f"consumer_record reads undeclared prompt fields: "
                        f"{prompt.read - set(run_pilot.CONSUMER_RECORD_REQUIRED_FIELDS)}")
        self.assertEqual(set(run_pilot.CONSUMER_RECORD_PROMPT_FIELDS), prompt.read
                         & set(run_pilot.CONSUMER_RECORD_PROMPT_FIELDS))

    def test_every_declared_field_is_bound_by_the_loaders(self):
        loaded = set(final_prompts.RENDERED_ROW_KEYS) | set(run_final_batch.BOUND_AT_LOAD_FIELDS)
        self.assertTrue(set(run_final_batch.REQUIRED_PROMPT_FIELDS) <= loaded,
                        set(run_final_batch.REQUIRED_PROMPT_FIELDS) - loaded)
        pilot = set(protocol.RenderedPrompt.__dataclass_fields__) | {"label_space"}
        self.assertTrue(set(run_final_batch.REQUIRED_PROMPT_FIELDS) <= pilot,
                        set(run_final_batch.REQUIRED_PROMPT_FIELDS) - pilot)

    def test_a_field_added_to_consumer_record_is_caught_before_any_call(self):
        # Only the consumer's own declaration is patched: the runner must follow it by itself.
        with patch.object(run_pilot, "CONSUMER_RECORD_REQUIRED_FIELDS",
                          run_pilot.CONSUMER_RECORD_REQUIRED_FIELDS + ("brand_new",)):
            self.assertIn("brand_new", run_final_batch.required_prompt_fields())
            with self.assertRaises(run_final_batch.BatchStop) as caught:
                with tempfile.TemporaryDirectory() as home:
                    path = Path(home) / "p.jsonl"
                    path.write_text(json.dumps(base.fixture_prompt("x")) + "\n")
                    run_final_batch.load_prompts({"prompts": {"path": str(path)}},
                                                 label_space=base.LABELS)
        self.assertIn("brand_new", str(caught.exception))
        self.assertNotIn("brand_new", run_final_batch.required_prompt_fields())

    def test_the_runner_reads_only_declared_prompt_fields_over_a_whole_pass(self):
        """Whole-pass instrumentation: every prompt access in run_pass is declared."""
        case = base.FinalBatchBase("setUp")
        case.setUp()
        try:
            case.pass_canary_day()
            tracked = {k: TrackingPrompt(v) for k, v in case.prompts.items()}
            case.prompts = tracked
            case.run_pass()
            read = set().union(*(p.read for p in tracked.values()))
            self.assertTrue(read <= set(run_final_batch.REQUIRED_PROMPT_FIELDS),
                            read - set(run_final_batch.REQUIRED_PROMPT_FIELDS))
        finally:
            case.doCleanups()


class ReferenceEnvironment(unittest.TestCase):
    def artifact(self, home, version="2.2.6"):
        path = Path(home) / "INVENTARIO_SCHEDULE_7_4.json"
        path.write_text(json.dumps({"schedule": {"numpy_version": version}}))
        return path

    def test_the_expected_version_is_read_from_the_frozen_schedule_artifact(self):
        import numpy
        declared = guards.reference_numpy_version()
        self.assertEqual(declared, "2.2.6")
        self.assertEqual(guards.require_reference_environment(), numpy.__version__)

    def test_a_different_numpy_stops_naming_observed_and_expected(self):
        with tempfile.TemporaryDirectory() as home:
            path = self.artifact(home, "2.2.6")
            with patch("numpy.__version__", "2.3.5"):
                with self.assertRaises(HarnessError) as caught:
                    guards.require_reference_environment(path)
        message = str(caught.exception)
        self.assertIn("2.3.5 observed", message)
        self.assertIn("2.2.6 expected", message)
        self.assertTrue(message.startswith("STOP"))

    def test_a_missing_or_silent_artifact_stops(self):
        with tempfile.TemporaryDirectory() as home:
            with self.assertRaises(HarnessError):
                guards.require_reference_environment(Path(home) / "absent.json")
            path = Path(home) / "x.json"
            path.write_text(json.dumps({"schedule": {}}))
            with self.assertRaises(HarnessError):
                guards.require_reference_environment(path)

    def test_every_main_of_the_pipeline_checks_the_environment_first(self):
        import importlib
        for name in BUILD_MAINS:
            module = importlib.import_module("studio2.fase03." + name)
            with patch.object(module, "require_reference_environment",
                              side_effect=HarnessError("STOP: env")) as guard:
                with self.assertRaises(HarnessError, msg=name):
                    module.main() if name == "build_final_inventory" else module.main([])
            guard.assert_called_once()
