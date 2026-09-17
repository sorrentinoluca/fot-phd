PILOT TECHNICAL PASS CONFIRMED — R3 REQUIRED; T5 = NOT ESTABLISHED; READY FOR AUTHOR GO/NO-GO

# Verifica scientifica indipendente dell'esito `pilot-03`

## 1. Perimetro, riferimenti e significato del verdetto

La verifica è stata eseguita il 17 settembre 2026 nella finestra `b567`, con shell nativa macOS,
modello `gpt-6-astra` e reasoning `high`. Il runtime esaminato è
`/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03`.

Il codice di riferimento è stato letto dalla worktree
`/Users/luker/fot-tep/.worktrees/rem6-riconciliazione`:

- commit `d3f8f844e5be4244477fc294ca754528e6938b15`;
- tree `6f62f5ea5e494c582c19b71365bb0f87193c8f6a`;
- parent `20ecfd8f6c6ffb9816d1ec25dd3a48e2c6667959`;
- subject `studio2(fase03): rifiuta retry di altro stage e binding su revisione superata`.

Il ledger è stato aperto esclusivamente con `sqlite3` sull'URI
`file:.../ledger.sqlite3?mode=ro&immutable=1`; non è stato istanziato `PilotLedger`. Non sono state
effettuate chiamate a provider, aperture di tunnel, retry, resume, remediation o modifiche al
runtime. L'unica scrittura della review è questo verbale.

Il verdetto conferma l'esito tecnico del pilot, non concede un GO allo studio e non modifica il
campo durevole `go_final=false`. La divergenza osservata rende obbligatorio `R=3`. T5 resta
`NOT ESTABLISHED`: le latenze sono state misurate e proiettate, ma il piano richiede anche il
conteggio completo per blocco/modello e una finestra operativa effettiva `W`, oggi non fissati.

## 2. Ledger, lineage e quote

La lettura diretta delle tabelle `requests` e `predecessor_lineage` dà:

| Stage | Righe native | `COMPLETED` | `ZERO_TOKEN_PROVEN` | `FAILED` | Lettura contabile |
| --- | ---: | ---: | ---: | ---: | --- |
| `technical_qualification_122b` | 1 | 1 | 0 | 0 | 1 quota `technical` |
| `producer_conformity` | 8 | 8 | 0 | 0 | 8 quote `base` |
| `producer_remediation` | 10 | 8 | 2 | 0 | 8 quote `remediation`; 2 quote `transport`, una zero-token e una completata |
| `alternate_conformity` | 14 | 9 | 5 | 0 | 8 output finali (1 `requalification` + 7 `base`), 1 antecedente `transport` completato, 5 tentativi zero-token |
| `budget_probe` | 3 | 3 | 0 | 0 | primo tripletto candidato sufficiente |
| `stability_gate` | 120 | 119 | 0 | 1 | nessun retry; l'unico `FAILED` è una invalidità di trasporto |
| **Totale nativo** | **156** | **148** | **7** | **1** | tutti gli intent sono terminali |

La lineage contiene cinque righe: una `HISTORICAL_OUTCOME_UNCERTAIN`, tre `COMPLETED` e una
`COMPLETED_IDENTITY_INVALID_ANTECEDENT_CONFIGURATION`. Il totale cumulativo è quindi
`156 + 5 = 161` intent. Il massimo pianificato con alternativo e requalification è
`160 + 1 successor + 5 predecessor + 1 requalification = 167`; l'hard stop è 200. Restano 39
posizioni rispetto all'hard stop sull'uso effettivo e 33 rispetto al massimo pianificato; questi
margini non sono autorizzazioni a ulteriori chiamate.

Le quote di riserva risultano consumate per `8 remediation + 7 transport = 15/15`; la singola
requalification è una quota distinta. Non vi sono righe `INTENT` o catene `retry_of` aperte.

### 2.1 Integrità e riconciliazioni

Sono stati ricalcolati dai contenuti durevoli:

- 148 hash di `raw_json` e 148 hash di `record_json`: zero mismatch;
- 148 receipt per le 148 richieste completate;
- 6 hash canonici dei binding di stage: zero mismatch;
- 7 contratti zero-token, inclusi file di evidenza/approvazione, digest incorporati, evento
  `reconciled:<request_id>` ed evento `reconciled_integrity:<request_id>`: zero mismatch;
- un `stop:tokenizer_accounting` con il corrispondente `stop_reconciled:tokenizer_accounting`;
- un `suspended:19a9b...` con il corrispondente `suspension_reconciled:19a9b...`;
- un solo `config_revision:1`, con digest
  `4b3e3ae66df67bb33d69585412dc49305592365f97dac0a674ab016606264302`.

Non resta alcun evento `stop:` o `suspended:` privo della propria riconciliazione durevole.

## 3. Identità e controlli di rendering

Tutte le 139 risposte 122B conservate nel ledger hanno esattamente:

- `returned_model = qwen3.5-122b`;
- `system_fingerprint = vllm-0.27.1-934a3247`.

Tutte le 9 risposte 27B conservate hanno esattamente:

- `returned_model = fot-exp2-consumer`;
- `system_fingerprint = vllm-0.28.0-5fc21ed4`.

I binding producer di `producer_conformity`, `producer_remediation` e
`alternate_conformity` fissano `max_tokens=2560` ed `enable_thinking=false`. Nelle 16 risposte
producer 122B finali `reasoning_tokens` è assente; nelle otto risposte 27B della libreria finale è
zero.

Va mantenuta una distinzione forense: l'antecedente 27B `19a9b372...`, eseguito prima della
requalification e poi sospeso/riconciliato, espone `reasoning_tokens=2047`, termina a lunghezza ed
è strutturalmente non valido. Non fa parte degli otto output finali né della libreria validata. La
presenza di questo antecedente è coerente con la storia durevole; non deve essere presentata come
proprietà degli output 27B riqualificati.

## 4. Producer alternativo 27B e librerie

### 4.1 Esito per caso finale

| Agente | Quota | Latenza s | Prompt / completion / totale | `schema_valid_first_attempt` | Classe errore | Finish |
| --- | --- | ---: | ---: | --- | --- | --- |
| `agent_1` | requalification | 31,897 | 1.397 / 451 / 1.848 | true | — | stop |
| `agent_2` | base | 28,611 | 1.018 / 426 / 1.444 | true | — | stop |
| `agent_3` | base | 37,245 | 1.387 / 569 / 1.956 | true | — | stop |
| `agent_4` | base | 36,485 | 1.331 / 536 / 1.867 | true | — | stop |
| `agent_5` | base | 34,596 | 1.396 / 499 / 1.895 | true | — | stop |
| `agent_6` | base | 30,469 | 1.068 / 455 / 1.523 | true | — | stop |
| `agent_7` | base | 36,015 | 1.201 / 548 / 1.749 | true | — | stop |
| `agent_8` | base | 37,022 | 1.387 / 551 / 1.938 | true | — | stop |

L'antecedente escluso `19a9b372...` ha latenza 171,664 s, `finish_reason=length`, classe
`structure` ed errore `invalid JSON: Unterminated string starting at`. La requalification
`26919ef2...` è il leaf valido della stessa catena.

Il summary alternativo dichiara `PASS`, 8 chiamate valutabili e 8 valide al primo tentativo; il suo
digest record è `baddd67043da38f1a3a176ea52f669564371c2e4618fe4bf3630e8a2695cc759`.

### 4.2 Validazione indipendente e confronto descrittivo

Le due librerie sono state rivalidate con il validatore R4 hash-pinned della worktree di riferimento,
lo schema congelato e il tokenizer locale Qwen3.8-27B-FP8 revisione
`017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`. Entrambe passano cardinalità, campi fissi,
ownership, leakage, riferimenti di variabile e cap token/caratteri.

| Misura descrittiva | 122B remediation | 27B alternate |
| --- | ---: | ---: |
| Insight validi | 16 | 16 |
| SHA canonico libreria | `c2469737bcaab0df8d07a1c2493d2f95784aae07a55998aecf49cc53fa5d1a30` | `f860063befb6a409f4ecf824e4dd7b57002cc8e67809184dadd03d0b934a05f3` |
| Voci `variable_ids` dichiarate | 128 | 128 |
| Variabili dichiarate distinte | 33 | 33 |
| Riferimenti letterali a variabili nel testo | 78 | 42 |
| Caratteri `observed_pattern`, totale / media / mediana | 6.817 / 426,06 / 423,5 | 6.471 / 404,44 / 424,0 |
| Token `observed_pattern`, totale / media / mediana | 1.602 / 100,13 / 93,5 | 1.627 / 101,69 / 110,5 |
| Massimo token/caratteri per record | 239 / 785 | 242 / 836 |

Questi numeri descrivono struttura e lunghezza; non costituiscono un claim di qualità scientifica
comparativa.

## 5. Sonda budget e freeze

La sonda contiene tre record, uno per condizione:

| Prompt | Condizione | Generazione | Parsing al primo tentativo | Finish |
| --- | --- | --- | --- | --- |
| `S2-P03-036` | A | seed 20260829; thinking 2048; max 2560 | valido | stop |
| `S2-P03-024` | B-LF | seed 20260829; thinking 2048; max 2560 | valido | stop |
| `S2-P03-025` | E-LF | seed 20260829; thinking 2048; max 2560 | valido | stop |

Il primo candidato è quindi quello selezionato. La lista ricostruita dai tre `record_json` coincide
byte-per-valore con `results/budget_probe_records.jsonl`; digest canonico:
`0d94d1987c5a3a797ec8ed7b5ffd538b7a0e6b1beed8290cc1859a93cb389950`.

Il digest canonico del contenuto congelato è
`de1f59ceb28e50cd8b9027874f5d2d22cb1337ceab2e4dda8c2adda4b2dda6f2`, uguale sia
all'`artifact_sha256` dell'evento `frozen_gate` sia al contenuto `frozen` autenticato dall'evento.
Il file pretty-printed ha invece SHA fisico
`709ae3400238b3ecdf50ef5b7d377b0bea4fdf87fcec569994d24cace39fa8ac`: i due digest hanno
semantiche diverse e non sono in conflitto.

`prepared/pilot_prompts.jsonl` contiene 40 prompt, distribuiti A/B-LF/E-LF = 8/16/16, con SHA
fisico `efd43620603b9c26dbbcc986ec80b663937fd48c05b82f2cb7406dadb61cf298`. Dopo
l'arricchimento deterministico `label_space` effettuato da `load_prepared`, i 40 oggetti coincidono
esattamente con `frozen_gate_config.prompt_sample`.

## 6. Ricalcolo indipendente del gate

Sono stati ricostruiti 120 record dal ledger: 119 `responses.record_json` e il record
`transport_invalidity` autenticato dall'evento associato alla richiesta fallita. L'esecuzione della
funzione di riferimento `evaluate_stability_gate` sulla lista così ottenuta e sul campione congelato
restituisce campo per campo:

| Campo | Valore ricalcolato |
| --- | --- |
| richieste / prompt / ripetizioni | 120 / 40 / 3 |
| validi / non validi al primo tentativo | 119 / 1 |
| T3 | PASS; copertura astensione true in A, B-LF ed E-LF |
| troncamenti / T4 | 0 / PASS |
| prompt tutti non validi / T6 valutabile | 0 / true |
| prompt divergenti | 1: `S2-P03-002` |
| stato | `R3_REQUIRED_PENDING_FEASIBILITY` |
| `go_final` | false |

Il risultato coincide integralmente con `results/stability_summary.json`. La lista ricostruita
coincide inoltre con i 120 record di `results/stability_records.jsonl` e produce il digest canonico
`bd9713eca7c3241c002d24a2ebf480f0255e5da82534289eb6cfb658d0e2f9a2` riportato nel
summary. Lo SHA fisico del JSONL è
`dde3f7de3c88bdee4844d14d3dd82daedd5e8fe7df70c465f1d3708c6f440ea6`.

### 6.1 Firme di `S2-P03-002`

| Ripetizione | Validità | Astensione | Pseudolabel | Firma semantica |
| ---: | --- | --- | --- | --- |
| 1 | valida | false | `Normal` | `(True, False, "Normal")` |
| 2 | non valida | n/a | n/a | `(False, "INVALID")` |
| 3 | valida | false | `Normal` | `(True, False, "Normal")` |

La seconda ripetizione è una invalidità di trasporto senza risposta: prompt `S2-P03-002`, classe
operativa `transport_invalidity`, errore `APIConnectionError: Connection error.`. Le due risposte
ricevute concordano su astensione e pseudolabel. La divergenza è dunque esclusivamente nella
validità, una delle due componenti espressamente previste dalla regola.

## 7. T5: latenze e proiezioni

Le statistiche usano `requests.latency_ms`. Il p95 principale è il percentile lineare; per
trasparenza, il nearest-rank del gate è 36,659 s e non cambia alcuna conclusione.

| Campione | n | Media s | Mediana s | p95 s | Totale osservato s |
| --- | ---: | ---: | ---: | ---: | ---: |
| gate 122B | 120 | 26,209 | 24,912 | 36,661 | 3.145,034 |
| alternate 27B finale valido | 8 | 34,043 | 35,305 | 37,167 | 272,341 |

Proiezione sequenziale del solo nucleo, usando la media osservata:

| Modello/campione | R=1, 1.728 richieste | R=1 +20% | R=3, 5.184 richieste | R=3 +20% |
| --- | ---: | ---: | ---: | ---: |
| 122B gate | 12,580 h | 15,096 h | 37,740 h | 45,288 h |
| 27B alternate finale | 16,340 h | 19,609 h | 49,021 h | 58,826 h |

Per controllo forense, includendo anche l'antecedente 27B troncato la media sulle nove risposte
salirebbe a 49,334 s; non è stata usata come stima della configurazione finale riqualificata.

Queste proiezioni non attestano T5 perché 1.728/5.184 sono il solo nucleo. Il piano impone
`T = Σ N_(blocco,modello) × latenza_media_(blocco,modello)` sul conteggio completo e poi
`1,20 × T ≤ W`. Restano da fissare i parametri del totale completo e la finestra effettiva `W`.
Pertanto `T5 = NOT ESTABLISHED`; non è corretto classificarlo PASS o FAIL dai soli dati presenti.

## 8. Decisione 11 e conseguenza R

Il testo esatto della regola in `PIANO_STATISTICO.md` §10.3 è:

> Due ripetizioni dello stesso prompt divergono se differiscono nella coppia
> (`abstain`, `predicted_label`) dopo il parsing, oppure se differiscono nella **validità**. Differenze
> nel solo JSON parsato, finish reason, testo libero o byte grezzi che non cambiano coppia o validità
> **non** sono divergenze ai fini del gate, ma vengono conservate e riportate. Un prompt è divergente
> se almeno una delle sue ripetizioni diverge dalle altre. Gate: **0 prompt divergenti valutabili su
> 40 → R=1**; **≥ 1 → R=3**.

`PREFLIGHT_03_0.md` precisa inoltre: «l'assenza dei due controlli viene registrata ma non attiva
R=3 da sola; una divergenza osservata fra ripetizioni sì.» Poiché `S2-P03-002` differisce nella
validità, la conseguenza prescritta è `R=3` sull'intero studio. Non è una scelta discrezionale della
review.

## 9. Invarianti finali

- `pilot-001/ledger.sqlite3` ha SHA-256
  `4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`, uguale al
  predecessore congelato.
- `pilot-002/ledger.sqlite3` ha SHA-256
  `9c9101826d2cb39498c1e8d0b167921680c38f045aa156220a3a4ba077ed304b` e la sua config
  ha SHA-256 `f21b33a5e9a625ca8fa9f08711a09d456ee613b23b1f7f447faf6b26bd114067`: entrambi
  coincidono con il manifest storico di materializzazione. `pilot-002` è quindi intoccato rispetto
  a quei riferimenti.
- Il target `pilot-03` non presenta `ledger.sqlite3-wal` né `ledger.sqlite3-shm`.
- `lsof /Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03/ledger.sqlite3` è vuoto al termine.
- Il ledger `pilot-03` ha conservato per tutta la review SHA-256
  `93ff83a5a4132800c2973fe6687c8e0ffcdb07d33f293a8517ca715ff8dc4089`.

La frase «nessun sidecar» è qui riferita al target `pilot-03`: il predecessore storico `pilot-001`
conserva i propri sidecar preesistenti e non è stato modificato.

## 10. Numeri destinabili a §4.13 e al paper

| Numero/asserzione | Valore verificato | Fonte o query riproducibile |
| --- | --- | --- |
| Intent nativi / cumulativi | 156 / 161 | `SELECT stage,status,quota_kind,count(*) FROM requests GROUP BY ...`; `SELECT disposition,count(*) FROM predecessor_lineage GROUP BY disposition` |
| Massimo pianificato / hard stop | 167 / 200 | formula di `ledger.py`: `160 + successor + predecessors + requalification`; conteggi durevoli 1+5+1 |
| Reserve remediation+transport | 15/15 | `SELECT quota_kind,count(*) FROM requests WHERE quota_kind IN ('remediation','transport') GROUP BY quota_kind` |
| Identità 122B | 139/139 `qwen3.5-122b`, fingerprint `vllm-0.27.1-934a3247` | join `requests`/`responses`, parsing di `raw_json` |
| Identità 27B | 9/9 `fot-exp2-consumer`, fingerprint `vllm-0.28.0-5fc21ed4` | join `requests`/`responses`, parsing di `raw_json` |
| T9 remediation 122B | 16 insight, 8/8 output finali validi | `outcome:producer_remediation`; libreria validata `validated_insight_library_qwen_122b_primary_producer_remediation.json` |
| T9 alternate 27B | 16 insight, 8/8 output finali validi | `outcome:alternate_conformity`; libreria validata `validated_insight_library_qwen_27b_alternate_alternate_conformity.json` |
| Sonda budget | 3/3 valide; generazione 2048/2560 | `responses.record_json` dello stage `budget_probe`; `budget_probe_records.jsonl` |
| Gate | 120 richieste; 119 valide; 1 invalidità trasporto; 0 truncation | ricalcolo `evaluate_stability_gate` sui record ledger e campione congelato |
| T3 / T4 / T6 | PASS / PASS / valutabile | stesso ricalcolo; confronto integrale con `stability_summary.json` |
| Divergenza | 1/40, `S2-P03-002`, differenza di validità | firme semantiche dei tre record ledger |
| R | R=3 obbligatorio | `PIANO_STATISTICO.md` §§10.1–10.3 e `PREFLIGHT_03_0.md` |
| Latenza 122B | media 26,209 s; mediana 24,912 s; p95 36,661 s | `SELECT latency_ms FROM requests WHERE stage='stability_gate'` |
| Latenza 27B finale | media 34,043 s; mediana 35,305 s; p95 37,167 s | otto leaf finali validi di `alternate_conformity` |
| Proiezione nucleo R=3 +20% | 45,288 h (122B); 58,826 h (27B) | media osservata × 5.184 × 1,20, esecuzione sequenziale |
| T5 | `NOT ESTABLISHED` | formula e prerequisiti di `BUDGET_RISORSE_REV10.md`; `W` e totale completo non fissati |

## 11. Conclusione

Il contenuto durevole conferma il PASS tecnico del pilot nei limiti dichiarati: producer finali
validi, sonda budget valida, T3 e T4 superati, T6 valutabile e integrità contabile riconciliata. La
singola divergenza di validità su `S2-P03-002` attiva obbligatoriamente R=3. La fattibilità T5 non è
ancora stabilita e il ledger conserva correttamente `go_final=false`; il prossimo atto è pertanto
una decisione GO/NO-GO dell'autore sulla fattibilità organizzativa completa, non un'autorizzazione
implicita della presente review.
