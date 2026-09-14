"""Producer prompts whose only model-authored field is observed_pattern."""

from __future__ import annotations

import json
from typing import Any

from .common import HarnessError


FALSE_POSITIVE_WARNING = """The validator intentionally rejects all of the following spellings or patterns, even in harmless prose: normal, unknown, valve, valvola, feed, step, A/B, and an x followed (possibly after spaces) by mv or meas. This includes phrases such as 'six MV values' and strings such as 'exmv'. Do not use any of them. Refer to variables only with exact declared identifiers such as XMEAS(7) or XMV(3); do not paraphrase physical variable names."""


def build_producer_prompt(
    *,
    agent_id: str,
    local_examples: list[dict[str, str]],
    fixed_contracts: list[dict[str, Any]],
    template: str | None = None,
) -> str:
    template = PRODUCER_TEMPLATE if template is None else template
    owned = [row for row in fixed_contracts if row["source_agent"] == agent_id]
    if len(owned) != 2:
        raise HarnessError(f"{agent_id} must own exactly two fixed insight contracts")
    fixed = [
        {key: row[key] for key in ("insight_id", "source_agent", "pseudolabel", "evidence_scope", "variable_ids")}
        for row in owned
    ]
    if len(local_examples) < 3 or {row["pseudolabel"] for row in local_examples} == {"Normal"}:
        raise HarnessError(f"{agent_id} requires fault and Normal local examples")
    if template.count('{fixed_contracts}') != 1 or template.count('{local_examples}') != 1:
        raise HarnessError('producer template requires exactly one contracts and examples placeholder')
    return template.replace('{fixed_contracts}', json.dumps(fixed, ensure_ascii=False, indent=2)).replace('{local_examples}', json.dumps(local_examples, ensure_ascii=False, indent=2))


PRODUCER_TEMPLATE = (
    'You produce two structured peer insights from the supplied local development examples.\n'
    'Return strict JSON only as {"insights":[...]} with exactly two objects in the supplied order.\n'
    'Copy insight_id, source_agent, pseudolabel, evidence_scope, and variable_ids byte-for-byte. '
    'Write only observed_pattern. Each narrative must be non-empty, at most 800 Unicode characters '
    'and at most 192 tokens under the pinned tokenizer. Use only observations supported by the examples.\n'
    + FALSE_POSITIVE_WARNING + '\n\nFIXED CONTRACTS\n{fixed_contracts}\n\nLOCAL DEVELOPMENT EXAMPLES\n{local_examples}\n'
)
