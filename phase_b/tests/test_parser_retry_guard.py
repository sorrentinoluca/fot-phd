from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from phase_b.conditions.parser import OutputValidationError, parse_diagnostic_output
from phase_b.conditions.retry import execute_with_retry
from phase_b.guard import HeldoutAccessError, HeldoutAccessGuard, project_guard
from phase_b.tests.helpers import load_config


ROOT = Path(__file__).resolve().parents[2]


class ParserRetryGuardTests(unittest.TestCase):
    def setUp(self) -> None:
        self.config = load_config()
        self.valid = {
            "predicted_label": self.config["label_space"][0],
            "abstain": False,
            "used_insight_ids": [],
            "reasoning_summary": "Evidence matches one supplied local example.",
        }

    def parse(self, raw: str) -> dict:
        return parse_diagnostic_output(
            raw, label_space=self.config["label_space"], allowed_insight_ids=[]
        )

    def test_invalid_json_rejected(self) -> None:
        with self.assertRaises(OutputValidationError):
            self.parse("```json\n{}\n```")
        with self.assertRaises(OutputValidationError):
            self.parse('{"predicted_label":')

    def test_unknown_label_and_extra_key_rejected(self) -> None:
        unknown = {**self.valid, "predicted_label": "CLS-XXXXX"}
        with self.assertRaisesRegex(OutputValidationError, "unknown"):
            self.parse(json.dumps(unknown, separators=(",", ":")))
        extra = {**self.valid, "confidence": 0.9}
        with self.assertRaises(OutputValidationError):
            self.parse(json.dumps(extra, separators=(",", ":")))

    def test_abstain_allows_null_prediction(self) -> None:
        value = {**self.valid, "predicted_label": None, "abstain": True}
        parsed = self.parse(json.dumps(value, separators=(",", ":")))
        self.assertTrue(parsed["abstain"])

    def test_abstain_rejects_non_null_prediction(self) -> None:
        value = {**self.valid, "abstain": True}
        with self.assertRaisesRegex(OutputValidationError, "requires predicted_label to be null"):
            self.parse(json.dumps(value, separators=(",", ":")))

    def test_retry_policy_is_bounded_and_deterministic(self) -> None:
        outputs = ["not-json", json.dumps(self.valid, separators=(",", ":"))]
        seen_prompts: list[str] = []

        def call(prompt: str, attempt: int) -> str:
            seen_prompts.append(prompt)
            return outputs[attempt - 1]

        result = execute_with_retry(call=call, prompt="BASE", parse=self.parse, max_retries=2)
        self.assertEqual(result.attempts, 2)
        self.assertEqual(len(result.validation_errors), 1)
        self.assertEqual(len(result.raw_attempts), 2)
        self.assertFalse(result.parse_failure)
        self.assertEqual(seen_prompts[0], "BASE")
        self.assertEqual(seen_prompts[1], seen_prompts[-1])
        self.assertIn("CORRECTION REQUIRED", seen_prompts[1])

    def test_exactly_two_retries_then_parse_failure_abstain(self) -> None:
        calls: list[int] = []

        def call(prompt: str, attempt: int) -> str:
            calls.append(attempt)
            return "not-json"

        result = execute_with_retry(call=call, prompt="BASE", parse=self.parse, max_retries=2)
        self.assertEqual(calls, [1, 2, 3])
        self.assertEqual(result.attempts, 3)
        self.assertEqual(result.raw_attempts, ("not-json", "not-json", "not-json"))
        self.assertTrue(result.parse_failure)
        self.assertEqual(
            result.parsed_output,
            {
                "predicted_label": None,
                "abstain": True,
                "used_insight_ids": [],
                "reasoning_summary": "parse_failure",
            },
        )

    def test_no_retry_for_valid_wrong_or_semantically_weak_output(self) -> None:
        valid_but_wrong = {
            **self.valid,
            "predicted_label": self.config["label_space"][1],
            "reasoning_summary": "Weak.",
            "used_insight_ids": [],
        }
        calls = 0

        def call(prompt: str, attempt: int) -> str:
            nonlocal calls
            calls += 1
            return json.dumps(valid_but_wrong, separators=(",", ":"))

        result = execute_with_retry(call=call, prompt="BASE", parse=self.parse, max_retries=2)
        self.assertEqual(calls, 1)
        self.assertEqual(result.attempts, 1)
        self.assertFalse(result.parse_failure)

    def test_retry_budget_cannot_be_changed(self) -> None:
        with self.assertRaisesRegex(ValueError, "exactly two retries"):
            execute_with_retry(
                call=lambda prompt, attempt: json.dumps(self.valid),
                prompt="BASE",
                parse=self.parse,
                max_retries=1,
            )

    def test_heldout_guard_denies_root_and_manifest_filename_without_opening(self) -> None:
        guard = project_guard(ROOT)
        with self.assertRaises(HeldoutAccessError):
            guard.assert_allowed(ROOT / "tep_heldout/mode1/mode1_1_11.xlsx")
        with self.assertRaises(HeldoutAccessError):
            guard.assert_allowed(ROOT / "somewhere/mode1_normal_12.xlsx")
        allowed = guard.assert_allowed(ROOT / "code/tep_cache/mode1_1_1.xlsx")
        self.assertEqual(allowed.name, "mode1_1_1.xlsx")

    def test_explicit_integrity_verifier_exception_only(self) -> None:
        guard = project_guard(ROOT)
        verifier = ROOT / "phase_b/heldout/verify_heldout_integrity.py"
        self.assertEqual(
            guard.assert_allowed(
                verifier,
                purpose="integrity_verification",
                explicit_integrity_request=True,
            ),
            verifier.resolve(),
        )


if __name__ == "__main__":
    unittest.main()
