# Report 7.4-FIX-RUNNER — tre difetti trovati dalla prima giornata canary reale

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

## Ripresa della campagna

1. Suite sul Mac nell'ambiente `fottep002`; merge in `main`; tag `studio2-fase03-runner-7-4-fix-001`.
2. Rieseguire il canary del giorno: `run_final_canary.py --target "$TARGET" --execute
   --acknowledge EXECUTE_PHASE03_FINAL_CANARY`. Lo slot `canary:day1:S2-P03-003` si chiude dai
   byte salvati, senza chiamata; le altre nove partono. Atteso `verdict PASS` e dieci identità
   `qwen3.5-122b` / `vllm-0.27.1-934a3247`.
3. Poi il primo tratto: `run_final_batch.py --target "$TARGET" --pass-index 1 --max-requests 250
   --execute --acknowledge EXECUTE_PHASE03_FINAL_BATCH`.
