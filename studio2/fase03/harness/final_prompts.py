"""Offline rendering of the 2,244 unique prompts of the final batch (protocol §4-§5).

Inputs, all frozen and hashed elsewhere:

* the logical inventory of ``final_inventory`` (stable identifiers only);
* the **frozen pilot input manifest** ``84176888...`` -- label space, agents, local
  examples and derangements are the pilot's and are not rebuilt here (rilievo B2);
* the **test-lot input manifest** of 03.11 produced by
  ``evidence/extract_test_lot_evidence.py``: one neutral text per case, the window
  assigned by D1;
* the two insight libraries accepted by 7.2-R: ``G_P`` (122B) and ``G_A`` (27B).

Rendering uses the frozen renderer of §2 for A, B-LF and E-LF and its tracked revision
``protocol_bnolf`` for B-noLF.  Nothing here selects, filters or inspects case content.
"""

from __future__ import annotations

from typing import Any, Callable, Iterable

from studio2.fase03 import protocol, protocol_bnolf
from .common import HarnessError, canonical_json, load_json, sha256_file, sha256_text
from . import final_inventory

LIBRARY_ROLE_BY_TOKEN = {final_inventory.LIBRARY_PRIMARY: "122B",
                         final_inventory.LIBRARY_ALTERNATE: "27B"}

PILOT_INPUT_MANIFEST_SHA256 = "8417688869b75bda8235387ac830018ecdc9030442a860d495418f195f2b4014"


def frozen_label_space(manifest_path) -> list[str]:
    """The label space of the frozen pilot input manifest, authenticated by its SHA-256.

    A rendered row carries ``available_insight_ids`` but not the label space: the label
    space is not prompt bytes, it is the closed set the answer is validated against, and it
    belongs to the frozen manifest (``84176888...``). The runners read it from here, so the
    rendered files -- pinned and already materialised inside a target -- are never touched.
    """
    from pathlib import Path as _Path

    path = _Path(manifest_path)
    if not path.is_file():
        raise HarnessError(f"frozen pilot input manifest not found: {path}")
    observed = sha256_file(path)
    if observed != PILOT_INPUT_MANIFEST_SHA256:
        raise HarnessError("pilot input manifest is not the frozen one: label space refused "
                           f"(SHA-256 {observed})")
    labels = load_json(path).get("label_space")
    if not isinstance(labels, list) or not labels or not all(isinstance(x, str) for x in labels):
        raise HarnessError("the frozen manifest carries no usable label space")
    return list(labels)


def resolve_library_path(entry: dict[str, Any], *, roots: Iterable[Any] = ()) -> Any:
    """Locate one accepted insight library and authenticate its bytes.

    ``LIBRERIE_FINALI_CANDIDATE.json`` records an absolute ``library_path`` that was valid
    on the machine that produced it and is not portable. The artifact is an accepted 7.2-R
    record and is **not** rewritten here: the file is looked up by its recorded path first
    and then by name under the supplied roots, and in every case it is accepted only if its
    SHA-256 matches ``library_file_sha256``.
    """
    from pathlib import Path

    recorded = Path(entry["library_path"])
    candidates = [recorded] + [Path(root) / recorded.name for root in roots]
    for candidate in candidates:
        try:
            if candidate.is_file() and sha256_file(candidate) == entry["library_file_sha256"]:
                return candidate
        except OSError:
            continue
    raise HarnessError(
        f"insight library not found or hash mismatch: {recorded.name}; "
        f"looked in {[str(item) for item in candidates]}")


def _insights(library: Iterable[dict[str, Any]]) -> list[protocol.Insight]:
    return [protocol.Insight(**{key: (tuple(value) if key == "variable_ids" else value)
                                for key, value in item.items()}) for item in library]


def render_entry(entry: dict[str, Any], *, manifest: dict[str, Any],
                 libraries: dict[str, list[protocol.Insight]], cases: dict[str, Any],
                 presentation_label_space=None) -> tuple[str, tuple[str, ...]]:
    case = cases.get(entry["case_id"])
    if case is None:
        raise HarnessError(f"no consumer input for case {entry['case_id']}")
    condition = entry["condition"]
    role = entry["library_role"]
    insights: list[protocol.Insight] = []
    if condition != "A":
        token = LIBRARY_ROLE_BY_TOKEN.get(role)
        if token is None:
            raise HarnessError(f"condition {condition} requires an insight library, got {role!r}")
        insights = libraries[token]
    common = dict(agent_id=entry["recipient_agent"], case=case, manifest=manifest,
                  insights=insights, presentation_label_space=presentation_label_space)
    if condition == protocol_bnolf.CONDITION:
        return protocol_bnolf.render_diagnostic_prompt(**common)
    return protocol.render_diagnostic_prompt(condition=condition, **common)


def render_all(*, inventory: list[dict[str, Any]], manifest: dict[str, Any],
               libraries: dict[str, list[dict[str, Any]]], cases: dict[str, Any],
               presentation_label_space=None,
               token_count: Callable[[str], int] | None = None,
               context_limit: int | None = None,
               reserved_output_tokens: int = 0) -> dict[str, Any]:
    """Render every unique prompt and verify counts, pairing and context arithmetic."""
    prepared = {token: _insights(rows) for token, rows in libraries.items()}
    rows: list[dict[str, Any]] = []
    by_block: dict[str, int] = {}
    by_condition: dict[str, int] = {}
    longest = 0
    counts: list[int] = []
    counts_by_condition: dict[str, list[int]] = {}
    over_context: list[str] = []
    for entry in inventory:
        text, ids = render_entry(entry, manifest=manifest, libraries=prepared, cases=cases,
                                 presentation_label_space=presentation_label_space)
        row = {"prompt_id": entry["stable_id"], "stable_id": entry["stable_id"],
               "block": entry["block"], "condition": entry["condition"],
               "case_id": entry["case_id"], "agent_id": entry["recipient_agent"],
               "library_role": entry["library_role"],
               "available_insight_ids": list(ids),
               "text": text, "prompt_sha256": sha256_text(text),
               "prompt_bytes": len(text.encode("utf-8"))}
        if token_count is not None:
            count = token_count(text)
            row["prompt_tokens"] = count
            longest = max(longest, count)
            counts.append(count)
            counts_by_condition.setdefault(entry["condition"], []).append(count)
            if context_limit is not None and count + reserved_output_tokens > context_limit:
                over_context.append(entry["stable_id"])
        rows.append(row)
        by_block[entry["block"]] = by_block.get(entry["block"], 0) + 1
        by_condition[entry["condition"]] = by_condition.get(entry["condition"], 0) + 1

    if by_block != final_inventory.EXPECTED_UNIQUE:
        raise HarnessError(f"rendered block counts differ from protocol §5: {by_block}")
    if len(rows) != final_inventory.EXPECTED_UNIQUE_TOTAL:
        raise HarnessError(f"rendered {len(rows)} prompts, expected "
                           f"{final_inventory.EXPECTED_UNIQUE_TOTAL}")
    if len({row["prompt_sha256"] for row in rows}) != len(rows):
        raise HarnessError("two distinct identifiers rendered the same prompt bytes")
    if over_context:
        raise HarnessError(f"{len(over_context)} prompts exceed the qualified context")
    summary = {
        "artifact_version": "PROMPT_FINALI_7_4_1",
        "unique_by_block": by_block,
        "unique_by_condition": by_condition,
        "unique_total": len(rows),
        "requests_total": len(rows) * len(final_inventory.REPETITIONS),
        "be_pseudolabel_diff": be_pseudolabel_diff(rows),
        "bnolf_policy_diff": bnolf_policy_diff(rows),
        "max_prompt_tokens": longest if token_count is not None else None,
        "prompt_token_distribution": _distribution(counts) if counts else None,
        "prompt_token_distribution_by_condition": (
            {key: _distribution(value) for key, value in sorted(counts_by_condition.items())}
            if counts else None),
        "context_limit": context_limit,
        "reserved_output_tokens": reserved_output_tokens,
        "prompts_sha256": sha256_text(canonical_json(
            [[row["prompt_id"], row["prompt_sha256"]] for row in rows])),
    }
    return {"rows": rows, "summary": summary}


def _distribution(values: list[int]) -> dict[str, Any]:
    """Synthetic distribution of prompt sizes. Counts only: no prompt text is read."""
    ordered = sorted(values)

    def percentile(fraction: float) -> int:
        if not ordered:
            return 0
        position = fraction * (len(ordered) - 1)
        low = int(position)
        high = min(low + 1, len(ordered) - 1)
        weight = position - low
        return int(round(ordered[low] * (1 - weight) + ordered[high] * weight))

    return {"count": len(ordered), "min": ordered[0], "p50": percentile(0.50),
            "p95": percentile(0.95), "max": ordered[-1],
            "mean": round(sum(ordered) / len(ordered), 1)}


def be_pseudolabel_diff(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """§3.3 on the rendered bytes: B-LF -> E-LF changes pseudolabels and nothing else."""
    by_cell: dict[tuple, dict[str, str]] = {}
    for row in rows:
        if row["condition"] in {"B-LF", "E-LF"}:
            key = (row["block"], row["case_id"], row["agent_id"], row["library_role"])
            by_cell.setdefault(key, {})[row["condition"]] = row["text"]
    paired = {key: value for key, value in by_cell.items() if len(value) == 2}
    identical = [key for key, value in paired.items() if value["B-LF"] == value["E-LF"]]
    outside = []
    for key, value in paired.items():
        head_b = value["B-LF"].split("PEER INSIGHTS", 1)
        head_e = value["E-LF"].split("PEER INSIGHTS", 1)
        if head_b[0] != head_e[0]:
            outside.append(key)
    return {"paired_cells": len(paired), "identical_pairs": len(identical),
            "changed_outside_peer_insights": len(outside),
            "status": "PASS" if paired and not identical and not outside else "FAIL"}


def bnolf_policy_diff(rows: list[dict[str, Any]]) -> dict[str, Any]:
    """Every rendered B-noLF prompt lacks the policy block and nothing else."""
    ablation = [row for row in rows if row["condition"] == protocol_bnolf.CONDITION]
    carrying = [row["prompt_id"] for row in ablation
                if protocol_bnolf.POLICY_HEADING in row["text"]]
    return {"ablation_prompts": len(ablation), "still_carrying_the_policy": len(carrying),
            "status": "PASS" if ablation and not carrying else "FAIL"}
