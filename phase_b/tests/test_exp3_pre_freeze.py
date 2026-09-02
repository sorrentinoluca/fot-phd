from __future__ import annotations

import copy
import csv
import hashlib
import importlib.util
import json
import re
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXP3 = ROOT / "phase_b/exp3"
PLAN_PATH = EXP3 / "exp3_case_plan.json"
GENERATOR_PATH = EXP3 / "generate_exp3_heldout.m"
SCHEMA_PATH = EXP3 / "exp3_attempt_log.schema.json"
ATTEMPT_TEMPLATE_PATH = EXP3 / "exp3_attempt_log.template.json"
MANIFEST_TEMPLATE_PATH = EXP3 / "exp3_manifest_template.csv"
PROTOCOL_PATH = EXP3 / "EXP3_FRESH_RUN_PROTOCOL.md"
RNG_EVIDENCE_PATH = EXP3 / "RNG_RUNTIME_VALIDATION.md"
RNG_PROBE_PATH = EXP3 / "validate_exp3_rng_runtime.m"
FREEZE_MANIFEST_PATH = EXP3 / "EXP3_FREEZE_MANIFEST.json"

spec = importlib.util.spec_from_file_location(
    "verify_exp3_heldout", EXP3 / "verify_exp3_heldout.py"
)
assert spec and spec.loader
verify = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verify)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Exp3PreFreezeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.plan = json.loads(PLAN_PATH.read_text(encoding="utf-8"))
        cls.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        cls.protocol = PROTOCOL_PATH.read_text(encoding="utf-8")
        cls.generator = GENERATOR_PATH.read_text(encoding="utf-8")

    def make_attempt(self, case: dict, attempt: int, structural_valid: bool) -> dict:
        seed = case["primary_seed"] if attempt == 0 else case["replacement_seed"]
        output_name = f"{case['physical_case_id']}__attempt-{attempt}.xlsx"
        row = {
            "physical_case_id": case["physical_case_id"],
            "fault_status": case["condition"],
            "attempt": attempt,
            "seed": seed,
            "rng_algorithm": "twister",
            "started_at": "2026-09-02T10:00:00.000Z",
            "completed_at": "2026-09-02T10:01:00.000Z",
            **verify.EXPECTED_RUNTIME,
            **verify.EXPECTED_SIMULATOR,
            "case_plan_hash": sha256_file(PLAN_PATH),
            "generation_script_hash": sha256_file(GENERATOR_PATH),
            "output_path": str(ROOT / "tep_exp3_heldout/mode1" / output_name),
            "output_size_bytes": 100 if structural_valid else 0,
            "output_sha256": "a" * 64 if structural_valid else "",
            "rows": 3001 if structural_valid else None,
            "cols": 54 if structural_valid else None,
            "time_start": 0.0 if structural_valid else None,
            "time_end": 50.0 if structural_valid else None,
            "sampling_interval": 1 / 60 if structural_valid else None,
            "finite_check": True if structural_valid else None,
            "structural_valid": structural_valid,
            "technical_failure_reason": "" if structural_valid else "XLSX missing",
        }
        return row

    def validate_attempts(self, attempts: list[dict]) -> list[str]:
        payload = {
            "schema_version": "1.0",
            "experiment": "Experiment 3 — Fresh Prospective Physical-Run Extension",
            "attempts": attempts,
        }
        return verify.validate_attempt_log(
            payload, self.plan, GENERATOR_PATH, PLAN_PATH, self.schema
        )

    def test_case_plan_is_exactly_canonical_and_deterministic(self) -> None:
        self.assertEqual(verify.validate_case_plan(self.plan), [])
        self.assertEqual(self.plan["status"], "FROZEN_BEFORE_GENERATION")
        self.assertEqual(self.plan["cases"], verify.canonical_cases())
        self.assertEqual(len(self.plan["cases"]), 30)
        self.assertEqual(
            Counter(row["condition"] for row in self.plan["cases"]),
            Counter({"Normal": 6, "F1": 6, "F8": 6, "F10": 6, "F13": 6}),
        )

    def test_case_ids_and_seed_namespaces_are_unique(self) -> None:
        cases = self.plan["cases"]
        ids = [row["physical_case_id"] for row in cases]
        primary = [row["primary_seed"] for row in cases]
        replacement = [row["replacement_seed"] for row in cases]
        self.assertEqual(len(set(ids)), 30)
        self.assertEqual(primary, list(range(310001, 310031)))
        self.assertEqual(len(set(replacement)), 30)
        self.assertFalse(set(primary) & set(replacement))
        self.assertTrue(all(r == p + 1_000_000 for p, r in zip(primary, replacement)))

    def test_attempt_policy_is_only_zero_then_optional_one(self) -> None:
        self.assertEqual(self.plan["rng"]["allowed_attempts"], [0, 1])
        self.assertEqual(self.plan["rng"]["max_total_attempts"], 2)
        attempt_schema = self.schema["$defs"]["attempt"]["properties"]["attempt"]
        self.assertEqual(attempt_schema["minimum"], 0)
        self.assertEqual(attempt_schema["maximum"], 1)

    def test_attempt_schema_has_only_technical_provenance(self) -> None:
        required = set(self.schema["$defs"]["attempt"]["required"])
        self.assertTrue(verify.ATTEMPT_REQUIRED_FIELDS.issubset(required))
        forbidden = {
            "prediction",
            "diagnosis",
            "accuracy",
            "verbalizer_assessment",
            "fault_strength_assessment",
        }
        self.assertTrue(required.isdisjoint(forbidden))

    def test_replacement_requires_failed_attempt_zero(self) -> None:
        case = self.plan["cases"][0]
        replacement = self.make_attempt(case, 1, True)
        errors = self.validate_attempts([replacement])
        self.assertTrue(any("no earlier attempt 0" in error for error in errors))

        primary_valid = self.make_attempt(case, 0, True)
        errors = self.validate_attempts([primary_valid, replacement])
        self.assertTrue(any("follows a valid attempt 0" in error for error in errors))

        primary_failed = self.make_attempt(case, 0, False)
        self.assertEqual(self.validate_attempts([primary_failed, replacement]), [])

    def test_attempt_two_is_rejected_fail_closed(self) -> None:
        row = self.make_attempt(self.plan["cases"][0], 1, True)
        row["attempt"] = 2
        errors = self.validate_attempts([row])
        self.assertTrue(errors)
        self.assertTrue(any("attempt" in error for error in errors))

    def test_seed_or_provenance_deviation_is_rejected(self) -> None:
        row = self.make_attempt(self.plan["cases"][0], 0, True)
        row["seed"] += 1
        row["matlab_build"] = "wrong"
        errors = self.validate_attempts([row])
        self.assertTrue(any("seed mismatch" in error for error in errors))
        self.assertTrue(any("matlab_build" in error for error in errors))

    def test_structural_values_are_enforced_on_valid_attempts(self) -> None:
        row = self.make_attempt(self.plan["cases"][0], 0, True)
        row["sampling_interval"] = 0.5
        errors = self.validate_attempts([row])
        self.assertTrue(any("sampling mismatch" in error for error in errors))

    def test_empty_attempt_and_manifest_templates_are_exact(self) -> None:
        errors = verify.prefreeze_checks(
            PLAN_PATH,
            MANIFEST_TEMPLATE_PATH,
            ATTEMPT_TEMPLATE_PATH,
            SCHEMA_PATH,
            FREEZE_MANIFEST_PATH,
        )
        self.assertEqual(errors, [])
        attempt_template = json.loads(ATTEMPT_TEMPLATE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(attempt_template["attempts"], [])
        with MANIFEST_TEMPLATE_PATH.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 30)
        self.assertTrue(all(row["attempt"] == "TBD" for row in rows))

    def test_mutated_case_plan_is_rejected_fail_closed(self) -> None:
        altered = copy.deepcopy(self.plan)
        altered["cases"][0]["replacement_seed"] += 1
        errors = verify.validate_case_plan(altered)
        self.assertTrue(errors)

    def test_generation_rng_and_sim_are_adjacent(self) -> None:
        pattern = re.compile(
            r"rng\(seed, 'twister'\);\s*\n\s*simResult = sim\(modelName\);"
        )
        self.assertEqual(len(pattern.findall(self.generator)), 1)
        self.assertNotIn(
            "rand()",
            self.generator.split("rng(seed, 'twister');", 1)[1].split(
                "simResult = sim(modelName);", 1
            )[0],
        )

    def test_generation_requires_frozen_plan_and_hash_manifest(self) -> None:
        self.assertIn("FROZEN_BEFORE_GENERATION", self.generator)
        self.assertIn("EXP3_FREEZE_MANIFEST.json", self.generator)
        self.assertIn("GenerationScriptNotFrozen", self.generator)
        self.assertIn("CasePlanNotFrozen", self.generator)

    def test_generator_contains_no_scientific_selection_pipeline(self) -> None:
        lowered = self.generator.lower()
        forbidden = (
            "tep_verbalize",
            "openai",
            "accuracy",
            "classification",
            "fault strength threshold",
        )
        for token in forbidden:
            self.assertNotIn(token, lowered)

    def test_protocol_code_and_config_agree(self) -> None:
        required = (
            "`phase_b/exp3/exp3_case_plan.json`",
            "`phase_b/exp3/generate_exp3_heldout.m`",
            "`phase_b/exp3/verify_exp3_heldout.py`",
            "There is no attempt `2`.",
            "maximum is two total attempts",
            "**310031**",
            "paired cluster bootstrap",
            "**B−A is the primary replication contrast.**",
            "**B−E is the supporting semantic-specificity contrast.**",
            "secondary descriptive analysis",
            "**Status:** `FROZEN BEFORE GENERATION`",
            "`phase_b/exp3/EXP3_FREEZE_MANIFEST.json`",
        )
        for text in required:
            self.assertIn(text, self.protocol)
        self.assertNotIn("-R01", self.protocol)
        self.assertNotIn("-R02", self.protocol)
        self.assertNotIn("three attempts total", self.protocol)

    def test_freeze_manifest_hashes_all_exp3_boundary_artifacts(self) -> None:
        self.assertEqual(verify.validate_freeze_manifest(FREEZE_MANIFEST_PATH), [])

    def test_exp3_python_dependencies_are_pinned(self) -> None:
        requirements = (ROOT / "requirements.txt").read_text(encoding="utf-8")
        self.assertIn("jsonschema==4.25.0", requirements.splitlines())
        self.assertIn("openpyxl==3.1.5", requirements.splitlines())

    def test_runtime_rng_evidence_is_exact_and_sentinel_only(self) -> None:
        evidence = RNG_EVIDENCE_PATH.read_text(encoding="utf-8")
        for value in (
            "25.2.0.3312555 (R2025b) Update 6",
            "3312555",
            "25.2",
            "28-Jul-2025",
            "MACA64",
            "/Applications/MATLAB_R2025b.app",
            "ce64df11668eafc5e1ab7516ff9667614b0517f6ccd4df57eab94fb07b507c42",
            "60e5f58c53458d9cc99d653391a459f41230e70fb2669e5c47eb0c86512950d9",
        ):
            self.assertIn(value, evidence)
        probe = RNG_PROBE_PATH.read_text(encoding="utf-8")
        self.assertIn("sameSeed = 987654321;", probe)
        self.assertIn("differentSeed = 123456789;", probe)
        self.assertNotIn("310001;", probe)

    def test_exp3_raw_output_is_ignored_and_not_generated(self) -> None:
        gitignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("tep_exp3_heldout/", gitignore.splitlines())
        generated = ROOT / "tep_exp3_heldout"
        self.assertFalse(generated.exists())
        self.assertEqual(list(EXP3.glob("*.xlsx")), [])

    def test_all_experiment_one_frozen_hashes_remain_exact(self) -> None:
        manifest = json.loads(
            (ROOT / "phase_b/PHASE_B_PROTOCOL_HASHES.json").read_text(encoding="utf-8")
        )
        self.assertGreaterEqual(len(manifest["artifacts"]), 50)
        for relative, expected in manifest["artifacts"].items():
            self.assertEqual(sha256_file(ROOT / relative), expected, relative)


if __name__ == "__main__":
    unittest.main()
