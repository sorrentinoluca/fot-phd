# Report 7.4-FIX-RUNNER — quattro difetti trovati dalla prima giornata reale

Worktree `7-4-fix-runner`, branch `codex/studio2-7-4-fix-runner` dal tag
`studio2-fase03-protocollo-finale-frozen-002` (`93c43a0`). Nessuna chiamata a modelli in
questa finestra. Protocollo, schedule, prompt, quote e pin **non sono toccati**: qui si
corregge solo il codice dei runner, quindi il tag 002 resta e la costante `PROTOCOL_TAG`
registrata nel target non si muove.

## Che cosa è successo il 2026-09-18

Il canary del giorno 1 è morto alla prima chiamata con
`KeyError: 'label_space'` dentro `run_pilot.consumer_record`, **dopo** che la risposta era
arrivata. Una chiamata consumata (`canary:day1:S2-P03-003`, 19,6 s di latenza).

## D1 — `label_space` non arriva mai ai runner finali

`consumer_record` valida la risposta contro lo spazio di label chiuso. Nel pilot quel campo
non sta nel file dei prompt: lo inietta `run_pilot` al caricamento, dal manifest congelato
(`prompt['label_space'] = manifest['label_space']`). Il canary legge le righe del file del
pilot e non lo inietta; `run_final_batch.load_prompts` legge `final_prompts.jsonl`, che
porta `available_insight_ids` ma **non** `label_space`, e non lo inietta. Il primo lotto
scientifico sarebbe morto identico, bruciando un'altra chiamata.

Correzione: `harness/final_prompts.frozen_label_space(path)` legge lo spazio di label dal
manifest congelato del pilot e lo **autentica per SHA-256** (`84176888…`, ora definito una
volta sola e importato da `build_final_prompts`). I due runner lo legano ai prompt al
caricamento. Il percorso predefinito è accanto allo snapshot del tokenizer che il target già
indica; `--pilot-manifest` lo sovrascrive. I file renderizzati — pinnati e già copiati nel
target — non si toccano: lo spazio di label non è byte di prompt, è l'insieme chiuso contro
cui si valida la risposta.

Il canary lega lo spazio di label **prima** del ritorno del piano: così
`run_final_canary.py --target …` senza `--execute` è un preflight vero, e un manifest assente
o alterato ferma il giorno a zero chiamate.

## D2 — `ledger_cli` non apre un ledger `final_batch`

Il CLI costruiva `PilotLedger` col profilo `pilot` cablato: su un ledger che dichiara
`final_batch` falliva con «ledger profile differs from the declared quota envelope». È lo
strumento che il runbook indica per lo `status` e per `reconcile-zero-token`, cioè per tutto
il percorso D3. Ora legge dal ledger il profilo dichiarato (`--profile` per forzarlo).

## D3 — `INTENT` con raw salvato non è consumo incerto

`execute_request` salva il raw **prima** di interpretarlo. Uno slot `INTENT` con raw salvato
descrive quindi una chiamata avvenuta, con byte e ricevuta durevoli: manca solo la
valutazione, che è fallita fuori dal ledger. La guardia D3 li trattava come incertezza e
fermava la ripresa, costringendo a buttare uno slot già pagato.

Correzione approvata dall'autore il 2026-09-18: `stored_without_record` distingue i due
casi. Con raw salvato lo slot si chiude rivalutando i byte, **senza trasporto**, e registra
l'evento non normativo `note:stored_response_evaluated:<request_id>`; il lotto lo conta in
`recovered_from_stored_response` e non in `sent_this_run`. Senza raw salvato, D3 riga 2 resta
esattamente com'era: nessun reinvio automatico, decisione dell'autore.

## La lezione, che è la terza volta

Tutti e tre i difetti erano invisibili ai test perché le fixture costruivano a mano oggetti
che il percorso reale non produce: `fixture_prompt` aggiungeva `label_space`, come i binding
di `test_final_batch` sostituivano `execution_config` nascondendo la guardia D9. Le fixture
ora rispettano il contratto vero: `fixture_prompt` non ha `label_space`, e la base dei test
costruisce i prompt passando da `load_prompts`, cioè dal codice che gira davvero.

## Verifiche

- `harness/test_runner_stored_response.py`, 10 test: la riga renderizzata non porta lo
  spazio di label e il loader lo lega; manifest non autentico, manifest assente e percorso
  predefinito; una giornata canary che parte da prompt senza `label_space`; il piano che si
  ferma a zero chiamate senza manifest; recupero da raw salvato per canary e per lotto, con
  un provider che **fallisce il test se viene chiamato**; slot irrisolto senza raw che
  continua a fermarsi.
- Suite completa nella VM: 324 test, stessi non-pass ambientali del ramo di partenza
  (3 failures, 49 errors, 22 skipped su `d04f423` come su questo commit) — nessuna
  regressione. **Fa fede il Mac**, sotto Python 3.10 / NumPy 2.2.6.

## D4 — il contratto del record di chiamata era chiuso a metà (7.4-FIX-CONTRATTO-RECORD)

Dopo D1 il canary del 2026-09-18 è passato con dieci chiamate reali, e il primo tratto
scientifico è morto alla **prima** risposta, pagata: `KeyError: 'sample_role'` in
`consumer_record`. Stessa forma di D1: il campo mancava nella riga renderizzata e la fixture
lo aggiungeva a mano. La correzione di D1 aveva tolto `label_space` da `fixture_prompt` e
lasciato `sample_role`. Lo slot è `INTENT` con raw salvato e si chiude da D3 senza chiamata.

### Elenco dei campi, ricavato dal codice che li consuma

| Consumatore | Campi letti dal prompt | Origine nel percorso reale |
| --- | --- | --- |
| `run_pilot.consumer_record`, copiati nel record durevole (`CONSUMER_RECORD_PROMPT_FIELDS`) | `prompt_id, agent_id, case_id, condition, prompt_sha256` | riga di `render_all` |
| | `sample_role` | **nessuna**: legato al caricamento, vedi sotto |
| `consumer_record`, validazione della risposta (`CONSUMER_RECORD_VALIDATION_FIELDS`) | `label_space` | manifest congelato `84176888…`, legato al caricamento (D1) |
| | `available_insight_ids` | riga di `render_all` |
| trasporto (`Provider.call`), `_call_record` (log T7 §8.7), `batch_spec` (`RUNNER_PROMPT_FIELDS`) | `text, prompt_sha256` | riga di `render_all` |
| `evaluate` del lotto (`repetition, stable_id, block, library_role`, giorni civili) | — | dallo **schedule**, non dal prompt |
| log T7 §8.7 (`CallRecord`) | nessun `sample_role` | — |

Le chiavi di una riga renderizzata sono ora dichiarate in
`final_prompts.RENDERED_ROW_KEYS` e `render_all` le verifica su ogni riga; i campi che
`consumer_record` legge sono dichiarati in `run_pilot` (`CONSUMER_RECORD_REQUIRED_FIELDS`, il
codice li usa da lì) e `run_final_batch.required_prompt_fields()` è la loro unione con quelli
del runner, ricalcolata a ogni caricamento: un campo aggiunto domani a `consumer_record` è
richiesto dal caricatore nello stesso istante. Il canary non soffriva del difetto: le sue righe sono del pilot
(`protocol.RenderedPrompt`), che porta `sample_role`.

### Decisione d'autore su `sample_role` (2026-09-18)

**Nel batch finale `sample_role` non è un ruolo di campionamento ma un marcatore costante di
provenienza, `final_batch`, perché i casi non sono campionati: i 2.244 casi corrono tutti.
L'informazione discriminante sta in `block`, `condition`, `library_role`, `locality`.** Nel
pilot lo stesso campo (`matched_transfer` / `context_stress`) descrive come quel caso fu
campionato. Derivarlo da `block`/`locality` avrebbe risposto a un'altra domanda sotto la
stessa chiave, ambiguità che non si spiega nel paper; toglierlo avrebbe richiesto un wrapper
di `consumer_record` e rotto l'allineamento delle chiavi fra record del pilot e del batch. Il
valore è legato al caricamento (`load_prompts`), come `label_space`, e **non** scritto nelle
righe renderizzate, pinnate e già dentro il target.

### Controllo di completezza, fail closed prima di qualunque chiamata

`load_prompts` verifica su ogni riga le chiavi del renderer, rifiuta una riga che porti già un
campo legato al caricamento (`label_space`, `sample_role`), lega i due e poi
`require_prompt_fields` nomina ogni campo mancante. `canary_prompts` passa dalla stessa
verifica. Il piano (`--pass-index N` senza `--execute`, canary senza `--execute`) carica i
prompt prima di restituire, quindi si ferma a **zero** chiamate. Il recupero da raw salvato
non è più gettato da `--max-requests`: non consuma chiamate e non è contato in `sent`.

### Ambiente di riferimento (aggiunta d'autore)

`harness.guards.require_reference_environment` legge `schedule.numpy_version` da
`batch_finale/INVENTARIO_SCHEDULE_7_4.json` (non ricablato) e ferma il comando se
`numpy.__version__` differisce, dicendo versione osservata e attesa. È la prima riga dei
`main()` di `build_final_inventory`, `build_window_assignment`, `build_final_prompts`,
`prepare_final_target_inputs`, `materialize_final_target`, `run_final_canary`,
`run_final_batch`, prima ancora del parser degli argomenti (anche `--help` si ferma).
Bloccante: sotto NumPy 2.3.x la schedule è un altro esperimento, e fin qui l'errore arrivava
come `FAIL pin schedule`, vero ma senza il perché. Conseguenza voluta: `build_final_inventory`
legge la versione dallo stesso artefatto che riscrive, quindi la schedule non si rigenera mai
sotto un NumPy diverso; con l'artefatto assente si ripristina da git prima di rilanciare.

### Verifiche

- `harness/test_record_contract.py`, 21 test. Righe del **renderer vero** sull'inventario
  reale caricate dal caricatore reale; `fixture_prompt` ha esattamente `RENDERED_ROW_KEYS`
  (asserito) e `fixture_pilot_prompt` passa da `protocol.RenderedPrompt`; una riga senza un
  campo ferma piano e caricatore nominandolo, a zero richieste; un canary con `sample_role`
  mancante o `label_space` già scritto si ferma prima di ogni chiamata; il record di ogni
  slot porta `final_batch` e il log T7 ha esattamente i campi di `CallRecord`; la ripresa dal
  raw salvato con il contratto chiuso (`recovered_from_stored_response: 1`, `sent_this_run`
  = nuove) e con un provider che **fallisce il test se chiamato**; una guardia che traccia
  ogni chiave letta da `consumer_record` e dall'intero `run_pass` e fallisce se ne compare una
  non dichiarata, più il caso "campo aggiunto domani" fermato dal caricatore; l'ambiente:
  versione letta dall'artefatto, mismatch con messaggio osservato/atteso, artefatto assente,
  e i sette `main()` che chiamano la guardia per primi.
- Regola: **nessuna fixture aggiunge a mano un campo che il codice di produzione non produce.**
- Suite nella VM: vedi sotto; **fa fede il Mac** (Python 3.10 / NumPy 2.2.6).

## Ripresa della campagna

1. Suite sul Mac nell'ambiente `fottep002`; merge in `main`; tag `studio2-fase03-runner-7-4-fix-001`.
2. Rieseguire il canary del giorno: `run_final_canary.py --target "$TARGET" --execute
   --acknowledge EXECUTE_PHASE03_FINAL_CANARY`. Lo slot `canary:day1:S2-P03-003` si chiude dai
   byte salvati, senza chiamata; le altre nove partono. Atteso `verdict PASS` e dieci identità
   `qwen3.5-122b` / `vllm-0.27.1-934a3247`.
3. Poi il primo tratto: `run_final_batch.py --target "$TARGET" --pass-index 1 --max-requests 250
   --execute --acknowledge EXECUTE_PHASE03_FINAL_BATCH`.

Dopo D4 (tratto fermo alla prima risposta, canary del 2026-09-18 già `PASS`): suite sul Mac,
merge, tag; piano `run_final_batch.py --target "$TARGET" --pass-index 1` (deve stampare
`PLAN_ONLY` con `already_recorded: 1`); poi lo stesso comando del punto 3 con **`--resume`**.
Attesi nel riepilogo `recovered_from_stored_response: 1` e `sent_this_run` pari alle chiamate
nuove; il record recuperato porta `sample_role: final_batch`.
