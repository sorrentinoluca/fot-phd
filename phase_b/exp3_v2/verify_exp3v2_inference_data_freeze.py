#!/usr/bin/env python3
"""Portable verifier for the disconnected EXP3_V2 inference-data freeze."""

from __future__ import annotations

import argparse
from collections.abc import Iterable
import hashlib
import importlib
import json
from pathlib import Path
import re
import stat
import subprocess
import sys
from typing import Any

import jsonschema


TAG = "exp3-v2-inference-frozen-001"
SCHEMA_RELATIVE_PATH = Path(
    "phase_b/exp3_v2/inference_schemas/"
    "exp3v2_inference_data_freeze_manifest.schema.json"
)
HARNESS_MANIFEST_RELATIVE_PATH = Path(
    "phase_b/exp3_v2/EXP3_V2_INFERENCE_HARNESS_MANIFEST_001.json"
)
EXPECTED_PAYLOAD_COUNT = 3248
EXPECTED_GOVERNANCE_COUNT = 3253
EXPECTED_TOTAL_BYTES = 20718869
EXPECTED_OUTPUT_INVENTORY = (
    "3343f6315a5f8cd9e8d11a18fe26c13e70de91a9479a5e1a3ee2ab2c9281f1ea"
)
EXPECTED_COMPLETE_INVENTORY = (
    "7eeb7bb53340d98236082bf64d83f71d2e6cc59c307389f566eabf367b709e72"
)
EXPECTED_PRINCIPAL = {
    "execution_metadata.json": (
        "0ba340a7f3e733e3677b914bbe316167f14fc0ba7ffdb86939e43d98cc0e5208"
    ),
    "repetition_records.jsonl": (
        "0bc8d76ea5d0d832b96e1c8afb2ac3caf67cad95a131ffa77cc0cd25069ce04e"
    ),
    "aggregate_records.jsonl": (
        "0fac87d1cf51597c61ae7be176970990001bed5b015756594a848d1e1bcca656"
    ),
    "inference_output_hash_manifest.json": (
        "64ea673252bfbf453161aa60bcbc7dfc430d4d693f25f2faed99c2ad42e3505a"
    ),
}
FORBIDDEN_JSON_KEYS = {
    "ground_truth",
    "ground_truth_label",
    "true_label",
    "real_label",
    "fault_identity",
    "real_to_opaque",
    "real_to_opaque_mapping",
    "evaluator_mapping",
    "evaluator_mappings",
    "api_key",
    "openai_api_key",
    "authorization_header",
    "credential",
    "credentials",
    "secret",
}
FORBIDDEN_EXACT_BYTES = (
    b"OPENAI_API_KEY",
    b"Authorization: Bearer",
    b"authorization: bearer",
    b'"api_key"',
    b'"openai_api_key"',
    b'"real_to_opaque"',
    b'"evaluator_mapping"',
)
OPENAI_SECRET_PATTERN = re.compile(rb"(?<![A-Za-z0-9_])sk-(?:proj-)?[A-Za-z0-9_-]{20,}")
LFS_HEADER = b"version https://git-lfs.github.com/spec/v1"


def canonical_json_bytes(value: Any) -> bytes:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
            allow_nan=False,
        )
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def git_output(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def validate_manifest_schema(manifest: dict[str, Any], schema_path: Path) -> None:
    schema = load_json(schema_path)
    jsonschema.Draft202012Validator(schema).validate(manifest)


def validate_relative_path(value: str) -> Path:
    path = Path(value)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise RuntimeError(f"non-canonical payload path: {value}")
    if str(path) != value or value.startswith("./"):
        raise RuntimeError(f"non-normalized payload path: {value}")
    return path


def build_file_inventory(payload_root: Path) -> list[dict[str, Any]]:
    if not payload_root.is_dir() or payload_root.is_symlink():
        raise RuntimeError("payload root is missing, non-directory, or symlinked")
    inventory: list[dict[str, Any]] = []
    for path in sorted(payload_root.rglob("*")):
        if path.is_symlink():
            raise RuntimeError(f"symlink in payload: {path.relative_to(payload_root)}")
        mode = path.stat().st_mode
        if path.is_dir():
            if not stat.S_ISDIR(mode):
                raise RuntimeError("non-directory container in payload")
            continue
        if not path.is_file() or not stat.S_ISREG(mode):
            raise RuntimeError(f"non-regular payload entry: {path}")
        relative = path.relative_to(payload_root).as_posix()
        inventory.append(
            {
                "path": relative,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    return inventory


def verify_payload_inventory(
    manifest: dict[str, Any], payload_root: Path
) -> dict[str, Any]:
    payload = manifest["payload"]
    expected = payload["artifacts"]
    if len(expected) != EXPECTED_PAYLOAD_COUNT:
        raise RuntimeError("manifest does not contain exactly 3,248 artifacts")
    if len({item["path"] for item in expected}) != len(expected):
        raise RuntimeError("duplicate artifact path in manifest")
    for item in expected:
        validate_relative_path(item["path"])
    actual = build_file_inventory(payload_root)
    if actual != expected:
        expected_by_path = {item["path"]: item for item in expected}
        actual_by_path = {item["path"]: item for item in actual}
        missing = sorted(set(expected_by_path) - set(actual_by_path))
        extra = sorted(set(actual_by_path) - set(expected_by_path))
        altered = sorted(
            path
            for path in set(expected_by_path) & set(actual_by_path)
            if expected_by_path[path] != actual_by_path[path]
        )
        raise RuntimeError(
            f"payload inventory mismatch: missing={missing}, extra={extra}, "
            f"altered={altered}"
        )
    total_bytes = sum(item["size_bytes"] for item in actual)
    if (
        total_bytes != EXPECTED_TOTAL_BYTES
        or total_bytes != payload["total_size_bytes"]
    ):
        raise RuntimeError("payload total byte count mismatch")
    complete_digest = sha256_bytes(canonical_json_bytes(actual))
    if complete_digest != EXPECTED_COMPLETE_INVENTORY:
        raise RuntimeError("complete 3,248-file inventory digest mismatch")

    by_path = {item["path"]: item for item in actual}
    if payload["principal_sha256"] != EXPECTED_PRINCIPAL:
        raise RuntimeError("principal hash binding differs from frozen contract")
    for relative, expected_sha in EXPECTED_PRINCIPAL.items():
        if by_path.get(relative, {}).get("sha256") != expected_sha:
            raise RuntimeError(f"principal artifact mismatch: {relative}")

    output_manifest = load_json(payload_root / "inference_output_hash_manifest.json")
    internal_artifacts = output_manifest["artifacts"]
    if len(internal_artifacts) != EXPECTED_PAYLOAD_COUNT - 1:
        raise RuntimeError("internal output inventory count mismatch")
    internal_digest = sha256_bytes(canonical_json_bytes(internal_artifacts))
    if internal_digest != EXPECTED_OUTPUT_INVENTORY:
        raise RuntimeError("frozen output inventory digest mismatch")
    if output_manifest["inventory_sha256"] != internal_digest:
        raise RuntimeError("output manifest does not bind its artifact inventory")
    expected_internal_paths = {item["path"] for item in internal_artifacts}
    if expected_internal_paths | {"inference_output_hash_manifest.json"} != set(
        by_path
    ):
        raise RuntimeError("internal output inventory path set mismatch")
    for item in internal_artifacts:
        if by_path[item["path"]] != item:
            raise RuntimeError(f"internal artifact mismatch: {item['path']}")
    for item in actual:
        path = payload_root / item["path"]
        with path.open("rb") as stream:
            if stream.read(len(LFS_HEADER)) == LFS_HEADER:
                raise RuntimeError(f"Git LFS pointer prohibited: {item['path']}")
    return {
        "path_count": len(actual),
        "total_size_bytes": total_bytes,
        "complete_file_inventory_sha256": complete_digest,
        "frozen_output_inventory_sha256": internal_digest,
    }


def _walk_keys(value: Any, found: set[str]) -> None:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key.lower() in FORBIDDEN_JSON_KEYS:
                found.add(key)
            _walk_keys(nested, found)
    elif isinstance(value, list):
        for nested in value:
            _walk_keys(nested, found)


def verify_no_prohibited_persistence(payload_root: Path) -> dict[str, int]:
    forbidden_keys: set[str] = set()
    exact_pattern_hits = 0
    credential_pattern_hits = 0
    for path in sorted(payload_root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        data = path.read_bytes()
        exact_pattern_hits += sum(
            data.count(pattern) for pattern in FORBIDDEN_EXACT_BYTES
        )
        credential_pattern_hits += len(OPENAI_SECRET_PATTERN.findall(data))
        if path.suffix == ".json":
            _walk_keys(json.loads(data), forbidden_keys)
        elif path.suffix == ".jsonl":
            for line in data.splitlines():
                if line:
                    _walk_keys(json.loads(line), forbidden_keys)
    if forbidden_keys or exact_pattern_hits or credential_pattern_hits:
        raise RuntimeError(
            "prohibited persistence detected: "
            f"keys={sorted(forbidden_keys)}, exact_patterns={exact_pattern_hits}, "
            f"credential_patterns={credential_pattern_hits}"
        )
    output_manifest = load_json(payload_root / "inference_output_hash_manifest.json")
    metadata = load_json(payload_root / "execution_metadata.json")
    if output_manifest["ground_truth_included"] is not False:
        raise RuntimeError("output manifest claims ground truth is included")
    if output_manifest["metrics_calculated"] is not False:
        raise RuntimeError("output manifest claims metrics were calculated")
    if metadata["ground_truth_joined"] is not False:
        raise RuntimeError("execution metadata claims ground truth was joined")
    if metadata["metrics_calculated"] is not False:
        raise RuntimeError("execution metadata claims metrics were calculated")
    return {
        "forbidden_json_key_hits": 0,
        "forbidden_exact_pattern_hits": 0,
        "credential_pattern_hits": 0,
    }


def verify_annotated_tag(
    root: Path, name: str, expected_object: str, expected_commit: str
) -> None:
    object_id = git_output(root, "rev-parse", f"refs/tags/{name}")
    if object_id != expected_object:
        raise RuntimeError(f"tag object mismatch: {name}")
    if git_output(root, "cat-file", "-t", object_id) != "tag":
        raise RuntimeError(f"tag is not annotated: {name}")
    if git_output(root, "rev-parse", f"refs/tags/{name}^{{commit}}") != expected_commit:
        raise RuntimeError(f"tag target mismatch: {name}")


def verify_detached_clean(root: Path, expected_commit: str) -> None:
    if (
        Path(git_output(root, "rev-parse", "--show-toplevel")).resolve()
        != root.resolve()
    ):
        raise RuntimeError(f"not a worktree root: {root}")
    if git_output(root, "rev-parse", "HEAD") != expected_commit:
        raise RuntimeError(f"checkout commit mismatch: {root}")
    symbolic = subprocess.run(
        ["git", "symbolic-ref", "-q", "HEAD"],
        cwd=root,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    if symbolic.returncode == 0:
        raise RuntimeError(f"checkout is not detached: {root}")
    if git_output(root, "status", "--porcelain=v1", "--untracked-files=all"):
        raise RuntimeError(f"checkout is not clean: {root}")


def verify_upstream_bindings(manifest: dict[str, Any], roots: dict[str, Path]) -> None:
    tag_bindings = {item["name"]: item for item in manifest["upstream_tags"]}
    if set(tag_bindings) != set(roots):
        raise RuntimeError("upstream checkout set differs from manifest")
    for name, root in roots.items():
        binding = tag_bindings[name]
        verify_annotated_tag(
            root, name, binding["tag_object"], binding["peeled_commit"]
        )
        verify_detached_clean(root, binding["peeled_commit"])
    manifest_bindings = manifest["upstream_manifest_bindings"]
    if {item["tag"] for item in manifest_bindings} != set(roots):
        raise RuntimeError("upstream manifest-binding tag set mismatch")
    for binding in manifest_bindings:
        path = roots[binding["tag"]] / binding["path"]
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"bound manifest missing or symlinked: {path}")
        if sha256_file(path) != binding["sha256"]:
            raise RuntimeError(f"bound manifest hash mismatch: {path}")


def verify_topology(manifest: dict[str, Any], freeze_root: Path) -> dict[str, str]:
    head = git_output(freeze_root, "rev-parse", "HEAD")
    tag_object = git_output(freeze_root, "rev-parse", f"refs/tags/{TAG}")
    if git_output(freeze_root, "cat-file", "-t", tag_object) != "tag":
        raise RuntimeError("final tag is not annotated")
    if git_output(freeze_root, "rev-parse", f"refs/tags/{TAG}^{{commit}}") != head:
        raise RuntimeError("final tag does not target governance commit")
    verify_detached_clean(freeze_root, head)
    if git_output(freeze_root, "for-each-ref", "--format=%(refname)", "refs/heads"):
        raise RuntimeError("branch ref exists in tag-only verification repository")

    parent_line = git_output(
        freeze_root, "rev-list", "--parents", "-n", "1", head
    ).split()
    if len(parent_line) != 2:
        raise RuntimeError("governance commit does not have exactly one parent")
    payload_commit = parent_line[1]
    if payload_commit != manifest["governance"]["actual_payload_commit"]:
        raise RuntimeError("governance parent differs from recorded payload commit")
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
        "inference_outputs/" + item["path"] for item in manifest["payload"]["artifacts"]
    }
    payload_paths = set(
        git_output(
            freeze_root, "ls-tree", "-r", "--name-only", payload_commit
        ).splitlines()
    )
    if payload_paths != expected_payload_paths:
        raise RuntimeError("payload commit tree differs from exact allowlist")
    if len(payload_paths) != EXPECTED_PAYLOAD_COUNT:
        raise RuntimeError("payload commit tree count mismatch")

    governance_allowlist = set(manifest["governance"]["file_allowlist"])
    diff_lines = git_output(
        freeze_root, "diff-tree", "--no-commit-id", "--name-status", "-r", head
    ).splitlines()
    additions = {
        line.split("\t", 1)[1]
        for line in diff_lines
        if line.startswith("A\t") and "\t" in line
    }
    if additions != governance_allowlist or len(diff_lines) != len(additions):
        raise RuntimeError("governance commit is not an additions-only allowlist diff")
    governance_paths = set(
        git_output(freeze_root, "ls-tree", "-r", "--name-only", head).splitlines()
    )
    if governance_paths != expected_payload_paths | governance_allowlist:
        raise RuntimeError("governance tree path set mismatch")
    if len(governance_paths) != EXPECTED_GOVERNANCE_COUNT:
        raise RuntimeError("governance tree count mismatch")
    return {
        "payload_commit": payload_commit,
        "governance_commit": head,
        "tag_object": tag_object,
        "payload_tree": git_output(
            freeze_root, "rev-parse", f"{payload_commit}^{{tree}}"
        ),
        "governance_tree": git_output(freeze_root, "rev-parse", "HEAD^{tree}"),
    }


def run_frozen_verifier(
    payload_root: Path,
    harness_root: Path,
    verbalizations_root: Path,
) -> dict[str, Any]:
    if str(harness_root) not in sys.path:
        sys.path.insert(0, str(harness_root))
    runner = importlib.import_module("phase_b.exp3_v2.run_exp3v2_inference")
    frozen = importlib.import_module("phase_b.exp3_v2.verify_exp3v2_inference")
    runtime_validator = importlib.import_module(
        "phase_b.exp3_v2.validate_exp3v2_inference_runtime"
    )
    harness_manifest = runner.load_json(harness_root / HARNESS_MANIFEST_RELATIVE_PATH)
    runtime_validator.validate_runtime(
        harness_root / "phase_b/exp3_v2/EXP3_V2_INFERENCE_RUNTIME_LOCK_001.json"
    )
    schedule_path = harness_root / harness_manifest["schedule"]["path"]
    schedule = runner.load_json(schedule_path)
    schedule_sha256 = harness_manifest["schedule"]["sha256"]
    runner.validate_schedule(schedule, schedule_sha256)
    case_texts = runner.load_case_texts(harness_manifest, verbalizations_root)
    assets = runner.FrozenAssets(harness_root, case_texts)
    return frozen.verify_output_set(schedule, assets, payload_root, schedule_sha256)


def verify(
    *,
    manifest_path: Path,
    payload_root: Path,
    freeze_root: Path | None,
    review_draft: bool,
    source_root: Path,
    data_root: Path,
    verbalization_harness_root: Path,
    verbalizations_root: Path,
    harness_root: Path,
    authorization_root: Path,
) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    schema_root = freeze_root if freeze_root is not None else manifest_path.parents[2]
    schema_path = schema_root / SCHEMA_RELATIVE_PATH
    validate_manifest_schema(manifest, schema_path)
    expected_status = (
        "PENDING_HUMAN_INFERENCE_DATA_FREEZE"
        if review_draft
        else "FROZEN_BEFORE_EVALUATION"
    )
    if manifest["status"] != expected_status:
        raise RuntimeError("manifest status differs from verifier mode")
    if review_draft:
        if freeze_root is not None:
            raise RuntimeError("review-draft mode must not receive a freeze root")
    else:
        if freeze_root is None:
            raise RuntimeError("final verification requires a freeze root")
        expected_manifest_path = freeze_root / (
            "phase_b/exp3_v2/EXP3_V2_INFERENCE_DATA_FREEZE_MANIFEST_001.json"
        )
        if manifest_path.resolve() != expected_manifest_path.resolve():
            raise RuntimeError("final manifest path differs from frozen tree contract")
        if payload_root.resolve() != (freeze_root / "inference_outputs").resolve():
            raise RuntimeError("final payload root differs from frozen tree contract")

    roots = {
        "exp3-v2-heldout-frozen-002": source_root,
        "exp3-v2-heldout-data-frozen-001": data_root,
        "exp3-v2-verbalization-harness-frozen-001": verbalization_harness_root,
        "exp3-v2-verbalizations-frozen-001": verbalizations_root,
        "exp3-v2-inference-harness-frozen-001": harness_root,
        "exp3-v2-inference-execution-frozen-001": authorization_root,
    }
    verify_upstream_bindings(manifest, roots)
    inventory_result = verify_payload_inventory(manifest, payload_root)
    leakage_result = verify_no_prohibited_persistence(payload_root)
    frozen_result = run_frozen_verifier(
        payload_root,
        harness_root,
        verbalizations_root,
    )
    if frozen_result["status"] != "PASS":
        raise RuntimeError("frozen inference verifier did not pass")
    topology_result = (
        verify_topology(manifest, freeze_root) if freeze_root is not None else None
    )
    return {
        "status": "PASS",
        "mode": "review_draft" if review_draft else "frozen_tag",
        "path_count": inventory_result["path_count"],
        "total_size_bytes": inventory_result["total_size_bytes"],
        "complete_file_inventory_sha256": inventory_result[
            "complete_file_inventory_sha256"
        ],
        "frozen_output_inventory_sha256": inventory_result[
            "frozen_output_inventory_sha256"
        ],
        "repetition_records": frozen_result["repetition_records"],
        "aggregate_records": frozen_result["aggregate_records"],
        "condition_counts": frozen_result["condition_counts"],
        "leakage_scan": leakage_result,
        "topology": topology_result,
        "ground_truth_joined": False,
        "metrics_calculated": False,
    }


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--payload-root", type=Path)
    parser.add_argument("--freeze-root", type=Path)
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--verbalization-harness-root", type=Path, required=True)
    parser.add_argument("--verbalizations-root", type=Path, required=True)
    parser.add_argument("--harness-root", type=Path, required=True)
    parser.add_argument("--authorization-root", type=Path, required=True)
    parser.add_argument("--review-draft", action="store_true")
    args = parser.parse_args(argv)
    if args.review_draft:
        if args.payload_root is None:
            parser.error("--review-draft requires --payload-root")
    else:
        if args.freeze_root is None:
            parser.error("final verification requires --freeze-root")
        if args.payload_root is not None:
            parser.error("final verification derives payload root from --freeze-root")
        args.payload_root = args.freeze_root / "inference_outputs"
    return args


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)
    result = verify(
        manifest_path=args.manifest,
        payload_root=args.payload_root,
        freeze_root=args.freeze_root,
        review_draft=args.review_draft,
        source_root=args.source_root,
        data_root=args.data_root,
        verbalization_harness_root=args.verbalization_harness_root,
        verbalizations_root=args.verbalizations_root,
        harness_root=args.harness_root,
        authorization_root=args.authorization_root,
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
