# FAR verification — Normal threshold

Threshold: `13.623626738268857`; freeze SHA-256: `ff5c27002a2548003e4bc5f54805cda3754fb19b9cb2559222996b9c7f7e14a9`.

Primary: **11/150 = 0.073333**, Clopper–Pearson 95% [0.037175, 0.127424].
Secondary: **108/1500 = 0.072000**, bootstrap SE 0.007513, 95% percentile [0.057333, 0.087333] (10,000 replicates, seed 20260913, unit run).

| Position | Exceedances | N | FAR |
|---:|---:|---:|---:|
| 1 | 14 | 150 | 0.093333 |
| 2 | 10 | 150 | 0.066667 |
| 3 | 12 | 150 | 0.080000 |
| 4 | 6 | 150 | 0.040000 |
| 5 | 14 | 150 | 0.093333 |
| 6 | 8 | 150 | 0.053333 |
| 7 | 11 | 150 | 0.073333 |
| 8 | 13 | 150 | 0.086667 |
| 9 | 10 | 150 | 0.066667 |
| 10 | 10 | 150 | 0.066667 |

Numeric validation: PASS; all 150 files matched the freeze seal; no threshold changes were made.
