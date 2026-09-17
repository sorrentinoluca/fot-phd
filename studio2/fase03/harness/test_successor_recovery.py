"""Successor 122B recovery contract. All calls and approvals are offline fixtures."""
from __future__ import annotations

from contextlib import closing
from copy import deepcopy
import difflib
import inspect
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


def _realign_accounting_links(ledger: PilotLedger, request_id: str, mutation: str) -> None:
    """Make an accounting mutation internally hash-consistent, as in the R2 review."""
    with ledger._transaction() as connection:
        event_name = "tokenizer_accounting:" + request_id
        row = connection.execute(
            "SELECT detail_json FROM events WHERE event=?", (event_name,)).fetchone()
        detail = json.loads(row["detail_json"])
        if mutation == "messages":
            detail["messages"] = [{"role": "user", "content": "mutated"}]
            detail["messages_sha256"] = sha256_text(canonical_json(detail["messages"]))
        elif mutation in {"local_prompt_tokens", "server_prompt_tokens"}:
            detail[mutation] += 1
        elif mutation == "snapshot":
            detail[mutation] = "Qwen/forged@snapshot"
        elif mutation == "request_identity_sha256":
            detail[mutation] = "8" * 64
        elif mutation == "artifact_version":
            detail[mutation] = "TOKENIZER_ACCOUNTING_FORGED"
        elif mutation == "raw_response_sha256":
            detail[mutation] = "9" * 64
        else:
            raise AssertionError("unknown accounting mutation: " + mutation)
        commitment = digest(detail)
        connection.execute(
            "UPDATE events SET artifact_sha256=?,detail_json=? WHERE event=?",
            (commitment, canonical_json(detail), event_name))
        connection.execute(
            "UPDATE requests SET proof_sha256=? WHERE request_id=?",
            (commitment, request_id))
        link_name = "tokenizer_accounting_record:" + request_id
        link_row = connection.execute(
            "SELECT detail_json FROM events WHERE event=?", (link_name,)).fetchone()
        link = json.loads(link_row["detail_json"])
        link["accounting_commitment_sha256"] = commitment
        connection.execute(
            "UPDATE events SET artifact_sha256=?,detail_json=? WHERE event=?",
            (digest(link), canonical_json(link), link_name))


def _replace_accounting_kwargs(ledger: PilotLedger, request_id: str, value) -> None:
    """Replace/remove kwargs while keeping every internal accounting link coherent."""
    with ledger._transaction() as connection:
        event_name = "tokenizer_accounting:" + request_id
        row = connection.execute(
            "SELECT detail_json FROM events WHERE event=?", (event_name,)).fetchone()
        detail = json.loads(row["detail_json"])
        if value is None:
            detail.pop("chat_template_kwargs", None)
        else:
            detail["chat_template_kwargs"] = deepcopy(value)
        commitment = digest(detail)
        connection.execute(
            "UPDATE events SET artifact_sha256=?,detail_json=? WHERE event=?",
            (commitment, canonical_json(detail), event_name))
        connection.execute(
            "UPDATE requests SET proof_sha256=? WHERE request_id=?",
            (commitment, request_id))
        link_name = "tokenizer_accounting_record:" + request_id
        row = connection.execute(
            "SELECT detail_json FROM events WHERE event=?", (link_name,)).fetchone()
        link = json.loads(row["detail_json"])
        link["accounting_commitment_sha256"] = commitment
        connection.execute(
            "UPDATE events SET artifact_sha256=?,detail_json=? WHERE event=?",
            (digest(link), canonical_json(link), link_name))


def _mutate_accounting_request_discriminator(
        ledger: PilotLedger, request_id: str, mutation: str) -> None:
    """Mutate one request discriminator; keep unrelated accounting links coherent."""
    with ledger._transaction() as connection:
        if mutation == "model":
            connection.execute(
                "UPDATE requests SET model='qwen3.5-27b' WHERE request_id=?", (request_id,))
        elif mutation == "stage":
            connection.execute(
                "UPDATE requests SET stage='budget_probe' WHERE request_id=?", (request_id,))
        elif mutation == "stage_run":
            connection.execute(
                "UPDATE requests SET stage_run=? WHERE request_id=?", ("e" * 64, request_id))
        elif mutation == "producer":
            connection.execute(
                "UPDATE requests SET producer='mutated-producer' WHERE request_id=?",
                (request_id,))
        elif mutation == "identity":
            request = connection.execute(
                "SELECT identity_json FROM requests WHERE request_id=?", (request_id,)).fetchone()
            identity = json.loads(request["identity_json"])
            identity["case_sha256"] = "f" * 64
            identity_json = canonical_json(identity)
            connection.execute(
                "UPDATE requests SET identity_json=? WHERE request_id=?",
                (identity_json, request_id))
            event_name = "tokenizer_accounting:" + request_id
            event = connection.execute(
                "SELECT detail_json FROM events WHERE event=?", (event_name,)).fetchone()
            detail = json.loads(event["detail_json"])
            detail["request_identity_sha256"] = sha256_text(identity_json)
            commitment = digest(detail)
            connection.execute(
                "UPDATE events SET artifact_sha256=?,detail_json=? WHERE event=?",
                (commitment, canonical_json(detail), event_name))
            connection.execute(
                "UPDATE requests SET proof_sha256=? WHERE request_id=?",
                (commitment, request_id))
            link_name = "tokenizer_accounting_record:" + request_id
            link_row = connection.execute(
                "SELECT detail_json FROM events WHERE event=?", (link_name,)).fetchone()
            link = json.loads(link_row["detail_json"])
            link["request_identity_sha256"] = sha256_text(identity_json)
            link["accounting_commitment_sha256"] = commitment
            connection.execute(
                "UPDATE events SET artifact_sha256=?,detail_json=? WHERE event=?",
                (digest(link), canonical_json(link), link_name))
        else:
            raise AssertionError("unknown request discriminator: " + mutation)


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

    def test_C1_technical_contract_and_provider_require_extra_body(self):
        from studio2.fase03 import technical_qualification_122b as tq
        from studio2.fase03.harness import d9
        configured = tq.technical_contract()
        self.assertEqual(tq._validate_contract({"d9": {
            "technical_qualification_122b": configured}}), configured)
        missing = deepcopy(configured)
        missing.pop("extra_body")
        with self.assertRaisesRegex(HarnessError, "extra_body"):
            tq._validate_contract({"d9": {"technical_qualification_122b": missing}})
        service = {
            "model": "qwen3.5-122b", "base_url": "http://fixture.invalid/v1",
            "identity_sha256": "a" * 64, "tokenizer": {},
            "expected_response": {
                "returned_model": "qwen3.5-122b", "system_fingerprint": None},
            "max_model_len": 32768, "max_output_tokens": 4096,
        }
        provider = {
            "name": "fixture", "base_url": service["base_url"],
            "model": service["model"], "max_tokens": 2560,
            "expected_max_model_len": service["max_model_len"],
            "identity_sha256": service["identity_sha256"],
            "expected_response": service["expected_response"], "tokenizer": {},
        }
        file_sha = "b" * 64
        d = {
            "successor_lineage": {"path": "/fixture", "sha256": "c" * 64},
            "services": {"122B": service}, "producer_configs": {"122B": file_sha},
            "alternate_placement": "deferred",
        }
        with mock.patch.object(d9, "validate_config", return_value=d):
            with self.assertRaisesRegex(HarnessError, "extra_body"):
                d9.validate_provider({}, provider, TECHNICAL_STAGE, file_sha256=file_sha)
            provider["extra_body"] = deepcopy(tq.NO_THINKING_EXTRA_BODY)
            self.assertEqual(d9.validate_provider(
                {}, provider, TECHNICAL_STAGE, file_sha256=file_sha), "122B")

    def test_C2_successor_122b_conformity_requires_exact_no_thinking(self):
        from studio2.fase03.harness import d9
        service = {
            "model": "qwen3.5-122b", "base_url": "http://fixture.invalid/v1",
            "identity_sha256": "a" * 64, "tokenizer": {},
            "expected_response": {
                "returned_model": "qwen3.5-122b", "system_fingerprint": None},
            "max_model_len": 32768, "max_output_tokens": 4096,
        }
        file_sha = "b" * 64
        contract = {
            "successor_lineage": {"path": "/fixture", "sha256": "d" * 64},
            "services": {"122B": service, "27B": deepcopy(service)},
            "producer_configs": {"122B": file_sha, "27B": "c" * 64},
            "alternate_placement": "deferred",
        }
        provider = {
            "name": "fixture", "model": service["model"],
            "base_url": service["base_url"], "identity_sha256": service["identity_sha256"],
            "tokenizer": service["tokenizer"], "expected_response": service["expected_response"],
            "expected_max_model_len": service["max_model_len"], "max_tokens": 2560,
        }
        with mock.patch.object(d9, "validate_config", return_value=contract):
            for invalid in (None,
                            {"chat_template_kwargs": {"enable_thinking": 0}},
                            {"chat_template_kwargs": {"enable_thinking": True}},
                            {"chat_template_kwargs": {"enable_thinking": False, "other": 1}},
                            {"other": {}}):
                candidate = deepcopy(provider)
                if invalid is not None:
                    candidate["extra_body"] = invalid
                with self.subTest(invalid=invalid), self.assertRaises(HarnessError):
                    d9.validate_provider({}, candidate, "producer_conformity",
                                         file_sha256=file_sha)
            accepted = deepcopy(provider)
            accepted["extra_body"] = {
                "chat_template_kwargs": {"enable_thinking": False}}
            self.assertEqual(d9.validate_provider(
                {}, accepted, "producer_conformity", file_sha256=file_sha), "122B")
            alternate = deepcopy(provider)
            alternate.update(model="fixture-27b")
            contract["services"]["27B"] = dict(service, model="fixture-27b")
            contract["producer_configs"]["27B"] = "c" * 64
            contract["alternate_placement"] = "pilot"
            self.assertEqual(d9.validate_provider(
                {}, alternate, "alternate_conformity", file_sha256="c" * 64), "27B")


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


class ReverificationRequiredLineageTests(unittest.TestCase):
    @staticmethod
    def _fixture():
        from studio2.fase03.harness import d9, guards
        fixture = SuccessorFixture()
        fixture.setUp()
        ledger = PilotLedger(fixture.successor_path, pilot_id=fixture.successor_id)
        package, approval = fixture.lineage_files()
        service = {
            "model": "qwen3.5-122b", "base_url": "http://fixture.invalid/v1",
            "identity_sha256": "a" * 64, "tokenizer": {},
            "expected_response": {
                "returned_model": "qwen3.5-122b", "system_fingerprint": None},
            "max_model_len": 32768, "max_output_tokens": 4096,
        }
        provider = {
            "name": "fixture-producer", "model": service["model"],
            "base_url": service["base_url"], "identity_sha256": service["identity_sha256"],
            "tokenizer": {}, "expected_response": service["expected_response"],
            "expected_max_model_len": service["max_model_len"], "max_tokens": 2560,
            "extra_body": {"chat_template_kwargs": {"enable_thinking": False}},
        }
        provider_path = fixture.home / "provider.json"
        provider_path.write_text(json.dumps(provider), encoding="utf-8")
        provider_sha = sha256_file(provider_path)
        d = {
            "successor_lineage": {"path": str(package), "sha256": sha256_file(package)},
            "successor_lineage_approval": {
                "path": str(approval), "sha256": sha256_file(approval)},
            "services": {"122B": service}, "producer_configs": {"122B": provider_sha},
            "alternate_placement": "deferred", "r4_snapshot": str(fixture.home),
        }
        config = {
            "pilot_ledger": {"path": str(ledger.path), "pilot_id": ledger.pilot_id},
            "d9": d,
        }
        binding = _binding(TECHNICAL_STAGE, 1)
        binding["requests"][0].update(
            model=provider["model"], producer=provider["name"])
        binding.update(
            execution_config=config, provider=provider, tokenizer={},
            tokenizer_snapshot=str(fixture.home.resolve()),
            provider_file_sha256=provider_sha,
            provider_reference={"path": str(provider_path.resolve()), "sha256": provider_sha},
        )
        patches = (
            mock.patch.object(d9, "validate_config", return_value=d),
            mock.patch.object(guards, "require_execution", return_value=None),
            mock.patch.object(guards, "verify_tokenizer", return_value=None),
        )
        return fixture, ledger, package, approval, config, binding, patches

    def test_R1_D9_requires_import_before_preflight_binding_and_reservation(self):
        from studio2.fase03.harness import d9, guards
        operations = ("direct", "preflight", "preflight_restart", "binding", "reservation")
        for operation in operations:
            fixture, ledger, package, approval, config, binding, patches = self._fixture()
            started = []
            try:
                for patcher in patches:
                    patcher.start()
                    started.append(patcher)
                if operation == "reservation":
                    with ledger._transaction() as connection:
                        connection.execute("INSERT INTO stages VALUES (?,?,?)", (
                            TECHNICAL_STAGE, canonical_json(binding), digest(binding)))
                if operation == "preflight_restart":
                    ledger = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
                before = _logical(ledger.path)
                with self.subTest(operation=operation), self.assertRaisesRegex(
                        HarnessError, "successor lineage import is required"):
                    if operation == "direct":
                        with ledger._transaction() as connection:
                            ledger._validated_predecessor_lineage(
                                connection, package_path=package, approval_path=approval)
                    elif operation.startswith("preflight"):
                        guards.require_pilot_ledger(config, ledger)
                    elif operation == "binding":
                        ledger.bind_stage(TECHNICAL_STAGE, binding)
                    else:
                        _reserve(ledger, TECHNICAL_STAGE, 0)
                self.assertEqual(_logical(ledger.path), before)
                with closing(sqlite3.connect(ledger.path)) as connection:
                    self.assertEqual(connection.execute(
                        "SELECT count(*) FROM requests").fetchone()[0], 0)
            finally:
                for patcher in reversed(started):
                    patcher.stop()
                fixture.doCleanups()

        fixture, ledger, package, approval, config, binding, patches = self._fixture()
        started = []
        try:
            for patcher in patches:
                patcher.start()
                started.append(patcher)
            ledger.reconcile_successor_lineage(
                package_path=package, approval_path=approval)
            restarted = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
            guards.require_pilot_ledger(config, restarted)
            restarted.bind_stage(TECHNICAL_STAGE, binding)
            _reserve(restarted, TECHNICAL_STAGE, 0)
            self.assertEqual(restarted.snapshot()["predecessor_lineage_requests"], 5)
            self.assertEqual(restarted.snapshot()["requests_cumulative"], 6)
        finally:
            for patcher in reversed(started):
                patcher.stop()
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
        binding["requests"][0]["prompt_sha256"] = sha256_text("fixture")
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

    def test_R2_closed_technical_reuse_revalidates_full_accounting_contract(self):
        positive, _ = self._completed_technical()
        positive.verify_stage_success(TECHNICAL_STAGE)
        restarted_positive = PilotLedger(positive.path, pilot_id=positive.pilot_id)
        restarted_positive.bind_stage(
            "producer_conformity", _binding("producer_conformity", 8))
        self.assertEqual(restarted_positive.snapshot()["native_requests"], 1)

        mutations = (
            "messages", "local_prompt_tokens", "server_prompt_tokens", "snapshot",
            "request_identity_sha256", "artifact_version", "raw_response_sha256",
        )
        for index, mutation in enumerate(mutations):
            ledger, request_id = self._completed_technical()
            _realign_accounting_links(ledger, request_id, mutation)
            if index % 2:
                ledger = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
            before_verify = _logical(ledger.path)
            with self.subTest(mutation=mutation, operation="verify"), self.assertRaisesRegex(
                    HarnessError, "FATAL_ACCOUNTING_ERROR"):
                ledger.verify_stage_success(TECHNICAL_STAGE)
            self.assertEqual(_logical(ledger.path), before_verify)
            before_bind = _logical(ledger.path)
            with self.subTest(mutation=mutation, operation="next_binding"), self.assertRaises(
                    HarnessError):
                ledger.bind_stage(
                    "producer_conformity", _binding("producer_conformity", 8))
            self.assertEqual(_logical(ledger.path), before_bind)
            with closing(sqlite3.connect(ledger.path)) as connection:
                self.assertEqual(connection.execute(
                    "SELECT count(*) FROM stages WHERE stage='producer_conformity'"
                ).fetchone()[0], 0)


class SuccessorProducerAccountingContractTests(SuccessorFixture):
    class Tokenizer:
        def apply_chat_template(self, messages, **kwargs):
            return [1] * 7

    @staticmethod
    def _messages(index: int) -> list[dict]:
        return [{"role": "user", "content": f"accounting-prompt-{index}"}]

    def _accounting_binding(self, stage: str, *, model: str = "qwen3.5-122b") -> dict:
        binding = _binding(stage, 8 if stage != "budget_probe" else 3)
        for index, spec in enumerate(binding["requests"]):
            spec["model"] = model
            spec["prompt_sha256"] = sha256_text(self._messages(index)[0]["content"])
        return binding

    @staticmethod
    def _raw(model: str = "qwen3.5-122b") -> dict:
        return {
            "id": "fixture", "model": model, "system_fingerprint": "fp",
            "choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 7, "completion_tokens": 1, "total_tokens": 8},
        }

    def _account_and_complete(self, ledger: PilotLedger, stage: str, index: int, *,
                              kwargs=None, schema_valid: bool = True) -> tuple[str, dict]:
        request_id = _reserve(ledger, stage, index)
        row = ledger.request(request_id)
        ledger.save_raw(request_id, self._raw(row["model"]))
        guard = TokenizerAccountingGuard(self.Tokenizer(), template_kwargs=kwargs)
        ledger.account_producer_response(
            request_id, messages=self._messages(index), guard=guard)
        identity = json.loads(row["identity_json"])
        record = {
            "request_id": request_id, "prompt_sha256": identity["prompt_sha256"],
            "response_id": "fixture", "returned_model": row["model"],
            "system_fingerprint": "fp", "identity_valid": True,
            "schema_valid_first_attempt": schema_valid,
            "validation_class": None if schema_valid else "structure",
            "finish_reason": "stop", "raw_output": "{}",
            "prompt_tokens": 7, "completion_tokens": 1, "total_tokens": 8,
        }
        ledger.bind_tokenizer_accounting_record(request_id, record=record)
        ledger.complete_request(
            request_id, status="COMPLETED", record=record,
            prompt_tokens=7, completion_tokens=1, total_tokens=8)
        return request_id, record

    def _fresh_successor(self) -> PilotLedger:
        index = len(list(self.home.glob("accounting-successor-*.sqlite3")))
        self.successor_path = (
            self.home / f"accounting-successor-{index}.sqlite3").resolve()
        return self.imported()

    def _successor_producer(self) -> tuple[PilotLedger, dict]:
        ledger = self._fresh_successor()
        self._pass_technical(ledger)
        binding = self._accounting_binding("producer_conformity")
        ledger.bind_stage("producer_conformity", binding)
        return ledger, binding

    def _completed_successor_producer(self) -> tuple[PilotLedger, str, dict]:
        ledger, _ = self._successor_producer()
        request_id, record = self._account_and_complete(
            ledger, "producer_conformity", 0,
            kwargs={"enable_thinking": False})
        return ledger, request_id, record

    def _authorize_remediation(self, ledger: PilotLedger) -> dict:
        initial = ledger.binding("producer_conformity")
        template = initial["template_text"] + "APPROVED ACCOUNTING FIXTURE\n"
        diff = "".join(difflib.unified_diff(
            initial["template_text"].splitlines(True), template.splitlines(True),
            fromfile="before", tofile="after"))
        template_path = self.home / "accounting-remediation-template.txt"
        diff_path = self.home / "accounting-remediation.diff"
        approval_path = self.home / "accounting-remediation-approval.json"
        template_path.write_text(template, encoding="utf-8")
        diff_path.write_text(diff, encoding="utf-8")
        approval_path.write_text(json.dumps({
            "author": "FIXTURE", "decision": "accepted",
            "diff_sha256": sha256_text(diff), "template_sha256": sha256_text(template),
            "initial_binding_sha256": digest(initial), "diagnosis": "structure",
        }), encoding="utf-8")
        ledger.authorize_remediation(
            diff_path=diff_path, approval_path=approval_path, template_path=template_path)
        remediation = deepcopy(initial)
        remediation["template_text"] = template
        ledger.bind_stage("producer_remediation", remediation)
        return remediation

    def test_P1_first_successor_producer_acquisition_requires_exact_false(self):
        ledger, _ = self._successor_producer()
        request_id = _reserve(ledger, "producer_conformity", 0)
        ledger.save_raw(request_id, self._raw())
        with self.assertRaisesRegex(HarnessError, "no-thinking"):
            ledger.account_producer_response(
                request_id, messages=self._messages(0),
                guard=TokenizerAccountingGuard(self.Tokenizer()))
        self.assertIsNone(ledger.event("tokenizer_accounting:" + request_id))
        self.assertIsNone(ledger.request(request_id)["proof_sha256"])

        positive, _ = self._successor_producer()
        first, record = self._account_and_complete(
            positive, "producer_conformity", 0,
            kwargs={"enable_thinking": False})
        restarted = PilotLedger(positive.path, pilot_id=positive.pilot_id)
        restarted.validate_tokenizer_accounting_record(first, record=record)
        second = _reserve(restarted, "producer_conformity", 1)
        self.assertEqual(restarted.request(second)["status"], "INTENT")

    def test_P2_reopened_nonconforming_proof_blocks_reuse_and_next_request(self):
        invalid_values = (
            None,
            {"enable_thinking": 0},
            {"enable_thinking": True},
            {"enable_thinking": False, "other": 1},
            {"other": False},
        )
        for invalid in invalid_values:
            ledger, _ = self._successor_producer()
            request_id, record = self._account_and_complete(
                ledger, "producer_conformity", 0,
                kwargs={"enable_thinking": False})
            _replace_accounting_kwargs(ledger, request_id, invalid)
            restarted = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
            baseline = _logical(restarted.path)
            with self.subTest(invalid=invalid, operation="reuse"), self.assertRaisesRegex(
                    HarnessError, "FATAL_ACCOUNTING_ERROR"):
                restarted.validate_tokenizer_accounting_record(request_id, record=record)
            self.assertEqual(_logical(restarted.path), baseline)
            binding = restarted.binding("producer_conformity")
            with self.subTest(invalid=invalid, operation="binding"), self.assertRaisesRegex(
                    HarnessError, "FATAL_ACCOUNTING_ERROR"):
                restarted.bind_stage("producer_conformity", binding)
            self.assertEqual(_logical(restarted.path), baseline)
            with self.subTest(invalid=invalid, operation="reservation"), self.assertRaisesRegex(
                    HarnessError, "FATAL_ACCOUNTING_ERROR"):
                _reserve(restarted, "producer_conformity", 1)
            self.assertEqual(_logical(restarted.path), baseline)
            with closing(sqlite3.connect(restarted.path)) as connection:
                self.assertEqual(connection.execute(
                    "SELECT count(*) FROM requests WHERE stage='producer_conformity'"
                ).fetchone()[0], 1)

    def test_P3_successor_122b_remediation_acquisition_requires_exact_false(self):
        ledger, _ = self._successor_producer()
        for index in range(8):
            self._account_and_complete(
                ledger, "producer_conformity", index,
                kwargs={"enable_thinking": False}, schema_valid=index != 0)
        records = ledger.stage_records("producer_conformity")
        artifact = {"records_sha256": digest(records)}
        ledger.record_stage_outcome(
            "producer_conformity", outcome="FAIL", artifact_sha256=digest(artifact),
            artifact=artifact, diagnosis="structure")
        self._authorize_remediation(ledger)
        request_id = _reserve(ledger, "producer_remediation", 0)
        ledger.save_raw(request_id, self._raw())
        with self.assertRaisesRegex(HarnessError, "no-thinking"):
            ledger.account_producer_response(
                request_id, messages=self._messages(0),
                guard=TokenizerAccountingGuard(self.Tokenizer()))
        self.assertIsNone(ledger.event("tokenizer_accounting:" + request_id))
        self.assertIsNone(ledger.request(request_id)["proof_sha256"])

    def test_P4_generic_consumer_and_27b_paths_remain_unchanged(self):
        generic = PilotLedger(
            self.home / "generic.sqlite3", pilot_id="generic-accounting")
        generic_binding = self._accounting_binding("producer_conformity")
        generic.bind_stage("producer_conformity", generic_binding)
        generic_id, _ = self._account_and_complete(
            generic, "producer_conformity", 0, kwargs=None)
        self.assertNotIn(
            "chat_template_kwargs",
            generic.event("tokenizer_accounting:" + generic_id))

        consumer = self._fresh_successor()
        self._pass_technical(consumer)
        consumer.bind_stage("producer_conformity", _binding("producer_conformity", 8))
        for index in range(8):
            _complete(consumer, _reserve(consumer, "producer_conformity", index))
        _outcome(consumer, "producer_conformity")
        consumer.bind_stage("budget_probe", self._accounting_binding("budget_probe"))
        consumer_id, _ = self._account_and_complete(
            consumer, "budget_probe", 0, kwargs=None)
        self.assertNotIn(
            "chat_template_kwargs",
            consumer.event("tokenizer_accounting:" + consumer_id))

        alternate = self._fresh_successor()
        self._pass_technical(alternate)
        alternate.bind_stage(
            "alternate_conformity",
            self._accounting_binding("alternate_conformity", model="qwen3.5-27b"))
        alternate_id = _reserve(alternate, "alternate_conformity", 0)
        _complete(alternate, alternate_id)
        self.assertIsNone(alternate.event("tokenizer_accounting:" + alternate_id))

    def test_Q1_version_lineage_incoherence_fails_all_decision_paths(self):
        from studio2.fase03.harness import d9, guards

        operations = ("direct", "rebind", "reservation", "quota", "snapshot", "preflight")
        for version in (2, 3):
            for operation in operations:
                ledger, request_id, record = self._completed_successor_producer()
                _replace_accounting_kwargs(ledger, request_id, None)
                with ledger._transaction() as connection:
                    event = connection.execute(
                        "SELECT detail_json FROM events WHERE event LIKE 'successor_lineage:%'"
                    ).fetchone()
                    lineage = json.loads(event["detail_json"])
                    connection.execute(f"PRAGMA user_version={version}")
                restarted = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
                baseline = _logical(restarted.path)
                config = {
                    "pilot_ledger": {
                        "path": str(restarted.path), "pilot_id": restarted.pilot_id},
                }
                d = {
                    "successor_lineage": lineage["package_reference"],
                    "successor_lineage_approval": lineage["approval_reference"],
                }
                with self.subTest(version=version, operation=operation):
                    with self.assertRaises(HarnessError):
                        if operation == "direct":
                            restarted.validate_tokenizer_accounting_record(
                                request_id, record=record)
                        elif operation == "rebind":
                            restarted.bind_stage(
                                "producer_conformity",
                                restarted.binding("producer_conformity"))
                        elif operation == "reservation":
                            _reserve(restarted, "producer_conformity", 1)
                        elif operation == "quota":
                            with restarted._transaction() as connection:
                                restarted._quota_predecessors(connection)
                        elif operation == "snapshot":
                            restarted.snapshot()
                        else:
                            with mock.patch.object(d9, "validate_config", return_value=d):
                                guards.require_pilot_ledger(config, restarted)
                    self.assertEqual(_logical(restarted.path), baseline)
                    with closing(sqlite3.connect(restarted.path)) as connection:
                        self.assertEqual(connection.execute(
                            "SELECT count(*) FROM requests WHERE stage='producer_conformity'"
                        ).fetchone()[0], 1)

    def test_Q2_request_discriminators_are_authenticated_before_classification(self):
        mutations = ("model", "stage", "stage_run", "identity", "producer")
        operations = ("direct", "rebind", "reservation")
        for index, mutation in enumerate(mutations):
            for operation in operations:
                ledger, request_id, record = self._completed_successor_producer()
                _replace_accounting_kwargs(ledger, request_id, None)
                _mutate_accounting_request_discriminator(ledger, request_id, mutation)
                if index % 2:
                    ledger = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
                baseline = _logical(ledger.path)
                with self.subTest(mutation=mutation, operation=operation):
                    with self.assertRaises(HarnessError):
                        if operation == "direct":
                            ledger.validate_tokenizer_accounting_record(
                                request_id, record=record)
                        elif operation == "rebind":
                            ledger.bind_stage(
                                "producer_conformity",
                                ledger.binding("producer_conformity"))
                        else:
                            _reserve(ledger, "producer_conformity", 1)
                    self.assertEqual(_logical(ledger.path), baseline)
                    with closing(sqlite3.connect(ledger.path)) as connection:
                        self.assertEqual(connection.execute(
                            "SELECT count(*) FROM requests").fetchone()[0], 2)

    def test_Q3_valid_successor_classification_preserves_five_predecessors(self):
        ledger, request_id, record = self._completed_successor_producer()
        restarted = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
        restarted.validate_tokenizer_accounting_record(request_id, record=record)
        snapshot = restarted.snapshot()
        self.assertEqual(snapshot["predecessor_lineage_requests"], 5)
        self.assertEqual(snapshot["requests_cumulative"], 7)


class PostFailureDiagnosisTests(SuccessorFixture):
    def _closed_producer(self, *, outcome="FAIL", validation_class="identifiers"):
        serial = getattr(self, "_producer_fixture_serial", 0) + 1
        self._producer_fixture_serial = serial
        self.successor_path = (self.home / f"successor-{serial}.sqlite3").resolve()
        self.successor_id = f"successor-fixture-{serial}"
        ledger = self.imported()
        self._pass_technical(ledger)
        ledger.bind_stage("producer_conformity", _binding("producer_conformity", 8))
        for index in range(8):
            request_id = _reserve(ledger, "producer_conformity", index)
            record = _complete(ledger, request_id,
                               schema_valid=outcome == "PASS" or index != 1)
            if outcome == "FAIL" and index == 1:
                record["validation_class"] = validation_class
                with ledger._transaction() as connection:
                    text = canonical_json(record)
                    connection.execute(
                        "UPDATE responses SET record_json=?,record_sha256=? WHERE request_id=?",
                        (text, sha256_text(text), request_id))
        _outcome(ledger, "producer_conformity", outcome)
        return ledger

    def _diagnosis_approval(self, ledger, diagnosis="identifiers", *, name="diagnosis"):
        outcome = ledger.event("outcome:producer_conformity")
        path = self.home / f"{name}.json"
        path.write_text(json.dumps({
            "decision": "accepted", "author": "FIXTURE AUTHOR",
            "diagnosis": diagnosis,
            "records_sha256": outcome["records_sha256"],
        }, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def _remediation_artifacts(self, ledger, diagnosis="identifiers"):
        initial = ledger.binding("producer_conformity")
        template = initial["template_text"] + "APPROVED FIXTURE CHANGE\n"
        diff = "".join(difflib.unified_diff(
            initial["template_text"].splitlines(True), template.splitlines(True),
            fromfile="before", tofile="after"))
        template_path = self.home / "remediation-template.txt"
        template_path.write_text(template, encoding="utf-8")
        diff_path = self.home / "remediation.diff"
        diff_path.write_text(diff, encoding="utf-8")
        approval_path = self.home / "remediation-approval.json"
        approval_path.write_text(json.dumps({
            "author": "FIXTURE", "decision": "accepted",
            "diff_sha256": sha256_text(diff),
            "template_sha256": sha256_text(template),
            "initial_binding_sha256": digest(initial), "diagnosis": diagnosis,
        }), encoding="utf-8")
        return diff_path, approval_path, template_path

    def test_RM1_a_post_fail_diagnosis_unlocks_existing_remediation_contract(self):
        ledger = self._closed_producer()
        diff_path, remediation_approval, template_path = self._remediation_artifacts(ledger)
        with self.assertRaises(HarnessError):
            ledger.authorize_remediation(
                diff_path=diff_path, approval_path=remediation_approval,
                template_path=template_path)
        diagnosis_approval = self._diagnosis_approval(ledger)
        ledger.diagnose_producer_failure(
            diagnosis="identifiers", approval_path=diagnosis_approval)
        diagnosis_event = ledger.event("diagnosis:producer_conformity")
        self.assertEqual(diagnosis_event["approval"]["content"]["diagnosis"],
                         "identifiers")
        diagnosis_approval.unlink()
        ledger.authorize_remediation(
            diff_path=diff_path, approval_path=remediation_approval,
            template_path=template_path)
        self.assertIsNotNone(ledger.event("remediation_authorized"))

    def test_RM1_b_diagnosis_must_match_a_failed_record(self):
        ledger = self._closed_producer(validation_class="identifiers")
        approval = self._diagnosis_approval(ledger, diagnosis="structure")
        baseline = _logical(ledger.path)
        with self.assertRaisesRegex(HarnessError, "diagnosis must match"):
            ledger.diagnose_producer_failure(
                diagnosis="structure", approval_path=approval)
        self.assertEqual(_logical(ledger.path), baseline)
        self.assertIsNone(ledger.event("diagnosis:producer_conformity"))

        correct = self._diagnosis_approval(
            ledger, diagnosis="identifiers", name="correct-diagnosis")
        with self.assertRaisesRegex(HarnessError, "hash mismatch"):
            ledger.diagnose_producer_failure(
                diagnosis="identifiers", approval_path=correct,
                approval_sha256="0" * 64)
        invalid = json.loads(correct.read_text())
        invalid["records_sha256"] = "1" * 64
        correct.write_text(json.dumps(invalid), encoding="utf-8")
        with self.assertRaisesRegex(HarnessError, "approval must bind"):
            ledger.diagnose_producer_failure(
                diagnosis="identifiers", approval_path=correct)
        self.assertEqual(_logical(ledger.path), baseline)

    def test_RM1_c_diagnosis_rejects_pass_disposition_and_downstream_work(self):
        passing = self._closed_producer(outcome="PASS")
        approval = self._diagnosis_approval(passing)
        with self.assertRaises(HarnessError):
            passing.diagnose_producer_failure(
                diagnosis="identifiers", approval_path=approval)

        authorized = self._closed_producer()
        diagnosis_approval = self._diagnosis_approval(authorized)
        authorized.diagnose_producer_failure(
            diagnosis="identifiers", approval_path=diagnosis_approval)
        diff_path, remediation_approval, template_path = self._remediation_artifacts(authorized)
        authorized.authorize_remediation(
            diff_path=diff_path, approval_path=remediation_approval,
            template_path=template_path)
        with self.assertRaises(HarnessError):
            authorized.diagnose_producer_failure(
                diagnosis="identifiers", approval_path=diagnosis_approval)

        waived = self._closed_producer()
        waived_approval = self._diagnosis_approval(waived)
        waived.waive_remediation(approval_sha256="a" * 64)
        with self.assertRaises(HarnessError):
            waived.diagnose_producer_failure(
                diagnosis="identifiers", approval_path=waived_approval)

        probed = self._closed_producer()
        probed_approval = self._diagnosis_approval(probed)
        spec = _spec("budget_probe", 0, count=3)
        with probed._transaction() as connection:
            connection.execute(
                "INSERT INTO requests VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                ("probe-blocker", spec["logical_id"], "budget_probe", "b" * 64,
                 spec["model"], spec["producer"], "base", None,
                 canonical_json(spec), "INTENT", "2026-09-17T00:00:00+00:00",
                 None, None, None, None, None, None, None))
        with self.assertRaises(HarnessError):
            probed.diagnose_producer_failure(
                diagnosis="identifiers", approval_path=probed_approval)

    def test_RM1_d_diagnosis_preserves_outcome_stage_and_quota(self):
        ledger = self._closed_producer()
        approval = self._diagnosis_approval(ledger)
        before_snapshot = ledger.snapshot()
        before_outcome = ledger.event("outcome:producer_conformity")
        ledger.diagnose_producer_failure(
            diagnosis="identifiers", approval_path=approval)
        after_snapshot = ledger.snapshot()
        self.assertEqual(ledger.event("outcome:producer_conformity"), before_outcome)
        for key in ("native_requests", "requests_cumulative", "remediation_calls",
                    "transport_calls", "reserve_equation_value"):
            self.assertEqual(after_snapshot[key], before_snapshot[key])
        self.assertEqual(set(after_snapshot["events"]) - set(before_snapshot["events"]),
                         {"diagnosis:producer_conformity"})
        with self.assertRaises(HarnessError):
            _reserve(ledger, "producer_conformity", 0, request_id="cannot-reopen")

    def test_RM1_e_same_approval_bytes_are_idempotent(self):
        ledger = self._closed_producer()
        approval = self._diagnosis_approval(ledger)
        first = ledger.diagnose_producer_failure(
            diagnosis="identifiers", approval_path=approval,
            approval_sha256=sha256_file(approval))
        logical = _logical(ledger.path)
        second = ledger.diagnose_producer_failure(
            diagnosis="identifiers", approval_path=approval,
            approval_sha256=sha256_file(approval))
        self.assertEqual(first, second)
        self.assertEqual(_logical(ledger.path), logical)
        with closing(sqlite3.connect(ledger.path)) as connection:
            self.assertEqual(connection.execute(
                "SELECT count(*) FROM events WHERE event='diagnosis:producer_conformity'"
            ).fetchone()[0], 1)


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


class BlockingCorrectionTests(SuccessorFixture):
    class Tokenizer:
        def apply_chat_template(self, messages, **kwargs):
            return [1] * 11

    def _one_accounted_producer_request(self):
        ledger = self.imported()
        self._pass_technical(ledger)
        binding = _binding("producer_conformity", 8)
        for index, spec in enumerate(binding["requests"]):
            spec["model"] = "qwen3.5-122b"
            spec["prompt_sha256"] = sha256_text(f"original-{index}")
        ledger.bind_stage("producer_conformity", binding)
        request_id = _reserve(ledger, "producer_conformity", 0)
        messages = [{"role": "user", "content": "original-0"}]
        raw = {
            "id": "accounted", "model": "qwen3.5-122b",
            "system_fingerprint": "fp",
            "choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 1,
                      "total_tokens": 12},
        }
        guard = TokenizerAccountingGuard(
            self.Tokenizer(), template_kwargs={"enable_thinking": False})
        ledger.save_raw(request_id, raw)
        ledger.account_producer_response(request_id, messages=messages, guard=guard)
        identity = json.loads(ledger.request(request_id)["identity_json"])
        record = {
            "request_id": request_id, "prompt_sha256": identity["prompt_sha256"],
            "response_id": raw["id"], "returned_model": raw["model"],
            "system_fingerprint": "fp", "identity_valid": True,
            "schema_valid_first_attempt": True, "finish_reason": "stop",
            "raw_output": "{}", "prompt_tokens": 11,
            "completion_tokens": 1, "total_tokens": 12,
        }
        ledger.bind_tokenizer_accounting_record(request_id, record=record)
        ledger.complete_request(
            request_id, status="COMPLETED", record=record,
            prompt_tokens=11, completion_tokens=1, total_tokens=12)
        return ledger, guard, binding["requests"][0]["logical_id"]

    def test_REM3_accounting_expected_messages_are_scoped_by_stage_and_logical_id(self):
        ledger, guard, logical_id = self._one_accounted_producer_request()
        remediation_messages = [{"role": "user", "content": "remediated-0"}]
        ledger.validate_tokenizer_accounting_evidence(
            guard, expected_stage="producer_remediation",
            expected_messages={logical_id: remediation_messages})
        self.assertIsNone(ledger.event("stop:tokenizer_accounting"))

    def test_REM3_same_stage_message_mismatch_remains_a_durable_stop(self):
        ledger, guard, logical_id = self._one_accounted_producer_request()
        changed_messages = [{"role": "user", "content": "changed-0"}]
        with self.assertRaisesRegex(HarnessError, "persisted accounting messages are invalid"):
            ledger.validate_tokenizer_accounting_evidence(
                guard, expected_stage="producer_conformity",
                expected_messages={logical_id: changed_messages})
        self.assertIsNotNone(ledger.event("stop:tokenizer_accounting"))

    def test_P1_02a_materializer_requires_explicit_gate_before_work(self):
        from studio2.fase03 import materialize_successor_recovery as materializer

        self.assertIn("argv", inspect.signature(materializer.main).parameters)
        with mock.patch.object(materializer, "materialize") as execute:
            with self.assertRaises(SystemExit):
                materializer.main([])
            execute.assert_not_called()
            with self.assertRaises(SystemExit):
                materializer.main(["--execute", "--acknowledge", "WRONG"])
            execute.assert_not_called()
            self.assertEqual(materializer.main([
                "--execute", "--acknowledge", materializer.ACK]), 0)
            execute.assert_called_once_with()

    def test_P1_02b_staging_failure_never_publishes_partial_target(self):
        from studio2.fase03 import materialize_successor_recovery as materializer

        publish = getattr(materializer, "_publish_staged", None)
        self.assertTrue(callable(publish), "materializer lacks atomic staged publication")
        target = self.home / "fresh-successor"
        with mock.patch.object(materializer, "TARGET_ROOT", target):
            def fail(staging):
                (staging / "partial").write_text("partial", encoding="utf-8")
                raise RuntimeError("injected materialization failure")

            with self.assertRaisesRegex(RuntimeError, "injected"):
                publish(fail)
            self.assertFalse(target.exists())
            self.assertEqual(list(self.home.glob(".fresh-successor.staging-*")), [])

            publish(lambda staging: (staging / "complete").write_text(
                "complete", encoding="utf-8"))
            self.assertEqual((target / "complete").read_text(encoding="utf-8"), "complete")
            called = []
            with self.assertRaisesRegex(RuntimeError, "already exists"):
                publish(lambda staging: called.append(staging))
            self.assertEqual(called, [])

    def test_identity_sha256_has_one_source_backed_object_and_distinct_file_digests(self):
        from studio2.fase03 import materialize_successor_recovery as materializer
        from studio2.fase03.harness import d9

        build = getattr(materializer, "_response_identity_binding", None)
        self.assertTrue(callable(build), "response identity digest semantics are not explicit")
        binding = build()
        self.assertEqual(
            binding["identity_sha256"],
            "d180061348b15bb0322cb75ae700bb97b1328994c8d572c98741455d5b0ef579")
        self.assertEqual(binding["qualification_supplement_file"]["sha256"],
                         "dd9c53f0e4262fffe592a04298f8d7a4cfd428ccf5c487faacfe68ca357decb7")
        self.assertEqual(binding["qualification_supplement_canonical_sha256"],
                         "79515feb95b1048f67e8c01446be580dcbb73def188a13175b842b58a5356a40")
        self.assertEqual(len({
            binding["identity_sha256"],
            binding["qualification_supplement_file"]["sha256"],
            binding["qualification_supplement_canonical_sha256"],
        }), 3)
        service = {
            "identity_sha256": binding["identity_sha256"],
            "expected_response": {
                "returned_model": "qwen3.5-122b",
                "system_fingerprint": "vllm-0.27.1-934a3247"},
        }
        d9._validate_response_identity_binding(binding, service)
        for field in ("identity_sha256", "qualification_supplement_canonical_sha256"):
            mutated = deepcopy(binding)
            mutated[field] = "0" * 64
            with self.subTest(field=field), self.assertRaises(HarnessError):
                d9._validate_response_identity_binding(mutated, service)

    def test_P2_01_mixed_accounting_uses_authenticated_per_event_guard(self):
        ledger = self.imported()
        self._pass_technical(ledger)
        producer = _binding("producer_conformity", 8)
        for index, spec in enumerate(producer["requests"]):
            spec["model"] = "qwen3.5-122b"
            spec["prompt_sha256"] = sha256_text(f"producer-{index}")
        ledger.bind_stage("producer_conformity", producer)
        for index in range(8):
            request_id = _reserve(ledger, "producer_conformity", index)
            messages = [{"role": "user", "content": f"producer-{index}"}]
            raw = {"id": f"producer-{index}", "model": "qwen3.5-122b",
                   "system_fingerprint": "fp",
                   "choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}],
                   "usage": {"prompt_tokens": 11, "completion_tokens": 1,
                             "total_tokens": 12}}
            ledger.save_raw(request_id, raw)
            guard = TokenizerAccountingGuard(
                self.Tokenizer(), template_kwargs={"enable_thinking": False})
            ledger.account_producer_response(request_id, messages=messages, guard=guard)
            identity = json.loads(ledger.request(request_id)["identity_json"])
            record = {"request_id": request_id,
                      "prompt_sha256": identity["prompt_sha256"],
                      "response_id": raw["id"], "returned_model": raw["model"],
                      "system_fingerprint": "fp", "identity_valid": True,
                      "schema_valid_first_attempt": True, "finish_reason": "stop",
                      "raw_output": "{}", "prompt_tokens": 11,
                      "completion_tokens": 1, "total_tokens": 12}
            ledger.bind_tokenizer_accounting_record(request_id, record=record)
            ledger.complete_request(request_id, status="COMPLETED", record=record,
                                    prompt_tokens=11, completion_tokens=1, total_tokens=12)
        _outcome(ledger, "producer_conformity")

        consumer = _binding("budget_probe", 3)
        consumer["requests"][0]["model"] = "qwen3.5-122b"
        consumer["requests"][0]["prompt_sha256"] = sha256_text("consumer")
        ledger.bind_stage("budget_probe", consumer)
        request_id = _reserve(ledger, "budget_probe", 0)
        messages = [{"role": "user", "content": "consumer"}]
        raw = {"id": "consumer", "model": "qwen3.5-122b", "system_fingerprint": "fp",
               "choices": [{"message": {"content": "{}"}, "finish_reason": "stop"}],
               "usage": {"prompt_tokens": 11, "completion_tokens": 1, "total_tokens": 12}}
        ledger.save_raw(request_id, raw)
        consumer_guard = TokenizerAccountingGuard(self.Tokenizer())
        ledger.account_producer_response(request_id, messages=messages, guard=consumer_guard)
        identity = json.loads(ledger.request(request_id)["identity_json"])
        record = {"request_id": request_id, "prompt_sha256": identity["prompt_sha256"],
                  "response_id": "consumer", "returned_model": "qwen3.5-122b",
                  "system_fingerprint": "fp", "identity_valid": True,
                  "schema_valid_first_attempt": True, "finish_reason": "stop",
                  "raw_output": "{}", "prompt_tokens": 11,
                  "completion_tokens": 1, "total_tokens": 12}
        ledger.bind_tokenizer_accounting_record(request_id, record=record)
        ledger.complete_request(request_id, status="COMPLETED", record=record,
                                prompt_tokens=11, completion_tokens=1, total_tokens=12)

        restarted = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
        try:
            restarted.validate_tokenizer_accounting_evidence(
                TokenizerAccountingGuard(
                    self.Tokenizer(), template_kwargs={"enable_thinking": False}))
        except HarnessError as exc:
            self.fail(f"mixed producer/consumer accounting produced a false STOP: {exc}")
        self.assertIsNone(restarted.event("stop:tokenizer_accounting"))
        self.assertEqual(restarted.snapshot()["native_requests"], 10)

    def test_P2_02_resume_reconstructs_complete_technical_outcome_without_send(self):
        from studio2.fase03 import technical_qualification_122b as tq
        from studio2.fase03.harness import d9, guards
        from studio2.fase03 import producer_probe

        ledger = self.imported()
        config_path = self.home / "config.json"
        config_path.write_text(json.dumps({"d9": {
            "technical_qualification_122b": tq.technical_contract()}}), encoding="utf-8")
        provider_path = self.home / "provider.json"
        provider_path.write_text("{}", encoding="utf-8")
        provider = {
            "name": "fixture-producer", "model": "qwen3.5-122b",
            "base_url": "http://fixture.invalid/v1", "max_tokens": 2560,
            "expected_max_model_len": 32768, "identity_sha256": "a" * 64,
            "expected_response": {
                "returned_model": "qwen3.5-122b", "system_fingerprint": "fp"},
            "tokenizer": {},
            "extra_body": {"chat_template_kwargs": {"enable_thinking": False}},
        }
        guard = TokenizerAccountingGuard(
            self.Tokenizer(), template_kwargs={"enable_thinking": False})
        raw = {
            "id": "technical", "model": "qwen3.5-122b", "system_fingerprint": "fp",
            "choices": [{"message": {"content": '{"status":"NO_THINKING_OK"}'},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 1, "total_tokens": 12},
        }
        patches = (
            mock.patch.object(guards, "require_execution", return_value=None),
            mock.patch.object(guards, "require_pilot_ledger", return_value=None),
            mock.patch.object(guards, "verify_tokenizer", return_value=None),
            mock.patch.object(producer_probe, "provider_config", return_value=provider),
            mock.patch.object(d9, "validate_provider", return_value="122B"),
            mock.patch.object(d9, "validate_binding", return_value=None),
            mock.patch.object(tq, "load_tokenizer_accounting_guard", return_value=guard),
        )
        started = []
        try:
            for patcher in patches:
                patcher.start()
                started.append(patcher)
            with mock.patch.object(
                    PilotLedger, "record_stage_outcome",
                    side_effect=RuntimeError("injected crash after completed technical record")):
                with self.assertRaisesRegex(RuntimeError, "injected crash"):
                    tq.run(
                        config_path=config_path, provider_path=provider_path,
                        ledger_path=ledger.path, pilot_id=ledger.pilot_id,
                        snapshot=self.home, results_dir=self.home / "results",
                        transport=lambda payload: deepcopy(raw))
            restarted = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
            before = restarted.snapshot()
            calls = []
            try:
                record = tq.run(
                    config_path=config_path, provider_path=provider_path,
                    ledger_path=ledger.path, pilot_id=ledger.pilot_id,
                    snapshot=self.home, results_dir=self.home / "results",
                    transport=lambda payload: calls.append(payload), resume=True)
            except HarnessError as exc:
                self.fail("resume did not reconstruct the complete technical PASS: " + str(exc))
            self.assertTrue(record["technical_pass"])
            self.assertEqual(calls, [])
            after = restarted.snapshot()
            self.assertEqual(after["native_requests"], before["native_requests"])
            self.assertEqual(after["requests_cumulative"], before["requests_cumulative"])
            restarted.verify_stage_success(TECHNICAL_STAGE)
            summary = json.loads((self.home / "results" /
                                  "technical_qualification_122b_summary.json").read_text())
            self.assertEqual(summary["status"], "PASS")
        finally:
            for patcher in reversed(started):
                patcher.stop()


class FreshTargetPilot03Tests(SuccessorFixture):
    """03.13-TARGET: fresh pilot-03 target and deterministic ledger close."""

    EXPECTED_ID = "studio2-fase03-d9-pilot-03"
    EXPECTED_ROOT = Path("/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03")

    def _fixture_sources(self):
        """Offline predecessor root and harness copy; no real runtime path is touched."""
        from studio2.fase03 import materialize_successor_recovery as materializer

        predecessor_root = self.home / "predecessor-root"
        (predecessor_root / "execution").mkdir(parents=True)
        for relative in ("tokenizers/122B-rev/tokenizer.json",
                         "tokenizers/27B/27B-rev/tokenizer.json"):
            path = predecessor_root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text('{"fixture": true}\n', encoding="utf-8")
        tokenizer = {"repository": "fixture/tokenizer", "revision": "122B-rev"}
        service = {"model": "fixture-122b", "base_url": "http://127.0.0.1:9/v1",
                   "tokenizer": tokenizer, "max_model_len": 131072,
                   "max_output_tokens": 2560}
        config = {
            "artifact_version": "FIXTURE", "status": "FIXTURE",
            "candidate": {}, "call_budget": {"historical_nominal_model": "122B"},
            "implementation_status": {},
            "d9": {"services": {"122B": service, "27B": {"model": "fixture-27b"}},
                   "r4_tokenizer": {"revision": "27B-rev"},
                   "history_reconciliation": {}, "history_approval": {}},
        }
        execution = predecessor_root / "execution"
        (execution / "pilot_d9_execution_candidate_03_13.private.json").write_text(
            json.dumps(config), encoding="utf-8")
        (execution / "producer_122b_03_13.private.json").write_text(
            json.dumps({"tokenizer": tokenizer}), encoding="utf-8")
        (execution / "producer_27b_03_13.private.json").write_text(
            '{"fixture": "27B producer"}\n', encoding="utf-8")
        (execution / "service_27b_03_13.private.json").write_text(
            '{"fixture": "27B service"}\n', encoding="utf-8")

        harness = self.home / "harness-copy"
        (harness / "reviews").mkdir(parents=True)
        for name in ("PROPOSTA_RECUPERO_STOP_122B_QWEN_D9_03_13.json",
                     "QUALIFICATION_SUPPLEMENT_122B_QWEN_D9_03_13.json"):
            (harness / name).write_bytes((materializer.HARNESS / name).read_bytes())
        sources = {
            "reviews/VERIFICA_STOP_PRIMA_CHIAMATA_PRODUCER_QWEN_D9_03_13_V2.md": "stop_review_v2",
            "PROPOSTA_RECUPERO_STOP_122B_QWEN_D9_03_13.md": "proposal_md",
            "reviews/VERIFICA_PROPOSTA_RECUPERO_STOP_122B_QWEN_D9_03_13.md": "proposal_review",
            "ACQUISIZIONE_DECISIONE_AUTORE_RECUPERO_SUCCESSOR_122B_QWEN_D9_03_13.json":
                "author_decision",
        }
        for relative, role in sources.items():
            (harness / relative).write_bytes(
                Path(self.evidence[role]["path"]).read_bytes())

        target = (self.home / "runtime" / self.EXPECTED_ID).resolve()
        patches = [
            mock.patch.object(materializer, "PREDECESSOR_ROOT", predecessor_root),
            mock.patch.object(materializer, "PREDECESSOR_LEDGER", self.predecessor.path),
            mock.patch.object(materializer, "PREDECESSOR_SHA256", self.predecessor_sha),
            mock.patch.object(materializer, "PREDECESSOR_PILOT_ID", self.predecessor.pilot_id),
            mock.patch.object(materializer, "AUTHOR_DECISION_TEXT_SHA256",
                              sha256_text("FIXTURE AUTHOR DECISION")),
            mock.patch.object(materializer, "HARNESS", harness),
            mock.patch.object(materializer, "TARGET_ROOT", target),
            mock.patch.object(materializer, "SOURCE_CONFIG",
                              execution / "pilot_d9_execution_candidate_03_13.private.json"),
            mock.patch.object(materializer, "SOURCE_PROVIDER_122B",
                              execution / "producer_122b_03_13.private.json"),
            mock.patch.object(materializer, "SOURCE_PROVIDER_27B",
                              execution / "producer_27b_03_13.private.json"),
            mock.patch.object(materializer, "SOURCE_SERVICE_27B",
                              execution / "service_27b_03_13.private.json"),
            # Full D9 validation is covered elsewhere; here only ledger finalization
            # and publication of the fixture tree are under test.
            mock.patch("studio2.fase03.harness.d9.validate_config"),
        ]
        for patch in patches:
            patch.start()
            self.addCleanup(patch.stop)
        return materializer, target

    def _durable_refs(self, target: Path) -> list[dict]:
        summary = json.loads((target / "MATERIALIZATION_SUMMARY.private.json").read_text(
            encoding="utf-8"))
        refs = [summary[key] for key in (
            "ledger", "configuration", "lineage_package", "lineage_approval",
            "qualification_supplement", "producer_122b", "service_122b")]
        config = json.loads(Path(summary["configuration"]["path"]).read_text(encoding="utf-8"))
        refs.extend([
            config["d9"]["successor_lineage"],
            config["d9"]["successor_lineage_approval"],
            config["d9"]["services"]["122B"]["documentation"],
            config["d9"]["services"]["27B"]["documentation"],
        ])
        for ref in refs:
            self.assertTrue(Path(ref["path"]).is_relative_to(target), ref["path"])
        return refs

    def _assert_refs(self, refs: list[dict]) -> None:
        for ref in refs:
            with self.subTest(path=ref["path"]):
                self.assertEqual(sha256_file(Path(ref["path"])), ref["sha256"])

    def test_T_a_fresh_pilot_03_identity_and_path_are_coherent(self):
        from studio2.fase03 import materialize_successor_recovery as materializer

        self.assertEqual(materializer.SUCCESSOR_PILOT_ID, self.EXPECTED_ID)
        self.assertEqual(materializer.TARGET_ROOT, self.EXPECTED_ROOT)
        self.assertEqual(materializer.TARGET_ROOT.name, materializer.SUCCESSOR_PILOT_ID)
        for value in (materializer.SUCCESSOR_PILOT_ID, str(materializer.TARGET_ROOT)):
            self.assertNotIn("pilot-002", value)
            self.assertNotIn("pilot-001", value)
        self.assertEqual(materializer.PREDECESSOR_PILOT_ID, "studio2-fase03-d9-pilot-001")
        self.assertEqual(materializer.PREDECESSOR_ROOT,
                         Path("/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001"))
        self.assertEqual(
            materializer.PREDECESSOR_SHA256,
            "4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb")
        source = Path(materializer.__file__).read_text(encoding="utf-8")
        self.assertNotIn("pilot-002", source)

    def test_T_b_published_target_has_no_wal_or_shm_sidecars(self):
        materializer, target = self._fixture_sources()
        # Persistent-WAL SQLite builds (e.g. Apple's) keep empty sidecars after close;
        # simulate them so the assertion does not depend on the local SQLite build.
        real_connect = sqlite3.connect

        def persistent_wal_connect(*args, **kwargs):
            connection = real_connect(*args, **kwargs)
            database = str(args[0] if args else kwargs["database"])
            if kwargs.get("uri") or database.startswith("file:"):
                return connection
            return _PersistentWalConnection(connection, Path(database))

        with mock.patch.object(materializer.sqlite3, "connect", persistent_wal_connect):
            result = materializer._publish_staged(materializer._materialize_tree)
        self.assertEqual(result["root"], str(target))
        self.assertTrue((target / "ledger.sqlite3").is_file())
        self.assertEqual(sorted(p.name for p in target.glob("ledger.sqlite3*")),
                         ["ledger.sqlite3"])
        self.assertEqual([p for p in target.rglob("*") if p.name.endswith(("-wal", "-shm"))], [])
        self.assertEqual(sha256_file(self.predecessor.path), self.predecessor_sha)

    def test_T_c_durable_hashes_hold_after_reopening_published_ledger(self):
        materializer, target = self._fixture_sources()
        result = materializer._publish_staged(materializer._materialize_tree)
        refs = self._durable_refs(target)
        self._assert_refs(refs)
        before = {p.name for p in target.iterdir()}

        published = target / "ledger.sqlite3"
        reopened = PilotLedger(published, pilot_id=materializer.SUCCESSOR_PILOT_ID)
        self.assertEqual(reopened.identity_path, published.resolve())
        package = Path(refs[2]["path"])
        approval = Path(refs[3]["path"])
        with reopened._transaction() as connection:
            rows = reopened._validated_predecessor_lineage(
                connection, package_path=package, approval_path=approval)
            self.assertEqual((len(rows), len(reopened._rows(connection)),
                              len(reopened._historical_rows(connection))), (5, 0, 0))
        with self.assertRaisesRegex(HarnessError, "already reconciled"):
            reopened.reconcile_successor_lineage(package_path=package, approval_path=approval)
        del reopened

        self.assertEqual(sha256_file(published), result["ledger_sha256"])
        self._assert_refs(refs)
        self.assertEqual({p.name for p in target.iterdir()}, before)
        self.assertEqual(sha256_file(self.predecessor.path), self.predecessor_sha)

    def test_T_d_directory_fsync_failure_after_rename_is_published_and_intact(self):
        import errno
        import stat

        materializer, target = self._fixture_sources()
        error_type = getattr(materializer, "PublishedDirectoryFsyncError", None)
        self.assertTrue(isinstance(error_type, type) and issubclass(error_type, RuntimeError),
                        "materializer lacks a dedicated published-but-not-durable diagnosis")
        real_fsync = os.fsync

        def failing_directory_fsync(descriptor):
            if stat.S_ISDIR(os.fstat(descriptor).st_mode):
                raise OSError(errno.EIO, "injected directory fsync failure")
            return real_fsync(descriptor)

        with mock.patch.object(materializer.os, "fsync", failing_directory_fsync):
            with self.assertRaises(error_type) as caught:
                materializer._publish_staged(materializer._materialize_tree)
        error = caught.exception
        self.assertIs(error.published, True)
        self.assertEqual(Path(error.target), target)
        self.assertEqual(error.result["root"], str(target))
        self.assertIsInstance(error.__cause__, OSError)
        self.assertEqual(error.__cause__.errno, errno.EIO)
        self.assertTrue(target.is_dir())
        self._assert_refs(self._durable_refs(target))
        self.assertEqual(sha256_file(target / "ledger.sqlite3"), error.result["ledger_sha256"])
        self.assertEqual(list(target.parent.glob(f".{target.name}.staging-*")), [])
        with self.assertRaisesRegex(RuntimeError, "already exists"):
            materializer._publish_staged(lambda staging: self.fail("builder must not run"))
        self._assert_refs(self._durable_refs(target))


FIXED_COMMIT = "82a41797c5b07dbd81a0e568dc399b45c98ff92f"


class AccountingStopReconciliationTests(SuccessorFixture):
    """03.13-REM-6: explicit, durable reconciliation of one spurious accounting STOP."""

    Tokenizer = BlockingCorrectionTests.Tokenizer
    _one_accounted_producer_request = BlockingCorrectionTests._one_accounted_producer_request

    def _spurious_stop(self):
        ledger, guard, logical_id = self._one_accounted_producer_request()
        with self.assertRaisesRegex(HarnessError, "persisted accounting messages are invalid"):
            ledger.validate_tokenizer_accounting_evidence(
                guard, expected_stage="producer_conformity",
                expected_messages={logical_id: [{"role": "user", "content": "changed-0"}]})
        self.assertIsNotNone(ledger.event("stop:tokenizer_accounting"))
        return ledger, guard

    def _approval(self, ledger, name="approval", **changes):
        stop = ledger.event("stop:tokenizer_accounting")
        value = {
            "decision": "accepted",
            "author": "FIXTURE AUTHOR",
            "stop_artifact_sha256": stop["artifact_sha256"],
            "stop_request_id": stop["request_id"],
            "cause": "harness_defect",
            "fixed_commit": FIXED_COMMIT,
            "ledger_sha256_before": sha256_file(ledger.path),
        }
        value.update(changes)
        path = self.home / f"{name}.json"
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
        return path

    def _reconcile(self, ledger, guard, approval):
        return ledger.reconcile_accounting_stop(
            approval_path=approval, fixed_commit=FIXED_COMMIT, guard=guard)

    def _state(self, ledger):
        with closing(sqlite3.connect(ledger.path)) as connection:
            return {
                "requests": list(connection.execute("SELECT * FROM requests ORDER BY rowid")),
                "responses": list(connection.execute("SELECT * FROM responses ORDER BY rowid")),
                "receipts": list(connection.execute("SELECT * FROM receipts ORDER BY rowid")),
                "stages": list(connection.execute("SELECT * FROM stages ORDER BY rowid")),
                "events": list(connection.execute(
                    "SELECT * FROM events WHERE event != 'stop_reconciled:tokenizer_accounting' "
                    "ORDER BY rowid")),
            }

    def test_REM6_a_spurious_stop_is_reconciled_and_new_requests_are_admitted(self):
        ledger, guard = self._spurious_stop()
        with self.assertRaisesRegex(HarnessError, "durable STOP blocks"):
            _reserve(ledger, "producer_conformity", 1)
        stop = ledger.event("stop:tokenizer_accounting")
        approval = self._approval(ledger)
        result = self._reconcile(ledger, guard, approval)
        self.assertEqual(result["status"], "RECONCILED")
        event = ledger.event("stop_reconciled:tokenizer_accounting")
        self.assertEqual(event["artifact_sha256"], stop["artifact_sha256"])
        self.assertEqual(event["approval"]["sha256"], sha256_file(approval))
        self.assertEqual(event["approval"]["content"]["cause"], "harness_defect")
        self.assertEqual(event["fixed_commit"], FIXED_COMMIT)
        self.assertEqual(ledger.event("stop:tokenizer_accounting"), stop)
        approval.unlink()
        ledger.validate_tokenizer_accounting_evidence(guard)
        self.assertEqual(_reserve(ledger, "producer_conformity", 1), "producer_conformity-1")

    def test_REM6_b_really_corrupted_accounting_refuses_reconciliation(self):
        ledger, guard = self._spurious_stop()
        approval = self._approval(ledger)
        with closing(sqlite3.connect(ledger.path)) as connection:
            name = "tokenizer_accounting:" + ledger.event("stop:tokenizer_accounting")["request_id"]
            detail = json.loads(connection.execute(
                "SELECT detail_json FROM events WHERE event=?", (name,)).fetchone()[0])
            detail["messages"] = [{"role": "user", "content": "tampered-0"}]
            connection.execute("UPDATE events SET detail_json=? WHERE event=?",
                               (canonical_json(detail), name))
            connection.commit()
        approval = self._approval(ledger, "approval-after-tamper")
        with self.assertRaisesRegex(HarnessError, "reconciliation refused"):
            self._reconcile(ledger, guard, approval)
        self.assertIsNone(ledger.event("stop_reconciled:tokenizer_accounting"))
        with self.assertRaisesRegex(HarnessError, "durable STOP blocks"):
            _reserve(ledger, "producer_conformity", 1)

    def _insert_request_copy(self, ledger, *, status, intent_utc):
        with closing(sqlite3.connect(ledger.path)) as connection:
            row = list(connection.execute("SELECT * FROM requests ORDER BY rowid LIMIT 1").fetchone())
            columns = [item[1] for item in connection.execute("PRAGMA table_info(requests)")]
            value = dict(zip(columns, row))
            value.update(request_id="after-stop", logical_id="after-stop-logical",
                         stage="producer_conformity", retry_of=None, status=status,
                         intent_utc=intent_utc)
            connection.execute(
                f"INSERT INTO requests VALUES ({','.join('?' for _ in columns)})",
                [value[column] for column in columns])
            connection.commit()

    def test_REM6_c_request_created_after_stop_refuses_reconciliation(self):
        ledger, guard = self._spurious_stop()
        with closing(sqlite3.connect(ledger.path)) as connection:
            stop_row = connection.execute(
                "SELECT created_utc FROM events WHERE event='stop:tokenizer_accounting'").fetchone()[0]
        self.assertLess(stop_row, "2999")
        later = "2999-01-01T00:00:00+00:00"
        self._insert_request_copy(ledger, status="COMPLETED", intent_utc=later)
        approval = self._approval(ledger)
        with self.assertRaisesRegex(HarnessError, "request created after the STOP"):
            self._reconcile(ledger, guard, approval)
        self.assertIsNone(ledger.event("stop_reconciled:tokenizer_accounting"))

    def test_REM6_c_unresolved_intent_refuses_reconciliation(self):
        ledger, guard = self._spurious_stop()
        self._insert_request_copy(ledger, status="INTENT", intent_utc="2000-01-01T00:00:00+00:00")
        approval = self._approval(ledger)
        with self.assertRaisesRegex(HarnessError, "unresolved INTENT"):
            self._reconcile(ledger, guard, approval)
        self.assertIsNone(ledger.event("stop_reconciled:tokenizer_accounting"))

    def test_REM6_d_approval_bound_to_another_stop_or_state_is_refused(self):
        ledger, guard = self._spurious_stop()
        cases = {
            "stop-hash": dict(stop_artifact_sha256="0" * 64),
            "stop-request": dict(stop_request_id="other-request"),
            "cause": dict(cause="provider_defect"),
            "decision": dict(decision="rejected"),
            "author": dict(author=""),
            "fixed-commit": dict(fixed_commit="0" * 40),
            "ledger-before": dict(ledger_sha256_before="1" * 64),
            "extra-key": dict(note="unexpected"),
        }
        for name, changes in cases.items():
            with self.subTest(name=name):
                approval = self._approval(ledger, name, **changes)
                with self.assertRaises(HarnessError):
                    self._reconcile(ledger, guard, approval)
                self.assertIsNone(ledger.event("stop_reconciled:tokenizer_accounting"))
        approval = self._approval(ledger, "wrong-fixed-argument")
        with self.assertRaises(HarnessError):
            ledger.reconcile_accounting_stop(
                approval_path=approval, fixed_commit="1" * 40, guard=guard)
        self.assertIsNone(ledger.event("stop_reconciled:tokenizer_accounting"))

    def test_REM6_d_absent_stop_is_not_reconcilable(self):
        ledger, guard, _ = self._one_accounted_producer_request()
        approval = self.home / "no-stop.json"
        approval.write_text(json.dumps({
            "decision": "accepted", "author": "FIXTURE AUTHOR",
            "stop_artifact_sha256": "0" * 64, "stop_request_id": "x",
            "cause": "harness_defect", "fixed_commit": FIXED_COMMIT,
            "ledger_sha256_before": sha256_file(ledger.path)}), encoding="utf-8")
        with self.assertRaisesRegex(HarnessError, "no tokenizer accounting STOP"):
            self._reconcile(ledger, guard, approval)

    def test_REM6_e_new_stop_after_reconciliation_blocks_again(self):
        ledger, guard = self._spurious_stop()
        self._reconcile(ledger, guard, self._approval(ledger))
        request_id = ledger.event("stop:tokenizer_accounting")["request_id"]
        logical_id = ledger.request(request_id)["logical_id"]
        with self.assertRaisesRegex(HarnessError, "persisted accounting messages are invalid"):
            ledger.validate_tokenizer_accounting_evidence(
                guard, expected_stage="producer_conformity",
                expected_messages={logical_id: [{"role": "user", "content": "changed-again"}]})
        self.assertIn("stop:tokenizer_accounting#2", ledger.snapshot()["events"])
        with self.assertRaisesRegex(HarnessError, "durable STOP blocks"):
            _reserve(ledger, "producer_conformity", 1)
        with self.assertRaisesRegex(HarnessError, "durable STOP blocks"):
            ledger.validate_tokenizer_accounting_evidence(guard)
        with self.assertRaises(HarnessError):
            self._reconcile(ledger, guard, self._approval(ledger, "second"))

    def test_REM6_e_corrupted_reconciliation_event_blocks_fail_closed(self):
        ledger, guard = self._spurious_stop()
        self._reconcile(ledger, guard, self._approval(ledger))
        with closing(sqlite3.connect(ledger.path)) as connection:
            detail = json.loads(connection.execute(
                "SELECT detail_json FROM events WHERE event='stop_reconciled:tokenizer_accounting'"
            ).fetchone()[0])
            detail["approval"]["content"]["cause"] = "operator_override"
            connection.execute(
                "UPDATE events SET detail_json=? WHERE event='stop_reconciled:tokenizer_accounting'",
                (canonical_json(detail),))
            connection.commit()
        with self.assertRaisesRegex(HarnessError, "FATAL_ACCOUNTING_ERROR"):
            _reserve(ledger, "producer_conformity", 1)

    def test_REM6_f_reconciliation_is_idempotent_and_single(self):
        ledger, guard = self._spurious_stop()
        approval = self._approval(ledger)
        self.assertEqual(self._reconcile(ledger, guard, approval)["status"], "RECONCILED")
        before = _logical(ledger.path)
        self.assertEqual(self._reconcile(ledger, guard, approval)["status"], "ALREADY_RECONCILED")
        self.assertEqual(_logical(ledger.path), before)
        with closing(sqlite3.connect(ledger.path)) as connection:
            self.assertEqual(connection.execute(
                "SELECT count(*) FROM events WHERE event LIKE 'stop_reconciled:%'").fetchone()[0], 1)
        other = self._approval(ledger, "other", author="OTHER AUTHOR")
        with self.assertRaisesRegex(HarnessError, "already reconciled"):
            self._reconcile(ledger, guard, other)
        self.assertEqual(_logical(ledger.path), before)

    def test_REM6_g_quota_and_outcomes_are_unchanged(self):
        ledger, guard = self._spurious_stop()
        state = self._state(ledger)
        snapshot = ledger.snapshot()
        self._reconcile(ledger, guard, self._approval(ledger))
        self.assertEqual(self._state(ledger), state)
        after = ledger.snapshot()
        self.assertEqual(after.pop("events"),
                         sorted(snapshot.pop("events") + ["stop_reconciled:tokenizer_accounting"]))
        self.assertEqual(after, snapshot)


class _PersistentWalConnection:
    """sqlite3 connection proxy that keeps empty WAL/SHM files after close.

    Models persistent-WAL SQLite builds: sidecars survive both an explicit close and
    an implicit close at garbage collection.
    """

    def __init__(self, connection, database: Path):
        self._connection = connection
        self._database = database
        self._closed = False

    def __getattr__(self, name):
        return getattr(self._connection, name)

    def __setattr__(self, name, value):
        if name.startswith("_"):
            object.__setattr__(self, name, value)
        else:
            setattr(self._connection, name, value)

    def __enter__(self):
        self._connection.__enter__()
        return self

    def __exit__(self, *exc):
        return self._connection.__exit__(*exc)

    def close(self):
        if self._closed:
            return
        self._closed = True
        self._connection.close()
        if self._database.parent.is_dir():
            for suffix in ("-wal", "-shm"):
                Path(str(self._database) + suffix).touch()

    def __del__(self):
        self.close()


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

    def test_REM6_reconcile_cli_requires_ack_and_existing_ledger(self):
        from studio2.fase03 import reconcile_accounting_stop as cli
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp)
            ledger_path = (home / "missing.sqlite3").resolve()
            approval = home / "approval.json"
            approval.write_text("{}", encoding="utf-8")
            base = ["--ledger", str(ledger_path), "--pilot-id", "successor-cli",
                    "--approval", str(approval), "--fixed-commit", "0" * 40,
                    "--provider-config", str(home / "missing-provider.json"),
                    "--model-snapshot", str(home / "missing-snapshot")]
            self.assertEqual(cli.main(base), 0)
            with self.assertRaises(SystemExit):
                cli.main(base + ["--execute", "--acknowledge", "WRONG"])
            with self.assertRaisesRegex(HarnessError, "existing absolute ledger"):
                cli.main(base + ["--execute", "--acknowledge", cli.ACK])
            self.assertFalse(ledger_path.exists())


if __name__ == "__main__":
    unittest.main(verbosity=2)
