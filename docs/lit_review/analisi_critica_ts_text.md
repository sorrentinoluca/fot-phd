# La trasformazione TS→Testo è un punto critico per la pubblicazione?

**FoT-TEP · Analisi di Pubblicabilità · Settembre 2026**

*Analisi critica del verbalizzatore V2 rispetto alla letteratura recente (2021–2026), con valutazione dei rischi e raccomandazioni per il posizionamento scientifico.*

---

## Verdetto sintetico

> **La trasformazione TS→testo non è un punto critico bloccante, ma è un punto che richiede un posizionamento attento.** L'approccio del progetto occupa una nicchia difendibile — verbalizzazione deterministica, fedele per costruzione, senza modelli appresi, con calibrazione statistica formale — che nessun lavoro in letteratura replica esattamente. Tuttavia, due paper recenti (CGTime, giugno 2026; T2SP, giugno 2026) restringono lo spazio argomentativo e rendono necessario un confronto esplicito nella sezione Related Work.

---

## 1. Panorama della letteratura: il campo si è mosso

La trasformazione di serie temporali in testo per il consumo di LLM è un problema attivamente studiato. Dall'analisi di oltre 25 paper (2017–2026), integrata con ricerche su OpenAlex, Scopus, ArXiv, e Crossref, emergono **sette categorie di approcci**, cui il progetto FoT-TEP aggiunge una settima propria:

| Cat. | Strategia | Esempi chiave | Appreso? | Fedeltà |
|------|-----------|---------------|----------|---------|
| A | Codifica numerica diretta | LLMTime, PromptCast | No | Triviale |
| B | Allineamento latente | Time-LLM, TEST, S²IP-LLM | Sì | No |
| C | Captioning generativo | TSLM, Chronicle, BEDTime, TRUCE | Sì | Variabile |
| D | Data-to-Text deterministico | Fuzzy D2T, ICA2TEXT | No | Sì (regole) |
| E | Rappresentazione simbolica | ESAX+BoW, SAX_HAR-LLM, HSQP | Parziale | Sì (token) |
| F | Decomposizione strutturata | T2SP (Kim et al. 2026) | No | Invertibile |
| **G** | **Verbalizzazione domain-driven** | **FoT-TEP V2** | **No** | **By construction** |

### I due paper più critici da affrontare

**CGTime — Feng et al. (arXiv:2608.05238, giugno 2026)**
"Decoupling Perception from Description": codice deterministico calcola 169 statistiche (medie, PCA, correlazioni, Mahalanobis), poi un LLM (Qwen3-4B) le verbalizza. Multivariate fact score: **0.283** vs GPT-4o-mini 0.173 (+64%). Filosofia quasi identica al FoT-TEP: la percezione è deterministica, la descrizione è linguistica. Ma CGTime è un modello addestrato (4B parametri), non un renderer a template.

**T2SP — Kim et al. (arXiv:2606.12481, giugno 2026)**
"Time-Series-to-Structured-Programs": decomposizione deterministica in trend (B-spline), periodicità (Fourier), eventi (spike/Gauss), residui. Training-free, invertibile (`φ⁻¹(φ(x))=x`). GPT-5.4 + T2SP raggiunge 0.907 fidelity su TSEdit. Ma è **solo univariato** — non gestisce 41 variabili simultanee.

**BEDTime — Sen et al. (arXiv:2509.05215, settembre 2025)**
Primo benchmark per la descrizione automatica di serie temporali. ~46.800 coppie TS-descrizione su 5 dataset. Scoperta chiave: i **VLM superano nettamente LLM e TSLM** specializzati. I modelli sono fragili a perturbazioni realistiche. Nessun approccio deterministico è valutato — il benchmark esclude la categoria D/G.

---

## 2. Risposta alle quattro domande

### Domanda 1: La trasformazione TS→testo è un punto critico per la pubblicazione?

**⚠ RISCHIO MODERATO**

La trasformazione *di per sé* non è un punto critico bloccante — il campo è sufficientemente nuovo da non avere un gold standard che il progetto dovrebbe adottare. Tuttavia è un punto che **un reviewer informato può contestare** sotto due profili:

**Profilo 1 — "Perché non usare un approccio della letteratura?"** La risposta è forte: nessun approccio della letteratura soddisfa simultaneamente i vincoli del progetto (determinismo completo, fedeltà by-construction, neutralità diagnostica, calibrazione statistica, semantica temporale formale, multi-agente ready). La tabella comparativa nella sezione 3 dimostra questa unicità su ogni dimensione.

**Profilo 2 — "Perché non confrontare con alternative?"** Questa è la vulnerabilità principale. Un reviewer può chiedere: "avete confrontato il vostro verbalizzatore con SAX, con serializzazione numerica diretta, o con CGTime?". Al momento il progetto non include un'ablation empirica sulla fase di verbalizzazione. La raccomandazione è di includere almeno un confronto qualitativo sistematico (già presente nella `verbalization_comparative_analysis.md`) e idealmente un esperimento ablativo minimale: stesso LLM diagnosticatore, stesso dataset TEP, tre rappresentazioni diverse in input (testo V2, serializzazione numerica, SAX).

> **Raccomandazione:** Il verbalizzatore V2 è pubblicabile come contributo, ma richiede una sezione Related Work che lo posizioni esplicitamente rispetto a CGTime e T2SP, e almeno un confronto ablativo minimale per prevenire l'obiezione "perché non avete confrontato?".

### Domanda 2: Cosa esiste in letteratura come alternativa?

**✅ RISCHIO BASSO**

Le alternative esistono ma nessuna è un sostituto diretto. Il landscape completo comprende i seguenti comparatori rilevanti, ordinati per prossimità filosofica:

| Approccio | Cosa condivide col FoT-TEP | Cosa manca |
|-----------|---------------------------|------------|
| **CGTime** | Separazione percezione/descrizione; statistiche deterministiche; multivariate | Modello appreso (4B params); non neutrale (genera interpretazioni); non frozen; non domain-specific |
| **T2SP** | Deterministico; training-free; invertibile | Solo univariato; nessuna semantica di dominio; nessuna calibrazione statistica |
| **LLM-TSFD** | Feature statistiche → template → LLM | Soglie manuali; template diagnostici (non neutrali); no logica temporale |
| **Fuzzy D2T** | Deterministico; regole; fedeltà by-construction | Soglie fuzzy manuali; non calibrato; non multi-agente ready |
| **TRUCE** | Obiettivo: fedeltà fattuale | Modello neurale appreso; non deterministico; solo univariato |
| **SAX_HAR-LLM** | Interfaccia simbolica interpretabile TS→LLM; auditabilità | Fine-tuning LLM; dominio HAR; SAX perde informazione continua |

**Sintesi:** Il progetto FoT-TEP è l'unico ad operare nella intersezione di: (1) determinismo completo senza modelli appresi, (2) calibrazione statistica formale (conformal α=0.05), (3) neutralità diagnostica, (4) semantica temporale strutturata (fasi, run, persistenza), (5) scala multivariata (41 variabili × 8 finestre × 5 feature). Nessun singolo approccio della letteratura copre più di due di questi cinque assi.

### Domanda 3: Sono state fatte comparazioni in letteratura per stabilire quale approccio è migliore?

**⚠ RISCHIO MODERATO**

La risposta è **sì, ma con importanti caveat**. Tre lavori recenti contribuiscono comparazioni sistematiche:

**BEDTime** (Sen et al. 2025) è il primo benchmark dedicato, con ~46.800 coppie TS-descrizione e tre task (recognition, differentiation, generation). Risultato principale: i VLM (GPT-4o-Vision) dominano nettamente su LLM e TSLM specializzati. Tuttavia il benchmark **non valuta approcci deterministici** (categoria D/G): tutti i baseline sono modelli neurali. Questo è sia una limitazione del benchmark sia un'opportunità per il progetto.

**CGTime** (Feng et al. 2026) include un confronto su "multivariate fact score" che è il più vicino a una valutazione della fedeltà fattuale per serie multivariate. CGTime (4B) supera GPT-4o-mini e GPT-5.4-nano, ma il confronto è tra modelli generativi — nessun approccio deterministico è nella baseline.

**T2SP** (Kim et al. 2026) confronta rappresentazione strutturata vs serializzazione numerica vs input visivo su task di editing, mostrando che la rappresentazione strutturata domina (+15% fidelity su raw, +41% su vision). Ma è solo univariato.

Il survey TMLR 2026 di Chen et al. ("Reasoning and Agentic Systems in Time Series with LLMs") cataloga oltre 100 paper in una tassonomia basata su topologia di ragionamento, ma non include una comparazione empirica diretta tra strategie di rappresentazione.

> **Implicazione per la pubblicazione:** Non esiste una comparazione diretta che includa approcci deterministici come il FoT-TEP. Questo è un **vantaggio**: non c'è un benchmark che dimostra che un'alternativa è superiore al vostro approccio. Ma è anche una **vulnerabilità**: un reviewer può obiettare che l'assenza di confronto non è prova di superiorità. L'esperimento ablativo raccomandato sopra colmerebbe questa lacuna.

### Domanda 4: Il problema TS→testo è stato discusso abbastanza in letteratura?

**✅ RISCHIO BASSO**

Il problema è stato discusso **ampiamente ma in modo frammentato**, e questo gioca a favore del progetto per tre ragioni:

**Il campo è maturo abbastanza da essere legittimo.** I survey (Jiang et al. IJCAI 2024; Abdullahi et al. IEEE Access 2025; Chen et al. TMLR 2026) riconoscono la trasformazione TS→testo come un sotto-problema distinto e attivo. Esistono benchmark dedicati (BEDTime), workshop tematici, e una tassonomia emergente. Un paper che contribuisce a questo campo è posizionabile.

**Ma non è così saturo da non avere spazio.** La maggior parte della letteratura si concentra sulle categorie A-C (serializzazione, allineamento latente, captioning generativo). Le categorie D-G (deterministico, simbolico, strutturato, domain-driven) sono sottorappresentate. La nicchia specifica del FoT-TEP — verbalizzazione deterministica fedele per sistemi multi-agente industriali — ha zero occupanti diretti.

**Le lacune della letteratura coincidono con i punti di forza del progetto.** I problemi aperti identificati dalla letteratura includono: fedeltà fattuale delle descrizioni (BEDTime mostra fragilità dei modelli neurali), scalabilità multivariata (CGTime inizia ad affrontarla, T2SP è solo univariato), e riproducibilità (nessun paper nella letteratura TS→testo propone un protocollo di freeze).

---

## 3. Mappa di posizionamento: cinque assi di differenziazione

### Fedeltà by-construction
Solo Fuzzy D2T e ICA2TEXT condividono questa proprietà, ma con soglie manuali. Il FoT-TEP aggiunge calibrazione conformal (α=0.05). CGTime e TRUCE mirano alla fedeltà ma con modelli appresi — residuo di errore non eliminabile.

### Neutralità diagnostica
Proprietà unica. Nessun altro approccio separa esplicitamente verbalizzazione e diagnosi. LLM-TSFD include indicatori diagnostici nei template; CGTime genera interpretazioni; T3 produce narrazioni ricche. Per la Federation over Text, la neutralità è un requisito architetturale.

### Semantica temporale formale
Run consecutivi, episodi sostenuti, persistenza globale, drift coerente, partizione in tre fasi. Nessun altro approccio formalizza la struttura temporale a questo livello. T2SP ha trend/period/events ma senza persistenza o fasi; BEDTime valuta "temporal localization" ma nessun baseline la gestisce bene.

### Scala multivariata
41 variabili × 8 finestre × 5 feature = 1.640 valori. T2SP è solo univariato. CGTime gestisce multivariato (PCA a O(rK)) ma con modello appreso. LLMTime, TRUCE, BEDTime baseline sono monovariati. Solo LLM-TSFD e Fuzzy D2T lavorano su multivariato, ma senza la granularità temporale del FoT-TEP.

---

## 4. Rischi specifici e mitigazioni

| Rischio reviewer | Gravità | Mitigazione |
|-----------------|---------|-------------|
| "Perché non avete confrontato con CGTime?" | **ALTA** | Confronto qualitativo nella Related Work (deterministico+template vs appreso+generativo). Idealmente, un'ablation: stesso LLM, testo V2 vs statistiche grezze vs SAX. CGTime non è replicabile in tempo utile (4B-param training), ma le differenze architetturali (appreso vs frozen, interpretativo vs neutrale) sono argomentabili. |
| "L'approccio è troppo domain-specific, non generalizza" | **MEDIA** | È un punto di forza, non di debolezza: la calibrazione su Normal N1-N5 e il vocabolario controllato sono *features* del design per fault diagnosis industriale. Citare che il progetto prevede estensione a PV (fotovoltaico) con la stessa architettura. |
| "Nessuna feature frequenziale è una limitazione seria" | **MEDIA** | Dichiarata esplicitamente nel freeze document come trade-off consapevole. Le feature tempo-dominio catturano shift e drift (i pattern dominanti nel TEP); l'analisi spettrale è delegabile a un secondo verbalizzatore specializzato in un'architettura modulare. |
| "Il benchmark BEDTime esiste — perché non lo usate?" | **BASSA** | BEDTime valuta captioning generico (stock, sintetico); il FoT-TEP opera su process data industriale con vincoli di fedeltà diversi. I dataset BEDTime non hanno ground truth per fault diagnosis. Citare BEDTime nel panorama ma argomentare che il benchmark appropriato è task-specific. |
| "Il testo è in italiano — limita la generalizzabilità" | **BASSA** | Il renderer è un modulo sostituibile; il vocabolario controllato (14 termini) è traducibile in modo deterministico. Il contributo è l'architettura (pipeline deterministica), non la lingua specifica. |

---

## 5. CGTime: il competitor da indirizzare

CGTime (Feng et al., HKUST/TUM/CAS, giugno 2026) merita una trattazione dedicata perché propone la **stessa filosofia fondamentale** del FoT-TEP: separare la percezione deterministica dalla descrizione linguistica. Le differenze sono tuttavia sostanziali:

| Dimensione | CGTime | FoT-TEP V2 |
|-----------|--------|------------|
| Percezione | 169 statistiche (univariate + PCA + correlazioni + Mahalanobis) | 5 feature × 41 var × 8 finestre (1.640 valori); soglie conformal |
| Descrizione | LLM Qwen3-4B fine-tuned (SFT + GRPO) | Renderer deterministico a template; vocabolario controllato |
| Parametri appresi | 4 miliardi | Zero |
| Fedeltà | Metrica Gaussian kernel per verificare fatti; non garantita | Garantita by-construction (template + vocabolario controllato) |
| Neutralità | Genera descrizioni interpretative ("risk indicators suggest…") | Solo osservazioni ("XMEAS_12 supera soglia in 6/8 finestre") |
| Dominio | General-purpose (multiple dataset) | TEP industriale con calibrazione domain-specific |
| Riproducibilità | Codice rilasciato; training richiede GPU | SHA-256 freeze; eseguibile su CPU in <1s per caso |
| Multi-agente | Non previsto | Progettato per Federation over Text |

> **Argomento difensivo:** CGTime e FoT-TEP condividono il principio "percezione deterministica + descrizione linguistica" ma fanno scelte opposte nella fase di descrizione: CGTime massimizza la ricchezza espressiva (LLM generativo), FoT-TEP massimizza la fedeltà e la controllabilità (template deterministico). In un contesto di fault diagnosis industriale multi-agente dove la verifica umana, la riproducibilità e l'assenza di allucinazioni sono prioritarie, la scelta del FoT-TEP è giustificata. CGTime è il complemento ideale per contesti dove la ricchezza della descrizione è più importante della garanzia di fedeltà.

---

## 6. Raccomandazioni operative per la pubblicazione

### Nella sezione Related Work

Strutturare il posizionamento attorno a tre filoni: (1) **TS→testo generativo** — TSLM, Chronicle, BEDTime, CGTime — riconoscendo la ricchezza espressiva ma evidenziando il rischio di allucinazione documentato da BEDTime; (2) **TS→testo deterministico** — Fuzzy D2T, ICA2TEXT, T2SP, LLM-TSFD — il filone metodologico a cui il progetto appartiene, distinguendosi per calibrazione statistica e neutralità; (3) **TS→LLM via rappresentazione intermedia** — SAX_HAR-LLM, HSQP, ESAX+BoW — approcci simbolici che condividono la filosofia ma producono token, non testo leggibile.

### Come esperimento aggiuntivo (fortemente raccomandato)

Un'ablation minimale a tre bracci sullo stesso LLM diagnosticatore e lo stesso dataset TEP: (a) testo V2 del verbalizzatore, (b) serializzazione numerica diretta (stile LLMTime), (c) rappresentazione SAX dei segnali. Metriche: accuratezza diagnostica, fedeltà fattuale del ragionamento, lunghezza/costo del prompt. Questo singolo esperimento smonterebbe l'obiezione "perché non avete confrontato?" e potrebbe diventare un contributo secondario del paper.

### Come framing del contributo

Non presentare il verbalizzatore come "il modo migliore" di trasformare TS in testo — la letteratura è troppo frammentata per sostenerlo. Presentarlo come **"il primo approccio deterministico con calibrazione statistica formale per la verbalizzazione fedele di serie temporali multivariate industriali, progettato per architetture multi-agente"**. Ogni parola di questa frase è difendibile con evidenza dal codice e dalla letteratura.

---

### Fonti principali

- CGTime: Feng et al. 2026, [arXiv:2608.05238](https://arxiv.org/abs/2608.05238)
- T2SP: Kim et al. 2026, [arXiv:2606.12481](https://arxiv.org/abs/2606.12481)
- BEDTime: Sen et al. 2025, [arXiv:2509.05215](https://arxiv.org/abs/2509.05215)
- TRUCE: Jhamtani & Berg-Kirkpatrick, EMNLP 2021
- Fuzzy D2T: Ramos-Soto et al. 2017
- SAX_HAR-LLM: Pappa et al. 2026, Expert Systems with Applications
- HSQP: Abdullahi et al. 2026, IEEE Access
- LLM-TSFD: vari
- Survey: Chen et al. TMLR 2026; Jiang et al. IJCAI 2024; Abdullahi et al. IEEE Access 2025

### Documenti del progetto analizzati

`tep_verbalize_v2.py`, `tep_verbalize.py`, `verbalizer_config_v2.json`, `verbalization_comparative_analysis.md`, `FOT_TEP_GAP_ANALYSIS_AND_RELATED_WORK.md`, `related_work_scan.md`, `literature_review_pv_text_federated.md`.

### Query di ricerca effettuate

Periodo coperto: 2021–2026. Paper nuovi identificati non presenti nelle review esistenti del progetto: CGTime, BEDTime, T2SP, survey TMLR 2026.

#### OpenAlex (3 query)

| # | Query | Risultati rilevanti | Copertura |
|---|-------|---------------------|-----------|
| O1 | `"time series" AND ("verbalization" OR "text generation" OR "natural language description")` | TRUCE, T3, Repr2Seq, TSLM, Chronicle | Filone captioning/narration generativo (Cat. C) e data-to-text (Cat. D) |
| O2 | `"time series" AND "faithfulness" AND ("captioning" OR "description")` | Truth-Conditional Captions (Jhamtani 2021), BEDTime (Sen 2025) | Fedeltà fattuale — nucleo del posizionamento FoT-TEP |
| O3 | `"time series" AND "data-to-text" AND ("deterministic" OR "rule-based")` | Fuzzy D2T (Ramos-Soto 2017), ICA2TEXT (Cascallar-Fuentes 2022) | Filone deterministico/linguistico (Cat. D) |

#### Scopus (2 query)

| # | Query | Risultati rilevanti | Copertura |
|---|-------|---------------------|-----------|
| S1 | `TITLE-ABS-KEY("time series" AND "natural language" AND ("generation" OR "verbalization"))` | TADACap, CLaSP, survey Jiang 2024 | Panorama ampio TS→testo; retrieval-based e contrastive |
| S2 | `TITLE-ABS-KEY("time series" AND "text" AND ("faithful" OR "deterministic" OR "symbolic"))` | ESAX+BoW (Zhao 2022), SAX_HAR-LLM (Pappa 2026), HSQP (Abdullahi 2026) | Filone simbolico (Cat. E) e interfacce TS→LLM |

#### WebSearch / Google Scholar (4 query)

| # | Query | Paper trovato | Note |
|---|-------|---------------|------|
| W1 | `CGTime "Decoupling Perception from Description" time series 2026` | CGTime (Feng et al., arXiv:2608.05238) | Competitor principale — non presente in nessuna review precedente |
| W2 | `BEDTime benchmark time series description evaluation 2025` | BEDTime (Sen et al., arXiv:2509.05215) | Primo benchmark TS→descrizione; ~46.800 coppie |
| W3 | `T2SP "Time-Series-to-Structured-Programs" deterministic 2026` | T2SP (Kim et al., arXiv:2606.12481) | Decomposizione deterministica invertibile; solo univariato |
| W4 | `survey time series LLM reasoning agentic TMLR 2026` | Chen et al. TMLR 2026 | Survey 100+ paper; tassonomia per topologia di ragionamento |

#### ArXiv (2 query)

| # | Query | Risultati rilevanti | Note |
|---|-------|---------------------|------|
| A1 | `time series captioning description multivariate 2025-2026` | CGTime (conferma), FD-LLM (Qaid 2024, Lin 2025) | Verifica incrociata con WebSearch |
| A2 | `time series text representation benchmark evaluation` | BEDTime (conferma), survey Abdullahi IEEE Access 2025 | Copertura benchmark e survey |

#### Crossref (1 query)

| # | Query | Risultati rilevanti | Copertura |
|---|-------|---------------------|-----------|
| C1 | `"time series" "text generation" "fault diagnosis"` | FD-LLM (Lin 2025, AEI), LLM-TSFD | Intersezione TS→testo + diagnostica industriale |

**Nota metodologica.** Le query sono state progettate con strategia a imbuto: (1) discovery ampio su OpenAlex e Scopus per il panorama completo, (2) query mirate su WebSearch per paper specifici emersi da citazioni incrociate, (3) verifica su ArXiv e Crossref per conferma e completamento. La copertura complessiva abbraccia tutte e sette le categorie della tassonomia (A–G), con enfasi sulle categorie C (captioning generativo), D (D2T deterministico) e E (simbolico) più rilevanti per il posizionamento del FoT-TEP.
