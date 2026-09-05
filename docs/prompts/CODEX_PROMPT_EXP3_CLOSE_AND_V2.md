You are a senior scientific-software engineer working in the local Git repository `/Users/luker/fot-tep`
(GitHub `sorrentinoluca/fot-phd`, branch `main`). You will (A) formally CLOSE the exhausted
Experiment 3 while preserving all its provenance, and (B) build a new, cleanly separated
**Experiment 3 V2** prospective fresh-run held-out that fixes every failure mode observed in EXP3 and
adds the end-to-end validation gate that was missing. You MUST stop at a frozen, sentinel-validated
state and MUST NOT generate the real scientific runs until a human explicitly authorizes it.

====================================================================
ABSOLUTE, NON-NEGOTIABLE CONSTRAINTS
====================================================================
1. Do NOT modify, rewrite, delete, move, or re-tag ANY of these (they are immutable history):
   - Experiment 1 frozen artifacts (all 56 paths in `phase_b/PHASE_B_PROTOCOL_HASHES.json`).
   - The EXP3 freeze commit `b02e93f92bf6fa85a4fd0a2e010bac365a3a7c89` and tag `exp3-heldout-frozen`.
   - Hotfix commits/tags: h1 `cdba0202435d1c97ea79cfff586e59534ce9baad`; h2 `28130023a34eda778c04a001a9f631404bd6b9a6` (tag `exp3-post-freeze-hotfix-002`); h3 `0d869720e6ac4d1b396b3b9d731463324d296e26` (tag `exp3-post-freeze-hotfix-003`); h4 `1cad481839475afaa6ad784bba25c1c45bb260ed` (tag `exp3-post-freeze-hotfix-004`, current HEAD).
   - The existing EXP3 attempt log `tep_exp3_heldout/exp3_attempt_log.json` (SHA-256
     `04ea7d8af227c3a7f947b4dde434e77510c163ce9c108892ffa22f491f022904`) and its two failure records.
     Treat it as read-only evidence; never edit or delete it.
2. Do NOT change any EXP3 scientific parameter anywhere. EXP3_V2 is a *harness/provenance* correction
   plus a fresh seed allocation, NOT a redesign of the science.
3. Do NOT run `sim`, do NOT run the real generator on any EXP3_V2 primary/replacement seed, do NOT
   create any real held-out workbook, do NOT inspect any scientific signal, and do NOT open EXP3
   workbooks (none exist). The ONLY simulation you may run is the sentinel integration gate (Part B,
   step 7) with a non-experiment seed, writing to a throwaway directory.
4. Everything that will be frozen must be pre-specified BEFORE any experiment run. No content-based /
   outcome-based decisions. Keep the representation diagnosis-neutral.
5. Do not weaken any existing fail-closed check. Add tests; never delete safety tests.
6. Work on a new branch; do NOT force-push; do NOT delete tags. Ask for human approval before the
   freeze commit/tag and before any real generation.

====================================================================
BACKGROUND: WHY EXP3 IS BEING CLOSED (read the audits under `docs/audits/`)
====================================================================
Read, do not modify: `docs/audits/EXP3_PREFREEZE_AUDIT_REPORT.md`,
`docs/audits/EXP3_FIRST_RUN_READINESS_AUDIT.md`, `docs/audits/EXP3_HOTFIX_001_MICROAUDIT.md`,
`docs/audits/EXP3_HOTFIX_002_MICROAUDIT.md`, `docs/audits/EXP3_HOTFIX_003_MICROAUDIT.md`,
`docs/audits/EXP3_ATTEMPT_EXHAUSTION_AUDIT.md`, plus `phase_b/exp3/EXP3_FRESH_RUN_PROTOCOL.md` and every
`phase_b/exp3/*` artifact and test.

EXP3 is EXHAUSTED for its first case: `EXP3-N-001` consumed both permitted attempts as documented
technical failures, produced zero workbooks, and per protocol §9.2 (max two attempts; "no alternative
seed or extra recovery run may be chosen without a new audited protocol version created before further
generation") cannot continue. No scientific signal was ever observed. Five serial software/technical
failures occurred, each fixed by a hotfix except the last:

| # | Stage | Error | Fixed by | Lesson → EXP3_V2 requirement |
|---|---|---|---|---|
| 1 | before sim | `Unrecognized field name "attempt"` (empty untyped `struct([])`) | h1 | Carry forward the TYPED empty attempt-log state. |
| 2 | before sim | `MATLAB product date mismatch` (`ver('MATLAB').Date` vs `version('-date')`) | h2 | Carry forward the 5-field runtime semantics. |
| 3 | during sim StopFcn | `Simulink:Engine:CallbackEvalErr` (`StopFcn=TEplot` reads base `tout`) | h3 | Carry forward guaranteed StopFcn suppress/restore. |
| 4 | before sim | `Unrecognized field name "frozen_original_generator_sha256"` (manifest contract) | h4 | Keep generator↔manifest field contract test. |
| 5 | AFTER sim returned | `MATLAB:structRefFromNonStruct` on `simResult.who` | **NOT YET FIXED** | Fix output retrieval (below) + END-TO-END SENTINEL GATE. |

Systemic root cause: pre-freeze validation exercised RNG plumbing and runtime identity with sentinels
but NEVER ran the full generator path (sim → output marshalling → workbook write → verifier). EXP3_V2
MUST make that end-to-end sentinel run a mandatory gate before any real seed is consumed.

Incident-5 technical root cause (verified from the model file, do not take on faith — re-verify):
`tep_parent_a0413e16/simulator/MultiLoop_mode1.mdl` (SHA-256
`d2f6659f65935021d4b1813e7189be02e7ae9f5639b794e8edc4f2f3c5cddba8`) has `ReturnWorkspaceOutputs=off`,
`SaveOutput=off`, `SaveTime=off`, `SaveState=off`, `TimeSaveName=tout`, `OutputSaveName=yout`,
`StopFcn=TEplot`, `PreLoadFcn=Mode_1_Init`, `LoadInitialState=on`, `InitialState=xInitial`. Under this
legacy config, `simResult = sim(modelName)` (single output) returns a numeric array (the time vector),
NOT a `Simulink.SimulationOutput`, so `simResult.who` throws. The frozen `EXP3` generator
(`phase_b/exp3/generate_exp3_heldout.m`) already contains a base-workspace fallback (`evalin('base', …)`)
but never reaches it because `.who` is called first.

====================================================================
FROZEN SCIENTIFIC INVARIANTS — EXP3_V2 MUST PRESERVE EXACTLY
====================================================================
- Sample: 30 physical runs = 6 Normal + 6 F1 + 6 F8 + 6 F10 + 6 F13 (same four fault classes).
- Fault mapping: `dist=zeros(1,28)`; F1→dist(1), F8→dist(8), F10→dist(10), F13→dist(13); Normal→all zero.
- Simulator: commit `a0413e16c940f0fc8b554d6a86248020d7fb7527`, model `MultiLoop_mode1`, Mode 1,
  simulation mode `normal`, solver `ode45`, horizon 0–50 h, sampling `1/60` h, fault injection 10 h,
  initial state `Mode1xInitial.mat`, S-function `temexd_mod`. Pin and check all four hashes
  (model `d2f6659f…`, initial-state `40eaebc9…`, S-func source `0da41d93…`, S-func mex `68f63238…`).
- Output contract: one worksheet `Sheet1`, 3001 numeric rows × 54 columns, header
  `Time (h)`, `XMEAS-1..41`, `XMV-1..12`, strictly increasing time 0→50, constant 1/60 h.
- RNG: MATLAB `twister`; `rng(seed,'twister')` MUST be the last random-relevant statement immediately
  before `sim`, with nothing random-relevant between them.
- Replacement policy: attempt 0 = primary seed; attempt 1 = replacement seed = primary + 1,000,000,
  allowed ONLY after a logged attempt-0 technical failure; MAX 2 attempts; no attempt 2; append-only
  log; refuse-overwrite; NO content/outcome-based replacement.
- Runtime identity to assert (5-field semantics): `matlab_version_full=version` (`25.2.0.3312555 (R2025b) Update 6`);
  `matlab_release=version('-release')` (`2025b`); `matlab_build`=parsed from `version` (`3312555`);
  `matlab_product_date=ver('MATLAB').Date` (`28-Jul-2025`); `matlab_runtime_update_date=version('-date')`
  (`June 30, 2026`); Simulink `25.2` `(R2025b)` `28-Jul-2025`; architecture `MACA64`;
  matlabroot `/Applications/MATLAB_R2025b.app`.
- Statistics: independent unit = physical run; agent-case observations NOT independent; paired cluster
  bootstrap stratified by true fault, 10,000 draws; primary analysis = EXP3_V2-only; primary contrast
  B−A; supporting semantic-specificity contrast B−E; any EXP1/EXP3_V2 pooling is secondary-descriptive only.
- Terminology: "pre-specified" (never "preregistered"); "prospective fresh-run replication on the same
  four fault classes"; not generalization/robustness/cross-domain/PV.

====================================================================
PART A — CLOSE EXPERIMENT 3 (provenance only; no history rewrite)
====================================================================
A1. Create `phase_b/exp3/EXP3_CLOSURE.md` and `phase_b/exp3/EXP3_CLOSURE.json` recording:
    - status `CLOSED_INCOMPLETE_ATTEMPTS_EXHAUSTED`;
    - the freeze commit/tag and the four hotfix commits/tags (verify each with `git rev-parse <tag>^{}`);
    - the five-incident timeline (table above);
    - the exhaustion basis (protocol §9.2), and that 0 of 30 cases completed and no scientific output
      was produced/observed;
    - the archived evidence of the two failure records: copy the current
      `tep_exp3_heldout/exp3_attempt_log.json` verbatim into a committed file
      `phase_b/exp3/EXP3_CLOSURE_attempt_log_archive.json` and record its SHA-256
      (`04ea7d8af227c3a7f947b4dde434e77510c163ce9c108892ffa22f491f022904`) in the JSON. (The live log
      is git-ignored; this archive makes the failures permanent, version-controlled evidence.)
    - an explicit statement that EXP3_V2 supersedes EXP3 and that EXP3's tags/commits remain immutable.
A2. Do NOT modify `phase_b/exp3/*` frozen artifacts, `tep_exp3_heldout/`, or any tag. The closure files
    are new additions only.

====================================================================
PART B — BUILD EXPERIMENT 3 V2 (new, isolated, pre-specified, frozen)
====================================================================
Create everything under a NEW directory `phase_b/exp3_v2/` (leave `phase_b/exp3/` untouched) and a NEW
git-ignored raw output directory `tep_exp3_v2_heldout/` (add to `.gitignore`). Reuse EXP3 logic by
copying-then-adapting; do not import from the frozen EXP3 files at runtime.

B1. Machine-readable case plan `phase_b/exp3_v2/exp3v2_case_plan.json`:
    - 30 cases, canonical order Normal, F1, F8, F10, F13 (6 each), run_index 1..6.
    - Physical IDs `EXP3V2-N-00{1..6}`, `EXP3V2-F1-00{1..6}`, `EXP3V2-F8-…`, `EXP3V2-F10-…`,
      `EXP3V2-F13-…` (distinct from EXP3 `EXP3-*` and Experiment 1 `PBH-*`).
    - FRESH seed namespace, disjoint from EXP3's 310000 namespace and from the sentinels 987654321 /
      123456789: master allocation base `320000`; primary seeds `320001..320030` (base + canonical
      ordinal); replacement seeds = primary + 1,000,000 (`1320001..1320030`); bootstrap seed `320031`
      (never a run seed). rng algorithm `twister`; allowed attempts [0,1]; max_total_attempts 2.
      Document WHY seeds are freshly allocated: the EXP3 seeds 310001/1310001 were consumed by failed,
      unobserved runs; fresh seeds remove any appearance of re-rolling while preserving determinism.
    - Same `simulator`, `runtime` (5-field), `statistics` blocks and output contract as EXP3
      (see invariants above), with `status` field starting at `PRE_FREEZE_DRAFT`.

B2. Protocol `phase_b/exp3_v2/EXP3_V2_FRESH_RUN_PROTOCOL.md`:
    - State it is a NEW pre-specified prospective fresh-run replication superseding EXP3; same four
      fault classes; same scientific invariants; fresh seed namespace; harness corrections only.
    - Reproduce the frozen invariants, the replacement policy (§9-equivalent), the prospective data
      boundary (generate → mechanical structural checks only → freeze held-out → verbalize → A/B/E
      inference), the statistical plan, and the success/failure criteria (B−A>0 with clustered
      bootstrap 95% CI lower bound >0 as primary; B−E>0 supporting).
    - Add a dedicated section documenting the incident-5 fix and the mandatory sentinel gate (below).
    - Provide a freeze checklist ending with items that remain `[ ]` until the human audit + freeze.

B3. Generator `phase_b/exp3_v2/generate_exp3v2_heldout.m` = the EXP4/h4 EXP3 generator logic
    (`phase_b/exp3/generate_exp3_heldout.m`) carried forward WITH ALL prior fixes, PLUS the incident-5
    output-retrieval fix. Requirements:
    - Keep: typed empty attempt-log state (h1); 5-field runtime capture + assert (h2); StopFcn
      suppress/restore via helpers with guaranteed onCleanup restoration, no `save_system`, Dirty
      restore, exact-`TEplot`-only acceptance (h3); complete hotfix/manifest field contract (h4);
      pinned model/initial-state/S-func(source+mex) hash checks; case-plan `status` gate
      (`FROZEN_BEFORE_GENERATION` required to run); self-hash + case-plan-hash binding against the V2
      freeze manifest; refuse-overwrite; append-only attempt log; structural-checks-only; no verbalizer/
      LLM/metrics.
    - FIX incident 5 — robust output retrieval that does NOT assume a `Simulink.SimulationOutput`.
      Implement ONE of the following, chosen and DOCUMENTED, and validated by the sentinel gate:
        (Preferred) Temporarily set `ReturnWorkspaceOutputs='on'` (and, if needed, a single simulation
        output) via `set_param` BEFORE `rng`/`sim`, guaranteeing restoration exactly like StopFcn
        (onCleanup + no `save_system` + Dirty restored + model file byte-identical), so `simResult`
        is a `Simulink.SimulationOutput` and `[tout,simout,xmv]` are obtained via its accessors; OR
        (Alternative) Keep model config untouched and read `tout`/`simout`/`xmv` directly from the base
        workspace with `isa(simResult,'Simulink.SimulationOutput')` guarding any object accessor, i.e.
        promote the existing base-workspace fallback to the primary path.
      Either way: it is a NON-SCIENTIFIC output-marshalling change; it MUST NOT alter dynamics, dist,
      seed, solver, injection, or the `rng(seed,'twister')`→`sim` adjacency; and it MUST produce the
      exact 3001×54 contract. Do NOT rely on the failing `simResult.who` pattern.
    - Any config toggled via `set_param` (StopFcn and, if used, ReturnWorkspaceOutputs) must be part of
      a single guaranteed-restore mechanism, verified after the run, and the model `.mdl` file must be
      byte-identical (`d2f6659f…`) before and after.

B4. Callback/config helpers under `phase_b/exp3_v2/`: reuse the h3 pattern
    (`suppress_/restore_exp3_plot_stopfcn.m` equivalents). If you toggle `ReturnWorkspaceOutputs`, add
    analogous `suppress_/restore` helpers with the same guaranteed-restore + no-save + Dirty-restore +
    exact-original-value discipline (refuse if the original value is unexpected).

B5. Attempt-log schema/template `phase_b/exp3_v2/exp3v2_attempt_log.schema.json` and
    `…template.json`: same technical-provenance-only fields as EXP3 (5-field runtime; no diagnostic
    fields), IDs restricted to the `EXP3V2-*` pattern, attempt ∈ {0,1}, empty `attempts` array in the
    template. NOTE: fix the EXP3 quirk where a single record serialized as a JSON object — ensure
    `append_attempt_record` always emits `attempts` as an ARRAY even for one record.

B6. Manifest template `phase_b/exp3_v2/exp3v2_manifest_template.csv`: 30 rows, IDs in canonical order,
    primary seeds populated, all output-dependent fields `TBD`.

B7. Verifier `phase_b/exp3_v2/verify_exp3v2_heldout.py`: carry forward the EXP3 verifier’s fail-closed
    checks (case-plan canonical/deterministic; seed namespaces unique & disjoint; runtime field-set +
    5-field semantics; simulator identity; attempt policy incl. replacement-requires-technical-failure
    and attempt≤1; structural output checks; manifest/attempt-log/data-dir consistency; pre-freeze mode
    that reads no workbook; post-generation mode that refuses unless case-plan status is FROZEN). Add:
    a check that the generator’s `hotfixManifest.*`/manifest field references all exist (h4 lesson);
    a check binding the V2 freeze manifest; and a check that the frozen EXP3 tags/commits and the
    Experiment 1 hashes are still intact (must remain 56/56). Provide a `--pre-freeze` mode.

B8. Freeze manifest `phase_b/exp3_v2/EXP3_V2_FREEZE_MANIFEST.json`: list every V2 boundary artifact with
    SHA-256, `status=FROZEN_BEFORE_GENERATION` (set only at the freeze step), `freeze_tag`
    `exp3-v2-heldout-frozen`, `created_before_generation=true`, `v2_workbooks_at_freeze=0`,
    `supersedes` = the EXP3 freeze + hotfix chain (by commit/tag), and the `EXP3_CLOSURE` reference.

B9. Tests (MATLAB + Python) under `phase_b/exp3_v2/` and `phase_b/tests/`:
    - Reuse/adapt all EXP3 pre-freeze tests (case-plan canonical; seeds unique/disjoint incl. disjoint
      from EXP3’s 310000 and from sentinels; attempt policy 0/1, reject attempt 2, replacement requires
      technical failure; rng↔sim adjacency; generator contains no verbalizer/LLM/accuracy; StopFcn
      fail-closed + never-calls-sim; runtime 5-field accept + per-field reject; templates exact; empty
      log typed; manifest/verifier fail-closed; Experiment 1 56/56 intact; freeze-manifest hashes).
    - ADD a regression test asserting the NEW output-retrieval path does not use the failing
      `simResult.who`-on-non-object pattern and that, in the sentinel run, `[tout,simout,xmv]` are
      obtained and shaped 3001×54.
    - ADD the generator↔manifest field-contract test (every `hotfixManifest.<field>` referenced by the
      generator exists in the manifest JSON).
    - ADD a test asserting `append_attempt_record` yields an ARRAY-typed `attempts` for one record.
    - Run with `PYTHONDONTWRITEBYTECODE=1` and pytest cache disabled; keep MATLAB Code Analyzer clean;
      run Black + Ruff; `git diff --check`. Pin `jsonschema==4.25.0`, `openpyxl==3.1.5` (repo
      `requirements.txt`; reference runtime CPython 3.13.9). Python verifier/tests require a git checkout
      where tags/commits are reachable.

B10. MANDATORY SENTINEL INTEGRATION GATE (the missing end-to-end validation) —
     `phase_b/exp3_v2/sentinel_integration_run.m` (or documented equivalent):
     - Uses a NON-experiment sentinel seed (e.g. `987654321`, already outside all allocations); assert
       it is not in the V2 primary/replacement ranges.
     - Executes the ACTUAL `generate_exp3v2_heldout` code path end-to-end: config asserts → callback/
       output-config suppression → `rng`→`sim` → output retrieval → structural checks → workbook WRITE →
       `verify_written_workbook`/verifier — writing to a THROWAWAY directory (e.g. `/tmp/…`, never
       `tep_exp3_v2_heldout/`).
     - Must produce a valid 3001×54 `Sheet1` workbook that PASSES `verify_exp3v2_heldout.py`; must
       restore `StopFcn=TEplot` (and `ReturnWorkspaceOutputs` if toggled); must leave `MultiLoop_mode1.mdl`
       byte-identical (`d2f6659f…`); must confirm `rng`→`sim` adjacency; must NOT touch the real
       attempt log or the real output dir.
     - Record the sentinel evidence (hashes, shapes, pass/fail) in a committed
       `phase_b/exp3_v2/EXP3_V2_SENTINEL_EVIDENCE.md`. This gate MUST pass BEFORE any real EXP3_V2 seed
       is ever consumed. Running this sentinel is the ONLY simulation you are permitted to run.

====================================================================
FREEZE PROCEDURE (stop here; await human authorization)
====================================================================
F1. Implement Parts A and B on a new branch. Do not set the case-plan/manifest status to
    `FROZEN_BEFORE_GENERATION` until F3.
F2. Run: all MATLAB tests, all Python tests, the verifier `--pre-freeze`, Black, Ruff, `git diff --check`,
    the Experiment 1 56/56 hash regression, and the sentinel integration gate (B10). Fix any failure.
    Report all results.
F3. Only after the human reviews and approves: flip `status` to `FROZEN_BEFORE_GENERATION` in the case
    plan and freeze manifest, pin all V2 artifact SHA-256s, commit, and create tag
    `exp3-v2-heldout-frozen`. Also commit Part A (closure) — separately or in the same series, clearly
    messaged. Use the repo’s attribution trailers for commits.
F4. DO NOT generate the 30 real EXP3_V2 runs. After the freeze + green sentinel gate, STOP and report
    that EXP3_V2 is frozen and sentinel-validated and awaits explicit human authorization to run
    attempt 0 for `EXP3V2-N-001` (primary seed 320001). Do not run it.

====================================================================
DEFINITION OF DONE (report against every item)
====================================================================
- EXP3 closed with permanent, version-controlled evidence of its two failures; no EXP3/EXP1/hotfix
  history or tags modified; Experiment 1 still 56/56.
- EXP3_V2 exists fully under `phase_b/exp3_v2/` + git-ignored `tep_exp3_v2_heldout/`, with fresh seed
  namespace (320001–320030 / 1320001–1320030 / bootstrap 320031), all scientific invariants preserved,
  the incident-5 output-retrieval fix in place, and the JSON-array attempt-log fix.
- The mandatory end-to-end sentinel gate is implemented and PASSES (evidence committed); model file
  byte-identical; StopFcn/ReturnWorkspaceOutputs restored; rng→sim adjacency preserved.
- All tests/linters/verifier green in the pinned environment; report the exact outputs.
- EXP3_V2 is frozen (tag `exp3-v2-heldout-frozen`) and STOPPED before real generation, awaiting
  human authorization.
Provide a concise final report: what changed, the new hashes/tag, test/sentinel results, and the exact
(NOT executed) command that a human would later run to start `EXP3V2-N-001` attempt 0. Ask before doing
anything outside this scope.
