# code/ — Phase A implementation

Frozen implementation of the Phase A numerical-evidence-to-neutral-text pipeline.
All thresholds, features, and renderer logic were frozen before validation and test
evaluation (freeze-before-test discipline).

## Core modules

| File | Description |
|---|---|
| `tep_features.py` | Feature extraction from TEP time-series workbooks |
| `tep_verbalize.py` | Original verbalizer (V1, superseded) |
| `tep_verbalize_v2.py` | Frozen V2 neutral-text renderer |
| `tep_characterize.py` | Original characterization script (V1) |
| `tep_characterize_v2.py` | V2 characterization with temporal signatures |
| `calibrate_thresholds_v2.py` | Reproducible threshold calibration from development data |
| `evaluate_verbalizer_v2.py` | Verbalizer evaluation harness |
| `verify_injection_time_v2.py` | Injection-time verification against known TEP schedule |
| `characterize_fot_communication_payload.py` | FoT communication payload size characterization |
| `verbalizer_config_v2.json` | Frozen V2 renderer configuration |

## Tests

| File | Description |
|---|---|
| `test_features.py` | Unit tests for feature extraction |
| `test_verbalize_v2.py` | Unit tests for V2 renderer |
| `test_calibrate_thresholds_v2.py` | Threshold calibration reproducibility tests |
| `test_characterize_fot_communication_payload.py` | Communication payload characterization tests |

## Derived data

`tep_analysis_v2/` contains intermediate CSV/JSON outputs from development-data
analysis: threshold calibration, feature tables, temporal signatures, and window
summaries. These are deterministic outputs of the scripts above applied to
development batches.

`tep_cache/` contains cached TEP workbook extracts used to speed up repeated runs.
