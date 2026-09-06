# Protocol amendment — Condition C: Centralized Full-Information Pooled ICL

Amendment ID: `C-001`

Base protocol freeze:
`3d86f64d43e14e7e0de520cb047ca1043bf9c1c0`

Historical tag: `phase-b-protocol-frozen`

## Reason and timing

This amendment extends the frozen Exp 1 protocol (Conditions A/B/E) with a
post-hoc centralized full-information reference condition (Condition C).

The decision was made after all Exp 1 inference was complete and evaluated,
and before any Condition C diagnostic LLM call:

- frozen verbalization commit:
  `32f0856040614870d3784a4811e76cee0eee77e3`;
- completed Condition C inference at decision: `0/45`;
- observed Condition C predictions: zero;
- observed Condition C accuracy or other diagnostic metrics: zero.

Condition C is designed and executed *after* observing the results of
A/B/E on the same held-out set. Its role is that of a **post-hoc
exploratory reference**, not an ex ante planned condition (see §6.5 of
PLAN_CENTRAL_POOLED_ICL.md).

## Definition of Condition C

Condition C uses a single centralized agent (`agent_id = "central"`)
with a **receiver-independent** context containing:

- **10 pooled examples**: union of the 4 local knowledge packs
  (LKP-001..LKP-004), deduplicated on the 2 shared Normal examples.
  Covers all 5 pseudolabel classes (2 examples each).
- **8 pooled insights**: all insights (INS-001..INS-008) from
  `pooled_insights.json`.

The prompt template is byte-identical to the A/B/E template. The output
schema, model (`gpt-5.6-terra`), reasoning effort (`medium`), retry policy
(max 2 structural retries), and `R = 3` majority aggregation rule are
unchanged from Exp 1.

"Full-information" refers to the union of prompt-facing frozen artifacts
(labeled examples + textual insights), not to the totality of source texts.

## Scheduling

The Condition C schedule is a **request-level** schedule with 45 entries
(15 cases × 3 repetitions). Ordering is deterministic:
`(pilot DESC, physical_case_id ASC, repetition ASC)`.

- **Pilot entries** (sequence_index 0..14): 5 pilot cases × 3 repetitions.
  Pilot cases are PBH-001 (Normal), PBH-004 (F1), PBH-007 (F8),
  PBH-010 (F10), PBH-013 (F13) — one per class, selected as the first
  case per class in the manifest.
- **Non-pilot entries** (sequence_index 15..44): remaining 10 cases × 3
  repetitions.

C-Pilot is the first blind tranche of C-Full, not a separate schedule.
The `--pilot-only` flag restricts execution to sequence_index 0..14;
subsequent execution without the flag resumes from sequence_index 15.

The generated schedule is `icl/full_evaluation/c_schedule.json`, with SHA-256
`3f1b102a89ecd9202fd045a8a39912380e534f68f1675574c7bb3d6ecaf4b986`.

## Mandatory statelessness

Every Condition C inference request is independent and stateless, identical
to the Exp 1 statelessness requirements (Amendment 001). Each request
contains one complete self-contained prompt with no conversation history,
`previous_response_id`, or cross-request state. The `stateless` field in
each `CRunRecord` is invariantly `true`.

## Firewall between inference and evaluation

- The inference-side freeze manifest (`freeze_manifest_inference.json`) is
  verified by the runner before any LLM call. The runner never accesses
  the evaluator-side manifest or pseudolabel mapping.
- The evaluator-side freeze manifest (`freeze_manifest_evaluator.json`) is
  verified by `evaluate_c_predictions.py` only after all Condition C
  predictions are frozen. The evaluator never modifies inference artifacts.
- No join with ground truth occurs until all 45 Condition C records are
  complete and frozen.

## Evaluation metrics

- `accuracy_C_fault`: fraction correct over the 12 held-out fault cases.
- `accuracy_C_normal`: fraction correct over the 3 held-out Normal cases.
- `delta_C_minus_B`: paired comparison (R5 §5.2), computed over the 12
  fault cases only, using the set of 3 unseen agents per fault case from
  Condition B.
- Bootstrap 95% CI on `delta_C_minus_B`: 12 clusters, 4 strata × 3,
  10000 draws, seed 20260906, percentile method.

## Scope of the amendment

This amendment adds Condition C as a post-hoc exploratory reference. It
does not change the held-out data, verbalizations, pseudolabels, local
examples, insights, B/E libraries, derangements, prompts, provider/model,
reasoning effort, retry policy, `R`, aggregation rule, hypotheses, or
existing Exp 1 metrics and bootstrap results.

The machine-readable source is
`icl/full_evaluation/protocol_amendment_c.json`.
