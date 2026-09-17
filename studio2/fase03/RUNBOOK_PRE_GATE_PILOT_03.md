# Runbook pre-gate `pilot-03` — sonda budget e stability gate

Comandi da lanciare dal terminale del Mac, in quest'ordine. Nessun comando qui sotto chiama il
modello tranne i passi 5 e 6. Interprete: `/opt/anaconda3/bin/python3` (serve `transformers` per i
passi 3–4, `openai` per i passi 5–6).

```bash
export PY=/opt/anaconda3/bin/python3
export WT=/Users/luker/fot-tep/.worktrees/rem6-riconciliazione
export RT=/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03
export CFG=$RT/execution/pilot_d9_successor_candidate_03_13.private.json
export LEDGER=$RT/ledger.sqlite3
export PILOT=studio2-fase03-d9-pilot-03
export EVD=/Users/luker/fot-tep-runtime/evidence-v2/studio2/fase03/evidence/output
cd "$WT"
```

## ⚠️ Stato al 2026-09-17 13:41 (Europe/Rome): il gate è bloccato

Il censimento di sola lettura del ledger (SHA-256
`3872029001346913f3722928b350813c8daaef349c5d4fbe98b770200c893fa0`) trova due condizioni che
**nessuna accettazione può sbloccare**:

| Controllo | Stato | Perché blocca |
|---|---|---|
| `L02_not_suspended` | `suspended:19a9b372…` del 2026-09-17 11:21 UTC, «response identity missing or changed» (run 27B alternate `alternate_20260917T131826.log`) | `ledger._prerequisites` rifiuta ogni stage e `inputs._insights` rifiuta l'handoff: «pilot suspended; requires a new reviewed disposition». Non esiste codice che la chiuda |
| `L06_alternate_pass` | `alternate_conformity` senza outcome (1 COMPLETED, 5 ZERO_TOKEN_PROVEN) | `d9.alternate_placement = "pilot"`: `d9.validate_binding` esige `alternate_conformity` PASS prima di `budget_probe` e `stability_gate` |

Serve una tua decisione separata (per esempio una remediation durevole della sospensione, sul
modello di REM-6, oppure un nuovo pilot successore). Finché il passo 2 riporta `blocking` non
vuoto, i passi 3–6 falliscono.

Tutto il resto è già soddisfatto: config `0c3cd34e…` con `execution_authorization` valida,
approvazione dell'ordine di presentazione `0f9f7b7f…` legata a `ordered_labels_sha256`
`6ec43fb8…`, STOP contabile riconciliato, remediation 122B PASS, binding uguali alla config,
handoff `producer_remediation` presente.

## 1. Evidenza 03.6 (una volta)

```bash
mkdir -p /Users/luker/fot-tep-runtime/evidence-v2 && cd /Users/luker/fot-tep-runtime/evidence-v2
curl -L -o ev2.tar https://github.com/sorrentinoluca/fot-tep-data/releases/download/studio2-fase03-evidence-v2/studio2-fase03-evidence-v2.tar
shasum -a 256 ev2.tar   # atteso 6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf
tar xf ev2.tar && cd "$WT"
```

## 2. Piano e censimento (sola lettura)

```bash
$PY studio2/fase03/author_acceptances.py --runtime $RT --worktree $WT --author Luca --evidence-root $EVD
```

Atteso: `"status": "PLAN_ONLY"`, exit 0. Leggere `"blocking"`: deve essere `[]` per proseguire.
Il censimento completo (`census`) elenca per ogni controllo file, chiave, formula dell'hash e
modulo che lo verifica.

## 3. Accettazioni e preflight (una decisione)

```bash
$PY studio2/fase03/author_acceptances.py --runtime $RT --worktree $WT --author Luca --evidence-root $EVD \
  --execute --acknowledge ACCEPT_PHASE03_PRE_GATE_INPUTS
```

Atteso: `"status": "READY_FOR_PRE_GATE_GENERATION_PROBE"`, `"prompt_count": 40`, exit 0. Scrive
soltanto:

- `$RT/execution/PILOT_INPUT_SOURCES.frozen.json` (inventario, `author_decision=accepted`);
- `$RT/execution/PILOT_INPUT_MANIFEST.frozen.json` (manifest `FROZEN_FOR_PHASE03_PRE_GATE`);
- `$RT/prepared/{pilot_prompts.jsonl,pre_gate_plan.json,pre_gate_hashes.json}`;
- `$RT/execution/PRE_GATE_ACCEPTANCE_03_13.private.json` (record della tua accettazione).

Config, autorizzazione e approvazione **non** vengono riscritte. Una versione precedente diversa
viene conservata come `*.pre_acceptance`. Rilanciarlo è idempotente (`UNCHANGED`/`REUSED`).
Con `blocking` non vuoto termina con `REFUSED_BLOCKING_CONDITIONS`, exit 2, senza scrivere nulla.

## 4. (facoltativo) stesso preflight con `prepare_gate.py`

Il passo 3 lo ha già eseguito. Per rifarlo a mano:

```bash
$PY studio2/fase03/prepare_gate.py --config $CFG \
  --input-manifest $RT/execution/PILOT_INPUT_MANIFEST.frozen.json \
  --source-inventory $RT/execution/PILOT_INPUT_SOURCES.frozen.json \
  --insight-handoff $RT/results/validated_insight_library_qwen_122b_primary_producer_remediation.json \
  --ledger $LEDGER --pilot-id $PILOT \
  --model-snapshot $RT/tokenizers/a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9 \
  --output-dir $RT/prepared
```

Atteso: `READY_FOR_PRE_GATE_GENERATION_PROBE`, exit 0.

## 5. Sonda budget (chiamate al 122B)

```bash
export STUDIO2_CONSUMER_API_KEY=...   # non nell'argv
$PY studio2/fase03/run_pilot.py --config $CFG --prepared-dir $RT/prepared --results-dir $RT/results \
  --ledger $LEDGER --pilot-id $PILOT --stage budget --execute --acknowledge EXECUTE_PHASE03_PRELIMINARY_PILOT
```

Atteso: `FROZEN_FOR_STABILITY_GATE` e `$RT/results/frozen_gate_config.json`; al massimo 3 chiamate
per candidato. `NO_GO_GENERATION_BUDGET` (exit 2) è un esito, non un errore.

## 6. Stability gate (120 chiamate)

```bash
$PY studio2/fase03/run_pilot.py --config $CFG --prepared-dir $RT/prepared --results-dir $RT/results \
  --ledger $LEDGER --pilot-id $PILOT --stage stability --execute --acknowledge EXECUTE_PHASE03_PRELIMINARY_PILOT
```

Atteso: `$RT/results/stability_summary.json` con `t3_pass`, `t4_pass`, `t6_evaluable`.

## Se un gate rifiuta

| Messaggio | Causa | Cosa fare |
|---|---|---|
| `presentation order has not been accepted by the author` | inventario pending o manomesso passato a prepare/runner | rilanciare il passo 3 e usare i file `*.frozen.json` |
| `presentation approval does not bind the exact order` / `sha256` dell'approvazione | file `PRESENTATION_ORDER_APPROVAL_2026-09-15.json` in `/Users/luker/.codex/worktrees/dd86/…` alterato o rimosso | **non** eliminare né potare la worktree `dd86`; ripristinare il file (copia identica: `$RT/execution/presentation_order_approval.private.json`, `0f9f7b7f…`). La config non può puntare altrove senza invalidare i binding |
| `execution approval does not cover this exact configuration` | config o autorizzazione modificate | ripristinare i byte `0c3cd34e…` / `7dcec105…`; non rigenerare l'autorizzazione |
| `configuration changed between stages` / `primary library was not produced under this execution configuration` | config diversa da quella nei binding | come sopra: la config è congelata dai binding esistenti |
| `pilot suspended; requires a new reviewed disposition` | `L02` | decisione separata, vedi sopra |
| `alternate_conformity has no successful closed outcome` | `L06` | decisione separata, vedi sopra |
| `durable STOP blocks …` | nuovo STOP contabile | fermarsi; non riconciliabile con REM-6 se `#N` |
| `prepared hash mismatch` / `prepared prompts differ` | `prepared/` alterata o config cambiata | rilanciare il passo 3 |
| `probe transport triplet unresolved` | errore di trasporto nella sonda | evidenza zero-token e `--resume --retry-request`, come per i producer |
| `frozen gate provenance mismatch` | `frozen_gate_config.json` o prepared cambiati dopo la sonda | non rigenerare `prepared/` dopo il passo 5 |
