# EXP3_V2 First Scientific Run — Operational Preflight Plan

**Date**: 2026-09-03
**Scope**: Read-only preflight for EXP3V2-N-001 attempt 0 — the first of 30 real runs
**Status**: All prerequisites confirmed. Plan only — nothing executed.

---

## 1. Confirmed Final-Freeze State

| Check | Result |
|-------|--------|
| Tag `exp3-v2-heldout-frozen` exists | ✓ Annotated tag, message "Freeze Exp3 V2 held-out generation boundary" |
| HEAD == tag target | ✓ Both at `a55537dfc85db7e70f32ada21afffcb4e8824b96` |
| Commits ahead of tag | 0 |
| Tracked-file diff vs tag | Empty |
| Staged changes | None |
| Manifest status | `FROZEN_BEFORE_GENERATION` |
| Case plan status | `FROZEN_BEFORE_GENERATION` |
| `sentinel_validation_passed` | `true` |
| `v2_workbooks_at_freeze` | `0` |
| Workbooks in `tep_exp3_v2_heldout/` | 0 |
| Attempt log in `tep_exp3_v2_heldout/` | Does not exist (correct — no runs yet) |
| Scientific seeds consumed | 0 of 30 |

---

## 2. Exact MATLAB Command

```matlab
generate_exp3v2_heldout('EXP3V2-N-001', 0, 'SimulatorDir', '<MATERIALIZED_RUNTIME_DIR>')
```

**Source**: `phase_b/exp3_v2/generate_exp3v2_heldout.m`, line 1. `inputParser` at lines 8–12.

### Parameters

| Parameter | Value | Source |
|-----------|-------|--------|
| `physicalCaseId` | `'EXP3V2-N-001'` | `exp3v2_case_plan.json`, case index 1 |
| `attempt` | `0` | First attempt; must be 0 |
| `'SimulatorDir'` | Path to materialized runtime | Name-value pair; asserted non-empty at line 27 |
| `PythonExecutable` | **NOT a parameter** of `generate_exp3v2_heldout` | Only `sentinel_integration_run.m` takes it; the real wrapper does not |

### Expected Seed

| Field | Value |
|-------|-------|
| Primary seed | **320001** |
| RNG algorithm | `twister` |
| Replacement seed (attempt-1 only) | 1320001 |

The engine selects seed at `run_exp3v2_engine.m` line 29: `seed = double(entry.primary_seed)` when `attempt == 0`.

### Expected Case Identity

| Field | Value |
|-------|-------|
| `physical_case_id` | `EXP3V2-N-001` |
| `condition` | `Normal` |
| `dist` vector | `zeros(1, 28)` — no fault injection |
| Expected output shape | 3001 × 54 (3001 rows, 41 XMEAS + 12 XMV + 1 time) |

---

## 3. Runtime Materialization

The real wrapper does **not** invoke the materializer itself — that is the sentinel orchestrator's job. For production runs, you must materialize the runtime **before** calling `generate_exp3v2_heldout`.

### Materialization Command

```bash
PYTHONDONTWRITEBYTECODE=1 python3 \
  phase_b/exp3_v2/materialize_exp3v2_runtime.py \
  --manifest phase_b/exp3_v2/EXP3_V2_HARNESS_FREEZE_MANIFEST_004.json \
  --source-simulator-dir tennessee-eastman-dataset/simulator \
  --destination-parent /tmp/exp3v2_runtime
```

**Source**: `materialize_exp3v2_runtime.py`, lines 156–161 (argparse), lines 127ff (materialize logic).

This will:
1. Read the 8 external runtime dependencies from the harness manifest
2. Copy them from `tennessee-eastman-dataset/simulator/` to a timestamped subdirectory under `--destination-parent`
3. Verify SHA-256 and size of each file; reject symlinks; exclude `.slxc`
4. Print JSON `{"status": "PASS", "runtime_dir": "<path>", "dependency_count": 8}` on success
5. On failure, delete the partial directory and print `{"status": "FAIL", ...}`

The `runtime_dir` from the JSON output is the value to pass as `'SimulatorDir'`.

### Python Requirements

| Requirement | Sentinel-validated version |
|-------------|---------------------------|
| Python | 3.13.9 (`/opt/anaconda3/bin/python3.13`) |
| jsonschema | 4.25.0 |
| openpyxl | 3.1.5 |

The materializer itself needs only stdlib. jsonschema and openpyxl are needed by the verifier (`verify_exp3v2_heldout.py`), which should be run after generation.

---

## 4. Git Cleanliness Requirements

### What the real production path checks (`assert_exp3v2_freeze_boundary.m`)

- **HEAD == tag target** (`exp3-v2-heldout-frozen^{}`): Lines 36–43. HARD FAIL if not equal.
- **All 117 artifact SHA-256 hashes match disk**: Lines 22–33. HARD FAIL on any mismatch.
- **Each artifact exists in the Git tree at HEAD**: `git cat-file -e HEAD:<path>`. HARD FAIL if absent.

### What it does NOT check

- `git status --porcelain` — **not checked** by the real wrapper. That check exists only in `sentinel_integration_run.m` (line 28).
- Untracked files — **ignored**. The 13 untracked files currently present (PDFs, audit reports, `Claude outputs/`, `PROJECT_HANDOFF_PROMPT.md`, etc.) will NOT block the run.
- Staged but uncommitted changes — not explicitly checked, but any staged change that modifies a frozen artifact would be caught by hash mismatch.

### Current Repository State

```
13 untracked files (all outside the frozen artifact set)
0 modified tracked files
0 staged changes
HEAD == exp3-v2-heldout-frozen^{}
```

**Verdict: The repository can be used as-is for the first run.** No worktree is required. The untracked files do not interfere.

---

## 5. Worktree: Not Required, But Recommended Practice

### Can the main repository be used?

**Yes.** The freeze boundary enforces HEAD == tag and artifact hashes, not `git status --porcelain`. The 13 untracked files are outside the artifact set and will not trigger any assertion.

### Should a dedicated worktree be used?

**Optional but defensible.** A worktree provides:
- Insurance against accidental `git commit` or `git checkout` during a long sim run (~50h simulated time, typically 2–10 min wall-clock)
- Cleaner provenance narrative for the paper
- No risk of IDE auto-save or editor temp files touching tracked paths

If you choose a worktree:

```bash
git worktree add --detach /Users/luker/exp3v2_worktree exp3-v2-heldout-frozen
```

A durable location like `/Users/luker/exp3v2_worktree` is recommended over `/tmp` (which macOS clears periodically). The worktree needs the `tennessee-eastman-dataset/simulator/` source accessible — either symlinked or provided as an absolute path to the materializer.

**My recommendation**: Use the main repo. The fail-closed assertions are sufficient, and the sentinel validated them. A worktree adds operational complexity without covering a risk the harness doesn't already catch.

---

## 6. Output Paths

All derived from `generate_exp3v2_heldout.m`, lines 20–24:

| Artifact | Path |
|----------|------|
| Workbook | `tep_exp3_v2_heldout/mode1/EXP3V2-N-001__attempt-0.xlsx` |
| Attempt log | `tep_exp3_v2_heldout/exp3v2_attempt_log.json` |
| Output directory | `tep_exp3_v2_heldout/mode1/` |

The engine asserts `~isfile(outputPath)` at line 45 before writing — refuses to overwrite.

---

## 7. Fail-Closed Checks Before `rng` (Execution Order)

Every assertion below fires before `rng(seed, 'twister')` at line 126. If any fails, the engine throws and no simulation runs.

| Order | Check | Engine location |
|-------|-------|-----------------|
| 1 | Mode ∈ {'real', 'sentinel'} | line 13 |
| 2 | `assert_plan_constants` — all 30 cases canonical, seeds, conditions, simulator config | line 15 (→ lines 197–243) |
| 3 | `assert_mode_paths` — output must be under `tep_exp3_v2_heldout/` | line 16 (→ lines 245–263) |
| 4 | Seed authorization (attempt-0 → primary seed) | lines 17–35 |
| 5 | Output file does not exist (refuse overwrite) | line 45 |
| 6 | `assert_exp3v2_runtime_bundle` — 8 files, hashes, sizes, no symlinks | line 49 |
| 7 | Model, initial state, S-function source/MEX hash verification | lines 57–66 |
| 8 | Freeze boundary — manifest status, artifact hashes, HEAD == tag | line 32 in wrapper (`generate_exp3v2_heldout.m`) |
| 9 | Case plan status == `FROZEN_BEFORE_GENERATION` | line 31 in wrapper |
| 10 | Sentinel validation passed + zero workbooks at freeze | line 35 in wrapper |
| 11 | No sentinel ID accepted by real wrapper | line 40 in wrapper |
| 12 | `assert_attempt_allowed` — no duplicate, seed consistency | engine line ~285 |
| 13 | `capture_runtime` + `assert_runtime` — MATLAB R2025b Update 6, MACA64, exact build | lines 72–73 |
| 14 | `addpath` + `cd` + `rehash` + `load_system` | lines 86–93 |
| 15 | `assert_model_configuration` — solver, horizon, callbacks, initial state | line 94 (→ lines 315–337) |
| 16 | S-function identity + parameters (`temexd_mod`, `[] rand()`) | lines 100–107 |
| 17 | `configure_exp3v2_model` — suppress TEplot StopFcn, enable ReturnWorkspaceOutputs | line 108 |
| 18 | `dist` vector assignment (deterministic, no RNG) | lines 109–115 |
| 19 | `clear tout simout xmv` + assert workspace clean | lines 119–123 |
| 20 | `rng(320001, 'twister')` ← **this is the seed commitment point** | line 126 |
| 21 | `sim('MultiLoop_mode1')` — single call, immediately after rng | line 127 |

---

## 8. Complete Operational Plan — Step by Step

### Pre-session (one-time, before opening MATLAB)

```bash
# 1. Confirm HEAD is at the freeze tag
cd /Users/luker/fot-tep
git log --oneline -1    # must show a55537d
git rev-parse exp3-v2-heldout-frozen^{}   # must match HEAD

# 2. Materialize the runtime bundle
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3.13 \
  phase_b/exp3_v2/materialize_exp3v2_runtime.py \
  --manifest phase_b/exp3_v2/EXP3_V2_HARNESS_FREEZE_MANIFEST_004.json \
  --source-simulator-dir tennessee-eastman-dataset/simulator \
  --destination-parent /tmp/exp3v2_runtime

# 3. Capture the runtime_dir from the JSON output — call it $RUNTIME_DIR
# Example: /tmp/exp3v2_runtime/exp3v2_runtime_20260903T...
```

### MATLAB session

```matlab
% 4. Open MATLAB R2025b Update 6 (MACA64, /Applications/MATLAB_R2025b.app)
% 5. cd to the repository root
cd('/Users/luker/fot-tep')

% 6. Run the first case
generate_exp3v2_heldout('EXP3V2-N-001', 0, 'SimulatorDir', '<RUNTIME_DIR>')
```

### Post-generation verification

```bash
# 7. Verify the workbook
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3.13 \
  phase_b/exp3_v2/verify_exp3v2_heldout.py \
  --attempt-log tep_exp3_v2_heldout/exp3v2_attempt_log.json \
  --data-dir tep_exp3_v2_heldout/mode1 \
  --runtime-dir <RUNTIME_DIR>
```

Expected output: `PASS: Experiment 3 V2 ...`

### Expected artifacts after one successful run

```
tep_exp3_v2_heldout/
├── exp3v2_attempt_log.json          (1 entry: EXP3V2-N-001, attempt 0, structural_valid: true)
└── mode1/
    └── EXP3V2-N-001__attempt-0.xlsx (3001 rows × 54 columns)
```

---

**END OF PREFLIGHT PLAN — Nothing has been executed.**
