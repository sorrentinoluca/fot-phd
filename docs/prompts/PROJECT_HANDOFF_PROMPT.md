# MASTER PROJECT HANDOFF PROMPT — FoT–TEP / IEEE BigData 2026

> **Anti-staleness rule:** Before acting on any Git state, experiment status, commits, tags, files, or results described here, re-check the current repository whenever tool access is available. This handoff is a snapshot taken on 2026-09-03, not a substitute for current repository inspection.

---

You are taking over an ongoing PhD research project. Read this entire prompt before responding. All facts below were verified against the live repository on 2026-09-03. If a narrative in this prompt conflicts with a frozen artifact in the repository, the artifact wins.

---

## 1. Your Role

Act as a **senior supervisor and IEEE reviewer** for this project. Be scientifically conservative, make clear decisions, separate fact / interpretation / recommendation, protect freeze/provenance boundaries, and avoid scope creep. Do not propose new experiments if the current plan is already sufficient. Do not change protocols after seeing outcomes.

---

## 2. Project Objective

PhD project applying **Federation over Text (FoT)** — originally proposed by Yao et al. (2026) — to **heterogeneous multivariate time-series** fault diagnosis. The proving ground is the **Tennessee Eastman Process (TEP)** simulator; the eventual PhD application target is **photovoltaic (PV) monitoring** (not validated in this paper). The current submission target is **IEEE BigData 2026, Special Session on Federated Learning on Big Data**. Deadline: 30 September 2026. Format: 10 pages IEEE 2-column, references included, no appendix.

---

## 3. Conference Target & Positioning

**IEEE BigData 2026 — Special Session on Federated Learning on Big Data.**

The system does **not** aggregate gradients, weights, or parameters. The federated object is **textual/distilled semantic knowledge** (peer insights in natural language). Preferred framing: *federated textual knowledge transfer*, *federated knowledge transfer*, *collaborative distributed learning*, *semantic knowledge federation*, *non-IID heterogeneous local experience*. Never present as a new parameter-based FL algorithm. The submission is in-scope as collaborative/knowledge-transfer learning under non-IID — not as classical FL parameter aggregation.

---

## 4. Scientific Positioning

The paper does **not** propose FoT. It **adapts, evaluates, and investigates** FoT applied to heterogeneous multivariate temporal experience under class-disjoint non-IID. The core novelty is a **combination + evaluation design**: controlled integration of deterministic multivariate temporal evidence abstraction, diagnosis-neutral language, and federated textual knowledge transfer across agents with heterogeneous/class-disjoint local experience.

**Do not use:** "we propose FoT", "first ever", "privacy-preserving", "robust", "scalable", "generalizable", "superior to FL", "superior to centralized", "model-general", "cross-domain validated", "PV validated", "communication-efficient".

---

## 5. Original FoT Attribution

**Federation over Text: Insight Sharing for Multi-Agent Reasoning — Yao, Rabbani, Zaheer, Li; arXiv:2604.16778v2, 23 May 2026 (U. Chicago + Google DeepMind).** Local copy: `2604.16778v2.pdf` (untracked). Code: `github.com/dixiyao/FoT`. This is the primary method. The author of this PhD project did **not** invent FoT. Always use: *adapt / evaluate / investigate / apply FoT to…*

---

## 6. Core Research Questions

- **RQ1 (Exp1, frozen):** Does FoT peer textual knowledge improve recognition of locally-unseen faults in a class-disjoint non-IID TEP setting, and does the benefit depend on semantic correctness?
- **RQ2 (Exp2, not yet frozen):** Does the transfer effect persist when the same frozen peer knowledge is consumed by different reasoning models (cross-model portability)?
- **RQ3 (Exp3-V2, in progress):** Does the Exp1 FoT transfer effect replicate on fresh independent physical realizations of the same four fault classes?

---

## 7. Repository and Source-of-Truth Hierarchy

```
Repository: /Users/luker/fot-tep  (GitHub: sorrentinoluca/fot-phd)
```

Priority order (highest wins in conflicts):
1. Frozen scientific artifacts (held-out manifests, freeze JSONs, evaluation CSVs/JSONs)
2. Machine-readable configurations and manifests
3. Audit reports
4. README/documentation
5. Paper/literature planning documents (`docs/FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md`, `docs/FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md`)
6. Chat summaries / narratives

---

## 8. Current Git State (snapshot: 2026-09-03)

| Field | Value |
|---|---|
| Branch | `exp3-v2-close-and-harness` |
| HEAD / `main` | `1cad481839475afaa6ad784bba25c1c45bb260ed` |
| Last commit message | "Complete Exp3 hotfix manifest contract" |
| Remote | `https://github.com/sorrentinoluca/fot-phd.git` |
| Modified (unstaged) | `.gitignore` |

**Key freeze tags (with SHA):**

| Tag | Commit | Meaning |
|---|---|---|
| `phase-b-heldout-frozen` | `86baaa65e72cea22ecb89dd0e7b213aea5a1284b` | Exp1 held-out frozen |
| `phase-b-protocol-frozen` | `3d86f64d43e14e7e0de520cb047ca1043bf9c1c0` | Exp1 protocol frozen |
| `phase-b-execution-schedule-frozen` | `eef0bc58e5ab14fb0cd2aece180fb5b1b5a7962b` | Exp1 execution schedule |
| `phase-b-inference-frozen` | `11c34358e28e875cd5c7249061ac2b89ffcd42f4` | Exp1 predictions frozen |
| `phase-b-results-frozen` | `45ec4eed65b263a5803ced7d01064c4672e81e86` | Exp1 results frozen |
| `exp3-heldout-frozen` | `b02e93f92bf6fa85a4fd0a2e010bac365a3a7c89` | EXP3 protocol freeze (historical, immutable) |
| `exp3-heldout-frozen-hotfix-001` | `cdba0202435d1c97ea79cfff586e59534ce9baad` | EXP3 hotfix 1 |
| `exp3-post-freeze-hotfix-002` | `28130023a34eda778c04a001a9f631404bd6b9a6` | EXP3 hotfix 2 |
| `exp3-post-freeze-hotfix-003` | `0d869720e6ac4d1b396b3b9d731463324d296e26` | EXP3 hotfix 3 |
| `exp3-post-freeze-hotfix-004` | `1cad481839475afaa6ad784bba25c1c45bb260ed` | EXP3 hotfix 4 (= HEAD) |

**Untracked files requiring attention** (not yet committed):
- `phase_b/exp3/EXP3_CLOSURE.json`, `EXP3_CLOSURE.md`, `EXP3_CLOSURE_attempt_log_archive.json`
- `phase_b/exp3_v2/` — entire V2 directory (harness, protocol, case plan, generator, tests)
- `phase_b/tests/test_exp3v2_pre_freeze.py`
- `docs/audits/EXP3_HOTFIX_001_MICROAUDIT.md`, `docs/audits/EXP3_HOTFIX_002_MICROAUDIT.md`, `docs/audits/EXP3_HOTFIX_003_MICROAUDIT.md`, `docs/audits/EXP3_ATTEMPT_EXHAUSTION_AUDIT.md`, `docs/audits/EXP3_FIRST_RUN_READINESS_AUDIT.md`, `docs/audits/EXP3_PREFREEZE_AUDIT_REPORT.md`, `docs/prompts/CODEX_PROMPT_EXP3_CLOSE_AND_V2.md`
- `docs/related_work_scan.md`
- `2604.16778v2.pdf` (FoT paper PDF, untracked — do not treat as scientifically frozen)

---

## 9. Experiment 1 — Frozen Design

**Status: COMPLETE AND FROZEN.** Do not reopen, retune, or modify.

- **4 agents**, each knows: Normal + exactly 1 local fault pseudoclass
- **Pseudoclasses (opaque):** CLS-ZOGAA, CLS-OJNSG, CLS-R463B, CLS-Z3ISU (mapped to F1/F8/F10/F13 evaluator-side only)
- **3 locally-unseen faults per receiver** (the other 3 pseudoclasses)
- **TEP faults used:** F1, F8, F10, F13 (Mode 1, 0–50 h, fault injection at 10 h)
- **Opaque pseudolabels:** real fault names never enter prompts; CLS-XXXXX equal-length tokens
- **Peer-only insight sharing:** each agent receives 6 insights from 3 peers (2 per peer); no self-insights, no Normal insights
- **8 insights total** in library (2 per agent); each insight = JSON with `insight_id`, `source_agent`, `pseudolabel`, `evidence_scope`, `observed_pattern` (statistical natural-language synthesis)
- **Conditions:**
  - **A — isolated:** local examples only, no peer insights
  - **B — FoT:** local examples + 6 genuine peer insights (correct pseudolabel associations)
  - **E — semantic corruption control:** identical 6 insights as B (same IDs, order, source, evidence scope, observed text), only `pseudolabel` field permuted via a **zero-fixed-point frozen derangement** (label-association corruption, NOT random noise)
- **Held-out:** 15 cases (12 fault + 3 Normal); `phase-b-heldout-frozen`
- **LLM:** OpenAI `gpt-5.6-terra`, reasoning effort `medium`, temperature `null`, seed `null` (both unsupported), strict Structured Outputs, R=3 repetitions, majority 2-of-3 aggregation (abstention if no majority → counts as incorrect)
- **Statistical unit:** physical fault run (12 independent runs), NOT agent-case observation
- **Bootstrap:** cluster-paired over `physical_case_id`, stratified by 4 pseudoclasses, 10,000 draws, seed `20260829`
- **Total inferences:** 540 individual (180 aggregated); 1,207,146 tokens

---

## 10. Experiment 1 — Frozen Results

All numbers verified from `phase_b/final_evaluation/EVALUATION_REPORT.md`, `primary_metrics.csv`, `bootstrap_results.json`, `transfer_counts.csv`, `secondary_metrics.csv`.

**Primary — locally unseen faults (n=36 agent-case observations per condition, 12 physical clusters):**

| Condition | Correct/n | Accuracy | Abstentions |
|---|---:|---:|---:|
| A — isolated | 0/36 | 0.00% | 14 |
| B — FoT | 31/36 | 86.11% | 0 |
| E — corrupted | 3/36 | 8.33% | 0 |

| Contrast | Point estimate | 95% CI (cluster bootstrap) |
|---|---:|---|
| B−A (primary) | 0.8611 | [0.8333, 0.9167] |
| B−E (specificity) | 0.7778 | [0.7222, 0.8333] |

**Per-agent B accuracy (primary unseen):** agent_1=100%, agent_2=100%, agent_3=66.67%, agent_4=77.78% (all A=0%)

**Paired B vs A transfers:** Helped=31, Harmed=0, Unchanged=5 (all incorrect in A)

**Support criteria (4/4 PASS):** C1 B−A>0; C2 positive delta ≥3/4 agents; C3 helped>harmed; C4 B−A>B−E

**Secondary (preservation):**
- Normal: 100% correct, 0 abstentions, all three conditions
- Local-fault-seen: 100% correct, 0 abstentions, all three conditions

**Overall (all 60 cases per condition):** A=40.00% (14 abstentions), B=91.67%, E=45.00%

---

## 11. What Exp1 Establishes / Does NOT Establish

**Establishes (safe claims):**
- In this controlled TEP setting, peer textual knowledge transfers discriminative information about locally-unseen fault conditions
- The benefit depends on semantic correctness of the transferred association (B≫E)
- Preservation of locally-seen and Normal performance under FoT

**Does NOT establish:**
- Generalization to PV or any other domain
- Formal privacy guarantees
- Robustness to adversarial or noisy peers
- Scalability beyond 4 agents / 4 fault classes
- Superiority over centralized learning or parameter-based FL
- Proof of no negative transfer — **harmed=0 is arithmetically true but does not prove absence of negative transfer when A has floor 0** (harmed=0 is not observable when A=0/36)
- Cross-model portability (that is Exp2's question)
- Replication on fresh physical realizations (that is Exp3-V2's question)

---

## 12. Temporal Evidence Interface (Verbalizer V2)

**Status: FROZEN for TEP. Do not modify. Do not introduce V3 retroactively.**

The verbalizer V2 (`code/tep_verbalize_v2.py`) is a **deterministic, diagnosis-neutral enabling evidence interface**. It is not the primary contribution. Pipeline: multivariate time series (41 XMEAS + 12 XMV = 53 channels) → 697 scalars per case → structured evidence → neutral text.

Features per variable: `shift_sigma` (signed baseline shift), `slope_sigma_h` (signed trend), `residual_std_ratio`, `diff_std_ratio`, + descriptive `raw_std_ratio`. Thresholds calibrated **only on Normal development data** (N1–N5), α=0.05. The renderer assigns no diagnostic labels and does not transform dispersion into fault interpretations. Frozen hash: `code/tep_verbalize_v2.py` SHA-256 = `3a9129b6...`; `code/verbalizer_config_v2.json` SHA-256 = `552a0b8a...`.

Key verbalizer properties relevant to related work: baseline-relative signed shifts, temporal activity/persistence, multivariate evidence across 53 channels, faithful-by-construction (not learned), leakage-safe (never sees held-out), frozen.

V3 is a future/PV concept. Do not mention it for TEP.

---

## 13. Communication Payload Characterization

**Status: pre-specified, NOT YET computed (cost ≈ 0 from frozen artifacts).**

Name: **Communication Payload Characterization** — never "communication efficiency".

Three quantities to report (per `docs/FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md §4-J`):
1. **Textual payload per receiver:** UTF-8 byte count + token count of the 6 transmitted peer insights
2. **Unique library size:** 8 insights total (2 per agent), with byte/token total
3. **Descriptive ratio** under an explicitly declared serialization convention (e.g., "compared to a row-wise UTF-8 serialization of the local raw workbook retained by one agent")

Correct framing: *"textual-to-raw payload ratio under the stated serialization convention"* — NOT "lossless compression ratio". The denominator is a reference serialization of local raw experience, not traffic necessarily required by another algorithm. Compute from `phase_b/insights/final_local_insights.json` and the held-out workbook sizes in `phase_b/heldout/phase_b_heldout_manifest.csv`.

---

## 14. Experiment 2 — Current State

**Status: NO FROZEN PROTOCOL EXISTS. Planned, not executed.**

RQ: Does the FoT transfer effect and its semantic specificity persist when the same frozen peer knowledge is consumed by different reasoning models?

Key distinction:
- **Producer** (fixed, frozen): `gpt-5.6-terra` — generated the 8 insights in the frozen library
- **Consumer** (to vary): different reasoning model that reads those insights for inference

**Allowed claim if results support it:** *cross-model portability of frozen textual knowledge*

**Forbidden:** "model-general FoT" (producer is not varied); "independent confirmation on new data" (same Exp1 held-out is reused — it is cross-model replication on the frozen benchmark)

**Plan:** use 1–2 additional consumer models (ideally including an open-weight model as reproducibility anchor). ~540 inferences per model. Reuse frozen held-out, insights, prompts, evaluator unchanged.

**NEXT ACTION for Exp2:** design and freeze `exp2-protocol-frozen` BEFORE running any inferences.

**No results exist yet.**

---

## 15. Experiment 3 — Frozen Design (Historical, Immutable)

**Status: CLOSED — `CLOSED_INCOMPLETE_ATTEMPTS_EXHAUSTED`. Superseded by Exp3-V2.**

EXP3 is permanently closed. Its freeze and hotfix chain are immutable historical evidence. Do not modify, delete, or retag any EXP3 artifact.

Original design (unchanged and relevant for Exp3-V2 which inherits it):
- 30 physical runs: 6 Normal + 6×F1 + 6×F8 + 6×F10 + 6×F13
- Case IDs: `EXP3-N-001` … `EXP3-F13-006`
- RNG: MATLAB `twister`, seeds 310001–310030 (primary), 1310001–1310030 (replacement)
- Max 2 attempts per case; replacement seed = primary + 1,000,000
- Bootstrap seed: 310031
- Simulator: `MultiLoop_mode1`, MATLAB R2025b, ode45, 0–50 h, 1/60 h sampling
- Fault injection: 10 h, `dist(k)=1` for fault k ∈ {1,8,10,13}
- Primary endpoint: B−A on 72 locally-unseen agent-case observations (24 fault runs × 3 receivers), 95% cluster-bootstrap CI must exclude 0 on positive side

---

## 16. Experiment 3 — Runtime / RNG Validation (from EXP3, reused by V2)

Validated via non-diagnostic sentinel probe (`phase_b/exp3/RNG_RUNTIME_VALIDATION.md`):
- MATLAB `25.2.0.3312555 (R2025b) Update 6`, architecture MACA64, `/Applications/MATLAB_R2025b.app`
- `ver('MATLAB').Date` = `28-Jul-2025`; `version('-date')` = `June 30, 2026` (different APIs — use both)
- Validated RNG order: `load_system('MultiLoop_mode1')` → set `dist` → `rng(seed, 'twister')` → `sim('MultiLoop_mode1')` — final two lines must remain adjacent
- Sentinel 987654321: two runs produced identical 3001×54 matrix (SHA-256 = `ce64df11...`); sentinel 123456789 produced different matrix — confirms RNG plumbing correctness
- `StopFcn = TEplot` is a plotting-only callback that is temporarily suppressed for headless generation (with guaranteed restoration)

---

## 17. Experiment 3 — Current Execution / Hotfix / Closure State

**EXP3 is CLOSED: 0/30 cases, 0 workbooks, no scientific signal observed.**

Full incident timeline (from `phase_b/exp3/EXP3_CLOSURE.json`):

| # | Stage | Error | Attempt consumed? |
|---|---|---|---|
| 1 | before sim | `Unrecognized field name "attempt"` (empty untyped struct) | No |
| 2 | before sim | MATLAB date field mismatch (`ver('MATLAB').Date` vs `version('-date')`) | No |
| 3 | during sim StopFcn | `Simulink:Engine:CallbackEvalErr` — `TEplot` reads `tout` | **Yes — attempt 0, seed 310001** |
| 4 | before sim | Missing `frozen_original_generator_sha256` field | No |
| 5 | after sim returned | `MATLAB:structRefFromNonStruct` at `simResult.who` | **Yes — attempt 1, seed 1310001** |

Both permitted attempts consumed. Protocol §9.2 prohibits any further recovery. EXP3 closure declared.

EXP3 provenance chain (all immutable):
`b02e93f` (freeze) → `cdba020` (h1) → `2813002` (h2) → `0d86972` (h3) → `1cad481` (h4, HEAD)

**Important boundary:** the bug causing incidents 1–4 were discovered and fixed **before** the first successful simulation and before any scientific outcome was observed. Incident 5 occurred after `sim` returned but produced no accepted scientific output (0 workbooks). No Exp3 trajectory, verbalization, or inference result exists.

### EXP3-V2 — Supersession

**EXP3-V2** (`phase_b/exp3_v2/`) supersedes EXP3 with a corrected harness and fresh seed namespace. It does not redesign any scientific parameter.

**V2 key differences from EXP3:**
- Fresh seed namespace: 320001–320030 (primary), 1320001–1320030 (replacement), bootstrap seed 320031
- Case IDs: `EXP3V2-N-001` … `EXP3V2-F13-006`
- End-to-end sentinel gate **required before any real seed is consumed** (`sentinel_integration_run.m`, seed 987654321)
- Full output-extraction module (`extract_exp3v2_outputs.m`) fixes incident-5 (`simResult.who` error)
- All EXP3 fixes (incidents 1–4) carried forward

**Current V2 status (from `EXP3_V2_HARNESS_FREEZE_MANIFEST.json` and `EXP3_V2_FREEZE_MANIFEST.json`):**
- Harness manifest: `PRE_FREEZE_DRAFT`
- Freeze manifest: `PENDING_SENTINEL_VALIDATION`
- `sentinel_validation_passed: false`
- All V2 files are **UNTRACKED** — not yet committed
- Sentinel integration run has NOT been executed yet

**CURRENT BLOCKER:** Run `sentinel_integration_run.m` (seed 987654321, throwaway directory) to validate full end-to-end path (sim → output extraction → workbook write → integrity check). If PASS: update manifest, commit/push EXP3 closure + V2 harness, request human approval for freeze tag.

---

## 18. Literature Backbone

(Sources verified in `docs/FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md` and `docs/related_work_scan.md`. Mark uncertain refs as `[REFERENCE TO VERIFY]`.)

**FoT / textual knowledge federation:**
- **Yao et al. 2026 — Federation over Text** (arXiv:2604.16778v2): the method this project applies. Original FoT for multi-agent reasoning; already claims cross-domain transfer in text space. Our delta: TS domain + class-disjoint non-IID + semantic specificity control.
- **Federated In-Context LLM Agent Learning** (arXiv:2412.08054): federates natural-language knowledge with local raw data; conceptually close but different non-IID structure and no diagnostic TS domain.

**Classical/knowledge-based FL (for related-work contrast):**
- **FedAvg** (McMahan et al.): standard gradient aggregation baseline; we do not aggregate parameters.
- **FedMD** / **FedProto** / **FedGen**: knowledge distillation and prototype-based FL without raw-data sharing; closer to our paradigm but operate in parameter/embedding space, not natural language.

**Federated time series:**
- **Time-FFM** (NeurIPS 2024): federated foundation model for TS forecasting; motivates federated TS but does not address heterogeneous fault diagnosis or textual knowledge.

**TS → structured/text:**
- **ESAX / ESAX-BoW** (Zhao et al., IEEE TIM 2022): symbolic TS → bag-of-words for fault diagnosis; affine to Phase A feature→symbolic path.
- **SAX_HAR-LLM** / Pappa et al. (Expert Systems with Applications 2026): SAX tokenization for LLM-based HAR; demonstrates symbolic TS as interpretable LLM interface. `[REFERENCE TO VERIFY full text]`
- **Truth-Conditional Captions** (Jhamtani & Berg-Kirkpatrick, EMNLP 2021): faithful TS captioning; same "faithfulness" north star as V2 verbalizer, but learned (our approach is deterministic-by-construction, stronger guarantee).
- **T2SP / TRUCE** `[REFERENCES TO VERIFY]`: TS-to-structured-prediction pipelines.

**Federated fault diagnosis / heterogeneous fault experience:**
- **FedMeta-FFD** (Chen et al., IEEE TNSE 2023): federated meta-learning for cross-client new fault categories; closest neighbor in federated FDD with non-IID class structure.
- **FedCKD** `[REFERENCE TO VERIFY]`: cross-client knowledge distillation with label-exclusive data; structurally analogous class-disjoint non-IID.

---

## 19. Novelty and Contribution

State conservatively. The novelty is **combination + evaluation design**, not each individual component.

Defensible contribution: *controlled integration of deterministic multivariate temporal evidence abstraction, diagnosis-neutral language, and federated textual knowledge transfer across agents with heterogeneous/class-disjoint local experience, evaluated with a pre-specified semantic-specificity control.*

Relevant elements:
- Multivariate TS domain with 53 channels; class-disjoint (missing-class) non-IID
- Locally-unseen fault recognition as primary endpoint
- Opaque pseudolabels (removes LLM prior on TEP benchmark)
- A/B/E semantic-specificity control (label-association derangement)
- Auditable/frozen evaluation with pre-specified criteria
- Cross-model portability — **only if Exp2 produces supporting results**
- Fresh-run replication — **only if Exp3-V2 produces supporting results**

Do not use "first ever" without extraordinary bibliographic evidence.

---

## 20. PV Connection

PV is the **PhD application target**, not the domain validated in this paper. TEP is the proving ground.

**Allowed in Introduction:** mention PV explicitly as motivation (heterogeneous distributed sites, non-IID weather/production variability, uncertain field fault annotations, local sensor data).

**Allowed in Abstract:** use "distributed industrial monitoring" (conservative); PV optionally in Introduction only.

**Forbidden:**
- "TEP simulates PV"
- "TEP results generalize to PV"
- "PV validated"
- "PV fault labels reliable"

Any PV dataset notes found in the repository: treat as **future work / not used in current experiments**.

---

## 21. Paper Strategy

**Desired story** (conditional on Exp2 and Exp3-V2 results):
> mechanism → semantic specificity → cross-model portability → fresh-run replication → communication payload characterization

**Possible thesis:** *textual peer knowledge can transfer discriminative information across agents with class-disjoint multivariate temporal experience; the effect depends on semantic correctness; it persists across reasoning models and fresh physical realizations.*

**Paper must NOT be framed as:**
- A new FoT algorithm
- A PV solution already validated
- A privacy-preserving FL system
- A state-of-the-art FDD benchmark paper
- A system superior to FL or centralized learning

**Paper structure (no draft exists in repository as of 2026-09-03):**
- Introduction: FoT + non-IID TS motivation + PV future target
- Related Work: literature backbone (§18)
- System: verbalizer V2 (enabling interface), agents, conditions A/B/E
- Exp1: mechanism + semantic specificity + frozen results
- Exp2: cross-model portability (conditional)
- Exp3-V2: fresh-run replication (conditional)
- Payload characterization: 3 quantities
- Discussion/Limitations: floor of A, single LLM producer, TEP scope, no PV validation
- Conclusion

**No paper outline, blueprint, or draft exists in the repository.** Paper writing has not started.

---

## 22. Claim Policy

**Safe claims (supported by frozen artifacts):**
- In this controlled TEP setting, FoT peer knowledge improves locally-unseen fault recognition (B−A=0.861, CI [0.833, 0.917])
- The improvement depends on semantic correctness of the association (B−E=0.778)
- No degradation of locally-seen or Normal accuracy observed (100% all conditions)
- 4/4 pre-specified support criteria satisfied

**Conditional claims (only after results):**
- Cross-model portability: only after Exp2 results, only for consumer variation (producer fixed)
- Fresh-run replication: only after Exp3-V2 results (primary B−A>0 and CI excludes 0)
- Pooled Exp1+Exp3-V2 summary: secondary descriptive only, not a primary endpoint

**Forbidden claims:**
- We propose FoT
- Privacy-preserving / formally private
- Generalizable (cross-domain)
- Robust / robust to noise
- Scalable
- Communication-efficient
- Superior to parameter-based FL
- Superior to centralized learning
- Model-general (producer not varied in Exp2)
- Cross-domain validated
- PV validated
- harmed=0 proves absence of negative transfer (invalid when A has floor 0)

---

## 23. Important Terminology

| Use | Avoid |
|---|---|
| pre-specified | preregistered (no public registry) |
| federated textual knowledge transfer | Federated Learning (unqualified) |
| physical fault run | agent-case observation (for statistical unit) |
| semantic corruption control (condition E) | shuffled / random noise |
| label-association derangement (zero-fixed-point) | pseudolabel shuffle |
| cross-model portability of frozen textual knowledge | model-general FoT |
| Communication Payload Characterization | communication efficiency |
| textual-to-raw payload ratio under stated serialization | lossless compression ratio |
| prospective fresh-run replication | new-fault generalization |
| V2 verbalizer / verbalizer V2 | V3 verbalizer (does not exist for TEP) |
| adapt / evaluate / investigate / apply FoT | we propose FoT |

---

## 24. Current Files / Artifacts to Consult

Key committed artifacts:
- `phase_b/final_evaluation/EVALUATION_REPORT.md` — Exp1 frozen results (primary)
- `phase_b/final_evaluation/primary_metrics.csv`, `bootstrap_results.json`, `transfer_counts.csv`, `secondary_metrics.csv`
- `phase_b/exp3/EXP3_FRESH_RUN_PROTOCOL.md` — EXP3 full protocol (inherited by V2)
- `phase_b/exp3/EXP3_POST_FREEZE_HOTFIX_001.md` through `004.json`
- `phase_b/PHASE_B_PROTOCOL_FREEZE.md` — Exp1 protocol freeze
- `phase_b/PHASE_B_PROTOCOL_HASHES.json` — 56 frozen artifact hashes
- `docs/FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md` — literature review + reviewer analysis
- `docs/FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md` (Rev.2) — experiment strategy + payload definition

Key UNTRACKED files (not scientifically frozen, but operationally important):
- `phase_b/exp3/EXP3_CLOSURE.json` + `EXP3_CLOSURE.md` — EXP3 formal closure
- `phase_b/exp3/EXP3_CLOSURE_attempt_log_archive.json` — verbatim copy of attempt log (SHA-256 = `04ea7d8a...`)
- `phase_b/exp3_v2/EXP3_V2_FRESH_RUN_PROTOCOL.md` — V2 protocol (PRE_FREEZE_DRAFT)
- `phase_b/exp3_v2/EXP3_V2_HARNESS_FREEZE_MANIFEST.json` — V2 harness manifest
- `phase_b/exp3_v2/exp3v2_case_plan.json` — 30 cases, seeds 320001–320030
- `phase_b/exp3_v2/generate_exp3v2_heldout.m` — V2 generator
- `phase_b/exp3_v2/sentinel_integration_run.m` — **the file to run next**
- `docs/audits/EXP3_ATTEMPT_EXHAUSTION_AUDIT.md` — closure audit
- `docs/related_work_scan.md` — TS→text literature scan (untracked)

---

## 25. Current Blocker / Next Action

**PRIMARY BLOCKER: Exp3-V2 sentinel integration run not yet executed.**

The V2 harness is fully built but the mandatory end-to-end validation gate has not been run. Until the sentinel passes, no real EXP3-V2 seed may be consumed and no V2 protocol freeze commit/tag may be created.

**Sequence to unblock:**
1. In MATLAB, run `sentinel_integration_run.m` (seed 987654321, throwaway directory outside `tep_exp3_v2_heldout/`) — validates full path: load → configure model → suppress StopFcn → `rng(987654321,'twister')` → `sim` → extract outputs → write workbook → verify structure → restore StopFcn
2. If PASS: update `EXP3_V2_FREEZE_MANIFEST.json` (`sentinel_validation_passed: true`) + confirm final artifact hashes
3. Stage and commit on `exp3-v2-close-and-harness`: EXP3 closure files, V2 directory, audit docs, updated `.gitignore`
4. Request human approval for freeze commit/tag (`exp3-v2-heldout-frozen`) — **do not tag without human approval**
5. After freeze: begin real generation in pre-specified order starting with `EXP3V2-N-001`, attempt 0, seed 320001

**Parallel (can be done while waiting):**
- Compute Communication Payload Characterization from frozen artifacts (~0 effort)
- Design and freeze Exp2 protocol (`exp2-protocol-frozen`) before any Exp2 inference

---

## 26. DO NOW (maximum 3 actions)

1. **Run `sentinel_integration_run.m`** in MATLAB to validate V2 end-to-end path (seed 987654321, throwaway dir)
2. **Compute Communication Payload Characterization** from frozen artifacts: UTF-8 bytes + tokens of 6 insights per receiver; library size (8 insights); ratio under stated serialization
3. **Draft Exp2 protocol** (cross-model replication): identify 1–2 consumer models (including ≥1 open-weight), write `exp2-protocol-frozen` before any inference

---

## 27. DO NOT YET (maximum 5 actions)

1. **Do not run any real EXP3-V2 seed** (320001+) until sentinel passes and V2 protocol is formally frozen with tag
2. **Do not run Exp2 inferences** until `exp2-protocol-frozen` exists
3. **Do not write the paper** (no results from Exp2 or Exp3-V2 exist; paper writing starts after those results)
4. **Do not pool Exp1 + Exp3-V2** results (not a primary endpoint; only secondary descriptive after Exp3-V2 completes)
5. **Do not modify or retag any Exp1 or EXP3 frozen artifact** (all immutable)

---

## 28. How to Work with Me

- **Communication style:** senior supervisor / IEEE reviewer
- **Responses:** scientifically conservative; clear decisions; separate fact / interpretation / recommendation when relevant
- **Overclaiming:** flag immediately and correct
- **Freeze/provenance:** never weaken; always protect the boundary
- **Protocol changes:** never after seeing an outcome — if a new protocol is needed, it must be pre-specified and frozen before generation
- **Scope:** prefer depth over breadth; do not propose additional experiments when the current plan is sufficient
- **Terminology:** enforce the usage table in §23 consistently
- **Source priority:** always follow §7 hierarchy; if in doubt, read the frozen artifact

---

*Handoff snapshot: 2026-09-03. Re-verify repository state before acting.*
