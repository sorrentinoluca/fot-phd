# C06 — proposed full test (not executed)

## Scope and authorization

Run B_LOCAL_FIRST_V1 on the complete frozen EXP3_V2 evaluation set: 120
agent-case groups, three stateless repetitions each, for 360 planned calls.
This document is a plan only; execution requires explicit approval.

All screening invariants remain unchanged: frozen neutral verbalizations,
examples, peer insights and order, mapping, schema, evaluator, aggregation,
`gpt-5.6-terra`, reasoning effort `medium`, 512 maximum output tokens, two
structural retries, no supplied temperature or seed, and `store=false`.

## Proposed gates

| Stratum | Gate |
|---|---:|
| Local-seen | ≥23/24 |
| Local-unseen | ≥67/72, allowing at most one loss from frozen B's 68/72 |
| Normal | 24/24 |
| Parse failures | No increase from the frozen-B baseline of zero |

Report all strata separately, together with overall accuracy, abstentions,
parse failures, three-repetition stability, insight declarations, calls,
provider attempts, token use, and cost.

## Budget estimate

- Planned calls: 360, excluding any structural retries.
- Conservative token projection from frozen-B usage plus the 74-token
  intervention: about 858k input and 58k output tokens.
- Conservative uncached list-price ceiling for that projection: about USD
  2.42. Prompt caching may reduce the actual amount; retries may increase it.

## Stronger follow-up

A later confirmatory experiment should randomize and interleave paired frozen-B
and B_LOCAL_FIRST_V1 calls concurrently over the same cases and repetitions.
That design requires 720 planned calls and reduces provider-time confounding.
It must be separately frozen and approved.
