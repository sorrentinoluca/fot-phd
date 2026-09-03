# Experiment 3 post-freeze headless StopFcn hotfix 003

**Status:** candidate hotfix authorized before the replacement attempt

**Original freeze:** commit
`b02e93f92bf6fa85a4fd0a2e010bac365a3a7c89`, tag
`exp3-heldout-frozen` (unchanged)

**Hotfix 001:** commit
`cdba0202435d1c97ea79cfff586e59534ce9baad` (unchanged)

**Hotfix 002:** commit
`28130023a34eda778c04a001a9f631404bd6b9a6`, tag
`exp3-post-freeze-hotfix-002` (unchanged)

## Discovery and boundary

The first scientific invocation, `EXP3-N-001`, attempt `0`, primary seed
`310001`, passed its pre-simulation gates and reached `sim`. Simulink then
failed before returning normally because the model evaluated its plotting
callback:

```text
Simulink:Engine:CallbackEvalErr
Error evaluating 'StopFcn' callback of block_diagram 'MultiLoop_mode1'.
Callback string is 'TEplot'
Caused by: Unrecognized function or variable 'tout'.
```

The exact observed boundary is:

- `sim_called = true`;
- `sim_returned_successfully = false`;
- workbooks created = `0`;
- output size = `0`;
- output SHA-256 = empty;
- signal inspection = `false`;
- attempt log created = `true`;
- attempt 0 recorded as a technical failure = `true`;
- scientifically accepted output = `false`.

Because `rng(310001, 'twister')` and `sim` were reached, seed `310001` is
consumed and attempt `0` is consumed. Neither may be replayed.

## Static audit of `TEplot`

The complete script at
`tep_parent_a0413e16/simulator/TEplot.m` was inspected. It assumes `tout`,
`simout`, and `xmv`; builds display-only `TEdata` and `TEmvs` structures; and
creates figures, plots, labels, and UI controls. It contains no change to the
plant, `dist`, the initial state, solver or model parameters; no `rng`, `rand`,
or `randn`; no model save; and no write of simulation data needed by the
scientific pipeline. It is plotting/post-processing, not simulator dynamics.

## Root cause

The function-scoped generator is incompatible with a plotting-only `StopFcn`
that expects `tout` in its callback workspace. `StopFcn` runs before `sim`
returns the simulation outputs to the generator, so `TEplot` cannot resolve
`tout` there.

## Fix

The generator uses **temporary suppression of a plotting-only StopFcn that is
incompatible with function-scoped headless generation, with guaranteed
restoration of the original callback**.

The helper fails closed unless the loaded model has exactly `StopFcn = TEplot`.
It captures the original callback and in-memory `Dirty` state, constructs an
`onCleanup` guard before calling `set_param`, temporarily sets only `StopFcn`
to the empty string, and restores and verifies the exact callback and `Dirty`
state after success or exception. The generator adds no `save_system` call.
The on-disk model is required and tested to remain byte-identical.

Restoration failure produces a dedicated fail-closed exception containing
both the original generator exception and the restoration exception as causes;
the original error is therefore not silently masked.

## Scientific impact

The hotfix changes only non-scientific plotting/post-processing behavior
required for headless generation. Plant dynamics, random realization, fault
configuration, simulator parameters, output sampling, and the frozen
experimental design remain unchanged.

## Restart rule

The append-only technical-failure record authorizes exactly the frozen
replacement:

- `EXP3-N-001`;
- attempt `1`;
- replacement seed `1310001`;
- RNG algorithm `twister`.

No attempt is executed while preparing this hotfix.

## Version/hash delta

The machine-readable companion
`phase_b/exp3/EXP3_POST_FREEZE_HOTFIX_003.json` records the complete
hotfix-002-to-hotfix-003 before/after SHA-256 set. Candidate hashes are:

<!-- HASH_TABLE_START -->
| Artifact | Hotfix 003 candidate SHA-256 |
|---|---|
| Protocol | `bb1d74befcda0d31fd8908a7cc1ff602f22aed532bd064202f903ce9e570b13f` |
| Generator | `da419e5d48282af4ca36263e402a54d5b26055e07efed95fa3207020472facbe` |
| StopFcn helper | `7930dd867e069cd8513efc42285ff1797e110d2f3a2f2072a95a71f45ae82597` |
| StopFcn restoration helper | `b8e45d6c0773598f36b525f9fee118932eb5bb2b33f8cb3def67e7094dddcd05` |
| Attempt-policy MATLAB regression | `17c72cced1412cc016d33270eb367afb326ae619ad21d757fdc4c16026fcfa8e` |
| StopFcn MATLAB regression | `2aa1b3ff42d9c50275090fc7361222902aacd9bc6d961e0fc46e9fe6ec11442c` |
| Verifier | `158603283b086d2ddf2a34312392eb3ac91ad82b9289435b23157eb5e30aaf36` |
| Python regression suite | `a1d66381ed747c66d3065f88c0bc30d2b527d38bf7f5d97cc78bd43d9b28880f` |
<!-- HASH_TABLE_END -->

The pinned model SHA-256 before and after callback-management regression is
`d2f6659f65935021d4b1813e7189be02e7ae9f5639b794e8edc4f2f3c5cddba8`.
The append-only attempt-log SHA-256 at discovery is
`0b2f2e6bf3c82e85da72591919fade41033c63431202f2f97dae6bd1d59a9729`.
