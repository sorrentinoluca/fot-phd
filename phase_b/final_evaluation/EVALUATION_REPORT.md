# Phase B final offline evaluation

The primary analysis uses only the frozen R=3 aggregate outcomes. No aggregation was recomputed and abstentions count as incorrect.

## Primary: locally unseen faults

| Condition | Correct / n | Accuracy | Abstentions |
|---|---:|---:|---:|
| A | 0 / 36 | 0.00% | 14 |
| B | 31 / 36 | 86.11% | 0 |
| E | 3 / 36 | 8.33% | 0 |

- Delta_unseen (B−A): 0.861111111111
- Delta_E (E−A): 0.0833333333333
- Delta_specificity (B−E): 0.777777777778

### Per-agent primary

| Agent | n | A | B | E | Delta B−A |
|---|---:|---:|---:|---:|---:|
| agent_1 | 9 | 0.00% | 100.00% | 0.00% | 1 |
| agent_2 | 9 | 0.00% | 100.00% | 0.00% | 1 |
| agent_3 | 9 | 0.00% | 66.67% | 22.22% | 0.666666666667 |
| agent_4 | 9 | 0.00% | 77.78% | 11.11% | 0.777777777778 |

### Paired B versus A transfers

- Helped: 31
- Harmed: 0
- Unchanged: 5 (correct 0, incorrect 5)

### Frozen support criteria

- C1 Delta_unseen > 0: PASS
- C2 positive delta in at least 3/4 agents: PASS
- C3 helped > harmed: PASS
- C4 Delta_unseen > Delta_E: PASS
- Primary support criteria satisfied: 4/4

### Frozen cluster bootstrap

- Draws: 10000; seed: 20260829
- Delta_unseen 95% CI: [0.833333333333, 0.916666666667]
- Delta_specificity 95% CI: [0.722222222222, 0.833333333333]

## Secondary outcomes

### Local fault seen

| Condition | Correct / n | Accuracy | Abstention rate |
|---|---:|---:|---:|
| A | 12 / 12 | 100.00% | 0.00% |
| B | 12 / 12 | 100.00% | 0.00% |
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
| A | 24 / 60 | 40.00% | 23.33% |
| B | 55 / 60 | 91.67% | 0.00% |
| E | 27 / 60 | 45.00% | 0.00% |

H2 (B local-fault-seen accuracy ≥ A, epsilon=0): **PASS**

Per-pseudolabel recall and complete confusion matrices are preserved in `confusion_matrices.json`.

## Integrity and reproducibility

- Ground-truth join: 15/15 physical cases, unique.
- Primary denominator: 36 aggregate agent-case observations per condition.
- Independent physical fault clusters: 12.
- Local-fault-seen denominator: 12 per condition.
- Normal denominator: 12 per condition.
- Overall denominator: 60 per condition.
- All internal consistency checks: PASS.
- Inference freeze: `phase-b-inference-frozen` at `11c34358e28e875cd5c7249061ac2b89ffcd42f4`.
