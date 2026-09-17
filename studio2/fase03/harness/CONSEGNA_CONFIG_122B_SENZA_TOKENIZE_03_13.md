# Consegna corretta — configurazione D9 122B senza `/tokenize`

Stato: **CANDIDATO SUCCESSORE LOCALE, NON QUALIFICATO E NON AUTORIZZATO
ALL'ESECUZIONE**.

Il candidato respinto di base è il commit
`6431612c632b4c46f87f3edec9d662c572a4996a`. La verifica indipendente ricevuta è
`studio2/fase03/VERIFICA_CONFIG_122B_ACCOUNTING_03_13.md`, SHA-256
`c7209a3f8c93380422841c648741795a9e03d6851e4e2d9a3597e794bce17052`.
Questo delta corregge esclusivamente i quattro blocker della verifica; non modifica
la configurazione provider già acquisita, non effettua chiamate esterne e non
autorizza sonda, gate o pilot.

## Correzioni applicate

Per ogni richiesta il cui modello effettivo è esattamente `qwen3.5-122b`, il punto
comune `execute_request` richiede, prima di intent, riserva o trasporto, un
`TokenizerAccountingGuard` e un solo messaggio user il cui contenuto corrisponde
all'hash del prompt congelato. La stessa lista `messages` viene consegnata al
trasporto. Il vincolo copre producer, budget probe, stability gate, CLI e invocazioni
dirette del runtime; gli altri modelli mantengono il percorso precedente.

La risposta raw viene contabilizzata o rivalidata prima di parsing e prima di
riusare un record già completato. Il commitment durevole e ricalcolabile lega:
identità della richiesta, messaggi esatti e relativo hash, revisione dello snapshot,
hash dei byte raw, conteggio locale, conteggio server ed esito PASS. Lo stesso
commitment è registrato sia nell'evento create-once sia nel campo proof della
richiesta. Un secondo legame semantico raw-to-record copre i campi consumati
(`response_id`, modello restituito, fingerprint, token, finish reason e contenuto),
così un'alterazione coerente dei soli hash interni non è accettata.

Resume, retry e restart ripetono il conteggio locale e verificano entrambi i legami
prima di restituire evidenza preesistente. Un evento PASS senza il record finale può
quindi riprendere idempotentemente senza nuovo trasporto. Qualunque eccezione del
tokenizer/template, comprese eccezioni ordinarie come `ValueError`, persiste invece
`stop:tokenizer_accounting` nella stessa transazione e blocca durevolmente ogni uso
successivo.

## Prova discriminante sul candidato respinto

Gli stessi byte finali di
`studio2/fase03/harness/test_tokenizer_accounting.py` sono stati eseguiti contro il
runtime esatto del commit respinto, prima delle modifiche al runtime. Il loro SHA-256
è `b212c73ca0946dd10295bc482bb071d8b241db952d190a08ef94b8eb92bf1e50`:

```text
arch -arm64 /usr/local/bin/python3 -m unittest studio2.fase03.harness.test_tokenizer_accounting -v
Ran 9 tests in 0.267s
FAILED (failures=4, errors=3)
```

Sette prove su nove erano discriminanti. I sei probe avversariali permanenti coprono:
guard mancante sul producer e sul consumer prima di intent/trasporto; record completato
con messaggi mutati; modifica coerente di raw e hash evento; eccezione ordinaria del
tokenizer con STOP durevole; PASS presente ma record assente con ripresa idempotente.
Le prove positive coprono producer e consumer 122B su prima esecuzione,
resume/restart senza nuovo trasporto, varianti `usage` non valide e compatibilità
non-122B.

## Verifiche sul candidato corretto

Tutte le verifiche seguenti sono state eseguite in locale con interprete arm64 e
senza accesso al provider:

```text
arch -arm64 /usr/local/bin/python3 -m unittest studio2.fase03.harness.test_tokenizer_accounting -v
Ran 9 tests in 0.269s
OK

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
Ran 127 tests in 249.685s
OK

arch -arm64 /usr/local/bin/python3 -m unittest studio2.fase03.harness.test_c01_c03 -v
Ran 14 tests in 268.614s
OK
```

Il guardian documentale è stato eseguito separatamente e **non è conteggiato come
PASS**:

```text
arch -arm64 /usr/local/bin/python3 docs/test_explanation.py
Ran 35 tests in 0.093s
FAILED (failures=14, skipped=1)
```

Sono le 14 divergenze documentali storiche già presenti fuori dal perimetro del
delta. Nessuna è stata nascosta, riclassificata o sommata alle suite verdi.

## Limiti invariati

Non sono stati eseguiti chat completion, `/models`, `/version`, `/tokenize`, sonda,
gate, pilot, qualificazione del servizio, verifica dell'identità byte-identica del
tokenizer server, riconciliazione/applicazione dello storico S, merge, push o tag.
L'uguaglianza locale/server qualifica esclusivamente la singola risposta contabilizzata;
non prova il tokenizer server e non concede execution authorization.
