# Verifica della rilevabilità IDV(6)/IDV(4) — supporto bibliografico Fase 03

Data: **2026-09-14**. Finestra: **Letteratura_LLM, Codex**. Stato: **analisi e addendum bibliografico, non decisione sperimentale**. Nessuna firma di 03.8 presunta.

## 1. Esito per 03.8

- **IDV(6): condizione bibliografica minima soddisfatta dalla PHM 2023.** Tabella 2, p. 6: fault detection rate **DAE 100%, PCA–T² 99%, PCA–SPE 100%**. È sostenibile “rilevato dai tre rivelatori confrontati nella PHM, con FDR 99–100%”; non “100% in tutti”, non “da tutti i metodi della letteratura”, non la stessa attribuzione a Yin senza leggerne le tabelle.
- **IDV(4): condizione di numero primario documentato soddisfatta.** La stessa tabella conferma **DAE 100%, PCA–T² 18%, PCA–SPE 100%**. La prestazione dipende dal rivelatore: una rilevabilità uniformemente alta è **contraddetta** da T². F4 resta nel complemento O della stratificazione congelata; O non significa facile.
- **Yin (2012): verifica numerica non completabile con le copie accessibili trovate.** Identità e abstract verificati, nessuna tabella primaria letta. La PHM basta separatamente per documentare numeri esterni; non basta a confermare un consenso fra le due pubblicazioni o a prevedere la prestazione FoT.

La sufficienza sopra riguarda **solo la presenza di un numero di rilevabilità esterno verificato**, richiesta dalla proposta §8.2 di 03.8. Non introduce una soglia universale di FDR, non seleziona OOD/sostituti e non verifica la generabilità di F6. Restano all’autore l’interpretazione di distinzione meccanica, la scelta OOD e l’accettazione dei limiti; 03.11 gestisce la verifica tecnica di generabilità nel proprio perimetro.

## 2. Provenienza interna e addendum al registro congelato

Worktree creato, dopo `git fetch origin`, da `origin/main` **a572d1c**, su `codex/studio2-letteratura-fase03`, in `/Users/luker/fot-tep-letteratura-fase03`. La copia principale non ha cambiato branch. Il lavoro non comprende commit, push, merge o tag.

La base letta per il **piano statistico** è il file effettivo nel worktree `/Users/luker/fot-tep-piano-statistico-fix`, HEAD **dd82cd1** con **otto modifiche tracciate non committate** osservate all’apertura. `PIANO_STATISTICO.md` misura **63602 byte**, SHA-256 `3326e992995114f92b20117cd4b4575f6c2e7ba1758fee4463461448f010fba6`. Sono stati letti §8, §§15–17 e passaggi su ipotesi/test/metodi necessari alla verifica bibliografica. La revisione 7 del **piano generale**, già in main a572d1c, è un documento distinto dalla revisione 7 del **piano statistico** nel worktree fix. Nessun file di quel worktree è stato modificato.

Questo documento costituisce l’**addendum separato** a [DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md](DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md), in particolare §§2–3. Non è una nuova revisione normativa. Tag effettivo: **`studio2-fase03-criteri-selezione-frozen-001`**, commit `9faecaf7337e5864b7a3ad44cadb8971853dd260`. Il tag D1 è **`studio2-fase03-catalogo-D1-frozen-001`**, commit `ab43f0b20f45cdb475c0caf52c6f7afcbae50891`.

Il manifest [CRITERIA_FREEZE.json](../../studio2/fase03/selection/CRITERIA_FREEZE.json) e la sua rev002 distinguono:

| File / ruolo | Impronta congelata / trattamento |
| --- | --- |
| Registro normativo dei criteri | SHA-256 `d58a7606d69a560a626da44833c065ddbf1aa395ae8b2e523262daf8622231c7`, 11339 byte: preservato |
| `selection/SOURCE_CHECK.json` | `82c654d142ac0ab13f9b47d9648231bd3f1bfda4c5486a8399f510ff87165372`, 747 byte: record di verifica storico preservato |
| `selection/FEASIBILITY.json` | `ca830d054af19e27aa191fcb51f8e80d3c8444bb746dd9da486304490bd59810`, 504 byte: preservato |
| Piano generale, snapshot di riferimento | Verificabile al source commit `9d0e1911afd6c244f748f05f62934590f5314794`, SHA-256 `7f9462c28eef7bc0cf74e201a1ffe283d68056359728fea62740e43a1bb1767a`; il manifest non congela per sempre l’intero piano vivente. Non modificato qui |
| Manifest, rapporti, verbali e catalogo D1 in `selection/` | Intera cartella preservata; confronto prima/dopo su 22 file, più registro = 23 impronte |

**Invarianti:** H={F3,F9,F15}; catalogo D1={F1,F2,F3,F8,F10,F13,F14,F15}; nessun nuovo criterio o riclassificazione. Il riferimento di integrità machine-readable è [VERIFICA_FONTI_FASE03.json](VERIFICA_FONTI_FASE03.json), che è evidenza bibliografica, non un freeze manifest.

**Discrepanza emersa sul registro, senza modificarlo.** Tabella 2 PHM, p. 6, riga **SPE**, colonna **9**, mostra **5,6%**; il registro §3 riporta **6,6%**. La copia è identica al precedente SOURCE_CHECK: è una discrepanza di trascrizione, non una nuova versione del paper. Questa rettifica bibliografica vale nell’addendum; non riscrive il registro, non altera H e non accredita una nuova soglia. Anche l’OK storico del verbale 6.1 resta intatto, con questo limite ora documentato.

## 3. Identificazione e integrità PHM

Zhongying Xiao, Arthur Kordon, Subrata Sen (2023), *Fault Detection and Diagnosis in Tennessee Eastman Process with Deep Autoencoder*, **Annual Conference of the PHM Society 15(1)**, pubblicato **26 ottobre 2023**, sezione editoriale *Industry Experience Papers*. DOI [10.36001/phmconf.2023.v15i1.3578](https://doi.org/10.36001/phmconf.2023.v15i1.3578). Metadati verificati su **Crossref e pagina dell’editore**; titolo e autori confermati sul frontespizio.

[Copia primaria PHM](https://papers.phmsociety.org/index.php/phmconf/article/download/3578/phmc_23_3578), **10 pagine PDF**, **721381 byte**, SHA-256 **`e11310c44cebca7a6ebc368b3862dc2edc0003a4ee31cb9223feb6d5e0ae7b78`**. Byte e impronta coincidono esattamente con SOURCE_CHECK. Conservata in `papers/` in una sola copia PDF/MD, con rendering delle pagine 6–7 per rilettura della verifica.

I metadati tecnici interni del PDF sono residui di template: titolo **“Sample Paper”**, autore **“Brice Carnahan - U. Michigan”**, subject **“CACHE Documentation Standards”**, creator Microsoft Word; creation/modification **2023-10-25 05:02:41 UTC**. Non sono la citazione bibliografica. Non è stata inferita una sostituzione di versione da questi campi: frontespizio, landing page e hash concordano con la copia registrata.

## 4. Tabella delle evidenze numeriche

**Orientamento verificato visivamente:** i fault sono **colonne**, non righe; i rivelatori sono righe **DAE, T², SPE**. Le intestazioni raggruppano F4 sotto *Back to control Faults* e F6 sotto *Uncontrollable Faults*. I metodi pertinenti sono tutti e tre quelli riportati: DAE e due statistiche della stessa PCA, non tre famiglie algoritmiche indipendenti. Tabelle 2/3/4 sulla medesima **p. 6**, senza note di riga che alterino F4/F6. La pagina 7 spiega metriche e interpretazione.

Tutti i numeri sotto provengono dalla stessa pubblicazione/versione identificata al §3 e condividono le condizioni del §5. Le celle non sono ricalcolate o arrotondate diversamente dalla stampa.

| Fault / colonna primaria | Riga / metodo | Tab. 2, FDR (%) | Tab. 3, FAR (%) | Tab. 4, ritardo FDD (min) |
| --- | --- | ---: | ---: | ---: |
| IDV(6), intestazione `6` | DAE | 100 | 0,6 | 0 |
| IDV(6), intestazione `6` | T² (PCA) | 99 | 1,3 | 24 |
| IDV(6), intestazione `6` | SPE (PCA) | 100 | 0,6 | 0 |
| IDV(4), intestazione `4` | DAE | 100 | 3,1 | 0 |
| IDV(4), intestazione `4` | T² (PCA) | 18 | 1,9 | 0 |
| IDV(4), intestazione `4` | SPE (PCA) | 100 | 5 | 0 |

La tabella conserva anche FAR e ritardi per evitare una selezione dei soli FDR favorevoli. **Ritardo zero non implica rilevazione sostenuta:** F4/T² ha ritardo zero e FDR 18%. F6/T² ha FDR 99% e ritardo 24 minuti. Non sono contraddizioni: misurano aspetti diversi.

## 5. Condizioni e significato delle metriche

- §3, p. 4: 21 condizioni di guasto; per ciascun caso gli autori descrivono dati di training solo Normal e test Normal+fault, **960 osservazioni** ciascuno, **52 variabili**, prime **160** osservazioni Normal. Il testo p. 4 dice “after the 161st observation”; p. 7 situa l’innesco al campione 161 per F5. Non si trasforma questa lieve ambiguità in una certezza sull’implementazione degli indici o sui denominatori esatti dei dati grezzi.
- §§4.1–4.2, pp. 4–5: DAE dinamico ottimizzato con **5 strati**, finestra di **3 campioni**, input **156** valori, attivazione **PReLU**, loss **MSE**; architetture valutate dagli autori sul loro dataset. §4.3, p. 6: PCA con **9 componenti**, T² e SPE sullo stesso training/test del DAE.
- §4.3, p. 7, formule controllate visivamente: **FDR = fault detection rate**, rapporto fra fault correttamente rilevati e totale dei fault, ×100. È una sensibilità di rilevazione nella serie sotto guasto; **non false discovery rate**, né accuratezza di classificazione del tipo di fault. FAR è il rapporto fra falsi allarmi e totale Normal, ×100. Il paper non fornisce intervalli di confidenza per le celle.
- Tabella 4 definisce l’unità del ritardo in **minuti**. Non si deduce un periodo di campionamento dai multipli della tabella: il periodo non è esplicitato nei passaggi testuali consultati. Soglie/nominal FAR e dettagli sufficienti a riprodurre ogni cella non sono specificati nei passaggi letti; non vengono inventati. Non abbiamo riaddestrato alcun metodo né riprodotto il benchmark.
- Queste sono prestazioni esterne di **rilevazione**, condizionate a dataset, modello, controllo e soglie di quel confronto. La selezione di variabili a fini di root-cause analysis non è una matrice di diagnosi multi-classe. Nessuna tabella verifica la **generabilità** su 40 h post-innesco del nostro generatore o la riuscita della **diagnosi FoT**.

Il commento p. 7 sostiene la difficoltà dei controllabili F3/F9/F15 e discute DAE e confronto PCA; la lettura dei numeri prevale su generalizzazioni retoriche del commento. La frase “F6 rilevato dai tre rivelatori” è una sintesi della riga/colonna effettivamente controllata, non una citazione letterale degli autori.

## 6. Yin et al. (2012): ricerca primaria e limite

Opera esatta: **Shen Yin, Steven X. Ding, Adel Haghani, Haiyang Hao, Ping Zhang**, *A comparison study of basic data-driven fault diagnosis and process monitoring methods on the benchmark Tennessee Eastman process*, **Journal of Process Control 22(9), 1567–1581**, ottobre 2012, [DOI 10.1016/j.jprocont.2012.06.009](https://doi.org/10.1016/j.jprocont.2012.06.009). Identità ricavata dal registro e confermata su Crossref, non completata a memoria.

| Via cercata | Esito osservato il 2026-09-14 |
| --- | --- |
| [Pagina editoriale Elsevier](https://www.sciencedirect.com/science/article/pii/S0959152412001503) e ricerca del titolo esatto con PDF | Metadati e abstract; nessuna tabella del testo integrale letta |
| API editoriale indicata da Crossref, `api.elsevier.com/content/article/PII:S0959152412001503?httpAccept=text/xml` | Risposta XML di 1887 byte con dati bibliografici; il nome `full-text-retrieval-response` non prova disponibilità del corpo integrale |
| [OpenAlex W1970537494](https://openalex.org/W1970537494), record DOI | `is_oa=false`, `oa_status=closed`, `any_repository_has_fulltext=false`; nessun `pdf_url`. È lo stato del catalogo, non prova di inesistenza globale |
| [Bibliografia istituzionale Duisburg-Essen, ubo_mods_00045484](https://bibliographie.ub.uni-due.de/receive/ubo_mods_00045484), identificata da OpenAlex | Scheda istituzionale rintracciata; accesso diretto restituisce Security Check. Non aggirato, nessun PDF ottenuto |
| Pagine di autori/indici emerse dalla ricerca del titolo | ResearchGate offre richiesta del testo, non una copia primaria letta; nessun contatto inviato agli autori |

Nessuno snippet, lavoro successivo o citazione indiretta è stato promosso a riscontro numerico. I range di F3/F9/F15 e la frase sui metodi di Yin restano **non verificati**, non “falsi”. Non è stata aggiunta una conversione MD fittizia. **PHM da sola soddisfa la verifica di presenza dei numeri F6/F4**, con i limiti del §5; non eredita l’ampiezza dei metodi di Yin.

## 7. Nove riferimenti assegnati: stato e attribuzioni

Le opere sono quelle di §17 del piano statistico effettivo e, per McMahan, della voce già esistente in §14.3/§14.7 del corpus. Metadati e disponibilità sono registrati anche in `papers/README.md`; le schede vivono soltanto nel corpus MD/HTML. Tutti sono 🟢 perché incidono su scelte o delimitano attribuzioni, **anche dove la verifica del full text resta incompleta**: il colore non è una certificazione di accesso.

| Riferimento | Verifica eseguita / disponibilità | Conseguenza bibliografica |
| --- | --- | --- |
| Toshiro Tango, 1998 — *Equivalence test and confidence interval for the difference in proportions for the paired-sample design* | Crossref e PubMed PMID 9595618. Testo primario §§2–4, pp. 892–897; caso nullo discordante eq. (29) p. 896. PDF e MD acquisiti. | Il margine aggregato non garantisce non inferiorità per agente. 03.8 deve giustificare il modello di coppie rispetto agli strati: indipendenza da sola non dimostra tutte le ipotesi di Tango. La gerarchia eredita l’approssimazione di H3. |
| W. Maurer, L. A. Hothorn e W. Lehmacher, 1995 — *Multiple comparisons in drug clinical trials and preclinical assays: a-priori ordered hypotheses* | DNB 944101399, frontespizio e indice primari. Frontespizio e indice primari nel catalogo DNB (3 pagine); voce nel CV pubblico di L. A. Hothorn; non il capitolo. PDF/MD integrali assenti, dichiarati. | La presenza bibliografica è verificata; la verifica sostanziale del capitolo resta aperta. La garanzia della sequenza fissa è dimostrata separatamente nell’analisi e non dipende dall’attribuzione non verificata. |
| Peter H. Westfall e Alok Krishen, 2001 — *Optimally weighted, fixed sequence and gatekeeper multiple testing procedures* | Crossref e pagina Elsevier. Abstract, introduzione e sezioni esposte nell’anteprima editoriale; PDF integrale non acquisito. PDF/MD integrali assenti, dichiarati. | Con test locali validi per tutta la rispettiva nulla e arresto al primo mancato rifiuto, la sequenza controlla fortemente FWER senza richiedere indipendenza fra test. Non ripara test locali invalidi o approssimati; la prova elementare è nell’analisi, distinta dall’anteprima letta. |
| C. J. Clopper ed E. S. Pearson, 1934 — *The use of confidence or fiducial limits illustrated in the case of the binomial* | Crossref e OUP. Testo primario pp. 404–408, in particolare pp. 406–407 sulla copertura almeno nominale. PDF e MD acquisiti. | Definire unità Bernoulli indipendenti e probabilità comune prima di chiamare esatto l’intervallo. Un intervallo su risposte correlate di più agenti non è reso esatto dal solo uso di Clopper–Pearson. |
| Leslie Kish, 1965 — *Survey Sampling* | Google Books; Open Library OL5947497M; Wiley per la sola ristampa. Cataloghi Google Books/Open Library e descrizione editoriale della ristampa 1995; testo 1965 non acquisito. PDF/MD integrali assenti, dichiarati. | Nell’analisi si deriva separatamente la formula per cluster equidimensionali, varianza comune e correlazione intra-cluster comune. È un’approssimazione di scenario, non una garanzia per il nostro disegno né un’attribuzione pagina-per-pagina a Kish. |
| International Conference on Harmonisation (ICH), 1998 — *Statistical Principles for Clinical Trials* | EMA/FDA, fonti ufficiali; nessun DOI attribuito. Testo ufficiale §§3.3.2 (pp. 17–18), 5.5 (pp. 27–28), 5.6 (p. 28), frontespizio. PDF e MD acquisiti. | 0,025 segue dalla convenzione quando il bilaterale è 0,05; E9 non prescrive 0,05 unilaterale per FoT e non sceglie m=0,125. Entrambe le decisioni restano all’autore, motivate sul dominio. |
| Wassily Hoeffding, 1963 — *Probability Inequalities for Sums of Bounded Random Variables* | Crossref e pagina Taylor & Francis; copia della rivista, non mimeo 1962. Testo primario §§1–2, pp. 13–16; teorema 1 eq. (2.3), teorema 2 eq. (2.6); controllo visivo pp. 14–16. PDF e MD acquisiti. | Con nulla E(media D)≤0 e N prefissato, t=√(2 log(1/α)/N) fornisce livello ≤α. Sono deduzioni algebriche dalla fonte, non simulazioni. Non giustifica MDE o potenza approssimata, né validità se cluster dipendono o sono selezionati sui risultati. |
| R. R. Bahadur e Leonard J. Savage, 1956 — *The Nonexistence of Certain Statistical Procedures in Nonparametric Problems* | Crossref, JSTOR e repository IAS; iniziali non espanse senza verifica. Testo primario §2, pp. 1115–1118; ipotesi (i)–(iii), teorema 1 e corollario 1; controllo visivo pp. 1115–1116. PDF e MD acquisiti. | Corretta la non applicabilità a H1/H2 limitate, ma è impreciso motivarla con “riguarda famiglie con code non limitate” senza distinguere limite comune e supporto individuale. La fonte non invalida tutti i test non parametrici della media e non dimostra la validità del sign-flip. |
| Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson e Blaise Aguera y Arcas, 2017 — *Communication-Efficient Learning of Deep Networks from Decentralized Data* | Catalogo PMLR e atti AISTATS 2017. Testo primario §2 e algoritmo 1, p. 1277 (PDF p. 5), discussione privacy e limiti. PDF e MD acquisiti. | La mancata condivisione dei dati grezzi non è una garanzia formale di privacy; il confronto empirico su altri dati non predice prestazioni FoT o FedAvg sul nostro TEP. |

**Tre precisazioni verificabili senza esperimenti.**

1. **Sequenza fissa:** sia j la prima ipotesi vera nell’ordine prefissato. Per commettere almeno un falso rifiuto bisogna rifiutare H_j, dunque FWER ≤ P(rifiutare H_j) ≤ α se il test locale ha livello uniforme ≤α su tutta la sua nulla e si arresta al primo mancato rifiuto. Questa è una **dimostrazione elementare qui esplicitata**, non una frase attribuita al capitolo Maurer non letto. Non richiede indipendenza fra test; richiede l’ordine e l’arresto. Con Tango approssimato il controllo esatto dell’intera gerarchia non segue.
2. **Hoeffding:** dal teorema 2, p. 16, eq. (2.6), intervalli [−1,1] danno somma delle ampiezze quadrate 4N e coda ≤exp(−Nt²/2). Sotto E(media D)≤0, t=√(2 log(1/α)/N) limita l’errore di primo tipo a α. L’indipendenza è fra D_c; non è richiesta identica distribuzione. Non è una dimostrazione di potenza/MDE o dell’indipendenza effettiva dei nostri cluster.
3. **Effetto di disegno:** con cluster di k osservazioni di varianza σ² e covarianza intra-cluster comune ρσ², Var(media del cluster)=σ²[1+(k−1)ρ]/k. Il rapporto rispetto a k osservazioni indipendenti è 1+(k−1)ρ. Questa è una **derivazione algebrica di scenario**, non la certificazione di una pagina non consultata di Kish. Dimensioni/pesi/covarianze diversi richiedono il calcolo appropriato.

**Punti che 03.8 deve interpretare:** il modello IID/multinomiale di Tango non è automaticamente giustificato dalla sola indipendenza di coppie campionate a quote fisse per fault; gli intervalli Clopper–Pearson non sono automaticamente esatti su risposte correlate o su una miscela di probabilità eterogenee. Sono limiti di applicabilità da giustificare, non una modifica del piano o un nuovo verdetto indipendente su 03.8.

**Bahadur–Savage:** pp. 1115–1117, §2, ipotesi (i)–(iii), teorema 1 e corollario 1. La ragione precisa della non applicabilità a una famiglia su [−1,1] è l’assenza della ricchezza richiesta (ogni media reale), non l’obbligo di code illimitate per ogni distribuzione. L’enunciato include famiglie di distribuzioni individualmente a supporto limitato o finito. Il piano `-fix` non è stato corretto qui: la formulazione più precisa è consegnata all’autore.

**Versioni e metadati non intercambiabili:** Hoeffding qui è la rivista 1963, non il mimeo 1962 trovato nel catalogo NCSU; ICH è E9 1998, copia EMA con impaginazione 2006, non E9(R1); Kish è il volume 1965, non la ristampa 1995. Maurer è un capitolo, non un articolo di rivista: indice DNB e CV dell’autore Hothorn corroborano pp. 3–18 (altre citazioni riportano 3–21). DOI non trovato per quel capitolo e per Kish; non attribuiti DOI di recensioni. PMLR non espone un DOI per gli atti FedAvg, quindi si usa l’URL degli atti, non il DOI del preprint come se fosse quello della conferenza.

## 8. Copie primarie conservate e impronte

| Copia in `papers/` | Byte | Pagine PDF | SHA-256 |
| --- | ---: | ---: | --- |
| [Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.pdf](../../papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.pdf) | 721381 | 10 | `e11310c44cebca7a6ebc368b3862dc2edc0003a4ee31cb9223feb6d5e0ae7b78` |
| [Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.pdf](../../papers/Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.pdf) | 257783 | 18 | `71dea8eddc08c73f15e2454d69b7f46d8bfa61b550c6246173fdfa4307df7ecd` |
| [The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.pdf](../../papers/The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.pdf) | 489367 | 11 | `e49da40d3fc184d591ec87681f30eae8077a2fb57b27850856207f54a7116e39` |
| [Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.pdf](../../papers/Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.pdf) | 332364 | 37 | `6dd74185bb88a6f48a4b3a154893f9d8953b2fa4784c56fedda102e45f410b96` |
| [Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.pdf](../../papers/Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.pdf) | 1451039 | 19 | `3021bcc097ef23a99a84d0eef8dcce2fd835c71df79a105727d3e03f8f0b8930` |
| [The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.pdf](../../papers/The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.pdf) | 760570 | 8 | `cc3d6d5b43fa3b136daae5db8831fac12b0e1cbb17326d8087302ffc5139caca` |
| [Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.pdf](../../papers/Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.pdf) | 763853 | 10 | `a7a8e2e3e437855c1efb53fe8f35f645eae7735fe9b6ac1f656a62004dbf5146` |

Ogni PDF ha un MD integrale per ricerca testuale. Hoeffding e Bahadur–Savage sono scansioni senza strato testuale utile: è stato prodotto OCR locale, dichiarato come **non affidabile per formule**, con enunciati pertinenti verificati sul rendering. Anche l’estrazione degli altri PDF può perdere formule/figure: il PDF prevale. Nessuna immagine mancante è mascherata da link fittizi; PHM conserva le immagini delle pagine effettivamente controllate. Nessun download HTML di login è stato importato come PDF.

Le risposte catalografiche essenziali, gli URL e le impronte delle copie sono in [VERIFICA_FONTI_FASE03.json](VERIFICA_FONTI_FASE03.json). I file temporanei di download/ricerca non costituiscono un corpus parallelo.

## 9. Verifiche documentali e limiti preesistenti

Risultati del controllo finale riportati in [VERIFICA_CORPUS_FASE03.json](VERIFICA_CORPUS_FASE03.json). `docs/test_explanation.py` viene confrontato prima/dopo; non certifica il corpus, perciò si verificano separatamente righe, colori, categorie, schede e link.

Il corpus passa da 117 a **128 voci classificate** (45 🟢, 47 🟡, 36 🔴), in **13 categorie**. Sono dieci opere aggiunte e una già citata (McMahan) completata e inclusa nell’indice, non undici opere prima assenti. Le schede passano da 29 a **40**: 39 riferite a 🟢 e una vecchia scheda FedSRD 🔴. L’arretrato delle sei schede 🟢 già dichiarate resta fuori perimetro. Rimane una voce precedente priva di autore verificato; i quattro limiti di accesso qui dichiarati sono una categoria di verifica diversa.

Problemi preesistenti estranei (eventuali link, conversioni o voci da riconciliare) sono elencati nel controllo finale e non riparati in massa. Nessuna lettura dei risultati dei nostri run è stata usata per motivare OOD. Zero simulazioni, training o chiamate sperimentali a modelli; OCR e controlli documentali sono le sole elaborazioni sulle fonti.


### Esito finale dei controlli

| Controllo | Prima → dopo / esito |
| --- | --- |
| `python3 docs/test_explanation.py` | **35 test; 14 fallimenti e 1 skipped → 14 fallimenti e 1 skipped**, stessi nomi dei fallimenti, nessun errore aggiunto |
| Tabelle del corpus MD/HTML | **182 righe complessive identiche nel contenuto testuale**; incluse le 128 voci classificate, stesso ordine |
| Categorie e colori | **13 categorie**, conteggi dichiarati uguali alle righe effettive; 45 🟢 + 47 🟡 + 36 🔴 = 128 |
| Schede | **40 titoli nello stesso ordine**, undici nuove schede con descrizione e implicazioni presenti identiche in HTML |
| Link nel corpus | HTML **0 → 0** link locali errati; MD **11 → 11** rimandi a vecchi anchor del walkthrough v2, preesistenti e lasciati intatti; nessun link locale nuovo errato |
| Riconciliazione PDF corrente ↔ §14.1 | **68/68 PDF** ricondotti a voci del corpus; alias ambigui controllati sul testo iniziale. Le due versioni Vovk restano distinte e documentate nella voce esistente |
| Coppie PDF/MD | Nessuna coppia corrente priva del proprio file; quattro opere non acquisite dichiarate senza segnaposti. Resta il MD Massart preesistente di **475 byte**, già dichiarato inservibile nel README |
| Deduplicazione acquisizioni | Nessuno dei sette nuovi PDF duplica il contenuto di un altro PDF corrente |
| Integrità congelati | **23/23 impronte prima/dopo identiche**; registro, SOURCE_CHECK, FEASIBILITY e manifest rev1 identici anche al tag criteri |
| Piano nel worktree fix | SHA-256 finale identico a quello iniziale; nessuna scrittura |

L’allineamento ha incluso solo la grafia di un’etichetta di link HTML già esistente (`studio2/fase03/fault_runs/SPECIFICA_RUN_FAULT.md`), per rendere identica la riga del corpus ai due formati; il suo contenuto scientifico non è stato riletto o corretto. Gli altri problemi preesistenti, incluso il vecchio arretrato di schede e il doppio tag di chiusura `head` dell’HTML, restano segnalati senza manutenzione estesa. La piccola integrazione al **blueprint** è richiesta da MAINTENANCE §6 punto 5: sola citazione McMahan già esistente e rimandi ai limiti bibliografici, nessun recepimento di decisioni sperimentali.

## 10. Conseguenze lasciate all’autore e letture effettuate

Le sole scelte scientifiche non risolte dalle fonti sono: quale distinzione meccanica adottare e se accettare F4 vicino al circuito di F14; come giustificare margine/livello di H3 e applicabilità di Tango alla popolazione stratificata; su quale unità e popolazione dichiarare esatti gli intervalli binomiali. La generabilità di F6 è un accertamento tecnico futuro, non una conclusione bibliografica. L’accesso mancante a Yin/Maurer/Westfall/Kish è un limite documentale dichiarato, non una domanda da risolvere scegliendo dati favorevoli.

Letture interne: MAINTENANCE, Prompt_LLM e Letteratura_LLM; handoff Fase 03; registro criteri, SOURCE_CHECK, verbale criteri 6.1, proposta OOD/D11, manifest criteri/D1 per perimetro e integrità; §8 e §§15–17 del piano statistico `-fix` e passaggi metodologici mirati; parti pertinenti della bozza decisioni autore; corpus e README per deduplicazione/classificazione; blueprint solo per i rimandi bibliografici obbligatori. Non è stato usato il walkthrough come fonte del disegno, né il solo HEAD dd82cd1 come sostituto del file modificato.

Fonti esterne effettivamente lette: PHM pp. 4–7 e frontespizio, inclusa verifica visiva completa pp. 6–7; Yin solo metadati/abstract; Tango §§2–4 pp. 892–897; Maurer frontespizio/indice DNB e voce nel CV dell’autore; Westfall anteprima editoriale; Clopper–Pearson pp. 404–408; Kish cataloghi e descrizione della ristampa; ICH §§3.3.2, 5.5–5.6; Hoeffding §§1–2 pp. 13–16; Bahadur–Savage §2 pp. 1115–1118; McMahan §2 e algoritmo 1 **PDF p. 5**, più discussione di privacy e limiti. **PDF completo disponibile non significa che tutte le pagine siano state lette.** Le schede dichiarano la lettura effettiva senza promuovere l’acquisizione a verifica integrale.

Costo di lettura: ordine di grandezza **alcune decine di migliaia di parole** fra fonti interne, cataloghi ed estratti primari; non una scansione integrale dei 128 lavori. Nessun costo di inferenza sperimentale o simulazione. La conversione/OCR è stata eseguita con script locali su sette PDF, senza revisione del corpus pregresso.

## 11. File modificati o aggiunti

Tutti nel worktree dedicato; nessun commit. Elenco completo, una riga per file:

| File | Modifica |
| --- | --- |
| [docs/letteratura.html](../../docs/letteratura.html) | Replica allineata sul contenuto, ordine, conteggi e schede; preservato lo stile esistente. |
| [docs/letteratura.md](../../docs/letteratura.md) | Dieci opere aggiunte, McMahan completato, undici classificazioni/schede; conteggi e limiti nelle sezioni 14.x. |
| [docs/lit_review/VERIFICA_CORPUS_FASE03.json](../../docs/lit_review/VERIFICA_CORPUS_FASE03.json) | Risultati di parità, conteggi, link, deduplicazione, riconciliazione e test prima/dopo. |
| [docs/lit_review/VERIFICA_FONTI_FASE03.json](../../docs/lit_review/VERIFICA_FONTI_FASE03.json) | Metadati verificati, URL, versioni, impronte delle fonti e snapshot di integrità. |
| [docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md](../../docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md) | Questa analisi di supporto e addendum separato al registro congelato. |
| [docs/paper/FoT_TEP_paper_blueprint.html](../../docs/paper/FoT_TEP_paper_blueprint.html) | Aggiornamento bibliografico minimo richiesto da MAINTENANCE: riferimento McMahan e rinvii alle verifiche. |
| [papers/Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.md](../../papers/Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.md) | Conversione testuale completa con provenienza e avvertenze sulle formule; OCR per le scansioni dichiarate. |
| [papers/Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.pdf](../../papers/Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.pdf) | Copia primaria acquisita, byte originali conservati. |
| [papers/Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.md](../../papers/Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.md) | Conversione testuale completa con provenienza e avvertenze sulle formule; OCR per le scansioni dichiarate. |
| [papers/Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.pdf](../../papers/Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.pdf) | Copia primaria acquisita, byte originali conservati. |
| [papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.md](../../papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.md) | Conversione testuale completa con provenienza e avvertenze sulle formule; OCR per le scansioni dichiarate. |
| [papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.pdf](../../papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.pdf) | Copia primaria acquisita, byte originali conservati. |
| [papers/Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.md](../../papers/Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.md) | Conversione testuale completa con provenienza e avvertenze sulle formule; OCR per le scansioni dichiarate. |
| [papers/Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.pdf](../../papers/Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.pdf) | Copia primaria acquisita, byte originali conservati. |
| [papers/README.md](../../papers/README.md) | Metadati, fonti, disponibilità/assenze e qualità delle conversioni. |
| [papers/Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.md](../../papers/Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.md) | Conversione testuale completa con provenienza e avvertenze sulle formule; OCR per le scansioni dichiarate. |
| [papers/Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.pdf](../../papers/Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.pdf) | Copia primaria acquisita, byte originali conservati. |
| [papers/The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.md](../../papers/The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.md) | Conversione testuale completa con provenienza e avvertenze sulle formule; OCR per le scansioni dichiarate. |
| [papers/The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.pdf](../../papers/The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.pdf) | Copia primaria acquisita, byte originali conservati. |
| [papers/The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.md](../../papers/The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.md) | Conversione testuale completa con provenienza e avvertenze sulle formule; OCR per le scansioni dichiarate. |
| [papers/The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.pdf](../../papers/The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.pdf) | Copia primaria acquisita, byte originali conservati. |
| [papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/page-6.png](../../papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/page-6.png) | Rendering PHM controllato; presente sul disco ma ignorato dalle regole Git esistenti per `_images/`, da includere esplicitamente nell’eventuale consegna futura. |
| [papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/page-7.png](../../papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/page-7.png) | Rendering PHM controllato; presente sul disco ma ignorato dalle regole Git esistenti per `_images/`, da includere esplicitamente nell’eventuale consegna futura. |

**Nota di conservazione:** i due PNG sono ignorati dalle regole Git esistenti; non sono stati forzati nell’indice. I PDF primari e i MD non sono ignorati. Nessuna modifica a `.gitignore`, staging o commit. Tutti i 23 file sono presenti nel worktree.
