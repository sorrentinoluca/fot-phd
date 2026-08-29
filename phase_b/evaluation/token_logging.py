"""Token-count logging without selecting a tokenizer, provider, or model."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class TokenLog:
    prompt_characters: int
    completion_characters: int
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    method: str

    def to_dict(self) -> dict[str, int | str | None]:
        return asdict(self)


def make_token_log(
    *,
    prompt: str,
    completion: str,
    prompt_tokens: int | None = None,
    completion_tokens: int | None = None,
    method: str = "provider_not_available",
) -> TokenLog:
    for name, value in (("prompt_tokens", prompt_tokens), ("completion_tokens", completion_tokens)):
        if value is not None and (type(value) is not int or value < 0):
            raise ValueError(f"{name} must be a non-negative integer or null")
    if (prompt_tokens is None) != (completion_tokens is None):
        raise ValueError("prompt and completion token counts must be supplied together")
    total = None if prompt_tokens is None else prompt_tokens + completion_tokens
    return TokenLog(
        prompt_characters=len(prompt),
        completion_characters=len(completion),
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=total,
        method=method,
    )
