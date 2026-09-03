# Experiment 3 V2 — Revision 003 sentinel failure

Revision 003 was frozen at tag `exp3-v2-harness-frozen-003`, commit
`bce8f0e2f24db7033b7ddbecc38e1bfaa74c85a6`. Its sole sentinel execution used
`EXP3V2-SENTINEL-001` and consumed non-scientific seed `987654321` with one
`rng` call and one `sim` call. It was not retried.

The engine produced a technically valid `3001 × 54` throwaway workbook of
1,704,651 bytes with SHA-256
`a1980855174e9db82416f576e84aa720eddd758b5686b9ecfc376aeedfa282a9`.
The workbook is not committed, and its cell values were not inspected while
preparing Revision 004.

End-to-end verification failed. The original wrapper selected ambient
`python3`, which could not import `jsonschema`. Subsequent forensic verification
with `/opt/anaconda3/bin/python3` (Python 3.13.9, jsonschema 4.25.0, openpyxl
3.1.5) also failed: the Revision 003 CSV serialized the exact `1/60` sampling
interval as `0.016667`, outside the verifier tolerance. The failed CSV is
preserved unchanged.

The available failure JSON, attempt log and sentinel manifest CSV are archived
byte-identically as Revision 003 evidence. No scientific seed was consumed and
no real EXP3_V2 workbook was produced.
