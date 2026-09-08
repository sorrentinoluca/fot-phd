# EXP2 Qwen consumer lane

This directory isolates the Qwen consumer implementation from every frozen
Experiment 1 artifact. It reads the original held-out verbalizations, prompts,
local examples, peer insights, A/B/E derangements, schedule, aggregation rule,
and evaluator code in place and verifies their hashes before use.

Execution contract:

- OpenAI-compatible base URL: `http://127.0.0.1:8000/v1`
- model alias: `fot-exp2-consumer`
- expected weights: `Qwen/Qwen3.8-27B-FP8` at revision
  `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`
- `temperature=0`, `seed=20260829`, `max_tokens=1536`
- conditions A/B/E, R=3, stateless single-message calls
- unchanged 2-of-3 aggregation and offline evaluator

`max_tokens=1536` is a pre-freeze revision of the inference protocol following
the capability audit: the previous value of 512 could be exhausted by Qwen
reasoning before any JSON content was emitted. The mandated first revision at
1024 still produced a first-attempt length truncation for the synthetic B and E
fixtures, as did the next conservative 256-token step at 1280. The following
256-token step is therefore used uniformly for A, B, and E. Qwen `/tokenize`
measured a maximum frozen input of 2340 tokens, so the revised bound is
`2340 + 1536 = 3876 <= 4096` (220 tokens of context margin).

The local vLLM 0.28.0 OpenAPI advertises both `reasoning_effort` and the
separate `thinking_token_budget` request field, and the server is configured
with the Qwen3 reasoning parser required by that control. Because Qwen filled
each tested total budget through 1536 on the first B/E attempt, this revision
uses the documented `thinking_token_budget=1024` uniformly for A, B, and E,
leaving 512 completion tokens for the schema-constrained content. The client
leaves `reasoning_effort` unset and sends no undocumented control.

Run offline tests:

```bash
python -m unittest discover -s phase_b/exp2/qwen/tests -v
```

Run the capability-only probe:

```bash
python -m phase_b.exp2.qwen.capability_probe
```

The probe uses a synthetic case and computes no diagnosis metric. The complete
experiment has a separate acknowledgement and must not be run during probe or
implementation work:

```bash
python -m phase_b.exp2.qwen.run_frozen_inference --execute-full-run
```

Evaluation is intentionally impossible until the 540 repetition records and
180 aggregates have been completed and hash-frozen.
