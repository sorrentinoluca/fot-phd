# Phase B independent held-out generation summary

## Frozen design

The frozen design contains 15 newly simulated physical cases:

| Offline class metadata | Run identifiers | Count |
|---|---|---:|
| Normal | 12, 13, 14 | 3 |
| F1 | 11, 12, 13 | 3 |
| F8 | 11, 12, 13 | 3 |
| F10 | 11, 12, 13 | 3 |
| F13 | 11, 12, 13 | 3 |

The class and fault identifiers are offline provenance metadata. This freeze
does not pass them to a verbalizer and performs no diagnostic evaluation.

## Generation groups

The manifest distinguishes two chronological groups:

- `initial_heldout_batch_11`: the four selected target-fault run 11 files;
- `phase_b_extra_runs`: fault runs 12–13 and Normal runs 12–14.

All runs used the isolated pre-setpoint simulator at upstream commit
`a0413e16c940f0fc8b554d6a86248020d7fb7527`, MATLAB/Simulink R2025b,
`MultiLoop_mode1`, solver `ode45`, and `StopTime=50` h. No custom setpoint or
manual RNG seed was used. The source audit is in `SIMULATOR_PARENT_AUDIT.md`.

## Preserved generation scripts

Two scripts were copied byte-for-byte from the isolated simulator:

| Script | SHA-256 | Recorded use |
|---|---|---|
| `generation/generate_heldout_mode1.m` | `a1aec546d977589a7b69238d84dbc456058b7b420f07d7824cc55ae54d96fdc9` | initial batch-11 generation |
| `generation/generate_phaseB_extra_runs.m` | `0230f834a98604e8330ef3d413bf944cd733f7ad36595b8d67b06a86693f073b` | F1/F8/F10/F13 runs 12–13 and Normal 12–13 |

The preserved state of `generate_heldout_mode1.m` loops over faults 2–21. The
contemporaneous generation note records that F1 run 11 was executed first as a
single test and the script was then left in its continuation state for faults
2–21. No distinct pre-edit script for that first F1 call was retained.

Normal 14 was subsequently generated with the same loaded model and the
recorded commands:

```matlab
dist = zeros(1,28);
simOut = sim('MultiLoop_mode1');
dataToSave = [tout, simout, xmv];
```

No separate Normal-14 script artifact was retained. These are provenance
limitations for exact procedural replay; the manifest nevertheless freezes the
exact bytes of all 15 resulting workbooks.

## Output schema and mechanical checks

Every selected workbook has one worksheet named `Sheet1`, 3001 data rows, and
54 columns:

```text
Time (h), XMEAS-1 ... XMEAS-41, XMV-1 ... XMV-12
```

The audit checked only:

- XLSX ZIP/container validity;
- exact header and dimensions;
- numeric finiteness, NaN absence, and Inf absence;
- Time start/end, strict monotonicity, and constant sampling interval;
- full 0–50 h length as a mechanical indication of no early stop;
- byte size and SHA-256.

All 15 files meet these checks. Time is `0...50` h inclusive with constant
interval `1/60` h = 1 min. No XMEAS/XMV mean, standard deviation, feature,
threshold, plot, similarity, or diagnostic interpretation was computed.

The field `complete_no_early_stop` in the manifest means only that the workbook
contains the expected 3001 samples and reaches 50 h. It does not infer plant
state from signal values.

## Generation warnings retained

The generation notes record two warning families:

- transient macOS MEX temporary-path messages;
- automatic temporary enlargement of the Variable Time Delay buffer.

The simulations completed and the model was not changed to suppress these
warnings. Runs were not selected or regenerated based on their signal content.

## Storage policy

Raw workbooks remain under the ignored local directory
`tep_heldout/mode1/`. No `.xlsx` file is versioned. The repository contains only
the manifest, source audit, preserved scripts, integrity verifier, and this
synthesis of the two contemporaneous local generation summaries.
