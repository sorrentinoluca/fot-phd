# Contratto implementato — riconciliazione dello storico S esterno

**Stato:** candidato tecnico offline; applicazione al ledger reale non autorizzata.

Base tecnica e documentale:
`8fbbfa01820d00562188594123182982939187b2`. La procedura proposta in
`PROPOSTA_RICONCILIAZIONE_STORICO_S_ESTERNO_2026-09-15.md` è stata approvata
dall'autore il 15 settembre 2026 per la sola implementazione test-first; il
record conserva il testo originale in
`APPROVAZIONE_IMPLEMENTAZIONE_RICONCILIAZIONE_STORICO_S_2026-09-15.md`.

## Oggetti richiesti

L'importazione accetta due file assoluti e recuperabili:

1. un pacchetto `MAPPING_REVIEWED`, con fonte S pinnata, ledger destinatario,
   riferimenti con SHA-256 a summary, attempts, records e verbale indipendente,
   e quattro mapping ordinati S1–S4;
2. un'approvazione `IMPORT_AUTHORIZED` che lega autore, SHA-256 del pacchetto,
   fonte e identità esatta del ledger.

Ogni mapping contiene un `request_id` nuovo, l'identità canonica e il suo hash,
il binding alla riga sorgente e la disposizione. L'identità dichiara
`ASSIGNED_DURING_RECONCILIATION`: non viene presentata come identità storica
recuperata. S1 ammette soltanto `HISTORICAL_OUTCOME_UNCERTAIN`; HTTP 400 e
`inference_completed=false` non diventano prova zero-token e non abilitano retry.
S2–S4 devono legarsi alle tre righe completate.

## Transazione e rappresentazione

`PilotLedger.reconcile_external_history` legge package, approvazione, verbale e
fonti, valida contenuto e impronte, crea la tabella separata
`external_history`, inserisce esattamente quattro righe, registra un solo evento
e porta esplicitamente lo schema da v2 a v3 in un'unica transazione
`BEGIN IMMEDIATE`. Un errore intermedio lascia schema, righe ed evento invariati.
Una seconda applicazione dello stesso pacchetto è idempotente; un pacchetto
diverso o uno stato parziale viene rifiutato.

Le righe storiche non entrano in `requests` e quindi non simulano chiamate del
nuovo pilot. Contribuiscono una volta a `requests_cumulative` e al limite
cumulativo 200. I massimi osservabili diventano 156/164 quando le quattro righe
sono presenti, mantenendo 152/160 come massimo delle richieste native. Le quote
remediation e transport restano calcolate solo dalle richieste native.

## Riconferma e rifiuto preventivo

Ogni binding o riserva scientifica con configurazione D9 esterna rilegge e
ricontrolla package, approvazione, verbale, fonti, mapping e righe v3 nella
transazione della decisione, prima dell'inserimento dell'intento. Mancanze,
duplicati, scambi, alterazioni, tipi errati, ledger diverso, cache stantia o
assenza di binding producono rifiuto. Le precedenze diagnostiche storiche
legittime restano invariate.

Questo contratto non crea un pacchetto reale, non assegna le quattro identità
reali, non approva un mapping, non modifica un ledger operativo e non concede
chiamate, pilot, retry, GO o freeze.

