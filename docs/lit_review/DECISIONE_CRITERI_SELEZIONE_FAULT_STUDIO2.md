# Studio 2 — criteri di selezione dei fault (§6.1), revisione 1

Data: **2026-09-13**. Profilo: **decisionale**. Perimetro: solo §6.1.
Questo registro è la fonte della decisione; report, verifica e attestazione del congelamento
vivono in `studio2/fase03/selection/`. La revisione diventa congelata solo dopo verifica OK,
commit e tag dedicato, prima dell'esecuzione di D1. Non è il catalogo definitivo.

## 1. Decisione e ordine temporale

Si mantengono gli otto posti previsti dal piano: quattro classi di continuità
**F1, F8, F10, F13** e quattro nuove. La continuità è un vincolo preesistente, non un'estrazione
cieca né un campione rappresentativo dei fault TEP. Il riuso dei loro vecchi run come nuovi
run di sviluppo resta respinto (R1). Non si usano risultati storici per scegliere i nuovi fault.

Ordine obbligatorio: criteri verificati e congelati → D1 (unica estrazione e catalogo) →
generazione e analisi dei nuovi run. Prima del freeze sono ammesse solo tassonomia esterna,
letteratura preesistente e verifica combinatoria senza estrazione. Sono vietati risultati
per-fault dei propri esperimenti, inclusi sviluppo, test, score, separabilità, attivazioni dei
descrittori, lunghezza o ricchezza dell'evidence, confusioni, accuracy e astensione del modello.
La sonda sintetica 03.0 non è una fonte per i criteri.

Il pre-impegno riguarda i quattro nuovi fault; non cancella la conoscenza pregressa del
catalogo di continuità. Una consultazione indebita o una modifica dopo l'apertura dei risultati
va registrata come deviazione: nessun congelamento retrodatato. La verifica della cronologia
attesta i file e le operazioni registrati, non lo stato cognitivo di tutte le persone coinvolte.

## 2. Universo e attributi strutturali

Si usano **IDV(1)–IDV(15)** della tabella 8, p. 250, di Downs & Vogel (1993).
IDV(16)–IDV(20) hanno variabile e meccanismo non specificati; IDV(21) e le estensioni non
appartengono a quella tabella. Restano fuori dall'universo di questa selezione, senza giudizi
sulla loro difficoltà. `F<n>` e `IDV(n)` identificano lo stesso fault.

| IDV | Variabile/intervento documentato | Meccanismo | Chiave di identità |
| ---: | --- | --- | --- |
| 1 | rapporto A/C, B costante, flusso 4 | step | ratio_ac_s4 |
| 2 | composizione B, A/C costante, flusso 4 | step | composition_b_s4 |
| 3 | temperatura alimentazione D, flusso 2 | step | temperature_d_s2 |
| 4 | temperatura ingresso acqua reattore | step | temperature_cw_reactor |
| 5 | temperatura ingresso acqua condensatore | step | temperature_cw_condenser |
| 6 | perdita alimentazione A, flusso 1 | step | feed_a_loss_s1 |
| 7 | pressione/disponibilità alimentazione C, flusso 4 | step | header_c_pressure_s4 |
| 8 | composizione A/B/C, flusso 4 | random variation | composition_abc_s4 |
| 9 | temperatura alimentazione D, flusso 2 | random variation | temperature_d_s2 |
| 10 | temperatura alimentazione C, flusso 4 | random variation | temperature_c_s4 |
| 11 | temperatura ingresso acqua reattore | random variation | temperature_cw_reactor |
| 12 | temperatura ingresso acqua condensatore | random variation | temperature_cw_condenser |
| 13 | cinetica di reazione | slow drift | reaction_kinetics |
| 14 | valvola acqua reattore | sticking valve | valve_cw_reactor |
| 15 | valvola acqua condensatore | sticking valve | valve_cw_condenser |

Le chiavi sono una codifica di progetto delle identità, non nuove variabili misurate.
La condivisione del flusso 4 fra F1/F2/F8 non rende identici i tre interventi della tabella;
resta una sovrapposizione strutturale da dichiarare. Non si pretende indipendenza fisica delle
classi. Questa regola non definisce le coppie confondibili di D11 né la distinzione OOD.

## 3. Stratificazione esterna

Si congela lo strato **H = {F3, F9, F15}**, denominato «difficoltà di rilevazione documentata».
Il complemento nell'universo è **O**, «ordinario rispetto a questa stratificazione», non
«facile». L'appartenenza è nominale e fissata dalle fonti indicate nel piano §12, non ricalcolata
applicando una nuova soglia ai nostri dati o ai risultati del futuro modello.

Riscontro primario: Xiao, Kordon & Sen (PHM 2023), tabella 2, p. 6, e commento §4.3, p. 7.
I valori FDR (%) sono:

| Fault | DAE | T² | SPE |
| --- | ---: | ---: | ---: |
| F3 | 3,6 | 5,9 | 7,6 |
| F9 | 3,5 | 5,6 | 6,6 |
| F15 | 7,9 | 5,8 | 5,9 |

Gli autori li raggruppano come controllabili, difficili da rilevare nei metodi confrontati.
F4 resta in O: la stessa tabella riporta DAE/SPE 100% e T² 18%, quindi la difficoltà dipende
qui dal metodo. Questi sono risultati esterni di rilevazione, non previsioni di diagnosi FoT.

**Correzione al piano §12.2:** «FDR sotto il 10% in tutti i metodi» non è la definizione
adottata. I range attribuiti a Yin et al. (2012) in §12.1 arrivano a 24,25%, 23,5% e 29,88%.
Il piano era quindi internamente contraddittorio. Si conserva il gruppo esplicito e il criterio
qualitativo di difficoltà concorde nei confronti citati; non si alza opportunisticamente la soglia
al 30%. La classificazione è corroborata direttamente dalla PHM 2023.

**Limite della verifica bibliografica:** per Yin et al. sono stati verificati metadati e
abstract sulla pagina editoriale; il testo integrale e i range del piano non sono stati
riverificati su una copia primaria accessibile in questa sessione. Quei range restano attribuzioni
del piano e non entrano nel calcolo di ammissibilità. Non si afferma che tutti i metodi di tutta
la letteratura falliscano né che H sia intrinsecamente indistinguibile da Normal o al suo interno.

## 4. Vincoli di ammissibilità, in ordine

1. Il catalogo contiene **8 ID distinti**, inclusi i quattro di continuità. I nuovi ID sono
   quattro, scelti dall'universo restante, senza reinserimento.
2. Copertura strutturale: **almeno 2 step, 2 random variation, 2 sticking valve e 1 slow drift**.
   L'ottavo posto può aumentare una famiglia già coperta. È la scelta operativa di questa
   revisione: estende la copertura oltre una singola istanza per famiglia, con l'eccezione
   obbligatoria IDV(13) del piano rev. 6. Il risultato sul drift resta riferito a IDV(13);
   non si scelgono run aggiuntivi e non si chiude E5-C3.
3. Nessuna coppia con la stessa chiave di identità del §2: sono vietate **{3,9}, {4,11}, {5,12}**.
   La regola controlla la duplicazione della variabile perturbata, non la confondibilità empirica.
4. Il catalogo include **almeno 2 membri di H**. È l'adozione vincolante della raccomandazione
   D1, non una quota proporzionale alla popolazione. Nessun ordinamento per FDR dentro H o O.

Tutti i vincoli sono congiunti. La priorità non autorizza ad allentarne uno automaticamente:
se l'insieme ammissibile è vuoto, D1 si ferma e occorre una nuova revisione verificata prima di
aprire dati. Nessun rimpiazzo per scarso segnale, risultati negativi o prompt troppo lunghi.

**Conseguenze esplicite, prima del sorteggio:** la quota sticking include necessariamente
F14 e F15; H con il divieto {3,9} impone uno e uno solo fra F3 e F9. Queste inclusioni sono
conseguenze strutturali, non esiti casuali. Rimane variabile il resto: non si presenta la
procedura come un'estrazione libera di quattro fault. Il catalogo non viene estratto qui.

## 5. Procedura riproducibile di D1, da eseguire dopo il freeze

Si congela anche il criterio di spareggio, per eliminare la discrezionalità residua:

1. Enumerare le combinazioni crescenti di quattro ID fra gli undici non di continuità.
2. Aggiungere la continuità, filtrare con §4, ordinare le quadruple ammissibili
   lessicograficamente **come tuple di interi**. Nessun peso basato su risultati o FDR.
3. Se N è il numero di quadruple ammissibili, selezionare un indice uniforme tramite
   rejection sampling deterministico su SHA-256. Seed ASCII **`20260913`**, scelto dalla data
   della presente decisione; namespace ASCII **`studio2-fase03-D1-v1`**. Per c=0,1,… calcolare
   SHA-256 dei byte UTF-8 di `studio2-fase03-D1-v1|20260913|c`, con c decimale senza zeri
   iniziali. Interpretare i 32 byte come intero unsigned big-endian x. Sia
   L = 2^256 − (2^256 mod N). Accettare il primo x < L; indice zero-based = x mod N.
   Se N=0, arresto prima di qualsiasi hash. Non usare `hash()` del linguaggio.
4. Registrare lista ordinata completa, N, seed, contatore accettato, digest, indice,
   catalogo, conteggi di meccanismo/strato, commit e hash dei criteri. Nessun secondo seed,
   sorteggio di prova o rilancio per cambiare catalogo. Un replay deve riprodurre lo stesso esito.

È un sorteggio uniforme fra cataloghi ammissibili sotto l'interpretazione pseudo-casuale
del digest; non garantisce uguali probabilità marginali ai singoli fault o alle composizioni di
meccanismo. Le quote e i vincoli possono forzare inclusioni. Non è una stima rappresentativa
su tutti i fault TEP. Il seed è qui prespecificato; il digest e l'indice non sono stati calcolati.

## 6. Limiti e passaggi successivi

Downs & Vogel, nota alla tabella 8, raccomandano di usare le perturbazioni 14–20 insieme ad
altra perturbazione o cambio di setpoint e suggeriscono 24–48 ore per l'effetto completo.
La copertura tassonomica delle valvole non garantisce un segnale utile nel disegno a singolo
fault. Si registra il limite ora; non si aggiungono perturbazioni, non si cambia durata e non
si eliminano F14/F15 guardando il segnale. La specifica di generazione dovrà esplicitare come
il protocollo dello studio si rapporta a questa raccomandazione prima di generare i nuovi run.

Restano aperti D1 (catalogo effettivo), D2, D11, OOD, producer alternativo e gate reale 03.0.
Il freeze riguarda esclusivamente questi criteri; non è il congelamento generale di Fase 03,
non chiude S1 (che richiede anche il catalogo) e non autorizza inferenze o simulazioni.

## 7. Fonti e tracciabilità

- Piano autorevole: [`FoT_TEP_Review_Piano_Sperimentale.md`](../paper/FoT_TEP_Review_Piano_Sperimentale.md),
  §§0.1, 2.2, 6.1, D1, 8.12 e 12.1–12.4. Correzione del §12.2 registrata in questa revisione.
- Downs, J.J. & Vogel, E.F. (1993), *A plant-wide industrial process control problem*,
  Computers & Chemical Engineering 17(3), 245–255.
  [DOI](https://doi.org/10.1016/0098-1354(93)80018-I),
  [copia primaria consultata, tabella 8 p. 250](https://users.abo.fi/~khaggblo/RS/Downs.pdf).
- Yin, S., Ding, S.X., Haghani, A., Hao, H. & Zhang, P. (2012), *A comparison study of basic
  data-driven fault diagnosis and process monitoring methods on the benchmark Tennessee Eastman
  process*, Journal of Process Control 22(9), 1567–1581.
  [Pagina editoriale](https://www.sciencedirect.com/science/article/pii/S0959152412001503),
  [DOI](https://doi.org/10.1016/j.jprocont.2012.06.009). Limite d'accesso al §3.
- Xiao, Z., Kordon, A. & Sen, S. (2023), *Fault Detection and Diagnosis in Tennessee Eastman
  Process with Deep Autoencoder*, Annual Conference of the PHM Society 15(1).
  [Pagina e DOI](https://papers.phmsociety.org/index.php/phmconf/article/view/3578),
  [testo primario, tabella 2 pp. 6–7](https://papers.phmsociety.org/index.php/phmconf/article/download/3578/phmc_23_3578).

Non è stata importata una nuova raccolta bibliografica: questi sono i riferimenti metodologici
già prescritti dal piano §12. I PDF sono stati consultati esternamente, senza copie nel corpus.
