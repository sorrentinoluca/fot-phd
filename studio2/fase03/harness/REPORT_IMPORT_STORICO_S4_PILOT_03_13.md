# Rapporto importazione una tantum storico S=4 — ledger pilot 03.13

Data: 2026-09-16. Esito: **RECONCILED**.

## Identità e decisioni distinte

- HEAD iniziale: `5ef87e3deea670cc343ae6cf8a7c2338922fb810`, tree
  `8ee84bfd76026452975ab5b2593916faf11c10e0`.
- Mapping revisionato:
  `MAPPING_REVIEWED_STORICO_S4_PILOT_03_13.json`, SHA-256
  `98608abe9831707254208ed29e493f92d29c06313a219d238ceec933f064d53c`.
- Review indipendente: `ACCEPT` sul mapping esatto, acquisito come presupposto nel
  mandato d'importazione; da solo non autorizzava la mutazione.
- Autorizzazione d'autore:
  `IMPORT_AUTHORIZED_STORICO_S4_PILOT_03_13.json`, autore Luca Sorrentino,
  SHA-256 `aaefae11807826b4eedb3a3a917a86f33f7ff6d5c5c9442b8a468f630f13f7cb`.
- Applicazione: una singola chiamata a `PilotLedger.reconcile_external_history` sui
  due file esatti, seguita da un solo richiamo di verifica idempotente.

Ledger destinatario:
`/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001/ledger.sqlite3`,
`pilot_id=studio2-fase03-d9-pilot-001`.

## Stato pre-import e copia consistente

L'impronta pre-import del ledger coincideva con la review:
`eb50e984cacaaddd3d0fa36a221f191285b59cd8fa7c1f3fc34dd04179799fee`.
Il controllo in sola lettura ha confermato schema v2, riga pilot esatta, zero righe
in `requests`, `stages`, `events`, `responses` e `receipts`, nessuna tabella
`external_history` e nessun evento di riconciliazione.

Copia SQLite consistente creata mediante `sqlite3.Connection.backup`, senza
sovrascrittura:

- path: `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001/ledger.pre-import-5ef87e3.sqlite3`
- SHA-256: `41ccea51f9c2dc695c62490d2684c6e3cdb2f34bc39179d35fc4a2340b77b0fe`
- `PRAGMA integrity_check=ok`, schema v2, zero richieste native.

## Validazione e importazione

Prima della mutazione, `validate_external_history_artifacts` ha ricalcolato e
validato package, approval, fonti e quattro mapping. Esito: 4/4 righe valide con
disposizioni `HISTORICAL_OUTCOME_UNCERTAIN`, `COMPLETED`, `COMPLETED`, `COMPLETED`.

L'importazione reale ha restituito:

```text
{'status': 'RECONCILED', 'historical_requests': 4}
```

Righe registrate:

| Ordinale | request_id | Disposizione |
| --- | --- | --- |
| S1 | `2816b74ff6df290645d411841d5b3fe52f9c8a94f51d8b2504add3ddb06798d7` | `HISTORICAL_OUTCOME_UNCERTAIN` |
| S2 | `bc65836bf364bee2d2221ae161edc6027eb4097c4fe06b89cd356d511b44531a` | `COMPLETED` |
| S3 | `b398041eb723f70febf057bbfe5f532a8f6392d01ae1076bfa83b5e4c83f7a81` | `COMPLETED` |
| S4 | `6842b2d03d8de8253539922fe529d0700309b64a7fb2fa60d477d694d72260e5` | `COMPLETED` |

S1 non contiene prova zero-token, non è stato trasformato in richiesta nativa e non
ha acquisito diritto al retry.

Evento unico:

```text
history_reconciliation:98608abe9831707254208ed29e493f92d29c06313a219d238ceec933f064d53c
```

Il relativo `artifact_sha256` coincide con il package e il dettaglio lega
`approval_sha256=aaefae11807826b4eedb3a3a917a86f33f7ff6d5c5c9442b8a468f630f13f7cb`,
`count=4`, `status=RECONCILED`.

## Snapshot finale e idempotenza

```json
{
  "user_version": 3,
  "requests_cumulative": 4,
  "native_requests": 0,
  "historical_requests": 4,
  "unresolved_intents": 0,
  "remediation_calls": 0,
  "transport_calls": 0,
  "reserve_equation_value": 0,
  "reserve_limit": 15,
  "planned_maximum": 156,
  "hard_stop": 200,
  "durable_responses": 0,
  "history_reconciliation_events": 1
}
```

Il secondo e ultimo richiamo della stessa API con gli stessi file ha restituito:

```text
{'status': 'ALREADY_RECONCILED', 'historical_requests': 4}
```

Lo stato logico completo prima e dopo è byte-canonicalmente identico, SHA-256
`5864386fb4c21824acfb82952568bfd3b77b7f27a5f553d19748b2e73d6b2de9`.
Non è stato eseguito un terzo richiamo.

Il primo script di verifica post-import aveva confrontato per errore un oggetto
`sqlite3.Row` con una tupla e si era fermato su quell'asserzione locale. Nessuna API
d'importazione è stata richiamata in quel controllo; le stesse query, con il confronto
corretto, hanno prodotto il PASS completo riportato sopra.

Copia SQLite consistente post-import:

- path: `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001/ledger.post-import-5ef87e3.sqlite3`
- SHA-256: `6a6a2cf06c2a2e5f5fa6502ef68524c99d9a1abce00716b4a1ce577c6c38b420`
- `PRAGMA integrity_check=ok`, schema v3, quattro righe storiche, un evento,
  zero richieste native.

SHA-256 del ledger operativo post-import:
`02ce8df46d04300b9eb19b0fbc3345c5edd41e7ea17bd1391f22c53f7a6d9d61`.

## Limiti rispettati

La risoluzione assoluta dei due path repository è stata necessaria perché il
validatore corrente rifiuta riferimenti relativi; i byte e i file passati all'API sono
quelli prescritti. Non sono stati modificati mapping, fonti storiche, runtime, test,
configurazioni o quote native/remediation/transport. Database e copie runtime non sono
inclusi nel repository.

Zero chiamate provider/endpoint, zero richieste native, nessun probe, gate, batch o
pilot. Nessun retry S1, GO, merge, rebase, push o tag. Questa importazione contabilizza
S=4 una sola volta e non autorizza l'avvio del pilot.
