# Review critica del nuovo piano sperimentale FoT-TEP

**Reviewer:** indipendente (simulato)
**Data prima stesura:** 11 settembre 2026
**Revisione 2:** 11 settembre 2026 — consolidata dopo tre cicli di correzione dell'autore
**Revisione 3:** 11 settembre 2026 — integrata la verifica critica del prior art federato (P065, P042, P041, P030, P031, P001)
**Oggetto:** Valutazione critica del piano sperimentale e definizione del piano consolidato
**Documenti esaminati:** fot_walkthrough_conversazione_v2.md (sezioni 0–15, in particolare §10.3), fot_walkthrough_v2.html, FoT_TEP_Review_Critica.md (registro critiche G1–G10, CF1–CF6), gap analysis, paper blueprint, CFP IEEE BigData 2026, SWaT dataset documentation (Goh et al. 2016, lista attacchi, glossario equipaggiamento), letteratura TEP sulla difficoltà per-fault (§12)

---

## 0 · Changelog della revisione 2

Questa revisione incorpora le correzioni dell'autore. Sono elencate qui perché diverse riguardano errori della prima stesura, non semplici raffinamenti.

| # | Correzione | Origine |
| --- | --- | --- |
| 1 | **G5 non è risolta.** La prima stesura la dichiarava "Risolve". Nello studio finale Qwen è sia producer sia consumer: la molteplicità di modelli è tra i due studi, non dentro il risultato. Riclassificata come mitigata. | autore |
| 2 | **Il conteggio delle chiamate era incoerente.** §2.5 contava 4 condizioni (4.032), §8 ne contava 3 (3.024). Il nucleo del piano originale costa **5.184** chiamate. | autore |
| 3 | **Il producer alternativo deve generare la libreria intera.** Generare insight solo per i fault confrontati produce un prompt a provenienza mista e confonde la manipolazione. | autore |
| 4 | **C06 non è risolta in anticipo**, ed è una **replica prospettica con protocollo congelato** di un effetto già misurato in §10.3, non un endpoint esplorativo. Il protocollo è congelato internamente, non registrato pubblicamente: «pre-registrata» sarebbe scorretto. | autore |
| 5 | **local-first resta istruzione nel prompt e diventa la definizione di B.** L'override esterno proposto in prima stesura è stato ritirato: richiederebbe un rilevatore locale e una soglia che non esistono nell'output attuale. | autore |
| 6 | **La selezione dei fault non deve dipendere dalla separabilità osservata nei propri dati.** Sostituita da stratificazione su difficoltà documentata in letteratura. | autore |
| 7 | **Il pilot non può dimostrare instabilità < 1%.** La soglia dell'1% è stata rimossa: il pilot è un gate tecnico. La regola del tre dà ≈2,5% come limite superiore al 95% con zero divergenze su 120 osservazioni. | autore |
| 8 | **Hash, timestamp e latenza non dimostrano un cambio di modello.** Aggiunti ID modello restituito, request ID, fingerprint e un set canary come strumento rilevativo. | autore |
| 9 | **Il test fuori catalogo va eseguito in tutte le condizioni**, non solo in B, altrimenti non dice se gli insight migliorano o peggiorano l'astensione. | autore |
| 10 | **SWaT è un benchmark candidato per lavori futuri**, non un "caso studio": non avremo risultati sperimentali su SWaT. | autore |
| 11 | Studio ponte, confronto Q4 e condizione A+ eliminati. | concordato |
| 12 | **F3/F9/F15 sono difficili da *rilevare*, non "quasi indistinguibili" tra loro.** Le fonti riguardano l'asse rilevazione (fault vs Normal), non discriminazione (fault vs fault). | autore |
| 13 | **F4 non è borderline: è dipendente dal metodo.** PHM 2023 lo rileva (DAE e SPE 100%, T² 18%); FaultExplainer lo esclude perché la *sua* PCA non lo vede. | autore |
| 14 | **I numeri di FaultExplainer vanno qualificati:** top-3, alias accettati, solo sui fault rilevati da PCA. | autore |
| 15 | **Il margine δ′ per C06 era ancora guidato dal risultato precedente.** Sostituito da due superiorità più una non inferiorità, con margine giustificato su basi esterne. | autore |
| 16 | **D8 risolta: sì a una baseline FedAvg minimale**, non FedProto. | autore |

### Revisione 3 — conseguenze del prior art federato

| # | Modifica | Origine |
| --- | --- | --- |
| 17 | **Schema degli insight congelato, tipizzato e con budget per-elemento** (§8.9). Nessuno dei sei lavori esaminati pubblica uno schema verificabile né misura la conformità. | P065, P042, P001 |
| 18 | **Parità strutturale obbligatoria fra producer** nel braccio swap: stesso schema, stesso numero di insight, stesso cap di lunghezza. Senza, "effetto producer" e "effetto verbosità" sono confusi. | P065, P031 |
| 19 | **E deve essere ottenuta modificando soltanto il campo pseudolabel**, con diff verificabile allegato. Controllo non osservato in nessuno dei sei lavori esaminati. | P041, P030, P031, P065, P042 |
| 20 | **Metriche di conformità** (validità schema, retry, parsing, troncamenti, token) aggiunte al logging. Nessuno dei sei le riporta. | tutti |
| 21 | **Novità riposizionata.** "Federare testo" e "trasferire conoscenza fra LLM" non sono sostenibili contro questo corpus. Le rivendicazioni che sopravvivono ai sei lavori esaminati sono la diagnosi local-unseen su serie temporali multivariate, lo spazio di etichette disgiunto, il confronto controllato con conoscenza semanticamente errata e la protezione dell'esperienza locale (§12.9). Sopravvivere a sei lavori non equivale a una lacuna del campo: serve una ricerca bibliografica più ampia. | tutti |
| 22 | **Confermato di NON introdurre** aggregazione, top-k, round multipli, confidence weighting e DP (§12.8), con motivazione citabile invece che per omissione. | P031, P030, P065 |

### Revisione 4 — verifica incrociata su letteratura e artefatti

| # | Modifica | Origine |
| --- | --- | --- |
| 23 | **Precedenze nella checklist §11.** S12 e S13 dipendono da S1; S5 da S17; S3 e S4 da S1–S2. La checklist elencava i requisiti senza il loro ordine, e §0.1 metteva le decisioni 1, 3 e 4 nello stesso gruppo «lavorabili oggi» senza ordinarle: alcuni prerequisiti risultavano risolvibili subito quando non lo sono, e la cronologia di §7 ne usciva ottimistica. | autore |
| 24 | **Unità statistica del gate R=1.** 40 prompt × 3 ripetizioni non sono 120 osservazioni indipendenti: l'unità è il prompt. Il limite della regola del tre passa da ≈2,5% a ≈7,5% (§8.7, D7). | verifica incrociata |
| 25 | **§8.10 punto 7 ridimensionato.** EviFDD-Agent pubblica sul TEP una tabella di conformità con intervalli di Wilson. Le due misure non coincidono — validità dello schema lato producer contro tracciabilità evidence-based del reporter — ma l'espressione «l'unica del suo genere fra i lavori comparabili» non è sostenibile. | verifica letteratura |
| 26 | **P065 va ristretto in tre punti**: scala a 500 client e non a 5 (§5 G2); riporta un pavimento Local-Only (§9.3); è il caso più vicino al claim local-unseen (§12.9 claim 2). | verifica letteratura |
| 27 | **FedProto: previsione tolta.** «Un secondo numero quasi identico al primo» non è dimostrabile — FedProto apprende anche la rappresentazione e aggrega Normal. La ridondanza è concettuale, non empirica. D8 regge. | autore |
| 28 | **Due comparatori FL già pubblicati su TEP mancavano in §9**: Zhang et al. 2026 e Xu et al. 2026, entrambi 🟢 in §14.1. | verifica letteratura |
| 29 | **Secondo vincolo sui due fault OOD** (§8.6, S13): il gruppo compensato dal controllo produce evidence quasi vuota, quindi astensione per assenza di segnale invece che per riconoscimento di novità. | verifica letteratura |
| 30 | **«sei lavori federati» → «sei lavori esaminati»**: cinque sono federati, P001/ACE è mono-agente, come §12.6 già dichiara. | verifica incrociata |
| 31 | **S11b esplicitata**: i tre numeri dell'endpoint vanno calcolati e riportati separatamente per A, B-LF ed E-LF. | autore |
| 32 | **§8.9 rafforzata** con la frase di P001 sulla stabilità 10K–100K e con i due riscontri operativi di EviFDD (identificatori di variabile, serializzazione deterministica). | verifica letteratura |

### Revisione 5 — verifica sugli artefatti congelati e sul codice

| # | Modifica | Origine |
| --- | --- | --- |
| 33 | **D10 risolta nella forma.** `Unknown` è congelato come nome dell'astensione già implementata (`abstain=true`, `predicted_label=null`), non come label letterale. La strada letterale richiederebbe di sostituire l'idioma posizionale `label_space[:-1]` — undici occorrenze, incluse quelle che governano derangement ed E — con categorie semantiche esplicite, e di riscrivere i test perché verifichino la separazione invece di riprodurla. | verifica codice |
| 34 | **Il trade-off di §8.6 non si applica.** «L'esplorativo non aveva `Unknown`» è falso sugli artefatti: `primary_metrics.csv` mostra 14 astensioni su 36 in A, un tasso misurato separatamente e un'accuratezza che già conta l'astensione come non-corretta. Il confronto descrittivo resta indebolito da scala, modello e contesto, non dallo spazio delle etichette. | `phase_b/final_evaluation/` |
| 35 | **S11b costa una metrica, non tre.** Due dei tre numeri dell'endpoint esistono già negli artefatti e nell'evaluator; manca solo l'accuratezza sui soli casi non astenuti, assente da entrambi i file di metriche. | verifica artefatti |
| 36 | **Il carico di simulazione è riconciliato col disegno conformal** (§8.8): 750 run con 6 per fault, 768 con 8, inclusi 150 run di qualifica già completati; il residuo è 600/618. Non consuma chiamate API ma è un secondo percorso critico indipendente da Qwen. | verifica dati |
| 37 | **Capacità dell'API registrate nel pilot** (§8.7, T10), con la regola che l'assenza di temperatura e seed non è una divergenza osservata e non attiva R=3 da sola. La politica conservativa, se voluta, è una nuova decisione da pre-specificare (§0.1, decisione 11). | `execution_config.json` |

---

### Revisione 6 — registrazione dell'ablazione dei descrittori di Fase A (2026-09-12)

| # | Modifica | Origine |
| --- | --- | --- |
| 38 | **Registrata in §8.12 l'ablazione testuale dei descrittori di Fase A**, approvata come disegno il 2026-09-11 e **non congelata**: restano aperti effetto minimo, run per fault e criterio di successo esatto (E5-C, decisione 12 di §0.1). Le sotto-decisioni usano il prefisso `E5-` per non collidere con il namespace D1–D12 di §10. | autore |
| 39 | **Il drift lento ha un solo fault documentato, IDV(13).** La copertura a due fault per meccanismo è insoddisfacibile per il drift; si adotta **un solo fault per il meccanismo slow drift**, con più run indipendenti, e **la conclusione va enunciata su IDV(13), non sui drift lenti in generale**. Vincola D1 (§10) oltre che §8.12. | verifica Downs & Vogel |
| 44 | **Tracciata in §0.1 la decisione di conservare i quattro descrittori di Fase A** (2026-09-11). La decisione viveva solo in un documento di rassegna; ora è rintracciabile dal piano autorevole, con rimando alla motivazione e senza duplicarla. | autore |
| 43 | **E5-C2 fissata in via provvisoria: scarto relativo ≤ 5% per caso** sul prompt completo, tokenizer del modello usato, zero differenze di troncamento; una sola violazione declassa il contrasto della famiglia. Soglia operativa, non statistica. Richiede una **verifica di fattibilità sui dati di sviluppo prima del freeze**, perché la regola è a scatto singolo e non rimediabile dopo. | autore |
| 42 | **E5-C1 chiusa: Δ ≥ 0,10** — 10 punti percentuali assoluti di accuratezza top-1 sul meccanismo bersaglio, soglia di **rilevanza pratica** e non di significatività, indipendente da modello e numerosità. Effetti inferiori si riportano ma non sostengono la necessità del descrittore; effetti negativi si riportano col segno. | autore |
| 41 | **IDV(13), via scelta: risultato esplorativo senza run dedicati.** E5 eredita D2; aggiungere run del solo IDV(13) richiederebbe riaprire D2 esplicitamente. Ne segue che il criterio di successo di E5-C è **a due livelli**: inferenziale per le famiglie con copertura sufficiente, sola stima descrittiva per `slope_sigma_h`. | autore |
| 40 | **Motivazione bibliografica** in `docs/lit_review/criteri_scelta_descrittori.md`: nessun criterio di selezione dei descrittori esiste in letteratura; l'argomento disponibile è di progetto (chiusura sui canali di perdita) più un'ipotesi da verificare. | `docs/lit_review/` |

---

## 0.1 · Decisioni ancora da congelare

La revisione precedente lasciava intendere che restasse aperta solo D8. Non è così. Queste sono **tutte** le decisioni che devono essere prese e congelate prima di aprire i run di test, con il riferimento alla sezione che le discute.

| # | Decisione | Dove | Stato |
| --- | --- | --- | --- |
| 1 | **Quali 4 fault nuovi**, oltre ai 4 di continuità | D1, §12 | ⬜ aperta |
| 2 | **6 o 8 run per fault** — prezzata: +590 chiamate, +24% | D2, §8.8 | ⬜ aperta |
| 3 | **Quali 2 fault fuori catalogo**, meccanicamente distinti da tutto il catalogo e con rilevabilità documentata | §8.6, S13 | ⬜ aperta — **dipende dalla 1** |
| 4 | **Sottoinsieme dell'ablation local-first**: quali coppie confondibili | D11, §8.3 | ⬜ aperta — **dipende dalla 1** |
| 5 | **Margini statistici**: il margine *m* di non inferiorità per H3, e la gerarchia di test | §8.5, S10–S11 | ⬜ aperta |
| 6 | Baseline FL | D8, §9 | ✅ **risolta: FedAvg minimale** |
| 7 | local-first | D6, §8.2 | ✅ risolta: B-LF è il metodo |
| 8 | R=1 o R=3 | D7, §8.7 | ⏳ subordinata al gate del pilot |
| 9 | Modello | D9, §7 | ⏳ data limite **17 settembre** |
| 10 | **Schema degli insight**: campi, cardinalità, cap per-elemento, validatore | §8.9, D12 | ⬜ **aperta, lavorabile oggi** |
| 11 | **Politica conservativa su R=3** in assenza di controlli di determinismo dell'API | §8.7, D7 | ⬜ aperta — da pre-specificare **prima** del pilot |
| 12 | **Ablazione dei descrittori**: effetto minimo (E5-C1), soglia di lunghezza (E5-C2), criterio di successo (E5-C3) | §8.12 | ⬜ parziale — **E5-C1 ✅ (Δ ≥ 0,10)**; **E5-C2 ⏳ provvisoria (≤ 5% per caso)**, si chiude dopo la verifica di fattibilità; **E5-C3** aperta, dipende dalla 1, dalla 2 e dalle altre due |
| — | **Conservare i quattro descrittori calibrati di Fase A, più `rapid` derivata**, anziché sostituirli | `docs/lit_review/criteri_scelta_descrittori.md` §5.1 | ✅ **risolta (2026-09-11): si conservano.** Motivazione lì, verifica dell'utilità diagnostica in §8.12 |
| — | **Pre-impegno sugli esiti di E5** | §8.12 · `docs/lit_review/DECISIONE_SCELTA_FEATURE_fase_A.md` §4 | ✅ **registrato 2026-09-12.** Gli esiti di E5, inclusi effetti nulli, negativi o discordanti, saranno riportati senza modificare retroattivamente descrittori, soglie, sottoinsiemi o criteri. Eventuali revisioni successive saranno dichiarate esplorative; una loro verifica prospettica richiederà dati non utilizzati per deciderle |
| — | Forma di `Unknown` | D10, §8.6 | ✅ **risolta: nome dell'astensione esistente** |

La decisione 10 è nuova nella revisione 3 e appartiene al gruppo indipendente dal modello: va congelata prima della produzione degli insight, non prima dei run di test, perché vincola *come* gli insight vengono generati da entrambi i producer.

Le prime cinque **non dipendono dalla disponibilità di Qwen**, ma non sono tutte lavorabili nello stesso momento. ⚠️ **Le decisioni 3 e 4 dipendono dalla 1.** «Meccanicamente distinto da tutto il catalogo» e «coppia confondibile» sono entrambe definite *rispetto agli 8 fault*, che è la 1 a fissare: scriverle come prerequisiti autonomi le fa sembrare risolvibili oggi quando non lo sono. Il cammino reale è: §6.1 congela i criteri → la 1 estrae gli 8 fault → solo allora si chiudono la 3 e la 4. Le decisioni 2 e 5 sono invece indipendenti e procedono in parallelo. Le decisioni 1, 3 e 4 vanno prese guardando soltanto Downs & Vogel e la letteratura di §12; la 5 guardando soltanto considerazioni operative e la risoluzione del disegno. Nessuna delle cinque può essere presa dopo aver visto un risultato.

---

## 1 · Giudizio generale

Il piano originale era ambizioso e affrontava con serietà le debolezze più gravi dello studio esplorativo Terra: scala ridotta (G2), unico producer (G5), degradazione dei local-seen (C06) e dipendenza delle conclusioni da un solo modello. La struttura a tre blocchi — esplorativo, ponte, finale — era logicamente corretta ma sovradimensionata: decine di condizioni, oltre cinquemila chiamate e un modello non ancora disponibile, con deadline al 30 settembre.

Il piano consolidato (§8) elimina il ponte, il confronto Q4 e la condizione A+; riduce le condizioni a tre; subordina R=1 a un gate tecnico; e reinveste il risparmio in due bracci che **mitigano** le due sole critiche non strutturali rimaste aperte. Il risultato è uno studio **più forte a meno della metà del costo**: circa 2.450 chiamate contro 5.184 di solo nucleo nella versione originale, con G5 e G6 rese misurabili invece che soltanto dichiarate come limiti. Nessuna delle due viene chiusa: la parola corretta, coerente con la tabella di §5, è *mitigare*.

Il prior art federato esaminato nella revisione 3 (§12.6–12.9) **rafforza il disegno ma non ne cambia i limiti**: conferma che schema congelato, parità fra producer, controllo con conoscenza errata e conformità misurata sono le scelte giuste, e al tempo stesso non risolve lo **scope FL** (CF1/CF5 resta aperta), non risolve la **scala** (G2 è mitigata moderatamente: otto agenti restano pochi) e non tocca la **validità esterna**, che resta limitata a un benchmark simulato.

Restano rischi scientifici aperti — lo scope FL (CF1/CF5), la scala (G2), la validità esterna e l'esito stesso delle baseline, che potrebbero non essere favorevoli. Il rischio **operativo** più urgente è invece temporale, e si concentra su una sola data: §7.

---

## 2 · Problemi e confondenti del piano originale

### 2.1 Dipendenza da un modello non ancora disponibile

Tutto il piano ruota attorno a Qwen3.8-2.4T-A95B, che non è ancora accessibile via API. Non sappiamo se il modello sarà stabile, se il formato delle risposte sarà compatibile con il parser esistente, se i token di ragionamento saranno sufficienti, né se il comportamento con 14 insight simultanei sarà accettabile. Nessuna pianificazione dettagliata può sostituire il capability pilot.

**Rischio:** se il modello si rivela inadatto (parsing instabile, troncamento del ragionamento, latenza proibitiva, cambiamenti del modello durante l'esperimento), l'intero piano finale crolla. Il piano B è ora esplicito e datato: D9 in §10.

### 2.2 Selezione post-hoc dei fault

Il piano prevede di passare da 4 a 8 fault. La scelta dei 4 fault aggiuntivi rischia di essere influenzata dalla conoscenza dei risultati sui primi 4 (F1, F8, F10, F13).

**Chiarimento della revisione 2.** F1, F8, F10 e F13 non diventano retroattivamente post-hoc: sono stati scelti prima dell'esplorativo e la loro selezione non era outcome-dependent. Vanno dichiarati come **quattro fault di continuità**. I quattro nuovi devono essere scelti con criteri congelati.

**Correzione importante.** La prima stesura elencava tra i criteri la "separabilità sulle feature di sviluppo". Questo criterio va **eliminato**: la separabilità in sviluppo correla fortemente con l'accuratezza in test, quindi selezionare su di essa è selezione sull'outcome anche se i dati non sono quelli di test. La sostituzione è la stratificazione su difficoltà **documentata in letteratura** (§12), che usa informazione esterna e preesistente.

### 2.3 Contaminazione temporale tra ponte e finale

Il problema è risolto per eliminazione: il ponte non esiste più nel piano consolidato. La sua funzione — verificare che il trasferimento regga con un producer diverso — è assorbita dal braccio producer-swap, che però opera su **dati vergini** e dentro lo studio finale, quindi ha valore inferenziale invece che solo diagnostico.

Resta valida la regola generale: qualsiasi decisione presa dopo il capability pilot che modifica il protocollo va documentata come decisione di progettazione, non come risultato indipendente.

### 2.4 L'illusione della separazione Q4–Q8

Il confronto Q4–Q8 sugli stessi run non isola un singolo fattore. Passando da Q4 a Q8 cambiano contemporaneamente sei variabili: numero di agenti (4→8), numero di fault (4→8), insight per ricevente (6→14), spazio delle pseudolabel (5→9), numero di distrattori (3→7), lunghezza del contesto. Non è un'ablazione, è un confronto tra due configurazioni. Approfondito in §4. **Q4 è eliminato dal piano consolidato.**

### 2.5 Costo del piano originale — conteggio corretto

La prima stesura conteneva un'incoerenza interna: §2.5 contava quattro condizioni, §8 tre. Il conteggio corretto del piano originale (A, B, local-first, E come quattro condizioni distinte, R=3, 6 run per fault, 7 riceventi) è:

| Blocco | Calcolo | Chiamate |
| --- | --- | ---: |
| local-unseen | 8 × 6 × 7 × 4 × 3 | 4.032 |
| local-seen | 8 × 6 × 1 × 4 × 3 | 576 |
| Normal | 6 × 8 × 4 × 3 | 576 |
| **Nucleo** | | **5.184** |

Con capability pilot, ponte, produzione insight e dati di sviluppo si superavano le 6.000 chiamate. La stima "~4.000" della prima stesura sottostimava di circa un terzo. Il piano consolidato (§8) scende a ~2.450, tetto 3.000.

---

## 3 · Valutazione dello studio ponte — eliminato

**Decisione della revisione 2: il ponte è eliminato.** Questa sezione resta come motivazione della decisione.

### 3.1 Il disegno proposto

| Producer | Consumer | Stato |
| --- | --- | --- |
| Terra | Terra | già eseguito |
| Terra | Qwen-27B | già eseguito |
| Terra | Qwen-2.4T | da eseguire |
| Qwen-2.4T | Qwen-2.4T | da eseguire |

### 3.2 Che cosa poteva distinguere

Con producer Terra fisso e tre consumer, il ponte stimava ragionevolmente l'**effetto del consumer**: tre punti sulla stessa curva, stessi insight in ingresso. Con consumer Qwen-2.4T fisso e due producer, otteneva un confronto descrittivo tra producer su due punti, senza replicazione.

### 3.3 Che cosa non poteva distinguere

**L'interazione producer×consumer è non identificabile** con 4 celle su 2 producer × 3 consumer e 2 celle mancanti. E soprattutto: **il ponte usa i 12 run dello studio principale**, cioè dati già usati per progettare insight, soglie e prompt. Misura la portabilità su dati di sviluppo, non su dati vergini.

### 3.4 Perché è eliminato

Il ponte costa chiamate e giorni per produrre un risultato non pubblicabile su dati contaminati dalla progettazione. Il braccio producer-swap (§8.4) risponde alla stessa domanda — l'effetto del producer — ma su dati vergini e dentro il disegno dello studio finale, quindi entra nei risultati invece che nell'appendice. A parità di scopo, è strettamente migliore.

La verifica tecnica di compatibilità che il ponte forniva incidentalmente resta necessaria, ma è coperta dal capability pilot (§7.1), che è più economico e più diretto.

---

## 4 · Valutazione del confronto Q4–Q8 — eliminato

### 4.1 Il problema fondamentale

Passando da Q4 a Q8 si cambiano almeno sei variabili contemporaneamente (elencate in §2.4). Se Q8 ottiene il 90% e Q4 il 95% sugli stessi 4 fault, non si può sapere se il calo dipende dal contesto più lungo, dai più distrattori, o dai fault aggiuntivi. E viceversa.

### 4.2 Che cosa si poteva dire comunque

Il confronto resta utile come descrizione fattuale — "nella configurazione a 8 fault, l'accuratezza sui 4 fault condivisi è X rispetto a Y" — ma non dimostra quale fattore sia responsabile.

### 4.3 Decisione

**Q4 è eliminato come studio formale.** Q8 da solo è lo studio completo. I 4 fault di continuità permettono un confronto descrittivo con l'esplorativo Terra, dichiarato come tale.

Un vero esperimento sulla dimensione della federazione richiederebbe stessi agenti, stessi fault, stesso contesto, e sottoinsiemi crescenti di insight per ricevente (2, 6, 10, 14). Questo isolerebbe l'effetto della quantità di informazione. È future work, non parte del piano minimo.

---

## 5 · Tabella delle critiche — aggiornata

| ID critica | Descrizione breve | Effetto del piano consolidato | Nota |
| --- | --- | --- | --- |
| **G1** | Baseline numerica superiore (100% vs 86.1%) | **Mitiga** | La baseline numerica è nel finale sugli stessi dati e protocollo. Se con 8 fault e un modello diverso la distanza si riduce, l'argomento migliora; se il numerico vince ancora nettamente, il problema resta identico. |
| **G2** | Scala troppo piccola | **Mitiga moderatamente** | 8 agenti, 8 fault, ≥6 run per fault: scala doppia rispetto all'esplorativo, 48 cluster contro 12. Il confronto con i sei lavori esaminati — 3 client in P041, P030 e P031, 5 in P042 e negli esperimenti principali di P065 — serve a collocare il numero, non a legittimarlo: otto agenti restano pochi, e non rendono lo studio scalabile né Big Data. ⚠️ Il confronto va però fatto con precisione: **P065 pubblica anche una tabella di scalabilità fino a 500 client**, con dimensione del compendio limitata e p95 sotto i 500 ms. Non è una federazione reale — resta simulazione senza rete né nodi offline — ma citare P065 come «5 client» è smontabile in una riga, ed è proprio la riga che deve reggere contro CF2/C18. La critica è attenuata, non risolta, e il paper non deve presentare il confronto come se lo fosse. |
| **G5** | Unico producer | **Mitiga — identificabile** | *Corretto rispetto alla revisione 1, che dichiarava "Risolve".* Lo studio finale ha producer = consumer = Qwen, quindi la molteplicità di modelli resta tra i due studi. Il braccio producer-swap (§8.4) rende però l'effetto del producer **misurabile su dati vergini**, con libreria di insight completa dal producer alternativo. G5 passa da non verificata a stimata, non a risolta. Va inoltre notato che producer = consumer introduce un confondente nuovo (possibile vantaggio del modello nel leggere il proprio fraseggio): il producer-swap è anche il controllo di quel confondente. |
| **C06** | Degradazione local-seen in B | **Replica prospettica con protocollo congelato** | *Riclassificata.* Non è un endpoint esplorativo: `B_LOCAL_FIRST_V1` è già congelato e già eseguito sull'intera replica (§10.3 del walkthrough), con 23/24 local-seen contro 19/24 di B e local-unseen invariati a 68/72. Nel nuovo studio è la replica di un effetto misurato, con protocollo ed endpoint congiunto fissati prima dell'apertura dei run. Il congelamento è **interno**, non una registrazione pubblica: il termine «pre-registrata» non va usato. Resta un esito atteso, non acquisito. |
| **C07** | Reasoning cap e parsing | **Mitiga e controlla, se il pilot passa** | Il capability pilot stabilisce i parametri prima del congelamento ed è un gate bloccante, non una previsione. Ma un pilot superato riduce il rischio di parsing e di budget di ragionamento; non garantisce che nessun errore compaia nello studio completo, che gira su un volume due ordini di grandezza maggiore. Per questo il controllo non finisce con il pilot: proseguono il logging di conformità e il set canary (§8.7). |
| **G6** | Fault fuori catalogo / astensione | **Mitiga parzialmente** | *Aggiornata: la revisione 1 diceva "Non affronta".* Il test OOD (§8.6) su 2 fault fuori catalogo × 3 run × 8 agenti × 3 condizioni misura l'astensione in mondo aperto. Ma sono 6 eventi OOD: è una prima sonda, non una caratterizzazione. G6 resta parzialmente aperta e va dichiarata tale. |
| **G8** | La condizione A è un pavimento ovvio | **Mitiga indirettamente** | *Riga nuova.* Con `Unknown` disponibile in tutte le condizioni, A non è più uno zero per costruzione: diventa la misura di quanto il modello sa di non sapere in assenza di insight. Il pavimento resta basso, ma smette di essere un artefatto del disegno. |
| **G9** | Feature e soglie fisse | **Mitiga debolmente** | Score combinato congelato su R2 e soglia ricalibrata su 350 nuovi run Normal, con FAR verificato su altri 150. Ma restano le stesse famiglie di feature, nessuna nel dominio della frequenza e nessun adattamento al drift. Miglioramento marginale. |
| **G10 / CF3** | Assenza baseline FL reali | **Mitiga** | *Aggiornata: D8 è risolta.* Il piano include una baseline FedAvg minimale sulle stesse feature 697-D, con pavimento locale e soffitto centralizzato (§9). Mitiga, non risolve: una sola famiglia di metodi FL, congelata e non ottimizzata, non copre la letteratura FL. |
| **CF2 / C18** | Manca evidenza Big Data | **Mitiga debolmente** | 8 agenti è meglio di 4, ma per una conferenza chiamata BigData resta insufficiente. Nessun test su 50+ agenti, streaming, o edge. |
| **G3** | Federazione solo simulata | **Non affronta; comune nei sei lavori comparabili esaminati** | I nodi restano processi logici sulla stessa macchina. Va dichiarato che P041 (ICML 2025), P030, P031 (ICLR 2025) e P042 simulano allo stesso modo, con 3–5 client su una macchina, e nessuno di essi ha rete, latenze o nodi offline. Questo colloca il limite rispetto ai lavori esaminati; non stabilisce che sia una norma del campo, per la quale servirebbe una rassegna più ampia. Resta un limite del lavoro. |
| **G4** | Un solo round, senza iterazione | **Non affronta — scelta di scopo dichiarata** | Insight prodotti una volta. La revisione 3 converte l'omissione in scelta documentata, ma con un'avvertenza sul tipo di evidenza. I tre riscontri citati riguardano **fenomeni diversi fra loro**: round di comunicazione federati (P030, plateau al round 2 e FERA-Q che peggiora nei round finali), step di ottimizzazione locale (P031, degrado da 5 a 10), iterazioni di riflessione di un singolo agente (P001, 67,6 → 65,2 da 5 a 10). Non sono la stessa grandezza e non sono cumulabili in un'unica tendenza. Giustificano di **non aprire questo fronte adesso**, dato il costo e la finestra di §7; **non dimostrano che round aggiuntivi sarebbero inutili in FoT**, dove il compito, l'unità scambiata e la struttura delle classi sono diversi da tutti e tre. Va scritto così nel paper, e l'iterazione resta future work con una domanda aperta, non chiusa. |
| **G7** | Nessuna garanzia di privacy | **Non affronta** | Nessun attacco di ricostruzione, nessuna analisi formale. La barra si è però alzata: P065 fornisce (ε,0)-DP sui *soli campi numerici* del proprio artefatto, lasciando il testo a mascheramento euristico. Conseguenza pratica: la privacy non va presentata come contributo di questo lavoro in nessuna forma, nemmeno parziale, e l'argomento «non inviamo dati grezzi» va dichiarato come proprietà architetturale, non come garanzia. Vanno inoltre citati **DP-FPL** (Tran et al. 2025) e **FedDTPT**, entrambi 🟢 in §14.1 ed espressamente sulla privacy federata: oggi la barra è costruita sul solo P065. |
| **CF1 / CF5** | Non è FL in senso stretto; aggregazione assente | **Mitiga, resta aperta** | *Corretto nella revisione 3, che su questo punto era andata troppo in là.* L'aggregazione **non è inapplicabile**: contributi di client diversi possono essere aggregati anche quando ogni client possiede un fault diverso. Ciò che la configurazione class-disjoint indebolisce è **FedProto** in particolare (§9.1), non l'aggregazione in generale, e la questione dello scope FL resta intera. Quello che il piano fa è mitigare: la baseline FedAvg colloca il lavoro rispetto alla FL canonica, e un framing corretto evita di promettere ciò che il metodo non fa. Va inoltre notato, come contesto e non come giustificazione, che l'aggregazione testuale resta problematica anche dove è stata tentata: P031 (ICLR 2025) riporta che la concatenazione ottiene risultati migliori della sintesi, non scala oltre la finestra di contesto, e che il rimedio proposto rende +0,01–0,02, entro una deviazione standard. **La critica resta aperta e va dichiarata come limite.** |
| **CF4** | Privacy non affrontata | **Non affronta** | Come G7. |

### Sintesi aggiornata

L'elenco che segue riproduce la colonna «effetto» della tabella sopra, voce per voce e con le stesse parole. **Nessuna critica è dichiarata risolta.**

- **Mitiga e controlla**, se il pilot passa, con controllo che prosegue durante l'esecuzione: C07.
- **Mitiga e rende stimabile**: G5 (producer-swap su dati vergini).
- **Replica prospettica con protocollo congelato**: C06.
- **Mitiga**: G1, G10/CF3.
- **Mitiga moderatamente**: G2.
- **Mitiga parzialmente**: G6.
- **Mitiga indirettamente**: G8.
- **Mitiga debolmente**: G9, CF2/C18.
- **Mitiga, ma la critica resta aperta**: CF1/CF5.
- **Non affronta**: G3 e G4 (con la qualificazione della tabella), G7, CF4.

Nessuna critica è dichiarata risolta da un argomento: dove il piano non produce una misura, produce al più una mitigazione.

Le critiche non affrontate restano **limiti strutturali del metodo**, non difetti del piano, e vanno dichiarate come limiti. La revisione 3 cambia solo il modo in cui G3 e G4 vanno dichiarate, e con un'ambito preciso: la federazione simulata su 3–5 client ricorre in tutti e sei i lavori esaminati, il che colloca il limite senza stabilire una norma del campo; e per G4 i riscontri disponibili giustificano di non aprire il fronte dell'iterazione adesso, non di dichiararlo chiuso. Entrambe restano limiti, meglio argomentati. G7 e CF4 restano omissioni piene, e la barra di P065 impone di non presentare la privacy come contributo in nessuna forma.

La differenza rispetto alla revisione 1 è che **G5 e G6, le due sole critiche non strutturali che restavano aperte, sono ora mitigate e misurabili grazie a due bracci che costano insieme 332 chiamate** — circa il 14% del budget. Mitigate, non chiuse: G5 resta stimata su due producer e non su una popolazione di producer, G6 resta sondata su 6 eventi OOD.

---

## 6 · Attività che si possono iniziare subito

Queste attività non richiedono Qwen-2.4T e non rischiano di contaminare il test finale, a condizione di rispettare le regole indicate. Sono, oggi, il cammino critico reale: ogni ora spesa qui è tempo sottratto al collo di bottiglia di §7.

**6.1 — Definire i criteri di selezione degli 8 fault**
Scrivere i criteri strutturali e **congelare** il documento prima di esaminare qualunque risultato per-fault. I criteri ammessi sono solo due famiglie: (a) copertura dei meccanismi fisici documentati in Downs & Vogel 1993 — step, random variation, slow drift, sticking valve — e identità di variabile perturbata, leggibile dalla loro tabella dei fault; (b) stratificazione per difficoltà **documentata in letteratura**, con le fonti di §12. Non è ammesso alcun criterio basato su separabilità osservata nei propri dati. I 4 fault di continuità sono dichiarati come tali (§2.2).

**6.2 — Generare nuovi run fault di sviluppo**
Per ciascuno degli 8 fault generare cinque batch di sviluppo. Servono per produrre insight e
prototipi, non per valutare: **40 simulazioni** (8 × 5). I quattro fault di continuità non fanno
eccezione. La qualifica R1 della Fase 02 ha respinto l'uso dei venti fault storici come sostituti,
perché seed, `Ts_base` e configurazione effettivamente eseguita non sono ricostruibili; restano
consultabili soltanto come materiale storico già osservato. I cinque nuovi Normal prima previsti
qui sono invece eliminati: il disegno autorevole di calibrazione, riconciliato in §6.3, usa R2 come
`baseline_fit` e nuovi run disgiunti per soglia e verifica.

**6.3 — Costruire e calibrare lo score Normal secondo il registro autorevole**
Applicare `docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md`: N1–N5 sono autorizzati come
sola `baseline_fit` congelata dopo il superamento della guardia R2; non sono cinque run indipendenti
e non calibrano la soglia. Lo score A, costruito sulla baseline, viene poi applicato a **350 nuovi
run `cal_thr`**, una finestra per run, e verificato su **150 nuovi run `far_ver`** mai usati prima.
I dieci pilot restano esclusi da baseline, calibrazione e verifica. Il fallback già congelato, se
R2 decade, è 100 `baseline_fit_new`, 300 `cal_thr` e 150 `far_ver`.

**6.4 — Produrre dati strutturati e verbalizzazioni di sviluppo**
Trasformare i run di sviluppo nelle 697-D evidence e nel testo neutrale. Stabilisce come i nuovi fault appaiono al verbalizzatore.

**6.5 — Definire pseudolabel e permutazioni di E**
Generare 9 pseudolabel opache (8 fault + Normal) e la permutazione a zero-fixed-point per 8 classi di fault. Operazione combinatorica, indipendente dal modello. ⚠️ Le pseudolabel sono **nove**, non dieci: per D10 `Unknown` è l'astensione (`abstain=true`, `predicted_label=null`) e non entra nello spazio delle etichette.

**6.6 — Scrivere il piano statistico completo**
Popolazione primaria, endpoint (§8.5), contrasti, criteri di successo, δ, metodo bootstrap adattato a 9 classi più astensione, definizione di cluster, run minimi per fault, regola GO/NO-GO. Tutto congelato prima del primo run di test.

**6.7 — Preparare la baseline numerica**
Prototipi per classe dai dati di sviluppo (vettori medi 697-D), regola di classificazione congelata (distanza L1 minima). Indipendente dal modello linguistico.

**6.8 — Preparare l'harness API**
Aggiornare l'inferenza per 8 agenti, 14 insight, 9 pseudolabel con astensione disponibile (D10), logging esteso (§8.7) e set canary. Testare con Qwen-27B come surrogato.

**6.9 — Generare e congelare i run finali di test**
Almeno 6 run per fault × 8 fault, più Normal: **54 simulazioni** con 6 run, **72** con 8. Vanno aggiunti i **6 run OOD** di §8.6 (2 fault × 3 run), che sono simulazioni come le altre. Generare adesso e sigillare. Regola cruciale: **nessuna decisione di progettazione dopo aver osservato questi run.** Se serve ispezionarli per integrità tecnica, l'ispezione va loggata e non deve includere analisi delle distribuzioni dei sensori.

**6.10 — Congelare lo schema degli insight (§8.9)**
Campi, tipi, cardinalità, cap di lunghezza per elemento, validatore eseguibile. Non dipende dal modello, non consuma chiamate, e **deve precedere la produzione degli insight** di entrambi i producer: è ciò che rende il braccio producer-swap una manipolazione a fattore singolo invece di un confronto fra stili di scrittura.

**6.11 — Implementare la baseline FedAvg (§9)**
Non consuma chiamate API e non attende Qwen: è l'unico componente sperimentale interamente eseguibile oggi. Insieme a FedAvg vanno prodotti il pavimento locale e il soffitto centralizzato (§9.3). Specifica congelata prima di guardare il test.

**6.12 — Scrivere le sezioni del paper indipendenti dal modello**
Related work, descrizione del metodo, verbalizzatore, threats to validity. Sono circa il 60% del testo e sono **identiche** nella versione Q8 e nella versione Terra-only del piano B. Scriverle ora è l'unica assicurazione reale sull'opzione 3 di D9, e non sottrae tempo all'opzione 1.

⚠️ **Attenzione su 6.2–6.4 e 6.9:** i run di sviluppo vanno generati con seed documentati e **diversi** dai seed dei run di test. La separazione deve essere dimostrabile con hash e timestamp.

---

## 7 · Attività bloccate e cronologia critica

**7.1 — Capability pilot su Qwen-2.4T.** È il gatekeeper. Deve rispondere a: il modello risponde? il JSON è compatibile con il parser? il reasoning budget basta con 14 insight? la latenza è accettabile? e il test di stabilità di §8.7.

**7.2 — Produzione insight con Qwen-2.4T.** Gli 8×2 insight dai dati di sviluppo, più la libreria completa dal producer alternativo per il braccio swap (§8.4).

**7.3 — Congelamento del protocollo finale.** Solo dopo il pilot.

**7.4 — Esecuzione dello studio finale.** Tutte le inferenze A, B-LF, E-LF, più swap, OOD, ablation e canary.

**7.5 — Analisi e redazione.** Solo dopo il completamento.

### Cronologia critica — aggiornata a R=1

Con R=1 l'esecuzione scende da ~7 giorni a 2–3. Il vincolo non è più il volume di chiamate ma **la data della decisione sul modello**.

| Giorno | Attività |
| --- | --- |
| entro 14 set | API Qwen-2.4T disponibile |
| 15–16 set | capability pilot, incluso test di stabilità |
| **17 set** | **decisione GO/NO-GO sul modello — data limite** |
| 18 set | congelamento protocollo, produzione insight |
| 19–21 set | esecuzione studio finale (~2.450 chiamate) |
| 22–25 set | analisi dei risultati |
| 25–29 set | redazione |
| 30 set | deadline |

Il margine è di circa tre giorni. **Oltre il 17 settembre l'opzione 1 del piano B non è più praticabile**, indipendentemente dal fatto che l'API diventi disponibile: non perché manchino le chiamate, ma perché analisi e redazione non comprimibili occupano gli ultimi nove giorni.

---

## 8 · Piano consolidato

Questa è la versione definitiva dello studio finale. Sostituisce integralmente la "proposta minima" della revisione 1.

### 8.1 Disegno

- **Studio unico:** Q8 — 8 agenti, 8 fault, Qwen-2.4T come producer e consumer
- **Tre condizioni**, non quattro:
  - **A** — sola conoscenza locale
  - **B-LF** — conoscenza locale + insight corretti + politica local-first
  - **E-LF** — conoscenza locale + insight permutati + la stessa politica local-first
- **Run di test:** ≥6 per fault (48 cluster), preferibilmente 8 (64 cluster)
- **Run di sviluppo:** ≥5 per fault, per calibrazione soglie e produzione insight
- **Run Normal:** ≥6 per il test, 5 per lo sviluppo
- **Baseline numerica:** prototipi condivisi, stessi dati, stesso protocollo
- **`Unknown` disponibile in tutte le condizioni** (§8.6)
- **Schema degli insight congelato, tipizzato, con cap di lunghezza per elemento** (§8.9), identico per entrambi i producer
- **E-LF ottenuta modificando esclusivamente il campo pseudolabel**, con diff verificabile (§8.9)
- **Bootstrap:** cluster appaiato, un cluster = un run simulato
- **Congelamento:** tutto prima del primo run di test
- **Eliminati:** studio ponte, confronto Q4, condizione A+, condizione C centralizzata, ablation delle rappresentazioni (già disponibile dall'esplorativo)

### 8.2 Perché local-first entra nella definizione di B

`B_LOCAL_FIRST_V1` non è una variante da testare: è già congelata e già eseguita sull'intera replica dell'esplorativo. §10.3 del walkthrough riporta 23/24 sui local-seen contro 19/24 di B originale, a **parità esatta** di local-unseen (68/72 in entrambi) e Normal (24/24), con zero errori di parsing e soglie fissate prima dell'esecuzione.

Ne segue che local-first è la versione matura del metodo, non un braccio sperimentale. Trattarla come quarta condizione costerebbe ~430 chiamate per misurare una differenza già misurata.

**L'override esterno proposto nella revisione 1 è ritirato.** Sarebbe stato gratuito in chiamate — applicabile a posteriori agli output di B — ma non gratuito scientificamente: richiederebbe un rilevatore locale e una soglia affidabile, i cui punteggi non esistono nell'output attuale, e introdurrebbe un metodo ibrido nuovo per risparmiare budget. Local-first resta un blocco di politica decisionale nel prompt.

### 8.3 L'ablation di B-senza-LF non è opzionale

Se local-first entra nella definizione del metodo, un reviewer chiederà se il numero di testa dipende da un accorgimento di prompt engineering. **Quell'ablation è l'unica risposta possibile**, quindi va pianificata come parte del disegno, non come residuo.

Vincolo di disegno: il sottoinsieme va scelto **strutturalmente e dichiarato prima**. In §10.3 i 5 miglioramenti e l'unica regressione cadono tutti nella confusione F8/F13, cioè in una coppia specifica. Con 8 fault le coppie confondibili saranno altre e vanno identificate su base meccanica — fault che condividono variabile perturbata o meccanismo secondo Downs & Vogel — non dopo aver visto le confusioni del test.

| Componente dell'ablation | Calcolo | Chiamate |
| --- | --- | ---: |
| local-seen su tutti gli 8 fault | 8 × 6 × 1 | 48 |
| local-unseen sulle coppie confondibili dichiarate | 4 × 3 × 7 | 84 |
| **Totale** | | **132** |

**Nota sulla simmetria** *(revisione 4)*. L'ablation esiste per B e non per E. Non è un buco del contrasto causale: local-first è tenuto **costante** fra B-LF ed E-LF, quindi B−E isola l'informazione e non la politica, ed è questo che va scritto nel paper. Non va invece affermato che la politica renda il contrasto *conservativo*: non è dimostrato, e local-first può spostare errori e astensioni in entrambe le direzioni. Se si volesse chiudere anche la simmetria, E-senza-LF sullo stesso sottoinsieme dichiarato costerebbe 4 × 3 × 7 = 84 chiamate, +3,4% del budget. Non è necessaria al claim.

### 8.4 Braccio producer-swap

Affronta G5 su dati vergini. La manipolazione è a fattore singolo: **libreria di insight interamente dal producer alternativo** contro libreria interamente da Qwen-2.4T, stesso consumer, stessi run di test, stessa condizione B-LF.

Generare insight solo per i fault confrontati produrrebbe un prompt a provenienza mista (4 swapped + 10 originali) e il confronto isolerebbe "libreria mista vs omogenea" invece dell'effetto del producer. Quindi: **il producer alternativo genera tutti gli 8×2 insight**, e la misura si limita a 4 fault per contenere le chiamate.

**Vincolo aggiunto nella revisione 3 — parità strutturale.** Entrambi i producer devono emettere lo **stesso schema, lo stesso numero di insight e lo stesso cap di lunghezza per elemento** (§8.9), e i token effettivi per insight vanno misurati e riportati per producer. Senza questo vincolo, "effetto del producer" ed "effetto della verbosità" restano confusi. Il confondente non è ipotetico: in P031 (ICLR 2025) la condizione con i prompt concatenati — più lunga — ottiene risultati migliori della condizione con i prompt sintetizzati su tutti e tre i task (0,90/0,69/0,94 contro 0,88/0,55/0,92). P031 **non isola la lunghezza** come causa, e nemmeno noi possiamo farlo per loro: la lettura corretta è che in quel confronto lunghezza e contenuto variano insieme e non sono separati. È esattamente la ragione per cui qui vanno tenuti fissi per costruzione — non perché sia dimostrato che la lunghezza causi il risultato, ma perché nessuno ha dimostrato che non lo faccia.

**Posizionamento.** P065 è l'unico dei lavori esaminati che dimostri il trasferimento di un artefatto testuale strutturato fra famiglie di modelli diverse, ma il suo esperimento è **consumer-swap**: un compendio costruito con LLaMA-3.1-8B viene *letto* da quattro modelli (GSM8k 0,92 / 0,90 / 0,91 / 0,92). Il compendio è prodotto da un solo modello in ogni esperimento, e la generalità rispetto al **produttore** non è mai testata. Il braccio di §8.4 occupa esattamente quel vuoto, ed è la ragione per cui va mantenuto anche nel piano B (§10, D9).

| Componente | Calcolo | Chiamate |
| --- | --- | ---: |
| Generazione libreria completa dal producer alternativo | 8 × 2 + margine | ~20 |
| Misura su 4 fault, condizione B-LF, R=1 | 4 × 6 × 7 | 168 |
| **Totale** | | **188** |

Nel piano B (D9 opzione 2), il producer alternativo è Terra: il braccio resta intatto e G5 resta coperta.

### 8.5 Endpoint

**Primario.** Accuratezza sui local-unseen in B-LF, contrastata con A e con E-LF. Il contrasto B−E è quello che porta il claim causale: distingue "il testo funziona perché contiene informazione corretta" da "il testo funziona perché c'è più contesto nel prompt". **E-LF non va ridotta a campione.**

**C06 e claim principale: tre ipotesi, una gerarchia.** Il riferimento naturale per i local-seen è A, che è pura conoscenza locale. La formulazione corretta non usa un margine δ′ scelto guardando il risultato precedente — sarebbe ancora una scelta guidata dall'esito — ma tre ipotesi di forma standard:

| # | Ipotesi | Forma | Che cosa dimostra |
| --- | --- | --- | --- |
| H1 | B-LF > E-LF sui local-unseen | superiorità | il trasferimento funziona perché l'informazione è corretta, non perché il contesto è più lungo |
| H2 | B-LF > A sui local-unseen | superiorità | il trasferimento aggiunge qualcosa alla sola conoscenza locale |
| H3 | B-LF non inferiore ad A sui local-seen | non inferiorità, margine *m* | il metodo non distrugge ciò che l'agente già sapeva |

Il metodo conserva ciò che l'agente conosce (H3) e trasferisce ciò che non conosce (H1, H2). Un criterio di sola preservazione sarebbe soddisfatto meccanicamente dalla politica local-first e non dimostrerebbe nulla; le due superiorità sono ciò che rende H3 informativa.

**Il margine non sparisce, cambia giustificazione.** Un test di non inferiorità richiede comunque un margine *m* pre-specificato: la formulazione elimina il δ′ arbitrario ma non la decisione. Le due giustificazioni ammissibili sono entrambe esterne ai risultati:

- **operativa** — quale degradazione sui fault già noti renderebbe il metodo inaccettabile in esercizio. Con 48 cluster local-seen, "più di un caso su otto perso" è una soglia esprimibile e discutibile con un ingegnere di processo;
- **di risoluzione del disegno** — la differenza minima che 48 cluster permettono di distinguere dal rumore, come controllo di sanità: un margine più stretto della risoluzione del disegno rende il test non informativo per costruzione.

Si sceglie la giustificazione operativa e si usa la seconda come verifica. Il dato di §10.3 (perdita zero su 72 casi) **non** va usato per fissare *m*: può essere citato come attesa, non come calibrazione.

**Gerarchia di test, per non gonfiare l'errore di primo tipo.** Tre ipotesi su una stessa popolazione richiedono un ordine di gatekeeping, congelato prima: H1, poi H2, poi H3, ciascuna a 0,05, procedendo solo se la precedente passa. Senza gerarchia, tre test indipendenti portano l'errore complessivo oltre il 14%.

**Con `Unknown` disponibile, l'endpoint va definito su tre numeri separati**, con indicazione di quale è primario:

1. accuratezza su tutti i tentativi, con l'astensione che conta come non-corretta *(primario)*
2. tasso di astensione
3. accuratezza sui soli casi non astenuti

Lasciata implicita, questa scelta diventa una leva post-hoc.

**Due dei tre numeri esistono già** *(revisione 5)*. `phase_b/final_evaluation/primary_metrics.csv` e `secondary_metrics.csv` portano le colonne `accuracy` — con le astensioni dentro il denominatore, cioè il numero 1 — e `abstention_rate`, cioè il numero 2; `phase_b/evaluation/metrics.py` le calcola. **Manca solo il numero 3**, ed è assente da entrambi gli artefatti: la sua aggiunta è nuova per assenza verificata, non per impressione. S11b costa quindi una metrica, non tre.

**Reporting stratificato obbligatorio.** Accuratezza riportata per i 4 fault di continuità, per i 4 fault nuovi, e aggregata. Costa zero e permette al lettore di vedere se il numero principale dipende dal sottoinsieme di continuità.

### 8.6 Test fuori catalogo e astensione

Affronta G6. Due fault non inclusi nel catalogo Q8, 3 run ciascuno, presentati a tutti gli 8 agenti, **in tutte e tre le condizioni**.

Eseguirlo solo in B non permetterebbe di capire se gli insight migliorano o peggiorano l'astensione: serve A come comparatore senza insight, ed E-LF per distinguere l'effetto dell'informazione da quello del contesto.

| Calcolo | Chiamate |
| --- | ---: |
| 2 fault × 3 run × 8 agenti × 3 condizioni | 144 |

**Condizione di validità:** il test misura qualcosa solo se il prompt offre effettivamente l'astensione. L'astensione va quindi disponibile in **tutte** le condizioni dall'inizio, non aggiunta per il solo test OOD — altrimenti il tasso di falsi positivi non ha comparatore in-catalogo. Costo aggiuntivo in chiamate: zero.

⚠️ **Correzione della revisione 5: il trade-off dichiarato qui non si applica.** Questa sezione affermava che l'inclusione di `Unknown` «cambia i numeri principali e indebolisce il confronto descrittivo con l'esplorativo, che non aveva `Unknown`». L'affermazione è falsa sugli artefatti congelati. `phase_b/final_evaluation/primary_metrics.csv` porta le colonne `abstentions` e `abstention_rate`:

```
condition,n,correct,accuracy,abstentions,abstention_rate
A,36,0,0.0,14,0.3888888888888889
B,36,31,0.8611111111111112,0,0.0
E,36,3,0.08333333333333333,0,0.0
```

Se ne leggono tre fatti. L'astensione era **offerta e usata** — 14 casi su 36 in A. Era **misurata come tasso separato**, cioè il secondo dei tre numeri di §8.5. Ed era **contata come non-corretta**, perché l'accuratezza di A è 0,0 su `n=36` con le 14 astensioni dentro il denominatore: esattamente la definizione marcata come primaria in §8.5. `phase_b/final_evaluation/secondary_metrics.csv` lo conferma sugli strati (A complessivo 24/60, 14 astensioni, tasso 0,2333); per la replica il numero corrispondente — 30 astensioni in A — è in §8.3 del walkthrough, che lo legge dagli oggetti dei tag `exp3-v2-*` e non dal working tree.

Ne segue che, nella forma congelata in D10, il confronto descrittivo con l'esplorativo **non è indebolito dallo spazio delle etichette**. Resta indebolito da tutto il resto — otto fault contro quattro, un modello diverso, un contesto più lungo — e questo va comunque dichiarato.

**Che cosa resta da osservare, e non da ereditare.** Che l'astensione fosse praticabile con 4 insight e 5 classi non dimostra che lo sia con **14 insight e 9 classi**. La condizione di validità di questa sezione va quindi verificata nel capability pilot, misurando il tasso di astensione in-catalogo delle tre condizioni prima di aprire i run di test. Un tasso che collassa a zero renderebbe il test OOD non informativo, e andrebbe saputo prima e non dopo.

**Scelta dei due fault OOD.** Devono essere meccanicamente distinti da **tutti** gli 8 in catalogo. F2 e F5, proposti nella revisione 1, non sono adatti se in catalogo c'è F1: F1 è uno step sul rapporto A/C in alimentazione, F2 uno step sulla composizione di B, e un agente che etichetta F2 come F1 non sta sbagliando in modo interessante. Il "falso positivo" sarebbe comportamento ragionevole e il test non discriminerebbe.

**Secondo vincolo, aggiunto nella revisione 4: la rilevabilità.** La distinzione meccanica non basta. §12.1 documenta che F3, F9 e F15 sono compensati dagli anelli di controllo e producono evidence quasi vuota. Un fault OOD scelto in quel gruppo farebbe astenere l'agente per **assenza di segnale**, non per riconoscimento di novità, e il test misurerebbe il verbalizzatore invece dell'agente. I due fault vanno quindi scelti fuori dal gruppo a fallimento concorde, oppure accompagnati da un criterio esterno di rilevabilità dichiarato prima.

⚠️ **La scelta dipende da quali 8 fault entrano in catalogo.** «Meccanicamente distinto da *tutti* gli 8» non è valutabile finché gli 8 non sono fissati: S13 dipende da S1, e quindi da §6.1 e da D1. È bloccante ma **non lavorabile oggi**, e va contato così nella cronologia di §7 (§0.1, §11).

**Limite da dichiarare.** 2 fault × 3 run sono 6 eventi OOD: una dimostrazione di esistenza, non una caratterizzazione del comportamento open-set. Nel paper va come *prima sonda*, con G6 dichiarata parzialmente aperta.

### 8.7 R=1, gate di stabilità e rilevamento del cambio di modello

**R=1 è il lever principale sul costo e sulla fattibilità**: porta il nucleo da 5.184 a 1.296 chiamate e comprime l'esecuzione da ~7 giorni a 2–3.

**Va però presentato per ciò che è: un compromesso operativo, non un'equivalenza statistica a R=3.** Due precisazioni che il paper deve fare esplicitamente, perché un reviewer attento le farebbe comunque:

- un pilot senza divergenze osservate **non dimostra il determinismo** del modello; stabilisce solo che, nelle condizioni e nella finestra osservate, non è emersa variabilità (§ la regola del tre, sotto);
- gli intervalli bootstrap sui cluster-run **misurano la variabilità fra run simulati, non la variabilità delle risposte del modello alla stessa identica richiesta**. Con R=1 quest'ultima componente non è stimata, e va dichiarata come non stimata anziché assunta nulla.

Ne segue che **l'audit a R=3 e il set canary non sono rifiniture ma i due strumenti che rendono R=1 difendibile**: senza di essi, R=1 sarebbe una scelta di costo travestita da scelta metodologica.

**Il pilot è un gate tecnico, non una stima.** Un pilot da 40 prompt × 3 ripetizioni con zero divergenze osservate non dimostra che l'instabilità sia sotto l'1%.

⚠️ **Correzione della revisione 4: l'unità statistica è il prompt, non la chiamata.** L'evento «divergenza» è definito *fra le ripetizioni di uno stesso prompt*, quindi le osservazioni indipendenti sono **40**, non 120. Per la regola del tre il limite superiore al 95% con zero eventi su 40 osservazioni è 3/40 ≈ **7,5%**, non 3/120 ≈ 2,5%. Vanno rimosse entrambe le soglie: l'1% era irraggiungibile in linea di principio, il 2,5% contava le ripetizioni come prove indipendenti. Unità statistica e definizione dell'evento vanno scritte nel protocollo **prima** di eseguire il pilot. La formulazione corretta è:

- **nessuna divergenza osservata nel pilot → R=1 con audit continuo**
- divergenze osservate → R=3 sull'intero studio, e il non-determinismo entra nel modello di varianza e nel reporting

Il caveat tecnico è sostanziale: Qwen-27B è un modello denso, un 2.4T-A95B è MoE, e nei MoE il routing può dipendere dalla composizione del batch. A T=0 la riproducibilità bit-a-bit **non è garantita** e il determinismo di Qwen-27B non si trasferisce per analogia.

**Audit continuo.** Sottoinsieme del 10% campionato su tutti i fault, agenti e condizioni, congelato prima, eseguito a R=3 e distribuito nel tempo. Per ogni chiamata dello studio va registrato:

| Campo | Scopo |
| --- | --- |
| stabilità dell'etichetta tra ripetizioni | rilevare non-determinismo |
| esito del parsing | rilevare degradazione del formato |
| lunghezza della risposta e troncamenti | rilevare esaurimento del reasoning budget |
| **ID del modello come restituito dall'API** (non come richiesto) | rilevare sostituzione dichiarata |
| **request ID** | tracciabilità |
| **system fingerprint o qualunque versione esposta** | rilevare cambio dichiarato |
| hash della risposta grezza, timestamp, latenza | ricostruzione forense |
| **validità dello schema al primo tentativo** (§8.9) | conformità del producer |
| **numero di retry per raggiungere un insight valido** | costo reale della struttura |
| **troncamenti rispetto al cap per elemento** | saturazione del budget |
| **token per insight e per prompt, per producer e condizione** | separare effetto informazione da effetto lunghezza |

**Registrare le capacità dell'API, non solo i suoi output** *(revisione 5)*. Il capability pilot deve annotare quali controlli di determinismo l'API del modello scelto espone effettivamente — temperatura e seed in primo luogo — e non assumerli. Il precedente è nel repository: `phase_b/config/execution_config.json` registra `temperature_supported: false` e `seed_supported: false` per il modello del primo studio, che quindi è stato eseguito senza alcuna leva sul determinismo.

Due regole interpretative da congelare con il protocollo, perché senza di esse la registrazione diventa una leva post-hoc:

- **l'assenza dei controlli non è una divergenza osservata**, e da sola non attiva R=3: il gate di D7 resta definito sull'evento «divergenza fra le ripetizioni di uno stesso prompt», non sulle capacità dichiarate dal provider;
- **se si vuole una politica più conservativa** — R=3 quando l'API non espone né temperatura né seed — è una **nuova decisione**, da pre-specificare prima del pilot e non dopo averne visto l'esito. È aperta (§0.1, decisione 11).

Il valore della registrazione è un altro: senza controlli sul determinismo, la riproducibilità operativa dello studio è più debole, e questo va scritto nei limiti invece di essere scoperto da un reviewer.

**Hash, timestamp e latenza non dimostrano un cambio di modello**: sono forensi, permettono di ricostruire un cambio dopo averlo sospettato. ID, request ID e fingerprint sono il livello dichiarativo, e dipendono dall'onestà e dall'aggiornamento del provider. Lo strumento **rilevativo** è un **set canary**: 10 prompt fissi con output atteso congelato, rieseguiti ogni giorno dell'esecuzione. Una variazione nel canary è evidenza positiva di cambio di comportamento indipendentemente da ciò che l'API dichiara. Costo: ~10 chiamate al giorno.

### 8.8 Budget

Il budget dipende da D2 — 6 o 8 run per fault — che non è ancora congelata. Entrambe le colonne sono calcolate, così la decisione è prezzata invece che rimandata.

| Blocco | 6 run (48 cluster) | 8 run (64 cluster) |
| --- | ---: | ---: |
| Nucleo local-unseen, 3 condizioni, R=1 | 1.008 | 1.344 |
| Nucleo local-seen | 144 | 192 |
| Nucleo Normal | 144 | 192 |
| **Nucleo** | **1.296** | **1.728** |
| Audit R=3 sul 10% *(nucleo soltanto; **non copre E5**)* | ~260 | ~346 |
| Braccio producer-swap (§8.4) | 188 | 244 |
| Ablation B-senza-LF (§8.3) | 132 | 148 |
| Experiment 5 — ablazione descrittori (§8.12) | 144\* | 192\* |
| Test fuori catalogo (§8.6) | 144 | 144 |
| Produzione insight | ~30 | ~30 |
| Capability pilot incluso test di stabilità | ~200 | ~200 |
| Verifiche tecniche e harness | ~100 | ~100 |
| Set canary | ~100 | ~100 |
| **Totale stimato** | **~2.594** | **~3.232** |
| Retry e riparsing (+10%) | ~259 | ~323 |
| **Sottototale con retry** | **~2.853** | **~3.555** |
| **Tetto da richiedere** | **3.000** | **3.700** |

\* **La voce E5 è parametrica, non definitiva.** Vale **2nR · Σ_F (m_F + c_F)** per i bracci
corrotti, con n run per fault, R ripetizioni, m_F fault bersaglio e c_F = 1 controllo per famiglia.
**Per E5 si adotta R = 1**, coerentemente con lo statuto descrittivo e con il contenimento del costo.

I 144/192 in tabella sono uno **scenario prudenziale di budget**, non il sottoinsieme concordato: tre
fault per ciascuna famiglia non coincide con quanto stabilito per `slope_sigma_h`, che ne ha due.
Con tre fault per ciascuna delle altre tre famiglie e due per slope il costo è **132/176** — anch'esso uno **scenario**, non il costo definitivo finché la mappa famiglia–meccanismo resta aperta. I 144/192 restano
come **accantonamento prudenziale e non autorizzano un controllo aggiuntivo**. La cifra resta
indicativa finché la mappa famiglia–meccanismo (E5-C3) è aperta.

**FULL è una voce aggiuntiva solo se non risulta riusabile da B-LF** (§8.12): in quel caso vale
**R n |∪_F S_F|**, cioè con R = 1 al massimo **48 a 6 run e 64 a 8**. Mantenendo l'accantonamento
prudenziale e senza riuso di FULL, i totali comprensivi del 10% diventano circa **2.906 / 3.626**,
entro i tetti scelti.

**L'audit R=3 del 10% è calcolato sul nucleo e non copre E5**, che gira a R = 1: **la stabilità dei
contrasti di E5 rispetto alle ripetizioni dell'inferenza non è verificata**, ed è un limite da
dichiarare nel paper, non una svista.

I tetti di **3.000 a 6 run e 3.700 a 8** sono tetti di **pianificazione**: le cifre effettive restano
subordinate alla mappa finale e al riuso di FULL.

Passare a 8 run costa **+590 chiamate, cioè +24%**, e porta i cluster da 48 a 64. La baseline FL (§9.1) non entra in questa tabella: non consuma chiamate API.

**Il budget in chiamate non è l'unico budget** *(revisione 5)*. Il piano prescrive la generazione dei run in §6.2 e §6.9 ma non ne ha mai totalizzato il costo, e questo ha fatto sembrare la generazione dati un preliminare invece di una voce del cammino critico:

| Blocco di simulazione | 6 run | 8 run |
| --- | ---: | ---: |
| Qualifica generatore e R2 — completata in Fase 02 | 150 | 150 |
| Sviluppo fault — 8 fault × 5 (§6.2) | 40 | 40 |
| Calibrazione Normal — `cal_thr` (§6.3) | 350 | 350 |
| Verifica Normal — `far_ver` (§6.3) | 150 | 150 |
| Test — 8 fault × *n* + *n* Normal (§6.9) | 54 | 72 |
| Fuori catalogo — 2 fault × 3 run (§8.6) | 6 | 6 |
| **Totale del protocollo di generazione** | **750** | **768** |
| **Residuo dopo la Fase 02** | **600** | **618** |

Nessuna di queste consuma chiamate API: consumano **tempo di simulazione** e disponibilità
dell'ambiente MATLAB/Simulink. Le 150 simulazioni di qualifica sono una voce di protocollo già
chiusa, non dati riusabili per calibrazione o test. Il conteggio distingue il budget scientifico
dalle ripetizioni tecniche eseguite durante l'implementazione e rendicontate nel report di Fase 02.
R1 non riduce le 40 simulazioni fault; R2 elimina soltanto i cinque Normal del vecchio §6.2 e non
riduce i 500 nuovi run conformal.

Ne segue una correzione alla lettura del collo di bottiglia data in §7: la data della decisione sul
modello resta il vincolo per l'**esecuzione**, ma la generazione dei run è un secondo percorso,
indipendente da Qwen e attivabile subito. Va pianificato in parallelo alla settimana del pilot.

**Ordine di generazione, identico a §8.12** *(sostituisce la prescrizione precedente, per cui la
generazione doveva chiudersi prima del congelamento).* Le simulazioni possono essere anticipate
rispetto al congelamento del protocollo, ma i run restano **sigillati**: nessuna ispezione di segnali,
feature o risultati del test per decisioni progettuali; ammesse le sole verifiche tecniche
predefinite che non orientano tali decisioni. Mappe donatore–ricevente e assegnazioni degli agenti si
costruiscono e si congelano **prima** del freeze, sui soli identificativi; l'applicazione
all'evidenza e la generazione di omissioni e prompt vengono **dopo**.

Per confronto, il piano originale costava 5.184 chiamate di **solo nucleo** e oltre 6.000 con tutto incluso. Un budget quotato come stima puntuale si esaurisce sempre: va chiesto come tetto.

### 8.9 Schema degli insight, parità fra producer, conformità

Questa sottosezione è nuova nella revisione 3 e nasce da una lacuna comune a tutti i lavori esaminati, non da un'idea presa in prestito da essi.

**Il problema.** Il prior art federato rivendica artefatti testuali strutturati ma non ne pubblica lo schema e non ne misura la conformità:

| Lavoro | Struttura dichiarata | Schema pubblicato | Cap di lunghezza | Metriche di conformità |
| --- | --- | --- | --- | --- |
| P065 (SYNAPSE) | 5 componenti tipizzate, validazione invocata come primitiva | **no** — nessun campo, tipo o cardinalità nel testo | dichiarato ma mai istanziato | **nessuna** |
| P042 (FICAL) | 4 campi del compendium | solo in figura, non nel corpo | nessuno | **nessuna** |
| P001 (ACE) | bullet con ID e contatori helpful/harmful | parziale, sezioni a stringa libera | **nessuno per elemento**; solo soglia sul contesto totale | **nessuna** |
| P041 (Fed-ICL) | coppie (query, risposta) | sì, semplice | **sì: 256 token** | costo *stimato* al massimo, mai misurato |
| P030 (FERA) | tracce di ragionamento | no | variabili di template mai istanziate | **nessuna** |
| P031 (FedTextGrad) | prompt in testo libero | nessuna struttura | nessuno lato client | token solo per la concatenazione |

**La decisione.** Congelare uno schema con campi nominati, tipi, cardinalità fissa e **cap di lunghezza per singolo insight**, più un validatore eseguibile, e riportare le metriche di conformità di §8.7.

**Beneficio, in tre punti concreti e non generici:**

1. **Rende il producer-swap interpretabile.** È la condizione perché §8.4 misuri il producer e non lo stile.
2. **Rende E una manipolazione a campo singolo.** Con uno schema tipizzato, E-LF si ottiene permutando **soltanto il valore del campo pseudolabel**, lasciando immutato ogni altro byte. Il diff fra la libreria B e la libreria E diventa un artefatto verificabile da allegare al paper: si vede che il contenuto descrittivo è identico e che cambia solo l'etichetta. Con insight in testo libero questa verifica non esiste e il controllo E resta un'affermazione degli autori.
3. **Rende misurabile ciò che i sei lavori esaminati non misurano.** Validità, retry, troncamenti e token non sono riportati da nessuno dei sei, e qui costano zero chiamate aggiuntive perché sono logging.

**Costo.** **Zero chiamate API aggiuntive.** La progettazione dello schema e il validatore sono lavoro di ingegneria indipendente dal modello (§6.10). Le ripetizioni per conformità rientrano nelle righe già presenti in §8.8: "Produzione insight" (~30) per il producer principale, la voce di generazione della libreria dentro il braccio swap (~20, §8.4), e il capability pilot (~200), che nella revisione 3 deve includere una sonda di conformità allo schema su **entrambi** i producer. **Il budget di §8.8 resta invariato: ~2.450 con 6 run, ~3.040 con 8 run.**

**Critica che mitiga.** Due, entrambe precise: *«l'effetto che chiamate producer è un effetto di formattazione»* e *«la vostra condizione E potrebbe differire da B per più della sola etichetta»*. La seconda è la più pericolosa, perché colpisce il contrasto che porta l'intero claim causale.

**Che cosa NON è, per evitare un'accusa di novità gonfiata.** Insight strutturati con campi e identificatori sono prior art consolidato: P001 (ICLR 2026) ha bullet con ID stabili e contatori di utilità, P065 ha un tipo-prodotto a cinque componenti, P042 ha quattro campi. **La struttura non è il contributo.** Il contributo è che lo schema sia *congelato prima*, *vincolato per elemento*, *identico fra producer* e *misurato*. Formulato diversamente, sarebbe una rivendicazione facilmente smontabile.

**Che cosa non è, seconda precisazione** *(revisione 4)*. Non è nemmeno la prima misura di conformità pubblicata su questo benchmark. **EviFDD-Agent** (2026, *Computers & Chemical Engineering*) riporta sul TEP una tabella con Evidence Field Traceability e Untraceable Report Rate, intervalli di Wilson su n = 210, sette configurazioni e una tassonomia degli errori. Misura però una grandezza **diversa e complementare**: la tracciabilità dei campi del *reporter* verso un evidence record già prodotto da tool deterministici, non la validità dello schema lato *producer* — che è ciò che §8.9 misura, insieme a retry, troncamenti e token. La differenza va nominata; l'omissione del lavoro no (§8.10 punto 7).

**Due riscontri di EviFDD che entrano nel disegno.** Primo: nel prompt passivo a singolo passaggio l'URR è 77,1%, e i fallimenti sono concentrati negli **identificatori di variabile** parafrasati — `XMEAS(n)` che diventa «reactor temperature» — mentre i campi numerici hanno zero errori. Gli insight FoT portano identificatori XMEAS: è la modalità di fallimento attesa, e il validatore di D12 va costruito su quella. Secondo: le condizioni in cui i campi critici sono serializzati da una struttura deterministica invece che trascritti dal modello raggiungono **URR = 0**, il che rende valutabile in D12 la separazione fra campi serializzati dal verbalizzatore e parte narrativa lasciata al producer. Va infine notato che lo stesso protocollo su due modelli della stessa famiglia dà URR 1,4% contro 19,5% con 11,8× di wall time, con il modello **più grande** meno conforme e più lento: la sonda di conformità del capability pilot va eseguita su **entrambi** i modelli candidati, non solo sul preferito (§7.1, T9).

**Un argomento a favore del cap, contro l'obiezione prevedibile.** P001 sostiene apertamente che i contesti debbano essere «comprehensive, not concise» e che i cap facciano perdere informazione. Ma la sua stessa Tab. 21 riporta, per soglie di pruning a 10K, 50K e 100K token, i valori 78,6 / 78,4 / 78,3: in quell'esperimento **un budget dieci volte più stretto non produce una perdita evidente**. Nulla in quei numeri dimostra che 10K sia *migliore* — lo scarto di 0,3 punti non è interpretabile e P001 non riporta varianza in alcun esperimento; l'unica lettura sostenibile è che la perdita attesa dal restringimento non si manifesta. Va inoltre notato che la tesi pro-verbosità di P001 non è sottoposta a un controllo di lunghezza a parità di contenuto. Il cap per elemento non è quindi dimostrato superiore: è una scelta che la letteratura disponibile non penalizza, ed è su questa base — non su una superiorità dimostrata — che va difesa. Va aggiunto che P001 arriva alla stessa lettura in proprio: «performance is stable from 10K to 100K tokens, indicating ACE does not require finely tuned length thresholds». L'argomento non è quindi una lettura di parte di Tab. 21, è la conclusione che gli autori traggono dal proprio esperimento.

### 8.10 Che cosa va nel paper

1. **Esplorativo Terra come motivazione:** uno studio con 4 agenti e 4 fault ha mostrato che il meccanismo funziona (B = 86,1%, replica 94,4%); lo studio finale verifica la generalizzazione a scala doppia con un modello indipendente.
2. **Studio finale Q8:** tutti i risultati, baseline numerica inclusa, con reporting stratificato (§8.5).
3. **Producer-swap:** l'effetto del producer su dati vergini, con parità strutturale (§8.4). Il prior art più vicino, P065, fa solo consumer-swap.
4. **Test fuori catalogo:** prima sonda sul comportamento open-set.
5. **Ablation local-first:** difesa del metodo principale.
6. **Confronto descrittivo con l'esplorativo** sui 4 fault di continuità, dichiarato come descrittivo e non causale.
7. **Conformità allo schema:** validità, retry, troncamenti e token per producer (§8.9). È una tabella piccola. ⚠️ **Non va presentata come «l'unica del suo genere fra i lavori comparabili»**: EviFDD-Agent pubblica sul TEP una tabella di conformità con intervalli di Wilson. La formulazione sostenibile è che fra i sei lavori esaminati — cinque federati e ACE, che è mono-agente — nessuno riporta congiuntamente validità dello schema **lato producer**, retry, troncamenti e token, mentre EviFDD riporta una grandezza diversa e complementare, la conformità evidence-traceable del reporter (§8.9).
8. **Related work obbligatoria:** P042, P041, P031, P030, P065, P001, FaultExplainer ed **EviFDD-Agent** (§12.6). L'omissione di uno qualsiasi è oggi un rischio concreto in revisione. EviFDD entra per due ragioni indipendenti: è LLM applicato alla diagnosi sul TEP, e delimita direttamente il punto 7.

### 8.11 Domande scientifiche, in ordine di priorità

Riformulate nella revisione 3 per non ricadere su terreno che i sei lavori esaminati occupano già (§12.7). Nessuna delle tre è "federare testo" o "trasferire conoscenza fra LLM": entrambe sono insostenibili contro quel corpus.

1. **La conoscenza testuale di un pari permette di diagnosticare una classe che l'agente non ha mai osservato localmente?** È l'endpoint local-unseen. Nessuno dei sei lavori esaminati riporta un numero su questa domanda: P041 e P030 usano spazi di etichette condivisi con eterogeneità solo distribuzionale; P042 ha toolset disgiunti ma non separa mai i tool posseduti da quelli noti solo per via altrui; P031 ha task disgiunti ma riporta solo la media fra task, senza scomposizione per client.
2. **Il guadagno dipende dalla correttezza dell'informazione o dalla sua sola presenza?** È il contrasto B−E. È il controllo che manca a tutti e sei (§12.7) e la ragione per cui E-LF non è riducibile a campione.
3. **La conoscenza ricevuta danneggia ciò che l'agente già sapeva, e a che prezzo la si può proteggere?** È C06 con local-first e l'endpoint congiunto di §8.5. Nessuno dei sei misura la degradazione sulle classi già note localmente.

Domande di supporto, non primarie: il testo compete con un trasferimento numerico semplice (baseline numerica e FedAvg, §9); il risultato dipende da chi produce gli insight (producer-swap, §8.4); payload, latenza, conformità e scomposizione per agente.

### 8.12 Ablazione testuale dei descrittori di Fase A (approvata 2026-09-11, **non congelata**)

**Documento autorevole del disegno: questa sezione.** Il piano BIGDATA2026 ne porta solo un rimando.
Motivazione bibliografica: `docs/lit_review/criteri_scelta_descrittori.md` §5.1 (la §5.5 dello stesso file è una bozza superata da questa sezione). **Non** sostituisce
l'ablazione in `analysis/feature_ablation/`, che resta valida sul proprio endpoint — separabilità
1-NN della signature strutturata — e **esplorativa**.

> ⚠️ **§8.12 NON È CONGELATA.** Mancano, e vanno chiusi prima di `exp5-protocol-frozen`:
> mappa famiglia–meccanismo; tabella delle assegnazioni ricevente–run; regola di aggregazione;
> specifica degli intervalli (pesi, bootstrap clusterizzato, accoppiamento donatore–ricevente);
> verifica della coincidenza FULL = B-LF sul decoding; chiusura di E5-C2.

**RQ.** Ciascuna famiglia di descrittori contribuisce all'utilità diagnostica del testo, e il
contributo è specifico del meccanismo che la famiglia è progettata a descrivere?

**Perché serve.** Nel corpus esaminato non emerge un criterio di selezione dei descrittori
applicabile a priori. FaultExplainer mostra che un'evidenza povera — **sei variabili scelte per
contributo al T² della PCA, senza alcun confronto fra descrittori** — limita la diagnosi: **F10
fallisce in entrambe le condizioni**, con e senza catalogo di cause; **F13 è corretto in top-3 solo
con il catalogo** e fallisce senza. Esistono conteggi (7/11 e 9/11 con catalogo, 8/11 entrambi
senza), con le tre qualificazioni di §12.5: top-3, alias accettati, denominatore ai soli 11 fault
rilevati dalla PCA. Questo **non** dimostra che i nostri descrittori colmino quel vuoto: è l'ipotesi
sotto test.

**Popolazione, condizione di riferimento e perimetro.**

*FULL è B-LF, non una condizione nuova.* Coincide **se e solo se** coincidono tutte e sei: stesso
**caso**; stesso **ricevente**; stesso **prompt completo** (esempi locali, libreria di insight, blocco
di politica local-first, testo V2 con il set completo); stesso **modello e configurazione**; stesso
**decoding**; stessa **regola di aggregazione**. La coincidenza del solo nome della politica non
basta. Se tutte valgono, FULL non si riesegue: è **riuso computazionale interno al nuovo studio**, non
riuso inferenziale di dati vecchi, perché B-LF appartiene a questo studio. ⬜ **Punto aperto:** la
verifica del decoding va fatta prima del freeze.

*Un ricevente per run fisico.* Scelto fra i sette agenti diversi dal proprietario della classe.
Assegnazione **bilanciata quanto possibile fra agenti, complessivamente ed entro ciascun fault**, così
che nessun fault sia legato a un solo agente. Algoritmo deterministico e seme documentati; calcolata
sui **soli identificativi dei run**, prima dell'apertura del test e indipendentemente dagli esiti;
tabella completa delle assegnazioni congelata con il protocollo. **Lo stesso ricevente vale per FULL,
PERM e OMIT**, e per tutte le famiglie in cui quel run compare. La scomposizione per agente è
descrittiva: il bilanciamento riduce la concentrazione, **non elimina l'effetto del ricevente**.

*Perimetro della manipolazione.* Si altera **solo il caso interrogato**. Esempi locali, insight della
libreria, contesto e politica restano **fissi e identici** in tutti i bracci.

*Sottoinsieme dei fault per famiglia.* Ogni famiglia gira sui fault del **proprio meccanismo
bersaglio** più **un fault di controllo fuori meccanismo**, fissati prima del freeze e riportati nella
mappa famiglia–meccanismo. OMIT resta su tutto il sottoinsieme, perché la regola di lettura congiunta
ne ha bisogno. I run **non** si riducono. ⚠️ Un solo controllo per famiglia consente il confronto **con
quel controllo**, non con tutti i meccanismi alternativi: il claim segue il sottoinsieme.

**Braccio principale — corruzione per derangement, a parità di forma.** Per ogni famiglia
F ∈ {level, trend, residual, diff}, l'evidenza strutturata di F è sostituita con quella della stessa
famiglia presa da un altro caso. La corruzione si applica **a monte del renderer**, sull'evidenza
strutturata, mai sul testo prodotto: schema, vocabolario controllato e grandezze derivate seguono dal
verbalizzatore congelato. Precedente: Pappa et al. §6.3; strutturalmente è **E applicata al
descrittore invece che alla pseudolabel**.

*Regola di permutazione, da congelare nel protocollo.* Per ciascuna famiglia F si definisce una
permutazione π_F sui casi che è un **derangement, cioè priva di punti fissi**: nessun caso conserva
la propria evidenza di F. Un derangement indipendente per famiglia, ciascuno generato con **seme
documentato e congelato**. Le mappe donatore–ricevente sono costruite e congelate **prima del freeze,
sui soli identificativi**, e applicate all'evidenza solo dopo.

*Gruppo dei donatori.* Il derangement avviene **entro il sottoinsieme S_F effettivamente valutato per
quella famiglia**, e resta disgiunto per classe. Conseguenza da dichiarare: se S_F contiene un solo
bersaglio e un solo controllo con uguale numerosità, l'evidenza del bersaglio proviene **interamente**
dal controllo e viceversa — è una **perturbazione specifica fra due classi**, non una corruzione
rappresentativa. *Nota per E5-C3, preferenza e non requisito.* Dove il costo lo consente e **senza modificare il
sottoinsieme concordato**, un S_F con almeno tre classi consente abbinamenti fra più classi, senza
garantire una perturbazione più rappresentativa. Non è un requisito: per `slope_sigma_h` il
sottoinsieme è necessariamente a due classi — un solo bersaglio, IDV(13), più un controllo — e **quel
caso si mantiene così, con il limite dichiarato**. Aggiungere un secondo controllo cambierebbe
sottoinsieme e budget concordati, e non si fa.

*Disgiuntività per classe (decisa 2026-09-12).* Il derangement è **anche disgiunto per classe**:
nessun caso riceve evidenza da un caso della propria classe. Ragione: una mappatura verso la stessa
classe sostituisce l'evidenza con evidenza simile e **non rimuove davvero l'informazione
diagnostica**, che è ciò che il braccio deve rimuovere. L'effetto di una mappatura intra-classe
**potrebbe** attenuare il contrasto, ma l'attenuazione **non è garantita** né quantificabile a
priori: non va quindi descritta come una conservatività del test.

Il campionamento resta **uniforme sui soli derangement validi** — quelli privi di punti fissi e senza
mappature intra-classe — quindi la disgiuntività non costa nulla sul piano metodologico: non è una
permutazione «meno uniforme», è una permutazione uniforme su un insieme ammissibile più piccolo.

*Che cosa significa «parità di forma».* Significa **stesso schema e stesso multinsieme dell'evidenza
della famiglia permutata**, non uguale lunghezza per singolo caso e **non** uguale distribuzione della
lunghezza totale dei prompt. Il derangement conserva esattamente il multinsieme dell'evidenza di F;
non conserva la lunghezza totale, per due motivi indipendenti: l'evidenza permutata si **abbina** a
un'evidenza diversa nelle altre famiglie, e `rapid` è **ricalcolata** (E5-B) da una combinazione
nuova. Entrambi possono spostare la distribuzione della lunghezza a livello di braccio. La conservazione
del multinsieme non va quindi presentata come garanzia sulla lunghezza: è la ragione per cui il
controllo che segue è obbligatorio e non una formalità.

Vanno tenute distinte due cose che altrimenti si confondono: la **costruzione** garantisce schema e
multinsieme, e nient'altro; la **verifica** (E5-C2) pretende in più una quasi-parità di lunghezza
*caso per caso*, e declassa il braccio se non la trova. La seconda non discende dalla prima: è un
requisito aggiuntivo che il disegno può fallire.

**E5-A — statuto del braccio di omissione *(chiusa)*.** L'omissione cambia insieme informazione e
lunghezza. È **dichiarata analisi secondaria, con il confondente dichiarato**, non mascherata con
riempitivi: un riempitivo neutro a lunghezza appaiata è esso stesso informazione e sposterebbe il
confondente senza eliminarlo. Permutazione e omissione restano separate perché misurano cose diverse
— *se l'LLM si appoggia* al descrittore, contro *se la diagnosi ne ha bisogno*. Una divergenza fra le
due è un risultato.

**E5-B — `rapid` va ricalcolata, mai trasportata *(chiusa)*.** `rapid` è derivata (residual **e** diff
congiuntamente attive). Lasciarla invariata mentre si altera un genitore le fa veicolare l'informazione
che si credeva rimossa. Regola: **in ogni braccio `rapid` è ricalcolata a valle dall'evidenza
effettivamente presente in quel braccio** — nella permutazione, `rapid` = (residual permutata ∧ diff
vera) o simmetricamente. Nell'omissione `rapid` non è computabile e cade con il genitore: quel braccio
rimuove quindi **una famiglia primaria più il canale derivato**, e va dichiarato così.

**Esiti: tabella minima e regola di lettura congiunta.** Per ogni famiglia F e ogni meccanismo M:

| Famiglia | Meccanismo | accuratezza FULL | FULL − PERM | FULL − OMIT | (FULL−PERM) − (FULL−OMIT) |

L'ultima colonna equivale a **OMIT − PERM**: positiva = **maggiore penalizzazione sotto corruzione**.
È lettura complementare, non un endpoint; la soglia di annotazione del 10% resta **solo su FULL −
PERM**. Regola pre-specificata:

- **cali concordi**, cioè **entrambi positivi** → sensibilità della diagnosi alla disponibilità e alla
  qualità dell'evidenza di quella famiglia. Effetti piccoli **non diventano supporto
  automaticamente**;
- **una penalizzazione maggiore sotto PERM rispetto a OMIT** è compatibile con un effetto aggiuntivo
  dell'evidenza incompatibile; se ne riportano **grandezza e incertezza**, senza attribuzione causale
  esclusiva;
- **esiti discordanti o incerti** → **non conclusivi**, e si riportano come tali.

*Asimmetrie, da dichiarare ogni volta che i due cali si confrontano.* OMIT modifica informazione,
lunghezza e struttura del prompt. PERM conserva lo schema e, sull'insieme di permutazione, il
multinsieme dell'evidenza primaria, ma può modificare la lunghezza dei singoli prompt e le
combinazioni fra famiglie. E5-C2 controlla la quasi-parità di lunghezza fra FULL e PERM. Per
`residual` e `diff`, OMIT elimina **anche `rapid`**. **Una violazione di E5-C2 impedisce di attribuire
il contrasto alla sola informazione della famiglia, anche in regime descrittivo: l'avvertenza non è
ornamentale.**

**E5-C — fault, effetto minimo, run, criterio di successo *(aperta)*.**

- *Catalogo dei fault: non se ne apre uno nuovo.* L'esperimento gira sugli **8 fault di D1** — i 4 di
  continuità (F1, F8, F10, F13) più i 4 nuovi — e sui **run per fault di D2**. E5-C **dipende quindi
  dalla 1 e dalla 2 di §0.1** e non è chiudibile prima di quelle.
- *Assegnazione del meccanismo:* Downs & Vogel 1993, secondo §12.4. Cieca rispetto a quali feature si
  attivano nei nostri dati: selezionare guardando le attivazioni sarebbe selezione sull'esito.
- *Drift lento — vincolo accettato.* **IDV(13) è l'unico fault documentato per il meccanismo slow
  drift.** Si adotta quindi **un solo fault per quel meccanismo**, con più run indipendenti: il
  meccanismo resta uno dei quattro, ciò che manca è una seconda istanza al suo interno. Conseguenza
  da rispettare nel testo del paper: **la conclusione sul drift riguarda IDV(13), non i drift lenti
  in generale.** Le valvole bloccate IDV(14)/(15) non
  sono utilizzabili come secondo drift, perché assegnerebbero il meccanismo dalla firma attesa; un
  dataset esteso è escluso dalla decisione P0/Via B, che fissa la generazione Simulink a 1 minuto per
  conservare le feature congelate.
*Le tre voci aperte non hanno la stessa dipendenza.* **E5-C1** ed **E5-C2** sono indipendenti da D1 e
da D2 e sono **chiudibili subito**; solo **E5-C3** deve attendere.

| Voce | Dipende da | Quando |
| --- | --- | --- |
| **E5-C1** — effetto minimo di interesse | nulla: è una scelta di merito scientifico. D2 determina soltanto se quell'effetto sia *rilevabile*, non quale sia | ✅ **chiusa: Δ ≥ 0,10** |
| **E5-C2** — soglia del controllo di lunghezza | modello e formato dei prompt; **non** dal numero di run | ⏳ **provvisoria: ≤ 5% per caso** — si chiude solo dopo la verifica di fattibilità |
| **E5-C3** — criterio di successo completo | D1, D2, **e** i valori fissati in E5-C1 ed E5-C2 | ⬜ dopo le altre |

- *Run per fault: **ereditati da D2**, non decisi di nuovo qui.* Ne segue che il numero di run è un
  vincolo in ingresso e non un'incognita: l'effetto minimo rilevabile è una **conseguenza** della
  scelta fatta in D2, non un parametro da cui calcolare i run. Se l'effetto che D2 rende rilevabile è
  più grande di quello di interesse, è un limite da dichiarare nel paper — non una ragione per
  cambiare D2 dentro questo esperimento.
- *E5-C1 — effetto minimo di interesse:* ✅ **fissato (2026-09-12): 10 punti percentuali assoluti** di
  accuratezza top-1 sul meccanismo bersaglio.

  `Δ_F = accuracy_FULL − accuracy_PERM_F ≥ 0,10`

  Lettura: almeno **una diagnosi corretta in più ogni dieci casi**. È una soglia di rilevanza
  pratica, scelta sul merito e **indipendente da modello e numerosità**; non è una soglia di
  significatività. Effetti inferiori **vanno riportati**, ma non possono sostenere la necessità
  pratica del descrittore.

  *Segno.* Δ_F può risultare **negativo** — la corruzione migliora l'accuratezza. Non è ipotesi di
  scuola: l'ablazione in `analysis/feature_ablation/` mostra già rimozioni che *alzano* il margine.
  I valori negativi vanno riportati come tali, mai troncati a zero né riportati in valore assoluto.

  *Nota da portare in E5-C3.* Con i run di D2 l'accuratezza per meccanismo si misura su poche unità
  indipendenti — 6 o 8 per IDV(13), circa il doppio dove i fault per meccanismo sono due. La
  granularità della stima puntuale è quindi grossolana rispetto a 10 punti, e su IDV(13) il più
  piccolo effetto non nullo osservabile è già ≥ 12,5 punti con 8 run. Non è un problema di E5-C1, che
  fissa una soglia di rilevanza e non di misurabilità; è un vincolo che E5-C3 deve assorbire quando
  tratterà incertezza e specificità di meccanismo.

  Si confronta **poi** con ciò che D2 rende rilevabile: se D2 non lo raggiunge, è un limite da
  dichiarare, non una ragione per rivedere l'effetto dopo aver visto il campione.
- *E5-C2 — soglia del controllo di lunghezza:* ⏳ **provvisoria (2026-09-12)**: scarto relativo ≤ 5%
  per caso e zero differenze di troncamento. Si chiude dopo la verifica di fattibilità. Specifica
  completa nel blocco «E5-C2» sopra.
- *Endpoint:* accuratezza diagnostica top-1 **per meccanismo**, unità = *physical run*, bootstrap
  clusterizzato. Contrasto: FULL − PERM_F per ciascuna famiglia F.
- *Limite principale, già noto e da dichiarare nel paper.* Con D2 pari a 6 o 8 run, **IDV(13) fornisce
  soltanto 6 o 8 unità indipendenti**: è l'unico fault del meccanismo slow drift, quindi non c'è una
  seconda istanza su cui accumulare potenza. Senza run aggiuntivi dedicati, **il risultato su
  `slope_sigma_h` resta esplorativo e non può sostenere un criterio inferenziale forte.** È il
  descrittore che ha già meno evidenza a favore (`analysis/feature_ablation/`), quindi il limite cade
  esattamente dove farebbe più danno. **Via scelta (2026-09-12): risultato esplorativo, senza run
  dedicati.** E5 eredita D2 e non lo modifica; aggiungere run del solo IDV(13) richiederebbe
  **riaprire D2 esplicitamente**, e non è una cosa che questo esperimento può fare per conto proprio.
- *E5-C3 — statuto **DESCRITTIVO**.* **Modifica deliberata del protocollo, 2026-09-12.** La
  formulazione precedente prevedeva un livello **inferenziale** per `level`/`residual`/`diff` e uno
  descrittivo per `slope_sigma_h`; è sostituita da uno statuto descrittivo integrale. Motivo:
  proporzione a un paper di 10 pagine, e un solo fault per meccanismo su almeno un meccanismo, che
  rende la gerarchia a due livelli più fragile di quanto appaia.

  Si riporta la tabella degli effetti per famiglia e meccanismo, con **intervalli dichiarati
  esplorativi**. **Nessun test di ipotesi, nessuna correzione per molteplicità.** La lettura resta
  orientata alla **specificità di meccanismo**: un calo concentrato sul meccanismo che la famiglia
  descrive dice altro da un calo uniforme, che indica perdita di informazione generica.

  Restano da fissare prima del freeze: **mappa famiglia–meccanismo**; **regola di aggregazione** (per
  fault, run, ricevente); e la specifica degli intervalli — **pesi, procedura del bootstrap
  clusterizzato e trattamento dell'accoppiamento donatore–ricevente**, che non è indipendenza fra
  osservazioni e va dichiarato. Un capoverso in metodologia, non un apparato.

**E5-C2 — controllo di lunghezza: ⏳ regola PROVVISORIA (2026-09-12).** Soglia **operativa**, non
statistica, applicata **senza modificare in seguito derangement o prompt**. **Non è chiusa:** il valore
del 5% può ancora cambiare all'esito della verifica di fattibilità, e finché può cambiare non va
segnato come deciso. Si chiude — e diventa congelabile — solo dopo quella verifica.

- *Conteggio:* con il **tokenizer del modello effettivamente usato**, sul **prompt completo**, non su
  un suo frammento né su una stima.
- *Criterio, per ogni coppia FULL / PERM_F e per ogni caso:*
  `|token_PERM − token_FULL| / token_FULL ≤ 5%`
- *Troncamento:* **zero differenze di troncamento** fra i due bracci.
- *Conseguenza:* se anche **un solo caso** supera il 5% o viene troncato diversamente, il contrasto
  di quella famiglia è **riportato con avvertenza esplicita di confondimento con la lunghezza**,
  accanto al contrasto stratificato per lunghezza. In regime descrittivo l'avvertenza non è
  ornamentale: una violazione **impedisce di attribuire il contrasto alla sola informazione della
  famiglia**. Non si sostituisce il braccio, non si rigenera il derangement, non si riscrive il
  prompt dopo aver visto i dati.

*Il controllo con `rapid` congelata al valore vero resta solo diagnostico:* serve ad attribuire uno
scostamento all'abbinamento fra famiglie o al ricalcolo di `rapid`, non è un braccio sperimentale e
non entra in nessun contrasto riportato.

⚠️ **Verifica di fattibilità, da fare prima del freeze e non dopo.** La regola è a scatto singolo: un
caso fuori soglia declassa l'intera famiglia, e non è rimediabile dopo il congelamento. È quindi
necessario misurare **in anticipo, sui soli dati di sviluppo e con il verbalizzatore congelato**, la
distribuzione effettiva di `|Δtoken|/token_FULL` sotto derangement disgiunto per classe. Il rischio è
concreto: una famiglia occupa una frazione non trascurabile del testo, e un caso che riceve evidenza
molto più attiva della propria può spostare il totale oltre il 5%. Se la misura mostra che il 5% non è
raggiungibile, la soglia va rivista **prima** di `exp5-protocol-frozen` — non dopo, e mai dopo aver
visto un risultato diagnostico. Questa verifica non apre validazione né test e non consuma chiamate al
modello oltre la tokenizzazione.

*Che cosa può motivare una revisione del 5%, e che cosa no.* Solo **misure di lunghezza** — la
distribuzione osservata di `|Δtoken|/token_FULL` sui dati di sviluppo. **Mai un risultato
diagnostico:** nessuna accuratezza, nessun contrasto, nessuna anteprima dell'endpoint può entrare
nella scelta della soglia, altrimenti il controllo smette di essere indipendente da ciò che deve
proteggere. Ogni revisione va **registrata qui con la sua misura e la sua data, prima del freeze**;
dopo `exp5-protocol-frozen` la soglia non si tocca più, qualunque cosa mostri l'esecuzione.

**Limiti dichiarati.**

- **Seme unico di derangement.** Il risultato è relativo **alla corruzione realizzata**, non alla
  media su tutte le corruzioni possibili.
- **I donatori possono condividere il meccanismo del ricevente.** La disgiuntività è per **classe**,
  non per meccanismo. Va documentata la **matrice degli abbinamenti**. *Opzionale, senza chiamate
  aggiuntive:* riportare FULL − PERM stratificato fra donatori di stesso e diverso meccanismo.
- **Meccanismi con un solo fault.** Il risultato riguarda **quella classe**, non il meccanismo. Regola
  valida per tutto il catalogo finale, non solo per IDV(13).

**Manifest dei dati e dei ruoli.**

| Ruolo | Dati | Nota |
| --- | --- | --- |
| Sviluppo | vecchi batch F1/F8/F10/F13 già osservati, tabelle `code/tep_analysis_v2/`, ablazione esistente | **usati nello sviluppo della rappresentazione e delle ipotesi**: non sono evidenza confermativa |
| Baseline | N1–N5, tratto Normal continuo | statistiche di riferimento del verbalizzatore |
| Calibrazione storica | le 50 finestre da N1–N5 usate per le soglie di Fase A | il FAR storico è un **conteggio in-sample**, non una verifica indipendente. Per l'eredità o meno delle soglie vale `docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md`: qui non se ne riformula la decisione |
| Test | **nuovi run degli otto fault di D1** — quattro classi di continuità e quattro nuove | la selezione storica del catalogo resta un **limite di generalizzazione** dichiarato |

**Costo.** Bracci corrotti: **2n · Σ_F (m_F + c_F)**, con n run per fault, m_F fault bersaglio e
c_F = 1 controllo. FULL: **n · |∪_F S_F| ≤ 8n**. Scenario a 3 fault per famiglia, R = 1, un ricevente
per caso, **FULL riusato da B-LF**: **144** chiamate a 6 run, **192** a 8 — circa il **6%** dello
studio. Perimetro pieno, per confronto: **lordo 3.024 / 4.032**; **aggiuntivo con FULL riusato
2.688 / 3.584**.

**Molteplicità.** Tutti gli esiti sono **descrittivi**: non si applica correzione per molteplicità
perché non si eseguono test. Unità = *physical run*, bootstrap clusterizzato per gli intervalli
esplorativi; mai trattare le osservazioni agent-case come indipendenti.

**Ordine di generazione e congelamento.** I **run fisici possono essere simulati prima del freeze ma
restano sigillati**. *Sigillato* significa: **nessuna ispezione di segnali, feature o risultati del
test per decisioni progettuali**; sono ammesse le verifiche tecniche predefinite che non orientano
tali decisioni. **Prima del freeze** si costruiscono e si congelano, **sui soli identificativi**, le
mappe donatore–ricevente e le assegnazioni degli agenti. **Dopo il freeze** si applicano le mappe
all'evidenza e si producono omissioni e prompt.

E5-C1 va fissata **prima** di conoscere la potenza disponibile, altrimenti l'effetto minimo finisce
adattato al campione.

1. ✅ **E5-C1** fissata: Δ ≥ 0,10 come soglia di annotazione;
2. ⏳ **E5-C2** provvisoria; si chiude con la **verifica di fattibilità** sulle sole lunghezze;
3. chiudere **D1** e **D2**; verificare la coincidenza **FULL = B-LF** sul decoding;
4. formulare **E5-C3** — mappa famiglia–meccanismo, regola di aggregazione, specifica degli intervalli;
5. costruire e congelare mappe e assegnazioni sui soli identificativi;
6. congelare con `exp5-protocol-frozen`; poi applicazione delle mappe, generazione di omissioni e
   prompt → esecuzione → results.

---

## 9 · Baseline FL — FedAvg minimale

Delle quattro estensioni proposte nella revisione 1, tre sono state riassorbite o eliminate:

- il **test fuori catalogo** è promosso a componente del piano consolidato (§8.6)
- il **confronto Q4 formale** è eliminato (§4.3)
- la **condizione A+** è eliminata: già dimostrata nell'esplorativo (A+ = A = 0/36)

La quarta — la baseline FL — non è più opzionale: **D8 è risolta con un sì**, nella forma descritta qui.

### 9.1 Perché FedAvg e non FedProto

FedProto è poco naturale su questo compito. Con clienti class-disjoint, ogni fault appartiene a un solo client e l'unica classe condivisa è Normal: l'aggregazione di prototipi ha quasi nulla da aggregare, e l'oggetto federato che ne risulta — un prototipo per classe — è lo stesso della baseline numerica a prototipi, che **esiste già** nel piano. ⚠️ *Precisazione della revisione 4:* **la ridondanza è concettuale, non empirica.** FedProto apprende anche la rappresentazione e aggrega la classe Normal fra gli otto client, quindi prevedere che «produrrebbe un numero quasi identico» sarebbe una previsione non dimostrabile e facilmente falsificabile. Ciò che si può affermare è che resterebbe nella stessa famiglia di oggetto federato già rappresentata nel piano — ed è esattamente questo che rende FedAvg il comparatore realmente diverso.

FedAvg è la scelta corretta:

| Criterio | FedAvg |
| --- | --- |
| Riconoscibilità | canonica; nessun reviewer FL chiede che cosa sia |
| Adeguatezza al compito | il label-skew class-disjoint è esattamente il regime in cui è studiata |
| Dati | eseguibile sulle stesse feature 697-D |
| Costo API | **zero** |
| Disponibilità | avviabile subito, non attende Qwen: non compete con il cammino critico di §7 |
| Attesa dei reviewer | **è il comparatore atteso in questa letteratura**: P041 e P030 eseguono entrambi FedAvg (OpenFedLLM). P031, pur essendo un paper di FL a ICLR 2025, non lo esegue mai — ed è una debolezza visibile. Non eseguirlo significa presentarsi sotto lo standard dei lavori con cui si verrà confrontati. |

**Comparatori FL già pubblicati sullo stesso benchmark** *(revisione 4)*. FedAvg non va presentata come l'unico riferimento FL disponibile su TEP. §14.1 del walkthrough contiene due lavori 🟢 testati sul Tennessee Eastman:

- **Zhang et al. 2026**, *Federated Meta-Learning with Transformer Fusion for Few-Shot Multi-Condition Fault Diagnosis*, Knowledge-Based Systems, DOI [10.1016/j.knosys.2026.116739](https://doi.org/10.1016/j.knosys.2026.116739);
- **Xu et al. 2026**, *Federated Learning Based on Fuzzy Fusion Rules for Chemical Production Process Fault Diagnosis*, Sensors, DOI [10.3390/s26113545](https://doi.org/10.3390/s26113545).

§14.2 li descrive come comparatori numerici diretti sullo stesso processo. **Non vanno riprodotti** — protocolli, split e compiti sono diversi, e riprodurli sarebbe un progetto a sé — ma vanno citati in §9 e nella related work, con la differenza di compito dichiarata. Presentare una baseline FL su TEP senza nominarli espone allo stesso rischio che §8.10 punto 8 vuole evitare.

### 9.2 Specifica minima da congelare

- rete **molto semplice**, output condiviso sulle **nove classi** (8 fault + Normal)
- addestramento federato sugli **otto client**, ciascuno con Normal + il proprio fault
- addestramento sui soli **dati di sviluppo**; valutazione sui run di test congelati
- ricetta standard documentata: round, epoche locali, learning rate, architettura, seed
- **nessun tuning sul test**, e specifica congelata prima di guardare i risultati
- **stesso protocollo di valutazione del braccio LLM**: unità statistica = run (cluster), stesso bootstrap appaiato, stesse metriche. Senza questo, il confronto non è appaiato e non è interpretabile.

### 9.3 I due numeri di contorno che rendono il risultato difendibile

FedAvg sotto label-skew estremo è noto per comportarsi male: la deriva del classificatore condiviso è documentata proprio in questo regime. Il rischio non è che il numero sia basso, è che un reviewer dica **"avete scelto una baseline costruita per fallire"**.

La difesa costa quasi nulla, perché è lo stesso codice eseguito due volte in più:

| Riferimento | Che cos'è | Che cosa dimostra |
| --- | --- | --- |
| **Pavimento** | la stessa rete addestrata da ogni client **da solo**, senza federazione | quanto vale la sola conoscenza locale in forma numerica |
| **FedAvg** | la baseline federata | che cosa ottiene il metodo FL canonico sotto questo skew |
| **Soffitto centralizzato** | la stessa rete addestrata sui **dati aggregati** | che la penalità è dovuta allo skew federato, non a un'implementazione debole |

Tre numeri da un solo codebase, zero chiamate API. Il soffitto centralizzato è la riga che disinnesca l'accusa di baseline azzoppata, ed è gratuito.

**La revisione 3 alza la priorità di questo blocco.** Il **pavimento** — ogni client da solo, senza collaborazione — è assente in P042, P030 e P031, e in P041 esiste solo in forma indiretta (Fed-ICL-LB). Senza pavimento non si sa quanto valga la sola conoscenza locale, e quindi quanto valga davvero la federazione: è la lacuna che rende i guadagni di quei lavori difficili da interpretare. Qui il pavimento esiste già in forma LLM — è la condizione A — quindi **riportarlo anche in forma numerica costa una sola esecuzione in più**. ⚠️ *Correzione della revisione 4:* non va presentato come un buco della letteratura comparabile. **P065 riporta il pavimento Local-Only in tabella**, su GSM8k, su τ-bench retail e per organizzazione. L'affermazione corretta è quindi «assente in P042, P030 e P031, indiretto in P041 (Fed-ICL-LB), presente in P065». Resta una difesa necessaria della baseline — senza pavimento non si sa quanto valga la federazione — e questo giustifica di eseguirlo prima e non dopo la disponibilità del modello. Non è però un elemento differenziante.

**Rischio residuo, da accettare in anticipo:** se FedAvg o il soffitto centralizzato battono nettamente FoT sulle stesse feature, il paper deve riportarlo. Sarebbe un risultato onesto e informativo — il trasferimento testuale non è competitivo con il trasferimento numerico su questo compito — ma cambierebbe il framing del lavoro. Meglio saperlo ora, che è possibile proprio perché FedAvg non dipende da Qwen ed è eseguibile questa settimana.

---

## 10 · Decisioni da congelare prima di aprire i run di test

### D1 — Quali 8 fault?

Criteri ammessi, in questo ordine:

1. **Copertura dei meccanismi fisici** documentati in Downs & Vogel 1993: step, random variation, slow drift, sticking valve.
2. **Identità della variabile perturbata**, per evitare duplicati funzionali. Verificabile direttamente dalla loro tabella dei fault: per esempio F3 e F9 agiscono sulla **stessa** variabile — temperatura di alimentazione D — con perturbazioni diverse (step vs random variation), e sono quindi candidati a duplicato funzionale.
3. **Stratificazione per difficoltà documentata in letteratura** (§12), non per separabilità osservata nei propri dati.

I 4 fault di continuità (F1, F8, F10, F13) sono dichiarati come tali. I 4 nuovi vanno scelti prima di osservare qualunque risultato; per la massima difendibilità, estrazione casuale con seed documentato dentro ogni strato di difficoltà.

**Raccomandazione sulla stratificazione:** includere deliberatamente almeno 2 fault documentati come difficili. Un 78% con i fault difficili dentro è più pubblicabile — e molto più difficile da attaccare — di un 97% su un catalogo selezionato.

### D2 — Quanti run per fault nel test? *(aperta, e prezzata)*

Minimo 6 (48 cluster, contro 12 dell'Exp1 e 24 della replica). Con 8 run (64 cluster) gli intervalli si stringono.

Il costo reale della decisione, ricalcolato in §8.8: **+590 chiamate, +24%**, da ~2.450 a ~3.040, con tetto da 3.000 a 3.500. Non cambia la finestra temporale di §7, perché il collo di bottiglia è la data della decisione sul modello e non il volume. Con R=1 la scelta è quindi economicamente sostenibile in entrambe le direzioni, e va presa sul merito statistico: 64 cluster restringono gli intervalli fra run e allargano il margine di manovra su H3, che è il test di non inferiorità e quindi il più esigente in termini di potenza. Nota che più cluster non compensano la componente lasciata non stimata da R=1 (§8.7): sono due fonti di variabilità distinte.

### D3 — Tutti e 7 i riceventi o un sottoinsieme?

Tutti e 7. Il costo è lineare, la potenza statistica dipende dai cluster (48 o 64) e non dalle coppie (336 o 448), e la scomposizione per agente è un'analisi descrittiva gratuita.

### D4 — A+ sì o no?

**No.** Già dimostrata nell'esplorativo. Eliminata anche come opzione.

### D5 — E deve essere completa?

**Sì, indispensabile, e nella variante E-LF.** È il controllo che distingue "il testo funziona perché contiene informazione corretta" da "il testo funziona perché c'è più contesto". Senza E il claim principale perde il supporto causale. Non ridurre a campione.

### D6 — Standard B e local-first: uno o entrambi?

**Risolta: B-LF è il metodo.** Local-first è un blocco di politica decisionale nel prompt, già congelato come `B_LOCAL_FIRST_V1` e già validato in §10.3. Non è una quarta condizione. B senza local-first sopravvive solo come ablation su sottoinsieme dichiarato (§8.3). L'override esterno è ritirato (§8.2).

### D7 — R=1 o R=3?

**Gate tecnico, non soglia numerica.** Nessuna divergenza osservata nel pilot → R=1 con audit continuo. Divergenze osservate → R=3 sull'intero studio e non-determinismo nel modello di varianza. La soglia dell'1% è rimossa, e nella revisione 4 lo è anche quella del 2,5%: le osservazioni indipendenti sono i **40 prompt**, non le 120 chiamate, quindi il limite della regola del tre è ≈ **7,5%** (§8.7). Unità statistica e definizione dell'evento di divergenza vanno scritte nel protocollo prima del pilot.

**R=1 resta un compromesso operativo.** Non stabilisce che il modello sia deterministico né che la variabilità delle risposte sia nulla: lascia quella componente non stimata, e per questo l'audit a R=3 e il set canary sono parte della decisione, non un complemento facoltativo (§8.7).

### D8 — Baseline FL *(risolta: sì, FedAvg minimale)*

**Decisione: implementare una FedAvg piccola, non FedProto.**

FedProto sarebbe **concettualmente** ridondante su questo compito: con clienti class-disjoint, ogni fault appartiene a un solo client e l'unica classe condivisa è Normal, quindi l'aggregazione di prototipi ha quasi nulla da aggregare e l'oggetto federato resta un prototipo per classe, cioè lo stesso della baseline numerica che già esiste. La ridondanza è di **famiglia**, non di numero atteso: FedProto apprende la rappresentazione e aggrega Normal, quindi prevederne il risultato sarebbe scorretto (§9.1).

FedAvg è invece la scelta giusta per cinque ragioni: è **canonica e immediatamente riconoscibile** da qualunque reviewer FL; è **adatta al label-skew class-disjoint**, che è esattamente il regime in cui è studiata; è **eseguibile sulle stesse feature 697-D**; **non consuma chiamate API**; ed è **avviabile subito**, senza attendere la disponibilità di Qwen — quindi non compete con il cammino critico di §7 nel modo in cui competerebbe un lavoro che dipende dal modello.

Specifica minima, da congelare prima di guardare il test: rete molto semplice con **output condiviso sulle nove classi**, addestrata federativamente sugli **otto client**, ricetta standard (numero di round, epoche locali, learning rate, architettura) documentata e **nessun tuning sul test**.

Vedi §9.1 per la specifica completa e per i due numeri di contorno che rendono il risultato difendibile.

### D12 — Schema degli insight *(aperta, lavorabile oggi)*

Campi, tipi, cardinalità fissa, cap di lunghezza per singolo insight, validatore eseguibile (§8.9). Va congelata **prima della produzione degli insight**, non prima dei run di test, perché vincola il modo in cui entrambi i producer generano. Non dipende dalla disponibilità del modello e non consuma budget.

Tre vincoli che la decisione deve soddisfare: lo schema è identico per i due producer; E si ottiene permutando soltanto il campo pseudolabel; validità, retry, troncamenti e token sono loggati per producer e condizione.

**Due indicazioni della revisione 4, da EviFDD-Agent (§8.9).** Il validatore va costruito sulla modalità di fallimento documentata — la parafrasi degli **identificatori di variabile**, non l'errore numerico. E va valutata la separazione fra campi serializzati deterministicamente dal verbalizzatore e parte narrativa lasciata al producer: nelle condizioni in cui i campi critici non passano dal modello, EviFDD ottiene URR = 0.

### D9 — Piano B, con date

1. **Qwen-2.4T** se disponibile e se supera il pilot **entro il 17 settembre** (§7).
2. **Altrimenti Qwen-27B** come producer e consumer dello studio finale, dopo un pilot breve. Configurazione degradata ma non compromessa: il braccio producer-swap resta intatto usando Terra come producer alternativo, quindi **G5 resta coperta**. Va scritto esplicitamente nel paper che il modello non è "nuovo".
3. Se anche Qwen-27B non supera parsing, stabilità e lunghezza del contesto: **fermare l'espansione** e scegliere tra paper Terra-only e conferenza successiva.

La copertura dell'opzione 3 va costruita adesso, non quando serve: le sezioni condivise tra le due versioni del paper sono circa il 60% del testo (§6.12).

### D10 — `Unknown` nello spazio delle etichette *(risolta nella revisione 5: `Unknown` è il nome dell'astensione esistente)*

**Sì, in tutte le condizioni, dall'inizio.** Non solo nel test OOD.

**La decisione residua era quale forma dare a `Unknown`, ed è ora congelata.** Le due strade non erano equivalenti, e la formulazione precedente le confondeva:

| Forma | Che cosa comporta |
| --- | --- |
| **`Unknown` = l'astensione già implementata** *(scelta)* | `abstain=true` con `predicted_label=null`. Schema di output, parser e due dei tre numeri di §8.5 esistono già e sono validati. Resta da aggiungere la terza metrica — accuratezza sui soli casi non astenuti — e da dichiarare il framing comparativo. |
| `Unknown` come label letterale | Non è una modifica di configurazione. `phase_b/config/protocol.py` impone cinque label con `Normal` in ultima posizione e fallirebbe in modo esplicito; se quel validatore venisse rilassato, l'idioma posizionale `label_space[:-1]` — **undici occorrenze**, in `insights/library.py` (validazione insight e dominio del derangement di E), `evaluation/bootstrap.py`, `execution/generate_final_insights.py`, `local_knowledge/build_local_examples.py` e cinque punti dentro `tests/` — farebbe entrare `Normal` nel dominio dei fault. Inserire `Unknown` prima di `Normal` non risolve: verrebbe trattato esso stesso come fault. Servirebbe sostituire l'assunzione posizionale con categorie semantiche esplicite — pseudolabel dei fault, `Normal`, esito open-set — e riscrivere i test perché **verifichino** quella separazione invece di riprodurla. |

La seconda strada tocca i percorsi che governano derangement ed E, cioè il contrasto causale B−E: è la via a maggior rischio metodologico per un guadagno espressivo. **Si congela la prima.**

**Conseguenze da congelare:** i tre numeri dell'endpoint di §8.5, riportati separatamente per A, B-LF ed E-LF (S11b); e la dichiarazione che il confronto descrittivo con l'esplorativo resta indebolito da scala, modello e lunghezza del contesto — ma **non** dallo spazio delle etichette, per la verifica sugli artefatti riportata in §8.6.

### D11 — Sottoinsieme dell'ablation local-first

Le coppie di fault confondibili vanno identificate su base meccanica — variabile perturbata o meccanismo condivisi secondo Downs & Vogel — e **dichiarate prima** di osservare le confusioni del test (§8.3).

---

## 11 · Checklist GO/NO-GO

### Prerequisiti tecnici

| # | Requisito | Stato | Bloccante? |
| --- | --- | --- | --- |
| T1 | API del modello scelto funzionante e stabile | ⬜ | **SÌ** |
| T2 | Capability pilot completato con esito positivo | ⬜ | **SÌ** |
| T3 | Formato JSON compatibile con il parser, astensione inclusa — `abstain=true` con `predicted_label=null` (D10) | ⬜ | **SÌ** |
| T4 | Reasoning budget sufficiente con 14 insight | ⬜ | **SÌ** |
| T5 | Latenza compatibile con il tetto di §8.8 (3.000 o 3.500) nella finestra di §7 | ⬜ | **SÌ** |
| T6 | Gate di stabilità superato (nessuna divergenza) o R=3 attivato | ⬜ | **SÌ** |
| T7 | Logging esteso attivo: ID modello restituito, request ID, fingerprint, hash, latenza | ⬜ | **SÌ** |
| T8 | Set canary definito, con output atteso congelato e schedulazione giornaliera | ⬜ | **SÌ** |
| T9 | Logging di conformità attivo: validità schema, retry, troncamenti, token per insight e per prompt (§8.7) | ⬜ | **SÌ** |
| T10 | Capacità di determinismo dell'API registrate nel pilot — temperatura e seed esposti o no — con la regola interpretativa di §8.7 congelata | ⬜ | **SÌ** |
| T11 | Tasso di astensione in-catalogo misurato nel pilot nelle tre condizioni, a 14 insight e 9 classi (§8.6) | ⬜ | No, ma è la condizione di validità del test OOD |

### Prerequisiti scientifici

| # | Requisito | Stato | Bloccante? |
| --- | --- | --- | --- |
| S1 | 8 fault selezionati con criteri documentati e congelati, senza criteri di separabilità | ⬜ | **SÌ** |
| S2 | Run di sviluppo generati per tutti gli 8 fault + Normal | ⬜ | **SÌ** |
| S3 | Run di test generati, congelati e hashati, con seed distinti da quelli di sviluppo | ⬜ | **SÌ** |
| S4 | Soglie calibrate sui soli Normal di sviluppo | ⬜ | **SÌ** |
| S5 | Insight prodotti e congelati, **per entrambi i producer** (libreria completa) | ⬜ | **SÌ** |
| S6 | Piano statistico completo scritto e congelato | ⬜ | **SÌ** |
| S7 | Le 9 pseudolabel, la forma dell'astensione (D10) e la permutazione E congelate | ⬜ | **SÌ** |
| S8 | Prompt, template e le tre condizioni congelate | ⬜ | **SÌ** |
| S9 | Baseline numerica preparata (prototipi dai dati di sviluppo) | ⬜ | **SÌ** |
| S10 | Le tre ipotesi H1–H3 scritte, con il margine *m* di non inferiorità e la sua giustificazione esterna | ⬜ | **SÌ** |
| S11 | Gerarchia di test (gatekeeping H1 → H2 → H3) congelata | ⬜ | **SÌ** |
| S11b | Definizione dei tre numeri dell'endpoint con l'astensione e indicazione del primario, con la regola esplicita: **i tre numeri sono calcolati e riportati separatamente per A, B-LF ed E-LF** | ⬜ | **SÌ** |
| S12 | Coppie confondibili dell'ablation dichiarate prima — **dipende da S1** | ⬜ | **SÌ** |
| S13 | Due fault OOD scelti, meccanicamente distinti da tutto il catalogo **e non appartenenti al gruppo compensato dal controllo** (§8.6, §12.1) — **dipende da S1** | ⬜ | **SÌ** |
| S14 | Regola di reporting stratificato (continuità / nuovi / aggregato) scritta | ⬜ | No, ma raccomandata |
| S15 | Specifica FedAvg congelata: architettura, round, epoche locali, lr, seed, e protocollo di valutazione identico al braccio LLM | ⬜ | **SÌ** se la baseline entra nel paper |
| S16 | Pavimento locale e soffitto centralizzato pianificati insieme a FedAvg (§9.3) | ⬜ | No, ma è la difesa della baseline |
| S17 | Schema degli insight congelato: campi, tipi, cardinalità, cap per elemento, validatore eseguibile (§8.9) | ⬜ | **SÌ** |
| S18 | Diff B↔E verificato e allegato: differisce esclusivamente nel campo pseudolabel (§8.9) | ⬜ | **SÌ** |
| S19 | Parità strutturale fra i due producer verificata sugli insight congelati (§8.4) | ⬜ | **SÌ** |

**Precedenze fra prerequisiti** *(revisione 4)*. La tabella elenca i requisiti, non il loro ordine, e questo ha fatto sembrare risolvibili subito prerequisiti che non lo sono.

| Requisito | Dipende da | Perché |
| --- | --- | --- |
| S3, S4 | S1, S2 | run di test e soglie si generano per gli 8 fault già scelti |
| S12 | S1 | «coppia confondibile» è definita rispetto al catalogo |
| S13 | S1 | «meccanicamente distinto da tutto il catalogo» è definito rispetto al catalogo |
| S5 | S17 | lo schema vincola il modo in cui entrambi i producer generano (§6.10, D12) |
| S18, S19 | S5, S17 | si verificano su insight già prodotti e congelati |

Conseguenza da riportare in §7: **S13 è bloccante e indipendente dal modello, ma non è lavorabile oggi.** Il suo cammino passa da §6.1 e da D1. Lo stesso vale per S12. Contarli fra le attività immediatamente avviabili rende la cronologia critica più ottimistica di quanto sia.

### Prerequisiti organizzativi

| # | Requisito | Stato | Bloccante? |
| --- | --- | --- | --- |
| O1 | Piano B definito e datato (D9) | ⬜ | **SÌ** |
| O2 | Budget API come tetto: **3.000** con 6 run, **3.500** con 8 run (§8.8) | ⬜ | **SÌ** |
| O3 | Decisione sul modello presa entro il 17 settembre | ⬜ | **SÌ** |
| O4 | Decisione su baseline FL | ✅ | risolta: FedAvg minimale (D8, §9) |
| O6 | Le cinque decisioni indipendenti dal modello di §0.1 congelate | ⬜ | **SÌ** |
| O5 | Sezioni del paper indipendenti dal modello iniziate (§6.12) | ⬜ | No, ma è l'unica copertura reale |

### Regola GO/NO-GO

**GO** se e solo se tutti i requisiti bloccanti sono soddisfatti.

**NO-GO** se almeno uno non lo è. In quel caso:
- blocco T1 → attivare D9 opzione 2
- blocco T2–T8 → valutare se è risolvibile in 24 ore; oltre, D9 opzione 2
- blocco T6 → non è un NO-GO ma un passaggio a R=3, con ricalcolo del budget e della finestra temporale
- blocco S1–S14 → completare il prerequisito, non procedere
- blocco O3 → D9 opzione 3

---

## 12 · Fonti esterne: difficoltà per-fault e prior art federato

Le sottosezioni 12.1–12.5 riguardano la difficoltà per-fault nel TEP. Le sottosezioni 12.6–12.9, nuove nella revisione 3, riguardano il prior art sull'ICL federato e le sue conseguenze sulla novità rivendicabile.

### Parte prima — difficoltà per-fault nel TEP

Questa sezione esiste perché la revisione 1 affermava, senza fonte, che F3, F9 e F15 sono "quasi indistinguibili". L'autore ha contestato l'affermazione; la verifica ha trovato le fonti, **e nel farlo ha corretto l'affermazione stessa**.

⚠️ **Le fonti dicono una cosa diversa da quella che la revisione 1 sosteneva.** Documentano che F3, F9 e F15 sono **difficili da rilevare**, cioè difficili da distinguere da Normal. **Non** documentano che siano difficili da distinguere **tra loro**. Sono due assi diversi: rilevazione (fault vs Normal) e discriminazione (fault vs fault). La formulazione "quasi indistinguibili" confondeva i due e va abbandonata.

La distinzione non è pedanteria, perché i due assi entrano nel piano in punti diversi:

- l'asse **rilevazione** è rilevante per il verbalizzatore, che costruisce le 697-D confrontando con baseline Normal: un fault che quasi non devia da Normal produce evidence quasi vuota, e questo è un problema reale per FoT;
- l'asse **discriminazione** è ciò che il compito di classificazione misura davvero, e su questo le fonti citate **non dicono nulla**.

Il vero argomento di quasi-duplicazione tra F3 e F9 non viene dagli FDR ma da Downs & Vogel: agiscono sulla **stessa variabile** (temperatura di alimentazione D) con perturbazioni diverse. Quell'argomento è strutturale e vale indipendentemente dai tassi di rilevazione. F15 non è duplicato di nulla: è semplicemente compensato dal controllo.

### 12.1 Che cosa dicono le fonti

**Yin, Ding, Haghani, Hao, Zhang (2012)** — *A comparison study of basic data-driven fault diagnosis and process monitoring methods on the benchmark Tennessee Eastman process*, Journal of Process Control 22(9):1567–1581, DOI [10.1016/j.jprocont.2012.06.009](https://doi.org/10.1016/j.jprocont.2012.06.009). È il confronto canonico del settore (oltre 1.200 citazioni). Tassi di rilevazione su otto e più metodi (PCA, DPCA, PLS, TPLS, MPLS, ICA, FDA, SAP):

| Fault | Descrizione | FDR, range tra i metodi |
| --- | --- | --- |
| IDV(3) | D feed temperature, step | 4,5% – 24,25% |
| IDV(9) | D feed temperature, random variation | 0,88% – 23,5% |
| IDV(15) | Condenser cooling water valve, sticking | 7,75% – 29,88% |

Gli autori scrivono che per questi tre fault "all methods give low FDRs thus cannot detect the faults successfully", e ne danno la ragione: hanno **effetto quasi nullo sulla variabile di qualità del prodotto** monitorata.

**Conferma indipendente** — *Fault Detection and Diagnosis in Tennessee Eastman Process with Deep Autoencoder*, Annual Conference of the PHM Society 2023, [papers.phmsociety.org](https://papers.phmsociety.org/index.php/phmconf/article/view/3578) (open access). Gli stessi tre fault, con numeri ancora più bassi: F3 = 3,6%, F9 = 3,5%, F15 = 7,9% con deep autoencoder, e 5,6–7,6% con T² e SPE. Li classifica come **"controllable faults"**, cioè fault che i loop di controllo compensano: "none of these three methods can produce satisfactory results".

**F4 non è borderline: è dipendente dal metodo.** *FaultExplainer* (arXiv [2412.14492](https://arxiv.org/abs/2412.14492)) elenca come non rilevabili dalla propria PCA i fault 3, 4, 9 e 15. Ma la PHM 2023 **include F4 e lo rileva**: DAE e SPE raggiungono il 100%, mentre T² si ferma al 18%. La conclusione corretta non è che le fonti siano in disaccordo sull'appartenenza di F4 al gruppo difficile, ma che **la rilevabilità di F4 dipende fortemente dal metodo**: FaultExplainer lo esclude perché la *sua* PCA non lo vede, non perché il fault sia intrinsecamente invisibile.

Questo ha una conseguenza sul criterio, più importante del caso F4 in sé: **"non rilevabile da PCA" non è una proprietà del fault, è una proprietà di PCA.** Il criterio di stratificazione deve quindi usare solo i fault su cui **tutti** i metodi falliscono — F3, F9, F15, dove il fallimento è concorde e ha una spiegazione meccanica — e non quelli dove fallisce un metodo solo. F4 esce dallo strato difficile e torna candidato ordinario.

### 12.2 Perché questo cambia il criterio di selezione

La distinzione che conta non è "difficile" contro "facile", ma **perché** è difficile, e **se il fallimento è concorde tra i metodi**. Le fonti convergono su una spiegazione meccanica per F3, F9 e F15: l'anello di controllo assorbe la perturbazione, quindi il fault è quasi invisibile nelle XMEAS **per una proprietà del processo in closed loop**, non per un limite di un particolare rilevatore. Il caso F4 mostra il contrario: fallimento di un solo metodo, quindi nessuna proprietà del fault.

Ne discende la forma di criterio utilizzabile — **strutturale, esterno, preesistente e concorde**:

> Stratificare su "fault compensati dal controllo, con FDR sotto il 10% **in tutti i metodi confrontati** nella letteratura citata".

È difendibile perché non usa i propri dati e non dipende da un singolo rilevatore. Non lo sono: "nei nostri dati di sviluppo separano male" (usa i propri dati) e "PCA non lo rileva" (usa un solo metodo).

### 12.3 Avvertenza sulla trasferibilità

I numeri sopra sono **tassi di rilevazione** (Normal vs fault) ottenuti con metodi della famiglia PCA, non tassi di **diagnosi** nella rappresentazione verbalizzata 697-D. Non si può assumere che un fault con FDR del 5% in PCA sia altrettanto difficile per il verbalizzatore V2, né il contrario. Le fonti vanno quindi usate per **stratificare e dichiarare**, non per prevedere il risultato: la stratificazione è una scelta di disegno documentata, non un'ipotesi sul risultato atteso.

### 12.4 Uso raccomandato nel documento dei criteri

Il documento congelato deve citare soltanto:

- **Downs & Vogel 1993** per meccanismo e identità della variabile perturbata (verificabile, non interpretativo)
- **Yin et al. 2012** e la **PHM 2023** per la stratificazione di difficoltà, con i numeri sopra
- eventuali altri paper **solo se portano numeri specifici**

Tutto ciò che non ha una di queste due forme non è un criterio ed è un'impressione: fuori dal documento.

### 12.5 FaultExplainer come lavoro correlato — e come trappola di confronto

*FaultExplainer* (arXiv [2412.14492](https://arxiv.org/abs/2412.14492)) applica GPT-4o e o1-preview alla diagnosi di fault sul TEP. È il vicino più prossimo a questo lavoro e **va citato nella related work**: un reviewer che lo conosce e non lo vede citato ne trarrà una conclusione sfavorevole.

⚠️ **I suoi numeri non vanno riportati come accuratezze ordinarie.** Il 64% e l'82% corrispondono a 7/11 e 9/11, ma con tre qualificazioni che cambiano il significato:

1. sono risultati **top-3**, non top-1;
2. gli **alias sono accettati come corretti**;
3. il denominatore sono **soltanto i fault rilevati dalla loro PCA**, non i 20 del benchmark.

Un confronto diretto tra questi numeri e l'accuratezza top-1 su 9 classi di questo studio sarebbe scorretto **a proprio favore**, ed è il tipo di confronto che un reviewer informato smonta in una riga. Quando FaultExplainer compare nel testo, le tre qualificazioni vanno con esso; e se serve un confronto, va costruito sulla stessa metrica o dichiarato non comparabile.

---

### Parte seconda — prior art federato

### 12.6 I sei lavori, verificati

Verifica condotta sul testo integrale, non sugli abstract. Gli scarti fra ciò che gli abstract promettono e ciò che gli esperimenti dimostrano sono rilevanti per il posizionamento, quindi sono riportati.

| ID | Lavoro | Venue | Unità scambiata | Round | Scala | Serie temporali / fault |
| --- | --- | --- | --- | --- | --- | --- |
| **P042** | FICAL | preprint (arXiv 2412.08054) | knowledge compendium, 4 campi | one-shot | 5–8 client | nessuna |
| **P041** | Fed-ICL | **ICML 2025** | coppie (query, risposta), cap 256 token | 6 | 3 client | nessuna |
| **P031** | FedTextGrad | **ICLR 2025** | prompt in testo libero | non specificato | 3 client | nessuna |
| **P030** | FERA | preprint | tracce di ragionamento + incertezza | 6 | 3 client | nessuna |
| **P065** | SYNAPSE | preprint | compendium tipizzato, 5 componenti | 3 (30 in simulazione) | 5 client | nessuna |
| **P001** | ACE | **ICLR 2026** | playbook di bullet con ID e contatori | 5 iterazioni | mono-agente | nessuna |

**Nessuno dei sei tocca serie temporali multivariate, dati sensoriali o diagnosi di guasti.** Verificato per ricerca diretta su ciascun testo. P001 non è nemmeno federato: Generator, Reflector e Curator sono tre ruoli dello stesso modello, con un unico playbook che evolve nel tempo.

**Cautela sull'uso delle fonti.** P042 e P065 sono preprint non sottoposti a revisione e contengono incoerenze interne verificabili — P042 dichiara che le baseline trasmettono solo LoRA ma calcola il proprio guadagno di comunicazione sul modello pieno da 8B; P065 riporta la stessa configurazione con due valori diversi di tool-call accuracy (0,540 e 0,631) e cita un tasso di deduplicazione del 95,2% che non compare in nessuna sua tabella. **Vanno citati per priorità concettuale, non usati come evidenza numerica.** P041, P031 e P001 sono peer-reviewed e vanno trattati come prior art solido — con la riserva, per P041, che non pubblica una sola tabella di risultati.

### 12.7 Affermazioni che i sei lavori rendono non sostenibili

Elenco delle affermazioni che **questi sei lavori** rendono non difendibili. Ciascuna è occupata da almeno uno di essi, con la forza indicata. La colonna «forza» si riferisce alla solidità dell'occupazione **rispetto a questo corpus**, non a una rassegna esaustiva del campo.

| Affermazione non più sostenibile | Occupata da | Forza rispetto a questo corpus |
| --- | --- | --- |
| Scambiare linguaggio naturale invece di parametri in FL con LLM | P042, P041, P031, P030 | definitiva |
| Artefatto di conoscenza strutturato generato da LLM al posto dei dati grezzi | P042, P065, P001 | definitiva |
| Comunicazione O(1) rispetto alla dimensione del modello | P042, P041 | definitiva |
| Server che aggrega testo dei client in un artefatto globale ridistribuito | P042, P041, P031 | definitiva |
| Refinement testuale iterativo multi-round, con prova di convergenza | P041 (ICML 2025) | definitiva |
| Selezione top-k / kNN / MMR degli elementi da includere nel prompt | P041, P030 | idea occupata, evidenza debole |
| Pesatura per confidenza dei contributi dei client | P030 | idea occupata, evidenza debole |
| Item testuali con ID stabili e metadata di utilità; aggiornamento incrementale a delta | P001 (ICLR 2026) | definitiva |
| Merge tipizzato con risoluzione di conflitti campo per campo | P065 | definitiva |
| DP per-campo sui metadati numerici di un artefatto testuale | P065 | definitiva |
| Leggibilità di un artefatto testuale da parte di LLM eterogenei | P065 (lato consumer) | definitiva lato consumer |
| Client con domini o toolset disgiunti che collaborano via testo | P042, P031 | definitiva |
| RAG sopra la conoscenza aggregata per gestire l'overflow di contesto | P042 | definitiva |
| Privacy per costruzione condividendo testo derivato | P042, P041 | definitiva come *claim* |

**Conseguenza diretta sul paper.** Qualunque formulazione del tipo «primo lavoro a federare conoscenza testuale» o «trasferimento di conoscenza fra LLM senza condividere dati» va rimossa dall'abstract e dall'introduzione: sei lavori bastano a falsificarla con una citazione.

⚠️ **La direzione opposta non vale.** Che una rivendicazione sopravviva a questo corpus non significa che sia nuova rispetto al campo: sei lavori, scelti perché pertinenti, non sono una rassegna sistematica. Le affermazioni di assenza in §12.9 sono quindi formulate come «non osservato nei sei lavori esaminati» e vanno mantenute in quella forma. Per rivendicare una lacuna del campo servirebbe una ricerca bibliografica più ampia, che non è stata condotta e che resta un prerequisito della stesura dell'introduzione.

### 12.8 Che cosa NON conviene introdurre, e perché

Quattro componenti presenti nei paper esaminati **non vanno aggiunte**. La motivazione non è il costo: è che ciascuna entra in un territorio già occupato dove la soluzione nota non funziona, oppure introduce un confondente nel disegno attuale.

| Componente | Verdetto | Motivo verificato | Costo evitato |
| --- | --- | --- | --- |
| **Aggregazione esplicita lato server** | **non introdurre in questo studio** | **Non perché sia inapplicabile.** Contributi di client diversi possono essere aggregati anche con un fault per client; ciò che la configurazione class-disjoint indebolisce in modo specifico è FedProto (§9.1). Le ragioni per escluderla qui sono due, entrambe di scopo: (a) introdurrebbe una componente nuova da progettare e un fattore in più nel disegno, a ridosso della finestra di §7; (b) nell'unico lavoro esaminato che la studia in profondità i risultati non sono incoraggianti — P031 (ICLR 2025) riporta che la concatenazione ottiene risultati migliori della sintesi (0,90/0,69/0,94 contro 0,88/0,55/0,92), non scala oltre la finestra di contesto, e che il rimedio proposto rende +0,01–0,02 entro una deviazione standard, con la loro stessa analisi di surprisal che non riscontra il meccanismo invocato. **CF1/CF5 resta quindi aperta** (§5): l'esclusione è una scelta di scopo, non una risposta alla critica. | progettazione nuova, chiamate, un fattore in più nel disegno |
| **Selezione top-k degli insight** | **non introdurre ora** | Con 14 insight il prompt non è vicino ad alcun limite, e variare il numero di insight per ricevente cambierebbe una delle sei variabili che §2.4 ha già identificato come confondenti. P030 usa MMR e k ∈ {1,3,5} ma non pubblica un solo numero. **Contingenza, non componente:** diventa rilevante solo se le misure di token di §8.7 mostrano il prompt vicino al limite del modello. | ~1 fattore aggiuntivo nel disegno |
| **Round multipli** | **non introdurre in questo studio** | Tre lavori riportano guadagni che decadono e poi si invertono, ma **su grandezze diverse fra loro**: round di comunicazione federati (P030, plateau al round 2 e FERA-Q che peggiora nei round finali), step di ottimizzazione locale (P031, 0,83→0,81 / 0,86→0,83 / 0,84→0,80 da 5 a 10), iterazioni di riflessione di un singolo agente (P001, 67,6 → 65,2 da 5 a 10). Non sono la stessa quantità e nessuno dei tre pubblica il guadagno marginale per round. L'evidenza è quindi sufficiente a **non aprire questo fronte adesso**, dato che il costo è un multiplo dell'intero budget e la finestra di §7 è stretta; **non è sufficiente a concludere che round aggiuntivi sarebbero inutili in FoT**, dove compito, unità scambiata e struttura delle classi differiscono da tutti e tre. Resta una domanda aperta per future work (§5, G4). | 2–6× il budget di §8.8 |
| **Confidence weighting** | **non introdurre** | P030 lo rivendica ma non lo dimostra: si dichiara *calibration-free* e non misura mai la calibrazione, non pubblica alcun numero per l'ablation con e senza incertezza, passa i pesi al modello aggregatore **come prosa** anziché usarli aritmeticamente, e in uno dei suoi prompt dichiara che la risposta finale viene da un voto di maggioranza **non pesato**. Il suo teorema assume pesi indipendenti dal round e dà un ottimo (w ∝ 1/σ) diverso dalla regola implementata. Adottarlo senza calibrarlo significa ereditarne la debolezza; calibrarlo è uno studio a sé. Nell'output attuale di FoT non esiste inoltre alcun segnale di confidenza. | calibrazione, un braccio, un confondente |
| **Privacy differenziale** | **non introdurre** | Gli insight di FoT sono interamente testo. P065 ottiene (ε,0)-DP sui *soli campi numerici*, lascia il testo a mascheramento euristico, non usa secure aggregation negli esperimenti e non riporta mai il budget composto del proprio esperimento a 30 round. Una garanzia DP sul testo sarebbe vuota o sarebbe un altro progetto. G7 e CF4 restano limiti dichiarati. | un progetto di ricerca |

**Nota di metodo.** Ciascuna di queste esclusioni va **scritta nel paper come scelta motivata con citazione**, non lasciata come omissione. È la differenza fra un reviewer che annota «manca l'aggregazione» e un reviewer che legge «l'aggregazione non si applica a un compito class-disjoint, e dove si applica P031 documenta che non scala».

### 12.9 Dove la novità è difendibile

La domanda non è se il lavoro sia nuovo in generale — a quella domanda questo corpus non può rispondere — ma quali rivendicazioni **sopravvivano** a ciò che §12.7 esclude. Le quattro seguenti sopravvivono alla verifica sui sei lavori esaminati, e vanno formulate con quell'ambito dichiarato: non «nessuno ha fatto X», ma «X non è osservato nei sei lavori esaminati» — sei, di cui **cinque** federati: P001/ACE è mono-agente, come §12.6 già dichiara, e chiamarli tutti «federati» è un'imprecisione che un reviewer coglie.

1. **Diagnosi local-unseen su serie temporali multivariate.** Nessuno dei sei tocca il dominio: tutti operano su dati già testuali — query, risposte, descrizioni di API, prompt. Il problema di *costruire* un artefatto testuale a partire da una modalità numerica, e di verificare che la traduzione preservi informazione diagnostica, non è affrontato in questo corpus. ⚠️ **L'ambito va tenuto stretto al federato.** Fuori da questo corpus quel problema è affrontato: S2S-FDD (Li & Zhao, 2026) converte segnali industriali multivariati in descrizioni di trend, periodicità e deviazione da una baseline normale e diagnostica zero-shot senza alcun dato di guasto; T2SP e CGTime lavorano sul verbalizzatore, e §14.7 del walkthrough dichiara già che T2SP «blocca ogni novità sul verbalizzatore». La rivendicazione va quindi formulata come «in regime federato», mai «in generale».
2. **Spazio di etichette realmente disgiunto, con misura sulla classe mai vista localmente.** P041 e P030 partizionano con Dirichlet uno spazio di etichette **condiviso**: nessun client deve mai produrre una classe che non conosce. P042 ha toolset disgiunti ma non separa mai le prestazioni sui tool posseduti da quelle sui tool noti solo attraverso il compendio altrui. P031 assegna task diversi ai client ma riporta solo la media fra task, senza scomposizione per client. ⚠️ **P065 è il caso più vicino e va nominato** *(revisione 4)*: riporta un pavimento Local-Only — 0,46 su GSM8k, 0,191 su τ-bench retail — contro il federato, e attribuisce il divario al fatto che «∼54% of queries require scenarios unseen locally». È però un'accuratezza **globale** più una percentuale di copertura, non un'accuratezza stratificata su quel sottoinsieme, e non esiste uno spazio di etichette chiuso in cui la risposta corretta sia una classe mai osservata localmente. **La formulazione difendibile è quindi: nessuno dei sei misura l'accuratezza per-classe su una classe che il client non ha mai osservato, dentro uno spazio di etichette chiuso e disgiunto.** «Nessuno pubblica un numero» è troppo forte e cade su P065.
3. **Confronto controllato fra conoscenza corretta e conoscenza semanticamente errata.** **Non osservato nei sei lavori esaminati:** nessuno dei sei esegue un controllo con informazione permutata a parità di tutto il resto. P030 arriva al troncamento (sottocampionamento di step), che non è informazione errata. P001 è il più vicino con il *harmful reflector* di Tab. 17, ma è iniezione di contenuto dannoso generato da un modello, non una permutazione controllata. Due dei sei contengono inoltre confronti in cui la quantità di contesto varia insieme al contenuto senza essere isolata (P041, 5 esempi contro 1; P031, concatenazione contro sintesi): in quei confronti «più contesto» resta una spiegazione alternativa non esclusa, il che rende il controllo più utile, non meno. Con E ottenuta permutando soltanto la pseudolabel su uno schema congelato (§8.9), il controllo diventa verificabile e non solo dichiarato.
4. **Protezione dell'esperienza locale.** **Non osservato nei sei lavori esaminati:** nessuno dei sei riporta la degradazione sulle classi che il client già conosceva, né propone un meccanismo per proteggerla. ⚠️ Il calo di accuratezza **media** al crescere del numero di client che P042, P041 e P030 documentano **non è evidenza di degradazione sulle classi localmente note**: è un aggregato compatibile con molte cause diverse — maggiore eterogeneità, contesto più lungo, più distrattori, diluizione dell'attenzione — e nessuno dei tre lo scompone. Va citato, se citato, solo come indizio che la scalabilità in numero di client non è risolta, non come sostegno a C06. Il sostegno a C06 viene da un'altra fonte e da un'altra misura: i 19/24 contro 23/24 di §10.3 del walkthrough, che sono proprio una misura sui local-seen. C06 con local-first e l'endpoint congiunto di §8.5 restano quindi una domanda che i sei lavori non affrontano.

**Formulazione difendibile della novità**, da usare come base per abstract e introduzione:

> Diagnosi di guasti su serie temporali multivariate in un regime class-disjoint, dove ogni agente conosce una sola classe, con un confronto controllato fra conoscenza testuale corretta, conoscenza semanticamente errata e protezione dell'esperienza locale, su uno schema di insight congelato e misurato.

Ogni elemento di questa frase è verificato contro i sei lavori esaminati — il che è una condizione necessaria, non sufficiente: prima dell'abstract va fatta la ricerca bibliografica più ampia di cui a §12.7. Ciò che va comunque **tolto** dalla formulazione è tutto il resto: federare testo, trasferire conoscenza fra LLM, efficienza di comunicazione, struttura degli artefatti.

---

## 13 · Risposte alle 14 domande della review

**1. Il piano è scientificamente coerente?**
Nella struttura sì; nella versione originale era troppo complesso. Il piano consolidato di §8 — tre condizioni, R=1 gated, ponte e Q4 eliminati, producer-swap e OOD aggiunti — è coerente e realizzabile nella finestra temporale.

**2. Lo studio ponte distingue davvero producer e consumer?**
Parzialmente, e su dati di sviluppo. Distingue bene l'effetto consumer, debolmente quello producer, non identifica l'interazione. **Eliminato**, sostituito dal producer-swap su dati vergini (§8.4).

**3. Q4–Q8 è un confronto interpretabile?**
No, non causalmente: sei variabili cambiano insieme. **Eliminato.**

**4. Quali dati possono essere riutilizzati e quali devono essere nuovi?**
I 12+24 run dell'esplorativo restano risultati dell'esplorativo. I nuovi dati di sviluppo servono per soglie e insight. I run di test devono essere nuovi, generati e congelati prima di qualsiasi decisione di progettazione.

**5. Come impedire contaminazione o leakage?**
Generare i run di test, hasharli, non usarli per nessuna decisione. Congelare soglie, insight, prompt, condizioni, endpoint e δ prima dell'apertura. Seed di sviluppo e di test distinti e documentati. Ogni ispezione tecnica loggata.

**6. Quanti run indipendenti servono per fault?**
Minimo 6 (48 cluster); 8 (64 cluster) è ora realistico perché R=1 abbatte il costo per run.

**7. Tutti i 7 riceventi o un sottoinsieme?**
Tutti e 7. Costo lineare, potenza determinata dai cluster, scomposizione per agente gratuita.

**8. A+ deve essere completa, limitata o eliminata?**
**Eliminata**, anche come opzione. Già dimostrata nell'esplorativo.

**9. E deve restare completa?**
Sì, indispensabile, nella variante E-LF. Senza E il claim principale perde il supporto causale.

**10. Standard B e local-first devono essere entrambi valutati?**
No. **B-LF è il metodo** (§8.2). B senza local-first sopravvive come ablation su sottoinsieme meccanicamente dichiarato (§8.3), che non è un residuo ma la difesa del claim principale.

**11. R=1 o R=3?**
Gate tecnico dopo il pilot: nessuna divergenza osservata → R=1 con audit continuo. La soglia dell'1% è rimossa perché non dimostrabile con 120 osservazioni (§8.7). R=1 va presentato come **compromesso operativo, non come equivalenza statistica a R=3**: un pilot senza divergenze non dimostra determinismo, e gli intervalli sui cluster-run non stimano la variabilità delle risposte del modello alla stessa richiesta. Audit R=3 e set canary sono per questo indispensabili, non opzionali.

**12. Quali baseline sono indispensabili?**
Due, più due numeri di contorno — e nella revisione 3 il pavimento sale di priorità, perché è assente in P042, P030 e P031 e presente solo indirettamente in P041. La **baseline numerica a prototipi condivisi** resta indispensabile. La **baseline FL è ora decisa**: FedAvg minimale sulle stesse feature 697-D, con output condiviso sulle nove classi e otto client (§9). Non consuma chiamate API ed è avviabile subito. Accanto a FedAvg vanno riportati il **pavimento** (stessa rete addestrata da ogni client da solo) e il **soffitto centralizzato** (stessa rete sui dati aggregati): costano solo due esecuzioni dello stesso codice e sono ciò che impedisce l'accusa di baseline costruita per fallire (§9.3).

**13. Quali analisi escludere?**
Escludere dal disegno: studio ponte, Q4, A+, condizione C centralizzata, ablation delle rappresentazioni. Escludere dalle componenti suggerite dal prior art, con motivazione citabile (§12.8): **aggregazione lato server, selezione top-k, round multipli, confidence weighting, privacy differenziale**. Mantenere: A, B-LF, E-LF, baseline numerica, FedAvg con pavimento e soffitto, producer-swap con parità strutturale, test OOD, ablation local-first, schema congelato con metriche di conformità, set canary.

**14. Qual è il minimo studio finale pubblicabile?**
§8 di questo documento: Q8 con 8 agenti e 8 fault, tre condizioni A/B-LF/E-LF, astensione disponibile in tutte (D10), ≥6 run per fault, baseline numerica, FedAvg minimale con pavimento e soffitto, producer-swap con libreria completa, test fuori catalogo in tutte le condizioni, ablation local-first dichiarata, R=1 subordinato al gate, audit continuo e set canary. Circa 2.450 chiamate con 6 run (tetto 3.000) o ~3.040 con 8 run (tetto 3.500); la baseline FL non consuma chiamate.

Tre ipotesi statistiche in gerarchia (§8.5): B-LF > E-LF e B-LF > A sui local-unseen, B-LF non inferiore ad A sui local-seen. Tre domande scientifiche riformulate in §8.11 sulla base dei gap osservati nei sei lavori esaminati: la conoscenza di un pari permette di diagnosticare una classe mai osservata localmente? il guadagno dipende dalla correttezza dell'informazione o dalla sua sola presenza? la conoscenza ricevuta danneggia ciò che l'agente già sapeva, e a che prezzo la si può proteggere?

---

## Addendum — Analisi del dataset SWaT e confronto con TEP

**Prima stesura:** 11 settembre 2026
**Revisione 2:** riformulata dopo la correzione dell'autore sulla qualificazione di SWaT
**Documenti esaminati:** A Dataset to Support Research in the Design of Secure Water Treatment Systems (Goh et al., 2016), List of Attacks Final, SWaT Equipment List & Glossary, readme.txt, letteratura su SWaT in contesti FL e anomaly detection

### Conclusione, in una frase

**SWaT non è adatto come sostituto del TEP né come benchmark del presente studio finale. Resta possibile come futuro esperimento dedicato sulla diagnosi di attacchi cyber-fisici, con rappresentazione e protocollo propri.** Nel paper va definito **benchmark candidato per lavori futuri**, non "caso studio": non avremo risultati sperimentali su SWaT, e chiamarlo caso studio implicherebbe il contrario.

---

### A1 · Che cos'è SWaT

SWaT (Secure Water Treatment) è un impianto di trattamento acque reale in scala ridotta, costruito presso iTrust — Centre for Research in Cyber Security alla Singapore University of Technology and Design. Non è una simulazione: è un testbed fisico con 6 stadi di processo (P1 acqua grezza → P2 dosaggio chimico → P3 ultrafiltrazione → P4 declorazione → P5 osmosi inversa → P6 distribuzione), ciascuno controllato da un PLC indipendente connesso tramite rete industriale.

Il dataset copre 11 giorni continui: 7 di funzionamento normale e 4 con attacchi cyber-fisici (36–41 secondo la fonte; la lista ufficiale ne elenca 41, di cui 5 senza impatto fisico misurabile). 51 attributi campionati ogni secondo, circa 946.722 campioni.

**Tipi di attacco:** SSSP single stage single point (26), SSMP single stage multi point (4), MSSP multi stage single point (2), MSMP multi stage multi point (4), senza impatto fisico (5).

Gli attacchi sono manipolazioni di sensori (spoofing del valore letto dal PLC) o di attuatori (forzatura di pompe e valvole). Non sono guasti di processo nel senso classico, ma intrusioni informatiche che alterano il comportamento del sistema fisico.

---

### A2 · Confronto strutturale SWaT vs TEP

| Dimensione | TEP | SWaT |
| --- | --- | --- |
| **Natura** | Simulazione software (Downs & Vogel, 1993) | Impianto fisico reale in scala ridotta |
| **Tipo di processo** | Processo chimico continuo, singolo flusso integrato | Trattamento acque a 6 stadi, ogni stadio con il proprio PLC |
| **Variabili** | 41 XMEAS + 12 XMV = 53 | 51 attributi (sensori e attuatori mescolati) |
| **Campionamento** | tipicamente 3 minuti | 1 secondo |
| **Tipo di anomalie** | Guasti di processo: step, random variation, slow drift, sticking valve | Attacchi cyber-fisici: spoofing di sensori, forzatura di attuatori |
| **Numero di classi** | 21 guasti standard con meccanismo fisico noto | 36–41 attacchi, molti specifici a un componente, alcuni senza effetto misurabile |
| **Etichettatura** | Un guasto per run, etichetta di classe per run | Etichetta binaria Normal/Attack per timestamp |
| **Generazione dati** | **Illimitata:** run indipendenti con seed, durata e condizioni configurabili | **Fissa:** un solo recording di 11 giorni, nessun simulatore |
| **Replicabilità statistica** | Eccellente: 6, 12, 24 o più run per classe con semi indipendenti | **Nulla sui dati originali:** le "repliche" richiedono resampling, che non sono run fisici indipendenti |
| **Partizione naturale per FL** | **Assente:** la partizione in agenti è artificiale | **Presente:** 6 stadi con PLC indipendenti |
| **Accesso** | Simulatore open-source | Registrazione presso iTrust/SUTD; versione preprocessata su Kaggle |
| **Dimensione** | pochi MB per run | Normal ~130 MB, Attack ~116 MB (.xlsx) |

---

### A3 · Perché SWaT non può sostituire il TEP nel progetto FoT

L'incompatibilità è strutturale, non tecnica. Cinque ragioni, ciascuna sufficiente da sola.

**1 — Le anomalie sono di natura diversa.** FoT è progettato per la diagnosi di guasti di processo: un agente sa come appare F1 (step nella composizione dell'alimentazione) e condivide una descrizione testuale di quel pattern. SWaT contiene intrusioni: "qualcuno ha forzato la valvola MV-101", "qualcuno ha falsificato LIT-101". Non è fault diagnosis, è intrusion detection. FoT assume che ogni agente osservi un'anomalia con profilo fisico caratteristico e **ripetibile**; un attacco cyber-fisico ha un profilo che dipende dalla strategia dell'attaccante, non dalla fisica. Due attacchi sullo stesso sensore possono avere firme completamente diverse.

**2 — Il dataset è fisso, non generabile.** L'impianto statistico di FoT-TEP si fonda sulla generazione di run indipendenti: 6 per fault, ciascuno un cluster per il bootstrap. SWaT ha una sola registrazione. Qualunque tentativo di creare repliche via finestre temporali o bootstrap sui campioni viola l'indipendenza tra cluster e rende inapplicabile il protocollo inferenziale.

**3 — La struttura delle classi non è compatibile con il class-disjoint.** In FoT-TEP ogni agente conosce Normal + 1 fault. In SWaT gli attacchi non sono classi: sono eventi con inizio, fine e una manipolazione specifica. Alcuni durano 3 minuti, altri quasi 10 ore (attacco 28). Alcuni non hanno effetto misurabile. Trasformarli in classi richiede scelte arbitrarie — per componente? per stadio? per tipo di manipolazione? — e nessuna tassonomia è canonica.

**4 — L'etichettatura è binaria, non multiclasse.** Servirebbe una pre-elaborazione non banale con scelte soggettive di raggruppamento, e il risultato avrebbe classi di dimensione estremamente diseguale (da ~200 a ~36.000 campioni) senza possibilità di bilanciare con nuovi run.

**5 — Il verbalizzatore non è trasferibile.** V2 è costruito sulle 41 feature XMEAS con 17 bande statistiche ciascuna, per un vettore 697-D. Adattarlo richiederebbe selezionare feature tra 51 attributi eterogenei, definire nuove bande e calibrare nuove soglie: progettazione, non adattamento parametrico. E i 25 attuatori binari on/off non si prestano alla verbalizzazione con soglie statistiche.

---

### A4 · SWaT come comparatore: gli scenari valutati

**Scenario A — secondo dataset nello studio finale.** Richiederebbe un verbalizzatore specifico, una tassonomia di classi, un protocollo class-disjoint compatibile con un dataset fisso e una soluzione al problema dei run non indipendenti. È un progetto di ricerca a sé stante. **Non fattibile nel tempo disponibile.**

**Scenario B — test di trasferibilità cross-dominio.** Presentare un insight prodotto sul TEP a un agente che opera su SWaT. Non è un test significativo: i processi sono incomparabili, le variabili non hanno corrispondenza, e un insight come "la variabile X mostra un incremento graduale oltre soglia" non ha traduzione tra i domini. Un risultato negativo sarebbe scontato, uno positivo un artefatto. **Non informativo.**

**Scenario C — menzione nel paper.** L'unico uso sostenibile, con la formulazione corretta: SWaT è un **benchmark candidato per lavori futuri**. L'applicazione di FoT richiederebbe una rappresentazione propria e un protocollo adattato al dataset fisso; il dominio — diagnosi di attacchi cyber-fisici — è diverso da quello di questo lavoro e merita uno studio dedicato.

**Scenario D — argomento sulla partizione naturale.** I 6 stadi con PLC indipendenti sono un caso reale in cui i nodi federati esistono per ragioni architetturali e non per scelta sperimentale. L'osservazione è legittima, con due vincoli: va **in Discussion e non in Introduction**, ed è un'osservazione su SWaT, non un supporto ai nostri risultati. In Introduction diventerebbe motivazione della validità del metodo tramite le proprietà di un impianto su cui non abbiamo misurato nulla.

---

### A5 · Che cosa scaricare, se si vuole ispezionare il dataset

Due file:

1. **SWaT_Dataset_Normal_v1.xlsx** (~130 MB) — 7 giorni di normale, versione 1 senza i primi 30 minuti di drenaggio. Baseline per i range delle 51 variabili.
2. **SWaT_Dataset_Attack_v0.xlsx** (~116 MB) — 4 giorni con attacchi ed etichette Normal/Attack per timestamp.

Canali: portale [iTrust Datasets](https://www.sutd.edu.sg/itrust/itrust-labs/datasets/) con registrazione e breve motivazione di ricerca (raccomandato per la citazione accademica), oppure una versione preprocessata su [Kaggle](https://www.kaggle.com/datasets/vishala28/swat-dataset-secure-water-treatment-system/data), più accessibile ma meno controllata sulle versioni.

⚠️ Oltre 100 MB ciascuno in .xlsx: convertire in CSV o caricare con `pd.read_excel()` invece di aprirli in Excel.

**Nota sulla priorità:** dato il vincolo temporale di §7, l'ispezione di SWaT non è sul cammino critico. Ha senso solo se l'obiettivo è preparare il futuro studio dedicato, non il paper di settembre.

---

### A6 · Vantaggi che SWaT avrebbe portato

Vale registrarli, perché inquadrano ciò che il TEP non fornisce e motivano il futuro studio dedicato:

1. **Partizione naturale per FL:** 6 stadi fisicamente separati con controllori indipendenti. Nessuna partizione da inventare. È la ragione per cui SWaT è usato nella letteratura FL per ICS.
2. **Dati reali:** rumore, non-linearità e interazioni di un processo fisico, non di un simulatore.
3. **Alta frequenza:** 1 secondo contro 3 minuti.
4. **Interazioni cross-stadio:** gli attacchi MSMP propagano effetti su più stadi, creando pattern distribuiti che un singolo nodo non può diagnosticare. È esattamente lo scenario in cui la federazione ha valore aggiunto reale.
5. **Rilevanza per la cybersecurity industriale:** è uno dei benchmark più citati nell'anomaly detection per ICS/SCADA.

Questi vantaggi sono reali ma **annullati dall'incompatibilità strutturale di A3** per il progetto attuale. Sono la ragione per cui vale la pena tornarci con un protocollo proprio, non per cui vale la pena forzarlo adesso.

---

### A7 · Sintesi

| Domanda | Risposta |
| --- | --- |
| **SWaT può sostituire TEP nel progetto FoT?** | **No.** Cinque incompatibilità strutturali: natura delle anomalie, dataset fisso, classi non standard, etichette binarie, verbalizzatore non trasferibile. |
| **SWaT può essere il benchmark del presente studio finale?** | **No**, per le stesse ragioni. Lo studio finale resta su TEP come unico benchmark. |
| **SWaT ha vantaggi rispetto a TEP?** | Sì: partizione naturale per FL, dati reali, alta frequenza, interazioni cross-stadio. Sfruttabili solo con rappresentazione e protocollo propri. |
| **Come va qualificato nel paper?** | **Benchmark candidato per lavori futuri**, in Discussion. Non "caso studio": non avremo risultati sperimentali su SWaT. |
| **Che cosa sarebbe il futuro esperimento?** | Uno studio dedicato sulla diagnosi di attacchi cyber-fisici, con verbalizzatore specifico per attuatori binari e variabili continue, tassonomia di classi dichiarata, e un protocollo inferenziale che non assuma run indipendenti. |
| **Quale file scaricare, se serve?** | `SWaT_Dataset_Normal_v1.xlsx` (~130 MB) e `SWaT_Dataset_Attack_v0.xlsx` (~116 MB), da iTrust/SUTD o Kaggle. Non è sul cammino critico di settembre. |

**Raccomandazione finale:** SWaT non entra nel piano sperimentale attuale. Nel paper è menzionato in Discussion come benchmark candidato per lavori futuri e come esempio di dominio con partizione naturale per la federazione. Costa zero esperimenti e zero tempo, e rafforza il paper mostrando consapevolezza dei benchmark rilevanti — a condizione di non attribuirgli un ruolo sperimentale che non ha.
