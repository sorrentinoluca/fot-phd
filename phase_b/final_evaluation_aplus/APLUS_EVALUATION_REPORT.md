# C01 — A+ (local-only self-insight) evaluation

Four-condition comparison: A (no insights), A+ (self-insights only), B (peer insights), E (corrupted peer insights).

Abstentions count as incorrect. Primary analysis uses only frozen R=3 aggregate outcomes.

## Primary: locally unseen faults

| Condition | Correct / n | Accuracy | Abstentions |
|---|---:|---:|---:|
| A | 0 / 36 | 0.00% | 14 |
| A+ | 0 / 36 | 0.00% | 21 |
| B | 31 / 36 | 86.11% | 0 |
| E | 3 / 36 | 8.33% | 0 |

### Key deltas

- Delta A+−A (self-insight effect): 0
- Delta B−A+ (peer benefit over local): 0.861111111111
- Delta E−A+ (corrupted vs local): 0.0833333333333
- Delta B−A (total FoT effect): 0.861111111111
- Delta B−E (specificity): 0.777777777778

### Per-agent primary (unseen faults)

| Agent | n | A | A+ | B | E | Δ(A+−A) | Δ(B−A+) |
|---|---:|---:|---:|---:|---:|---:|---:|
| agent_1 | 9 | 0.00% | 0.00% | 100.00% | 0.00% | 0 | 1 |
| agent_2 | 9 | 0.00% | 0.00% | 100.00% | 0.00% | 0 | 1 |
| agent_3 | 9 | 0.00% | 0.00% | 66.67% | 22.22% | 0 | 0.666666666667 |
| agent_4 | 9 | 0.00% | 0.00% | 77.78% | 11.11% | 0 | 0.777777777778 |

### Paired transfers (unseen, n=36)

| Comparison | Helped | Harmed | Unchanged (correct/incorrect) |
|---|---:|---:|---|
| A+_vs_A_unseen | 0 | 0 | 36 (0/36) |
| B_vs_A+_unseen | 31 | 0 | 5 (0/5) |
| E_vs_A+_unseen | 3 | 0 | 33 (0/33) |
| B_vs_A_unseen | 31 | 0 | 5 (0/5) |

### Inter-repetition agreement (A+)

- Unanimous 3/3: 57 / 60
- Majority 2/3: 3 / 60
- All different: 0 / 60
- Unanimity rate: 95.00%

### Bootstrap confidence intervals

- Draws: 10000; seed: 20260829
- Delta A+−A 95% CI: [0, 0]
- Delta B−A+ 95% CI: [0.833333333333, 0.916666666667]
- Delta E−A+ 95% CI: [0.0277777777778, 0.138888888889]

## C01 interpretation criteria

- A unseen = 0%: True
- A+ unseen ≈ A (self-insights alone insufficient): expected
- B > A+ (peer insights help beyond self): PASS
- B > E (correct peers beat corrupted): PASS
- A+ ≤ B (peer benefit confirmed): PASS

> A+ provides the self-insight control. If A+ ≈ A, self-insights alone do not help on unseen faults (as expected: the agent already knows its own class). If B >> A+ >> A, both self and peer insights help. If B >> A+ ≈ A, peer insights are the sole driver of transfer.

## Secondary outcomes

### Local fault seen

| Condition | Correct / n | Accuracy | Abstention rate |
|---|---:|---:|---:|
| A | 12 / 12 | 100.00% | 0.00% |
| A+ | 12 / 12 | 100.00% | 0.00% |
| B | 12 / 12 | 100.00% | 0.00% |
| E | 12 / 12 | 100.00% | 0.00% |

### Normal

| Condition | Correct / n | Accuracy | Abstention rate |
|---|---:|---:|---:|
| A | 12 / 12 | 100.00% | 0.00% |
| A+ | 12 / 12 | 100.00% | 0.00% |
| B | 12 / 12 | 100.00% | 0.00% |
| E | 12 / 12 | 100.00% | 0.00% |

### Overall

| Condition | Correct / n | Accuracy | Abstention rate |
|---|---:|---:|---:|
| A | 24 / 60 | 40.00% | 23.33% |
| A+ | 24 / 60 | 40.00% | 35.00% |
| B | 55 / 60 | 91.67% | 0.00% |
| E | 27 / 60 | 45.00% | 0.00% |

A+ confusion matrix and per-pseudolabel recall are preserved in `aplus_confusion_matrix.json`.

## Token usage (A+ inference only)

- Input tokens: 333,192
- Output tokens: 29,695
- Total tokens: 362,887
- Structural retries: 0
- Final parse failures: 0

## Integrity and reproducibility

- Ground-truth join: 15/15 physical cases, unique.
- Primary denominator: 36 aggregate agent-case observations per condition.
- Independent physical fault clusters: 12.
- Local-fault-seen denominator: 12 per condition.
- Normal denominator: 12 per condition.
- Overall denominator: 60 per condition.
- All internal consistency checks: PASS.
- A/B/E frozen results: verified untouched.
- A+ frozen inputs: verified against APLUS_FREEZE_MANIFEST.json.
