# Piano — Condizione C: Central/Pooled Equal-Information ICL

**Data:** 2026-09-06
**Scopo:** Aggiungere un comparatore che isoli il valore della *federazione distribuita*
rispetto al semplice *possesso dell'informazione testuale*, rispondendo alla critica
"B−A confonde presenza di informazione con valore della federazione".

---

## 1. Razionale

Nell'esperimento corrente (Exp 1, frozen):

| Condizione | Insight ricevuti | Accuracy unseen |
|---|---|---|
| **A** (isolated) | 0 | 0.000 (0/36) |
| **B** (FoT peer) | 6 (2 per ciascuno degli altri 3 agenti) | 0.861 (31/36) |
| **E** (corrupted) | 6 (stessi pattern, pseudolabel deranged) | 0.083 (3/36) |

Il delta B−A = +0.861 è enorme ma strutturale: A non ha *alcuna* evidenza sulle
classi non viste. Un reviewer può obiettare che il miglioramento derivi dal semplice
avere informazione testuale sulle classi mancanti, non dalla provenienza distribuita
(federazione). Per rispondere serve una baseline **a informazione equivalente ma
centralizzata**: un singolo agente che riceve *tutti* gli 8 insight (anziché i 6 peer
di B) e diagnostica gli stessi held-out case.

### 1.1 Cosa testa la condizione C

- **C > B** → la centralizzazione (avere anche i propri insight come reference
  esplicito) dà un vantaggio; la federazione peer-only perde informazione.
- **C ≈ B** → la provenienza distribuita non degrada; la federazione è
  information-equivalent alla centralizzazione.
- **C < B** → improbabile ma informativo: il rumore degli insight locali (già noti
  implicitamente) confonde il modello.

In tutti i casi, B−E resta il controllo di specificità semantica, indipendente da C.

### 1.2 Perché non è un benchmark "da battere"

C è un **topline descrittivo**: il caso ideale in cui un singolo agente ha tutta
l'esperienza testuale del sistema. Non è un metodo alternativo da superare, ma il
riferimento che mostra *dove* si posiziona B rispetto all'informazione totale
disponibile. Va riportato come tale nel paper.

---

## 2. Definizione della condizione C (Pooled ICL)

### 2.1 Struttura del prompt

Il template diagnostico è **identico** a quello di A/B/E (stessa struttura, stesse
istruzioni, stesso output schema). L'unica differenza è il blocco PEER INSIGHTS:

| Condizione | Local examples | Insight block |
|---|---|---|
| A | 4 (2 local fault + 2 Normal) | assente |
| B | 4 (2 local fault + 2 Normal) | 6 peer insight (esclusi i 2 self) |
| E | 4 (2 local fault + 2 Normal) | 6 peer insight (pseudolabel deranged) |
| **C** | **4 (2 local fault + 2 Normal)** | **8 insight (tutti, inclusi i 2 self)** |

### 2.2 Insight pool per agente nella condizione C

Ogni agente nella condizione C riceve **tutti gli 8 insight** dalla
`final_local_insights.json`:

| Agent | Insight ricevuti (C) | Di cui self | Di cui peer |
|---|---|---|---|
| agent_1 | INS-001..INS-008 | INS-001, INS-002 | INS-003..INS-008 |
| agent_2 | INS-001..INS-008 | INS-003, INS-004 | INS-001,002,005..008 |
| agent_3 | INS-001..INS-008 | INS-005, INS-006 | INS-001..004,007,008 |
| agent_4 | INS-001..INS-008 | INS-007, INS-008 | INS-001..006 |

**Nota:** gli insight self (generati dallo stesso agente sulla propria classe locale)
sono ridondanti con i local examples, ma il pooled agent li riceve ugualmente perché
simula un agente centrale con *tutta* la conoscenza testuale aggregata.

### 2.3 Ordinamento

Come per B, gli insight nel blocco PEER INSIGHTS sono ordinati per `insight_id`
crescente (INS-001 → INS-008). Il campo `source_agent` resta visibile (non ha
impatto informativo dato che l'agente "centrale" non ha identità distribuita).

### 2.4 Pseudolabel

Identiche a B: le pseudolabel corrette, non deranged. C usa gli stessi opaque
token (CLS-ZOGAA, CLS-OJNSG, CLS-R463B, CLS-Z3ISU, Normal).

---

## 3. Piano di implementazione — Fase 1 (smoke test su pochi dati)

### Obiettivo Fase 1

Validare la pipeline C end-to-end su un **sottoinsieme ridotto** dei held-out case
prima di lanciare l'intera valutazione. Il sottoinsieme è sufficiente a verificare
che il codice funzioni, che il prompt sia ben formato, e a ottenere un segnale
direzionale sulla performance di C.

### 3.1 Step 0 — Struttura directory

```
icl/
├── PLAN_CENTRAL_POOLED_ICL.md        ← questo file
├── config/
│   └── condition_c_config.json       ← parametri specifici di C
├── conditions/
│   ├── __init__.py
│   └── builder_c.py                  ← builder per il prompt C
├── prompts/
│   └── pooled_C.txt                  ← template (copia identica di A/B/E)
├── peer_libraries/
│   ├── agent_1_C.json                ← tutti 8 insight
│   ├── agent_2_C.json
│   ├── agent_3_C.json
│   └── agent_4_C.json
├── phase1/
│   ├── phase1_schedule.json          ← subset di held-out case
│   ├── inference/                    ← raw responses
│   ├── predictions/                  ← parsed predictions
│   └── phase1_results.json           ← metriche smoke test
├── full_evaluation/                  ← (Fase 2, struttura analoga a phase_b/final_evaluation)
├── tests/
│   └── test_builder_c.py             ← unit test del builder
└── README.md
```

### 3.2 Step 1 — Creare il template e le librerie C

**Azioni:**

1. **Template `pooled_C.txt`:** copia byte-identica di `phase_b/prompts/fot_B.txt`.
   Verificare con diff che i quattro template (A/B/E/C) siano identici.

2. **Librerie pooled per ciascun agente (`agent_X_C.json`):** per ogni agente,
   caricare `final_local_insights.json` e produrre la lista completa di 8 insight,
   ordinata per `insight_id`. Non filtrare i self.

3. **`condition_c_config.json`:**
   ```json
   {
     "condition": "C",
     "condition_name": "pooled_equal_information",
     "insight_source": "all_8_insights_unfiltered",
     "insight_count_per_agent": 8,
     "includes_self_insights": true,
     "ordering": "insight_id",
     "derangement": null,
     "template": "pooled_C.txt",
     "note": "Topline descriptive comparator, not a method to beat"
   }
   ```

**Criterio di completamento:** `diff pooled_C.txt fot_B.txt` restituisce 0;
ogni `agent_X_C.json` contiene esattamente 8 insight con pseudolabel corrette.

### 3.3 Step 2 — Implementare `builder_c.py`

**Azioni:**

1. Riutilizzare la logica di `phase_b/conditions/builders.py`, in particolare
   `render_diagnostic_prompt()`. Le differenze rispetto a B sono:
   - La funzione `condition_peer_insights()` per la condizione C **non** filtra
     i self insight (salta il filtro `peer_only_insights`).
   - Restituisce tutti gli 8 insight ordinati per `insight_id`.

2. Implementare `build_pooled_insights(agent_id, global_insights)` che:
   - Accetta l'intera lista di 8 insight.
   - NON filtra per `source_agent != agent_id`.
   - Ordina per `insight_id`.
   - Ritorna la lista completa.

3. Implementare `render_condition_c_prompt(...)` che:
   - Carica il template `pooled_C.txt`.
   - Verifica l'identità byte con gli altri template.
   - Sostituisce i placeholder come `render_diagnostic_prompt` di phase_b.
   - Esegue lo scan anti-leakage (`leakage.py`).
   - Ritorna un `RenderedPrompt` con `condition="C"` e
     `available_insight_ids` = tutti e 8.

4. **Verifica token-count:** il prompt C sarà leggermente più lungo di B (8 vs 6
   insight). Documentare la differenza in caratteri e, se possibile, in token
   (tramite tiktoken o il tokenizer del modello). Questa asimmetria va dichiarata
   nella sezione Method del paper.

**Criterio di completamento:** unit test in `tests/test_builder_c.py` che verifica:
- 8 insight nel blocco peer.
- Placeholder tutti sostituiti.
- Leakage scanner non rileva violazioni.
- Il prompt contiene tutti e 8 gli `INS-00X`.

### 3.4 Step 3 — Selezionare il subset Fase 1

**Azioni:**

1. Dalla `inference_schedule.json` di Exp 1, selezionare **1 physical case per
   fault class** (4 case totali), ciascuno valutato da tutti gli agenti per cui è
   unseen (3 agenti ciascuno), per un totale di **12 osservazioni aggregate**
   (il minimo per avere almeno 1 cluster per pseudolabel).

2. Selezione deterministica: prendere il **primo `physical_case_id`** per ciascuna
   delle 4 pseudolabel nella schedule di Exp 1.

3. Ogni osservazione va eseguita **R=3** volte (come Exp 1), per un totale di
   **36 chiamate LLM** nella Fase 1.

4. Aggiungere anche **1 caso Normal** e **1 caso local-fault-seen** per agente
   come sanity check (non necessari per il delta, ma verificano che C non degradi
   le performance viste).

5. Salvare il subset in `phase1/phase1_schedule.json` con lo stesso schema di
   `inference_schedule.json`.

**Criterio di completamento:** schedule generato, validato, contiene ≤ 50 chiamate
LLM totali. I `physical_case_id` sono un sottoinsieme di quelli frozen in Exp 1.

### 3.5 Step 4 — Eseguire la Fase 1 (smoke inference)

**Azioni:**

1. **Precondizione:** verificare che le verbalizzazioni held-out per i case
   selezionati esistano già in `phase_b/final_evaluation/verbalized/`. Riusarle
   senza rigenerarle (il verbalizer è frozen e deterministico).

2. **Esecuzione:** per ogni entry della schedule:
   - Caricare il `case_text` dalla verbalizzazione frozen.
   - Caricare i `local_examples` dal pack dell'agente (`local_examples.json`).
   - Renderizzare il prompt C tramite `builder_c.py`.
   - Inviare al modello (`gpt-5.6-terra`, `reasoning_effort=medium`, structured
     output con lo stesso schema di Exp 1).
   - Salvare la raw response in `phase1/inference/`.

3. **Configurazione LLM:** identica a Exp 1:
   - Modello: `gpt-5.6-terra`
   - Reasoning effort: `medium`
   - Temperature: non supportata (null)
   - Seed: non supportato (null)
   - Structured output: strict, stesso schema
   - Max structural retries: 2
   - R=3 ripetizioni per osservazione

4. **Parsing e aggregazione:** applicare lo stesso parser e la stessa regola di
   maggioranza R=3 (almeno 2 label uguali) usata in Exp 1.

5. Salvare le prediction aggregate in `phase1/predictions/`.

**Criterio di completamento:** tutte le chiamate completate; nessun parse failure
non recuperato; raw responses e predictions salvate.

### 3.6 Step 5 — Valutare i risultati Fase 1

**Azioni:**

1. Calcolare le metriche primarie sul subset:
   - `accuracy_C_unseen` (sul subset di 12 osservazioni unseen)
   - `delta_C_minus_B` = accuracy_C − accuracy_B (sugli stessi case, usando i
     risultati B già frozen di Exp 1)
   - `delta_C_minus_A` = accuracy_C − accuracy_A
   - Per-agent accuracy C

2. Calcolare le metriche secondarie:
   - `accuracy_C_local_seen` (sanity: atteso ≈ 1.0)
   - `accuracy_C_normal` (sanity: atteso ≈ 1.0)

3. Verifiche di coerenza:
   - C non dovrebbe degradare local-seen né Normal.
   - C_unseen dovrebbe essere ≥ B_unseen (o molto vicino), altrimenti
     investigare perché l'informazione aggiuntiva (self insight) confonde.

4. Salvare tutto in `phase1/phase1_results.json`.

**Criterio di completamento:** metriche calcolate, coerenza verificata, segnale
direzionale documentato. Decisione go/no-go per la Fase 2 (full evaluation).

### 3.7 Step 6 — Decisione go/no-go e Fase 2

**Go** (Fase 2 completa) se:
- La pipeline funziona senza errori.
- C_unseen ≥ 0.50 (segnale che l'informazione pooled è utile, come atteso).
- Nessuna degradazione su seen/Normal.

**Investigate** se:
- C_unseen << B_unseen sullo stesso subset → debug prompt, verificare che gli 8
  insight siano presenti e ben formati.

**No-go** se:
- Errori strutturali nella pipeline non risolvibili.

La Fase 2 replica l'intera schedule di Exp 1 (tutti i 12 physical case × 4 agenti
× 3 condizioni viste per agente = 36 unseen + 12 seen + 12 Normal = 60 osservazioni
aggregate, R=3 → 180 chiamate LLM) ma per la sola condizione C.

---

## 4. Costi stimati

### Fase 1 (smoke test)
- ~36 chiamate LLM (12 osservazioni × R=3) + eventuali sanity check
- Costo stimato: < $5 (basato sul costo per chiamata di Exp 1)
- Tempo: ~30 minuti di esecuzione

### Fase 2 (full evaluation)
- ~180 chiamate LLM (60 osservazioni × R=3)
- Costo stimato: ~$15–20
- Tempo: ~2 ore di esecuzione

---

## 5. Impatto sul paper

### 5.1 Cosa aggiungere nella sezione Method
- Una riga nella tabella delle condizioni: **C = pooled equal-information ICL**
  (tutti gli 8 insight, inclusi self).
- Nota sulla differenza di lunghezza del prompt (8 vs 6 insight).

### 5.2 Cosa aggiungere nella sezione Results
- Tabella estesa con 4 condizioni (A/B/C/E).
- Commento su C−B: se ≈ 0, la federazione peer-only è information-equivalent;
  se > 0, la centralizzazione ha un lieve vantaggio ma la federazione ne cattura
  la maggior parte.

### 5.3 Cosa aggiungere in Discussion/Limitations
- C è un topline descrittivo, non un metodo alternativo.
- La differenza B−C (se esiste) va interpretata come il "costo" della distribuzione,
  non come evidenza contro la federazione.
- L'asimmetria informativa (8 vs 6 insight) va dichiarata.

---

## 6. Vincoli e guardrail

1. **Nessuna modifica ai dati frozen di Exp 1.** I risultati A/B/E restano
   intatti; C è un esperimento aggiuntivo che riusa gli stessi held-out case
   e le stesse verbalizzazioni.

2. **Stesso modello e stessa configurazione.** `gpt-5.6-terra`, `medium`,
   structured output strict. Nessuna variazione.

3. **Stessa regola di aggregazione.** R=3, maggioranza ≥ 2.

4. **Leakage scanner attivo.** Ogni prompt C viene scansionato prima dell'invio.

5. **Nessun tuning o selezione adattiva.** Gli 8 insight sono quelli frozen,
   nell'ordine `insight_id`. Nessuna curazione, nessun ranking, nessuna rimozione.

6. **Pseudolabel opache.** Nessuna modifica allo spazio delle label.

---

## 7. Checklist Fase 1

- [ ] Creare la struttura directory `icl/`
- [ ] Copiare e verificare il template `pooled_C.txt`
- [ ] Generare le 4 librerie `agent_X_C.json`
- [ ] Scrivere `condition_c_config.json`
- [ ] Implementare `builder_c.py`
- [ ] Scrivere `test_builder_c.py` e verificare che passi
- [ ] Generare `phase1_schedule.json`
- [ ] Eseguire le ~36 chiamate LLM
- [ ] Parsare e aggregare le prediction
- [ ] Calcolare le metriche Fase 1
- [ ] Documentare i risultati in `phase1_results.json`
- [ ] Decisione go/no-go per Fase 2
