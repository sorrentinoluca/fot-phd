from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
from types import SimpleNamespace
import unittest

from phase_b.execution.openai_adapter import OpenAIAdapter
from phase_b.final_evaluation.build_inference_schedule import (
    build_schedule,
    canonical_schedule_bytes,
    load_amendment,
)


ROOT = Path(__file__).resolve().parents[2]
SCHEDULE_PATH = ROOT / "phase_b/final_evaluation/inference_schedule.json"
RUNNER_PATH = ROOT / "phase_b/final_evaluation/build_inference_schedule.py"


class _Usage:
    input_tokens = 1
    output_tokens = 1
    total_tokens = 2

    def model_dump(self, *, mode: str) -> dict:
        del mode
        return {"input_tokens": 1, "output_tokens": 1, "total_tokens": 2}


class _Response:
    output_text = "{}"
    model = "gpt-5.6-terra"
    id = "response_fixture"
    _request_id = "request_fixture"
    usage = _Usage()

    def model_dump(self, *, mode: str) -> dict:
        del mode
        return {"id": self.id, "model": self.model, "output_text": self.output_text}


class _Responses:
    def __init__(self) -> None:
        self.calls: list[dict] = []

    def create(self, **kwargs):
        self.calls.append(kwargs)
        return _Response()


class ExecutionScheduleAmendmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.amendment = load_amendment()
        cls.schedule = json.loads(SCHEDULE_PATH.read_text(encoding="utf-8"))

    def test_exact_cardinality_uniqueness_and_nested_order(self) -> None:
        self.assertEqual(len(self.schedule), 540)
        keys = {
            (
                entry["physical_case_id"],
                entry["agent_id"],
                entry["condition"],
                entry["repetition"],
            )
            for entry in self.schedule
        }
        self.assertEqual(len(keys), 540)
        self.assertEqual(len({entry["block_index"] for entry in self.schedule}), 180)
        self.assertEqual([entry["sequence_index"] for entry in self.schedule], list(range(540)))
        expected = build_schedule(self.amendment)
        self.assertEqual(self.schedule, expected)

    def test_condition_and_global_position_balance(self) -> None:
        condition_counts = Counter(entry["condition"] for entry in self.schedule)
        self.assertEqual(condition_counts, Counter({"A": 180, "B": 180, "E": 180}))
        position_counts = Counter(
            (entry["condition"], entry["position_in_block"])
            for entry in self.schedule
        )
        self.assertEqual(
            position_counts,
            Counter({(condition, position): 60 for condition in "ABE" for position in (1, 2, 3)}),
        )

    def test_per_agent_position_balance(self) -> None:
        counts = Counter(
            (entry["agent_id"], entry["condition"], entry["position_in_block"])
            for entry in self.schedule
        )
        expected = Counter(
            {
                (f"agent_{agent}", condition, position): 15
                for agent in range(1, 5)
                for condition in "ABE"
                for position in (1, 2, 3)
            }
        )
        self.assertEqual(counts, expected)

    def test_deterministic_regeneration_and_frozen_sha(self) -> None:
        first = canonical_schedule_bytes(build_schedule(self.amendment))
        second = canonical_schedule_bytes(build_schedule(self.amendment))
        self.assertEqual(first, second)
        self.assertEqual(first, SCHEDULE_PATH.read_bytes())
        self.assertEqual(
            hashlib.sha256(first).hexdigest(),
            self.amendment["inference_schedule"]["sha256"],
        )

    def test_scheduler_is_label_blind(self) -> None:
        source = RUNNER_PATH.read_text(encoding="utf-8").lower()
        forbidden = (
            "class_offline",
            "fault_id",
            "pseudolabel",
            "neutral_text",
            "xmeas",
            "xmv",
            "prediction",
            "insight",
        )
        self.assertTrue(all(token not in source for token in forbidden))

    def test_adapter_requests_are_stateless(self) -> None:
        responses = _Responses()
        adapter = OpenAIAdapter(
            requested_model="gpt-5.6-terra",
            client=SimpleNamespace(responses=responses),
        )
        adapter.create_response(prompt="complete-one", reasoning_effort="medium")
        adapter.create_response(prompt="complete-two", reasoning_effort="medium")
        self.assertEqual(len(responses.calls), 2)
        for index, request in enumerate(responses.calls, start=1):
            self.assertEqual(request["input"], f"complete-{'one' if index == 1 else 'two'}")
            self.assertFalse(request["store"])
            self.assertNotIn("previous_response_id", request)
            self.assertNotIn("conversation", request)
            self.assertNotIn("thread", request)
            self.assertNotIn("session", request)


if __name__ == "__main__":
    unittest.main()
