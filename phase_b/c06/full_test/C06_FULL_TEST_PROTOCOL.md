# C06 — B_LOCAL_FIRST_V1 full test protocol

## Scope

This is a post-hoc diagnostic analysis of the frozen EXP3_V2 evaluation set.
It is not a new independent replication. The intervention is the addition of
one general local-first decision instruction to the frozen condition-B prompt,
identical to the one validated in the 24-case screening (gate PASS, 23/24).

This full test extends the screening to all 120 agent-case groups across
three strata: local-seen (24), local-unseen (72), and Normal (24). Each
group receives three stateless repetitions, for 360 planned calls.

## Invariants

All screening invariants remain unchanged:

- Consumer: `gpt-5.6-terra`, reasoning effort `medium`.
- Frozen OpenAI Python SDK: `3.6.0`.
- Isolated runtime: `/Users/luker/fot-c06-env/bin/python`.
- Three stateless repetitions per agent-case; 360 planned calls.
- Strict frozen output schema and maximum 512 output tokens.
- Frozen data, neutral verbalizations, local examples, peer insights, peer
  insight order, pseudolabels, and two-of-three aggregation.
- No temperature or seed is sent; `store=false`; no previous response ID.
- Structural retry policy remains two retries after the first attempt.

The baseline prompt and every imported prompt-side dependency are bound to
the EXP3_V2 frozen tags and hashes.

## Intervention

`B_LOCAL_FIRST_V1` differs from frozen B only by the decision-policy block
defined in the screening protocol. It contains no experiment case identifier,
real fault identity, evaluator label mapping, answer, or named problematic
insight.

## Strata

| Stratum | Definition | Cases |
|---|---|---:|
| local-seen | Agent diagnoses its own locally represented fault type | 24 |
| local-unseen | Agent diagnoses a fault type known only through peer insights | 72 |
| normal | Agent diagnoses a Normal (no-fault) case | 24 |

## Gates

All four gates must pass:

| Stratum | Gate | Rationale |
|---|---|---|
| Local-seen | ≥ 23/24 | Screening showed 23/24; full test must confirm | 
| Local-unseen | ≥ 67/72 | At most one loss from frozen B's 68/72 |
| Normal | 24/24 | No degradation on Normal cases |
| Parse failures | 0 | No increase from frozen-B baseline |

## Report

Report all strata separately, together with overall accuracy, abstentions,
parse failures, three-repetition stability, insight declarations,
regressions (correct→wrong), improvements (wrong→correct), calls, provider
attempts, token use, and cost.

## Budget estimate

- Planned calls: 360, excluding any structural retries.
- Conservative token projection from frozen-B usage plus the 74-token
  intervention: about 858k input and 58k output tokens.
- Conservative uncached list-price ceiling: about USD 2.42.

## Authorization

This full test was authorized by the project lead as a direct follow-up to
the successful screening gate (PASS, 23/24, 4/5 errors recovered, 0 new
errors). The screening results are in `phase_b/c06/inference/`.
