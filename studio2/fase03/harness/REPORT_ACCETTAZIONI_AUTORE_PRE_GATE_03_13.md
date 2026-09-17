# Accettazioni dell'autore e preflight pre-gate `pilot-03` — 03.13-ACC

## Esito

**READY FOR INDEPENDENT REVIEW (author) — con gate reale BLOCCATO.** Script, test e runbook sono
pronti e verificati offline. Sul runtime reale, però, `pilot-03` non può arrivare a sonda budget
e stability gate con nessuna accettazione: il ledger contiene una **sospensione** e
`alternate_conformity` non ha PASS mentre `alternate_placement = "pilot"`. Serve una tua
decisione separata.

Esecutore `claude-opus-5` (Claude Cowork), non `gpt-5.6-sol`. Base `4ab1e2e7…`, stessa worktree.

## 1. Censimento

Letto dal codice e, in sola lettura, dal runtime `pilot-03` (ledger aperto solo come SQLite
`immutable=1`, SHA-256 invariato `38720290…`). Lo script `author_acceptances.py` lo ristampa con
lo stato corrente.

| Id | File · chiave | Formula | Verificato da | `pilot-03` |
|---|---|---|---|---|
| C01 | config · `study_model_decision`, `status` | letterali | `guards.require_execution` | ✅ |
| C02 | config · `d9.roles/status/missing_requirements` | letterali | `d9.validate_config` | ✅ |
| C03 | config · `presentation_approval{path,sha256}` | sha256 file; `ordered_labels_sha256 = sha256(canonical_json(presentation_order(d9.presentation_order)))` | `d9.validate_config` → `guards.require_presentation` | ✅ `0f9f7b7f…`, ordine `6ec43fb8…` |
| C04 | config · `execution_authorization{path,sha256}` | sha256 file; `configuration_sha256 = sha256(canonical_json(config − execution_authorization))` | `guards.require_execution` | ✅ `7dcec105…`, autore Luca |
| C05 | config · `d9.successor_lineage(+_approval)` | sha256 file | `d9.validate_config` | ✅ |
| C06 | config · `d9.services.*.documentation` | sha256 file | `d9.validate_config` | ✅ |
| C07 | config · `approved_producer_config_sha256` = `d9.producer_configs` | uguaglianza di insiemi | `d9.validate_config` | ✅ |
| C08 | config · `d9.alternate_placement` | `pilot`/`deferred` | `d9.validate_config`, `d9.validate_binding` | ✅ `pilot` (vedi L06) |
| C09 | config · `pilot_go` | — | nessun controllo nel codice | `false`, informativo |
| L01 | ledger · `stop:tokenizer_accounting[#N]` | riconciliazione REM-6 | `ledger._require_no_tokenizer_accounting_stop` | ✅ riconciliato 10:33 UTC |
| **L02** | ledger · `suspended:*` | assente | `ledger._prerequisites`, `inputs._insights` | ❌ `suspended:19a9b372…` 11:21 UTC, «response identity missing or changed» |
| L03 | ledger · request `INTENT` | 0 | `runtime.execute_request` | ✅ |
| L04 | ledger · `outcome:technical_qualification_122b` | PASS | `ledger._prerequisites` | ✅ |
| L05 | ledger · `outcome:producer_remediation` | PASS | `ledger._prerequisites('budget_probe')` | ✅ |
| **L06** | ledger · `outcome:alternate_conformity` | PASS se `placement=pilot` | `d9.validate_binding` | ❌ assente (1 COMPLETED, 5 ZERO_TOKEN_PROVEN) |
| L07 | ledger · `stages.binding_json.execution_config` | = contenuto della config | `d9.validate_binding`, `preparation.authenticate` | ✅ 4/4 stage |
| H01 | `results/validated_insight_library_…_producer_remediation.json` | = ricostruzione dai raw durevoli | `inputs._insights` | ✅ 16 insight, `c2469737…` |
| P01 | inventario congelato · `presentation.author_decision=accepted`, `COMPLETE_READY_TO_FREEZE` | = pending autenticato + provenienza handoff | `render.build_real_pilot_sample`, `preparation.authenticate` | da generare (causa del rifiuto «presentation order has not been accepted») |
| P02 | manifest eseguibile · `FROZEN_FOR_PHASE03_PRE_GATE` | = sorgenti canoniche + libreria | `preparation.authenticate` | da generare |
| P03 | `prepared/` · stato `READY_FOR_PRE_GATE_GENERATION_PROBE`, `pilot_id`, hash | `pre_gate_hashes.json` | `run_pilot.load_prepared` | da generare |
| G01 | `results/frozen_gate_config.json` | prodotto dalla sonda | `run_pilot.run_stability_stage` | non è un'accettazione |

Nessuna approvazione D9/storico aggiuntiva è richiesta: il pilot usa la lineage successor.

## 2. Script `studio2/fase03/author_acceptances.py`

`--runtime --worktree --author --evidence-root [--config --insight-handoff --model-snapshot]
[--execute --acknowledge ACCEPT_PHASE03_PRE_GATE_INPUTS]`. Senza `--execute` stampa piano,
censimento, `blocking` e SHA prima. Con `--execute`:

1. rifiuta senza scrivere se il censimento ha voci bloccanti;
2. apre il ledger come già fa `inputs.py`, `require_execution`, `verify_tokenizer`,
   `require_pilot_ledger`;
3. `inputs.build_inventory` **in-process** con la config del pilot e il contatore R4 (27B) usato da
   `authenticate`, con `presentation_approval` della config → inventario
   `execution/PILOT_INPUT_SOURCES.frozen.json` e manifest `execution/PILOT_INPUT_MANIFEST.frozen.json`;
4. `require_presentation` sull'inventario congelato;
5. `prepare_gate.prepare` in `<runtime>/prepared` (riusa la preparazione se `load_prepared` passa
   già sugli stessi input), poi `run_pilot.load_prepared`: 40 prompt;
6. record non normativo `execution/PRE_GATE_ACCEPTANCE_03_13.private.json` con autore e hash;
7. SHA prima/dopo di ogni file toccato; config, autorizzazione, approvazione e handoff devono
   restare identici. Idempotente; versioni precedenti diverse salvate come `*.pre_acceptance`.

### Deviazioni dal mandato, motivate

| Mandato | Fatto | Motivo |
|---|---|---|
| Scrivere `presentation_approval_03_13.private.json` e aggiornare la config | **Non fatto**: l'approvazione esistente `0f9f7b7f…` è verificata | già valida e legata all'ordine esatto; ogni binding durevole contiene la config intera (L07): cambiarla fa fallire `validate_binding` («configuration changed between stages») e `authenticate` («primary library was not produced under this execution configuration») |
| Rigenerare `technical_execution_authorization_03_13` | **Non fatto** | stessa ragione; l'autorizzazione copre già la config corrente |
| Rigenerare l'inventario con la CLI `inputs.py` | `build_inventory` chiamato in-process | la CLI legge `protocol.PREFLIGHT_CONFIG_PATH` e non accetta `--config`; inoltre usa il contatore 122B, mentre `authenticate` rivalida con R4 |
| Manifest in `PILOT_INPUT_SOURCES.frozen.json` | inventario lì, manifest eseguibile in `PILOT_INPUT_MANIFEST.frozen.json` | servono entrambi a `prepare` e `load_prepared` |
| `--evidence-root` non previsto | obbligatorio | `build_inventory` rilegge i 320 testi della release 03.6 |

## 3. Test `harness/test_author_acceptances.py`

Sul fixture sintetico `RunnerRevisions` con la release di evidenza reale (`FOT_HARNESS_TEST_EVIDENCE`):

| Test | Verifica |
|---|---|
| ACC00 | senza script l'inventario pending riproduce «presentation order has not been accepted by the author» |
| ACC01 | dopo lo script sonda budget (3 chiamate stub) e stability (120) passano; config invariata |
| ACC02 | solo piano: nessun file scritto, censimento completo |
| ACC03 | idempotenza byte-identica; dump del ledger invariato |
| ACC04 | approvazione presentazione, autorizzazione, inventario, manifest, plan manomessi → il gate rifiuta, 0 chiamate |
| ACC05 | pilot sospeso → rifiuto prima di ogni scrittura, ledger invariato |
| ACC06 | `placement=pilot` senza PASS → bloccante |
| ACC07 | config riscritta → L07 bloccante |
| ACC08 | acknowledgement errato e worktree diversa rifiutati |

9/9 PASS. Suite a 16 moduli nella VM: tutti PASS tranne 2 non-pass ambientali (percorso Mac
assente), stessa causa della base. Guardian invariato (14 failure). Dettaglio:
`logs_accettazioni_autore_pre_gate_03_13/verification.log`.

## 4. Runbook

`studio2/fase03/RUNBOOK_PRE_GATE_PILOT_03.md`: evidenza, piano, esecuzione, `prepare_gate`
facoltativo, budget, stability, tabella dei rifiuti.

## Rischi e limiti

- La config punta all'approvazione nella worktree `dd86` (`/Users/luker/.codex/worktrees/dd86/…`),
  che Git segna come *prunable* dalla VM. Se viene potata, ogni `require_execution` fallisce e la
  config non può essere ripuntata. Esiste una copia identica nel runtime.
- Lo script non è stato eseguito sul runtime reale: i percorsi `/Users/...` non sono risolvibili
  nella VM e comunque L02/L06 bloccano.
- Nessun file del runtime scritto; nessuna chiamata; nessun push, merge o tag.

**READY FOR INDEPENDENT REVIEW (author)**
