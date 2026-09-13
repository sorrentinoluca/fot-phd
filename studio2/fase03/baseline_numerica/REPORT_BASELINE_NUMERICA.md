# Sotto-fase 03.9 — report baseline numerica

**Completata per specifica e codice; artefatto reale pending.** Data: 2026-09-14. Nessuna
simulazione, nessuna chiamata a modelli linguistici e nessuna valutazione su dati reali.

## 1. Riassunto e risultati

La decisione dell'autore è attuata come lotto `normal_dev`: 40 run, cinque assegnati a ciascun
agente prima della generazione, stream 60000–60039, 65 h per run, otto finestre `[25,65)` e uso
solo di sviluppo. Sono **2.600 h simulate**; a 0,2067275 s/h la proiezione è **537,49 s = 8,96
min**, esclusi avvio, audit, estrazione e pubblicazione. L'alternativa U4/N1–N5 è respinta dalla
revisione 7: avrebbe evitato simulazioni, ma avrebbe sovrapposto dati della trasformazione e
osservazioni di sviluppo e richiesto una nuova autorizzazione di riuso.

La regola locale Normal è fissata prima dei dati: run di indice 1 e finestra 1 `[25,30)` per ogni
agente. `normal_dev` resta dipendente da N1–N5/soglie V2 via U3 per normalizzazione e flag; non usa
N1–N5 come esempi o osservazioni di prototipo. Alla 03.14 è passato il vincolo 320 finestre Normal
contro 40 per fault, da trattare nella ricetta FedAvg prima dell'addestramento.

La baseline è specificata e implementata con due varianti: nove prototipi globali e due prototipi
locali per agente (Normal + fault locale). Ogni prototipo è la media aritmetica di tutte le finestre
fissate; classificazione a L1 media minima; pareggio entro `1e-12` produce astensione; nessuna
soglia di distanza; nessun fallback globale per classi locali assenti. Il codice legge firme già
estratte, verifica hash/dimensione/range e non importa codice congelato.

Non sono stati creati `PROTOTYPES.json` o risultati reali: mancano il batch e le evidence Normal.
`BASELINE_FREEZE.json` è correttamente `pending_normal_dev_and_independent_verification`, non un
freeze efficace.

## 2. Formato di uscita

Le righe evaluator-side seguono la proposta 03.8:
`condition,agent_id,physical_case_id,true_pseudolabel,abstain,predicted_label,valid,is_correct,population`.
Le predizioni non valutate sono scritte prima dell'unione con la verità. `metrics.json` riporta per
aggregato e cluster fisico i tre numeri `accuracy`, `abstention_rate`,
`accuracy_non_abstained`, i conteggi grezzi e `independence_claim=false`.

La 03.10 non ha pubblicato un branch o formato definitivo. L'interfaccia è quindi concordata con
la 03.8 ma **pending** verso la 03.10; va confrontata prima del freeze, senza modificare file 03.10
esistenti.

## 3. Test eseguiti

`python3 -m unittest studio2.fase03.baseline_numerica.test_baseline studio2.fase03.baseline_numerica.test_normal_dev_plan -v`:
**Ran 7 tests — OK**. Copertura: fixture sintetica end-to-end, byte-determinismo, controllo hash
fail-closed, pareggio→astensione, classi locali assenti senza fallback, tre numeri, assenza di
F-number, piano 40×5 e disgiunzione degli stream.

Il preflight con bypass esclusivamente di test accetta 40 righe e 60000–60039. Senza bypass si
arresta come previsto: `origin/main` non contiene `a572d1c`. Il batch non è stato avviato.

`docs/test_explanation.py` prima e dopo: `Ran 35 tests` — **FAILED (failures=14, skipped=1)**;
conteggio invariato e interamente preesistente.

## 4. File toccati

- `studio2/fase03/baseline_numerica/SPECIFICA_NORMAL_DEV.md` — decisione e ruoli del lotto.
- `studio2/fase03/baseline_numerica/plans/normal_dev.csv` — 40 assegnazioni e stream immutabili.
- `studio2/fase03/baseline_numerica/build_normal_dev_plan.py` — generazione/verifica deterministica.
- `studio2/fase03/baseline_numerica/preflight_normal_dev.py` — collisioni, destinazione e guardia rev. 7.
- `studio2/fase03/baseline_numerica/generate_normal_dev_runs.m` — delega al generatore qualificato.
- `studio2/fase03/baseline_numerica/launch_normal_dev_batch.sh` — launcher non eseguito.
- `studio2/fase03/baseline_numerica/HANDOFF_NORMAL_DEV.md` — blocco, comando e consegna del batch.
- `studio2/fase03/baseline_numerica/SPECIFICA_BASELINE_NUMERICA.md` — protocollo pre-osservazione.
- `studio2/fase03/baseline_numerica/baseline.py` — build, classificazione, valutazione e manifest.
- `studio2/fase03/baseline_numerica/test_baseline.py` — test sintetici e negativi.
- `studio2/fase03/baseline_numerica/test_normal_dev_plan.py` — test del piano e degli stream.
- `studio2/fase03/baseline_numerica/__init__.py` — package nuovo.
- `studio2/fase03/baseline_numerica/BASELINE_FREEZE.json` — stato pending e impronte.
- `studio2/fase03/baseline_numerica/REPORT_BASELINE_NUMERICA.md` — questo report.
- `studio2/PROVENIENZA.md` — nuova sezione 03.9, incluso il nuovo uso operativo U3.

Non sono stati modificati piano, walkthrough, `phase_b/`, `code/`, `protocol.py`, `run_pilot.py`,
`prepare_gate.py` o schemi esistenti.

## 5. Modello e profilo

OpenAI Codex (GPT-5), profilo **implementativo**, ragionamento medio, test eseguiti. Il batch resta
profilo **esecutivo-batch** ed è consegnato all'autore o a una finestra dedicata.

## 6. Cosa resta aperto

1. Pubblicare `a572d1c` in `origin/main`; fino ad allora il batch è non lanciabile.
2. Eseguire, auditare e conservare `normal_dev` nella release proposta.
3. Estrarre e verificare le 320 evidence Normal con U3/R2 e indice evaluator-side per agente.
4. Costruire `PROTOTYPES.json`/manifest, aggiornare il freeze in un file revisionato e svolgere la
   verifica indipendente.
5. Confrontare lo schema d'uscita con la futura interfaccia 03.10 e adottarla se differisce.
6. Valutare sui run di test solo dopo la 03.11 e applicare il protocollo statistico quando non sarà
   più pending.

## 7. Commit

Creati tre cambiamenti separati prima di questo report:

- `0a38e2c` — specifica, piano e handoff `normal_dev`;
- `8eed658` — specifica pre-osservazione della baseline;
- `c12f29a` — codice e test sintetici.

Il cambiamento di chiusura proposto contiene freeze pending, provenienza e report con messaggio
`studio2(baseline): registra freeze pending e report della 03.9`.

## Fonti lette e costo

Letti i prompt operativi, MAINTENANCE §1/§2/§8, walkthrough studio2 §0/§0.1 e mappa fasi, piano
§6.7/§8.5/§9.3/D10 e revisione 7, piano statistico 03.8 §2–§3/§6, evidence 03.6 e relativo
estrattore/manifest/release, pseudolabel e assegnazione 03.7, specifica/launcher 03.5, specifica
fault e pattern C02B con freeze. Costo approssimativo: 25–35 mila token di testo/codice; test
sintetici sotto un secondo, test documentale circa un secondo.
