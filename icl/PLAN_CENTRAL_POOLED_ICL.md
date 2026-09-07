# Piano — Condizione C: Centralized Full-Information Pooled ICL

**Data:** 2026-09-06
**Revisione:** R5 (post-quinto audit — path verificati su repository)
**Scopo:** Aggiungere un comparatore centralizzato con accesso a tutta
l'esperienza testuale del sistema, per mostrare dove si posiziona la
federazione peer-only (B) rispetto a un riferimento empirico post-hoc con
informazione completa rispetto agli artefatti prompt-facing.

---

## 0. Disposizione dei rilievi

### Audit 1 (8 rilievi — tutti accolti in R1)

| # | Rilievo | Disposizione R1 |
|---|---------|-----------------|
| 1 | C non era centralizzata | Accolto: pooled examples |
| 2 | Mancava freeze protocollo | Accolto: amendment formale |
| 3 | Confounding temporale B vs C | Parzialmente accolto: limite dichiarato |
| 4 | Go/no-go adattivo | Accolto: gate solo tecnico |
| 5 | Mancava piano statistico | Accolto: cluster bootstrap |
| 6 | Conteggio chiamate errato | Accolto: ricalcolato |
| 7 | Schedule senza pseudolabel | Accolto: procedura evaluator-side |
| 8 | Nomenclatura collidente | Accolto: C-Pilot / C-Full |

### Audit 2 (7 rilievi — accolti in R2)

| # | Rilievo | Severità | Disposizione R2 |
|---|---------|----------|-----------------|
| 1 | "Equal-information" e linguaggio causale troppo forti | Alto | **Accolto.** Rinominata "centralized full-information". Linguaggio causale rimosso ovunque (§1, §2.5, §2.6). |
| 2 | Pilot apre ground truth prima del freeze C-Full | Alto | **Accolto.** Pilot = prima tranche blind di C-Full; nessun join con ground truth fino al freeze di tutte le predizioni C (§3.6). |
| 3 | Due strategie statistiche aperte in §3.7 vs §5 | Medio | **Accolto.** Eliminata la replica virtuale. Formula fissata in §5.2. |
| 4 | In C non esistono fault "unseen" o "seen" | Medio | **Accolto.** Terminologia aggiornata: tutti i fault sono "class-covered" per C (§3.5, §3.6). |
| 5 | Conteggio pilot ambiguo (R=3 vs R=1) | Medio | **Accolto.** Fissato a 15 chiamate: 4 fault + 1 Normal, tutti R=3 (§3.5). |
| 6 | Freeze dovrebbe coprire più artefatti | Medio | **Accolto.** Lista estesa in §3.3. |
| 7 | C non è un upper bound garantito | Basso | **Accolto.** Terminologia corretta: "full-information empirical reference" (§2.6). |

### Audit 3 (4 rilievi + refinements — accolti in R3)

| # | Rilievo | Severità | Disposizione R3 |
|---|---------|----------|-----------------|
| 1 | Mancano i file eseguibili: runner, evaluator, record schema tutti hard-coded per A/B/E | Alto | **Accolto.** Nuovo §3.4-bis con lista completa dei file eseguibili da creare e relativi test (§3.4-bis). |
| 2 | Freeze manifest incompleto: manca il codice eseguibile (runner, aggregation, evaluator) | Alto | **Accolto.** Tabella §3.3 estesa per coprire tutto il codice eseguibile, i test e gli script di orchestrazione. |
| 3 | "Full-information" va circoscritto: non include i testi sorgente, solo gli artefatti prompt-facing frozen | Medio | **Accolto.** Definizione scoped in §2.1, §2.6 e §6.4. |
| 4 | Natura post-hoc di C non dichiarata: C è progettata dopo aver osservato i risultati A/B/E sullo stesso held-out | Medio | **Accolto.** Nuovo §6.5, richiamo in §1 e nel titolo dello scopo. |

**Refinements minori (audit 3):**

| # | Punto | Disposizione R3 |
|---|-------|-----------------|
| R1 | "sottoinsieme etichettato" → "subset marcato `pilot=true`" | **Accolto** in §3.5. |
| R2 | "significativamente più efficace" → "mostra accuracy osservata più alta" | **Accolto** in §2.5. |
| R3 | Gate tollera errori di rete recuperati via retry | **Accolto** in §3.6. |

### Audit 4 (4 rilievi implementativi — accolti in R4)

| # | Rilievo | Severità | Disposizione R4 |
|---|---------|----------|-----------------|
| 1 | Schedule ambigua: 15 entry case-level vs 45 entry request-level | Medio | **Accolto.** Schedule request-level con 45 entry. |
| 2 | Due archivi (pilot/inference + full_evaluation/inference) creano un passo di trasferimento fragile | Medio | **Accolto.** Archivio canonico unico append-only `c_records.jsonl`. |
| 3 | Freeze manifest incompleto: mancano adapter, bootstrap, verbalizzazioni, mapping, held-out manifest, risultati B frozen | Medio | **Accolto.** Manifest esteso; runner verifica hash a runtime. |
| 4 | CRunRecord troppo ridotto: mancano prompt hash, raw attempts, retry count, model, token usage, timestamps | Basso | **Accolto.** Campi di provenienza completi. Aggiunto `test_run_c_inference.py`. |

### Audit 5 (6 rilievi — verifica contro repository reale — accolti in questa R5)

| # | Rilievo | Severità | Disposizione R5 |
|---|---------|----------|-----------------|
| 1 | Due path inesistenti: `held_out_manifest.json` e `aggregate_predictions_B.json` | Alto | **Accolto.** Path corretti: `phase_b/heldout/phase_b_heldout_manifest.csv` e `phase_b/final_evaluation/inference/aggregate_records.jsonl` filtrato per `condition=="B"`, verificato tramite `inference_output_hash_manifest.json` (§3.3). |
| 2 | Verbalizzazioni non hashabili come `*.json` glob | Medio | **Accolto.** Il manifest di riferimento è `heldout_verbalizations_manifest.json` che contiene `neutral_text_sha256` per ciascun case. Il runner verifica gli hash dei 15 file `.txt` via manifest (§3.3). |
| 3 | Ordinamento schedule contraddittorio: `physical_case_id` ascending vs pilot in 0..14 | Medio | **Accolto.** Ordinamento esplicito: `(pilot DESC, physical_case_id ASC, repetition ASC)`. I pilot case (PBH-001, PBH-004, PBH-007, PBH-010, PBH-013) occupano sequence_index 0..14; i non-pilot 15..44 (§3.5). |
| 4 | Runner non dovrebbe verificare artefatti evaluator-side (viola firewall) | Medio | **Accolto.** Freeze manifest separato in due sezioni: inference-side (verificato dal runner) ed evaluator-side (verificato solo da `evaluate_c_predictions.py`) (§3.3, §7.11). |
| 5 | CRunRecord deve conservare `parsed_output` completo e provenienza per attempt | Basso | **Accolto.** `parsed_output` con tutti i campi (`predicted_label`, `abstain`, `used_insight_ids`, `reasoning_summary`). `request_id`, `response_id`, `token_usage` per ciascun attempt in `raw_attempts` (§3.4-bis). |
| 6 | Congelare JSONL grezzo nel manifest post-inferenza | Basso | **Accolto.** `predictions_manifest.json` include hash di `c_records.jsonl`, predizioni aggregate e execution metadata (§3.7). |

---

## 1. Razionale

Nell'esperimento corrente (Exp 1, frozen):

| Condizione | Esempi locali | Insight ricevuti | Accuracy (36 unseen agent-case) |
|---|---|---|---|
| **A** (isolated) | 4 (2 local fault + 2 Normal) | 0 | 0.000 |
| **B** (FoT peer) | 4 (2 local fault + 2 Normal) | 6 peer | 0.861 |
| **E** (corrupted) | 4 (2 local fault + 2 Normal) | 6 peer (deranged) | 0.083 |

Il delta B−A = +0.861 è strutturale: A non ha alcuna evidenza sulle classi non
viste. Un reviewer può obiettare che il miglioramento derivi dal semplice possesso
di informazione testuale sulle classi mancanti, non dal meccanismo di federazione.

Per contestualizzare questo risultato serve un **riferimento centralizzato**: un
contesto LLM che disponga di tutta l'esperienza testuale prompt-facing che nel
setting federato è distribuita tra i 4 agenti. La condizione C mostra la
performance empirica di questo riferimento; il confronto B vs C posiziona la
federazione rispetto alla centralizzazione, senza attribuzioni causali (i due
contesti differiscono per quantità, forma e struttura — §6.1).

**Nota sulla temporalità:** C è progettata e eseguita *dopo* aver osservato i
risultati di A/B/E sullo stesso held-out set. Il suo ruolo è quello di un
**riferimento esplorativo post-hoc**, non di una condizione pianificata ex ante
(§6.5).

---

## 2. Definizione della condizione C (Centralized Full-Information Pooled ICL)

### 2.1 Cosa significa "centralizzato" e "full-information" nel paradigma testuale

In FL classico, "centralizzato" significa un singolo modello addestrato su tutti
i dati. Nel paradigma testuale in-context, l'analogo è un singolo contesto LLM
che riceve tutta l'esperienza prompt-facing del sistema:

- **Tutti gli esempi locali** di tutti gli agenti (copertura di tutte le classi).
- **Tutti gli insight** generati da tutti gli agenti.

**Scoping di "full-information":** il termine si riferisce all'unione degli
artefatti prompt-facing frozen (esempi etichettati + insight testuali), non alla
totalità dei testi sorgente del TEP. C non vede, ad esempio, i testi dei case di
training da cui gli insight sono stati estratti, né alcun artefatto non incluso
nei file frozen `pooled_examples.json` e `pooled_insights.json`.

### 2.2 Struttura del prompt C

Il template diagnostico è **identico** a quello di A/B/E. Le differenze sono nel
contenuto iniettato:

| Condizione | LOCAL LABELED EXAMPLES | PEER INSIGHTS block |
|---|---|---|
| A | 4 esempi (2 local fault + 2 Normal) | assente |
| B | 4 esempi (2 local fault + 2 Normal) | 6 peer insight |
| E | 4 esempi (2 local fault + 2 Normal) | 6 peer insight (deranged) |
| **C** | **10 esempi (2 per ciascuna delle 4 classi fault + 2 Normal)** | **8 insight (tutti)** |

Il blocco LOCAL LABELED EXAMPLES della condizione C contiene i 10 esempi unici,
unione dei 4 pack LKP-001..004 deduplicata sui due Normal condivisi:

| example_id | pseudolabel | Provenienza pack |
|---|---|---|
| EXM-001 | CLS-ZOGAA | LKP-001 |
| EXM-002 | CLS-ZOGAA | LKP-001 |
| EXM-003 | CLS-OJNSG | LKP-002 |
| EXM-004 | CLS-OJNSG | LKP-002 |
| EXM-005 | CLS-R463B | LKP-003 |
| EXM-006 | CLS-R463B | LKP-003 |
| EXM-007 | CLS-Z3ISU | LKP-004 |
| EXM-008 | CLS-Z3ISU | LKP-004 |
| EXM-009 | Normal | condiviso |
| EXM-010 | Normal | condiviso |

Il blocco PEER INSIGHTS contiene tutti gli 8 insight (INS-001..INS-008), ordinati
per `insight_id`.

### 2.3 Receiver-independence

A differenza di B (dove ogni agente ha un contesto diverso: i propri esempi +
i peer insight altrui), la condizione C è **receiver-independent**: il contesto
è identico per ogni caso diagnosticato. Non esiste variazione per agente.
Questo simula un singolo agente centrale con l'intera esperienza testuale
prompt-facing del sistema.

### 2.4 Pseudolabel e label space

Identici a B: le pseudolabel corrette, non deranged. Stesso label space a
5 elementi (CLS-ZOGAA, CLS-OJNSG, CLS-R463B, CLS-Z3ISU, Normal).

### 2.5 Cosa mostra il confronto C vs B

C riceve più informazione di B (10 vs 4 esempi, 8 vs 6 insight) e in forma
diversa (esempi diretti di tutte le classi vs insight peer sulle classi non
viste). Il confronto C−B **non è a parità di informazione** e non isola un
singolo fattore. Mostra dove si posiziona la federazione peer-only rispetto
al riferimento centralizzato con informazione completa prompt-facing:

- **C ≫ B** → la federazione cattura solo una parte dell'informazione
  disponibile; avere esempi diretti di tutte le classi mostra accuracy
  osservata più alta.
- **C ≈ B** → la federazione testuale raggiunge empiricamente una performance
  vicina al riferimento centralizzato, nonostante l'informazione ridotta.
- **C < B** → risultato informativo: la ricchezza del contesto confonde il
  modello (prompt troppo lungo, ridondanza insight/esempi).

In tutti i casi, B−E resta il controllo di specificità semantica, ortogonale a C.

### 2.6 Cosa C NON è

C è un **riferimento empirico post-hoc con informazione prompt-facing completa**
(full-information empirical reference). Non è:

- Un **upper bound garantito**: è possibile che C < B per effetti di contesto.
- Un **metodo alternativo da battere**: nel paper va presentato come riferimento
  descrittivo ("centralized full-information pooled ICL reference").
- Una **condizione a parità di informazione**: C ha accesso a più informazione
  e in forma diversa rispetto a B.
- Una **condizione pianificata ex ante**: C è stata progettata dopo aver
  osservato i risultati di A/B/E sullo stesso held-out set (§6.5).

"Full-information" si riferisce all'unione degli artefatti prompt-facing frozen,
non alla totalità dei dati sorgente (§2.1).

---

## 3. Piano di implementazione

Il piano usa la nomenclatura **C-Pilot** (smoke test tecnico su subset ridotto)
e **C-Full** (valutazione completa su tutti i held-out).

### 3.1 Step 0 — Struttura directory

```
icl/
├── PLAN_CENTRAL_POOLED_ICL.md           ← questo file
├── config/
│   └── condition_c_config.json          ← parametri specifici di C
├── conditions/
│   ├── __init__.py
│   └── builder_c.py                     ← builder per il prompt C
├── prompts/
│   └── pooled_C.txt                     ← template (copia identica di A/B/E)
├── pooled_libraries/
│   ├── pooled_examples.json             ← 10 esempi (receiver-independent)
│   └── pooled_insights.json             ← tutti 8 insight
├── runner/
│   ├── build_c_schedule.py              ← genera c_schedule.json con tag pilot
│   ├── run_c_inference.py               ← runner: prompt → API → raw response
│   └── records_c.py                     ← CRunRecord (condition="C", central identity)
├── evaluation/
│   ├── aggregation_c.py                 ← aggregazione majority R=3 per C
│   └── evaluate_c_predictions.py        ← join ground truth + metriche
├── schemas/
│   └── c_run_record.schema.json         ← JSON Schema per i record C
├── inference/                           ← ARCHIVIO CANONICO UNICO (append-only)
│   └── c_records.jsonl                  ← tutti i CRunRecord (pilot + full)
├── full_evaluation/
│   ├── protocol_amendment_c.md          ← amendment formale
│   ├── protocol_amendment_c.json        ← machine-readable
│   ├── freeze_manifest_inference.json   ← hash artefatti inference-side
│   ├── freeze_manifest_evaluator.json   ← hash artefatti evaluator-side
│   ├── c_schedule.json                  ← schedule completa request-level (45 entry)
│   ├── predictions/                     ← parsed aggregate predictions
│   ├── predictions_manifest.json        ← hash pre-join (JSONL grezzo + aggregati)
│   └── evaluation_results_c.json        ← metriche finali
├── tests/
│   ├── test_builder_c.py
│   ├── test_records_c.py
│   ├── test_aggregation_c.py
│   ├── test_build_c_schedule.py
│   ├── test_evaluate_c.py
│   └── test_run_c_inference.py          ← resume, idempotenza, freeze guards
└── README.md
```

**Nota architetturale:** non esiste una directory `pilot/inference/` separata.
Tutte le raw response (pilot e full) vengono scritte nello stesso archivio
append-only `icl/inference/c_records.jsonl`. Il runner in modalità
`--pilot-only` esegue le entry con `pilot=true`; la seconda esecuzione
(senza flag) riprende dalle entry rimanenti, verificando tramite
`sequence_index` quali sono già presenti nel JSONL e saltandole (idempotenza).

### 3.2 Step 1 — Creare template, librerie pooled e config

**Azioni:**

1. **Template `pooled_C.txt`:** copia byte-identica di `phase_b/prompts/fot_B.txt`.
   Verificare con `diff` che i template (A/B/E/C) siano identici.

2. **`pooled_examples.json`:** unione dei 4 pack da `local_examples.json`,
   deduplicata sui Normal (EXM-009, EXM-010 compaiono una sola volta).
   10 record totali, ordinati per `example_id`. Ogni record contiene solo
   `example_id`, `pseudolabel`, `neutral_text`.

3. **`pooled_insights.json`:** copia completa di `final_local_insights.json`
   (tutti 8 insight, ordinati per `insight_id`).

4. **`condition_c_config.json`:**
   ```json
   {
     "condition": "C",
     "condition_name": "centralized_full_information_pooled_icl",
     "description": "Post-hoc full-information empirical reference: receiver-independent context with all 10 examples (covering all fault classes) and all 8 insights. Full-information refers to the union of prompt-facing frozen artifacts, not all source texts.",
     "examples": {
       "source": "union of LKP-001..LKP-004 deduplicated on Normal",
       "count": 10,
       "covers_all_fault_classes": true
     },
     "insights": {
       "source": "final_local_insights.json (unfiltered)",
       "count": 8,
       "includes_self": true,
       "filtering": "none"
     },
     "receiver_independent": true,
     "ordering_examples": "example_id",
     "ordering_insights": "insight_id",
     "derangement": null,
     "template": "pooled_C.txt",
     "post_hoc": true,
     "role": "post-hoc full-information empirical reference, not a method to beat"
   }
   ```

**Criterio di completamento:** `diff pooled_C.txt fot_B.txt` → 0;
`pooled_examples.json` contiene 10 record con tutte e 5 le label;
`pooled_insights.json` contiene 8 insight.

### 3.3 Step 2 — Protocol amendment e freeze artefatti

Prima di qualsiasi chiamata LLM, redigere e congelare un **amendment formale**
che estenda il protocollo frozen di Exp 1. L'amendment segue il formato di
`PHASE_B_PROTOCOL_AMENDMENT_001.md`.

**Contenuto dell'amendment:**

1. Razionale: condizione C come riferimento empirico post-hoc centralizzato.
2. Definizione di C: 10 pooled examples + 8 insight, receiver-independent,
   stesso template/schema/modello/R=3.
3. Scheduling: C-Pilot è la prima tranche blind di C-Full.
4. Statelessness: ogni richiesta C è indipendente.
5. Firewall: nessun join con ground truth fino al freeze di tutte le
   predizioni C (pilot + full).
6. Dichiarazione temporale: C è eseguita in un momento diverso da A/B/E;
   il confronto C−B è descrittivo.
7. **Dichiarazione post-hoc:** C è progettata dopo aver osservato i risultati
   di A/B/E sullo stesso held-out set; va trattata come riferimento esplorativo.

#### Freeze manifest — sezione inference-side

Verificato dal runner (`run_c_inference.py`) prima di ogni tranche.
Contiene solo artefatti a cui il runner ha legittimo accesso.

**Artefatti di prompt (prompt-facing):**

| Artefatto | Percorso |
|---|---|
| Template C | `icl/prompts/pooled_C.txt` |
| Esempi pooled | `icl/pooled_libraries/pooled_examples.json` |
| Insight pooled | `icl/pooled_libraries/pooled_insights.json` |
| Config C | `icl/config/condition_c_config.json` |
| Output schema (riuso) | `phase_b/conditions/diagnostic_output.openai.schema.json` |

**Codice eseguibile (pipeline C):**

| Artefatto | Percorso |
|---|---|
| Builder C | `icl/conditions/builder_c.py` |
| Schedule builder | `icl/runner/build_c_schedule.py` |
| Runner C | `icl/runner/run_c_inference.py` |
| Record C | `icl/runner/records_c.py` |
| Record schema C | `icl/schemas/c_run_record.schema.json` |

**Codice riusato da Exp 1 (hash invariato):**

| Artefatto | Percorso |
|---|---|
| Parser | `phase_b/conditions/parser.py` |
| Retry | `phase_b/conditions/retry.py` |
| Leakage scanner | `phase_b/prompts/leakage.py` |
| Execution config | `phase_b/config/execution_config.json` |
| OpenAI adapter | `phase_b/execution/openai_adapter.py` |

**Dati di input frozen (inference-side):**

| Artefatto | Percorso |
|---|---|
| Held-out manifest | `phase_b/heldout/phase_b_heldout_manifest.csv` |
| Verbalizzazioni manifest | `phase_b/final_evaluation/heldout_verbalizations_manifest.json` |
| Verbalizzazioni neutral text | `phase_b/final_evaluation/verbalized/neutral_text/PBH-001.txt` .. `PBH-015.txt` (15 file; hash per-case da `heldout_verbalizations_manifest.json` campo `neutral_text_sha256`) |

**Scheduling:**

| Artefatto | Percorso |
|---|---|
| Schedule completa (request-level) | `icl/full_evaluation/c_schedule.json` |

**Test:**

| Artefatto | Percorso |
|---|---|
| Test builder | `icl/tests/test_builder_c.py` |
| Test records | `icl/tests/test_records_c.py` |
| Test schedule | `icl/tests/test_build_c_schedule.py` |
| Test runner | `icl/tests/test_run_c_inference.py` |

#### Freeze manifest — sezione evaluator-side

Verificato solo da `evaluate_c_predictions.py` dopo il freeze di tutte le
predizioni C. Il runner **non** accede a questi artefatti — la separazione
preserva il firewall tra predizioni e ground truth.

**Codice eseguibile (evaluation C):**

| Artefatto | Percorso |
|---|---|
| Aggregation C | `icl/evaluation/aggregation_c.py` |
| Evaluator C | `icl/evaluation/evaluate_c_predictions.py` |
| Bootstrap (riuso) | `phase_b/evaluation/bootstrap.py` |

**Dati evaluator-side:**

| Artefatto | Percorso |
|---|---|
| Mapping pseudolabel | `phase_b/config/evaluator_side/pseudolabel_mapping.json` |
| Predizioni aggregate B (per Δ C−B) | `phase_b/final_evaluation/inference/aggregate_records.jsonl` (filtrate per `condition=="B"`) |
| Hash manifest inferenza Exp 1 | `phase_b/final_evaluation/inference/inference_output_hash_manifest.json` |

**Test (evaluator-side):**

| Artefatto | Percorso |
|---|---|
| Test aggregation | `icl/tests/test_aggregation_c.py` |
| Test evaluator | `icl/tests/test_evaluate_c.py` |

#### Artefatti dell'amendment

| Artefatto | Percorso |
|---|---|
| Amendment testo | `icl/full_evaluation/protocol_amendment_c.md` |
| Amendment machine | `icl/full_evaluation/protocol_amendment_c.json` |

| Regola non-file | Valore |
|---|---|
| Regola di aggregazione | R=3, majority ≥ 2 (invariata da Exp 1) |

**Entrambi i manifest (inference-side e evaluator-side) e l'amendment vanno
congelati (commit + hash) prima di qualsiasi inferenza C, incluso il C-Pilot.**

### 3.4 Step 3 — Implementare `builder_c.py`

**Azioni:**

1. Creare `builder_c.py` che implementa `render_condition_c_prompt(...)`:
   - Carica il template `pooled_C.txt`.
   - Verifica identità byte con i template A/B/E di phase_b.
   - Carica i 10 esempi da `pooled_examples.json`.
   - Valida: esattamente 10 esempi, 2 per ciascuna delle 4 pseudolabel fault +
     2 Normal, ogni record ha solo `example_id`, `pseudolabel`, `neutral_text`.
   - Carica gli 8 insight da `pooled_insights.json`.
   - Sostituisce i placeholder `<<LABEL_SPACE>>`, `<<LOCAL_EXAMPLES>>`,
     `<<PEER_INSIGHTS_BLOCK>>`, `<<CASE_TEXT>>`.
   - Verifica che nessun placeholder resti non-sostituito.
   - Esegue lo scan anti-leakage (`phase_b/prompts/leakage.py`).
   - Ritorna un `RenderedPrompt` con `condition="C"` e
     `available_insight_ids` = tutti e 8.

2. **Documentare la differenza di prompt length:** caratteri (e token se
   possibile) tra prompt C (10 esempi + 8 insight) e prompt B (4 esempi +
   6 insight). Questa asimmetria va dichiarata nel paper.

**Criterio di completamento:** unit test in `tests/test_builder_c.py`:
- 10 esempi nel blocco LOCAL LABELED EXAMPLES.
- Tutte e 5 le pseudolabel presenti negli esempi.
- 8 insight nel blocco PEER INSIGHTS.
- Placeholder tutti sostituiti.
- Leakage scanner senza violazioni.
- Il prompt contiene tutti gli INS-001..INS-008.
- Il prompt è receiver-independent (identico dato lo stesso `case_text`,
  indipendentemente da quale "agente" lo invoca).

### 3.4-bis Step 3b — Implementare l'harness eseguibile

L'infrastruttura di Exp 1 (`phase_b/evaluation/records.py`,
`phase_b/evaluation/aggregation.py`, `phase_b/evaluation/run_record.schema.json`)
è hard-coded per le condizioni A/B/E e non può ospitare C:

- `RunRecord` valida `agent_id` come `^agent_[1-4]$` e `condition ∈ {A, B, E}`.
- `aggregate_run_records()` raggruppa per `(agent_id, condition, physical_case_id)`,
  ma C è receiver-independent e non ha un `agent_id` significativo.
- Lo schema JSON (`run_record.schema.json`) ripete gli stessi vincoli.

Servono file nuovi, non patch ai file frozen di Exp 1.

**File da creare:**

1. **`icl/runner/records_c.py` — `CRunRecord`**

   Campi obbligatori (identità):
   - `agent_id`: fisso a `"central"` (identità receiver-independent).
   - `condition`: fisso a `"C"`.
   - `physical_case_id`: `^PBH-\d{3}$`.
   - `repetition`: 1..3.
   - `sequence_index`: intero 0..44, posizione nella schedule request-level.

   Campi di predizione (output strutturato completo, come Exp 1):
   - `parsed_output`: oggetto con:
     - `predicted_label`: pseudolabel predetta (stringa dal label space).
     - `abstain`: bool.
     - `used_insight_ids`: lista di `INS-XXX` usati dal modello.
     - `reasoning_summary`: stringa del ragionamento del modello.
   - `valid`: bool (predizione parsabile e label valida).

   Campi di provenienza completi:
   - `prompt_sha256`: hash SHA-256 del prompt renderizzato inviato all'API.
   - `raw_attempts`: lista di tutti i tentativi (inclusi retry strutturali),
     ciascuno con:
     - `attempt_index`: intero 0-based.
     - `raw_response`: testo completo della risposta.
     - `parse_success`: bool.
     - `error_type`: null o stringa (`"network"`, `"parse"`, `"schema"`).
     - `request_id`: ID della richiesta API (header `x-request-id` o equiv.).
     - `response_id`: ID della response (campo `id` della response API).
     - `token_usage`: oggetto con `prompt_tokens`, `completion_tokens`,
       `total_tokens` (dal campo `usage` della response API).
   - `retry_count`: numero totale di retry effettuati (0 se successo al primo
     tentativo).
   - `model_requested`: stringa del modello richiesto (es. `"gpt-5.6-terra"`).
   - `model_returned`: stringa del modello effettivamente usato (dal campo
     `model` della response API, può differire).
   - `reasoning_effort`: `"medium"`.
   - `timestamp_iso`: ISO 8601 UTC del momento di completamento della
     richiesta (ultimo tentativo).
   - `stateless`: `true` (invariante: ogni richiesta C è indipendente, senza
     contesto conversazionale).

   Serializzazione: una riga JSON per record in `c_records.jsonl`, conforme
   a `c_run_record.schema.json`.

2. **`icl/schemas/c_run_record.schema.json`**
   - JSON Schema con `agent_id = "central"`, `condition = "C"`, tutti i
     campi di provenienza sopra elencati (inclusi `raw_attempts` con
     provenienza per-attempt), stesso pattern per `physical_case_id` e
     `repetition` di Exp 1.

3. **`icl/runner/build_c_schedule.py`**
   - Input: held-out manifest di Exp 1 (`phase_b/heldout/phase_b_heldout_manifest.csv`)
     + mapping pseudolabel (`phase_b/config/evaluator_side/pseudolabel_mapping.json`).
   - Output: `c_schedule.json` — **schedule request-level con 45 entry**.
   - Ogni entry contiene:
     - `sequence_index`: intero 0..44, ordine deterministico.
     - `physical_case_id`: `PBH-XXX`.
     - `repetition`: 1, 2 o 3.
     - `condition`: `"C"` (invariante).
     - `receiver_id`: `"central"` (invariante).
     - `pilot`: `true` o `false`.
   - **Ordinamento deterministico:**
     `(pilot DESC, physical_case_id ASC, repetition ASC)`.
     Le 15 entry pilot (5 case × 3 repetition) occupano sequence_index 0..14;
     le 30 entry non-pilot occupano 15..44.
   - Pilot case (selezionati evaluator-side — primo per ciascuna classe):
     PBH-001 (Normal), PBH-004 (F1), PBH-007 (F8), PBH-010 (F10),
     PBH-013 (F13).
   - La pseudolabel usata per la selezione del pilot è interna allo script
     e NON compare nell'output (opacità mantenuta verso il runner).

4. **`icl/runner/run_c_inference.py`**
   - Input: `c_schedule.json`, `builder_c`, config esecuzione,
     `freeze_manifest_inference.json`.
   - **Freeze guard a runtime (inference-side only):** prima di qualsiasi
     inferenza, verifica che gli hash SHA-256 di tutti gli artefatti nel
     manifest inference-side corrispondano ai file su disco. Inclusa la
     verifica per-case dei 15 `neutral_text/*.txt` usando il campo
     `neutral_text_sha256` da `heldout_verbalizations_manifest.json`.
     Abort con errore esplicito se un hash non corrisponde.
     **Il runner NON verifica il manifest evaluator-side** (firewall §7.11).
   - Per ogni entry della schedule:
     1. Controlla se un record con lo stesso `sequence_index` esiste già
        in `c_records.jsonl` → salta (idempotenza per resume).
     2. Renderizza il prompt C tramite `builder_c.py`.
     3. Chiama l'API tramite `openai_adapter.py` (riusato da Exp 1).
     4. Salva il `CRunRecord` completo come nuova riga in `c_records.jsonl`.
   - Modalità `--pilot-only`: esegue solo le entry con `pilot=true`
     (sequence_index 0..14).
   - Modalità default (senza flag): esegue tutte le entry non ancora
     presenti nel JSONL (resume-safe).
   - Retry su errori di rete recuperabili (stessa policy di Exp 1, tracciata
     in `raw_attempts` con provenienza per-attempt).

5. **`icl/evaluation/aggregation_c.py`**
   - Input: `c_records.jsonl`.
   - Valida che il JSONL contenga esattamente 45 record (15 case × 3 rep).
   - Raggruppa per `physical_case_id` (non per `agent_id`, che è sempre
     `"central"`). Regola invariata: majority R=3, ≥ 2 label uguali.
   - Output: una predizione aggregata per physical case, con struttura
     compatibile con `aggregate_records.jsonl` di Exp 1 (stessi campi:
     `agent_id`, `condition`, `physical_case_id`, `aggregation_rule`,
     `parsed_output`, `repetition_outcomes`).

6. **`icl/evaluation/evaluate_c_predictions.py`**
   - Input: predizioni aggregate C + mapping pseudolabel
     (`phase_b/config/evaluator_side/pseudolabel_mapping.json`) +
     predizioni aggregate B da
     `phase_b/final_evaluation/inference/aggregate_records.jsonl`
     (filtrate per `condition=="B"`, verificate contro
     `inference_output_hash_manifest.json`).
   - **Freeze guard evaluator-side:** verifica gli hash nel manifest
     evaluator-side prima del join. **Non accede al manifest inference-side.**
   - Join con ground truth **solo dopo il freeze di tutte le predizioni**.
   - Calcola: `accuracy_C_fault`, `accuracy_C_normal`, `delta_C_minus_B`
     (formula §5.2), cluster bootstrap (§5.3) tramite
     `phase_b/evaluation/bootstrap.py` (riusato).
   - Output: `evaluation_results_c.json`.

**Test per ciascun file:**

| File | Test | Verifica principale |
|---|---|---|
| `records_c.py` | `test_records_c.py` | `agent_id="central"`, `condition="C"`, rifiuta valori A/B/E; `parsed_output` completo con tutti i campi; `raw_attempts` con provenienza per-attempt; serializzazione JSONL |
| `c_run_record.schema.json` | `test_records_c.py` | Validazione JSON Schema coerente con `CRunRecord` |
| `build_c_schedule.py` | `test_build_c_schedule.py` | **45 entry totali**, 15 con `pilot=true` (5 case × 3 rep, sequence_index 0..14), 30 con `pilot=false` (15..44); ordinamento `(pilot DESC, physical_case_id ASC, repetition ASC)`; pseudolabel non esposta |
| `run_c_inference.py` | `test_run_c_inference.py` | **Resume:** dopo interruzione a metà, la riesecuzione salta i record già presenti; **idempotenza:** due esecuzioni consecutive producono lo stesso JSONL; **freeze guard:** fallisce se un hash nel manifest inference-side non corrisponde; **non accede al manifest evaluator-side** |
| `aggregation_c.py` | `test_aggregation_c.py` | Majority corretto, raggruppa per `physical_case_id` solo, rifiuta JSONL incompleto, output compatibile con `aggregate_records.jsonl` di Exp 1 |
| `evaluate_c_predictions.py` | `test_evaluate_c.py` | Formula delta C−B corretta, carica B da `aggregate_records.jsonl` filtrato, verifica hash via `inference_output_hash_manifest.json`, bootstrap seed riproducibile |

**Criterio di completamento:** tutti i test passano; `CRunRecord` rifiuta
`agent_id ≠ "central"` e `condition ≠ "C"`; lo schedule builder produce 45
entry request-level con ordinamento e tag pilot corretti; il runner è
resume-safe e verifica solo il freeze manifest inference-side.

### 3.5 Step 4 — Generare la schedule C completa

La schedule C copre **tutti** i held-out case e viene generata e congelata
**prima** di qualsiasi inferenza. Il C-Pilot è un subset di questa schedule,
non una schedule separata.

**Held-out case nella schedule C:**

Poiché C è receiver-independent e ha esempi di tutte le classi, non esiste la
distinzione "unseen vs locally-seen" che definisce le condizioni in Exp 1.
Tutti i held-out fault case sono **class-covered** per C. Tuttavia, per
confronto diretto con B, la schedule C include gli stessi held-out case usati
in Exp 1.

**Schedule request-level (45 entry):**

Ogni entry nella schedule rappresenta una singola richiesta API, non un case.
Questo elimina qualsiasi ambiguità sull'espansione case→richieste.

- **12 held-out fault case** × R=3 = **36 entry**
- **3 held-out Normal case** × R=3 = **9 entry**
- **Totale C-Full: 45 entry = 45 chiamate LLM**

Campi di ogni entry:

| Campo | Tipo | Descrizione |
|---|---|---|
| `sequence_index` | int 0..44 | Posizione deterministica nella schedule |
| `physical_case_id` | string | `PBH-XXX` |
| `repetition` | int 1..3 | Ripetizione per questo case |
| `condition` | string | `"C"` (invariante) |
| `receiver_id` | string | `"central"` (invariante) |
| `pilot` | bool | `true` per le prime 15 entry (5 case × 3 rep) |

**Ordinamento deterministico:** `(pilot DESC, physical_case_id ASC, repetition ASC)`.

Le 15 entry pilot (sequence_index 0..14) coprono i 5 pilot case:

| sequence_index | physical_case_id | repetition | pilot | classe reale |
|---|---|---|---|---|
| 0 | PBH-001 | 1 | true | Normal |
| 1 | PBH-001 | 2 | true | Normal |
| 2 | PBH-001 | 3 | true | Normal |
| 3 | PBH-004 | 1 | true | F1 |
| 4 | PBH-004 | 2 | true | F1 |
| 5 | PBH-004 | 3 | true | F1 |
| 6 | PBH-007 | 1 | true | F8 |
| 7 | PBH-007 | 2 | true | F8 |
| 8 | PBH-007 | 3 | true | F8 |
| 9 | PBH-010 | 1 | true | F10 |
| 10 | PBH-010 | 2 | true | F10 |
| 11 | PBH-010 | 3 | true | F10 |
| 12 | PBH-013 | 1 | true | F13 |
| 13 | PBH-013 | 2 | true | F13 |
| 14 | PBH-013 | 3 | true | F13 |

**Nota:** la colonna "classe reale" è riportata qui solo a scopo documentativo.
NON compare nella schedule; il runner vede solo `physical_case_id` e `pilot`.

Le 30 entry non-pilot (sequence_index 15..44) coprono i restanti 10 case
(PBH-002, PBH-003, PBH-005, PBH-006, PBH-008, PBH-009, PBH-011, PBH-012,
PBH-014, PBH-015), nello stesso ordine `(physical_case_id ASC, repetition ASC)`.

**La schedule completa (tutte le 45 entry con tag pilot) è congelata
con hash in `freeze_manifest_inference.json` prima di qualsiasi inferenza.**

### 3.6 Step 5 — Eseguire il C-Pilot (prima tranche blind)

**Precondizioni:**
- Amendment congelato (step 2).
- Builder testato (step 3).
- Harness eseguibile testato (step 3b).
- Schedule congelata (step 4).
- Verbalizzazioni held-out già esistenti in
  `phase_b/final_evaluation/verbalized/neutral_text/`.
- **Freeze guard inference-side superato:** il runner ha verificato tutti gli
  hash nel manifest inference-side, inclusi i 15 `neutral_text/*.txt` via
  `heldout_verbalizations_manifest.json` (§7.11).

**Esecuzione:** `run_c_inference.py --pilot-only`

Per ogni entry con `pilot=true` (sequence_index 0..14):
1. Caricare il `case_text` dal file `neutral_text/PBH-XXX.txt` frozen.
2. Renderizzare il prompt C tramite `builder_c.py`.
3. Inviare al modello con configurazione identica a Exp 1:
   - Modello: `gpt-5.6-terra`
   - Reasoning effort: `medium`
   - Temperature: null (non supportata)
   - Seed: null (non supportato)
   - Structured output: strict, stesso schema
   - Max structural retries: 2
4. Salvare il `CRunRecord` completo (con `parsed_output` e tutti i campi di
   provenienza per-attempt) come nuova riga in `icl/inference/c_records.jsonl`.

**Il pilot NON calcola metriche e NON esegue il join con la ground truth.**
Le raw response e le predizioni parsate del pilot restano blind.

**Gate C-Pilot → completamento C-Full (solo tecnico):**
- Tutte le 15 entry completate (errori di rete recuperati via retry sono
  ammessi; contano solo i fallimenti non recuperati).
- Nessun parse failure non recuperato dopo i retry.
- Il prompt renderizzato supera lo scan anti-leakage.
- Lo schema di output è valido per tutte le risposte.
- Le prediction sono tutte label valide o abstention esplicita.

Se tutti i gate tecnici passano, procedere con le restanti 30 entry
(C-Full minus pilot). Le risposte del pilot sono già nel JSONL canonico
e non vengono rieseguite.

### 3.7 Step 6 — Completare C-Full

Eseguire `run_c_inference.py` (senza flag). Il runner:
1. Ri-verifica il freeze guard inference-side (§7.11).
2. Scansiona `c_records.jsonl` e identifica i `sequence_index` già presenti
   (le 15 entry pilot).
3. Esegue le restanti 30 entry (sequence_index 15..44).
4. Appende ogni nuovo `CRunRecord` allo stesso JSONL.

Al termine, `c_records.jsonl` contiene esattamente 45 record.

**Procedura di freeze post-inferenza:**

1. Aggregare tutte le 45 risposte con la stessa regola di maggioranza R=3
   (≥ 2 label uguali) tramite `aggregation_c.py`.
2. Salvare le predizioni aggregate in `full_evaluation/predictions/`.
3. Congelare in `predictions_manifest.json`:
   - Hash SHA-256 di `icl/inference/c_records.jsonl` (JSONL grezzo completo).
   - Hash SHA-256 delle predizioni aggregate.
   - Conteggi: 45 record di ripetizione, 15 predizioni aggregate.
   - `status: "IMMUTABLE_BEFORE_EVALUATION"`.
4. **Solo dopo il freeze delle predizioni:** eseguire il join evaluator-side
   con la ground truth tramite `evaluate_c_predictions.py` (che verifica
   il freeze manifest evaluator-side) e calcolare le metriche.

### 3.8 Step 7 — Valutazione C-Full

**Metriche:**

- `accuracy_C_fault`: predizioni corrette sui 12 held-out fault case.
- `accuracy_C_normal`: predizioni corrette sui 3 held-out Normal case
  (sanity: atteso ≈ 1.0).
- `delta_C_minus_B`: confronto descrittivo (formula in §5.2).

Salvare in `full_evaluation/evaluation_results_c.json`.

---

## 4. Costi stimati

| Fase | Entry | Costo | Tempo |
|---|---|---|---|
| C-Pilot | 15 | < $2 | ~10 min |
| Resto C-Full | 30 | ~$3–5 | ~25 min |
| **Totale C-Full** | **45** | **~$5–7** | **~35 min** |

---

## 5. Piano statistico

### 5.1 Unità statistica

L'unità indipendente è il **physical case** (run fisico TEP). C-Full ha
12 case fault indipendenti, 3 per ciascuna delle 4 pseudolabel.

### 5.2 Confronto C−B

Il confronto è **descrittivo** (non un contrasto sperimentale entro la stessa
sessione temporale). Il delta è definito come:

$$\Delta_{C-B} = \frac{1}{12} \sum_{i=1}^{12} \left[ \mathbb{1}(C_i = y_i) - \frac{1}{|U_i|} \sum_{a \in U_i} \mathbb{1}(B_{ia} = y_i) \right]$$

dove:
- $C_i$ è la predizione aggregata (majority R=3) di C sul physical case $i$.
- $y_i$ è la classe vera del physical case $i$.
- $U_i$ è l'insieme dei 3 agenti per cui il case $i$ è unseen in Exp 1.
- $B_{ia}$ è la predizione aggregata di B dell'agente $a$ sul case $i$.

Le predizioni B sono caricate da
`phase_b/final_evaluation/inference/aggregate_records.jsonl` (filtrate per
`condition=="B"`), la cui integrità è verificata tramite
`inference_output_hash_manifest.json`.

Nessuna replica virtuale di C: una sola predizione C per case, confrontata
con la media delle 3 predizioni B (agent-case) sullo stesso case.

### 5.3 Cluster bootstrap

- **Resampling:** 10000 draw.
- **Seed:** 20260906.
- **Stratificazione:** per pseudolabel vera (3 cluster per pseudolabel).
- **Unità resampled:** physical case (si resampla il case e con esso sia la
  predizione C sia le 3 predizioni B).
- **CI:** 95%, percentile method.

### 5.4 C-Pilot

Il pilot contiene solo 4 fault cluster (1 per pseudolabel). Nessuna metrica
prestazionale è calcolata nel pilot; le risposte restano blind fino al freeze
di tutte le predizioni C.

---

## 6. Limiti da dichiarare nel paper

### 6.1 Asimmetria informativa

C riceve più informazione di B: 10 vs 4 esempi, 8 vs 6 insight, copertura
diretta di tutte le classi vs copertura indiretta tramite insight. Quantità,
forma e struttura del contesto cambiano simultaneamente. Il delta C−B non
isola un singolo fattore e non può essere interpretato causalmente. C è un
riferimento empirico, non una condizione sperimentale a parità di informazione.

### 6.2 Prompt length

Il prompt C è più lungo del prompt B. Documentare la differenza in caratteri
e, se possibile, in token.

### 6.3 Confounding temporale

C è eseguita in un momento diverso da A/B/E. Con lo stesso modello
(`gpt-5.6-terra`) e la stessa configurazione, drift del servizio potrebbe
contribuire a differenze osservate. Il delta C−B è dichiarato descrittivo
e temporalmente confondibile. Una mitigazione opzionale (re-esecuzione di
B contemporanea a C, con ordine controbilanciato) è possibile ma non
pianificata per il pilot.

### 6.4 C come riferimento post-hoc, non come metodo

C non è un metodo proposto — è il riferimento empirico post-hoc che mostra la
performance con informazione prompt-facing completa centralizzata. Non è un
upper bound garantito (effetti di contesto possono far sì che C < B).
Terminologia nel paper: "centralized full-information pooled ICL reference".

"Full-information" si riferisce esclusivamente all'unione degli artefatti
prompt-facing frozen (i 10 esempi etichettati e gli 8 insight testuali),
non alla totalità dei testi sorgente del TEP né ad alcun artefatto non
incluso nei file frozen.

### 6.5 Natura post-hoc

La condizione C è stata progettata **dopo** aver osservato i risultati delle
condizioni A, B ed E sullo stesso held-out set. Questo implica:

1. **C non è una condizione pianificata ex ante.** Il confronto C−B è
   esplorativo, non confermativo.
2. **Rischio di data-snooping:** avendo osservato che B raggiunge 0.861 sui
   fault unseen, la scelta di aggiungere un riferimento centralizzato è
   informata dai risultati. Il piano mitiga questo rischio congelandone il
   disegno (amendment, schedule, artefatti) prima di qualsiasi inferenza C.
3. **Terminologia nel paper:** C va introdotta come "post-hoc exploratory
   reference" e il confronto C−B come "descriptive comparison". Non usare
   linguaggio confermativo (es. "we test the hypothesis that...").
4. **Il firewall ground truth (§3.6, §3.7) mitiga parzialmente** il rischio:
   le predizioni C sono congelate prima del join con le label vere, quindi il
   risultato C non è adattato ai dati. Tuttavia, la *decisione* di eseguire C
   è informata dai risultati osservati.

---

## 7. Vincoli e guardrail

1. **Nessuna modifica ai dati frozen di Exp 1.** I risultati A/B/E restano
   intatti; C è un esperimento aggiuntivo.

2. **Amendment e freeze manifest congelati prima di qualsiasi inferenza.**

3. **Stesso modello e configurazione.** `gpt-5.6-terra`, `medium`, structured
   output strict.

4. **Stessa regola di aggregazione.** R=3, maggioranza ≥ 2.

5. **Leakage scanner attivo.** Ogni prompt C viene scansionato.

6. **Nessun tuning o selezione adattiva.** Esempi e insight sono quelli frozen.
   Il gate pilot→full è solo tecnico.

7. **Firewall ground truth.** Nessun join con ground truth fino al freeze di
   tutte le predizioni C (pilot + resto). Le raw response del pilot restano
   blind.

8. **Pseudolabel opache.** Nessuna modifica allo spazio delle label.

9. **Schedule unica pre-frozen.** La schedule C-Full request-level (45 entry,
   con tag pilot) è congelata con hash prima della prima inferenza.

10. **Infrastruttura separata.** Nessuna patch ai file frozen di Exp 1:
    runner, record, schema e aggregation di C sono file nuovi nella directory
    `icl/`, congelati nel loro proprio manifest.

11. **Freeze guard a runtime — separazione inference/evaluator.**
    - **Inference-side:** prima di ogni tranche (pilot e full), il runner
      verifica gli hash SHA-256 di tutti gli artefatti nel
      `freeze_manifest_inference.json`, inclusi i 15 file
      `neutral_text/PBH-XXX.txt` verificati per-case tramite i campi
      `neutral_text_sha256` di `heldout_verbalizations_manifest.json`.
      Se un hash non corrisponde, il runner abort con errore esplicito.
    - **Evaluator-side:** `evaluate_c_predictions.py` verifica gli hash nel
      `freeze_manifest_evaluator.json` prima del join con ground truth.
      Include la verifica dell'integrità di `aggregate_records.jsonl` tramite
      `inference_output_hash_manifest.json`.
    - **Il runner NON accede al manifest evaluator-side.** L'evaluator NON
      accede al manifest inference-side. Questa separazione preserva il
      firewall: il runner non vede mapping pseudolabel né predizioni B;
      l'evaluator non altera gli artefatti di inferenza.

12. **Archivio canonico unico.** Tutte le raw response (pilot e full) sono
    scritte nello stesso file append-only `icl/inference/c_records.jsonl`.
    Non esistono archivi separati per pilot e full. Il runner è idempotente:
    una riesecuzione salta i `sequence_index` già presenti nel JSONL.

13. **Freeze post-inferenza.** Dopo il completamento di C-Full,
    `predictions_manifest.json` congela con hash sia il JSONL grezzo
    (`c_records.jsonl`) sia le predizioni aggregate, rendendo immutabile
    l'intera provenance prima dell'evaluation.

---

## 8. Checklist

### Preparazione (pre-inferenza)

- [x] Creare la struttura directory `icl/`
- [x] Copiare e verificare il template `pooled_C.txt`
- [x] Generare `pooled_examples.json` (10 record)
- [x] Generare `pooled_insights.json` (8 insight)
- [x] Scrivere `condition_c_config.json`
- [x] Implementare `builder_c.py`
- [x] Scrivere e passare `test_builder_c.py`
- [x] Implementare `records_c.py` (con `parsed_output` completo e provenienza per-attempt) + `c_run_record.schema.json`
- [x] Scrivere e passare `test_records_c.py`
- [x] Implementare `build_c_schedule.py` (45 entry, ordinamento `pilot DESC, physical_case_id ASC, repetition ASC`)
- [x] Scrivere e passare `test_build_c_schedule.py` (verifica 45 entry, 15 pilot in 0..14, ordinamento corretto)
- [x] Implementare `run_c_inference.py` (con freeze guard inference-side e resume/idempotenza)
- [x] Scrivere e passare `test_run_c_inference.py` (resume, idempotenza, freeze guard inference-side, no accesso evaluator-side)
- [x] Implementare `aggregation_c.py` (output compatibile con `aggregate_records.jsonl` di Exp 1)
- [x] Scrivere e passare `test_aggregation_c.py`
- [x] Implementare `evaluate_c_predictions.py` (carica B da `aggregate_records.jsonl`, freeze guard evaluator-side)
- [x] Scrivere e passare `test_evaluate_c_predictions.py`
- [x] Generare `c_schedule.json` (45 entry con subset pilot marcato `pilot=true`)
- [x] Redigere `protocol_amendment_c.md/.json`
- [x] Calcolare SHA-256 in `freeze_manifest_inference.json` e `freeze_manifest_evaluator.json`
- [x] Commit e tag di freeze

### C-Pilot (prima tranche blind)

- [x] Eseguire `run_c_inference.py --pilot-only` (15 entry → `c_records.jsonl`)
- [x] Verificare i 5 gate tecnici (NO metriche, NO ground truth)
- [x] Decisione go/no-go puramente tecnica

### Completamento C-Full

- [x] Eseguire `run_c_inference.py` (30 entry rimanenti → stesso `c_records.jsonl`)
- [x] Verificare che `c_records.jsonl` contenga esattamente 45 record
- [x] Aggregare tutte le predizioni con `aggregation_c.py`
- [x] Congelare `c_records.jsonl` + predizioni aggregate in `c_predictions_manifest.json` e `c_aggregate_manifest.json`
- [x] Join evaluator-side con ground truth via `evaluate_c_predictions.py`
- [x] Calcolare accuracy C e delta C−B con cluster bootstrap
- [x] Salvare `evaluation_results_c.json`
- [ ] Aggiornare la sezione Results del paper

### Chiusura esecutiva R10

L'esecuzione e la valutazione sono concluse e congelate attraverso la seguente
catena Git:

| Milestone | Tag | Commit |
|---|---|---|
| Code freeze | `condition-c-freeze-r10` | `60ccc7539714e909aae7318cc72031d7acdd4e78` |
| Predictions freeze | `condition-c-predictions-frozen-r10` | `8d6b7a0636e9a15f0ebbd32ed0f9e2ce4faea30a` |
| Results freeze | `condition-c-results-frozen-r10` | `89e4caebe635973ef438d4b601bb4f761417193a` |

Il risultato canonico è
[`full_evaluation/evaluation_results_c.json`](full_evaluation/evaluation_results_c.json).
La
[`review indipendente`](../docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md)
ha espresso il verdetto **GO WITH LIMITATIONS**. Restano aperte esclusivamente
l'integrazione interpretativa nella sezione Results del paper e il successivo
aggiornamento del walkthrough; nessuna ulteriore inferenza o valutazione è
richiesta per Condition C R10.
