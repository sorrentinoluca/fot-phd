# Experiment 3 — Post-Freeze Hotfix 001 Micro-Audit (read-only)

Scope: read-only verification of `EXP3_POST_FREEZE_HOTFIX_001` only. No file modified; no simulation;
no data; no commit/push/tag; no full redesign review. Date 2026-09-03 (UTC). HEAD `b02e93f9…a7c89`
(unchanged); hotfix present as uncommitted working-tree delta (2 tracked files modified + 3 untracked
hotfix files).

## Verdict

> ## ✅ HOTFIX ACCEPTED — SAFE TO FORMALIZE AND RETRY ATTEMPT 0

Evidence, point by point:

1. **Root cause — confirmed.** `git diff exp3-heldout-frozen` on the generator shows the failing site
   is the empty-log branch of `assert_attempt_allowed`: `prior = struct([])` (a 0×0 struct with **no**
   fields), after which `[prior.attempt]` raises `Unrecognized field name "attempt"`. The bug is
   exactly a field access on an empty **untyped** struct.
2. **Minimality — confirmed.** The only scientific-logic change is the empty view becoming a typed
   0×0 struct carrying precisely the three fields later read on `prior`:
   `struct('attempt',{},'structural_valid',{},'technical_failure_reason',{})`. Unchanged (not in the
   diff): case plan, physical_case IDs, primary/replacement seeds, fault mapping, max attempts,
   technical-replacement policy body, simulator configuration, RNG placement (`rng`→`sim` adjacency),
   output-validation criteria, statistical design. `exp3_case_plan.json` is **not** among the changed
   files and its SHA-256 is still `f2d27ef1…`. The remaining diff (a `HotfixManifestPath` param and
   re-anchoring the generator's self-hash gate to the authorized hotfix record) is the **necessary**
   consequence of changing one byte in a self-hash-checked generator; it changes only code-integrity
   gating, not experimental behavior, and additionally **re-asserts the case-plan hash is unchanged**.
3. **Empty-state correctness — confirmed.** On an empty log the typed `prior` yields `[prior.attempt]
   == []`, so `any(...)==false` → attempt 0 is allowed; `numel(prior)=0 < 2` holds; no undefined
   behavior remains.
4. **Duplicate protection — preserved.** The `EXP3:DuplicateAttempt` check is unchanged; a re-logged
   `(case, attempt)` enters the non-empty branch and is rejected.
5. **Replacement policy — preserved.** `assert_attempt_allowed` body is unchanged: attempt 1 is
   rejected without a logged attempt-0 technical failure (`EXP3:ReplacementWithoutPrimary` /
   `EXP3:UnauthorizedReplacement`), allowed only after a conforming technical failure, and uses the
   pre-specified `replacement_seed`; `EXP3:AttemptLimit` (`numel(prior)<2`) forbids any attempt >1. A
   new MATLAB regression (`test_exp3_attempt_policy.m`) asserts this policy is byte-identical to the
   generator's, and the Python suite asserts all four error IDs remain present.
6. **Scientific boundary — confirmed by code position.** The crash is at `assert_attempt_allowed`
   (called at generator line 59), which precedes output-directory creation (line 61), the pinned hash
   checks, and the `dist`/`rng`/`sim` block (line ~160+, inside the later `try`). Therefore no output
   directory, no attempt-log file (written only by `append_attempt_record` inside the try), no `sim`,
   no workbook, no signal inspection, and no scientific outcome occurred. The hotfix manifest records
   `sim_called=false, output_directory_created=false, attempt_log_created=false, workbooks_created=0`,
   consistent with the code path.
7. **Freeze provenance — intact.** `exp3-heldout-frozen^{commit}` still resolves to
   `b02e93f9…a7c89`; the frozen-tag generator blob is the original `018b13d5…`; `EXP3_FREEZE_MANIFEST.json`
   is byte-identical to the tag; the delta is documented separately in `EXP3_POST_FREEZE_HOTFIX_001.{json,md}`.
   The freeze-manifest artifacts that now differ from the working tree are **exactly** the two
   authorized files (`generate_exp3_heldout.m`, `test_exp3_pre_freeze.py`) — nothing else. Experiment 1
   frozen artifacts: **56/56 intact**. Hotfix-manifest hashes are self-consistent (frozen original
   `018b13d5…`, hotfixed `54d89c03…` = actual worktree generator, case plan `f2d27ef1…` = actual).
8. **Restart rule — confirmed.** Because no attempt was executed or logged, the correct restart is
   `EXP3-N-001 / attempt 0 / seed 310001`, not attempt 1 (attempt 1 is unauthorized without a logged
   attempt-0 technical failure).

## Blockers

**None.**

## Non-blocking observations

1. **Formalize the delta in version control.** The hotfix currently lives only in the working tree
   (HEAD is still the freeze commit; generator + test modified, and `EXP3_POST_FREEZE_HOTFIX_001.{json,md}`
   + `test_exp3_attempt_policy.m` untracked). Commit it as a documented post-freeze hotfix (optionally
   a new tag, e.g. `exp3-heldout-frozen-hotfix-001`) so the authorized delta and its provenance are
   tracked; leave the original `exp3-heldout-frozen` tag/commit untouched.
2. **Integrity anchor going forward.** By design the original freeze manifest no longer matches the
   two hotfixed files; `EXP3_POST_FREEZE_HOTFIX_001.json` is now the authoritative anchor the generator
   checks. Ensure the commit in (1) includes that manifest so the anchor is versioned.
3. **Python suite runtime.** The reported 22/22 / 93/93 must be run in the pinned reference venv
   (CPython 3.13.9 + `requirements.txt`); the device system Python (3.10, jsonschema 3.2.0) cannot
   import the verifier. Not related to the hotfix correctness.

## Scientific-boundary assessment

The hotfix **is** a software implementation correction made **before observation of any Experiment 3
experimental outcome**: it fixes empty-log handling at a point strictly upstream of the first `rng`,
`sim`, output directory, attempt-log write, workbook, and any signal inspection. It changes no
scientific design element (sample, IDs, seeds, fault mapping, replacement policy, simulator config,
RNG placement, validation, statistics). It therefore **does not alter the prospective character** of
Experiment 3, and the pre-specified freeze remains scientifically valid.

## Restart confirmation

> **CONFIRMED: restart at `EXP3-N-001` / attempt `0` / seed `310001`** (not attempt 1).

---
*Read-only micro-audit. No file modified, no simulation, no data, no commit/tag. Tag `exp3-heldout-frozen`
= `b02e93f9…a7c89` intact; Experiment 1 56/56 intact.*
