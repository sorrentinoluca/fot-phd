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
HARNESS_PATH = V2 / "EXP3_V2_HARNESS_FREEZE_MANIFEST_004.json"
REVISION_002_MANIFEST_PATH = V2 / "EXP3_V2_HARNESS_FREEZE_MANIFEST_002.json"
REVISION_003_MANIFEST_PATH = V2 / "EXP3_V2_HARNESS_FREEZE_MANIFEST_003.json"
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
        self.assertFalse(all_v2 & {987654321, 987654322, 123456789})

    def test_sentinel_identity_is_separate_and_collision_free(self) -> None:
        descriptor = json.loads((V2 / "exp3v2_sentinel_case.json").read_text())
        self.assertEqual(verify.validate_sentinel_descriptor(descriptor, self.plan), [])
        self.assertEqual(descriptor["status"], "SENTINEL_VALIDATION_ONLY")
        self.assertEqual(descriptor["physical_case_id"], "EXP3V2-SENTINEL-002")
        self.assertEqual(descriptor["seed"], 987654322)
        self.assertFalse(descriptor["replacement_allowed"])
        self.assertEqual(
            descriptor["consumed_sentinels"][0]["physical_case_id"],
            "EXP3V2-SENTINEL-001",
        )
        self.assertFalse(descriptor["consumed_sentinels"][0]["eligible_for_reuse"])

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

    def test_workspace_isolation_uses_tested_text_scalar_contract(self) -> None:
        helper = (V2 / "exp3v2_workspace_outputs_present.m").read_text()
        regression = (V2 / "test_exp3v2_workspace_isolation.m").read_text()
        self.assertIn("exp3v2_workspace_outputs_present()", self.engine)
        self.assertIn("expression = \"exist('tout','var') || \" +", helper)
        self.assertIn("isstring(expression) && isscalar(expression)", helper)
        self.assertNotIn("[\"exist('tout','var') || \"", self.engine + helper)
        for name in ("tout", "simout", "xmv"):
            self.assertIn(f"assignin('base', '{name}', 1)", regression)
        self.assertIn("RandStream.getGlobalStream()", regression)
        self.assertNotRegex(regression, r"\brng\s*\(")
        self.assertNotRegex(regression, r"\bsim\s*\(")

    def test_model_changes_use_one_guard_and_never_save(self) -> None:
        configure = (V2 / "configure_exp3v2_model.m").read_text()
        restore = (V2 / "restore_exp3v2_model_config.m").read_text()
        self.assertIn("onCleanup(@() restore_exp3v2_model_config(state))", configure)
        self.assertIn("strcmp(originalStopFcn, 'TEplot')", configure)
        self.assertIn("strcmp(originalReturnWorkspaceOutputs, 'off')", configure)
        self.assertIn("'ReturnWorkspaceOutputs', 'on'", configure)
        self.assertIn("state.original_dirty", restore)
        self.assertNotIn("save_system", configure + restore + self.engine)

    def test_file_generation_is_isolated_and_restored(self) -> None:
        configure = (V2 / "configure_exp3v2_file_generation.m").read_text()
        restore = (V2 / "restore_exp3v2_file_generation.m").read_text()
        sentinel = (V2 / "sentinel_integration_run.m").read_text()
        self.assertIn("Simulink.fileGenControl('getConfig')", configure)
        self.assertIn("'CacheFolder', cacheFolder", configure)
        self.assertIn("'CodeGenFolder', codeGenFolder", configure)
        self.assertIn("onCleanup(@() restore_exp3v2_file_generation(state))", configure)
        self.assertIn("Simulink.fileGenControl('setConfig'", restore)
        self.assertIn("restore_exp3v2_file_generation(fileGenState)", sentinel)
        self.assertLess(
            sentinel.index("configure_exp3v2_file_generation"),
            sentinel.index("generate_exp3v2_sentinel"),
        )

    def test_real_and_sentinel_authorization_are_separate(self) -> None:
        real = (V2 / "generate_exp3v2_heldout.m").read_text()
        sentinel = (V2 / "generate_exp3v2_sentinel.m").read_text()
        self.assertIn("FROZEN_BEFORE_GENERATION", real)
        self.assertIn("exp3-v2-heldout-frozen", real)
        self.assertIn("SentinelRejectedByRealWrapper", real)
        self.assertIn("HARNESS_FROZEN_FOR_SENTINEL", sentinel)
        self.assertIn("exp3-v2-harness-frozen-004", sentinel)
        self.assertIn("SentinelRealPathOverlap", sentinel)
        self.assertIn("ExplicitRuntimeRequired", real)
        self.assertIn("ExplicitRuntimeRequired", sentinel)

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
        self.assertEqual(sha256_file(archive), EXPECTED_LOG_HASH)
        if live.exists():
            self.assertEqual(live.read_bytes(), archive.read_bytes())
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

    def test_history_exp1_and_external_inventory_are_intact(self) -> None:
        self.assertEqual(verify.validate_history(), [])
        harness = json.loads(HARNESS_PATH.read_text())
        self.assertEqual(verify.validate_external_dependency_inventory(harness), [])

    def test_aborted_preflight_is_recorded_without_seed_consumption(self) -> None:
        evidence = json.loads(
            (V2 / "EXP3_V2_SENTINEL_PREFLIGHT_ABORT_001.json").read_text()
        )
        self.assertEqual(evidence["status"], "ABORTED_BEFORE_SENTINEL")
        self.assertEqual(evidence["sim_calls"], 0)
        self.assertEqual(evidence["sentinel_executions"], 0)
        self.assertFalse(evidence["seed_consumed"])
        self.assertEqual(evidence["workbooks_created"], 0)
        self.assertFalse(evidence["retry_performed"])
        self.assertFalse(evidence["real_path_interference"])

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
            "`exp3-v2-harness-frozen-002`",
            "`exp3-v2-harness-frozen-003`",
            "`exp3-v2-harness-frozen-004`",
            "`exp3-v2-heldout-frozen`",
        ):
            self.assertIn(token, self.protocol)
        self.assertNotIn("preregistered", self.protocol.lower())

    def test_revision_002_manifest_is_immutable(self) -> None:
        expected = "c552a6f474491243f549f9588eec52d61fe65922ef8734ff843ef75745710019"
        self.assertEqual(sha256_file(REVISION_002_MANIFEST_PATH), expected)
        self.assertEqual(
            git_show(
                "exp3-v2-harness-frozen-002",
                "phase_b/exp3_v2/EXP3_V2_HARNESS_FREEZE_MANIFEST_002.json",
            ),
            REVISION_002_MANIFEST_PATH.read_bytes(),
        )

    def test_revision_003_manifest_is_immutable(self) -> None:
        expected = "e9db49a5a71a4ffbb83213f81224e54569d85c841a31ca492c29a0fb32a62e03"
        self.assertEqual(sha256_file(REVISION_003_MANIFEST_PATH), expected)
        self.assertEqual(
            git_show(
                "exp3-v2-harness-frozen-003",
                "phase_b/exp3_v2/EXP3_V2_HARNESS_FREEZE_MANIFEST_003.json",
            ),
            REVISION_003_MANIFEST_PATH.read_bytes(),
        )

    def test_revision_004_frozen_hashes_and_prefreeze_verifier(self) -> None:
        errors = verify.prefreeze_checks(PLAN_PATH, HARNESS_PATH, FINAL_PATH)
        self.assertEqual(errors, [])
        harness = json.loads(HARNESS_PATH.read_text())
        self.assertEqual(harness["status"], "HARNESS_FROZEN_FOR_SENTINEL")
        self.assertEqual(harness["manifest_revision"], "004")
        self.assertEqual(harness["freeze_tag"], "exp3-v2-harness-frozen-004")
        self.assertTrue(harness["tag_created"])
        self.assertEqual(
            harness["human_approval"],
            "Prepare EXP3_V2 Harness Revision 004 in draft form only",
        )
        self.assertEqual(
            harness["freeze_human_approval"],
            "APPROVO IL FREEZE HARNESS EXP3_V2 REVISION 004",
        )
        self.assertEqual(harness["freeze_human_approval_date"], "2026-09-03")
        self.assertEqual(
            harness["parent_revision_003"],
            {
                "commit": "bce8f0e2f24db7033b7ddbecc38e1bfaa74c85a6",
                "tag": "exp3-v2-harness-frozen-003",
                "manifest_sha256": (
                    "e9db49a5a71a4ffbb83213f81224e54569d85c841a31ca492c29a0fb32a62e03"
                ),
            },
        )
        self.assertEqual(
            harness["active_sentinel"]["physical_case_id"],
            "EXP3V2-SENTINEL-002",
        )
        self.assertEqual(harness["active_sentinel"]["seed"], 987654322)
        self.assertFalse(harness["active_sentinel"]["seed_consumed"])
        self.assertEqual(harness["consumed_sentinels"][0]["seed"], 987654321)
        self.assertFalse(harness["consumed_sentinels"][0]["eligible_for_reuse"])
        self.assertEqual(harness["rng_seed_calls_at_revision_preparation"], 0)
        self.assertEqual(harness["sim_calls_at_revision_preparation"], 0)
        self.assertEqual(harness["workbooks_created_at_revision_preparation"], 0)
        self.assertEqual(
            {row["path"] for row in harness["artifacts"]},
            verify.REQUIRED_HARNESS_PATHS,
        )
        forbidden = {
            "tep_exp3_heldout/exp3_attempt_log.json",
            *{
                f"tep_parent_a0413e16/simulator/{name}"
                for name in verify.EXPECTED_EXTERNAL_DEPENDENCIES
            },
        }
        self.assertTrue(forbidden.isdisjoint(verify.REQUIRED_HARNESS_PATHS))
        self.assertEqual(
            {row["path"] for row in harness["external_runtime_dependencies"]},
            set(verify.EXPECTED_EXTERNAL_DEPENDENCIES),
        )
        self.assertEqual(len(harness["external_runtime_dependencies"]), 8)
        self.assertNotIn(
            "MultiLoop_mode1.slxc",
            {row["path"] for row in harness["external_runtime_dependencies"]},
        )

    def test_preexecution_incident_chain_is_distinct_and_archived(self) -> None:
        record = json.loads(
            (V2 / "EXP3_V2_REV003_PREEXECUTION_INCIDENTS.json").read_text()
        )
        self.assertEqual([row["ordinal"] for row in record["events"]], [1, 2, 3])
        self.assertTrue(
            all(
                row["classification"] == "PRE_EXECUTION_TECHNICAL_ABORT"
                and row["rng_calls"] == 0
                and row["sim_calls"] == 0
                and not row["sentinel_simulation_completed"]
                for row in record["events"]
            )
        )
        self.assertEqual(record["unavailable_evidence"], [])
        archives = {
            "EXP3_V2_REV002_EXTERNAL_DRIVER_FAILURE_ARCHIVE.json": (
                "b074f871556ddfc229cfc842e71a8d7884ad19c7206d48c3f06ebee3f4bef6ff"
            ),
            "EXP3_V2_REV002_EXTERNAL_DRIVER_ATTEMPT_LOG_ARCHIVE.json": (
                "6b392bfef158585e2127721a676773b4419aff2d655edae159318908fdffd1bd"
            ),
            "EXP3_V2_REV002_OFFICIAL_WRAPPER_FAILURE_ARCHIVE.json": (
                "aaf58e8626fb300e740801dbd509b4cbf0b662bcd2a45b13fef09e89266dba25"
            ),
            "EXP3_V2_REV002_OFFICIAL_WRAPPER_ATTEMPT_LOG_ARCHIVE.json": (
                "d10d281781a920439479f1b052649fd6bb8f16c2ecc076306bb5f910c1be4260"
            ),
        }
        for name, digest in archives.items():
            self.assertEqual(sha256_file(V2 / name), digest)

    def test_revision_003_sentinel_failure_is_permanent_and_consumed(self) -> None:
        record = json.loads((V2 / "EXP3_V2_REV003_SENTINEL_FAILURE.json").read_text())
        sentinel = record["sentinel"]
        self.assertEqual(sentinel["physical_case_id"], "EXP3V2-SENTINEL-001")
        self.assertEqual(sentinel["seed"], 987654321)
        self.assertTrue(sentinel["seed_consumed"])
        self.assertEqual(sentinel["rng_calls"], 1)
        self.assertEqual(sentinel["sim_calls"], 1)
        self.assertFalse(sentinel["retry_performed"])
        workbook = record["throwaway_workbook"]
        self.assertEqual((workbook["rows"], workbook["cols"]), (3001, 54))
        self.assertEqual(workbook["size_bytes"], 1704651)
        self.assertEqual(
            workbook["sha256"],
            "a1980855174e9db82416f576e84aa720eddd758b5686b9ecfc376aeedfa282a9",
        )
        self.assertFalse(workbook["committed"])
        self.assertEqual(record["scientific_seeds_consumed"], 0)
        self.assertEqual(record["real_exp3v2_workbooks_created"], 0)
        archives = {
            "EXP3_V2_REV003_SENTINEL_FAILURE_ARCHIVE.json": (
                "04fae56a1b10cddf4e27c0a43367fbd4eb80b6591d7c813edeb9ce55f8e5e57c"
            ),
            "EXP3_V2_REV003_SENTINEL_ATTEMPT_LOG_ARCHIVE.json": (
                "2ef6166cf783b9a915f3f569528b1a9f9a335f200655edd8e169fe5eb69a5f40"
            ),
            "EXP3_V2_REV003_SENTINEL_MANIFEST_ARCHIVE.csv": (
                "ca51663b9d721c5b109b7bfbe8a815b8e814f77cd2911c3f1587be998e6783b1"
            ),
        }
        for name, digest in archives.items():
            self.assertEqual(sha256_file(V2 / name), digest)

    def test_python_preflight_precedes_engine_and_uses_pinned_executable(self) -> None:
        wrapper = (V2 / "sentinel_integration_run.m").read_text()
        preflight = (V2 / "validate_exp3v2_python_runtime.m").read_text()
        regression = (V2 / "test_exp3v2_python_runtime_preflight.m").read_text()
        self.assertLess(
            wrapper.index("validate_exp3v2_python_runtime"),
            wrapper.index("generate_exp3v2_sentinel"),
        )
        self.assertNotIn('python3 "', wrapper)
        self.assertGreaterEqual(wrapper.count("pythonRuntime.executable_path"), 2)
        self.assertIn("importlib.metadata", preflight)
        self.assertNotIn("__version__", preflight)
        for token in (
            "3.13.9",
            "4.25.0",
            "3.1.5",
            "PythonExecutableNotRegular",
            "PythonExecutableNotExecutable",
            "PythonRuntimeProbeFailed",
        ):
            self.assertIn(token, preflight + regression)
        self.assertNotRegex(preflight + regression, r"\brng\s*\(")
        self.assertNotRegex(preflight + regression, r"\bsim\s*\(")

    def test_round_trip_sampling_manifest_passes_verifier_contract(self) -> None:
        formatter = (V2 / "format_exp3v2_csv_scalar.m").read_text()
        self.assertIn("sprintf('%.17g', double(input))", formatter)
        row = {
            "physical_case_id": "EXP3V2-SENTINEL-002",
            "attempt": "0",
            "seed": "987654322",
            "filename": "EXP3V2-SENTINEL-002__attempt-0.xlsx",
            "sampling": "0.016666666666666666",
        }
        self.assertEqual(verify.validate_sentinel_manifest_row(row), [])
        truncated = dict(row, sampling="0.016667")
        self.assertIn(
            "sentinel manifest sampling mismatch",
            verify.validate_sentinel_manifest_row(truncated),
        )
        self.assertEqual(float(row["sampling"]), 1 / 60)

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
