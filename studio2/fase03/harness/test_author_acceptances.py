"""03.13-ACC offline probes on the sacrificial RunnerRevisions fixture. No provider calls."""
from contextlib import closing
import json
from pathlib import Path
import sqlite3
import unittest

from studio2.fase03 import author_acceptances as acc, run_pilot as rp
from studio2.fase03.harness.common import HarnessError, sha256_file
from studio2.fase03.harness.test_revisions import REFERENCE, ROOT, SCHEMA


def _dump(path):
    with closing(sqlite3.connect(path)) as connection:
        return "\n".join(connection.iterdump())


@unittest.skipUnless((REFERENCE / "EVIDENCE_MANIFEST.csv").is_file(),
                     "03.6 evidence release required (FOT_HARNESS_TEST_EVIDENCE)")
class AuthorAcceptanceTests(unittest.TestCase):
    def setUp(self):
        from studio2.fase03.harness.test_revisions import RunnerRevisions
        self.t = RunnerRevisions(); self.t.setUp(); self.addCleanup(self.t.doCleanups)
        self.assertEqual(self.t.producer()["status"], "PASS")
        self.runtime = self.t.home / "runtime"
        self.handoff = self.t.home / "results/validated_insight_library_fixture_producer_conformity.json"

    def run_script(self, execute=True):
        return acc.run(runtime=self.runtime, worktree=ROOT, author="FIXTURE AUTHOR",
                       evidence_root=REFERENCE, execute=execute, config_path=self.t.config_path,
                       handoff=self.handoff, snapshot=self.t.snapshot, schema_dir=SCHEMA)

    def gate(self):
        prepared, results = self.runtime / acc.PREPARED_NAME, self.t.home / "consumer_results"
        frozen = rp.run_budget_stage(prepared, results, ledger=self.t.ledger)
        return frozen, rp.run_stability_stage(prepared, results, ledger=self.t.ledger)

    def test_ACC00_without_script_pending_inventory_reproduces_the_refusal(self):
        from studio2.fase03 import prepare_gate as pg
        from studio2.fase03.harness import inputs
        manifest = self.t.home / "manifest.json"
        _, value = inputs.build_inventory(**self.t.inventory_args(), insight_handoff=self.handoff,
                                          ledger=self.t.ledger, token_count=lambda s: len(s.split()),
                                          schema_dir=SCHEMA,
                                          presentation_approval=self.t.config["presentation_approval"])
        manifest.write_text(json.dumps(value))
        with self.assertRaisesRegex(HarnessError, "presentation order has not been accepted by the author"):
            pg.prepare(manifest, self.t.snapshot, self.t.home / "prepared", source_inventory_path=self.t.source,
                       insight_handoff=self.handoff, ledger=self.t.ledger)

    def test_ACC01_all_gates_pass_after_script(self):
        before_config = self.t.config_path.read_bytes()
        result = self.run_script()
        self.assertEqual(result["status"], acc.READY, result["blocking"])
        self.assertEqual(result["prompt_count"], 40)
        self.assertEqual(self.t.config_path.read_bytes(), before_config)
        inventory = json.loads((self.runtime / acc.FROZEN_INVENTORY_NAME).read_text())
        self.assertEqual(inventory["presentation"]["author_decision"], "accepted")
        frozen, summary = self.gate()
        self.assertEqual(frozen["status"], "FROZEN_FOR_STABILITY_GATE")
        self.assertEqual(len(self.t.consumer_calls), 3 + 120)
        self.assertIn("t3_pass", summary)
        record = json.loads((self.runtime / acc.RECORD_NAME).read_text())
        self.assertEqual((record["decision"], record["author"]), ("accepted", "FIXTURE AUTHOR"))

    def test_ACC02_plan_only_writes_nothing(self):
        result = self.run_script(execute=False)
        self.assertEqual(result["status"], "PLAN_ONLY")
        self.assertEqual(result["blocking"], [])
        self.assertFalse(self.runtime.exists())
        ids = [row["id"] for row in result["census"]]
        for key in ("C03_presentation_approval", "C04_execution_authorization", "L02_not_suspended",
                    "L06_alternate_pass", "L07_binding_config_equality", "H01_insight_handoff"):
            self.assertIn(key, ids)

    def test_ACC03_idempotent_and_ledger_unchanged(self):
        ledger_before = _dump(self.t.ledger.path)
        self.run_script()
        files = {p: p.read_bytes() for p in self.runtime.rglob("*") if p.is_file()}
        second = self.run_script()
        self.assertEqual(second["status"], acc.READY)
        self.assertTrue(all(c["action"] in {"UNCHANGED", "REUSED"} for c in second["changes"]), second["changes"])
        self.assertEqual({p: p.read_bytes() for p in self.runtime.rglob("*") if p.is_file()}, files)
        self.assertEqual(_dump(self.t.ledger.path), ledger_before)

    def test_ACC04_tampered_acceptance_files_fail_their_gate(self):
        self.run_script()
        prepared, results = self.runtime / acc.PREPARED_NAME, self.t.home / "consumer_results"
        targets = {
            "presentation_approval": (Path(self.t.config["presentation_approval"]["path"]), "C03_presentation_approval"),
            "execution_authorization": (Path(self.t.config["execution_authorization"]["path"]), "C04_execution_authorization"),
        }
        for name, (path, census_id) in targets.items():
            with self.subTest(name=name):
                original = path.read_bytes()
                value = json.loads(original); value["author"] = ""
                path.write_text(json.dumps(value))
                with self.assertRaises((HarnessError, RuntimeError)):
                    rp.run_budget_stage(prepared, results, ledger=self.t.ledger)
                self.assertEqual(self.run_script()["status"], "REFUSED_BLOCKING_CONDITIONS")
                self.assertIn(census_id, self.run_script(execute=False)["blocking"])
                path.write_bytes(original)
        generated = {
            "frozen_inventory": (self.runtime / acc.FROZEN_INVENTORY_NAME,
                                 lambda v: v["presentation"].__setitem__("author_decision", "pending")),
            "frozen_manifest": (self.runtime / acc.FROZEN_MANIFEST_NAME,
                                lambda v: v.__setitem__("transfer_case_by_agent", {})),
            "prepared_plan": (prepared / "pre_gate_plan.json", lambda v: v.__setitem__("status", "NO_GO_STATIC_CONTEXT")),
        }
        for name, (path, mutate) in generated.items():
            with self.subTest(name=name):
                original = path.read_bytes()
                value = json.loads(original); mutate(value)
                path.write_text(json.dumps(value, indent=2) + "\n")
                with self.assertRaises((HarnessError, RuntimeError)):
                    rp.run_budget_stage(prepared, results, ledger=self.t.ledger)
                path.write_bytes(original)
        self.assertEqual(self.t.consumer_calls, [])

    def test_ACC05_suspended_pilot_is_refused_before_any_write(self):
        with closing(sqlite3.connect(self.t.ledger.path)) as connection:
            connection.execute("INSERT INTO events VALUES (?,?,?,?)",
                               ("suspended:fixture", "2026-09-17T00:00:00+00:00", "0" * 64,
                                json.dumps({"reason": "response identity missing or changed"})))
            connection.commit()
        before = _dump(self.t.ledger.path)
        result = self.run_script()
        self.assertEqual(result["status"], "REFUSED_BLOCKING_CONDITIONS")
        self.assertIn("L02_not_suspended", result["blocking"])
        self.assertFalse(self.runtime.exists())
        self.assertEqual(_dump(self.t.ledger.path), before)

    def test_ACC06_alternate_in_pilot_without_pass_is_blocking(self):
        self.t.config["d9"]["alternate_placement"] = "pilot"; self.t.approve_config()
        result = self.run_script()
        self.assertEqual(result["status"], "REFUSED_BLOCKING_CONDITIONS")
        self.assertIn("L06_alternate_pass", result["blocking"])
        self.assertFalse(self.runtime.exists())

    def test_ACC07_rewritten_configuration_is_blocking(self):
        self.t.config["pilot_go"] = True; self.t.approve_config()
        result = self.run_script(execute=False)
        self.assertIn("L07_binding_config_equality", result["blocking"])

    def test_ACC08_cli_requires_acknowledgement(self):
        argv = ["--runtime", str(self.runtime), "--worktree", str(ROOT), "--author", "X",
                "--evidence-root", str(REFERENCE), "--config", str(self.t.config_path), "--execute"]
        with self.assertRaises(SystemExit):
            acc.main(argv + ["--acknowledge", "WRONG"])
        self.assertFalse(self.runtime.exists())
        with self.assertRaises(HarnessError):
            acc.run(runtime=self.runtime, worktree=self.t.home, author="X", evidence_root=REFERENCE,
                    execute=False, config_path=self.t.config_path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
