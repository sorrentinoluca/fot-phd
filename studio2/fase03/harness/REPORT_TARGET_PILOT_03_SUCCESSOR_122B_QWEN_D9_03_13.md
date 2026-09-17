# Target fresco pilot-03 e chiusura deterministica del ledger — successor 122B Qwen D9 03.13

## Esito

**READY FOR INDEPENDENT REVIEW (author).** Materializzazione offline completata sul candidato
`79ce7da5f869c96a718e73a328ac8bcbab0b547e` (tree `eb173bc6f2e89d25d9da708dce071db3d233d85b`),
branch `codex/studio2-config-122b-accounting`, prompt 03.13-TARGET. Commit e tree del nuovo
candidato sono riportati nell'handoff, dopo la finalizzazione degli artefatti, per evitare
riferimenti circolari. Manifest: `TARGET_PILOT_03_SUCCESSOR_122B_QWEN_D9_03_13.manifest.json`.

Nessuna authorization, qualifica, chiamata 122B/27B, tunnel o VPN; la materializzazione è stata
offline e senza transport.
`/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001` e `…-pilot-002` non sono stati
toccati né aperti; `server_enea.json` non è stato letto.

Il verbale di review indipendente (`VERIFICA_CANDIDATO_79CE7DA_…`, SHA-256
`46a6d426aa05f44fda1ea994a89f3d04cede01331ebdc4866be37fd34b252f0f`, verdetto invariato;
pre-addendum `00f0a97e20ef858ff9bd9226525ebe9fc4b357e8847a8e6b0059bf6952670104`) e il parere Claude
(`reviews/PARERE_CLAUDE_SU_VERIFICA_79CE7DA_03_13.md`, SHA-256 `12e77f43…6d`, lasciato untracked)
sono solo contesto: P1-02a/b, P2-01, P2-02 e `identity_sha256` non sono stati rifatti.

## 1. Pilot id/path fresco

`studio2/fase03/materialize_successor_recovery.py`, r. 35–36:

```text
TARGET_ROOT        = /Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03
SUCCESSOR_PILOT_ID = studio2-fase03-d9-pilot-03
```

`grep -rn pilot-002 studio2/fase03 --include=*.py` non restituiva altri punti runtime/test che
derivassero id o path del successor: ledger ref, approval, staging `.studio2-fase03-d9-pilot-03.staging-*`,
lock e config derivano tutti dalle due costanti. Dopo il delta le sole occorrenze di `pilot-002`
nei `.py` sono le due asserzioni negative del test (a). Predecessore `pilot-001`, il suo SHA-256
`4802d791…1eb` e la lineage S=5 sono invariati.

## 2. Chiusura esplicita post-checkpoint

Il checkpoint resta nello stesso punto (dopo l'ultima scrittura sul ledger successor e il
controllo S=5/166/34, prima di ogni hash). Nuovo helper `_checkpoint_and_close_ledger`:

- `closing(sqlite3.connect(...))` esegue `PRAGMA wal_checkpoint(TRUNCATE)` e chiude la connessione
  in modo deterministico; un checkpoint `busy` fallisce chiuso;
- se la build SQLite mantiene sidecar vuoti dopo l'ultima chiusura (persistent WAL, come la
  SQLite di sistema Apple), `-wal`/`-journal` vengono rimossi solo se di 0 byte e `-shm` viene
  rimosso; un sidecar non vuoto fallisce chiuso (staging rimosso, target assente);
- `_assert_no_ledger_sidecars` ricontrolla l'assenza di sidecar dopo il checkpoint e di nuovo
  prima del ritorno del builder, quindi prima della pubblicazione.

Il riferimento Python all'istanza `PilotLedger` di staging viene rilasciato (`del successor`);
`PilotLedger` non tiene connessioni aperte fuori da `_transaction()`.

## 3. Confine post-rename (opzionale, fatto)

In `_publish_staged` un flag `published` diventa vero subito dopo `os.rename`. Un `OSError` in
`open`/`fsync` della directory padre solleva la nuova `PublishedDirectoryFsyncError`
(sottoclasse di `RuntimeError`) con `published=True`, `target` e `result` del builder, e
`__cause__` pari all'errore originale. Il ramo di cleanup non tocca mai nulla se `published` è
vero: il target pubblicato non viene cancellato né riscritto; una nuova pubblicazione resta
rifiutata con `already exists` senza eseguire il builder. Il file `.<target>.publish.lock` nel
genitore resta, come prima (rilievo documentale P3 del parere).

## 4. Documenti

- `SUPERSESSIONE_TARGET_PILOT_03_SUCCESSOR_122B_QWEN_D9_03_13.json`: il contratto congelato
  `CONTRATTO_RECUPERO_SUCCESSOR_122B_QWEN_D9_03_13.json` (SHA-256 `143e709a…f37a`) non è
  riscritto; è superato solo nel campo `successor.pilot_id`. `pilot-002` = candidato v4
  preesistente non migrato, mai materializzato da questa linea; `pilot-03` = target fresco.
- Questo report e il manifest; log in `logs_target_pilot_03/`.

## Test nuovi (`harness/test_successor_recovery.py`, classe `FreshTargetPilot03Tests`)

Il fixture esegue il vero `_publish_staged(_materialize_tree)` su un predecessore sintetico
offline (ledger fixture S=5, config/provider sintetici, copia byte-identica di proposta e
supplemento), con tutte le costanti di path patchate in una directory temporanea.
`d9.validate_config` è mockato: la validazione D9 completa è coperta dagli altri test; qui sono
sotto test solo finalizzazione del ledger e pubblicazione.

| Test | Contenuto | `79ce7da` + test nuovi | Candidato |
|---|---|---|---|
| (a) `test_T_a_…` | costanti `pilot-03` coerenti, diverse da `pilot-002`/`pilot-001`; predecessore invariato; nessun `pilot-002` nel sorgente | FAIL | OK |
| (b) `test_T_b_…` | target pubblicato con solo `ledger.sqlite3`, nessun `-wal`/`-shm`; SQLite persistent-WAL simulata con un proxy di connessione | FAIL (sidecar presenti) | OK |
| (c) `test_T_c_…` | riapertura del ledger pubblicato con `identity_path` di default, lineage 5/0/0 riautenticata, reimport rifiutato, poi hash di ledger e di tutti i riferimenti durevoli (summary + config) ricontrollati; insieme dei file invariato | **OK** | OK |
| (d) `test_T_d_…` | `os.fsync` iniettato a EIO solo sulle directory: `PublishedDirectoryFsyncError`, `published=True`, causa EIO, target intatto, nessuno staging residuo, ripubblicazione rifiutata senza builder | FAIL | OK |

**Deviazione dichiarata su (c).** Il prompt chiede che (c) fallisca sui byte `79ce7da`: non
fallisce. Sui byte `79ce7da` gli hash erano già corretti (checkpoint prima di ogni hash, nessuna
scrittura successiva), come già valutato nel parere (P3 non bloccante). (c) resta quindi una
guardia di regressione, non una prova rossa; non è stato forzato un rosso artificiale.
Discriminanti: (a), (b), (d). Log: `logs_target_pilot_03/red_79ce7da_bytes_with_new_tests.log`
(32 metodi, 3 failure attese, 0 errori).

## Verifiche

Ambiente: VM Linux del Mac collegato (Python 3.10.12, SQLite 3.37.2), non l'interprete arm64
macOS. Installati nella VM, fuori dal repository, `transformers 4.57.6` e `jsonschema 4.26.0`
da PyPI (unica attività di rete; nessun provider). I test che usano path assoluti
`/Users/luker/...` (worktree di verifica storiche, evidence 03.6) non possono girare nella VM:
per questo ogni suite è stata eseguita **anche sui byte `79ce7da`** nello stesso ambiente, con
confronto test per test. Unica differenza: i 4 test nuovi.

| Suite | Candidato | Base `79ce7da` (stesso ambiente) |
|---|---|---|
| Successor mirata | 32/32 OK, 5,8 s | 28/28 OK |
| Discovery harness (`discover -s studio2/fase03/harness`) | 185 eseguiti: 150 OK, 2 FAIL, 33 ERROR, 47,2 s | 181 eseguiti: 146 OK, 2 FAIL, 33 ERROR, 46,3 s |
| Regressione pertinente, 15 moduli (esecuzione per modulo) | 198 eseguiti: 164 OK, 2 FAIL, 33 ERROR | 194 eseguiti: 160 OK, 2 FAIL, 33 ERROR |
| `py_compile` dei due moduli toccati | PASS | — |
| Validazione JSON (supersessione, manifest) | PASS | — |
| `git diff --check` | PASS | — |

Sui 15 moduli i non-OK sono concentrati in `test_c01_c03` (1F+9E), `test_d01_replay` (errore
di import del modulo: `git -C /Users/luker/fot-tep-riverifica-harness-…`), `test_d02` (1E),
`test_d03` (2E, incluso il noto `test_D03_real_legacy_proofs…`), `test_d9` (2E),
`test_d9_corrections` (7E), `test_revisions` (1F+11E). 34 dei 35 blocchi di errore citano path
`/Users/luker/...` assenti nella VM; il restante (`test_R07_producer_and_consumer_real_process_crashes`,
returncode 1≠23 del subprocess) è identico sulla base. Classificazione: **ENV-BLOCKED, invariati
rispetto a `79ce7da`**, non PASS. Sul Mac la regressione di riferimento era 205/205 (con 28
metodi successor); la riesecuzione arm64 sul Mac resta a carico della review.

Le due suite si sovrappongono e non sono sommate.

**Guardian storico** (`docs/test_explanation.py`), riportato separatamente e non convertito in
PASS: 35 test, 14 failure, 0 errori, 1 skip, identico riga per riga sulla base. Log completi
(~2,5 MB) non versionati; nei log sono versionati i riepiloghi con lo SHA-256 del log completo.

## Invarianti

Prompt, schema, otto casi, ordine, `max_tokens=2560`, `enable_thinking=false` sul solo producer
122B, budget 166/200 con margine 34: invariati. Nessun push, merge o tag; nessuna pulizia di
untracked. Prossimo passo: review indipendente nella finestra `b567` (03.13-RV7), con
ripetizione delle sonde B e riesecuzione arm64 delle suite ENV-BLOCKED.
