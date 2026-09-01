# FoT–TEP project: canonical LLM reference

This is a compact retrieval card derived from the canonical technical narrative
at commit `4e94f69b0bc7e48abece125bd4762088f5e30a36`. It is not a second full
project narrative and does not replace the frozen scientific artifacts.

# Source-of-truth hierarchy

1. **Frozen experimental artifacts and results** are authoritative for the
   exact protocol, records, hashes, predictions, metrics, and bootstrap output.
2. **[FOT_PROJECT_TECHNICAL_NARRATIVE.md](FOT_PROJECT_TECHNICAL_NARRATIVE.md)**
   is the authoritative human-readable technical and didactic narrative.
3. **This reference card** is a compact retrieval layer derived from that
   narrative.
4. **Historical or superseded design documents** are useful for project
   history, but are not sources of truth for the final protocol.

> **Conflict rule:** If this short reference conflicts with a frozen artifact,
> the frozen artifact wins.

## Purpose

Use this file for rapid, caveated answers to: What is the project? Why TEP?
What did Phase A do? What did Phase B test? What was the primary result? What
does it support or not support? What comes next for PV? For the complete
methodological history and teaching context, read the technical narrative.

## Project in 10 points

1. The PhD target is Federation over Text for photovoltaic fault diagnosis.
2. TEP is a preliminary feasibility gate and methodological proving ground.
3. Phase A maps time series to structured evidence and then to neutral text.
4. Phase A does **not** diagnose the fault class.
5. Phase B tests non-IID local agents and peer textual knowledge transfer.
6. Raw data, gradients, and model weights are not federated.
7. A/B/E isolate an agent, add genuine FoT, or add corrupted knowledge.
8. B−A is the preregistered primary contrast.
9. B−E is the preregistered specificity/mechanistic contrast.
10. PV is the next main empirical phase; cross-domain generalization has not
    yet been demonstrated.

## Canonical numbers

| Quantity | Canonical value | Interpretation |
|---|---:|---|
| Unseen A | 0/36 (0.00%) | Isolated condition at an information floor |
| Unseen B | 31/36 (86.11%) | Genuine peer FoT in the tested setup |
| Unseen E | 3/36 (8.33%) | Matched text with corrupted label association |
| Primary B−A | +0.8611 | Preregistered primary contrast |
| Specificity B−E | +0.7778 | Preregistered mechanistic contrast, not primary |
| Per-agent B−A | +1.0000, +1.0000, +0.6667, +0.7778 | Positive for all four agents |
| Helped / harmed / unchanged | 31 / 0 / 5 | Paired B versus A on unseen observations |
| Normal A/B/E | 100% / 100% / 100% | Observed preservation in this sample |
| Local-fault-seen A/B/E | 100% / 100% / 100% | Observed preservation in this sample |
| Overall A/B/E | 40.00% / 91.67% / 45.00% | Secondary mixture of subsets |
| Unseen abstention A/B/E | 38.89% / 0% / 0% | Abstention remains incorrect |
| Bootstrap B−A | [0.8333, 0.9167] | Clustered and stratified 95% interval |
| Bootstrap B−E | [0.7222, 0.8333] | Clustered and stratified 95% interval |

> **Do not interpret 91.67% overall as the main scientific answer.**

## Claim hierarchy

**PRIMARY PREREGISTERED:** B−A.

**SPECIFICITY / MECHANISTIC CONTRAST:** B−E.

**B−E is not the primary endpoint.** It is correct to say that B−E is
interpretively more diagnostic about whether correct transferred information
matters. It is incorrect to say that B−E replaced B−A as the primary result.

## How to interpret A

- A unseen: **0/36 correct**.
- A unseen abstentions: **14/36**.
- A unseen committed predictions: **22/36**.
- Correct among committed predictions: **0/22**.

A was information-deprived for unseen pseudoclasses. It had the full opaque
label space, but no experimental class-semantic evidence for systematic unseen
mapping. It could technically guess a label, so the floor was not a
mathematical impossibility. Nor was the floor dominated by abstention: most
cases were committed predictions, and none was correct.

Abstention remains incorrect in primary scoring. The 14/36–22/36–0/22
breakdown is a post-hoc descriptive characterization, not a new metric or
rescoring rule.

## Supported interpretations

Within this controlled TEP PoC, the evidence supports:

- feasibility of a neutral textual representation of time-series evidence;
- feasibility of LLM reasoning over that representation;
- local generation of textual insight;
- benefit of genuine peer textual knowledge relative to isolation;
- a strong positive B-versus-E specificity contrast;
- methodological feasibility of leakage-resistant FoT evaluation;
- observed preservation of Normal and local-seen performance in this sample.

These are observations within the controlled PoC. They do not prove universal
causality, guarantee safety, or establish cross-domain generalization.

## Do not claim

**DO NOT SAY:**

- “FoT improves diagnosis by 86 percentage points in general.”
- “91.67% is the scientific answer.”
- “B−E is the primary endpoint.”
- “FoT cannot cause negative transfer.”
- “Harmed=0 proves safety.”
- “Phase A is a classifier.”
- “The TEP verbalizer is domain-agnostic.”
- “The method already generalizes to PV.”
- “The PV protocol is already frozen.”
- “FoT has already been shown superior to central ICL.”

## Phase A quick reference

**Purpose:** representation, not diagnosis.

**Features:**

- signed `shift_sigma`;
- signed `slope_sigma_h`;
- `raw_std_ratio`, descriptive only;
- `diff_std_ratio`;
- `residual_std_ratio`.

Thresholds were calibrated only on Normal development data. Structured JSON is
the scientific representation; neutral text is its LLM-readable serialization.
The Phase A evaluator measures descriptive stability and separability, **not
classifier accuracy**.

## Phase B quick reference

- Four agents; each has Normal plus one local fault pseudoclass.
- The other three fault pseudoclasses are locally unseen.
- Fault names are replaced by opaque pseudolabels; their mapping is evaluator-only.
- Diagnosis uses two local examples per local class.
- Each agent generates two local insights from development evidence.
- Federation is peer-only: no self insight and no Normal insight.
- A is isolated; B receives genuine peer insight; E receives the matched text
  with corrupted pseudolabel association.
- `R=3` identical-input LLM repetitions use deterministic aggregation.
- Retry is structural only; it is never triggered by apparent correctness.
- Predictions are frozen before ground-truth evaluation.

## Statistical unit

**Do not say:** “n=36 independent physical cases.”

The correct structure is **12 independent physical fault-runs**, producing
**36 agent-case unseen observations per condition** because three agents assess
each locally unseen physical run. The bootstrap is clustered by
`physical_case_id` and stratified across four true pseudoclasses × three runs.

## Freeze and provenance quick table

| Boundary | Commit | Tag / status |
|---|---|---|
| Source TEP dataset snapshot | `309b944f35ac440ff0c70616947ffe723c766e14` | Pinned external source dataset commit |
| Phase A pre-validation freeze | `3fd960a192bafacbaabce9471e3c3614d6b2d2db` | `verbalizer-v2-pre-validation` |
| Phase A test/closure | `0a45817fd783513e23d58a35c55489404c95feec` | `phase-a-verbalizer-v2-complete` |
| Held-out freeze | `86baaa65e72cea22ecb89dd0e7b213aea5a1284b` | `phase-b-heldout-frozen` |
| Protocol freeze | `3d86f64d43e14e7e0de520cb047ca1043bf9c1c0` | `phase-b-protocol-frozen` |
| Execution schedule freeze | `eef0bc58e5ab14fb0cd2aece180fb5b1b5a7962b` | `phase-b-execution-schedule-frozen` |
| Inference freeze | `11c34358e28e875cd5c7249061ac2b89ffcd42f4` | `phase-b-inference-frozen` |
| Results freeze | `45ec4eed65b263a5803ced7d01064c4672e81e86` | `phase-b-results-frozen` |
| Canonical technical narrative | `4e94f69b0bc7e48abece125bd4762088f5e30a36` | Post-results documentation |

## Historical versus final state

V1 is historically important but superseded. Historical design documents may
contain exploratory options, earlier assumptions, and prototypes. When asked
what was finally done, prefer this order:

`frozen artifacts → final technical narrative → this reference card`

Do not silently promote historical drafts to the final protocol.

## TEP to PV

| Reusable methodological architecture | Must be redesigned or revalidated for PV |
|---|---|
| Representation/reasoning separation | Verbalizer features |
| Non-IID local knowledge structure | Baseline and thresholds |
| Local insight generation and provenance | Time windows and event taxonomy |
| Peer textual federation | Seasonality and irradiance |
| Pseudonymization logic | Temperature and operating regimes |
| Specificity controls | Inverter/site heterogeneity |
| Freeze and held-out discipline | Missing data and sensor drift |
| Physical-run versus LLM-repetition distinction | Real-world ground truth |
| Clustered evaluation philosophy | Independent empirical validation |

> The methodological architecture is designed to be transferable across
> time-series diagnostic domains, whereas the concrete representation layer
> must be adapted and independently validated for the physical domain.

## FoT versus central ICL

FoT versus central ICL is an **open research question** for the future PV
phase. The TEP PoC did not experimentally isolate the value of distributed
provenance against a centrally supplied knowledge base with comparable
information content. This does not invalidate the TEP PoC. It is a research
question that emerged from the controlled experiment and requires a future
comparator.

## Known provenance limits

- The initial MATLAB RNG state was not recorded.
- Separate generation scripts for F1-run11 and Normal-run14 were not preserved.
- No definitive PV dataset or protocol is currently documented.

Do not fill these gaps by inference.

## How an LLM should answer

- For conceptual questions, use this reference together with the technical narrative.
- For exact numerical, hash, or provenance questions, verify against frozen
  repository artifacts whenever executable access is available.
- If executable verification is unavailable, say **“According to the canonical
  project documentation…”** rather than claiming independent verification.
- State the domain, experimental subset, and relevant caveat with every result.
- Never use a historical design draft to override a frozen artifact.

## Recommended answer language

Prefer:

- “supports the interpretation that…”;
- “within the controlled TEP PoC…”;
- “the preregistered primary contrast…”;
- “the specificity/mechanistic contrast…”;
- “empirical cross-domain generalization has not yet been tested.”

Avoid “proves,” “guarantees,” “works generally,” “generalizes to PV,” and “no
negative transfer,” unless explicitly explaining why those claims are
unsupported.

## Quick Q&A

**1. What is Federation over Text here?**  
It is peer sharing of locally generated textual diagnostic insight. Raw time
series, gradients, and model weights are not the federated objects.

**2. Why use TEP?**  
TEP supplies controlled multivariate faults, replication, and offline ground
truth. It is a methodological proving ground for the later PV research phase.

**3. What did Phase A do?**  
It deterministically transformed time-series measurements into structured
evidence and factual neutral text. It did not assign a diagnostic class.

**4. What did Phase B test?**  
It tested whether non-IID agents benefit on locally unseen classes when they
receive genuine peer-derived textual knowledge under a frozen protocol.

**5. What are A, B, and E?**  
A is isolated, B receives genuine peer FoT insight, and E receives otherwise
matched insight with corrupted pseudolabel associations.

**6. What is the primary result?**  
The preregistered primary contrast is B−A on unseen agent-case observations:
31/36 versus 0/36, or +0.8611, within this controlled TEP PoC.

**7. Why is B−E important?**  
B−E is the preregistered specificity/mechanistic contrast (+0.7778). It
supports the interpretation that correct association matters beyond text volume.

**8. Why is A=0/36 not a general baseline comparison?**  
A lacked experimental class-semantic evidence for systematic unseen mapping.
It was an information-deprived protocol condition, not a generally competent
diagnostic baseline or a mathematical impossibility.

**9. Does the work generalize to PV?**  
Not yet empirically. The methodological architecture is transferable in
principle, but the physical representation and protocol require independent PV
design and validation.

**10. What is the next research step?**  
Design the main empirical PV phase: define data and ground truth, adapt the
representation, freeze an independent protocol, and evaluate FoT against
appropriate controls including a central-ICL candidate.

## Verified navigation

- [Canonical technical narrative](FOT_PROJECT_TECHNICAL_NARRATIVE.md)
- [Canonical final synthesis](FOT_TEP_POC_FINAL_SYNTHESIS.md)
- [Phase A V2 freeze](../phase_a/VERBALIZER_V2_FREEZE.md)
- [Phase A canonical status](../phase_a/PHASE_A_STATUS.md)
- [Phase B protocol freeze](../../phase_b/PHASE_B_PROTOCOL_FREEZE.md)
- [Machine-readable frozen protocol](../../phase_b/config/phase_b_protocol_frozen.json)
- [Execution-schedule amendment](../../phase_b/PHASE_B_PROTOCOL_AMENDMENT_001.md)
- [Held-out manifest](../../phase_b/heldout/phase_b_heldout_manifest.csv)
- [Frozen inference metadata](../../phase_b/final_evaluation/inference/execution_metadata.json)
- [Frozen evaluation results](../../phase_b/final_evaluation/evaluation_results.json)
- [Frozen bootstrap results](../../phase_b/final_evaluation/bootstrap_results.json)
- [Human-readable evaluation report](../../phase_b/final_evaluation/EVALUATION_REPORT.md)
