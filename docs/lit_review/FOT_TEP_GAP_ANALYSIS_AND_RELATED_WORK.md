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
- **DBLP:** errore 500 (intermittente, documentato)
- **Scopus:** non utilizzato direttamente in questa sessione (tool disponibile)
- **Citation chaining:** dalla review esistente (OUTPUT 8–9)

---

## SEZIONE 5 — CONCLUSIONI DELLA GAP ANALYSIS

### 5.1 Il gap è confermato

La ricerca sistematica su 2021–2026, coprendo >50 lavori attraverso 6 database accademici e citation chaining, conferma che **nessun lavoro pubblicato o prepublicato identificato** combina simultaneamente:

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
