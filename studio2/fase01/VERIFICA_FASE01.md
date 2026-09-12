# OK — ricognizione e consolidamento del patrimonio sperimentale, fasi 1–7

**Verdetto: OK alla chiusura della ricognizione 1–7.** Sul consuntivo `REPORT_FASE01.md`, verificato separatamente in §8: **OK**. Le tre correzioni richieste sono state applicate dalla finestra di lavoro e riverificate; nessuna condizione resta pendente prima del commit. I rilievi che avevano prodotto il
precedente NON OK sulle fasi 1, 6 e 7 sono risolti al livello della ricognizione; le correzioni
sono coerenti con le fasi 2–5. Restano tre voci da registrare, nessuna bloccante, elencate in §6.

> Questo documento **non certifica** la prontezza a generare dati né a eseguire l'esperimento.
> `Ts_base`, burn-in, Philox, score eseguibile, equivalenza dei prefissi e congelamenti operativi
> restano interamente da realizzare.

---

## 1 · Chi, quando, su cosa

| Voce | Valore |
| --- | --- |
| Data | 2026-09-12 |
| Finestra | Sessione Claude (Cowork), distinta dalla finestra che ha svolto la ricognizione |
| Modello | Configurato `claude-fable-5-1`; l'ambiente di sessione riporta `claude-opus-5`. Il modello che serve il turno può differire da entrambi: **l'indipendenza rispetto alla finestra di lavoro è accertata, quella rispetto al modello no** |
| Modalità | **Sola lettura.** Nessuna modifica a documentazione, codice o artefatti; nessun commit, tag, simulazione o chiamata LLM sperimentale. Unica scrittura: questo file |
| HEAD — primo giro | `9289a4cb3b2d657553c4564fc4bb0f95569b6cac` |
| HEAD — riesame | `941c09b2253887101243615165df1d894b8e5c2d` |
| HEAD — stesura di questo file | `9e3d9031013788a583e348fbd7bfc40e14d3c68b` |

**Invarianza fra i tre HEAD.** `git diff` su `code/`, `phase_b/`, `icl/`, `ablation/`,
`reproducibility/`, `tep_test_v2/`, `tep_validation_v2/`, `docs/paper/` e `docs/lit_review/` è
**vuoto** fra `9289a4cb` e `9e3d9031`. I soli commit intercorsi — `941c09b` e `9e3d903` — toccano
`docs/MAINTENANCE.md`, la coppia walkthrough studio 2 e `docs/prompts/`. Le verifiche condotte sul
primo HEAD restano quindi valide senza rifarle.

## 2 · Rapporto con il contratto, e ordine dei fatti

`docs/prompts/Verifica_LLM.md` prevede come oggetto della verifica un file
`studio2/fase<N>/REPORT_FASE<N>.md` e prescrive di fermarsi se non esiste, perché «un riassunto
incollato a mano non è verificabile».

✅ **Il report esiste ed è stato verificato** (§8). Va però registrato l'ordine effettivo, perché
cambia la portata dell'OK:

1. La verifica delle fasi 1–7 è stata condotta sugli **artefatti**, avendo come oggetto le
   affermazioni del prompt di lavoro: `REPORT_FASE01.md` non esisteva ancora.
2. Il verdetto OK è stato emesso in quel momento, e riguarda **il lavoro di ricognizione**.
3. `REPORT_FASE01.md` è stato prodotto **dopo**, e verificato in un passaggio successivo contro le
   stesse fonti primarie.

⚠️ Ne segue che l'OK della ricognizione **non è stato emesso leggendo il report**, e che la verifica
del report è successiva al verdetto che il report stesso cita. Il report ne è consapevole e lo dice
in §10 («non una revisione indipendente della successiva redazione di questo report»): la
formulazione è corretta. Dalla prossima macrofase l'ordine del contratto va rispettato — report
prima, verifica poi — così che i due passaggi non si incrocino.

⚠️ **Non verificabile:** il report attribuisce al testo del riesame ricevuto l'impronta SHA-256
`0ea4657e…`. Non dispongo dei byte esatti di ciò che è stato incollato e non posso confermarla.
L'impronta di un allegato di conversazione non è comunque un artefatto del repository.

## 3 · Esiti per fase della ricognizione

| Fase | Esito | Fonte primaria e riscontro |
| :---: | :---: | --- |
| **1 · Inventario e censimento** | ✅ | Perimetro dichiarato e riproducibile: `code/tep_cache/` 21 + `tep_cache/` 25 (5 radice, 8 validation, 12 test) + `tep_heldout/mode1/` 32 + `tep_exp3_v2_heldout/mode1/` 30 = **108 percorsi, 104 contenuti distinti** per SHA-256; quattro duplicazioni sul batch 1 di F1/F8/F10/F13 fra le due cache. `phase_b/heldout/phase_b_heldout_manifest.csv` ha **15 righe**: i 17 restanti sono esattamente il complemento e rispettano **tutti** `tep_heldout/mode1/mode1_<fault>_11.xlsx`, senza eccezioni |
| **1 · Tabella dei 17** | ✅ | Riprodotta **esattamente su tutti e 17**: byte, righe dati e ora finale, F6 inclusa (582507 / 1029 / 17,1333333333). Verificati su ciascuno **54 campi**, `t0 = 0`, griglia a un minuto; SHA-256 calcolati singolarmente. Nessuna analisi di segnali, separabilità o attivazioni |
| **1 · F6** | ✅ | `tep_heldout_phase_summary.md` §12: il simulatore emette «Low Stripper Liquid Level!! Shutting down.». La nota documenta la scelta di non rilanciarlo «finché passa» per non introdurre bias di selezione, e le istruzioni di non fare padding né troncamento e di conservarlo come prodotto. **Trip fisico, non guasto tecnico** |
| **1 · «non nel manifest» ≠ «mai osservato»** | ✅ | Sostenuto in positivo, non per sola assenza: la stessa nota riporta la campagna (21 run), le lunghezze per run e lo stato del trip; `phase_b/heldout/verify_heldout_integrity.py` documenta il controllo tecnico. L'osservazione **tecnica** c'è stata; quella **scientifica** non è né certificata né esclusa |
| **1 · `r ≤ 24`** | ✅ | Per ciascuno dei quattro guasti nuovi esiste al più un run di questo gruppo; venti recuperabili per le quattro classi già previste. Il limite può scendere: F6 non soddisfa la durata ordinaria finché manca una politica sui trip. La scelta delle classi non deve dipendere da questo risparmio |
| **2 · Provenienza** | ✅ | N1–N5 = cinque blocchi da 50 h in [0, 250 h) di `mode1_normal_500.xlsx`, 15.000 campioni a 1 min, vincolo imposto nel codice. `Ts_base` **non ricostruito**: `0.0005` in `gen_modes.m` contro `5/1000` in `single_batch_autorum.m`. Le **46 copie** di cache coincidono tutte per oid SHA-256 **e** dimensione con i puntatori LFS al commit `309b944f…`. Distinzione a tre mantenuta e ora affinata da §5 |
| **3 · EXP3_V2 e 3.002 record** | ✅ | Artefatti EXP3_V2 solo nei tag `exp3-v2-*` (`phase_b/exp3_v2/` in albero contiene solo `__pycache__`). I 1.080 derivano da `build_exp3v2_inference_schedule.py` nel tag: `range(1080)`, 360 blocchi, A/B/E = 360. Riprodotti 540, 540, 180, 45, 180, 72, 360; i 5 record stanno in `refs/remotes/origin/codex/qwen-reasoning-cap-sensitivity` @ `d4f4708…` e sono rirun su PBH-007/009/014/015. Nessun doppio conteggio di aggregati. **I 3.002 poggiano su 45 casi fisici distinti** (15 PBH + 30 EXP3V2) |
| **4 · Verifica numerica** | ✅ | Riprodotta in memoria sui soli N1–N5, nessun artefatto scritto. LOBO coincide con `normal_5h_window_maxima.csv` entro 7,1·10⁻¹³ (**non** bit a bit); baseline fissa differisce su **50/50** finestre, fino a 0,1395 σ; le quattro soglie congelate si riproducono a <10⁻¹² solo con LOBO; baseline per sensore **identica bit a bit** a quella del verbalizzatore (41 XMEAS × 4 statistiche). Nota: la baseline coincidente è quella **fissa**, le tabelle archiviate sono **LOBO** — oggetti diversi. Lo scostamento delle soglie non è unidirezionale |
| **5 · Ruoli di riuso** | ✅ | `tep_verbalize_v2.py:283–286`: le quattro attivazioni sono `feature > soglia`; la firma strutturata porta `thresholds` e `dataset_commit` come campi di primo livello. Feature indipendenti dalle soglie; firme, testi, esempi e prototipi no |
| **6 · Revisioni R1/R2** | ✅ | Entrambe **non formalizzate**: il piano §6.2 prescrive tuttora 45 simulazioni (8×5 + 5 Normal) «per tutti e otto i fault», e il **requisito residuo 4** del registro rev. 18 nomina ancora il conflitto e chiede quale documento aggiornare. Separazione R1/R2 corretta |
| **6 · Formula e scenari** | ✅ | `N = B + (40 − r) + u + 9n + 6 + D` riproduce la tabella esattamente: **595/613 · 590/608 · 591/609 · 586/604**. Ramo alternativo `B=560, r=20, u=5`: **645/663**; incremento di B da solo **50**, confronto con lo scenario principale `u=0` **55** (50 + 5 Normal). 570/588 richiederebbero `r=40`: **ritirati**, coerentemente con `r ≤ 24`. Ritiro dell'assegnazione automatica di cinque dei cento `baseline_fit_new`: corretto, il registro non la stabilisce |
| **6 · Budget API** | ✅ | §8.8 conferma 2.594/3.232, ~2.853/~3.555, tetti 3.000/3.700. Delta corrente **638 ≈ 24,6 %**; il «+590» appartiene alla coppia obsoleta 2.450/3.040. Il budget resta condizionato a R=1 nel nucleo, perimetro E5 e riuso FULL=B-LF, e non è certificato dal recupero dei vecchi risultati |
| **7 · Percorsi predefiniti** | ✅ | Rilievo **accertato e più netto**: `code/tep_characterize_v2.py` riga 39 `OUTPUT_DIR = Path("tep_analysis_v2")`, scritture da riga 203, e lo script **non contiene alcun `add_argument`** — nessuna interfaccia a riga di comando, quindi la destinazione non è sovrascrivibile da alcuna invocazione: la cambia solo la directory di esecuzione. Trattarlo come non riutilizzabile così com'è, con adattamento in file nuovo a destinazioni esplicite, è sufficiente a livello di ricognizione |
| **7 · Perimetro §8** | ✅ | `docs/MAINTENANCE.md` §8 presente in HEAD: radice unica `studio2/`, niente `code/studio2/` né `outputs/studio2/`. Verificato che `studio2/` non esisteva prima di questo file e che nessuna documentazione è stata creata dalla ricognizione |

## 4 · Esiti sui controlli di `Verifica_LLM.md`

| # | Controllo | Esito | Riscontro |
| :---: | --- | :---: | --- |
| 1 | Fonti ricostruite da zero | ✅ | Ogni numero risalito all'artefatto: manifest, tag, ref, codice, XLSX |
| 2 | Perimetro congelato intatto | ✅ | `git diff` vuoto su `phase_b/`, `icl/`, `ablation/`, `reproducibility/`, `tep_*_v2/`, `code/` fra `9289a4cb` e `9e3d9031`; albero di lavoro pulito |
| 3 | Precedenze rispettate | ✅ | Calibrazione: prevale il registro rev. 18, usato come fonte per `B=510/560` e per il requisito 4. `BIGDATA2026` non usato come piano; il rimando discordante in §0.1 del walkthrough risulta **corretto e committato** in `941c09b` |
| 3b | `criteri_scelta_descrittori.md` §5.1 vs §5.5 | ⚠️ | **Non esaminato**: la ricognizione non tocca la scelta dei descrittori. Non è un riscontro, è un non-oggetto |
| 4 | Dati del primo studio: letti, non ipotizzati | ✅ | Letti: 108 XLSX per SHA-256, 46 confronti contro i puntatori LFS, riproduzione numerica su N1–N5 |
| 4b | Riga in `studio2/PROVENIENZA.md` | ⚠️ | Il file **non esiste**. Non è ancora dovuto — nessun riuso è stato eseguito, R1 e R2 sono proposte — ma va creato prima di qualunque operazione che usi quei dati |
| 5 | Ordine delle sotto-fasi, decisioni anticipate | ✅ | Nessuna decisione anticipata riscontrata. La ricognizione non sceglie guasti e non esamina separabilità o attivazioni, coerentemente con il divieto di §6.1 del piano |
| 6 | Coppia MD/HTML allineata sul contenuto | ✅ | `fot_walkthrough_conversazione_studio2.md` ↔ `.html`: tutti e 17 i riferimenti §6.x/§7.x presenti in entrambi, «Sintesi per sezione» presente in entrambi. Le differenze rilevate a un primo passaggio erano di sola marcatura: livello dell'intestazione, numerali di lista ordinata, entità `&#9888;` |
| 7 | `python3 docs/test_explanation.py` | ✅ | `Ran 35 tests` — `FAILED (failures=14, skipped=1)`. **14 fallimenti, esattamente la soglia preesistente** di `MAINTENANCE.md` §5. Non peggiorato |

## 5 · Conservazione — misura, e correzione di un mio errore

❌ **Nel primo giro avevo scritto che nessun XLSX è conservato in Git. È falso.** Vero
dell'indice corrente, falso della storia.

✅ Verificato senza checkout né ripristino: il tag `exp3-v2-heldout-data-frozen-001` contiene
**30 blob XLSX reali** (firma ZIP `PK\x03\x04`, nessun puntatore), **tutti e 30 coincidenti per
SHA-256 con le copie locali**, per 51.188.047 byte.

✅ Misura estesa a **tutti i ref** (tag, branch, remoti): nell'intero object store esistono
**esattamente 30 blob XLSX distinti**, quelli. Copertura sui 104 contenuti distinti:

| Raccolta | Contenuti distinti | Conservati in Git |
| --- | ---: | :---: |
| `tep_exp3_v2_heldout/mode1/` | 30 | **sì** |
| Le due cache — 46 percorsi, **42** distinti (38 una volta, 4 due volte) | 42 | no |
| `tep_heldout/mode1/` | 32 | no |
| **Totale** | **104** | **30** |

**Conseguenza.** I 74 contenuti non conservati comprendono N1–N5 (`mode1_normal_500.xlsx`), i venti
run di sviluppo che R1 propone di riusare, i quindici casi PBH che portano l'evidenza confermativa
del primo studio e i diciassette candidati per i guasti nuovi. *Tutto ciò che R1 e R2 propongono di
riusare sta nell'insieme non protetto; i trenta conservati sono gli unici da cui il riuso non
dipende.* Lo store LFS locale dell'upstream è vuoto e `git-lfs` non è installato: i 42 contenuti di
cache non sono neppure riscaricabili qui. Nessuna copia di sicurezza verificata trovata; gli hash
non colmano la lacuna, ed è quanto dice `MAINTENANCE.md` §8.5.

**Blocca la chiusura della ricognizione? No.** La ricognizione ha individuato, localizzato, misurato
e delimitato la lacuna, e chiuderla non consuma il rischio. Va però distinta dagli altri pendenti:
`Ts_base`, burn-in, Philox, score, prefissi e congelamenti sono cose **da costruire**, e il ritardo
costa calendario; questa è una cosa **che si può perdere in modo irreversibile**, ed è l'unica il
cui margine può chiudersi da solo. Poiché le prime attività successive alla chiusura — verifica di
R1/R2, ricalcolo della baseline su N1–N5 — leggono tutte da quell'insieme, **la messa in sicurezza
va eseguita prima di qualunque operazione che legga o sposti quei 74 contenuti**. È una copia
verificata più la sua registrazione, non una decisione di disegno.

## 6 · Che cosa resta, per categoria

**Rilievi accertati.** Percorsi predefiniti di `tep_characterize_v2.py`; `r ≤ 24`; F6 terminato per
trip fisico; «non nel manifest» ≠ «mai osservato»; copertura di conservazione 30/104.

**Revisioni proposte al disegno, non decise.** R1 — riuso verificato dei venti run fault di
sviluppo al posto della rigenerazione. R2 — N1–N5 al posto dei cinque nuovi Normal di sviluppo, con
separazione fra sviluppo, baseline e calibrazione, da agganciare al requisito residuo 4 del registro
rev. 18 e da riconciliare con §§6.2–6.3 del piano. Nel ramo principale `u=0` **richiede R2**; senza,
`u=5`.

**Attività implementative successive.** Messa in sicurezza dei 74 contenuti; adattamento del
caratterizzatore in un file nuovo dentro `studio2/`; politica metodologica sui trip; creazione di
`studio2/PROVENIENZA.md`; correzione delle discordanze di budget nel piano.

**Lacune residue, nessuna bloccante, tre da registrare.**

1. **La discordanza di budget è più estesa di come è stata registrata, e ne contiene una seconda.**
   La coppia 2.450/3.040 compare nel piano alle righe 119, 164, 324, 609, 1027 e 1369, ed è ora
   entrata anche nel walkthrough studio 2 committato (riga 106, §7.4). Soprattutto, **il tetto a
   otto run è registrato in due valori diversi**: §8.8 chiede **3.700** (righe 534, 555), mentre le
   righe 1027, **1110 (T5)** e **1160 (O2)** — criteri della checklist GO/NO-GO — e 1369 portano
   **3.500**. Il sottototale con retry di §8.8 a otto run è **~3.555 > 3.500**: allo stato dei
   documenti **un criterio GO/NO-GO è violato dall'aritmetica del piano stesso**. «Correggere
   successivamente» va quindi delimitato: **prima della decisione 2 di §0.1** (sei o otto run), che
   è ciò che `n` parametrizza.
2. **§8 non copre due casi prodotti dalla ricognizione.** §8.1 elenca «codice, configurazioni, test,
   manifest, esecuzioni, risultati» e **non nomina i dati**, che è il punto aperto visto che
   `*.xlsx` è ignorato globalmente (§8.5 li tratta, il perimetro di §8.1 no). E §8.2 punto 1 esige
   in `PROVENIENZA.md` «origine, seed, data e commit», ma per i diciassette run **il seed non
   risulta da alcun artefatto**: il manifest PBH porta `simulator_commit`, `model_name`,
   `matlab_version`, `solver`, non il seed. La regola «metadati mancanti dichiarati mancanti» è
   necessaria ma **non è scritta in §8**, che dice solo che i dati non si ipotizzano.
3. **Tracciabilità della verifica.** Vedi §2: assenza di `REPORT_FASE01.md`.

## 7 · Informazioni non recuperabili

`Ts_base` storico di N1–N5; i seed di generazione dei run del primo studio; la disponibilità remota
degli oggetti LFS del dataset upstream. Vanno dichiarate mancanti, non ricostruite per inferenza.

---

## 8 · Verifica di `REPORT_FASE01.md`

Aggiunta il 2026-09-12, dopo che il report è stato reso disponibile. Oggetto: il file
`studio2/fase01/REPORT_FASE01.md` (303 righe) su HEAD `9e3d9031…`. Ogni affermazione è stata
risalita alla fonte primaria, non al report. **Esito: OK.** Tre correzioni erano state richieste in prima
lettura; sono state applicate e riverificate il 2026-09-12 (§8.3). Nessuna condizione resta
pendente prima del commit raccomandato dal report in §11.

### 8.1 Riscontri positivi

| Affermazione del report | Esito | Riscontro |
| --- | :---: | --- |
| §4.1 — regola di perimetro, 108 percorsi / 104 contenuti, composizione delle sei righe, quattro duplicazioni nominate, 46 percorsi e 42 contenuti (38 + 4×2) nelle due cache | ✅ | Ricontato sui file |
| §4.1 — `tep_exp3_v2_heldout/mode1/` = 24 fault e sei Normal | ✅ | Nomi `EXP3V2-{F1,F8,F10,F13,N}-00{1..6}` |
| §4.1 — N1–N5 sono 250 ore continue, non cinque simulazioni; il Normal da 50 h non è di indipendenza stabilita | ✅ | `mode1_normal_50.xlsx` (3001 righe, 0→50 h) **non è un prefisso** di `mode1_normal_500.xlsx`: max&#124;diff&#124; 143,31 sul tratto comune. Dato diverso, indipendenza non dimostrata da questo: la cautela del report è corretta |
| §4.2 — tabella dei 17: byte, righe, ora finale **e SHA-256 completi** | ✅ | **17/17** coincidono con il file reale, impronta a 64 cifre e dimensione |
| §4.2 — F6, trip fisico, nessun padding o troncamento autorizzato | ✅ | `tep_heldout_phase_summary.md` §12 |
| §4.3 — 30 conservati in Git, 74 no; blob reali non puntatori; non nell'indice corrente | ✅ | Misurato su tutti i ref |
| §4.3 — «l'assenza di git-lfs è una limitazione dello strumento, non prova di indisponibilità remota» | ✅ | Correzione giusta a una mia formulazione troppo forte del primo giro |
| §5 — 820 feature per caso, 6.560 per finestra, 820 firme temporali, 2.050 Normal per variabile, 50 massimi | ✅ | Righe dati delle rispettive tabelle in `code/tep_analysis_v2/` |
| §5 — quattro raccolte di esempi locali, dieci esempi sorgente distinti | ✅ | `local_example_sources.json`: `EXM-001…EXM-010` da **nove file**, perché N1 e N2 vengono entrambi da `mode1_normal_500.xlsx`; `agent_to_pack` = `LKP-001…LKP-004`. Esempio esatto della distinzione fra unità che il report stesso impone |
| §5 — otto modelli centralizzati salvati | ✅ | `c02b_supervisor_model_suite/results/models/`: cinque `.pkl` e tre `.bin` |
| §5 — 3.002 record su 45 casi fisici distinti; il local-first completo riusa i 30 EXP3_V2 | ✅ | Come da §3 di questo documento |
| §5 — il follow-up sensitivity ha **quattro** risposte corrette su cinque | ✅ | `results.json` su `d4f4708…`: `errors_at_3072_persistent` = `[["agent_4","PBH-014"]]`, `incorrect_and_still_capped_at_4096` vuoto. Correzione utile: quel record è un errore persistente, non un successo |
| §5 — verificate nove dipendenze del manifest conclusivo e tre payload | ✅ | `boundary_tags` len 9; `evaluation_outputs/` contiene esattamente tre file. Il report dichiara che non è una verifica ricorsiva: corretto |
| §6.1 — tabella degli scarti massimi fra archivio LOBO e baseline fissa | ✅ | **Riprodotta esattamente sui 2.050 valori**: 0,1395248782 · 0,0317945538 · 0,0556652197 · 0,0298025431 |
| §6.1 — tutti i 2.050 valori di ciascuna delle quattro feature differiscono oltre 1e-12 con baseline fissa | ✅ | 2050/2050 per tutte e quattro |
| §7, §8.1 — R1/R2 distinte e non formalizzate; formula con `u`; tabella dei cinque scenari; ritiro di 570/588; ritiro dell'assegnazione dei cinque baseline | ✅ | 595/613 · 590/608 · 591/609 · 586/604 · 645/663 ricalcolati; piano §6.2 e requisito 4 del registro invariati |
| §8.1 — R1 e R2 insieme eviterebbero 25 simulazioni; i 17 offrono al massimo un candidato per classe nuova | ✅ | 20 + 5 = 25; un solo run per fault fra i 17 |
| §8.2 — 105/123 = 45 sviluppo + 60/78 valutazione; tabella API di §8.8 | ✅ | 45 + 54 + 6 e 45 + 72 + 6; tutte le righe coincidono con §8.8 |
| §8.3 — tetto a otto run 3.700 contro 3.500 in T5 e O2, con ~3.555 che supera 3.500; delta 638 ≈ 24,6 % | ✅ | Confermato; il report recepisce il rilievo e lo àncora correttamente **prima della decisione D2** |
| §9 — rilievo sui percorsi, quattro asserzioni | ✅ | Riga 39, scritture da riga 203, nessun `add_argument` nello script, destinazione relativa alla directory di esecuzione |
| §11 — 12 collegamenti locali risolti; una sola riga aggiunta a `DOCUMENTATION_INDEX.md`; 35 test e 14 fallimenti | ✅ | 12/12 risolti; il diff dell'indice è **una riga**, e mappa una cartella non un file, come vuole `MAINTENANCE.md` §4; `FAILED (failures=14, skipped=1)` |
| §10 — l'OK non copre la redazione del report e non adotta R1/R2 | ✅ | Rappresentazione fedele del verdetto |

### 8.2 Coerenza con questo documento

Dove il report e la §3 di questo file danno numeri diversi per la stessa feature, **gli oggetti sono
diversi e entrambi i conti sono giusti**: il report misura sui **2.050 valori per variabile e
finestra** (`normal_5h_variable_features.csv`), questo documento misurava sui **50 massimi per
finestra** (`normal_5h_window_maxima.csv`). Sui massimi per finestra gli scarti con baseline fissa
sono 0,1395 · 0,0303 · 0,0329 · 0,0298 su 50/50 finestre; sui 2.050 valori sono quelli della
tabella del report. Nessuna delle due misura contraddice l'altra, e la conclusione — ricalcolo
necessario — è la stessa.

### 8.3 Correzioni richieste, applicate e riverificate

Le tre correzioni sono state applicate dalla finestra di lavoro e ricontrollate sul file. Il
rilievo originale resta registrato qui: è la traccia di che cosa la verifica ha intercettato.

| # | Rilievo di prima lettura | Stato | Riscontro sulla correzione |
| :---: | --- | :---: | --- |
| 1 | §6.1 dichiarava «scarto massimo dell'ordine di `4,44e-16`». Era il massimo del solo `diff_std_ratio`, **il più piccolo dei quattro**, presentato come massimo complessivo: tre ordini di grandezza di scarto. I quattro massimi reali sui 2.050 valori sono `1,414e-12` · `5,551e-16` · `2,098e-14` · `4,441e-16` | ✅ chiuso | Riga 148 riporta ora `1,41e-12`, che coincide con la misura indipendente |
| 2 | §8.3 citava la coppia obsoleta 2450/3040 come presente in «§§0.1, 2, 7, 8.9, 10 e 13». La riga 119 sta in **§1** «Giudizio generale»; §0.1 porta il «+590 chiamate» (riga 94), cifra collegata ma diversa | ✅ chiuso | Riga 260 riporta ora «§§1, 2, 7, 8.9, 10 e 13» |
| 3 | §8.2 attribuiva a E5 i totali 2.906/3.626, che il piano lega al **mancato riuso di FULL da B-LF** (§8.8) | ✅ chiuso | Riga 254 riporta ora «Senza riuso di FULL da B-LF», allineato alla formulazione del piano |

**Integrità del resto del documento.** Il file resta di 303 righe e 28.557 byte — le tre modifiche
si compensano in lunghezza — e i controlli sostanziali sono stati ripetuti dopo l'intervento: i 17
SHA-256 del censimento coincidono 17/17 con i file reali, i quattro valori della tabella §6.1 sono
invariati, la tabella degli scenari e quella del budget API sono integre, i 12 collegamenti
risolvono. Nessuna modifica collaterale.

### 8.4 Un punto di formulazione rimasto aperto, non bloccante

⚠️ La correzione del numero **non chiude** il rilievo che la accompagnava, e anzi lo rende
visibile. La frase di §6.1 ora dice che lo scarto LOBO massimo è `1,41e-12` e, subito dopo, che i
2.050 valori con baseline fissa «differiscono **invece** oltre `1e-12`». Ma **20 dei 2.050 valori
LOBO superano anch'essi `1e-12`**: l'avversativa poggia su una soglia che i due casi condividono.

La separazione è reale e larghissima — ordine `1e-12` contro ordine `1e-2`, dieci ordini di
grandezza — quindi la conclusione del report è corretta e non serve rivederla. È l'argomento che
andrebbe detto sulla **magnitudine** invece che su quella soglia. Lo registro come punto di
formulazione: **non blocca il commit** e non richiede una nuova verifica.

### 8.5 Perché l'esito è OK

Nessuno dei tre difetti toccava una conclusione: il ricalcolo delle feature Normal resta
necessario, le discordanze di budget restano quelle rilevate, e la mappatura delle sezioni è un
localizzatore, non un argomento. Il primo era però **un numero misurato riportato male**, in un
documento il cui scopo è conservare misure, e andava corretto prima che il consuntivo entrasse
nella storia del repository: è stato fatto.

---

## 9 · Stato al momento della chiusura

Rilevato il 2026-09-12, a verifica conclusa.

| Voce | Stato |
| --- | --- |
| Branch | `codex/studio2-report-ricognizione`, un commit avanti a `main` (`9e3d903`), tracciato su `origin`. Nome conforme a `MAINTENANCE.md` §8.3 |
| `DOCUMENTATION_INDEX.md` | **Committato** in `bd91f33`, una sola riga, che mappa una cartella e non un file come vuole §4 |
| `studio2/fase01/` | **Non committata.** Contiene `REPORT_FASE01.md` e questo file; non è ignorata da Git |
| ⚠️ Link interno | `git ls-tree bd91f33 studio2` è vuoto: la riga d'indice già committata punta a un percorso che in quel commit non esiste, contro §5 punto 2. Si risolve al commit di `studio2/`, che va quindi fatto e non rimandato |
| Congelamenti | Nessun tag creato. Nessun artefatto congelato modificato |
