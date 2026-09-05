# Experiment 3 — First-Physical-Run Readiness Audit (read-only)
## FoT–TEP, IEEE BigData 2026

Role: read-only technical auditor. Repository: `/Users/luker/fot-tep`. Audit date: 2026-09-02 (UTC).
No file was modified/created/deleted/renamed; no git state change; no MATLAB generator run; no `sim`;
no workbook; no verbalization/feature/inference; no scientific evaluation. Untracked files left
untouched. Verifier/tests were run only in read-only pre-freeze mode (and one expected fail-closed
probe), with `PYTHONDONTWRITEBYTECODE=1`; the authoritative run used the pinned reference deps in an
isolated copy, never writing into the project.

---

## 1. OVERALL VERDICT

> ## ✅ OVERALL VERDICT: READY FOR FIRST PHYSICAL RUN

HEAD equals the expected commit and the `exp3-heldout-frozen` tag; the working tree has no tracked
modifications; the freeze manifest and all 12 boundary artifacts hash-match; the 30-case plan is
exactly canonical; templates/policies are correct and empty/TBD; the isolated simulator is present
with all four hashes matching the case plan; no Experiment 3 data exists yet; Experiment 1 is intact
(56/56 frozen hashes); and the verifier (`--pre-freeze`) plus the 19-test pre-freeze suite pass in
the pinned reference environment. No blocker was found.

---

## 2. CHECK TABLE

| Check | Expected | Observed | PASS/FAIL | Evidence |
|---|---|---|---|---|
| Repo directory | `/Users/luker/fot-tep` | `…/mnt/fot-tep` (= that path) | PASS | `git rev-parse --show-toplevel` |
| HEAD commit | `b02e93f9…a7c89` | `b02e93f92bf6fa85a4fd0a2e010bac365a3a7c89` | PASS | `git rev-parse HEAD` |
| Tag resolves | `exp3-heldout-frozen^{commit}` = expected | `b02e93f9…a7c89` | PASS | `git rev-parse exp3-heldout-frozen^{commit}` |
| Branch | main | main | PASS | `git rev-parse --abbrev-ref HEAD` |
| Tracked modifications | none | none (only untracked files) | PASS | `git status --short` (all `??`) |
| Untracked preserved | untouched | untouched | PASS | none modified |
| Freeze manifest JSON | valid | valid | PASS | parse `EXP3_FREEZE_MANIFEST.json` |
| Manifest status | `FROZEN_BEFORE_GENERATION` | idem | PASS | field read |
| Manifest freeze_tag | `exp3-heldout-frozen` | idem | PASS | field read |
| created_before_generation | true | true | PASS | field read |
| exp3_workbooks_at_freeze | 0 | 0 | PASS | field read |
| Manifest artifacts present + SHA-256 | all match | 12/12 PASS | PASS | recomputed SHA-256 vs manifest |
| Case plan count | 30 | 30 | PASS | `exp3_case_plan.json` |
| Canonical order + 6/group | N,F1,F8,F10,F13 ×6 | exact | PASS | programmatic |
| IDs | `EXP3-N-001`…`EXP3-F13-006` | exact, in order | PASS | programmatic |
| Run index 1–6/group | yes | yes | PASS | programmatic |
| Primary seeds | 310001–310030 consecutive | exact | PASS | programmatic |
| Replacement seeds | primary + 1,000,000 | 1310001–1310030 | PASS | programmatic |
| RNG algorithm | twister (all) | twister (all) | PASS | programmatic |
| Allowed attempts | {0,1}, max 2 | [0,1], 2 | PASS | plan + schema |
| Bootstrap seed | 310031, not a run seed | 310031, disjoint | PASS | programmatic |
| No duplicate IDs/seeds; namespaces disjoint | yes | yes | PASS | programmatic |
| Simulator identity | commit `a0413e16…`, `MultiLoop_mode1`, Mode 1/normal/ode45, 0–50 h, 1/60 h, inject 10 h | exact | PASS | case plan + protocol |
| Output regime | 3001×54, `Sheet1` | exact | PASS | case plan; matches Exp1 held-out manifest |
| Runtime identity | R2025b `25.2.0.3312555`, Simulink 25.2, MACA64, `/Applications/MATLAB_R2025b.app` | exact | PASS | case plan runtime block |
| Statistics plan | physical-run unit; paired cluster bootstrap; 10 000; seed 310031; Exp3-only primary; B−A primary; B−E supporting; pooled secondary | exact | PASS | case plan statistics block |
| Attempt-log schema | valid; attempt 0/1; no diagnostic fields | valid; min0/max1; disjoint from diagnostic fields | PASS | schema parse |
| Attempt-log template | empty (`attempts=[]`) | empty | PASS | template parse |
| Manifest template | 30 rows, IDs in order, non-key fields TBD | exact | PASS | CSV parse |
| Replacement policy | attempt1 only after attempt0 technical failure; no attempt2; append-only; refuse overwrite; filename `<id>__attempt-<n>.xlsx` | enforced in plan+schema+generator+verifier | PASS | generator L338–363, L64–67; verifier |
| Exclusion criteria | purely technical | only technical (§9.1) | PASS | protocol; generator `inspect_numeric_output` |
| No Exp3 generation | absent | `tep_exp3_heldout/` absent; 0 workbooks; no operational log/manifest | PASS | filesystem checks |
| `.gitignore` ignores raw dir | yes | line 28 `tep_exp3_heldout/` | PASS | grep |
| Isolated simulator | present + 4 hashes match plan | dir+files present; 4/4 PASS | PASS | SHA-256 vs case plan |
| Experiment 1 immutable | 56/56 frozen hashes | 56/56, 0 failures | PASS | `PHASE_B_PROTOCOL_HASHES.json` recompute |
| Terminology | no forbidden positive claims | only "cross-domain validity" disclaimer | PASS | grep |
| requirements pinned | jsonschema/openpyxl pinned | `jsonschema==4.25.0`, `openpyxl==3.1.5`, numpy/pandas; CPython 3.13.9 | PASS | `requirements.txt` (hash matches manifest) |
| Verifier `--pre-freeze` | PASS | PASS (exit 0) | PASS | authoritative run |
| Verifier post-gen pre-generation | fail-closed | FAIL (missing attempt log, exit 1) | PASS (correct) | authoritative run |
| Pre-freeze unittest | all pass | 19 tests OK (exit 0) | PASS | authoritative run |

---

## 3. READ-ONLY COMMANDS EXECUTED

Git (device):
```
git rev-parse --show-toplevel
git rev-parse HEAD
git rev-parse --abbrev-ref HEAD
git rev-parse "exp3-heldout-frozen^{commit}"
git tag -l 'exp3*'
git status --short
```
Reads/parsing/hashing (device, `PYTHONDONTWRITEBYTECODE=1`):
```
cat phase_b/exp3/EXP3_FREEZE_MANIFEST.json
python3  # JSON parse + SHA-256 of all 12 manifest artifacts
python3  # exp3_case_plan.json full invariant checks
python3  # attempt-log schema/template + manifest template checks
python3  # PHASE_B_PROTOCOL_HASHES.json -> recompute 56 Exp1 hashes
python3  # isolated simulator 4-hash check vs case plan
grep -nE (protocol critical strings; forbidden terminology)
sed -n / cat -n phase_b/exp3/generate_exp3_heldout.m   # signature, gates, RNG/sim, error handling
find … -name '*.xlsx' ; test -e tep_exp3_heldout ; cat requirements.txt
python3 phase_b/exp3/verify_exp3_heldout.py --pre-freeze   # (device: ImportError — see note)
python3 -m unittest phase_b.tests.test_exp3_pre_freeze     # (device: ImportError — see note)
```
Authoritative execution (isolated copy of the frozen artifacts, pinned deps `jsonschema==4.25.0`,
`openpyxl==3.1.5`; no writes into the project):
```
python3 phase_b/exp3/verify_exp3_heldout.py --pre-freeze
python3 phase_b/exp3/verify_exp3_heldout.py           # expected fail-closed pre-generation
python3 phase_b/tests/test_exp3_pre_freeze.py -v
```

Environment note (not a blocker): the device **system** interpreter is CPython 3.10 with
`jsonschema 3.2.0`, so the verifier/tests raise `ImportError: cannot import name
'Draft202012Validator'` there. This is by design — `requirements.txt` pins the reference runtime
(CPython 3.13.9, `jsonschema==4.25.0`); the verifier/tests must be run in that venv
(`pip install -r requirements.txt`). It does not affect MATLAB generation of the first run.

---

## 4. ESSENTIAL VERIFIER / TEST OUTPUT (non-paraphrased)

Freeze-manifest artifact hashing (12/12):
```
PASS  .gitignore
PASS  requirements.txt
PASS  phase_b/exp3/EXP3_FRESH_RUN_PROTOCOL.md
PASS  phase_b/exp3/RNG_RUNTIME_VALIDATION.md
PASS  phase_b/exp3/exp3_attempt_log.schema.json
PASS  phase_b/exp3/exp3_attempt_log.template.json
PASS  phase_b/exp3/exp3_case_plan.json
PASS  phase_b/exp3/exp3_manifest_template.csv
PASS  phase_b/exp3/generate_exp3_heldout.m
PASS  phase_b/exp3/validate_exp3_rng_runtime.m
PASS  phase_b/exp3/verify_exp3_heldout.py
PASS  phase_b/tests/test_exp3_pre_freeze.py
ARTIFACTS: 12 total; failures/missing = 0
```
Experiment 1 immutability:
```
Exp1 frozen artifacts checked=56; failures=0
```
Isolated simulator vs case plan:
```
PASS  MultiLoop_mode1.mdl
PASS  Mode1xInitial.mat
PASS  temexd_mod.c
PASS  temexd_mod.mexmaca64
```
Verifier (pinned env):
```
PASS: Experiment 3 pre-freeze infrastructure verification succeeded.        (exit 0)
FAIL: [Errno 2] No such file or directory: '.../tep_exp3_heldout/exp3_attempt_log.json'  (exit 1, expected pre-generation)
```
Pre-freeze unittest (pinned env):
```
test_all_experiment_one_frozen_hashes_remain_exact ... ok
test_attempt_policy_is_only_zero_then_optional_one ... ok
test_attempt_schema_has_only_technical_provenance ... ok
test_attempt_two_is_rejected_fail_closed ... ok
test_case_ids_and_seed_namespaces_are_unique ... ok
test_case_plan_is_exactly_canonical_and_deterministic ... ok
test_empty_attempt_and_manifest_templates_are_exact ... ok
test_exp3_python_dependencies_are_pinned ... ok
test_exp3_raw_output_is_ignored_and_not_generated ... ok
test_freeze_manifest_hashes_all_exp3_boundary_artifacts ... ok
test_generation_requires_frozen_plan_and_hash_manifest ... ok
test_generation_rng_and_sim_are_adjacent ... ok
test_generator_contains_no_scientific_selection_pipeline ... ok
test_mutated_case_plan_is_rejected_fail_closed ... ok
test_protocol_code_and_config_agree ... ok
test_replacement_requires_failed_attempt_zero ... ok
test_runtime_rng_evidence_is_exact_and_sentinel_only ... ok
test_seed_or_provenance_deviation_is_rejected ... ok
test_structural_values_are_enforced_on_valid_attempts ... ok
Ran 19 tests ... OK        (exit 0)
```
(An earlier sandbox run showed 3 non-passes solely because `requirements.txt` had not been copied
into the isolated tree; on the live repo it is present and hash-matches, and after copying it the
suite is fully green as above.)

---

## 5. BLOCKERS

**None.**

Operational notes (not blockers, no action required to start the first run):
- Run the Python verifier/tests in the pinned reference venv (CPython 3.13.9 + `requirements.txt`);
  the device's system Python cannot import the verifier (`jsonschema 3.2.0`). This matters only for
  the **post-generation** verification step, not for MATLAB generation.
- Untracked files in the tree (`2604.16778v2.pdf`, `EXP3_PREFREEZE_AUDIT_REPORT.md`, two `docs/…`)
  are outside the freeze and irrelevant to generation; leave them as-is.

---

## 6. GENERATOR INVOCATION CONTRACT (derived from `phase_b/exp3/generate_exp3_heldout.m`)

- **Kind:** MATLAB **function**, `record = generate_exp3_heldout(physicalCaseId, attempt, varargin)` (L1).
- **Required args:**
  - `physicalCaseId` (char/string) — must match exactly one of the 30 planned IDs (L13, L48).
  - `attempt` (numeric scalar) — must be `0` or `1` (L14). `0`=primary seed, `1`=replacement seed
    (L52–56).
- **Optional name–value params** (defaults resolve to repo-standard paths):
  - `CasePlanPath` → `phase_b/exp3/exp3_case_plan.json` (L15, L28–29)
  - `FreezeManifestPath` → `phase_b/exp3/EXP3_FREEZE_MANIFEST.json` (L16, L30–31)
  - `OutputDir` → `<repoRoot>/tep_exp3_heldout/mode1` (L17, L32–33)
  - `AttemptLogPath` → `<repoRoot>/tep_exp3_heldout/exp3_attempt_log.json` (L18, L34–35)
  - `SimulatorDir` → `<repoRoot>/tep_parent_a0413e16/simulator` (L19, L36–37)
- **Directory creation:** output dir auto-created if missing (L61–63). Refuses to overwrite an
  existing output file (L66–67, `EXP3:RefuseOverwrite`).
- **Pre-simulation gates (fail-closed):** case-plan `status==FROZEN_BEFORE_GENERATION` (L40→L249);
  freeze-manifest `status`/`hash_algorithm`/`freeze_tag` (L41–47); attempt-allowed incl.
  replacement-only-after-technical-failure and ≤2 attempts (L59→L338–363); pinned hash checks of
  model/initial-state/S-function source/MEX (L69–85); **self-hash of the generator and case-plan
  hash checked against the freeze manifest** (L87–96); runtime identity match (L97–98); model
  parameter asserts (mode/solver/start/stop/initial-state/callbacks/S-function identity+params).
- **Fault/seed selection:** condition read from the case entry; `dist=zeros(1,28)`, `dist(k)=1` for
  `F{1,8,10,13}` (L160–166); seed from case entry per attempt.
- **RNG/sim order (protocol-critical):** `rng(seed,'twister')` (L169) is the last statement before
  `sim(modelName)` (L170); nothing random-relevant between them (L168 comment); `dist` assigned
  before `rng` (L166).
- **Post-simulation:** structural checks only via `inspect_numeric_output` (rows=3001, cols=54,
  finite, time 0→50, strictly increasing, constant 1/60 h) (L188–191); no diagnostic/feature/LLM
  step anywhere.
- **Output:** one workbook `<physical_case_id>__attempt-<attempt>.xlsx`, `Sheet1`, header
  `Time (h)`,`XMEAS-1..41`,`XMV-1..12` (L64, L193–198); write is round-trip verified (L200).
- **Logging:** append-only attempt log; success appends a record with `structural_valid=true` and
  empty failure reason (L203–214); **on any error** it appends a record with a non-empty
  `technical_failure_reason` and then rethrows (L215–226) — failures are never silently dropped.
- **Working directory / path:** the function manages cwd internally (adds `SimulatorDir` to path and
  `cd`s into it, restoring on cleanup). To be callable, `phase_b/exp3` must be on the MATLAB path
  (or be the current folder).
- **Manual operator steps:** launch MATLAB `R2025b` Update 6 on macOS (`MACA64`); ensure the
  isolated simulator dir (`tep_parent_a0413e16/simulator`) is present (verified); put `phase_b/exp3`
  on the path; call the function. No other setup.
- **Console output on success:** the function returns the provenance `record` struct (MATLAB echoes
  it if the call is not semicolon-terminated); authoritative success is the appended attempt-log
  record (`structural_valid=true`) plus the written workbook. There is no separate "success" banner.

---

## 7. RECOMMENDED SINGLE MATLAB COMMAND — `EXP3-N-001`, attempt 0  **[NOT EXECUTED]**

From the repository root, with the Experiment 3 folder on the MATLAB path (defaults resolve the
case plan, freeze manifest, simulator, output dir, and attempt log):

```matlab
% >>> NOT EXECUTED BY THIS AUDIT — provided for the operator only <<<
addpath(fullfile(pwd,'phase_b','exp3'));
record = generate_exp3_heldout('EXP3-N-001', 0);
```

This uses `primary_seed = 310001`, writes
`tep_exp3_heldout/mode1/EXP3-N-001__attempt-0.xlsx`, and appends one record to
`tep_exp3_heldout/exp3_attempt_log.json`. **Do not run it as part of any audit.**

---

## 8. OPERATIONS NOT PERFORMED

No simulation (`sim`) or model execution; no workbook created; no attempt log or manifest
initialized/populated; no verbalization, feature extraction, plotting, signal statistics, LLM
inference, or scientific evaluation; no inspection of any Exp3 workbook content (none exist); no
file modified, created, deleted, renamed, or reformatted in the project; no `git checkout/switch/
reset/clean/commit/stash/tag`; no change to untracked files; the RNG sentinel probe was **not**
re-run. All executed operations were reads, hashes, JSON/CSV parsing, and the read-only pre-freeze
verifier/tests (plus one expected fail-closed probe) in an isolated copy with bytecode writing
disabled.

---

*Read-only audit. HEAD = tag `exp3-heldout-frozen` = `b02e93f92bf6fa85a4fd0a2e010bac365a3a7c89`.
Experiment 1 immutable (`45ec4ee`; 56/56). Verdict: READY FOR FIRST PHYSICAL RUN.*
