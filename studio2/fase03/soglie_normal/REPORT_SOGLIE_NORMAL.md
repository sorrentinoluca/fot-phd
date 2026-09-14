# REPORT — soglie Normal, sotto-fase 03.5

## Chiusura della finestra

1. **Specificazione.** Sono congelati `baseline_fit` U1/R2 N1–N5, score A, burn-in 20 h,
   350 `cal_thr` economici con `J~Unif{1..10}` e ultima finestra, 150 `far_ver` pieni con dieci
   finestre, trip-stop e fallback R2. Fonti e definizioni sono in `SPECIFICA_SOGLIE_NORMAL.md`.
2. **Guardia R2 e audit.** La guardia è `pass=true`, con risultato indipendente byte-identico;
   l’audit del lotto ha trovato 350+150 manifest, 500 workbook, zero trip/errori e zero file
   estranei. `R2_GUARD_RECHECK.json` è stato prodotto da `recheck_r2_guard.py`, che ricalcola le
   cinque SHA-256, verifica 64 caratteri esadecimali, confronta i risultati R2 Fase 02 e riscrive
   l’attestazione. Il valore corretto di `tep_features_sha256` è
   `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c`.
3. **Piani e script.** Piani validati: 350+150, stream 40000–40349 e 50000–50149, smoke
   49900–49901; generatori J riproducibili e preflight anti-collisione. Il test standard-library
   passa; `pytest` non è installato nell’ambiente di sistema.
4. **Smoke.** Due run MATLAB completati senza trip: `cal_thr` 1/1 finestra, `far_ver` 10/10.
   Tempo reale 42,79 s; runtime manifest 10,00 s e 10,25 s. Verifica score indipendente passa
   con variante A in `SMOKE_CHECK.json`. La proiezione dal fault precedente è 0,2067275 s/h,
   cioè 5.707,75 s (95,13 min) per 27.610 h.
5. **Soglia e FAR.** Freeze prima dell’analisi `far_ver`: soglia `13.623626738268857`, rango 334,
   n=350, regola `S > threshold`, commit `9507143`. FAR primario 11/150 = 7,333%, IC CP 95%
   [3,717%; 12,742%]. Secondario 108/1500 = 7,200%, SE bootstrap 0,751%, intervallo percentile
   95% [5,733%; 8,733%]. Diagnostica per posizione: 1:14, 2:10, 3:12, 4:6, 5:14, 6:8, 7:11,
   8:13, 9:10, 10:10 superamenti su 150.
6. **Conservazione.** Manifest di 515 file e release `studio2-fase03-normal-v1` verificata per
   riscaricamento: 515/515 file, zero mismatch; archivio SHA-256
   `bbcfd0c43a5fbda624deba62fea746150dda4a6d649e6372b8e118270277ac1d`.
7. **Provenienza e stato.** Nessuna modifica a Fase 02, `phase_b`, `code` o `tep_*_v2`; nessuna
   chiamata a modelli linguistici. Le righe di `studio2/PROVENIENZA.md` sono state aggiunte; il
   walkthrough resta fuori fino alla verifica indipendente. La non conformità di processo è che
   il launcher ha generato fisicamente `far_ver` prima del freeze analitico, come previsto
   dall’handoff; il freeze e l’analisi sono però stati eseguiti nell’ordine vincolante senza
   leggere `far_ver` prima del freeze.

`python3 docs/test_explanation.py` è stato eseguito prima e dopo la sottofase: stesso esito,
35 test eseguiti, 14 failure preesistenti nelle verifiche del walkthrough/Qwen e 1 skip; nessuna
failure è riferita ai file di `soglie_normal`.

### Correzione pre-batch e cosa è rimasto fuori

La correzione è stata limitata a `R2_GUARD_RECHECK.json`, allo script di rigenerazione e al test.
La scansione con regex di 63 caratteri esadecimali su specifica, report, handoff, smoke check e
manifest smoke non ha trovato altri valori troncati. Restano fuori, come previsto, il batch, la
soglia, il rango, il FAR e `THRESHOLD_FREEZE.json`; non è stata eseguita alcuna simulazione.

### Cosa è rimasto fuori e decisioni che richiedono l’intervento dell’autore

Restano fuori il walkthrough e la verifica indipendente della finestra; non è stata modificata la
soglia dopo il freeze. Serve l’intervento dell’autore per autorizzare la verifica indipendente e
decidere come riportare nel paper la non conformità temporale del launcher.

## Addendum — confronto FAR atteso/osservato e nota di processo

**Data:** 2026-09-14

Per la verifica primaria il registro prevede, con FAR nominale del 5% e 150 run indipendenti,
un conteggio atteso nell’intervallo **3–12 superamenti**, con probabilità **0,947**. Sono stati
osservati **11/150 superamenti**, pari a **7,333%**: il conteggio è quindi nell’intervallo
pre-specificato e l’intervallo Clopper–Pearson al 95% è **[3,717%; 12,742%]**, includendo il 5%
nominale. Il risultato è compatibile con il controllo previsto; non costituisce una prova di
uguaglianza esatta al 5%.

La verifica secondaria, basata sulle 1.500 finestre e con bootstrap a livello di run, dà
**108/1500 = 7,200%**, SE **0,751%**, IC percentile 95% **[5,733%; 8,733%]**. La diagnostica
per posizione varia da 4,000% (posizione 4) a 9,333% (posizioni 1 e 5), senza modifica della
soglia congelata.

Nota di processo: il launcher ha generato fisicamente i file `far_ver` nello stesso processo
subito dopo `cal_thr`, prima che l’analisi potesse creare `THRESHOLD_FREEZE.json`; questo non
rispetta l’ordine scientifico previsto dall’handoff. La non conformità è stata registrata e non
è stata nascosta né corretta retroattivamente. L’ordine analitico successivo è stato rispettato:
audit e score `cal_thr`, freeze della soglia, ricontrollo del sigillo, quindi apertura e analisi
dei contenuti `far_ver`; nessuna soglia è stata modificata dopo l’analisi FAR. La decisione
sull’accettabilità di questa deviazione di processo resta aperta alla verifica indipendente.
