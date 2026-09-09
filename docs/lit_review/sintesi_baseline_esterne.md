# Baseline esterne al paradigma: sintesi della ricerca bibliografica

## Contesto
Critica analizzata: *"Baseline esterne al paradigma — metodi diagnostici convenzionali come PCA/DPCA, SVM o Random Forest, e tecniche propriamente federate come FedAvg o FedProx. Queste baseline verificherebbero se il paradigma testuale sia competitivo rispetto a quello numerico."*

---

## 1. Esistono lavori che confrontano direttamente approcci testuali/LLM-based con baseline numeriche classiche per fault diagnosis su TS?

**Sì, ma sono pochissimi e con caveat importanti.**

| Paper | Anno | Dataset | Confronta LLM vs classici? | Dettaglio |
|-------|------|---------|---------------------------|-----------|
| **FD-LLM** (Qaid et al.) | 2024 | CWRU bearing | **Sì**: LLMs (Llama3, Qwen, Mistral) vs SVM e 1D-CNN | Primo confronto diretto su vibration data. LLM converte segnali in testo. Task: classificazione supervisionata standard (tutte le classi note) |
| **FaultExplainer** (Khan et al.) | 2024/2025 | TEP | **No**: LLM interpreta output PCA; non è un sostituto ma un layer interpretativo | Ibrido: PCA fa detection, LLM spiega. Nessun confronto LLM-standalone vs PCA |
| **Chen et al.** (IFAC) | 2025 | TEP | **Parziale**: LLaMA3 genera pseudo-labels, poi fuse con classificatore base | "Outperforms traditional methods" ma LLM è ausiliario, non standalone |
| **Lee et al.** | 2025 | HVAC sim. | **No**: solo LLM configs vs rule-based semplice | Giustificazione esplicita: rule-based è "appropriate comparison due to its simplicity" |
| **Liang & Sin** | 2026 | TEP | **No**: LLM coordina CNN-based tools via MCP | LLM come orchestratore, non come classificatore |
| **FD-Zero** (Ran et al.) | 2025 | Bearing | **No**: zero-shot LLM, confronta solo configurazioni interne | Focus su cross-modal alignment, non su battere SVM |
| **Wang et al.** | 2026 | Bearing | **No**: cross-modal alignment LLM-driven | Generalizzazione, non competition con classici |
| **Zhou & Yu** (ICLR) | 2025 | Vari TS | **Parziale**: Isolation Forest come sanity check | Conclusione: "LLMs' abilities to understand and reason about numerical time series are considerably limited" |

**Verdetto**: Un solo paper (FD-LLM) confronta direttamente LLMs vs SVM/CNN, e lo fa su un task *diverso* dal nostro (classificazione supervisionata su classi note, non diagnosi di classi unseen). La stragrande maggioranza dei paper LLM-FDD **non** include baseline numeriche classiche come competitor diretti.

---

## 2. Paper di federated learning applicato a fault diagnosis includono confronti cross-paradigma (testuale vs parametrico)?

**No. I due filoni sono completamente separati.**

- La ricerca nel repository curato [LLM-based-PHM](https://github.com/CHAOZHAO-1/LLM-based-PHM) (>50 paper) non contiene **nessun** paper all'intersezione di "federated learning" + "LLM fault diagnosis."
- Le ricerche su OpenAlex per "federated learning fault diagnosis baseline FedAvg" restituiscono solo survey generici su FL, nessuno che confronti FL parametrico con approcci testuali/linguistici.
- Il gap analysis presente nel nostro doc `FOT_TEP_GAP_ANALYSIS_AND_RELATED_WORK.md` (riga 160) conferma: tutti i paper FL-FDD esistenti scambiano parametri/gradienti; **nessuno** usa trasferimento testuale di conoscenza.
- La catena evolutiva FedAvg → FedMD → FedProto → FedGen → FoT (tracciata nel nostro `FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md`, Parte C) mostra che FoT è il primo a proporre la federazione over text.

**Verdetto**: Non esistono precedenti di confronto cross-paradigma (testuale vs parametrico) in FL-FDD. FoT apre un filone nuovo, il che rende il confronto diretto con FedAvg non solo tecnicamente problematico (task diversi: unseen-class transfer vs classificazione completa) ma anche senza precedenti nella letteratura.

---

## 3. Esiste un precedente accettato in cui un paper propone un nuovo paradigma senza baseline del paradigma precedente?

**Sì, è un pattern ricorrente e accettato nei paper LLM-FDD recenti.**

- **Lee et al. (2025)**: Confronta solo configurazioni LLM + un semplice rule-based. Giustificazione esplicita: *"While this may not represent the most sophisticated baseline, and more advanced statistical or machine learning methods could yield better performance, we consider it a valuable and appropriate comparison due to its simplicity and ease of implementation."*
- **FaultExplainer (Khan et al. 2024/2025)**: Non confronta LLM vs PCA/SVM. Usa PCA *dentro* il sistema come componente, posizionando l'LLM come layer interpretativo complementare.
- **S2S-FDD (arxiv 2603.08048, 2026)**: Signal-to-Semantic framework. Nessun confronto con classificatori numerici. Posizionamento: "conventional diagnosis models typically produce abstract outputs such as anomaly scores or fault categories" — il paper risolve un *problema diverso* (spiegazione e supporto operativo).
- **FD-Zero (Ran et al. 2025)**, **Wang et al. 2026**: Zero-shot LLM fault diagnosis. Confrontano solo varianti interne del proprio framework.

**Pattern comune**: I paper che introducono approcci LLM-based per FDD **non** includono baseline numeriche classiche quando il task che risolvono è intrinsecamente diverso (zero-shot, interpretabilità, unseen classes). L'assenza di baseline cross-paradigma è la norma, non l'eccezione.

---

## 4. Quale framing usano i paper LLM-based per posizionarsi rispetto ai metodi numerici?

Emergono **4 strategie di framing** ricorrenti:

### A) "Complementare, non sostitutivo"
- **FaultExplainer**: LLM *sopra* PCA, non *al posto di* PCA
- **Liang & Sin 2026**: LLM come coordinatore di strumenti CNN-based
- **Aghaee & Shaker (Sensors 2026)**: "LLMs are most credible as interpretive, supervisory, diagnostic layers embedded within hybrid architectures"
- Messaggio: *il paradigma testuale aggiunge valore dove il numerico non arriva (interpretabilità, operabilità), senza pretendere di sostituirlo*

### B) "Task diverso, confronto non applicabile"
- **Lee et al. 2025**: Il task è diagnosi esplorativa via LLM, non classificazione supervisionata → baseline semplice sufficiente
- **S2S-FDD**: Il task è rispondere a "perché" e "come riparare", non classificare → nessun confronto con classificatori
- **FoT (nostro progetto)**: Il task è diagnosi di classi *mai viste localmente*, non classificazione su tutte le classi → FedAvg non risolve lo stesso problema
- Messaggio: *quando il task è qualitativamente diverso, la metrica di confronto non esiste*

### C) "Limitazioni note del numerico come motivazione"
- **Zhou & Yu (ICLR 2025)**: Dimostrano che "LLMs' abilities to understand and reason about numerical time series are considerably limited" → questo *supporta* l'approccio di verbalizzazione (prima converti in testo, poi ragiona)
- **Nie et al. (Sensors 2026)**: Review che traccia l'evoluzione da ML tradizionale a "LLM fusion paradigm" come progresso naturale
- Messaggio: *il nuovo paradigma nasce dai limiti riconosciuti del precedente*

### D) "Confronto diretto ma su task specifico"
- **FD-LLM (Qaid et al. 2024)**: Unico a fare LLM vs SVM/CNN, ma su bearing vibration con classi note
- **Chen et al. (IFAC 2025)**: LLM-augmented vs metodi tradizionali su TEP, ma LLM è ausiliario
- Messaggio: *quando il confronto diretto è fattibile (stesso task, stesse classi), viene fatto*

---

## 5. È un punto critico per la pubblicazione?

### Valutazione: **RISCHIO MODERATO-BASSO** — gestibile con framing corretto

**Fattori che mitigano il rischio:**

1. **Nessun precedente da imitare**: Non esiste letteratura FL + LLM-FDD con confronto cross-paradigma. I reviewer non possono citare un paper che lo fa perché non ce n'è nessuno.

2. **Il pattern è consolidato**: I paper LLM-FDD più recenti e prestigiosi (ICLR 2025, Computers & Chemical Engineering 2025, Control Engineering Practice 2025) non includono baseline numeriche classiche come competitor diretti. Lee et al. lo giustificano esplicitamente.

3. **Task incommensurabile**: FoT risolve un task (diagnosi di classi unseen via trasferimento testuale) che SVM/CNN/FedAvg non affrontano nella stessa formulazione. Confrontare accuracy su task diversi è metodologicamente scorretto. Questo è già documentato nel nostro `FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md` (righe 504-508).

4. **Baseline intra-paradigma presente**: Il confronto Central-ICL (tutte le informazioni testuali a un singolo agente) è la baseline appropriata e già implementata (Condition C / builder_c.py).

5. **Ablation copre le alternative**: Condizioni A (no insight), B (insight corretto), E (insight corrotto) + ablation su rappresentazioni (V2_TEXT, RAW_FEATURES, SAX_SYMBOLIC) mostrano che il contributo del paradigma testuale è robusto.

**Fattori di rischio residuo:**

1. **Reviewer non specializzato**: Un reviewer che conosce FDD classica ma non il filone LLM-FDD potrebbe chiedere "perché non confrontare con CNN/SVM?"
2. **Aspettativa generica di "state of the art"**: Alcuni venue hanno cultura di confronto esaustivo con SOTA.
3. **Confusione tra task**: Se il reviewer non coglie che unseen-class diagnosis ≠ supervised classification, la critica nasce.

### Strategia raccomandata per il paper:

1. **Related Work**: Sezione dedicata che traccia la catena FedAvg → FedMD → FedProto → FoT e spiega perché il confronto è intra-catena, non cross-paradigma. Citare Lee et al. 2025 e FaultExplainer come precedenti di framing.

2. **Limitations**: Paragrafo esplicito: *"We do not benchmark FoT against numerical FDD classifiers (e.g., PCA/DPCA, SVM, CNN) or parameter-based FL methods (FedAvg, FedProx) because these approaches address a fundamentally different task — supervised classification on classes seen during training — whereas FoT targets the transfer of diagnostic capability for locally unseen fault classes through textual knowledge federation. Comparing accuracy across incommensurable task definitions would be methodologically unsound (cf. [FoT lit review, righe 504-508])."*

3. **Discussion**: Posizionare FoT come "complementare" ai metodi numerici (framing A), aprendo a future integrazioni ibride.

4. **Rebuttal-ready**: Se il reviewer chiede, la risposta è pronta: "No prior work in FL-FDD compares textual and parametric paradigms; the closest LLM-FDD papers (Lee et al. 2025, Khan et al. 2025) also do not include classical baselines when the task formulation differs."

---

## Riferimenti chiave trovati

- Khan, A. et al. (2024/2025). *FaultExplainer: Leveraging Large Language Models for Interpretable Fault Detection and Diagnosis.* Computers & Chemical Engineering. DOI: 10.1016/j.compchemeng.2025.109152
- Lee, X.Y. et al. (2025). *Exploring LLM-based Frameworks for Fault Diagnosis.* arXiv:2509.23113
- Zhou, Z. & Yu, R. (2025). *Can LLMs Understand Time Series Anomalies?* ICLR 2025
- Qaid, H. et al. (2024). *FD-LLM: Large Language Model for Fault Diagnosis of Machines.* arXiv:2412.01218
- Ran, G. et al. (2025). *FD-Zero framework: LLM-based diagnosis framework for zero-shot mechanical time-domain signals.* SHM. DOI: 10.1177/14759217251366940
- Wang, J. et al. (2026). *Towards generalizable fault diagnosis via LLM-driven hierarchical cross-modal alignment.* KBS. DOI: 10.1016/j.knosys.2026.115897
- Liang, J. & Sin, G. (2026). *A Large Language Model Enhanced Fault Diagnosis Framework for Chemical Processes.* Systems and Control Transactions. DOI: 10.69997/sct.118894
- Chen, Q. et al. (2025). *Enhanced Fault Diagnosis Using Large Language Models and Probabilistic Label Fusion.* IFAC-PapersOnLine. DOI: 10.1016/j.ifacol.2025.09.401
- Nie, Q. et al. (2026). *A Review of Fault Diagnosis Methods: From Traditional Machine Learning to Large Language Model Fusion Paradigm.* Sensors. DOI: 10.3390/s26020702
- Zhao, S. et al. (2025). *Data-driven fault detection and diagnosis in industrial process systems: A systematic review and perspective.* RESS. DOI: 10.1016/j.ress.2025.112159
