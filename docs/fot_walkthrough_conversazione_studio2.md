# Studio 2 — walkthrough

> **Documento vivo, a scheletro.** Si aggiorna **fase per fase**: si lavora su una fase, si
> documenta qui, si passa alla successiva. Stato al **2026-09-12**: **fase 01 documentata in §2**;
> le fasi successive restano a scheletro. Finché una sezione resta vuota, **la fonte autorevole è
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
| Calibrazione delle soglie | `lit_review/DECISIONE_calibrazione_soglie_fase_B.md` (rev. 18) | **prevale sul piano**: il piano dichiara di non riformularne la decisione. Sette requisiti residui, tre bloccanti |
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

Nessuno dei tre si risolve dentro una singola sessione di lavoro: richiedono una decisione
dell'autore. Restano qui finché non sono chiusi, con la data in cui sono stati registrati.

| # | Punto aperto | Perché blocca | Chi decide | Registrato | Decisione da chiudere in |
| :---: | --- | --- | --- | --- | --- |
| 1 | **Sigle `C06`, `C07`, `C18`** citate dal piano sperimentale | Vengono dal registro critiche `C01–C18`, che esiste **solo** in `fot_walkthrough_conversazione.md` §33 — la prima esposizione del primo studio, che non è fonte. Finché restano così sono riferimenti appesi a un documento che nessuno deve usare | riportarle per esteso nel piano **oppure** rinumerarle | 2026-09-12 | `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` §0.1 — **non** il piano BIGDATA2026, che §0 esclude dalle fonti autorevoli |
| 2 | **Quali dati del primo studio lo studio 2 riusa davvero** | Se sono solo i run Normal per la calibrazione è una cosa; se sono anche gli insight o le soglie congelate è un'altra, e cambia quanto dello **strato operativo** va recuperato dalla prima esposizione (schema del testo neutrale §9, contabilità byte/token §29, definizioni statistiche §6 e §8) | autore | 2026-09-12 | `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` §0.1, più un registro in `docs/lit_review/` se la selezione del riuso richiede motivazione per singolo dato |
| 3 | **Perimetro del codice della Q8** | La terza metrica di §8.5, il cap sulla lunghezza dello schema, l'estensione a 8 agenti e il derangement a 7 pseudolabel richiedono tutti di scrivere dentro `phase_b/`, che [`MAINTENANCE.md`](MAINTENANCE.md) §1 dichiara **congelato**. Nessuna sessione può decidere da sola di scriverci | aprire un perimetro nuovo (`phase_b/q8/`) **oppure** dichiarare quale parte di `phase_b/` è harness riutilizzabile e quale è artefatto — in entrambi i casi è una modifica a §1 | 2026-09-12 | `docs/MAINTENANCE.md` §1 (separato tra harness riutilizzabile e artefatto) |

*Registrati il 2026-09-12. Quando uno si chiude, va tolto da qui e la decisione va scritta dove
compete: nel piano, in un registro di `lit_review/`, o in `MAINTENANCE.md` §1.*

---

## 1 · Introduzione

*Scheletro. Ogni voce dice dove sta oggi la fonte; il testo si scrive quando la fase relativa
è conclusa.*

- **Le fasi dello studio 2** — la fase 01 è documentata in
  [§2](#2--preparazione-indipendente-dal-modello--ricognizione-del-patrimonio-fase-01) e le
  successive sono mappate in [§3–12](#312--fasi-successive); l'ordine dentro §6 è vincolato: preparazione
  indipendente dal modello, capability pilot come gate, produzione insight, congelamento, esecuzione, analisi.
- **Obiettivo e domanda scientifica dello studio 2** — piano §8
- **Che cosa cambia rispetto al primo studio** — e che cosa viene riusato: da decidere e
  scrivere qui, è la voce che manca a tutti gli altri documenti
- **Banco di prova: agenti, guasti, pseudolabel** — piano §8; ⚠️ le pseudolabel sono **nove**,
  non dieci: `Unknown` è il nome dell'astensione, non una classe
- **Condizioni e bracci** — piano §8, incluso il braccio *producer-swap*
- **Popolazione, endpoint e contrasti** — piano §8.5
- **Protocollo di valutazione e criteri di successo** — piano §8.5, §11 (GO/NO-GO)
- **Baseline** — piano §9
- **Che cosa non è ancora congelato** — piano §0.1, più i sette requisiti residui di
  `lit_review/DECISIONE_calibrazione_soglie_fase_B.md`
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

Prima delle fasi dipendenti dal modello restano da realizzare la messa in sicurezza dei 74
contenuti, la decisione su R1/R2, `Ts_base`, burn-in, Philox, score eseguibile e casi degeneri,
verifica dei prefissi, scelte ancora aperte del piano e congelamento degli artefatti effettivamente
usati. I tre punti di §0.1 restano aperti.

---

## 3–12 · Fasi successive

Le fasi successive vengono da **§6** (i cantieri di preparazione indipendenti dal modello ancora
da eseguire) e **§7** (esecuzione subordinata alla disponibilità di Qwen) del piano sperimentale.

### Sintesi per sezione

| § | Fase | Che cos'è | Fonte | Stato |
| :---: | --- | --- | --- | --- |
| 3 | **Capability pilot** | Il *gatekeeper*: il modello risponde, il JSON passa il parser, il budget di ragionamento tiene, la stabilità regge | piano §7.1 | bloccata dall'API |
| 4 | **Produzione degli insight** | Gli 8×2 insight dai dati di sviluppo, più la libreria completa del producer alternativo per il braccio *producer-swap* | piano §7.2 | dopo il pilot |
| 5 | **Congelamento del protocollo** | Solo dopo il pilot, mai prima | piano §7.3 | dopo il pilot |
| 6 | **Esecuzione dello studio finale** | Tutte le inferenze A, B-LF, E-LF, più swap, OOD, ablation e canary — circa 2.853/3.555 chiamate con margine, per 6/8 run | piano §7.4 e §8.8 | dopo il congelamento |
| 7 | **Analisi e redazione** | Solo a esecuzione completata | piano §7.5 | ultima |
| 8–12 | *riservate* | Spazio per fasi non previste, o per separare l'analisi dalla redazione | — | — |

Dettaglio dei cantieri ancora previsti dal piano §§6–7:

1. **§6.1** — Definire i criteri di selezione degli 8 fault
2. **§6.2** — Generare nuovi run di sviluppo
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
