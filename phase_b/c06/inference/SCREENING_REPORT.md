# C06 B_LOCAL_FIRST_V1 screening

> Post-hoc diagnostic analysis; this is not an independent replication.

Gate: **PASS**

- Accuracy: 23/24 (95.8%)
- Original errors recovered: 4/5
- New errors: 0/19
- Aggregate abstentions: 0
- Parse failures: 0
- Three-of-three agreement: 23/24

| Agent | Case | Expected | Frozen B | Variant | Repetitions | Correct | Insights |
|---|---|---|---|---|---|---:|---|
| agent_1 | EXP3V2-F1-001 | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA/CLS-ZOGAA/CLS-ZOGAA | yes | — |
| agent_1 | EXP3V2-F1-002 | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA/CLS-ZOGAA/CLS-ZOGAA | yes | — |
| agent_1 | EXP3V2-F1-003 | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA/CLS-ZOGAA/CLS-ZOGAA | yes | — |
| agent_1 | EXP3V2-F1-004 | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA/CLS-ZOGAA/CLS-ZOGAA | yes | — |
| agent_1 | EXP3V2-F1-005 | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA/CLS-ZOGAA/CLS-ZOGAA | yes | — |
| agent_1 | EXP3V2-F1-006 | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA | CLS-ZOGAA/CLS-ZOGAA/CLS-ZOGAA | yes | — |
| agent_2 | EXP3V2-F8-001 | CLS-OJNSG | CLS-OJNSG | CLS-OJNSG | CLS-OJNSG/CLS-OJNSG/CLS-OJNSG | yes | — |
| agent_2 | EXP3V2-F8-002 | CLS-OJNSG | CLS-OJNSG | CLS-OJNSG | CLS-OJNSG/CLS-OJNSG/CLS-OJNSG | yes | — |
| agent_2 | EXP3V2-F8-003 | CLS-OJNSG | CLS-Z3ISU | CLS-OJNSG | CLS-OJNSG/CLS-OJNSG/CLS-OJNSG | yes | — |
| agent_2 | EXP3V2-F8-004 | CLS-OJNSG | CLS-OJNSG | CLS-OJNSG | CLS-OJNSG/CLS-OJNSG/CLS-OJNSG | yes | — |
| agent_2 | EXP3V2-F8-005 | CLS-OJNSG | CLS-OJNSG | CLS-OJNSG | CLS-OJNSG/CLS-OJNSG/CLS-OJNSG | yes | — |
| agent_2 | EXP3V2-F8-006 | CLS-OJNSG | CLS-OJNSG | CLS-OJNSG | CLS-OJNSG/CLS-OJNSG/CLS-OJNSG | yes | — |
| agent_3 | EXP3V2-F10-001 | CLS-R463B | CLS-R463B | CLS-R463B | CLS-R463B/CLS-R463B/CLS-R463B | yes | — |
| agent_3 | EXP3V2-F10-002 | CLS-R463B | CLS-R463B | CLS-R463B | CLS-R463B/CLS-R463B/CLS-R463B | yes | — |
| agent_3 | EXP3V2-F10-003 | CLS-R463B | CLS-R463B | CLS-R463B | CLS-R463B/CLS-R463B/CLS-R463B | yes | — |
| agent_3 | EXP3V2-F10-004 | CLS-R463B | CLS-R463B | CLS-R463B | CLS-R463B/CLS-R463B/CLS-R463B | yes | — |
| agent_3 | EXP3V2-F10-005 | CLS-R463B | CLS-R463B | CLS-R463B | CLS-R463B/CLS-R463B/CLS-R463B | yes | — |
| agent_3 | EXP3V2-F10-006 | CLS-R463B | CLS-R463B | CLS-R463B | CLS-R463B/CLS-R463B/CLS-R463B | yes | — |
| agent_4 | EXP3V2-F13-001 | CLS-Z3ISU | CLS-Z3ISU | CLS-Z3ISU | CLS-Z3ISU/CLS-Z3ISU/CLS-Z3ISU | yes | — |
| agent_4 | EXP3V2-F13-002 | CLS-Z3ISU | CLS-OJNSG | CLS-OJNSG | CLS-OJNSG/CLS-Z3ISU/CLS-OJNSG | no | INS-003,INS-004 |
| agent_4 | EXP3V2-F13-003 | CLS-Z3ISU | CLS-OJNSG | CLS-Z3ISU | CLS-Z3ISU/CLS-Z3ISU/CLS-Z3ISU | yes | — |
| agent_4 | EXP3V2-F13-004 | CLS-Z3ISU | CLS-OJNSG | CLS-Z3ISU | CLS-Z3ISU/CLS-Z3ISU/CLS-Z3ISU | yes | — |
| agent_4 | EXP3V2-F13-005 | CLS-Z3ISU | CLS-OJNSG | CLS-Z3ISU | CLS-Z3ISU/CLS-Z3ISU/CLS-Z3ISU | yes | — |
| agent_4 | EXP3V2-F13-006 | CLS-Z3ISU | CLS-Z3ISU | CLS-Z3ISU | CLS-Z3ISU/CLS-Z3ISU/CLS-Z3ISU | yes | — |

## Five original frozen-B errors

| Agent | Case | Frozen B | Variant reps | Variant aggregate | Declared insight IDs | Recovered |
|---|---|---|---|---|---|---:|
| agent_2 | EXP3V2-F8-003 | CLS-Z3ISU | CLS-OJNSG/CLS-OJNSG/CLS-OJNSG | CLS-OJNSG | — | yes |
| agent_4 | EXP3V2-F13-002 | CLS-OJNSG | CLS-OJNSG/CLS-Z3ISU/CLS-OJNSG | CLS-OJNSG | INS-003,INS-004 | no |
| agent_4 | EXP3V2-F13-003 | CLS-OJNSG | CLS-Z3ISU/CLS-Z3ISU/CLS-Z3ISU | CLS-Z3ISU | — | yes |
| agent_4 | EXP3V2-F13-004 | CLS-OJNSG | CLS-Z3ISU/CLS-Z3ISU/CLS-Z3ISU | CLS-Z3ISU | — | yes |
| agent_4 | EXP3V2-F13-005 | CLS-OJNSG | CLS-Z3ISU/CLS-Z3ISU/CLS-Z3ISU | CLS-Z3ISU | — | yes |

## New errors among the 19 frozen-B correct cases

None.
