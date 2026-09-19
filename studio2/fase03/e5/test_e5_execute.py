"""Offline tests of the E5 execution adapter (``run_e5_execute.py``).

SACRIFICIAL FIXTURES ONLY: synthetic carriers, synthetic provider, no socket. Every slot goes
through the real ``run_final_batch.run_pass`` / ``harness.runtime.execute_request`` and the
real canary ``run_final_canary.run_day``, as the batch tests do.

    python -m unittest studio2.fase03.e5.test_e5_execute -v
"""

from __future__ import annotations

import json
from pathlib import Path
import sqlite3
import tempfile
import unittest

from studio2.fase03.e5 import run_e5_execute as e5x
from studio2.fase03.harness.common import HarnessError, sha256_text
from studio2.fase03.harness.ledger import FINAL_PASS_STAGES, PilotLedger
from studio2.fase03.harness import final_inventory
from studio2.fase03.harness.runtime import IdentitySuspension
from studio2.fase03.harness.test_final_batch import INSIGHTS, FakeProvider, FinalBatchBase
from studio2.fase03 import run_final_batch

from verifica_e5_c2_prompt import CASE_HEADING, SCHEMA_HEADING, compose, split_carrier  # noqa: E402

ROWS = 4  # 2 recipients x (PERM, OMIT)
_BATCH_ENTRIES = None


def batch_entries():
    """The batch schedule as the committed generator writes it (the target holds these bytes)."""
    global _BATCH_ENTRIES
    if _BATCH_ENTRIES is None:
        _BATCH_ENTRIES = final_inventory.build_schedule(final_inventory.build_inventory())
    return _BATCH_ENTRIES


def batch_source():
    return e5x.truth_source(batch_entries())


class SmallE5Ledger(e5x.E5Ledger):
    envelope = e5x.e5_profile(ROWS)


def carrier_text(case: str) -> str:
    return ("BASE INSTRUCTION\n\nFIXTURE ONLY policy and library\n\n" + CASE_HEADING + "\n\n"
            + case + "\n\n" + SCHEMA_HEADING + "\n\n{\"predicted_label\":null}\n")


def fixture_carriers_and_manifest():
    """Two real (case, receiver) cells of RICEVENTI_E5 for family ``level``; synthetic bytes."""
    derangement = json.loads(e5x.DERANGEMENTS.read_text())["derangements"]["level"]["pairs"]
    receivers = json.loads(e5x.RECIPIENTS.read_text())["recipients"]["assignments"]
    carriers, rows = {}, []
    for recipient, donor in sorted(derangement.items())[:2]:
        agent = receivers[recipient][0]
        stable = f"nucleus|B-LF|{recipient}|{agent}|G_P"
        text = carrier_text(f"FIXTURE ONLY neutral text {sha256_text(recipient)[:12]}")
        carriers[stable] = {"prompt_id": stable, "stable_id": stable, "block": "nucleus",
                            "condition": "B-LF", "case_id": recipient, "agent_id": agent,
                            "library_role": "G_P", "available_insight_ids": INSIGHTS,
                            "text": text, "prompt_sha256": sha256_text(text),
                            "prompt_bytes": len(text.encode())}
        prefix, _, suffix = split_carrier(text)
        for arm in ("PERM", "OMIT"):
            altered = compose(prefix, f"FIXTURE ONLY {arm} text {sha256_text(recipient + donor)[:12]}", suffix)
            pid = f"e5_{arm.lower()}_level_{recipient}_{agent}_gp"
            rows.append({"prompt_id": pid, "stable_id": pid, "source_stable_id": stable, "arm": arm,
                         "family": "level", "case_id": recipient, "donor_case_id": donor,
                         "agent_id": agent, "text": altered, "prompt_sha256": sha256_text(altered)})
    return carriers, rows


class E5Offline(unittest.TestCase):
    def setUp(self):
        self.carriers, self.rows = fixture_carriers_and_manifest()

    def test_rendered_rows_keep_the_renderer_contract_and_reprove_s18(self):
        rendered = e5x.rendered_rows(self.rows, self.carriers)
        self.assertEqual({r["block"] for r in rendered}, {"e5_perm", "e5_omit"})
        self.assertEqual({r["condition"] for r in rendered}, {"B-LF"})
        self.assertTrue(all(tuple(r) == run_final_batch.RENDERED_ROW_KEYS for r in rendered))
        bad = dict(self.rows[0], text=self.rows[0]["text"].replace("BASE", "BASE!"))
        bad["prompt_sha256"] = sha256_text(bad["text"])
        with self.assertRaises(Exception):
            e5x.rendered_rows([bad], self.carriers)

    def test_carrier_must_be_the_b_lf_g_p_nucleus_cell(self):
        stable = self.rows[0]["source_stable_id"]
        carriers = dict(self.carriers, **{stable: dict(self.carriers[stable], library_role="G_A")})
        with self.assertRaises(HarnessError):
            e5x.rendered_rows(self.rows, carriers)

    def test_schedule_is_deterministic_and_takes_truth_from_the_batch_inventory(self):
        one = e5x.build_schedule(self.rows, batch_source(), expected_rows=ROWS)
        self.assertEqual(one, e5x.build_schedule(self.rows, batch_source(), expected_rows=ROWS))
        self.assertEqual(len(one), ROWS * 3)
        self.assertEqual(sorted({r["repetition"] for r in one}), [1, 2, 3])
        batch = {r["stable_id"]: r for r in batch_entries()}
        for row in one:
            for key in e5x.TRUTH_FIELDS:
                self.assertEqual(row[key], batch[row["source_stable_id"]][key])
            self.assertEqual(row["logical_id"], f"{row['stable_id']}|r{row['repetition']}")
            self.assertNotIn("|", row["stable_id"])

    def test_a_batch_schedule_that_disagrees_with_the_committed_inventory_stops(self):
        entries = [dict(r) for r in batch_entries()]
        target = next(r for r in entries if r["stable_id"] == self.rows[0]["source_stable_id"])
        target["true_pseudolabel"] = "S2-CLS-ZZZZZ"
        with self.assertRaises(HarnessError):
            e5x.truth_source(entries)

    def test_configuration_changes_only_ledger_and_target_identity(self):
        batch = {"candidate": {"requested_model": "m"}, "expected_response": {"returned_model": "m",
                 "system_fingerprint": "f"}, "pilot_ledger": {"path": "/b/ledger", "pilot_id": "batch-01"},
                 "d9": {"services": {"x": 1}, "final_target": {"artifact_version": "FINAL_TARGET_1",
                        "target_id": "batch-01", "predecessor_consumption": "NONE_FRESH_TARGET"}},
                 "execution_authorization": {"path": "/b/a"}, "call_budget": {}, "derived_from": {}}
        config = e5x.e5_configuration(batch, ledger_path=Path("/e5/ledger.sqlite3"),
                                      batch_config_sha256="0" * 64, batch_target_id="batch-01")
        self.assertEqual(config["expected_response"], batch["expected_response"])
        self.assertEqual(config["d9"]["final_target"]["target_id"], e5x.TARGET_ID)
        self.assertEqual(config["pilot_ledger"]["pilot_id"], e5x.TARGET_ID)
        self.assertNotIn("execution_authorization", config)
        self.assertEqual(config["call_budget"]["stage_quota"]["final_batch_r1"], e5x.E5_PASS_ROWS)

    def test_the_batch_ledger_is_never_opened_as_an_e5_ledger(self):
        with tempfile.TemporaryDirectory() as home:
            path = Path(home).resolve() / "batch.sqlite3"
            PilotLedger(path, pilot_id=e5x.TARGET_ID, profile="final_batch")
            with self.assertRaises(HarnessError):
                e5x.E5Ledger(path)
            ledger = e5x.E5Ledger(Path(home).resolve() / "e5.sqlite3")
            self.assertEqual(ledger.profile.base_limits["final_batch_r1"], e5x.E5_PASS_ROWS)
            self.assertEqual(ledger.profile.name, "final_batch")
            e5x.E5Ledger(Path(home).resolve() / "e5.sqlite3")  # reopen: same envelope

    def test_batch_closed_is_read_only_and_needs_the_last_closure(self):
        with tempfile.TemporaryDirectory() as home:
            path = Path(home) / "batch.sqlite3"
            self.assertFalse(e5x.batch_closed(path))
            with sqlite3.connect(path) as c:
                c.execute("CREATE TABLE events (event TEXT PRIMARY KEY)")
                c.execute("INSERT INTO events VALUES ('outcome:final_batch_r2')")
            self.assertFalse(e5x.batch_closed(path))
            with sqlite3.connect(path) as c:
                c.execute("INSERT INTO events VALUES ('outcome:final_batch_r3')")
            self.assertTrue(e5x.batch_closed(path))

    def test_metric_row_is_the_batch_scoring(self):
        row = {"true_pseudolabel": "S2-CLS-AAAAA", "case_id": "c"}
        ok = {"parse_valid_first_attempt": True, "parsed_output": {"predicted_label": "S2-CLS-AAAAA", "abstain": False}}
        self.assertTrue(e5x.metric_row(ok, row)["correct"])
        abst = {"parse_valid_first_attempt": True, "parsed_output": {"predicted_label": None, "abstain": True}}
        self.assertTrue(e5x.metric_row(abst, row)["abstained"])
        invalid = {"parse_valid_first_attempt": False, "parsed_output": None}
        self.assertEqual((e5x.metric_row(invalid, row)["valid"], e5x.metric_row(invalid, row)["correct"]), (False, False))


class E5Execution(FinalBatchBase):
    """The E5 rows through the real pass, canary, retry, identity STOP and closure."""

    rows_per_pass = ROWS

    def setUp(self):
        super().setUp()
        carriers, rows = fixture_carriers_and_manifest()
        self.ledger = SmallE5Ledger(self.home.resolve() / "e5.sqlite3", pilot_id=self.pilot_id)
        self.schedule = e5x.build_schedule(rows, batch_source(), expected_rows=ROWS)
        path = self.home / "e5_prompts.jsonl"
        path.write_text("".join(json.dumps(r) + "\n" for r in e5x.rendered_rows(rows, carriers)),
                        encoding="utf-8")
        self.target["prompts"] = {"path": str(path), "sha256": "1" * 64}
        self.prompts = e5x.load_prompts(self.target, label_space=run_final_batch.target_label_space(self.target))
        run_final_batch.executable_rows(self.schedule, self.prompts)

    def test_a_pass_runs_the_e5_rows_and_scores_them(self):
        self.pass_canary_day()
        summary = self.run_pass()
        self.assertEqual((summary["status"], summary["sent_this_run"]), ("COMPLETE", ROWS))
        leaf = self.ledger.leaf(FINAL_PASS_STAGES[0], self.schedule[0]["logical_id"])
        record = self.ledger.response(leaf["request_id"])["record"]
        self.assertEqual(record["sample_role"], e5x.E5_SAMPLE_ROLE)
        self.assertIn(record["block"], ("e5_perm", "e5_omit"))
        with self.assertRaises(run_final_batch.BatchStop):
            e5x.score(self.target | {"target_id": e5x.TARGET_ID}, self.ledger, self.schedule)
        scores = e5x.score(self.target | {"target_id": e5x.TARGET_ID}, self.ledger, self.schedule, partial=True)
        self.assertEqual((scores["status"], scores["open_passes"]),
                         ("PARTIAL_NOT_ANALYZABLE", list(FINAL_PASS_STAGES)))
        self.assertEqual(scores["status_counts"], {"COMPLETED": ROWS, "MISSING": 2 * ROWS})

    def test_no_scientific_call_without_the_canary(self):
        with self.assertRaises(HarnessError):
            self.run_pass()
        self.assertEqual(self.ledger.snapshot()["requests_by_stage"][FINAL_PASS_STAGES[0]], 0)

    def test_identity_change_stops(self):
        self.pass_canary_day()
        FakeProvider.script = {self.schedule[0]["logical_id"]: "identity"}
        with self.assertRaises(IdentitySuspension):
            self.run_pass()
        FakeProvider.script = {}

    def test_unobserved_transport_is_retried_then_abandoned_and_the_pass_closes(self):
        from studio2.fase03.harness.test_unobserved_transport_retry import RetryProvider
        RetryProvider.failures, RetryProvider.script = {}, {self.schedule[0]["logical_id"]: "sdk:APIConnectionError"}
        self.pass_canary_day()
        summary = self.run_pass(provider_factory=RetryProvider, sleep=lambda _: None)
        self.assertEqual(summary["abandoned_unobserved_transport"], [self.schedule[0]["logical_id"]])
        artifact = run_final_batch.close_pass(target=self.target, ledger=self.ledger, pass_index=1)
        self.assertEqual(artifact["planned"], ROWS)
        scores = e5x.score(self.target | {"target_id": e5x.TARGET_ID}, self.ledger, self.schedule, partial=True)
        self.assertEqual(scores["status_counts"]["ABANDONED"], 1)
        self.assertEqual(scores["open_passes"], list(FINAL_PASS_STAGES[1:]))
        RetryProvider.script = {}


class G3Check(unittest.TestCase):
    def test_g3_reproves_s18_scans_leakage_and_writes_case_texts(self):
        import verifica_e5_g3
        carriers, manifest = full_fixture_manifest()
        with tempfile.TemporaryDirectory() as home:
            home = Path(home)
            (home / "fp.jsonl").write_text("".join(json.dumps(r) + "\n" for r in carriers.values()))
            (home / "m.json").write_text(json.dumps(manifest))
            (home / "ct.jsonl").write_text("STALE")
            out = verifica_e5_g3.check(manifest=home / "m.json", full_prompts=home / "fp.jsonl",
                                       case_texts=home / "ct.jsonl", expected_inert=[])
            self.assertEqual((out["s18_and_carrier_failures"], out["leakage_findings_in_case_blocks"]), ([], []))
            self.assertEqual((out["perm_pairs_for_c2"], out["plan"]["planned_calls"]), (96, 576))
            self.assertEqual(out["status"], "FAIL")  # 192 synthetic carriers, not the 2,244 of the batch
            self.assertFalse((home / "ct.jsonl").exists())  # stale file removed, nothing written on FAIL
            self.assertEqual(out["case_texts"], "NOT WRITTEN: G3 failed")
            row = manifest["rows"][0]
            prefix, _, suffix = split_carrier(row["text"])
            row["text"] = compose(prefix, "FIXTURE ONLY leak IDV(1)", suffix)
            row["prompt_sha256"] = sha256_text(row["text"])
            (home / "m.json").write_text(json.dumps(manifest))
            out = verifica_e5_g3.check(manifest=home / "m.json", full_prompts=home / "fp.jsonl",
                                       case_texts=home / "ct.jsonl", expected_inert=[])
            self.assertEqual(len(out["leakage_findings_in_case_blocks"]), 1)
            self.assertEqual(out["status"], "FAIL")
            self.assertFalse((home / "ct.jsonl").exists())

    def test_g3_writes_case_texts_only_on_pass(self):
        from unittest.mock import patch
        from studio2.fase03.protocol import canonical_json
        import verifica_e5_g3
        carriers, manifest = full_fixture_manifest()
        rows = list(carriers.values())
        for index in range(2244 - len(rows)):  # filler to the batch shape: 848 B-LF in 2,244
            text = f"FIXTURE ONLY filler {index}"
            rows.append({"prompt_id": f"filler-{index}", "stable_id": f"filler-{index}", "block": "x",
                         "condition": "B-LF" if index < 848 - len(carriers) else "A", "case_id": "c",
                         "agent_id": "agent_1", "library_role": "none", "text": text,
                         "prompt_sha256": sha256_text(text)})
        mapping = sha256_text(canonical_json([[r["prompt_id"], r["prompt_sha256"]] for r in rows]))
        with tempfile.TemporaryDirectory() as home, patch.object(verifica_e5_g3, "PROMPT_MAP_SHA256", mapping):
            home = Path(home)
            (home / "fp.jsonl").write_text("".join(json.dumps(r) + "\n" for r in rows))
            (home / "m.json").write_text(json.dumps(manifest))
            out = verifica_e5_g3.check(manifest=home / "m.json", full_prompts=home / "fp.jsonl",
                                       case_texts=home / "ct.jsonl", expected_inert=[])
            self.assertEqual(out["status"], "PASS")
            self.assertEqual(len((home / "ct.jsonl").read_text().splitlines()), 96)
            # the same bytes with an unexpected inert set: FAIL, and the file just written is gone
            out = verifica_e5_g3.check(manifest=home / "m.json", full_prompts=home / "fp.jsonl",
                                       case_texts=home / "ct.jsonl", expected_inert=["e5_perm_x"])
            self.assertEqual((out["status"], out["inert_as_expected"]), ("FAIL", False))
            self.assertFalse((home / "ct.jsonl").exists())

class InertPerm(unittest.TestCase):
    """REVISIONE_E5_001: a PERM whose case block the swap leaves unchanged is kept and marked."""

    def setUp(self):
        self.carriers, manifest = full_fixture_manifest()
        self.manifest = manifest
        row = next(r for r in manifest["rows"] if r["arm"] == "PERM")
        carrier = self.carriers[row["source_stable_id"]]
        row.update(text=carrier["text"], prompt_sha256=carrier["prompt_sha256"], inert=True)
        self.inert = row

    def test_case_proof_admits_only_an_unchanged_perm(self):
        from build_e5_prompts_rev1 import case_proof
        from build_e5_prompts import E5PromptError
        carrier = self.carriers[self.inert["source_stable_id"]]["text"]
        self.assertTrue(case_proof(carrier, carrier, arm="PERM")["inert"])
        with self.assertRaises(E5PromptError):
            case_proof(carrier, carrier, arm="OMIT")
        prefix, _, suffix = split_carrier(carrier)
        self.assertFalse(case_proof(carrier, compose(prefix, "FIXTURE ONLY other", suffix), arm="PERM")["inert"])

    def test_inert_rows_render_schedule_and_carry_the_flag(self):
        rendered = e5x.rendered_rows(self.manifest["rows"], self.carriers)
        self.assertEqual(len(rendered), 192)
        schedule = e5x.build_schedule(self.manifest["rows"], batch_source())
        flagged = {r["stable_id"] for r in schedule if r["inert"]}
        self.assertEqual(flagged, {self.inert["stable_id"]})
        self.assertEqual(sum(r["inert"] for r in schedule), 3)  # R=3, all sent

    def test_the_flag_must_match_the_bytes(self):
        unflagged = [dict(r, inert=False) if r is self.inert else r for r in self.manifest["rows"]]
        with self.assertRaises(HarnessError):
            e5x.rendered_rows(unflagged, self.carriers)
        other = next(r for r in self.manifest["rows"] if r["arm"] == "PERM" and r is not self.inert)
        wrong = [dict(r, inert=True) if r is other else r for r in self.manifest["rows"]]
        with self.assertRaises(HarnessError):
            e5x.rendered_rows(wrong, self.carriers)

    def test_g3_lists_inert_rows_and_does_not_fail_on_them(self):
        import verifica_e5_g3
        with tempfile.TemporaryDirectory() as home:
            home = Path(home)
            (home / "fp.jsonl").write_text("".join(json.dumps(r) + "\n" for r in self.carriers.values()))
            (home / "m.json").write_text(json.dumps(self.manifest))
            out = verifica_e5_g3.check(manifest=home / "m.json", full_prompts=home / "fp.jsonl", case_texts=None,
                                       expected_inert=[self.inert["prompt_id"]])
            self.assertEqual(out["s18_and_carrier_failures"], [])
            self.assertEqual(out["inert_perm_prompts"], [self.inert["prompt_id"]])
            self.assertTrue(out["inert_as_expected"])
            out = verifica_e5_g3.check(manifest=home / "m.json", full_prompts=home / "fp.jsonl", case_texts=None,
                                       expected_inert=[])
            self.assertFalse(out["inert_as_expected"])

    def test_the_committed_expectation_is_eight_perm_ids(self):
        import verifica_e5_g3
        ids = verifica_e5_g3.expected_inert_ids()
        self.assertEqual(len(ids), 8)
        self.assertTrue(all(i.startswith("e5_perm_") for i in ids))


from studio2.fase03.harness import test_final_target_d9 as _d9t  # noqa: E402


class E5RealD9(_d9t.FinalTargetD9):
    """E5 configuration derived from a real ``d9.final_target`` config: whole D9 chain, real bindings."""

    rows_per_pass = ROWS

    def setUp(self):
        super().setUp()
        from studio2.fase03.harness.common import sha256_file
        batch_config = self.config
        path = self.home.resolve() / "e5.sqlite3"
        config = e5x.e5_configuration(batch_config, ledger_path=path, batch_config_sha256="0" * 64,
                                      batch_target_id=self.pilot_id)
        approval = self.home / "e5_authorization.json"
        approval.write_text(json.dumps(e5x.authorization(author="FIXTURE ONLY",
                                                         configuration=e5x.configuration_sha256(config))))
        config["execution_authorization"] = {"path": str(approval), "sha256": sha256_file(approval)}
        self.batch_config, self.config = batch_config, config
        self.ledger = SmallE5Ledger(path)
        carriers, rows = fixture_carriers_and_manifest()
        self.schedule = e5x.build_schedule(rows, batch_source(), expected_rows=ROWS)
        prompts = self.home / "e5_prompts.jsonl"
        prompts.write_text("".join(json.dumps(r) + "\n" for r in e5x.rendered_rows(rows, carriers)),
                           encoding="utf-8")
        self.target["prompts"] = {"path": str(prompts), "sha256": "1" * 64}
        self.prompts = e5x.load_prompts(self.target, label_space=run_final_batch.target_label_space(self.target))

    def test_e5_config_passes_the_d9_chain_and_keeps_the_batch_identity(self):
        from studio2.fase03.harness.guards import require_execution, require_pilot_ledger
        require_execution(self.config)
        require_pilot_ledger(self.config, self.ledger)
        for key in ("candidate", "expected_response"):
            self.assertEqual(self.config[key], self.batch_config[key])
        self.assertEqual(self.config["d9"]["services"], self.batch_config["d9"]["services"])

    def test_e5_canary_and_pass_on_real_bindings(self):
        self.assertEqual(self.pass_canary_day()["verdict"], "PASS")
        summary = self.run_pass(provider_factory=_d9t.QualifiedProvider)
        self.assertEqual((summary["status"], summary["planned"]), ("COMPLETE", ROWS))
        self.assertEqual(self.ledger.binding(FINAL_PASS_STAGES[0])["execution_config"], self.config)

    def test_a_different_fingerprint_stops_e5(self):
        self.pass_canary_day()
        FakeProvider.script = {self.schedule[0]["logical_id"]: "identity"}
        with self.assertRaises(IdentitySuspension):
            self.run_pass(provider_factory=FakeProvider)
        FakeProvider.script = {}

    def test_the_batch_config_cannot_open_the_e5_ledger(self):
        from studio2.fase03.harness.guards import require_pilot_ledger
        with self.assertRaises(HarnessError):
            require_pilot_ledger(self.batch_config, self.ledger)


for _name in dir(_d9t.FinalTargetD9):
    if _name.startswith("test_"):
        setattr(E5RealD9, _name, None)  # the batch's own tests stay in their module


def full_fixture_manifest():
    """All 192 real E5 cells (DERANGEMENTS x RICEVENTI) with synthetic carrier bytes."""
    derangements = json.loads(e5x.DERANGEMENTS.read_text())["derangements"]
    receivers = json.loads(e5x.RECIPIENTS.read_text())["recipients"]["assignments"]
    carriers, rows = {}, []
    for family, value in sorted(derangements.items()):
        for recipient, donor in sorted(value["pairs"].items()):
            agent = receivers[recipient][0]
            stable = f"nucleus|B-LF|{recipient}|{agent}|G_P"
            text = carrier_text(f"FIXTURE ONLY neutral text {sha256_text(recipient)[:12]}")
            carriers[stable] = {"prompt_id": stable, "stable_id": stable, "block": "nucleus",
                                "condition": "B-LF", "case_id": recipient, "agent_id": agent,
                                "library_role": "G_P", "available_insight_ids": INSIGHTS,
                                "text": text, "prompt_sha256": sha256_text(text),
                                "prompt_bytes": len(text.encode())}
            prefix, _, suffix = split_carrier(text)
            for arm in ("PERM", "OMIT"):
                altered = compose(prefix, f"FIXTURE ONLY {arm} {family} {sha256_text(recipient + donor)[:12]}", suffix)
                pid = f"e5_{arm.lower()}_{family}_{recipient}_{agent}_gp"
                rows.append({"prompt_id": pid, "stable_id": pid, "source_stable_id": stable,
                             "arm": arm, "family": family, "case_id": recipient,
                             "donor_case_id": donor, "agent_id": agent, "text": altered,
                             "prompt_sha256": sha256_text(altered)})
    from studio2.fase03.harness.common import sha256_file
    manifest = {"artifact_version": "E5_PROMPTS_1", "status": "OFFLINE_NOT_EXECUTED",
                "inputs": {"derangements_sha256": sha256_file(e5x.DERANGEMENTS),
                           "recipients_sha256": sha256_file(e5x.RECIPIENTS)},
                "rows": rows,
                "s18_case_block_diff": [{"prompt_id": r["prompt_id"], "status": "PASS"} for r in rows]}
    return carriers, manifest


class E5Materialize(_d9t.FinalTargetD9):
    """``materialize`` plan and execute on a fixture batch target; then the real E5 runtime path."""

    def setUp(self):
        super().setUp()
        from argparse import Namespace
        from unittest.mock import patch
        from studio2.fase03.harness.common import sha256_file
        home = self.home.resolve()
        carriers, manifest = full_fixture_manifest()
        files = {"prompts": home / "batch_prompts.jsonl", "schedule": home / "batch_schedule.json",
                 "config": home / "batch_config.json"}
        files["prompts"].write_text("".join(json.dumps(r) + "\n" for r in carriers.values()))
        files["schedule"].write_text(json.dumps({"entries": batch_entries()}))
        files["config"].write_text(json.dumps(self.config))
        expectations = Path(self.target["canary_expectations"]["path"])
        self.stack.enter_context(patch.object(e5x, "CANARY_EXPECTATIONS", expectations))
        batch = {"artifact_version": "TARGET_FINALE_7_4_1", "target_id": self.pilot_id,
                 "ledger": {"path": str(self.ledger.path), "pilot_id": self.pilot_id, "profile": "final_batch"},
                 **{role: {"path": str(path), "sha256": sha256_file(path)} for role, path in files.items()},
                 "canary_expectations": {"path": str(expectations), "sha256": sha256_file(expectations)},
                 "canary_prompts": {"path": self.target["canary_prompts"]["path"],
                                    "sha256": sha256_file(Path(self.target["canary_prompts"]["path"]))},
                 "tokenizer_snapshot": self.target["tokenizer_snapshot"], "generation": self.generation,
                 "results_dir": str(home / "batch_results")}
        (home / "TARGET_FINALE_7_4.json").write_text(json.dumps(batch))
        self.committed_inert = e5x.EXPECTED_INERT
        (home / "inert.json").write_text(json.dumps({"inert_prompt_ids": []}))  # fixture has none
        self.stack.enter_context(patch.object(e5x, "EXPECTED_INERT", home / "inert.json"))
        (home / "e5_manifest.json").write_text(json.dumps(manifest))
        self.arguments = Namespace(batch_target=home / "TARGET_FINALE_7_4.json",
                                   e5_prompts=home / "e5_manifest.json", test_input=None,
                                   root=home / "e5root", pilot_manifest=None, execute=False,
                                   acknowledge=None, author=None, accept_configuration_sha256=None)

    def test_a_batch_schedule_with_other_truth_is_refused(self):
        from studio2.fase03.harness.common import sha256_file
        path = Path(json.loads(self.arguments.batch_target.read_text())["schedule"]["path"])
        entries = [dict(r) for r in batch_entries()]
        entries[0]["true_pseudolabel"] = "S2-CLS-ZZZZZ"
        path.write_text(json.dumps({"entries": entries}))
        batch = json.loads(self.arguments.batch_target.read_text())
        batch["schedule"]["sha256"] = sha256_file(path)  # authenticated, yet not the committed truth
        self.arguments.batch_target.write_text(json.dumps(batch))
        with self.assertRaises(HarnessError):
            e5x.materialize(self.arguments)

    def test_an_inert_set_other_than_the_expected_one_is_refused(self):
        from unittest.mock import patch
        with patch.object(e5x, "EXPECTED_INERT", self.committed_inert), self.assertRaises(HarnessError):
            e5x.materialize(self.arguments)

    def test_plan_then_materialize_then_run_the_e5_target(self):
        plan = e5x.materialize(self.arguments)
        self.assertEqual(plan["status"], "PLAN_ONLY")
        self.assertEqual((plan["unique_prompts"], plan["planned_calls"]), (192, 576))
        self.assertEqual(plan["by_block"], {"e5_perm": 96, "e5_omit": 96})
        self.assertEqual(plan["rehearsal"]["pass_slots_planned"],
                         {stage: 192 for stage in FINAL_PASS_STAGES})
        self.assertEqual(plan["rehearsal"]["canary_slots_bound"], 300)
        self.assertFalse(plan["batch_closed"])
        self.assertFalse(self.arguments.root.exists())
        self.arguments.execute, self.arguments.acknowledge = True, e5x.ACK_MATERIALIZE
        self.arguments.author = "FIXTURE ONLY"
        with self.assertRaises(HarnessError):
            e5x.materialize(self.arguments)  # no accepted SHA
        self.arguments.accept_configuration_sha256 = plan["configuration_sha256_to_accept"]
        done = e5x.materialize(self.arguments)
        self.assertEqual(done["status"], "MATERIALIZED")
        target = e5x.load_target(Path(done["descriptor"]))
        schedule = e5x.load_schedule(target)
        self.assertEqual(len(schedule), 576)
        from studio2.fase03.harness.guards import require_execution, require_pilot_ledger
        config = json.loads(Path(target["config"]["path"]).read_text())
        require_execution(config)
        ledger = e5x.E5Ledger(Path(target["ledger"]["path"]))
        require_pilot_ledger(config, ledger)
        with self.assertRaises(run_final_batch.BatchStop):
            e5x.require_batch_closed(target)
        prompts = e5x.load_prompts(target, label_space=run_final_batch.target_label_space(target))
        from studio2.fase03 import run_final_canary
        day = run_final_canary.run_day(
            target=target, ledger=ledger, config=config, generation=target["generation"],
            schema=self.schema, day="2026-09-18", results_dir=Path(target["results_dir"]),
            execute=True, provider_factory=_d9t.QualifiedProvider, now=self.noon("2026-09-18"))
        self.assertEqual(day["verdict"], "PASS")
        summary = run_final_batch.run_pass(
            target=target, ledger=ledger, schedule=schedule, prompts=prompts, config=config,
            generation=target["generation"], schema=self.schema, pass_index=1,
            results_dir=Path(target["results_dir"]), execute=True, max_requests=3,
            provider_factory=_d9t.QualifiedProvider, day="2026-09-18", now=self.noon("2026-09-18"))
        self.assertEqual((summary["planned"], summary["sent_this_run"]), (192, 3))
        self.assertEqual(ledger.binding(FINAL_PASS_STAGES[0])["execution_config"], config)
        with self.assertRaises(HarnessError):
            e5x.materialize(self.arguments)  # a fresh target is never reused


for _name in dir(_d9t.FinalTargetD9):
    if _name.startswith("test_"):
        setattr(E5Materialize, _name, None)


if __name__ == "__main__":
    unittest.main()
