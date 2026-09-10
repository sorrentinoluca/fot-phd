# EXP2 Qwen capped-at-3072 diagnostic follow-up

This is a post-hoc diagnostic analysis of five condition-B, repetition-1 agent-case observations selected because they were the complete set with `cap_reached=true` at reasoning budget 3072. It is not a new estimate of overall accuracy at budget 4096.

## Protocol and integrity

- Source cap-set verification: `PASS` (exactly 5 declared pairs).
- Frozen-artifact integrity: `PASS` (38 files checked).
- Inference: condition B, R=1, temperature=0.0, seed=20260829, stateless single-message requests, reasoning budget=4096, max_tokens=4608.
- Server: `Qwen/Qwen3.8-27B-FP8` revision `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`, vLLM `0.28.0`, reasoning parser `qwen3`, max_model_len=7168, physical GPU 0.
- Context fit: `PASS`; maximum request prompt=2389 tokens and maximum prompt+max_tokens=6997.

## Per-case trajectories

Each cell is `prediction (reasoning tokens; cap status)`. Correct predictions are marked ✓ and errors ✗.

| Agent | Case | Truth | 1024 | 1536 | 2048 | 3072 | 4096 | Diagnostic reading |
|---|---|---|---|---|---|---|---|---|
| agent_2 | PBH-007 | CLS-OJNSG | CLS-Z3ISU (1023; cap; ✗) | CLS-Z3ISU (1535; cap; ✗) | CLS-OJNSG (2047; cap; ✓) | CLS-OJNSG (3071; cap; ✓) | CLS-OJNSG (4095; cap; ✓) | correct while still capped; additional evidence that reaching the cap does not imply error |
| agent_4 | PBH-007 | CLS-OJNSG | CLS-OJNSG (1023; cap; ✓) | CLS-OJNSG (1535; cap; ✓) | CLS-OJNSG (2047; cap; ✓) | CLS-OJNSG (3071; cap; ✓) | CLS-OJNSG (3196; below; ✓) | correct and terminated below the new cap |
| agent_3 | PBH-009 | CLS-OJNSG | CLS-ZOGAA (1023; cap; ✗) | CLS-ZOGAA (1535; cap; ✗) | CLS-ZOGAA (2047; cap; ✗) | CLS-ZOGAA (3071; cap; ✗) | CLS-OJNSG (4095; cap; ✓) | correct while still capped; additional evidence that reaching the cap does not imply error |
| agent_4 | PBH-014 | CLS-Z3ISU | CLS-OJNSG (1023; cap; ✗) | CLS-OJNSG (1535; cap; ✗) | CLS-OJNSG (2047; cap; ✗) | CLS-OJNSG (3071; cap; ✗) | CLS-OJNSG (3187; below; ✗) | 3072 error persists below the new cap; interference or negative transfer is more plausible, without causal attribution |
| agent_1 | PBH-015 | CLS-Z3ISU | CLS-Z3ISU (1023; cap; ✓) | CLS-Z3ISU (1535; cap; ✓) | CLS-Z3ISU (2047; cap; ✓) | CLS-Z3ISU (3071; cap; ✓) | CLS-Z3ISU (4095; cap; ✓) | correct while still capped; additional evidence that reaching the cap does not imply error |

## Diagnostic summary

- Terminated below the 4096 reasoning cap: 2/5; still capped: 3/5.
- Errors present at 3072 and corrected at 4096: 1.
- Errors present at 3072 and still incorrect at 4096: 1.
- Incorrect and still capped at 4096, hence mechanistically inconclusive: 0.
- Correct while still capped at 4096: 3; such a case is further evidence that reaching a cap does not automatically imply error.
- Regressions relative to 3072: 0; any regression shows that greater reasoning budget is not monotonically beneficial.

An error corrected and terminated below the new limit is compatible with reasoning truncation. An error that persists but terminates below the limit makes interference or negative transfer more plausible, without establishing causality. An error still at the new limit remains inconclusive.

## Methodological limits

The subset was selected after observing cap status at 3072, so selection is outcome-dependent and cannot support an overall 4096-budget accuracy claim. R=1 with deterministic settings checks this fixed execution path but does not estimate stochastic variability. The comparison is diagnostic and observational: changes across budgets cannot by themselves identify a causal mechanism.
