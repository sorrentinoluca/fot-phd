# Literature Review mirata — Federation over Text su serie temporali multivariate (TEP)
## Posizionamento scientifico per IEEE BigData 2026 — Special Session on Federated Learning on Big Data

**Ruolo del revisore.** Senior researcher / reviewer IEEE. Obiettivo: stabilire con rigore
come posizionare l'esperimento *Federation over Text* (FoT) su serie temporali multivariate
rispetto allo stato dell'arte, quali claim siano difendibili e quali obiezioni dei reviewer
siano prevedibili. Il documento **non** vende il paper: stima quanto sia realmente nuovo,
corretto e in-scope.

---

### Metadati della consultazione

- **Repository analizzato:** `github.com/sorrentinoluca/fot-phd`, branch `main`.
- **Commit SHA:** `406a889eaa66e3fb82b6af8cc7c6d1e16b4996fb` (HEAD di `main`, 2026-09-02 01:27 CET).
- **Tag scientifico dei risultati:** `phase-b-results-frozen` → `45ec4eed65b263a5803ced7d01064c4672e81e86`.
- **Data della consultazione:** 2026-09-02.
- **Fonte primaria obbligatoria (metodo):** Yao, Rabbani, Zaheer, Li, *Federation over Text:
  Insight Sharing for Multi-Agent Reasoning*, arXiv:2604.16778v2, 23 May 2026 (preprint;
  U. Chicago + Google DeepMind). Copia locale: `2604.16778v2.pdf`. Codice: `github.com/dixiyao/FoT`.
- **Call di destinazione:** IEEE BigData 2026, *Special Session on Federated Learning on Big Data*.

### Gerarchia delle fonti applicata

1. Frozen protocol/results/artifacts (`phase_b/final_evaluation/`, `PHASE_B_PROTOCOL_FREEZE.md`).
2. Codice/config frozen (`code/`, `phase_b/config/`, verbalizer freeze).
3. `README.md` / `AUDIT_GUIDE.md`.
4. Technical narrative + final synthesis + LLM reference.
5. Walkthrough / documenti storici.

In caso di conflitto vince l'artefatto frozen. Tutti i numeri riportati sotto come *FATTO DAL
REPOSITORY* sono stati letti dai file frozen (README, `EVALUATION_REPORT.md`,
`PHASE_B_PROTOCOL_FREEZE.md`, `final_local_insights.json`, `VERBALIZER_V2_FREEZE.md`).

### Convenzione di lettura (usata in tutto il documento)

- **[FATTO — REPO]** = verificato negli artefatti del repository.
- **[EVIDENZA — LETTERATURA]** = affermazione sostenuta da fonte primaria esterna.
- **[INTERPRETAZIONE]** = mia lettura da reviewer.
- **[RACCOMANDAZIONE]** = cosa consiglio di fare/scrivere.

Distinzioni tenute rigorosamente separate: assenza di scambio di raw-data ≠ privacy formale;
FoT (Yao et al.) ≠ invenzione di questo progetto; non-IID ≠ privacy; textual knowledge transfer
≠ parameter aggregation; feasibility evidence ≠ generalization.

---

# OUTPUT 1 — EXECUTIVE REVIEW

**1. Il paper è in scope per la Special Session?**
Parzialmente, con un rischio di framing reale. La Special Session *Federated Learning on Big
Data* [EVIDENZA] elenca fra i topic: *collaborative learning frameworks*, *challenges under
non-IID data distributions*, *novel architectures and platforms*, *evaluation metrics and
benchmarking*, *privacy-preserving mechanisms*, *applications (healthcare, finance, IoT)*.
Il nostro lavoro tocca genuinamente *collaborative learning*, *non-IID*, *novel architecture* e
*benchmarking/evaluation*. Tuttavia la sessione è a impostazione **FL classica** (aggregazione
di modelli/gradienti, privacy dei dati, edge). Il nostro sistema **non aggrega né gradienti né
pesi**: scambia *insight testuali*. [INTERPRETAZIONE] È in-scope come *collaborative /
knowledge-transfer learning* sotto non-IID, non come FL parametrico. In-scope: **sì, se
inquadrato come collaborative/federated knowledge transfer**; **no**, se ci si aspetta
aggregazione di modelli.

**2. I 3–5 filoni più importanti.**
(i) *Federated knowledge distillation / knowledge transfer* senza parameter averaging
(FedMD, FedDF, FedGKT, FedProto, FedGen; + label-exclusive: FedCKD, monoclass teachers) — è il
**vero predecessore metodologico**. (ii) *Textual/semantic knowledge exchange & multi-agent LLM*
(FoT originale, Federated In-Context LLM Agent Learning, Social Learning, ExpeL/Metacognitive
Reuse). (iii) *Federated LLM / foundation models* (Time-FFM, FedCoT). (iv) *Non-IID missing-class /
class-disjoint experience* (tassonomia non-IID; partially class-disjoint data). (v) *Federated
time-series / fault diagnosis* (contesto applicativo di confronto).

**3. I 5 lavori più vicini.**
(1) **Federation over Text** — Yao et al. 2026 (il metodo che applichiamo). (2) **Federated
In-Context LLM Agent Learning** (arXiv:2412.08054) — federazione di conoscenza in linguaggio
naturale, dati grezzi locali. (3) **FedCKD** — cross-client KD con dataset *label-exclusive*
(struttura non-IID class-disjoint quasi identica; analogo strutturale di "Normal + un guasto"). (4)
**FedMeta-FFD** (Chen et al., IEEE TNSE 2023) — federated meta-learning per nuove categorie di guasto
cross-client (neighbor FDD più diretto). (5) **Federated zero-shot learning with mid-level semantic
knowledge transfer** (Pattern Recognition 2024) — trasferimento *semantico* verso classi non viste in
FL. Adiacenti forti: Time-FFM, FedCoT.

**4. Novelty ancora difendibile.**
Non il *metodo* FoT (è di Yao et al.). È difendibile una novelty di **combinazione + dominio +
disegno sperimentale controllato**: prima applicazione documentata di FoT a **serie temporali
multivariate / diagnosi guasti**, sotto una eterogeneità **non-IID di tipo class-disjoint
(missing-class)** — diversa dalla eterogeneità cross-task di FoT — con un **controllo di
specificità pre-registrato (B vs E, derangement delle pseudolabel a parità di testo)** che, nella
letteratura esaminata, non ho identificato applicato a questo problema. Vedi Novelty Red Team.

**5. Principale minaccia alla novelty.**
FoT (Yao et al.) rivendica **già** trasferimento cross-domain a task non visti, weak-to-strong nel
text space e un'analisi di leakage. Federated In-Context LLM Agent Learning rivendica **già**
federazione di conoscenza in linguaggio naturale con dati locali. La combinazione "FL + testo +
non-IID + LLM" è **già occupata** a livello concettuale. La nostra difesa residua è *dominio TS +
tipo di non-IID missing-class + controllo di specificità*, non il paradigma in sé.

**6. Principale minaccia metodologica.**
La scala e il *floor* del baseline. A = **0/36** sulle classi non viste [FATTO — REPO] genera un
B−A enorme (+0.861) ma **strutturale**: A è privo di evidenza class-semantica per le classi unseen.
Inoltre: 12 fault-run fisici indipendenti (non 36), un solo LLM (`gpt-5.6-terra`, temperature/seed
non esposti), un solo simulatore/mode, 4 guasti. Rischio "evidenza di feasibility, non di
generalizzazione".

**7. Baseline aggiuntiva più probabilmente richiesta.**
Un **comparatore a informazione equivalente ma centralizzato/pooled** (central-ICL o pooled
textual knowledge): stessi 6 insight forniti a un singolo agente centrale, per isolare il valore
della *provenance distribuita* rispetto al semplice avere l'informazione. Il team lo dichiara già
come questione aperta [FATTO — REPO, `FoT versus central ICL`]. È il buco più citabile da un
reviewer FL.

**8. Possiamo presentare FoT come Federated Learning senza qualificazioni?**
**No.** Gli stessi autori originali lo definiscono *"federated learning-like"* / *"analogous to
FL"*, mai FL puro [EVIDENZA]. Il nostro setup non aggrega parametri/gradienti. Presentarlo come
"Federated Learning" senza qualificatore in una sessione FL classica è un invito al rifiuto da
parte del Reviewer A. Usare *federated knowledge transfer / FL-like collaborative learning*.

**9. Terminologia consigliata in titolo/abstract.**
Preferire **"federated (textual) knowledge transfer"** o **"federated knowledge sharing"** con
FoT nominato come metodo di riferimento; evitare "Federated Learning" nudo, "privacy-preserving",
"robust", "generalizable", "secure". Vedi OUTPUT 5.

**10. Submission readiness: PLAUSIBLE (al limite basso di *plausible*).**
[INTERPRETAZIONE] La combinazione dominio + controllo di specificità + rigore di freeze è un
contributo onesto e pubblicabile in una sessione speciale, *a condizione* di (a) framing
terminologico corretto, (b) aggiunta o discussione seria del comparatore a informazione
equivalente, (c) esposizione esplicita del floor di A e della scala. Senza almeno la discussione
rigorosa di (b), scivola verso *risky* di fronte a un reviewer FL. Non è *strong* perché la
novelty di metodo appartiene a Yao et al. e la scala è piccola.

---

# PARTE A — RICOSTRUZIONE DEL NOSTRO ESPERIMENTO (dal repository)

Tutto in questa sezione è **[FATTO — REPO]** salvo dove indicato.

## A.1 Architettura sperimentale

- **4 agenti.** Ciascun agente conosce **Normal + esattamente una** pseudoclasse di guasto locale
  (`PHASE_B_PROTOCOL_FREEZE.md §B`). Le pseudoclassi di guasto sono 4 in totale
  (`CLS-ZOGAA`, `CLS-OJNSG`, `CLS-R463B`, `CLS-Z3ISU`). Per ogni agente, le **altre 3** pseudoclassi
  di guasto sono **localmente non viste** (locally unseen).
- **Pseudolabel opache.** Le etichette reali dei guasti sono sostituite da token opachi `CLS-XXXXX`
  di ugual lunghezza; la mappa reale→opaca è **evaluator-side only** e non entra nei prompt
  (`§C`). Serve a neutralizzare la prior knowledge dell'LLM sul benchmark TEP.
- **Interfaccia di verbalizzazione (Phase A, enabling layer).** Serie temporale multivariata → 41
  variabili XMEAS × 17 componenti = **697 scalari** per caso, poi **testo neutrale** deterministico.
  Feature: `shift_sigma` (spostamento firmato), `slope_sigma_h` (pendenza firmata),
  `residual_std_ratio`, `diff_std_ratio`, + `raw_std_ratio` descrittivo. Soglie calibrate **solo su
  Normal development** (N1–N5), `alpha=0.05`. Il renderer **non** assegna etichette né trasforma la
  dispersione in "drift/oscillazione/diagnosi" (`VERBALIZER_V2_FREEZE.md`). Pipeline dichiarata:
  `time series → structured evidence → neutral text → reasoning/diagnosis`.
- **Conoscenza locale.** Per ogni classe locale l'agente ha **2 esempi neutral-text** (batch 1–2,
  Normal N1–N2) nel prompt diagnostico. Gli **insight** sono generati usando le 5 batch di
  development (1–5). Boundary dati rispettato: held-out mai aperto in fase di generazione insight
  (`FINAL_INSIGHT_GENERATION_REPORT.md`: Held-out accessed = false, Leakage audit PASS).
- **Cosa viene scambiato (l'oggetto federato).** **8 insight testuali** totali (2 per agente),
  ciascuno = JSON con `insight_id`, `source_agent`, `pseudolabel` (`CLS-XXXXX`), `evidence_scope`,
  `observed_pattern`. `observed_pattern` è una **sintesi statistica in linguaggio naturale** dei
  pattern locali (es. *"XMEAS-1 supera la soglia di spostamento in 8/8 finestre… massima dispersione
  (rapporto dev.st. 46.06–46.50)"*). **Nessuna serie temporale grezza, nessun vettore numerico,
  nessun gradiente, nessun peso** attraversa gli agenti.
- **Federazione peer-only.** Ogni agente riceve **6 insight** dai 3 peer (2 per peer); mai i propri,
  mai insight di Normal (`§E`). Non c'è server iterativo che distilla una libreria globale: la
  "federazione" è single-shot, peer-only.

## A.2 Le tre condizioni

- **A — isolated:** solo esempi locali, nessun insight peer.
- **B — Federation over Text:** esempi locali + i 6 insight peer **genuini** (associazione
  `observed_pattern`↔`pseudolabel` corretta).
- **E — controllo di specificità/corruzione:** **gli stessi 6 insight** di B (stessi ID, stesso
  ordine, stesso `source_agent`, stesso `evidence_scope`, **stesso testo**), con **solo** il campo
  `pseudolabel` permutato secondo un **derangement frozen a zero punti fissi** (`§F`;
  `FINAL_INSIGHT_GENERATION_REPORT.md`: Zero fixed point PASS, Character equivalence PASS).
  [INTERPRETAZIONE] **E non è rumore casuale**: è il *medesimo* testo con la stessa quantità e
  struttura di informazione, in cui è stata corrotta **solo l'associazione semantica** testo→classe.
  Va descritto esattamente così (label-association derangement), non come "shuffled/random noise".

## A.3 Esecuzione e statistica

- **LLM:** provider OpenAI, modello richiesto/restituito `gpt-5.6-terra`, reasoning effort `medium`,
  **temperature/seed = null** (non supportati dal path provider), Structured Outputs strict.
  R=3 ripetizioni per ogni agente-caso-condizione; aggregazione = **maggioranza 2-su-3** su label
  valida, altrimenti **abstention** (contata come *incorrect* nella primaria). 540 record
  individuali → 180 aggregati. Token totali 1,207,146. [INTERPRETAZIONE] un solo modello,
  proprietario, non deterministico e con nome inusuale: punto di attacco per il Reviewer D.
- **Unità statistica:** **12 fault-run fisici indipendenti** (4 pseudoclassi × 3 run); ogni run è
  unseen per 3 agenti ⇒ **36 osservazioni agent-case correlate** per condizione. Held-out totale =
  15 casi (12 guasti + 3 Normal); overall = 60 = 15×4 agenti. Bootstrap **cluster-pairato**, 10.000
  draws, seed `20260829`, ricampionando `physical_case_id` entro 4 strati.

## A.4 Risultati frozen (verificati in `EVALUATION_REPORT.md`)

**Primaria — classi localmente non viste:**

| Condizione | Corretti / n | Accuracy | Abstention |
|---|---:|---:|---:|
| A — isolated | 0 / 36 | 0.00% | 14 |
| B — FoT | 31 / 36 | 86.11% | 0 |
| E — corrupted | 3 / 36 | 8.33% | 0 |

- **B−A = +0.8611** (contrasto primario pre-registrato, H1). Positivo per **4/4** agenti
  (+1.00, +1.00, +0.667, +0.778). **Helped 31, harmed 0, unchanged 5** (tutti e 5 scorretti).
- **B−E = +0.7778** (contrasto di **specificità/meccanicistico** pre-registrato, H3/C4). **Non è
  l'endpoint primario.**
- **E−A = +0.0833.**
- Bootstrap 95% CI: **B−A [0.833, 0.917]**, **B−E [0.722, 0.833]**.
- Criteri pre-registrati C1–C4: **4/4 PASS**.

**Secondarie (preservazione), stessi record frozen:**

| Sottoinsieme | A | B | E |
|---|---:|---:|---:|
| Local-fault-seen (12) | 100% | 100% | 100% |
| Normal (12) | 100% | 100% | 100% |
| Overall (60) | 40.00% (23.3% abst.) | 91.67% (0% abst.) | 45.00% (0% abst.) |

**Caratterizzazione descrittiva del floor di A (post-hoc, non ripunteggio):** su 36 unseen, A ha
14 astensioni e 22 predizioni committed, di cui **0/22 corrette**; a livello di ripetizione (108
tentativi) 78 riconoscono l'anomalia ma dichiarano di non poterla mappare; **zero** falsi "Normal".
[INTERPRETAZIONE] A è *information-deprived*, non malfunzionante (seen-fault 12/12, Normal 12/12).

## A.5 Cosa il repository dichiara di NON dimostrare (vincolante)

[FATTO — REPO, `FOT_TEP_POC_FINAL_SYNTHESIS §5`, `LLM_REFERENCE "Do not claim"`]: **non** "+86 punti
in generale" (baseline a floor); **non** assenza di negative transfer (harmed=0 è aritmetico, A non
ha casi unseen corretti da peggiorare); **non** generalizzazione (12 run, un simulatore, un mode, 4
guasti, un LLM); **non** "il verbalizer classifica"; **non** privacy formale; **non** superiorità
dimostrata su central-ICL (questione aperta). Questa disciplina di claim è già scritta nel repo:
il paper deve ereditarla.

---

# PARTE B — FoT ORIGINALE (Yao et al. 2026) E CONFRONTO PUNTO-PER-PUNTO

**FoT NON è stato inventato da noi.** [EVIDENZA — LETTERATURA] Ricostruzione dalla fonte primaria
(arXiv:2604.16778v2).

## B.1 Cosa è FoT (Yao et al.)

- **Problema.** Trasferire/riusare/distillare tracce di ragionamento indipendenti tra agenti che
  risolvono task **diversi ma correlati**, costruendo una **insight library** condivisa ed evolutiva.
  Motivazione: (i) ragionamento inefficiente (ripetuto da zero); (ii) ragionamento isolato non
  riusabile tra agenti.
- **Architettura.** **Iterativa, multi-round, con server** (fisico o logico). Ad ogni round: ogni
  client esegue un LLM locale che risolve il proprio task e fa *self-improvement*, genera **tracce
  di ragionamento metacognitive** (linguaggio naturale), le carica al server; il server **clusterizza
  e distilla** frammenti ricorrenti in insight espliciti → aggiorna la **insight library** →
  la ridistribuisce a tutti per il round successivo (Algorithm 2).
- **Oggetto scambiato.** **Reasoning traces / insight astratti in linguaggio naturale.** Non raw
  problem instances, non gradienti, non pesi.
- **Agenti / eterogeneità.** Agenti decentralizzati su **task/domini diversi** (8 agenti = 8 dataset
  di matematica; multi-dominio math/QA/coding/HLE; daily tasks; paper di ricerca). L'eterogeneità è
  **cross-task / cross-domain**, non non-IID di classi entro un unico task di classificazione.
- **Ruolo del server.** Aggregatore che distilla via prompt curati; broadcast della libreria.
- **Task/dataset.** AIME24/25, AMC, CCEE, CNMO, WLPMC, LiveMathBench; GPQA(-diamond), LiveCodeBench,
  Humanity's Last Exam; PinchBench/OpenClaw (daily tasks); ICLR papers (insight discovery).
- **Base LLM.** DeepSeek-R1-Distill-Qwen-7B, Gemini 3.0 Pro, Gemini 2.5 Flash Lite, Qwen2.5-7B.
- **Evaluation.** +25% score medio con −4% reasoning token (prime 3 applicazioni); insight library
  copre **>80%** dei contributi dei paper ICLR successivi.
- **Ablation.** local reasoning strategies (§6.1), server aggregation (§6.2), **modelli LLM
  eterogenei** (§6.3), library size (§6.4), agent participation include/exclude-one (§6.5),
  transferability a modelli/task nuovi (weak-to-strong nel text space, Tab. 4–5).
- **Privacy.** *Safeguarding raw problem instances*: le tracce astratte non contengono il problema
  originale; **prompt-stealing attacker → token-level F1 < 0.25**; **nessun PII**; la libreria non
  contiene le risposte (Jaccard 4-gram ≈ 0). **Non** è privacy formale/DP.
- **Limiti dichiarati.** personalization e distribution drift tra agenti = future work;
  propagazione di allucinazioni negli insight = rischio aperto.

## B.2 Confronto punto-per-punto e "cosa aggiungiamo"

| Dimensione | FoT originale (Yao et al.) | Il nostro esperimento (TEP) |
|---|---|---|
| Dominio | Reasoning testuale (math, QA, coding, ricerca) | **Serie temporali multivariate / diagnosi guasti industriali** |
| Interfaccia dato→testo | Nessuna (task già testuali) | **Verbalizer deterministico TS→evidence→neutral text** |
| Eterogeneità | Cross-task / cross-domain | **Non-IID class-disjoint (Normal + 1 guasto; 3 unseen)** |
| Round / server | Multi-round iterativo, server distillante | **Single-shot, peer-only, senza libreria globale evolutiva** |
| Oggetto scambiato | Reasoning traces → insight (NL) | Insight (NL) con `pseudolabel` opaca + evidence scope |
| Endpoint | Accuracy ↑, token ↓, coverage insight | **Riconoscimento di classi localmente non viste (B−A)** |
| Controllo di specificità | Ablation (aggregation, library size…) | **B vs E: derangement pre-registrato delle associazioni** |
| Anti-leakage di valutazione | Argomento di privacy sull'input | **Pseudolabel opache + freeze chain + held-out guard** |
| Privacy | Analisi empirica di leakage (F1<0.25) | Solo *no raw-data exchange* (più debole di FoT) |

**Domanda centrale — cosa stabiliamo che FoT non stabiliva già?**
[INTERPRETAZIONE] Tre cose, tutte *modeste ma reali*:
1. **Applicabilità a un dominio non-testuale (serie temporali multivariate) tramite
   verbalizzazione deterministica** — FoT assume task nativamente testuali; noi mostriamo che il
   meccanismo FoT-like funziona quando l'evidenza è un'interfaccia testuale deterministica su segnali.
2. **Un tipo di eterogeneità diverso e più "FL-classico": non-IID class-disjoint con classi
   localmente non viste** — FoT non studia questo; è precisamente il caso che i reviewer FL
   riconoscono (label subset skew estremo).
3. **Un controllo di specificità semantica pre-registrato (B−E)** che isola la *correttezza
   dell'associazione* dal *volume di testo* — non ho identificato questo controllo, in questa forma,
   applicato a FoT/federated distillation su questo problema.

**Cosa FoT fa e noi NON facciamo:** multi-round con libreria evolutiva; self-improvement loop;
aggregazione server-side distillante; scala e diversità di task; analisi di leakage quantitativa;
weak-to-strong tra modelli. **Vietato** scrivere "we propose Federation over Text": FoT è di Yao
et al. Corretto: *"we adapt/apply FoT (Yao et al., 2026) to…"* e *"we contribute a controlled
evaluation…"*.

---

# PARTE C — È DAVVERO "FEDERATED LEARNING"? (Domanda critica n.1)

[INTERPRETAZIONE + EVIDENZA] Sezione **descrittiva, non apologetica**.

## C.1 Cosa fa il nostro sistema, letteralmente

Non federa osservazioni grezze; non aggrega gradienti; non aggrega pesi; scambia **conoscenza
testuale derivata localmente**; agenti con esperienza locale eterogenea; un agente beneficia
dell'esperienza altrui su classi mai viste localmente. In termini ML: è **in-context learning
federato** dove l'oggetto condiviso è testo distillato peer-generato, single-round.

## C.2 La linea concettuale dell'"oggetto federato"

`parameter/gradient federation` (FedAvg, FedProx, SCAFFOLD, FedNova)
→ `knowledge-distillation federation / logit exchange` (FedMD, FedDF, FedGKT)
→ `prototype/representation federation` (FedProto)
→ `synthetic-knowledge / data-free federation` (FedGen; Social Learning)
→ `foundation-model / parameter-efficient federation` (Time-FFM, FedCoT, federated LoRA/prompt)
→ `textual / semantic knowledge federation` (**FoT**, Federated In-Context LLM Agent Learning, *noi*).

[INTERPRETAZIONE] FoT — e il nostro esperimento — si collocano all'**estremo semantico** di questa
linea: l'oggetto federato è **linguaggio naturale interpretabile**, non un tensore. Esiste dunque un
precedente terminologico: già FedMD/FedDF hanno spostato l'"oggetto federato" da pesi a logit; già
FedProto a prototipi; FedGen a conoscenza sintetica. Chiamare "federato" lo scambio di conoscenza
non-parametrica **ha basi in letteratura**. Ma:

## C.3 Verdetto onesto

[INTERPRETAZIONE] Definire il lavoro **"Federated Learning" senza qualificatori è debole** per tre
motivi: (i) non c'è *learning* nel senso di ottimizzazione iterativa di un modello condiviso — c'è
inferenza/ICL; (ii) è single-round, senza aggregazione di modello; (iii) gli **stessi autori di FoT**
lo chiamano *"federated learning-like"*. Il termine **difendibile e accurato** è **"federated
knowledge transfer"** / **"federated (textual) knowledge sharing"** / **"collaborative distributed
learning"**. "Federated reasoning" è accettabile ma enfatizza l'LLM più del transfer. Vedi OUTPUT 5.

---

# PARTE D — I SETTE FILONI (sintesi della letteratura)

Legenda classe di rilevanza: **DC** = direct competitor · **PRED** = close methodological
predecessor · **ADJ** = adjacent · **BG** = background · **NR** = not actually relevant.
Per ogni metodo: cosa resta locale / cosa si scambia / dati pubblici richiesti / omogeneità
architetturale / non-IID / privacy / costo comunicazione / output. `not reported` dove non noto.

## Filone 1 — Foundational Federated Learning (BG)

Necessari **solo** per inquadrare il problema che FoT-like *evita*: statistical heterogeneity,
client drift, comunicazione.

- **FedAvg** (McMahan et al., AISTATS 2017) — media pesata dei **pesi** dopo training locale.
  Locale: dati. Scambiato: pesi/aggiornamenti. Omogeneità architetturale: **sì**. non-IID: degrada,
  motivazione originaria. Privacy: nessuna formale (solo data locality). BG.
- **FedProx** (Li et al., MLSys 2020) — termine prossimale contro client drift sotto eterogeneità.
  BG.
- **SCAFFOLD** (Karimireddy et al., ICML 2020) — control variates per correggere il drift non-IID. BG.
- **FedNova** (Wang et al., NeurIPS 2020) — normalizzazione degli update con lavoro locale
  eterogeneo. BG.
- *Personalized FL* (pFedMe, Ditto, ecc.) — modelli personalizzati per client. ADJ/BG: rilevante
  perché il nostro è intrinsecamente *personalizzato* (ogni agente resta specializzato; la
  federazione non crea un modello globale).

[INTERPRETAZIONE] Uso in Related Work: **una frase** che dice "FL classico aggrega parametri sotto
non-IID (FedAvg…SCAFFOLD); noi non aggreghiamo parametri". Non serve una storia del FL.

## Filone 2 — Federated Knowledge Distillation / Knowledge Transfer (PRED — sezione centrale)

**È il vero predecessore metodologico**, più del FedAvg. Sposta l'oggetto federato da pesi a
conoscenza.

- **FedMD** (Li & Wang, NeurIPS'19 WS; arXiv:1910.03581) — **DC/PRED**. Locale: modello+dati privati.
  Scambiato: **logit** su un **public dataset** condiviso. Omogeneità: **no** (model-agnostic).
  non-IID: gestito via public set. Privacy: no raw data. Output: personalizzato. *Vicino perché
  federa conoscenza (logit) non pesi; lontano perché richiede public data e scambia numeri, non testo.*
- **FedDF** (Lin et al., NeurIPS 2020; arXiv:2006.07242) — **PRED**. Ensemble distillation lato
  server su dati unlabeled/generati; fonde modelli eterogenei. Scambia modelli+usa distillation.
- **FedGKT** (He et al., NeurIPS 2020; arXiv:2007.14513) — **PRED**. Group knowledge transfer: edge
  piccoli ↔ server grande via feature/logit. Scambia feature+logit.
- **FedProto** (Tan et al., AAAI 2022; arXiv:2105.00243) — **PRED**. Scambia **prototipi** (medie di
  embedding per classe), non pesi. non-IID esplicito. *Concettualmente l'analogo "numerico" del
  nostro insight: una rappresentazione compatta per-classe. Differenza: prototipo = vettore; il
  nostro = testo con pseudolabel.*
- **FedGen** (Zhu et al., ICML 2021; arXiv:2105.10056) — **PRED**. Data-free KD: un generatore
  produce conoscenza sintetica per correggere non-IID. Scambia generatore/knowledge sintetica.
- **FedCKD** (2025/2026) — **PRED forte**. KD cross-client con dataset **label-exclusive** (classi
  disgiunte tra client). *Struttura non-IID quasi identica alla nostra*; ma parameter/logit-based,
  non testuale, non LLM, non TS.
- **One-Shot Federated Distillation Using Monoclass Teachers** — **PRED forte**. Ogni client possiede
  **una sola classe** (monoclass) → distillazione one-shot. *Analogo strutturale diretto di "Normal +
  un guasto per agente".* Non testuale, non LLM, non TS.
- *Social Learning* (Mohtashami et al., 2023; arXiv:2312.11441) — **PRED**. Agenti-insegnanti
  generano **esempi sintetici / prompt astratti in linguaggio naturale** condivisi per uno studente
  (single-task). *È il ponte tra federated distillation e testo naturale.* Citato dallo stesso FoT.

Per ogni metodo, la colonna decisiva: **cosa comunica** = logit / prototipi / feature / conoscenza
sintetica / (testo, in Social Learning). Nessuno di questi **è un LLM che ragiona su testo neutrale
di serie temporali con classi localmente non viste**. Questo è il cuore del nostro posizionamento.

## Filone 3 — Federated LLM / Foundation Model (ADJ, con 1 PRED)

- **Time-FFM** (Liu et al., NeurIPS 2024; arXiv:2405.14252; codice CityMind-Lab) — **ADJ (obbligatorio)**.
  Federated foundation model per **forecasting** di serie temporali: allinea le TS alla modalità
  linguistica via prompt, apprende un **modulo globale leggero** (transformer backbone da un LM
  pre-addestrato, parti personalizzate locali) con aggregazione **FedAvg-style**. Locale: dati TS +
  moduli personalizzati. Scambiato: **parametri** del modulo condiviso. non-IID: domini TS
  eterogenei. *Vicino: FL + foundation model + serie temporali. NON equivalente: federa **parametri**
  (non testo), fa **forecasting** (non diagnosi/classificazione), **apprende** (non ICL), nessuna
  nozione di classe localmente non vista né controllo di specificità.* È il miglior "adjacent" per
  segnalare consapevolezza del filone TS-federato.
- **FedCoT** (Chuan Li et al., 2025; arXiv:2508.10020) — **PRED/ADJ**. *Federated reasoning* per LLM:
  scambia **parametri LoRA** (+ selezione della miglior chain-of-thought via discriminatore), dati
  locali, eterogeneità via client-classifier-aware LoRA stacking; task di **medical reasoning**.
  *Vicino perché "federated reasoning con LLM"; lontano perché federa **parametri LoRA**, non testo,
  e non ha il nostro setting non-IID class-disjoint su TS.*
- **Federated fine-tuning / prompt / LoRA tuning** (survey: *A Survey on Federated Fine-tuning of
  LLMs*, arXiv:2503.12016; *When FL Meets LLMs*, CMC 2025; personalized federated prompt learning,
  arXiv:2501.13904) — **ADJ/BG**. Federano adapter/prompt **parametrici**. Utili per la linea
  concettuale; non testuali.

[INTERPRETAZIONE] Cercato un lavoro **più vicino di Time-FFM**: il più vicino sull'asse
"FL+foundation+TS" resta Time-FFM (parametrico); sull'asse "FL+testo+LLM" i più vicini sono FoT e
Federated In-Context LLM Agent Learning (Filone 4). Non ho identificato un lavoro che unisca
*foundation-model federation + serie temporali + scambio testuale + classi non viste*.

## Filone 4 — Textual / Semantic Knowledge Exchange & Multi-Agent LLM (DC/PRED)

- **Federation over Text** (Yao et al., 2026; arXiv:2604.16778) — **DC (il metodo)**. Vedi Parte B.
- **Federated In-Context LLM Agent Learning** (arXiv:2412.08054, 2024) — **DC/PRED**. Scambia
  **"knowledge compendiums"** e rappresentazioni in **linguaggio naturale** generate da un modulo
  LLM (KCG); **dati grezzi locali**; forte riduzione di comunicazione; eterogeneità dei dati citata.
  *Il vicino più pericoloso per la novelty "textual federation": federazione LLM di conoscenza NL,
  non parametri.* Non tratta TS, non tratta diagnosi guasti, non ha il controllo di specificità né
  classi localmente non viste. **Da citare e distinguere esplicitamente.**
- *ExpeL* (Zhao et al., AAAI 2024) — **ADJ/PRED**. Agenti LLM come *experiential learners*: estraggono
  esperienze/insight testuali da traiettorie passate. Single-agent memory, non federazione tra pari.
- *Metacognitive Reuse* (Didolkar et al., 2025; arXiv:2509.13237) — **ADJ**. Trasforma reasoning
  ricorrente in "behaviors" concisi riusabili. Base locale di FoT; non federazione.
- *Agentic Context Engineering (ACE)*, *HyperAgents*, *Evolving Prompts in-context* (ICML 2025) —
  **ADJ/BG**. Auto-miglioramento testuale/di contesto di agenti; possibili "local reasoning" dentro FoT.
- *Multi-agent memory/experience sharing* in generale — **ADJ**. Condividono memoria/esperienza
  testuale ma tipicamente **non** in setting non-IID class-disjoint con held-out e controllo di
  specificità.

[INTERPRETAZIONE] Questo filone è dove la novelty è **più minacciata**: la combinazione
"agenti + scambio di conoscenza in linguaggio naturale + dati locali" è già occupata da FoT e da
Federated In-Context LLM Agent Learning. La nostra difesa è *dominio + tipo di non-IID + controllo*.

## Filone 5 — Non-IID knowledge / experience (PRED/BG per il framing)

Non solo *class proportion skew*, ma **client con esperienza di classe asimmetrica / non
sovrapposta**.

- Tassonomia non-IID (Zhu et al., *FL on non-IID data: a survey*, Neurocomputing 2021; Li et al.,
  *FL on non-IID Data Silos: An Experimental Study*, ICDE 2022/arXiv:2102.02079; Kairouz et al.,
  *Advances and Open Problems in FL*, 2021) — **BG**. Definiscono *label distribution skew*, *label
  subset skew* (partizione `#C=k`: ogni client vede solo k classi), *feature skew*, *quantity skew*.
- **Partially Class-Disjoint Data (PCDD)** (arXiv:2405.18972, 2024) — **PRED (terminologia)**. Nomina
  esattamente il regime "client con classi parzialmente disgiunte".
- *Federated few-shot / cross-client transfer* (es. Industrial Edge Intelligence: Federated-Meta
  few-shot fault diagnosis) — **ADJ**. Trasferimento tra client con classi scarse/nuove.
- *Federated zero-shot learning with mid-level semantic knowledge transfer* (Pattern Recognition
  2024) — **PRED forte (semantico)**. FL + **trasferimento semantico** verso classi **non viste**.
  *Vicino: "semantic knowledge transfer + unseen classes + FL". Lontano: usa attributi ZSL classici,
  non testo LLM, non TS, non insight peer-generati.*

**Quanto è inusuale la nostra struttura "Normal + un guasto locale, altri guasti unseen"?**
[INTERPRETAZIONE] È un caso **estremo ma non inedito** di *label subset skew* / *class-disjoint*
(vicino a "monoclass + Normal"). Il termine tassonomico corretto è **class-disjoint / label-subset
skew estremo (missing-class heterogeneity)**, non "pathological non-IID" generico. Vedi OUTPUT
terminologia non-IID.

## Filone 6 — Federated Time-Series / Fault Diagnosis (ADJ — contesto di confronto)

Cosa confronterebbe un reviewer di diagnosi guasti federata.

- **Deep Anomaly Detection for TS in Industrial IoT: Communication-Efficient On-Device FL** (Liu et
  al., IEEE IoT-J 2020) — **ADJ**. Canonico: FedAvg on-device su TS, anomaly detection. Federa
  **pesi**. Nessuna classe localmente non vista trasferita via testo.
- **Federated (fuzzy fusion) fault diagnosis di processi chimici** (PubMed 42281064) — **ADJ**. FL su
  processo chimico, aggregazione di regole/modelli.
- **A federated learning approach to mixed fault diagnosis in rotating machinery** (ScienceDirect,
  2023) — **ADJ**. FL parametrico su macchine rotanti.
- **Industrial Edge Intelligence: Federated-Meta Learning for Few-Shot Fault Diagnosis** — **ADJ**.
  Meta-learning federato per pochi campioni / nuovi guasti; parametrico.
- **TEP** in letteratura è quasi sempre usato in setting **centralizzati** (autoencoder, deep FDD,
  interpretable knowledge discovery). Non ho identificato un lavoro che faccia **FoT/textual
  federated knowledge transfer su TEP**.

Regola: **non confrontare accuracy tra task diversi** come se fossero equivalenti (i nostri 86.11%
su unseen non sono comparabili con l'accuracy di un classificatore FedAvg su tutte le classi).

Per ciascuno: dataset (machinery/chemical/TEP), task (FDD/anomaly), costruzione client (per
macchina/sito), non-IID (per lo più feature/quantity skew), modello (CNN/AE/…), meccanismo
(FedAvg/param), raw-data policy (locale), evaluation (accuracy/F1 su tutte le classi), comunicazione
(pesi), **studio del transfer di guasti localmente non visti: raramente/no**.

## Filone 7 — Verbalizer TS→text (BG SECONDARIO, spazio proporzionato)

Il paper **non** va posizionato come nuovo verbalizer. Questa letteratura serve solo a giustificare
che *un'interfaccia testuale deterministica e diagnosis-neutral è una scelta sperimentale legittima*.

- **T2SP** — Kim, Oh, Lee, Rish, Lee, *Representing Time Series as Structured Programs for LLM
  Reasoning*, arXiv:2606.12481, giu 2026 — **BG chiave**. Rappresentazione **deterministica,
  training-free** di TS come programma strutturato per il reasoning LLM. **Prova che le
  rappresentazioni strutturate deterministiche TS→LLM sono già una direzione attiva.** ⇒ **vietato**
  claim "introduciamo la rappresentazione deterministica di TS per LLM".
- **TRUCE** — Jhamtani & Berg-Kirkpatrick, *Truth-Conditional Captioning of Time Series Data*,
  EMNLP 2021 Findings (arXiv:2110.01839) — **BG**. Captioning *truth-conditional*: esegue programmi
  sulla serie e condiziona il testo solo sui pattern veri. Predecessore diretto dell'idea "testo
  fattuale, non allucinato".
- **FD-LLM (Qaid et al., 2024, arXiv:2412.01218)** e **FD-LLM (Lin et al., Adv. Eng. Informatics
  2025)** — **BG**. LLM/MM-LLM per diagnosi guasti da dati time-series (serializzazione / modal
  alignment / LoRA). Mostrano l'interesse per LLM+FDD; **centralizzati**, non federati.
- **ESAX+BoW** (Zhao et al., IEEE TIM 2022) e **SAX_HAR-LLM** (Pappa et al., ESWA 2026) — **BG**.
  Rappresentazioni simboliche (SAX/ESAX) di TS per FDD/HAR e per LLM. Precedenti sulla
  simbolizzazione.

[INTERPRETAZIONE] In 10 pagine, questo filone merita **≤1 breve paragrafo** con T2SP e TRUCE come
ancore ("evidence interface deterministica, diagnosis-neutral, coerente con T2SP/TRUCE"), citando
FD-LLM come contesto LLM+FDD.

---

# PARTE E — MATRICE COMPARATIVA PRINCIPALE

[INTERPRETAZIONE metodologica] La matrice richiesta ha ~26 colonne: in Markdown/IEEE 2-col non è
leggibile su una riga. La rendo in **due viste**: (E.1) una tabella sintetica ad alta densità sui
campi discriminanti; (E.2) schede compatte che coprono **tutti** i campi richiesti per i lavori
più rilevanti. Celle ignote = `n/r` (not reported).

## E.1 Tabella sintetica (assi discriminanti)

Colonne: paradigma; **Oggetto scambiato** (Raw/Grad/Param/Logit/Proto/Synth/**Text**); FM=foundation
model coinvolto; TS=serie temporali; FDD=fault/industrial; non-IID; Privacy formale; Classe.

| # | Lavoro (anno, venue) | Paradigma | Scambiato | FM | TS | FDD | non-IID | Priv.form. | Classe |
|---|---|---|---|:--:|:--:|:--:|---|:--:|:--:|
| 1 | FoT — Yao et al. 2026 (arXiv preprint) | FL-like knowledge fed. | **Text** (insight) | sì | no | no | cross-task | no | **DC** |
| 2 | Federated In-Context LLM Agent Learning 2024 (arXiv) | FL LLM knowledge | **Text** (compendium) | sì | no | no | data heterog. | no | **DC/PRED** |
| 3 | Social Learning 2023 (arXiv) | collab. LLM | **Text**/synth ex. | sì | no | no | single-task | no | PRED |
| 4 | FedCoT 2025 (arXiv) | federated reasoning | Param (LoRA)+CoT | sì | no | no | client-aware | no | PRED/ADJ |
| 5 | Time-FFM 2024 (NeurIPS) | federated FM | Param (module) | sì | **sì** | no | domini TS | no | ADJ |
| 6 | FedMD 2019 (NeurIPS WS) | fed. distillation | Logit (public) | no | no | no | label skew | no | PRED |
| 7 | FedDF 2020 (NeurIPS) | ensemble distill. | Model+distill | no | no | no | eterogeneo | no | PRED |
| 8 | FedGKT 2020 (NeurIPS) | group KT | Feature+logit | no | no | no | edge | no | PRED |
| 9 | FedProto 2022 (AAAI) | prototype fed. | **Prototipi** | no | no | no | sì (esplicito) | no | PRED |
| 10 | FedGen 2021 (ICML) | data-free KD | Synth knowledge | no | no | no | sì | no | PRED |
| 11 | FedCKD 2025/26 | cross-client KD | Logit/param | no | no | no | **label-exclusive** | no | PRED |
| 12 | Monoclass / one-shot fed. distillation (regime; preprint non verif.) | one-shot distill. | Distill/param | no | no | no | **monoclass** | no | PRED (regime) |
| 13 | Fed. zero-shot, mid-level semantic transfer 2024 (Pattern Recog.) | FL ZSL | **Semantic attr.** | no | no | no | **unseen classes** | no | PRED |
| 14 | PCDD — Bilateral Curation 2024 (arXiv) | FL non-IID | Param | no | no | no | **class-disjoint** | no | BG/PRED |
| 15 | FedAvg 2017 (AISTATS) | FL param | **Param** | no | no | no | (degrada) | no | BG |
| 16 | FedProx 2020 (MLSys) | FL param | Param | no | no | no | sì | no | BG |
| 17 | SCAFFOLD 2020 (ICML) | FL param | Param+ctrl var | no | no | no | sì | no | BG |
| 18 | Deep Anomaly Det. TS IIoT (FL) 2020 (IEEE IoT-J) | FL param | **Param** | no | **sì** | anomaly | feature/qty | no | ADJ |
| 19 | FL fault diag. rotating machinery 2023 (Elsevier) | FL param | Param | no | **sì** | **sì** | per-macchina | no | ADJ |
| 20 | Federated-Meta few-shot fault diagnosis | fed. meta-learn | Param | no | **sì** | **sì** | few-shot/new | no | ADJ |
| 21 | T2SP 2026 (arXiv) | TS→program repr. | — (repr.) | uses LLM | **sì** | no | n/a | no | BG |
| 22 | TRUCE 2021 (EMNLP) | TS captioning | — (repr.) | no | **sì** | no | n/a | no | BG |
| 23 | FD-LLM (Qaid 2024; Lin 2025) | LLM FDD (central) | — (central) | sì | **sì** | **sì** | n/a | no | BG |
| — | **NOSTRO (TEP FoT)** | **FL-like textual KT** | **Text (insight+pseudolabel)** | sì | **sì** | **sì** | **class-disjoint/unseen** | **no** | — |

## E.2 Schede compatte (campi completi) per i lavori-chiave

Ogni scheda: *problema · cosa resta locale · cosa si scambia · raw? param? grad? logit? proto?
synth? text? · FM? · TS? · FDD? · inferenza personalizzata/globale · privacy formale · comunicazione
· evidenza sperimentale principale · similarità col nostro · differenza critica · classe · indebolisce
una nostra claim? come?*

**S1. FoT (Yao et al. 2026).** Trasferimento di reasoning tra agenti cross-task · locale: problemi
grezzi + LLM · scambia: **insight testuali** · raw no, param no, grad no, logit no, proto no, synth
no, **text sì** · FM sì · TS no · FDD no · inferenza personalizzata (task diversi) · privacy formale
no (leakage empirico) · comunicazione: testo compatto multi-round · evidenza: +25% score, −4% token,
>80% coverage · **similarità: è il metodo** · **differenza: dominio, non-IID class-disjoint,
single-round, controllo E** · **DC** · *Indebolisce:* la claim "proponiamo FoT" (fatale) e
"prima federazione testuale" (già loro).

**S2. Federated In-Context LLM Agent Learning (2412.08054, 2024).** FL LLM con scarsità di dati
sensibili · locale: dati grezzi · scambia: **knowledge compendiums (NL)** · **text sì**, param no,
grad no · FM sì · TS no · FDD no · inferenza per-client · privacy formale no (data locality) ·
comunicazione: −3.3×10⁵ costo · evidenza: performance competitiva vs SOTA · **similarità: federazione
LLM di conoscenza NL, dati locali** · **differenza: no TS, no FDD, no classi unseen, no controllo di
specificità** · **DC/PRED** · *Indebolisce:* "prima federazione di conoscenza testuale con dati locali".

**S3. FedProto (AAAI 2022).** FL eterogeneo via prototipi · locale: modello+dati · scambia:
**prototipi** (media embedding/classe) · proto sì, param no · FM no · TS no · FDD no · personalizzato
· privacy no · comunicazione: piccola (prototipi) · evidenza: robustezza non-IID · **similarità:
rappresentazione compatta per-classe federata (analogo numerico dell'insight)** · **differenza:
vettore vs testo, no LLM/ICL, no unseen-transfer, no TS** · **PRED** · *Indebolisce:* "federare
rappresentazioni per-classe è nuovo" (no).

**S4. FedCKD (label-exclusive) & S5. Monoclass Teachers.** Cross-client KD con classi disgiunte /
un client-una classe · scambia: logit/distillazione · FM no · TS no · FDD no · **non-IID
class-disjoint/monoclass** identico alla nostra struttura · **PRED forti** · *Indebolisce:* "la
struttura non-IID class-disjoint è nuova" (no — è nota; nostra novità è farlo via **testo/LLM su TS**).

**S6. Time-FFM (NeurIPS 2024).** Federated foundation model per forecasting TS · scambia: **parametri**
del modulo condiviso · FM sì · **TS sì** · FDD no (forecasting) · non-IID: domini TS · **ADJ
obbligatorio** · *Indebolisce:* "primo foundation-model federato su TS" (no — ma loro forecasting
parametrico, noi diagnosi testuale). Non intacca il nostro core.

**S7. Fed. zero-shot mid-level semantic transfer (Pattern Recognition 2024).** FL + trasferimento
**semantico** a classi **non viste** · scambia attributi semantici · FM no · TS no · **PRED forte** ·
*Indebolisce:* "trasferire conoscenza semantica a classi non viste in FL è nuovo" (no — nostra
differenza: linguaggio naturale LLM-mediato + TS + insight peer-generati vs attributi ZSL fissi).

---

# PARTE F — NEAREST-NEIGHBOR ANALYSIS (Top 5)

Per ciascuno: (1) cosa fanno; (2) perché vicini; (3) cosa facciamo noi che loro no; (4) cosa fanno
loro che noi no; (5) quale nostra claim impediscono; (6) quale claim resta possibile.

**N1 — Federation over Text (Yao et al. 2026).** (1) Federazione multi-round di insight testuali tra
agenti cross-task, server distillante. (2) È il metodo che applichiamo; identità di paradigma. (3)
Lo portiamo su **serie temporali multivariate** via verbalizzazione deterministica, in **non-IID
class-disjoint**, con **controllo di specificità B−E**. (4) Multi-round, libreria evolutiva,
self-improvement, scala/varietà di task, leakage quantitativo, weak-to-strong. (5) Impedisce
qualsiasi claim di **invenzione del metodo** ("we propose FoT"). (6) Resta possibile: *"prima
applicazione controllata di FoT a diagnosi TS multivariata sotto esperienza non-IID class-disjoint,
con controllo di specificità"*.

**N2 — Federated In-Context LLM Agent Learning (2024).** (1) FL che scambia knowledge compendiums in
NL, dati locali, super-efficiente. (2) Stesso oggetto federato (testo NL da LLM), dati locali. (3)
Dominio TS/FDD, classi localmente non viste, controllo E, pseudolabel opache anti-leakage. (4)
Efficienza di comunicazione quantificata, framework generale. (5) Impedisce "**primo** a federare
conoscenza testuale con dati locali via LLM". (6) Resta: *"applicazione a TS diagnosis con
valutazione controllata del transfer su classi non viste"*.

**N3 — FedCKD (label-exclusive KD).** (1) KD cross-client con dataset a classi esclusive. (2)
Struttura non-IID (classi disgiunte) quasi identica. (3) Facciamo transfer **testuale LLM** (non
logit/param) su **TS**, con classi *mai viste localmente* riconosciute a inferenza. (4) Training
distillativo con aggregazione parametrica; scala maggiore. (5) Impedisce "**la struttura
class-disjoint è la novità**". (6) Resta: *"l'oggetto federato è testo interpretabile e il transfer
avviene in ICL, non via parametri"*.

**N4 — FedMeta-FFD (Chen, Tang, Li, IEEE TNSE 2023; DOI 10.1109/tnse.2023.3266942).** (1) Federated
meta-learning per few-shot fault diagnosis: un global meta-learner si adatta rapidamente a un client
nuovo o a una **categoria di guasto mai incontrata** con pochi esempi etichettati. (2) Vicino perché
è FL + diagnosi guasti + **nuove categorie di guasto cross-client** — il neighbor FDD più diretto.
(3) Noi riconosciamo guasti **mai visti localmente senza alcun esempio etichettato della classe**,
via **testo peer LLM** (non parametri) e senza aggregare un modello. (4) Loro: meta-learner globale
parametrico, richiede *alcuni* esempi della nuova classe, convergenza analizzata. (5) Impedisce
"**primo trasferimento cross-client verso nuove classi di guasto**". (6) Resta: *nessun esempio della
classe unseen + oggetto testuale + nessun modello aggregato*. *(N.B.: un preprint affine "one-shot
federated distillation with monoclass teachers", HAL, resta non verificato in cataloghi indicizzati;
il punto strutturale "un client–una classe" è comunque coperto, verificato, da FedCKD — vedi N3.)*

**N5 — Federated zero-shot, mid-level semantic knowledge transfer (2024).** (1) FL che trasferisce
conoscenza **semantica** per riconoscere classi **non viste**. (2) Combinazione "FL + semantica +
unseen classes". (3) La "semantica" è **linguaggio naturale generato/ragionato da LLM** e il dominio
è **TS diagnosi**, con controllo di corruzione delle associazioni. (4) Formalismo ZSL, attributi
strutturati. (5) Impedisce "**primo transfer semantico a classi non viste in FL**". (6) Resta:
*trasferimento via testo LLM peer-generato, non attributi ZSL predefiniti; su TS; con B−E*.

**Sintesi nearest-neighbor.** [INTERPRETAZIONE] Ogni singolo asse del nostro lavoro ha un vicino
stretto. **Nessuno dei cinque** combina *TS multivariate + LLM/ICL + scambio testuale + classi
localmente non viste + no raw-data + controllo di specificità*. La novelty vive **nell'intersezione
e nel disegno di valutazione**, non nei singoli componenti.

---

# PARTE G — NOVELTY RED TEAM (tentativo di falsificazione)

**Obiettivo dichiarato:** *falsificare* la novelty. Ho cercato un lavoro che combini tutti gli assi:
`non-IID agents` + `time-series data` + `LLM reasoning` + `natural-language knowledge exchange` +
`locally unseen conditions` + `no raw-data exchange`.

**Ricerca a criteri pieni.** Query su IEEE/arXiv/OpenAlex/Scopus/Semantic Scholar per combinazioni
di questi termini. **Esito:** *I did not identify an equivalent method in the literature searched.*
(Non affermo che non esista.)

**Rilassamento progressivo dei criteri (i più vicini che emergono):**
- Tolgo *time-series* → **FoT** e **Federated In-Context LLM Agent Learning** (federazione testuale
  LLM, non-IID/eterogeneo, dati locali). Equivalenti sul paradigma, non sul dominio.
- Tolgo *LLM/testo* → **FedCKD**, **Monoclass Teachers**, **Fed. ZSL semantic transfer** (non-IID
  class-disjoint / unseen, transfer di conoscenza non-parametrica). Equivalenti sulla struttura
  non-IID e sull'idea di transfer a classi non viste, non sull'oggetto testuale/LLM.
- Tolgo *unseen classes* → **Time-FFM** (FL + FM + TS, parametrico).
- Tengo *time-series + FDD + LLM*, tolgo *federazione* → **FD-LLM (2024/2025)** (LLM per FDD,
  centralizzati).

**Verdetto novelty.** [INTERPRETAZIONE] La novelty **non è component-level**. È una **novelty di
combinazione + dominio + evaluation design**. È reale ma **stretta**: difendibile solo se il paper
(a) attribuisce FoT a Yao et al., (b) posiziona la combinazione e il controllo B−E come contributo,
(c) non rivendica primati sui singoli assi. Formula sicura da usare nel paper:
> *"To the best of our knowledge, we did not identify a prior method that federates locally-derived
> textual knowledge across agents with class-disjoint temporal experience to recognize locally
> unseen fault conditions, under a preregistered semantic-specificity control."*
Mai *"no such method exists"*.

---

# PARTE H — NOVELTY A LIVELLI

- **Component novelty — bassa.** Verbalizzazione deterministica (T2SP/TRUCE), insight testuali (FoT,
  ExpeL), federazione non-parametrica (FedMD/FedProto), non-IID class-disjoint (FedCKD/monoclass),
  transfer a classi non viste (Fed. ZSL): **tutti noti singolarmente**.
- **Combination novelty — moderata.** L'unione *testo-LLM + TS multivariate + class-disjoint +
  unseen + no-raw* non l'ho trovata combinata. **È il livello più difendibile.**
- **Evaluation novelty — moderata/alta (il pezzo migliore).** Il disegno **A/B/E con derangement
  pre-registrato** e la disciplina di freeze/held-out/pseudolabel sono un contributo metodologico
  concreto e trasferibile. Il controllo **B−E** (specificità semantica a parità di testo) è raro in
  questo filone.
- **Domain novelty — moderata.** Prima applicazione documentata di FoT-like a **diagnosi TS
  multivariata / TEP**. Reale ma "applicativa".
- **Methodological novelty — bassa/moderata.** La separazione `deterministic evidence → local
  reasoning → textual insight transfer` è una **composizione** di tecniche note (T2SP + FoT +
  federated distillation), resa rigorosa. Non un meccanismo nuovo.
- **Scientific-question novelty — moderata.** La domanda *"può la conoscenza testuale semantica
  abilitare il riconoscimento di guasti localmente non visti sotto esperienza temporale distribuita
  ed eterogenea?"* è, nella forma **TS + LLM-testo + controllo di specificità**, non affrontata nei
  lavori esaminati; ma varianti (FL ZSL semantic, FoT cross-task) esistono.

[RACCOMANDAZIONE] Puntare il paper su **Combination + Evaluation novelty**. Non su Component/
Methodological.

---

# PARTE I — ANALISI DEL CONTROLLO E (B vs E)

**Cosa è E** [FATTO — REPO]: stessi 6 insight di B (stesso testo, ordine, sorgente, evidence scope),
**solo** `pseudolabel` permutata via **derangement a zero punti fissi**. Quantità e struttura
dell'informazione **identiche**; cambia solo l'**associazione semantica** testo→classe.

**Analoghi in letteratura** [EVIDENZA]: è un **label-permutation / semantic-corruption control**,
famiglia dei *placebo/knowledge-shuffling controls*. Precedenti concettuali: random-label controls in
representation learning; shuffled-knowledge ablation nella federated distillation; prompt-corruption
/ counterfactual-context nei lavori LLM (es. controlli in cui il contesto è mantenuto ma reso
inconsistente). Nella federated-KD, ablazioni tipiche variano *quantità* o *fonte*; **variare solo
l'associazione semantica a parità di volume è meno comune** ed è il punto di forza.

**Può B−E essere presentato come evidenza di specificità semantica?** [INTERPRETAZIONE] **Sì, con
linguaggio calibrato.** B−E = +0.778 (CI [0.722, 0.833]) isola la variabile "correttezza
dell'associazione" tenendo fisso il "volume di testo". Linguaggio corretto:
> *"supports the interpretation that the benefit depends on the correctness of the transferred
> associations rather than on text volume"*.
**Vietato:** chiamarlo prova causale di un meccanismo più ampio di quello isolato dal controllo;
E controlla *l'associazione pseudolabel↔pattern*, **non** dimostra causalità sul processo di
reasoning in generale, né esclude altri confounder (es. l'LLM potrebbe usare i pattern anche senza
etichetta corretta in alcuni casi — infatti E=3/36 non è 0). Presentare B−E come **specificity
contrast**, non come "endpoint primario" (coerente con la gerarchia del repo).

---

# PARTE J — IL PROBLEMA DI A COME INFORMATION FLOOR

**Fatto** [REPO]: A unseen = 0/36; 14 astensioni; 22 committed; 0/22 corrette. A è competente quando
informato (seen-fault 12/12, Normal 12/12). Il floor **non** è impossibilità matematica (l'agente
*ha* il token di classe nello label space, potrebbe indovinare) né dominato dall'astensione (la
maggioranza sono committed sbagliate).

**Come la letteratura tratta i baseline "senza informazione"** [EVIDENZA]: nei setting *missing-class
/ zero-shot client* è **atteso** che un client senza esempi/semantica della classe non la riconosca;
gli *information-floor baselines* sono legittimi per definire il punto di partenza del transfer (cfr.
FL ZSL, monoclass). La critica del reviewer sarà comunque: *"il baseline è artificialmente debole
perché il ricevente non ha alcuna semantica della classe non vista"*.

**È una critica fatale?** [INTERPRETAZIONE] **No, se inquadrata correttamente; sì, se B−A è venduto
come guadagno di accuracy generale.** Il disegno è **appropriato alla RQ** ("un agente può
riconoscere una classe mai vista *solo grazie* al testo peer?"): A=0 è precisamente la condizione
"assenza di informazione", e il valore scientifico sta in **B−E** (a parità di informazione, conta la
correttezza) più che nella magnitudine di B−A. **Mitigazioni:** (i) presentare B−A come "presenza vs
assenza di informazione", non come "+86 punti"; (ii) dare centralità a B−E; (iii) riportare la
decomposizione 14/22/0; (iv) considerare la baseline a informazione equivalente (Parte K).
**Alternative di baseline che un reviewer potrebbe chiedere:** central-ICL con gli stessi insight;
"oracle textual description" della classe; un classificatore prototype/nearest-neighbor sui 697
componenti (Parte K).

---

# PARTE K — BASELINE CHE I REVIEWER POTREBBERO CHIEDERE

Classificazione pragmatica, **tenendo conto della deadline 30/09/2026 e del limite 10 pagine senza
appendice**.

**MUST HAVE prima della submission (rischio reviewer alto se assenti):**
- **Central/pooled equal-information ICL.** Un singolo agente riceve gli stessi 6 insight (o tutti gli
  8) e diagnostica. Isola *provenance distribuita vs semplice disponibilità dell'informazione*. Il
  repo lo dichiara mancante ("FoT vs central ICL = open question"). [INTERPRETAZIONE] **È l'unico
  vero must-have**: senza, il Reviewer A/B dirà che non avete mostrato che la *federazione* aggiunge
  qualcosa oltre "avere il testo". *Feasibility:* **alta** — riusa insight e prompt esistenti, poche
  chiamate LLM aggiuntive, nessun nuovo dato. Fortemente consigliato entro la deadline.

**HIGH-VALUE se fattibile:**
- **No-verbalizer / raw-numeric prompting.** Stessa pipeline ma con serie grezza serializzata invece
  del testo neutrale: mostra che l'interfaccia deterministica aiuta (difende la scelta del verbalizer
  come enabling, non come claim). Fattibilità media.
- **Classificatore non-LLM (nearest-prototype sui 697 componenti).** Mostra il gap rispetto a un
  metodo classico e contestualizza. Fattibilità alta ma **attenzione**: non è apples-to-apples col
  transfer di classi non viste (un classificatore centralizzato vede tutte le classi).

**NICE TO HAVE:**
- **Oracle textual description** della classe (upper bound del transfer testuale).
- **Un secondo LLM** (per attenuare "un solo modello"). Fattibilità media; alto valore per Reviewer D.
- **Random-insight control** (oltre a E): insight testuale casuale/irrilevante, per distinguere
  "informazione sbagliata" (E) da "nessuna informazione utile".

**NOT APPLES-TO-APPLES (non adatte alla RQ):**
- **FL parametrico (FedAvg) / federated distillation con aggregazione di modello.** Cambiano il
  paradigma: non c'è modello condiviso da aggregare. Vanno **discussi** in Related Work, non
  implementati come baseline diretta.
- Confronto diretto di accuracy con classificatori FDD centralizzati su tutte le classi.

[RACCOMANDAZIONE] **Priorità realistica entro il 30/09:** aggiungere il **central/pooled
equal-information ICL** (must) e, se il tempo lo consente, il **secondo LLM** o il **no-verbalizer**.
Il resto va discusso a parole in Limitations. Non serve una V3 del verbalizer né validazione PV.

---

# PARTE L — TERMINOLOGIA NON-IID (termine esatto)

[EVIDENZA + INTERPRETAZIONE] Nella tassonomia FL standard (Zhu 2021; Li et al. ICDE 2022; Kairouz
2021) il nostro caso — ogni client possiede Normal + 1 classe, con le altre classi assenti
localmente — è **label subset skew estremo**, equivalente alla partizione `#C=k` con k minimo, ovvero
**class-disjoint / missing-class heterogeneity** (in parte anche **partially class-disjoint data**,
PCDD). Non è semplice *label distribution skew* (proporzioni diverse), non è *feature skew*.
**Termine raccomandato nel paper:** *"class-disjoint (missing-class) label-skew heterogeneity"* —
supportato dalla tassonomia, non scelto per convenienza. Evitare "pathological non-IID" (vago) come
etichetta principale.

---

# PARTE M — BIG DATA FIT (i "V")

[INTERPRETAZIONE, senza gonfiare]:
- **Variety — rilevante.** Dati sensoristici multivariati eterogenei, esperienza locale eterogenea:
  è la "V" più difendibile.
- **Veracity — moderata.** L'interfaccia deterministica diagnosis-neutral e il controllo di
  specificità toccano l'affidabilità dell'informazione trasferita.
- **Velocity — debole/assente.** Nessuna evidenza di streaming/tempo reale nel PoC.
- **Volume — NON dimostrato.** 15 casi held-out, 12 run fisici. **Non fingere Volume.** Il TEP è
  piccolo per costruzione (banco controllato).
- **Value — moderata.** Riduzione dello scambio di dati grezzi + interpretabilità.

**Framing Big Data difendibile:** *"distributed, heterogeneous sensor/time-series knowledge under
non-IID experience"* — enfasi su **decentralized analytics + Variety/Veracity**, con Volume/Velocity
esplicitamente fuori scope del PoC. [RACCOMANDAZIONE] Nell'abstract legare al Big Data via
*distributed + heterogeneous + decentralized*, non via *large-scale/volume*.

---

# OUTPUT 2 — CONFERENCE-FIT MATRIX

Fit con i topic ufficiali della Special Session (senza gonfiare). Strength ∈ {Strong, Moderate,
Weak, Not applicable}.

| Special Session topic | Rilevanza per il nostro lavoro | Evidenza | Strength |
|---|---|---|---|
| Collaborative learning frameworks (multi-institutional) | Framework collaborativo tra 4 agenti con esperienza locale | Architettura FoT-like peer-only | **Strong** |
| Challenges under non-IID data distributions | Non-IID class-disjoint estremo, transfer a classi non viste | A/B/E, 4 agenti missing-class | **Strong** |
| Evaluation metrics and benchmarking | Disegno A/B/E, contrasto di specificità, freeze/held-out | Protocollo frozen, bootstrap clusterizzato | **Strong** |
| Novel architectures and platforms for FL | Architettura non-parametrica (scambio testuale) | Insight peer-only, no aggregazione modello | Moderate |
| Adaptive/personalized FL models | Agenti intrinsecamente personalizzati (nessun modello globale) | Ogni agente resta specializzato | Moderate |
| Privacy-preserving mechanisms | Solo *no raw-data exchange* (non privacy formale) | Protocollo: nessuno scambio di serie grezze | Weak |
| Efficient model aggregation/optimization | Nessuna aggregazione di modello/gradienti | — | Weak / Not applicable |
| Security challenges/solutions | Non affrontato | — | Not applicable |
| Federated unlearning | Non affrontato | — | Not applicable |
| Resource-efficient FL for edge | Comunicazione testuale compatta (aneddotico) | Insight brevi | Weak |
| Applications (healthcare/finance/IoT) | Industrial/IoT-adjacent (diagnosi processo) | TEP proxy per fault diagnosis | Moderate |
| Data governance/compliance | Non affrontato | — | Not applicable |

[INTERPRETAZIONE] Punti di aggancio forti: **collaborative frameworks + non-IID + evaluation/benchmarking**.
Costruire abstract e claim su questi tre, NON su privacy/security/aggregation.

---

# OUTPUT 3 — RELATED-WORK TAXONOMY (per una Related Work da paper 10 pagine)

[RACCOMANDAZIONE] 3 sottosezioni (max 4), con densità decrescente. Struttura consigliata:

**RW.1 — Federated knowledge transfer beyond parameter aggregation.**
Da FedAvg/non-IID (una frase) a knowledge/logit/prototype/data-free federation (FedMD, FedDF, FedGKT,
FedProto, FedGen) e label-exclusive/monoclass (FedCKD, monoclass teachers). Tesi: *l'oggetto federato
si è spostato da pesi a conoscenza; noi lo spostiamo a **testo interpretabile**.*

**RW.2 — Textual/semantic knowledge sharing and federated LLMs.**
FoT (Yao et al.) come riferimento del metodo; Federated In-Context LLM Agent Learning; Social
Learning; FedCoT; federated prompt/LoRA tuning; Time-FFM come federated FM su TS. Agent memory (ExpeL,
Metacognitive Reuse) come "local reasoning". Tesi: *la federazione testuale LLM esiste ma non è stata
studiata su serie temporali con esperienza non-IID class-disjoint.*

**RW.3 — Time-series representation for LLMs and (federated) fault diagnosis.**
Verbalizzazione/rappresentazione (T2SP, TRUCE; FD-LLM) come *enabling interface* (breve); federated
fault diagnosis parametrico (rotating machinery, chemical process, federated-meta few-shot; TS anomaly
IIoT) come contesto applicativo. Tesi: *la diagnosi federata è parametrica; la rappresentazione
TS→testo deterministica è una direzione attiva (T2SP), che noi usiamo come interfaccia, non come
contributo.*

(Opz. RW.4 breve: non-IID heterogeneity taxonomy per fissare il termine class-disjoint.)

---

# OUTPUT 4 — CLAIM AUDIT

Supported / Partially / Unsupported. "Evidence" = fonte. "Safer wording" = formulazione reviewer-safe.

| Candidate claim | Supported? | Evidence | Risk | Safer wording |
|---|---|---|---|---|
| Novel federated architecture | **Partially** | Architettura FoT-like adattata; FoT è di Yao et al. | Alto se "novel" implica metodo nuovo | "a federated **knowledge-transfer** setup adapting FoT (Yao et al., 2026) to…" |
| First FoT application to time-series | **Partially (difendibile)** | Nessun FoT su TS identificato | Medio (preprint recente) | "to our knowledge, the first controlled application of FoT-style textual federation to multivariate time-series diagnosis" |
| First textual federation for fault diagnosis | **Partially** | FD-LLM centralizzati; FoT non-TS | Medio | "we did not identify prior textual **federated** knowledge transfer for fault diagnosis" |
| Handles non-IID data | **Supported** | 4 agenti class-disjoint; B−A 4/4 | Basso | "under class-disjoint (missing-class) non-IID experience" |
| Transfers knowledge across clients | **Supported** | B−A=+0.861; B−E=+0.778 | Basso | "transfers **discriminative** textual information across agents" |
| Does not exchange raw data | **Supported** | Protocollo: solo insight testuali | Basso | "raw time-series observations are not exchanged between agents" |
| Privacy-preserving | **Unsupported** | Nessuna DP/secure agg.; leakage non testato | **Fatale** | evitare; "data locality (no raw-series exchange); we make no formal privacy claim" |
| Semantic specificity | **Supported (as interpretation)** | B−E=+0.778, CI [.722,.833] | Basso-medio | "supports the interpretation of semantic specificity of the transferred associations" |
| Enables locally-unseen recognition | **Supported** | A=0/36 → B=31/36 | Basso (se floor esplicitato) | "enables recognition of **locally unseen** fault conditions in this controlled setting" |
| Robust | **Unsupported** | Un modello, 12 run, no perturbazioni | Alto | evitare; "consistent across the four agents in this PoC" |
| Generalizable | **Unsupported** | Nessun cross-domain; PV non fatto | **Fatale** | evitare; "cross-domain generalization is not yet tested" |
| Communication efficient | **Partially** | Insight compatti, ma non misurato vs baseline | Medio | "communication is limited to compact textual insights" (senza numeri non misurati) |
| Multivariate | **Supported** | 41 XMEAS | Basso | "multivariate (41-variable) time series" |
| Interpretable/auditable | **Supported** | Insight NL + freeze/hash chain | Basso | "human-readable insights and a fully frozen, auditable protocol" |

[INTERPRETAZIONE] Le due claim **fatali** da non fare mai: *privacy-preserving* e *generalizable*.
Le due più forti e sicure: *no raw-data exchange* + *semantic specificity (B−E)* + *interpretable/
auditable evaluation*.

---

# OUTPUT 5 — TERMINOLOGY RECOMMENDATION

Per ogni termine: accuratezza scientifica · rischio reviewer · compatibilità con la call · consiglio.

- **Federated Learning (nudo)** — accuratezza *bassa* (no aggregazione parametri, single-round,
  ICL) · rischio *alto* (Reviewer A) · compat. call *alta come parola-chiave* · **QUALIFY/AVOID**:
  usare solo con qualificatore ("FL-like", "federated … transfer").
- **Federation over Text (FoT)** — accuratezza *alta come nome del metodo di Yao et al.* · rischio
  *alto se presentato come nostro* · compat. *media* · **USE come riferimento**: "we build on FoT
  (Yao et al., 2026)"; mai "we propose FoT".
- **Federated Knowledge Transfer** — accuratezza *alta* · rischio *basso* · compat. *alta*
  (collaborative learning / non-IID) · **USE (primario).**
- **Federated Reasoning** — accuratezza *media/alta* · rischio *medio* (enfasi LLM) · compat. *media*
  · **USE come secondario** ("federated textual reasoning").
- **Collaborative Learning** — accuratezza *alta* · rischio *basso* · compat. *alta* (topic esplicito)
  · **USE (nel framing sessione).**
- **Distributed Knowledge Sharing** — accuratezza *alta* · rischio *basso* · compat. *media* ·
  **USE (variante).**
- **Semantic Federation / Semantic Knowledge Federation** — accuratezza *alta e specifica* · rischio
  *basso-medio* · compat. *media* · **USE (per catturare l'oggetto testuale).**

[RACCOMANDAZIONE] **Terminologia primaria del paper:** *"federated textual knowledge transfer"* /
*"federated knowledge sharing"* (con "collaborative learning under non-IID" per l'aggancio alla
call), FoT nominato come metodo di riferimento. **Bandire** in titolo/abstract: *privacy-preserving,
secure, robust, generalizable*.

---

# OUTPUT 6 — REVIEWER RED TEAM

Severity ∈ {fatal, major, moderate, minor}. Per ciascuna: risposta possibile + se serve **nuovo
esperimento** o solo **framing**.

**Reviewer A — esperto Federated Learning (scettico che sia FL).**
1. *"Questo non è FL: nessun modello/gradiente aggregato."* — **major** → *framing*: adottare
   "federated knowledge transfer / FL-like", citare la linea FedMD→FedProto→FoT; citare che gli
   autori di FoT usano "FL-like".
2. *"Single-round, nessuna convergenza: dov'è il learning?"* — **moderate** → *framing*: dichiarare
   esplicitamente single-shot ICL federato; posizionare come knowledge transfer, non training.
3. *"Manca il confronto con FL parametrico / federated distillation."* — **moderate** → *framing +
   Related Work* (non apples-to-apples; spiegare perché).
4. *"Privacy solo asserita."* — **major se rivendicate privacy** → *framing*: rimuovere claim di
   privacy; solo data locality.
5. *"Solo 4 client, 1 round: non scala a Big Data."* — **moderate** → *framing*: PoC controllato;
   Variety non Volume.

**Reviewer B — esperto LLM/multi-agent (scettico sulla novelty vs FoT originale).**
1. *"FoT esiste già (Yao et al. 2026): cosa aggiungete?"* — **major/potenzialmente fatal se mal
   inquadrato** → *framing*: contributo = dominio TS + non-IID class-disjoint + controllo B−E; mai
   "we propose FoT". Serve una frase di delta esplicita.
2. *"E Federated In-Context LLM Agent Learning? Anche loro federano testo con dati locali."* —
   **major** → *framing*: citare e distinguere (no TS/FDD/unseen/controllo).
3. *"B−E potrebbe riflettere che l'LLM ignora etichette sbagliate, non 'specificità semantica'."* —
   **moderate** → *framing*: linguaggio "supports the interpretation"; E=3/36≠0 mostra che non è un
   effetto banale.
4. *"Un solo LLM, proprietario, non riproducibile (no seed/temp)."* — **major** → *nuovo esperimento
   leggero* (secondo LLM) **o** framing forte (R=3 + aggregazione + freeze) + Limitations.

**Reviewer C — esperto time-series/fault diagnosis (scettico su verbalizer e baseline A).**
1. *"Il verbalizer è il vero contributo? È validato come classificatore?"* — **moderate** →
   *framing*: dichiarare verbalizer come *enabling interface* (non classificatore), citare T2SP/TRUCE;
   Phase A misura separabilità, non accuracy.
2. *"A=0/36 è un uomo di paglia."* — **major** → *framing (floor esplicito) + baseline central-ICL*
   (Parte K). Questo è il punto in cui un *esperimento* (central-ICL) aiuta di più.
3. *"Perché non un classificatore FDD standard (CNN/SVM) come riferimento?"* — **moderate** →
   *baseline nice-to-have* (nearest-prototype) + spiegare non-apples-to-apples con unseen transfer.
4. *"TEP simulato, un solo mode/4 guasti: rilevanza industriale?"* — **moderate** → *framing*: PoC
   controllato; PV = future work (non richiesto qui).

**Reviewer D — esperto metodologia/statistica (scettico su n, floor, CI, generalizzazione).**
1. *"n=36 non indipendenti; realmente 12 run."* — **moderate** (già gestito) → *framing*: enfatizzare
   che usate bootstrap clusterizzato su 12 cluster; non dire mai "36 casi indipendenti".
2. *"12 run fisici sono pochi per CI stretti."* — **major** → *framing*: CI riportati come clusterati;
   dichiarare la scala come limite; eventualmente più run (costoso; non necessario se onesti).
3. *"harmed=0 = nessun negative transfer?"* — **moderate** → *framing*: harmed=0 è aritmetico (floor
   di A); dirlo esplicitamente.
4. *"B−A confonde 'presenza di informazione' con 'valore della federazione'."* — **major** →
   *framing (B−E centrale) + central-ICL baseline*.
5. *"Generalizzazione?"* — **moderate** → *framing*: feasibility, non generalization; PV future.

[INTERPRETAZIONE] Le critiche che richiedono davvero un **esperimento** (non solo framing) sono
**una sola con alto ritorno**: il **central/pooled equal-information ICL** (risponde a A3, B1-parziale,
C2, D4). Un **secondo LLM** attenua B4/D. Tutto il resto è **framing + Limitations**.

---

# OUTPUT 7 — WHAT MUST BE IN THE PAPER (10 pagine, no appendice)

**Introduction (indispensabile):** problema (diagnosi sotto esperienza distribuita eterogenea);
RQ esplicita ("can textual knowledge federation transfer discriminative information across agents
with class-disjoint temporal experience, without exchanging raw series?"); **attribuzione di FoT a
Yao et al.**; delta di contributo in 2-3 bullet; disclaimer TEP=testbed controllato, PV fuori scope.

**Related Work (indispensabile, compatto):** le 3 sottosezioni di OUTPUT 3; citare esplicitamente
FoT, Federated In-Context LLM Agent Learning, FedProto/FedMD, Time-FFM/FedCoT, T2SP; frase su
non-IID class-disjoint (FedCKD/monoclass); una riga di FL classico.

**Method (indispensabile):** verbalizer come *enabling interface* deterministica diagnosis-neutral
(breve); struttura a 4 agenti class-disjoint + pseudolabel opache; generazione insight peer-only;
federazione single-round; formato dell'insight (pseudolabel + observed_pattern). Dire chiaramente
cosa NON viene scambiato.

**Experimental Design (indispensabile):** condizioni A/B/E; **definizione precisa di E come
derangement pre-registrato delle associazioni a parità di testo**; R=3 + aggregazione; unità
statistica (12 cluster fisici / 36 osservazioni); bootstrap clusterizzato; freeze/held-out guard;
**baseline central-ICL** (se aggiunta).

**Results (indispensabile):** tabella primaria A/B/E; B−A (primario) + B−E (specificità) con CI;
per-agente; helped/harmed/unchanged; preservazione Normal/seen; **decomposizione del floor di A**.

**Limitations (indispensabile, non opzionale):** scala (12 run); floor di A e lettura di B−A; un
solo LLM non deterministico; TEP proxy (no PV); nessuna privacy formale; harmed=0 aritmetico;
central-ICL come comparatore (se non aggiunto, dichiararlo come limite).

[INTERPRETAZIONE] Con 10 pagine senza appendice, il **budget di spazio** è il vero vincolo: tagliare
il dettaglio del verbalizer (rimando a lavoro/tag), tenere il disegno A/B/E e B−E come cuore.

---

# OUTPUT 8 — BIBLIOGRAPHY PRIORITIZATION

### MUST CITE (≤15)

1. **Yao, Rabbani, Zaheer, Li — Federation over Text: Insight Sharing for Multi-Agent Reasoning.**
   arXiv:2604.16778 (2026), preprint. *Il metodo che applichiamo; attribuzione obbligatoria; delimita
   la nostra novelty.*
2. **McMahan et al. — Communication-Efficient Learning of Deep Networks from Decentralized Data
   (FedAvg).** AISTATS 2017. *Radice del FL; contrasto "noi non aggreghiamo parametri".*
3. **Li & Wang — FedMD: Heterogeneous FL via Model Distillation.** NeurIPS 2019 WS; arXiv:1910.03581.
   *Sposta l'oggetto federato a logit; predecessore.*
4. **Lin et al. — Ensemble Distillation for Robust Model Fusion in FL (FedDF).** NeurIPS 2020. *KD
   federata server-side.*
5. **Tan et al. — FedProto: Federated Prototype Learning across Heterogeneous Clients.** AAAI 2022;
   DOI 10.1609/aaai.v36i8.20819. *Comunica prototipi di classe invece di gradienti — analogo numerico
   dell'insight per-classe.*
6. **Zhu, Hong, Zhou — Data-Free KD for Heterogeneous FL (FedGen).** ICML 2021. *Federazione di
   conoscenza sintetica.*
7. **Federated In-Context LLM Agent Learning.** arXiv:2412.08054 (2024). *Vicino più pericoloso:
   federazione testuale LLM con dati locali.*
8. **Mohtashami et al. — Social Learning: Towards Collaborative Learning with LLMs.** arXiv:2312.11441
   (2023). *Ponte distillazione→testo naturale.*
9. **Liu et al. — Time-FFM: LM-Empowered Federated Foundation Model for TS Forecasting.** NeurIPS
   2024; arXiv:2405.14252. *FL+FM+TS parametrico (adjacent obbligatorio).*
10. **Chuan Li et al. — FedCoT: Communication-Efficient Federated Reasoning Enhancement for LLMs.**
    arXiv:2508.10020 (2025). *Federated reasoning parametrico (LoRA).*
11. **Kim et al. — Representing Time Series as Structured Programs for LLM Reasoning (T2SP).**
    arXiv:2606.12481 (2026). *Rappresentazione deterministica TS→LLM già attiva ⇒ blocca claim di
    novità sul verbalizer.*
12. **Jhamtani & Berg-Kirkpatrick — Truth-Conditional Captioning of Time Series Data (TRUCE).**
    EMNLP 2021 Findings; arXiv:2110.01839. *Testo fattuale su TS.*
13. **Li et al. — Federated Learning on Non-IID Data Silos: An Experimental Study.** ICDE 2022;
    arXiv:2102.02079. *Tassonomia label-subset skew / partizione #C=k.*
14. **Zhu et al. — Federated Learning on Non-IID Data: A Survey.** Neurocomputing 2021. *Framing
    non-IID.*
15. **He, Annavaram, Avestimehr — Group Knowledge Transfer (FedGKT).** NeurIPS 2020;
    arXiv:2007.14513. *KT edge-server (feature/logit).*

### SHOULD CITE (≤20)

16. Li et al. — **FedProx** (MLSys 2020). 17. Karimireddy et al. — **SCAFFOLD** (ICML 2020).
18. Wang et al. — **FedNova** (NeurIPS 2020). 19. Kairouz et al. — **Advances and Open Problems in
FL** (2021). 20. **PCDD / Bilateral Curation** (arXiv:2405.18972, 2024) — terminologia
class-disjoint. 21. **Le, Le, Le, Truong-Huu — FedCKD: A Knowledge Distillation Approach to
Cross-Client Learning in FL with Label-Exclusive Datasets** (LNCS, 2026; DOI
10.1007/978-981-92-1462-4_29) — *verificato*; da non confondere con l'omonimo "FedCKD:
Cluster-Aware KD for medical FL" (2025). 22. **Chen, Tang, Li — FedMeta-FFD: Industrial Edge
Intelligence, Federated-Meta Learning for Few-Shot Fault Diagnosis** (IEEE TNSE 2023; DOI
10.1109/tnse.2023.3266942) — *verificato*; neighbor FDD diretto (FL + meta-learning verso nuove
categorie di guasto). *(Il preprint "one-shot monoclass-teachers", HAL hal-05272000, resta NON
verificato in Crossref/OpenAlex: non citare finché venue/DOI non confermati.)* 23. **Sun, Si, Wu, Gong — Federated
Zero-Shot Learning with Mid-Level Semantic Knowledge Transfer** (Pattern Recognition, 2024; DOI
10.1016/j.patcog.2024.110824) — *verificato*; nota: aggrega un **modello globale** e usa attributi
semantici ZSL (non testo LLM / non insight peer). 24. Zhao et al. — **ExpeL**
(AAAI 2024). 25. Didolkar et al. — **Metacognitive Reuse** (arXiv:2509.13237, 2025). 26. Lewis et
al. — **RAG** (NeurIPS 2020) — comparatore concettuale. 27. Burns et al. — **Weak-to-strong
generalization** (ICML 2024). 28. **FD-LLM** (Qaid et al., arXiv:2412.01218, 2024). 29. **FD-LLM**
(Lin et al., Adv. Eng. Informatics 2025). 30. **SAX_HAR-LLM** (Pappa et al., ESWA 2026). 31. Liu et
al. — **Deep Anomaly Detection for TS in IIoT (FL)** (IEEE IoT-J 2020). 32. **FL fault diagnosis in
rotating machinery** (Elsevier 2023). 33. **Knowledge Distillation in Federated Learning: a
comprehensive survey** (Discover Computing, 2025) — inquadramento del filone federated-KD. 34. **A
Survey on Federated Fine-tuning of LLMs** (arXiv:2503.12016). 35. Zhao et al. — **ESAX+BoW** (IEEE
TIM 2022).

### OPTIONAL / BACKGROUND
Personalized FL (Ditto/pFedMe); federated prompt learning (arXiv:2501.13904); ACE/HyperAgents/
Evolving Prompts; KD-in-FL surveys; DP/secure aggregation classici (solo se si discute privacy per
negarla); TEP FDD centralizzati (autoencoder/interpretable knowledge discovery).

[RACCOMANDAZIONE] Le voci marcate "verificare venue/DOI" (21, 22, 23) vanno confermate su
IEEE Xplore/Scopus/Crossref prima del camera-ready; le altre sono ancorate a venue note.

---

# OUTPUT 9 — SEARCH LOG (riproducibilità)

**Database/fonti consultati.** Web (Google/Bing via strumento di ricerca) su domini primari:
arXiv, OpenReview/NeurIPS/ICML/ICLR, ACM DL, IEEE Xplore, Springer, Elsevier/ScienceDirect,
Semantic Scholar/OpenAlex; sito ufficiale IEEE BigData 2026; fonte primaria FoT letta come PDF
locale (`2604.16778v2.pdf`). Connettore Elsevier/Scopus disponibile per verifica DOI in fase di
camera-ready (uso pianificato, vedi note).

**Range temporale.** Fino a settembre 2026 (data consultazione 2026-09-02). Enfasi 2020–2026.

**Query principali (rappresentative):**
- `IEEE BigData 2026 Special Session Federated Learning on Big Data call topics deadline`
- `Time-FFM LM-Empowered Federated Foundation Model Time Series Forecasting`
- `federated fault diagnosis Tennessee Eastman Process non-IID clients unseen fault classes`
- `FedCoT communication-efficient federated reasoning enhancement large language models`
- `federated in-context learning prompt sharing LLM clients privacy`
- `federated learning LLM sharing natural language insights reasoning agents non-IID 2026`
- `non-IID federated learning taxonomy label distribution skew missing classes survey`
- `federated learning clients disjoint classes transfer locally unseen classes zero-shot`
- `federated time series classification anomaly detection industrial IoT survey`

**Fonti primarie lette in dettaglio.** FoT (arXiv:2604.16778v2, testo integrale + tabelle +
referenze); FedCoT (abstract/pagina arXiv); Federated In-Context LLM Agent Learning (abstract);
Time-FFM (metadati NeurIPS/arXiv); PDF locali del filone verbalizer (T2SP, TRUCE, FD-LLM×2,
ESAX+BoW, SAX_HAR-LLM: front matter/abstract per bibliografia).

**Citation chaining.**
- *Backward* (obbligatorio su FoT): estratte le referenze di Yao et al. → FedAvg[8], Social
  Learning[19], ExpeL[22], Metacognitive Reuse[23], HyperAgents[25], ACE[26], Evolving Prompts[28],
  FedCoT[18], weak-to-strong[49], RAG[48].
- *Forward*: dai vicini (FoT, federated distillation, federated LLM, Time-FFM, federated FDD,
  textual knowledge sharing) verso competitor/follow-up → Federated In-Context LLM Agent Learning,
  FedCKD, monoclass teachers, PCDD, Fed. ZSL semantic transfer.

**Criteri di inclusione.** Rilevanza su ≥1 asse (FL/knowledge transfer; testo/semantica; LLM/FM;
non-IID class-disjoint; TS/FDD; valutazione/controlli). Preferite fonti primarie e venue note.

**Criteri di esclusione.** Blog/press non primari come fonte di claim; lavori solo keyword-simili
ma divergenti dopo lettura (es. TEP FDD centralizzati generici → BG/NR).

**Screening.** ~60–80 record ispezionati (titoli/abstract); **~35** inclusi nella core review;
**~23** nella matrice comparativa; **5** nel nearest-neighbor.

**Limiti della ricerca (onestà).** (i) FoT è un **preprint** non ancora peer-reviewed: status da
ri-verificare prima della submission. (ii) **Verificate in questa passata** via
Crossref/OpenAlex: FedProto (DOI 10.1609/aaai.v36i8.20819), FedCKD label-exclusive (DOI
10.1007/978-981-92-1462-4_29), Fed. ZSL mid-level semantic transfer (DOI
10.1016/j.patcog.2024.110824), FedMeta-FFD (DOI 10.1109/tnse.2023.3266942). **Ancora da confermare**
(solo record HAL): "One-Shot Federated Distillation, Monoclass Teachers" — **da non citare** finché
venue/DOI non sono confermati (il punto strutturale è già coperto, verificato, da FedCKD). (iii) Le citazioni
foundational (FedAvg/FedProx/SCAFFOLD/FedNova/FedMD/FedDF/FedGKT/FedProto/FedGen) sono ancorate a
venue consolidate note; non ogni PDF è stato riaperto singolarmente in questa passata.

---

# OUTPUT 10 — FINAL POSITIONING (tre versioni)

## Conservative (massima sicurezza reviewer)

**Contribution statement.** *"We present a controlled feasibility study showing that, in a frozen
Tennessee Eastman testbed, sharing locally-derived textual insights across agents with class-disjoint
temporal experience can transfer discriminative information about locally unseen fault conditions,
without exchanging raw time-series data."*

- Applichiamo un meccanismo FoT-style (Yao et al., 2026) a serie temporali multivariate via
  un'interfaccia di verbalizzazione deterministica e diagnosis-neutral.
- Introduciamo un protocollo di valutazione **leakage-resistant e pre-registrato** (pseudolabel
  opache, freeze/held-out, A/B/E) con un **controllo di specificità (B−E)**.
- Riportiamo evidenza *di feasibility* (B−A primario; B−E specificità) con incertezza clusterizzata,
  delimitando esplicitamente scala e floor del baseline.

## Balanced (raccomandata)

**Contribution statement.** *"We adapt Federation over Text (Yao et al., 2026) to multivariate
time-series fault diagnosis and provide the first controlled evaluation of textual knowledge
federation under class-disjoint (missing-class) non-IID experience, isolating the role of semantic
correctness via a preregistered label-association control."*

- **Domain + setting:** prima applicazione controllata di federazione testuale a diagnosi TS
  multivariata sotto esperienza non-IID class-disjoint, con classi localmente non viste.
- **Evaluation contribution:** disegno A/B/E con controllo di specificità B−E (a parità di testo,
  conta la correttezza dell'associazione) e protocollo interamente frozen/auditable.
- **Findings:** gli agenti riconoscono guasti mai visti localmente grazie agli insight peer corretti
  (B−A=+0.861; 4/4 agenti); il beneficio crolla con associazioni corrotte (B−E=+0.778) — feasibility,
  non generalizzazione.

## Aggressive (claim più forte ancora plausibile — con rischio)

**Contribution statement.** *"We show that agents with disjoint, single-fault local experience can
collectively diagnose faults none of them has seen locally by exchanging only natural-language
insights, and that this collective capability is driven by the semantic correctness of the shared
knowledge rather than its volume."*

- Rischio: enfatizza "collective capability" e "driven by" (quasi-causale) → esposto a Reviewer B/D.
- **Mitigazione obbligatoria se scelta:** central-ICL baseline presente; linguaggio "supports the
  interpretation"; floor di A e scala dichiarati; nessun accenno a privacy/generalizzazione.
- [INTERPRETAZIONE] Sconsigliata senza il comparatore a informazione equivalente.

**In nessuna versione** attribuirci l'invenzione di FoT.

---

# OUTPUT 11 — POSSIBILI TITOLI

Riflettono il contributo reale; evitano *privacy-preserving/robust/generalizable/secure*.

1. *Federated Textual Knowledge Transfer for Multivariate Time-Series Fault Diagnosis under
   Class-Disjoint Experience*
2. *Sharing Insights, Not Signals: Federation over Text for Locally-Unseen Fault Recognition in
   Multivariate Time Series*
3. *Can Textual Knowledge Federation Transfer Discriminative Information across Non-IID Temporal
   Agents? A Controlled Tennessee Eastman Study*
4. *Federation over Text on Time Series: A Controlled Evaluation of Semantic Knowledge Transfer for
   Locally Unseen Faults*
5. *Diagnosing the Unseen: Peer Textual Insights for Class-Disjoint Multivariate Time-Series Agents*
6. *Text-Mediated Federated Knowledge Transfer for Industrial Fault Diagnosis: A Specificity-
   Controlled Feasibility Study*
7. *When Agents Talk Instead of Averaging: Federated Textual Insight Sharing for Time-Series
   Diagnosis under Missing-Class Heterogeneity*
8. *A Leakage-Resistant, Preregistered Evaluation of Federated Textual Insight Transfer for
   Multivariate Time-Series Diagnosis*
9. *From Signals to Insights: Federated Knowledge Sharing for Locally Unseen Conditions in
   Multivariate Time Series*
10. *Semantic Specificity of Federated Textual Knowledge: Evidence from a Controlled Time-Series
    Fault-Diagnosis Testbed*

[RACCOMANDAZIONE] Preferiti per la Special Session: **#1** (aggancio non-IID/collaborative) e **#3**
(RQ esplicita, testbed onesto). #6/#8 se si vuole enfatizzare il rigore di valutazione.

---

# OUTPUT FINALE — CRITERIO DECISIONALE (§39)

**Domanda:** *dato il deadline del 30 settembre 2026, l'evidenza TEP frozen è sufficiente per una
submission scientificamente difendibile se inquadrata correttamente, oppure la letteratura rivela
gap critici da colmare sperimentalmente prima della submission?*

[INTERPRETAZIONE — risposta separata per priorità]

### Critical before submission (necessari per difendibilità)
1. **Framing terminologico** (federated knowledge transfer / FL-like; MAI "we propose FoT"; MAI
   privacy-preserving/generalizable). *Solo framing — costo zero.*
2. **Delta esplicito vs FoT e vs Federated In-Context LLM Agent Learning** (una frase di
   posizionamento + citazioni). *Solo framing.*
3. **Comparatore a informazione equivalente (central/pooled ICL).** *Unico esperimento realmente
   critico*; risponde alla critica più forte (B−A confonde presenza-di-informazione con valore-della-
   federazione). **Fattibile entro il 30/09** (riusa insight/prompt). Se impossibile, va **dichiarato
   come limite esplicito** e la claim ridotta alla versione Conservative.

### Can be handled by framing / limitations
- Floor di A (decomposizione 14/22/0 + lettura "presenza vs assenza"); B−E centrale.
- Scala (12 run) e CI clusterizzati.
- Un solo LLM non deterministico (R=3 + freeze; secondo LLM = nice-to-have).
- harmed=0 aritmetico; assenza di privacy formale; TEP proxy.
- Non-apples-to-apples con FL parametrico / FDD classico (Related Work + Limitations).

### Post-submission / future PV work (NON richiesti per questo paper)
- Validazione fotovoltaica (PV): esplicitamente fuori scope; **non** è condizione di questa review.
- Multi-round / libreria evolutiva FoT; più guasti/mode; più modelli su larga scala; analisi di
  leakage quantitativa; DP/secure aggregation.

**Non si raccomanda** né una V3 del verbalizer né una validazione PV: la letteratura **non** le
rende necessarie per rendere difendibile *questa* submission. Il verbalizer resta enabling layer
(coperto da T2SP/TRUCE come precedenti); il PV è la fase empirica successiva del PhD.

### Verdetto finale
[INTERPRETAZIONE] **Submission difendibile = SÌ, condizionata**, nella versione **Balanced**, se:
(a) framing e attribuzione corretti; (b) presente il comparatore central-ICL **oppure** claim
ridotta alla Conservative con il comparatore dichiarato come limite; (c) floor/scala/limiti esposti
onestamente. In questa forma il contributo è **onesto, in-scope come collaborative/knowledge-transfer
learning sotto non-IID, e nuovo a livello di combinazione + evaluation design** — non a livello di
metodo. Senza (b), il paper è a rischio di rifiuto da un reviewer FL o LLM che chiede "cosa aggiunge
la *federazione* oltre l'avere il testo".

---

*Fine del report. Tutti i numeri sperimentali provengono dagli artefatti frozen al commit
`45ec4eed…` (tag `phase-b-results-frozen`). Le affermazioni di letteratura sono ancorate alle fonti
elencate in OUTPUT 8–9; le voci marcate "verificare venue/DOI" vanno confermate prima del
camera-ready.*
