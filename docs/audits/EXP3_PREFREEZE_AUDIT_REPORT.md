# Experiment 3 — Pre-Freeze Audit Report
## Fresh Prospective Physical-Run Extension (FoT–TEP, IEEE BigData 2026)

**Role:** Senior researcher / IEEE reviewer / independent experimental auditor.
**Scope:** read-only pre-freeze audit of the Experiment 3 protocol + generation/verification
infrastructure, **before** generation of the 30 physical runs.
**Nothing was modified, generated, executed as a simulation, inferred, committed, or tagged.**

### Audit provenance

- **Repository HEAD:** `430590001922b28d618b739b12e3471e7ebd0afa` (== the stated reference commit).
- **Working tree at audit time:** two tracked files modified vs HEAD — `.gitignore`
  (adds `tep_exp3_heldout/`) and `phase_b/exp3/EXP3_FRESH_RUN_PROTOCOL.md`; untracked new Exp3
  artifacts under `phase_b/exp3/` + `phase_b/tests/test_exp3_pre_freeze.py`; plus unrelated
  untracked files (`2604.16778v2.pdf`, `docs/fot_walkthrough_conversazione.pdf`,
  `docs/related_work_scan.md`).
- **Remote sync:** `git fetch` is not reachable from this environment; audit performed on the live
  local working tree (authoritative for a pre-freeze audit). `main` and `origin/main` were level at
  the reference commit per the local tracking ref.
- **Experiment 1 status:** verified intact (see §D and blockers).
- **Audit date:** 2026-09-02.

---

## A. VERDICT

> ## ✅ READY FOR EXP3 FREEZE

The Experiment 3 protocol, machine-readable case plan, generation script, RNG runtime evidence,
attempt-log schema/template, manifest template, and fail-closed verifier are **scientifically and
technically ready to be frozen before generation**. No blocker was identified. Experiment 1 remains
byte-for-byte immutable. The design is a correctly-scoped *prospective fresh-run replication on the
same four fault classes*, with a fixed sample, deterministic seeds, a technically-pure exclusion
policy, an enforced data boundary, and a statistical plan consistent with Experiment 1.

"Freeze" here means the **protocol + generation-infrastructure freeze** (flip the case-plan status
to `FROZEN_BEFORE_GENERATION`, pin every Exp3 artifact hash, tag). This verdict constitutes the
scientific-audit approval that Section 17 of the protocol lists as still-open; the remaining open
checklist items are the freeze action itself and the *later* pre-inference schedule freeze, neither
of which is a defect.

---

## B. BLOCKERS

**None.**

Every condition that would have produced a BLOCKER was checked and is satisfied:

- no adaptive/outcome-driven retry (replacement is technical-only, deterministic, capped at 2
  attempts, and enforced in plan + schema + generator + verifier — see §D);
- no non-technical exclusion criterion anywhere;
- no modification of any Experiment 1 frozen artifact (56/56 hashes match);
- no Exp3 data, verbalization, or inference performed;
- no open `k=5–7` sample interval (fixed at 6/class = 30);
- terminology contains no forbidden positive claim.

---

## C. NON-BLOCKING OBSERVATIONS

1. **Verifier dependency not satisfied on the generation host** *(tooling — fix before relying on
   the verifier).*
   - **File:** `phase_b/exp3/verify_exp3_heldout.py` (imports `Draft202012Validator`).
   - **Problem:** the host ships `jsonschema 3.2.0`; the verifier requires `jsonschema ≥ 4.18`. On
     the host the verifier currently raises `ImportError` and cannot run. In a correctly pinned
     environment the auditor ran it: `--pre-freeze` → **PASS**, and full mode on the still-draft plan
     → correctly **refuses** ("case plan is not frozen; held-out verification is disabled").
   - **Why it matters:** the project's reproducibility discipline depends on the fail-closed verifier
     being runnable on the same machine that generates the data; the freeze checklist marks the
     verifier as validated.
   - **Minimal fix:** pin `jsonschema>=4.18` (and `openpyxl`) in the reference requirements, and
     record a green `--pre-freeze` verifier run **and** `test_exp3_pre_freeze.py` run in the freeze
     commit. (No logic change needed — the logic is correct.)

2. **Freeze-commit scope hygiene** *(process).*
   - **Problem:** unrelated untracked files (`2604.16778v2.pdf`, `docs/…pdf`, `docs/related_work_scan.md`)
     sit in the working tree.
   - **Minimal fix:** scope the freeze commit to exactly the Exp3 artifacts + `.gitignore` +
     `EXP3_FRESH_RUN_PROTOCOL.md`; keep the stray PDFs/docs out of the freeze.

3. **Stale `.git/index.lock` present** *(operational).*
   - **Problem:** a stale lock is in `.git/`; it will block the freeze commit until removed.
   - **Minimal fix:** remove `.git/index.lock` before the freeze commit (left untouched here to
     preserve the read-only audit).

4. **Status strings must flip together at freeze** *(consistency, already designed).*
   - `exp3_case_plan.json` status is `PRE_FREEZE_DRAFT` and the protocol header is `DRAFT FOR
     SCIENTIFIC AUDIT — NOT FROZEN`. The generator refuses to run until the plan status is
     `FROZEN_BEFORE_GENERATION`. At freeze, flip both, then pin the resulting `case_plan` hash — the
     generator/verifier bind that exact hash. This is the intended mechanism, noted so the two
     status strings are updated in the same freeze step.

5. **S-function seed entropy is a single scalar** *(disclosed, empirically mitigated).*
   - The MATLAB seed reaches the plant via one `rand()` scalar that seeds the S-function's internal
     LCG. Distinctness of realizations is demonstrated empirically for the sentinels
     (`isequal=false`, max abs diff `131.56`) and the 30 consecutive twister seeds yield well-spread
     first draws; the protocol honestly states the freeze does not *mathematically* guarantee
     independence. No action required; keep the honest independence wording in the paper.

---

## D. CONSISTENCY MATRIX

Protocol = `EXP3_FRESH_RUN_PROTOCOL.md`; Config = `exp3_case_plan.json` (+ schema/template);
Code = `generate_exp3_heldout.m` / `verify_exp3_heldout.py`; Runtime evidence =
`RNG_RUNTIME_VALIDATION.md` / sentinel probe.

| Aspect | Protocol | Config | Code | Runtime evidence | Status |
|---|---|---|---|---|---|
| Sample size | 6×5 = 30 (24 fault + 6 Normal) | 30 cases; totals 30/24 | generator asserts 30; verifier enforces counts=6 each | n/a | **CONSISTENT** |
| Physical IDs | `EXP3-{N,F1,F8,F10,F13}-00[1-6]`, no `PBH-*` overlap | 30 unique IDs, deterministic order | regex + canonical order asserted | n/a | **CONSISTENT** |
| RNG | twister; primary 310001–310030; replace +1e6; bootstrap 310031 | identical | generator/verifier assert identical | sentinel same/diff seed proof | **CONSISTENT** |
| Replacement policy | attempt 0/1; max 2; technical-only; no attempt 2 | allowed_attempts [0,1]; max 2 | generator + schema + verifier enforce technical-failure precondition; attempt≤1 | n/a | **CONSISTENT** |
| Simulator identity | commit `a0413e16`, `MultiLoop_mode1`, Mode 1, normal, ode45, 0–50 h, 1/60 h, inject 10 h | identical + model/init/sfunction/MEX SHA-256 | generator hash-checks model/init/sfunction/MEX before sim | matches Exp1 `SIMULATOR_PARENT_AUDIT.md` | **CONSISTENT** |
| Runtime identity | R2025b `25.2.0.3312555`, Simulink `25.2`/`28-Jul-2025`, MACA64 | identical (const-pinned) | generator + verifier assert identical | captured by probe | **CONSISTENT** |
| Output structure | 1×Sheet1, 3001×54, `Time (h)`+XMEAS1–41+XMV1–12, 0–50 h, 1/60 h | expected_rows 3001, cols 54 | structural check + workbook round-trip; verifier re-checks | matches Exp1 held-out manifest (3001×54) | **CONSISTENT** |
| Statistics | physical-run unit; paired cluster bootstrap; 10 000; seed 310031; Exp3-only primary; pooled secondary; B−A primary, B−E supporting | identical statistics block | verifier enforces statistics block | n/a | **CONSISTENT** |
| Data boundary | generate → mechanical checks → freeze → verbalize → infer; no diagnostic inspection pre-verbalization | status gate `FROZEN_BEFORE_GENERATION` | generator disabled until frozen; no verbalizer/LLM/metrics; raw dir git-ignored | n/a | **CONSISTENT** |
| Experiment 1 immutability | declared immutable; frozen hashes re-checked | reuses Exp1 frozen hashes in §10 | test re-hashes ≥50 artifacts | 56/56 artifacts match, 0 mismatch (independently re-verified) | **CONSISTENT** |

---

## E. REVIEWER RED-TEAM (residual critiques after this freeze candidate)

1. **Reviewer A (statistics).** *"72 unseen agent-cases from only 24 fault runs — is this
   pseudo-replication?"* → Mitigated by design: the independent unit is the physical run; the three
   unseen agent rows per run are clustered; the paired cluster bootstrap resamples runs, not rows.
   Residual is the honest small-cluster count (24 fault runs), correctly disclosed — not a defect.

2. **Reviewer B (reproducibility).** *"How exhaustively is seed→realization distinctness
   guaranteed across all 30 seeds, given a single-scalar S-function seed?"* → Empirically shown for
   sentinels and mechanistically well-behaved for consecutive twister seeds; not exhaustively proven
   for all 30. Disclosed. The pinned runtime + hashes + attempt log make each run auditable.

3. **Reviewer C (TEP/domain).** *"Is the fresh regime truly identical to Experiment 1, or is there
   hidden drift?"* → Model/initial-state/S-function(source+MEX) hashes match the Exp1 held-out
   provenance; injection fixed at 10 h via the hash-pinned model; output schema matches the Exp1
   held-out (3001×54). Residual: the same simulator/mode/four-fault domain — which is exactly the
   intended scope (replication, not generalization).

4. **Reviewer D (LLM/evaluation).** *"Any leakage or tuning on the new runs?"* → Generation performs
   no verbalization/LLM/metrics; the data boundary forbids diagnostic inspection before the held-out
   freeze; verbalizer/insights/prompts/derangement/evaluator are reused frozen; ground-truth join
   stays post-inference. The pre-inference Exp3 schedule freeze remains a required later gate
   (correctly deferred).

5. **Reviewer A/D (analysis discipline).** *"Could a null Exp3 result be rescued by pooling with
   Exp1?"* → Prevented: §15 fixes the Exp3-only analysis as primary and the pooled Exp1+Exp3 summary
   as descriptive-only, with no pooled success criterion pre-specified and post-hoc addition
   prohibited. Success/failure criteria for B−A (CI excludes 0) are fixed before outcomes.

None of the five is fatal or requires a design change before freezing.

---

## F. FINAL RECOMMENDATION

On the basis of the artifacts **as they stand, before any Experiment 3 outcome is visible**, the
protocol can be frozen **without introducing an avoidable methodological vulnerability**. The
construction is unusually disciplined: fail-closed on every axis the brief asked me to attack
(sample, IDs, RNG, replacement, simulator identity, runtime, output structure, statistics, data
boundary, Experiment 1 immutability), technically-pure exclusion criteria, and an honest
independence statement.

**Proceed to freeze**, executing these steps (all outside this read-only audit):

1. Remove the stale `.git/index.lock`.
2. Pin `jsonschema>=4.18` and `openpyxl` in the reference requirements; record a green
   `verify_exp3_heldout.py --pre-freeze` run **and** `test_exp3_pre_freeze.py` run.
3. Flip `exp3_case_plan.json` status → `FROZEN_BEFORE_GENERATION` and the protocol header → frozen,
   in the same commit.
4. Scope the freeze commit to the Exp3 artifacts + `.gitignore` + protocol only; pin every Exp3
   artifact SHA-256; create the freeze tag.
5. Only then generate the 30 runs in canonical order; the pre-inference Exp3 schedule freeze remains
   a separate, later gate before any A/B/E inference.

**Result that would change this recommendation:** none among the audited artifacts. Only the
introduction of a non-technical exclusion criterion, an outcome-dependent seed/sample change, a
modification to any Experiment 1 frozen artifact, or generation occurring before the freeze would
turn this into **NOT READY FOR EXP3 FREEZE**.

---

*Read-only audit. No file modified, no simulation run, no data generated, no inference performed, no
commit, no tag. Experiment 1 verified immutable (`45ec4ee`; 56/56 frozen hashes match).*
