NON OK con rilievi sul solo delta offline — Modello dichiarato: Codex, basato su GPT-6; finestra 01a0a579-3fd7-7461-8c26-5449bd3d2b7a.

# Verifica D9 indipendente della preparazione

15 settembre 2026, Europe/Rome. Mandato: eseguire PROMPT_VERIFICA_D9.md in una finestra separata, senza modificare il candidato. Questo verbale formalizza **R-D9-01 e R-D9-02**, entrambi P2. Nessun GO, qualificazione del servizio, freeze 03.10 o autorizzazione scientifica.

## 1. Identità, indipendenza e conservazione

| Oggetto | Identità verificata |
| --- | --- |
| Tecnico esaminato | `6a8031b25aa1208047d79cc7f030bf9cf7841e67` |
| Tree tecnico | `bb3872d8fc1cbddebb4b055a8edad372e5aad430` |
| Worktree originale | `/Users/luker/fot-tep-harness-d9`, branch `codex/studio2-harness-d9` |
| HEAD documentale | `08670fb4793ecec99754a73c6a91a51c1c372960`, tree `8430d8c0a9e1602abcd41730a9b2e0660ba0627e` |
| Base documentale D04 | `5886c6f9d078ee624deaec08763e04c14e96e4f0` |
| Contratto/test-first | `62343a7bb526d5285df547ceb8f5ea0341515cef` |
| Antecedente tecnico | `aae29a908356e4a4842a214fdc3db9bff26ec3ca`, tree `4e1f7f043725d64fb16b7d1c921c619bce8d1bb3` |
| Manifest candidato | SHA-256 `356e87d29028a80488a6acfde66b7551bacde94481eba3389922e04124625668` |

✅ Il successore documentale aggiunge cinque file di consegna, prompt, report e controlli; non cambia il tecnico. Il commit test-first cambia, fra i Python, soltanto test_d9.py. I 141 membri del manifest coincidono per byte e SHA-256; coincidono anche tutti i 211 Python inventariati in TESTED_BYTES. Inventariato non significa eseguito. Le sette fonti di SOURCES.json coincidono con i blob Git dei commit indicati. Prove: [integrity.json](evidence/integrity.json), [tested_bytes_check.json](evidence/tested_bytes_check.json), [scope_and_preservation.json](evidence/scope_and_preservation.json).

✅ I test sono stati eseguiti sulla copia estratta con `git archive` dal tecnico, in `work/candidate` della sede di review; il confronto usa `work/antecedent`, estratto dal tecnico aae29a9. Nessun nuovo worktree Git è stato creato. È conservato anche [l'archivio completo del candidato](candidate_6a8031b.tar.gz). La sede di review è `/Users/luker/Documents/Codex/2026-09-15/esegui-integralmente-il-prompt-di-review/outputs/d9-review`.

✅ Controllati stato locale, branch, HEAD/tree, worktree e URL effettivamente configurato per origin (`https://github.com/sorrentinoluca/fot-phd.git`), senza contattare il remoto. L'osservazione dei processi e `lsof` non ha individuato un writer sui file harness originali; non costituisce un lock globale. La conservazione finale è documentata in [preservation_final.json](evidence/preservation_final.json): stato D9/D04 pulito e impronte originali confrontate. Il perimetro delle 53 modifiche tecniche è in [delta_paths.json](evidence/delta_paths.json): nessuna modifica agli artefatti congelati del primo studio o alle coppie walkthrough MD/HTML.

⚠️ Questa è una finestra distinta dalla preparatrice `01a0a53e-927d-7493-a50a-34617bbac13f`; l'ID corrente è riscontrato in CODEX_THREAD_ID. Ho ricostruito fonti, hash, risultati e sonde senza assumere verificati quelli della preparatrice. Il modello è dichiarato dal contesto come Codex basato su GPT-6: variante, identità dei pesi e backend realmente servito non sono attestabili qui. Non è dimostrata la diversità di modello dalla preparatrice; pertanto non rivendico la garanzia di “altro modello” di Verifica_LLM.md. Sono indipendenti la finestra e la ricostruzione comportamentale, non l'ambiente, il framework delle fixture o la famiglia del modello. Non sono stati impiegati sottoagenti.

Le interruzioni della conversazione sono distinte dai test. Alla prima ripresa la discovery era ancora in esecuzione nel processo originale; non è stata rilanciata o sovrascritta. Alla successiva sospensione per possibile duplicazione, tutte le suite erano concluse e nessun processo di test era attivo. Il mandato dell'autore è stato poi ripreso per formalizzare e consegnare questa review. Nessun rilievo preliminare era un verbale già emesso.

## 2. Fonti e precedenze

Letti MAINTENANCE prima del lavoro, Prompt_LLM e Verifica_LLM, walkthrough studio2 §0, AUDIT_GUIDE §§5–13 per il metodo di riscontro, skill fot-tep-harness-lessons e lessons-and-evidence; contratto D9 prima del codice e appendice D9_FIELD_CONTRACT; report D9; contratti D03/D04 e contratto di esecuzione/ripresa; contratto schema R4 e adattatore pinnato. L'handoff rev03 è stato usato per lo stato operativo, senza sostituire le fonti.

Letti nelle versioni identificate i record D9, inventario servizi, checklist, richiesta metadati non inviata, budget rev10, DELTA_HARNESS e sezioni pertinenti del piano statistico (in particolare §§7.2, 10–11, 16). Le copie sono in [references](evidence/references), con impronte nel manifest di review. Il piano completo è acquisito e improntato; non è stata rifatta la review statistica né quella del primo studio. Volume di lettura: alcune decine di migliaia di parole tra contratti, fonti e codice; non è un conteggio esatto dei token fatturati.

✅ D9 approva P=C=122B, P_alt=27B con libreria completa16, consumer122B fisso nello swap, Terra storico descrittivo interno. Non approva fallback, consumer27B, fattoriale, nuovi casi o decisioni dai risultati.

✅ R4 resta al target `3c64390bc4dd58c48cc4e1e388a38989b32b3143`: libreria16, due insight per fault e14peer per ricevente; Normal non produce insight. Il contatore canonico senza special token è distinto dal conteggio chat del servizio. L'ordine1a esige propria approvazione; non deriva da label_space, mapping o derangement. Questi artefatti03.7 non sono stati rigenerati.

✅ Il blob storico S è stato letto e acquisito separatamente: [historical_S.json](evidence/references/historical_S.json), SHA-256 `c9adf2a8f07d9058257cc2c51a00064662874611875a715c716a1f1ea4828368`, riporta4 richieste totali,3 inferenze completate e nessun gate autorizzato. Non è stato riconciliato, migrato, duplicato o azzerato alcun consumo scientifico.

✅ Le due review D04 restano riferite esclusivamente ad aae29a9. Sono preservati i verbali Codex (21.340 byte, `2fc9ed8e3303a779833f1b1dced7f9a70022603118d985280722bed0156a8fef`) e Claude (11.864 byte, `0ce2cb9485e5047c5e87eed6f69d0f8ddd3e1b09a2c4a005f0a42e92ef4dc83c`). I risultati storici Codex128/128 e163/163, e Claude127 verdi+1 env-bloccato fra128, non sono risultati D9 di questa finestra.

## 3. Prove effettive

Ambiente: Anaconda Python3.13.9, SQLite3.51.0, macOS26.6.2 arm64; [runtime.json](evidence/runtime.json). `PYTHONDONTWRITEBYTECODE=1`; fixture isolate, SDK/server e contatori fittizi. Le fixture runner vietano socket. Non sono stati chiamati servizi, eseguite inferenze dello studio, simulazioni TEP, pilot o prodotti insight reali. Non sono state installate dipendenze.

| Prova | Metodi | Fallimenti | Errori | Skip | Secondi | Log |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| Suite mirata fornita | 145 | 0 | 0 | 0 | 458.029 | [targeted.log](evidence/targeted.log) |
| Discovery completa fornita | 180 | 0 | 0 | 0 | 465.880 | [discovery.log](evidence/discovery.log) |
| D9 finale fornito | 17 | 0 | 0 | 0 | 7.143 | [d9.log](evidence/d9.log) |
| Stesso D9 finale su aae29a9 | 17 | 3 | 14 | 0 | 1.318 | [antecedent.log](evidence/antecedent.log) |
| Sonde indipendenti finali U01–U08 | 8 | 3 | 0 | 0 | 8.862 | [independent_probes.log](evidence/independent_probes.log) |
| Stesse U04–U07 su aae29a9 | 4 | 2 | 0 | 0 | 5.374 | [independent_probes_antecedent.log](evidence/independent_probes_antecedent.log) |
| Guardiano documentale | 35 | 14 | 0 | 1 | 0.078 | [guardian.log](evidence/guardian.log) |

Le suite mirata, discovery e D9 sono sovrapposte: **non si sommano**. I conteggi sono metodi unittest, distinti da subtest, assertion e processi. Il risultato dei test indipendenti con assertion fallite è la riproduzione dei rilievi, non un test d'ambiente abortito.

✅ I byte finali di test_d9.py, SHA-256 `a5f9598f2c1e4b533617415421a985331276e274537abc509f9920a807a40fe5`, sono stati usati anche contro l'antecedente. I3 fallimenti riguardano approvazione nominale senza D9, temperature122B e provider principale nell'alternativo; i14 errori riguardano API D9 assenti. **Non sono17 regressioni D04.**

✅ CLI in modalità piano: run_pilot=0, producer_probe=0, prepare_gate=3 per input sospesi. Il test D9 pending verifica separatamente che gli ingressi esecutivi coperti non creino ledger. Compilati in memoria i98 file dell'inventario della preparatrice: zero errori; una prima scansione autonoma di79 file, con esclusioni diverse, resta conservata e non è sommata. Prove: [cli_plans.json](evidence/cli_plans.json), [compile_same_scope.json](evidence/compile_same_scope.json).

### Adattamenti e limiti d'ambiente

- I test forniti sono stati eseguiti senza modificarne i byte. Le loro fixture D9 sostituiscono i pin reali R4 e la storia S con file sintetici e fonte0/0: questo permette di esercitare il codice, non qualifica asset/tokenizer o riconciliazioni reali.
- C01/D02 impostano pilot nelle fixture che devono raggiungere la conformità alternativa. D01 scientifico legacy senza D9 ora rifiuta prima della rematerializzazione; il positivo del ledger generico rimane. Queste variazioni dichiarate sono coerenti con la nuova barriera e non sono ripetizioni letterali delle vecchie fixture D04.
- La dipendenza legacy `/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate` è disponibile; il test verifica commit `0c8157f23bee49a3a5a2df648525c34706da29d7`, tree `a1573b49615a875f24ee97f9f1cd4bab399be93d` e pulizia. Nessun env-bloccato nelle suite completate qui. Restano necessarie tali dipendenze per riprodurre altrove.
- La nuova sonda usa il supporto RunnerRevisions per preparare input validi; le mutazioni, assertion e il controllo con SDK reale fittizio sono del revisore. Le copie dei ledger/raw e degli output sono conservate. I riferimenti assoluti interni delle fixture documentano i percorsi originali temporanei; per rigenerarle si usa lo script, senza riscriverne retroattivamente gli hash.
- Il primo lancio delle sonde importava la classe TestCase nel namespace unittest, raccogliendo anche RunnerRevisions. È stato fermato dopo i risultati U01–U08 e alcune prove aggiuntive. Script/log interrotti sono conservati; il namespace è stato corretto soltanto nello script esterno del revisore e i8 metodi sono stati rieseguiti integralmente. Un'ulteriore revisione ha aggiunto selezione del target e osservazioni recuperabili; gli stessi byte finali sono stati usati sui due target dove applicabile.
- Non sono stati rilanciati indiscriminatamente i launcher storici V/W/Y/Z/X. Le suite richieste includono le regressioni interessate; non viene rilasciata una nuova chiusura complessiva della storia R01–D04.

## 4. Rilievi riproducibili

### R-D9-01 — P2: placeholder con spazi accettato come metadato completo

❌ **Sorgente:** `studio2/fase03/harness/d9.py:34–35`, usata da validate_config alle righe118–121. `_text` usa strip per verificare la stringa non vuota, ma confronta il placeholder con `value.upper()` senza strip. `PENDING` viene rifiutato; ` PENDING ` viene accettato.

**Riproduzione:** U01 completa conformità e resume con revisione fixture esplicita; U02 imposta weights_revision=PENDING, con riferimento documentale e approvazione fixture coerenti, e ottiene rifiuto prima di intenti/invii. U03 cambia solo quel valore in ` PENDING `, aggiornando allo stesso modo hash del documento e approvazione fixture: la conformità passa, con **8 intenti,8 invii fittizi e8 raw**. L'assertion che richiedeva HarnessError fallisce. Nessun hash o byte runtime è alterato.

**Impatto:** contraddice il requisito D9 che metadati mancanti/placeholder restino bloccanti anche con una configurazione nominalmente approvata. L'approvazione dell'hash non trasforma una revisione mancante in una revisione documentata. Non dimostra un bypass del config pending consegnato, né disponibilità dei servizi.

**Correzione richiesta:** applicare coerentemente il controllo dei sentinel sul testo normalizzato, senza promuovere i placeholder a metadati validi; conservare positivi e rifiuto preventivo. Nessuna correzione è stata applicata. Questo controllo è nuovo in D9: il medesimo documento D9 non è un input supportato dall'antecedente, quindi non viene inventato un confronto comportamentale equivalente.

Prove: [independent_probes.py](evidence/independent_probes.py), [log finale](evidence/independent_probes.log), [osservazioni U03](evidence/probe_fixtures/test_U03_whitespace_pending_metadata_must_refuse/observations.json), con fixture e database nella stessa cartella.

### R-D9-02 — P2: file tokenizer non riconfermato alla nuova riserva D9

❌ **Sorgente:** `studio2/fase03/harness/d9.py:93–94,183–219`; il controllo dei file è in r4_counter, separato da validate_binding. Il binding D9 verifica che r4_snapshot sia assoluto e che i pin dichiarati coincidano, ma non la permanenza dei file. Il Provider consumer ricontrolla configurazione e INTENT, non i file tokenizer.

**Riproduzione:** la preparazione ordinaria produce8 richieste producer valide, autentica i prompt e crea il binding budget_probe. La sonda esterna ferma il runner prima della prima riserva consumer. U04, con file intatti, riserva correttamente il primo consumer. U05 elimina tokenizer.json dalla sola fixture, lasciando config, approvazioni, binding e digest intatti: la riserva è ancora accettata e il contatore sale8→9. U06 osserva lo stesso comportamento riaprendo PilotLedger. U07 dimostra che, con la medesima perdita prima dell'ingresso ordinario, run_budget_stage rifiuta e resta a8; U08 conferma che l'alterazione del documento27B viene invece rifiutata dalla riserva, senza invii.

**Confine del trasporto:** [transport_snapshot_probe.py](evidence/transport_snapshot_probe.py) usa gli oggetti già autenticati, il vero `_tracked_call → execute_request → Provider.call` e soltanto l'SDK fittizio. Dopo la perdita del file, osserva **1 invio SDK fittizio,9 intenti cumulativi e raw persistito**. Non è una chiamata privata diretta al client che scavalca il ledger. [Risultato](evidence/transport_snapshot_probe/result.json) e fixture sono recuperabili.

**Limiti del rilievo:** nella fixture R4 e servizio usano lo stesso snapshot sintetico; questa prova non isola due directory reali distinte e non dimostra che il prompt già calcolato sia sbagliato. Dimostra la mancata riconferma della recuperabilità del tokenizer autorizzato al punto della nuova decisione. L'ingresso ordinario con snapshot già mancante è protetto. Il caso diretto era presente anche in aae29a9: **non è una nuova regressione D04** e non revoca il suo OK storico entro il perimetro verificato. Rimane però non soddisfatta la copertura dichiarata dal nuovo D9_FIELD_CONTRACT per snapshot normativo e riserve dirette.

**Correzione richiesta:** proteggere questo prerequisito alla decisione di riserva/riuso D9, oppure conservare e autenticare una copia durevole dei byte già verificati che soddisfi il contratto di recuperabilità. Non basta il path assoluto e non va trasformato il dato mancante in un'approvazione. Nessun cambiamento runtime è stato fatto.

Prove differenziali: stessi byte di independent_probes.py, U04–U07 su aae29a9:2 positivi,2 assertion fallite,0 errori. [Log antecedente](evidence/independent_probes_antecedent.log). La restrizione ai quattro metodi è esplicita: le sonde dei documenti D9 non sono applicabili a quell'API.

## 5. Copertura positiva e limiti scientifici

La [matrice dei campi e dei percorsi](evidence/MATRICE_COPERTURA_D9.md) segue acquisizione, persistenza, rilettura e decisione per tutti i gruppi di D9_FIELD_CONTRACT; distingue test da ispezione del codice.

✅ Nei casi verificati: ruoli/stadi/provider non si scambiano; temperature122B è assente anche dai payload dell'adattatore vero con SDK fittizio e null/0/0.6 non la rendono ammissibile; conteggio R4 e chat sono separati; la conformità costruisce la libreria prima dei prompt14peer; primaria e alternativa sono autenticate separatamente; swap conserva i casi forniti e consumer122B; PENDING blocca, deferred non inventa stadi successivi e pilot richiede PASS alternativo.

✅ Contenuto provider, fonti documentali, autorizzazione e configurazione persistita sono ricontrollati nei casi coperti, anche dopo restart e nelle riserve. Restano transazioni D04, inventario cumulativo, quote e prove D03; nessuna migrazione di schema, backfill o riscrittura dei consumi. Il positivo di contabilità conta ogni intento una volta e aggrega P+C a122B.

⚠️ server_contract produce `DOCUMENTED_NOT_LIVE_VERIFIED`; alias e hash documentali non provano i pesi né zero token. Metadati effettivi, file/tokenizer reali, qualificazioni, ordine1a, collocazione/contabilità alternativa, riconciliazione S, autorizzazioni esecutive, insight reali, capienza e T5 restano pendenti. Il config consegnato è bloccato. La helper swap non seleziona il campione definitivo e non avvia lo studio. Nessun risultato offline viene convertito in qualifica scientifica.

⚠️ **Guardiano storico NON PASS:**35 test,14 fallimenti,1 skip,0 errori. Gli identificativi dei14 FAIL, inclusi i subtest, coincidono con guardian_comparison.json del candidato. Non è PASS e non dimostra correttezza del delta. Il confronto nominativo è in [guardian_comparison_independent.json](evidence/guardian_comparison_independent.json); il log completo è conservato. Nessuna correzione alla documentazione storica.

## 6. Consegna e conclusione

**NON OK sul delta offline per R-D9-01 e R-D9-02.** I risultati positivi delle suite fornite non coprono i due confini riprodotti dalle sonde indipendenti. La decisione non dipende dal NON PASS storico del guardiano e non trasferisce o revoca automaticamente gli OK di altri tecnici.

Tutti i file creati appartengono alla sede di review: verbale, archivio del candidato, script esterni, log, fixture/raw, riferimenti acquisiti e inventario. [COMANDI.md](evidence/COMANDI.md) contiene riproduzione e adattamenti; [MANIFEST.json](MANIFEST.json) elenca byte e SHA-256 dei file conservati. Il manifest esclude se stesso e CONSEGNA.json per evitare circolarità; quest'ultimo lega manifest e verbale alle rispettive impronte. Gli hash attestano integrità locale, non pubblicazione remota.

Nessuna correzione runtime, commit, push, merge, tag, invio a terzi, modifica delle coppie condivise o scrittura su ledger scientifici. La review termina a questo verbale e alle sue prove recuperabili.
