# Federation over Text — TEP Phase A

This repository contains Phase A of a proof-of-concept Federation over Text
(FoT) study on the Tennessee Eastman Process. Phase A freezes and evaluates the
numerical time-series to neutral-text layer:

`time series -> structured numerical evidence -> neutral text`

It does not implement the later FoT reasoning experiment and does not present
the V2 verbalizer as a numerical fault classifier.

## Pinned provenance

- Upstream dataset: [mv-per/tennessee-eastman-dataset](https://github.com/mv-per/tennessee-eastman-dataset)
- Dataset commit: `309b944f35ac440ff0c70616947ffe723c766e14`
- V2 pre-validation freeze: commit `3fd960a192bafacbaabce9471e3c3614d6b2d2db`, tag `verbalizer-v2-pre-validation`
- Validation completion: commit `1d9c1617b56c19d2bc71dfef7b7902df0670b537`, tag `verbalizer-v2-validation-complete`
- Held-out test completion: commit `0a45817fd783513e23d58a35c55489404c95feec`, tag `verbalizer-v2-test-complete`
- Phase A completion tag: `phase-a-verbalizer-v2-complete`

The raw Tennessee Eastman dataset is deliberately not duplicated in this
repository. Workbooks, dataset clones, and local caches are excluded by
`.gitignore`.

## Repository map

- `code/tep_features.py`: frozen numerical feature layer.
- `code/tep_verbalize_v2.py`: frozen structured evidence and neutral renderer.
- `code/verbalizer_config_v2.json`: frozen V2 configuration and thresholds.
- `code/evaluate_verbalizer_v2.py`: frozen deterministic evaluator.
- `code/calibrate_thresholds_v2.py`: verification-only calibration reproducer.
- `code/verify_injection_time_v2.py`: development-only empirical timing check.
- `code/tep_analysis_v2/`: committed development analysis artifacts.
- `tep_validation_v2/`: committed out-of-development validation artifacts.
- `tep_test_v2/`: committed held-out test artifacts.
- `VERBALIZER_V2_FREEZE.md`: pre-validation specification and frozen hashes.
- `PHASE_A_STATUS.md`: final status and review caveats.

## Reproducing Phase A

The reference environment used for Phase A was CPython `3.13.9`. The dependency
versions actually used are pinned in `requirements.txt`.

### 1. Clone the project

```bash
git clone https://github.com/sorrentinoluca/fot-phd.git
cd fot-phd
```

### 2. Install dependencies

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

No separate development dependency file is required: the regression tests use
the Python standard library plus the runtime packages above.

### 3. Retrieve the pinned upstream dataset

Keep the upstream clone outside version control for this repository:

```bash
git clone https://github.com/mv-per/tennessee-eastman-dataset.git tennessee-eastman-dataset
git -C tennessee-eastman-dataset checkout 309b944f35ac440ff0c70616947ffe723c766e14
git -C tennessee-eastman-dataset rev-parse HEAD
```

The last command must print the pinned commit. The upstream repository may use
Git LFS for workbook delivery; Git LFS is not used by `fot-phd` itself.

The Normal workbook expected by the reproduction commands is:

```text
tennessee-eastman-dataset/simulations/mode_1/mode1_normal_500.xlsx
```

### 4. Reproduce the frozen calibration

The calibration command reads only Normal N1–N5, writes new verification
artifacts, and refuses to overwrite the frozen config or original calibration
reference:

```bash
python code/calibrate_thresholds_v2.py \
  --normal tennessee-eastman-dataset/simulations/mode_1/mode1_normal_500.xlsx \
  --output reproducibility/threshold_calibration_verification.json \
  --maxima-output reproducibility/normal_5h_window_maxima_recalculated.csv

python code/test_calibrate_thresholds_v2.py \
  --normal tennessee-eastman-dataset/simulations/mode_1/mode1_normal_500.xlsx
```

The four recalculated values must match both
`code/verbalizer_config_v2.json` and
`code/tep_analysis_v2/threshold_calibration.json` within absolute tolerance
`1e-12`. In the reference run, every absolute error is exactly zero.

### 5. Development workflow

Development and calibration are the only phases in which methodological
choices were made. `tep_characterize_v2.py` has guards restricting it to fault
batches 1–5:

```bash
cd code
python tep_characterize_v2.py
cd ..
```

The script downloads the pinned development files into ignored `tep_cache/`
storage and regenerates `code/tep_analysis_v2/`. Compare regenerated outputs
with the committed artifacts using `git diff`; do not alter frozen thresholds
to remove differences.

The independent injection-time consistency check also uses development data
only. After the development cache exists:

```bash
python code/verify_injection_time_v2.py \
  --cache-dir code/tep_cache \
  --normal code/tep_cache/mode1_normal_500.xlsx \
  --config code/verbalizer_config_v2.json \
  --output-dir reproducibility/injection_time \
  --report INJECTION_TIME_VERIFICATION.md
```

### 6. Run software and regression tests

```bash
python code/test_features.py
python code/test_calibrate_thresholds_v2.py \
  --normal code/tep_cache/mode1_normal_500.xlsx
python code/test_verbalize_v2.py
```

`test_verbalize_v2.py` includes development-only regression checks and expects
the ignored development cache. Tests verify frozen properties; they must never
be used to tune thresholds against validation or test results.

### 7. Reproduce validation artifacts

Validation consists exclusively of F1/F8/F10/F13 batches 6–7 and Normal
N6–N7. The committed raw-to-structured results, anonymous text, metadata, and
metrics are under `tep_validation_v2/`.

`tep_validation_v2/run_validation.py` recomputes the deterministic evaluator
tables from the committed structured cases and the pinned Normal workbook. It
must be run only after checking the frozen hashes in
`VERBALIZER_V2_FREEZE.md`. It is not part of calibration and must not feed back
into configuration or thresholds:

```bash
python tep_validation_v2/run_validation.py
git diff -- tep_validation_v2
```

### 8. Reproduce held-out test artifacts

The held-out test consists exclusively of F1/F8/F10/F13 batches 8–10 and
Normal N8–N10. Its committed artifacts are under `tep_test_v2/`.

Run this step separately and only after development and validation decisions
are frozen:

```bash
python tep_test_v2/run_test.py
git diff -- tep_test_v2
```

The test runner applies the frozen representation, `top_k=4`, and
`similarity = 1 - mean(abs(a-b))`. It does not authorize tuning or creation of
V2.1.

## Reproduction boundaries

- **Frozen-result reproduction** verifies hashes, recalculates thresholds, and
  compares regenerated artifacts with committed outputs.
- **Development workflow** is limited to N1–N5 and fault batches 1–5.
- **Out-of-development validation** is N6–N7 and fault batches 6–7.
- **Held-out evaluation** is N8–N10 and fault batches 8–10.

These phases are deliberately separate. There is no single command that runs
calibration, validation, and test in sequence, because such automation would
make accidental feedback or tuning easier.

## Phase A results

The final independent review verdict is **GO WITH CAVEATS**. The caveats concern
reproducibility and documentation and are closed by the separate scripts and
records added after the scientific freeze. The frozen methodology and results
remain unchanged. See `PHASE_A_STATUS.md` and `INJECTION_TIME_VERIFICATION.md`.
