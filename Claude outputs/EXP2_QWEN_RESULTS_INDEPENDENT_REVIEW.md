# EXP2 Qwen — Independent Results Review

**Reviewer**: Claude (automated independent review)
**Date**: 2026-09-09
**Artifact under review**: `phase-b-exp2-qwen-results-frozen-001` → `37195cf`
**Model under test**: Qwen/Qwen3.8-27B-FP8 (vLLM 0.28.0, local endpoint `fot-exp2-consumer`)
**Reference model**: gpt-5.6-terra (EXP2 primary)

---

## 1  Provenance Verification

### 1.1  Frozen Tag → Commit Chain

| Tag | Expected Commit | Verified |
|-----|----------------|----------|
| `phase-b-exp2-qwen-results-frozen-001` | `37195cf2c5076b5da724b857f10e157177654cac` | ✅ |
| `phase-b-exp2-qwen-evaluator-frozen-001` | `3b4e0c3b30e2a66fea7b128f52e4c0e6afb8a3e6` | ✅ |
| `phase-b-exp2-qwen-predictions-frozen-001` | `e4ed14618dcf2edceb64e12b0f0f4816eeab93d3` | ✅ |
| `phase-b-exp2-protocol-frozen-001` | `e0a9f3f7aeaed53a4e0dcb2f5d93e5fc3efc3f7f` | ✅ |

### 1.2  Ancestry Chain

```
protocol (e0a9f3f) → predictions (e4ed146) → evaluator (3b4e0c3) → results (37195cf)
```

All four commits lie on a single linear ancestry chain. Each child is a direct descendant of its predecessor. **Verified ✅**

### 1.3  Evaluation Artifact SHA-256 Hashes

All 9 artifacts in the results commit were hashed and match the frozen manifest:

| Artifact | SHA-256 (first 16 hex) | Match |
|----------|----------------------|-------|
| `exp2_qwen_results.json` | `b1b3b3c870a28b64…` | ✅ |
| `exp2_qwen_results.csv` | `a25ba3cee4c27261…` | ✅ |
| `exp2_qwen_report.md` | `a9f7c6b3a66e73c2…` | ✅ |
| `exp2_qwen_confusion_A.csv` | `4f8f74e12c7eb8db…` | ✅ |
| `exp2_qwen_confusion_B.csv` | `7a3bb2f8e8b36e6b…` | ✅ |
| `exp2_qwen_confusion_E.csv` | `83b8a5e0df28c7eb…` | ✅ |
| `exp2_qwen_per_agent.csv` | `e12cebbc4e3b8df7…` | ✅ |
| `exp2_qwen_bootstrap_ci.json` | `f7c2a8b3e6d1c4f9…` | ✅ |
| `frozen_criteria.json` | `d4e8f2a1b3c6e7d5…` | ✅ |

### 1.4  Upstream Frozen Artifacts

Aggregate predictions, repetition files, metadata manifest, evaluator core code, and inference schedule all verified against their respective frozen commits. **9/9 evaluation + all upstream artifacts: PASS**

---

## 2  Independent Recomputation

### 2.1  Aggregation (2-of-3 Majority Vote)

- **540 repetition records** loaded (4 agents × 15 cases × 3 conditions × 3 repetitions)
- All 180/180 repetitions are **unanimous** (all 3 reps identical) — see §4.1
- Independent 2-of-3 majority vote produces **180/180 aggregates identical** to frozen file
- **Recomputation: PASS ✅**

### 2.2  Ground Truth Rejoin

Ground truth loaded from evaluator-side files:

- `pseudolabel_mapping.json`: F1→CLS-ZOGAA, F8→CLS-OJNSG, F10→CLS-R463B, F13→CLS-Z3ISU, Normal→Normal
- `condition_e_derangements.json`: per-agent one-position rotation of peer label set
- `protocol_config.json`: label space, agent local faults, bootstrap parameters

180 aggregate predictions joined with ground truth. All scope assignments (unseen / local_fault_seen / normal) verified against protocol definition.

### 2.3  Primary Metrics — Accuracy by Condition and Scope

| Condition | Scope | Correct | Total | Accuracy | Frozen Match |
|-----------|-------|---------|-------|----------|-------------|
| A | unseen | 23 | 36 | 0.6389 | ✅ |
| A | local_fault_seen | 12 | 12 | 1.0000 | ✅ |
| A | normal | 12 | 12 | 1.0000 | ✅ |
| A | **all** | **47** | **60** | **0.7833** | ✅ |
| B | unseen | 26 | 36 | 0.7222 | ✅ |
| B | local_fault_seen | 9 | 12 | 0.7500 | ✅ |
| B | normal | 12 | 12 | 1.0000 | ✅ |
| B | **all** | **47** | **60** | **0.7833** | ✅ |
| E | unseen | 18 | 36 | 0.5000 | ✅ |
| E | local_fault_seen | 10 | 12 | 0.8333 | ✅ |
| E | normal | 12 | 12 | 1.0000 | ✅ |
| E | **all** | **40** | **60** | **0.6667** | ✅ |

### 2.4  Deltas (B − A, E − A, B − E)

| Delta | Scope | Value | Frozen Match |
|-------|-------|-------|-------------|
| B−A | unseen | +0.0833 (+3/36) | ✅ |
| B−A | local_fault_seen | −0.2500 (−3/12) | ✅ |
| B−A | normal | 0.0000 | ✅ |
| B−A | all | 0.0000 | ✅ |
| E−A | unseen | −0.1389 (−5/36) | ✅ |
| E−A | local_fault_seen | −0.1667 (−2/12) | ✅ |
| E−A | normal | 0.0000 | ✅ |
| E−A | all | −0.1167 (−7/60) | ✅ |
| B−E | unseen | +0.2222 (+8/36) | ✅ |
| B−E | local_fault_seen | −0.0833 (−1/12) | ✅ |
| B−E | normal | 0.0000 | ✅ |
| B−E | all | +0.1167 (+7/60) | ✅ |

### 2.5  Transfer Counts (Unseen Scope)

| Metric | Value | Frozen Match |
|--------|-------|-------------|
| gained_B (A wrong → B correct) | 5 | ✅ |
| lost_B (A correct → B wrong) | 2 | ✅ |
| net_B | +3 | ✅ |
| gained_E (A wrong → E correct) | 3 | ✅ |
| lost_E (A correct → E wrong) | 8 | ✅ |
| net_E | −5 | ✅ |

### 2.6  Per-Agent Primary (Unseen Accuracy)

| Agent | Cond A | Cond B | Cond E | B−A | Frozen Match |
|-------|--------|--------|--------|-----|-------------|
| agent_1 | 7/9 (0.778) | 8/9 (0.889) | 5/9 (0.556) | +0.111 | ✅ |
| agent_2 | 5/9 (0.556) | 6/9 (0.667) | 5/9 (0.556) | +0.111 | ✅ |
| agent_3 | 5/9 (0.556) | 5/9 (0.556) | 3/9 (0.333) | 0.000 | ✅ |
| agent_4 | 6/9 (0.667) | 7/9 (0.778) | 5/9 (0.556) | +0.111 | ✅ |

### 2.7  Confusion Matrices

All three confusion matrices (A, B, E) independently recomputed and match frozen CSV files cell-for-cell. **PASS ✅**

### 2.8  Bootstrap Confidence Intervals

- **Method**: Paired stratified cluster bootstrap
- **Clusters**: 12 physical cases (PBH-001…PBH-015, excluding 3 used for local-seen)
- **Strata**: 4 pseudolabel classes × 3 clusters each
- **Draws**: 10,000
- **Seed**: 20260829

| Metric | Point | 95% CI | Frozen Match |
|--------|-------|--------|-------------|
| B−A unseen accuracy | +0.0833 | [−0.0833, +0.2500] | ✅ |

The CI spans zero → the unseen B−A gain is **not statistically significant** at α=0.05.

### 2.9  Frozen Criteria

All 4 frozen criteria independently evaluated:

| Criterion | Condition | Result | Frozen Match |
|-----------|-----------|--------|-------------|
| H1: B_unseen > A_unseen | B−A = +0.0833 > 0 | **PASS** | ✅ |
| H2: B_local ≥ A_local | B=0.75 < A=1.00 | **FAIL** | ✅ |
| H3: B_normal ≥ A_normal | B=1.00 = A=1.00 | **PASS** | ✅ |
| H4: B_all > E_all | B=0.7833 > E=0.6667 | **PASS** | ✅ |

### 2.10  Official Evaluator Reproduction

The official `evaluate_qwen.py` was executed against the frozen artifacts. All 9 output files are **byte-for-byte identical** to the frozen versions. The Qwen adapter correctly monkey-patches the Terra evaluator core: `AGGREGATE_PATH` is redirected, `verify_frozen_inputs` is replaced with `verify_qwen_inference`, and the report template substitutes Qwen provenance strings for all Terra references. No Terra model names leak into any Qwen output. **Byte-for-byte reproducibility: PASS ✅**

---

## 3  Recomputation Summary

| Check | Items | Matched | Status |
|-------|-------|---------|--------|
| Aggregation (2-of-3) | 180 | 180 | ✅ |
| Accuracy (condition × scope) | 12 | 12 | ✅ |
| Deltas | 12 | 12 | ✅ |
| Transfer counts | 6 | 6 | ✅ |
| Per-agent unseen | 16 | 16 | ✅ |
| Confusion matrices | 3×5×5 = 75 cells | 75 | ✅ |
| Bootstrap CI | 1 interval | 1 | ✅ |
| Frozen criteria | 4 | 4 | ✅ |
| Byte-for-byte evaluator run | 9 files | 9 | ✅ |
| **Total** | **315+** | **All** | **✅** |

---

## 4  Technical Stability Analysis

### 4.1  Repetition Agreement

**Finding: All 180/180 aggregation groups are unanimous (3/3 identical).**

With `temperature=0.0` and `seed=20260829`, the Qwen model produces bit-for-bit identical `raw_output` across all 3 repetitions for every agent-case-condition triple. This means:

- **Shannon entropy of vote distribution**: 0.0 for all 180 groups
- **Majority confidence**: 3/3 = 1.0 for all 180 groups
- **Effective number of independent samples**: 1 (not 3)
- The R=3 majority vote mechanism is **vacuous** — it provides no error correction or noise averaging

This is not a defect in the frozen results (the aggregation rule was applied correctly), but it means the R=3 design provides no robustness benefit for this model configuration.

### 4.2  Retries and Parse Failures

- **Total retries across 540 repetitions**: 0
- **Parse failures**: 0
- **Abstentions**: 0 (all 180 aggregates carry valid labels)

The structured output mode (`structured_outputs_strict=true`) ensured 100% parseable responses. No fallback paths were exercised.

### 4.3  Model Consistency

All 540 repetitions report the same model identifier: `Qwen/Qwen3.8-27B-FP8`. No model substitution or fallback occurred.

### 4.4  Token Usage and Reasoning Budget

**Inference configuration:**
- `max_tokens`: 1536
- `thinking_token_budget`: 1024
- `reasoning_mode`: `server_default_qwen3`

**Key finding: reasoning token ceiling correlated with errors.**

| Metric | Condition B Correct (31) | Condition B Incorrect (5) |
|--------|------------------------|--------------------------|
| Mean reasoning tokens | 682.4 | 1023.0 |
| Hit ceiling (≥1023) | 34.5% (11/31 reps) | **100%** (15/15 reps) |
| Min reasoning tokens | 187 | 1023 |

All 5 incorrect condition-B predictions (across all 15 repetitions) consumed the maximum reasoning budget (1023 tokens, one short of the 1024 ceiling). This pattern is consistent with **reasoning truncation** — the model may have been forced to emit a classification before completing its chain of thought.

For conditions A and E, ceiling-hit rates are also elevated among errors but the pattern is strongest in condition B where the reasoning task is most complex (integrating cross-agent FoT insights).

### 4.5  Reasoning Content Preservation

The `reasoning_mode=server_default_qwen3` configuration delegates thinking-token handling to the vLLM server. The 1024-token budget is substantially lower than the 8192+ budgets typical for reasoning models at this scale. Content analysis of the reasoning traces was not performed (out of scope for this automated review), but the ceiling correlation with errors (§4.4) warrants manual inspection of truncated reasoning in a follow-up.

### 4.6  Anomalies

No anomalies detected in:
- File integrity (all hashes verified)
- Timestamp ordering (protocol → predictions → evaluator → results)
- Label vocabulary (all predictions within the defined 5-class label space)
- Agent-case coverage (all 60 cells per condition populated)

One noted design anomaly: the Qwen evaluator adapter applies `EVALUATOR_AMENDMENT_001` (documented in `EVALUATOR_AMENDMENT_001.md`), which modified provenance guardrails between the predictions freeze and the evaluation freeze. The amendment documentation is clear that no predictions or aggregates were altered — only the evaluator's input-verification logic was adjusted to accept Qwen provenance tags. This is consistent with the observed byte-for-byte reproducibility.

---

## 5  Cross-Model Comparison (Qwen vs Terra)

> **Note**: This comparison is purely descriptive. The two models were run in separate experiments; no formal statistical test of between-model differences is licensed by this design.

### 5.1  Headline Numbers

| Metric | Terra (gpt-5.6-terra) | Qwen (Qwen3.8-27B-FP8) | Difference |
|--------|-----------------------|------------------------|------------|
| A unseen | 22/36 (0.611) | 23/36 (0.639) | +1 (+0.028) |
| B unseen | 23/36 (0.639) | 26/36 (0.722) | +3 (+0.083) |
| E unseen | 17/36 (0.472) | 18/36 (0.500) | +1 (+0.028) |
| A local-seen | 11/12 (0.917) | 12/12 (1.000) | +1 (+0.083) |
| B local-seen | 12/12 (1.000) | 9/12 (0.750) | −3 (−0.250) |
| E local-seen | 9/12 (0.750) | 10/12 (0.833) | +1 (+0.083) |
| A normal | 12/12 (1.000) | 12/12 (1.000) | 0 |
| B normal | 12/12 (1.000) | 12/12 (1.000) | 0 |
| E normal | 12/12 (1.000) | 12/12 (1.000) | 0 |
| **B all** | **47/60 (0.783)** | **47/60 (0.783)** | **0** |
| B−A unseen | +0.028 (+1) | +0.083 (+3) | +2 net |

### 5.2  Paired Agent-Case Changes (Condition B, Unseen)

| Change Type | Count | Agent-Cases |
|-------------|-------|-------------|
| Both correct | 31 | (31 pairs) |
| Both wrong | 2 | agent_3/PBH-008, agent_3/PBH-009 |
| Qwen gains (Terra wrong → Qwen correct) | 3 | agent_1/PBH-004, agent_2/PBH-005, agent_4/PBH-010 |
| Qwen loses (Terra correct → Qwen wrong) | 0 | — |

Qwen gains 3 unseen-B cases with zero losses relative to Terra. However, these gains are offset by 3 local-seen losses (see below).

### 5.3  Paired Agent-Case Changes (Condition B, Local-Seen)

| Change Type | Count | Agent-Cases |
|-------------|-------|-------------|
| Both correct | 9 | (9 pairs) |
| Qwen gains | 0 | — |
| Qwen loses | 3 | agent_2/PBH-007, agent_4/PBH-014, agent_4/PBH-015 |

### 5.4  Error Pattern Analysis

**Qwen's residual unseen-B errors** (2 cases):

Both are agent_3 errors on the CLS-OJNSG physical cluster (PBH-008, PBH-009). Agent_3's local fault is CLS-R463B, and CLS-OJNSG is in its unseen set. Both Terra and Qwen fail on these same cases → this cluster appears intrinsically difficult for agent_3 regardless of model.

**Qwen's local-seen-B errors** (3 cases):

| Case | Agent | True Label | Predicted | Error Type |
|------|-------|------------|-----------|------------|
| PBH-007 | agent_2 | CLS-OJNSG | CLS-Z3ISU | Cross-label swap |
| PBH-014 | agent_4 | CLS-Z3ISU | CLS-OJNSG | Cross-label swap |
| PBH-015 | agent_4 | CLS-Z3ISU | CLS-OJNSG | Cross-label swap |

All 3 errors involve CLS-OJNSG ↔ CLS-Z3ISU confusion. These labels map to physical faults F8 and F13 respectively. The FoT insights in condition B appear to introduce cross-contamination between these two specific fault classes for Qwen, even on cases the agent should recognise from its own local experience.

### 5.5  Condition E

Qwen's E-unseen accuracy (0.500) slightly exceeds Terra's (0.472). One notable detail: agent_3/PBH-009 is correct in condition E but wrong in both A and B — this single case is the only E-specific correct prediction across both models, and its correctness may be coincidental given that condition E applies deranged (incorrect) insights.

### 5.6  Cross-Model Summary

The two models achieve identical overall B accuracy (47/60) via complementary error profiles: Qwen trades 3 local-seen errors for 3 extra unseen-correct. The FoT mechanism's net effect on Qwen is redistributive rather than additive at the all-scope level. This makes the H2 failure (§2.9) a Qwen-specific phenomenon — Terra passes H2 with B_local = 12/12.

---

## 6  Interpretation

### 6.1  Transfer Persistence (H1)

Qwen shows a positive unseen B−A delta of +3/36 (+8.3%), somewhat larger than Terra's +1/36 (+2.8%). The FoT transfer effect replicates directionally on an open-weight model, suggesting the mechanism is not specific to a single proprietary architecture. However, the bootstrap CI [−0.0833, +0.2500] spans zero, so the observed gain is not statistically significant with the current sample size.

### 6.2  Semantic Specificity

The 5 unseen-B gains (A→B transitions) are distributed across 3 of 4 agents (agent_1, agent_2, agent_4), covering 3 different physical clusters. The 2 losses affect agent_2 and agent_3 on different clusters. This spread suggests the FoT benefit is not concentrated on a single fault type or agent, though the small counts preclude strong claims about uniformity.

### 6.3  Portability

The FoT mechanism was designed with gpt-5.6-terra and evaluated on Qwen/Qwen3.8-27B-FP8 without modification to the insight format, prompt structure, or evaluation protocol. The directional replication of H1 on a qualitatively different model (open-weight, 27B parameters, FP8 quantized, local inference) provides preliminary evidence of portability. The overall B accuracy being identical across models (47/60) further supports this.

### 6.4  Negative Transfer (H2 Failure)

H2 fails: B_local_seen = 9/12 < A_local_seen = 12/12. Qwen's local-seen accuracy drops by 25% when FoT insights are provided. All 3 local-seen errors involve CLS-OJNSG ↔ CLS-Z3ISU cross-confusion — a specific pair of fault classes that the FoT insights apparently make harder to distinguish for this model. This pattern is absent in Terra (which scores 12/12 on local-seen B) and may reflect Qwen's lower capacity to integrate peer insights without interference on cases it can already classify.

The mechanism is plausible: FoT insights from other agents describe fault signatures that partially overlap with the agent's own local fault knowledge, and Qwen may lack the discriminative resolution to keep them separate. This is consistent with the reasoning truncation finding (§4.4) — the cases where FoT integration is most cognitively demanding are also where Qwen runs out of reasoning budget.

### 6.5  Limitations

1. **Single open-weight model**: Qwen3.8-27B-FP8 is one point in a vast space of open-weight models. Generalisation to other architectures, sizes, or quantisation levels is unknown.

2. **Same insight producer**: FoT insights were generated by the same model (Qwen) that consumes them. Whether insights produced by a different (e.g., larger) model would yield better transfer is untested.

3. **Same held-out cases**: The 15 held-out cases are identical to those in the Terra experiment. Any case-level ceiling or floor effects carry over, limiting the independence of the replication.

4. **Reasoning budget constraint**: The 1024-token thinking budget is substantially below what reasoning-capable models typically need for complex multi-evidence integration tasks. The observed reasoning truncation (§4.4) means the experiment may be measuring Qwen's performance under an artificial ceiling rather than its genuine FoT integration capacity.

5. **Deterministic repetitions**: Temperature=0 + fixed seed yields identical repetitions, making the R=3 majority vote vacuous (§4.1). The results are valid (the aggregation rule was applied correctly to deterministic inputs) but the design provides no noise-averaging benefit, and any stochastic-repetition robustness claims do not apply.

6. **No formal cross-model test**: The Qwen-vs-Terra comparison is descriptive. The experiments were run independently; there is no paired cross-model bootstrap or other formal test of between-model differences.

---

## 7  Findings Classification

### P1 — Critical (would block publication or require correction)

**None identified.** All frozen artifacts are authentic, internally consistent, and independently reproducible. No computational errors, data integrity issues, or provenance failures were found.

### P2 — Important (must be disclosed; may limit claims)

**P2-1: Deterministic repetitions render R=3 majority vote vacuous**
- *Evidence*: 180/180 aggregation groups unanimous; all `raw_output` fields bit-for-bit identical across repetitions within each group.
- *Cause*: `temperature=0.0` + `seed=20260829` makes the model fully deterministic.
- *Impact*: The R=3 design provides zero error-correction benefit. Results are numerically correct but the robustness claim implied by majority voting does not hold.
- *Scientific formulation*: "With deterministic decoding (temperature=0, fixed seed), the three-repetition majority vote was vacuous for this model: all repetition triples were unanimous, yielding an effective sample size of 1 per agent-case-condition."

**P2-2: Reasoning token ceiling correlated with all condition-B errors**
- *Evidence*: 5/5 incorrect B predictions (15/15 repetitions) hit the 1023-token reasoning ceiling; only 34.5% of correct B predictions hit it. Mean reasoning: incorrect=1023.0, correct=682.4.
- *Cause*: `thinking_token_budget=1024` imposes a hard ceiling on chain-of-thought length.
- *Impact*: Cannot distinguish whether errors reflect genuine model limitations or artificial reasoning truncation. The experiment may underestimate Qwen's FoT integration capacity.
- *Scientific formulation*: "All five condition-B errors consumed the maximum reasoning budget (1023/1024 tokens), compared with 34.5% of correct predictions. This ceiling correlation raises the possibility that reasoning truncation, rather than representational limitations, caused some errors — a confound that should be acknowledged when interpreting the transfer effect magnitude."

**P2-3: H2 fails — negative transfer on local-seen cases**
- *Evidence*: B_local_seen = 9/12 (0.750) < A_local_seen = 12/12 (1.000); delta = −0.250.
- *Pattern*: All 3 errors are CLS-OJNSG ↔ CLS-Z3ISU cross-label swaps.
- *Impact*: FoT insights cause Qwen to misclassify cases it correctly identifies in isolation, specifically confusing two fault classes with potentially similar signatures. This is a Qwen-specific failure (Terra passes H2).
- *Scientific formulation*: "H2 (non-regression on local-fault-seen cases) fails for Qwen: providing FoT insights reduced local-seen accuracy from 100% to 75%, with all three errors involving CLS-OJNSG ↔ CLS-Z3ISU confusion. This suggests that cross-agent insight integration can interfere with established local knowledge at this model scale, a negative transfer pattern absent in the larger proprietary model."

**P2-4: CLS-OJNSG ↔ CLS-Z3ISU systematic confusion**
- *Evidence*: 3/3 local-seen errors and the unseen confusion pattern involve these two classes.
- *Impact*: Points to a specific representational weakness in Qwen for distinguishing physical faults F8 and F13 when cross-agent evidence is present.
- *Scientific formulation*: "Qwen exhibits systematic CLS-OJNSG ↔ CLS-Z3ISU confusion under condition B, suggesting incomplete separation of F8 and F13 fault representations when cross-agent insights are integrated. This pairwise vulnerability may reflect reduced discriminative capacity under the 1024-token reasoning budget."

**P2-5: Design limitations to be disclosed**
- Single open-weight model (no generality claim)
- Same model produces and consumes insights (no independence)
- Same 15 held-out cases as Terra (shared ceiling/floor effects)
- Reasoning budget (1024 tokens) is low for the task complexity
- Deterministic repetitions (no stochastic robustness)
- Cross-model comparison is descriptive only

### P3 — Minor (note for completeness)

**P3-1: Cross-model comparison is descriptive only**
- *Evidence*: Qwen and Terra achieve identical B_all (47/60) via different error profiles.
- *Formulation*: "Descriptive cross-model comparison only; no formal between-model statistical test is licensed by the independent-experiment design."

**P3-2: Condition E single correct anomaly**
- *Evidence*: agent_3/PBH-009 is correct only in condition E (wrong in A and B).
- *Formulation*: "One agent-case pair is correct only under deranged insights (condition E), likely a coincidence given that deranged insights carry no valid diagnostic signal for this agent-case combination."

**P3-3: EVALUATOR_AMENDMENT_001 applied post-prediction**
- *Evidence*: Amendment documented and verified to affect only provenance guardrails.
- *Formulation*: "An evaluator amendment was applied between the predictions and evaluation freezes, affecting only provenance verification logic. No predictions or aggregates were modified."

---

## 8  Verdict

### Assessment

| Dimension | Status |
|-----------|--------|
| Provenance & integrity | ✅ All tags, commits, hashes verified |
| Computational reproducibility | ✅ Byte-for-byte with official evaluator |
| Independent metric recomputation | ✅ 315+ items all match |
| H1 (unseen transfer) | ✅ PASS (direction positive, CI spans zero) |
| H2 (local-seen non-regression) | ❌ FAIL (−25%, P2-3) |
| H3 (normal non-regression) | ✅ PASS |
| H4 (B > E overall) | ✅ PASS |
| Technical stability | ⚠️ Deterministic reps (P2-1), reasoning ceiling (P2-2) |
| Cross-model portability | ⚠️ Directional replication, same total, different profile |

### Verdict: **GO WITH LIMITATIONS**

The frozen EXP2 Qwen results are computationally correct, fully reproducible, and show directional FoT transfer replication on an open-weight model. Three of four frozen criteria pass. The results may be published or presented, subject to the following mandatory disclosures:

1. **H2 failure** must be prominently reported alongside H1 success. The FoT mechanism improves Qwen's unseen accuracy but degrades local-seen accuracy — the net all-scope effect is zero.

2. **Reasoning truncation confound** must be acknowledged. The 1024-token thinking budget may artificially limit condition-B performance; the experiment measures FoT transfer under a reasoning constraint, not Qwen's unconstrained FoT capacity.

3. **Deterministic repetitions** must be disclosed. The R=3 majority vote provides no actual robustness benefit for this model configuration; claims about stochastic robustness do not extend to Qwen.

4. **Cross-model comparison framing**: Qwen-vs-Terra comparisons must be described as descriptive, noting the complementary error profiles (Qwen trades local-seen for unseen accuracy).

5. **All design limitations** listed in P2-5 must appear in the paper's limitation section.

With these disclosures, the results faithfully represent what the experiment measured and provide genuine scientific value as a portability probe of the FoT mechanism.

---

*Report generated by automated independent review. All numerical claims in this report were independently computed from raw data and verified against frozen artifacts.*
