# EXP3_V2 minimal confirmatory evaluation protocol 001

Status: `PRE_FREEZE_DRAFT`

Prospective harness tag: `exp3-v2-evaluation-harness-frozen-001`

Prospective results tag: `exp3-v2-results-frozen-001`

This protocol is prepared after the public inference-data freeze and before any
EXP3_V2 prediction is joined to evaluator truth. It authorizes no evaluation by
itself. The production evaluator refuses to run until this harness is frozen in
a clean detached checkout under the annotated harness tag.

## Scope

The package is confirmatory and minimal. It produces only:

1. condition-wise primary unseen counts and accuracies for A, B and E;
2. the primary `B-A` and supporting `B-E` contrasts;
3. the complete 10,000-draw paired cluster-bootstrap distributions and 95%
   percentile intervals for those two contrasts;
4. condition-wise descriptive counts and accuracies for local-seen, Normal and
   overall populations;
5. the frozen success decisions already specified by the EXP3_V2 source
   protocol; and
6. a deterministic output hash manifest.

It excludes pooled Experiment 1 + EXP3_V2 analysis, per-agent tables,
helped/harmed tables, repetition-stability summaries, confusion matrices,
per-pseudolabel recall, per-agent tables, pooled analyses, p-values and any new
exploratory or class-specific analysis. The approved secondary descriptive
populations receive no bootstrap interval, success criterion or inferential
promotion.

## Immutable boundaries

The harness binds the seven annotated tags and peeled commits recorded in
`EXP3_V2_EVALUATION_HARNESS_MANIFEST_001.json`. All checkouts must be detached,
clean and exact. The inference-data tag contains exactly 360 already-frozen R=3
aggregate records. Repetition records are provenance only and never replace the
aggregate records as the primary prediction source.

## Units and denominators

- Repetitions: 1,080 total and 360 per condition; not a primary analysis unit.
- Aggregates: 360 total and 120 per condition.
- Primary population: 72 locally-unseen fault agent-cases per condition.
- Secondary local-seen population: 24 fault agent-cases per condition.
- Secondary Normal population: 24 agent-cases per condition.
- Secondary overall population: all 120 agent-cases per condition.
- Independent sampling unit: 24 physical fault runs.
- Strata: four true faults with six physical runs each.
- Every sampled physical run retains its three unseen receiving-agent rows.
- A, B and E remain paired within physical case and receiving agent.

Missing, duplicate, reordered or unexpected records abort evaluation. There is
no denominator reduction, imputation or outcome-based exclusion. Unseen,
local-seen and Normal must be pairwise disjoint and their union must equal the
overall population exactly. For each reported population, `correct + incorrect`
equals its denominator. `abstentions` is reported separately as a subset of
`incorrect`, preserving the frozen rule that every abstention is inaccurate.

## Labels and Condition E

Evaluator truth uses the frozen mapping `F1 -> CLS-ZOGAA`,
`F8 -> CLS-OJNSG`, `F10 -> CLS-R463B`, `F13 -> CLS-Z3ISU`, and
`Normal -> Normal`. The case plan and populated data manifest must agree in
canonical order, condition, attempt 0 and seed before the mapping is applied.

Condition E altered only the labels attached to peer insights during prompt
construction. Its outputs remain in the global opaque label space. Evaluation
therefore compares E directly with the same true opaque label as A and B; it
does not invert or otherwise decode the E derangement.

## Aggregation and failure treatment

The frozen aggregation rule is one valid label with at least two of three
votes; otherwise aggregate abstention. A parse-failure repetition is an
abstention. Aggregate abstention is incorrect. The evaluator verifies the
frozen aggregate against its three recorded outcomes but computes confirmatory
statistics only from the frozen aggregate result.

## Confirmatory estimands

For `C` in `{A,B,E}`:

`accuracy_C_unseen = correct frozen aggregates / 72`.

The primary contrast is `B-A`. Replication is supported only if its observed
value is positive and the lower endpoint of its paired cluster-bootstrap 95%
interval is strictly positive.

The supporting semantic-specificity contrast is `B-E`. Semantic specificity
is supported when its observed value is positive. Its bootstrap interval is
reported, but interval exclusion of zero is not a gate.

There is one primary contrast and no multiplicity adjustment. No supporting or
excluded analysis may be promoted to co-primary status.

The pre-specified secondary outputs are descriptive only. For each condition,
report local-seen accuracy and counts over 24 rows, Normal accuracy and counts
over 24 rows, and overall accuracy and counts over 120 rows. Do not compute or
report secondary bootstrap intervals or secondary success criteria.

## Bootstrap

Use NumPy `default_rng(320031)`. For each of 10,000 draws, sample six physical
case IDs with replacement within each of the four sorted true-pseudolabel
strata. Retain all three unseen receiving-agent rows for every sampled case.
Use the same sampled rows for B-A and B-E. Report percentile 95% intervals using
`numpy.quantile` default linear interpolation at 0.025 and 0.975. Do not persist
individual draws anywhere else. The bootstrap artifact preserves both complete
10,000-value distributions in generated order as the audit record.

## Runtime

The runtime is CPython 3.13.9 with NumPy 2.5.2 and jsonschema 4.25.0 plus the
four exact transitive packages in `EXP3_V2_EVALUATION_RUNTIME_LOCK_001.json`.
Installation is offline from the six hash-bound wheels. OpenAI, pandas and
openpyxl are prohibited and no credential or network access is required.

## Frozen checkout layout and future command

The future evaluation environment uses:

- harness: `/private/tmp/exp3v2-evaluation-harness-001/worktree`
- source: `/private/tmp/exp3v2-evaluation-source-001/worktree`
- data: `/private/tmp/exp3v2-evaluation-data-001/worktree`
- verbalization harness: `/private/tmp/exp3v2-evaluation-verbalization-harness-001/worktree`
- verbalizations: `/private/tmp/exp3v2-evaluation-verbalizations-001/worktree`
- inference harness: `/private/tmp/exp3v2-evaluation-inference-harness-001/worktree`
- execution authorization: `/private/tmp/exp3v2-evaluation-authorization-001/worktree`
- inference outputs: `/private/tmp/exp3v2-evaluation-inference-001/worktree`
- output: `/private/tmp/exp3v2-evaluation-run-001/output`

After a separate public harness-freeze approval, the exact one-time command is:

```bash
/private/tmp/exp3v2-evaluation-runtime-001/bin/python3 \
  /private/tmp/exp3v2-evaluation-harness-001/worktree/phase_b/exp3_v2/evaluate_exp3v2_frozen_predictions.py \
  --harness-manifest /private/tmp/exp3v2-evaluation-harness-001/worktree/phase_b/exp3_v2/EXP3_V2_EVALUATION_HARNESS_MANIFEST_001.json \
  --source-root /private/tmp/exp3v2-evaluation-source-001/worktree \
  --data-root /private/tmp/exp3v2-evaluation-data-001/worktree \
  --verbalization-harness-root /private/tmp/exp3v2-evaluation-verbalization-harness-001/worktree \
  --verbalizations-root /private/tmp/exp3v2-evaluation-verbalizations-001/worktree \
  --inference-harness-root /private/tmp/exp3v2-evaluation-inference-harness-001/worktree \
  --authorization-root /private/tmp/exp3v2-evaluation-authorization-001/worktree \
  --inference-root /private/tmp/exp3v2-evaluation-inference-001/worktree \
  --output-root /private/tmp/exp3v2-evaluation-run-001/output
```

The output root must not exist. The command creates exactly three files and
refuses overwrite. Any failure leaves the root in place for forensic review;
there is no automatic retry.

## Synthetic validation and freeze sequence

Before harness freeze, tests use synthetic identities and predictions only.
They cover canonical coverage, exact 72/24/24/120 denominators, disjoint and
complete population partitioning, label mapping, majority and parse-failure
handling, missing/extra/reordered records, paired clustering, both complete
10,000-draw distributions, seeded bootstrap determinism, output hashes, tag
enforcement, absence of secondary intervals/success criteria and exclusion of
optional analyses.

After the harness freeze and a separate explicit evaluation authorization, the
evaluator may run once. The portable verifier recomputes the three expected
bytestrings and requires exact equality. A later review-only results-freeze
candidate is governed by `EXP3_V2_EVALUATION_RESULTS_FREEZE_PROTOCOL_001.md`.
