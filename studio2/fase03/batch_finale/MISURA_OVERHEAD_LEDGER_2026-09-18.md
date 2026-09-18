# Costo del ledger per chiamata — misura prima/dopo (2026-09-18)

Seguito di `ANALISI_LATENZA_TRATTO_1.md`, che attribuiva al runner la deriva della latenza
del tratto 1 (16,8 → 19,4 s; +49 ms di latenza e +24 ms di intervallo per riga del ledger).

## Causa

Prima di ogni invio `Provider.call` esegue `binding` + `bind_stage`, e la prenotazione
(`_insert_intent`) rivalida l'inventario: il ledger intero passa 2–3 volte per chiamata. Per ogni
riga 122B `COMPLETED`, `_accounting_record_link` e `_validate_tokenizer_accounting_record`
leggevano **tutti** gli eventi con `detail_json`, e gli eventi `tokenizer_accounting:` contengono
il prompt intero: costo più che lineare nel numero di righe.

## Correzione (`65f2a1f`)

Stessi controlli, ripetuti solo quando i dati cambiano: `detail_json` degli eventi letto dal DB
su richiesta e mai in cache fra chiamate; esito della validazione 122B per riga memorizzato nel
processo (chiave: riga, hash raw/record, artefatto, istante e lunghezza del detail dei due
eventi di accounting); digest dei binding memorizzato; `leaf`/`attempts` filtrati in SQLite. Un
processo nuovo valida comunque tutto il ledger una volta.

## Misura

`bench_ledger_overhead.py` su una copia del ledger reale `studio2-fase03-batch-finale-01`
(71 righe native: canary + 58 scientifiche + FAILED), Mac, ambiente `fottep002`, nessuna
chiamata al modello. Tempo di `binding` + `bind_stage`, cioè il lavoro di `Provider.call` prima
dell'invio; mediana di 4 ripetizioni dopo la prima.

| Codice | Prima chiamata | Per chiamata |
| --- | ---: | ---: |
| `066f4f1` (main, runner-7-4-fix-002) | 1.701 ms | **1.729 ms** |
| `65f2a1f` (7-4-fix-retry-rete) | 1.088 ms | **61 ms** |

Il vecchio valore (~24 ms per riga a 71 righe) coincide con la crescita dell'intervallo fra
chiamate misurata nel tratto 1 (0,27 → 1,60 s). Il nuovo costo per chiamata è 28 volte più
basso; la prima chiamata di un processo resta la validazione completa (una volta per tratto).

## Limiti

Misurato a 71 righe. La parte residua che cresce con il ledger (lettura della tabella
`requests`, controlli per riga in Python) era ~8 ms ogni 400 righe nelle fixture; va
ricontrollata con lo stesso script a fine passaggio 1 (~2.300 righe). La latenza del modello
(~7,7 ms per token generato) non cambia.
