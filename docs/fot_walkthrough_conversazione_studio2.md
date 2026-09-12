# Studio 2 — walkthrough

> **Documento vivo, a scheletro.** Si aggiorna **fase per fase**: si lavora su una fase, si
> documenta qui, si passa alla successiva. Stato al **2026-09-12**: **fasi 01 e 02 documentate in
> §2 e §3**; le fasi successive restano a scheletro. Finché una sezione resta vuota, **la fonte autorevole è
> il piano**, non questo file.

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
| Calibrazione delle soglie | `lit_review/DECISIONE_calibrazione_soglie_fase_B.md` (rev. 19) | **prevale sul piano**: la fase 02 ne ha chiuso i prerequisiti operativi; soglia, rango e FAR restano risultati futuri |
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

*Registrati il 2026-09-12. Quando uno si chiude, va tolto da qui e la decisione va scritta dove
compete: nel piano, in un registro di `lit_review/`, o in `MAINTENANCE.md` §1.*

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
- **Che cosa non è ancora congelato** — piano §0.1; per la calibrazione restano da produrre e
  congelare soglia, rango, numerosità e FAR nelle fasi successive
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

1. **§6.1** — Definire i criteri di selezione degli 8 fault
2. **§6.2** — Generare nuovi run fault di sviluppo; la generazione Normal e R1/R2 sono già qualificate in §3
3. **§6.3** — Calibrare soglie sui Normal di sviluppo
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
distinto dal catalogo» e «coppia confondibile» sono definite *rispetto a quegli otto*, quindi non
sono lavorabili oggi. Il piano §7 lo dice esplicitamente: il rischio più urgente non è
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
