# Decisione: calibrazione delle soglie in Fase B

**Data**: 2026-09-11 · **Revisione**: 16 (regola di selezione A/A′ adottata e congelata il 2026-09-12) · **Stato**: disegno statistico **chiuso e concordato** (C0–C4 approvate, P0 risolto con la Via B, C5 separata e non attivata).
**Non congelabile operativamente** finché mancano tre prerequisiti bloccanti: (i) durata del burn-in e criterio verificabile per dichiararlo concluso — riguarda il transitorio e l'interpretazione a regime, **non** produce indipendenza fra run; (ii) implementazione e validazione dello schema dei flussi pseudocasuali (scelta teorica compiuta: Philox4×32-10; restano implementazione, compilazione, verifica con vettori noti, misura runtime e validazione contro il legacy); (iii) `Ts_base` fissato, documentato e registrato nel manifest, con lo stesso valore per `cal_thr` e `far_ver`.

Flussi separati e procedura identica **sostengono in sede di progetto** l'assunzione IID su cui poggiano la Beta e la binomiale esatta, senza dimostrarla. La ricostruzione del `Ts_base` **storico** di N1–N5 è invece una questione di riproducibilità e confrontabilità, e non è da sola condizione necessaria della garanzia conformal del nuovo esperimento.
> **Nota terminologica (2026-09-11).** In tutto il documento il criterio decisivo per la validità conformal è la **scambiabilità**, non l'indipendenza. La dipendenza può esserne un indizio, non è il criterio matematico.
>
> Restano corrette le occorrenze in cui la dipendenza è invocata per ciò che fa davvero, cioè gonfiare l'errore standard di una stima: la verifica del FAR, dove l'errore standard si ottiene con un bootstrap a livello di run.
>
> Non è invece mai corretto trattare una soglia più severa come rimedio alla dipendenza: se la distribuzione di riferimento non vale, la direzione dell'errore non è garantita e abbassare il livello nasconde il problema anziché correggerlo. È la ragione per cui il test binomiale pilota è stato ritirato (vedi *Controllo preliminare sui 10 run pilota*).

**Base**: 22 paper letti integralmente (`threshold_calibration_search_2000_2026.md`) + `code/tep_analysis_v2/threshold_calibration_report.md` + `code/calibrate_thresholds_v2.py`

## Correzioni rispetto alla revisione 1

Quattro errori della revisione 1, tutti confermati sul repository:

1. Il massimo è calcolato sulle **41 XMEAS**, non su 52. (`tep_features.XMEAS`, len = 41; il report originale lo dice: *"Ogni score è il massimo sulle 41 XMEAS"*.)
2. I **500 run Normal non esistono nel repository**. `tennessee-eastman-dataset/simulations/mode_1/faults` è vuota e il simulatore è Simulink (`MultiLoop_mode1.mdl`). La Fase A ha usato un singolo tratto Normal continuo di 250 h a campionamento 1 min (15.000 campioni, N1–N5). I run vanno procurati o generati: è un prerequisito con un costo, non un dato disponibile. Vedi **P0**.
3. Il leave-one-block-out **non può restare identico**. Va separato l'insieme che costruisce la baseline da quello che calibra la soglia. Vedi **C0**.
4. Non si può dire che in Fase A la garanzia fosse "esatta". Il report originale lo nega già, per due motivi indipendenti. Vedi sotto.

## Punto di partenza reale (Fase A, già eseguita)

`code/calibrate_thresholds_v2.py`: 50 finestre non sovrapposte da 5 h (10 per blocco × 5 blocchi da 50 h dello stesso tratto Normal), baseline leave-one-block-out, massimo sulle 41 XMEAS, quattro soglie indipendenti a α = 0.05 con rango `ceil((n+1)(1−α))` = 49.

Il report originale documenta già tre limiti che la revisione 1 aveva appiattito:

- *"La funzione di score non è la stessa in calibrazione e in applicazione."* I 50 punteggi di calibrazione usano una baseline costruita sugli **altri quattro** blocchi; fault, validazione e test usano una baseline costruita su **tutti e cinque**. Il report conclude da sé: *"non converte automaticamente la procedura in cross-conformal con garanzia ... È una ragione ulteriore, indipendente dalla dipendenza temporale, per attenersi alla formula conformal-style upper order statistic e non rivendicare una copertura marginale."*
- *"Le finestre Normal adiacenti dello stesso blocco non sono indipendenti; la garanzia conformal exchangeability è quindi approssimata, non dimostrata."* — **citazione verbatim del report congelato, da riformulare quando viene ripresa altrove.** Il criterio matematico decisivo non è l'indipendenza: il conformal richiede **scambiabilità**, e dati dipendenti ma scambiabili sarebbero ammissibili. Ciò che manca qui è la dimostrazione della scambiabilità. La dipendenza fra finestre adiacenti è un indizio del problema, non il problema.
- *"La calibrazione è per-feature e corregge la simultaneità tra 41 sensori, ma non la simultaneità tra le quattro feature."* Il FPR diagnostico in-sample è 2.0% per feature e **6.0% sull'unione** (3/50), contro un α dichiarato del 5% per feature.

**Conseguenza sul piano statistico.** La Fase A non è uno split conformal, e **basta il primo dei due motivi**: la funzione di score cambia fra i due lati. Questo invalida la costruzione da solo, senza alcuna considerazione sulla struttura dei dati. Il secondo motivo è distinto e più debole — la scambiabilità degli score **non è stabilita** — e non va enunciato come "gli score non sono scambiabili", che asserirebbe più di quanto sia dimostrato. Quindi la distribuzione Beta del FAR condizionale **non descrive la Fase A**: descrive il caso migliore a cui la Fase B può aspirare. Questa è la differenza sostanziale fra le due fasi, più della numerosità.

| | Fase A (eseguita) | Fase B (proposta) | RBC-AD 2026 |
|---|---|---|---|
| Unità di calibrazione | finestra | **run** | finestra |
| n usato per la soglia | 50 | **350** (non 500: vedi P0) | 3.075 |
| Unità indipendenti | 5 blocchi di 1 tratto | 350 run | 75 run |
| Sovrapposizione finestre | no | no | 90% (W=100, stride 10) |
| Score identico su entrambi i lati | **no** (baseline 4 vs 5 blocchi) | **sì** (C0) | sì |
| Split conformal valido | no | sì | struttura split-conformal; garanzia non stabilita |
| FAR condizionale | **distribuzione ignota** | Beta(17, 334) sullo **score combinato unico** (C3), **esatta sotto ipotesi di continuità di `S`** | non applicabile (scambiabilità non stabilita) |
| media / sd | — | 4.84% / 1.14% | — |
| intervallo 90% | — | [3.12%, 6.86%] | — |
| pavimento 1/(n+1) | 1.96% | 0.28% | — |

A titolo di riferimento, sotto split conformal con score scambiabili n = 50 e α = 0.05 darebbero Beta(2, 49), media 3.92%, intervallo 90% [0.7%, 9.1%]. Va presentato come ciò che n = 50 permetterebbe **nel caso migliore**, non come stima della Fase A.

## P0 — Generazione dei run Normal: risolto

**Via scelta: B, generazione con il simulatore Simulink** (`tennessee-eastman-dataset/simulator`), a campionamento 1 minuto.

Motivo: conserva le quattro feature congelate, i dati precedenti e il confronto con la Fase A. Con il dataset esteso di Rieth a 3 minuti bisognerebbe portare a 3 minuti anche fault, few-shot e test, altrimenti si calibrerebbe e si testerebbe a frequenze diverse.

### Allocazione dei run

500 run complessivi più 10 pilota, **non** 500 per la calibrazione. La baseline riusa N1–N5, già disponibile.

| Insieme | Fonte | Numero | Lunghezza per run | Uso |
|---|---|---|---|---|
| `pilot` | nuovi run | **10** | burn-in + 50 h | solo controllo preliminare; **esclusi da tutto il resto** |
| `baseline_fit` | N1–N5 esistenti | 250 h continue | — | normalizzazione dello score, congelata |
| `cal_thr` | nuovi run | **350** | burn-in + 5·J, J ~ Unif{1..10} | **una** finestra per run → la soglia |
| `far_ver` | nuovi run | **150** | burn-in + 50 h | verifica del FAR |

### La posizione temporale della finestra va campionata, non fissata

La revisione 3 proponeva run di calibrazione corti, con la finestra sempre immediatamente dopo il burn-in. **È sbagliato**: la verifica usa anche finestre molto successive, e la distribuzione dello score alla posizione 1 non è necessariamente quella alla posizione 10. Se le due distribuzioni differiscono, calibrazione e verifica non sono scambiabili e la garanzia non si trasferisce.

La posizione va quindi campionata nella calibrazione **con la stessa distribuzione che ha nella verifica**. Con J = 10 finestre utili per run di verifica, la posizione marginale in verifica è uniforme su {1,…,10}, quindi:

- *Forma diretta*: generare i run di calibrazione a lunghezza piena (burn-in + 50 h) e campionare una finestra uniformemente fra le dieci. È il dispositivo di Kaur et al. 2024 / CODiT.
- *Forma economica, equivalente in distribuzione*: estrarre J ~ Unif{1,…,10} per ciascun run di calibrazione, simulare burn-in + 5·J ore e prendere l'**ultima** finestra. Lo stato del processo al tempo burn-in + 5·J non dipende dall'intenzione di continuare la simulazione, quindi la coppia (posizione, score) ha la stessa distribuzione congiunta della forma diretta, a lunghezza media burn-in + 27.5 h invece di burn-in + 50 h.

Con burn-in di 20 h: forma diretta 35.000 h simulate in totale, forma economica 27.125 h, cioè il 22% in meno. Il risparmio della revisione 3 era del 60% ma comprava finestre non scambiabili, quindi non valeva nulla.

### Verifica del FAR: una metrica primaria e una secondaria

- **Primaria, allineata alla garanzia**: una finestra per run di `far_ver`, a posizione uniforme su {1,…,10}. Dà 150 osservazioni, quindi un intervallo binomiale **esatto sotto run indipendenti e identicamente distribuiti**: non è senza assunzioni, ma le due assunzioni riguardano la procedura di generazione, non i dati. **Semi distinti non bastano**: servono **flussi separati**, uno per run. La scelta è compiuta (Philox4×32-10) e restano implementazione, verifica con vettori noti e validazione contro il legacy. Anche a schema realizzato, flussi separati e procedura identica sostengono l'assunzione IID in sede di progetto senza dimostrarla: resta un requisito di progetto dichiarato, non un fatto acquisito. L'identica distribuzione viene invece dall'usare la stessa procedura per `cal_thr` e `far_ver`. *Precisione attesa prima dell'esperimento*, non un intervallo già determinato: con FAR vero 4.84% il conteggio dei superamenti cadrà fra 3 e 12 con probabilità **0.947**, non 0.90: è l'intervallo centrale nominale al 90% allargato dalla discrezione della binomiale (l'intervallo 4–12 copre **0.9046**), e la semiampiezza dell'intervallo di Clopper–Pearson varierà di conseguenza fra **2.7 e 4.7 pt**. L'esito modale è 7 superamenti (P = 0.152), che darebbe [1.90%, 9.38%] e semiampiezza 3.74 pt: è un esempio atteso, non una previsione.
- **Secondaria, operativa**: tutte le 1.500 finestre di `far_ver`. Precisazione necessaria: **non** è vero che ogni posizione abbia la stessa distribuzione di una finestra di calibrazione; è la **miscela uniforme delle dieci posizioni** a coincidere con la distribuzione di calibrazione. La media su tutte le finestre stima quindi il FAR della miscela, che è esattamente la quantità coperta dalla garanzia, mentre i FAR per singola posizione possono differire fra loro. La dipendenza intra-run gonfia soltanto l'errore standard, che si ottiene con un bootstrap a livello di run. È il numero che interessa in esercizio, non quello che verifica la garanzia.
- **Diagnostica da riportare insieme**: il FAR disaggregato per posizione 1,…,10. Un FAR sistematicamente più alto alla posizione 1 **suggerisce** un burn-in insufficiente, ma non lo dimostra da solo: spiegazioni alternative sono un transitorio residuo dal cambio di condizione iniziale, il comportamento delle feature di pendenza al bordo dello stream, o una baseline che non copre il regime di inizio run. Alla diagnostica segue quindi una verifica mirata, allungando il burn-in su un sottoinsieme di run e ricontrollando la posizione 1, non una conclusione immediata. Non costa nulla perché i dati ci sono già.

**Limite da dichiarare, e non mitigabile entro questo budget.** La semiampiezza attesa della verifica primaria (2.7–4.7 pt secondo il conteggio osservato) è dell'ordine del doppio di quella dell'intervallo Beta predetto sotto continuità (1.87 pt): con 150 run si può constatare che il FAR è nell'ordine di grandezza giusto, non verificare la Beta in modo stretto. È una proprietà del budget, non del disegno. E il rimedio non è allungare i run: **allungare i run aiuta solo la metrica secondaria, e solo se la correlazione intra-run è bassa; se è alta servono più run indipendenti**, che è l'unica leva sulla metrica primaria.

### Controllo preliminare sui 10 run pilota: guardia descrittiva, non test

I 10 run pilota sono generati per primi, con la stessa procedura, e **sono esclusi da `cal_thr`, da `far_ver` e dalla baseline**: non rientrano in nessun altro uso, qualunque sia l'esito.

**Il test binomiale proposto nella revisione 4 non è valido e viene ritirato.** Le 100 finestre pilota provengono da 10 run e sono dipendenti entro run; abbassare il livello dall'5% all'1% non corregge la dipendenza, la nasconde. In più la soglia provvisoria sarebbe ricavata dalle stesse finestre di `baseline_fit` che definiscono la normalizzazione dello score, quindi il tasso di superamento su baseline è ≈ 5% per costruzione e il confronto confonde due cose. Con 10 run indipendenti, una finestra per run, non esiste potenza per testare un tasso del 5%: servirebbero ordini di grandezza in più.

**Riformulazione, e perché è sufficiente.** Questo controllo non protegge la validità. Se i nuovi run si discostano da N1–N5, lo scostamento si applica **identico** a `cal_thr` e a `far_ver`, quindi la costruzione split-conformal resta valida e si perde soltanto potenza di rilevazione. La guardia serve a sapere in anticipo se la potenza sarà cattiva, non a giustificare un'inferenza: non ha quindi bisogno di validità inferenziale.

Si presenta perciò come **controllo descrittivo con una regola di decisione basata sull'ampiezza dell'effetto, pre-registrata e dichiaratamente non inferenziale**:

- Si riportano, per lo score combinato `S`, mediana e MAD sulle 100 finestre pilota e sulle 50 finestre di `baseline_fit`, più i due istogrammi sovrapposti e il KS a due campioni come descrittiva.
- **Regola di ricostruzione della baseline**: si ricostruisce se `|mediana(S_pilot) − mediana(S_baseline)| > 0.5 · MAD(S_baseline)`, oppure se `MAD(S_pilot) / MAD(S_baseline)` esce dall'intervallo [0.5, 2.0].
- Nessun p-value è usato come trigger. La regola è una soglia di magnitudine fissata prima di guardare i dati, e il suo unico scopo è evitare di calibrare su una baseline che descrive un regime diverso da quello dei run nuovi.

*Destino dello split se la baseline va ricostruita,* deciso ora per non scegliere dopo aver visto i dati: si generano **100 run aggiuntivi** per `baseline_fit_new`, **di lunghezza burn-in + 50 h come `far_ver`**, usandone **tutte** le finestre. Tre ragioni per questa lunghezza: la normalizzazione richiede molti valori per-variabile in coda (100 run × 10 finestre × 41 XMEAS = 41.000 valori per feature, contro i 2.050 di N1–N5); le dieci posizioni risultano uniformemente rappresentate, quindi la baseline è bilanciata per posizione come la calibrazione e la verifica; e il burn-in si ammortizza su dieci finestre invece di una. `cal_thr` scende a **300** e `far_ver` resta a 150. Conseguenza sul risultato principale: Beta(15, 286), livello dichiarabile 4.98%, IC90 [3.11%, 7.20%], semiampiezza 2.05 pt invece di 1.87. Totale 560 run invece di 510.

### Requisiti sulla generazione

- `cal_thr` e `far_ver` devono provenire dalla **stessa procedura di generazione**: stessa distribuzione dello stato iniziale, stessa politica di burn-in, stessa famiglia di semi, con i soli semi a variare. È questo che rende i due insiemi scambiabili fra loro, ed è la condizione su cui poggia tutto.
- La baseline da N1–N5 non deve essere scambiabile con nulla: per la validità basta che sia **congelata e disgiunta** dai run di calibrazione e verifica. Se i nuovi run differiscono sistematicamente da N1–N5, lo scostamento si applica identico a calibrazione e verifica, quindi una differenza limitata alla baseline storica non invalida la calibrazione su nuovi run omogenei. Può però alterare **sensibilità e confrontabilità**, e la guardia mediana/MAD **non garantisce di intercettarla**, in particolare se cambiano le code o le correlazioni temporali: quella guardia confronta posizione e scala, non forma della coda né struttura temporale.
- **Ambiguità storica su `Ts_base`, da ricostruire.** Gli artefatti mostrano `0.0005` in una riga **commentata** di `Mode_1_Init.m` e `5/1000` come assegnazione in un altro script di lancio, un fattore 10 di differenza. Questo documenta un'ambiguità fra artefatti; **non** dimostra che N1–N5 siano stati generati con uno dei due valori. Il parametro storico resta da ricostruire, ed è una lacuna di riproducibilità della Fase A indipendente dalla Fase B: le quattro soglie in `verbalizer_config_v2.json` sono state calibrate su N1–N5 a un `Ts_base` non documentato.
- **Controllo preliminare, prima di calibrare**: confrontare la distribuzione dei quattro score su una decina di nuovi run con quella degli score su N1–N5. Se è spostata in modo marcato, le feature stanno misurando la procedura di generazione e non il processo, e in quel caso la baseline va ricostruita dai nuovi run invece di riusare N1–N5.
- Burn-in da documentare e da scartare esplicitamente, con il criterio usato per dichiarare raggiunto il regime stazionario.
- **`Ts_base` fissato, documentato e registrato nel manifest: requisito bloccante.** `Ts_base` è il periodo di campionamento dei controllori PI discreti, quindi governa la dinamica ad anello chiuso e non solo la risoluzione in uscita, anche con `ode45`. `cal_thr` e `far_ver` devono usare **lo stesso** valore: valori diversi farebbero venir meno la giustificazione progettuale della scambiabilità fra i due insiemi, non sarebbero una questione di sola potenza.
- I batch di validazione e test sigillati non vengono aperti: la verifica del FAR usa run normali nuovi.

## Le modifiche approvate

**C0 — Separare i dati che costruiscono la baseline da quelli che calibrano la soglia.** Split a livello di run in quattro insiemi disgiunti, sul modello di RBC-AD (`train_fit` 325 / `val_fit` 50 / `cal_thr` 75 / `cal_lam` 50): un insieme `baseline_fit` per le statistiche di riferimento, `cal_thr` per la soglia, un insieme per eventuali scelte di iperparametro, e validazione/test mai aperti. La funzione di score si congela su `baseline_fit` e si applica **identica** alla calibrazione, alla validazione e al test.
*Motivazione*: lo richiede la costruzione split-conformal, e lo chiede già il report della Fase A quando spiega perché non rivendica copertura marginale.
*Guadagno*: è questa modifica, non la numerosità, che rende la Fase B uno split conformal legittimo. Senza C0 le altre quattro non producono una garanzia.

**C1 — L'unità di calibrazione diventa il run.** Una finestra per run normale, scelta uniformemente fra quelle del run.
*Motivazione*: Kaur, Yang, Sokolsky, Lee (ACM TCPS 2024) e CODiT (ICCPS 2023) ottengono l'IID campionando **una finestra per traccia**; l'equivarianza temporale dà potenza, il disegno di campionamento dà validità.
*Guadagno*: la scambiabilità diventa una proprietà del disegno. Rispetto a RBC-AD, che ha n nominale sei volte maggiore ma finestre sovrapposte al 90% e ammette *"exchangeability is not enforced"*, il nostro Beta sarebbe applicabile ai nostri dati.

**C2 — Dichiarare il livello effettivamente attingibile.** A n = 50 i FAR attesi possibili sono l/51 (1.96%, 3.92%, 5.88%, …): α = 0.05 non è raggiungibile e il rango 49 calibra di fatto a 3.92%. A n_cal = 350 il passo della griglia è 1/351 = 0.28 punti e il livello dichiarabile è **4.84%** (l = 17, k = 334).
*Guadagno*: elimina un'imprecisione formale verificabile in due righe da un revisore.

**C3 — Un unico score combinato, congelato prima della conformalizzazione.** La revisione 3 proponeva di conformalizzare i quattro score separatamente sugli stessi 350 run e poi combinare i quattro p-value. **Non è compatibile con Beta(17, 334)**: quella distribuzione descrive il quantile di *un solo* score calibrato su 350 punteggi scambiabili, mentre quattro statistiche d'ordine dipendenti combinate a posteriori danno un FAR condizionale che non segue quella legge, ed è conservativo in modo non quantificato se la combinazione è di tipo Bonferroni.

Ordine corretto: **prima costruire e congelare un unico score combinato, poi applicarlo ai 350 run, poi calibrarne il quantile con la formula del rango.**

Costruzione dello score combinato, interamente su `baseline_fit` e poi congelata:

0. **Le quattro quantità per-variabile sono tutte a una coda e non negative, e vanno prese in valore assoluto dove il segno esiste**: `|shift_sigma|` e `|slope_sigma_h|` (cioè `abs_shift_sigma` e `abs_slope_sigma_h`, coerentemente con `tep_verbalize_v2.py`, che confronta `np.abs(shifts)` e `np.abs(slopes)`), mentre `residual_std_ratio` e `diff_std_ratio` sono già rapporti positivi. Usare i valori con segno ignorerebbe le deviazioni negative, che sono anomalie quanto quelle positive. Solo la coda superiore è informativa.
1. Su N1–N5, per ciascuna delle quattro feature si raccolgono i valori **per-variabile** così definiti (50 finestre × 41 XMEAS = 2.050 valori per feature, non i 50 massimi di finestra) e si stimano mediana e MAD.
2. Si congelano gli otto numeri risultanti (4 mediane, 4 MAD).
3. Per una finestra qualsiasi: `z[f,v] = (s[f,v] − med[f]) / MAD[f]`, e lo score combinato è `S = max` su f e su v di `z[f,v]`.
4. Il quantile di `S` si calibra sui 350 punteggi di `cal_thr` con `k = ceil((n+1)(1−α))`.

Così la molteplicità fra i 41 sensori **e** fra le quattro feature è gestita dallo stesso massimo, la comparabilità fra scale eterogenee è risolta su un insieme congelato e disgiunto invece che con una riscalatura arbitraria, e c'è una sola soglia, un solo α e una sola Beta, esatta sotto l'ipotesi di continuità di `S` (vedi sotto).

Perché mediana/MAD sui valori per-variabile e non una trasformazione di rango sui massimi di finestra: con 2.050 valori per feature la stima robusta di centro e scala è ben determinata, mentre una ECDF su 50 massimi avrebbe risoluzione 1/50 proprio in coda. È la stessa normalizzazione robusta usata da RBC-AD, applicata però a un insieme disgiunto da quello di calibrazione.

*Verifica da pre-registrare.* Il massimo di z robusti assume che le quattro feature abbiano code di forma comparabile, non solo centro e scala: se una ha code molto più pesanti domina il massimo. Sul solo `baseline_fit` si conta quale feature realizza il massimo; se una sola lo realizza in più del 70% delle finestre si valuta la **variante A′** definita qui sotto, e la si adotta solo se riduce strettamente la dominanza massima; altrimenti A è terminale. Vedi la regola congelata più sotto. La scelta si fa su `baseline_fit`, mai su `cal_thr`.

**Variante B — ritirata dal percorso principale.** La motivazione è più semplice di quella data nelle revisioni 6–8, e sufficiente da sola.

`p_f` è una trasformazione empirica: assume valori nell'insieme finito `{1/(N_f+1), 2/(N_f+1), …, 1}`. Quindi `S = −min p_f` assume valori in un insieme finito, cioè **`S` è discreto**. L'ipotesi di continuità di `S` richiesta da Beta(17, 334) viene meno, e la Beta **non è giustificata**. Ciò che resta è la garanzia marginale `P(falso allarme) ≤ α`, conservativa.

Questo è il motivo, e non servono gli altri che avevo addotto, tutti difettosi: *essere limitato superiormente* non è di per sé un problema, perché anche uno score continuo e limitato produce la Beta esatta; *la presenza di un atomo all'estremo* non implica che la soglia al 5% vi cada, cosa che accade solo se la massa dell'atomo è abbastanza grande; e il limite `164/2051` presupponeva che ogni valore nuovo fosse scambiabile con i valori della baseline aggregata, che il pooling di 41 variabili eterogenee non garantisce. Quei tre argomenti sono rimossi.

La distinzione che conta fra le varianti è quindi una sola: A e A′ applicano ai valori una mappa **continua e strettamente monotona**, quindi **preservano** la continuità di `S` se i valori di partenza sono continui — non la garantiscono, perché la continuità resta una proprietà delle quantità di partenza; B li sostituisce con ranghi, e la distrugge in ogni caso.

La scelta è fra esattezza della Beta e trasformazione di rango, e **si sceglie l'esattezza**: il senso di C3 era avere un unico score il cui quantile ha una distribuzione condizionale nota. La variante B si conserva soltanto come **analisi di sensibilità documentata**, con il suo FAR dichiarato come limite superiore `≤ α` e senza rivendicare alcuna distribuzione condizionale.

**Variante A′ — la risposta alla comparabilità delle code, senza saturazione.** Il motivo per cui B era stata introdotta era la possibile disparità di forma delle code fra le quattro feature. Si ottiene lo stesso effetto restando continui: poiché le quattro quantità sono tutte positive e a una coda, si applica una trasformazione stabilizzante prima della standardizzazione robusta,

`u[f,v] = log1p( s[f,v] / c_f )`,  `z_f[v] = ( u[f,v] − median_f(u) ) / MAD_f(u)`

dove `c_f > 0` è un offset di scala **stimato e congelato su `baseline_fit`**, definito come la **mediana dei soli valori per-variabile strettamente positivi** di quella feature. La mediana semplice non garantirebbe `c_f > 0`: se oltre metà dei valori di `|slope_sigma_h|` fosse esattamente zero la mediana sarebbe nulla e la trasformazione indefinita. Con la regola sui soli positivi `c_f` coincide con la mediana semplice nel caso realistico in cui tutti i valori sono positivi, ed è comunque ben definita finché esiste almeno un valore positivo.

**Controlli di degenerazione, entrambi bloccanti.** Lo script si arresta con un errore esplicito, senza sostituzioni silenziose, in due casi: se una feature non ha alcun valore positivo su `baseline_fit`, quindi `c_f` non è definibile; e **se una delle quattro `MAD_f(u)` vale zero**, che renderebbe `z` indefinito per divisione. La seconda condizione si verifica quando più di metà dei valori trasformati coincidono, ed è indipendente dalla prima.

*Precondizioni verificate sui dati attuali*: su N1–N5 tutte le 2.050 osservazioni per feature sono positive e le quattro MAD delle quantità trasformate sono maggiori di zero. Nessuno dei due controlli scatta oggi; restano nello script perché `baseline_fit_new`, se si rendesse necessaria, sarebbe generata ex novo. Il logaritmo nudo non va: `|shift_sigma|` e `|slope_sigma_h|` possono valere esattamente zero, e i valori prossimi allo zero manderebbero `log s` verso −∞ distorcendo mediana e MAD anche senza zeri esatti. `log1p(s/c_f)` è definita in `s = 0` (dove vale 0), strettamente crescente e continua su `[0, ∞)`, quindi **non introduce atomi** e non satura sopra il massimo di baseline. Per i due rapporti, che stanno intorno a 1.2 e non si avvicinano allo zero, la trasformazione è innocua; serve per le due quantità in valore assoluto.

A′ congela dodici numeri (4 offset `c_f`, 4 mediane di `u`, 4 MAD di `u`) invece degli otto di A. Sulle quantità positive a coda pesante la trasformazione riduce la disparità di forma, che era l'unico problema che B doveva risolvere.

### Regola di selezione fra A e A′ — ADOTTATA E CONGELATA il 2026-09-12

La dominanza è la frazione di finestre di `baseline_fit` in cui una stessa famiglia realizza il massimo; la *dominanza massima* è il valore della famiglia che la realizza più spesso.

1. Se la dominanza massima con A è **≤ 70%**, si mantiene **A** e **A′ non viene calcolata**.
2. Se è **> 70%**, si calcola A′ sulla **stessa** `baseline_fit` e si adotta A′ **soltanto se la dominanza massima diminuisce strettamente**.
3. In caso di **parità o peggioramento** si mantiene **A**. Se la variante selezionata resta sopra il 70%, si dichiara la dominanza residua come limite, **senza** passare a B.

La dominanza si misura esclusivamente su `baseline_fit`, mai su `cal_thr`.

**Natura dell'intervento.** Questa è una **modifica adottata** della regola precedente, non un chiarimento: la versione precedente, una volta passata ad A′, la manteneva anche se la dominanza non migliorava. La modifica risponde direttamente al motivo per cui la trasformazione viene considerata, cioè ridurre la dominanza, e il costo espositivo è minimo.

**Proprietà garantita, e suo limite.** L'enunciato corretto è: *nessun percorso aumenta la dominanza misurata sulla baseline.* **Non** «nessun percorso congela la variante peggiore»: una dominanza minore non implica una maggiore potenza diagnostica, che non è stabilita. La proprietà riguarda esclusivamente la dominanza misurata sulla baseline.

**Stato del congelamento.** Congelata il 2026-09-12. La scelta è **informata dai dati storici di sviluppo e baseline già osservati**, inclusa la diagnostica LOBO riportata sotto, e questo è dichiarato esplicitamente. Ciò che è congelato è la **procedura di selezione**: l'esito effettivo, A oppure A′, sarà determinato applicandola alla `baseline_fit` prevista, **prima della calibrazione** e prima di ogni accesso a verifica, validazione e test.

**Indicazione anticipata dai dati di Fase A, non esito della decisione.** Sulle feature leave-one-block-out di N1–N5 la dominanza risulta del 48% con A e del 74% con A′. Per riferimento, le mediane delle feature **per variabile** `residual_std_ratio` e `diff_std_ratio` sullo stesso CSV storico valgono 0,9518127 e 0,9978460: sono mediane di quelle due feature, **non** mediane degli score combinati A e A′. Applicando la regola congelata a questi numeri l'esito sarebbe «si resta su A», per la clausola 1 (48% ≤ 70%), senza nemmeno calcolare A′. Questi numeri sono calcolati con la funzione di score della Fase A, baseline su quattro blocchi, non con la funzione congelata di C0 su `baseline_fit`: sono un'indicazione utile — e rassicurante su A — ma non costituiscono l'esito della decisione, che non esiste ancora. Mostrano inoltre che la trasformazione di A′ può peggiorare la dominanza anziché riequilibrarla.

**Formulazione corretta della garanzia, e controllo sui pareggi.** Osservare 350 punteggi tutti distinti **non dimostra** che la distribuzione di `S` sia priva di atomi: è una diagnostica, non una prova. La dicitura da usare è quindi: *Beta(17, 334) esatta sotto l'ipotesi di continuità di `S`; l'assenza di pareggi fra i 350 punteggi di calibrazione è riportata come diagnostica a supporto, non come verifica dell'ipotesi.* Lo script verifica la distinzione dei 350 valori e riporta il numero di pareggi se presenti. **In presenza di pareggi la Beta non diventa "approssimata": formalmente non è giustificata**, e non va riportata. Ciò che resta è la garanzia marginale `P(falso allarme) ≤ α`, conservativa, e va dichiarata in quei termini.

L'alternativa che renderebbe l'esattezza indipendente dall'ipotesi è il **tie-breaking casuale** (statistica d'ordine smoothed). La ragione per non adottarlo **non è la riproducibilità**: un seme congelato la garantisce. Le ragioni effettive sono tre: è superfluo se la continuità vale, e per uno score costruito da misure continue l'ipotesi è mite; introduce nella soglia una componente dipendente dal seme, riproducibile ma arbitraria, senza un criterio principiato per scegliere un seme piuttosto che un altro; e rompe la confrontabilità con la Fase A, che usava una statistica d'ordine deterministica. Resta disponibile se si preferisse l'esattezza senza ipotesi a queste tre cose. Il confronto resta quello della Fase A, superamento stretto `S > soglia`.

**C4 — Riportare l'incertezza della soglia, non solo la soglia.** Tre quantità accanto al valore: l'intervallo Beta del FAR condizionale, **esatto sotto l'ipotesi di continuità di `S`** e da omettere in presenza di pareggi, un bootstrap sui run per la soglia stessa, e il **FAR realizzato su `far_ver`**, cioè su run normali nuovi mai usati né per la baseline né per la calibrazione, calcolato su tutte le loro finestre con errore standard da bootstrap a livello di run.
*Motivazione*: Diallo, Homri, Dantan (J. Process Control 2025) danno `FAR ~ Beta(l, n_c+1−l)` e documentano che il conformal marginale viola α = 1% nel 48.2% delle realizzazioni. Nessuno dei 22 paper riporta questo intervallo su TEP. Per contrasto: Odiowei & Cao (2010) riportano *"no false alarm has been observed"* contro l'1% nominale come risultato positivo; Zhang et al. (2018) e TceOne (2023) dichiarano il 99% e non misurano mai il FAR; Spina et al. (2024) lo misurano in-sample. La Fase A stessa dichiara il suo conteggio *"descrittivo, non una stima out-of-sample"*.
*Guadagno*: il primo FAR out-of-sample documentato su questa pipeline, e l'obiezione prevedibile del revisore diventa un risultato nostro.

## Componente separata, non attivata

**C5 — Garanzia per evento.** Da trattare come estensione distinta del rilevatore, da attivare solo se si costruisce un rilevatore operativo, non come parte della calibrazione delle soglie del verbalizzatore.

Va inoltre enunciata con precisione. Kaur et al. 2024 (Teorema 2, Lemma 3) limitano la probabilità di **falso allarme su una traccia**: `P(falso allarme su X_t) ≤ ε`, cioè un errore **per run**. Non è "allarmi per ora". Il passaggio a un tasso orario richiede in più: una definizione operativa di evento di allarme (Khan et al. 2026 usa la sequenza contigua massima di predizioni positive), una durata di run fissata, e l'assunzione che il tasso si calcoli mediando su run di quella durata. Senza queste tre cose l'affermazione "allarmi/ora garantiti" non è supportata. La formulazione difendibile è: *≤ ε falsi allarmi per run di durata T*, con la conversione oraria dichiarata come media su run omogenei. Il bersaglio operativo orario esiste in Khan et al. (Scientific Reports 2026) **senza garanzia**; la garanzia esiste in Diallo e in Kundačina **per campione**. Unire le due cose resta il contributo rivendicabile, ma va costruito, non dedotto.

## Cosa non cambia

Formula del rango `ceil((n+1)(1−α))`; calibrazione su soli dati normali; massimo sulle 41 XMEAS dentro la finestra (che gestisce correttamente la molteplicità fra sensori); superamento stretto `score > threshold`; divieto di ritoccare le soglie dopo l'apertura di validazione e test.

Il leave-one-block-out **non** è in questa lista: sostituito da C0.

## Cosa scartiamo, con il motivo

- **Aggiustamento DKW (Bates et al. 2023)**: `sqrt(log(2/δ)/2n)` vale 0.173 a n = 50, 0.065 a n = 350, 0.022 a n = 3.075. A n_cal = 350 è ancora maggiore di α = 0.05. Resta come riga di confronto, non come soglia operativa.
- **EVT / GPD**: con n_cal = 350 il pavimento è 0.28%. Serve solo se il budget di allarmi scende sotto quel livello.
- **Validità condizionale alla calibrazione come contributo rivendicato**: occupata da due gruppi indipendenti (Diallo 2025, Kundačina 2025). Si cita, non si rivendica.

## Prerequisito (ii): generatore del simulatore e schema dei flussi

*Accertato sul sorgente il 2026-09-12. La direzione è decisa; una quantità resta da misurare.*

### Come entra l'alea

Il blocco S-function `TE Code` in `MultiLoop_mode1.mdl` ha `Parameters = [] rand()`: il secondo parametro è il seme, valutato da MATLAB e passato al mex. In `temexd_mod.c` il seme inizializza `randsd_.g` e l'unico generatore è `tesub7_`:

`g ← fmod(g · 9228907, 2³²)`,  uniforme = `g / 2³²` per il rumore di misura, `2g/2³² − 1` per i disturbi.

`tesub6_` costruisce il rumore gaussiano come somma di **12** uniformi, `(Σ − 6)·std`, applicato a **22** misure: **264 estrazioni per aggiornamento**.

### Quello che è accertato

1. *Non esistono substream.* Si controlla un solo numero per run e il mex non espone alcun jump-ahead.
2. *Fuori dal sottoinsieme dei multipli di 8 la ricorrenza intera non è garantita.* Il prodotto `g·9228907` può superare 2⁵³ e può non essere esattamente rappresentabile; pertanto la ricorrenza intera non è garantita durante quel tratto, e in esso l'identità `g_k = g_0·a^k mod 2³²` non descrive necessariamente la mappa implementata. Superare 2⁵³ non implica di per sé arrotondamento: dipende dalla rappresentabilità del prodotto. **Questo non autorizza a concludere che il non-sovrapponimento non sia analizzabile**: quando lo stato appartiene ai multipli di 8 la mappa è esatta, come documentato nella sezione successiva, che prevale su questo punto.
3. *Sui semi verificati lo stato entra nei multipli di 8 e non ne esce.* È un'**osservazione** sui semi provati, interi e frazionari, non una dimostrazione generale: il seme 123456789 vi entra alla 17ª estrazione. Finché resta un'osservazione, il confinamento ai 2²⁹ stati multipli di 8 va enunciato come tale e non come proprietà dimostrata della mappa per ogni seme.

### Struttura del generatore legacy: cosa è stabilito e cosa no

*Controlli riproducendo in sola lettura la ricorrenza del sorgente. Non sono misure runtime del MEX.*

**Stabilito.** Quando lo stato appartiene ai multipli di 8 la ricorrenza è **esatta**, non arrotondata: `g = 8h` con `h < 2²⁹` dà `h·a < 2⁵²·¹⁴ < 2⁵³`, e la moltiplicazione per 8 sposta solo l'esponente. Verificato su 20.000 stati casuali: la mappa in virgola mobile coincide con la mappa intera `h ← h·a mod 2²⁹`. L'ordine moltiplicativo di 9228907 modulo 2²⁹ è **2²⁷**. Cade quindi l'affermazione delle revisioni 11–12 secondo cui l'aritmetica inesatta impedirebbe qualunque analisi: il jump-ahead è calcolabile esattamente su questa orbita.

**Stabilito, e decisivo contro l'argomento per cassetti della revisione 12.** Gli stati **non appartengono tutti alla stessa orbita**. Le unità modulo 2²⁹ sono 2²⁸ e l'ordine di `a` è 2²⁷, quindi l'indice è 2: per `h` dispari esistono **due** orbite distinte di periodo 2²⁷ ciascuna, una confinata nelle classi {1,3} mod 8 e l'altra in {5,7} (verificato). Contando anche le valutazioni 2-adiche superiori, l'unione di tutte le orbite è l'intero insieme dei 2²⁹ stati multipli di 8. **Sommare le estrazioni di tutti i run e dividerle per 2²⁷ non dimostra nulla**, perché confonde il periodo di una singola orbita con lo spazio complessivamente disponibile a run che partono da orbite diverse.

Cade anche l'ipotesi di un'orbita chiusa sui multipli di 4: il seme 123456789 entra nei multipli di 8 alla 17ª estrazione e non ne esce più. Il tratto precedente è un transitorio, e da esso non segue alcun limite di periodo 2²⁸.

**Rapporti fra domanda e spazio disponibile** (tutti i 2²⁹ stati multipli di 8; ipotesi più favorevole di 264 estrazioni per minuto simulato):

| Disegno | Estrazioni ipotizzate | Rapporto con 2²⁹ |
|---|---:|---:|
| Completo, 510 run da 70 h | 565.488.000 | 1,0533 |
| Economico principale, durata attesa | 440.748.000 | 0,8210 |
| Economico con `baseline_fit_new`, durata attesa | 514.008.000 | 0,9574 |

**Conclusione, deliberatamente non conclusiva.** Per il disegno *completo* un argomento per cassetti sull'intero spazio può funzionare, ma solo giustificando sia il limite inferiore delle estrazioni sia l'appartenenza degli stati conteggiati a quel sottoinsieme. Per il disegno *economico*, che è quello proposto, questi numeri non bastano: il rapporto è sotto 1 e le durate sono **attese**, non deterministiche, perché `J ~ Unif{1,…,10}`. L'insufficienza del generatore legacy **non è quindi dimostrata** per il disegno proposto, e non va registrata come tale.

**Ruolo del contatore diagnostico.** Resta quello originario e pieno: misurare il consumo effettivo di estrazioni e il comportamento reale delle callback — quante invocazioni per `Callflag`, dato che il rumore di misura è sotto guardia `Callflag < 2` e `mdlDerivatives` chiama con 2 — oltre alla tracciabilità. Non è declassato a strumento di dimensionamento dei contatori Philox.

### Decisioni prese

- **Modifica e ricompilazione sì, in una copia versionata del simulatore.** Il legacy resta intatto e utilizzabile, e la copia modificata è un artefatto distinto e tracciato.
- **Generatore: Philox4×32-10**, con **implementazione verificata** contro i vettori di test noti (known-answer tests di Random123) prima dell'uso. Identificatore di flusso = indice di run, contatore = indice di estrazione. **Indice di run e contatore registrati nel manifest** insieme a seme della chiave, versione del mex, hash del modello, burn-in, lunghezza del run e posizione della finestra.
- `tesub6_` resta **identica**: somma di 12 uniformi e `(Σ−6)·std`. Cambia il flusso uniforme sottostante, non la legge del rumore.

### Tre qualificazioni da mantenere nel testo del paper

1. **Philox fornisce flussi pseudocasuali separati, non indipendenza matematica.** L'IID fra run resta un'**assunzione del disegno**, sostenuta dalla separazione dei flussi e dall'identità della procedura, non un teorema. Vale per la binomiale esatta della verifica primaria e per la Beta allo stesso modo.
2. **Cambiare generatore conserva la distribuzione marginale del rumore ma può cambiarne le correlazioni temporali.** Le quattro feature misurano struttura temporale (pendenza, rapporti su residuo e differenze), quindi la distribuzione di `S` può spostarsi anche a legge marginale invariata.
3. Di conseguenza **il simulatore modificato va validato contro il legacy**: a parità di tutto il resto si generano due insiemi di run, uno per generatore, e si confrontano le distribuzioni dei quattro score e di `S`. La macchina è la stessa del controllo preliminare sui pilota (mediana e MAD di `S`, con la regola di magnitudine già fissata), applicata però a un confronto fra generatori anziché fra baseline e run nuovi. Se il confronto mostra uno scostamento, va dichiarato e discusso, non assorbito.

### Due effetti collaterali da correggere nello stesso intervento

Il parametro `rand()` va sostituito con una variabile esplicita di workspace, così il seme è controllato e registrato e non dipende dallo stato del generatore di MATLAB: all'avvio di una sessione nuova `rand()` restituisce sempre lo stesso valore, quindi run lanciati da sessioni distinte condividerebbero il seme. Vale la pena verificare se questo ha già interessato la generazione di N1–N5.

Il bit `0x20` di `MSFlag` va lasciato **non impostato**: con quel bit `measnoise` e `procdist` sono due stati inizializzati entrambi a `rseed` e avanzati dalla stessa mappa, quindi la k-esima estrazione di rumore e la k-esima di disturbo coincidono. Oggi il modello passa due soli parametri, quindi `MSFlag = 0` e il bit è già spento; va documentato perché deve restare così.

## Nota su come citare RBC-AD

La forma del quantile corretto in campione finito è l'Eq. (20) di RBC-AD, ma è una formula standard e va attribuita alla letteratura conformal. RBC-AD si cita per la sua rinuncia esplicita: *"This FAR-based selection ... does not add a conformal guarantee beyond the quantile computation on calibration scores. Calibration scores used for quantiles are computed on overlapping windows and are not independent; exchangeability is not enforced."* È il precedente più vicino sullo stesso benchmark e non rivendica la garanzia che il titolo promette.
