# Ablation FoT-TEP: Panoramica e Contesto

*Documento companion a `ablation_report.md` — stessa ablation, spiegata in modo discorsivo.*

---

## Cosa fa il nostro esperimento, in parole semplici

Immagina un impianto chimico con 41 sensori che misurano temperature, pressioni, flussi. Quando qualcosa va storto (un guasto), i sensori cambiano comportamento. Il problema è: **come fai a dire a un modello linguistico (tipo ChatGPT) cosa dicono quei sensori?** Il modello capisce il testo, non numeri grezzi di un impianto chimico.

Noi abbiamo testato 4 modi diversi di "tradurre" i dati dei sensori in testo:

- **V2_TEXT:** traduzione in italiano tecnico con giudizi ("il valore è sopra soglia, trend in crescita") — il nostro metodo
- **RAW_FEATURES:** numeri puri in tabella, senza interpretazione
- **CGTIME_STATS:** centinaia di statistiche calcolate per ogni sensore (media, varianza, correlazioni…)
- **SAX_SYMBOLIC:** lettere (tipo "aabccddee") che codificano la forma del segnale

L'idea è semplice: stesse condizioni, stesso modello, stessi casi di test — cambia solo come "parli" all'LLM. Chi funziona meglio?


## Dove ci collochiamo nella letteratura

Il campo dell'uso di LLM per diagnosticare guasti industriali è molto giovane — le prime pubblicazioni serie risalgono al 2024-2025. La maggior parte dei lavori precedenti usa reti neurali tradizionali (CNN, LSTM, trasformatori) addestrate direttamente sui numeri dei sensori, senza passare per il linguaggio naturale. Quei metodi raggiungono accuratezze altissime (95%+) ma richiedono tanti dati di addestramento e non spiegano il ragionamento.

Il nostro contributo si inserisce in un filone che si chiede: **possiamo usare l'intelligenza "generica" di un LLM per diagnosticare guasti senza doverlo addestrare?** La risposta sembra sì, ma la domanda successiva è: quale formato di rappresentazione funziona meglio?

Ed è esattamente la domanda a cui rispondiamo. In letteratura:

- **LLMTime** (Gruver et al., 2023) ha mostrato che gli LLM possono gestire serie temporali serializzate come numeri → noi testiamo qualcosa di simile con RAW_FEATURES
- **CGTime** (Feng et al., 2026) propone un approccio "percezione statistica" → noi ne testiamo una versione adattata
- **SAX/HAR-LLM** (Pappa et al., 2026) usa codifiche simboliche per sensori → noi testiamo SAX
- Nessuno, per quanto ci risulta, **ha fatto un confronto sistematico di queste strategie sullo stesso dataset, stesso LLM, stesse condizioni**

Questo è il nostro punto di forza: siamo probabilmente il **primo confronto controllato head-to-head** di strategie di rappresentazione TS→text per fault diagnosis con LLM.


## Cosa dicono i risultati, e quanto sono forti

Il risultato principale è che i tre metodi migliori (V2_TEXT, RAW_FEATURES, CGTIME_STATS) hanno accuratezze osservate vicine (88.9%, 93.3%, 91.1%), e **nessuna differenza è statisticamente significativa con nessun test**. SAX va peggio (73.3%) ma nemmeno quel divario è confermato statisticamente con test corretti.

Tradotto: con il campione che abbiamo, **non possiamo dire chi vince**. Possiamo dire che il V2 non è chiaramente peggiore nonostante usi 180 volte meno token.

Un dato interessante emerge dalla selective accuracy: RAW_FEATURES e CGTIME_STATS hanno selective_accuracy = 1.000 — cioè quando rispondono, non sbagliano mai. La differenza rispetto al V2 dipende interamente dal fatto che si astengono di più sul guasto F13 (il drift lento, il caso più difficile). Attenzione però: selective accuracy = 1.000 è condizionata alla non-astensione — non sostituisce l'accuratezza complessiva, la copertura o il selective risk.


## Le critiche principali che ci possono fare (e le nostre difese)

### Critica 1: "Il campione è troppo piccolo"

Abbiamo 15 casi indipendenti (3 per classe). Per rilevare una differenza del 10% servirebbe un campione molto più grande. È la critica più forte e più legittima.

**Difesa:** Lo dichiariamo esplicitamente. È un pilot study esplorativo, non un trial confermativo. L'MDE (minimum detectable effect) è ~25 punti percentuali — lo riportiamo. Nessuno dovrebbe aspettarsi conclusioni definitive da 15 casi, e noi non le pretendiamo.

### Critica 2: "Avete testato solo 4 guasti su 28"

Il TEP ha 28 tipi di guasto. Ne abbiamo usati 4 (uno facile, due medi, uno difficile).

**Difesa:** Copriamo le categorie principali (step, stocastico, drift), ma non possiamo generalizzare a tutti i 28. Lo diciamo chiaramente. L'obiettivo era dimostrare il framework di confronto, non esaurire lo spazio dei guasti.

### Critica 3: "V2_TEXT bara perché inietta conoscenza di dominio"

V2_TEXT non è solo un formato diverso: include soglie calcolate statisticamente e descrizioni dei trend. Gli altri arm non hanno questa informazione.

**Difesa:** È vero, ed è un caveat che riportiamo. Il confronto misura "formato + informazione" insieme, non solo il formato. Ma nella pratica, il fatto che V2 raggiunga risultati simili con 180× meno token *includendo* il preprocessing è comunque rilevante operativamente. E il costo del preprocessing è esterno al budget di token del prompt — lo segnaliamo esplicitamente.

### Critica 4: "Un solo LLM"

Tutto è testato con GPT-5.6-terra. Un altro modello potrebbe ribaltare il ranking.

**Difesa:** Corretto. È un limite dichiarato. Ma il contributo metodologico (il framework di confronto) resta valido indipendentemente dal modello specifico.

### Critica 5: "I metodi classici (deep learning) funzionano meglio"

Non abbiamo un baseline di ML tradizionale per confronto.

**Difesa:** Lo scope dell'esperimento è *tra* rappresentazioni per LLM, non LLM vs ML tradizionale. Ma un reviewer potrebbe chiedere un confronto. Se servisse, si potrebbe aggiungere un classificatore Random Forest o LSTM come riferimento.

### Critica 6: "Il test era centralizzato, ma il sistema reale è federato"

La pipeline di produzione FoT usa 4 agenti specialisti (ciascuno guasto vs normale), non un singolo LLM a 5 classi.

**Difesa:** L'ablation isola la variabile "rappresentazione" in condizioni controllate. Centralizzare il task è una scelta di design sperimentale per evitare confounding con l'architettura federata. Validare nel setting federato è un follow-up necessario, ma l'ablation fa il suo lavoro: confrontare le rappresentazioni a parità di tutto il resto.


## Critica A vs Critica B: una distinzione importante

Non tutte le critiche sono uguali. Vale la pena distinguere due famiglie:

### Critica A: "Perché il vostro verbalizer e non un altro metodo di rappresentazione TS→text per LLM?"

Questa è la critica a cui l'ablation **risponde bene**. Un reviewer che conosce LLMTime, CGTime o SAX potrebbe chiederti: "avete inventato il vostro verbalizer V2, ma come fate a sapere che non funzionerebbe meglio dare i numeri grezzi all'LLM, o usare statistiche à la CGTime, o una codifica simbolica?"

L'ablation mostra che V2_TEXT ottiene accuratezza osservata comparabile ai tre approcci alternativi, usando 39–180× meno token. Questo è un argomento forte, anche se non conclusivo: non hai dimostrato equivalenza (il campione è troppo piccolo per quello), ma hai dimostrato che **non c'è evidenza di inferiorità**, e hai un vantaggio pratico enorme in efficienza.

In un paper puoi scrivere qualcosa come:

> *"Per valutare la scelta della strategia di rappresentazione, abbiamo condotto un'ablation su 15 casi TEP indipendenti confrontando V2 con tre approcci dalla letteratura (serializzazione numerica diretta, percezione statistica CGTime-inspired, codifica simbolica SAX). Nessuna differenza statisticamente significativa è emersa tra i primi tre approcci (permutation test, p > 0.25 per tutti i confronti), mentre V2 richiede ~1/39–1/180 dei token in input. Questi risultati preliminari suggeriscono che la rappresentazione V2 offre un compromesso favorevole tra accuratezza diagnostica e costo computazionale."*

Questo è sufficiente per un paper che si presenta come contributo metodologico. Nessun reviewer ragionevole pretenderà una dimostrazione su scala industriale per un'ablation.

### Critica B: "Perché usare un LLM e non un metodo tradizionale di fault diagnosis (Random Forest, CNN, LSTM)?"

Questa è una critica diversa e più fondamentale, e l'ablation **non la copre**. Tutti e quattro gli arm usano un LLM — stai confrontando quattro modi di parlare allo stesso LLM, non stai confrontando l'LLM contro un classificatore tradizionale.

Un reviewer potrebbe dire: "Bella l'ablation, ma un Random Forest addestrato sulle stesse 5 feature V2 probabilmente avrebbe il 98% di accuratezza senza bisogno di un LLM."

Per questa critica, la difesa è diversa e non richiede necessariamente un esperimento aggiuntivo. Puoi argomentare su tre fronti:

1. **Zero-shot:** l'LLM non richiede addestramento su dati etichettati del processo specifico (few-shot, non supervised)
2. **Interpretabilità:** produce un ragionamento leggibile e verificabile, non solo un'etichetta
3. **Generalizzabilità:** il framework FoT è generalizzabile a nuovi impianti senza ri-training

Sono vantaggi architetturali, non di accuratezza pura.

**In pratica:** l'ablation ti protegge dalla Critica A ("perché V2 e non un'altra rappresentazione?") — che è la critica più probabile nel contesto del tuo contributo specifico. Non ti protegge dalla Critica B ("perché un LLM?") — ma quella si difende con argomenti qualitativi (interpretabilità, zero-shot, generalizzabilità) che sono già parte della motivazione del lavoro FoT-TEP, non del risultato dell'ablation.

Se vuoi blindarti anche dalla Critica B con un dato numerico, la cosa più economica sarebbe aggiungere un singolo baseline ML tradizionale (un Random Forest o XGBoost sulle stesse 5 feature V2, addestrato sui 10 esempi di sviluppo) come riga di riferimento nella tabella. Non è indispensabile, ma renderebbe il paper più difficile da attaccare.


## In sintesi: dove siamo

Siamo in una posizione da **buon pilot study esplorativo**. Abbiamo:

- Il **primo confronto sistematico** di rappresentazioni TS→text per fault diagnosis con LLM
- Una **metodologia statistica corretta e robusta** (test cluster-aware, MDE dichiarato, conclusioni calibrate)
- **Risultati interessanti**: il metodo più compatto (V2) funziona altrettanto bene dei metodi più verbosi, con un vantaggio pratico enorme in termini di costi

Le limitazioni (campione piccolo, un solo LLM, 4 fault su 28) sono tutte dichiarate e nessuna è fatale per un paper che si presenti come studio esplorativo piuttosto che come evidenza definitiva.

Il verdetto **GO-with-reservations** della review esterna riflette proprio questo: pubblicabile con le dovute qualificazioni, non come risultato conclusivo.


## Percorso metodologico: dalla review alle correzioni

Vale la pena raccontare anche cosa è successo dopo i primi risultati. Il report originale è stato sottoposto a una review indipendente che ha restituito un verdetto GO-with-reservations con 22 finding (1 critico, 10 major, 7 minor, 2 informativi).

Il **finding critico** riguardava il test di McNemar: l'analisi originale usava N = 45 righe come se fossero indipendenti, ma le 3 ripetizioni per caso sono generate dallo stesso input — non sono indipendenti. Corretto: l'unità indipendente è il `case_id`, e ne abbiamo 15, non 45.

Le correzioni implementate:

1. **Test cluster-aware aggiunti:** permutation test esatto (sign-flip su 15 casi, tutte le 2^15 = 32,768 permutazioni) e McNemar aggregato per caso con majority vote
2. **McNemar row-level declassato** a NON-INFERENTIAL e mantenuto solo come riferimento con warning esplicito
3. **Conclusioni riformulate:** da "indistinguishable" a "not demonstrably different" — una differenza sottile ma importante (il primo implica equivalenza, il secondo riconosce che il campione è troppo piccolo per distinguere)
4. **F13 qualificato per arm:** non più "universalmente il più difficile" ma "il più difficile nella maggior parte degli arm, con pattern arm-dependent"
5. **Analisi aggiuntive:** selective accuracy, coverage, leave-one-class-out
6. **Caveat sull'efficienza V2:** il risparmio di token è reale, ma include preprocessing esterno il cui costo va contabilizzato separatamente

Il risultato delle correzioni ha confermato la previsione della review: con test corretti, **nessun confronto è statisticamente significativo**. La discrepanza tra McNemar row-level (che trovava due confronti significativi) e i test cluster-aware è un caso da manuale di come ignorare la struttura di clustering gonfia artificialmente la significatività.


## Riferimenti ai file

Per chi volesse i dettagli tecnici:

- **`ablation_report.md`** — il report statistico completo con tutte le tabelle, i p-value e le note metodologiche
- **`ablation_evaluation.json`** — i risultati grezzi in formato machine-readable
- **`ablation_evaluate.py`** — lo script di valutazione con tutti i test statistici (bootstrap, permutation, McNemar)
- **`EXPERIMENT_DESIGN.md`** — il protocollo sperimentale pre-registrato
- **`RESULTS_REVIEW_PROMPT.md`** — il prompt usato per la review indipendente
- **`inference_results.jsonl`** — le 180 predizioni grezze del modello

---

*Documento generato come companion discorsivo all'ablation report tecnico.
Ultima revisione: settembre 2026.*
