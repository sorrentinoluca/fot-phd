# Studio 2 — walkthrough

> **Documento vivo, a scheletro.** Si aggiorna **fase per fase**. Stato al **2026-09-14**:
> fasi 01 e 02 documentate in §2 e §3; la sotto-fase **criteri di selezione (§6.1)** della
> Fase 03 è documentata in [§4.1](#criteri-selezione-61); **D1, verificata, congelata e pubblicata**, in [§4.2](#catalogo-d1);
> i **run fault di sviluppo (§6.2)**, verificati e conservati, in [§4.3](#run-fault-62); le
> **soglie Normal (§6.3)**, calibrate e verificate, in [§4.4](#soglie-normal-63). La Fase 03 resta aperta. La parte restante delle fasi successive
> resta a scheletro: per essa **la fonte autorevole è il piano**, non questo file.

| Ruolo | File |
| --- | --- |
| Documento lungo (questo) | `fot_walkthrough_conversazione_studio2.md` |
| Replica web, da tenere allineata | `fot_walkthrough_conversazione_studio2.html` |
| Sintesi divulgativa | `fot_walkthrough_studio2.html` — rimanda, non duplica |
| Letteratura | [`letteratura.md`](letteratura.md) — luogo unico, non si copia qui |
| Primo studio | `fot_walkthrough_conversazione_v2.md` — **record**, non fonte per questo disegno |

**Perché la numerazione salta da 1 a 13.** Le sezioni §2–§12 sono riservate alle fasi, che si
aggiungeranno man mano. §13 e §14 stanno dove stavano nel primo studio, così i riferimenti
«§13» e «§14» conservano lo stesso significato in entrambi gli studi.

---

## 0 · Fonti autorevoli e precedenze

Da rispettare finché questo documento non descrive una fase di persona.

| Ambito | Fonte | Nota |
| --- | --- | --- |
| Disegno generale | `paper/FoT_TEP_Review_Piano_Sperimentale.md` §§8–11, §13 | la revisione corrente è la 6 |
| Decisioni non ancora congelate | idem, §0.1 | prima cosa da guardare |
| Calibrazione delle soglie | `lit_review/DECISIONE_calibrazione_soglie_fase_B.md` (rev. 19) | **prevale sul piano** per il metodo; soglia, rango, FAR e incertezza prodotti dalla 03.5 sono documentati in [§4.4](#soglie-normal-63) |
| Scelta dei descrittori | `lit_review/criteri_scelta_descrittori.md` §5.1 | ⚠️ **non** la §5.5, superata dal piano |
| Feature e pre-impegno su E5 | `lit_review/DECISIONE_SCELTA_FEATURE_fase_A.md` | registro di decisione; il disegno resta autorevole nel piano |
| Ablazione dei descrittori | `../analysis/feature_ablation/FEATURE_ABLATION.md` | |
| Vincoli su cosa è congelato | `MAINTENANCE.md` §1 e §2 | |
| Letteratura | [`letteratura.md`](letteratura.md) | |

**Il ciclo di lavoro di una fase.** `Fase_LLM` → `Verifica_LLM` (altra finestra, altro modello) →
`Documentazione_LLM` → `Commit_LLM`, tutti in [`prompts/`](prompts), con il `README.md` della
cartella che dice quale aprire quando. L'ordine non è negoziabile: **questa sezione del walkthrough
non si scrive prima della verifica indipendente.** Le regole di perimetro, commit e congelamento
sono in [`MAINTENANCE.md`](MAINTENANCE.md) §8.

**I dati del primo studio si leggono, non si ipotizzano.** Sono patrimonio disponibile, non una
storia da raccontare: nel paper si descrivono per quello che sono — configurazione, seed, data di
generazione — senza narrare un esperimento precedente. Ciò che non è sostenibile è farli passare
per generati *per* questo studio. La provenienza resta interna, in `studio2/PROVENIENZA.md`, con la
marca **pre-specificato / post-hoc** di ogni analisi che li usa ([`MAINTENANCE.md`](MAINTENANCE.md) §8.2).

**Da non usare come fonte:** `paper/FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md` — è il piano
originale che la review critica, non lo stato corrente; i risultati e la narrazione del primo
studio; `archive/lit_review_2026-09/`.

## 0.1 · Punti aperti — da risolvere, non da aggirare

Restano qui le decisioni che una fase non può chiudere da sola. Il precedente punto sul riuso dei
dati del primo studio è stato chiuso dalla fase 02: R1 è respinto come sostituzione di nuovi run
fault e R2 è autorizzato soltanto come `baseline_fit` condizionata
([§3](#3--preparazione-indipendente-dal-modello--generazione-e-riuso-fase-02)).

| # | Punto aperto | Perché blocca | Chi decide | Registrato | Decisione da chiudere in |
| :---: | --- | --- | --- | --- | --- |
| 1 | **Sigle `C06`, `C07`, `C18`** citate dal piano sperimentale | Vengono dal registro critiche `C01–C18`, che esiste **solo** in `fot_walkthrough_conversazione.md` §33 — la prima esposizione del primo studio, che non è fonte. Finché restano così sono riferimenti appesi a un documento che nessuno deve usare | riportarle per esteso nel piano **oppure** rinumerarle | 2026-09-12 | `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` §0.1 — **non** il piano BIGDATA2026, che §0 esclude dalle fonti autorevoli |
| 2 | **Perimetro del codice della Q8** | La terza metrica di §8.5, il cap sulla lunghezza dello schema, l'estensione a 8 agenti e il derangement a 7 pseudolabel richiedono tutti di scrivere dentro `phase_b/`, che [`MAINTENANCE.md`](MAINTENANCE.md) §1 dichiara **congelato**. Nessuna sessione può decidere da sola di scriverci | aprire un perimetro nuovo (`phase_b/q8/`) **oppure** dichiarare quale parte di `phase_b/` è harness riutilizzabile e quale è artefatto — in entrambi i casi è una modifica a §1 | 2026-09-12 | `docs/MAINTENANCE.md` §1 (separato tra harness riutilizzabile e artefatto) |
| 3 | **Congelamento definitivo della fase 02** | Gli artefatti sono committati e il freeze è stato rigenerato sul loro HEAD; il record di storage e il freeze rigenerato sono successivi al riesame indipendente | riverifica indipendente delle impronte del freeze rigenerato prima di ogni tag definitivo | 2026-09-12 | `studio2/fase02/validation/PRECALIBRATION_FREEZE.json` e ciclo `Verifica_LLM` |
| 4 | **Formato del tag di lotto su `fot-tep-data`** | Chiuso: segue `MAINTENANCE.md` §8.5; per i lotti il formato operativo è ora esplicito e rinvia lì | aggiornato in `MAINTENANCE.md` | 2026-09-13 | `docs/MAINTENANCE.md` §8.5 / §8.6 |

*Registrati il 2026-09-12 (1–3) e il 2026-09-13 (4, ora chiuso in `MAINTENANCE.md` §8). Quando uno si chiude, va tolto da qui e la decisione va scritta dove
compete: nel piano, in un registro di `lit_review/`, o in `MAINTENANCE.md` §1/§8.*

---

## 1 · Introduzione

*Scheletro. Ogni voce dice dove sta oggi la fonte; il testo si scrive quando la fase relativa
è conclusa.*

- **Le fasi dello studio 2** — le fasi 01 e 02 sono documentate in
  [§2](#2--preparazione-indipendente-dal-modello--ricognizione-del-patrimonio-fase-01) e
  [§3](#3--preparazione-indipendente-dal-modello--generazione-e-riuso-fase-02); le successive
  sono mappate in [§4–12](#412--fasi-successive); l'ordine dentro §6 è vincolato: preparazione
  indipendente dal modello, capability pilot come gate, produzione insight, congelamento, esecuzione, analisi.
- **Obiettivo e domanda scientifica dello studio 2** — piano §8
- **Che cosa cambia rispetto al primo studio** — il riuso effettivo finora è limitato a N1–N5
  come `baseline_fit`, pre-specificata nel nuovo studio ma basata su dati già osservati; §3 ne
  registra provenienza e limiti. Il resto del confronto resta da completare nelle fasi successive
- **Banco di prova: agenti, guasti, pseudolabel** — piano §8; ⚠️ le pseudolabel sono **nove**,
  non dieci: `Unknown` è il nome dell'astensione, non una classe
- **Condizioni e bracci** — piano §8, incluso il braccio *producer-swap*
- **Popolazione, endpoint e contrasti** — piano §8.5
- **Protocollo di valutazione e criteri di successo** — piano §8.5, §11 (GO/NO-GO)
- **Baseline** — piano §9
- **Che cosa non è ancora congelato** — piano §0.1; soglia, rango, numerosità e FAR della 03.5
  sono ora documentati in [§4.4](#soglie-normal-63), mentre la Fase 03 resta aperta
- **Limiti dichiarati in partenza** — piano §5 (tabella delle critiche) e §12

---

## 2 · Preparazione indipendente dal modello — ricognizione del patrimonio (fase 01)

### 2.1 · Riassunto e sintesi

La fase 01 ha chiuso la **ricognizione e il consolidamento del patrimonio sperimentale**: ha
censito dati grezzi, derivati, esecuzioni e componenti disponibili; ne ha ricostruito la
provenienza; ha distinto ciò che può essere riusato direttamente, ciò che richiede un ricalcolo e
ciò che resta soltanto un riferimento descrittivo; ha infine riesaminato il perimetro dei dati, il
budget e i percorsi di scrittura. La verifica indipendente ha dato **OK alla chiusura della
ricognizione**, dopo un primo NON OK e le integrazioni richieste
([report](../studio2/fase01/REPORT_FASE01.md),
[verifica](../studio2/fase01/VERIFICA_FASE01.md)).

L'esito è una mappa verificata di ciò che esiste e di ciò che manca, **non** l'esecuzione dei dodici
cantieri di preparazione del piano. Non sono state avviate nuove simulazioni o inferenze LLM, non
sono state scelte nuove classi, non sono state calibrate nuove soglie e non è stato congelato alcun
protocollo. Le proposte di riuso R1 e R2 restano proposte: l'OK non le adotta e non trasforma dati
già osservati in una conferma indipendente del nuovo studio.

### 2.2 · Dettaglio

#### Inventario e provenienza

Il censimento riproducibile trova **108 percorsi XLSX materializzati e 104 contenuti distinti per
SHA-256** nelle quattro raccolte `code/tep_cache/`, `tep_cache/`, `tep_heldout/mode1/` e
`tep_exp3_v2_heldout/mode1/`. Il [manifest PBH](../phase_b/heldout/phase_b_heldout_manifest.csv)
contiene 15 casi; i 17 file held-out restanti sono il suo complemento dentro la stessa raccolta,
non un'aggiunta al totale. Uno di essi, F6, termina a 17,1333 ore per un trip fisico documentato:
non sono autorizzati padding, troncamento o rigenerazione selettiva
([nota di generazione](../tep_heldout_phase_summary.md), §12).

N1–N5 sono cinque blocchi consecutivi di 50 ore estratti dalla stessa traiettoria Normal di 500
ore: rappresentano **250 ore continue, non cinque simulazioni indipendenti**. Il seed dei 17 run
aggiuntivi, il `Ts_base` storico di N1–N5 e la disponibilità remota degli oggetti LFS non sono stati
ricostruiti e non vanno inferiti.

La verifica sui ref Git trova 30 contenuti EXP3_V2 conservati come blob XLSX reali nel tag
`exp3-v2-heldout-data-frozen-001`; gli altri **74 dei 104 contenuti distinti non risultano
conservati in Git**. Gli hash ne attestano l'identità, non la reperibilità. La prima attività
operativa successiva deve quindi essere una copia recuperabile verificata dei 74 contenuti, con
registrazione di posizione e impronte, prima di ulteriori usi o spostamenti per il nuovo studio
([verifica, §5](../studio2/fase01/VERIFICA_FASE01.md)).

#### Derivati ed esecuzioni recuperati

Le tabelle in [`code/tep_analysis_v2/`](../code/tep_analysis_v2/) contengono, al netto delle
intestazioni, 820 record di feature per caso, 6.560 per finestra, 820 firme temporali, 2.050 valori
Normal per variabile e finestra e 50 massimi Normal. Sono granularità diverse e non osservazioni
indipendenti da sommare. Gli artefatti di inferenza recuperati comprendono 3.002 record costruiti
su **45 casi fisici distinti** — 15 PBH e 30 EXP3_V2 — e quindi non documentano 3.002 simulazioni
indipendenti. Il dettaglio per gruppo e i relativi ref sono verificati in
[`VERIFICA_FASE01.md`, §3](../studio2/fase01/VERIFICA_FASE01.md).

#### Compatibilità e classificazione del riuso

Il controllo numerico sui Normal mostra che le tabelle archiviate usano una baseline
leave-one-block-out, mentre il nuovo score richiede una baseline fissa sui blocchi di sviluppo.
Di conseguenza i dati Normal possono essere riusati solo nel ruolo che sarà autorizzato, ma le
feature necessarie al nuovo score devono essere ricalcolate. Le feature dei fault anteriori
all'applicazione delle soglie sono riusabili soltanto se coincidono dati, baseline, finestre e
formule; firme, testi, esempi e prototipi dipendono invece dalle scelte definitive e devono essere
ricostruiti o verificati per identità. Le fonti numeriche sono
[`normal_5h_variable_features.csv`](../code/tep_analysis_v2/normal_5h_variable_features.csv),
[`normal_5h_window_maxima.csv`](../code/tep_analysis_v2/normal_5h_window_maxima.csv) e
[`threshold_calibration.json`](../code/tep_analysis_v2/threshold_calibration.json).

Il report recepisce il massimo LOBO corretto, `1,41e-12`. La verifica precisa che il valore non
arrotondato è `1,414e-12` per `abs_shift_sigma` e che 20 valori LOBO su 2.050 superano `1e-12`.
La separazione dalla baseline fissa resta ampia, ma si fonda sulla magnitudine — ordine `1e-12`
contro ordine `1e-2` — non su `1e-12` come soglia separatrice
([verifica, §8.3](../studio2/fase01/VERIFICA_FASE01.md)).

#### Perimetro dei dati e budget

La fase formula due revisioni distinte, entrambe ancora da decidere:

- **R1:** riusare i 20 run di sviluppo F1/F8/F10/F13 al posto della loro rigenerazione;
- **R2:** usare N1–N5 anche come Normal di sviluppo, ruolo ulteriore rispetto alla baseline già
  prevista dal registro di calibrazione.

R1 e R2 insieme eviterebbero 25 nuove simulazioni soltanto se superano le rispettive verifiche di
compatibilità. Il budget delle simulazioni resta parametrico in run recuperabili, nuovi Normal di
sviluppo, 6/8 run per classe e diagnostiche ancora da dimensionare. Il budget API corrente del
piano è circa **2.853/3.555 chiamate con margine** per 6/8 run, con tetti di pianificazione
3.000/3.700 ([piano, §8.8](paper/FoT_TEP_Review_Piano_Sperimentale.md)). Prima della decisione sul
numero di run va corretta la contraddizione con i criteri T5 e O2, che riportano ancora 3.500 per
il ramo a otto run; il suo subtotale stimato di circa 3.555 supera quel tetto.

#### Perimetro operativo

Tutto il nuovo codice, i dati, le configurazioni, i test, i manifest, le esecuzioni e i risultati
devono vivere sotto `studio2/`. Il caratterizzatore esistente
[`tep_characterize_v2.py`](../code/tep_characterize_v2.py) usa una destinazione relativa
predefinita, non espone un parametro per cambiarla e può scrivere nell'area degli artefatti
esistenti: **non è riutilizzabile così com'è**. L'adattamento dovrà essere un file nuovo dentro
`studio2/`, con destinazioni esplicite e protezioni contro la sovrascrittura. Prima di qualsiasi
riuso va inoltre creato `studio2/PROVENIENZA.md`, indicando per ogni oggetto origine, commit,
impronta, destinazione, modifiche, ruolo e natura pre-specificata o post-hoc dell'analisi; i
metadati non recuperabili devono essere dichiarati mancanti.

### 2.3 · Connessione alla letteratura

La ricognizione non produce un claim bibliografico nuovo. Rafforza però tre vincoli già registrati
in [`letteratura.md`](letteratura.md):

- le schede sulla predizione conforme (§14.2) richiedono di distinguere validità marginale,
  condizionale ed empirica e di esplicitare IID/scambiabilità; la continuità di N1–N5 impedisce di
  contarli come cinque repliche indipendenti senza ulteriore giustificazione;
- EviFDD-Agent (§14.2) sostiene la separazione fra campi deterministici e narrazione e rende
  centrale la tracciabilità dello schema, ma questa fase non ha ancora dimostrato la conformità
  degli insight del nuovo studio;
- FedSRD (§14.2) rende pertinente la misura di byte e token, ma un budget di chiamate non dimostra
  efficienza comunicativa. §§14.5–14.6 delimitano inoltre ogni rivendicazione di novità: il
  contributo difendibile resta nell'intersezione e nel disegno A/B/E, non nel semplice riuso o
  inventario di componenti noti.

### 2.4 · Connessione alle critiche

La fase **non chiude alcuna critica scientifica** del piano. Mitiga il rischio operativo di riuso
opaco rendendo visibili provenienza, duplicazioni, dipendenze e lacune di conservazione; rende
inoltre misurabili i costi prima dell'esecuzione. Restano aperte le critiche sulla scala e sulla
pretesa Big Data, sulla degradazione delle classi localmente note, sul parsing e sul reasoning cap,
sulla dipendenza dal producer e sull'OOD: per esse la ricognizione prepara i controlli, ma non
fornisce risultati.

### 2.5 · Artefatti e riproducibilità

- Chiusura: [`REPORT_FASE01.md`](../studio2/fase01/REPORT_FASE01.md), SHA-256
  `51ca64099e50e37724b87c0aeb6fd7a16081ba39b8b2b1f30c2c9cf8d3e164e3`.
- Verifica indipendente: [`VERIFICA_FASE01.md`](../studio2/fase01/VERIFICA_FASE01.md), SHA-256
  `fbbb163a22d3d8aad7c8bd9bbc7951a1349f4e1f3c2b192b86e62323d7ddee42`; verdetto **OK**. Le tre
  correzioni puntuali richieste dalla verifica sono state recepite nel report.
- Manifest di riferimento: [`phase_b_heldout_manifest.csv`](../phase_b/heldout/phase_b_heldout_manifest.csv),
  SHA-256 `610c8a5fa6e763c25a9f9602a7e095c5fe850ed41b22552b0b92cec7edb450a3`.
- Configurazione di calibrazione recuperata:
  [`threshold_calibration.json`](../code/tep_analysis_v2/threshold_calibration.json), SHA-256
  `684ce2a68761d81bf839590292d8e7225e27ab079f4172f70b3dbc38f9649c33`.
- Stati esaminati dalla ricognizione e dalla verifica: `9289a4cb…`, `941c09b…` e `9e3d9031…`;
  stato di redazione del report: `9e3d9031013788a583e348fbd7bfc40e14d3c68b`. Sono riferimenti di
  provenienza, non tag di congelamento. Nessun nuovo tag o freeze è stato creato.

### 2.6 · Lavoro che resta

La fase 02 ha poi messo in sicurezza i 74 contenuti, deciso R1/R2, fissato `Ts_base`, qualificato
burn-in e Philox, reso eseguibile lo score e verificato i prefissi. Restano le scelte di catalogo,
la calibrazione e verifica FAR, i run fault, le componenti dipendenti dal modello e il congelamento
definitivo sul commit completo.

---

## 3 · Preparazione indipendente dal modello — generazione e riuso (fase 02)

### 3.1 · Riassunto e sintesi

La fase 02 ha trasformato la ricognizione in una **procedura eseguibile di generazione Normal** e
ha deciso i due riusi candidati. Ha fissato `Ts_base`, burn-in, generatore pseudocasuale, score e
regole sui fallimenti; ha quindi verificato replay, compatibilità descrittiva col generatore legacy,
coincidenza dei prefissi e guardia sul riuso. Il verdetto indipendente è **OK** per chiudere la fase
e passare alla fase 03 ([report](../studio2/fase02/REPORT_FASE02.md),
[verifica](../studio2/fase02/VERIFICA_FASE02.md)).

L'esito non è una calibrazione già conclusa: soglia, rango, numerosità e FAR realizzato sono ancora
assenti dal [freeze](../studio2/fase02/validation/PRECALIBRATION_FREEZE.json), come previsto. Non
sono stati selezionati i nuovi fault, generati i run finali o avviate inferenze LLM. L'accordo
osservato nei gate autorizza la configurazione nel perimetro provato; **non dimostra** indipendenza
matematica dei flussi, equivalenza generale Philox–legacy o validità fuori dalle configurazioni
esaminate.

### 3.2 · Dettaglio

#### Conservazione e provenienza

Il [manifest di conservazione](../studio2/fase02/MANIFEST_CONSERVAZIONE.csv) collega 78 percorsi
logici a **74 contenuti distinti**, identificati per SHA-256. I contenuti occupano 144.745.600 byte
distinti contro 152.308.644 byte logici. Il [registro di provenienza](../studio2/PROVENIENZA.md)
separa conservazione, candidatura e uso autorizzato e lascia esplicitamente mancanti seed, data di
generazione e `Ts_base` storici quando non sono recuperabili.

Il [record di storage](../studio2/fase02/ARTIFACT_STORAGE.json) registra la release pubblica
`studio2-fase02-v1`, il commit dati `6d238929285e57c6c70f4d563ef7e30b59da6ac5` e una verifica
per nuovo download dei due archivi: **74 workbook legacy e 150 output di validazione**, zero
mismatch. Questo record è successivo al riesame indipendente, che al momento del proprio verdetto
segnalava ancora il trasferimento come in corso; perciò la pubblicazione è documentata
dall'artefatto corrente, non attribuita retroattivamente al verificatore.

#### Specifica, generatore e score

La [specifica](../studio2/fase02/SPECIFICA_GENERAZIONE.md) e la sua
[forma machine-readable](../studio2/fase02/generation_spec.json) fissano `Ts_base=0.0005 h`, uscita
ogni minuto, finestre utili da 5 h e Philox4×32-10 con namespace di stream separati. Distinguono
trip fisici, trip Normal e fallimenti tecnici, impedendo sostituzioni o rilanci selettivi basati
sull'esito.

Lo [score congelato](../studio2/fase02/validation/score_fit_legacy.json) seleziona la variante A:
la dominanza massima osservata sulla `baseline_fit` è **0,48**, sotto il limite 0,70 della regola
pre-specificata. Il file contiene otto parametri robusti e 164 riferimenti per sensore; la MAD è
non riscalata e i casi degeneri arrestano il calcolo invece di introdurre sostituzioni silenziose.

#### Gate numerici

La procedura sui dieci stream Normal confronta i candidati 10/20/30/40 h con l'intervallo tardivo
`[60,70)` e richiede due candidati consecutivi. Il
[risultato burn-in](../studio2/fase02/validation/burn_in_result_v2.json) registra il passaggio di
20 e 30 h e seleziona **20 h**.

Il [confronto Philox–legacy](../studio2/fase02/validation/generator_comparison_result_v2.json)
passa tutte le cinque metriche — quattro famiglie di feature e `S` — sui dieci run per generatore.
Il [gate dei prefissi](../studio2/fase02/validation/prefix_result_v2.json) passa **100/100**
confronti su dieci stream e dieci posizioni: differenze massime nulle per uscite, feature e score,
contatori crescenti e J10 uguale al run pieno per tutti gli stream. Sono risultati descrittivi e
configurazione-specifici, non una prova di equivalenza universale.

#### Decisioni R1 e R2

La [qualificazione del riuso](../studio2/fase02/QUALIFICAZIONE_RIUSO.md) chiude separatamente i due
candidati:

- **R1 è respinto come sostituzione**: i 20 fault storici restano materiale già osservato, perché
  seed, data, `Ts_base` e configurazione effettivamente eseguita non sono ricostruibili;
- **R2 è autorizzato condizionatamente soltanto come `baseline_fit`**. N1–N5 sono cinque blocchi
  contigui dello stesso tratto, non repliche indipendenti e non possono entrare in `cal_thr`,
  `far_ver` o test. La [guardia R2](../studio2/fase02/validation/r2_guard_result_v2.json) passa le
  quattro famiglie e `S`; per `S` registra scarto **0,389889 MAD** e rapporto MAD **0,956200**.

L'analisi R2 era **pre-specificata rispetto all'uso nel nuovo studio**, ma usa dati storici già
osservati e non è cieca rispetto a essi. Se identità dei dati, codice, parametri o verifica
decadono, il fallback fissato è 100 nuovi run `baseline_fit`, 300 `cal_thr` e 150 `far_ver`.

#### Budget e stato del congelamento

Il piano riconciliato assegna 150 simulazioni alla qualifica già conclusa, 40 allo sviluppo fault,
350 a `cal_thr`, 150 a `far_ver`, 54/72 al test in catalogo e 6 all'OOD: **750/768** simulazioni
scientifiche per 6/8 run a fault, con **600/618** residue
([piano, §8.8](paper/FoT_TEP_Review_Piano_Sperimentale.md)). Le ripetizioni tecniche non cambiano
questo budget scientifico.

Il [freeze pre-calibrazione](../studio2/fase02/validation/PRECALIBRATION_FREEZE.json), schema 2,
elenca **41 file e cinque manifest eseguiti** per contenuto. Il verificatore aveva controllato la
versione precedente con 40 file più cinque manifest; il quarantunesimo è il record di storage
aggiunto in seguito. Lo stato corrente resta correttamente
`content_frozen_and_data_archived_pending_independent_reverification_and_commit`: gli artefatti
sono stati committati e il freeze è stato rigenerato sull'HEAD che li contiene; resta il controllo
indipendente finale delle impronte. Nessun tag di congelamento è stato creato.

### 3.3 · Connessione alla letteratura

La fase non introduce un claim bibliografico nuovo. Applica invece i vincoli già raccolti in
[`letteratura.md`](letteratura.md) §14.2: Bates et al. e Vovk impongono di non confondere garanzia
marginale, legge condizionale alla calibrazione e FAR osservato, mentre Marques F. distingue la
copertura empirica sotto scambiabilità dall'errore condizionale su un punto futuro. Di conseguenza
la separazione degli stream e l'identità della procedura sostengono l'assunzione di progetto, ma
non la dimostrano; N1–N5 contigui non vengono promossi a unità scambiabili.

Le §§14.5–14.6 restano invariate: conservazione, RNG e score sono infrastruttura metodologica, non
la novità del lavoro. L'eventuale contributo resta nell'intersezione fra trasferimento testuale,
serie multivariate, esperienza disgiunta per classe e controllo A/B/E, che questa fase non ha
ancora valutato.

### 3.4 · Connessione alle critiche

La fase **mitiga**, ma non chiude, G9 (*feature e soglie fisse*): rende eseguibili la variante A,
la futura calibrazione su nuovi Normal e la verifica FAR su un insieme separato. Mitiga inoltre i
rischi operativi di provenienza opaca, RNG non riproducibile e rerun selettivi. Non chiude C07
(*reasoning cap e parsing*), che appartiene al capability pilot, né le critiche su scala/Big Data,
local-seen, dipendenza dal producer e OOD. Non produce ancora alcun effetto diagnostico.

### 3.5 · Artefatti e riproducibilità

- Chiusura: [`REPORT_FASE02.md`](../studio2/fase02/REPORT_FASE02.md), SHA-256
  `fa555197b9421f073d65f9cfb34aa7f06762fc0377ab26bad76ef60da47641d2`.
- Verifica indipendente: [`VERIFICA_FASE02.md`](../studio2/fase02/VERIFICA_FASE02.md), SHA-256
  `34c8df542c1ee6dc9b3169d4ef53aba9eca726f15a92547bd28065178b903183`; verdetto **OK**, con il
  limite temporale sul trasferimento dati descritto sopra.
- Freeze corrente: [`PRECALIBRATION_FREEZE.json`](../studio2/fase02/validation/PRECALIBRATION_FREEZE.json),
  SHA-256 `be01fe4cccf6e9f3c9d82e8de69e426aa68b80d3e106bac81fa29dfb325bf085`.
- Storage pubblico: [`ARTIFACT_STORAGE.json`](../studio2/fase02/ARTIFACT_STORAGE.json), SHA-256
  `74eae7b154524ce3fd4667cd68accebbc658c8cf1521e256d50de17282eab4a5`.
- Codice, piani, manifest e risultati numerici sono sotto [`studio2/fase02/`](../studio2/fase02/);
  gli originali congelati del primo studio non sono stati modificati.

### 3.6 · Lavoro che resta

Restano la selezione e generazione dei nuovi fault, `cal_thr` e `far_ver`, la produzione delle
feature/evidence e dei prototipi, le decisioni di catalogo, il capability pilot e tutte le
inferenze LLM. Prima di dichiarare definitivo il congelamento della fase 02 resta la riverifica
indipendente finale delle impronte del freeze rigenerato.

---

## 4–12 · Fasi successive

Le fasi successive vengono da **§6** (i cantieri di preparazione indipendenti dal modello ancora
da eseguire) e **§7** (esecuzione subordinata alla disponibilità di Qwen) del piano sperimentale.

<a id="criteri-selezione-61"></a>

### 4.1 · Fase 03 — criteri di selezione dei fault (§6.1)

#### Riassunto e sintesi

La sotto-fase decisionale §6.1 ha definito i criteri prima di eseguire D1 o consultare risultati
per-fault dei nostri esperimenti. La [verifica indipendente](../studio2/fase03/selection/VERIFICA_CRITERI_6_1.md)
ha dato **OK** alla prespecificazione e alla fattibilità. Il congelamento dedicato riguarda
esclusivamente i criteri: **alla chiusura di §6.1 il catalogo non era ancora estratto**.
L’esito successivo D1 è in [§4.2](#catalogo-d1); la Fase 03 resta aperta. La fonte della decisione è il
[registro dei criteri](lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md), collegato dal piano §6.1.

#### Dettaglio della decisione

Il disegno prespecificato mantiene F1/F8/F10/F13 come quattro classi di continuità, con quattro nuovi
fault nell'universo IDV(1)–IDV(15). I vincoli congiunti fissano almeno due step, due random
variation, due sticking valve e un solo slow drift, IDV(13); vietano le coppie con identica
variabile perturbata {3,9}, {4,11}, {5,12}; richiedono almeno due membri dello strato nominale
H={F3,F9,F15}, difficile da rilevare secondo le fonti esterne prescritte. Il complemento è
«ordinario rispetto alla stratificazione», senza dichiarazione di facilità diagnostica.

Il [controllo combinatorio](../studio2/fase03/selection/FEASIBILITY.json) conta **330 quadruple
candidate e 12 ammissibili**: cinque con composizione step/random/drift/sticking 3/2/1/2 e sette
con 2/3/1/2. F14/F15 sono quindi inclusioni forzate dai criteri; entra esattamente uno fra
F3 e F9. Nella sotto-fase §6.1 nessun catalogo è stato sorteggiato. Il registro prespecifica seed `20260913`,
ordinamento e procedura riproducibile di D1, senza rilanci per cambiare esito.

La quota di due fault per famiglia è una scelta di progetto: non deriva da una legge
bibliografica e non garantisce generalizzabilità al meccanismo o potenza inferenziale.
La continuità non diventa un campione casuale e i suoi run storici non sostituiscono i nuovi
run di sviluppo. Il risultato sul drift rimane riferito a IDV(13).

#### Connessione alla letteratura

La tassonomia usa Downs & Vogel, richiamati in [`letteratura.md`](letteratura.md) §14.3;
la stratificazione segue i riferimenti già prescritti dal piano §12. Il
[record delle fonti](../studio2/fase03/selection/SOURCE_CHECK.json) identifica i PDF primari
consultati e riverificati. La PHM 2023 conferma direttamente il gruppo nominale H; il testo
integrale di Yin 2012 non è stato riverificato e i suoi range non entrano nel filtro.

È stata corretta nel piano §12.2 la richiesta incoerente di FDR sotto il 10% in tutti i metodi,
che contraddiceva i range dello stesso §12.1. Non è stata introdotta una nuova soglia dai massimi.
Gli FDR esterni riguardano rilevazione, non diagnosi FoT. Non nasce un nuovo claim bibliografico:
§§14.5–14.6 del corpus restano invariati.

#### Connessione alle critiche e limiti

La prespecificazione mitiga la selezione del catalogo in base agli esiti, ma non dimostra
rappresentatività su tutti i fault TEP. L'audit può verificare artefatti e operazioni registrate,
non l'assenza di conoscenza pregressa. Downs & Vogel raccomandano perturbazioni congiunte per
IDV(14)–IDV(20) e 24–48 ore per osservarne l'effetto completo: la futura specifica di generazione
deve esplicitare il rapporto col disegno a singolo fault **prima dei nuovi run**, senza scegliere
in base al segnale osservato. La copertura tassonomica non dimostra rilevabilità.

#### Artefatti e riproducibilità

Il [report](../studio2/fase03/selection/REPORT_CRITERI_6_1.md) e la
[verifica](../studio2/fase03/selection/VERIFICA_CRITERI_6_1.md) sono specifici della sotto-fase.
Il [freeze dei criteri](../studio2/fase03/selection/CRITERIA_FREEZE.json) registra commit sorgente,
impronte e perimetro. Il piano è registrato come snapshot al commit sorgente e resta aggiornabile
nelle parti estranee ai criteri; il tag dedicato è `studio2-fase03-criteri-selezione-frozen-001`.
Il [controllo di consegna](../studio2/fase03/selection/DELIVERY_CHECK.json) registra parità
MD/HTML, link, impronte e verifiche offline. Il controllo documentale generale mantiene
**35 test, 14 fallimenti preesistenti e 1 skipped**; non copre direttamente i nuovi criteri.

Il branch pilot integrato con questa consegna comprende 13 commit `studio2(fase03)` fino a
`6a02927`. I suoi file sono conservati invariati. I 16 test offline passano e i comandi di
preparazione restano a zero chiamate; ciò non è un nuovo audit scientifico del pilot.
Il suo [preflight](../studio2/fase03/PREFLIGHT_03_0.md) e lo
[stato implementativo](../studio2/fase03/IMPLEMENTATION_STATUS.md) continuano a dichiarare
sospeso il gate reale. La sonda sintetica provvisoria non fonda la scelta dei criteri.

#### Lavoro che resta

Alla chiusura di §6.1 restava da eseguire D1. L'estrazione e la sua verifica sono ora
registrate in [§4.2](#catalogo-d1); il catalogo è ora congelato e pubblicato.
D11 e la scelta OOD sono ora lavorabili ma restano aperte. Restano inoltre D2, producer
alternativo, nuovi run ed evidence reali, sonda sui prompt reali e gate 40×3.
La sola chiusura di §6.1 non chiude S1 e non autorizza esecuzioni.

<a id="catalogo-d1"></a>

### 4.2 · Fase 03 — estrazione, verifica e congelamento del catalogo D1

#### Riassunto e sintesi

L'estrazione applica i criteri già congelati in §4.1. Il catalogo risultante è **F1, F2, F3,
F8, F10, F13, F14, F15**. La [verifica indipendente](../studio2/fase03/selection/VERIFICA_CATALOGO_D1.md)
ha dato inizialmente NON OK per tre problemi di tracciabilità, poi **OK** dopo le correzioni.
L'esito e il log originali sono rimasti invariati. Il catalogo è **congelato e pubblicato**
con il tag annotato `studio2-fase03-catalogo-D1-frozen-001`, sul commit `ab43f0b` integrato in
`origin/main`. La pubblicazione è stata verificata dopo l'autorizzazione dell'autore.

L'[appendice 01 alla verifica](../studio2/fase03/selection/VERIFICA_CATALOGO_D1_APPENDICE_01.md)
colma un'omissione del verbale originario: attesta esplicitamente, leggendo il registro al tag
rev. 1 dei criteri, che seed, namespace, ordinamento e regola completa di estrazione erano già
prescritti prima di D1. È un riscontro documentato successivamente, senza nuovo sorteggio;
il verbale congelato e i tag restano intatti.

#### Dettaglio dell'estrazione

Il [log originale](../studio2/fase03/selection/D1_DRAW_LOG.json) registra le 330 quadruple
candidate e le 12 ammissibili nell'ordine prespecificato. Namespace `studio2-fase03-D1-v1`,
seed `20260913`, contatore accettato **0**, nessun rifiuto e indice estratto **0** producono
la quadrupla nuova **F2/F3/F14/F15**. Il digest completo è
`0116bf108b82d515210233f433caa65f0b91d9fe46a18fc9d25a1294b8a644f0`.

| Fault | Meccanismo | Strato | Origine |
| --- | --- | :---: | --- |
| F1 | step | O | continuità |
| F2 | step | O | nuovo |
| F3 | step | H | nuovo |
| F8 | random variation | O | continuità |
| F10 | random variation | O | continuità |
| F13 | slow drift | O | continuità |
| F14 | sticking valve | O | nuovo, forzato dai vincoli |
| F15 | sticking valve | H | nuovo, forzato dai vincoli |

Il [manifest del catalogo](../studio2/fase03/selection/CATALOG_FREEZE.json) registra
composizione step/random/drift/sticking **3/2/1/2**, H={F3,F15} e otto chiavi distinte.
F14/F15 erano già forzati dai criteri; l'indice zero è il risultato del digest, non una scelta
manuale del primo catalogo. I replay di audit non sono rilanci per cambiare esito.

#### Connessione alla letteratura

D1 usa la tassonomia e lo strato H trascritti nel registro congelato, già verificati sulle
fonti primarie. Non aggiunge proprietà dei fault o nuove conclusioni bibliografiche.
Valgono i riferimenti e i limiti di §4.1 e di [`letteratura.md`](letteratura.md) §14.3;
la conoscenza esterna di rilevazione non predice la diagnosi nel futuro esperimento.

#### Connessione alle critiche e limiti

La riproduzione indipendente conferma che l'esito segue la procedura prespecificata. Non
prova la rappresentatività del catalogo né l'assenza di consultazioni private non registrate.
Il catalogo non è stato selezionato usando risultati per-fault dei nostri esperimenti.
Prima di generare run resta obbligatorio esplicitare nella specifica il rapporto fra
IDV(14)/IDV(15), disegno a singolo fault e raccomandazione Downs & Vogel sulle perturbazioni
congiunte e sulle 24–48 ore. Il risultato sul drift resta limitato a IDV(13).

#### Artefatti e riproducibilità

Il [report D1](../studio2/fase03/selection/REPORT_CATALOGO_D1.md) distingue l'esecuzione
originaria dalle correzioni. Lo [snapshot dello script eseguito](../studio2/fase03/selection/execution_snapshot/draw_d1.py)
e il log originario sono conservati byte per byte. Lo [script corrente di replay](../studio2/fase03/selection/draw_d1.py)
verifica il contesto congelato prima del sorteggio, conserva il commit storico dopo
l'avanzamento di HEAD e protegge il log originale. **Quattro test di regressione passano**,
compreso il replay byte-identico in un contesto Git successivo.

[CRITERIA_FREEZE_rev002.json](../studio2/fase03/selection/CRITERIA_FREEZE_rev002.json) è una
revisione amministrativa: sotto `criteria_origin` conserva i metadati storici della rev1,
che resta intatta; il nuovo stato D1 è attestato dalla propria verifica e dal tag
`studio2-fase03-catalogo-D1-frozen-001`. Il tag dei criteri non attesta la rev002.
Il [controllo del riesame](../studio2/fase03/selection/D1_REVIEW_CHECK.json) e il
[controllo documentale](../studio2/fase03/selection/D1_DELIVERY_CHECK.json) riportano verifiche
e impronte. Il test documentale generale mantiene **35 test, 14 fallimenti preesistenti e
1 skipped**. Non sono state eseguite inferenze scientifiche o simulazioni.

I manifest e i verbali nel tag conservano i byte verificati e lo stato storico precedente alla
pubblicazione (`catalog_frozen=false`); le loro condizioni di efficacia sono ora soddisfatte.
Lo stato efficace `catalog_frozen=true`, il commit completo, l'oggetto del tag e le impronte
sono registrati nell'[attestazione di pubblicazione](../studio2/fase03/selection/CATALOG_PUBLICATION.json).
Il [resoconto di pubblicazione](../studio2/fase03/selection/PUBBLICAZIONE_CATALOGO_D1.md) distingue
commit, controlli documentali e attività rimaste aperte. Il tag non è stato spostato e gli
artefatti congelati non sono stati riscritti.

#### Passaggi ancora aperti

Restano D2, producer alternativo, specifica di generazione,
nuovi run/evidence e gate reale 03.0. OOD e D11 sono ora lavorabili: la
[nota di proposta](../studio2/fase03/selection/PROPOSTA_OOD_D11.md) resta non vincolante e
**fuori dal congelamento D1**. Questa consegna non sceglie il secondo fault OOD, non approva
coppie D11 e non chiude la Fase 03.

<a id="run-fault-62"></a>

### 4.3 · Fase 03 — run fault di sviluppo (§6.2)

#### Riassunto e sintesi

La sotto-fase §6.2 ha generato i **40 run fault di sviluppo** previsti dal piano: gli otto
fault del catalogo congelato F1/F2/F3/F8/F10/F13/F14/F15, cinque batch per fault, un solo IDV
per run e nessun cambio di setpoint, sugli stream Philox 30000–30039. Tutti i 40 run sono
`complete`, senza trip fisici né errori tecnici, e ciascuno dichiara complete le otto finestre
post-fault da 5 h (320/320). I dati, esclusi da Git, sono pubblicati su `fot-tep-data` nella
release `studio2-fase03-fault-dev-v1`; la copia remota è stata verificata per riscaricamento due
volte — dalla finestra di lavoro e dalla verifica indipendente — con zero mismatch su 240 file. La
[verifica indipendente](../studio2/fase03/fault_runs/VERIFICA_RUN_FAULT.md) ha dato **OK, con
condizioni** documentali e di conservazione; il replay MATLAB, unica prova sperimentale mancante
al momento del verdetto, è stato poi eseguito dall'autore e riverificato dal verificatore sugli
artefatti (Appendice A). Il [report di chiusura](../studio2/fase03/fault_runs/REPORT_RUN_FAULT.md)
è l'indice della sotto-fase; i numeri di questa sezione vengono dagli artefatti che esso elenca.

Questa consegna chiude la sotto-fase dei run fault di sviluppo, **non la macro-Fase 03**. I 40 run
sono materiale di sviluppo, non di valutazione: da essi non sono ancora state estratte feature,
evidence o verbalizzazioni; non esistono insight, prototipi, soglie o score; nessuna chiamata a
modelli linguistici è stata effettuata durante generazione, audit, prove di equivalenza,
conservazione o documentazione. Per scelta, questa sezione non riporta alcuna osservazione sul
segnale diagnostico dei run: leggerla non anticipa nulla sulle fasi successive.

#### Dettaglio

Le sotto-fasi sono descritte nell'ordine in cui sono state eseguite; i commit citati sono sul
branch `codex/studio2-fault-runs`, tutti del 2026-09-13.

##### Specifica pre-esecuzione

La [specifica originale](../studio2/fase03/fault_runs/SPECIFICA_RUN_FAULT.md) è stata fissata al
commit `c02111d` (11:56 CEST), **prima** di piano, generatore, compilazione e batch; la sua
impronta `14d36742…` è registrata come `spec_sha256` nei 40 manifest e nel manifest dello smoke,
e il file ha un solo commit nella sua storia. Prescrive il catalogo dal tag
`studio2-fase03-catalogo-D1-frozen-001` — [`CATALOG_FREEZE.json`](../studio2/fase03/selection/CATALOG_FREEZE.json),
SHA-256 `68b8461a…`, identico al tag, a HEAD e nei `dependency_hashes` dei 40 manifest — e
mantiene gli invarianti della Fase 02: `Ts_base` 0,0005 h, uscita ogni 1/60 h, burn-in 20 h,
Philox4×32-10 con chiave `0x464f545445503032` e flusso uguale all'indice, MSFlag 0, solver
`ode45`, stato iniziale `Mode1xInitial.mat` fra le dipendenze hashate; il modello
`MultiLoop_mode1.mdl` non è stato salvato e gli override (ritardo 25/25 h, nome della
S-function) sono in memoria e registrati in `model_overrides`. Per ogni run: innesco a 25 h,
orizzonte post-fault 40 h, termine a 65 h, otto finestre half-open da 5 h, e una finestra di
controllo negativo interno [20,25) marcata `development_eligible=false` in tutti i manifest ed
esclusa dallo sviluppo.

La specifica contiene la decisione dell'autore, presa **prima** dei nuovi dati, di studiare
**F14 e F15 come fault singoli**, in deviazione dichiarata dalla raccomandazione di Downs & Vogel
(pp. 250–251) di accoppiare IDV(14)–(20) a un altro disturbo o a un cambio di setpoint; l'orizzonte
di 40 h ricade nelle 24–48 h suggerite, ma nessuna fonte dimostra che basti. La regola
preregistrata è che **segnale debole o assente in F14/F15 è un esito da registrare**: dopo
l'osservazione non si aggiungono disturbi, non si allunga l'orizzonte, non si cambiano le
finestre, non si sostituiscono run o fault. La specifica prescrive anche il gemello strumentato
del simulatore, senza poterne preregistrare l'hash binario. Le provenienze delle convenzioni riusate
(40 h post-fault e otto finestre traslate da 10 a 25 h, launcher e generatore gemelli della Fase
02) sono in [`PROVENIENZA.md`](../studio2/PROVENIENZA.md) §7 con marca **pre-specificato**; lo
stesso registro dichiara un'esposizione incidentale alla tabella narrativa di risultati per-fault
del primo studio, senza uso di alcun suo valore e senza rivendicare cecità assoluta.

##### Piano e generatore

Il commit `55d442b` aggiunge [`build_generation_plan.py`](../studio2/fase03/fault_runs/build_generation_plan.py),
che produce il [piano](../studio2/fase03/fault_runs/plans/fault_dev.csv) di 40 righe (SHA-256
`583f4316…`): `run_id` `fault-dev-F<idv>-b0<b>`, `run_index_uint64 = stream_id = 30000 + 5k +
(b−1)` con `k` posizione del fault nel catalogo, formula verificata vera su tutte le 40 righe.
L'intervallo 30000–30039, con 30040 riservato allo smoke, è disgiunto da tutti gli indici usati
nella Fase 02 (`0–9`, `100–109`, `200–209`, `1000–1009`, `999999`) e dalle sue prenotazioni
(`2000–2099`, `10000–10349`, `20000–20149`). Lo stesso commit aggiunge
[`prepare_simulator.py`](../studio2/fase03/fault_runs/prepare_simulator.py), che accetta solo il
sorgente base con impronta `230086e7…` e vi inserisce blocchi diagnostici delimitati,
[`compile_fault_philox.m`](../studio2/fase03/fault_runs/compile_fault_philox.m) e il launcher
[`generate_fault_runs.m`](../studio2/fase03/fault_runs/generate_fault_runs.m), gemello di quello
Normal: manifest per tentativo, destinazione protetta, gestione di trip e fallimenti tecnici,
registrazione dell'hash del MEX in ogni manifest.

##### Test

Il commit `88eb34e` aggiunge [`tests/test_fault_runs.py`](../studio2/fase03/fault_runs/tests/test_fault_runs.py):
**21 test offline** su piani, manifest, log e strumentazione, ripassati dal verificatore. Fra questi
il round-trip del sorgente: `instrument(base)` riproduce byte per byte il sorgente strumentato su
disco e `strip_instrumentation(strumentato)` riproduce il sorgente base.

##### Smoke F1/30040

Il commit `49d5806` (12:16 CEST) registra l'unico smoke, [`smoke/f1_short_001/`](../studio2/fase03/fault_runs/smoke/f1_short_001/):
un solo run, F1, stream `30040`, orizzonte post-fault ridotto a 0,1 h e termine a 25,1 h, 1507
righe × 54 colonne, nessuna finestra post-fault completa, `complete`, contatore Philox finale
152981172, HEAD di esecuzione `88eb34e` e MEX `834e2361…` nel manifest. L'attivazione osservata è a
25,000410376861183 h; il controllo della composizione interna del flusso 4, con tolleranza `1e-10`,
è il check di attivazione prescritto dalla specifica §7 e il
[report dello smoke](../studio2/fase03/fault_runs/smoke/REPORT_SMOKE.md) nega esplicitamente che
sia un risultato di separabilità. La proiezione lineare del tempo di batch (circa 16,6 minuti) è
dichiarata come tale. Lo stesso commit consegna il batch all'autore
([`HANDOFF_BATCH.md`](../studio2/fase03/fault_runs/HANDOFF_BATCH.md)) e contiene la prima versione
di `REPORT_RUN_FAULT.md`, che descrive la consegna pre-batch ed è stata poi riscritta in luogo alla
chiusura: chi legge il `git_commit` dei manifest deve saperlo.

##### Batch, con il tentativo di lancio abortito

Il primo tentativo di avvio in background non ha prodotto run né output parziali: il processo è
stato terminato dalla sandbox al termine della finestra di esecuzione, `matlab.log` è rimasto
vuoto (0 byte) e il PID registrato è `94590`. L'evidenza è conservata in
`runtime/batch_launch_failed_20260913T122247/` (due file, inclusi nell'archivio pubblico) e in
`failed_launch_attempts_recoverable` di [`BATCH_SUMMARY.json`](../studio2/fase03/fault_runs/BATCH_SUMMARY.json).
Il batch è stato rilanciato da un terminale esterno con piano, stream e destinazione invariati:
`campaign_start` alle 10:23:12 UTC e `campaign_end` alle 10:28:44 UTC in
`runs/fault_dev_001/events.jsonl`, 82 righe (1 + 40 + 40 + 1) con timestamp monotòni.

Esito, dai 40 `*.manifest.json` e da `BATCH_SUMMARY.json`: **40/40 `complete`**, 0 trip fisici,
0 errori tecnici, 0 `not_run`, **320/320 finestre post-fault complete**, 3901 righe × 54 colonne
per run (griglia `0, 1/60, …, 65` h), durata totale **330,764 s** (somma dei `runtime_seconds`;
simulazione pura 323,231 s), commit di esecuzione `49d5806` in tutti i manifest. Gli stream sono
esattamente `30000…30039`, univoci, con `stream_id = run_index_uint64` e IDV uguale al piano. Gli
onset osservati stanno fra **25,00007946967903 h** e **25,0005 h**, cioè entro un passo `Ts_base`
dal nominale: nei 40 log del simulatore c'è una sola riga `FOT_IDV` per run, con maschera
`1 << (idv−1)`, e nei 40 `*.diagnostics.csv` la colonna `idv_mask` è nulla prima e pari alla
maschera dopo. L'attivazione nominale non va presentata come un istante osservato esatto. Il
[riepilogo](../studio2/fase03/fault_runs/BATCH_SUMMARY.json) non registra anomalie.

##### Manifest e riepilogo

Il commit `fe771e5` registra [`MANIFEST_FAULT_DEV.csv`](../studio2/fase03/fault_runs/MANIFEST_FAULT_DEV.csv)
(SHA-256 `9eaed0e9…`), derivato in sola lettura dai 40 manifest per-run, il `generation_manifest.csv`
della campagna (SHA-256 `69a7f2f9…`, coerente campo per campo con i manifest JSON) e
`BATCH_SUMMARY.json`. I 200 hash di output, diagnostiche, log, manifest per-run e attempt (5 × 40)
coincidono con i file su disco.

##### Conservazione e MEX record

Il commit `49f1229` pubblica i dati ignorati da Git — `runs/` e `runtime/` — nel repository
[`sorrentinoluca/fot-tep-data`](https://github.com/sorrentinoluca/fot-tep-data), release
[`studio2-fase03-fault-dev-v1`](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-fault-dev-v1),
commit `6d238929285e57c6c70f4d563ef7e30b59da6ac5`, pubblicata alle 11:06:10 UTC. L'asset
`studio2-fase03-fault-dev-v1.tar` ha **208.257.536 byte** e SHA-256 `6edd96711d29…`; contiene
**240 file per 207.757.349 byte**: 213 sotto `runs/fault_dev_001/` (5 file × 40 run, `events.jsonl`,
`generation_manifest.csv` e 11 file di cache Simulink), 2 sotto la directory del tentativo abortito e
25 sotto `runtime/mex_equivalence/`. Il [manifest di conservazione](../studio2/fase03/fault_runs/MANIFEST_CONSERVAZIONE.csv)
li elenca con percorso, byte e SHA-256; il [record di storage](../studio2/fase03/fault_runs/ARTIFACT_STORAGE.json)
ha stato `public_release_verified_by_redownload`, con riscaricamento in una directory temporanea
fuori dal repository e 240/240 file coincidenti. La verifica indipendente ha riscaricato l'asset una
seconda volta, in un contenitore separato: stesso SHA-256, 240/240 file, 0 mismatch. Questa
sotto-fase applica la convenzione di [`MAINTENANCE.md`](MAINTENANCE.md) §8.5 e l'obbligo di verifica
per riscaricamento di `Commit_LLM.md` §7, introdotti dal commit `6851bb6` (12:41 CEST, genitore
`fe771e5`); il messaggio di quel commit, `docs: Fix artifact publication/verif convention`, non
segue il formato `studio2(<ambito>): <azione>` di §8.3, e lo si annota senza correggerlo.

Lo stesso commit aggiunge [`MEX_RECORD.md`](../studio2/fase03/fault_runs/MEX_RECORD.md) e la
[revisione 2 della specifica](../studio2/fase03/fault_runs/SPECIFICA_RUN_FAULT_rev002.md). Il MEX
usato nei 40 run è il gemello strumentato `temexd_fault_philox.mexmaca64`, SHA-256
`834e2361…`, compilato il 2026-09-13 alle 12:03 CEST su macOS Apple Silicon con MATLAB R2025b
Update 6 e Xcode/Clang, dal sorgente `temexd_fault_philox.c` (SHA-256 `74bf641b…`), derivato dal
sorgente congelato della Fase 02 (`230086e7…`) con **35 inserimenti e 1 cancellazione**: il nome
della S-function, due campi diagnostici appesi in coda alla struttura dati, e stampe a sola lettura
di maschera IDV, variabili interne e trip, senza scritture su equazioni, stato Philox, ordine delle
estrazioni, XMEAS o XMV — diff ricostruito indipendentemente dal verificatore. L'equivalenza col
MEX base `6ae7e7be…` è dimostrata su tre lati:

- il Normal `burnin_qual-001` della Fase 02 rigenerato col MEX strumentato: **7/7 membri ZIP
  byte-identici**, 4201 × 54, contatore Philox finale **423367045** uguale al manifest di Fase 02;
  42 byte diversi nel contenitore, tutti timestamp DOS;
- F1/30000 rigenerato col MEX base: CSV **byte-identico** al run della campagna, 3.817.751 byte,
  SHA-256 `acb4c4ec…`, contatore **383902344** uguale al manifest del run;
- F1/30000 rigenerato col MEX strumentato, dopo la verifica (Appendice A, sotto).

La revisione 2 fissa il criterio documentale che ne segue: `mex_sha256` dei manifest deve essere
uguale all'hash del MEX **strumentato**, non a quello del MEX base; non cambia catalogo, indici,
stream, onset, orizzonte, finestre o dati, e l'originale resta intatto (solo blocchi aggiunti, nessuna
riga rimossa). L'hash binario vale per questa campagna: su altre piattaforme il binario va
ricompilato e la portabilità è garantita dal sorgente e dalle prove, non dall'hash.

##### Chiusura

Il commit `3b9ec1e` (13:11 CEST) riscrive `REPORT_RUN_FAULT.md` nella forma finale, aggiorna
[`IMPLEMENTATION_STATUS.md`](../studio2/fase03/IMPLEMENTATION_STATUS.md) — run fault disponibili,
gate reale ancora sospeso — e registra la sotto-fase in [`PROVENIENZA.md`](../studio2/PROVENIENZA.md)
§8, con le marche **pre-specificato** per piano e specifica, «documentazione post-esecuzione» per il
manifest aggregato ed «equivalenza verificata post-esecuzione» per il MEX. I sette commit della
sotto-fase hanno perimetro omogeneo e messaggi nel formato di §8.3; nessun tag è stato creato e il
branch non è stato pubblicato. Gli artefatti congelati non sono stati toccati: il diff da
`origin/main` fuori da `studio2/fase03` riguarda solo `DOCUMENTATION_INDEX.md`, `MAINTENANCE.md`,
`Commit_LLM.md` e `PROVENIENZA.md`.

##### Verifica indipendente

La [verifica](../studio2/fase03/fault_runs/VERIFICA_RUN_FAULT.md), svolta in un'altra finestra con
un altro modello e senza simulazioni né chiamate a modelli, ha risalito ogni numero al file o
all'oggetto git, mai al report. I sette controlli — catalogo, invarianti e indici, diff e hash del
MEX, equivalenza, conservazione, tracciabilità, perimetro del report — reggono tutti; le otto
osservazioni di §8 sono di tracciabilità e conservazione e non toccano catalogo, indici, stream,
onset, orizzonte, finestre, dati o copia remota. Il verdetto è **OK**, con la condizione
sperimentale §9.1 (replay MATLAB, non eseguibile dalla finestra di verifica) e le condizioni
documentali §9.2–§9.5, riportate sotto in «Lavoro che resta». Il verificatore ha anche confermato che
il report, lo smoke, il record MEX e lo stato implementativo non contengono valori, confronti o
commenti per-fault sui 40 run.

##### Replay

Dopo il verdetto l'autore ha rieseguito F1/30000 col MEX strumentato in
`runtime/mex_equivalence/fault_instrumented_30000_replay/`; il verificatore ha ricontrollato i file
senza prendere per buono il riepilogo (Appendice A del verbale). Il CSV grezzo è **byte-identico** al
run della campagna (SHA-256 `acb4c4ec…`); il log contiene 3901 righe `FOT_DIAG` e una sola riga
`FOT_IDV` a 25,0005 h con IDV(1), stampe che esistono solo nel MEX strumentato; le 3902 righe
`FOT_*` sono identiche a quelle del log originale; il contatore è 383902344; nessuna riga
`FOT_TRIP`. Un primo tentativo fallito per permessi di `fopen` non ha promosso file parziali. Con la
prova col MEX base il triangolo campagna–MEX base–MEX strumentato è chiuso sullo stesso stream, e la
condizione §9.1 è soddisfatta. La directory del replay sta in `runtime/`, ignorata da Git e **non
inclusa** nell'asset `6edd…`.

#### Connessione alla letteratura

La tassonomia dei meccanismi e la nota su IDV(14)–(20) sono di Downs & Vogel, richiamati in
[`letteratura.md`](letteratura.md) §14.3; la specifica ne cita direttamente le pp. 250–251 e ne
dichiara la deviazione. Il requisito posto in §4.1 e §4.2 — esplicitare nella specifica, **prima
dei nuovi run**, il rapporto fra IDV(14)/IDV(15), disegno a singolo fault e raccomandazione sulle
perturbazioni congiunte e sulle 24–48 h — è soddisfatto al commit `c02111d`. Non nasce un claim
bibliografico nuovo e §§14.5–14.6 restano invariati. Se la deviazione su F14/F15 avrà implicazioni
per quelle sezioni, si scriveranno là con `Letteratura_LLM.md`, non qui.

#### Connessione alle critiche

La sotto-fase **mitiga** il rischio di adattamento post-hoc e di rerun selettivi: specifica, regola
su F14/F15, piano e indici sono anteriori ai dati, e i fallimenti sono trattati come esiti. Mitiga
anche il rischio di provenienza opaca dei run, con manifest, hash e copia remota verificata.
**Lascia aperte**: la dipendenza fra le otto finestre dello stesso run, che non sono osservazioni
indipendenti; F14/F15 senza eccitazione congiunta, il cui esito non è ancora stato osservato e non
va osservato qui; il controllo interno [20,25), che è descrittivo e non è una prova di regime
stazionario. Restano aperte, come dopo la fase 02, G9 (*feature e soglie fisse*), C07
(*reasoning cap e parsing*) e le critiche su scala, local-seen, dipendenza dal producer e OOD. La
sotto-fase non produce alcun effetto diagnostico.

#### Artefatti e riproducibilità

- Chiusura: [`REPORT_RUN_FAULT.md`](../studio2/fase03/fault_runs/REPORT_RUN_FAULT.md), SHA-256
  `5fbd6750df832a21b2956128321c5e803c108f5db6b1ef72851873c0ee8b610b`.
- Verifica indipendente: [`VERIFICA_RUN_FAULT.md`](../studio2/fase03/fault_runs/VERIFICA_RUN_FAULT.md),
  SHA-256 `f3a0f7a75663a1ff3d5e4741a965ddea2c5f469dc711dcc77c7ffe45d35e1d6f`; verdetto **OK, con
  condizioni**; Appendice A per il replay.
- Specifica originale, commit `c02111d`: SHA-256
  `14d36742c158b1ca71b1adc848d13d6f7a85107530450b19a3e1d122eb063b2e`; revisione 2, commit `49f1229`:
  SHA-256 `a0bcfe9376024c68870fa0dc06fe98ed30a4a7900afdee81d878c7de6064d557`.
- Piano: SHA-256 `583f4316f3788abd23f687e19ba9494aa44087a7ce2c6b0c8263eec9147aa178`; manifest
  aggregato `MANIFEST_FAULT_DEV.csv`: `9eaed0e901c6f06d5aa94b4e2d81d5afdd3464022ae6d2709b92f872789a6d9d`;
  `generation_manifest.csv`: `69a7f2f97568a656a96e8eeb0871a6295b087d44b2ae7306fd09a5365e1f4f23`.
- Simulatore: sorgente base `230086e7712e753bf48f3e9108cd0ce2f68aba97d9590ebb3c7593a47f8b6d25`;
  sorgente strumentato `74bf641bcd16ce42093b3c78cf03887376d19561041f8746ccf01339042fb4c9`; MEX base
  `6ae7e7be5394773f1854f1c53eddbd778ad7557b61fb05a93b3edb0552b1d11e`; MEX strumentato
  `834e2361915249402a1ec9074a4be04f22a6404deb841e5134bf34347dfde544`
  ([`MEX_RECORD.md`](../studio2/fase03/fault_runs/MEX_RECORD.md), SHA-256
  `9d3885197133268105c2a9f6e9f65114384952fa1a269f365105870d48375725`).
- Conservazione: [`ARTIFACT_STORAGE.json`](../studio2/fase03/fault_runs/ARTIFACT_STORAGE.json), SHA-256
  `ac9fa82f0b0198252a060846105a3a162fd895f141b4cd7134c1a88f7d0a1262`;
  [`MANIFEST_CONSERVAZIONE.csv`](../studio2/fase03/fault_runs/MANIFEST_CONSERVAZIONE.csv), SHA-256
  `85930a16e6b59c4048ce5cedac79b83ad72606bea45207b8a7d6b7565f11d1b0`; asset
  `6edd96711d2913953c6de81ce6dbb7c51e7677a2a7c1892b0676de5e7a9fd97c`.
- Conservazione, rev002: [`ARTIFACT_STORAGE.json`](../studio2/fase03/fault_runs/ARTIFACT_STORAGE.json)
  ristrutturato a `schema_version` 2 (`releases[]`, `archive_root` dichiarato), SHA-256
  `9ca14c8cf5f8bbc78084cdbdd64e166d93b7246b47962dce5c3d15e5ed0b31b1`;
  [`MANIFEST_CONSERVAZIONE_rev002.csv`](../studio2/fase03/fault_runs/MANIFEST_CONSERVAZIONE_rev002.csv),
  SHA-256 `d8724cb964d487a2c12ae9d1d0f04bf2b2bc72e5fde442f52c50b153fba98ebb`; asset
  [`studio2-fase03-fault-dev-v2.tar`](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-fault-dev-v2),
  SHA-256 `5940fd417149d3ff92ee4c3d4f7826b80cb2b58b066eb2213b4ce38ac32a2527`, 20 file, verificato per
  riscaricamento con 0 mismatch; non riscrive l'asset v1.
- Commit della sotto-fase, in ordine: `c02111d`, `55d442b`, `88eb34e`, `49d5806` (esecuzione
  registrata nei manifest), `fe771e5`, `49f1229`, `3b9ec1e`; convenzione di pubblicazione al commit
  docs `6851bb6`. Sono riferimenti di provenienza, non tag di congelamento: nessun tag è stato creato.
- `runs/` e `runtime/` sono ignorati da Git: i loro contenuti si trovano sul disco dell'autore e, per
  i 240 file del manifest, nell'asset pubblico. Il controllo documentale generale mantiene **35
  test, 14 fallimenti preesistenti e 1 skipped**; non copre questa sezione.

#### Lavoro che resta

Le condizioni §9.2–§9.5 e le osservazioni §8 del verbale sono lavoro **documentale e di
conservazione**, non scientifico: nessuna richiede di toccare run, manifest, piano, specifica
originale o artefatti congelati.

- Il sorgente strumentato (con i due header) e il binario `834e…` non sono né in Git né
  nell'asset: il sorgente è riproducibile da `prepare_simulator.py`, il binario esiste solo sul
  disco dell'autore. Vanno conservati in una **nuova revisione** di `MANIFEST_CONSERVAZIONE.csv`,
  `ARTIFACT_STORAGE.json` e asset su `fot-tep-data`, senza riscrivere l'asset `6edd…` già
  verificato.
- Gli script MATLAB delle due prove di equivalenza e del replay non sono conservati accanto ai loro
  output; l'uso del MEX base in F1/30000 è dedotto dall'assenza di righe `FOT_`, non da un manifest.
  La directory del replay, con il resto di `runtime/mex_equivalence/` nuovo, va inclusa nella stessa
  revisione.
- Il log del lancio riuscito (`runtime/batch_launch/matlab.log` e `matlab.pid`) non è conservato,
  mentre lo è quello del tentativo fallito; l'informazione è ridondante con `events.jsonl` e i 40 log
  del simulatore, ma l'asimmetria va sanata nella stessa revisione.
- `MANIFEST_CONSERVAZIONE.csv` usa percorsi dalla radice del repository, l'archivio percorsi relativi
  a `fault_runs/`: la radice va dichiarata in `ARTIFACT_STORAGE.json`, e un formato unico del
  manifest per le fasi future resta da valutare, perché quello della Fase 02 ha uno schema diverso.
- Il tag `studio2-fase03-fault-dev-v1` non segue letteralmente `studio2-fase<N>-v<k>` di
  [`MAINTENANCE.md`](MAINTENANCE.md) §8.5: il formato per lotto va esplicitato lì, o l'eccezione registrata.
  Punto 4, risolto come rinvio di allineamento in [MAINTENANCE §8.6](MAINTENANCE.md#86-sotto-fasi-e-granularità-del-ciclo).
- Chiuso: la release `studio2-fase03-fault-dev-v2` conserva sorgente e binario del MEX strumentato,
  `matlab.log`/`matlab.pid` del lancio riuscito e la directory del replay (primi tre punti sopra),
  con `MANIFEST_CONSERVAZIONE_rev002.csv` e `ARTIFACT_STORAGE.json` §`archive_root` dichiarato.
  Restano non recuperabili, e dichiarati assenti, gli script MATLAB delle due prove di equivalenza
  e del replay (secondo punto sopra, solo la parte degli script).

Restano inoltre le dipendenze del report §7: estrazione pre-specificata di feature ed evidence dai
40 run; insight e prototipi delle sotto-fasi successive; manifest scientifico autonomo dei veri
input del pilot; nuovo controllo di capienza e autorizzazione esplicita prima di qualunque gate
LLM; decisioni D2, D11, OOD e producer alternativo; integrazione in `main` solo su richiesta
dell'autore. La macro-Fase 03 resta aperta.

<a id="soglie-normal-63"></a>

### 4.4 · Fase 03 — soglie Normal (§6.3)

#### Riassunto e sintesi

La sotto-fase 03.5 ha calibrato lo score combinato sui **350 run Normal `cal_thr`** e ha
congelato la soglia **13,623626738268857**, rango **334**, con regola stretta
`S > threshold`. La verifica separata su **150 run Normal `far_ver`** ha osservato
**11/150 = 7,3333%** di falsi allarmi nella metrica primaria; l’IC esatto di
Clopper–Pearson al 95% è **[3,7175%; 12,7424%]**. Sulle dieci finestre per run, la stima
secondaria è **108/1500 = 7,2%**, con bootstrap a livello di run, SE **0,7513 punti
percentuali** e intervallo percentile 95% **[5,7333%; 8,7333%]**.

La soglia resta invariata. Il FAR primario è compatibile con l’ordine di grandezza atteso ma,
con 150 run, non verifica strettamente la legge Beta fra calibrazioni. La sotto-fase è chiusa
nel presente branch dopo decisione autoriale, verifica indipendente e documentazione; la
**macro-Fase 03 resta aperta** e non è stata integrata o pubblicata da questa consegna.

#### Dettaglio

Il disegno segue il registro autorevole
[`DECISIONE_calibrazione_soglie_fase_B.md`](lit_review/DECISIONE_calibrazione_soglie_fase_B.md),
revisione 19. I 350 score sono tutti distinti; la molteplicità alla soglia è uno. Questa
assenza di pareggi è una diagnostica, non dimostra continuità o IID. Sotto continuità dello
score, IID dei run pertinenti e fit fissato indipendentemente, il FAR condizionale fra
calibrazioni segue **Beta(17,334)**: media **4,843304843%**, SD **1,144245586 punti
percentuali**, intervallo centrale 90% **[3,118163613%; 6,860631796%]**. È una legge teorica
condizionata alle ipotesi, non l’intervallo empirico del FAR della soglia realizzata.

Il completamento C4 ricampiona i 350 run con rango fisso 334, seed 20260914 e 10.000 repliche.
Per la soglia ottiene SE **0,5821769414** nelle unità dello score e intervallo Monte Carlo
95% **[12,2632210962; 14,2087372188]**. Il controllo esatto della distribuzione bootstrap
empirica usa l’inversa generalizzata e conserva anche **[12,2632210962; 14,4086543351]**.
Condizionate ai 350 score osservati, le masse dei due intervalli chiusi sono rispettivamente
**95,38705407%** e **96,89204510%**: non sono garanzie di copertura frequentista del quantile
della popolazione. Seed, numero di repliche e convenzione percentile sono dettagli operativi
fissati dopo i risultati; non vengono presentati come preregistrazione cieca.

I file `far_ver` erano già stati generati e accessibili prima del freeze, anche se le tracce
disponibili collocano l’apertura analitica FAR dopo il congelamento. Sigilli, log e storia Git
provano identità e sequenza registrata, non l’assenza assoluta di consultazioni umane o di
processi non registrati. L’autore ha accettato esplicitamente l’uso dei risultati FAR con
soglia invariata e questo limite dichiarato; la sua decisione resta distinta dalle prove
tecniche. Non sono state introdotte nuove simulazioni o calibrazioni per colmare a posteriori
questa lacuna storica.

#### Connessione alla letteratura

La cornice metodologica è quella raccolta in [`letteratura.md`](letteratura.md) §14.3 e nel
registro rev. 19: il quantile conforme in campione finito, la legge Beta condizionata alle
ipotesi e l’obbligo di misurare il FAR su Normal nuovi sono trattati come componenti diverse.
La 03.5 non trasforma l’assenza di pareggi in prova di continuità e non usa il FAR osservato
per rifissare la soglia.

#### Connessione alle critiche e limiti

La sotto-fase chiude la componente “soglia fissa e verificata” di G9 e rende osservabile il FAR
out-of-sample della pipeline; non dimostra continuità, IID, uguaglianza fra FAR vero e livello
nominale, né copertura del quantile della popolazione da parte degli intervalli bootstrap. Il
profilo per posizione non autorizza conclusioni causali sul burn-in. Il limite di segregazione
dei file FAR è accettato e dichiarato, non cancellato.

#### Artefatti e riproducibilità

- [Report della sotto-fase](../studio2/fase03/soglie_normal/REPORT_SOGLIE_NORMAL.md) e
  [decisione FAR dell’autore](../studio2/fase03/soglie_normal/DECISIONE_AUTORE_FAR.md).
- [Freeze della soglia](../studio2/fase03/soglie_normal/THRESHOLD_FREEZE.json),
  [risultati FAR](../studio2/fase03/soglie_normal/FAR_VERIFICATION.json),
  [protocollo C4](../studio2/fase03/soglie_normal/THRESHOLD_UNCERTAINTY_PROTOCOL.json) e
  [risultato C4](../studio2/fase03/soglie_normal/THRESHOLD_UNCERTAINTY.json).
- [Procedura riproducibile C4](../studio2/fase03/soglie_normal/REPRODUCIBILITY_C4.md) con
  dipendenze fissate; non richiede la directory temporanea usata dalla prima riverifica.
- Il verbale mirato ha conservato il proprio NON OK; le
  [Appendice 01](../studio2/fase03/soglie_normal/VERIFICA_DELTA_N1_IDENTITA_APPENDICE_01.md) e
  [Appendice 02](../studio2/fase03/soglie_normal/VERIFICA_DELTA_N1_IDENTITA_APPENDICE_02.md) e
  [Appendice 03](../studio2/fase03/soglie_normal/VERIFICA_DELTA_N1_IDENTITA_APPENDICE_03.md)
  registrano i successivi OK senza sovrascriverlo. I due verbali storici e lo snapshot già
  approvato sono acquisiti byte per byte in `soglie_normal/evidence/`.
- I dati voluminosi restano nella release verificata `studio2-fase03-normal-v1`; il
  [record di storage](../studio2/fase03/soglie_normal/ARTIFACT_STORAGE.json) documenta asset,
  impronta e riscaricamento. La release e i suoi dati non sono stati rigenerati.

### Sintesi per sezione

| § | Fase | Che cos'è | Fonte | Stato |
| :---: | --- | --- | --- | --- |
| 4 | **Capability pilot** | Il *gatekeeper*: il modello risponde, il JSON passa il parser, il budget di ragionamento tiene, la stabilità regge | piano §7.1 | dopo la preparazione residua |
| 5 | **Produzione degli insight** | Gli 8×2 insight dai dati di sviluppo, più la libreria completa del producer alternativo per il braccio *producer-swap* | piano §7.2 | dopo il pilot |
| 6 | **Congelamento del protocollo** | Solo dopo il pilot, mai prima | piano §7.3 | dopo il pilot |
| 7 | **Esecuzione dello studio finale** | Tutte le inferenze A, B-LF, E-LF, più swap, OOD, ablation e canary — circa 2.853/3.555 chiamate con margine, per 6/8 run | piano §7.4 e §8.8 | dopo il congelamento |
| 8 | **Analisi e redazione** | Solo a esecuzione completata | piano §7.5 | ultima |
| 9–12 | *riservate* | Spazio per fasi non previste, o per separare l'analisi dalla redazione | — | — |

Dettaglio dei cantieri ancora previsti dal piano §§6–7:

1. **§6.1** — Criteri verificati e congelati nella sotto-fase descritta in [§4.1](#criteri-selezione-61); estrazione D1 verificata in [§4.2](#catalogo-d1), catalogo congelato e pubblicato
2. **§6.2** — Run fault di sviluppo eseguiti, verificati e conservati nella sotto-fase descritta in [§4.3](#run-fault-62): 40 run, catalogo D1, stream 30000–30039, release `studio2-fase03-fault-dev-v1`; la generazione Normal e R1/R2 erano già qualificate in §3
3. **§6.3** — Soglia Normal calibrata e FAR verificato nella sotto-fase descritta in
   [§4.4](#soglie-normal-63): rango 334 su 350, soglia 13,623626738268857, release
   `studio2-fase03-normal-v1`; la macro-Fase 03 resta aperta
4. **§6.4** — Produrre dati strutturati e verbalizzazioni di sviluppo
5. **§6.5** — Definire pseudolabel e permutazioni di E
6. **§6.6** — Scrivere il piano statistico completo
7. **§6.7** — Preparare la baseline numerica
8. **§6.8** — Preparare l'harness API
9. **§6.9** — Generare e congelare i run finali di test
10. **§6.10** — Congelare lo schema degli insight
11. **§6.11** — Implementare la baseline FedAvg
12. **§6.12** — Scrivere le sezioni del paper indipendenti dal modello
13. **§7.1** — Capability pilot su Qwen-2.4T
14. **§7.2** — Produzione insight con Qwen-2.4T
15. **§7.3** — Congelamento protocollo finale
16. **§7.4** — Esecuzione studio finale
17. **§7.5** — Analisi e redazione

⚠️ **Ordine vincolato, non suggerito.** Dentro §6 le dipendenze non sono libere: i criteri di
§6.1 devono congelarsi **prima** che si estraggano gli 8 fault, e le decisioni «meccanicamente
distinto dal catalogo» e «coppia confondibile» sono definite *rispetto a quegli otto*, quindi
sono ora lavorabili dopo l’estrazione verificata D1; restano decisioni separate. Il piano §7 lo dice esplicitamente: il rischio più urgente non è
scientifico, è **temporale**, e si concentra su una sola data — la decisione GO/NO-GO sul modello.

*Una sezione si scrive quando la fase è conclusa, non mentre è in corso: finché è aperta, la
fonte resta il piano.*

---

## 13 · Conferenza

*Work in progress.* Sede, scadenze, formato e vincoli editoriali. Finché è vuota, il
riferimento è il piano e `paper/FoT_TEP_paper_blueprint.html`.

---

## 14 · Letteratura

Il corpus bibliografico **non vive qui**: sta in [`letteratura.md`](letteratura.md)
(replica web [`letteratura.html`](letteratura.html)), che è il **luogo unico** stabilito da
[`MAINTENANCE.md`](MAINTENANCE.md) §3. Vale per entrambi gli studi, e per questo non appartiene
a nessuno dei due walkthrough.

La numerazione interna è invariata: `§14.1` corpus completo (117 lavori), `§14.2` schede estese,
`§14.3` riferimenti metodologici, `§14.4` perimetro consultato, `§14.5` i lavori più vicini,
`§14.6` tenuta della novità, `§14.7` priorità bibliografica.

Quando lo studio 2 avrà implicazioni bibliografiche proprie, si aggiornano **§14.5 e §14.6 in
`letteratura.md`**, non questa sezione.
