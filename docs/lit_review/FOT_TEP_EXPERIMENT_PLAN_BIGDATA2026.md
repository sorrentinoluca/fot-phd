# Piano sperimentale pre-submission — FoT–TEP per IEEE BigData 2026 (Rev. 3)
## Supervisor / Area-Chair review: pacchetto di esperimenti pre-specificati per massimizzare l'accettazione

**Companion di** `FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md`.

### Changelog — Rev. 3 (aggiornamento allo stato corrente, 2026-09-09)

Rispetto alla Rev. 2, aggiornamento completo dello stato sperimentale:

1. **Experiment 3 / EXP3_V2 (fresh-run replication) COMPLETATO.** 24 nuovi run fisici (6/classe),
   72 agent-case unseen. Risultati: A=0/72, B=68/72, E=4/72; B−A=+0.9444 [0.8611, 1.0],
   B−E=+0.8889 [0.7778, 0.9861]. Criterio di replica soddisfatto. **Degradazione local-seen in B:**
   19/24 vs A=24/24 (5 errori: Agent 4 su F13-002/003/004/005, Agent 2 su F8-003).
2. **Condition C (centralized pooled ICL) COMPLETATA** come riferimento post-hoc esplorativo sul solo
   held-out di Experiment 1. Risultato: 15/15 correct, 0 astensioni. C−B=+0.139 [0.083, 0.167].
   Intero vantaggio concentrato sui 3 casi F8. Natura: **centralized full-information pooled ICL
   post-hoc exploratory reference**, non benchmark.
3. **Experiment 2 (cross-model, Qwen 27B) AVVIATO.** Protocollo frozen: commit `d9bb95c`, tag
   `phase-b-exp2-qwen-protocol-frozen-001`. Probe: 19/19 PASS, verdetto GO. Full run 540 inferenze
   in corso. Nessun risultato scientifico ancora disponibile.
4. **§2 CENTRAL/POOLED ICL aggiornato** per riflettere che Condition C è stata eseguita come
   riferimento esplorativo, non come benchmark — coerente con la raccomandazione "DO NOT" come
   benchmark ma compatibile con l'esplorazione post-hoc.
5. **Tutti i §§ downstream aggiornati** (verdetto, pacchetti, red team, raccomandazione, starting
   today) per riflettere lo stato corrente.

### Changelog — Rev. 2 (recepisce il parere di Luca, 2026-09-02)

Rispetto alla Rev. 1, quattro correzioni sostanziali + due affinamenti:

1. **Exp 2 ridefinito** come **cross-model replication of frozen textual knowledge** (portabilità),
   non "model-general replication". Distinzione **producer vs consumer** resa esplicita. Preferenza per
   **due** reasoner aggiuntivi.
2. **Fresh prospective physical-run extension promossa** sopra l'ablation degli insight: è la vera
   *replication dimension sul dato* e attacca la vulnerabilità "3 run/guasto".
3. **Insight ablation ridisegnata**: eliminati `pattern-only` e `label-only` come cuore (quasi
   tautologici col label space opaco); sostituiti con *full vs core-semantic vs reduced-library vs
   no-provenance* — condizioni che tengono il task **possibile**. Declassata a "solo se resta tempo".
4. **Communication characterization ridefinita** come *payload characterization* con denominatore
   esplicito (tre quantità separate), mai *efficiency*.
+ **PV nell'abstract**: posizione **conservativa** (abstract = "distributed industrial monitoring";
   PV esplicito solo in Introduction).
+ **Affinamenti**: (a) la fresh extension è *precisione/replica sugli stessi 4 guasti*, non
   generalizzazione di classe; pre-specificare il pooling Exp1+extension. (b) l'ablation redisegnata
   resta *secondaria e a bassa novelty* (si sovrappone alle ablation di FoT), con controllo di
   molteplicità.

### Metadati

- **HEAD corrente:** `5946fb7` (2026-09-02). **Experiment 1 (frozen):** tag `phase-b-results-frozen`
  → `45ec4eed…`. **Resta immutato.**
- **EXP3_V2 (Fase 2):** 24 nuovi run fisici, risultati frozen. **COMPLETATO.**
- **Condition C:** riferimento centralized pooled ICL post-hoc su Exp1 held-out. **COMPLETATO.**
- **Experiment 2 (Qwen 27B):** protocollo frozen `d9bb95c`, tag
  `phase-b-exp2-qwen-protocol-frozen-001`. Full run **IN CORSO**, nessun risultato.
- **Deadline:** 30 settembre 2026 (~3 settimane). **Limite:** 10 pagine IEEE 2-col, ref incluse,
  **niente appendice**.
- **Convenzione:** [FATTO — REPO] · [EVIDENZA — LETTERATURA] · [INTERPRETAZIONE] · [RACCOMANDAZIONE].
- **Terminologia:** *pre-specified / pre-specificato* (nessun registry pubblico), mai *preregistered*.

### Regola invariabile

Experiment 1 (A/B/E, pseudolabel, held-out, bootstrap, criteri, verbalizer V2) **è frozen**. Ogni
aggiunta è un **nuovo esperimento pre-specificato**, separato, congelato **prima** di vederne gli esiti.

---

## 0. VERDETTO ESECUTIVO (Rev. 3)

La storia raccomandata nella Rev. 2 è ora **in gran parte realizzata**:

> **mechanism → semantic specificity → cross-model portability → fresh-run replication →
> communication payload characterization.**

Stato di avanzamento:

1. ✅ **Experiment 1 — Mechanism isolation (frozen).** A=0/36, B=31/36, E=3/36. B−A=+0.861
   [0.833, 0.917]. **Completato e immutato.**
2. ✅ **Experiment 3 / EXP3_V2 — Fresh prospective physical-run extension.** 24 nuovi run fisici
   (6/classe), 72 agent-case unseen. A=0/72, B=68/72, E=4/72; B−A=+0.9444 [0.8611, 1.0].
   **Completato.** Criterio di replica soddisfatto. Segnale di degradazione local-seen (B: 19/24 vs
   A: 24/24) da registrare come osservazione descrittiva.
3. ✅ **Condition C — Centralized pooled ICL post-hoc reference** (solo Exp1 held-out). 15/15 correct.
   C−B=+0.139 [0.083, 0.167]. Vantaggio interamente su 3 casi F8. Riferimento **esplorativo
   descrittivo**, non benchmark — coerente con §2.
4. 🔄 **Experiment 2 — Cross-model replication (Qwen 27B).** Protocollo frozen, probe GO, full run
   540 inferenze **in corso**. Nessun risultato ancora disponibile. Una seconda lane open-weight è
   desiderabile ma non ancora avviata.
5. ⬜ **Communication payload characterization** — da completare (costo ~0).
6. ⬜ **Experiment 4 — Focused insight/library ablation** — **solo se resta tempo**.

**Non** aggiungere: baseline FL parametrica, classificatore FDD come competitor, multi-round FoT,
`pattern-only`/`label-only` ablation, V3 verbalizer, esperimento PV. **PV = motivazione**, non
risultato. Central/pooled ICL **non** come benchmark (Condition C è già stata eseguita come
riferimento esplorativo post-hoc, che è la forma corretta).

Il resto giustifica il verdetto.

---

## 1. STATO ATTUALE (delta — Rev. 3)

### 1.1 Experiment 1 (frozen, immutato)

[FATTO — REPO] 4 agenti (Normal + 1 guasto; 3 unseen ciascuno); A / B / **E = stessi 6 insight,
stesso ordine/volume, solo `pseudolabel` permutata via derangement frozen a zero punti fissi**; R=3;
**12 fault-run fisici indipendenti** → 36 osservazioni agent-case correlate/condizione;
**A=0/36, B=31/36, E=3/36**; **B−A=+0.861** (primario, 4/4 agenti), **B−E=+0.778** (specificità, non
primario); bootstrap cluster-pairato su 12 cluster (CI B−A [0.833,0.917], B−E [0.722,0.833]);
preservazione Normal/seen 100%. Inferenze Exp 1: 15×4×3×R3 = **540** individuali (180 aggregati);
unseen = 108 individuali (36 aggregati)/condizione.

### 1.2 EXP3_V2 — Fresh-run replication (COMPLETATO)

[FATTO — REPO] **24 nuovi run fisici** (6 per ciascuno dei 4 fault) + 6 Normal, generati dal parent
simulator frozen, congelati prima dell'inferenza. Stesso protocollo, stessi insight, stessi agenti di
Exp 1 — cambiano solo i dati fisici. **72 agent-case unseen per condizione.**

| Condizione | Corretti / 72 | Accuratezza | Astensioni |
|---|---|---|---|
| **A** | 0 / 72 | 0.0% | 30 |
| **B** | 68 / 72 | 94.4% | 0 |
| **E** | 4 / 72 | 5.6% | 0 |

| Contrasto | Stima | CI percentile 95% | Note |
|---|---|---|---|
| **B−A** | +0.9444 | [0.8611, 1.0] | Criterio di replica soddisfatto (B−A>0 e CI_inf>0). |
| **B−E** | +0.8889 | [0.7778, 0.9861] | Evidenza supporting per specificità semantica. |

Bootstrap cluster-pairato su **24 cluster**, seed 320031, stratificato per pseudolabel, 10.000 draw.

**Degradazione local-seen (descrittiva):** A=24/24; **B=19/24** (79.2%); E=22/24. Cinque errori
local-seen in B: Agent 4 su F13-002, -003, -004, -005 (4/6); Agent 2 su F8-003 (1/6). Segnale non
visibile in Exp 1 (12/12 in tutte le condizioni). Fenomeno da registrare; non invalida il primary
result unseen ma merita approfondimento nel disegno futuro. Normal: 24/24 in tutte le condizioni.

### 1.3 Condition C — Centralized pooled ICL post-hoc reference (COMPLETATO)

[FATTO — REPO] **Centralized full-information pooled ICL post-hoc exploratory reference**, applicata
esclusivamente al held-out di Experiment 1 (15 casi). Agente unico con tutti gli artefatti
prompt-facing dei 4 agenti (10 esempi pooled + 8 insight). **15/15 correct, 0 astensioni.**

C−B = +0.138889 [0.083333, 0.166667] (bootstrap 10.000 draw, seed 20260906). L'intero vantaggio è
concentrato sui 3 casi F8; per gli altri 9 casi fault il delta è zero. Condition C **non** è stata
applicata a EXP3_V2.

### 1.4 Experiment 2 — Cross-model replication (IN CORSO)

[FATTO — REPO] Consumer open-weight: **Qwen3.8-27B-FP8** via vLLM 0.28.0, 1 GPU (NVIDIA RTX 5000
Ada). Producer invariato (`gpt-5.6-terra`). Protocollo frozen: commit `d9bb95c`, tag
`phase-b-exp2-qwen-protocol-frozen-001`. Capability probe: **19/19 PASS**, verdetto **GO**.
`max_tokens=1536`, `thinking_token_budget=1024`. Full run 540 inferenze **avviato**, nessun
risultato scientifico ancora disponibile.

### 1.5 Cosa è ora dimostrato e cosa resta aperto

Dimostrato: (1) *peer information is useful* (B≫A, confermato su 2 campioni indipendenti);
(2) *conta la correttezza semantica dell'associazione, non il volume* (B≫E, confermato su 2
campioni); (3) l'effetto **si riproduce su nuove realizzazioni fisiche** degli stessi guasti (EXP3_V2);
(4) un riferimento centralizzato post-hoc raggiunge 15/15 ma con delta C−B concentrato su F8
(Condition C).

Resta aperto: (5) **consumo della conoscenza da parte di altri reasoner** — Exp 2 in corso;
(6) generalità su più guasti/simulatori; (7) diagnosi della degradazione local-seen in B;
(8) Condition C non applicata a EXP3_V2.

---

## 2. CENTRAL/POOLED ICL: NON come benchmark — Condition C realizzata come riferimento esplorativo

[INTERPRETAZIONE — aggiornamento Rev. 3.] La raccomandazione della Rev. 2 era "NON aggiungere come
benchmark". Nella pratica, **Condition C è stata realizzata** nella forma raccomandata: un
*information-matched pooled reference* riportato come topline **descrittiva** ("centralized
full-information pooled ICL post-hoc exploratory reference"), non "il metodo da battere".

**Risultato:** C classifica correttamente 15/15 casi del held-out di Experiment 1 (0 astensioni).
C−B = +0.139 [0.083, 0.167]. L'intero delta è concentrato sui 3 casi F8; per gli altri 9 fault
il delta è zero. Condition C **non** è stata applicata a EXP3_V2.

**Interpretazione coerente con §2 originale:** Condition C colloca B rispetto a un contesto
centralizzato più ricco (10 esempi pooled + 8 insight vs 4 locali + 6 peer), ma quantità, forma e
struttura cambiano simultaneamente → il confronto è **descrittivo e non causale**. Non autorizza una
lettura di superiorità generale del centralizzato, specialmente dato che il delta si concentra su
una singola classe. **Resta confermato: NON usare C come benchmark.**

**Limite residuo:** Condition C copre solo il held-out Exp1 (15 casi, 12 cluster). Non è stata
eseguita sulle 24 realizzazioni di EXP3_V2 → la copertura del riferimento centralizzato sui
nuovi dati è un gap della Fase 2.

---

## 3. EXP 2 — COSA DIMOSTRA DAVVERO (producer vs consumer)

[INTERPRETAZIONE — precisazione chiave della Rev. 2.]

Riusando gli insight frozen e cambiando solo il reasoner, l'esperimento **non** è una replica
end-to-end di FoT con un secondo modello, né una prova di "model-generality". Gli insight frozen sono
stati **prodotti** da `gpt-5.6-terra` (il producer); il cross-model varia il **consumer** (il reasoner
che li usa in ICL). Quindi:

- **Claim corretta:** *"The transfer effect and its semantic specificity persist when the same frozen
  peer knowledge is consumed by different reasoning models."* / *"cross-model portability of frozen
  textual knowledge."*
- **Claim vietate:** *"FoT is model-general"* (il producer non è variato); *"independent confirmation
  on new data"* (l'held-out è lo stesso di Exp 1, ormai noto ai ricercatori → è **cross-model
  replication on the frozen benchmark**, non nuova conferma indipendente sui dati — quella è Exp 3).
- **Perché è comunque forte:** dimostra che la conoscenza testuale prodotta da un modello è
  **consumabile da reasoner diversi** — proprietà molto rilevante per FoT, che si aggancia al
  risultato *weak-to-strong in text space* di Yao et al. Con originale + **due** reasoner aggiuntivi:
  *same frozen evidence, same knowledge, same cases → three different reasoning models.*

Per parlare di "model-general" servirebbero ≥3 modelli **e** cautela; con un solo modello aggiuntivo
si dice "replication across a second reasoning model", nulla di più.

---

## 4. FAMIGLIE DI ESPERIMENTI (rivalutate)

Legenda: *rischio ridotto · RQ · contributo · costo · costo statistico · scope-creep · valore pub. ·
raccomandazione.*

**A. Central/pooled equal-information comparator.** → **COMPLETATO come riferimento esplorativo**
(Condition C su Exp1 held-out: 15/15 correct, C−B=+0.139). Vedi §2. **NON** come benchmark.

**B. Cross-model replication (Exp 2).** 🔄 **IN CORSO.** Riduce: la critica quasi-fatale "un solo LLM
proprietario, non deterministico, non riproducibile" (Reviewer B/D). RQ: la conoscenza frozen è
**consumabile** da reasoner diversi? Contr.: **alto**. Prima lane (Qwen 27B): protocollo frozen,
probe GO, full run in corso. Una seconda lane è desiderabile. Claim: portabilità cross-model della
conoscenza testuale (§3), non model-generality.

**C. Fresh prospective physical-run extension (Exp 3).** ✅ **COMPLETATO (EXP3_V2).** 24 nuovi run
fisici (6/classe), 72 agent-case unseen. A=0/72, B=68/72, E=4/72; B−A=+0.9444 [0.8611, 1.0];
B−E=+0.8889 [0.7778, 0.9861]. Criterio di replica soddisfatto. Degradazione local-seen in B
(19/24 vs A=24/24) da registrare.

**D. More TEP fault classes (+agenti).** → **CONDITIONAL / Package C**. Alta generalità di task ma
alto costo/scope; criterio di selezione classi **pre-specificato** obbligatorio.

**E. More agents (senza più guasti).** → **NO** (cosmetico per il meccanismo).

**F. Classical numerical classifier.** → **OPTIONAL come oracle/upper-reference descrittivo**; DO NOT
come competitor (non apples-to-apples col task locally-unseen).

**G. Parameter-based FL baseline.** → **DO NOT** (paradigma diverso). Discutere in Related Work.

**H. No-verbalizer / raw-numeric LLM baseline.** → **OPTIONAL** (difende l'enabling layer; rischia di
spostare il focus sul verbalizer).

**I. Insight / library ablation — RIDISEGNATA (Exp 4).** Riduce: "cosa nel bundle di insight conta?".
RQ **vere e con task possibile** (vedi §7-Exp4): provenance? evidence metadata? 2 insight/classe o 1?
Contr.: medio. Costo: medio (riusa held-out+modello). Costo stat.: molteplicità (contrasti secondari).
Scope-creep: controllabile. Valore pub.: **medio** (bassa novelty: si sovrappone alle ablation di FoT
su library-size). → **HIGH VALUE solo se resta tempo (Package C).** **Eliminati `pattern-only` e
`label-only`**: col label space opaco recidono il ponte pattern↔classe e rendono il fallimento
tautologico; **E è già l'ablation semantica superiore**.

**J. Communication payload characterization.** Riduce: fit Special Session ("communication
constraints") + "perché federare". RQ: caratterizzazione (non efficiency). Costo: **~0**. → **MUST.**
Definizione corretta (Rev. 2): **non** confrontare "6 insight vs un caso raw" (rapporto arbitrario).
Riportare **tre quantità separate**:
1. *textual payload effettivamente trasmesso per ricevente*: byte/char UTF-8 + token count dei 6
   insight;
2. *numero di valori numerici grezzi trattenuti localmente* da cui la conoscenza è derivata (evidenza
   development locale);
3. *rapporto descrittivo* sotto una **serialization definition esplicita** (dichiarare esattamente
   cosa sta al denominatore: es. i valori grezzi che servirebbe trasferire per rendere disponibile la
   stessa esperienza).
Nome: **communication payload characterization**, mai *efficiency* (vietata senza comparatore).

**K. Multi-round FoT.** → **DO NOT** (ambiguità interpretativa; single-shot = scelta di design;
multi-round = future work).

**L. Semantic-corruption variants oltre E.** → **DO NOT** (E isola già bene; al più *una*
"irrelevant-text" se avanza budget, per distinguere info-sbagliata da info-assente).

---

## 5. REVIEWER-RISK REDUCTION MATRIX (Rev. 3) — aggiornata con stato corrente

| Esperimento/azione | Critica neutralizzata | Stato | Riduzione rischio | Priorità |
|---|---|---|---|---|
| **Communication payload characterization (J)** | A: "perché federare / Big Data?" | ⬜ Da fare (~0 costo) | Media | **1 (MUST)** |
| **Framing + terminologia + PV-motivation + delta vs FoT** | A (è FL?), B (novelty) | ⬜ Da fare (~0 costo) | **Alta** | **1 (MUST)** |
| **Fresh physical-run extension (Exp 3, C)** | D: "3 run/guasto, 12 totali"; benchmark noto | ✅ **COMPLETATO** (EXP3_V2) | **Alta → Neutralizzata** | — |
| **Cross-model replication (Exp 2, B)** | B/D: "un solo LLM proprietario, irreproducibile" | 🔄 **IN CORSO** (Qwen 27B) | **Alta** | **2 (MUST)** |
| **Central/pooled ICL (A)** | A: "perché federare?" | ✅ **COMPLETATO** (Condition C, esplorativo) | Media → Parzialm. neutralizzata | — |
| **Insight/library ablation ridisegnata (Exp 4, I)** | B/C: "cosa nel bundle conta?" | ⬜ Solo se resta tempo | Media-Bassa | 4 (HIGH, se tempo) |
| More fault classes (+agenti) (D) | C/D: "solo 4 guasti" | ⬜ Pkg C | Media | 5 (Pkg C) |
| No-verbalizer (H) | C: "il verbalizer fa il lavoro" | ⬜ Opzionale | Bassa-Media | Opzionale |
| Classical FDD (F) | C: "manca baseline FDD" | ⬜ Opzionale | Bassa | Opzionale |
| Parameter-FL (G) / Multi-round (K) | A / B | ❌ DO NOT | Negativa (scope) | **DO NOT** |

[INTERPRETAZIONE — Rev. 3] Due dei tre esperimenti MUST della Rev. 2 sono ora completati o in corso.
La fresh-run extension ha **soddisfatto il criterio di replica**. La critica residua più alta è
"un solo LLM" — il full run Qwen è in corso. Communication payload characterization e framing
restano i MUST a costo zero ancora da completare.

---

## 6. COSA AUMENTARE (Rev. 3) — stato aggiornato

Le due dimensioni principali raccomandate nella Rev. 2 sono state affrontate:

1. ✅ **Più run fisici indipendenti (stessi 4 guasti).** EXP3_V2 completato: da 12 a 36 run fisici
   totali (Exp1 12 + EXP3_V2 24), criterio di replica soddisfatto.
2. 🔄 **Più reasoner (consumer).** Exp 2 in corso con Qwen 27B. Una seconda lane (famiglia diversa)
   è desiderabile se il tempo lo consente.
3. ⬜ **Più classi di guasto.** Allarga la claim ma costoso → Pkg C, non prioritario.
4. ❌ **Più agenti (da soli).** Cosmetico → no.

**Budget residuo (Rev. 3):**
- **Exp 2 Qwen (~540 inf):** in esecuzione.
- **Se resta tempo dopo Exp 2:** una **seconda lane open-weight** (~540 inf) o **Exp 4 ablation
  ridisegnata** su unseen (~108 inf).
- **Communication payload characterization:** ~0 costo, da completare.

---

## 7. DESIGN PRE-SPECIFICATI (Rev. 2)

Congelare ogni protocollo (git tag) **prima** dell'esecuzione e **prima** di osservarne gli esiti.

### Experiment 2 — Cross-model replication of frozen textual knowledge (MUST) — 🔄 IN CORSO

- **RQ:** la conoscenza testuale peer frozen, prodotta dal modello originale, resta utile (B≫A) e
  semanticamente specifica (B≫E) quando **consumata da reasoner diversi**?
- **Claim target (§3):** portabilità cross-model; **non** model-generality end-to-end.
- **Cosa varia:** **solo il consumer LLM.** Restano byte-identici: held-out frozen, esempi locali,
  6 insight peer (B), libreria E (derangement), prompt, pseudolabel, R=3, aggregazione, evaluator.

**Stato corrente (Rev. 3):**
- **Lane 1 — Qwen3.8-27B-FP8** (open-weight, 27B parametri): protocollo frozen nel commit `d9bb95c`,
  tag `phase-b-exp2-qwen-protocol-frozen-001`. Capability probe: **19/19 PASS**, verdetto **GO**.
  `max_tokens=1536`, `thinking_token_budget=1024`. Servito via vLLM 0.28.0, 1× NVIDIA RTX 5000 Ada.
  Full run **540 inferenze avviato**, nessun risultato scientifico ancora disponibile.
- **Lane 2:** desiderabile (famiglia diversa dall'originale), non ancora avviata.

- **Endpoint (per modello, non poolato):** unseen A/B/E, B−A, B−E; per-agente; preservazione.
- **Statistica:** stesso bootstrap cluster-pairato (12 cluster), **seed nuovo pre-dichiarato**.
- **Molteplicità:** ogni modello = replica indipendente pre-dichiarata; riportare tutti i modelli
  eseguiti (niente cherry-pick del migliore).
- **Success:** B−A>0 e B−E>0 con CI(B−A) escludente 0 su ≥1 open-weight, segno concorde ≥3/4 agenti.
- **Failure (riportare comunque):** se su un modello B−A≤0 o B−E≤0 → *model-dependence*, dichiarata
  apertamente (rafforza credibilità).
- **Freeze order:** `exp2-protocol-frozen` (modelli+seed+criteri) → esecuzione → `exp2-inference-frozen`
  → valutazione → `exp2-results-frozen`.

### Experiment 3 / EXP3_V2 — Fresh prospective physical-run extension — ✅ COMPLETATO

- **RQ:** l'effetto (B−A) e la specificità (B−E) si **riproducono su nuove realizzazioni fisiche
  indipendenti** degli stessi 4 guasti?
- **Natura:** **precisione/replica sugli stessi 4 guasti**, NON generalizzazione a nuove classi.
- **Design realizzato:** k=6 run/guasto → **24 nuovi run fisici** + 6 Normal, generati dal parent
  simulator frozen, congelati prima dell'inferenza. Insight/esempi/prompt/condizioni **= Exp 1**.

**Risultati (frozen):**

| Condizione | Corretti / 72 | Accuratezza |
|---|---|---|
| **A** | 0 / 72 | 0.0% |
| **B** | 68 / 72 | 94.4% |
| **E** | 4 / 72 | 5.6% |

| Contrasto | Stima | CI percentile 95% |
|---|---|---|
| **B−A** | +0.9444 | [0.8611, 1.0] |
| **B−E** | +0.8889 | [0.7778, 0.9861] |

Bootstrap cluster-pairato su 24 cluster, seed 320031, 10.000 draw.

- **Success:** ✅ B−A>0 e CI_inf>0 — **criterio di replica soddisfatto.**
- **Degradazione local-seen (descrittiva):** B=19/24 vs A=24/24. 5 errori: Agent 4 (F13) su 4 run,
  Agent 2 (F8) su 1 run. Segnale non visibile in Exp 1. Da registrare come osservazione per il
  disegno futuro.
- **Limite:** Condition C non applicata a EXP3_V2.

### Experiment 4 — Focused insight/library ablation, RIDISEGNATA (HIGH, solo se tempo)

- **RQ:** quali *componenti del bundle* di insight contribuiscono, **mantenendo il task possibile**?
- **Condizioni (tutte con `pseudolabel`+`observed_pattern` intatti → ponte pattern↔classe preservato):**
  - **Full B:** `pseudolabel` + `observed_pattern` + `evidence_scope` + `source_agent` (= Exp 1).
  - **Core-semantic:** solo `pseudolabel` + `observed_pattern` (rimossi scope e source).
  - **No-provenance:** rimosso `source_agent`, tenuti pseudolabel+pattern (+scope) — attesa: effetto
    piccolo ("provenance non necessaria") — nice-to-know, non load-bearing.
  - **Reduced library:** **1 insight/peer** invece di 2 (3 insight invece di 6) — sufficienza/ridondanza;
    aggancio diretto alle ablation library-size di FoT.
- **Endpoint/contrasti (secondari, pre-dichiarati):** B − core-semantic; B − no-provenance;
  B − reduced-library.
- **Perché NON `pattern-only`/`label-only`:** col label space opaco recidono il ponte e il fallimento
  è tautologico; **E** già isola la specificità semantica in modo superiore.
- **Molteplicità:** dichiarare i contrasti come **secondari/esplorativi**; niente claim primarie qui.
- **Freeze order:** `exp4-protocol-frozen` → esecuzione → results.

**Invariante statistico (tutti):** unità = *physical run*; bootstrap clusterizzato; mai trattare le
osservazioni agent-case come indipendenti.

---

## 8. STRUTTURA DEL PAPER (Rev. 2)

- **Experiment 1 — Controlled mechanism isolation (frozen):** A/B/E; B−A primario; **B−E specificità**.
- **Experiment 2 — Cross-model portability:** stessa conoscenza frozen, reasoner diversi.
- **Experiment 3 — Fresh-run replication:** nuove realizzazioni fisiche, protocollo prospettico.
- **(Experiment 4 — Insight/library decomposition:** solo se tempo.)
- **Communication payload characterization:** sottosezione di Results.

Story: **mechanism → semantic specificity → cross-model portability → fresh-run replication →
communication payload.** Più forte del Package B della Rev. 1 perché aggiunge **due dimensioni di
replica** (modello, dato) invece di una decomposizione potenzialmente tautologica.

---

## 9. NOVELTY (invariata nel merito)

La novelty resta **combinazione + evaluation design** (non method novelty). I nuovi esperimenti la
**irrobustiscono**: cross-model portability + fresh-run replication trasformano *"in un setting, con un
modello"* in *"la conoscenza testuale trasferisce informazione discriminativa in modo semanticamente
specifico, portabile tra reasoner e replicabile su nuove realizzazioni fisiche"*. È una tesi
evaluation-side difficile da attaccare e distinta da FoT.

---

## 10. BASELINE ATTESE DALLA LETTERATURA (invariato)

[EVIDENZA] Comparatore standard del filone = **isolated** (≡ A) + eventuale **RAG/retrieval**; FoT
misura anche il **costo di comunicazione** → la nostra *payload characterization* è attesa. FedMeta-FFD
(Chen et al., IEEE TNSE 2023, DOI 10.1109/tnse.2023.3266942) [verificato] è il neighbor FDD diretto
(nuove categorie cross-client, parametrico). Il central-ICL **non** è lo standard del setting. Ref non
verificata "monoclass teachers" (HAL): **non citare** (coperta da FedCKD).

---

## 11. AUDITABILITY COME CONTRIBUTO (invariato)

[RACCOMANDAZIONE] Posizionare come **contributo metodologico secondario**: *"an auditable, fully
pre-specified and frozen evaluation protocol (opaque pseudolabels + freeze chain + ground-truth-blind
inference + semantic-specificity control) for LLM-mediated federated textual knowledge transfer"*.
La combinazione è una pratica **leakage-resistant** poco comune nel filone LLM-agent; forte per il
topic *evaluation/benchmarking* di IEEE BigData. Non chiamarla "novelty" in senso forte.

---

## 12. BIG DATA FIT + PV (Rev. 2)

**Big Data fit:** *distributed sensor analytics across heterogeneous sites* — decentralized ownership,
heterogeneous streams, non-IID local experience, communication constraints (ora concreta via §4-J),
data locality. **Vietato** Volume (TEP piccolo) e Velocity (niente streaming).

**PV — Introduction: SÌ.** Motivazione forte e onesta (il repo definisce PV come target finale e TEP
come proof-of-concept metodologico). Frase raccomandata:
> *"The target application motivating this work is distributed photovoltaic monitoring, where
> physically separated sites accumulate heterogeneous local experience while reliable field fault
> labels can be difficult to obtain. We therefore isolate the knowledge-transfer question first in a
> controlled multivariate process with verifiable fault ground truth."*
Menzionare in forma **generale** multi-site heterogeneity e weak/uncertain labels (giustificano il
design). **Tenere fuori** i numeri del dataset non usato (11 impianti, ~41 var. meteo, inverter-level,
5 min, 4 anni).

**PV — Abstract: posizione conservativa (Rev. 2).** Nell'abstract usare **"distributed industrial
monitoring"** (generale); specificare **PV nell'Introduction**. Motivo: spazio limitato + rischio che
un reviewer pensi *"se il PV motiva, dove sono gli esperimenti PV?"*. Decisione finale quando l'abstract
completo è scritto; la formulazione PV-esplicita resta un'alternativa accettabile ma meno prudente.

**Vietato** [vincoli]: TEP simula il PV; risultati TEP generalizzano al PV; stesse feature al PV;
impianti già usati; dataset PV validato; label PV affidabili.

---

## 13. TRE PACCHETTI (Rev. 3 — stato aggiornato)

### PACKAGE A — Minimum defensible — ⬜ Non ancora completato
Communication payload characterization + framing/terminologia/PV-motivation + delta vs FoT/Federated
In-Context LLM Agent Learning. **0 nuove inferenze.** I componenti a costo zero restano da completare.

### PACKAGE B — Recommended for acceptance — 🔄 In gran parte realizzato
Package A **+ Exp 2 (cross-model) + Exp 3 (fresh-run extension) + Condition C (esplorativo)**.

| Componente | Stato |
|---|---|
| Exp 1 (mechanism isolation) | ✅ Frozen |
| Exp 3 / EXP3_V2 (fresh-run replication) | ✅ Completato — criterio di replica soddisfatto |
| Condition C (centralized pooled ICL) | ✅ Completato — riferimento esplorativo post-hoc |
| Exp 2 lane 1 (Qwen 27B, cross-model) | 🔄 In corso — full run avviato |
| Exp 2 lane 2 (seconda famiglia) | ⬜ Desiderabile, non avviata |
| Communication payload characterization | ⬜ Da completare (~0 costo) |
| Framing + terminologia + PV-motivation | ⬜ Da completare (~0 costo) |

Story: mechanism→specificity→**replication→portability**→centralized-reference→payload. Più forte
del Package B della Rev. 2 perché include anche il riferimento centralizzato. La story dipende
dall'esito di Exp 2: un risultato positivo completa la catena; un risultato negativo richiederebbe
un framing "model-dependent".

### PACKAGE C — Ambitious
Package B **+ Exp 4 (insight/library ablation ridisegnata)** e/o **più classi di guasto** (criterio di
selezione pre-specificato) + eventuale seconda lane Exp 2. Rischio deadline/scope alto.

---

## 14. RACCOMANDAZIONE UNIVOCA (Rev. 3 — aggiornata)

[RACCOMANDAZIONE — "se fossi il supervisor"] **Package B resta la raccomandazione**, ed è ora in
gran parte realizzato. Azioni rimanenti, in ordine di priorità:

1. 🔄 **Completare Exp 2 — full run Qwen 27B** (in corso). Attendere risultati, valutare, congelare.
2. ⬜ **Communication payload characterization** (~0 costo, dagli artefatti frozen).
3. ⬜ **Framing + terminologia + PV-motivation + delta vs FoT** per il paper.
4. *(Solo se resta tempo)* **Seconda lane Exp 2** (famiglia diversa) o **Exp 4 — insight/library
   ablation ridisegnata**.

**Risultati che imporrebbero un cambio di framing (invariati):**
- **Exp 2:** se Qwen dà B−A≤0 o B−E≤0 → la conoscenza non è portabile a quella classe di modelli
  → da *"portabile tra reasoner"* a *"consumabile da questa classe di reasoner"*; riportare apertamente.
- **Communication:** se il payload testuale non è più piccolo dei valori grezzi trattenuti → eliminare
  ogni accenno a compattezza.

**Cosa NON fare:** FL parametrica; FDD classico come competitor; multi-round;
`pattern-only`/`label-only`; V3; esperimento PV; controlli ridondanti oltre E. Central/pooled ICL
come benchmark (Condition C è già stata fatta come riferimento esplorativo, che è la forma corretta).

---

## 15. RESEARCH QUESTIONS FINALI (Rev. 2)

- **RQ1.** Can peer-derived textual knowledge enable agents with class-disjoint temporal experience to
  recognize locally unseen fault conditions? → Exp 1 (B−A).
- **RQ2.** Does the benefit depend on the semantic correctness of the transferred associations rather
  than on text presence/volume? → Exp 1 (B−E).
- **RQ3.** Does the effect persist when the same frozen peer knowledge is **consumed by different
  reasoning models**? → Exp 2 (cross-model portability).
- **RQ4.** Does the effect **reproduce on newly generated independent physical runs** of the same
  faults? → Exp 3 (fresh-run replication).
- *(RQ5, opz. Pkg C: which components of the insight bundle contribute? → Exp 4.)*

---

## 16. CLAIM SET (Rev. 2)

**Package B — Primaria:** *peer textual knowledge transfers discriminative information for locally
unseen faults (B−A), and the benefit is semantically specific (B−E)*. **Secondarie:** *the effect and
its specificity are **portable across reasoning models** consuming the same frozen knowledge* (Exp 2);
*they **replicate on fresh independent physical runs** of the same faults* (Exp 3); *communication is a
compact textual payload of X bytes/tokens per receiver* (descrittiva).

**Vietate in ogni package** (salvo nuova evidenza diretta): *privacy-preserving · generalizable ·
robust · scalable · communication-efficient (superiorità) · superior to FL · superior to centralized ·
model-general end-to-end · cross-domain (PV)*.

---

## 17. RED TEAM FINALE (Rev. 3 — rivalutata con evidenza corrente)

- **Reviewer A (FL).** Residuo: *"è ICL transfer, non FL; 4 client."* → non risolvibile con esperimenti
  senza snaturare il lavoro; terminologia + linea FedMD→FedProto→FoT + fit collaborative/non-IID.
  **Moderate** (invariato).
- **Reviewer B (LLM/FoT).** Residuo: *"delta vs FoT ancora di grado."* → dopo EXP3_V2 (replica su
  nuove realizzazioni) e Condition C (riferimento centralizzato), il delta è più forte; se Exp 2
  conferma la portabilità cross-model, il lavoro si aggancia a weak-to-strong. Resta giudizio di grado.
  **Moderate → moderate-minor** (condizionato a Exp 2).
- **Reviewer C (TS/FDD).** Residuo: *"solo 4 guasti, un simulatore; niente baseline FDD."* →
  parzialmente aperto. EXP3_V2 attenua "un solo held-out" (36 run totali tra Exp1+EXP3_V2).
  Condition C fornisce un riferimento centralizzato. **Moderate** (invariato).
- **Reviewer D (stat).** Residuo: *"le nuove run vengono dallo stesso simulatore/mode."* →
  vero limite di dominio, da dichiarare. L'indipendenza dei run nuovi è garantita dal freeze
  prospettico. EXP3_V2 ha **soddisfatto il criterio di replica pre-specificato**. La degradazione
  local-seen (19/24) è un segnale da riportare trasparentemente. **Moderate → minor.**
- **Nuovo segnale: degradazione local-seen.** 5 errori local-seen in B (EXP3_V2), concentrati su
  Agent 4/F13 e Agent 2/F8. Potenziale critica: *"gli insight peer interferiscono col riconoscimento
  dei fault già noti"*. Mitigazione: (a) è un endpoint secondario descrittivo; (b) il primary result
  unseen non è invalidato; (c) va riportato trasparentemente come osservazione per il disegno futuro.
  **Minor** (se riportato onestamente; **moderate** se omesso e scoperto dal reviewer).

**Conclusione (Rev. 3):** con EXP3_V2 completato e Condition C eseguita, **nessuna critica fatale**.
La critica residua più alta — "un solo LLM" — dipende dall'esito di Exp 2 (in corso). La
degradazione local-seen è un segnale da riportare apertamente, non da nascondere. La scala statistica
è ora affrontata (36 run totali, criterio di replica soddisfatto).

---

## 18. TABELLA DELLE DECISIONI (Rev. 3)

| Decision | Recommendation | Stato | Motivazione |
|---|---|---|---|
| Keep frozen Experiment 1? | **YES** | ✅ | Mechanism-isolation; cuore del paper. |
| Add central/pooled ICL? | **Fatto** (esplorativo) | ✅ | Condition C come riferimento post-hoc, non benchmark. |
| Add second/third LLM (cross-model)? | **YES** | 🔄 | Qwen 27B in corso; seconda lane desiderabile. |
| Add fresh physical-run extension? | **YES** | ✅ | EXP3_V2: criterio di replica soddisfatto. |
| Add more TEP runs (within Exp 3)? | **YES** | ✅ | k=6 run/guasto, 24 nuovi run completati. |
| Add more fault classes? | **CONDITIONAL** | ⬜ | Alta generalità ma alto costo/scope → solo Pkg C. |
| Add more agents? | **NO** (da soli) | ❌ | Cosmetico per il meccanismo. |
| Add classical FDD baseline? | **CONDITIONAL** | ⬜ | Solo oracle/upper-reference descrittivo. |
| Add parameter-FL baseline? | **NO** | ❌ | Paradigma diverso. |
| Add communication analysis? | **YES** | ⬜ | Payload characterization; ~0 costo, da fare. |
| Add verbalizer ablation? | **CONDITIONAL** | ⬜ | Opzionale. |
| Add insight `pattern-only`/`label-only`? | **NO** | ❌ | Tautologico col label space opaco. |
| Add insight full/core/reduced-library ablation? | **CONDITIONAL** | ⬜ | Solo se tempo. |
| Add multi-round FoT? | **NO** | ❌ | Future work. |
| Mention PV in Introduction? | **YES** | ⬜ | Motivazione forte e onesta. |
| Mention PV in Abstract? | **CONDITIONAL → lean NO** | ⬜ | "distributed industrial monitoring". |
| Develop V3 verbalizer now? | **NO** | ❌ | Non necessario. |
| Run PV experiment before submission? | **NO** | ❌ | Fuori scope. |

---

## 19. COSA RESTA DA FARE (Rev. 3 — aggiornamento 2026-09-09)

### Completato

1. ✅ **Experiment 1** — frozen e immutato (`45ec4ee`).
2. ✅ **Experiment 3 / EXP3_V2** — 24 nuovi run fisici, risultati frozen, criterio di replica
   soddisfatto. B−A=+0.9444 [0.8611, 1.0].
3. ✅ **Condition C** — riferimento centralizzato post-hoc su Exp1 held-out. 15/15 correct.

### In corso

4. 🔄 **Experiment 2 — Qwen 27B full run** (540 inferenze). Attendere completamento → freeze →
   evaluation offline → risultati. **Questa è la priorità corrente.**

### Da fare (~3 settimane alla deadline)

5. ⬜ **Communication payload characterization** — costo ~0, dagli artefatti frozen.
6. ⬜ **Framing + terminologia + PV-motivation + delta vs FoT** — per il paper.
7. ⬜ **Scrittura del paper** (10 pagine IEEE 2-col).
8. *(Solo se resta tempo dopo 4–7)* **Seconda lane Exp 2** (famiglia diversa) o **Exp 4 — ablation**.

### Risultati che imporrebbero un cambio di framing

- **Exp 2:** se Qwen dà B−A≤0 o B−E≤0 → la conoscenza non è portabile a quella classe di modelli
  → da *"portabile tra reasoner"* a *"consumabile da questa classe di reasoner"*; riportare apertamente.
- **Communication:** se il payload testuale non è più piccolo dei valori grezzi trattenuti → eliminare
  ogni accenno a compattezza.

### Osservazioni da gestire nel paper

- **Degradazione local-seen in B (EXP3_V2):** 19/24 vs A=24/24. Da riportare trasparentemente come
  segnale descrittivo; non invalida il primary result unseen; merita approfondimento nel disegno futuro.
- **Condition C solo su Exp1:** gap della Fase 2 (non applicata a EXP3_V2), da dichiarare.

**Principio guida (invariato):** ogni aggiunta ha una funzione precisa. Experiment 1 resta **frozen**.

---

*Rev. 3 — aggiornamento allo stato corrente (2026-09-09). Experiment 1 immutato (`45ec4ee`).
EXP3_V2 completato (criterio di replica soddisfatto). Condition C completata (riferimento post-hoc
esplorativo). Exp 2 Qwen in corso (protocollo frozen `d9bb95c`). ~3 settimane alla deadline.*
