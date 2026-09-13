# REPORT — soglie Normal, sotto-fase 03.5

## Chiusura della finestra

1. **Specificazione.** Sono congelati `baseline_fit` U1/R2 N1–N5, score A, burn-in 20 h,
   350 `cal_thr` economici con `J~Unif{1..10}` e ultima finestra, 150 `far_ver` pieni con dieci
   finestre, trip-stop e fallback R2. Fonti e definizioni sono in `SPECIFICA_SOGLIE_NORMAL.md`.
2. **Guardia R2.** Riverifica su impronte correnti: `pass=true`, file indipendente byte-identico;
   ramo attivo 350+150. Dopo la correzione, `R2_GUARD_RECHECK.json` è stato prodotto da
   `recheck_r2_guard.py`, che ricalcola le cinque SHA-256, verifica 64 caratteri esadecimali,
   confronta i due risultati R2 della Fase 02 e riscrive l’attestazione. Il valore corretto di
   `tep_features_sha256` è `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c`.
3. **Piani e script.** Piani validati: 350+150, stream 40000–40349 e 50000–50149, smoke
   49900–49901; generatori J riproducibili e preflight anti-collisione. Il test standard-library
   passa; `pytest` non è installato nell’ambiente di sistema.
4. **Smoke.** Due run MATLAB completati senza trip: `cal_thr` 1/1 finestra, `far_ver` 10/10.
   Tempo reale 42,79 s; runtime manifest 10,00 s e 10,25 s. Verifica score indipendente passa
   con variante A in `SMOKE_CHECK.json`. La proiezione dal fault precedente è 0,2067275 s/h,
   cioè 5.707,75 s (95,13 min) per 27.610 h.
5. **Risultati e freeze.** Non disponibili: il batch è consegnato all’autore e non è stato
   eseguito. Pertanto non esistono ancora soglia, rango, FAR o `THRESHOLD_FREEZE.json`.
6. **Conservazione.** Non applicabile al batch non rientrato; al rientro si produrranno manifest
   aggregato, `ARTIFACT_STORAGE.json`, release dati e verifica per riscaricamento.
7. **Provenienza e stato.** Nessuna modifica a Fase 02, `phase_b`, `code` o `tep_*_v2`; nessuna
   chiamata a modelli linguistici. Le righe di `studio2/PROVENIENZA.md` e il walkthrough restano
   aperti fino alla verifica indipendente.

`python3 docs/test_explanation.py` è stato eseguito prima e dopo la sottofase: stesso esito,
35 test eseguiti, 14 failure preesistenti nelle verifiche del walkthrough/Qwen e 1 skip; nessuna
failure è riferita ai file di `soglie_normal`.

### Correzione pre-batch e cosa è rimasto fuori

La correzione è stata limitata a `R2_GUARD_RECHECK.json`, allo script di rigenerazione e al test.
La scansione con regex di 63 caratteri esadecimali su specifica, report, handoff, smoke check e
manifest smoke non ha trovato altri valori troncati. Restano fuori, come previsto, il batch, la
soglia, il rango, il FAR e `THRESHOLD_FREEZE.json`; non è stata eseguita alcuna simulazione.

### Decisioni che richiedono l’intervento dell’autore

Eseguire il comando in `HANDOFF_BATCH.md`, conservare la destinazione e restituire il lotto;
poi autorizzare la finestra di analisi dei risultati. In caso di trip/fallimento, fermarsi e
aprire la revisione prevista, senza sostituzioni.
