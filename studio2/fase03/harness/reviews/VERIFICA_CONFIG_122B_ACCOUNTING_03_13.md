# Verifica indipendente minima — configurazione 122B senza `/tokenize` (03.13)

## Esito

**NON OK** per l'esatto commit `6431612c632b4c46f87f3edec9d662c572a4996a`,
tree `dfa85151b291b69f800ab90c9c81902460463385`, parent
`15e56a89b0f377e6d90eef28ed941d4d54b5b00c`, branch sorgente
`codex/studio2-config-122b-accounting`.

Il delta introduce un controllo corretto nel percorso producer ordinario e i tre test forniti
passano, ma la contabilità non è obbligatoria su tutti i percorsi 122B, il riuso non la
riconferma sempre e alcune manomissioni coerenti restano accettate. Il candidato non autorizza
pilot, gate o batch.

## Rilievi bloccanti

1. **Il consumer 122B e l'API diretta possono eseguire senza guard.**
   `studio2/fase03/harness/d9.py:13-14` assegna il 122B anche a `budget_probe` e
   `stability_gate`, ma `studio2/fase03/run_pilot.py:330-334` chiama `execute_request` senza
   `messages` e senza `accounting_guard`. Inoltre `studio2/fase03/harness/runtime.py:41-42`
   rende entrambi opzionali e `runtime.py:96-99` contabilizza solo se il guard è già presente.
   Un probe esterno ha eseguito direttamente una richiesta con modello `qwen3.5-122b`, guard
   assente e risposta priva di contabilità protetta: un transport osservato, nessun rifiuto.

2. **Un record completato viene restituito prima della riconvalida contabile.**
   `studio2/fase03/harness/runtime.py:71-76` ritorna il record persistito prima del blocco
   contabile a `runtime.py:96-99`. Dopo una modifica coerente dei `messages` nell'evento
   contabile, una chiamata diretta `execute_request(..., resume=True, accounting_guard=...)`
   ha riusato il record senza errore e senza transport. Il controllo preventivo del solo runner
   producer (`studio2/fase03/producer_probe.py:149-152`) non chiude il percorso diretto né il
   runner consumer.

3. **La manomissione coerente di raw e hash non è rilevata.**
   `studio2/fase03/harness/ledger.py:285-310` verifica hash e riferimenti che risiedono nello
   stesso ledger, ma non conserva un legame indipendente e ricalcolabile tra l'intero raw e il
   record valutato. Il probe ha cambiato `raw.id`, ricalcolato `responses.raw_sha256`,
   `events.artifact_sha256` e `detail.raw_response_sha256`; anche con gli esatti messaggi attesi,
   `validate_tokenizer_accounting_evidence` ha accettato l'evidenza alterata.

4. **STOP ed evidenza create-once non coprono due percorsi di errore/resume.**
   `studio2/fase03/harness/ledger.py:258-263` trasforma in STOP soltanto `HarnessError`: una
   `ValueError` sintetica da `apply_chat_template` è uscita senza `stop:tokenizer_accounting`.
   Inoltre, dopo raw ed evento PASS già durevoli ma prima del record, il resume richiama
   `account_producer_response`; l'inserimento a `ledger.py:275` collide con il vincolo
   create-once di `ledger.py:317-322`. Il restart ha quindi fallito su evento duplicato invece
   di riconvalidare idempotentemente il PASS e completare senza un nuovo transport.

## Test realmente eseguiti

- Test candidato fornito:
  `python3 -m unittest studio2.fase03.harness.test_tokenizer_accounting -v` — **3/3 PASS**
  in 0,252 s.
- Gli stessi byte finali del test sul parent — **rosso discriminante**, exit 1:
  `ImportError` per assenza di `TokenizerAccountingGuard` nel parent.
- Sei probe temporanei esterni al candidato, solo con tokenizer/transport sintetici e ledger
  temporanei — **0/6 conformi**: 4 failure e 2 error. Hanno riprodotto i quattro rilievi sopra;
  nessun client provider o endpoint è stato costruito o chiamato.
- Regressioni pertinenti D01-D04, D9, D9-corrections, harness offline, riconciliazione storico e
  revisions, eseguite con l'interprete arm64 compatibile già presente — **127/127 PASS** in
  241,548 s.
- Regressioni C01-C03 — **14/14 PASS** in 276,607 s.

Il primo tentativo delle 127 regressioni con Python x86_64 non è conteggiato: `jsonschema`
falliva importando `rpds.cpython-311-darwin.so` arm64 (`have arm64, need x86_64`). La stessa
selezione è stata poi rieseguita integralmente con
`arch -arm64 /usr/local/bin/python3` ed è passata 127/127.

## Limiti e non eseguiti

Non sono stati eseguiti provider, endpoint, chat completion, `/models`, `/version`, `/tokenize`,
sonda reale, gate reale, pilot o batch. Non sono state stabilite qualificazione del servizio,
identità del tokenizer server, equivalenza byte-identica server/client, capacità o autorizzazione
delle chiamate. Non è stata eseguita la discovery completa non pertinente oltre alle suite
elencate. Il candidato, i ledger reali e gli artefatti di output reali non sono stati modificati;
non sono stati effettuati commit, merge, push o tag.

L'impronta SHA-256 dei byte di questo verbale è comunicata separatamente, senza autoreferenza.
