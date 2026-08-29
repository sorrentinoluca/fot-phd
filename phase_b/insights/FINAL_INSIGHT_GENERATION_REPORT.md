# Phase B final local insight generation — structural report

Status: **COMPLETE — content not evaluated**

- Generation completed: 4/4
- Final insight count: 8
- Count per source agent: 2 each
- First structurally valid output wins: PASS
- Local schema validation: PASS
- Leakage audit: PASS (0 findings)
- Held-out accessed: false
- Definitive diagnosis or performance metric calculated: false

## Attempts

| Agent | Attempts | Structural retries |
|---|---:|---:|
| agent_1 | 1 | 0 |
| agent_2 | 1 | 0 |
| agent_3 | 1 | 0 |
| agent_4 | 1 | 0 |

## Deterministic B/E libraries

| Agent | B count | E count | Zero fixed point | Strong normalized invariance | Character equivalence |
|---|---:|---:|---|---|---|
| agent_1 | 6 | 6 | PASS | PASS | PASS |
| agent_2 | 6 | 6 | PASS | PASS | PASS |
| agent_3 | 6 | 6 | PASS | PASS | PASS |
| agent_4 | 6 | 6 | PASS | PASS | PASS |

Provenance and required hashes are complete. Raw provider responses and
every structural attempt are retained in `generation_runs.json`. This
report intentionally contains no observed pattern, insight text, predicted
label, qualitative assessment, or diagnostic interpretation.

Hash groups recorded: 11.

## Verification

- Complete Phase B suite: PASS (44/44 tests)
- Phase A frozen hashes: PASS
- Held-out guard: PASS
- Recorded SHA-256 verification: PASS (27/27 checks)
- Secret scan: PASS (0 findings)
- Sensitive credential/header keys in stored provider responses: 0
- Blockers: none
