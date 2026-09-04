#!/usr/bin/env python3
"""Fail-closed validator for the isolated EXP3_V2 inference runtime."""

from __future__ import annotations

import argparse
import importlib
import importlib.metadata
import json
import os
from pathlib import Path
import platform
import sys


HERE = Path(__file__).resolve().parent
DEFAULT_LOCK = HERE / "EXP3_V2_INFERENCE_RUNTIME_LOCK_001.json"
IGNORED_DISTRIBUTIONS = {"pip", "setuptools"}


def normalized(name: str) -> str:
    return name.lower().replace("_", "-")


def installed_environment() -> dict[str, str]:
    observed: dict[str, str] = {}
    for distribution in importlib.metadata.distributions():
        raw_name = distribution.metadata.get("Name")
        if not raw_name:
            continue
        name = normalized(raw_name)
        if name in IGNORED_DISTRIBUTIONS:
            continue
        if name in observed:
            raise RuntimeError(f"duplicate installed distribution: {name}")
        observed[name] = distribution.version
    return dict(sorted(observed.items()))


def validate_runtime(lock_path: Path = DEFAULT_LOCK) -> dict[str, object]:
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    invocation = Path(sys.executable).absolute()
    expected_invocation = Path(lock["invocation_executable"])
    if invocation != expected_invocation:
        raise RuntimeError(
            f"runtime invocation mismatch: {invocation} != {expected_invocation}"
        )
    if not invocation.is_file() or not os.access(invocation, os.X_OK):
        raise RuntimeError("runtime executable is not an executable file")
    canonical = invocation.resolve(strict=True)
    if canonical != Path(lock["canonical_base_executable"]):
        raise RuntimeError("canonical Python executable mismatch")
    if platform.python_version() != lock["python_version"]:
        raise RuntimeError("Python version mismatch")

    expected = {
        normalized(name): version
        for name, version in lock["complete_environment"].items()
    }
    observed = installed_environment()
    if observed != dict(sorted(expected.items())):
        missing = sorted(set(expected) - set(observed))
        extra = sorted(set(observed) - set(expected))
        altered = sorted(
            name
            for name in set(expected) & set(observed)
            if expected[name] != observed[name]
        )
        raise RuntimeError(
            f"runtime dependency closure mismatch: missing={missing}, extra={extra}, altered={altered}"
        )
    for module in ("openai", "jsonschema"):
        importlib.import_module(module)
    return {
        "status": "PASS",
        "invocation_executable": str(invocation),
        "canonical_base_executable": str(canonical),
        "python_version": platform.python_version(),
        "packages": observed,
        "credential_environment_inspected": False,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lock", type=Path, default=DEFAULT_LOCK)
    args = parser.parse_args(argv)
    print(json.dumps(validate_runtime(args.lock), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
