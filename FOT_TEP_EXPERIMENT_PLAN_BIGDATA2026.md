# Piano sperimentale pre-submission — FoT–TEP per IEEE BigData 2026
## Supervisor / Area-Chair review: quale pacchetto minimo di esperimenti aggiuntivi massimizza la probabilità di accettazione

**Companion di** `FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md`. Questo documento **non** ripete la
literature review: la usa come base e risponde alla domanda nuova —
> *dato il lavoro già completato (Experiment 1, frozen) e il tempo ancora disponibile, quale pacchetto
> minimo ma ad alto impatto di nuovi esperimenti **pre-specificati** riduce di più i rischi reviewer?*

### Metadati

- **HEAD corrente:** `5946fb7` (2026-09-02 19:11 CET, "commit cartella papers folder").
- **Experiment 1 (frozen):** tag `phase-b-results-frozen` → `45ec4eed…`. **Resta immutato.**
- **Data della review:** 2026-09-02. **Deadline:** 30 settembre 2026. **Limite:** 10 pagine IEEE
  2-col, referenze incluse, **niente appendice**.
- **Convenzione:** [FATTO — REPO] · [EVIDENZA — LETTERATURA] · [INTERPRETAZIONE] · [RACCOMANDAZIONE].

### Nota terminologica (applicata)

Nel paper e in questi documenti si usa **pre-specified / pre-specificato** (protocollo fissato prima
dell'esecuzione), **non** *preregistered*: non esiste registrazione in un registry pubblico. Gli
artefatti frozen di Experiment 1 usano internamente la parola "preregistered": **non vanno
modificati** (sono frozen); nel *paper* la si rende come *pre-specified*. La review companion è già
stata corretta (12 occorrenze → *pre-specificato/pre-specified*).

### Regola invariabile

Experiment 1 (A/B/E, pseudolabel, held-out, bootstrap, criteri, verbalizer V2) **è frozen**. Ogni
aggiunta è un **nuovo esperimento pre-specificato**, chiaramente separato, con protocollo congelato
**prima** di vederne gli esiti.

---

## 0. VERDETTO ESECUTIVO (la raccomandazione, in testa)

[INTERPRETAZIONE — sintesi] La conclusione precedente ("il central/pooled ICL è il principale
esperimento da aggiungere") **va corretta**. Rivista da zero (§2), quella baseline risponde a una
domanda — *"la federazione distribuita vale più dell'accesso centralizzato alla stessa
informazione?"* — che **questo paper non deve porsi**. Introdurla come benchmark rischia scope-creep
e un'ottica auto-lesiva ("allora perché federare?").

**Il pacchetto che massimizza l'accettazione non è "una baseline in più": è trasformare Experiment 1
da _un modello, un controllo_ in _un'evidenza model-generale e meccanicisticamente decomposta_,
mantenendo il focus.** Tre azioni, in ordine:

1. **Communication characterization** (costo ~0, dagli artefatti esistenti) — misura byte/token degli
   insight vs serie grezza; supporta il fit con la Special Session.
2. **Experiment 2 — Second-LLM replication** (≈540 inferenze) — ripete A/B/E sullo **stesso held-out
   frozen, stessi insight, stessi prompt**, cambiando **solo il modello** (idealmente un open-weight +
   un secondo di famiglia diversa). Neutralizza la critica più pericolosa ("un solo LLM proprietario,
   non riproducibile").
3. **Experiment 3 — Insight-content ablation** (≈324 inferenze) — decompone *cosa* nel testo porta il
   segnale (label-only, pattern-only, fewer-insights). Rafforza il contributo **di valutazione**, che
   è la vera novelty.

**Non** aggiungere (ora): central/pooled ICL come benchmark, baseline FL parametrica, classificatore
FDD come competitor, multi-round FoT, nuove classi di guasto (a meno del Package C), V3 verbalizer,
esperimento PV. **PV = solo motivazione**, non risultato.

Il resto del documento giustifica questo verdetto punto per punto.

---

## 1. STATO ATTUALE (delta, non ripetizione)

[FATTO — REPO, verificato in Experiment 1] 4 agenti (Normal + 1 guasto ciascuno; 3 guasti unseen
per agente); A isolated / B genuine peer insights / **E = stessi 6 insight, stesso ordine e volume,
solo `pseudolabel` permutata via derangement frozen a zero punti fissi**; R=3; **12 fault-run fisici
indipendenti** → 36 osservazioni agent-case correlate/condizione; **A=0/36, B=31/36, E=3/36**;
**B−A=+0.861** (primario, 4/4 agenti), **B−E=+0.778** (specificità semantica, non primario); bootstrap
cluster-pairato su 12 cluster (CI B−A [0.833,0.917], B−E [0.722,0.833]); preservazione Normal/seen
100%. Contabilità inferenze: 15 held-out × 4 agenti × 3 condizioni × R=3 = **540 individuali → 180
aggregati**; sottoinsieme unseen = 108 individuali (36 aggregati) per condizione.

Cosa Experiment 1 **dimostra**: (1) *peer information is useful* (B≫A); (2) *il beneficio dipende
dalla correttezza semantica dell'associazione, non dal volume di testo* (B≫E). Cosa **non** tocca:
(3) *valore dell'organizzazione distribuita/federata*; (4) *FoT preferibile all'accesso centralizzato
alla stessa informazione*; (5) *generalità su più modelli*; (6) *generalità su più guasti/più run*.

---

## 2. RI-DERIVAZIONE: SERVE DAVVERO IL CENTRAL/POOLED ICL? (§5)

[INTERPRETAZIONE — è il punto più importante di questa revisione.]

La baseline central/pooled ICL testa (3) e (4): *la distribuzione aggiunge valore rispetto al
centralizzare la stessa informazione?* Chiediamoci se **il nostro paper deve sostenere (3) o (4)**.

- **Il contributo dichiarato** (versione Balanced della review) è sul **meccanismo di
  knowledge-transfer** sotto esperienza non-IID class-disjoint: *può la conoscenza testuale peer far
  riconoscere classi mai viste localmente, ed è la correttezza semantica a guidarlo?* → sono (1)+(2).
  **Non** rivendichiamo che federare batta il centralizzare.
- **Cosa fa il campo** [EVIDENZA]: FoT (Yao et al.) confronta *isolated agents* vs FoT, più RAG ed
  ExpeL; Federated In-Context LLM Agent Learning confronta con isolated / FL fine-tuning e misura il
  **costo di comunicazione**. Il comparatore *standard* del filone è **isolated** (che noi abbiamo =
  A), non un pooled-central ICL. Quindi un reviewer *non* considera il central-ICL come baseline
  obbligatoria del setting; considera obbligatorio l'isolated (già presente) e, semmai, un controllo
  di specificità (già presente, E) e un check di comunicazione.
- **Il rischio del central-ICL.** In questo setup, un agente "centrale" con l'unione della conoscenza
  (tutti gli 8 insight + tutti gli esempi locali) ha **strettamente più informazione** di ogni agente
  B (che ne riceve 6, peer-only): non è equal-information, è *more-information*. Renderlo davvero
  equal-information è delicato (quali 6 insight? quale identità di agente? quale label space?), e —
  peggio — se il central pareggia o supera B, un lettore ingenuo conclude *"allora la federazione è
  inutile"*, danneggiando un paper che non ha mai promesso (3)/(4).

**Verdetto** [RACCOMANDAZIONE]: il central/pooled ICL **NON è un must**. Va **declassato** da MUST a
**OPZIONALE/CONDIZIONALE**. La domanda "perché federare?" si risponde in **Discussion** con la
motivazione PV (proprietà dei dati distribuita, label centrali deboli, data locality) — cioè con
**framing**, non con un esperimento che introduce un endpoint che non ci serve. Lo si esegue **solo
se** si decide consapevolmente di rivendicare (3)/(4) — cosa che **non** consiglio per questa
submission.

---

## 3. SE (E SOLO SE) SI USA IL CENTRAL/POOLED ICL: specifica esatta (§6)

[RACCOMANDAZIONE] Se, contro il mio consiglio, si vuole includerlo, l'unica versione difendibile è un
**information-matched pooled reference**, non un "central onnisciente":

- **Un solo agente centrale**, stesso LLM, stesso prompt template, stesso R=3, **stesso held-out
  frozen**, stessa ground-truth blindness, stesso decision space (label space opaco completo).
- **Riceve esattamente l'unione degli insight che i peer avrebbero prodotto**, cioè **gli 8 insight**
  (2 per ciascuno dei 4 agenti), con `source_agent` e `pseudolabel` **mantenuti** — perché il central
  non ha "peer" da escludere. *Attenzione:* questo gli dà accesso anche all'insight della classe che
  in B è "propria" di ciascun agente ⇒ **non** è equal-information con un singolo agente B. L'unico
  confronto onesto è *"pooled-8 central" vs "l'unione dei 4 agenti B"* a livello di **copertura di
  sistema**, non a livello di singolo agente.
- **Ipotesi testata:** H_arch: *l'accuratezza di sistema del pooling centrale ≠ quella della
  federazione peer-only a parità di insight totali.* Endpoint: accuratezza unseen di sistema.
- **Come riportarlo:** come **reference descrittivo / topline informativa**, non come "il metodo da
  battere". Dichiarare esplicitamente che un pareggio **non** indebolisce (1)/(2).
- Se non si riesce a costruire un confronto realmente equal-information e fair, **dichiararlo e non
  usarlo** come benchmark artificiale.

Costo: ~ 15×1×3×R3 = 45 inferenze aggiuntive per il central su tutto l'held-out (economico), ma il
costo vero è **narrativo/di scope**, non computazionale.

---

## 4. VALUTAZIONE SISTEMATICA DELLE FAMIGLIE A–L (§7–8)

Per ciascuna: *rischio reviewer ridotto · RQ aggiunta · contributo incrementale · costo sperimentale ·
costo statistico · scope-creep · valore di pubblicazione · raccomandazione.*

**A. Equal-information centralized/pooled comparator.** Riduce: Reviewer A "perché federare". RQ:
(3)/(4). Contributo: basso *per il nostro focus*. Costo sper.: basso. Costo stat.: **nuovo endpoint
+ nuova famiglia di ipotesi**. Scope-creep: **alto** (sposta il paper su architettura). Valore pub.:
basso-medio. → **OPTIONAL / DO NOT (come benchmark).** Vedi §2–3.

**B. Second LLM / model replication.** Riduce: Reviewer B/D "un solo LLM proprietario, non
riproducibile" (quasi-fatale). RQ: "il transfer persiste cambiando il reasoner?" (generalità). Contr.:
**alto**. Costo sper.: medio (~540/modello, riusa tutto). Costo stat.: basso (replication per-modello;
**non** pooling tra modelli). Scope-creep: basso. Valore pub.: **alto**. → **MUST.**

**C. More independent TEP runs.** Riduce: Reviewer D "12 run, CI larghi". RQ: precisione, non nuova
domanda. Contr.: medio. Costo sper.: medio-alto (nuova simulazione + verbalizzazione + freeze
held-out). Costo stat.: **più cluster, stesso endpoint** (buono: non moltiplica ipotesi). Scope-creep:
basso. Valore pub.: medio. → **HIGH VALUE** (Package C, o B se c'è tempo).

**D. More TEP fault classes.** Riduce: Reviewer C/D "solo 4 guasti, poco diversi". RQ: "il transfer
generalizza a più/altri guasti?" (generalità di task). Contr.: **alto** ma. Costo sper.: **alto**
(nuovi agenti, nuovi insight, nuova generazione+freeze, controllo context-length). Costo stat.: nuovi
strati. Scope-creep: medio. Valore pub.: alto. → **HIGH VALUE solo in Package C.** Serve criterio di
selezione delle classi **pre-specificato** (es. i successivi IDV per indice fisso, esclusi quelli di
calibrazione) per evitare cherry-picking.

**E. More agents.** Riduce: Reviewer A "solo 4 client" (ottica di scala FL). RQ: scala distribuita.
Contr.: **basso** al meccanismo (per lo più cosmetico), a meno che accoppiato a D. Costo: medio.
Scope-creep: medio. Valore pub.: basso-medio. → **OPTIONAL** (solo se accoppiato a D).

**F. Classical numerical classifier (nearest-proto/CNN/TCN…).** Riduce: Reviewer C "dov'è il
baseline FDD". RQ: nessuna nostra. Problema: **non apples-to-apples** — un classificatore
centralizzato vede *tutte* le classi; il nostro task è *localmente unseen*. Può essere solo un
**oracle/upper-reference descrittivo**, mai un competitor. Costo: basso-medio. Scope-creep: medio
(confonde il contributo). Valore pub.: basso. → **OPTIONAL come oracle descrittivo; DO NOT come
baseline competitiva.**

**G. Parameter-based FL baseline (FedAvg/FedProto/fed-distill).** Riduce: Reviewer A "confronto con
FL". Problema: **paradigma diverso** (non c'è modello condiviso da aggregare); introdurrebbe un
problema differente e un impianto di training assente. Costo: alto. Valore pub.: basso (rischio di
sembrare un confronto forzato). → **DO NOT.** Discutere in Related Work.

**H. Raw-numeric / no-verbalizer LLM baseline.** Riduce: Reviewer C "il verbalizer fa il lavoro / TS
grezze basterebbero". RQ: "l'interfaccia deterministica aiuta il reasoning?". Contr.: medio (difende
la scelta del verbalizer come *enabling*, non come contributo). Costo: medio. Scope-creep: basso-medio
(rischia di spostare il focus sul verbalizer). Valore pub.: medio. → **OPTIONAL / HIGH VALUE-basso.**

**I. Insight ablations (source/scope/label-only/pattern-only/fewer/random subset).** Riduce: Reviewer
B/C "il testo è davvero informativo? cosa conta?". RQ: **decomposizione del segnale** (label vs
pattern vs quantità). Contr.: **alto** — potenzia il contributo *di valutazione/specificità* (la vera
novelty). Costo: medio (~108 inf/variante, riusa held-out+modello). Costo stat.: nuove condizioni →
gestire molteplicità. Scope-creep: **controllabile** se ci si limita a 2–3 varianti con RQ chiara.
Valore pub.: **alto**. → **HIGH VALUE (MUST del Package B).**

**J. Communication analysis.** Riduce: Reviewer A + fit Special Session ("communication constraints").
RQ: caratterizzazione (non efficiency claim). Contr.: medio a costo ~0. Costo sper.: **nullo** (dagli
artefatti). Scope-creep: nullo. Valore pub.: medio-alto per *questa* sessione. → **MUST.** Supporta
solo *"la comunicazione è limitata a testo compatto"* + rapporto insight/raw; **non** una claim di
efficienza superiore (non c'è comparatore parametrico misurato).

**K. Multi-round FoT.** Riduce: Reviewer B "il vostro è single-shot, FoT è multi-round". RQ: la
libreria evolutiva aiuta? Problema: **aumenta l'ambiguità interpretativa** (mescola generazione,
distillazione, propagazione errori) e allontana dal clean mechanism isolation. Costo: alto. Valore
pub.: medio ma rischioso. → **DO NOT** per questo paper; dichiarare il single-shot come **scelta di
design** e il multi-round come future work.

**L. Semantic-corruption variants (random label / irrelevant text / correct-label+wrong-desc /
source-permutation).** E isola già bene "correttezza dell'associazione vs volume". Un solo aggiunta
con RQ distinta e cheap può valere: **"irrelevant/random text"** distingue *informazione sbagliata*
(E) da *nessuna informazione utile*. Le altre (source-permutation, correct-label+wrong-desc) sono per
lo più ridondanti con E o con l'ablation I. → **OPTIONAL** (al più una variante "irrelevant-text");
**DO NOT** moltiplicare controlli ridondanti.

---

## 5. REVIEWER-RISK REDUCTION MATRIX (§9) — ordinata per riduzione-rischio / costo

| Esperimento/azione | Critica reviewer neutralizzata | Guadagno scientifico atteso | Costo | Riduzione rischio | Priorità |
|---|---|---|---|---|---|
| **Communication characterization (J)** | A: "perché federare / Big Data?" | Fit sessione + *"comunicazione = testo compatto"* | **~0** | Media | **1 (MUST)** |
| **Framing + attribuzione + terminologia + PV motivation** | A (è FL?), B (novelty vs FoT) | Rimuove claim fatali; posiziona il delta | ~0 | **Alta** | **1 (MUST)** |
| **Second-LLM replication (B)** | B/D: "un solo LLM proprietario, irreproducibile" | Generalità di modello | Medio (~540/mod.) | **Alta** | **2 (MUST)** |
| **Insight-content ablation (I)** | B/C: "il testo è davvero informativo? cosa conta?" | Decomposizione del segnale (evaluation contribution) | Medio (~324) | Medio-Alta | **3 (HIGH)** |
| **More independent runs (C)** | D: "12 run, CI larghi" | Precisione statistica | Medio-Alto | Media | 4 (HIGH, Pkg C) |
| More fault classes (+agents) (D/E) | C/D: "solo 4 guasti" | Generalità di task | Alto | Media | 5 (Pkg C) |
| Central/pooled ICL (A) | A: "perché federare?" | Testa (3)/(4) — non necessari | Basso comp./Alto scope | **Bassa (per il focus)** | Opzionale |
| No-verbalizer/raw-numeric (H) | C: "il verbalizer fa il lavoro" | Difende l'enabling layer | Medio | Bassa-Media | Opzionale |
| Classical FDD classifier (F) | C: "manca baseline FDD" | Oracle descrittivo | Basso-Medio | Bassa | Opzionale (oracle) |
| Parameter-FL baseline (G) | A: "confronto FL" | — (problema diverso) | Alto | Negativa (scope) | **DO NOT** |
| Multi-round FoT (K) | B: "single-shot" | Ambiguo | Alto | Bassa/negativa | **DO NOT** |

[INTERPRETAZIONE] Le prime tre righe (a costo ~0 le prime due, medio la terza) coprono i rischi
**fatali/quasi-fatali** (single-model, novelty framing) e il fit di sessione. Tutto ciò che sta sotto
"Second-LLM + Insight ablation" ha riduzione-rischio decrescente e costo/scope crescente.

---

## 6. COSA CONVIENE AUMENTARE (§10) — ranking con numeri concreti

Il meccanismo è già mostrato: le lacune di credibilità sono, in ordine, **generalità di modello** e
**generalità/precisione di task**. Ranking:

1. **More LLMs (replication).** *Perché primo:* neutralizza la critica singola più pericolosa a costo
   minimo (riusa held-out+insight+prompt+evaluator; cambia solo il reasoner). Massima
   riduzione-rischio per inferenza. Aggiunge una RQ di generalità reale.
2. **More fault classes.** *Perché secondo:* allarga la claim ("non specifico a 4 guasti scelti") e
   stressa il meccanismo su classi più difficili — più valore scientifico che semplici repliche. Ma
   costoso (nuovi agenti/insight/generazione/freeze).
3. **More independent runs.** *Perché terzo:* migliora la precisione (CI) e risponde a Reviewer D,
   ma non allarga la claim; è "più dello stesso".
4. **More agents.** *Perché ultimo:* migliora l'ottica di "scala distribuita" per una sede FL ma
   aggiunge poco al meccanismo, salvo se accoppiato a (2).

**Scenari di budget concreti:**
- **+100–200 agent-case inferenze:** *non* bastano per una replica full second-model (≈540) né per
  una runs-expansion. Investirle nell'**insight-content ablation sul solo sottoinsieme unseen** con il
  modello esistente: es. 1–2 varianti (label-only, pattern-only) × 36 unseen × R=3 = 108–216 inf. Alto
  valore mechanistico a basso costo.
- **+500–1000 inferenze:** eseguire l'**Experiment 2 (second-LLM full A/B/E ≈540)** — prima scelta.
  Con la coda del budget, aggiungere l'ablation unseen (≈324) → totale ~864, dentro 1000. In
  alternativa, se si preferisce la precisione statistica, **runs-expansion** (+5 run/guasto ≈ +540
  inf) al posto dell'ablation.
- **+1500–2000 inferenze (ambizioso):** Experiment 2 su **due** modelli (open-weight + API diversa,
  ~1080) + insight ablation (~324) + una variante "irrelevant-text" (~108) ≈ 1500.

---

## 7. DESIGN PRE-SPECIFICATI (§11) per gli esperimenti MUST/HIGH-VALUE

Ogni design va **congelato prima dell'esecuzione** (git tag dedicato) e prima di osservarne gli esiti.

### Experiment 2 — Second-LLM replication (MUST)

- **RQ:** il beneficio del transfer testuale (B≫A) e la sua specificità semantica (B≫E) persistono
  cambiando il modello di reasoning?
- **Ipotesi (pre-specificata):** H2a: B−A>0; H2b: B−E>0, per ciascun modello aggiuntivo.
- **Primary endpoint:** unseen accuracy A/B/E e contrasti B−A, B−E **per modello** (non poolati).
- **Secondary:** preservazione Normal/seen; concordanza per-agente del segno di B−A tra modelli.
- **Unità di indipendenza:** i **12 fault-run fisici** (identici a Exp 1) → bootstrap cluster-pairato
  invariato.
- **Test-set / data boundary:** **held-out frozen di Exp 1**, invariato; nessun nuovo dato; insight,
  esempi locali, prompt, pseudolabel, derangement E **riusati byte-identici**.
- **Modelli:** ≥1 **open-weight** (per riproducibilità piena; es. un Llama/Qwen-class di taglia
  adeguata) e, se budget, 1 di **famiglia diversa** dall'originale. Motivare la scelta a priori; NON
  scegliere il modello dopo aver visto i risultati.
- **R:** 3, aggregazione 2-di-3 identica; abstention = incorrect.
- **Statistica:** stesso bootstrap (10k, seed **nuovo e pre-dichiarato**, es. da fissare nel freeze).
- **Molteplicità:** ogni modello è una **replica indipendente pre-dichiarata**, non un test aggiuntivo
  sull'endpoint primario di Exp 1 → riportare per-modello; nessuna correzione necessaria se si evita
  di "cherry-pickare" il modello migliore.
- **Success criterion:** B−A>0 e B−E>0 con CI(B−A) escludente 0 su ≥1 modello open-weight, e segno
  concorde su ≥3/4 agenti.
- **Failure criterion:** se su un modello B−A≤0 o B−E≤0, **riportarlo onestamente** come limite di
  model-dependence (non nascondere) — è comunque informativo e difende dalla critica "cherry-picked
  model".
- **Freeze order:** (1) scelta modelli + seed + criteri → tag `exp2-protocol-frozen`; (2) esecuzione;
  (3) predictions → `exp2-inference-frozen`; (4) valutazione offline → `exp2-results-frozen`.

### Experiment 3 — Insight-content ablation (HIGH VALUE)

- **RQ:** quale componente dell'insight porta il segnale — l'associazione a `pseudolabel`, il testo
  `observed_pattern`, o la quantità?
- **Condizioni (oltre a B ed E già frozen), tutte a parità di routing peer-only:**
  - **B_label-only:** insight con `pseudolabel` corretta ma `observed_pattern` rimosso/oscurato.
  - **B_pattern-only:** `observed_pattern` corretto ma `pseudolabel` rimossa (label space anonimo).
  - **B_half:** 1 insight per peer invece di 2 (3 insight invece di 6) → effetto quantità.
  - *(opz.)* **B_irrelevant:** testo peer irrilevante/casuale, quantità pari a B → distingue
    "informazione sbagliata" (E) da "nessuna informazione utile".
- **Endpoint:** unseen accuracy per condizione; contrasti **B − B_label-only**, **B − B_pattern-only**,
  **B − B_half** (pre-dichiarati).
- **Ipotesi pre-specificata:** il pieno beneficio richiede **sia** pattern **sia** label corretti;
  attesa: B > B_label-only, B > B_pattern-only; B ≈ B_half se 3 insight bastano, altrimenti B > B_half.
- **Unità/test-set/boundary:** held-out frozen, 12 cluster, R=3, bootstrap invariato.
- **Molteplicità:** famiglia di 3–4 contrasti secondari → dichiarare che sono **secondari/esplorativi**
  rispetto a Exp 1; riportare CI, evitare claim primarie da questi.
- **Success/failure:** success se almeno B>B_label-only **e** B>B_pattern-only (mostra che serve la
  congiunzione); nessun "fallimento" fatale — ogni esito è interpretabile.
- **Freeze order:** protocollo+condizioni+seed → `exp3-protocol-frozen`; poi esecuzione; poi results.

### Experiment 4 — More independent runs (HIGH VALUE, opzionale/Package C)

- **RQ:** i contrasti restano stabili e con CI più stretti aumentando i run fisici indipendenti?
- **Design:** +k run/guasto sui **medesimi 4 guasti** + Normal, generati dal **parent simulator
  frozen** (S-function byte-identica), **congelati prima** di ogni verbalizzazione (held-out
  extension set, nuovo tag). Consiglio k tale da portare 3→6 run/guasto (12→24 fault-run, 36→72 unseen
  obs) se il budget lo consente.
- **Boundary:** stessi confini dati; nessun contatto con development.
- **Statistica:** stesso endpoint, **più cluster** (nessuna nuova famiglia di ipotesi — vantaggio).
- **Pre-specificare k prima di simulare** (evita "generato finché non ha funzionato").
- **Freeze order:** `exp4-heldout-frozen` → inference → results.

**Nota di indipendenza (tutti):** unità = *physical run*; il bootstrap resta clusterizzato; mai
trattare le osservazioni agent-case come indipendenti.

---

## 8. STRUTTURA DEL PAPER A PIÙ ESPERIMENTI (§12)

[RACCOMANDAZIONE] La struttura più forte (Package B):

- **Experiment 1 — Controlled mechanism isolation (frozen).** A/B/E; B−A primario; **B−E specificità**.
- **Experiment 2 — Model-generality replication.** Stesso protocollo, altri LLM → generalità.
- **Experiment 3 — Insight-content decomposition.** Cosa nel testo porta il segnale.
- **Communication characterization** come sottosezione di Results (non un "Experiment" a sé).

**Non** adottare automaticamente un "Experiment 2 = architecture/equal-information control": inseritelo
solo se si sceglie di rivendicare (3)/(4) (§2). La spina dorsale è **mechanism → generality →
decomposition**, tutta *evaluation-side*, coerente con la novelty reale.

---

## 9. NOVELTY ALLA LUCE DEI NUOVI ESPERIMENTI (§13)

[INTERPRETAZIONE] Non inseguire una nuova *method novelty*. L'esperimento che trasforma "plausible"
in "molto più convincente" è un **evaluation contribution**, non un'architettura:

- **Second-LLM replication + insight-content decomposition** convertono la claim da *"in un setting,
  con un modello, il testo peer aiuta"* a *"attraverso modelli diversi, e decomponendo il contenuto
  testuale, mostriamo che è la **congiunzione pattern+associazione corretta** a trasferire
  informazione discriminativa"*. Questa è una tesi di **specificità semantica model-general**, molto
  più difficile da attaccare e distintiva rispetto a FoT (che non fa né la decomposizione né questo
  controllo su un task class-disjoint di serie temporali).
- La novelty resta **combinazione + evaluation design**; i nuovi esperimenti la **irrobustiscono**
  senza spostarla verso un claim di metodo che non possiamo difendere.

---

## 10. BASELINE ATTESE DALLA LETTERATURA (§14) — aggiornamento e verifiche

[EVIDENZA] Baseline/ablation tipiche dei vicini:
- **FoT (Yao et al. 2026):** baseline = *isolated agents*, **RAG datastore**, **ExpeL**; ablation su
  local-reasoning, aggregation, modelli eterogenei, library size, participation. → Il comparatore
  standard è **isolated** (≡ nostra A) + eventualmente **RAG/retrieval**; **non** un pooled-central.
- **Federated In-Context LLM Agent Learning (2024):** baseline = isolated / FL fine-tuning; enfasi su
  **communication cost**. → Rende la nostra *communication characterization* attesa e apprezzata.
- **FedProto / FedMD / fed-distill:** baseline = FedAvg/FedProx/local-only; ablation su grado di
  non-IID. → Confronti *parametrici*, non applicabili al nostro paradigma (§4-G).
- **FedMeta-FFD (Chen, Tang, Li, IEEE TNSE 2023, DOI 10.1109/tnse.2023.3266942)** [verificato]: FL +
  meta-learning per few-shot FDD; **si adatta a categorie di guasto nuove** con pochi esempi
  etichettati; global meta-learner (parametrico). → Vicino sull'idea "nuovi guasti cross-client", ma
  richiede *alcune* etichette della nuova classe e aggrega un modello: **non** riconosce classi
  *mai viste localmente* via solo testo. Da citare come ADJ nel confronto FDD.

[INTERPRETAZIONE] Un reviewer del *nostro* setting considera "standard": **isolated (A)** ✓, un
**controllo di specificità (E)** ✓, e — sempre più — un **model-generality check** e una **communication
analysis**. Il central-ICL **non** è lo standard del filone.

**Aggiornamento verifiche referenze:**
- **Confermate** (Crossref/OpenAlex): FedProto (10.1609/aaai.v36i8.20819), FedCKD label-exclusive
  (10.1007/978-981-92-1462-4_29), Fed. ZSL mid-level semantic transfer (10.1016/j.patcog.2024.110824),
  FedMeta-FFD (10.1109/tnse.2023.3266942).
- **NON confermata:** *"One-Shot Federated Distillation Using Monoclass Teachers"* — assente da
  Crossref/OpenAlex (solo record HAL). [RACCOMANDAZIONE] **Non citarla** finché venue/DOI non sono
  verificati; l'analogo "monoclass/label-exclusive" è già coperto da **FedCKD**. Rimuovere o
  sostituire nella bibliografia della review.

---

## 11. AUDITABILITY COME CONTRIBUTO (§16)

[FATTO — REPO] Il progetto ha: protocol/inference/result freeze; hash SHA-256; provenance completa;
evaluator offline deterministico; **join della ground-truth solo dopo l'inference**; pseudolabel
opache; confini dati espliciti; held-out guard fail-closed.

[INTERPRETAZIONE + RACCOMANDAZIONE] È un **punto di forza reale e citabile per IEEE BigData**
(topic: *evaluation metrics and benchmarking*, reproducibility). Posizionarlo come **contributo
metodologico secondario** — *"an auditable, fully pre-specified and frozen evaluation protocol for
LLM-mediated federated textual knowledge transfer"* — **senza** chiamarlo "novelty" in senso forte
(il freeze/hashing non è nuovo di per sé): la combinazione *pseudolabel opache + freeze chain +
ground-truth-blind inference + specificity control* è però una pratica di valutazione
**leakage-resistant** poco comune nel filone LLM-agent, e vale come contributo di rigore.

---

## 12. BIG DATA FIT + PV (§17–18)

**Big Data fit** [INTERPRETAZIONE]: con il target PV, il framing difendibile è **distributed sensor
analytics across heterogeneous sites**: *decentralized data ownership · heterogeneous sensor streams ·
non-IID local experience · communication constraints · data locality*. La **communication
characterization** (§4-J) è il pezzo che rende concreto il "Big Data / FL on Big Data" senza
inventare Volume/Velocity. **Vietato**: usare Volume (TEP è piccolo per costruzione) o Velocity (niente
streaming valutato). PV **motiva** il problema Big Data; **non** è evidenza di performance.

**PV — quanto inserirne, senza overclaiming** [RACCOMANDAZIONE]:
- **Introduction: SÌ**, breve e mirato. La motivazione è *forte e onesta*: il PV distribuito genera
  esperienza locale eterogenea per natura (siti, meteo, equipaggiamento, regimi), **ma** la ground
  truth dei guasti sul campo è debole/inaffidabile → **da qui la scelta metodologica** di isolare il
  meccanismo in un testbed controllato a verità nota. Questa narrativa spiega *perché* servono
  rappresentazione diagnosis-neutral, confini dati verificabili e non-IID esplicito. **Non**
  opportunistica: è esattamente il razionale del testbed.
- **Motivation/Discussion: SÌ** per collegare il non-IID class-disjoint alla realtà PV e per il
  "perché federare" (data ownership distribuita, label centrali deboli).
- **Cosa menzionare / cosa no:** menzionare, in forma **generale**, *multi-site heterogeneity* e
  *weak/uncertain field labels* (giustificano il design). **Tenere fuori** i dettagli concreti del
  dataset non ancora usato — *11 impianti, ~41 variabili meteo, dati inverter-level, 5 min, 4 anni* —
  perché numeri specifici su dati non impiegati fanno chiedere "dove sono i risultati PV?" e fanno
  sembrare TEP un preliminare incompleto.
- **Vietato** [dai vincoli]: TEP simula il PV; i risultati TEP generalizzano al PV; le stesse feature
  passeranno al PV; gli 11 impianti sono già usati; dataset PV validato; label PV affidabili.

**PV nell'Abstract — verdetto: CONDITIONAL-YES (una sola proposizione di motivazione).**
[INTERPRETAZIONE] Una clausola motivazionale iniziale colloca la rilevanza Big Data ed è appropriata,
**a patto** che inquadri TEP come scelta *deliberata e rigorosa*, non come ripiego.
- **Formulazione raccomandata (usare questa):**
  > *"Motivated by distributed photovoltaic monitoring—where heterogeneous local experience
  > accumulates across sites while field fault labels remain weak—we isolate the textual
  > knowledge-transfer mechanism in a controlled multivariate testbed with verifiable ground truth."*
- **Evitare** *"As a controlled precursor to distributed PV monitoring…"*: "precursor" fa sembrare
  TEP incompleto/preliminare. Preferire *"controlled testbed with verifiable ground truth"*.
- Se si vuole massima prudenza, l'alternativa **NO** (nessun PV in abstract; PV solo in Intro) è
  accettabile e sicura; ma una singola clausola motivazionale, ben formulata, **aiuta** il fit di
  sessione più di quanto rischi.

---

## 13. TRE PACCHETTI SPERIMENTALI (§19)

### PACKAGE A — Minimum defensible
- **Esperimenti:** Communication characterization (J) + framing/terminologia/PV-motivation + delta
  esplicito vs FoT e vs Federated In-Context LLM Agent Learning.
- **Rationale:** rimuove i rischi *fatali* (claim di privacy/generalizzazione; "we propose FoT";
  "è FL?") a costo ~0, senza nuove inferenze.
- **Inference count:** **0** nuove (solo misure sugli artefatti).
- **Nuovo sviluppo:** script di conteggio byte/token (banale).
- **Rischio:** resta la critica "un solo LLM" (Reviewer B/D) e "solo 4 guasti/12 run" (D).
- **Reviewer neutralizzato:** parzialmente A e B (framing).
- **Nuova claim possibile:** *"communication is limited to compact textual insights (ratio X vs raw
  series)"* — descrittiva.

### PACKAGE B — Recommended for acceptance
- **Esperimenti:** Package A **+ Experiment 2 (second-LLM replication)** + **Experiment 3
  (insight-content ablation)**.
- **Rationale:** converte "un modello, un controllo" in "model-general + decomposizione del segnale";
  colpisce la critica più pericolosa (single-model) e potenzia l'evaluation contribution (la vera
  novelty).
- **Inference count:** ~540 (Exp 2, un modello; ~1080 con due) + ~324 (Exp 3) ≈ **~864–1400**.
- **Nuovo sviluppo:** integrazione di ≥1 LLM aggiuntivo nello stesso runner; generatore delle varianti
  di insight (label-only/pattern-only/half) — riusa insight/prompt/evaluator esistenti.
- **Rischio:** scope-creep contenuto (tutto sullo stesso held-out frozen); molteplicità dei contrasti
  secondari da dichiarare.
- **Reviewer neutralizzato:** B/D (single-model), B/C (il testo è informativo? cosa conta?); A/D
  parzialmente.
- **Nuove claim possibili:** *"the transfer and its semantic specificity replicate across LLMs"* +
  *"the benefit requires the conjunction of correct pattern text and correct label association"*.

### PACKAGE C — Ambitious
- **Esperimenti:** Package B **+ Experiment 4 (more independent runs, 3→6/guasto)** **e/o** more fault
  classes+agents (4→6) con criterio di selezione pre-specificato; opz. Exp 2 su un **secondo** modello.
- **Rationale:** generalità di task + precisione statistica (CI più stretti); credibilità di scala per
  una sede FL.
- **Inference count:** +~540 (runs) e/o +~800–1200 (più guasti/agenti) → totale **~2000–3000**.
- **Nuovo sviluppo:** nuova generazione/freeze held-out; (per i guasti) nuovi agenti/insight, controllo
  context-length.
- **Rischio:** **alto** di scope-creep e di non chiudere entro il 30/09; la generazione di nuovi run
  reintroduce il tema della riproducibilità del simulatore.
- **Reviewer neutralizzato:** D (scala/CI), C/D (diversità di guasti).
- **Nuove claim possibili:** *"the effect is stable across additional independent runs / additional
  fault classes"* — generalità.

---

## 14. RACCOMANDAZIONE UNIVOCA (§20)

[RACCOMANDAZIONE — "se fossi il supervisor"] **Eseguirei esattamente questo, in questo ordine:**

1. **Communication characterization** (oggi, ~0 costo) — misure byte/token insight vs raw series
   sugli artefatti frozen.
2. **Experiment 2 — second-LLM replication** su **un modello open-weight** (riproducibile) sull'intero
   A/B/E dell'held-out frozen (~540 inf), protocollo congelato prima.
3. **Experiment 3 — insight-content ablation** (label-only, pattern-only, fewer-insights) sul
   sottoinsieme unseen (~324 inf), protocollo congelato prima.
4. *(Se e solo se resta tempo e budget prima del freeze finale)* **un secondo LLM** in Exp 2 (di
   famiglia diversa) per rafforzare la generalità — **non** more-runs/more-faults, che rischiano di
   non chiudere in tempo.

Questo è **Package B** (nucleo). Massimizza riduzione-rischio per unità di costo, non tocca Experiment
1, e costruisce una tesi *evaluation-side model-general* difficile da rifiutare.

**Cosa NON fare:** central/pooled ICL come benchmark; baseline FL parametrica (FedAvg/FedProto);
classificatore FDD come competitor (al più oracle descrittivo); multi-round FoT; V3 verbalizer;
qualsiasi esperimento PV; controlli di corruzione ridondanti oltre E (al più *una* variante
irrelevant-text se avanza budget).

---

## 15. RESEARCH QUESTIONS FINALI (§21)

Tre RQ (non quattro: la quarta — confronto con comparatore federato/centralizzato — non è
scientificamente necessaria per il contributo dichiarato):

- **RQ1.** *Can peer-derived textual knowledge enable agents with class-disjoint temporal experience
  to recognize locally unseen fault conditions?* → Experiment 1, B−A.
- **RQ2.** *Does the benefit depend on the semantic correctness of the transferred associations rather
  than on the mere presence/volume of text?* → Experiment 1, B−E; **Experiment 3** (decomposizione
  pattern/label/quantità).
- **RQ3.** *Does the observed transfer and its semantic specificity persist across different reasoning
  models?* → **Experiment 2**.

(Se si adottasse Package C: **RQ3b** *…and across additional independent runs / fault classes?*)

---

## 16. CLAIM SET PER PACKAGE (§22)

**Package A** — Primaria: *peer textual knowledge transfers discriminative information for locally
unseen faults in a controlled testbed (B−A)*. Secondaria: *the benefit is semantically specific
(B−E)*; *communication is limited to compact text*. **Vietate:** privacy-preserving, generalizable,
robust, scalable, communication-efficient(superiorità), superior-to-FL, superior-to-central.

**Package B** — Primaria: come A. Secondarie: *the transfer and its semantic specificity **replicate
across LLMs*** (Exp 2); *the effect requires the **conjunction** of correct pattern text and correct
label association* (Exp 3). **Vietate:** identiche ad A (in particolare *generalizable* e
*communication-efficient* come superiorità restano vietate).

**Package C** — Aggiunge: *the effect is **stable across additional independent runs / fault
classes*** (generalità empirica intra-testbed). **Ancora vietate:** cross-domain generalization (PV),
privacy, superiority-to-FL/central.

[REGOLA] In nessun package: *privacy-preserving · generalizable · robust · scalable · communication
efficient(superiore) · superior to FL · superior to centralized learning* — salvo nuova evidenza
diretta (che questi pacchetti **non** producono).

---

## 17. RED TEAM FINALE (§23) — dopo Package B

Domanda per ciascuno: *dopo i nuovi esperimenti, quale resterebbe la mia principale ragione di
rejection?*

- **Reviewer A (FL).** Residuo: *"È in-context transfer, non FL: nessun modello aggregato; 4 client."*
  → **Non risolvibile con esperimenti** senza snaturare il lavoro; si gestisce con terminologia
  ("federated knowledge transfer / FL-like"), la linea FedMD→FedProto→FoT, e il fit su
  *collaborative/non-IID*. **Severità: moderate.** Non richiede nuovi esperimenti.
- **Reviewer B (LLM/FoT).** Residuo: *"Delta rispetto a FoT/Federated In-Context LLM Agent Learning
  ancora incrementale."* → Dopo Exp 2+3 il delta è più forte (dominio TS + class-disjoint + specificità
  model-general + decomposizione). Resta un giudizio di *grado*. **Severità: moderate**, gestibile con
  framing del contributo (evaluation, non metodo).
- **Reviewer C (TS/FDD).** Residuo: *"Solo 4 guasti, un simulatore; niente baseline FDD."* →
  Parzialmente aperto in Package B (chiuso in C con più guasti/run). **Severità: moderate.**
  Risolvibile sperimentalmente **solo** con Package C (più run/guasti) entro il tempo: valutare se vale
  il rischio di non chiudere.
- **Reviewer D (stat/metodo).** Residuo: *"12 run fisici, CI larghi; molteplicità dei contrasti
  secondari di Exp 3."* → Package B non aumenta i run (li aumenta C). Gestibile con CI clusterizzati,
  dichiarazione dei contrasti come secondari/esplorativi, e onestà sulla scala. **Severità: moderate**;
  la parte *precisione* è risolvibile solo con Package C.

**Conclusione red team:** dopo Package B **non resta alcuna critica fatale**; restano critiche
*moderate* di grado (novelty incrementale, scala). L'unica risolvibile-sperimentalmente-entro-il-tempo
è la **scala** (Package C, più run/guasti): da soppesare contro il rischio di deadline. Il mio
giudizio: **Package B è il punto di massimo rapporto accettazione/rischio**; Package C solo se il
freeze di Exp 2/3 è chiuso con ampio margine.

---

## 18. TABELLA DELLE DECISIONI (§24)

| Decision | Recommendation | Motivazione (una frase) |
|---|---|---|
| Keep frozen Experiment 1? | **YES** | È il mechanism-isolation study; non va toccato — è il cuore del paper. |
| Add central/pooled ICL? | **CONDITIONAL** | Solo se si sceglie di rivendicare "valore della distribuzione" (3/4), che questo paper non deve; altrimenti scope-creep. |
| Add second LLM? | **YES** | Neutralizza la critica quasi-fatale "un solo LLM proprietario"; massimo rapporto valore/costo. |
| Add more TEP runs? | **CONDITIONAL** | Utile per CI più stretti (Package C) ma richiede nuova simulazione/freeze; solo con margine di tempo. |
| Add more fault classes? | **CONDITIONAL** | Alta generalità di task ma alto costo/scope; solo Package C con criterio di selezione pre-specificato. |
| Add more agents? | **NO** (salvo con più guasti) | Da solo è per lo più cosmetico per il meccanismo. |
| Add classical FDD baseline? | **CONDITIONAL** | Solo come oracle/upper-reference descrittivo; non è apples-to-apples col task locally-unseen. |
| Add parameter-FL baseline? | **NO** | Paradigma diverso (nessun modello condiviso); introdurrebbe un problema differente. |
| Add communication analysis? | **YES** | Costo ~0, alto fit con la Special Session; supporta una claim descrittiva onesta. |
| Add verbalizer ablation? | **CONDITIONAL** | Il no-verbalizer/raw-numeric difende l'enabling layer ma rischia di spostare il focus; opzionale. |
| Add multi-round FoT? | **NO** | Aumenta l'ambiguità interpretativa; single-shot è una scelta di design, multi-round = future work. |
| Mention PV in Introduction? | **YES** | Motivazione forte e onesta (label reali deboli → serve testbed a verità nota); giustifica le scelte di design. |
| Mention PV in Abstract? | **CONDITIONAL-YES** | Una sola clausola motivazionale ("Motivated by distributed PV monitoring…"), mai come dominio studiato. |
| Develop V3 verbalizer now? | **NO** | La letteratura (T2SP/TRUCE) copre l'interfaccia; non è richiesto per la difendibilità. |
| Run PV experiment before submission? | **NO** | Fuori scope; dataset non pronto/validato, label inaffidabili; sarebbe overclaiming. |

---

## 19. STARTING TODAY — COSA IMPLEMENTARE PER PRIMO (§25)

1. **Primo (oggi):** **Communication characterization** — script che calcola, dagli artefatti frozen,
   byte/token/caratteri degli insight scambiati (6 per agente) e li rapporta alla dimensione della
   serie grezza per caso (41 XMEAS × campioni). Zero nuove inferenze, zero rischio. Produce una figura/
   riga per la Special Session.
2. **Secondo:** **Experiment 2 — second-LLM replication** su **un modello open-weight**. Prima
   *pre-specificare e congelare* (`exp2-protocol-frozen`: modello, seed bootstrap, endpoint, criteri
   di successo/fallimento), poi eseguire A/B/E sull'held-out frozen riusando insight/prompt/evaluator,
   poi `exp2-results-frozen`. ~540 inferenze.
3. **Terzo:** **Experiment 3 — insight-content ablation** (label-only, pattern-only, fewer-insights)
   sul sottoinsieme unseen. Congelare il protocollo prima (`exp3-protocol-frozen`), poi eseguire.
   ~324 inferenze.

**Cosa congelare prima di eseguire (ordine di freeze, per ogni nuovo esperimento):**
protocollo+ipotesi+endpoint+criteri+seed → *(freeze)* → esecuzione → predictions → *(freeze)* →
evaluation offline → *(freeze)*. Riusare l'evaluator e il bootstrap di Exp 1 **senza modificarli**.
Nessuna scelta (modello, k run, classi) va fatta **dopo** aver visto gli esiti.

**Risultati che imporrebbero un cambio di framing:**
- Se in **Experiment 2** un secondo modello desse **B−A ≤ 0** o **B−E ≤ 0**: il transfer è
  *model-dependent* → ridimensionare da "il meccanismo trasferisce" a "trasferisce **con questa classe
  di modelli**"; riportarlo apertamente (rafforza la credibilità, non la distrugge).
- Se in **Experiment 3** risultasse **B ≈ B_pattern-only** (la label corretta non serve): la storia
  "semantic specificity" si indebolisce → riformulare come "è il **contenuto del pattern** a
  trasferire, indipendentemente dall'etichetta" (una claim diversa, ancora pubblicabile ma da riscrivere).
- Se **B ≈ B_label-only** (basta l'etichetta, il testo non serve): allarme — il beneficio potrebbe
  derivare da *label leakage*/prior; rivedere il controllo anti-leakage e il framing prima di
  qualunque claim.
- Se la **communication analysis** mostrasse insight non più piccoli della serie grezza (improbabile):
  eliminare qualsiasi accenno a compattezza/comunicazione.

**Principio guida.** Non preservare Experiment 1 "a ogni costo" né aggiungere esperimenti perché "di
più è meglio": ogni aggiunta ha una funzione precisa — **Exp 2** uccide "single-model", **Exp 3**
irrobustisce la specificità (la vera novelty), **communication** serve il fit di sessione. Tutto il
resto è, oggi, rumore rispetto alla deadline.

---

*Fine del piano. Experiment 1 resta frozen (`45ec4ee`). Ogni nuovo esperimento è pre-specificato e
congelato prima dell'esecuzione, separato da Experiment 1. Riferimenti verificati in §10; la voce
"monoclass teachers" è stata rimossa perché non confermata in cataloghi indicizzati.*
