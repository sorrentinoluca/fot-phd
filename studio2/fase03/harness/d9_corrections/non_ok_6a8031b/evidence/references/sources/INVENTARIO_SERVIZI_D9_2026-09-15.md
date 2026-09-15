# Inventario documentale dei servizi Qwen — D9

**PREPARAZIONE OFFLINE — SERVIZI NON QUALIFICATI DA QUESTA CONSEGNA**

Redazione: **15 settembre 2026, Europe/Rome**. La data indica l'acquisizione documentale in questa finestra, non una nuova osservazione dei servizi o una nuova comunicazione del gestore.

## 1. Mandato, ruoli e stato Git

Il mandato corrente richiede inventario, metadati mancanti, testo da inoltrare e checklist. Nessun contatto con servizi o terzi è stato effettuato. Le sole operazioni remote sono letture Git di `refs/heads/main` dal repository effettivo; non sono prove dei servizi Qwen.

Preflight prima di scrivere:

- repository/worktree: `/Users/luker/fot-tep-proposta-d9`;
- branch: `codex/studio2-proposta-d9`;
- HEAD iniziale: `aaba893dff8c62f9f9281eec7423eee020235e03`, coincidente con il commit D9 comunicato; worktree pulito;
- origin fetch/push: `https://github.com/sorrentinoluca/fot-phd.git`;
- main remoto effettivo osservato con `git ls-remote origin refs/heads/main`: `a00605862f627710347bd63c49f79a6d0a00135f`;
- altri worktree preservati; nessuna importazione del candidato harness in review. Il suo contratto al pin H10 è stato soltanto letto per distinguere requisiti futuri da verifiche già svolte.

Il [record D9 approvato](DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md) e la [consegna di recepimento](CONSEGNA_RECEPIMENTO_D9_2026-09-14.md), fonti D e C, fissano:

| Ruolo | Assegnazione già approvata | Conseguenza per questo inventario |
| --- | --- | --- |
| Producer principale P | Qwen 122B | Identificare e qualificare la produzione della libreria conforme. |
| Consumer C | Qwen 122B | Identificare e qualificare input diagnostici, output parsato, capienza, stabilità e latenza nei soli stadi previsti. |
| Producer alternativo P_alt | Qwen 27B | Libreria completa di **16 insight**, secondo il contratto vigente; nessun ruolo automatico di consumer di fallback. |
| Producer-swap | Consumer **122B invariato**, medesimi casi previsti dal disegno | Varia la libreria del producer, non il consumer né la popolazione dei casi. |
| Terra | Solo riferimento storico descrittivo interno | Separato dalle stime del nuovo studio; nessuna nuova produzione né qualifica Terra. |

La raccomandazione iniziale della proposta (27B principale, 122B alternativo) e la proposta harness con Terra alternativo sono superate nei ruoli. La proposta originale, il record approvato e gli altri artefatti D9 restano byte-identici. D9 non approva ordine label 1a, firma materiale 03.8, configurazioni eseguibili, chiamate, pilot, nuovi bracci o budget. A/B, FAR, U3 e freeze pubblicati restano invariati.

## 2. Come leggere le evidenze

- **D — dichiarata corrente** dall'autore o dal gestore, come riportato nella fonte e alla data di quella comunicazione; non ricertificata oggi.
- **H — storica, da riconfermare** per un eventuale uso corrente. Un file di configurazione descrive valori attesi o impostati, non necessariamente ciò che il servizio oggi applica.
- **V — verificata entro un perimetro documentato**: il record descrive una verifica delimitata per data, endpoint, input e configurazione. Qui è stata controllata la fonte locale, non rieseguita la verifica remota. Una V storica rimane H rispetto alla disponibilità attuale.
- **M — mancante** nelle fonti consultate, oppure non attestata per il servizio/ruolo corrente. “M” non significa che la capacità sia assente.

I codici fonte rimandano a §7, con percorso, commit di consultazione e SHA-256 dei byte. Le date degli eventi sono riportate qui dalle fonti; il commit di consultazione non è il timestamp dell'evento. Nessuna firma, sessione o ora del messaggio originario del gestore viene ricostruita per intuizione.

## 3. Servizio 122B — P e C

Fonte comune delle dichiarazioni: **H0 §5**, handoff datato 14 settembre 2026, comunicazioni dell'autore/gestore riportate nel documento e poi pubblicate in 03.15. Il mandato corrente mantiene queste indicazioni, in particolare l'omissione di `temperature`; non aggiunge un'attestazione dei pesi.

| Informazione | Valore documentato e classe | Limite / dato ancora necessario |
| --- | --- | --- |
| Disponibilità | **D**: «Up and running» riferito dall'autore | Disponibilità dichiarata, non qualifica; nessun controllo di raggiungibilità oggi. |
| Nome annunciato | **D**: `Qwen3.5-122B-A10B-FP8` | **M**: repository esatto, revisione immutabile e prova di corrispondenza ai pesi serviti. Non aggiungere un namespace presunto. |
| API | **D**: base URL `http://cygnusx1.portici.enea.it:8000/v1`, alias `qwen3.5-122b`, accesso solo API | **M**: mapping alias→backend, eventuali repliche/routing e contratto effettivo delle richieste/risposte. Nessuna credenziale riportata. |
| Quantizzazione/calcolo | **D**: suffisso FP8 nel nome annunciato | **M**: quantizzazione effettiva, formato/ricetta, dtype di calcolo/KV, hardware e parallelismo. Il suffisso non è un'attestazione tecnica. |
| Limiti | **D**: contesto 131.072 token, output massimo 16.384 | **M**: semantica input/output/combinato, overhead template e reasoning, limiti del gateway, comportamento oltre limite e tagli silenziosi. Non dedurre un input massimo per semplice sottrazione. |
| Temperatura | **D**: **omettere interamente `temperature` dalla richiesta**, default server dichiarato **0,6** | Non inviare `null`, stringa vuota o `0.6`. Default non misurato; **M** gli altri parametri effettivi e la loro applicazione. |
| Tokenizer/template | **M**: nessun pin del servizio 122B nelle fonti consultate | Repository/revisione tokenizer, file e hash, template effettivo e override, special token e opzioni di rendering. |
| Serving/thinking/risposta | **M**: versione/build, parser, thinking e campi reasoning, schema supportato, request ID, usage, finish reason e fingerprint | Nessuna proprietà del vecchio vLLM viene trasferita al 122B. |
| Immagini/browser/cache | **D**: immagini supportate secondo il gestore; browser use non supportato; prompt cache non disponibile | Studio testuale; nessuna estensione multimodale e nessun risparmio cache presunto. Non occorre richiedere di nuovo queste informazioni per D9. |
| Quota | **D**: «non hai limiti di utilizzo in token», secondo il gestore | Non elimina contabilità dello studio, timeout, rate limit, code, limiti per richiesta o vincoli temporali. |
| Aggiornamenti, tempo, carico | **M**: politica di aggiornamento/freeze, finestra di disponibilità, concorrenza, condivisione risorse, latenza e stabilità effettive | Richiedere condizioni amministrative; misurare prestazioni solo in stadi autorizzati. |

Non risultano prove di inferenza 122B nelle fonti consultate. I blocchi pubblicati 03.15 (P15) riprendono H0, non aggiungono un'attestazione indipendente. Il loro “D9 aperta” è precedente al record D e non riapre i ruoli. L'identità del nuovo servizio precedentemente indicata come `qwen3.8-27b`, con 262144/32768, è esplicitamente superata da H0; non va importata dal delta statistico storico. Il 2.4T dichiarato non ospitabile non è una risorsa prevista.

## 4. Servizio 27B — soltanto P_alt

La disponibilità del 27B sull'altro server è **D**, comunicata dall'autore in H0 e richiamata nel mandato; l'identità esatta corrente va invece ricollegata ai seguenti record **H/V**. Il nome API storico `fot-exp2-consumer` non assegna oggi un ruolo consumer.

| Informazione | Valore documentato, data e classe | Perimetro / riconferma necessaria |
| --- | --- | --- |
| Pesi e alias | **H**, preflight F e record E del 13/09: `Qwen/Qwen3.8-27B-FP8`, revisione `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`, alias `fot-exp2-consumer` | **M** mapping corrente del servizio che produrrà i 16 insight. Conservare nome e revisione letterali. |
| Endpoint | **V storica** E §§8,13: host albireo, `http://127.0.0.1:8001/v1`, `max_model_len=16384`; health e models osservati il 13/09 | Loopback riferito al server, non indirizzo utilizzabile dal Mac. **M** modalità di accesso corrente autorizzabile e mapping; nessun SSH presunto. |
| Processi | **V storica** E: API PID 690460, EngineCore 690661; avvio 13/09 01:52:36 CEST | PID e tempi sono snapshot; non identificano in modo persistente pesi o servizio. |
| Serving | **H/V** E, F, L: vLLM 0.28.0; `--reasoning-parser qwen3`, text-only, TP=1, max-num-seqs=1, gpu-memory-utilization=0.97, enforce-eager, generation-config=vllm, prefix caching disabilitato | Comando completo e ambiente sono nelle fonti. **M** riconferma build/config/parser effettivi del servizio corrente e delle eventuali modifiche. |
| Ambiente | **V storica** E §16: Python 3.12.14, PyTorch 2.13.0+cu132, Transformers 5.16.1, Triton 3.7.1, flashinfer-python 0.6.16.post3; driver 580.173.02 | Versioni osservate allora, non requisiti nuovi. FlashInfer sampling disattivato con `VLLM_USE_FLASHINFER_SAMPLER=0`; non basta l'argv a descrivere l'ambiente. |
| Quantizzazione/hardware | **V storica** E §§4–5,16: fp8, `torch.bfloat16`, architettura risolta `Qwen3_5ForConditionalGeneration`; GPU0 su host con 2×RTX 5000 Ada, 32760 MiB ciascuna | Non “correggere” `Qwen3.8` in `Qwen3.5`: la discordanza fra nome e classe architetturale è da far chiarire con attestazione. **M** configurazione corrente, ricetta FP8 e dtype KV effettivo. |
| Cache dei pesi | **V storica documentata** E §15: 76 file di inferenza con stessi basename/hash dei blob fra le due cache locali; quattro file accessori solo in una | Attestazione conservata, non nuovo hashing dei pesi. Non prova indipendenza di modelli fra endpoint né parità delle configurazioni; la cache di pesi HF non è prompt cache. |
| Tokenizer e template | **H** F: tre impronte riportate sotto. **V circoscritta** R4 del 14/09 sul tokenizer reale per i test del contratto insight, 26/26 senza skip | Verifica R4 del contratto, non del servizio corrente né della capienza chat. **M** riconferma file effettivi, revisione tokenizer e override del template di serving. |
| Sampling/thinking | **H** F: T=0, seed=20260829; candidati thinking 2048/3072/4096, riserva risposta 512, margine 256; selezione congelata assente | Valori del vecchio preflight consumer: non configurazione approvata P_alt, non valori da trasferire al 122B. |
| Stato preflight | **H** F: `GATE_ENVELOPE_FROZEN_EXECUTION_SUSPENDED`, `study_model_decision=UNDECIDED` | Stato storico preservato. D9 è approvata nel record D, ma questo JSON non è diventato eseguibile. |
| Concorrenza | **H/V** E,F: max-num-seqs=1; log KV 34.133 token e stima 2,08× | Non prova di due richieste concorrenti servibili, throughput o disponibilità odierna. Risorse condivise anche con altro processo e desktop, secondo lo snapshot. |
| Metadati risposta | **V storica** Q, 08/09, endpoint 8000@4096: `response_id`, `model`, `finish_reason`, usage prompt/completion/total, reasoning_tokens, raw `message.reasoning` separato da content, `system_fingerprint=vllm-0.28.0-abc0cde2` | Quattro richieste su fixture capability, incluso replay B. Non garantisce campi o stabilità attuali. Il fingerprint API non è la revisione dei pesi. |
| Limiti e latenza su fixture | **V storica** S, 13/09 00:44:21.793634 UTC: tre inferenze su fixture sintetiche a 16384, più una richiesta precedente rifiutata; budget provvisorio thinking 2048/max_tokens 2560 | PASS tecnico provvisorio, budget non congelato, nessun gate autorizzato. Latenze A/B-LF/E-LF circa 32,826/152,536/62,297 s appartengono a quelle sole fixture consumer; non stimano il producer P_alt né T5 corrente. |
| Errori/zero token e gestione | **M** per il servizio corrente: timeout, codici errore, annullamento, prova correlabile di mancata generazione/zero token, update policy, disponibilità e carico | I record storici di avvio e probe non attestano queste garanzie oggi. |

Il record E attesta **zero POST nella sua finestra di osservazione di avvio** (02:04:40 CEST); S, completato dopo (02:44:21 CEST), registra inferenze su fixture. Non sono contraddittori e non si può estendere lo zero iniziale all'intera storia del pilot. La consegna futura deve riconciliare il consumo storico; D9 e il cambio alias non azzerano il ledger.

Impronte tecniche **storiche**, trascritte da F (non ricalcolate sui file remoti):

| Oggetto | SHA-256 dichiarato nel record |
| --- | --- |
| `tokenizer.json` | `0997f410c57a1f4e53b09e4be8f4a172d90edd9564368fb0847030937229b9f3` |
| `tokenizer_config.json` | `b11349aafa7cdc6a320767cf7ceb29ed82f7eda5d65e8e0819e76f0ce947bf27` |
| `chat_template` | `c3cf9e34abf4f9e36c2d72165aa9c132d3e2a725b6c2586aaa3a8af9d7a81041` |
| Comando processo | `b1560330f54807c5396e03360e7938748a1e4c41bf63f427ff74b6661de499d7` |
| Ambiente selezionato | `de6e5d641edcdc8542fddadf5abfbbeae9054e08aa099cb2998150d274816793` |
| Fingerprint composito processo | `39b59324e643e892bfdd05beac763aa9ca80092941f28ce01f582f0f3a593017` |

Quest'ultimo hash non è `system_fingerprint` dell'API. Per il template occorre distinguere hash del file `chat_template.jinja`, della stringa selezionata e del template effettivamente applicato con eventuali override: richiedere byte e regola di hashing, senza equipararli.

## 5. Matrice dei metadati mancanti per ruolo

**G** = attestazione/configurazione documentabile dal gestore competente (o dall'autore per il server che amministra), senza credenziali; indicare data di validità, origine e modifiche rispetto allo snapshot. **O** = controllo offline su file acquisiti e improntati. **P** = comportamento da verificare sul servizio con futura autorizzazione. La disponibilità di documenti G non equivale a esito P. Le prove P vanno inserite negli stadi già previsti (§6 e checklist), non diventano un nuovo pacchetto di chiamate.

| ID / dato | 122B P+C: quanto manca | 27B P_alt: quanto manca o va riconfermato | Attestazione / futura verifica |
| --- | --- | --- | --- |
| M01 Pesi | Repo e revisione immutabile; manifest dei file effettivamente caricati, eventuali adattatori | Riconfermare nome/revisione di §4, snapshot e corrispondenza ai file caricati; chiarire ambiguità nome/architettura | G: identificativi e manifest, non solo model ID. O: coerenza/impronte dei file disponibili. P: identità esposta coerente; sola API non prova crittograficamente i pesi. |
| M02 Quantizzazione/calcolo | FP8 effettivo, formato/ricetta, dtype di calcolo e KV, hardware, parallelismo | Riconferma fp8/bfloat16, ambiente e hardware, precisare ricetta/KV e delta | G/O per manifest/config; P per fattibilità nelle condizioni autorizzate, senza benchmark aggiuntivo. |
| M03 Alias/backend/accesso | Mapping `qwen3.5-122b`, repliche/load balancing, protocollo/versione API e modalità di identificazione cambi | Alias ed endpoint effettivi per P_alt, accesso dalla postazione prevista; non assumere loopback o SSH | G: mapping e contratto. P: request/response binding; rilevare incongruenze senza fallback. Nessuna chiave nei documenti. |
| M04 Tokenizer | Repo/revisione, implementazione/versione, file e SHA-256, special/added token | Riconfermare pin storici, file caricati e override | G: file/manifest. O: hash e conteggio riproducibile; tenere distinto il contatore canonico R4 comune. |
| M05 Chat template | Byte effettivi, origine, SHA-256 e regola di hashing, kwargs/special token/prompt di sistema aggiunti | Stessi dati, raccordati al vecchio hash senza presumere identità | G/O; P: confronto conteggio input con usage se disponibile e ricerca di differenze; nessun fallback al solo testo. |
| M06 Serving/parser/schema | Software versione/build, avvio/config, parser reasoning e structured-output supportato; vincoli diversi producer/consumer | Riconferma vLLM/config/env, parser e supporto al contratto **producer** | G: config espurgata da segreti, build e parser. O: compatibilità adapter/schema. P: conformità reale distinta P/C. |
| M07 Thinking/output | Modalità e default thinking, controlli/limiti, output totale vs testo finale, nomi campi reasoning | Supporto effettivo per produzione insight; vecchi budget consumer non selezionano quello producer | G: semantica/supporto; P: raw/content/reasoning e termine generazione nelle richieste autorizzate. Non confondere reasoning con `observed_pattern`. |
| M08 Limiti/troncamenti | Precisare input/output/combinato dietro 131072/16384, overhead, tagli e gateway | Riconfermare16384 e limiti input/output effettivi per prompt producer | G: limiti e politiche. O: input completo+output+margin con tokenizer/template effettivi. P: capienza, errori/finish reason, eventuale taglio silenzioso. |
| M09 Sampling/seed | Altri default e parametri supportati/ignorati: seed, top_p/top_k, penalità, stop; `temperature` resta **omessa** | Riconfermare parametri applicabili a P_alt, default, seed e override; T=0 storico non è un nuovo freeze | G: elenco e semantica supportati/ignorati/rifiutati. P: applicazione e variabilità dove prevista; né seed né T=0 garantiscono determinismo. |
| M10 Tracciabilità | Request ID correlabile, response ID, model, usage incl. reasoning, finish reason e fingerprint se disponibili | Riconfermare campi storici e loro semantica corrente | G: schema/esempio già disponibile, assenze esplicite. P: persistenza raw e confronto per richiesta; null/mancante non è zero. |
| M11 Timeout/errori/zero token | Timeout server/proxy/coda, codici e cancellazione, prove di richiesta non generata e token zero | Stesso fabbisogno, per chiamate producer | G: log/documenti correlabili a ID e significato contatori. P: acquisire evidenza su errori eventualmente occorsi; nessun errore provocato o retry fuori quota. Timeout solo non prova mancata generazione. |
| M12 Aggiornamenti | Backend stabile durante finestra? politica di restart/update, notifiche, fingerprint/versione dopo cambi | Riconfermare servizio e policy, non usare PID storici come freeze | G: calendario/garanzie realistiche. P: osservare drift durante attività autorizzata; cambi→sospensione e revisione, non nuova qualifica automatica. |
| M13 Disponibilità/carico | Periodi, manutenzione, rate limit, concorrenza ammessa, code e carico condiviso | Idem per produzione completa; chiarire risorse condivise con altri processi | G: disponibilità W e vincoli. P: latenza per ruolo/blocco inclusa attesa; nessuno speedup assunto dai due server. |
| M14 Stabilità/fattibilità | Nessuna misura corrente: qualifica P e gate C previsti, T5 con margine 20% | Nessuna misura corrente P_alt: conformità completa e latenza produzione; **nessun gate diagnostico 40×3 sul 27B** | G: condizioni operative. P: sole misure negli stadi autorizzati; O: contabilità e calendario. |

Per P e P_alt resta comune il contratto schema insight R4, compresi campi fissi, cap e conteggio canonico col tokenizer 27B senza special token. Per entrambi servono **anche** tokenizer/template del rispettivo servizio per calcolare il prompt completo: i due conteggi hanno scopi diversi. Non cambiare il cap canonico per favorire uno dei producer.

## 6. Consegna e dipendenze

- [Messaggio breve da inoltrare](RICHIESTA_METADATI_QWEN_DA_INOLTRARE_2026-09-15.md): pronto, **non inviato**; richiede dati mancanti o riconferme, non esecuzioni.
- [Checklist futura per ruolo](CHECKLIST_QUALIFICAZIONE_D9_2026-09-15.md): controlli offline, verifiche servizio e stadi del protocollo mantenuti separati; nessuna nuova autorizzazione.
- **03.8:** usare metadati e poi misure per contabilità per modello/blocco, disponibilità W e T5. Firma materiale e collocazione delle otto chiamate alternative nel pilot o in produzione restano passaggi distinti; D9 non seleziona automaticamente `a=1`. Le latenze storiche non sostituiscono misure 122B/P_alt.
- **03.10:** dopo review e nel recepimento seriale, associare P/C al 122B e P_alt al 27B tramite nuove configurazioni improntate, tokenizer/template e ledger; non riattivare il preflight storico e non ereditare fallback 27B. H10 è un candidato letto, non importato né approvato qui.
- **03.15:** recepire serialmente D9 e questo inventario mantenendo visibili “dichiarato”, “storico”, “verificato nel perimetro” e “mancante”; non pubblicizzare una qualifica sulla base di questa consegna. Terra resta descrittivo interno.

Gli hash e i dettagli tecnici mancanti sono **dati da acquisire**, non nuove scelte di ruolo. La scelta della configurazione operativa esatta, l'ordine 1a, la firma 03.8 e l'autorizzazione a chiamare sono invece **approvazioni separate**. La registrazione D9 non dipende dalla loro chiusura. I confronti nuovi con Terra o un consumer 27B richiederebbero una decisione di disegno non compresa nel mandato: non sono nella checklist.

## 7. Fonti e impronte dei documenti consultati

I commit indicano snapshot Git esatti consultati, non certificazioni del servizio. Le impronte seguenti sono ricalcolate localmente sui blob; gli hash tecnici remoti di §4 sono invece attestazioni riportate. Tutti i percorsi sono relativi alla radice repository; per fonti non presenti nel worktree D9 il pin consente la lettura con `git show COMMIT:PERCORSO`, senza importazione.

| ID | Percorso | Commit di consultazione | Byte / SHA-256 | Provenienza e uso |
| --- | --- | --- | --- | --- |
| M0 | `docs/MAINTENANCE.md` | `819b12e97fb94d501032655ec2f226139e6c5ca5` | 19373 / `4a75b0677c5eb09d36274cb36be37a1ec73afb2ca86b274cc36193812465647b` | Copia principale richiesta; regole, non evento servizio |
| M1 | `docs/MAINTENANCE.md` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 20636 / `77b4768c2b6ae1bc27d2e1aaaa56f9c38626add20b2f5e74f6a426eef7a66ec0` | Regole della copia D9 |
| MC | `docs/prompts/Commit_LLM.md` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 2643 / `5488a915b79aee9d703c17aa628b669db1d5c5eaccaf042e72f375366d107623` | Regole commit |
| D | `studio2/fase03/DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 9083 / `fcb113636de80cc87709905324436555e0ba103bd46de3ac079ce0ef7f60f1b8` | Acquisizione decisione 14/09; ruoli approvati |
| C | `studio2/fase03/CONSEGNA_RECEPIMENTO_D9_2026-09-14.md` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 13282 / `3ea739065f1011ed2fd17bface11231f8857dc3f5256d26eff7abcc1d1ef2c77` | Consegna completata 15/09; nessun recepimento anticipato |
| I | `studio2/fase03/IMPRONTE_DECISIONE_D9_2026-09-14.json` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 11169 / `3b95d17ab3b467bebe5d0bda5fa84d8ab63f3ee13f87397e02caf396654af77b` | Manifest D9 storico |
| PR | `studio2/fase03/PROPOSTA_D9_RUOLI_MODELLI_2026-09-14.md` | `95ff8571af02bab79094ed1a6be3f6a7b410c711` | 36141 / `a47f42dda7ee9702c292e34ada6b116ac3c85e42ec3a50e68af97c159f0d0f9d` | Proposta storica 14/09; raccomandazione superata |
| H0 | `studio2/fase03/paper_sections/evidenze_verifica_raccordo_0315/fonte_esterna_HANDOFF_FASE03_2026-09-14_rev02.md` | `a00605862f627710347bd63c49f79a6d0a00135f` | 48244 / `b7d47c75538e12ab129fa17789c241a54d290ad19746cec18ecb53dc1050abff` | Inventario comunicato 14/09, §§4.8–4.9 e5 |
| F | `studio2/fase03/config/pilot_preflight.json` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 11636 / `6bf50982d2ba8040e18c468999a110c426e3b9be217d5d9be5f272df6515f5f5` | Freeze envelope 13/09; esecuzione sospesa |
| E | `studio2/fase03/env/ENDPOINT_8001_16384_RECORD.md` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 23669 / `6424d416d3228898a4e9313b800162441b530bcadd1d7fe2e1b83ee096a2af21` | Avvio 13/09 01:52 CEST; aggiunta 02:05 CEST |
| L | `studio2/fase03/env/start_vllm_8001_16384.sh` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 636 / `fca8ea1c48bd640f28a944ae038e70cf896c3de7b231198e7c3474c374ffa36f` | Script storico 13/09; soltanto letto |
| Q | `phase_b/exp2/qwen/probe/capability_probe.json` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 49891 / `93881b18c1945ac24b0f26318fe7bf559f268b752e1441c32a552db02a2ec6b3` | Probe 08/09 13:26:29.231095 UTC; storico Exp2 |
| QC | `phase_b/exp2/qwen/config.json` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 2379 / `3b58e321c5d09c8e1fdf2f5ddab6bac14f9b537b0febcc294909164f3febcbe9` | Configurazione storica associata a Q |
| QR | `phase_b/exp2/qwen/probe/CAPABILITY_PROBE.md` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 2138 / `39f6d324a1e0db4b33035697327904a28e056f216978b41b0ba3f6c5883a55e5` | Rapporto capability storico Q |
| S | `studio2/fase03/results/provisional_cap_stress/provisional_stress_probe_summary.json` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 4375 / `c9adf2a8f07d9058257cc2c51a00064662874611875a715c716a1f1ea4828368` | Sonda fixture 13/09 00:44:21.793634 UTC, non gate |
| R4 | `studio2/fase03/schema_insight/TEST_RESULTS_qwen_rev004.txt` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 7459 / `a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972` | Log R4 acquisito 14/09; no nuova esecuzione |
| R4V | `studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004.md` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 21288 / `d0e69094953cac7966eda9d1f612b81f44cc8e646151fd2339dba0b7ca88ec8e` | Verifica 14/09 sul target 3c64390 |
| R4C | `studio2/fase03/schema_insight/DECISIONE_SCHEMA_INSIGHT.md` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 9671 / `6923e8d428f1aee0fa2b8adc3584601ece123894b4c8b6b81ba60c79545c8520` | Contratto schema insight vigente nel pin |
| PS | `studio2/fase03/piano_statistico/PIANO_STATISTICO.md` | `6aaa5b3eebfed4ba502c25c0443caabd0051af21` | 81490 / `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a` | Rev10 del 14/09; solo stadi/criteri, inventario nuovo superato da H0/D |
| B | `studio2/fase03/piano_statistico/BUDGET_RISORSE_REV10.md` | `6aaa5b3eebfed4ba502c25c0443caabd0051af21` | 8528 / `8d909d8f851b8b9c633687989d3a9f3221230b48e1f0595278e075556d283887` | Rev10; contabilità vigente del riferimento D9 |
| DH | `studio2/fase03/piano_statistico/DELTA_HARNESS_03_10.md` | `aaba893dff8c62f9f9281eec7423eee020235e03` | 7108 / `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e` | 14/09; norme stadi, inventario nuovo superato da H0/D |
| H10 | `studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md` | `6268437b8b64288b50ad5f7c924e1fcab85b27d3` | 10570 / `5bd46b02f3d2b3f8b64de1aa0b34a82276e5a561e80192bf7ff23edd45d64684` | 15/09; candidato correzioni in review, non qualifica |
| H10R | `studio2/fase03/harness/REPORT_CORREZIONI_HARNESS_03_10.md` | `6268437b8b64288b50ad5f7c924e1fcab85b27d3` | 14207 / `ac97694744a1a0c931573c663ba321216be8ece05041facab53d3afe0fe19b28` | 15/09; limiti delle sole prove offline |
| P15a | `studio2/fase03/paper_sections/protocol.md` | `a00605862f627710347bd63c49f79a6d0a00135f` | 17418 / `ddcaf1c2790d7e3fe966ed80bb91d3ae7316090d4b9dc554b85f8dd030ca5468` | Pubblicato 14/09, anteriore a D9 |
| P15b | `studio2/fase03/paper_sections/method.md` | `a00605862f627710347bd63c49f79a6d0a00135f` | 7557 / `db697de1d124150bf8e754154c21a2d07cfaa0a79034bf32d3a6c5a449331938` | Pubblicato 14/09, anteriore a D9 |
| P15c | `studio2/fase03/paper_sections/threats.md` | `a00605862f627710347bd63c49f79a6d0a00135f` | 9221 / `915b7484ee3bff65c2633405db027c3e797d927bc56548238da2d631c06b2c35` | Pubblicato 14/09, anteriore a D9 |

H0 è la copia pubblicata del handoff originariamente locale; la coincidenza con `/Users/luker/fot-tep/studio2/fase03/HANDOFF_FASE03_2026-09-14_rev02.md` è verificata per SHA-256, non trattata come seconda attestazione. R4 si riferisce al target `3c64390bc4dd58c48cc4e1e388a38989b32b3143`; log e verifica sono stati acquisiti nel commit `43b31afc1ff271594cb4bd21a39fa4469a8c83bc`. Il tag schema già pubblicato `studio2-fase03-schema-insight-frozen-001` punta a quel target; nessun tag creato o spostato qui. Il file F mantiene limiti e logica storici superati in parte da PS/DH: non viene assunto come protocollo operativo corrente.

## 8. Rapporto dei controlli documentali

Controlli del preparatore, svolti il 15 settembre 2026. Nessuna verifica indipendente scientifica, chiusura di sottofase, misura del servizio o GO viene dichiarata.

| Controllo | Esito |
| --- | --- |
| Riferimenti del nuovo inventario | 26 percorsi risolti nei commit esatti; dimensioni e SHA-256 verificati sui blob Git. |
| Manifest D9 storico | Tutte le 17 fonti del manifest I verificate ai rispettivi pin, senza aggiornarle alle copie parallele. |
| Preservazione | Proposta PR, decisione D, consegna C e manifest I byte-identici al commit D9 iniziale; proposta identica anche al commit 95ff857. Nessun file preesistente modificato o eliminato. |
| Handoff | Copia originale locale e snapshot pubblicato H0 byte-identici: 48.244 byte, SHA-256 riportato in §7. Non due attestazioni indipendenti. |
| Link e perimetro | 6 link relativi dei tre documenti risolti; nessun conflitto Git o credenziale evidente. Tre soli file Markdown nuovi; nessuna coppia MD/HTML o struttura di cartelle cambiata, quindi nessun aggiornamento di indici/walkthrough. |
| Guardiano documentale | `python3 docs/test_explanation.py`, prima e dopo: 35 test, 14 fallimenti storici, 1 skip, 0 errori, exit code 1. Stessi identificatori di fallimento e subtest: **non peggiorato, non PASS**. |
| Diff | `git diff --check` e `git diff --cached --check`: nessun rilievo dopo rimozione degli spazi finali. Selezione esplicita dei soli tre nuovi documenti. |
| Main remoto alla chiusura dei controlli | Nuova lettura di `origin` effettivo: `a00605862f627710347bd63c49f79a6d0a00135f`, invariato rispetto al preflight. Nessun fetch/import del candidato harness, push, merge o tag. |

Il confronto del guardiano conserva le stesse 14 righe `FAIL:` (compresi subtest) e lo stesso riepilogo già elencati nel manifest I. Lo skip resta `TutorialChecks`: legacy part-1 walkthrough assente in questa copia. SHA-256 della sequenza ordinata di righe skip, `FAIL:` e `FAILED (...)`, unite da newline e con newline finale: `f08e08be0b2daa7dfde1404a999abb923ce62f2c827904e4c9994ce48d938712`. Nessun fallimento storico è corretto o mascherato da questo incarico.

Impronte degli altri due documenti di questa consegna (il commit contenente l'inventario identifica anche i suoi byte, evitando un hash autoreferenziale):

| Documento | Byte | SHA-256 |
| --- | --- | --- |
| `RICHIESTA_METADATI_QWEN_DA_INOLTRARE_2026-09-15.md` | 2820 | `8aa7d3f4ac51ef6e78e4be9cbf2bebdfed0dbb58685471019fdbc565cf466993` |
| `CHECKLIST_QUALIFICAZIONE_D9_2026-09-15.md` | 12952 | `7b35f6cbb5575e7a3c23b7df88539c99ae0161885bf8115352be9c5de8c80acc` |

La qualifica dei servizi, i metadati non disponibili e il recepimento operativo restano pendenti. Questa consegna contiene solo inventario, richiesta non inviata e checklist; non tocca le configurazioni canoniche né il piano, l'harness, le bozze paper o il walkthrough delle altre finestre.
