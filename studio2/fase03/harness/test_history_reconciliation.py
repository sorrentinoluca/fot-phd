"""Discriminating offline contract for an explicitly authorized external-S import.

Fixtures are synthetic and authorize neither a real ledger mutation nor provider calls.
"""
from contextlib import ExitStack
from copy import deepcopy
import json
import multiprocessing
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch

if os.environ.get("FOT_HISTORY_TARGET"):
    sys.path.insert(0, os.environ["FOT_HISTORY_TARGET"])

from studio2.fase03.harness.common import HarnessError, canonical_json, sha256_bytes, sha256_file
from studio2.fase03.harness.ledger import PilotLedger, digest


def _write_json(path, value):
    path.write_text(json.dumps(value, sort_keys=True))
    return path


def _import_worker(ledger_path, pilot_id, package_path, approval_path, source, queue):
    try:
        from studio2.fase03.harness import d9
        with patch.object(d9, "HISTORY_SOURCE", source):
            PilotLedger(Path(ledger_path), pilot_id=pilot_id).reconcile_external_history(
                package_path=Path(package_path), approval_path=Path(approval_path))
        queue.put("OK")
    except Exception as exc:  # result is asserted in the parent process
        queue.put(type(exc).__name__ + ":" + str(exc))


def _reserve_worker(ledger_path, pilot_id, source, r4_tokenizer, reservation, queue):
    try:
        from studio2.fase03.harness import d9
        with patch.object(d9, "HISTORY_SOURCE", source), patch.object(d9, "R4_TOKENIZER", r4_tokenizer):
            PilotLedger(Path(ledger_path), pilot_id=pilot_id).reserve_request(**reservation)
        queue.put("OK")
    except Exception as exc:
        queue.put(type(exc).__name__ + ":" + str(exc))


class ExternalHistoryReconciliation(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.home = Path(self.tmp.name)
        self.ledger = PilotLedger(self.home / "pilot.sqlite3", pilot_id="pilot-history-fixture")
        self.package, self.approval, self.source = self._package()
        from studio2.fase03.harness import d9
        self.original_history_source = deepcopy(d9.HISTORY_SOURCE)
        self.stack = ExitStack(); self.addCleanup(self.stack.close)
        self.stack.enter_context(patch.object(d9, "HISTORY_SOURCE", deepcopy(self.source)))

    def _package(self):
        attempts = self.home / "attempts.jsonl"
        attempts.write_text(canonical_json({"outcome": "REJECTED_BEFORE_INFERENCE",
                                            "http_status": 400,
                                            "inference_completed": False}) + "\n")
        records = self.home / "records.jsonl"
        synthetic_records = []
        for i in range(2, 5):
            raw = f"fixture-output-{i}"
            usage = {"prompt_tokens": i, "completion_tokens": 1, "total_tokens": i + 1}
            synthetic_records.append({"response_id": f"fixture-{i}",
                "returned_model": "fixture-model", "system_fingerprint": "fixture-fingerprint",
                "finish_reason": "stop", "raw_output": raw,
                "raw_output_sha256": sha256_bytes(raw.encode()), **usage,
                "response_raw": {"id": f"fixture-{i}", "model": "fixture-model",
                    "system_fingerprint": "fixture-fingerprint", "usage": usage,
                    "choices": [{"finish_reason": "stop", "message": {"content": raw}}]}})
        records.write_text("".join(canonical_json(row) + "\n" for row in synthetic_records))
        summary = _write_json(self.home / "summary.json", {
            "provider_requests_total": 4, "completed_model_inferences": 3,
            "attempt_journal_sha256": sha256_file(attempts),
            "records_sha256": sha256_file(records)})
        source = {"sha256": sha256_file(summary), "reported_requests": 4,
                  "completed_inferences": 3}
        refs = {key: {"path": str(path), "sha256": sha256_file(path)}
                for key, path in (("summary", summary), ("attempts", attempts),
                                  ("records", records))}
        parsed = {
            "attempts": [json.loads(attempts.read_text().splitlines()[0])],
            "records": [json.loads(line) for line in records.read_text().splitlines()],
        }
        mappings = []
        for ordinal in range(1, 5):
            source_key, line = ("attempts", 1) if ordinal == 1 else ("records", ordinal - 1)
            binding = {"source_key": source_key, "line": line,
                       "record_sha256": digest(parsed[source_key][line - 1])}
            request_id = f"external-s{ordinal}-fixture"
            identity = {"assignment": "ASSIGNED_DURING_RECONCILIATION",
                        "historical_ordinal": ordinal, "request_id": request_id,
                        "source_binding_sha256": digest(binding)}
            mappings.append({"historical_ordinal": ordinal, "request_id": request_id,
                             "identity": identity, "identity_sha256": digest(identity),
                             "source_binding": binding,
                             "disposition": "HISTORICAL_OUTCOME_UNCERTAIN" if ordinal == 1 else "COMPLETED"})
        review = self.home / "review.md"
        review.write_text("OK LIMITATO DOCUMENTALE — FIXTURE ONLY\n")
        package = _write_json(self.home / "package.json", {
            "artifact_version": "1", "status": "MAPPING_REVIEWED",
            "source": source,
            "pilot_ledger": {"path": str(self.ledger.path), "pilot_id": self.ledger.pilot_id},
            "source_files": refs, "request_imports": mappings,
            "review": {"reviewer": "FIXTURE REVIEWER",
                       "path": str(review), "sha256": sha256_file(review)}})
        approval = _write_json(self.home / "approval.json", {
            "artifact_version": "1", "author": "FIXTURE AUTHOR",
            "decision": "IMPORT_AUTHORIZED", "package_sha256": sha256_file(package),
            "pilot_ledger": {"path": str(self.ledger.path), "pilot_id": self.ledger.pilot_id},
            "source": source})
        return package, approval, source

    def _import(self):
        return self.ledger.reconcile_external_history(
            package_path=self.package, approval_path=self.approval)

    def _logical_state(self):
        with sqlite3.connect(self.ledger.path) as connection:
            tables = [r[0] for r in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
            rows = connection.execute("SELECT * FROM external_history ORDER BY historical_ordinal").fetchall() if "external_history" in tables else []
            version = connection.execute("PRAGMA user_version").fetchone()[0]
        return version, tables, rows, self.ledger.snapshot()

    def test_positive_is_separate_charged_once_reopen_and_idempotent(self):
        self.assertEqual(self._import()["status"], "RECONCILED")
        first = self._logical_state()
        self.assertEqual(first[0], 3)
        self.assertEqual(first[3]["historical_requests"], 4)
        self.assertEqual(first[3]["requests_cumulative"], 4)
        self.assertEqual(first[3]["native_requests"], 0)
        self.assertEqual(len(first[2]), 4)
        self.assertEqual(self._import()["status"], "ALREADY_RECONCILED")
        reopened = PilotLedger(self.ledger.path, pilot_id=self.ledger.pilot_id)
        reopened.reconcile_external_history(package_path=self.package, approval_path=self.approval)
        self.assertEqual(self._logical_state(), first)

    def test_incomplete_duplicate_swapped_and_false_zero_refuse_atomically(self):
        mutations = []
        mutations.append(lambda p: p["request_imports"].pop())
        mutations.append(lambda p: p["request_imports"].__setitem__(1, deepcopy(p["request_imports"][0])))
        def swapped(p):
            p["request_imports"][1]["source_binding"], p["request_imports"][2]["source_binding"] = p["request_imports"][2]["source_binding"], p["request_imports"][1]["source_binding"]
        mutations.append(swapped)
        mutations.append(lambda p: p["request_imports"][0].update(disposition="ZERO_TOKEN_PROVEN"))
        baseline = self._logical_state()
        for index, mutate in enumerate(mutations):
            value = json.loads(self.package.read_text()); mutate(value)
            bad = _write_json(self.home / f"bad-{index}.json", value)
            approval = json.loads(self.approval.read_text()); approval["package_sha256"] = sha256_file(bad)
            auth = _write_json(self.home / f"bad-approval-{index}.json", approval)
            with self.subTest(index=index), self.assertRaises(HarnessError):
                self.ledger.reconcile_external_history(package_path=bad, approval_path=auth)
            self.assertEqual(self._logical_state(), baseline)

    def test_source_change_even_with_rewritten_reference_refuses(self):
        value = json.loads(self.package.read_text())
        source = Path(value["source_files"]["records"]["path"])
        source.write_text(source.read_text().replace("fixture-output-2", "altered-output-2"))
        value["source_files"]["records"]["sha256"] = sha256_file(source)
        bad = _write_json(self.home / "realigned.json", value)
        approval = json.loads(self.approval.read_text()); approval["package_sha256"] = sha256_file(bad)
        auth = _write_json(self.home / "realigned-approval.json", approval)
        with self.assertRaises(HarnessError):
            self.ledger.reconcile_external_history(package_path=bad, approval_path=auth)
        self.assertEqual(self.ledger.snapshot()["requests_cumulative"], 0)

    def test_repository_source_bytes_fit_contract_on_fixture_ledger(self):
        from studio2.fase03.harness import d9
        root = Path(__file__).resolve().parents[3]
        source_dir = root / "studio2/fase03/results/provisional_cap_stress"
        paths = {"summary": source_dir / "provisional_stress_probe_summary.json",
                 "attempts": source_dir / "provisional_stress_probe_attempts.jsonl",
                 "records": source_dir / "provisional_stress_probe_records.jsonl"}
        rows = {key: [json.loads(line) for line in path.read_text().splitlines()]
                for key, path in paths.items() if key != "summary"}
        ledger = PilotLedger(self.home / "repository-source.sqlite3",
                             pilot_id="repository-source-fixture")
        mappings = []
        for ordinal in range(1, 5):
            source_key, line = ("attempts", 1) if ordinal == 1 else ("records", ordinal - 1)
            binding = {"source_key": source_key, "line": line,
                       "record_sha256": digest(rows[source_key][line - 1])}
            request_id = f"repository-source-s{ordinal}"
            identity = {"assignment": "ASSIGNED_DURING_RECONCILIATION",
                        "historical_ordinal": ordinal, "request_id": request_id,
                        "source_binding_sha256": digest(binding)}
            mappings.append({"historical_ordinal": ordinal, "request_id": request_id,
                "identity": identity, "identity_sha256": digest(identity),
                "source_binding": binding,
                "disposition": "HISTORICAL_OUTCOME_UNCERTAIN" if ordinal == 1 else "COMPLETED"})
        review = self.home / "repository-source-review.md"
        review.write_text("OK LIMITATO DOCUMENTALE — FIXTURE LEDGER ONLY\n")
        package = _write_json(self.home / "repository-source-package.json", {
            "artifact_version": "1", "status": "MAPPING_REVIEWED",
            "source": self.original_history_source,
            "pilot_ledger": {"path": str(ledger.path), "pilot_id": ledger.pilot_id},
            "source_files": {key: {"path": str(path), "sha256": sha256_file(path)}
                             for key, path in paths.items()},
            "request_imports": mappings,
            "review": {"reviewer": "FIXTURE REVIEWER", "path": str(review),
                       "sha256": sha256_file(review)}})
        approval = _write_json(self.home / "repository-source-approval.json", {
            "artifact_version": "1", "author": "FIXTURE AUTHOR",
            "decision": "IMPORT_AUTHORIZED", "package_sha256": sha256_file(package),
            "pilot_ledger": {"path": str(ledger.path), "pilot_id": ledger.pilot_id},
            "source": self.original_history_source})
        with patch.object(d9, "HISTORY_SOURCE", deepcopy(self.original_history_source)):
            ledger.reconcile_external_history(package_path=package, approval_path=approval)
        self.assertEqual(ledger.snapshot()["historical_requests"], 4)

    def test_wrong_ledger_types_missing_review_or_approval_refuse(self):
        variants = []
        variants.append((lambda p: p["pilot_ledger"].update(pilot_id="other-pilot"), None))
        variants.append((lambda p: p["request_imports"][0].update(historical_ordinal=True), None))
        variants.append((lambda p: p["review"].update(sha256="0" * 64), None))
        variants.append((None, lambda a: a.update(decision="PENDING")))
        for index, (mutate_package, mutate_approval) in enumerate(variants):
            value = json.loads(self.package.read_text())
            if mutate_package: mutate_package(value)
            package = _write_json(self.home / f"variant-{index}.json", value)
            approval = json.loads(self.approval.read_text())
            approval["package_sha256"] = sha256_file(package)
            if mutate_approval: mutate_approval(approval)
            auth = _write_json(self.home / f"variant-auth-{index}.json", approval)
            with self.subTest(index=index), self.assertRaises(HarnessError):
                self.ledger.reconcile_external_history(package_path=package, approval_path=auth)
        self.assertEqual(self.ledger.snapshot()["requests_cumulative"], 0)

    def test_failure_after_intermediate_insert_rolls_back_and_resume_succeeds(self):
        original = self.ledger._insert_external_history
        calls = []
        def fail_second(connection, row, package_sha256):
            calls.append(row["historical_ordinal"])
            original(connection, row, package_sha256)
            if len(calls) == 2:
                raise OSError("fixture crash after second insert")
        with patch.object(self.ledger, "_insert_external_history", side_effect=fail_second):
            with self.assertRaises(OSError): self._import()
        self.assertEqual(self._logical_state()[0], 2)
        self.assertEqual(self.ledger.snapshot()["requests_cumulative"], 0)
        self._import()
        self.assertEqual(self.ledger.snapshot()["requests_cumulative"], 4)

    def test_two_processes_reconcile_one_event_and_four_rows(self):
        queue = multiprocessing.Queue()
        processes = [multiprocessing.Process(target=_import_worker,
                    args=(str(self.ledger.path), self.ledger.pilot_id,
                          str(self.package), str(self.approval), self.source, queue)) for _ in range(2)]
        for process in processes: process.start()
        for process in processes: process.join(20)
        self.assertEqual([process.exitcode for process in processes], [0, 0])
        self.assertEqual(sorted(queue.get(timeout=2) for _ in processes),
                         ["OK", "OK"])
        state = self._logical_state()
        self.assertEqual(len(state[2]), 4)
        self.assertEqual(sum(name.startswith("history_reconciliation:")
                             for name in state[3]["events"]), 1)

    def test_direct_reservation_without_rebind_refuses_after_history(self):
        self._import()
        before = self.ledger.snapshot()
        with self.assertRaises(HarnessError):
            self.ledger.reserve_request(request_id="unbound", logical_id="case-0",
                model="fixture-model", producer="fixture-producer",
                stage="producer_conformity", stage_run="a" * 64)
        self.assertEqual(self.ledger.snapshot(), before)

    def test_two_processes_compete_for_first_native_slot_once(self):
        self._import()
        from studio2.fase03.harness.test_revisions import RunnerRevisions
        from studio2.fase03.harness.offline_fixtures import Trial
        from studio2.fase03.harness import d9
        owner = RunnerRevisions(); owner.setUp(); self.addCleanup(owner.doCleanups)
        owner.stack.enter_context(patch.object(d9, "HISTORY_SOURCE", deepcopy(self.source)))
        owner.ledger = self.ledger
        owner.config["pilot_ledger"] = {"path": str(self.ledger.path),
                                          "pilot_id": self.ledger.pilot_id}
        owner.config["d9"]["history_reconciliation"] = {
            "path": str(self.package), "sha256": sha256_file(self.package)}
        owner.config["d9"]["history_approval"] = {
            "path": str(self.approval), "sha256": sha256_file(self.approval)}
        owner.approve_config()
        helper = Trial(self.home / "binding-helper")
        binding = helper.binding("producer_conformity")
        for request in binding["requests"]:
            request["producer"] = owner.provider_value["name"]
        binding.update(provider=owner.provider_value,
            execution_config=owner.config, tokenizer_snapshot=str(owner.snapshot),
            provider_file_sha256=sha256_file(owner.provider),
            provider_reference={"path": str(owner.provider), "sha256": sha256_file(owner.provider)})
        self.ledger.bind_stage("producer_conformity", binding)
        spec = binding["requests"][0]
        common = dict(logical_id=spec["logical_id"], model=spec["model"],
                      producer=spec["producer"], stage="producer_conformity",
                      stage_run=digest(binding))
        # Release the fixture's global socket/module patches before spawning.
        # The child applies only the D9 source pin and never constructs transport.
        owner.stack.close()
        queue = multiprocessing.Queue()
        processes = [multiprocessing.Process(target=_reserve_worker,
            args=(str(self.ledger.path), self.ledger.pilot_id, self.source,
                  owner.tokenizer, dict(common, request_id=f"race-{i}"), queue)) for i in range(2)]
        for process in processes: process.start()
        for process in processes: process.join(20)
        results = [queue.get(timeout=2) for _ in processes]
        self.assertEqual(sum(result == "OK" for result in results), 1, results)
        self.assertEqual(self.ledger.snapshot()["requests_cumulative"], 5)
        self.assertEqual(self.ledger.snapshot()["native_requests"], 1)

    def test_reconfirmed_before_direct_reservation_and_no_side_effect(self):
        self._import()
        from studio2.fase03.harness.test_revisions import RunnerRevisions
        from studio2.fase03.harness import d9
        owner = RunnerRevisions(); owner.setUp(); self.addCleanup(owner.doCleanups)
        # This test uses the already imported ledger and fixture-only D9 metadata.
        owner.ledger = self.ledger; owner.config["pilot_ledger"] = {
            "path": str(self.ledger.path), "pilot_id": self.ledger.pilot_id}
        owner.config["d9"]["history_reconciliation"] = {
            "path": str(self.package), "sha256": sha256_file(self.package)}
        owner.config["d9"]["history_approval"] = {
            "path": str(self.approval), "sha256": sha256_file(self.approval)}
        owner.stack.enter_context(patch.object(d9, "HISTORY_SOURCE", deepcopy(self.source)))
        owner.approve_config(); owner.producer()
        before = self.ledger.snapshot()
        calls_before = list(owner.calls)
        binding = self.ledger.binding("producer_conformity")
        spec = binding["requests"][0]
        source = Path(json.loads(self.package.read_text())["source_files"]["records"]["path"])
        source.write_text(source.read_text() + "{}\n")
        with self.assertRaises(HarnessError):
            self.ledger.reserve_request(request_id="must-not-exist", logical_id=spec["logical_id"],
                model=spec["model"], producer=spec["producer"], stage="producer_conformity",
                stage_run=digest(binding))
        after = self.ledger.snapshot()
        self.assertEqual(after["requests_cumulative"], before["requests_cumulative"])
        self.assertEqual(after["events"], before["events"])
        self.assertEqual(owner.calls, calls_before)


if __name__ == "__main__":
    unittest.main()
