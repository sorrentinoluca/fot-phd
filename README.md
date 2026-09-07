# Federation over Text for Distributed Time-Series Diagnosis

**Federation over Text (FoT)** is the research project. Its final application
target is **photovoltaic (PV) systems**. The Tennessee Eastman
Process (TEP) is not the target domain: it is a **controlled methodological
proof of concept and feasibility gate** for multivariate time-series knowledge
transfer.

```text
FoT research hypothesis
→ controlled multivariate time-series PoC on TEP
→ validation of textual federated knowledge transfer
→ next empirical phase: photovoltaic systems
```

The TEP proof of concept is complete and frozen. It supports feasibility in the
controlled setting studied here; it does not establish performance or
cross-domain generalization in PV systems. A subsequently executed
**centralized full-information pooled ICL post-hoc exploratory reference**
(Condition C) is also complete, frozen, and independently reviewed.

## Reading path

1. **Understand the project and experiment** →
   [`docs/fot_walkthrough_conversazione.html`](docs/fot_walkthrough_conversazione.html)
   ([view in browser](https://htmlpreview.github.io/?https://github.com/sorrentinoluca/fot-phd/blob/main/docs/fot_walkthrough_conversazione.html))
2. **Understand repository scope and project status** → this `README.md`
3. **Independently verify the frozen results** →
   [`AUDIT_GUIDE.md`](AUDIT_GUIDE.md)

> All other documents and artifacts are protocol, implementation, provenance,
> freeze, reproducibility, or historical records and are not required for an
> initial scientific review.

## Research objective

The project asks whether distributed agents with non-IID local experience can
transfer useful knowledge about locally unseen time-series conditions by
sharing compact textual insights rather than raw data, gradients, or model
weights.

In this implementation, **FoT** means:

- each agent retains its local time-series data;
- numerical evidence is converted into a neutral textual representation;
- local regularities are distilled into provenance-aware textual insights;
- only eligible peer insights are federated;
- an LLM is invoked under a frozen execution configuration and controlled
  experimental conditions.

This is a bounded proof of concept. It is not a claim of formal privacy,
general FoT superiority, or readiness for deployment.

## Phase A — Numerical evidence to neutral text

Phase A freezes the representation layer:

```text
multivariate time series
→ structured numerical evidence
→ neutral text
```

The representation preserves signed level shift, signed slope, residual
variability, sample-to-sample variability, and temporal activation patterns.
The renderer reports observed facts without assigning a fault label or turning
dispersion automatically into drift, oscillation, or diagnosis.

Phase A therefore validates a descriptive interface, not a new numerical
classifier. Its development, validation, test discipline, exact thresholds,
and frozen hashes are preserved in [`VERBALIZER_V2_FREEZE.md`](supporting_records/phase_a/VERBALIZER_V2_FREEZE.md),
[`tep_validation_v2/`](tep_validation_v2/), and [`tep_test_v2/`](tep_test_v2/).

## Phase B — Federation over Text

Four agents each know Normal plus one local fault pseudoclass. The other three
fault pseudoclasses are locally unseen. Real fault identities are hidden from
the diagnostic LLM behind frozen opaque pseudolabels.

Local examples and insight-generation inputs come only from permitted
development data. Federation is peer-only: an agent receives six insights from
the other three agents, never its own. The frozen experiment compares:

- **A — isolated:** local knowledge only, without peer insights;
- **B — FoT:** genuine peer-derived insights with correct pseudolabel
  associations;
- **E — corrupted control:** the same six peer insights and the same order as
  B, with only the pseudolabel associations changed by the frozen derangement.

Each agent-case-condition was executed three times (`R=3`) and aggregated by
the frozen two-of-three valid-label majority rule. Predictions were frozen
before ground truth was joined offline.

## Main frozen result

The primary subset is composed of fault classes locally unseen by the receiving
agent.

| Condition | Correct / agent-case observations | Accuracy |
|---|---:|---:|
| A — isolated | 0/36 | 0.0000 |
| B — FoT | 31/36 | 0.8611 |
| E — corrupted | 3/36 | 0.0833 |

- **B−A = +0.8611** — preregistered primary contrast.
- **B−E = +0.7778** — preregistered specificity/mechanistic contrast; it is
  not the primary endpoint.

Interpret these numbers with the frozen design:

- the denominator 36 contains **agent-case observations**, not 36 independent
  physical runs;
- the independent fault units are **12 physical runs**, three per fault, each
  judged by the three agents for which that fault was unseen;
- a descriptive decomposition of the frozen outcomes shows that A is at an
  information floor on locally unseen faults: 14/36 abstentions and 22/36
  committed predictions, of which 0/22 are correct;
- abstention remains incorrect under the frozen protocol;
- the secondary 91.67% overall accuracy is not the primary scientific result;
- `harmed=0` does not prove a general absence of negative transfer, because A
  has no correct primary case that B could harm;
- the TEP result supports feasibility only; it does not establish empirical
  generalization to PV.

Exact results and uncertainty estimates are in
[`phase_b/final_evaluation/EVALUATION_REPORT.md`](phase_b/final_evaluation/EVALUATION_REPORT.md).

## Centralized pooled reference (Condition C)

Condition C is a **centralized full-information pooled ICL post-hoc exploratory
reference**. Here, “full-information” is limited to the union of the frozen
prompt-facing artifacts (the pooled labeled examples and textual insights), not
to all source data or source texts. Its 45 provider records cover 15 physical
cases with three repetitions each and produce the following frozen results:

| Scope | Correct / cases | Accuracy |
|---|---:|---:|
| Overall | 15/15 | 1.0000 |
| Fault | 12/12 | 1.0000 |
| Normal | 3/3 | 1.0000 |

There were no abstentions. Against B's 31/36 locally-unseen fault agent-case
outcomes, the descriptive contrast is C−B = 5/36 = 0.138889, with a stratified
cluster-bootstrap 95% interval of [0.083333, 0.166667]. This is not a causal or
equal-unit comparison: C contributes one aggregate prediction for each of 12
physical fault cases, whereas B contributes 36 correlated unseen agent-case
outcomes, and the two conditions differ in both quantity and form of
information. The entire 5/36 advantage is concentrated in `CLS-OJNSG`; the
other nine fault cases have zero C−B difference. It therefore does not
establish a general superiority of centralization or federation.

The numerical source of truth is
[`icl/full_evaluation/evaluation_results_c.json`](icl/full_evaluation/evaluation_results_c.json).
The independent review records **GO WITH LIMITATIONS** in
[`docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md`](docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md).

## Project status

| Component | Status |
|---|---|
| Phase A — neutral TEP representation | Completed and frozen |
| Phase B — TEP Federation over Text | Completed and frozen |
| Frozen held-out inference | 540/540 repetitions; 180 aggregate outcomes |
| Offline evaluation | Completed and frozen |
| Condition C — centralized pooled reference | Completed, frozen, independently reviewed; post-hoc exploratory |
| Empirical PV phase | Not yet executed; no protocol frozen |

The next research phase must redesign and revalidate features, baselines,
windows, event taxonomy, physical units, and ground truth for PV. The TEP
percentages must not be transferred to PV.

## Source-of-truth hierarchy

1. **Frozen scientific artifacts** — manifests, configurations, prompts,
   predictions, evaluator code, bootstrap code, metrics, hashes, and tags.
2. **Canonical scientific documentation** — human-readable interpretation and
   methodological context.
3. **Pedagogical walkthrough** — the primary explanatory route through the
   project.
4. **Historical and superseded records** — preserved to document how decisions
   were made.

`README.md` and the walkthrough are navigation and explanation layers. If they
conflict with a frozen artifact, the frozen artifact is authoritative. Use
[`AUDIT_GUIDE.md`](AUDIT_GUIDE.md) to follow the numerical source-of-truth
chain directly. For Condition C, the canonical result is
[`evaluation_results_c.json`](icl/full_evaluation/evaluation_results_c.json)
and its interpretive audit is the
[`independent R10 review`](docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md).

## Repository map

```text
fot-phd/
├── README.md                           # project orientation
├── AUDIT_GUIDE.md                      # independent verification path
├── DOCUMENTATION_INDEX.md              # complete documentation inventory
├── requirements.txt                    # reference Python dependencies
├── docs/                              # documentation, walkthrough, literature, audits, prompts
│   ├── fot_walkthrough_conversazione.html  # primary scientific/didactic guide
│   ├── lit_review/                     # experiment plan, literature review, related work
│   │   ├── FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md
│   │   └── FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md
│   ├── audits/                        # pre-freeze and post-freeze audit reports
│   ├── prompts/                       # operational AI prompts
│   └── figures/                       # walkthrough and paper figures
├── code/                              # frozen Phase A implementation and evidence
├── phase_b/                           # frozen Phase B protocol, execution, and results
│   ├── final_evaluation/              #   Experiment 1 — frozen results and evaluation report
│   ├── exp3/                          #   Experiment 3 — closed incomplete
│   └── exp3_v2/                       #   Experiment 3 V2 — confirmatory revision
├── icl/                               # Condition C centralized pooled protocol, predictions, and results
├── supporting_records/                # provenance, narratives, and historical records
├── papers/                            # reference papers
├── reproducibility/                   # Phase A verification artifacts
├── tep_validation_v2/                 # Phase A validation artifacts
├── tep_test_v2/                       # Phase A final test artifacts
```

Non-entry-point provenance, narrative, design, and status documents are
consolidated under `supporting_records/`. Frozen or hash-bound documents inside
`phase_b/` remain at their original paths so the committed audit chain and
path-based manifests stay intact.

For a full inventory of all documentation files with descriptions, see
[`DOCUMENTATION_INDEX.md`](DOCUMENTATION_INDEX.md).

## Frozen milestones

| Milestone | Annotated tag | Target commit |
|---|---|---|
| Phase A reproducibility completion | `phase-a-reproducibility-complete` | `145b6b79c59c352e06028166185bad3c9fb49607` |
| Phase B held-out freeze | `phase-b-heldout-frozen` | `86baaa65e72cea22ecb89dd0e7b213aea5a1284b` |
| Phase B protocol freeze | `phase-b-protocol-frozen` | `3d86f64d43e14e7e0de520cb047ca1043bf9c1c0` |
| Execution schedule freeze | `phase-b-execution-schedule-frozen` | `eef0bc58e5ab14fb0cd2aece180fb5b1b5a7962b` |
| Inference freeze | `phase-b-inference-frozen` | `11c34358e28e875cd5c7249061ac2b89ffcd42f4` |
| Results freeze | `phase-b-results-frozen` | `45ec4eed65b263a5803ced7d01064c4672e81e86` |
| Condition C R10 code freeze | `condition-c-freeze-r10` | `60ccc7539714e909aae7318cc72031d7acdd4e78` |
| Condition C R10 predictions freeze | `condition-c-predictions-frozen-r10` | `8d6b7a0636e9a15f0ebbd32ed0f9e2ce4faea30a` |
| Condition C R10 results freeze | `condition-c-results-frozen-r10` | `89e4caebe635973ef438d4b601bb4f761417193a` |

The external TEP source dataset is pinned separately at commit
`309b944f35ac440ff0c70616947ffe723c766e14`.

## Reproducibility boundary

The committed repository preserves the protocol, schedules, local knowledge,
insights, 540 individual LLM records, 180 aggregate predictions, evaluator,
bootstrap, metrics, reports, and cryptographic manifests required to recompute
the reported Phase B results from frozen predictions. It also preserves the
Condition C R10 schedule, 45 repetition records, 15 aggregate predictions,
post-inference manifests, frozen evaluation result, and independent review.

The 15 raw Phase B held-out `.xlsx` workbooks are intentionally excluded from
Git. Their filenames, sizes, and SHA-256 hashes are committed. If supplied
separately, their byte identity and structure can be verified with the frozen
verifier. Their original random simulation realizations cannot be regenerated
bit-for-bit from scripts alone because the initial MATLAB RNG state was not
recorded.

See [`AUDIT_GUIDE.md`](AUDIT_GUIDE.md) for exact commands and boundaries.
