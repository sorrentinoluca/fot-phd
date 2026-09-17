OK — limitato all'importazione dello storico S=4 nel ledger pilot indicato.

# Verifica indipendente import storico S=4 — 03.13

## Identità, mandato e metodo

- Revisore: Codex, agente basato su GPT-6; identificatore backend e livello di reasoning non attestati da questa verifica.
- Finestra: 2026-09-16, Europe/Rome; controllo programmatico terminato il 2026-09-15 alle 23:26:47 UTC (01:26:47 Europe/Rome).
- Mandato: `/Users/luker/fot-tep/studio2/fase03/PROMPT_VERIFICA_IMPORT_STORICO_S4_LEDGER_PILOT_03_13.md`.
- Candidato: `/Users/luker/.codex/worktrees/dd86/fot-tep`.
- Worktree indipendente di consegna: `/Users/luker/.codex/worktrees/c91a/fot-tep`.
- Verbale: `/Users/luker/.codex/worktrees/c91a/fot-tep/studio2/fase03/harness/VERIFICA_IMPORT_STORICO_S4_LEDGER_PILOT_03_13.md`.

Sono stati applicati il contratto `docs/MAINTENANCE.md` e la skill
`fot-tep-harness-lessons`, con particolare attenzione a ricalcolo delle fonti,
distinzione fra identità assegnate e storiche, conservazione dell'incertezza S1
e distinzione fra verifiche eseguite e ispezione del codice.

Verifica effettuata tramite comandi Git di lettura, SHA-256, validatore del
candidato e query SQLite. Gli script di controllo sono stati eseguiti in memoria
con `/usr/bin/python3 -B`, senza creare file Python o bytecode. L'unico artefatto
creato è questo verbale nel worktree indipendente. Nessuna suite ampia o guardian
è stata rieseguita, come richiesto espressamente dal mandato.

## 1. Candidato e delta — PASS

| Oggetto | Valore verificato |
| --- | --- |
| Commit HEAD | `d38da38b96d252ba1a224b6f373cb08ca519a1ed` |
| Tree | `02ad075223d42bf3db0d17927c9938a6274ecc75` |
| Parent | `5ef87e3deea670cc343ae6cf8a7c2338922fb810` |
| Stato candidato | pulito, prima e dopo i controlli |

`git diff-tree` restituisce esattamente due aggiunte:

- `studio2/fase03/harness/IMPORT_AUTHORIZED_STORICO_S4_PILOT_03_13.json`;
- `studio2/fase03/harness/REPORT_IMPORT_STORICO_S4_PILOT_03_13.md`.

Nessuna modifica a runtime, configurazioni, test, mapping o fonti. I byte locali
di mapping, approval e rapporto sono stati confrontati anche con i rispettivi
blob del commit candidato: coincidono.

## 2. Hash e validazione semantica — PASS

Percorsi dei tre artefatti sotto
`/Users/luker/.codex/worktrees/dd86/fot-tep/studio2/fase03/harness/`.

| Artefatto | SHA-256 ricalcolato |
| --- | --- |
| `MAPPING_REVIEWED_STORICO_S4_PILOT_03_13.json` | `98608abe9831707254208ed29e493f92d29c06313a219d238ceec933f064d53c` |
| `IMPORT_AUTHORIZED_STORICO_S4_PILOT_03_13.json` | `aaefae11807826b4eedb3a3a917a86f33f7ff6d5c5c9442b8a468f630f13f7cb` |
| `REPORT_IMPORT_STORICO_S4_PILOT_03_13.md` | `382ba3199b45d39943fbefaab129a7ff3d24542854f094f0978ecda649812607` |

Tutti gli hash coincidono con il mandato e sono rimasti invariati al termine
del controllo programmatico.

È stata eseguita realmente `validate_external_history_artifacts(...)`, importata
da `/Users/luker/.codex/worktrees/dd86/fot-tep/studio2/fase03/harness/d9.py`;
il percorso del modulo è stato verificato. Parametri: mapping e approval come
percorsi assoluti, `expected_ledger` con il path operativo e il `pilot_id` prescritti.
Esito: **quattro mapping validi**.

L'approval ha autore esatto `Luca Sorrentino` e decisione `IMPORT_AUTHORIZED`;
lega l'hash effettivo del mapping, il ledger esatto e la fonte storica con quattro
richieste e tre inferenze completate. Il validatore ha riletto e controllato
schema, riferimenti, fonte, verbale referenziato, cardinalità, ordinali, identità,
unicità, binding e contenuto delle risposte complete.

Hash delle fonti primarie ricalcolati sui file referenziati, sotto
`/Users/luker/fot-tep/studio2/fase03/results/provisional_cap_stress/`:

| Fonte | SHA-256 |
| --- | --- |
| `provisional_stress_probe_summary.json` | `c9adf2a8f07d9058257cc2c51a00064662874611875a715c716a1f1ea4828368` |
| `provisional_stress_probe_attempts.jsonl` | `cc3a21d8a045598b844372b04af4a68a4ac6702c05c5428a457eed098f03c382` |
| `provisional_stress_probe_records.jsonl` | `825b649e409e462b953da263fd01d11b9d92563fd930747da17e36f93d94b158` |

È stata inoltre ricalcolata per tutte le identità la formula
`SHA256(canonical_json([pilot_id, "external_history", ordinale, SHA256(canonical_json(source_binding))]))`:
corrispondenza 4/4. S1 lega `attempts:1`; S2–S4 legano nell'ordine `records:1–3`.

S1 mantiene `HISTORICAL_OUTCOME_UNCERTAIN`. Il solo record storico HTTP 400 con
`inference_completed=false` non contiene contatori token, prova zero-token o
legame di retry; il mapping e le righe importate non ne aggiungono. Le identità
restano marcate `ASSIGNED_DURING_RECONCILIATION`.

S2–S4 mantengono `COMPLETED`. Il validatore ha verificato raw-output hash,
response ID, modello, fingerprint, finish reason, contenuto del messaggio e
coerenza usage. Controlli aggiuntivi eseguiti sui tre record: `parsed_output`
uguale al parsing del raw, timestamp uguale al secondo `response_raw.created`,
tipi interi anche nei contatori usage dell'envelope e `retry_count=0`.

Il campo `review` del mapping conserva il precedente verbale limitato a
ricognizione/proposta. L'ACCEPT del mapping esatto è stato espresso nella review
precedente di questa conversazione e viene distinto nel rapporto d'importazione
dalla successiva approval. Il solo valore di schema `MAPPING_REVIEWED` non è stato
trattato come autorizzazione; qui è presente e verificata la distinta approval.

## 3. Ledger operativo e copie consistenti — PASS

Directory: `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001/`.
Ogni database è stato aperto esclusivamente con URI
`file:<percorso-assoluto>?mode=ro&immutable=1`
e `PRAGMA query_only=ON`. Nessun costruttore `PilotLedger`, metodo d'importazione,
backup, migrazione o checkpoint è stato eseguito durante questa review.

| Database | Byte | Schema | `integrity_check` | Storico | Eventi | Richieste native |
| --- | ---: | ---: | --- | ---: | ---: | ---: |
| `ledger.pre-import-5ef87e3.sqlite3` | 61440 | v2 | `ok` | tabella assente | 0 | 0 |
| `ledger.post-import-5ef87e3.sqlite3` | 81920 | v3 | `ok` | 4 | 1 | 0 |
| `ledger.sqlite3` | 81920 | v3 | `ok` | 4 | 1 | 0 |

| Database | SHA-256 prima e dopo la lettura |
| --- | --- |
| Pre-import | `41ccea51f9c2dc695c62490d2684c6e3cdb2f34bc39179d35fc4a2340b77b0fe` |
| Post-import | `6a6a2cf06c2a2e5f5fa6502ef68524c99d9a1abce00716b4a1ce577c6c38b420` |
| Operativo | `02ce8df46d04300b9eb19b0fbc3345c5edd41e7ea17bd1391f22c53f7a6d9d61` |

Tutti e tre hanno un'unica riga `pilot` con ID
`studio2-fase03-d9-pilot-001`. Le tabelle `requests`, `stages`, `responses` e
`receipts` sono vuote in tutti e tre. Il pre-import non ha tabella
`external_history` né eventi. Sono state controllate tutte le tabelle presenti,
senza tabelle ulteriori rispetto allo schema atteso.

Le quattro righe del ledger operativo e della copia post-import sono state
confrontate integralmente con quelle derivate dal mapping validato, includendo
`request_id`, ordinale, byte JSON canonici di identità e binding, relativi hash,
disposizione e hash del package: **uguaglianza esatta 4/4 per entrambi**.

L'unico evento, identico nei due database v3, è:

```text
history_reconciliation:98608abe9831707254208ed29e493f92d29c06313a219d238ceec933f064d53c
```

Ha `created_utc=2026-09-15T23:17:38.706029+00:00`, `artifact_sha256` uguale
all'hash del mapping e dettaglio esatto:

```json
{"approval_sha256":"aaefae11807826b4eedb3a3a917a86f33f7ff6d5c5c9442b8a468f630f13f7cb","count":4,"package_sha256":"98608abe9831707254208ed29e493f92d29c06313a219d238ceec933f064d53c","status":"RECONCILED"}
```

Lo schema SQL completo e tutte le righe della copia post-import coincidono con
quelli del ledger operativo. Le differenti impronte fisiche non corrispondono
a differenze logiche. Byte e mtime di ciascuno dei tre database sono rimasti
identici dopo l'accesso. La directory è rimasta invariata, senza WAL/SHM/journal.

Conteggio ricavato direttamente dalle query: `historical_requests=4`,
`native_requests=0`, `requests_cumulative=4`; remediation e transport registrati
pari a zero. Nessuno stage, evento scientifico, probe, gate o pilot risulta
registrato. Questo rilievo riguarda il contenuto del ledger, non un audit
indipendente dei log remoti del provider.

## 4. Secondo richiamo e idempotenza — ispezione conforme

È stato ispezionato `PilotLedger.reconcile_external_history` nel candidato,
in particolare `ledger.py:194–235` e i validatori richiamati.

Con righe già presenti, il metodo riconferma gli artefatti e lo stato storico,
verifica hash del package e dell'approval e ritorna
`{'status': 'ALREADY_RECONCILED', 'historical_requests': 4}` prima di raggiungere
`CREATE TABLE`, inserimenti, creazione evento e passaggio di schema. Le funzioni
richiamate nel ramo eseguono letture e validazioni. Pertanto, per lo stato e gli
artefatti esatti verificati, il secondo richiamo identico descritto nel rapporto
è coerente con il codice e non aggiunge righe o eventi.

La review non ha eseguito un ulteriore richiamo d'importazione. Non attesta di
aver osservato direttamente il secondo richiamo storico né riprodotto il digest
del confronto prima/dopo riportato dal suo autore; verifica il ramo per ispezione
e lo stato finale reale mediante query, come richiesto dal mandato.

## 5. Verdetto e limiti

**OK**: tutti i controlli richiesti su candidato, artefatti, validazione semantica,
ledger operativo, copie e ramo idempotente risultano conformi. Nessun rilievo
bloccante nel perimetro dell'importazione S=4 su questi byte e su questo ledger.

L'OK certifica quattro contributori storici contabilizzati una sola volta, con
S1 incerto e zero richieste native. Non autorizza pilot, gate, chiamate Qwen,
retry S1, GO o freeze e non costituisce una nuova review generale del runtime.

Il candidato, il ledger, le copie, mapping, approval e fonti sono stati soltanto
letti. Nessuna chiamata esterna o esecuzione scientifica, nessun commit, push,
merge o tag. Consegna del solo presente verbale nel worktree indipendente.
