# OK — Fase 02 verificata; pubblicazione dell'archivio dati ancora in corso

**Verdetto dopo il riesame:** **OK** per chiudere la Fase 02, aggiornare la documentazione e avviare
la Fase 03. I risultati numerici e i conteggi dichiarati reggono alla ricostruzione indipendente;
il freeze esteso copre ora gli input e le dipendenze contestati. La pubblicazione dei 224 workbook
nel repository dati pubblico resta un adempimento operativo esplicito: non blocca la Fase 03, che è
il capability pilot e non legge questi dati, ma deve concludersi ed essere verificata per hash prima
del congelamento definitivo che pretenda la riproducibilità da una nuova clone.

## 1 · Chi, quando, su cosa

| Voce | Valore |
| --- | --- |
| Data | 2026-09-12 |
| Finestra | task Codex distinta dalla finestra che ha prodotto `REPORT_FASE02.md` |
| Modello | Codex, modello GPT-5 fornito dalla sessione |
| Modalità | sola lettura sugli artefatti; unica scrittura: questo file. Compilazione e smoke di verifica eseguiti in `/tmp`, fuori dal repository |
| Report verificato | `studio2/fase02/REPORT_FASE02.md` |
| HEAD | `93f33fc932a0bf547483cb0d13c59373e274ae1a` |

## 2 · Esiti sulle affermazioni principali

| Punto | Esito | Fonte primaria e riscontro |
| --- | :---: | --- |
| Conservazione | ✅ | `MANIFEST_CONSERVAZIONE.csv` e i file sorgente/destinazione: **78** percorsi logici, **74** contenuti distinti, SHA-256 e dimensioni coincidenti, inode distinti, ZIP XLSX validi; **152.308.644** byte logici e **144.745.600** distinti. |
| Provenienza R1/R2 | ✅ | `studio2/PROVENIENZA.md`, `QUALIFICAZIONE_RIUSO.md` e SHA del workbook Normal: R1 è respinto come sostituzione; R2 è autorizzato solo come `baseline_fit`, esplicitamente pre-specificato ma basato su dati già osservati. Seed, data e `Ts_base` mancanti non sono stati inventati. |
| Score | ✅ | Ricalcolo da `code/tep_cache/mode1_normal_500.xlsx` con `combined_score.py`: variante **A**, dominanza massima **0,48**, otto parametri robusti e 4 × 41 = **164** riferimenti per sensore, coincidenti con `score_fit_legacy.json`. |
| Burn-in | ✅ | Ricalcolo dai dieci workbook in `validation/data_v2/burnin_qual/`: risultato identico a `burn_in_result_v2.json`; passano 20 h e 30 h e la regola seleziona **20 h**. |
| Philox–legacy | ✅ | Ricalcolo sui 10 + 10 workbook: risultato identico a `generator_comparison_result_v2.json`; tutte le cinque metriche e i numeri riportati nel report coincidono. |
| Prefissi | ✅ | Ricalcolo sui 110 workbook definitivi: risultato identico a `prefix_result_v2.json`; **100/100**, differenze massime 0, zero fallimenti dei contatori e J10 = full per 10/10 stream. |
| Guardia R2 | ✅ | Ricalcolo sui dieci pilot: risultato identico a `r2_guard_result_v2.json`; passano le quattro famiglie e `S`, inclusi 0,389889 MAD e rapporto MAD 0,956200 per `S`. |
| Build e smoke | ✅ | `philox_kat.c` compilato C99 con `-Wall -Wextra -Werror`: tre KAT, replay e stream smoke PASS. Il MEX è stato ricompilato con MATLAB R2025b ARM e Xcode/Clang in `/tmp`; uno smoke in memoria sullo stream 999999 ha riprodotto esattamente `validation/data/instrumented_smoke/implementation-smoke.xlsx` (4 × 54, differenza massima 0, contatore finale 308616). |
| Integrità dei risultati | ✅ | I 12 manifest contano **293** output; tutti i file esistono e hanno l'hash dichiarato. I quattro manifest Philox definitivi contano **140** righe e superano hash, stato, durata, forma, chiave, stream e contatore. Le 50 esecuzioni da 70 h riproducono 9,206 s di mediana, 8,916–14,672 s; le 20 full/J10 riproducono 9,320 s, 8,916–10,426 s. |
| Budget | ✅ | Dal piano autorevole: 150 + 40 + 350 + 150 + 54/72 + 6 = **750/768**; sottraendo i 150 ruoli diagnostici completati restano **600/618**. Le 293 esecuzioni fisiche includono ripetizioni tecniche e non cambiano il budget scientifico. |

## 3 · Controlli richiesti da `Verifica_LLM.md`

| # | Controllo | Esito | Riscontro |
| :---: | --- | :---: | --- |
| 1 | Fonti ricostruite da zero | ✅ | Numeri ricalcolati dai workbook, dai manifest, dal codice e dai JSON; non assunti dal report. Dopo la correzione, gli hash correnti dei **40 file** e dei cinque manifest elencati in `PRECALIBRATION_FREEZE.json` coincidono: **45/45**. |
| 2 | Perimetro congelato | ✅ | `git diff HEAD` è vuoto su `phase_b/`, `icl/`, `ablation/`, `reproducibility/`, `tep_validation_v2/`, `tep_test_v2/` e `tep_exp3_v2_heldout/`. Le modifiche osservate sono nei registri/piano ammessi e sotto `studio2/`. Nessun tag di congelamento è stato creato. |
| 3 | Precedenze | ✅ | Usati il registro di calibrazione rev. 19, che prevale sul piano, e il piano corrente §§8–11; non è stato usato `FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md`. La scelta dei descrittori non è stata riaperta né ricavata dalla §5.5 superata. |
| 4 | Dati del primo studio | ⚠️ | L'uso effettivo U1/R2 è registrato con ruolo, SHA-256, trasformazioni e marca corretta. I due commit di origine dichiarati (`309b944f…` e `a0413e16…`) non sono presenti nell'object database Git locale: sono verificabili le impronte dei byte locali, non il legame a quei commit. `PROVENIENZA.md` ora dichiara esplicitamente entrambe le indisponibilità; il limite è quindi correttamente tracciato e non viene trasformato in una provenienza più forte di quella verificabile. |
| 5 | Ordine delle sotto-fasi | ⚠️ | Birth time di specifica (18:00), piani e timestamp UTC dei manifest sostengono l'ordine dichiarato. Tuttavia specifica e piano erano file non committati e modificabili; `SPECIFICA_GENERAZIONE.md` è stata modificata alle 18:49, dopo il primo lotto prefissi concluso alle 18:46 e il primo risultato alle 18:48. Non esiste quindi una versione immutabile che permetta di provare quali clausole fossero già fissate per ogni lotto. La regola sui batch onerosi è arrivata con `93f33fc` dopo l'esecuzione: non la applico retroattivamente e, dato il ricalcolo indipendente, non richiedo una ripetizione delegata. |
| 6 | Coppie e conteggi | ✅ | Nessuna coppia MD/HTML è stata toccata. Piano e registro standalone concordano su R1/R2, A, 20 h, 350/150 e budget. I conteggi dei manifest e dei file coincidono con il report. |
| 7 | Test | ✅ | `python3 docs/test_explanation.py`: **35 test, 14 fallimenti, 1 skipped**, identico al baseline dichiarato. Nell'ambiente Python del progetto: **7/7** test Fase 02 PASS. Compilazione Python e `git diff --check`: PASS. |

## 4 · Riesame dei rilievi

### ⚠️ 4.1 · Archivio pubblico identificato, trasferimento non ancora verificabile

È stato creato il repository pubblico durevole
[`sorrentinoluca/fot-tep-data`](https://github.com/sorrentinoluca/fot-tep-data). Al momento del
riesame il repository è pubblico e contiene il README iniziale, ma non ancora i due archivi. Il
trasferimento dichiarato comprende **224 workbook autorevoli**: 74 contenuti legacy e 150 output
necessari ai ricalcoli, circa 407 MB complessivi, divisi in due archivi.

Questo trasferimento non è necessario per il capability pilot della Fase 03 e non blocca
l'aggiornamento narrativo della Fase 02. Resta però un gate prima del congelamento definitivo della
recuperabilità: dopo il caricamento vanno registrati release/commit immutabile, nomi e SHA-256 dei
due archivi, e va eseguita almeno una verifica di estrazione e confronto dei 224 file contro i
manifest. Fino ad allora non si deve scrivere che il recupero da nuova clone sia già verificato.

### ✅ 4.2 · Freeze esteso agli input eseguiti e alle dipendenze transitive

`PRECALIBRATION_FREEZE.json` include ora **40 file**, fra cui i cinque piani eseguiti,
`SIMULATOR_PROVENIENZA.md`, tutti i sorgenti e le dipendenze Simulink individuate, KAT, fixture e
test. A questi si aggiungono i cinque manifest di esecuzione. Il controllo indipendente ricalcola
dimensione e SHA-256 con esito **45/45 PASS**. È quindi congelato anche il piano burn-in realmente
eseguito, senza doverlo ricostruire dalla versione corrente del generatore.

Lo stato resta correttamente `content_frozen_pending_independent_verification_and_commit` e il
campo `source_head_commit=93f33fc…` non contiene ancora gli artefatti non tracciati. Come già
previsto dal report, dopo il commit completo il freeze va rigenerato con quel commit e ricontrollato;
questa è la normale chiusura del congelamento, non più una lacuna dell'insieme di file.

## 5 · Conclusione

**OK**: il lavoro regge e si può procedere all'aggiornamento della documentazione e alla Fase 03.
Il freeze incompleto e l'omissione su `a0413e16…` sono stati corretti. Non risultano errori nei
risultati 20 h, A, Philox–legacy, 100/100 prefissi, R2 o nei conteggi 750/768; non è richiesta una
nuova campagna di simulazione.

Resta una sola condizione operativa non bloccante per la fase successiva: completare i due archivi
in `sorrentinoluca/fot-tep-data` e verificarne il recupero prima di dichiarare chiuso il requisito
di `MAINTENANCE.md` §8.5 e prima del congelamento definitivo destinato a una nuova clone.

## 6 · Fonti lette e costo

Letti: prompt operativi; `MAINTENANCE.md` §§1–3, 5 e 8; `AUDIT_GUIDE.md` §§5–13 per il metodo di
audit; walkthrough Studio 2 §0; registro di calibrazione rev. 19; piano corrente nelle sezioni
pertinenti; registro descrittori §5.1; provenienza, specifica, qualifica, freeze, sorgenti, launcher,
test, piani, manifest e risultati della Fase 02. Ispezionati e ricalcolati i workbook necessari,
senza leggere repliche HTML o paper in blocco. Ordine di grandezza: circa 35–45k token documentali,
oltre a circa 650 MB di artefatti numerici letti meccanicamente.
