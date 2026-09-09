# Ablation Experiment: TS→Text Representation Comparison

## Experiment Design

Four representation arms tested on 15 held-out TEP cases (PBH-001..PBH-015),
5-class centralized classification (F1, F8, F10, F13, Normal),
GPT-5.6-terra with structured output, 3 repetitions per arm × case = 180 total inferences.

**Independent units:** 15 case_ids (not 45 replicate rows).  All cluster-aware tests
operate at the case level.  Three repetitions per case measure within-case stability
but do not add independent statistical units.

**Statistical tests (all cluster-aware):**
- Clustered bootstrap (10,000 resamples of 15 case_ids, independent RNG per comparison)
- Exact sign-flip permutation test (2^15 = 32,768 permutations, per-case accuracy differences)
- McNemar at case level (majority-vote aggregated binary outcomes, N = 15, exact binomial)
- Holm–Bonferroni step-down correction across 6 pairwise comparisons

**Note:** Row-level McNemar (N = 45) is retained for reference only and labeled
NON-INFERENTIAL.  It treats replicate predictions as independent, which they are not
(same input), yielding anti-conservative p-values.

| Arm | Description |
|-----|-------------|
| V2_TEXT | Conformal verbalizer (Phase A/B baseline): 8 windows × 5 features per XMEAS, natural language with domain knowledge (thresholds, temporal trends) |
| RAW_FEATURES | LLMTime-style direct numerical serialization of V2 features |
| CGTIME_STATS | CGTime-inspired statistical baseline (adapted subset of Feng et al. 2026): 3-family summary, window-aligned |
| SAX_SYMBOLIC | Symbolic Aggregate approXimation encoding (alphabet=5, word=10), baseline-relative Z-norm |

## Results Summary

| Arm | Accuracy | 95% CI | Bal. Acc | Macro-F1 | MCC | Fault-Only | MV Acc | Abstain | Sel. Acc | Coverage | Agreement |
|-----|----------|--------|---------|----------|-----|-----------|--------|---------|----------|----------|-----------|
| V2_TEXT | 0.889 | [0.733, 1.000] | 0.889 | 0.907 | 0.866 | 0.861 | 0.867 | 0.044 | 0.930 | 0.956 | 0.933 |
| RAW_FEATURES | 0.933 | [0.800, 1.000] | 0.933 | 0.960 | 0.923 | 0.917 | 0.933 | 0.067 | 1.000 | 0.933 | 1.000 |
| CGTIME_STATS | 0.911 | [0.756, 1.000] | 0.911 | 0.943 | 0.900 | 0.889 | 0.933 | 0.089 | 1.000 | 0.911 | 0.933 |
| SAX_SYMBOLIC | 0.733 | [0.533, 0.933] | 0.733 | 0.721 | 0.699 | 0.833 | 0.733 | 0.067 | 0.786 | 0.933 | 1.000 |

## Per-Class Recall

| Arm | F1 | F8 | F10 | F13 | Normal |
|-----|----|----|-----|-----|--------|
| V2_TEXT | 1.000 | 0.667 | 1.000 | 0.778 | 1.000 |
| RAW_FEATURES | 1.000 | 1.000 | 1.000 | 0.667 | 1.000 |
| CGTIME_STATS | 1.000 | 1.000 | 1.000 | 0.556 | 1.000 |
| SAX_SYMBOLIC | 1.000 | 1.000 | 1.000 | 0.333 | 0.333 |

## Leave-One-Class-Out Accuracy (Sensitivity Analysis)

| Arm | excl. F1 | excl. F8 | excl. F10 | excl. F13 | excl. Normal |
|-----|----------|----------|-----------|-----------|--------------|
| V2_TEXT | 0.861 | 0.944 | 0.861 | 0.917 | 0.861 |
| RAW_FEATURES | 0.917 | 0.917 | 0.917 | 1.000 | 0.917 |
| CGTIME_STATS | 0.889 | 0.889 | 0.889 | 1.000 | 0.889 |
| SAX_SYMBOLIC | 0.667 | 0.667 | 0.667 | 0.833 | 0.833 |

## Pairwise Statistical Comparisons (Cluster-Aware — Primary Inference)

| Comparison | Δ Accuracy | 95% CI (boot) | p (boot) | p (perm) | p (McN-case) |
|------------|-----------|---------------|----------|----------|--------------|
| V2_TEXT vs RAW_FEATURES | -0.044 | [-0.200, 0.067] | 0.7690 | 1.0000 | 1.0000 |
| V2_TEXT vs CGTIME_STATS | -0.022 | [-0.178, 0.089] | 0.9672 | 1.0000 | 1.0000 |
| V2_TEXT vs SAX_SYMBOLIC | +0.156 | [-0.111, 0.422] | 0.2702 | 0.3750 | 0.6250 |
| RAW_FEATURES vs CGTIME_STATS | +0.022 | [0.000, 0.067] | 0.7096 | 1.0000 | 1.0000 |
| RAW_FEATURES vs SAX_SYMBOLIC | +0.200 | [0.000, 0.400] | 0.0716 | 0.2500 | 0.2500 |
| CGTIME_STATS vs SAX_SYMBOLIC | +0.178 | [0.000, 0.378] | 0.0706 | 0.2500 | 0.2500 |

### Holm–Bonferroni Correction (Clustered Bootstrap)

| Comparison | Raw p | Adjusted p | Significant? |
|------------|-------|------------|-------------|
| CGTIME_STATS vs SAX_SYMBOLIC | 0.0706 | 0.4236 | No |
| RAW_FEATURES vs SAX_SYMBOLIC | 0.0716 | 0.4236 | No |
| V2_TEXT vs SAX_SYMBOLIC | 0.2702 | 1.0000 | No |
| RAW_FEATURES vs CGTIME_STATS | 0.7096 | 1.0000 | No |
| V2_TEXT vs RAW_FEATURES | 0.7690 | 1.0000 | No |
| V2_TEXT vs CGTIME_STATS | 0.9672 | 1.0000 | No |

### Holm–Bonferroni Correction (Permutation Test)

| Comparison | Raw p | Adjusted p | Significant? |
|------------|-------|------------|-------------|
| RAW_FEATURES vs SAX_SYMBOLIC | 0.2500 | 1.0000 | No |
| CGTIME_STATS vs SAX_SYMBOLIC | 0.2500 | 1.0000 | No |
| V2_TEXT vs SAX_SYMBOLIC | 0.3750 | 1.0000 | No |
| V2_TEXT vs RAW_FEATURES | 1.0000 | 1.0000 | No |
| V2_TEXT vs CGTIME_STATS | 1.0000 | 1.0000 | No |
| RAW_FEATURES vs CGTIME_STATS | 1.0000 | 1.0000 | No |

### Holm–Bonferroni Correction (McNemar Case-Level, N=15)

| Comparison | Raw p | Adjusted p | Significant? |
|------------|-------|------------|-------------|
| RAW_FEATURES vs SAX_SYMBOLIC | 0.2500 | 1.0000 | No |
| CGTIME_STATS vs SAX_SYMBOLIC | 0.2500 | 1.0000 | No |
| V2_TEXT vs SAX_SYMBOLIC | 0.6250 | 1.0000 | No |
| V2_TEXT vs RAW_FEATURES | 1.0000 | 1.0000 | No |
| V2_TEXT vs CGTIME_STATS | 1.0000 | 1.0000 | No |
| RAW_FEATURES vs CGTIME_STATS | 1.0000 | 1.0000 | No |

### Row-Level McNemar (NON-INFERENTIAL — Reference Only)

> **Warning:** These results treat 45 replicate predictions as independent
> observations.  Since each case_id contributes 3 non-independent predictions
> (same input), these p-values are anti-conservative and should NOT be used
> for inferential conclusions.

| Comparison | Raw p | Adjusted p | Significant? |
|------------|-------|------------|-------------|
| RAW_FEATURES vs SAX_SYMBOLIC | 0.0039 | 0.0234 | Yes |
| CGTIME_STATS vs SAX_SYMBOLIC | 0.0078 | 0.0391 | Yes |
| V2_TEXT vs SAX_SYMBOLIC | 0.0923 | 0.3691 | No |
| V2_TEXT vs RAW_FEATURES | 0.6250 | 1.0000 | No |
| V2_TEXT vs CGTIME_STATS | 1.0000 | 1.0000 | No |
| RAW_FEATURES vs CGTIME_STATS | 1.0000 | 1.0000 | No |

## Confusion Matrices

### V2_TEXT

| True \ Pred | F1 | F8 | F10 | F13 | Normal | ABSTAIN |
|---|---|---|---|---|---|---|
| F1 | 9 | 0 | 0 | 0 | 0 | 0 |
| F8 | 0 | 6 | 0 | 3 | 0 | 0 |
| F10 | 0 | 0 | 9 | 0 | 0 | 0 |
| F13 | 0 | 0 | 0 | 7 | 0 | 2 |
| Normal | 0 | 0 | 0 | 0 | 9 | 0 |

### RAW_FEATURES

| True \ Pred | F1 | F8 | F10 | F13 | Normal | ABSTAIN |
|---|---|---|---|---|---|---|
| F1 | 9 | 0 | 0 | 0 | 0 | 0 |
| F8 | 0 | 9 | 0 | 0 | 0 | 0 |
| F10 | 0 | 0 | 9 | 0 | 0 | 0 |
| F13 | 0 | 0 | 0 | 6 | 0 | 3 |
| Normal | 0 | 0 | 0 | 0 | 9 | 0 |

### CGTIME_STATS

| True \ Pred | F1 | F8 | F10 | F13 | Normal | ABSTAIN |
|---|---|---|---|---|---|---|
| F1 | 9 | 0 | 0 | 0 | 0 | 0 |
| F8 | 0 | 9 | 0 | 0 | 0 | 0 |
| F10 | 0 | 0 | 9 | 0 | 0 | 0 |
| F13 | 0 | 0 | 0 | 5 | 0 | 4 |
| Normal | 0 | 0 | 0 | 0 | 9 | 0 |

### SAX_SYMBOLIC

| True \ Pred | F1 | F8 | F10 | F13 | Normal | ABSTAIN |
|---|---|---|---|---|---|---|
| F1 | 9 | 0 | 0 | 0 | 0 | 0 |
| F8 | 0 | 9 | 0 | 0 | 0 | 0 |
| F10 | 0 | 0 | 9 | 0 | 0 | 0 |
| F13 | 0 | 3 | 0 | 3 | 0 | 3 |
| Normal | 0 | 0 | 6 | 0 | 3 | 0 |

## Conclusions

### Corrected interpretations (post external review)

1. **V2_TEXT, RAW_FEATURES, and CGTIME_STATS: not demonstrably different.**
   No pairwise comparison among these three arms reaches statistical significance
   on any cluster-aware test after Holm–Bonferroni correction.  However, the
   experiment has limited statistical power (N_eff = 15 independent cases;
   MDE ≈ 0.25–0.30), so the absence of significance does not demonstrate
   equivalence.  Moderate or small true differences cannot be excluded.

2. **SAX_SYMBOLIC: descriptively inferior, significance test-dependent.**
   SAX_SYMBOLIC shows the lowest observed accuracy (0.733 vs 0.889–0.933).
   Row-level McNemar (N = 45, non-cluster-aware) found significance for
   RAW vs SAX and CGTIME vs SAX, but this test ignores clustering and its
   p-values are anti-conservative.  Cluster-aware tests (permutation test,
   case-level McNemar, clustered bootstrap) should be consulted for
   inferential conclusions; with N = 15 independent cases, their power is
   limited.  The descriptive pattern is strong but formal confirmation
   requires a larger sample.

3. **F13 is a difficult class, but not uniformly the hardest.**
   F13 (slow drift) shows low recall across all arms (0.333–0.778),
   concentrated in abstentions (RAW, CGTIME, SAX) or F8 misclassification
   (V2_TEXT).  However, V2_TEXT shows lower recall for F8 (0.667) than F13
   (0.778), and SAX_SYMBOLIC ties F13 and Normal at 0.333.  The pattern is
   arm-dependent, not universal.

4. **V2_TEXT offers the best observed cost–accuracy trade-off.**
   V2_TEXT uses ~1/39× the tokens of RAW_FEATURES and ~1/180× of CGTIME_STATS
   while achieving comparable observed accuracy.  This advantage includes
   pre-computed domain knowledge (conformal thresholds, temporal trend
   descriptions) whose preprocessing cost is external to the prompt token
   budget and should be accounted for separately.

5. **Results are limited in scope.**
   This experiment covers 4 of 28 TEP fault types, one simulation mode,
   one LLM (GPT-5.6-terra), and a centralised 5-class classification task
   (not the production federated 2-class architecture).  The ranking may
   differ for other faults (especially those with subtle multivariate
   signatures), other LLMs, or the production pipeline configuration.

### Caveats

- **Information–representation confound:** V2_TEXT embeds domain knowledge
  (thresholds, trend descriptions); RAW_FEATURES uses derived features;
  CGTIME and SAX operate closer to raw sensor data.  The experiment tests
  the combined effect of representation format and information content,
  not format alone.
- **Selective accuracy caveat:** RAW_FEATURES and CGTIME_STATS achieve
  selective accuracy = 1.000, but this is conditioned on non-abstention
  (coverage 0.933 and 0.911 respectively).  Selective accuracy does not
  substitute for overall accuracy, coverage, or selective risk; the high
  values indicate that errors in these arms are exclusively abstentions
  on F13, not misclassifications.
- **Prompt-length confound:** CGTIME_STATS uses ~180× more tokens than
  V2_TEXT.  Comparable accuracy could reflect offsetting effects of richer
  information and attention dilution.
- **Statistical power:** with 15 independent cases, only large effects
  (Δ ≥ 0.25) are reliably detectable.  Additional independent cases are
  needed to resolve finer differences.

## Statistical Notes

- **Accuracy:** abstentions count as incorrect predictions.
- **Selective accuracy:** accuracy among non-abstained predictions only.
- **Coverage:** fraction of non-abstained predictions (= 1 − abstention rate).
- **Balanced accuracy:** mean of per-class recalls.
- **Macro-F1:** unweighted mean of per-class F1 scores.
- **MCC:** Matthews correlation coefficient (multi-class, Gorodkin 2004); ranges from −1 to +1.
- **Fault-Only Accuracy:** excludes Normal cases.
- **Majority Vote:** requires ≥ ceil(R/2) concordant votes; otherwise no-majority (counted wrong).
- **Agreement:** fraction of cases where all 3 reps agree on the same label.
- **Leave-One-Class-Out:** accuracy when excluding each class in turn; shows sensitivity to individual classes.
- **Bootstrap CIs:** 10,000 resamples, seed=42, clustered by case_id (15 independent units).
- **Permutation test:** exact sign-flip test on per-case accuracy differences (2^15 = 32,768 permutations); cluster-aware.
- **McNemar case-level:** exact binomial on majority-vote aggregated binary outcomes per case (N = 15); cluster-aware.
- **McNemar row-level (NON-INFERENTIAL):** exact binomial on 45 prediction pairs; ignores clustering, anti-conservative; retained for reference only.
- **Holm–Bonferroni:** step-down correction across 6 pairwise comparisons.

## Phase B Reference

Phase B used per-agent 2-label classification (specialist + Normal) with federated peer insights.
Condition A (isolated): ~56% accuracy. Condition B (FoT): ~86% accuracy.
This ablation uses 5-label centralized classification — a harder task — so direct numerical comparison is **not** the primary endpoint.
The quantity of interest is the **relative ranking** between the four representation arms.
