# Analisi Comparativa: Approccio di Verbalizzazione del Progetto FoT-TEP vs. Letteratura

**Progetto:** Text-Based Federated Multi-Agent System (FoT-TEP)
**Data:** Settembre 2026

---

## 1. Panoramica dell'Approccio del Progetto

Il verbalizzatore V2 del progetto FoT-TEP trasforma serie temporali multivariate del Tennessee Eastman Process (41 variabili XMEAS, campionate a 1 min) in descrizioni testuali neutrali destinate al ragionamento di un LLM. La pipeline segue uno schema rigoroso:

**Serie Temporale → Feature Statistiche per Finestra → Struttura Numerica Intermedia → Testo Neutrale in Linguaggio Naturale**

Le caratteristiche architetturali fondamentali sono:

- **Finestre temporali fisse** di 5 ore (8 finestre post-iniezione guasto nell'intervallo 10–50 h), con partizione in tre fasi: iniziale (prime 2 finestre), intermedia e tardiva (ultime 2).
- **Cinque feature primarie per variabile per finestra**: `shift_sigma` (spostamento di livello normalizzato), `slope_sigma_h` (pendenza OLS locale), `residual_std_ratio` (variabilità residua dopo detrending lineare), `diff_std_ratio` (variazioni campione-campione), `raw_std_ratio` (dispersione complessiva).
- **Soglie congelate** calibrate esclusivamente su dati normali di sviluppo (N1–N5), con approccio conformal/nearest-rank ad α = 0.05.
- **Logica temporale strutturata**: run di attivazione consecutivi, episodi sostenuti (≥2 finestre), consistenza di segno, persistenza globale stretta, drift coerente, transiente di assestamento.
- **Renderer neutrale**: produce testo osservazionale in italiano, senza diagnosi, senza etichette di guasto, senza prototipi diagnostici. Il testo riporta conteggi di soglia, direzioni, run, attività early/late.
- **Vocabolario controllato**: 14 termini ammessi (es. "spostamento di livello", "drift persistente", "variabilità rapida persistente") e 4 termini proibiti (es. "oscillazione", "periodicità").

---

## 2. Tassonomia delle Strategie di Verbalizzazione nella Letteratura

Dalla literature review emergono tre macro-categorie di approcci, ciascuna con una filosofia diversa sul rapporto tra dati numerici e testo:

| Categoria | Approcci | Principio |
|---|---|---|
| **A. Codifica Numerica Diretta** | LLMTime, PromptCast | I numeri stessi diventano token testuali |
| **B. Allineamento Latente** | Time-LLM, TEST, S²IP-LLM | Embedding delle serie temporali nello spazio semantico dell'LLM |
| **C. Generazione Descrittiva** | TSLM, BEDTime, Chronicle, GPT4MTS | Un modello produce descrizioni in linguaggio naturale |

Il progetto FoT-TEP non rientra in nessuna di queste tre categorie. Introduce una **quarta strategia** che definiamo:

> **D. Verbalizzazione Strutturata Domain-Driven**: le serie temporali vengono prima ridotte a feature statistiche interpretabili tramite regole deterministiche domain-specific, poi le feature vengono rese in linguaggio naturale tramite un renderer basato su template. Non c'è alcun modello appreso nel processo di verbalizzazione.

---

## 3. Confronto Dimensione per Dimensione

### 3.1 Meccanismo di Trasformazione

| Approccio | Trasformazione | Apprendimento Coinvolto | Determinismo |
|---|---|---|---|
| **LLMTime** | Serializzazione CSV dei valori grezzi | Nessuno | Deterministico |
| **PromptCast** | Template fissi con valori numerici inline | Fine-tuning del decoder | Semi-deterministico |
| **Time-LLM** | Cross-attention con prototipi testuali appresi | Addestramento della proiezione | Non deterministico |
| **TEST** | Proiezione in spazio di prototipi testuali | Rete di proiezione appresa | Non deterministico |
| **S²IP-LLM** | Retrieval di word embedding più vicini | Apprendimento contrastivo | Non deterministico |
| **TSLM** | Encoder CNN+Attention → decoder linguistico | Encoder+decoder appresi | Non deterministico |
| **Chronicle** | Tokenizzazione unificata numeri+testo | Pre-training congiunto | Non deterministico |
| **GPT4MTS** | Dual encoding numerico+testuale con cross-attention | Cross-attention appresa | Non deterministico |
| **LLM-TSFD** | Feature statistiche → template testuali → LLM | Nessuno nel verbalizzatore | Deterministico |
| **FoT-TEP V2** | Feature statistiche + soglie congelate → renderer neutrale | **Nessuno** | **Completamente deterministico** |

**Osservazione critica**: Il progetto FoT-TEP condivide la filosofia di LLM-TSFD (estrazione di feature → template testuali → ragionamento LLM) ma va significativamente oltre in tre aspetti:

1. **Calibrazione statistica delle soglie** (conformal-style, α = 0.05), non soglie arbitrarie o manuali.
2. **Logica temporale formale** (run, persistenza, coerenza di drift, fasi temporali), non semplici conteggi.
3. **Separazione esplicita verbalizzazione/diagnosi**: il testo è neutrale per design, il ragionamento diagnostico è delegato interamente all'LLM. LLM-TSFD, al contrario, incorpora indicazioni diagnostiche già nella fase di template.

### 3.2 Granularità e Ricchezza dell'Informazione

| Approccio | Unità di Input | Variabili Gestite | Semantica Temporale |
|---|---|---|---|
| **LLMTime** | Intera serie grezza | Monovariata | Implicita (posizionale) |
| **PromptCast** | Valori puntuali con timestamp | Monovariata | Timestamp espliciti |
| **Time-LLM** | Patch di serie temporale | Monovariata per patch | Patch-level, no fasi |
| **TEST** | Segmenti di serie temporale | Monovariata per segmento | Assente |
| **TSLM** | Intera serie temporale | Monovariata | Tendenze globali |
| **LLM-TSFD** | Feature aggregate | Multivariata | Aggregata, no finestre |
| **FoT-TEP V2** | **Feature per finestra per variabile** | **41 variabili simultanee** | **Tre fasi + run + episodi** |

Il progetto FoT-TEP opera a una granularità senza precedenti nella letteratura: 41 variabili × 8 finestre × 5 feature = **1.640 valori** ridotti a una struttura intermedia di 697 componenti normalizzate (per l'evaluator) e a un testo di circa 100–200 parole (per il renderer). Nessun altro approccio gestisce simultaneamente questo volume di informazione multivariata con semantica temporale strutturata.

### 3.3 Trattamento del Dominio

| Approccio | Knowledge Domain | Come Entra |
|---|---|---|
| **LLMTime** | Nessuno | Delegato implicitamente all'LLM |
| **PromptCast** | Metadati nel template | Testo statico nel prompt |
| **Time-LLM** | Prompt-as-Prefix | Prefisso contestuale + prototipi |
| **TEST** | Vocabolario di prototipi | Parole-ancora scelte manualmente |
| **LLM-TSFD** | Tassonomia guasti nel prompt | Template + alberi decisionali |
| **FoT-TEP V2** | **Baseline statistica + semantica delle feature + vocabolario controllato** | **Integrato nel codice e nella configurazione** |

Il progetto FoT-TEP integra la conoscenza di dominio in tre strati distinti:

1. **Strato statistico**: la baseline dai dati normali N1–N5 fornisce i parametri di normalizzazione (media, deviazione standard per ogni XMEAS). Le soglie sono derivate quantitativamente, non prescelte.
2. **Strato semantico**: il file di configurazione (`verbalizer_config_v2.json`) definisce formalmente la semantica di ogni feature (es. `shift_sigma` = "signed displacement of the window mean in baseline standard-deviation units").
3. **Strato lessicale**: il vocabolario controllato ammette solo termini che il renderer può generare, impedendo interpretazioni automatiche premature (es. vietato "oscillazione" che implicherebbe una diagnosi).

Questo design a tre strati non ha equivalenti nella letteratura, dove la conoscenza di dominio è tipicamente incorporata in modo meno strutturato (prototipi appresi in TEST/Time-LLM, prompt manuali in LLM-TSFD).

### 3.4 Riproducibilità e Congelamento

| Approccio | Riproducibilità | Congelamento Formale |
|---|---|---|
| **LLMTime** | Dipende dal modello LLM | No |
| **PromptCast** | Dipende dal fine-tuning | No |
| **Time-LLM** | Dipende dall'addestramento | No |
| **Metodi con componenti appresi** | Variabile | No |
| **LLM-TSFD** | Alta per l'estrazione, variabile per l'LLM | No |
| **FoT-TEP V2** | **Completamente riproducibile** | **Sì: hash SHA-256 di tutti i file, dataset commit, protocollo di validazione pre-definito** |

Questo è probabilmente il punto di **massima differenziazione** del progetto. Il freeze document (`VERBALIZER_V2_FREEZE.md`) stabilisce un protocollo scientifico completo:

- Hash SHA-256 dei file di codice e configurazione congelati.
- Separazione esplicita tra dati di sviluppo, validazione e test.
- Protocollo di reporting per la validazione definito prima di aprire i dati di validazione.
- Nessun parametro appreso: la verbalizzazione è interamente deterministica data la stessa configurazione e gli stessi dati di input.

Nessun approccio nella letteratura raggiunge questo livello di rigore sperimentale nella fase di verbalizzazione.

### 3.5 Neutralità vs. Diagnosi

| Approccio | Output della Verbalizzazione | Diagnosi |
|---|---|---|
| **LLMTime** | Numeri come stringa | Nessuna |
| **PromptCast** | Frase con valori | Nessuna |
| **Time-LLM** | Token riprogrammati (non leggibili) | Embedding space |
| **TEST** | Prototipo più vicino | Classificazione implicita |
| **TSLM** | Descrizione in linguaggio naturale | Può contenere interpretazioni |
| **LLM-TSFD** | Template con indicatori diagnostici | Integrata nella verbalizzazione |
| **FoT-TEP V2** | **Testo puramente osservazionale** | **Esplicitamente esclusa** |

La scelta architetturale del progetto di rendere il verbalizzatore *completamente neutrale* è unica. Il freeze document lo dichiara esplicitamente:

> *"The intended pipeline is: time series → structured numerical evidence → neutral text → reasoning/diagnosis"*

Questa separazione è cruciale per l'architettura federata: il testo scambiato tra agenti è **evidenza**, non diagnosi. Ogni agente riceve le stesse osservazioni neutrali e applica il proprio ragionamento diagnostico, permettendo il dibattito multi-agente (Du et al., 2024) su interpretazioni diverse della stessa evidenza.

---

## 4. Posizionamento Rispetto ai Framework della Letteratura

### 4.1 Rispetto alla Pipeline LLM-TSFD

Il progetto FoT-TEP adotta la stessa struttura a tre stadi di LLM-TSFD (estrai → verbalizza → ragiona), ma con innovazioni sostanziali:

| Aspetto | LLM-TSFD | FoT-TEP V2 |
|---|---|---|
| Feature | Statistiche + frequenziali (FFT) | Solo dominio temporale (no FFT, no wavelet) |
| Soglie | Non specificate / manuali | Calibrate formalmente (conformal, α=0.05) |
| Template | Con interpretazioni diagnostiche | Puramente neutrali |
| Logica temporale | Assente | Formalizzata (fasi, run, persistenza) |
| Congelamento | Non previsto | Hash SHA-256 + protocollo |
| Contesto federato | Non previsto | Progettato per Federation over Text |

La scelta di escludere feature frequenziali (FFT, wavelet) è una **limitazione consapevole**, dichiarata esplicitamente nel freeze document:

> *"Minimal time-domain features cannot always distinguish very slow oscillation from nonlinear transients, or rapid oscillation from increased stochastic noise variance."*

Questa trasparenza sulle limitazioni è rara nella letteratura e coerente con la filosofia di neutralità del progetto.

### 4.2 Rispetto a Time-LLM e TEST (Allineamento con Prototipi)

Il progetto FoT-TEP condivide con Time-LLM e TEST l'idea di mediare tra serie temporali e testo attraverso un livello semantico intermedio, ma il meccanismo è fondamentalmente diverso:

- **Time-LLM/TEST**: prototipi testuali appresi nello spazio latente dell'LLM; l'allineamento è un'operazione differenziabile.
- **FoT-TEP**: "prototipi" sono feature statistiche con semantica esplicita e vocabolario controllato; l'allineamento è un'operazione deterministica basata su soglie calibrate.

Il vantaggio del progetto è la **completa interpretabilità**: ogni passaggio dalla serie temporale al testo è tracciabile e verificabile. Il vantaggio di Time-LLM/TEST è la **capacità di catturare pattern non lineari** che feature statistiche semplici potrebbero non cogliere.

### 4.3 Rispetto a TSLM e Chronicle (Generazione Descrittiva)

TSLM e Chronicle producono descrizioni in linguaggio naturale "end-to-end", con un modello generativo che decide autonomamente cosa descrivere. Il progetto FoT-TEP adotta l'approccio opposto:

- **TSLM/Chronicle**: il modello decide *cosa* è saliente e *come* descriverlo → rischio di allucinazioni, mancanza di riproducibilità.
- **FoT-TEP**: il codice deterministico decide *cosa* è saliente (soglie calibrate) e *come* descriverlo (renderer con vocabolario controllato) → nessuna allucinazione possibile, ma minor flessibilità espressiva.

Per un sistema di fault diagnosis industriale dove l'affidabilità è prioritaria rispetto alla ricchezza espressiva, la scelta del progetto è ben motivata.

### 4.4 Rispetto a Federation over Text (Protocollo Federato)

Il paper "Federation over Text" (arXiv:2604.16778) — presente nella cartella `papers/` del progetto — fornisce il framework architetturale per lo scambio di insight testuali tra agenti. Il verbalizzatore V2 si colloca come il **componente di produzione degli insight locali** di questa architettura:

- Federation over Text assume che ogni agente produca insight testuali dal proprio dato locale → il verbalizzatore V2 è esattamente questo componente.
- Il paper non specifica *come* produrre gli insight da dati numerici → il verbalizzatore V2 fornisce questa risposta per il dominio delle serie temporali industriali.
- La neutralità del testo prodotto è coerente con la filosofia federata: agenti diversi possono applicare ragionamenti diagnostici diversi sulla stessa evidenza testuale.

---

## 5. Punti di Forza e Limitazioni

### 5.1 Punti di Forza Unici del Progetto

1. **Rigore scientifico del congelamento**: nessun approccio in letteratura presenta un protocollo di freeze con hash, split dei dati, e reporting pre-definito per la fase di verbalizzazione.

2. **Separazione verbalizzazione/diagnosi**: la neutralità del renderer permette di usare lo stesso testo per ragionamento locale, dibattito multi-agente, e audit umano — un requisito critico per la Federation over Text.

3. **Determinismo completo**: dato lo stesso input e la stessa configurazione, il testo prodotto è identico. Questo è essenziale per la riproducibilità scientifica e per il debugging in un sistema multi-agente.

4. **Logica temporale formale**: la partizione in fasi (iniziale/intermedia/tardiva), la rilevazione di run coerenti, e i criteri di persistenza globale stretta sono un livello di analisi temporale strutturata che manca in tutti gli approcci della letteratura.

5. **Scalabilità multivariata**: 41 variabili analizzate simultaneamente con la stessa pipeline, con ranking automatico delle variabili dominanti — un aspetto non affrontato dalla maggior parte della letteratura che lavora su serie monovariate.

### 5.2 Limitazioni Identificate

1. **Nessuna feature frequenziale**: l'esclusione esplicita di FFT/wavelet limita la capacità di distinguere oscillazioni lente da transienti non lineari. Approcci come LLM-TSFD includono feature spettrali.

2. **Compressione dell'informazione**: il renderer produce solo le variabili "dominanti" (top 4 per categoria), potenzialmente perdendo pattern combinatoriali complessi che coinvolgono molte variabili con segnali deboli.

3. **Nessun apprendimento adattivo**: le soglie sono congelate e non si adattano a drift del processo o a condizioni operative diverse. Time-LLM e TEST apprendono rappresentazioni che possono catturare nuove modalità.

4. **Template fissi**: il renderer produce testo con struttura fissa, limitando la ricchezza delle descrizioni rispetto a TSLM o Chronicle che possono adattare lo stile e il contenuto al contesto.

5. **Lingua**: il testo è generato in italiano, il che è coerente con il contesto del progetto ma limita la generalizzabilità e l'interoperabilità con LLM prevalentemente addestrati su testo inglese.

---

## 6. Raccomandazioni per il Posizionamento Scientifico

Il verbalizzatore V2 del progetto FoT-TEP dovrebbe essere presentato nella letteratura come un approccio che combina il meglio di due mondi:

1. **Dalla tradizione dell'ingegneria di processo**: rigore statistico, soglie calibrate, feature con semantica esplicita, congelamento formale — approccio radicato nella statistica di processo (SPC) e nel monitoraggio industriale.

2. **Dalla frontiera LLM**: la produzione di testo in linguaggio naturale come interfaccia verso il ragionamento dell'LLM e verso la Federation over Text — approccio che si inserisce nella corrente di ricerca su time-series verbalization.

La **novità principale** è la dimostrazione che un approccio deterministico, completamente trasparente, e statisticamente rigoroso per la verbalizzazione delle serie temporali può servire efficacemente come componente di input per un sistema multi-agente LLM-based, senza richiedere alcun modello appreso nella fase di trasformazione dati→testo.

Questa posizione è complementare, non antagonista, rispetto agli approcci con componenti appresi (Time-LLM, TEST, TSLM). In un'architettura matura, i due approcci potrebbero coesistere: verbalizzazione deterministica per l'evidenza primaria (affidabile, verificabile, congelabile) e modelli generativi per descrizioni contestuali supplementari (ricche, adattive, ma meno verificabili).

---

## 7. Tabella Riassuntiva

| Dimensione | FoT-TEP V2 | LLMTime | PromptCast | Time-LLM | TEST | TSLM | LLM-TSFD |
|---|---|---|---|---|---|---|---|
| Apprendimento | Nessuno | Nessuno | Fine-tuning | Proiezione | Proiezione | Enc+Dec | Nessuno |
| Determinismo | Completo | Dipende da LLM | Parziale | No | No | No | Parziale |
| Multivariata | 41 var. | Mono | Mono | Mono | Mono | Mono | Multi |
| Semantica temp. | Fasi+run+persist. | Nessuna | Timestamp | Patch | Nessuna | Globale | Assente |
| Neutralità | Totale | N/A | N/A | N/A | Implicita | Variabile | Parziale |
| Dominio | Integrato | Assente | Minimo | Prototipi | Prototipi | Appreso | Template |
| Congelamento | SHA-256+protocollo | No | No | No | No | No | No |
| Fed. ready | Progettato | No | Parziale | No | Parziale | Sì | No |
| Feature freq. | No | N/A | N/A | Implicite | Implicite | Implicite | Sì |
| Riproducibilità | Totale | Bassa | Media | Bassa | Bassa | Bassa | Media |
