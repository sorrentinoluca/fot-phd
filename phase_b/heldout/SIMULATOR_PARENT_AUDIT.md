# Simulator parent audit for the Phase B held-out

## Scope and verdict

The held-out workbooks were generated from an isolated copy of the simulator at
commit `a0413e16c940f0fc8b554d6a86248020d7fb7527`. This commit is the direct
parent of dataset commit `309b944f35ac440ff0c70616947ffe723c766e14`:

```text
309b944f35ac440ff0c70616947ffe723c766e14
parent: a0413e16c940f0fc8b554d6a86248020d7fb7527
subject: Add simulations with sp changes
```

The targeted source audit found no change to the standard plant dynamics,
controller parameters, fault-delay routing, solver, stop time, or numerical
initial state. Commit `309b944f` adds an external setpoint layer; the parent is
the last self-contained standard workflow before that layer. The parent is
therefore mechanically comparable for standard, no-custom-setpoint runs. No
held-out signal values were used to reach this conclusion.

## Files compared

The comparison was performed with `git show`/`git diff` in the upstream clone,
not by assuming that the current working tree represented the parent.

| Standard simulator path | Parent to `309b944f` | Audit result |
|---|---:|---|
| `simulator/MultiLoop_mode1.mdl` | changed | external setpoint and display/output changes; common standard blocks retain parameters |
| `simulator/Mode_1_Init.m` | changed | same nominal constants and loaded numerical initial state; initialization variables relocated/commented in the SP workflow |
| `simulator/auto_run.m` | changed | batch/fault coverage and saved output schema only |
| `simulator/Mode1xInitial.mat` | changed container | `xInitial` structure and every stored numerical value are identical |
| `simulator/temexd_mod.c` | byte-identical | plant S-function source unchanged |
| `simulator/teprob_mod.h` | byte-identical | plant declarations unchanged |
| `simulator/TElib.mdl` | byte-identical | library unchanged |
| `simulator/tesys.mdl` | byte-identical | library unchanged |

The child `Mode1xInitial.mat` also contains workspace variables saved alongside
`xInitial`; this explains its different container hash. A recursive comparison
of the common `xInitial` structure found 35/35 signal entries equal, including
the 50-value plant-state vector, all scalar states, dimensions, and zero maximum
absolute difference for every numerical field.

## Structural model comparison

All XML system parts embedded in both text-packaged models were parsed and
compared by system part, SID, block type, and saved semantic parameters:

- parent blocks: 257;
- child blocks: 361;
- common blocks: 257;
- parent-only blocks: 0;
- child-only blocks: 104;
- common blocks with a semantic parameter difference: 1.

The one common difference is the setpoint-selection S-function wrapper at SID
`260::31`: its port count changes from `[2 2]` to `[3 2]` to accept
`custom_sp`. The 104 added blocks are the remaining `custom_sp` MATLAB Function
subsystems, `From Workspace` inputs, and scopes. No gain, numerator,
denominator, initial condition, delay parameter, or plant S-function parameter
changed in any common block.

The configuration-set comparison found exactly two differences:

```text
SaveFormat: Structure -> Array
SaveOutput: off -> on
```

These affect saved output, not the simulated dynamics. Both models save:

```text
StartTime = 0.0
StopTime  = 50
Solver    = ode45
FixedStep = Ts_base
```

In the parent, `Mode_1_Init.m` explicitly assigns `Ts_base=0.0005` and
`Ts_save=1/60`. In the child those assignments are commented, but the child MAT
container contains the same variables. The held-out generation used the parent
initialization, where the assignments are explicit.

## Plant, disturbance, and randomization path

The parent model retains:

```text
FunctionName = temexd_mod
Parameters   = [] rand()
```

The plant source, disturbance library, Variable Transport Delay block, its
routing, and its parameters are common blocks with no semantic difference.
Successive calls to `sim` therefore receive successive values from MATLAB
`rand()` as the S-function seed input. No manual `rng(seed)` appears in either
preserved generation script. This documents the generation mechanism; it does
not claim bitwise reproducibility of the random draws because their starting
MATLAB RNG state was not recorded.

## Isolated-copy verification

The following files in
`/Users/luker/fot-tep/tep_parent_a0413e16/simulator` are byte-for-byte equal to
`git show a0413e16:simulator/<file>`:

| File | SHA-256 |
|---|---|
| `MultiLoop_mode1.mdl` | `d2f6659f65935021d4b1813e7189be02e7ae9f5639b794e8edc4f2f3c5cddba8` |
| `Mode_1_Init.m` | `9dfb4e404c8c982c035fe47472020443b0a1d3f37b55425219968489d92d8933` |
| `auto_run.m` | `5b33275db0ade521e9e746a5e5a99edea6acbe45942f2831ab65808eaf16883f` |
| `Mode1xInitial.mat` | `40eaebc92badb04ad026e358cfd28ec9c778fcf2d24a1b8f5d85565854da2747` |
| `temexd_mod.c` | `0da41d939e5ab7ba122d7b70c124368ee0882fce40e775dba5d180e7a7e24e5e` |
| `teprob_mod.h` | `e8d07857030a837443ce947361335f2e6f2ade5d2fa54a85bcc5c4a6d9afe939` |
| `TElib.mdl` | `4605de6ca0e6da67626e2be6d5f328c735f8bf5a5a730dc67f558a3f1dabddba` |
| `tesys.mdl` | `53fb449f1fb592134a584dc8ad7d6c8cbbf2a33fa72fc87f5e795e8f4111c341` |

The macOS MEX binary is not present as a parent Git blob. The isolated copy is
byte-identical to the binary used by the `309b944f` checkout; its SHA-256 is
`68f632388cb698dd7b8c595000bc03c2e1d19200546b9d4357df90e3fc93af0d`.
Its corresponding C source is byte-identical across the two commits.

## Audit boundary

This audit establishes source/configuration comparability and the exact origin
of the isolated simulator. It does not inspect XMEAS/XMV distributions, run the
V2 verbalizer, calculate signatures, or infer fault behavior.
