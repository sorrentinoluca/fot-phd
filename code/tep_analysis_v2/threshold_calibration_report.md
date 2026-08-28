# Normal-only threshold calibration report

## Perimetro e metodo

- Dataset commit: `309b944f35ac440ff0c70616947ffe723c766e14`.
- Sono stati caricati esclusivamente i 15.000 campioni Normal in `[0, 250 h)`, cioè N1–N5.
- Ogni blocco da 50 h è stato diviso in 10 finestre non sovrapposte da 5 h: 50 finestre totali, 300 campioni per finestra.
- Per ogni finestra di Ni, la baseline usa soltanto gli altri quattro blocchi development.
- Ogni score è il massimo sulle 41 XMEAS, quindi incorpora la molteplicità tra sensori.
- Calibrazione: `k = ceil((n+1)*(1-alpha)) = ceil(51*0.95) = 49`; soglia = 49° valore ordinato (1-based). Poiché `49 <= 50`, non è stato necessario alcun clipping. Se k fosse maggiore di n, non verrebbe sostituito silenziosamente con n.
- Una candidatura richiede superamento stretto: `score > threshold`.

## Soglie normal-only congelate per questa revisione

| Feature | Soglia |
|---|---:|
| `abs_shift_sigma` | 1.969533323 |
| `abs_slope_sigma_h` | 0.746862121 |
| `residual_std_ratio` | 1.368161354 |
| `diff_std_ratio` | 1.405124505 |

## Distribuzioni degli score Normal

Median è la media dei due valori centrali; Q1, Q3 e P95 usano il nearest-rank esplicito.

| Score | Median | Q1 | Q3 | P95 | Maximum | Soglia k=49 |
|---|---:|---:|---:|---:|---:|---:|
| max `abs_shift_sigma` | 0.716284 | 0.536476 | 0.975455 | 1.598838 | 2.005051 | 1.969533 |
| max `abs_slope_sigma_h` | 0.407610 | 0.329686 | 0.529553 | 0.665240 | 0.792485 | 0.746862 |
| max residual_std_ratio | 1.169999 | 1.124664 | 1.238185 | 1.336248 | 1.457493 | 1.368161 |
| max diff_std_ratio | 1.242955 | 1.190042 | 1.307870 | 1.373978 | 1.473045 | 1.405125 |
| max raw_std_ratio (descrittivo) | 1.198117 | 1.153311 | 1.265805 | 1.390726 | 1.510657 | — |

## False-positive diagnostico sul Normal development

| Candidatura | Finestre | Percentuale |
|---|---:|---:|
| Level | 1/50 | 2.0% |
| Trend | 1/50 | 2.0% |
| Residual variability | 1/50 | 2.0% |
| Diff | 1/50 | 2.0% |
| Rapid variability (residual e diff sulla stessa variabile) | 0/50 | 0.0% |
| Qualsiasi anomalia primaria | 3/50 | 6.0% |

Nota: alpha=0.05 è applicato separatamente a ciascuna feature. Non controlla il family-wise error sulla simultaneità delle quattro feature; per questo l’unione produce un tasso diagnostico diverso dal 5%.

## Applicazione ai fault development (soglie non ritoccate)

| Fault | Level | Trend | Residual | Diff | Rapid | Any |
|---|---:|---:|---:|---:|---:|---:|
| F1 | 100.0% | 70.0% | 50.0% | 17.5% | 12.5% | 100.0% |
| F8 | 100.0% | 100.0% | 100.0% | 77.5% | 77.5% | 100.0% |
| F10 | 87.5% | 95.0% | 100.0% | 87.5% | 87.5% | 100.0% |
| F13 | 100.0% | 100.0% | 100.0% | 92.5% | 92.5% | 100.0% |

### Prima finestra `[10,15 h)` vs regime tardivo `[40,50 h)`

| Fault | Periodo | Level | Trend | Residual | Diff | Rapid |
|---|---|---:|---:|---:|---:|---:|
| F1 | Prima | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| F1 | Tardivo | 100.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| F8 | Prima | 100.0% | 100.0% | 100.0% | 60.0% | 60.0% |
| F8 | Tardivo | 100.0% | 100.0% | 100.0% | 80.0% | 80.0% |
| F10 | Prima | 60.0% | 100.0% | 100.0% | 80.0% | 80.0% |
| F10 | Tardivo | 90.0% | 90.0% | 100.0% | 90.0% | 90.0% |
| F13 | Prima | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% |
| F13 | Tardivo | 100.0% | 100.0% | 100.0% | 80.0% | 80.0% |

### Persistenza massima osservata per una singola variabile

| Fault | Level stesso segno | Trend stesso segno | Drift coerente | Residual | Diff | Rapid |
|---|---:|---:|---:|---:|---:|---:|
| F1 | 8 | 1 | 1 | 4 | 1 | 1 |
| F8 | 5 | 5 | 3 | 8 | 6 | 6 |
| F10 | 6 | 6 | 2 | 8 | 8 | 8 |
| F13 | 8 | 5 | 3 | 8 | 8 | 8 |

### Coerenza del segno della variabile dominante per finestra

| Fault | Shift +/− | Coerenza shift | Slope +/− | Coerenza slope |
|---|---:|---:|---:|---:|
| F1 | 40/0 | 100.0% | 16/12 | 57.1% |
| F8 | 16/24 | 60.0% | 17/23 | 57.5% |
| F10 | 21/14 | 60.0% | 16/22 | 57.9% |
| F13 | 11/29 | 72.5% | 27/13 | 67.5% |

### Variabili persistenti in almeno 4/5 batch

Per level, la persistenza richiede almeno due finestre consecutive positive con
lo stesso segno. Per drift richiede inoltre che lo `shift_sigma`, equivalente
alla media normalizzata della finestra, evolva nella direzione della slope. Per
residual, diff e rapid richiede almeno due finestre consecutive positive. La
lista indica persistenza in un qualunque tratto post-injection, non
necessariamente nel regime tardivo.

**F1**
- level: XMEAS-1 (5/5), XMEAS-13 (5/5), XMEAS-16 (5/5), XMEAS-18 (5/5), XMEAS-27 (5/5), XMEAS-28 (5/5), XMEAS-33 (5/5), XMEAS-34 (5/5), XMEAS-38 (5/5), XMEAS-4 (5/5), XMEAS-7 (5/5)
- drift: nessuna
- residual: XMEAS-1 (5/5), XMEAS-10 (5/5), XMEAS-11 (5/5), XMEAS-13 (5/5), XMEAS-15 (5/5), XMEAS-16 (5/5), XMEAS-18 (5/5), XMEAS-20 (5/5), XMEAS-21 (5/5), XMEAS-22 (5/5), XMEAS-23 (5/5), XMEAS-24 (5/5), XMEAS-25 (5/5), XMEAS-28 (5/5), XMEAS-29 (5/5), XMEAS-30 (5/5), XMEAS-31 (5/5), XMEAS-34 (5/5), XMEAS-5 (5/5), XMEAS-6 (5/5), XMEAS-7 (5/5), XMEAS-35 (4/5)
- diff: nessuna
- rapid: nessuna

**F8**
- level: XMEAS-13 (5/5), XMEAS-16 (5/5), XMEAS-20 (5/5), XMEAS-22 (5/5), XMEAS-28 (5/5), XMEAS-30 (5/5), XMEAS-34 (5/5), XMEAS-38 (5/5), XMEAS-7 (5/5), XMEAS-1 (4/5), XMEAS-11 (4/5), XMEAS-18 (4/5), XMEAS-24 (4/5), XMEAS-25 (4/5), XMEAS-27 (4/5), XMEAS-31 (4/5), XMEAS-33 (4/5)
- drift: XMEAS-11 (5/5), XMEAS-18 (5/5), XMEAS-20 (5/5), XMEAS-22 (5/5), XMEAS-1 (4/5), XMEAS-10 (4/5), XMEAS-21 (4/5), XMEAS-25 (4/5), XMEAS-29 (4/5), XMEAS-31 (4/5), XMEAS-35 (4/5), XMEAS-4 (4/5)
- residual: XMEAS-1 (5/5), XMEAS-10 (5/5), XMEAS-11 (5/5), XMEAS-12 (5/5), XMEAS-13 (5/5), XMEAS-14 (5/5), XMEAS-15 (5/5), XMEAS-16 (5/5), XMEAS-18 (5/5), XMEAS-20 (5/5), XMEAS-21 (5/5), XMEAS-22 (5/5), XMEAS-23 (5/5), XMEAS-24 (5/5), XMEAS-25 (5/5), XMEAS-28 (5/5), XMEAS-29 (5/5), XMEAS-30 (5/5), XMEAS-31 (5/5), XMEAS-34 (5/5), XMEAS-35 (5/5), XMEAS-38 (5/5), XMEAS-5 (5/5), XMEAS-6 (5/5), XMEAS-7 (5/5), XMEAS-4 (4/5)
- diff: XMEAS-10 (5/5), XMEAS-31 (5/5), XMEAS-1 (4/5), XMEAS-29 (4/5)
- rapid: XMEAS-10 (5/5), XMEAS-31 (5/5), XMEAS-1 (4/5), XMEAS-29 (4/5)

**F10**
- level: XMEAS-18 (5/5)
- drift: XMEAS-18 (4/5)
- residual: XMEAS-18 (5/5)
- diff: XMEAS-18 (5/5)
- rapid: XMEAS-18 (5/5)

**F13**
- level: XMEAS-10 (5/5), XMEAS-11 (5/5), XMEAS-13 (5/5), XMEAS-15 (5/5), XMEAS-16 (5/5), XMEAS-18 (5/5), XMEAS-20 (5/5), XMEAS-21 (5/5), XMEAS-22 (5/5), XMEAS-24 (5/5), XMEAS-27 (5/5), XMEAS-28 (5/5), XMEAS-30 (5/5), XMEAS-33 (5/5), XMEAS-34 (5/5), XMEAS-38 (5/5), XMEAS-5 (5/5), XMEAS-6 (5/5), XMEAS-7 (5/5)
- drift: XMEAS-20 (5/5), XMEAS-22 (5/5), XMEAS-24 (5/5), XMEAS-30 (5/5), XMEAS-34 (5/5), XMEAS-10 (4/5), XMEAS-11 (4/5), XMEAS-13 (4/5), XMEAS-15 (4/5), XMEAS-16 (4/5), XMEAS-18 (4/5), XMEAS-21 (4/5), XMEAS-28 (4/5), XMEAS-33 (4/5), XMEAS-35 (4/5), XMEAS-38 (4/5), XMEAS-7 (4/5)
- residual: XMEAS-1 (5/5), XMEAS-10 (5/5), XMEAS-11 (5/5), XMEAS-12 (5/5), XMEAS-13 (5/5), XMEAS-14 (5/5), XMEAS-15 (5/5), XMEAS-16 (5/5), XMEAS-18 (5/5), XMEAS-20 (5/5), XMEAS-21 (5/5), XMEAS-22 (5/5), XMEAS-24 (5/5), XMEAS-25 (5/5), XMEAS-28 (5/5), XMEAS-29 (5/5), XMEAS-30 (5/5), XMEAS-31 (5/5), XMEAS-33 (5/5), XMEAS-34 (5/5), XMEAS-35 (5/5), XMEAS-38 (5/5), XMEAS-5 (5/5), XMEAS-6 (5/5), XMEAS-7 (5/5), XMEAS-8 (5/5), XMEAS-9 (5/5), XMEAS-36 (4/5)
- diff: XMEAS-10 (5/5), XMEAS-13 (5/5), XMEAS-16 (5/5), XMEAS-7 (5/5)
- rapid: XMEAS-10 (5/5), XMEAS-13 (5/5), XMEAS-16 (5/5), XMEAS-7 (5/5)

## Verifica esplicita F1 / XMEAS-1

- Shift persistente: PASS — 40/40 finestre positive, persistente in 5/5 batch, segno positivo.
- A livello di sistema, nella prima finestra almeno una variabile è positiva per residual, diff e rapid in 5/5 batch; nelle ultime due finestre nessuna delle tre candidature compare in alcun batch.
- Prima finestra: residual positivo in 5/5 batch; diff positivo in 1/5 batch.
- Regime tardivo: residual positivo in 0/10 finestre; diff positivo in 0/10; rapid positivo in 0/10.
- Assenza di variabilità tardiva persistente su XMEAS-1: PASS.

La firma F1 richiesta è quindi verificata senza adattare le soglie ai fault.
La componente diff iniziale è però multivariabile: non è attribuita
coerentemente a XMEAS-1 nei cinque batch.

## Problemi metodologici e limiti

- Le stesse 50 finestre sono usate per calibrazione e diagnostica false-positive: il conteggio è descrittivo, non una stima out-of-sample.
- La calibrazione è per-feature e corregge la simultaneità tra 41 sensori, ma non la simultaneità tra le quattro feature.
- Le finestre Normal adiacenti dello stesso blocco non sono indipendenti; la garanzia conformal exchangeability è quindi approssimata, non dimostrata.
- Con n=50 il rank 49 produce una calibrazione discreta e conservativa per singola feature: con superamento stretto, normalmente una sola finestra supera la soglia.
- `rapid` richiede residual e diff sopra soglia sulla stessa variabile; non autorizza i termini “oscillazione” o “periodicità”.
- Nessun batch validation/test è stato aperto. Le soglie devono restare immutate durante la successiva validazione.
