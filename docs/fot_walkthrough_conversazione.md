# FoT su TEP — Un unico percorso, dal dato alla valutazione

# FoT (Federation over Text) — Un ponte verso i dati PV attraverso TEP

**Step 1 / 17**

## Introduzione

Il dominio di base è quello degli impianti **fotovoltaici (PV) distribuiti**. Ogni sito osserva proprie serie temporali e propri eventi; clima, impianto, guasti, inverter e regime operativo rendono plausibile una conoscenza locale eterogenea, cioè **non-IID**.

L'obiettivo è esplorare una federazione in cui i siti non debbano centralizzare dati grezzi né scambiarsi necessariamente pesi o gradienti di un modello: ciascun nodo sintetizza conoscenza locale in **testo strutturato** e gli altri nodi la usano per ragionare. La ground truth entra soltanto nella valutazione offline; osservazione numerica, comunicazione testuale, insight e decisione restano separati, così che un buon testo non venga confuso con una diagnosi corretta.

L'idea parte dal paradigma del lavoro *Federation over Text: Insight Sharing for Multi-Agent Reasoning* (Yao, Rabbani, Zaheer, Li — [arXiv:2604.16778](https://arxiv.org/abs/2604.16778), repo [github.com/dixiyao/FoT](https://github.com/dixiyao/FoT)): agenti con LLM frozen distillano *reasoning trace* in insight, che vengono aggregati e ridistribuiti come testo, senza gradienti né fine-tuning. In quel lavoro originale il paradigma è applicato a task di reasoning testuale (matematica, QA, coding); qui viene portato su un dominio nuovo, la **diagnosi di guasti su serie temporali**.

Come banco di prova controllato si usa il **Tennessee Eastman Process (TEP)**, un processo chimico simulato con fault noti e ground truth verificabile. I dati provengono dallo snapshot upstream [github.com/mv-per/tennessee-eastman-dataset](https://github.com/mv-per/tennessee-eastman-dataset) (commit pinnato `309b944f`). TEP è un **gate di fattibilità metodologica**: permette di verificare il meccanismo FoT in condizioni note, non è la destinazione applicativa finale, che resta il fotovoltaico.

### 1.2 Lessico operativo e unità di analisi

Nel paradigma FoT, la questione sperimentale non è soltanto se ciascun nodo sappia riconoscere ciò che ha già osservato, ma anche se possa utilizzare la conoscenza testuale prodotta da altri nodi per diagnosticare tipi di guasto assenti dalla propria esperienza locale.

L’esperimento prevede quattro agenti, intesi come astrazioni di nodi diagnostici distribuiti. Ogni agente osserva l’andamento delle variabili misurate del processo, indicate come variabili XMEAS, e deve stabilire quale stato o tipo di guasto spieghi meglio il comportamento osservato. Gli agenti possiedono esperienze locali differenti: ciascuno dispone di conoscenze ricavate dai tipi di guasto osservati localmente.

I tipi di guasto, denominati formalmente *fault classes*, sono F1, F8, F10 e F13. Per ciascun tipo vengono generate *K* realizzazioni simulate, cioè simulazioni indipendenti dello stesso guasto. Il valore di *K* può variare tra gli esperimenti ed è specificato nei passaggi corrispondenti.

Ogni realizzazione simulata viene sottoposta a tutti e quattro gli agenti. L’unità elementare della valutazione è quindi la coppia **agente–realizzazione**. La relazione tra l’esperienza locale dell’agente e il tipo di guasto determina se questa valutazione è **local-seen** oppure **local-unseen**.

Per l’agente che possiede esperienza locale relativa a quel tipo di guasto, la valutazione è **local-seen**. Per gli altri tre agenti, che non hanno osservato localmente quel tipo durante la costruzione della propria conoscenza diagnostica, la valutazione è **local-unseen**, denominata semplicemente *unseen* nei risultati frozen.

Ogni realizzazione produce pertanto una valutazione **local-seen** e tre valutazioni **local-unseen**. Con *K* realizzazioni per ciascuno dei quattro tipi di guasto, si ottengono complessivamente 4 × *K* valutazioni **local-seen** e 12 × *K* valutazioni **local-unseen** per ogni configurazione informativa. I valori concreti di *K* e le dimensioni campionarie risultanti sono riportati nelle sezioni dedicate ai singoli esperimenti.

Le realizzazioni **Normal** rappresentano invece il funzionamento normale del processo, in assenza dei quattro tipi di guasto considerati. Le relative valutazioni vengono mantenute separate da quelle **local-seen** e **local-unseen**.

Nel seguito, un **insight** è una breve unità di conoscenza testuale che sintetizza ciò che un agente ha appreso dalla propria esperienza locale. Gli insight possono essere raccolti e messi a disposizione degli altri agenti come parte del contesto testuale utilizzato durante la diagnosi, senza trasferire i dati grezzi da cui sono stati ricavati.

Le configurazioni informative **A**, **B** ed **E**, indicate formalmente nei protocolli come *conditions*, stabiliscono se gli insight vengono forniti e in quale relazione si trovano con il tipo di guasto da riconoscere:

- **A** costituisce il riferimento senza insight condivisi;
- **B** mette a disposizione insight pertinenti al tipo di guasto da riconoscere;
- **E** funge da controllo della pertinenza dell’informazione: gli insight sono presenti, ma la loro associazione con i tipi di guasto viene deliberatamente alterata secondo la mappatura di controllo stabilita dal protocollo.

Il confronto tra queste configurazioni informative permette di distinguere l’effetto della semplice presenza di testo dall’effetto prodotto da conoscenza pertinente al tipo di guasto.

### 1.3 Obiettivi sperimentali

L’obiettivo principale è verificare se la configurazione informativa **B** migliori, rispetto alla configurazione informativa **A**, la diagnosi delle realizzazioni **local-unseen**. Il confronto primario **B−A** valuta quindi se un agente possa utilizzare conoscenza condivisa per riconoscere un tipo di guasto che non ha incontrato nella propria esperienza locale.

Il confronto **B−E** ha invece funzione di supporto e valuta la pertinenza dell’informazione, indicata formalmente come *specificità semantica*. Esso permette di verificare se l’eventuale beneficio dipenda dalla corretta relazione tra l’**insight** e il tipo di guasto, anziché dalla sola presenza di informazioni testuali. **B−E** non costituisce un secondo confronto primario.

I meccanismi concreti con cui vengono costruite le configurazioni informative **A**, **B** ed **E** — la struttura del prompt, la federazione degli insight e la permutazione di controllo — sono descritti negli Step 15 e 16. Le popolazioni **local-seen**, **Normal** e overall rimangono descrittive e non introducono ulteriori obiettivi confermativi.

### 1.4 Review in sintesi

Una review mirata della letteratura, documentata nella [gap analysis e related work](lit_review/FOT_TEP_GAP_ANALYSIS_AND_RELATED_WORK.md), ha esaminato l’intersezione tra federazione della conoscenza testuale, sistemi multi-agente, esperienze locali disgiunte per tipo di guasto e diagnosi di serie temporali multivariate.

La ricerca ha compreso:

1. **OpenAlex**: otto query eseguite in parallelo e circa 40 risultati ispezionati;
2. **ArXiv**: due articoli recuperati direttamente tramite identificativo durante una precedente fase della review;
3. **Crossref**: una query e cinque risultati, prevalentemente tangenziali rispetto al tema FedMeta-FFD;
4. **DBLP**: interrogazione non completata a causa di un errore HTTP 500 intermittente, documentato nella review;
5. **Scopus**: non interrogato direttamente;
6. **Citation chaining**: esame delle relazioni bibliografiche individuate dalla review preesistente, documentato negli Output 8–9.

Nei limiti delle fonti, delle query e delle procedure consultate, non è stato individuato un lavoro precedente che combini simultaneamente tutti gli elementi centrali di questo progetto: insight testuali derivati dall’esperienza locale, condivisione fra agenti distribuiti con esperienza disgiunta per tipo di guasto e diagnosi di fault su serie temporali multivariate.

La conseguente affermazione di novità viene pertanto formulata in modo qualificato:

> *“To the best of our knowledge, no prior work federates locally-derived textual insights across distributed agents with class-disjoint experience to diagnose faults in multivariate time series.”*

Questa conclusione non implica l’assenza assoluta di lavori non recuperati dalla ricerca. Definisce invece il gap emerso entro il perimetro documentato della review e motiva la domanda sperimentale affrontata dal progetto.

### 1.5 Critiche costruttive e limiti noti

Le critiche che seguono sono dichiarate in anticipo perché derivano direttamente dalle scelte di design del progetto. Riconoscerle non riduce il valore della prova di fattibilità; lo circoscrive.

#### Federazione simulata su un singolo processo

Nel progetto attuale la federazione esiste a livello logico: quattro agenti possiedono esperienze locali diverse e condividono esclusivamente insight testuali. Tuttavia i dati provengono dallo stesso processo simulato TEP; non viene pertanto dimostrata una reale eterogeneità tra impianti fisicamente distinti.

Mancano alcuni aspetti caratteristici di una federazione reale: differenze tra siti, inverter o condizioni ambientali; proprietari e confini dei dati distinti; problemi di comunicazione e disponibilità dei nodi; generalizzazione verso impianti mai osservati.

Questa scelta è deliberata. Il TEP offre una ground truth controllabile — fault noti, istante di iniezione verificato, run replicabili — che il dominio fotovoltaico reale non fornisce nella fase attuale. Il progetto usa dunque il TEP come *gate di fattibilità metodologica* della federazione testuale, non come validazione completa di un sistema federato industriale. In una futura applicazione fotovoltaica, gli agenti dovranno corrispondere a impianti, inverter o stringhe differenti, ciascuno caratterizzato da dati, condizioni operative ed esperienze di guasto proprie. Una validazione multi-sito su dati PV reali costituisce il passaggio necessario per rispondere pienamente a questa critica.

#### Assenza di baseline classiche ed esterne

Le configurazioni informative A, B ed E permettono di verificare internamente se la condivisione di insight pertinenti produca un beneficio e se tale beneficio dipenda dalla pertinenza dell'informazione. Non consentono però di stabilire se FoT sia migliore dei metodi diagnostici esistenti.

Un confronto più completo dovrebbe comprendere almeno due piani di baseline:

1. **Baseline interne al paradigma testuale** — un modello *local-only*, in cui ciascun agente usa l'LLM con la sola esperienza locale senza federazione, e un modello *centralized pooled*, in cui un singolo agente dispone dell'esperienza aggregata di tutti i nodi. Queste baseline verificherebbero se la federazione testuale superi sia l'isolamento sia la centralizzazione dei dati entro lo stesso paradigma.
2. **Baseline esterne al paradigma** — metodi diagnostici convenzionali come PCA/DPCA, SVM o Random Forest, e tecniche propriamente federate come FedAvg o FedProx. Queste baseline verificherebbero se il paradigma testuale sia competitivo rispetto a quello numerico.

L'assenza di queste baseline non invalida l'esperimento: il progetto conserva valore come prova controllata del meccanismo, mostrando che insight testuali pertinenti possono aiutare gli agenti sui tipi di guasto assenti dalla loro esperienza locale. L'assenza limita però qualsiasi affermazione secondo cui FoT sia complessivamente migliore degli approcci diagnostici tradizionali o delle tecniche federate esistenti. I confronti primari A–B–E restano validi entro il loro perimetro: misurano l'effetto incrementale della federazione testuale, non la posizione assoluta di FoT nel panorama diagnostico.

**Step 2 / 17(Ph.A)**

## Dataset

Il **Tennessee Eastman Process** è un impianto chimico simulato. Il suo simulatore fornisce segnali multivariati, fault noti, run replicabili e un istante di attivazione del guasto verificato a **10 h**: è quindi un ottimo banco di prova, con una **ground truth controllabile** che il dominio fotovoltaico reale non offre. La pipeline legge da ogni file `Time` più **41 variabili misurate XMEAS**.

Nel progetto si usano due tipi di dato:

- **Dataset Normal** — un solo file di processo *senza fault*, lungo **500 h**, con **30001 righe** (500 h × 60 = 30000 campioni, più la riga di endpoint a 500 h). Campionamento **1 minuto** (`1/60 h`). L'ultima riga (l'endpoint) viene **esclusa** dai blocchi: 30000 righe si dividono esattamente in 10 blocchi da 50 h, mentre la 30001ª cadrebbe fuori dalla suddivisione uniforme. 41 XMEAS per riga.
- **Dataset di fault** — i quattro fault studiati sono **F1, F8, F10, F13**. Ogni file è un run (batch) da **50 h**, **3001 righe** (50 h × 60 + endpoint), campionamento 1 minuto, 41 XMEAS. Il fault è iniettato a 10 h, quindi le prime 10 h sono processo nominale e le 40 h successive contengono la firma del guasto.

I file di fault contengono anche **12 variabili manipolate XMV** (le grandezze che l'operatore può controllare). Vengono **escluse** dalla rappresentazione: il layer Phase A è stato definito sulle sole XMEAS e congelato così; aggiungere le XMV dopo aver osservato i dati cambierebbe la rappresentazione a valle del freeze. La pipeline conserva quindi soltanto `Time` + 41 XMEAS.

Le 41 variabili misurate XMEAS (nomenclatura standard del processo)

Nel dataset i canali sono identificati come `XMEAS-1 … XMEAS-41`. La loro denominazione fisica standard nel Tennessee Eastman Process è la seguente (misure continue 1–22; composizioni da analizzatore 23–41):

| # | Variabile | # | Variabile |
| --- | --- | --- | --- |
| XMEAS-1 | A Feed (stream 1) | XMEAS-22 | Separator cooling water outlet temp. |
| XMEAS-2 | D Feed (stream 2) | XMEAS-23 | Composition A (reactor feed) |
| XMEAS-3 | E Feed (stream 3) | XMEAS-24 | Composition B (reactor feed) |
| XMEAS-4 | A and C Feed (stream 4) | XMEAS-25 | Composition C (reactor feed) |
| XMEAS-5 | Recycle Flow (stream 8) | XMEAS-26 | Composition D (reactor feed) |
| XMEAS-6 | Reactor Feed Rate (stream 6) | XMEAS-27 | Composition E (reactor feed) |
| XMEAS-7 | Reactor Pressure | XMEAS-28 | Composition F (reactor feed) |
| XMEAS-8 | Reactor Level | XMEAS-29 | Composition A (purge) |
| XMEAS-9 | Reactor Temperature | XMEAS-30 | Composition B (purge) |
| XMEAS-10 | Purge Rate (stream 9) | XMEAS-31 | Composition C (purge) |
| XMEAS-11 | Product Separator Temperature | XMEAS-32 | Composition D (purge) |
| XMEAS-12 | Product Separator Level | XMEAS-33 | Composition E (purge) |
| XMEAS-13 | Product Separator Pressure | XMEAS-34 | Composition F (purge) |
| XMEAS-14 | Product Separator Underflow (stream 10) | XMEAS-35 | Composition G (purge) |
| XMEAS-15 | Stripper Level | XMEAS-36 | Composition H (purge) |
| XMEAS-16 | Stripper Pressure | XMEAS-37 | Composition D (product) |
| XMEAS-17 | Stripper Underflow (stream 11) | XMEAS-38 | Composition E (product) |
| XMEAS-18 | Stripper Temperature | XMEAS-39 | Composition F (product) |
| XMEAS-19 | Stripper Steam Flow | XMEAS-40 | Composition G (product) |
| XMEAS-20 | Compressor Work | XMEAS-41 | Composition H (product) |
| XMEAS-21 | Reactor cooling water outlet temp. |  |  |

Nomenclatura canonica del TEP (Downs & Vogel, 1993). Il repository tratta i canali come `XMEAS-1…41` senza etichette descrittive; questi nomi sono forniti solo come riferimento fisico.

**Step 3 / 17(Ph.A)**

## Analisi e split dei dataset

Il dataset Normal è un file da 500 h, diviso in **10 blocchi da 50 h** (N1…N10); ogni blocco Ni viene ulteriormente suddiviso in **10 finestre da 5 h** (N1-f1, N1-f2, …). Il campionamento è un minuto, cioè `1/60 h`. I file di fault sono quattro: **F1, F8, F10, F13**; ogni run dura 50 h: le prime 10 h precedono l'attivazione e le 40 h successive producono **8 finestre da 5 h**. Una finestra è una porzione descrittiva dello stesso run, non una replica fisica: questa distinzione tornerà cruciale allo Step finale, quando conteremo i casi statisticamente indipendenti.

### Split dei dati e ruoli distinti

| Split | Fault (F1, F8, F10, F13) | Normal | Ruolo |
| --- | --- | --- | --- |
| Development/calibration | batch 1–5 | N1–N5 | costruisce e calibra il metodo |
| Validation | batch 6–7 | N6–N7 | controllo fuori sviluppo, nessun tuning |
| Test split | batch 8–10 | N8–N10 | verifica finale, aperto dopo il freeze |

> ### Struttura temporale e finestratura
>
> Come nasce la finestratura (struttura pre-splitting)
>
> | Oggetto | Intervallo | Suddivisione | N. finestre |
> | --- | --- | --- | --- |
> | Run di fault — pre-fault | 0–10 h | escluso dall'analisi (processo nominale) | — |
> | Run di fault — post-fault | 10–50 h | [10,15) [15,20) … [45,50) | **8** |
> | Blocco Normal completo | 0–50 h | [0,5) [5,10) … [45,50) | **10** |
>
> L'iniezione del fault a 10 h è ciò che rende 8 le finestre del caso con fault (40 h ÷ 5 h), mentre un blocco Normal completo (50 h) ne produce 10. Non è una proprietà universale della serie: dipende dall'intervallo analizzato.
>
> ### Schema splitting
>
> Scenario con fault
>
> | Pre-fault | Iniezione del fault | Post-fault |
> | --- | --- | --- |
> | **0–10 h** Processo nominale, escluso dall'analisi del caso fault. | **10 h** Il fault diventa attivo. | **10–50 h** Intervallo analizzato. |
>
> Finestratura
>
> | Oggetto | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
> | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
> | Caso con fault analisi 10–50 h | 10–15 | 15–20 | 20–25 | 25–30 | 30–35 | 35–40 | 40–45 | 45–50 | — | — |
> | Blocco Normal completo 0–50 h | 0–5 | 5–10 | 10–15 | 15–20 | 20–25 | 25–30 | 30–35 | 35–40 | 40–45 | 45–50 |
>
> **8 finestre da 5 h** per il caso con fault; **10 finestre da 5 h** per il blocco Normal completo.

**Step 4 / 17(Ph.A)Design / development-time**

## La pipeline di Phase A: le sei operazioni

Di seguito le fasi svolte dalla pipeline della fase A del progetto.

| Ordine | Fase | Quando e che cosa produce |
| --- | --- | --- |
| 1 | **Scelta delle feature** | Decisione di design, eseguita una volta. Si caratterizzano i **fault batch 1–5** per decidere *quali* feature usare (shift, slope, residual, diff); qui **non** si calcolano soglie. |
| 2 | **Calibrazione delle soglie** | Eseguita **soltanto sui blocchi Normal N1–N5**, senza mai guardare i fault; produce baseline e soglie. I fault influenzano *quali* feature, non il *valore* delle soglie. |
| 3 | **Freeze** | Congela feature, baseline, soglie, struttura e renderer. Avviene dopo la calibrazione; da qui in avanti le regole si applicano soltanto, non si ridefiniscono. |
| 4 | **Calcolo delle feature e applicazione delle soglie** | A runtime, per ogni finestra × XMEAS, calcola i **valori delle feature** e li confronta con le soglie già congelate (flag 0/1). |
| 5 | **Dalle finestre al JSON** | Aggrega flag e struttura temporale in evidenza numerica auditabile. |
| 6 | **Dal JSON al testo neutrale** | Renderizza fatti quantitativi senza fault ID o diagnosi automatica. |

**Step 5 / 17(Ph.A)Design / development-time**

## Scelta delle feature

La **scelta** delle feature è una decisione di design sul development/calibration. Il **calcolo** delle feature è invece l'operazione ripetuta su ogni finestra. Confondere i due momenti farebbe sembrare che il metodo venga reinventato per ciascun fault.

> Elenco delle feature
>
> | Feature | Quantifica | Non prova da sola |
> | --- | --- | --- |
> | `shift_sigma` | Spostamento della media in σ Normal | La causa |
> | `slope_sigma_h` | Pendenza normalizzata per ora | Drift persistente |
> | `residual_std_ratio` | Variabilità dopo detrend | Periodicità |
> | `diff_std_ratio` | Variazioni campione-campione | Oscillazioni lente |
> | `raw_std_ratio` | Dispersione descrittiva | Instabilità oscillatoria |

**Step 6 / 17(Ph.A)Design / development-time**

## Calibrazione delle soglie

In questa fase di **calibrazione** vengono calcolate le soglie che saranno utilizzate nelle fasi successive per valutare le evidenze dei casi di fault. È importante sottolineare che la calibrazione usa esclusivamente i blocchi **N1–N5 Normal** della fase development/calibration e non utilizza i fault. N1–N5 forniscono 5 blocchi × 10 finestre = 50 finestre. Per ciascuna finestra e feature si calcolano le 41 XMEAS e si prende il massimo di sistema; i 50 massimi vengono ordinati e la soglia è il valore al **rango 49**, cioè il 49º elemento ordinato, con attivazione stretta `>`. Come esempio, `shift_sigma` viene calcolata così:

```
shift_sigma = (x̄_w − μ₀) / σ₀
```

- `x̄_w`: media della stessa XMEAS nella finestra corrente;
- `μ₀`: media della baseline Normal N1–N5 per quella XMEAS;
- `σ₀`: deviazione standard campionaria della baseline Normal N1–N5 per quella XMEAS.

Il confronto con la soglia usa il modulo: `|shift_sigma| > soglia`; il segno resta disponibile nell'evidenza strutturata.

> **Perché prendiamo il massimo?** Prima del confronto, lo score di ogni XMEAS è espresso rispetto al comportamento Normal di quella stessa variabile: per `shift_sigma`, per esempio, lo spostamento è misurato in deviazioni standard Normal. Gli score sono quindi adimensionali e confrontabili: non stiamo mettendo a confronto pressioni, temperature o portate nelle loro unità fisiche. Il massimo identifica, dentro quella finestra, *la deviazione standardizzata più estrema* tra i 41 canali e risponde alla domanda di sistema «almeno una variabile si è allontanata dal proprio normale più del previsto?». Non identifica la causa del cambiamento e non rende anomale le altre variabili; comprime la finestra in un solo score conservando il canale più distante dal suo riferimento. Calibrare la soglia sui massimi Normal, anziché su score individuali, incorpora inoltre nel riferimento il fatto che in ogni finestra cerchiamo l'estremo fra 41 opportunità.

Il **leave-one-block-out** nasce qui: quando si misura N1, il riferimento usa N2+N3+N4+N5. Si ripete ciclicamente fino a N5.

> Esempio reale
>
> ### Dalle 50 finestre alla soglia shift
>
> N1–N5 → → → 50 finestre → → → max |shift| su 41 canali → → → sort → → → rango 49
>
> Coda reale degli score `max_abs_shift`
>
> | Rango | Score | Finestra | Esito |
> | --- | --- | --- | --- |
> | 47 | 1.2688185320140528 | N3 [135,140) | sotto |
> | 48 | 1.5988379030092623 | N2 [85,90) | sotto |
> | **49** | **1.9695333234149084** | N4 [190,195) | **soglia** |
> | 50 | 2.0050511992352518 | N2 [95,100) | unico `>` soglia |
>
> Mostriamo solo la coda, ma ogni score è davvero il massimo sui 41 canali.

**Step 7 / 17(Ph.A)Design / development-time**

## Il freeze: congelare feature, soglie e renderer

Prima di aprire validation, test e held-out vengono congelati feature, soglie, rappresentazione temporale, renderer ed evaluator. È il principio *freeze-before-test*: nessun dato di valutazione può più influenzare le regole con cui verrà giudicato. In questo modo si evita il **leakage** — cioè che osservare i risultati porti, anche inconsapevolmente, a riscrivere feature o soglie per farle combaciare con i casi da valutare. Da qui in avanti quelle regole si possono soltanto applicare, non ridefinire.

> **Che cosa è stato usato fino a qui.** Fino al freeze sono entrati in gioco soltanto i blocchi **Normal N1–N5** (per calibrare le soglie) e i **fault batch 1–5**. Questi ultimi sono stati usati **solo in fase di design/development, per scegliere *quali* feature usare** — non per calcolare le soglie e non a runtime. La scelta delle feature è una decisione fatta una volta, a monte, non un'operazione ripetuta su ogni caso. I restanti dati — **N6–N10** e i **fault batch 6–10** — **non sono ancora stati toccati**: entreranno solo dopo il freeze, in validation e test. (N1–N5 servono in due momenti: a design-time per calibrare le soglie e poi come baseline di riferimento anche a runtime.)

**Step 8 / 17(Ph.A)Runtime / finestra × XMEAS**

## Dalle feature ai flag: soglie e segni

Per ogni finestra (le **8** del caso con fault) e per ogni variabile **XMEAS** (le **41**) vengono applicate le soglie: se il valore della feature è maggiore della soglia — ricordiamo che la soglia è stata calibrata sui **Normal** — viene generato un **flag** (attivo/non attivo) e, per le feature con segno (shift, slope), il relativo **segno**. Vediamo il calcolo reale su una singola finestra: F1 batch 1, XMEAS-1, W1. (Caso development/calibration, non test indipendente; non usa LOBO. W1 è `[10,15)` h: 5 h × 60 = 300 misure.)

> Worked example reale · raw → feature → flag
>
> ### Il calcolo completo
>
> Ricordiamo la feature che stiamo calcolando (la stessa dello Step 6):
>
> ```
> shift_sigma = (x̄_w − μ₀) / σ₀
> ```
>
> dove **x̄_w** è la media della finestra, **μ₀** la media del riferimento Normal e **σ₀** la sua deviazione standard. Prima dei numeri, due chiarimenti sui termini che compaiono qui sotto: la *«anteprima raw»* sono le misure grezze di XMEAS-1 campionate ogni minuto dentro la finestra W1 (300 valori: 5 h × 60), di cui mostriamo solo i primi cinque e gli ultimi tre; la *«media W1»* è proprio x̄_w, la media aritmetica di quei 300 valori, cioè il numeratore che entra nella formula.
>
> 1. **Anteprima raw.**  
>    `0.266206, 0.264258, 0.265880, 0.268725, 0.267920, …, 1.018145, 1.017490, 1.018571`  
>    La media usa tutti i **300** valori, non solo gli otto mostrati.
> 2. **Media W1.**  
>    `Σxᵢ = 216.7053282371516`  
>    `window_mean = 0.7223510941238387`
> 3. **Riferimento pooled N1–N5.** **15000** misure XMEAS-1 in `[0,250)` h.  
>    `μ₀ = 0.26679593084899306`  
>    `σ₀ = 0.005941491332146645`, std campionaria `ddof=1`.
> 4. **Sostituzione.**  
>    `shift_sigma = (0.7223510941238387 − 0.26679593084899306)  
>     / 0.005941491332146645  
>     = 76.67353831016274`
> 5. **Confronto.** `|76.67353831016274| > 1.9695333234149084` → **level flag = 1**, segno positivo conservato.
>
> Provenienza e precisione
>
> W1: `mode1_1_1.xlsx`, righe Excel 602–901, XMEAS-1. Baseline: `mode1_normal_500.xlsx`, righe 2–15001 della colonna ricondotta a XMEAS-1. Il ricalcolo read-only coincide con il CSV entro l'ultima unità floating-point; qui è riportata la precisione frozen del CSV.

**Step 9 / 17(Ph.A)Runtime / caso completo**

## Dai flag al JSON, fino al testo neutrale

La griglia di flag (8 finestre × 41 XMEAS) viene utilizzata per generare un **JSON strutturato**, che il renderer trasforma in una **descrizione neutrale**. Si sottolinea che nel testo prodotto non sono presenti ID di fault, nessuna etichetta di classe, nessuna diagnosi: è presente solo un testo descrittivo dei fatti osservati, mai un'interpretazione o una diagnosi.

> Esempio reale · F1 batch 1, XMEAS-1
>
> ### 1 · I flag per finestra (feature `level`, 1 = attivo)
>
> | Finestra | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
> | --- | --- | --- | --- | --- | --- | --- | --- | --- |
> | flag level | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
> | segno | + | + | + | + | + | + | + | + |
>
> ### 2 · Evidenza numerica strutturata (JSON, estratto reale)
>
> ```
> {
>   "variable": "XMEAS-1",
>   "window_size_h": 5,
>   "level": {
>     "n_active_windows": 8, "active_fraction": 1.0,
>     "positive_count": 8, "negative_count": 0,
>     "sign_consistency": 1.0, "longest_same_sign_run": 8,
>     "first_active_window": 10.0, "last_active_window": 45.0,
>     "early_active": true, "late_active": true
>   }
> }
> ```
>
> ### 3 · Firma (temporal summary)
>
> - `n_active_windows = 8` — numero di finestre con flag = 1.
> - `positive_count = 8` — finestre attive con segno positivo (qui tutte).
> - `late_active = true` — presenza di attivazioni nelle ultime finestre (fase tardiva).
> - `longest_same_sign_run = 8` — lunghezza massima di finestre attive consecutive con lo stesso segno.
>
> ### 4 · Testo neutrale reale (EXM-001)
>
> > Intervallo osservato 10.0–50.0 h in 8 finestre da 5.0 h. XMEAS-1 supera la soglia di spostamento in 8/8 finestre, sempre con segno positivo; il run più lungo con segno coerente comprende 8 finestre, dalla prima attivazione a 10.0 h all'ultima a 45.0 h. XMEAS-1 supera la soglia di pendenza in 6/8 finestre, con segno positivo in 3 e negativo in 3; il run più lungo con segno coerente comprende 1 finestra, dalla prima attivazione a 10.0 h all'ultima a 35.0 h. XMEAS-20: variabilità residua dopo rimozione del trend lineare sopra soglia in 4/8 finestre; 2/2 nella fase iniziale e 0/2 nelle ultime finestre. XMEAS-10: variazioni campione-campione sopra soglia in 1/8 finestre; 1/2 nella fase iniziale e 0/2 nelle ultime finestre. Su XMEAS-10, residual e diff superano simultaneamente le rispettive soglie in 1/8 finestre, incluse 0/2 finestre finali. La massima dispersione complessiva osservata è su XMEAS-1 (rapporto tra deviazioni standard 46.30).
>
> L'estratto JSON mostra la parte `level` di XMEAS-1. Il testo completo nasce dal JSON completo a 41 canali, quindi cita altri canali quando dominano altre sezioni (qui XMEAS-20 e XMEAS-10). Non contiene F1, batch, pseudolabel o soglie: nessuna diagnosi, solo fatti.

**Step 10 / 17(Ph.A)Controllo offline**

## Evaluator · signature vector

Solo ora entra l'evaluator, con uno scopo preciso: verificare offline se la rappresentazione neutrale conserva una struttura sufficientemente stabile e separabile prima che i testi vengano affidati a un reasoner. Lavora sul JSON e misura stabilità intra-classe e separabilità inter-classe. Una firma contiene 17 componenti normalizzate per XMEAS: 41 × 17 = 697 valori; la similarità è `1 − mean(abs(a−b))`. L'evaluator può quindi chiedere se due run F1 presentano pattern temporali simili o se un run F1 è più vicino agli altri F1 che ai Normal. Non produce una predicted label e non misura accuracy: valuta la qualità descrittiva della rappresentazione. **La separabilità descrittiva non equivale all'accuratezza diagnostica**, perché una firma separabile non garantisce che un reasoner la utilizzi correttamente.

> Mini-esempio · a cosa serve la firma
>
> ### Confrontare due firme
>
> Le firme reali hanno 697 componenti (41 XMEAS × 17): impossibili da leggere a occhio. Qui riduciamo a **4 componenti schematiche** — valori inventati, solo per illustrare la meccanica — dove ogni componente è una statistica normalizzata in `[0,1]` estratta dal JSON (per es. frazione di finestre attive, coerenza di segno, run più lungo, precocità dell'attivazione).
>
> | Firma | c₁ | c₂ | c₃ | c₄ |
> | --- | --- | --- | --- | --- |
> | F1 · run A | 1.00 | 1.00 | 0.90 | 0.20 |
> | F1 · run B | 1.00 | 0.95 | 0.85 | 0.25 |
> | Normal · run C | 0.10 | 0.00 | 0.05 | 0.90 |
>
> ### Similarità = `1 − mean(abs(a−b))`
>
> **Intra-classe** (F1·A vs F1·B): differenze assolute `|0.00|, |0.05|, |0.05|, |0.05|` → media `0.0375` → similarità **0.9625**. Due run dello stesso fault hanno firme quasi coincidenti: la rappresentazione è **stabile**.
>
> **Inter-classe** (F1·A vs Normal·C): differenze `|0.90|, |1.00|, |0.85|, |0.70|` → media `0.8625` → similarità **0.1375**. Fault e Normal sono lontani: la rappresentazione è **separabile**.
>
> > **A cosa serve.** Alta similarità intra-classe + bassa similarità inter-classe = il testo neutrale di Phase A conserva abbastanza struttura da distinguere le condizioni *senza mai nominarle*. È il pre-requisito descrittivo che rende sensato, nello step successivo, dare quei testi in pasto a un reasoner in Phase B — ma resta separabilità, non ancora accuracy diagnostica.

**Step 11 / 17(Ph.A)Valutazione out-of-development/calibration**

## Validation e test split: applicare dopo il freeze

La progettazione si è terminata con il freeze; adesso si esegue la stessa pipeline runtime prima sulla validation (fault batch 6–7 e Normal N6–N7) e poi sul test split (batch 8–10 e N8–N10). In entrambi i casi il percorso è sempre `finestre → feature → soglie congelate → JSON → testo neutrale → evaluator`. È importante notare come lo split «development/calibration» sia utilizzato per progettare e calibrare, in seguito al freeze la validation è utilizzata per effettuare controlli intermedi e alla fine il test split resta chiuso fino alla verifica finale di Phase A.

**Step 12 / 17(Ph.A)Confine sperimentale**

## Nuove simulazioni indipendenti

I batch 8–10 del test split erano test di Phase A, ma sono stati aperti. Un test osservato non è più vergine per Phase B. La catena è: test split visto → non può essere nuovo test indipendente → servono run nuovi → vanno congelati prima di verbalizzazione e inference. Un test indipendente e congelato prima dell'inferenza serve proprio a questo: impedisce il leakage da riuso di uno split già osservato e offre una misura non distorta della generalizzazione, senza che il test possa ricalibrare soglie o insight (nessun overfitting al set di valutazione). Questi 15 run congelati sono il materiale su cui si aprirà **Phase B** (dal prossimo step): fin qui — Step 4–12 — siamo rimasti dentro Phase A.

15 nuove realizzazioni simulate = 3 Normali + 3 run per ciascun fault

| Normal | F1 | F8 | F10 | F13 |
| --- | --- | --- | --- | --- |
| 3 run | 3 run | 3 run | 3 run | 3 run |

**Step 13 / 17(Ph.B)Phase B / conoscenza locale**

## Agenti non-IID, pseudolabel ed esempi locali

> **Inizia Phase B.** Finora (Step 4–12) siamo rimasti in Phase A: pipeline deterministica, soglie calibrate e congelate, nessun LLM. Da qui entrano in gioco gli agenti, il reasoner e la federazione. La pipeline Phase A non viene ri-progettata: gli agenti la *riusano* così com'è, applicando baseline e soglie congelate senza mai ricalibrarle.

Quattro agenti conoscono tutti il Normal ma ciascuno un solo fault. Ogni agente riceve due esempi del proprio fault (batch 1–2) e gli stessi due Normal (N1–N2).

Distribuzione non-IID: ogni agente conosce solo il proprio fault

| Agente A | Agente B | Agente C | Agente D |
| --- | --- | --- | --- |
| 2 Normali + 2 esempi da F1 | 2 Normali + 2 esempi da F8 | 2 Normali + 2 esempi da F10 | 2 Normali + 2 esempi da F13 |

> **Da dove vengono i dati.** Attenzione a non confondere tre cose distinte: gli **esempi** del few-shot sono batch 1–2 di fault e Normal N1–N2 dal **TEP originale** (gli stessi workbook di Phase A), non i run indipendenti; il **caso da diagnosticare** sarà invece un run del **held-out indipendente** — i 15 PBH dello Step 12 — e comparirà solo all'inferenza (Step 16); le **soglie** restano quelle calibrate in Phase A sul TEP originale (Normal N1–N5), congelate e mai ricalcolate.

> Prima operazione di Phase B · il few-shot locale
>
> ### Ogni agente costruisce i propri esempi few-shot
>
> La prima cosa che fa ogni agente è preparare il proprio **few-shot locale**: prende i casi che conosce (i suoi batch 1–2 di fault e i Normal N1–N2), li fa passare per la pipeline Phase A già congelata e ne ricava esempi pronti da mostrare al reasoner. Non è materiale che «compare» già pronto: viene ricostruito dai workbook, senza LLM e senza ricalibrare nulla. Il ramo few-shot usa batch 1–2; il ramo insight dello step successivo riparte separatamente dai batch 1–5.
>
> | Passaggio | Che cosa accade realmente |
> | --- | --- |
> | **Input dei casi** | Per ciascun agente: i workbook fissi batch 1–2 del proprio fault locale e i blocchi Normal N1–N2. La baseline development/calibration N1–N5 resta il riferimento frozen. |
> | **Operazione** | Con questi input, l'agente riesegue la pipeline Phase A congelata (`finestre → feature → soglie già congelate → flag → JSON → testo neutrale`) e associa a ogni caso la sua **pseudolabel** — un'etichetta opaca che nasconde il nome reale del fault (spiegata in dettaglio qui sotto). Nessun LLM, nessuna ricalibrazione delle soglie. |
> | **Output** | 4 pack × 4 esempi, ciascuno ridotto alla coppia `(testo neutrale, pseudolabel)`. |

> ### Che cosa significa pseudolabel e che cosa vede l'LLM
>
> Una **pseudolabel** sostituisce nel materiale prompt-facing il nome reale del fault con un token opaco `CLS-…`: F1, F8, F10 e F13 non vengono mostrati all'LLM, mentre `Normal` resta `Normal`. Il mapping reale↔opaco è noto **soltanto all'evaluator**. La pseudonimizzazione maschera il nome del fault, non la sua firma descritta nel testo.
>
> ### Com'è composto il prompt few-shot dell'agente
>
> | Testo neutrale dell'held-out (caso da diagnosticare) | + Esempi locali few-shot (dello stesso agente) | + Spazio delle etichette (Normal + i fault, come token opachi) |
> | --- | --- | --- |
> | Il testo di un nuovo caso, senza etichetta. | Le coppie `(testo neutrale, pseudolabel)` costruite sopra. | L'insieme delle scelte possibili: `Normal` e le pseudolabel `CLS-…`, non i nomi reali F1/F8/F10/F13. |
>
> Lo schema mostra i tre ingredienti a livello concettuale. Sul lato prompt-facing i fault restano token opachi `CLS-…`; i nomi F1/F8/F10/F13 sono noti solo all'evaluator.
>
> Un esempio **few-shot locale** è la coppia `(neutral text, pseudolabel)`: non contiene il JSON numerico e non contiene il workbook.
>
> > **Few-shot reale EXM-001 · F1 batch 1, identità offline.**
> > > Intervallo osservato 10.0–50.0 h in 8 finestre da 5.0 h. XMEAS-1 supera la soglia di spostamento in 8/8 finestre, sempre con segno positivo; il run più lungo con segno coerente comprende 8 finestre, dalla prima attivazione a 10.0 h all'ultima a 45.0 h. XMEAS-1 supera la soglia di pendenza in 6/8 finestre, con segno positivo in 3 e negativo in 3; il run più lungo con segno coerente comprende 1 finestra, dalla prima attivazione a 10.0 h all'ultima a 35.0 h. XMEAS-20: variabilità residua dopo rimozione del trend lineare sopra soglia in 4/8 finestre; 2/2 nella fase iniziale e 0/2 nelle ultime finestre. XMEAS-10: variazioni campione-campione sopra soglia in 1/8 finestre; 1/2 nella fase iniziale e 0/2 nelle ultime finestre. Su XMEAS-10, residual e diff superano simultaneamente le rispettive soglie in 1/8 finestre, incluse 0/2 finestre finali. La massima dispersione complessiva osservata è su XMEAS-1 (rapporto tra deviazioni standard 46.30).
> >
> > **Etichetta mostrata all'LLM:** `CLS-ZOGAA`. La coppia è testo + etichetta; F1 e batch 1 restano provenance evaluator-side.

**Step 14 / 17(Ph.B)Phase B / federazione**

## Gli insight distillano più casi; la federazione li distribuisce peer-only

Dopo il few-shot, ogni agente compie una seconda operazione: condensa ciò che sa del proprio fault in due brevi osservazioni testuali, gli **insight**. Per farlo riparte dai cinque casi development/calibration del fault locale (batch 1–5, dati TEP originali già usati in Phase A), li fa passare per la stessa pipeline congelata ottenendone i testi neutrali e chiede all'LLM di distillarne le regolarità ricorrenti: **2 insight per agente, 8 in totale**. Questo è un ramo distinto dal few-shot dello Step 13: non usa come input il file degli esempi locali. Tutto avviene **prima di aprire diagnosticamente** i 15 run indipendenti dello Step 12, già generati e congelati: gli insight nascono soltanto da ciò che l'agente conosceva già. Infine avviene la **federazione**: ogni agente riceve i sei insight degli altri tre peer — mai i propri — così la conoscenza circola come testo, senza scambiare dati grezzi né parametri del modello.

> Ramo insight separato · input → operazione → output
>
> ### Cinque run vengono riverbalizzati prima della distillazione LLM
>
> | Passaggio | Che cosa accade realmente |
> | --- | --- |
> | **Input** | Un bundle distinto per agente, `phase_b/insights/input_bundles/agent_N.json`, con 5 testi neutrali del fault locale. I testi sono ricostruiti direttamente dai workbook development/calibration batch 1–5 tramite `verbalize_case` e la pipeline frozen; non provengono dal file few-shot. |
> | **Operazione** | Dopo la ri-esecuzione deterministica `finestre → feature → soglie congelate → flag → JSON → testo neutrale`, il bundle viene passato a `gpt-5.6-terra`, reasoning `medium`. Vale *first structurally valid output wins*; nell'esecuzione frozen ogni agente ha richiesto 1 attempt e 0 retry. Nessuna soglia viene ricalibrata. |
> | **Output** | 2 insight strutturati per agente, quindi 8 totali in `final_local_insights.json`. |

| Parametro | Valore |
| --- | --- |
| Modello | gpt-5.6-terra, reasoning effortmedium, Structured Outputs strict. |
| Regola | First structurally valid output wins: viene accettata la prima risposta che passa lo schema, senza selezione o rigenerazione basata sul contenuto. |
| Esito reale | Per tutti e quattro gli agenti: 1 attempt, 0 retry, 2 insight accettati. |

> Esempio: F1 diventa conoscenza trasferibile
>
> ### Da Agent 1 a un peer che non conosce F1
>
> ```
> INS-001 · agent_1 · CLS-ZOGAA
> "XMEAS-1 exceeds the displacement threshold positively in all 8/8 windows,
>  with one coherent 8-window run from 10.0 to 45.0 h; it also has the largest
>  overall dispersion (standard-deviation ratio 46.06–46.50)."
> ```
>
> Il range deriva da cinque run development/calibration, non da uno. Agent 3 riceve INS-001 e INS-002 da Agent 1 più quattro insight dagli altri peer, ma non i propri F10.
>
> > **8 generati, 6 ricevuti.** La libreria globale ha otto insight; ciascuna peer library ne ha sei.

**Step 15 / 17(Ph.B)Phase B / protocollo frozen**

## Configurazioni informative controllate e struttura completa dell'inference

Una **configurazione informativa** è una versione controllata dello stesso agent-case: neutral text held-out e few-shot locali restano identici, mentre cambia una sola variabile sperimentale, il blocco degli insight peer. In questo modo la differenza tra configurazioni informative non può essere attribuita a un workbook diverso o a esempi locali diversi.

> Disegno A/B/E frozen
>
> ### Che cosa cambia davvero
>
> | Configurazione informativa | Input oltre ai few-shot locali | Domanda controllata |
> | --- | --- | --- |
> | **A — isolated** | Nessun insight peer: solo conoscenza locale. | Che cosa fa l'agente senza federazione? |
> | **B — FoT** | 6 insight peer genuini, con pseudolabel corrette. | Che cosa aggiunge la conoscenza peer corretta? |
> | **E — corrupted** | Gli stessi 6 insight di B: stessi ID, fonti, testi, ordine e volume; cambiano soltanto le pseudolabel, permutate. | Il beneficio dipende dall'associazione corretta o dalla sola presenza di più testo? |
>
> > **Perché E è cruciale.** La permutazione è un *derangement* specifico per agente con zero punti fissi: nessuna pseudolabel resta associata alla classe originale. Per Agent 3, per esempio, `CLS-ZOGAA → CLS-OJNSG`. E isola quindi la correttezza dell'informazione dal volume e dalla forma del peer block.
>
> ### Dal disegno alle richieste
>
> 15 casi held-out → × → 4 agenti → × → 3 configurazioni informative → × → R=3 → = → 540 richieste
>
> Per ogni agent-case–configurazione informativa, **R=3** significa tre chiamate con input identico. Una pseudolabel con almeno 2 voti diventa la prediction aggregata; senza maggioranza valida l'agente astiene, e l'astensione conta come errore nel protocollo. Le ripetizioni stabilizzano il non-determinismo dell'LLM: **non sono tre esperimenti fisici**.
>
> Le 540 risposte diventano 180 esiti aggregati; tutte le predizioni vengono congelate **prima** di unirle alla ground truth. L'analisi del trasferimento (Step 17) si concentrerà poi soltanto sui casi in cui il fault è *unseen* per l'agente — 36 agent-case per configurazione informativa.

**Step 16 / 17(Ph.B)Phase B / inference frozen**

## Dal testo neutrale alla decisione: PBH-004 visto da Agent 3

Finora abbiamo definito le tre configurazioni informative. Vediamo ora che cosa accade realmente allo stesso caso quando attraversa A, B ed E. PBH-004 è un nuovo run held-out di F1 (`mode1_1_11.xlsx`), ma questa identità è conosciuta soltanto dall'evaluator. La pipeline congelata trasforma il workbook nel suo testo neutrale; quel testo viene poi presentato ad Agent 3, che possiede esempi locali di F10 e per il quale F1 è quindi una classe *unseen*. Il caso, i few-shot, il modello e il prompt restano gli stessi: cambia soltanto il blocco degli insight peer.

Il testo neutrale di PBH-004 segnala XMEAS-1 sopra la soglia di spostamento in 8/8 finestre, sempre positivo, con dispersione massima 47.00: la firma di F1, osservata però su un run mai visto.

PBH-004 → → → pipeline Phase A congelata → → → testo neutrale → → → Agent 3 → → → A / B / E → → → tre esiti aggregati → → → ground truth ancora chiusa

> Agent 3 × PBH-004 · record frozen
>
> ### La sola manipolazione A/B/E
>
> | Configurazione informativa | Peer block | R=3 | Aggregato |
> | --- | --- | --- | --- |
> | **A** | Nessun insight | `null ×3` | astensione, incorrect |
> | **B** | 6 insight genuini; INS-001 associa F1 a CLS-ZOGAA | `CLS-ZOGAA ×3` | corretta |
> | **E** | Stessi testi/ordine; INS-001 associa F1 a CLS-OJNSG | `CLS-OJNSG ×3` | errata |
>
> I record hanno `used_insight_ids=[]`: non attribuiamo la singola risposta a INS-001. Confrontiamo correttamente le configurazioni informative frozen nel loro insieme.

**Step 17 / 17(Ph.B)Ground-truth evaluation**

## Risultati Phase B: trasferimento di conoscenza sui fault localmente unseen

Lo step conclusivo è la valutazione dell'intero esperimento. Ricordiamoci che TEP non è il dominio target, ma possiamo definirlo come il banco di prova controllato. La domanda scientifica di questa POC è in realtà — *«FoT può trasferire conoscenza discriminante tra agenti che operano su serie temporali multivariate eterogenee, permettendo il riconoscimento di una condizione temporale localmente unseen?»* — e **non** «FoT risolve la diagnosi dei fault?», tantomeno «FoT funziona sul fotovoltaico?».

> **Provenienza dei risultati.**
>
> #### Che cosa avevamo deciso di misurare prima di conoscere gli esiti finali?
>
> 1. **B−A:** contrasto principale. Chiede se gli insight FoT autentici migliorano il riconoscimento dei fault localmente unseen rispetto all'agente isolato.
> 2. **B−E:** contrasto sulla pertinenza dell'informazione. Chiede se il vantaggio di B dipende dalla corretta associazione semantica degli insight, invece che dalla semplice presenza di testo aggiuntivo.
> 3. **Criteri di supporto:** per esempio B−A > 0, effetto positivo in almeno 3/4 agenti, `helped > harmed`, e il criterio relativo a E.
> 4. **Normal e local-seen preservation:** outcome secondari tenuti separati dal primary, per controllare che l'aggiunta degli insight non comprometta le condizioni già conosciute.
>
> #### Dato il risultato frozen, che cosa possiamo descrivere ulteriormente senza cambiare l'analisi che avevamo deciso in anticipo?
>
> - **Coverage e committed accuracy di A.** Il risultato primary dice semplicemente A = 0/36. Dopo possiamo decomporlo e vedere che A ha 14 astensioni e 22 decisioni committed, tutte e 22 errate. Questo aiuta a capire *come* si forma lo 0/36, ma non cambia l'endpoint.
> - **Unseen-per-fault.** Dopo aver osservato il risultato possiamo chiedere dove sono distribuiti i 31/36 corretti di B: F1 9/9, F8 4/9, F10 9/9, F13 9/9. Questo rivela l'eterogeneità su F8, ma **F8 non diventa un nuovo endpoint pre-specificato**.
> - **Heatmap run × agente.** È una visualizzazione dei medesimi frozen outcomes. Fa vedere quali combinazioni run/agente sono corrette o errate. Non produce nuova evidenza indipendente.
> - **R=3 unanimous vs split.** Dai repetition records possiamo osservare che 33/36 decisioni unseen di B sono unanimi e 3/36 sono split. È un descrittore di *decision stability*, non un test previsto per sostenere l'ipotesi principale.

### 1 · 12 run fisici → 36 agent-case

L'endpoint primario riguarda esclusivamente i fault **localmente unseen**: **12 run fisici indipendenti** (tre per ciascuno dei quattro fault), ciascuno giudicato dai **tre agenti** che non conoscono localmente quel fault → **36 agent-case per configurazione informativa**. Le tre osservazioni sullo stesso run sono correlate: l'unità indipendente è il **run fisico (12)**, non l'agent-case (36) né la singola chiamata LLM. Le predizioni sono gli aggregati frozen di **R=3 chiamate con lo stesso input hash e la stessa configurazione frozen**; l'**astensione conta come incorrect**; gli intervalli derivano da un **cluster bootstrap paired** sui 12 run, stratificato per pseudolabel (10.000 draws, seed frozen 20260829). I criteri di supporto pre-specificati nel protocollo frozen risultano soddisfatti **4/4**:

1. `B−A > 0`;
2. effetto positivo in almeno `3/4` agenti;
3. `helped > harmed`;
4. `Delta_unseen > Delta_E`, dove `Delta_unseen = B−A` e `Delta_E = E−A` (numericamente equivalente a `B−E > 0`).

12 run fisici indipendenti → → → 3 agenti unseen per run → → → 36 agent-case per configurazione informativa → → → A / B / E sugli stessi agent-case → → → bootstrap sui 12 run, non sulle 36 righe

### 2 · Figura 1 — Composizione degli esiti A/B/E

```
A: 22 | 14
B: 31 | 5
E: 3 | 33
```

correttaerrata con decisioneastensione· ogni barra = 36 agent-case

> In A, l'agente si astiene in 14/36 casi e produce una predizione in 22/36 casi. Nessuna delle 22 predizioni committed è corretta. Quindi lo 0/36 di A non deriva soltanto dalle astensioni: anche quando l'agente sceglie una classe localmente unseen, la decisione è errata. In B ed E, invece, non si osservano astensioni.

**Figura 1 —** Composizione degli esiti sui fault localmente unseen. Ogni barra contiene 36 agent-case aggregati derivati da 12 run fisici indipendenti; l'astensione è conteggiata come incorrect. A raggiunge il floor attraverso 14 astensioni e 22 predizioni committed errate; B produce 31 risposte corrette; E conserva lo stesso peer-information block di B ma con associazioni insight–pseudolabel corrotte.

### 3 · Figura 2 — Contrasti B−A e B−E con intervalli di confidenza

Questa figura mostra **quanto cambia l'accuratezza della configurazione informativa FoT (B) rispetto alle due configurazioni informative di controllo**. Non rappresenta quindi le accuracy assolute di A, B ed E, ma le loro differenze.

Per leggere il grafico:

- il **punto** rappresenta la differenza di accuratezza osservata;
- il **segmento orizzontale** rappresenta l'intervallo di confidenza al 95% ottenuto mediante il cluster bootstrap sui 12 run fisici;
- la **linea verticale a Δ=0** rappresenta l'assenza di differenza tra le configurazioni informative confrontate;
- valori positivi, più a destra, indicano un vantaggio maggiore della configurazione informativa B.

Il primo contrasto, **B−A**, risponde alla domanda principale dell'esperimento: gli insight peer autentici aiutano un agente a riconoscere fault che non ha mai osservato localmente? Il risultato è **+0.8611**, con intervallo di confidenza **[0.8333, 0.9167]**. Nel campione osservato, B passa quindi da 0/36 risposte corrette di A a 31/36.

Il secondo contrasto, **B−E**, pone una domanda diversa: il vantaggio di B dipende dalla corretta associazione semantica degli insight oppure potrebbe essere spiegato semplicemente dalla presenza di ulteriore testo nel prompt? Il risultato è **+0.7778**, con intervallo di confidenza **[0.7222, 0.8333]**. Poiché E contiene lo stesso peer-information block di B ma con le associazioni pseudolabel corrotte, questo contrasto supporta l'interpretazione che il beneficio osservato dipenda dalla corretta associazione dell'informazione trasferita e non dalla sola quantità di testo aggiuntivo.

Entrambi gli intervalli rimangono interamente sopra lo zero. **B−A è il contrasto primario pre-specificato; B−E è il contrasto sulla pertinenza dell'informazione pre-specificato e non costituisce un secondo endpoint primario.**

La magnitudine di B−A va comunque interpretata tenendo presente che A rappresenta un **information floor** per le classi localmente unseen: l'agente ricevente non possiede esempi locali della pseudoclasse corrispondente. Il valore +0.8611 non deve quindi essere interpretato come una misura generale delle prestazioni di FoT in altri problemi, modelli o domini.

Differenze di accuratezza B meno A e B meno E
Il punto indica la differenza osservata, il segmento l'intervallo di confidenza bootstrap al 95 per cento e la linea verticale a delta zero l'assenza di differenza.


0
0.25
0.50
0.75
1.00
Δ = 0 · nessuna differenza

B−A
riferimento A = 0/36 (information floor)
+0.861 [0.833, 0.917]

B−E
+0.778 [0.722, 0.833]
Δ accuratezza rispetto al riferimento

**Figura 2 —** Differenze di accuratezza sui fault localmente unseen. I punti indicano i contrasti osservati e i segmenti i relativi intervalli di confidenza al 95%, calcolati con 10.000 ricampionamenti paired dei 12 run fisici, stratificati per pseudolabel (seed frozen 20260829).

> **Nota sull'incertezza.** Gli intervalli sono ottenuti mediante cluster bootstrap paired sui 12 run fisici indipendenti, mantenendo insieme le tre osservazioni dei receiving agents associate allo stesso run. Con soli 12 cluster indipendenti, gli intervalli vanno interpretati nel contesto di questo PoC controllato e non come una caratterizzazione generale dell'incertezza di FoT.

### 4 · Figura 3 — Dove si concentrano successi ed errori di FoT?

Le 31 risposte corrette su 36 agent-case della configurazione informativa B non corrispondono a 36 osservazioni fisiche indipendenti. Il nuovo held-out contiene **12 run di fault indipendenti**: tre F1, tre F8, tre F10 e tre F13. Ogni run viene valutato dai quattro agenti, ma per l'analisi locally-unseen viene escluso l'agente che possiede localmente quel fault. Rimangono quindi tre receiving agents per run: **12 run fisici × 3 receiving agents unseen = 36 agent-case unseen**.

La figura seguente mostra una riga per ciascuno dei 12 run fisici. Una cella verde indica una classificazione unseen corretta in B, una cella rossa una classificazione errata e una cella grigia indica il caso local-seen, escluso dall'endpoint primario.

| # | Fault reale* | Run fisico | Agent 1 | Agent 2 | Agent 3 | Agent 4 |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | F1 | PBH-004 | ● | ✓ | ✓ | ✓ |
| 2 | F1 | PBH-005 | ● | ✓ | ✓ | ✓ |
| 3 | F1 | PBH-006 | ● | ✓ | ✓ | ✓ |
| 4 | F8 | PBH-007 | ✓ | ● | ✗ | ✗ |
| 5 | F8 | PBH-008 | ✓ | ● | ✗ | ✓ |
| 6 | F8 | PBH-009 | ✓ | ● | ✗ | ✗ |
| 7 | F10 | PBH-010 | ✓ | ✓ | ● | ✓ |
| 8 | F10 | PBH-011 | ✓ | ✓ | ● | ✓ |
| 9 | F10 | PBH-012 | ✓ | ✓ | ● | ✓ |
| 10 | F13 | PBH-013 | ✓ | ✓ | ✓ | ● |
| 11 | F13 | PBH-014 | ✓ | ✓ | ✓ | ● |
| 12 | F13 | PBH-015 | ✓ | ✓ | ✓ | ● |

* **Fault reale**: identità evaluator-side, utilizzata esclusivamente nell'analisi offline dopo la frozen inference e non visibile agli agenti, che operavano nello spazio delle pseudolabel.

✓ corretta unseen✗ errata unseen● local-seen — questo fault appartiene alla conoscenza locale dell'agente; la cella non entra nell'endpoint locally-unseen

**Risultati di B per fault reale — analisi descrittiva post-hoc**

Per ciascun fault ci sono 3 run fisici, ciascuno valutato dai 3 agenti che non possiedono localmente quel fault: quindi **3 × 3 = 9 agent-case unseen per fault**.

Fault: F1 · 9/9, F8 · 4/9, F10 · 9/9, F13 · 9/9

In B, F1, F10 e F13 sono riconosciuti correttamente in tutti i 9 agent-case unseen per fault. F8 è corretto in 4/9. Tutti e cinque gli errori unseen osservati in B sono quindi concentrati sugli agent-case associati ai tre run F8.

All'interno dei tre run F8 compare inoltre eterogeneità tra i receiving agents: l'agente che possiede localmente F1 riconosce F8 in 3/3 run, quello che possiede localmente F10 in 0/3 e quello che possiede localmente F13 in 1/3.

Questa è un'analisi descrittiva post-hoc dei record frozen. Mostra dove si concentra la difficoltà osservata, ma non permette di identificarne la causa.

Per confronto, A contiene 0/36 risposte corrette, 22 errori committed e 14 astensioni; E contiene 3/36 risposte corrette e 33 errori. La composizione globale delle tre configurazioni informative è già mostrata nella Figura 1.

**Figura 3 — Distribuzione degli outcome della configurazione informativa B nei 12 run fisici di fault del nuovo held-out.** Ogni riga rappresenta un singolo run fisico; le quattro colonne rappresentano i quattro agenti. Per ogni run, la cella dell'agente che possiede localmente quel fault è indicata come local-seen ed esclusa dall'endpoint primario. Le altre tre celle costituiscono i tre agent-case locally-unseen associati al run. I 12 run producono quindi 36 agent-case unseen, non 36 osservazioni fisiche indipendenti. La figura è un'analisi descrittiva post-hoc dei record frozen.

### 5 · Cosa succede ai casi già conosciuti e quanto sono stabili le decisioni?

Il risultato principale della Phase B riguarda i fault localmente unseen: vogliamo sapere se gli insight peer permettono al receiving agent di riconoscere condizioni che non possiede nella propria conoscenza locale. Un trasferimento utile, però, non dovrebbe essere valutato soltanto su ciò che l'agente non conosce: è importante controllare anche che cosa accade ai casi che sa già riconoscere.

Per questo il protocollo frozen mantiene separati due outcome secondari: i fault **local-seen**, per i quali l'agente possiede esempi locali, e la condizione **Normal**. Non sono l'endpoint primario, che resta locally-unseen; sono outcome distinti usati per verificare se, nel campione held-out osservato, l'aggiunta degli insight peer sia accompagnata da una degradazione evidente delle prestazioni già acquisite.

#### 5.1 · Preservation: FoT altera ciò che l'agente sa già riconoscere?

Il controllo di preservation confronta A, B ed E sui casi local-seen e Normal. Se l'aggiunta degli insight peer producesse errori in condizioni precedentemente riconosciute correttamente, questo costituirebbe un segnale di possibile interferenza o negative transfer nel campione osservato.

| Secondary outcome | A | B | E |
| --- | --- | --- | --- |
| Local-seen pre-specificato nel protocollo frozen | 12/12 | 12/12 | 12/12 |
| Normal pre-specificato nel protocollo frozen | 12/12 | 12/12 | 12/12 |

In ciascuno dei due scope ci sono **12 agent-case** osservati. Per i fault local-seen, ciascuno dei 12 run fisici di fault viene valutato dall'unico agente che possiede localmente quel fault. Per Normal, i tre run Normal del nuovo held-out vengono valutati dai quattro agenti, producendo **3 × 4 = 12 agent-case**.

Nel campione held-out osservato, tutti i casi local-seen e Normal risultano corretti in tutte e tre le configurazioni informative: A, B ed E ottengono 12/12 in entrambi gli scope. **Nel campione held-out osservato non è stata rilevata degradazione** delle prestazioni su condizioni già conosciute quando vengono aggiunti gli insight peer.

Questo risultato è un controllo di preservation nel campione studiato. Non dimostra che FoT sia generalmente immune da negative transfer e non autorizza una claim universale di assenza di degradazione.

#### 5.2 · Stabilità delle decisioni nelle tre chiamate R=3

Ogni agent-case-condition è stato eseguito tre volte. Le tre chiamate condividono lo stesso input hash e la stessa configurazione frozen, ma le risposte del modello non sono necessariamente identiche. Il protocollo aggrega le tre chiamate con la regola frozen: una pseudolabel valida con almeno due voti diventa la predizione aggregata; in assenza di una maggioranza valida di due voti, l'aggregato astiene.

Per descrivere la consistenza delle decisioni distinguiamo:

- **unanimous:** le tre chiamate R=3 coincidono nella decisione, considerando pseudolabel predetta e stato di astensione;
- **split:** almeno una delle tre chiamate differisce; la regola frozen può comunque produrre una decisione aggregata quando una pseudolabel valida riceve almeno due voti.

**Decisioni B sui 36 agent-case unseen** post-hoc descrittivo

Fault: Unanimous· 33/36 · 91.67%, Split· 3/36 · 8.33%

Questa decomposizione unanimous/split è una derivazione descrittiva post-hoc dei repetition records frozen. Non era uno degli endpoint utilizzati per giudicare il successo primario della Phase B.

Il fatto che 33/36 decisioni unseen di B siano unanimi indica che, nel setup frozen osservato, la maggior parte delle decisioni aggregate deriva da tre chiamate concordi. È un descrittore della **stabilità delle decisioni tra le tre chiamate R=3**, non una misura generale di robustezza. Le chiamate usano lo stesso input e la stessa configurazione: il risultato non dimostra stabilità rispetto a perturbazioni dei dati, prompt diversi, altri modelli, altre configurazioni di reasoning o distribuzioni differenti.

> **Come leggere questi controlli.** Il primary result mostra il trasferimento sui fault localmente unseen. I secondary outcome mostrano che, nel campione osservato, questo beneficio non è accompagnato da una degradazione visibile sui casi local-seen o Normal. La verifica R=3 aggiunge un'informazione diversa: descrive quanto le tre chiamate concordano tra loro. Nessuno di questi controlli amplia il risultato oltre il setup TEP studiato.

### 6 · Scope and limitations

- TEP è una POC metodologica controllata; il fotovoltaico è il dominio-obiettivo finale.
- A è una baseline information-floor per la semantica delle classi localmente unseen.
- Riconoscimento in spazio di pseudolabel chiuso, non diagnosi open-world.
- Solo 12 cluster indipendenti.
- Un solo simulatore/processo.
- Una sola configurazione LLM/reasoning.
- Nessuna garanzia formale di privacy.
- Nessuna baseline ICL centralizzata a pari informazione.
- Nessuna claim di generalizzazione al PV o cross-domain.
- harmed=0 non è evidenza di assenza generale di negative transfer.

### 7 · Claim finale

> Nel protocollo frozen e sui 12 run fisici di fault del nuovo held-out TEP, gli insight peer autentici hanno aumentato l'accuratezza sui fault localmente unseen da **0/36 (A) a 31/36 (B)**; il contrasto primario **B−A è +0.8611 [0.8333, 0.9167]**. A parità di testi, ID, ordine e volume del peer block, la corruzione delle associazioni ha ridotto l'accuratezza a **3/36**: *il contrasto B−E supporta l'interpretazione che il beneficio osservato dipenda dalla corretta associazione dell'informazione trasferita, anziché dalla mera presenza o dal volume del testo aggiuntivo* (B−E +0.7778 [0.7222, 0.8333]). *La configurazione informativa A rappresenta uno scenario di limite informativo per la semantica delle classi localmente unseen, perché l'agente ricevente non dispone di alcun esempio locale della pseudoclasse corrispondente*; la magnitudine di B−A va quindi letta rispetto a questo floor. Questi risultati supportano la **feasibility** del trasferimento testuale federato di conoscenza discriminante tra agenti su serie temporali multivariate eterogenee nel setup TEP studiato; non dimostrano generalizzazione cross-domain o al fotovoltaico, non forniscono garanzie di privacy, né stabiliscono superiorità rispetto a una baseline centralizzata ICL a pari informazione. La validazione empirica sul fotovoltaico è la fase successiva.

Fase 2 — Replica confirmatory · EXP3_V2

**Dalla Fase 1 alla Fase 2.** Lo Step 17 ha mostrato che, su 12 run fisici held-out, gli insight FoT autentici hanno portato l'accuratezza unseen da 0/36 (A) a 31/36 (B), con un contrasto B−A di +0.861 [0.833, 0.917]. Ma quel risultato poggia su un singolo campione held-out di 12 run fisici. La domanda che apre la Fase 2 è: *il fenomeno si riproduce su nuove realizzazioni indipendenti delle stesse classi?*

Tutto il metodo — feature, soglie, agenti, insight, configurazioni informative, protocollo frozen — rimane identico. Cambiano solo i dati fisici sottostanti: 24 nuovi run di fault (6 per classe) e 6 nuovi run Normal, il doppio della Fase 1. L'architettura sperimentale e le decisioni di analisi sono state congelate *prima* di generare questi dati.

**Step 18 / 25Fase 2Esperimento confermativo su nuove realizzazioni simulate**

## Esperimento confermativo su nuove realizzazioni simulate

Un held-out, per definizione, può essere aperto una sola volta: dopo che i risultati di Experiment 1 sono stati osservati, quei dati non sono più vergini rispetto all'ipotesi. Non è quindi possibile riusarli per rispondere alla domanda *«il risultato regge su realizzazioni fisiche diverse?»* senza introdurre un rischio di conferma post-hoc.

Il rischio specifico da escludere non è il data leakage classico — il protocollo frozen lo controlla già — ma che le dodici realizzazioni fisiche del held-out di Experiment 1 abbiano caratteristiche idiosincratiche (pattern di rumore, transitori, derive di sensore) che hanno favorito il trasferimento in quel campione particolare, senza che il fenomeno sia riproducibile su run indipendenti delle stesse classi.

Le nuove realizzazioni fisiche sono run TEP indipendenti delle stesse quattro classi — non reruns dei file già usati, non nuove classi, non un dominio diverso. Il perimetro sperimentale rimane deliberatamente invariato: il metodo, gli agenti, le soglie e il protocollo frozen di Experiment 1 vengono riapplicati as-is alle nuove realizzazioni. L'obiettivo non è la generalizzazione, ma verificare se l'effetto osservato sia riproducibile quando i dati fisici cambiano pur restando fisso tutto il resto.

**Step 19 / 25Fase 2Nuovo held-out**

## Le nuove realizzazioni fisiche di EXP3_V2

Per costruire il nuovo held-out sono stati generati run TEP indipendenti degli stessi quattro tipi di guasto studiati in Experiment 1, più i casi Normal. I run sono stati congelati prima di qualsiasi inferenza, applicando la stessa logica freeze-before-test che ha governato la Fase 1: nessun dato del nuovo held-out ha influenzato feature, soglie, agenti o insight, che restano quelli di Experiment 1 senza ricalibrazione.

30 nuove realizzazioni simulate = 6 Normali + 6 run per ciascun fault

| Normal | F1 | F8 | F10 | F13 |
| --- | --- | --- | --- | --- |
| 6 run | 6 run | 6 run | 6 run | 6 run |

Il raddoppio rispetto ai 15 run di Experiment 1 (3 per classe) porta a 72 agent-case unseen, aumentando la potenza statistica del contrasto primario B−A senza modificare il disegno sperimentale.

**Step 20 / 25Fase 2Disegno confirmatory frozen**

## Il disegno confirmatory di EXP3_V2

Un disegno **confirmatory frozen** significa che ipotesi primaria, popolazione di analisi, contrasti e criteri di successo sono stati scritti prima di aprire i dati — e non possono essere modificati dopo aver visto i risultati. L'analisi è quindi eseguita una volta sola, sui record già congelati, senza margine di aggiustamento retroattivo.

> Popolazione e configurazioni informative
>
> ### Chi viene valutato e in quale configurazione informativa
>
> **Popolazione primaria:** i casi *locally unseen*, cioè i fault run valutati dall'agente che non possiede esempi locali di quella classe. Ogni fault ha tre agenti che non lo conoscono: con 6 run per fault e 4 fault, la popolazione primaria è **6 × 4 × 3 = 72 agent-case**.
>
> Ciascuno di questi 72 agent-case viene valutato in tre configurazioni informative — A, B ed E — definite esattamente come in Experiment 1 (Step 15):
>
> | Configurazione informativa | Che cosa riceve l'agente oltre ai few-shot locali |
> | --- | --- |
> | **A — isolated** | Nessun insight peer. Misura la performance senza alcuna federazione. |
> | **B — FoT** | 6 insight peer autentici, con associazioni semantiche corrette. |
> | **E — corrupted** | Gli stessi 6 insight di B — stessi testi, stessi ID, stesso volume — ma con le pseudolabel permutate in modo che nessuna rimanga associata alla classe originale. |
>
> Le astensioni (nessuna maggioranza tra le R=3 risposte) contano come errori in tutte e tre le configurazioni informative.

> Contrasti e criterio di replica
>
> ### Che cosa si confronta e come si decide
>
> **B−A (contrasto primario):** la differenza di accuratezza tra la configurazione informativa con federazione autentica e quella senza. Risponde alla domanda: *«aggiungere insight peer corretti aumenta la capacità di riconoscere fault unseen?»*. Il criterio di replica richiede *congiuntamente* che la differenza osservata sia positiva *e* che il limite inferiore del suo intervallo di confidenza al 95% sia positivo — entrambe le condizioni devono essere soddisfatte.
>
> **B−E (evidenza supporting):** la differenza tra insight autentici e insight con associazioni corrotte. Risponde alla domanda: *«il beneficio di B dipende dal contenuto semanticamente corretto degli insight, o basta avere più testo nel prompt?»*. Un valore positivo di B−E costituisce l’evidenza di supporto pre-specificata. Il relativo intervallo di confidenza al 95% viene riportato per descrivere l’incertezza della stima, ma l’esclusione dello zero non costituisce un ulteriore criterio decisionale per la replica.
>
> 72 agent-case unseen → × → configurazioni informative A / B / E → → → aggregati frozen → → → bootstrap cluster-paired → → → contrasti B−A · B−E

**Step 21 / 25Fase 2**

## Diagnosi di guasti non osservati localmente

L'endpoint primario riguarda esclusivamente i fault **localmente unseen**: **24 run fisici indipendenti** (sei per ciascuno dei quattro fault), ciascuno giudicato dai **tre agenti** che non conoscono localmente quel fault → **72 agent-case per configurazione informativa**. Le tre osservazioni sullo stesso run sono correlate: l'unità indipendente è il **run fisico (24)**, non l'agent-case (72). Le predizioni sono gli aggregati frozen di R=3 chiamate; l'**astensione conta come incorrect**; gli intervalli derivano da un **cluster bootstrap paired** sui 24 run, stratificato per pseudolabel (10.000 draws, seed frozen 320031).

24 run fisici indipendenti → → → 3 agenti unseen per run → → → 72 agent-case per configurazione informativa → → → A / B / E sugli stessi agent-case → → → bootstrap sui 24 run, non sulle 72 righe

### 1 · Tabella riassuntiva

Popolazione primaria unseen — EXP3_V2

| Configurazione informativa | Corretti / 72 | Accuratezza | Astensioni | Errori committed |
| --- | --- | --- | --- | --- |
| **A** | 0 / 72 | 0.0% | 30 | 42 |
| **B** | 68 / 72 | 94.4% | 0 | 4 |
| **E** | 4 / 72 | 5.6% | 0 | 68 |

### 2 · Figura 4 — Composizione degli esiti A/B/E

```
A: 42 | 30
B: 68 | 4
E: 4 | 68
```

correttaerrata con decisioneastensione· ogni barra = 72 agent-case

> **Decomposizione dello 0/72 di A.** In A, l'agente si astiene in 30/72 casi e produce una predizione committed in 42/72 casi. Nessuna delle 42 predizioni committed è corretta. Lo 0/72 non deriva soltanto dalle astensioni: anche quando l'agente sceglie una classe localmente unseen, la decisione è errata. In B ed E, invece, non si osservano astensioni.

**Figura 4 —** Composizione degli esiti sui fault localmente unseen. Ogni barra contiene 72 agent-case aggregati derivati da 24 run fisici indipendenti; l'astensione è conteggiata come incorrect. A raggiunge il floor attraverso 30 astensioni e 42 predizioni committed errate; B produce 68 risposte corrette; E conserva lo stesso peer-information block di B ma con associazioni insight–pseudolabel corrotte e produce 4 risposte corrette.

### 3 · Figura 5 — Dove si concentrano successi ed errori di FoT?

Le 68 risposte corrette su 72 agent-case della configurazione informativa B derivano da **24 run di fault indipendenti**: sei F1, sei F8, sei F10 e sei F13. Ogni run viene valutato dai quattro agenti, ma per l'analisi locally-unseen viene escluso l'agente che possiede localmente quel fault. Rimangono quindi tre receiving agents per run: **24 run fisici × 3 receiving agents unseen = 72 agent-case unseen**.

La figura seguente mostra una riga per ciascuno dei 24 run fisici. Una cella verde indica una classificazione unseen corretta in B, una cella rossa una classificazione errata. Le celle con sfondo grigio chiaro indicano il caso local-seen, escluso dall'endpoint primario; quelle con sfondo rosato indicano un errore local-seen.

| # | Fault reale* | Run fisico | Agent 1 (F1) | Agent 2 (F8) | Agent 3 (F10) | Agent 4 (F13) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | F1 | EXP3V2-F1-001 | • | ✓ | ✓ | ✓ |
| 2 | F1 | EXP3V2-F1-002 | • | ✓ | ✓ | ✓ |
| 3 | F1 | EXP3V2-F1-003 | • | ✓ | ✓ | ✓ |
| 4 | F1 | EXP3V2-F1-004 | • | ✓ | ✓ | ✓ |
| 5 | F1 | EXP3V2-F1-005 | • | ✓ | ✓ | ✓ |
| 6 | F1 | EXP3V2-F1-006 | • | ✓ | ✓ | ✓ |
| 7 | F8 | EXP3V2-F8-001 | ✓ | • | ✓ | ✓ |
| 8 | F8 | EXP3V2-F8-002 | ✓ | • | ✓ | ✓ |
| 9 | F8 | EXP3V2-F8-003 | ✗ | ✗ | ✗ | ✓ |
| 10 | F8 | EXP3V2-F8-004 | ✓ | • | ✓ | ✓ |
| 11 | F8 | EXP3V2-F8-005 | ✓ | • | ✓ | ✓ |
| 12 | F8 | EXP3V2-F8-006 | ✓ | • | ✓ | ✓ |
| 13 | F10 | EXP3V2-F10-001 | ✓ | ✓ | • | ✓ |
| 14 | F10 | EXP3V2-F10-002 | ✓ | ✓ | • | ✓ |
| 15 | F10 | EXP3V2-F10-003 | ✓ | ✓ | • | ✓ |
| 16 | F10 | EXP3V2-F10-004 | ✓ | ✓ | • | ✓ |
| 17 | F10 | EXP3V2-F10-005 | ✓ | ✓ | • | ✓ |
| 18 | F10 | EXP3V2-F10-006 | ✓ | ✓ | • | ✓ |
| 19 | F13 | EXP3V2-F13-001 | ✓ | ✓ | ✓ | • |
| 20 | F13 | EXP3V2-F13-002 | ✗ | ✓ | ✗ | ✗ |
| 21 | F13 | EXP3V2-F13-003 | ✓ | ✓ | ✓ | ✗ |
| 22 | F13 | EXP3V2-F13-004 | ✓ | ✓ | ✓ | ✗ |
| 23 | F13 | EXP3V2-F13-005 | ✓ | ✓ | ✓ | ✗ |
| 24 | F13 | EXP3V2-F13-006 | ✓ | ✓ | ✓ | • |

* **Fault reale**: identità evaluator-side, utilizzata esclusivamente nell'analisi offline dopo la frozen inference. Le celle con sfondo rosato indicano errori local-seen dell'agente che possiede quel fault.

✓ corretta unseen✗ errata unseen• local-seen corretta✗ local-seen errata

**Risultati di B per fault reale — analisi descrittiva post-hoc**

Per ciascun fault ci sono 6 run fisici, ciascuno valutato dai 3 agenti che non possiedono localmente quel fault: quindi **6 × 3 = 18 agent-case unseen per fault**.

Fault: F1 · 18/18, F8 · 16/18, F10 · 18/18, F13 · 16/18

In B, F1 e F10 sono riconosciuti correttamente in tutti i 18 agent-case unseen per fault. F8 e F13 presentano ciascuno 2 errori unseen.

**Per-agent unseen accuracy di B** post-hoc descrittivo

Fault: Agent 1 (F1) · 16/18, Agent 2 (F8) · 18/18, Agent 3 (F10) · 16/18, Agent 4 (F13) · 18/18

Tutti e quattro gli errori unseen di B sono concentrati su due run specifici — EXP3V2-F8-003 e EXP3V2-F13-002 — dove sia Agent 1 sia Agent 3 sbagliano contemporaneamente. Agent 2 e Agent 4 non commettono errori unseen.

**Figura 5 — Distribuzione degli outcome della configurazione informativa B nei 24 run fisici di fault di EXP3_V2.** Ogni riga rappresenta un singolo run fisico; le quattro colonne rappresentano i quattro agenti. Per ogni run, la cella dell'agente che possiede localmente quel fault è indicata come local-seen. Le altre tre celle costituiscono i tre agent-case locally-unseen. I 24 run producono 72 agent-case unseen, non 72 osservazioni fisiche indipendenti. La figura è un'analisi descrittiva post-hoc dei record frozen.

**Step 22 / 25Fase 2**

## B−A primario e B−E di supporto: differenze di accuratezza e intervalli di confidenza

### 1 · Tabella dei contrasti

| Contrasto | Stima | CI percentile 95% | Ruolo |
| --- | --- | --- | --- |
| **B−A** | 0.9444 | [0.8611, 1.0] | Contrasto primario; entrambi i criteri pre-specificati sono soddisfatti. |
| **B−E** | 0.8889 | [0.7778, 0.9861] | Evidenza supporting per la pertinenza dell'informazione; il CI non costituisce un gate aggiuntivo. |

### 2 · Figura 6 — Forest plot dei contrasti EXP3_V2

Questa figura mostra **quanto cambia l'accuratezza della configurazione informativa FoT (B) rispetto alle due configurazioni informative di controllo**. Non rappresenta le accuracy assolute di A, B ed E, ma le loro differenze.

Per leggere il grafico: il **punto** rappresenta la differenza osservata; il **segmento orizzontale** l'intervallo di confidenza al 95%; la **linea verticale a Δ=0** l'assenza di differenza; valori più a destra indicano un vantaggio maggiore di B.

Differenze di accuratezza B meno A e B meno E — EXP3_V2
Il punto indica la differenza osservata, il segmento l'intervallo di confidenza bootstrap al 95 per cento e la linea verticale a delta zero l'assenza di differenza.


0
0.25
0.50
0.75
1.00
Δ = 0 · nessuna differenza


B−A
riferimento A = 0/72 (information floor)
+0.944 [0.861, 1.0]


B−E
+0.889 [0.778, 0.986]
Δ accuratezza rispetto al riferimento

**Figura 6 —** Differenze di accuratezza sui fault localmente unseen. I punti indicano i contrasti osservati e i segmenti i relativi intervalli di confidenza al 95%, calcolati con 10.000 ricampionamenti paired dei 24 run fisici, stratificati per pseudolabel (seed frozen 320031).

> **Criterio di replica.** Il contrasto B−A osservato è +0.9444 > 0 e il limite inferiore del CI al 95% è 0.8611 > 0. Entrambe le condizioni del criterio pre-specificato sono quindi soddisfatte. Entrambi gli intervalli rimangono interamente sopra lo zero.
>
> B−A è il contrasto primario pre-specificato; B−E è il contrasto sulla pertinenza dell'informazione pre-specificato e non costituisce un secondo endpoint primario. La magnitudine di B−A va interpretata tenendo presente che A rappresenta un **information floor** per le classi localmente unseen.

> **Nota sull'incertezza.** Gli intervalli sono ottenuti mediante cluster bootstrap paired sui 24 run fisici indipendenti, mantenendo insieme le tre osservazioni dei receiving agents associate allo stesso run. Con 24 cluster indipendenti (il doppio di Experiment 1), gli intervalli sono più stretti ma vanno comunque interpretati nel contesto di questo PoC controllato.

**Step 23 / 25Fase 2**

## Risultati secondari descrittivi

Le popolazioni local-seen, Normal e overall sono risultati secondari esclusivamente descrittivi e non aggiungono criteri inferenziali.

| Configurazione informativa | Local-seen (fault) | Normal | Overall |
| --- | --- | --- | --- |
| **A** | 24/24 (100.0%) | 24/24 (100.0%) | 48/120 (40.0%) |
| **B** | 19/24 (79.2%) | 24/24 (100.0%) | 111/120 (92.5%) |
| **E** | 22/24 (91.7%) | 24/24 (100.0%) | 50/120 (41.7%) |

> **Osservazione sulla degradazione local-seen di B.** In Experiment 1, i fault local-seen erano 12/12 in tutte e tre le configurazioni informative: nessuna degradazione. In EXP3_V2, A mantiene 24/24 ma **B scende a 19/24**: cinque casi local-seen diventano errori quando gli insight peer vengono aggiunti. I cinque errori riguardano Agent 4 (F13) su quattro run e Agent 2 (F8) su uno. In particolare:
>
> - Agent 4 sbaglia i run F13-002, -003, -004, -005 (4 errori local-seen su 6 run del proprio fault)
> - Agent 2 sbaglia il run F8-003 (1 errore local-seen su 6 run del proprio fault)
>
> Anche E mostra una leggera degradazione (22/24). Questo è un segnale descrittivo che gli insight peer, in alcune combinazioni run–agente, possono interferire con il riconoscimento di fault già noti localmente. Il fenomeno non era osservabile con soli 12 local-seen di Experiment 1. Non essendo un endpoint primario, la sua entità non altera la decisione sulla replica, ma va registrato come osservazione rilevante per il disegno futuro.

### Tabella comparativa: Experiment 1 vs EXP3_V2

**Experiment 1 (Fase 1)**

**EXP3_V2 (Fase 2)**

**Dimensioni del campione**

12 run di fault (3 per classe) + 3 Normal36 agent-case unseen per configurazione informativa

24 run di fault (6 per classe) + 6 Normal72 agent-case unseen per configurazione informativa

**Risultati primari unseen**

A:0/36 ·B:31/36 ·E:3/36

A:0/72 ·B:68/72 ·E:4/72

**Contrasto B−A [CI 95%]**

+0.861 [0.833, 0.917]12 cluster, seed 20260829

+0.944 [0.861, 1.0]24 cluster, seed 320031

**Contrasto B−E [CI 95%]**

+0.778 [0.722, 0.833]

+0.889 [0.778, 0.986]

**Decomposizione A**

22 errori committed + 14 astensioni = 0/36

42 errori committed + 30 astensioni = 0/72

**Local-seen fault (B)**

12/12 (100%) — nessuna degradazione

19/24 (79.2%)— 5 errori local-seen

**Normal (B)**

12/12 (100%)

24/24 (100%)

La tabella confronta i risultati dei due esperimenti sullo stesso disegno sperimentale. L'incremento della dimensione campionaria da 12 a 24 run fisici restringe gli intervalli di confidenza. La degradazione local-seen osservata in EXP3_V2 non era visibile in Experiment 1.

**Step 24 / 25Fase 2Interpretazione, limiti e provenienza frozen**

## Che cosa supporta la replica, e che cosa non dimostra

### 1 · Scope and limitations

- TEP è una POC metodologica controllata; il fotovoltaico è il dominio-obiettivo finale.
- A è una baseline information-floor per la semantica delle classi localmente unseen.
- Riconoscimento in spazio di pseudolabel chiuso, non diagnosi open-world.
- 24 cluster indipendenti (il doppio di Experiment 1, ma pur sempre un campione limitato).
- Un solo simulatore/processo (TEP).
- Una sola configurazione LLM/reasoning (`gpt-5.6-terra`, reasoning `medium`).
- Nessuna garanzia formale di privacy.
- Nessuna baseline ICL centralizzata a pari informazione.
- Nessuna claim di generalizzazione al PV o cross-domain.
- La degradazione local-seen osservata in B (19/24 vs 24/24 di A) è un segnale descrittivo che merita approfondimento nel disegno futuro, ma non invalida il primary result unseen.
- Il disegno riproduce *le stesse classi di fault* su nuove realizzazioni, non generalizza a fault non studiati.

### 2 · Claim finale — EXP3_V2

> Nel protocollo frozen e sulle 24 nuove realizzazioni fisiche di fault del held-out EXP3_V2, gli insight peer autentici hanno aumentato l’accuratezza sui fault localmente unseen da **0/72 (A) a 68/72 (B)**; il contrasto primario **B−A è +0.9444 [0.8611, 1.0]**. Il criterio pre-specificato di replica — B−A > 0 con limite inferiore del CI > 0 — è soddisfatto.
>
> A parità di testi, ID, ordine e volume del peer block, la corruzione delle associazioni ha ridotto l’accuratezza a **4/72**: il contrasto B−E +0.8889 [0.7778, 0.9861] supporta l’interpretazione che il beneficio osservato dipenda dalla corretta associazione dell’informazione trasferita. *La configurazione informativa A rappresenta uno scenario di limite informativo per la semantica delle classi localmente unseen*; la magnitudine di B−A va letta rispetto a questo floor.
>
> EXP3_V2 rafforza il risultato di Experiment 1 raddoppiando la dimensione campionaria e riproducendo l’effetto su realizzazioni fisiche indipendenti. Tuttavia, la degradazione local-seen (B: 19/24 vs A: 24/24) indica che gli insight peer possono interferire con il riconoscimento dei fault già noti in alcune combinazioni run–agente — un aspetto non emerso con il campione più piccolo di Experiment 1.
>
> Questi risultati supportano la **feasibility** e la **riproducibilità** del trasferimento testuale federato di conoscenza discriminante tra agenti su serie temporali multivariate eterogenee nel setup TEP studiato; non dimostrano generalizzazione cross-domain o al fotovoltaico, non forniscono garanzie di privacy, né stabiliscono superiorità rispetto a una baseline centralizzata ICL a pari informazione. La validazione empirica sul fotovoltaico è la fase successiva.

Fase 3 — Portabilità cross-model · EXP2

**Dalla Fase 2 alla Fase 3.** Experiment 1 ha stabilito l’effetto di trasferimento e la sua specificità semantica; Experiment 3 (Fase 2) lo ha replicato su realizzazioni fisiche indipendenti. Entrambi, però, hanno utilizzato un unico reasoning model (`gpt-5.6-terra`) sia per produrre gli insight sia per consumarli in fase di classificazione. Resta aperta una domanda: *la conoscenza testuale congelata è accoppiata al reasoner che l’ha generata, oppure può essere consumata utilmente da modelli diversi?*

**Step 25 / 25Fase 3Portabilità cross-model**

## Intro preliminare

La distinzione chiave è tra **producer** e **consumer**. Il producer — il modello che ha generato gli insight a partire dai casi development/calibration — rimane `gpt-5.6-terra` e non viene variato: gli insight peer restano quelli frozen di Experiment 1, byte per byte. Ciò che varia è esclusivamente il consumer, cioè il reasoning model che riceve il caso da classificare, gli esempi locali few-shot e gli insight federati e deve produrre la pseudolabel finale. Experiment 2 testa quindi la **portabilità cross-model della conoscenza testuale congelata**: la stessa evidenza, la stessa conoscenza, gli stessi casi — un reasoner diverso.

Tutti gli altri elementi sperimentali sono mantenuti identici: held-out frozen di Experiment 1, verbalizer V2, pseudolabel opache, configurazioni informative A/B/E, prompt, regola di aggregazione, evaluator e bootstrap. In questo modo, qualsiasi variazione osservata può essere attribuita al cambio del consumer e non a differenze nei dati o nella conoscenza trasferita.

La scelta dei reasoner include almeno un modello **open-weight**, che serve anche da ancora di riproducibilità: un risultato replicabile con pesi pubblici e inferenza deterministica (temperature 0, seed fisso) è più difficile da contestare di uno ottenuto esclusivamente con API proprietarie. L’aggiunta di un secondo modello di famiglia diversa dall’originale rafforza ulteriormente la claim.

La research question di Experiment 2 è:

> *Does the transfer effect and its semantic specificity persist when the same frozen peer textual knowledge is consumed by different reasoning models?*

Un risultato positivo fornirebbe evidenza che la conoscenza testuale prodotta nel setting FoT non è accoppiata al reasoner originale — proprietà rilevante per la praticabilità del meccanismo, che si aggancia al risultato *weak-to-strong in text space* della letteratura. Tuttavia, poiché il producer degli insight non viene variato e l’held-out è lo stesso di Experiment 1, la claim resta circoscritta alla portabilità del consumo: parlare di «model-generality end-to-end» richiederebbe variare anche la produzione. Experiment 2 è quindi complementare a Experiment 3 (Fase 2): là cambiavano i dati fisici a parità di reasoner, qui cambia il reasoner a parità di dati e conoscenza.
