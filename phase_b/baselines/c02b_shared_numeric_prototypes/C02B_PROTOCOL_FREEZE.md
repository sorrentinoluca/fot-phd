# C02b numerical shared-prototype protocol freeze

**Status:** frozen before executing or inspecting this baseline's predictions.

This protocol evaluates the **baseline numerica con prototipi condivisi,
ispirata a FedProto**. It is not called FedProto because it does not train a
representation network or implement the optimization procedure of the original
algorithm.

## Same-task boundary

- Four agents; each knows Normal and exactly one opaque fault pseudoclass.
- Training uses only fault batches 1–5 and Normal blocks N1–N5.
- Testing uses the 15 physical PBH cases already used by FoT Experiment 1.
- The classifier sees only opaque pseudolabels. Real labels are joined only by
  the offline evaluator after every prediction has been written.
- No validation, original batch 8–10, PBH truth, or LLM repetition can enter
  fitting or prediction.

## Frozen method

Each development case is represented by the frozen 697-component V2 numerical
signature (`41 XMEAS × 17` temporal components). This vector is derived from
the structured evidence immediately upstream of the neutral text, is bounded
in `[0,1]`, and requires no test-fitted normalization.

For every known class, an agent computes the component-wise mean of its five
development vectors. A receiving agent classifies a held-out vector by minimum
mean absolute distance. The main arm adds the three peer fault prototypes to
the agent's own Normal and fault prototypes. The local-only control retains
only those two local prototypes. The centralized descriptive reference builds
the same five prototypes in one process from all development data.

Exact ties within `1e-12` produce an abstention, counted as incorrect. Missing,
non-finite, dimensionally invalid, or hash-mismatched inputs stop the full run;
there is no imputation or selective case removal. The computation is
deterministic; seed `20260910` is fixed for the physical-case cluster bootstrap.

## Primary analysis and payload

The primary metric is local-unseen fault accuracy for the shared-prototype arm:
36 agent-case observations grouped into 12 physical-case clusters. Secondary
outputs are overall, local-seen, Normal, per-agent, per-fault, and confusion
results. If uncertainty is reported, the 12 physical fault cases—not model
repetitions—are resampled, stratified by opaque fault class.

Each receiving agent gets three peer fault prototypes. The frozen wire format
is nine ASCII pseudolabel bytes followed by 697 little-endian float64 values,
in sorted label order. Normal is already local at every agent and is not sent.
The resulting byte counts will be taken from the actual emitted payload files,
not estimated from text length.

PCA+SVM and FedAvg are not executed here. A conventional centralized PCA+SVM
would train on all classes and therefore change local-unseen into ordinary
supervised classification. FedAvg would additionally require a newly designed
shared model and aligned output space; averaging local models does not by
itself give an agent an unseen opaque output class. Such numbers would not
answer C02b's same-task question.

The complete machine-readable choices and frozen input hashes are in
`protocol_config.json`. The configuration hash is recorded in
`protocol_freeze_manifest.json` before baseline execution.
