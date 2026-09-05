# EXP3_V2 Final-Freeze & First-Real-Run Readiness Audit

**Auditor**: Independent read-only review (Claude, senior-supervisor role)
**Date**: 2026-09-03
**Scope**: All 12 checklist items from the user's specification
**Repository**: `fot-tep`, HEAD at commit `258f629f`
**Harness**: Revision 004, tag `exp3-v2-harness-frozen-004`

---

## VERDICT: READY FOR EXP3_V2 FINAL FREEZE

No blocking findings. All 12 checklist items pass. The sentinel genuinely validates the production path. The human finalization sequence (status transition → commit → annotated tag) may proceed.

---

## Checklist Evidence

### 1. Sentinel-to-real shared-engine equivalence

Both `generate_exp3v2_sentinel.m` and `generate_exp3v2_heldout.m` build a `config` struct and call the identical function:

```
record = run_exp3v2_engine(config);
```

The engine (`run_exp3v2_engine.m`) accepts `config.mode ∈ {'real','sentinel'}` (line 13–14). The mode field controls exactly three things:

- **Authorization gate** (lines 17–24): sentinel accepts only `EXP3V2-SENTINEL-002`/seed `987654322`/attempt 0; real accepts attempt ∈ {0,1} and selects primary or replacement seed.
- **Path boundary** (`assert_mode_paths`, lines 245–263): real writes must be under `tep_exp3_v2_heldout/`; sentinel paths must be disjoint from both `tep_exp3_v2_heldout/` and `tep_exp3_heldout/`.
- **Attempt policy** (`assert_attempt_allowed`, line 291): sentinel allows one attempt with no replacement; real allows attempt-0 then attempt-1 only after a technical failure.

Every other line of the engine — `addpath`, `cd`, `rehash`, `load_system`, model configuration, `dist` vector setup, workspace clearing, `rng`, `sim`, output extraction, workbook writing, model-hash post-check, `onCleanup` — executes identically for both modes.

**PASS.** The sentinel exercised the same engine the 30 real runs will use.

### 2. Execution ordering: rng → sim adjacency

`run_exp3v2_engine.m`, lines 125–127:

```matlab
% PROTOCOL-CRITICAL: rng is the last random-relevant statement before sim.
rng(seed, 'twister');
simResult = sim(modelName);
```

Between `rng` and `sim` there is no intervening call that could consume or reseed the PRNG. The workspace clear (`clear tout simout xmv` + assertion) precedes `rng`. The `dist` vector assignment (`zeros(1,28)`, then deterministic fault-index write) also precedes `rng`. Exactly one `sim` call exists in the engine.

**PASS.**

### 3. Inter-run isolation

- Base-workspace outputs (`tout`, `simout`, `xmv`) are cleared at line 121 and asserted absent at line 122 before every run.
- `ReturnWorkspaceOutputs` is enabled by `configure_exp3v2_model.m`, so `sim` returns a `Simulink.SimulationOutput` object. `extract_exp3v2_outputs.m` uses typed `simResult.get()` — no `evalin('base',…)` fallback exists.
- `onCleanup` restores model config, path, and cwd even on exception.
- File-generation isolation (`configure_exp3v2_file_generation.m` / `restore_exp3v2_file_generation.m`) redirects `.slxc` and codegen to the throwaway root.
- Sentinel evidence confirms all restoration checks PASSED: `StopFcn_restored`, `ReturnWorkspaceOutputs_restored`, `Dirty_restored`, `model_hash_restored`, `injected_error_restoration_test`, `file_generation_isolated`, `file_generation_restored`.

**PASS.**

### 4. Case plan integrity

`exp3v2_case_plan.json`: 30 cases, status `PRE_FREEZE_DRAFT`.

- Conditions: Normal×6, F1×6, F8×6, F10×6, F13×6 (verified by `assert_plan_constants`, line 197ff).
- Primary seeds: 320001–320030, consecutive, no duplicates. Replacement seeds: 1320001–1320030. Bootstrap seed: 320031.
- Simulator config: Mode 1, ode45, 0–50h, sampling 1/60 h, fault injection at 10h, expected shape 3001×54, commit `a0413e16`.
- `assert_plan_constants` (lines 197–243) validates all of the above at engine entry for every run.
- Engine line 112: fault index restricted to `ismember(faultIndex, [1 8 10 13])`.

**PASS.**

### 5. Attempt-log lifecycle and production safeguards

- `append_exp3v2_attempt_record.m`: append-only JSON, temp-file + `movefile` atomicity, refuses stale temp.
- `assert_attempt_allowed` (line 285ff): rejects duplicate attempt, requires prior technical failure for attempt-1, enforces primary vs replacement seed, max 2 attempts.
- `test_exp3v2_attempt_policy.m`: tests empty-log, attempt-0 allowed, attempt-1 blocked without prior, attempt-1 allowed after tech failure, duplicate blocked, JSON array serialization. All without sim.
- Real wrapper (`generate_exp3v2_heldout.m`, line 40): rejects all sentinel IDs via `startsWith(string(physicalCaseId), 'EXP3V2-SENTINEL-')`.

**PASS.**

### 6. Runtime materialization and external bundle

- `assert_exp3v2_runtime_bundle.m`: exactly 8 pinned files (Mode1xInitial.mat, Mode_1_Init.m, MultiLoop_mode1.mdl, TElib.mdl, TEplot.m, temexd_mod.c, temexd_mod.mexmaca64, teprob_mod.h). Rejects symlinks. SHA-256 + size per file.
- `materialize_exp3v2_runtime.py`: copies from source simulator dir to throwaway, verifies hashes, excludes `.slxc`.
- Sentinel evidence records all 8 dependencies with matching hashes.
- Real wrapper requires explicit `'SimulatorDir'` parameter (line 27: asserts `strlength > 0`).

**PASS.**

### 7. Sentinel evidence authenticity

`EXP3_V2_SENTINEL_EVIDENCE.json`:

- Status: `PASS`
- Harness revision: 004, commit `258f629f`
- Identity: `EXP3V2-SENTINEL-002`, seed `987654322`
- Workbook: 3001×54, 1704419 bytes, SHA `337f3e70…`
- All 17 named checks: PASS
- 114 artifact hashes recorded
- 8 external runtime dependencies recorded
- Python 3.13.9, jsonschema 4.25.0, openpyxl 3.1.5
- Verifier output: `"PASS: Experiment 3 V2 sentinel verification succeeded."`

SHA of evidence file matches final manifest's `sentinel_evidence_sha256`: `daf67273138bf192d77e62dd56bc8598a90070baaf4f8714a8851ed3ca9f3a86`.

**PASS.**

### 8. Freeze-boundary chain

- Harness manifest 004 SHA `dacc810bd29203d3d701e3613a9ce8c72dc6423aa475f5c4e8c8b4989b40e139` matches final manifest's `harness_boundary.manifest_sha256`.
- Final manifest (`EXP3_V2_FREEZE_MANIFEST.json`): status `PENDING_HUMAN_FINAL_FREEZE`, `sentinel_validation_passed: true`, `v2_workbooks_at_freeze: 0`.
- 117 artifacts listed with SHA-256 hashes. Manifest does NOT list itself (not self-referential) — correct.
- `allowed_finalization_changes`: 3 files with before/after SHA pairs (protocol, verifier, pre-freeze test).
- Tag target: `258f629f`.

**PASS.**

### 9. PRE_FREEZE_DRAFT → FROZEN_BEFORE_GENERATION transition

- Case plan currently at `PRE_FREEZE_DRAFT` — correct for pre-finalization state.
- Final manifest documents the required transition under `finalization_pending.case_plan_status_transition`.
- `generate_exp3v2_heldout.m` line 31 asserts `strcmp(plan.status, 'FROZEN_BEFORE_GENERATION')` — the real wrapper will refuse to run until this transition is made.
- Manifest records `case_plan.bytes_unchanged_from_harness: true` — the plan content itself does not change, only its status field.

**PASS.**

### 10. Final-freeze commit atomicity and tag self-containment

`finalization_pending` in the final manifest lists 4 steps: `human_review`, `case_plan_status_transition`, `commit`, `annotated_tag`. The `allowed_finalization_changes` constrains exactly which files may differ from harness freeze. The tag `exp3-v2-heldout-frozen` will be the single point of reference for all 30 runs. `assert_exp3v2_freeze_boundary.m` checks HEAD == tag target at real-run time.

**PASS.**

### 11. No workbooks or attempt logs exist yet

`tep_exp3_v2_heldout/` — confirmed empty of workbooks and attempt logs. The final manifest binds `v2_workbooks_at_freeze: 0`. The real wrapper asserts this at line 35.

**PASS.**

### 12. Verifier and pre-freeze test coverage

- `verify_exp3v2_heldout.py` (under `phase_b/tests/`): schema validation, numeric bounds, round-trip, header check.
- `test_exp3v2_pre_freeze.py` (under `phase_b/tests/`): pre-freeze assertions including artifact inventory, hash verification, status checks.
- `test_exp3v2_runtime_materialization.py` (under `phase_b/tests/`): runtime bundle integrity.
- All three paths are listed in the harness manifest's `REQUIRED_HARNESS_PATHS`.

**PASS.**

---

## Production-Only Branches Not Exercised by Sentinel

These code paths exist only in the real production run and were NOT exercised by the sentinel. None are blocking — they are guarded by assertions and tested by unit tests — but they are the residual untested-by-integration surface:

1. **Attempt-1 replacement path** (`run_exp3v2_engine.m`, lines 28–31): When `attempt == 1`, the engine uses `entry.replacement_seed` instead of `entry.primary_seed`. The sentinel is hard-coded to `attempt == 0` only (line 20). Unit-tested in `test_exp3v2_attempt_policy.m` but never integration-tested with an actual `sim` call.

2. **Fault-injection branches F1, F8, F10, F13** (`run_exp3v2_engine.m`, lines 110–115): The sentinel runs condition `Normal` (dist = zeros(1,28)). The four fault conditions set `dist(faultIndex) = 1`. The `dist` assignment is deterministic and trivial, but the TEP simulator's response to each fault type is exercised only in production. The `ismember(faultIndex, [1 8 10 13])` guard (line 112) prevents out-of-range faults.

3. **Non-empty attempt log** (`assert_attempt_allowed`): The sentinel runs against a fresh (empty) throwaway log. The first real run will also face an empty log. The non-trivial paths (duplicate rejection, prior-failure check) only activate from the second run onward. Unit-tested in `test_exp3v2_attempt_policy.m`.

---

## Residual Risks

All rated **LOW** — none warrant blocking the freeze.

| # | Risk | Mitigation | Severity |
|---|------|------------|----------|
| R1 | TElib.mdl compilation warning at Simulink load time (cosmetic, observed in prior runs) | Does not affect simulation output; sentinel workbook passed all numeric checks | LOW |
| R2 | Variable Time Delay block buffer growth under ode45 | Sentinel completed 0–50h without timeout or memory error; 3001 rows confirmed | LOW |
| R3 | MATLAB R2025b Update 6 on Apple Silicon (MACA64) — no Rosetta layer but architecture-specific MEX | `temexd_mod.mexmaca64` is pinned and hash-verified; sentinel ran natively | LOW |
| R4 | 1/60 h sampling serialized as `0.016666666666666666` (17 significant digits) — Rev 003 truncated to 6 digits and failed | Rev 004 uses full-precision `format_exp3v2_csv_scalar.m`; sentinel CSV round-tripped correctly | LOW |

---

## First-Run Invocation Syntax

Derived from `generate_exp3v2_heldout.m` signature (line 1) and its `inputParser` (lines 8–13):

```matlab
generate_exp3v2_heldout('EXP3V2-N-001', 0, 'SimulatorDir', '<path_to_materialized_runtime>')
```

Where:

- `'EXP3V2-N-001'` — the first Normal-condition case (physical_case_id from case plan)
- `0` — attempt number (must be 0 for first attempt)
- `'SimulatorDir'` — name-value pair; the absolute path to the directory where `materialize_exp3v2_runtime.py` placed the 8 pinned files

**Prerequisites before this call:**

1. Human completes finalization: `PRE_FREEZE_DRAFT` → `FROZEN_BEFORE_GENERATION` in `exp3v2_case_plan.json`, `PENDING_HUMAN_FINAL_FREEZE` → `FROZEN_BEFORE_GENERATION` in `EXP3_V2_FREEZE_MANIFEST.json`, commit, annotated tag `exp3-v2-heldout-frozen`.
2. Runtime materialized via `materialize_exp3v2_runtime.py` into a clean directory.
3. MATLAB R2025b Update 6 session with Simulink loaded, working directory at repo root or `phase_b/exp3_v2/`.

---

**END OF AUDIT**
