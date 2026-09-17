# Correzione 03.13-REV27B-FIX — soli rilievi E20 ed E4

## Esito

**READY FOR INDEPENDENT REVIEW.** E20 ed E4 sono corretti con due guardie circoscritte e due
test discriminanti. E26 è dichiarato come limite noto e non è stato corretto. Nessuna rete,
provider call, tunnel o apertura del ledger reale.

## Provenienza

- candidato respinto: `20ecfd8f6c6ffb9816d1ec25dd3a48e2c6667959`;
- tree candidato respinto: `8b44bd52defebf7b5d11e9d139a06f7fa60c8e47`;
- parent: `3952fb4408281f0c4181f3741617419e6ae2085f`;
- verbale indipendente:
  `/Users/luker/.codex/worktrees/b567/fot-tep/studio2/fase03/harness/VERIFICA_REVISIONE_CONFIG_RIQUALIFICA_27B_03_13.md`;
- SHA-256 verbale:
  `70faa3a0f7dd7acda459bfe7e723d7f686ef3e443ebd7685a3b3adb44ec27f99`.

La worktree era pulita. Il solo intervento infrastrutturale preliminare è stato l'aggiornamento
dei due puntatori Git locali rimasti sul precedente mount `/sessions/...`; nessun byte versionato
è stato modificato da tale riparazione.

## Guardia E20 — selettore retry

`runtime.retry_requests_by_logical_id` autentica ogni ID esplicito prima di qualsiasi intent:
la request deve esistere e appartenere allo stage corrente. `execute_request` richiede inoltre
che la selezione ricevuta appartenga al `logical_id` in esecuzione.

I due runner validano il vettore completo prima della prima scrittura possibile e lo instradano
per identità logica:

- `producer_probe.run` valida prima di `bind_stage` e passa a ogni chiamata solo gli ID del suo
  `logical_id`;
- `run_pilot._probe_retry` usa la stessa guardia; `run_budget_stage` la esegue prima del bind e
  conserva la prenotazione atomica della tripla.

Le guardie durevoli preesistenti restano invariate: `_insert_intent` continua a verificare che il
parent del transport retry abbia stesso stage, identità completa e prova zero-token; la
remediation base non riceve alcun `retry_of`. Un ID cross-stage o inesistente viene ora respinto
con `HarnessError`, senza binding, intent, quota, journal o transport.

## Guardia E4 — bind sulla testa corrente

`PilotLedger.bind_stage` passa l'`execution_config` proposta a `_require_accepted_config` anche
come config corrente. Se esiste una catena di `config_revision`, solo la testa può essere
persistita da un nuovo bind o rebinding.

Il percorso di sola rilettura non cambia: `_binding`/`validate_binding` continuano ad accettare
gli stage storici salvati con una revisione precedente autenticata nella catena. La correzione
separa quindi la mutazione corrente dalla validazione della storia.

## Due test finali e RED/GREEN

Entrambi i test sono in `harness/test_config_revision.py`:

1. `test_FIX_E20_retry_selector_must_match_stage_and_logical_id` prova ID cross-stage, ID
   inesistente, assenza di scritture/quota/journal/transport e il retry corretto positivo;
2. `test_FIX_E4_bind_requires_current_revision_but_saved_stage_accepts_old` prova rifiuto C0
   dopo C1 senza scritture, rilettura valida dello stage storico C0 e bind/rebinding C1 positivo.

Gli stessi byte finali dei test sono stati eseguiti in un `git archive` isolato del commit
`20ecfd8` e sui byte corretti:

| Esecuzione | Risultato |
|---|---|
| RED `20ecfd8` | 2 test, 2 failure, 0 errori, 1,420 s |
| GREEN correzione | 2/2 PASS, 2,143 s |

Nel RED E20 raggiunge il rifiuto storico per identità sospesa invece della nuova guardia e E4 non
solleva alcun errore; le cause coincidono con il verbale indipendente.

## E26 — limite noto, nessuna correzione

Il rename della config e l'evento SQLite `config_revision:<n>` non sono una transazione atomica
cross-filesystem. Questo delta non modifica il protocollo. Il runbook dichiara che un'interruzione
fra i due passi rende lo stato operativamente non utilizzabile: non si avviano alternate, probe o
gate e si rilancia identico lo script, che completa idempotentemente revisione, riconciliazione e
preflight. La prosecuzione è ammessa solo dopo stato `RECORDED`/`ALREADY_RECORDED` e
`RECONCILED`/`ALREADY_RECONCILED`.

Questa è una mitigazione operativa documentata, non una nuova garanzia di atomicità fra filesystem
e ledger.

## Verifiche

| Verifica | Risultato |
|---|---|
| Nuovi test E20/E4 | 2/2 PASS |
| `test_config_revision` + `test_author_acceptances` + `test_successor_recovery` | 72/72 PASS in 95,835 s |
| Guardian `docs/test_explanation.py` | NON PASS storico: 35 test, 14 failure, 1 skip, 0 errori in 0,076 s |
| Rete/provider/runtime reale | non usati |

Il guardian è riportato separatamente e non è riclassificato come PASS.

## SHA-256 dei file toccati, escluso questo report

| File | SHA-256 |
|---|---|
| `studio2/fase03/harness/ledger.py` | `65f5162dfe29a3352b1f50659c2dd24a71b590700d7d959653ed672cbe76fa40` |
| `studio2/fase03/harness/runtime.py` | `d30ad9ed300f7d5724ccc16926e919e24dc40e9bbddf653627138e727ebd9deb` |
| `studio2/fase03/producer_probe.py` | `b353728e425b77772de866cdfba74948889b6d2eceef05fa77d8ec90aa72fbd1` |
| `studio2/fase03/run_pilot.py` | `bf1632e6edae97ebd72a12c7407d454714daca41c9742c6f53eee743b9ff02e7` |
| `studio2/fase03/harness/test_config_revision.py` | `43f3a0381894330391ae3b7411ce7255a355d243a43fd9ca8ad3f2c71b7051d0` |
| `studio2/fase03/RUNBOOK_RIPRESA_27B_PILOT_03.md` | `289d2e8bc091c338284554f569f57bcfb62e22e016038b6c3122c56ea3119125` |

Il SHA di questo report viene calcolato e dichiarato dopo la chiusura dei suoi byte.
