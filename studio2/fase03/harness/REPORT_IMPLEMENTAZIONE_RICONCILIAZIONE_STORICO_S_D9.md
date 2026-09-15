# Report — implementazione minima della riconciliazione dello storico S

**Esito:** candidato tecnico offline preparato; nessuna applicazione a ledger
reale e nessuna autorizzazione esecutiva.

## Delta

- `d9.py` valida il pacchetto revisionato, l'approvazione distinta, le tre fonti
  S byte-pinnate e i quattro binding ordinati. S1 resta esito storico incerto,
  senza prova D03 e senza retry.
- `ledger.py` aggiunge l'importazione transazionale esplicita v2→v3 e mantiene
  gli addebiti esterni separati dalle richieste native. S=4 entra una volta nel
  cumulativo e non altera le quote remediation/transport.
- `test_history_reconciliation.py` copre positivo, fonti reali su ledger
  fixture, mapping incompleto/duplicato/scambiato, tipi, approvazioni, fonte
  alterata con riferimento riallineato, rollback, idempotenza, riapertura,
  chiamata diretta senza rebind, cache stantia e due contese multiprocesso.

## Prove

Gli stessi byte finali del test, SHA-256
`ebbe59d6d230f5052d4d8cd4beb5492e23452824aca0fb01111648565409e88c`,
producono rosso sul parent `8fbbfa0` e verde sul candidato:

| Runtime | Esito |
| --- | --- |
| parent `8fbbfa0` estratto con `git archive` | 10 eseguiti; 1 failure, 15 errori; exit 1 |
| candidato corrente | 10/10 OK; exit 0 |

I log integrali e le impronte sono in `history_reconciliation_evidence/`.
Regressioni direttamente dipendenti, eseguite separatamente: D9 17/17,
correzioni D9 11/11, D04 quota aperta 8/8, lifecycle ledger 37/37.
Le suite non vengono sommate al test nuovo.

Il guardiano documentale resta correttamente **NON PASS**: 35 test,
14 fallimenti storici, 1 skip, 0 errori. Il delta non modifica i walkthrough.

## Limiti e passaggio successivo

Non esistono ancora package reale, quattro identità assegnate, ledger/pilot_id
autorizzati, review del mapping o approvazione `IMPORT_AUTHORIZED`. Il test sulle
fonti repository usa un ledger temporaneo dichiaratamente fixture e non muta i
dati sorgente. L'applicazione reale resta vietata dal mandato.

Il candidato richiede review indipendente sui byte committati. Un eventuale OK
tecnico non qualifica servizi, non approva capienza/T5 e non concede pilot, GO,
freeze o chiamate.
