"""Fail-closed verification of every artifact that can reach an API prompt."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from .common import HarnessError, load_json, require_sha256, sha256_text


@dataclass(frozen=True)
class FileGuard:
    path: Path
    sha256: str
    role: str


def verify_files(guards: Iterable[FileGuard]) -> None:
    rows = list(guards)
    if not rows:
        raise HarnessError("at least one guarded file is required")
    for guard in rows:
        require_sha256(guard.path, guard.sha256, role=guard.role)


def verify_tokenizer(
    snapshot: Path,
    *,
    revision: str,
    tokenizer_json_sha256: str,
    tokenizer_config_sha256: str,
    chat_template_sha256: str,
) -> None:
    if snapshot.name != revision:
        raise HarnessError("tokenizer snapshot directory does not identify pinned revision")
    verify_files(
        [
            FileGuard(snapshot / "tokenizer.json", tokenizer_json_sha256, "tokenizer.json"),
            FileGuard(
                snapshot / "tokenizer_config.json",
                tokenizer_config_sha256,
                "tokenizer_config.json",
            ),
        ]
    )
    template_path = snapshot / "chat_template.jinja"
    if template_path.is_file():
        require_sha256(template_path, chat_template_sha256, role="chat_template.jinja")
    else:
        config = load_json(snapshot / "tokenizer_config.json")
        template = config.get("chat_template")
        if not isinstance(template, str) or sha256_text(template) != chat_template_sha256:
            raise HarnessError("chat template is missing or differs from the pinned template")


def verify_endpoint(observed: dict[str, Any], expected: dict[str, Any]) -> None:
    """Compare declarative endpoint identity without contacting it."""
    keys = (
        "returned_model_root",
        "returned_model_revision",
        "vllm_version",
        "command_sha256",
        "environment_sha256",
        "fingerprint_sha256",
        "max_model_len",
    )
    missing = [key for key in keys if key not in observed or key not in expected]
    if missing:
        raise HarnessError(f"endpoint fingerprint missing keys: {missing}")
    differences = {key: (expected[key], observed[key]) for key in keys if observed[key] != expected[key]}
    if differences:
        raise HarnessError(f"endpoint fingerprint mismatch: {differences}")


def assert_ready_for_calls(
    *,
    status: str,
    missing_requirements: list[str],
    file_guards: Iterable[FileGuard],
    tokenizer: tuple[Path, dict[str, str]],
    endpoint_observed: dict[str, Any],
    endpoint_expected: dict[str, Any],
) -> None:
    if status != "FROZEN_FOR_PHASE03_PRE_GATE" or missing_requirements:
        raise HarnessError("scientific input manifest is incomplete or not frozen")
    verify_files(file_guards)
    snapshot, token = tokenizer
    verify_tokenizer(snapshot, **token)
    verify_endpoint(endpoint_observed, endpoint_expected)
