"""Condition C inference runner — centralized full-information pooled ICL.

Executes the 45-entry request schedule, writing CRunRecord entries
to c_records.jsonl.  Supports idempotent resume via sequence_index
and optional --pilot-only mode for the first 15 entries.

No LLM call is made until the inference-side freeze guard passes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import logging
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from icl.conditions.builder_c import (
    ALL_INSIGHT_IDS,
    LABEL_SPACE,
    render_condition_c_prompt,
)
from icl.runner.build_c_schedule import SCHEDULE_PATH
from icl.runner.records_c import CRunRecord


_log = logging.getLogger(__name__)

# Network retry parameters (R5 review: transient error resilience).
_MAX_NETWORK_RETRIES = 4
_INITIAL_BACKOFF_S = 2.0
_BACKOFF_FACTOR = 2.0
_RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


ROOT = Path(__file__).resolve().parents[2]

DEFAULT_OUTPUT_PATH = ROOT / "icl" / "inference" / "c_records.jsonl"
FREEZE_MANIFEST_PATH = ROOT / "icl" / "full_evaluation" / "freeze_manifest_inference.json"
VERBALIZATIONS_MANIFEST_PATH = (
    ROOT / "phase_b" / "final_evaluation"
    / "heldout_verbalizations_manifest.json"
)
EXECUTION_CONFIG_PATH = ROOT / "phase_b" / "config" / "execution_config.json"
DIAGNOSTIC_SCHEMA_PATH = (
    ROOT / "phase_b" / "conditions"
    / "diagnostic_output.openai.schema.json"
)


# ------------------------------------------------------------------
# Freeze guard
# ------------------------------------------------------------------

def _file_sha256(path: Path) -> str:
    """Compute SHA-256 of file content (raw bytes)."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


_CANONICAL_INFERENCE_ARTIFACT_COUNT = 23

_CANONICAL_INFERENCE_ARTIFACT_PATHS = frozenset({
    "icl/conditions/builder_c.py",
    "icl/config/condition_c_config.json",
    "icl/full_evaluation/c_schedule.json",
    "icl/full_evaluation/protocol_amendment_c.json",
    "icl/full_evaluation/protocol_amendment_c.md",
    "icl/pooled_libraries/pooled_examples.json",
    "icl/pooled_libraries/pooled_insights.json",
    "icl/prompts/pooled_C.txt",
    "icl/runner/build_c_schedule.py",
    "icl/runner/records_c.py",
    "icl/runner/run_c_inference.py",
    "icl/schemas/c_run_record.schema.json",
    "icl/tests/test_build_c_schedule.py",
    "icl/tests/test_builder_c.py",
    "icl/tests/test_records_c.py",
    "icl/tests/test_run_c_inference.py",
    "phase_b/conditions/diagnostic_output.openai.schema.json",
    "phase_b/conditions/parser.py",
    "phase_b/conditions/retry.py",
    "phase_b/config/execution_config.json",
    "phase_b/execution/openai_adapter.py",
    "phase_b/heldout/phase_b_heldout_manifest.csv",
    "phase_b/prompts/leakage.py",
})

assert len(_CANONICAL_INFERENCE_ARTIFACT_PATHS) == _CANONICAL_INFERENCE_ARTIFACT_COUNT


def verify_inference_freeze(
    manifest_path: Path,
    *,
    root: Path = ROOT,
) -> dict[str, Any]:
    """Verify all inference-side artifact hashes; raise on mismatch.

    Fail-closed: the manifest must contain exactly the canonical set of
    23 artifacts.  A reduced manifest (e.g. via ``--freeze-manifest``)
    is rejected.

    Returns the parsed freeze manifest on success.
    """
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    # R8: reject arbitrarily reduced manifests.
    artifact_count = len(manifest.get("artifact_hashes", {}))
    if artifact_count != _CANONICAL_INFERENCE_ARTIFACT_COUNT:
        raise RuntimeError(
            f"freeze guard: manifest must have exactly "
            f"{_CANONICAL_INFERENCE_ARTIFACT_COUNT} artifact hashes, "
            f"got {artifact_count}"
        )

    # R9: reject manifests with non-canonical paths.
    manifest_paths = frozenset(manifest["artifact_hashes"].keys())
    if manifest_paths != _CANONICAL_INFERENCE_ARTIFACT_PATHS:
        extra = manifest_paths - _CANONICAL_INFERENCE_ARTIFACT_PATHS
        missing = _CANONICAL_INFERENCE_ARTIFACT_PATHS - manifest_paths
        parts = []
        if extra:
            parts.append(f"unexpected: {sorted(extra)}")
        if missing:
            parts.append(f"missing: {sorted(missing)}")
        raise RuntimeError(
            f"freeze guard: manifest artifact paths do not match "
            f"canonical set — {'; '.join(parts)}"
        )

    for rel_path, expected in manifest["artifact_hashes"].items():
        actual = _file_sha256(root / rel_path)
        if actual != expected:
            raise RuntimeError(
                f"freeze guard: {rel_path} hash mismatch "
                f"(expected {expected[:16]}…, got {actual[:16]}…)"
            )

    verb_path = root / manifest["verbalizations_manifest_path"]
    verb_expected = manifest["verbalizations_manifest_sha256"]
    verb_actual = _file_sha256(verb_path)
    if verb_actual != verb_expected:
        raise RuntimeError(
            f"freeze guard: verbalizations manifest hash mismatch "
            f"(expected {verb_expected[:16]}…, got {verb_actual[:16]}…)"
        )

    return manifest


# ------------------------------------------------------------------
# Case-text loader with hash verification
# ------------------------------------------------------------------

def load_case_texts(
    *,
    verbalizations_manifest_path: Path = VERBALIZATIONS_MANIFEST_PATH,
    root: Path = ROOT,
) -> dict[str, str]:
    """Load and hash-verify neutral texts for all 15 held-out cases.

    Returns ``{physical_case_id: neutral_text}``.
    """
    manifest = json.loads(
        verbalizations_manifest_path.read_text(encoding="utf-8")
    )
    case_texts: dict[str, str] = {}

    for case in manifest["cases"]:
        case_id = case["physical_case_id"]
        text_path = root / case["neutral_text_path"]
        raw_bytes = text_path.read_bytes()
        actual_hash = hashlib.sha256(raw_bytes).hexdigest()
        if actual_hash != case["neutral_text_sha256"]:
            raise RuntimeError(
                f"neutral text hash mismatch for {case_id}: "
                f"expected {case['neutral_text_sha256'][:16]}…, "
                f"got {actual_hash[:16]}…"
            )
        case_texts[case_id] = raw_bytes.decode("utf-8")

    if len(case_texts) != 15:
        raise ValueError(f"expected 15 case texts, got {len(case_texts)}")

    return case_texts


# ------------------------------------------------------------------
# Resume support
# ------------------------------------------------------------------

def load_existing_indices(
    path: Path,
    schedule: list[dict[str, Any]] | None = None,
) -> set[int]:
    """Read existing c_records.jsonl and return completed sequence_index values.

    Each line is validated as a full CRunRecord (fail-fast on corruption).
    Duplicate sequence_index values are detected and rejected.

    When *schedule* is provided, each record's ``(physical_case_id, repetition)``
    is verified against the schedule entry at the corresponding
    ``sequence_index`` (fail-fast on identity mismatch).
    """
    if not path.exists():
        return set()

    # Build schedule lookup for identity verification.
    schedule_lookup: dict[int, tuple[str, int]] | None = None
    if schedule is not None:
        schedule_lookup = {
            e["sequence_index"]: (e["physical_case_id"], e["repetition"])
            for e in schedule
        }

    indices: set[int] = set()
    with path.open(encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            stripped = line.strip()
            if not stripped:
                continue
            try:
                record = CRunRecord.from_jsonl_line(stripped)
            except (json.JSONDecodeError, TypeError, ValueError) as exc:
                raise RuntimeError(
                    f"corrupt c_records.jsonl at line {line_num}: {exc}"
                ) from exc
            if record.sequence_index in indices:
                raise RuntimeError(
                    f"duplicate sequence_index {record.sequence_index} "
                    f"at line {line_num}"
                )
            # Verify identity against schedule (R5 review: resume safety).
            if schedule_lookup is not None:
                expected = schedule_lookup.get(record.sequence_index)
                if expected is None:
                    raise RuntimeError(
                        f"sequence_index {record.sequence_index} at line "
                        f"{line_num} not found in schedule"
                    )
                actual = (record.physical_case_id, record.repetition)
                if actual != expected:
                    raise RuntimeError(
                        f"identity mismatch at line {line_num}: "
                        f"record has {actual}, schedule expects {expected}"
                    )
            indices.add(record.sequence_index)
    return indices


# ------------------------------------------------------------------
# RetryResult + ProviderResponse → CRunRecord mapping
# ------------------------------------------------------------------

def _build_raw_attempts(
    result: Any,
    provider_attempts: tuple,
) -> list[dict[str, Any]]:
    """Map RetryResult + ProviderResponse[] → CRunRecord raw_attempts.

    Token field mapping: ``input_tokens → prompt_tokens``,
    ``output_tokens → completion_tokens``.
    """
    attempts: list[dict[str, Any]] = []
    for i, (raw_text, prov) in enumerate(
        zip(result.raw_attempts, provider_attempts)
    ):
        is_last = i == len(result.raw_attempts) - 1
        if is_last and not result.parse_failure:
            parse_success = True
            error_type = None
        else:
            parse_success = False
            error_type = "parse"

        token_usage = None
        if prov.input_tokens is not None:
            token_usage = {
                "prompt_tokens": prov.input_tokens,
                "completion_tokens": prov.output_tokens,
                "total_tokens": prov.total_tokens,
            }

        attempts.append({
            "attempt_index": i,
            "raw_response": raw_text,
            "parse_success": parse_success,
            "error_type": error_type,
            "request_id": prov.request_id,
            "response_id": prov.response_id,
            "token_usage": token_usage,
        })

    return attempts


# ------------------------------------------------------------------
# Network retry  (R5 review point: transient error resilience)
# ------------------------------------------------------------------

def _is_transient(exc: Exception) -> bool:
    """Return True if *exc* is a transient network/server error.

    Checks both Python built-in network exceptions *and* openai-specific
    exceptions (APIConnectionError, APITimeoutError) which do not inherit
    from the Python built-ins.  (R7 review P1-1.)
    """
    if isinstance(exc, (ConnectionError, TimeoutError, OSError)):
        return True
    # openai.APIConnectionError / openai.APITimeoutError do not inherit from
    # Python's ConnectionError / TimeoutError — check by class name so that
    # the runner module does not hard-depend on openai at import time.
    exc_qualname = type(exc).__qualname__
    exc_module = type(exc).__module__ or ""
    if exc_module.startswith("openai") and exc_qualname in (
        "APIConnectionError", "APITimeoutError",
    ):
        return True
    # OpenAI / httpx status-code errors.
    status = getattr(exc, "status_code", None) or getattr(exc, "status", None)
    if status is not None and int(status) in _RETRYABLE_STATUS_CODES:
        return True
    return False


def _call_with_network_retry(
    fn: Any,
    *,
    max_retries: int = _MAX_NETWORK_RETRIES,
) -> Any:
    """Call *fn* with exponential-backoff retry on transient errors.

    Standalone wrapper around the retry logic also used by
    :class:`_PerCallNetworkRetry`.  Tests and one-off call-sites that
    don't need the context-manager adapter-patching use this directly.
    """
    backoff = _INITIAL_BACKOFF_S
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except Exception as exc:
            if attempt == max_retries or not _is_transient(exc):
                raise
            _log.warning(
                "transient error (attempt %d/%d): %s — retrying in %.1fs",
                attempt + 1, max_retries + 1, exc, backoff,
            )
            time.sleep(backoff)
            backoff *= _BACKOFF_FACTOR
    raise AssertionError("unreachable")  # pragma: no cover


class _PerCallNetworkRetry:
    """Context manager: wraps adapter.create_response with per-call network retry.

    Pushes network retry down to the individual API call level so that
    structural retries inside ``execute_diagnostic`` are preserved when
    a transient network error occurs mid-sequence.
    """

    def __init__(self, adapter: Any) -> None:
        self._adapter = adapter
        self._original = adapter.create_response
        self.network_retries: list[dict[str, Any]] = []

    def __enter__(self) -> "_PerCallNetworkRetry":
        self._adapter.create_response = self._retrying_create_response
        return self

    def __exit__(self, *exc_info: Any) -> None:
        self._adapter.create_response = self._original

    def _retrying_create_response(self, **kwargs: Any) -> Any:
        backoff = _INITIAL_BACKOFF_S
        for attempt in range(_MAX_NETWORK_RETRIES + 1):
            try:
                return self._original(**kwargs)
            except Exception as exc:
                if attempt == _MAX_NETWORK_RETRIES or not _is_transient(exc):
                    raise
                self.network_retries.append({
                    "attempt": attempt,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                    "backoff_seconds": backoff,
                    "timestamp_iso": datetime.now(timezone.utc).isoformat(),
                })
                _log.warning(
                    "transient network error (attempt %d/%d): %s "
                    "— retrying in %.1fs",
                    attempt + 1, _MAX_NETWORK_RETRIES + 1, exc, backoff,
                )
                time.sleep(backoff)
                backoff *= _BACKOFF_FACTOR
        raise AssertionError("unreachable")  # pragma: no cover


# ------------------------------------------------------------------
# Main inference loop
# ------------------------------------------------------------------

def run_c_inference(
    *,
    schedule: list[dict[str, Any]],
    output_path: Path,
    adapter: Any,
    case_texts: dict[str, str],
    reasoning_effort: str,
    schema: dict[str, Any],
    label_space: list[str] | None = None,
    allowed_insight_ids: tuple[str, ...] | None = None,
    pilot_only: bool = False,
    max_structural_retries: int = 2,
    openai_sdk_version: str = "",
) -> dict[str, int]:
    """Execute the Condition C inference loop.

    Appends CRunRecord JSONL lines to *output_path*.  Entries whose
    ``sequence_index`` already appears in the file are skipped
    (idempotent resume).

    Returns ``{"completed": n, "skipped": n, "total": n}``.
    """
    if label_space is None:
        label_space = list(LABEL_SPACE)
    if allowed_insight_ids is None:
        allowed_insight_ids = ALL_INSIGHT_IDS

    existing = load_existing_indices(output_path, schedule=schedule)

    if pilot_only:
        schedule = [e for e in schedule if e["pilot"]]

    prompt_cache: dict[str, Any] = {}
    completed = 0
    skipped = 0

    for entry in schedule:
        seq_idx = entry["sequence_index"]

        if seq_idx in existing:
            skipped += 1
            continue

        case_id = entry["physical_case_id"]

        # Render prompt (cached per case_id — receiver-independent).
        if case_id not in prompt_cache:
            prompt_cache[case_id] = render_condition_c_prompt(
                case_text=case_texts[case_id],
            )
        rendered = prompt_cache[case_id]

        with _PerCallNetworkRetry(adapter) as _net_retry:
            execution = adapter.execute_diagnostic(
                prompt=rendered.text,
                label_space=label_space,
                allowed_insight_ids=allowed_insight_ids,
                reasoning_effort=reasoning_effort,
                schema=schema,
                max_structural_retries=max_structural_retries,
            )
        net_retry_details = _net_retry.network_retries

        result = execution.result
        provider_attempts = execution.provider_attempts

        raw_attempts = _build_raw_attempts(result, provider_attempts)

        record = CRunRecord(
            agent_id="central",
            condition="C",
            physical_case_id=case_id,
            repetition=entry["repetition"],
            sequence_index=seq_idx,
            parsed_output=dict(result.parsed_output),
            valid=not result.parse_failure,
            prompt_sha256=rendered.prompt_hash,
            raw_attempts=raw_attempts,
            retry_count=result.attempts - 1,
            model_requested=provider_attempts[0].requested_model,
            model_returned=provider_attempts[-1].returned_model,
            reasoning_effort=reasoning_effort,
            timestamp_iso=datetime.now(timezone.utc).isoformat(),
            openai_sdk_version=openai_sdk_version,
            stateless=True,
            network_retries=net_retry_details,
        )

        line = record.to_jsonl_line()
        with output_path.open("a", encoding="utf-8") as f:
            f.write(line + "\n")

        existing.add(seq_idx)
        completed += 1

    return {
        "completed": completed,
        "skipped": skipped,
        "total": len(schedule),
    }


# ------------------------------------------------------------------
# CLI entry point
# ------------------------------------------------------------------

def main() -> int:
    """CLI entry point for Condition C inference."""
    parser = argparse.ArgumentParser(
        description="Condition C inference runner",
    )
    parser.add_argument(
        "--pilot-only",
        action="store_true",
        help="Run only pilot entries (sequence_index 0..14)",
    )
    parser.add_argument(
        "--freeze-manifest",
        type=Path,
        default=FREEZE_MANIFEST_PATH,
        help=(
            "Path to inference-side freeze manifest. "
            "Freeze guard always runs (fail-closed). "
            "Default: %(default)s"
        ),
    )
    args = parser.parse_args()

    exec_config = json.loads(
        EXECUTION_CONFIG_PATH.read_text(encoding="utf-8")
    )
    reasoning_effort = exec_config["reasoning_effort_requested"]
    model = exec_config["requested_model"]
    max_retries = exec_config["max_structural_retries"]

    schema = json.loads(DIAGNOSTIC_SCHEMA_PATH.read_text(encoding="utf-8"))

    # Freeze guard is mandatory / fail-closed (R5 review point 8).
    verify_inference_freeze(args.freeze_manifest)
    print("Freeze guard: PASS")

    # R7 P1-2: verify SDK version matches protocol before any inference.
    expected_sdk = exec_config.get("sdk_version", "")
    expected_pkg = exec_config.get("sdk_package", "openai")
    # Lazy import to avoid openai dependency at module level.
    from phase_b.execution.openai_adapter import OpenAIAdapter
    import importlib
    sdk_mod = importlib.import_module(expected_pkg)
    actual_sdk_version: str = getattr(sdk_mod, "__version__", "")
    if actual_sdk_version != expected_sdk:
        raise RuntimeError(
            f"SDK version mismatch: protocol requires "
            f"{expected_pkg}=={expected_sdk}, installed "
            f"{expected_pkg}=={actual_sdk_version}"
        )
    print(f"SDK version check: {expected_pkg}=={actual_sdk_version} OK")

    case_texts = load_case_texts()
    print(f"Loaded {len(case_texts)} case texts")

    schedule = json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))
    print(f"Schedule: {len(schedule)} entries")

    adapter = OpenAIAdapter(requested_model=model)

    DEFAULT_OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    summary = run_c_inference(
        schedule=schedule,
        output_path=DEFAULT_OUTPUT_PATH,
        adapter=adapter,
        case_texts=case_texts,
        reasoning_effort=reasoning_effort,
        schema=schema,
        pilot_only=args.pilot_only,
        max_structural_retries=max_retries,
        openai_sdk_version=actual_sdk_version,
    )

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
