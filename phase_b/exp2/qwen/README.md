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
- `temperature=0`, `seed=20260829`, `max_tokens=512`
- conditions A/B/E, R=3, stateless single-message calls
- unchanged 2-of-3 aggregation and offline evaluator

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
