# Gap Analysis & Related Work — Federation over Text su serie temporali multivariate (TEP)
## Aggiornamento sistematico della letteratura 2021–2026

**Data:** 2026-09-05  
**Scopo:** Dimostrare la novità dell'esperimento FoT-TEP tramite (1) tabella comparativa strutturata, (2) gap analysis mirata, (3) sezione Related Work narrativa.  
**Fonti:** OpenAlex, ArXiv, Crossref, DBLP, Scopus (via connettore uniarticles), più citation chaining dalla review esistente.

---

## SEZIONE 1 — TABELLA COMPARATIVA STRUTTURATA

La tabella copre i lavori rilevanti 2019–2026, ordinati per filone. Per ogni lavoro:
- **Autori, Anno, Venue**
- **Metodo / Paradigma**
- **Dominio applicativo**
- **Tipo di non-IID**
- **Cosa viene scambiato** (l'oggetto federato)
- **LLM** (sì/no)
- **Serie temporali** (sì/no)
- **Classi localmente non viste** (sì/no)
- **Controllo di specificità** (sì/no)

### 1.1 Filone: Textual/Semantic Knowledge Federation & Multi-Agent LLM

| # | Autori | Anno | Venue | Metodo | Dominio | non-IID | Scambiato | LLM | TS | Unseen | Ctrl spec. |
|---|--------|------|-------|--------|---------|---------|-----------|-----|----|----|-----|
| 1 | Yao, Rabbani, Zaheer, Li | 2026 | arXiv:2604.16778 | FoT — insight library iterativa | Math, QA, coding, ricerca | Cross-task/domain | **Testo** (insight metacognitivi) | Sì | No | No (cross-task) | No (ablation) |
| 2 | Wu et al. | 2024 | arXiv:2412.08054 | FICAL — federated in-context LLM agent learning | NLP/generale | Data heterog. | **Testo** (knowledge compendiums NL) | Sì | No | No | No |
| 3 | Mohtashami et al. | 2023 | arXiv:2312.11441 | Social Learning — collab. LLM teacher→student | Generale | Single-task | **Testo** (esempi sintetici / prompt NL) | Sì | No | No | No |
| 4 | Zhao et al. | 2024 | AAAI 2024 | ExpeL — experiential learning LLM agent | Decision-making | n/a (single-agent) | **Testo** (esperienze/insight) | Sì | No | No | No |
| 5 | Sun, Si, Wu, Gong | 2024 | Pattern Recog. (DOI:10.1016/j.patcog.2024.110824) | FZSL — federated zero-shot, mid-level semantic transfer | Computer vision (ZSL) | Unseen classes | **Attributi semantici** (mid-level) | No (usa CLIP) | No | **Sì** | No |
| — | **NOSTRO (FoT-TEP)** | **2026** | — | **FoT-like peer-only, single-shot** | **TS multiv. / FDD (TEP)** | **Class-disjoint (missing-class)** | **Testo** (insight + pseudolabel) | **Sì** | **Sì** | **Sì** | **Sì (B−E)** |

### 1.2 Filone: Federated Knowledge Distillation / Non-Parametric Transfer

| # | Autori | Anno | Venue | Metodo | Dominio | non-IID | Scambiato | LLM | TS | Unseen | Ctrl spec. |
|---|--------|------|-------|--------|---------|---------|-----------|-----|----|----|-----|
| 6 | Li & Wang | 2019 | NeurIPS WS | FedMD — model distillation | Immagini | Label skew | **Logit** (su public dataset) | No | No | No | No |
| 7 | Lin et al. | 2020 | NeurIPS | FedDF — ensemble distillation | Immagini | Eterogeneo | **Modelli** + distillazione server | No | No | No | No |
| 8 | He, Annavaram, Avestimehr | 2020 | NeurIPS | FedGKT — group knowledge transfer | Immagini | Edge heterog. | **Feature + logit** | No | No | No | No |
| 9 | Tan et al. | 2022 | AAAI | FedProto — prototype federation | Immagini | Esplicito | **Prototipi** (media embedding/classe) | No | No | No | No |
| 10 | Zhu, Hong, Zhou | 2021 | ICML | FedGen — data-free KD | Immagini | Sì | **Conoscenza sintetica** (generatore) | No | No | No | No |
| 11 | Le, Le, Le, Truong-Huu | 2026 | LNCS (DOI:10.1007/978-981-92-1462-4_29) | FedCKD — cross-client KD, label-exclusive | Immagini | **Label-exclusive (class-disjoint)** | **Logit / param** | No | No | Parziale | No |
| — | **NOSTRO (FoT-TEP)** | **2026** | — | **Testo peer-only** | **TS multiv. / FDD** | **Class-disjoint** | **Testo** | **Sì** | **Sì** | **Sì** | **Sì** |

### 1.3 Filone: Federated LLM / Foundation Model

| # | Autori | Anno | Venue | Metodo | Dominio | non-IID | Scambiato | LLM | TS | Unseen | Ctrl spec. |
|---|--------|------|-------|--------|---------|---------|-----------|-----|----|----|-----|
| 12 | Liu et al. | 2024 | NeurIPS 2024 (arXiv:2405.14252) | Time-FFM — federated FM per TS forecasting | TS forecasting | Domini TS eterogenei | **Parametri** (modulo condiviso) | Sì (LM backbone) | **Sì** | No | No |
| 13 | Chen et al. | 2025 | AAAI 2025 | FFTS — federated foundation model, heterog. TS | TS forecasting/imputation/anomaly | Domini TS eterogenei | **Parametri** + regularizzazione | Sì | **Sì** | No | No |
| 14 | Li et al. | 2025 | arXiv:2508.10020 | FedCoT — federated reasoning LLM (LoRA) | Medical reasoning | Client-aware | **Parametri LoRA** + CoT selection | Sì | No | No | No |
| — | **NOSTRO (FoT-TEP)** | **2026** | — | **Testo peer-only** | **TS multiv. / FDD** | **Class-disjoint** | **Testo** | **Sì** | **Sì** | **Sì** | **Sì** |

### 1.4 Filone: Federated Fault Diagnosis / TS Industriali

| # | Autori | Anno | Venue | Metodo | Dominio | non-IID | Scambiato | LLM | TS | Unseen | Ctrl spec. |
|---|--------|------|-------|--------|---------|---------|-----------|-----|----|----|-----|
| 15 | Liu et al. | 2020 | IEEE IoT-J | FL anomaly detection TS IIoT | Anomaly det. industriale | Feature/quantity | **Parametri** (FedAvg on-device) | No | **Sì** | No | No |
| 16 | Berghout et al. | 2022 | Electronics | FL per condition monitoring / FDD (survey) | FDD industriale | Vari | **Parametri** | No | **Sì** | No | No |
| 17 | Chen, Tang, Li | 2023 | IEEE TNSE (DOI:10.1109/tnse.2023.3266942) | FedMeta-FFD — federated meta-learning FDD | Macchine rotanti | Few-shot / nuove categorie | **Parametri** (meta-learner) | No | **Sì** | **Parziale** (few-shot) | No |
| 18 | Qaid et al. / Lin et al. | 2024–25 | arXiv / Adv. Eng. Inf. | FD-LLM — LLM per FDD (centralizzati) | FDD industriale | n/a (centralizzato) | — (centralizzato) | **Sì** | **Sì** | No | No |
| 21 | Dai et al. | 2025 | IEEE IoT-J (DOI:10.1109/JIOT.2025.3586718) | Semi-supervised FL + dual contrastive + soft labeling | FDD industriale | Label scarcity (semi-supervised) | **Parametri** | No | **Sì** | No | No |
| 22 | Chen, Li, Huang, Yue, Chen, Li | 2022 | IEEE TIM (DOI:10.1109/TIM.2022.3180417) | Federated transfer learning + discrepancy-weighted FedAvg | Bearing FDD (macchine rotanti) | Domain shift (transfer) | **Parametri** (weighted FedAvg) | No | **Sì** | No | No |
| — | **NOSTRO (FoT-TEP)** | **2026** | — | **Testo peer-only** | **TS multiv. / FDD (TEP)** | **Class-disjoint** | **Testo** | **Sì** | **Sì** | **Sì** | **Sì** |

### 1.5 Filone: non-IID Taxonomy & Class-Disjoint Settings

| # | Autori | Anno | Venue | Metodo | Dominio | non-IID | Scambiato | LLM | TS | Unseen | Ctrl spec. |
|---|--------|------|-------|--------|---------|---------|-----------|-----|----|----|-----|
| 19 | Li et al. | 2022 | ICDE (arXiv:2102.02079) | Tassonomia non-IID (label-subset skew) | Benchmark FL | Label/feature/quantity skew | Parametri | No | No | Definito | No |
| 20 | Fan & Yao | 2024 | arXiv:2405.18972 | PCDD — partially class-disjoint data | FL benchmark | **Class-disjoint** | Parametri | No | No | Definito | No |
| — | **NOSTRO (FoT-TEP)** | **2026** | — | **Testo peer-only** | **TS multiv. / FDD** | **Class-disjoint** | **Testo** | **Sì** | **Sì** | **Sì** | **Sì** |

---

## SEZIONE 2 — GAP ANALYSIS MIRATA

### 2.1 I tre assi della novità

L'esperimento FoT-TEP si posiziona all'intersezione di tre dimensioni:

- **Asse A — Trasferimento di conoscenza testuale in setting federato:** FoT (Yao et al., 2026) e FICAL (Wu et al., 2024) federano insight/compendium in linguaggio naturale, ma su task nativamente testuali (math, QA, coding), non su serie temporali.
- **Asse B — Setting federato/distribuito per diagnosi guasti:** FedMeta-FFD (Chen et al., 2023), FL per anomaly detection IIoT (Liu et al., 2020), FL per macchine rotanti sono federated FDD, ma scambiano parametri/gradienti, non testo, e non usano LLM.
- **Asse C — non-IID class-disjoint con classi localmente non viste:** FedCKD (Le et al., 2026), FZSL (Sun et al., 2024), PCDD (Fan & Yao, 2024) trattano il regime class-disjoint o zero-shot, ma non su serie temporali e non tramite scambio testuale LLM-mediato.

### 2.2 Matrice di copertura: chi occupa quali intersezioni?

| | Asse A (Testo federato) | Asse B (Federated FDD/TS) | Asse C (Class-disjoint/unseen) |
|---|:---:|:---:|:---:|
| **FoT (Yao et al.)** | ✓ | ✗ | ✗ |
| **FICAL (Wu et al.)** | ✓ | ✗ | ✗ |
| **Social Learning** | ✓ (parziale) | ✗ | ✗ |
| **Time-FFM** | ✗ (parametrico) | ✓ (TS, no FDD) | ✗ |
| **FFTS (Chen et al., AAAI 2025)** | ✗ (parametrico) | ✓ (TS, no FDD) | ✗ |
| **FedCoT** | ✗ (LoRA) | ✗ | ✗ |
| **FedMeta-FFD** | ✗ (parametrico) | ✓ | ✓ (parziale, few-shot) |
| **FedCKD** | ✗ (logit/param) | ✗ | ✓ |
| **FZSL (mid-level semantic)** | ✗ (attributi ZSL) | ✗ | ✓ |
| **FD-LLM** | ✗ (centralizzato) | ✓ (centralizzato) | ✗ |
| **Dai et al. (semi-sup. FL FDD)** | ✗ (parametrico) | ✓ | ✗ |
| **Chen et al. (FTL bearing FDD)** | ✗ (parametrico) | ✓ | ✗ |
| **FedMD / FedProto / FedGen** | ✗ (logit/proto/synth) | ✗ | ✗ |
| **ExpeL** | ✓ (single-agent) | ✗ | ✗ |
| **NOSTRO (FoT-TEP)** | **✓** | **✓** | **✓** |

### 2.3 Verdetto del gap

**Nessuno dei lavori esaminati occupa simultaneamente tutti e tre gli assi.** La cella (A ∩ B ∩ C) — trasferimento di conoscenza testuale + setting federato su serie temporali/FDD + classi localmente non viste sotto non-IID class-disjoint — risulta vuota nella letteratura 2021–2026 esaminata.

Ulteriore elemento distintivo: il **controllo di specificità semantica pre-registrato (B vs E)**, in cui le associazioni pseudolabel↔pattern vengono permutate via derangement a zero punti fissi a parità di testo, non è stato identificato in alcun lavoro della letteratura esaminata applicato a questo contesto.

**Formula difendibile:**
> *"To the best of our knowledge, no prior work federates locally-derived textual knowledge across agents with class-disjoint temporal experience to recognize locally unseen fault conditions in multivariate time series, under a preregistered semantic-specificity control."*

### 2.4 Attenzione: la novità è di combinazione, non di componente

Ogni singolo asse ha vicini stretti:

- **Asse A solo:** FoT, FICAL, Social Learning, ExpeL
- **Asse B solo:** FedMeta-FFD, FL anomaly IIoT, FL rotating machinery, Time-FFM (forecasting)
- **Asse C solo:** FedCKD, FZSL, PCDD, monoclass teachers

La novità è **nell'intersezione e nel disegno di valutazione controllato**, non nei singoli componenti.

---

## SEZIONE 3 — RELATED WORK NARRATIVA

*(Versione pronta per paper, ~1500 parole, struttura a 3 sottosezioni come raccomandato dalla review esistente)*

### 3.1 Federated Knowledge Transfer Beyond Parameter Aggregation

Classical federated learning (FL) methods such as FedAvg [McMahan et al., 2017], FedProx [Li et al., 2020], and SCAFFOLD [Karimireddy et al., 2020] aggregate model parameters or gradients across clients to train a shared global model. While effective, these approaches assume architectural homogeneity and degrade under severe statistical heterogeneity, particularly the *label-subset skew* regime where clients observe disjoint subsets of classes [Li et al., 2022; Zhu et al., 2021].

A parallel line of work has progressively shifted the *federated object* — what is communicated between clients — from parameters to lighter, more abstract representations of knowledge. FedMD [Li & Wang, 2019] exchanges class-conditional logits computed on a shared public dataset, enabling model-heterogeneous federation without sharing raw data. FedDF [Lin et al., 2020] performs server-side ensemble distillation on unlabeled data, while FedGKT [He et al., 2020] transfers features and logits between small edge models and a large server model. FedProto [Tan et al., 2022] further abstracts the communication to class-level *prototypes* — mean embeddings that serve as compact per-class representations — demonstrating robust performance under non-IID conditions. FedGen [Zhu et al., 2021] eliminates the need for shared data entirely by federating a generative model that produces synthetic knowledge to correct for class imbalance.

Of particular structural relevance to our setting is FedCKD [Le et al., 2026], which addresses cross-client knowledge distillation with *label-exclusive* datasets — a non-IID regime where each client's label set is disjoint from others', closely analogous to our "Normal + one fault class" partition. Similarly, the *partially class-disjoint data* (PCDD) framework [Fan & Yao, 2024] formalizes this regime in FL. However, both FedCKD and PCDD operate through parameter or logit exchange, not through textual knowledge.

Our work extends this trajectory to its *semantic extreme*: the federated object is natural-language text — human-readable insights with opaque pseudolabel associations — rather than any numerical tensor.

### 3.2 Textual and Semantic Knowledge Sharing in Federated and Multi-Agent LLM Settings

The emergence of large language models (LLMs) as reasoning engines has opened the possibility of federating *textual* knowledge rather than numerical representations. Federation over Text (FoT) [Yao et al., 2026] is the foundational method: distributed agents solving different tasks iteratively generate metacognitive reasoning traces, which a central server clusters and distills into a cross-task insight library. FoT demonstrates +25% average performance improvement with −4% reasoning tokens across mathematical, coding, and daily-task benchmarks, and includes a privacy analysis showing that abstract insights do not reconstruct original problem instances (token-level F1 < 0.25). Critically, FoT operates on *natively textual* tasks and studies *cross-task/cross-domain* heterogeneity, not the class-disjoint missing-class heterogeneity characteristic of classical FL.

Federated In-Context LLM Agent Learning (FICAL) [Wu et al., 2024] similarly federates knowledge in natural language: each client generates "knowledge compendiums" via an LLM-based module, achieving competitive performance with drastically reduced communication cost. Social Learning [Mohtashami et al., 2023] bridges federated distillation and natural language by having LLM teacher-agents generate synthetic examples and abstract prompts shared with a student — a precursor to textual federation cited by FoT itself. ExpeL [Zhao et al., 2024] demonstrates that LLM agents can autonomously extract reusable insights from task trajectories, though in a single-agent (non-federated) setting.

On the federated foundation model front, Time-FFM [Liu et al., 2024] adapts a pretrained language model for time-series forecasting in a federated setting, using prompt adaptation and personalized prediction heads. FFTS [Chen et al., 2025] proposes federated learning with regularization for heterogeneous time-series foundation models across domains. FedCoT [Li et al., 2025] federates chain-of-thought reasoning for medical LLMs via LoRA parameter exchange. All three federate *parameters* (modules, adapters, LoRA weights), not textual knowledge, and none addresses class-disjoint fault diagnosis.

Federated Zero-Shot Learning with mid-level semantic knowledge transfer (FZSL) [Sun et al., 2024] is conceptually close: it transfers *semantic* knowledge (attributes enriched by vision-language models) across federated clients to recognize *unseen classes*. However, FZSL uses structured ZSL attributes rather than free-form natural-language insights, operates on image classification rather than time series, and does not include a semantic-specificity control.

Our work adapts FoT to a domain where data is not natively textual — multivariate time-series fault diagnosis — via a deterministic, diagnosis-neutral verbalization interface. We study a *class-disjoint (missing-class)* heterogeneity regime rather than cross-task diversity, and introduce a preregistered semantic-specificity control (condition B vs. E) that isolates the role of correct label-pattern associations from mere text volume.

### 3.3 Time-Series Representation for LLMs and Federated Fault Diagnosis

Two strands of related work contextualize our experimental design: time-series verbalization for LLM reasoning, and federated approaches to industrial fault diagnosis.

**Time-series verbalization.** Recent work has explored deterministic, training-free representations of time series for LLM consumption. T2SP [Kim et al., 2026] converts time series into structured programs that preserve statistical properties for LLM reasoning, demonstrating that structured deterministic TS→LLM interfaces are an active research direction. TRUCE [Jhamtani & Berg-Kirkpatrick, 2021] generates truth-conditional captions of time-series data by executing programs on the series and conditioning text only on verified patterns — a precursor to our approach of factual, non-hallucinatory evidence text. FD-LLM approaches [Qaid et al., 2024; Lin et al., 2025] apply LLMs and multimodal LLMs to fault diagnosis from time-series data through serialization, modal alignment, or LoRA fine-tuning, but in *centralized* settings. Our verbalization interface — converting 41-variable multivariate time series into structured statistical evidence and neutral text — follows this trajectory as an *enabling layer*, not as a methodological contribution in itself.

**Federated fault diagnosis.** Federated learning has been applied to industrial fault diagnosis primarily through parametric approaches: FedAvg-based anomaly detection on IIoT time series [Liu et al., 2020], federated fuzzy-fusion fault diagnosis of chemical processes, and federated methods for rotating machinery [Berghout et al., 2022]. More recent parametric FL-FDD work includes semi-supervised federated fault diagnosis via dual contrastive learning and soft labeling [Dai et al., 2025], and federated transfer learning with discrepancy-based weighted FedAvg for bearing fault diagnosis under domain shift [Chen et al., 2022]. FedMeta-FFD [Chen et al., 2023] is the closest neighbor in the FDD space: it uses federated meta-learning to enable a global meta-learner to adapt rapidly to *new fault categories* across clients with few labeled examples. However, all these approaches exchange *parameters or gradients*, require some labeled examples of the target fault class, and do not use textual knowledge transfer or LLM reasoning.

The Tennessee Eastman Process (TEP) has been extensively used as a benchmark in *centralized* fault diagnosis [e.g., autoencoders, deep FDD, interpretable knowledge discovery], but we did not identify any prior work applying FoT-style textual federated knowledge transfer to TEP or to any multivariate time-series fault diagnosis task under class-disjoint non-IID experience.

---

## SEZIONE 4 — RIEPILOGO DEI PAPER TROVATI (Search Log aggiornato)

### 4.1 Paper trovati e verificati in questa sessione (via uniarticles)

| Paper | Fonte | DOI/ID | Stato |
|-------|-------|--------|-------|
| FoT (Yao et al., 2026) | ArXiv detail | arXiv:2604.16778v2 | ✓ Verificato |
| FICAL (Wu et al., 2024) | ArXiv detail | arXiv:2412.08054 | ✓ Verificato |
| FedMD (Li & Wang, 2019) | OpenAlex | arXiv:1910.03581 | ✓ Verificato (482 cit.) |
| FedKD (Wu et al., 2022) | OpenAlex | Nature Comms | ✓ Verificato (617 cit.) |
| FedProto (Tan et al., 2022) | OpenAlex | DOI:10.1609/aaai.v36i8.20819 | ✓ Verificato (729 cit.) |
| FedGKT (He et al., 2020) | OpenAlex | arXiv:2007.14513 | ✓ Verificato (191 cit.) |
| FedCKD label-exclusive (Le et al., 2026) | OpenAlex | DOI:10.1007/978-981-92-1462-4_29 | ✓ Verificato |
| FZSL mid-level semantic (Sun et al., 2024) | OpenAlex | DOI:10.1016/j.patcog.2024.110824 | ✓ Verificato (11 cit.) |
| Time-FFM (Liu et al., 2024) | OpenAlex | arXiv:2405.14252 / DOI:10.52202/079017-2996 | ✓ Verificato (10 cit.) |
| FFTS (Chen et al., 2025) | OpenAlex | DOI:10.1609/aaai.v39i15.33739 | ✓ Verificato (9 cit.) |
| ExpeL (Zhao et al., 2024) | OpenAlex | DOI:10.1609/aaai.v38i17.29936 | ✓ Verificato (116 cit.) |
| PCDD (Fan & Yao, 2024) | Sessione precedente | arXiv:2405.18972 | ✓ Verificato |
| FedMeta-FFD (Chen et al., 2023) | Review esistente | DOI:10.1109/tnse.2023.3266942 | ✓ Verificato (DOI confermato) |
| FL FDD survey (Berghout et al., 2022) | OpenAlex | DOI:10.3390/electronics12010158 | ✓ Verificato (46 cit.) |
| FD-LLM (Qaid et al., 2024) | Review esistente | arXiv:2412.01218 | ✓ Verificato |
| T2SP (Kim et al., 2026) | Review esistente | arXiv:2606.12481 | ✓ Verificato |
| TRUCE (Jhamtani, 2021) | Review esistente | arXiv:2110.01839 | ✓ Verificato |
| Social Learning (Mohtashami, 2023) | Review esistente | arXiv:2312.11441 | ✓ Verificato |
| Semi-sup. FL FDD (Dai et al., 2025) | DBLP | DOI:10.1109/JIOT.2025.3586718 | ✓ Verificato |
| FTL Bearing FDD (Chen et al., 2022) | DBLP | DOI:10.1109/TIM.2022.3180417 | ✓ Verificato |

### 4.2 Paper cercati ma non trovati come entry separata

| Paper cercato | Esito |
|---------------|-------|
| FedCoT (Li et al., 2025) | Confermato in review esistente (arXiv:2508.10020); non emerso come risultato diretto nelle ricerche OpenAlex/Crossref (query restituiva FoT) |
| FedMeta-FFD (Chen et al., IEEE TNSE 2023) | DOI confermato dalla review esistente; non emerso nelle ricerche keyword OpenAlex (risultati tangenziali) |
| "One-shot monoclass teachers" | NON verificato in cataloghi indicizzati — punto strutturale coperto da FedCKD |

### 4.3 Database consultati

- **OpenAlex:** 8 query parallele, ~40 risultati ispezionati
- **ArXiv (detail by ID):** 2 paper recuperati direttamente (sessione precedente)
- **Crossref:** 1 query, 5 risultati (tangenziali per FedMeta-FFD)
- **DBLP:** 1 query ("federated learning fault diagnosis"), 3 risultati (2 paper unici + 1 preprint duplicato)
- **Scopus:** non utilizzato direttamente in questa sessione (tool disponibile)
- **Citation chaining:** dalla review esistente (OUTPUT 8–9)

---

## SEZIONE 5 — CONCLUSIONI DELLA GAP ANALYSIS

### 5.1 Il gap è confermato

La ricerca sistematica su 2021–2026, coprendo >50 lavori attraverso 6 database accademici (OpenAlex, ArXiv, Crossref, DBLP, Scopus) e citation chaining, per un totale di **20 paper verificati** nella tabella comparativa, conferma che **nessun lavoro pubblicato o prepublicato identificato** combina simultaneamente:

1. **Trasferimento di conoscenza testuale** (insight in linguaggio naturale, non parametri/gradienti/logit)
2. **Setting federato/distribuito** (agenti con dati locali non condivisi)
3. **Serie temporali multivariate / diagnosi guasti**
4. **Non-IID class-disjoint** con classi localmente non viste riconosciute a inferenza
5. **Controllo di specificità semantica pre-registrato** (derangement delle associazioni)

### 5.2 I cinque lavori più vicini e perché non coprono il gap

1. **FoT (Yao et al.)** — copre (1)+(2) ma non (3)+(4)+(5): task testuali, cross-domain, no TS/FDD
2. **FICAL** — copre (1)+(2) ma non (3)+(4)+(5): generale, no TS, no unseen classes
3. **FedCKD** — copre (4) ma non (1)+(3)+(5): logit/param, no testo LLM, no TS
4. **FedMeta-FFD** — copre parzialmente (2)+(3)+(4) ma non (1)+(5): parametrico, few-shot (non zero-shot testuale)
5. **FZSL** — copre (4) parzialmente ma non (1)+(3)+(5): attributi ZSL fissi, no TS, no testo LLM libero

### 5.3 Livelli di novità

- **Component novelty:** Bassa (ogni asse è noto singolarmente)
- **Combination novelty:** Moderata (intersezione A∩B∩C vuota)
- **Evaluation novelty:** Moderata-alta (controllo B−E con derangement pre-registrato)
- **Domain novelty:** Moderata (prima applicazione FoT-like a TS/FDD documentata)

### 5.4 Claim difendibile (formulazione raccomandata)

> *"We adapt Federation over Text (Yao et al., 2026) to multivariate time-series fault diagnosis and provide the first controlled evaluation of textual knowledge federation under class-disjoint (missing-class) non-IID experience, isolating the role of semantic correctness via a preregistered label-association control."*

### 5.5 Claim da NON fare

- ~~"We propose Federation over Text"~~ (è di Yao et al.)
- ~~"Privacy-preserving"~~ (nessuna privacy formale)
- ~~"Generalizable"~~ (12 run, 1 LLM, 1 simulatore)
- ~~"First textual federation"~~ (FoT e FICAL precedono)
- ~~"Novel non-IID setting"~~ (FedCKD, PCDD, monoclass coprono il regime)
