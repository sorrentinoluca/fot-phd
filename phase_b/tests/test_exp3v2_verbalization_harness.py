#!/usr/bin/env python3
"""Synthetic-only tests for the EXP3_V2 verbalization harness."""

from __future__ import annotations

import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
HARNESS_DIR = ROOT / "phase_b/exp3_v2"
sys.path.insert(0, str(HARNESS_DIR))
sys.path.insert(0, str(ROOT / "code"))

import run_exp3v2_verbalization as runner  # noqa: E402
import verify_exp3v2_verbalizations as verifier  # noqa: E402
from tep_features import BaselineStats, XMEAS  # noqa: E402


PRODUCTION_MANIFEST = HARNESS_DIR / "EXP3_V2_VERBALIZATION_HARNESS_MANIFEST_001.json"
BASELINE_PATH = HARNESS_DIR / "EXP3_V2_VERBALIZATION_BASELINE_STATS_001.json"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_git(repo: Path, *args: str) -> str:
    environment = {
        **os.environ,
        "GIT_AUTHOR_NAME": "EXP3_V2 synthetic rehearsal",
        "GIT_AUTHOR_EMAIL": "synthetic-rehearsal@example.invalid",
        "GIT_COMMITTER_NAME": "EXP3_V2 synthetic rehearsal",
        "GIT_COMMITTER_EMAIL": "synthetic-rehearsal@example.invalid",
    }
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env=environment,
    )
    return completed.stdout.strip()


def copy_relative(source_root: Path, destination_root: Path, relative: str) -> Path:
    destination = destination_root / relative
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_root / relative, destination)
    return destination


class VerbalizationHarnessTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.temporary = tempfile.TemporaryDirectory(
            prefix="exp3v2-verbalization-synthetic-"
        )
        cls.root = Path(cls.temporary.name)
        cls.data_root = cls.root / "synthetic-data"
        cls.workbook_root = cls.data_root / "tep_exp3_v2_heldout/mode1"
        cls.workbook_root.mkdir(parents=True)
        cls.manifest = json.loads(PRODUCTION_MANIFEST.read_text(encoding="utf-8"))
        cls.manifest["status"] = runner.FROZEN_STATUS
        cls.manifest["tag_created"] = True

        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        means = np.asarray(baseline["mean"], dtype=float)
        standard_deviations = np.asarray(baseline["std"], dtype=float)
        cls.synthetic_baseline = BaselineStats(
            mean=pd.Series(means, index=XMEAS, dtype=float),
            std=pd.Series(standard_deviations, index=XMEAS, dtype=float),
            diff_std=pd.Series(baseline["diff_std"], index=XMEAS, dtype=float),
            residual_std=pd.Series(baseline["residual_std"], index=XMEAS, dtype=float),
        )
        time = np.arange(0.0, 50.5, 0.5, dtype=float)
        rows = []
        concatenated = hashlib.sha256()
        inventory = hashlib.sha256()
        for order, case_id in enumerate(
            cls.manifest["inputs"]["canonical_case_ids"], start=1
        ):
            frame: dict[str, np.ndarray] = {"Time": time}
            for index, variable in enumerate(XMEAS):
                phase = 0.11 * (index + 1) + 0.007 * order
                values = means[index] + standard_deviations[index] * (
                    0.20 * np.sin(0.31 * time + phase)
                    + 0.03 * np.cos(0.07 * time * (index % 5 + 1))
                )
                frame[variable] = values
            filename = f"{case_id}__attempt-0.xlsx"
            path = cls.workbook_root / filename
            pd.DataFrame(frame).to_excel(path, index=False)
            raw = path.read_bytes()
            digest = hashlib.sha256(raw).hexdigest()
            relative = f"tep_exp3_v2_heldout/mode1/{filename}"
            row = {
                "order": order,
                "physical_case_id": case_id,
                "attempt": 0,
                "seed": 320000 + order,
                "path": relative,
                "filename": filename,
                "size_bytes": len(raw),
                "sha256": digest,
            }
            rows.append(row)
            concatenated.update(raw)
            inventory.update(f"{filename},{len(raw)},{digest}\n".encode("utf-8"))

        data_manifest = {
            "status": "FROZEN_BEFORE_VERBALIZATION",
            "data_artifacts": {
                "workbook_inventory": rows,
                "aggregate_digests": {
                    "inventory_sha256": inventory.hexdigest(),
                    "concatenated_workbook_bytes_sha256": concatenated.hexdigest(),
                },
            },
        }
        data_manifest_path = cls.data_root / "phase_b/exp3_v2/SYNTHETIC_DATA.json"
        data_manifest_path.parent.mkdir(parents=True)
        data_manifest_path.write_text(
            json.dumps(data_manifest, indent=2) + "\n", encoding="utf-8"
        )
        cls.manifest["boundaries"]["data"].update(
            {
                "manifest_path": "phase_b/exp3_v2/SYNTHETIC_DATA.json",
                "manifest_size_bytes": data_manifest_path.stat().st_size,
                "manifest_sha256": sha256_file(data_manifest_path),
            }
        )
        cls.manifest["inputs"]["input_inventory_sha256"] = inventory.hexdigest()
        cls.manifest["inputs"][
            "concatenated_workbook_bytes_sha256"
        ] = concatenated.hexdigest()
        cls.synthetic_manifest = cls.root / "SYNTHETIC_HARNESS.json"
        cls.synthetic_manifest.write_text(
            json.dumps(cls.manifest, indent=2) + "\n", encoding="utf-8"
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.temporary.cleanup()

    def test_production_manifest_is_frozen_and_exact(self) -> None:
        manifest = json.loads(PRODUCTION_MANIFEST.read_text(encoding="utf-8"))
        self.assertEqual(manifest["status"], runner.FROZEN_STATUS)
        self.assertTrue(manifest["tag_created"])
        self.assertEqual(
            manifest["freeze_human_approval"],
            "APPROVO IL FREEZE DELL’HARNESS DI VERBALIZZAZIONE EXP3_V2",
        )
        self.assertEqual(
            manifest["prospective_tag"],
            "exp3-v2-verbalization-harness-frozen-001",
        )
        ids = manifest["inputs"]["canonical_case_ids"]
        self.assertEqual(len(ids), 30)
        self.assertEqual(len(set(ids)), 30)
        expected = []
        for condition in ("N", "F1", "F8", "F10", "F13"):
            expected.extend(f"EXP3V2-{condition}-{index:03d}" for index in range(1, 7))
        self.assertEqual(ids, expected)
        expected_allowlist = [
            "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_BASELINE_STATS_001.json",
            "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_HARNESS_MANIFEST_001.json",
            "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_PROTOCOL_001.md",
            "phase_b/exp3_v2/run_exp3v2_verbalization.py",
            "phase_b/exp3_v2/verify_exp3v2_verbalizations.py",
            "phase_b/tests/test_exp3v2_verbalization_harness.py",
        ]
        self.assertEqual(manifest["freeze_commit_allowlist"]["path_count"], 6)
        self.assertEqual(
            manifest["freeze_commit_allowlist"]["paths"], expected_allowlist
        )
        self.assertEqual(
            {record["path"] for record in manifest["harness_artifacts"]},
            set(expected_allowlist) - {str(PRODUCTION_MANIFEST.relative_to(ROOT))},
        )
        baseline = json.loads(BASELINE_PATH.read_text(encoding="utf-8"))
        self.assertEqual(baseline["status"], "FROZEN_DEVELOPMENT_BASELINE_STATISTICS")
        self.assertEqual(
            baseline["prospective_frozen_status"],
            "FROZEN_DEVELOPMENT_BASELINE_STATISTICS",
        )
        final_freeze = manifest["final_verbalization_freeze"]
        self.assertFalse(final_freeze["tag_only_fetch_sufficient_for_verification"])
        self.assertEqual(final_freeze["payload_root"], "verbalization_outputs")
        self.assertEqual(final_freeze["payload_tree_count"], 61)
        self.assertEqual(final_freeze["governance_tree_count"], 62)

    def test_draft_refuses_execution_before_any_output(self) -> None:
        draft = json.loads(self.synthetic_manifest.read_text(encoding="utf-8"))
        draft["status"] = "PRE_FREEZE_DRAFT"
        path = self.root / "DRAFT.json"
        path.write_text(json.dumps(draft), encoding="utf-8")
        output = self.root / "draft-output"
        with self.assertRaisesRegex(runner.HarnessError, "non-executable"):
            runner.execute_harness(
                path,
                self.data_root,
                output,
                enforce_repository_boundaries=False,
            )
        self.assertFalse(output.exists())

    def test_complete_synthetic_harness_is_deterministic_and_portable(self) -> None:
        output_a = self.root / "output-a"
        output_b = self.root / "output-b"
        with mock.patch.object(
            runner, "_load_baseline", return_value=self.synthetic_baseline
        ):
            first = runner.execute_harness(
                self.synthetic_manifest,
                self.data_root,
                output_a,
                enforce_repository_boundaries=False,
            )
            second = runner.execute_harness(
                self.synthetic_manifest,
                self.data_root,
                output_b,
                enforce_repository_boundaries=False,
            )
        self.assertEqual(first, second)
        self.assertEqual(first["case_count"], 30)
        self.assertEqual(
            (output_a / runner.OUTPUT_MANIFEST_NAME).read_bytes(),
            (output_b / runner.OUTPUT_MANIFEST_NAME).read_bytes(),
        )
        for entry in first["cases"]:
            self.assertEqual(
                (output_a / entry["structured_path"]).read_bytes(),
                (output_b / entry["structured_path"]).read_bytes(),
            )
            self.assertEqual(
                (output_a / entry["neutral_text_path"]).read_bytes(),
                (output_b / entry["neutral_text_path"]).read_bytes(),
            )
        self.assertEqual(
            verifier.verify_outputs(self.synthetic_manifest, self.data_root, output_a),
            [],
        )
        neutral = output_a / first["cases"][0]["neutral_text_path"]
        neutral_bytes = neutral.read_bytes()
        output_manifest_path = output_a / runner.OUTPUT_MANIFEST_NAME
        output_manifest_bytes = output_manifest_path.read_bytes()
        coordinated = json.loads(output_manifest_bytes)
        tampered_bytes = b"coordinated neutral-text tamper\n"
        neutral.write_bytes(tampered_bytes)
        coordinated_entry = coordinated["cases"][0]
        coordinated_entry["neutral_text_size_bytes"] = len(tampered_bytes)
        coordinated_entry["neutral_text_sha256"] = hashlib.sha256(
            tampered_bytes
        ).hexdigest()
        inventory = hashlib.sha256()
        for entry in coordinated["cases"]:
            inventory.update(
                (
                    f"{entry['physical_case_id']},{entry['structured_path']},"
                    f"{entry['structured_size_bytes']},{entry['structured_sha256']},"
                    f"{entry['neutral_text_path']},"
                    f"{entry['neutral_text_size_bytes']},"
                    f"{entry['neutral_text_sha256']}\n"
                ).encode("utf-8")
            )
        coordinated["output_inventory_sha256"] = inventory.hexdigest()
        output_manifest_path.write_text(
            runner.canonical_json(coordinated), encoding="utf-8"
        )
        try:
            errors = verifier.verify_outputs(
                self.synthetic_manifest, self.data_root, output_a
            )
            self.assertIn(
                "neutral text differs from frozen render_text output: "
                f"{first['cases'][0]['physical_case_id']}",
                errors,
            )
        finally:
            neutral.write_bytes(neutral_bytes)
            output_manifest_path.write_bytes(output_manifest_bytes)
        structured = json.loads(
            (output_a / first["cases"][0]["structured_path"]).read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual(structured["time_range_h"], [10.0, 50.0])
        self.assertEqual(structured["window_hours"], 5.0)
        self.assertEqual(structured["n_windows"], 8)

    def test_missing_extra_altered_and_nonempty_outputs_fail_closed(self) -> None:
        freeze, rows = runner._load_and_verify_inputs(self.manifest, self.data_root)
        self.assertEqual(len(rows), 30)
        self.assertEqual(freeze["status"], "FROZEN_BEFORE_VERBALIZATION")
        first = self.data_root / rows[0]["path"]
        backup = self.root / "first-backup.xlsx"

        first.rename(backup)
        try:
            with self.assertRaisesRegex(runner.HarnessError, "regular non-symlink"):
                runner._load_and_verify_inputs(self.manifest, self.data_root)
        finally:
            backup.rename(first)

        extra = self.workbook_root / "EXTRA.xlsx"
        shutil.copyfile(first, extra)
        try:
            with self.assertRaisesRegex(runner.HarnessError, "extra files"):
                runner._load_and_verify_inputs(self.manifest, self.data_root)
        finally:
            extra.unlink()

        original = first.read_bytes()
        changed = bytearray(original)
        changed[-1] ^= 1
        first.write_bytes(changed)
        try:
            with self.assertRaisesRegex(runner.HarnessError, "SHA-256 mismatch"):
                runner._load_and_verify_inputs(self.manifest, self.data_root)
        finally:
            first.write_bytes(original)

        output = self.root / "already-exists"
        output.mkdir()
        (output / "sentinel").write_text("occupied", encoding="utf-8")
        with mock.patch.object(
            runner, "_load_baseline", return_value=self.synthetic_baseline
        ):
            with self.assertRaisesRegex(runner.HarnessError, "must not exist"):
                runner.execute_harness(
                    self.synthetic_manifest,
                    self.data_root,
                    output,
                    enforce_repository_boundaries=False,
                )
        self.assertTrue((output / "sentinel").is_file())

    def test_failure_cleans_only_new_output_root(self) -> None:
        output = self.root / "failure-output"
        source_hashes = {
            row["path"]: sha256_file(self.data_root / row["path"])
            for row in json.loads(
                (self.data_root / "phase_b/exp3_v2/SYNTHETIC_DATA.json").read_text(
                    encoding="utf-8"
                )
            )["data_artifacts"]["workbook_inventory"]
        }
        with (
            mock.patch.object(
                runner, "_load_baseline", return_value=self.synthetic_baseline
            ),
            mock.patch.object(
                runner,
                "_validate_result",
                side_effect=RuntimeError("synthetic failure"),
            ),
        ):
            with self.assertRaisesRegex(RuntimeError, "synthetic failure"):
                runner.execute_harness(
                    self.synthetic_manifest,
                    self.data_root,
                    output,
                    enforce_repository_boundaries=False,
                )
        self.assertFalse(output.exists())
        self.assertEqual(
            source_hashes,
            {path: sha256_file(self.data_root / path) for path in source_hashes},
        )

    def test_policy_has_no_rng_network_or_recalibration_calls(self) -> None:
        runner._verify_static_prohibitions(self.manifest, ROOT)
        tree = ast.parse(
            (HARNESS_DIR / "run_exp3v2_verbalization.py").read_text(encoding="utf-8")
        )
        imports = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        roots = {name.split(".")[0] for name in imports}
        self.assertTrue(roots.isdisjoint(runner.FORBIDDEN_IMPORT_ROOTS))

    def test_runtime_is_exactly_pinned_and_fails_closed(self) -> None:
        self.assertEqual(
            runner._verify_runtime(self.manifest),
            {
                "python": "3.13.9",
                "pandas": "2.3.3",
                "numpy": "2.3.5",
                "openpyxl": "3.1.5",
                "jsonschema": "4.25.0",
            },
        )
        altered = json.loads(json.dumps(self.manifest))
        altered["python_runtime"]["packages"]["numpy"] = "0.0.0"
        with self.assertRaisesRegex(runner.HarnessError, "dependency mismatch"):
            runner._verify_runtime(altered)

    def test_actual_cli_enforces_annotated_tag_boundaries_synthetically(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="exp3v2-verbalization-cli-boundary-"
        ) as temporary:
            rehearsal = Path(temporary)
            data_repo = rehearsal / "data-repository"
            harness_repo = rehearsal / "harness-repository"
            output_parent = rehearsal / "verbalization-output"
            data_repo.mkdir()
            harness_repo.mkdir()
            output_parent.mkdir()

            run_git(data_repo, "init", "--initial-branch=synthetic-data")
            shutil.copytree(self.data_root, data_repo, dirs_exist_ok=True)
            run_git(data_repo, "add", "--all")
            run_git(data_repo, "commit", "-m", "Synthetic data boundary")
            data_commit = run_git(data_repo, "rev-parse", "HEAD")
            data_tag = "synthetic-exp3v2-data-frozen-001"
            run_git(data_repo, "tag", "-a", data_tag, "-m", "Synthetic data tag")
            data_tag_object = run_git(data_repo, "rev-parse", f"refs/tags/{data_tag}")
            run_git(data_repo, "checkout", "--detach", data_tag)
            run_git(data_repo, "branch", "-D", "synthetic-data")

            run_git(harness_repo, "init", "--initial-branch=synthetic-harness")
            source_paths = [record["path"] for record in self.manifest["frozen_assets"]]
            if (ROOT / ".gitignore").is_file():
                source_paths.append(".gitignore")
            for relative in source_paths:
                copy_relative(ROOT, harness_repo, relative)
            run_git(harness_repo, "add", "--all")
            run_git(harness_repo, "commit", "-m", "Synthetic source boundary")
            source_commit = run_git(harness_repo, "rev-parse", "HEAD")
            source_tag = "synthetic-exp3v2-source-frozen-001"
            run_git(
                harness_repo,
                "tag",
                "-a",
                source_tag,
                "-m",
                "Synthetic source tag",
            )
            source_tag_object = run_git(
                harness_repo, "rev-parse", f"refs/tags/{source_tag}"
            )

            candidate_paths = [
                "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_BASELINE_STATS_001.json",
                "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_PROTOCOL_001.md",
                "phase_b/exp3_v2/run_exp3v2_verbalization.py",
                "phase_b/exp3_v2/verify_exp3v2_verbalizations.py",
                "phase_b/tests/test_exp3v2_verbalization_harness.py",
            ]
            for relative in candidate_paths:
                copy_relative(ROOT, harness_repo, relative)

            baseline_path = (
                harness_repo
                / "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_BASELINE_STATS_001.json"
            )
            baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
            baseline["status"] = "FROZEN_DEVELOPMENT_BASELINE_STATISTICS"
            baseline_path.write_text(runner.canonical_json(baseline), encoding="utf-8")

            synthetic_manifest = json.loads(json.dumps(self.manifest))
            synthetic_manifest["status"] = runner.FROZEN_STATUS
            synthetic_manifest["tag_created"] = True
            harness_tag = "synthetic-exp3v2-verbalization-harness-frozen-001"
            synthetic_manifest["prospective_tag"] = harness_tag
            synthetic_manifest["boundaries"]["source"].update(
                {
                    "tag": source_tag,
                    "tag_object": source_tag_object,
                    "commit": source_commit,
                }
            )
            data_manifest_path = data_repo / "phase_b/exp3_v2/SYNTHETIC_DATA.json"
            synthetic_manifest["boundaries"]["data"].update(
                {
                    "tag": data_tag,
                    "tag_object": data_tag_object,
                    "commit": data_commit,
                    "data_commit": data_commit,
                    "manifest_path": "phase_b/exp3_v2/SYNTHETIC_DATA.json",
                    "manifest_size_bytes": data_manifest_path.stat().st_size,
                    "manifest_sha256": sha256_file(data_manifest_path),
                }
            )
            for record in synthetic_manifest["frozen_assets"]:
                record["source_tag"] = source_tag
            roles = {
                record["path"]: record["role"]
                for record in synthetic_manifest["harness_artifacts"]
            }
            roles["phase_b/tests/test_exp3v2_verbalization_harness.py"] = (
                "synthetic and production-boundary regression tests"
            )
            synthetic_manifest["harness_artifacts"] = [
                {
                    "path": relative,
                    "size_bytes": (harness_repo / relative).stat().st_size,
                    "sha256": sha256_file(harness_repo / relative),
                    "role": roles[relative],
                }
                for relative in candidate_paths
            ]
            synthetic_manifest["baseline_statistics"].update(
                {
                    "size_bytes": baseline_path.stat().st_size,
                    "sha256": sha256_file(baseline_path),
                }
            )
            manifest_path = (
                harness_repo
                / "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_HARNESS_MANIFEST_001.json"
            )
            manifest_path.write_text(
                runner.canonical_json(synthetic_manifest), encoding="utf-8"
            )
            run_git(harness_repo, "add", "--all")
            run_git(harness_repo, "commit", "-m", "Synthetic frozen harness")
            run_git(
                harness_repo,
                "tag",
                "-a",
                harness_tag,
                "-m",
                "Synthetic harness tag",
            )
            run_git(harness_repo, "checkout", "--detach", harness_tag)
            run_git(harness_repo, "branch", "-D", "synthetic-harness")

            output_root = output_parent / "output"
            python = self.manifest["python_runtime"]["invocation_executable"]
            command = [
                python,
                str(harness_repo / "phase_b/exp3_v2/run_exp3v2_verbalization.py"),
                "--manifest",
                str(manifest_path),
                "--data-root",
                str(data_repo),
                "--output-root",
                str(output_root),
            ]
            completed = subprocess.run(
                command,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result["result"], "PASS")
            self.assertEqual(result["cases"], 30)

            verify_command = [
                python,
                str(harness_repo / "phase_b/exp3_v2/verify_exp3v2_verbalizations.py"),
                "--manifest",
                str(manifest_path),
                "--data-root",
                str(data_repo),
                "--output-root",
                str(output_root),
            ]
            verified = subprocess.run(
                verify_command,
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(verified.returncode, 0, verified.stderr)
            self.assertIn("PASS:", verified.stdout)

            final_repo = rehearsal / "final-verbalization-repository"
            final_repo.mkdir()
            run_git(final_repo, "init", "--initial-branch=synthetic-final")
            shutil.copytree(output_root, final_repo / "verbalization_outputs")
            run_git(final_repo, "add", "--all")
            run_git(final_repo, "commit", "-m", "Synthetic verbalization payload")
            data_commit = run_git(final_repo, "rev-parse", "HEAD")
            self.assertEqual(
                run_git(final_repo, "rev-list", "--parents", "-n", "1", data_commit),
                data_commit,
            )
            self.assertEqual(
                len(
                    run_git(
                        final_repo, "ls-tree", "-r", "--name-only", "HEAD"
                    ).splitlines()
                ),
                61,
            )
            governance_path = (
                final_repo
                / "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_DATA_FREEZE_MANIFEST_001.json"
            )
            governance_path.parent.mkdir(parents=True)
            governance_path.write_text(
                runner.canonical_json(
                    {
                        "status": "SYNTHETIC_FROZEN_BEFORE_INFERENCE",
                        "payload_commit": data_commit,
                    }
                ),
                encoding="utf-8",
            )
            run_git(final_repo, "add", str(governance_path.relative_to(final_repo)))
            run_git(final_repo, "commit", "-m", "Synthetic verbalization governance")
            self.assertEqual(
                len(
                    run_git(
                        final_repo, "ls-tree", "-r", "--name-only", "HEAD"
                    ).splitlines()
                ),
                62,
            )
            final_tag = "synthetic-exp3v2-verbalizations-frozen-001"
            run_git(final_repo, "tag", "-a", final_tag, "-m", "Synthetic final tag")
            run_git(final_repo, "checkout", "--detach", final_tag)
            run_git(final_repo, "branch", "-D", "synthetic-final")
            self.assertEqual(
                run_git(
                    final_repo, "for-each-ref", "--format=%(refname)", "refs/heads"
                ),
                "",
            )
            final_verified = subprocess.run(
                [*verify_command[:-1], str(final_repo / "verbalization_outputs")],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertEqual(final_verified.returncode, 0, final_verified.stderr)
            self.assertIn("PASS:", final_verified.stdout)

            (harness_repo / "UNTRACKED_BOUNDARY_VIOLATION").write_text(
                "synthetic only\n", encoding="utf-8"
            )
            rejected_output = output_parent / "must-not-be-created"
            rejected = subprocess.run(
                [*command[:-1], str(rejected_output)],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            self.assertNotEqual(rejected.returncode, 0)
            self.assertIn("harness worktree must be completely clean", rejected.stderr)
            self.assertFalse(rejected_output.exists())


if __name__ == "__main__":
    unittest.main()
