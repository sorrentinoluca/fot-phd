# Experiment 3 post-freeze implementation hotfix 001

**Status:** implementation hotfix discovered before the first experimental
simulation

**Original freeze commit:**
`b02e93f92bf6fa85a4fd0a2e010bac365a3a7c89`

**Original freeze tag:** `exp3-heldout-frozen` (unchanged)

## Discovery

On 2026-09-03, the first pre-simulation invocation was attempted for
`EXP3-N-001`, attempt `0`, primary seed `310001`:

```matlab
record = generate_exp3_heldout('EXP3-N-001', 0)
```

Execution stopped in `assert_attempt_allowed` with:

```text
Unrecognized field name "attempt".

Error in generate_exp3_heldout>assert_attempt_allowed
assert(~any([prior.attempt] == attempt), 'EXP3:DuplicateAttempt', ...
```

## Boundary evidence

The failure occurred before creation of the output directory and before the
first call to `rng` or `sim`. Immediately afterward, both the output directory
and operational attempt log were absent. Consequently:

- `sim` was not called;
- no primary seed was consumed by a TEP simulation;
- no attempt was registered;
- no workbook or physical realization was created;
- no signal was inspected;
- no verbalization or inference was executed;
- no scientific outcome was observed;
- no scientific design element was modified.

## Root cause

When the operational attempt log does not yet exist, `read_attempt_log`
returns `attempts=[]`. The empty branch then created `prior=struct([])`, an
untyped empty structure without an `attempt` field. The expression
`[prior.attempt]` therefore raised an error before the duplicate-attempt check
could be evaluated.

## Fix

Only the empty local view was changed. It is now an empty structure carrying
the three fields subsequently read by the frozen policy logic:

```matlab
prior = struct('attempt', {}, 'structural_valid', {}, ...
    'technical_failure_reason', {});
```

Non-empty log handling, duplicate protection, seed checks, replacement
authorization, maximum attempts, simulation configuration, and all scientific
decisions are unchanged. Because the generator is self-hash-checked, the
companion machine-readable delta record authorizes the new generator hash while
preserving the original freeze manifest and tag unchanged.

## Version/hash delta

| Artifact | SHA-256 |
|---|---|
| Frozen original generator | `018b13d5e85a80e190b9d7a6931cfd40f0ee28639cb7ff8193dac2fb82aae813` |
| Hotfixed generator | `54d89c033414e67bfe1cacaaa879dd46d1391ed3c322452e275770adf8a38b24` |
| Unchanged case plan | `f2d27ef19d6b5f923cc33fe3329e8a3922800ec9eff34afc58b47c54c03e5b3b` |

> **No scientific protocol element was changed. The patch only fixes
> empty-state handling before the first simulator execution.**

## Restart rule

After audit of this hotfix, the first case remains:

- `EXP3-N-001`;
- attempt `0`;
- seed `310001`.

Attempt `1` is not authorized because no technical simulation attempt was
executed or recorded.
