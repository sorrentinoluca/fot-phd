# Independent Review — Condition C R10 Evaluation

**Reviewer:** Claude (automated independent review)
**Date:** 2026-09-07
**Scope:** Read-only critical review of the Condition C ("centralized full-information pooled ICL") evaluation in the fot-tep project
**Commits reviewed:**

| Tag | Commit |
|---|---|
| `condition-c-freeze-r10` | `60ccc7539714e909aae7318cc72031d7acdd4e78` |
| `condition-c-predictions-frozen-r10` | `8d6b7a0636e9a15f0ebbd32ed0f9e2ce4faea30a` |
| `condition-c-results-frozen-r10` | `89e4caebe635973ef438d4b601bb4f761417193a` |

---

## Verdict

### GO WITH LIMITATIONS

The evaluation pipeline is cryptographically sound, no code defects were found in the reviewed evaluation paths, the metrics reproduce, and the procedural sequence was followed. The single limitation that prevents an unconditional GO is interpretive: the entire C−B advantage is driven by one fault class (CLS-OJNSG), and the bootstrap CI, while correctly computed, is constrained by a 5-value discrete grid with only 3 clusters per stratum. This does not invalidate the result but materially limits the generalizability claim. The result must be presented as a post-hoc exploratory reference finding, not as evidence of a general advantage, and the single-stratum concentration must be disclosed.

---

## Findings by Severity

### P1 — Critical

**None.**

No critical defects were found. All cryptographic chains are intact, the evaluator code is correct, the firewall between inference and evaluation is sound, and the frozen artifacts are self-consistent.

---

### P2 — Significant

#### P2-1: Entire C−B advantage concentrated in one fault stratum

**Category:** Scientific interpretation
**Verified fact:** All 5 B-agent errors across the 12 fault cases (36 agent-case pairs) occur in the CLS-OJNSG stratum: PBH-007 (2/3 unseen agents wrong), PBH-008 (1/3 wrong), PBH-009 (2/3 wrong). The remaining 9 fault cases have `paired_delta_i = 0` — Conditions B and C perform identically.

**Consequence:** The point estimate Δ_{C-B} = 5/36 ≈ 0.139 and bootstrap CI [1/12, 1/6] are arithmetically correct, but the delta is entirely an artifact of B's difficulty with one specific fault class. The bootstrap, stratified by true pseudolabel with 3 clusters per stratum, correctly preserves this structure — the CI can only take 5 distinct values — but this means the "confidence interval" reflects resampling noise over 3 cases within one failing stratum, not a broad distributional statement.

**Recommendation:** Any publication or summary that cites Δ_{C-B} must disclose:
1. The advantage is driven entirely by CLS-OJNSG (3 cases).
2. The 9 non-CLS-OJNSG fault cases show zero difference.
3. The bootstrap CI inhabits a 5-value discrete lattice.
4. With only 3 clusters per stratum, the stratified bootstrap has minimal effective resolution.

This is correctly flagged by `independence_claim: False` in the results file, and the PLAN document (§6.1–§6.5) acknowledges the limitations. The P2 rating reflects the risk that downstream consumers may cite the headline delta without the stratum-level decomposition.

---

### P3 — Minor

#### P3-1: Byte-for-byte reproduction requires Python version pinning

**Category:** Reproducibility
**Verified fact:** In the independent reproduction, `delta_C_minus_B` and the bootstrap `point_estimate` differed by 1 ULP (unit in the last place) between Python 3.11 and Python 3.13. The Python interpreter version is not pinned by the protocol, although the OpenAI SDK, model, and reasoning effort are pinned.

The differences are ≤ 1.11e-16 in magnitude (IEEE 754 rounding of the sum 5/36). Mathematical equivalence holds; both round to 5/36. All integer-checkable quantities (counts, correct/incorrect, CI endpoints 1/12 and 1/6) reproduce exactly.

**Recommendation:** Pin the Python interpreter version (3.13.x) in the protocol amendment or execution_config for strict byte-for-byte reproducibility. Alternatively, document that ULP-level float differences under different CPython versions are expected and benign.

#### P3-2: Phase B suite requires the canonical repository context

**Category:** Test infrastructure
**Verified fact:** An initial run from a stripped staging copy could not satisfy tests that depend on Git history and external held-out workbooks. The final canonical rerun in a temporary repository mirror, with Git history and all 15 external workbook files referenced by the manifest, passed 100/100 tests. The temporary mirror was then removed.

**Recommendation:** Document Git history and the 15 manifest-referenced workbooks as environmental prerequisites for running the complete Phase B suite. No evaluation-logic defect was found.

---

## Section-by-Section Audit

### §1 — Git Chain and Scope

| Check | Status |
|---|---|
| Three tags exist and resolve to expected commits | ✅ |
| Linear chain: freeze → predictions → results | ✅ |
| File scope: freeze commit touches only `icl/` files | ✅ |
| No evaluator-side files modified in inference commits | ✅ |
| No `phase_b/` files modified in any C commit | ✅ |
| Worktree HEAD matches results tag | ✅ |

All six sub-checks pass. The commit chain is linear and correctly scoped.

### §2 — Cryptographic Integrity and Provenance

| Artifact | Expected SHA-256 (prefix) | Verified |
|---|---|---|
| `evaluation_results_c.json` | `1ea60e12de...` | ✅ |
| `c_records.jsonl` | per predictions manifest | ✅ |
| `c_aggregate_records.jsonl` | per aggregate manifest | ✅ |
| `c_schedule.json` | `3f1b102a89...` | ✅ |
| Evaluator-side freeze manifest (11 artifacts) | all match | ✅ |

**Verification functions executed (all pass):**
- `verify_c_predictions_freeze()`: hash, count (45), schedule cross-check, per-record validation
- `verify_evaluator_freeze()`: all evaluator-side artifact hashes, B-aggregate hash against inference manifest
- `verify_aggregate_freeze()`: 11 checks including R10 integral recomputation cross-verification

Record-level provenance verified: 45 raw records (15 cases × 3 reps), all `valid=True`, all `stateless=True`, consistent `prompt_sha256` per case (15 unique hashes), `model_requested = model_returned = gpt-5.6-terra`, `openai_sdk_version = 3.6.0`, `reasoning_effort = medium`, zero structural retries, zero network retries.

### §3 — Independent Reproduction

Metrics recomputed independently from raw records:

| Metric | Frozen Value | Reproduced | Match |
|---|---|---|---|
| Overall accuracy | 15/15 = 1.0 | 15/15 = 1.0 | ✅ |
| Fault accuracy | 12/12 = 1.0 | 12/12 = 1.0 | ✅ |
| Normal accuracy | 3/3 = 1.0 | 3/3 = 1.0 | ✅ |
| Abstentions | 0 | 0 | ✅ |
| Δ_{C-B} | 0.13888888888888892 | 5/36 ≈ 0.1389 | ✅ (ULP) |
| CI lower | 0.08333333333333333 | 1/12 | ✅ |
| CI upper | 0.16666666666666666 | 1/6 | ✅ |
| B unseen fault accuracy | 31/36 | 31/36 | ✅ |

Simple independent recomputation path: C gets all 15 correct. B-unseen gets 31/36 correct (5 errors all in CLS-OJNSG). Delta = (12 - 31/3) / 12 = (12 - 31/3)/12 = 5/36. CI endpoints correspond to resampling the 3 CLS-OJNSG cases: all-worst = 1/6, all-best stays at 1/12 due to the mix.

### §4 — Bootstrap Analysis

| Parameter | Protocol | Code | Match |
|---|---|---|---|
| Iterations | 10,000 | 10,000 | ✅ |
| Seed | 20260906 | 20260906 | ✅ |
| Clusters | 12 (physical cases) | 12 | ✅ |
| Strata | 4 fault classes × 3 | 4 × 3 | ✅ |
| CI level | 95% | 95% | ✅ |
| Method | Percentile | `np.quantile` | ✅ |
| RNG | `np.random.default_rng` | confirmed | ✅ |

The bootstrap is correctly implemented: stratified resampling within each fault-class stratum, maintaining the pairing structure. The `independence_claim: False` flag is correctly set.

**Structural observation (not a defect):** Because 9 of 12 cases have `delta_i = 0` and the remaining 3 cases take values from {1/3, 2/3}, the bootstrap draw distribution is a discrete lattice with only 5 distinct possible delta values. The CI [1/12, 1/6] is the tightest interval the data can produce. This is a property of the data, not a code error.

### §5 — Evaluator Code Review

Systematic review of `evaluate_c_predictions.py` (1117 lines), `aggregation_c.py` (497 lines), `records_c.py` (229 lines):

| Check | Result |
|---|---|
| Ground truth leakage in inference path | None found ✅ |
| Freeze guard bypass paths | None — all guards mandatory, fail-closed ✅ |
| Denominator correctness (12 fault, 3 normal, 15 overall) | Correct ✅ |
| Paired comparison structure | Correctly paired per physical_case_id ✅ |
| Normal cases excluded from delta | `if truth == normal_label: continue` ✅ |
| Unseen agent set (|U_i| = 3) | Validated with explicit check ✅ |
| Majority voting (≥2 of 3) | Correct, only `valid=True` records vote ✅ |
| R10 integral cross-verification | Recomputed aggregates compared field-by-field ✅ |
| Bootstrap stratification | 4 strata × 3 clusters, within-stratum resampling ✅ |
| CRunRecord validation coverage | 30+ field-level checks, all provenance fields ✅ |
| Plan-code-result consistency | All formula references (R5 §5.2, §5.3) match ✅ |
| `independence_claim: False` | Correctly set ✅ |

No defects found in the evaluator code. The defense-in-depth architecture (predictions barrier → evaluator freeze → aggregate freeze → R10 cross-verify → metrics → delta → bootstrap) is sound.

### §6 — Test Suites

| Suite | Total | Passed | Failed | Errors | Notes |
|---|---|---|---|---|---|
| ICL (`icl/tests/`) | 301 | 301 | 0 | 0 | All pass ✅ |
| Phase B (`phase_b/tests/`) | 100 | 100 | 0 | 0 | Canonical temporary mirror ✅ |

ICL test suite includes: record validation (CRunRecord schema, rejections, coherence), runner tests (full run, idempotency, pilot-only, resume, freeze guard, firewall, network retry), schedule tests, evaluation tests, and integration tests. All 301 pass.

The first attempt from a stripped staging copy exposed environmental prerequisites. The definitive rerun used a temporary repository mirror with Git history and the 15 external workbook files referenced by the manifest; all 100 tests passed and the mirror was removed.

### §7 — Procedural Deviation Assessment (Pilot Gate)

| Check | Result |
|---|---|
| Pilot records (seq 0–14) timestamps | 00:18:07 – 00:18:41 UTC ✅ |
| Non-pilot records (seq 15–44) timestamps | 07:09:44 – 07:11:04 UTC ✅ |
| Gap between last pilot and first non-pilot | **411 minutes (6.85 hours)** ✅ |
| Orchestrator stop respected | Yes — clear temporal separation ✅ |
| All 45 records present and complete | Yes ✅ |
| Sequential execution order | seq 0→44, monotonically increasing timestamps ✅ |

The 411-minute gap between pilot completion (00:18:41) and non-pilot start (07:09:44) confirms the orchestrator stop instruction was respected. The pilot gate was executed as a separate tranche; the 30 non-pilot requests were not run until after the pilot was reviewed.

### §8 — Scientific Interpretation

| Claim | Verified | Assessment |
|---|---|---|
| C is a post-hoc exploratory reference | ✅ | `post_hoc: True`, `independence_claim: False` |
| C achieves 100% accuracy (15/15) | ✅ | All cases correct, 0 abstentions |
| Δ_{C-B} = 5/36 ≈ 0.139, CI [1/12, 1/6] | ✅ | Arithmetically correct |
| Full-information = examples + insights, not source texts | ✅ | Stated in protocol amendment |
| C does not replace the A/B/E conditions | ✅ | Stated in amendment scope |
| Unchanged: data, verbalizations, pseudolabels, model, R | ✅ | Verified by freeze manifests |
| No temperature/seed (not supported by model) | ✅ | execution_config confirms |
| Structured output strict mode | ✅ | Confirmed in config |

**Interpretive caution (see P2-1):** The headline Δ = 0.139 with CI excluding zero is technically accurate but potentially misleading without the stratum decomposition. Condition C's advantage is entirely due to correctly classifying CLS-OJNSG cases that B's unseen agents frequently misclassify. On the other 9 fault cases, B and C are equally correct. This is consistent with the information-theoretic expectation (C has full coverage; B agents lack CLS-OJNSG examples when it is their unseen class), but it means the delta measures a specific knowledge-gap effect, not a general performance advantage.

---

## Positive Findings

1. **Exemplary cryptographic provenance chain.** Triple-layer manifest verification (predictions → evaluator → aggregate) with fail-closed semantics. R10 integral cross-verification recomputes aggregates from raw records and compares field-by-field — this catches any semantic drift, not just hash-level corruption.

2. **Robust firewall architecture.** The inference/evaluation split is enforced structurally: the runner never imports evaluator-side modules, never accesses pseudolabel_mapping.json, and tests (`test_no_evaluator_side_references`, `test_no_phase_b_prediction_access`) verify this at the source-code scan level.

3. **Comprehensive test coverage.** 301 ICL tests covering record validation, runner behavior, freeze guards, idempotent resume, network retry, firewall enforcement, and schedule identity. All pass.

4. **Correct post-hoc framing.** The results file sets `independence_claim: False`. The protocol amendment clearly states post-hoc status with zero completed inference at decision time. The PLAN document (§6.1–§6.5) enumerates five specific limitations.

5. **Clean execution.** All 45 records completed with zero structural retries, zero network retries, consistent model and SDK version, valid structured output on every call.

6. **Proper pilot gate sequencing.** 411-minute gap between pilot and non-pilot tranches confirms the stop-and-review protocol was followed.

---

## Summary Table

| Section | Status | Findings |
|---|---|---|
| §1 Git chain | ✅ PASS | — |
| §2 Integrity | ✅ PASS | — |
| §3 Reproduction | ✅ PASS | P3-1 (float ULP) |
| §4 Bootstrap | ✅ PASS | Part of P2-1 |
| §5 Code review | ✅ PASS | — |
| §6 Test suites | ✅ PASS | P3-2 (environment prerequisite) |
| §7 Pilot gate | ✅ PASS | — |
| §8 Interpretation | ⚠️ LIMITATION | P2-1 (single-stratum concentration) |

**Verdict: GO WITH LIMITATIONS**

The evaluation is technically sound and ready for use as a post-hoc exploratory reference, provided the single-stratum concentration (P2-1) is disclosed in any downstream reporting.
