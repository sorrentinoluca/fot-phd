# Phase B protocol implementation status

Status: **pre-freeze adversarial audit hardened; not protocol-frozen**.

This document records software readiness only. It contains no definitive local
insight, real inference, held-out result, or authorization to access held-out.

## Adversarial audit finding and correction

The audit found one reversible prompt-side metadata channel in the original
implementation: `local_knowledge/local_examples.json` grouped examples directly
under `agent_1` … `agent_4`. Because each list contains exactly one fault
pseudolabel, the complete prompt-facing artifact encoded an
`agent -> owned pseudolabel` crosswalk even though the diagnostic renderer passed
only the selected list.

The prompt-facing artifact now uses opaque `LKP-001` … `LKP-004` pack keys and
contains no agent identifier. The `agent -> pack` assignment is stored only in
`config/evaluator_side/local_example_sources.json`. The diagnostic builder is
given the selected four-item list, never the pack ID, agent topology, source
filename, source batch, real class, or diagnostic case ID. The mandatory
`source_agent` remains inside each peer insight for provenance; no diagnostic
prompt receives a second source-agent ownership crosswalk.

No additional leakage channel was found in insight IDs, evidence scope, observed
patterns, prompt headers, agent descriptions, label-space rendering, filenames,
case identifiers, or serialized prompt comments/metadata. Validation now rejects
any configured pseudolabel or evaluator-only real-class identifier in every
prompt-facing insight field other than `pseudolabel`.

## Condition B/E invariants

For every receiving agent:

- B contains the three peer pseudolabels exactly twice each;
- E contains exactly the same label multiset;
- every `observed_pattern -> pseudolabel` association changes (no fixed point);
- IDs, order, observed patterns, source agents, and evidence scopes are unchanged;
- replacing every pseudolabel value in both rendered peer blocks with `<LABEL>`
  makes the UTF-8 byte streams identical;
- raw B/E character counts remain equal.

The tokenizer interface is implemented but no arbitrary tokenizer is treated as
authoritative. `execution.tokenizer` remains null and blocks real execution.
After provider/model selection, its authoritative tokenizer must be recorded and
B/E token counts compared or any difference documented before protocol freeze.

## Diagnostic schema and retry

The exact output keys are `predicted_label`, `abstain`, `used_insight_ids`, and
`reasoning_summary`. `abstain=false` requires one exact supplied label;
`abstain=true` requires `predicted_label=null`. Unknown labels and either
inconsistency are structural failures.

Execution uses one initial attempt plus at most two retries. Retry occurs only
after invalid JSON, invalid schema, unknown label, or abstain/prediction
inconsistency. It does not occur for a wrong valid prediction, weak reasoning,
unused insights, or perceived semantic quality. Three structurally invalid
attempts return `ABSTAIN / parse_failure`, count as incorrect in primary metrics,
and retain all three raw outputs.

## R=3 aggregation and metrics

The definitive aggregation rule is:

- two or three equal valid labels -> that label;
- otherwise -> aggregate abstention.

Thus `X,X,Y` and `X,X,ABSTAIN` produce `X`; `X,Y,Z`, `X,Y,ABSTAIN`, and
`ABSTAIN,ABSTAIN,X` abstain. Primary accuracy uses aggregate predictions.
Repetition-level predictions remain saved and are reported only for stochastic
stability.

Primary:

- `Delta_unseen = accuracy_B_unseen - accuracy_A_unseen` after aggregation;
- 36 aggregate unseen agent-case observations over 12 physical fault-run clusters;
- `Delta_E = accuracy_E_unseen - accuracy_A_unseen`;
- specificity comparison `Delta_unseen > Delta_E`, equivalently
  `accuracy_B_unseen > accuracy_E_unseen`;
- support reports `Delta_unseen > 0`, positive effect for at least 3/4 agents,
  helped versus harmed, and `Delta_unseen > Delta_E`.

Secondary seen reporting separates local-fault-seen accuracy from Normal
accuracy. H2 uses `epsilon = 0`; neither secondary quantity is promoted to a new
primary metric.

## Bootstrap

The primary paired bootstrap is configured for 10,000 draws and frozen seed
`20260829`. It resamples `physical_case_id`, not the 36 agent-case observations.
Resampling is stratified by true opaque pseudoclass: exactly four strata with
three physical fault-runs per stratum. All three unseen aggregate agent rows of a
sampled physical run remain together. Abstentions are incorrect.

## Completed safeguards

- Four-agent opaque-label topology and evaluator-only real mapping.
- Development-only local examples: fault batches 1–2 and Normal N1–N2.
- Prompt-facing opaque knowledge packs; no structured numerical JSON.
- Exact-two label-neutral insight schema and peer-only six-insight filtering.
- Fixed three-label derangements and strong normalized-byte B/E identity test.
- Byte-identical A/B/E diagnostic templates outside the peer block.
- Strict parser, bounded structural retry, raw-attempt persistence.
- Aggregate primary metrics plus separate repetition-level reporting.
- Separate local-fault-seen and Normal secondary metrics with epsilon zero.
- 12-cluster, four-stratum paired bootstrap.
- Held-out access guard and Phase A frozen-hash regression test.

## Still requires researcher decision

- LLM provider, exact model/version, and authoritative tokenizer.
- Confirmation of temperature-zero and seed support, or a documented supported
  fixed alternative before freeze.
- Provider context and output-token limits.
- Researcher approval of prompt wording before definitive insight generation.

No original batch 8–10, held-out workbook, or held-out manifest was opened by
this audit. No `phase-b-protocol-frozen` tag has been created.
