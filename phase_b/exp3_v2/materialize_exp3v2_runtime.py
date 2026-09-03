#!/usr/bin/env python3
"""Materialize the reviewed EXP3 V2 external runtime bundle fail-closed."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path, PurePosixPath
from typing import Any


EXPECTED_DEPENDENCY_PATHS = {
    "Mode1xInitial.mat",
    "Mode_1_Init.m",
    "MultiLoop_mode1.mdl",
    "TElib.mdl",
    "TEplot.m",
    "temexd_mod.c",
    "temexd_mod.mexmaca64",
    "teprob_mod.h",
}
HASH_LENGTH = 64


class MaterializationError(RuntimeError):
    """Raised when the external runtime bundle is not exactly allowlisted."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _safe_relative_path(value: Any) -> Path:
    if not isinstance(value, str):
        raise MaterializationError("dependency path must be a string")
    portable = PurePosixPath(value)
    if portable.is_absolute() or not portable.parts or ".." in portable.parts:
        raise MaterializationError(f"unsafe dependency path: {value}")
    return Path(*portable.parts)


def load_dependencies(manifest_path: Path) -> list[dict[str, Any]]:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise MaterializationError(f"cannot read harness manifest: {exc}") from exc
    dependencies = manifest.get("external_runtime_dependencies")
    if not isinstance(dependencies, list):
        raise MaterializationError("external_runtime_dependencies must be an array")
    required_fields = {"path", "size_bytes", "sha256", "role", "provenance"}
    observed_paths: list[str] = []
    for dependency in dependencies:
        if not isinstance(dependency, dict) or set(dependency) != required_fields:
            raise MaterializationError("external dependency entry schema mismatch")
        relative = _safe_relative_path(dependency["path"])
        observed_paths.append(relative.as_posix())
        if (
            not isinstance(dependency["size_bytes"], int)
            or dependency["size_bytes"] < 0
        ):
            raise MaterializationError(f"invalid dependency size: {relative}")
        digest = dependency["sha256"]
        if (
            not isinstance(digest, str)
            or len(digest) != HASH_LENGTH
            or any(character not in "0123456789abcdef" for character in digest)
        ):
            raise MaterializationError(f"invalid dependency hash: {relative}")
        if not isinstance(dependency["role"], str) or not dependency["role"]:
            raise MaterializationError(f"missing dependency role: {relative}")
        if (
            not isinstance(dependency["provenance"], str)
            or not dependency["provenance"]
        ):
            raise MaterializationError(f"missing dependency provenance: {relative}")
    if len(observed_paths) != len(set(observed_paths)):
        raise MaterializationError("duplicate external dependency path")
    if set(observed_paths) != EXPECTED_DEPENDENCY_PATHS:
        raise MaterializationError("missing or extra required external dependency")
    return dependencies


def _assert_no_symlinks(root: Path) -> None:
    if root.is_symlink():
        raise MaterializationError(f"symlink is forbidden: {root}")
    for path in root.rglob("*"):
        if path.is_symlink():
            raise MaterializationError(f"symlink is forbidden: {path}")


def _inventory_files(root: Path) -> set[str]:
    return {
        path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()
    }


def validate_bundle(
    bundle_dir: Path, dependencies: list[dict[str, Any]], *, exact: bool
) -> None:
    if bundle_dir.is_symlink() or not bundle_dir.is_dir():
        raise MaterializationError(
            f"bundle directory is missing or a symlink: {bundle_dir}"
        )
    _assert_no_symlinks(bundle_dir)
    expected_paths = {dependency["path"] for dependency in dependencies}
    if exact and _inventory_files(bundle_dir) != expected_paths:
        raise MaterializationError("materialized bundle has missing or extra files")
    for dependency in dependencies:
        relative = _safe_relative_path(dependency["path"])
        path = bundle_dir / relative
        if path.is_symlink() or not path.is_file():
            raise MaterializationError(f"missing regular dependency file: {relative}")
        observed_size = path.stat().st_size
        if observed_size != dependency["size_bytes"]:
            raise MaterializationError(f"dependency size mismatch: {relative}")
        if sha256_file(path) != dependency["sha256"]:
            raise MaterializationError(f"dependency hash mismatch: {relative}")


def materialize_runtime(
    manifest_path: Path, source_simulator_dir: Path, destination_parent: Path
) -> Path:
    dependencies = load_dependencies(manifest_path)
    source = source_simulator_dir.absolute()
    parent = destination_parent.absolute()
    if source.is_symlink() or not source.is_dir():
        raise MaterializationError("explicit source simulator directory is invalid")
    if parent.is_symlink() or not parent.is_dir():
        raise MaterializationError("destination parent is invalid")
    _assert_no_symlinks(source)
    validate_bundle(source, dependencies, exact=False)
    if source == parent or source in parent.parents or parent in source.parents:
        raise MaterializationError("source and destination trees must be disjoint")

    runtime_dir = Path(tempfile.mkdtemp(prefix="exp3v2-runtime-", dir=parent))
    try:
        for dependency in dependencies:
            relative = _safe_relative_path(dependency["path"])
            destination = runtime_dir / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source / relative, destination, follow_symlinks=False)
        validate_bundle(runtime_dir, dependencies, exact=True)
    except Exception:
        shutil.rmtree(runtime_dir, ignore_errors=True)
        raise
    return runtime_dir


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--source-simulator-dir", type=Path, required=True)
    parser.add_argument("--destination-parent", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        runtime_dir = materialize_runtime(
            args.manifest, args.source_simulator_dir, args.destination_parent
        )
    except Exception as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}))
        return 1
    print(
        json.dumps(
            {
                "status": "PASS",
                "runtime_dir": str(runtime_dir),
                "dependency_count": len(EXPECTED_DEPENDENCY_PATHS),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
