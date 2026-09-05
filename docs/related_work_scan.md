# Related-work scan — Ricerca 1: architetture time-series → testo neutrale

**Obiettivo.** Verificare se esiste in letteratura un'architettura già testata che trasformi serie temporali (multivariate) in testo / linguaggio naturale, migliore o complementare alla Phase A del progetto FoT (pipeline deterministica, senza LLM: finestre → feature con soglie calibrate su Normal → flag → JSON → testo neutrale, faithful-by-construction, frozen, privo di etichette diagnostiche).

**Provenienza dei dati (leggere prima).**
- **Discovery:** Scopus (Elsevier), tre query a imbuto, deduplica per DOI. La chiave universitaria abilita la *ricerca* Scopus (metadati) ma **non** gli abstract né i full-text (`META_ABS`/`FULL` → 401; ScienceDirect → 403). Quindi titoli, venue, anno, citazioni, DOI, open-access = **fattuali da Scopus**.
- **Abstract:** recuperati da **OpenAlex** (aperto) per non inventare le architetture. Dove l'abstract non era disponibile è indicato «abstract non recuperato — da verificare sul full-text».
- **Rilevanza per Phase A e verdetto:** analisi mia, non un dato bibliografico.
- Ricerca eseguita il 2026-09-02. Quota Scopus usata: ~4 chiamate su 20000.

---

## Ranking per rilevanza alla Phase A

### A. Nucleo: generazione di testo *fedele* da serie temporali (il più vicino al tuo obiettivo)

**1. Truth-Conditional Captions for Time Series Data** — Jhamtani & Berg-Kirkpatrick, EMNLP 2021 (OA). DOI: 10.18653/v1/2021.emnlp-main.55 · cit. ~13 (Scopus).
- *Architettura (da abstract):* genera descrizioni in linguaggio naturale dei pattern salienti di una serie (picco, calo). Osserva che i modelli neurali con attention producono output fluenti ma **spesso factualmente errati**, e costruisce un modello orientato alla correttezza fattuale (truth-conditional).
- *Rilevanza:* è l'**unico lavoro il cui obiettivo dichiarato coincide col tuo** — testo *fedele* al segnale, non allucinato. Differenza chiave: loro lo perseguono con un modello appreso; tu lo ottieni **per costruzione** con verbalizer deterministico + soglie, il che è una garanzia più forte e compatibile con la tua disciplina frozen/anti-leakage. È il riferimento naturale di related work per «faithfulness».

**2. T3: Domain-Agnostic Neural Time-series Narration** — Sharma, Brownstein & Ramakrishnan, IEEE ICDM 2021. DOI: 10.1109/ICDM51629.2021.00165.
- *Architettura (da abstract):* serie → **knowledge graph denso** di elementi essenziali → narrazione fluente via PLM (transfer learning). Motivazione esplicita: superare i template «meccanici». +65% di diversità lessicale mantenendo la grammatica; expert review (n=21).
- *Rilevanza:* è l'esatto **opposto filosofico** della tua scelta: loro abbandonano i template per ricchezza; tu tieni i template per fedeltà e determinismo. Utile citarlo per giustificare *perché* nel tuo setting la ricchezza narrativa non è desiderabile (introdurrebbe variabilità e rischio di leakage semantico).

**3. Repr2Seq: A Data-to-Text Generation Model for Time Series** — Li et al., IJCNN 2023. DOI: 10.1109/IJCNN54540.2023.10191421.
- *Architettura (da abstract):* representation learning della serie → vettori → modello neurale che genera la sequenza testuale. Dataset stock+commenti.
- *Rilevanza:* data-to-text *appreso* end-to-end; alternativa neurale al tuo stadio deterministico. Nessuna garanzia di fedeltà esplicita. Comparatore, non miglioria.

**4. Demonstration Selection Strategies for Numerical Time Series Data-to-Text** — Kawarada et al., EMNLP Findings 2024 (OA). DOI: 10.18653/v1/2024.findings-emnlp.435.
- *Architettura (da abstract):* strategie di selezione degli esempi in-context per data-to-text su serie *numeriche*; propone selezione per similarità di sequenza e per conoscenza task-specific. Risultato: **misure scale-invariant (Pearson) battono quelle scale-variant (Euclidea)**.
- *Rilevanza:* riguarda la **Phase B (few-shot)**, non la Phase A. Direttamente utile se vorrai giustificare/ottimizzare come selezioni gli esempi few-shot locali. Da tenere per il capitolo Phase B.

**5. TADACap: Time-series Adaptive Domain-Aware Captioning** — Fons et al., ACM ICAIF 2024 (OA). DOI: 10.1145/3677052.3698690.
- *Architettura (da abstract):* framework **retrieval-based** che genera caption domain-aware per immagini di serie temporali, adattandosi a nuovi domini **senza retraining**; recupera coppie immagine-caption diverse dal dominio target.
- *Rilevanza:* opera su *immagini* di serie (non sui valori) e su captioning ricco; lontano dal tuo testo neutrale fattuale, ma l'idea «adattamento a nuovo dominio senza retraining» è pertinente al tuo passaggio TEP→PV. Citazione di contorno.

**6. CLaSP: Learning Concepts for Time-Series Signals from Natural Language Supervision** — Ito, Dohi & Kawaguchi, EUSIPCO 2025. DOI: 10.23919/EUSIPCO63237.2025.11226094.
- *Architettura (da abstract):* **contrastive learning** (stile CLIP) che mappa segnali temporali ↔ descrizioni in linguaggio naturale; elimina i dizionari di sinonimi predefiniti; retrieval di segnali via query testuale. Usa i dataset TRUCE e SUSHI.
- *Rilevanza:* non genera il tuo testo, ma la **separabilità concetto↔descrizione** è esattamente il pre-requisito del tuo Step 10 (signature vector / separabilità). Ottimo riferimento per argomentare che «il testo neutrale conserva struttura discriminante».

### B. Data-to-text deterministico / linguistico (la tua stessa filosofia: fedele e interpretabile)

**7. Using Fuzzy Sets in a Data-to-Text System for Business Service Intelligence** — Ramos-Soto, Janeiro, Alonso, Bugarín et al., 2017. DOI: 10.1007/978-3-319-66827-7_20. *(abstract non recuperato — da verificare sul full-text)*
- *Cosa è (da titolo/gruppo):* linea consolidata di **data-to-text linguistico con fuzzy sets** (gruppo Bugarín/Ramos-Soto), deterministico e interpretabile.
- *Rilevanza:* prior art diretto sul verbalizer *deterministico*. È il filone in cui collocare metodologicamente la tua Phase A (D2T rule-based fedele), distinto dal filone neurale.

**8. ICA2TEXT: automatic natural language description of air quality time series** — Cascallar-Fuentes et al., CEUR 2022. *(nessun DOI; abstract non recuperato)*
- *Cosa è (da titolo):* sistema D2T/NLG che descrive automaticamente serie di qualità dell'aria — linguistico/deterministico.
- *Rilevanza:* esempio applicativo del D2T deterministico su serie ambientali; affine alla tua verbalizzazione. Contorno.

### C. Simbolico / feature → testo per fault diagnosis (vicino al tuo stadio feature+soglie)

**9. A Novel Feature Extraction Approach for Mechanical Fault Diagnosis Based on ESAX and BoW** — Zhao et al., IEEE TIM 2022. DOI: 10.1109/TIM.2022.3185658 · cit. ~13–15.
- *Architettura (da abstract):* Extremum-SAX converte il segnale in stringhe simboliche (correggendo l'aliasing informativo di SAX classico) → **bag-of-words** conta le «parole di fault» → Laplacian score le ordina → feature vector per la diagnosi.
- *Rilevanza:* **molto affine alla tua Phase A**: discretizzazione simbolica + conteggi (il tuo Step 9 «dalle finestre ai conteggi» è concettualmente vicino). Differenza: produce vettori numerici, non testo neutrale leggibile. Ottimo comparatore per la parte «feature→simboli→conteggi».

**10. Bridging time series and LLMs via symbolic representation for HAR (SAX_HAR-LLM)** — Pappa, Karvelis & Stylios, Expert Systems with Applications 2026 (OA, Elsevier). DOI: 10.1016/j.eswa.2026.133478.
- *Architettura (da abstract):* SAX produce token ordinati **compatibili con l'input di un LLM**; framework dual-stream (simboli + descrittori cinematici) su LLM causale fine-tuned per HAR. Predizioni **pienamente auditabili**: l'attention si allinea ad assi sensoriali fisicamente sensati; performance competitiva a costo modesto in accuratezza.
- *Rilevanza:* dimostra empiricamente che **la rappresentazione simbolica è un'interfaccia interpretabile TS→LLM**; l'enfasi su auditabilità/tracciabilità è allineata al tuo spirito frozen/leakage-safe. Elsevier, quindi leggibile con i tuoi accessi. Buon candidato di «miglioria dell'interfaccia».

**11. HSQP: Plug-and-Play Symbolic-Quantized Framework for Time-Series Tokenization in LLMs** — Abdullahi et al., IEEE Access 2026 (OA). DOI: 10.1109/ACCESS.2026.3674765.
- *Architettura (da abstract):* tokenizzazione gerarchica **simbolica+quantizzata** (patching + ABBA symbolic aggregation + quantizzazione affine) in token duali; modulo plug-and-play con LLM *frozen*; analisi teorica dell'errore di quantizzazione.
- *Rilevanza:* è per il **forecasting**, non per generare testo; ma la nozione di token simbolico-numerico su backbone *frozen* è affine e potrebbe standardizzare come feedi l'evidenza a un reasoner. Miglioria d'interfaccia potenziale, con caveat (obiettivo diverso).

### D. LLM che diagnostica da segnali «testificati» (delimita il tuo Phase A→B, comparatori)

**12. FD-LLM: Large Language Model for Fault Diagnosis of Machines** — Qaid et al., arXiv 2024. DOI: 10.48550/arXiv.2412.01218 (OA). *(NB: omonimo ma DIVERSO dal #13)*
- *Architettura (da abstract):* adatta LLM a input numerici per diagnosi da serie sensoriali, come classificazione multi-classe. Due encoding: **(a)** tokenizzazione string-based del segnale; **(b)** **feature statistiche tempo+frequenza come riassunti** del segnale. Llama3/Llama3-instruct battono DL SOTA in molti casi, con adattabilità cross-condizione e cross-componente.
- *Rilevanza:* l'opzione **(b)** è di fatto un'istanza validata del tuo *seam* Phase A→B (feature statistiche → riassunto testuale → LLM). Comparatore molto pertinente; utile per posizionare il tuo «testo neutrale fedele» rispetto a «riassunto statistico».

**13. FD-LLM: Large language model for fault diagnosis of complex equipment** — Lin et al., Advanced Engineering Informatics 2025 (Elsevier). DOI: 10.1016/j.aei.2025.103208 · cit. ~105 (Scopus). *(abstract non recuperato — leggibile coi tuoi accessi Elsevier)*
- *Cosa è:* LLM per fault diagnosis di equipaggiamenti complessi; altamente citato. Omonimo del #12 ma paper distinto.
- *Rilevanza:* riferimento forte e recente sul filone «LLM per fault diagnosis»; da leggere in full-text per confronto metodologico.

### E. Survey per il panorama (orientamento, non metodo)

**14. Empowering Time Series Analysis with Large Language Models: A Survey** — Jiang et al., IJCAI 2024 · cit. ~25.
**15. Time-Series Large Language Models: A Systematic Review of State-of-the-Art** — Abdullahi et al., IEEE Access 2025 (OA) · cit. ~40.
- *Rilevanza:* mappano il campo TS+LLM (per lo più forecasting/classification). Utili per la sezione «panorama» del related work; la generazione di *testo neutrale fedele* vi è marginale — il che rafforza la tua tesi di nicchia.

---

## Da NON inseguire (fuori scope, chiarimento)

- **Time-LLM** (Jin et al., ICLR 2024, ~494 cit.) e la nutrita famiglia *LLM-per-forecasting* (TF-LLM, Informer-LLM, STL-LLM, Time-LlaMA, ecc.): riprogrammano LLM per **previsione**, non per trasformare serie in testo. Nonostante il nome «TS+LLM» ricorrente, non sono architetture TS→testo e non competono con la tua Phase A.

---

## Verdetto

1. **Il campo è attivo ma bifronte.** Da un lato captioning/narration **neurale** (Truth-Conditional, T3, Repr2Seq, TADACap, TSLM): espressivo ma non fedele-per-costruzione, con rischio di allucinazione. Dall'altro **data-to-text deterministico/linguistico** (Ramos-Soto/fuzzy, ICA2TEXT) e **simbolico** (ESAX-BoW, Pappa SAX-LLM): fedele e interpretabile.

2. **Nessuna architettura domina la tua sul tuo specifico vincolo** = testo neutrale *fedele-per-costruzione*, **senza LLM**, frozen, leakage-safe, privo di etichette. L'unico lavoro con lo stesso «north star» (fedeltà) è **Truth-Conditional Captioning**, ma è appreso; il tuo verbalizer deterministico offre una garanzia più forte proprio dove a te serve.

3. **Migliorie candidate (complementi, non sostituzioni):**
   - *Interfaccia simbolica standardizzata:* ESAX-BoW (#9) e Pappa SAX-LLM (#10) per formalizzare feature→simboli→conteggi con auditabilità (allineato al tuo Step 9). Pappa è Elsevier, leggibile.
   - *Fedeltà formalizzata:* i criteri truth-conditional (#1) e la separabilità concetto↔testo di CLaSP (#6) se un domani vorrai andare oltre i template mantenendo garanzie — CLaSP tocca esattamente il tuo Step 10.
   - *Comparatore diretto del seam Phase A→B:* FD-LLM/Qaid opzione-(b) (#12), feature statistiche → riassunto → LLM.
   - *Solo per Phase B:* selezione delle demo few-shot (#4), con Pearson > Euclidea.

4. **Raccomandazione di posizionamento.** La tua Phase A occupa una **nicchia difendibile e poco battuta**: verbalizzazione *fedele-per-costruzione, LLM-free, frozen*. In related work posiziónati attorno a Truth-Conditional Captioning (fedeltà), alla linea fuzzy/linguistica D2T (determinismo) e al simbolico-per-fault-diagnosis (ESAX-BoW, Pappa), citando FD-LLM/Qaid come comparatore feature→LLM. Non ho trovato un'architettura testata chiaramente superiore da adottare al posto della tua; le migliori opportunità sono di *interfaccia* (tokenizzazione simbolica) e di *inquadramento della fedeltà*, non di sostituzione.

---

*Caveat di verifica.* Le caratterizzazioni architetturali derivano dagli abstract OpenAlex (o, dove indicato, non recuperati). Prima di citare in un paper, verifica i dettagli sul full-text — in particolare per i lavori Elsevier che puoi aprire con i tuoi accessi (#10 ESWA, #13 AEI, TSLM EAAI).
