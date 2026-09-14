NON OK

# Verifica indipendente completa — sotto-fase 03.5, incluso l’addendum

**Candidato:** `819b12e97fb94d501032655ec2f226139e6c5ca5`, branch di provenienza `codex/studio2-soglie-normal`. Verifica del pacchetto complessivo, non soltanto delle 24 righe dell’addendum.

**Finestra:** task `01a09f81-e508-77e0-b510-872bdeba46e3`, aperta il 2026-09-14 alle 10:41:25 UTC. **Modello effettivo: `gpt-6-astra`**, riscontrato nel `turn_context` locale. Worktree detached: `/Users/luker/fot-tep-verifica-soglie-normal`.

**Indipendenza documentata:** la sessione esecutrice `01a09b8c-822a-70a3-a5e0-246d9c8bf840` registra **`gpt-5.6-luna`** nei contesti dei turni di specifica/implementazione, correzione R2, analisi e addendum. Le esecuzioni di commit sono riconducibili agli stessi turni: specifica alla riga 80 del rollout, freeze alla 707, analisi definitiva alla 807, addendum alla 991; contesti modello alle righe 6, 360, 527 e 955. Non è stata usata la sola etichetta “Codex” per identificarlo. La richiesta dell’autore di ricevere il comando da eseguire localmente precede il batch; il launcher è uno script MATLAB, non un’inferenza LLM. Il suo avvio umano è sostenuto dalla conversazione, non certificato da una registrazione indipendente del terminale umano.

Fonte dei metadati: `/Users/luker/.codex/archived_sessions/rollout-2026-09-13T18-14-32-01a09b8c-822a-70a3-a5e0-246d9c8bf840.jsonl`, SHA-256 `3f21bd048089023c500f2393acaa237e328a59c6adc78987e5d582dadcf16e47`. Estratti verificabili in `executor_evidence.json` nella directory di supporto. Sono metadati locali, non un’attestazione crittografica del fornitore sul backend del modello.

**Supporto esterno:** `/Users/luker/verifica-soglie-normal-support-WE8Qqc`. Qui sono conservati script, ambiente, archivio riscaricato, estrazione, piani rigenerati, campione, confronti per finestra, cronologia e log. L’indice delle impronte è `SUPPORT_SHA256.csv`; la sua impronta è riportata in fondo. È una directory di supporto alla verifica, non una modifica agli artefatti candidati.

## Ambiente, fonti e criterio

Ricalcoli con Python **3.11.5**, Clang 13.0.0, piattaforma rilevata **macOS 26.6.2, x86_64**, NumPy **2.4.6**, SciPy **1.17.1**, pandas **3.0.5**, openpyxl **3.1.5**. Interprete: `/Users/luker/verifica-soglie-normal-support-WE8Qqc/venv/bin/python`. Il Python di sistema non disponeva di NumPy; il runtime incluso nell’app non disponeva di SciPy. Le dipendenze sono state installate esclusivamente nel venv esterno; versioni complete in `environment.txt` e `requirements.txt`. L’esecuzione scientifica originale risulta MATLAB R2025b ARM; questa verifica non ha avviato MATLAB né simulazioni.

Lette le istruzioni della copia principale prima delle modifiche: `docs/MAINTENANCE.md`, `docs/prompts/Prompt_LLM.md`, `docs/prompts/Verifica_LLM.md`; il mandato locale `verifica_3_5_prompt.md` è un file non tracciato della copia principale, non un artefatto del candidato. Sono state applicate anche tutte le precisazioni dell’allegato dell’autore.

Fonti scientifiche lette direttamente nel candidato: registro `docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md` **rev. 19**, in particolare requisiti iniziali, P0, C0–C4 e continuità/pareggi; piano §6.2–6.3; specifica, handoff, report, codice e test di `soglie_normal`; `LOT_AUDIT.json`, `R2_GUARD_RECHECK.json`, `CAL_THR_SCORES.csv`, `THRESHOLD_FREEZE.json`, `FAR_VERIFICATION.json/.md`, `ARTIFACT_STORAGE.json`, `MANIFEST_CONSERVAZIONE.csv`; `PROVENIENZA.md` §§1–4 e 9, freeze e moduli numerici di Fase 02, risultati R2 e manifest eseguiti. Per il requisito di report è stato letto `docs/prompts/Fase_LLM.md`. Non è stata usata la replica HTML come seconda fonte. Letture mirate complessive: ordine di grandezza 35–50 mila token, esclusi dati elaborati dagli script e output troncati; non è una misura di fatturazione.

Il registro prevale sul piano e sul prompt. Due interpretazioni suggerite nel mandato originario non sono state recepite: la secondaria **stima la stessa quantità della garanzia**, ossia il FAR della miscela; la generazione anticipata non va automaticamente assolta né dichiarata contraria a un divieto di generazione che l’handoff non contiene.

Legenda: ✅ riscontro diretto; ⚠️ limite od omissione; ❌ affermazione smentita o requisito non soddisfatto. I rilievi numerici, documentali e di processo sono distinti sotto. Il verdetto non attribuisce errori agli score che i ricalcoli hanno invece confermato.

## 1. Perimetro e basi effettive

✅ La base immediata della specifica è **`53a3e9299ff7548fde30c54014a340d7113bf882`**, non `b7f359f`: `8ec3c38^ = 53a3e92`. Il confronto integrale `b7f359f..819b12e` comprende anche `53a3e92`, dedicato alla **03.4, perimetro Q8**; i suoi file in `perimetro_q8` sono attribuiti a quel commit, senza esclusioni di percorso. `b7f359f` è a sua volta il precedente intervento bibliografico su Downs & Vogel, catalogo D1 e IDV(14)–(20), successivo ai lavori sui fault di sviluppo. Non è un commit della 03.5.

✅ Il delta effettivo **`53a3e92..819b12e`** contiene soltanto `studio2/fase03/soglie_normal/` e l’aggiunta di §9 a `studio2/PROVENIENZA.md`. Nessuna modifica di `phase_b/`, `code/`, dati del primo studio, Fase 02 o walkthrough. I workbook della sotto-fase non sono tracciati in Git. I confronti completi sono `scope_actual.txt`, `scope_declared.txt` e `commits_all.txt`.

✅ **`819b12e` modifica soltanto `REPORT_SOGLIE_NORMAL.md`: 24 righe aggiunte.** Nessuna variazione di score, soglia, piano o freeze nell’addendum.

⚠️ La dicitura “Base: b7f359f (origin/main)” della specifica è un riferimento di contesto incompleto per il delta effettivo; è stata riconciliata con la storia, non adottata come filtro.

## 2. Specifica, piani, posizioni e stream

✅ La specifica è introdotta da `8ec3c38`, il **13 settembre 16:16:42 UTC**. Piani/script finali: `6c128c4`; smoke/handoff: `4fb1620`; correzione impronta R2: `d09e7ed`, tutti prima del batch. Le modifiche successive della specifica riguardano contabilità, proiezione e misura smoke: non spostano distribuzione di J, finestre, score o regola della soglia. La specifica iniziale precede gli smoke; la revisione con le misure smoke precede i 500 run scientifici. Non si pretende che la misura dello smoke fosse nota prima dello smoke.

✅ Rigenerazione in directory esterna tramite le funzioni **non modificate** `build_rows` e `validate_rows`, con la stessa serializzazione CSV. La CLI rifiuta output esterni a `plans/`: per evitare sovrascritture si è importato il modulo. Confronto byte per byte su tutti e quattro i piani, non soltanto confronto delle righe:

| Piano | Righe | SHA-256 rigenerato = candidato |
|---|---:|---|
| cal_thr | 350 | `fae355fdfd6db17b25e55c72f174ee8c7bb9c8b298facfb9a8012908f921a3ad` |
| far_ver | 150 | `084dcabf03cc34c6a23002a956d579864c6e1086ca18bbc3b44ef96d218c10a5` |
| smoke_cal_thr | 1 | `c34a2cf4352bfec5d7604cfd3f0c0580aa25202a164dc14da10124f7e751d577` |
| smoke_far_ver | 1 | `574f3544a5ce641bedcdcd24eae9278e662e7719fe113c31f93b14e05bcc4d21` |

✅ Ricontrollati chiave `0x464f545445503032`, input del digest `KEY|namespace|ordinal|stream`, namespace distinti `fot-tep/fase03/soglie_normal/cal_thr/j/v1` e `fot-tep/fase03/soglie_normal/far_ver/position/v1`, derivazione da SHA-256 e posizione. Frequenze J di calibrazione: **30,29,31,30,37,38,44,38,34,39**, somma J **2022**. Frequenze delle posizioni primarie FAR: **15,14,20,13,13,14,13,19,13,16**. Distribuzione uniforme è l’assunzione progettuale dell’estrazione pseudocasuale, non l’uguaglianza delle frequenze osservate; la riduzione modulo 10 dei 64 bit ha uno sbilanciamento teorico inferiore a `10⁻¹⁹`, trascurabile ma non è uniformità matematica esatta.

✅ Stream **40000–40349**, **50000–50149**, **49900–49901**, tutti distinti. Disgiunzione verificata rispetto all’intero `STREAM_RANGES` di Fase 02: 0–9, 100–109, 200–209, 1000–1009, 2000–2099, 10000–10349, 20000–20149; inoltre fault 30000–30039. Inventario aggiuntivo di **21 CSV** con stream fuori dalla 03.5, inclusi smoke pertinenti: zero collisioni (`traces_result.json`). Riusi dello stesso stream all’interno delle qualificazioni/prefix replay non sono nuovi run di calibrazione.

✅ I 500 manifest riscaricati concordano con i piani per ID, stream, stop, burn-in e posizione. Philox4x32-10, chiave, MEX, modello, `Ts_base=0.0005 h`, uscita 1 minuto, contatore iniziale zero/finale positivo e durata completa coincidono con il freeze. Calibrazione **17.110 h**, FAR **10.500 h**, totale **27.610 h**. Zero run incompleti/trip. Il log contiene 500 warning di espansione del buffer Variable Time Delay, ma nessuna riga di errore/trip e le due conclusioni “Generated 350 runs” / “Generated 150 runs”; warning non significa fallimento tecnico.

⚠️ Errore documentale minore nella specifica, «35.000 h piene per cal_thr»: 350×70 sono **24.500 h**; 35.000 è il totale di 500 run pieni. I piani e il totale economico effettivo sono corretti.

## 3. Freeze, ricerca pregressa e deviazione di processo

✅ Cronologia ricostruita da Git e dai log, orari UTC:

| Evento | Commit / prova | Data e ora |
|---|---|---|
| Specifica | `8ec3c386be93ee556c93677f0b58cbfd5b8bbaf0` | 13-09 16:16:42 |
| Guardia corretta | `d09e7ed189b4a068f6c094a34c6ad60937d13eb7` | 13-09 16:34:31 |
| Generazione cal_thr | manifest scaricato | 13-09 16:38:19–17:19:15 |
| Generazione far_ver | manifest scaricato | 13-09 17:19:17–17:42:24 |
| Audit | `2d9c44561d0330a3e83e817f3f6ea9f51409c0ed` | 13-09 18:25:14 |
| Score cal_thr | `0127ef4df99b0e0b0c8dc64a1edaa5dda726b248` | 13-09 18:27:47 |
| Freeze + sigillo | `950714389f92e559eac922a09404742a71c74346` | 13-09 18:28:19 |
| Analisi FAR definitiva | `0b2aac5db03d877d47e26a2d734b2fab4577bafb` | 13-09 18:34:53 |
| Manifest / pubblicazione | `264a20e` / `0802c31` | 13-09 18:35:37 / 18:40:05 |
| Report / addendum | `582e575` / `819b12e` | 13-09 18:40:45 / 14-09 08:53:32 |

`frozen_at_utc=2026-09-13T18:28:19.798728+00:00`, con `source_head_commit=0127ef4…`. Le date dei manifest sono prodotte da `datetime(...,'TimeZone','UTC')` nel launcher qualificato, anche se il CSV non aggiunge un suffisso Z.

✅ L’unico commit che introduce/modifica `THRESHOLD_FREEZE.json` nella storia accessibile è `9507143`. SHA-256 **`ff5c27002a2548003e4bc5f54805cda3754fb19b9cb2559222996b9c7f7e14a9`**, identico in tutti i discendenti del candidato e nella release; coincide con il riferimento in FAR. Tutte le nove impronte di `sources` coincidono con gli input.

✅ La ricerca `git log --all --diff-filter=A -- '*far_ver*score*'` è vuota, ma è stata ampliata: storia completa di `soglie_normal`, ispezione di `0127ef4` (solo script/CSV cal_thr), ricerca pre-freeze indipendente dal percorso con `-G 'window_scores|far_primary|far_secondary'`. Gli unici due risultati di quest’ultima sono **primo studio**, `145b6b7` e `7e32ea5`, non score far_ver della 03.5. Conservati i risultati anche vuoti. Nella storia del candidato l’analisi e i 1500 score FAR compaiono in `0b2aac5`.

✅/⚠️ Cercate anche le tracce locali: **33 chiamate pertinenti** pre-freeze nei rollout accessibili, inventario di file temporanei, log originali e directory scientifica. I riscontri riguardano preparazione, manifest/hash e smoke separati, poi audit cal_thr. Gli score `smoke_far_ver`, stream 49901, esistono prima del freeze: sono qualificazione esplicitamente separata, **non** il lotto far_ver 50000–50149. Non è corretto dichiarare assenza di qualsiasi score con il nome far_ver. La prima invocazione registrata di `analyze_far_ver.py` è dopo il freeze (18:29:02, fallita per SciPy assente); seguono una versione errata del conteggio secondario (18:32:01, valore >1) e la correzione del conteggio (18:34:43) prima del commit definitivo. Si tratta di una correzione software osservabile, non di un cambiamento della soglia. I ricalcoli attuali verificano la versione definitiva.

**Limite della prova:** assenza nella storia Git, nei file rimasti e nei log accessibili non prova assenza di letture umane, accessi da altri processi, file cancellati o storia non disponibile. `LOT_AUDIT.json` dichiara mancata apertura, ma campi come `far_ver_scores_present=false` sono scritti dal codice, non prodotti da un controllo del sistema operativo. Gli hash dei workbook provano identità dei byte, non mancata consultazione. Il codice dell’audit esaminato legge i byte FAR per SHA-256 senza decodificare le celle; `load_case` è nel ramo cal_thr.

❌ **D3, documentale/processo, gravità media.** L’addendum afferma che la generazione anticipata «non rispetta l’ordine scientifico previsto dall’handoff». L’handoff invece descrive esplicitamente entrambi i piani **in un solo processo MATLAB**, e impone «Prima di aprire qualsiasi finestra far_ver» il freeze. Il registro, requisiti iniziali, prescrive **«Dopo la calibrazione e prima della verifica»** il congelamento; C3 colloca selezione/fit prima dell’accesso alla verifica. Non contiene un divieto esplicito di simulare e conservare i file far_ver prima del freeze. La specifica separa gli usi ma non aggiunge quel divieto. Anche il report originario diceva «come previsto dall’handoff», creando una contraddizione interna con l’addendum.

La sequenza **generazione/conservazione → freeze → apertura analitica registrata** è documentata. La formulazione più forte «nessuno li ha letti» non è dimostrabile. La generazione anticipata ha reso materialmente possibile una consultazione: è un limite di segregazione operativa da dichiarare, non una prova automatica di contaminazione. Non si assolve né si invalida il FAR per il solo timestamp di generazione. La decisione finale di accettare tale livello di tracciabilità spetta all’autore; questo verbale non sostituisce quella decisione.

## 4. Guardia R2 e integrità di Fase 02

✅ `recheck_r2_guard.py` rieseguito con il solo percorso di output rediretto all’esterno. Tutte le cinque impronte coincidono e sono SHA-256 completi. Risultato identico tranne **`checked_at_utc` 2026-09-13 → 2026-09-14**. Controllata anche l’identità **dei byte** dei due risultati Fase 02: il codice originario confronta oggetti JSON, che da solo non garantirebbe identità byte per byte.

✅ Ricalcolo ulteriore della guardia dai **10 workbook pilot** conservati nella copia principale, confrontati con le impronte del manifest qualificato, e N1–N5 all’impronta congelata. Usati i parametri già congelati, senza fit su cal_thr/far_ver. Tutte le cinque famiglie passano; differenza numerica massima rispetto a `r2_guard_result_v2.json`: **`5.440092820663267e-15`**. Per S: scarto di mediana **0,38988948329843953 MAD**, rapporto MAD **0,956200160288558**. Ramo attivo **U1/R2, 350+150**; fallback 100+300+150 non attivato. Dati R2 letti da copia locale verificata, non riscaricati in questa verifica; il riscaricamento richiesto riguarda la release Normal.

✅ `PRECALIBRATION_FREEZE.json` è byte-identico al commit **`d2e8092`**, SHA-256 **`be01fe4cccf6e9f3c9d82e8de69e426aa68b80d3e106bac81fa29dfb325bf085`**. Tutti i **41 file** elencati coincidono con dimensione/hash nella revisione `d2e8092`. Nel candidato i moduli e parametri scientifici sono ancora identici. Le sole differenze rispetto ai contenuti storici elencati sono piano narrativo e `PROVENIENZA.md`, evoluti nelle successive sotto-fasi: non sono una mutazione del freeze o dello score. La loro storia è conservata in `phase02_frozen_input_changes.txt`.

| Input effettivamente caricato nel ricalcolo | SHA-256 |
|---|---|
| score_fit_legacy.json | `e679caf45bf1ec1c923b8ef50b36fef5bcb350e17cf3296e00c748ec9fdef477` |
| combined_score.py | `6d083820789c888c393864b40c19205920029eac3113e36133e78d53c98cac48` |
| tep_features.py | `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c` |
| validate_numerics.py | `f17066ebd6a7523eddf350589a44ac2cf85a90c95ef0e3076a1bb492b9f27efe` |
| r2_guard_result_v2.json | `3b7131400747cd7b13a6ad02841fbdb84c85952297e090bd7b99678f03f2ee82` |

## 5. Campionamento cieco agli score e ricalcolo indipendente

✅ **Regola e ID registrati alle 10:43:25 UTC**, prima dell’apertura dei CSV/JSON contenenti gli score scientifici nella verifica. Sono stati letti soltanto i piani per scegliere il campione: ordinare, in ciascuno strato J/posizione, per SHA-256 di `independent-819b12e-v1|run_id`; prendere 4 cal_thr per J=1–5 e 3 per J=6–10; 2 far_ver per posizione primaria 1–5 e 1 per 6–10. Nessuna sostituzione dopo il confronto. I valori aggregati attesi erano già nel mandato, ma non sono stati usati nella selezione. `sample_preregistration.json` SHA-256 **`8bbacb0daab7c9edf47fa6170c8ef809613b1cc76ac9acd9a6ba6a685b748c6d`**.

| J / posizione primaria | cal_thr, suffissi degli ID | far_ver, suffissi degli ID |
|---:|---|---|
| 1 | 347, 201, 235, 225 | 137, 109 |
| 2 | 243, 042, 004, 293 | 071, 030 |
| 3 | 061, 326, 155, 196 | 042, 081 |
| 4 | 069, 154, 072, 165 | 002, 074 |
| 5 | 081, 272, 255, 277 | 082, 064 |
| 6 | 148, 318, 302 | 150 |
| 7 | 119, 158, 271 | 009 |
| 8 | 089, 031, 043 | 044 |
| 9 | 132, 146, 322 | 037 |
| 10 | 133, 073, 310 | 083 |

Prefissi completi: `cal_thr-` e `far_ver-`. Per **ognuno** dei 15 FAR sono state ricalcolate tutte le dieci finestre, indipendentemente dalla posizione primaria.

✅ Il ricalcolo carica `BaselineStats` e `RobustParameters` direttamente dai 164 riferimenti e dagli otto parametri di `score_fit_legacy.json`, variante A; applica i moduli qualificati `analyze_window` e `score_feature_table`. Non richiama gli script produttori di Fase 03 per ottenere gli score, non rifitta né adatta la funzione sui dati osservati. Workbook letti dall’archivio appena riscaricato. Controllati valori finiti, passo 1 minuto, 300 righe per finestra half-open, estremi `[20+5(pos−1),20+5pos)`, J finestre disponibili e **ultima finestra J** per cal_thr.

| Controllo | Run | Finestre ricalcolate | Errore assoluto massimo | Tolleranza |
|---|---:|---:|---:|---:|
| Calibrazione | 35 | 35 | `3.552713678800501e-15` | `1e-8` |
| FAR | 15 | 150 | `5.329070518200751e-15` | `1e-8` |

Tutti passano. `score_checks.json` conserva per ciascuna finestra ID, posizione, estremi, righe, SHA-256 workbook, score originale, ricalcolato e scarto. Hash di tutti i file in `archive_files.json`. Il ricalcolo numerico, inclusa R2, ha impiegato circa **55,01 secondi**. Nessuna chiamata di tool per singolo file. Il campione non equivale al ricalcolo integrale dei restanti workbook: questi sono verificati per identità e metadati, come previsto dal mandato.

## 6. Soglia, regola stretta e pareggi

✅ Verificati tutti i 350 valori del CSV, ID univoci, finitezza, corrispondenza J/stream con il piano. Con `n=350`, `alpha=0.05`, **`ceil(351×0.95)=334`**. Il 334° score ordinato è **`13.623626738268857`**, scarto dal freeze **zero**. La regola del codice è **`S > threshold`**. Nel campione di calibrazione 333 valori sono inferiori, uno uguale e 16 superiori.

✅ **350 valori distinti, zero gruppi duplicati, zero duplicati eccedenti; molteplicità alla soglia = 1.** Il campo `score_ties_at_threshold=1` conta quell’unica osservazione, non una coppia di punteggi uguali. L’assenza di pareggi osservati non dimostra la continuità della distribuzione di S. La legge **Beta(17,334)** richiede l’ipotesi di continuità e le ipotesi IID pertinenti, condizionatamente alla funzione di score fissata; non viene certificata dalla sola diagnostica.

⚠️ **D2, documentale/completezza, gravità media:** `freeze_threshold.py` conta soltanto le occorrenze del valore soglia. Il pacchetto non riporta la diagnostica di tutti i pareggi richiesta dal registro §“Formulazione corretta della garanzia”. Il controllo completo è ora nel supporto di verifica, ma non rende retroattivamente completa la rendicontazione del candidato.

❌ **D2, requisito C4 non soddisfatto:** accanto alla soglia il registro prescrive intervallo Beta del FAR condizionale, qualificato dalle ipotesi, e **bootstrap sui run della soglia stessa**, oltre al FAR su nuovi run. Il pacchetto fornisce il bootstrap del FAR secondario, che non è il bootstrap della soglia, e non fornisce quelle due componenti. Il registro riporta come riferimento Beta90% circa [3,12%;6,86%]; il ricalcolo dà **[3,118163613%;6,860631796%]**, media **4,843304843%**, SD **1,144245586 punti percentuali**. È variabilità teorica del FAR fra realizzazioni della calibrazione, non l’IC Clopper–Pearson della soglia realizzata. Non è stato prodotto un nuovo bootstrap della soglia per colmare il report: qui si verifica e si segnala l’omissione, senza correggere o ricalibrare il candidato.

## 7. FAR, incertezza e controllo dell’addendum

✅ Ricostruzione dai **1500 score memorizzati** e dal piano, con riconciliazione di tutti gli ID, stream, posizione e score primario, non sommando soltanto i booleani già riportati:

| Quantità | Ricalcolo | Scarto dagli artefatti |
|---|---|---|
| Primario | **11/150 = 0,0733333333333333 = 7,333333333%** | zero conteggi |
| CP 95% | **[0,03717461478190552; 0,12742416212603871]**, cioè **[3,717461478%;12,742416213%]** | estremi `+4.025e-16`, `−1.027e-15` in proporzione |
| Secondario | **108/1500 = 0,072 = 7,2%** | zero conteggi; rappresentazione JSON 0,07200000000000001 |
| Bootstrap per run | seed **20260913**, **10.000** repliche | stessi seed/repliche |
| SE secondario | **0,007512512137130144** in proporzione = **0,751251214 punti percentuali** | zero |
| IC percentile 95% | **[0,05733333333333334;0,08733333333333333]**, cioè **[5,733333333%;8,733333333%]** | zero |
| Superamenti per posizione 1–10 | **14,10,12,6,14,8,11,13,10,10**, somma 108 | zero |

Il CP è stato calcolato con SciPy `beta.ppf`, indipendentemente dall’approssimazione beta incompleta implementata in Fase 03. Il bootstrap campiona **150 indici di run** con rimpiazzo, mantenendo insieme le dieci finestre per ogni indice. SE con `ddof=1`; percentili 2,5 e 97,5. Non si trattano le 1500 finestre come IID. Nel report “SE 0,751%” è una notazione ambigua: l’unità esplicita corretta è **punti percentuali**.

❌ **D1, errore numerico nell’interpretazione dell’addendum, gravità media:** per `X~Binomiale(150,p)`, la probabilità esatta ricalcolata di `3≤X≤12` è:

| Parametro p | Probabilità |
|---|---:|
| `17/351 = 0,04843304843304843` | **0,9470465065943391** |
| `0,0484`, arrotondamento testuale del registro | **0,9471050101548655** |
| `0,05`, parametro citato nell’addendum | **0,9433302578164797** |

Lo 0,947 del registro è corretto per il suo parametro; associarlo al 5% è falso. Lo scarto tra la probabilità a `17/351` e quella al 5% è circa **0,003716249**, ossia **0,371625 punti percentuali di probabilità**. Non cambia il fatto aritmetico che 11 sia tra 3 e 12, ma richiede correzione dell’attribuzione.

⚠️ **D1, omissione interpretativa:** l’addendum non esplicita `17/351`, non segnala che l’IC secondario **esclude 4,8433%** (ed esclude anche 5%), e non sviluppa il rapporto fra miscela e dipendenza intra-run. Le quantità da distinguere sono:

1. **α=5%**: livello nominale scelto.
2. **17/351≈4,8433%**: media teorica del FAR condizionale su ripetute calibrazioni, sotto le ipotesi della statistica d’ordine continua; non il FAR vero necessariamente ottenuto con questa soglia.
3. **q(T)=P(S nuovo>T | soglia/fit ottenuti)**: FAR ignoto della soglia effettiva per la miscela uniforme delle posizioni.
4. **11/150** e **108/1500**: due stime di q(T), con meccanismi d’incertezza diversi.

La previsione binomiale a p fissato nel registro è una diagnostica di precisione in quello scenario; non identifica q(T) con la media della Beta. Il primario è allineato al protocollo di una finestra per run e permette l’intervallo binomiale sotto IID dei run. La secondaria media tutte le posizioni, stima **lo stesso FAR della miscela** e usa bootstrap di cluster per la dipendenza. È dunque scorretta la frase suggerita nel prompt originario secondo cui il secondario non sarebbe la quantità coperta dalla garanzia condizionale. Il registro P0 dice espressamente il contrario; è il metodo binomiale sulle 1500 finestre a non essere giustificato.

✅ L’IC primario include sia 5% sia 4,8433%; l’IC secondario li esclude. Questi fatti non sono una contraddizione numerica: la soglia realizzata può avere FAR diverso dalla media teorica. La compatibilità del primario non prova FAR esatto, validità delle ipotesi o verifica stretta della Beta. Il limite di precisione dei 150 run richiesto da P0 va mantenuto.

✅/⚠️ La posizione 1 ha 14 superamenti, come la 5: non emerge un massimo esclusivo in posizione 1. Questa sola diagnostica non prova burn-in sufficiente, né autorizza conclusioni causali su transitori o correlazione. Nessun allungamento del burn-in, esclusione di finestre o ritocco della soglia è stato introdotto dal candidato o da questa verifica.

## 8. Conservazione e riscaricamento

✅ Download nuovo fuori dal repository dall’URL in `ARTIFACT_STORAGE.json`, senza modificare la release **studio2-fase03-normal-v1** di `sorrentinoluca/fot-tep-data`. Dimensione **943.793.152 byte** e SHA-256 **`bbcfd0c43a5fbda624deba62fea746150dda4a6d649e6372b8e118270277ac1d`** coincidono con metadati e mandato.

✅ **515/515 file previsti** coincidono per percorso, dimensione e SHA-256. **Mancanti 0; mismatch 0; duplicati di percorso 0.** Verificati separatamente **150/150 `far_ver_seal`**, senza scarti, e tutte le impronte dei 502 file del lotto elencati in `LOT_AUDIT.json`. Workbook scientifici: 350+150. L’estrazione ha rifiutato percorsi assoluti/traversal e membri non regolari; non ha installato metadati nel repository.

⚠️ Contabilità completa dell’archivio, più precisa di “515 file”: **516 file ordinari**, perché c’è un extra rispetto al manifest, **`MANIFEST_CONSERVAZIONE.csv` stesso**, byte-identico alla copia Git. Inoltre **514 membri AppleDouble `._*`**, separati dai file scientifici, e **514 membri con intestazioni PAX associate**. PAX è metadato del contenitore, non un run extra. Liste e hash in `archive_metadata.json`. Il file extra non è corruzione né dato sperimentale non previsto; l’omissione di questa distinzione nei metadati è minore.

⚠️ **D4, documentale, gravità bassa:** il report incluso nella release è la revisione pre-chiusura, hash **`b22acf0f098482344f00c1fbabea4ba946fc382ab7dd982c26979bd8a40a01b0`**, corrispondente alla storia da `d09e7ed` fino a `0802c31`; non è il report a `819b12e`. Il manifest descrive correttamente quei byte. La chiusura `582e575` e l’addendum vengono dopo la pubblicazione e restano recuperabili in Git. Non è stato trattato questo normale disallineamento di snapshot come mismatch dell’asset, né si richiede di ripubblicarlo.

## 9. Provenienza e ruolo della baseline

✅ U1/R2 è autorizzato esclusivamente come **baseline_fit** di N1–N5, non come nuova replica, calibrazione, FAR o test. Sorgente `mode1_normal_500.xlsx`, SHA-256 **`79883dd0aabbd034c15337b0be1ffca37e59ea7b32443a15d560b7feda2b2e6a`**, coincidente fra sorgente locale, copia conservata e `baseline_source_sha256` del fit. Segmentazione di cinque blocchi contigui da 50 h; marca **pre-specificato ma su dati osservati**, correttamente distinta da cecità o indipendenza. Nessuna promozione R1 o dei lotti di qualifica.

✅ §9 registra 350 cal_thr, 150 far_ver, stream, CSV score, commit del freeze, risultati FAR e release. Le impronte complete dei piani e degli input sono recuperabili transitivamente in freeze/manifest; quelle verificate coincidono. La specifica e i piani precedono il batch, perciò la marca di analisi pre-specificata è sostenuta per selezione di J, uso dei lotti, score, rango e regola. Conservazione e scrittura del freeze sono correttamente atti post-esecuzione; non diventano scelte dei dati.

⚠️ Il commit sorgente storico **`309b944f35ac440ff0c70616947ffe723c766e14`** non è disponibile nell’object database locale. L’impronta del workbook è verificata; il legame a quel commit resta un limite **già dichiarato** in PROVENIENZA e nella verifica Fase 02. Non è stato inventato né ricostruito per analogia. Anche i manifest MATLAB riportano hash/parametri ma non un commit completo dell’avvio: il contesto `d09e7ed` è ricostruito dai log e dalla storia, non letto da un campo inesistente del manifest.

## 10. Report, requisiti di chiusura e test

❌ **D4, documentale, gravità media:** nel report candidato la sezione “Correzione pre-batch” mantiene al presente «Restano fuori … il batch, la soglia, il rango, il FAR e THRESHOLD_FREEZE.json; non è stata eseguita alcuna simulazione», mentre sopra riporta il batch e il freeze già prodotti. Va circoscritta esplicitamente alla finestra storica della correzione. La necessità di autorizzare la verifica è anch’essa uno stato precedente al presente mandato. Non è una contraddizione degli artefatti numerici, ma il report di chiusura non è autosufficiente nel distinguere gli stati.

⚠️ Rispetto ai sette punti di `Fase_LLM.md`: risultati e decisioni residue sono presenti; manca l’elenco dei file toccati **uno per riga**, manca **modello/profilo per passo**, e manca una chiusura esplicita sullo stato/decisione di commit. L’identità luna è stata recuperata qui dai metadati, ma resta assente nel report. Il testo originale non costituisce da solo una traccia sufficiente dell’indipendenza.

✅ Test di sotto-fase rieseguiti: **4/4 pytest PASS**, più lo script standard-library **PASS**. Cache pytest e bytecode disabilitati per non scrivere nella sotto-fase. Nessun nuovo test che si limiti a ripetere l’implementazione è stato aggiunto.

✅ `python3 docs/test_explanation.py` eseguito su una **estrazione Git della base effettiva `53a3e92`** nel supporto e sul candidato, prima e dopo il verbale. Risultato: **35 test, 14 failure, 1 skip**. Confronto delle **identità complete**, inclusi parametri dei subtest: uguali; nessun nuovo fallimento. Non è stato accettato il solo numero dichiarato nel report. I test della 03.5 non esistono nella base; questo non è contato come skip o failure della base.

| Identità dei fallimenti documentali | Istanze |
|---|---:|
| `UnifiedConversationChecks.test_condition_c_contract_and_caveats`, phrase=`non un risultato empiricamente misurato` | 1 |
| `UnifiedConversationChecks.test_one_flow_and_ordered_step_headings` | 1 |
| `UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations`: phrase=`0.944444`, `0.916667`, `0.833333`, `zero astensioni`, `C1–C4: 4/4 PASS`, `controllo secondario distinto`, `budget nominale di 1024`, `36 aggregati B non cappati sono corretti`, più il fallimento del metodo senza parametro | 9 |
| `UnifiedConversationChecks.test_step27_qwen_protocol_stable_facts`: doc=`html`, doc=`md`, più il fallimento senza parametro | 3 |

Questi test riguardano documenti storici; il risultato invariato non convalida la 03.5. La verifica sostanziale è nei controlli numerici e documentali precedenti.

## Conclusione motivata e attività necessarie

**NON OK per completezza e correttezza della rendicontazione, non per un errore riscontrato negli score o nella soglia.** Prima dell’OK occorre:

1. **D1:** correggere il parametro associato a 0,947; esplicitare 5%, 17/351, FAR della soglia ottenuta e le due stime; dichiarare l’esclusione di 4,8433% dall’IC secondario e il significato della miscela/cluster, senza ritoccare la soglia.
2. **D2:** rendicontare tutti i pareggi e le ipotesi della Beta; soddisfare C4 per l’incertezza della soglia, o ottenere una decisione esplicita dell’autore sulla riduzione del perimetro. Il bootstrap del FAR non soddisfa quel requisito diverso.
3. **D3:** riconciliare la nota di processo con il testo effettivo dell’handoff/registro; distinguere generazione, lettura per hash, apertura delle celle e analisi; non dichiarare provata una mancata lettura universale. La decisione di accettazione del limite operativo è dell’autore.
4. **D4:** storicizzare le frasi pre-batch, completare modello/profilo e chiusura del report; precisare lo snapshot del report archiviato e correggere la contabilità “35.000 h per cal_thr”.

Non sono richieste nuove simulazioni, una soglia diversa o una nuova calibrazione dai risultati osservati. Nessuna accusa di contaminazione è dedotta dalla sola generazione anticipata. Non è stata corretta alcuna parte del report candidato.

## Comandi, supporto e preservazione

Comandi essenziali effettivamente eseguiti; nelle righe seguenti `R` è il worktree di verifica e `S` la directory di supporto sopra dichiarati:

```bash
git worktree add --detach /Users/luker/fot-tep-verifica-soglie-normal 819b12e97fb94d501032655ec2f226139e6c5ca5
curl -fL --retry 2 -o "$S/studio2-fase03-normal-v1.tar" https://github.com/sorrentinoluca/fot-tep-data/releases/download/studio2-fase03-normal-v1/studio2-fase03-normal-v1.tar
PYTHONDONTWRITEBYTECODE=1 python3 "$S/check_plans.py"
python3 "$S/check_archive.py"
PYTHONDONTWRITEBYTECODE=1 "$S/venv/bin/python" "$S/check_numerics.py"
python3 "$S/check_history.py"
python3 "$S/check_traces.py"
git archive 53a3e92 | tar -xf - -C "$S/base-53a3e92"
PYTHONDONTWRITEBYTECODE=1 "$S/venv/bin/python" -m pytest -p no:cacheprovider studio2/fase03/soglie_normal/tests -q
PYTHONDONTWRITEBYTECODE=1 python3 studio2/fase03/soglie_normal/tests/test_generation_plan_stdlib.py
PYTHONDONTWRITEBYTECODE=1 python3 docs/test_explanation.py
```

Ogni esecuzione ha log nel supporto. L’ultima riga è stata eseguita dalla base estratta e dal candidato; risultati comparati in `tests_result.json`. `check_history.py` conserva i comandi Git estesi, inclusi i confronti senza esclusioni. Gli script di estrazione/rigenerazione usano creazione esclusiva per evitare sovrascritture: per ripeterli si usa una nuova directory di supporto con gli stessi input, non si rilanciano distruttivamente sui risultati esistenti. `check_traces.py` include anche la riproduzione della regola del campione preregistrato.

L’indice `SUPPORT_SHA256.csv` elenca impronte e dimensioni degli script, log, risultati, archivio e inventari. Le impronte dei 516 file ordinari estratti sono in `archive_files.json`; quelle AppleDouble in `archive_metadata.json`; le 185 finestre ricalcolate in `score_checks.json`. Non viene duplicato nel verbale l’intero inventario dei dati. Anche i cinque manifest eseguiti di Fase 02 nella copia principale coincidono con le impronte di `executed_manifests` del freeze, compreso quello dei pilot R2 (`additional_checks.json`).

Impronte degli script eseguiti nel supporto:

| Script | SHA-256 |
|---|---|
| check_archive.py | `8c97812a2035722cb2f5ec10cdeb8771d19846ee756f2d8da25f070d290fab34` |
| check_plans.py | `d1703ee523f212c806b8fa20c45c0af000a852f32cfd0a16bcd9d61eadc01589` |
| check_numerics.py | `23f9a762a5e6f41307b240170c0838384d6e6a40db67c24d6bf08f51a2be3b0c` |
| check_history.py | `122843fdd28cfe29abbeaed32357c1b204c95566806007a3ca8459dfbd76a799` |
| check_traces.py | `0945c144d44188329fddd728352ce83cf33148208c9c66d9fc2083ec89f07d13` |

`numeric_result.json`: `3cf2156a56610972891c35f02908f636c73eeec8fb4f2db448fe38939802cc23`; `tests_result.json`: `6d949ef9911f625034c1f775ec722499c203347fa408e3386e538e9dcccaf23d`. Il log di finalizzazione conserva anche l’impronta dell’indice intermedio; fa fede l’impronta conclusiva dell’indice riportata sotto.

**Unico nuovo documento persistente nel worktree:** questo `VERIFICA_SOGLIE_NORMAL.md`. Non esisteva un verbale a quel percorso: nessun verbale precedente sovrascritto. Nessuna modifica della copia di lavoro principale, del suo branch, di dati, score, soglia, freeze, piani, report o provenienza. Nessun commit, push, merge, tag, pubblicazione o aggiornamento del walkthrough; nessuna simulazione TEP o chiamata a modelli aggiuntivi. La sola modifica ai metadati Git condivisi è la registrazione del worktree esplicitamente richiesta.

**Impronta conclusiva del supporto:** `/Users/luker/verifica-soglie-normal-support-WE8Qqc/SUPPORT_SHA256.csv`, **56 voci**, SHA-256 **`c109c36e83413d6924ab4892b1756d96197833b8b8f572b4c005cdac8bab825b`**. Venv, estrazione della base ed estrazione dell’archivio non sono duplicati nell’indice: ambiente/versioni sono registrati e i contenuti dell’archivio hanno il proprio inventario completo con hash.
