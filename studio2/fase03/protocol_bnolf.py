"""Tracked revision of the renderer for the ablation arm ``B-noLF`` (author decision D2).

``protocol.py`` is frozen at SHA-256 ``791fa347...`` and is **not** modified in place.
This file is the new, separately hashed revision required by MAINTENANCE Sec.8.2: it
reuses the frozen renderer and defines ``B-noLF`` by subtraction, so the definition
cannot drift.

    B-noLF prompt  ==  B-LF prompt  minus the DECISION POLICY block, and nothing else.

The subtraction is literal: the frozen renderer joins its sections with a blank line, so
the two sections ``DECISION POLICY`` and ``LOCAL_FIRST_POLICY`` form one contiguous run of
bytes.  That exact run is removed, once, and its removal is verified against the frozen
B-LF prompt before the result is returned.  Peer insights, label space, local examples,
case text, output schema and trailing instructions are the B-LF ones, byte for byte.
"""

from __future__ import annotations

import difflib
from pathlib import Path
from typing import Any, Iterable

from . import protocol
from .protocol import ContractError

FROZEN_PROTOCOL_SHA256 = "791fa347e97ca49e15a8b7ca1e02e0e38c0be37e23eece092c8a094e9a653d1e"
PROTOCOL_PATH = Path(protocol.__file__).resolve()

CONDITION = "B-noLF"
BASE_CONDITION = "B-LF"
POLICY_HEADING = "DECISION POLICY"
# The frozen renderer emits "\n\n".join(sections); the policy heading and its body are two
# consecutive sections, hence this exact byte run inside every B-LF prompt.
POLICY_BLOCK = POLICY_HEADING + "\n\n" + protocol.LOCAL_FIRST_POLICY + "\n\n"

# Conditions that reach a provider in the final batch (Sec.4 of the final protocol).
FINAL_CONDITIONS = (*protocol.CONDITIONS, CONDITION)


def verify_frozen_renderer(path: Path | None = None) -> str:
    """Fail closed if the frozen renderer this revision builds on has changed."""
    target = path or PROTOCOL_PATH
    observed = protocol.sha256_file(target)
    if observed != FROZEN_PROTOCOL_SHA256:
        raise ContractError(
            f"frozen renderer changed: expected {FROZEN_PROTOCOL_SHA256}, got {observed}")
    return observed


def render_diagnostic_prompt(
    *,
    agent_id: str,
    condition: str = CONDITION,
    case: dict[str, Any],
    manifest: dict[str, Any],
    insights: list[protocol.Insight],
    presentation_label_space: Iterable[str] | None = None,
    verify_renderer: bool = True,
) -> tuple[str, tuple[str, ...]]:
    """Render the ablation prompt: the frozen B-LF prompt minus the local-first policy."""
    if condition != CONDITION:
        raise ContractError(f"this revision renders {CONDITION} only, not {condition!r}")
    if verify_renderer:
        verify_frozen_renderer()
    base_text, insight_ids = protocol.render_diagnostic_prompt(
        agent_id=agent_id, condition=BASE_CONDITION, case=case, manifest=manifest,
        insights=insights, presentation_label_space=presentation_label_space)
    if base_text.count(POLICY_BLOCK) != 1:
        raise ContractError("the frozen B-LF prompt does not contain the policy block exactly once")
    text = base_text.replace(POLICY_BLOCK, "", 1)
    # The only difference admitted, verified on the bytes themselves.
    if len(base_text.encode("utf-8")) - len(text.encode("utf-8")) != len(POLICY_BLOCK.encode("utf-8")):
        raise ContractError("policy removal is not a single literal deletion")
    if POLICY_HEADING in text or protocol.LOCAL_FIRST_POLICY in text:
        raise ContractError("the local-first policy survived the ablation")
    restored = _restore(text, base_text)
    if restored != base_text:
        raise ContractError("B-noLF is not B-LF minus the policy block alone")
    return text, insight_ids


def _restore(text: str, base_text: str) -> str:
    """Re-insert the policy block at its original offset; must rebuild B-LF exactly."""
    offset = base_text.index(POLICY_BLOCK)
    return text[:offset] + POLICY_BLOCK + text[offset:]


def render_pair(**kwargs: Any) -> dict[str, Any]:
    """Render B-LF and B-noLF for the same cell and return both with their hashes."""
    verify_renderer = kwargs.pop("verify_renderer", True)
    if verify_renderer:
        verify_frozen_renderer()
    base_text, base_ids = protocol.render_diagnostic_prompt(condition=BASE_CONDITION, **kwargs)
    text, ids = render_diagnostic_prompt(condition=CONDITION, verify_renderer=False, **kwargs)
    if base_ids != ids:
        raise ContractError("the ablation changed the supplied peer insight identifiers")
    return {
        "b_lf_text": base_text, "b_lf_sha256": protocol.sha256_text(base_text),
        "b_nolf_text": text, "b_nolf_sha256": protocol.sha256_text(text),
        "used_insight_ids": list(ids),
        "removed_bytes": len(base_text.encode("utf-8")) - len(text.encode("utf-8")),
    }


def policy_diff(pair: dict[str, Any]) -> str:
    """Unified diff B-LF -> B-noLF; the evidence attached to the decision."""
    return "".join(difflib.unified_diff(
        pair["b_lf_text"].splitlines(keepends=True),
        pair["b_nolf_text"].splitlines(keepends=True),
        fromfile="B-LF", tofile="B-noLF", n=2))


def diff_is_policy_only(pair: dict[str, Any]) -> bool:
    """True when every removed line belongs to the policy block and nothing is added."""
    removed = [line[1:] for line in policy_diff(pair).splitlines()
               if line.startswith("-") and not line.startswith("---")]
    added = [line for line in policy_diff(pair).splitlines()
             if line.startswith("+") and not line.startswith("+++")]
    expected = [line for line in POLICY_BLOCK.splitlines() if line]
    return not added and [line for line in removed if line] == expected
