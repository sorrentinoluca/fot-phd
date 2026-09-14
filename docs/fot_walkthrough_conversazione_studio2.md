# Studio 2 — walkthrough

> **Documento vivo, a scheletro.** Si aggiorna **fase per fase**. Stato al **2026-09-14**:
> fasi 01 e 02 documentate in §2 e §3; la sotto-fase **criteri di selezione (§6.1)** della
> Fase 03 è documentata in [§4.1](#criteri-selezione-61); **D1, verificata, congelata e pubblicata**, in [§4.2](#catalogo-d1);
> i **run fault di sviluppo (§6.2)**, verificati e conservati, in [§4.3](#run-fault-62); il **perimetro del codice Q8**, chiuso, in [§4.4](#perimetro-codice-q8); le **soglie Normal (§6.3)**, calibrate e verificate, in [§4.5](#soglie-normal-63); le **evidence 697-D**, verificate e conservate nella release v2, in [§4.6](#evidence-697-d); pseudolabel e derangement, verificati, in [§4.7](#pseudolabel-037); `normal_dev` e baseline numerica, verificati ma non ancora congelati efficacemente, in [§4.9](#normal-dev-baseline-039); il **raccordo delle metriche 03.9 → 03.10**, verificato sul solo delta, in [§4.10](#harness-raccordo-metriche-0310); lo **schema insight R4**, verificato e congelato con tag pubblicato, in [§4.12](#schema-insight-0312); le **sezioni comuni del paper**, aggiornate e verificate ma conservate soltanto nel candidato locale, in [§4.15](#paper-sections-0315). La Fase 03 resta aperta. La parte restante delle fasi successive
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
| Calibrazione delle soglie | `lit_review/DECISIONE_calibrazione_soglie_fase_B.md` (rev. 19) | **prevale sul piano** per il metodo; soglia, rango, FAR e incertezza prodotti dalla 03.5 sono documentati in [§4.5](#soglie-normal-63) |
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
fault e R2 è autorizzato come `baseline_fit` condizionata
([§3](#3--preparazione-indipendente-dal-modello--generazione-e-riuso-fase-02)). La decisione U3
del 2026-09-13 ne ha esteso l'uso, in modo circoscritto, alla normalizzazione e ai flag del
verbalizzatore V2 delle evidence 03.6, senza autorizzare calibrazione, verifica o test su N1–N5
([§4.6](#evidence-697-d)). Il punto sul
perimetro del codice della Q8, registrato il 2026-09-12, è stato chiuso dalla sotto-fase 03.4 senza
aprire un nuovo perimetro: la terza metrica di §8.5, il cap dello schema, l'estensione a 8 agenti e
il derangement a 7 peer sono codice nuovo in `studio2/` secondo [`MAINTENANCE.md`](MAINTENANCE.md)
§8.2, che ora disciplina il riuso a livello di funzione; `phase_b/` e il nucleo di `code/` restano
congelati per impronta ([`MAINTENANCE.md`](MAINTENANCE.md) §1).

| # | Punto aperto | Perché blocca | Chi decide | Registrato | Decisione da chiudere in |
| :---: | --- | --- | --- | --- | --- |
| 1 | **Sigle `C06`, `C07`, `C18`** citate dal piano sperimentale | Vengono dal registro critiche `C01–C18`, che esiste **solo** in `fot_walkthrough_conversazione.md` §33 — la prima esposizione del primo studio, che non è fonte. Finché restano così sono riferimenti appesi a un documento che nessuno deve usare | riportarle per esteso nel piano **oppure** rinumerarle | 2026-09-12 | `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` §0.1 — **non** il piano BIGDATA2026, che §0 esclude dalle fonti autorevoli |
| 3 | **Congelamento definitivo della fase 02** | Gli artefatti sono committati e il freeze è stato rigenerato sul loro HEAD; il record di storage e il freeze rigenerato sono successivi al riesame indipendente | riverifica indipendente delle impronte del freeze rigenerato prima di ogni tag definitivo | 2026-09-12 | `studio2/fase02/validation/PRECALIBRATION_FREEZE.json` e ciclo `Verifica_LLM` |
| 4 | **Formato del tag di lotto su `fot-tep-data`** | Chiuso: segue `MAINTENANCE.md` §8.5; per i lotti il formato operativo è ora esplicito e rinvia lì | aggiornato in `MAINTENANCE.md` | 2026-09-13 | `docs/MAINTENANCE.md` §8.5 / §8.6 |

*Registrati il 2026-09-12 (1–3) e il 2026-09-13 (4, ora chiuso in `MAINTENANCE.md` §8); il punto 2 è stato chiuso il 2026-09-13 e rimosso dalla tabella. Quando uno si chiude, va tolto da qui e la decisione va scritta dove
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
  sono ora documentati in [§4.5](#soglie-normal-63), mentre la Fase 03 resta aperta
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
([report della fase 01](../studio2/fase01/REPORT_FASE01.md), §4.2;
[verifica indipendente](../studio2/fase01/VERIFICA_FASE01.md)).

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

Questa consegna chiude la sotto-fase dei run fault di sviluppo, **non la macro-Fase 03**. Alla sua
chiusura i 40 run erano materiale di sviluppo, non di valutazione, e non ne erano ancora state
estratte feature, evidence o verbalizzazioni; l'estrazione successiva è documentata in
[§4.6](#evidence-697-d). Non esistono ancora insight; nessuna chiamata a
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

L'estrazione pre-specificata di feature ed evidence dai 40 run è ora chiusa in
[§4.6](#evidence-697-d); i prototipi sono documentati in [§4.9](#normal-dev-baseline-039).
Restano le altre dipendenze del report §7: insight delle sotto-fasi successive; manifest scientifico autonomo dei veri
input del pilot; nuovo controllo di capienza e autorizzazione esplicita prima di qualunque gate
LLM; decisioni D2, D11, OOD e producer alternativo; integrazione in `main` solo su richiesta
dell'autore. La macro-Fase 03 resta aperta.

<a id="perimetro-codice-q8"></a>

### 4.4 · Fase 03 — perimetro del codice Q8 (sotto-fase 03.4)

#### Riassunto e sintesi

La sotto-fase 03.4 ha chiuso il punto aperto sul perimetro del codice senza creare `phase_b/q8/`
né separare l'harness dagli artefatti dentro `phase_b/`. Tutto il codice nuovo resta sotto
`studio2/`; il codice congelato del primo studio si riusa soltanto a livello di funzioni
compatibili, con dipendenze ed effetti di caricamento verificati, provenienza e controllo
fail-closed dell'impronta prima dell'import. Default ereditati, incluse finestre, burn-in, soglie e
orizzonti, devono essere passati o dichiarati esplicitamente. La Fase 03 **non è chiusa**.

#### Dettaglio

L'opzione (a′) confermata conserva `phase_b/` e il nucleo di `code/` come artefatti congelati e
corregge la premessa secondo cui l'estensione a otto agenti avrebbe richiesto di scrivere nel primo.
Se un'assunzione non è eliminabile tramite parametri, la funzione viene adattata riscrivendola in
`studio2/`; gli import da `phase_b/` restano vietati e i test vengono riscritti sugli invarianti del
nuovo studio. La funzione `signature_vector` illustra l'unità di riuso, ma la sua compatibilità non
rende automaticamente importabile l'intero modulo che la contiene.

#### Connessione alla letteratura e alle critiche

La decisione è di processo e non introduce un claim bibliografico. Mitiga il rischio di riuso opaco
e di contaminazione fra studi; non chiude critiche scientifiche su trasferimento, accuratezza,
astensione o generalità del modello.

#### Artefatti e riproducibilità

La traccia è in [`PROPOSTA_PERIMETRO_Q8.md`](../studio2/fase03/perimetro_q8/PROPOSTA_PERIMETRO_Q8.md),
[`REPORT_PERIMETRO_Q8.md`](../studio2/fase03/perimetro_q8/REPORT_PERIMETRO_Q8.md), nei tre verbali
[`VERIFICA_PERIMETRO_Q8.md`](../studio2/fase03/perimetro_q8/VERIFICA_PERIMETRO_Q8.md),
[`rev002`](../studio2/fase03/perimetro_q8/VERIFICA_PERIMETRO_Q8_rev002.md) e
[`rev003`](../studio2/fase03/perimetro_q8/VERIFICA_PERIMETRO_Q8_rev003.md), concluso con **OK**, e in
[`DECISIONE_PERIMETRO_Q8.md`](../studio2/fase03/perimetro_q8/DECISIONE_PERIMETRO_Q8.md). La riga U2
di [`PROVENIENZA.md`](../studio2/PROVENIENZA.md) registra tardivamente la copia byte-identica di
`tep_features.py` usata nella Fase 02, senza modificarla. Nessun tag è stato creato.

#### Lavoro che resta

Le sotto-fasi 03.6 e 03.9 hanno applicato la regola function-level alle funzioni effettivamente
usate e hanno reso espliciti i parametri. Resta all'autore la scelta se proteggere
`code/tep_analysis_v2/` a HEAD oppure lasciarla fuori da §1 e affidarsi ai tag Phase A; questa
sotto-fase non decide il punto. Restano inoltre aperte l'integrazione del branch e la chiusura della
macro-Fase 03.

<a id="soglie-normal-63"></a>

### 4.5 · Fase 03 — soglie Normal (§6.3)

#### Riassunto e sintesi

La sotto-fase 03.5 ha calibrato lo score combinato sui **350 run Normal `cal_thr`** e ha
congelato la soglia **13,623626738268857**, rango **334**, con regola stretta
`S > threshold`. La verifica separata su **150 run Normal `far_ver`** ha osservato
**11/150 = 7,3333%** di falsi allarmi nella metrica primaria; l’IC esatto di
Clopper–Pearson al 95% è **[3,7175%; 12,7424%]**. Sulle dieci finestre per run, la stima
secondaria è **108/1500 = 7,2%**, con bootstrap a livello di run, SE **0,7513 punti
percentuali** e intervallo percentile 95% **[5,7333%; 8,7333%]**.

La soglia resta invariata. Il FAR primario è compatibile con l’ordine di grandezza atteso ma,
con 150 run, non verifica strettamente la legge Beta fra calibrazioni. La sotto-fase è chiusa,
integrata in `origin/main` e pubblicata con il tag `studio2-fase03-soglie-normal-frozen-001`,
dopo decisione autoriale, verifica indipendente e documentazione. La **macro-Fase 03 resta aperta**.
La [nota di integrazione](../studio2/fase03/soglie_normal/INTEGRAZIONE_03_5.md) distingue il tag
di consegna dal freeze scientifico storico della soglia.

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

<a id="evidence-697-d"></a>

### 4.6 · Fase 03 — sotto-fase 03.6 — evidence 697-D

#### Riassunto e sintesi

La sotto-fase 03.6 ha trasformato i 40 run fault di sviluppo già conservati in unità evidence
deterministiche: per ciascuna finestra produce una tabella di feature, un JSON strutturato, un testo
neutrale e una firma lunga 697 componenti. Fault, batch, stream e provenienza del run restano in un
indice evaluator-side separato dai payload destinati al consumer. La
[verifica indipendente](../studio2/fase03/evidence/VERIFICA_EVIDENCE.md), riferita al pacchetto
scientifico fino al commit `2f6dd8d`, ha dato **OK**; il verbale è entrato nella storia con
`54bbd0c`. Il commit successivo `bb6d9e7` non cambia alcun file scientifico: registra la release
preferita `studio2-fase03-evidence-v2`, nuovo packaging degli stessi 1.283 file. La Fase 03
**non è chiusa**; verifica scientifica, integrazione in `main` e pubblicazione restano atti
distinti.

#### Dettaglio

##### Guardia, baseline e soglie

Prima di aggiungere `code/` al percorso di importazione, l'estrattore verifica contro
[`PHASE_B_PROTOCOL_HASHES.json`](../phase_b/PHASE_B_PROTOCOL_HASHES.json) le impronte dei quattro
sorgenti congelati effettivamente riusati: `tep_features.py`, `tep_verbalize_v2.py`,
`verbalizer_config_v2.json` ed `evaluate_verbalizer_v2.py`. Solo dopo il superamento della guardia
carica le funzioni; un singolo mismatch arresta l'esecuzione. I passaggi e gli effetti di
caricamento sono dichiarati in
[`DIPENDENZE_EVIDENCE.md`](../studio2/fase03/evidence/DIPENDENZE_EVIDENCE.md) §1 e registrati
function-level in [`PROVENIENZA.md`](../studio2/PROVENIENZA.md) §12.

U3 estende U1/R2 per un solo scopo: i cinque blocchi Normal N1–N5 in `[0,250 h)` forniscono la
baseline di normalizzazione e i flag del verbalizzatore. Restano accoppiati alle quattro soglie V2
congelate — `abs_shift_sigma=1.9695333234149084`,
`abs_slope_sigma_h=0.7468621213669596`,
`residual_std_ratio=1.3681613543196571` e
`diff_std_ratio=1.4051245046201666` — senza ricalibrazione
([`DIPENDENZE_EVIDENCE.md`](../studio2/fase03/evidence/DIPENDENZE_EVIDENCE.md) §§2–3). Il recheck
R2 richiesto è `PASS` al commit `d09e7ed`, con record SHA-256
`7df0cef2d7854c689b79eb911fa01d1ede1625e22f0d3636c0ea5d678c9f33f8`: `guard_pass`,
`parameters_and_code_current` e `r2_guard_result_independent_byte_identical` sono veri, come
ricontrollato dal verbale §3. U3 non autorizza calibrazione, scelta di soglia, verifica o test su
N1–N5; la soglia dello score dipende dai nuovi Normal della 03.5. Se R2 decade o la baseline passa
a `baseline_fit_new`, l'intero lotto evidence diventa invalido e deve essere rigenerato, senza
sostituzione automatica della baseline.

##### Trasformazione e conteggi

L'onset non eredita il default legacy a 10 h: è passato esplicitamente come **25 h**. Ogni run è
diviso nelle otto finestre half-open da 5 h di `[25,65)`; per ciascuna l'estrattore calcola 41 righe
XMEAS, le verbalizza in JSON e testo neutrali e ricava dal JSON la firma `41 × 17 = 697-D`. La
seguente contabilità è ricostruita dall'indice e dal manifest:

| Quantità | Valore ricostruito | Fonte precisa |
| --- | ---: | --- |
| Run complessivi | 40: 8 fault × 5 run | 40 `run_id` distinti in `output/EVALUATOR_INDEX.csv`, riepilogati in [`OUTPUT_CHECK.json`](../studio2/fase03/evidence/OUTPUT_CHECK.json) |
| Finestre per run | 8 in `[25,65)` | `windows_per_run`, `onset_h`, `end_h` e `window_h` in `output/EXTRACTION_SUMMARY.json`, la cui impronta è in [`OUTPUT_CHECK.json`](../studio2/fase03/evidence/OUTPUT_CHECK.json) |
| Unità evidence | 320: 40 × 8 | 320 righe di `output/EVALUATOR_INDEX.csv` e `evidence_unit_count` in `output/EXTRACTION_SUMMARY.json` |
| Unità per fault | 40 finestre, **non 40 run** | conteggi evaluator-side per F1/F2/F3/F8/F10/F13/F14/F15 in [`OUTPUT_CHECK.json`](../studio2/fase03/evidence/OUTPUT_CHECK.json); l'indice mostra 5 run per fault × 8 finestre |
| Componenti per firma | 697: 41 × 17 | `signature_dimension` in [`OUTPUT_CHECK.json`](../studio2/fase03/evidence/OUTPUT_CHECK.json) e costruzione verificata nel verbale §5 |
| File unitari | 1.280: 320 × 4 | 320 file per ciascun suffisso `.features.csv`, `.evidence.json`, `.txt`, `.signature.csv` in [`MANIFEST_CONSERVAZIONE.csv`](../studio2/fase03/evidence/MANIFEST_CONSERVAZIONE.csv) |
| File scientifici e payload | 1.283 e 61.208.618 byte | 1.280 unitari + `EVALUATOR_INDEX.csv`, `EVIDENCE_MANIFEST.csv`, `EXTRACTION_SUMMARY.json`; righe e somma `bytes` di [`MANIFEST_CONSERVAZIONE.csv`](../studio2/fase03/evidence/MANIFEST_CONSERVAZIONE.csv), confermate da [`OUTPUT_CHECK.json`](../studio2/fase03/evidence/OUTPUT_CHECK.json) |

##### Leakage: significato e limiti

Il controllo anti-leakage è `PASS` sui 320 JSON e sui 320 testi consumer-facing; il test positivo
mostra inoltre che lo scanner intercetta ID di fault/IDV, nomi dei meccanismi e marche di origine
vietate. La separazione dell'indice impedisce che fault, batch e stream vengano copiati nei
payload. Questo controllo dimostra l'assenza dei pattern espliciti coperti dallo scanner nei due
formati testuali verificati; **non** dimostra assenza di ogni correlato indiretto o leakage
semantico, privacy formale, separabilità dei fault, correttezza diagnostica o utilità della
rappresentazione. La firma e le feature sono trasformazioni deterministiche, non una misura di
validità scientifica.

#### Connessione alla letteratura

La scelta segue il filone segnale → descrizione → reasoning e la separazione fra evidence
deterministica e inferenza discussi nelle schede di [`letteratura.md`](letteratura.md) §14.2. I
lavori su verbalizzazione deterministica e reporting evidence-traceable sostengono l'esigenza di
un'interfaccia verificabile, ma non convalidano questa istanza né il suo uso federato. I lavori
centralizzati sul fault diagnosis delimitano inoltre il claim: produrre testo da serie industriali
non è di per sé il contributo. Non nasce qui un nuovo claim bibliografico; §§14.5–14.6 restano il
luogo unico per novità e confronti, senza duplicare il corpus nel walkthrough.

#### Connessione alle critiche e limiti

La guardia prima dell'import, la provenienza U3 e la separazione evaluator-side **mitigano** il
riuso opaco e il leakage esplicito; non chiudono le critiche scientifiche. In particolare:

- il determinismo byte-identico è verificato entro l'ambiente dichiarato. Nel diverso ambiente del
  verificatore, testo e firma sono rimasti byte-identici, mentre feature e JSON hanno mostrato soli
  scarti floating-point dell'ordine di `10⁻¹³`; la rigenerazione bit-per-bit cross-ambiente richiede
  quindi versioni di libreria fissate o un confronto a tolleranza sui numerici grezzi;
- non sono state misurate accuracy, separabilità, rilevabilità, intensità del segnale, astensione o
  validità diagnostica;
- le otto finestre dello stesso run non sono otto run indipendenti;
- le evidence `normal_dev` non fanno parte di questo pacchetto e sono documentate in §4.9;
- il lotto è condizionato a R2 e alla baseline attuale: il decadimento di R2 o il passaggio a
  `baseline_fit_new` lo invalida;
- la sotto-fase è verificata, ma la Fase 03 resta aperta; integrazione e pubblicazione non fanno
  parte del verdetto scientifico.

#### Artefatti e riproducibilità

Il [report storico](../studio2/fase03/evidence/REPORT_EVIDENCE.md) conserva correttamente la frase
«in attesa di verifica» e il riferimento alla v1 perché fotografa lo stato alla propria chiusura.
Lo stato successivo si ricostruisce senza riscriverlo: [il verbale
indipendente](../studio2/fase03/evidence/VERIFICA_EVIDENCE.md), acquisito da `54bbd0c`, attesta il
pacchetto scientifico fino a `2f6dd8d`; il controllo separato
[`PACKAGING_V2_CHECK.json`](../studio2/fase03/evidence/PACKAGING_V2_CHECK.json), introdotto da
`bb6d9e7`, attesta il packaging v2. Non si attribuisce quindi al verificatore originario un
controllo svolto dopo il suo verbale.

La release preferita è `studio2-fase03-evidence-v2`. Il suo archivio misura **62.185.472 byte** e
ha SHA-256
`6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf`; non va confusa la
dimensione del contenitore tar con la somma dei payload scientifici, **61.208.618 byte**. Il
riscaricamento registrato in [`ARTIFACT_STORAGE.json`](../studio2/fase03/evidence/ARTIFACT_STORAGE.json)
e nel controllo v2 verifica **1.283/1.283** file per percorso, byte e SHA-256, con zero mismatch,
zero extra e zero AppleDouble; i metadati riportano inoltre zero membri con header PAX. La v1
resta pubblicata e immutata: v2 è soltanto un nuovo packaging AppleDouble-free degli stessi
1.283 file scientifici, con percorsi, byte e hash invariati.

I riferimenti riproducibili sono:

- dipendenze e condizioni U3:
  [`DIPENDENZE_EVIDENCE.md`](../studio2/fase03/evidence/DIPENDENZE_EVIDENCE.md);
- esito machine-readable:
  [`OUTPUT_CHECK.json`](../studio2/fase03/evidence/OUTPUT_CHECK.json);
- manifest scientifico:
  [`MANIFEST_CONSERVAZIONE.csv`](../studio2/fase03/evidence/MANIFEST_CONSERVAZIONE.csv);
- storage e release:
  [`ARTIFACT_STORAGE.json`](../studio2/fase03/evidence/ARTIFACT_STORAGE.json) e
  [`PACKAGING_V2_CHECK.json`](../studio2/fase03/evidence/PACKAGING_V2_CHECK.json);
- provenienza function-level e U3:
  [`PROVENIENZA.md`](../studio2/PROVENIENZA.md) §12;
- implementazione verificata:
  [`extract_evidence.py`](../studio2/fase03/evidence/extract_evidence.py),
  [`leakage.py`](../studio2/fase03/evidence/leakage.py) e
  [`verify_output.py`](../studio2/fase03/evidence/verify_output.py).

Il controllo documentale generale resta al baseline di **35 test, 14 fallimenti preesistenti e 1
skipped**; non misura la correttezza scientifica di questa sezione.

<a id="pseudolabel-037"></a>

### 4.7 · Fase 03 — pseudolabel e derangement di E (sotto-fase 03.7)

#### Riassunto e sintesi

La sotto-fase 03.7 ha prodotto e verificato otto pseudolabel opache più `Normal`,
la biiezione degli otto fault del catalogo D1 con gli otto agenti e un derangement
senza punti fissi dei sette peer per ciascun agente. La verifica indipendente è
**OK dopo rettifiche documentali**. L’autore conserva il sorteggio v1 e ne accetta
esplicitamente la correlazione d’ordine osservata. La Fase 03 **non è chiusa**.

#### Dettaglio

La specifica al commit `221bf58` precede la generazione `8c90ece`; il freeze
originale è in `fdf06b82`. Namespace `studio2-fase03-pseudolabel-v1`, seed `20260913`:
le label derivano da SHA-256/base32 e l’assegnazione da digest separati; il seed
interviene soltanto nei derangement. Per agente si sceglie un indice fra i 1854
derangement dei sette peer tramite rejection sampling su parole derivate da SHA-256.
La costruzione è pseudocasuale e riproducibile; l’eliminazione del bias modulo
presuppone parole uniformi, non dimostra empiricamente casualità.

Le otto label opache hanno lunghezza 12; `Normal` è letterale, lungo 6 e ultimo;
`Unknown` è astensione, non una classe. Il mapping reale resta evaluator-side;
le sole label operative sono utilizzabili nei prompt. Il revisore ha ricostruito
indipendentemente label, assegnazioni e derangement; 21 test dedicati e 16 test Q8
sono passati, con replay byte-identico dei quattro artefatti e sette impronte verificate.

#### Connessione alla letteratura

La scheda FERA in `letteratura.md` §14.2 distingue la gestione dell’inaffidabilità
dalla sua induzione deliberata nella condizione E. Questa sotto-fase prepara
il controllo B/E; non misura ancora un effetto e non aggiunge claim bibliografici.

#### Connessione alle critiche e limiti

Sulle otto label di fault la correlazione di Spearman fra rango di catalogo e
rango lessicografico è **−5/6 (−0,833)**; F15, F14 e F13 occupano le prime tre
posizioni. Il test `|rho| < 1` esclude soltanto una relazione monotona perfetta,
non verifica l’assenza di correlazione richiesta letteralmente dal prompt iniziale.
L’accettazione dell’autore è successiva all’osservazione e registrata come tale:
non si rigenera v1 né si riordina ad hoc per compensare questo valore.

Opacità delle stringhe non significa segretezza: namespace, algoritmo e
identificatori consentono di ricostruire il mapping. L’harness deve mantenere
questi ingredienti e il mapping fuori dai prompt sperimentali. Log e storia Git
mostrano un insieme registrato e la specifica precedente; non provano l’assenza
di esecuzioni private non registrate. Gli effetti di posizione non sono esclusi.

#### Artefatti e riproducibilità

Le fonti sono [specifica](../studio2/fase03/pseudolabel/SPECIFICA_PSEUDOLABEL.md),
[report rettificato](../studio2/fase03/pseudolabel/REPORT_PSEUDOLABEL.md),
[verifica indipendente](../studio2/fase03/pseudolabel/VERIFICA_PSEUDOLABEL.md) e
[decisione dell’autore](../studio2/fase03/pseudolabel/DECISIONE_ACCETTAZIONE_V1.md).
Il [freeze v1](../studio2/fase03/pseudolabel/PSEUDOLABEL_FREEZE.json) registra
sette impronte e il commit sorgente `8c90ecec421980211258e9323d4266a32ba70ccd`;
resta intatto come fotografia dello stato pending originario. Il tag previsto è
`studio2-fase03-pseudolabel-frozen-001`, subordinato a verifica OK, sorgente
raggiungibile da `origin/main` e replay al commit taggato. Il controllo è
`python3 -m studio2.fase03.pseudolabel.pseudolabel_draw --check`.
La provenienza del pattern riscritto è in `studio2/PROVENIENZA.md` §9, senza
import da `phase_b/` e senza riuso di dati sperimentali. Il controllo documentale
generale mantiene 14 fallimenti preesistenti e un test saltato; non copre questa sottofase.

#### Lavoro che resta

L’anticipo combinatorio rispetto all’ordine proposto 03.12 → 03.7 non chiude
lo schema degli insight: 03.12 deve confermare la compatibilità prima del pilot.
Un cambio di formato richiede nuovo namespace e nuovi file, senza sovrascrivere v1.
L’eventuale regola generale di presentazione nei prompt compete a 03.10/03.12:
deve essere riproducibile e comune alle condizioni confrontate, fissata prima
del pilot. Restano fuori contenuti degli insight, esempi locali, manifest reale
ed esecuzione del pilot; nessuna chiamata al modello o simulazione è stata avviata.

<a id="normal-dev-baseline-039"></a>

### 4.9 · Fase 03 — `normal_dev` e baseline numerica (sotto-fase 03.9)

#### Riassunto e sintesi

La sotto-fase 03.9 ha accettato tecnicamente il lotto Normal di sviluppo e ha costruito la
baseline numerica pre-specificata. L'audit e la verifica indipendente confermano **40/40 run** e
**320/320 finestre**; dai dati di sviluppo sono state estratte 320 evidence Normal da 697
componenti e costruiti **nove prototipi globali e sedici locali**. Il ricalcolo indipendente dei
25 vettori ha differenza massima zero. Non sono stati aperti dati di test, calcolate accuratezze o
scelte soglie sulle prestazioni.

La verifica separata è **OK**, dopo due candidati NON OK per errori di provenienza poi corretti.
Il pacchetto è integrato in `origin/main` e il lotto è pubblicato e verificato per riscaricamento.
L'OK non rende efficace il freeze: restano il mapping dei nomi nella 03.10, l'integrazione dei
sorgenti riusati di 03.6 e il tag della baseline. La Fase 03 **non è chiusa**.

#### Dettaglio

Il piano, fissato prima della generazione, assegna cinque run a ciascuno degli otto agenti e gli
stream 60000–60039. Ogni workbook copre 65 h con campionamento al minuto; le otto finestre utili
sono `[25,30)`, …, `[60,65)`. L'audit ha verificato piano, manifest, hash, modello, MEX, RNG,
griglia, dimensioni e finitezza. Le 320 finestre appartengono a 40 run e non sono trattate come 320
repliche indipendenti.

L'autore ha accettato il riuso del pathname `normal_dev_001` dopo il tentativo pre-start e ha
considerato sufficiente la tracciabilità residua di comando e `MATLABPATH`, conservandone il
limite. Non ha autorizzato una deroga al prerequisito `origin/main`: lo stato del ref al momento
del lancio non è attestato. Il log riuscito contiene 40 warning del blocco `Variable Time Delay`.
Modello e generatore congelati, `FixedBuffer=off`, normal-mode, `ode45` e assenza di code
generation circoscrivono il messaggio alla crescita dinamica del buffer. L'accettazione vale solo
per questo lotto e non per ERT/GRT, embedded o validità scientifica generale.

L'estrazione Normal verifica per hash `extract_evidence.py` e `leakage.py` della 03.6 e conserva
le guardie U3/R2: N1–N5 e soglie V2 servono soltanto a normalizzazione e flag, non come esempi
Normal. Se R2 decade, le evidence vanno rigenerate. La release fault preferita è
`studio2-fase03-evidence-v2`, repackaging verificato con gli stessi 1.283 file scientifici della
v1. La baseline usa 40 firme per fault, 320 Normal globali e 40 Normal per agente; ciascun
prototipo è una media aritmetica 697-D e la classificazione usa L1 media, con pareggio entro
`1e-12` che produce astensione e senza nuova soglia di distanza o fallback globale.

Gli otto esempi Normal locali seguono la regola pre-specificata run locale 1, finestra `[25,30)`.
Il parser reale del harness 03.10 li accetta 8/8. Le righe evaluator-side sono compatibili con la
03.8; resta però da adottare in 03.10 il mapping `accuracy`→`accuracy_all`, `n`→`total` e
`abstentions`→`abstained`, con il conteggio `invalid` aggiuntivo nel harness.

#### Connessione alla letteratura e alle critiche

La sotto-fase non introduce un nuovo claim bibliografico: prepara il comparatore deterministico
che il disegno richiede per interpretare i bracci LLM. Mitiga i rischi di selezione post-hoc e di
contaminazione del test grazie a specifica precedente, separazione development/test e verifica
hash; non dimostra accuratezza, robustezza o indipendenza statistica. Lo sbilanciamento di sviluppo
fra 320 firme Normal e 40 per fault resta un vincolo da trattare nella ricetta FedAvg della 03.14.

#### Artefatti e riproducibilità

Il [report](../studio2/fase03/baseline_numerica/REPORT_BASELINE_NUMERICA.md) indicizza specifiche,
audit, decisione, controllo del warning, evidence, prototipi e controllo d'interfaccia. La
[verifica indipendente](../studio2/fase03/baseline_numerica/VERIFICA_BASELINE_NUMERICA.md) registra
l'OK sul commit `ba1a206e1fe31c062d5491b4fb821ff925149982` e la cronologia dei due NON OK. Il
[freeze revisionato](../studio2/fase03/baseline_numerica/BASELINE_FREEZE_rev003.json) resta
`effective=false`; i manifest storico e rev. 2 non sono stati sovrascritti.

`PROTOTYPES.json` ha SHA-256 `6d0b754065eb8a69d0657638deeef0756de0ec8e93a905c55aea18fadace2cb2`;
il manifest dei prototipi `8309a914d2141da38d1120606897bcead40142829ecd541b6b0423d0d9465751`;
il manifest Normal `cc8d96c2c60169afc99cb811cea194aa553afcc7cc51cad4a0092d44de38fdc1`.
L'archivio USTAR pubblicato ha SHA-256
`eef69b42d8506c993ac45d77208df982d138b4354d7d4134bd67ba421dc91a03` e 1.336 membri verificati
per riscaricamento dalla release `studio2-fase03-normal-dev-v1`, senza differenze. Dati grezzi, runtime, storia audit, evidence e archivio restano fuori
da Git e sono legati agli inventari tracciati.

#### Lavoro che resta

Integrare e testare il mapping dei nomi nella 03.10 e rendere raggiungibili da `origin/main`
i sorgenti riusati della 03.6. Solo dopo, creare e registrare il tag della baseline in una
nuova revisione del freeze. Pubblicazione, riscaricamento e integrazione del pacchetto 03.9
sono completati; la sotto-fase resta aperta. La
[consegna di integrazione](../studio2/fase03/baseline_numerica/CONSEGNA_INTEGRAZIONE_03_9.md)
riporta commit, prove e dipendenze residue.

<a id="harness-raccordo-metriche-0310"></a>

### 4.10 · Fase 03 — harness: raccordo delle metriche 03.9 → 03.10 (sotto-fase 03.10)

> Questa sotto-sezione documenta **soltanto** il raccordo (adattamento offline) delle metriche
> fra la baseline numerica 03.9 e l'harness 03.10, delta `5116087..caf5bfb`. **Non** documenta
> l'intero harness 03.10, che resta aperto, e non chiude 03.9 né 03.10. La Fase 03 **non è chiusa**.

>
> **Stato d'integrazione (candidato locale su `e82b5a0`).** Il *delta metriche* `5116087..caf5bfb` è già verificato **OK** in modo indipendente (verbale acquisito). Il presente *candidato d'integrazione* è invece **nuovo lavoro non ancora verificato indipendentemente**: importa il raccordo sulla base comune `e82b5a0` (che non conteneva `studio2/fase03/harness/`), con la sola chiusura minima di dipendenze (`common.py`) e un test mirato `test_metric_raccordo.py` (MetricTests estratti dal test verificato). `common.py` è codice di supporto preesistente **non coperto** dall'OK del solo delta; il test mirato e l'import completo vanno sottoposti a verifica indipendente del nuovo delta d'integrazione.

#### Riassunto e sintesi

Il delta aggiunge un adattatore offline, hash-pinned e fail-closed, che legge il documento
`metrics.json` della baseline numerica 03.9 e ne rinomina i campi verso il contratto a tre numeri
dell'harness 03.10 **senza ricalcolare** i valori. La verifica indipendente sul solo delta è
**OK** (verbale `VERIFICA_RACCORDO_METRICHE.md`, prima riga `VERDETTO: OK`). L'OK vale per il
commit e il perimetro indicati, non per l'intero harness: restano aperti input reali, pin 03.12,
ordine delle label, qualificazione dell'endpoint e collegamento ai run finali.

#### Dettaglio — mapping, conteggi e denominatori

Il mapping dei nomi è `accuracy` → `accuracy_all`, `n` → `total`, `abstentions` → `abstained`;
`non_abstained` è preservato dopo la verifica `non_abstained = total − abstained`. Il campo
`invalid` è assente nella sorgente 03.9 e viene emesso come `invalid = 0` **solo** perché la
baseline 03.9 è valid-only (ogni riga ha `valid=true` e un input non valido arresta l'esecuzione);
un campo `invalid` inatteso, o conteggi/rapporti incoerenti, fanno fallire l'adattatore (fonti:
`CONTRATTO_RACCORDO_METRICHE.md`, `metric_adapter.py`).

I denominatori sono `accuracy_all = correct / total`, `abstention_rate = abstained / total` e
`accuracy_non_abstained = correct / non_abstained`, con `non_abstained = total − abstained`. Nel
calcolo generale dell'harness un invalido non è corretto e non è un'astensione, ma **resta nel
denominatore** di `accuracy_non_abstained`; con denominatore zero il valore è `null` (fonti:
`metrics.py`, `SPECIFICA_HARNESS.md` §8, e la rev. 10 del piano statistico per la categoria
autonoma dell'invalidità). I tre valori dei rapporti sono copiati per identità dall'oggetto
sorgente, senza arrotondamento (verificato su 12.341 configurazioni valid-only). L'ambito del diff
è 5 file, +484 / −1 riga, `git diff --check` pulito.

#### Connessione alla letteratura e alle critiche

Il raccordo è un passaggio interno di interfaccia e non introduce claim bibliografici nuovi: rende
adottabile in 03.10 la baseline deterministica documentata in [§4.9](#normal-dev-baseline-039)
senza alterarne i numeri. Mitiga il rischio di disallineamento semantico fra produttore 03.9 e
consumatore 03.10; non dimostra accuratezza, robustezza o indipendenza statistica.

#### Limiti

L'OK è **limitato al delta `5116087..caf5bfb`**: non è un OK dell'intero harness, non chiude
03.9 / 03.10, non rende efficace `HARNESS_FREEZE.json` e non autorizza chiamate, simulazioni o
analisi sui run finali. La verifica indipendente registra due **skip** (checkout esterni non
montati nella sandbox: test dell'adapter 03.12 e inventario release 03.6), da tenere distinti dal
risultato locale dell'esecutore, che riporta invece **1 errore preesistente** nel test del vecchio
pin 03.12 (il checkout 03.12 corrente non coincide con l'hash pinnato). Il **problema del pin 03.12
resta aperto e fuori perimetro**: non è stato convertito in PASS né corretto. La semantica
invalidità/astensione dipende normativamente da `DELTA_HARNESS_03_10.md` della rev. 10, non ancora
integrata nel branch harness.

#### Artefatti e riproducibilità

Delta verificato: commit `caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae`; base
`51160872906feaa63c1fda5e9cf6e0fe8538fb16`; sorgente 03.9
`c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`. Report e manifest del candidato sono nel commit
successivo `1ac06eb`: il [report](../studio2/fase03/harness/REPORT_RACCORDO_METRICHE.md)
(SHA-256 `8ab3ac62…`), il [contratto](../studio2/fase03/harness/CONTRATTO_RACCORDO_METRICHE.md)
(SHA-256 `5c81586f…`) e il manifest `METRIC_INTERFACE_CANDIDATE.json` (stato
`independent_verification: PENDING` conservato). Il
[verbale indipendente](../studio2/fase03/harness/VERIFICA_RACCORDO_METRICHE.md) ha SHA-256
`0d90779981871b8c9ceaf2a729f97b371abb7297fb804dc4335ddf0f1bec0e80`; l'OK è registrato in
[REGISTRO_OK_RACCORDO_METRICHE.md](../studio2/fase03/harness/REGISTRO_OK_RACCORDO_METRICHE.md).
Dipendenza normativa rev. 10: `studio2/fase03/piano_statistico/DELTA_HARNESS_03_10.md` al
riferimento Git stabile `6aaa5b3eebfed4ba502c25c0443caabd0051af21` (blob `780e08ae…`, contenuto
SHA-256 `e92661fe…`).

#### Lavoro che resta

Collegare l'adapter agli artefatti reali dell'harness e agli input verificati; integrare la
rev. 10 nel branch harness; completare pin 03.12, ordine delle label, endpoint e qualificazione dei
modelli. Solo con i sorgenti 03.6 raggiungibili da `origin/main` e i controlli previsti si potrà
completare il record di freeze 03.9 e il relativo tag. La sotto-fase 03.10 resta aperta.

<a id="schema-insight-0312"></a>

### 4.12 · Fase 03 — schema degli insight (sotto-fase 03.12)

#### Riassunto e sintesi

La revisione 4 definisce e valida il contratto strutturale degli insight prima della loro
produzione. Il verificatore indipendente ha dato **OK R4-V** sull'esatto commit
`3c64390bc4dd58c48cc4e1e388a38989b32b3143`: il contesto usa otto pseudolabel fault opache
assegnate agli otto agenti e la label separata, letterale e case-sensitive `Normal`. La libreria
resta di 16 insight, due per ciascun fault; ogni ricevente ne vede 14 dopo il filtro dei propri.
`Normal` non produce insight e `Unknown` resta soltanto l'astensione.

Questo esito qualifica il contratto R4, non una produzione scientifica: nessun insight è stato
prodotto o valutato, la capienza dei prompt reali e l'ottimalità dei cap non sono dimostrate. Il
tag annotato `studio2-fase03-schema-insight-frozen-001` è stato pubblicato sull'esatto target
R4; `SCHEMA_FREEZE.json` conserva correttamente lo stato storico
`frozen_pending_independent_verification`. La Fase 03 **resta aperta**.

#### Dettaglio

Ogni record ha sei campi obbligatori e vieta proprietà aggiuntive. Cinque campi deterministici
(`insight_id`, `source_agent`, `pseudolabel`, `evidence_scope`, `variable_ids`) provengono dal
manifest fidato e sono confrontati esattamente dal validatore; il producer scrive soltanto
`observed_pattern`. Il record canonico è limitato a 1.400 caratteri e 384 token, la narrativa a
800 caratteri e 192 token, `evidence_scope` a 240 caratteri e 64 token. Gli ID di variabile sono
limitati a `XMEAS(1…41)` e `XMV(1…12)`; il controllo lessicale vieta riferimenti a fault,
meccanismi, nomi fisici e label fuori dal campo previsto. La condizione E viene controllata sui
byte canonici dopo il filtro peer e può cambiare soltanto `pseudolabel` secondo il derangement
fornito dalla 03.7.

La suite locale documentata per R4 conta **25 PASS, 0 FAIL e 1 SKIP su 26**: è saltato solo il
test del tokenizer reale perché lo snapshot pinnato non era disponibile localmente. La
trascrizione del terminale fornita dall'autore documenta invece sul server **26 PASS su 26,
senza skip**, con tokenizer Qwen pinnato: 83 token/record per `S2-INS-001`–`006` e `013`–`016`,
84 per `007`–`012`, 20 token di narrativa e 4 di `evidence_scope` per tutti i record sintetici.
Il log è una trascrizione fornita dall'autore, copiata byte per byte dall'allegato, **non** un
file originale scaricato dal server. Questi conteggi qualificano fixture e implementazione;
non provano capienza dei prompt reali o qualità scientifica.

#### Connessione alla letteratura e alle critiche

EviFDD-Agent in [`letteratura.md` §14.2](letteratura.md) sostiene la separazione fra campi
deterministici e narrazione tracciabile. ACE (P001) delimita qualunque affermazione sulla
concisione, Fed-ICL (P041) offre un confronto di budget ma non giustifica il cap 192, e SYNAPSE
(P065) delimita la novità e il consumer-swap. La sotto-fase mitiga i rischi di mutazione dei
campi fissi, leakage lessicale e corruzioni ulteriori nella condizione E; non chiude la validità
semantica degli insight, la copertura universale delle parafrasi, l'EFT o la robustezza del
producer.

#### Artefatti e riproducibilità

Il [report storico R4](../studio2/fase03/schema_insight/REPORT_SCHEMA_INSIGHT.md), la
[decisione](../studio2/fase03/schema_insight/DECISIONE_SCHEMA_INSIGHT.md) e il
[manifest rev. 5](../studio2/fase03/schema_insight/SCHEMA_FREEZE.json) restano byte-identici al
target verificato. Il manifest misura 12.323 byte, SHA-256
`d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`; le sue 18 voci e la
catena `previous_manifest_sha256` sono state verificate. Il
[verbale OK R4-V](../studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004.md) misura
21.288 byte, SHA-256 `d0e69094953cac7966eda9d1f612b81f44cc8e646151fd2339dba0b7ca88ec8e`;
il [log server](../studio2/fase03/schema_insight/TEST_RESULTS_qwen_rev004.txt) misura 7.459 byte,
SHA-256 `a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972`.
Il [record di pubblicazione](../studio2/fase03/schema_insight/PUBBLICAZIONE_SCHEMA_INSIGHT.md)
registra oggetto tag remoto `4d15c4fb915ea9db9f7425225d231746778f0ba1` e peeled
`3c64390bc4dd58c48cc4e1e388a38989b32b3143`; il
[record di preparazione locale](../studio2/fase03/schema_insight/PREPARAZIONE_INTEGRAZIONE_SCHEMA_INSIGHT_R4.md)
resta la cronologia dei controlli anteriori al freeze.

L'esecutore R4 è identificato dall'evidenza runtime come Codex/OpenAI `gpt-5.6-sol`, reasoning
medium, task `01a09f1b-a581-7c41-a1ec-87912c8896ef`; il verificatore indipendente è
Claude/Anthropic, identificativo configurato `claude-fable-5-1`, sessione
`session_01Y11UC227qhEvrbQxjzRpzK`, con i limiti d'identificazione dichiarati nel verbale. Il
[precedente NON OK](../studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004_NON_OK_STORICO.md)
è conservato separatamente e byte-identico, SHA-256
`5bd196820f74b7fbd5ee6736df2b72afc64afbbfb26459dc69f1fe5e15dafd19`; il verbale OK chiude
il rilievo sull'indipendenza senza cancellarne la cronologia.

#### Lavoro che resta

Target R4, evidenze e documentazione sono raggiungibili da `origin/main`; il tag annotato è
pubblicato e il freeze 03.12 è effettivo. Restano separati la capienza dei prompt reali, il futuro
pilot e la qualificazione del servizio/modello 122B. In una successiva attività 03.10 andranno
aggiornati i pin dell'adapter; questo aggiornamento non appartiene alla 03.12 e non è stato
eseguito qui.

<a id="paper-sections-0315"></a>

### 4.15 · Fase 03 — sezioni comuni del paper (sotto-fase 03.15)

#### Riassunto e sintesi

La sotto-fase 03.15 ha preparato, senza promuoverle nel manoscritto, cinque bozze comuni e una
mappa editoriale in `studio2/fase03/paper_sections/`. Il pacchetto storico sul candidato
`cf79e81f917c7969dfd375e38db54315c28d4c07` conserva il proprio OK; il successivo delta
scientifico `bcb462d..91a880b136dee5d805b54040f5e32345be361eb2` ha ricevuto un **nuovo OK
indipendente**, limitato alle modifiche e alla coerenza risultante delle cinque sezioni. Il verbale
del nuovo OK è stato acquisito byte-identico nel pacchetto `d35b684acbfd1f357bc34f3a21cebb18e8a6bea0`.
Sono tre riferimenti distinti: nessun verdetto è esteso a un futuro raccordo o a un manoscritto
pubblicato.

Il pacchetto `d35b684` è stato raccordato localmente sulla base comune esatta
`e82b5a08bf642ad45f77e71832958207beb1181c`. Nell'ascendenza del candidato locale sono
raggiungibili storia, bozze, verbali e **44 delle 54 fonti** registrate; delle restanti, **8**
rimangono su commit esterni non antenati e **2** sono fonti locali senza commit. Il raccordo non
integra il pacchetto in `main`, non lo pubblica e non chiude né 03.15 né la Fase 03.

#### Dettaglio

Il delta verificato allinea soprattutto `protocol.md` e `verbalizer.md` alle fonti già maturate:
`normal_dev` reale e baseline numerica della 03.9, soglia e FAR della 03.5 ormai chiusa, decisioni
statistiche della revisione 10 e regole A/B. Raccordi circoscritti mantengono coerenti
`method.md`, `threats.md`, `related_work.md` e `PIANO_SEZIONI.md`. Restano invariati lo spazio
delle label — otto fault opachi, `Normal` letterale e `Unknown` solo come astensione — e il
producer-swap previsto. Le bozze non contengono nuovi risultati diagnostici, abstract o
conclusioni e non trasformano lo storico Terra in un braccio controllato.

Il solo conflitto effettivo dell'integrazione locale riguardava `studio2/PROVENIENZA.md`.
Le sezioni 1–13 del raccordo precedente sono state conservate e la 03.15 ha ricevuto il primo
numero libero reale, §14, con il delta successivo in §14.1. Nessuna bozza scientifica, fonte
improntata o verifica è stata modificata durante la risoluzione.

#### Connessione alla letteratura e alle critiche

La sotto-fase usa il corpus unico in [`letteratura.md` §§14.1–14.6](letteratura.md) per delimitare
i riferimenti su federazione, verbalizzazione, calibrazione e statistica; non crea un secondo
corpus e non formula un claim bibliografico nuovo. La redazione rende espliciti limiti già
registrati — dipendenza U3 da N1–N5 e soglie V2, indipendenza effettiva dei cluster,
applicabilità asintotica di Tango, tracciabilità di FAR e `normal_dev` — ma non li risolve.
Il guardiano documentale controlla struttura e riferimenti storici: non è prova del merito
scientifico delle bozze.

#### Artefatti e riproducibilità

Il [report del delta](../studio2/fase03/paper_sections/REPORT_DELTA_0315.md) identifica le 54 fonti
nel relativo [registro con commit, byte e SHA-256](../studio2/fase03/paper_sections/FONTI_DELTA_0315.json).
Il [verbale del nuovo OK](../studio2/fase03/paper_sections/VERIFICA_DELTA_0315.md) misura 12.311
byte, SHA-256 `00553079e88a58a68762ba9a3400c04cb22b91f6a99f37f191b67cfd12ca9770`;
il [record di acquisizione](../studio2/fase03/paper_sections/ACQUISIZIONE_VERIFICA_DELTA_0315.md)
documenta la copia byte-identica. Il [verbale storico](../studio2/fase03/paper_sections/VERIFICA_PAPER_SECTIONS.md)
su `cf79e81` resta separato, 13.949 byte e SHA-256
`8faca80c87071d87bf66d97848c290a5724f6569be6f6040cfb6568bad022cb1`.

I **17 file del pacchetto** sotto `paper_sections/` sono invariati rispetto a `d35b684`. Dopo il
pacchetto sono state aggiunte due consegne: la [consegna operativa 03.15](../studio2/fase03/paper_sections/CONSEGNA_0315_2026-09-14.md),
acquisita byte-identica in un commit locale distinto dal merge, e la
[consegna dell'integrazione locale](../studio2/fase03/paper_sections/CONSEGNA_INTEGRAZIONE_LOCALE_0315_2026-09-14.md).
`FONTI_DELTA_0315.json`, report improntato, bozze e verbali non sono stati riscritti.

#### Lavoro che resta

La decisione D9 sui ruoli dei modelli, l'identità completa e la qualificazione del servizio
restano aperte. Restano inoltre la firma materiale e il freeze statistico della 03.8, la
fattibilità T5, ledger e calendario, gli allineamenti dell'harness 03.10 e i controlli tecnici
OOD della 03.11. FAR e A/B non sono stati riaperti. Le bozze non sono state promosse in
`docs/paper/`.

Il presente aggiornamento MD/HTML è un **nuovo delta documentale di raccordo**: deve essere
riesaminato nel successivo passaggio seriale per coerenza, link, anchor, numerazione e parità,
senza riaprire la review scientifica già conclusa su `91a880b`. Il candidato resta locale e
distinto da ogni futura integrazione in `main`, pubblicazione o congelamento. 03.15 e la Fase 03
**restano aperte**.

### Sintesi per sezione

| § | Fase | Che cos'è | Fonte | Stato |
| :---: | --- | --- | --- | --- |
| 4 | **Preparazione e capability pilot — Fase 03** | Cantieri §6.1–§6.12 e gate §7.1; §4.1–§4.4 documentano criteri, catalogo D1, run fault e perimetro del codice; §4.5 soglie Normal; §4.6 evidence 697-D; §4.7 pseudolabel; §4.9 `normal_dev` e baseline; §4.12 schema insight R4; §4.15 sezioni comuni del paper | piano §§6–7.1 e artefatti delle sotto-fasi | aperta; 03.5 chiusa e pubblicata; 03.6 verificata e documentata; 03.9 integrata e dati pubblicati, freeze pending; 03.12 R4-V OK e tag pubblicato; 03.15 verificata e raccordata solo nel candidato locale |
| 5 | **Produzione degli insight** | Gli 8×2 insight dai dati di sviluppo, più la libreria completa del producer alternativo per il braccio *producer-swap* | piano §7.2 | dopo il pilot |
| 6 | **Congelamento del protocollo** | Solo dopo il pilot, mai prima | piano §7.3 | dopo il pilot |
| 7 | **Esecuzione dello studio finale** | Tutte le inferenze A, B-LF, E-LF, più swap, OOD, ablation e canary — circa 2.853/3.555 chiamate con margine, per 6/8 run | piano §7.4 e §8.8 | dopo il congelamento |
| 8 | **Analisi e redazione** | Solo a esecuzione completata | piano §7.5 | ultima |
| 9–12 | *riservate* | Spazio per fasi non previste, o per separare l'analisi dalla redazione | — | — |

Dettaglio dei cantieri ancora previsti dal piano §§6–7:

1. **§6.1** — Criteri verificati e congelati nella sotto-fase descritta in [§4.1](#criteri-selezione-61); estrazione D1 verificata in [§4.2](#catalogo-d1), catalogo congelato e pubblicato
2. **§6.2** — Run fault di sviluppo eseguiti, verificati e conservati nella sotto-fase descritta in [§4.3](#run-fault-62): 40 run, catalogo D1, stream 30000–30039, release `studio2-fase03-fault-dev-v1`; la generazione Normal e R1/R2 erano già qualificate in §3
3. **Blocco 03.4** — Perimetro del codice Q8 chiuso nella sotto-fase descritta in [§4.4](#perimetro-codice-q8): nessun nuovo perimetro, riuso function-level secondo MAINTENANCE §8.2
3. **§6.3** — Soglia Normal calibrata e FAR verificato nella sotto-fase descritta in
   [§4.5](#soglie-normal-63): rango 334 su 350, soglia 13,623626738268857, release
   `studio2-fase03-normal-v1`; la macro-Fase 03 resta aperta
4. **§6.4** — Dati strutturati, testi neutrali e firme di sviluppo prodotti e verificati nella sotto-fase 03.6 descritta in [§4.6](#evidence-697-d); le evidence `normal_dev` sono documentate separatamente in [§4.9](#normal-dev-baseline-039)
5. **§6.5** — Pseudolabel e derangement v1 verificati in [§4.7](#pseudolabel-037); interfaccia finale con 03.12 ancora aperta
6. **§6.6** — Scrivere il piano statistico completo
7. **§6.7** — Baseline numerica costruita e verificata nella [§4.9](#normal-dev-baseline-039); freeze efficace e integrazione 03.10 pending
8. **§6.8** — Preparare l'harness API
9. **§6.9** — Generare e congelare i run finali di test
10. **§6.10** — Schema insight R4 verificato e congelato con tag pubblicato in [§4.12](#schema-insight-0312); pin dell'adapter e qualifica del pilot restano separati
11. **§6.11** — Implementare la baseline FedAvg
12. **§6.12** — Sezioni comuni del paper aggiornate e verificate in [§4.15](#paper-sections-0315); candidato soltanto locale, D9 e promozione nel manoscritto ancora aperte
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
