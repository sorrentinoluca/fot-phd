from __future__ import annotations

import importlib.util
from pathlib import Path
import subprocess
from unittest import mock

import pytest


ROOT = Path(__file__).resolve().parents[2]
VERIFIER_PATH = ROOT / "phase_b/exp3_v2/verify_exp3v2_inference_data_freeze.py"
SPEC = importlib.util.spec_from_file_location("inference_data_freeze", VERIFIER_PATH)
assert SPEC is not None and SPEC.loader is not None
verifier = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(verifier)


def write_bytes(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def synthetic_payload(root: Path) -> dict:
    write_bytes(root / "a.txt", b"alpha\n")
    first = {
        "path": "a.txt",
        "size_bytes": (root / "a.txt").stat().st_size,
        "sha256": verifier.sha256_file(root / "a.txt"),
    }
    internal = {
        "artifacts": [first],
        "inventory_sha256": verifier.sha256_bytes(
            verifier.canonical_json_bytes([first])
        ),
        "ground_truth_included": False,
        "metrics_calculated": False,
    }
    write_bytes(
        root / "inference_output_hash_manifest.json",
        verifier.canonical_json_bytes(internal),
    )
    artifacts = verifier.build_file_inventory(root)
    principal = {
        "inference_output_hash_manifest.json": verifier.sha256_file(
            root / "inference_output_hash_manifest.json"
        )
    }
    return {
        "payload": {
            "artifacts": artifacts,
            "total_size_bytes": sum(item["size_bytes"] for item in artifacts),
            "principal_sha256": principal,
        },
        "artifacts": artifacts,
        "principal": principal,
        "internal_digest": internal["inventory_sha256"],
        "complete_digest": verifier.sha256_bytes(
            verifier.canonical_json_bytes(artifacts)
        ),
    }


def inventory_patches(case: dict):
    return mock.patch.multiple(
        verifier,
        EXPECTED_PAYLOAD_COUNT=2,
        EXPECTED_TOTAL_BYTES=case["payload"]["total_size_bytes"],
        EXPECTED_OUTPUT_INVENTORY=case["internal_digest"],
        EXPECTED_COMPLETE_INVENTORY=case["complete_digest"],
        EXPECTED_PRINCIPAL=case["principal"],
    )


def test_inventory_accepts_relative_hash_bound_payload(tmp_path: Path) -> None:
    case = synthetic_payload(tmp_path)
    with inventory_patches(case):
        result = verifier.verify_payload_inventory(case, tmp_path)
    assert result["path_count"] == 2


@pytest.mark.parametrize("mutation", ["missing", "extra", "altered"])
def test_inventory_fails_closed_on_set_or_hash_change(
    tmp_path: Path, mutation: str
) -> None:
    case = synthetic_payload(tmp_path)
    if mutation == "missing":
        (tmp_path / "a.txt").unlink()
    elif mutation == "extra":
        write_bytes(tmp_path / "extra.txt", b"extra\n")
    else:
        write_bytes(tmp_path / "a.txt", b"altered\n")
    with inventory_patches(case), pytest.raises(RuntimeError):
        verifier.verify_payload_inventory(case, tmp_path)


def test_inventory_rejects_symlink(tmp_path: Path) -> None:
    case = synthetic_payload(tmp_path)
    (tmp_path / "link.txt").symlink_to(tmp_path / "a.txt")
    with inventory_patches(case), pytest.raises(RuntimeError, match="symlink"):
        verifier.verify_payload_inventory(case, tmp_path)


def test_inventory_rejects_lfs_pointer(tmp_path: Path) -> None:
    case = synthetic_payload(tmp_path)
    lfs = verifier.LFS_HEADER + b"\noid sha256:" + b"0" * 64 + b"\nsize 1\n"
    write_bytes(tmp_path / "a.txt", lfs)
    artifacts = verifier.build_file_inventory(tmp_path)
    internal = {
        "artifacts": [artifacts[0]],
        "inventory_sha256": verifier.sha256_bytes(
            verifier.canonical_json_bytes([artifacts[0]])
        ),
        "ground_truth_included": False,
        "metrics_calculated": False,
    }
    write_bytes(
        tmp_path / "inference_output_hash_manifest.json",
        verifier.canonical_json_bytes(internal),
    )
    artifacts = verifier.build_file_inventory(tmp_path)
    case["payload"]["artifacts"] = artifacts
    case["payload"]["total_size_bytes"] = sum(x["size_bytes"] for x in artifacts)
    case["principal"] = {
        "inference_output_hash_manifest.json": verifier.sha256_file(
            tmp_path / "inference_output_hash_manifest.json"
        )
    }
    case["payload"]["principal_sha256"] = case["principal"]
    case["internal_digest"] = internal["inventory_sha256"]
    case["complete_digest"] = verifier.sha256_bytes(
        verifier.canonical_json_bytes(artifacts)
    )
    with inventory_patches(case), pytest.raises(RuntimeError, match="LFS"):
        verifier.verify_payload_inventory(case, tmp_path)


def leakage_root(root: Path) -> None:
    write_bytes(
        root / "inference_output_hash_manifest.json",
        verifier.canonical_json_bytes(
            {"ground_truth_included": False, "metrics_calculated": False}
        ),
    )
    write_bytes(
        root / "execution_metadata.json",
        verifier.canonical_json_bytes(
            {"ground_truth_joined": False, "metrics_calculated": False}
        ),
    )


def test_leakage_scan_accepts_metadata_only(tmp_path: Path) -> None:
    leakage_root(tmp_path)
    assert verifier.verify_no_prohibited_persistence(tmp_path) == {
        "forbidden_json_key_hits": 0,
        "forbidden_exact_pattern_hits": 0,
        "credential_pattern_hits": 0,
    }


@pytest.mark.parametrize(
    "payload",
    [
        b'{"ground_truth":"prohibited"}\n',
        b'{"api_key":"prohibited"}\n',
        b'{"note":"Authorization: Bearer prohibited"}\n',
        b'{"note":"sk-proj-ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"}\n',
    ],
)
def test_leakage_scan_rejects_prohibited_persistence(
    tmp_path: Path, payload: bytes
) -> None:
    leakage_root(tmp_path)
    write_bytes(tmp_path / "bad.json", payload)
    with pytest.raises(RuntimeError, match="prohibited persistence"):
        verifier.verify_no_prohibited_persistence(tmp_path)


def run_git(root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=root,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    ).stdout.strip()


def test_disconnected_tag_only_topology(tmp_path: Path) -> None:
    run_git(tmp_path, "init", "-b", "payload-build")
    run_git(tmp_path, "config", "user.name", "EXP3V2 Test")
    run_git(tmp_path, "config", "user.email", "exp3v2-test@example.invalid")
    write_bytes(tmp_path / "inference_outputs/a.txt", b"a\n")
    write_bytes(tmp_path / "inference_outputs/b.txt", b"b\n")
    run_git(tmp_path, "add", "inference_outputs")
    run_git(tmp_path, "commit", "-m", "payload")
    payload_commit = run_git(tmp_path, "rev-parse", "HEAD")
    write_bytes(tmp_path / "gov.txt", b"governance\n")
    run_git(tmp_path, "add", "gov.txt")
    run_git(tmp_path, "commit", "-m", "governance")
    run_git(tmp_path, "tag", "-a", verifier.TAG, "-m", "test tag")
    run_git(tmp_path, "checkout", "--detach")
    run_git(tmp_path, "branch", "-D", "payload-build")
    manifest = {
        "governance": {
            "actual_payload_commit": payload_commit,
            "file_allowlist": ["gov.txt"],
        },
        "payload": {
            "artifacts": [
                {"path": "a.txt", "size_bytes": 2, "sha256": "0" * 64},
                {"path": "b.txt", "size_bytes": 2, "sha256": "0" * 64},
            ]
        },
    }
    with mock.patch.multiple(
        verifier, EXPECTED_PAYLOAD_COUNT=2, EXPECTED_GOVERNANCE_COUNT=3
    ):
        result = verifier.verify_topology(manifest, tmp_path)
    assert result["payload_commit"] == payload_commit


def test_absolute_source_provenance_is_not_used_for_resolution(tmp_path: Path) -> None:
    case = synthetic_payload(tmp_path)
    case["payload"][
        "authoritative_source_root_provenance"
    ] = "/host-specific/path/that/does/not/exist"
    with inventory_patches(case):
        assert verifier.verify_payload_inventory(case, tmp_path)["path_count"] == 2
