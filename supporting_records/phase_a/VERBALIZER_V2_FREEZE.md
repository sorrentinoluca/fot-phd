# Verbalizer V2 pre-validation freeze

This document freezes the V2 verbalizer before any validation batch is opened.
The freeze covers the numerical representation, thresholds, neutral renderer,
and offline evaluator. It does not claim diagnostic classification performance.

## Dataset provenance and split

- Dataset commit: `309b944f35ac440ff0c70616947ffe723c766e14`.
- Sampling interval: `1/60 h` (one minute).
- Fault injection time: `10 h`.
- Development: fault batches 1–5 and Normal blocks N1–N5.
- Validation: fault batches 6–7 and Normal blocks N6–N7.
- Held-out test: fault batches 8–10 and Normal blocks N8–N10.

Only development data were used to choose or audit the frozen representation,
thresholds, renderer, and evaluator. Validation and held-out test data were not
opened for this freeze.

The injection time was verified from the dataset source. In `auto_run.m`, the
disturbance vector is initialized to zero, `dist(faultNum)` is set to one, and
the simulation is then started. In `MultiLoop_mode1.mdl`, that vector is the
data input of a `VariableTransportDelay`; an explicit Constant block with value
`10` is connected to its delay input, and the delayed output is routed to the
plant `Disturbances` input. `InitialOutput` is not explicitly serialized in the
model; the compatible Simulink default is zero. Therefore the plant sees a zero
disturbance vector before 10 simulation-time units and the selected disturbance
after the delay. `StopTime=50`, the saved time axis in hours, and the observed
`1/60 h` sampling establish that the delay value is 10 hours.

## Frozen features and semantics

The primary features are computed per XMEAS and per five-hour window:

- `shift_sigma`: signed displacement of the window mean from the Normal
  baseline mean, divided by the Normal baseline standard deviation. Its
  magnitude measures level displacement; its sign records direction.
- `slope_sigma_h`: signed OLS slope in baseline-standard-deviation units per
  hour. It is local trend evidence, not by itself a diagnosis of drift.
- `residual_std_ratio`: standard deviation after linear detrending divided by
  the corresponding Normal residual standard deviation. It measures residual
  variability, not automatically oscillation.
- `diff_std_ratio`: standard deviation of first differences divided by the
  corresponding Normal first-difference standard deviation. It measures
  sample-to-sample variability.

`raw_std_ratio` is retained as a descriptive measure of overall dispersion but
is not a primary decision feature. Every `std_ratio` is a ratio of standard
deviations, not a ratio of variances. No FFT, wavelet, or other complex feature
is part of this freeze.

## Frozen thresholds

Threshold comparisons are strict (`value > threshold`, or absolute value for
signed features). Full-precision values from `verbalizer_config_v2.json` are:

| Feature | Threshold |
|---|---:|
| `abs(shift_sigma)` | `1.9695333234149084` |
| `abs(slope_sigma_h)` | `0.7468621213669596` |
| `residual_std_ratio` | `1.3681613543196571` |
| `diff_std_ratio` | `1.4051245046201666` |

They were calibrated only from Normal development blocks N1–N5, using 50
five-hour windows, maximum-over-41-XMEAS statistics, `alpha=0.05`, and rank 49.
The observed development calibration allows local Normal positives; the
renderer must report them as evidence rather than infer that the process is a
fault.

## Frozen temporal representation

The post-injection interval `[10 h, 50 h)` is represented by eight consecutive,
non-overlapping five-hour windows. The initial phase is the first two windows;
the late phase is the last two. For each feature and XMEAS, the structured
output preserves at least:

- `n_active_windows` and `active_fraction`;
- `positive_count`, `negative_count`, and `sign_consistency` for signed
  features;
- `longest_same_sign_run` for signed features, or `longest_run` for unsigned
  features;
- `first_active_window` and `last_active_window`;
- `early_active` and `late_active`, including their counts/fractions where
  represented.

The derived `rapid` evidence is true only when residual and first-difference
variability are both above their frozen thresholds for the same XMEAS and
window. It remains neutral numerical evidence and is not an oscillation label.

## Neutral renderer rules

The renderer is factual-first. It reports quantitative counts, directions,
runs, and early/late occurrence, for example that a threshold is exceeded in
`k/8` windows or that signs split between positive and negative windows.

It must not:

- emit fault IDs, true class labels, or prototype labels A/B/C/D;
- turn evidence automatically into diagnoses such as transient settling,
  persistent drift, oscillation, oscillatory instability, or periodicity;
- require every Normal window to be negative;
- change or duplicate frozen thresholds in rendering logic.

The intended pipeline is:

`time series -> structured numerical evidence -> neutral text -> reasoning/diagnosis`

## Evaluator representation: 17 components per XMEAS

For each XMEAS, `signature_vector()` emits the following components in this
exact order:

| # | Component | Normalization |
|---:|---|---|
| 1 | level `active_fraction` | active-window count divided by `n_windows` |
| 2 | level signed activity | `((positive_count-negative_count)/n_windows + 1)/2` |
| 3 | level `late_active_fraction` | active late-window count divided by the number of late windows |
| 4 | level `longest_same_sign_run` | run length divided by `n_windows` |
| 5 | trend `active_fraction` | active-window count divided by `n_windows` |
| 6 | trend signed activity | `((positive_count-negative_count)/n_windows + 1)/2` |
| 7 | trend `late_active_fraction` | active late-window count divided by the number of late windows |
| 8 | trend `longest_same_sign_run` | run length divided by `n_windows` |
| 9 | residual `active_fraction` | active-window count divided by `n_windows` |
| 10 | residual `late_active_fraction` | active late-window count divided by the number of late windows |
| 11 | residual `longest_run` | run length divided by `n_windows` |
| 12 | diff `active_fraction` | active-window count divided by `n_windows` |
| 13 | diff `late_active_fraction` | active late-window count divided by the number of late windows |
| 14 | diff `longest_run` | run length divided by `n_windows` |
| 15 | rapid `active_fraction` | jointly active-window count divided by `n_windows` |
| 16 | rapid `late_active_fraction` | jointly active late-window count divided by the number of late windows |
| 17 | rapid `longest_run` | run length divided by `n_windows` |

Thus each case has `41 * 17 = 697` scalar components. Counts and run lengths
are normalized only by window counts from the same case. Signed activity lies
in `[-1,1]` before the affine map and in `[0,1]` afterward. Every component is
therefore in `[0,1]`; the implementation also rejects non-finite or out-of-range
components.

No component normalization uses fault batches 6–10, Normal blocks N6–N10, or
statistics calculated by class. There are no learned normalization parameters.

## Evaluator metrics

Structured-signature similarity is:

`similarity(a,b) = 1 - mean(abs(a-b))`.

There are no weights: all 697 components contribute equally to the mean
absolute difference. Because every component is in `[0,1]`, each absolute
difference and its mean are in `[0,1]`, so the similarity has the valid range
`[0,1]`. The implementation does not need clipping because it validates the
input range.

Dominant-variable similarity uses Jaccard similarity on sets of XMEAS names.
The frozen value is `top_k = 4` per feature. The evaluator CLI permits an
override for exploratory use, but the pre-validation protocol must use 4. If
both dominant sets are empty, their union is empty: the Jaccard value is
reported as undefined and the pair is counted separately, rather than assigned
an arbitrary score.

The evaluator is deterministic and contains no LLM or classifier. True labels
are used only as offline ground truth for grouping cases. Reported distribution
summaries use median, first and third quartiles, minimum, and maximum.

## Validation reporting protocol fixed before opening validation

Validation is descriptive. Features, thresholds, representation, equal
weighting, and `top_k=4` remain frozen. No numerical success cutoff, including
any rule of the form `margin > X`, will be introduced.

For F1, F8, F10, F13 batches 6–7 and Normal N6–N7, report:

1. **Intra-class similarity.** With two cases per class there is one pair;
   report its raw similarity and identify that quartiles are not informative
   for a single value.
2. **Inter-class similarity.** For each class pair there are four cross-case
   pairs; report all values plus median, Q1, Q3, minimum, and maximum.
3. **Margin.** For each class, report its validation intra-class similarity
   minus the highest validation inter-class median involving that class. Treat
   this only as a descriptive difference.
4. **Dominant-variable Jaccard.** For each feature, report the top-4 Jaccard for
   the single within-class pair, or explicitly report an undefined empty-union
   case.
5. **Variable recurrence.** For every feature and class, report how often each
   XMEAS is top-4 across the two validation cases (`0/2`, `1/2`, or `2/2`).
6. **Comparison with development intervals.** Place validation values beside
   the frozen development raw distributions, median/IQR, and min/max. State
   whether validation observations fall inside or outside the development IQR
   and range, and report median deltas where the sample sizes make that useful.

These observations will show whether development properties persist outside
development; they will not be converted into a pass/fail classification rule.

## Known limitations

- Validation has only two cases per class, so intra-class uncertainty cannot be
  estimated reliably and recurrence counts are coarse.
- Adjacent windows from one simulation are temporally dependent.
- Normal thresholds were calibrated on development Normal data and are not a
  guarantee that every unseen Normal window is negative.
- Feature-wise thresholds do not directly control the union probability across
  all features and XMEAS variables.
- Equal-weight mean-L1 similarity can be dominated by the many components that
  are inactive or similar across cases.
- Jaccard is undefined when both dominant-variable sets are empty.
- Minimal time-domain features cannot always distinguish very slow oscillation
  from nonlinear transients, or rapid oscillation from increased stochastic
  noise variance.
- The evaluator measures structural stability and separability; it is not a
  diagnostic classifier and supplies no causal interpretation.

## Frozen file hashes

SHA-256 hashes were computed on the exact files frozen before validation:

| File | SHA-256 |
|---|---|
| `code/verbalizer_config_v2.json` | `552a0b8a9cf9e416de77daa7aca2d8dee152a2700bbfaab4ae5e039081712519` |
| `code/tep_verbalize_v2.py` | `3a9129b6353cac6f8c9e02281282f137dd07885b1f882ca633ee9d6bf52393be` |
| `code/evaluate_verbalizer_v2.py` | `972e06fa29bee5a58d57ca757bd158c5cddaa2f4ed12eb5c739169c7fef79a92` |
| `code/tep_features.py` | `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c` |

Any change to one of these files after this commit invalidates this freeze and
requires a new documented hash and version decision before validation results
are interpreted.
