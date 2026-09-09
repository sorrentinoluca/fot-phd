# Ablation Experiment: Representation Strategies for LLM Fault Diagnosis

## Objective

Compare four TS→text representation strategies on the same held-out TEP cases
using the same diagnostic LLM, to answer: "Does the V2 deterministic verbalizer
produce representations that lead to better fault diagnosis than alternatives?"

**Primary endpoint:** relative ranking between the four arms (not absolute
accuracy comparison with Phase B — see §Phase B Reference below).

## Arms

| Arm | Strategy | Category | Inspired by |
|-----|----------|----------|-------------|
| **V2_TEXT** | Frozen V2 neutral text (existing) | Domain-driven verbalization | FoT-TEP |
| **RAW_FEATURES** | Raw feature values, no thresholds or temporal logic | Numerical serialization | LLMTime-style |
| **CGTIME_STATS** | CGTime-inspired statistical baseline (adapted subset) | Statistical perception | CGTime (Feng 2026) |
| **SAX_SYMBOLIC** | Symbolic Aggregate approXimation encoding | Symbolic representation | SAX / HAR-LLM (Pappa 2026) |

### Note on CGTIME_STATS (L8)

This arm implements a **CGTime-inspired statistical baseline**, not a full
replica of the CGTime framework (Feng et al. 2026).  Specifically:

- **Included:** Direct (10 stats/var), Marginal (14 stats/var), Joint system
  statistics (PCA, correlation, Mahalanobis with Ledoit–Wolf regularised
  covariance, windowed correlation stability, per-channel synchronisation).
- **Not included:** the full PCA cross-channel description reduction O(rK)
  pipeline, the CGTime multi-scale temporal decomposition, and the
  domain-specific feature selection module.
- The Mahalanobis distance uses regularised (Ledoit–Wolf shrinkage) covariance
  inverse, not a diagonal simplification.

This arm should be cited as "CGTime-inspired statistical baseline" and compared
against the original paper or a reference implementation for any claims about
CGTime performance.

## Design

- **Cases:** 15 held-out PBH cases (PBH-001..PBH-015): F1×3, F8×3, F10×3, F13×3, Normal×3
- **Prompt setup:** Centralized (all 5 labels visible, 10 local examples: 2 per class)
- **Examples source:** Development batches 1-2 (same as Phase B local examples); Normal uses blocks N1-N2 from mode1_normal_500.xlsx (extracted as 50h windows with time reset to match held-out Normal config)
- **Example ordering:** fixed permutation (seed=42), identical across all arms
- **Examples rendered in EACH arm's format** for consistency
- **LLM:** GPT-5.6-terra (same as Phase B), structured output (Responses API)
- **Repetitions:** 3 per arm × case
- **Total inferences:** 4 arms × 15 cases × 3 reps = 180 calls
- **Reasoning effort:** medium (same as Phase B)
- **Max prompt tokens:** 900,000 (preflight validated before each API call)

## Window Structure

All arms use the same temporal structure: 8 windows × 5h, from 10h to 50h
post-injection.  This ensures identical temporal granularity across all four
representations.  CGTIME_STATS computes per-variable statistics (Direct and
Marginal families) per window, and Joint statistics per window, matching the
other arms' temporal resolution.

## Fault Selection Rationale (L5)

The four fault types were selected to span different fault mechanisms and
difficulty levels from the TEP benchmark:

| Fault | Mechanism | Difficulty | Rationale |
|-------|-----------|------------|-----------|
| **F1**  | Step change in A/C feed ratio | Easy–Medium | Classic abrupt fault; well-studied baseline |
| **F8**  | Random variation in AB feed composition | Medium | Stochastic, harder than step; composition fault |
| **F10** | Random variation in C feed temperature | Medium–Hard | Temperature perturbation; tests thermal sensitivity |
| **F13** | Slow drift in D feed reaction kinetics | Hard | Gradual onset; most challenging for early detection |

This selection covers: one abrupt fault (F1), two stochastic faults (F8, F10),
and one drift fault (F13), representing the main fault categories in TEP.
However, results should be interpreted as valid for **this four-fault sample
only** and do not generalise to all 28 TEP fault types without replication.

## Representation Details

### Arm 1: V2_TEXT (~137 words/case)
Existing `render_text()` output from the frozen V2 verbalizer. Natural language with
conformal threshold comparisons (alpha=0.05), temporal trend descriptions, and system-level
summary. Represents the current FoT-TEP pipeline.

### Arm 2: RAW_FEATURES (~370 words/case)
The same 5 V2 features (shift_sigma, slope_sigma_h, residual_std_ratio, diff_std_ratio,
raw_std_ratio) for each variable × window, presented as a flat numerical table.
No threshold comparison, no temporal interpretation, no "above/below threshold" flags.
Tests whether the LLM can diagnose from the same numeric inputs the verbalizer uses.

### Arm 3: CGTIME_STATS (~2312 words/case)
CGTime-inspired statistical baseline — adapted subset of Feng et al. (2026):

- **Direct family (10 stats/variable/window):** mean, std, min, max, median, IQR, range, start_value, end_value, max_peak_prominence (min_prominence=0.01)
- **Marginal family (14 stats/variable/window):** acf_lag1, mean_abs_change, ols_slope, R², CV, num_peaks, num_troughs, sign_changes, spectral_entropy, dominant_freq, anomaly_count, skewness, kurtosis
- **Joint family (per window):** PCA (11: k, floor, ratios, effective_rank, PC1 trend/volatility/loadings), Correlation (6: mean/max abs, n_highly_correlated, sync ratios), Mahalanobis with Ledoit–Wolf regularised covariance (4: mean/max distance, outlier ratio/count), Windowed correlation stability (4: structure stability, Frobenius change, dynamics), Per-channel sync (4: avg/std R² top-k, high_sync, decoupled ratios)
- **Total:** ~1014 statistics per window × 8 windows per case

### Arm 4: SAX_SYMBOLIC (~694 words/case)
SAX encoding per variable per window:
- Z-normalization relative to baseline mean and std (not local/per-window)
- PAA reduction to word_size=10 segments (end index clamped to series length)
- Alphabet size: 5 (a-e), breakpoints from standard normal quantiles
- Format: `XMEAS-01: aabccddeed | bccdeeeddd | ...`

## Controls

- Same LLM model and parameters across all arms
- Same prompt template (only the case text and examples blocks differ by arm)
- Same structured output schema (predicted_label, abstain, reasoning_summary) with strict JSON validation
- Same random seed where applicable
- Examples in each arm use that arm's representation format
- Same temporal window structure (8 windows, 10–50h)
- Same example ordering (fixed permutation, seed=42)
- Provenance hash (code + config + manifest + examples) verified on resume

## Metrics

### Primary

1. **Overall accuracy** (correct / total, abstain = wrong)
2. **Balanced accuracy** (mean of per-class recalls)
3. **Macro-F1** (unweighted mean of per-class F1)
4. **MCC** (Matthews correlation coefficient, multi-class)
5. **Pairwise comparisons** (all 6 pairs):
   - Bootstrap paired accuracy difference with 95% CI (clustered by case_id)
   - McNemar's test (exact binomial when discordant < 25, asymptotic otherwise)
   - Holm–Bonferroni correction across 6 comparisons

### Secondary

6. **Fault-only accuracy** (excluding Normal cases)
7. **Per-class recall** (F1, F8, F10, F13, Normal)
8. **Majority vote accuracy** (requires ≥ ceil(R/2) = 2 concordant votes; else no-majority = wrong)
9. **Abstention rate**
10. **Repetition agreement** (fraction of cases where all 3 reps agree)
11. **Token usage** (input/output tokens per arm)
12. **Confusion matrices** (5×5 + ABSTAIN column)

### Statistical design

- **Independent units:** 15 case_ids (not 45 replicate rows)
- **Bootstrap:** 10,000 resamples, seed=42, clustered by case_id; independent RNG per comparison (derived deterministically from seed + pair name)
- **p-values:** two-sided throughout
- **Multiplicity correction:** Holm–Bonferroni across 6 pairwise comparisons
- **Minimum detectable effect (MDE):** with N_eff ≈ 15 (clustered), the experiment can reliably detect differences of ~0.25–0.30 in accuracy; smaller effects require additional independent cases

## Pipeline

```
ablation_representations.py  # 4 representation generators (window-aligned)
ablation_runner.py           # Inference runner (--dry-run for testing)
ablation_evaluate.py         # Evaluation and statistical analysis
```

### Running

```bash
# Dry run (random predictions, no API calls)
python ablation_runner.py --project-root /path/to/fot-tep --dry-run

# Full run
python ablation_runner.py --project-root /path/to/fot-tep --output-dir ablation_results

# Resume after interruption (verifies provenance hash)
python ablation_runner.py --project-root /path/to/fot-tep --output-dir ablation_results --resume

# Evaluate
python ablation_evaluate.py ablation_results
```

### Dependencies

```
pip install pandas numpy scipy openpyxl openai scikit-learn
```

## Phase B Reference (L4)

Phase B used per-agent 2-label classification (specialist fault + Normal) with
federated peer insights across 4 specialised agents.  Condition A (isolated):
~56% accuracy.  Condition B (FoT): ~86% accuracy.

**This ablation differs from Phase B in several structural ways:**

- **Label space:** 5-class centralised (harder) vs 2-class per-agent
- **Architecture:** single LLM vs 4 federated specialist agents with peer insight exchange
- **Task complexity:** must discriminate among 4 fault types + Normal vs binary fault/normal

Therefore, **direct numerical comparison of absolute accuracy with Phase B is
not meaningful**.  The primary endpoint of this ablation is the **relative
ranking between the four representation arms**.  If a Phase B comparison is
needed, it should use a V2_TEXT condition run with the Phase B protocol (2-label,
per-agent, federated) as a separate validation condition.
