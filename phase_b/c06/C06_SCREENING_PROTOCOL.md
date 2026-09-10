# C06 — B_LOCAL_FIRST_V1 screening protocol

## Scope

This is a post-hoc diagnostic analysis of the frozen EXP3_V2 sample. It is not
a new independent replication. The intervention is the addition of one general
local-first decision instruction to the frozen condition-B prompt.

The scheduling layer selects the 24 agent-case observations corresponding to
each agent's own locally represented fault. Neither this selection fact nor any
offline answer, real fault identifier, target case list, or evaluator mapping is
included in a consumer prompt.

## Invariants

- Consumer: `gpt-5.6-terra`, reasoning effort `medium`.
- Frozen OpenAI Python SDK: `3.6.0`.
- Isolated runtime: `/Users/luker/fot-c06-env/bin/python`.
- Three stateless repetitions per agent-case; 72 planned calls.
- Strict frozen output schema and maximum 512 output tokens.
- Frozen data, neutral verbalizations, local examples, peer insights, peer
  insight order, pseudolabels, and two-of-three aggregation.
- No temperature or seed is sent; `store=false`; no previous response ID.
- Structural retry policy remains two retries after the first attempt.

The baseline prompt and every imported prompt-side dependency are bound to the
EXP3_V2 frozen tags and hashes. Neutral texts are read directly from the frozen
verbalization payload commit and verified against its output manifest.

## Intervention

`B_LOCAL_FIRST_V1` differs from frozen B only by the decision-policy block in
`prompts/B_LOCAL_FIRST_V1.diff`. It contains no experiment case identifier,
real fault identity, evaluator label mapping, answer, or named problematic
insight.

## Outcomes and gate

Report aggregate accuracy, recovery of the five original errors, new errors in
the 19 previously correct observations, abstentions, parse failures,
three-repetition agreement, and declared insight use.

PASS requires all of:

- at least four of five original errors recovered;
- no new error in the 19 previously correct observations;
- at least 23/24 aggregate predictions correct;
- zero parse failures;
- all prompt-leakage and frozen-input checks passing.

If the gate fails, no alternative prompt is attempted automatically. If it
passes, only a plan is prepared for the 120-agent-case full test; that test
requires separate approval.

## Full-test plan, not authorized by this protocol

The future full test contains 120 agent-case aggregates and 360 new calls. It
reports local-seen, local-unseen, Normal, overall, abstentions, parse failures,
and repetition stability separately. Proposed gates are local-seen at least
23/24, unseen at least 67/72, Normal 24/24, and no increase in parse failures.
A stronger follow-up should run frozen B and B_LOCAL_FIRST_V1 concurrently in
a randomized paired schedule to reduce provider-time confounding.
