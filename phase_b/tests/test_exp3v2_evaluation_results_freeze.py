from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "phase_b/exp3_v2/verify_exp3v2_evaluation_results_freeze.py"
SPEC = importlib.util.spec_from_file_location("results_freeze_verifier", MODULE_PATH)
assert SPEC and SPEC.loader
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


def run_git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


class ResultsFreezeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.payload = self.root / "payload"
        self.payload.mkdir()
        self.schema_root = self.root / "phase_b/exp3_v2/evaluation_schemas"
        self.schema_root.mkdir(parents=True)
        (self.schema_root / verifier.SCHEMA_RELATIVE.name).write_text(
            '{"type":"object"}\n', encoding="utf-8"
        )
        self.constants = self._write_synthetic_payload()
        self.manifest = self._manifest()
        self.patches = [
            mock.patch.object(verifier, "EXPECTED_ARTIFACTS", self.constants["items"]),
            mock.patch.object(
                verifier, "EXPECTED_TOTAL_BYTES", self.constants["total"]
            ),
            mock.patch.object(
                verifier, "EXPECTED_INVENTORY_SHA256", self.constants["inventory"]
            ),
            mock.patch.object(
                verifier,
                "EXPECTED_CONCATENATED_SHA256",
                self.constants["concatenated"],
            ),
            mock.patch.object(
                verifier,
                "EXPECTED_INTERNAL_INVENTORY_SHA256",
                self.constants["internal"],
            ),
        ]
        for patcher in self.patches:
            patcher.start()
            self.addCleanup(patcher.stop)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _write_synthetic_payload(self) -> dict[str, object]:
        names = [item["path"] for item in verifier.EXPECTED_ARTIFACTS]
        contents = {
            names[0]: b"synthetic-bootstrap\n",
            names[1]: b"synthetic-results\n",
        }
        internal_items = [
            {
                "path": name,
                "size_bytes": len(contents[name]),
                "sha256": hashlib.sha256(contents[name]).hexdigest(),
            }
            for name in names[:2]
        ]
        internal_inventory = "".join(
            f"{item['path']}\0{item['size_bytes']}\0{item['sha256']}\n"
            for item in internal_items
        ).encode("utf-8")
        internal_digest = hashlib.sha256(internal_inventory).hexdigest()
        internal_manifest = {
            "schema_version": "1.0",
            "status": "COMPLETE_PENDING_RESULTS_FREEZE",
            "artifact_count": 2,
            "artifacts": internal_items,
            "inventory_sha256": internal_digest,
            "optional_analyses_included": [],
        }
        contents[names[2]] = verifier.canonical_json_bytes(internal_manifest)
        items = [
            {
                "path": name,
                "size_bytes": len(contents[name]),
                "sha256": hashlib.sha256(contents[name]).hexdigest(),
            }
            for name in names
        ]
        for name, content in contents.items():
            (self.payload / name).write_bytes(content)
        concatenated = hashlib.sha256()
        for item in items:
            concatenated.update((self.payload / item["path"]).read_bytes())
        return {
            "items": items,
            "total": sum(item["size_bytes"] for item in items),
            "inventory": hashlib.sha256(
                verifier.canonical_json_bytes(items)
            ).hexdigest(),
            "concatenated": concatenated.hexdigest(),
            "internal": internal_digest,
        }

    def _manifest(self) -> dict[str, object]:
        return {
            "status": verifier.DRAFT_STATUS,
            "prospective_tag": verifier.TAG,
            "tag_created": False,
            "human_freeze_approval": None,
            "non_self_referential": {
                "manifest_sha256_recorded": False,
                "governance_commit_recorded": False,
                "tag_object_recorded": False,
                "payload_commit_may_be_recorded": True,
            },
            "governance": {
                "actual_payload_commit": None,
                "file_allowlist": verifier.GOVERNANCE_ALLOWLIST,
                "non_manifest_artifacts": [],
            },
            "boundary_tags": verifier.EXPECTED_BOUNDARIES,
            "critical_artifacts": verifier.EXPECTED_CRITICAL_ARTIFACTS,
            "execution_provenance": verifier.EXPECTED_EXECUTION_PROVENANCE,
            "payload": {
                "artifacts": self.constants["items"],
                "path_count": 3,
                "total_size_bytes": self.constants["total"],
                "inventory_sha256": self.constants["inventory"],
                "concatenated_bytes_sha256": self.constants["concatenated"],
            },
            "portable_verification": {
                "required_annotated_tags": [
                    item["name"] for item in verifier.EXPECTED_BOUNDARIES
                ]
                + [verifier.TAG]
            },
        }

    def test_clean_payload(self) -> None:
        observed = verifier.verify_payload(self.manifest, self.payload)
        self.assertEqual(observed["path_count"], 3)

    def test_altered_payload_fails(self) -> None:
        (self.payload / self.constants["items"][0]["path"]).write_bytes(b"altered")
        with self.assertRaisesRegex(RuntimeError, "independent frozen constants"):
            verifier.verify_payload(self.manifest, self.payload)

    def test_missing_payload_fails(self) -> None:
        (self.payload / self.constants["items"][0]["path"]).unlink()
        with self.assertRaises(RuntimeError):
            verifier.verify_payload(self.manifest, self.payload)

    def test_extra_payload_fails(self) -> None:
        (self.payload / "extra.json").write_text("{}\n", encoding="utf-8")
        with self.assertRaises(RuntimeError):
            verifier.verify_payload(self.manifest, self.payload)

    def test_symlink_fails(self) -> None:
        target = self.payload / self.constants["items"][0]["path"]
        target.unlink()
        target.symlink_to(self.payload / self.constants["items"][1]["path"])
        with self.assertRaisesRegex(RuntimeError, "symlink"):
            verifier.verify_payload(self.manifest, self.payload)

    def test_lfs_pointer_fails(self) -> None:
        path = self.payload / self.constants["items"][0]["path"]
        path.write_bytes(verifier.LFS_HEADER + b"\noid sha256:00\n")
        items = copy.deepcopy(self.constants["items"])
        items[0]["size_bytes"] = path.stat().st_size
        items[0]["sha256"] = verifier.sha256_file(path)
        total = sum(item["size_bytes"] for item in items)
        inventory = hashlib.sha256(verifier.canonical_json_bytes(items)).hexdigest()
        with (
            mock.patch.object(verifier, "EXPECTED_ARTIFACTS", items),
            mock.patch.object(verifier, "EXPECTED_TOTAL_BYTES", total),
            mock.patch.object(verifier, "EXPECTED_INVENTORY_SHA256", inventory),
        ):
            self.manifest["payload"]["artifacts"] = items
            with self.assertRaisesRegex(RuntimeError, "LFS"):
                verifier.verify_payload(self.manifest, self.payload)

    def test_coordinated_manifest_tamper_fails(self) -> None:
        path = self.payload / self.constants["items"][0]["path"]
        path.write_bytes(b"coordinated-alteration\n")
        tampered = copy.deepcopy(self.manifest)
        item = tampered["payload"]["artifacts"][0]
        item["size_bytes"] = path.stat().st_size
        item["sha256"] = verifier.sha256_file(path)
        tampered["payload"]["total_size_bytes"] = sum(
            entry["size_bytes"] for entry in tampered["payload"]["artifacts"]
        )
        tampered["payload"]["inventory_sha256"] = hashlib.sha256(
            verifier.canonical_json_bytes(tampered["payload"]["artifacts"])
        ).hexdigest()
        with self.assertRaisesRegex(RuntimeError, "independent frozen constants"):
            verifier.verify_payload(tampered, self.payload)

    def test_wrong_revision_binding_fails(self) -> None:
        altered = copy.deepcopy(self.manifest)
        altered["boundary_tags"][-1]["peeled_commit"] = "0" * 40
        with self.assertRaisesRegex(RuntimeError, "boundary"):
            verifier.validate_manifest(
                altered,
                self.schema_root / verifier.SCHEMA_RELATIVE.name,
                "review_draft",
            )

    def test_failure_provenance_tamper_fails(self) -> None:
        altered = copy.deepcopy(self.manifest)
        altered["execution_provenance"]["revision_001"]["exhausted"] = False
        with self.assertRaisesRegex(RuntimeError, "provenance"):
            verifier.validate_manifest(
                altered,
                self.schema_root / verifier.SCHEMA_RELATIVE.name,
                "review_draft",
            )

    def test_draft_cannot_be_accepted_as_frozen(self) -> None:
        with self.assertRaisesRegex(RuntimeError, "status"):
            verifier.validate_manifest(
                self.manifest,
                self.schema_root / verifier.SCHEMA_RELATIVE.name,
                "public_final",
            )

    def _make_topology(
        self, *, annotated: bool = True, keep_branch: bool = False, extra: bool = False
    ) -> tuple[Path, dict[str, object], str]:
        repo = self.root / f"repo-{len(list(self.root.glob('repo-*')))}"
        repo.mkdir()
        run_git(repo, "init", "-q")
        run_git(repo, "config", "user.name", "Synthetic Test")
        run_git(repo, "config", "user.email", "synthetic@example.invalid")
        output = repo / "evaluation_outputs"
        output.mkdir()
        for item in self.constants["items"]:
            (output / item["path"]).write_bytes(
                (self.payload / item["path"]).read_bytes()
            )
        run_git(repo, "add", "evaluation_outputs")
        run_git(repo, "commit", "-qm", "synthetic parentless payload")
        payload_commit = run_git(repo, "rev-parse", "HEAD")
        for relative in verifier.GOVERNANCE_ALLOWLIST:
            path = repo / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("synthetic governance\n", encoding="utf-8")
        if extra:
            (repo / "unexpected.txt").write_text("extra\n", encoding="utf-8")
        run_git(repo, "add", ".")
        run_git(repo, "commit", "-qm", "synthetic governance")
        if annotated:
            run_git(repo, "tag", "-a", verifier.TAG, "-m", "synthetic tag")
        else:
            run_git(repo, "tag", verifier.TAG)
        run_git(repo, "checkout", "-q", "--detach", "HEAD")
        if not keep_branch:
            branch = run_git(
                repo, "for-each-ref", "--format=%(refname:short)", "refs/heads"
            )
            run_git(repo, "branch", "-D", branch)
        manifest = copy.deepcopy(self.manifest)
        manifest["governance"]["actual_payload_commit"] = payload_commit
        return repo, manifest, payload_commit

    def test_clean_topology(self) -> None:
        repo, manifest, payload_commit = self._make_topology()
        observed = verifier.verify_topology(manifest, repo)
        self.assertEqual(observed["payload_commit"], payload_commit)

    def test_wrong_parentage_fails(self) -> None:
        repo, manifest, _ = self._make_topology()
        manifest["governance"]["actual_payload_commit"] = "0" * 40
        with self.assertRaisesRegex(RuntimeError, "parent"):
            verifier.verify_topology(manifest, repo)

    def test_lightweight_tag_fails(self) -> None:
        repo, manifest, _ = self._make_topology(annotated=False)
        with self.assertRaisesRegex(RuntimeError, "annotated"):
            verifier.verify_topology(manifest, repo)

    def test_branch_ref_fails(self) -> None:
        repo, manifest, _ = self._make_topology(keep_branch=True)
        with self.assertRaisesRegex(RuntimeError, "branch"):
            verifier.verify_topology(manifest, repo)

    def test_tree_count_or_extra_path_fails(self) -> None:
        repo, manifest, _ = self._make_topology(extra=True)
        with self.assertRaisesRegex(RuntimeError, "governance commit"):
            verifier.verify_topology(manifest, repo)

    def test_fresh_tag_only_fetch_is_portable(self) -> None:
        source, manifest, payload_commit = self._make_topology()
        fresh = self.root / "fresh"
        fresh.mkdir()
        run_git(fresh, "init", "-q")
        run_git(fresh, "remote", "add", "origin", str(source))
        run_git(
            fresh,
            "fetch",
            "--no-tags",
            "origin",
            f"refs/tags/{verifier.TAG}:refs/tags/{verifier.TAG}",
        )
        run_git(fresh, "checkout", "-q", "--detach", f"refs/tags/{verifier.TAG}^{{}}")
        self.assertFalse(
            run_git(fresh, "for-each-ref", "--format=%(refname)", "refs/heads")
        )
        self.assertFalse(
            run_git(fresh, "for-each-ref", "--format=%(refname)", "refs/remotes")
        )
        observed = verifier.verify_topology(manifest, fresh)
        self.assertEqual(observed["payload_commit"], payload_commit)

    def test_finalization_is_acyclic(self) -> None:
        candidate = json.loads(
            (
                ROOT
                / "phase_b/exp3_v2/EXP3_V2_EVALUATION_RESULTS_FREEZE_MANIFEST_001.json"
            ).read_text(encoding="utf-8")
        )
        self.assertNotIn("manifest_sha256", candidate)
        self.assertNotIn("governance_commit", candidate)
        self.assertNotIn("tag_object", candidate)
        self.assertFalse(candidate["non_self_referential"]["manifest_sha256_recorded"])
        self.assertFalse(
            candidate["non_self_referential"]["governance_commit_recorded"]
        )
        self.assertFalse(candidate["non_self_referential"]["tag_object_recorded"])
        self.assertIsNone(candidate["governance"]["actual_payload_commit"])

    def test_real_draft_schema_is_valid(self) -> None:
        manifest_path = (
            ROOT / "phase_b/exp3_v2/EXP3_V2_EVALUATION_RESULTS_FREEZE_MANIFEST_001.json"
        )
        schema_path = ROOT / verifier.SCHEMA_RELATIVE
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        verifier.jsonschema.Draft202012Validator(
            json.loads(schema_path.read_text(encoding="utf-8"))
        ).validate(manifest)
        self.assertEqual(manifest["status"], verifier.DRAFT_STATUS)


if __name__ == "__main__":
    unittest.main()
