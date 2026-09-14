# Report del raccordo metriche 03.9 → 03.10

**Stato: candidato implementato; verifica indipendente PENDING.** Data: 2026-09-14.
Branch proprietario: `codex/studio2-harness`. HEAD iniziale verificato:
`51160872906feaa63c1fda5e9cf6e0fe8538fb16`. Commit implementativo esatto:
`caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae`.

Questo report non è un verbale indipendente, non chiude 03.9 o 03.10 e non rende efficace
`HARNESS_FREEZE.json`. Nessun walkthrough è stato aggiornato.

## Esito implementativo

È stato aggiunto un ingresso hash-pinned che legge il documento `metrics.json` 03.9, ne verifica
struttura, conteggi, denominatori e rapporti, quindi applica a ogni foglia di `summary` e
`clusters`:

- `accuracy` → `accuracy_all`;
- `n` → `total`;
- `abstentions` → `abstained`;
- `non_abstained` preservato e verificato uguale a `total - abstained`;
- `invalid=0` esplicito soltanto per il contratto 03.9 valid-only.

I valori dei tre rapporti vengono copiati dal documento sorgente dopo la verifica e non
ricalcolati nell'output. Il calcolo nativo 03.10 ora espone anche `non_abstained`. Una risposta
invalida del pilot è non corretta e non astenuta; resta quindi compresa nel denominatore di
`accuracy_non_abstained`, senza essere promossa a previsione valida.

## Compatibilità delle fonti

Non è emerso un conflitto normativo. La differenza concreta è questa:

- la specifica 03.9 dichiara `valid=true` per tutte le righe prodotte, perché un input invalido
  arresta l'esecuzione; perciò il suo aggregato non contiene `invalid`;
- la specifica 03.10 contempla risposte non valide del modello e impone che non diventino
  astensioni; perciò `invalid` è un conteggio autonomo e `non_abstained = total - abstained` lo
  include.

L'adapter non generalizza `invalid=0` a sorgenti diverse: rifiuta campi extra, compreso un campo
`invalid` inatteso, e fallisce su aritmetica incoerente. Il contratto completo è in
`CONTRATTO_RACCORDO_METRICHE.md`.

## Punti effettivi individuati

- Produzione 03.9: `baseline.py::metric`, consumata da `evaluate` per `summary` e `clusters` e
  serializzata in `metrics.json`.
- Lettura del raccordo: `metric_adapter.py::load_baseline_metrics`, con SHA-256 atteso
  obbligatorio.
- Adattamento di tutte le foglie: `adapt_baseline_metrics_document` e
  `adapt_baseline_metric`.
- Produzione nativa 03.10: `metrics.py::three_numbers`.
- Consumo degli endpoint 03.10: `metrics.py::endpoint_statistic` e il bootstrap che riceve tale
  statistica.

La ricerca sul codice ha confermato che prima di questo delta non esisteva un lettore operativo
del documento 03.9: `INTERFACE_CHECK.json` era soltanto un confronto read-only.

## Test ed esiti

Prima delle modifiche:

- suite protocollo/guardie/harness: 28 eseguiti, 27 PASS, 1 errore preesistente in
  `test_real_0312_adapter_when_checkout_is_available`; il checkout 03.12 corrente non coincide
  più con il vecchio hash pinnato dal candidato 03.10;
- guardiano documentale: 35 test, 14 failure preesistenti, 1 skip.

Dopo il delta:

- test mirati `MetricTests`: **9/9 PASS**;
- suite 03.9 sul main corrente: **10/10 PASS**;
- confronto esaustivo fra la funzione reale `baseline.py::metric`, l'adapter e
  `metrics.py::three_numbers`: **12.341/12.341 configurazioni PASS**, per `total=0..40`, tutte
  le combinazioni ammissibili di corrette e astensioni, con identità dei tre oggetti numerici
  copiati dall'adapter;
- suite protocollo/guardie/harness: 34 eseguiti, **33 PASS e lo stesso unico errore 03.12**;
- `python3 -m py_compile` sui tre moduli interessati: PASS;
- `git diff --check`: PASS;
- guardiano documentale: 35 test, gli stessi 14 failure e 1 skip.

L'errore 03.12 non è stato corretto perché questo incarico vieta di cambiare i pin 03.12; era
presente prima del delta e non appartiene al raccordo delle metriche. I log locali sono
`/tmp/fot_tep_metric_full_tests.log` e `/tmp/fot_tep_metric_docs_tests.log`; non sono artefatti da
committare.

## File del commit implementativo

- `metric_adapter.py`: adapter hash-pinned e fail-closed del documento completo 03.9;
- `metrics.py`: esposizione esplicita del conteggio `non_abstained`;
- `test_harness.py`: casi ordinari, astensioni, invalidi, zero righe, denominatore nullo,
  documento completo, hash errato e sorgente incoerente;
- `SPECIFICA_HARNESS.md`: denominatori, mapping e semantica validità/invalidità;
- `CONTRATTO_RACCORDO_METRICHE.md`: contratto autonomo e inventario producer/consumer.

Diff implementativo: **5 file, 484 inserimenti, 1 rimozione** rispetto a `5116087`.

## Perimetro preservato

Non sono stati modificati D9, endpoint, configurazione canonica dei modelli, ordine delle label,
pin 03.12, `run_pilot.py`, piano statistico generale, dati o risultati. Non sono state eseguite
chiamate API, simulazioni, inferenze o analisi su run finali. Il vecchio
`HARNESS_FREEZE.json` resta la fotografia pending del candidato precedente e non viene presentato
come manifest del nuovo delta.

## Identità e verifica successiva

Esecutore del delta: **OpenAI Codex basato su GPT-5**, finestra proprietaria corrente, profilo
implementativo. L'identificativo interno della task e il livello di reasoning non sono esposti in
modo verificabile a questa sessione e non vengono inventati.

Revisore indipendente: **non ancora assegnato; stato PENDING**. Il revisore dovrà operare in
un'altra finestra, preferibilmente con un altro modello, e registrare nel verbale modello esatto,
provider/prodotto, livello di reasoning se visibile, ID della task/sessione, data, worktree e
commit verificato. Il prompt pronto è `PROMPT_VERIFICA_RACCORDO_METRICHE.md`.

## Fonti lette

Sono stati letti l'handoff rev. 02, `docs/MAINTENANCE.md`, i prompt operativi di fase, verifica,
documentazione e commit, la consegna/specifica/report/verbale/controllo interfaccia/manifest rev. 3
della 03.9, specifica/report/stato/freeze e codice pertinente della 03.10, e il solo
`DELTA_HARNESS_03_10.md` della rev. 10 per le regole incidenti sul raccordo. Costo indicativo:
circa 20–25 mila token di fonti e codice mirato, senza lettura massiva di dati sperimentali.
