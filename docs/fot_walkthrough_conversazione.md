# Federation over Text for Locally Unseen Fault Diagnosis in Multivariate Time Series

**Step 1 / 28**

## Introduzione

Il dominio di base è quello degli impianti **fotovoltaici (PV) distribuiti**. Ogni sito osserva proprie serie temporali e propri eventi; clima, impianto, guasti, inverter e regime operativo rendono plausibile una conoscenza locale eterogenea, cioè **non-IID**.

L'obiettivo è esplorare una federazione in cui i siti non debbano centralizzare dati grezzi né scambiarsi necessariamente pesi o gradienti di un modello: ciascun nodo sintetizza conoscenza locale in **testo strutturato** e gli altri nodi la usano per ragionare. La ground truth entra soltanto nella valutazione offline; osservazione numerica, comunicazione testuale, insight e decisione restano separati, così che un buon testo non venga confuso con una diagnosi corretta.

Il lavoro adotta **Federation over Text (FoT), introdotto da Yao et al.** in *Federation over Text: Insight Sharing for Multi-Agent Reasoning* (Yao, Rabbani, Zaheer, Li — [arXiv:2604.16778](https://arxiv.org/abs/2604.16778), repo [github.com/dixiyao/FoT](https://github.com/dixiyao/FoT)). In FoT, agenti con LLM frozen distillano *reasoning trace* in insight, poi aggregati e ridistribuiti come testo, senza gradienti né fine-tuning. Yao et al. valutano il paradigma su task testuali di matematica, QA e coding; qui lo si applica e valuta nella diagnosi di guasti da serie temporali industriali multivariate.

Da FoT di Yao et al. si riprende l’architettura ad alto livello: insight locali → aggregazione → ridistribuzione ai peer. L'adattamento usa una verbalizzazione deterministica e verificabile delle serie temporali, separata dalla successiva inferenza dell'LLM.

Come banco di prova controllato si usa il **Tennessee Eastman Process (TEP)**, un processo chimico simulato con fault noti e ground truth verificabile. I dati provengono dallo snapshot upstream [github.com/mv-per/tennessee-eastman-dataset](https://github.com/mv-per/tennessee-eastman-dataset) (commit pinnato `309b944f`). TEP è un **gate di fattibilità metodologica**: permette di verificare il meccanismo FoT in condizioni note, non è la destinazione applicativa finale, che resta il fotovoltaico.

Lo stato attuale comprende un primo esperimento, una replica su nuovi run simulati, un consumer open-weight, un riferimento centralizzato, un confronto tra quattro rappresentazioni TS→testo, la misura del payload comunicativo, una baseline numerica a prototipi condivisi sul compito local-unseen e una suite centralizzata con gli otto modelli richiesti dal supervisor. I limiti e il loro stato sono raccolti nella sezione **Critiche**.

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

- **A** costituisce il riferimento senza insight — né peer né propri: l'agente usa soltanto i few-shot — la coppia (testo neutrale, pseudolabel) prodotta facendo passare i batch 1–2 (fault) e N1–N2 (Normal) attraverso la pipeline Fase 1 — etichettati della propria esperienza locale, senza includere i propri insight generati localmente;
- **B** fornisce i sei insight dei tre peer. Due descrivono il guasto da riconoscere e quattro agiscono da distrattori;
- **E** contiene gli stessi sei insight, nello stesso ordine e con la stessa lunghezza, ma associa ogni descrizione alla pseudolabel sbagliata.

Il confronto tra queste configurazioni informative permette di distinguere l’effetto della semplice presenza di testo dall’effetto prodotto da conoscenza pertinente al tipo di guasto.

### 1.3 Obiettivi sperimentali

L’obiettivo principale è verificare se la configurazione informativa **B** migliori, rispetto alla configurazione informativa **A**, la diagnosi delle realizzazioni **local-unseen**. Il confronto primario **B−A** valuta quindi se un agente possa utilizzare conoscenza condivisa per riconoscere un tipo di guasto che non ha incontrato nella propria esperienza locale.

Il confronto **B−E** ha invece funzione di supporto e valuta la pertinenza dell’informazione, indicata formalmente come *specificità semantica*. Esso permette di verificare se l’eventuale beneficio dipenda dalla corretta relazione tra l’**insight** e il tipo di guasto, anziché dalla sola presenza di informazioni testuali. **B−E** non costituisce un secondo confronto primario.

I meccanismi concreti con cui vengono costruite le configurazioni informative **A**, **B** ed **E** — la struttura del prompt, la federazione degli insight e la permutazione di controllo — sono descritti negli Step 15 e 16. Le popolazioni **local-seen**, **Normal** e overall rimangono descrittive e non introducono ulteriori obiettivi confermativi. La replica sui nuovi run, il test con Qwen, il riferimento C, l'ablation e la misura del payload rafforzano o delimitano il risultato principale; non cambiano l'obiettivo primario.

### 1.6 Novità dell'esperimento

FoT è stato introdotto da Yao et al.; questo lavoro non propone FoT né la federazione testuale. Il contributo va descritto prudentemente come la seguente combinazione:

1. **Applicazione industriale.** Federation over Text di Yao et al. viene applicato a serie temporali industriali multivariate.
2. **Esperienza class-disjoint.** Ogni agente conosce localmente un solo guasto e viene valutato anche su diagnosi *local-unseen*.
3. **Verbalizzazione verificabile.** La serie numerica diventa testo con regole fisse, soglie calibrate e parole neutrali; ogni frase può essere ricondotta ai numeri di partenza.
4. **Controllo B/E.** B ed E hanno lo stesso payload, ma E collega il testo alle etichette sbagliate; il contrasto verifica la specificità semantica dell'informazione.
5. **Protocollo frozen e replica.** Configurazione e artefatti vengono congelati prima della valutazione; il meccanismo viene poi replicato su nuovi run dello stesso simulatore e degli stessi quattro guasti.

La frase di novità più prudente resta: *“To the best of our knowledge, this is the first controlled study of federated textual knowledge transfer for locally unseen fault diagnosis in multivariate industrial time series.”*

**Step 2 / 28(St.1)**

## Dataset

Il **Tennessee Eastman Process** è un impianto chimico simulato. Il suo simulatore fornisce segnali multivariati, fault noti, run replicabili e un istante di attivazione del guasto verificato a **10 h**: è quindi un ottimo banco di prova, con una **ground truth controllabile** che il dominio fotovoltaico reale non offre. La pipeline legge da ogni file `Time` più **41 variabili misurate XMEAS**.

Nel progetto si usano due tipi di dato:

- **Dataset Normal** — un solo file di processo *senza fault*, lungo **500 h**, con **30001 righe** (500 h × 60 = 30000 campioni, più la riga di endpoint a 500 h). Campionamento **1 minuto** (`1/60 h`). L'ultima riga (l'endpoint) viene **esclusa** dai blocchi: 30000 righe si dividono esattamente in 10 blocchi da 50 h, mentre la 30001ª cadrebbe fuori dalla suddivisione uniforme. 41 XMEAS per riga.
- **Dataset di fault** — i quattro fault studiati sono **F1, F8, F10, F13**. Ogni file è un run (batch) da **50 h**, **3001 righe** (50 h × 60 + endpoint), campionamento 1 minuto, 41 XMEAS. Il fault è iniettato a 10 h, quindi le prime 10 h sono processo nominale e le 40 h successive contengono la firma del guasto.

> **Perché proprio F1, F8, F10, F13?**
>
> Il TEP definisce 21 tipi di fault raggruppati per meccanismo fisico nella tassonomia originale di Downs & Vogel (1993): **Step** (F1–F7), **Random variation** (F8–F12), **Slow drift** (F13 unico), **Sticking** (F14–F15) e **Unknown** (F16–F20), più il guasto a valvola fissa F21.
>
> La scelta dei quattro fault segue un **criterio di copertura dei meccanismi**. All'interno di ciascuna categoria il meccanismo generativo è lo stesso e cambiano solo la variabile colpita e l'ampiezza; selezionare più fault dalla stessa famiglia (ad esempio F1 e F4, entrambi step) avrebbe introdotto ridondanza senza aggiungere diversità strutturale. Servono invece rappresentanti di famiglie distinte:
>
> - **F1** — rappresentante della famiglia *Step*: perturbazione istantanea e persistente.
> - **F8** — rappresentante della famiglia *Random variation*: disturbo stocastico continuo.
> - **F10** — secondo *Random variation*, scelto per creare una coppia intra-famiglia (F8 vs F10) che testa la capacità del metodo di distinguere fault con lo stesso meccanismo ma variabile-target diversa.
> - **F13** — **unico** fault di tipo *Slow drift* nel TEP: la sua inclusione è obbligata se si vuole coprire la deriva lenta, e rappresenta il caso diagnosticamente più difficile (la firma emerge gradualmente e si sovrappone a lungo al processo nominale).
>
> Restano esclusi: F16–F20 (*Unknown*), la cui mancanza di un meccanismo documentato li rende inadatti a uno studio che richiede ground truth interpretabile; F14–F15 (*Sticking*), meccanismo ridondante rispetto allo *Step* sul piano della firma statica; F21 (*Fixed valve*), caso a sé fuori dalla tassonomia a cinque famiglie.
>
> La combinazione risultante {F1, F8, F10, F13} copre tre dei cinque meccanismi documentati e crea tre assi di contrasto complementari: *step vs random* (F1 vs F8), *intra-famiglia random* (F8 vs F10) e *drift lento vs perturbazioni rapide* (F13 vs tutti gli altri). L'analisi quantitativa delle firme a 697 dimensioni conferma a posteriori che i quattro fault campionano lo spettro di difficoltà diagnostica:
>
> | Fault | Meccanismo | Similarità intra-classe | Margine dal Normal | Nota |
> |-------|------------|------------------------|--------------------|------|
> | F1 | Step | 0.991 | 0.077 | Firma stabile, ben separata |
> | F10 | Random var. | 0.991 | 0.011 | Stabile ma quasi sovrapposta a F1 (inter-class 0.905) |
> | F8 | Random var. | 0.860 | 0.014 | La meno stabile: massima variabilità intra-classe |
> | F13 | Slow drift | 0.889 | 0.044 | Minima similarità col Normal (0.718), drift graduale |

I file di fault contengono anche **12 variabili manipolate XMV** (le grandezze che l'operatore può controllare). Vengono **escluse** dalla rappresentazione: il layer Stadio 1 è stato definito sulle sole XMEAS e congelato così; aggiungere le XMV dopo aver osservato i dati cambierebbe la rappresentazione a valle del freeze. La pipeline conserva quindi soltanto `Time` + 41 XMEAS.

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

**Step 3 / 28(St.1)**

## Analisi e split dei dataset

Il dataset Normal è un file da 500 h, diviso in **10 blocchi da 50 h** (N1…N10); ogni blocco Ni viene ulteriormente suddiviso in **10 finestre da 5 h** (N1-f1, N1-f2, …). Il campionamento è un minuto, cioè `1/60 h`. I file di fault sono quattro: **F1, F8, F10, F13**; ogni run dura 50 h: le prime 10 h precedono l'attivazione e le 40 h successive producono **8 finestre da 5 h**. Una finestra è una porzione descrittiva dello stesso run, non una replica fisica: questa distinzione tornerà cruciale allo Step finale, quando conteremo i casi statisticamente indipendenti.

Nel caso con fault, le otto finestre post-fault sono indicate come **W1–W8**, rispettivamente da `[10,15)` a `[45,50)` h. Il calcolo delle feature viene eseguito separatamente su ciascuna finestra e su ciascuna delle 41 XMEAS, usando ogni volta i dati grezzi della finestra corrente. Le finestre dei blocchi Normal mantengono invece la propria numerazione (per esempio N1-f1, N1-f2, …) e seguono la stessa logica di calcolo sulle rispettive porzioni da 5 h.

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

**Step 4 / 28(St.1)Design / development-time**

## La pipeline di Stadio 1: le sei operazioni

Di seguito le fasi svolte dalla pipeline della fase A del progetto.

| Ordine | Fase | Quando e che cosa produce |
| --- | --- | --- |
| 1 | **Scelta delle feature** | Decisione di design, eseguita una volta. Si caratterizzano i **fault batch 1–5** per decidere *quali* feature usare (shift, slope, residual, diff); qui **non** si calcolano soglie. |
| 2 | **Calibrazione delle soglie** | Eseguita **soltanto sui blocchi Normal N1–N5**, senza mai guardare i fault; produce baseline e soglie. I fault influenzano *quali* feature, non il *valore* delle soglie. |
| 3 | **Freeze** | Congela feature, baseline, soglie, struttura e renderer. Avviene dopo la calibrazione; da qui in avanti le regole si applicano soltanto, non si ridefiniscono. |
| 4 | **Calcolo delle feature e applicazione delle soglie** | A runtime, per ogni finestra × XMEAS, calcola i **valori delle feature** e li confronta con le soglie già congelate (flag 0/1). |
| 5 | **Dalle finestre al JSON** | Aggrega flag e struttura temporale in evidenza numerica auditabile. |
| 6 | **Dal JSON al testo neutrale** | Renderizza fatti quantitativi senza fault ID o diagnosi automatica. |

**Step 5 / 28(St.1)Design / development-time**

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

**Step 6 / 28(St.1)Design / development-time**

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

**Step 7 / 28(St.1)Design / development-time**

## Il freeze: congelare feature, soglie e renderer

Prima di aprire validation, test e held-out vengono congelati feature, soglie, rappresentazione temporale, renderer ed evaluator. È il principio *freeze-before-test*: nessun dato di valutazione può più influenzare le regole con cui verrà giudicato. In questo modo si evita il **leakage** — cioè che osservare i risultati porti, anche inconsapevolmente, a riscrivere feature o soglie per farle combaciare con i casi da valutare. Da qui in avanti quelle regole si possono soltanto applicare, non ridefinire.

> **Che cosa è stato usato fino a qui.** Fino al freeze sono entrati in gioco soltanto i blocchi **Normal N1–N5** (per calibrare le soglie) e i **fault batch 1–5**. Questi ultimi sono stati usati **solo in fase di design/development, per scegliere *quali* feature usare** — non per calcolare le soglie e non a runtime. La scelta delle feature è una decisione fatta una volta, a monte, non un'operazione ripetuta su ogni caso. I restanti dati — **N6–N10** e i **fault batch 6–10** — **non sono ancora stati toccati**: entreranno solo dopo il freeze, in validation e test. (N1–N5 servono in due momenti: a design-time per calibrare le soglie e poi come baseline di riferimento anche a runtime.)

**Step 8 / 28(St.1)Runtime / finestra × XMEAS**

## Dalle feature ai flag: soglie e segni

Per ogni finestra (le **8** del caso con fault) e per ogni variabile **XMEAS** (le **41**) vengono applicate le soglie: se il valore della feature è maggiore della soglia — ricordiamo che la soglia è stata calibrata sui **Normal** — viene generato un **flag** (attivo/non attivo) e, per le feature con segno (shift, slope), il relativo **segno**. Vediamo il calcolo reale su una singola finestra: F1 batch 1, XMEAS-1, W1. (Caso development/calibration, non test indipendente; non usa LOBO. W1 è `[10,15)` h: 5 h × 60 = 300 misure.)

W1 è mostrata esclusivamente come esempio di calcolo. Nella pipeline completa, lo stesso procedimento viene ripetuto per ciascuna finestra del run — W1–W8 nei casi con fault — e per ciascuna delle 41 XMEAS, utilizzando ogni volta i dati della finestra corrente; la baseline Normal e le soglie congelate restano riferimenti distinti.

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

**Step 9 / 28(St.1)Runtime / caso completo**

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

**Step 10 / 28(St.1)Controllo offline**

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
> > **A cosa serve.** Alta similarità intra-classe + bassa similarità inter-classe = il testo neutrale di Stadio 1 conserva abbastanza struttura da distinguere le condizioni *senza mai nominarle*. È il pre-requisito descrittivo che rende sensato, nello step successivo, dare quei testi in pasto a un reasoner in Stadio 2 — ma resta separabilità, non ancora accuracy diagnostica.

**Step 11 / 28(St.1)Valutazione out-of-development/calibration**

## Validation e test split: applicare dopo il freeze

La progettazione si è terminata con il freeze; adesso si esegue la stessa pipeline runtime prima sulla validation (fault batch 6–7 e Normal N6–N7) e poi sul test split (batch 8–10 e N8–N10). In entrambi i casi il percorso è sempre `finestre → feature → soglie congelate → JSON → testo neutrale → evaluator`. È importante notare come lo split «development/calibration» sia utilizzato per progettare e calibrare, in seguito al freeze la validation è utilizzata per effettuare controlli intermedi e alla fine il test split resta chiuso fino alla verifica finale di Stadio 1.

**Step 12 / 28(St.1)Confine sperimentale**

## Nuove simulazioni indipendenti

I batch 8–10 del test split erano test di Stadio 1, ma sono stati aperti. Un test osservato non è più vergine per Stadio 2. La catena è: test split visto → non può essere nuovo test indipendente → servono run nuovi → vanno congelati prima di verbalizzazione e inference. Un test indipendente e congelato prima dell'inferenza serve proprio a questo: impedisce il leakage da riuso di uno split già osservato e offre una misura non distorta della generalizzazione, senza che il test possa ricalibrare soglie o insight (nessun overfitting al set di valutazione). Questi 15 run congelati sono il materiale su cui si aprirà **Stadio 2** (dal prossimo step): fin qui — Step 4–12 — siamo rimasti dentro Stadio 1.

15 nuove realizzazioni simulate = 3 Normali + 3 run per ciascun fault

| Normal | F1 | F8 | F10 | F13 |
| --- | --- | --- | --- | --- |
| 3 run | 3 run | 3 run | 3 run | 3 run |

**Step 13 / 28(St.2)Stadio 2 / conoscenza locale**

## Agenti non-IID, pseudolabel ed esempi locali

> **Inizia Stadio 2.** Finora (Step 4–12) siamo rimasti in Stadio 1: pipeline deterministica, soglie calibrate e congelate, nessun LLM. Da qui entrano in gioco gli agenti, il reasoner e la federazione. La pipeline Stadio 1 non viene ri-progettata: gli agenti la *riusano* così com'è, applicando baseline e soglie congelate senza mai ricalibrarle.

Quattro agenti conoscono tutti il Normal ma ciascuno un solo fault. Ogni agente riceve due esempi del proprio fault (batch 1–2) e gli stessi due Normal (N1–N2).

Distribuzione non-IID: ogni agente conosce solo il proprio fault

| Agente A | Agente B | Agente C | Agente D |
| --- | --- | --- | --- |
| 2 Normali + 2 esempi da F1 | 2 Normali + 2 esempi da F8 | 2 Normali + 2 esempi da F10 | 2 Normali + 2 esempi da F13 |

> **Da dove vengono i dati.** Attenzione a non confondere tre cose distinte: gli **esempi** del few-shot sono batch 1–2 di fault e Normal N1–N2 dal **TEP originale** (gli stessi workbook di Stadio 1), non i run indipendenti; il **caso da diagnosticare** sarà invece un run del **held-out indipendente** — i 15 PBH dello Step 12 — e comparirà solo all'inferenza (Step 16); le **soglie** restano quelle calibrate in Stadio 1 sul TEP originale (Normal N1–N5), congelate e mai ricalcolate.

> Prima operazione di Stadio 2 · il few-shot locale
>
> ### Ogni agente costruisce i propri esempi few-shot
>
> La prima cosa che fa ogni agente è preparare il proprio **few-shot locale**: prende i casi che conosce (i suoi batch 1–2 di fault e i Normal N1–N2), li fa passare per la pipeline Stadio 1 già congelata e ne ricava esempi pronti da mostrare al reasoner. Non è materiale che «compare» già pronto: viene ricostruito dai workbook, senza LLM e senza ricalibrare nulla. Il ramo few-shot usa batch 1–2; il ramo insight dello step successivo riparte separatamente dai batch 1–5.
>
> | Passaggio | Che cosa accade realmente |
> | --- | --- |
> | **Input dei casi** | Per ciascun agente: i workbook fissi batch 1–2 del proprio fault locale e i blocchi Normal N1–N2. La baseline development/calibration N1–N5 resta il riferimento frozen. |
> | **Operazione** | Con questi input, l'agente riesegue la pipeline Stadio 1 congelata (`finestre → feature → soglie già congelate → flag → JSON → testo neutrale`) e associa a ogni caso la sua **pseudolabel** — un'etichetta opaca che nasconde il nome reale del fault (spiegata in dettaglio qui sotto). Nessun LLM, nessuna ricalibrazione delle soglie. |
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

**Step 14 / 28(St.2)Stadio 2 / federazione**

## Gli insight distillano più casi; la federazione li distribuisce peer-only

Dopo il few-shot, ogni agente compie una seconda operazione: condensa ciò che sa del proprio fault in due brevi osservazioni testuali, gli **insight**. Per farlo riparte dai cinque casi development/calibration del fault locale (batch 1–5, dati TEP originali già usati in Stadio 1), li fa passare per la stessa pipeline congelata ottenendone i testi neutrali e chiede all'LLM di distillarne le regolarità ricorrenti: **2 insight per agente, 8 in totale**. Questo è un ramo distinto dal few-shot dello Step 13: non usa come input il file degli esempi locali. Tutto avviene **prima di aprire diagnosticamente** i 15 run indipendenti dello Step 12, già generati e congelati: gli insight nascono soltanto da ciò che l'agente conosceva già. Infine avviene la **federazione**: ogni agente riceve i sei insight degli altri tre peer — mai i propri — così la conoscenza circola come testo, senza scambiare dati grezzi né parametri del modello.

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

**Step 15 / 28(St.2)Stadio 2 / protocollo frozen**

## Configurazioni informative controllate e struttura completa dell'inference

Una **configurazione informativa** è una versione controllata dello stesso agent-case: neutral text held-out e few-shot locali restano identici, mentre cambia una sola variabile sperimentale, il blocco degli insight peer. In questo modo la differenza tra configurazioni informative non può essere attribuita a un workbook diverso o a esempi locali diversi.

> Disegno A/B/E frozen
>
> ### Che cosa cambia davvero
>
> | Configurazione informativa | Input oltre ai few-shot locali | Domanda controllata |
> | --- | --- | --- |
> | **A — isolated** | Nessun insight — né peer né propri: soltanto i 4 few-shot locali. | Qual è l'information floor senza insight per le classi locally-unseen? |
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

> **Cronologia del protocollo.** Condition C non faceva parte del protocollo originale A/B/E: è stata progettata post-hoc dopo l'osservazione dei risultati A/B/E. Ha però avuto un proprio amendment e un proprio freeze, entrambi completati prima delle sue chiamate LLM. Il carattere post-hoc riguarda quindi la scelta di introdurre il confronto, non una modifica delle predizioni dopo averne osservato gli esiti.

**Step 16 / 28(St.2)Stadio 2 / inference frozen**

## Dal testo neutrale alla decisione: PBH-004 visto da Agent 3

Finora abbiamo definito le tre configurazioni informative. Vediamo ora che cosa accade realmente allo stesso caso quando attraversa A, B ed E. PBH-004 è un nuovo run held-out di F1 (`mode1_1_11.xlsx`), ma questa identità è conosciuta soltanto dall'evaluator. La pipeline congelata trasforma il workbook nel suo testo neutrale; quel testo viene poi presentato ad Agent 3, che possiede esempi locali di F10 e per il quale F1 è quindi una classe *unseen*. Il caso, i few-shot, il modello e il prompt restano gli stessi: cambia soltanto il blocco degli insight peer.

Il testo neutrale di PBH-004 segnala XMEAS-1 sopra la soglia di spostamento in 8/8 finestre, sempre positivo, con dispersione massima 47.00: la firma di F1, osservata però su un run mai visto.

PBH-004 → → → pipeline Stadio 1 congelata → → → testo neutrale → → → Agent 3 → → → A / B / E → → → tre esiti aggregati → → → ground truth ancora chiusa

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

**Step 17 / 28(St.2)Ground-truth evaluation**

## Risultati Stadio 2: trasferimento di conoscenza sui fault localmente unseen

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

Il risultato principale dello Stadio 2 riguarda i fault localmente unseen: vogliamo sapere se gli insight peer permettono al receiving agent di riconoscere condizioni che non possiede nella propria conoscenza locale. Un trasferimento utile, però, non dovrebbe essere valutato soltanto su ciò che l'agente non conosce: è importante controllare anche che cosa accade ai casi che sa già riconoscere.

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

Questa decomposizione unanimous/split è una derivazione descrittiva post-hoc dei repetition records frozen. Non era uno degli endpoint utilizzati per giudicare il successo primario dello Stadio 2.

Il fatto che 33/36 decisioni unseen di B siano unanimi indica che, nel setup frozen osservato, la maggior parte delle decisioni aggregate deriva da tre chiamate concordi. È un descrittore della **stabilità delle decisioni tra le tre chiamate R=3**, non una misura generale di robustezza. Le chiamate usano lo stesso input e la stessa configurazione: il risultato non dimostra stabilità rispetto a perturbazioni dei dati, prompt diversi, altri modelli, altre configurazioni di reasoning o distribuzioni differenti.

**Riferimento aggiunto successivamente.** Condition C è stata applicata post-hoc esclusivamente al medesimo held-out di Experiment 1, con una predizione centralizzata per ciascuno dei 15 casi. Non è parte dei contrasti originali A/B/E e non è stata applicata a EXP3_V2; design e risultati sono documentati negli Step 25–26.

> **Come leggere questi controlli.** Il primary result mostra il trasferimento sui fault localmente unseen. I secondary outcome mostrano che, nel campione osservato, questo beneficio non è accompagnato da una degradazione visibile sui casi local-seen o Normal. La verifica R=3 aggiunge un'informazione diversa: descrive quanto le tre chiamate concordano tra loro. Nessuno di questi controlli amplia il risultato oltre il setup TEP studiato.

### 6 · Scope and limitations

- TEP è una POC metodologica controllata; il fotovoltaico è il dominio-obiettivo finale.
- A è una baseline senza insight e un information floor per la semantica delle classi locally-unseen; una vera local-only includerebbe gli insight propri e non è stata implementata come condizione separata.
- Riconoscimento in spazio di pseudolabel chiuso, non diagnosi open-world.
- Solo 12 cluster indipendenti.
- Un solo simulatore/processo.
- Una sola configurazione LLM/reasoning.
- Nessuna garanzia formale di privacy.
- Il riferimento centralizzato C, aggiunto post-hoc, differisce da B per quantità e forma dell'informazione; C−B è descrittivo e non causale.
- Nessuna claim di generalizzazione al PV o cross-domain.
- harmed=0 non è evidenza di assenza generale di negative transfer.

### 7 · Claim finale

> Nel protocollo frozen e sui 12 run fisici di fault del nuovo held-out TEP, gli insight peer autentici hanno aumentato l'accuratezza sui fault localmente unseen da **0/36 (A) a 31/36 (B)**; il contrasto primario **B−A è +0.8611 [0.8333, 0.9167]**. A parità di testi, ID, ordine e volume del peer block, la corruzione delle associazioni ha ridotto l'accuratezza a **3/36**: *il contrasto B−E supporta l'interpretazione che il beneficio osservato dipenda dalla corretta associazione dell'informazione trasferita, anziché dalla mera presenza o dal volume del testo aggiuntivo* (B−E +0.7778 [0.7222, 0.8333]). *La configurazione informativa A rappresenta uno scenario di limite informativo per la semantica delle classi localmente unseen, perché l'agente ricevente non dispone di alcun esempio locale della pseudoclasse corrispondente*; la magnitudine di B−A va quindi letta rispetto a questo floor. Questi risultati supportano la **feasibility** del trasferimento testuale federato di conoscenza discriminante tra agenti su serie temporali multivariate eterogenee nel setup TEP studiato; non dimostrano generalizzazione cross-domain o al fotovoltaico e non forniscono garanzie di privacy. Condition C, documentata negli Step 25–26, è un riferimento centralizzato post-hoc sullo stesso held-out, entro lo stesso paradigma testuale e con un contesto informativo diverso da B.

Fase 2 — Replica confirmatory · EXP3_V2

**Dalla Fase 1 alla Fase 2.** Lo Step 17 ha mostrato che, su 12 run fisici held-out, gli insight FoT autentici hanno portato l'accuratezza unseen da 0/36 (A) a 31/36 (B), con un contrasto B−A di +0.861 [0.833, 0.917]. Ma quel risultato poggia su un singolo campione held-out di 12 run fisici. La domanda che apre la Fase 2 è: *il fenomeno si riproduce su nuove realizzazioni indipendenti delle stesse classi?*

Tutto il metodo — feature, soglie, agenti, insight, configurazioni informative, protocollo frozen — rimane identico. Cambiano solo i dati fisici sottostanti: 24 nuovi run di fault (6 per classe) e 6 nuovi run Normal, il doppio della Fase 1. L'architettura sperimentale e le decisioni di analisi sono state congelate *prima* di generare questi dati.

**Step 18 / 28Fase 2Esperimento confermativo su nuove realizzazioni simulate**

## Esperimento confermativo su nuove realizzazioni simulate

Un held-out, per definizione, può essere aperto una sola volta: dopo che i risultati di Experiment 1 sono stati osservati, quei dati non sono più vergini rispetto all'ipotesi. Non è quindi possibile riusarli per rispondere alla domanda *«il risultato regge su realizzazioni fisiche diverse?»* senza introdurre un rischio di conferma post-hoc.

Il rischio specifico da escludere non è il data leakage classico — il protocollo frozen lo controlla già — ma che le dodici realizzazioni fisiche del held-out di Experiment 1 abbiano caratteristiche idiosincratiche (pattern di rumore, transitori, derive di sensore) che hanno favorito il trasferimento in quel campione particolare, senza che il fenomeno sia riproducibile su run indipendenti delle stesse classi.

Le nuove realizzazioni fisiche sono run TEP indipendenti delle stesse quattro classi — non reruns dei file già usati, non nuove classi, non un dominio diverso. Il perimetro sperimentale rimane deliberatamente invariato: il metodo, gli agenti, le soglie e il protocollo frozen di Experiment 1 vengono riapplicati as-is alle nuove realizzazioni. L'obiettivo non è la generalizzazione, ma verificare se l'effetto osservato sia riproducibile quando i dati fisici cambiano pur restando fisso tutto il resto.

**Step 19 / 28Fase 2Nuovo held-out**

## Le nuove realizzazioni fisiche di EXP3_V2

Per costruire il nuovo held-out sono stati generati run TEP indipendenti degli stessi quattro tipi di guasto studiati in Experiment 1, più i casi Normal. I run sono stati congelati prima di qualsiasi inferenza, applicando la stessa logica freeze-before-test che ha governato la Fase 1: nessun dato del nuovo held-out ha influenzato feature, soglie, agenti o insight, che restano quelli di Experiment 1 senza ricalibrazione.

30 nuove realizzazioni simulate = 6 Normali + 6 run per ciascun fault

| Normal | F1 | F8 | F10 | F13 |
| --- | --- | --- | --- | --- |
| 6 run | 6 run | 6 run | 6 run | 6 run |

Il raddoppio rispetto ai 15 run di Experiment 1 (3 per classe) porta a 72 agent-case unseen, aumentando la potenza statistica del contrasto primario B−A senza modificare il disegno sperimentale.

**Step 20 / 28Fase 2Disegno confirmatory frozen**

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
> | **A — isolated** | Nessun insight — né peer né propri: solo few-shot etichettati locali. Misura la performance senza alcuna federazione e senza insight. |
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

**Step 21 / 28Fase 2**

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

**Step 22 / 28Fase 2**

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

**Step 23 / 28Fase 2**

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

**Step 24 / 28Fase 2Interpretazione, limiti e provenienza frozen**

## Che cosa supporta la replica, e che cosa non dimostra

### 1 · Scope and limitations

- TEP è una POC metodologica controllata; il fotovoltaico è il dominio-obiettivo finale.
- A è una baseline senza insight e un information floor per la semantica delle classi locally-unseen; una vera local-only includerebbe gli insight propri e non è stata implementata come condizione separata.
- Riconoscimento in spazio di pseudolabel chiuso, non diagnosi open-world.
- 24 cluster indipendenti (il doppio di Experiment 1, ma pur sempre un campione limitato).
- Un solo simulatore/processo (TEP).
- Una sola configurazione LLM/reasoning (`gpt-5.6-terra`, reasoning `medium`).
- Nessuna garanzia formale di privacy.
- EXP3_V2 non comprende una propria baseline centralized pooled. Condition C degli Step 25–26 non è stata eseguita sulle realizzazioni EXP3_V2 e non colma quindi questo gap della Fase 2.
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
> Questi risultati supportano la **feasibility** e la **riproducibilità** del trasferimento testuale federato di conoscenza discriminante tra agenti su serie temporali multivariate eterogenee nel setup TEP studiato; non dimostrano generalizzazione cross-domain o al fotovoltaico e non forniscono garanzie di privacy. EXP3_V2 resta privo di un proprio comparatore centralized pooled: il riferimento centralizzato C non è stato eseguito su queste realizzazioni.

> **Transizione cronologica.** Il blocco seguente è collocato dopo la Fase 2 perché Condition C è stata introdotta successivamente nella cronologia del progetto. Gli Step 25–26 riaprono però il confronto di **Experiment 1**: usano il suo medesimo held-out e non i run EXP3_V2.

**Step 25 / 28Federazione VS centralizzazione**

## Federazione e riferimento centralizzato

Abbiamo chiesto: quanto perde il sistema a quattro agenti rispetto a uno solo che sa tutto? Per rispondere abbiamo costruito un agente unico a cui abbiamo dato tutte le conoscenze degli altri quattro — gli stessi esempi, le stesse descrizioni testuali dei guasti. Non dati grezzi o informazioni riservate, solo ciò che nella federazione verrebbe scambiato tra i nodi. Il confronto è diretto perché entrambi lavorano con lo stesso tipo di materiale, ma non alla pari: l'agente centralizzato vede tutto insieme, quelli federati vedono solo pezzi.

**Full-information** è qui circoscritto all'unione degli artefatti prompt-facing frozen — esempi etichettati e insight testuali — e non implica accesso ai dati grezzi, ai testi sorgente, alla ground truth o a informazione evaluator-side.

> C e B: contesti diversi entro lo stesso paradigma
>
> ### Che cosa vede ciascun ricevente
>
> | Condizione | Esempi etichettati | Insight | Forma del contesto |
> | --- | --- | --- | --- |
> | **C** | 10 pooled: 2 per ciascuna delle 4 classi fault + 2 Normal | 8, inclusi quelli che in B sarebbero propri | Unico contesto centralizzato, receiver-independent |
> | **B** | 4 locali per receiving agent: 2 del fault noto + 2 Normal | 6 peer | Contesto diverso per ciascun receiving agent |
>
> Da dove vengono i 10 esempi di C? Ogni agente ha il suo pacchetto di esempi etichettati (LKP-001…LKP-004). Per C si prendono tutti e quattro i pacchetti e si fondono in un unico mazzo. Siccome gli esempi Normal sono gli stessi in ogni pacchetto, dopo la deduplicazione restano **10 esempi**: 2 per ognuno dei 4 guasti + 2 Normal, ordinati per `example_id`. Lo **schedule frozen** è una cosa separata: governa **quali casi sottoporre al modello e in che ordine** (15 casi × 3 ripetizioni = 45 chiamate), ma non ha nessun ruolo nella selezione degli esempi pooled — quelli derivano meccanicamente dall'unione dei pacchetti.

C classifica i **15 casi del held-out di Experiment 1** (12 fault + 3 Normal), ciascuno R=3: 45 provider records e 15 decisioni aggregate. C e B differiscono sia nella quantità sia nella forma dell'informazione; di conseguenza C−B è un confronto **descrittivo e non causale**, entro lo stesso paradigma testuale.

### Configurazione frozen e guardrail

- Modello `gpt-5.6-terra` e reasoning effort `medium`, frozen e coerenti nei 45 record.
- `temperature=null` e `seed=null`.
- R=3, structured output strict e inferenza stateless.
- Nessun accesso alla ground truth prima del freeze delle predizioni; join soltanto evaluator-side.

**Step 26 / 28Risultati C e confronto descrittivo C−B**

## Risultati del riferimento centralizzato e distanza descrittiva da B

Condition C ha classificato correttamente tutte le 15 decisioni aggregate, senza astensioni. **Per ciascuno dei 15 casi, le tre ripetizioni hanno prodotto la stessa decisione aggregabile.**

| Scope | Corretti / casi | Accuratezza | Astensioni |
| --- | --- | --- | --- |
| **Fault** | 12 / 12 | 100.0% | 0 |
| **Normal** | 3 / 3 | 100.0% | 0 |
| **Overall** | 15 / 15 | 100.0% | 0 |

### 1 · Delta paired C−B sui 12 casi fault

Per ciascun caso *i*, C contribuisce una decisione e B la media delle decisioni dei tre receiving agents per cui quel fault è unseen:

`Δ_(C−B) = (1/12) Σ_i=1^12 [1(C_i=y_i) − (1/|U_i|) Σ_(a∈U_i) 1(B_ia=y_i)]`, con `|U_i|=3`.

| Caso | Fault reale | Pseudolabel | C | B (3 unseen) | δ_i |
| --- | --- | --- | --- | --- | --- |
| PBH-004 | F1 | CLS-ZOGAA | ✓ | 3/3 | 0.000 |
| PBH-005 | F1 | CLS-ZOGAA | ✓ | 3/3 | 0.000 |
| PBH-006 | F1 | CLS-ZOGAA | ✓ | 3/3 | 0.000 |
| PBH-007 | F8 | CLS-OJNSG | ✓ | 1/3 | **0.667** |
| PBH-008 | F8 | CLS-OJNSG | ✓ | 2/3 | **0.333** |
| PBH-009 | F8 | CLS-OJNSG | ✓ | 1/3 | **0.667** |
| PBH-010 | F10 | CLS-R463B | ✓ | 3/3 | 0.000 |
| PBH-011 | F10 | CLS-R463B | ✓ | 3/3 | 0.000 |
| PBH-012 | F10 | CLS-R463B | ✓ | 3/3 | 0.000 |
| PBH-013 | F13 | CLS-Z3ISU | ✓ | 3/3 | 0.000 |
| PBH-014 | F13 | CLS-Z3ISU | ✓ | 3/3 | 0.000 |
| PBH-015 | F13 | CLS-Z3ISU | ✓ | 3/3 | 0.000 |

**Delta C−B:** 5/36 = **0.138889**. **Bootstrap percentile 95%:** [0.083333, 0.166667], 10.000 draw, seed 20260906.

> **Limitazione principale.** L'intero vantaggio C−B è concentrato nei tre casi CLS-OJNSG/F8; per gli altri nove casi fault il delta è zero. Il bootstrap è stratificato su 4 classi × 3 cluster e la sua distribuzione occupa una griglia discreta di soli cinque valori. Con tre cluster per strato ha risoluzione effettiva minima: il CI è corretto, ma non supporta una conclusione generale sulla centralizzazione.

### 2 · Interpretazione e provenienza

C è una **centralized full-information pooled ICL post-hoc exploratory reference**: colloca B entro lo stesso paradigma testuale, ma quantità, forma e struttura del contesto cambiano simultaneamente. Il risultato è descrittivo, temporalmente confondibile e non autorizza una lettura causale o una superiorità generale.

Fonti canoniche: [`evaluation_results_c.json`](../icl/full_evaluation/evaluation_results_c.json), [`PLAN_CENTRAL_POOLED_ICL.md`](../icl/PLAN_CENTRAL_POOLED_ICL.md) e [`CONDITION_C_R10_INDEPENDENT_REVIEW.md`](audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md).

Fase 3 — Portabilità cross-model · EXP2

**Dal riferimento centralizzato alla Fase 3.** Experiment 1 ha stabilito l’effetto di trasferimento e la sua specificità semantica; Experiment 3 (Fase 2) lo ha replicato su realizzazioni fisiche indipendenti; Condition C ha poi fornito un riferimento post-hoc sul solo held-out di Experiment 1. EXP2 ha ora esaminato la portabilità lato consumer: gli insight prodotti da `gpt-5.6-terra` sono stati consumati da Qwen nella configurazione frozen, con risultati congelati e sottoposti a review indipendente.

**Step 27 / 28Fase 3Portabilità cross-model**

## Consumer open-weight: risultati di Experiment 2

### 1 · Domanda scientifica

Experiment 2 verifica se gli stessi insight testuali frozen, prodotti da `gpt-5.6-terra`, possono essere consumati utilmente da un reasoner diverso. La distinzione chiave è tra **producer** e **consumer**:

- il **producer** — il modello che ha generato gli insight — rimane `gpt-5.6-terra` e non viene variato: gli insight peer restano quelli frozen di Experiment 1, byte per byte;
- il **consumer** — il modello che riceve il caso da classificare e gli insight federati e deve produrre la diagnosi — cambia: al posto di `gpt-5.6-terra` viene utilizzato un modello open-weight locale.

La claim riguarda la **portabilità del consumo**, non la generalità end-to-end: il producer degli insight non è stato cambiato. Experiment 2 è complementare a Experiment 3 (Fase 2): là cambiavano i dati fisici a parità di reasoner, qui cambia il reasoner a parità di dati e conoscenza. La scelta di un modello open-weight serve anche da ancora di riproducibilità: un risultato replicabile con pesi pubblici e inferenza deterministica è più difficile da contestare di uno ottenuto esclusivamente con API proprietarie.

### 2 · Setup sperimentale

Tutti gli elementi sperimentali di Experiment 1 sono mantenuti identici: held-out (15 run), insight peer, prompt template, schedule, derangement della condizione E, aggregazione 2-su-3, evaluator. Questo rende il cambio di consumer l'unica variabile, ma il confronto cross-model resta descrittivo.

Il consumer è **Qwen3.8-27B-FP8** (Qwen 27B), un modello open-weight da 27 miliardi di parametri, servito localmente tramite **vLLM** su GPU NVIDIA RTX 5000 Ada. L'inferenza avviene interamente su hardware locale, senza chiamate a servizi cloud.

Lo schedule produce: 15 casi × 4 agenti × 3 condizioni × 3 ripetizioni = **540 inferenze** e **180 decisioni aggregate**. Con `temperature=0` e seed fisso, le tre ripetizioni risultano byte-identiche per tutti i 180 aggregati: `R=3` è degenere e il majority vote non misura variabilità stocastica.

Il protocollo è stato sottoposto a capability probe e audit indipendente prima del freeze. Il probe iniziale ha rivelato un problema di troncamento del reasoning nella condizione E (budget di 512 token insufficiente), corretto portando `max_tokens` a 1536 e introducendo un `thinking_token_budget` di 1024. Il re-audit ha emesso **GO per il freeze**.

### 3 · Risultati

**Risultati primari locally-unseen** (36 agent-case per configurazione):

| Configurazione | Corrette | Accuracy |
| --- | ---: | ---: |
| A — isolated | 0/36 | 0% |
| B — FoT | 34/36 | 94.44% |
| E — corrupted | 1/36 | 2.78% |

- **B−A = +0.944**, CI bootstrap 95% [0.917, 1.0]
- **B−E = +0.917**, CI bootstrap 95% [0.833, 1.0]
- 34 helped, 0 harmed, 2 unchanged-incorrect
- Zero astensioni; criteri primari C1–C4: **4/4 PASS**

**Risultati secondari:**

| Popolazione | A | B | E |
| --- | ---: | ---: | ---: |
| local-seen | 100% | 75% | 100% |
| Normal | 100% | 100% | 100% |
| overall | 40% | 91.67% | 41.67% |

Il verdetto della review scientifica indipendente è **GO WITH LIMITATIONS**.

### 4 · Reasoning cap e cautela su H2

Il limite effettivo del reasoning nella configurazione frozen è **1023 token** (budget nominale 1024). Tutti e cinque gli errori aggregati di B avevano le tre ripetizioni al cap; al contrario, tutti i 36 aggregati B non cappati erano corretti. Questa coincidenza rendeva ambiguo il fallimento di H2: un errore poteva dipendere dagli insight peer, ma anche da un ragionamento interrotto troppo presto.

Per separare le due spiegazioni è stata eseguita una **sensitivity analysis deterministica e appaiata** sulle 60 osservazioni agent-case uniche della condizione B. Si usa `R=1`, perché le triplette frozen erano byte-identiche con temperatura 0 e seed fisso: il test misura l'effetto del budget, non la variabilità stocastica. L'anchor a 1024 riproduce 60/60 predizioni frozen e i controlli d'integrità sono `PASS`.

| Budget reasoning | Accuracy B | Local-seen | Unseen | Al cap | Nuove regressioni |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1024 | 91,67% | 75,00% | 94,44% | 24/60 | 0 |
| 1536 | 93,33% | 75,00% | 97,22% | 15/60 | 0 |
| 2048 | 95,00% | 83,33% | 97,22% | 10/60 | 0 |
| 3072 | 95,00% | 83,33% | 97,22% | 5/60 | 0 |

L'aumento del budget porta quindi B da 55/60 a 57/60 risposte corrette e riduce i casi al cap dal 40,0% all'8,3%, senza regressioni fra i 55 casi originariamente corretti. Il guadagno si arresta però dopo 2048: più spazio di ragionamento corregge alcuni errori, ma non tutti.

I cinque casi ancora capped a 3072 sono stati poi rieseguiti a 4096 in un **follow-up diagnostico post-hoc**. Due terminano sotto il limite; tre raggiungono ancora il cap, ma risultano tutti corretti. Fra i due errori presenti a 3072, `agent_3/PBH-009` viene corretto ma resta capped, mentre `agent_4/PBH-014` resta errato pur terminando sotto il limite. Non si osservano regressioni né parse failure. Questo sottoinsieme selezionato non permette di stimare l'accuracy globale a 4096.

La lettura causale deve rimanere prudente. `agent_3/PBH-008`, corretto e sotto il limite a 3072, è compatibile con troncatura del reasoning. `agent_4/PBH-014` e `agent_4/PBH-015`, ancora errati ma sotto il limite, rendono più plausibile interferenza o negative transfer, senza dimostrarla. Le correzioni di `agent_2/PBH-007` e `agent_3/PBH-009`, entrambe ancora capped a 4096, mostrano che il budget influenza la decisione, ma lasciano inconclusivo il meccanismo. In altre parole: **raggiungere il cap non implica essere errati**, e terminare sotto il cap non identifica da solo la causa dell'errore.

B ed E hanno lunghezza del prompt, consumo di reasoning e tasso di citazione degli insight comparabili. Il forte B−E costituisce evidenza di specificità rispetto al contenuto degli insight, ma non una prova causale definitiva.

### 5 · Limitazioni e conclusione

- È stato esaminato un solo consumer open-weight; un singolo consumer non dimostra generalità.
- Gli insight sono stati prodotti con `gpt-5.6-terra`: non è una replica end-to-end interamente open-weight.
- Sono stati riutilizzati gli stessi held-out case di Experiment 1; il confronto cross-model è descrittivo.
- Le ripetizioni deterministiche byte-identiche rendono `R=3` inidoneo a misurare variabilità.
- Il floor strutturale di A e la confusione `CLS-OJNSG` ↔ `CLS-Z3ISU` delimitano l'interpretazione; la sensitivity analysis riduce il confondimento del reasoning cap, ma non identifica causalmente ogni errore.

La conclusione prudente è che il vantaggio della configurazione federata B persiste su un secondo consumer LLM open-weight nella configurazione frozen esaminata. Il risultato mitiga la critica di dipendenza da un unico consumer proprietario, ma non dimostra portabilità universale, generalità cross-model o indipendenza end-to-end da un modello proprietario.

---

**Step 28 / 28**

## Ablation: confronto sistematico delle rappresentazioni TS→Testo

### 1 · Cosa fa l'esperimento, in parole semplici

Immagina un impianto chimico con 41 sensori che misurano temperature, pressioni, flussi. Quando qualcosa va storto (un guasto), i sensori cambiano comportamento. Il problema è: **come fai a dire a un modello linguistico cosa dicono quei sensori?** Il modello capisce il testo, non numeri grezzi di un impianto chimico.

Noi abbiamo testato 4 modi diversi di "tradurre" i dati dei sensori in testo:

- **V2_TEXT:** traduzione in italiano tecnico con giudizi ("il valore è sopra soglia, trend in crescita") — il nostro metodo
- **RAW_FEATURES:** numeri puri in tabella, senza interpretazione
- **CGTIME_STATS:** centinaia di statistiche calcolate per ogni sensore (media, varianza, correlazioni…)
- **SAX_SYMBOLIC:** lettere (tipo "aabccddee") che codificano la forma del segnale

L'idea è semplice: stesse condizioni, stesso modello, stessi casi di test — cambia solo come "parli" all'LLM. Chi funziona meglio?

Il protocollo è una classificazione centralizzata a 5 classi (F1, F8, F10, F13, Normal) su 15 casi held-out indipendenti (PBH-001…PBH-015), 3 ripetizioni per caso, GPT-5.6-terra con output strutturato. 4 bracci × 15 casi × 3 ripetizioni = **180 inferenze totali**.

| Braccio | Descrizione | Ispirazione | Token/prompt |
| --- | --- | --- | --- |
| **V2_TEXT** | Verbalizzatore conformal: 8 finestre × 5 feature per XMEAS, linguaggio naturale con soglie e trend | Il nostro metodo | ~550 |
| **RAW_FEATURES** | Serializzazione numerica diretta delle feature V2 in tabella | LLMTime (Gruver et al., 2023) | ~21 000 |
| **CGTIME_STATS** | 169 statistiche per sensore, 3 famiglie, window-aligned | CGTime (Feng et al., 2026) | ~99 000 |
| **SAX_SYMBOLIC** | Codifica simbolica SAX: lettere che codificano la forma del segnale (alphabet=5, word=10) | SAX/HAR-LLM (Pappa et al., 2026) | ~21 000 |

La centralizzazione del task è una scelta di design sperimentale: la pipeline di produzione FoT usa 4 agenti specialisti (ciascuno guasto vs normale), non un singolo LLM a 5 classi. Centralizzare isola la variabile "rappresentazione" evitando confounding con l'architettura federata.

### 2 · Dove ci collochiamo nella letteratura

Il campo dell'uso di LLM per diagnosticare guasti industriali è molto giovane — le prime pubblicazioni serie risalgono al 2024-2025. La maggior parte dei lavori precedenti usa reti neurali tradizionali (CNN, LSTM, trasformatori) addestrate direttamente sui numeri dei sensori, senza passare per il linguaggio naturale. Quei metodi raggiungono accuratezze altissime (95%+) ma richiedono tanti dati di addestramento e non spiegano il ragionamento.

Il nostro contributo si inserisce in un filone che si chiede: **possiamo usare l'intelligenza "generica" di un LLM per diagnosticare guasti senza doverlo addestrare?** La risposta sembra sì, ma la domanda successiva è: quale formato di rappresentazione funziona meglio?

Ed è esattamente la domanda a cui rispondiamo. In letteratura:

- **LLMTime** (Gruver et al., 2023) ha mostrato che gli LLM possono gestire serie temporali serializzate come numeri → noi testiamo qualcosa di simile con RAW_FEATURES
- **CGTime** (Feng et al., 2026) propone un approccio "percezione statistica" → noi ne testiamo una versione adattata
- **SAX/HAR-LLM** (Pappa et al., 2026) usa codifiche simboliche per sensori → noi testiamo SAX
- Nel corpus consultato **non abbiamo identificato un confronto sistematico di queste strategie sullo stesso dataset, stesso LLM e stesse condizioni**; ciò non dimostra l'assenza assoluta di precedenti

Questo è il nostro punto di forza: siamo probabilmente il **primo confronto controllato head-to-head** di strategie di rappresentazione TS→text per fault diagnosis con LLM.

### 3 · Cosa dicono i risultati, e quanto sono forti

Il risultato principale è che i tre metodi migliori (V2_TEXT, RAW_FEATURES, CGTIME_STATS) hanno accuratezze osservate vicine (88.9%, 93.3%, 91.1%), e **nessuna differenza è statisticamente significativa con nessun test**. SAX va peggio (73.3%) ma nemmeno quel divario è confermato statisticamente con test corretti.

Tradotto: con il campione che abbiamo, **non possiamo dire chi vince**. Possiamo dire che il V2 non è chiaramente peggiore nonostante usi 180 volte meno token.

| Braccio | Accuracy | 95% CI (boot) | Bal. Acc | Macro-F1 | MCC | Sel. Acc | Coverage |
| --- | --- | --- | --- | --- | --- | --- | --- |
| **V2_TEXT** | 0.889 | [0.733, 1.000] | 0.889 | 0.907 | 0.866 | 0.930 | 0.956 |
| **RAW_FEATURES** | 0.933 | [0.800, 1.000] | 0.933 | 0.960 | 0.923 | 1.000 | 0.933 |
| **CGTIME_STATS** | 0.911 | [0.756, 1.000] | 0.911 | 0.943 | 0.900 | 1.000 | 0.911 |
| **SAX_SYMBOLIC** | 0.733 | [0.533, 0.933] | 0.733 | 0.721 | 0.699 | 0.786 | 0.933 |

Un dato interessante emerge dalla selective accuracy: RAW_FEATURES e CGTIME_STATS hanno selective accuracy = 1.000 — cioè quando rispondono, non sbagliano mai. La differenza rispetto al V2 dipende interamente dal fatto che si astengono di più sul guasto F13 (il drift lento, il caso più difficile). Attenzione però: selective accuracy = 1.000 è condizionata alla non-astensione — non sostituisce l'accuratezza complessiva, la copertura o il selective risk.

Il recall per classe conferma il pattern:

| Braccio | F1 | F8 | F10 | F13 | Normal |
| --- | --- | --- | --- | --- | --- |
| V2_TEXT | 1.000 | 0.667 | 1.000 | 0.778 | 1.000 |
| RAW_FEATURES | 1.000 | 1.000 | 1.000 | 0.667 | 1.000 |
| CGTIME_STATS | 1.000 | 1.000 | 1.000 | 0.556 | 1.000 |
| SAX_SYMBOLIC | 1.000 | 1.000 | 1.000 | 0.333 | 0.333 |

F13 è il guasto più difficile nella maggior parte dei bracci, ma con pattern arm-dependent: V2 tende a misclassificarlo come F8, mentre RAW e CGTIME tendono ad astenersi. SAX_SYMBOLIC mostra problemi sia su F13 sia su Normal. Non è "universalmente il più difficile" — la difficoltà varia per braccio.

I confronti pairwise con test cluster-aware e correzione Holm–Bonferroni confermano l'assenza di significatività:

| Confronto | Δ Accuracy | p (boot) | p (perm) | p (McN-case) | Significativo? |
| --- | --- | --- | --- | --- | --- |
| V2 vs RAW | −0.044 | 0.769 | 1.000 | 1.000 | No |
| V2 vs CGTIME | −0.022 | 0.967 | 1.000 | 1.000 | No |
| V2 vs SAX | +0.156 | 0.270 | 0.375 | 0.625 | No |
| RAW vs CGTIME | +0.022 | 0.710 | 1.000 | 1.000 | No |
| RAW vs SAX | +0.200 | 0.072 | 0.250 | 0.250 | No |
| CGTIME vs SAX | +0.178 | 0.071 | 0.250 | 0.250 | No |

### 4 · Le critiche principali che ci possono fare (e le nostre difese)

**Critica 1: "Il campione è troppo piccolo"** — Abbiamo 15 casi indipendenti (3 per classe). Per rilevare una differenza del 10% servirebbe un campione molto più grande. È la critica più forte e più legittima. *Difesa:* lo dichiariamo esplicitamente. È un pilot study esplorativo, non un trial confermativo. L'MDE (minimum detectable effect) è ~25 punti percentuali — lo riportiamo. Nessuno dovrebbe aspettarsi conclusioni definitive da 15 casi, e noi non le pretendiamo.

**Critica 2: "Avete testato solo 4 guasti su 28"** — Il TEP ha 28 tipi di guasto. Ne abbiamo usati 4 (uno facile, due medi, uno difficile). *Difesa:* copriamo le categorie principali (step, stocastico, drift), ma non possiamo generalizzare a tutti i 28. Lo diciamo chiaramente. L'obiettivo era dimostrare il framework di confronto, non esaurire lo spazio dei guasti.

**Critica 3: "V2_TEXT bara perché inietta conoscenza di dominio"** — V2_TEXT non è solo un formato diverso: include soglie calcolate statisticamente e descrizioni dei trend. Gli altri arm non hanno questa informazione. *Difesa:* è vero, ed è un caveat che riportiamo. Il confronto misura "formato + informazione" insieme, non solo il formato. Ma nella pratica, il fatto che V2 raggiunga risultati simili con 180× meno token *includendo* il preprocessing è comunque rilevante operativamente. E il costo del preprocessing è esterno al budget di token del prompt — lo segnaliamo esplicitamente.

**Critica 4: "Un solo LLM"** — Tutto è testato con GPT-5.6-terra. Un altro modello potrebbe ribaltare il ranking. *Difesa:* corretto. È un limite dichiarato. Ma il contributo metodologico (il framework di confronto) resta valido indipendentemente dal modello specifico.

**Critica 5: "I metodi numerici funzionano meglio"** — Il confronto C02b sul medesimo compito ora mostra che la baseline numerica con prototipi condivisi ottiene 36/36 local-unseen, contro 31/36 di FoT B. *Risposta:* va riportato apertamente: sul benchmark studiato il numerico è migliore. L'ablation resta una domanda distinta, limitata ai formati forniti allo stesso LLM.

**Critica 6: "Il test era centralizzato, ma il sistema reale è federato"** — La pipeline di produzione FoT usa 4 agenti specialisti, non un singolo LLM a 5 classi. *Difesa:* l'ablation isola la variabile "rappresentazione" in condizioni controllate. Centralizzare il task è una scelta di design sperimentale per evitare confounding con l'architettura federata. Validare nel setting federato è un follow-up necessario, ma l'ablation fa il suo lavoro: confrontare le rappresentazioni a parità di tutto il resto.

Una distinzione utile: l'ablation risponde alla critica "perché V2 e non un'altra rappresentazione per lo stesso LLM?" mostrando che V2 ottiene accuratezza comparabile con 39–180× meno token. La critica "perché un LLM e non un metodo numerico?" è invece affrontata dal confronto C02b; in questo benchmark il prototipo numerico vince. Interpretabilità testuale e assenza di training del consumer restano proprietà qualitative, non compensazioni quantitative dimostrate.

### 5 · Sintesi

Siamo in una posizione da **buon pilot study esplorativo**. Abbiamo:

- Il **primo confronto sistematico** di rappresentazioni TS→text per fault diagnosis con LLM
- Una **metodologia statistica corretta e robusta** (test cluster-aware, MDE dichiarato, conclusioni calibrate)
- **Risultati interessanti**: il metodo più compatto (V2) funziona altrettanto bene dei metodi più verbosi, con un vantaggio pratico enorme in termini di costi

Le limitazioni (campione piccolo, un solo LLM, 4 fault su 28) sono tutte dichiarate e nessuna è fatale per un paper che si presenti come studio esplorativo piuttosto che come evidenza definitiva.

Il verdetto **GO-with-reservations** della review esterna riflette proprio questo: pubblicabile con le dovute qualificazioni, non come risultato conclusivo.

---

## Caratterizzazione del payload comunicativo FoT–TEP

Questa sezione quantifica la comunicazione usando **soltanto gli artefatti frozen**: non sono state eseguite nuove inferenze LLM e nessun risultato sperimentale è stato modificato. L'unità primaria è il blocco realmente inserito nel prompt del consumer: `PEER INSIGHTS\n` + array JSON UTF-8 indentato + due newline finali. I prompt A/B/E e C sono stati ricostruiti deterministicamente e tutti gli hash sono stati verificati contro i prediction log.

### Perché la mancata caratterizzazione era una critica

L'esperimento mostrava soprattutto che gli insight miglioravano la diagnosi, ma inizialmente non quantificava il **prezzo della comunicazione** necessaria per ottenere quel risultato. La domanda naturale di un reviewer era quindi: *«Il metodo funziona, ma quanta informazione devono scambiarsi gli agenti?»*

La caratterizzazione del payload risponde misurando quanti insight vengono inviati, quanto pesano in byte, quanti token aggiungono ai prompt, quante volte vengono trasferiti e quale costo registrato richiedono per essere prodotti e consumati. Senza queste misure non si può sostenere che FoT sia leggero, economico o più efficiente di metodi che scambiano logit, prototipi o parametri. L'analisi colma la lacuna descrivendo il costo osservato di FoT, ma **non dimostra automaticamente né maggiore efficienza né privacy**.

Gli output completi e machine-readable sono il [report di caratterizzazione](../analysis/communication_characterization/COMMUNICATION_PAYLOAD_CHARACTERIZATION.md), il [CSV](../analysis/communication_characterization/communication_payload_metrics.csv) e il [riepilogo JSON](../analysis/communication_characterization/communication_payload_summary.json). Si rigenerano con un solo comando:

```bash
python analysis/communication_characterization/characterize_payload.py
```

### Payload prodotto e ricevuto

La libreria contiene **8 insight unici, 2 per producer**. L'artefatto completo occupa 3.108 caratteri e 3.125 byte UTF-8, inclusa la newline terminale. Ogni consumer riceve i 6 insight prodotti dai tre peer:

| Consumer | Insight | Caratteri | Byte UTF-8 | Parole | Righe | Token GPT* | Token Qwen* |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| agent_1 | 6 | 2.289 | 2.304 | 240 | 46 | 664 | 724 |
| agent_2 | 6 | 2.327 | 2.336 | 244 | 46 | 684 | 749 |
| agent_3 | 6 | 2.410 | 2.420 | 258 | 46 | 681 | 747 |
| agent_4 | 6 | 2.361 | 2.378 | 250 | 46 | 690 | 754 |
| **Unità completa, 4 receiver** | **24 consegne** | **9.387** | **9.438** | — | — | **2.719** | **2.974** |

\* I token sono incrementi **esatti in contesto** B−A ricavati dai log del provider, non tokenizzazioni standalone del solo blocco. Per GPT-5.6-terra il nome/versione del tokenizer non è frozen; per Qwen è frozen la revisione `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`, ma non i file del tokenizer. Le stime standalone per insight non vanno presentate come misure esatte.

Statistiche sui singoli oggetti insight JSON, escluso il framing dell'array/header:

| Metrica | Media | Mediana | Min | Max | Dev. std. popolazione |
| --- | ---: | ---: | ---: | ---: | ---: |
| Caratteri | 372,12 | 380,00 | 320 | 412 | 25,94 |
| Byte UTF-8 | 374,25 | 382,00 | 321 | 412 | 26,01 |
| Parole | 41,00 | 40,00 | 33 | 46 | 4,03 |
| Righe | 7,00 | 7,00 | 7 | 7 | 0,00 |
| Token GPT stimati | 107,75 | 110,00 | 92 | 119 | 7,69 |
| Token Qwen stimati | 118,12 | 120,50 | 101 | 130 | 8,33 |

La regola per le parole è `\b[^\W_]+(?:[’'-][^\W_]+)*\b`; caratteri, byte e righe seguono rispettivamente code point Python, codifica UTF-8 e `splitlines()`.

### Controllo strutturale B versus E

Il controllo ha esito **PASS**. Per ogni receiver B ed E hanno stesso numero di insight, stessi ID, fonti, ordine, chiavi JSON, observed pattern, caratteri, parole, righe, byte e gli stessi conteggi token osservati nei due consumer. **Non sono byte-identici**: E cambia esclusivamente i sei valori `pseudolabel` secondo il derangement frozen. Tutte le pseudolabel sono ASCII di 9 byte, perciò la lunghezza resta invariata.

| Consumer | Sostituzioni | Posizioni byte diverse | Byte B = E | Token GPT B = E | Token Qwen B = E |
| --- | ---: | ---: | ---: | ---: | ---: |
| agent_1 | 6 | 28 | 2.304 | 664 | 724 |
| agent_2 | 6 | 28 | 2.336 | 684 | 749 |
| agent_3 | 6 | 26 | 2.420 | 681 | 747 |
| agent_4 | 6 | 30 | 2.378 | 690 | 754 |
| **Totale** | **24** | **112** | **9.438** | **2.719** | **2.974** |

Non vi sono inserimenti o cancellazioni. La parità di token è una misura osservata per questi modelli e questi prompt, non una proprietà generale delle stringhe derangiate.

### Costo separato di produzione, trasferimento e consumo

La produzione degli insight è un costo frozen una tantum: **4 chiamate**, 7.954 input token, 820 output token, 0 reasoning token e 9 s di latenza provider registrata. Ciascun agente ha prodotto due insight:

| Producer / fault | Chiamate | Input tok | Output tok | Reasoning tok | Latenza |
| --- | ---: | ---: | ---: | ---: | ---: |
| agent_1 / F1 | 1 | 1.961 | 220 | 0 | 2 s |
| agent_2 / F8 | 1 | 2.002 | 201 | 0 | 3 s |
| agent_3 / F10 | 1 | 1.996 | 204 | 0 | 2 s |
| agent_4 / F13 | 1 | 1.995 | 195 | 0 | 2 s |

Il trasferimento non è una chiamata separata: il suo costo token è l'incremento nel prompt del consumer. I reasoning token sono inclusi negli output/completion token e non devono essere sommati di nuovo.

| Esperimento | Cond. | Chiamate logiche/provider | Byte payload | Token payload* | Input tok | Output tok | Reasoning tok | Unseen corrette |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Experiment 1 | A | 180/180 | 0 | 0 | 291.567 | 28.155 | 9.733 | 0/36 |
| Experiment 1 | B | 180/180 | 424.710 | 122.355 | 413.922 | 27.888 | 8.684 | 31/36 |
| Experiment 1 | E | 180/181 | 424.710 | 122.355 | 413.970 | 28.792 | 9.874 | 3/36 |
| EXP3_V2 | A | 360/360 | 0 | 0 | 581.670 | 55.426 | 19.156 | 0/72 |
| EXP3_V2 | B | 360/362 | 849.420 | 244.710 | 826.476 | 57.236 | 19.378 | 68/72 |
| EXP3_V2 | E | 360/360 | 849.420 | 244.710 | 826.380 | 59.614 | 20.365 | 4/72 |
| Experiment 2 Qwen | A | 180/180 | 0 | 0 | 287.205 | 101.766 | 83.838 | 0/36 |
| Experiment 2 Qwen | B | 180/180 | 424.710 | 133.830 | 421.035 | 150.705 | 127.833 | 34/36 |
| Experiment 2 Qwen | E | 180/180 | 424.710 | 133.830 | 421.035 | 151.179 | 128.271 | 1/36 |
| Exp. 1, Condition C | C | 45/45 | 570.060 | solo stima | 209.118 | 5.869 | n.d. | 15/15 overall |

\* Esatti in contesto per A/B/E. Per C i due blocchi aggiunti — 10 esempi pooled e 8 insight — occupano 12.668 byte per chiamata; le stime sono 3.650 token GPT e 3.992 token Qwen, ma il delta esatto non è isolabile dai log. C è post-hoc, receiver-independent, disponibile solo su Experiment 1 e non isomorfa a B.

La latenza consumer registrata è: Experiment 1 A/B/E = 417/411/407 s totali (2,32/2,28/2,26 s medi); EXP3_V2 = 1.148/1.123/1.153 s (3,19/3,12/3,20 s medi). Per Qwen e C la latenza non è disponibile. Non è calcolato alcun costo monetario perché il repository non congela prezzi applicabili o addebiti.

### Round, volumi ed efficienza descrittiva

Ogni braccio B o E usa una libreria statica: **un round logico di conoscenza**, 12 archi diretti source→consumer, 4 blocchi receiver-specific e 24 consegne di insight. Il blocco viene però reinserito in ogni chiamata. Considerando insieme B+E:

| Esperimento | Round logici | Blocchi reinseriti | Trasferimenti source→consumer | Insight consegnati | Byte | Token in contesto |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Experiment 1 | 2 | 360 | 1.080 | 2.160 | 849.420 | 244.710 |
| EXP3_V2 | 2 | 720 | 2.160 | 4.320 | 1.698.840 | 489.420 |
| Experiment 2 Qwen | 2 | 360 | 1.080 | 2.160 | 849.420 | 267.660 |

Le normalizzazioni seguenti riguardano soltanto le predizioni aggregate locally-unseen e mantengono separate le tre ripetizioni LLM. Sono misure descrittive dipendenti dal campione, non una prova di superiorità comunicativa.

| Esperimento | Casi fault fisici | Pred. unseen aggregate | B−A | B−E | Byte/B corretta | Token/B corretta | Token per punto % |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Experiment 1 | 12 | 36 | +0,8611 | +0,7778 | 8.220,19 | 2.368,16 | 23,68 |
| EXP3_V2 | 24 | 72 | +0,9444 | +0,8889 | 7.494,88 | 2.159,21 | 21,59 |
| Experiment 2 Qwen | 12 | 36 | +0,9444 | +0,9167 | 7.494,88 | 2.361,71 | 23,62 |

“Token per punto %” = incremento medio B−A per chiamata × R=3 / incremento di accuracy in punti percentuali. Il payload B rappresenta il 32,51%/29,56% di byte/token del prompt completo in Experiment 1, il 32,56%/29,61% in EXP3_V2 e il 32,51%/31,79% in Experiment 2 Qwen. Per C il rapporto byte è 88,10%; il rapporto token non è disponibile come misura esatta.

### Confronto concettuale con paradigmi adiacenti

| Paradigma | Oggetto trasmesso | Unità naturale | Leggibilità | Dipendenza dal modello | Dati pubblici | Costo per round | Audit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| FedMD | Logit su esempi condivisi | scalari/byte | bassa | spazio output compatibile | sì, nel metodo canonico | `K × N_pub × C × byte/logit`, dati concreti n.d. | tensori e dataset ispezionabili |
| FedProto | Prototipi medi per classe | scalari/byte | bassa–media | spazio embedding/proiezione | non necessariamente | `Σ_k C_k × d × byte/scalare`, dati concreti n.d. | semantica indiretta |
| Adapter/LoRA federati | Parametri trainabili | parametri/byte | bassa | alta: architettura, layer e rank | no in generale | `K × P_adapter × byte/parametro`, dati concreti n.d. | provenienza binaria, bassa leggibilità semantica |
| FoT | Record JSON testuali | caratteri/byte/token | alta per ispezione umana | tokenizzazione e uso dipendono dal consumer | no nel setup TEP | somma misurata dei blocchi per receiver/chiamata | contenuto, ordine, mapping e hash verificabili |

Il confronto è concettuale e non isomorfo: byte di testo, logit, prototipi e parametri non sono direttamente equivalenti. Non sono prodotti numeri attribuiti agli algoritmi originali FedMD, FedProto o LoRA; la sezione C02b seguente riporta invece una baseline same-task con prototipi condivisi, esplicitamente qualificata come ispirata a FedProto. Le misure FoT non dimostrano privacy, efficienza di banda o superiorità rispetto a FL parametrico.

### Provenienza e limiti della misura

Le fonti primarie sono `phase_b/insights`, `phase_b/final_evaluation`, `phase_b/exp2/qwen`, `icl`, e gli oggetti Git dei tag frozen `exp3-v2-inference-frozen-001` e `exp3-v2-results-frozen-001`. Sono stati superati 10 controlli di coerenza, inclusa la verifica degli hash dei prompt ricostruiti e del controllo B/E. Restano non disponibili: tokenizer standalone GPT, file tokenizer Qwen nel repository, reasoning e latenza di C, latenza Qwen, prezzi/addebiti e una Condition C su EXP3_V2.

---

## Baseline numerica sullo stesso compito · C02b

Il confronto esterno principale è la **baseline numerica con prototipi condivisi, ispirata a FedProto**. Non è chiamata “FedProto”: non addestra una rete di rappresentazione e non implementa l’ottimizzazione dell’algoritmo originale. Rispetta però lo stesso problema informativo di FoT: quattro agenti, Normal più un solo fault locale, pseudolabel opache, stessi dati development e stessi 15 PBH held-out. La ground truth PBH viene collegata alle predizioni soltanto nella valutazione offline.

Il protocollo è stato congelato e hashato prima dell’esecuzione. Ogni caso diventa il vettore numerico frozen a **697 componenti** (`41 XMEAS × 17`) derivato dall’evidenza strutturata prima del testo. Per ogni classe si calcola la media dei cinque casi development; la classificazione sceglie il prototipo con minima distanza assoluta media. Non viene appresa alcuna normalizzazione sul test. Un pareggio entro `1e-12` produce astensione; input mancanti, non finiti o con hash errato fermano l’intera esecuzione.

| Braccio | Libreria disponibile a ciascun agente | Complessiva | Local-seen | Local-unseen | Normal |
| --- | --- | ---: | ---: | ---: | ---: |
| Prototipi condivisi | Normal + fault locale + 3 fault peer | **60/60 (100%)** | 12/12 | **36/36 (100%)** | 12/12 |
| Local-only numerica | Normal + solo fault locale | 24/60 (40%) | 12/12 | 0/36 (0%) | 12/12 |
| Centralizzata numerica | Tutti i 5 centroidi development | 60/60 (100%) | 12/12 | 36/36 (100%) | 12/12 |

L’intervallo bootstrap al 95% della metrica primaria è `[100%, 100%]`, ma non indica certezza generale: ricampiona soltanto i 12 casi fisici disponibili, stratificati per fault, mantenendo unite le tre viste local-unseen di ciascun caso.

### Confronto prudente con A, B ed E

| Metodo | Local-unseen | Differenza prototipi condivisi − metodo |
| --- | ---: | ---: |
| Prototipi condivisi | **36/36 (100%)** | — |
| FoT A | 0/36 (0%) | +100,0 punti |
| FoT B | 31/36 (86,1%) | **+13,9 punti** |
| FoT E | 3/36 (8,3%) | +91,7 punti |

Sul benchmark studiato la baseline numerica è migliore di FoT B. Di conseguenza, questi dati **non supportano un claim di superiorità diagnostica di FoT**. Mostrano due cose più circoscritte: condividere conoscenza di classe è indispensabile nel setup local-unseen, e una media numerica compatta delle firme V2 è sufficiente a separare tutti i PBH osservati. A resta un information floor e E un controllo di associazione semantica, non competitor numerici.

### Risultati per agente e fault

Nel braccio condiviso ogni cella è `3/3`; la diagonale è local-seen e le altre celle sono local-unseen.

| Agente | CLS-ZOGAA / F1 | CLS-OJNSG / F8 | CLS-R463B / F10 | CLS-Z3ISU / F13 |
| --- | ---: | ---: | ---: | ---: |
| agent_1 | **3/3 seen** | 3/3 | 3/3 | 3/3 |
| agent_2 | 3/3 | **3/3 seen** | 3/3 | 3/3 |
| agent_3 | 3/3 | 3/3 | **3/3 seen** | 3/3 |
| agent_4 | 3/3 | 3/3 | 3/3 | **3/3 seen** |

La matrice di confusione aggregata è interamente diagonale: 12/12 per ciascuna delle quattro pseudoclassi fault e 12/12 per Normal, zero astensioni. I 12 conteggi per fault derivano da 3 casi fisici × 4 agenti e non sono trattati come 12 run indipendenti.

### Payload e limiti

Ogni agente riceve **3 prototipi**, cioè **2.091 scalari**. I payload binari prodotti realmente occupano **16.755 byte per agente** e **67.020 byte complessivi** per le 12 consegne peer: per prototipo, 9 byte ASCII di pseudolabel più 697 float64 little-endian. Non è incluso il framing di rete. Il prototipo Normal non viene trasmesso perché ogni agente possiede già lo stesso riferimento N1–N5.

Il riferimento centralizzato coincide matematicamente con il braccio condiviso perché usa gli stessi cinque centroidi; è un controllo descrittivo, non un upper bound garantito. PCA+SVM centralizzata non è stata eseguita perché esporre tutte le classi al training trasformerebbe il problema in classificazione supervisionata ordinaria. FedAvg non è stato eseguito perché richiederebbe un nuovo modello e un protocollo di output class-disjoint: la semplice media di modelli locali non rende disponibile una pseudoclasse mai presente nell’output locale. Produrre quei numeri avrebbe cambiato il compito.

Protocollo, codice, predizioni, matrice completa, payload e hash sono in [`phase_b/baselines/c02b_shared_numeric_prototypes`](../phase_b/baselines/c02b_shared_numeric_prototypes/results/C02B_BASELINE_REPORT.md). Il protocollo machine-readable ha SHA-256 `229f901a037cb0eca7e623b0efc585201de21a7a16ac51c4d143ea7a49cab545`.

### Suite di modelli richiesta dal supervisor

È stata inoltre eseguita una suite congelata prima del training con **AdaBoost, Random Forest, MLP, lineare elastic-net, k-NN, LSTM causale con attention, BiLSTM con attention e BiLSTM multimodale con attention**. La multimodale fonde la sequenza numerica con il testo neutro TF-IDF prodotto dal verbalizzatore frozen. XGBoost non era disponibile nell'ambiente, quindi è stata usata l'alternativa esplicitamente ammessa, AdaBoost.

| Modello centralizzato | 15 casi fisici | 12 fault | Local-unseen proiettato |
| --- | ---: | ---: | ---: |
| AdaBoost | **15/15 (100%)** | 12/12 | 36/36 |
| Random Forest | **15/15 (100%)** | 12/12 | 36/36 |
| MLP | **15/15 (100%)** | 12/12 | 36/36 |
| Lineare elastic-net | **15/15 (100%)** | 12/12 | 36/36 |
| k-NN | **15/15 (100%)** | 12/12 | 36/36 |
| LSTM causale + attention | **15/15 (100%)** | 12/12 | 36/36 |
| BiLSTM + attention | 14/15 (93,3%) | 11/12 | 33/36 |
| BiLSTM multimodale + attention | 14/15 (93,3%) | 11/12 | 33/36 |

I primi sei modelli non commettono errori sul piccolo held-out. La BiLSTM scambia PBH-011/F10 con Normal; la multimodale scambia PBH-014/F13 con F8. Ogni modello raggiunge il 100% sui 25 casi di training. Questo, insieme ai soli cinque casi development e tre test per classe, impone prudenza: il risultato può riflettere un benchmark facilmente separabile e non prova generalizzazione ampia.

Questi otto modelli vedono tutte le cinque pseudoclassi durante il training centralizzato. Il valore “local-unseen proiettato” replica la stessa predizione centrale sui tre agenti per cui il fault è localmente unseen; non trasforma il metodo in federato e non crea 36 osservazioni indipendenti. Il confronto diretto class-disjoint resta quindi quello con i prototipi condivisi. Inoltre, una BiLSTM non viene chiamata causale: usa anche i passi successivi nell'intervallo osservato. La variante multimodale usa due rappresentazioni degli stessi sensori, non una seconda sorgente fisica.

Il [rapporto completo della suite](../phase_b/baselines/c02b_supervisor_model_suite/results/SUPERVISOR_MODEL_SUITE_REPORT.md) contiene matrici, predizioni, pesi, storie di training e hash. La configurazione frozen ha SHA-256 `9b9a90c7878845f06d0be0e7e4c58b0f55b89035ef5b406c2a3e516a460527ed`; una seconda esecuzione ha verificato gli artefatti byte-per-byte.

---

## Condizione A+ e risposta alla critica C01

### Motivazione

La critica C01 osserva che la baseline A è debole: lo 0% sulle classi non viste è in parte atteso, perché l'agente non possiede alcuna informazione sulle classi remote. Prima di attribuire il vantaggio di B all'effetto peer, occorre escludere che il semplice possesso dei propri insight (già noti all'agente) possa migliorare la diagnosi.

### Disegno sperimentale

La condizione **A+** (local-only self-insight) replica esattamente il protocollo frozen della Phase B, con un'unica differenza: nel blocco `<<PEER_INSIGHTS_BLOCK>>` del prompt, ogni agente riceve i **due insight che ha prodotto sulla propria classe locale**, anziché gli insight peer (B) o corrotti (E). Nessun insight peer, nessun nome di classe reale, nessuna etichetta di test e nessun risultato held-out entra nel prompt A+.

Parametri identici al protocollo frozen: modello `gpt-5.6-terra`, reasoning `medium`, structured outputs strict, `temperature=null`, `seed=null`, R=3 ripetizioni, aggregazione majority-vote 2/3, astensioni contate come errore. Casi held-out identici (15 casi fisici × 4 agenti = 60 osservazioni aggregate). Configurazione congelata e verificata tramite `APLUS_FREEZE_MANIFEST.json` prima dell'inferenza.

### Risultati primari: classi localmente non viste

| Condizione | Corrette / n | Accuratezza | Astensioni |
|---|---:|---:|---:|
| A | 0 / 36 | 0,00% | 14 |
| A+ | 0 / 36 | 0,00% | 21 |
| B | 31 / 36 | 86,11% | 0 |
| E | 3 / 36 | 8,33% | 0 |

**Delta A+−A = 0 esattamente.** I self-insight non apportano alcun beneficio sulle classi non viste. L'agente conosce già la propria classe locale; reinserire quell'informazione nel prompt non gli consente di diagnosticare guasti mai osservati.

### Trasferimenti appaiati (unseen, n=36)

| Confronto | Aiutati | Danneggiati | Invariati (corretti/errati) |
|---|---:|---:|---|
| A+ vs A | 0 | 0 | 36 (0/36) |
| B vs A+ | 31 | 0 | 5 (0/5) |
| E vs A+ | 3 | 0 | 33 (0/33) |

B aiuta 31 osservazioni rispetto ad A+ (e ad A: i numeri coincidono), senza mai danneggiare.

### Bootstrap stratificato per cluster fisici

- 10.000 draw, seed 20260829, stratificazione per pseudolabel vera (4 strati × 3 run fisici)
- Delta A+−A 95% CI: [0, 0]
- Delta B−A+ 95% CI: [0,833 ; 0,917]
- Delta E−A+ 95% CI: [0,028 ; 0,139]

### Per agente (classi non viste)

| Agente | n | A | A+ | B | E | Δ(A+−A) | Δ(B−A+) |
|---|---:|---:|---:|---:|---:|---:|---:|
| agent_1 | 9 | 0,00% | 0,00% | 100,00% | 0,00% | 0 | 1 |
| agent_2 | 9 | 0,00% | 0,00% | 100,00% | 0,00% | 0 | 1 |
| agent_3 | 9 | 0,00% | 0,00% | 66,67% | 22,22% | 0 | 0,667 |
| agent_4 | 9 | 0,00% | 0,00% | 77,78% | 11,11% | 0 | 0,778 |

Tutti e quattro gli agenti: A+ = 0% sulle classi non viste, identico ad A.

### Esiti secondari

Le classi localmente viste (local-seen) e i casi Normal restano 100% in tutte e quattro le condizioni: la condizione A+ non introduce regressioni.

### Accordo inter-ripetizione (A+)

- Unanimità 3/3: 57 / 60 (95,0%)
- Maggioranza 2/3: 3 / 60
- Tutti diversi: 0 / 60

### Token e costi

- Input: 333.192 token
- Output: 29.695 token
- Totale: 362.887 token
- Structural retries: 0; parse failures: 0

### Interpretazione

A+ ≈ A conferma che i **self-insight non sono sufficienti** per diagnosticare classi non viste: l'agente possiede già la conoscenza della propria classe locale, e reinserirla nel prompt non aggiunge informazione utile. Il fatto che B >> A+ ≈ A dimostra che il beneficio di B è **interamente attribuibile alla conoscenza peer**, cioè agli insight prodotti dagli altri agenti sulle loro rispettive classi. La critica C01 riceve così una risposta sperimentale: A non è una baseline artificialmente debole — è il corretto pavimento informativo. Rafforzarla con la conoscenza di sé non cambia l'esito.

Protocollo, codice, predizioni, metriche e hash sono in [`phase_b/final_evaluation_aplus`](../phase_b/final_evaluation_aplus/APLUS_EVALUATION_REPORT.md). La configurazione frozen ha SHA-256 verificabile tramite `APLUS_FREEZE_MANIFEST.json`.


---

## C06 · Full test della policy «local evidence first»

La replica EXP3_V2 aveva rivelato un problema importante: nella configurazione B, gli insight peer miglioravano molto i guasti localmente non visti, ma i casi **local-seen** scendevano da 24/24 in A a **19/24**. In cinque casi l'agente ignorava o sottopesava una firma che conosceva già localmente, soprattutto nella confusione F8↔F13.

Il controllo C06 ha modificato una sola parte del prompt di B: un breve blocco di *decision policy* ordina all'agente di dare precedenza all'evidenza locale quando questa è forte e coerente, usando gli insight peer come supporto e non come sostituto. Dopo uno screening su 24 casi, la variante congelata `B_LOCAL_FIRST_V1` è stata eseguita sull'intero EXP3_V2: **120 agent-case aggregati**, ciascuno ottenuto da R=3 ripetizioni valide.

| Gate del full test | B originale | B_LOCAL_FIRST_V1 | Soglia | Esito |
| --- | ---: | ---: | ---: | --- |
| Local-seen | 19/24 (79,2%) | **23/24 (95,8%)** | ≥ 23/24 | **PASS** |
| Local-unseen | 68/72 (94,4%) | **68/72 (94,4%)** | ≥ 67/72 | **PASS** |
| Normal | 24/24 (100%) | **24/24 (100%)** | = 24/24 | **PASS** |
| Parse failures | 0 | **0** | = 0 | **PASS** |
| Overall | 111/120 (92,5%) | **115/120 (95,8%)** | — | +4 netti |

Il confronto appaiato contiene **5 miglioramenti e 1 regressione**, tutti nella confusione F8↔F13. I quattro recuperi local-seen sono Agent 4 su F13-003, F13-004 e F13-005 e Agent 2 su F8-003; si aggiunge il recupero local-unseen di Agent 1 su F8-003. L'unica regressione è Agent 2 su F13-002, local-unseen, stabile 3/3; il caso local-seen F13-002 di Agent 4 resta errato. La nuova policy mantiene quindi invariata l'accuratezza aggregata local-unseen, ma **non elimina ogni regressione a livello di singolo caso**. Si osservano inoltre 112/120 decisioni unanimi 3/3 e una sola astensione aggregata.

La conclusione corretta è circoscritta: **nel perimetro post-hoc di EXP3_V2**, il trasferimento negativo local-seen è sostanzialmente mitigato da una singola policy che antepone l'evidenza locale agli insight peer, senza perdita aggregata sulle diagnosi remote o sui casi Normal. Non è una prova di immunità generale al trasferimento negativo: la variante è stata progettata dopo aver osservato gli errori ed è valutata sullo stesso campione EXP3_V2, non su una replica indipendente.

Protocollo, predizioni, log e gate sono nel [rapporto completo C06](../phase_b/c06/full_test/inference/FULL_TEST_REPORT.md).

---

## Critiche

### Giudizio generale aggiornato

L'esperimento è una buona prova controllata: mostra che una descrizione testuale corretta può portare a un agente la conoscenza che gli manca. Il punto debole è che questa conoscenza viene data a B per costruzione, mentre A non possiede il collegamento alle classi remote. Il grande vantaggio di B dimostra quindi il **meccanismo**, non ancora la superiorità di un sistema federato completo.

**Legenda:** **Risolta** = la misura richiesta esiste; **Risolta editorialmente** = i testi sono stati corretti, senza nuova evidenza sperimentale; **Mitigata** = è stata aggiunta evidenza, ma resta un limite; **In corso** = il controllo è previsto o in completamento; **Aperta** = manca ancora una risposta sperimentale.

| ID | Categoria | Critica | Stato | Spiegazione semplice |
| --- | --- | --- | --- | --- |
| C01 | Valutazione | Baseline A troppo debole | **Risolta** | A+ (self-insight only) conferma che lo 0% di A non dipende dall'assenza di insight propri: A+ = 0% sulle classi non viste, identico ad A. Il vantaggio di B è interamente peer-driven. Vedi sezione "Condizione A+". |
| C02a | Baseline interne | Confronti interni incompleti | **Mitigata** | A/B/E, A+ (local-only self-insight), Condition C e l'ablation confrontano varianti del sistema. A+ colma la lacuna del confronto local-only con gli insight propri. |
| C02b | Baseline esterne | Mancano baseline numeriche e FL | **Mitigata** | Il confronto diretto a prototipi condivisi ottiene 36/36 local-unseen contro 31/36 di FoT B. Sono stati aggiunti anche otto riferimenti centralizzati richiesti dal supervisor (93,3–100%), ma non sono federati; manca ancora una suite FL originale sullo stesso compito. |
| C03 | Rappresentazione | Trasformazione TS→testo | **Mitigata** | L'ablation confronta quattro formati. V2 usa molti meno token, ma il campione è piccolo e cambia anche quanta informazione viene preparata prima del prompt. |
| C04 | Modelli | Dipendenza da un solo LLM | **Mitigata** | Qwen conferma il risultato lato consumer. Gli insight sono però ancora prodotti da un solo modello proprietario. |
| C05 | Comunicazione | Payload non caratterizzato | **Risolta** | Ora sappiamo quanti messaggi, byte e token vengono scambiati. Resta vietato dire che FoT è più efficiente senza un confronto diretto. |
| C06 | Affidabilità | Peggioramento sui guasti già noti | **Risolta nel perimetro EXP3_V2** | Il full test B_LOCAL_FIRST_V1 supera tutti i gate: local-seen 23/24 contro 19/24 di B, local-unseen invariato a 68/72, Normal 24/24 e zero parse failure. Il saldo è +4 (5 miglioramenti, 1 regressione); resta quindi mitigazione sostanziale, non assenza universale di trasferimento negativo. |
| C07 | Inferenza | Reasoning cap e repliche identiche | **Risolta** | La sensitivity appaiata 1024–3072 e il follow-up capped a 4096 separano gli errori compatibili con troncatura da quelli per cui l'interferenza è più plausibile. Nessuna regressione; `R=1` resta però un test deterministico, non una misura di variabilità stocastica. |
| C08 | Scala | Pochi guasti, agenti e simulatori | **Mitigata** | La replica aggiunge 24 run, ma restano quattro guasti su 28, quattro agenti e un solo simulatore. Non prova generalità industriale. |
| C09 | Federazione | Federazione solo logica | **Aperta** | I nodi sono simulati sullo stesso processo. Non ci sono siti reali, proprietari diversi, nodi offline o reti instabili. |
| C10 | Sistema | Un solo round statico | **Aperta** | Gli insight vengono creati una volta e copiati nei prompt. Non sappiamo cosa succede con aggiornamenti, drift, ritardi o molti agenti. |
| C11 | Privacy | Nessuna garanzia formale | **Aperta** | Non si inviano dati grezzi, ma il testo può comunque rivelare informazioni. Non sono stati fatti attacchi di ricostruzione o misure di privacy. |
| C12 | Open world | Spazio di etichette chiuso | **Aperta** | Il modello sceglie tra pseudolabel note. Non è testato un guasto davvero nuovo, ambiguo o fuori catalogo. |
| C13 | Centralizzazione | Condition C non equivalente | **Mitigata** | C ottiene 15/15, ma è post-hoc, usa più contesto ed esiste solo per Experiment 1. È un riferimento, non una prova causale. |
| C14 | Statistica | Evidenza ancora piccola | **Mitigata** | La replica e i test per run sono corretti. Tuttavia il numero di run indipendenti resta basso per conclusioni ampie. |
| C15 | Novità | FoT non nasce in questo lavoro | **Risolta editorialmente** | FoT è attribuito a Yao et al.; il contributo è circoscritto alla combinazione tra TS industriali multivariate, esperienza class-disjoint/local-unseen, verbalizzazione verificabile, controllo B/E, protocollo frozen e replica. |
| C16 | Verbalizzatore | Feature e soglie rigide | **Aperta** | Mancano feature frequenziali e adattamento al drift. Soglie valide su TEP potrebbero non funzionare su un altro impianto. |
| C17 | Applicazione | Nessuna validazione PV reale | **Aperta** | Il fotovoltaico motiva il progetto, ma gli esperimenti usano solo TEP. Il paper non può dire che il metodo funziona già sul PV. |
| C18 | Conferenza | Debole evidenza di “Big Data” | **Risolta editorialmente** | L'aderenza è limitata a dati distribuiti, non-IID class-disjoint, collaborazione, Variety, Veracity, Value, evaluation/benchmarking e contesto industriale/IoT. Non c'è evidenza su Volume, Velocity, edge o scalabilità. |

C06 è chiusa nel perimetro di EXP3_V2 dal full test local-first; una replica indipendente della policy resta future work. C01 è risolta dalla condizione A+, C07 dalla sensitivity analysis, mentre C15 e C18 sono chiuse sul piano editoriale. C02a è ulteriormente rafforzata da A+, C02b resta mitigata: per avanzare servono metodi FL che mantengano lo **stesso compito class-disjoint**.

---

## Conferenza

### IEEE BigData 2026 · Special Session on Federated Learning on Big Data

La [call ufficiale della Special Session](https://bigdataieee.org/BigData2026/calls/special-federated-learning/) include dati distribuiti, distribuzioni non-IID, collaborative learning, evaluation e benchmarking, 5V e applicazioni IoT. Il lavoro vi aderisce per aspetti realmente valutati:

- **dati distribuiti e non-IID class-disjoint:** i quattro agenti hanno esperienze locali diverse;
- **collaborative knowledge transfer:** gli agenti condividono insight testuali, non aggiornamenti di modello;
- **Variety:** il testbed contiene serie industriali multivariate e firme di guasto eterogenee;
- **Veracity:** ground truth, verbalizzazione deterministica, artefatti frozen e controllo B/E rendono verificabili dati e associazioni semantiche;
- **Value:** si valuta se la conoscenza peer consenta la diagnosi di guasti localmente non osservati;
- **evaluation e benchmarking:** protocollo A/B/E, replica su nuovi run, sensitivity analysis del reasoning cap e confronti controllati forniscono una valutazione riproducibile;
- **contesto industriale e IoT:** TEP è un banco di prova industriale simulato pertinente al tema IoT della call.

Il framing corretto è **federated textual knowledge transfer**, cioè collaborative learning di tipo FL-like, non Federated Learning parametrico classico. Volume, Velocity, deployment edge, scalabilità a molti nodi, privacy, sicurezza e applicazioni fotovoltaiche validate non sono risultati di questo studio. Per i limiti di novità e di aderenza si vedano **C15** e **C18** nella sezione Critiche.

*Valutazione editoriale basata sui materiali del progetto e sulla call consultata il 10 settembre 2026.*

---

## Lit review

### Introduzione

Questa mappa unifica i Markdown di `docs/lit_review`, il workbook `docs/lit_review/FoT_literature_review.xlsx` e i paper convertiti in `papers`. Sono inclusi i lavori che incidono su almeno uno degli assi dell'esperimento: oggetto federato, classi localmente non viste, trasformazione TS→testo e diagnosi mediante LLM. Il README del convertitore PDF è documentazione tecnica, non un paper scientifico, e non compare nella tabella.

| Titolo | Query | Categoria |
| --- | --- | --- |
| Federation over Text: Insight Sharing for Multi-Agent Reasoning | `federated learning LLM sharing natural language insights reasoning agents non-IID 2026` | Federazione testuale |
| Federated In-Context LLM Agent Learning (FICAL) | `federated in-context learning prompt sharing LLM clients privacy` | Federazione testuale |
| Social Learning: Towards Collaborative Learning with LLMs | `federated learning LLM sharing natural language insights reasoning agents non-IID 2026` | Federazione testuale |
| FedCoT: Communication-Efficient Federated Reasoning Enhancement for LLMs | `FedCoT communication-efficient federated reasoning enhancement large language models` | Federazione testuale |
| Time-FFM: LM-Empowered Federated Foundation Model for Time Series Forecasting | `Time-FFM LM-Empowered Federated Foundation Model Time Series Forecasting` | Federazione testuale |
| FedMD: Heterogeneous Federated Learning via Model Distillation | `federated learning clients disjoint classes transfer locally unseen classes zero-shot` | FL class-disjoint |
| FedProto: Federated Prototype Learning across Heterogeneous Clients | `federated learning clients disjoint classes transfer locally unseen classes zero-shot` | FL class-disjoint |
| FedCKD: Knowledge Distillation with Label-Exclusive Clients | `federated learning clients disjoint classes transfer locally unseen classes zero-shot` | FL class-disjoint |
| FedMeta-FFD: Federated Meta-Learning for Fault Diagnosis | `federated fault diagnosis Tennessee Eastman Process non-IID clients unseen fault classes` | FL class-disjoint |
| Federated Zero-Shot Learning with Mid-Level Semantic Knowledge Transfer | `federated learning clients disjoint classes transfer locally unseen classes zero-shot` | FL class-disjoint |
| Truth-Conditional Captions for Time Series Data | `"time series" AND "faithfulness" AND ("captioning" OR "description")` | TS→text fedele |
| A Fuzzy Approach to Data-to-Text for Time Series | `"time series" AND "data-to-text" AND ("deterministic" OR "rule-based")` | TS→text fedele |
| ICA2TEXT: Data-to-Text for Air-Quality Time Series | `"time series" AND "data-to-text" AND ("deterministic" OR "rule-based")` | TS→text fedele |
| Representing Time Series as Structured Programs for LLM Reasoning (T2SP) | `T2SP "Time-Series-to-Structured-Programs" deterministic 2026` | TS→text fedele |
| CGTime: Decoupling Perception from Description in Time-Series Reasoning | `CGTime "Decoupling Perception from Description" time series 2026` | TS→text fedele |
| A Novel Feature Extraction Approach for Mechanical Fault Diagnosis Based on ESAX and BoW | `TITLE-ABS-KEY("time series" AND "text" AND ("faithful" OR "deterministic" OR "symbolic"))` | Simbolico |
| Bridging Time Series and Large Language Models via Symbolic Representation for HAR | stessa query simbolica | Simbolico |
| HSQP: Hierarchical Symbolic Quantization Prompting for Time-Series Forecasting | stessa query simbolica | Simbolico |
| T3: Domain-Agnostic Neural Time-Series Narration | `"time series" AND ("verbalization" OR "text generation" OR "natural language description")` | Allineamento TS–linguaggio |
| Repr2Seq: Time Series Representation to Sequence | stessa query narration | Allineamento TS–linguaggio |
| TADACap: Time-Series Image Retrieval for Domain-Aware Captioning | `TITLE-ABS-KEY("time series" AND "natural language" AND ("generation" OR "verbalization"))` | Allineamento TS–linguaggio |
| CLaSP: Contrastive Language–Signal Pretraining | stessa query natural language | Allineamento TS–linguaggio |
| TSLM: Time-Series Language Model for Captioning | stessa query narration | Allineamento TS–linguaggio |
| FD-LLM: Large Language Model for Fault Diagnosis of Machines | `time series captioning description multivariate 2025-2026` | LLM fault diagnosis |
| FD-LLM: Large Language Model for Fault Diagnosis of Complex Equipment | `"time series" "text generation" "fault diagnosis"` | LLM fault diagnosis |
| LLM-TSFD: Industrial Time-Series Human-in-the-Loop Fault Diagnosis | stessa query fault diagnosis | LLM fault diagnosis |
| BEDTime: A Unified Benchmark for Automatically Describing Time Series | `BEDTime benchmark time series description evaluation 2025` | Survey / benchmark |
| Empowering Time Series Analysis with Large Language Models: A Survey | query natural language sopra | Survey / benchmark |
| Time-Series Large Language Models: A Systematic Review | `time series text representation benchmark evaluation` | Survey / benchmark |
| Large Language Models for Time-Series Reasoning: A TMLR Survey | `survey time series LLM reasoning agentic TMLR 2026` | Survey / benchmark |
| Federated Reasoning LLMs: A Survey | `("communication cost" OR payload OR token) AND (federated LLM OR federated reasoning)` | Survey / benchmark |
| FedSRD: Communication-Efficient Federated LLM Fine-Tuning via Sparsify-Reconstruct-Decompose | `("communication cost" OR payload OR token) AND (federated LLM OR federated reasoning)` | Federazione testuale |
| FedMAPS: Federated Meta-Learning with Adaptive Cross-Domain Contrastive Learning for Few-Shot Fault Diagnosis | `("class-disjoint" OR "label-exclusive" OR "locally unseen classes") AND federated AND (diagnosis OR classification)` | FL class-disjoint |
| FedAPA-FD: Class-Sensitive Personalized Federated Learning for Non-IID Bearing Fault Diagnosis | `("class-disjoint" OR "label-exclusive" OR "locally unseen classes") AND federated AND (diagnosis OR classification)` | FL class-disjoint |
| Federated Meta-Learning with Transformer Fusion for Few-Shot Multi-Condition Fault Diagnosis | `("federated fault diagnosis" OR "distributed fault diagnosis") AND ("Tennessee Eastman" OR process industry) AND non-IID` | FL class-disjoint |
| Federated Learning Based on Fuzzy Fusion Rules for Chemical Production Process Fault Diagnosis | `("federated fault diagnosis" OR "distributed fault diagnosis") AND ("Tennessee Eastman" OR process industry) AND non-IID` | FL class-disjoint |
| On-the-Fly Signals-to-Semantics Storytelling for Explainable Industrial Maintenance Decisions | `("deterministic verbalization" OR "structured program") AND multivariate AND "time series" AND LLM` | TS→text fedele |
| LLM-ABBA: Understanding Time Series via Symbolic Approximation | `(SAX OR symbolic OR quantization) AND LLM AND "fault diagnosis" AND multivariate` | Simbolico |
| TableTime: Training-Free Table Understanding for Time Series Classification with LLMs | `("frozen LLM" OR "training-free") AND "time series" AND (diagnosis OR classification) AND cross-model` | Allineamento TS–linguaggio |
| Towards Semantically Faithful Text-to-Time Series Generation via Agents and Spectral Conditioning | `("time series to text" OR verbalization) AND (faithfulness OR factuality OR hallucination) AND benchmark` | Allineamento TS–linguaggio |
| EviFDD-Agent: Evidence-Traceable LLM Reporting for Industrial Process Fault Detection and Diagnosis | `("federated fault diagnosis" OR "distributed fault diagnosis") AND ("Tennessee Eastman" OR process industry) AND non-IID` | LLM fault diagnosis |
| CL-LLMOps: Fuzzy-Gated Verification of LLM Agents for Industrial Fault Diagnosis | `("selective prediction" OR abstention OR calibration) AND LLM AND industrial diagnosis` | LLM fault diagnosis |
| DML–LLM Hybrid Architecture for Fault Detection and Diagnosis in Sensor-Rich Industrial Systems | `("selective prediction" OR abstention OR calibration) AND LLM AND industrial diagnosis` | LLM fault diagnosis |
| Uncertainty-Aware Fault Diagnosis with Conformal Prediction | `("selective prediction" OR abstention OR calibration) AND LLM AND industrial diagnosis` | Calibrazione |
| Class-Conditional Conformal Prediction for Reliable Open-Set Fault Diagnosis in Safety-Critical Industrial Systems | `("selective prediction" OR abstention OR calibration) AND LLM AND industrial diagnosis` | Calibrazione |

### Federazione di conoscenza testuale

<details><summary>Federation over Text: Insight Sharing for Multi-Agent Reasoning</summary>

Agenti locali trasformano traiettorie in insight; un server li raggruppa, distilla e redistribuisce senza condividere esempi o gradienti.

**Confronto con FoT–TEP** — **Somiglianza:** insight naturali come oggetto federato. **Differenza:** FoT di Yao et al. è multi-round, server-based e cross-task; FoT–TEP è single-shot, peer-only e class-disjoint. **Implicazione:** prior obbligatorio; il contributo è l'adattamento e la valutazione controllata.
</details>

<details><summary>Federated In-Context LLM Agent Learning (FICAL)</summary>

I client costruiscono compendi di conoscenza naturale da esempi locali e li riusano in-context con costo comunicativo ridotto.

**Confronto con FoT–TEP** — **Somiglianza:** memoria testuale condivisa. **Differenza:** task nativamente testuali, senza sensori, unseen class o renderer verificabile. **Implicazione:** rafforza il framing *federated knowledge transfer*.
</details>

<details><summary>Social Learning: Towards Collaborative Learning with LLMs</summary>

Teacher LLM producono esempi sintetici e prompt astratti per un learner, collegando distillazione e trasferimento linguistico.

**Confronto con FoT–TEP** — **Somiglianza:** conoscenza condivisa come artefatto testuale. **Differenza:** esempi sintetici invece di firme neutrali di guasto. **Implicazione:** precedente concettuale, con controllo semantico meno forte di A/B/E.
</details>

<details><summary>FedCoT: Communication-Efficient Federated Reasoning Enhancement for LLMs</summary>

Seleziona chain-of-thought e scambia parametri LoRA per federare il reasoning medico.

**Confronto con FoT–TEP** — **Somiglianza:** reasoning collaborativo LLM. **Differenza:** adapter parametrici contro solo testo leggibile. **Implicazione:** motiva la misura byte/token del payload.
</details>

<details><summary>Time-FFM: LM-Empowered Federated Foundation Model for Time Series Forecasting</summary>

Adatta un backbone linguistico al forecasting TS federato mediante moduli condivisi e teste personalizzate.

**Confronto con FoT–TEP** — **Somiglianza:** FL, foundation model e TS. **Differenza:** forecasting parametrico contro diagnosi con insight. **Implicazione:** vieta claim generici di “primo FL+LLM per TS”.
</details>

<details><summary>FedSRD: Communication-Efficient Federated LLM Fine-Tuning via Sparsify-Reconstruct-Decompose</summary>

Yan et al. (WWW 2026). Propone una pipeline SRD che sparsifica gli aggiornamenti LoRA, ricostruisce una matrice densa e la decompone per ridurre il payload di comunicazione nel fine-tuning federato di LLM. Riduce fino al 90 % la banda senza degradare la qualità.

DOI: `10.1145/3774904.3792144`

**Confronto con FoT–TEP** — **Somiglianza:** affronta il costo comunicativo della federazione LLM. **Differenza:** scambia gradienti compressi, non insight testuali; FoT–TEP scambia un payload testuale misurato in byte e token. **Implicazione:** baseline concettuale per la metrica del payload; senza confronto diretto non si sostiene un vantaggio di scala o efficienza.
</details>

### FL non parametrico e class-disjoint

<details><summary>FedMD: Heterogeneous Federated Learning via Model Distillation</summary>

Scambia predizioni su dati pubblici per distillare modelli eterogenei.

**Confronto con FoT–TEP** — **Somiglianza:** l'oggetto federato non sono i pesi. **Differenza:** logit e dati pubblici contro insight naturali. **Implicazione:** precedente della catena FedMD→FedProto→FoT.
</details>

<details><summary>FedProto: Federated Prototype Learning across Heterogeneous Clients</summary>

Condivide prototipi di classe nello spazio di embedding per dati non-IID.

**Confronto con FoT–TEP** — **Somiglianza:** conoscenza class-specific compatta. **Differenza:** vettori appresi contro testo citabile. **Implicazione:** baseline concettuale per costo e astrazione.
</details>

<details><summary>FedCKD: Knowledge Distillation with Label-Exclusive Clients</summary>

Studia distillazione cross-client con insiemi di etichette esclusivi.

**Confronto con FoT–TEP** — **Somiglianza:** classi non locali. **Differenza:** logit/parametri e immagini contro evidenza testuale da TS. **Implicazione:** il regime class-disjoint non è nuovo.
</details>

<details><summary>FedMeta-FFD: Federated Meta-Learning for Fault Diagnosis</summary>

Meta-apprendimento federato per adattare la diagnosi a nuove categorie di guasto con pochi esempi.

**Confronto con FoT–TEP** — **Somiglianza:** federated FDD con categorie nuove. **Differenza:** few-shot parametrico contro knowledge transfer testuale. **Implicazione:** vicino più forte sull'asse FDD.
</details>

<details><summary>Federated Zero-Shot Learning with Mid-Level Semantic Knowledge Transfer</summary>

Trasferisce attributi semantici intermedi per riconoscere classi visive non viste.

**Confronto con FoT–TEP** — **Somiglianza:** semantica condivisa per unseen class. **Differenza:** attributi e immagini contro insight liberi e TS. **Implicazione:** rende distintivo il controllo A/B/E, non lo zero-shot in sé.
</details>

<details><summary>FedMAPS: Federated Meta-Learning with Adaptive Cross-Domain Contrastive Learning for Few-Shot Fault Diagnosis</summary>

Sun et al. (Mechanical Systems and Signal Processing, 2026). Framework federato meta-learning con apprendimento contrastivo cross-dominio adattivo per diagnosi di guasti few-shot in scenari con distribuzione non omogenea e domini operativi diversi tra i client.

DOI: `10.1016/j.ymssp.2026.114273`

**Confronto con FoT–TEP** — **Somiglianza:** federazione + classi di guasto scarse/assenti localmente. **Differenza:** scambio di prototipi e gradienti, non insight testuali; richiede training. **Implicazione:** comparator parametrico per il setting few-shot class-disjoint; FoT–TEP è training-free.
</details>

<details><summary>FedAPA-FD: Class-Sensitive Personalized Federated Learning for Non-IID Bearing Fault Diagnosis</summary>

Yu et al. (ICMTIM 2026). Personalizza l'aggregazione federata con pesi class-sensitive per gestire label-skew tra client nel bearing fault diagnosis.

DOI: `10.1109/icmtim69588.2026.11525891`

**Confronto con FoT–TEP** — **Somiglianza:** non-IID label-exclusive, personalizzazione per client. **Differenza:** aggregazione parametrica su modelli specializzati, non testo. **Implicazione:** rafforza l'evidenza che il class-disjoint FD è un problema attivo; FoT–TEP offre un'alternativa senza parametri condivisi.
</details>

<details><summary>Federated Meta-Learning with Transformer Fusion for Few-Shot Multi-Condition Fault Diagnosis</summary>

Zhang et al. (Knowledge-Based Systems, 2026). Combina meta-learning federato con fusione di feature via transformer e training avversariale per diagnosi few-shot sotto condizioni operative multiple, testato anche su TEP.

DOI: `10.1016/j.knosys.2026.116739`

**Confronto con FoT–TEP** — **Somiglianza:** TEP come benchmark, classi di guasto distribuite. **Differenza:** scambio di rappresentazioni intermedie, non insight linguistici. **Implicazione:** benchmark numerico diretto; FoT–TEP potrebbe raggiungere accuratezze simili senza scambio di feature.
</details>

<details><summary>Federated Learning Based on Fuzzy Fusion Rules for Chemical Production Process Fault Diagnosis</summary>

Xu et al. (Sensors, 2026). Applica regole di fusione fuzzy all'aggregazione federata per la diagnosi di guasti in processi chimici, incluso il Tennessee Eastman Process.

DOI: `10.3390/s26113545`

**Confronto con FoT–TEP** — **Somiglianza:** FL + TEP, stessa piattaforma sperimentale. **Differenza:** aggregazione parametrica con logica fuzzy, nessun layer testuale. **Implicazione:** comparator diretto per accuracy su TEP in setting FL; condivide la motivazione industriale.
</details>

### TS→text fedele e deterministico

<details><summary>Truth-Conditional Captions for Time Series Data</summary>

TRUCE compone programmi di pattern e genera una caption solo quando il programma ne rende vere le condizioni; i moduli restano appresi.

**Confronto con FoT–TEP** — **Somiglianza:** enfasi sulla fedeltà. **Differenza:** caption neurale monovariata contro renderer deterministico multivariato. **Implicazione:** definire con precisione “fedele per costruzione”.
</details>

<details><summary>A Fuzzy Approach to Data-to-Text for Time Series</summary>

Pipeline deterministica a variabili fuzzy, regole e template.

**Confronto con FoT–TEP** — **Somiglianza:** testo auditabile. **Differenza:** soglie di dominio contro calibrazione statistica e separazione evidence/inference. **Implicazione:** predecessore metodologico del verbalizzatore.
</details>

<details><summary>ICA2TEXT: Data-to-Text for Air-Quality Time Series</summary>

Seleziona e realizza linguisticamente fatti temporali sulla qualità dell'aria con una pipeline deterministica.

**Confronto con FoT–TEP** — **Somiglianza:** fatti separati dalla realizzazione testuale. **Differenza:** reporting ambientale, non diagnosi distribuita. **Implicazione:** supporta l'architettura a strati.
</details>

<details><summary>Representing Time Series as Structured Programs for LLM Reasoning (T2SP)</summary>

Decompone serie univariate in trend, periodicità, eventi e residuo come programma training-free e invertibile.

**Confronto con FoT–TEP** — **Somiglianza:** rappresentazione compatta e verificabile. **Differenza:** ricostruibilità numerica contro giudizi calibrati multivariati. **Implicazione:** competitor metodologico più forte; misurare perdita informativa.
</details>

<details><summary>CGTime: Decoupling Perception from Description in Time-Series Reasoning</summary>

Calcola 169 statistiche, usa un encoder temporale e addestra un LLM a verbalizzare fatti computati.

**Confronto con FoT–TEP** — **Somiglianza:** percezione separata dalla descrizione. **Differenza:** training e testo generativo contro template congelati e neutrali. **Implicazione:** la tesi difendibile è efficienza/auditabilità, non superiorità di accuracy.
</details>

<details><summary>On-the-Fly Signals-to-Semantics Storytelling for Explainable Industrial Maintenance Decisions</summary>

Yue et al. (IEEE Transactions on Automation Science and Engineering, 2026). Framework che trasforma segnali di sensori industriali in narrazioni semantiche in tempo reale per decisioni di manutenzione spiegabili, separando la percezione numerica dalla generazione linguistica.

DOI: `10.1109/TASE.2026.3706386`

**Confronto con FoT–TEP** — **Somiglianza:** pipeline signals→semantics per contesto industriale, separazione percezione/narrazione. **Differenza:** narrazione monolitica, non federata; generazione on-the-fly vs batch. **Implicazione:** validazione indipendente che la conversione TS→testo è praticabile nell'industria; il verbalizzatore V2 potrebbe adottare pattern analoghi.
</details>

### Rappresentazioni simboliche

<details><summary>A Novel Feature Extraction Approach for Mechanical Fault Diagnosis Based on ESAX and BoW</summary>

ESAX produce stringhe simboliche trasformate in conteggi Bag-of-Words per classificatori classici.

**Confronto con FoT–TEP** — **Somiglianza:** compressione deterministica. **Differenza:** feature numeriche, non testo o federazione. **Implicazione:** baseline di rappresentazione, non del reasoning linguistico.
</details>

<details><summary>Bridging Time Series and Large Language Models via Symbolic Representation for HAR</summary>

Combina SAX e descrittori cinematici e fine-tuna un LLM per activity recognition, con notevole costo d'inferenza.

**Confronto con FoT–TEP** — **Somiglianza:** ponte simbolico segnale–LLM. **Differenza:** fine-tuning centralizzato contro in-context e testo leggibile. **Implicazione:** giustifica SAX nell'ablation e il reporting del costo.
</details>

<details><summary>HSQP: Hierarchical Symbolic Quantization Prompting for Time-Series Forecasting</summary>

Quantizza la serie su più risoluzioni e fornisce token simbolici a un LLM congelato.

**Confronto con FoT–TEP** — **Somiglianza:** encoder deterministico e consumer frozen. **Differenza:** forecasting e token contro diagnosi e testo tecnico. **Implicazione:** la leggibilità è una scelta da valutare.
</details>

<details><summary>LLM-ABBA: Understanding Time Series via Symbolic Approximation</summary>

Carson, Chen & Kang (Qeios, 2025; rev. 2026). Integra la discretizzazione simbolica ABBA (Adaptive Brownian Bridge-based Aggregation) nei LLM per classificazione, regressione e previsione di serie temporali. ABBA preserva ampiezza e periodo con token esistenti del vocabolario LLM, raggiungendo SOTA su UCR e TSER benchmark.

DOI: `10.32388/wd5bow.2`

**Confronto con FoT–TEP** — **Somiglianza:** ponte simbolico TS→LLM, preservazione di feature salienti. **Differenza:** ABBA è adattivo e appreso, V2 è deterministico e rule-based; nessun contesto federato. **Implicazione:** alternativa alla pipeline SAX/eSAX per il verbalizzatore; la confrontabilità ABBA vs eSAX misura il trade-off flessibilità/determinismo.
</details>

### Allineamento e captioning TS–linguaggio

<details><summary>T3: Domain-Agnostic Neural Time-Series Narration</summary>

Genera narrazioni domain-agnostic tramite una rappresentazione intermedia e un modello neurale.

**Confronto con FoT–TEP** — **Somiglianza:** TS consumabile come linguaggio. **Differenza:** generazione libera contro renderer vincolato. **Implicazione:** più ricco, meno auditabile.
</details>

<details><summary>Repr2Seq: Time Series Representation to Sequence</summary>

Apprende end-to-end la mappatura da serie, soprattutto finanziarie, a testo.

**Confronto con FoT–TEP** — **Somiglianza:** output naturale. **Differenza:** richiede coppie TS-testo e non garantisce fedeltà. **Implicazione:** rappresenta il trade-off adattività/controllo.
</details>

<details><summary>TADACap: Time-Series Image Retrieval for Domain-Aware Captioning</summary>

Usa immagini di serie e retrieval contestuale per caption domain-aware.

**Confronto con FoT–TEP** — **Somiglianza:** testo contestuale. **Differenza:** rendering visivo/retrieval contro fatti tabulari calcolati. **Implicazione:** futuro braccio multimodale.
</details>

<details><summary>CLaSP: Contrastive Language–Signal Pretraining</summary>

Allinea embedding di segnali e descrizioni per retrieval cross-modale.

**Confronto con FoT–TEP** — **Somiglianza:** collega struttura temporale e semantica. **Differenza:** spazio latente contro testo esplicito. **Implicazione:** possibile matching migliore al costo di trasparenza.
</details>

<details><summary>TSLM: Time-Series Language Model for Captioning</summary>

Encoder temporale e decoder linguistico apprendono da coppie serie-caption a descrivere pattern salienti.

**Confronto con FoT–TEP** — **Somiglianza:** descrizioni leggibili. **Differenza:** caption data-hungry contro template calibrato. **Implicazione:** utile come descrizione secondaria con fact checking.
</details>

<details><summary>TableTime: Training-Free Table Understanding for Time Series Classification with LLMs</summary>

Wang et al. (CIKM 2025, 6 citazioni). Riformula la classificazione di serie temporali come comprensione tabulare, permettendo a LLM frozen di classificare senza fine-tuning. I dati numerici vengono presentati come tabelle strutturate nel prompt.

DOI: `10.1145/3746252.3761056`

**Confronto con FoT–TEP** — **Somiglianza:** LLM frozen, TS presentata come testo strutturato, training-free. **Differenza:** rappresentazione tabulare diretta vs verbalizzazione con template; nessuna componente federata. **Implicazione:** conferma la fattibilità di classificazione TS con LLM frozen; benchmark per V2 in assenza di training.
</details>

<details><summary>Towards Semantically Faithful Text-to-Time Series Generation via Agents and Spectral Conditioning</summary>

Wu et al. (ICASSP 2026). Affronta la generazione text→TS con condizionamento spettrale e orchestrazione agentica per preservare la fedeltà semantica tra descrizione testuale e serie temporale generata.

DOI: `10.1109/icassp55912.2026.11463399`

**Confronto con FoT–TEP** — **Somiglianza:** fedeltà semantica nella traduzione testo↔TS. **Differenza:** direzione inversa (text→TS), non TS→text; focus su generazione, non diagnosi. **Implicazione:** le metriche di fedeltà spettrale possono validare indirettamente il verbalizzatore V2: se la TS ricostruita dal testo V2 preserva lo spettro, la verbalizzazione è fedele.
</details>

### LLM per fault diagnosis

<details><summary>FD-LLM: Large Language Model for Fault Diagnosis of Machines</summary>

Serializza FFT o statistiche e fine-tuna LLM open-weight con LoRA per diagnosi multiclass su CWRU.

**Confronto con FoT–TEP** — **Somiglianza:** segnali resi sequenze per LLM. **Differenza:** classi note e training centralizzato contro consumer frozen e insight remoti. **Implicazione:** forte baseline supervisionato, ma problema differente.
</details>

<details><summary>FD-LLM: Large Language Model for Fault Diagnosis of Complex Equipment</summary>

Allinea encoder dati a embedding testuali, aggiunge semantica fuzzy e adatta Vicuna con LoRA.

**Confronto con FoT–TEP** — **Somiglianza:** diagnosi mediata dal linguaggio. **Differenza:** pipeline addestrata end-to-end con label note. **Implicazione:** alza l'asticella centralizzata senza coprire il trasferimento federato.
</details>

<details><summary>LLM-TSFD: Industrial Time-Series Human-in-the-Loop Fault Diagnosis</summary>

Estrae feature, usa template testuali diagnostici e guida l'LLM con tassonomie e alberi decisionali.

**Confronto con FoT–TEP** — **Somiglianza:** pipeline estrai→verbalizza→ragiona. **Differenza:** soglie manuali e template diagnostici contro calibrazione e neutralità. **Implicazione:** riferimento diretto per freeze e separazione evidence/inference.
</details>

<details><summary>EviFDD-Agent: Evidence-Traceable LLM Reporting for Industrial Process Fault Detection and Diagnosis</summary>

Chen et al. (SSRN preprint, 2026). Framework ReAct per diagnosi di guasti su TEP con tracciabilità dell'evidenza: i campi critici del report sono prodotti da tool deterministici, il LLM è confinato alla narrazione vincolata. EviFDD-Agent con DeepSeek-V4-Flash raggiunge EFT = 0.997 e URR = 1.4 % su 210 casi TEP.

DOI: `10.2139/ssrn.6778889`

**Confronto con FoT–TEP** — **Somiglianza:** TEP benchmark, LLM per diagnosi, separazione evidence/inference, tracciabilità. **Differenza:** centralizzato, non federato; il LLM genera report post-hoc, non riceve insight da peer. **Implicazione:** comparator diretto per accuracy su TEP; il pattern evidence-traceable è compatibile con la pipeline FoT.
</details>

<details><summary>CL-LLMOps: Fuzzy-Gated Verification of LLM Agents for Industrial Fault Diagnosis</summary>

Xiao et al. (SSRN preprint, 2026). Closed-loop framework che orchestra agenti LLM attraverso cinque fasi, con verifica semantica tramite fuzzy inference per rilevare hallucination ed evidenze contraddittorie prima delle decisioni di manutenzione. Riduce l'inconsistency-type hallucination dal 12 % al 2 %.

DOI: `10.2139/ssrn.6778404`

**Confronto con FoT–TEP** — **Somiglianza:** agenti LLM per fault diagnosis, rilevamento hallucination. **Differenza:** verifica fuzzy centralizzata, non calibrazione conforme distribuita. **Implicazione:** rafforza la necessità del controllo di qualità sugli output LLM; il gating fuzzy è complementare alla calibrazione conforme di V2.
</details>

<details><summary>DML–LLM Hybrid Architecture for Fault Detection and Diagnosis in Sensor-Rich Industrial Systems</summary>

Hu et al. (Sensors, 2026). Architettura ibrida che combina Dynamic Master Logic (ragionamento causale deterministico con regole fuzzy) e LLM per FDD. Il routing deterministico preserva tracciabilità; il LLM interpreta log e documenti sotto prompt controllati. Su semiconduttori: TTD da 7.4 h a 1.2 h, F1 da 0.59 a 0.83.

DOI: `10.3390/s26062008`

**Confronto con FoT–TEP** — **Somiglianza:** pipeline deterministica + LLM, tracciabilità, routing causale. **Differenza:** monolitico, non federato; ragionamento Bayesiano vs in-context. **Implicazione:** il pattern "regole deterministiche → LLM confinato" è convergente con V2; valida la separazione evidence layer / reasoning layer.
</details>

### Survey e benchmark

<details><summary>BEDTime: A Unified Benchmark for Automatically Describing Time Series</summary>

Circa 46.800 coppie serie-descrizione su tre task; mostra vantaggio dei VLM e fragilità alle perturbazioni, ma non valuta renderer deterministici.

**Confronto con FoT–TEP** — **Somiglianza:** qualità semantica delle descrizioni. **Differenza:** captioning generale, non diagnosi federata. **Implicazione:** adattare metriche e stress test a V2.
</details>

<details><summary>Empowering Time Series Analysis with Large Language Models: A Survey</summary>

Organizza forecasting, classificazione, anomaly detection e generazione con prompting, alignment e reprogramming.

**Confronto con FoT–TEP** — **Somiglianza:** quadro TS–LLM. **Differenza:** non copre in profondità testo federato class-disjoint. **Implicazione:** delimita il contributo.
</details>

<details><summary>Time-Series Large Language Models: A Systematic Review</summary>

Rassegna architetture, task, dataset e modalità di integrazione, evidenziando frammentazione valutativa e generalizzazione debole.

**Confronto con FoT–TEP** — **Somiglianza:** contesto per representation choice ed evaluation. **Differenza:** panoramica, non comparator. **Implicazione:** sostiene protocolli riproducibili e claim prudenti.
</details>

<details><summary>Large Language Models for Time-Series Reasoning: A TMLR Survey</summary>

Estende la tassonomia verso reasoning, tool use e agenti, distinguendo percezione numerica, rappresentazione e decisione.

**Confronto con FoT–TEP** — **Somiglianza:** reasoning agentico con percezione esternalizzata. **Differenza:** nessun protocollo FoT o controllo derangiato. **Implicazione:** V2 è perception layer; gli insight sono knowledge/memory layer.
</details>

<details><summary>Federated Reasoning LLMs: A Survey</summary>

Wei et al. (Frontiers of Computer Science, 2025, 19 citazioni). Survey sistematica su LLM di ragionamento federato. Propone tassonomia basata sui segnali di training (dati raw, rappresentazioni apprese, feedback di preferenza) e analizza efficacia, costo comunicativo e preservazione della privacy per ciascuna categoria.

DOI: `10.1007/s11704-025-50480-3`

**Confronto con FoT–TEP** — **Somiglianza:** quadro generale FL + LLM reasoning, include comunicazione e privacy. **Differenza:** focus su fine-tuning distribuito di rLLM, non su insight testuali come oggetto federato. **Implicazione:** mappa lo spazio dei metodi; FoT–TEP si colloca nell'estremo "zero-parameter, text-only" non coperto dalla survey.
</details>

### Calibrazione e predizione conforme

<details><summary>Uncertainty-Aware Fault Diagnosis with Conformal Prediction</summary>

Heddoub et al. (IFAC-PapersOnLine, 2025, 7 citazioni). Introduce la conformal prediction nella diagnosi di guasti industriali per produrre set di predizione con garanzie di copertura statistiche, quantificando l'incertezza del classificatore senza ipotesi distributive.

DOI: `10.1016/j.ifacol.2025.09.092`

**Confronto con FoT–TEP** — **Somiglianza:** calibrazione per fault diagnosis industriale, garanzie di copertura. **Differenza:** applicata a classificatori tradizionali, non a LLM; centralizzata. **Implicazione:** fondamento teorico per la calibrazione conforme del verbalizzatore V2; le soglie A/B/E di FoT–TEP perseguono lo stesso obiettivo con metodo diverso.
</details>

<details><summary>Class-Conditional Conformal Prediction for Reliable Open-Set Fault Diagnosis in Safety-Critical Industrial Systems</summary>

Heddoub et al. (Journal of Process Control, 2026, 2 citazioni). Estende la conformal prediction al setting open-set: il modello deve diagnosticare guasti noti e rifiutare (astenersi su) classi mai viste, con garanzie per-classe.

DOI: `10.1016/j.jprocont.2026.103701`

**Confronto con FoT–TEP** — **Somiglianza:** open-set ≈ class-disjoint visto dal singolo client; astensione su classi non viste. **Differenza:** approccio statistico su feature, non linguistico. **Implicazione:** il meccanismo di astensione è il ponte con la selective prediction di FoT–TEP: quando V2 non riconosce un pattern, la conformal prediction offre un framework rigoroso per il rifiuto.
</details>

### To do

Tutte le 12 query sono state eseguite su OpenAlex, arXiv, Scopus e Crossref tramite il connector uniarticles. Sono stati aggiunti 15 paper. Riepilogo per query:

- ✅ `("federated knowledge transfer" OR …) AND "time series"` — nessun paper specifico (intersezione troppo stretta); coperta indirettamente da Federated Reasoning LLMs Survey e FedSRD
- ✅ `("class-disjoint" OR …) AND federated AND diagnosis` — FedMAPS, FedAPA-FD
- ✅ `("federated fault diagnosis" OR …) AND "Tennessee Eastman" AND non-IID` — Zhang et al. KBS 2026, Xu et al. Sensors 2026, EviFDD-Agent
- ✅ `("semantic specificity" OR …) AND "in-context learning"` — nessun risultato rilevante nella query eseguita; ciò non dimostra un'assenza assoluta di precedenti
- ✅ `("time series to text" OR verbalization) AND faithfulness` — Faithful Text-to-TS (Wu ICASSP 2026)
- ✅ `("deterministic verbalization" OR …) AND "time series" AND LLM` — Signals-to-Semantics (Yue IEEE TASE 2026)
- ✅ `(SAX OR symbolic) AND LLM AND "fault diagnosis"` — LLM-ABBA (Carson et al. 2025/2026)
- ✅ `("negative transfer" OR interference) AND federated AND prompt` — nessun paper specifico emerso dalla query all’intersezione FoT
- ✅ `("communication cost" OR payload) AND federated LLM` — Federated Reasoning LLMs Survey (Wei et al. 2025), FedSRD (Yan et al. 2026)
- ✅ `("selective prediction" OR abstention OR calibration) AND LLM AND industrial` — CL-LLMOps, DML–LLM Hybrid, Conformal FD (Heddoub 2025, 2026)
- ✅ `("frozen LLM" OR "training-free") AND "time series"` — TableTime (Wang et al. CIKM 2025)
- ✅ `("causal evaluation" OR placebo) AND "knowledge sharing" AND multi-agent` — nessun risultato emerso dalla query eseguita

**Query senza risultati rilevanti** (4, 8, 12): delimitano il corpus consultato, ma non provano l'assenza assoluta di precedenti. Sostengono soltanto un claim prudente sulla combinazione studiata, formulato come *to the best of our knowledge*.

**Possibili estensioni future:** monitorare preprint su arXiv per le query 4, 8, 12; cercare su Google Scholar con citazione diretta di “Federation over Text” per lavori derivati.

---

## Paper

*In arrivo*
