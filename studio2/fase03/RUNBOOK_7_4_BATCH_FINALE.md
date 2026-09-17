# Runbook 7.4 — batch finale (comandi per Luca dalla shell nativa del Mac)

Sostituzione di modello dichiarata: il mandato era indirizzato a `gpt-5.6-sol`; l'esecuzione
è di `claude-opus-5` (Claude Cowork). Nessuna chiamata a modelli è stata effettuata in
preparazione: tutto ciò che segue lo esegue Luca.

Questo runbook **non autorizza nulla**. Esegue solo dopo: review indipendente del
protocollo candidato, tag annotato `studio2-fase03-protocollo-finale-frozen-001`, e
chiusura dei punti aperti di `REPORT_7_4_PREP.md` (i punti 1 e 2 sono bloccanti).

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
"$PY" -m unittest studio2.fase03.harness.test_final_batch
```

Attesi: `unique_total 2244`, `requests_total 6732`, `be_structural_diff` `PASS` su entrambe
le librerie, e gli SHA di inventario e schedule uguali a quelli in
`studio2/fase03/batch_finale/INVENTARIO_SCHEDULE_7_4.json`. Se uno SHA differisce, **fermarsi**:
la schedule non è più quella pre-registrata.

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
  --prompts   /Users/luker/fot-tep-runtime/prepared-7-4/final_prompts.jsonl \
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

- `verdict: PASS` → il batch è sbloccato per quel giorno;
- `verdict: MARKED` (coppia parsata diversa in almeno un canary) → giorno marcato: il
  protocollo non cambia, ma il secondo giorno marcato è STOP;
- variazione del solo hash grezzo → registrata, **non** marca il giorno;
- cambio di `returned_model` o `system_fingerprint` → STOP immediato, prima di altre chiamate.

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
| totale 6 902 | 6 902 | ~50,2 h | ~70,3 h |

Con il margine del 20% del criterio T5: 60,3 h alla media e 84,3 h al p95, contro una
finestra `W` di 168 h. Il margine temporale **non** crea quota di chiamate.

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
`--resume` salta soltanto gli slot terminali (risposta ricevuta, o zero-token provato e
riconciliato), non rimescola e non riusa slot. Senza `--resume` il runner rifiuta di
continuare una passata che ha già richieste registrate.

Se il comando si interrompe fra invio e salvataggio, lo slot resta `INTENT`/`FAILED` e la
ripresa si ferma: è incertezza, non un fallimento da ritentare (punto 6).

## 6. Cosa fare per ogni tipo di STOP

| STOP | Segnale | Azione |
| --- | --- | --- |
| Richiesta incerta (`INTENT`/`FAILED` senza risposta) | `uncertain request ...; reconcile it with ledger_cli` | Raccogliere la prova durevole del provider, poi `"$PY" -m studio2.fase03.harness.ledger_cli --ledger <ledger> --pilot-id studio2-fase03-batch-finale-01 reconcile-zero-token --request-id <id> --evidence <f> --approval <f>`. Con `Q=0` **non** segue un nuovo invio: lo slot resta invalido e il batch prosegue. Se la prova non chiude l'incertezza: STOP e decisione dell'autore. |
| Sospensione d'identità | `pilot suspended: returned model/fingerprint ...` | STOP. L'unico percorso ammesso è una revisione approvata della configurazione e la riconciliazione già implementata; la ripresa richiede decisione dell'autore e, se cambia identità o autorizza nuove chiamate, una revisione di protocollo/quota. |
| Canary: identità cambiata | `canary identity change on <giorno>` | STOP immediato prima di altre chiamate. Nessun comando riprende da solo. |
| Canary: secondo giorno marcato | `second marked canary day` | STOP prima del lotto successivo; decisione dell'autore prima di qualunque ripresa. Le chiamate fra l'ultimo canary PASS e il canary fallito sono **marcate**: restano nell'analisi primaria ed escono dall'analisi di sensibilità già pre-specificata. |
| Quota per stage o totale | `stage quota ... is exhausted` / `cumulative hard stop 6902` | STOP. Nessun allargamento locale: il tetto 6.902 è il protocollo. |
| Schedule non autenticata | `schedule differs from the deterministic generator` | STOP. Non rigenerare sopra: verificare quale artefatto è cambiato. |
| Condizione non producibile | `conditions the frozen renderer does not produce` | STOP atteso finché il punto aperto 1 non è chiuso dall'autore. |
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

Attesi finali: `final_batch_r1 = final_batch_r2 = final_batch_r3 = 2244`,
`final_canary <= 70`, `technical_verification <= 100`, cumulativo `<= 6902`,
`unresolved_intents = 0`. Solo dopo la chiusura del ledger e questa verifica si passa
all'analisi (§7.1, passo 5).
