# Prompt di riverifica indipendente — accounting Qwen 122B 03.13

Esegui una verifica indipendente, read-only, del commit `HEAD` che contiene questo
file. Il suo genitore atteso è il candidato respinto
`6431612c632b4c46f87f3edec9d662c572a4996a`; segnala immediatamente se la genealogia
non coincide o se il delta comprende modifiche estranee.

La verifica precedente è
`studio2/fase03/VERIFICA_CONFIG_122B_ACCOUNTING_03_13.md`, il cui SHA-256 atteso è
`c7209a3f8c93380422841c648741795a9e03d6851e4e2d9a3597e794bce17052`.
Ricalcola l'hash prima di usarla. Leggi inoltre `docs/MAINTENANCE.md` e applica le
regole di revisione dell'harness. Non modificare file, ledger o artefatti; non
effettuare chiamate provider, merge, push, tag, sonda, gate o pilot.

## Domande bloccanti

Accetta il successore soltanto se dimostri tutte le proprietà seguenti:

1. Ogni chiamata con modello effettivo esattamente `qwen3.5-122b`, su producer,
   consumer budget/gate, CLI e uso diretto di `execute_request`, richiede guard e
   messaggi prima di intent, riserva e trasporto. I messaggi contabilizzati devono
   essere esattamente quelli trasmessi. Gli altri modelli devono restare compatibili.
2. Prima di riusare qualunque raw o record 122B, inclusi completed record, resume,
   retry e restart, il conteggio locale deve essere ricalcolato e confrontato con
   `usage.prompt_tokens` senza eseguire un nuovo trasporto.
3. L'evidenza durevole deve legare in modo semantico e indipendentemente
   ricalcolabile identità della richiesta, messaggi, snapshot, raw e campi consumati
   dal record. Prova alterazioni coerenti di raw e hash/eventi: non devono essere
   accettate soltanto perché gli hash interni concordano tra loro.
4. Ogni eccezione del tokenizer/template, non solo `HarnessError`, deve creare uno
   STOP durevole. Un PASS valido già persistito ma privo del record finale deve
   invece completare su resume in modo idempotente e senza collisione evento o nuovo
   trasporto.

Controlla anche che la validazione avvenga prima di parsing, decisioni, output e gate,
che i dati token siano interi non booleani e non negativi, e che un errore successivo
al trasporto non possa essere presentato come prevenzione della chiamata.

## Test richiesti

Verifica che i byte finali di
`studio2/fase03/harness/test_tokenizer_accounting.py` siano quelli documentati nella
consegna e che, applicati al runtime del commit base respinto, producano la prova
rossa dichiarata. Sul successore esegui almeno, con interprete arm64:

```text
arch -arm64 /usr/local/bin/python3 -m unittest studio2.fase03.harness.test_tokenizer_accounting -v
arch -arm64 /usr/local/bin/python3 -m unittest \
  studio2.fase03.harness.test_d01_replay \
  studio2.fase03.harness.test_d02_predecessors \
  studio2.fase03.harness.test_d03_contract \
  studio2.fase03.harness.test_d04_open_quota \
  studio2.fase03.harness.test_d9 \
  studio2.fase03.harness.test_d9_corrections \
  studio2.fase03.harness.test_harness_offline \
  studio2.fase03.harness.test_history_reconciliation \
  studio2.fase03.harness.test_revisions
arch -arm64 /usr/local/bin/python3 -m unittest studio2.fase03.harness.test_c01_c03 -v
arch -arm64 /usr/local/bin/python3 docs/test_explanation.py
```

Riporta separatamente ogni suite. Il guardian documentale non può essere dichiarato
PASS se conserva failure note. Includi commit e tree verificati, elenco completo dei
file del delta, eventuali limiti ambientali e un verdetto esplicito `ACCEPT` oppure
`REJECT`, con ogni blocker associato a file e riga.
