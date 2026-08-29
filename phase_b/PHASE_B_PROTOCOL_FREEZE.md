# Phase B FoT protocol freeze

Protocol version: `phase-b-fot-1.0.0`

Status: **frozen before independent held-out evaluation**

This document freezes the Phase B experimental protocol. It reports structure,
provenance, and decision rules only; it intentionally contains no insight text
or diagnostic result.

## A. Data boundary

- Insight generation and local knowledge use only development fault batches
  1–5 and the corresponding frozen Normal development baseline.
- Diagnostic few-shot examples are fixed to fault batches 1–2 and Normal blocks
  N1–N2. This is distinct from the five-batch insight-generation evidence.
- Batches 6–7 were used only for completed plumbing and technical validation.
- Original batches 8–10 are not the Phase B final test.
- The final held-out consists of 15 independently generated cases already
  frozen by commit `86baaa65e72cea22ecb89dd0e7b213aea5a1284b`
  and tag `phase-b-heldout-frozen`. Their raw workbook bytes are not tracked and
  remain diagnostically unopened at this protocol freeze.

## B. Agents

There are exactly four agents. Each agent has Normal plus exactly one local
opaque fault pseudoclass; no agent owns more than one fault pseudoclass.

## C. Pseudolabels

Fault labels are opaque, equal-length `CLS-` tokens. The real-to-opaque mapping
is evaluator-side only and is not supplied to diagnostic prompts. Its frozen
identity is recorded by hash in the machine-readable freeze and global manifest.

## D. Insights

The definitive library contains exactly eight insights: two from each agent.
Each generation used all five local development batches. The first structurally
valid output was accepted for all four agents, with one attempt and zero retry
per agent. There was no human selection, content-based regeneration, ranking,
merge, deduplication, or editing. This document does not reproduce the insights.

## E. Federation

Federation is peer-only: self and Normal insights are excluded.

- Condition B gives each agent exactly six genuine insights: two from each of
  the three peer pseudoclasses.
- Condition E uses the same six insight IDs, order, source agent, evidence scope,
  and observed text as B. Only pseudolabel association changes according to the
  already frozen per-agent derangement. The derangement has zero fixed points.

## F. Conditions

- **A — isolated:** local examples, no federated insights.
- **B — FoT:** local examples plus the six genuine peer-only insights.
- **E — corrupted control:** the same peer evidence as B with only the frozen
  pseudolabel derangement.

Condition D and oracle variants are excluded from the primary proof of concept.

## G. LLM execution

- Provider: OpenAI.
- Requested and returned model: `gpt-5.6-terra`.
- Reasoning effort: `medium`.
- Temperature: unsupported, therefore `null`.
- Seed: unsupported, therefore `null`.
- Output enforcement: strict Structured Outputs using the compatible provider
  schema, followed by the unchanged, more restrictive local parser/validator.
- Token accounting source: `response.usage`.

## H. Repetitions and aggregation

Every agent–case–condition is executed with `R = 3`. Exactly repetitions 1, 2,
and 3 are required and must share the same input hash. A valid pseudolabel with
at least two votes is the aggregate prediction. If no valid label has a two-vote
majority, the aggregate abstains. Abstention counts as incorrect in the primary
analysis.

## I. Metrics and hypotheses

The primary metric is:

`Delta_unseen = accuracy_B_unseen - accuracy_A_unseen`

The pre-specified support criteria are:

- `Delta_unseen > 0`;
- positive `Delta_unseen` for at least three of four agents;
- `helped > harmed`;
- `Delta_unseen > Delta_E`, where `Delta_E` is the E-minus-A unseen delta.

For H2, `epsilon = 0`. Normal accuracy and local-fault-seen accuracy are
secondary outcomes and are reported separately.

## J. Statistics

The primary statistical units are 12 physical fault-run clusters: three runs
for each of four true pseudoclasses. The unseen comparison contains 36 aggregate
agent–case observations because every physical fault run is unseen to three
agents; these 36 observations are not independent.

The paired cluster bootstrap uses 10,000 draws with seed `20260829`, resamples
`physical_case_id` within each of the four true-pseudolabel strata, and retains
all three unseen aggregate agent rows for every sampled physical run.

## K. Immutability

Before final held-out evaluation, the following cannot change: pseudolabel
mapping, local examples, prompt templates, definitive insights, B/E libraries,
derangements, provider/model/execution settings, `R`, retry policy, aggregation,
conditions, metrics, hypotheses, bootstrap settings, parser, validator, or
schemas.

Any later modification invalidates this freeze. It must be documented as a new
protocol version before the independent held-out is reopened. The exact frozen
configuration is `phase_b/config/phase_b_protocol_frozen.json`; repository-
relative artifact hashes are in `phase_b/PHASE_B_PROTOCOL_HASHES.json`.
