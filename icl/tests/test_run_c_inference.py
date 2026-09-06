"""Unit tests for the Condition C inference runner."""

from __future__ import annotations

import hashlib
import json
import shutil
import tempfile
import types
import unittest
from pathlib import Path
from typing import Any
from unittest.mock import patch

from icl.runner.records_c import CRunRecord
from icl.runner.run_c_inference import (
    DEFAULT_OUTPUT_PATH,
    FREEZE_MANIFEST_PATH,
    _CANONICAL_INFERENCE_ARTIFACT_COUNT,
    _build_raw_attempts,
    _PerCallNetworkRetry,
    _is_transient,
    load_existing_indices,
    run_c_inference,
    verify_inference_freeze,
    load_case_texts,
)


ROOT = Path(__file__).resolve().parents[2]


# ------------------------------------------------------------------
# Mock objects (avoid openai import)
# ------------------------------------------------------------------

def _mock_provider_response(
    raw_output: str = "",
    model: str = "gpt-5.6-terra",
) -> types.SimpleNamespace:
    return types.SimpleNamespace(
        raw_output=raw_output,
        requested_model=model,
        returned_model=model,
        response_id="resp-mock-001",
        request_id="req-mock-001",
        input_tokens=1000,
        output_tokens=50,
        total_tokens=1050,
    )


def _valid_parsed_output() -> dict[str, Any]:
    return {
        "predicted_label": "CLS-ZOGAA",
        "abstain": False,
        "used_insight_ids": ["INS-001"],
        "reasoning_summary": "Mock diagnostic output.",
    }


def _mock_execution(
    parsed_output: dict[str, Any] | None = None,
    parse_failure: bool = False,
    num_attempts: int = 1,
    model: str = "gpt-5.6-terra",
) -> types.SimpleNamespace:
    """Build a mock DiagnosticExecution-like object."""
    if parsed_output is None:
        parsed_output = _valid_parsed_output()
    raw = json.dumps(parsed_output)
    raw_attempts = tuple(raw for _ in range(num_attempts))
    if parse_failure:
        validation_errors = tuple(f"error-{i}" for i in range(num_attempts))
    else:
        validation_errors = tuple(
            f"error-{i}" for i in range(num_attempts - 1)
        )
    result = types.SimpleNamespace(
        raw_output=raw,
        parsed_output=parsed_output,
        attempts=num_attempts,
        validation_errors=validation_errors,
        raw_attempts=raw_attempts,
        parse_failure=parse_failure,
    )
    provider_attempts = tuple(
        _mock_provider_response(raw_output=raw, model=model)
        for _ in range(num_attempts)
    )
    return types.SimpleNamespace(
        result=result, provider_attempts=provider_attempts,
    )


class _MockAdapter:
    """Mock adapter returning valid diagnostic executions."""

    def __init__(self, model: str = "gpt-5.6-terra") -> None:
        self.requested_model = model
        self.call_count = 0

    def create_response(self, **kwargs: Any) -> Any:
        """Dummy create_response — required by _PerCallNetworkRetry."""
        return None  # pragma: no cover

    def execute_diagnostic(
        self, *, prompt, label_space, allowed_insight_ids,
        reasoning_effort, schema, max_structural_retries=2, **kw,
    ) -> types.SimpleNamespace:
        self.call_count += 1
        return _mock_execution(model=self.requested_model)


# ------------------------------------------------------------------
# Mock render_condition_c_prompt
# ------------------------------------------------------------------

def _mock_render(*, case_text: str) -> types.SimpleNamespace:
    return types.SimpleNamespace(
        text=f"mock prompt: {case_text[:30]}",
        prompt_hash=hashlib.sha256(case_text.encode()).hexdigest(),
        available_insight_ids=tuple(f"INS-{i:03d}" for i in range(1, 9)),
    )


# ------------------------------------------------------------------
# Schedule and case_text helpers
# ------------------------------------------------------------------

def _make_schedule(
    n_pilot: int = 1, n_non_pilot: int = 1,
) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for i in range(1, n_pilot + 1):
        cid = f"PBH-{i:03d}"
        for rep in (1, 2, 3):
            entries.append({
                "sequence_index": len(entries),
                "physical_case_id": cid,
                "repetition": rep,
                "condition": "C",
                "receiver_id": "central",
                "pilot": True,
            })
    for i in range(n_pilot + 1, n_pilot + n_non_pilot + 1):
        cid = f"PBH-{i:03d}"
        for rep in (1, 2, 3):
            entries.append({
                "sequence_index": len(entries),
                "physical_case_id": cid,
                "repetition": rep,
                "condition": "C",
                "receiver_id": "central",
                "pilot": False,
            })
    return entries


def _case_texts_for(
    schedule: list[dict[str, Any]],
) -> dict[str, str]:
    ids = sorted({e["physical_case_id"] for e in schedule})
    return {
        cid: f"Process variable readings for observation {cid}."
        for cid in ids
    }


# ------------------------------------------------------------------
# Helper: valid CRunRecord JSONL line for resume testing
# ------------------------------------------------------------------

def _valid_record_line(
    sequence_index: int,
    case_id: str = "PBH-001",
    repetition: int = 1,
) -> str:
    """Build a valid CRunRecord JSONL line for testing resume."""
    record = CRunRecord(
        agent_id="central", condition="C",
        physical_case_id=case_id, repetition=repetition,
        sequence_index=sequence_index,
        parsed_output={
            "predicted_label": "CLS-ZOGAA", "abstain": False,
            "used_insight_ids": ["INS-001"],
            "reasoning_summary": "test resume record",
        },
        valid=True,
        prompt_sha256=hashlib.sha256(b"test").hexdigest(),
        raw_attempts=[{
            "attempt_index": 0, "raw_response": "{}",
            "parse_success": True, "error_type": None,
            "request_id": "req-1", "response_id": "resp-1",
            "token_usage": {
                "prompt_tokens": 1000,
                "completion_tokens": 50,
                "total_tokens": 1050,
            },
        }],
        retry_count=0,
        model_requested="gpt-5.6-terra",
        model_returned="gpt-5.6-terra",
        reasoning_effort="medium",
        timestamp_iso="2026-09-06T12:00:00+00:00",
        openai_sdk_version="3.6.0",
        stateless=True,
    )
    return record.to_jsonl_line()


# ------------------------------------------------------------------
# Tests: load_existing_indices
# ------------------------------------------------------------------

class TestLoadExistingIndices(unittest.TestCase):

    def test_nonexistent_file(self) -> None:
        p = Path(tempfile.mktemp(suffix=".jsonl"))
        self.assertEqual(load_existing_indices(p), set())

    def test_populated_file(self) -> None:
        d = Path(tempfile.mkdtemp())
        try:
            p = d / "records.jsonl"
            with p.open("w", encoding="utf-8") as f:
                for idx in (0, 5, 10):
                    f.write(_valid_record_line(idx) + "\n")
            self.assertEqual(load_existing_indices(p), {0, 5, 10})
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_corrupt_file_raises(self) -> None:
        d = Path(tempfile.mkdtemp())
        try:
            p = d / "records.jsonl"
            p.write_text("not json\n", encoding="utf-8")
            with self.assertRaises(RuntimeError):
                load_existing_indices(p)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_invalid_record_raises(self) -> None:
        """A line that is valid JSON but not a valid CRunRecord → RuntimeError."""
        d = Path(tempfile.mkdtemp())
        try:
            p = d / "records.jsonl"
            p.write_text(
                json.dumps({"sequence_index": 0}) + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(RuntimeError):
                load_existing_indices(p)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_duplicate_sequence_index_raises(self) -> None:
        """Duplicate sequence_index values → RuntimeError."""
        d = Path(tempfile.mkdtemp())
        try:
            p = d / "records.jsonl"
            with p.open("w", encoding="utf-8") as f:
                f.write(_valid_record_line(0) + "\n")
                f.write(_valid_record_line(0) + "\n")
            with self.assertRaises(RuntimeError) as ctx:
                load_existing_indices(p)
            self.assertIn("duplicate", str(ctx.exception))
        finally:
            shutil.rmtree(d, ignore_errors=True)


# ------------------------------------------------------------------
# Tests: _build_raw_attempts
# ------------------------------------------------------------------

class TestBuildRawAttempts(unittest.TestCase):

    def test_single_success(self) -> None:
        exe = _mock_execution(num_attempts=1, parse_failure=False)
        attempts = _build_raw_attempts(exe.result, exe.provider_attempts)
        self.assertEqual(len(attempts), 1)
        self.assertTrue(attempts[0]["parse_success"])
        self.assertIsNone(attempts[0]["error_type"])
        self.assertEqual(attempts[0]["attempt_index"], 0)
        self.assertEqual(attempts[0]["token_usage"]["prompt_tokens"], 1000)
        self.assertEqual(attempts[0]["token_usage"]["completion_tokens"], 50)
        self.assertEqual(attempts[0]["token_usage"]["total_tokens"], 1050)

    def test_retry_then_success(self) -> None:
        exe = _mock_execution(num_attempts=2, parse_failure=False)
        attempts = _build_raw_attempts(exe.result, exe.provider_attempts)
        self.assertEqual(len(attempts), 2)
        self.assertFalse(attempts[0]["parse_success"])
        self.assertEqual(attempts[0]["error_type"], "parse")
        self.assertTrue(attempts[1]["parse_success"])
        self.assertIsNone(attempts[1]["error_type"])

    def test_all_failed(self) -> None:
        exe = _mock_execution(num_attempts=3, parse_failure=True)
        attempts = _build_raw_attempts(exe.result, exe.provider_attempts)
        self.assertEqual(len(attempts), 3)
        for att in attempts:
            self.assertFalse(att["parse_success"])
            self.assertEqual(att["error_type"], "parse")

    def test_null_token_usage(self) -> None:
        exe = _mock_execution(num_attempts=1, parse_failure=False)
        exe.provider_attempts[0].input_tokens = None
        attempts = _build_raw_attempts(exe.result, exe.provider_attempts)
        self.assertIsNone(attempts[0]["token_usage"])

    def test_request_and_response_ids(self) -> None:
        exe = _mock_execution(num_attempts=1, parse_failure=False)
        attempts = _build_raw_attempts(exe.result, exe.provider_attempts)
        self.assertEqual(attempts[0]["request_id"], "req-mock-001")
        self.assertEqual(attempts[0]["response_id"], "resp-mock-001")


# ------------------------------------------------------------------
# Tests: run_c_inference (with mocked prompt builder)
# ------------------------------------------------------------------

@patch(
    "icl.runner.run_c_inference.render_condition_c_prompt",
    side_effect=_mock_render,
)
class TestRunCInference(unittest.TestCase):

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())
        self.output_path = self.tmpdir / "c_records.jsonl"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _pre_populate(
        self, indices: set[int], schedule: list[dict] | None = None,
    ) -> None:
        """Write valid CRunRecord entries for resume testing."""
        sched_lookup = {e["sequence_index"]: e for e in schedule} if schedule else {}
        with self.output_path.open("w", encoding="utf-8") as f:
            for idx in sorted(indices):
                if idx in sched_lookup:
                    entry = sched_lookup[idx]
                    f.write(_valid_record_line(
                        idx,
                        case_id=entry["physical_case_id"],
                        repetition=entry["repetition"],
                    ) + "\n")
                else:
                    f.write(_valid_record_line(idx) + "\n")

    def _read_lines(self) -> list[str]:
        return [
            l for l in
            self.output_path.read_text("utf-8").strip().split("\n")
            if l.strip()
        ]

    def test_full_run(self, mock_render) -> None:
        schedule = _make_schedule(1, 1)
        adapter = _MockAdapter()
        summary = run_c_inference(
            schedule=schedule,
            output_path=self.output_path,
            adapter=adapter,
            case_texts=_case_texts_for(schedule),
            reasoning_effort="medium",
            schema={"type": "object"},
            openai_sdk_version="3.6.0",
        )
        self.assertEqual(summary["completed"], 6)
        self.assertEqual(summary["skipped"], 0)
        self.assertEqual(summary["total"], 6)
        self.assertEqual(len(self._read_lines()), 6)
        self.assertEqual(adapter.call_count, 6)

    def test_resume_skips_existing(self, mock_render) -> None:
        schedule = _make_schedule(1, 1)
        self._pre_populate({0, 1, 2}, schedule=schedule)
        adapter = _MockAdapter()
        summary = run_c_inference(
            schedule=schedule,
            output_path=self.output_path,
            adapter=adapter,
            case_texts=_case_texts_for(schedule),
            reasoning_effort="medium",
            schema={"type": "object"},
            openai_sdk_version="3.6.0",
        )
        self.assertEqual(summary["completed"], 3)
        self.assertEqual(summary["skipped"], 3)
        self.assertEqual(adapter.call_count, 3)

    def test_idempotency(self, mock_render) -> None:
        """Second run skips everything — zero adapter calls."""
        schedule = _make_schedule(1, 0)
        adapter1 = _MockAdapter()
        run_c_inference(
            schedule=schedule,
            output_path=self.output_path,
            adapter=adapter1,
            case_texts=_case_texts_for(schedule),
            reasoning_effort="medium",
            schema={"type": "object"},
            openai_sdk_version="3.6.0",
        )
        adapter2 = _MockAdapter()
        summary2 = run_c_inference(
            schedule=schedule,
            output_path=self.output_path,
            adapter=adapter2,
            case_texts=_case_texts_for(schedule),
            reasoning_effort="medium",
            schema={"type": "object"},
            openai_sdk_version="3.6.0",
        )
        self.assertEqual(summary2["completed"], 0)
        self.assertEqual(summary2["skipped"], 3)
        self.assertEqual(adapter2.call_count, 0)

    def test_pilot_only(self, mock_render) -> None:
        schedule = _make_schedule(2, 2)  # 6 pilot + 6 non-pilot = 12
        adapter = _MockAdapter()
        summary = run_c_inference(
            schedule=schedule,
            output_path=self.output_path,
            adapter=adapter,
            case_texts=_case_texts_for(schedule),
            reasoning_effort="medium",
            schema={"type": "object"},
            openai_sdk_version="3.6.0",
            pilot_only=True,
        )
        self.assertEqual(summary["completed"], 6)
        self.assertEqual(summary["total"], 6)
        self.assertEqual(adapter.call_count, 6)

    def test_record_fields(self, mock_render) -> None:
        schedule = _make_schedule(1, 0)
        run_c_inference(
            schedule=schedule,
            output_path=self.output_path,
            adapter=_MockAdapter(),
            case_texts=_case_texts_for(schedule),
            reasoning_effort="medium",
            schema={"type": "object"},
            openai_sdk_version="3.6.0",
        )
        record = json.loads(self._read_lines()[0])
        self.assertEqual(record["agent_id"], "central")
        self.assertEqual(record["condition"], "C")
        self.assertEqual(record["physical_case_id"], "PBH-001")
        self.assertEqual(record["repetition"], 1)
        self.assertEqual(record["sequence_index"], 0)
        self.assertTrue(record["valid"])
        self.assertTrue(record["stateless"])
        self.assertEqual(record["reasoning_effort"], "medium")
        self.assertEqual(record["retry_count"], 0)
        self.assertEqual(record["model_requested"], "gpt-5.6-terra")
        self.assertEqual(record["model_returned"], "gpt-5.6-terra")
        self.assertEqual(len(record["raw_attempts"]), 1)
        self.assertTrue(record["raw_attempts"][0]["parse_success"])
        self.assertEqual(record["network_retries"], [])

    def test_all_records_stateless(self, mock_render) -> None:
        schedule = _make_schedule(1, 1)
        run_c_inference(
            schedule=schedule,
            output_path=self.output_path,
            adapter=_MockAdapter(),
            case_texts=_case_texts_for(schedule),
            reasoning_effort="medium",
            schema={"type": "object"},
            openai_sdk_version="3.6.0",
        )
        for line in self._read_lines():
            record = json.loads(line)
            self.assertTrue(record["stateless"])

    def test_prompt_cache_reuses_per_case(self, mock_render) -> None:
        """PBH-001 has 3 repetitions; render should be called once."""
        schedule = _make_schedule(1, 0)
        run_c_inference(
            schedule=schedule,
            output_path=self.output_path,
            adapter=_MockAdapter(),
            case_texts=_case_texts_for(schedule),
            reasoning_effort="medium",
            schema={"type": "object"},
            openai_sdk_version="3.6.0",
        )
        self.assertEqual(mock_render.call_count, 1)

    def test_written_records_validate(self, mock_render) -> None:
        """Every written line must pass CRunRecord roundtrip validation."""
        schedule = _make_schedule(1, 0)
        run_c_inference(
            schedule=schedule,
            output_path=self.output_path,
            adapter=_MockAdapter(),
            case_texts=_case_texts_for(schedule),
            reasoning_effort="medium",
            schema={"type": "object"},
            openai_sdk_version="3.6.0",
        )
        for line in self._read_lines():
            record = CRunRecord.from_jsonl_line(line)
            self.assertEqual(record.condition, "C")
            self.assertEqual(record.agent_id, "central")

    def test_sequential_indices(self, mock_render) -> None:
        """Records are written in schedule order."""
        schedule = _make_schedule(1, 1)
        run_c_inference(
            schedule=schedule,
            output_path=self.output_path,
            adapter=_MockAdapter(),
            case_texts=_case_texts_for(schedule),
            reasoning_effort="medium",
            schema={"type": "object"},
            openai_sdk_version="3.6.0",
        )
        indices = [
            json.loads(line)["sequence_index"]
            for line in self._read_lines()
        ]
        self.assertEqual(indices, list(range(6)))


# ------------------------------------------------------------------
# Tests: freeze guard
# ------------------------------------------------------------------

class TestFreezeGuard(unittest.TestCase):

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def _write(self, rel_path: str, content: str) -> str:
        p = self.tmpdir / rel_path
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        return hashlib.sha256(content.encode("utf-8")).hexdigest()

    def _make_n_artifacts(self, n: int) -> dict[str, str]:
        """Create *n* dummy artifact files; return {rel_path: sha256}."""
        hashes: dict[str, str] = {}
        for i in range(n):
            rel = f"artifact_{i:03d}.json"
            h = self._write(rel, json.dumps({"idx": i}))
            hashes[rel] = h
        return hashes

    def test_pass(self) -> None:
        artifact_hashes = self._make_n_artifacts(
            _CANONICAL_INFERENCE_ARTIFACT_COUNT,
        )
        verb_hash = self._write("verb_manifest.json", '{"cases": []}')

        manifest = {
            "artifact_hashes": artifact_hashes,
            "verbalizations_manifest_path": "verb_manifest.json",
            "verbalizations_manifest_sha256": verb_hash,
        }
        manifest_path = self.tmpdir / "freeze.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        result = verify_inference_freeze(manifest_path, root=self.tmpdir)
        self.assertIn("artifact_hashes", result)

    def test_artifact_hash_mismatch(self) -> None:
        artifact_hashes = self._make_n_artifacts(
            _CANONICAL_INFERENCE_ARTIFACT_COUNT,
        )
        verb_hash = self._write("verb_manifest.json", "{}")
        # Corrupt one hash.
        first_key = next(iter(artifact_hashes))
        artifact_hashes[first_key] = "0" * 64

        manifest = {
            "artifact_hashes": artifact_hashes,
            "verbalizations_manifest_path": "verb_manifest.json",
            "verbalizations_manifest_sha256": verb_hash,
        }
        manifest_path = self.tmpdir / "freeze.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        with self.assertRaises(RuntimeError) as ctx:
            verify_inference_freeze(manifest_path, root=self.tmpdir)
        self.assertIn("freeze guard", str(ctx.exception))
        self.assertIn(first_key, str(ctx.exception))

    def test_verbalization_manifest_mismatch(self) -> None:
        artifact_hashes = self._make_n_artifacts(
            _CANONICAL_INFERENCE_ARTIFACT_COUNT,
        )
        self._write("verb_manifest.json", '{"cases": []}')

        manifest = {
            "artifact_hashes": artifact_hashes,
            "verbalizations_manifest_path": "verb_manifest.json",
            "verbalizations_manifest_sha256": "0" * 64,
        }
        manifest_path = self.tmpdir / "freeze.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")

        with self.assertRaises(RuntimeError) as ctx:
            verify_inference_freeze(manifest_path, root=self.tmpdir)
        self.assertIn("verbalizations manifest", str(ctx.exception))

    def test_wrong_artifact_count_raises(self) -> None:
        """R8: manifest with != 23 artifact hashes is rejected."""
        for bad_count in (0, 1, 22, 24, 50):
            artifact_hashes = self._make_n_artifacts(bad_count)
            verb_hash = self._write("verb_manifest.json", "{}")
            manifest = {
                "artifact_hashes": artifact_hashes,
                "verbalizations_manifest_path": "verb_manifest.json",
                "verbalizations_manifest_sha256": verb_hash,
            }
            manifest_path = self.tmpdir / "freeze.json"
            manifest_path.write_text(
                json.dumps(manifest), encoding="utf-8",
            )
            with self.assertRaises(RuntimeError, msg=f"count={bad_count}") as ctx:
                verify_inference_freeze(manifest_path, root=self.tmpdir)
            self.assertIn(
                str(_CANONICAL_INFERENCE_ARTIFACT_COUNT),
                str(ctx.exception),
            )

    def test_canonical_count_constant(self) -> None:
        """R8: the constant is 23."""
        self.assertEqual(_CANONICAL_INFERENCE_ARTIFACT_COUNT, 23)




class TestFreezeGuardIntegration(unittest.TestCase):
    """Integration: verify_inference_freeze against the real manifest on disk."""

    def test_real_manifest_passes(self) -> None:
        """Run verify_inference_freeze(FREEZE_MANIFEST_PATH) on the actual
        freeze_manifest_inference.json.  This catches structural regressions
        (missing keys, removed artifacts) that unit tests with synthetic
        fixtures cannot detect."""
        result = verify_inference_freeze(FREEZE_MANIFEST_PATH)
        self.assertIn("artifact_hashes", result)
        self.assertIsInstance(result["artifact_hashes"], dict)
        self.assertEqual(
            len(result["artifact_hashes"]),
            _CANONICAL_INFERENCE_ARTIFACT_COUNT,
        )

    def test_real_manifest_has_verbalizations_keys(self) -> None:
        """The manifest must carry verbalizations_manifest_path and
        verbalizations_manifest_sha256 — verify_inference_freeze reads them."""
        manifest = json.loads(FREEZE_MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertIn("verbalizations_manifest_path", manifest)
        self.assertIn("verbalizations_manifest_sha256", manifest)

    def test_real_manifest_has_manifest_type(self) -> None:
        manifest = json.loads(FREEZE_MANIFEST_PATH.read_text(encoding="utf-8"))
        self.assertEqual(manifest["manifest_type"], "freeze_manifest_inference")


# ------------------------------------------------------------------
# Tests: firewall (source-code scan)
# ------------------------------------------------------------------

class TestFirewall(unittest.TestCase):

    def test_no_evaluator_side_references(self) -> None:
        """Runner source must not reference evaluator-side artifacts."""
        source_path = ROOT / "icl" / "runner" / "run_c_inference.py"
        source = source_path.read_text(encoding="utf-8")
        forbidden = [
            "pseudolabel_mapping",
            "evaluator_side",
            "class_offline",
            "real_to_opaque",
        ]
        for term in forbidden:
            self.assertNotIn(
                term, source,
                f"runner source must not contain '{term}' (firewall)",
            )

    def test_no_phase_b_prediction_access(self) -> None:
        """Runner must not read Phase B predictions."""
        source_path = ROOT / "icl" / "runner" / "run_c_inference.py"
        source = source_path.read_text(encoding="utf-8")
        forbidden = ["b_records", "predictions/b_", "run_record.schema"]
        for term in forbidden:
            self.assertNotIn(
                term, source,
                f"runner source must not contain '{term}' (firewall)",
            )


# ------------------------------------------------------------------
# Tests: load_case_texts (integration, requires real files)
# ------------------------------------------------------------------

class TestLoadCaseTexts(unittest.TestCase):

    def test_loads_all_15_cases(self) -> None:
        """Integration: verify real manifest loads and hashes pass."""
        case_texts = load_case_texts()
        self.assertEqual(len(case_texts), 15)
        for i in range(1, 16):
            cid = f"PBH-{i:03d}"
            self.assertIn(cid, case_texts)
            self.assertIsInstance(case_texts[cid], str)
            self.assertTrue(case_texts[cid].strip())


# ------------------------------------------------------------------
# Tests: path constants (R5 review points 8-9)
# ------------------------------------------------------------------

class TestPathConstants(unittest.TestCase):

    def test_default_output_path(self) -> None:
        """DEFAULT_OUTPUT_PATH must point to icl/inference/c_records.jsonl."""
        self.assertEqual(DEFAULT_OUTPUT_PATH.name, "c_records.jsonl")
        self.assertTrue(
            str(DEFAULT_OUTPUT_PATH).endswith(
                "icl/inference/c_records.jsonl"
            ),
            f"unexpected DEFAULT_OUTPUT_PATH: {DEFAULT_OUTPUT_PATH}",
        )

    def test_freeze_manifest_path_exists(self) -> None:
        """FREEZE_MANIFEST_PATH must point to freeze_manifest_inference.json."""
        self.assertEqual(FREEZE_MANIFEST_PATH.name, "freeze_manifest_inference.json")
        self.assertTrue(
            str(FREEZE_MANIFEST_PATH).endswith(
                "icl/full_evaluation/freeze_manifest_inference.json"
            ),
            f"unexpected FREEZE_MANIFEST_PATH: {FREEZE_MANIFEST_PATH}",
        )


class TestMandatoryFreeze(unittest.TestCase):
    """R5 review point 8: --freeze-manifest is fail-closed."""

    def test_main_always_calls_freeze_guard(self) -> None:
        """main() runs verify_inference_freeze unconditionally."""
        import icl.runner.run_c_inference as mod
        source = Path(mod.__file__).read_text(encoding="utf-8")
        # Must NOT contain 'if args.freeze_manifest is not None:'
        self.assertNotIn(
            "if args.freeze_manifest is not None",
            source,
            "freeze guard must be unconditional (fail-closed)",
        )
        # Must contain unconditional verify_inference_freeze call.
        self.assertIn("verify_inference_freeze(args.freeze_manifest)", source)


# ------------------------------------------------------------------
# Tests: _is_transient
# ------------------------------------------------------------------

class TestIsTransient(unittest.TestCase):

    def test_connection_error(self) -> None:
        self.assertTrue(_is_transient(ConnectionError("reset")))

    def test_timeout_error(self) -> None:
        self.assertTrue(_is_transient(TimeoutError("timed out")))

    def test_os_error(self) -> None:
        self.assertTrue(_is_transient(OSError("network unreachable")))

    def test_status_429(self) -> None:
        exc = Exception("rate limited")
        exc.status_code = 429
        self.assertTrue(_is_transient(exc))

    def test_status_502(self) -> None:
        exc = Exception("bad gateway")
        exc.status_code = 502
        self.assertTrue(_is_transient(exc))

    def test_status_503(self) -> None:
        exc = Exception("unavailable")
        exc.status_code = 503
        self.assertTrue(_is_transient(exc))

    def test_status_400_not_transient(self) -> None:
        exc = Exception("bad request")
        exc.status_code = 400
        self.assertFalse(_is_transient(exc))

    def test_value_error_not_transient(self) -> None:
        self.assertFalse(_is_transient(ValueError("bad value")))

    def test_runtime_error_not_transient(self) -> None:
        self.assertFalse(_is_transient(RuntimeError("logic error")))

    # R7 P1-1: openai-specific exceptions.

    def test_openai_api_connection_error(self) -> None:
        """openai.APIConnectionError is transient (detected by class name)."""
        # Simulate without importing openai — create a class with the right
        # qualname and module.
        exc = type("APIConnectionError", (Exception,), {})("conn failed")
        type(exc).__module__ = "openai"
        self.assertTrue(_is_transient(exc))

    def test_openai_api_timeout_error(self) -> None:
        """openai.APITimeoutError is transient (detected by class name)."""
        exc = type("APITimeoutError", (Exception,), {})("timed out")
        type(exc).__module__ = "openai"
        self.assertTrue(_is_transient(exc))

    def test_openai_submodule_exception(self) -> None:
        """Exceptions from openai.* submodules are also caught."""
        exc = type("APIConnectionError", (Exception,), {})("conn failed")
        type(exc).__module__ = "openai._exceptions"
        self.assertTrue(_is_transient(exc))

    def test_non_openai_api_connection_error_not_transient(self) -> None:
        """APIConnectionError from a different module is not transient."""
        exc = type("APIConnectionError", (Exception,), {})("conn failed")
        type(exc).__module__ = "some_other_lib"
        self.assertFalse(_is_transient(exc))


# ------------------------------------------------------------------
# Tests: _call_with_network_retry
# ------------------------------------------------------------------

class TestPerCallNetworkRetry(unittest.TestCase):
    """Tests for _PerCallNetworkRetry (per-call network retry wrapper)."""

    def _make_adapter(self) -> types.SimpleNamespace:
        """Return a minimal adapter with a create_response method."""
        adapter = types.SimpleNamespace()
        adapter.create_response = lambda **kw: {"raw": "ok"}
        return adapter

    def test_success_first_try(self) -> None:
        adapter = self._make_adapter()
        with _PerCallNetworkRetry(adapter) as nr:
            result = adapter.create_response(prompt="hi")
        self.assertEqual(result, {"raw": "ok"})
        self.assertEqual(nr.network_retries, [])

    @patch("icl.runner.run_c_inference.time.sleep")
    def test_retries_on_transient(self, mock_sleep) -> None:
        adapter = self._make_adapter()
        calls = {"n": 0}
        original = adapter.create_response
        def flaky(**kw):
            calls["n"] += 1
            if calls["n"] < 3:
                raise ConnectionError("transient")
            return original(**kw)
        adapter.create_response = flaky
        with _PerCallNetworkRetry(adapter) as nr:
            result = adapter.create_response(prompt="test")
        self.assertEqual(result, {"raw": "ok"})
        self.assertEqual(len(nr.network_retries), 2)
        for entry in nr.network_retries:
            self.assertIn("attempt", entry)
            self.assertIn("error_type", entry)
            self.assertIn("error_message", entry)
            self.assertIn("backoff_seconds", entry)
            self.assertIn("timestamp_iso", entry)
        self.assertEqual(mock_sleep.call_count, 2)

    @patch("icl.runner.run_c_inference.time.sleep")
    def test_gives_up_after_max_retries(self, mock_sleep) -> None:
        adapter = self._make_adapter()
        adapter.create_response = lambda **kw: (_ for _ in ()).throw(
            ConnectionError("down"))
        with self.assertRaises(ConnectionError):
            with _PerCallNetworkRetry(adapter) as nr:
                adapter.create_response(prompt="x")

    def test_propagates_non_transient(self) -> None:
        adapter = self._make_adapter()
        adapter.create_response = lambda **kw: (_ for _ in ()).throw(
            ValueError("not transient"))
        with self.assertRaises(ValueError):
            with _PerCallNetworkRetry(adapter) as nr:
                adapter.create_response(prompt="x")

    @patch("icl.runner.run_c_inference.time.sleep")
    def test_exponential_backoff(self, mock_sleep) -> None:
        adapter = self._make_adapter()
        calls = {"n": 0}
        original = adapter.create_response
        def flaky(**kw):
            calls["n"] += 1
            if calls["n"] < 4:
                raise TimeoutError("slow")
            return original(**kw)
        adapter.create_response = flaky
        with _PerCallNetworkRetry(adapter) as nr:
            adapter.create_response(prompt="test")
        self.assertEqual(len(nr.network_retries), 3)
        backoffs = [e["backoff_seconds"] for e in nr.network_retries]
        self.assertAlmostEqual(backoffs[0], 2.0)
        self.assertAlmostEqual(backoffs[1], 4.0)
        self.assertAlmostEqual(backoffs[2], 8.0)
        delays = [c[0][0] for c in mock_sleep.call_args_list]
        self.assertAlmostEqual(delays[0], 2.0)
        self.assertAlmostEqual(delays[1], 4.0)
        self.assertAlmostEqual(delays[2], 8.0)

    def test_restores_original_on_exit(self) -> None:
        adapter = self._make_adapter()
        original = adapter.create_response
        with _PerCallNetworkRetry(adapter):
            self.assertIsNot(adapter.create_response, original)
        self.assertIs(adapter.create_response, original)

    @patch("icl.runner.run_c_inference.time.sleep")
    def test_structural_retries_preserved(self, mock_sleep) -> None:
        """Network retry wraps each create_response call individually,
        so structural retries inside execute_diagnostic are preserved."""
        adapter = self._make_adapter()
        cr_calls = {"n": 0}
        original = adapter.create_response
        def flaky_cr(**kw):
            cr_calls["n"] += 1
            # Fail on the 2nd call with transient error, succeed on retry.
            if cr_calls["n"] == 2:
                raise ConnectionError("transient on 2nd structural attempt")
            return original(**kw)
        adapter.create_response = flaky_cr
        # Simulate execute_diagnostic making 3 calls to create_response.
        results = []
        with _PerCallNetworkRetry(adapter) as nr:
            results.append(adapter.create_response(prompt="call1"))
            results.append(adapter.create_response(prompt="call2"))
            results.append(adapter.create_response(prompt="call3"))
        # All 3 calls succeeded (call2 was retried once).
        self.assertEqual(len(results), 3)
        self.assertEqual(len(nr.network_retries), 1)
        # 4 total underlying calls: 1 + (1 fail + 1 retry) + 1
        self.assertEqual(cr_calls["n"], 4)


# ------------------------------------------------------------------
# Tests: load_existing_indices with schedule identity (P1-2)
# ------------------------------------------------------------------

class TestLoadExistingIndicesScheduleIdentity(unittest.TestCase):

    def setUp(self) -> None:
        self.tmpdir = Path(tempfile.mkdtemp())

    def tearDown(self) -> None:
        shutil.rmtree(self.tmpdir, ignore_errors=True)

    def test_identity_match_passes(self) -> None:
        """Records matching schedule identity are accepted."""
        p = self.tmpdir / "records.jsonl"
        schedule = _make_schedule(1, 0)  # PBH-001, reps 1-3, seq 0-2
        with p.open("w", encoding="utf-8") as f:
            for entry in schedule:
                f.write(_valid_record_line(
                    entry["sequence_index"],
                    case_id=entry["physical_case_id"],
                    repetition=entry["repetition"],
                ) + "\n")
        result = load_existing_indices(p, schedule=schedule)
        self.assertEqual(result, {0, 1, 2})

    def test_identity_mismatch_raises(self) -> None:
        """Record with wrong case_id for its sequence_index → RuntimeError."""
        p = self.tmpdir / "records.jsonl"
        schedule = _make_schedule(1, 0)
        # Write record with PBH-002 at sequence_index 0 (schedule says PBH-001)
        with p.open("w", encoding="utf-8") as f:
            f.write(_valid_record_line(0, case_id="PBH-002", repetition=1) + "\n")
        with self.assertRaises(RuntimeError) as ctx:
            load_existing_indices(p, schedule=schedule)
        self.assertIn("identity mismatch", str(ctx.exception))

    def test_unknown_sequence_index_raises(self) -> None:
        """Record with sequence_index not in schedule → RuntimeError."""
        p = self.tmpdir / "records.jsonl"
        schedule = _make_schedule(1, 0)  # seq 0-2 only
        with p.open("w", encoding="utf-8") as f:
            f.write(_valid_record_line(3, case_id="PBH-001", repetition=1) + "\n")
        with self.assertRaises(RuntimeError) as ctx:
            load_existing_indices(p, schedule=schedule)
        self.assertIn("not found in schedule", str(ctx.exception))

    def test_no_schedule_skips_identity_check(self) -> None:
        """Without schedule, identity check is skipped (backward compat)."""
        p = self.tmpdir / "records.jsonl"
        with p.open("w", encoding="utf-8") as f:
            f.write(_valid_record_line(0) + "\n")
        result = load_existing_indices(p)
        self.assertEqual(result, {0})


if __name__ == "__main__":
    unittest.main()
