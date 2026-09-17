"""03.13-REV27B offline probes. The fixture reproduces pilot-03: alternate in pilot, agent_1
answered with a changed system fingerprint and suspended the pilot. No provider calls."""
from contextlib import closing
from copy import deepcopy
import json
from pathlib import Path
import sqlite3
import sys
import types
import unittest
from unittest.mock import patch

from studio2.fase03 import author_acceptances as acc, producer_probe as pp, run_pilot as rp
from studio2.fase03.harness.common import HarnessError, sha256_file
from studio2.fase03.harness.ledger import digest
from studio2.fase03.harness.test_revisions import REFERENCE, ROOT, SCHEMA

FINGERPRINT = "vllm-fixture-5fc21ed4"


def _dump(path):
    with closing(sqlite3.connect(path)) as connection:
        return "\n".join(connection.iterdump())


@unittest.skipUnless((REFERENCE / "EVIDENCE_MANIFEST.csv").is_file(),
                     "03.6 evidence release required (FOT_HARNESS_TEST_EVIDENCE)")
class ConfigRevisionTests(unittest.TestCase):
    def setUp(self):
        from studio2.fase03.harness.test_revisions import RunnerRevisions
        t = self.t = RunnerRevisions(); t.setUp(); self.addCleanup(t.doCleanups)
        t.config["d9"]["alternate_placement"] = "pilot"; t.approve_config()
        self.assertEqual(t.producer()["status"], "PASS")
        # The runtime now answers with a fingerprint; the frozen 27B expectation is null.
        self.fingerprints = []
        original_factory = sys.modules["openai"].OpenAI
        owner = self

        def factory(**kwargs):
            client = original_factory(**kwargs)
            create = client.chat.completions.create

            def wrapped(**payload):
                raw = deepcopy(create(**payload).model_dump())
                if payload["model"] == "fixture-alternate-model":
                    raw["system_fingerprint"] = FINGERPRINT
                    owner.fingerprints.append(payload)
                return types.SimpleNamespace(model_dump=lambda **unused: raw)
            return types.SimpleNamespace(chat=types.SimpleNamespace(
                completions=types.SimpleNamespace(create=wrapped)))
        t.stack.enter_context(patch.dict(sys.modules, {"openai": types.SimpleNamespace(OpenAI=factory)}))
        with self.assertRaisesRegex(HarnessError, "pilot suspended"):
            t.producer(stage="alternate_conformity")
        self.suspended = t.ledger.leaf("alternate_conformity", "agent_1")["request_id"]
        self.native_before = t.ledger.snapshot()["native_requests"]
        self.previous_config = t.config_path.read_bytes()

    # helpers -----------------------------------------------------------------
    def revise(self, execute=True, **kw):
        values = dict(config_path=self.t.config_path, ledger_path=self.t.ledger.path,
                      pilot_id=self.t.ledger.pilot_id, author="FIXTURE AUTHOR",
                      reason="27B runtime now reports a system fingerprint", fingerprint=FINGERPRINT,
                      suspended_request_id=self.suspended, execute=execute)
        values.update(kw)
        from studio2.fase03 import revise_pilot_config as rev
        return rev.revise(**values)

    def rev2_provider(self):
        return self.t.alternate_provider.with_name("alternate_provider.rev2.json")

    def resume_alternate(self, retry=True):
        self.t.config = json.loads(self.t.config_path.read_text())
        return pp.run(source_inventory=self.t.source, results_dir=self.t.home / "results",
                      provider_path=self.rev2_provider(), snapshot=self.t.snapshot, schema_dir=SCHEMA,
                      ledger=self.t.ledger, stage="alternate_conformity", resume=True,
                      retry_requests=[self.suspended] if retry else [])

    # properties --------------------------------------------------------------
    def test_REV0_fixture_reproduces_blocked_state(self):
        self.assertIn("suspended:" + self.suspended, self.t.ledger.snapshot()["events"])
        record = self.t.ledger.response(self.suspended)["record"]
        self.assertEqual(record["system_fingerprint"], FINGERPRINT)
        self.assertFalse(record["identity_valid"])
        with self.assertRaisesRegex(HarnessError, "pilot suspended"):
            self.t.ledger.verify_stage_success("producer_conformity")

    def test_REV1_plan_only_writes_nothing(self):
        before = _dump(self.t.ledger.path)
        files = sorted(p.name for p in self.t.home.iterdir())
        result = self.revise(execute=False)
        self.assertEqual(result["status"], "PLAN_ONLY")
        self.assertEqual(sorted(p.name for p in self.t.home.iterdir()), files)
        self.assertEqual(_dump(self.t.ledger.path), before)
        self.assertEqual(self.t.config_path.read_bytes(), self.previous_config)
        from studio2.fase03 import revise_pilot_config as rev
        with self.assertRaises(SystemExit):
            rev.main(["--runtime", str(self.t.home), "--author", "X", "--execute", "--acknowledge", "WRONG"])
        self.assertEqual(_dump(self.t.ledger.path), before)

    def test_REV2_revision_then_resume_passes_alternate_budget_and_gate(self):
        result = self.revise()
        self.assertEqual(result["status"], "REVISED", result)
        config = json.loads(self.t.config_path.read_text())
        self.assertEqual(config["d9"]["services"]["27B"]["expected_response"]["system_fingerprint"], FINGERPRINT)
        provider = json.loads(self.rev2_provider().read_text())
        self.assertEqual(provider["extra_body"], {"chat_template_kwargs": {"enable_thinking": False}})
        self.assertEqual(provider["max_tokens"], json.loads(self.t.alternate_provider.read_text())["max_tokens"])
        doc = json.loads(Path(config["d9"]["services"]["27B"]["documentation"]["path"]).read_text())
        self.assertEqual(doc["service"]["expected_response"]["system_fingerprint"], FINGERPRINT)
        summary = self.resume_alternate()
        self.assertEqual(summary["status"], "PASS")
        self.assertTrue(all(p["extra_body"] == {"chat_template_kwargs": {"enable_thinking": False}}
                            for p in self.fingerprints[1:]))
        leaves = self.t.ledger.stage_records("alternate_conformity")
        self.assertEqual(len(leaves), 8)
        self.assertTrue(all(r["identity_valid"] for r in leaves))
        self.assertFalse(self.t.ledger.response(self.suspended)["record"]["identity_valid"])
        snapshot = self.t.ledger.snapshot()
        self.assertEqual(snapshot["native_requests"], self.native_before + 8)
        self.assertEqual(snapshot["requalification_calls"], 1)
        self.assertEqual(snapshot["planned_maximum_with_alternate"], 161)
        self.assertEqual(snapshot["reserve_equation_value"], 0)
        runtime = self.t.home / "runtime"
        handoff = self.t.home / "results/validated_insight_library_fixture_producer_conformity.json"
        ready = acc.run(runtime=runtime, worktree=ROOT, author="FIXTURE AUTHOR", evidence_root=REFERENCE,
                        execute=True, config_path=self.t.config_path, handoff=handoff,
                        snapshot=self.t.snapshot, schema_dir=SCHEMA)
        self.assertEqual(ready["status"], acc.READY, ready["blocking"])
        rp.run_budget_stage(runtime / "prepared", self.t.home / "cr", ledger=self.t.ledger)
        rp.run_stability_stage(runtime / "prepared", self.t.home / "cr", ledger=self.t.ledger)
        self.assertEqual(len(self.t.consumer_calls), 123)

    def test_REV3_revision_outside_allowed_keys_is_refused(self):
        previous = self.t.config_path.with_name("previous.json")
        previous.write_bytes(self.previous_config)
        for name, mutate in {
                "generation": lambda c: c["generation_budget"].__setitem__("seed", 1),
                "122B": lambda c: c["d9"]["services"]["122B"].__setitem__("max_output_tokens", 1),
                "27B_model": lambda c: c["d9"]["services"]["27B"].__setitem__("max_model_len", 1),
                "presentation": lambda c: c.__setitem__("pilot_go", True)}.items():
            with self.subTest(name=name):
                value = json.loads(self.previous_config)
                mutate(value)
                new = self.t.home / f"bad-{name}.json"
                new.write_text(json.dumps(value))
                approval = self.t.home / f"bad-{name}-approval.json"
                approval.write_text(json.dumps(dict(decision="accepted", author="FIXTURE AUTHOR",
                                                    previous_sha256=sha256_file(previous),
                                                    new_sha256=sha256_file(new), reason="bad")))
                with self.assertRaisesRegex(HarnessError, "config revision"):
                    self.t.ledger.record_config_revision(previous_config_path=previous,
                                                         new_config_path=new, approval_path=approval)
        self.assertFalse(any(e.startswith("config_revision:") for e in self.t.ledger.snapshot()["events"]))

    def test_REV4_bindings_accept_registered_revision_only(self):
        self.revise()
        from studio2.fase03.harness.guards import require_pilot_ledger
        config = json.loads(self.t.config_path.read_text())
        require_pilot_ledger(config, self.t.ledger)
        self.t.ledger.binding("producer_conformity")
        unregistered = deepcopy(config)
        unregistered["d9"]["services"]["27B"]["expected_response"]["system_fingerprint"] = "other"
        with self.assertRaisesRegex(HarnessError, "revision"):
            require_pilot_ledger(unregistered, self.t.ledger)
        with self.assertRaisesRegex(HarnessError, "revision"):
            require_pilot_ledger(json.loads(self.previous_config), self.t.ledger)

    def test_REV5_suspension_reconciliation_guards(self):
        with self.assertRaisesRegex(HarnessError, "revision"):
            self.revise(fingerprint="another-fingerprint")
        events = self.t.ledger.snapshot()["events"]
        self.assertIn("suspended:" + self.suspended, events)
        self.assertFalse(any(e.startswith(("suspension_reconciled:", "config_revision:")) for e in events))
        self.assertEqual(self.t.config_path.read_bytes(), self.previous_config)
        # A request created after the suspension forbids reconciliation.
        with closing(sqlite3.connect(self.t.ledger.path)) as connection:
            row = connection.execute("SELECT * FROM requests WHERE request_id=?", (self.suspended,)).fetchone()
            values = list(row); values[0] = "after-suspension"; values[1] = "agent_2"; values[7] = None
            values[9] = "COMPLETED"; values[10] = "2999-01-01T00:00:00+00:00"
            connection.execute(f"INSERT INTO requests VALUES ({','.join('?' * len(values))})", values)
            connection.commit()
        with self.assertRaisesRegex(HarnessError, "after the suspension"):
            self.revise()

    def test_REV6_resend_requires_explicit_single_requalification(self):
        with self.assertRaisesRegex(HarnessError, "pilot suspended"):
            pp.run(source_inventory=self.t.source, results_dir=self.t.home / "results",
                   provider_path=self.t.alternate_provider, snapshot=self.t.snapshot, schema_dir=SCHEMA,
                   ledger=self.t.ledger, stage="alternate_conformity", resume=True,
                   retry_requests=[self.suspended])
        self.revise()
        with self.assertRaisesRegex(HarnessError, "suspended|identity"):
            self.resume_alternate(retry=False)
        self.assertEqual(self.t.ledger.snapshot()["native_requests"], self.native_before)
        original = self.t.ledger.request(self.suspended)
        with self.assertRaisesRegex(HarnessError, "stage inputs changed|stage_run"):
            self.t.ledger.reserve_requalification_retry(
                request_id="stale-binding", logical_id="agent_1", model=original["model"],
                producer=original["producer"], stage="alternate_conformity",
                stage_run=original["stage_run"], retry_of=self.suspended)
        self.resume_alternate()
        leaf = self.t.ledger.leaf("alternate_conformity", "agent_1")
        self.assertEqual((leaf["retry_of"], leaf["quota_kind"]), (self.suspended, "requalification"))
        with closing(sqlite3.connect(self.t.ledger.path)) as connection:
            self.assertEqual(connection.execute(
                "SELECT count(*) FROM requests WHERE quota_kind='requalification'").fetchone()[0], 1)
        # The quota is single even across stages or chains.
        with self.assertRaisesRegex(HarnessError, "requalification|closed stage"):
            self.t.ledger.reserve_requalification_retry(
                request_id="second", logical_id="agent_1", model=leaf["model"], producer=leaf["producer"],
                stage="alternate_conformity", stage_run=leaf["stage_run"], retry_of=leaf["request_id"])

    def test_REV7_idempotent_revision(self):
        self.revise()
        files = {p: p.read_bytes() for p in self.t.home.iterdir() if p.is_file()}
        dump = _dump(self.t.ledger.path)
        again = self.revise()
        self.assertEqual(again["status"], "REVISED")
        self.assertTrue(all(c["action"] == "UNCHANGED" for c in again["changes"]), again["changes"])
        self.assertEqual({p: p.read_bytes() for p in self.t.home.iterdir() if p.is_file()}, files)
        self.assertEqual(_dump(self.t.ledger.path), dump)

    def test_REV8_corrupted_revision_or_reconciliation_blocks(self):
        self.revise()
        for event, mutate in [("config_revision:1", lambda d: d["new"]["content"].__setitem__("pilot_go", True)),
                              ("suspension_reconciled:" + self.suspended,
                               lambda d: d["approval"]["content"].__setitem__("author", "someone else"))]:
            with self.subTest(event=event):
                with closing(sqlite3.connect(self.t.ledger.path)) as connection:
                    original = connection.execute("SELECT detail_json FROM events WHERE event=?", (event,)).fetchone()[0]
                    detail = json.loads(original); mutate(detail)
                    connection.execute("UPDATE events SET detail_json=? WHERE event=?", (json.dumps(detail), event))
                    connection.commit()
                with self.assertRaises(HarnessError):
                    self.t.ledger.verify_stage_success("producer_conformity")
                with closing(sqlite3.connect(self.t.ledger.path)) as connection:
                    connection.execute("UPDATE events SET detail_json=? WHERE event=?", (original, event))
                    connection.commit()
        self.t.ledger.verify_stage_success("producer_conformity")

    def test_REV9_rebinding_limited_to_approved_provider_change(self):
        self.revise()
        provider = json.loads(self.rev2_provider().read_text())
        provider["max_tokens"] = 1
        bad = self.t.home / "bad_provider.json"; bad.write_text(json.dumps(provider))
        with self.assertRaises(HarnessError):
            pp.run(source_inventory=self.t.source, results_dir=self.t.home / "results", provider_path=bad,
                   snapshot=self.t.snapshot, schema_dir=SCHEMA, ledger=self.t.ledger,
                   stage="alternate_conformity", resume=True, retry_requests=[self.suspended])
        self.assertEqual(self.t.ledger.snapshot()["native_requests"], self.native_before)

    def test_REV10_rebinding_guard_rejects_other_changes(self):
        self.revise()
        ledger = self.t.ledger
        head = ledger.config_revisions()[-1]
        with ledger._transaction() as c:
            old = ledger._binding(c, "alternate_conformity")
        good = deepcopy(old)
        good["execution_config"] = head
        good["provider"] = json.loads(self.rev2_provider().read_text())
        good["provider_file_sha256"] = head["d9"]["producer_configs"]["27B"]
        good["provider_reference"] = {"path": str(self.rev2_provider()), "sha256": good["provider_file_sha256"]}
        cases = {
            "max_tokens": lambda b: b["provider"].__setitem__("max_tokens", 1),
            "thinking_on": lambda b: b["provider"]["extra_body"]["chat_template_kwargs"].__setitem__("enable_thinking", True),
            "model": lambda b: b["provider"]["expected_response"].__setitem__("returned_model", "other"),
            "template": lambda b: b.__setitem__("template_text", "changed\n"),
            "stale_config": lambda b: b.__setitem__("execution_config", json.loads(self.previous_config)),
        }
        for name, mutate in cases.items():
            with self.subTest(name=name):
                bad = deepcopy(good); mutate(bad)
                with self.assertRaises(HarnessError), ledger._transaction() as c:
                    ledger._rebind_stage(c, "alternate_conformity", old, bad)
        with self.assertRaisesRegex(HarnessError, "stage inputs changed"), ledger._transaction() as c:
            ledger._rebind_stage(c, "producer_conformity", old, good)
        self.assertFalse(any(e.startswith("stage_rebinding:") for e in ledger.snapshot()["events"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
