#!/usr/bin/env python3
"""Create and verify the recoverable copy required before Studio 2 data reuse."""

from __future__ import annotations

import argparse
import csv
import hashlib
import os
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


SOURCE_ROOTS = (
    Path("code/tep_cache"),
    Path("tep_cache"),
    Path("tep_heldout/mode1"),
)
EXPECTED_SOURCE_PATHS = 78
EXPECTED_UNIQUE_CONTENTS = 74
MANIFEST_FIELDS = (
    "source_path",
    "source_size_bytes",
    "sha256",
    "destination_path",
    "destination_size_bytes",
    "destination_sha256",
)


@dataclass(frozen=True)
class SourceFile:
    path: Path
    size: int
    sha256: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def discover_sources(repo_root: Path) -> list[SourceFile]:
    paths: list[Path] = []
    for relative_root in SOURCE_ROOTS:
        root = repo_root / relative_root
        if not root.is_dir():
            raise RuntimeError(f"directory sorgente assente: {relative_root}")
        paths.extend(path for path in root.rglob("*.xlsx") if path.is_file())

    sources = [
        SourceFile(
            path=path.relative_to(repo_root),
            size=path.stat().st_size,
            sha256=sha256_file(path),
        )
        for path in sorted(paths)
    ]
    unique_hashes = {source.sha256 for source in sources}
    if len(sources) != EXPECTED_SOURCE_PATHS:
        raise RuntimeError(
            f"perimetro inatteso: {len(sources)} percorsi, "
            f"attesi {EXPECTED_SOURCE_PATHS}"
        )
    if len(unique_hashes) != EXPECTED_UNIQUE_CONTENTS:
        raise RuntimeError(
            f"perimetro inatteso: {len(unique_hashes)} contenuti unici, "
            f"attesi {EXPECTED_UNIQUE_CONTENTS}"
        )
    return sources


def copy_atomically(source: Path, destination: Path) -> None:
    temporary = destination.with_suffix(destination.suffix + ".tmp")
    try:
        with source.open("rb") as source_handle, temporary.open("xb") as target_handle:
            shutil.copyfileobj(source_handle, target_handle, length=1024 * 1024)
            target_handle.flush()
            os.fsync(target_handle.fileno())
        os.replace(temporary, destination)
    finally:
        temporary.unlink(missing_ok=True)


def preserve(repo_root: Path, destination_root: Path, manifest_path: Path) -> tuple[int, int]:
    sources = discover_sources(repo_root)
    destination_root.mkdir(parents=True, exist_ok=True)

    source_by_hash: dict[str, SourceFile] = {}
    for source in sources:
        source_by_hash.setdefault(source.sha256, source)

    copied = 0
    for digest, source in sorted(source_by_hash.items()):
        destination = destination_root / f"{digest}.xlsx"
        if destination.exists():
            if destination.stat().st_size != source.size or sha256_file(destination) != digest:
                raise RuntimeError(
                    f"destinazione esistente non valida, non sovrascritta: {destination}"
                )
            continue
        copy_atomically(repo_root / source.path, destination)
        if destination.stat().st_size != source.size or sha256_file(destination) != digest:
            raise RuntimeError(f"verifica della copia fallita: {destination}")
        copied += 1

    rows: list[dict[str, str | int]] = []
    destination_prefix = destination_root.relative_to(repo_root)
    for source in sources:
        destination = destination_root / f"{source.sha256}.xlsx"
        destination_digest = sha256_file(destination)
        if destination.stat().st_size != source.size or destination_digest != source.sha256:
            raise RuntimeError(f"verifica finale fallita: {destination}")
        rows.append(
            {
                "source_path": source.path.as_posix(),
                "source_size_bytes": source.size,
                "sha256": source.sha256,
                "destination_path": (destination_prefix / destination.name).as_posix(),
                "destination_size_bytes": destination.stat().st_size,
                "destination_sha256": destination_digest,
            }
        )

    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_manifest = manifest_path.with_suffix(manifest_path.suffix + ".tmp")
    try:
        with temporary_manifest.open("x", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=MANIFEST_FIELDS, lineterminator="\n")
            writer.writeheader()
            writer.writerows(rows)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_manifest, manifest_path)
    finally:
        temporary_manifest.unlink(missing_ok=True)

    return copied, len(source_by_hash)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parents[2],
        help="radice del repository (default: rilevata dal percorso dello script)",
    )
    parser.add_argument(
        "--destination",
        type=Path,
        default=Path("studio2/fase02/patrimonio_conservato/contenuti"),
        help="destinazione relativa alla radice del repository",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=Path("studio2/fase02/MANIFEST_CONSERVAZIONE.csv"),
        help="manifest relativo alla radice del repository",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = args.repo_root.resolve()
    destination_root = (repo_root / args.destination).resolve()
    manifest_path = (repo_root / args.manifest).resolve()
    try:
        destination_root.relative_to(repo_root / "studio2")
        manifest_path.relative_to(repo_root / "studio2")
    except ValueError:
        print("destinazione e manifest devono restare sotto studio2/", file=sys.stderr)
        return 2

    try:
        copied, unique = preserve(repo_root, destination_root, manifest_path)
    except (OSError, RuntimeError) as error:
        print(f"ERRORE: {error}", file=sys.stderr)
        return 1

    print(
        f"OK: {unique} contenuti verificati; {copied} nuove copie; "
        f"manifest={manifest_path.relative_to(repo_root)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
