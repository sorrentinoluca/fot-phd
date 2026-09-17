# Runbook 7.2 — rigenerazione della libreria insight (contingenza)

**Si esegue solo se l'autore sceglie l'opzione 2 di
[`RIUSO_LIBRERIE_7_2.md`](RIUSO_LIBRERIE_7_2.md) §6**: rigenerare la libreria del 27B con il
template di remediation, per avere istruzioni identiche fra i due producer. Con l'opzione 1
(accettare l'asimmetria e dichiararla) non serve nessuna chiamata e questo file resta inapplicato.

Nessun meccanismo nuovo: si usano `producer_probe.py`, il ledger e i rimedi standard
(handoff rev07 §6.2). Questo documento **non** modifica codice, quota o accounting.

## 0. Prerequisito che tocca quota e accounting → review `b567`

Lo stage `alternate_conformity` di `pilot-03` è **chiuso** (`outcome` PASS) e la riserva del pilot
è esaurita (`8r+t = 15/15`, `requalification` 1/1): non è possibile rigenerare dentro `pilot-03`.
Serve un **target successore** (`pilot-04`), materializzato con `materialize_successor_recovery.py`
dallo stesso predecessore e con lineage dichiarata, e una configurazione che autorizzi il solo
stage producer alternativo.

Quota proposta per il nuovo target, da approvare:

| Voce | Richieste | Nota |
|---|---:|---|
| Libreria 27B (`G_A`) | 8 | uno per agente |
| Margine di retry di trasporto | 4 | `8r+t ≤ 15` resta valido con `r=0`; copre 401 e cadute del tunnel |
| **Totale** | **12** | il piano §8.4 prevede fino a ~20 fra generazione e retry |

Se l'autore vuole anche il 122B (non raccomandato: rimetterebbe in gioco il FAIL T9), aggiungere 8+4.
Ogni richiesta entra nel conteggio complessivo dello studio: 161 già consumate su `pilot-03`, il
nuovo target parte da zero con la propria lineage e il proprio massimo pianificato.

**Poiché tocca quota e accounting, la preparazione del target va sottoposta a `b567` prima
dell'esecuzione** (handoff rev07 §2 e §7).

## 1. Prima di partire (Mac, shell nativa)

```bash
export PY=/opt/anaconda3/bin/python3
export WT=/Users/luker/fot-tep/.worktrees/rem6-riconciliazione
export RT4=/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-04     # nuovo target
export PILOT=studio2-fase03-d9-pilot-04
cd "$WT"
lsof "$RT4/ledger.sqlite3"            # deve essere vuoto; se no: Cmd+Q di Claude desktop
ssh -N -L 127.0.0.1:18001:127.0.0.1:8001 10.168.24.21 &   # tunnel 27B
export STUDIO2_PRODUCER_API_KEY=…      # solo in env, mai in argv né nei log
caffeinate -dims -w $$ &
```

VPN GlobalProtect serve solo per il 122B: per il solo 27B basta il tunnel. Non toccare il server
27B né `--max-model-len`.

## 2. Blocco noto del runner, da sciogliere prima

`producer_probe.run` rifiuta un template diverso da quello congelato su qualunque stage che non sia
`producer_remediation`:

```text
only authorized remediation may change producer template
```

Quindi l'opzione 2 **non è eseguibile così com'è**: serve una decisione dell'autore su come dare al
27B le stesse istruzioni del 122B. Le due strade, entrambe da approvare e da far verificare a
`b567` perché toccano il contratto del runner o la quota:

1. autorizzare esplicitamente il template di remediation per lo stage alternate del nuovo target
   (modifica minima e dichiarata del guard, con la stessa forma di approvazione usata per la
   remediation: diagnosi, diff del template, hash);
2. eseguire la generazione 27B come stage di remediation del nuovo target, con l'autorizzazione
   scritta prevista da T9, tenendo il ruolo «alternativo» nella documentazione.

Finché una delle due non è decisa, questo runbook resta fermo qui.

## 3. Esecuzione (8 chiamate)

```bash
$PY studio2/fase03/producer_probe.py --config $RT4/execution/<config>.private.json \
  --source-inventory studio2/fase03/harness/PILOT_INPUT_SOURCES.pending.json \
  --results-dir $RT4/results \
  --provider-config $RT4/execution/producer_27b_successor.rev2.private.json \
  --model-snapshot $RT4/tokenizers/27B/017b9c7af6b5689d5dd426a76e0bc077eb5ca20a \
  --template $RT4/execution/producer_template_remediation_03_13.txt \
  --stage alternate_conformity --ledger $RT4/ledger.sqlite3 --pilot-id $PILOT \
  --execute --acknowledge EXECUTE_PHASE03_PRODUCER_CONFORMANCE \
  2>&1 | tee $RT4/results/alternate_$(date -u +%Y%m%dT%H%M%S).log
```

Atteso: `PASS`, 8/8 validi al primo tentativo, `validated_insight_library_qwen_27b_alternate_alternate_conformity.json`.

Il comando presuppone che sia stata sciolta la questione del §2; senza quella decisione il runner
rifiuta il template e non invia nulla.

## 4. Rimedi standard (nessun meccanismo nuovo)

| Sintomo | Rimedio |
|---|---|
| HTTP 401 o caduta del tunnel prima della generazione | `reconcile_zero_token` con evidenza `not_generated`, token 0, approvazione con `evidence_sha256`; poi `--resume --retry-request <id>` |
| STOP contabile | `reconcile_accounting_stop.py` (solo se spurio e con approvazione) |
| Fingerprint del 27B diverso da `vllm-0.28.0-5fc21ed4` | `revise_pilot_config.py` sul nuovo target: revisione approvata + riconciliazione, poi `--resume` |
| Richiesta incerta senza risposta | mai reinviare senza `--retry-request`: il ledger è fail-closed |

## 5. Regola pre-registrata per una risposta non valida

Fissata **prima** dell'esecuzione:

- per ciascun agente, al massimo **un** reinvio con lo **stesso prompt** e la stessa configurazione,
  ammesso solo per cause di trasporto documentate (zero token, nessuna risposta);
- una risposta **ricevuta** e non valida contro lo schema **non si reinvia**: si chiude lo stage con
  `FAIL` e si porta la decisione all'autore;
- nessuna modifica del template, dello schema, dei casi, dell'ordine o del cap dopo l'osservazione;
- limite complessivo: 12 richieste sul target; raggiunto il limite, STOP.

## 6. Dopo il run, consegnare a questa finestra

`ledger.sqlite3` (SHA prima e dopo), `results/` (summary, libreria validata, log del run), gli
eventuali file di riconciliazione, e l'esito stampato. La finestra scrive evidenza, report e
aggiorna `LIBRERIE_FINALI_CANDIDATE.json`; l'accettazione è di 7.2-R (`b567`) con i criteri di
[`CRITERI_ACCETTAZIONE_7_2.md`](CRITERI_ACCETTAZIONE_7_2.md).
