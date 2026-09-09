from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .config import CACHE_VERSION


def empty_cache() -> dict[str, Any]:
    return {
        "version": CACHE_VERSION,
        "routing": {},
        "chart_tables": {},
        "openai_analyses": {},
    }


def load_cache(cache_file: Path) -> dict[str, Any]:
    if not cache_file.exists():
        return empty_cache()

    try:
        cache = json.loads(cache_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        print(f"Warning: Could not read cache file: {cache_file}")
        return empty_cache()

    required_sections = {"routing", "chart_tables", "openai_analyses"}
    if (
        not isinstance(cache, dict)
        or cache.get("version") != CACHE_VERSION
        or not required_sections.issubset(cache)
    ):
        print("Existing figure cache uses an older format; starting a new cache.")
        return empty_cache()

    return cache


def save_cache(cache_file: Path, cache: dict[str, Any]) -> None:
    cache_file.parent.mkdir(parents=True, exist_ok=True)
    temporary_file = cache_file.with_suffix(".tmp")
    temporary_file.write_text(
        json.dumps(cache, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    temporary_file.replace(cache_file)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def make_cache_key(*parts: str) -> str:
    return sha256_bytes("\0".join(parts).encode("utf-8"))
