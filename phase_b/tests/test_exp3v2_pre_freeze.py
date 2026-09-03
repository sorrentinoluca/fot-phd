from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXP3 = ROOT / "phase_b/exp3"
V2 = ROOT / "phase_b/exp3_v2"
PLAN_PATH = V2 / "exp3v2_case_plan.json"
SCHEMA_PATH = V2 / "exp3v2_attempt_log.schema.json"
HARNESS_PATH = V2 / "EXP3_V2_HARNESS_FREEZE_MANIFEST.json"
FINAL_PATH = V2 / "EXP3_V2_FREEZE_MANIFEST.json"
VERIFIER_PATH = V2 / "verify_exp3v2_heldout.py"
EXPECTED_LOG_HASH = "04ea7d8af227c3a7f947b4dde434e77510c163ce9c108892ffa22f491f022904"

spec = importlib.util.spec_from_file_location("verify_exp3v2", VERIFIER_PATH)
assert spec and spec.loader
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_show(revision: str, relative: str) -> bytes:
    return subprocess.run(
        ["git", "show", f"{revision}:{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout


class Exp3V2PreFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = json.loads(PLAN_PATH.read_text())
        cls.schema = json.loads(SCHEMA_PATH.read_text())
        cls.protocol = (V2 / "EXP3_V2_FRESH_RUN_PROTOCOL.md").read_text()
        cls.engine = (V2 / "run_exp3v2_engine.m").read_text()
        cls.extractor = (V2 / "extract_exp3v2_outputs.m").read_text()

    def make_attempt(self, case: dict, attempt: int, structural_valid: bool) -> dict:
        expected_simulator = {
            "simulator_commit": verify.EXPECTED_SIMULATOR["simulator_commit"],
            "model_name": verify.EXPECTED_SIMULATOR["model"],
            "simulation_mode": verify.EXPECTED_SIMULATOR["simulation_mode"],
            "solver": verify.EXPECTED_SIMULATOR["solver"],
            "sfunction_identity": verify.EXPECTED_SIMULATOR["sfunction_identity"],
            "sfunction_hash": verify.EXPECTED_SIMULATOR["sfunction_source_sha256"],
            "sfunction_mex_hash": verify.EXPECTED_SIMULATOR[
                "sfunction_macos_mex_sha256"
            ],
            "model_hash": verify.EXPECTED_SIMULATOR["model_sha256"],
            "initial_state_hash": verify.EXPECTED_SIMULATOR["initial_state_sha256"],
        }
        seed = case["primary_seed"] if attempt == 0 else case["replacement_seed"]
        return {
            "physical_case_id": case["physical_case_id"],
            "fault_status": case["condition"],
            "attempt": attempt,
            "seed": seed,
            "rng_algorithm": "twister",
            "started_at": "2026-09-03T10:00:00.000Z",
            "completed_at": "2026-09-03T10:01:00.000Z",
            **verify.EXPECTED_RUNTIME,
            **expected_simulator,
            "case_plan_hash": sha256_file(PLAN_PATH),
            "generation_script_hash": sha256_file(V2 / "run_exp3v2_engine.m"),
            "output_path": str(
                ROOT
                / "tep_exp3_v2_heldout/mode1"
                / f"{case['physical_case_id']}__attempt-{attempt}.xlsx"
            ),
            "output_size_bytes": 100 if structural_valid else 0,
            "output_sha256": "a" * 64 if structural_valid else "",
            "rows": 3001 if structural_valid else None,
            "cols": 54 if structural_valid else None,
            "time_start": 0.0 if structural_valid else None,
            "time_end": 50.0 if structural_valid else None,
            "sampling_interval": 1 / 60 if structural_valid else None,
            "finite_check": True if structural_valid else False,
            "structural_valid": structural_valid,
            "technical_failure_reason": "" if structural_valid else "technical",
        }

    def validate_attempts(self, rows: list[dict]) -> list[str]:
        payload = {
            "schema_version": "1.0",
            "experiment": "Experiment 3 V2 — Prospective Fresh-Run Held-Out",
            "attempts": rows,
        }
        return verify.validate_attempt_log(payload, self.plan, self.schema)

    def test_case_plan_is_exactly_canonical_and_still_draft(self) -> None:
        self.assertEqual(verify.validate_case_plan(self.plan), [])
        self.assertEqual(self.plan["status"], "PRE_FREEZE_DRAFT")
        self.assertEqual(self.plan["cases"], verify.canonical_cases())
        self.assertEqual(
            Counter(row["condition"] for row in self.plan["cases"]),
            Counter({"Normal": 6, "F1": 6, "F8": 6, "F10": 6, "F13": 6}),
        )

    def test_fresh_seed_namespaces_are_exact_and_disjoint(self) -> None:
        primary = [row["primary_seed"] for row in self.plan["cases"]]
        replacement = [row["replacement_seed"] for row in self.plan["cases"]]
        self.assertEqual(primary, list(range(320001, 320031)))
        self.assertEqual(replacement, list(range(1320001, 1320031)))
        all_v2 = set(primary) | set(replacement) | {320031}
        old = set(range(310001, 310031)) | set(range(1310001, 1310031))
        self.assertFalse(all_v2 & old)
        self.assertFalse(all_v2 & {987654321, 123456789})

    def test_sentinel_identity_is_separate_and_collision_free(self) -> None:
        descriptor = json.loads((V2 / "exp3v2_sentinel_case.json").read_text())
        self.assertEqual(verify.validate_sentinel_descriptor(descriptor, self.plan), [])
        self.assertEqual(descriptor["status"], "SENTINEL_VALIDATION_ONLY")
        self.assertFalse(descriptor["replacement_allowed"])

    def test_attempt_schema_and_policy_are_fail_closed(self) -> None:
        attempt_schema = self.schema["$defs"]["attempt"]
        self.assertEqual(attempt_schema["properties"]["attempt"]["minimum"], 0)
        self.assertEqual(attempt_schema["properties"]["attempt"]["maximum"], 1)
        self.assertEqual(
            attempt_schema["properties"]["physical_case_id"]["pattern"],
            "^EXP3V2-(N|F1|F8|F10|F13)-00[1-6]$",
        )
        forbidden = {
            "prediction",
            "diagnosis",
            "accuracy",
            "verbalizer_assessment",
            "fault_strength_assessment",
        }
        self.assertTrue(set(attempt_schema["required"]).isdisjoint(forbidden))

    def test_replacement_requires_earlier_technical_failure(self) -> None:
        case = self.plan["cases"][0]
        replacement = self.make_attempt(case, 1, True)
        self.assertTrue(
            any(
                "no earlier attempt 0" in error
                for error in self.validate_attempts([replacement])
            )
        )
        valid_primary = self.make_attempt(case, 0, True)
        self.assertTrue(
            any(
                "follows a valid attempt 0" in error
                for error in self.validate_attempts([valid_primary, replacement])
            )
        )
        failed_primary = self.make_attempt(case, 0, False)
        self.assertEqual(self.validate_attempts([failed_primary, replacement]), [])

    def test_attempt_two_and_runtime_mismatches_are_rejected(self) -> None:
        row = self.make_attempt(self.plan["cases"][0], 1, True)
        row["attempt"] = 2
        self.assertTrue(self.validate_attempts([row]))
        for field in (
            "matlab_version_full",
            "matlab_release",
            "matlab_build",
            "matlab_product_date",
            "matlab_runtime_update_date",
        ):
            wrong = self.make_attempt(self.plan["cases"][0], 0, True)
            wrong[field] = "wrong"
            self.assertTrue(
                any(field in error for error in self.validate_attempts([wrong]))
            )

    def test_rng_to_sim_adjacency_and_one_shared_sim_call(self) -> None:
        pattern = re.compile(
            r"rng\(seed, 'twister'\);\s*\n\s*simResult = sim\(modelName\);"
        )
        self.assertEqual(len(pattern.findall(self.engine)), 1)
        self.assertEqual(len(re.findall(r"\bsim\s*\(", self.engine)), 1)
        self.assertNotRegex(
            (V2 / "generate_exp3v2_heldout.m").read_text(), r"\bsim\s*\("
        )
        self.assertNotRegex(
            (V2 / "generate_exp3v2_sentinel.m").read_text(), r"\bsim\s*\("
        )

    def test_incident_five_retrieval_is_typed_and_has_no_fallback(self) -> None:
        required = (
            "isa(simResult, 'Simulink.SimulationOutput')",
            "who(simResult)",
            "simResult.get('tout')",
            "simResult.get('simout')",
            "simResult.get('xmv')",
            "[expectedRows 1]",
            "[expectedRows 41]",
            "[expectedRows 12]",
        )
        for token in required:
            self.assertIn(token, self.extractor)
        self.assertNotIn("evalin", self.extractor)
        self.assertNotIn("simResult.who", self.engine + self.extractor)

    def test_model_changes_use_one_guard_and_never_save(self) -> None:
        configure = (V2 / "configure_exp3v2_model.m").read_text()
        restore = (V2 / "restore_exp3v2_model_config.m").read_text()
        self.assertIn("onCleanup(@() restore_exp3v2_model_config(state))", configure)
        self.assertIn("strcmp(originalStopFcn, 'TEplot')", configure)
        self.assertIn("strcmp(originalReturnWorkspaceOutputs, 'off')", configure)
        self.assertIn("'ReturnWorkspaceOutputs', 'on'", configure)
        self.assertIn("state.original_dirty", restore)
        self.assertNotIn("save_system", configure + restore + self.engine)

    def test_real_and_sentinel_authorization_are_separate(self) -> None:
        real = (V2 / "generate_exp3v2_heldout.m").read_text()
        sentinel = (V2 / "generate_exp3v2_sentinel.m").read_text()
        self.assertIn("FROZEN_BEFORE_GENERATION", real)
        self.assertIn("exp3-v2-heldout-frozen", real)
        self.assertIn("SentinelRejectedByRealWrapper", real)
        self.assertIn("HARNESS_FROZEN_FOR_SENTINEL", sentinel)
        self.assertIn("exp3-v2-harness-frozen", sentinel)
        self.assertIn("SentinelRealPathOverlap", sentinel)

    def test_templates_are_exact_and_attempts_array_is_explicit(self) -> None:
        template_source = (V2 / "exp3v2_attempt_log.template.json").read_text()
        self.assertRegex(template_source, r'"attempts"\s*:\s*\[\s*\]')
        append_source = (V2 / "append_exp3v2_attempt_record.m").read_text()
        self.assertIn('"attempts": [', append_source)
        with (V2 / "exp3v2_manifest_template.csv").open(newline="") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 30)
        self.assertTrue(all(row["attempt"] == "TBD" for row in rows))
        self.assertTrue(
            all(
                row["seed"] == str(case["primary_seed"])
                for row, case in zip(rows, verify.canonical_cases())
            )
        )

    def test_closure_archive_is_verbatim_and_exp3_files_are_immutable(self) -> None:
        live = ROOT / "tep_exp3_heldout/exp3_attempt_log.json"
        archive = EXP3 / "EXP3_CLOSURE_attempt_log_archive.json"
        self.assertEqual(live.read_bytes(), archive.read_bytes())
        self.assertEqual(sha256_file(archive), EXPECTED_LOG_HASH)
        tracked = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "1cad481", "phase_b/exp3"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.splitlines()
        for relative in tracked:
            self.assertEqual(
                (ROOT / relative).read_bytes(), git_show("1cad481", relative)
            )

    def test_history_exp1_and_simulator_are_intact(self) -> None:
        self.assertEqual(verify.validate_history(), [])
        self.assertEqual(verify.validate_simulator_files(), [])

    def test_protocol_preserves_science_and_open_gates(self) -> None:
        for token in (
            "prospective fresh-run replication on the same four fault classes",
            "`PRE_FREEZE_DRAFT`",
            "`320001`–`320030`",
            "`1320001`–`1320030`",
            "bootstrap seed `320031`",
            "paired cluster bootstrap",
            "10,000 bootstrap draws",
            "B−A is the primary replication contrast",
            "B−E is the supporting semantic-specificity contrast",
            "mandatory sentinel gate",
            "`exp3-v2-harness-frozen`",
            "`exp3-v2-heldout-frozen`",
        ):
            self.assertIn(token, self.protocol)
        self.assertNotIn("preregistered", self.protocol.lower())

    def test_frozen_harness_hashes_and_prefreeze_verifier(self) -> None:
        errors = verify.prefreeze_checks(PLAN_PATH, HARNESS_PATH, FINAL_PATH)
        self.assertEqual(errors, [])
        harness = json.loads(HARNESS_PATH.read_text())
        self.assertEqual(harness["status"], "HARNESS_FROZEN_FOR_SENTINEL")
        self.assertEqual(
            harness["reviewed_candidate_commit"],
            "8dff1d67693cc4423c3241d77c5fb6609b176ecd",
        )
        self.assertEqual(harness["human_approval"], "APPROVO IL FREEZE HARNESS EXP3_V2")
        self.assertEqual(
            {row["path"] for row in harness["artifacts"]},
            verify.REQUIRED_HARNESS_PATHS,
        )

    def test_mode_paths_are_mutually_exclusive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [
                    sys.executable,
                    str(VERIFIER_PATH),
                    "--pre-freeze",
                    "--data-dir",
                    directory,
                ],
                cwd=ROOT,
                capture_output=True,
                text=True,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("rejects workbook/log/sentinel paths", result.stderr)

    def test_no_v2_workbook_or_real_attempt_log_exists(self) -> None:
        root = ROOT / "tep_exp3_v2_heldout"
        self.assertEqual(list(root.rglob("*.xlsx")) if root.exists() else [], [])
        self.assertFalse((root / "exp3v2_attempt_log.json").exists())
        self.assertIn(
            "tep_exp3_v2_heldout/", (ROOT / ".gitignore").read_text().splitlines()
        )


if __name__ == "__main__":
    unittest.main()
