VERDETTO: OK

# Verifica indipendente del raccordo metriche 03.9 → 03.10

> Questo verbale certifica **esclusivamente** il delta `5116087..caf5bfb` (adattamento offline
> delle metriche della baseline numerica 03.9 verso il contratto endpoint 03.10). Non è un OK
> dell'intero harness né della sottofase, non chiude 03.9/03.10, non rende efficace alcun freeze,
> non autorizza chiamate, simulazioni o analisi sui run finali. Verifica in sola lettura.

## Intestazione obbligatoria

- **Modello esatto e provider/prodotto:** Anthropic — Claude Opus 4.8 (identificativo modello
  configurato: `claude-opus-4-8`); prodotto Claude in modalità Cowork (Claude Agent SDK). Il
  modello che serve il singolo turno può differire da quello configurato; qui è riportato
  l'identificativo configurato, come richiesto.
- **Livello di reasoning:** non esposto in modo verificabile a questa sessione → "non esposto".
- **ID task/sessione:** sessione `session_01WRDU2fmSdMwPx4ovj7npqU`
  (https://claude.ai/code/session_01WRDU2fmSdMwPx4ovj7npqU); sandbox
  `rcw-01wrdu2fmsdmwpx4ovj7npqu`. ID task interno non esposto.
- **Data e timezone:** 2026-09-14 18:30 CEST (UTC+02:00), Europe/Rome.
- **Percorso della copia isolata:**
  `/Users/luker/fot-tep/.worktrees/verifica-raccordo-caf5bfb` (worktree detached dedicato,
  distinto dalla finestra proprietaria `.worktrees/studio2-harness`). Per i test 03.9 sul main è
  stata usata la copia isolata gemella
  `/Users/luker/fot-tep/.worktrees/verifica-raccordo-main-c486eee` (detached a `c486eee`).
- **Commit verificato:** `caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae`.
- **Base del delta:** `51160872906feaa63c1fda5e9cf6e0fe8538fb16`.
- **Sorgente 03.9:** `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` (origin/main).

## Metodo

Contratto ricostruito dalle fonti primarie, non dal report. Letti integralmente:
`docs/MAINTENANCE.md`, `docs/prompts/Prompt_LLM.md`, `docs/prompts/Verifica_LLM.md`,
`CONTRATTO_RACCORDO_METRICHE.md`, `SPECIFICA_HARNESS.md` §8, e dal main `c486eee`
`SPECIFICA_BASELINE_NUMERICA.md`, `baseline.py`, `INTERFACE_CHECK.json`,
`BASELINE_FREEZE_rev003.json`; da `codex/studio2-piano-statistico-fix` il solo
`DELTA_HARNESS_03_10.md` per astensione/invalidità/denominatori; il `REPORT_RACCORDO_METRICHE.md`
(presente in `1ac06eb`, non nel delta) è stato letto solo come oggetto di verifica.

Integrità delle fonti fissate (SHA-256 ricalcolati sui blob di `c486eee`, coincidono con quelli
dichiarati nel contratto):

- `baseline.py` → `b1fe2a83b29b25760dd32df00a2178c5235f714273a194feb6cfe8a12ac74f22` ✅
- `SPECIFICA_BASELINE_NUMERICA.md` → `510b119ca54ac05225a7302dcf1b685cb4a778673a0f18d5a9a0e736078a6143` ✅
- `INTERFACE_CHECK.json` → `77cf4d8d3620bc739f58f48782e6846345d922463d4d93e34d281ea85d62a4f9` ✅
- `BASELINE_FREEZE_rev003.json` → `0312f416dfdbaf8984b2063df2c2e9d00e1737321b9a65dd7e32b0295a937ec8` ✅

Ambito del diff `5116087..caf5bfb`: **5 file, 484 inserimenti, 1 rimozione**, `git diff --check`
pulito. File toccati: `CONTRATTO_RACCORDO_METRICHE.md` (nuovo), `SPECIFICA_HARNESS.md` (mod.),
`metric_adapter.py` (nuovo), `metrics.py` (+1 riga), `test_harness.py` (mod., aggiunge i soli
6 metodi `MetricTests`). Coincide con l'ambito dichiarato.

## Riscontri per punto

**1 — Mapping accuracy→accuracy_all, n→total, abstentions→abstained.** ✅
`metric_adapter.py::adapt_baseline_metric` legge `source["accuracy"]`, `source["n"]`,
`source["abstentions"]` e li emette come `accuracy_all`, `total`, `abstained`; il blocco
`metric_interface.name_mapping` dichiara la stessa rinomina. Fonte primaria del nome sorgente:
`baseline_numerica/baseline.py::metric` (righe ~292–304 in `c486eee`) che emette esattamente
`n, correct, abstentions, non_abstained, accuracy, abstention_rate, accuracy_non_abstained`.
`INTERFACE_CHECK.json.metric_semantics.mappings_required` elenca le stesse tre coppie.

**2 — `non_abstained` preservato e uguale a `total - abstained`.** ✅
`adapt_baseline_metric` fallisce se `non_abstained != total - abstained` (e se `abstained > total`)
e poi copia il valore sorgente. `metrics.py::three_numbers` (riga 36) calcola
`non_abstained = total - abstained` nativamente. La sorgente `baseline.py::metric` pone
`non_abstained = len(rows) - abstentions`. Le tre definizioni coincidono.

**3 — `invalid=0` ammesso solo per la sorgente 03.9 valid-only.** ✅
`baseline.py::evaluate` scrive ogni riga con `"valid": "true"` e arresta l'esecuzione con
`RuntimeError` sugli input non validi; `SPECIFICA_BASELINE_NUMERICA.md` conferma «`valid=true`
sempre, perché un errore di input arresta l'esecuzione», e l'aggregato non contiene `invalid`.
`adapt_baseline_metric` esige l'insieme di campi esatto `_BASELINE_METRIC_FIELDS` (senza
`invalid`) e solo dopo la validazione dell'intero contratto valid-only emette `invalid: 0`;
un campo `invalid` in più fa fallire (verificato: vedi punto 5). Coerente con
`INTERFACE_CHECK.json` (`harness_additional_count: ["invalid"]`).

**4 — Nell'harness generale gli invalidi non sono corretti né astensioni e restano nel
denominatore di `accuracy_non_abstained`.** ✅
`metrics.py`: `_correct` richiede `valid is True and abstain is False`; `_abstained` richiede
`valid is True and abstain is True`; `invalid = sum(row.get("valid") is not True)`;
`non_abstained = total - abstained` (quindi comprende gli invalidi) e
`accuracy_non_abstained = correct / non_abstained`. Verificato indipendentemente su 10.626
configurazioni (`total 0..20`, tutte le ripartizioni corretti/astenuti/invalidi), incluso il caso
avverso in cui una riga invalida porta `abstain=true` e una label corrispondente: non viene
contata né come astensione né come corretta. Concorde con `DELTA_HARNESS_03_10.md`
(invalidità categoria autonoma, non astensione) e con `SPECIFICA_HARNESS.md` §8.

**5 — `null` solo con denominatore zero e rifiuto fail-closed di campi/conteggi/rapporti/strutture/
SHA-256 incoerenti.** ✅
`_ratio` impone `null` se e solo se il denominatore atteso è `None`, e rifiuta un valore non
`None` a denominatore zero, un `None` a denominatore non nullo, i booleani, i non finiti e ogni
valore diverso da quello ricomputato. `_count` rifiuta booleani, non interi e negativi.
`adapt_baseline_metrics_document` verifica `schema_version`, `status`, `statistical_unit`,
`independence_claim=false`, `three_numbers`, le due condizioni, le quattro popolazioni, la lista
cluster, l'identità/metadati cluster e l'unicità delle identità. `common.py::require_sha256`
solleva `HarnessError` su impronta errata prima di aprire il file; `load_json` è fail-closed.
Verificato indipendentemente: rifiuto su campo extra/`invalid` inatteso, campo mancante, conteggio
negativo/booleano, `non_abstained` incoerente, `correct > non_abstained`, `abstained > total`,
rapporto perturbato, `null`/non-`null` a denominatore errato, e su tutte le rotture a livello di
documento (schema, status, unità, independence, three_numbers, popolazione/condizione mancante,
cluster con campo extra o identità duplicata) e su SHA-256 errato.

**6 — Tutte le foglie `summary` e `clusters` adattate, senza arrotondamento o sostituzione dei tre
valori numerici sorgente.** ✅
`adapt_baseline_metrics_document` itera tutte le condizioni × popolazioni di `summary` e tutti gli
elementi di `clusters` (via `_adapt_cluster`). `_ratio`/`_count` restituiscono l'**oggetto
sorgente** dopo la validazione, non un ricalcolo. Verificato per identità (`is`) su 12.341
configurazioni valid-only (`total 0..40`): i tre valori numerici (`accuracy_all`,
`abstention_rate`, `accuracy_non_abstained`) dell'output sono lo stesso oggetto Python della
sorgente; nessun arrotondamento, nessuna riscrittura. Le foglie adattate coincidono con
`three_numbers` sulle stesse configurazioni.

**7 — Nessun consumer effettivo delle metriche omesso.** ✅
Ricognizione sul codice `studio2/fase03/harness`: l'unico lettore di un `metrics.json` 03.9 nel
namespace 03.10 è `metric_adapter.py::load_baseline_metrics` (grep: nessun altro riferimento a
`metrics.json`/`load_baseline_metrics`/`adapt_baseline_metric` fuori da adapter e test). Il
produttore 03.9 è `baseline.py::metric`→`evaluate`; il produttore nativo 03.10 è
`metrics.py::three_numbers`; l'unico consumatore del contratto a tre numeri è
`metrics.py::endpoint_statistic` (chiavi `accuracy_all`, `abstention_rate`,
`accuracy_non_abstained`), che l'adapter alimenta con gli stessi nomi. L'inventario del contratto
coincide con la ricognizione. Prima del delta non esisteva un lettore operativo: `INTERFACE_CHECK.json`
era solo un confronto documentale read-only.

**8 — Nessuna modifica fuori perimetro.** ✅
Il diff tocca solo i 5 file harness elencati. Nessuna modifica a `run_pilot.py`, ordine label
(`ordering.py`), D9, endpoint/guardie, configurazione modelli, pin 03.12/`schema_insight`,
walkthrough, piano statistico generale, dati o run finali. L'aggiunta a `metrics.py` è il solo
conteggio additivo `non_abstained`, che non altera `endpoint_statistic` (legge per chiave i tre
rapporti). `HARNESS_FREEZE.json` non è ripresentato come manifest del nuovo delta.

## Riesecuzione test

- `python3 -m unittest studio2.fase03.harness.test_harness.MetricTests` @`caf5bfb`: **9/9 OK**. ✅
- `python3 -m unittest studio2.fase03.baseline_numerica.test_baseline test_normal_dev_plan
  test_extract_normal_evidence` nel checkout main `c486eee`: **10/10 OK**. ✅
- Suite protocollo/guardie/harness @`caf5bfb`
  (`tests.test_protocol` + `tests.test_execution_guard` + `harness.test_harness`): **34 test,
  esito OK, skipped=2**. ✅ con una precisazione ⚠️ (sotto).
- Guardiano documentale `python3 docs/test_explanation.py` @`caf5bfb`: **35 test, 14 failure,
  1 skip, 0 errori**. ✅ Coincide con il numero preesistente noto (MAINTENANCE §5: 14 failure sui
  walkthrough v1). I 14 failure sono tutti in `UnifiedConversationChecks`
  (`test_condition_c_contract_and_caveats`, `test_one_flow_and_ordered_step_headings`,
  `test_step27_qwen_frozen_results_and_limitations`, `test_step27_qwen_protocol_stable_facts`),
  estranei al raccordo metriche e non toccati dal delta (che non modifica alcun file `docs/`).
  Non trasformati in PASS, non corretti.
- Verifica indipendente dell'equivalenza `baseline.py::metric` ↔ adapter ↔
  `metrics.py::three_numbers`: **12.341** configurazioni valid-only PASS (con identità degli
  oggetti numerici) + **10.626** configurazioni con invalidi PASS + tutte le rotture fail-closed
  dell'adapter e del gate SHA-256 PASS. ✅

### ⚠️ Precisazione sull'errore 03.12 noto e dichiarato estraneo

Il report dichiara, prima del delta, un errore estraneo in
`harness.test_harness.AdapterAndGuardTests::test_real_0312_adapter_when_checkout_is_available`,
causato dal fatto che il checkout 03.12 corrente non coincide più con il vecchio hash pinnato.
Nella copia isolata questo test **non si trasforma in PASS**: risulta `skipped`
('independent 03.12 checkout not available'), perché il test punta al percorso assoluto
`/Users/luker/fot-tep-schema-insight/studio2/fase03/schema_insight`, non montato nella sandbox di
verifica, quindi non eseguibile qui. Identificativo confermato coincidente; la causa (dipendenza
da un checkout 03.12 esterno pinnato) è coerente con quella dichiarata; il test è **preesistente**
e **non toccato** dal delta (il diff aggiunge a `test_harness.py` soltanto i 6 metodi
`MetricTests`). L'esito è ⚠️ per questo singolo elemento: noto ed estraneo, non riproducibile come
errore nell'ambiente isolato (skip), coerentemente con la richiesta di non trasformarlo in PASS né
correggerlo. Non incide sulla certificazione del delta. Analogamente
`test_real_036_release_inventory_when_checkout_is_available` è skip per checkout 03.6 non montato.

## Conclusione

Tutti gli otto controlli richiesti risultano ✅ sulla fonte primaria; l'unico ⚠️ riguarda il test
03.12 esterno, già dichiarato noto ed estraneo dal prompt stesso e non appartenente a questo
delta. Il raccordo metriche 03.9 → 03.10 nel commit
`caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae` è un adapter fail-closed, hash-pinned, che rinomina
senza ricalcolare, preserva `non_abstained`, dichiara `invalid=0` solo per il contratto valid-only,
tratta gli invalidi correttamente nel denominatore, adatta tutte le foglie e non modifica nulla
fuori perimetro.

**VERDETTO: OK** — limitatamente al delta `5116087..caf5bfb`. Non costituisce OK dell'intero
harness né della sottofase 03.9/03.10.
