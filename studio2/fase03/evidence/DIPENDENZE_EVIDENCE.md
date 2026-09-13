# Sotto-fase 03.6 — dipendenze dell'estrazione evidence

Data: **2026-09-13**. Stato: **autorizzata dall'autore; pronta per l'estrazione reale**.
Nessuna simulazione, chiamata a modelli o valutazione del segnale è prevista in questa
sotto-fase.

## 1. Codice congelato importato

Lo script verifica tutti e quattro i file contro
`phase_b/PHASE_B_PROTOCOL_HASHES.json` **prima** di aggiungere `code/` a `sys.path` e
prima di eseguire qualunque import. Un mismatch arresta l'esecuzione.

| Funzione / costante | Modulo di origine | Commit | SHA-256 | Dipendenze effettive al caricamento | Ruolo |
| --- | --- | --- | --- | --- | --- |
| `XMEAS`, `load_case`, `compute_baseline_stats_from_blocks`, `analyze_case_windows` | `code/tep_features.py` | `3fd960a192bafacbaabce9471e3c3614d6b2d2db` | `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c` | stdlib, NumPy, pandas | schema delle 41 XMEAS, baseline sintetica nei test, feature numeriche per finestra |
| `load_config`, `load_development_baseline`, `verbalize_feature_table` | `code/tep_verbalize_v2.py` | `3fd960a192bafacbaabce9471e3c3614d6b2d2db` | `3a9129b6353cac6f8c9e02281282f137dd07885b1f882ca633ee9d6bf52393be` | importa `tep_features`; stdlib, NumPy, pandas; `load_development_baseline` richiede un reader XLSX | configurazione congelata, baseline N1–N5 se autorizzata, JSON e testo neutrali |
| configurazione V2 | `code/verbalizer_config_v2.json` | `3fd960a192bafacbaabce9471e3c3614d6b2d2db` | `552a0b8a9cf9e416de77daa7aca2d8dee152a2700bbfaab4ae5e039081712519` | caricata solo dal percorso esplicito passato a `load_config` | soglie e vocabolario di Fase A, dichiarati e non ridecisi |
| `signature_vector` | `code/evaluate_verbalizer_v2.py` | `3fd960a192bafacbaabce9471e3c3614d6b2d2db` | `972e06fa29bee5a58d57ca757bd158c5cddaa2f4ed12eb5c739169c7fef79a92` | al caricamento importa `tep_features` e `tep_verbalize_v2`, anche se il corpo della funzione usa solo `XMEAS`, NumPy e il JSON strutturato | firma deterministica 41 × 17 = 697 componenti in `[0,1]` |

Dipendenze runtime esterne: Python, NumPy, pandas e, soltanto per leggere la baseline
XLSX reale, `openpyxl`. Non viene importato alcun modulo da `phase_b/`.

## 2. Parametri e default resi espliciti

- `config`: sempre `code/verbalizer_config_v2.json`, mai il default del modulo;
- `fault_injection_h` operativo: **25.0 h**, passato come `start_h`; il valore legacy
  `10.0 h` presente nella configurazione non viene usato per delimitare i nuovi run;
- orizzonte: `[25.0, 65.0)`, quindi `end_h=65.0` e **40.0 h** post-innesco;
- `window_h=5.0`, passato esplicitamente ad `analyze_case_windows`;
- finestre attese: **8** per run, ognuna half-open e completa;
- run attesi: **40**, unità evidence attese: **320**;
- ordinamento: righe del manifest ordinate per `run_id`, finestre per inizio, variabili
  nell'ordine fisso `XMEAS-1` … `XMEAS-41`;
- ogni unità consumer-facing contiene una sola finestra; di conseguenza il JSON dichiara
  `n_windows=1` e la firma resta comunque lunga 697.

Le soglie sono le quattro costanti congelate di Fase A presenti nella configurazione:
`abs_shift_sigma=1.9695333234149084`,
`abs_slope_sigma_h=0.7468621213669596`,
`residual_std_ratio=1.3681613543196571`,
`diff_std_ratio=1.4051245046201666`. L'estrazione non le calibra né le modifica.

## 3. Baseline richiesta e decisione dell'autore

`load_development_baseline` richiede il workbook legacy Normal e costruisce le statistiche
di normalizzazione dai cinque blocchi contigui N1–N5 in `[0,250 h)`. Il registro
`studio2/PROVENIENZA.md` §4 autorizza U1/R2 come **`baseline_fit` soltanto** per lo score A,
con destinazione `fase02/validation/score_fit_legacy.json`; inoltre precisa che la
registrazione U2 delle feature non autorizza nuovi import o valori operativi.

La formulazione originaria non rendeva evidente che U1/R2 coprisse questo secondo uso.
L'autore ha deciso il 2026-09-13 di estendere U1/R2 con l'uso **U3**, limitatamente alla
normalizzazione e ai flag del verbalizzatore V2. Il dato resta
`code/tep_cache/mode1_normal_500.xlsx`, snapshot dichiarato `309b944f…`, SHA-256
`79883dd0…`, letto in `[0,250 h)`; è vietato usarlo per calibrazione, scelta di soglia,
verifica o test.

La baseline e le quattro soglie di `verbalizer_config_v2.json` sono trattate come coppia
indivisibile: le soglie restano quelle congelate contro N1–N5 in Fase A e non vengono
ricalibrate. La soglia dello score resta invece di competenza dei nuovi Normal della 03.5.

Condizione fail-closed: l'estrazione richiede il file canonico
`R2_GUARD_RECHECK.json` della 03.5, SHA-256
`7df0cef2d7854c689b79eb911fa01d1ede1625e22f0d3636c0ea5d678c9f33f8`, con
`guard_pass`, `parameters_and_code_current` e
`r2_guard_result_independent_byte_identical` veri. Se R2 decade o la 03.5 passa a
`baseline_fit_new`, tutte le evidence prodotte con U3 sono invalide e vanno rigenerate;
questa regola è scritta nel manifest e nel riepilogo dell'estrazione.

## 4. Esclusioni scientifiche

Questa sotto-fase non calcola separabilità, accuracy, rilevabilità, margini tra classi o
«quanto si vede» un fault; non sceglie soglie e non seleziona finestre in base al loro
contenuto. Fault, batch e stream restano in un indice evaluator-side separato. Testi e
JSON consumer-facing non contengono numero del fault, IDV, meccanismo, label o marca
«continuità/nuovo».
