# Experiment 3 — Post-Freeze Hotfix 002 Micro-Audit (read-only)

Scope: read-only verification of `EXP3_POST_FREEZE_HOTFIX_002` only. No file modified; no simulation;
no data; no commit/push/tag; no full redesign. Date 2026-09-03 (UTC). HEAD `cdba020` (= hotfix-001
commit); hotfix 002 is an **uncommitted** working-tree delta (8 tracked files modified + 3 untracked:
`EXP3_POST_FREEZE_HOTFIX_002.{json,md}`, `test_exp3_runtime_provenance.m`). All chain checks were run
against the real `.git` (the new verifier/tests are git-dependent), plus a direct hash re-verification.

## Verdict

> ## ✅ HOTFIX 002 ACCEPTED — SAFE TO FORMALIZE AND RETRY ATTEMPT 0

1. **Root cause — confirmed.** The `exp3_case_plan.json` diff and the generator diff show the frozen
   field previously called `matlab_date` held `"June 30, 2026"`, while `capture_runtime` assigned
   `matlab_product_date = ver('MATLAB').Date = "28-Jul-2025"` and `assert_runtime` compared the two →
   `"MATLAB product date mismatch."`. `"June 30, 2026"` is `version('-date')` (runtime/update date);
   `"28-Jul-2025"` is `ver('MATLAB').Date` (product date). Two semantically different APIs had been
   bound to one frozen field. The installed runtime is nonetheless the correct one
   (`25.2.0.3312555 (R2025b) Update 6`, 2025b, 3312555, MACA64, `/Applications/MATLAB_R2025b.app`).
   The hotfix record's `actual_vs_expected` documents exactly this.
2. **Semantic correctness — confirmed (not an assert-silencer).** The five fields now map to their
   correct APIs, consistently across case plan, attempt-log schema, generator (`capture_runtime` +
   `assert_runtime` + `empty_record`), verifier (`EXPECTED_RUNTIME`), the sentinel probe, and the new
   MATLAB test: `matlab_version_full←version`, `matlab_release←version('-release')`,
   `matlab_build←parsed-from-version` (fail-closed regexp), `matlab_product_date←ver('MATLAB').Date`
   (=28-Jul-2025), `matlab_runtime_update_date←version('-date')` (=June 30, 2026). No ambiguous
   `matlab_date` remains: `validate_case_plan` now asserts `set(runtime)==expected set`
   ("runtime field set mismatch"), and the dead `simulink_separate_build` was removed. The new
   `test_exp3_runtime_provenance.m` exercises the **real** APIs and adds a negative test per MATLAB
   field asserting the exact rejection identifier — it is genuine coverage, not hardcoded pass-values.
3. **Minimality — confirmed.** `git diff` (freeze/hotfix001 → worktree) touches exactly runtime
   provenance + integrity-chain machinery. The `exp3_case_plan.json` change is confined to the
   `runtime` block; the `cases`, `rng`, `sample`, `simulator`, and `statistics` blocks are byte-
   unchanged. Therefore all invariants hold: 30-case plan (6 Normal/F1/F8/F10/F13), IDs
   `EXP3-N-001…EXP3-F13-006`, primary seeds 310001–310030, replacement seeds (+1e6), bootstrap 310031,
   fault mapping, RNG algorithm `twister`, RNG placement (`rng`→`sim` adjacency), simulator config
   (`a0413e16…`, `ode45`, 0–50 h, 1/60 h, injection 10 h, 3001×54), replacement policy, max attempts,
   statistical/analysis plan. No scientific parameter changed.
4. **Runtime gate — fail-closed.** `assert_runtime` accepts exactly the correct runtime and asserts
   every field (version_full, release, build, product_date, runtime_update_date, simulink ×3,
   architecture, matlabroot) with a distinct error id; the MATLAB regression proves rejection on a
   wrong value for each of the five MATLAB fields.
5. **Second-failure boundary — confirmed and precisely documented.** The runtime check
   (`assert_runtime`) runs before the `try`/`sim` block. The output directory `mkdir` runs earlier, so
   the failure created only the empty `tep_exp3_heldout/` and `tep_exp3_heldout/mode1/` directories.
   Verified on disk: both dirs exist and are empty; no workbook, no attempt log, no final manifest; no
   `sim`, no run RNG, no signal inspection, no scientific outcome. The hotfix record's
   `failed_invocation` encodes exactly this (`output_directories_created=true`, `directories_empty=true`,
   all scientific fields `false`/`0`), and the verifier enforces this exact object.
6. **Prospective integrity — intact.** The change is a runtime-provenance metadata correction made
   before the first experimental simulation and before any Exp3 scientific outcome; it modifies no
   scientific design element. The prospective character of Experiment 3 is preserved.
7. **Freeze-chain — verified end to end against `.git`.** `exp3-heldout-frozen^{}` = `b02e93f9…a7c89`;
   the freeze manifest is byte-identical to the tagged bytes; all 12 frozen artifacts hash-match at the
   tag. Hotfix 001 is unchanged: `hotfix_001_generator_sha256` = generator@`cdba020` =
   `hotfix001.hotfixed_generator_sha256` = `54d89c03…`; `hotfix_001_manifest_sha256` matches. Hotfix 002
   is a separate record whose `changed_artifacts` before-hashes equal the bytes at `cdba020` and whose
   after-hashes equal the current files; `frozen_original_*` and `original_freeze_manifest_sha256` match
   the freeze; the candidate hashes match (`gen f1cf1647…`, `plan 967423e1…`, `verifier 794a7a7e…`).
   The verifier walks `freeze → hotfix001 → hotfix002` and re-derives all of this from git. Experiment 1
   remains intact (**56/56** frozen hashes).
8. **Restart — confirmed.** No `sim`, no run RNG, no logged attempt ⇒ the correct restart is
   `EXP3-N-001 / attempt 0 / seed 310001` (not attempt 1). The pre-existing empty output directories do
   not block it (dir creation is `~isfolder`-guarded; overwrite refusal triggers only on an existing
   output **file**, and none exists).

## Blockers

**None.**

## Non-blocking observations

1. **Formalize the delta.** Hotfix 002 is uncommitted (8 tracked files + 3 untracked). Commit it as a
   documented post-freeze provenance hotfix (as was done for hotfix 001 at `cdba020`), leaving the
   `exp3-heldout-frozen` tag and the hotfix-001 commit untouched; include the hotfix-002 manifest,
   report, and `test_exp3_runtime_provenance.m` in that commit.
2. **Verification environment.** The updated verifier/tests need jsonschema ≥ 4.18 **and** a git
   checkout where the tag and `cdba020` are reachable (they call `git show`/`git rev-parse`). Run them
   in the pinned reference venv against the real repo; the device system Python (3.10, jsonschema 3.2.0)
   cannot import the verifier. (This audit verified the git chain directly instead of re-running it.)
3. **Sentinel-probe asymmetry (cosmetic).** `validate_exp3_rng_runtime.m` still carries extra
   descriptive fields (`matlab_product_version`, `matlab_product_release`) not present in the gated
   runtime block. Harmless — the probe is not the gate — but a minor naming asymmetry.
4. **Empty output dirs on disk.** The failed run left `tep_exp3_heldout/{,mode1}` empty. Harmless and
   documented in the record; may be left as-is (retry is unaffected).

## Semantic-provenance assessment

The five runtime fields now correctly represent their MATLAB APIs:
`matlab_version_full = version`; `matlab_release = version('-release')`;
`matlab_build = parsed from version`; `matlab_product_date = ver('MATLAB').Date` (28-Jul-2025);
`matlab_runtime_update_date = version('-date')` (June 30, 2026). No field is used with two meanings; no
ambiguous `matlab_date` survives.

## Scientific-boundary assessment

**No Exp3 scientific outcome was observed before this correction.** The second failure occurred after
only empty output directories were created and strictly before any `rng`/`sim`/workbook/attempt-log/
manifest/signal step. The change alters no scientific design element; the prospective character of
Experiment 3 remains intact.

## Freeze-chain assessment

**Confirmed:** original freeze unchanged (tag → `b02e93f9…a7c89`, manifest byte-identical, 12/12 tagged
artifacts intact) → hotfix 001 unchanged (`cdba020`, generator `54d89c03…` preserved and bound) →
hotfix 002 a separate, chain-bound delta (uncommitted working tree + its own manifest/report).

## Restart confirmation

> **CONFIRMED: restart at `EXP3-N-001` / attempt `0` / seed `310001`** (not attempt 1).

---
*Read-only micro-audit. No file modified, no simulation, no data, no commit/tag. Tag
`exp3-heldout-frozen` = `b02e93f9…a7c89` intact; hotfix 001 = `cdba020` intact; Experiment 1 56/56
intact. Chain freeze→hotfix001→hotfix002 verified against `.git`.*
