"""Small deterministic helpers shared by the 03.10 harness."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


class HarnessError(ValueError):
    """An input violates a pre-specified harness contract."""


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require_sha256(path: Path, expected: str, *, role: str) -> None:
    if not path.is_file():
        raise HarnessError(f"missing {role}: {path}")
    actual = sha256_file(path)
    if actual != expected:
        raise HarnessError(f"{role} SHA-256 mismatch: expected {expected}, got {actual}")


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise HarnessError(f"cannot load JSON {path}: {exc}") from exc

