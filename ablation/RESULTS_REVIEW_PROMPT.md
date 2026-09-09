# Independent External Review — Ablation Experiment Results

## Review scope

You are asked to perform an independent review of an ablation experiment
comparing four time-series-to-text (TS→text) representation strategies for
LLM-based fault diagnosis on the Tennessee Eastman Process (TEP).  The
experiment has been designed, executed, and evaluated.  Your review covers
**the results, statistical analysis, and the conclusions drawn** — not the
code implementation (which was reviewed separately before the run).

Provide a structured verdict: **GO / GO-with-reservations / NO-GO**, with
numbered findings and explicit severity (CRITICAL / MAJOR / MINOR /
INFORMATIONAL).

---

## 1 — Experiment context

### 1.1 Research question

> Does the V2 deterministic verbalizer produce TS→text representations that
> lead to better LLM fault diagnosis than three alternative strategies?

**Primary endpoint:** relative ranking between the four arms (not absolute
accuracy comparison with any external baseline).

### 1.2 Arms

| Arm | Strategy | Token budget (mean input) |
|-----|----------|--------------------------|
| **V2_TEXT** | Frozen V2 neutral verbalizer: conformal thresholds (α = 0.05), temporal trend descriptions, natural-language system summary | 3 296 |
| **RAW_FEATURES** | Same 5 V2 numeric features per variable × window, flat table, no thresholds or interpretation | 127 962 |
| **CGTIME_STATS** | CGTime-inspired statistical baseline (adapted subset of Feng et al. 2026): Direct (10 stats/var), Marginal (14 stats/var), Joint (PCA, correlation, Mahalanobis w/ Ledoit–Wolf regularised covariance) — ~1 014 stats/window | 593 475 |
| **SAX_SYMBOLIC** | SAX encoding: Z-norm (baseline-relative), PAA word_size = 10, alphabet = 5 | 21 138 |

### 1.3 Design

- **Cases:** 15 held-out TEP cases (PBH-001 … PBH-015): F1 × 3, F8 × 3, F10 × 3, F13 × 3, Normal × 3
- **Label space:** 5-class centralised (F1, F8, F10, F13, Normal)
- **Prompt:** Centralised, all 5 labels visible, 10 in-context examples (2 per class), rendered in each arm's format
- **Example ordering:** Fixed permutation (seed = 42), identical across arms
- **LLM:** GPT-5.6-terra (OpenAI Responses API, structured output)
- **Reasoning effort:** medium
- **Repetitions:** 3 per arm × case → **180 total inferences**
- **Max prompt tokens:** 900 000 (preflight-validated)
- **Window structure:** 8 windows × 5 h, from 10 h to 50 h post-injection — identical across all arms
- **Abstention handling:** Abstain counts as incorrect
- **Independent units:** 15 case_ids (not 45 replicate rows)

### 1.4 Fault selection

| Fault | Mechanism | Difficulty |
|-------|-----------|------------|
| F1 | Step change in A/C feed ratio | Easy–Medium |
| F8 | Random variation in AB feed composition | Medium |
| F10 | Random variation in C feed temperature | Medium–Hard |
| F13 | Slow drift in D feed reaction kinetics | Hard |

Selection rationale: one abrupt (F1), two stochastic (F8, F10), one drift (F13).
Results valid for this four-fault sample only.

---

## 2 — Results

### 2.1 Primary metrics

| Arm | Accuracy | 95 % CI (clustered bootstrap) | Balanced Acc. | Macro-F1 | MCC |
|-----|----------|-------------------------------|---------------|----------|-----|
| RAW_FEATURES | **0.9333** | [0.800, 1.000] | 0.9333 | 0.9600 | 0.9231 |
| CGTIME_STATS | 0.9111 | [0.756, 1.000] | 0.9111 | 0.9429 | 0.9001 |
| V2_TEXT | 0.8889 | [0.733, 1.000] | 0.8889 | 0.9074 | 0.8664 |
| SAX_SYMBOLIC | 0.7333 | [0.533, 0.933] | 0.7333 | 0.7214 | 0.6990 |

### 2.2 Secondary metrics

| Arm | Fault-only Acc. | Maj. Vote Acc. | No-majority cases | Abstention rate | Rep. agreement |
|-----|-----------------|----------------|--------------------|-----------------|----------------|
| RAW_FEATURES | 0.9167 | 0.9333 | 1 | 0.0667 | 1.0000 |
| CGTIME_STATS | 0.8889 | 0.9333 | 1 | 0.0889 | 0.9333 |
| V2_TEXT | 0.8611 | 0.8667 | 1 | 0.0444 | 0.9333 |
| SAX_SYMBOLIC | 0.8333 | 0.7333 | 1 | 0.0667 | 1.0000 |

### 2.3 Per-class recall

| Arm | F1 | F8 | F10 | F13 | Normal |
|-----|----|----|-----|-----|--------|
| V2_TEXT | 1.0 | 0.667 | 1.0 | 0.778 | 1.0 |
| RAW_FEATURES | 1.0 | 1.0 | 1.0 | 0.667 | 1.0 |
| CGTIME_STATS | 1.0 | 1.0 | 1.0 | 0.556 | 1.0 |
| SAX_SYMBOLIC | 1.0 | 1.0 | 1.0 | 0.333 | 0.333 |

### 2.4 Confusion matrices (true class → predicted, ABSTAIN column included)

**V2_TEXT:**

|  | F1 | F8 | F10 | F13 | Normal | ABSTAIN |
|--|----|----|-----|-----|--------|---------|
| F1 | 9 | 0 | 0 | 0 | 0 | 0 |
| F8 | 0 | 6 | 0 | 3 | 0 | 0 |
| F10 | 0 | 0 | 9 | 0 | 0 | 0 |
| F13 | 0 | 0 | 0 | 7 | 0 | 2 |
| Normal | 0 | 0 | 0 | 0 | 9 | 0 |

**RAW_FEATURES:**

|  | F1 | F8 | F10 | F13 | Normal | ABSTAIN |
|--|----|----|-----|-----|--------|---------|
| F1 | 9 | 0 | 0 | 0 | 0 | 0 |
| F8 | 0 | 9 | 0 | 0 | 0 | 0 |
| F10 | 0 | 0 | 9 | 0 | 0 | 0 |
| F13 | 0 | 0 | 0 | 6 | 0 | 3 |
| Normal | 0 | 0 | 0 | 0 | 9 | 0 |

**CGTIME_STATS:**

|  | F1 | F8 | F10 | F13 | Normal | ABSTAIN |
|--|----|----|-----|-----|--------|---------|
| F1 | 9 | 0 | 0 | 0 | 0 | 0 |
| F8 | 0 | 9 | 0 | 0 | 0 | 0 |
| F10 | 0 | 0 | 9 | 0 | 0 | 0 |
| F13 | 0 | 0 | 0 | 5 | 0 | 4 |
| Normal | 0 | 0 | 0 | 0 | 9 | 0 |

**SAX_SYMBOLIC:**

|  | F1 | F8 | F10 | F13 | Normal | ABSTAIN |
|--|----|----|-----|-----|--------|---------|
| F1 | 9 | 0 | 0 | 0 | 0 | 0 |
| F8 | 0 | 9 | 0 | 0 | 0 | 0 |
| F10 | 0 | 0 | 9 | 0 | 0 | 0 |
| F13 | 0 | 3 | 0 | 3 | 0 | 3 |
| Normal | 0 | 0 | 6 | 0 | 3 | 0 |

### 2.5 Pairwise comparisons (6 pairs)

| Pair | Δ Accuracy | Bootstrap 95 % CI | Bootstrap p | McNemar stat | McNemar p |
|------|-----------|-------------------|-------------|--------------|-----------|
| V2_TEXT vs RAW_FEATURES | −0.044 | [−0.200, +0.067] | 0.769 | 1 | 0.625 |
| V2_TEXT vs CGTIME_STATS | −0.022 | [−0.178, +0.089] | 0.967 | 2 | 1.000 |
| V2_TEXT vs SAX_SYMBOLIC | +0.156 | [−0.111, +0.422] | 0.270 | 10 | 0.092 |
| RAW_FEATURES vs CGTIME_STATS | +0.022 | [+0.000, +0.067] | 0.710 | 1 | 1.000 |
| RAW_FEATURES vs SAX_SYMBOLIC | +0.200 | [+0.000, +0.400] | 0.072 | 9 | 0.004 |
| CGTIME_STATS vs SAX_SYMBOLIC | +0.178 | [+0.000, +0.378] | 0.071 | 8 | 0.008 |

### 2.6 Holm–Bonferroni correction (α = 0.05, k = 6 comparisons)

**Bootstrap test (clustered by case_id):**

| Comparison | Raw p | Adjusted p | Significant? |
|-----------|-------|------------|-------------|
| CGTIME_STATS vs SAX_SYMBOLIC | 0.071 | 0.424 | No |
| RAW_FEATURES vs SAX_SYMBOLIC | 0.072 | 0.424 | No |
| V2_TEXT vs SAX_SYMBOLIC | 0.270 | 1.000 | No |
| RAW_FEATURES vs CGTIME_STATS | 0.710 | 1.000 | No |
| V2_TEXT vs RAW_FEATURES | 0.769 | 1.000 | No |
| V2_TEXT vs CGTIME_STATS | 0.967 | 1.000 | No |

**McNemar test (exact binomial, all pairs had < 25 discordant):**

| Comparison | Raw p | Adjusted p | Significant? |
|-----------|-------|------------|-------------|
| RAW_FEATURES vs SAX_SYMBOLIC | 0.004 | **0.023** | **Yes** |
| CGTIME_STATS vs SAX_SYMBOLIC | 0.008 | **0.039** | **Yes** |
| V2_TEXT vs SAX_SYMBOLIC | 0.092 | 0.369 | No |
| V2_TEXT vs RAW_FEATURES | 0.625 | 1.000 | No |
| V2_TEXT vs CGTIME_STATS | 1.000 | 1.000 | No |
| RAW_FEATURES vs CGTIME_STATS | 1.000 | 1.000 | No |

### 2.7 Token usage and latency

| Arm | Mean input tokens | Mean output tokens | Total input | Mean latency (ms) |
|-----|-------------------|--------------------|-------------|-------------------|
| V2_TEXT | 3 296 | 99 | 148 326 | 2 403 |
| RAW_FEATURES | 127 962 | 151 | 5 758 272 | 3 885 |
| CGTIME_STATS | 593 475 | 163 | 26 706 372 | 33 409 |
| SAX_SYMBOLIC | 21 138 | 235 | 951 228 | 4 422 |

---

## 3 — Authors' preliminary conclusions

The authors draw the following conclusions from the data above (the reviewer
should independently assess whether each is supported):

1. **Top-3 indistinguishable:** V2_TEXT, RAW_FEATURES, and CGTIME_STATS
   produce statistically indistinguishable accuracy on this sample
   (no pairwise comparison reaches significance after Holm–Bonferroni
   correction on the clustered bootstrap test; McNemar also non-significant
   for all three mutual pairs).

2. **SAX_SYMBOLIC significantly worse:** RAW_FEATURES and CGTIME_STATS each
   significantly outperform SAX_SYMBOLIC (McNemar adjusted p = 0.023 and
   0.039 respectively).  V2_TEXT vs SAX_SYMBOLIC approaches but does not
   reach significance (adjusted p = 0.369).

3. **F13 is universally hard:** All four arms show lowest recall on F13
   (slow drift), with errors concentrated in abstentions (RAW, CGTIME, SAX)
   or misclassification as F8 (V2_TEXT).

4. **V2_TEXT is the most efficient:** V2_TEXT achieves comparable accuracy
   at 1/39× the tokens of RAW_FEATURES and 1/180× the tokens of
   CGTIME_STATS.

5. **Absence of evidence ≠ evidence of absence:** The experiment has
   N_eff ≈ 15 (clustered by case_id); the minimum detectable effect (MDE) is
   approximately 0.25–0.30.  True differences smaller than this cannot be
   reliably detected.

---

## 4 — Review questions

Please address **each** of the following.  For each, state whether you
find the claim supported, partially supported, or unsupported, with
justification.

### 4.1 Statistical validity

1. **Clustered bootstrap appropriateness.** The bootstrap resamples 15
   case_ids (not 45 individual predictions).  Is this the correct unit of
   analysis given that each case_id has 3 replicate predictions with the
   same input?  Are there alternative approaches that might be more
   appropriate or powerful?

2. **McNemar vs bootstrap divergence.** McNemar detects RAW vs SAX and
   CGTIME vs SAX as significant, but the clustered bootstrap does not
   (after correction).  What explains this divergence?  Which test is more
   trustworthy for this experimental design?  Is the discrepancy a concern?

3. **Holm–Bonferroni choice.** Six pairwise comparisons were corrected with
   Holm–Bonferroni.  Was this the right correction method?  Would an
   alternative (e.g., Bonferroni, Benjamini–Hochberg, Dunnett against
   V2_TEXT as control) change the conclusions?

4. **Confidence interval width.** All 95 % CIs are very wide (e.g., V2_TEXT:
   [0.733, 1.000]; SAX: [0.533, 0.933]).  Do these widths undermine the
   ability to draw any reliable conclusions?  Is the stated MDE of 0.25–0.30
   correctly computed and appropriately disclosed?

5. **Independence of RNG streams.** Each pairwise comparison uses an
   independent RNG derived deterministically from SHA-256(seed + pair_name).
   Is this a valid approach for ensuring independence between bootstrap
   tests?  Could it introduce subtle correlations?

### 4.2 Experimental design

6. **Sample size adequacy.** With only 15 independent cases (3 per class),
   is the experiment adequately powered to answer the research question?
   What sample size would be needed to detect, say, a 10-percentage-point
   difference with 80 % power?

7. **Class balance and case selection.** Three cases per class from one TEP
   simulation mode (mode 1).  Is this sufficient for generalisable
   conclusions?  What biases might arise from this limited sampling?

8. **Repetition structure.** Three repetitions per case with the same prompt
   yield repetition agreement of 0.93–1.00.  Does this high agreement
   suggest the 3-rep design adds minimal independent information?  Should
   the token budget have been spent on more independent cases instead?

9. **In-context example contamination.** All arms use 10 in-context examples
   (2 per class) from the development set.  Could the example selection
   disproportionately favour one arm?  The examples are rendered in each
   arm's own format — does this fully control for the confound?

10. **Abstention as error.** Abstentions are counted as incorrect.  Is this
    appropriate?  CGTIME_STATS has the highest abstention rate (8.9 %),
    concentrated on F13.  Could an alternative scoring (e.g., excluding
    abstentions, or scoring them as half-correct) change the ranking?

### 4.3 Threats to validity

11. **Prompt-length confound.** CGTIME_STATS uses ~180× more input tokens
    than V2_TEXT.  Despite comparable accuracy, could the LLM's performance
    be degraded by the sheer volume of CGTIME input (attention dilution,
    lost-in-the-middle effects)?  If so, CGTIME's "true" informational
    content might be higher than its accuracy suggests.  How should this
    confound be addressed or disclosed?

12. **Representation-information confound.** V2_TEXT includes threshold
    comparisons and temporal trend descriptions that constitute **domain
    knowledge injected by the verbalizer** — information the other arms
    do not receive.  RAW_FEATURES uses the same 5 derived features (already
    a form of feature engineering).  CGTIME_STATS and SAX_SYMBOLIC work
    from raw sensor data.  The arms therefore differ not only in
    *representation format* but in *information content*.  Does the
    experiment actually test "representation strategy" or "how much
    domain knowledge to inject"?

13. **Single LLM dependency.** All results are from GPT-5.6-terra.  How
    sensitive might the ranking be to LLM choice?  Would a different model
    (e.g., Claude, Gemini, an open-source model) potentially reverse the
    ranking?

14. **Centralised vs federated mismatch.** The production system (Phase B)
    uses 4 federated specialist agents with 2-class classification.  This
    ablation uses centralised 5-class.  Does this structural difference
    limit the external validity of the representation ranking for the
    actual production pipeline?

15. **Temporal window choice.** All arms use 10–50 h post-injection.  Could
    the window placement favour or disadvantage specific representations
    (e.g., SAX might perform better with earlier or later windows)?

### 4.4 Interpretation of results

16. **"Top-3 indistinguishable" claim.** The authors conclude V2_TEXT,
    RAW_FEATURES, and CGTIME_STATS are indistinguishable.  Given the wide
    CIs and low power (MDE ≈ 0.25), is "indistinguishable" the right word,
    or should it be "not demonstrably different given the available
    statistical power"?  Is there a meaningful distinction?

17. **SAX failure mode.** SAX_SYMBOLIC's errors are distinctive: F13 → F8
    misclassification (3/9 reps) and Normal → F10 misclassification (6/9
    reps).  What does this reveal about SAX's representational limitations?
    Is the Z-normalisation (baseline-relative) appropriate, or could it
    erase the signal SAX needs?

18. **F13 universal difficulty.** Every arm struggles with F13 (recall:
    0.33–0.78).  The error patterns differ: V2_TEXT confuses F13 with F8;
    the others abstain.  Does this suggest F13's slow-drift signature is
    genuinely ambiguous in a 10–50 h window, or that the representations
    lose the drift signal?

19. **V2_TEXT efficiency argument.** The authors note V2_TEXT achieves
    comparable accuracy at a fraction of the token cost.  Is this a valid
    practical advantage, or is it confounded by the fact that V2_TEXT
    embeds more domain knowledge (pre-computed thresholds, temporal
    interpretations)?

20. **Generalisability.** Results cover 4 of 28 TEP fault types.  What
    specific caveats should accompany any publication of these results?
    Could the ranking plausibly reverse for fault types not tested (e.g.,
    faults with subtle multivariate signatures that CGTIME_STATS might
    capture better)?

### 4.5 Additional analysis

21. **Missing analyses.** Are there analyses that should have been performed
    but were not?  Consider: per-class pairwise tests, effect-size
    reporting (Cohen's h or similar), cost-normalised comparisons,
    calibration analysis (are confidence-like signals in reasoning_summary
    calibrated?), inter-rater reliability between reps.

22. **Robustness checks.** What sensitivity analyses would strengthen the
    conclusions?  For example: leave-one-class-out accuracy, accuracy
    excluding F13, alternative abstention scoring, alternative bootstrap
    schemes (e.g., BCA bootstrap, permutation test).

---

## 5 — Requested deliverables

Please provide:

1. **Structured finding list** — numbered, with severity (CRITICAL / MAJOR /
   MINOR / INFORMATIONAL) and clear recommendation for each.

2. **Overall verdict** — GO / GO-with-reservations / NO-GO for publication
   of these results, with conditions if GO-with-reservations.

3. **Suggested rewording** — for any conclusion the reviewer considers
   overclaimed or underclaimed, provide specific alternative phrasing.

4. **Priority ranking** — if additional experiments or analyses are
   recommended, rank them by impact-to-effort ratio.

---

## 6 — Reference materials

The following materials are available for the review:

- `EXPERIMENT_DESIGN.md` — Full protocol documentation (reproduced above in §1)
- `ablation_results/ablation_evaluation.json` — Machine-readable results (reproduced above in §2)
- `ablation_results/ablation_report.md` — Human-readable evaluation report
- `ablation_results/inference_results.jsonl` — Raw inference outputs (180 records)
- `ablation_representations.py` — Representation generators (~750 lines)
- `ablation_runner.py` — Inference runner (~530 lines)
- `ablation_evaluate.py` — Evaluation and statistical analysis (~580 lines)
- `ablation_results/manifest.json` — Case manifest with file mappings
- `ablation_results/provenance.json` — SHA-256 hash of code + config + manifest + examples

All code and data are available for inspection upon request.
