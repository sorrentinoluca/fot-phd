"""Successor 122B recovery contract. All calls and approvals are offline fixtures."""
from __future__ import annotations

from contextlib import closing
from copy import deepcopy
import difflib
import json
import multiprocessing
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest import mock

from studio2.fase03.harness.common import HarnessError, canonical_json, sha256_file, sha256_text
from studio2.fase03.harness.ledger import PilotLedger, TokenizerAccountingGuard, digest


TECHNICAL_STAGE = "technical_qualification_122b"


def _logical(path: Path) -> str:
    with closing(sqlite3.connect(path)) as connection:
        return "\n".join(connection.iterdump())


def _spec(stage: str, index: int, *, count: int) -> dict:
    condition = ("A", "B-LF", "E-LF")[index % 3] if stage == "budget_probe" else "technical" if stage == TECHNICAL_STAGE else "producer"
    return {
        "logical_id": f"{stage}-{index}",
        "model": "fixture-model",
        "producer": "fixture-producer",
        "prompt_sha256": sha256_text(f"{stage}-prompt-{index}"),
        "case_sha256": digest([stage, "case", index]),
        "contract_sha256": digest([stage, "contract", index]),
        "condition": condition,
        "group": str(index // 3) if stage == "budget_probe" else str(index),
        "repetition": 1,
    }


def _binding(stage: str, count: int) -> dict:
    return {
        "requests": [_spec(stage, index, count=count) for index in range(count)],
        "template_text": "OFFLINE FIXTURE TEMPLATE\n",
        "inventory_sha256": digest([stage, count]),
    }


def _complete(ledger: PilotLedger, request_id: str, *, technical_pass: bool = True,
              finish_reason: str = "stop", schema_valid: bool = True) -> dict:
    row = ledger.request(request_id)
    identity = json.loads(row["identity_json"])
    record = {
        "request_id": request_id,
        "prompt_sha256": identity["prompt_sha256"],
        "identity_valid": True,
        "schema_valid_first_attempt": schema_valid,
        "validation_class": None if schema_valid else "structure",
        "finish_reason": finish_reason,
        "raw_output": "FIXTURE",
    }
    if row["stage"] == TECHNICAL_STAGE:
        record.update(technical_pass=technical_pass, reasoning_empty=True,
                      rendering_control_accepted=True, scientific_use="FORBIDDEN")
    ledger.save_raw(request_id, {"fixture": "raw"})
    ledger.complete_request(request_id, status="COMPLETED", record=record)
    return record


def _outcome(ledger: PilotLedger, stage: str, outcome: str = "PASS") -> None:
    records = ledger.stage_records(stage)
    artifact = {"records_sha256": digest(records)}
    frozen = None
    if stage == "budget_probe":
        frozen = {"generation": records[-1]["generation"], "prompt_sample": []}
    ledger.record_stage_outcome(stage, outcome=outcome, artifact_sha256=digest(artifact),
                                artifact=artifact, frozen=frozen)


def _reserve(ledger: PilotLedger, stage: str, index: int, request_id: str | None = None) -> str:
    binding = ledger.binding(stage)
    spec = binding["requests"][index]
    value = dict(request_id=request_id or f"{stage}-{index}", logical_id=spec["logical_id"],
                 model=spec["model"], producer=spec["producer"], stage_run=digest(binding))
    if stage == TECHNICAL_STAGE:
        ledger.reserve_technical_request(**value)
    elif stage == "producer_remediation":
        ledger.reserve_remediation_request(**value)
    else:
        ledger.reserve_request(stage=stage, **value)
    return value["request_id"]


def _zero(ledger: PilotLedger, request_id: str, home: Path, serial: int) -> None:
    row = ledger.request(request_id)
    evidence = {
        "request_id": request_id,
        "request_identity_sha256": sha256_text(row["identity_json"]),
        "disposition": "not_generated",
        "provider_request_id": f"FIXTURE-{serial}",
        "provider_evidence": "OFFLINE FIXTURE",
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0,
    }
    evidence_path = home / f"zero-{serial}.json"
    evidence_path.write_text(json.dumps(evidence), encoding="utf-8")
    approval_path = home / f"zero-{serial}-approval.json"
    approval_path.write_text(json.dumps({"author": "FIXTURE", "decision": "accepted",
                                         "evidence_sha256": sha256_file(evidence_path)}), encoding="utf-8")
    ledger.reconcile_zero_token(request_id, evidence_path=evidence_path, approval_path=approval_path)


def _make_predecessor(path: Path) -> PilotLedger:
    ledger = PilotLedger(path, pilot_id="predecessor-fixture")
    package_hash = "a" * 64
    approval_hash = "b" * 64
    with ledger._transaction() as connection:
        connection.execute("""CREATE TABLE external_history (
            request_id TEXT PRIMARY KEY,
            historical_ordinal INTEGER NOT NULL UNIQUE CHECK(historical_ordinal BETWEEN 1 AND 4),
            identity_json TEXT NOT NULL,
            identity_sha256 TEXT NOT NULL UNIQUE,
            source_binding_json TEXT NOT NULL,
            source_binding_sha256 TEXT NOT NULL UNIQUE,
            disposition TEXT NOT NULL,
            package_sha256 TEXT NOT NULL)""")
        for ordinal in range(1, 5):
            identity = canonical_json({"historical_ordinal": ordinal, "fixture": True})
            source = canonical_json({"source": ordinal, "fixture": True})
            connection.execute("INSERT INTO external_history VALUES (?,?,?,?,?,?,?,?)", (
                f"historical-{ordinal}", ordinal, identity, sha256_text(identity),
                source, sha256_text(source),
                "HISTORICAL_OUTCOME_UNCERTAIN" if ordinal == 1 else "COMPLETED", package_hash))
        detail = canonical_json({"status": "RECONCILED", "count": 4,
                                 "package_sha256": package_hash,
                                 "approval_sha256": approval_hash})
        connection.execute("INSERT INTO events VALUES (?,?,?,?)", (
            "history_reconciliation:" + package_hash, "2026-09-16T00:00:00+00:00",
            package_hash, detail))
        connection.execute("PRAGMA user_version=3")
    binding = _binding("producer_conformity", 8)
    ledger.bind_stage("producer_conformity", binding)
    spec = binding["requests"][0]
    request_id = digest([ledger.pilot_id, "producer_conformity", spec["logical_id"]])
    ledger.reserve_request(request_id=request_id, logical_id=spec["logical_id"],
                           model=spec["model"], producer=spec["producer"],
                           stage="producer_conformity", stage_run=digest(binding))
    raw = {"id": "fixture-response", "model": "fixture-model",
           "system_fingerprint": "fixture-fingerprint", "choices": [],
           "usage": {"prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}}
    ledger.save_raw(request_id, raw)
    record = {"request_id": request_id, "prompt_sha256": spec["prompt_sha256"],
              "returned_model": "fixture-model", "system_fingerprint": "fixture-fingerprint",
              "identity_valid": False, "schema_valid_first_attempt": False,
              "finish_reason": "length", "raw_output": None,
              "prompt_tokens": 1, "completion_tokens": 1, "total_tokens": 2}
    ledger.complete_request(request_id, status="COMPLETED", record=record,
                            prompt_tokens=1, completion_tokens=1, total_tokens=2)
    return ledger


def _mutate_successor_lineage(ledger: PilotLedger, mutation: str) -> str:
    """Apply one post-import corruption to a sacrificial successor fixture."""
    with ledger._transaction() as connection:
        native_id = connection.execute(
            "SELECT request_id FROM predecessor_lineage WHERE ordinal=5").fetchone()[0]
        if mutation == "ordinal":
            connection.execute("PRAGMA ignore_check_constraints=ON")
            connection.execute("UPDATE predecessor_lineage SET ordinal=6 WHERE ordinal=5")
        elif mutation == "request_id":
            connection.execute(
                "UPDATE predecessor_lineage SET request_id='mutated-native-id' WHERE ordinal=5")
        elif mutation == "source_kind":
            connection.execute(
                "UPDATE predecessor_lineage SET source_kind='external_history' WHERE ordinal=5")
        elif mutation == "identity_json_and_digest":
            identity = canonical_json({"mutated": True})
            connection.execute(
                "UPDATE predecessor_lineage SET identity_json=?,identity_sha256=? WHERE ordinal=5",
                (identity, sha256_text(identity)))
        elif mutation == "identity_sha256":
            connection.execute(
                "UPDATE predecessor_lineage SET identity_sha256=? WHERE ordinal=5", ("1" * 64,))
        elif mutation == "source_binding_sha256":
            connection.execute(
                "UPDATE predecessor_lineage SET source_binding_sha256=? WHERE ordinal=5",
                ("2" * 64,))
        elif mutation == "disposition":
            connection.execute(
                "UPDATE predecessor_lineage SET disposition='COMPLETED' WHERE ordinal=5")
        elif mutation == "raw_sha256":
            connection.execute(
                "UPDATE predecessor_lineage SET raw_sha256=? WHERE ordinal=5", ("3" * 64,))
        elif mutation == "record_sha256":
            connection.execute(
                "UPDATE predecessor_lineage SET record_sha256=? WHERE ordinal=5", ("4" * 64,))
        elif mutation == "package_sha256":
            connection.execute(
                "UPDATE predecessor_lineage SET package_sha256=? WHERE ordinal=5", ("5" * 64,))
        elif mutation == "predecessor_sha256":
            connection.execute(
                "UPDATE predecessor_lineage SET predecessor_sha256=? WHERE ordinal=5",
                ("6" * 64,))
        elif mutation == "approval_sha256":
            row = connection.execute(
                "SELECT event,detail_json FROM events WHERE event LIKE 'successor_lineage:%'"
            ).fetchone()
            detail = json.loads(row["detail_json"])
            detail["approval_sha256"] = "7" * 64
            connection.execute("UPDATE events SET detail_json=? WHERE event=?",
                               (canonical_json(detail), row["event"]))
        else:
            raise AssertionError("unknown lineage mutation: " + mutation)
    return native_id


def _reserve_worker(path: str, pilot_id: str, queue) -> None:
    try:
        ledger = PilotLedger(Path(path), pilot_id=pilot_id)
        _reserve(ledger, "stability_gate", 119, request_id=f"race-{os.getpid()}")
    except Exception as exc:  # process boundary reports only outcome
        queue.put(type(exc).__name__ + ":" + str(exc))
    else:
        queue.put("OK")


class SuccessorFixture(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.predecessor = _make_predecessor(self.home / "predecessor.sqlite3")
        self.predecessor_sha = sha256_file(self.predecessor.path)
        self.successor_path = (self.home / "successor.sqlite3").resolve()
        self.successor_id = "successor-fixture"
        self.evidence = {}
        for name in ("stop_review_v2", "proposal_md", "proposal_json", "proposal_review"):
            path = self.home / f"{name}.txt"
            path.write_text("OFFLINE FIXTURE " + name + "\n", encoding="utf-8")
            self.evidence[name] = {"path": str(path.resolve()), "sha256": sha256_file(path)}
        decision_path = self.home / "author_decision.json"
        decision_path.write_text(json.dumps({
            "status": "AUTHOR_DECISION_ACQUIRED",
            "decision_text": "FIXTURE AUTHOR DECISION",
            "selection": {
                "t9_classification": "ANTECEDENT_QUALIFICATION_CONFIGURATION_FAILURE",
                "predecessor_sha256": self.predecessor_sha,
                "cumulative_lineage_requests": 5,
                "lineage_import": "EXACTLY_ONCE_SUCCESSOR_ONLY",
                "technical_qualification_calls": 1,
                "producer_rendering_control": {
                    "chat_template_kwargs": {"enable_thinking": False}},
                "consumer_probe_gate": "UNCHANGED",
                "t9": "UNCHANGED_AND_NOT_CONSUMED_BY_TECHNICAL_STAGE",
                "remediation": "NOT_CONSUMED_NOT_AUTHORIZED",
                "cumulative_planned_maximum": 166,
                "hard_stop": 200,
                "non_spendable_margin": 34,
            },
            "independent_review": {"sha256": self.evidence["proposal_review"]["sha256"]},
            "authorization": {
                "implementation_and_offline_materialization": True,
                "provider_calls": False,
                "execution_authorization_created": False,
            },
        }), encoding="utf-8")
        self.evidence["author_decision"] = {
            "path": str(decision_path.resolve()), "sha256": sha256_file(decision_path)}

    def lineage_files(self, *, mutate=None):
        from studio2.fase03.harness.successor import build_successor_lineage_package
        package_value = build_successor_lineage_package(
            predecessor_path=self.predecessor.path,
            predecessor_pilot_id=self.predecessor.pilot_id,
            successor_ledger={"path": str(self.successor_path), "pilot_id": self.successor_id},
            evidence=self.evidence,
            author_decision_text_sha256=sha256_text("FIXTURE AUTHOR DECISION"),
        )
        if mutate:
            mutate(package_value)
        package = self.home / f"package-{len(list(self.home.glob('package-*')))}.json"
        package.write_text(json.dumps(package_value, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        approval = self.home / (package.stem + "-approval.json")
        approval.write_text(json.dumps({
            "artifact_version": "1",
            "author": "FIXTURE AUTHOR",
            "decision": "SUCCESSOR_LINEAGE_IMPORT_AUTHORIZED",
            "package_sha256": sha256_file(package),
            "successor_ledger": {"path": str(self.successor_path), "pilot_id": self.successor_id},
            "author_decision": self.evidence["author_decision"],
        }, sort_keys=True, indent=2) + "\n", encoding="utf-8")
        return package, approval

    def imported(self) -> PilotLedger:
        ledger = PilotLedger(self.successor_path, pilot_id=self.successor_id)
        package, approval = self.lineage_files()
        ledger.reconcile_successor_lineage(package_path=package, approval_path=approval)
        return ledger

    def _pass_technical(self, ledger: PilotLedger) -> None:
        ledger.bind_stage(TECHNICAL_STAGE, _binding(TECHNICAL_STAGE, 1))
        request_id = _reserve(ledger, TECHNICAL_STAGE, 0)
        _complete(ledger, request_id)
        _outcome(ledger, TECHNICAL_STAGE)


class SuccessorLineageTests(SuccessorFixture):
    def test_valid_exactly_once_restart_and_predecessor_immutable(self):
        before = self.predecessor.path.read_bytes()
        ledger = self.imported()
        snapshot = ledger.snapshot()
        self.assertEqual(snapshot["requests_cumulative"], 5)
        self.assertEqual(snapshot["predecessor_lineage_requests"], 5)
        self.assertEqual(snapshot["planned_maximum_with_alternate"], 166)
        lineage_package, _ = self.lineage_files()
        package_value = json.loads(lineage_package.read_text(encoding="utf-8"))
        predecessor_request_id = package_value["requests"][-1]["request_id"]
        ledger.bind_stage(TECHNICAL_STAGE, _binding(TECHNICAL_STAGE, 1))
        binding = ledger.binding(TECHNICAL_STAGE)
        spec = binding["requests"][0]
        common = dict(logical_id=spec["logical_id"], model=spec["model"],
                      producer=spec["producer"], stage_run=digest(binding))
        with self.assertRaisesRegex(HarnessError, "predecessor lineage"):
            ledger.reserve_technical_request(request_id=predecessor_request_id, **common)
        with self.assertRaisesRegex(HarnessError, "predecessor lineage"):
            ledger.reserve_transport_retry(
                request_id="forbidden-retry", stage="producer_conformity",
                retry_of=predecessor_request_id, **common)
        self.assertEqual(ledger.snapshot()["requests_cumulative"], 5)
        package, approval = self.lineage_files()
        state = _logical(ledger.path)
        with self.assertRaisesRegex(HarnessError, "already reconciled"):
            ledger.reconcile_successor_lineage(package_path=package, approval_path=approval)
        self.assertEqual(_logical(ledger.path), state)
        restarted = PilotLedger(ledger.path, pilot_id=self.successor_id)
        self.assertEqual(restarted.snapshot()["requests_cumulative"], 5)
        self.assertEqual(self.predecessor.path.read_bytes(), before)
        self.assertEqual(sha256_file(self.predecessor.path), self.predecessor_sha)

    def test_selective_tampered_and_transitive_imports_refuse_without_side_effect(self):
        mutations = [
            lambda value: value["requests"].pop(),
            lambda value: value["requests"][4].update(disposition="COMPLETED"),
            lambda value: value["predecessor"].update(sha256="0" * 64),
            lambda value: value["evidence"]["proposal_review"].update(sha256="1" * 64),
        ]
        for index, mutation in enumerate(mutations):
            path = (self.home / f"successor-{index}.sqlite3").resolve()
            self.successor_path = path
            ledger = PilotLedger(path, pilot_id=self.successor_id)
            package, approval = self.lineage_files(mutate=mutation)
            before = _logical(path)
            with self.subTest(index=index), self.assertRaises(HarnessError):
                ledger.reconcile_successor_lineage(package_path=package, approval_path=approval)
            self.assertEqual(_logical(path), before)
        with closing(sqlite3.connect(self.predecessor.path)) as connection, connection:
            connection.execute("CREATE TABLE predecessor_lineage(marker TEXT)")
        with self.assertRaisesRegex(HarnessError, "transitive"):
            self.lineage_files()


class TechnicalStageTests(SuccessorFixture):
    def test_technical_stage_is_mandatory_once_before_conformity_and_survives_restart(self):
        ledger = self.imported()
        with self.assertRaisesRegex(HarnessError, "technical qualification"):
            ledger.bind_stage("producer_conformity", _binding("producer_conformity", 8))
        self._pass_technical(ledger)
        with self.assertRaises(HarnessError):
            _reserve(ledger, TECHNICAL_STAGE, 0, request_id="second-technical")
        restarted = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
        restarted.bind_stage("producer_conformity", _binding("producer_conformity", 8))
        self.assertEqual(restarted.snapshot()["requests_by_stage"][TECHNICAL_STAGE], 1)

    def test_each_technical_mismatch_fails_closed_and_never_enters_t9(self):
        from studio2.fase03.technical_qualification_122b import evaluate_response
        base = {
            "id": "fixture", "model": "qwen3.5-122b", "system_fingerprint": "fp-exact",
            "choices": [{"message": {"content": '{"status":"NO_THINKING_OK"}'},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 6, "total_tokens": 16},
        }
        expected = {"returned_model": "qwen3.5-122b", "system_fingerprint": "fp-exact"}
        self.assertTrue(evaluate_response(deepcopy(base), expected)["technical_pass"])
        mutations = [
            lambda raw: raw.update(system_fingerprint="changed"),
            lambda raw: raw["choices"][0]["message"].update(reasoning="not empty"),
            lambda raw: raw["choices"][0]["message"].update(content='{"status":"WRONG"}'),
            lambda raw: raw["choices"][0].update(finish_reason="length"),
        ]
        for mutation in mutations:
            raw = deepcopy(base)
            mutation(raw)
            record = evaluate_response(raw, expected)
            self.assertFalse(record["technical_pass"])
            self.assertEqual(record["scientific_use"], "FORBIDDEN")
        ledger = self.imported()
        ledger.bind_stage(TECHNICAL_STAGE, _binding(TECHNICAL_STAGE, 1))
        request_id = _reserve(ledger, TECHNICAL_STAGE, 0)
        _complete(ledger, request_id, technical_pass=False)
        ledger.suspend_technical(request_id, reason="OFFLINE FIXTURE MISMATCH")
        before = ledger.snapshot()["requests_cumulative"]
        restarted = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
        with self.assertRaisesRegex(HarnessError, "suspended"):
            restarted.bind_stage("producer_conformity", _binding("producer_conformity", 8))
        self.assertEqual(restarted.snapshot()["requests_cumulative"], before)

    def test_accounting_mismatch_is_a_persistent_charged_stop_before_second_call(self):
        class MismatchTokenizer:
            def apply_chat_template(self, messages, **kwargs):
                return [1] * 12

        ledger = self.imported()
        binding = _binding(TECHNICAL_STAGE, 1)
        binding["requests"][0]["model"] = "qwen3.5-122b"
        ledger.bind_stage(TECHNICAL_STAGE, binding)
        request_id = _reserve(ledger, TECHNICAL_STAGE, 0)
        ledger.save_raw(request_id, {
            "id": "fixture", "model": "qwen3.5-122b", "system_fingerprint": "fp",
            "choices": [{"message": {"content": '{"status":"NO_THINKING_OK"}'},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 9, "total_tokens": 20},
        })
        guard = TokenizerAccountingGuard(
            MismatchTokenizer(), template_kwargs={"enable_thinking": False})
        with self.assertRaisesRegex(HarnessError, "Mismatch"):
            ledger.account_producer_response(
                request_id, messages=[{"role": "user", "content": "fixture"}], guard=guard)
        restarted = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
        self.assertEqual(restarted.snapshot()["requests_cumulative"], 6)
        with self.assertRaisesRegex(HarnessError, "durable STOP"):
            restarted.bind_stage("producer_conformity", _binding("producer_conformity", 8))
        self.assertEqual(restarted.snapshot()["requests_cumulative"], 6)


class ProducerRenderingAndAccountingTests(unittest.TestCase):
    def test_only_exact_122b_producer_no_thinking_shape_is_accepted(self):
        from studio2.fase03.harness.d9 import producer_extra_body
        exact = {"chat_template_kwargs": {"enable_thinking": False}}
        self.assertEqual(producer_extra_body(exact, model_role="122B"), exact)
        for invalid in (
            {"chat_template_kwargs": {"enable_thinking": 0}},
            {"chat_template_kwargs": {"enable_thinking": True}},
            {"chat_template_kwargs": {"enable_thinking": False, "other": 1}},
            {"other": {}},
        ):
            with self.subTest(invalid=invalid), self.assertRaises(HarnessError):
                producer_extra_body(invalid, model_role="122B")
        with self.assertRaises(HarnessError):
            producer_extra_body(exact, model_role="27B")
        self.assertEqual(
            __import__("studio2.fase03.harness.d9", fromlist=["generation_kwargs"]).generation_kwargs(
                {"max_tokens": 2560, "thinking_token_budget": 2048}, model_role="122B"),
            {"max_tokens": 2560, "extra_body": {"thinking_token_budget": 2048}},
        )

    def test_accounting_uses_and_commits_exact_transport_template_kwargs(self):
        class Tokenizer:
            def __init__(self):
                self.calls = []

            def apply_chat_template(self, messages, **kwargs):
                self.calls.append((deepcopy(messages), deepcopy(kwargs)))
                return [1] * (11 if kwargs.get("enable_thinking") is False else 12)

        tokenizer = Tokenizer()
        guard = TokenizerAccountingGuard(tokenizer, template_kwargs={"enable_thinking": False})
        result = guard.validate_producer_response(
            [{"role": "user", "content": "fixture"}],
            {"usage": {"prompt_tokens": 11}},
        )
        self.assertEqual(result["local_prompt_tokens"], 11)
        self.assertEqual(tokenizer.calls[0][1]["enable_thinking"], False)
        self.assertEqual(guard.template_kwargs, {"enable_thinking": False})
        with self.assertRaisesRegex(HarnessError, "Mismatch"):
            TokenizerAccountingGuard(tokenizer).validate_producer_response(
                [{"role": "user", "content": "fixture"}],
                {"usage": {"prompt_tokens": 11}},
            )
        with self.assertRaisesRegex(HarnessError, "unsupported chat-template kwargs"):
            TokenizerAccountingGuard(tokenizer, template_kwargs={"enable_thinking": 0})


class ReviewCorrectionLineageTests(unittest.TestCase):
    MUTATIONS = (
        "ordinal", "request_id", "source_kind", "identity_json_and_digest",
        "identity_sha256", "source_binding_sha256", "disposition", "raw_sha256",
        "record_sha256", "package_sha256", "predecessor_sha256", "approval_sha256",
    )

    @staticmethod
    def _new_fixture():
        fixture = SuccessorFixture()
        fixture.setUp()
        return fixture

    def test_F1_direct_reservation_reauthenticates_every_persisted_field(self):
        positive = self._new_fixture()
        try:
            ledger = positive.imported()
            ledger.bind_stage(TECHNICAL_STAGE, _binding(TECHNICAL_STAGE, 1))
            _reserve(ledger, TECHNICAL_STAGE, 0)
            self.assertEqual(ledger.snapshot()["native_requests"], 1)
        finally:
            positive.doCleanups()

        for index, mutation in enumerate(self.MUTATIONS):
            fixture = self._new_fixture()
            try:
                ledger = fixture.imported()
                ledger.bind_stage(TECHNICAL_STAGE, _binding(TECHNICAL_STAGE, 1))
                native_id = _mutate_successor_lineage(ledger, mutation)
                if index % 2:
                    ledger = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
                baseline = _logical(ledger.path)
                request_id = native_id if mutation == "request_id" else "protected-" + mutation
                with self.subTest(mutation=mutation), self.assertRaises(HarnessError):
                    _reserve(ledger, TECHNICAL_STAGE, 0, request_id=request_id)
                self.assertEqual(_logical(ledger.path), baseline)
                with closing(sqlite3.connect(ledger.path)) as connection:
                    self.assertEqual(connection.execute("SELECT count(*) FROM requests").fetchone()[0], 0)
            finally:
                fixture.doCleanups()

    def test_F1_D9_path_reauthenticates_same_instance_and_restart(self):
        from studio2.fase03.harness import d9
        positive = self._new_fixture()
        try:
            ledger = positive.imported()
            package = next(path for path in sorted(positive.home.glob("package-*.json"))
                           if not path.name.endswith("-approval.json"))
            approval = positive.home / (package.stem + "-approval.json")
            config = {"pilot_ledger": {"path": str(ledger.path), "pilot_id": ledger.pilot_id},
                      "d9": {"successor_lineage": {"path": str(package), "sha256": sha256_file(package)},
                             "successor_lineage_approval": {
                                 "path": str(approval), "sha256": sha256_file(approval)}}}
            with mock.patch.object(d9, "validate_config", return_value=config["d9"]):
                with ledger._transaction() as connection:
                    d9.validate_history(config, ledger, connection)
        finally:
            positive.doCleanups()

        for index, mutation in enumerate(self.MUTATIONS):
            fixture = self._new_fixture()
            try:
                ledger = fixture.imported()
                package = next(path for path in sorted(fixture.home.glob("package-*.json"))
                               if not path.name.endswith("-approval.json"))
                approval = fixture.home / (package.stem + "-approval.json")
                config = {"pilot_ledger": {"path": str(ledger.path), "pilot_id": ledger.pilot_id},
                          "d9": {"successor_lineage": {
                                     "path": str(package), "sha256": sha256_file(package)},
                                 "successor_lineage_approval": {
                                     "path": str(approval), "sha256": sha256_file(approval)}}}
                _mutate_successor_lineage(ledger, mutation)
                if index % 2:
                    ledger = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
                baseline = _logical(ledger.path)
                with mock.patch.object(d9, "validate_config", return_value=config["d9"]):
                    with self.subTest(mutation=mutation), self.assertRaises(HarnessError):
                        with ledger._transaction() as connection:
                            d9.validate_history(config, ledger, connection)
                self.assertEqual(_logical(ledger.path), baseline)
                with closing(sqlite3.connect(ledger.path)) as connection:
                    self.assertEqual(connection.execute("SELECT count(*) FROM requests").fetchone()[0], 0)
            finally:
                fixture.doCleanups()


class ReviewCorrectionAccountingTests(SuccessorFixture):
    class Tokenizer:
        def apply_chat_template(self, messages, **kwargs):
            return [1] * 11

    def _completed_technical(self):
        index = len(list(self.home.glob("technical-successor-*.sqlite3")))
        self.successor_path = (self.home / f"technical-successor-{index}.sqlite3").resolve()
        ledger = self.imported()
        binding = _binding(TECHNICAL_STAGE, 1)
        binding["requests"][0]["model"] = "qwen3.5-122b"
        ledger.bind_stage(TECHNICAL_STAGE, binding)
        request_id = _reserve(ledger, TECHNICAL_STAGE, 0)
        messages = [{"role": "user", "content": "fixture"}]
        raw = {
            "id": "fixture", "model": "qwen3.5-122b", "system_fingerprint": "fp",
            "choices": [{"message": {"content": '{"status":"NO_THINKING_OK"}'},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 9, "total_tokens": 20},
        }
        ledger.save_raw(request_id, raw)
        guard = TokenizerAccountingGuard(
            self.Tokenizer(), template_kwargs={"enable_thinking": False})
        ledger.account_producer_response(request_id, messages=messages, guard=guard)
        spec = binding["requests"][0]
        record = {
            "request_id": request_id, "prompt_sha256": spec["prompt_sha256"],
            "response_id": "fixture", "returned_model": "qwen3.5-122b",
            "system_fingerprint": "fp",
            "identity_valid": True, "schema_valid_first_attempt": True,
            "technical_pass": True, "reasoning_empty": True,
            "rendering_control_accepted": True, "scientific_use": "FORBIDDEN",
            "finish_reason": "stop", "raw_output": '{"status":"NO_THINKING_OK"}',
            "prompt_tokens": 11, "completion_tokens": 9, "total_tokens": 20,
        }
        ledger.bind_tokenizer_accounting_record(request_id, record=record)
        ledger.complete_request(request_id, status="COMPLETED", record=record,
                                prompt_tokens=11, completion_tokens=9, total_tokens=20)
        _outcome(ledger, TECHNICAL_STAGE)
        return ledger, request_id

    def test_F2_persisted_accounting_false_to_zero_is_rejected_before_next_stage(self):
        positive, _ = self._completed_technical()
        positive.bind_stage("producer_conformity", _binding("producer_conformity", 8))
        self.assertEqual(positive.snapshot()["native_requests"], 1)

        ledger, request_id = self._completed_technical()
        with ledger._transaction() as connection:
            row = connection.execute(
                "SELECT detail_json FROM events WHERE event=?",
                ("tokenizer_accounting:" + request_id,)).fetchone()
            detail = json.loads(row["detail_json"])
            self.assertIs(detail["chat_template_kwargs"]["enable_thinking"], False)
            detail["chat_template_kwargs"]["enable_thinking"] = 0
            connection.execute("UPDATE events SET detail_json=? WHERE event=?",
                               (canonical_json(detail), "tokenizer_accounting:" + request_id))
        baseline = _logical(ledger.path)
        with self.assertRaises(HarnessError):
            ledger.bind_stage("producer_conformity", _binding("producer_conformity", 8))
        self.assertEqual(_logical(ledger.path), baseline)
        self.assertEqual(ledger.snapshot()["native_requests"], 1)


class SuccessorQuotaTests(SuccessorFixture):
    def test_planned_maximum_166_and_two_processes_compete_for_last_slot(self):
        ledger = self.imported()
        self._pass_technical(ledger)
        ledger.bind_stage("producer_conformity", _binding("producer_conformity", 8))
        for index in range(8):
            _complete(ledger, _reserve(ledger, "producer_conformity", index),
                      schema_valid=index != 0)
        records = ledger.stage_records("producer_conformity")
        artifact = {"records_sha256": digest(records)}
        ledger.record_stage_outcome("producer_conformity", outcome="FAIL",
                                    artifact_sha256=digest(artifact), artifact=artifact,
                                    diagnosis="structure")
        initial = ledger.binding("producer_conformity")
        remediated_template = initial["template_text"] + "APPROVED FIXTURE CHANGE\n"
        diff = "".join(difflib.unified_diff(
            initial["template_text"].splitlines(True), remediated_template.splitlines(True),
            fromfile="before", tofile="after"))
        template_path = self.home / "remediation-template.txt"
        template_path.write_text(remediated_template, encoding="utf-8")
        diff_path = self.home / "remediation.diff"
        diff_path.write_text(diff, encoding="utf-8")
        approval_path = self.home / "remediation-approval.json"
        approval_path.write_text(json.dumps({
            "author": "FIXTURE", "decision": "accepted",
            "diff_sha256": sha256_text(diff),
            "template_sha256": sha256_text(remediated_template),
            "initial_binding_sha256": digest(initial), "diagnosis": "structure",
        }), encoding="utf-8")
        ledger.authorize_remediation(diff_path=diff_path, approval_path=approval_path,
                                     template_path=template_path)
        remediation = deepcopy(initial)
        remediation["template_text"] = remediated_template
        ledger.bind_stage("producer_remediation", remediation)
        first = _reserve(ledger, "producer_remediation", 0)
        serial = 0
        _zero(ledger, first, self.home, serial)
        current = first
        for index in range(7):
            serial += 1
            row = ledger.request(current)
            request_id = f"transport-{index}"
            ledger.reserve_transport_retry(request_id=request_id, logical_id=row["logical_id"],
                                           model=row["model"], producer=row["producer"],
                                           stage=row["stage"], stage_run=row["stage_run"], retry_of=current)
            current = request_id
            if index < 6:
                _zero(ledger, current, self.home, serial)
            else:
                _complete(ledger, current)
        for index in range(1, 8):
            _complete(ledger, _reserve(ledger, "producer_remediation", index))
        _outcome(ledger, "producer_remediation")
        ledger.bind_stage("alternate_conformity", _binding("alternate_conformity", 8))
        for index in range(8):
            _complete(ledger, _reserve(ledger, "alternate_conformity", index))
        _outcome(ledger, "alternate_conformity")
        ledger.bind_stage("budget_probe", _binding("budget_probe", 9))
        for index in range(9):
            request_id = _reserve(ledger, "budget_probe", index)
            record = _complete(ledger, request_id, finish_reason="length" if index < 6 else "stop")
            record["parse_valid_first_attempt"] = True
            record["generation"] = {"max_tokens": 2560}
            with ledger._transaction() as connection:
                text = canonical_json(record)
                connection.execute("UPDATE responses SET record_json=?,record_sha256=? WHERE request_id=?",
                                   (text, sha256_text(text), request_id))
        records = ledger.stage_records("budget_probe")
        artifact = {"records_sha256": digest(records)}
        frozen = {"generation": {"max_tokens": 2560}, "prompt_sample": []}
        ledger.record_stage_outcome("budget_probe", outcome="PASS",
                                    artifact_sha256=digest(artifact), artifact=artifact, frozen=frozen)
        ledger.bind_stage("stability_gate", _binding("stability_gate", 120))
        for index in range(119):
            _complete(ledger, _reserve(ledger, "stability_gate", index))
        self.assertEqual(ledger.snapshot()["requests_cumulative"], 165)
        queue = multiprocessing.Queue()
        processes = [multiprocessing.Process(target=_reserve_worker,
                     args=(str(ledger.path), ledger.pilot_id, queue)) for _ in range(2)]
        for process in processes:
            process.start()
        for process in processes:
            process.join(20)
        results = [queue.get(timeout=2) for _ in processes]
        self.assertEqual(results.count("OK"), 1, results)
        snapshot = PilotLedger(ledger.path, pilot_id=ledger.pilot_id).snapshot()
        self.assertEqual(snapshot["requests_cumulative"], 166)
        self.assertEqual(snapshot["planned_maximum_with_alternate"], 166)
        self.assertEqual(snapshot["hard_stop"], 200)
        self.assertEqual(snapshot["hard_stop_margin_at_planned_maximum"], 34)


class EntrypointFailClosedTests(unittest.TestCase):
    def test_direct_and_cli_refuse_unapproved_successor_before_transport_or_ledger(self):
        from studio2.fase03 import technical_qualification_122b as tq
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            config = home / "candidate.json"
            config.write_text(json.dumps({"status": "READY_FOR_INDEPENDENT_REVIEW"}), encoding="utf-8")
            calls = []
            with self.assertRaises(HarnessError):
                tq.run(config_path=config, provider_path=home / "missing-provider.json",
                       ledger_path=(home / "direct.sqlite3").resolve(), pilot_id="successor-direct",
                       snapshot=home / "missing-snapshot", results_dir=home / "results",
                       transport=lambda payload: calls.append(payload))
            self.assertEqual(calls, [])
            self.assertFalse((home / "direct.sqlite3").exists())
            argv = ["technical_qualification_122b.py", "--config", str(config),
                    "--provider-config", str(home / "missing-provider.json"),
                    "--ledger", str((home / "cli.sqlite3").resolve()),
                    "--pilot-id", "successor-cli",
                    "--model-snapshot", str(home / "missing-snapshot"),
                    "--results-dir", str(home / "results"), "--execute",
                    "--acknowledge", tq.ACK]
            with mock.patch.object(tq.sys, "argv", argv), self.assertRaises(HarnessError):
                tq.main()
            self.assertFalse((home / "cli.sqlite3").exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
