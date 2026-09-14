#!/usr/bin/env python3
"""Create and verify the local normal_dev conservation candidate."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import tarfile
import tempfile
from pathlib import Path
from typing import Any


RELEASE_TAG = "studio2-fase03-normal-dev-v1"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sources(root: Path) -> list[tuple[Path, str, str]]:
    mappings = (
        (root / "runs" / "normal_dev_001", "normal_dev_001", "raw_run"),
        (root / "evidence" / "normal_dev_002", "normal_evidence_002", "normal_evidence"),
        (root / "runtime", "runtime", "runtime_trace"),
        (root / "audit_history", "audit_history", "audit_history"),
    )
    result: list[tuple[Path, str, str]] = []
    for source_root, archive_root, role in mappings:
        if not source_root.is_dir():
            raise FileNotFoundError(source_root)
        for path in sorted(item for item in source_root.rglob("*") if item.is_file()):
            result.append((path, str(Path(archive_root) / path.relative_to(source_root)), role))
    for path, archive_path, role in (
        (root / "plans" / "normal_dev.csv", "normal_dev.csv", "generation_plan"),
        (root / "AUDIT_NORMAL_DEV.json", "AUDIT_NORMAL_DEV.json", "current_audit"),
        (root / "AUDIT_NORMAL_DEV.md", "AUDIT_NORMAL_DEV.md", "current_audit"),
    ):
        if not path.is_file():
            raise FileNotFoundError(path)
        result.append((path, archive_path, role))
    archive_paths = [archive_path for _, archive_path, _ in result]
    if len(archive_paths) != len(set(archive_paths)):
        raise RuntimeError("duplicate archive path")
    forbidden = [path for path in archive_paths if Path(path).name.startswith("._")]
    if forbidden:
        raise RuntimeError(f"AppleDouble source entries are forbidden: {forbidden}")
    return sorted(result, key=lambda item: item[1])


def inventory(root: Path, entries: list[tuple[Path, str, str]]) -> list[dict[str, Any]]:
    return [
        {
            "archive_path": archive_path,
            "source_path": str(path.relative_to(root)),
            "role": role,
            "bytes": path.stat().st_size,
            "sha256": sha256_file(path),
        }
        for path, archive_path, role in entries
    ]


def write_manifest(path: Path, rows: list[dict[str, Any]]) -> None:
    fields = ["archive_path", "source_path", "role", "bytes", "sha256"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build_tar(path: Path, entries: list[tuple[Path, str, str]]) -> None:
    if path.exists():
        raise FileExistsError(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    partial = path.with_suffix(path.suffix + ".partial")
    if partial.exists():
        raise FileExistsError(partial)
    try:
        with tarfile.open(partial, "w", format=tarfile.USTAR_FORMAT) as archive:
            for source, archive_path, _ in entries:
                info = archive.gettarinfo(str(source), arcname=archive_path)
                info.uid = 0
                info.gid = 0
                info.uname = ""
                info.gname = ""
                info.mtime = 0
                info.mode = 0o644
                with source.open("rb") as handle:
                    archive.addfile(info, handle)
        partial.rename(path)
    except Exception:
        partial.unlink(missing_ok=True)
        raise


def verify_tar(path: Path, rows: list[dict[str, Any]]) -> dict[str, Any]:
    expected = {row["archive_path"]: row for row in rows}
    with tarfile.open(path, "r") as archive:
        members = archive.getmembers()
        regular = [member for member in members if member.isfile()]
        appledouble = [member.name for member in members if Path(member.name).name.startswith("._")]
        pax = [member.name for member in members if member.pax_headers]
        names = [member.name for member in regular]
        if appledouble or pax or set(names) != set(expected) or len(names) != len(expected):
            raise RuntimeError("archive members, AppleDouble, or PAX headers differ from policy")
        for member in regular:
            stream = archive.extractfile(member)
            if stream is None:
                raise RuntimeError(f"cannot read archive member: {member.name}")
            digest = hashlib.sha256()
            size = 0
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
                size += len(chunk)
            row = expected[member.name]
            if digest.hexdigest() != row["sha256"] or size != int(row["bytes"]):
                raise RuntimeError(f"archive member mismatch: {member.name}")

    with tempfile.TemporaryDirectory(prefix="fot-tep-normal-dev-verify-") as directory:
        destination = Path(directory)
        with tarfile.open(path, "r") as archive:
            archive.extractall(destination, filter="data")
        extracted = [item for item in destination.rglob("*") if item.is_file()]
        if len(extracted) != len(expected):
            raise RuntimeError("extracted file count differs from inventory")
        for item in extracted:
            row = expected[str(item.relative_to(destination))]
            if item.stat().st_size != int(row["bytes"]) or sha256_file(item) != row["sha256"]:
                raise RuntimeError(f"extracted file mismatch: {item}")
    return {
        "local_archive_verification": "PASS",
        "regular_files": len(expected),
        "bytes_verified": sum(int(row["bytes"]) for row in rows),
        "appledouble_entries": 0,
        "members_with_pax_headers": 0,
        "extra_files": 0,
        "mismatches": 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    manifest_path = root / "MANIFEST_CONSERVAZIONE.csv"
    storage_path = root / "ARTIFACT_STORAGE.json"
    archive_path = root / "conservation" / f"{RELEASE_TAG}.tar"
    if manifest_path.exists() or storage_path.exists():
        raise FileExistsError("conservation metadata already exists")
    entries = sources(root)
    rows = inventory(root, entries)
    write_manifest(manifest_path, rows)
    build_tar(archive_path, entries)
    verification = verify_tar(archive_path, rows)
    storage = {
        "schema_version": 1,
        "scope": "normal_dev raw workbooks, runtime, audit history, and Normal evidence",
        "release": {
            "proposed_tag": RELEASE_TAG,
            "status": "local_candidate_not_published_not_redownloaded",
            "repository": "sorrentinoluca/fot-tep-data",
            "release_url": None,
            "published_at_utc": None,
            "redownload_verified": False,
        },
        "archive": {
            "local_path": str(archive_path.relative_to(root)),
            "name": archive_path.name,
            "bytes": archive_path.stat().st_size,
            "sha256": sha256_file(archive_path),
            "format": "uncompressed POSIX ustar",
        },
        "inventory": {
            "path": str(manifest_path.relative_to(root)),
            "rows": len(rows),
            "bytes": sum(int(row["bytes"]) for row in rows),
            "sha256": sha256_file(manifest_path),
        },
        "packaging": {
            "deterministic_metadata": "uid/gid/mtime normalized; regular files only",
            "appledouble_entries": 0,
            "members_with_pax_headers": 0,
            "xattrs_stored": False,
        },
        "verification": verification,
        "publication_requirements_remaining": [
            "publish the archive and SHA-256 asset under the proposed tag",
            "download the published asset into a fresh external directory",
            "compare archive SHA-256, members, bytes, and every file SHA-256",
        ],
    }
    storage_path.write_text(
        json.dumps(storage, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(storage, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
