# Report — candidato locale d'integrazione del raccordo metriche 03.9 → 03.10

**Stato: candidato d'integrazione preparato e testato in locale; verifica indipendente del nuovo
delta d'integrazione PENDING.** 03.9 e 03.10 restano APERTE; nessun freeze reso efficace; nessun
merge/push/tag; nessuna chiamata API/simulazione.

## 1. Base e candidato esatti

- **Base comune:** `e82b5a08bf642ad45f77e71832958207beb1181c` (non conteneva `studio2/fase03/harness/`).
- **Branch candidato:** `codex/studio2-raccordo-metriche-integrazione`.
- **Catena commit:** `e82b5a0` → `fae8ae8` (import) → `f4bca45` (acquisizione) → `f890a3d` (test) → `3360867` (documentazione).
- **Worktree on-disk:** `/Users/luker/fot-tep/.worktrees/integrazione-raccordo-metriche` (HEAD `3360867`).
- **Riferimenti d'origine:** delta tecnico verificato `caf5bfb`; report/manifest `1ac06eb`;
  acquisizione/registro OK `6c51330`; sorgente baseline 03.9 `c486eee` (= e82b5a0 per i 4 file pinnati).

## 2. Chiusura delle dipendenze — matrice file → origine → ruolo → dipendenze → copertura

### (a) Implementazione verificata (OK sul delta `5116087..caf5bfb`)

| File | Origine Git | Ruolo | Dipendenze | Copertura |
|---|---|---|---|---|
| `metric_adapter.py` | caf5bfb | adapter offline 03.9→03.10 (rinomina, no ricalcolo, fail-closed, hash-pinned) | `.common` (+ stdlib) | OK delta + 9/9 test mirati |
| `metrics.py` | caf5bfb | metriche endpoint 03.10 (delta: +`non_abstained` in `three_numbers`) | `.common` (+ stdlib) | OK delta + test mirati |
| `SPECIFICA_HARNESS.md` | caf5bfb | spec harness (§8 mapping/denominatori/invalidità) | — (doc) | OK delta [doc] |
| `CONTRATTO_RACCORDO_METRICHE.md` | caf5bfb | contratto autonomo + inventario consumer | — (doc) | OK delta [doc] |

### (b) Supporto preesistente NECESSARIO ma NON coperto dall'OK del solo delta

| File | Origine Git | Ruolo | Dipendenze | Copertura |
|---|---|---|---|---|
| `common.py` | caf5bfb | helper condivisi: `HarnessError`, `load_json`, `require_sha256`, `sha256_*`, `canonical_json` | stdlib | **NON coperto** dall'OK del solo delta; esercitato indirettamente dai 9 test mirati; **da verificare** nel nuovo delta |
| `__init__.py` | caf5bfb | package marker `studio2.fase03.harness` | — | banale |

### Prove e report/manifest (impronte preservate)

| File | Origine Git | Ruolo |
|---|---|---|
| `REPORT_RACCORDO_METRICHE.md` | 1ac06eb | report implementativo improntato (SHA-256 `8ab3ac62…`) |
| `METRIC_INTERFACE_CANDIDATE.json` | 1ac06eb | manifest candidato (stato `independent_verification: PENDING` conservato) |
| `PROMPT_VERIFICA_RACCORDO_METRICHE.md` | 1ac06eb | prompt di review del delta caf5bfb (storico) |
| `VERIFICA_RACCORDO_METRICHE.md` | 6c51330 | verbale indipendente (SHA-256 `0d907799…`; `VERDETTO: OK`) |
| `CONSEGNA_VERIFICA_RACCORDO_METRICHE.md` | 6c51330 | consegna del revisore |
| `CONSEGNA_RACCORDO_METRICHE_03_10.md` | 6c51330 | consegna dell'esecutore |
| `REGISTRO_OK_RACCORDO_METRICHE.md` | 6c51330 | registro OK sul solo delta |

### Lavoro nuovo d'integrazione (DA verificare nel nuovo delta)

| File | Origine | Ruolo | Dipendenze | Copertura |
|---|---|---|---|---|
| `test_metric_raccordo.py` | **NUOVO** (MetricTests + LABELS/AGENTS estratti verbatim da test_harness.py/inputs.py @caf5bfb) | test mirati del raccordo | common, metric_adapter, metrics | **NUOVO — da verificare** (9/9 OK in locale) |
| `docs/fot_walkthrough_conversazione_studio2.md/.html` (§4.10) | **NUOVO** hunk | documentazione | — | **NUOVO — da verificare** |

### (c) Componenti ESCLUSI di proposito (non importati)

| File / componente | Motivo dell'esclusione |
|---|---|
| `canary.py`, `guards.py`, `logging_v1.py`, `producer.py`, `sampling.py`, `ordering.py` | supporto harness generale non richiesto dalla chiusura runtime del raccordo (adapter/metrics dipendono solo da `common`) |
| `inputs.py` | input-building harness; il test mirato usa solo la costante `AGENTS`, riprodotta identica come literal, senza importare il modulo |
| `insight_adapter.py` | accoppiato al validatore/pin 03.12 (fuori perimetro; pin 03.12 non toccato) |
| `render.py` | importa `studio2.fase03.protocol` (esterno) e non è usato dal raccordo/test |
| `test_harness.py` (completo) | trascina l'intero package e i test `AdapterAndGuardTests` dipendenti da checkout fratelli (03.12/03.6); **conservato nella fonte caf5bfb**, non importato |
| `HARNESS_FREEZE.json`, `INTEGRATION_STATUS.json` | stato/freeze del candidato precedente `5116087`, non rappresentano questo delta |
| `PILOT_INPUT_SOURCES.pending.json`, `run_pilot.py`, endpoint/config, pin 03.12, ledger | componenti sperimentali/pilot estranei al raccordo metriche |
| `REPORT_HARNESS.md` | report harness generale, non il report del raccordo |

Nessuno stub o modulo vuoto è stato creato per far passare gli import.

## 3. Impronte preservate (importazione byte-identica)

Tutti i 13 file importati/acquisiti sono **byte-identici** ai blob dei riferimenti Git d'origine
(verifica blob-a-blob superata). SHA-256 di contenuto notevoli (dal manifest / verbale):
`metric_adapter.py` `967f998a…`, `metrics.py` `97f04274…`, `SPECIFICA_HARNESS.md` `f50fb290…`,
`CONTRATTO` `5c81586f…`, `REPORT` `8ab3ac62…`, verbale `0d90779981871b8c9ceaf2a729f97b371abb7297fb804dc4335ddf0f1bec0e80`.
La sorgente baseline 03.9 pinnata (`baseline.py`, `SPECIFICA_BASELINE_NUMERICA.md`,
`INTERFACE_CHECK.json`, `BASELINE_FREEZE_rev003.json`) è **identica** fra `e82b5a0` e `c486eee`.

## 4. Modifiche introdotte

- Nuovo package `studio2/fase03/harness/` con la sola chiusura minima del raccordo (import selettivo).
- Nuovo `test_metric_raccordo.py` (adattamento per riproducibilità locale; MetricTests estratti).
- Nuova §4.10 nel walkthrough (coppia MD/HTML), con nota che distingue delta OK / candidato
  d'integrazione non verificato / dipendenze aggiunte.
- Nessuna modifica a file preesistenti di `e82b5a0` fuori dalla coppia walkthrough (le uniche 2
  righe rimosse sono nella frase-indice del walkthrough, sostituita per inserire il rimando a §4.10).

## 5. Test e guardiano

- Test mirati `studio2.fase03.harness.test_metric_raccordo` sul checkout del candidato: **9/9 OK,
  0 skip, 0 error**, senza dipendenza da checkout fratelli. Coprono mapping, conteggi, denominatori,
  astensioni, invalidi, casi limite, rifiuti fail-closed e controllo SHA-256.
- `py_compile` di `common.py`, `metric_adapter.py`, `metrics.py`, `test_metric_raccordo.py`: OK.
- Guardiano `docs/test_explanation.py`: **prima (e82b5a0) e dopo (candidato) identici** — 35 test,
  14 failure, 1 skip, **stessi identificativi/subtest** (tutti in `UnifiedConversationChecks`,
  walkthrough v1, estranei al raccordo; non convertiti in PASS).

## 6. Limiti

- Il candidato è il **solo raccordo metriche** con dipendenze minime; **non** è l'harness 03.10
  completo. `common.py` è supporto preesistente non coperto dall'OK del solo delta.
- `test_metric_raccordo.py` e i hunk §4.10 sono **lavoro nuovo**: richiedono la verifica
  indipendente del nuovo delta d'integrazione (non una ripetizione della review di `caf5bfb`).
- `SPECIFICA_HARNESS.md` descrive l'harness generale; nel candidato molti suoi rimandi puntano a
  componenti esclusi (limite documentale noto, non runtime).
- Dipendenza normativa rev. 10 (`DELTA_HARNESS_03_10.md`, rif. stabile `6aaa5b3`, blob `780e08ae`,
  SHA-256 `e92661fe…`): **identificata, non importata**. Resta il residuo di raggiungibilità in
  `origin/main` (o nel base d'integrazione seriale); il piano statistico non è stato importato.
- Il vecchio pin 03.12 resta APERTO e fuori perimetro (i due skip del revisore ≠ l'errore locale
  dell'esecutore; nessun pin 03.12 toccato).

## 7. Dipendenze ancora da risolvere per l'integrazione seriale finale

1. Decidere se/quando portare l'**harness 03.10 completo** (guards, inputs, insight_adapter,
   logging_v1, producer, sampling, ordering, render, test_harness) — integrazione più ampia e
   distinta da questo raccordo minimo; comporta il pin 03.12 e la dipendenza `protocol`.
2. **Raggiungibilità rev. 10** in `origin/main` (o base seriale) per la dipendenza normativa.
3. **Sorgenti 03.6** raggiungibili in `origin/main` (prerequisito del freeze 03.9).
4. **Pin 03.12** aperto e separato.
5. Verifica indipendente del **nuovo delta d'integrazione** (import + test mirato + §4.10):
   completezza e comportamento nel nuovo checkout, non ripetizione della review `caf5bfb`.

## 8. Nota infrastrutturale

I commit sono stati costruiti in un repo di lavoro isolato fuori dal mount (dove i lockfile git
funzionano) e trasferiti nel repository come **oggetti additivi**; il worktree on-disk è stato poi
creato dal commit finale. `.lock`/`tmp_obj_*` residui sotto `.git` sono innocui in lettura (il mount
nega `unlink`); i lock/indici altrui non sono stati toccati.
