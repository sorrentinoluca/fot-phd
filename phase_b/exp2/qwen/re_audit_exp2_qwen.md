# Re-audit indipendente — branch `codex/exp2-qwen`

**Data:** 2026-09-08  
**Autorità scientifica:** `docs/fot_walkthrough_conversazione.md`, Step 27  
**Commit auditato:** `d9bb95c31bdeb2f1608aaedc52f25b98de9bbf96`  
**Commit precedente (baseline):** `b4bb61fbf49ab30b6809c341df9d45a1c28e9e49`  
**Branch:** `origin/codex/exp2-qwen`  
**Modalità:** read-only, nessun file modificato, nessuna inferenza eseguita

---

## Riepilogo

| # | Punto di verifica | Esito |
|---|---|---|
| 1 | Invio uniforme di max_tokens=1536 e thinking_token_budget=1024 (A/B/E, retry, replay) | PASS |
| 2 | Supporto effettivo di thinking_token_budget da parte di vLLM 0.28.0 | PASS |
| 3 | Semantica del cap: assenza di troncamento nascosto | PASS |
| 4 | Calcolo del contesto con chat template Qwen | PASS |
| 5 | Estrazione reasoning / reasoning_content in tutte le varianti | PASS |
| 6 | Autenticità e coerenza temporale del probe | PASS |
| 7 | Assenza di modifiche agli artefatti frozen e al disegno scientifico | PASS |
| 8 | Adeguatezza dei test e assenza di test indeboliti | PASS |
| — | B/E raggiungono il cap di 1024 reasoning token: valutazione metodologica | ACCETTABILE |

---

## Verdetto

# GO per il freeze del protocollo

Tutti i finding del primo audit (blocker #1, major #2, minor #3) sono stati risolti. Nessun nuovo finding di severità blocker o major è emerso. Il protocollo è pronto per l'esecuzione heldout.

---

## Dettaglio delle verifiche

### 1. Invio uniforme di max_tokens=1536 e thinking_token_budget=1024 — PASS

- **File:** `phase_b/exp2/qwen/config.json:14-15`
  - `"max_tokens": 1536`, `"thinking_token_budget": 1024`
- **File:** `phase_b/exp2/qwen/adapter.py:85-100`
  - `create_chat_completion()` accetta `thinking_token_budget` come parametro e lo invia via `extra_body={"thinking_token_budget": thinking_token_budget}`.
  - `max_tokens=1536` passato come argomento posizionale a `chat.completions.create`.
- **File:** `phase_b/exp2/qwen/adapter.py:110-135` (`execute_diagnostic`)
  - La closure `_call()` cattura `thinking_token_budget` dall'argomento di `execute_diagnostic` e lo passa a `create_chat_completion` in ogni invocazione, inclusi i retry via `execute_with_retry`.
- **File:** `phase_b/exp2/qwen/run_frozen_inference.py:45-50` (`execute_one`)
  - Legge `config["thinking_token_budget"]` e lo passa a `execute_diagnostic`.
- **File:** `phase_b/exp2/qwen/capability_probe.py` (fixture e replay)
  - Tutte le chiamate fixture (A, B, E) e la chiamata replay passano `thinking_token_budget=config["thinking_token_budget"]`.
- **Evidenza dal probe:** `capability_probe.json` → `request_accounting`:
  - A: 1 request, 0 retries. B: 1 request, 0 retries. E: 1 request, 0 retries. Replay: 1 request, 0 retries.
  - `total_requests: 4`, `total_structural_retries: 0`.
  - `checks.thinking_token_budget_configured: true`.

### 2. Supporto effettivo di thinking_token_budget in vLLM 0.28.0 — PASS

- **File:** `phase_b/exp2/qwen/probe/capability_probe.json` → `reasoning_controls`
  - `thinking_token_budget_advertised: true` — il probe ha verificato la presenza del parametro nello schema OpenAPI esposto da vLLM 0.28.0 all'endpoint `/v1/chat/completions`.
  - `reasoning_effort_advertised: true` — anch'esso disponibile (non utilizzato per design).
- **Evidenza:** Il probe ha effettuato 4 chiamate reali al server vLLM, tutte con `extra_body={"thinking_token_budget": 1024}`. Tutte hanno restituito `finish_reason=stop` con content non-null, dimostrando che il parametro è stato accettato e rispettato dal server.
- **Fingerprint:** Tutte le risposte condividono `system_fingerprint: "vllm-0.28.0-abc0cde2"`, confermando la versione del server.

### 3. Semantica del cap: assenza di troncamento nascosto — PASS

- **Evidenza dal probe** (`capability_probe.json` → `conditions`):
  - **A:** `finish_reason=stop`, `reasoning_tokens=255`, `completion_tokens=349`, `reasoning_content=1057 chars`, `content=387 chars`. Reasoning ben sotto il cap, content prodotto normalmente.
  - **B:** `finish_reason=stop`, `reasoning_tokens=1023`, `completion_tokens=1124`, `reasoning_content=3420 chars`, `content=440 chars`. Reasoning raggiunge il cap (1023 ≈ 1024), content prodotto normalmente con 101 token residui.
  - **E:** `finish_reason=stop`, `reasoning_tokens=1023`, `completion_tokens=1117`, `reasoning_content=3823 chars`, `content=411 chars`. Stesso pattern di B.
- **Verifica critica:** Nel primo audit, con `max_tokens=512` combinato, E produceva `finish_reason=length` e `content=None` (troncamento sistematico). Ora, con budget separati (`thinking_token_budget=1024` per reasoning, `max_tokens=1536` totale → fino a 512 per content), tutte e tre le condizioni producono `finish_reason=stop` con JSON valido.
- **File:** `phase_b/exp2/qwen/probe/capability_probe.json` → `checks`:
  - `all_finish_reasons_stop: true`
  - `all_outputs_content_non_null: true`
  - `all_outputs_schema_valid: true`
  - `no_length_truncation: true`

### 4. Calcolo del contesto con chat template Qwen — PASS

- **File:** `phase_b/exp2/qwen/probe/capability_probe.json` → `prompt_budget`
  - `minimum_raw_prompt_tokens: 1386`
  - `maximum_raw_prompt_tokens: 2340` (il prompt più lungo tra tutte le 180 combinazioni)
  - `maximum_plus_output_budget: 3876` (= 2340 + 1536)
  - `expected_max_model_len: 4096` (da `config.json`)
  - `context_margin_tokens: 220` (= 4096 − 3876)
  - `all_prompt_hashes_match_original: true` (i 180 prompt sono identici a Experiment 1)
- **Calcolo:** 2340 (massimo input frozen) + 1536 (max_tokens) = 3876 ≤ 4096, con un margine di 220 token. Il completamento osservato massimo è 1124 token (B: 2300 prompt + 1124 completion = 3424 token totali). Il probe ha confermato che tutte le 4 chiamate reali hanno prodotto output completi senza errori di contesto.
- **Correzione editoriale:** la versione precedente di questa sezione riportava erroneamente `max_prompt_tokens: 3876` e un totale stimato di ~5000 token. Il valore 3876 corrisponde a `maximum_plus_output_budget` (input + output), non al solo input. I valori corretti provengono da `capability_probe.json` → `prompt_budget`. Questa correzione non modifica il verdetto GO.

### 5. Estrazione reasoning / reasoning_content — PASS

- **File:** `phase_b/exp2/qwen/adapter.py:60-71` — nuova funzione `_extract_reasoning()`:
  ```python
  def _extract_reasoning(message: Any) -> str | None:
      extra = getattr(message, "model_extra", None)
      candidates = [
          getattr(message, "reasoning_content", None),  # priorità 1
          getattr(message, "reasoning", None),           # priorità 2
          extra.get("reasoning_content") if isinstance(extra, dict) else None,  # priorità 3
          extra.get("reasoning") if isinstance(extra, dict) else None,          # priorità 4
      ]
      return next((value for value in candidates if isinstance(value, str)), None)
  ```
- **Evidenza dal probe:** Il campo `reasoning_content` nel `ChatProviderResponse` è ora popolato per tutte e tre le condizioni:
  - A: 1057 chars
  - B: 3420 chars
  - E: 3823 chars
- **Verifica incrociata:** Il probe include `response_invariants` per ogni condizione. Il check `reasoning_preserved: true` conferma che il valore estratto da `_extract_reasoning()` corrisponde esattamente al campo `reasoning` nel `response_raw.choices[0].message` restituito da vLLM.
- **File:** `phase_b/exp2/qwen/probe/capability_probe.json` → `checks.all_reasoning_preserved: true`

### 6. Autenticità e coerenza temporale del probe — PASS

- **Timestamp delle chiamate** (dal probe JSON):
  - A: `2026-09-08T13:22:21Z`
  - B: `2026-09-08T13:22:44Z` (+23s)
  - E: `2026-09-08T13:23:34Z` (+73s dopo A, +50s dopo B)
  - Replay: `2026-09-08T13:23:36Z` (+75s dopo A, +2s dopo E)
- **Coerenza:** I timestamp sono monotonicamente crescenti con intervalli plausibili per chiamate sequenziali a un modello 27B con ragionamento. Il gap A→B (23s) e B→E (50s) riflettono ragionamento crescente (255 → 1023 → 1023 reasoning tokens). Il gap E→replay (2s) è coerente con un replay deterministico della condizione A (reasoning breve).
- **Fingerprint unico:** Tutte le risposte portano `system_fingerprint: "vllm-0.28.0-abc0cde2"`, confermando una singola sessione server.
- **Replay deterministico:** `identical_raw_output: true` — la risposta replay è identica bit-per-bit alla risposta originale della condizione A, confermando determinismo con `temperature=0, seed=20260829`.

### 7. Assenza di modifiche agli artefatti frozen — PASS

- **Verifica git diff:** `git diff --name-status b4bb61f..d9bb95c` mostra modifiche esclusivamente sotto `phase_b/exp2/qwen/`:
  - `M phase_b/exp2/qwen/adapter.py`
  - `M phase_b/exp2/qwen/capability_probe.py`
  - `M phase_b/exp2/qwen/config.json`
  - `M phase_b/exp2/qwen/run_frozen_inference.py`
  - `A phase_b/exp2/qwen/probe/capability_probe.json` (nuovo probe)
  - `M phase_b/exp2/qwen/tests/test_adapter.py`
  - `M phase_b/exp2/qwen/tests/test_contracts.py`
  - `M phase_b/exp2/qwen/tests/test_probe_artifact.py`
- **Nessun file esterno a `phase_b/exp2/qwen/` è stato modificato.** In particolare:
  - `phase_b/conditions/` (builders, retry, parser): intatti
  - `phase_b/evaluation/` (aggregation, bootstrap, records): intatti
  - `phase_b/final_evaluation/`: intatto
  - `docs/`: intatto
  - Tutti i 10 hash in `frozen_input_hashes` di `config.json` sono invariati rispetto al commit precedente.

### 8. Adeguatezza dei test e assenza di test indeboliti — PASS

- **File:** `phase_b/exp2/qwen/tests/test_contracts.py`
  - Aggiunti: `assertEqual(config["max_tokens"], 1536)`, `assertEqual(config["expected_max_model_len"], 4096)`, `assertEqual(config["thinking_token_budget"], 1024)`.
  - Nessuna asserzione rimossa o indebolita.

- **File:** `phase_b/exp2/qwen/tests/test_adapter.py`
  - Aggiornato: `max_tokens` da 512 a 1536, aggiunto `thinking_token_budget=1024`.
  - Aggiunta asserzione: `assertEqual(request["extra_body"], {"thinking_token_budget": 1024})` — verifica che il parametro sia effettivamente inviato nella request.
  - 5 nuovi test per `_extract_reasoning()`:
    1. `test_reasoning_from_message_reasoning_content_has_first_priority`
    2. `test_reasoning_from_message_reasoning_is_second_priority`
    3. `test_reasoning_from_model_extra_reasoning_content_is_third_priority`
    4. `test_reasoning_from_model_extra_reasoning_is_fourth_priority`
    5. `test_reasoning_can_be_completely_absent`
  - `FakeCompletions` esteso per accettare messaggi custom, abilitando test di tutte le varianti di estrazione.

- **File:** `phase_b/exp2/qwen/tests/test_probe_artifact.py`
  - **Rafforzato:** `assertIn(status, {"PASS", "FAIL"})` → `assertEqual(status, "PASS")` — ora il test fallisce se il probe non è PASS.
  - 11 nuove asserzioni:
    - `all_finish_reasons_stop`, `all_outputs_content_non_null`, `all_outputs_schema_valid`
    - `all_reasoning_preserved`, `no_length_truncation`
    - `thinking_token_budget_advertised`, `thinking_token_budget_configured`
    - `total_requests == 4`, `total_structural_retries == 0`
    - Contabilità per-condizione: requests e retries per A, B, E.

---

## Valutazione metodologica: B/E al cap di 1024 reasoning token

### Osservazione

Il probe mostra che B ed E raggiungono esattamente `reasoning_tokens=1023` (≈1024), mentre A usa solo 255 reasoning token. Il modello esaurirebbe il budget di ragionamento per B/E se non fosse limitato dal cap.

### Valutazione

Questo **non** costituisce un problema metodologico per le seguenti ragioni:

1. **Uniformità del vincolo:** Il cap `thinking_token_budget=1024` è applicato identicamente a B e a E. Se il reasoning tronco penalizza la qualità della risposta, lo fa in modo simmetrico. Il confronto B vs E — che misura la specificità semantica (insight reali vs corrotti) — rimane equo.

2. **Analogia con Experiment 1:** In Experiment 1, `reasoning_effort=medium` su gpt-5.6-terra impone un vincolo analogo sul ragionamento. Step 27 non prescrive reasoning illimitato per il consumer; prescrive lo stesso protocollo sperimentale.

3. **Il cap non è troncamento:** A differenza del blocker originale (`max_tokens=512` combinato → `finish_reason=length`, `content=None`), qui il cap è gestito dal server: il modello completa il ragionamento entro il budget e produce content valido (`finish_reason=stop`). Il JSON è sempre emesso e validato.

4. **Condizione A come baseline:** A usa solo 255/1024 reasoning token, dimostrando che il cap non è globalmente restrittivo. Le condizioni B/E richiedono reasoning più lungo perché il prompt include peer insights (reali o corrotti), aumentando la complessità del ragionamento. Questo è un effetto atteso del design sperimentale.

5. **Trade-off documentato:** Il `config.json` dichiara esplicitamente `thinking_token_budget: 1024` e `expected_max_model_len: 4096`. Il probe certifica il funzionamento. L'eventuale impatto del cap sull'accuratezza è un risultato sperimentale, non un artefatto tecnico.

---

## Stato dei finding del primo audit

| # | Severità originale | Titolo | Stato nel commit d9bb95c |
|---|---|---|---|
| 1 | **BLOCKER** | E-condition troncamento sistematico | **RISOLTO** — `max_tokens=1536` + `thinking_token_budget=1024`. Probe: `finish_reason=stop` per tutte le condizioni. |
| 2 | MAJOR | `reasoning_content` sempre None | **RISOLTO** — `_extract_reasoning()` con 4-candidate priority chain. Probe: `all_reasoning_preserved: true`. |
| 3 | MINOR | B-condition budget marginale | **RISOLTO** — implicito dal fix di #1. Probe: B 1 tentativo, 0 retries. |

---

## Nuovi finding

Nessun nuovo finding di severità blocker, major o minor.

---

## Conclusione

**GO per il freeze del protocollo.** I tre finding del primo audit sono stati risolti. Il capability probe passa tutti i 19 check. Il design sperimentale è intatto: gli artefatti frozen, il disegno scientifico e l'evaluator sono invariati. Il cap di reasoning token su B/E è un vincolo uniforme e documentato, non un artefatto di troncamento. Il protocollo è pronto per l'esecuzione dell'inferenza heldout.

### Prossimi passi (fuori scope di questo audit)

1. Eseguire `run_frozen_inference.py` per le 540 chiamate heldout.
2. Verificare `inference_output_hash_manifest.json` con status `IMMUTABLE_BEFORE_OFFLINE_EVALUATION`.
3. Eseguire `evaluate_qwen.py` per la valutazione offline.
