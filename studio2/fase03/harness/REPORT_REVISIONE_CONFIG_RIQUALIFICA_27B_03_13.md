# Revisione approvata della config, riqualifica 27B e ripresa alternate `pilot-03` — 03.13-REV27B

## Esito

**READY FOR INDEPENDENT REVIEW (author).** Codice, test e runbook sono pronti e verificati
offline. Il ledger reale non è stato toccato; lo aprono gli script dal terminale di Luca.

Esecutore `claude-opus-5` (Claude Cowork), non `gpt-5.6-sol`. Base `3952fb4…`, stessa worktree.

## Fatti verificati sul ledger reale (sola lettura, SHA `38720290…` invariato)

- `19a9b372…` (`agent_1`, `alternate_conformity`) è `COMPLETED`, con `identity_valid=false`:
  `model=fot-exp2-consumer`, `system_fingerprint=vllm-0.28.0-5fc21ed4` contro un atteso `null`,
  `finish_reason=length`, 2047 token di reasoning su 2560.
- **Correzione ai fatti del prompt: la request è già un retry transport** (6° tentativo di
  `agent_1`: una base e quattro transport `ZERO_TOKEN_PROVEN`, poi questa). La riserva condivisa
  è piena: remediation 8 + transport 7 = 15/15, e oltre 7 transport serve un waiver.
- Consumo: 25 request native + 5 di lineage = 30. I 4 binding hanno `execution_config` uguale
  alla config `0c3cd34e…`.

## Decisioni dell'autore acquisite in sessione

1. Il resend di `agent_1` va su una **nuova quota `requalification`**: massimo 1, solo per una
   request con sospensione riconciliata. Conta nel cumulativo e nel limite di 200; il massimo
   pianificato passa da 166 a **167/200**; la formula 8r+t≤15 non cambia.
2. **Documentazione del servizio 27B in rev2** (file nuovo, cambia solo il fingerprint; il
   vecchio resta intatto). `d9.services['27B'].documentation` è tra le chiavi ammesse della
   revisione, così servizio, provider e documentazione dicono la stessa cosa.

## Nota per i metodi (deroga singola)

> Durante il pilot il runtime del produttore alternativo (Qwen3.8-27B-FP8, vLLM 0.28.0) ha
> iniziato a restituire un `system_fingerprint` (`vllm-0.28.0-5fc21ed4`) dove la configurazione
> congelata ne prevedeva l'assenza. Il primo caso dello stage (`agent_1`) è stato quindi
> invalidato per identità e il pilot sospeso. Con una revisione della configurazione approvata
> dall'autore e registrata nel ledger, il fingerprint osservato è stato riqualificato e il
> produttore 27B è stato impostato con `enable_thinking=false` (budget di output invariato,
> 2560); il caso sospeso è stato reinviato una sola volta su una quota dedicata
> (`requalification`, massimo 1). Questa è l'unica deroga al massimo pianificato, che sale di
> una request (167/200); la riserva condivisa 8r+t≤15 resta invariata. La risposta invalidata
> resta nel ledger con `identity_valid=false`.

## Implementazione

### Ledger (`harness/ledger.py`)

| Proprietà | Meccanismo |
|---|---|
| 1. Revisione approvata | `record_config_revision(previous_config_path, new_config_path, approval_path)` → `config_revision:<n>`, con config precedente e nuova (SHA dei file, digest e contenuto), chiavi cambiate e approvazione incorporata `{decision, author, previous_sha256, new_sha256, reason}` (byte UTF-8 ri-hashati a ogni uso). Chiavi ammesse: `d9.producer_configs.27B`, `d9.services.27B.expected_response.system_fingerprint`, `d9.services.27B.documentation`, `approved_producer_config_sha256` (deve restare uguale a `producer_configs`), `execution_authorization`. La catena parte dalla config di tutti i binding e ogni revisione parte dalla testa |
| Binding | `_require_accepted_config`: una config salvata è valida se, senza revisioni, è uguale alla corrente; altrimenti se appartiene alla catena. `require_pilot_ledger` esige che la config corrente sia la testa. Le request già eseguite restano legate alla loro revisione |
| 2. Sospensione | `reconcile_suspension(request_id, approval_path)` → `suspension_reconciled:<id>`. Solo per `reason='response identity missing or changed'`; nessuna request `INTENT` e nessuna request successiva alla sospensione; identità osservata = raw = record; accettata da `expected_response` della revisione indicata. L'evento `suspended:` e il record restano. `_prerequisites` e `inputs._insights` ignorano solo sospensioni riconciliate e ri-autenticate |
| 3. Ripresa | Il binding dell'alternate è immutabile, ma i provider e la config nuovi ne cambiano il digest: `_rebind_stage` registra `stage_rebinding:alternate_conformity:<n>` (binding precedente intero) solo se cambiano `execution_config` (revisione → testa) e il provider (`extra_body` no-thinking esatto, fingerprint, rimozione di `thinking_token_budget`, hash pinnato). Nessun outcome e nessuna `INTENT` ammessi. Le request precedenti restano valide sul loro `stage_run` |
| Requalification | `reserve_requalification_retry` / `runtime.execute_request` con `--resume --retry-request <id>` su un leaf `COMPLETED`: `retry_of` → parent sospeso e riconciliato, stesso stage e stessa identità, un solo figlio, **1 in tutto il ledger**. `_chain_leaves` e `_validate_attempts` accettano la catena `base → … → completed sospeso → requalification`; l'outcome PASS si calcola sulle leaf. `snapshot()` espone `requalification_calls` e il massimo pianificato +1 |

### Altro codice

- `d9.producer_extra_body`: il 27B accetta **solo** `chat_template_kwargs.enable_thinking=false`
  esatto. Il vecchio test che lo vietava (`ProducerRenderingAndAccountingTests`) è stato
  aggiornato secondo la decisione A.
- `d9.validate_binding`, `d9.swap_manifest`, `preparation.authenticate`: da uguaglianza ad
  appartenenza alla catena. `guards.require_pilot_ledger`: la config dev'essere la testa.
- `author_acceptances.py` (censimento): L02 ignora le sospensioni riconciliate, L07 accetta la
  catena. Il ledger è letto con `immutable=1` solo quando non c'è WAL.
- `revise_pilot_config.py` (`--runtime --author [--reason --fingerprint --suspended-request
  --evidence-root] --execute --acknowledge REVISE_PHASE03_PILOT_CONFIG`): calcola tutto in modo
  deterministico e rifiuta prima di scrivere. Poi scrive i file `.rev2`, il backup `.pre_rev2`,
  la config (temp + rename), registra revisione e riconciliazione, ed esegue il preflight
  (`require_execution`, `validate_provider` rev2, `require_pilot_ledger`, `binding()` di ogni
  stage, nessuna sospensione aperta, piano di `author_acceptances`). Idempotente.

### Deviazioni dal prompt

| Prompt | Fatto | Motivo |
|---|---|---|
| Resend «addebitato» come `retry_of` transport | quota `requalification` | riserva piena (15/15); decisione dell'autore |
| Modifiche solo a producer_configs, fingerprint, authorization | + `services.27B.documentation` e `approved_producer_config_sha256` | `validate_config` confronta documentazione e allowlist; decisione dell'autore per la prima |
| «rigenera technical_execution_authorization» | nuovo file `…authorization_03_13.rev2.private.json` | sovrascriverlo invaliderebbe la config precedente, che i binding storici rivalidano |
| Provider rev2 «copia con enable_thinking e fingerprint» | rimosso anche `thinking_token_budget` (2048) | con il thinking spento non ha effetto, e `producer_probe` rifiuta di unire due `extra_body`; il 122B è configurato allo stesso modo |
| «nuova revisione nel binding» | evento di rebinding con il binding precedente incorporato | il binding è immutabile e le request esistenti ne portano il digest |

## Test (`harness/test_config_revision.py`)

Fixture `RunnerRevisions` che riproduce lo stato reale: alternate in pilot, `agent_1` con
fingerprint cambiato, pilot sospeso (REV0).

| Test | Proprietà |
|---|---|
| REV1 | piano senza scritture; acknowledgement errato rifiutato |
| REV2 | revisione → resume → alternate PASS sulle leaf (8/8 validi, record sospeso ancora invalido), +8 native, 1 requalification, reserve 0, massimo +1, poi `author_acceptances`, sonda e gate (123 chiamate stub) |
| REV3 (a) | config mutata fuori dalle chiavi ammesse → rifiuto (4 casi) |
| REV4 (b) | binding precedenti accettati con la revisione; config non registrata o superata → rifiuto |
| REV5 (c) | identità non accettata → nessuna scrittura; request successiva alla sospensione → rifiuto |
| REV6 (d) | senza revisione o senza `--retry-request` nessun invio; con → requalification; secondo resend rifiutato; `stage_run` superato rifiutato |
| REV7 (g) | idempotenza byte-identica di file e ledger |
| REV8 | revisione o riconciliazione manomessa → blocco |
| REV9–10 | rebinding limitato al cambio 27B approvato (max_tokens, thinking on, modello, template, config superata, stage diverso) |
| (e), (f) | coperti in REV2 |

RED: sulla base `3952fb4` REV0 passa (la fixture riproduce il blocco), gli altri 10 test
falliscono con 13 errori (API assenti).

## Verifiche

VM Linux con Python 3.10 e release di evidenza `evidence-v2` scaricata e verificata.

| Verifica | Esito |
|---|---|
| `test_config_revision` | 11/11 PASS |
| Suite a 17 moduli (i 15 storici + `test_author_acceptances` + `test_config_revision`) | tutti PASS salvo 2 non-pass ambientali (percorso Mac assente), come sulla base |
| Guardian | 35 test, 14 failure, 1 skip: invariato |
| Ledger reale | SHA `38720290…` invariato; nessun file del runtime scritto |

Il GREEN completo va rieseguito sul Mac (`/opt/anaconda3/bin/python3`) in review.

**READY FOR INDEPENDENT REVIEW (author)**
