# Experiment 3 post-freeze provenance/runtime-validation hotfix 002

**Status:** candidate hotfix discovered before the first experimental
simulation

**Original freeze:** commit
`b02e93f92bf6fa85a4fd0a2e010bac365a3a7c89`, tag
`exp3-heldout-frozen` (unchanged)

**Hotfix 001:** commit
`cdba0202435d1c97ea79cfff586e59534ce9baad` (unchanged)

## Discovery

After hotfix 001, the pre-simulation invocation for `EXP3-N-001`, attempt `0`,
primary seed `310001` stopped in the runtime gate with:

```text
MATLAB product date mismatch.

ACTUAL_MATLAB_DATE=<28-Jul-2025>
EXPECTED_MATLAB_DATE=<June 30, 2026>
```

## Actual versus expected

Direct API capture on the installed runtime established:

```text
ver('MATLAB').Date = 28-Jul-2025
version('-date')   = June 30, 2026
```

The frozen field `matlab_date` contained the latter value, while the generator
compared it with the former API. The two values were correct outputs for
different metadata properties but were assigned one ambiguous meaning.

## Root cause

The failure was a field-semantic mismatch between frozen provenance metadata
and the MATLAB API used for runtime validation. The exact full version,
release, build, architecture, MATLAB root, and installed runtime were otherwise
the pre-specified values.

## Boundary evidence

The runtime assertion executes before model loading and before `rng(seed,
'twister')` or `sim`. The generator had already created the raw output
directory, so the precise boundary is: **output directory created, but no
scientific output created**.

- `sim_called = false`;
- run RNG consumed = `false`;
- workbooks created = `0`;
- attempt log created = `false`;
- final manifest created = `false`;
- scientific outcome observed = `false`;
- output directories created = `true`;
- directories empty = `true`;
- signal inspection and inference = `0`.

## Fix

Runtime provenance now uses one explicit name per API-derived property:

| Field | Source API | Expected value |
|---|---|---|
| `matlab_version_full` | `version` | `25.2.0.3312555 (R2025b) Update 6` |
| `matlab_release` | `version('-release')` | `2025b` |
| `matlab_build` | parsed fail-closed from `version` | `3312555` |
| `matlab_product_date` | `ver('MATLAB').Date` | `28-Jul-2025` |
| `matlab_runtime_update_date` | `version('-date')` | `June 30, 2026` |

Generator, case plan, protocol, runtime report, attempt-log schema, verifier,
and tests use these semantics consistently. No date conversion or permissive
fallback was introduced; every identity check remains exact and fail-closed.

## Version/hash delta

The machine-readable companion
`phase_b/exp3/EXP3_POST_FREEZE_HOTFIX_002.json` records the complete
before/after SHA-256 set. Final candidate hashes are:

<!-- HASH_TABLE_START -->
| Artifact | Hotfix 002 candidate SHA-256 |
|---|---|
| Protocol | `e337a2942a0a0d4d840e3fd3789ff1165b78cf9b0e9a7de5e824e4b589bc3237` |
| Runtime report | `425242736ea11b69f0980b7e98065cdbbe7df51d01b7e680a6359ce1a934f326` |
| Attempt-log schema | `f0b4b54471bcf9f81da772616d7076feb7700bf1ffe356bef165db24e96a72de` |
| Case plan | `967423e16c257a78453c91a28bc5730b016649ef8df3d4fd582fdc55de29cdf4` |
| Generator | `f1cf1647df149e26bee94281e3c55ee1561dce143be942fa361733458268bd6f` |
| MATLAB runtime regression | `4f9f206332edc1716c042649d8bf5c952b69875e4f258949e1cdce45eadd79bd` |
| RNG probe | `d21ffaba3ceaf5796ef2f45caf8388c9bc58122c4b9c25fe4dd97dec37d67dbb` |
| Verifier | `794a7a7e214011776d02796f881bb900811cc52f19ce44a804dddca6c6a9ee3f` |
| Python regression suite | `3c162cb17a78bc36f40ec9b4d9237566b92d41d344377a53b563c0a397a32392` |
<!-- HASH_TABLE_END -->

> **No scientific protocol element was changed. The correction aligns runtime
> provenance metadata with the actual MATLAB API semantics and occurs before
> the first experimental simulation or observation of any Exp3 outcome.**

## Restart rule

After micro-audit and formalization, the first case remains:

- `EXP3-N-001`;
- attempt `0`;
- seed `310001`.

Attempt `1` is not authorized because no simulator attempt was executed or
recorded.
