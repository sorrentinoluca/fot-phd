"""Token-count logging without selecting a tokenizer, provider, or model."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Protocol


class TokenCounter(Protocol):
    """Provider/model-specific counter selected explicitly before freeze."""

    name: str

    def count(self, text: str) -> int:
        ...


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


@dataclass(frozen=True)
class TokenEquivalence:
    tokenizer: str
    left_characters: int
    right_characters: int
    left_tokens: int
    right_tokens: int
    character_equal: bool
    token_equal: bool


def compare_token_counts(
    left: str, right: str, *, tokenizer: TokenCounter
) -> TokenEquivalence:
    """Compare B/E using the explicitly selected model tokenizer."""
    name = getattr(tokenizer, "name", None)
    if not isinstance(name, str) or not name.strip():
        raise ValueError("tokenizer must expose a non-empty name")
    left_tokens = tokenizer.count(left)
    right_tokens = tokenizer.count(right)
    if any(type(value) is not int or value < 0 for value in (left_tokens, right_tokens)):
        raise ValueError("tokenizer counts must be non-negative integers")
    return TokenEquivalence(
        tokenizer=name,
        left_characters=len(left),
        right_characters=len(right),
        left_tokens=left_tokens,
        right_tokens=right_tokens,
        character_equal=len(left) == len(right),
        token_equal=left_tokens == right_tokens,
    )


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
