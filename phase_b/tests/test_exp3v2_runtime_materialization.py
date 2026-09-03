from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
V2 = ROOT / "phase_b/exp3_v2"
MANIFEST_PATH = V2 / "EXP3_V2_HARNESS_FREEZE_MANIFEST_003.json"
SOURCE = ROOT / "tep_parent_a0413e16/simulator"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


materialize = load_module(
    "materialize_exp3v2_runtime", V2 / "materialize_exp3v2_runtime.py"
)
verify = load_module("verify_exp3v2", V2 / "verify_exp3v2_heldout.py")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class Exp3V2RuntimeMaterializationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.manifest = json.loads(MANIFEST_PATH.read_text())
        self.dependencies = self.manifest["external_runtime_dependencies"]

    def copy_source_bundle(self, destination: Path, *, omit: str = "") -> None:
        destination.mkdir()
        for dependency in self.dependencies:
            relative = dependency["path"]
            if relative != omit:
                shutil.copyfile(SOURCE / relative, destination / relative)

    def test_clean_boundary_preflight_passes_with_materialized_bundle(self) -> None:
        source_before = {
            row["path"]: sha256_file(SOURCE / row["path"]) for row in self.dependencies
        }
        with tempfile.TemporaryDirectory() as directory:
            parent = Path(directory)
            runtime = materialize.materialize_runtime(MANIFEST_PATH, SOURCE, parent)
            self.assertEqual(
                verify.validate_runtime_directory(self.manifest, runtime), []
            )
            self.assertEqual(
                verify.prefreeze_checks(
                    V2 / "exp3v2_case_plan.json",
                    MANIFEST_PATH,
                    V2 / "EXP3_V2_FREEZE_MANIFEST.json",
                    runtime,
                ),
                [],
            )
            self.assertEqual(
                {path.name for path in runtime.iterdir()},
                set(materialize.EXPECTED_DEPENDENCY_PATHS),
            )
            self.assertFalse((runtime / "MultiLoop_mode1.slxc").exists())
        source_after = {
            row["path"]: sha256_file(SOURCE / row["path"]) for row in self.dependencies
        }
        self.assertEqual(source_before, source_after)

    def test_missing_dependency_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            parent = root / "parent"
            parent.mkdir()
            self.copy_source_bundle(source, omit="TElib.mdl")
            with self.assertRaisesRegex(
                materialize.MaterializationError, "missing regular dependency"
            ):
                materialize.materialize_runtime(MANIFEST_PATH, source, parent)

    def test_altered_dependency_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            parent = root / "parent"
            parent.mkdir()
            self.copy_source_bundle(source)
            with (source / "Mode_1_Init.m").open("ab") as stream:
                stream.write(b"\n% altered fixture\n")
            with self.assertRaisesRegex(
                materialize.MaterializationError, "size mismatch"
            ):
                materialize.materialize_runtime(MANIFEST_PATH, source, parent)

    def test_source_symlink_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            parent = root / "parent"
            parent.mkdir()
            self.copy_source_bundle(source, omit="TElib.mdl")
            (source / "TElib.mdl").symlink_to(SOURCE / "TElib.mdl")
            with self.assertRaisesRegex(
                materialize.MaterializationError, "symlink is forbidden"
            ):
                materialize.materialize_runtime(MANIFEST_PATH, source, parent)

    def test_generated_slxc_is_rejected_from_materialized_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            runtime = materialize.materialize_runtime(
                MANIFEST_PATH, SOURCE, Path(directory)
            )
            shutil.copyfile(
                SOURCE / "MultiLoop_mode1.slxc",
                runtime / "MultiLoop_mode1.slxc",
            )
            self.assertIn(
                "materialized runtime has missing or extra files",
                verify.validate_runtime_directory(self.manifest, runtime),
            )

    def test_extra_manifest_dependency_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            altered = json.loads(MANIFEST_PATH.read_text())
            altered["external_runtime_dependencies"].append(
                {
                    "path": "unexpected.txt",
                    "size_bytes": 0,
                    "sha256": "0" * 64,
                    "role": "unexpected",
                    "provenance": "test fixture",
                }
            )
            altered_path = root / "manifest.json"
            altered_path.write_text(json.dumps(altered))
            with self.assertRaisesRegex(
                materialize.MaterializationError,
                "missing or extra required external dependency",
            ):
                materialize.load_dependencies(altered_path)

    def test_git_boundary_excludes_ignored_live_and_runtime_files(self) -> None:
        artifacts = {row["path"] for row in self.manifest["artifacts"]}
        self.assertNotIn("tep_exp3_heldout/exp3_attempt_log.json", artifacts)
        self.assertFalse(
            any(path.startswith("tep_parent_a0413e16/simulator/") for path in artifacts)
        )
        for relative in artifacts:
            ignored = subprocess.run(
                ["git", "check-ignore", "--no-index", "--quiet", relative],
                cwd=ROOT,
            )
            self.assertNotEqual(ignored.returncode, 0, relative)


if __name__ == "__main__":
    unittest.main()
