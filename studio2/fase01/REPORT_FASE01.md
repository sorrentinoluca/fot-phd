# Studio 2 — Report fase 01

**Macrofase:** ricognizione e consolidamento del patrimonio sperimentale.

**Data di redazione:** 2026-09-12.

**Stato del lavoro:** ricognizione conclusa, con OK della verifica indipendente.

**Stato sperimentale:** nessuna autorizzazione alla generazione dei dati o all'esecuzione dello studio deriva da questa chiusura.

## 1. Scopo e nomenclatura

La **fase 01** è la prima macrofase dello studio 2. Comprende tutte le sette attività chiamate «fasi 1–7» durante la discussione: inventario, provenienza, compatibilità, classificazione del riuso, perimetro dei dati, budget e perimetro operativo. Quella numerazione descrive le attività interne della presente macrofase; non identifica sette macrofasi del nuovo esperimento e non coincide con i sette requisiti residui della calibrazione.

L'obiettivo era recuperare il più possibile dati, numeri, esecuzioni e componenti disponibili, determinando il lavoro nuovo indispensabile. Nel paper i materiali eventualmente inclusi potranno essere descritti per configurazione, provenienza verificabile e ruolo, senza raccontare un distinto esperimento precedente. Rimangono necessarie la tracciabilità interna e la distinzione fra analisi pre-specificate e post-hoc. Un dato già osservato non diventa una nuova conferma indipendente per effetto della sua inclusione nello studio 2.

Questo documento è il **consuntivo della ricognizione richiesto dall'autore**. Non sostituisce il piano o i registri autorevoli, non formalizza le proposte R1/R2 e non costituisce un congelamento del protocollo. Le descrizioni del patrimonio precedente hanno funzione di provenienza interna.

## 2. Fonti e stato del repository

Le precedenze sono quelle di [walkthrough studio 2, §0](../../docs/fot_walkthrough_conversazione_studio2.md):

| Ambito | Fonte |
|---|---|
| Contratto, perimetro e congelamenti | [MAINTENANCE.md](../../docs/MAINTENANCE.md), inclusa §8 |
| Disegno sperimentale | [Piano sperimentale](../../docs/paper/FoT_TEP_Review_Piano_Sperimentale.md), revisione 6 |
| Calibrazione, prevalente sul piano | [Registro calibrazione](../../docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md), revisione 18 |
| Descrittori | [Criteri](../../docs/lit_review/criteri_scelta_descrittori.md), §5.1, e [registro feature](../../docs/lit_review/DECISIONE_SCELTA_FEATURE_fase_A.md) |
| Guida ai risultati disponibili | [Walkthrough v2](../../docs/fot_walkthrough_conversazione_v2.md), letto integralmente |
| Dettagli operativi della costruzione | [Prima esposizione](../../docs/fot_walkthrough_conversazione.md) |

Il piano originale `FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md` non è la fonte del disegno corrente.

La ricognizione iniziale è stata svolta sullo stato identificato da `9289a4cb3b2d657553c4564fc4bb0f95569b6cac`; il riesame indipendente conclusivo si riferisce a `941c09b2253887101243615165df1d894b8e5c2d`, che introduce le regole della §8. Il presente report viene redatto su `9e3d9031013788a583e348fbd7bfc40e14d3c68b`, nel branch `codex/studio2-report-ricognizione`. Questi sono riferimenti allo stato esaminato, non nuovi tag di congelamento.

## 3. Attività interne e risultato

| Attività | Lavoro svolto | Esito della ricognizione |
|---|---|---|
| 1. Inventario | Censimento di raccolte, duplicazioni, derivati, esecuzioni e 17 run aggiuntivi | Chiuso dopo integrazione richiesta dalla review |
| 2. Provenienza | Collegamento fra dati, commit, tag, manifest e impieghi precedenti | Chiuso; lacune di metadati e conservazione esplicitate |
| 3. Compatibilità | Confronto di baseline, feature, soglie, rappresentazioni e componenti | Chiuso come analisi; compatibilità operativa futura non certificata |
| 4. Ruoli di riuso | Distinzione fra riuso diretto, condizionato, ricalcolo e riferimento | Chiuso |
| 5. Perimetro dei dati | Separazione fra baseline, sviluppo, pilota, calibrazione e verifiche | Chiuso come proposta; R1/R2 non formalizzate |
| 6. Budget | Formula parametrica con Normal di sviluppo, limiti del recupero e costi API | Chiuso dopo correzioni della review |
| 7. Perimetro operativo | Rilievo negativo sui percorsi predefiniti e allineamento alla radice unica studio2/ | Chiuso come ricognizione; adattamenti non implementati |

Le attività 1 e 2 sono state affrontate in parallelo. Le altre sono state sviluppate rispettando le dipendenze. Nessuna nuova simulazione, produzione di insight o inferenza sperimentale è stata avviata durante la ricognizione.

## 4. Inventario dei dati grezzi

### 4.1 Regola di perimetro

Il conteggio comprende i file `.xlsx` materializzati nelle quattro raccolte `code/tep_cache/`, `tep_cache/`, `tep_heldout/mode1/` e `tep_exp3_v2_heldout/mode1/`, incluse le sottocartelle. Si contano separatamente percorsi e contenuti distinti per SHA-256.

Non è un censimento indistinto di tutti i fogli sul computer. Sono esclusi i puntatori LFS senza contenuto, altri dataset o modalità e le copie storiche dei medesimi dati nei tag, che non incrementano il numero di contenuti. Un file, un contenuto distinto, un blocco temporale e un run indipendente non sono la stessa unità.

| Raccolta | File XLSX | Composizione |
|---|---:|---|
| `code/tep_cache/` | 21 | 20 fault F1/F8/F10/F13, batch 1–5, e Normal 500 h |
| `tep_cache/`, sola radice | 5 | Quattro copie del batch 1 e Normal 50 h |
| `tep_cache/validation_v2/` | 8 | Quattro fault, batch 6–7 |
| `tep_cache/test_v2/` | 12 | Quattro fault, batch 8–10 |
| `tep_heldout/mode1/` | 32 | 15 casi PBH più 17 run aggiuntivi |
| `tep_exp3_v2_heldout/mode1/` | 30 | 24 fault e sei Normal |
| **Totale** | **108** | **104 contenuti distinti** |

Le quattro duplicazioni sono `mode1_1_1.xlsx`, `mode1_8_1.xlsx`, `mode1_10_1.xlsx`, `mode1_13_1.xlsx` fra le due cache. Le due cache comprendono complessivamente 46 percorsi e 42 contenuti distinti: 38 con un solo percorso e quattro con due percorsi.

N1–N5 sono i primi cinque blocchi da 50 ore del Normal da 500 ore, cioè **250 ore continue**, non cinque simulazioni indipendenti. N6–N10 appartengono alla stessa traiettoria. Non è stata stabilita l'indipendenza del separato file Normal da 50 ore rispetto a quella traiettoria.

### 4.2 I 17 run aggiuntivi

Sono il complemento dei 15 casi nel [manifest PBH](../../phase_b/heldout/phase_b_heldout_manifest.csv) all'interno dei 32 file held-out, non 17 file da aggiungere nuovamente al totale.

Tutti hanno percorso `tep_heldout/mode1/mode1_<fault>_11.xlsx`, 54 campi, tempo iniziale zero e griglia temporale di un minuto. I controlli hanno riguardato dimensioni, tempi e impronte, senza usare separabilità o attivazioni per scegliere i nuovi guasti.

| Fault | Byte | Righe dati | Fine (h) | SHA-256 |
|---|---:|---:|---:|---|
| F2 | 1704087 | 3001 | 50 | `1b36661790fe6467989b87d0e7afa02268655ae343af1117cc006f4c403954ac` |
| F3 | 1704410 | 3001 | 50 | `96a336d2ec6dda55741c9d3c4fe1695076cecb1751ef3b613e6e53ccbe68c1db` |
| F4 | 1704087 | 3001 | 50 | `58e65a6a5b9be2b55b90cb75c32cc5d3906d2285ea7fd526632e775867148773` |
| F5 | 1704228 | 3001 | 50 | `f2d0862c5a352d08f8b9f68347b26c487346b839de51c17a4a59acd1ca8c701d` |
| F6 | 582507 | 1029 | 17,1333333333 | `86275cb0327a8d250a348378e74afa98df72b77cf8d1d90155b2123df653366d` |
| F7 | 1704750 | 3001 | 50 | `713bcf3f3e36002b241a698af080a9c5c226b26da824862e749b322aac21b7f5` |
| F9 | 1704503 | 3001 | 50 | `4ddee0f471ee1cb19b73d439b6ca836cb2843fcf49a1f331a7ea893903b2252f` |
| F11 | 1708626 | 3001 | 50 | `2b203b1111503ad853e8fbc4192ba6efca6604ab227140af9841bbc277d20c41` |
| F12 | 1706546 | 3001 | 50 | `f491e45be674c5e9ecd5f855b9ec1c9f8f10dfb214ec82688f9d43e3cbea9063` |
| F14 | 1707075 | 3001 | 50 | `b6606b26cd5d5aa009573765a020d8a1a23eefc4bb1c654529119eb57b19b5a3` |
| F15 | 1704671 | 3001 | 50 | `ee177dfb69992719933f04f814d26c1034e9e67bb9d4aa1d04a4c186a60660fa` |
| F16 | 1704957 | 3001 | 50 | `dd8f8f51686d9588bcc89bfac0286860d6cfdf6100caec82bbe52e178afdad23` |
| F17 | 1706431 | 3001 | 50 | `28fba76dd0f0502bd29d1f091283794133bf0c58ad09b38ebc90b724591fc6dc` |
| F18 | 1706329 | 3001 | 50 | `916c36c086c704eee2f236be9826fb278f4ed8846ac1d574964d2361778a71f2` |
| F19 | 1706690 | 3001 | 50 | `c9c70ba8f0fae1500a5aecc0c23236e3178b2638e7d45c8401af3eed404bfda7` |
| F20 | 1708359 | 3001 | 50 | `4f69b18e79bc0a94d8b289eb34ec65c2fec6bd543de8b0c1e20d367f6577fa20` |
| F21 | 1704508 | 3001 | 50 | `69194ad481309bf89f0405842639ee382b574940e9afad6ed05bf49f2118b075` |

La nota locale `tep_heldout_phase_summary.md`, §12, documenta per F6 il trip fisico «Low Stripper Liquid Level!! Shutting down.» e la decisione di non rigenerarlo selettivamente. Non sono autorizzati padding, troncamento o esclusione metodologica automatica. Il riepilogo della generazione è in [HELDOUT_GENERATION_SUMMARY.md](../../phase_b/heldout/HELDOUT_GENERATION_SUMMARY.md).

«Non incluso nel manifest PBH» non equivale a «mai osservato»: l'ispezione tecnica è documentata; l'assenza di osservazione scientifica non è certificata. Il seed dei 17 run non è ricostruito dagli artefatti esaminati. Il riferimento al simulatore non va scambiato per un commit che conservi i loro dati.

### 4.3 Recuperabilità e conservazione

Sono state confrontate 46 copie di cache con dimensioni e SHA-256 dei puntatori LFS del dataset al commit `309b944f35ac440ff0c70616947ffe723c766e14`: corrispondenza verificata. I puntatori non conservano il contenuto. Lo store LFS locale dell'upstream risulta vuoto; la disponibilità remota dei contenuti non è stata verificata. L'assenza di git-lfs segnalata dal riesame è una limitazione dello strumento disponibile, non una prova di indisponibilità di ogni possibile canale di recupero remoto.

| Gruppo | Contenuti distinti | Conservazione Git verificata |
|---|---:|---|
| Due cache | 42 | Non riscontrata |
| Held-out PBH e 17 aggiuntivi | 32 | Non riscontrata |
| EXP3_V2 | 30 | Presente nel tag `exp3-v2-heldout-data-frozen-001` |
| **Totale** | **104** | **30 conservati; 74 non conservati in Git** |

I 30 blob EXP3_V2 sono XLSX reali, non puntatori; tutti coincidono per SHA-256 con le copie locali. Il riesame indipendente ne riporta 51.188.047 byte e conferma che sono gli unici 30 blob XLSX distinti raggiungibili nei ref esaminati. Non compaiono nell'indice corrente: la presenza nella storia e la presenza nel checkout sono verifiche diverse. La conservazione nel Git locale non dimostra un backup esterno o la piena conformità del repository finale alla §8.5.

**Prima attività successiva alla chiusura:** mettere in sicurezza i 74 contenuti con una copia recuperabile verificata e registrarne posizione e impronte, prima di ulteriori letture operative o spostamenti di quei file. Vi rientrano N1–N5, i venti run candidati a R1, i quindici PBH e i diciassette run aggiuntivi. Gli hash già calcolati non sostituiscono tale copia. La messa in sicurezza non è stata eseguita durante questa macrofase né durante la redazione del report.

## 5. Derivati ed esecuzioni recuperati

Fra i materiali in [tep_analysis_v2](../../code/tep_analysis_v2) sono stati individuati 820 record di feature per caso, 6.560 record di feature per finestra dei venti fault di sviluppo, 820 firme temporali, 2.050 record Normal per variabile/finestra e 50 massimi Normal. Sono granularità diverse, non campioni indipendenti da sommare.

Sono disponibili testi e strutture di validation/test, dei 15 PBH e dei 30 EXP3_V2; quattro raccolte di esempi locali con dieci esempi sorgente distinti; otto insight finali con input, risposte e metadati; librerie derivate B/E/A+ e pooled; prototipi numerici, predizioni e otto modelli centralizzati salvati. Per EXP3_V2 parte del materiale è nei tag e non nel working tree.

Il conteggio recuperato delle esecuzioni diagnostiche è:

| Gruppo | Record |
|---|---:|
| Exp1 A/B/E | 540 |
| Exp2 Qwen A/B/E, stessi PBH | 540 |
| EXP3_V2 A/B/E | 1.080 |
| A+ | 180 |
| C pooled | 45 |
| Ablazione delle rappresentazioni | 180 |
| Screening local-first | 72 |
| Local-first completo | 360 |
| Follow-up sensitivity Qwen a 4096 | 5 |
| **Totale** | **3.002** |

Il patrimonio di questi record riguarda **45 casi fisici distinti: 15 PBH e 30 EXP3_V2**. Non sono 3.002 simulazioni, prove indipendenti o necessariamente 3.002 tentativi API: retry, ripetizioni, aggregazioni e riusi dello stesso caso vanno mantenuti distinti. Il controllo local-first completo riusa i 30 casi EXP3_V2; non è una nuova conferma su altri dati.

I cinque record aggiuntivi sono nel riferimento `origin/codex/qwen-reasoning-cap-sensitivity`, commit `d4f4708ccf67b7b58320dca465fe0b28a8d22cc2`, sotto `phase_b/exp2/qwen/sensitivity/capped_followup/`. I record grezzi dello sweep precedente non sono stati recuperati: le tabelle che lo descrivono non sono conteggiate come record disponibili. Il follow-up ha quattro risposte corrette su cinque, non cinque su cinque; eventuali discordanze narrative restano da correggere nelle sedi autorevoli.

Le evidenze EXP3_V2 sono raggiungibili tramite `exp3-v2-results-frozen-001` e i tag delle rispettive fasi. Sono state verificate le nove dipendenze del manifest conclusivo e i tre payload dei risultati; questo non equivale a una verifica ricorsiva di ogni artefatto. L'integrazione finale deve rispettare MAINTENANCE §8.5 senza dipendere da branch temporanei.

## 6. Compatibilità e ruoli di riuso

### 6.1 Controllo numerico della baseline

Il controllo in memoria, senza scrittura di nuovi artefatti, ha ricostruito la baseline per sensore su tutti N1–N5 e verificato la coincidenza con quella caricata dal verbalizzatore. Ha riprodotto le feature Normal archiviate con la procedura leave-one-block-out, con scarto massimo dell'ordine di `1,41e-12`. Tutti i 2.050 valori di ciascuna delle quattro feature differiscono invece oltre `1e-12` rispetto al calcolo con baseline fissa su tutti i blocchi.

| Feature | Massimo scarto assoluto fra archivio LOBO e baseline fissa |
|---|---:|
| abs_shift_sigma | 0,1395248782 |
| abs_slope_sigma_h | 0,0317945538 |
| residual_std_ratio | 0,0556652197 |
| diff_std_ratio | 0,0298025431 |

Conseguenza: si riusano i dati Normal, ma si ricalcolano le feature necessarie al nuovo score con la funzione fissa. Non sono state selezionate operativamente A/A′, calcolate nuove soglie o validate integrazioni in produzione.

### 6.2 Classificazione degli artefatti

| Materiale | Ruolo assegnato |
|---|---|
| N1–N5 | Baseline prevista dal registro, subordinata alla guardia pilota; proposta R2 per lo sviluppo Normal |
| Venti fault di sviluppo | Candidati prioritari a R1, subordinati alla compatibilità del processo di generazione |
| Altri dati già valutati | Controlli, sviluppo e risultati descrittivi eventualmente pertinenti; nessuna promozione a nuova conferma indipendente |
| Diciassette run aggiuntivi | Sviluppo potenziale dopo la scelta dei guasti e la verifica di ammissibilità |
| Feature dei fault prima delle soglie | Riutilizzabili se dati, baseline, finestre e formule coincidono |
| Feature Normal LOBO | Ricalcolo necessario per applicare la nuova baseline fissa |
| Soglie archiviate | Riproduzione e controllo; non sostituiscono la nuova calibrazione |
| Firme 697-D, testi ed esempi | Ricostruzione o verifica di identità dopo baseline/soglie definitive; elaborazione deterministica |
| Otto insight esistenti | Riferimento di sviluppo; riuso diretto nel nuovo protocollo non dimostrato |
| Predizioni e metriche esistenti | Conservazione e possibile uso descrittivo con ruolo esplicito; non sostituiscono Q8 |
| Prototipi e modelli salvati | Ricette e componenti recuperabili; aggiornamento dei prototipi e addestramento per nove classi |
| Codice e politica local-first | Base per adattamenti nel nuovo perimetro; non tutti i comandi sono eseguibili così come sono |

Gli insight esistenti sono prodotti da Terra. Il piano richiede due librerie complete da 16 insight con schema, cardinalità e cap controllati. La suite di modelli centralizzati a cinque classi non sostituisce FedAvg, né i suoi riferimenti locale e centralizzato sul nuovo compito.

La conversione algebrica di una soglia unica S in quattro soglie equivalenti per feature è strutturalmente possibile per le trasformazioni monotone previste dal registro; non certifica l'integrazione nel verbalizzatore. Il pilot Normal non certifica la compatibilità delle traiettorie fault. Il Ts_base storico di N1–N5 resta non ricostruito; quello documentato in un diverso snapshot del simulatore non può essergli attribuito automaticamente.

## 7. Perimetro proposto dei dati

**R1 — Proposta distinta:** riusare i venti run di sviluppo F1/F8/F10/F13, batch 1–5, invece di rigenerarli. Il piano §6.2 ne prescrive ancora la rigenerazione.

**R2 — Seconda proposta distinta:** sostituire i cinque nuovi Normal di sviluppo con N1–N5. Va riconciliata con §§6.2–6.3 del piano e collegata al requisito residuo 4 del registro rev. 18. Il riuso di N1–N5 come baseline nel registro non formalizza automaticamente il loro ulteriore ruolo di sviluppo.

L'OK alla ricognizione non adotta R1 o R2. Le loro verifiche di compatibilità e la decisione dell'autore restano esplicite.

| Insieme | Perimetro |
|---|---|
| baseline_fit | N1–N5, statistiche di riferimento e normalizzazione dello score |
| Sviluppo Normal, se adottata R2 | N1–N5 per esempi e baseline numeriche; N1–N2 come sorgenti degli esempi locali |
| Sviluppo fault | Cinque casi per ciascuno degli otto guasti; recuperare quelli ammissibili, completare il mancante |
| Pilota della calibrazione | Dieci nuovi run Normal, esclusi da ogni altro utilizzo |
| cal_thr | 350 nuovi run Normal, una finestra di cinque ore per run, posizione uniforme fra dieci |
| far_ver | 150 nuovi run Normal; verifica primaria su una finestra per run, secondaria su tutte le 1.500 finestre con dipendenza intra-run gestita |
| Test diagnostico | 54 oppure 72 nuovi run, distinti dallo sviluppo, più sei fuori catalogo |
| Pilot LLM e controlli tecnici | Materiale di sviluppo; attività distinta dai dieci run pilota della calibrazione |

La forma economica di cal_thr richiede la verifica numerica dei prefissi; in caso di mancata accettazione si usa la forma completa. Il burn-in non ha ancora durata e criterio operativi fissati.

Se la guardia pilota impone di ricostruire la baseline, il registro prevede 100 nuovi baseline, 300 cal_thr, 150 far_ver e dieci pilota: **560 run**. È stata ritirata l'assegnazione automatica di cinque dei cento baseline allo sviluppo, perché il registro non la stabilisce. Il budget del ramo alternativo mantiene cinque nuovi Normal dedicati allo sviluppo, salvo futura decisione esplicita.

La scelta dei quattro guasti nuovi deve precedere l'uso dei loro risultati per progettare lo studio. Si fonda su meccanismi fisici e difficoltà documentata in letteratura; non su disponibilità dei file, separabilità o attivazioni nei dati propri. OOD, coppie local-first e mappa E5 dipendono dal catalogo finale.

## 8. Lavoro nuovo e budget corretto

### 8.1 Simulazioni

Al livello minimo di cinque casi di sviluppo per classe:

`N = B + (40 − r) + u + 9n + 6 + D`

- B: 510 nel ramo principale o 560 nell'alternativo, inclusi i dieci pilota.
- r: run fault di sviluppo effettivamente recuperati. Nel perimetro locale attuale r ≤ 24; può essere inferiore per incompatibilità o per il trattamento ancora da decidere dei trip.
- u: nuovi Normal dedicati allo sviluppo; nel ramo principale u=0 richiede R2, altrimenti u=5. Nell'alternativo si mantiene u=5 salvo decisione esplicita.
- n: sei oppure otto run per classe nel test diagnostico, Normal incluso.
- 6: run fuori catalogo.
- D: diagnostiche e validazioni ancora da dimensionare; non assunto zero.

| Scenario | Sei run per classe, prima di D | Otto run per classe, prima di D |
|---|---:|---:|
| B=510, r=20, u=5 | 595 | 613 |
| B=510, r=20, u=0 | 590 | 608 |
| B=510, r=24, u=5 | 591 | 609 |
| B=510, r=24, u=0 | 586 | 604 |
| B=560, r=20, u=5 | 645 | 663 |

**590** significa esclusivamente lo scenario principale con venti fault riusati, R2 adottata, sei run di test per classe e D escluso. Non è un tetto definitivo. Nel confronto con tale scenario, il ramo alternativo dell'ultima riga aggiunge 55 run: 50 per il cambio di B e cinque per u.

I precedenti 570/588 richiedevano r=40: sono **ritirati dal budget operativo**, irraggiungibili con r≤24. Un recupero esterno potrebbe ampliare il censimento, ma richiederebbe contenuti effettivamente recuperati e verificati; i puntatori non autorizzano quel risparmio.

R1 e R2 insieme eviterebbero 25 simulazioni di sviluppo rispetto alla rigenerazione integrale, subordinatamente alle rispettive condizioni. I 17 run aggiuntivi offrono al massimo un candidato per ciascuna delle quattro nuove classi, non diciassette sostituzioni delle venti simulazioni mancanti.

### 8.2 Ricalcoli e chiamate LLM

Nel perimetro diagnostico sono previsti 45 casi di sviluppo e 60 oppure 78 casi di valutazione: **105/123 casi da rappresentare**, non necessariamente tutte nuove simulazioni. Il conteggio esclude gli score degli insiemi di calibrazione, le varianti E5 e i controlli tecnici. Feature compatibili possono essere riutilizzate. Testi neutrali, firme, score e prototipi sono elaborazioni deterministiche; FedAvg e i riferimenti numerici richiedono addestramento, non chiamate LLM.

| Budget API corrente di §8.8, nucleo R=1 | Sei run | Otto run |
|---|---:|---:|
| Nucleo A/B-LF/E-LF | 1.296 | 1.728 |
| Audit R=3 sul 10% del nucleo | ~260 | ~346 |
| Producer-swap, inclusa generazione alternativa | 188 | 244 |
| Ablazione B senza local-first | 132 | 148 |
| E5, accantonamento parametrico | 144 | 192 |
| Fuori catalogo | 144 | 144 |
| Produzione insight principale | ~30 | ~30 |
| Capability pilot | ~200 | ~200 |
| Controlli tecnici | ~100 | ~100 |
| Canary | ~100 | ~100 |
| **Totale** | **~2.594** | **~3.232** |
| **Con margine 10%** | **~2.853** | **~3.555** |
| **Tetto di pianificazione corrente** | **3.000** | **3.700** |

Le precedenti predizioni non riducono direttamente il budget Q8. Il riuso interno FULL=B-LF evita fino a 48/64 chiamate aggiuntive soltanto se coincidono caso, ricevente, prompt completo, modello/configurazione, decoding e aggregazione. Senza riuso di FULL da B-LF, il piano stima circa 2.906/3.626 chiamate incluso il margine. E5 resta parametrico; se il pilot impone R=3 nel nucleo, il budget va rivisto.

Due insight per richiesta, come nel meccanismo esistente, consentirebbero 16 richieste nominali per le due librerie complete: è una possibilità operativa, non una misura acquisita sul nuovo protocollo. Si conservano i margini del piano.

### 8.3 Discordanze documentali da correggere prima della decisione sei/otto run

La coppia obsoleta 2450/3040 è ripetuta nel piano in §§1, 2, 7, 8.9, 10 e 13 e una stima precedente è entrata nel walkthrough studio 2. Il riesame ne segnala le righe 119, 164, 324, 609, 1027 e 1369 del piano e la riga 106 del walkthrough nello stato esaminato. I riferimenti di riga sono localizzatori di quello snapshot, non identificatori stabili.

Il tetto a otto run è inoltre 3.700 in §8.8 ma ancora 3.500 in altri passaggi, compresi T5 e O2 della checklist GO/NO-GO. Il subtotale corrente con retry, ~3.555, supera 3.500: occorre riconciliare i criteri **prima della decisione D2**, non dopo la scelta del campione.

Il delta fra i totali correnti è **638 chiamate, circa 24,6%**. Il «+590 chiamate» del piano deriva dalle stime precedenti ed è distinto dalle 590 simulazioni dello scenario definito sopra. Il presente report registra le discordanze; non le corregge nelle fonti autorevoli.

## 9. Perimetro operativo e rilievo sui percorsi

Il contratto vigente prescrive **studio2/** come radice unica di tutto il nuovo codice, configurazioni, test, manifest, esecuzioni e risultati. Le precedenti proposte `code/studio2/` e `outputs/studio2/` sono ritirate. Piano, registri, letteratura e walkthrough restano nelle sedi autorevoli. Il registro di provenienza previsto è `studio2/PROVENIENZA.md`, non ancora creato da questo lavoro.

Il controllo statico dei percorsi predefiniti ha **esito negativo accertato**:

- [tep_characterize_v2.py](../../code/tep_characterize_v2.py) definisce `OUTPUT_DIR = Path("tep_analysis_v2")` a riga 39;
- le scritture da riga 203 non impediscono la sovrascrittura;
- lo script non espone un parametro a riga di comando per cambiare la destinazione;
- eseguito da `code/`, scriverebbe in `code/tep_analysis_v2/`, dove sono gli artefatti esistenti.

Lo script **non è un comando riutilizzabile così com'è** per studio 2. È escluso dall'esecuzione diretta; l'adattamento dovrà essere un file nuovo dentro studio2/, con destinazioni esplicite e protezione delle aree congelate. L'originale non è stato eseguito o modificato per risolvere questo rilievo. La chiusura della ricognizione certifica l'identificazione del problema, non la sua correzione implementativa.

Per la prossima modifica concordata di MAINTENANCE §8 restano due precisazioni documentali: nominare esplicitamente i dati nel perimetro §8.1 e stabilire la forma ammessa per metadati non ricostruibili in §8.2. Il principio operativo rimane dichiarare il dato mancante, senza inventare seed, data o commit di conservazione.

## 10. Verifica indipendente e chiusura

La prima verifica ha dato **NON OK**, riaprendo inventario, budget e perimetro operativo. Sono seguiti il censimento individuale dei 17 run, l'esplicitazione di R1/R2, la correzione della formula con u, il ritiro degli scenari non raggiungibili, la verifica negativa dei percorsi e l'allineamento alla §8.

Il secondo riesame, fornito dall'autore in conversazione, conclude:

> OK alla chiusura della ricognizione 1–7

Il riesame conferma che i rilievi sono risolti al livello della ricognizione e che le attività residue appartengono al seguito del lavoro. Precisa che la lacuna di conservazione non blocca la chiusura conoscitiva, ma richiede la priorità operativa indicata in §4.3. Il testo ricevuto ha SHA-256 `0ea4657e4e82cc797aaeb1861ac50859c5252327e7e405dd98aca7a379519ee6`; era un allegato della conversazione, non un artefatto già integrato nel repository. Questo report ne conserva il verdetto, il perimetro e i rilievi residui, non pretende di conservarne il testo integrale mediante la sola impronta.

L'OK riguarda il lavoro di ricognizione descritto, **non una revisione indipendente della successiva redazione di questo report** e non un'approvazione automatica delle revisioni al disegno.

Restano integralmente da realizzare Ts_base operativo, durata e criterio del burn-in, implementazione e validazione Philox, score eseguibile e casi degeneri, verifica dei prefissi e congelamenti degli artefatti effettivamente usati. Restano aperte, prima dei rispettivi passaggi, scelta dei guasti nuovi, numero di run, margine di non inferiorità, schema degli insight, politica sulle ripetizioni, OOD, coppie local-first e dettagli E5. Nessun valore mancante è stato scelto per completare artificialmente la ricognizione.

## 11. Perimetro di questa consegna e commit

L'autore ha autorizzato espressamente la creazione del presente report in `studio2/fase01/REPORT_FASE01.md`. È aggiunto il solo riferimento alla nuova cartella nella mappa di `DOCUMENTATION_INDEX.md`, come richiesto dal contratto per un cambiamento strutturale. Non sono aggiornati walkthrough, piano, registri, MAINTENANCE o artefatti congelati; le modifiche documentali più ampie richiedono ancora l'accordo sui dettagli.

Non sono letti nuovamente, spostati o ricalcolati i 74 contenuti grezzi non conservati per redigere il report: le tabelle riportano i controlli già eseguiti e riesaminati. Non è stata creata una copia di sicurezza in questa consegna.

Verifiche della consegna completate: **12 collegamenti locali del report risolti**, nuovo riferimento alla cartella nell'indice verificato, 17 righe del censimento con SHA-256 formalmente validi, `git diff --check` e controllo equivalente sul report nuovo senza rilievi. Il guardiano documentale riporta prima e dopo la modifica **35 test, 14 fallimenti preesistenti e uno skipped**: nessun aumento dei fallimenti. Non sono stati corretti problemi estranei.

**Raccomandazione sul commit:** salvare questo consuntivo e la relativa voce strutturale in un commit dedicato, dopo i controlli, senza includere modifiche estranee. Messaggio proposto: `studio2(fase01): documenta ricognizione e verifica indipendente`. Nessun commit o tag di congelamento è stato eseguito per questa consegna.
