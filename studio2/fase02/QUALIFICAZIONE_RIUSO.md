# Fase 02 — Qualificazione del riuso R1/R2

**Data:** 2026-09-12  
**Ambito:** sviluppo e baseline; nessun materiale storico è promosso a validazione o test.

## R1 — venti run fault F1/F8/F10/F13, batch 1–5

**Decisione:** **NO** alla sostituzione delle venti nuove simulazioni equivalenti previste per lo
sviluppo. I file restano utilizzabili soltanto come materiale storico già osservato per formulare
ipotesi, sviluppare la rappresentazione e documentare continuità col primo studio.

Controlli eseguiti:

- i 20 SHA-256 sono distinti e coincidono con le copie recuperabili elencate in
  `MANIFEST_CONSERVAZIONE.csv`;
- tutti i workbook hanno tempo monotono da 0 a 50 h, 3.001 campioni, passo mediano 1 min, 41 XMEAS
  e 12 XMV; dieci hanno anche `operational_cost`, colonna non usata dalle feature;
- il dataset dichiara lo snapshot upstream
  `309b944f35ac440ff0c70616947ffe723c766e14`, ma quell'oggetto non è disponibile nell'object
  database Git locale; seed, data di generazione e `Ts_base` effettivo dei workbook sono mancanti;
- Philox supera vettori noti, confronto col legacy e gate dei prefissi, ma questi controlli
  qualificano il nuovo generatore: non ricostruiscono la configurazione effettiva dei 20 file.

La condizione pre-specificata di identità del simulatore/configurazione non è quindi dimostrabile.
Autorizzare i 20 file «al posto» di nuovi run attribuirebbe loro un'equivalenza che le impronte e lo
schema non possono stabilire. Il loro uso storico rimane marcato **pre-specificato rispetto alla
presente decisione ma basato su dati già osservati**, mai confermativo.

## R2 — N1–N5 dal workbook Normal continuo

**Decisione:** **SÌ condizionato**, esclusivamente come `baseline_fit` congelata per riferimenti
per sensore e parametri robusti dello score A. Non è autorizzato come `cal_thr`, `far_ver`, test o
come cinque repliche indipendenti.

Identità del contenuto: SHA-256
`79883dd0aabbd034c15337b0be1ffca37e59ea7b32443a15d560b7feda2b2e6a`; i cinque blocchi da
50 h sono segmenti contigui dello stesso tratto da 250 h.

La guardia fissata prima del pilot confronta N1–N5 con dieci nuovi run Philox, stream 1000–1009,
dopo 20 h di burn-in. Tutte le metriche superano i limiti `scarto ≤ 0,5 MAD_storica` e rapporto MAD
in `[0,5; 2,0]`:

| Metrica | Scarto mediana / MAD storica | MAD pilot / MAD storica |
| --- | ---: | ---: |
| `abs_shift_sigma` | 0,109493 | 0,909157 |
| `abs_slope_sigma_h` | 0,124700 | 0,878447 |
| `residual_std_ratio` | 0,036861 | 0,938670 |
| `diff_std_ratio` | 0,017972 | 1,001357 |
| `S` | 0,389889 | 0,956200 |

Il risultato completo è in `validation/r2_guard_result_v2.json`. La guardia confronta posizione e
scala, non code e correlazioni temporali; inoltre non ricostruisce il `Ts_base` storico. Perciò R2
è una baseline di sviluppo disgiunta e congelata, non un campione scambiabile con i nuovi run. Se
in seguito l'impronta, il codice delle feature o i parametri congelati non coincidono, oppure una
verifica indipendente invalida il gate, l'autorizzazione decade e si applica il fallback già
stabilito: 100 run `baseline_fit_new`, `cal_thr=300`, `far_ver=150`.
