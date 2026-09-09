# EXP2 Qwen — Independent Results Review (R2)

**Review ID:** R2 (from scratch)
**Date:** 2026-09-09
**Reviewed repository:** `/home/luca/fot-phd` (server working copy)
**Branch / HEAD at review time:** `codex/exp2-qwen` @ `37195cf2c5076b5da724b857f10e157177654cac`
**Report location (outside the repository):** `/home/luca/fot-exp2/reviews/EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW_R2.md`
**Scratch area:** `/tmp/exp2qwen_r2/` (all scripts, venv, isolated clone)

## Rules of engagement observed

- The repository was **not modified**: no file written, no commit, no tag, no branch. `git status --porcelain` was empty before and after the review, and the nine frozen outputs still match their canonical SHA-256.
- **No LLM / vLLM experimental calls** were made. No inference was executed. Only frozen artifacts on disk were read.
- The earlier review file `Claude outputs/EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW.md` was **never opened**, and no number, framing, or conclusion from it appears here. Every figure below was re-derived from the frozen records in this session.
- All scripts live under `/tmp/exp2qwen_r2/`. The official evaluator re-run was performed inside a **throwaway clone** at `/tmp/exp2qwen_r2/repo`, with a hard runtime guard that aborts on any write under `/home/luca/fot-phd`.
- Environment note: no Python with `numpy` existed on the machine; a disposable venv was created at `/tmp/exp2qwen_r2/venv` (`numpy 2.5.3`, `pytest`). Nothing was installed into the repository or into a shared environment.

---

# FASE 0 — Identity gate

## 0.1 Tag dereference

```bash
cd /home/luca/fot-phd
for t in phase-b-exp2-qwen-protocol-frozen-001 \
         phase-b-exp2-qwen-predictions-frozen-001 \
         phase-b-exp2-qwen-evaluator-frozen-001 \
         phase-b-exp2-qwen-results-frozen-001; do
  printf '%-50s %s\n' "$t" "$(git rev-parse "$t^{}")"
done
```

| Tag | Expected | Observed | Verdict |
|---|---|---|---|
| `phase-b-exp2-qwen-protocol-frozen-001^{}` | `d9bb95c31bdeb2f1608aaedc52f25b98de9bbf96` | `d9bb95c31bdeb2f1608aaedc52f25b98de9bbf96` | ✅ |
| `phase-b-exp2-qwen-predictions-frozen-001^{}` | `a4f264c210873536c989ebd99aa2c6cf9857c85c` | `a4f264c210873536c989ebd99aa2c6cf9857c85c` | ✅ |
| `phase-b-exp2-qwen-evaluator-frozen-001^{}` | `a8f9884dfe2150a89131ba604b34ff1f6914f6e9` | `a8f9884dfe2150a89131ba604b34ff1f6914f6e9` | ✅ |
| `phase-b-exp2-qwen-results-frozen-001^{}` | `37195cf2c5076b5da724b857f10e157177654cac` | `37195cf2c5076b5da724b857f10e157177654cac` | ✅ |

**4/4 match.**

## 0.2 Output set carried by the results tag

```bash
git diff --name-status phase-b-exp2-qwen-evaluator-frozen-001^{} \
                       phase-b-exp2-qwen-results-frozen-001^{}
git ls-tree -r --name-only phase-b-exp2-qwen-results-frozen-001^{} \
  -- phase_b/exp2/qwen/evaluation/
```

The results commit adds **exactly nine files**, all under `phase_b/exp2/qwen/evaluation/`, and touches nothing else:

`EVALUATION_REPORT.md`, `bootstrap_results.json`, `confusion_matrices.json`, `evaluation_hash_manifest.json`, `evaluation_results.json`, `per_agent_metrics.csv`, `primary_metrics.csv`, `secondary_metrics.csv`, `transfer_counts.csv`.

Forbidden-name scan over the whole tag tree — **no hits**, so this is not the wrong artefact family:

```bash
git ls-tree -r --name-only phase-b-exp2-qwen-results-frozen-001^{} \
  | grep -E 'exp2_qwen_results\.(json|csv)|frozen_criteria\.json|exp2_qwen_confusion_A\.csv'
# → NONE FOUND
```

**9/9 expected names present, 0/4 forbidden names present.**

## 0.3 Canonical SHA-256

Computed both from the tag blobs and from the working tree.

```bash
git cat-file blob phase-b-exp2-qwen-results-frozen-001^{}:phase_b/exp2/qwen/evaluation/<file> | sha256sum
cd /home/luca/fot-phd/phase_b/exp2/qwen/evaluation && sha256sum -c /tmp/expected_sha.txt
```

| Artefact | SHA-256 (observed = expected) | Verdict |
|---|---|---|
| `EVALUATION_REPORT.md` | `0c6f2b3d795961a660ff659ce5cb31620209d126d92bed11aea265587a436ba9` | ✅ |
| `bootstrap_results.json` | `d421a30aea4a29aee9b30ec99d31dc97ea637322a7c16cc29ba4981ac0d3a9c2` | ✅ |
| `confusion_matrices.json` | `c3b0beaf56ca2f455e0ed80e56dcaba5bad67e95ac74cfb2322679f0ef936061` | ✅ |
| `evaluation_hash_manifest.json` | `d9f18d8804b8528c58029736b276356f0a34c59af69f27034eeab2f971472732` | ✅ |
| `evaluation_results.json` | `5d499d63ff771343c402fc3ecc03b93862ae2cfb9719b231b985077c1e2257d3` | ✅ |
| `per_agent_metrics.csv` | `842afff50b87d571ab6698e81b2791fbd30e4e4e775ef1c8dfb43f6ee9b993a8` | ✅ |
| `primary_metrics.csv` | `89d1e52ec146d98d6bf45ab9b692a272e091cf08200fbd0966ed379d841b1d8e` | ✅ |
| `secondary_metrics.csv` | `32d395f379c3c5d86a295705037aab53049e45c4887277cf35105f74d6462ca1` | ✅ |
| `transfer_counts.csv` | `8c95d3141acdd99317f36c2c3d650cecf2ac9c8992f893325d4ce73b571eb4a2` | ✅ |

**9/9 canonical hashes match, tag blobs and working tree agree.**

## 0.4 Sentinel check, read directly from `evaluation_results.json`

Script: `/tmp/exp2qwen_r2/` (inline, reading `phase_b/exp2/qwen/evaluation/evaluation_results.json`).

| Sentinel | Required | Observed | Verdict |
|---|---|---|---|
| A unseen | 0/36 | `condition_metrics.A.unseen` = 0/36 | ✅ |
| B unseen | 34/36 | `condition_metrics.B.unseen` = 34/36 | ✅ |
| E unseen | 1/36 | `condition_metrics.E.unseen` = 1/36 | ✅ |
| B local-seen | 9/12 | `condition_metrics.B.local_fault_seen` = 9/12 | ✅ |
| B overall | 55/60 | `condition_metrics.B.overall` = 55/60 | ✅ |
| C1 | PASS | `C1_delta_unseen_gt_0` = true | ✅ |
| C2 | PASS | `C2_positive_delta_at_least_3_of_4_agents` = true | ✅ |
| C3 | PASS | `C3_helped_gt_harmed` = true | ✅ |
| C4 | PASS | `C4_delta_unseen_gt_delta_E` = true | ✅ |
| C1–C4 tally | 4/4 | `primary_support_criteria_satisfied` = 4 / `_total` = 4 | ✅ |
| H2 local-seen non-regression | FAIL | `H2_local_fault_seen_B_ge_A_epsilon_0` = false | ✅ |

**11/11 sentinels match.**

## FASE 0 verdict

> **IDENTITY GATE: PASS.** Tags 4/4, output set 9/9 with 0 forbidden names, SHA-256 9/9, sentinels 11/11. This is the correct frozen artefact set. Phase 1 proceeds.

## 0.5 Supporting provenance (verified in addition to the mandated gate)

- Upstream inputs match the hashes the evaluator declares as canonical:
  `aggregate_records.jsonl` = `73ace466…f9e0a`, `execution_metadata.json` = `7ec4719d…2468e`, `repetition_records.jsonl` = `20fdc8e3…72198`;
  `pseudolabel_mapping.json` = `f68a690d…8b3035`, `phase_b_heldout_manifest.csv` = `610c8a5f…b450a3` — all equal to the values recorded inside `evaluation_results.json.reproducibility`.
- Freeze chain is strictly linear and correctly ordered (`git merge-base --is-ancestor`):
  protocol `d9bb95c` → predictions `a4f264c` → evaluator `a8f9884` → results `37195cf`.
- The evaluator-freeze commit touches **only** `evaluate_qwen.py`, `EVALUATOR_AMENDMENT_001.md` and a provenance test — it does **not** touch any inference artefact. The reasoning/extraction fix (`d9bb95c`) precedes the predictions freeze, so it could not have been applied after seeing outcomes.

---

# FASE 1 — Independent review

## 1. Recomputation of the 180 aggregates from the 540 repetition records

Script: `/tmp/exp2qwen_r2/independent_recompute.py` — a standalone re-implementation that **imports nothing from the repository**. It re-derives the aggregation rule `frozen_valid_label_majority_2_of_3_else_abstain` from the protocol definition and re-runs it over `phase_b/exp2/qwen/inference/repetition_records.jsonl`.

```bash
/tmp/exp2qwen_r2/venv/bin/python /tmp/exp2qwen_r2/independent_recompute.py > /tmp/exp2qwen_r2/recompute.json
```

| Check | Result |
|---|---|
| Repetition records read | 540 |
| Distinct (agent, condition, case) groups | 180 |
| Groups with repetitions exactly {1,2,3} | 180/180 |
| Groups with a single consistent `input_hash` | 180/180 |
| Aggregates recomputed | 180 |
| Aggregates differing from frozen `aggregate_records.jsonl` | **0** |
| Canonical-JSON identity of the whole recomputed file | **True** |

**The 540 → 180 aggregation reproduces exactly, field for field and record for record.**

## 2. Recomputation of metrics, transfer counts, per-agent results, confusion matrices, bootstrap

Same script, independent ground-truth join from `phase_b/heldout/phase_b_heldout_manifest.csv` + `phase_b/config/evaluator_side/pseudolabel_mapping.json` (15 cases, 3 runs × 5 classes, unique mapping).

### Condition metrics (correct / n) — recomputed

| Condition | unseen | local-fault-seen | normal | overall |
|---|---:|---:|---:|---:|
| A | 0/36 | 12/12 | 12/12 | 24/60 |
| B | **34/36** | **9/12** | 12/12 | **55/60** |
| E | 1/36 | 12/12 | 12/12 | 25/60 |

Abstentions: **0** in every condition and every stratum.

### Primary scalars — recomputed

| Quantity | Value |
|---|---|
| `delta_unseen_B_minus_A` | 0.944444444444 |
| `delta_E_E_minus_A` | 0.027777777778 |
| `delta_specificity_B_minus_E` | 0.916666666667 |
| `positive_delta_agents` | 4 |
| `local_fault_seen_B_minus_A` | **−0.25** |
| `normal_B_minus_A` | 0.0 |
| `overall_B_minus_A` | 0.516666666667 |

### Transfer counts (paired B vs A, 36 unseen pairs) — recomputed

`n_pairs` 36 · **helped 34** · **harmed 0** · unchanged 2 (correct 0, incorrect 2).

### Per-agent primary — recomputed

| Agent | n | A | B | E | Δ B−A |
|---|---:|---:|---:|---:|---:|
| agent_1 | 9 | 0.000 | 1.000 | 0.000 | 1.000 |
| agent_2 | 9 | 0.000 | 1.000 | 0.000 | 1.000 |
| agent_3 | 9 | 0.000 | 0.778 | 0.111 | 0.778 |
| agent_4 | 9 | 0.000 | 1.000 | 0.000 | 1.000 |

### Confusion matrices — recomputed (fault truths; `Normal` is 12/12 everywhere)

| truth | A | B | E |
|---|---|---|---|
| CLS-ZOGAA | ZOGAA 3, OJNSG 3, R463B 3, Z3ISU 3 | **ZOGAA 12** | ZOGAA 3, OJNSG 6, R463B 3 |
| CLS-OJNSG | ZOGAA 3, OJNSG 3, R463B 3, Z3ISU 3 | **OJNSG 9**, Z3ISU 2, ZOGAA 1 | R463B 6, OJNSG 4, ZOGAA 1, Z3ISU 1 |
| CLS-R463B | ZOGAA 3, OJNSG 3, R463B 3, Z3ISU 3 | **R463B 12** | Z3ISU 6, R463B 3, ZOGAA 3 |
| CLS-Z3ISU | ZOGAA 3, OJNSG 3, R463B 3, Z3ISU 3 | **Z3ISU 10**, OJNSG 2 | ZOGAA 6, OJNSG 3, Z3ISU 3 |

### Bootstrap — recomputed independently (10 000 draws, seed 20260829, 4 strata × 3 clusters)

| Statistic | Point estimate | 95% CI |
|---|---|---|
| `delta_unseen_B_minus_A` | 0.944444444444 | [0.916666666667, 1.0] |
| `delta_specificity_B_minus_E` | 0.916666666667 | [0.833333333333, 1.0] |

**Every recomputed quantity — including both bootstrap intervals to full float precision — equals the frozen value.**

## 3. Re-execution of the official evaluator and byte-for-byte verification

The evaluator embeds `ROOT`-relative paths in its hash manifest, so a faithful re-run requires a real repository root. It was therefore run inside an **isolated clone**, never in the server repo:

```bash
git clone --no-hardlinks /home/luca/fot-phd /tmp/exp2qwen_r2/repo
cd /tmp/exp2qwen_r2/repo && git checkout codex/exp2-qwen     # HEAD 37195cf, tags carried over
/tmp/exp2qwen_r2/venv/bin/python /tmp/exp2qwen_r2/rerun_official_evaluator.py
```

The harness deletes `phase_b/exp2/qwen/evaluation/` **in the clone only**, imports `phase_b.exp2.qwen.evaluate_qwen` from the clone, asserts `eq.ROOT == clone`, monkey-patches `write_if_identical_or_absent` with a guard that raises on any path under `/home/luca/fot-phd`, and then calls `evaluate()`.

Evaluator return payload: `{"integrity": "PASS", "physical_clusters": 12, "primary_n_per_condition": 36}`.
Artefacts produced: exactly the nine expected names.

| Artefact | Regenerated SHA-256 | vs frozen |
|---|---|---|
| `EVALUATION_REPORT.md` | `0c6f2b3d…36ba9` (2511 B) | **IDENTICAL** |
| `bootstrap_results.json` | `d421a30a…d3a9c2` (712 B) | **IDENTICAL** |
| `confusion_matrices.json` | `c3b0beaf…f936061` (2865 B) | **IDENTICAL** |
| `evaluation_hash_manifest.json` | `d9f18d88…472732` (1937 B) | **IDENTICAL** |
| `evaluation_results.json` | `5d499d63…257d3` (8220 B) | **IDENTICAL** |
| `per_agent_metrics.csv` | `842afff5…b993a8` (216 B) | **IDENTICAL** |
| `primary_metrics.csv` | `89d1e52e…41d1b8` (141 B) | **IDENTICAL** |
| `secondary_metrics.csv` | `32d395f3…6462a1` (351 B) | **IDENTICAL** |
| `transfer_counts.csv` | `8c95d314…73eb4a2` (117 B) | **IDENTICAL** |

> **BYTE-FOR-BYTE REPRODUCTION: PASS (9/9).** The server repository was untouched; the guard never fired.

Lane test suite, run in the clone (`pytest phase_b/exp2/qwen/tests`, excluding `test_adapter.py` which needs the `openai` package, not installed since no LLM calls were permitted): **19 passed, 90 subtests passed, 1 failed**. The single failure is `test_probe_artifact.py::test_complete_experiment_outputs_do_not_exist`, a *pre-inference* guard asserting that `inference/repetition_records.jsonl` does **not** exist. It is stale by construction after the run and carries no bearing on the results; it is a housekeeping item, not a defect.

## 4. Criteria verified separately

### 4.1 The four primary support criteria (C1–C4)

Each recomputed from my own aggregates and metrics, not read from the frozen file:

| Criterion | Definition | Recomputed evidence | Verdict |
|---|---|---|---|
| **C1** | Δ_unseen(B−A) > 0 | 0.944444 > 0 | **PASS** |
| **C2** | positive Δ in ≥ 3 of 4 agents | 4 of 4 agents strictly positive (1.0, 1.0, 0.778, 1.0) | **PASS** |
| **C3** | helped > harmed | 34 > 0 | **PASS** |
| **C4** | Δ_unseen > Δ_E | 0.944444 > 0.027778 | **PASS** |

**C1–C4 = 4/4 PASS**, independently confirmed.

### 4.2 H2 — a *separate secondary* check, not one of the four primary criteria

H2 is `local_fault_seen` accuracy in B ≥ accuracy in A, with ε = 0. It is deliberately **excluded** from `primary_support_criteria_satisfied` (which sums only C1–C4 and totals 4), and it sits under `secondary` in the results schema.

| | A | B | Δ | ε | Verdict |
|---|---:|---:|---:|---:|---|
| local-fault-seen | 12/12 = 1.000 | 9/12 = 0.750 | **−0.250** | 0.0 | **FAIL** |

**H2 = FAIL**, independently confirmed, and correctly classified as secondary. The "4/4 PASS" headline and the H2 failure are **not in tension**: they measure different things (transfer to unseen faults vs. non-regression on the agent's own already-known fault).

## 5. Comparison with Terra — frozen results only

Read from `phase_b/final_evaluation/evaluation_results.json` (`6fcc9719…f60d38`) and `phase_b/final_evaluation/inference/aggregate_records.jsonl`. The three anchors supplied for this review were verified against those files and are correct.

| Quantity | Terra (frozen) | Qwen (frozen) |
|---|---|---|
| A unseen | 0/36 ✓ | 0/36 |
| B unseen | 31/36 ✓ | **34/36** |
| E unseen | 3/36 ✓ | **1/36** |
| B local-fault-seen | 12/12 ✓ | **9/12** |
| B overall | 55/60 ✓ | 55/60 |
| Δ_unseen (B−A) | 0.861111 | **0.944444** |
| Δ_unseen 95% CI | [0.833333, 0.916667] | [0.916667, 1.000000] |
| Δ_specificity (B−E) | 0.777778 | **0.916667** |
| helped / harmed | 31 / 0 | 34 / 0 |
| positive-Δ agents | 4/4 | 4/4 |
| C1–C4 | 4/4 PASS | 4/4 PASS |
| **H2** | **PASS** (Δ = 0.0) | **FAIL** (Δ = −0.25) |
| Abstentions | 14 (all in A unseen) | **0** |

Reading:

- **The primary effect replicates on a second, independent consumer, and is somewhat larger.** Qwen's Δ_unseen point estimate (0.944) lies above Terra's upper CI bound (0.917), and the two CIs touch only at that boundary. Direction, sign, unanimity across agents, and the zero-harm transfer profile all agree.
- **B overall = 55/60 in both lanes is a coincidence of totals, not of structure.** Terra: 31 unseen + 12 local-seen + 12 normal. Qwen: 34 unseen + 9 local-seen + 12 normal. Qwen buys 3 extra unseen successes and loses exactly 3 local-seen ones. Quoting "55/60 in both" as agreement would be misleading.
- **The lanes diverge precisely on H2**, and only there.
- **The condition-A floors are reached by different mechanisms.** In Qwen, condition A is a *fully degenerate constant classifier*: on all 48 fault rows each agent emits its own `local_fault_label`, with zero deviations. In Terra, A deviates from the own-label response in 14 of 48 rows and produces 14 abstentions. Both floors are 0/36, so Δ_unseen is comparable as a number, but the baseline is not the same object in the two lanes, and in neither lane is it a chance-level baseline.

## 6. Recomputation from the raw records

All figures below come from `phase_b/exp2/qwen/inference/repetition_records.jsonl` (540 records) via `/tmp/exp2qwen_r2/independent_recompute.py` and follow-up inline analyses.

### 6.1 R = 3 agreement

| Metric | Value |
|---|---|
| Aggregates with unanimous 3/3 valid-label agreement | **180 / 180** |
| Aggregates decided by a 2/3 majority | 0 |
| Aggregates with no majority (→ abstain) | 0 |
| Per condition (A / B / E) | 60/60, 60/60, 60/60 unanimous |

**This unanimity is an artefact of deterministic decoding, not evidence of stability.** In all 180 groups the three repetitions are **byte-identical** in `raw_output`, and identical in `completion_tokens`. Configuration is uniform: `temperature = 0.0`, `seed = 20260829`, `stateless = true`, `previous_response_id_used = false`, single model revision `017b9c7a…`. The lane's own capability probe records `deterministic_replay: True`, consistent with this.

Consequence: **R = 3 contributes no replication variance in the Qwen lane.** For contrast, Terra's frozen aggregates show 154 unanimous, 12 majority-2/3 and 14 no-majority — there, R = 3 did real work. Uncertainty in the Qwen lane rests entirely on the 12-physical-cluster bootstrap, which remains valid, but the "3/3 unanimous everywhere" figure must not be reported as a robustness result.

### 6.2 Retries and parse failures

| Metric | Value |
|---|---|
| `retry_count` | 0 in all 540 records |
| `max_structural_retries` configured | 2 (never consumed) |
| `parse_failure = true` | **0 / 540** |
| Repetition outcomes marked `parse_failure` | 0 |
| Non-empty `structural_validation_errors` | 0 |
| Provider attempts per record | exactly 1 in all 540 |
| `finish_reason` | `stop` in 540/540; `length` in 0 |
| Repetition-level abstentions | 0 |
| `structured_outputs_strict` | true in 540/540 |

**Structured-output extraction is clean end to end: no retry, no parse failure, no abstention, no output truncation.**

### 6.3 Reasoning token usage

Token accounting from `provider_attempts[0].usage_raw.completion_tokens_details`.

| Metric | A | B | E | All |
|---|---:|---:|---:|---:|
| `prompt_tokens` mean | 1595.6 | 2339.1 | 2339.1 | — |
| `completion_tokens` mean | 565.4 | 837.2 | 839.9 | 747.5 |
| `reasoning_tokens` mean | 465.8 | 710.2 | 712.6 | 629.5 |
| `reasoning_tokens` median | 272.5 | 769.0 | 841.0 | 561.5 |
| `reasoning_tokens` max | 1023 | 1023 | 1023 | **1023** |

- Output (non-reasoning) tokens are small and stable: min 74, median 117, max 177.
- `max_tokens` = 1536 for all 540 calls; the largest observed `completion_tokens` is 1200, leaving 336 tokens of headroom. **The 1536 output ceiling is never reached** — consistent with `finish_reason = stop` throughout and with the probe's `no_length_truncation: PASS`.
- **B and E are matched on budget.** Identical prompt-token distributions (mean 2339.1 for both) and near-identical reasoning-token means (710.2 vs 712.6). The B−E contrast is therefore *not* confounded by compute.
- A uses materially less prompt and reasoning budget than B/E, because condition A carries no peer insights. The B−A contrast is *not* budget-matched.

### 6.4 Ceiling incidence on correct and incorrect cases

The declared `thinking_token_budget` is 1024, but the **effective hard cap is 1023 reasoning tokens**: 195 of 540 records sit at exactly 1023 and none exceed it. This cap does **not** raise `finish_reason = length` and is invisible to the probe's `no_length_truncation` gate, which only concerns the 1536 output limit. The two must not be conflated.

Repetition-level incidence at the 1023 cap:

| Slice | Correct at cap | Incorrect at cap |
|---|---|---|
| All 540 | 87/312 (27.9%) | 108/228 (47.4%) |
| Condition A | 0/72 (0.0%) | 45/108 (41.7%) |
| **Condition B** | 57/165 (34.5%) | **15/15 (100.0%)** |
| Condition E | 30/75 (40.0%) | 48/105 (45.7%) |
| B unseen | 39/102 (38.2%) | **6/6 (100.0%)** |
| B local-seen | 18/27 (66.7%) | **9/9 (100.0%)** |
| Normal rows | 0/108 | 0/0 |

Aggregate level in condition B (capping is all-or-none per aggregate, since the three repetitions are byte-identical):

| B aggregates | n | correct | wrong |
|---|---:|---:|---:|
| all 3 repetitions at the 1023 cap | 24 | 19 | **5** |
| below the cap | 36 | **36** | **0** |

**Every single error B makes — all 5 aggregates, all 15 underlying repetitions — occurs at the reasoning cap. Not one of the 36 uncapped B aggregates is wrong.** Reaching the cap is thus a *necessary* condition for B error in this dataset, though not a sufficient one (19 of 24 capped aggregates are still correct). Condition-A and E comparisons: A at-cap error rate 100% vs 46.7% below; E 61.5% vs 55.9% below.

### 6.5 CLS-OJNSG / CLS-Z3ISU pattern

Recall by pseudolabel (12 agent-case observations per label per condition):

| Label | A | B | E |
|---|---:|---:|---:|
| CLS-ZOGAA | 3/12 | **12/12** | 3/12 |
| CLS-R463B | 3/12 | **12/12** | 3/12 |
| **CLS-OJNSG** | 3/12 | **9/12** | 4/12 |
| **CLS-Z3ISU** | 3/12 | **10/12** | 3/12 |

All five B errors, enumerated:

| Agent | Case | Truth | Scope | Predicted | 3 repetitions |
|---|---|---|---|---|---|
| agent_2 | PBH-007 | CLS-OJNSG | **local-seen** | CLS-Z3ISU | Z3ISU ×3 |
| agent_3 | PBH-008 | CLS-OJNSG | unseen | CLS-Z3ISU | Z3ISU ×3 |
| agent_3 | PBH-009 | CLS-OJNSG | unseen | CLS-ZOGAA | ZOGAA ×3 |
| agent_4 | PBH-014 | CLS-Z3ISU | **local-seen** | CLS-OJNSG | OJNSG ×3 |
| agent_4 | PBH-015 | CLS-Z3ISU | **local-seen** | CLS-OJNSG | OJNSG ×3 |

Findings:

- **B's residual error is entirely confined to the {CLS-OJNSG, CLS-Z3ISU} pair.** CLS-ZOGAA and CLS-R463B are perfect (12/12) in condition B. Every error has a truth label in that pair, and 4 of the 5 predict the *other* member of the pair — a bidirectional OJNSG ↔ Z3ISU confusion.
- **The confusion is what drives the H2 failure.** All three local-seen losses are cases where an agent abandoned its *own* known fault label in favour of the paired one: agent_2 (owner of CLS-OJNSG) answered CLS-Z3ISU; agent_4 (owner of CLS-Z3ISU) answered CLS-OJNSG twice. This is a symmetric, content-specific interference, not diffuse degradation.
- **CLS-OJNSG is the hardest class in both lanes.** Terra's five B errors are *all* on truth CLS-OJNSG. Qwen's errors also centre on it (3 of 5, plus 2 predicting it). The lanes differ on CLS-Z3ISU: Terra B = 12/12, Qwen B = 10/12.
- The single E unseen success is agent_3 on PBH-009 (CLS-OJNSG) — a lone hit against a corrupted mapping, consistent with noise.
- Condition E's error structure is a coherent derangement at the population level (modal mapping ZOGAA→OJNSG, OJNSG→R463B, R463B→Z3ISU, Z3ISU→ZOGAA, 6/12 each), confirming the corrupted condition behaves as designed rather than as random noise.

### 6.6 Insight citation — a control on the specificity claim

| Condition | Insights offered | Unseen repetitions citing ≥ 1 insight | Unseen accuracy |
|---|---|---|---|
| A | 0 (0/180 records) | n/a | 0/108 |
| B | 6 (180/180 records) | **108/108 (100%)** | **102/108** |
| E | 6 (180/180 records) | **108/108 (100%)** | 3/108 |

B and E agents consume the offered insights at an identical 100% rate, with matched prompt length and matched reasoning budget, yet differ by 0.917 in unseen accuracy. **The effect tracks the *correctness* of insight content, not its presence, its length, or the agent's willingness to use it.** This is the strongest single piece of evidence in the dataset.

## 7. Independence statement

No number, table, or conclusion in this report derives from the invalidated review. Every quantity was recomputed in this session from the frozen records, using a standalone implementation that imports nothing from the repository, and was then cross-checked against a faithful re-run of the official evaluator in an isolated clone.

## 8. Distinctions the results require

The four findings below must be kept separate; collapsing them would misstate what this experiment shows.

### 8.1 Persistence of unseen transfer — **strongly supported**

B reaches 34/36 on locally unseen faults against a floor of 0/36, Δ = 0.944, bootstrap 95% CI [0.917, 1.000] over 12 independent physical clusters. All 4 agents are positive, 34 pairs helped, **0 harmed**. Two of the four fault classes are perfect. The effect replicates Terra's direction and magnitude on an independent consumer and is, if anything, larger. This conclusion is robust to every reservation raised below.

### 8.2 B−E specificity — **strongly supported and well controlled**

Δ_specificity = 0.917, CI [0.833, 1.000]. B and E are matched on prompt length, on reasoning-token consumption, and on insight-citation rate (100% in both). The only difference is whether the peer insights are truthful. E performs at 1/36, *below* even a naive floor, and its errors follow the intended derangement structure. This rules out the "any extra context helps" explanation cleanly. It is a separate claim from 8.1 and it stands on its own.

### 8.3 H2 local-seen failure — **real, secondary, and mechanistically narrow**

B loses 3 of 12 local-seen cases that A gets right (Δ = −0.25); Terra showed no such regression (Δ = 0.0). This is a genuine divergence between the two consumers and must not be waved away. Three qualifications matter:

- It is a **secondary** check, deliberately outside the C1–C4 primary set. "4/4 PASS" and "H2 FAIL" are both true and describe different questions.
- The A reference is **not informative** in the Qwen lane: A's 12/12 on local-seen is obtained by a degenerate constant classifier that answers its own label on every fault case, and so scores 12/12 for free while scoring 0/36 on unseen. Measuring regression against that reference overstates what A "knew".
- The mechanism is narrow and specific: all three losses are OJNSG ↔ Z3ISU substitutions (§6.5), not broad erosion.

Even with those qualifications, the finding stands: peer insights caused this consumer to abandon correct local knowledge in 3 of 12 cases. That is a real cost, and it should be reported as such.

### 8.4 Reasoning-budget confounding — **present, material, unresolved**

The effective reasoning cap is 1023 tokens (declared budget 1024), silent — it never triggers `finish_reason = length`, so the probe's `no_length_truncation: PASS` gate does not cover it.

**All 5 of B's errors — including all 3 that cause the H2 failure — occur in aggregates where every repetition hit that cap. All 36 uncapped B aggregates are correct.** Reaching the cap is necessary for B error here.

This does **not** threaten §8.1 or §8.2 — B's 34/36 and the B−E gap are unaffected, and B and E are budget-matched. It **does** confound §8.3: the H2 failure is inseparable, in these data, from reasoning exhaustion on the hardest cases. Two readings remain open and cannot be distinguished without new inference (explicitly out of scope here):

1. Peer insights genuinely interfere with local knowledge on the OJNSG/Z3ISU pair; or
2. Longer insight-bearing prompts push those cases past the thinking cap, and the errors are truncation artefacts.

Causality also runs in the other direction — harder cases naturally reason longer and so hit the cap — so the correlation is not self-interpreting. **Resolving this requires re-running the B condition at a raised `thinking_token_budget` and checking whether the 3 local-seen losses survive.** Until then H2 FAIL should be reported as *confounded*, and the budget should be treated as an uncontrolled variable of the design rather than a fixed constant.

### 8.5 Portability limits — **one alternative consumer only**

- **A single alternative consumer.** `Qwen/Qwen3.8-27B-FP8` @ revision `017b9c7a…`, one alias, one vLLM version (0.28.0), one decode configuration. Two lanes make a replication, not a portability claim; "the protocol is portable" is not yet supported, only "it transferred to one further model".
- **Small case base.** 12 independent physical fault clusters, 15 physical cases, 4 fault classes, 4 agents. The bootstrap correctly resamples clusters rather than agent rows and honestly declares `independence_claim: false`, but the CI upper bound of 1.0 reflects a ceiling effect on a small support.
- **R = 3 is degenerate in this lane** (§6.1). Deterministic decoding means the replication design contributes nothing here; sensitivity to sampling has not been probed for Qwen at all.
- **The condition-A baseline is degenerate** (48/48 own-label responses), so Δ_unseen is measured against a structural floor, not an informed comparator. Terra's A behaves differently, so the two Δ values are not strictly like-for-like even though both floors are 0.
- **Context margin is thin.** The probe records a minimum context margin of 220 tokens against a 4096 window. There is little headroom for the raised-budget re-run that §8.4 calls for; that run may need a larger context.
- **No environment pin.** The artefacts record code hashes but no Python or numpy version. Reproduction happened to be exact under numpy 2.5.3, but bit-identical bootstrap CIs are not guaranteed across BitGenerator or quantile-implementation changes. Pinning the numeric stack in the manifest would close this.
- Housekeeping: `test_probe_artifact.py::test_complete_experiment_outputs_do_not_exist` is stale post-inference (§3).

---

# Verdict

**Identity gate:** passed in full — tags 4/4, output set 9/9 with zero forbidden names, SHA-256 9/9, sentinels 11/11.

**Reproduction:** complete and exact. The 180 aggregates re-derive from the 540 repetition records with zero deviation; every metric, transfer count, per-agent figure, confusion matrix and both bootstrap intervals recompute to the frozen values; and an independent re-run of the official evaluator reproduces all nine artefacts **byte-for-byte**.

**Claims:** C1–C4 independently confirmed at 4/4 PASS. H2 independently confirmed FAIL, and correctly scoped as a secondary check outside the primary four.

## GO WITH LIMITATIONS

The primary result — persistence of unseen-fault transfer on a second, independent consumer — is sound, exactly reproducible, and supported by a well-controlled specificity contrast in which prompt length, reasoning budget and insight-citation rate are all matched between B and E. It may be reported.

It must be reported with these limitations attached, not as footnotes but as part of the claim:

1. **H2's local-seen regression (−0.25) is confounded with the 1023-token reasoning cap** — 100% of B's errors sit at that cap, 0% of uncapped B aggregates err. Report H2 as *failed and confounded*; do not attribute it to peer-insight interference without a raised-budget re-run of condition B.
2. **R = 3 is degenerate in this lane** — all 180 aggregates are byte-identical triplicates. Do not present 180/180 unanimity as evidence of stability.
3. **Condition A is a degenerate constant baseline** (48/48 own-label). Δ_unseen is measured against a structural floor, and Terra's A floor arises differently.
4. **Portability is not established by n = 1 alternative consumer** over 12 physical clusters. Claim replication on a second model, not protocol portability.
5. **Pin the numeric stack** (Python, numpy) in the reproducibility manifest; the current artefacts pin code hashes only.
6. Refresh the stale pre-inference probe test.

Recommended next step before any stronger claim: re-run condition B at a raised `thinking_token_budget` (with attention to the 220-token context margin) and check whether the three local-seen losses on the CLS-OJNSG ↔ CLS-Z3ISU pair persist. That single experiment separates the two live interpretations of H2.

---

## Appendix — commands and paths actually verified

**Paths read (server repo, read-only):**

```
/home/luca/fot-phd/phase_b/exp2/qwen/evaluation/{EVALUATION_REPORT.md,bootstrap_results.json,
    confusion_matrices.json,evaluation_hash_manifest.json,evaluation_results.json,
    per_agent_metrics.csv,primary_metrics.csv,secondary_metrics.csv,transfer_counts.csv}
/home/luca/fot-phd/phase_b/exp2/qwen/inference/{repetition_records.jsonl,aggregate_records.jsonl,
    execution_metadata.json,inference_output_hash_manifest.json}
/home/luca/fot-phd/phase_b/exp2/qwen/probe/{CAPABILITY_PROBE.md,capability_probe.json}
/home/luca/fot-phd/phase_b/exp2/qwen/{evaluate_qwen.py,EVALUATOR_AMENDMENT_001.md}
/home/luca/fot-phd/phase_b/final_evaluation/evaluate_frozen_predictions.py
/home/luca/fot-phd/phase_b/final_evaluation/evaluation_results.json
/home/luca/fot-phd/phase_b/final_evaluation/inference/aggregate_records.jsonl
/home/luca/fot-phd/phase_b/evaluation/{aggregation.py,bootstrap.py}
/home/luca/fot-phd/phase_b/config/protocol_config.json
/home/luca/fot-phd/phase_b/config/evaluator_side/pseudolabel_mapping.json
/home/luca/fot-phd/phase_b/heldout/phase_b_heldout_manifest.csv
```

**Scripts written (all under /tmp):**

```
/tmp/exp2qwen_r2/independent_recompute.py       # standalone re-derivation, imports nothing from the repo
/tmp/exp2qwen_r2/rerun_official_evaluator.py    # evaluator re-run in isolated clone + byte diff
/tmp/exp2qwen_r2/venv/                          # numpy 2.5.3, pytest
/tmp/exp2qwen_r2/repo/                          # throwaway clone
/tmp/expected_sha.txt                           # canonical hash list for sha256sum -c
```

**Key commands:**

```bash
# Phase 0
git rev-parse phase-b-exp2-qwen-{protocol,predictions,evaluator,results}-frozen-001^{}
git diff --name-status phase-b-exp2-qwen-evaluator-frozen-001^{} phase-b-exp2-qwen-results-frozen-001^{}
git ls-tree -r --name-only phase-b-exp2-qwen-results-frozen-001^{} -- phase_b/exp2/qwen/evaluation/
git cat-file blob phase-b-exp2-qwen-results-frozen-001^{}:<path> | sha256sum
cd phase_b/exp2/qwen/evaluation && sha256sum -c /tmp/expected_sha.txt
git merge-base --is-ancestor <protocol> <predictions>   # and the two following links
git status --porcelain                                   # empty, before and after

# Phase 1
/tmp/exp2qwen_r2/venv/bin/python /tmp/exp2qwen_r2/independent_recompute.py
git clone --no-hardlinks /home/luca/fot-phd /tmp/exp2qwen_r2/repo
/tmp/exp2qwen_r2/venv/bin/python /tmp/exp2qwen_r2/rerun_official_evaluator.py
cd /tmp/exp2qwen_r2/repo && /tmp/exp2qwen_r2/venv/bin/python -m pytest phase_b/exp2/qwen/tests -q \
    --ignore=phase_b/exp2/qwen/tests/test_adapter.py
```

**Repository state at end of review:** `git status --porcelain` empty; HEAD still `37195cf`; all nine frozen outputs still match their canonical SHA-256. No commit, tag, branch or file was created or modified in `/home/luca/fot-phd`. No LLM or vLLM call was made.
