# Experiment 3 — Fresh Prospective Physical-Run Extension

**Status:** `DRAFT FOR SCIENTIFIC AUDIT — NOT FROZEN`<br>
**Experiment:** prospective fresh physical-run replication on the same four TEP fault classes<br>
**Repository branch:** `main`<br>
**Protocol scope:** Experiment 3 only; Experiment 1 remains immutable

This document pre-specifies Experiment 3 before generation of any Experiment 3
physical run. It is not a report of results, does not open an existing held-out
set, and does not authorize simulation, verbalization, or LLM inference. The
protocol cannot be frozen until every item marked **BLOCKER BEFORE FREEZE** has
been resolved and recorded without inspecting diagnostic signal content.

The source-of-truth order used here is:

1. frozen machine-readable Experiment 1 artifacts and their hashes;
2. frozen held-out manifest and simulator provenance records;
3. frozen protocol and execution records;
4. narrative documentation only where it agrees with the artifacts above.

## 1. Purpose and research question

Experiment 3 asks one question:

> **Does the FoT transfer effect observed in Experiment 1 reproduce on fresh
> independent physical realizations of the same four fault classes?**

Operationally, this is a **prospective fresh-run replication on the same four
TEP fault classes**. It tests whether the Experiment 1 FoT contrast is observed
again when the unchanged pipeline is applied to newly simulated physical
realizations generated after this protocol is frozen.

The resulting 30-run dataset is the prospective Experiment 3 **held-out extension**.

It does **not** test new fault classes, cross-class transfer beyond the original
four classes, PV transfer, a new verbalizer, or a new FoT architecture. It does
not establish cross-domain validity.

## 2. Relationship to frozen Experiment 1

Experiment 1 is historical, complete, and immutable. Experiment 3 neither
reopens nor retunes it. All Experiment 1 predictions, outcomes, metrics,
manifests, hashes, and freeze tags remain unchanged.

Experiment 3 changes only the physical realizations supplied to the already
frozen analysis and inference stack. It retains:

- the same four TEP fault classes: F1, F8, F10, and F13;
- the same four-agent non-IID topology and opaque pseudolabel space;
- the same locally-unseen primary population;
- the same Conditions A, B, and E;
- the same verbalizer, knowledge artifacts, prompts, LLM configuration,
  aggregation, and evaluator logic.

The phrase *fresh* refers to newly generated simulator realizations. The phrase
*prospective* refers to fixing generation and analysis decisions before those
realizations are generated or inspected. Neither phrase implies a new domain
or new fault identity.

Experiment 1 remains addressable through its immutable boundary tags:

| Boundary | Frozen reference | Target commit |
|---|---|---|
| Original held-out | `phase-b-heldout-frozen` | `86baaa65e72cea22ecb89dd0e7b213aea5a1284b` |
| Protocol | `phase-b-protocol-frozen` | `3d86f64d43e14e7e0de520cb047ca1043bf9c1c0` |
| Execution schedule | `phase-b-execution-schedule-frozen` | `eef0bc58e5ab14fb0cd2aece180fb5b1b5a7962b` |
| Predictions before ground-truth evaluation | `phase-b-inference-frozen` | `11c34358e28e875cd5c7249061ac2b89ffcd42f4` |
| Evaluation results | `phase-b-results-frozen` | `45ec4eed65b263a5803ced7d01064c4672e81e86` |

## 3. Fixed sample size

The sample size is fixed before generation:

| Condition represented by the physical run | New physical runs |
|---|---:|
| Normal | 6 |
| F1 | 6 |
| F8 | 6 |
| F10 | 6 |
| F13 | 6 |
| **Total** | **30** |

Thus, the fault portion contains 24 physical runs: six realizations of each of
the same four fault classes used in Experiment 1. No additional run may be
generated to improve an observed diagnostic or inference result. A technically
invalid generation attempt is governed only by the replacement policy in
Section 9.

For the frozen four-agent topology, each fault run yields three locally-unseen
receiving-agent observations and one local-seen observation. Therefore the
primary Experiment 3 population contains:

> **24 fault physical runs × 3 locally-unseen receiving agents = 72 clustered
> agent-case observations per condition.**

The six Normal runs yield 24 Normal agent-case observations per condition. The
24 fault runs also yield 24 local-seen agent-case observations per condition.

## 4. Physical case IDs

The following 30 identifiers are fixed. Each identifies one planned primary
physical-run attempt and does not overlap the `PBH-*` identifiers used in
Experiment 1.

| Ordinal | physical_case_id | Status/fault | Run index |
|---:|---|---|---:|
| 1 | `EXP3-N-001` | Normal | 1 |
| 2 | `EXP3-N-002` | Normal | 2 |
| 3 | `EXP3-N-003` | Normal | 3 |
| 4 | `EXP3-N-004` | Normal | 4 |
| 5 | `EXP3-N-005` | Normal | 5 |
| 6 | `EXP3-N-006` | Normal | 6 |
| 7 | `EXP3-F1-001` | F1 | 1 |
| 8 | `EXP3-F1-002` | F1 | 2 |
| 9 | `EXP3-F1-003` | F1 | 3 |
| 10 | `EXP3-F1-004` | F1 | 4 |
| 11 | `EXP3-F1-005` | F1 | 5 |
| 12 | `EXP3-F1-006` | F1 | 6 |
| 13 | `EXP3-F8-001` | F8 | 1 |
| 14 | `EXP3-F8-002` | F8 | 2 |
| 15 | `EXP3-F8-003` | F8 | 3 |
| 16 | `EXP3-F8-004` | F8 | 4 |
| 17 | `EXP3-F8-005` | F8 | 5 |
| 18 | `EXP3-F8-006` | F8 | 6 |
| 19 | `EXP3-F10-001` | F10 | 1 |
| 20 | `EXP3-F10-002` | F10 | 2 |
| 21 | `EXP3-F10-003` | F10 | 3 |
| 22 | `EXP3-F10-004` | F10 | 4 |
| 23 | `EXP3-F10-005` | F10 | 5 |
| 24 | `EXP3-F10-006` | F10 | 6 |
| 25 | `EXP3-F13-001` | F13 | 1 |
| 26 | `EXP3-F13-002` | F13 | 2 |
| 27 | `EXP3-F13-003` | F13 | 3 |
| 28 | `EXP3-F13-004` | F13 | 4 |
| 29 | `EXP3-F13-005` | F13 | 5 |
| 30 | `EXP3-F13-006` | F13 | 6 |

If a primary attempt is technically invalid, it retains this identifier in the
append-only attempt log. A permitted replacement is a distinct physical run and
receives the suffix `-R01` or `-R02` after the primary identifier. The analysis
slot remains the original condition and run index; the manifest records the
actual accepted physical-run identifier. This prevents a failed attempt and its
replacement from sharing an identifier.

## 5. RNG policy and full seed table

### 5.1 Pre-specified allocation rule

- MATLAB RNG algorithm: `twister` (MATLAB's MT19937 implementation).
- Master allocation seed/base: `310000`.
- Canonical order: the ordinal order in Sections 4 and 5—Normal, F1, F8, F10,
  F13; within each status/fault, run indices 1 through 6.
- Primary run seed: `310000 + ordinal`, yielding the consecutive, unique seeds
  `310001` through `310030`.
- No data, diagnostic feature, verbalizer output, LLM output, or outcome is used
  in seed allocation.
- Immediately before each `sim` call, the generation procedure must execute
  `rng(run_seed, 'twister')` and must not make an unlogged random draw between
  that call and evaluation of the plant S-function seed expression.

The master allocation seed/base is a deterministic namespace, not a seed drawn
from a random generator. It is used only by the stated arithmetic allocation
rule; MATLAB receives the 30 explicit per-run seeds below.

### 5.2 Fixed primary-run seeds

| physical_case_id | Condition | Run index | RNG algorithm | Seed |
|---|---|---:|---|---:|
| `EXP3-N-001` | Normal | 1 | `twister` | 310001 |
| `EXP3-N-002` | Normal | 2 | `twister` | 310002 |
| `EXP3-N-003` | Normal | 3 | `twister` | 310003 |
| `EXP3-N-004` | Normal | 4 | `twister` | 310004 |
| `EXP3-N-005` | Normal | 5 | `twister` | 310005 |
| `EXP3-N-006` | Normal | 6 | `twister` | 310006 |
| `EXP3-F1-001` | F1 | 1 | `twister` | 310007 |
| `EXP3-F1-002` | F1 | 2 | `twister` | 310008 |
| `EXP3-F1-003` | F1 | 3 | `twister` | 310009 |
| `EXP3-F1-004` | F1 | 4 | `twister` | 310010 |
| `EXP3-F1-005` | F1 | 5 | `twister` | 310011 |
| `EXP3-F1-006` | F1 | 6 | `twister` | 310012 |
| `EXP3-F8-001` | F8 | 1 | `twister` | 310013 |
| `EXP3-F8-002` | F8 | 2 | `twister` | 310014 |
| `EXP3-F8-003` | F8 | 3 | `twister` | 310015 |
| `EXP3-F8-004` | F8 | 4 | `twister` | 310016 |
| `EXP3-F8-005` | F8 | 5 | `twister` | 310017 |
| `EXP3-F8-006` | F8 | 6 | `twister` | 310018 |
| `EXP3-F10-001` | F10 | 1 | `twister` | 310019 |
| `EXP3-F10-002` | F10 | 2 | `twister` | 310020 |
| `EXP3-F10-003` | F10 | 3 | `twister` | 310021 |
| `EXP3-F10-004` | F10 | 4 | `twister` | 310022 |
| `EXP3-F10-005` | F10 | 5 | `twister` | 310023 |
| `EXP3-F10-006` | F10 | 6 | `twister` | 310024 |
| `EXP3-F13-001` | F13 | 1 | `twister` | 310025 |
| `EXP3-F13-002` | F13 | 2 | `twister` | 310026 |
| `EXP3-F13-003` | F13 | 3 | `twister` | 310027 |
| `EXP3-F13-004` | F13 | 4 | `twister` | 310028 |
| `EXP3-F13-005` | F13 | 5 | `twister` | 310029 |
| `EXP3-F13-006` | F13 | 6 | `twister` | 310030 |

### 5.3 Simulator RNG path and unresolved runtime proof

The frozen simulator model stores the plant block as:

```text
FunctionName = temexd_mod
Parameters   = [] rand()
```

The C source documents parameter 2 as the scalar seed for the random generator.
At initialization, that scalar initializes the internal `g`, `measnoise`, and
`procdist` states. Those states drive measurement noise and random process
disturbances. The static source therefore establishes a MATLAB `rand()` →
S-function-seed path.

The model supplies two S-function parameters (`[]` and `rand()`) and omits the
optional third structure parameter, so `MSFlag` defaults to zero. Under that
flag, the C source uses the shared internal state `g` for both measurement-noise
and process-disturbance draws; the recurrence is
`state = mod(state × 9228907, 2^32)`. Thus Experiment 3 does not posit separate
user-selected measurement and process seeds: one MATLAB-controlled scalar is
passed to the unchanged S-function, which then advances its own deterministic
internal generator.

**BLOCKER BEFORE FREEZE — RNG plumbing:** the repository does not contain a
runtime record proving exactly when Simulink evaluates the stored `rand()`
expression relative to a per-run `rng(run_seed, 'twister')`, nor that no model
initialization action consumes a MATLAB random draw first. Before protocol
freeze, a non-diagnostic runtime plumbing probe must demonstrate that:

1. each of two clean executions with the same planned run seed passes the same
   scalar seed to `temexd_mod` and produces a byte-equivalent numeric output;
2. two distinct planned run seeds pass distinct scalar seeds;
3. the probe does not inspect XMEAS/XMV behavior or select seeds by outcome;
4. the exact evaluated S-function seed and pre-`sim` MATLAB RNG state are logged
   in the generation manifest or an immutable companion record.

No Experiment 3 physical run may be generated until this blocker is resolved.
If the probe shows that `rng(run_seed, 'twister')` does not control the stored
expression as specified, the generation mechanism must be revised and audited
in a new protocol version before any Experiment 3 run is created.

## 6. Simulator configuration

The following configuration is reconstructed from the frozen Experiment 1
held-out provenance and the isolated simulator copy. “Verified” means supported
by a frozen record or byte-checked source; it does not mean inferred from signal
behavior.

| Field | Pre-specified Experiment 3 value | Evidence/status |
|---|---|---|
| Upstream repository | `mv-per/tennessee-eastman-dataset` | Pinned source provenance |
| Source dataset snapshot | `309b944f35ac440ff0c70616947ffe723c766e14` | Pinned dataset commit; adds the external setpoint workflow |
| Simulator commit used | `a0413e16c940f0fc8b554d6a86248020d7fb7527` | Verified direct parent of `309b944f`; isolated pre-setpoint simulator used for Experiment 1 held-out |
| TEP operating mode | Mode 1 | `MultiLoop_mode1` and `Mode_1_Init.m` |
| Simulink model | `MultiLoop_mode1` | Verified |
| Simulink simulation mode | `normal` | Saved model parameter |
| MATLAB release | R2025b | Frozen held-out manifest/generation record |
| Simulink release | R2025b | Frozen narrative generation record; exact product version/build was not logged—see blocker below |
| Model start time | `0.0` h | Saved model parameter |
| Model stop time | `50` h | Saved model parameter |
| Solver | `ode45`, variable-step | Saved model parameter |
| Relative tolerance | `1e-6` | Saved model parameter |
| Absolute tolerance | `auto`; autoscaling `on` | Saved model parameters |
| Initial step / maximum step | `auto` / `auto` | Saved model parameters |
| Minimum step | `1e-6` | Saved model parameter |
| Zero-crossing algorithm | `Nonadaptive` | Saved model parameter |
| Saved `FixedStep` field | `Ts_base` | Saved but not the integration step under variable-step `ode45`; `Ts_base=0.0005` h is the controller sampling period |
| Output sampling interval | `Ts_save=1/60` h = 1 min | `Mode_1_Init.m` |
| Custom setpoints | None | Pre-setpoint parent simulator; same regime as Experiment 1 held-out |
| Initial-state callback | `PreLoadFcn=Mode_1_Init` | Saved model parameter |
| Initial-state loading | `load Mode1xInitial`; `LoadInitialState=on`; state name `xInitial` | Verified source/model parameters |
| Initial-state file hash | `40eaebc92badb04ad026e358cfd28ec9c778fcf2d24a1b8f5d85565854da2747` | SHA-256 of isolated `Mode1xInitial.mat` |
| Model file hash | `d2f6659f65935021d4b1813e7189be02e7ae9f5639b794e8edc4f2f3c5cddba8` | SHA-256 of isolated `MultiLoop_mode1.mdl` |
| S-function | `temexd_mod` | Saved plant block identity |
| S-function C-source hash | `0da41d939e5ab7ba122d7b70c124368ee0882fce40e775dba5d180e7a7e24e5e` | SHA-256; source byte-identical across parent/child commits |
| macOS MEX hash | `68f632388cb698dd7b8c595000bc03c2e1d19200546b9d4357df90e3fc93af0d` | SHA-256 of the binary used with the isolated simulator; MEX is not a Git blob |
| Workspace outputs | `tout`, `simout` (41 XMEAS), `xmv` (12 XMV) | Verified generation scripts/model |
| Saved numeric matrix | `[tout, simout, xmv]` | Verified generation scripts |
| Expected workbook | one `Sheet1`; 3001 numeric rows; 54 columns | Same structural regime as frozen held-out |
| Expected headers | `Time (h)`, `XMEAS-1`…`XMEAS-41`, `XMV-1`…`XMV-12` | Frozen held-out schema |
| Expected time axis | 0–50 h inclusive; strictly increasing; constant `1/60` h interval | Frozen held-out schema |

The model contains a `FixedStep=Ts_base` configuration field, but the active
solver is variable-step `ode45`; this field must not be misreported as the
numerical integration step. The one-minute interval is the saved-output sampling
interval, not the solver step.

**BLOCKER BEFORE FREEZE — runtime version identity:** before freeze, the
generation host must record `version`, `version('-release')`, and the full
`ver('simulink')` result. The release must be R2025b and the exact Simulink
product version/build must be added to this protocol or its machine-readable
companion. The previous held-out record establishes R2025b but does not preserve
the exact Simulink product build.

**BLOCKER BEFORE FREEZE — generation implementation:** a dedicated Experiment 3
generation script has not yet been created or frozen. It must implement the
case/seed tables, no-overwrite behavior, attempt logging, exact path/hash checks,
and Section 9 replacement policy. Its hash must be added before protocol freeze.
This document does not authorize reusing an ad hoc command sequence.

## 7. Fault and injection configuration

The disturbance vector has length 28. For a fault run it is initialized to zero
and exactly one element is set to one:

| Fault | Configuration |
|---|---|
| F1 | `dist=zeros(1,28); dist(1)=1` |
| F8 | `dist=zeros(1,28); dist(8)=1` |
| F10 | `dist=zeros(1,28); dist(10)=1` |
| F13 | `dist=zeros(1,28); dist(13)=1` |
| Normal | `dist=zeros(1,28)` |

The fault list is inherited from Experiment 1; it is not selected using the
relative difficulty or prior result of any class.

The verified source routing is:

```text
dist constant ──> VariableTransportDelay data input ──> plant input 13
                         ^
                         │
                  Constant(10) delay input
```

`MaximumDelay=20` is capacity, not the applied delay. The second input is the
constant 10. The pre-delay output is zero: `InitialOutput` is not explicitly
serialized in the compatible R2024b model and the documented compatible
Simulink default is zero. Simulation time and saved time are in hours.
Therefore the same Experiment 1 injection time is fixed at **10 h**, with a
simulation interval of **0–50 h** and post-injection interval **10–50 h**.

Experiment 3 must not modify the delay, disturbance routing, fault flags,
simulation duration, or operating mode.

## 8. Prospective data boundary

The following sequence is mandatory:

1. resolve every blocker in Section 18 without creating or diagnostically
   inspecting an Experiment 3 physical run;
2. audit and freeze this protocol, its machine-readable companion if created,
   the generation script, runtime identity, and integrity verifier;
3. generate the 30 planned physical runs in the pre-specified order and under
   the pre-specified seed policy;
4. perform only the pre-specified mechanical integrity checks;
5. populate and freeze the held-out manifest, raw workbook hashes, attempt log,
   and generation provenance;
6. only after that held-out freeze may the unchanged verbalizer open the raw
   workbooks and produce structured evidence and neutral text;
7. only after the verbalizations are frozen may the unchanged A/B/E inference
   and offline evaluation proceed under their frozen execution order.

Before Step 6, no person or program may calculate or view XMEAS/XMV summaries,
features, plots, diagnostic signatures, verbalizations, class separability, or
LLM predictions. Mechanical checks may read cells only to verify schema,
finiteness, dimensions, and the time axis; they must not report or retain
diagnostic signal summaries.

After generation:

- no run may be excluded because its fault manifestation appears weak;
- no run may be excluded because its frozen verbalization is ambiguous;
- no run may be excluded because A, B, or E classifies it incorrectly;
- no run may be regenerated to obtain a more favorable realization;
- no additional run may be added after scientific outcomes are visible.

The prospective freeze prevents adaptive generation, outcome-dependent
selection, and cherry-picking. It does not by itself prove statistical
independence.

## 9. Technical validity, exclusion, and replacement policy

### 9.1 Permitted technical-invalidity criteria

A generation attempt is technically invalid only if at least one of these
pre-specified checks fails:

1. MATLAB/Simulink reports execution failure or the simulation does not finish;
2. the workbook is missing, cannot be opened as a valid XLSX ZIP container, or
   does not contain exactly one worksheet named `Sheet1`;
3. the workbook does not contain exactly 3001 numeric data rows and 54 columns;
4. headers differ from `Time (h)`, 41 ordered XMEAS names, and 12 ordered XMV
   names;
5. a numeric cell is missing or contains NaN/Inf;
6. the time axis does not start at 0 h, end at 50 h, increase strictly, and use
   a constant `1/60` h interval;
7. the logged simulator/model/S-function/initial-state hashes, runtime release,
   assigned seed, or case configuration differ from the frozen protocol;
8. an output file would overwrite an existing attempt or provenance record.

No test may assess magnitude, trajectory, detectability, class signature, or
diagnostic quality. A complete 0–50 h time axis establishes structural
completion only; it does not assert a plant-state interpretation.

### 9.2 Fixed replacement rule

Replacement is **yes**, but only for a failure in Section 9.1.

- The failed attempt is never deleted or silently overwritten. Its identifier,
  seed, failure code, logs, and any materialized file hash are retained in an
  append-only attempt record.
- Replacement attempt `j` receives identifier `<primary_id>-R0j`, where
  `j ∈ {1,2}`.
- Its seed is `primary_seed + 1,000,000 × j`. This deterministic rule is fixed
  now and does not use the failed signal or any scientific outcome.
- The replacement uses the same condition, run index, and all other frozen
  simulator settings.
- At most two replacements are allowed per planned slot (three attempts total,
  including the primary attempt).
- If the second replacement also fails, generation stops with an incomplete
  Experiment 3. The sample size is not reduced, the case is not analyzed, and
  no alternative seed or extra recovery run may be chosen without a new audited
  protocol version created before further generation.

Only the first structurally valid attempt for a planned slot enters the 30-run
held-out. Technical-invalidity status is determined before verbalization and
without diagnostic inspection.

## 10. Frozen preprocessing, verbalizer, and FoT dependencies

Experiment 3 must use these Experiment 1 artifacts without modification. Hashes
are copied from `phase_b/config/phase_b_protocol_frozen.json` and
`phase_b/PHASE_B_PROTOCOL_HASHES.json`.

| Role | Frozen artifact | SHA-256 |
|---|---|---|
| Verbalizer config, including development Normal baseline and thresholds | `code/verbalizer_config_v2.json` | `552a0b8a9cf9e416de77daa7aca2d8dee152a2700bbfaab4ae5e039081712519` |
| Preprocessing/features | `code/tep_features.py` | `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c` |
| Phase A verbalizer V2 | `code/tep_verbalize_v2.py` | `3a9129b6353cac6f8c9e02281282f137dd07885b1f882ca633ee9d6bf52393be` |
| Phase A structured evaluator | `code/evaluate_verbalizer_v2.py` | `972e06fa29bee5a58d57ca757bd158c5cddaa2f4ed12eb5c739169c7fef79a92` |
| Local examples | `phase_b/local_knowledge/local_examples.json` | `468d51b7987b8655fc80638d99366dbe3632af0606c9034ca6db7fd1fdcd0a5c` |
| Final insight library | `phase_b/insights/final_local_insights.json` | `b7ea847ccaf72b04c407ae4878924719c5363d4ccc6851d3d5fef79386e4bcfd` |
| Evaluator-side pseudolabel mapping | `phase_b/config/evaluator_side/pseudolabel_mapping.json` | `f68a690df9c5d0d9505c8b388379c78ccdaa4143e9b4c4e4814ea6d7888b3035` |
| Condition E derangement | `phase_b/config/evaluator_side/condition_e_derangements.json` | `e8a0bdbf5a0b7c04d1ba978fd7e18f55b933d8062125ea11c1fb117f9990b231` |
| Condition A prompt | `phase_b/prompts/isolated_A.txt` | `cecc664e5d9b9558ca7f8675bee37ae59a5d97a5ff0518175a8a8855a5328289` |
| Condition B prompt | `phase_b/prompts/fot_B.txt` | `cecc664e5d9b9558ca7f8675bee37ae59a5d97a5ff0518175a8a8855a5328289` |
| Condition E prompt | `phase_b/prompts/corrupted_E.txt` | `cecc664e5d9b9558ca7f8675bee37ae59a5d97a5ff0518175a8a8855a5328289` |
| A/B/E construction | `phase_b/conditions/builders.py` | `5a4906304e5ab09ad12cd004e8838dd337ac2f5544ac03d0c392f21ae2009bd9` |
| Execution configuration | `phase_b/config/execution_config.json` | `2a88d915af9c76a6d8ecd4331efe42d756a5a305d8a07479990996685419d234` |
| R=3 aggregation | `phase_b/evaluation/aggregation.py` | `ce44166fcb9f871d2b46073e8049a3d6ca6fca0aadfbcf49067d5af95f3bc212` |
| Metric implementation | `phase_b/evaluation/metrics.py` | `9aa8e6d12957c10e3059c95dcb93efa59679e97a7374500aea9e86ad26e9f0cb` |
| Cluster-bootstrap implementation | `phase_b/evaluation/bootstrap.py` | `524751fede48e678ee66b9f783be8fdeaefe7bebe32772e5367ba9be9c3d9df5` |
| Evaluation record logic | `phase_b/evaluation/records.py` | `2dd9e98fe3b11f72cdb1f0a02b2dfec52292869b5e59a060edac7283594f67d4` |
| Final offline evaluator | `phase_b/final_evaluation/evaluate_frozen_predictions.py` | `fbbc159a0e61e92723f46d4a97e59244a129741bffbf84acd433416bc74d567e` |

The final offline evaluator hash above is verified unchanged relative to the
`phase-b-results-frozen` tag. The frozen execution identity is OpenAI
`gpt-5.6-terra`, reasoning effort
`medium`, temperature `null`, seed `null`, strict Structured Outputs, and R=3
calls with the same input hash and frozen configuration. The same local schema
and stricter local semantic validator remain mandatory. Conditions retain their
frozen meanings:

- **A:** isolated agent;
- **B:** six genuine peer-only insights;
- **E:** the same six peer insights and order as B, with only the pseudolabel
  association changed by the frozen zero-fixed-point derangement.

No Experiment 3 series may change the baseline, thresholds, features, renderer,
local examples, insight text, mappings, prompts, condition payloads, repetition
count, retry policy, aggregation, or evaluator.

## 11. Statistical unit and dependence structure

The independent sampling unit for inference is the **physical run**. The three
locally-unseen receiving-agent observations derived from the same fault run
share one physical realization and are not treated as independent.

The 24 fault simulations are separate executions with distinct pre-specified
run seeds. Conditional on the fixed simulator and generation mechanism, they
are intended as distinct stochastic physical realizations. This is the basis
for treating physical runs as sampling units. It is a property to be supported
by the verified RNG mechanism and separate execution logs, not a consequence of
the Git or data freeze itself.

The prospective freeze and held-out boundary prevent adaptive selection and
outcome-driven regeneration. They do not mathematically guarantee independence
and must not be described as doing so.

## 12. Endpoint definitions

### 12.1 Primary population

The primary population is all fault agent-cases in which the true fault class
is locally unseen by the receiving agent. For Experiment 3 this is 72 aggregate
agent-case outcomes per condition, clustered within 24 physical runs.

An abstention is incorrect, exactly as in Experiment 1.

### 12.2 Pre-specified quantities

For condition `C ∈ {A,B,E}`:

```text
accuracy_C_unseen = correct aggregate predictions under C
                    / 72 locally-unseen aggregate agent-cases
```

The contrasts are:

```text
B−A = accuracy_B_unseen − accuracy_A_unseen
B−E = accuracy_B_unseen − accuracy_E_unseen
```

- **B−A is the primary replication contrast.** It addresses whether authentic
  FoT peer insight improves recognition of locally-unseen instances relative to
  isolation on the fresh extension.
- **B−E is the supporting semantic-specificity contrast.** It assesses whether
  B exceeds the matched-text corrupted-association control. It is not a second
  primary endpoint.

`accuracy_A_unseen`, `accuracy_B_unseen`, and `accuracy_E_unseen` are reported
with numerators and denominators. Per-agent, helped/harmed, abstention, and
repetition-stability summaries may be produced only through the unchanged
evaluator and are supporting/descriptive, not replacements for B−A.

### 12.3 Secondary preservation evidence

Normal and local-seen outcomes are kept separate from the primary population:

- Normal: 6 physical runs × 4 agents = 24 aggregate agent-cases per condition;
- local-seen: 24 fault physical runs × 1 owning agent = 24 aggregate
  agent-cases per condition.

Their condition-wise accuracies, abstentions, and paired changes are secondary
preservation evidence. They are not pooled into locally-unseen accuracy.

## 13. Bootstrap and statistical plan

### 13.1 Experiment 3 primary analysis

The Experiment 3 analysis reuses the Experiment 1 statistical principle and
implementation:

- paired cluster bootstrap over `physical_case_id`;
- stratification by the four true evaluator-side pseudoclasses/faults;
- all three unseen receiving-agent rows of a sampled physical run remain in the
  same cluster and are carried together;
- A, B, and E outcomes remain paired within every sampled run/receiver record;
- six physical runs are sampled with replacement inside each of the four
  strata, producing 24 run clusters per bootstrap draw;
- 10,000 bootstrap draws;
- percentile 95% confidence intervals, as implemented by the frozen bootstrap
  code;
- new bootstrap seed: **310031**.

The bootstrap seed is fixed before generation, is distinct from the Experiment
1 seed `20260829`, and is outside the 30 run-seed range. It is a computational
reproducibility constant and has no role in physical-run generation.

The same paired draws are used to estimate confidence intervals for B−A and
B−E. No agent-case row is bootstrapped independently of its physical run.

### 13.2 Deterministic reporting

The evaluator must report exact counts and denominators before decimal
accuracies. No threshold, class-specific analysis, or inferential test may be
introduced after observing results. Class/fault breakdowns, if emitted by the
unchanged evaluator, are explicitly descriptive and post-hoc unless separately
listed as pre-specified here; they are not success criteria.

## 14. Success and failure criteria

### 14.1 Primary replication conclusion

**Replication supported** only if both conditions hold in the separate
Experiment 3 analysis:

1. observed `B−A > 0`; and
2. the paired cluster-bootstrap 95% confidence interval for B−A excludes zero
   on the positive side (lower endpoint `> 0`).

If either condition fails, the result is reported as **failure to replicate / an
evidence limitation**. The criterion will not be weakened after outcomes are
known, and no recovery runs will be generated.

### 14.2 Semantic-specificity conclusion

**Semantic-specificity support** requires observed `B−E > 0` on Experiment 3.
The pre-specified paired cluster-bootstrap interval for B−E is also reported,
but interval exclusion of zero is not an additional gate for this supporting
criterion.

The B−E conclusion remains supporting and cannot be promoted to the primary
endpoint. Normal and local-seen preservation remain secondary and do not alter
the primary replication conclusion.

## 15. Experiment 3-only versus pooled analysis

### 15.1 Primary analysis

The primary analysis uses **only the 24 new Experiment 3 fault physical runs**.
Experiment 1 observations are not added to its numerator, denominator, or
bootstrap. The success/failure decision in Section 14 is based exclusively on
this separate analysis.

### 15.2 Secondary descriptive pooled result

A pooled `Experiment 1 + Experiment 3` summary is allowed only as a
pre-declared secondary descriptive analysis. It may report exact counts,
denominators, accuracies, B−A, and B−E across:

- 12 Experiment 1 + 24 Experiment 3 fault physical runs = 36 run clusters;
- 36 Experiment 1 + 72 Experiment 3 locally-unseen agent-cases = 108
  locally-unseen agent-case observations per condition.

The pooled summary will not replace, rescue, or redefine the Experiment 3-only
replication result. No pooled confidence interval or pooled success criterion is
pre-specified here; adding one after seeing outcomes is prohibited.

## 16. Manifest template

The final manifest is populated only after actual generation and mechanical
integrity verification. File-dependent fields remain `TBD` now; no final
filename, size, or hash is invented in this protocol.

| physical_case_id | fault/status | seed | filename | size_bytes | SHA256 | rows | cols | time_start | time_end | sampling | finite_check | structural_valid |
|---|---|---:|---|---:|---|---:|---:|---:|---:|---:|---|---|
| `EXP3-N-001` | Normal | 310001 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-N-002` | Normal | 310002 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-N-003` | Normal | 310003 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-N-004` | Normal | 310004 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-N-005` | Normal | 310005 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-N-006` | Normal | 310006 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F1-001` | F1 | 310007 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F1-002` | F1 | 310008 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F1-003` | F1 | 310009 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F1-004` | F1 | 310010 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F1-005` | F1 | 310011 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F1-006` | F1 | 310012 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F8-001` | F8 | 310013 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F8-002` | F8 | 310014 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F8-003` | F8 | 310015 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F8-004` | F8 | 310016 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F8-005` | F8 | 310017 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F8-006` | F8 | 310018 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F10-001` | F10 | 310019 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F10-002` | F10 | 310020 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F10-003` | F10 | 310021 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F10-004` | F10 | 310022 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F10-005` | F10 | 310023 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F10-006` | F10 | 310024 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F13-001` | F13 | 310025 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F13-002` | F13 | 310026 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F13-003` | F13 | 310027 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F13-004` | F13 | 310028 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F13-005` | F13 | 310029 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| `EXP3-F13-006` | F13 | 310030 | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

The implementation may add attempt/provenance fields such as
`planned_case_id`, `generation_attempt`, `replacement_of`,
`technical_failure_code`, `matlab_rng_state_before_sim`, and
`evaluated_sfunction_seed`; it may not remove the fields above. Replacement
rows use the replacement physical-run ID and deterministic seed from Section 9.

## 17. Freeze checklist

The protocol may move from draft to frozen only when every item is checked and
no Experiment 3 diagnostic signal has been inspected:

- [ ] Scientific audit approves the RQ, same-four-class scope, fixed sample,
      endpoints, and success/failure criteria.
- [ ] All 30 primary IDs and seeds exactly match Sections 4 and 5.
- [ ] RNG plumbing blocker is resolved by a non-diagnostic reproducibility
      probe and its immutable record is linked.
- [ ] MATLAB and Simulink runtime release/build identities are recorded and
      satisfy Section 6.
- [ ] Dedicated generation script is implemented, reviewed, hash-pinned, and
      proven to refuse overwrite.
- [ ] Generation script verifies model, initial-state, S-function source, and
      MEX hashes before every generation session.
- [ ] Integrity verifier implements only the Section 9 technical checks and is
      hash-pinned.
- [ ] Attempt log and manifest schemas represent replacements without deleting
      failed attempts.
- [ ] Experiment 1 frozen artifacts are re-hashed against
      `phase_b/PHASE_B_PROTOCOL_HASHES.json`.
- [ ] The frozen Experiment 1 schedule-construction and execution-order rules
      are reused without condition-order or prompt changes; an Experiment 3
      schedule containing only the new IDs is generated and frozen before its
      first inference.
- [ ] New bootstrap seed is exactly `310031`; draws remain 10,000.
- [ ] Raw output directory is ignored by Git and empty of Experiment 3 cases
      before generation.
- [ ] Prospective diagnostic-access guard is enabled before the first run.
- [ ] Protocol, machine-readable config if any, generation code, verifier, and
      empty manifest template receive a freeze commit/tag before generation.
- [ ] No simulation, feature extraction, neutral-text generation, LLM call, or
      scientific outcome evaluation occurred before that freeze.

After generation, a separate held-out freeze is required before verbalization.
It must bind the accepted workbooks, failed-attempt provenance, exact file
sizes/hashes, structural verification output, runtime identity, and actual RNG
records. That future held-out freeze is distinct from the protocol freeze.

## 18. Explicit unresolved blockers

The following blockers are known at draft creation:

1. **BLOCKER BEFORE FREEZE — RNG evaluation timing and control.** Static source
   establishes `rand()` as the S-function seed source, but a non-diagnostic
   runtime probe must verify that the per-run MATLAB `twister` seed controls the
   exact scalar passed to `temexd_mod` and reproduces output under the planned
   load/simulation sequence.
2. **BLOCKER BEFORE FREEZE — exact runtime identity.** R2025b is documented, but
   the exact MATLAB and Simulink version/build values for the generation host
   must be captured before freeze.
3. **BLOCKER BEFORE FREEZE — generation and verification implementation.** The
   dedicated Experiment 3 generation script, attempt log schema, and integrity
   verifier configuration do not yet exist as hash-pinned artifacts. They must
   implement this protocol without changing its scientific decisions.

These blockers prevent protocol freeze and data generation. They do not leave
the sample size, case identities, primary seeds, endpoint, or success criteria
open for later choice.

---

## Provenance consulted for this draft

- `FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md`
- `README.md`
- `AUDIT_GUIDE.md`
- `phase_b/PHASE_B_PROTOCOL_FREEZE.md`
- `phase_b/config/phase_b_protocol_frozen.json`
- `phase_b/PHASE_B_PROTOCOL_HASHES.json`
- `phase_b/config/execution_config.json`
- `phase_b/heldout/HELDOUT_GENERATION_SUMMARY.md`
- `phase_b/heldout/PHASE_B_HELDOUT_FREEZE.md`
- `phase_b/heldout/SIMULATOR_PARENT_AUDIT.md`
- `phase_b/heldout/phase_b_heldout_manifest.csv`
- `phase_b/heldout/verify_heldout_integrity.py`
- `phase_b/heldout/generation/generate_heldout_mode1.m`
- `phase_b/heldout/generation/generate_phaseB_extra_runs.m`
- `supporting_records/phase_a/INJECTION_TIME_VERIFICATION.md`
- `supporting_records/phase_a/VERBALIZER_V2_FREEZE.md`
- isolated, byte-verified simulator sources under the ignored
  `tep_parent_a0413e16/simulator/` directory.

No Experiment 3 simulation, raw-data generation, verbalization, LLM inference,
or scientific evaluation was performed while preparing this draft.
