# Specifica pre-esecuzione — soglie Normal (sotto-fase 03.5)

**Data:** 2026-09-13  
**Base:** `b7f359f` (`origin/main`)  
**Stato:** pre-specificata; nessun run di calibrazione o verifica è stato aperto.

Questa specifica implementa il registro autorevole di calibrazione. Le fonti sono riportate
accanto a ogni decisione; il registro prevale sul piano sperimentale.

## Disegno congelato

- `baseline_fit`: N1–N5 del file storico, con uso U1/R2 soltanto; score combinato variante A,
  parametri e riferimenti già congelati in `studio2/fase02/validation/score_fit_legacy.json`.
  Fonte: `docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md`, §P0, §§C0–C3 e §«Regola di
  selezione fra A e A′»; `studio2/PROVENIENZA.md`, §4.
- `cal_thr`: 350 run indipendenti. Ogni run estrae `J ~ Unif{1,…,10}` con dominio SHA-256
  `fot-tep/fase03/soglie_normal/cal_thr/j/v1`, simula `20 + 5J` h e usa l’ultima finestra
  half-open da 5 h (`[20+5(J−1), 20+5J)`). Fonte: decisione, §§P0 e gate della forma economica;
  `studio2/fase02/SPECIFICA_GENERAZIONE.md`, §§1 e 6.
- `far_ver`: 150 run indipendenti, ciascuno per 70 h totali (`20 + 50`), con dieci finestre
  half-open da 5 h. La finestra primaria è estratta uniformemente con dominio SHA-256
  `fot-tep/fase03/soglie_normal/far_ver/position/v1`; tutte le 1.500 finestre entrano nella
  metrica secondaria. Fonte: decisione, §P0 e §§C2/C4.
- RNG: Philox4×32-10, chiave `0x464f545445503032`, stream ID uguale all’indice del run e
  contatore di estrazione registrato. `Ts_base=0.0005 h`, uscita 1 min, MEX base qualificato,
  modello e stato iniziale identici alla qualifica Fase 02. Fonte: `SPECIFICA_GENERAZIONE.md`,
  §§1, 3–4, 7; `REPORT_FASE02.md`, §§3–4.
- Trip Normal o fallimento tecnico: arresto del lotto; nessun rerun selettivo, padding o
  sostituzione. Il tentativo e il motivo restano nel log. Fonte: `SPECIFICA_GENERAZIONE.md`, §3.
- Se la guardia R2 non fosse passata, il ramo già deciso sarebbe 100 `baseline_fit_new` + 300
  `cal_thr` + 150 `far_ver`, con `baseline_fit_new` a lunghezza piena. Fonte: decisione, §P0 e
  `validation/r2_guard_result_v2.json`.

## Soglia e verifica FAR

Per i 350 punteggi `S` di `cal_thr`, con `α=0.05`, si congela `k=ceil((350+1)(1−α))=334`,
cioè il quantile d’ordine crescente 334, e si applica esclusivamente `S > threshold`.
Il livello dichiarabile è `17/351 = 4.84%`; la Beta(17,334) è riportabile solo sotto continuità
di `S`, mentre i pareggi sono diagnostica e fanno decadere quella formulazione. Fonte: decisione,
§C2, §C3 e §«Formulazione corretta della garanzia».

La metrica FAR primaria conta un superamento per run nella posizione uniforme pre-specificata,
con intervallo esatto di Clopper–Pearson. La secondaria conta tutti i 1.500 punteggi e usa
bootstrap a livello di run per rispettare la dipendenza intra-run. La diagnostica riporta il FAR
separato per posizione 1,…,10; non modifica burn-in, soglia o inclusione delle finestre. Fonte:
decisione, §§P0 e C4.

## Contabilità e prestazione attesa

Il lotto attivo contiene **500 run**. Le ore simulate sono `350×20 + 5×ΣJ + 150×70`; con il
generatore deterministico del piano `ΣJ` è registrata nel manifest e, per il piano corrente,
vale 1.925, quindi **27.125 h** (`cal_thr`) + **10.500 h** (`far_ver`) = **37.625 h**.
La forma economica sostituisce 35.000 h piene per `cal_thr` senza cambiare la finestra di legge;
fonte: decisione, §P0.

La proiezione è calcolata dal precedente fault in termini di secondi per ora simulata, mai per
run: il report precedente registra il tempo complessivo e le ore effettivamente completate.
Il valore misurato nello smoke di questa sotto-fase aggiornerà la proiezione nel report e nel
handoff; il batch non viene lanciato in questa finestra.

## Stream riservati

`cal_thr`: **40000–40349**; `far_ver`: **50000–50149**; smoke: **49900–49901**. Sono disgiunti
da tutti gli stream elencati in `studio2/fase02/build_generation_plan.py` (qualifica, pilot,
baseline fallback e piani Fase 02) e da `30000–30039` dei fault. Gli indici di run sono registrati
come `uint64` nel piano e nel manifest. I dieci pilot (1000–1009) restano esclusi da ogni uso.

