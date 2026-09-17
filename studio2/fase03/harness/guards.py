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


def require_execution(config: dict[str, Any]) -> None:
    """Historical preflight can never authorize transport, even via direct entrypoints."""
    from .common import canonical_json
    if config.get('study_model_decision') != 'APPROVED' or config.get('status') != 'APPROVED_FOR_PHASE03_EXECUTION':
        raise HarnessError('execution suspended: approved model decision and executable preflight required after D9')
    from .d9 import validate_config
    validate_config(config)
    approval_ref = config.get('execution_authorization', {})
    path = Path(approval_ref.get('path', ''))
    require_sha256(path, approval_ref.get('sha256', ''), role='execution approval')
    approval = load_json(path)
    payload = {k: v for k, v in config.items() if k != 'execution_authorization'}
    if approval.get('decision') != 'accepted' or not approval.get('author') or approval.get('configuration_sha256') != sha256_text(canonical_json(payload)):
        raise HarnessError('execution approval does not cover this exact configuration')


def response_identity_valid(record: dict[str, Any], expected: dict[str, Any]) -> bool:
    # Null fingerprint is admissible only when explicitly recorded as unavailable.
    if not isinstance(expected.get('returned_model'), str) or not expected['returned_model']:
        raise HarnessError('expected returned model is missing')
    if 'system_fingerprint' not in expected or (expected['system_fingerprint'] is not None and (not isinstance(expected['system_fingerprint'], str) or not expected['system_fingerprint'])):
        raise HarnessError('expected fingerprint must be explicit, including unavailable/null')
    return all(key in record and record[key] == expected[key] for key in ('returned_model', 'system_fingerprint'))


def require_presentation(inventory: dict[str, Any], approval_ref: dict[str, Any]) -> None:
    from .common import canonical_json
    from .ordering import presentation_order
    presentation = inventory.get('presentation', {})
    if presentation.get('author_decision') != 'accepted':
        raise HarnessError('presentation order has not been accepted by the author')
    ordered = presentation_order(presentation.get('ordered_labels', []))
    path = Path(approval_ref.get('path', ''))
    require_sha256(path, approval_ref.get('sha256', ''), role='presentation approval')
    approval = load_json(path)
    if approval.get('decision') != 'accepted' or not approval.get('author') or approval.get('ordered_labels_sha256') != sha256_text(canonical_json(ordered)):
        raise HarnessError('presentation approval does not bind the exact order')


def require_pilot_ledger(config, ledger):
    expected = config.get('pilot_ledger', {})
    if (expected.get('pilot_id') != ledger.pilot_id or not expected.get('path')
            or Path(expected['path']).resolve() != ledger.identity_path):
        raise HarnessError('pilot ledger identity/path is not covered by execution approval')
    from .d9 import validate_history
    with ledger._transaction() as connection:
        ledger.require_current_config(config, connection)
        validate_history(config, ledger, connection)
        ledger._validated_attempt_inventory(connection)
