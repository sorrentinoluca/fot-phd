# Evidenza materializzazione offline pilot-03 — successor 122B Qwen D9

Data: 2026-09-16, Europe/Rome. Worktree: `dd86`, HEAD pre-esecuzione
`a199d6f9d974503f68b22791680d56f95fcd7e43`, tree `88cd9cc12b0c28dfdf27048d5a6a3dd6de25e3b5`.

## Esito

**TARGET MATERIALIZED — READY FOR INDEPENDENT REVIEW (author)**

Il comando è stato eseguito una sola volta con `/usr/local/bin/python3` (Python 3.11.5):

```text
/usr/local/bin/python3 studio2/fase03/materialize_successor_recovery.py --execute --acknowledge MATERIALIZE_PHASE03_122B_SUCCESSOR_OFFLINE
```

Exit code: `0`. Nessun retry, authorization, qualifica, chiamata 122B/27B, tunnel, VPN o
accesso al server. Log integrale: `logs_materializzazione_pilot_03/materialize_successor_recovery.stdout-stderr.log`.

## Pre-condizioni e budget

- materializzatore SHA-256: `5b9ad9e9c0264fe8c02a5c0e77d3f349e13398b1d4df1c4c1e83634f55b59be7`;
- target assente prima dell'esecuzione; `pilot-002` presente e intoccato;
- `pilot-001/ledger.sqlite3`: SHA-256 invariato `4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`;
- deroga autorizzata dall'autore: `ledger.sqlite3-wal` 0 byte, mtime
  `2026-09-16T03:29:15+0200`, `-rw-r--r--`; `ledger.sqlite3-shm` 32768 byte, mtime
  `2026-09-16T03:31:41+0200`, `-rw-r--r--`; `lsof` exit `1`, nessun processo. I sidecar non
  sono stati cancellati né toccati;
- budget nel summary: `S=5`, `technical=1`, `planned_maximum=166`, `hard_stop=200`,
  `non_spendable_margin=34`;
- `network.provider_calls=0`, `tokens=0`, `tunnels=0`; `execution_authorization=ABSENT`.

## Target pubblicato

Root: `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03`.
Tutte le directory sono `0700` e tutti i file `0600`; non esistono staging sibling, sidecar
SQLite o filename contenenti `authorization`. Il publish lock esiste e `flock(LOCK_EX|LOCK_NB)`
ha avuto esito `SUCCESS`.

Il summary privato ha `status=READY_FOR_INDEPENDENT_REVIEW` e digest stdout:

```text
configuration_sha256 6f8d616c1f75596ddff480b6bd4c01481adb85343c99205ea2a51d129c99da4f
ledger_sha256        8af057b5e295a21a3aa178e414673f4fe6e76979670a2b74a5a487606b4e01f1
predecessor_sha256   4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb
```

Il campo `references` non è presente come array nel summary (`null`); sono stati invece
ricomputati e verificati tutti gli otto riferimenti nominati nel summary, con path sotto il
target e senza `.staging-`. L'elenco completo path/hash, incluse le risorse private non
committate, è nel manifest di questa evidenza.

## Invarianze e limiti

Il listing di `pilot-001` è stato verificato post-materializzazione con i sidecar inclusi;
ledger SHA e metadati dei sidecar corrispondono alla deroga registrata. `pilot-002` è presente
e non è stato aperto o modificato. Il repository contiene solo evidenza, log e aggiornamenti
documentali; nessun contenuto privato è incluso. La review resta nella finestra `b567`.

## Riferimento review

Il report, il manifest precedente e la supersessione di `a199d6f` riportano il verbale corrente
SHA-256 `46a6d426aa05f44fda1ea994a89f3d04cede01331ebdc4866be37fd34b252f0f`, con nota:
“pre-addendum `00f0a97e20ef858ff9bd9226525ebe9fc4b357e8847a8e6b0059bf6952670104`, verdetto invariato”.
