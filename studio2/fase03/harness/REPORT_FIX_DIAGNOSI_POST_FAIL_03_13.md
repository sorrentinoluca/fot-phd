# Fix diagnosi post-FAIL per remediation producer — 03.13-REM-1

## Esito

**READY FOR INDEPENDENT REVIEW (author).** Il difetto che rendeva irraggiungibile la remediation
del producer dopo un FAIL reale è corretto sul candidato derivato da
`2a135c26b3733651168f0bc07789daf107f40d25`, tree
`b013f76dffbad565a096c2f06f4f1aaaddf60633`.

La correzione è esclusivamente offline. Non sono stati aperti o modificati ledger reali, non è
stata usata la rete e non sono state eseguite chiamate provider o attività scientifiche.

## Correzione

`PilotLedger.diagnose_producer_failure` registra una diagnosi approvata dopo la chiusura dello
stage `producer_conformity`, senza riscrivere l'evento outcome. L'operazione:

- accetta soltanto un outcome `FAIL` già chiuso e privo di diagnosi;
- richiede una diagnosi ammessa e presente come `validation_class` di almeno un record fallito;
- autentica i byte di un approval JSON che lega decisione, autore, diagnosi e
  `records_sha256` dell'outcome;
- rifiuta una disposizione remediation già presa e qualunque richiesta `budget_probe` o
  `stability_gate` già presente;
- persiste un solo evento `diagnosis:producer_conformity` e rende idempotente il replay degli
  stessi byte;
- non riapre lo stage, non crea request e non altera outcome, quota o contatori nativi.

`authorize_remediation` continua a preferire la diagnosi presente nell'outcome. Solo quando
quella diagnosi è assente usa l'evento post-FAIL, rivalidandone approval, hash e binding ai record.
Il resto del contratto di autorizzazione è invariato.

Non sono stati modificati `producer_probe.py`, schema SQLite, prompt scientifici, contratti
congelati, quote o ordine degli stage.

## Test RED/GREEN

I cinque test REM-1 eseguiti contro l'implementazione parent hanno prodotto il RED atteso:
5 errori su 5, tutti dovuti all'assenza di `diagnose_producer_failure`. Sugli stessi casi, il
candidato finale passa 5/5.

I casi coprono:

1. FAIL senza diagnosi: remediation respinta prima, ammessa dopo l'evento approvato;
2. diagnosi incoerente, hash approval errato e binding `records_sha256` errato: rifiutati senza
   mutazioni durevoli;
3. outcome PASS, remediation autorizzata o waived e presenza di probe: rifiutati;
4. outcome, chiusura stage, quota e `native_requests`: invariati;
5. replay degli stessi byte: un solo evento, stesso risultato.

## Verifiche

| Verifica | Risultato osservato |
|---|---|
| RED sul parent, cinque test REM-1 | 5 errori attesi in 0,295 s |
| GREEN `PostFailureDiagnosisTests` | 5/5 PASS in 0,466 s |
| Successor mirata | 37/37 PASS in 5,541 s |
| Regressione esplicita, 15 moduli | 210/210 PASS in 476,969 s |
| `py_compile` dei due moduli modificati | PASS |
| `git diff --check` | PASS |

La regressione ha emesso `ResourceWarning` SQLite storici, senza failure o errori.

Il guardian è stato eseguito e rendicontato separatamente: 35 test, 14 failure storiche, 1 skip,
0 errori in 0,078 s. Il suo NON PASS coincide con il baseline documentale noto ed è fuori dallo
scope REM-1; non viene contato come esito della suite applicativa.

## Invarianti operativi

- zero chiamate provider e zero uso della rete;
- nessun ledger runtime reale aperto, letto o modificato;
- `server_enea.json` non letto;
- nessuna remediation reale, retry, resume, T9 o altra esecuzione scientifica;
- nessun push, merge o tag.

Il log compatto è
`harness/logs_fix_diagnosi_post_fail_03_13/verification.log`; il manifest associato è
`harness/FIX_DIAGNOSI_POST_FAIL_03_13.manifest.json`.
