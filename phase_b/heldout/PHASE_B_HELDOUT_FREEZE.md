# Phase B held-out freeze

## Freeze boundary

This record freezes the mechanically audited Phase B held-out before any V2,
FoT, threshold, similarity, plotting, or diagnostic analysis of these cases.
The selected files are exactly the 15 rows in
`phase_b_heldout_manifest.csv`. Other local simulator outputs are outside this
freeze and must not be substituted.

Raw workbook bytes are intentionally not committed. Their filename, byte size,
and SHA-256 are the immutable identifiers. Run:

```bash
python phase_b/heldout/verify_heldout_integrity.py \
  --data-dir tep_heldout/mode1
```

The verifier performs structural and finite-value integrity checks only.

## Provenance

- project branch at freeze: `phase-b-fot`;
- project pre-freeze HEAD: `145b6b79c59c352e06028166185bad3c9fb49607`;
- dataset reference commit: `309b944f35ac440ff0c70616947ffe723c766e14`;
- simulator commit: `a0413e16c940f0fc8b554d6a86248020d7fb7527`;
- simulator relationship: direct parent of the dataset reference commit;
- model: `MultiLoop_mode1`;
- MATLAB/Simulink: R2025b;
- solver: `ode45`;
- start/stop: 0/50 h;
- saved interval: `1/60` h = 1 min;
- custom setpoints: none;
- manual RNG seed: none recorded or set by the preserved scripts.

The source-level comparability decision and exact file hashes for the isolated
simulator are documented in `SIMULATOR_PARENT_AUDIT.md`.

## Frozen held-out artifacts

| Artifact | SHA-256 |
|---|---|
| `phase_b_heldout_manifest.csv` | `610c8a5fa6e763c25a9f9602a7e095c5fe850ed41b22552b0b92cec7edb450a3` |
| `generation/generate_heldout_mode1.m` | `a1aec546d977589a7b69238d84dbc456058b7b420f07d7824cc55ae54d96fdc9` |
| `generation/generate_phaseB_extra_runs.m` | `0230f834a98604e8330ef3d413bf944cd733f7ad36595b8d67b06a86693f073b` |
| `verify_heldout_integrity.py` | `92ced75eee649c16e929b75f780efa4dad3a22a82dcdf5b7691aa9c5ce1c5c9f` |

Reference audit environment: CPython 3.13.9 and openpyxl 3.1.5.

## Phase A immutability check

The following Phase A frozen files were hashed before creating the Phase B
held-out artifacts and must be identical afterward:

| Frozen file | SHA-256 |
|---|---|
| `code/verbalizer_config_v2.json` | `552a0b8a9cf9e416de77daa7aca2d8dee152a2700bbfaab4ae5e039081712519` |
| `code/tep_verbalize_v2.py` | `3a9129b6353cac6f8c9e02281282f137dd07885b1f882ca633ee9d6bf52393be` |
| `code/evaluate_verbalizer_v2.py` | `972e06fa29bee5a58d57ca757bd158c5cddaa2f4ed12eb5c739169c7fef79a92` |
| `code/tep_features.py` | `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c` |

No Phase A file, threshold, feature, verbalizer, evaluator, configuration, or
paper is part of this freeze commit.

## Known reproducibility limits

- The initial MATLAB RNG state was not recorded, so the random draws cannot be
  regenerated bit-for-bit from the scripts alone.
- The first F1 batch-11 script state and a separate Normal-14 script were not
  retained; their recorded command sequences are documented in
  `HELDOUT_GENERATION_SUMMARY.md`.
- The macOS MEX binary is not a blob in the parent upstream commit. Its exact
  local hash and equality with the dataset checkout copy are recorded in the
  simulator audit; the corresponding C source is a parent/child-identical Git
  blob.

These limits do not alter the frozen identity of the existing workbooks,
because the manifest records their exact sizes and hashes.

## Version-control marker

The intended commit subject is:

```text
Freeze independent Phase B held-out dataset manifest
```

The intended annotated tag is `phase-b-heldout-frozen`, with annotation:

```text
Independent TEP held-out dataset frozen for Phase B evaluation
```
