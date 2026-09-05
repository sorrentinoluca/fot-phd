# Experiment 3 — Attempt-Exhaustion Audit (EXP3-N-001), read-only

Independent technical + scientific/governance audit after both permitted attempts of the first
physical case failed. Repository `/Users/luker/fot-tep`. Date 2026-09-03 (UTC). Read-only: no `sim`,
no generator run, no attempt re-run, no attempt 2, no workbook, no signal inspection, no file/commit/
tag change. Legend per finding: **[OBS]** observed fact · **[INF]** inference · **[REC]** recommendation ·
confidence H/M/L.

---

## 1. OVERALL VERDICT

> ## ⛔ BLOCKED — ATTEMPTS EXHAUSTED

Both permitted attempts for `EXP3-N-001` are consumed as documented technical failures (attempt 0
seed 310001; attempt 1 seed 1310001), no workbook exists, and the frozen protocol's two-attempt limit
(§9.2) is reached. Under the **current** frozen protocol, `EXP3-N-001` is `technically_failed`/missing
and generation may **not** continue for this case without a **new audited protocol version created
before any further simulation** (protocol §9.2, lines 442–445). A generator hotfix alone cannot
rescue it: there is no remaining attempt slot to apply it to. **[OBS/H]**

Mitigating fact for any future recovery decision: **no Exp3 scientific signal was ever observed** —
all five failures were software/technical (empty-log field access, MATLAB-date semantics, plotting
`StopFcn`, manifest contract, output marshalling), none related to any fault trajectory. **[OBS/H]**
Whether to authorize a recovery is a **scientific-governance decision requiring a new audit/freeze**;
it is **not** authorized by the current protocol (see §12–14). This report does not authorize it.

---

## 2. AUDIT SCOPE AND READ-ONLY GUARANTEE

Verified only through: `git` read commands (`rev-parse`, `log`, `cat-file`, `merge-base`,
`check-ignore`, `ls-files`), `cat`/`grep`/`sed` reads, SHA-256 hashing, and JSON parsing with
`PYTHONDONTWRITEBYTECODE=1`. No `sim`, no `generate_exp3_heldout`, no attempt re-run/creation, no
workbook, no plotting, no signal inspection, no edit/commit/tag/push/reset/checkout/clean. No
scientific trajectory was used as a decision criterion (none exists to use). **[OBS/H]**

## 3. GIT / FREEZE / HOTFIX CHAIN

**[OBS/H]** HEAD = `1cad481839475afaa6ad784bba25c1c45bb260ed` ("Complete Exp3 hotfix manifest
contract"). Freeze is an ancestor of HEAD; linear chain:

| Stage | Commit | Tag | Verified |
|---|---|---|---|
| Original freeze | `b02e93f9…a7c89` | `exp3-heldout-frozen` | tag^{} = commit ✓ |
| Hotfix 001 | `cdba0202…9baad` | — | commit present ✓ |
| Hotfix 002 | `28130023…6b9a6` | `exp3-post-freeze-hotfix-002` | tag^{} = commit ✓ |
| Hotfix 003 | `0d869720…296e26` | `exp3-post-freeze-hotfix-003` | tag^{} = commit ✓ |
| Hotfix 004 | `1cad4818…b260ed` (= HEAD) | `exp3-post-freeze-hotfix-004` | tag^{} = commit ✓ |

Ancestry `b02e93f..HEAD` = h1→h2→h3→h4, in order. Working tree: **no tracked modifications** (only
untracked PDFs/prior audit reports/docs). Experiment 1: **56/56 frozen artifacts intact** (recomputed
vs `PHASE_B_PROTOCOL_HASHES.json`). **[OBS/H]**

## 4. INCIDENT TIMELINE (five serial software/technical failures, one case)

**[OBS/H]** all confirmed against code/log/config; incidents 1,2,4 reconstructed from the user brief +
git history (the pre-attempt failures left no persistent log), incidents 3,5 confirmed in the on-disk
attempt log.

| # | Stage reached | Error | Fix | Attempt consumed? |
|---|---|---|---|---|
| 1 | before `sim` | `Unrecognized field name "attempt"` (empty untyped `struct([])`) | hotfix 001 (`cdba020`) | No (nothing logged) |
| 2 | before `sim` | `MATLAB product date mismatch` (`ver('MATLAB').Date` vs `version('-date')`) | hotfix 002 (`2813002`) | No |
| 3 | during `sim` StopFcn | `Simulink:Engine:CallbackEvalErr` — `StopFcn=TEplot`, `tout` undefined | hotfix 003 (`0d86972`) | **Yes — attempt 0, seed 310001** |
| 4 | before `sim` | `Unrecognized field name "frozen_original_generator_sha256"` (manifest contract) | hotfix 004 (`1cad481`) | No |
| 5 | after `sim` returned | `MATLAB:structRefFromNonStruct` — `simResult.who` on a non-struct | *(uncommitted / none yet)* | **Yes — attempt 1, seed 1310001** |

Both attempt-consuming failures (3, 5) reached or completed `sim`; incidents 1, 2, 4 failed before
`sim` and consumed nothing.

## 5. ATTEMPT-LOG INTEGRITY

**[OBS/H]** `tep_exp3_heldout/exp3_attempt_log.json` (sha256 `04ea7d8af227…f022904`) contains exactly
**2** records, both `EXP3-N-001`:

- attempt `0`, seed `310001`, `structural_valid=false`, reason `Simulink:Engine:CallbackEvalErr … 'TEplot'`,
  `output_size_bytes=0`, generator hash `f1cf1647` (hotfix-002 generator).
- attempt `1`, seed `1310001` (serialized `1.310001E+6`), `structural_valid=false`, reason
  `MATLAB:structRefFromNonStruct: Dot indexing is not supported…`, `output_size_bytes=0`, generator
  hash `da419e5d` (hotfix-003 generator, current at HEAD).

Both records satisfy the frozen definitions: attempt 0 = primary seed; attempt 1 = replacement seed
`primary+1,000,000` allowed only after a logged attempt-0 technical failure (§9.2, L430–433). The log
is append-only and both failures are preserved. **[OBS/H]**

Minor serialization notes (non-blocking, cosmetic): the replacement seed is stored in scientific
notation (`1.310001E+6`); `time_start/end/sampling` are `[]` in record 0 and `null` in record 1
(MATLAB empty-array vs null). Values are correct. **[OBS/M]**

**Preservation gap [OBS/H]:** `tep_exp3_heldout/` is **git-ignored** (`git check-ignore` matches;
`git ls-files` reports the log is not tracked). The two failure records therefore exist **only on
local disk**, outside version control. Any recovery must snapshot/hash-archive this log into committed
provenance before proceeding (see §12/§16).

## 6. WORKBOOK AND DATA-BOUNDARY STATUS

**[OBS/H]** Zero `.xlsx` under `tep_exp3_heldout/` (only the attempt log exists). `output_size_bytes=0`
and `output_sha256=""` in both records. No workbook was written, none accepted, none inspected; the
`StopFcn` plotting was suppressed in attempt 1 (hotfix 003), so no figure was produced either.
No scientific/diagnostic output crossed the data boundary. **[OBS/H]**

## 7. ROOT CAUSE OF `simResult.who` FAILURE

**[OBS/H]** `generate_exp3_heldout.m` L229 `simResult = sim(modelName);` (single output), then L237
`availableOutputs = string(simResult.who);`. `simResult.who` requires `simResult` to be a
`Simulink.SimulationOutput`. In the frozen model configuration it is not (see §8): with
`ReturnWorkspaceOutputs='off'`, single-output `sim(model)` returns a **numeric array** (the time
vector), so `.who` on a `double` raises `MATLAB:structRefFromNonStruct` ("Dot indexing is not
supported for variables of this type"). **[INF/H — from model config + error identity; not executed.]**

The generator's own base-workspace fallback (L242–249, `evalin('base','tout'|'simout'|'xmv')`) is the
correct retrieval path for this model, but it is **never reached** because L237 throws first. The
failure is therefore **post-simulation output marshalling**, not a simulation/physics failure: `sim`
at L229 returned, `StopFcn` was restored and asserted (L231–235) — i.e., the dynamics for seed
1310001 completed before the error. **[OBS/H for control flow; INF/H for "dynamics completed".]**

Answers to the mandatory technical questions:
1. `simResult` is a **numeric array (double)** — the time vector — not a `Simulink.SimulationOutput`,
   struct, or table. **[INF/H]**
2. `.who` is invalid because it is a `double` method call on a non-object under `ReturnWorkspaceOutputs='off'`. **[INF/H]**
3. Yes — the generator implicitly assumed `Simulink.SimulationOutput` (i.e. `ReturnWorkspaceOutputs='on'`); the model uses `'off'`. **[OBS/H]**
4. Yes — `simResult` is effectively `tout` only. **[INF/H]**
5. `tout`/`simout`/`xmv` are produced in the **base workspace** by the model's own To-Workspace
   mechanism (the frozen `StopFcn=TEplot` reads them as base variables), not via the sim-config
   Save* options (which are `off`). **[INF/M — consistent with TEplot + model, not executed; the
   sentinel run in §15 must confirm the base variables are populated and shaped 3001×54.]**
6. **After** dynamics completion (error at L237, after `sim` returned at L229). **[OBS/H]**
7. Transiently, `tout/simout/xmv` likely existed in the **base workspace** during the failed run, but
   they do not persist across MATLAB sessions and no workbook captured them; `onCleanup`
   (`cleanup_environment`) plus session end clear them. Nothing persists on disk. **[INF/M; OBS/H that
   no file persists.]**
8. No signal was displayed, saved, or analyzed (StopFcn suppressed; no workbook; log records 0 output). **[OBS/H]**
10. Robust documented retrieval without plotting and without assuming a SimulationOutput: read the
    base-workspace variables directly (guard with `isa(simResult,'Simulink.SimulationOutput')`, or skip
    to the base-workspace read), i.e. the generator's existing fallback promoted to the primary path.
    Alternatively (more invasive) temporarily set `ReturnWorkspaceOutputs='on'` + `SaveOutput/SaveTime='on'`
    with a single-simulation-output. The first is the minimal non-scientific fix. **[REC/H]** Cite only
    MathWorks R2025b `sim`/`ReturnWorkspaceOutputs` documentation when formalizing; not re-fetched here. **[flagged: external doc not consulted]**
11. The fix is a **non-scientific generator change** (output marshalling); it does **not** require a
    simulator-configuration change if the base-workspace read is used. **[REC/H]**

## 8. MODEL OUTPUT-CONFIGURATION EVIDENCE

**[OBS/H]** `tep_parent_a0413e16/simulator/MultiLoop_mode1.mdl` (hash `d2f6659f…`, unchanged):

| Param | Line | Value |
|---|---|---|
| `ReturnWorkspaceOutputs` | 233 | **`off`** |
| `SaveOutput` | 223 | `off` |
| `SaveState` | 224 | `off` |
| `SaveTime` | 232 | `off` |
| `SaveFormat` | 221 | `Structure` |
| `TimeSaveName` | 235 | `tout` |
| `OutputSaveName` | 236 | `yout` |
| `StateSaveName` | 234 | `xout` |
| `LoadInitialState` | 218 | `on` |

`ReturnWorkspaceOutputs='off'` is the direct cause of `simResult` not being a SimulationOutput. **[OBS/H]**

## 9. MATLAB / SIMULINK API EVIDENCE

Confirmed from code + config (not executed): the generator assumes the SimulationOutput single-output
API (`.who`/`.get`) at L237–241; the model config contradicts that assumption. The observed error
identity `MATLAB:structRefFromNonStruct` on `simResult.who` is exactly what a `double`-typed
`simResult` produces. **[INF/H]** Full runtime confirmation would require executing `sim` (prohibited
by this audit and by the exhausted-attempt state). External MathWorks documentation was **not**
consulted in this pass and should be cited when the fix is formalized. **[flagged]**

## 10. WARNING ASSESSMENT

**[OBS/M — reported warnings, not reproduced here]** Both warnings from the attempt-1 run are
pre-existing legacy-model notices, **not** blockers:
- "TElib was last saved using Simulink 5.0" — legacy library-version notice; the model loads and runs.
- "Variable Time Delay buffer was temporarily increased" — the fault-injection `VariableTransportDelay`
  (MaximumDelay=20; applied delay=10 h) auto-sizing notice; non-fatal, does not change the 10 h
  injection. Both appeared in the attempt-1 run that **completed** its dynamics, confirming they did
  not prevent simulation. **[INF/H]** Neither indicates a scientific problem.

## 11. ATTEMPT-EXHAUSTION DETERMINATION

**[OBS/H]** Protocol §9.2 (`EXP3_FRESH_RUN_PROTOCOL.md`):
- L440–441: "The maximum is two total attempts per intended physical case. Attempt `2` does not exist
  and is rejected by plan, schema, generator, and verifier."
- L442–445: "If attempt `1` also fails, generation stops with an incomplete Experiment 3 and the
  intended case remains `technically_failed` / missing. The sample size is not reduced, the case is
  not analyzed, and **no alternative seed or extra recovery run may be chosen without a new audited
  protocol version created before further generation**."

Attempt 0 and attempt 1 are both logged technical failures ⇒ **two of two attempts consumed** ⇒
`EXP3-N-001` is `technically_failed`/missing and the current protocol is **exhausted** for it. Reuse
of attempt 1 is forbidden regardless of the missing workbook (§9.2 does not condition exhaustion on
workbook creation). That `sim` was called with both seeds only reinforces exhaustion (both seeds
consumed). **Confidence: H.**

## 12. SCIENTIFIC AND GOVERNANCE IMPLICATIONS

Answers to the governance questions (**[INF]** unless a protocol line is cited):
1. Yes — both records formally satisfy the frozen attempt-0 / attempt-1 definitions (§9.2). **[OBS/H]**
2. Yes — both attempts are consumed. **[OBS/H]**
3. No — a missing workbook does **not** re-open attempt 1; the policy caps attempts at 2 irrespective
   of output (§9.2 L440–445). **[OBS/H]**
4. `sim` having run with both seeds does not change (3); it strengthens exhaustion. **[INF/H]**
5. A hotfix under the **current** protocol cannot rescue this case: fixing the generator only matters
   if a run follows, and no attempt slot remains. **[INF/H]**
6. A **new audited protocol version is obligatory** to continue this case (§9.2 L444–445). **[OBS/H]**
7. Introducing an "attempt 2" under the current protocol is **not** defensible; a recovery is
   defensible **only** as a new, pre-specified, separately audited protocol amendment. **[INF/H]**
8. Conditions for a defensible recovery (to be pre-specified **before** any simulation): (i) fix the
   output-marshalling bug (non-scientific); (ii) a mandatory full end-to-end **sentinel** integration
   run through workbook-write + verifier (non-Exp3 seed) that must pass first (§15); (iii) a
   **freshly-allocated seed namespace** for the affected case(s), pre-specified and frozen; (iv)
   permanent preservation of the two existing failure records; (v) a new freeze before generation. **[REC]**
9–10. **Most rigorous + proportionate:** a **protocol amendment (Experiment 3 recovery / v2)** — not a
   full restart and not case-identity replacement — because every failure was a fixable harness/
   software defect and **no scientific signal was observed**, so there is no adaptive-selection
   contamination to purge. Terminating outright is defensible but disproportionate (0 of 30 cases
   completed, all failures non-scientific). Fresh-namespace seeds (vs reusing 310001/1310001) minimize
   any appearance of re-rolling; reuse is arguably valid too (deterministic realization, never
   observed) but carries a small appearance cost — the amendment must pick and pre-specify one. **[REC]**
11. Preserve the two failure records by hash-archiving the current attempt log (sha256 `04ea7d8a…`)
    into committed amendment provenance and starting the recovery in a **new, separate** attempt-log
    namespace so the failures are never overwritten (the log is currently git-ignored, §5). **[REC/H]**
12. Yes — the new procedure **must** include a full sentinel integration run before any Exp3 seed (§15). **[REC/H]**

## 13. RECOVERY OPTIONS WITH RISKS

| Option | Description | Main risk | Assessment |
|---|---|---|---|
| A. Terminate Exp3 as incomplete | Stop; report 0/30 | Loses the entire extension over fixable software bugs | Defensible but **disproportionate** |
| B. **Protocol amendment (recovery v2)** | Fix marshalling + mandatory sentinel gate + fresh frozen seeds + preserve failures + re-freeze | Must be pre-specified & audited before any sim; appearance risk if seeds reused | **Recommended** (proportionate, rigorous) |
| C. Replace case identity | New ID for EXP3-N-001 | Unnecessary; the case, not the harness, was never the problem | Not preferred |
| D. Full restart, new allocation | Re-allocate all 30 | Wasteful; no contamination to justify it | Overkill |

Adaptive-selection risk is ~0 across all options because no signal was observed; the discriminating
factor is proportionality and appearance, which favors **B with a fresh seed namespace**. **[INF/H]**

## 14. RECOMMENDED PATH

**[REC — requires a new scientific/governance decision + audit; NOT authorized now]**
1. Declare `EXP3-N-001` `technically_failed` under the current protocol; **stop** (do not run attempt 2).
2. Author an **Experiment 3 recovery protocol amendment (v2)**, pre-specified and frozen **before any
   simulation**, that: fixes the generator output-retrieval (base-workspace read / `isa` guard —
   non-scientific); mandates the §15 sentinel gate; allocates a **fresh, documented seed namespace**;
   preserves the two failure records (hash-archived) and uses a new attempt-log namespace; re-affirms
   the unchanged scientific plan (case plan, IDs, fault mapping, `ode45`, 0–50 h, 1/60 h, injection
   10 h, 3001×54, replacement policy, statistics).
3. Independently audit + freeze the amendment; **only then** generate, starting from the sentinel run.

Do **not** treat this as authorized: it is a recommendation pending the author's decision and a fresh
pre-generation audit.

## 15. REQUIRED PRE-GENERATION TESTS

**[REC/H]** The systemic root cause of five serial failures is that pre-freeze validation exercised
RNG plumbing and runtime identity with sentinels but **never ran the full generator path end-to-end**.
Before any further Exp3 seed is consumed, a **full sentinel integration run** must:
- use a **non-Exp3 sentinel seed** (e.g. `987654321`, already outside the 310001–310030 / 1310001–…
  allocation);
- execute the **actual** `generate_exp3_heldout` code path (config asserts → StopFcn suppression →
  `rng`→`sim` → **output marshalling** → structural checks → **workbook write** → `verify_written_workbook`)
  to a **throwaway** output directory;
- produce a valid `3001×54` `Sheet1` workbook and pass `verify_exp3_heldout.py`;
- restore `StopFcn=TEplot` and leave the model file byte-identical (`d2f6659f…`);
- confirm `rng(seed,'twister')`→`sim` adjacency and that no attempt-2 path exists.
This run must be discarded (sentinel), and it must pass **before** any Exp3 seed is used.

## 16. ARTIFACTS THAT WOULD REQUIRE A NEW FREEZE

**[REC]** A recovery necessarily creates a **new frozen boundary** (separate from `exp3-heldout-frozen`
and hotfix tags), covering: the amended protocol; the corrected generator; a new hotfix/amendment
manifest binding the chain freeze→h1→h2→h3→h4→**recovery**; the new seed-allocation record; the
archived pre-recovery attempt log (sha256 `04ea7d8a…`); the sentinel-run evidence; and the updated
verifier/tests (including a regression that asserts the output-marshalling path and the sentinel gate).
The original freeze, the four hotfix commits/tags, and Experiment 1 (56/56) must remain untouched.

## 17. OPERATIONS NOT PERFORMED

No `sim`; no `generate_exp3_heldout`; no re-run of attempt 0 or 1; no attempt 2; no workbook; no signal
inspection; no plot; no seed/case-ID change; no file modified/created/deleted; no commit/tag/push/
reset/checkout/clean; the attempt log was read only, never modified; no scientific trajectory used as a
decision criterion.

## 18. FINAL BLOCKER STATEMENT

`EXP3-N-001` has consumed both permitted attempts (2/2) as documented technical failures with no
accepted scientific output; the current frozen protocol is **exhausted** for this case and, by its own
§9.2, cannot continue without a **new audited protocol version created before further simulation**.
**Status: BLOCKED — ATTEMPTS EXHAUSTED.** Continuation is a governance decision requiring a new
pre-specified, independently audited, re-frozen recovery amendment (recommended Option B) — explicitly
**not** authorized by this read-only audit. Experiment 1 remains intact (56/56); the freeze and all
four hotfix tags are unchanged.

---
*Read-only audit. Verdict: BLOCKED — ATTEMPTS EXHAUSTED. Chain freeze(`b02e93f9`)→h1(`cdba020`)→
h2(`2813002`)→h3(`0d86972`)→h4(`1cad481`) verified against `.git`; attempt log (`04ea7d8a`, git-ignored)
holds exactly 2 technical failures; 0 workbooks; Experiment 1 56/56 intact; model `.mdl` `d2f6659f`
unchanged.*
