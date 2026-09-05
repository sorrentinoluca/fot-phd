#!/usr/bin/env python3
"""Portable verifier for the EXP3_V2 evaluation-results tag-only freeze."""

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from typing import Any, Iterable

import jsonschema


sys.dont_write_bytecode = True


TAG = "exp3-v2-results-frozen-001"
DRAFT_STATUS = "PENDING_HUMAN_EVALUATION_RESULTS_FREEZE"
FROZEN_STATUS = "FROZEN_BEFORE_VERBALIZATION"
RUNTIME = Path("/private/tmp/exp3v2-evaluation-runtime-001/bin/python3")
MANIFEST_RELATIVE = Path(
    "phase_b/exp3_v2/EXP3_V2_EVALUATION_RESULTS_FREEZE_MANIFEST_001.json"
)
SCHEMA_RELATIVE = Path(
    "phase_b/exp3_v2/evaluation_schemas/"
    "exp3v2_evaluation_results_freeze_manifest.schema.json"
)
FROZEN_SEMANTIC_VERIFIER = Path("phase_b/exp3_v2/verify_exp3v2_evaluation.py")
LFS_HEADER = b"version https://git-lfs.github.com/spec/v1"

EXPECTED_ARTIFACTS = [
    {
        "path": "exp3v2_confirmatory_bootstrap.json",
        "size_bytes": 350285,
        "sha256": "05a0f4446f8cdf6c20a8cf3e804472ddceb838b708245173906f5f2d81bfa9e8",
    },
    {
        "path": "exp3v2_confirmatory_results.json",
        "size_bytes": 2033,
        "sha256": "e01b948cc78f2d35e79db4430db530c68cea3381385fb635bb5dd8145a58ffdb",
    },
    {
        "path": "exp3v2_evaluation_output_hash_manifest.json",
        "size_bytes": 499,
        "sha256": "48811e09f310c3133018bb3d60a05abc5553d77efcba2337d81e5e385e67d448",
    },
]
EXPECTED_TOTAL_BYTES = 352817
EXPECTED_INVENTORY_SHA256 = (
    "23161e0cbb7a099f44aa4503538aee03ef343be7d47e19c9711865709ba45d86"
)
EXPECTED_CONCATENATED_SHA256 = (
    "7a13563934be6e14ee23af5a41010a3188bbb7fe5604f2305a1bb8e5dd0f55e4"
)
EXPECTED_INTERNAL_INVENTORY_SHA256 = (
    "d3266329ef9fa782263eefe7ca69fedbdc2bb2cdfec3b7a973a0341c60a2ca83"
)

GOVERNANCE_ALLOWLIST = [
    "phase_b/exp3_v2/EXP3_V2_EVALUATION_RESULTS_FREEZE_PROTOCOL_002.md",
    "phase_b/exp3_v2/evaluation_schemas/exp3v2_evaluation_results_freeze_manifest.schema.json",
    "phase_b/exp3_v2/EXP3_V2_EVALUATION_RESULTS_FREEZE_MANIFEST_001.json",
    "phase_b/exp3_v2/verify_exp3v2_evaluation_results_freeze.py",
    "phase_b/tests/test_exp3v2_evaluation_results_freeze.py",
]

EXPECTED_BOUNDARIES = [
    {
        "role": "source",
        "name": "exp3-v2-heldout-frozen-002",
        "tag_object": "eaddc2c0791febcccce6412c0a9cc2cf81b3cb21",
        "peeled_commit": "6f88abdecc25e015064e5fc2c59000f8a1a0bc7e",
        "manifest_path": "phase_b/exp3_v2/EXP3_V2_FREEZE_MANIFEST_002.json",
        "manifest_sha256": "8e50fb79a31a336f3e93e4057ee10d4551a3f3f7a8f717096a433259de7ee26f",
    },
    {
        "role": "data",
        "name": "exp3-v2-heldout-data-frozen-001",
        "tag_object": "34319bbb28fcedadd15acc5dfa2183b3fe733ce3",
        "peeled_commit": "7bcf309910920b52c485125312599d1ded9c4c74",
        "manifest_path": "phase_b/exp3_v2/EXP3_V2_DATA_FREEZE_MANIFEST_001.json",
        "manifest_sha256": "adb8875ace9155906bb28332791fc3278409a4e5389abfb78c8d14aacc750ad2",
    },
    {
        "role": "verbalization_harness",
        "name": "exp3-v2-verbalization-harness-frozen-001",
        "tag_object": "b2ac5c24835e1f5817baa0e1e8ba13d498777e7d",
        "peeled_commit": "0ca1ebf339a49c78908e00f65093aeccccc1616f",
        "manifest_path": "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_HARNESS_MANIFEST_001.json",
        "manifest_sha256": "8eb4ec8953112555d4f4168127e7296be7d33a8d0fc513249d49328f4775f1b5",
    },
    {
        "role": "verbalizations",
        "name": "exp3-v2-verbalizations-frozen-001",
        "tag_object": "4eeb14e77c5d5b45395da0d88012bcf30cea83ea",
        "peeled_commit": "4159fba5e4d23cbc9af62c2aad72f11eda1491db",
        "manifest_path": "phase_b/exp3_v2/EXP3_V2_VERBALIZATION_DATA_FREEZE_MANIFEST_001.json",
        "manifest_sha256": "d75d51a3c30efc7ed5e2a82f5f17cdecf77e2484d17a87e3716f4abbb8fe35a7",
    },
    {
        "role": "inference_harness",
        "name": "exp3-v2-inference-harness-frozen-001",
        "tag_object": "df1f77fee805b19d7a6e782c0ea696dd6c3ffa07",
        "peeled_commit": "24b030a07652649556953aaa1a2cfb29e54ab2f7",
        "manifest_path": "phase_b/exp3_v2/EXP3_V2_INFERENCE_HARNESS_MANIFEST_001.json",
        "manifest_sha256": "68256cf4eeab3eb3e9c44b16914dcbfc4e9514a2db8e570b2f61cd7576365bf6",
    },
    {
        "role": "execution_authorization",
        "name": "exp3-v2-inference-execution-frozen-001",
        "tag_object": "74a14b941cbf229b48529c9c7202613ac4a482c7",
        "peeled_commit": "c62c871657c061826efda708aacd386779a16d02",
        "manifest_path": "phase_b/exp3_v2/EXP3_V2_INFERENCE_EXECUTION_AUTHORIZATION_MANIFEST_001.json",
        "manifest_sha256": "04fd71e4d625d0057b2cb8aa82ce921e3344a364d00a37cc0bd882caa44a253b",
    },
    {
        "role": "inference_outputs",
        "name": "exp3-v2-inference-frozen-001",
        "tag_object": "e1aa80d2f54d4cefdbc7273cbcdb139f0df57563",
        "peeled_commit": "9a7ccaa95bae8c0d2d00dc0959e177eb90a5cd61",
        "manifest_path": "phase_b/exp3_v2/EXP3_V2_INFERENCE_DATA_FREEZE_MANIFEST_001.json",
        "manifest_sha256": "ab3ee52bc391546bb4b75e7575b6709bc1192513fb17a731278c2c43648674f0",
    },
    {
        "role": "evaluation_harness_revision_001",
        "name": "exp3-v2-evaluation-harness-frozen-001",
        "tag_object": "43163e51ebd4e592aaf3d03d7bec50c4cd0b63fb",
        "peeled_commit": "25dc65bba805f15836f09e9613505bf483199a4f",
        "manifest_path": "phase_b/exp3_v2/EXP3_V2_EVALUATION_HARNESS_MANIFEST_001.json",
        "manifest_sha256": "d8454d13ed7299fdac690657fcacb731e8b8b6f0c0cebf2213af5adf1e7547cd",
    },
    {
        "role": "evaluation_harness_revision_002",
        "name": "exp3-v2-evaluation-harness-frozen-002",
        "tag_object": "77115c2b608a19d1e1f1be6187928bfb3f0d297d",
        "peeled_commit": "d0da3921051787539c4ddfa1ee4d0714ee6c0139",
        "manifest_path": "phase_b/exp3_v2/EXP3_V2_EVALUATION_HARNESS_MANIFEST_002.json",
        "manifest_sha256": "853ce14dd53837459837ef8549124a4d65cb20e40078f88010477162cce3efa6",
    },
]

EXPECTED_CRITICAL_ARTIFACTS = [
    {
        "role": "revision_001_manifest",
        "boundary_tag": "exp3-v2-evaluation-harness-frozen-001",
        "path": "phase_b/exp3_v2/EXP3_V2_EVALUATION_HARNESS_MANIFEST_001.json",
        "size_bytes": 9428,
        "sha256": "d8454d13ed7299fdac690657fcacb731e8b8b6f0c0cebf2213af5adf1e7547cd",
    },
    {
        "role": "revision_002_manifest",
        "boundary_tag": "exp3-v2-evaluation-harness-frozen-002",
        "path": "phase_b/exp3_v2/EXP3_V2_EVALUATION_HARNESS_MANIFEST_002.json",
        "size_bytes": 11977,
        "sha256": "853ce14dd53837459837ef8549124a4d65cb20e40078f88010477162cce3efa6",
    },
    {
        "role": "revision_002_evaluator",
        "boundary_tag": "exp3-v2-evaluation-harness-frozen-002",
        "path": "phase_b/exp3_v2/evaluate_exp3v2_frozen_predictions.py",
        "size_bytes": 29904,
        "sha256": "e7be1b11686aec68fd220bba6b4502b5bbdc5c2960d847ee240113222c6bd919",
    },
    {
        "role": "revision_002_verifier",
        "boundary_tag": "exp3-v2-evaluation-harness-frozen-002",
        "path": "phase_b/exp3_v2/verify_exp3v2_evaluation.py",
        "size_bytes": 6318,
        "sha256": "c20de70519d70d3634e808b662a08ca8936af863adba44377c667418d42d8e1c",
    },
    {
        "role": "frozen_scientific_config",
        "boundary_tag": "exp3-v2-evaluation-harness-frozen-002",
        "path": "phase_b/exp3_v2/EXP3_V2_EVALUATION_CONFIG_001.json",
        "size_bytes": 1835,
        "sha256": "5d836027adb493c7c12d3fa495696960a1f208ddaa9b102a7d1d5ba551b6ffdb",
    },
    {
        "role": "revision_001_failure_json",
        "boundary_tag": "exp3-v2-evaluation-harness-frozen-002",
        "path": "phase_b/exp3_v2/EXP3_V2_EVALUATION_REV001_EXECUTION_FAILURE.json",
        "size_bytes": 3209,
        "sha256": "b6233abefada6334bc3ea3b20aa372c9da6fe396f556a9306d366730a3115433",
    },
    {
        "role": "revision_001_failure_markdown",
        "boundary_tag": "exp3-v2-evaluation-harness-frozen-002",
        "path": "phase_b/exp3_v2/EXP3_V2_EVALUATION_REV001_EXECUTION_FAILURE.md",
        "size_bytes": 2934,
        "sha256": "192de37a6a3545aa9a935ab459f9916f8deb5b6f02ea4c398125993165a7f042",
    },
]

EXPECTED_EXECUTION_PROVENANCE = {
    "revision_001": {
        "evaluator_invocations": 1,
        "default_rng_invocations": 1,
        "seed": 320031,
        "draws": 10000,
        "retries": 0,
        "verifier_invocations": 0,
        "output_files": 0,
        "failed_after_in_memory_before_write": True,
        "exhausted": True,
        "replay_eligible": False,
    },
    "revision_002": {
        "evaluator_invocations": 1,
        "replays": 1,
        "retries": 0,
        "default_rng_invocations": 1,
        "seed": 320031,
        "draws": 10000,
        "output_files": 3,
        "exit_code": 0,
        "status": "PASS",
    },
    "separate_verifier": {
        "invocations": 1,
        "retries": 0,
        "exit_code": 0,
        "status": "PASS",
        "bootstrap_recomputations": 1,
        "default_rng_invocations": 1,
        "seed": 320031,
        "draws": 10000,
        "byte_identity_before_after": True,
    },
    "outcome_based_selection": False,
}


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False) + "\n"
    ).encode("utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_output(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def validate_manifest(manifest: dict[str, Any], schema_path: Path, mode: str) -> None:
    jsonschema.Draft202012Validator(load_json(schema_path)).validate(manifest)
    expected_status = DRAFT_STATUS if mode == "review_draft" else FROZEN_STATUS
    if manifest["status"] != expected_status:
        raise RuntimeError("manifest status differs from verifier mode")
    if manifest["prospective_tag"] != TAG:
        raise RuntimeError("prospective tag differs from frozen contract")
    if manifest["governance"]["file_allowlist"] != GOVERNANCE_ALLOWLIST:
        raise RuntimeError("governance allowlist differs from independent constants")
    if manifest["boundary_tags"] != EXPECTED_BOUNDARIES:
        raise RuntimeError("boundary bindings differ from independent constants")
    if manifest["critical_artifacts"] != EXPECTED_CRITICAL_ARTIFACTS:
        raise RuntimeError("critical artifact bindings differ from constants")
    if manifest["execution_provenance"] != EXPECTED_EXECUTION_PROVENANCE:
        raise RuntimeError("execution provenance differs from frozen facts")
    payload = manifest["payload"]
    if payload["artifacts"] != EXPECTED_ARTIFACTS:
        raise RuntimeError("payload bindings differ from independent constants")
    if (
        payload["path_count"] != 3
        or payload["total_size_bytes"] != EXPECTED_TOTAL_BYTES
    ):
        raise RuntimeError("payload counts differ from frozen constants")
    if payload["inventory_sha256"] != EXPECTED_INVENTORY_SHA256:
        raise RuntimeError("payload inventory digest differs from frozen constant")
    if payload["concatenated_bytes_sha256"] != EXPECTED_CONCATENATED_SHA256:
        raise RuntimeError("payload concatenated digest differs from frozen constant")
    required_tags = [item["name"] for item in EXPECTED_BOUNDARIES] + [TAG]
    if manifest["portable_verification"]["required_annotated_tags"] != required_tags:
        raise RuntimeError("required detached-tag order differs from contract")
    nonself = manifest["non_self_referential"]
    if nonself != {
        "manifest_sha256_recorded": False,
        "governance_commit_recorded": False,
        "tag_object_recorded": False,
        "payload_commit_may_be_recorded": True,
    }:
        raise RuntimeError("non-self-reference declaration differs")
    if mode == "review_draft":
        if manifest["tag_created"] or manifest["human_freeze_approval"] is not None:
            raise RuntimeError("draft contains freeze authorization")
        if manifest["governance"]["actual_payload_commit"] is not None:
            raise RuntimeError("draft records an actual payload commit")
    elif mode == "rehearsal_final":
        approval = manifest["human_freeze_approval"]
        if approval["scope"] != "SYNTHETIC_ISOLATED_REHEARSAL_ONLY":
            raise RuntimeError("rehearsal mode requires synthetic-only approval")
    else:
        approval = manifest["human_freeze_approval"]
        if approval["scope"] != "EXP3_V2_EVALUATION_RESULTS_FREEZE_001":
            raise RuntimeError("public verification requires real human approval")


def build_inventory(payload_root: Path) -> list[dict[str, Any]]:
    if payload_root.is_symlink() or not payload_root.is_dir():
        raise RuntimeError("payload root is missing, non-directory, or symlinked")
    result: list[dict[str, Any]] = []
    for path in sorted(payload_root.rglob("*")):
        if path.is_symlink():
            raise RuntimeError(f"symlink in payload: {path}")
        mode = path.stat().st_mode
        if path.is_dir():
            if not stat.S_ISDIR(mode):
                raise RuntimeError("non-directory payload container")
            continue
        if not path.is_file() or not stat.S_ISREG(mode):
            raise RuntimeError(f"non-regular payload entry: {path}")
        relative = path.relative_to(payload_root).as_posix()
        result.append(
            {
                "path": relative,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return result


def verify_payload(manifest: dict[str, Any], payload_root: Path) -> dict[str, Any]:
    actual = build_inventory(payload_root)
    if actual != EXPECTED_ARTIFACTS:
        raise RuntimeError("payload bytes differ from independent frozen constants")
    if manifest["payload"]["artifacts"] != actual:
        raise RuntimeError("manifest payload inventory differs from actual bytes")
    if sum(item["size_bytes"] for item in actual) != EXPECTED_TOTAL_BYTES:
        raise RuntimeError("payload total byte count mismatch")
    inventory_digest = hashlib.sha256(canonical_json_bytes(actual)).hexdigest()
    if inventory_digest != EXPECTED_INVENTORY_SHA256:
        raise RuntimeError("payload inventory digest mismatch")
    concatenated = hashlib.sha256()
    for item in actual:
        path = payload_root / item["path"]
        with path.open("rb") as stream:
            prefix = stream.read(len(LFS_HEADER))
            if prefix == LFS_HEADER:
                raise RuntimeError(f"Git LFS pointer prohibited: {item['path']}")
            concatenated.update(prefix)
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                concatenated.update(chunk)
    if concatenated.hexdigest() != EXPECTED_CONCATENATED_SHA256:
        raise RuntimeError("concatenated payload digest mismatch")
    internal = load_json(payload_root / "exp3v2_evaluation_output_hash_manifest.json")
    if internal.get("artifact_count") != 2:
        raise RuntimeError("internal output manifest count mismatch")
    if internal.get("artifacts") != EXPECTED_ARTIFACTS[:2]:
        raise RuntimeError("internal output manifest artifact binding mismatch")
    internal_inventory = "".join(
        f"{item['path']}\0{item['size_bytes']}\0{item['sha256']}\n"
        for item in internal["artifacts"]
    ).encode("utf-8")
    digest = hashlib.sha256(internal_inventory).hexdigest()
    if digest != EXPECTED_INTERNAL_INVENTORY_SHA256:
        raise RuntimeError("internal inventory digest differs from frozen constant")
    if internal.get("inventory_sha256") != digest:
        raise RuntimeError("internal output manifest digest mismatch")
    return {
        "path_count": 3,
        "total_size_bytes": EXPECTED_TOTAL_BYTES,
        "inventory_sha256": inventory_digest,
        "concatenated_bytes_sha256": concatenated.hexdigest(),
    }


def verify_runtime() -> None:
    observed = {
        "python": sys.version.split()[0],
        "numpy": importlib.metadata.version("numpy"),
        "jsonschema": importlib.metadata.version("jsonschema"),
    }
    expected = {"python": "3.13.9", "numpy": "2.5.2", "jsonschema": "4.25.0"}
    if observed != expected:
        raise RuntimeError(f"runtime mismatch: {observed}")
    if Path(os.path.realpath(sys.executable)) != Path("/opt/anaconda3/bin/python3.13"):
        raise RuntimeError("canonical Python executable mismatch")


def verify_tag_checkout(root: Path, binding: dict[str, Any]) -> None:
    if git_output(root, "cat-file", "-t", f"refs/tags/{binding['name']}") != "tag":
        raise RuntimeError(f"tag is not annotated: {binding['name']}")
    if (
        git_output(root, "rev-parse", f"refs/tags/{binding['name']}")
        != binding["tag_object"]
    ):
        raise RuntimeError(f"tag object mismatch: {binding['name']}")
    if (
        git_output(root, "rev-parse", f"refs/tags/{binding['name']}^{{}}")
        != binding["peeled_commit"]
    ):
        raise RuntimeError(f"tag target mismatch: {binding['name']}")
    if git_output(root, "rev-parse", "HEAD") != binding["peeled_commit"]:
        raise RuntimeError(f"checkout HEAD mismatch: {binding['name']}")
    symbolic = subprocess.run(
        ["git", "symbolic-ref", "-q", "HEAD"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if symbolic.returncode == 0:
        raise RuntimeError(f"checkout is not detached: {binding['name']}")
    if git_output(root, "status", "--porcelain=v1", "--untracked-files=all"):
        raise RuntimeError(f"checkout is not clean: {binding['name']}")
    if git_output(root, "for-each-ref", "--format=%(refname)", "refs/heads"):
        raise RuntimeError(f"local branch exists: {binding['name']}")
    if git_output(root, "for-each-ref", "--format=%(refname)", "refs/remotes"):
        raise RuntimeError(f"remote-tracking ref exists: {binding['name']}")


def verify_boundaries(manifest: dict[str, Any], roots: dict[str, Path]) -> None:
    expected_by_role = {item["role"]: item for item in EXPECTED_BOUNDARIES}
    if set(roots) != set(expected_by_role):
        raise RuntimeError("boundary root role set mismatch")
    if manifest["boundary_tags"] != EXPECTED_BOUNDARIES:
        raise RuntimeError("manifest boundary list mismatch")
    by_tag: dict[str, Path] = {}
    for role, root in roots.items():
        binding = expected_by_role[role]
        verify_tag_checkout(root, binding)
        manifest_path = root / binding["manifest_path"]
        if manifest_path.is_symlink() or not manifest_path.is_file():
            raise RuntimeError(f"boundary manifest missing: {role}")
        if sha256_file(manifest_path) != binding["manifest_sha256"]:
            raise RuntimeError(f"boundary manifest hash mismatch: {role}")
        by_tag[binding["name"]] = root
    for item in EXPECTED_CRITICAL_ARTIFACTS:
        path = by_tag[item["boundary_tag"]] / item["path"]
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(f"critical artifact missing: {item['role']}")
        if (
            path.stat().st_size != item["size_bytes"]
            or sha256_file(path) != item["sha256"]
        ):
            raise RuntimeError(f"critical artifact mismatch: {item['role']}")


def verify_governance_artifacts(manifest: dict[str, Any], freeze_root: Path) -> None:
    expected_paths = set(GOVERNANCE_ALLOWLIST) - {MANIFEST_RELATIVE.as_posix()}
    recorded = manifest["governance"]["non_manifest_artifacts"]
    if {item["path"] for item in recorded} != expected_paths:
        raise RuntimeError("non-manifest governance hash set mismatch")
    for item in recorded:
        path = freeze_root / item["path"]
        if path.is_symlink() or not path.is_file():
            raise RuntimeError(f"governance artifact missing: {item['path']}")
        if (
            path.stat().st_size != item["size_bytes"]
            or sha256_file(path) != item["sha256"]
        ):
            raise RuntimeError(f"governance artifact hash mismatch: {item['path']}")


def verify_topology(manifest: dict[str, Any], freeze_root: Path) -> dict[str, str]:
    head = git_output(freeze_root, "rev-parse", "HEAD")
    tag_object = git_output(freeze_root, "rev-parse", f"refs/tags/{TAG}")
    if git_output(freeze_root, "cat-file", "-t", tag_object) != "tag":
        raise RuntimeError("results tag is not annotated")
    if git_output(freeze_root, "rev-parse", f"refs/tags/{TAG}^{{}}") != head:
        raise RuntimeError("results tag does not target governance commit")
    if git_output(freeze_root, "for-each-ref", "--format=%(refname)", "refs/heads"):
        raise RuntimeError("branch ref exists in verification repository")
    if git_output(freeze_root, "for-each-ref", "--format=%(refname)", "refs/remotes"):
        raise RuntimeError("remote-tracking ref exists in verification repository")
    if git_output(freeze_root, "status", "--porcelain=v1", "--untracked-files=all"):
        raise RuntimeError("results checkout is not clean")
    parents = git_output(freeze_root, "rev-list", "--parents", "-n", "1", head).split()
    if len(parents) != 2:
        raise RuntimeError("governance commit does not have exactly one parent")
    payload_commit = parents[1]
    if payload_commit != manifest["governance"]["actual_payload_commit"]:
        raise RuntimeError("governance parent differs from manifest payload commit")
    if (
        len(
            git_output(
                freeze_root, "rev-list", "--parents", "-n", "1", payload_commit
            ).split()
        )
        != 1
    ):
        raise RuntimeError("payload commit is not parentless")
    expected_payload_paths = {
        "evaluation_outputs/" + item["path"] for item in EXPECTED_ARTIFACTS
    }
    payload_paths = set(
        git_output(
            freeze_root, "ls-tree", "-r", "--name-only", payload_commit
        ).splitlines()
    )
    if payload_paths != expected_payload_paths or len(payload_paths) != 3:
        raise RuntimeError("payload commit path set mismatch")
    diff = git_output(
        freeze_root, "diff-tree", "--no-commit-id", "--name-status", "-r", head
    ).splitlines()
    additions = {line.split("\t", 1)[1] for line in diff if line.startswith("A\t")}
    if additions != set(GOVERNANCE_ALLOWLIST) or len(diff) != 5:
        raise RuntimeError("governance commit is not an exact additions-only diff")
    final_paths = set(
        git_output(freeze_root, "ls-tree", "-r", "--name-only", head).splitlines()
    )
    if (
        final_paths != expected_payload_paths | set(GOVERNANCE_ALLOWLIST)
        or len(final_paths) != 8
    ):
        raise RuntimeError("governance tree path set mismatch")
    for commit, paths in ((payload_commit, payload_paths), (head, final_paths)):
        for path in paths:
            if git_output(freeze_root, "cat-file", "-t", f"{commit}:{path}") != "blob":
                raise RuntimeError(f"non-blob tree entry: {path}")
    return {
        "payload_commit": payload_commit,
        "payload_tree": git_output(
            freeze_root, "rev-parse", f"{payload_commit}^{{tree}}"
        ),
        "governance_commit": head,
        "governance_tree": git_output(freeze_root, "rev-parse", "HEAD^{tree}"),
        "tag_object": tag_object,
    }


def run_frozen_semantic_verifier(roots: dict[str, Path], payload_root: Path) -> None:
    command = [
        str(RUNTIME),
        str(roots["evaluation_harness_revision_002"] / FROZEN_SEMANTIC_VERIFIER),
        "--harness-manifest",
        str(
            roots["evaluation_harness_revision_002"]
            / EXPECTED_BOUNDARIES[-1]["manifest_path"]
        ),
        "--source-root",
        str(roots["source"]),
        "--data-root",
        str(roots["data"]),
        "--verbalization-harness-root",
        str(roots["verbalization_harness"]),
        "--verbalizations-root",
        str(roots["verbalizations"]),
        "--inference-harness-root",
        str(roots["inference_harness"]),
        "--authorization-root",
        str(roots["execution_authorization"]),
        "--inference-root",
        str(roots["inference_outputs"]),
        "--output-root",
        str(payload_root),
    ]
    result = subprocess.run(
        command,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError("frozen Revision 002 semantic verifier failed")
    observed = json.loads(result.stdout)
    if observed.get("status") != "PASS" or observed.get("output_files") != 3:
        raise RuntimeError("frozen semantic verifier returned a non-PASS result")


def verify(
    *,
    manifest_path: Path,
    payload_root: Path,
    mode: str,
    freeze_root: Path | None = None,
    roots: dict[str, Path] | None = None,
) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    schema_root = manifest_path.parents[2] if freeze_root is None else freeze_root
    validate_manifest(manifest, schema_root / SCHEMA_RELATIVE, mode)
    verify_runtime()
    payload_result = verify_payload(manifest, payload_root)
    topology = None
    semantic = "NOT_RUN_REVIEW_ONLY"
    if mode != "review_draft":
        if freeze_root is None:
            raise RuntimeError("final modes require --freeze-root")
        expected_manifest = freeze_root / MANIFEST_RELATIVE
        if manifest_path.resolve() != expected_manifest.resolve():
            raise RuntimeError("manifest path differs from final tree contract")
        if payload_root.resolve() != (freeze_root / "evaluation_outputs").resolve():
            raise RuntimeError("payload root differs from final tree contract")
        topology = verify_topology(manifest, freeze_root)
        verify_governance_artifacts(manifest, freeze_root)
        if mode == "rehearsal_final":
            semantic = "NOT_RUN_SYNTHETIC_REHEARSAL_SCOPE"
        else:
            if roots is None:
                raise RuntimeError(
                    "public final verification requires all boundary roots"
                )
            verify_boundaries(manifest, roots)
            run_frozen_semantic_verifier(roots, payload_root)
            semantic = "PASS"
    return {
        "status": "PASS",
        "mode": mode,
        "path_count": payload_result["path_count"],
        "total_size_bytes": payload_result["total_size_bytes"],
        "inventory_sha256": payload_result["inventory_sha256"],
        "concatenated_bytes_sha256": payload_result["concatenated_bytes_sha256"],
        "topology": topology,
        "semantic_verification": semantic,
        "scientific_values_reported": False,
    }


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--payload-root", type=Path)
    parser.add_argument("--freeze-root", type=Path)
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--review-draft", action="store_true")
    modes.add_argument("--rehearsal-final", action="store_true")
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--data-root", type=Path)
    parser.add_argument("--verbalization-harness-root", type=Path)
    parser.add_argument("--verbalizations-root", type=Path)
    parser.add_argument("--inference-harness-root", type=Path)
    parser.add_argument("--authorization-root", type=Path)
    parser.add_argument("--inference-root", type=Path)
    parser.add_argument("--evaluation-harness-rev001-root", type=Path)
    parser.add_argument("--evaluation-harness-rev002-root", type=Path)
    args = parser.parse_args(argv)
    if args.review_draft:
        if args.payload_root is None or args.freeze_root is not None:
            parser.error(
                "--review-draft requires --payload-root and forbids --freeze-root"
            )
        args.mode = "review_draft"
    else:
        if args.freeze_root is None or args.payload_root is not None:
            parser.error(
                "final modes require --freeze-root and derive the payload root"
            )
        args.payload_root = args.freeze_root / "evaluation_outputs"
        args.mode = "rehearsal_final" if args.rehearsal_final else "public_final"
    root_values = {
        "source": args.source_root,
        "data": args.data_root,
        "verbalization_harness": args.verbalization_harness_root,
        "verbalizations": args.verbalizations_root,
        "inference_harness": args.inference_harness_root,
        "execution_authorization": args.authorization_root,
        "inference_outputs": args.inference_root,
        "evaluation_harness_revision_001": args.evaluation_harness_rev001_root,
        "evaluation_harness_revision_002": args.evaluation_harness_rev002_root,
    }
    if args.mode == "public_final":
        if any(value is None for value in root_values.values()):
            parser.error("public final verification requires all nine boundary roots")
        args.roots = root_values
    else:
        if any(value is not None for value in root_values.values()):
            parser.error("review and rehearsal modes forbid boundary-root arguments")
        args.roots = None
    return args


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    result = verify(
        manifest_path=args.manifest.resolve(),
        payload_root=args.payload_root.resolve(),
        mode=args.mode,
        freeze_root=args.freeze_root.resolve() if args.freeze_root else None,
        roots=args.roots,
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
