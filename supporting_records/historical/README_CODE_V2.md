# FoT/TEP code v2 — development-only stage

This folder implements the methodological changes established by the audit.

## Files

- `tep_features.py` — threshold-free feature extraction.
- `test_features.py` — synthetic regression tests for normal/step/drift/oscillation/noise.
- `tep_characterize_v2.py` — development-only analysis of F1/F8/F10/F13 batches 1–5.

The original `tep_characterize.py` and `tep_verbalize.py` are intentionally not overwritten yet.

## Fixed facts encoded

- Dataset snapshot pinned to commit `309b944f35ac440ff0c70616947ffe723c766e14`.
- 10 batches exist per fault in that snapshot.
- Fault injection time is `10 h`, derived from the simulator chain `dist -> VariableTransportDelay(10) -> plant`.
- Development fault batches are `1..5`.
- Batches `6..7` (validation) and `8..10` (test) are explicitly blocked in `tep_characterize_v2.py`.
- `mode1_normal_500.xlsx` is split into ten non-overlapping 50 h blocks; N1–N5 are used in development.

## Run

```bash
python test_features.py
python tep_characterize_v2.py
```

`tep_characterize_v2.py` writes threshold-free CSVs to `tep_analysis_v2/`.

## Important design choice

`raw_std_ratio` is named **raw dispersion** and is never treated as synonymous with oscillation.
The core descriptors are:

- signed `shift_sigma`;
- signed `slope_sigma_h`;
- `residual_std_ratio`;
- `diff_std_ratio`.

The temporal window table is the primary artifact for deciding whether a phenomenon is transient or persistent. No final diagnostic thresholds are hardcoded here.

## Next step

Use only the generated development outputs to choose/freeze thresholds and temporal persistence rules. Only after that should the main verbalizer be patched and validation batches 6–7 opened.
