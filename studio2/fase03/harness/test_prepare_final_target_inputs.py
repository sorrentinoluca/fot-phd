"""Offline tests of ``prepare_final_target_inputs.py`` on a synthetic pilot runtime.

SACRIFICIAL FIXTURES ONLY. The pins of the real runtime are replaced by the fixture's own;
what is exercised is the derivation of the configuration, the byte-identical canary copy,
the author's acceptance and the rehearsal of the real D9 chain. No socket is ever opened.
"""

from __future__ import annotations

from contextlib import ExitStack, redirect_stdout
from copy import deepcopy
import io
import json
from pathlib import Path
import shutil
import unittest
from unittest.mock import patch

from .common import sha256_file, sha256_text
from .ledger import digest
from . import d9
from studio2.fase03 import materialize_final_target as materializer
from studio2.fase03 import prepare_final_target_inputs as prep

TARGET_ID = "studio2-fase03-batch-fixture"


class PrepareFinalTargetInputs(unittest.TestCase):
    def setUp(self):
        from .test_revisions import RunnerRevisions
        self.fixture = RunnerRevisions()
        self.fixture.setUp()
        self.addCleanup(self.fixture.doCleanups)
        self.stack = ExitStack()
        self.addCleanup(self.stack.close)
        self.home = self.fixture.home
        self.runtime = self.home / "runtime"
        self.pilot = self.runtime / prep.PILOT_ID
        self.write_pilot_configuration()
        self.write_canary_sources()
        self.write_gate()
        snapshot = self.pilot / "tokenizers" / self.fixture.snapshot.name
        shutil.copytree(self.fixture.snapshot, snapshot)
        self.test_input = self.home / "output_test"
        self.test_input.mkdir()
        (self.test_input / "INPUT_MANIFEST_TEST_7_4.json").write_text("{}")
        pins = dict(prep.PINS, test_input_manifest_sha256=sha256_file(
            self.test_input / "INPUT_MANIFEST_TEST_7_4.json"))
        for name, value in (("PINS", pins), ("TOKENIZER_REVISION", self.fixture.snapshot.name),
                            ("FROZEN_GATE_FILE_SHA256", sha256_file(self.frozen_path)),
                            ("FROZEN_GATE_CANONICAL_SHA256", digest(self.frozen)),
                            ("table_section6", self.table), ("render_prompts", self.render)):
            self.stack.enter_context(patch.object(prep, name, value))
        self.stack.enter_context(patch.object(materializer, "CANARY_PATH", self.expectations_path))

    def write_pilot_configuration(self):
        from studio2.fase03 import materialize_successor_recovery as recovery
        t = self.fixture
        config = t.config
        config.pop("execution_authorization", None)
        service = config["d9"]["services"]["122B"]
        service.update(model="qwen3.5-122b", identity_sha256=d9.APPROVED_122B_IDENTITY_SHA256,
                       expected_response=dict(prep.QUALIFIED_IDENTITY))
        path = Path(service["documentation"]["path"])
        document = json.loads(path.read_text())
        document["service"] = {k: deepcopy(v) for k, v in service.items() if k != "documentation"}
        document["identity_binding"] = recovery._response_identity_binding()
        path.write_text(json.dumps(document))
        service["documentation"] = {"path": str(path), "sha256": sha256_file(path)}
        config["expected_response"] = dict(prep.QUALIFIED_IDENTITY)
        config["candidate"]["requested_model"] = "qwen3.5-122b"
        t.approve_config()
        self.pilot_config = deepcopy(t.config)
        target = self.pilot / prep.PILOT_CONFIG
        target.parent.mkdir(parents=True)
        target.write_text(json.dumps(self.pilot_config))

    def write_canary_sources(self):
        rows = [{"prompt_id": f"S2-P03-{index:03d}", "text": f"FIXTURE ONLY prompt {index} è",
                 "agent_id": f"agent_{index % 8 + 1}", "case_id": f"case-{index}",
                 "condition": ("A", "B-LF", "E-LF")[index % 3]} for index in range(1, 13)]
        self.prompt_lines = [json.dumps(row, ensure_ascii=bool(index % 2)).encode() + b"\n"
                             for index, row in enumerate(rows)]
        self.pilot_prompts = self.pilot / "prepared/pilot_prompts.jsonl"
        self.pilot_prompts.parent.mkdir(parents=True)
        self.pilot_prompts.write_bytes(b"".join(self.prompt_lines))
        self.canary_rows = rows[1:11]
        expectations = [{"prompt_id": row["prompt_id"], "condition": row["condition"],
                         "agent_id": row["agent_id"], "prompt_sha256": sha256_text(row["text"]),
                         "abstain": False, "predicted_label": "Normal",
                         "raw_response_sha256": "0" * 64} for row in self.canary_rows]
        self.expectations_path = self.home / "CANARY_ATTESI_7_4.json"
        self.expectations_path.write_text(json.dumps({"expectations": expectations}))
        self.expectations = expectations

    def table(self):
        return {row["prompt_id"]: {k: v for k, v in row.items() if k != "prompt_id"}
                for row in self.expectations}

    def write_gate(self):
        self.frozen = {"status": "FROZEN_FOR_STABILITY_GATE", "generation": dict(prep.GATE_GENERATION),
                       "candidate": self.pilot_config["candidate"],
                       "config_sha256": digest(self.pilot_config),
                       "prompt_file_sha256": sha256_file(self.pilot_prompts)}
        self.frozen_path = self.pilot / "results/frozen_gate_config.json"
        self.frozen_path.parent.mkdir(parents=True)
        self.frozen_path.write_text(json.dumps(self.frozen))

    def render(self, arguments, out_dir):
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "final_prompts.jsonl").write_text("".join(
            json.dumps({"prompt_id": str(index)}) + "\n" for index in range(2244)))
        return {"prompts_sha256": prep.PINS["prompt_map_sha256"], "unique_total": 2244}

    def call(self, *extra):
        sink = io.StringIO()
        with redirect_stdout(sink):
            status = prep.main(["--runtime-root", str(self.runtime), "--test-input",
                                str(self.test_input), "--target-id", TARGET_ID, *extra])
        return status, json.loads(sink.getvalue())

    def execute(self, sha):
        return self.call("--execute", "--acknowledge", prep.ACK, "--author", "FIXTURE ONLY",
                         "--accept-configuration-sha256", sha)

    def test_plan_writes_nothing_and_names_the_configuration(self):
        status, value = self.call()
        self.assertEqual((status, value["status"]), (0, "PLAN_ONLY"), value)
        self.assertFalse((self.runtime / (TARGET_ID + ".config")).exists())
        self.assertFalse((self.runtime / "prepared-7-4").exists())
        self.assertRegex(value["configuration_sha256_to_accept"], "^[0-9a-f]{64}$")
        self.assertNotIn("offline.invalid", json.dumps(value))

    def test_execute_requires_the_exact_acceptance_then_prepares_and_rehearses(self):
        _, plan = self.call()
        status, refused = self.execute("0" * 64)
        self.assertEqual((status, refused["status"]), (2, "FAIL"))
        self.assertFalse((self.runtime / (TARGET_ID + ".config")).exists())
        status, value = self.execute(plan["configuration_sha256_to_accept"])
        self.assertEqual((status, value["status"]), (0, "PREPARED"), value)
        config = json.loads(Path(value["outputs"]["execution.private.json"]).read_text())
        self.assertEqual(config["d9"]["final_target"]["target_id"], TARGET_ID)
        self.assertFalse(set(d9.PILOT_HISTORY_KEYS) & set(config["d9"]))
        self.assertEqual(config["pilot_ledger"]["pilot_id"], TARGET_ID)
        self.assertEqual(config["call_budget"]["hard_stop_provider_requests"], 7432)
        self.assertEqual(config["candidate"], self.pilot_config["candidate"])
        self.assertEqual(json.loads(Path(value["outputs"]["generation.json"]).read_text()),
                         prep.GATE_GENERATION)
        self.assertEqual(Path(value["outputs"]["canary_prompts.jsonl"]).read_bytes(),
                         b"".join(self.prompt_lines[1:11]))
        rehearsal = next(row for row in value["checks"] if row["check"].startswith("rehearsal"))
        self.assertEqual(rehearsal["detail"]["canary_slots_bound"], 300)
        self.assertFalse((self.runtime / TARGET_ID).exists())
        again_status, again = self.execute(plan["configuration_sha256_to_accept"])
        self.assertEqual((again_status, again["files_sha256"]), (0, value["files_sha256"]))

    def test_a_changed_canary_prompt_is_refused(self):
        row = dict(self.canary_rows[0], text="changed")
        self.pilot_prompts.write_bytes(json.dumps(row).encode() + b"\n" + b"".join(self.prompt_lines[2:]))
        with patch.dict(self.frozen, prompt_file_sha256=sha256_file(self.pilot_prompts)):
            self.frozen_path.write_text(json.dumps(self.frozen))
            with patch.object(prep, "FROZEN_GATE_FILE_SHA256", sha256_file(self.frozen_path)), \
                    patch.object(prep, "FROZEN_GATE_CANONICAL_SHA256", digest(self.frozen)):
                status, value = self.call()
        self.assertEqual(status, 2)
        self.assertIn("differs from the frozen table", value["error"])

    def test_a_generation_contract_other_than_the_gate_is_refused(self):
        with patch.object(prep, "GATE_GENERATION", dict(prep.GATE_GENERATION, seed=1)):
            status, value = self.call()
        self.assertEqual(status, 2)
        self.assertIn("field by field", value["error"])


if __name__ == "__main__":
    unittest.main()
