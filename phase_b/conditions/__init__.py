"""Builders and strict parsers for Phase B conditions A, B, and E."""

from .builders import (
    RenderedPrompt,
    condition_peer_insights,
    render_diagnostic_prompt,
    render_insight_prompt,
    render_peer_insight_block,
)
from .parser import OutputValidationError, parse_diagnostic_output

__all__ = [
    "OutputValidationError",
    "RenderedPrompt",
    "condition_peer_insights",
    "parse_diagnostic_output",
    "render_diagnostic_prompt",
    "render_insight_prompt",
    "render_peer_insight_block",
]
