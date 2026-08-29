from __future__ import annotations

from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
from types import SimpleNamespace
import unittest
from unittest.mock import patch

import phase_b.execution.openai_adapter as adapter_module
from phase_b.conditions.parser import OutputValidationError, parse_diagnostic_output
from phase_b.execution.openai_adapter import OpenAIAdapter
from phase_b.tests.helpers import load_config


class FakeUsage:
    def __init__(self, input_tokens: int = 100, output_tokens: int = 20) -> None:
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens
        self.total_tokens = input_tokens + output_tokens

    def model_dump(self, *, mode: str) -> dict:
        self.mode = mode
        return {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "output_tokens_details": {"reasoning_tokens": 7},
        }


class FakeResponse:
    def __init__(self, output_text: str) -> None:
        self.output_text = output_text
        self.model = "gpt-5.6-terra"
        self.id = "resp_fixture"
        self._request_id = "req_fixture"
        self.usage = FakeUsage()

    def model_dump(self, *, mode: str) -> dict:
        self.mode = mode
        return {
            "id": self.id,
            "model": self.model,
            "output_text": self.output_text,
            "usage": self.usage.model_dump(mode=mode),
        }


class FakeResponses:
    def __init__(self, outputs: list[str] | None = None, error: Exception | None = None) -> None:
        self.outputs = list(outputs or [])
        self.error = error
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        if self.error is not None:
            raise self.error
        return FakeResponse(self.outputs.pop(0))


class OpenAIExecutionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_config()
        self.valid = {
            "predicted_label": self.config["label_space"][0],
            "abstain": False,
            "used_insight_ids": [],
            "reasoning_summary": "Synthetic structural response.",
        }

    def adapter(self, responses: FakeResponses) -> OpenAIAdapter:
        return OpenAIAdapter(
            requested_model="gpt-5.6-terra",
            client=SimpleNamespace(responses=responses),
        )

    def test_local_schema_is_unchanged_and_provider_schema_is_explicit_derivation(self) -> None:
        root = Path(__file__).resolve().parents[2]
        local_path = root / "phase_b/conditions/diagnostic_output.schema.json"
        local_bytes = local_path.read_bytes()
        self.assertEqual(
            hashlib.sha256(local_bytes).hexdigest(),
            "5abed6a82be2ecd1a6654a32124338fe08c1dceae0c24b51e0ec9e6c99363b19",
        )
        local = json.loads(local_bytes)
        provider = json.loads(
            (
                root
                / "phase_b/conditions/diagnostic_output.openai.schema.json"
            ).read_text(encoding="utf-8")
        )
        expected = deepcopy(local)
        expected["title"] = "Phase B diagnostic output (OpenAI Structured Outputs)"
        expected.pop("allOf")
        expected["properties"]["used_insight_ids"].pop("uniqueItems")
        self.assertEqual(provider, expected)

    def test_local_validator_still_rejects_duplicate_used_insight_ids(self) -> None:
        duplicate = {
            **self.valid,
            "used_insight_ids": ["INS-001", "INS-001"],
        }
        with self.assertRaisesRegex(OutputValidationError, "must not contain duplicates"):
            parse_diagnostic_output(
                json.dumps(duplicate),
                label_space=self.config["label_space"],
                allowed_insight_ids=["INS-001"],
            )

    def test_capability_config_records_verified_provider_results(self) -> None:
        root = Path(__file__).resolve().parents[2]
        execution = json.loads(
            (root / "phase_b/config/execution_config.json").read_text(encoding="utf-8")
        )
        self.assertEqual(execution["provider"], "openai")
        self.assertEqual(execution["requested_model"], "gpt-5.6-terra")
        self.assertEqual(execution["returned_model"], "gpt-5.6-terra")
        self.assertEqual(execution["reasoning_effort_effective"], "medium")
        self.assertIs(execution["temperature_supported"], False)
        self.assertIsNone(execution["temperature"])
        self.assertIs(execution["seed_supported"], False)
        self.assertIsNone(execution["seed"])
        self.assertIs(execution["structured_output_supported"], True)
        self.assertIs(execution["structured_output_strict"], True)
        self.assertIs(execution["token_accounting_supported"], True)
        self.assertEqual(execution["token_accounting_source"], "response.usage")
        self.assertEqual(execution["repetitions"], 3)
        self.assertEqual(execution["max_structural_retries"], 2)
        self.assertEqual(execution["bootstrap_draws"], 10_000)
        self.assertEqual(execution["bootstrap_seed"], 20260829)

    def test_recorded_provider_aware_B_E_token_equivalence(self) -> None:
        root = Path(__file__).resolve().parents[2]
        artifact = json.loads(
            (root / "phase_b/reports/LLM_CAPABILITY_PROBE_RAW.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertTrue(artifact["sanitized"])
        self.assertFalse(artifact["raw_outputs_stored"])
        self.assertEqual(artifact["api_calls_made"], 3)
        dry = artifact["dry_run"]
        self.assertEqual(dry["B"]["prompt_characters"], dry["E"]["prompt_characters"])
        self.assertEqual(
            dry["B"]["peer_block_characters"],
            dry["E"]["peer_block_characters"],
        )
        self.assertEqual(dry["B"]["input_tokens"], 1850)
        self.assertEqual(dry["E"]["input_tokens"], 1850)
        comparison = artifact["provider_token_equivalence"]
        self.assertEqual(comparison["difference_B_minus_E"], 0)
        self.assertTrue(comparison["equivalent"])

    def test_api_key_is_environment_only_when_creating_real_client(self) -> None:
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaisesRegex(RuntimeError, "OPENAI_API_KEY"):
                OpenAIAdapter(requested_model="gpt-5.6-terra")

    def test_sdk_automatic_retries_are_disabled(self) -> None:
        fake_client = SimpleNamespace(responses=FakeResponses([]))
        with patch.dict(os.environ, {"OPENAI_API_KEY": "test-only-placeholder"}, clear=True):
            with patch.object(adapter_module, "OpenAI", return_value=fake_client) as constructor:
                adapter = OpenAIAdapter(requested_model="gpt-5.6-terra")
        self.assertIs(adapter.client, fake_client)
        constructor.assert_called_once_with(max_retries=0, timeout=120.0)

    def test_request_and_response_provenance_usage_and_raw_preservation(self) -> None:
        responses = FakeResponses([json.dumps(self.valid)])
        adapter = self.adapter(responses)
        schema = {"type": "object", "additionalProperties": False}
        result = adapter.create_response(
            prompt="fixture",
            reasoning_effort="medium",
            schema=schema,
            temperature=0.0,
            seed=20260829,
        )
        request = responses.calls[0]
        self.assertEqual(request["model"], "gpt-5.6-terra")
        self.assertEqual(request["reasoning"], {"effort": "medium"})
        self.assertEqual(request["temperature"], 0.0)
        self.assertEqual(request["extra_body"], {"seed": 20260829})
        self.assertEqual(request["text"]["format"]["schema"], schema)
        self.assertTrue(request["text"]["format"]["strict"])
        self.assertFalse(request["store"])
        self.assertEqual(result.returned_model, "gpt-5.6-terra")
        self.assertEqual(result.response_id, "resp_fixture")
        self.assertEqual(result.request_id, "req_fixture")
        self.assertEqual((result.input_tokens, result.output_tokens, result.total_tokens), (100, 20, 120))
        self.assertEqual(result.usage_raw["output_tokens_details"]["reasoning_tokens"], 7)
        self.assertEqual(result.response_raw["id"], "resp_fixture")

    def test_structural_retry_preserves_every_provider_attempt(self) -> None:
        responses = FakeResponses(["not-json", json.dumps(self.valid)])
        result = self.adapter(responses).execute_diagnostic(
            prompt="BASE",
            label_space=self.config["label_space"],
            allowed_insight_ids=[],
            reasoning_effort="medium",
            schema=None,
        )
        self.assertEqual(result.result.attempts, 2)
        self.assertEqual(result.result.raw_attempts, ("not-json", json.dumps(self.valid)))
        self.assertEqual(len(result.provider_attempts), 2)
        self.assertEqual(len(responses.calls), 2)
        self.assertNotIn("CORRECTION REQUIRED", responses.calls[0]["input"])
        self.assertIn("CORRECTION REQUIRED", responses.calls[1]["input"])

    def test_unknown_used_insight_id_is_a_structural_retry(self) -> None:
        invalid = {**self.valid, "used_insight_ids": ["INS-999"]}
        valid = {**self.valid, "used_insight_ids": ["INS-001"]}
        responses = FakeResponses([json.dumps(invalid), json.dumps(valid)])
        result = self.adapter(responses).execute_diagnostic(
            prompt="BASE",
            label_space=self.config["label_space"],
            allowed_insight_ids=["INS-001"],
            reasoning_effort="medium",
            schema=None,
        )
        self.assertEqual(result.result.attempts, 2)
        self.assertEqual(result.result.parsed_output["used_insight_ids"], ["INS-001"])

    def test_provider_error_is_not_structurally_retried(self) -> None:
        responses = FakeResponses(error=RuntimeError("provider failure"))
        with self.assertRaisesRegex(RuntimeError, "provider failure"):
            self.adapter(responses).execute_diagnostic(
                prompt="BASE",
                label_space=self.config["label_space"],
                allowed_insight_ids=[],
                reasoning_effort="medium",
                schema=None,
            )
        self.assertEqual(len(responses.calls), 1)


if __name__ == "__main__":
    unittest.main()
