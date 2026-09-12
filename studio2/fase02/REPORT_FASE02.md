# REPORT_FASE02 — Preparazione e validazione della generazione e del riuso

**Data:** 2026-09-12  
**Stato:** macrofase corretta dopo il primo verdetto indipendente `NON OK`, pronta per nuova
verifica indipendente; nessun commit o tag creato nel repository sorgente da questa lavorazione.  
**HEAD di partenza:** `043e05bb296871ac2a0413d7115fb784b9fefe93`.  
**HEAD corrente:** `63274711a506597ff9690e7a87c7b4b3fac80591`; durante la lavorazione sono comparsi
due commit concorrenti dell'autore, `93f33fc` e `6327471`, entrambi limitati ai prompt. Il freeze
candidato registra l'HEAD corrente.  
**Perimetro:** tutto il nuovo codice, dati e risultati sotto `studio2/`; aggiornati fuori perimetro
soltanto il piano e il registro di calibrazione nelle loro sedi autorevoli.

## Esito sintetico

La Fase 02 produce una procedura di generazione verificata e un riuso qualificato, senza avviare la
campagna completa di calibrazione/test, la selezione dei nuovi fault o le inferenze LLM.

- `Ts_base=0.0005 h`, uscita a 1 min, burn-in qualificato **20 h**.
- Philox4×32-10 supera compilazione, tre vettori noti Random123, replay, confronto legacy e gate dei
  prefissi; la forma economica è autorizzata sul campione pre-specificato.
- R1 è respinto come sostituzione di nuovi run fault; R2 è autorizzato condizionatamente soltanto
  come `baseline_fit` congelata.
- Il piano riconciliato conta **750/768** simulazioni di protocollo (6/8 run per fault), **150** già
  chiuse nella qualifica e **600/618** residue.

### Non conformità di processo e primo esito indipendente

Alle 19:03:28 +0200 è comparso sull'HEAD il commit concorrente `93f33fc` (*prompts: soglia
quantitativa per le operazioni onerose, stimata prima di iniziare*), discendente dall'HEAD iniziale
e non prodotto da questa lavorazione. Esso ha aggiunto a `Fase_LLM.md`/`Prompt_LLM.md` la regola di
fermarsi prima di batch oltre dieci ripetizioni o dieci minuti e consegnare lo script
parallelizzabile. Il cambiamento è stato rilevato soltanto al controllo finale, dopo l'esecuzione
dei batch MATLAB. I batch erano già descritti da un piano, eseguiti da un unico launcher e
rendicontati su file, ma secondo la nuova regola avrebbero dovuto essere proposti all'autore invece
di essere avviati dall'agente. È una non conformità procedurale, non un fallimento dei gate; il
Nessun file modificato da questa fase si sovrappone al commit concorrente.

La prima verifica indipendente è registrata in `VERIFICA_FASE02.md` con verdetto **NON OK**. Ha
riprodotto integralmente i risultati numerici e ha stabilito che la regola sopravvenuta non richiede
di ripetere le simulazioni. Ha individuato due blocchi: assenza di una posizione recuperabile per i
workbook ignorati da Git e freeze incompleto. La correzione successiva ha pubblicato i 224 workbook
autorevoli nella release pubblica versionata `studio2-fase02-v1` di `sorrentinoluca/fot-tep-data`,
ne ha verificato il recupero con un nuovo download e ha esteso il freeze a piani e dipendenze
transitive. Queste correzioni devono ora ricevere una nuova verifica indipendente.

## 1. Conservazione del patrimonio

`preserve_legacy_data.py` ha risolto 78 percorsi logici relativi ai materiali non già conservati in
Git, corrispondenti a **74 contenuti distinti**. Ogni contenuto è copiato una sola volta, con nome
SHA-256, sotto `patrimonio_conservato/contenuti/`; `MANIFEST_CONSERVAZIONE.csv` mantiene la mappa
dalle origini alla copia.

Controlli indipendenti: 74 copie presenti, hash coincidenti, 74 inode distinti dalle origini,
workbook ZIP validi, 152.308.644 byte logici e 144.745.600 byte distinti. Una seconda esecuzione ha
verificato tutti i contenuti e creato zero copie. I workbook restano ignorati da Git per la regola
globale `*.xlsx`, ma i 74 contenuti sono ora recuperabili dalla release pubblica
[`studio2-fase02-v1`](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase02-v1).
L'asset legacy è stato riscaricato, estratto e verificato contro tutte le 78 righe/74 destinazioni
del manifest, senza mismatch.

## 2. Provenienza operativa

`studio2/PROVENIENZA.md` distingue esplicitamente:

1. conservazione senza autorizzazione;
2. candidatura R1/R2;
3. usi effettivamente autorizzati.

Seed, data di generazione e `Ts_base` storici mancanti non sono stati dedotti. Lo snapshot dataset
dichiarato è `309b944f35ac440ff0c70616947ffe723c766e14`; l'oggetto non è presente nell'object database Git
locale, mentre le copie sono identificate per SHA-256. Il simulatore pre-setpoint è ricondotto al
commit `a0413e16c940f0fc8b554d6a86248020d7fb7527` e alle impronte dei singoli file; anche questo commit
è dichiarato ma assente dall'object database locale. Il limite è ora esplicito in
`studio2/PROVENIENZA.md` e non viene sostituito da un'inferenza.

## 3. Specifica della generazione

`SPECIFICA_GENERAZIONE.md` e `generation_spec.json` hanno fissato prima dei rispettivi dati:

- `Ts_base`, frequenza di uscita, finestra da 5 h e namespace degli stream;
- procedura a dieci run per scegliere il burn-in fra 10/20/30/40 h contro `[60,70)`;
- politica distinta per trip fisico, trip Normal e fallimento tecnico;
- gate Philox, confronto col legacy, prefissi e guardia R2;
- fallback senza aggiustamento post-hoc delle soglie;
- campi minimi dei manifest.

Lo score è eseguibile in `analysis/combined_score.py`. La MAD è non riscalata, i pareggi esatti di
dominanza dividono il peso e i casi `c_f`/MAD degeneri arrestano il calcolo. Su N1–N5 la regola
congelata seleziona **A**, dominanza massima 0,48; `validation/score_fit_legacy.json` contiene gli
otto parametri robusti e i 164 riferimenti per sensore.

## 4. Implementazione nel nuovo perimetro

La copia adattata del simulatore è in `simulator/`. Gli originali non sono stati modificati.
Philox usa chiave radice `0x464f545445503032`, stream ID come parte del contatore e indice di
estrazione come contatore di draw. Il bit `MSFlag 0x20` è rifiutato.

Il launcher:

- accetta solo piani espliciti e output sotto `studio2/`;
- rifiuta sovrascritture e manifest preesistenti;
- scrive prima un workbook temporaneo e lo sposta solo a completamento;
- arresta il lotto se un Normal non raggiunge lo stop richiesto;
- confina cache/codegen sotto `simulator/build/`;
- registra stream, chiave, contatori, SHA di MEX/modello/output, configurazione, durata e stato.

Build locale definitiva: MATLAB R2025b ARM + Xcode/Clang, MEX SHA-256
`6ae7e7be5394773f1854f1c53eddbd778ad7557b61fb05a93b3edb0552b1d11e`. Il MEX è ignorato e va
ricostruito sulle altre piattaforme. Simulink emette sui run lunghi l'avviso che il buffer del
`Variable Time Delay` viene aumentato dinamicamente a 63.488/64.512; non ha prodotto trip, ma va
risolto prima di un'eventuale generazione di codice embedded.

## 5. Validazione tecnica e numerica

La prima build non esportava il contatore finale. Dopo aver rilevato la difformità dal manifest
pre-specificato, è stata aggiunta la sola strumentazione diagnostica, ricompilato il MEX e ripetuti
tutti i lotti Philox sulla build definitiva. Uno smoke test prima/dopo la modifica ha dato valori
numerici esattamente uguali. I risultati autorevoli hanno suffisso `_v2`.

### Gate e risultati

| Gate | Campione | Esito |
| --- | --- | --- |
| Known-answer test | 3 vettori Philox4×32-10 dalla suite ufficiale [Random123](https://github.com/DEShawResearch/random123) | bit-esatto, PASS |
| Replay | stesso stream/configurazione, esecuzioni separate | valori grezzi esatti, PASS |
| Burn-in | 10 stream × 70 h | 20 e 30 h passano; selezionato **20 h** |
| Philox vs legacy | 10 + 10 run, 50 h utili | 5/5 metriche, PASS |
| Prefissi | 10 stream × 10 posizioni | **100/100**, zero fallimenti |
| Contatori prefissi | 10 stream | endpoint crescenti; J10=full per 10/10, PASS |
| Integrità output definitivi | 140 workbook Philox | hash/durata/stato/contatore, 140/140 PASS |

Confronto Philox–legacy:

| Metrica | Scarto mediana / MAD legacy | MAD Philox / MAD legacy |
| --- | ---: | ---: |
| `abs_shift_sigma` | 0,030931 | 1,018051 |
| `abs_slope_sigma_h` | 0,097146 | 1,076287 |
| `residual_std_ratio` | 0,023606 | 0,982913 |
| `diff_std_ratio` | 0,026606 | 1,062815 |
| `S` | 0,018032 | 1,064466 |

Nei 100 confronti di prefisso le massime differenze per uscite, feature e `S` sono tutte **0,0**.
La validazione osserva gli endpoint dei contatori: non introduce checkpoint interni nel run full.
L'accordo esatto dei dati comuni, la monotonia degli endpoint corti e J10=full sostengono il gate
nel perimetro provato, non una proprietà generale di ogni solver/configurazione.

Prestazione: su 50 esecuzioni Philox da 70 h, mediana **9,21 s**, minimo 8,92 s, massimo 14,67 s.
Il sottoinsieme full/J10 comprende 20 esecuzioni appaiate con mediana 9,32 s (8,92–10,43 s).

Sono stati prodotti 293 workbook complessivi durante sviluppo e verifica: 150 nel primo giro
scientifico, 140 ripetizioni Philox sulla build definitiva e 3 smoke test. Il budget del piano
conta i **150 ruoli diagnostici pre-specificati**, non le ripetizioni tecniche.

## 6. Qualificazione R1/R2

La motivazione completa è in `QUALIFICAZIONE_RIUSO.md`.

- **R1 — NO come sostituzione.** I 20 fault storici hanno schema e griglia coerenti e copie
  verificate, ma mancano seed, data, `Ts_base` e prova della configurazione eseguita. Restano
  materiale storico già osservato per ipotesi/rappresentazione, mai nuove repliche confermative.
- **R2 — SÌ condizionato come sola baseline.** Dieci pilot Philox superano la guardia su `S`
  (scarto 0,389889 MAD; rapporto MAD 0,956200) e, in aggiunta, sulle quattro famiglie. N1–N5
  restano cinque blocchi contigui: vietato usarli come run indipendenti, calibrazione o verifica.

Il fallback R2 resta 100 `baseline_fit_new`, 300 `cal_thr`, 150 `far_ver` se impronte, codice,
parametri o verifica indipendente non coincidono.

## 7. Piano aggiornato e congelamento

Il piano e il registro di calibrazione ora concordano su R1/R2, score A, 20 h, Philox, forma
economica, 350 `cal_thr` e 150 `far_ver`. Il budget è parametrico rispetto a 6/8 run di test:

| Voce | 6 run | 8 run |
| --- | ---: | ---: |
| Qualifica Fase 02, completata | 150 | 150 |
| Sviluppo fault | 40 | 40 |
| `cal_thr` | 350 | 350 |
| `far_ver` | 150 | 150 |
| Test in catalogo | 54 | 72 |
| OOD | 6 | 6 |
| **Totale** | **750** | **768** |
| **Residuo** | **600** | **618** |

`validation/PRECALIBRATION_FREEZE.json` schema 2 identifica **41 artefatti** per contenuto e cinque
manifest eseguiti. Include i cinque piani effettivi, tutte le dipendenze transitive del simulatore,
stato iniziale, KAT, test, fixture smoke, documenti di provenienza e record dello storage pubblico.
Stato: `content_frozen_and_data_archived_pending_independent_reverification_and_commit`. Soglia,
rango e numerosità restano `null` correttamente: sono risultati della futura calibrazione; dopo di
essa e prima di `far_ver` dovranno essere aggiunti con la regola `S > threshold`.

`ARTIFACT_STORAGE.json` identifica la release dati e i due asset. Il primo contiene 74 workbook
legacy; il secondo 140 output Philox definitivi, 10 output legacy autorevoli e cinque manifest.
La copia remota è stata verificata con un download separato: SHA degli asset coincidenti e zero
mismatch sui 224 workbook estratti. Il tag della release punta al commit dati
`6d238929285e57c6c70f4d563ef7e30b59da6ac5`.

## File toccati

I workbook ignorati non sono duplicati in questo elenco: ciascuno compare una riga nel relativo
manifest. Sono 74 copie di conservazione e 293 output di simulazione.

- `docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md` — revisione 19, esiti dei sette requisiti, R2 e forma economica.
- `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` — R1/R2 e budget 750/768 riconciliati.
- `studio2/PROVENIENZA.md` — origine, metadati mancanti, candidatura e uso autorizzato U1/R2.
- `studio2/fase02/ARTIFACT_STORAGE.json` — release pubblica, asset, impronte e verifica del recupero.
- `studio2/fase02/MANIFEST_CONSERVAZIONE.csv` — 78 origini logiche e 74 destinazioni per hash.
- `studio2/fase02/QUALIFICAZIONE_RIUSO.md` — decisioni motivate R1 e R2.
- `studio2/fase02/REPORT_FASE02.md` — questo report.
- `studio2/fase02/SIMULATOR_PROVENIENZA.md` — origine e modifiche della copia del simulatore.
- `studio2/fase02/SPECIFICA_GENERAZIONE.md` — specifica pre-esecuzione, gate e fallback.
- `studio2/fase02/generation_spec.json` — forma machine-readable della specifica.
- `studio2/fase02/preserve_legacy_data.py` — conservazione idempotente e manifest.
- `studio2/fase02/build_generation_plan.py` — piani e namespace separati; 110 righe per i prefissi.
- `studio2/fase02/freeze_precalibration.py` — costruzione del freeze per contenuto.
- `studio2/fase02/analysis/tep_features.py` — copia adattabile delle feature del primo studio.
- `studio2/fase02/analysis/combined_score.py` — fit/applicazione A/A′ e riferimenti per sensore.
- `studio2/fase02/analysis/validate_numerics.py` — gate burn-in, generatori, prefissi e R2.
- `studio2/fase02/simulator/source/temexd_philox.c` — S-function Philox e contatore diagnostico.
- `studio2/fase02/simulator/source/philox4x32.h` — implementazione Philox4×32-10.
- `studio2/fase02/simulator/source/philox_kat.c` — known-answer test e replay.
- `studio2/fase02/simulator/source/teprob_mod.h` — dipendenza copiata senza modifica.
- `studio2/fase02/simulator/matlab/MultiLoop_mode1.mdl` — modello collegato a `temexd_philox`.
- `studio2/fase02/simulator/matlab/tesys.mdl` — sottosistema collegato a `temexd_philox`.
- `studio2/fase02/simulator/matlab/TElib.mdl` — dipendenza copiata senza modifica.
- `studio2/fase02/simulator/matlab/Mode_1_Init.m` — init copiato senza modifica.
- `studio2/fase02/simulator/matlab/Mode1xInitial.mat` — stato iniziale copiato senza modifica.
- `studio2/fase02/simulator/matlab/TEplot.m` — callback legacy copiata senza modifica.
- `studio2/fase02/simulator/matlab/compile_philox.m` — compilazione protetta sotto build.
- `studio2/fase02/simulator/matlab/generate_normal_runs.m` — launcher Philox e manifest completo.
- `studio2/fase02/simulator/matlab/generate_legacy_normal_runs.m` — confronto legacy con seed espliciti.
- `studio2/fase02/simulator/build/.gitignore` — esclusione delle build locali.
- `studio2/fase02/tests/fixtures/runtime_smoke_plan.csv` — piano smoke riservato.
- `studio2/fase02/tests/test_combined_score.py` — test score e degenerazioni.
- `studio2/fase02/tests/test_generation_plan.py` — test prefissi, seed e disgiunzione stream.
- `studio2/fase02/validation/plans/burnin_qual.csv` — 10 run di qualifica burn-in.
- `studio2/fase02/validation/plans/philox_legacy_qual.csv` — 10 run Philox di confronto.
- `studio2/fase02/validation/plans/legacy_generator_qual.csv` — 10 run legacy con seed fissati.
- `studio2/fase02/validation/plans/prefix_qual.csv` — 110 run di confronto prefissi.
- `studio2/fase02/validation/plans/r2_pilot.csv` — 10 pilot R2 riservati.
- `studio2/fase02/runtime_smoke_output/generation_manifest.csv` — primo smoke tecnico.
- `studio2/fase02/runtime_smoke_replay/generation_manifest.csv` — replay smoke tecnico.
- `studio2/fase02/validation/data/instrumented_smoke/generation_manifest.csv` — smoke della build definitiva.
- `studio2/fase02/validation/data/burnin_qual/generation_manifest.csv` — primo lotto burn-in.
- `studio2/fase02/validation/data/philox_legacy_qual/generation_manifest.csv` — primo lotto Philox/legacy.
- `studio2/fase02/validation/data/legacy_generator_qual/generation_manifest.csv` — lotto legacy autorevole.
- `studio2/fase02/validation/data/prefix_qual/generation_manifest.csv` — primo lotto prefissi.
- `studio2/fase02/validation/data/r2_pilot/generation_manifest.csv` — primo pilot R2.
- `studio2/fase02/validation/data_v2/burnin_qual/generation_manifest.csv` — burn-in build definitiva.
- `studio2/fase02/validation/data_v2/philox_legacy_qual/generation_manifest.csv` — confronto build definitiva.
- `studio2/fase02/validation/data_v2/prefix_qual/generation_manifest.csv` — prefissi build definitiva.
- `studio2/fase02/validation/data_v2/r2_pilot/generation_manifest.csv` — pilot R2 build definitiva.
- `studio2/fase02/validation/burn_in_result.json` — risultato preliminare prima strumentazione.
- `studio2/fase02/validation/generator_comparison_result.json` — confronto preliminare.
- `studio2/fase02/validation/prefix_result.json` — prefissi preliminari.
- `studio2/fase02/validation/r2_guard_result.json` — guardia R2 preliminare.
- `studio2/fase02/validation/burn_in_result_v2.json` — risultato burn-in autorevole.
- `studio2/fase02/validation/generator_comparison_result_v2.json` — confronto autorevole.
- `studio2/fase02/validation/prefix_result_v2.json` — prefissi e contatori autorevoli.
- `studio2/fase02/validation/r2_guard_result_v2.json` — guardia R2 autorevole.
- `studio2/fase02/validation/score_fit_legacy.json` — A, parametri e 164 riferimenti.
- `studio2/fase02/validation/PRECALIBRATION_FREEZE.json` — 41 artefatti e 5 manifest per hash.
- `studio2/fase02/VERIFICA_FASE02.md` — primo verdetto indipendente `NON OK` e rilievi corretti.

## Profili d'esecuzione e modello

La classificazione seguente è aggiunta per conformità alla versione di `Fase_LLM.md` introdotta dal
commit concorrente `6327471` durante la correzione. La fase originaria non disponeva ancora di
queste etichette in apertura. Il modello della finestra di produzione e di questa correzione è **Codex, famiglia GPT-5
fornita dalla sessione**; la verifica `NON OK` è stata svolta in un task distinto, anch'esso
identificato dal verificatore come Codex/GPT-5.

| Sotto-fase | Profilo | Esecuzione |
| --- | --- | --- |
| 1. Conservazione | implementativo; copia meccanica | script e copia eseguiti nella finestra di produzione |
| 2. Provenienza | decisionale | finestra di produzione |
| 3. Specifica | decisionale | finestra di produzione |
| 4. Implementazione | implementativo | finestra di produzione |
| 5. Validazione | implementativo + esecutivo-batch | launcher e batch eseguiti nella finestra di produzione; non conformità dichiarata, risultati poi riprodotti integralmente dal verificatore |
| 6. Qualificazione R1/R2 | decisionale | finestra di produzione |
| 7. Piano e report | decisionale + implementativo | finestra di produzione |
| Correzione storage | implementativo; quattro operazioni esterne di archivio/upload sotto soglia | questa finestra, dopo conteggio di 224 workbook e stima preventiva; nessuna simulazione |
| Correzione freeze | implementativo | questa finestra |

Il commit concorrente che modifica `docs/prompts/Fase_LLM.md` non è stato prodotto da questa
lavorazione; il file è stato soltanto riletto per applicare il nuovo requisito al report.

## Fuori dalla Fase 02

- campagna `cal_thr`/`far_ver`, soglia, rango e FAR realizzato;
- 40 nuovi fault di sviluppo, test in catalogo e 6 OOD;
- selezione dei nuovi fault e decisioni del catalogo;
- produzione delle feature/evidence di sviluppo e dei prototipi fault;
- harness e inferenze LLM;
- aggiornamento della coppia walkthrough Markdown/HTML, subordinato alla verifica;
- commit e tag di congelamento, subordinati al ciclo `Verifica_LLM` → `Commit_LLM`.

## Decisioni ancora necessarie

1. Una nuova finestra indipendente deve verificare il recupero pubblico e la completezza del freeze
   dopo le correzioni al primo verdetto `NON OK`.
2. Dopo un esito positivo, l'autore deve autorizzare il commit di congelamento e rigenerare il
   freeze col nuovo commit completo.
3. Le scelte ancora aperte del catalogo e il numero finale 6/8 run restano fuori da questa fase;
   i conteggi sono quindi mantenuti nelle due colonne.

## Letture effettuate e costo indicativo

Sono stati letti: `docs/MAINTENANCE.md`; `Prompt_LLM.md` e `Fase_LLM.md`; §0, §0.1 e §2–12 del
walkthrough Studio 2; le sezioni pertinenti dei due walkthrough del primo studio; §6 e le porzioni
di budget/manifest del piano; il registro di calibrazione; report e verifica di Fase 01; sorgenti,
launcher, manifest e dati necessari. Non sono stati aperti in blocco i paper né le repliche HTML.
Ordine di grandezza della lettura documentale: circa 30–40k token, oltre all'ispezione mirata di
codice e risultati.

## Verifiche finali

- test unitari Studio 2: 7/7 PASS;
- compilazione Python: PASS;
- C99 con `-Wall -Wextra -Werror`: PASS;
- conservazione: 74/74, seconda esecuzione idempotente;
- manifest build definitiva: 140/140 output verificati;
- storage pubblico: due asset, 426.552.832 byte; nuovo download con SHA coincidenti; 224/224
  workbook estratti verificati contro i manifest;
- freeze schema 2: 41 file e 5 manifest, 46/46 impronte coincidenti;
- `git diff --check`: PASS;
- aree congelate modificate: 0;
- directory `slprj` alla radice e file `.tmp.xlsx`: 0;
- `python3 docs/test_explanation.py`: 35 test, **14 fallimenti**, 1 skipped, identico al baseline
  preesistente indicato in `docs/MAINTENANCE.md`; nessun peggioramento.

Non sono stati aggiornati i walkthrough: secondo il flusso di `Fase_LLM.md`, l'aggiornamento segue
la verifica indipendente. Non sono stati creati commit o tag. Messaggio di commit proposto, dopo
verifica: `studio2(fase02): qualifica generazione e riuso`.

## Istruzioni per il verificatore indipendente

1. Controllare le 41 impronte dei file e le cinque impronte dei manifest nel freeze; il report non
   è incluso perché è l'oggetto della verifica.
2. Scaricare i due asset indicati da `ARTIFACT_STORAGE.json` in un ambiente separato, verificarne
   SHA-256, estrarli in una nuova clone e verificare i 224 workbook contro i manifest inclusi.
3. Confermare che piani eseguiti, sorgenti, sottosistemi, stato iniziale, KAT e test siano tutti nel
   freeze. I risultati numerici sono già stati riprodotti integralmente dalla prima verifica e non
   richiedono nuove simulazioni per controllare queste correzioni.
4. Confermare che nessuna area congelata sia cambiata e che il test documentale resti a 14
   fallimenti preesistenti.
5. Solo dopo esito positivo: creare il commit di congelamento, rigenerare il freeze col commit
   completo e aggiornare il walkthrough Studio 2 nella sua coppia Markdown/HTML.
