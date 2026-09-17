# Runbook 7.4 — batch finale (comandi per Luca dalla shell nativa del Mac)

Sostituzione di modello dichiarata: il mandato era indirizzato a `gpt-5.6-sol`; l'esecuzione
è di `claude-opus-5` (Claude Cowork). Nessuna chiamata a modelli è stata effettuata in
preparazione: tutto ciò che segue lo esegue Luca.

Questo runbook **non autorizza nulla**. Esegue solo dopo: review indipendente del
protocollo candidato, tag annotato `studio2-fase03-protocollo-finale-frozen-001`, e
chiusura dei punti aperti di `REPORT_7_4_PREP.md`.

Aggiornato da 7.4-FIX con le decisioni d'autore del 2026-09-17
(`DECISIONI_AUTORE_7_3_REV2_2026-09-17.md`, SHA `535939de…`): D1 assegnazione delle
finestre, D2 condizione `B-noLF`, D3 retry/STOP al posto di `Q=0`. Il totale massimo di
chiamate passa da **6.902 a 7.302** (6.902 + quota retry separata di 400).

## 0. Ambiente

Tutti i comandi si eseguono dalla shell nativa del Mac, mai da una finestra LLM.

```bash
cd /Users/luker/fot-tep
export PY=/opt/anaconda3/bin/python3
export STUDIO2_CONSUMER_API_KEY='...'   # solo in env, mai in argv, mai in un file committato
export STUDIO2_PRODUCER_API_KEY='...'   # non usato dal batch finale: nessuna chiamata producer
```

Prima di qualunque comando che scrive sul ledger:

1. VPN GlobalProtect connessa;
2. Cmd+Q dell'app Claude desktop (nessuna finestra LLM attiva);
3. `lsof` vuoto sul ledger del target:
   ```bash
   lsof /Users/luker/fot-tep-runtime/studio2-fase03-batch-finale-01/ledger.sqlite3
   ```
4. avvio sotto `caffeinate` legato al PID del comando:
   ```bash
   "$PY" studio2/fase03/run_final_batch.py ... & caffeinate -dims -w $!
   ```

Le chiavi non compaiono mai in `argv`, nei log o nei file committati; `api_key.json` e
`server_enea.json` non si aprono.

## 1. Preflight offline (nessuna chiamata, ripetibile)

```bash
"$PY" studio2/fase03/build_final_inventory.py --out-dir /tmp/batch74
"$PY" studio2/fase03/build_window_assignment.py
"$PY" -m unittest studio2.fase03.harness.test_final_batch \
  studio2.fase03.harness.test_final_prompts studio2.fase03.harness.test_bnolf \
  studio2.fase03.harness.test_window_assignment \
  studio2.fase03.evidence.test_test_lot_evidence
```

Attesi: `unique_total 2244`, `requests_total 6732`, `be_structural_diff` `PASS` su entrambe
le librerie, e gli SHA di inventario e schedule uguali a quelli in
`studio2/fase03/batch_finale/INVENTARIO_SCHEDULE_7_4.json`. Se uno SHA differisce, **fermarsi**:
la schedule non è più quella pre-registrata.

`build_window_assignment.py` è idempotente e non deve modificare
`batch_finale/ASSEGNAZIONE_FINESTRE_7_4.json`: se `git status` lo mostra sporco, l'assegnazione
non è più quella congelata prima dei dati di test e ci si ferma.

## 1-bis. Input consumer del lotto test (D1, prerequisito dei prompt)

Il lotto test 03.11 non è in repository: si scarica dalla release `studio2-fase03-test-v1`
e si verifica **prima** di estrarre qualunque evidenza.

```bash
cd /Users/luker/fot-tep
mkdir -p studio2/fase03/fault_runs/test_batch
curl -fL -o studio2/fase03/fault_runs/test_batch/test_batch_f5_001.tar.gz \
  https://github.com/sorrentinoluca/fot-tep-data/releases/download/studio2-fase03-test-v1/test_batch_f5_001.tar.gz
printf '%s  %s\n' \
  ac1e7c0c4575ab746ee24a8bb5ce7f09289919773bc4d8c61ba86f7a93218a55 \
  studio2/fase03/fault_runs/test_batch/test_batch_f5_001.tar.gz \
  > studio2/fase03/fault_runs/test_batch/test_batch_f5_001.tar.gz.sha256
shasum -a 256 -c studio2/fase03/fault_runs/test_batch/test_batch_f5_001.tar.gz.sha256
tar -xzf studio2/fase03/fault_runs/test_batch/test_batch_f5_001.tar.gz \
  -C studio2/fase03/fault_runs/test_batch
```

Se `shasum -c` non dice `OK`, **fermarsi**: non si estrae da un archivio non verificato.

Estrazione con la pipeline congelata 03.6, **solo** per la finestra assegnata a ciascun run:

```bash
"$PY" studio2/fase03/evidence/extract_test_lot_evidence.py \
  --lot-root studio2/fase03/fault_runs/test_batch/test_batch_f5_001 \
  --normal   code/tep_cache/mode1_normal_500.xlsx \
  --r2-guard studio2/fase03/soglie_normal/R2_GUARD_RECHECK.json \
  --output   /Users/luker/fot-tep-runtime/prepared-7-4/test_input
```

Attesi: `evidence_unit_count 78`, `not_extracted []`, `windows_extracted_per_run 1`,
`consumer_visible_json_text_leakage PASS`. Un run assente o una finestra non estraibile si
**registra** in `not_extracted` e non si sostituisce: se la lista non è vuota, riportarla e
fermarsi prima di rendere i prompt.

## 1-ter. Rendering offline dei 2.244 prompt

```bash
"$PY" studio2/fase03/build_final_prompts.py \
  --pilot-manifest /Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03/execution/PILOT_INPUT_MANIFEST.frozen.json \
  --test-input     /Users/luker/fot-tep-runtime/prepared-7-4/test_input \
  --tokenizer-snapshot /Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03/tokenizers/a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9 \
  --out /Users/luker/fot-tep-runtime/prepared-7-4
```

Attesi: `unique_total 2244`, conteggi per blocco `1728/224/148/144`,
`be_pseudolabel_diff.status PASS`, `bnolf_policy_diff.status PASS` su 148 prompt,
`max_prompt_tokens` entro il contesto qualificato. Esempi locali, spazio di label, agenti e
derangement restano quelli del manifest congelato del pilot `84176888…`: dal lotto test
viene **solo** il testo neutrale del caso.

## 2. Materializzazione del target (la esegue Luca dopo il tag)

Prima il dry-run, che non scrive nulla ed elenca i prerequisiti mancanti:

```bash
"$PY" studio2/fase03/materialize_final_target.py \
  --approval /Users/luker/fot-tep/studio2/fase03/batch_finale/APPROVAZIONE_MATERIALIZZAZIONE_7_4.json
```

Quando lo stato è `READY_TO_MATERIALIZE`:

```bash
"$PY" studio2/fase03/materialize_final_target.py \
  --approval .../APPROVAZIONE_MATERIALIZZAZIONE_7_4.json \
  --config    /Users/luker/fot-tep-runtime/studio2-fase03-batch-finale-01.config/execution.private.json \
  --generation /Users/luker/fot-tep-runtime/studio2-fase03-batch-finale-01.config/generation.json \
  --prompts   /Users/luker/fot-tep-runtime/prepared-7-4/build/final_prompts.jsonl \
  --canary-prompts /Users/luker/fot-tep-runtime/prepared-7-4/canary_prompts.jsonl \
  --tokenizer-snapshot /Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03/tokenizers/a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9 \
  --execute --acknowledge MATERIALIZE_PHASE03_FINAL_BATCH_TARGET
```

Crea `TARGET_FINALE_7_4.json`, il ledger sotto profilo `final_batch`, e vi congela
inventario, schedule e attesi canary. La radice del target deve **non** esistere prima:
un successore fresco non riusa mai una radice.

Da qui in avanti, `export TARGET=/Users/luker/fot-tep-runtime/studio2-fase03-batch-finale-01/TARGET_FINALE_7_4.json`.

## 3. Canary iniziale (obbligatorio prima di ogni chiamata scientifica)

```bash
"$PY" studio2/fase03/run_final_canary.py --target "$TARGET"          # piano, nessuna chiamata
"$PY" studio2/fase03/run_final_canary.py --target "$TARGET" \
  --execute --acknowledge EXECUTE_PHASE03_FINAL_CANARY
```

Dieci chiamate, una volta per giorno civile Europe/Rome in cui si inviano chiamate
scientifiche, **prima** del primo lotto del giorno; al massimo sette giorni, quindi 70.

- `verdict: PASS` → il batch è sbloccato **per quel giorno civile**: il runner rifiuta un
  lotto in un giorno che non ha un canary PASS proprio (barriera canary→lotto, §6);
- `verdict: MARKED` (coppia parsata diversa in almeno un canary) → giorno marcato: il
  protocollo non cambia, ma il secondo giorno marcato è STOP;
- variazione del solo hash grezzo → registrata, **non** marca il giorno;
- cambio di `returned_model` **o** `system_fingerprint` → STOP immediato, prima di altre
  chiamate; l'identità osservata su tutte e dieci le chiamate del giorno è persistita
  nell'evento del verdetto (`identity`), non solo controllata in memoria;
- una risposta canary **ricevuta ma invalida** non si rigenera (D3): il giorno non si chiude,
  resta senza verdetto, e nessun lotto scientifico parte in quel giorno finché l'autore non
  decide. Il file `results/canary_<giorno>_invalid.json` elenca i prompt coinvolti.

Per sapere quali lotti scientifici sono marcati da un canary fallito (query di sola lettura,
eseguibile anche a campagna chiusa):

```bash
"$PY" studio2/fase03/query_canary_marking.py --target "$TARGET" --full
```

Regola applicata: **unione** fra l'intervallo §6.5 (chiamate fra l'ultimo canary PASS e il
canary fallito) e l'insieme §10.5 (chiamate del giorno civile marcato). La query non scrive
nulla: nessun record terminale viene riscritto.

## 4. Tratti consigliati del batch

Le tre passate sono stage separati: `--pass-index 1`, poi `2`, poi `3`. Una passata si apre
solo quando la precedente è chiusa.

```bash
# piano, nessuna chiamata
"$PY" studio2/fase03/run_final_batch.py --target "$TARGET" --pass-index 1

# primo tratto
"$PY" studio2/fase03/run_final_batch.py --target "$TARGET" --pass-index 1 \
  --max-requests 250 --execute --acknowledge EXECUTE_PHASE03_FINAL_BATCH

# tratti successivi dello stesso stage
"$PY" studio2/fase03/run_final_batch.py --target "$TARGET" --pass-index 1 \
  --max-requests 250 --resume --execute --acknowledge EXECUTE_PHASE03_FINAL_BATCH
```

Dimensionamento a ~26 s per chiamata (media misurata nel pilot; p95 ~36,7 s):

| Tratto | Chiamate | Durata attesa (media) | Durata attesa (p95) |
| --- | ---: | ---: | ---: |
| consigliato | 250 | ~1 h 49 min | ~2 h 33 min |
| giornata piena | 1 000 | ~7 h 17 min | ~10 h 11 min |
| una passata | 2 244 | ~16 h 20 min | ~22 h 51 min |
| nucleo + canary + X | 6 902 | ~50,2 h | ~70,3 h |
| con la quota retry piena | 7 302 | ~53,2 h | ~74,4 h |

Con il margine del 20% del criterio T5: 60,3 h alla media e 84,3 h al p95 a 6.902 chiamate;
63,8 h e 89,3 h se l'intera quota retry di 400 venisse consumata, contro una finestra `W` di
168 h. Il margine temporale **non** crea quota di chiamate.

La riga di avanzamento è, per ogni chiamata:

```
final_batch_r1 312/2244 sent=62 invalid=1 abstain=44 mean=25.9s eta=13.9h
```

`sent` conta le chiamate di questo tratto, `invalid` le risposte ricevute non parsabili
(terminali), `abstain` le astensioni D10, `eta` è sequenziale sulla media osservata.

## 5. Come fermare e come riprendere

Fermare: `Ctrl-C` fra due chiamate, oppure semplicemente lasciare esaurire `--max-requests`.
SQLite è la fonte autoritativa; il record dell'ultima chiamata è già durevole.

Riprendere: **sempre** con `--resume`, stesso target, stessa schedule, stesso `--pass-index`.
`--resume` salta gli slot con risposta ricevuta (terminali, validi o no), non rimescola e non
riusa slot. Uno slot `ZERO_TOKEN_PROVEN` — cioè riconciliato con prova che non è stata
generata alcuna emissione — viene **ritentato** una volta, dopo un'attesa crescente
(30 s, 60 s, 120 s, 240 s… fino a 15 min), a carico della quota retry separata. Senza
`--resume` il runner rifiuta di continuare una passata che ha già richieste registrate.

Il giorno civile del tratto si dichiara con `--day AAAA-MM-GG` quando l'esecuzione
attraversa la mezzanotte di Roma; senza l'opzione vale il giorno corrente.

Se il comando si interrompe fra invio e salvataggio, lo slot resta `INTENT`/`FAILED` e la
ripresa si ferma: è incertezza, non un fallimento da ritentare (punto 6).

## 6. Cosa fare per ogni tipo di STOP

| STOP | Segnale | Azione |
| --- | --- | --- |
| Richiesta incerta (`INTENT`/`FAILED` senza risposta) | `uncertain request ...; reconcile it with ledger_cli` | Raccogliere la prova durevole del provider, poi `"$PY" -m studio2.fase03.harness.ledger_cli --ledger <ledger> --pilot-id studio2-fase03-batch-finale-01 reconcile-zero-token --request-id <id> --evidence <f> --approval <f>`. **D3:** se la prova stabilisce zero token generati (ragionamento incluso), la ripresa con `--resume` ritenta lo slot una volta, a carico della quota retry. Se la prova non chiude l'incertezza: nessun reinvio, STOP e decisione dell'autore. |
| Risposta ricevuta ma invalida o troncata | `invalid` nella riga di avanzamento | Nessuna azione: è un fallimento registrato e definitivo (D3 riga 3). Non si rigenera. |
| Quota retry esaurita | `cumulative retry quota 400 is exhausted` | STOP. Il tetto retry è separato dalla quota scientifica e non si allarga localmente. |
| Cinque fallimenti tecnici consecutivi | `STOP: 5 consecutive technical failures on [...]` | STOP: servizio verosimilmente indisponibile. Il contatore è **persistente** (derivato dal ledger) e non si azzera riavviando; si azzera solo con una chiamata che riceve risposta. Decisione dell'autore prima di riprendere. |
| Canary invalido | `canary day ... has N invalid responses` | Il giorno non si chiude e nessun lotto parte in quel giorno. Decisione dell'autore. |
| Lotto fuori da un giorno canary | `no canary PASS recorded for <giorno>` | Eseguire il canary del giorno prima del primo lotto, oppure dichiarare il giorno corretto con `--day`. |
| Sospensione d'identità | `pilot suspended: returned model/fingerprint ...` | STOP. L'unico percorso ammesso è una revisione approvata della configurazione e la riconciliazione già implementata; la ripresa richiede decisione dell'autore e, se cambia identità o autorizza nuove chiamate, una revisione di protocollo/quota. |
| Canary: identità cambiata | `canary identity change on <giorno>` | STOP immediato prima di altre chiamate. Nessun comando riprende da solo. |
| Canary: secondo giorno marcato | `second marked canary day` | STOP prima del lotto successivo; decisione dell'autore prima di qualunque ripresa. L'insieme marcato è quello dato da `query_canary_marking.py`: unione fra le chiamate dall'ultimo canary PASS al canary fallito e le chiamate del giorno civile marcato. Restano nell'analisi primaria ed escono dall'analisi di sensibilità già pre-specificata. |
| Quota per stage o totale | `stage quota ... is exhausted` / `cumulative hard stop 7302` | STOP. Nessun allargamento locale: il tetto è 6.902 chiamate scientifiche/canary/X più 400 retry provati = 7.302. |
| Schedule non autenticata | `schedule differs from the deterministic generator` | STOP. Non rigenerare sopra: verificare quale artefatto è cambiato. |
| Condizione non producibile | `conditions the frozen renderer does not produce` | STOP. Le quattro condizioni del protocollo (A, B-LF, E-LF, B-noLF) sono producibili: qualunque altro token è un errore di inventario, non una condizione da reinterpretare. |
| Ledger incoerente | qualunque `HarnessError` dal ledger in fase di bind | STOP. Non riscrivere storia incerta, non retrofittare. |

## 7. Cosa consegnare alla finestra dopo ogni tratto

Per ogni tratto, dal target:

- `results/final_batch_r<N>_summary.json` (fatti/totale, invalidi, astensioni, `stage_run`);
- `results/final_batch_r<N>_call_log.jsonl` (logging T7 §8.7, una riga per chiamata);
- l'ultimo `results/canary_<giorno>.json` e il suo verdetto;
- `"$PY" -m studio2.fase03.harness.ledger_cli --ledger <ledger> --pilot-id studio2-fase03-batch-finale-01 status`
  (conteggi per stage, quota, eventi canary).

Nessun file con chiavi o `base_url`. L'evidenza per lotto si consegna come i lotti del pilot:
manifest dei file, byte e SHA-256.

## 8. Verifica di chiusura dei conteggi

A fine passata e a fine batch:

```bash
"$PY" -m studio2.fase03.harness.ledger_cli --ledger <ledger> \
  --pilot-id studio2-fase03-batch-finale-01 status
```

Attesi finali: 2.244 richieste **base** per ciascuno dei tre stage di passata
(`final_batch_r1/r2/r3`, retry esclusi dal conteggio di stage e contati a parte),
`final_canary <= 70`, `technical_verification <= 100`, `retry_quota_used <= 400`,
cumulativo `<= 7302`, `unresolved_intents = 0`,
`consecutive_technical_failures` tutti sotto 5. Solo dopo la chiusura del ledger e questa
verifica si passa all'analisi (§7.1, passo 5).
