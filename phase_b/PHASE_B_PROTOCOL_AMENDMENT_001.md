# Execution-order amendment before held-out LLM inference

Amendment ID: `001`

Base protocol freeze:
`3d86f64d43e14e7e0de520cb047ca1043bf9c1c0`

Historical tag: `phase-b-protocol-frozen`

## Reason and timing

The frozen protocol specified coverage, Conditions A/B/E, and `R = 3`, but did
not specify the temporal order of the 540 independent API requests. This
amendment adds that missing execution-order rule before any diagnostic LLM
inference.

The decision was made after deterministic V2 verbalization and before any
diagnostic LLM call:

- frozen verbalization commit:
  `32f0856040614870d3784a4811e76cee0eee77e3`;
- completed final inference at decision: `0/540`;
- observed predictions: zero;
- observed accuracy or other diagnostic metrics: zero.

The frozen verbalization manifest is
`phase_b/final_evaluation/heldout_verbalizations_manifest.json`, with SHA-256
`a5a00e6f3724ba5af50f8c4b09e82a6e61676b0a1019276733925c6d3fc7ef68`.
It already records the individual hashes of all 15 neutral-text artifacts.
Their content was neither opened nor interpreted for this amendment.

## Normative scheduling unit and iteration

A scheduling block is:

`physical_case_id × agent_id × repetition`

There are `15 × 4 × 3 = 180` scheduling blocks. Each block contains exactly
three requests, one for each condition, yielding 540 requests total.

Blocks are created by this exact explicit nested iteration:

```text
for physical_case_id in PBH-001 .. PBH-015:
    for agent_id in agent_1 .. agent_4:
        for repetition in 1 .. 3:
            create one scheduling block
```

The zero-based `block_index` increments once per block in that order. No dict,
filesystem, glob, JSON-object, or set ordering is normative or permitted as a
substitute for these explicit sequences.

## Normative condition rotation

Within each block, condition position is fixed by `block_index modulo 3`:

- remainder 0: `A, B, E`;
- remainder 1: `B, E, A`;
- remainder 2: `E, A, B`.

There is no randomization, seed, runtime choice, or content-dependent ordering.
The resulting schedule has 180 requests per condition. Globally, every
condition appears 60 times in each position. Per agent, every condition appears
15 times in each position.

## Mandatory statelessness

Every inference request is independent and stateless. Each request must contain
one complete self-contained prompt and must not use conversation history,
`previous_response_id`, conversation/thread/session state, or any output from a
previous condition or scheduling block. First/second/third denotes only
provider request time, never shared context.

The frozen OpenAI adapter already sends a complete `input`, sets `store=false`,
and does not send any chaining identifier. Regression tests enforce this for
future execution code.

## Scope of the amendment

The only additions are deterministic counterbalanced execution ordering and
mandatory statelessness. This amendment does not change the held-out data,
verbalizations, pseudolabels, local examples, insights, B/E libraries,
derangements, prompts, provider/model, reasoning effort, retry policy, `R`,
aggregation, hypotheses, metrics, or bootstrap.

The machine-readable source is
`phase_b/config/phase_b_protocol_amendment_001.json`. The generated schedule is
`phase_b/final_evaluation/inference_schedule.json`, with SHA-256
`d30cdf6a6c622c1653176b393114073b447fdde69729086f6399291d776c0c9b`.
