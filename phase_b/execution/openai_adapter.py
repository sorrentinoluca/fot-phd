"""Isolated OpenAI Responses API adapter for the Phase B protocol."""

from __future__ import annotations

from dataclasses import asdict, dataclass
import os
from pathlib import Path
from typing import Any, Iterable

import openai
from openai import OpenAI

from phase_b.conditions.parser import parse_diagnostic_output
from phase_b.conditions.retry import RetryResult, execute_with_retry


ROOT = Path(__file__).resolve().parents[2]
DIAGNOSTIC_SCHEMA = (
    ROOT / "phase_b" / "conditions" / "diagnostic_output.openai.schema.json"
)
UNSET = object()


@dataclass(frozen=True)
class ProviderResponse:
    raw_output: str
    requested_model: str
    returned_model: str
    response_id: str | None
    request_id: str | None
    input_tokens: int | None
    output_tokens: int | None
    total_tokens: int | None
    usage_raw: dict[str, Any] | None
    response_raw: dict[str, Any]
    sdk_version: str
    api_family: str = "Responses API"
    endpoint: str = "/v1/responses"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class DiagnosticExecution:
    result: RetryResult
    provider_attempts: tuple[ProviderResponse, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "result": asdict(self.result),
            "provider_attempts": [item.to_dict() for item in self.provider_attempts],
        }


def _as_dict(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    if isinstance(value, dict):
        return value
    model_dump = getattr(value, "model_dump", None)
    if callable(model_dump):
        return model_dump(mode="json")
    return None


class OpenAIAdapter:
    """One-model adapter with SDK retries disabled and local structural retries."""

    def __init__(
        self,
        *,
        requested_model: str,
        client: Any | None = None,
        timeout_seconds: float = 120.0,
    ) -> None:
        if not requested_model.strip():
            raise ValueError("requested_model is required")
        if client is None:
            if not os.environ.get("OPENAI_API_KEY"):
                raise RuntimeError(
                    "OPENAI_API_KEY is required in the environment; no credential file is read"
                )
            client = OpenAI(max_retries=0, timeout=timeout_seconds)
        self.client = client
        self.requested_model = requested_model

    @property
    def sdk_version(self) -> str:
        return openai.__version__

    def create_response(
        self,
        *,
        prompt: str,
        reasoning_effort: str | None,
        schema: dict[str, Any] | None = None,
        temperature: float | None | object = UNSET,
        seed: int | None | object = UNSET,
        max_output_tokens: int = 512,
    ) -> ProviderResponse:
        if not isinstance(prompt, str) or not prompt.strip():
            raise ValueError("prompt must be non-empty text")
        kwargs: dict[str, Any] = {
            "model": self.requested_model,
            "input": prompt,
            "max_output_tokens": max_output_tokens,
            "store": False,
        }
        if reasoning_effort is not None:
            kwargs["reasoning"] = {"effort": reasoning_effort}
        if schema is not None:
            kwargs["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": "phase_b_diagnostic_output",
                    "schema": schema,
                    "strict": True,
                }
            }
        if temperature is not UNSET:
            kwargs["temperature"] = temperature
        if seed is not UNSET:
            kwargs["extra_body"] = {"seed": seed}

        response = self.client.responses.create(**kwargs)
        response_raw = _as_dict(response)
        if response_raw is None:
            raise RuntimeError("OpenAI response could not be serialized")
        usage_raw = _as_dict(getattr(response, "usage", None))
        input_tokens = getattr(getattr(response, "usage", None), "input_tokens", None)
        output_tokens = getattr(getattr(response, "usage", None), "output_tokens", None)
        total_tokens = getattr(getattr(response, "usage", None), "total_tokens", None)
        return ProviderResponse(
            raw_output=str(getattr(response, "output_text", "")),
            requested_model=self.requested_model,
            returned_model=str(getattr(response, "model", "")),
            response_id=getattr(response, "id", None),
            request_id=getattr(response, "_request_id", None),
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            total_tokens=total_tokens,
            usage_raw=usage_raw,
            response_raw=response_raw,
            sdk_version=self.sdk_version,
        )

    def execute_diagnostic(
        self,
        *,
        prompt: str,
        label_space: Iterable[str],
        allowed_insight_ids: Iterable[str],
        reasoning_effort: str | None,
        schema: dict[str, Any] | None,
        temperature: float | None | object = UNSET,
        seed: int | None | object = UNSET,
        max_output_tokens: int = 512,
        max_structural_retries: int = 2,
    ) -> DiagnosticExecution:
        provider_attempts: list[ProviderResponse] = []

        def call(current_prompt: str, attempt: int) -> str:
            del attempt
            response = self.create_response(
                prompt=current_prompt,
                reasoning_effort=reasoning_effort,
                schema=schema,
                temperature=temperature,
                seed=seed,
                max_output_tokens=max_output_tokens,
            )
            provider_attempts.append(response)
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
        return DiagnosticExecution(result=result, provider_attempts=tuple(provider_attempts))
