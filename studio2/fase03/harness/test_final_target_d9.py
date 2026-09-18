"""The final target under a real D9 configuration (REVISIONE_002, ``d9.final_target``).

``test_final_batch`` strips ``execution_config`` from its bindings; here the bindings are
the real ones, so every reservation walks the whole D9 chain on a ``final_batch`` ledger.
SACRIFICIAL FIXTURES ONLY: no approval here is scientific and no test opens a socket.
"""

from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from unittest.mock import patch

from .common import HarnessError, sha256_file
from .guards import require_execution, require_pilot_ledger
from .ledger import FINAL_CANARY_STAGE, FINAL_PASS_STAGES, PilotLedger
from . import d9
from . import test_final_batch as base
from studio2.fase03 import run_final_batch, run_final_canary

QUALIFIED = {"returned_model": "qwen3.5-122b", "system_fingerprint": "vllm-0.27.1-934a3247"}


class QualifiedProvider(base.FakeProvider):
    """Synthetic transport answering with the qualified 122B identity."""

    def call(self, **kwargs):
        raw = super().call(**kwargs)
        if raw["system_fingerprint"] == base.FINGERPRINT:
            raw.update(model=QUALIFIED["returned_model"],
                       system_fingerprint=QUALIFIED["system_fingerprint"])
        return raw


class FinalTargetD9(base.FinalBatchBase):
    def setUp(self):
        super().setUp()
        # Real bindings again: the point of this file.
        self.stack.enter_context(patch.object(run_final_batch, "pass_binding", base._PASS_BINDING))
        self.stack.enter_context(patch.object(run_final_canary, "canary_binding",
                                              base._CANARY_BINDING))
        from .test_revisions import RunnerRevisions
        from studio2.fase03 import materialize_successor_recovery as materializer
        self.fixture = RunnerRevisions()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.identity_binding = materializer._response_identity_binding()
        self.config = self.final_config()
        self.target["tokenizer_snapshot"] = str(self.fixture.snapshot)

    def final_config(self, *, mutate=None):
        t = self.fixture
        config = t.config
        config.pop("execution_authorization", None)
        section = config["d9"]
        section.pop("history_reconciliation", None)
        section["final_target"] = {"artifact_version": d9.FINAL_TARGET_VERSION,
                                   "target_id": self.pilot_id,
                                   "predecessor_consumption": d9.FINAL_TARGET_PREDECESSORS}
        service = section["services"]["122B"]
        service.update(identity_sha256=d9.APPROVED_122B_IDENTITY_SHA256,
                       expected_response=dict(QUALIFIED))
        path = Path(service["documentation"]["path"])
        document = json.loads(path.read_text())
        document["service"] = {k: deepcopy(v) for k, v in service.items() if k != "documentation"}
        document["identity_binding"] = self.identity_binding
        path.write_text(json.dumps(document))
        service["documentation"] = {"path": str(path), "sha256": sha256_file(path)}
        config["expected_response"] = dict(QUALIFIED)
        config["pilot_ledger"] = {"path": str(self.ledger.identity_path), "pilot_id": self.pilot_id}
        if mutate is not None:
            mutate(config)
        t.approve_config()
        return deepcopy(t.config)

    def run_day(self, day="2026-09-18", now=None):
        return run_final_canary.run_day(
            target=self.target, ledger=self.ledger, config=self.config,
            generation=self.generation, schema=self.schema, day=day,
            results_dir=self.results, execute=True, provider_factory=QualifiedProvider,
            now=now if now is not None else self.noon(day))

    def test_guards_accept_the_fresh_final_target(self):
        require_execution(self.config)
        require_pilot_ledger(self.config, self.ledger)

    def test_canary_and_pass_run_on_real_bindings(self):
        self.assertEqual(self.pass_canary_day()["verdict"], "PASS")
        summary = self.run_pass(provider_factory=QualifiedProvider)
        self.assertEqual(summary["status"], "COMPLETE")
        for stage in (FINAL_CANARY_STAGE, FINAL_PASS_STAGES[0]):
            self.assertEqual(self.ledger.binding(stage)["execution_config"], self.config)

    def test_plan_without_calls_passes_the_history_guard(self):
        outcome = run_final_canary.run_day(
            target=self.target, ledger=self.ledger, config=self.config,
            generation=self.generation, schema=self.schema, day="2026-09-18",
            results_dir=self.results, execute=False, now=self.noon("2026-09-18"))
        self.assertEqual(outcome["status"], "PLAN_ONLY")
        require_pilot_ledger(self.config, self.ledger)

    def test_final_target_is_exclusive_with_pilot_history(self):
        for key in d9.PILOT_HISTORY_KEYS:
            config = deepcopy(self.config)
            config["d9"][key] = {"path": "/nonexistent", "sha256": "0" * 64}
            with self.subTest(key=key), self.assertRaisesRegex(HarnessError, "cannot be combined"):
                d9.validate_config(config)

    def test_declaration_must_name_this_ledger_exactly(self):
        for field, value in (("target_id", "another-target"), ("predecessor_consumption", "S5"),
                             ("artifact_version", "0"), ("extra", 1)):
            config = deepcopy(self.config)
            config["d9"]["final_target"][field] = value
            with self.subTest(field=field), self.assertRaisesRegex(HarnessError, "final target"):
                d9.validate_config(config)

    def test_122b_identity_binding_stays_mandatory(self):
        path = Path(self.config["d9"]["services"]["122B"]["documentation"]["path"])
        document = json.loads(path.read_text())
        document.pop("identity_binding")
        path.write_text(json.dumps(document))
        config = deepcopy(self.config)
        config["d9"]["services"]["122B"]["documentation"]["sha256"] = sha256_file(path)
        with self.assertRaisesRegex(HarnessError, "identity binding"):
            d9.validate_config(config)

    def test_mode_and_ledger_profile_go_together_only(self):
        pilot = PilotLedger(self.home / "pilot.sqlite3", pilot_id=self.pilot_id)
        with pilot._transaction() as connection:
            with self.assertRaisesRegex(HarnessError, "go together only"):
                d9.validate_history(self.config, pilot, connection)
        with self.assertRaisesRegex(HarnessError, "go together only"):
            require_pilot_ledger(self.fixture_pilot_mode_config(), self.ledger)

    def fixture_pilot_mode_config(self):
        """The pilot's zero-history fixture mode addressed to the final ledger."""
        history = self.home / "history.json"
        ledger = {"path": str(self.ledger.identity_path), "pilot_id": self.pilot_id}
        history.write_text(json.dumps({"status": "RECONCILED", "reviewer": "FIXTURE ONLY",
                                       "source": d9.HISTORY_SOURCE, "pilot_ledger": ledger,
                                       "request_identities": {}}))

        def mutate(config):
            config["d9"].pop("final_target")
            config["d9"]["history_reconciliation"] = {"path": str(history),
                                                      "sha256": sha256_file(history)}
        return self.final_config(mutate=mutate)


if __name__ == "__main__":
    import unittest
    unittest.main()
