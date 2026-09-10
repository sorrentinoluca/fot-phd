# C06 — B_LOCAL_FIRST_V1 screening decision

> Post-hoc diagnostic analysis on the frozen EXP3_V2 sample; not an independent replication.

## Decision

**PASS**. C06 status: **Mitigata — correzione preliminare promettente**.
This status is not “Risolta”: a separately approved full test is still required.

| Gate component | Required | Observed | Result |
|---|---:|---:|---:|
| Original frozen-B errors recovered | ≥4/5 | 4/5 | PASS |
| New errors among 19 frozen-B correct cases | 0 | 0 | PASS |
| Local-seen aggregate accuracy | ≥23/24 | 23/24 (95.8%) | PASS |
| Final parse failures | 0 | 0 | PASS |
| Forbidden information in consumer prompts | 0 | 0 | PASS |

There were zero aggregate abstentions. Twenty-three of 24 agent-case groups had
three-of-three repetition agreement. All 72 provider calls returned
`gpt-5.6-terra` under reasoning effort `medium`, SDK `3.6.0`, strict Structured
Outputs, no supplied temperature or seed, `store=false`, and stateless calls.

## Exact intervention

```text
DECISION POLICY
First compare the case with the local labeled examples. Prefer a local match supported by specific variables and temporal behavior; use peer observations mainly when the local examples do not provide a good match. Do not choose a peer-supported label from global counts or generic persistence alone. If local and peer evidence are both plausible and neither is clearly stronger, abstain.
```

The frozen-B reconstruction and variant differ only by this insertion. See
`../prompts/B_LOCAL_FIRST_V1.diff`.

## Five original errors

| Agent | Case | Frozen B | Variant repetitions | Aggregate | Declared peer insights | Recovered |
|---|---|---|---|---|---|---:|
| agent_2 | EXP3V2-F8-003 | CLS-Z3ISU | CLS-OJNSG / CLS-OJNSG / CLS-OJNSG | CLS-OJNSG | none | yes |
| agent_4 | EXP3V2-F13-002 | CLS-OJNSG | CLS-OJNSG / CLS-Z3ISU / CLS-OJNSG | CLS-OJNSG | INS-003 and INS-004 in the two wrong repetitions | no |
| agent_4 | EXP3V2-F13-003 | CLS-OJNSG | CLS-Z3ISU / CLS-Z3ISU / CLS-Z3ISU | CLS-Z3ISU | none | yes |
| agent_4 | EXP3V2-F13-004 | CLS-OJNSG | CLS-Z3ISU / CLS-Z3ISU / CLS-Z3ISU | CLS-Z3ISU | none | yes |
| agent_4 | EXP3V2-F13-005 | CLS-OJNSG | CLS-Z3ISU / CLS-Z3ISU / CLS-Z3ISU | CLS-Z3ISU | none | yes |

No new errors occurred among the 19 cases that frozen B classified correctly.
The complete 24-row table is in `SCREENING_REPORT.md` and
`screening_table.csv`.

## Interpretation

The local-first instruction removed most of the observed peer-interference
failure without a detected local-seen regression. The residual F13-002 error is
mechanistically consistent with incomplete mitigation: its two wrong
repetitions explicitly used INS-003 and INS-004, while the correct repetition
used no peer insight. Across all 72 repetitions, only those two wrong outputs
declared peer-insight use. This is promising diagnostic evidence, not an
independent causal replication.

## Usage and estimated list-price cost

- Completed calls/provider attempts: 72/72; structural retries: 0.
- Input tokens: 173,130, including 115,276 cached tokens.
- Output tokens: 14,217, including 5,486 reasoning tokens.
- Total tokens: 187,347.
- Estimated list-price cost: approximately USD 0.31, using USD 2.00/M
  uncached input, USD 0.20/M cached input, and USD 12.00/M output. Taxes,
  negotiated pricing, and account-specific adjustments are excluded.

One earlier request was rejected before inference with
`credit_balance_exhausted`; its intent is preserved under
`infrastructure_failures/` and is excluded from the 72 completed calls and
token totals.

## Recommendation

Proceed to the frozen 120-agent-case full-test plan only after explicit
approval. Do not create another prompt variant. Do not characterize C06 as
resolved unless the full test also passes its gates.
