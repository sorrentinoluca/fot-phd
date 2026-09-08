"""OpenAI-compatible Chat Completions adapter for the EXP2 Qwen lane."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable

import openai
from openai import OpenAI

from phase_b.conditions.parser import parse_diagnostic_output
from phase_b.conditions.retry import RetryResult, execute_with_retry


def _as_dict(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    dump = getattr(value, "model_dump", None)
    if callable(dump):
        return dump(mode="json")
    return None


@dataclass(frozen=True)
class ChatProviderResponse:
    raw_output: str
    reasoning_content: str | None
    requested_model: str
    returned_model: str
    response_id: str | None
    finish_reason: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    usage_raw: dict[str, Any] | None
    response_raw: dict[str, Any]
    sdk_version: str
    api_family: str = "Chat Completions"
    endpoint: str = "/v1/chat/completions"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DiagnosticExecution:
    result: RetryResult
    provider_attempts: tuple[ChatProviderResponse, ...]


class QwenOpenAICompatibleAdapter:
    """Stateless, single-model adapter with provider retries disabled."""

    def __init__(
        self,
        *,
        base_url: str,
        requested_model: str,
        api_key: str = "local-vllm",
        client: Any | None = None,
        timeout_seconds: float = 180.0,
    ) -> None:
        if not base_url.rstrip("/").endswith("/v1"):
            raise ValueError("base_url must end with /v1")
        if not requested_model.strip():
            raise ValueError("requested_model is required")
        self.base_url = base_url.rstrip("/")
        self.requested_model = requested_model
        self.client = client or OpenAI(
            api_key=api_key,
            base_url=self.base_url,
            max_retries=0,
            timeout=timeout_seconds,
        )

    @property
    def sdk_version(self) -> str:
        return openai.__version__

    def create_chat_completion(
        self,
        *,
        prompt: str,
        schema: dict[str, Any],
        temperature: float,
        seed: int,
        max_tokens: int,
    ) -> ChatProviderResponse:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be non-empty text")
        response = self.client.chat.completions.create(
            model=self.requested_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            seed=seed,
            max_tokens=max_tokens,
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "phase_b_diagnostic_output",
                    "strict": True,
                    "schema": schema,
                },
            },
        )
        response_raw = _as_dict(response)
        if response_raw is None:
            raise RuntimeError("chat completion could not be serialized")
        choices = getattr(response, "choices", None)
        if not choices or len(choices) != 1:
            raise RuntimeError("provider must return exactly one choice")
        choice = choices[0]
        message = choice.message
        content = getattr(message, "content", None)
        raw_output = content if isinstance(content, str) else ""
        reasoning = getattr(message, "reasoning_content", None)
        if reasoning is None:
            extra = getattr(message, "model_extra", None)
            if isinstance(extra, dict):
                reasoning = extra.get("reasoning_content")
        usage = getattr(response, "usage", None)
        return ChatProviderResponse(
            raw_output=raw_output,
            reasoning_content=reasoning if isinstance(reasoning, str) else None,
            requested_model=self.requested_model,
            returned_model=str(getattr(response, "model", "")),
            response_id=getattr(response, "id", None),
            finish_reason=getattr(choice, "finish_reason", None),
            prompt_tokens=getattr(usage, "prompt_tokens", None),
            completion_tokens=getattr(usage, "completion_tokens", None),
            total_tokens=getattr(usage, "total_tokens", None),
            usage_raw=_as_dict(usage),
            response_raw=response_raw,
            sdk_version=self.sdk_version,
        )

    def execute_diagnostic(
        self,
        *,
        prompt: str,
        label_space: Iterable[str],
        allowed_insight_ids: Iterable[str],
        schema: dict[str, Any],
        temperature: float,
        seed: int,
        max_tokens: int,
        max_structural_retries: int = 2,
    ) -> DiagnosticExecution:
        attempts: list[ChatProviderResponse] = []

        def call(current_prompt: str, attempt: int) -> str:
            del attempt
            response = self.create_chat_completion(
                prompt=current_prompt,
                schema=schema,
                temperature=temperature,
                seed=seed,
                max_tokens=max_tokens,
            )
            attempts.append(response)
            return response.raw_output

        result = execute_with_retry(
            call=call,
            prompt=prompt,
            parse=lambda raw: parse_diagnostic_output(
                raw,
                label_space=label_space,
                allowed_insight_ids=allowed_insight_ids,
            ),
            max_retries=max_structural_retries,
        )
        return DiagnosticExecution(result=result, provider_attempts=tuple(attempts))
