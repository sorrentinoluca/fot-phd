"""Fail-closed access guard for the pre-freeze Phase B development framework."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


class HeldoutAccessError(PermissionError):
    """Raised when development code attempts to access frozen held-out data."""


@dataclass(frozen=True)
class HeldoutAccessGuard:
    raw_heldout_root: Path
    frozen_filenames: frozenset[str]
    integrity_verifier: Path | None = None

    @classmethod
    def from_manifest(
        cls,
        *,
        raw_heldout_root: str | Path,
        manifest: str | Path,
        integrity_verifier: str | Path | None = None,
    ) -> "HeldoutAccessGuard":
        with Path(manifest).open(newline="", encoding="utf-8") as stream:
            filenames = frozenset(row["filename"] for row in csv.DictReader(stream))
        return cls(
            raw_heldout_root=Path(raw_heldout_root).resolve(),
            frozen_filenames=filenames,
            integrity_verifier=(
                Path(integrity_verifier).resolve() if integrity_verifier else None
            ),
        )

    def assert_allowed(
        self,
        path: str | Path,
        *,
        purpose: str = "development",
        explicit_integrity_request: bool = False,
    ) -> Path:
        candidate = Path(path).resolve()
        if (
            explicit_integrity_request
            and purpose == "integrity_verification"
            and self.integrity_verifier is not None
            and candidate == self.integrity_verifier
        ):
            return candidate
        under_raw_root = candidate == self.raw_heldout_root or self.raw_heldout_root in candidate.parents
        name_frozen = candidate.name in self.frozen_filenames
        if under_raw_root or name_frozen:
            raise HeldoutAccessError(
                f"Phase B held-out access denied before protocol freeze: {candidate}"
            )
        return candidate


def project_guard(project_root: str | Path) -> HeldoutAccessGuard:
    root = Path(project_root).resolve()
    heldout_docs = root / "phase_b" / "heldout"
    return HeldoutAccessGuard.from_manifest(
        raw_heldout_root=root / "tep_heldout",
        manifest=heldout_docs / "phase_b_heldout_manifest.csv",
        integrity_verifier=heldout_docs / "verify_heldout_integrity.py",
    )
