# Experiment 3 closure

Status: `CLOSED_INCOMPLETE_ATTEMPTS_EXHAUSTED`

Experiment 3 is formally closed as an incomplete experiment. The first planned case, `EXP3-N-001`, consumed both attempts allowed by Section 9.2 of `EXP3_FRESH_RUN_PROTOCOL.md`. No alternative seed or additional recovery run is authorized under that frozen protocol.

Exactly 0 of 30 planned cases completed. No workbook was produced, no accepted scientific output exists, and no scientific signal was observed. The live ignored attempt log was hash-verified before archival and copied verbatim to `EXP3_CLOSURE_attempt_log_archive.json` as permanent version-controlled evidence. Both copies have SHA-256 `04ea7d8af227c3a7f947b4dde434e77510c163ce9c108892ffa22f491f022904`.

## Immutable provenance chain

| Boundary | Commit | Tag | Relationship |
|---|---|---|---|
| EXP3 freeze | `b02e93f92bf6fa85a4fd0a2e010bac365a3a7c89` | `exp3-heldout-frozen` | root of the verified EXP3 chain |
| hotfix 001 | `cdba0202435d1c97ea79cfff586e59534ce9baad` | `exp3-heldout-frozen-hotfix-001` | descendant of freeze |
| hotfix 002 | `28130023a34eda778c04a001a9f631404bd6b9a6` | `exp3-post-freeze-hotfix-002` | descendant of hotfix 001 |
| hotfix 003 | `0d869720e6ac4d1b396b3b9d731463324d296e26` | `exp3-post-freeze-hotfix-003` | descendant of hotfix 002 |
| hotfix 004 | `1cad481839475afaa6ad784bba25c1c45bb260ed` | `exp3-post-freeze-hotfix-004` | descendant of hotfix 003; source boundary for this closure |

Every tag above was resolved with `git rev-parse <tag>^{}` and matched the recorded commit. The ancestry is linear in the displayed order. These commits and tags, all existing EXP3 artifacts, and all Experiment 1 frozen artifacts remain immutable.

## Incident timeline

| # | Stage | Technical error | Resolution |
|---:|---|---|---|
| 1 | before simulation | `Unrecognized field name "attempt"` from an untyped empty structure | hotfix 001 carried forward typed empty attempt state |
| 2 | before simulation | MATLAB product-date mismatch between `ver('MATLAB').Date` and `version('-date')` | hotfix 002 established five-field runtime semantics |
| 3 | during simulation StopFcn | `Simulink:Engine:CallbackEvalErr`; `TEplot` read base-workspace `tout` | hotfix 003 added guarded StopFcn suppression/restoration |
| 4 | before simulation | missing `frozen_original_generator_sha256` manifest field | hotfix 004 completed the generator/manifest contract |
| 5 | after simulation returned | `MATLAB:structRefFromNonStruct` at `simResult.who` | not fixed within EXP3; both permitted attempts were exhausted |

Incidents 3 and 5 are the two archived attempt records. Incidents 1, 2, and 4 occurred before `sim` and did not consume an attempt.

## Supersession

Experiment 3 V2 supersedes Experiment 3 through a new, separately pre-specified harness and fresh seed namespace. It does not rewrite, reopen, or retag Experiment 3. The original EXP3 freeze and hotfix provenance remain immutable historical evidence.
