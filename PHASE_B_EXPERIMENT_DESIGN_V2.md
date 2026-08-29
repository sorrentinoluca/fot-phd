# PHASE_B_EXPERIMENT_DESIGN_V2.md

Specifica sperimentale **pre-implementazione** della Fase B, revisione 2.
Sostituisce `PHASE_B_EXPERIMENT_DESIGN.md` alla luce del nuovo held-out
indipendente congelato.

Non è codice, non è la sezione risultati di un paper, non autorizza inference.

**Fonte verificata:** repository `sorrentinoluca/fot-phd`, branch `phase-b-fot`,
HEAD `86baaa65e72cea22ecb89dd0e7b213aea5a1284b`, tag `phase-b-heldout-frozen`
(verificato: punta allo stesso commit).

Verificato direttamente negli artefatti del repo, **senza leggere alcun valore
di segnale dei workbook held-out**:
- `phase_b/heldout/phase_b_heldout_manifest.csv`: 15 casi (PBH-001…PBH-015),
  con SHA-256, byte size, e metadata di provenienza per ciascuno.
- `phase_b/heldout/PHASE_B_HELDOUT_FREEZE.md`: boundary del freeze, hash degli
  artefatti, check di immutabilità di Fase A.
- `phase_b/heldout/SIMULATOR_PARENT_AUDIT.md`: audit di comparabilità del
  simulatore.
- `phase_b/heldout/HELDOUT_GENERATION_SUMMARY.md`: composizione e provenienza.
- `phase_b/heldout/verify_heldout_integrity.py`: verificatore di integrità.

> **Principio invariato:** Fase A resta congelata. Il freeze doc conferma che i
> quattro file frozen di Fase A sono stati hashati prima di creare l'held-out e
> devono restare identici.

## Implementation resolution — framework commit

The implementation brief that follows this pre-implementation design resolves
the previously open plumbing choices as follows: four deterministic opaque
equal-length `CLS-*` tokens; exactly two local examples from batches 1–2;
exactly two insights per fault pseudoclass; peer-only A/B/E; fixed per-agent
condition-E derangements; no confidence field; abstention counted incorrect in
primary accuracy; `epsilon=0`; and `R=3`. Model/provider and exact model version
remain mandatory researcher decisions and no inference is authorized.

Where the historical sections below still show illustrative `Class-A/B/C/D`,
`≤2`, confidence, or unresolved abstention alternatives, this resolution and
the executable config under `phase_b/config/` take precedence for the framework
implementation. The document remains a design record; it is not the protocol
freeze.

The pre-freeze adversarial hardening further fixes: label-neutral insight fields
outside `pseudolabel`; no prompt-facing agent-to-local-label crosswalk; strong
normalized-byte B/E invariance; strict null prediction on abstention; one initial
attempt plus two structural-only retries ending in `ABSTAIN / parse_failure`;
R=3 two-vote aggregation for primary metrics; separate local-fault-seen and
Normal secondary accuracies; and a 10,000-draw bootstrap over the 12 fault-run
clusters (four pseudoclass strata × three runs). Repetition-level outcomes remain
stochastic-stability reporting. These executable decisions supersede historical
examples below that describe another alternative.

---

## 0. Cosa cambia rispetto alla V1 del design (sintesi)

1. **Nuovo held-out indipendente** (15 casi da simulatore parent) sostituisce i
   batch 8–10 come test finale. Risolve il problema "8–10 già ispezionati".
2. **Pseudolabel obbligatorie** nei prompt: mai F1/F8/F10/F13 all'LLM (prior
   knowledge del benchmark TEP).
3. **Peer-only federation**: in FoT ogni agente riceve solo insight *degli
   altri*, non i propri, e nessun insight sul Normal.
4. **Interpretazione onesta della shared library**: il discriminante da V1 non è
   "non è una prototype library" ma **provenance + local derivation**.
5. **Controlli D/E ridimensionati**: riesaminati criticamente per il PoC minimo.
6. **Ipotesi ripulite** dai termini vaghi ("substantially"), rese
   pre-registrabili.
7. **Unità statistica a tre livelli** esplicita, con clustering per run fisico.

---

## 1. Domanda scientifica centrale (invariata)

> A parità di verbalizzatore V2 congelato e di modello LLM, la condivisione di
> insight testuali tra agenti con conoscenza locale non-IID migliora la diagnosi
> dei fault che il singolo agente non ha osservato localmente?

```
Phase A:  time series → structured evidence → neutral text     [FROZEN]
Phase B:  neutral text → local reasoning → insight sharing → diagnosis
```

La Fase B misura il **valore marginale della federazione**, non del
verbalizzatore.

---

## 2. Il nuovo held-out indipendente

### 2.1 Composizione (dal manifest, verificato)

15 casi fisici nuovi, congelati prima di qualsiasi verbalizzazione,
tuning, insight-generation o inference di Fase B:

| Classe (metadato offline) | Run | Casi | case_id |
|---|---|---|---|
| Normal | 12, 13, 14 | 3 | PBH-001..003 |
| F1 | 11, 12, 13 | 3 | PBH-004..006 |
| F8 | 11, 12, 13 | 3 | PBH-007..009 |
| F10 | 11, 12, 13 | 3 | PBH-010..012 |
| F13 | 11, 12, 13 | 3 | PBH-013..015 |

Ogni caso: `StopTime=50 h`, sampling `1/60 h = 1 min`, 3001 righe, 54 colonne,
integrità strutturale verificata (`xlsx_valid`, `no_nan`, `no_inf`,
`sampling_constant`, `complete_no_early_stop`).

> **Attenzione — le label di classe sono metadata offline.** Nel manifest la
> classe è `class_offline` / `fault_id`: servono a *noi*, evaluator-side. Il
> freeze doc è esplicito: "This freeze does not pass them to a verbalizer and
> performs no diagnostic evaluation." Non entrano mai nel prompt (§ pseudolabel).

### 2.2 Perché questo held-out è metodologicamente valido

Il punto delicato di un held-out *nuovo* è: è comparabile al dataset su cui è
stata costruita la Fase A, o è un dominio diverso che confonderebbe i risultati?
L'audit (`SIMULATOR_PARENT_AUDIT.md`) risponde, e l'ho verificato:

- il simulatore usato è a commit `a0413e1`, **parent diretto** del commit dataset
  `309b944` di Fase A;
- la S-function del plant (`temexd_mod.c`), le dichiarazioni (`teprob_mod.h`) e
  le librerie (`TElib.mdl`, `tesys.mdl`) sono **byte-identiche**;
- lo stato iniziale numerico (`xInitial`) è **identico**: 35/35 entries uguali,
  differenza massima assoluta zero su ogni campo;
- l'unica differenza del commit figlio è l'aggiunta di un layer di *setpoint
  esterni*; il parent è l'ultimo workflow standard prima di quel layer, e i run
  held-out usano il workflow standard senza setpoint custom.

> **Perché è importante?** Il nuovo held-out è **meccanicamente comparabile** al
> dataset di Fase A per run standard, non un dominio nuovo. Quindi un
> peggioramento in Fase B non sarà attribuibile a "dati diversi". E soprattutto:
> è **genuinamente untouched a livello di progetto** — nessuno ha ancora guardato
> i suoi valori di segnale. Risolve alla radice il limite dell'held-out della V1.

### 2.3 Ruolo dei batch 8–10 (declassati)

I batch originali 8–10 **non sono più il test finale**. Al massimo possono
servire come **materiale storico / secondary analysis** (es. confronto
esplorativo), mai come held-out primario. Qualsiasi risultato su 8–10 va
etichettato "secondary, previously inspected", separato dal test primario.

---

## 3. Pseudolabel

### 3.1 Il problema

Un LLM preaddestrato **potrebbe conoscere il benchmark Tennessee Eastman**: i
nomi "Fault 1/8/10/13" sono documentati in letteratura, con le loro firme. Se
l'LLM vedesse "F13" nel prompt, potrebbe attingere a conoscenza pregressa invece
di ragionare sulle firme fornite — un canale di contaminazione che
falserebbe sia isolated sia FoT, e in modo non uniforme tra classi.

### 3.2 La soluzione: pseudonimizzazione deterministica e congelata

- Nei prompt, i fault sono nominati con **pseudolabel opache**: es. `Class-A`,
  `Class-B`, `Class-C`, `Class-D` (o identificatori casuali opachi tipo
  `CLS-7f3a`). **Requires researcher decision** sullo schema esatto (§ decisioni).
- La mappa **`real fault ↔ pseudolabel` esiste SOLO evaluator-side**, in un file
  congelato, mai nel prompt.
- **Normal resta "Normal"**: è un riferimento neutro condiviso, non un fault del
  benchmark con una firma nominata da riconoscere; il rischio di prior knowledge
  su "normale" è trascurabile e mascherarlo complicherebbe senza guadagno.
- La pseudonimizzazione è **fissa per tutto l'esperimento**: la stessa
  pseudolabel indica lo stesso fault in ogni agente, ogni condizione, ogni caso.

> **Perché riduce la contaminazione:** l'LLM non può agganciare "Class-C" a
> conoscenza enciclopedica su un fault TEP specifico, perché "Class-C" non esiste
> in nessun corpus. È costretto a usare **solo** le firme fornite (esempi locali +
> insight peer), che è esattamente ciò che vogliamo misurare. La conoscenza
> discriminante deve venire dall'esperimento, non dal pretraining.

> **Attenzione — limite residuo:** la pseudonimizzazione nasconde il *nome*, non
> la *firma*. Se una firma verbalizzata fosse così caratteristica da essere
> riconoscibile come "il fault TEP con la grande dinamica su una certa misura",
> un LLM potrebbe ancora agganciarla. Non è eliminabile del tutto; va dichiarato
> come threat residuo (§ threats).

---

## 4. Topologia degli agenti

Quattro agenti, ciascuno esperto locale di **una** pseudoclasse fault + Normal:

| Agent | Local known | Locally unseen (fault) |
|---|---|---|
| Agent 1 | Normal, Class-A | Class-B, Class-C, Class-D |
| Agent 2 | Normal, Class-B | Class-A, Class-C, Class-D |
| Agent 3 | Normal, Class-C | Class-A, Class-B, Class-D |
| Agent 4 | Normal, Class-D | Class-A, Class-B, Class-C |

(La corrispondenza Class-X ↔ fault reale è evaluator-side, congelata.)

"Conoscenza locale" = esempi etichettati (con pseudolabel) solo della propria
classe fault + Normal, presi da development (batch 1–5). Non-IID perché ogni
agente vede una distribuzione parziale e diversa.

Normal universale (§ motivazione invariata: riferimento condiviso, task ben
posto).

---

## 5. Peer-only federation

In condizione FoT, ogni agente riceve **solo insight provenienti dagli altri
tre agenti**. Esclusioni esplicite:

- **non riceve i propri insight** (già incorporati nella sua conoscenza locale);
- **non riceve insight sul Normal** (Normal è già locale a tutti).

Quindi la libreria vista da Agent 1 contiene solo insight su Class-B, Class-C,
Class-D (prodotti rispettivamente da Agent 2, 3, 4).

> **Perché è importante:** così la differenza **isolated → FoT** rappresenta
> *esclusivamente* conoscenza acquisita dagli altri nodi sui fault che l'agente
> non ha visto. Se un agente ricevesse i propri insight, il delta includerebbe
> "riformulazione della propria conoscenza", confondendo il segnale. Il filtro
> peer-only rende il delta interpretabile come puro trasferimento.

Conseguenza pratica: la libreria è **specifica per agente** (ciascuno riceve i
tre insight-set che non sono i suoi). Va costruita e congelata per agente, con
provenance.

---

## 6. Interpretazione onesta della shared library

Questa sezione corregge un punto della V1.

**Non** si sostiene ingenuamente che "la shared insight library non è una
prototype library". Onestà strutturale: dopo la federazione, la libreria **può
diventare** una raccolta `pseudoclasse → pattern diagnostico`. La forma finale
somiglia a una prototype library.

Il discriminante scientifico rispetto alla V1 è **come quella conoscenza è
nata**, non la sua forma finale:

| | Prototype library (V1, da evitare) | Phase B shared library |
|---|---|---|
| Chi la produce | il ricercatore, ex ante | ogni agente, dai propri dati locali |
| Da quali dati | conoscenza globale/enciclopedica | esempi locali (batch 1–5) di UNA classe |
| Copertura per agente | tutte le classi | solo la propria classe locale |
| Provenance | assente | obbligatoria (`source_agent`, scope) |
| Come arriva al peer | fornita a tutti | trasferita via testo dai peer |

> **Formulazione da usare nel paper:** la differenza non è la forma della
> libreria, ma **provenance + local derivation**: in Fase B la conoscenza
> classe-specifica è *derivata localmente dai dati locali di ciascun agente,
> esportata come testo con provenienza, e ricevuta dai peer*. Che il risultato
> aggregato assomigli a una mappa classe→firma è atteso e non è un difetto: è ciò
> che la federazione *produce*, non ciò che le viene *regalato*.

---

## 7. Formato dei local insight

Schema minimale con provenance obbligatoria:

```json
{
  "insight_id": "agentX_clsY_i",
  "source_agent": "agent_2",
  "pseudolabel": "Class-B",
  "evidence_scope": "local development examples, batches 1-5",
  "observed_pattern": "descrizione testuale della firma osservata localmente",
  "confidence": "high | medium | low"
}
```

Regole (minimal PoC):
- **numero fisso di insight per fault**: raccomandato **≤2** (vedi §8);
- **nessun editing manuale**;
- **nessuna generazione su validation (6–7) o sul nuovo held-out**;
- `observed_pattern` descrive la firma, non contiene il nome reale del fault (usa
  la pseudolabel);
- provenance (`source_agent`, `evidence_scope`) obbligatoria.

Campo `confidence`: mantenuto come descrittore testuale, **non** usato per
ranking automatico (§8).

---

## 8. Niente dedup/ranking complessi

Per il PoC minimo:
- **niente LLM di merge**;
- **niente ranking per self-confidence**;
- **niente selezione adattiva** degli insight;
- **ordine deterministico congelato** (es. per `insight_id`).

Osservazione che semplifica tutto: **c'è un solo esperto locale per ciascun
fault** (un solo agente conosce Class-B). Quindi **non c'è deduplicazione
inter-agente sullo stesso fault da fare** — non esistono due agenti che
producono insight sulla stessa classe. La libreria è semplicemente l'unione
degli insight, filtrata peer-only.

---

## 9. Unità statistica (tre livelli)

Distinzione obbligatoria:

- **A. Physical independent unit:** `fault × TEP run`. Nel nuovo held-out: 15
  unità fisiche indipendenti (5 classi × 3 run).
- **B. Inference instance:** `agent × physical case`. Uno stesso caso fisico
  viene diagnosticato da più agenti → più istanze di inference, **non**
  indipendenti tra loro.
- **C. Stochastic LLM repetition:** R repliche dello stesso prompt.

> **Regola non negoziabile:** le diagnosi di tre agenti sullo **stesso run
> fisico** NON sono tre repliche fisiche indipendenti. Sono tre istanze di
> inference sulla stessa unità fisica. Qualsiasi bootstrap/CI deve
> **clusterizzare almeno per run fisico** (i 15 casi PBH), non trattare le
> istanze agente×caso come indipendenti. La variabilità LLM (livello C) si
> aggrega *entro* istanza; la variabilità fisica (livello A) è il livello a cui
> si fa inferenza.

Con 15 run fisici, il potere statistico resta limitato: va dichiarato (§
threats). Ma 15 casi nuovi e untouched sono migliori dei 9 già visti (8–10).

---

## 10. Cosa riceve l'agente

**In tutte le condizioni:**
- **neutral text V2** del caso (verbalizzatore congelato);
- **local labeled examples** con **pseudolabel** (Class-X + Normal), da batch 1–5;
- **label space pseudonimizzato**: l'elenco `[Class-A, Class-B, Class-C,
  Class-D, Normal]`.

**Solo in FoT:**
- **peer insights** (§5): solo dagli altri tre agenti, nessuno sul Normal.

**Mai:**
- **structured numerical JSON** (le feature grezze) — solo neutral text;
- nomi reali dei fault;
- mappa globale classe→firma completa fornita ex ante;
- batch/case ID, metadata di provenienza.

---

## 11. Output diagnostico

Schema JSON minimale:

```json
{
  "predicted_label": "Class-A | Class-B | Class-C | Class-D | Normal",
  "abstain": false,
  "used_insight_ids": ["agent_3_clsC_1", "..."],
  "reasoning_summary": "breve, 1-3 frasi",
  "confidence": 0.0
}
```

Note:
- `predicted_label`: singola pseudoclasse (primaria). Top-k opzionale, non usato
  dalla metrica primaria.
- `used_insight_ids`: essenziale per H3 — verifica *se* l'agente ha usato insight
  peer e correla uso ↔ beneficio.
- `abstain`: gestione da decidere (§ decisioni).
- `confidence`: **valutare se serve.** Raccomandazione: mantenerla come campo
  **descrittivo** (utile per analisi di calibrazione a posteriori) ma **non**
  usarla nella metrica primaria, che si basa su correttezza della predizione. Se
  complica il parsing, si può omettere senza perdita per H1/H3.

---

## 12. Condizioni sperimentali (riesaminate)

**Essenziali:**
- **A = ISOLATED**: solo conoscenza locale.
- **B = FoT**: identico + peer insights.

**Controlli di specificità (H3) — riesame critico:**
La V1 marcava D ed E come entrambi essenziali. Riesame per il PoC minimo:

- **E = CORRUPTED/SHUFFLED insights** *(raccomandato essenziale)*: insight veri
  ma con pseudolabel permutate. È il controllo più informativo: se l'agente fa
  bene lo stesso, gli insight non stanno trasferendo la mappa firma→classe, e H1
  sarebbe spiegata da altro. Costa poco (riusa gli insight già generati,
  permutando le etichette).
- **D = RANDOM/IRRELEVANT insights** *(declassato a opzionale)*: controlla il
  puro effetto-volume di testo. Utile, ma E copre gran parte dello stesso rischio
  e la lunghezza del testo può essere riportata direttamente (token count) senza
  una condizione dedicata.

> **Raccomandazione:** per il **minimal defensible**, usare **A + B + E**. La
> condizione D resta come upgrade opzionale. Questo riduce le inference rispetto
> alla V1 (che chiedeva A+B+D+E) mantenendo il controllo di specificità più
> importante.

**Oracle (C):** non nel PoC minimo (upper bound opzionale).

---

## 13. Controllo delle variabili

Identici tra A, B, E: modello e versione, temperature, seed (se disponibile),
system prompt, esempi locali e loro ordine, input verbalizzato, token budget,
schema di output, parsing, retry, context length, label nascoste.

**Unica differenza ammessa:** blocco peer-insights (assente in A; genuino in B;
etichette-permutate in E). Riportare sempre la **lunghezza in token** delle tre
condizioni: B ed E devono avere lunghezza quasi identica (stessi insight, solo
pseudolabel diverse), il che neutralizza l'effetto-volume senza bisogno di D.

---

## 14. Ipotesi (pre-registrabili, senza termini vaghi)

**H1 — FoT benefit (primaria).**
`Delta_unseen = accuracy_FoT_unseen − accuracy_isolated_unseen > 0`,
dove l'accuratezza è calcolata sulle sole classi **localmente non viste** di
ciascun agente, sui 15 casi held-out.

**Consistency support (parte di H1):**
`Delta_unseen > 0` per **almeno 3 dei 4 agenti**.

**Transfer (primaria, direzionale):**
`helped > harmed` in aggregato (§ definizioni sotto).

**H3 — Specificity (primaria):**
`Delta_FoT > Delta_control`, dove il controllo è E (corrupted). Cioè il beneficio
di FoT deve superare quello ottenuto con insight a etichette permutate.

**H2 — No degradation on seen (secondaria, pre-registrabile):**
`accuracy_FoT_seen ≥ accuracy_isolated_seen − epsilon`, con **epsilon fissato
prima** (raccomandato: epsilon = 0, cioè "non peggiora"; oppure una tolleranza
minima dichiarata). Sulle classi **localmente viste**, FoT non deve degradare.

**H4 — Negative transfer (secondaria, di reporting):**
`harmed` va **sempre riportato**, con il suo valore assoluto, anche se
`helped > harmed`.

Definizioni transfer (su istanze appaiate isolated↔FoT):
- **helped:** isolated errato → FoT corretto;
- **harmed:** isolated corretto → FoT errato;
- **unchanged:** stessa correttezza.

---

## 15. Development / tuning data — cosa è permesso

- **Local knowledge + insight generation:** SOLO original batch 1–5.
- **Batch 6–7 (ex-validation Fase A):** SOLO sviluppo/tuning di plumbing Fase B —
  formato prompt, parser, schema di output, quantità di insight, meccanica. Mai
  come misura di performance predittiva che poi si generalizza.
- **Original 8–10:** non più necessari come final test (declassati a secondary).
- **NUOVO held-out (15 casi):** NON aperto finché il protocollo non è
  completamente congelato (§16).

Cosa **può** cambiare dopo aver guardato 6–7: formattazione del prompt, robustezza
del parser, schema JSON, numero di insight, dettagli di plumbing.
Cosa **NON può** cambiare dopo 6–7: la definizione delle metriche, le ipotesi, i
criteri di successo, la selezione degli esempi (una volta fissata la regola), e
nulla che riguardi i 15 casi held-out.

> **Attenzione:** il tuning su 6–7 non deve diventare ottimizzazione della
> performance. È plumbing (funziona il parsing? il formato è valido?), non "quale
> prompt fa vincere FoT". Quest'ultimo sarebbe leakage di design.

---

## 16. Selezione degli esempi locali

Proposta concreta: **2 esempi per classe locale** (Class-X + Normal), da batch
1–5, selezione **deterministica** (i primi 2 batch in ordine numerico: batch 1 e
2).

Perché 2 e non 3: con un PoC a 15 casi e prompt che includono anche i peer
insights, contenere il few-shot riduce lunghezza del prompt e rischio che il
beneficio venga dal volume. 2 esempi per classe danno un ancoraggio sufficiente
senza gonfiare. **Requires researcher decision** se preferire 3 per dare più
ancoraggio alle classi difficili (es. F8).

Vietato il cherry-picking: la regola è meccanica (primi N batch), non "gli
esempi più chiari".

---

## 17. Generazione insight — pipeline

```
local labeled examples (batch 1-5, classe locale)
   → insight-generation prompt (identico per tutti gli agenti)
   → ≤2 candidate insights per fault
   → schema §7 con provenance + pseudolabel
   → peer-only filtering per agente
   → shared library per-agent (congelata, hashata)
```

Stesso modello e versione per generazione e diagnosi (coerenza, controllo
variabili). Nessuna generazione su 6–7 o held-out.

---

## 18. Federation over Text — meccanismo

```
Agent 1 esperto di Class-A  → esporta ≤2 insight testuali su Class-A
Agent 2 esperto di Class-B  → esporta ≤2 insight su Class-B
Agent 3 esperto di Class-C  → esporta ≤2 insight su Class-C
Agent 4 esperto di Class-D  → esporta ≤2 insight su Class-D
        ↓  (peer-only filtering)
Agent 1 riceve: insight su B, C, D  (non i propri, non Normal)
        ↓
Agent 1 può ora ragionare su Class-B/C/D che non ha mai visto localmente
```

Federato = **testo** (insight con provenance). Non dati grezzi, non parametri.

---

## 19. Metriche

**Primaria:** `Delta_unseen` (accuratezza sulle classi localmente non viste,
FoT − isolated, appaiata). Denominatore, per ciascun agente, le istanze delle sue
3 classi fault unseen sui 15 casi held-out.

**Secondarie:** overall accuracy; seen-class accuracy (per H2); helped / harmed /
unchanged; per-pseudoclasse recall; confusion matrix; abstention rate;
`used_insight_ids` usage rate (per H3, correlazione uso↔beneficio); confidence
calibration (opzionale, descrittiva).

---

## 20. Paired comparison e inferenza

Confronto **appaiato** sulla stessa istanza (stesso agente, stesso caso fisico,
stesso input) isolated vs FoT. Rimuove la varianza tra casi.

Analisi, **clusterizzate per run fisico** (§9):
- **McNemar** sulle coppie appaiate (esito binario corretto/errato);
- **paired bootstrap clusterizzato sui 15 run fisici** per CI su `Delta_unseen`;
- per il PoC: **paired reporting** (tabelle helped/harmed/unchanged) è il minimo.

> **Dichiarazione obbligatoria:** con 15 run fisici e 4 agenti, il potere è
> limitato. La Fase B è un PoC che indica una direzione, non uno studio
> confermativo. Nessuna affermazione di significatività forte.

---

## 21. Stabilità stocastica dell'LLM

- **R = 3** repliche per prompt (raccomandato minimo).
- **temperature:** 0 se l'API lo consente (max riproducibilità); altrimenti bassa
  fissa.
- **seed:** fissato se esposto.
- **aggregazione entro istanza:** maggioranza sulle R repliche, oppure accuratezza
  media; deciso e congelato prima.

Ribadito (§9): repliche LLM (livello C) ≠ run fisici (livello A). Non mescolarle
nello stesso denominatore.

---

## 22. Prompt design (struttura)

```
[SYSTEM]           ruolo, task, vincoli output
[TASK]             cosa produrre, schema JSON
[LABEL SPACE]      [Class-A, Class-B, Class-C, Class-D, Normal]
[LOCAL KNOWLEDGE]  few-shot pseudo-etichettati (classe locale + Normal)
[PEER INSIGHTS]    solo FoT (B) / permutati (E) / assente (isolated A)
[CASE TO DIAGNOSE] neutral text V2 del caso
[OUTPUT SCHEMA]    JSON deterministico
```

A, B, E differiscono **solo** nel blocco `[PEER INSIGHTS]`. Versione testuale
finale non scritta ora: parte del freeze §23.

---

## 23. Freeze del protocollo Fase B

Prima della final evaluation, congelare (config JSON + commit + tag + SHA-256):

- **pseudolabel mapping** (evaluator-side);
- **agent topology**;
- **model / version**;
- **local example selection** (regola + lista risultante);
- **prompt templates** (tutti i moduli, A/B/E);
- **insight-generation prompt**;
- **generated insight library** (per-agent, con provenance);
- **peer filtering**;
- **conditions** (A, B, E; eventuale D);
- **parser**;
- **metrics** (script + definizioni);
- **R**, **temperature**, **seeds**.

Tag previsto: **`phase-b-protocol-frozen`**.

Integrazione con l'held-out già congelato: il tag `phase-b-heldout-frozen`
(`86baaa6`) è già in essere. Prima della final evaluation va eseguito
`phase_b/heldout/verify_heldout_integrity.py` per **verificare gli SHA-256** dei
15 workbook contro il manifest, così si conferma che i dati valutati sono
esattamente quelli congelati.

---

## 24. Final test — sequenza (solo dopo il protocol freeze)

1. verificare l'integrità dell'held-out (`verify_heldout_integrity.py`,
   SHA-256 vs manifest);
2. verbalizzare i 15 casi con **V2 congelato**;
3. **nascondere le label reali** all'LLM (pseudolabel + Normal);
4. eseguire **paired isolated (A) vs FoT (B)** [+ E], R repliche;
5. salvare **tutte** le inference (§ artefatti);
6. valutare **offline** (mappa pseudolabel↔reale solo qui).

---

## 25. Costo — ricalcolo sul nuovo held-out

Base: **5 classi × 3 run = 15 casi fisici.**

Ogni caso viene presentato a **tutti e 4 gli agenti** (ciascuno lo diagnostica dal
proprio punto di vista) → 15 × 4 = **60 istanze di inference** per condizione,
per replica.

**Evaluation completa (all-case)** vs **primary (unseen-only):**
- *all-case*: tutte le 60 istanze (ogni agente diagnostica ogni caso, incluse le
  sue classi seen). Denominatore ampio, usato per metriche secondarie (seen vs
  unseen, confusion).
- *unseen-only (primaria)*: per agente contano solo i casi delle sue 3 classi
  fault unseen. Casi fault held-out = 12 (F1/F8/F10/F13 × 3 run). Per ciascun
  agente, unseen = i 9 casi che non sono la sua classe (3 classi × 3 run). 4
  agenti × 9 = **36 istanze unseen** per condizione per replica. (Il Normal e la
  classe seen entrano solo nelle secondarie.)

**Conteggio inference (R = 3):**

| Config | Istanze/condizione | Condizioni | R | Totale inference |
|---|---|---|---|---|
| A+B minimal (all-case) | 60 | 2 | 3 | **360** |
| A+B+E (all-case) | 60 | 3 | 3 | **540** |
| A+B+E+D (all-case) | 60 | 4 | 3 | **720** |

Più la **generazione insight** una tantum: 4 agenti × ≤2 insight × (1 prompt di
generazione per classe locale) ≈ poche decine di call.

Ordine di grandezza raccomandato (A+B+E, R=3): **~540 inference** + generazione.
La metrica primaria si legge sul sottoinsieme delle **36 istanze unseen** per
condizione.

---

## 26. Artefatti da salvare

```
phase_b/
  heldout/           # GIA' CONGELATO (manifest, freeze, verifier, audit)
  config/            # protocol freeze config, hash, tag, pseudolabel map
  prompts/           # template A/B/E + insight-generation
  local_knowledge/   # esempi locali selezionati (batch 1-5, pseudo-etichettati)
  insights/          # candidate + per-agent peer-filtered library + provenance
  runs/              # una entry per inference
  evaluation/        # script metriche + output
  reports/           # report finale
```

Per ogni inference: agent ID, condition (A/B/E), model, model version, prompt
hash, input hash, output raw, output parsato, physical case_id (PBH-xxx, offline),
timestamp, seed/temperature.

---

## 27. Threats to validity

**Internal:** effetto-volume del testo (neutralizzato da E a pari lunghezza + token
count); prototype mascherata (mitigata da provenance/local derivation §6, testata
da E); prior knowledge del benchmark (mitigato da pseudolabel §3, residuo: la
firma resta riconoscibile).

**External:** un solo simulatore/mode; 4 fault; dominio simulato. **Migliorato**
rispetto alla V1: held-out da simulatore parent verificato comparabile, ma è pur
sempre lo stesso impianto.

**Construct:** diagnosi = scelta da label-space noto; label-space prior (l'agente
sa quante pseudoclassi esistono); insight come proxy di conoscenza diagnostica.

**Statistical:** **15 run fisici** → potere limitato; clustering per run
obbligatorio; LLM stochasticity mitigata da R ma non eliminata; F8 variabilità
ereditata da Fase A (un errore su Class-che-è-F8 può venire dalla firma debole,
non dalla federazione).

---

## 28. Ruolo di F8 (invariato nella sostanza)

F8 (una delle pseudoclassi) ha mostrato in Fase A maggiore variabilità
distribuzionale. In Fase B: non correggere il verbalizzatore, non escluderla,
usarla come test di robustezza. Un fallimento su F8 può derivare dalla firma
verbalizzata debole (eredità Fase A) o dal reasoning/FoT: `used_insight_ids` e
l'analisi per-pseudoclasse aiutano a distinguere, senza garanzia di separazione
netta.

---

# Recommended minimal Phase B protocol

Una configurazione unica, consigliata.

- **Held-out finale:** i 15 casi congelati (`phase-b-heldout-frozen`, `86baaa6`),
  verificati via `verify_heldout_integrity.py` prima dell'uso.
- **Pseudolabel:** `Class-A/B/C/D` per i fault, `Normal` invariato; mappa
  evaluator-side congelata.
- **Agenti:** 4, uno per pseudoclasse fault + Normal universale.
- **Federazione:** peer-only (no self, no Normal insights).
- **Esempi locali:** 2 per classe locale, deterministici (batch 1 e 2).
- **Insight:** ≤2 per fault, schema con provenance, nessun dedup/ranking, ordine
  deterministico.
- **Condizioni:** A (isolated), B (FoT), E (corrupted/shuffled). D opzionale.
- **Input agente:** neutral text V2 + esempi pseudo-etichettati + label space +
  peer insights (solo B/E). No JSON numerico.
- **Output:** `predicted_label`, `abstain`, `used_insight_ids`,
  `reasoning_summary`; `confidence` descrittiva opzionale.
- **Modello:** uno, versione fissata (stesso per generazione e diagnosi).
- **R = 3**, temperature 0 se possibile, seed se disponibile.
- **Unità statistica:** run fisico (15); bootstrap clusterizzato per run.
- **Primaria:** `Delta_unseen > 0`, consistente ≥3/4 agenti; `helped > harmed`;
  `Delta_FoT > Delta_E`.
- **Tuning:** plumbing solo su batch 6–7; conoscenza/insight solo da batch 1–5;
  held-out aperto solo dopo `phase-b-protocol-frozen`.
- **Costo:** ~540 inference (A+B+E, R=3) + generazione insight.

Sequenza operativa:

1. Fissare pseudolabel mapping (evaluator-side) e congelarlo.
2. Selezionare esempi locali deterministici (batch 1–2) per pseudoclasse.
3. Definire prompt (moduli §22) e insight-generation prompt; bozza su dev.
4. Generare ≤2 insight per fault (batch 1–5), schema con provenance.
5. Applicare peer-only filtering → libreria per-agente; costruire condizione E
   (pseudolabel permutate).
6. Tuning plumbing su batch 6–7 (parser, schema, formato). Nessuna metrica
   held-out osservata.
7. **FREEZE** protocollo → tag `phase-b-protocol-frozen` + SHA-256.
8. `verify_heldout_integrity.py` sui 15 casi.
9. Verbalizzare i 15 casi con V2 congelato; nascondere label reali.
10. Eseguire A/B/E appaiati, R=3; salvare ogni inference.
11. Valutare offline: `Delta_unseen`, helped/harmed, `Delta_FoT` vs `Delta_E`,
    con bootstrap clusterizzato per run.
12. Report con threats e caveat (15 casi, F8, pseudonimizzazione residua).

---

# Decisions I need from the researcher

Solo scelte ancora realmente aperte (il final held-out è **RISOLTO**, non in
elenco):

- [ ] **Pseudolabel scheme:** `Class-A/B/C/D` vs identificatori opachi casuali
  (es. `CLS-7f3a`). *Raccomandazione:* opachi casuali (meno suggestivi di
  ordinamento). Conseguenza: nessuna, se la mappa è evaluator-side.
- [ ] **Esempi locali: 2 vs 3** per classe. *Raccomandazione:* 2 (contenere il
  prompt). Conseguenza: 3 dà più ancoraggio alle classi difficili ma allunga.
- [ ] **Insight per fault: ≤2 vs ≤3.** *Raccomandazione:* ≤2. Conseguenza: più
  insight = più rischio effetto-volume.
- [ ] **Modello / versione.** *Not inferable from repository.* *Raccomandazione:*
  stesso modello economico del prototipo, versione fissata.
- [ ] **R (repliche LLM): 3 vs 5.** *Raccomandazione:* 3 per il minimal.
- [ ] **Temperature:** 0 vs bassa fissa. *Raccomandazione:* 0 se l'API lo
  consente.
- [ ] **Controlli: A+B+E (raccomandato) vs A+B+E+D.** *Raccomandazione:* A+B+E;
  D opzionale.
- [ ] **Abstention handling:** errore vs categoria separata. *Raccomandazione:*
  categoria separata, riportata; da decidere il peso nel denominatore primario.
- [ ] **Criterio di successo esatto:** confermare
  `Delta_unseen>0 ∧ ≥3/4 agenti ∧ helped>harmed ∧ Delta_FoT>Delta_E`, con
  `epsilon` di H2 (raccomandato 0).

---

## Nota di coerenza col repository

Verificato su `phase-b-fot` a `86baaa6` (tag `phase-b-heldout-frozen`): manifest
di 15 casi con SHA-256; freeze doc con check di immutabilità di Fase A; audit del
simulatore parent (S-function byte-identica, `xInitial` 35/35 identico,
differenza massima zero); verifier di integrità presente. Non è stato letto alcun
valore di segnale dei workbook held-out, e non è stata eseguita alcuna inference.
Due punti restano fuori dal repository: la scelta del modello LLM e i parametri di
esecuzione (R, temperature), elencati tra le decisioni aperte.
