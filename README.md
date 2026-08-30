# Federation over Text for Distributed Time-Series Diagnosis

This repository documents a PhD research project on **Federation over Text
(FoT)** for distributed time-series diagnosis. The final application target is
photovoltaic (PV) systems. The Tennessee Eastman Process (TEP) is the controlled
preliminary methodological proving ground used to develop and test the
representation and knowledge-federation architecture.

The TEP work is complete: Phase A established a neutral time-series
representation layer, and Phase B evaluated FoT under a frozen held-out
protocol. The results support feasibility in this controlled setting; they are
not evidence of performance in PV systems or of general cross-domain validity.

## Project at a glance

`PV research goal → controlled TEP proving ground → Phase A representation → Phase B FoT → feasibility supported → next: empirical PV phase`

**TEP is a methodological feasibility gate, not the final application domain.**

The research question is whether distributed agents with different local
experience can exchange compact textual knowledge that helps reasoning about
locally unseen time-series conditions, without federating their raw data.

## What is Federation over Text?

In this project:

- agents hold non-IID local knowledge;
- raw time-series data remain local;
- local evidence is distilled into provenance-aware textual insights;
- those insights are shared with eligible peers;
- an LLM reasons from a neutral case representation and the knowledge available
  under the assigned experimental condition.

FoT here is a controlled proof of concept. The experiment evaluates a specific
TEP setup and does not claim that FoT has already been validated in general.

## Phase A — Neutral representation

Phase A freezes the layer:

`multivariate time series → structured numerical evidence → neutral text`

The structured representation retains quantitative and temporal evidence such
as signed level shift, signed slope, residual variability, and
sample-to-sample variability. The renderer serializes observed evidence without
automatically assigning fault semantics such as drift or oscillation.

Phase A therefore **describes rather than diagnoses**. Its offline evaluator
measures descriptive stability and separability across splits; those measures
are not classifier accuracy. Configuration, implementation, split discipline,
and frozen hashes are documented in
[`VERBALIZER_V2_FREEZE.md`](VERBALIZER_V2_FREEZE.md) and the code guide
[`docs/README_CODE_V2.md`](docs/README_CODE_V2.md).

## Phase B — Federation over Text

Phase B uses four agents. Each agent knows Normal and one local fault
pseudoclass; the other three fault pseudoclasses are locally unseen. Fault
identities are replaced in agent-facing material by opaque pseudolabels.

Each agent builds local textual insights from permitted development evidence.
Federation is peer-only: agents receive eligible peer-derived insights, not
their own insights, and no raw process data, gradients, or model weights are
federated. Diagnosis uses the frozen Phase A neutral representation.

The final experiment uses three LLM repetitions (`R=3`) per agent-case and
condition. Its held-out cases were independently generated and frozen before
verbalization, inference, and ground-truth evaluation.

### Experimental conditions

- **A — isolated:** local knowledge only; no peer insight block.
- **B — FoT:** genuine peer-derived textual insights are available.
- **E — corrupted specificity control:** the B insight structure is matched,
  but pseudolabel associations are incorrect.

**B−A is the preregistered primary contrast.**

**B−E is the preregistered specificity/mechanistic contrast; it is not the
primary endpoint.**

## Key held-out result

The primary subset contains cases from fault pseudoclasses locally unseen by
each receiving agent.

| Condition | Unseen accuracy |
|---|---:|
| A — isolated | 0/36 (0.00%) |
| B — FoT | 31/36 (86.11%) |
| E — corrupted control | 3/36 (8.33%) |

- Primary contrast: **B−A = +0.8611**.
- Specificity/mechanistic contrast: **B−E = +0.7778**.

These numbers require the following qualifications:

- The 36 rows are agent-case observations, **not 36 independent physical
  cases**.
- They arise from **12 independent physical fault-runs**, each assessed by the
  three agents for which that fault pseudoclass was unseen.
- Condition A operates at an information floor for unseen class semantics.
- The result does not mean “+86 percentage points in general.”
- The secondary 91.67% overall accuracy is not the main scientific answer.
- The observed `harmed = 0` does not establish a general no-negative-transfer
  guarantee.

For the complete frozen analysis, see
[`phase_b/final_evaluation/EVALUATION_REPORT.md`](phase_b/final_evaluation/EVALUATION_REPORT.md).

## What the TEP PoC supports

Within this controlled experiment, the evidence supports:

- feasibility of time-series to neutral-text representation;
- feasibility of generating local textual insights with explicit provenance;
- benefit of genuine peer textual knowledge relative to isolation;
- a positive specificity/mechanistic contrast between genuine and corrupted
  knowledge;
- a leakage-resistant workflow with held-out, protocol, schedule, inference,
  and result freezes.

These are bounded findings from the TEP proof of concept.

## What this work does not establish

- No empirical cross-domain generalization has yet been tested.
- No PV diagnostic performance has yet been measured.
- There is no general no-negative-transfer guarantee.
- The current TEP verbalizer is not claimed to be domain-agnostic.
- FoT has not yet been compared with a central in-context-learning knowledge
  baseline of comparable information content.
- No superiority over classical federated learning is claimed.

## Start here

### Quick orientation — LLM or RAG

Read [`docs/FOT_PROJECT_LLM_REFERENCE.md`](docs/FOT_PROJECT_LLM_REFERENCE.md)
first. It is the compact canonical retrieval and reference layer, with the
claim hierarchy, canonical numbers, caveats, and provenance pointers.

### Full technical and didactic narrative

Read
[`docs/FOT_PROJECT_TECHNICAL_NARRATIVE.md`](docs/FOT_PROJECT_TECHNICAL_NARRATIVE.md)
for the complete historical, methodological, and didactic account.

### Final PoC synthesis

Read [`FOT_TEP_POC_FINAL_SYNTHESIS.md`](FOT_TEP_POC_FINAL_SYNTHESIS.md) for a
compact final scientific synthesis of the TEP proof of concept.

## Source-of-truth hierarchy

1. **Frozen experimental artifacts and results** — exact protocol, records,
   hashes, predictions, and metrics.
2. **Canonical technical narrative** — authoritative human-readable
   explanation.
3. **LLM reference** — compact retrieval and orientation layer.
4. **Historical or superseded documents** — methodological history only when
   later freezes supersede them.

> If documentation conflicts with a frozen experimental artifact, the frozen
> artifact takes precedence for the exact experimental record.

The LLM reference is deliberately the first file to read for rapid orientation,
but it does not outrank frozen artifacts in scientific authority.

## Repository map

```text
.
├── README.md
├── FOT_TEP_POC_FINAL_SYNTHESIS.md
├── VERBALIZER_V2_FREEZE.md
├── PHASE_A_STATUS.md
├── code/
│   ├── tep_features.py
│   ├── tep_verbalize_v2.py
│   ├── verbalizer_config_v2.json
│   └── evaluate_verbalizer_v2.py
├── docs/
│   ├── FOT_PROJECT_LLM_REFERENCE.md
│   ├── FOT_PROJECT_TECHNICAL_NARRATIVE.md
│   ├── README_CODE_V2.md
│   └── figures/
├── tep_validation_v2/
├── tep_test_v2/
├── phase_b/
│   ├── heldout/
│   ├── insights/
│   ├── conditions/
│   ├── execution/
│   ├── final_evaluation/
│   └── tests/
└── reproducibility/
```

- `code/`, `tep_validation_v2/`, and `tep_test_v2/` preserve the Phase A
  implementation and split-specific evidence.
- `phase_b/` contains the FoT protocol, guarded held-out provenance, insight
  libraries, execution records, and offline evaluation.
- `docs/` contains the canonical navigation and teaching documents plus their
  conceptual figures.
- `reproducibility/` contains Phase A verification artifacts.

## Reproducibility and freeze milestones

Tags preserve immutable scientific milestones. Branch names organize
development; they are not the scientific source of truth.

| Milestone | Tag | Commit |
|---|---|---|
| Phase A reproducibility closure | `phase-a-reproducibility-complete` | `145b6b79c59c352e06028166185bad3c9fb49607` |
| Independent held-out freeze | `phase-b-heldout-frozen` | `86baaa65e72cea22ecb89dd0e7b213aea5a1284b` |
| Phase B protocol freeze | `phase-b-protocol-frozen` | `3d86f64d43e14e7e0de520cb047ca1043bf9c1c0` |
| Execution schedule freeze | `phase-b-execution-schedule-frozen` | `eef0bc58e5ab14fb0cd2aece180fb5b1b5a7962b` |
| Prediction freeze | `phase-b-inference-frozen` | `11c34358e28e875cd5c7249061ac2b89ffcd42f4` |
| Evaluation results freeze | `phase-b-results-frozen` | `45ec4eed65b263a5803ced7d01064c4672e81e86` |

The source TEP dataset is pinned separately to upstream commit
`309b944f35ac440ff0c70616947ffe723c766e14`.

## Reproducing the TEP work

The reference Phase A environment used CPython `3.13.9`; exact dependencies are
in [`requirements.txt`](requirements.txt). A compact setup is:

```bash
git clone https://github.com/sorrentinoluca/fot-phd.git
cd fot-phd
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Clone the upstream TEP dataset outside this repository and check out the pinned
commit:

```bash
git clone https://github.com/mv-per/tennessee-eastman-dataset.git
git -C tennessee-eastman-dataset checkout 309b944f35ac440ff0c70616947ffe723c766e14
```

The raw workbooks, local caches, and generated temporary outputs are excluded
from version control. Phase A commands, split boundaries, calibration checks,
and regression tests are documented in
[`docs/README_CODE_V2.md`](docs/README_CODE_V2.md). The frozen Phase B record is
anchored by
[`phase_b/PHASE_B_PROTOCOL_FREEZE.md`](phase_b/PHASE_B_PROTOCOL_FREEZE.md), its
schedule amendment in
[`phase_b/PHASE_B_PROTOCOL_AMENDMENT_001.md`](phase_b/PHASE_B_PROTOCOL_AMENDMENT_001.md),
and the final evaluation report linked above.

## Historical documents

Some repository files intentionally preserve earlier proposals, exploratory
designs, and superseded states. They remain available for provenance and
methodological history. When such a file conflicts with a frozen artifact or
the final technical narrative, use the frozen/final state. This distinction is
important for both human readers and automated retrieval.

## Current status

| Component | Status |
|---|---|
| Phase A — TEP neutral representation | **COMPLETED** |
| Phase B — TEP Federation over Text | **COMPLETED / FROZEN** |
| Technical narrative | **CANONICAL** |
| LLM reference | **CANONICAL** |
| Next empirical research phase | **PHOTOVOLTAIC DOMAIN** |

No PV experimental protocol is currently frozen.

## Next research phase — Photovoltaics

The next phase will test whether the methodological architecture remains useful
in real PV settings. Candidate reusable elements include:

- separation between representation and reasoning;
- local insight generation with provenance;
- peer textual federation;
- freeze and held-out discipline;
- clustered evaluation aligned with physical experimental units.

The following must be redesigned or independently revalidated for PV:

- features, baselines, thresholds, and time windows;
- seasonality, irradiance, temperature, and operating regimes;
- site and inverter heterogeneity;
- missing data and sensor or system drift;
- event taxonomy and trustworthy ground truth.

Whether FoT offers an advantage over a comparable central
in-context-learning knowledge baseline remains an open research question.
