OK

# Verifica indipendente — criteri di selezione §6.1, Fase 03

Data: **2026-09-13**. Verificatore: **Codex**; modello richiesto per il sottoagente dal tool:
**gpt-5.6-sol**; autoidentificazione disponibile nel contesto: **GPT-5**. Agente/finestra separata
`/root/verifica_criteri`, diversa dalla finestra autrice dichiarata nel report (**Codex,
GPT-6**). Oggetto limitato alla sotto-fase §6.1: non è un audit completo del capability pilot,
della Fase 03 o del protocollo sperimentale generale.

Non è stato eseguito D1: non sono stati calcolati digest, contatore, indice o catalogo e non sono
stati aperti risultati per-fault dei nostri esperimenti.

## 1. Perimetro, fonti autorevoli e cronologia

| Esito | Riscontro |
| :---: | --- |
| ✅ | Il report richiesto esiste in `studio2/fase03/selection/REPORT_CRITERI_6_1.md`. La verifica è stata ricostruita dalle fonti e dagli artefatti citati, non assunta dal report. |
| ✅ | Le precedenze sono rispettate: per questa sezione ancora vuota del walkthrough la fonte del disegno è `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`; il nuovo registro è collegato dal piano in §6.1 e la correzione è registrata in §12.2. Non è stato usato `FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md`. |
| ✅ | L'HEAD di partenza della sotto-fase è `6a02927`, discendente da `c6e19d6` mediante **13 commit**, tutti con prefisso `studio2(fase03)`. Prima della presente verifica lo stato mostrava soltanto la modifica al piano e i nuovi file dichiarati della selezione; nessun file del pilot ereditato e nessun artefatto congelato risultavano modificati rispetto a `6a02927`. `studio2/PROVENIENZA.md` è invariato. |
| ⚠️ | L'affermazione del report secondo cui il checkout iniziale fosse `main`, pulito e allineato a `origin/main`, è uno stato storico non attestato da un record della sotto-fase e non è ricostruibile dal solo worktree corrente. L'ascendenza e lo stato attuale sono invece verificabili. Il limite non incide sui criteri. |
| ✅ | La collocazione del registro sotto `docs/lit_review/` è coerente con la precedenza specifica del walkthrough §0.1, che indica i registri di decisione in quella sede. Resta una tensione lessicale con `MAINTENANCE.md` §1, che descrive la cartella come riservata ad analisi e rassegne, ma il contratto §8.1 e il walkthrough nominano espressamente registri di decisione fuori da `studio2/`; non si crea qui una fonte concorrente sotto `studio2/`. |

## 2. Fonte primaria Downs & Vogel (1993)

| Esito | Riscontro |
| :---: | --- |
| ✅ | La copia è stata riscaricata indipendentemente dall'URL registrato. Dimensione **972.988 byte** e SHA-256 `5f19b0bf7f0e5c052335943fff263769a28757066582c3166e16ac163e0e9538` coincidono con `SOURCE_CHECK.json`. |
| ✅ | La tabella 8, p. 250, conferma esattamente l'universo strutturale usato: IDV(1)–IDV(7) step, IDV(8)–IDV(12) random variation, IDV(13) **slow drift**, IDV(14)–IDV(15) sticking; IDV(16)–IDV(20) hanno variabile e tipo unknown. |
| ✅ | Le descrizioni delle variabili e le tre identità duplicate vietate, `{3,9}`, `{4,11}`, `{5,12}`, sono direttamente riscontrabili nella tabella. F1/F2/F8 condividono il flusso 4 ma descrivono interventi compositivi diversi; trattarli come sovrapposti ma non identici è una scelta dichiarata e compatibile col testo della fonte. |
| ✅ | La nota sotto la tabella dice che le perturbazioni 14–20 dovrebbero essere usate con un'altra perturbazione della tabella o con un cambio di setpoint e raccomanda **24–48 h** per realizzarne l'effetto completo. Il registro riporta entrambe le condizioni e non le trasforma in prova di segnale utile nel disegno a singolo fault. |

Fonte primaria: Downs, J.J. e Vogel, E.F. (1993), *A plant-wide industrial process control
problem*, tabella 8 e nota, p. 250, DOI `10.1016/0098-1354(93)80018-I`; copia consultata:
<https://users.abo.fi/~khaggblo/RS/Downs.pdf>.

## 3. Fonte primaria PHM 2023 e limite Yin 2012

| Esito | Riscontro |
| :---: | --- |
| ✅ | La copia PHM è stata riscaricata indipendentemente dall'URL registrato. Dimensione **721.381 byte** e SHA-256 `e11310c44cebca7a6ebc368b3862dc2edc0003a4ee31cb9223feb6d5e0ae7b78` coincidono con `SOURCE_CHECK.json`. Titolo, autori, anno, venue e DOI sono confermati anche dalla pagina della PHM Society. |
| ✅ | La tabella 2, p. 6, conferma tutti i nove numeri del registro: F3 = 3,6/5,9/7,6; F9 = 3,5/5,6/6,6; F15 = 7,9/5,8/5,9 per DAE/T²/SPE. Conferma inoltre F4 = 100/18/100. |
| ✅ | Il commento a p. 7 chiama F3, F9 e F15 `controllable faults`, li qualifica `hard-to-detect` e afferma che nessuno dei tre metodi produce risultati soddisfacenti. Distingue F4, F5 e F7 come `back-to-control faults`; per essi DAE raggiunge 100% FDR. Il gruppo nominale H={F3,F9,F15} e l'esclusione di F4 sono quindi sostenuti direttamente dalla fonte primaria verificata. |
| ✅ | Il registro conserva correttamente la distinzione fra rilevazione fault-vs-Normal e diagnosi fault-vs-fault. Non usa gli FDR esterni per predire accuratezza, evidence o separabilità del futuro FoT. |
| ⚠️ | Del lavoro Yin et al. (2012) sono verificabili metadati bibliografici e abstract, ma in questa verifica non è disponibile il testo integrale primario. I range 4,5–24,25%, 0,88–23,5% e 7,75–29,88% e la frase attribuita agli autori non ricevono quindi un secondo riscontro sul full text. Il registro lo dichiara e non usa quei valori come filtro numerico. La formula `concorde nei confronti citati` resta più forte di quanto questa sola verifica possa attestare; il nucleo operativo H è però sostenuto autonomamente dalla tabella e dal commento PHM primari. |

Fonte primaria verificata: Xiao, Z., Kordon, A. e Sen, S. (2023), *Fault Detection and Diagnosis
in Tennessee Eastman Process with Deep Autoencoder*, tabella 2 pp. 6–7 e §4.3 p. 7, DOI
`10.36001/phmconf.2023.v15i1.3578`, <https://papers.phmsociety.org/index.php/phmconf/article/view/3578>.

## 4. Coerenza scientifica dei criteri e discrezionalità residua

| Esito | Riscontro |
| :---: | --- |
| ✅ | I criteri appartengono alle famiglie ammesse dal piano D1/§6.1: meccanismo e identità dalla tassonomia esterna, più difficoltà documentata esternamente. Non compaiono separabilità, score o prestazioni dei dati propri. |
| ✅ | I quattro fault F1/F8/F10/F13 sono mantenuti esplicitamente come continuità e non presentati come campione casuale o rappresentativo. IDV(13) resta l'unica istanza di drift e il registro limita il relativo risultato a IDV(13). |
| ✅ | La quota `almeno 2` per step, random variation e sticking, con `almeno 1` slow drift, è una scelta di progetto esplicita. Garantisce almeno due istanze per ogni famiglia che ne possiede due nell'universo e rende visibile l'eccezione strutturale del drift. Non è attribuita a Downs, PHM o Yin. |
| ⚠️ | La quota due, la quota H≥2, l'universo ristretto a IDV(1)–IDV(15), l'equivalenza per chiave esatta e il seed basato sulla data sono decisioni discrezionali di progetto. Il freeze le protegge dalla selezione outcome-dependent, ma non le rende uniche o derivate dalla letteratura. Due istanze per meccanismo non forniscono da sole generalizzabilità al meccanismo né potenza inferenziale; questo limite deve restare esplicito nella documentazione e nell'interpretazione. |
| ✅ | Le conseguenze dei vincoli sono dichiarate prima del sorteggio: F14 e F15 sono forzati; la quota H e il divieto `{3,9}` impongono esattamente uno fra F3 e F9. Il registro non presenta quindi D1 come estrazione libera dei quattro nuovi fault. |
| ⚠️ | Forzare entrambi gli sticking concentra due degli otto posti proprio sui fault coperti dalla nota prudenziale di Downs. La scelta resta tecnicamente fattibile e trova un precedente esterno nella PHM, che valuta F14 e F15, ma la copertura tassonomica non garantisce segnale utile. Prima di generare run la specifica successiva deve stabilire e registrare il rapporto fra protocollo a singolo fault, istante di iniezione/durata e raccomandazione Downs. Il registro già pone questo passaggio come obbligatorio; non va risolto dopo aver osservato il segnale. |

## 5. Fattibilità combinatoria e procedura D1

| Esito | Riscontro |
| :---: | --- |
| ✅ | Un'enumerazione indipendente dei soli attributi strutturali, senza SHA-256 del sorteggio, conferma `C(11,4) = 330` quadruple candidate e **12** quadruple ammissibili. |
| ✅ | Le composizioni confermate sono **5** cataloghi con step/random/drift/sticking = **3/2/1/2** e **7** con **2/3/1/2**. Tutte forzano F14 e F15. I valori di `FEASIBILITY.json` sono corretti. |
| ✅ | L'insieme ammissibile non è vuoto, perciò D1 è eseguibile senza revisione dei criteri. Nessun catalogo è stato selezionato durante questa verifica. |
| ✅ | Enumerazione delle combinazioni crescenti, ordinamento lessicografico come tuple di interi, codifica ASCII/UTF-8 del namespace-seed-contatore, interpretazione unsigned big-endian e rejection sampling con `L = 2^256 - (2^256 mod N)` definiscono una procedura non ambigua e priva di bias modulo, assumendo SHA-256 come sorgente pseudocasuale. |
| ⚠️ | Un seed pubblico già fissato rende il risultato matematicamente calcolabile da chiunque prima del passo formale D1. Il commit/freeze prova la precedenza dei criteri rispetto ai risultati futuri, ma non può provare che nessuna persona abbia calcolato privatamente il digest prima del commit. È un limite di audit, già riconosciuto dal registro quando distingue operazioni attestabili e stato cognitivo. La procedura resta riproducibile e vieta rilanci. |

## 6. Assenza di contaminazione e riuso

| Esito | Riscontro |
| :---: | --- |
| ✅ | `FEASIBILITY.json` contiene solo conteggi combinatori e dichiara `draw_executed=false`, `catalog_selected=false`, `scientific_data_opened=false`, `model_calls=0`. La riproduzione indipendente ha usato esclusivamente la tassonomia e i vincoli. |
| ✅ | Nessun risultato proprio per fault è necessario per ricavare universo, H, duplicati, quote o ammissibilità. La sonda sintetica 03.0 è espressamente esclusa dalle fonti dei criteri. |
| ✅ | I criteri non riusano dati o risultati del primo studio. La continuità F1/F8/F10/F13 è una decisione dichiarata dal piano; non è trattata come nuova evidenza e non richiede una nuova riga dati in `PROVENIENZA.md`. Il registro di provenienza resta invariato. |
| ⚠️ | L'assenza assoluta di consultazioni non registrate non è dimostrabile dal repository. È verificabile che gli artefatti e le giustificazioni della sotto-fase non dipendono da risultati propri e che lo stato corrente non modifica tali risultati. |

## 7. Coerenza del report, link e test

| Esito | Riscontro |
| :---: | --- |
| ✅ | Le affermazioni numeriche centrali di `REPORT_CRITERI_6_1.md` su fonti, conteggi e composizioni sono confermate. D1, D2, D11, OOD, producer alternativo, dati reali del pilot e gate 40×3 restano aperti; questa verifica non li chiude. |
| ✅ | I percorsi relativi dal registro verso il piano e i quattro artefatti della selezione esistono. Gli URL dei due PDF sono raggiungibili e restituiscono esattamente i byte registrati. |
| ✅ | `python3 docs/test_explanation.py` esegue **35 test**, con **14 fallimenti e 1 skipped**, come dichiarato. I fallimenti sono nel materiale preesistente e il test non copre direttamente questa sotto-fase. |
| ✅ | `git diff --check` non segnala errori di whitespace nella modifica tracciata al piano. Non esiste ancora una coppia walkthrough modificata da controllare: l'aggiornamento documentale è correttamente successivo a questo verdetto. |

## 8. Verdetto

**OK — i criteri §6.1 reggono e si può procedere all'aggiornamento della documentazione e al
congelamento dedicato prima di D1.**

L'OK riguarda la prespecificazione e la fattibilità del criterio, non la rappresentatività del
catalogo futuro, la validità dei run sticking, il successo del gate, la potenza statistica o la
chiusura della Fase 03. Restano da mantenere come limiti: Yin senza secondo riscontro sul testo
integrale; quote discrezionali e non bibliografiche; nessuna generalizzazione da due fault a un
intero meccanismo; verifica della raccomandazione Downs nella specifica di generazione prima dei
run; impossibilità di attestare lo stato cognitivo pre-commit.
