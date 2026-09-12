# Come la letteratura giustifica la scelta dei descrittori — e perché non aiuta

**Data:** 2026-09-11 · **Revisione:** 2026-09-11, dopo revisione dell'autore (§5 riscritta e allineata a `DECISIONE_calibrazione_soglie_fase_B.md`; §§0–4 invariate)
**Domanda:** esiste in letteratura un criterio riusabile per giustificare *perché proprio quei descrittori* nello strato di rappresentazione della Fase A (`shift_sigma`, `slope_sigma_h`, `residual_std_ratio`, `diff_std_ratio`, più la derivata `rapid`)?
**Risposta breve:** no. Ma esiste un *template di argomentazione* pubblicato, ed esiste un risultato negativo pubblicato che rende la domanda molto meno pericolosa di quanto sembri.

---

## 0. Provenienza dei dati — leggere prima

Questo documento mescola tre livelli di evidenza. Sono tenuti separati apposta.

| Livello | Che cosa | Affidabilità |
| --- | --- | --- |
| **Metadati Scopus/arXiv** | Titolo, venue, anno, DOI, citazioni, open-access dei 30 risultati della ricerca §1 | Fattuali |
| **Full text letto** | I cinque paper della §3, letti integralmente dal `.md` in `papers/`, con citazioni verbatim | Fattuali, verificabili nel file citato |
| **Analisi** | Verdetti, implicazioni per la Fase A, §2 e §5 | Mia, non un dato bibliografico |

**Limite dichiarato sulla §1.** I 25 risultati Scopus sono stati ottenuti con `view=STANDARD`, che **non restituisce l'abstract**. La caratterizzazione di quel gruppo in §2 è quindi inferenza dai titoli, non lettura. I 5 risultati arXiv avevano l'abstract. Nessuno dei 30 è stato letto in full text *in quanto risultato della ricerca*; i cinque della §3 sono stati letti perché già presenti in `papers/`.

**Nota di metodo emersa a posteriori.** Circa 17 dei 30 risultati erano **già nel corpus locale** `papers/` in full text. La ricerca ha in buona parte riscoperto materiale già posseduto. Prima di lanciare una ricerca bibliografica su questo progetto conviene enumerare `papers/` per intero (sono 52 file, ~483.000 parole) invece di fidarsi di un listato troncato.

---

## 1. La ricerca eseguita

Finestra 2010–2026, tetto 30 risultati. Fonti: Scopus (25), arXiv (5). OpenAlex non disponibile (HTTP 503 su tutte le chiamate, come già nella ricerca sulla calibrazione delle soglie dello stesso giorno).

```
("Tennessee Eastman Process" OR "Tennessee Eastman" OR TEP)
AND ("fault diagnosis" OR "fault detection")
AND ("feature selection" OR "feature engineering" OR "feature extraction"
     OR "time-domain features" OR "frequency-domain features"
     OR "cross-sensor features" OR "learned representation")
AND ("multivariate time series" OR "industrial process data")
```

## 2. Esito: nessun criterio di selezione (analisi)

Nei 30 risultati la scelta delle feature non è una decisione metodologica documentata: è l'architettura della rete. «Multi-scale feature extraction», «spatio-temporal representation learning», «feature fusion» descrivono topologie, non criteri. Dove il contributo per feature *viene* quantificato, è attribuzione a posteriori su un modello già addestrato — inutilizzabile sotto la disciplina di congelamento della Fase A, che fissa la rappresentazione prima di aprire la validazione.

Una verifica indipendente sul corpus locale conferma la direzione: su 52 file in `papers/`, **uno solo** contiene linguaggio di criterio dichiarato per la scelta dei descrittori, e alla lettura si è rivelato un falso positivo (§3.4). Il grep trova vocabolario, non argomenti, quindi questa è conferma parziale, non prova.

**`catch22` / `hctsa` / `tsfresh`: pista chiusa.** Nel corpus locale `tsfresh` compare tre volte, tutte incidentali (una frase di tassonomia, una riga di tabella, la bibliografia) in Pappa et al.; `catch22` e `hctsa` non compaiono mai, in nessun file. La letteratura dei cataloghi canonici di feature per serie temporali — che *è* il luogo dove un criterio di selezione esplicito esiste — non ha contatto con questo filone. Se serve, va importata dall'esterno: non è disponibile come precedente interno.

---

## 3. I cinque paper letti in full text

### 3.1 FaultExplainer — il risultato negativo che serve alla Fase A

Khan, Nahar, Chen, Constante Flores, Li (Purdue). Preprint sottomesso a *Computers & Chemical Engineering*, 20 dicembre 2024. **Nessun DOI nel file** — da risolvere prima di citare. Codice: `github.com/li-group/FaultExplainer`.

È il lavoro più vicino alla Fase A: anch'esso decide *quale evidenza numerica mettere davanti a un LLM*. Quello che mostra:

> «Once a fault is detected, we select the six features (variables) with the largest contribution values **at the last time step**. The values of these features are compared to their mean values during normal operation, and the value comparisons and percentage changes are incorporated into the prompts for the LLM.» (§5.1)

Cioè: **un solo descrittore** — scarto percentuale di livello — su **un solo istante**. Nessuna finestra, nessun trend, nessuna dispersione. Il taglio a sei non è giustificato in nessun punto del paper; non c'è ablazione né analisi di sensibilità sull'evidenza mostrata (l'unica cosa variata è lo spazio delle ipotesi nel prompt). La selezione è ereditata da PCA/T² e presentata come data.

**Il valore per noi non è come precedente ma come fallimento documentato dagli autori stessi**, su due meccanismi che corrispondono uno-a-uno a due nostri descrittori:

> «The model's reasoning was **limited by the feature set provided by PCA**, which failed to capture variables directly linked to the root cause.» (§5.2.2, sul Fault 10 — variazione casuale)

> «the **inability of the PCA-selected features to capture the subtle dynamics** of reaction kinetics changes… particularly those involving **gradual or non-obvious changes like reaction kinetics drift**.» (§5.3.2, sul Fault 13 — drift lento)

E la loro future work chiede esplicitamente ciò che la Fase A fa:

> «integrating advanced feature selection techniques, such as **domain-informed feature engineering** or causal inference, could enhance the model's ability to detect faults linked to complex root causes.» (Conclusioni)

Fault 13 è il drift che `slope_sigma_h` esiste per esprimere; Fault 10 è la variazione casuale che i due rapporti di variabilità esistono per esprimere.

*Cautela.* Questo giustifica *feature ingegnerizzate su base di dominio contro contributi PCA*. **Non** giustifica quattro descrittori invece di cinque, né descrittori progettati contro rappresentazioni apprese. Quel vuoto resta nostro.

*Da non citare approvativamente:* il loro tasso di falsi allarmi di 10⁻¹² è ottenuto come 0.01⁶ assumendo osservazioni indipendenti, assunzione insostenibile su TEP.

### 3.2 Pappa, Karvelis, Stylios — il template di argomentazione

*Expert Systems With Applications*, vol. 332 (2027), art. 133478. DOI `10.1016/j.eswa.2026.133478`. CC BY. **Discrepanza d'anno da gestire:** il DOI e il copyright dicono 2026, il volume dice 2027.

Architettura sorella: SAX simbolico → testo → LLM, con un blocco ausiliario di descrittori numerici progettati a mano. Usano **tre** descrittori (μ_y, σ_y, μ_z), scelti su base fisica, con citazione d'autorità a Kwapisz et al. 2011, **senza pool di candidati, senza criterio di ricerca, senza sweep**; e la sensitivity sulla loro unica soglia libera (ε = 0.05) è **esplicitamente rinviata a future work**. Ha passato una rivista Q1.

Il principio che dichiarano è la cosa più portabile del paper:

> «The design question in a new domain reduces to **identifying which classes become symbolically indistinguishable after normalization and selecting descriptors that restore the lost discriminative information**, which is a substantially more tractable problem than redesigning the representational pipeline from scratch.» (§7.4)

Pappa giustifica i descrittori come **recupero mirato di informazioni discriminanti perse nella normalizzazione e nell'aggregazione**. Questo offre un precedente per l'argomento progettuale, non dimostra la completezza del nostro set. Ammettono anche il costo dell'asserzione: «this requires prior knowledge of which physical quantities are discriminative for the target domain» (§7.4).

**La forma della loro ablazione è più importante dei numeri.** Rimuovere l'intero blocco di descrittori costa 15,06 punti, ma la tesi non sta nella media: sta nel fatto che il recall di *Standing* crolla al 20,8 % con 176 campioni assorbiti da *Sitting*. Rimuovere il canale di trend costa **0,95 punti**, e lo incorniciano così:

> «trend-aware encoding **addresses a specific representational gap rather than providing a general performance boost**.» (§6.2)

Con una metrica globale quel canale sarebbe stato scartato.

*Limite che ci riguarda direttamente:* rendono sei assi come sei righe etichettate indipendenti, senza alcun costrutto simbolico cross-sensore, delegando tutta la struttura inter-variabile all'attenzione dell'LLM, dentro un budget di 1024 token. **Non offrono alcun precedente per 41 sensori**, né metodo di selezione dei canali, né discussione dello scaling della lunghezza del prompt.

### 3.3 HDLCNN-SHAP — inutilizzabile, per due motivi indipendenti

Li, Peng, Wang, Wang (Zhejiang Univ. / UESTC). Sottomesso a *IEEE T-ASE*. **Nessun anno e nessun DOI nel file.**

Primo motivo, confermato dal full text: SHAP è strettamente post-hoc.

> «Then the **trained model is seen as a black box** and we apply the SHAP method to interpret the model performance.» (§III)

Secondo motivo, che l'abstract nascondeva: le sue «feature» sono le 22 variabili misurate grezze, non descrittori ingegnerizzati. Anche applicato a priori ordinerebbe *sensori*, non *statistiche di sensori*. È muto sulla nostra domanda.

*Unica cosa trasferibile, ed è metodologica:* il clustering gerarchico di §III-A è non supervisionato, senza etichette, invariante all'ordine, e **fissato prima di qualsiasi addestramento**. È un precedente per la *disciplina* (rappresentazione fissata a priori con sola struttura non supervisionata, poi congelata), non per i quattro descrittori. Da notare che il loro k = 2 non è giustificato da alcun criterio.

*Validazione root-cause debole:* n = 2 guasti su 21, scelti perché «their root-cause features are proven and widely used», verifica solo visiva, nessuna metrica quantitativa.

### 3.4 Zhang, Jiang, Li, Yang (SDAE + kNN) — falso positivo, ma precedente su un altro punto

*Journal of Process Control* 64 (2018) 49–61. DOI `10.1016/j.jprocont.2018.02.004`.

Il grep l'aveva segnalato come unico file con un criterio dichiarato. Alla lettura, il match è su linguaggio che dice **l'opposto**: ciò che si evita di scegliere a mano è la *funzione kernel*, non i descrittori.

> «the architecture of SDAE is all learned from data, which not only avoids the problem of **choosing nonlinear function manually**…» (§1)

Non contiene alcun criterio di selezione di descrittori. Argomenta contro la progettazione manuale ma **non esegue mai un baseline con feature progettate a mano**, non riporta il tasso di falsi allarmi, non dichiara il valore di k, non fa alcuna ablazione. La tesi «appreso batte progettato» è, in questo corpus, asserita e non dimostrata. La sua stessa Tabella 5 mostra la statistica sullo spazio di feature appreso (HD²) molto peggiore di quella sui residui (RD²) proprio sui guasti sottili (F16 0,282 contro 0,901; F19 0,087 contro 0,761).

*Precedente genuino, da citare con precisione:* i limiti di controllo sono stimati via KDE al 99 % **su soli dati normali** (§3.3, passi 1–7; i guasti entrano solo nel monitoraggio online). **Caveat obbligatorio:** i loro iperparametri di rete sono stati messi a punto sul FDR di un set di validazione *etichettato con guasti*. Citare i passi 1–7, non il paper in blocco.

### 3.5 RBC-AD — non è il precedente conformal che sembrava

Mudasir, Asiri, Ameer, Al Reshan, Almansour, Awan, Shaikh. *Connection Science* 38:1 (2026), art. 2707826. DOI `10.1080/09540091.2026.2707826`. CC BY.

La parola «guarantee» compare **una sola volta in tutto il paper, in una smentita**:

> «This FAR-based selection defines a deployment operating point under a fixed detector configuration and **does not add a conformal guarantee** beyond the quantile computation on calibration scores. Calibration scores used for quantiles are computed on overlapping windows and are not independent; **exchangeability is not enforced**.» (§3.4)

Non è coverage marginale né condizionale. Non c'è costruzione a blocchi, nessuna correzione per la dimensione campionaria efficace, nessuna citazione alla letteratura *beyond exchangeability*.

**Quello che offre davvero, ed è utile, è il template della formulazione onesta:** chiamare la soglia un quantile finito-campione calcolato su punteggi di calibrazione normali sotto impostazioni fisse, dichiarare che l'exchangeability non è imposta perché le finestre si sovrappongono, e poi **riportare il tasso di allarme realizzato su dati normali held-out** (loro: 0,0398 contro un target di 0,05).

**Dettaglio tecnico direttamente trasferibile** — la regola di rango finito-campione:

> «k = min(max(⌈(n + 1)q⌉, 1), n), Q̂(q) = u₍k₎» (§3.4, Eq. 20)

La nostra calibrazione di Fase A (50 finestre, α = 0,05, **rango 49**) *è* esattamente questo stimatore: ⌈51 × 0,95⌉ = 49. Se ne può citare la forma.

**Esposizione che ne deriva, e che va registrata.** Il rango 49 su 50 è il **secondo valore più grande osservato**: varianza alta, tasso di falsi allarmi realizzato potenzialmente lontano da 0,05 in entrambe le direzioni. RBC-AD calibra su 3.075 finestre — circa sessanta volte le nostre — e **nonostante questo rinuncia a rivendicare la garanzia**. Il paper non contiene alcuna discussione di n minimo, sensibilità di τ a n, o comportamento in piccolo campione: non offre copertura per il nostro regime. Da approfondire con Barber, Candès, Ramdas & Tibshirani (conformal beyond exchangeability) o con una costruzione conformal a blocchi/per-run — nessuno dei due citato da RBC-AD. Si veda anche [`threshold_calibration_search_2000_2026.md`](threshold_calibration_search_2000_2026.md).

*Da sapere prima di citare:* la citazione «(Zhang et al., 2024)» in §2 non ha voce corrispondente in bibliografia; il paper non enumera mai quali guasti TEP usa; il parametro `ANOM_BETA_DIV`, che fissa il livello nominale della soglia di anomalia, non riceve mai un valore. Il punteggio dominante è una verosimiglianza neurale appresa (λ = 0,95) e la parte progettata a mano pesa 0,05 con coefficienti fissati per fiat (0,55/0,30/0,15) e nessuna ablazione: **non è un alleato per difendere descrittori progettati a mano**.

---

## 4. Metadati verificati sul full text

| Lavoro | Anno | Venue | DOI |
| --- | --- | --- | --- |
| FaultExplainer — Khan, Nahar, Chen, Constante Flores, Li | 2024 (preprint) | sottomesso a *Computers & Chemical Engineering* | **assente nel file** |
| SAX_HAR-LLM — Pappa, Karvelis, Stylios | 2026 / vol. 2027 | *Expert Systems With Applications* 332, art. 133478 | `10.1016/j.eswa.2026.133478` |
| HDLCNN-SHAP — Li, Peng, Wang, Wang | **non indicato** | sottomesso a *IEEE T-ASE* | **assente nel file** |
| SDAE-kNN — Zhang, Jiang, Li, Yang | 2018 | *Journal of Process Control* 64, 49–61 | `10.1016/j.jprocont.2018.02.004` |
| RBC-AD — Mudasir, Asiri, Ameer et al. | 2026 | *Connection Science* 38:1, art. 2707826 | `10.1080/09540091.2026.2707826` |

---

## 5. Conseguenze operative (analisi)

**5.1 Nel corpus esaminato non emerge un criterio di selezione. Passa per un argomento di progetto più un'ipotesi da verificare.**

*(a) Argomento di progetto, citabile.* Sul modello di Pappa §7.4, i quattro descrittori **coprono quattro aspetti scelti del segnale, senza conservarne integralmente l'informazione**. Non rappresentano esplicitamente le correlazioni temporali fra sensori né consentono di ricostruire l'andamento completo e i valori campione per campione. Mappa aspetto→operazione che lo perde in `DECISIONE_SCELTA_FEATURE_fase_A.md` §2.1. `shift_sigma` restituisce lo scostamento assoluto rispetto al baseline; `slope_sigma_h` restituisce la tendenza locale che la sintesi per finestra comprime; `residual_std_ratio` e `diff_std_ratio` restituiscono due dispersioni che differiscono **per ciò che rimuovono prima di misurare** — la retta locale della finestra la prima, il campione precedente la seconda.

> **Terminologia.** Non chiamarle feature «in bassa» e «in alta frequenza»: non sono risolte in banda e il freeze di Fase A dichiara esplicitamente «No FFT, wavelet, or other complex feature is part of this freeze». Sono misure di dispersione, non descrittori spettrali. Analogamente, il set va enunciato come **quattro feature calibrate più `rapid` derivata**, non come cinque feature.

Pappa fornisce la *forma* dell'argomento e il precedente che quella forma supera la revisione in una rivista Q1. **Non** dimostra che i nostri quattro descrittori siano necessari: il contenuto dell'argomento resta nostro da sostenere.

*(b) Motivazione dell'ipotesi, non difesa.* FaultExplainer dimostra che un'evidenza povera derivata da PCA — un solo scarto percentuale di livello su un solo istante — **limita la diagnosi su F10 e F13**, e sono gli autori stessi ad attribuirne la colpa allo strato di feature. Questo stabilisce che il vuoto esiste e che è consequenziale su questo benchmark. **Non** dimostra che pendenza e rapporti di variabilità lo colmino: quella è una nostra ipotesi, ed è esattamente ciò che la [§8.12 del piano autorevole](../paper/FoT_TEP_Review_Piano_Sperimentale.md) deve mettere alla prova. Citare FaultExplainer come difesa del nostro set sarebbe una scorciatoia che un revisore attento blocca.

**5.2 L'ablazione esistente è valida sul proprio endpoint; quell'endpoint non è la domanda.** L'ablazione leave-one-feature-out in [`analysis/feature_ablation/`](../../analysis/feature_ablation/FEATURE_ABLATION.md) misura il margine medio globale e la separabilità 1-NN della signature strutturata, e su quel terreno il suo esito è corretto e va conservato: togliere `trend`, `diff` o `rapid` alza il margine medio, e il blocco di sola variabilità mantiene 25/25 con il miglior margine sulla classe peggiore. Non è un artefatto. È semplicemente una risposta a una domanda diversa da quella che ci interessa, perché la Fase A non è progettata per massimizzare la separabilità 1-NN di un vettore a 697 componenti: è progettata perché un LLM legga un testo.

La rianalisi con endpoint localizzato — *quale coppia di classi collassa* quando si toglie una famiglia, sul modello di Pappa §6.2 — si può fare sui dati già raccolti senza ricalcolare nulla. **Resta però esplorativa**: cambia la lente su un esperimento già eseguito, non aggiunge evidenza indipendente. Il suo esito è un indizio che orienta il disegno della [§8.12 del piano autorevole](../paper/FoT_TEP_Review_Piano_Sperimentale.md), non una prova.

Ciò che quei dati sostengono oggi, ed è poco: **`residual_std_ratio`**. È l'unica rimozione **singola** che rompe la separabilità perfetta — `drop_residual_only` (residual tolto, `rapid` conservato) porta il 1-NN a **0,960** e il margine di F8/B2 a **−0,01503** — ed è quella che degrada più margini fra le rimozioni singole, **21 su 25**, contro 13 su 25 della successiva (`drop_diff_only`).

Il margine negativo **non è però esclusivo di quel braccio**: la rimozione coerente `drop_residual` (residual **più** la derivata `rapid`) mantiene il 1-NN a **1,000** e tuttavia porta F8/B2 a **−0,01150**. In entrambi i bracci la classe concorrente è F1 — similarità mediana inter-classe 0,90832 e 0,88941, la più alta in ciascun caso. Il dato sostiene quindi un'**associazione** fra la rimozione dell'evidenza residual e il collasso del margine di F8/B2 verso F1, non la necessità individuale della feature: `residual_std_ratio` resta nel set per motivazione di progetto, e questo indizio sui margini è il suo unico supporto empirico. Nient'altro è sostenuto.

In particolare **`slope_sigma_h` non è sostenuto da nulla**, nemmeno su F13: rimuoverlo *alza* il margine di F13 da 0,03300 a 0,03922. Va pesato contro il fatto che il canale di trend di Pappa vale 0,95 punti ed è stato accettato con la motivazione «specific representational gap» — un effetto piccolo e localizzato non è di per sé da scartare — ma allo stato attuale la pendenza è il descrittore con meno evidenza a favore, e va trattata come tale finché la [§8.12 del piano autorevole](../paper/FoT_TEP_Review_Piano_Sperimentale.md) non dice altro.

**5.3 Il fianco scoperto più probabile non è la scelta delle feature ma la calibrazione — e riguarda la Fase A.** Il rango 49 su 50 (§3.5) è la calibrazione **della Fase A, già eseguita**: 50 finestre da 5 h, massimo sulle 41 XMEAS, quattro soglie indipendenti a α = 0,05, rango ⌈(n+1)(1−α)⌉ = 49.

Su questo la mia lettura di §3.5 era incompleta. Il problema vincolante non è la varianza dello stimatore di rango: è che **la Fase A non è uno split conformal valido**, indipendentemente da n. Come stabilisce [`DECISIONE_calibrazione_soglie_fase_B.md`](DECISIONE_calibrazione_soglie_fase_B.md) sulla base del report di calibrazione originale, la funzione di score **non è la stessa sui due lati**: i 50 punteggi di calibrazione usano una baseline costruita sugli altri quattro blocchi, mentre fault, validazione e test usano una baseline costruita su tutti e cinque. **Questo da solo basta a invalidare lo split conformal**, senza bisogno di alcuna considerazione sulla struttura dei dati.

Il secondo limite è distinto e più debole, e va enunciato con precisione: la **scambiabilità** delle finestre adiacenti dello stesso blocco non è dimostrata. Non è la dipendenza in sé a invalidare il conformal — la garanzia richiede scambiabilità, non indipendenza, e dati dipendenti ma scambiabili sarebbero ammissibili. Ciò che manca è la dimostrazione, non l'indipendenza.

Non si può quindi rivendicare copertura marginale, e la distribuzione Beta del FAR condizionale non descrive la Fase A: descrive il caso migliore a cui la Fase B può aspirare. Si aggiunge la simultaneità fra le quattro feature, non corretta: α = 0,05 per feature ma FPR in-sample del 6,0 % sull'unione.

La posizione corretta per la Fase A è quindi quella che il report adotta già da sé — formula conformal-style come *upper order statistic*, senza rivendicazione di copertura — non una difesa della numerosità. Per la Fase B la questione è chiusa altrove: calibrazione a livello di **run** anziché di finestra, score identico sui due lati, n = 350, Beta(17, 334). Vedi il documento di decisione; qui non si duplica.

**5.4 Il cluster conformal del corpus locale è esaminato separatamente.** CODiT, RBC-AD, conformal anomaly detection industriale, EVT, alarm fatigue, weighted conformal in regime di pochi dati, one-class control charts: tocca il controllo dei falsi allarmi con garanzie e la difendibilità statistica in piccolo campione. È stato trattato per conto suo, non qui — ricerca bibliografica in [`threshold_calibration_search_2000_2026.md`](threshold_calibration_search_2000_2026.md), 22 paper letti integralmente, e decisione operativa in [`DECISIONE_calibrazione_soglie_fase_B.md`](DECISIONE_calibrazione_soglie_fase_B.md).

Sovrapposizione da conoscere: RBC-AD compare in entrambi i documenti. Qui (§3.5) è letto per la regola di rango e per la formulazione onesta della rinuncia alla garanzia; là è usato come colonna di confronto sulle unità di calibrazione. Le due letture sono coerenti e nessuna delle due va aggiornata a partire dall'altra.

> **Bozza superata.** Il disegno vigente è [§8.12 del piano autorevole](../paper/FoT_TEP_Review_Piano_Sperimentale.md); in caso di conflitto vale §8.12.

**5.5 La verifica vera è prospettica: ablazione testuale sui nuovi fault.** *(Disegno da approvare. Quando approvato va registrato nel piano sperimentale in `docs/paper/`, non qui: questo documento è analisi della letteratura, non protocollo.)*

L'endpoint è l'accuratezza diagnostica dell'LLM **per meccanismo di guasto**, non la separabilità di una signature. È l'unico endpoint che coincide con lo scopo per cui la Fase A esiste, ed è l'unico che può convertire la §5.1(b) da ipotesi a risultato.

Vincoli di disegno, tutti già identificati e nessuno negoziabile:

1. **Definito prima di eseguire i nuovi test.** Bracci, endpoint, regola di aggregazione e criterio di successo fissati in anticipo. Altrimenti è esplorazione travestita da conferma.

2. **Schema e lunghezza del prompt invariati fra i bracci.** Se «tolgo un descrittore» significa anche «fornisco meno testo», l'effetto misurato confonde informazione e lunghezza. La soluzione è **corrompere a parità di forma** invece di omettere: si sostituiscono i valori renderizzati di una famiglia con quelli della stessa famiglia presi da un altro caso, permutati fra i casi. Schema identico, stesse frasi, stesso numero di token, stessa distribuzione marginale; sparisce solo l'associazione col caso. Ha precedente in Pappa §6.3 (simboli di un asse randomizzati a lunghezza costante) ed è strutturalmente la **Condizione E del progetto applicata al descrittore invece che alla pseudolabel** — vocabolario di disegno già in uso, non un'invenzione.

3. **Due bracci, perché rispondono a domande diverse.** La permutazione misura *se l'LLM si appoggia a quel descrittore*; l'omissione misura *se la diagnosi ne ha bisogno*. Una divergenza fra i due è informativa e con un braccio solo resta invisibile.

4. **Selezione dei fault dalla descrizione fisica del meccanismo**, dalla tabella dei guasti TEP, **cieca rispetto a quali feature si attivano nei nostri dati**. Selezionare i fault guardando le attivazioni è selezione sull'esito e invalida la rivendicazione.

5. **La potenza viene dai run indipendenti per fault, non dal numero di fault.** Due fault per meccanismo danno copertura; non danno potenza. Poiché la rivendicazione è *per meccanismo*, il denominatore che conta è quello del singolo fault: a 5 run per fault un calo da 5/5 a 3/5 non è distinguibile dal rumore, qualunque sia l'n complessivo. A parità di costo, raddoppiare i run sui fault esistenti vale più di aggiungere due fault.

6. **Lo slegamento dalla fase congelata toglie vincoli di artefatto, non di credibilità.** Il nuovo esperimento deve congelare la propria rappresentazione e pre-registrare il proprio protocollo prima di aprire il proprio split di validazione, altrimenti non eredita nulla della disciplina che rende difendibile la Fase 1.

**5.6 Stato epistemico, da tenere separato nel paper.**

| Affermazione | Stato | Fonte |
| --- | --- | --- |
| Nel corpus esaminato non emerge un criterio di selezione dei descrittori applicabile a priori | Stabilito, limitatamente a questo corpus | §§1–3 |
| Il recupero mirato di informazioni perse ha un precedente nella rappresentazione simbolica per HAR | Documentato | Pappa §7.4; trasferibilità al nostro setting da verificare |
| Un'evidenza PCA povera limita la diagnosi su F10 e F13 | Stabilito | FaultExplainer §§5.2.2, 5.3.2 |
| I nostri quattro descrittori colmano quel vuoto | **Ipotesi** | da verificare in [§8.12 del piano autorevole](../paper/FoT_TEP_Review_Piano_Sperimentale.md) |
| La rimozione dell'evidenza residual degrada alcuni margini nella vecchia ablazione | Indizio esplorativo; necessità individuale non dimostrata | `analysis/feature_ablation/` |
| `slope_sigma_h` contribuisce | **Non sostenuta** allo stato attuale | ibid. |

---

> **Perimetro.** Questo documento è un'analisi di supporto. La letteratura ha un solo luogo attivo, la §14 di `docs/fot_walkthrough_conversazione_v2.md` (coppia `.md`/`.html`): **non è stata toccata**. Se uno di questi lavori va promosso a scheda di corpus, va aggiunto lì e solo lì.
