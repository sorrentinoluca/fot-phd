OK

# Verifica indipendente del candidato bibliografico FoT-TEP — Fase 03

Data: **14 settembre 2026**  
Esito: **OK, nessun rilievo bloccante e nessuna correzione richiesta al candidato**.

## Firma, separazione dei ruoli e oggetto

La conclusione scientifica e il giudizio complessivo di questo verbale sono formulati da **`gpt-5.6-sol`**, task indipendente **`/root/independent_reviewer`**, in una sessione di agente distinta entro la finestra utente **`01a09f7d-e3e3-7c42-a5ac-02313a776bc2`**.

L'esecuzione bibliografica e i ricalcoli tecnici sono di **`gpt-6-astra`**. L'identità non è dedotta dallo stile: i record `/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T11-05-57-01a09f2a-7cc4-7ad0-adbf-df0e6060be8d.jsonl` e `/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T12-37-02-01a09f7d-e3e3-7c42-a5ac-02313a776bc2.jsonl` riportano `model=gpt-6-astra` nei rispettivi `turn_context` dell'esecutore e del coordinatore nella finestra principale. Il revisore indipendente è invece il task agente separato `/root/independent_reviewer`, assegnato esplicitamente a `gpt-5.6-sol`. Ho letto il rapporto tecnico, gli script e gli output, ho rieseguito gli script di audit e ne ho valutato autonomamente metodo e risultati. La ripetizione tecnica dello stesso modello esecutore costituisce evidenza controllabile, ma non viene presentata come firma scientifica indipendente. La firma indipendente riguarda la mia lettura delle fonti e la mia valutazione finale dell'intero insieme di prove.

Oggetto verificato: snapshot isolato `/Users/luker/fot-tep-verifica-letteratura-fase03`, costituito dalla base Git `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155` e dalla sovrapposizione selettiva dei 23 file del candidato provenienti da `/Users/luker/fot-tep-letteratura-fase03`, branch `codex/studio2-letteratura-fase03`. Lo snapshot non ha una propria `.git`. Questo verbale è un artefatto successivo di verifica e non fa parte dei 23 file candidati.

Ho applicato `docs/MAINTENANCE.md` e i prompt `Prompt_LLM.md`, `Verifica_LLM.md` e `Letteratura_LLM.md`. Ho controllato fonti, PDF, rendering, formule e attribuzioni; non ho modificato il worktree sorgente, i 23 artefatti candidati, gli artefatti congelati o il piano statistico. Non sono stati eseguiti esperimenti, simulazioni, training o chiamate sperimentali a modelli.

## Giudizio complessivo

| Area | Esito | Giudizio indipendente |
|---|---|---|
| Fonte PHM e numeri F4/F6/F9 | ✅ | PDF corrente, copia candidata e hash storico coincidono; tabelle rilette sul rendering indipendente; valori e semantica riportati correttamente |
| Nove riferimenti metodologici | ✅ | Attribuzioni, formule e limiti sono corretti; le deduzioni FoT sono separate dalle citazioni |
| Yin e accessi incompleti | ⚠️ dichiarato | Quattro limiti di full text sono espliciti; nessuna affermazione eccede il materiale realmente consultato |
| Corpus MD/HTML, README, JSON | ✅ | Conteggi, ordine, schede, metadati, link e disponibilità delle fonti sono coerenti |
| Integrità e perimetro | ✅ | Soli quattro file tracciati attesi differiscono dalla base; 23 file protetti invariati; nessun contenuto sperimentale introdotto |
| Test prima/dopo | ⚠️ preesistente | Stessi 14 fallimenti e 1 skip su 35 test, zero errori; nessuna regressione del candidato |
| OOD, piano e freeze 03.8 | ✅ per il perimetro | Il candidato fornisce supporto bibliografico e lascia le decisioni all'autore; non approva o congela alcuna scelta sperimentale |

Non ho trovato errori scientifici, omissioni materiali nuove, attribuzioni eccessive, regressioni documentali o violazioni del perimetro che richiedano una correzione. Gli arretrati preesistenti e i limiti di accesso sono mantenuti visibili e non sono mascherati da segnaposti o deduzioni favorevoli.

## Verifica scientifica primaria PHM

Ho riscaricato il PDF ufficiale da PHM Society e l'ho confrontato con la copia candidata e con l'impronta storica in `studio2/fase03/selection/SOURCE_CHECK.json`. I tre riscontri coincidono: **SHA-256 `e11310c44cebca7a6ebc368b3862dc2edc0003a4ee31cb9223feb6d5e0ae7b78`, 721381 byte, 10 pagine**. Ho renderizzato indipendentemente con Poppler a 220 dpi le pagine PDF 6 e 7 e letto le celle sulle immagini.

La tabella 2 dispone i fault nelle colonne e `DAE`, `T²`, `SPE` nelle righe. Le tabelle 2, 3 e 4 sono tutte a p. 6. I valori verificati per singola cella sono:

| Fault / colonna | Detector / riga | Tabella 2 FDR (%) | Tabella 3 FAR (%) | Tabella 4 ritardo FDD (min) |
|---|---|---:|---:|---:|
| **F6**, “Uncontrollable faults” | DAE | **100** | **0,6** | **0** |
| **F6**, “Uncontrollable faults” | T² (PCA) | **99** | **1,3** | **24** |
| **F6**, “Uncontrollable faults” | SPE (PCA) | **100** | **0,6** | **0** |
| **F4**, “Back to control faults” | DAE | **100** | **3,1** | **0** |
| **F4**, “Back to control faults” | T² (PCA) | **18** | **1,9** | **0** |
| **F4**, “Back to control faults” | SPE (PCA) | **100** | **5** | **0** |

Per **F9/SPE**, tabella 2, il valore è **5,6%**. Il **6,6%** in `docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md:70` è quindi una trascrizione nel registro congelato, non uno scarto fra versioni della fonte. Il candidato la segnala correttamente nell'addendum senza modificare il registro.

La pagina 7 definisce FDR come **fault detection rate**; non è false discovery rate né accuratezza diagnostica. FAR e ritardi sono misure separate. La frase sui “tre detector” è limitata alle tre righe del paper: DAE e due statistiche PCA, T² e SPE. Il candidato riporta anche le condizioni pertinenti — 960 osservazioni di training e test, 52 variabili, prime 160 normali, DAE dinamico, PCA con 9 componenti — e dichiara che il paper non offre intervalli di confidenza, riproduzione FoT, prova di generabilità nel simulatore o diagnosi della causa.

La conseguenza bibliografica è circoscritta: PHM fornisce un riscontro esterno numerico per la rilevazione di F6 e documenta il comportamento diverso di F4. Non decide una soglia FDR universale, una scelta OOD, una riclassificazione di H, un fault sostitutivo, la generabilità tecnica o il freeze. Questa delimitazione compare in `docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md:7-11`, `:33`, `:37-82` e in `docs/paper/FoT_TEP_paper_blueprint.html:591`.

## Verifica delle nove fonti metodologiche

| Opera | Anno e sede | Versione verificata | DOI / collegamento primario |
|---|---|---|---|
| T. Tango, *Equivalence test and confidence interval for the difference in proportions for the paired-sample design* | 1998, *Statistics in Medicine* 17(8), 891–908 | PDF typeset della rivista | DOI [`10.1002/(SICI)1097-0258(19980430)17:8<891::AID-SIM780>3.0.CO;2-B`](https://doi.org/10.1002/%28SICI%291097-0258%2819980430%2917%3A8%3C891%3A%3AAID-SIM780%3E3.0.CO%3B2-B); [PDF](https://www.eiti.uottawa.ca/~nat/Courses/csi5388/Tango.paired.pdf) |
| W. Maurer, L. A. Hothorn, W. Lehmacher, *Multiple comparisons… a-priori ordered hypotheses* | 1995, capitolo in *Testing principles in clinical and preclinical trials*, pp. 3–18 | Frontespizio e indice DNB; voce nel CV di Ludwig A. Hothorn; capitolo non acquisito | DOI non reperito; [DNB](https://d-nb.info/944101399/04) |
| P. H. Westfall, A. Krishen, *Optimally weighted, fixed sequence and gatekeeper multiple testing procedures* | 2001, *Journal of Statistical Planning and Inference* 99(1), 25–40 | Metadati e anteprima editoriale; PDF integrale non acquisito | DOI [`10.1016/S0378-3758(01)00077-5`](https://doi.org/10.1016/S0378-3758%2801%2900077-5); [editore](https://www.sciencedirect.com/science/article/pii/S0378375801000775) |
| C. J. Clopper, E. S. Pearson, *The use of confidence or fiducial limits illustrated in the case of the binomial* | 1934, *Biometrika* 26(4), 404–413 | Scansione JSTOR con copertina aggiunta | DOI [`10.1093/biomet/26.4.404`](https://doi.org/10.1093/biomet/26.4.404); [PDF](https://www.barestatistics.nl/uploads/1/1/7/9/11797954/clopper__pearson_1934.pdf) |
| L. Kish, *Survey Sampling* | 1965, Wiley, xvi+643 pp. | Edizione 1965 verificata da cataloghi; testo non acquisito, distinta dalla ristampa 1995 | DOI non reperito; [Google Books](https://books.google.com/books/about/Survey_sampling.html?id=3xVHAQAAIAAJ) |
| ICH, *Statistical Principles for Clinical Trials*, E9 | 1998, Step 5 CPMP/ICH/363/96 | Copia ufficiale EMA con impaginazione EMEA 2006; non E9(R1) | DOI non assegnato; [PDF EMA](https://www.ema.europa.eu/system/files/documents/scientific-guideline/wc500002928_en.pdf) |
| W. Hoeffding, *Probability Inequalities for Sums of Bounded Random Variables* | 1963, *JASA* 58(301), 13–30 | Articolo di rivista 1963; non mimeo 1962 | DOI [`10.1080/01621459.1963.10500830`](https://doi.org/10.1080/01621459.1963.10500830); [PDF](https://www.cs.rpi.edu/academics/courses/spring06/random/hoefding.pdf) |
| R. R. Bahadur, L. J. Savage, *The Nonexistence of Certain Statistical Procedures in Nonparametric Problems* | 1956, *Annals of Mathematical Statistics* 27(4), 1115–1122 | Scansione dell'articolo di rivista | DOI [`10.1214/aoms/1177728077`](https://doi.org/10.1214/aoms/1177728077); [repository IAS](https://repository.ias.ac.in/27021/1/314.pdf) |
| B. McMahan et al., *Communication-Efficient Learning of Deep Networks from Decentralized Data* | 2017, AISTATS, PMLR 54, 1273–1282 | PDF ufficiale degli atti PMLR | DOI degli atti non reperito/non esposto; [PMLR](https://proceedings.mlr.press/v54/mcmahan17a.html) |

### Tango (1998)

Ho letto §§2–4, pp. 892–897 del PDF typeset, che coincide con la copia candidata: SHA-256 `71dea8eddc08c73f15e2454d69b7f46d8bfa61b550c6246173fdfa4307df7ecd`. Il modello è un campione casuale multinomiale appaiato; l'equazione (29), p. 896, tratta il caso con celle discordanti nulle. Il test score proposto è asintotico. `docs/letteratura.md:575-584` e l'addendum precisano correttamente che quote fisse per fault e strati eterogenei non sono automaticamente IID/multinomiali e che una conclusione aggregata non garantisce non inferiorità per agente.

### Maurer, Hothorn e Lehmacher (1995)

Il full text del capitolo non è stato acquisito. Ho verificato frontespizio e indice DNB, SHA-256 temporaneo `2f5be181cc595285fe9b50731560f4a6449176de93b63db51344d8f4f3691436`, e la voce nel CV di **Ludwig A. Hothorn**, la cui prima riga è “Curriculum Vitae Ludwig A. Hothorn”, SHA-256 `97e9bbcac8e46c8fe60ad868ad5a9c541df53b7885ba346137be8eb00dc6d064`. Il capitolo inizia a p. 3 e termina prima del successivo, che inizia a p. 19: pp. 3–18 sono corroborate. Il limite è dichiarato a `VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md:91` e `docs/letteratura.md:586-595`.

La dimostrazione autonoma della fixed sequence è corretta: in un ordine prefissato con arresto al primo mancato rifiuto, ogni falso rifiuto implica il rifiuto della prima ipotesi vera. Se ciascun test locale ha livello uniforme al più α, la FWER forte è al più α, senza richiedere indipendenza fra test. La validità esatta non segue se il test locale è soltanto approssimato. Il candidato presenta questa prova come propria derivazione, non come testo letto in Maurer.

### Westfall e Krishen (2001)

La risposta Elsevier conservata è metadata-only, SHA-256 `fc52a92ee0f299725bf61e46a17881761aec781847721ae07100ce4c3ad93b2b`. Ho verificato Crossref e l'anteprima editoriale accessibile, che tratta il controllo forte FWE e dichiara, nella sezione esposta, che la fixed sequence non richiede indipendenza. Il PDF integrale è assente e il candidato non lo presenta come letto; la prova della procedura resta autonoma.

### Clopper e Pearson (1934)

Ho letto pp. 404–408 e controllato visivamente pp. 406–407; SHA-256 candidato `e49da40d3fc184d591ec87681f30eae8077a2fb57b27850856207f54a7116e39`. L'intervallo deriva dalle code binomiali e garantisce copertura ripetuta almeno nominale nel modello binomiale. Le schede non estendono l'esattezza a risposte correlate o a una miscela di probabilità eterogenee: unità Bernoulli, popolazione e assunzioni devono essere specificate per FoT.

### Kish (1965)

Il full text non è stato acquisito. Google Books conferma autore, titolo, Wiley, 1965, 643 pagine e ISBN 047148900X/9780471489009. La formula `1+(k−1)ρ` è derivata separatamente per cluster equidimensionali, varianza marginale comune e correlazione intra-cluster comune. Il candidato la qualifica come scenario algebrico e non la attribuisce a una pagina primaria non letta né la tratta come garanzia per il disegno effettivo.

### ICH E9 (1998)

Ho letto il PDF ufficiale EMA §§3.3.2, 5.5 e 5.6, pp. 17–18 e 27–28; SHA-256 candidato `6dd74185bb88a6f48a4b3a154893f9d8953b2fa4784c56fedda102e45f410b96`. La guida richiede una giustificazione clinica del margine di non inferiorità e, nel contesto regolatorio, preferisce un errore unilaterale pari alla metà di quello bilaterale convenzionale. Il valore 0,025 segue se il bilaterale è 0,05; la guida non sceglie α=0,05 unilaterale o m=0,125 per FoT e non è presentata come standard ML.

### Hoeffding (1963)

Ho controllato sul rendering §§1–2, pp. 13–16, incluso il teorema 2, eq. (2.6); SHA-256 candidato `3021bcc097ef23a99a84d0eef8dcce2fd835c71df79a105727d3e03f8f0b8930`. Per variabili indipendenti `D_c ∈ [-1,1]`, anche non identicamente distribuite, segue `P(media(D)−E media(D) ≥ t) ≤ exp(−Nt²/2)`. Sotto `E media(D)≤0`, la soglia `sqrt(2 log(1/α)/N)` ha livello al più α. Il candidato dichiara che ciò non dimostra potenza, MDE o indipendenza effettiva dei cluster.

### Bahadur e Savage (1956)

Ho controllato sul rendering §2, pp. 1115–1118, ipotesi (i)–(iii), teorema 1 e corollario 1; SHA-256 candidato `cc3d6d5b43fa3b136daae5db8831fac12b0e1cbb17326d8087302ffc5139caca`. La classe richiede distribuzioni di ogni media reale e convessità; può includere distribuzioni individualmente a supporto finito o limitato. Il limite comune `[-1,1]` fa fallire la ricchezza delle medie, non perché ogni distribuzione debba avere code illimitate. Il candidato corregge questa distinzione e non sostiene che la fonte invalidi tutti i test non parametrici della media o dimostri il sign-flip.

### McMahan et al. (2017)

Ho letto §2, algoritmo 1 a p. 1277, PDF p. 5, e la discussione su privacy e limiti; SHA-256 candidato `a7a8e2e3e437855c1efb53fe8f35f645eae7735fe9b6ac1f656a62004dbf5146`. FedAvg combina SGD locale con aggregazione dei modelli pesata da `n_k/n`. Mantenere locali i dati grezzi non è una garanzia formale di privacy; gli aggiornamenti possono perdere informazione e privacy differenziale/secure aggregation sono misure separate. Risultati su altri dataset non predicono FoT/TEP. La scheda e il blueprint restano entro questi limiti.

## Yin et al. e disponibilità delle fonti

Crossref conferma titolo, cinque autori, *Journal of Process Control* 22(9), 1567–1581, ottobre 2012 e DOI `10.1016/j.jprocont.2012.06.009`. OpenAlex indica accesso chiuso e nessun full text di repository. La risposta Elsevier conservata, SHA-256 `1fc5653688728cbd2912530871aaac6de71b60bc4972fa5c0551bdd7d440b8b9`, è metadata-only. Non ho trovato una copia primaria integrale accessibile.

I quattro limiti sono quindi: Yin, metadata/abstract; Maurer, frontespizio/indice e CV; Westfall, metadata e anteprima editoriale; Kish, cataloghi. `docs/letteratura.md`, `papers/README.md`, l'addendum e `VERIFICA_FONTI_FASE03.json` li descrivono in modo coerente. Nessun numero non letto è attribuito a Yin; nessun segnaposto è dichiarato come PDF integrale; ogni risultato metodologico utilizzato è limitato al materiale esposto o accompagnato da una derivazione verificabile.

## Inventario esatto dei 23 file candidati

Il rapporto tecnico di `gpt-6-astra` ha letto e confrontato i byte della sorgente e dello snapshot. Ho controllato il relativo inventario e gli output di hash. Totale: **6.407.129 byte**.

| File relativo allo snapshot | Stato | Byte | SHA-256 |
|---|---|---:|---|
| `docs/letteratura.html` | tracked | 118348 | `c6836de6f7b3eea83c5d29bebea1db2b4a410ae21460515336f8cceba633ba3d` |
| `docs/letteratura.md` | tracked | 90911 | `d4048e7f6ae14fb853315ab3f61bdaada0818f31d0e8ff1532e8dbeae7e1974f` |
| `docs/lit_review/VERIFICA_CORPUS_FASE03.json` | untracked | 56124 | `f7a0f8dea9d0bc248976dee3ee651336c3d7a38f089834dbd45856eb587e958c` |
| `docs/lit_review/VERIFICA_FONTI_FASE03.json` | untracked | 18119 | `b1b9e6e7b7c2c20ff4c800281e5807a481de7ab77a786596be336ec03e602c4c` |
| `docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md` | untracked | 34808 | `f2c29416664e27c2ecac7d439939f51f1a3f7313e2aba669bb39db7106cf0b8e` |
| `docs/paper/FoT_TEP_paper_blueprint.html` | tracked | 84596 | `bb7175c3daf12031dd4c4369861385cb5bc3c8a128ccfa015a8073ea25e3e85f` |
| `papers/Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.md` | untracked | 49642 | `ff35468825adcbedb8ed9a483c9fe6d508fb66d8f80884c64e3e8a3b9d20b379` |
| `papers/Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.pdf` | untracked | 763853 | `a7a8e2e3e437855c1efb53fe8f35f645eae7735fe9b6ac1f656a62004dbf5146` |
| `papers/Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.md` | untracked | 42171 | `e45f191f919d84e4586ebf894fb8f6dbff4160a9376610dc0d3ae1cfdd204e90` |
| `papers/Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.pdf` | untracked | 257783 | `71dea8eddc08c73f15e2454d69b7f46d8bfa61b550c6246173fdfa4307df7ecd` |
| `papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.md` | untracked | 41600 | `4eb0676440e30f8e6f3fe944497efa23f5a64222f4173e0c261cfaa99d71ea00` |
| `papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.pdf` | untracked | 721381 | `e11310c44cebca7a6ebc368b3862dc2edc0003a4ee31cb9223feb6d5e0ae7b78` |
| `papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/page-6.png` | ignored | 286075 | `0d4174ce35e88e941540b722ff1d632b5a0ed6527f66aeed7d2089eb6d4f2bf8` |
| `papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/page-7.png` | ignored | 557127 | `020f08386172d87c5ca45fecabc30a402904498bbb60754a745a4520104bed91` |
| `papers/Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.md` | untracked | 35965 | `8aac701840988609d760fcde92760222a1682babef043711a63f8a9a615f19c5` |
| `papers/Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.pdf` | untracked | 1451039 | `3021bcc097ef23a99a84d0eef8dcce2fd835c71df79a105727d3e03f8f0b8930` |
| `papers/README.md` | tracked | 34388 | `b3777d58cbee1660044d2cf36387570cef7c220f5ce0f6fba06ddb2a081d0fc0` |
| `papers/Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.md` | untracked | 140385 | `805cb8bef8a7783de84fe17015172034f998d17c7abb9de46d8fbf10d121695d` |
| `papers/Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.pdf` | untracked | 332364 | `6dd74185bb88a6f48a4b3a154893f9d8953b2fa4784c56fedda102e45f410b96` |
| `papers/The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.md` | untracked | 18729 | `921835907c12fcbe5f63905e9bfaf7042bdc95207f7699cb8f646669ad4c3d19` |
| `papers/The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.pdf` | untracked | 760570 | `cc3d6d5b43fa3b136daae5db8831fac12b0e1cbb17326d8087302ffc5139caca` |
| `papers/The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.md` | untracked | 21784 | `5a423c7d5f0af2f2e4b246f0cabe30cc2b8f3f5d3f31c82a41b88d21079dcbcb` |
| `papers/The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.pdf` | untracked | 489367 | `e49da40d3fc184d591ec87681f30eae8077a2fb57b27850856207f54a7116e39` |

I due PNG sono immagini valide, 980×1268, identiche fra sorgente e snapshot. Sono ignorate dalla regola `.gitignore:47` (`/papers/**/*_images/`) e dovranno essere incluse esplicitamente in un'eventuale consegna futura; non sono state forzate nell'indice.

## Corpus, conversioni e collegamenti

I ricalcoli tecnici, riesaminati e rieseguiti, danno:

- base **117 voci / 12 categorie / 29 schede**; candidato **128 / 13 / 40**;
- colori del candidato: **45 verdi, 47 gialli, 36 rossi**;
- **182** righe tabellari MD e HTML identiche cella per cella dopo normalizzazione del markup;
- **40** titoli di scheda nello stesso ordine;
- tutti i **191** blocchi di prosa MD presenti in HTML, senza aggiunte sostanziali inverse;
- **68 PDF / 68 MD**, nessuna coppia mancante, nessun hash PDF duplicato;
- tutti i 68 PDF ricondotti a una voce di §14.1, con lettura dei frontespizi per i 17 alias deboli e disambiguazione di HDLCNN-SHAP, i due FD-LLM, Federation over Text, Odiowei–Cao rispetto a CVKA, KSVD rispetto a K-Means e le due versioni Vovk;
- le sette nuove coppie coprono tutte le pagine; cinque MD coincidono pagina per pagina con una nuova estrazione pypdf, mentre Hoeffding e Bahadur–Savage sono scansioni OCR dichiarate non affidabili per le formule, controllate qui sul rendering;
- **67** link a percorsi locali nei MD candidati, tutti esistenti;
- link locali HTML: **0 errori nella base, 0 nel candidato**;
- Markdown: **11 rimandi a vecchi anchor del walkthrough v2 mancanti nella base e gli stessi 11 nel candidato**; nessun link nuovo rotto.

Gli arretrati sono preesistenti e dichiarati: sei voci verdi senza scheda — FICAL, DP-FPL, FedDTPT, T2SP, TableTime e *Federated Reasoning LLMs: A Survey* — una scheda rossa FedSRD e il MD Massart di 475 byte già indicato come inservibile in `papers/README.md:75`. Non sono regressioni del candidato e la loro manutenzione non è condizione di questo esito.

## Integrità, test e perimetro protetto

L'audit ha improntato i **2226 file tracciati** della sorgente. Rispetto alla base differiscono soltanto i quattro file tracciati attesi: `docs/letteratura.html`, `docs/letteratura.md`, `docs/paper/FoT_TEP_paper_blueprint.html` e `papers/README.md`. I 23 file candidati sono byte-identici fra sorgente e copia.

I **23 file protetti** — registro e 22 file in `studio2/fase03/selection/` — sono byte-identici fra base, sorgente e snapshot. Registro, `SOURCE_CHECK.json`, `FEASIBILITY.json` e `CRITERIA_FREEZE.json` coincidono anche con il tag `studio2-fase03-criteri-selezione-frozen-001`, commit `9faecaf7337e5864b7a3ad44cadb8971853dd260`. H resta `{F3,F9,F15}` e D1 resta `{F1,F2,F3,F8,F10,F13,F14,F15}`; `{F3,F15}` nella proposta OOD indica l'intersezione di H con D1 e non una riclassificazione globale.

Il piano esterno effettivamente osservato in `/Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/PIANO_STATISTICO.md` misura 63602 byte e ha SHA-256 `3326e992995114f92b20117cd4b4575f6c2e7ba1758fee4463461448f010fba6`. I confronti sono mirati al testo effettivo: il piano tratta F6/F4 e le scelte statistiche come proposte o decisioni ancora da assumere. Questo dato non costituisce un giudizio automatico su 03.8.

Il diff del blueprint contiene tre soli hunk bibliografici: rinvio ai limiti delle fonti, addendum con numeri e limiti PHM, aggiornamento dello stato McMahan. A riga 591 dichiara che non recepisce scelte OOD o statistiche. Nessun file di piano, walkthrough o artefatto congelato rientra nei quattro delta tracciati.

`python3 docs/test_explanation.py`, eseguito in due directory isolate, produce sia sulla base sia sul candidato **35 test, 14 fallimenti, 1 skip e 0 errori**. Le 14 identità, inclusi i subtest, coincidono esattamente. Il test riguarda il walkthrough preesistente e non certifica §14; il confronto dimostra l'assenza di regressioni del candidato, non la correttezza dei fallimenti preesistenti.

Al controllo di concorrenza **2026-09-14T10:45:22.496394+00:00** risultavano **modificati 0/23** file candidati sorgenti, **0/23** copie e **0/2226** file tracciati sorgenti, ossia invariati rispettivamente 23/23, 23/23 e 2226/2226; HEAD era ancora `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155` e l'indice sorgente non aveva file staged. Un controllo successivo alla scrittura di questo verbale è registrato in calce.

## Rilievi, conseguenze e correzioni

| Esito | Evidenza e localizzazione | Conseguenza | Correzione richiesta |
|---|---|---|---|
| ✅ | PHM tabelle 2–4, pp. 6–7; addendum `:33`, `:45-68` | F4/F6, FAR, ritardi e F9/SPE sono riportati correttamente; il 6,6% congelato è una trascrizione | Nessuna; mantenere il registro congelato e l'addendum separato |
| ✅ | Tango §§2–4; addendum `:90`, `:102`, `:106` | Il test è asintotico e il modello non è automaticamente trasferibile a quote/strati FoT | Nessuna; la cautela è già presente |
| ✅ | Maurer/Westfall e prova autonoma | La fixed sequence controlla FWER sotto ordine, arresto e test locali validi; non richiede indipendenza | Nessuna; non trasformare Tango in garanzia esatta |
| ✅ | Clopper pp. 404–408; derivazione Kish | Esattezza binomiale e design effect dipendono dalle unità e dal modello dichiarati | Nessuna |
| ✅ | ICH §§3.3.2, 5.5–5.6; Hoeffding eq. (2.6); Bahadur–Savage §2 | Margine, α, indipendenza e classe distributiva restano assunzioni o scelte da giustificare | Nessuna |
| ✅ | McMahan §2, algoritmo 1 e privacy | FedAvg non offre privacy formale né trasferibilità automatica a FoT | Nessuna |
| ⚠️ documentale | Schede Yin/Maurer/Westfall/Kish, README e JSON | Il controllo è limitato a metadata, indice, preview o cataloghi | Nessuna; il limite è esplicito e nessun claim lo eccede |
| ⚠️ preesistente | Sei schede verdi, FedSRD, Massart, 11 anchor, test walkthrough | Arretrato separato, invariato prima/dopo | Nessuna nel candidato corrente |

## Decisioni che restano all'autore

Questo esito non risolve e non deve essere letto come approvazione implicita di:

1. quale distinzione meccanica adottare e se collocare F4 vicino al circuito di F14;
2. margine, livello, ordine e modello di campionamento per H3, inclusa l'applicabilità di Tango alla popolazione stratificata;
3. unità Bernoulli e popolazione rispetto alle quali dichiarare “esatto” un intervallo Clopper–Pearson;
4. indipendenza effettiva dei cluster richiesta per l'uso diretto della soglia di Hoeffding;
5. generabilità tecnica di F6 nel simulatore;
6. selezione OOD, sostituzione di fault, riclassificazione di H, adozione del piano o freeze della fase 03.8.

Le fonti delimitano queste decisioni ma non le prendono. Il candidato rispetta tale confine.

## Provenienza delle prove e ripetibilità

La mia revisione scientifica dettagliata è conservata in `/tmp/fot-tep-lit-independent/scientific-review.md`, SHA-256 `f0a42bd800f44e96e3632d0be97c8cc22da8d09360886209e942689b1c04e9e0`. Il rapporto tecnico di `gpt-6-astra` è `/tmp/fot-tep-lit-independent/technical-review.md`, SHA-256 `53a7e4ff8eb23a3797e644703d2d88ee3d144c5235aa6891b62b6d3cf30cd93f`. Gli script e gli output sono in `/tmp/fot-tep-lit-independent/`: `audit_corpus.py`, `audit_integrity.py`, `snapshot.json`, `corpus-recalculated.json`, `integrity.json`, `conversions.json`, `pdf-reconciliation-final.json`, `final-integrity.json`, log dei test e diff candidato. Il presente verbale incorpora gli elementi essenziali perché `/tmp` non è una sede durevole.

Letture interne: `MAINTENANCE.md`, i tre prompt operativi, richiesta integrale, registro criteri, `SOURCE_CHECK`, `FEASIBILITY`, manifest e verbali congelati, proposta OOD/D1, passaggi mirati del piano statistico effettivo, addendum, corpus MD/HTML, README, JSON di verifica e tre hunk del blueprint. Letture esterne: frontespizi e metadati delle opere elencate; PHM pp. 4–7 con rendering pp. 6–7; Tango pp. 892–897; Clopper–Pearson pp. 404–408; ICH §§3.3.2 e 5.5–5.6; Hoeffding pp. 13–16; Bahadur–Savage pp. 1115–1118; McMahan §2, algoritmo 1 e discussione privacy; per Maurer, Westfall, Kish e Yin soltanto le porzioni disponibili già dichiarate. “PDF disponibile” non significa lettura integrale di ogni pagina.

Il costo di lettura è stimato nell'ordine di **alcune decine di migliaia di parole** fra fonti interne, estratti primari, cataloghi e metadati. Non è una revisione integrale dei 128 lavori e non comprende costo di inferenza sperimentale o simulazione.

## Conclusione indipendente

**OK.** Il candidato bibliografico è scientificamente fedele alle fonti consultate, documenta con precisione ciò che non è stato possibile leggere, conserva separati fatti bibliografici, deduzioni autonome e decisioni sperimentali, e non introduce regressioni o modifiche al perimetro congelato. Non sono necessarie correzioni prima della consegna del candidato. I due PNG ignorati richiedono inclusione esplicita qualora la consegna debba conservarli; ciò è già dichiarato e non altera l'esito scientifico.

Il giudizio riguarda questo candidato bibliografico nello snapshot e nelle impronte indicate. **Non costituisce un verdetto favorevole automatico sulla fase 03.8, sul piano statistico, sull'OOD o sul freeze.**

## Controllo di concorrenza successivo al verbale

Controllo conclusivo eseguito dal coordinatore `gpt-6-astra` il **2026-09-14T10:59:56.234044+00:00**, dopo la stesura e revisione indipendente del verbale.

✅ Impronte ricalcolate: **23/23 file candidati sorgenti invariati**, **23/23 copie candidate invariate**, **2226/2226 file tracciati sorgenti invariati** rispetto all’acquisizione iniziale. Nessuna modifica concorrente rilevata. HEAD sorgente resta `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155`; indice Git sorgente senza file staged. Lo stato presenta ancora soltanto i quattro file tracciati modificati e i diciassette nuovi file non ignorati del candidato; i due PNG restano ignorati.

Questo verbale è il solo nuovo artefatto finale scritto nella copia di verifica ed è escluso dalle 23 impronte candidate. Sorgente e artefatti verificati non sono stati corretti. Nessun commit, push, merge, tag o aggiornamento del walkthrough. La conclusione indipendente di `gpt-5.6-sol` sopra resta invariata.
