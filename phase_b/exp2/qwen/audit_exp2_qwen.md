# Audit indipendente — branch `codex/exp2-qwen`

**Data:** 2026-09-08  
**Autorità scientifica:** `docs/fot_walkthrough_conversazione.md`, Step 27  
**Commit auditato:** `b4bb61fbf49ab30b6809c341df9d45a1c28e9e49`  
**Branch:** `origin/codex/exp2-qwen`  
**Modalità:** read-only, nessun file modificato, nessuna inferenza eseguita

---

## Riepilogo

| # | Punto di verifica | Esito |
|---|---|---|
| 1 | Frozen artefact integrity | PASS |
| 2 | Protocol equivalence (prompt/conditions/examples/agents/R=3) | PASS |
| 3 | Consumer-only modification | PASS |
| 4 | Inference parameters (temperature, seed, max_tokens, reasoning_effort) | PASS con riserva |
| 5 | Raw / reasoning_content / content separation | MAJOR |
| 6 | Heldout / evaluator leakage | PASS |
| 7 | Synthetic-only probes | PASS |
| 8 | Qwen tokenizer / chat template | PASS |
| 9 | Retry / resume / truncation / JSON validation | **BLOCKER** |
| 10 | Unchanged aggregation / evaluator / bootstrap reuse | PASS |
| 11 | Hash / manifest traceability | PASS |
| 12 | Probe status coerente con il codice | PASS (probe correttamente FAIL) |

---

## Verdetto

# NO-GO per il freeze del protocollo

La condizione E è sistematicamente troncata: il modello esaurisce il budget `max_tokens=512` nella sola catena di ragionamento interna senza mai emettere il JSON di risposta. Questo invalida il test di specificità semantica (B vs E), che è uno dei due claim primari di Experiment 2.

---

## Finding 1 — BLOCKER

**E-condition: troncamento sistematico per esaurimento token di ragionamento**

- **File:** `phase_b/exp2/qwen/config.json:14` (`max_tokens: 512`)
- **File:** `phase_b/exp2/qwen/adapter.py:96` (parametro `max_tokens` passato a `chat.completions.create`)
- **Evidenza dal probe** (`phase_b/exp2/qwen/probe/capability_probe.json`):
  - Condizione A: 1 tentativo, `finish_reason=stop`, reasoning=1057 chars, content=387 chars. **PASS.**
  - Condizione B: 2 tentativi. Tentativo 0: `finish_reason=length`, reasoning_tokens=512, content=None. Tentativo 1 (con correction suffix): `finish_reason=stop`, reasoning_tokens=395, content=405 chars. **PASS marginale.**
  - Condizione E: 3 tentativi, **tutti** `finish_reason=length`, reasoning_tokens=512, content=None. Reasoning chars: 1858 → 2026 → 2026. **FAIL sistematico.**
  - Probe `checks.all_outputs_schema_valid: false`, `checks.no_length_truncation: false`
  - Probe `status: "FAIL"`
- **Meccanismo:** vLLM applica `max_tokens` come limite *combinato* su reasoning_tokens + content tokens (`completion_tokens_details.reasoning_tokens = 512` = totale). Il ragionamento interno del modello sui corrupted insights della condizione E è sistematicamente più lungo di 512 token, non lasciando budget residuo per il JSON di output. Il retry con correction suffix non aiuta: il ragionamento cresce anziché ridursi (1858 → 2026 chars).
- **Conseguenza:** Tutte le 180 chiamate E produrranno `parse_failure` → `abstain=True, predicted_label=None`. L'evaluator tratta le astensioni come errori, quindi accuracy(E) ≈ 0%. Il delta_specificity (B−E) sarà gonfiato artificialmente: rifletterà un artefatto tecnico (troncamento), non una confusione genuina del modello causata dagli insight corrotti. Il test di specificità semantica — pilastro scientifico di Experiment 2 — è invalidato.
- **Fix minimo:** Aumentare `max_tokens` ad almeno 1024 per accomodare reasoning + JSON. Alternativa: utilizzare il parametro vLLM `--max-tokens-thinking` (se supportato nella versione 0.28.0) per separare i budget reasoning e content. Dopo la modifica, rieseguire il capability probe e verificare che E produca `finish_reason=stop` con content non-null.

---

## Finding 2 — MAJOR

**Estrazione `reasoning_content` sempre `None`: field naming mismatch con vLLM**

- **File:** `phase_b/exp2/qwen/adapter.py:112-118`
- **Codice attuale:**
  ```python
  reasoning = getattr(message, "reasoning_content", None)
  if reasoning is None:
      extra = getattr(message, "model_extra", None)
      if isinstance(extra, dict):
          reasoning = extra.get("reasoning_content")
  ```
- **Evidenza:** Il `response_raw` del probe mostra che vLLM restituisce la catena di ragionamento nel campo `choices[0].message.reasoning` (nome `reasoning`), non `reasoning_content`. Per tutte e tre le condizioni, `ChatProviderResponse.reasoning_content` risulta `None` anche quando il modello ha prodotto centinaia/migliaia di caratteri di reasoning.
- **Fattore mitigante:** Il reasoning completo **è** preservato in `response_raw`, che viene salvato integralmente nel record. Non si tratta di perdita di dati. Tuttavia, il campo dedicato `reasoning_content` nel `ChatProviderResponse` e quindi nel `RunRecord` sarà sempre `None`, rendendo l'analisi post-hoc del ragionamento più laboriosa (bisogna estrarre da `response_raw` anziché dal campo diretto).
- **Conseguenza:** Nessun impatto sulla correttezza dell'inferenza o della valutazione (che usa solo `raw_output` / `parsed_output`). Impatto sulla qualità dei metadati e sulla facilità di analisi post-hoc.
- **Fix minimo:** Aggiungere un fallback nel blocco di estrazione:
  ```python
  if reasoning is None and isinstance(extra, dict):
      reasoning = extra.get("reasoning")
  ```

---

## Finding 3 — MINOR

**Condizione B: budget token marginale, retry non deterministic**

- **File:** `phase_b/exp2/qwen/config.json:14` (`max_tokens: 512`)
- **Evidenza:** Nel probe, B attempt 0 esaurisce 512 token in reasoning (content=None, `finish_reason=length`). Attempt 1 con correction suffix riesce (395 reasoning + 101 content = 496 token). Il correction suffix induce il modello a ragionare più brevemente.
- **Conseguenza:** Alcune chiamate B richiederanno 2 tentativi, altre 1, a seconda della lunghezza del ragionamento per quel caso specifico. Questo non invalida i risultati (il retry è deterministico con temperature=0 + seed) ma introduce eterogeneità nel numero di tentativi. Con `max_tokens` aumentato per il fix del blocker, anche questo problema si risolve.

---

## Punti di verifica: dettaglio

### 1. Frozen artefact integrity — PASS

`git diff --name-status main...origin/codex/exp2-qwen` mostra esclusivamente 17 file con status `A` (added), tutti sotto `phase_b/exp2/`. Nessun file esistente è stato modificato. Le 10 entry in `frozen_input_hashes` di `config.json` coprono tutti gli artefatti frozen (template di prompt, insight, esempi locali, derangements, schema JSON, aggregation.py, bootstrap.py, manifest delle verbalizzazioni). La funzione `verify_frozen_hashes()` in `common.py` li valida all'avvio con SHA-256.

### 2. Protocol equivalence — PASS

- **Prompt:** Tutte le 180 hash dei prompt unici corrispondono agli originali di Experiment 1 (`prompt_budget.all_prompt_hashes_match_original: true`). La funzione `original_prompt_hashes()` in `common.py` estrae le 180 mappature (case, agent, condition) → prompt_hash dal `repetition_records.jsonl` originale e le confronta con i prompt renderizzati per Qwen.
- **Condizioni A/B/E:** I tre template sono intenzionalmente identici (stessa struttura); `_load_equivalent_template()` in `builders.py` lo verifica esplicitamente con `if len(set(contents.values())) != 1: raise RuntimeError(...)`. La differenziazione avviene tramite il placeholder `<<PEER_INSIGHTS_BLOCK>>` (vuoto per A, insight reali per B, deranged per E).
- **Esempi locali:** Stessi `local_examples.json` (hash: `468d51b7...`).
- **4 agenti:** `AGENT_PACK = {"agent_1":"LKP-001", ..., "agent_4":"LKP-004"}` in `common.py`.
- **R=3:** `config.json` dichiara `repetitions: 3`. `validate_schedule()` in `run_frozen_inference.py` forza esattamente 540 entry, A:180/B:180/E:180, indici sequenziali 0–539.

### 3. Consumer-only modification — PASS

Solo `phase_b/exp2/` contiene file nuovi. Il producer (gpt-5.6-terra) non è toccato. Gli insight frozen sono gli stessi di Experiment 1 (hash: `b7ea847c...`).

### 4. Inference parameters — PASS con riserva

| Parametro | Valore | Conforme a Step 27? |
|---|---|---|
| temperature | 0.0 | Sì ("temperature 0") |
| seed | 20260829 | Sì ("seed fisso") |
| max_tokens | 512 | Valore identico a Exp1, ma insufficiente per Qwen3 reasoning (vedi Blocker) |
| reasoning_effort | null | **Sì** — Step 27 menziona reasoning_effort=medium solo per gpt-5.6-terra (producer). Non è un parametro applicabile a vLLM/Qwen. `reasoning_mode: "server_default_qwen3"` delega correttamente a `--reasoning-parser qwen3`. |

### 5. Raw / reasoning_content / content separation — MAJOR

Vedi Finding 2. Il campo `raw_output` (= `content`) è correttamente estratto. Il `response_raw` è integro. Solo l'estrazione dedicata di `reasoning_content` è nulla per mismatch di nome campo.

### 6. Heldout / evaluator leakage — PASS

Il probe certifica:
- `heldout_predictions_generated: false`
- `ground_truth_accessed: false`
- `full_experiment_calls_made: 0`
- `fixture.contains_heldout_case_text: false`
- `fixture.contains_ground_truth: false`

### 7. Synthetic-only probes — PASS

`capability_probe.py` genera un caso sintetico tramite `synthetic_case()`. Nessun dato heldout è utilizzato nelle fixture. `performance_metrics_calculated: false`.

### 8. Qwen tokenizer / chat template — PASS

vLLM command line verificata dal probe:
```
vllm serve Qwen/Qwen3.8-27B-FP8 \
  --revision 017b9c7af6b5689d5dd426a76e0bc077eb5ca20a \
  --reasoning-parser qwen3 \
  --language-model-only \
  --seed 20260829 \
  --max-model-len 4096 \
  --served-model-name fot-exp2-consumer
```

Probe `checks`: `vllm_version_matches: true`, `model_root_matches: true`, `model_revision_matches_process: true`, `returned_model_matches: true`.

### 9. Retry / resume / truncation / JSON validation — BLOCKER su truncation

- **Retry:** Riutilizza `execute_with_retry` da `phase_b.conditions.retry` con `max_retries=2`. Invariato.
- **Resume:** `load_existing()` valida i record esistenti prima di riprendere.
- **JSON validation:** Usa `parse_diagnostic_output` + `json_schema` strict server-side. Invariato.
- **Truncation:** Vedi Finding 1. E-condition sistematicamente troncata.

### 10. Aggregation / evaluator / bootstrap reuse — PASS

- `aggregation.py` hash in frozen_input_hashes: `ce44166f...`
- `bootstrap.py` hash in frozen_input_hashes: `524751fe...`
- `evaluate_qwen.py` monkey-patcha solo `AGGREGATE_PATH` e `verify_frozen_inputs`, poi chiama `build_results()` e `render_report()` invariati.
- Nessuna reimplementazione di aggregazione, bootstrap o metriche.

### 11. Hash / manifest traceability — PASS

`config.json` lista 10 hash frozen. `verify_frozen_hashes()` valida schedule + tutti gli input frozen. `run_frozen_inference.py` produce `inference_output_hash_manifest.json` con status `IMMUTABLE_BEFORE_OFFLINE_EVALUATION`. `evaluate_qwen.py` verifica il manifest Qwen prima della valutazione.

### 12. Probe status — PASS (coerente)

Il probe dichiara `status: "FAIL"`, coerente con `all_outputs_schema_valid: false` e `no_length_truncation: false`. I check che passano (10 su 12) sono genuini. Il probe *non* nasconde il problema; lo segnala esplicitamente.

---

## Checklist test unitari

I 14 test (`test_contracts.py`, `test_adapter.py`, `test_common.py`, `test_probe_artifact.py`) sono dichiarati tutti PASS dal commit message. Nota: `test_adapter.py` usa un mock `FakeCompletions` che restituisce `reasoning_content` come attributo diretto — questo maschera il field naming mismatch con vLLM reale (Finding 2).

---

## Tabella riassuntiva findings

| # | Severità | Titolo | File:riga | Fix minimo |
|---|---|---|---|---|
| 1 | **BLOCKER** | E-condition troncamento sistematico | `config.json:14`, `adapter.py:96` | `max_tokens` ≥ 1024, o separare budget reasoning/content |
| 2 | MAJOR | `reasoning_content` sempre None | `adapter.py:112-118` | Aggiungere fallback `extra.get("reasoning")` |
| 3 | MINOR | B-condition budget marginale | `config.json:14` | Risolto implicitamente dal fix di #1 |

---

## Conclusione

**NO-GO.** Il blocker #1 invalida la metà "specificità semantica" del design sperimentale: con tutte le risposte E troncate, il confronto B vs E non misura l'effetto degli insight corrotti ma un artefatto di budget token. Prima del freeze:

1. Risolvere il blocker: aumentare `max_tokens` o separare i budget.
2. Rieseguire il capability probe fino a `status: "PASS"` su tutte e tre le condizioni.
3. Correggere il field naming del reasoning (major #2).
4. Sottoporre a re-audit.
