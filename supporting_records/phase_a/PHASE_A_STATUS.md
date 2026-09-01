# Phase A status

## Status

**Phase A completed.** The numerical time-series to structured evidence to
neutral-text layer has completed development, pre-validation freeze,
out-of-development validation, and held-out test evaluation.

The independent final review verdict is **GO WITH CAVEATS**. The caveats were
limited to reproducibility and documentation. They do not authorize changes to
the V2 feature layer, thresholds, renderer, evaluator, or configuration.

## Milestones

| Milestone | Commit | Tag | Status |
|---|---|---|---|
| Development methodology | before freeze; artifacts later preserved in `b113046` | — | completed |
| Pre-validation freeze | `3fd960a192bafacbaabce9471e3c3614d6b2d2db` | `verbalizer-v2-pre-validation` | completed |
| Out-of-development validation | `1d9c1617b56c19d2bc71dfef7b7902df0670b537` | `verbalizer-v2-validation-complete` | completed |
| Held-out final test | `0a45817fd783513e23d58a35c55489404c95feec` | `verbalizer-v2-test-complete` | completed |
| Phase A scientific completion | `0a45817fd783513e23d58a35c55489404c95feec` | `phase-a-verbalizer-v2-complete` | completed |
| Reproducibility caveat closure | this separate documentation/reproducibility commit | `phase-a-reproducibility-complete` | completed with this record |

Dataset provenance remains pinned to upstream commit
`309b944f35ac440ff0c70616947ffe723c766e14`; raw workbooks are not duplicated in
this repository.

## Review caveats closed

This reproducibility closure adds, without modifying frozen files:

1. `code/calibrate_thresholds_v2.py`, an executable reproduction of the exact
   Normal N1–N5 leave-one-block-out threshold procedure.
2. `code/test_calibrate_thresholds_v2.py`, with committed-maxima and full
   workbook regression checks.
3. A recorded calibration verification in `reproducibility/`, demonstrating
   zero numerical error against both frozen threshold references.
4. `requirements.txt`, pinning the actual Phase A runtime dependencies, and a
   documented CPython `3.13.9` reference runtime.
5. `code/verify_injection_time_v2.py` and
   `INJECTION_TIME_VERIFICATION.md`, separating source routing evidence from a
   development-only empirical consistency check.
6. A repository-level `README.md` that separates calibration/development,
   validation, and held-out test reproduction.

No new feature, threshold, diagnostic rule, or methodology is introduced.

## Immutable config status field

`code/verbalizer_config_v2.json` intentionally still contains:

```json
"status": "FROZEN_PENDING_VALIDATION"
```

This field records the state at the instant of the pre-validation freeze. It is
part of the byte-identical frozen artifact and is intentionally not updated to
reflect later project milestones. Current lifecycle status belongs in this
document, not in the historical frozen config.

## Main artifacts and hashes

| Artifact | SHA-256 |
|---|---|
| `VERBALIZER_V2_FREEZE.md` | `e03e99d2430205635fc637c2b85299c1a55184bfb6de7895942c71e5232686e2` |
| `code/tep_analysis_v2/threshold_calibration.json` | `684ce2a68761d81bf839590292d8e7225e27ab079f4172f70b3dbc38f9649c33` |
| `tep_validation_v2/validation_report.md` | `4f401407b5882138c9075d5de92ce85ad394ccc5894838d37f3aa6b21e114d1e` |
| `tep_test_v2/test_report.md` | `a92b75ab4ffc6a74edf376ba786897c0989429f9b0357740f733075af0d2a30b` |
| `reproducibility/threshold_calibration_verification.json` | `e0c285f6a936cbf2d60a2e6b43f70ee8a0e79abe80709e1b9d4a069fb9633504` |
| `INJECTION_TIME_VERIFICATION.md` | `0e5d50114d6f8151f85241983f74ecc38b568c58dd29c45a7fef2ceee1c10391` |

Frozen implementation hashes remain those recorded in
`VERBALIZER_V2_FREEZE.md`. Phase B FoT has not started.
