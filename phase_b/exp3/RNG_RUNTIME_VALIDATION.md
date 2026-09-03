# Experiment 3 RNG and runtime technical validation

**Status:** technical evidence acquired before Experiment 3 protocol freeze

**Scope:** sentinel-only simulator plumbing; no Experiment 3 seed or run used
**Diagnostic inspection:** none

## Runtime capture

The runtime was queried with:

```matlab
version
version('-release')
version('-date')
ver('MATLAB')
ver('Simulink')
computer
matlabroot
```

The exact captured identity was:

| Field | Captured value |
|---|---|
| MATLAB full version (`version`) | `25.2.0.3312555 (R2025b) Update 6` |
| MATLAB release | `2025b` |
| MATLAB runtime build | `3312555` |
| MATLAB product date (`ver('MATLAB').Date`) | `28-Jul-2025` |
| MATLAB runtime/update date (`version('-date')`) | `June 30, 2026` |
| Simulink version | `25.2` |
| Simulink release | `(R2025b)` |
| Simulink product date | `28-Jul-2025` |
| Simulink separate build | not exposed by `ver('Simulink')`; none recorded |
| Architecture | `MACA64` |
| `matlabroot` | `/Applications/MATLAB_R2025b.app` |

## Initialization and randomness audit

The model callbacks and plant block were read before the probe:

| Item | Observed value |
|---|---|
| `PreLoadFcn` | `Mode_1_Init` |
| `StopFcn` | `TEplot` |
| Plant S-function path | `MultiLoop_mode1/TE Plant/TE Code` |
| S-function identity | `temexd_mod` |
| S-function parameters | `[] rand()` |

`Mode_1_Init` and `TEplot` contain no call to `rand`, `randn`, or `rng`.
`load_system('MultiLoop_mode1')`, including `PreLoadFcn -> Mode_1_Init` and
loading `Mode1xInitial`, left the MATLAB RNG state unchanged. A simulation
advanced the MATLAB RNG state by exactly one `rand()` call: evaluation of the
stored S-function seed expression.

The controlled placement is therefore:

```matlab
load_system('MultiLoop_mode1'); % PreLoadFcn -> Mode_1_Init -> Mode1xInitial
dist = ...;                     % configure the planned physical condition
rng(seed, 'twister');           % final random-relevant operation
sim('MultiLoop_mode1');
```

No random-consuming operation may occur between `rng` and `sim`. The generation
script keeps these statements adjacent and records the explicit run seed and
algorithm in the attempt log.

## Sentinel-only empirical result

The validation used seeds outside the Experiment 3 allocation `310001–310030`.
The complete numeric matrix `[tout, simout, xmv]` had shape `3001 x 54`; it was
compared mechanically in memory and no XMEAS/XMV trajectory was interpreted.

| Comparison | Result |
|---|---|
| Same seed `987654321`, `isequal` | `true` |
| Same seed, maximum absolute difference | `0` |
| Same-seed output SHA-256 | `ce64df11668eafc5e1ab7516ff9667614b0517f6ccd4df57eab94fb07b507c42` |
| Different seed `123456789`, `isequal` | `false` |
| Different-seed maximum absolute difference | `131.55889448158541` |
| Different-seed output SHA-256 | `60e5f58c53458d9cc99d653391a459f41230e70fb2669e5c47eb0c86512950d9` |

This evidence establishes technical reproducibility for the validated runtime:
the same sentinel seed and clean initialization procedure reproduce the same
numeric realization exactly, while a different sentinel seed changes it. It
does not assess fault strength, feature separability, verbalizer behavior, or
FoT performance.

The reproducible probe is implemented in
`phase_b/exp3/validate_exp3_rng_runtime.m`. It is not an Experiment 3 generator
and must never be run with Experiment 3 allocated seeds.
