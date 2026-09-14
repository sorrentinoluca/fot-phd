"""Deterministic balanced selectors for canaries and the continuous audit."""

from __future__ import annotations

from collections import Counter
import math
from typing import Any, Iterable

from .common import HarnessError, sha256_text


CANARY_NAMESPACE = "studio2-fase03-canary-v1"
AUDIT_NAMESPACE = "studio2-fase03-audit-v1"


def _balanced_pick(
    candidates: list[dict[str, Any]],
    *,
    count: int,
    namespace: str,
    selected: list[dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    chosen = [] if selected is None else list(selected)
    available = [row for row in candidates if row not in chosen]
    agents = Counter(row["agent_id"] for row in chosen)
    faults = Counter(row["true_pseudolabel"] for row in chosen)
    conditions = Counter(row["condition"] for row in chosen)
    for _ in range(count):
        if not available:
            raise HarnessError("not enough unique prompt candidates")
        row = min(
            available,
            key=lambda item: (
                agents[item["agent_id"]],
                faults[item["true_pseudolabel"]],
                conditions[item["condition"]],
                sha256_text(f"{namespace}|{item['prompt_id']}|{item['prompt_sha256']}"),
            ),
        )
        chosen.append(row)
        available.remove(row)
        agents[row["agent_id"]] += 1
        faults[row["true_pseudolabel"]] += 1
        conditions[row["condition"]] += 1
    return chosen


def select_canaries(prompts: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = list(prompts)
    required = {"prompt_id", "prompt_sha256", "agent_id", "true_pseudolabel", "condition"}
    if any(not isinstance(row, dict) or not required <= set(row) for row in rows):
        raise HarnessError("canary candidates lack required prompt metadata")
    selected: list[dict[str, Any]] = []
    for condition, quota in (("A", 2), ("B-LF", 4), ("E-LF", 4)):
        candidates = [row for row in rows if row["condition"] == condition]
        new = _balanced_pick(
            [row for row in candidates if row not in selected],
            count=quota,
            namespace=CANARY_NAMESPACE,
            selected=selected,
        )
        selected = new
    if Counter(row["condition"] for row in selected) != Counter({"A": 2, "B-LF": 4, "E-LF": 4}):
        raise AssertionError("unexpected canary condition balance")
    if len({row["agent_id"] for row in selected}) != 8:
        raise HarnessError("canary selector could not cover all eight agents")
    return selected


def select_audit(prompts: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = list(prompts)
    if not rows:
        raise HarnessError("audit requires a non-empty nucleus")
    count = math.ceil(len(rows) * 0.10)
    return _balanced_pick(rows, count=count, namespace=AUDIT_NAMESPACE)
