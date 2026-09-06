# Piano sperimentale pre-submission — FoT–TEP per IEEE BigData 2026 (Rev. 2)
## Supervisor / Area-Chair review: pacchetto di esperimenti pre-specificati per massimizzare l'accettazione

**Companion di** `FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md`.

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
- **Deadline:** 30 settembre 2026 (~4 settimane). **Limite:** 10 pagine IEEE 2-col, ref incluse,
  **niente appendice**.
- **Convenzione:** [FATTO — REPO] · [EVIDENZA — LETTERATURA] · [INTERPRETAZIONE] · [RACCOMANDAZIONE].
- **Terminologia:** *pre-specified / pre-specificato* (nessun registry pubblico), mai *preregistered*.

### Regola invariabile

Experiment 1 (A/B/E, pseudolabel, held-out, bootstrap, criteri, verbalizer V2) **è frozen**. Ogni
aggiunta è un **nuovo esperimento pre-specificato**, separato, congelato **prima** di vederne gli esiti.

---

## 0. VERDETTO ESECUTIVO (Rev. 2)

Il pacchetto raccomandato racconta una storia ordinata e difficile da attaccare:

> **mechanism → semantic specificity → cross-model portability → fresh-run replication →
> communication payload characterization.**

Azioni, in ordine di esecuzione:

1. **Communication payload characterization** (costo ~0, dagli artefatti frozen) — vedi §4-J per la
   definizione corretta del denominatore.
2. **Experiment 2 — Cross-model replication of frozen textual knowledge** (~540 inf/modello; **due**
   reasoner aggiuntivi se fattibile). Consuma gli insight frozen con reasoner diversi. Risolve la
   critica quasi-fatale "un solo LLM proprietario, non deterministico, non riproducibile" — l'open-weight
   è anche l'ancora di riproducibilità.
3. **Experiment 3 — Fresh prospective physical-run extension** (~540–700 inf) — nuovi run indipendenti
   degli **stessi 4 guasti**, generati dopo il freeze del protocollo. Attacca "n=12 run".
4. **Experiment 4 — Focused insight/library ablation** (ridisegnata) — **solo se resta tempo**.

**Non** aggiungere: central/pooled ICL come benchmark, baseline FL parametrica, classificatore FDD come
competitor, multi-round FoT, `pattern-only`/`label-only` ablation, V3 verbalizer, esperimento PV.
**PV = motivazione**, non risultato.

Il resto giustifica il verdetto.

---

## 1. STATO ATTUALE (delta)

[FATTO — REPO] 4 agenti (Normal + 1 guasto; 3 unseen ciascuno); A / B / **E = stessi 6 insight,
stesso ordine/volume, solo `pseudolabel` permutata via derangement frozen a zero punti fissi**; R=3;
**12 fault-run fisici indipendenti** → 36 osservazioni agent-case correlate/condizione;
**A=0/36, B=31/36, E=3/36**; **B−A=+0.861** (primario, 4/4 agenti), **B−E=+0.778** (specificità, non
primario); bootstrap cluster-pairato su 12 cluster (CI B−A [0.833,0.917], B−E [0.722,0.833]);
preservazione Normal/seen 100%. Inferenze Exp 1: 15×4×3×R3 = **540** individuali (180 aggregati);
unseen = 108 individuali (36 aggregati)/condizione.

Cosa Exp 1 dimostra: (1) *peer information is useful* (B≫A); (2) *conta la correttezza semantica
dell'associazione, non il volume* (B≫E). Cosa non tocca: (3) valore della distribuzione; (4) FoT vs
central; (5) **consumo della conoscenza da parte di altri reasoner**; (6) generalità su più run/guasti.

---

## 2. CENTRAL/POOLED ICL: confermato NON necessario (§5 originale — invariato)

[INTERPRETAZIONE — punto già condiviso con l'autore.] La baseline central/pooled ICL testa (3)/(4):
*la distribuzione batte il centralizzare la stessa informazione?* Il paper **non deve** sostenerlo.
Inoltre il comparatore standard del filone (FoT stesso) è **isolated** (≡ A), non un central-ICL; e
costruire un vero *equal-information* central è concettualmente scomodo (un central con tutti gli 8
insight ha un information set diverso da ogni agente B, che ne riceve 6 peer-only). **Verdetto: NON
aggiungere**, salvo cambiare volontariamente la RQ. Se proprio lo si volesse, l'unica forma difendibile
è un *information-matched pooled reference* riportato come topline **descrittiva** (non "il metodo da
battere"), confrontando copertura di **sistema** (pooled-8 vs unione dei 4 agenti B), mai a livello di
singolo agente.

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

**A. Central/pooled equal-information comparator.** → **DO NOT** (come benchmark). Vedi §2.

**B. Cross-model replication (Exp 2).** Riduce: la critica quasi-fatale "un solo LLM proprietario,
non deterministico, non riproducibile" (Reviewer B/D). RQ: la conoscenza frozen è **consumabile** da
reasoner diversi? Contr.: **alto**. Costo: medio (~540/modello, riusa tutto). Costo stat.: basso
(replica per-modello, **niente pooling tra modelli**). Scope-creep: basso. Valore pub.: **alto**.
→ **MUST.** Claim: portabilità cross-model della conoscenza testuale (§3), non model-generality.

**C. Fresh prospective physical-run extension (Exp 3).** Riduce: "solo 3 run/guasto, 12 totali"
(Reviewer D) e "avete forse adattato all'held-out noto" (validità del benchmark). RQ: l'effetto si
**riproduce su nuove realizzazioni fisiche** degli stessi guasti? Contr.: **alto** (vera replica sul
dato). Costo: medio-alto (nuova simulazione + verbalizzazione + freeze; ma parent simulator già
disponibile). Costo stat.: **più cluster, stesso endpoint** (nessuna nuova famiglia di ipotesi).
Scope-creep: basso. Valore pub.: **alto**. → **MUST/HIGH.** *Precisione/replica, non generalizzazione
di classe.*

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

## 5. REVIEWER-RISK REDUCTION MATRIX (Rev. 2) — per riduzione-rischio / costo

| Esperimento/azione | Critica neutralizzata | Guadagno | Costo | Riduzione rischio | Priorità |
|---|---|---|---|---|---|
| **Communication payload characterization (J)** | A: "perché federare / Big Data?" | Fit sessione + payload dichiarato | **~0** | Media | **1 (MUST)** |
| **Framing + terminologia + PV-motivation + delta vs FoT** | A (è FL?), B (novelty) | Rimuove claim fatali | ~0 | **Alta** | **1 (MUST)** |
| **Cross-model replication (Exp 2, B)** | B/D: "un solo LLM proprietario, irreproducibile" | Portabilità cross-model + riproducibilità (open-weight) | Medio (~540/mod.) | **Alta** | **2 (MUST)** |
| **Fresh physical-run extension (Exp 3, C)** | D: "3 run/guasto, 12 totali"; benchmark noto | Replica prospettica sul dato | Medio-Alto | **Alta** | **3 (MUST/HIGH)** |
| **Insight/library ablation ridisegnata (Exp 4, I)** | B/C: "cosa nel bundle conta?" | Decomposizione secondaria | Medio | Media-Bassa | 4 (HIGH, se tempo) |
| More fault classes (+agenti) (D) | C/D: "solo 4 guasti" | Generalità di task | Alto | Media | 5 (Pkg C) |
| Central/pooled ICL (A) | A: "perché federare?" | testa (3)/(4) non necessari | Basso comp./Alto scope | **Bassa** | DO NOT (benchmark) |
| No-verbalizer (H) | C: "il verbalizer fa il lavoro" | difende enabling layer | Medio | Bassa-Media | Opzionale |
| Classical FDD (F) | C: "manca baseline FDD" | oracle descrittivo | Basso-Medio | Bassa | Opzionale (oracle) |
| Parameter-FL (G) / Multi-round (K) | A / B | problema diverso / ambiguo | Alto | Negativa (scope) | **DO NOT** |

[INTERPRETAZIONE] Le prime **quattro** righe sono il pacchetto raccomandato. Cross-model e fresh-runs
hanno **entrambe** alta riduzione-rischio; l'ordine (2 poi 3) è dettato dal fatto che l'open-weight
copre anche la riproducibilità, la critica più dannosa reputazionalmente.

---

## 6. COSA AUMENTARE (Rev. 2) — ranking con numeri

1. **Più reasoner (consumer).** Massima riduzione-rischio/costo: riusa tutto, cambia solo il modello;
   copre single-model **e** riproducibilità. 2 modelli aggiuntivi (open-weight + famiglia diversa).
2. **Più run fisici indipendenti (stessi 4 guasti).** Attacca "n=12"; replica prospettica sul dato;
   nessuna nuova famiglia di ipotesi (solo più cluster).
3. **Più classi di guasto.** Allarga la claim ma costoso (nuovi agenti/insight/generazione) → Pkg C.
4. **Più agenti (da soli).** Cosmetico → no.

**Budget concreti:**
- **+100–200 inf:** non bastano per un modello full (≈540) né per una runs-extension. Investire in
  una **irrelevant-text control** o in **1 variante di ablation ridisegnata** sul solo unseen
  (~108 inf). Marginale rispetto ai MUST.
- **+500–1000 inf:** **Exp 2 con un modello open-weight** (~540). Con la coda, iniziare la
  progettazione di Exp 3.
- **+1500–2500 inf (raccomandato se c'è tempo):** **Exp 2 con due modelli** (~1080) **+ Exp 3**
  fresh-runs (~540–700). È il pacchetto B della Rev. 2.

---

## 7. DESIGN PRE-SPECIFICATI (Rev. 2)

Congelare ogni protocollo (git tag) **prima** dell'esecuzione e **prima** di osservarne gli esiti.

### Experiment 2 — Cross-model replication of frozen textual knowledge (MUST)

- **RQ:** la conoscenza testuale peer frozen, prodotta dal modello originale, resta utile (B≫A) e
  semanticamente specifica (B≫E) quando **consumata da reasoner diversi**?
- **Claim target (§3):** portabilità cross-model; **non** model-generality end-to-end.
- **Cosa varia:** **solo il consumer LLM.** Restano byte-identici: held-out frozen, esempi locali,
  6 insight peer (B), libreria E (derangement), prompt, pseudolabel, R=3, aggregazione, evaluator.
- **Modelli:** ≥1 **open-weight** (ancora di riproducibilità; determinismo con temperature=0/seed
  dove supportato) + idealmente 1 di **famiglia diversa** dall'originale. Scelta **a priori**, mai
  dopo aver visto i risultati.
- **Endpoint (per modello, non poolato):** unseen A/B/E, B−A, B−E; per-agente; preservazione.
- **Statistica:** stesso bootstrap cluster-pairato (12 cluster), **seed nuovo pre-dichiarato**.
- **Molteplicità:** ogni modello = replica indipendente pre-dichiarata; riportare tutti i modelli
  eseguiti (niente cherry-pick del migliore).
- **Success:** B−A>0 e B−E>0 con CI(B−A) escludente 0 su ≥1 open-weight, segno concorde ≥3/4 agenti.
- **Failure (riportare comunque):** se su un modello B−A≤0 o B−E≤0 → *model-dependence*, dichiarata
  apertamente (rafforza credibilità).
- **Freeze order:** `exp2-protocol-frozen` (modelli+seed+criteri) → esecuzione → `exp2-inference-frozen`
  → valutazione → `exp2-results-frozen`.

### Experiment 3 — Fresh prospective physical-run extension (MUST/HIGH)

- **RQ:** l'effetto (B−A) e la specificità (B−E) si **riproducono su nuove realizzazioni fisiche
  indipendenti** degli stessi 4 guasti?
- **Natura:** **precisione/replica sugli stessi 4 guasti**, NON generalizzazione a nuove classi (da
  dichiarare esplicitamente per non fuorviare il reviewer).
- **Design:** +k run/guasto (consiglio **k=5–7** → **20–28 nuovi run fisici**) + Normal proporzionale,
  generati dal **parent simulator frozen** (S-function byte-identica), **congelati prima** di ogni
  verbalizzazione (nuovo held-out extension set, tag dedicato). Insight/esempi/prompt/condizioni **=
  Exp 1** (la conoscenza resta frozen: si testa se la *stessa* conoscenza regge su dati nuovi).
- **Da congelare prima di simulare:** RNG, simulatore, generation script, **selezione guasti** (gli
  stessi 4), **numero di run k**, timing di iniezione, preprocessing, verbalizer, condizioni,
  endpoint, regola di aggregazione, bootstrap. **Non fermarsi** quando "sembra buono".
- **Unità di indipendenza:** il nuovo *physical run*; bootstrap clusterizzato sui nuovi cluster.
- **Analisi:** **prima separata** (extension come confermativo primario), **poi** pooled Exp1+extension
  come **secondario descrittivo** — *entrambe pre-specificate* (per non scegliere a posteriori la
  presentazione).
- **Success:** B−A>0 e B−E>0 sull'extension, CI(B−A) escludente 0.
- **Failure (riportare):** effetto non replicato → limite forte, da dichiarare.
- **Freeze order:** `exp3-heldout-frozen` → inference → `exp3-results-frozen`.
- **Costo:** unseen = (20–28 run × 3 agenti unseen) × 3 condizioni × R3 ≈ **540–756** individuali,
  + seen/Normal per preservazione. **Path critico** (simulazione MATLAB): iniziare subito.

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

## 13. TRE PACCHETTI (Rev. 2)

### PACKAGE A — Minimum defensible
Communication payload characterization + framing/terminologia/PV-motivation + delta vs FoT/Federated
In-Context LLM Agent Learning. **0 nuove inferenze.** Rimuove i rischi *fatali* (privacy/generalizzazione;
"we propose FoT"; "è FL?"). Resta esposto a "un solo LLM" e "n=12".

### PACKAGE B — Recommended for acceptance
Package A **+ Exp 2 (cross-model, 2 reasoner) + Exp 3 (fresh-run extension)**. ~1080 (Exp2) + ~540–700
(Exp3) ≈ **1600–1800 inf**. Story completa mechanism→specificity→portability→replication→payload.
Neutralizza B/D (single-model, riproducibilità) e D (n=12/benchmark noto). Nuove claim: *portabilità
cross-model* + *replica su nuove realizzazioni fisiche*.

### PACKAGE C — Ambitious
Package B **+ Exp 4 (insight/library ablation ridisegnata)** e/o **più classi di guasto** (criterio di
selezione pre-specificato) + eventuale terzo reasoner. +~300–1500 inf. Rischio deadline/scope alto.

---

## 14. RACCOMANDAZIONE UNIVOCA (Rev. 2)

[RACCOMANDAZIONE — "se fossi il supervisor"] **Package B**, in questo ordine:

1. **Communication payload characterization** (oggi, ~0).
2. **Exp 2 — cross-model replication** su **due** reasoner (open-weight + famiglia diversa), protocollo
   congelato prima; consuma insight frozen; risultati per-modello.
3. **Exp 3 — fresh prospective physical-run extension** (k=5–7 run/guasto sugli stessi 4 guasti),
   protocollo e generazione congelati prima; analisi separata poi pooled.
4. *(Solo se resta tempo)* **Exp 4 — insight/library ablation ridisegnata** (full vs core-semantic vs
   reduced-library vs no-provenance).

**Path critico:** avviare **subito** la generazione dei nuovi run TEP (simulazione MATLAB = collo di
bottiglia), in parallelo all'integrazione dei reasoner.

**Cosa NON fare:** central/pooled ICL come benchmark; FL parametrica; FDD classico come competitor;
multi-round; `pattern-only`/`label-only`; V3; esperimento PV; controlli ridondanti oltre E.

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

## 17. RED TEAM FINALE (dopo Package B)

- **Reviewer A (FL).** Residuo: *"è ICL transfer, non FL; 4 client."* → non risolvibile con esperimenti
  senza snaturare il lavoro; terminologia + linea FedMD→FedProto→FoT + fit collaborative/non-IID.
  **Moderate.**
- **Reviewer B (LLM/FoT).** Residuo: *"delta vs FoT ancora di grado."* → dopo Exp 2 (portabilità
  cross-model, agganciata a weak-to-strong) + fresh-run, il delta è più forte; resta giudizio di grado.
  **Moderate.**
- **Reviewer C (TS/FDD).** Residuo: *"solo 4 guasti, un simulatore; niente baseline FDD."* → parzialmente
  aperto (chiuso in Pkg C con più classi). Fresh-run attenua "un solo held-out". **Moderate.**
- **Reviewer D (stat).** Residuo dopo Exp 3: *"le nuove run vengono dallo stesso simulatore/mode."* →
  vero limite di dominio (non di indipendenza statistica), da dichiarare; l'indipendenza dei run nuovi è
  garantita dal freeze prospettico. **Moderate → minor.**

**Conclusione:** dopo Package B **nessuna critica fatale**; restano *moderate* di grado (novelty
incrementale; dominio singolo). La scala statistica — la più citabile — è ora **attivamente
affrontata** da Exp 3.

---

## 18. TABELLA DELLE DECISIONI (Rev. 2)

| Decision | Recommendation | Motivazione |
|---|---|---|
| Keep frozen Experiment 1? | **YES** | Mechanism-isolation; cuore del paper. |
| Add central/pooled ICL? | **NO** (benchmark) | Testa (3)/(4) non necessari; scope-creep + ottica auto-lesiva. |
| Add second/third LLM (cross-model)? | **YES** | Neutralizza "un solo LLM proprietario"; portabilità + riproducibilità (open-weight). |
| Add fresh physical-run extension? | **YES** | Vera replica prospettica sul dato; attacca "n=12". |
| Add more TEP runs (within Exp 3)? | **YES** | È esattamente Exp 3: k=5–7 run/guasto, freeze prospettico. |
| Add more fault classes? | **CONDITIONAL** | Alta generalità ma alto costo/scope → solo Pkg C, criterio pre-specificato. |
| Add more agents? | **NO** (da soli) | Cosmetico per il meccanismo. |
| Add classical FDD baseline? | **CONDITIONAL** | Solo oracle/upper-reference descrittivo; non apples-to-apples. |
| Add parameter-FL baseline? | **NO** | Paradigma diverso. |
| Add communication analysis? | **YES** | Payload characterization (3 quantità), non efficiency; ~0 costo. |
| Add verbalizer ablation? | **CONDITIONAL** | No-verbalizer difende l'enabling layer; opzionale. |
| Add insight `pattern-only`/`label-only`? | **NO** | Tautologico col label space opaco; E è superiore. |
| Add insight full/core/reduced-library ablation? | **CONDITIONAL** | Task possibile, ma bassa novelty → solo se tempo. |
| Add multi-round FoT? | **NO** | Ambiguità interpretativa; future work. |
| Mention PV in Introduction? | **YES** | Motivazione forte e onesta; giustifica il design. |
| Mention PV in Abstract? | **CONDITIONAL → lean NO** | Abstract = "distributed industrial monitoring"; PV in Intro; evita "dove sono i risultati PV?". |
| Develop V3 verbalizer now? | **NO** | Coperto da T2SP/TRUCE; non necessario. |
| Run PV experiment before submission? | **NO** | Fuori scope; dataset non pronto, label inaffidabili. |

---

## 19. STARTING TODAY — COSA IMPLEMENTARE PER PRIMO (Rev. 2)

1. **Oggi (parallelo, path critico):** avviare la **generazione dei nuovi run TEP** per Exp 3
   (simulazione MATLAB dei 4 guasti, k=5–7/guasto) dopo aver scritto e **congelato**
   `exp3-heldout-frozen` (RNG, script, selezione guasti, k, timing, preprocessing). È il collo di
   bottiglia temporale.
2. **In parallelo:** **Communication payload characterization** dagli artefatti frozen (byte/token dei
   6 insight per ricevente; conteggio valori grezzi locali; rapporto sotto serialization esplicita).
3. **Poi:** **Exp 2 — cross-model replication** su due reasoner (integrazione modelli nel runner
   esistente; riuso di held-out/insight/prompt/evaluator; `exp2-protocol-frozen` prima dell'esecuzione).
4. **Solo se resta tempo:** **Exp 4 — insight/library ablation ridisegnata**.

**Cosa congelare prima di eseguire (ogni esperimento):** protocollo+ipotesi+endpoint+criteri+seed
(+ per Exp 3 anche simulatore/RNG/script/k/selezione guasti) → *(freeze)* → esecuzione → predictions →
*(freeze)* → evaluation offline → *(freeze)*. Riusare evaluator e bootstrap di Exp 1 **senza
modificarli**. Nessuna scelta (modelli, k, classi) dopo aver visto gli esiti.

**Risultati che imporrebbero un cambio di framing:**
- **Exp 2:** se un reasoner dà B−A≤0 o B−E≤0 → la conoscenza non è portabile a quella classe di modelli
  → da *"portabile tra reasoner"* a *"consumabile da questa classe di reasoner"*; riportare apertamente.
- **Exp 3:** se l'effetto non replica sulle nuove run → limite forte sulla robustezza dell'evidenza →
  ridimensionare la claim primaria a *"osservato sull'held-out originale, non replicato su nuove run"*.
- **Communication:** se il payload testuale non è più piccolo dei valori grezzi trattenuti → eliminare
  ogni accenno a compattezza.

**Principio guida (invariato):** ogni aggiunta ha una funzione precisa — Exp 2 uccide "single-model" e
la riproducibilità, Exp 3 attacca "n=12" con una replica prospettica, communication serve il fit di
sessione. Nessun esperimento "perché di più è meglio". Experiment 1 resta **frozen**.

---

*Rev. 2 — recepisce il parere dell'autore (2026-09-02). Experiment 1 immutato (`45ec4ee`). Ogni nuovo
esperimento è pre-specificato e congelato prima dell'esecuzione. Non avviare Exp 2 prima del freeze dei
protocolli; il path critico è la generazione dei nuovi run TEP per Exp 3.*
