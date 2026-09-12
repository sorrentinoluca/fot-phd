# Federation over Text for Locally Unseen Fault Diagnosis in Multivariate Time Series

*Documentazione sperimentale interna — versione 2. Destinata all'autore e ai colleghi, per comprendere, discutere e riprodurre il lavoro. Non contiene testo destinato a essere copiato nel paper.*

---

## 0 · Come leggere questo documento

Questo documento presenta un **framework sperimentale di base per il trasferimento federato di conoscenza testuale**. È organizzato per domande e funzioni, non secondo l'ordine in cui il lavoro è stato costruito.

### 0.1 Che cosa trova, e dove

| Se vuole sapere… | Vada a |
| --- | --- |
| perché esiste questo esperimento e che cosa chiede | §1 |
| perché sono stati scelti questo processo, questi agenti e questi guasti | §2 |
| come i numeri dei sensori diventano testo verificabile | §3 |
| come nasce e come circola la conoscenza testuale | §4 |
| che cosa distingue le quattro condizioni sperimentali | §5 |
| come si conta, che cosa è l'unità statistica, come si costruiscono gli intervalli | §6 |
| il risultato principale | §7 |
| se il risultato si ripete su dati nuovi | §8 |
| come si colloca rispetto a metodi numerici e a riferimenti centralizzati | §9 |
| quanto tiene il risultato sotto verifiche indipendenti | §10 |
| quanto testo viene effettivamente scambiato | §11 |
| che cosa si può e non si può concludere | §12 |
| come si colloca rispetto alla conferenza | §13 |
| che cosa esiste in letteratura | §14 |
| dove verificare ogni numero | §15 |

### 0.2 Nomi usati in questo documento

La numerazione tecnica presente negli artefatti e nei documenti precedenti è confusa: coesistevano tre sistemi (`Step N`, `Fase 1/2/3`, `Experiment 1/2/3`) con corrispondenze contro-intuitive. Qui si usano nomi funzionali. Gli identificativi tecnici compaiono una volta tra parentesi e nelle tabelle di provenienza di §15.

| Nome usato qui | Identificativo tecnico |
| --- | --- |
| Studio principale | Experiment 1 · Phase B |
| Replica su nuovi run | EXP3_V2 · Experiment 3 |
| Verifica con un altro LLM | Experiment 2 · lane Qwen |
| Condizione senza insight (A) | Condition A · isolated |
| Controllo local-only (A+) | Condition A+ · local-only self-insight |
| Condizione federata (B) | Condition B · FoT |
| Condizione con associazioni corrotte (E) | Condition E · corrupted |
| Riferimento testuale centralizzato | Condition C · centralized pooled ICL |
| Baseline numerica condivisa | Baseline a prototipi numerici condivisi |
| Baseline numerica local-only | Braccio local-only della stessa baseline |
| Riferimenti ML centralizzati | Suite di otto modelli centralizzati |
| Confronto delle rappresentazioni | Ablation TS→testo |
| Sensibilità al budget di ragionamento | Sensitivity analysis sul reasoning cap |
| Approfondimento sui casi al limite | Follow-up capped a 4096 token |
| Variante local-first | `B_LOCAL_FIRST_V1` |
| Costo della comunicazione | Communication payload characterization |

### 0.3 Glossario minimo

- **Agente** — un nodo diagnostico. Nell'esperimento è una configurazione di prompt su un modello linguistico frozen, non un impianto fisico.
- **Sensore (variabile misurata XMEAS)** — un canale del processo. Il simulatore ne registra 41; nel testo breve viene chiamato semplicemente *sensore XMEAS*.
- **Run** — una simulazione indipendente del processo, con o senza guasto.
- **Batch** — il numero assegnato a un run nel dataset originale. Per esempio, *F1 batch 1* è il primo run disponibile di F1.
- **Finestra** — una porzione temporale di un run. Non è un nuovo run e non è un'unità sperimentale indipendente.
- **Misura calcolata (feature)** — un numero ricavato dalle misure grezze di un sensore dentro una finestra, per esempio lo spostamento della media.
- **Funzionamento normale (Normal)** — la classe senza guasto, usata per costruire il riferimento e come possibile risposta diagnostica.
- **Coppia agente–run** — l'unità elementare di valutazione: un agente giudica un run. Negli artefatti si chiama *agent-case*.
- **Guasto già noto localmente** — il run appartiene alla classe di guasto che quell'agente conosce (*local-seen*).
- **Guasto mai visto da quell'agente** — il run appartiene a una classe che quell'agente non ha nella propria esperienza locale (*local-unseen*). È la popolazione primaria.
- **Testo neutrale** — la descrizione di un singolo run prodotta da regole fisse, senza nomi di guasto e senza diagnosi.
- **Insight** — una breve unità di conoscenza testuale che sintetizza ciò che un agente ha appreso da più testi neutrali. *Testo neutrale* e *insight* non sono sinonimi.
- **Pseudolabel** — un'etichetta opaca (`CLS-…`) che sostituisce il nome reale del guasto nel materiale mostrato al modello.
- **Contenuto trasmesso (payload)** — l'insieme degli insight inviati agli altri agenti.
- **Congelato prima della valutazione** — la configurazione è stata fissata e verificata con hash prima di eseguire la valutazione corrispondente, e non è più stata modificata.

### 0.4 Gerarchia delle fonti

Il Markdown è la **fonte editoriale principale** dei documenti V2. I numeri e le conclusioni **derivano dagli artefatti sperimentali verificati**. La replica HTML lunga è una replica fedele di questo Markdown.

In caso di conflitto vale questo ordine:

1. risultati sperimentali, rapporti verificati e configurazioni congelate;
2. artefatti e manifest tecnici;
3. la documentazione discorsiva precedente;
4. il blueprint del paper;
5. le versioni HTML, che sono copie o sintesi.

Nessun dato è stato accettato perché proveniente dal documento più recente: ogni valore riportato qui è stato verificato nell'artefatto corrispondente. §15 dice dove.

### 0.5 Categorie usate per qualificare le prove

Non tutte le prove hanno lo stesso valore, e il documento lo dichiara ogni volta.

| Categoria | Significato |
| --- | --- |
| Studio principale | Disegno e criteri fissati prima della propria valutazione |
| Replica su nuovi dati | Stesso disegno applicato a realizzazioni simulate nuove |
| Controllo aggiuntivo | Condizione che esclude una spiegazione alternativa specifica |
| Confronto esterno | Metodo diverso valutato sullo stesso compito |
| Riferimento descrittivo | Metodo non confrontabile alla pari, usato per collocare il risultato |
| Analisi di sensibilità | Variazione controllata di un parametro operativo |
| Verifica diagnostica | Intervento definito dopo aver osservato un problema e valutato sullo stesso campione |
| Analisi esplorativa | Confronto introdotto dopo aver visto i risultati, non causale |
| Analisi descrittiva | Decomposizione dei record già congelati, senza nuovo endpoint |

---

## 1 · Obiettivo e domanda scientifica

### 1.1 Il problema

Immagini quattro impianti dello stesso tipo. Ciascuno osserva le proprie serie temporali e i propri eventi. Nella pratica non tutti i guasti capitano ovunque: ogni sito accumula esperienza su ciò che gli è successo, e resta cieco sul resto. Quando in un sito si presenta un guasto che lì non è mai occorso, chi lo osserva non ha modo di riconoscerlo.

La domanda è se sia possibile dare a un nodo la conoscenza che gli manca **senza condividere le serie temporali grezze né i parametri di un modello**. Il vincolo è importante e va enunciato con precisione: quello che circola sono descrizioni testuali, che derivano comunque dai dati locali. Non è vero che «non esce nulla»; è vero che non escono né le serie né i pesi.

### 1.2 La domanda scientifica

> Un agente può usare conoscenza testuale prodotta da altri agenti per riconoscere un tipo di guasto assente dalla propria esperienza locale?

Non è la domanda «FoT risolve la diagnosi dei guasti?», e non è la domanda «FoT è il metodo migliore per questo compito?». È una domanda sul **meccanismo**: il testo può funzionare come veicolo di conoscenza discriminante fra nodi con esperienza diversa?

Il confronto primario è **B−A**: la condizione con gli insight dei peer contro la condizione senza insight, sui guasti mai visti da quell'agente. Il confronto di supporto è **B−E**: gli stessi insight con le associazioni semantiche corrotte, per distinguere l'effetto del contenuto da quello del semplice volume di testo. B−E non è un secondo endpoint primario.

### 1.3 Attribuzione

**Federation over Text (FoT) è stato introdotto da Yao et al.**, *Federation over Text: Insight Sharing for Multi-Agent Reasoning* ([arXiv:2604.16778](https://arxiv.org/abs/2604.16778), repo [github.com/dixiyao/FoT](https://github.com/dixiyao/FoT)). In FoT, agenti con LLM frozen distillano tracce di ragionamento in insight, che vengono aggregati e ridistribuiti come testo, senza gradienti né fine-tuning. Yao et al. valutano il paradigma su compiti testuali di matematica, question answering e coding.

Questo lavoro **non propone FoT** e non propone la federazione testuale. Riprende l'architettura ad alto livello — insight locali, ridistribuzione, consumo in contesto — e la applica a un dominio diverso.

### 1.4 Perimetro del contributo

Il contributo è circoscritto alla combinazione dei seguenti elementi, non a ciascuno di essi preso singolarmente:

1. serie temporali industriali multivariate come dominio;
2. esperienza locale disgiunta per classe: ogni agente conosce il funzionamento normale e un solo guasto;
3. valutazione su guasti localmente non osservati;
4. pseudolabel opache, che impediscono al modello di rispondere usando conoscenza pregressa sul processo invece dell'evidenza trasferita;
5. verbalizzazione deterministica e verificabile: ogni frase è riconducibile ai numeri di partenza;
6. trasferimento di insight testuali fra pari, senza server di aggregazione;
7. controllo semantico B/E a parità di testo, ordine e volume;
8. confronto con il controllo local-only A+;
9. protocollo congelato prima della propria valutazione;
10. replica su realizzazioni simulate nuove;
11. confronto numerico sullo stesso compito;
12. portabilità lato consumatore verso un secondo modello;
13. caratterizzazione del payload comunicativo.

La formulazione di novità più prudente resta: *«To the best of our knowledge, this is the first controlled study of federated textual knowledge transfer for locally unseen fault diagnosis in multivariate industrial time series.»* Il perimetro del corpus consultato che sostiene questa formulazione è descritto in §14.

### 1.5 Che cosa questo documento non sostiene

Il framework, così com'è, non dimostra superiorità diagnostica, garanzie di privacy, scalabilità, efficienza di comunicazione, generalizzazione industriale, equivalenza con FedAvg o FedProto, né funzionamento in mondo aperto. §12 raccoglie i limiti in modo sistematico.

---

## 2 · Il banco di prova: TEP, agenti, guasti

Questa sezione raccoglie le motivazioni di disegno. Per ciascuna è indicata la natura della giustificazione: letteratura, caratteristiche dei dati, necessità sperimentale, scelta tecnica, limite pratico. Dove gli artefatti non documentano una motivazione ulteriore, il documento lo dichiara invece di costruirne una a posteriori.

### 2.1 Perché il Tennessee Eastman Process

*Natura della motivazione: necessità sperimentale.*

Il TEP è un impianto chimico simulato. Offre guasti noti, una risposta corretta verificabile e run distinti e ripetibili. Questo permette di verificare il framework in condizioni controllate. Il framework è pensato per altri domini di serie temporali industriali, ma questo lavoro non ne dimostra ancora la trasferibilità.

I dati provengono dallo snapshot upstream [github.com/mv-per/tennessee-eastman-dataset](https://github.com/mv-per/tennessee-eastman-dataset), commit pinnato `309b944f`. La pipeline legge da ogni file la colonna `Time` più **41 sensori, registrati come variabili misurate XMEAS**, campionati a un minuto.

### 2.2 I dati usati

| Tipo | Struttura | Uso |
| --- | --- | --- |
| Normal | un file da 500 h, 30 001 righe, diviso in 10 blocchi da 50 h (N1…N10) | riferimento e casi normali |
| Guasto | un file per run, 50 h, 3 001 righe; guasto iniettato a 10 h | casi di guasto |

L'ultima riga del file Normal, l'endpoint a 500 h, viene esclusa: 30 000 righe si dividono esattamente in dieci blocchi da 50 h.

I file di guasto contengono anche **12 variabili manipolate XMV**. Vengono escluse. *Natura della motivazione: limite pratico e procedurale.* Il layer di rappresentazione è stato definito sulle sole XMEAS e congelato così; aggiungere le XMV dopo aver osservato i dati modificherebbe la rappresentazione a valle del congelamento. Non è una scelta motivata da ragioni fisiche o diagnostiche.

### 2.3 Perché quattro agenti

*Natura della motivazione: scelta di disegno. Gli artefatti non documentano una motivazione ulteriore.*

Quattro agenti è il numero minimo che, con un solo guasto conosciuto per agente, consente contemporaneamente di avere quattro classi di guasto distinte e, per ogni run di guasto, un agente informato e tre non informati. La struttura del conteggio dipende da questo: ogni run produce una coppia su guasto già noto e tre coppie su guasto mai visto. Non risulta documentata negli artefatti una motivazione che vada oltre questa convenienza strutturale, e non ne viene costruita una a posteriori.

### 2.4 Perché ogni agente conosce il funzionamento normale e un solo guasto

*Natura della motivazione: necessità sperimentale.*

È la condizione che rende possibile la domanda. Se ogni agente conoscesse più guasti, la nozione di «guasto mai visto da quell'agente» si diluirebbe e il confronto primario perderebbe significato. La disgiunzione per classe è la forma estrema di eterogeneità fra nodi: dati diversi tra gli agenti, per costruzione.

### 2.5 Perché F1, F8, F10 e F13

*Natura della motivazione: letteratura (tassonomia dei comportamenti documentati) più caratteristiche dei dati (osservazione a posteriori sulle firme).*

Il **dataset utilizzato contiene i 21 guasti standard del Tennessee Eastman Process**, raggruppati per meccanismo nella tassonomia originale di Downs & Vogel (1993): *gradino (Step)* (F1–F7), *variazione casuale (Random variation)* (F8–F12), *deriva lenta (Slow drift)* (F13), *blocco (Sticking)* (F14–F15), *meccanismo non specificato (Unknown)* (F16–F20), più il guasto a valvola fissa F21. Il simulatore modificato espone 28 ingressi di disturbo, ma questi **non vanno presentati come 28 classi di guasto**. L'esperimento valuta quattro guasti standard: F1, F8, F10 e F13.

I quattro guasti coprono tre famiglie di comportamento documentate. **F1** rappresenta un cambiamento improvviso e persistente. **F8** e **F10** appartengono entrambi alla famiglia delle variazioni casuali: la loro presenza permette di verificare se il metodo distingue guasti della stessa famiglia che interessano variabili diverse. **F13** introduce invece una deriva lenta, la cui firma emerge gradualmente e si sovrappone a lungo al comportamento nominale.

Gli altri guasti non sono stati valutati perché lo studio è limitato a quattro classi; **i risultati non permettono di stabilire che siano ridondanti o inadatti**.

L'analisi delle firme a 697 dimensioni descrive a posteriori come si collocano le quattro classi. È una caratterizzazione del campione osservato, non una scala di difficoltà generale: le difficoltà rilevate dipendono da questo esperimento e da questa rappresentazione.

| Guasto | Meccanismo | Similarità dentro la classe | Margine dal Normal | Nota |
| --- | --- | ---: | ---: | --- |
| F1 | Gradino (Step) | 0,991 | 0,077 | firma stabile, ben separata |
| F10 | Variazione casuale (Random variation) | 0,991 | 0,011 | stabile ma vicina a F1 (0,905 fra le due classi) |
| F8 | Variazione casuale (Random variation) | 0,860 | 0,014 | la meno stabile fra le quattro: massima variabilità interna |
| F13 | Deriva lenta (Slow drift) | 0,889 | 0,044 | minima similarità col Normal (0,718), deriva graduale |

### 2.6 Come sono divisi i dati

| Split | Guasti (F1, F8, F10, F13) | Normal | Ruolo |
| --- | --- | --- | --- |
| Sviluppo e calibrazione | batch 1–5 | N1–N5 | costruisce e calibra il metodo |
| Validazione | batch 6–7 | N6–N7 | controllo fuori sviluppo, nessuna taratura |
| Test | batch 8–10 | N8–N10 | verifica finale, aperto dopo il congelamento |

I run di guasto vengono analizzati solo dopo l'iniezione: le 40 h successive alle prime 10 h producono **otto finestre da 5 h** (W1…W8, da `[10,15)` a `[45,50)`). Un blocco Normal completo, 50 h, ne produce dieci.

*Natura della motivazione della finestra da 5 h: scelta di disegno. Gli artefatti non documentano una motivazione ulteriore* — la durata non risulta ottimizzata né confrontata con alternative; discende dall'intervallo post-guasto di 40 h e dall'ottenere otto finestre per run.

Una finestra è una porzione descrittiva dello stesso run, **non un run indipendente**. La distinzione torna decisiva in §6, quando si contano i casi statisticamente indipendenti.

---

## 3 · Dalla serie temporale al testo

Questa è la parte deterministica del framework: nessun modello linguistico interviene. Le regole vengono definite una volta, congelate, e da lì in avanti soltanto applicate.

### 3.1 Le sei operazioni

| Ordine | Operazione | Quando, e che cosa produce |
| --- | --- | --- |
| 1 | Scelta delle feature | decisione di progetto, eseguita una volta: si caratterizzano i guasti batch 1–5 per decidere **quali** feature usare; qui non si calcolano soglie |
| 2 | Calibrazione delle soglie | eseguita **soltanto** sui blocchi Normal N1–N5, senza guardare i guasti; produce riferimento e soglie |
| 3 | Congelamento | fissa feature, riferimento, soglie, struttura e renderer |
| 4 | Calcolo delle feature e applicazione delle soglie | a runtime, per ogni finestra × XMEAS: valori e confronto con le soglie già congelate |
| 5 | Dalle finestre alla struttura | aggrega flag e struttura temporale in evidenza numerica verificabile |
| 6 | Dalla struttura al testo neutrale | rende i fatti quantitativi senza identificativi di guasto e senza diagnosi |

La distinzione fra il punto 1 e il punto 4 è sostanziale: la **scelta** delle feature è una decisione presa una volta a monte; il **calcolo** è l'operazione ripetuta su ogni finestra. Confonderli farebbe sembrare che il metodo venga reinventato per ciascun guasto.

### 3.2 Le feature

| Feature | Che cosa quantifica | Che cosa non prova da sola |
| --- | --- | --- |
| `shift_sigma` | spostamento della media, in deviazioni standard del Normal | la causa |
| `slope_sigma_h` | pendenza normalizzata per ora | deriva persistente |
| `residual_std_ratio` | variabilità dopo rimozione del trend | periodicità |
| `diff_std_ratio` | variazioni fra campioni consecutivi | oscillazioni lente |
| `raw_std_ratio` | dispersione descrittiva | instabilità oscillatoria |

### 3.3 Il riferimento normale e la soglia

Prima di dire che qualcosa è cambiato serve sapere com'è quando tutto va bene. Il riferimento si costruisce **solo** dai blocchi Normal N1–N5: cinque blocchi × dieci finestre = 50 finestre.

Per `shift_sigma`, il calcolo è:

```
shift_sigma = (x̄_w − μ₀) / σ₀
```

dove `x̄_w` è la media della stessa XMEAS nella finestra corrente, `μ₀` la media del riferimento Normal per quella variabile e `σ₀` la sua deviazione standard campionaria. Il confronto con la soglia usa il modulo; il segno resta disponibile nell'evidenza strutturata.

Per ciascuna delle 50 finestre si calcola la feature sulle 41 XMEAS e si prende **il massimo di sistema**. Gli score sono adimensionali — ogni variabile è espressa rispetto al proprio comportamento normale — quindi il massimo risponde alla domanda «almeno una variabile si è allontanata dal proprio normale più del previsto?». Non identifica la causa e non rende anomale le altre variabili.

I 50 massimi vengono ordinati e la soglia è il valore al **rango 49**, con attivazione stretta `>`.

*Natura della motivazione del rango 49: scelta di disegno.* Corrisponde a un quantile empirico prossimo al 98° sui massimi Normal disponibili. Gli artefatti **non documentano** una calibrazione mirata a un tasso di falsi allarmi obiettivo, e non ne viene attribuita una a posteriori.

> **Dove si verifica davvero.** La formula, il valore di `alpha` e i limiti della calibrazione stanno in [`code/tep_analysis_v2/threshold_calibration_report.md`](../code/tep_analysis_v2/threshold_calibration_report.md) e in `threshold_calibration.json`, che sono la fonte: questa sezione ne è la narrazione. Il report registra `alpha = 0.05`, la regola `k = ceil((n+1)*(1-alpha)) = 49` e cinque limiti dichiarati — fra cui che le finestre adiacenti non sono indipendenti, che la calibrazione è per-feature e non corregge la simultaneità fra le quattro feature (l'unione produce 3/50, cioè 6,0%, non 5%), e che **la funzione di score non è la stessa in calibrazione e in applicazione**, perché la calibrazione usa una baseline leave-one-block-out su quattro blocchi e le finestre di fault e di test ne usano una su tutti e cinque. Chi deve verificare una soglia apre il report, non questa pagina.

> **Esempio reale — dalle 50 finestre alla soglia di spostamento**
>
> | Rango | Score | Finestra | Esito |
> | ---: | ---: | --- | --- |
> | 47 | 1,2688185320140528 | N3 [135,140) | sotto |
> | 48 | 1,5988379030092623 | N2 [85,90) | sotto |
> | **49** | **1,9695333234149084** | N4 [190,195) | **soglia** |
> | 50 | 2,0050511992352518 | N2 [95,100) | unico `>` soglia |
>
> Ogni score è il massimo sui 41 canali della finestra corrispondente.

Il criterio **leave-one-block-out** nasce qui: quando si misura N1, il riferimento usa N2+N3+N4+N5, e così ciclicamente.

### 3.4 Il congelamento

Prima di aprire validazione, test e held-out vengono congelati feature, soglie, rappresentazione temporale, renderer ed evaluator. È il principio *congela prima di valutare*: nessun dato di valutazione può più influenzare le regole con cui verrà giudicato. Da qui in avanti le regole si applicano soltanto, non si ridefiniscono.

Fino a questo punto sono entrati in gioco esclusivamente i blocchi Normal N1–N5, per calibrare le soglie, e i guasti batch 1–5, usati **solo** in fase di progetto per scegliere quali feature usare — mai per calcolare le soglie. N6–N10 e i guasti batch 6–10 non sono ancora stati toccati.

### 3.5 Dai numeri ai fatti strutturati

Per ogni finestra e per ogni XMEAS si applica la soglia congelata: se il valore la supera si genera un **flag**, e per le feature con segno si conserva il segno.

> **Esempio reale — F1 batch 1, XMEAS-1, finestra W1**
>
> Caso di sviluppo, non test indipendente. W1 è `[10,15)` h: 5 h × 60 = 300 misure.
>
> 1. **Misure grezze** (prime cinque e ultime tre delle 300): `0.266206, 0.264258, 0.265880, 0.268725, 0.267920, …, 1.018145, 1.017490, 1.018571`
> 2. **Media della finestra**: `Σxᵢ = 216.7053282371516` → `x̄_w = 0.7223510941238387`
> 3. **Riferimento N1–N5**, 15 000 misure in `[0,250)` h: `μ₀ = 0.26679593084899306`, `σ₀ = 0.005941491332146645`
> 4. **Sostituzione**: `shift_sigma = (0.7223510941238387 − 0.26679593084899306) / 0.005941491332146645 = 76.67353831016274`
> 5. **Confronto**: `|76.67353831016274| > 1.9695333234149084` → flag attivo, segno positivo conservato.
>
> Provenienza: `mode1_1_1.xlsx`, righe 602–901, XMEAS-1; riferimento da `mode1_normal_500.xlsx`, righe 2–15001.

Lo stesso procedimento si ripete per tutte le otto finestre e tutte le 41 XMEAS. La griglia risultante viene aggregata in una **struttura di fatti** che conserva conteggi, segni, coerenza di segno e collocazione temporale delle attivazioni.

> **Estratto reale della struttura, per XMEAS-1**
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

### 3.6 Il testo neutrale

Il renderer trasforma la struttura in una descrizione a parole. Nel testo prodotto **non compaiono identificativi di guasto, etichette di classe o diagnosi**: solo fatti osservati.

> **Testo neutrale reale — caso EXM-001 (F1 batch 1, identità nota solo all'evaluator)**
>
> Intervallo osservato 10.0–50.0 h in 8 finestre da 5.0 h. XMEAS-1 supera la soglia di spostamento in 8/8 finestre, sempre con segno positivo; il run più lungo con segno coerente comprende 8 finestre, dalla prima attivazione a 10.0 h all'ultima a 45.0 h. XMEAS-1 supera la soglia di pendenza in 6/8 finestre, con segno positivo in 3 e negativo in 3; il run più lungo con segno coerente comprende 1 finestra, dalla prima attivazione a 10.0 h all'ultima a 35.0 h. XMEAS-20: variabilità residua dopo rimozione del trend lineare sopra soglia in 4/8 finestre; 2/2 nella fase iniziale e 0/2 nelle ultime finestre. XMEAS-10: variazioni campione-campione sopra soglia in 1/8 finestre; 1/2 nella fase iniziale e 0/2 nelle ultime finestre. Su XMEAS-10, residual e diff superano simultaneamente le rispettive soglie in 1/8 finestre, incluse 0/2 finestre finali. La massima dispersione complessiva osservata è su XMEAS-1 (rapporto tra deviazioni standard 46.30).

Il testo nasce dalla struttura completa a 41 canali, quindi cita altri canali quando dominano altre sezioni. Ogni frase è riconducibile ai numeri di partenza: è questo che rende la verbalizzazione verificabile.

### 3.7 Il controllo della rappresentazione

Prima di affidare i testi a un modello linguistico, un evaluator offline verifica se la rappresentazione conserva struttura sufficiente. Lavora sulla struttura numerica, non sul testo, e misura stabilità dentro la classe e separabilità fra classi. Una firma contiene 17 componenti normalizzate per XMEAS: 41 × 17 = **697 valori**; la similarità è `1 − mean(abs(a−b))`.

L'evaluator **non produce una predizione e non misura accuratezza**. Verifica la qualità descrittiva della rappresentazione.

> **La distinzione che conta.** Alta similarità dentro la classe e bassa similarità fra classi indicano che il testo neutrale conserva abbastanza struttura da distinguere le condizioni senza mai nominarle. Ma **la separabilità descrittiva non equivale all'accuratezza diagnostica**: una firma separabile non garantisce che un ragionatore la utilizzi correttamente.

### 3.8 Dopo il congelamento: validazione, test, nuove simulazioni

La stessa pipeline runtime viene eseguita prima sulla validazione (guasti batch 6–7, Normal N6–N7) e poi sul test (batch 8–10, N8–N10). Il percorso è sempre `finestre → feature → soglie congelate → struttura → testo neutrale → evaluator`.

I batch 8–10 erano il test di questa fase, e sono stati aperti. Un test osservato non è più vergine per la fase successiva. Servono quindi run nuovi, generati e congelati prima della verbalizzazione e dell'inferenza. Sono **15 nuove realizzazioni simulate**: 3 Normal e 3 run per ciascuno dei quattro guasti. Sono il materiale dello studio principale.

---

## 4 · Produzione e trasferimento degli insight

Da qui entrano in gioco gli agenti e il modello linguistico. La pipeline della sezione precedente non viene ri-progettata: gli agenti la riusano così com'è, applicando riferimento e soglie congelati senza mai ricalibrarli.

### 4.1 Gli agenti e la loro conoscenza locale

Quattro agenti conoscono tutti il funzionamento normale, ma ciascuno un solo guasto.

| Agente 1 | Agente 2 | Agente 3 | Agente 4 |
| --- | --- | --- | --- |
| 2 Normal + 2 esempi di F1 | 2 Normal + 2 esempi di F8 | 2 Normal + 2 esempi di F10 | 2 Normal + 2 esempi di F13 |

Tre cose vanno tenute distinte:

- gli **esempi locali** sono i batch 1–2 del proprio guasto e i blocchi Normal N1–N2, dai dati originali;
- il **caso da diagnosticare** è un run dell'held-out indipendente, e compare solo al momento dell'inferenza;
- le **soglie** restano quelle calibrate su N1–N5, congelate e mai ricalcolate.

Ogni agente costruisce i propri esempi facendo passare i casi che conosce attraverso la pipeline già congelata, e associa a ciascuno la propria pseudolabel. Nessun modello linguistico interviene in questo passaggio. Il risultato sono quattro pacchetti da quattro esempi, ciascuno ridotto alla coppia `(testo neutrale, pseudolabel)`.

### 4.2 Perché le etichette sono opache

*Natura della motivazione: necessità sperimentale.*

Una **pseudolabel** sostituisce il nome reale del guasto con un token opaco `CLS-…`: F1, F8, F10 e F13 non vengono mai mostrati al modello, mentre `Normal` resta `Normal`. La corrispondenza reale è nota soltanto all'evaluator.

Il TEP è un benchmark pubblico e molto citato. Se il modello vedesse i nomi reali, una risposta corretta non distinguerebbe fra l'uso dell'evidenza trasferita e il recupero di conoscenza acquisita in addestramento. La pseudonimizzazione maschera il nome, non la firma descritta nel testo: è una difesa contro la scorciatoia, non contro l'inferenza.

> **Esempio di coppia locale.** Il testo neutrale EXM-001 riportato in §3.6, presentato al modello con l'etichetta `CLS-ZOGAA`. Che si tratti di F1 batch 1 resta informazione lato evaluator.

### 4.3 Come nascono gli insight

Dopo gli esempi, ogni agente compie una seconda operazione, su un ramo distinto: riparte dai **cinque** casi di sviluppo del proprio guasto (batch 1–5), li fa passare per la stessa pipeline congelata e chiede al modello di distillarne le regolarità ricorrenti.

| Passaggio | Che cosa accade |
| --- | --- |
| Ingresso | un bundle per agente con cinque testi neutrali del guasto locale, ricostruiti dai workbook di sviluppo tramite la pipeline congelata; non provengono dal file degli esempi |
| Operazione | il bundle viene passato a `gpt-5.6-terra`, reasoning `medium`, output strutturato strict. Vale la regola *vince il primo output strutturalmente valido*: nessuna selezione o rigenerazione basata sul contenuto |
| Uscita | 2 insight per agente, **8 in totale** |

Nell'esecuzione congelata ogni agente ha richiesto un solo tentativo e zero ripetizioni. Nessuna soglia viene ricalibrata.

Tutto questo avviene **prima** di aprire diagnosticamente i 15 run indipendenti, già generati e congelati: gli insight nascono soltanto da ciò che l'agente conosceva già.

> **Esempio reale — un insight di Agente 1**
>
> ```
> INS-001 · agent_1 · CLS-ZOGAA
> "XMEAS-1 exceeds the displacement threshold positively in all 8/8 windows,
>  with one coherent 8-window run from 10.0 to 45.0 h; it also has the largest
>  overall dispersion (standard-deviation ratio 46.06–46.50)."
> ```
>
> L'intervallo 46,06–46,50 deriva da cinque run, non da uno: l'insight distilla più casi.

### 4.4 Come circolano

La federazione è **fra pari e senza server**: ogni agente riceve i sei insight prodotti dagli altri tre, **mai i propri**. La libreria globale ne contiene otto; ciascuna libreria ricevuta ne contiene sei.

Dei sei insight che un agente riceve, due descrivono il guasto che si troverà davanti in un dato caso e quattro agiscono da distrattori. La conoscenza circola come testo: non vengono scambiati dati grezzi né parametri del modello.

---

## 5 · Le quattro condizioni: A, A+, B, E

Una **condizione** è una versione controllata dello stesso caso. Il testo neutrale del caso e gli esempi locali restano identici; cambia una sola cosa: il blocco degli insight inserito nel prompt. Così la differenza fra condizioni non può essere attribuita a un caso diverso o a esempi diversi.

Prima in parole comuni, poi con le sigle che verranno usate nelle tabelle.

| In parole | Sigla | Che cosa riceve l'agente oltre ai propri esempi | A quale domanda risponde |
| --- | --- | --- | --- |
| **Da solo** | **A** | nessun insight, né dei pari né propri | qual è il punto di partenza informativo per una classe che l'agente non conosce? |
| **Da solo, con le proprie descrizioni** | **A+** | i due insight che ha prodotto sulla propria classe locale | il vantaggio potrebbe venire dal semplice possesso di insight, anche propri? |
| **Con le descrizioni degli altri** | **B** | i sei insight dei pari, con le associazioni corrette | che cosa aggiunge la conoscenza degli altri agenti? |
| **Con le descrizioni associate alle etichette sbagliate** | **E** | gli stessi sei insight di B: stessi identificativi, fonti, testi, ordine e volume; cambiano solo le pseudolabel, permutate | il beneficio dipende dall'associazione corretta o dalla sola presenza di più testo? |

### 5.1 Perché E è la condizione decisiva

La permutazione è uno **scompaginamento senza punti fissi**, specifico per agente: nessuna pseudolabel resta associata alla classe originale. Per l'agente 3, per esempio, `CLS-ZOGAA` diventa `CLS-OJNSG`.

E ha quindi lo stesso volume, la stessa forma e lo stesso costo in token di B. Se bastasse avere più testo nel prompt, E funzionerebbe quanto B. Il contrasto B−E isola la correttezza dell'informazione dal volume del testo.

### 5.2 Perché A+ è una condizione e non un dettaglio

A è un punto di partenza in cui l'agente non possiede alcuna informazione sulla classe remota. Si potrebbe obiettare che il salto da A a B derivi semplicemente dall'aggiungere un blocco di insight al prompt, indipendentemente da chi li ha scritti.

A+ risponde a questa obiezione specifica: l'agente riceve **i propri** insight, prodotti sulla propria classe locale, nella stessa posizione del prompt in cui B mette quelli dei pari. Struttura identica, sorgente diversa. È un controllo aggiuntivo, non un esperimento separato, ed è per questo che i suoi risultati compaiono insieme a quelli dello studio principale in §7.

### 5.3 Lo spazio delle risposte è chiuso

L'agente sceglie fra le pseudolabel presenti nel prompt più `Normal`. Il protocollo prevede l'**astensione**: se le ripetizioni non producono una maggioranza valida, la decisione aggregata è un'astensione, che nel conteggio vale come errore.

Questo va detto qui perché è una proprietà del disegno, non un limite emerso a posteriori: il sistema opera in un catalogo chiuso di risposte. §12 ne trae le conseguenze.

---

## 6 · Protocollo di valutazione

Questa sezione contiene, **una volta sola**, le regole di conteggio e di inferenza che valgono per tutte le sezioni successive.

### 6.1 L'unità statistica

L'endpoint primario riguarda esclusivamente i **guasti mai visti dall'agente che giudica**. Ogni run di guasto viene valutato dai quattro agenti; per l'endpoint primario si esclude l'agente che possiede localmente quel guasto. Restano tre agenti riceventi per run.

Le tre osservazioni sullo stesso run **sono correlate**: provengono dallo stesso run simulato, con lo stesso rumore e gli stessi transitori. **Il run simulato è trattato come unità sperimentale indipendente**, non la coppia agente–run e non la singola chiamata al modello. È la ragione per cui gli intervalli si calcolano su 12 o 24 cluster, non su 36 o 72 righe.

| | Studio principale | Replica su nuovi run |
| --- | ---: | ---: |
| Run simulati di guasto, indipendenti | 12 | 24 |
| Coppie su guasto mai visto, per condizione | 36 | 72 |
| Run Normal | 3 | 6 |

### 6.2 Ripetizioni e aggregazione

Ogni combinazione caso–agente–condizione viene eseguita **R = 3** volte con lo stesso input. Una pseudolabel che riceve almeno due voti diventa la predizione aggregata; senza maggioranza valida l'agente si astiene.

*Natura della motivazione: scelta tecnica.* Le ripetizioni servono a stabilizzare il non-determinismo del modello. **Non sono tre run indipendenti.** Va aggiunto un limite: nella verifica con l'altro modello, eseguita a temperatura 0 e seed fisso, le tre ripetizioni risultano identiche byte per byte, quindi lì R = 3 è degenere e non misura alcuna variabilità.

### 6.3 Astensione

**L'astensione conta come errore** in tutte le condizioni e in tutte le popolazioni. È la convenzione più severa fra quelle possibili e vale per l'intero documento.

### 6.4 Congelamento e valutazione

Tutte le predizioni vengono congelate **prima** di essere unite alla risposta corretta. La corrispondenza fra pseudolabel e guasto reale è nota solo all'evaluator e viene applicata offline.

Configurazione, prompt, schedule e criteri di successo sono stati **definiti e congelati prima della propria valutazione**, con manifest e hash verificabili. Non si tratta di una preregistrazione: non esiste alcuna registrazione presso un ente esterno.

### 6.5 Incertezza

Gli intervalli derivano da un **bootstrap appaiato per cluster** sui run simulati, stratificato per pseudolabel, con 10 000 ricampionamenti e seed congelato. Le tre osservazioni dei riceventi associate allo stesso run vengono mantenute insieme.

Con 12 o 24 cluster indipendenti, gli intervalli vanno interpretati nel contesto di questo studio controllato e non come una caratterizzazione generale dell'incertezza del metodo.

### 6.6 Popolazioni secondarie

Guasti già noti localmente, casi Normal e risultato complessivo sono **secondari e descrittivi**. Non introducono criteri inferenziali e non modificano l'endpoint primario. Servono a verificare che l'aggiunta della conoscenza dei pari non degradi ciò che l'agente già riconosceva.

### 6.7 Criteri di supporto pre-specificati

Per lo studio principale, il protocollo congelato indicava quattro criteri: `B−A > 0`; effetto positivo in almeno 3 agenti su 4; casi migliorati maggiori dei casi peggiorati; `B−A > E−A`, numericamente equivalente a `B−E > 0`.

Per la replica, il criterio è più stringente e riguarda solo il contrasto primario: la differenza osservata deve essere positiva **e** il limite inferiore del suo intervallo al 95% deve essere positivo. Entrambe le condizioni devono valere congiuntamente. Per B−E l'intervallo viene riportato a fini descrittivi e non costituisce un ulteriore criterio decisionale.

---

## 7 · Studio principale

*Categoria: studio principale, con un controllo aggiuntivo (A+).*
*Identificativo tecnico: Experiment 1 · Phase B.*

### 7.1 Il disegno

15 casi held-out, congelati prima di qualsiasi inferenza: 12 run di guasto (tre per classe) e 3 run Normal. Ogni caso viene sottoposto ai quattro agenti in ciascuna condizione, con R = 3.

Per le condizioni A, B ed E: 15 casi × 4 agenti × 3 condizioni × 3 ripetizioni = **540 chiamate**, che diventano 180 esiti aggregati. Il controllo A+ aggiunge 15 × 4 × 3 = 180 chiamate e 60 esiti aggregati.

La popolazione primaria è costituita dalle 36 coppie su guasto mai visto, derivate da 12 run simulati indipendenti.

### 7.2 Come si presenta un singolo caso

Un esempio rende concreta l'unica manipolazione in gioco. Il caso PBH-004 è un nuovo run di F1, identità nota solo all'evaluator. La pipeline congelata lo trasforma nel suo testo neutrale, che segnala XMEAS-1 sopra la soglia di spostamento in 8/8 finestre, sempre positivo, con dispersione massima 47,00: la firma di F1, osservata però su un run mai visto. Il testo viene presentato all'agente 3, che possiede esempi locali di F10 e per cui F1 è quindi una classe mai vista.

| Condizione | Blocco insight | Le tre ripetizioni | Esito aggregato |
| --- | --- | --- | --- |
| A | nessuno | `null ×3` | astensione, conta come errore |
| B | sei insight autentici; INS-001 associa quella firma a `CLS-ZOGAA` | `CLS-ZOGAA ×3` | corretta |
| E | stessi testi e stesso ordine; INS-001 associa quella firma a `CLS-OJNSG` | `CLS-OJNSG ×3` | errata |

Il caso, gli esempi locali, il modello e il prompt sono identici nelle tre righe. Cambia soltanto il blocco degli insight. I record hanno `used_insight_ids=[]`: non viene attribuita la singola risposta a uno specifico insight; si confrontano le condizioni nel loro insieme.

### 7.3 Il risultato primario

**Guasti mai visti dall'agente che giudica — 36 coppie per condizione, da 12 run simulati**

| Condizione | Corrette | Accuratezza | Astensioni | Errori con decisione |
| --- | ---: | ---: | ---: | ---: |
| **A** — da solo | **0 / 36** | 0,0 % | 14 | 22 |
| **A+** — da solo, con le proprie descrizioni | **0 / 36** | 0,0 % | 21 | 15 |
| **B** — con le descrizioni degli altri | **31 / 36** | 86,1 % | 0 | 5 |
| **E** — con le associazioni corrotte | **3 / 36** | 8,3 % | 0 | 33 |

Tre letture, in ordine di importanza.

**Lo zero di A non deriva solo dalle astensioni.** L'agente si astiene in 14 casi su 36 e produce una decisione in 22, e **nessuna** delle 22 decisioni è corretta. Anche quando sceglie, sbaglia.

**I propri insight non aggiungono nulla.** A+ è 0/36 come A, con delta esattamente **0** e intervallo al 95% `[0, 0]`. L'agente conosce già la propria classe locale; reinserire quella conoscenza nel prompt non gli permette di diagnosticare guasti mai osservati. Il salto non è quindi spiegabile con la semplice presenza di un blocco di insight nel prompt.

**Lo stesso testo, associato male, fa crollare il risultato.** E contiene esattamente gli stessi sei insight di B — stessi identificativi, fonti, testi, ordine e volume — e scende a 3/36.

### 7.4 I contrasti

| Contrasto | Stima | Intervallo 95% | Ruolo |
| --- | ---: | --- | --- |
| **B − A** | **+0,8611** | [0,8333 – 0,9167] | contrasto primario pre-specificato |
| **B − E** | **+0,7778** | [0,7222 – 0,8333] | contrasto sulla pertinenza dell'informazione |
| **A+ − A** | 0,0000 | [0 – 0] | controllo local-only |
| **B − A+** | +0,8611 | [0,833 – 0,917] | trasferimento rispetto al controllo |
| **E − A+** | +0,0833 | [0,028 – 0,139] | — |

I quattro criteri di supporto pre-specificati risultano soddisfatti 4/4.

Confronti appaiati sulle 36 coppie: B migliora 31 casi rispetto ad A e ad A+, non ne peggiora nessuno; E migliora 3 casi e non ne peggiora nessuno; A+ non cambia alcun caso rispetto ad A.

La magnitudine di B−A va letta tenendo presente che A è un **punto di partenza informativo**: l'agente ricevente non possiede alcun esempio locale della classe corrispondente. Il valore +0,8611 non è una misura generale delle prestazioni del metodo in altri problemi, modelli o domini.

### 7.5 Casi già noti e casi normali

*Categoria: analisi descrittiva su popolazioni secondarie.*

| Popolazione | A | A+ | B | E |
| --- | ---: | ---: | ---: | ---: |
| Guasti già noti localmente | 12/12 | 12/12 | 12/12 | 12/12 |
| Normal | 12/12 | 12/12 | 12/12 | 12/12 |

Nel campione osservato non si rileva alcuna degradazione delle prestazioni su condizioni già conosciute quando vengono aggiunti gli insight dei pari. Questo non dimostra che il metodo sia immune da interferenze in generale, e §8 mostra che su un campione più grande il quadro cambia.

### 7.6 Dove si concentrano gli errori

*Categoria: analisi descrittiva dei record già congelati. Non introduce nuovi endpoint.*

Per ciascun guasto ci sono tre run simulati, ciascuno valutato dai tre agenti che non lo conoscono: nove coppie per guasto.

| Guasto | Coppie corrette in B |
| --- | ---: |
| F1 | 9 / 9 |
| F8 | **4 / 9** |
| F10 | 9 / 9 |
| F13 | 9 / 9 |

Tutti e cinque gli errori di B si concentrano sui tre run di F8. Dentro quei run compare eterogeneità fra riceventi: l'agente che conosce F1 riconosce F8 in 3 run su 3, quello che conosce F10 in 0 su 3, quello che conosce F13 in 1 su 3.

Per agente, sulle nove coppie ciascuno: agente 1 e agente 2 al 100%, agente 3 al 66,7%, agente 4 al 77,8%.

Queste decomposizioni mostrano **dove** si concentra la difficoltà osservata, non **perché**. F8 non diventa un endpoint.

### 7.7 Stabilità delle decisioni

*Categoria: analisi descrittiva.*

Delle 36 decisioni di B sui guasti mai visti, **33 sono unanime** fra le tre ripetizioni e 3 sono divise. In A+, su 60 esiti aggregati, 57 sono unanimi e 3 a maggioranza 2 su 3.

È un descrittore dell'accordo fra tre chiamate con lo stesso input e la stessa configurazione. Non è una misura di robustezza rispetto a perturbazioni dei dati, prompt diversi, altri modelli o distribuzioni differenti.

### 7.8 Costo in token del controllo A+

333 192 token in ingresso, 29 695 in uscita, 362 887 in totale; zero ripetizioni strutturali e zero errori di parsing.

---

## 8 · Replica su nuovi run

*Categoria: replica su nuovi dati.*
*Identificativo tecnico: EXP3_V2 · Experiment 3.*

### 8.1 Perché serve

Un held-out, per definizione, si apre una volta sola: dopo che i risultati sono stati osservati, quei dati non sono più vergini rispetto all'ipotesi.

Il rischio specifico da escludere non è la contaminazione classica — il congelamento la controlla già — ma che le dodici realizzazioni simulate dello studio principale avessero caratteristiche idiosincratiche (pattern di rumore, transitori, derive) che hanno favorito il trasferimento in quel campione particolare.

Le nuove realizzazioni simulate sono run indipendenti delle **stesse quattro classi**: non nuove esecuzioni degli stessi file, non classi nuove, non un dominio diverso. Metodo, agenti, soglie, insight e protocollo restano quelli dello studio principale, riapplicati senza ricalibrazione. L'obiettivo non è la generalizzazione, ma verificare se l'effetto sia riproducibile quando cambiano i segnali simulati e resta fisso tutto il resto.

### 8.2 Il disegno

30 nuove realizzazioni simulate: 6 Normal e 6 run per ciascuno dei quattro guasti, il doppio dello studio principale. Congelate prima di qualsiasi inferenza.

24 run di guasto × 3 agenti riceventi = **72 coppie per condizione**, da 24 run simulati indipendenti. Ipotesi primaria, popolazione, contrasti e criteri sono stati scritti prima di aprire i dati.

Il controllo A+ **non compare in questa replica**: è stato eseguito soltanto sui casi dello studio principale.

### 8.3 Il risultato primario

**Guasti mai visti dall'agente che giudica — 72 coppie per condizione, da 24 run simulati**

| Condizione | Corrette | Accuratezza | Astensioni | Errori con decisione |
| --- | ---: | ---: | ---: | ---: |
| **A** — da solo | **0 / 72** | 0,0 % | 30 | 42 |
| **B** — con le descrizioni degli altri | **68 / 72** | 94,4 % | 0 | 4 |
| **E** — con le associazioni corrotte | **4 / 72** | 5,6 % | 0 | 68 |

Anche qui lo zero di A non deriva solo dalle astensioni: 42 decisioni prese, nessuna corretta.

| Contrasto | Stima | Intervallo 95% | Ruolo |
| --- | ---: | --- | --- |
| **B − A** | **+0,9444** | [0,8611 – 1,0] | contrasto primario |
| **B − E** | **+0,8889** | [0,7778 – 0,9861] | evidenza di supporto |

**Il criterio di replica pre-specificato è soddisfatto**: la differenza osservata è positiva e il limite inferiore dell'intervallo, 0,8611, è positivo.

Con 24 cluster indipendenti, il doppio dello studio principale, gli intervalli sono più stretti, ma restano quelli di uno studio controllato di piccola scala.

### 8.4 Dove si concentrano gli errori

*Categoria: analisi descrittiva.*

Per ciascun guasto ci sono sei run simulati e tre agenti riceventi: 18 coppie per guasto.

| Guasto | Coppie corrette in B |
| --- | ---: |
| F1 | 18 / 18 |
| F8 | 16 / 18 |
| F10 | 18 / 18 |
| F13 | 16 / 18 |

I quattro errori si concentrano su due run specifici, sui quali sbagliano contemporaneamente l'agente che conosce F1 e quello che conosce F10. Gli agenti che conoscono F8 e F13 non commettono errori su guasti mai visti.

### 8.5 Il fenomeno nuovo: degradazione sui guasti già noti

*Categoria: risultato descrittivo su popolazione secondaria.*

| Popolazione | A | B | E |
| --- | ---: | ---: | ---: |
| Guasti già noti localmente | 24/24 (100 %) | **19/24 (79,2 %)** | 22/24 (91,7 %) |
| Normal | 24/24 | 24/24 | 24/24 |
| Complessivo | 48/120 (40,0 %) | 111/120 (92,5 %) | 50/120 (41,7 %) |

Nello studio principale i guasti già noti erano 12/12 in tutte le condizioni: nessuna degradazione. Qui A resta a 24/24 ma **B scende a 19/24**: cinque casi che l'agente riconosceva diventano errori quando vengono aggiunti gli insight dei pari. Quattro riguardano l'agente che conosce F13, uno l'agente che conosce F8; la confusione è fra queste due classi. Anche E mostra una degradazione più lieve.

È un segnale che gli insight dei pari, in alcune combinazioni run–agente, possono interferire con il riconoscimento di guasti già noti. Il fenomeno non era osservabile con soli 12 casi. Non essendo un endpoint primario non altera la decisione sulla replica, ma va registrato — e §10 descrive l'intervento che ne è seguito.

Lo stesso fenomeno ricompare, in un contesto diverso, nella verifica con l'altro modello linguistico: là i guasti già noti scendono a 9/12 sui dati **dello studio principale**, dove con il modello originale erano 12/12. Non è quindi legato a un singolo campione.

### 8.6 Confronto sintetico fra le due evidenze

| | Studio principale | Replica su nuovi run |
| --- | --- | --- |
| Run simulati di guasto | 12 | 24 |
| Guasti mai visti — A / B / E | 0/36 · 31/36 · 3/36 | 0/72 · 68/72 · 4/72 |
| B − A | +0,861 [0,833 – 0,917] | +0,944 [0,861 – 1,0] |
| B − E | +0,778 [0,722 – 0,833] | +0,889 [0,778 – 0,986] |
| Guasti già noti in B | 12/12 | 19/24 |

Il disegno riproduce **le stesse classi di guasto su nuove realizzazioni simulate**; non generalizza a guasti non studiati. La replica non comprende un proprio riferimento centralizzato.

---

## 9 · Confronti esterni e riferimenti

Questa sezione risponde a una domanda diversa da quella dello studio principale: **come si colloca il trasferimento testuale rispetto a chi usa direttamente i numeri, o rispetto a chi vede tutto?**

I quattro elementi che seguono hanno ruoli epistemici diversi, ed è essenziale non confonderli.

### 9.1 Baseline numerica condivisa — confronto diretto

*Categoria: confronto esterno. Rispetta lo stesso problema informativo del metodo testuale.*

Quattro agenti, ciascuno con il funzionamento normale più un solo guasto locale, pseudolabel opache, stessi dati di sviluppo e stessi 15 casi held-out. La risposta corretta viene collegata alle predizioni solo nella valutazione offline. Il protocollo è stato congelato e hashato prima dell'esecuzione.

Ogni caso diventa il vettore numerico a **697 componenti** (41 XMEAS × 17) derivato dall'evidenza strutturata **prima** del testo. Per ogni classe si calcola la media dei cinque casi di sviluppo; la classificazione sceglie il prototipo a distanza assoluta media minima. Nessuna normalizzazione viene appresa sul test. Un pareggio entro `1e-12` produce astensione.

Il metodo è ispirato a FedProto ma **non è FedProto**: non addestra una rete di rappresentazione e non implementa l'ottimizzazione dell'algoritmo originale.

| Braccio | Libreria disponibile a ciascun agente | Complessivo | Guasti già noti | Guasti mai visti | Normal |
| --- | --- | ---: | ---: | ---: | ---: |
| **Prototipi condivisi** | Normal + guasto locale + 3 guasti dei pari | **60/60 (100 %)** | 12/12 | **36/36 (100 %)** | 12/12 |
| **Local-only numerica** | Normal + solo guasto locale | 24/60 (40 %) | 12/12 | **0/36 (0 %)** | 12/12 |
| **Centralizzata numerica** | tutti e cinque i centroidi di sviluppo | 60/60 (100 %) | 12/12 | 36/36 (100 %) | 12/12 |

L'intervallo bootstrap al 95% della metrica primaria è `[100 %, 100 %]`, ma non indica certezza generale: ricampiona soltanto i 12 run simulati disponibili.

#### Il confronto, senza attenuazioni

| Metodo | Guasti mai visti | Differenza rispetto ai prototipi condivisi |
| --- | ---: | ---: |
| **Prototipi condivisi** | **36 / 36** | — |
| FoT A | 0 / 36 | +36 casi |
| **FoT B** | **31 / 36** | **+5 casi** |
| FoT E | 3 / 36 | +33 casi |

**Sul campione confrontato la baseline numerica è più accurata di FoT B.** Questi dati **non supportano un claim di superiorità diagnostica del trasferimento testuale.** Mostrano due cose più circoscritte:

1. condividere conoscenza di classe è indispensabile in questo compito — lo stesso metodo numerico, senza ricevere nulla dagli altri, scende a 0/36;
2. una media numerica compatta delle firme è sufficiente a separare tutti i casi osservati.

A resta un punto di partenza informativo ed E un controllo di associazione semantica: non sono competitori numerici.

Nel braccio condiviso ogni cella per agente e per classe è `3/3`; la matrice di confusione aggregata è interamente diagonale, con zero astensioni.

**Payload del confronto.** Ogni agente riceve 3 prototipi, cioè 2 091 scalari: 16 755 byte per agente e 67 020 byte complessivi per le 12 consegne, contando 9 byte di pseudolabel più 697 float64 per prototipo. Il prototipo Normal non viene trasmesso perché ogni agente possiede già lo stesso riferimento.

**Che cosa non è stato eseguito, e perché.** PCA+SVM centralizzata non è stata eseguita perché esporre tutte le classi al training trasformerebbe il problema in una classificazione supervisionata ordinaria. FedAvg non è stato eseguito perché richiederebbe un nuovo modello e un protocollo di uscita disgiunto per classe: la semplice media di modelli locali non rende disponibile una classe mai presente nell'uscita locale. Produrre quei numeri avrebbe cambiato il compito. Resta il fatto, registrato in §12, che **manca un algoritmo di federated learning pubblicato eseguito sullo stesso compito**.

### 9.2 Riferimenti ML centralizzati — riferimenti descrittivi

*Categoria: riferimento descrittivo. Non federato, non confrontabile alla pari.*

Una suite congelata prima del training, con otto modelli: AdaBoost, Random Forest, MLP, lineare elastic-net, k-NN, LSTM causale con attention, BiLSTM con attention e BiLSTM multimodale con attention. La variante multimodale fonde la sequenza numerica con il testo neutrale vettorizzato TF-IDF. XGBoost non era disponibile nell'ambiente, quindi è stata usata l'alternativa esplicitamente ammessa, AdaBoost — *limite pratico, dichiarato come tale*.

| Modello centralizzato | 15 run simulati | 12 casi di guasto | Guasti mai visti, proiettato |
| --- | ---: | ---: | ---: |
| AdaBoost | 15/15 (100 %) | 12/12 | 36/36 |
| Random Forest | 15/15 (100 %) | 12/12 | 36/36 |
| MLP | 15/15 (100 %) | 12/12 | 36/36 |
| Lineare elastic-net | 15/15 (100 %) | 12/12 | 36/36 |
| k-NN | 15/15 (100 %) | 12/12 | 36/36 |
| LSTM causale + attention | 15/15 (100 %) | 12/12 | 36/36 |
| BiLSTM + attention | 14/15 (93,3 %) | 11/12 | 33/36 |
| BiLSTM multimodale + attention | 14/15 (93,3 %) | 11/12 | 33/36 |

Tre avvertenze, tutte necessarie perché la tabella non venga letta male.

**Questi otto modelli vedono tutte e cinque le classi durante il training centralizzato.** Non sono federati e non affrontano il problema disgiunto per classe. Il valore «proiettato» replica la stessa predizione centrale sui tre agenti per cui il guasto è localmente mai visto: non trasforma il metodo in federato e non crea 36 osservazioni indipendenti.

**Ogni modello raggiunge il 100% sui 25 casi di training.** Questo, insieme ai soli cinque casi di sviluppo e tre di test per classe, impone prudenza: il risultato può riflettere un benchmark facilmente separabile e non prova generalizzazione ampia.

**Due precisazioni terminologiche.** Una BiLSTM non è causale: usa anche i passi successivi nell'intervallo osservato. La variante multimodale usa due rappresentazioni degli stessi sensori, non una seconda sorgente fisica.

Il confronto diretto e alla pari resta quello con i prototipi condivisi.

### 9.3 Riferimento testuale centralizzato — analisi esplorativa

*Categoria: analisi esplorativa. Introdotta dopo aver osservato i risultati A/B/E. Non è un confronto causale.*

La domanda: quanto perde un sistema a quattro agenti rispetto a uno solo che riceve tutto ciò che nella federazione verrebbe scambiato? È stato costruito un agente unico con l'unione degli artefatti destinati al prompt: esempi etichettati e insight testuali. Non dati grezzi, non testi sorgente, non la risposta corretta, non informazione lato evaluator.

| | Esempi etichettati | Insight | Forma del contesto |
| --- | --- | --- | --- |
| **Riferimento centralizzato** | 10 aggregati: 2 per ciascuna delle 4 classi + 2 Normal | 8, inclusi quelli che in B sarebbero propri | contesto unico, indipendente dal ricevente |
| **B** | 4 locali per ricevente: 2 del guasto noto + 2 Normal | 6 dei pari | contesto diverso per ciascun ricevente |

I 10 esempi derivano meccanicamente dall'unione dei quattro pacchetti, con deduplicazione dei Normal.

**Risultati.** 15 casi, R = 3, 45 record e 15 decisioni aggregate: **15/15 (100 %)**, con 12/12 sui casi di guasto e 3/3 sui Normal, zero astensioni. Per ciascun caso le tre ripetizioni hanno prodotto la stessa decisione.

**Distanza descrittiva da B.** Per ciascuno dei 12 casi di guasto si confronta la decisione centralizzata con la media delle decisioni dei tre riceventi per cui quel guasto è mai visto. Il delta appaiato è **+0,1389** con intervallo `[0,0833 – 0,1667]`, 10 000 ricampionamenti.

L'intero vantaggio è concentrato nei tre casi di F8, dove i riceventi ottengono 1/3, 2/3 e 1/3; sugli altri nove casi il delta è zero. Il bootstrap è stratificato su 4 classi × 3 cluster e la sua distribuzione occupa una griglia discreta di soli cinque valori: l'intervallo è corretto ma ha risoluzione minima.

**Il riferimento non è isomorfo a B**: cambiano contemporaneamente quantità, forma e struttura del contesto. Il risultato è descrittivo e temporalmente confondibile; non autorizza una lettura causale né una conclusione generale sulla centralizzazione. Non è stato eseguito sulle realizzazioni della replica.

---

## 10 · Verifiche di robustezza

Nessuna delle verifiche di questa sezione è evidenza primaria. Ciascuna porta la propria qualificazione.

### 10.1 Verifica con un altro LLM

*Categoria: confronto esterno, limitato al lato consumatore.*
*Identificativo tecnico: Experiment 2 · lane Qwen.*

La distinzione essenziale è fra **produttore** e **consumatore**:

- il **produttore** degli insight resta `gpt-5.6-terra` e non viene variato: gli insight sono quelli congelati dello studio principale, byte per byte;
- il **consumatore**, cioè il modello che riceve il caso e gli insight e produce la diagnosi, cambia.

Il consumatore è **Qwen3.8-27B-FP8**, un modello a pesi aperti servito localmente tramite vLLM su GPU locale, senza chiamate a servizi cloud. Tutto il resto è identico: held-out, insight, template di prompt, schedule, scompaginamento di E, aggregazione 2 su 3, evaluator.

| Condizione | Corrette | Accuratezza |
| --- | ---: | ---: |
| A — da solo | 0 / 36 | 0 % |
| B — con le descrizioni degli altri | **34 / 36** | 94,44 % |
| E — con le associazioni corrotte | 1 / 36 | 2,78 % |

B − A = +0,944 `[0,917 – 1,0]`; B − E = +0,917 `[0,833 – 1,0]`. 34 casi migliorati, 0 peggiorati, 2 invariati ed errati. Zero astensioni. I quattro criteri primari risultano soddisfatti.

Popolazioni secondarie: Normal 12/12, complessivo 55/60 (91,67 %), e **guasti già noti 9/12 (75 %)**, contro 12/12 ottenuti dal modello originale sugli stessi casi. È lo stesso fenomeno di interferenza osservato nella replica, in un contesto diverso.

**Che cosa la verifica stabilisce.** Il vantaggio della condizione federata persiste su un secondo consumatore nella configurazione esaminata. **Che cosa non stabilisce.** Un solo consumatore non dimostra generalità; gli insight sono ancora prodotti da un unico modello proprietario, quindi non è una replica interamente a pesi aperti; il confronto fra modelli è descrittivo; con temperatura 0 e seed fisso le tre ripetizioni sono identiche byte per byte, quindi qui R = 3 non misura variabilità.

Il protocollo è stato sottoposto a sonda di capacità e audit indipendente prima del congelamento. La sonda iniziale aveva rivelato un troncamento del ragionamento nella condizione E con un budget di 512 token, corretto portando `max_tokens` a 1536 e introducendo un budget di ragionamento di 1024. Il verdetto della review scientifica indipendente è **GO WITH LIMITATIONS**.

### 10.2 Sensibilità al budget di ragionamento

*Categoria: analisi di sensibilità. Riguarda esclusivamente la verifica con l'altro modello, non lo studio principale.*

Nella configurazione congelata il limite effettivo del ragionamento è **1 023 token** su un budget nominale di 1 024. Tutti e cinque gli errori aggregati di B avevano le tre ripetizioni al limite; tutti i 36 aggregati non limitati erano corretti. Questa coincidenza rendeva ambiguo il fallimento: un errore poteva dipendere dagli insight, ma anche da un ragionamento interrotto troppo presto.

È stata quindi eseguita un'analisi appaiata e deterministica sulle 60 osservazioni uniche della condizione B, con R = 1 — le triplette congelate erano identiche byte per byte, quindi la ripetizione non aggiungeva informazione. L'ancora a 1 024 riproduce 60/60 predizioni congelate e i controlli di integrità sono superati.

| Budget | Accuratezza B | Guasti già noti | Guasti mai visti | Al limite | Nuove regressioni |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 024 | 91,67 % | 75,00 % | 94,44 % | 24/60 | 0 |
| 1 536 | 93,33 % | 75,00 % | 97,22 % | 15/60 | 0 |
| 2 048 | 95,00 % | 83,33 % | 97,22 % | 10/60 | 0 |
| 3 072 | 95,00 % | 83,33 % | 97,22 % | 5/60 | 0 |

L'aumento del budget porta B da 55/60 a 57/60 e riduce i casi al limite dal 40,0 % all'8,3 %, senza regressioni fra i 55 casi già corretti. Il guadagno si arresta dopo 2 048: più spazio di ragionamento corregge alcuni errori, non tutti.

#### Approfondimento sui casi al limite

*Categoria: verifica diagnostica. Riguarda casi selezionati dopo l'analisi e non stima la prestazione complessiva.*

I cinque casi ancora al limite a 3 072 sono stati rieseguiti a 4 096. Due terminano sotto il limite, tre lo raggiungono ancora, e tutti e cinque risultano corretti. Fra i due errori presenti a 3 072, uno viene corretto pur restando al limite, l'altro resta errato pur terminando sotto il limite. Nessuna regressione, nessun errore di parsing.

La lettura causale deve restare prudente. Un caso corretto e sotto il limite è compatibile con la troncatura del ragionamento; due casi ancora errati ma sotto il limite rendono più plausibile un'interferenza, senza dimostrarla; due correzioni ottenute pur restando al limite mostrano che il budget influenza la decisione ma lasciano inconcluso il meccanismo. In breve: **raggiungere il limite non implica sbagliare**, e terminare sotto il limite non identifica da solo la causa dell'errore.

### 10.3 Variante local-first

*Categoria: verifica diagnostica.*
*Identificativo tecnico: `B_LOCAL_FIRST_V1`.*

La replica aveva mostrato che nella condizione B i guasti già noti scendevano da 24/24 a 19/24: in cinque casi l'agente ignorava o sottopesava una firma che conosceva già, soprattutto nella confusione fra F8 e F13.

La variante modifica **una sola parte** del prompt di B: un breve blocco di politica decisionale ordina all'agente di dare precedenza all'evidenza locale quando questa è forte e coerente, usando gli insight dei pari come supporto e non come sostituto. Dopo uno screening su 24 casi, la variante congelata è stata eseguita sull'intera replica: 120 coppie aggregate, ciascuna da tre ripetizioni valide.

| Criterio del test completo | B originale | Variante local-first | Soglia | Esito |
| --- | ---: | ---: | ---: | --- |
| Guasti già noti | 19/24 (79,2 %) | **23/24 (95,8 %)** | ≥ 23/24 | superato |
| Guasti mai visti | 68/72 (94,4 %) | **68/72 (94,4 %)** | ≥ 67/72 | superato |
| Normal | 24/24 (100 %) | **24/24 (100 %)** | = 24/24 | superato |
| Errori di parsing | 0 | **0** | = 0 | superato |
| Complessivo | 111/120 (92,5 %) | **115/120 (95,8 %)** | — | +4 netti |

Le soglie erano state fissate e congelate prima dell'esecuzione del test completo.

Il confronto appaiato contiene **5 miglioramenti e 1 regressione**, tutti nella confusione fra F8 e F13. Si osservano inoltre 112/120 decisioni unanimi e una sola astensione aggregata. La politica mantiene invariata l'accuratezza aggregata sui guasti mai visti, ma **non elimina ogni regressione a livello di singolo caso**.

Il limite di interpretazione è in §12.

### 10.4 Confronto delle rappresentazioni

*Categoria: analisi esplorativa.*
*Identificativo tecnico: ablation TS→testo.*

La domanda è diversa da quelle precedenti: **perché tradurre i numeri in testo proprio così, e non in un altro modo?**

Quattro modi di rendere gli stessi dati, forniti allo stesso modello, sugli stessi casi, nelle stesse condizioni:

| Braccio | Che cos'è | Ispirazione |
| --- | --- | --- |
| **Verbalizzazione V2** | il verbalizzatore usato in questo lavoro: otto finestre × cinque feature per variabile, in linguaggio naturale con soglie e trend | metodo di questo lavoro |
| **RAW_FEATURES** | serializzazione numerica diretta delle stesse feature, in tabella | LLMTime (Gruver et al., 2023) |
| **CGTIME_STATS** | 169 statistiche per sensore, tre famiglie, allineate alle finestre | CGTime (Feng et al., 2026) |
| **SAX_SYMBOLIC** | codifica simbolica in lettere, alfabeto 5, parola 10 | SAX / HAR-LLM (Pappa et al., 2026) |

Il compito è una classificazione centralizzata a cinque classi su 15 casi held-out, 3 ripetizioni per caso: 4 bracci × 15 casi × 3 ripetizioni = 180 inferenze. *Natura della scelta: necessità sperimentale.* Centralizzare isola la variabile «rappresentazione» evitando confondimento con l'architettura federata; validare nel contesto federato resta un lavoro successivo.

| Braccio | Accuratezza | Intervallo 95% | MCC |
| --- | ---: | --- | ---: |
| RAW_FEATURES | 0,933 | [0,800 – 1,000] | 0,923 |
| CGTIME_STATS | 0,911 | [0,756 – 1,000] | 0,900 |
| **Verbalizzazione V2** | 0,889 | [0,733 – 1,000] | 0,866 |
| SAX_SYMBOLIC | 0,733 | [0,533 – 0,933] | 0,699 |

**Nessun confronto a coppie risulta significativo** dopo correzione Holm–Bonferroni con test consapevoli della struttura a cluster: i valori corretti restano tutti sopra 0,42. Con 15 casi indipendenti, l'effetto minimo rilevabile è di circa 25 punti percentuali. Con questo campione **non è possibile stabilire una graduatoria**.

Il dato operativamente rilevante riguarda il costo in **token in ingresso**, cioè i token di prompt. I valori sono i totali per braccio riportati dall'artefatto, dove figurano come stima (`est_prompt_tokens`):

| Braccio | Token in ingresso |
| --- | ---: |
| Verbalizzazione V2 | 2 541 |
| SAX_SYMBOLIC | 13 443 |
| RAW_FEATURES | 50 798 |
| CGTIME_STATS | 342 136 |

La verbalizzazione V2 usa circa **20 volte meno token di RAW_FEATURES, 135 volte meno di CGTIME_STATS e 5,3 volte meno di SAX**, a parità statistica sui dati osservati. Questo è un dato di costo del prompt in questo confronto; **non costituisce un claim generale di efficienza della comunicazione**.

Due caveat necessari.

**Il confronto misura formato e informazione insieme.** La verbalizzazione V2 non è solo un formato diverso: incorpora soglie calcolate statisticamente e descrizioni dei trend che gli altri bracci non hanno. Il costo di quel pre-processing è esterno al budget di token del prompt.

**Il campione è piccolo e il modello è uno solo.** In questo confronto F13 è la classe su cui i bracci sbagliano o si astengono più spesso, ma con un pattern che dipende dal braccio: la verbalizzazione V2 tende a confonderlo con F8, gli altri due bracci principali tendono ad astenersi. È un'osservazione su questa rappresentazione e su questo campione, non una proprietà generale della classe.

---

## 11 · Costo della comunicazione

*Categoria: misura descrittiva sugli artefatti congelati.*

Questa sezione quantifica quanto testo viene effettivamente scambiato. Non sono state eseguite nuove inferenze e nessun risultato è stato modificato: i prompt sono stati ricostruiti in modo deterministico e tutti gli hash verificati contro i log delle predizioni.

Senza queste misure non si potrebbe dire nulla sul costo del metodo. Con queste misure si può dire quanto costa, **non** che sia più economico o più efficiente di metodi che scambiano logit, prototipi o parametri.

### 11.1 Che cosa viene scambiato

L'unità primaria è il blocco realmente inserito nel prompt del consumatore: intestazione `PEER INSIGHTS`, array JSON UTF-8 indentato, due ritorni a capo finali.

La libreria contiene **8 insight unici, 2 per produttore**, e occupa 3 108 caratteri, 3 125 byte. Ogni consumatore riceve i 6 insight prodotti dagli altri tre.

| Consumatore | Insight | Caratteri | Byte | Token in contesto (GPT) | Token in contesto (Qwen) |
| --- | ---: | ---: | ---: | ---: | ---: |
| agente 1 | 6 | 2 289 | 2 304 | 664 | 724 |
| agente 2 | 6 | 2 327 | 2 336 | 684 | 749 |
| agente 3 | 6 | 2 410 | 2 420 | 681 | 747 |
| agente 4 | 6 | 2 361 | 2 378 | 690 | 754 |
| **Unità completa, 4 riceventi** | **24 consegne** | **9 387** | **9 438** | **2 719** | **2 974** |

I token sono incrementi **esatti in contesto**, ricavati dai log del provider, non tokenizzazioni isolate del blocco. Per il modello proprietario il nome e la versione del tokenizer non sono congelati; per il modello aperto è congelata la revisione ma non i file del tokenizer. Le stime isolate per singolo insight non vanno presentate come misure esatte.

### 11.2 Controllo strutturale fra B ed E

Il controllo è **superato**. Per ogni ricevente, B ed E hanno stesso numero di insight, stessi identificativi, fonti, ordine, chiavi, pattern osservati, caratteri, parole, righe, byte e stessi conteggi di token osservati in entrambi i consumatori.

**Non sono identici byte per byte**: E cambia esclusivamente i sei valori di pseudolabel secondo lo scompaginamento congelato. Le pseudolabel sono tutte ASCII da 9 byte, quindi la lunghezza resta invariata. In totale 24 sostituzioni e 112 posizioni byte differenti, senza inserimenti né cancellazioni.

La parità di token è una misura osservata per questi modelli e questi prompt, non una proprietà generale delle stringhe permutate.

### 11.3 Costo di produzione, trasferimento e consumo

La produzione degli insight è un costo una tantum: **4 chiamate**, 7 954 token in ingresso, 820 in uscita, 0 token di ragionamento, 9 secondi di latenza registrata.

Il trasferimento non è una chiamata separata: il suo costo è l'incremento nel prompt del consumatore. I token di ragionamento sono inclusi in quelli di uscita e non vanno sommati di nuovo.

| Esperimento | Cond. | Byte payload | Token payload | Token ingresso | Token uscita | Corrette su guasti mai visti |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| Studio principale | A | 0 | 0 | 291 567 | 28 155 | 0/36 |
| Studio principale | B | 424 710 | 122 355 | 413 922 | 27 888 | 31/36 |
| Studio principale | E | 424 710 | 122 355 | 413 970 | 28 792 | 3/36 |
| Replica | A | 0 | 0 | 581 670 | 55 426 | 0/72 |
| Replica | B | 849 420 | 244 710 | 826 476 | 57 236 | 68/72 |
| Replica | E | 849 420 | 244 710 | 826 380 | 59 614 | 4/72 |
| Verifica altro LLM | A | 0 | 0 | 287 205 | 101 766 | 0/36 |
| Verifica altro LLM | B | 424 710 | 133 830 | 421 035 | 150 705 | 34/36 |
| Verifica altro LLM | E | 424 710 | 133 830 | 421 035 | 151 179 | 1/36 |
| Riferimento centralizzato | C | 570 060 | solo stima | 209 118 | 5 869 | 15/15 complessivo |

Per il riferimento centralizzato i due blocchi aggiunti occupano 12 668 byte per chiamata; le stime sono 3 650 e 3 992 token, ma il delta esatto non è isolabile dai log.

Non è calcolato alcun costo monetario: il repository non congela prezzi applicabili.

### 11.4 Round e volumi

Ogni braccio B o E usa una libreria statica: **un round logico di conoscenza**, 12 archi diretti da sorgente a consumatore, 4 blocchi specifici per ricevente, 24 consegne. Il blocco viene però **reinserito in ogni chiamata**.

| Esperimento | Round logici | Blocchi reinseriti | Insight consegnati | Byte | Token in contesto |
| --- | ---: | ---: | ---: | ---: | ---: |
| Studio principale (B+E) | 2 | 360 | 2 160 | 849 420 | 244 710 |
| Replica (B+E) | 2 | 720 | 4 320 | 1 698 840 | 489 420 |
| Verifica altro LLM (B+E) | 2 | 360 | 2 160 | 849 420 | 267 660 |

Il payload di B rappresenta circa il 32,5 % dei byte e il 29,6 % dei token del prompt completo nello studio principale, valori analoghi nella replica, e il 32,5 % / 31,8 % nella verifica con l'altro modello.

### 11.5 Confronto concettuale con paradigmi adiacenti

| Paradigma | Oggetto trasmesso | Leggibilità | Dipendenza dal modello | Verificabilità |
| --- | --- | --- | --- | --- |
| FedMD | logit su esempi condivisi | bassa | spazio di uscita compatibile | tensori e dataset ispezionabili |
| FedProto | prototipi medi per classe | bassa–media | spazio di embedding | semantica indiretta |
| Adapter / LoRA federati | parametri addestrabili | bassa | architettura, layer, rango | provenienza binaria |
| Trasferimento testuale | record JSON testuali | alta per ispezione umana | tokenizzazione e uso dipendono dal consumatore | contenuto, ordine, corrispondenze e hash verificabili |

Il confronto è **concettuale e non isomorfo**: byte di testo, logit, prototipi e parametri non sono equivalenti. Non sono prodotti numeri attribuiti agli algoritmi originali. Le misure riportate qui non dimostrano privacy, efficienza di banda o superiorità rispetto al federated learning parametrico.

---

## 12 · Che cosa il framework mostra e che cosa non mostra

Questa è l'unica sezione in cui sono raccolti i limiti. Le sezioni precedenti riportano i fatti osservati; qui si dice che cosa se ne può inferire.

### 12.1 Che cosa mostra

Una descrizione testuale corretta può portare a un agente conoscenza discriminante che non possiede. Il risultato è forte nel campione osservato — da 0/36 a 31/36 — e si ripete su realizzazioni simulate indipendenti — da 0/72 a 68/72.

Il beneficio non è spiegabile con la semplice presenza di più testo nel prompt: a parità di identificativi, testi, ordine e volume, la corruzione delle associazioni fa scendere il risultato a 3/36 e 4/72.

Il beneficio non è spiegabile con il semplice possesso di insight: fornire all'agente i propri, nella stessa posizione del prompt, lascia il risultato a 0/36 esattamente come senza.

La rappresentazione intermedia è deterministica e verificabile: ogni frase del testo neutrale è riconducibile ai numeri di partenza.

### 12.2 Che cosa non mostra

**Non mostra superiorità diagnostica.** Sul campione confrontato la baseline numerica a prototipi condivisi ottiene 36/36 contro 31/36. Il metodo testuale è meno accurato. I vantaggi qualitativi che gli si attribuiscono — leggibilità, verificabilità, assenza di addestramento del consumatore — non sono stati quantificati come compensazioni.

**Non mostra equivalenza con il federated learning parametrico.** Manca un algoritmo di federated learning pubblicato eseguito sullo stesso compito disgiunto per classe. La baseline numerica è ispirata a FedProto ma non è FedProto; FedAvg e le altre suite non sono state eseguite. La collocazione nel panorama del FL resta quindi incompleta.

**Non mostra assenza di interferenza sui guasti già noti.** La replica ha rilevato una degradazione: 19/24 contro 24/24. Lo stesso fenomeno compare nella verifica con l'altro modello linguistico, dove i guasti già noti scendono a 9/12 sui dati dello studio principale. La variante local-first riporta il valore a 23/24 sulla replica, ma **è stata progettata dopo l'osservazione degli errori, è stata provata sullo stesso campione che li aveva mostrati e deve essere replicata su dati indipendenti**. Nel suo perimetro non elimina ogni regressione a livello di singolo caso.

**Non mostra generalità cross-model.** La portabilità è stata verificata **solo lato consumatore**: gli insight sono ancora prodotti da un unico modello proprietario. Non è stato verificato che cosa accada se a produrli è un modello diverso.

**Non mostra funzionamento in mondo aperto.** L'agente sceglie fra le pseudolabel presenti nel prompt. Il protocollo prevede l'astensione, ma questa possibilità **non è stata verificata su guasti realmente fuori catalogo**: non si sa se davanti a un guasto completamente nuovo il sistema si asterrebbe o sceglierebbe erroneamente una classe nota.

**Non mostra scala né generalità industriale.** Quattro agenti, quattro guasti standard fra i 21 del processo, 12 e 24 run simulati, un solo simulatore, una sola configurazione di ragionamento. L'effetto minimo rilevabile nel confronto delle rappresentazioni è di circa 25 punti percentuali.

**Non mostra praticabilità della federazione.** I quattro nodi sono processi logici. Non esistono siti distinti, proprietari diversi, nodi che vanno offline, latenze o reti instabili. Il coordinamento, che in un sistema federato reale è la parte difficile, non è stato affrontato.

**Non mostra robustezza nel tempo.** Gli insight vengono creati una volta e non cambiano. Non c'è iterazione, non c'è aggregazione, non c'è aggiornamento. Non si sa come regga con deriva dei dati, insight iniziali errati, ritardi o molti nodi.

**Non mostra privacy.** Non vengono inviate serie grezze né parametri, ma le descrizioni contengono informazioni statistiche dettagliate. Non è stato tentato alcun attacco di ricostruzione e non esistono garanzie formali.

**Non mostra efficienza di comunicazione.** Le misure di §11 descrivono un costo osservato. Senza un confronto diretto con metodi che scambiano logit, prototipi o parametri, non si può affermare che il metodo sia più leggero.

**Non mostra trasferibilità della rappresentazione.** Il verbalizzatore non ha feature nel dominio della frequenza né adattamento alla deriva; le soglie sono calibrate su questo processo. Se la traduzione in testo non cattura un pattern diagnostico, nessun insight potrà trasmetterlo. Il confronto delle rappresentazioni non stabilisce una graduatoria e cambia contemporaneamente formato e quantità di informazione preparata a monte.

**Non mostra validazione su un impianto reale.** Tutti gli esperimenti usano un processo simulato.

**Non mostra che la statistica sia ampia.** Con 12 e 24 cluster indipendenti gli intervalli sono utilizzabili ma stretti sul piano della portata: valgono per questo studio controllato.

### 12.3 La lettura d'insieme

L'esperimento è una buona prova controllata: mostra che una descrizione testuale corretta può portare a un agente la conoscenza che gli manca, e che il beneficio dipende dal contenuto e non dal volume del testo. Il punto debole è che questa conoscenza viene fornita a B per costruzione, mentre A non possiede alcun collegamento alle classi remote.

Il grande vantaggio di B dimostra quindi il **meccanismo**, non la superiorità di un sistema federato completo.

### 12.4 Riferimenti descrittivi, non prove

Due elementi vanno letti come collocazione e non come evidenza. Gli otto modelli centralizzati vedono tutte le classi in addestramento e raggiungono il 100% anche sui casi di training: il loro risultato dice che il benchmark è facilmente separabile, non che il metodo federato sia inferiore a un metodo federato. Il riferimento testuale centralizzato è stato introdotto dopo aver visto i risultati, riceve più contesto e in forma diversa, ed esiste solo per lo studio principale: la distanza da B è descrittiva e non causale.

---

## 13 · Aderenza alla conferenza

La [call ufficiale della Special Session su Federated Learning on Big Data, IEEE BigData 2026](https://bigdataieee.org/BigData2026/calls/special-federated-learning/) include dati distribuiti, distribuzioni non-IID, aggregazione, personalizzazione, privacy, sicurezza, dispositivi edge, evaluation e benchmarking, le cinque V e applicazioni IoT.

### 13.1 Assi su cui il lavoro aderisce, con evidenza

- **Dati distribuiti ed eterogenei per classe** — i quattro agenti hanno esperienze locali disgiunte; è la forma estrema di distribuzione non-IID.
- **Trasferimento collaborativo di conoscenza** — gli agenti condividono insight testuali, non aggiornamenti di modello.
- **Variety** — serie industriali multivariate e firme di guasto eterogenee.
- **Veracity** — risposta corretta verificabile, verbalizzazione deterministica, artefatti congelati, controllo B/E.
- **Value** — si valuta se la conoscenza dei pari consenta la diagnosi di guasti localmente non osservati.
- **Evaluation e benchmarking** — protocollo a quattro condizioni, replica su nuovi run, analisi di sensibilità, confronti controllati e confronto numerico sullo stesso compito. È l'asse su cui il contributo è più solido.
- **Contesto industriale e IoT** — banco di prova industriale simulato pertinente al tema.

### 13.2 Assi su cui non c'è evidenza

Volume, Velocity, deployment su dispositivi edge, scalabilità a molti nodi, privacy, sicurezza e validazione su impianto reale **non sono risultati di questo studio**. Il dettaglio dei limiti corrispondenti è in **§12**.

### 13.3 Framing corretto

Il framing appropriato è **trasferimento federato di conoscenza testuale**, cioè apprendimento collaborativo di tipo FL-like, non federated learning parametrico classico. Non vengono aggregati parametri, gradienti o modelli, e non viene costruito iterativamente un modello globale.

Il rischio di posizionamento è reale e va anticipato: un revisore legato alla definizione canonica di federated learning potrebbe considerare questo lavoro distante dal perimetro della sessione. La risposta più difendibile è duplice — inquadrare il lavoro come esplorazione di un estremo nella traiettoria dell'oggetto federato (parametri → logit → prototipi → testo), e valorizzare il contributo di evaluation e benchmarking, che è un tema esplicito della call.

Il limite di novità è già circoscritto in §1.3: FoT è di Yao et al., e il contributo è la combinazione descritta in §1.4.

*Valutazione editoriale basata sui materiali del progetto e sulla call consultata il 10 settembre 2026. Requisiti di formato e scadenze vanno verificati sulle istruzioni ufficiali della sessione.*

---

## 14 · Letteratura

Questa sezione unifica i materiali di `docs/lit_review`, il workbook bibliografico e i paper convertiti in `papers/`. Sono inclusi i lavori che incidono su almeno uno degli assi dell'esperimento: oggetto federato, classi localmente non osservate, trasformazione da serie temporale a testo, diagnosi mediante modelli linguistici.

Al corpus originario si aggiungono i **venticinque lavori di federazione con modelli linguistici** raccolti in [`papers/archive/fed_fsl_2026-07/`](../papers/archive/fed_fsl_2026-07) e verificati sul testo integrale dall'audit di prior art conservato nella stessa cartella. Di questi, **diciannove** incidono su almeno uno degli assi e compaiono in §14.1; **sei** riguardano federated prompt learning parametrico su benchmark visivi, sono stati esaminati e lasciati fuori perimetro. L'esclusione è documentata in §14.4, non implicita.

**Il corpus si è allargato oltre i quattro assi.** I trentacinque lavori entrati nel settembre 2026 — diagnosi e monitoraggio centralizzati sul Tennessee Eastman, calibrazione conforme, soglie statistiche — **non toccano nessuno degli assi**. Entrano perché condividono il banco di prova e documentano il perimetro consultato. **Nessuno di essi è 🟢**: nessuno incide sul disegno e nessuno vieta un'affermazione di questo documento, quindi nessuno ha una scheda in §14.2.

Le schede estese, in §14.2, riguardano soltanto i lavori che **influenzano direttamente il disegno**. Per gli altri, la tabella e i file in `docs/lit_review` sono sufficienti.

### 14.1 Corpus completo

La tabella è divisa per categoria: apri quella che ti serve, richiudila con la **✕** nell'intestazione o con il pulsante in fondo al pannello. La colonna **Vicinanza** dice quanto il lavoro tocca questo esperimento.

| Icona | Significato | Che cosa comporta |
| :---: | --- | --- |
| 🟢 | **Vicino** | Incide sul disegno o delimita un claim: va citato e discusso, non solo elencato |
| 🟡 | **Adiacente** | Condivide un asse — dominio, regime non-IID o payload — ma non cambia le nostre scelte: citazione di contesto |
| 🔴 | **Distante** | Sfondo del campo: serve a mostrare il perimetro consultato, non richiede discussione |

Complessivamente: **117 lavori**, di cui 34 🟢, 47 🟡, 36 🔴.

Autori e anno provengono da fonti già verificate nel repository: l'audit di prior art, la gap analysis e la scansione del related work. Un trattino **—** significa che il dato **non è stato verificato su fonte ufficiale**: è 1 lavoro su 117, e va confermato prima di usarli in bibliografia.

<details>
<summary><strong>Federazione testuale</strong> · 14 lavori · 🟢 7 · 🟡 5 · 🔴 2</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Federation over Text: Insight Sharing for Multi-Agent Reasoning | Yao, Rabbani, Zaheer, Li, 2026 | 🟢 |
| Federated In-Context LLM Agent Learning (FICAL) | Wu, Li, Nan, Wang, 2024 | 🟢 |
| SYNAPSE: Federated Tool Routing via Typed Compendium Artifacts | Chakraborty, Shah, Gupta, 2026 | 🟢 |
| Federated In-Context Learning: Iterative Refinement for Improved Answer Quality (Fed-ICL) | Wang, Wang, Huang, Wang, Yu, Yao, Lui, Zhou, 2025 | 🟢 |
| FERA: Uncertainty-Aware Federated Reasoning for Large Language Models | Wang, Huang, Wang, Wu, Wang, Yu, McAuley, Yao, Zhou, 2026 | 🟢 |
| Can Textual Gradient Work in Federated Learning? (FedTextGrad) | Chen, Jin, Deng, Chen, Huang, Yu, Li, 2025 | 🟢 |
| Time-FFM: LM-Empowered Federated Foundation Model for Time Series Forecasting | Liu et al., 2024 | 🟢 |
| Implicit Federated In-Context Learning for Task-Specific LLM Fine-Tuning (IFed-ICL) | Li, Chen, Zhou, Li, Xian, Liu, Li, 2025 | 🟡 |
| AsynDBT: Asynchronous Distributed Bilevel Tuning for Efficient In-Context Learning | Ma, Dou, Liu, Xing, Feng, Pi, 2026 | 🟡 |
| Fed-SE: Federated Self-Evolution for Cross-Environment Knowledge Transfer | Chen, Shi, Lan, Qiu, Wang, Gu, Yan | 🟡 |
| Social Learning: Towards Collaborative Learning with LLMs | Mohtashami et al., 2023 | 🟡 |
| FedCoT: Communication-Efficient Federated Reasoning Enhancement for LLMs | Li et al., 2025 | 🟡 |
| Federation of Agents: A Semantics-Aware Communication Fabric for Large-Scale Agentic AI | Giusti et al. (CERN) | 🔴 |
| FedSRD: Communication-Efficient Federated LLM Fine-Tuning via Sparsify-Reconstruct-Decompose | Yan et al., 2026 | 🔴 |

</details>

<details>
<summary><strong>FL disgiunto per classe</strong> · 9 lavori · 🟢 7 · 🟡 2</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| FedMD: Heterogeneous Federated Learning via Model Distillation | Li & Wang, 2019 | 🟢 |
| FedProto: Federated Prototype Learning across Heterogeneous Clients | Tan et al., 2022 | 🟢 |
| FedCKD: Knowledge Distillation with Label-Exclusive Clients | Le, Le, Le, Truong-Huu, 2026 | 🟢 |
| FedMeta-FFD: Federated Meta-Learning for Fault Diagnosis | Chen, Tang, Li, 2023 | 🟢 |
| Federated Zero-Shot Learning with Mid-Level Semantic Knowledge Transfer | Sun, Si, Wu, Gong, 2024 | 🟢 |
| Federated Meta-Learning with Transformer Fusion for Few-Shot Multi-Condition Fault Diagnosis | Zhang et al., 2026 | 🟢 |
| Federated Learning Based on Fuzzy Fusion Rules for Chemical Production Process Fault Diagnosis | Xu et al., 2026 | 🟢 |
| FedMAPS: A Federated Meta-Learning Framework with Adaptive Cross-Domain Contrastive Learning for Few-Shot Fault Diagnosis | Sun, Lu, Chen, Xiang, Hu, 2026 | 🟡 |
| FedAPA-FD: Class-Sensitive Personalized Federated Learning for Non-IID Bearing Fault Diagnosis | Yu, Li, Zhou, 2026 | 🟡 |

</details>

<details>
<summary><strong>Contesto e memoria testuale</strong> · 4 lavori · 🟢 1 · 🟡 2 · 🔴 1</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Agentic Context Engineering: Evolving Contexts for Self-Improving Language Models (ACE) | Zhang, Hu, Upasani et al., Zou, Olukotun, 2026 | 🟢 |
| FORGE: Self-Evolving Agent Memory With No Weight Updates via Population Broadcast | Bogdanov, Lung, Kunz, Taylor, Gao, Zaman, 2026 | 🟡 |
| Evo-Memory: Benchmarking LLM Agent Test-time Learning with Self-Evolving Memory | Wei, Sachdeva et al. (Google DeepMind), 2026 | 🟡 |
| TextGrad: Automatic "Differentiation" via Text | Yuksekgonul, Bianchi, Boen, Liu, Huang, Guestrin, Zou, 2024 | 🔴 |

</details>

<details>
<summary><strong>Federated few-shot e privacy</strong> · 5 lavori · 🟢 2 · 🟡 3</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Privacy-Preserving Personalized Federated Prompt Learning for Multimodal LLMs (DP-FPL) | Tran, Sun, Patterson, Milanova, 2025 | 🟢 |
| FedDTPT: Federated Discrete and Transferable Prompt Tuning for Black-Box LLMs | Wu, Chen, Yang et al. | 🟢 |
| Federated Few-shot Learning (F²L) | Fu, Wang, Ding, Chen, Chen, Li, 2023 | 🟡 |
| Personalized Federated Few-Shot Learning (pFedFSL) | Zhao, Yu, Wang, Domeniconi, Guo, Zhang, Cui, 2024 | 🟡 |
| PPFedIT: Towards Privacy-preserving Federated Instruction Tuning with Few-shot Local Examples | Zhang, Zhang, Huang et al., 2026 | 🟡 |

</details>

<details>
<summary><strong>TS→testo fedele</strong> · 7 lavori · 🟢 4 · 🟡 1 · 🔴 2</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Truth-Conditional Captions for Time Series Data | Jhamtani & Berg-Kirkpatrick, 2021 | 🟢 |
| Representing Time Series as Structured Programs for LLM Reasoning (T2SP) | Kim et al., 2026 | 🟢 |
| CGTime: Decoupling Perception from Description in Time-Series Reasoning | Feng, Xie, Zhang, Li, Ling, Li, Liu | 🟢 |
| S2S-FDD: Bridging Industrial Time Series and Natural Language for Explainable Zero-shot Fault Diagnosis | Li & Zhao, 2025 | 🟢 |
| An On-the-Fly Signals-to-Semantics Storytelling Framework for Explainable Industrial Maintenance Decisions | Yue, Zhao, Cheng, 2026 | 🟡 |
| A Fuzzy Approach to Data-to-Text for Time Series | Ramos-Soto, Janeiro, Alonso, Bugarín et al., 2017 | 🔴 |
| ICA2TEXT: Data-to-Text for Air-Quality Time Series | Cascallar-Fuentes et al., 2022 | 🔴 |

</details>

<details>
<summary><strong>Rappresentazioni simboliche</strong> · 4 lavori · 🟢 1 · 🟡 1 · 🔴 2</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Bridging Time Series and Large Language Models via Symbolic Representation for HAR | Pappa, Karvelis & Stylios, 2026 | 🟢 |
| A Novel Feature Extraction Approach for Mechanical Fault Diagnosis Based on ESAX and BoW | Zhao et al., 2022 | 🟡 |
| HSQP: Hierarchical Symbolic Quantization Prompting for Time-Series Forecasting | Abdullahi et al., 2026 | 🔴 |
| LLM-ABBA: Understanding Time Series via Symbolic Approximation | Chen, Carson, Kang, 2026 | 🔴 |

</details>

<details>
<summary><strong>LLM per fault diagnosis</strong> · 10 lavori · 🟢 3 · 🟡 5 · 🔴 2</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Evidence-Traceable LLM Reporting for Industrial Process Fault Detection and Diagnosis (EviFDD-Agent) | Chen, Peng, Zhang, Zhu, Hu, Zhai et al., 2026 | 🟢 |
| Exploring LLM-based Agentic Frameworks for Fault Diagnosis | Lee, Vidyaratne, Farahat, Gupta, 2025 | 🟢 |
| FaultExplainer: Leveraging Large Language Models for Interpretable Fault Detection and Diagnosis | Khan, Nahar, Chen, Constante-Flores, Li, 2025 | 🟢 |
| FD-LLM: Large Language Model for Fault Diagnosis of Machines | Qaid et al., 2024 | 🟡 |
| FD-LLM: Large Language Model for Fault Diagnosis of Complex Equipment | Lin et al., 2025 | 🟡 |
| LLM-TSFD: Industrial Time-Series Human-in-the-Loop Fault Diagnosis | Zhang, Xu, Li, Sun, Bao, Zhang, 2024 | 🟡 |
| A Large Language Model Enhanced Fault Diagnosis Framework for Chemical Processes | Liang & Sin, 2026 | 🟡 |
| Enhanced Fault Diagnosis Using Large Language Models and Probabilistic Label Fusion | Chen, Yao, Wang, Shi, Qin, Li et al., 2025 | 🟡 |
| CL-LLMOps: Fuzzy-Gated Verification of LLM Agents for Industrial Fault Diagnosis | Xiao, Xu, Li, Ding, Huang (identità da confermare), 2026 | 🔴 |
| DML–LLM Hybrid Architecture for Fault Detection and Diagnosis in Sensor-Rich Industrial Systems | Hu, Marandi, Modarres, 2026 | 🔴 |

</details>

<details>
<summary><strong>Calibrazione e predizione conforme</strong> · 18 lavori · 🟢 6 · 🟡 9 · 🔴 3</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Class-Conditional Conformal Prediction for Reliable Open-Set Fault Diagnosis in Safety-Critical Industrial Systems | Heddoub et al., 2026 | 🟢 |
| Testing for Outliers with Conformal p-values | Bates, Candès, Lei, Romano, Sesia, 2023 | 🟢 |
| Conditional validity of inductive conformal predictors | Vovk, 2012 / 2013 | 🟢 |
| Conformal Prediction via Transported Beta Laws | Ramos, Graziadei, Cabezas, 2026 | 🟢 |
| Universal distribution of the empirical coverage in split conformal prediction | Marques F., 2025 | 🟢 |
| Training-conditional coverage for distribution-free predictive inference | Bian & Barber, 2023 | 🟢 |
| Uncertainty-Aware Fault Diagnosis with Conformal Prediction | Heddoub, Diallo, Homri, Dantan, Siadat, 2025 | 🟡 |
| RBC-AD: conformal anomaly detection with explicit false-alarm control for the Tennessee Eastman Process | Mudasir, Asiri, Ameer, Al Reshan, Almansour, Awan, Shaikh, 2026 | 🟡 |
| Reducing false alarms in fault detection: a comparative analysis between conformal prediction and classical methods applied to PCA and autoencoders | Diallo, Homri, Dantan, 2025 | 🟡 |
| Quantifying and mitigating alarm fatigue caused by fault detection systems | Diallo, Homri, Boeuf, Dantan, Bonnet, 2026 | 🟡 |
| Conformal machine learning for reliable anomaly detection in industrial cyber-physical systems | Yuan, Li, Wang, Zhang, 2026 | 🟡 |
| Adaptive Conformal Anomaly Detection with Time Series Foundation Models for Signal Monitoring | Martinez Gil, O'Donncha, Gifford, Zhou, Patel, Vaculin, 2026 | 🟡 |
| Semi-supervised concept drift detection and adaptation based on conformal martingale framework | Zhang, Zhou, Zhang, Lu, Chai, 2025 | 🟡 |
| Conformal Anomaly Detection for Predictive Maintenance in Thermal Power Plants | Kundačina, Vincan, Gojić, Ninković, Mišković, 2025 | 🟡 |
| The Tight Constant in the Dvoretzky–Kiefer–Wolfowitz Inequality | Massart, 1990 | 🟡 |
| CODiT: Conformal Out-of-Distribution Detection in Time-Series Data for Cyber-Physical Systems | Kaur, Sridhar, Park, Yang, Jha, Roy, Sokolsky, Lee, 2023 | 🔴 |
| Out-of-distribution Detection in Dependent Data for Cyber-physical Systems with Conformal Guarantees (estensione di CODiT) | Kaur, Yang, Sokolsky, Lee, 2024 | 🔴 |
| Between Resolution Collapse and Variance Inflation: Weighted Conformal Anomaly Detection in Low-Data Regimes | Hennhöfer & Preisach, 2026 | 🔴 |

Le sette voci 🟡 aggiunte nel 2026-09 calibrano o controllano esplicitamente l'errore **su TEP o su processi industriali**: è il terreno che questo studio non presidia, perché [§6.3](#sez-6-protocollo-di-valutazione) conta l'astensione come errore e [§12.2](#sez-12-che-cosa-il-framework-mostra-e-che-cosa) dichiara non verificato il funzionamento in mondo aperto. Le tre 🔴 riguardano domini ciberfisici estranei al processo chimico o sono puramente metodologiche. Nessuna vieta un'affermazione di questo documento. Le tre entrate del 2026-09-12 non sono applicative ma **fondazionali**, e cambiano il registro della categoria: sono le fonti primarie su cui poggia la calibrazione delle soglie di Fase B, e dicono con quali ipotesi ciascuna garanzia vale. Sono perciò le prime 🟢 teoriche del corpus. Massart (1990) entra invece come 🟡 e non 🟢: è la fonte della costante che rende DKW utilizzabile, quindi va citato **se** si riportano numeri DKW, ma non delimita alcuna affermazione di questo studio. Le due entrate del 2026-09-11 spostano leggermente il perimetro: Kundačina et al. controllano il tasso di falsi positivi su un impianto reale senza taratura manuale della soglia, e Zhang et al. usano gli intervalli conformi per **selezionare gli pseudolabel affidabili** prima di riaddestrare. Quest'ultimo è l'alternativa di principio a ciò che qui si fa di proposito — consumare gli pseudolabel opachi senza filtrarli — e va citato quando si giustifica la condizione E invece di un pesaggio per affidabilità.

</details>

<details>
<summary><strong>Allineamento TS–linguaggio</strong> · 9 lavori · 🟢 1 · 🟡 2 · 🔴 6</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| TableTime: Reformulating Time Series Classification as Training-Free Table Understanding with LLMs | Wang, Cheng, Mao, Zhou, Wang, Liu et al., 2025 | 🟢 |
| FD-Zero: LLM-Based Diagnosis Framework for Zero-Shot Mechanical Time-Domain Signals | Ran, Li, Li, Li, Wang, Chu et al., 2025 | 🟡 |
| Towards Generalizable Fault Diagnosis via LLM-Driven Hierarchical Cross-Modal Alignment (HCMA_GPT) | Wang, Sun, Zhang, Shao, Xiao, Liu, 2026 | 🟡 |
| T3: Domain-Agnostic Neural Time-Series Narration | Sharma, Brownstein & Ramakrishnan, 2021 | 🔴 |
| Repr2Seq: Time Series Representation to Sequence | Li et al., 2023 | 🔴 |
| TADACap: Time-Series Image Retrieval for Domain-Aware Captioning | Fons et al., 2024 | 🔴 |
| CLaSP: Contrastive Language–Signal Pretraining | Ito, Dohi & Kawaguchi, 2025 | 🔴 |
| TSLM: Time Series Language Model for Descriptive Caption Generation | Trabelsi, Boyd, Cao, Uzunalioğlu, 2025 | 🔴 |
| Towards Semantically Faithful Text-to-Time Series Generation via Agents and Spectral Conditioning | Wu, Lu, Zheng, Liu, Zhang, 2026 | 🔴 |

</details>

<details>
<summary><strong>Survey e benchmark</strong> · 8 lavori · 🟢 2 · 🟡 2 · 🔴 4</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Federated Reasoning LLMs: A Survey | Wei, Tong, Zhou, Xu, Gao, Tu et al., 2025 | 🟢 |
| Can LLMs Understand Time Series Anomalies? | Zhou & Yu, 2025 | 🟢 |
| BEDTime: A Unified Benchmark for Automatically Describing Time Series | Sen, Gottesman, Qiu, Bruss, Nguyen, Hartvigsen, 2025 | 🟡 |
| Data-Driven Fault Detection and Diagnosis in Industrial Process Systems: A Systematic Review and Perspective | Zhao, Yang, Kareck, Khan, Wang, 2025 | 🟡 |
| Empowering Time Series Analysis with Large Language Models: A Survey | Jiang et al., 2024 | 🔴 |
| Time-Series Large Language Models: A Systematic Review | Abdullahi et al., 2025 | 🔴 |
| Large Language Models for Time-Series Reasoning: A TMLR Survey | — | 🔴 |
| A Review of Fault Diagnosis Methods: From Traditional Machine Learning to Large Language Model Fusion Paradigm | Nie, Geng, Liu, 2026 | 🔴 |

</details>

<details>
<summary><strong>Diagnosi e monitoraggio di processo centralizzati su TEP</strong> · 24 lavori · 🟡 15 · 🔴 9</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| TopoCausFormer (TCF-STAE): spatio-temporal representation learning per la diagnosi in processi industriali complessi | Peng, Tang, Li, Simani, Dong, 2026 | 🟡 |
| A novel deep learning based fault diagnosis approach for chemical process with extended deep belief network | Wang, Pan, Yuan, Yang, Gui, 2020 | 🟡 |
| A novel fault diagnosis method based on CNN and LSTM and its application in fault diagnosis for complex systems | Huang, Zhang, Tang, Zhao, Lu, 2022 | 🟡 |
| HDLCNN-SHAP: hierarchical dilated CNN order-invariant e interpretabile per rilevazione e diagnosi chimica | Li, Peng, Wang, Wang, 2023 | 🟡 |
| DACN: dual adversarial and contrastive network per single-source domain generalization nella diagnosi | Li, Atoui, Li, 2025 | 🟡 |
| ES-QLSTM: entropy space quantum-behaved dung beetle optimized LSTM per la diagnosi di processo | Ao, Ma, Liu, Li, Han, 2026 | 🟡 |
| SAEDLPP: improved discrimination locality preserving projections integrate con sparse autoencoder | He, Li, Zhang, Xu, Zhu, 2021 | 🟡 |
| Fault Diagnosis of Chemical Processes Based on PCA-MSRN | Sun, 2026 | 🟡 |
| Improving Accuracy and Interpretability of CNN-Based Fault Diagnosis through an Attention Mechanism | Huang, Zhang, Liu, Zhao, 2023 | 🟡 |
| Inception-SECA-BiLSTM: estrazione multi-scala con attenzione per la diagnosi di processo | Lv, Wang, Gao, Zhang, 2026 | 🟡 |
| MDGCN: multichannel dynamic graph convolutional network, applicato all'altoforno | Wu, Wang, Gao, Zhang, Lou, Yang, 2023 | 🟡 |
| TDLN-trees: three-layer deep learning network random trees per la produzione chimica | Lu, Gao, Zou, Chen, Li, 2024 | 🟡 |
| Deep Anomaly Detection on Tennessee Eastman Process Data | Hartung et al., 2023 | 🟡 |
| Comparison of autoencoder architectures for fault detection in industrial processes | Spina et al., 2024 | 🟡 |
| Early-warning industrial fault detection based on physics-guided residual learning and calibrated CRNNs | Khan et al., 2026 | 🟡 |
| Automated feature learning for nonlinear process monitoring – stacked denoising autoencoder e regola k-NN | Zhang, Jiang, Li, Yang, 2018 | 🔴 |
| MSLKPCA: multi-block statistics local kernel PCA per il rilevamento non lineare | Zhou & Gu, 2020 | 🔴 |
| CVKA: Nonlinear Dynamic Process Monitoring Using Canonical Variate Kernel Analysis | Li, Yang, Cao, 2023 | 🔴 |
| Temporal-Spatial Neighborhood Enhanced Sparse Autoencoder per il monitoraggio dinamico non lineare | Li, Shi, Song, Tao, 2020 | 🔴 |
| TceOne: temporal CapsNet encoder con classificatore one-class per le industrie di processo | Wang, Zhao, Han, Wang, 2023 | 🔴 |
| Incipient Fault Detection Using Sliding Window K-Means Shared Dictionary Learning | Shen, Chen, Shang, Zhu, Hu, 2026 | 🔴 |
| Real-time incipient fault detection con KSVD a finestra scorrevole e limiti di controllo adattativi | Wang, Zhou, Liu, 2026 | 🔴 |
| DAE-PCA: learnable faster kernel-PCA per il rilevamento non lineare, realizzazione con deep autoencoder | Ren, Jiang, Yang, Tang, Zhang, Yu, 2024 | 🔴 |
| Odiowei & Cao: CVA con stime di densità kernel per il monitoraggio dinamico non lineare | Odiowei & Cao, 2010 | 🔴 |

Categoria aperta nel 2026-09. **Nessuno di questi lavori è federato e nessuno usa modelli linguistici**: entrano perché condividono il banco di prova, non perché incidano sul disegno. 🟡 quelli che affrontano la **diagnosi multi-classe** su TEP — lo stesso compito delle condizioni A/B/E — o che sono **benchmark comparativi**, e come tali sostengono la lettura di [§9.2](#sez-9-confronti-esterni-e-riferimenti) e [§12.4](#sez-12-che-cosa-il-framework-mostra-e-che-cosa) secondo cui il benchmark è facilmente separabile. 🔴 quelli di **sola rilevazione** o monitoraggio statistico, che restano sfondo del campo. La voce del 2026-09-11 (Khan et al., 2026) è la prima della categoria a riportare **probabilità calibrate, ECE e intervalli bootstrap** sul TEP: rafforza la lettura di §9.2 sulla separabilità del banco — circa 99% di accuratezza con macro-F1 0,93 su split a livello di run — e mostra quale forma di governo della soglia la letteratura centralizzata considera ormai attesa.

</details>

<details>
<summary><strong>Rilevamento di anomalie e soglie statistiche</strong> · 5 lavori · 🔴 5</summary>

| Lavoro | Autori, anno | Vicinanza |
| --- | --- | :---: |
| Anomaly Detection in Streams with Extreme Value Theory (SPOT/DSPOT) | Siffer, Fouque, Termier, Largouët, 2017 | 🔴 |
| Anomaly Detection in Streaming Nonstationary Temporal Data (oddstream) | Talagala, Hyndman, Smith-Miles, Kandanaarachchi, Muñoz, 2019 | 🔴 |
| SHNN-CAD: Online Learning and Sequential Anomaly Detection in Trajectories | Laxhammar & Falkman, 2014 | 🔴 |
| One-class classification-based control charts for multivariate process monitoring | Sukchotrat, Kim, Tsung, 2010 | 🔴 |
| Structure-Aware Unsupervised Anomaly Detection for Spacecraft Telemetry with Adaptive EVT Thresholding | Alcarria, Sánchez, Sempere et al., 2026 | 🔴 |

Categoria aperta nel 2026-09. Sfondo metodologico su soglie statistiche e rilevamento sequenziale, su domini estranei al processo chimico: flussi generici, traiettorie di sorveglianza, carte di controllo, telemetria satellitare. Nessuno tocca gli assi dell'esperimento; servono a documentare il perimetro consultato, non richiedono discussione.

</details>

Le stringhe di ricerca che hanno prodotto ciascuna voce sono conservate in [`docs/lit_review`](lit_review), insieme alle schede complete.

### 14.2 Schede estese: i lavori che influenzano il disegno

Le schede riguardano i lavori che **influenzano direttamente il disegno**. Stessa modalità di §14.1: apri la categoria che ti serve e richiudila con la **✕** o con il pulsante in fondo.

> **Le schede sono 29, i 🟢 di §14.1 sono 34.** Una scheda riguarda un 🔴 (FedSRD), quindi i vicini con scheda sono 28 e **sei** restano senza: FICAL, DP-FPL, FedDTPT, T2SP, TableTime e la rassegna sui federated reasoning LLM. È un arretrato dichiarato, non una svista. EviFDD-Agent è uscito dall'arretrato nel 2026-09: delimita §8.9–§8.10 del piano sperimentale e non poteva restare senza scheda. FaultExplainer non è mai entrato nell'arretrato: individuato l'11 settembre 2026 come **assente da §14.1** durante la riconciliazione con `papers/`, è stato inserito già con la sua scheda. Lo stesso vale per le tre 🟢 fondazionali sulla predizione conforme, entrate il 2026-09-12 con la scheda contestuale.

<details>
<summary><strong>Federazione testuale</strong> · 7 schede</summary>

**Federation over Text: Insight Sharing for Multi-Agent Reasoning**  
*Yao, Rabbani, Zaheer, Li, 2026*

Agenti locali trasformano traiettorie in insight; un server li raggruppa, distilla e ridistribuisce senza condividere esempi o gradienti.

**Rapporto con questo lavoro** — *Somiglianza:* gli insight in linguaggio naturale come oggetto federato. *Differenza:* il lavoro originale è multi-round, basato su server e cross-task; qui il trasferimento è a colpo singolo, fra pari e disgiunto per classe. *Implicazione:* è il precedente obbligatorio; il contributo è l'adattamento e la valutazione controllata.

**SYNAPSE: Federated Tool Routing via Typed Compendium Artifacts**  
*Chakraborty, Shah, Gupta, 2026*

Propone artefatti federati **tipizzati**: oggetti validati da schema il cui insieme di campi dichiarato rende la privacy per campo, la fusione e il trasferimento fra architetture diverse operazioni definite invece che approssimazioni euristiche. Un unico compendio viene consumato da quattro famiglie di modelli congelati con una perdita di circa due punti.

**Rapporto con questo lavoro** — *Somiglianza:* payload testuale strutturato fra client con modelli congelati ed eterogenei, e trasferimento dello stesso artefatto a consumatori diversi. *Differenza:* il compito è il routing di strumenti, non il riconoscimento di condizioni temporali; il nostro insight non è tipizzato da schema e non porta garanzie formali. *Implicazione:* è il **precedente diretto della portabilità lato consumatore** di [§10.1](#sez-10-verifiche-di-robustezza). Che un artefatto testuale congelato sopravviva al cambio di modello non è una scoperta di questo lavoro, e va detto. Rende inoltre esplicito ciò che il nostro insight non offre: nessuna struttura a campi su cui far leva per privacy o risoluzione dei conflitti.

**Federated In-Context Learning: Iterative Refinement (Fed-ICL)**  
*Wang, Wang, Huang, Wang, Yu, Yao, Lui, Zhou, 2025*

I client conservano gli esempi, il server coordina più round di raffinamento delle risposte, nessun parametro viene trasmesso; la convergenza è dimostrata su compiti di question answering.

**Rapporto con questo lavoro** — *Somiglianza:* nessuna trasmissione di parametri, la conoscenza utile resta in forma di contesto. *Differenza:* multi-round con server aggregatore su QA, contro trasferimento a colpo singolo fra pari su evidenza temporale disgiunta per classe. *Implicazione:* è il riferimento canonico che colloca questo lavoro dentro la ICL federata. Delimita anche il contributo: il nostro protocollo è **più povero** — un round, nessuna aggregazione — e questo va dichiarato come scelta di disegno, non presentato come semplificazione neutra.

**FERA: Uncertainty-Aware Federated Reasoning**  
*Wang, Huang, Wang, Wu, Wang, Yu, McAuley, Yao, Zhou, 2026*

Framework senza addestramento in cui il server non può ispezionare i dati dei client e l'affidabilità di ciascun contributo dipende dalla richiesta; i client emettono tracce di ragionamento con stime di incertezza e il server le sintetizza pesandole.

**Rapporto con questo lavoro** — *Somiglianza:* affronta la stessa domanda della condizione E, cioè che cosa accade quando la conoscenza federata è inaffidabile. *Differenza:* FERA gestisce l'inaffidabilità pesando per incertezza; qui l'inaffidabilità è **indotta deliberatamente** dalla permutazione congelata dei pseudolabel e misurata. *Implicazione:* rende meno isolato il controllo B/E — il problema è riconosciuto in letteratura — e indica l'estensione naturale: pesare gli insight peer invece di consumarli tutti alla pari.

**Can Textual Gradient Work in Federated Learning? (FedTextGrad)**  
*Chen, Jin, Deng, Chen, Huang, Yu, Li, 2025*

Studia sistematicamente l'aggregazione testuale in federated learning: i client caricano prompt ottimizzati localmente e il server li riassume. Mostra che il riassunto di contributi eterogenei perde dettaglio e degrada le prestazioni.

**Rapporto con questo lavoro** — *Somiglianza:* il testo come oggetto aggregato in un protocollo federato. *Differenza:* là il server riassume, qui i sei insight peer arrivano al ricevente **integri e con la propria provenienza**. *Implicazione:* sostiene a posteriori la scelta di [§4](#sez-4-produzione-e-trasferimento-degli-insight) di non aggregare, e fornisce l'argomento con cui rispondere a chi chiederà perché non si riassume.

**Time-FFM: LM-Empowered Federated Foundation Model for Time Series Forecasting**  
*Liu et al., 2024*

Adatta un backbone linguistico al forecasting federato di serie temporali con moduli condivisi e teste personalizzate.

**Rapporto con questo lavoro** — *Somiglianza:* federazione, foundation model e serie temporali. *Differenza:* forecasting parametrico contro diagnosi con insight. *Implicazione:* **vieta** qualsiasi claim di «primo FL+LLM per serie temporali».

**FedSRD: Communication-Efficient Federated LLM Fine-Tuning via Sparsify-Reconstruct-Decompose**  
*Yan et al., 2026*

Yan et al., WWW 2026. DOI `10.1145/3774904.3792144`. Sparsifica gli aggiornamenti LoRA, ricostruisce e decompone per ridurre il payload nel fine-tuning federato.

**Rapporto con questo lavoro** — *Somiglianza:* affronta il costo comunicativo della federazione con modelli linguistici. *Differenza:* scambia gradienti compressi, non insight testuali. *Implicazione:* è la ragione per cui §11 misura byte e token, e insieme la ragione per cui non se ne può dedurre un vantaggio di efficienza senza confronto diretto.

</details>

<details>
<summary><strong>FL disgiunto per classe</strong> · 7 schede</summary>

**FedMD: Heterogeneous Federated Learning via Model Distillation**  
*Li & Wang, 2019*

Scambia predizioni su dati pubblici per distillare modelli eterogenei.

**Rapporto con questo lavoro** — *Somiglianza:* l'oggetto federato non sono i pesi. *Differenza:* logit e dati pubblici contro insight in linguaggio naturale. *Implicazione:* precedente della catena FedMD → FedProto → trasferimento testuale, che è la traiettoria dell'oggetto federato richiamata in §13.

**FedProto: Federated Prototype Learning across Heterogeneous Clients**  
*Tan et al., 2022*

Condivide prototipi di classe nello spazio di embedding per dati non-IID.

**Rapporto con questo lavoro** — *Somiglianza:* conoscenza compatta specifica per classe. *Differenza:* vettori appresi contro testo citabile. *Implicazione:* è l'ispirazione dichiarata della baseline numerica di §9.1, che però **non implementa** l'algoritmo originale.

**FedCKD: Knowledge Distillation with Label-Exclusive Clients**  
*Le, Le, Le, Truong-Huu, 2026*

Studia la distillazione fra client con insiemi di etichette esclusivi.

**Rapporto con questo lavoro** — *Somiglianza:* classi non locali. *Differenza:* logit e parametri su immagini contro evidenza testuale da serie temporali. *Implicazione:* il regime disgiunto per classe **non è nuovo**; è una ragione per cui il contributo va circoscritto alla combinazione.

**Federated Zero-Shot Learning with Mid-Level Semantic Knowledge Transfer**  
*Sun, Si, Wu, Gong, 2024*

Trasferisce attributi semantici intermedi per riconoscere classi visive mai viste.

**Rapporto con questo lavoro** — *Somiglianza:* semantica condivisa per classi non osservate. *Differenza:* attributi strutturati su immagini contro insight liberi da serie temporali. *Implicazione:* rende distintivo il controllo B/E, non lo zero-shot in sé.

**FedMeta-FFD: Federated Meta-Learning for Fault Diagnosis**  
*Chen, Tang, Li, 2023*

Meta-apprendimento federato per adattare la diagnosi a nuove categorie di guasto con pochi esempi.

**Rapporto con questo lavoro** — *Somiglianza:* diagnosi federata con categorie nuove. *Differenza:* few-shot parametrico contro trasferimento di conoscenza testuale. *Implicazione:* è il vicino più prossimo sull'asse della diagnosi.

**Federated Meta-Learning with Transformer Fusion for Few-Shot Multi-Condition Fault Diagnosis**  
*Zhang et al., 2026*

Zhang et al., *Knowledge-Based Systems*, 2026. DOI `10.1016/j.knosys.2026.116739`. Combina meta-learning federato e fusione di feature via transformer, testato anche su TEP.

**Rapporto con questo lavoro** — *Somiglianza:* stesso benchmark, classi distribuite. *Differenza:* scambio di rappresentazioni intermedie, non di insight linguistici. *Implicazione:* è un comparatore numerico diretto sullo stesso processo, e la sua esistenza rende più visibile la lacuna registrata in §12.2.

**Federated Learning Based on Fuzzy Fusion Rules for Chemical Production Process Fault Diagnosis**  
*Xu et al., 2026*

Xu et al., *Sensors*, 2026. DOI `10.3390/s26113545`. Applica regole di fusione fuzzy all'aggregazione federata su processi chimici, incluso il TEP.

**Rapporto con questo lavoro** — *Somiglianza:* federated learning più TEP, stessa piattaforma sperimentale. *Differenza:* aggregazione parametrica, nessun layer testuale. *Implicazione:* comparatore diretto sull'asse dell'accuratezza in contesto federato.

</details>

<details>
<summary><strong>Contesto e memoria testuale</strong> · 1 schede</summary>

**Agentic Context Engineering (ACE)**  
*Zhang, Hu, Upasani et al., Zou, Olukotun, 2026*

Tratta il contesto come un manuale che si accumula e si organizza, e nomina due modalità di fallimento della sua costruzione: il *brevity bias*, per cui il riassunto conciso scarta il dettaglio di dominio, e il *context collapse*, per cui la riscrittura iterativa erode l'informazione.

**Rapporto con questo lavoro** — *Somiglianza:* il problema di produrre testo che conservi il dettaglio utile invece di comprimerlo. *Differenza:* ACE ottimizza il contesto con un ciclo di generazione, riflessione e curazione; qui il verbalizzatore è deterministico e gli insight sono prodotti una volta e congelati. *Implicazione:* dà un nome alle due patologie che [§3](#sez-3-dalla-serie-temporale-al-testo) e [§4](#sez-4-produzione-e-trasferimento-degli-insight) devono evitare, ed è il riferimento da citare quando si giustifica perché l'interfaccia testuale è deterministica e verificabile invece che riassuntiva.

</details>

<details>
<summary><strong>TS→testo fedele</strong> · 3 schede</summary>

**Truth-Conditional Captions for Time Series Data**  
*Jhamtani & Berg-Kirkpatrick, 2021*

Compone programmi di pattern e genera una didascalia solo quando il programma ne rende vere le condizioni; i moduli restano appresi.

**Rapporto con questo lavoro** — *Somiglianza:* enfasi sulla fedeltà della descrizione. *Differenza:* didascalia neurale monovariata contro renderer deterministico multivariato. *Implicazione:* serve a definire con precisione che cosa significa «fedele per costruzione» in §3.

**CGTime: Decoupling Perception from Description in Time-Series Reasoning**  
*Feng, Xie, Zhang, Li, Ling, Li, Liu*

Propone un approccio a percezione statistica separata dalla descrizione.

**Rapporto con questo lavoro** — *Implicazione:* è il braccio `CGTIME_STATS` del confronto delle rappresentazioni di §10.4, nella versione adattata.

**S2S-FDD: Bridging Industrial Time Series and Natural Language for Explainable Zero-shot Fault Diagnosis**  
*Li & Zhao, 2025*

Li, B. & Zhao, C., *2025 CAA Symposium on Fault Detection, Supervision and Safety for Technical Processes (SAFEPROCESS)*, IEEE. DOI `10.1109/safeprocess67117.2025.11268252`; preprint arXiv `2603.08048`. Un operatore Signal-to-Semantic converte segnali di sensori multivariati in descrizioni in linguaggio naturale che catturano trend, periodicità e deviazione rispetto a una baseline normale costruita su 500 campioni; un metodo di diagnosi multi-turno ad albero interroga poi documenti di manutenzione e richiede dinamicamente altri segnali. 76,92% di accuratezza sul multiphase flow di Cranfield, **senza alcun dato di guasto**.

**Rapporto con questo lavoro** — *Somiglianza:* è la stessa catena — segnale numerico → descrizione testuale → diagnosi di una condizione mai osservata — sulle stesse tre famiglie di descrittori che usa il verbalizzatore V2. *Differenza:* è centralizzato e mono-agente, non c'è federazione né trasferimento fra pari; il banco è il multiphase flow, non il TEP; e la descrizione è generata da un LLM, non da un renderer deterministico. *Implicazione:* è il **precedente centralizzato più vicino alla catena FoT**, e delimita un claim. Impedisce di sostenere che costruire un artefatto testuale a partire da una modalità numerica per diagnosticare una classe non vista sia un problema non affrontato: lo è, fuori dal contesto federato. La rivendicazione va quindi ancorata al regime federato e al confronto controllato B/E, mai formulata «in generale».

</details>

<details>
<summary><strong>Rappresentazioni simboliche</strong> · 1 schede</summary>

**Bridging Time Series and Large Language Models via Symbolic Representation for HAR**  
*Pappa, Karvelis & Stylios, 2026*

Codifica simbolica di segnali da sensori per il consumo da parte di un modello linguistico.

**Rapporto con questo lavoro** — *Implicazione:* è il braccio `SAX_SYMBOLIC` del confronto delle rappresentazioni di §10.4.

</details>

<details>
<summary><strong>LLM per fault diagnosis</strong> · 3 schede</summary>

**Evidence-Traceable LLM Reporting for Industrial Process Fault Detection and Diagnosis (EviFDD-Agent)**  
*Chen, Peng, Zhang, Zhu, Hu, Zhai et al., 2026*

Preprint sottomesso a *Computers & Chemical Engineering*. Un *Evidence Citation Schema* lega i campi strutturati di un report diagnostico alle uscite dei tool che li hanno prodotti; tre metriche — Evidence Field Traceability, Untraceable Report Rate e un Report Actionability Score preliminare — misurano quanto il testo generato sia riconducibile a quelle uscite. Valutato sul TEP su sette configurazioni, n = 210, con intervalli di Wilson.

**Rapporto con questo lavoro** — *Somiglianza:* è l'unico lavoro del corpus che **misuri e pubblichi** la conformità di un artefatto testuale a uno schema, sullo stesso banco di prova. *Differenza:* misura la tracciabilità dei campi del **reporter** verso un evidence record già prodotto da tool deterministici; §8.9 del piano misura la validità dello schema lato **producer**, insieme a retry, troncamenti e token. Sono grandezze complementari, non equivalenti. *Implicazione:* delimita il claim di §8.10 punto 7, che non può dire «l'unica tabella del suo genere fra i lavori comparabili». Porta inoltre due indicazioni operative: i fallimenti di conformità si concentrano negli **identificatori di variabile** parafrasati (URR 77,1% nel prompt passivo, campi numerici a zero errori), e le configurazioni in cui i campi critici sono serializzati da una struttura deterministica raggiungono URR = 0. Con due modelli della stessa famiglia, il più grande risulta il meno conforme (URR 19,5% contro 1,4%) e 11,8× più lento.

**Exploring LLM-based Agentic Frameworks for Fault Diagnosis**  
*Lee, Vidyaratne, Farahat, Gupta, 2025*

Lee, X.Y., Vidyaratne, L., Farahat, A. & Gupta, C., *Annual Conference of the PHM Society* 17(1), 2025. DOI `10.36001/phmconf.2025.v17i1.4350`. ⚠️ Il titolo esatto contiene **«Agentic»**, che il nome del file omette. Confronta configurazioni di agenti LLM su dati di sensori grezzi: rappresentazione dell'ingresso (dati grezzi, statistiche descrittive, entrambe), presenza e forma dei dati di riferimento normali, architettura singolo-LLM contro multi-LLM, e apprendimento continuo da feedback.

**Rapporto con questo lavoro** — *Somiglianza:* mette a confronto **rappresentazioni** dello stesso segnale in ingresso a un LLM, che è ciò che fa §10.4, e contrappone un agente LLM a una baseline statistica, che è ciò che fa §9.1. *Differenza:* non è federato, non è sul TEP, e il compito primario è la rilevazione binaria più una classificazione a poche classi. *Implicazione:* delimita tre affermazioni. Primo, la superiorità della rappresentazione descrittiva sui dati grezzi è già pubblicata (F1 0,84 contro 0,79; accuratezza 0,73 contro 0,67): §10.4 la conferma su un altro dominio, non la scopre. Secondo, la baseline a regole ottiene F1 0,85 in rilevazione — **più di ogni configurazione LLM** — ma precision, recall e F1 pari a zero in classificazione: è il precedente pubblicato dello scenario di rischio di §9.3, e permette di riportarlo come pattern noto invece che come sconfitta. Terzo, gli LLM non migliorano con il feedback accumulato in contesto, il che sostiene §5 G4 senza chiuderne la domanda.

**FaultExplainer: Leveraging Large Language Models for Interpretable Fault Detection and Diagnosis**  
*Khan, Nahar, Chen, Constante-Flores, Li, 2025*

Khan, A., Nahar, R., Chen, H., Constante-Flores, G.E. & Li, C., *Computers & Chemical Engineering* (2025). DOI `10.1016/j.compchemeng.2025.109152`; preprint arXiv `2412.14492` (2024). La rilevazione è PCA con statistica T²; l'analisi dei contributi seleziona le sei variabili più deviate, che insieme a una descrizione testuale del TEP entrano nel prompt di GPT-4o e o1-preview, chiamati a proporre tre ipotesi di causa radice. Due condizioni: con la lista dei 15 guasti di Downs & Vogel (*Root Causes-Included Prompt*) e senza (*General Reasoning Prompt*), quest'ultima costruita per imitare un guasto mai incontrato.

**Rapporto con questo lavoro** — *Somiglianza:* è la stessa catena — poche feature deviate più una descrizione di processo → LLM congelato → ipotesi di causa per un guasto fuori dal repertorio — sullo stesso banco di prova. *Differenza:* è centralizzato e mono-agente, senza federazione né trasferimento fra pari; l'uscita è una spiegazione in prosa valutata qualitativamente guasto per guasto, non una classificazione con accuratezza e astensione misurate su una popolazione; e le feature vengono dalla PCA, non da un verbalizzatore deterministico. *Implicazione:* **delimita il claim sul guasto non visto**. Non si può sostenere che interrogare un LLM congelato sulla causa di un guasto TEP mai osservato sia un problema non affrontato: lo è, dal 2024, fuori dal contesto federato. La rivendicazione va ancorata al regime federato e al contrasto B/E, mai formulata in generale. Porta inoltre un avvertimento diretto su §8.6: quando le feature selezionate non contengono il meccanismo del guasto (casi 10 e 13), entrambi i modelli costruiscono una catena causale **plausibile e sbagliata** invece di astenersi. È la forma che prende l'«evidence quasi vuota» segnalata in S13, ed è una ragione in più per misurare l'astensione invece di darla per acquisita.


</details>

<details>
<summary><strong>Allineamento TS–linguaggio</strong> · 1 schede</summary>

**Can LLMs Understand Time Series Anomalies?**  
*Zhou & Yu, 2025*

Zhou, Z. & Yu, R. Il frontespizio riporta *Published as a conference paper at ICLR 2025*; i cataloghi registrano solo il preprint arXiv `2410.05440` (DOI `10.48550/arXiv.2410.05440`), quindi la sede non è confermata su catalogo. Studio controllato su quattro ipotesi: gli LLM capiscono le serie temporali meglio come **immagini** che come testo; **non** migliorano quando sono sollecitati a ragionare esplicitamente, e spesso peggiorano; la loro comprensione non deriva da bias di ripetizione o da abilità aritmetiche; il comportamento varia molto fra modelli.

**Rapporto con questo lavoro** — *Somiglianza:* è la domanda che sta sotto all'intera catena di §3 — che cosa un LLM sia effettivamente in grado di fare su una serie temporale. *Differenza:* presenta serie grezze o immagini, non testo verbalizzato da un renderer deterministico, e il compito è rilevazione di anomalie, non diagnosi multi-classe. *Implicazione:* sostiene indirettamente la scelta della verbalizzazione — se il numerico grezzo è un ingresso povero, tradurlo è la mossa giusta — e allo stesso tempo **impedisce di trattarla come contributo**. Delimita inoltre §8.7 e §10.2: che un budget di ragionamento più ampio migliori il risultato non è un'assunzione neutra, perché su serie temporali il ragionamento esplicito è documentato come non migliorativo. Su ingresso verbalizzato il risultato può non trasferirsi, ma l'assunzione va dichiarata e il capability pilot è il luogo dove il dato esiste già senza costo aggiuntivo.

</details>

<details>
<summary><strong>Calibrazione e predizione conforme</strong> · 6 schede</summary>

**Class-Conditional Conformal Prediction for Reliable Open-Set Fault Diagnosis in Safety-Critical Industrial Systems**  
*Heddoub et al., 2026*

Heddoub et al., *Journal of Process Control*, 2026. DOI `10.1016/j.jprocont.2026.103701`. Estende la predizione conforme al contesto open-set: diagnosticare i guasti noti e rifiutare le classi mai viste, con garanzie per classe.

**Rapporto con questo lavoro** — *Somiglianza:* il caso open-set visto dal singolo nodo assomiglia al regime disgiunto per classe; l'astensione su classi non note è il punto di contatto. *Differenza:* approccio statistico su feature, non linguistico. *Implicazione:* è il quadro di riferimento naturale per il limite registrato in §12.2 sull'astensione mai provata su guasti fuori catalogo.

**Testing for Outliers with Conformal p-values**  
*Bates, Candès, Lei, Romano, Sesia, 2023*

Bates, S., Candès, E., Lei, L., Romano, Y. & Sesia, M., *The Annals of Statistics* 51(1), 2023. DOI `10.1214/22-AOS2244`; preprint arXiv `2104.08279` (2021). P-value conformi per il rilevamento di outlier, in ottica di test multiplo. La **§1.1** fissa le ipotesi — punti **IID** e score con distribuzione continua — e la distinzione che qui conta: i p-value conformi sono indipendenti fra loro **solo condizionatamente al set di calibrazione**, mentre sono validi **solo marginalmente** su di esso. La **§3.1** enuncia il tasso di falsi positivi realizzato a soglia fissata come variabile aleatoria: FPR(α; D) ∼ Beta(ℓ, n+1−ℓ) con ℓ = ⌊(n+1)α⌋, e la garanzia marginale E[FPR] ≤ α ne è la **media**. Il risultato è attribuito a Vovk (2012), non rivendicato.

**Rapporto con questo lavoro** — *Somiglianza:* è la stessa struttura della calibrazione delle soglie di Fase B — score congelato, insieme di calibrazione, soglia realizzata, e un FAR che da quella soglia dipende. *Differenza:* il compito è test multiplo di outlier con controllo dell'FDR, non diagnosi multi-classe; nulla di federato né di linguistico. *Implicazione:* è la fonte primaria delle **tre garanzie da enunciare separatamente** — marginale, Beta condizionale alla calibrazione, proporzione a soglia congelata — ciascuna con le sue ipotesi. Vieta di scrivere «FAR garantito al 5%» per la soglia realizzata: con n = 350 e k = 334 la Beta(17, 334) dà P(FAR > 5%) = 41,68%. Impone inoltre di **dichiarare** la continuità dello score invece di darla per acquisita: nessun pareggio osservato non la dimostra.

**Conditional validity of inductive conformal predictors**  
*Vovk, 2012 / 2013*

Vovk, V., *Machine Learning* 92(2–3), 349–376, 2013. DOI `10.1007/s10994-013-5355-6`. Versione di conferenza: ACML 2012, PMLR 25:475–490 — **è questa che Bates cita** come fonte della legge Beta. In `papers/` ci sono ora **entrambe le versioni**: `…_ACML2012.pdf` sono gli atti (JMLR W&CP 25:475–490, editor Hoi e Buntine) e `…_predictors.pdf` è l'estesa su arXiv `1209.2673` del 10 agosto 2018. ✅ Confronto eseguito il 2026-09-12: **la numerazione coincide** — proposizione 2a, proposizione 2b, stesso enunciato, stessa condizione (7), stessa ipotesi IID nella §3. «Vovk (2012), proposizione 2b» è quindi citabile così com'è. La §3 lavora esplicitamente su esempi **IID** («we consider a canonical probability space in which Zᵢ … are i.i.d. random examples»). La proposizione 2a è il limite PAC ottenuto con Hoeffding; la **2b** è la versione esatta che si ferma prima di quel passaggio: Γ^ε è (E, δ)-valido se bin_{n,E}(⌊ε(n+1)−1⌋) ≤ δ, e **se e solo se** quando lo score è continuo. L'appendice A la riconduce alle regioni di tolleranza di Wilks (1941).

**Rapporto con questo lavoro** — *Somiglianza:* è il risultato che la decisione sulla calibrazione usa due volte — la legge Beta del FAR e il limite di tolleranza binomiale. *Differenza:* è teoria della predizione conforme, senza dominio industriale e senza federazione. *Implicazione:* precisa in che senso la 2b sia un'«alternativa» a DKW. Le due letture **non danno numeri diversi**: con n = 350 e k = 340, `Beta(11, 340).sf(0,05)` e `bin_{350; 0,05}(10)` valgono entrambe 3,526974%, perché sono la stessa quantità letta come coda oppure come coppia (E, δ). La conservatività in più si paga **spostando k**, non cambiando formula: k = 340 porta il FAR marginale da 4,843% a 3,134%. Secondo punto: anche la 2b poggia su **IID**, non sulla sola scambiabilità — non è una scorciatoia per evitare l'ipotesi che la Beta richiede.

**Conformal Prediction via Transported Beta Laws**  
*Ramos, Graziadei, Cabezas, 2026*

Ramos, T. R., Graziadei, H. & Cabezas, L. M. C. (Federal University of São Carlos; USP; Inria / Université Grenoble Alpes). Preprint in formato JMLR, **15 maggio 2026** (data di creazione del PDF). ⚠️ **Nessun DOI, nessun identificatore arXiv, assente da OpenAlex, Crossref e arXiv** alla verifica del 2026-09-12: i metadati non sono confermabili su fonte ufficiale e vanno riverificati prima della bibliografia. Prende la legge Beta della copertura condizionale alla calibrazione come **oggetto di riferimento a campione finito** e misura gli scostamenti da essa con distanze di Wasserstein su [0,1], separando due sorgenti distinte di comportamento non-IID: lo shift lato test agisce come mappa di trasporto sulla scala della copertura, mentre la dipendenza dentro la calibrazione cambia la legge delle statistiche d'ordine. Istanziato nei casi scale-shift, clusterizzato e stazionario mixing.

**Rapporto con questo lavoro** — *Somiglianza:* è esattamente la domanda che la calibrazione di Fase B lascia aperta — che cosa resta della Beta quando le unità di calibrazione non sono indipendenti. *Differenza:* lavoro teorico, nessun banco industriale, nessun LLM. *Implicazione:* attenua due formule e ne chiarisce una terza. Primo, il suo related work mostra un campo **attivo** — Marques F. (2025, *Statistics and Probability Letters*), Gazin (2024), la linea conformal + optimal transport — quindi «vuoto reale» e «unico lavoro del suo genere» non sono sostenibili. Secondo, e più utile: dichiara che l'ipotesi IID «can be relaxed to exchangeability» **nel senso di Marques F. (2025)**, dove la copertura *empirica* su un campione di test scambiabile converge quasi certamente a una legge Beta per de Finetti. Non è lo stesso oggetto del FAR condizionale a calibrazione fissata e test finito, che è ciò di cui parla il controesempio *U*, 1−*U*. I due enunciati convivono e vanno tenuti distinti nel testo: la scambiabilità basta per il **limite empirico**, non per la legge a campione finito.

**Universal distribution of the empirical coverage in split conformal prediction**  
*Marques F., 2025*

Marques F., P. C. (Insper, São Paulo), *Statistics & Probability Letters* 219 (2025) 110350. DOI `10.1016/j.spl.2024.110350`. Due teoremi, entrambi sotto **sola scambiabilità** dei dati e con funzione di conformità regolare (pareggi esclusi quasi certamente). **Teorema 1:** la copertura empirica di un lotto **finito** di m osservabili futuri soddisfa m·Cₘ ∼ Beta-Binomiale(⌈(1−α)(n+1)⌉, ⌊α(n+1)⌋). **Teorema 2:** per m → ∞, Cₘ converge **quasi certamente** a C∞ ∼ Beta(⌈(1−α)(n+1)⌉, ⌊α(n+1)⌋), per rappresentazione di de Finetti. Entrambe le leggi sono *universali*: dipendono solo da α e da n.

**Rapporto con questo lavoro** — *Somiglianza:* sono esattamente i due oggetti che la calibrazione di Fase B calcola — la beta-binomiale del conteggio di falsi allarmi e la Beta del FAR. *Differenza:* teoria pura, nessun banco, nessuna diagnosi. *Implicazione:* **scioglie l'apparente contraddizione** fra «serve IID» e «basta la scambiabilità», che senza questo lavoro resta un'obiezione aperta in review. La scambiabilità basta per la legge della copertura **empirica** — lotto finito, e limite quasi certo su lotto infinito. Non basta per l'oggetto diverso su cui poggia il controesempio *U*, 1−*U*: la probabilità di errore **condizionale alla calibrazione** per un singolo punto di test. Il teorema 2 chiede una successione scambiabile **infinita**, e *U*, 1−*U* è una coppia finita non estendibile: i due enunciati non si contraddicono, parlano di cose diverse. Conseguenza pratica: la beta-binomiale del registro può essere enunciata sotto scambiabilità; la frase sul FAR condizionale no. Resta intatto il problema vero, che è **la dipendenza fra le unità di calibrazione** — cinque blocchi contigui dello stesso tratto non sono né IID né dimostratamente scambiabili con il test.

**Training-conditional coverage for distribution-free predictive inference**  
*Bian & Barber, 2023*

Bian, M. & Barber, R. F., *Electronic Journal of Statistics* (2023). DOI `10.1214/23-EJS2145`; preprint arXiv `2205.03647`, 19 gennaio 2023. Ipotesi: punti di addestramento **IID**. Il loro **teorema 1 è dichiaratamente «Vovk [2012, Proposition 2a]»**, riportato per il solo split conformal. Il contributo proprio è **negativo**: per full conformal e jackknife+ la copertura condizionale all'addestramento è *impossibile* da garantire senza ipotesi aggiuntive (la stabilità algoritmica, che Liang & Barber 2025 mostrano essere sufficiente).

**Rapporto con questo lavoro** — *Somiglianza:* riguarda la stessa garanzia che la Fase B invoca, cioè che *la maggior parte* delle calibrazioni dia una soglia accettabile, non solo la media. *Differenza:* è regressione distribution-free, nessun dominio industriale. *Implicazione:* sostiene per esclusione la scelta di disegno. Lo split conformal non è la variante più debole per pigrizia: **è l'unica delle famiglie esaminate a portare con sé una garanzia condizionale all'addestramento senza ipotesi ulteriori**, e questo va scritto come argomento, non taciuto. Delimita però anche l'attribuzione: descriverlo come co-proprietario del risultato Beta insieme a Vovk è impreciso — per lo split conformal *riporta* Vovk. Se si cita la garanzia, la fonte è Vovk; Bian & Barber si citano per ciò che è **impossibile** altrove.



</details>

### 14.3 Riferimenti metodologici e di dominio

I seguenti riferimenti sostengono affermazioni presenti in questo documento e sono stati verificati su Crossref, OpenAlex, DataCite e PMLR quanto a titolo, autori, anno e sede.

| Riferimento | Che cosa sostiene, qui |
| --- | --- |
| Downs, J.J. & Vogel, E.F. (1993), *A plant-wide industrial process control problem*, Computers & Chemical Engineering 17(3). DOI `10.1016/0098-1354(93)80018-I` | La tassonomia dei meccanismi di guasto su cui si fonda la selezione di F1, F8, F10 e F13 (§2.5) |
| Bathelt, A., Ricker, N.L. & Jelali, M. (2015), *Revision of the Tennessee Eastman Process Model*, IFAC-PapersOnLine. DOI `10.1016/j.ifacol.2015.08.199` | La distinzione fra i 21 guasti standard del processo e i 28 ingressi di disturbo esposti dal simulatore modificato (§2.5) |
| Rieth, C.A., Amsel, B.D., Tran, R. & Cook, M.B. (2017), *Additional Tennessee Eastman Process Simulation Data for Anomaly Detection Evaluation*, Harvard Dataverse. DOI `10.7910/DVN/6C3JR1` | La prassi consolidata di generare realizzazioni simulate indipendenti, che è ciò che fa la replica di §8 |
| Chiang, L.H., Russell, E.L. & Braatz, R.D. (2001), *Fault Detection and Diagnosis in Industrial Systems*, Springer. DOI `10.1007/978-1-4471-0347-9` | Il contesto in cui leggere il 36/36 della baseline numerica e i riferimenti centralizzati di §9 |
| McMahan, B., Moore, E., Ramage, D., Hampson, S. & Agüera y Arcas, B. (2017), *Communication-Efficient Learning of Deep Networks from Decentralized Data*, AISTATS, PMLR 54, 1273–1282 | Il termine di paragone rispetto al quale §12.2 dichiara **non** equivalenza |
| Wang, Z., Dai, Z., Póczos, B. & Carbonell, J. (2019), *Characterizing and Avoiding Negative Transfer*, CVPR. DOI `10.1109/CVPR.2019.01155` | Il quadro in cui collocare la degradazione sui guasti già noti di §8.5 e la variante local-first di §10.3 |
| Holm, S. (1979), *A Simple Sequentially Rejective Multiple Test Procedure*, Scandinavian Journal of Statistics 6(2), 65–70 | La correzione per confronti multipli usata nel confronto delle rappresentazioni (§10.4) |
| Field, C.A. & Welsh, A.H. (2007), *Bootstrapping Clustered Data*, JRSS-B. DOI `10.1111/j.1467-9868.2007.00593.x` | Il fondamento del bootstrap appaiato per cluster descritto in §6.5 |

### 14.4 Perimetro del corpus consultato

Le ricerche sono state eseguite su OpenAlex, arXiv, Scopus e Crossref, e sono state integrate da un **audit sul testo integrale** dei venticinque lavori raccolti in [`papers/archive/fed_fsl_2026-07/`](../papers/archive/fed_fsl_2026-07).

**Prima interrogazione — resta senza risultati.** L'intersezione fra trasferimento federato di conoscenza *testuale* e serie temporali non produce precedenti: nessuno dei venticinque lavori tocca serie temporali, diagnosi di guasto o dati industriali. È la lacuna su cui poggia la formulazione prudente di [§1.4](#sez-1-obiettivo-e-domanda-scientifica).

**Le altre due interrogazioni non sono più vuote, e la dichiarazione precedente va corretta.** La specificità semantica in apprendimento in contesto è affrontata, in forma diversa dalla nostra, da ACE, che nomina *brevity bias* e *context collapse* come modalità di degradazione del contesto, e da FedTextGrad, che misura la perdita di dettaglio nell'aggregazione testuale. L'affidabilità della conoscenza condivisa fra agenti è affrontata da FERA, con pesatura per incertezza, e da SYNAPSE, con risoluzione dei conflitti per campo.

**Nessuno di questi lavori usa però un controllo ad associazione corrotta a parità di contenuto e ordine.** La condizione E di [§7](#sez-7-studio-principale) resta, nel corpus consultato, senza equivalenti: gli altri mitigano l'inaffidabilità, non la inducono per misurarne l'effetto.

Questo **delimita il corpus consultato, non prova l'assenza di precedenti**. Sostiene una formulazione prudente sulla combinazione studiata, del tipo *to the best of our knowledge* — ora su un perimetro più ampio e verificato sul testo integrale, non soltanto su interrogazioni bibliografiche.

⚠️ **Correzione del 2026-09: la prima interrogazione va riletta in modo più stretto.** «L'intersezione fra trasferimento federato di conoscenza *testuale* e serie temporali non produce precedenti» resta vera per l'intersezione a **tre** assi, ed è su quella che poggia §1.4. Non è invece vera se si toglie il federato: S2S-FDD (Li & Zhao, 2025) costruisce descrizioni in linguaggio naturale da segnali industriali multivariati e diagnostica zero-shot senza dati di guasto, e T2SP e CGTime lavorano sul verbalizzatore. La formula da usare nomina quindi tutti e tre gli assi insieme, e non la sola coppia testo + serie temporali.

**Come è stata condotta la ricerca.** Fonti: arXiv, OpenReview e gli atti NeurIPS/ICML/ICLR, ACM DL, IEEE Xplore, Springer, Elsevier/ScienceDirect, Semantic Scholar, OpenAlex, Crossref, Scopus e DBLP. Intervallo fino a settembre 2026, con enfasi sul 2020–2026. Alle interrogazioni dirette si è aggiunto il *citation chaining*: all'indietro dalle referenze di Yao et al., in avanti dai vicini verso i lavori che li citano. Le stringhe esatte sono conservate in [`docs/lit_review`](lit_review).

**Esclusioni documentate.** Sei dei venticinque lavori — FedPOB, FedPrompt, pFedPG, pFedMoAP, DP²FL, pFedRAG — sono stati esaminati e lasciati fuori perimetro: aggiornano parametri, scambiano payload numerici (prompt continui, parametri di bandit, pesi di embedding) e in gran parte lavorano su benchmark visivi. Non hanno un corrispettivo testuale con cui confrontarsi.

### 14.5 I lavori più vicini

Cinque lavori sono abbastanza vicini da poter essere scambiati per il nostro. Per ciascuno conta sapere **quale affermazione ci impedisce** e quale resta possibile.

| Lavoro | Perché è vicino | Claim che ci vieta | Claim che resta |
| --- | --- | --- | --- |
| **Federation over Text** (Yao et al., 2026) | È il metodo che applichiamo | «proponiamo FoT» — qualsiasi rivendicazione di invenzione del metodo | Prima applicazione controllata a diagnosi su serie temporali multivariate con esperienza non-IID disgiunta per classe e controllo di specificità |
| **FICAL** (2024) | Stesso oggetto federato: testo in linguaggio naturale prodotto da un LLM, dati che restano locali | «primi a federare conoscenza testuale con dati locali via LLM» | Applicazione alla diagnosi con valutazione controllata del trasferimento su classi non viste |
| **FedCKD** | Struttura non-IID a classi esclusive quasi identica alla nostra | «la struttura disgiunta per classe è la novità» | L'oggetto federato è testo interpretabile e il trasferimento avviene in contesto, non via parametri |
| **FedMeta-FFD** (IEEE TNSE 2023) | Il vicino più diretto sull'asse diagnosi: federazione più nuove categorie di guasto | «primo trasferimento cross-client verso nuove classi di guasto» | Nessun esempio etichettato della classe non vista, oggetto testuale, nessun modello aggregato |
| **Federated zero-shot con trasferimento semantico di medio livello** (2024) | Federazione più semantica più classi non viste | «primo trasferimento semantico a classi non viste in FL» | La semantica è linguaggio naturale generato da un LLM, il dominio è la diagnosi, e c'è il controllo di corruzione |

**Sintesi.** Ogni singolo asse ha un vicino stretto. Nessuno dei cinque combina serie temporali multivariate, LLM in contesto, scambio testuale, classi localmente non viste, assenza di scambio di dati grezzi e controllo di specificità. La novità vive **nell'intersezione e nel disegno di valutazione**, non nei componenti.

> **Un sesto vicino, individuato dopo.** Questa analisi precede l'esame del corpus federato di §14.1. **SYNAPSE** va aggiunto come vicino sull'asse che qui non compare: la portabilità dello stesso artefatto testuale fra famiglie di modelli diverse. Vieta di presentare la portabilità cross-model di [§10.1](#sez-10-verifiche-di-robustezza) come capacità inedita; lascia possibile presentarla come conferma lato consumatore su evidenza temporale.

> **Un settimo vicino, aggiunto nel 2026-09.** **S2S-FDD** (Li & Zhao, 2025) è vicino sull'asse che gli altri sei non toccano: la catena segnale numerico → descrizione testuale → diagnosi di una condizione mai osservata, su un processo industriale reale. *Claim che ci vieta:* qualunque formulazione per cui tradurre una modalità numerica in testo diagnostico per riconoscere una classe non vista sarebbe un problema aperto. *Claim che resta:* la stessa catena in regime **federato**, con esperienza disgiunta per classe fra pari, controllo di specificità B/E e misura della degradazione sulle classi già note — nessuna delle quali compare in S2S-FDD, che è centralizzato, mono-agente e senza controllo a informazione corrotta.

> **Un ottavo vicino, aggiunto il 2026-09-11.** **FaultExplainer** (Khan, Nahar, Chen, Constante-Flores & Li, 2025) è vicino sull'asse più scomodo: interroga un LLM congelato sulla **causa di un guasto TEP non presente nel repertorio fornito**, sul nostro stesso banco di prova. *Claim che ci vieta:* qualunque formulazione per cui chiedere a un LLM di ragionare sulla causa di un guasto mai visto sul TEP sarebbe un problema aperto o inedito. *Claim che resta:* il regime federato, il trasferimento di insight fra pari con esperienza disgiunta per classe, il controllo B/E e la misura dell'astensione su una popolazione — FaultExplainer è centralizzato, mono-agente, con feature scelte dalla PCA, e valuta la spiegazione in prosa guasto per guasto invece di misurare accuratezza e astensione.

### 14.6 Tenuta della novità

**Tentativo di falsificazione.** La ricerca è stata condotta *contro* la nostra tesi, cercando un lavoro che combinasse tutti gli assi insieme. A criteri pieni non ne è emerso alcuno. Rilassando i criteri uno alla volta compaiono i vicini, e mostrano dove la nostra posizione è fragile:

- togliendo *serie temporali* → FoT e FICAL, equivalenti sul paradigma ma non sul dominio;
- togliendo *LLM e testo* → FedCKD e il trasferimento semantico zero-shot, equivalenti sulla struttura non-IID e sull'idea di classi non viste, ma non sull'oggetto testuale;
- togliendo *classi non viste* → Time-FFM, che è federazione parametrica su serie temporali;
- tenendo *serie temporali, diagnosi e LLM* ma togliendo la federazione → la famiglia FD-LLM, centralizzata, e **FaultExplainer**, che è centralizzato ma gira **sul TEP stesso**.

**La novità non è a livello di componente.** È una novità di combinazione, dominio e disegno di valutazione:

| Livello | Tenuta |
| --- | --- |
| Componente — verbalizzazione, insight testuali, federazione non parametrica, classi disgiunte | **Bassa.** Tutti noti singolarmente |
| Combinazione — l'unione di testo-LLM, serie temporali multivariate, classi disgiunte, non viste, nessun dato grezzo | **Moderata.** Il livello più difendibile |
| Valutazione — A/B/E con permutazione pre-registrata, freeze, held-out, pseudolabel opachi | **Moderata/alta.** Il pezzo migliore: il controllo B−E, cioè specificità semantica a parità di testo, è raro in questo filone |
| Dominio — prima applicazione documentata di un approccio FoT-like alla diagnosi su TEP | **Moderata, rivista al ribasso nel 2026-09.** Reale ma applicativa, e non più isolata: S2S-FDD porta la catena segnale→testo→diagnosi zero-shot su un processo industriale, sebbene centralizzata e su un altro banco; e FaultExplainer (Khan et al., 2025) porta un LLM congelato sulla causa di un guasto non visto **sul TEP stesso**, pur restando centralizzato e limitato alla spiegazione |
| Metodologia — la catena evidenza deterministica → ragionamento locale → trasferimento testuale | **Bassa/moderata.** Composizione di tecniche note, resa rigorosa |

La raccomandazione che ne segue è puntare il paper su **combinazione e valutazione**, non su componente e metodologia. La formula sicura, da usare così com'è:

> *To the best of our knowledge, we did not identify a prior method that federates locally-derived textual knowledge across agents with class-disjoint temporal experience to recognize locally unseen fault conditions, under a preregistered semantic-specificity control.*

Mai *no such method exists*.

### 14.7 Priorità bibliografica

Quindici riferimenti sono obbligatori. Non perché siano i più citati, ma perché ciascuno **delimita** qualcosa che non possiamo rivendicare.

| Riferimento | Che cosa delimita |
| --- | --- |
| Yao et al., *Federation over Text*, arXiv:2604.16778 | Il metodo che applichiamo: attribuzione obbligatoria |
| McMahan et al., *FedAvg*, AISTATS 2017 | La radice del FL, e il contrasto «noi non aggreghiamo parametri» |
| Li & Wang, *FedMD*, NeurIPS 2019 WS | Sposta l'oggetto federato ai logit |
| Lin et al., *Ensemble Distillation (FedDF)*, NeurIPS 2020 | Distillazione federata lato server |
| Tan et al., *FedProto*, AAAI 2022 | Prototipi invece di gradienti: l'analogo numerico dell'insight per classe |
| Zhu, Hong, Zhou, *FedGen*, ICML 2021 | Federazione di conoscenza sintetica |
| *Federated In-Context LLM Agent Learning*, arXiv:2412.08054 | Il vicino più pericoloso: federazione testuale con dati locali |
| Mohtashami et al., *Social Learning*, arXiv:2312.11441 | Il ponte fra distillazione e linguaggio naturale |
| Liu et al., *Time-FFM*, NeurIPS 2024 | FL più foundation model più serie temporali: vieta il primato su «FL+LLM per TS» |
| Li et al., *FedCoT*, arXiv:2508.10020 | Ragionamento federato parametrico |
| Kim et al., *T2SP*, arXiv:2606.12481 | Rappresentazione deterministica TS→LLM già attiva: blocca ogni novità sul verbalizzatore |
| Jhamtani & Berg-Kirkpatrick, *TRUCE*, EMNLP 2021 | Testo fattuale su serie temporali |
| Li et al., *Non-IID Data Silos*, ICDE 2022 | La tassonomia label-subset skew, cioè il nome esatto del nostro regime |
| Zhu et al., *FL on Non-IID Data*, Neurocomputing 2021 | L'inquadramento non-IID |
| He et al., *FedGKT*, NeurIPS 2020 | Trasferimento di conoscenza edge-server |

A questi si aggiungono i lavori del corpus federato di §14.1 che incidono sul disegno: SYNAPSE, Fed-ICL, FedTextGrad, FERA e ACE, con il ruolo descritto nelle schede di §14.2.

Dal 2026-09-12 se ne aggiungono altri due, su un asse diverso — quello di **ciò che si può affermare sul FAR della soglia calibrata**: **Bates et al. (2023)** per la distinzione fra garanzia marginale e legge Beta condizionale alla calibrazione, e **Vovk (2012/2013)** perché ne è la fonte e fornisce il limite di tolleranza binomiale esatto. **Ramos et al. (2026)** va citato solo se il testo afferma qualcosa sulla Beta sotto dipendenza, e finché i suoi metadati non sono confermati va trattato come preprint non verificato.

---

## 15 · Provenienza e riproducibilità

### 15.1 Che cosa è verificabile e che cosa no

**È verificabile** il ricalcolo scientifico a partire dalle predizioni congelate: metriche, contrasti, intervalli e confronti si ottengono dai record esistenti senza nuove chiamate al modello.

**Non è riproducibile bit per bit** la rigenerazione delle simulazioni del processo: lo stato del generatore casuale non è stato registrato. Questo riguarda la generazione dei dati, non il calcolo dei risultati.

### 15.2 Dove si trova ogni cosa

| Sezione | Artefatti |
| --- | --- |
| §3 pipeline, soglie, congelamento | [`code/`](../code), [`reproducibility/`](../reproducibility), [`tep_validation_v2/`](../tep_validation_v2), [`tep_test_v2/`](../tep_test_v2) |
| §4 insight | [`phase_b/insights/`](../phase_b/insights) e [`final_local_insights.json`](../phase_b/insights/final_local_insights.json) |
| §7 studio principale | [`phase_b/final_evaluation/`](../phase_b/final_evaluation), [`primary_metrics.csv`](../phase_b/final_evaluation/primary_metrics.csv), [`evaluation_results.json`](../phase_b/final_evaluation/evaluation_results.json) |
| §7 controllo A+ | [`APLUS_EVALUATION_REPORT.md`](../phase_b/final_evaluation_aplus/APLUS_EVALUATION_REPORT.md), [`aplus_primary_metrics.csv`](../phase_b/final_evaluation_aplus/aplus_primary_metrics.csv), [`APLUS_FREEZE_MANIFEST.json`](../phase_b/final_evaluation_aplus/APLUS_FREEZE_MANIFEST.json) |
| §8 replica | oggetti Git dei tag `exp3-v2-inference-frozen-001` e `exp3-v2-results-frozen-001` — vedi §15.3 |
| §9.1 baseline numerica | [`C02B_BASELINE_REPORT.md`](../phase_b/baselines/c02b_shared_numeric_prototypes/results/C02B_BASELINE_REPORT.md) |
| §9.2 riferimenti ML centralizzati | [`SUPERVISOR_MODEL_SUITE_REPORT.md`](../phase_b/baselines/c02b_supervisor_model_suite/results/SUPERVISOR_MODEL_SUITE_REPORT.md) |
| §9.3 riferimento testuale centralizzato | [`evaluation_results_c.json`](../icl/full_evaluation/evaluation_results_c.json), [`PLAN_CENTRAL_POOLED_ICL.md`](../icl/PLAN_CENTRAL_POOLED_ICL.md), [`CONDITION_C_R10_INDEPENDENT_REVIEW.md`](audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md) |
| §10.1 verifica con altro LLM | [`phase_b/exp2/qwen/`](../phase_b/exp2/qwen), [`EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW_R2.md`](audits/EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW_R2.md) |
| §10.3 variante local-first | [`FULL_TEST_REPORT.md`](../phase_b/c06/full_test/inference/FULL_TEST_REPORT.md), [`full_test_results.json`](../phase_b/c06/full_test/inference/full_test_results.json) |
| §10.4 confronto delle rappresentazioni | [`ablation_evaluation.json`](../ablation/ablation_results/ablation_evaluation.json), [`token_summary.json`](../ablation/ablation_results/token_summary.json), [`ablation_report.md`](../ablation/ablation_results/ablation_report.md) |
| §11 costo della comunicazione | [`COMMUNICATION_PAYLOAD_CHARACTERIZATION.md`](../analysis/communication_characterization/COMMUNICATION_PAYLOAD_CHARACTERIZATION.md), [`communication_payload_metrics.csv`](../analysis/communication_characterization/communication_payload_metrics.csv) |

### 15.3 Artefatti disponibili nei tag Git

Gli artefatti della **replica su nuovi run** non sono presenti nel working tree: la cartella corrispondente contiene solo file temporanei. Restano però **congelati e indirizzabili negli oggetti Git**, sotto i tag `exp3-v2-inference-frozen-001` e `exp3-v2-results-frozen-001`. Tutti i valori riportati in §8 sono stati letti da lì e sono verificabili.

Lo stesso vale per gli artefatti dell'**approfondimento sui casi al limite** a 4 096 token, leggibili dai commit del ramo dedicato alla sensibilità del budget di ragionamento.

Questi non sono dati mancanti: sono dati fuori dal working tree.

### 15.4 Artefatti effettivamente mancanti

Un solo elemento rientra in questa categoria. I record grezzi del **sweep del budget di ragionamento** a 1 024, 1 536, 2 048 e 3 072 token — quelli da cui deriva la tabella di §10.2 — non esistono né nel working tree né in alcun commit del repository. Sono referenziati per hash dalla configurazione dell'approfondimento a 4 096, ma il file corrispondente non è presente.

Di conseguenza: l'approfondimento a 4 096 è verificabile su artefatto; la tabella del sweep è verificabile solo sulla documentazione. Chi volesse riprodurla dovrebbe rieseguire l'analisi.

### 15.5 Disallineamento dell'indice del repository

I file di orientamento alla radice del repository — l'indice della documentazione e la guida di audit — non indicizzano il controllo A+, la variante local-first e le baseline numeriche, tutti successivi alla loro ultima revisione. Chi partisse da lì per una verifica indipendente non li troverebbe. Il riallineamento di quei file è fuori dal perimetro di questo documento, che non li modifica.

### 15.6 Perimetro di questo documento

Questo documento e le sue versioni HTML sono materiale editoriale nuovo. Non modificano né sostituiscono la documentazione precedente, il blueprint del paper, i paper o gli artefatti sperimentali, che restano intatti.
