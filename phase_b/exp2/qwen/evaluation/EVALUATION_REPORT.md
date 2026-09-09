# Phase B EXP2 Qwen final offline evaluation

The primary analysis uses only the frozen R=3 aggregate outcomes. No aggregation was recomputed and abstentions count as incorrect.

## Primary: locally unseen faults

| Condition | Correct / n | Accuracy | Abstentions |
|---|---:|---:|---:|
| A | 0 / 36 | 0.00% | 0 |
| B | 34 / 36 | 94.44% | 0 |
| E | 1 / 36 | 2.78% | 0 |

- Delta_unseen (B−A): 0.944444444444
- Delta_E (E−A): 0.0277777777778
- Delta_specificity (B−E): 0.916666666667

### Per-agent primary

| Agent | n | A | B | E | Delta B−A |
|---|---:|---:|---:|---:|---:|
| agent_1 | 9 | 0.00% | 100.00% | 0.00% | 1 |
| agent_2 | 9 | 0.00% | 100.00% | 0.00% | 1 |
| agent_3 | 9 | 0.00% | 77.78% | 11.11% | 0.777777777778 |
| agent_4 | 9 | 0.00% | 100.00% | 0.00% | 1 |

### Paired B versus A transfers

- Helped: 34
- Harmed: 0
- Unchanged: 2 (correct 0, incorrect 2)

### Frozen support criteria

- C1 Delta_unseen > 0: PASS
- C2 positive delta in at least 3/4 agents: PASS
- C3 helped > harmed: PASS
- C4 Delta_unseen > Delta_E: PASS
- Primary support criteria satisfied: 4/4

### Frozen cluster bootstrap

- Draws: 10000; seed: 20260829
- Delta_unseen 95% CI: [0.916666666667, 1]
- Delta_specificity 95% CI: [0.833333333333, 1]

## Secondary outcomes

### Local fault seen

| Condition | Correct / n | Accuracy | Abstention rate |
|---|---:|---:|---:|
| A | 12 / 12 | 100.00% | 0.00% |
| B | 9 / 12 | 75.00% | 0.00% |
| E | 12 / 12 | 100.00% | 0.00% |

### Normal

| Condition | Correct / n | Accuracy | Abstention rate |
|---|---:|---:|---:|
| A | 12 / 12 | 100.00% | 0.00% |
| B | 12 / 12 | 100.00% | 0.00% |
| E | 12 / 12 | 100.00% | 0.00% |

### Overall

| Condition | Correct / n | Accuracy | Abstention rate |
|---|---:|---:|---:|
| A | 24 / 60 | 40.00% | 0.00% |
| B | 55 / 60 | 91.67% | 0.00% |
| E | 25 / 60 | 41.67% | 0.00% |

H2 (B local-fault-seen accuracy ≥ A, epsilon=0): **FAIL**

Per-pseudolabel recall and complete confusion matrices are preserved in `confusion_matrices.json`.

## Integrity and reproducibility

- Ground-truth join: 15/15 physical cases, unique.
- Primary denominator: 36 aggregate agent-case observations per condition.
- Independent physical fault clusters: 12.
- Local-fault-seen denominator: 12 per condition.
- Normal denominator: 12 per condition.
- Overall denominator: 60 per condition.
- All internal consistency checks: PASS.
- EXP2 Qwen predictions freeze: `phase-b-exp2-qwen-predictions-frozen-001` at `a4f264c210873536c989ebd99aa2c6cf9857c85c`.
