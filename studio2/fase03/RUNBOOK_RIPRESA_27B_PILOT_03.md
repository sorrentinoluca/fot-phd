# Runbook ripresa 27B `pilot-03` — revisione config, alternate, sonda e gate

Comandi da lanciare dal terminale del Mac, nell'ordine. Solo i passi 3, 5 e 6 chiamano un modello.

```bash
export PY=/opt/anaconda3/bin/python3
export WT=/Users/luker/fot-tep/.worktrees/rem6-riconciliazione
export RT=/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03
export CFG=$RT/execution/pilot_d9_successor_candidate_03_13.private.json
export LEDGER=$RT/ledger.sqlite3
export PILOT=studio2-fase03-d9-pilot-03
export SUSP=19a9b37269bede1b62799cf3ac5819557dc19a5273aa53099f04b202bb94b207
export EVD=/Users/luker/fot-tep-runtime/evidence-v2/studio2/fase03/evidence/output
cd "$WT"
```

Stato di partenza atteso: ledger `38720290…`, config `0c3cd34e…`, nessun processo che tenga aperto
il ledger (`lsof $LEDGER` vuoto).

## 1. Piano della revisione (nessuna scrittura)

```bash
$PY studio2/fase03/revise_pilot_config.py --author Luca
```

Atteso: `"status": "PLAN_ONLY"`. `changed_keys` deve essere esattamente:

```text
approved_producer_config_sha256
d9.producer_configs.27B
d9.services.27B.documentation
d9.services.27B.expected_response.system_fingerprint
execution_authorization
```

`observed_identity` = `fot-exp2-consumer` / `vllm-0.28.0-5fc21ed4`.

## 2. Revisione, riqualifica 27B e riconciliazione della sospensione

```bash
$PY studio2/fase03/revise_pilot_config.py --author Luca --evidence-root $EVD \
  --execute --acknowledge REVISE_PHASE03_PILOT_CONFIG
```

Atteso: `"status": "REVISED"`, `revision.status = RECORDED`, `suspension.status = RECONCILED`,
`snapshot.planned_maximum_with_alternate = 167`, `author_acceptances_blocking = ["L06_alternate_pass"]`.

File nuovi in `$RT/execution/` (gli originali restano identici):

- `producer_27b_successor_03_13.rev2.private.json` — `extra_body.chat_template_kwargs.enable_thinking=false`, fingerprint, `max_tokens=2560`, senza `thinking_token_budget`;
- `service_27b_successor_03_13.rev2.private.json` — solo il fingerprint cambiato;
- `technical_execution_authorization_03_13.rev2.private.json` — sul nuovo hash di config;
- `config_revision_01_03_13.private.json`, `suspension_reconciliation_03_13.private.json` — le tue approvazioni;
- `pilot_d9_successor_candidate_03_13.private.json.pre_rev2` — byte precedenti della config.

La config viene sostituita (temp + rename). Nel ledger: `config_revision:1` e
`suspension_reconciled:19a9b372…`. Rilanciarlo è idempotente (`UNCHANGED`, `ALREADY_…`).

## 3. Ripresa dell'alternate 27B (8 chiamate: 1 requalification + 7 base)

Tunnel verso il 27B su `127.0.0.1:18001` aperto come nei run precedenti.

```bash
$PY studio2/fase03/producer_probe.py --config $CFG \
  --source-inventory studio2/fase03/harness/PILOT_INPUT_SOURCES.pending.json \
  --results-dir $RT/results \
  --provider-config $RT/execution/producer_27b_successor_03_13.rev2.private.json \
  --model-snapshot $RT/tokenizers/27B/017b9c7af6b5689d5dd426a76e0bc077eb5ca20a \
  --stage alternate_conformity --ledger $LEDGER --pilot-id $PILOT \
  --resume --retry-request $SUSP \
  --execute --acknowledge EXECUTE_PHASE03_PRODUCER_CONFORMANCE
```

Atteso: il primo bind registra `stage_rebinding:alternate_conformity:1`; `agent_1` viene
reinviato come `quota_kind=requalification`, `retry_of=19a9b372…`; `agent_2`–`agent_8` come base;
summary `PASS` e `results/validated_insight_library_qwen_27b_alternate_alternate_conformity.json`.
Consumo nativo 25 → 33.

Se l'alternate chiude `FAIL` (per esempio JSON troncato o identificatori), l'esito è definitivo:
budget e gate restano bloccati e serve una nuova decisione.

## 4. Accettazioni e preflight pre-gate

```bash
$PY studio2/fase03/author_acceptances.py --runtime $RT --worktree $WT --author Luca --evidence-root $EVD \
  --execute --acknowledge ACCEPT_PHASE03_PRE_GATE_INPUTS
```

Atteso: `READY_FOR_PRE_GATE_GENERATION_PROBE`, 40 prompt, `blocking = []`.

## 5. Sonda budget (122B)

```bash
export STUDIO2_CONSUMER_API_KEY=...
$PY studio2/fase03/run_pilot.py --config $CFG --prepared-dir $RT/prepared --results-dir $RT/results \
  --ledger $LEDGER --pilot-id $PILOT --stage budget --execute --acknowledge EXECUTE_PHASE03_PRELIMINARY_PILOT
```

Atteso: `FROZEN_FOR_STABILITY_GATE` (al massimo 9 chiamate).

## 6. Stability gate (120 chiamate)

```bash
$PY studio2/fase03/run_pilot.py --config $CFG --prepared-dir $RT/prepared --results-dir $RT/results \
  --ledger $LEDGER --pilot-id $PILOT --stage stability --execute --acknowledge EXECUTE_PHASE03_PRELIMINARY_PILOT
```

Consumo finale massimo: 162 native + 5 lineage = 167/200.

## Se qualcosa rifiuta

| Messaggio | Causa | Cosa fare |
|---|---|---|
| `config revision changes keys outside the approved set` | la config di partenza non è `0c3cd34e…` o è stata modificata a mano | ripristinare i byte `0c3cd34e…` (o `.pre_rev2`) e rilanciare il passo 2 |
| `refusing to overwrite a different existing file` | un file `.rev2` esiste con contenuto diverso | non cancellarlo: confrontarlo e decidere; lo script non sovrascrive |
| `a request was created after the suspension` | nuovi invii dopo il 2026-09-17 11:21 UTC | fermarsi: la riconciliazione non è più ammessa |
| `observed identity is not accepted` | fingerprint diverso da `vllm-0.28.0-5fc21ed4` | verificare il raw e rilanciare con `--fingerprint` corretto (nuova decisione) |
| `pilot suspended; requires a new reviewed disposition` | passo 2 non eseguito, oppure una **nuova** sospensione | per una nuova sospensione serve una nuova decisione (la quota requalification è 1) |
| `requalification quota is exhausted` / `already has a retry` | secondo resend | non ammesso |
| `stage rebinding provider change is outside the approved 27B requalification` | provider diverso dal `.rev2` | usare esattamente il file `.rev2` |
| `existing stage requires explicit --resume` / `pilot suspended by persisted response identity mismatch` | manca `--resume` o `--retry-request $SUSP` | rilanciare il passo 3 com'è scritto |
| `FATAL: config revision chain is corrupted` / `suspension reconciliation is corrupted` | eventi alterati | fermarsi: nessun invio è possibile |
| `presentation order has not been accepted` / `alternate_conformity has no successful closed outcome` | passo 4 non eseguito / passo 3 non PASS | vedere `RUNBOOK_PRE_GATE_PILOT_03.md` |
