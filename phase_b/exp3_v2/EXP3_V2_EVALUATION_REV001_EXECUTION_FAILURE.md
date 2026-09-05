# EXP3_V2 Evaluation Revision 001 Execution Failure Record

Status: `REVIEW_ONLY_DRAFT_FOR_PERMANENT_RECORD`

The exact invocation timestamp is `NOT_AVAILABLE` (`null` in the JSON record).

## Frozen boundary identity

- Harness revision: `001`
- Harness tag: `exp3-v2-evaluation-harness-frozen-001`
- Annotated tag object: `43163e51ebd4e592aaf3d03d7bec50c4cd0b63fb`
- Target commit: `25dc65bba805f15836f09e9613505bf483199a4f`
- Parent commit: `c62c871657c061826efda708aacd386779a16d02`
- Frozen manifest SHA-256: `d8454d13ed7299fdac690657fcacb731e8b8b6f0c0cebf2213af5adf1e7547cd`
- Frozen config SHA-256: `5d836027adb493c7c12d3fa495696960a1f208ddaa9b102a7d1d5ba551b6ffdb`
- Frozen protocol SHA-256: `8f9b7706a58b8c9caef788e2c61ef69129711bfde0b2c9029c3573c1caf785c8`
- Frozen evaluator SHA-256: `272f56d01711ce6879969aa1f5c3f662a706b63957c1652e41cfbad8c6052990`

## Technical failure

The sole authorized Revision 001 execution was performed. It failed with:

```text
FileNotFoundError: /private/tmp/exp3v2-evaluation-run-001/output
```

The frozen runner executed `output_root.mkdir(parents=False)` while the parent
`/private/tmp/exp3v2-evaluation-run-001` was absent. The failure occurred after
the in-memory evaluation and bootstrap calculation and before any output write.

## Execution counters and seed state

- Evaluator invocations: `1`
- Retries: `0`
- Verifier executions: `0`
- `numpy.random.default_rng(320031)` invocations: `1`
- Bootstrap seed used: `320031`
- API/LLM calls: `0`
- Credentials accessed: `0`

Revision 001 is exhausted and authorizes no retry. Seed `320031` is not eligible
for reuse under Revision 001. Any deterministic replay using the same seed must
be explicitly defined, reviewed and authorized in a future Revision 002; this
record provides no automatic replay authorization.

## Output and inspection state

- Output files created: `0`
- Final output root: `ABSENT`
- Results-freeze tag `exp3-v2-results-frozen-001` created: `false`
- Results frozen: `false`
- Results published: `false`
- Results inspected or reported: `0`
- Metrics inspected or reported: `0`
- Bootstrap distributions inspected or reported: `0`
- Scientific values inspected or reported: `0`
- Ground truth or predictions reported: `0`

All eight frozen checkouts were clean after the failure (`8/8`), and frozen
artifacts modified remained `0`.

## Governance consequence and next permitted step

No automatic retry, Revision 001 retry, Revision 001 seed reuse or result freeze
is authorized. The next permitted step is preparation and review of a future
Revision 002 definition and correction. No evaluator execution or replay of
seed `320031` may occur without separate explicit authorization.

## This review-only record-preparation operation

- Evaluator invocations: `0`
- Retries: `0`
- RNG invocations: `0`
- Metrics calculated: `0`
- Output files created: `0`
- Commits created: `0`
- Tags created: `0`
- Pushes: `0`
