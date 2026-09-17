# Decisione autoriale e inizializzazione ledger — mapping S=4, 03.13

Data: 2026-09-16. Stato: **PREPARATO PER REVIEW; IMPORT NON AUTORIZZATO**.

## Decisione conservata letteralmente

Contesto approvato: addebito prudenziale dello storico **S=4 una sola volta** e
creazione offline del ledger del nuovo pilot; nessuna chiamata Qwen autorizzata.

> Se è la scelta migliore per il fine: realizzare l'esperimento nel miglior modo scientificamente possibile a prova di review critica, si

Questa decisione approva S=4 e l'inizializzazione vuota del ledger, ma non sostituisce
`IMPORT_AUTHORIZED`. L'hash definitivo del mapping candidato deve essere verificato da
una review indipendente e poi legato da una successiva autorizzazione esplicita prima
di qualunque importazione.

## Identità del ledger inizializzato

- `pilot_id`: `studio2-fase03-d9-pilot-001`
- path: `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001/ledger.sqlite3`
- schema SQLite: `PRAGMA user_version=2`
- SHA-256 della fotografia vuota iniziale:
  `eb50e984cacaaddd3d0fa36a221f191285b59cd8fa7c1f3fc34dd04179799fee`
- dimensione iniziale: 61.440 byte

La fotografia iniziale registra soltanto l'identità del pilot. Al controllo successivo
all'inizializzazione: una riga `pilot`, zero `requests`, zero `stages`, zero `events`,
zero `responses`, zero `receipts`; la tabella `external_history` non esiste. L'hash del
database è una fotografia di inizializzazione, non un identificatore immutabile del
ledger dopo future mutazioni autorizzate.

## Mapping candidato

Il package [MAPPING_REVIEWED_STORICO_S4_PILOT_03_13.json](MAPPING_REVIEWED_STORICO_S4_PILOT_03_13.json)
ha SHA-256
`98608abe9831707254208ed29e493f92d29c06313a219d238ceec933f064d53c`.
Il valore di schema `MAPPING_REVIEWED` identifica il formato atteso dal contratto;
questo record non afferma che il mapping esatto abbia già superato la nuova review.
La review precedente nel campo `review` copre soltanto ricognizione e proposta, come
dichiarato testualmente nello stesso campo.

Le identità sono nuove e non storiche. Per ciascun ordinale `n`, il `request_id` è:

```text
SHA256(canonical_json([pilot_id, "external_history", n,
                       SHA256(canonical_json(source_binding))]))
```

Ogni identità dichiara `ASSIGNED_DURING_RECONCILIATION` e lega il digest del proprio
`source_binding`.

| Ordinale | request_id | identity_sha256 | Disposizione |
| --- | --- | --- | --- |
| S1 | `2816b74ff6df290645d411841d5b3fe52f9c8a94f51d8b2504add3ddb06798d7` | `574d3335db3e364f2428903422336def278f71a2cd27f395ab1c3f38020e0dde` | `HISTORICAL_OUTCOME_UNCERTAIN` |
| S2 | `bc65836bf364bee2d2221ae161edc6027eb4097c4fe06b89cd356d511b44531a` | `b601d3c547ab60de08d4d3ea5f3138d5fa6dfa7373a0864d93f0f7b61bc31e31` | `COMPLETED` |
| S3 | `b398041eb723f70febf057bbfe5f532a8f6392d01ae1076bfa83b5e4c83f7a81` | `29067d59635ac9bcd059e9718e79e0f01f490a9a69535ea1c303f4d09063d0c4` | `COMPLETED` |
| S4 | `6842b2d03d8de8253539922fe529d0700309b64a7fb2fa60d477d694d72260e5` | `0bfa66fe054d6f9a5c380f85c0f9adacb11d145b374ff2830295cbf25f25a04b` | `COMPLETED` |

S1 conserva il solo HTTP 400 storico come esito incerto: non è prova zero-token,
non abilita retry e non inventa usage. S2–S4 sono legate, nell'ordine, alle righe 1–3
dei record completi. Le tre risposte completate sono un sottoinsieme dei quattro
tentativi e non producono addebiti ulteriori.

## Limiti

Il mapping non è stato applicato. Non esistono `IMPORT_AUTHORIZED`, righe
`external_history`, eventi di riconciliazione, richieste native o chiamate. Non sono
autorizzati provider, endpoint, sonda, gate, batch, pilot, retry S1, `pilot_go=true`,
freeze o GO operativo.
