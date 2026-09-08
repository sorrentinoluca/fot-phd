from __future__ import annotations

from types import SimpleNamespace
import unittest

from phase_b.exp2.qwen.adapter import QwenOpenAICompatibleAdapter


VALID_OUTPUT = (
    '{"predicted_label":"Normal","abstain":false,'
    '"used_insight_ids":[],"reasoning_summary":"Synthetic fixture."}'
)


class Dumpable(SimpleNamespace):
    def model_dump(self, mode: str = "json"):
        del mode
        result = {}
        for key, value in vars(self).items():
            if isinstance(value, Dumpable):
                result[key] = value.model_dump()
            elif isinstance(value, list):
                result[key] = [
                    item.model_dump() if isinstance(item, Dumpable) else item
                    for item in value
                ]
            else:
                result[key] = value
        return result


class FakeCompletions:
    def __init__(
        self,
        outputs: list[str] | None = None,
        messages: list[Dumpable] | None = None,
    ):
        self.outputs = list(outputs or [VALID_OUTPUT])
        self.messages = list(messages or [])
        self.requests = []

    def create(self, **kwargs):
        self.requests.append(kwargs)
        output = self.outputs.pop(0)
        message = (
            self.messages.pop(0)
            if self.messages
            else Dumpable(content=output, reasoning_content="synthetic reasoning")
        )
        choice = Dumpable(message=message, finish_reason="stop")
        usage = Dumpable(prompt_tokens=100, completion_tokens=20, total_tokens=120)
        return Dumpable(
            id="chatcmpl-test",
            model="fot-exp2-consumer",
            choices=[choice],
            usage=usage,
        )


def fake_client(completions: FakeCompletions):
    return SimpleNamespace(chat=SimpleNamespace(completions=completions))


class AdapterTests(unittest.TestCase):
    def setUp(self):
        self.schema = {
            "type": "object",
            "properties": {"predicted_label": {"type": ["string", "null"]}},
        }

    def test_exact_qwen_request_parameters(self):
        completions = FakeCompletions()
        adapter = QwenOpenAICompatibleAdapter(
            base_url="http://127.0.0.1:8000/v1",
            requested_model="fot-exp2-consumer",
            client=fake_client(completions),
        )
        response = adapter.create_chat_completion(
            prompt="frozen prompt",
            schema=self.schema,
            temperature=0.0,
            seed=20260829,
            max_tokens=1536,
            thinking_token_budget=1024,
        )
        request = completions.requests[0]
        self.assertEqual(request["model"], "fot-exp2-consumer")
        self.assertEqual(request["messages"], [{"role": "user", "content": "frozen prompt"}])
        self.assertEqual(request["temperature"], 0.0)
        self.assertEqual(request["seed"], 20260829)
        self.assertEqual(request["max_tokens"], 1536)
        self.assertEqual(request["extra_body"], {"thinking_token_budget": 1024})
        self.assertTrue(request["response_format"]["json_schema"]["strict"])
        self.assertEqual(response.raw_output, VALID_OUTPUT)
        self.assertEqual(response.reasoning_content, "synthetic reasoning")
        self.assertEqual(response.total_tokens, 120)

    def test_structural_retry_policy_is_reused_unchanged(self):
        completions = FakeCompletions(["not json", VALID_OUTPUT])
        adapter = QwenOpenAICompatibleAdapter(
            base_url="http://127.0.0.1:8000/v1",
            requested_model="fot-exp2-consumer",
            client=fake_client(completions),
        )
        result = adapter.execute_diagnostic(
            prompt="frozen prompt",
            label_space=["Normal"],
            allowed_insight_ids=[],
            schema=self.schema,
            temperature=0.0,
            seed=20260829,
            max_tokens=1536,
            thinking_token_budget=1024,
            max_structural_retries=2,
        )
        self.assertEqual(result.result.attempts, 2)
        self.assertFalse(result.result.parse_failure)
        self.assertEqual(len(completions.requests), 2)
        self.assertEqual(completions.requests[1]["temperature"], 0.0)
        self.assertEqual(completions.requests[1]["seed"], 20260829)
        self.assertEqual(completions.requests[1]["max_tokens"], 1536)
        self.assertEqual(
            completions.requests[1]["extra_body"],
            {"thinking_token_budget": 1024},
        )
        self.assertIn("CORRECTION REQUIRED", completions.requests[1]["messages"][0]["content"])

    def _response_for_message(self, message: Dumpable):
        completions = FakeCompletions(messages=[message])
        adapter = QwenOpenAICompatibleAdapter(
            base_url="http://127.0.0.1:8000/v1",
            requested_model="fot-exp2-consumer",
            client=fake_client(completions),
        )
        return adapter.create_chat_completion(
            prompt="synthetic prompt",
            schema=self.schema,
            temperature=0.0,
            seed=20260829,
            max_tokens=1536,
            thinking_token_budget=1024,
        )

    def test_reasoning_from_message_reasoning_content_has_first_priority(self):
        response = self._response_for_message(
            Dumpable(
                content=VALID_OUTPUT,
                reasoning_content="direct reasoning_content",
                reasoning="direct reasoning",
                model_extra={
                    "reasoning_content": "extra reasoning_content",
                    "reasoning": "extra reasoning",
                },
            )
        )
        self.assertEqual(response.reasoning_content, "direct reasoning_content")
        self.assertEqual(
            response.response_raw["choices"][0]["message"]["reasoning"],
            "direct reasoning",
        )

    def test_reasoning_from_message_reasoning_is_second_priority(self):
        response = self._response_for_message(
            Dumpable(
                content=VALID_OUTPUT,
                reasoning="direct reasoning",
                model_extra={
                    "reasoning_content": "extra reasoning_content",
                    "reasoning": "extra reasoning",
                },
            )
        )
        self.assertEqual(response.reasoning_content, "direct reasoning")

    def test_reasoning_from_model_extra_reasoning_content_is_third_priority(self):
        response = self._response_for_message(
            Dumpable(
                content=VALID_OUTPUT,
                model_extra={
                    "reasoning_content": "extra reasoning_content",
                    "reasoning": "extra reasoning",
                },
            )
        )
        self.assertEqual(response.reasoning_content, "extra reasoning_content")

    def test_reasoning_from_model_extra_reasoning_is_fourth_priority(self):
        response = self._response_for_message(
            Dumpable(
                content=VALID_OUTPUT,
                model_extra={"reasoning": "extra reasoning"},
            )
        )
        self.assertEqual(response.reasoning_content, "extra reasoning")

    def test_reasoning_can_be_completely_absent(self):
        response = self._response_for_message(Dumpable(content=VALID_OUTPUT))
        self.assertIsNone(response.reasoning_content)

    def test_base_url_must_target_v1(self):
        with self.assertRaises(ValueError):
            QwenOpenAICompatibleAdapter(
                base_url="http://127.0.0.1:8000",
                requested_model="fot-exp2-consumer",
                client=fake_client(FakeCompletions()),
            )


if __name__ == "__main__":
    unittest.main()
