# Report 7.4-MAT — materializzazione del target finale (preparazione)

Finestra `batch-finale-esecuzione`, branch `codex/studio2-batch-finale-esecuzione` dal tag
`studio2-fase03-protocollo-finale-frozen-001` (`3963537`). Esecuzione di Claude Cowork
(il mandato era indirizzato a `gpt-5.6-sol`). **Zero chiamate a modelli**; runtime mai
collegato alla VM.

## Cosa contiene la revisione 002

| Commit | Contenuto |
| --- | --- |
| `e7ed69d` | Nessun limite di giorni: `FINAL_CANARY_QUOTA` 70 → 300 (guardia contabile), `CANARY_MAX_DAYS` = quota // 10, massimo 7.202 → 7.432. Due `7` cablati in `run_final_canary.py` corretti insieme alla costante del profilo. |
| `6da353b` | Modo `d9.final_target`: la guardia D9 legava ogni configurazione al ledger del pilot (lineage S=5 o riconciliazione storica S=4), quindi nessuna configurazione poteva aprire un ledger `final_batch` fresco. Terzo modo esplicito, esclusivo con lineage/storico, ammesso solo sul profilo `final_batch` senza righe di lineage o storico, con identita' 122B sempre autenticata. `test_final_target_d9.py` percorre i binding reali. |
| questo commit | `prepare_final_target_inputs.py` e il §1-quater del runbook. |

Il difetto era invisibile ai test perche' `test_final_batch.py` sostituisce
`pass_binding`/`canary_binding` con versioni senza `execution_config`: i binding di prova non
attraversavano la catena D9. `test_final_target_d9.py` nasce per chiudere quel buco.

## `prepare_final_target_inputs.py`

Deriva dal runtime del pilot i quattro input che `materialize_final_target.py` pretende
(configurazione eseguibile, contratto di generazione, prompt canary, 2.244 prompt) piu'
l'`execution_authorization` che `require_execution` esige sulla configurazione esatta del
target. Offline e fail-closed: senza `--execute` non scrive fuori da una temporanea, non apre
socket, non legge `api_key.json` ne' `server_enea.json`, stampa solo percorsi, SHA-256,
conteggi ed esiti.

Cosa autentica, prima di scrivere: i cinque pin (inventario, schedule, assegnazione finestre,
manifest del lotto test, mappa id→hash dei prompt); il contratto di generazione uguale campo
per campo a quello congelato dal gate del pilot, con lo SHA dei byte e quello canonico; la
configurazione del pilot uguale a quella sotto cui il gate ha girato; che le differenze dalla
configurazione del pilot siano **solo** quelle dichiarate (`execution_authorization`,
`pilot_ledger`, `call_budget`, `d9`, `derived_from`); l'identita' 122B qualificata; i dieci
prompt canary come righe **byte per byte** del file del pilot, con gli SHA della tabella §6 del
protocollo e di `CANARY_ATTESI_7_4.json`; la radice del target che ancora non esiste.

Chiude con una prova a vuoto che e' la risposta diretta alla lezione del difetto D9: catena
D9 reale e binding canary vero (`bind_stage` con `execution_config`) su un ledger `final_batch`
usa e getta che porta l'identita' del target, con rilettura del binding dal ledger. Atteso
`canary_slots_bound` = 300.

`--approval-template` scrive il modello di `APPROVAZIONE_MATERIALIZZAZIONE_7_4.json` con
`decision`, `author` e `date` vuoti — li compila l'autore — e pretende il tag 002 sul commit in
esecuzione. Nessuno dei file scritti viene mai sovrascritto con byte diversi.

## Verifiche fatte in questa finestra

- `python3 -m py_compile` sullo script; firme di `d9`, `ledger`, `guards`, `final_inventory`,
  `run_final_canary`, `run_pilot`, `runtime` controllate contro le chiamate dello script.
- `test_final_batch` 45 OK e `test_final_target_d9` nella VM (`e7ed69d`/`6da353b`).
- **Fa fede la suite sul Mac**: nella VM `jsonschema` e' vecchio e mancano i runtime.
  Da rieseguire su questo commit prima del merge (`batch_finale/SUITE_MAC_<sha>.txt`).
- `test_prepare_final_target_inputs` 4 OK nella VM: runtime del pilot sintetico, piano che non
  scrive, accettazione con SHA sbagliato rifiutata, scrittura, copia canary byte per byte, prova a
  vuoto con 300 slot, idempotenza, rifiuto di un canary alterato e di un contratto diverso dal gate.
- Non verificato in questa finestra: l'esecuzione reale di `prepare_final_target_inputs.py`,
  che richiede `/Users/luker/fot-tep-runtime` — mai collegato alle sessioni Cowork. Il piano
  (`PLAN_ONLY`) e' il primo comando di Luca e non scrive nulla.

## Sequenza per Luca

Comandi esatti, attesi e criteri di STOP: `batch_finale/SEQUENZA_7_4_MAT.md`.

1. Merge **locale** in `main` e suite completa sul Mac (attesi 329 test).
2. Runbook §1-quater: piano ed `--execute` con la prova a vuoto, **prima del tag**: un difetto
   emerso sul runtime reale si corregge senza una revisione 003.
3. Tag annotato `studio2-fase03-protocollo-finale-frozen-002`, push; poi `--approval-template` e
   compilazione a mano dell'approvazione (si committa con l'evidenza).
4. Runbook §2: `materialize_final_target.py` in dry-run, poi `--execute`.
5. Runbook §3: canary iniziale (dieci chiamate) — le prime chiamate della campagna.
6. Runbook §4: primo tratto, `--pass-index 1 --max-requests 250`. Il tratto da' la latenza
   reale: la stima di durata si aggiorna li'.
