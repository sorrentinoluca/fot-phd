# 7.4-MAT — sequenza per Luca (shell nativa del Mac)

Eseguito da Claude Cowork al posto di `gpt-5.6-sol` (sostituzione dichiarata). Nessuna finestra
LLM esegue questi comandi; `fot-tep-runtime` non è mai collegato a una sessione. A ogni passo:
incolla in chat **solo** l'output indicato (SHA, conteggi, esiti — mai `base_url`, chiavi, path
con segreti). Un criterio di STOP vale sempre: qualunque `FAIL`, traceback o valore diverso
dall'atteso → fermarsi e incollare l'errore, senza riprovare.

```bash
export WT=/Users/luker/fot-tep-pubblicazione-consolidamento-0315-metriche   # worktree di main
export PY=/opt/anaconda3/bin/python3
export RT=/Users/luker/fot-tep-runtime
export ROOT_T=$RT/studio2-fase03-batch-finale-01
export CFG_T=$RT/studio2-fase03-batch-finale-01.config
cd "$WT"
```

## 1. Merge locale e suite (nessun push, nessun tag)

```bash
git status --short | head -5          # atteso: vuoto
git merge --no-ff codex/studio2-batch-finale-esecuzione \
  -m "Merge studio2 fase03: revisione 002 e preparazione 7.4-MAT"
"$PY" -c "import numpy, tzdata, openai, transformers, jsonschema; print(numpy.__version__)"   # atteso 2.2.6
"$PY" -m unittest $(ls studio2/fase03/harness/test_*.py | sed 's|/|.|g; s|\.py$||') \
  studio2.fase03.evidence.test_test_lot_evidence 2>&1 | tee /tmp/suite_002.txt | tail -4
```

Atteso: `Ran 329 tests` (318 + 7 `test_final_target_d9` + 4 `test_prepare_final_target_inputs`),
`OK`. Incolla le ultime 4 righe. STOP se non è `OK`.

## 2. Preparazione degli input (offline, non tocca alcun ledger)

```bash
"$PY" studio2/fase03/prepare_final_target_inputs.py            # piano: non scrive nulla
```

Atteso: `"status": "PLAN_ONLY"`, tutti i controlli `PASS` (una sola riga `NOTE` con lo SHA di
`final_prompts.jsonl`), e `configuration_sha256_to_accept`. Se è così, l'accettazione della
configurazione esatta è tua e si esprime ripetendo quello SHA:

```bash
"$PY" studio2/fase03/prepare_final_target_inputs.py --execute \
  --acknowledge PREPARE_PHASE03_FINAL_TARGET_INPUTS --author Luca \
  --accept-configuration-sha256 <SHA stampato dal piano>
```

Atteso: `"status": "PREPARED"`, `files_sha256` con cinque SHA, e il controllo
`rehearsal: D9 chain and real canary binding…` `PASS` con `canary_slots_bound: 300`: è la prova
generale del piano canary (stessa catena D9, binding reale) su un ledger temporaneo che porta
l'identità del target e viene cancellato. Scrive solo `$CFG_T/{execution.private.json,
generation.json,execution_authorization.private.json}` e `$RT/prepared-7-4/{canary_prompts.jsonl,
final_prompts.jsonl,PROMPT_FINALI_7_4.json}`. Incolla l'output intero (non contiene endpoint).
STOP su qualunque `FAIL`: prima del tag si corregge senza nuova revisione.

## 3. Tag 002 e push (solo se 1 e 2 sono OK)

```bash
cp /tmp/suite_002.txt studio2/fase03/batch_finale/SUITE_MAC_revisione_002.txt
git add studio2/fase03/batch_finale/SUITE_MAC_revisione_002.txt
git commit -m "studio2(fase03): suite Mac sulla revisione 002"
git tag -a studio2-fase03-protocollo-finale-frozen-002 \
  -m "Protocollo finale, revisione 002: nessun limite di giorni (canary 300, massimo 7.432), modo d9.final_target"
git push origin main studio2-fase03-protocollo-finale-frozen-002
git rev-parse HEAD
```

Incolla lo SHA. Da qui il contenuto congelato non si modifica in luogo.

## 4. Approvazione della materializzazione (decisione tua, non precompilata)

```bash
"$PY" studio2/fase03/prepare_final_target_inputs.py --approval-template
```

Scrive `studio2/fase03/batch_finale/APPROVAZIONE_MATERIALIZZAZIONE_7_4.json` con tag, commit,
SHA del protocollo e della revisione, `inventory_sha256`, `schedule_sha256`, SHA dei quattro file,
massimo 7.432 — e `decision`, `author`, `date` **vuoti**. Controlla i valori, poi compila a mano
i tre campi (`"decision": "accepted"`, `"author": "Luca"`, `"date": "2026-09-18"`). Il file si
committa con l'evidenza (passo 8), non prima: la materializzazione ne registra lo SHA.

## 5. Dry-run e materializzazione

```bash
MAT_ARGS=(--approval "$WT/studio2/fase03/batch_finale/APPROVAZIONE_MATERIALIZZAZIONE_7_4.json"
  --config "$CFG_T/execution.private.json" --generation "$CFG_T/generation.json"
  --prompts "$RT/prepared-7-4/final_prompts.jsonl"
  --canary-prompts "$RT/prepared-7-4/canary_prompts.jsonl"
  --tokenizer-snapshot "$RT/studio2-fase03-d9-pilot-03/tokenizers/a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9")
"$PY" studio2/fase03/materialize_final_target.py "${MAT_ARGS[@]}"
```

Atteso: `"status": "READY_TO_MATERIALIZE"`, `blocking_prerequisites: []`, `planned_maximum 7432`,
`stage_quota.final_canary 300`, inventario `227e5e9c…`, schedule `1acfc404…`. STOP altrimenti.

```bash
ls "$ROOT_T" 2>/dev/null && echo "STOP: la radice esiste"
"$PY" studio2/fase03/materialize_final_target.py "${MAT_ARGS[@]}" \
  --execute --acknowledge MATERIALIZE_PHASE03_FINAL_BATCH_TARGET
export TARGET=$ROOT_T/TARGET_FINALE_7_4.json
shasum -a 256 "$ROOT_T"/{TARGET_FINALE_7_4.json,INVENTARIO_FINALE_7_4.json,SCHEDULE_FINALE_7_4.json,CANARY_ATTESI_7_4.json,final_prompts.jsonl,canary_prompts.jsonl}
```

Atteso: `"status": "MATERIALIZED"`. Incolla l'output JSON e i sei SHA.

## 6. Piano del canary (nessuna chiamata) — sul target reale

```bash
lsof "$ROOT_T/ledger.sqlite3"                                  # atteso: vuoto
"$PY" studio2/fase03/run_final_canary.py --target "$TARGET"
```

Atteso: `"status": "PLAN_ONLY"`, `planned 10`, `day_index 1`, `declared_day` = `observed_day` =
oggi (Europe/Rome), `passed/marked/stops` vuoti. STOP su qualunque errore `D9:` o
`FATAL_ACCOUNTING_ERROR`: non si passa alle chiamate.

## 7. Canary iniziale (10 chiamate reali)

Preflight: VPN GlobalProtect connessa; `lsof` sul ledger vuoto; chiave solo in env. Cmd+Q di
Claude desktop non serve finché nessuna sessione ha `fot-tep-runtime` collegato.

```bash
export STUDIO2_CONSUMER_API_KEY='...'      # mai in argv o in file
"$PY" studio2/fase03/run_final_canary.py --target "$TARGET" \
  --execute --acknowledge EXECUTE_PHASE03_FINAL_CANARY 2>&1 | tee /tmp/canary_giorno1.txt
```

Atteso: `"verdict": "PASS"`, `behavior_changes 0`, e in `identity` dieci volte
`qwen3.5-122b` / `vllm-0.27.1-934a3247`. Esiti diversi:

- `canary identity change` → STOP durevole; nessun comando riprende da solo;
- `MARKED` al primo giorno → il batch **non** si sblocca (§6.4): decisione dell'autore;
- risposta invalida (`canary day … has N invalid responses`) → il giorno resta aperto, non si
  rigenera (D3): decisione dell'autore;
- errore di trasporto → non rilanciare a mano: incolla l'errore (prova zero-token o consumo incerto
  si decidono con D3).

Poi, in sola lettura:

```bash
sqlite3 "file:$ROOT_T/ledger.sqlite3?mode=ro" \
 "select stage,status,quota_kind,count(*),round(avg(latency_ms)/1000,2),sum(prompt_tokens),sum(completion_tokens) from requests group by 1,2,3;" \
 "select event,created_utc,artifact_sha256 from events where event like 'ledger_profile:%' or event like 'canary_%';" \
 "select detail_json from events where event like 'ledger_profile:%';"
shasum -a 256 "$ROOT_T"/results/canary_*.json
```

Incolla: l'output JSON del canary (contiene solo verdetto, hash e identità, nessun testo di
risposta) e l'output di `sqlite3`/`shasum`.

## 8. Dopo l'evidenza

Claude scrive `EVIDENZA_MATERIALIZZAZIONE_7_4.md` (+ manifest) dal tuo output; la si committa
insieme a `APPROVAZIONE_MATERIALIZZAZIONE_7_4.json`. **Nessun lotto scientifico** in questo
mandato: il primo comando del batch si esegue solo col via dell'autore.
