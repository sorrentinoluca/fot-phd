OK — chiusura 03.10 limitata all’harness offline sul candidato `dcc742282124784c3fd9004dc642962a9b1e9868`.

# Verifica minima indipendente — chiusura 03.10

Data: 15 settembre 2026. Revisore: Codex, agente basato su GPT-5, finestra `01a0a579-3fd7-7461-8c26-5449bd3d2b7a`. Verifica in sola lettura; nessun sottoagente, servizio, endpoint, SSH, inferenza, pilot o ledger operativo coinvolto.

## Identità e perimetro

- Base: `8fbbfa01820d00562188594123182982939187b2`, tree `965d317985bbcef39bc7358022144fd3bd109e0a`.
- Candidato tecnico: `dcc742282124784c3fd9004dc642962a9b1e9868`, tree `0c203c447e8ebdf2453b6048b6873f6b42e96d4a`.
- Parent effettivo del candidato: `868b1f4317f49877a67d3b76908379c53d6aedc8`.
- Il commit base è antenato del candidato. Il successore `ce4a4cb5bd7748ce1a0c2591acebc402aa8b66ac` aggiunge soltanto il prompt di review ed è escluso.
- Il worktree era sull’HEAD documentale `ce4a4cb`; il file non tracciato `PROMPT_VERIFICA_RECEPIMENTO_DECISIONI_D9_3180AEA.md` era estraneo al delta ed è rimasto intatto.

Il delta esatto contiene dieci file: contratto, approvazione e report della riconciliazione S, dichiarazione di chiusura 03.10, implementazione in `d9.py` e `ledger.py`, test discriminante e risultati rosso/verde. Nessun artefatto congelato in `phase_b/`, `code/`, `reproducibility/` o `tep_*` è modificato. Il controllo `git diff --check` segnala soltanto una riga vuota aggiuntiva a fine file in due documenti; è un rilievo cosmetico non bloccante.

## Esito tecnico

Nessun rilievo bloccante.

Il contratto richiede un pacchetto `MAPPING_REVIEWED` e un’approvazione distinta `IMPORT_AUTHORIZED`, entrambi legati alla fonte S e all’identità esatta `path + pilot_id` del ledger. I quattro mapping devono essere ordinati S1–S4, con identità assegnate esplicitamente durante la riconciliazione. S1 conserva `HISTORICAL_OUTCOME_UNCERTAIN`: il rifiuto HTTP 400 non viene trasformato in prova zero-token D03 e non abilita retry; S2–S4 devono corrispondere alle tre inferenze completate.

L’importazione è racchiusa nella stessa transazione SQLite `BEGIN IMMEDIATE`: legge e valida package, approvazione, review e fonti; crea `external_history`; inserisce quattro righe; registra un solo evento; porta `user_version` da 2 a 3; riconvalida lo stato prima del commit. Un errore dopo il secondo inserimento annulla schema, righe, evento e versione. Il riavvio successivo riesce. Due processi concorrenti producono quattro righe e un solo evento; una seconda applicazione dello stesso package è idempotente, mentre package o approvazione differenti sono rifiutati.

Lo storico è separato dalle richieste native. Le quattro righe contribuiscono una volta a `requests_cumulative` e al limite assoluto 200; i massimi osservabili diventano 156/164, mantenendo 152/160 richieste native. `remediation_calls`, `transport_calls` e l’equazione `8r+t≤15` continuano a dipendere soltanto dalle richieste native. Il controllo dello storico è richiamato nell’inventario degli addebiti e, per un binding D9 esterno, rilegge gli artefatti e confronta package, approvazione, evento e righe nella transazione della decisione. Il test verifica anche la riserva diretta senza rebind, il guasto dopo una precedente riuscita e la contesa sul primo slot nativo: il rifiuto non crea nuovi intenti o invii.

L’implementazione aggiunge una capacità offline, ma non contiene un package reale né quattro identità reali, review del mapping, `IMPORT_AUTHORIZED`, ledger/pilot_id autorizzati o chiamate. L’approvazione acquisita autorizza soltanto l’implementazione test-first e vieta applicazione reale, retry S1, pilot, GO, freeze, push, merge e tag.

Il confine documentato è coerente: 03.10 chiude l’harness offline; endpoint, tokenizer/template, fingerprint, capienza, package reale, ledger e chiamate restano nel preflight/pilot 03.13. La Fase 03 resta aperta.

## Prova eseguita e impronte

Comando eseguito su una copia temporanea estratta con `git archive` dal candidato esatto:

```text
PYTHONDONTWRITEBYTECODE=1 arch -arm64 /usr/local/bin/python3.11 \
  -m unittest -v studio2.fase03.harness.test_history_reconciliation
```

Ambiente osservato: Python 3.11.5, processo `arm64`. Esito indipendente: **10 test, 10 OK, 0 failure, 0 errori**, 1,137 s. Le fixture usano ledger temporanei e non costruiscono trasporti verso servizi.

Impronte ricalcolate direttamente dai blob del candidato:

| Oggetto | Byte | SHA-256 | Risultato registrato |
| --- | ---: | --- | --- |
| `test_history_reconciliation.py` | 20.480 | `ebbe59d6d230f5052d4d8cd4beb5492e23452824aca0fb01111648565409e88c` | stessi byte dichiarati per rosso/verde |
| `red.log` | 16.222 | `2564a0a437d80e8ec72195d7449263f1c24807d1763ad55e8b9500112ffabd51` | parent: 10 test, 1 failure, 15 errori |
| `green.log` | 3.385 | `97dd4671d5afb930181eb43a4e055214d546e7bbebe92c1e2055b7134bb9f76e` | candidato: 10/10 OK |

Il rosso registrato è discriminante: sul parent manca l’API `reconcile_external_history`; non è stato rieseguito in questa review minima. Le impronte e i conteggi dei due log coincidono con `history_reconciliation_evidence/RESULTS.json`.

## Limiti del verdetto

Come richiesto, non ho rieseguito suite complete, regressioni dipendenti o guardiano. I relativi risultati restano evidenza registrata, non risultato indipendentemente rieseguito qui. Il guardiano conserva la descrizione storica **NON PASS: 35 test, 14 fallimenti, 1 skip, 0 errori**; questa review non lo riclassifica.

L’OK vale per il solo delta `8fbbfa0..dcc7422`, per l’atomicità, l’idempotenza e l’addebito prudenziale S=4 verificati offline. Non qualifica servizi, non approva capienza/T5, non autorizza importazione reale, inferenze, pilot, GO, freeze o chiusura della Fase 03.
