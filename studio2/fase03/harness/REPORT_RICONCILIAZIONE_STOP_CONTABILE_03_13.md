# Riconciliazione dello STOP contabile spurio su `pilot-03` — 03.13-REM-6

## Esito

**READY FOR INDEPENDENT REVIEW (author).** Parte **codice** completata offline, test-first,
sopra il fix accettato `82a41797c5b07dbd81a0e568dc399b45c98ff92f`. La parte **applicazione al
ledger reale** non è stata eseguita: richiede review OK e disposizione di Luca.

Esecutore: `claude-opus-5` (Claude Cowork), non `gpt-5.6-sol` come indicato nel prompt.
Finestra: la worktree `dd86` (`/Users/luker/.codex/worktrees/dd86/fot-tep`) non è
raggiungibile da questa sessione; il lavoro è su una worktree nuova
`/Users/luker/fot-tep/.worktrees/rem6-riconciliazione`, branch
`codex/studio2-riconciliazione-stop-contabile`, creata da `82a41797`.

## Stato di partenza

Il ledger `pilot-03` (`/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03/ledger.sqlite3`,
SHA-256 atteso `3690ccfac8a0807d20f1be581325748f392ed777a206ee7c2e8954106df19779`) contiene
`stop:tokenizer_accounting`, request T9 `agent_1`
`e6019d34669737981fec3174173a92c160df3e192924880226bfc7952a50bb67`, artifact
`d02464d2937cc7d5f31038b40478bfe0b547112c277371da5c1b2d3b37dbc54a`, prodotto dal difetto di
scoping corretto in `82a41797`. Prima di questa modifica nessun percorso poteva sbloccarlo.

## Codice

### `PilotLedger.reconcile_accounting_stop(*, approval_path, fixed_commit, guard)`

In una sola transazione `BEGIN IMMEDIATE`:

1. richiede `stop:tokenizer_accounting` presente; se esiste già
   `stop_reconciled:tokenizer_accounting` con gli stessi byte di approval e lo stesso
   `fixed_commit` restituisce `ALREADY_RECONCILED` senza scrivere, altrimenti rifiuta;
2. l'inventario degli STOP deve essere esattamente `[stop:tokenizer_accounting]`;
3. approval JSON con chiavi **esattamente** `decision="accepted"`, `author` non vuoto,
   `stop_artifact_sha256` = artifact dello STOP, `stop_request_id` = request dello STOP,
   `cause="harness_defect"`, `fixed_commit` = argomento (40 hex), `ledger_sha256_before`;
4. `ledger_sha256_before` deve coincidere con lo SHA-256 del file ledger, con `-wal` assente o
   vuoto (stato checkpointed);
5. nessuna request `INTENT` e nessuna request con `intent_utc` successivo allo STOP;
6. rivalida **tutti** gli eventi `tokenizer_accounting:*` con il validatore corretto e i soli
   messaggi persistiti (nessun `expected_stage`/`expected_messages`); qualsiasi errore rifiuta
   senza scrivere; l'evento contabile della request dello STOP deve risultare tra i validati;
7. scrive un solo evento `stop_reconciled:tokenizer_accounting`, `artifact_sha256` = artifact
   dello STOP, con `stop_event`, `stop_request_id`, `stop_created_utc`, `stop_reason`,
   `fixed_commit`, elenco degli eventi rivalidati e `approval = {path, sha256, content, utf8}`
   (stesso schema durevole di `diagnosis:`). Lo STOP resta nel ledger.

### Blocco (`_tokenizer_accounting_stop` / `_require_no_tokenizer_accounting_stop`)

Uno STOP originale è ignorato solo se esiste l'evento di riconciliazione e questo si
ri-autentica a ogni uso: byte UTF-8 incorporati ri-hashati, JSON uguale al contenuto
incorporato, artifact e request uguali allo STOP, approval ancora valido. Un evento di
riconciliazione corrotto o senza STOP originale produce `FATAL_ACCOUNTING_ERROR` e blocca.

### Deviazioni dal prompt, dichiarate

| Deviazione | Motivo |
|---|---|
| Argomento aggiuntivo obbligatorio `guard` | la rivalidazione con `validate_tokenizer_accounting_evidence` ricalcola i token localmente e richiede il tokenizer congelato |
| Rivalidazione tramite `_revalidate_accounting_events`, estratto senza cambi di comportamento dal corpo di `validate_tokenizer_accounting_evidence` | il metodo pubblico si arresta sullo STOP esistente e scrive STOP; la riconciliazione deve rivalidare sotto STOP e rifiutare senza scrivere |
| `_persist_accounting_stop` scrive gli STOP successivi come `stop:tokenizer_accounting#N` | l'evento `stop:tokenizer_accounting` è create-once: senza questo un nuovo errore dopo la riconciliazione non lascerebbe uno STOP durevole (test e). Gli STOP `#N` non sono riconciliabili da questo codice |
| CLI con `--fixed-commit`, `--provider-config`, `--model-snapshot` obbligatori; senza `--execute` stampa solo il piano; rifiuta ledger inesistente | servono a costruire il guard con `verify_tokenizer` sugli hash del provider config e a non creare un ledger nuovo per errore |

Script: `studio2/fase03/reconcile_accounting_stop.py`, acknowledgement
`RECONCILE_PHASE03_ACCOUNTING_STOP`.

## Test (red/green)

Nuova classe `AccountingStopReconciliationTests` in `test_successor_recovery.py` (modulo già
nella suite a 15), più un test CLI in `EntrypointFailClosedTests`. Lo STOP è prodotto come nel
caso reale: mismatch di messaggi nello stesso stage su un evento contabile valido.

| Caso | Test |
|---|---|
| (a) STOP spurio + eventi validi + approval → riconciliato; lo STOP resta; l'approval sopravvive alla cancellazione del file; `validate_tokenizer_accounting_evidence` e nuove request ammesse | `test_REM6_a_…` |
| (b) evento contabile realmente manomesso → rifiuto, nessuna scrittura, blocco invariato | `test_REM6_b_…` |
| (c) request creata dopo lo STOP / `INTENT` aperta → rifiuto | `test_REM6_c_…` (2) |
| (d) hash STOP, request, causa, decisione, autore, commit, stato ledger, chiave extra o `fixed_commit` argomento diversi → rifiuto; STOP assente → rifiuto | `test_REM6_d_…` (2, 8 subtest) |
| (e) nuovo STOP dopo la riconciliazione → `#2`, blocca request e rivalidazione, non riconciliabile; evento di riconciliazione corrotto → blocca | `test_REM6_e_…` (2) |
| (f) idempotenza byte-identica; approval diverso rifiutato; un solo evento | `test_REM6_f_…` |
| (g) request, response, receipt, stage, eventi e snapshot quota invariati salvo il nuovo evento | `test_REM6_g_…` |
| CLI: senza `--execute` solo piano; ack errato rifiutato; ledger inesistente rifiutato e non creato | `test_REM6_reconcile_cli_…` |

## Verifiche

Ambiente: VM Linux della sessione, Python 3.10.12 (non l'interprete Mac 3.13.9 del log
precedente), `jsonschema` 4.26.0 installato nell'utente per i test.

| Verifica | Risultato osservato |
|---|---|
| RED sul codice `82a41797` | 10 test, 18 errori attesi (`reconcile_accounting_stop` assente), 0,315 s |
| GREEN `test_successor_recovery` | 50/50 PASS in 6,712 s |
| 15 moduli, candidato vs base `82a41797` nella stessa VM | 216 test candidato / 205 base; 35 non-pass in entrambi, **insieme identico** |
| Guardian `docs/test_explanation.py` | 35 test, 14 failure, 1 skip: baseline invariata |
| `py_compile`, `git diff --check` | PASS |

I 35 non-pass sono ambientali: dipendono da percorsi presenti solo sul Mac
(`/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec`,
`/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec`). **La review deve rieseguire la suite a
15 moduli con `/opt/anaconda3/bin/python3` sul Mac** per il GREEN completo. Dettaglio in
`logs_riconciliazione_stop_contabile_03_13/verification.log`.

## Stato runtime e limiti

Il ledger reale `pilot-03` non è stato aperto, copiato né misurato: sta fuori dalla cartella
collegata a questa sessione. Nessuna rete verso provider, nessuna request, retry, resume,
remediation, push, merge o tag.

## Per la fase di applicazione (dopo review OK e disposizione)

1. verificare SHA-256 del ledger reale (`3690ccfa…`) con nessun processo aperto e `-wal` assente;
2. scrivere l'approval con `stop_artifact_sha256`
   `d02464d2937cc7d5f31038b40478bfe0b547112c277371da5c1b2d3b37dbc54a`, `stop_request_id`
   `e6019d34…bb67`, `cause="harness_defect"`, `fixed_commit` = commit accettato,
   `ledger_sha256_before` = hash del punto 1;
3. eseguire lo script prima senza `--execute`, poi con `--execute --acknowledge
   RECONCILE_PHASE03_ACCOUNTING_STOP`, con provider config
   `04b2c948c586c9ae4e38d9d0c50d36aad86a5b609a609d94c2d31fde7c2a8bf0` e snapshot 122B congelato;
4. atteso: `RECONCILED`, 9 eventi contabili rivalidati, request/quote invariate (14/166/200).

La worktree è stata creata dalla VM: il suo file `.git` punta a un percorso della VM. Sul Mac
serve `git worktree repair /Users/luker/fot-tep/.worktrees/rem6-riconciliazione` prima di usarla.

**READY FOR INDEPENDENT REVIEW (author)**
