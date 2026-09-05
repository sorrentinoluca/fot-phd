# Experiment 3 — Post-Freeze Hotfix 003 Micro-Audit (read-only)

Scope: read-only verification of `EXP3_POST_FREEZE_HOTFIX_003` (headless plotting-callback hotfix)
only. No file modified; no simulation; no data; no commit/push/tag; no full redesign; **attempt 1 not
executed**. Date 2026-09-03 (UTC). HEAD `2813002` (= hotfix-002 commit, tag
`exp3-post-freeze-hotfix-002`). Hotfix 003 is an **uncommitted** working-tree delta (5 tracked files
modified + 5 untracked: `EXP3_POST_FREEZE_HOTFIX_003.{json,md}`, `suppress_/restore_exp3_plot_stopfcn.m`,
`test_exp3_stopfcn_management.m`). The new verifier/tests are git-dependent, so the chain was verified
directly against `.git`.

## Verdict

> ## ✅ HOTFIX 003 ACCEPTED — SAFE TO FORMALIZE AND EXECUTE EXP3-N-001 ATTEMPT 1

## Blockers

**None.**

## Non-blocking observations

1. **Attempt-log JSON shape (pre-existing, not from hotfix 003).** `tep_exp3_heldout/exp3_attempt_log.json`
   serializes `attempts` as a JSON **object** (a single record), not a 1-element array — a MATLAB
   `jsonencode(scalar struct)` artifact of `append_attempt_record`. The MATLAB read path handles it
   (attempt 1 authorization works), and the log becomes a proper array once ≥2 records exist. The
   Python verifier's `load_attempt_log`, however, requires a list, so a *mid-generation* full-verifier
   run on the single-record log would reject it. Recommend normalizing `append_attempt_record` to emit
   a 1-element array. Does not block attempt 1.
2. **Uncommitted delta.** Formalize hotfix 003 as a documented post-freeze commit (+ optional tag, as
   for h1/h2), leaving the freeze tag and the h1/h2 commits/tags untouched; include the two
   `HOTFIX_003.*`, the two callback helpers, and `test_exp3_stopfcn_management.m`.
3. **Verification environment.** Verifier/tests need jsonschema ≥ 4.18 **and** a checkout where the
   tags/commits are reachable (`git show`/`rev-parse`). Run in the pinned reference venv on the real
   repo; the device system Python (3.10, jsonschema 3.2.0) cannot import the verifier. (Chain verified
   directly here instead.)
4. **Residual on-disk state from attempt 0.** Empty `tep_exp3_heldout/{,mode1}` and the single-record
   attempt log persist. No attempt-0 workbook was written (`output_size_bytes=0`); attempt 1 writes a
   distinct `EXP3-N-001__attempt-1.xlsx`, so refuse-overwrite is not triggered. Harmless.

## TEplot assessment

`TEplot` **is purely plotting/post-processing.** The frozen model's `StopFcn` is exactly `TEplot`
(`MultiLoop_mode1.mdl` line 118). `TEplot.m` reads the simulation outputs `tout`/`simout`/`xmv`,
builds label/title structs, and creates figures + `uicontrol` selectors; a grep confirms it contains
**no** `rand`/`randn`/`rng`, no `dist`, no `xInitial`, no `set_param`, no `Solver` change, no
`assignin`, no `sim`, no `save_system`, no `evalin`. It modifies no plant dynamics, fault realization,
initial state, solver, randomness, or measurement generation, and produces no data the dynamics
consume. Its temporary suppression therefore **leaves the scientific simulation unchanged**: with the
callback neutralized the run produces the identical numeric realization, differing only in that the
post-run plotting/UI is skipped. The failure is fully explained: as a model `StopFcn`, `TEplot`
executes inside `sim` and references base-workspace `tout`, which does not exist in the function-scoped
generator → `Unrecognized function or variable 'tout'` (`Simulink:Engine:CallbackEvalErr`).

## RNG assessment

**Confirmed.** Callback suppression occurs **before** RNG placement (the
`suppress_exp3_plot_stopfcn` call precedes `dist = zeros(1,28)` and `rng(seed,'twister')`), and no
random-relevant operation is introduced between `rng(seed,'twister')` and `sim(modelName)` — they
remain adjacent, with the restore performed only **after** `sim`. Neither suppression/restore nor
`TEplot` consumes randomness (`set_param`/`get_param` on `StopFcn`/`Dirty` do not touch the RNG; grep
confirms no RNG calls in the callback helpers or `TEplot`). `test_generation_rng_and_sim_are_adjacent`
enforces the adjacency.

## Model-integrity assessment

**Confirmed — no permanent model modification.** `suppress_exp3_plot_stopfcn` accepts **only** exactly
`StopFcn == 'TEplot'` (rejects empty, different, or composite callbacks with
`EXP3:StopCallbackMismatch`, without mutating them), arms `onCleanup(restore)` **before** clearing,
sets `StopFcn=''`, and never calls `save_system`. `restore_exp3_plot_stopfcn` restores exactly the
original `TEplot` and the original `Dirty` state (both asserted), and is fail-closed if the model is
closed. The generator restores + asserts `StopFcn=='TEplot'` after `sim` **and** in the `catch` path
(raising a combined `EXP3:StopCallbackRestoreFailed` if restore fails), with the `onCleanup` guard as
backstop — so control cannot exit leaving a different callback without signaling. The pinned model file
stays byte-identical: the on-disk `MultiLoop_mode1.mdl` is `d2f6659f65935021d4b1813e7189be02e7ae9f5639b794e8edc4f2f3c5cddba8`,
and `test_exp3_stopfcn_management.m::testPinnedModelUnchanged` loads the real model, suppresses,
restores, closes, and asserts the file hash is unchanged, without calling `sim`.

## Attempt-policy assessment

**Confirmed.** The real attempt log records `EXP3-N-001 / attempt 0 / seed 310001`,
`structural_valid=false`, non-empty `technical_failure_reason` (`Simulink:Engine:CallbackEvalErr … 'TEplot'`)
→ attempt 0 is a consumed technical failure. It is append-only and immutable; the duplicate-attempt
check (`EXP3:DuplicateAttempt`) makes attempt 0 non-retriable. Attempt 1 is authorizable **only**
because a logged attempt 0 exists with `structural_valid=false` and a non-empty reason
(`EXP3:ReplacementWithoutPrimary`/`EXP3:UnauthorizedReplacement` otherwise); it uses replacement seed
**1310001**. `numel(prior) < 2` (`EXP3:AttemptLimit`) forbids attempt > 1. The generator's
`assert_attempt_allowed` is unchanged by hotfix 003; the MATLAB and Python regressions bind and cover it.

## Scientific-boundary assessment

**No accepted Exp3 scientific output or diagnostic information was observed from attempt 0.** `sim` was
reached and the primary seed 310001 was consumed, but the failure occurred in the post-run plotting
`StopFcn`: `workbooks_created=0`, `output_size_bytes=0`, no signal inspection, no accepted scientific
output, no diagnostic/FoT outcome. The replacement was pre-specified in the frozen protocol before any
outcome (attempt 1, seed 1310001, both frozen), so this is **not** data selection; the prospective
character of Experiment 3 remains intact. The hotfix record's `failed_invocation` reflects this exactly
(`sim_called=true`, `sim_returned_successfully=false`, all scientific fields false/0,
`attempt_0_recorded_technical_failure=true`).

## Freeze-chain assessment

**Confirmed:** original freeze unchanged (`exp3-heldout-frozen` → `b02e93f9…a7c89`; freeze manifest
byte-identical to tag; 12/12 tagged artifacts intact) → hotfix 001 unchanged (`cdba020`) → hotfix 002
unchanged (`2813002`, tag `exp3-post-freeze-hotfix-002`; generator `f1cf1647…` bound) → hotfix 003 a
separate authorized delta (uncommitted working tree + its own manifest). The hotfix-003 record's chain
hashes all match reality (`original_freeze_manifest`, `hotfix_001/002_manifest`, `hotfix_002_generator`,
`hotfix_003_generator = da419e5d…`, `hotfix_003_case_plan = 967423e1…` unchanged); its `changed_artifacts`
before-hashes equal the bytes at `2813002` and after-hashes equal the current files; `exp3_case_plan.json`
is **not** in the changed set (scientific plan untouched). The verifier (`validate_hotfix_003`) walks the
full chain, re-checks the frozen artifacts against the git tag, enforces the boundary, the authorized
restart (seed 1310001), and the exact permitted-delta set, and binds the generator self-hash — it is
not weakened. **Experiment 1: 56/56 frozen artifacts intact.**

## Minimality

The only scientific-logic-adjacent change is non-scientific: temporary suppression/restoration of the
plotting `StopFcn`, plus provenance/test/verifier updates. Case plan, 30-case sample (6×5), physical
IDs, primary seeds 310001–310030, replacement seeds, bootstrap 310031, fault mapping, `twister`,
simulator commit/S-function/initial state/`dist`/`ode45`/0–50 h/1-min/injection 10 h/3001×54, output
validity rules, replacement policy, max attempts, append-only log, no-overwrite policy, and the
statistical/analysis plan are all unchanged (case plan byte-identical to hotfix 002; the protocol diff
is documentation only).

## Restart confirmation

> **CONFIRMED: next and only replacement is `EXP3-N-001` / attempt `1` / seed `1310001`** (not attempt 0,
not seed 310001, not any other seed; attempt > 1 forbidden).

---
*Read-only micro-audit. No file modified, no simulation, no data, no commit/tag, attempt 1 not executed.
Chain freeze→h1→h2→h3 verified against `.git`; tag `exp3-heldout-frozen` = `b02e93f9…a7c89` and hotfix
002 tag = `2813002…` intact; model `.mdl` = `d2f6659f…` unchanged; Experiment 1 56/56 intact.*
