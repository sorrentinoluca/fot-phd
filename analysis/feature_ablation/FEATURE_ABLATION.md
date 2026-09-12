# Leave-one-feature-out ablation of the V2 structured signature

**Status: exploratory, development-only, negative on its original question.**

This analysis was run to test a specific claim: *removing any one of the four
primary features degrades class separability.* **The data do not support that
claim.** What they support is narrower and is stated in §5.

## 1. Scope and guarantees

- Input: `code/tep_analysis_v2/` development tables only — Normal blocks N1–N5
  and fault batches 1–5 for F1, F8, F10, F13. The loader in
  `evaluate_verbalizer_v2.load_development_cases` raises if anything else
  appears, so the scope is enforced rather than merely documented.
- Thresholds: frozen `code/verbalizer_config_v2.json`, unchanged.
- No classifier is trained, no weight is learned, no prototype is built.
- Nothing under `ablation/`, `phase_b/`, `icl/`, `reproducibility/` or any
  `tep_*_v2/` directory is read or modified. This is **not** the frozen
  representation-strategy ablation in `ablation/`, which compares V2_TEXT
  against RAW_FEATURES / CGTIME_STATS / SAX_SYMBOLIC. Different question,
  different artifact.

## 2. What is ablated

The frozen signature is 41 XMEAS × 17 components. The 17 components partition
into five families:

| Family | Components | Underlying feature |
|---|---|---|
| `level` | 1–4 | `shift_sigma` |
| `trend` | 5–8 | `slope_sigma_h` |
| `residual` | 9–11 | `residual_std_ratio` |
| `diff` | 12–14 | `diff_std_ratio` |
| `rapid` | 15–17 | derived: residual **and** diff jointly active |

An arm masks the components of one or more families and recomputes the frozen
similarity `1 - mean|a-b|`. Because the similarity is a **mean** and not a sum,
arms of different dimensionality remain on the same scale.

Since `rapid` is derived from `residual` and `diff`, it is not computable once a
parent is removed. Removal is therefore reported under two policies: *coherent*
(`rapid` goes with its parent) and *isolated* (`rapid` retained, confounded by
construction). Both are reported so the coupling cannot be mistaken for the
result.

## 3. Endpoints

- **Class separation margin** — the frozen evaluator's definition: within-class
  median similarity minus the highest between-class median similarity.
- **Per-case margin** — the same quantity computed per case, giving 25 paired
  values for a two-sided sign-flip permutation test against FULL
  (100,000 permutations, seed 20260911).
- **Leave-one-out 1-NN accuracy** over the 25 development cases under the frozen
  similarity.

## 4. Results

Class-level separation margins, macro mean, worst class, and LOO 1-NN:

| Arm | comps/var | F1 | F8 | F10 | F13 | Normal | macro | worst | 1-NN |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| FULL | 17 | 0.07903 | 0.05152 | 0.01188 | 0.03300 | 0.02102 | 0.03929 | 0.01188 | **1.00** |
| drop_level | 13 | 0.05634 | 0.04978 | 0.01284 | 0.02861 | 0.02331 | 0.03418 | 0.01284 | 1.00 |
| drop_trend | 13 | 0.07786 | 0.05259 | 0.01225 | 0.03922 | 0.02068 | 0.04052 | 0.01225 | 1.00 |
| drop_residual (+rapid) | 11 | 0.08502 | 0.04719 | 0.00935 | 0.02827 | 0.01438 | 0.03684 | 0.00935 | 1.00 |
| drop_diff (+rapid) | 11 | 0.12162 | 0.06423 | 0.00956 | 0.02716 | 0.01918 | 0.04835 | 0.00956 | 1.00 |
| drop_residual_only | 14 | 0.06669 | 0.04541 | 0.01078 | 0.03277 | 0.01609 | 0.03435 | 0.01078 | **0.96** |
| drop_diff_only | 14 | 0.09578 | 0.05722 | 0.01138 | 0.03169 | 0.02030 | 0.04327 | 0.01138 | 1.00 |
| drop_rapid | 14 | 0.09585 | 0.05657 | 0.01138 | 0.03038 | 0.02030 | 0.04289 | 0.01138 | 1.00 |
| keep_only_level | 4 | 0.13834 | 0.05964 | 0.00972 | 0.04668 | 0.01410 | 0.05370 | 0.00972 | 0.96 |
| keep_only_trend | 4 | 0.08312 | 0.04116 | 0.01010 | 0.01925 | 0.01715 | 0.03415 | 0.01010 | 0.92 |
| keep_only_residual | 3 | 0.12957 | 0.10010 | 0.01067 | 0.03760 | 0.03150 | 0.06189 | 0.01067 | 0.96 |
| keep_only_diff | 3 | 0.00102 | 0.01372 | 0.01524 | 0.02033 | 0.00407 | 0.01087 | 0.00102 | 0.96 |
| keep_only_location (level+trend) | 8 | 0.11347 | 0.04602 | 0.00800 | 0.02363 | 0.01315 | 0.04085 | 0.00800 | 0.96 |
| keep_only_variability (residual+diff+rapid) | 9 | 0.04472 | 0.05640 | 0.01338 | 0.03591 | 0.02520 | 0.03512 | 0.01338 | **1.00** |

Paired per-case margin change against FULL (sign-flip permutation, two-sided):

| Arm | mean Δ | degraded / 25 | p |
|---|---:|---:|---:|
| drop_level | −0.00352 | 12 | 0.0886 |
| drop_trend | **+0.00213** | 6 | 0.0059 |
| drop_residual (+rapid) | −0.00415 | 18 | 0.0266 |
| drop_diff (+rapid) | **+0.00896** | 13 | 0.0217 |
| drop_residual_only | −0.00677 | 21 | 0.00004 |
| drop_diff_only | **+0.00381** | 13 | 0.0156 |
| drop_rapid | **+0.00368** | 12 | 0.0199 |

LOO 1-NN errors, where any: `drop_residual_only` → F8/B2 classified F1;
`keep_only_level` → F10/B3 → Normal; `keep_only_trend` → F8/B3 → F13 and
F13/B4 → F8; `keep_only_residual` → F13/B2 → F8; `keep_only_diff` → F8/B2 → F1;
`keep_only_location` → F13/B4 → F8.

## 5. What the data actually support

**Negative on the original claim.** Removing `trend`, `diff`, or `rapid`
*increases* the mean per-case margin, and every one of those removals keeps LOO
1-NN at 25/25. `keep_only_variability` — dropping `level` and `trend` entirely,
9 components per variable instead of 17 — also holds 25/25 and has the **best
worst-class margin of any arm** (0.01338 vs 0.01188 for FULL). On this endpoint
the four-feature set is not minimal; a reviewer running this ablation would
conclude that the location features can be dropped.

**What the data support, and how strongly:**

1. *No single feature family is sufficient.* Every keep-only-one arm loses
   perfect leave-one-out separability (0.92–0.96). The representation cannot be
   reduced to one descriptor.
2. *`residual_std_ratio` is the only family whose single removal breaks perfect
   LOO separability — an indication, not a demonstration of necessity.* Three
   facts, all read from `feature_ablation_results.json`:

   - `drop_residual_only` (residual removed, `rapid` retained) is the only
     single-family removal that breaks perfect LOO separability: LOO 1-NN
     **0.960**, with F8/B2 driven to **−0.01503**.
   - It also degrades the most per-case margins of any single-family removal,
     **21 of 25** (p = 4×10⁻⁵), against 13 of 25 for the next one
     (`drop_diff_only`), 12 for `drop_level` and `drop_rapid`, 6 for `drop_trend`.
   - The coherent removal `drop_residual` (residual **and** its derived `rapid`)
     keeps LOO 1-NN at **1.000**, yet also drives F8/B2 negative, to **−0.01150**.

   The negative margin is therefore **not unique to one arm**: it appears whenever
   residual evidence is removed, in either form, and appears for no other family.
   In both arms the competing class is F1 — between-class median similarity 0.90832
   and 0.88941 respectively, the highest in each case — so what the data support is
   an association between removing residual evidence and the collapse of the F8/B2
   margin towards F1, not that `residual_std_ratio` is individually necessary. The
   family stays in the set on design grounds; this margin indication is the only
   empirical support it has.

**Per-class specialisation is visible but does not generalise into necessity.**
`level` carries F1 (removing it costs F1 29% of its margin, the largest single
loss in the table); `residual` carries F10, F13 and Normal. But `trend` is not
supported for any class, including F13, the drift fault it was meant to
describe: `drop_trend` *raises* the F13 margin from 0.03300 to 0.03922.

## 6. Why this endpoint is weak evidence either way

The similarity is an unweighted mean of absolute component differences. A family
that is inactive for a given class contributes near-identical values to both the
within-class and between-class terms, so it **dilutes** that class's margin. The
metric therefore rewards removing any family not exercised by the evaluation
set. With only four fault mechanisms in scope (F1 step, F8/F10 random variation,
F13 slow drift) and five realisations each, a representation designed for
*coverage across mechanisms* is structurally penalised. "Removal improves the
margin" is consequently weak evidence of dispensability — but it is equally weak
as a defence, which is why §5 does not claim one.

More directly: separability of a 697-component vector under 1-NN is not the
property Phase A was designed for. Phase A was designed so that a neutral text
renders the mechanism in a form a peer agent's LLM can reason about. Those two
properties are not the same, and this ablation measures only the first.

## 7. Limits

- 25 cases, 5 per class. Any margin difference of this size is within what 5
  realisations can produce by chance for most arms; only `drop_residual_only`
  and the keep-only arms separate clearly from FULL.
- Four of 28 TEP faults. Results do not transfer to unexercised mechanisms.
- Development data only, by design. Nothing here was checked on validation or
  held-out test data, and nothing here licenses reopening them.
- The permutation test treats the 25 per-case margins as exchangeable under the
  null. They are not fully independent: margins share the same similarity matrix.
  The p-values are indicative, not confirmatory.

## 8. Provenance

- Repository commit at run time: `5effe26`.
- Script: `feature_ablation.py`; full numeric output: `feature_ablation_results.json`.
- Runtime: CPython 3.10.12, numpy 2.2.6, pandas 2.3.3. **This differs from the
  Phase A reference runtime** in `requirements.txt` (CPython 3.13.9,
  numpy 2.5.2, pandas 3.0.5). The script only reads frozen CSVs and performs
  elementwise arithmetic, so the deviation is low-risk, but it is declared here
  rather than hidden.
- Seed 20260911, 100,000 permutations per arm.
- Revised 2026-09-12: §5 claim 2 corrected. The earlier text called
  `residual_std_ratio` "individually necessary" and `drop_residual_only` "the only
  arm that drives a case margin negative"; both were wrong. `drop_residual` also
  produces a negative F8/B2 margin (−0.01150) while keeping LOO at 1.000. The same
  correction is applied to `docs/lit_review/criteri_scelta_descrittori.md` §5.2 and
  `docs/lit_review/DECISIONE_SCELTA_FEATURE_fase_A.md`; the three must agree on
  these figures.
