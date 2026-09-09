# Federation over Text for Distributed Time-Series Diagnosis

**Federation over Text (FoT)** is the research project. Its final application
target is **photovoltaic (PV) systems**. The Tennessee Eastman
Process (TEP) is not the target domain: it is a **controlled methodological
proof of concept and feasibility gate** for multivariate time-series knowledge
transfer.

```text
FoT research hypothesis
→ controlled multivariate time-series PoC on TEP
→ validation and fresh-run replication of textual federated knowledge transfer
→ frozen cross-model consumer-portability study on the TEP benchmark
→ future empirical phase: photovoltaic systems
```

The core TEP proof of concept and its fresh-run confirmatory replication are
complete and frozen. They support feasibility and reproducibility across new
physical realizations of the same four TEP fault classes; they do not establish
performance or cross-domain generalization in PV systems. A subsequently
executed **centralized full-information pooled ICL post-hoc exploratory
reference** (Condition C) is also complete, frozen, and independently reviewed.
The consumer-only cross-model extension (Experiment 2) is complete and frozen:
the advantage of B persists with one Qwen open-weight consumer in the examined
configuration. This mitigates dependence on a single proprietary consumer, but
does not establish universal portability or an end-to-end open-weight replica.

## Reading path

1. **Understand the project and experiment** →
   [`docs/fot_walkthrough_conversazione.html`](docs/fot_walkthrough_conversazione.html)
   ([view in browser](https://htmlpreview.github.io/?https://github.com/sorrentinoluca/fot-phd/blob/main/docs/fot_walkthrough_conversazione.html),
   [Markdown source](docs/fot_walkthrough_conversazione.md))
2. **Understand repository scope and project status** → this `README.md`
3. **Independently verify the Experiment 1, Condition C, and EXP2 Qwen frozen results** →
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

- **A — isolated:** four labeled local few-shot examples, with neither peer nor
  self-generated insights; this is an information floor for locally unseen
  classes;
- **B — FoT:** genuine peer-derived insights with correct pseudolabel
  associations;
- **E — corrupted control:** the same six peer insights and the same order as
  B, with only the pseudolabel associations changed by the frozen derangement.

Each agent-case-condition was executed three times (`R=3`) and aggregated by
the frozen two-of-three valid-label majority rule. Predictions were frozen
before ground truth was joined offline.

## Experiment 1 — initial frozen result

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

## Experiment 3 V2 — fresh-run confirmatory replication

EXP3_V2 is the corrective and substitutive prospective replica of the closed,
incomplete Experiment 3. It kept the frozen representation, agents, insights,
conditions, prompts, aggregation rule, evaluator, and four fault classes fixed,
while testing 24 new physical fault runs (six per class) and six new Normal
runs. Its primary locally unseen population contains 72 agent-case observations
per condition, clustered in 24 independent physical fault runs.

| Condition | Correct / agent-case observations | Accuracy |
|---|---:|---:|
| A — isolated | 0/72 | 0.0000 |
| B — FoT | 68/72 | 0.9444 |
| E — corrupted | 4/72 | 0.0556 |

- **B−A = +0.9444**, bootstrap 95% interval **[0.8611, 1.0000]**. The
  pre-specified replication criterion was satisfied.
- **B−E = +0.8889**, bootstrap 95% interval **[0.7778, 0.9861]**. This is
  supporting evidence for semantic specificity, not a second primary endpoint.

The replication strengthens the Experiment 1 feasibility result on new
realizations of the same studied classes, but it is not evidence of new-class,
cross-process, or PV generalization. A relevant secondary result is that B
preserved all Normal observations (24/24) but reduced local-seen fault accuracy
from A's 24/24 to 19/24. Peer insights can therefore interfere with already
known faults in some run-agent combinations, even though they substantially
improve the primary locally unseen population. Condition C was not run on the
EXP3_V2 cases.

The EXP3_V2 artifacts are preserved by tag-only freeze chains and are not
materialized on `main`. The numerical sources of truth are the
[`exp3v2_confirmatory_results.json`](https://github.com/sorrentinoluca/fot-phd/blob/exp3-v2-results-frozen-001/evaluation_outputs/exp3v2_confirmatory_results.json)
and
[`exp3v2_confirmatory_bootstrap.json`](https://github.com/sorrentinoluca/fot-phd/blob/exp3-v2-results-frozen-001/evaluation_outputs/exp3v2_confirmatory_bootstrap.json)
artifacts under `exp3-v2-results-frozen-001`; see
[`phase_b/README.md`](phase_b/README.md) for the experiment map and storage
boundary.

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

## Experiment 2 — frozen Qwen consumer result

Experiment 2 keeps the frozen Experiment 1 held-out cases, local examples,
insights, A/B/E conditions, and evaluation logic fixed while replacing only the
consumer with `Qwen/Qwen3.8-27B-FP8`. The 540 repetitions and 180 aggregates
were frozen before the offline evaluation. On the primary locally-unseen
population, the result is:

| Condition | Correct / agent-case observations | Accuracy |
|---|---:|---:|
| A — isolated | 0/36 | 0% |
| B — FoT | 34/36 | 94.44% |
| E — corrupted | 1/36 | 2.78% |

- **B−A = 0.944444**, bootstrap 95% CI **[0.916667, 1.0]**;
- **B−E = 0.916667**, bootstrap 95% CI **[0.833333, 1.0]**;
- 34 observations were helped, 0 harmed, and 2 remained incorrect; there were
  zero abstentions and the four primary criteria C1–C4 passed (**4/4 PASS**).

The secondary results are local-seen A 100%, B 75%, E 100%; Normal 100% for
A, B, and E; and overall A 40%, B 91.67%, E 41.67%. H2 is a distinct secondary
control, not one of C1–C4, and it fails.

The canonical outputs are the
[`evaluation report`](phase_b/exp2/qwen/evaluation/EVALUATION_REPORT.md),
[`evaluation results`](phase_b/exp2/qwen/evaluation/evaluation_results.json),
[`bootstrap results`](phase_b/exp2/qwen/evaluation/bootstrap_results.json), and
[`primary`](phase_b/exp2/qwen/evaluation/primary_metrics.csv) and
[`secondary`](phase_b/exp2/qwen/evaluation/secondary_metrics.csv) metrics. The
frozen Git chain is:

- `phase-b-exp2-qwen-protocol-frozen-001` → `d9bb95c31bdeb2f1608aaedc52f25b98de9bbf96`;
- `phase-b-exp2-qwen-predictions-frozen-001` → `a4f264c210873536c989ebd99aa2c6cf9857c85c`;
- `phase-b-exp2-qwen-evaluator-frozen-001` → `a8f9884dfe2150a89131ba604b34ff1f6914f6e9`;
- `phase-b-exp2-qwen-results-frozen-001` → `37195cf2c5076b5da724b857f10e157177654cac`.

The archived
[`evaluator review`](docs/audits/EXP2_QWEN_EVALUATOR_REVIEW.md) and
[`independent results review R2`](docs/audits/EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW_R2.md)
record the final verdict **GO WITH LIMITATIONS**. Only one open-weight consumer
was tested, while the insights were still produced with `gpt-5.6-terra` and the
same held-out cases were reused. The cross-model comparison is therefore
descriptive. With temperature zero and a fixed seed, all three repetitions are
byte-identical for every aggregate, so `R=3` does not measure variability. A is
a constant local-label classifier on fault cases and is a structural unseen
floor. Errors also show systematic `CLS-OJNSG` ↔ `CLS-Z3ISU` confusion.

The effective reasoning cap is 1023 tokens despite a nominal budget of 1024.
All five aggregate B errors have all three repetitions at that cap, whereas all
36 uncapped B aggregates are correct. H2 is consequently confounded with
reasoning-budget exhaustion and cannot be causally attributed to insight
interference without a separate sensitivity analysis. B and E have comparable
prompt length, reasoning use, and insight-citation rates; the strong B−E result
supports specificity to insight content, but is not definitive causal proof.

Accordingly, B's advantage persists for a second, open-weight consumer in this
frozen configuration. This mitigates the single proprietary-consumer concern;
it does not demonstrate universal portability, cross-model generality, or
end-to-end independence from a proprietary model.

## Project status

| Component | Status |
|---|---|
| Phase A — neutral TEP representation | Completed and frozen |
| Experiment 1 — initial TEP held-out | Completed and frozen; 540/540 repetitions and 180 aggregate outcomes |
| Experiment 3 | Closed incomplete after technical attempt exhaustion; no scientific data produced |
| Experiment 3 V2 — fresh-run confirmatory replica | Completed and frozen (tag-only); 1,080/1,080 repetitions and 360 aggregate outcomes |
| Condition C — centralized pooled reference | Completed, frozen, independently reviewed; post-hoc exploratory |
| Experiment 2 — cross-model consumer portability | Completed, frozen, reproduced, and independently reviewed; `GO WITH LIMITATIONS` |
| Empirical PV phase | Not yet executed; no protocol frozen |

Before the later empirical PV phase, features, baselines, windows, event
taxonomy, physical units, and ground truth must be redesigned and revalidated.
The TEP percentages must not be transferred to PV.

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
For EXP2 Qwen, use the
[`evaluation report`](phase_b/exp2/qwen/evaluation/EVALUATION_REPORT.md) and the
[`independent results review R2`](docs/audits/EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW_R2.md).

## Repository map

```text
fot-phd/
├── README.md                           # project orientation
├── AUDIT_GUIDE.md                      # independent verification path
├── DOCUMENTATION_INDEX.md              # complete documentation inventory
├── requirements.txt                    # reference Python dependencies
├── docs/                              # documentation, walkthrough, literature, audits, prompts
│   ├── fot_walkthrough_conversazione.html  # primary scientific/didactic guide
│   ├── fot_walkthrough_conversazione.md    # Markdown source of the guide
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
│   └── exp3_v2/                       #   Experiment 3 V2 — confirmatory revision (tag-only results)
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
| EXP3_V2 final held-out boundary | `exp3-v2-heldout-frozen-002` | `6f88abdecc25e015064e5fc2c59000f8a1a0bc7e` |
| EXP3_V2 held-out data | `exp3-v2-heldout-data-frozen-001` | `7bcf309910920b52c485125312599d1ded9c4c74` |
| EXP3_V2 verbalizations | `exp3-v2-verbalizations-frozen-001` | `4159fba5e4d23cbc9af62c2aad72f11eda1491db` |
| EXP3_V2 inference | `exp3-v2-inference-frozen-001` | `9a7ccaa95bae8c0d2d00dc0959e177eb90a5cd61` |
| EXP3_V2 results | `exp3-v2-results-frozen-001` | `3781d6801191757a47bd919f0e4e9705b5895769` |
| Condition C R10 code freeze | `condition-c-freeze-r10` | `60ccc7539714e909aae7318cc72031d7acdd4e78` |
| Condition C R10 predictions freeze | `condition-c-predictions-frozen-r10` | `8d6b7a0636e9a15f0ebbd32ed0f9e2ce4faea30a` |
| Condition C R10 results freeze | `condition-c-results-frozen-r10` | `89e4caebe635973ef438d4b601bb4f761417193a` |

The external TEP source dataset is pinned separately at commit
`309b944f35ac440ff0c70616947ffe723c766e14`.

## Reproducibility boundary

For Experiment 1, the `main` tree preserves the protocol, schedules, local
knowledge, insights, 540 individual LLM records, 180 aggregate predictions,
evaluator, bootstrap, metrics, reports, and cryptographic manifests required to
recompute the reported results from frozen predictions.

EXP3_V2 is preserved separately through ordinary-Git annotated tags rather than
being materialized on `main`. Its tag-only chain contains the 30 frozen held-out
workbooks, frozen verbalizations, 1,080 individual LLM records, 360 aggregate
predictions, evaluation artifacts, and integrity manifests. The results are
governed by `exp3-v2-results-frozen-001`.

The repository also preserves the Condition C R10 schedule, 45 repetition
records, 15 aggregate predictions, post-inference manifests, frozen evaluation
result, and independent review.

The EXP2 Qwen lane preserves 540 deterministic repetition records, 180
aggregate predictions, their hash manifests, the frozen offline evaluation,
and the two canonical reviews. All files under `phase_b/exp2/qwen/` remain
bound to `phase-b-exp2-qwen-results-frozen-001`.

The 15 raw Experiment 1 held-out `.xlsx` workbooks are intentionally excluded
from Git. Their filenames, sizes, and SHA-256 hashes are committed. If supplied
separately, their byte identity and structure can be verified with the frozen
verifier. Their original random simulation realizations cannot be regenerated
bit-for-bit from scripts alone because the initial MATLAB RNG state was not
recorded. This limitation is specific to Experiment 1; the 30 EXP3_V2
workbooks are preserved in its tag-only data freeze.

See [`AUDIT_GUIDE.md`](AUDIT_GUIDE.md) for the exact Experiment 1, Condition C,
and EXP2 Qwen commands and boundaries, and [`phase_b/README.md`](phase_b/README.md)
for the EXP3_V2 tag-only chain.
