OK

# Verifica indipendente delle acquisizioni e del recepimento documentale D9 — 03.8

**Oggetto:** candidato `8a20c125bd294191c67ebdbf571832b1e32ac0f1`, tree `f58eedf88d8c9c30767425c945b5ee5c421cf0b7`; acquisizioni da 16f2274 e delta documentale dalla base immediata dc4d656. Le due acquisizioni sono integre e il recepimento D9 rispetta la decisione dell'autore senza estenderla. Nessun rilievo bloccante individuato nel perimetro richiesto.

Il record D9 è ora acquisito in 03.8 e recepito documentalmente nel candidato locale. **Restano pendenti recepimento eseguibile, identità/configurazioni, qualificazioni e fattibilità.** Non occorre una nuova approvazione dei ruoli. L'OK storico su 9a56d12 è preservato, non ripetuto né automaticamente esteso: il presente esito riguarda le acquisizioni e il nuovo delta D9.

## Revisore e indipendenza effettiva

- Codex, modello esposto **gpt-6-astra**, provider **openai**, effort esposto **high**.
- Task/sessione **01a0a1d9-8ccd-7893-b504-4fde93380ea0**.
- Fonte verificata dei metadati: `session_meta` e ultimo `turn_context` in `/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T23-36-24-01a0a1d9-8ccd-7893-b504-4fde93380ea0.jsonl`; letti solo i campi di identità pertinenti, senza dedurli dal nome della finestra o dal verbale acquisito.
- Worktree del revisore: `/Users/luker/fot-tep-verifica-recepimento-d9-038`, **detached HEAD** al candidato esatto; repository Git comune `/Users/luker/fot-tep`.
- Preparatore distinto: `/Users/luker/fot-tep-allineamenti-038-r1-r4`, branch `codex/studio2-allineamenti-038-r1-r4`.
- **Limite dichiarato:** questa sessione ha già emesso NON OK su 4503cb6 e OK su 9a56d12, e conosce il record D9 dalla review precedente. È indipendente dal preparatore, ma non è una nuova task senza contesto né una seconda opinione di altro modello. Non ha preparato il delta D9 o i suoi record di acquisizione. Nessun sottoagente impiegato.

Il mandato è il prompt fornito dall'autore, `PROMPT_VERIFICA_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md`, letto nella copia preparatrice e riferibile alla consegna successiva 7d9100a. Non è parte del candidato. Non è stata richiesta o eseguita alcuna modifica del candidato: unica scrittura nella copia isolata, il presente verbale non tracciato.

## Preflight, base e genealogia

Preflight della copia preparatrice: pulita a **7d9100a4d2c3f8dd8f61e4f9316ebd8549c1da90**, tree `b72ea479f133d1e86fd2963986155d8726908512`; tale HEAD è stato distinto dal candidato. Creata la copia detached sul commit richiesto e verificati HEAD/tree/stato pulito prima della review. Nessun AGENTS.md applicabile trovato nelle directory antenate e nella catena di destinazione del verbale.

`origin/main` e `git ls-remote origin refs/heads/main` coincidono a **a00605862f627710347bd63c49f79a6d0a00135f**, come nella preparazione: nessun avanzamento remoto osservato. Nessun pull, merge o rebase. Il main locale è un'altra ref, `4f98a2973d2e1ca7932f19c34e9dd4c0498b8b43`, e non è stato mosso. Principale e cantieri harness sono rimasti fuori dalle scritture; le copie preparatrice e sorgente D9 sono risultate pulite anche al controllo successivo.

| Passaggio | Commit | Parent unico | Tree |
| --- | --- | --- | --- |
| Consegna R1–R4, base delle acquisizioni | `16f227439357b07b7dc945f67ab5a4368c12b684` | `9a56d12d0633a0c9790c48792182f26fc6eb424a` | `4b65ae9805a0e88c189d4516f03c38d46fbc61a1` |
| Acquisizione OK | `5b784219b08de1249636536ac98e9a546b4d4577` | `16f227439357b07b7dc945f67ab5a4368c12b684` | `998060863396b729deb88888c424c6f6bd968879` |
| Acquisizione D9 / base immediata | `dc4d6560af73579300e33a0a81fc9c3b4316722d` | `5b784219b08de1249636536ac98e9a546b4d4577` | `6d7466e07190d4294b73d24539b6a89a2b214560` |
| **Candidato esaminato** | `8a20c125bd294191c67ebdbf571832b1e32ac0f1` | `dc4d6560af73579300e33a0a81fc9c3b4316722d` | `f58eedf88d8c9c30767425c945b5ee5c421cf0b7` |
| Consegna successiva, esclusa dal delta candidato | `7d9100a4d2c3f8dd8f61e4f9316ebd8549c1da90` | `8a20c125bd294191c67ebdbf571832b1e32ac0f1` | `b72ea479f133d1e86fd2963986155d8726908512` |

Il successore 7d9100a aggiunge soltanto consegna e prompt. L'OK R1–R4 resta riferito al candidato **9a56d12d0633a0c9790c48792182f26fc6eb424a**, tree **e35e5ca661325657715dce6723e4e8ec09540101**. Conservata la precedente catena 4503cb6 → 2520e7a → 1a21fd2 → 9a56d12 → 16f2274.

## Acquisizioni e preservazione: riscontri indipendenti

| Verifica | Esito | Fonte, metodo e conclusione |
| --- | --- | --- |
| Acquisizione OK, 16f2274→5b78421 | ✅ | Due soli file aggiunti: verbale e record di acquisizione. Copia del verbale confrontata byte per byte con l'originale assoluto fornito e il blob 5b78421: **20.816 byte**, SHA-256 `9248c42572a20388ddf5af976840e68fdc908e545312a63234167778ce53a256`. Provenienza, candidato/tree e limite di indipendenza trascritti correttamente. Nessuna estensione del verdetto. |
| Acquisizione D9, 5b78421→dc4d656 | ✅ | Tre blob agli stessi percorsi `studio2/fase03/` più `ACQUISIZIONE_D9_ALLINEAMENTI_03_8.md`; nessun altro delta. Confrontati byte del candidato, blob di acquisizione e blob sorgenti **aaba893dff8c62f9f9281eec7423eee020235e03**. Coincidenza completa dei tre file; due voci `artifacts` del JSON corrispondenti. Il JSON non si auto-impronta: il suo hash è nel record di acquisizione. |
| Assenza di fusione D9 | ✅ | aaba893 non è antenato di 8a20c12 (`merge-base --is-ancestor`, exit 1); parent singolo dc4d656 e delta selettivo confermano che non è stato incorporato il branch D9. Nessuna proposta o fonte storica importata per completare il checkout. |
| Preservazione della cartella statistica | ✅ | Enumerati con `git ls-tree` **47 file preesistenti a 16f2274**; insieme coincidente con l'inventario e tutti byte-identici ai blob. Inclusi NON OK, report/manifest storici, OK statistico, matrice e consegna tecnica pregresse. NON OK ancora **22.063 byte**, SHA-256 `52944646527d0e73d6508ae53669f47f5e8661050ff777c75a448ca535ca9c13`. |
| Preservazione rev.10 | ✅ | Letto il manifest originario: **19 files +6 inputs_read**. Tutti verificati per dimensione/SHA-256 e byte-identità con **51782e8c40069c0a2310afafc36907a61d517ff6**. Piano, budget, atto da sottoscrivere, manifest e delta harness non sono riscritti per introdurre D9 retroattivamente. Nessun test statistico eseguito. |
| Perimetro recepimento, dc4d656→8a20c12 | ✅ | Esattamente **2 M +5 A**: piano generale, APERTURA e cinque record 03.8. Nessuna modifica/importazione di codice o configurazioni, candidati/correzioni harness R01–R10, paper_sections 03.15 o walkthrough MD/HTML. |

Originale dell'OK verificato: `/Users/luker/fot-tep-verifica-correzioni-allineamenti-03-8-rev10/studio2/fase03/piano_statistico/VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md`.

| Blob D9 acquisito, sotto studio2/fase03 | Byte | SHA-256 |
| --- | ---: | --- |
| `DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md` | 9083 | `fcb113636de80cc87709905324436555e0ba103bd46de3ac079ce0ef7f60f1b8` |
| `CONSEGNA_RECEPIMENTO_D9_2026-09-14.md` | 13282 | `3ea739065f1011ed2fd17bface11231f8857dc3f5256d26eff7abcc1d1ef2c77` |
| `IMPRONTE_DECISIONE_D9_2026-09-14.json` | 11169 | `3b95d17ab3b467bebe5d0bda5fa84d8ab63f3ee13f87397e02caf396654af77b` |

## Coerenza del nuovo delta rispetto alla decisione D9

Letti integralmente diff normativo, due nuovi successori, record D9 e sua consegna/matrice; confrontate le sezioni correnti pertinenti del piano e APERTURA. La fonte autorizzativa è il record ai §§1–2, con limiti §§4–5; la consegna D9 §§2–3 distingue i recepimenti e i residui. Il report del preparatore è stato trattato come oggetto da verificare, non come prova primaria.

| Controllo | Esito | Evidenza e conseguenza |
| --- | --- | --- |
| Cinque stati distinti | ✅ | Intestazione e D9 del piano, APERTURA, `MATRICE_RESIDUI_03_8_DOPO_D9.md` e stato del manifest concordano: ruoli approvati; record acquisito; recepimento documentale locale preparato, review pending nel candidato; recepimento eseguibile pendente/non attestato; identità/configurazioni/qualificazioni/fattibilità pendenti. “Completato” per la redazione locale non implica review già ottenuta o integrazione in main. |
| Ruoli e swap | ✅ | P=C=122B, P_alt=27B, **libreria completa di 16 insight**, consumer 122B fisso sui medesimi casi; nessuna libreria mista o limitata ai quattro fault della misura. Piano §8.4 e D9, matrice e consegna successiva corrispondono al record §§1–2. |
| Terra e fallback | ✅ | Terra soltanto storico descrittivo interno, separato dalle nuove stime, senza nuove chiamate o pooling. Il 27B non è consumer fallback. I riferimenti storici a 2.4T/Terra o al piano B non tornano autorizzazioni correnti; gli impedimenti richiedono sospensione, senza cambi automatici. |
| Nessuna nuova scelta D9 | ✅ | Le diciture correnti del piano passano da registro in acquisizione a record acquisito/recepito. Le vecchie fotografie, compresa la consegna D9 “recepimento pendente”, restano temporalmente proprie e non prevalgono sui successori. Nessuna riapprovazione richiesta e nessuna attribuzione retroattiva alla rev.10. |
| Label, firma e autorizzazioni | ✅ | **Ordine label 1a non approvato**, firma materiale 03.8 separata, nessuna autorizzazione a pilot/chiamate e nessuna qualificazione dedotta da nomi nominali o operatività dichiarata. Esplicito in D9 corrente, matrice e consegna tecnica. |
| Parametri e quartetto swap | ✅ | Nessuna nuova revisione, endpoint, temperatura, metadato tecnico, capienza, budget o calendario inventati nel delta. `a`, riusi, X/Q e quartetto dello swap non vengono scelti: i successori riprendono la distinzione della consegna D9 fra rintraccio delle scelte pre-specificate, dati da acquisire e decisioni davvero ulteriori. Non deducono il quartetto da D11. |
| Ledger e contatore R4 | ✅ | P=C implica aggregare richieste distinte sul 122B senza duplicazioni, non azzerare il ledger o aggiungere quote. Budget/riserva/hard stop/R restano nella fonte intatta. Il contatore canonico e i cap R4 restano quelli congelati, distinti da tokenizer/template e capienza effettivi dei servizi; il consumer 122B non li sostituisce automaticamente. |
| Precedenze e sottofasi chiuse | ✅ | Matrice e consegna successive mantengono **freeze statistico → 03.11/OOD → chiamate dopo gli altri GO**. L'harness eseguibile resta prerequisito dei rispettivi stadi operativi, senza diventare dipendenza circolare del freeze statistico. A/B, FAR, U3, 03.5, 03.9 e 03.12 non riaperti. |
| Matrice file→modifica→motivazione→controllo | ✅ | La matrice nel report corrisponde ai sette file del delta: il piano aggiorna fonte/stato, §0.1, swap, D9 e O1; APERTURA aggiorna intestazione e rinvii; due successori aggiornano residui/consegna senza riscrivere fonti improntate; report/controlli/manifest fissano provenienza e perimetro. Nessuna estensione normativa estranea individuata. |

Riferimenti puntuali al candidato:

- `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md:22`: fonte D9 e distinzione dall'OK precedente; `:131` e `:147`: stato corrente; `:461`: full16, consumer fisso, contabilità e assenza fallback; `:1190`: D9 acquisita, qualifica e label 1a separate; `:1297`: O1 operativo.
- `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md:16`: OK R1–R4 acquisito e nuova review distinta; `:21`: record D9 acquisito; `:27`: successori espliciti; `:81` e sezione finale: sequenza 03.8/03.11 e prerequisiti del pilot distinti.
- `MATRICE_RESIDUI_03_8_DOPO_D9.md`: tabella dei cinque stati, vincoli/residui separati e sezione verifiche/freeze; `CONSEGNA_TECNICA_03_8_D9_PER_03_10.md`: tabella dei ruoli e paragrafi su contatore/ledger/1a.

La lettura delle prescrizioni risultanti è limitata alle conseguenze D9 e ai loro raccordi. Non è una nuova review R1–R4, delle statistiche o dell'harness. Il richiamo ai “parametri D9” ancora da determinare nel budget corrente riguarda i dati/configurazioni tecnici e non riapre i ruoli approvati.

## Manifest, JSON e link

✅ JSON del delta e delle impronte D9 validi. Verificati autonomamente **6/6 artifacts**, **14/14 sources**, **47/47 preserved_sources**, **25/25 statistical_sources** del nuovo manifest. Le fonti sono state lette come blob agli esatti commit registrati, confrontando dimensioni e SHA-256; per gli insiemi preservati anche confronto diretto con i byte nel candidato. L'elenco di 47 file è stato riscontrato con Git, non assunto dal manifest. Il manifest non include sé stesso; `freeze_effective=false`, stato locale e review pending sono corretti al candidato.

Impronte dei file del delta, calcolate nella copia isolata; percorsi relativi alla radice:

| File | Byte | SHA-256 |
| --- | ---: | --- |
| `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` | 174468 | `558889a88fea6ca261cce963e2052a3e45efc9db2735553af1177007503d9241` |
| `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md` | 12362 | `1f929d8a94213606049836fdd03fe40bfa3f93859c873644cc19e081527ce627` |
| `studio2/fase03/piano_statistico/MATRICE_RESIDUI_03_8_DOPO_D9.md` | 4020 | `77cc77b2c94743a4ea450377dd49ab8c703272ef4e625cd0b7a211d76ea8beed` |
| `studio2/fase03/piano_statistico/CONSEGNA_TECNICA_03_8_D9_PER_03_10.md` | 3150 | `e49f178c84f3dca5857011c577edcbd79ca9bba471dac4b0b14e391a93d7101c` |
| `studio2/fase03/piano_statistico/REPORT_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md` | 10773 | `97564d55fa400980b4c0a8106ab8074c226df7d4f0d9d09544956fb7f0856308` |
| `studio2/fase03/piano_statistico/CONTROLLI_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json` | 32478 | `2f81b3d9d4da1864a485726f6a10ff9dcf3afd4213580197d0c34a8b795ee897` |
| `studio2/fase03/piano_statistico/MANIFEST_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json` | 24446 | `bb5e4d9668f9714cead929bb575d44e497823376cda062c1443c0666dadc343a` |

✅ Ricalcolato l'inventario Markdown dei file pertinenti: **25 occorrenze**, di cui **13 introdotte nel delta documentale**, tutte le 13 risolte. Confrontate anche le singole voci e la marca nuovo/ereditato con il JSON: coincidenti. Sono rinvii a file, senza nuovi anchor da verificare.

⚠️ **Eccezione ereditata dichiarata:** il record D9 byte-identico contiene il link relativo `PROPOSTA_D9_RUOLI_MODELLI_2026-09-14.md`, assente nel checkout 03.8 per scelta di acquisizione selettiva. Non è un nuovo link del delta dc4d656→8a20c12. Verificata recuperabilità effettiva tramite:

```text
git show 95ff8571af02bab79094ed1a6be3f6a7b410c711:studio2/fase03/PROPOSTA_D9_RUOLI_MODELLI_2026-09-14.md
```

Il blob recuperato ha **36.141 byte**, SHA-256 **a47f42dda7ee9702c292e34ada6b116ac3c85e42ec3a50e68af97c159f0d0f9d**, come nel record di acquisizione. L'eccezione non è stata riparata importando la proposta o alterando il record. Il link assoluto alla vecchia proposta harness è risolvibile nella sede storica, ma non certifica lo stato del cantiere R01–R10 o di un suo candidato successivo. Tali limiti sono espliciti nei record acquisiti e nel nuovo rapporto; nessun OK all'harness deriva da questa verifica.

Le 17 fonti storiche elencate nel JSON D9 restano inventario della registrazione originaria: non sono state importate né sottoposte a una nuova review complessiva. La presente review verifica i tre blob, le due voci artifacts e la recuperabilità specificamente richiesta della proposta.

## Guardiano e controlli eseguiti

✅ `git diff --check` pulito, exit 0 e nessun output, per entrambi i delta di acquisizione e per **dc4d6560af73579300e33a0a81fc9c3b4316722d → 8a20c125bd294191c67ebdbf571832b1e32ac0f1**. Controllato anche il successore documentale per distinguerne i soli due nuovi file.

⚠️ Rieseguito esclusivamente il guardiano documentale **`python3 docs/test_explanation.py`**: **35 test, 14 fallimenti storici, 1 skip, 0 errori, exit 1 — NON PASS**. Stdout+stderr acquisiti in memoria tramite subprocess, fuori dai documenti scientifici e senza scrivere log nel candidato. L'intero oggetto ricostruito (test, identificativi completi dei failure, sottocasi, errori, skip, exit) coincide con **entrambi** `guardian_before` e `guardian_after` del JSON.

Identificativi completi confrontati:

```text
test_condition_c_contract_and_caveats (__main__.UnifiedConversationChecks.test_condition_c_contract_and_caveats) (phrase='non un risultato empiricamente misurato')
test_one_flow_and_ordered_step_headings (__main__.UnifiedConversationChecks.test_one_flow_and_ordered_step_headings)
test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='0.944444')
test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='0.916667')
test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='0.833333')
test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='zero astensioni')
test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='C1–C4: 4/4 PASS')
test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='controllo secondario distinto')
test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='budget nominale di 1024')
test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations) (phrase='36 aggregati B non cappati sono corretti')
test_step27_qwen_frozen_results_and_limitations (__main__.UnifiedConversationChecks.test_step27_qwen_frozen_results_and_limitations)
test_step27_qwen_protocol_stable_facts (__main__.UnifiedConversationChecks.test_step27_qwen_protocol_stable_facts) (doc='html')
test_step27_qwen_protocol_stable_facts (__main__.UnifiedConversationChecks.test_step27_qwen_protocol_stable_facts) (doc='md')
test_step27_qwen_protocol_stable_facts (__main__.UnifiedConversationChecks.test_step27_qwen_protocol_stable_facts)
```

Skip confrontato:

```text
setUpClass (__main__.TutorialChecks) ... skipped 'legacy part-1 walkthrough is not present in this checkout'
```

Anche i due log grezzi del preparatore, `/tmp/fot-tep-038-d9/guardian_before.log` e `/tmp/fot-tep-038-d9/guardian_after.log`, risultano presenti al riscontro: dimensioni/hash coincidono con il JSON e i failure estratti coincidono. Restano file temporanei non tracciati del preparatore, non prove di pubblicazione permanente. Non è stato confrontato l'hash del log di una nuova esecuzione con quelli storici come se il tempo stampato fosse deterministico. Il guardiano invariato non è prova della correttezza normativa o scientifica.

Procedure riproducibili principali:

```text
git worktree add --detach /Users/luker/fot-tep-verifica-recepimento-d9-038 8a20c125bd294191c67ebdbf571832b1e32ac0f1
git rev-parse HEAD HEAD^{tree}
git status --short
git worktree list
git rev-parse origin/main
git ls-remote origin refs/heads/main
git show -s --format='%H %T %P' <commit>
git diff --name-status <base> <successore>
git diff dc4d656..8a20c12 -- docs/paper/FoT_TEP_Review_Piano_Sperimentale.md studio2/fase03/APERTURA_SOTTOFASI_FASE03.md
git ls-tree -r --name-only 16f2274 -- studio2/fase03/piano_statistico
git show <commit>:<path>
git merge-base --is-ancestor aaba893 8a20c12
git diff --check dc4d6560af73579300e33a0a81fc9c3b4316722d 8a20c125bd294191c67ebdbf571832b1e32ac0f1
python3 docs/test_explanation.py
```

Script Python di sola lettura con pathlib/json/hashlib/subprocess/re hanno confrontato blob, dimensioni/hash, insieme dei file, voci artifacts e link introdotti rispetto alla base. Ricerche `rg` su D9/122B/27B/Terra/2.4T/acquisizione/recepimento/qualifica e lettura dei paragrafi circostanti hanno verificato gli stati correnti.

## Letture, limiti e consegna

Letti contratto MAINTENANCE (in particolare §§1–2, 5 e 8), prompt Prompt/Verifica/Fase/Documentazione/Commit pertinenti, walkthrough §0 e intestazione per le prevalenze, prompt della review, report/manifest/controlli, entrambi i record di acquisizione, decisione e consegna/matrice D9, diff normativo integrale, successori 03.8 e relative sezioni correnti. Confrontate matrice/consegna rev.10 preservate. Il verbale storico OK è quello emesso da questa stessa sessione: è stato verificato per byte senza ripeterne il lavoro. Letture documentali nell'ordine di diverse migliaia di parole; nessuna nuova lettura dei paper o ricerca bibliografica.

Non eseguiti test scientifici, ricostruzioni statistiche, prove dei servizi, test harness, API, inferenze, simulazioni o pilot. Non verificato il progresso effettivo del cantiere harness R01–R10: il suo recepimento rimane dichiarato pendente/non attestato. Non modificati paper_sections o walkthrough; nessuna parità MD/HTML nuova da certificare.

**03.8 e Fase 03 restano aperte.** Il presente OK non firma 03.8, non approva l'ordine label 1a, non qualifica servizi, non integra/pubblica/congela e non autorizza chiamate. Restano i passi distinti di acquisizione di questo verbale e successivi raccordi documentali, firma materiale, integrazione/pubblicazione e freeze secondo i requisiti vigenti; nessuno è eseguito qui. Il candidato è invariato e il verbale rimane non tracciato nella sola copia del revisore. Dimensione e SHA-256 del verbale sono comunicati fuori dal file, evitando auto-hash.

Data di emissione: 2026-09-15T01:03:35+02:00 (Europe/Rome).
