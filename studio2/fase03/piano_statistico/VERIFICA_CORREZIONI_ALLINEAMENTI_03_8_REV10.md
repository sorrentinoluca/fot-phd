OK

# Verifica delle correzioni R1–R4 — allineamenti 03.8 rev.10

Esito riferito esclusivamente al candidato `9a56d12d0633a0c9790c48792182f26fc6eb424a`, tree `e35e5ca661325657715dce6723e4e8ec09540101`. Le quattro classi di rilievi del precedente NON OK sono risolte nel delta e nelle prescrizioni risultanti esaminate. Nessun rilievo bloccante residuo individuato nel perimetro richiesto. Il successivo `16f2274` è una consegna documentale e non è il candidato valutato.

L'aggiornamento dell'autore prevale sulla cronologia preparatoria: **D9 è già approvata e registrata localmente al commit `aaba893dff8c62f9f9281eec7423eee020235e03`; resta pendente il recepimento del record nel ramo 03.8. Non occorre una nuova decisione sui ruoli.** Il record è stato letto dagli oggetti Git come evidenza esterna, senza importarlo nel candidato.

## Identità effettiva, indipendenza e stato

- Revisore: Codex; modello esposto `gpt-6-astra`, provider `openai`, effort esposto `high`.
- Task/sessione: `01a0a1d9-8ccd-7893-b504-4fde93380ea0`.
- Fonte dei metadati: record `session_meta` e ultimo `turn_context` nel file locale `/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T23-36-24-01a0a1d9-8ccd-7893-b504-4fde93380ea0.jsonl`; letti i soli campi pertinenti all'identità. Non si tratta di un'identità attesa copiata dal prompt.
- Repository comune: `/Users/luker/fot-tep`. Copia isolata del revisore: `/Users/luker/fot-tep-verifica-correzioni-allineamenti-03-8-rev10`, **detached HEAD** sull'esatto candidato. Stato iniziale pulito.
- Preparatore distinto: worktree `/Users/luker/fot-tep-allineamenti-038-r1-r4`, branch `codex/studio2-allineamenti-038-r1-r4`. Nessuna partecipazione di questa sessione alla preparazione delle correzioni, nessun sottoagente impiegato.
- **Limite reale dell'indipendenza:** questa è la stessa sessione che ha emesso il precedente NON OK, ora proseguita su richiesta dell'autore. È indipendente dal preparatore, ma non è una nuova task senza contesto né una seconda opinione di un modello diverso. La nuova review riguarda il delta correttivo e la coerenza risultante; non autocertifica la preparazione.
- Unica scrittura nella copia del candidato: il presente verbale, lasciato non tracciato. Nessun file normativo corretto, nessun commit, merge, push o tag.

## Mandato e identità Git

Il prompt originariamente indicato dall'autore, `PROMPT_VERIFICA_ALLINEAMENTI_03_8_REV10.md` nella copia di consegna `/Users/luker/fot-tep-piano-statistico-chiusura`, conserva SHA-256 `04401004d2bcc0196725faca22d8c4ff2cc97e2903e833399628bffb0d7a33e5`. Il mandato successivo identifica il nuovo candidato e aggiorna D9. Per le verifiche del delta correttivo è stato letto anche `PROMPT_VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md` dal commit di consegna `16f2274`, senza spostare HEAD su tale commit.

| Oggetto | Commit | Tree |
| --- | --- | --- |
| Candidato precedente NON OK | `4503cb6f4fbc9942785c7d1fb74b4caf90cb83b8` | `1eb1d7df58e55a546931711f0a1cf9d800e02e3e` |
| Sua consegna | `2520e7abc1cd68785f2789448b509dea5e55ee7d` | `37f246174c9fecb6e623873c5487de04ec65b400` |
| Acquisizione NON OK / base immediata | `1a21fd260ad2df6a3b04ffb6fa5e2d642a3f63b1` | `5fc28db3628c63a047cb1a152bba3ad5d87b4ae7` |
| **Candidato verificato** | `9a56d12d0633a0c9790c48792182f26fc6eb424a` | `e35e5ca661325657715dce6723e4e8ec09540101` |
| Consegna successiva, esclusa dal delta normativo | `16f227439357b07b7dc945f67ab5a4368c12b684` | `4b65ae9805a0e88c189d4516f03c38d46fbc61a1` |

Ogni riga dopo la prima ha come unico parent il commit della riga precedente. Il parent di 4503cb6 è `70c84e3a573951171813add26a46167cbc6c7203`. La ref locale `origin/main` e `git ls-remote origin refs/heads/main` coincidono con `a00605862f627710347bd63c49f79a6d0a00135f`, la base pubblicata indicata dal preparatore: nessun avanzamento remoto osservato durante la verifica. Il worktree sorgente della precedente consegna risulta pulito a 2520e7a; non è stato usato il suo HEAD come nuovo candidato.

## Metodo e fonti

Confrontati parent, tree, elenco dei file e diff integrale base immediata→candidato. Rilette le prescrizioni correnti del piano generale nelle quattro classi, APERTURA, report, manifest, acquisizione e controlli; eseguite ricerche estese nell'intero piano per numeri, modelli, ruoli, precedenze e stati residui. Le letture pertinenti di MAINTENANCE, Prompt/Fase/Verifica/Documentazione/Commit, fonti e prevalenze del walkthrough, rev.10 e fonti di pubblicazione già svolte nella precedente review della stessa sessione sono state riutilizzate dove i byte sono invariati. Confrontati nuovamente i paragrafi interessati e verificati i pin: non si afferma una nuova lettura integrale dei paper o una nuova validazione statistica.

Le 27 fonti del nuovo manifest sono state ricostruite con `git show <commit>:<path>` agli esatti pin e confrontate per byte, dimensione e SHA-256. Le fonti di merito comprendono piano statistico §§1, 5, 7–11, 15–16 e budget/coordinamento nella consegna `51782e8c40069c0a2310afafc36907a61d517ff6`, catalogo D1, pubblicazione e manifest R4, chiusura 03.5, precedenti consegne e NON OK. Il controllo delle impronte non sostituisce la lettura normativa.

Comandi e procedure principali, eseguiti nella copia isolata:

```text
git rev-parse HEAD HEAD^{tree}
git status --short
git show -s --format='%H %T %P' <commit>
git diff --name-status <base>..<candidato>
git diff 1a21fd260ad2df6a3b04ffb6fa5e2d642a3f63b1..9a56d12d0633a0c9790c48792182f26fc6eb424a -- <file>
git ls-tree -r --name-only 2520e7a -- studio2/fase03/piano_statistico
git show <commit>:<path>
git ls-remote origin refs/heads/main
git merge-base --is-ancestor aaba893dff8c62f9f9281eec7423eee020235e03 9a56d12d0633a0c9790c48792182f26fc6eb424a
rg -n <espressioni pertinenti> <piano generale e APERTURA>
git diff --check 1a21fd260ad2df6a3b04ffb6fa5e2d642a3f63b1..9a56d12d0633a0c9790c48792182f26fc6eb424a
python3 docs/test_explanation.py
```

Script Python di sola lettura con `pathlib`, `json`, `hashlib`, `subprocess` e `re` hanno confrontato manifest/blob, risolto link, estratto gli identificativi completi del guardiano e ricostruito in memoria i log grezzi. Nessun log o artefatto scientifico è stato rigenerato nel working tree.

## Esito dei nove punti

| Punto | Esito | Evidenza e conclusione |
| --- | --- | --- |
| 1. Genealogia e perimetro | ✅ | Catena e tree sopra verificati. L'acquisizione 1a21fd2 aggiunge soltanto il precedente verbale e `ACQUISIZIONE_NON_OK_ALLINEAMENTI_03_8_REV10.md`. Il candidato contiene **2 M +5 A**: piano generale e APERTURA modificati; report, manifest, controlli e due log nuovi. Nessuna modifica a harness, proposta/registro D9, paper_sections o walkthrough. 16f2274 aggiunge soltanto consegna e prompt. |
| 2. Preservazione | ✅ | **38/38** file preesistenti della cartella statistica byte-identici a 2520e7a; **19/19 files +6/6 inputs_read** del manifest rev.10 corrispondono a dimensioni, SHA-256 e blob di 51782e8. Preservati piano, manifest, verbale OK, atto da sottoscrivere, budget e delta harness. Vecchio NON OK identico: **22.063 byte**, SHA-256 `52944646527d0e73d6508ae53669f47f5e8661050ff777c75a448ca535ca9c13`. Restano integri anche vecchio report/manifest e matrice dei residui. |
| 3. R1: costi e calendario | ✅ | Piano generale §§1, 7, 8.7–8.8, checklist T5 e §13; fonti rev.10 §7.2, budget e coordinamento §2. Nucleo **1.344+192+192=1.728**, ×3=**5.184**. Swap 224, ablation 148 e OOD 144 portano le quattro misure a **2.244R**, non al totale complessivo. Il ledger aggiunge audit, E5, canary, generazione librerie, pilot, verifiche e retry senza doppio conteggio. Regola **1,20×T≤W**; nessun tetto rigido vigente di 3.700, durata in giorni derivata dal solo R o calendario validato per implicazione. |
| 4. R2: run e ablation | ✅ | Piano generale §§5, 6.9, 8.1/8.3/8.5/8.8/8.12, D2/D3, §13 e addendum SWaT; rev.10 §§1, 7.3–7.4 e 9.2. **8 run/fault, 64 fault+8 Normal=72 primari; +6 OOD+11 scorte=89**. Scorte solo sostitutive, mai nuovi cluster, criteri/identificativi pre-specificati e nessuna sostituzione dopo la prima chiamata sul run. Ablation **64+4×3×7=148**, ×3=444. Coerenti 64 cluster e tutti i sette riceventi non proprietari. |
| 5. R3: OOD, D11, R4 e precedenze | ✅ | Piano generale §§6.9–6.10, 8.6, 8.9, 8.12, D11/D12 e §11; APERTURA 03.8/03.11; rev.10 §§8–9 e 16. F6/F4 condizionati, catene **F6→F5→F12** e **F4→F11→F5**, verifiche individuali dei sostituti e due OOD distinti; collisione F5/caso irrisolto richiede sospensione e decisione esplicita dell'autore. D11 **{F1,F2}/{F14,F15}, indici 1–3**. R4 pubblicata e congelata; adapter/conformità/servizi rimangono futuri. Ordine **freeze statistico→03.11 tecnica→chiamate dopo gli altri GO**; E5 distingue il proprio freeze dal freeze statistico, senza generazione anticipata né ciclo. T11 resta non bloccante automaticamente; 03.5 non riaperta. |
| 6. R4: ruoli e provenienza D9 | ✅ | Piano generale intestazione, §§0.1, 2.1, 5–8, D9 e §11, APERTURA; mandato e record esterno aaba893. **122B producer principale e consumer; 27B producer alternativo, libreria completa di 16 insight, consumer 122B fisso nello swap; Terra solo storico descrittivo interno, fuori dalle nuove stime.** Nessuna assegnazione corrente a Qwen-2.4T, surrogato consumer 27B o fallback Terra. Acquisizione documentale, qualifica tecnica e firma restano distinti. L'aggiornamento dell'autore precisa che il record locale esiste già: manca il recepimento in 03.8. |
| 7. Coerenza risultante | ✅ | Verificati anche i raccordi fuori dalle vecchie righe segnalate: G2/G5, §6.9, calendario, E5, checklist, risposte §13 e confronto SWaT. L'estensione corregge le stesse quattro classi e impedisce prescrizioni concorrenti. APERTURA mantiene 03.8 aperta, 03.11 futura e qualifica D9 distinta. Non introduce risultati, nuove scelte E5, A/B, margine, FAR, U3 o nuove analisi. |
| 8. Manifest e residui | ✅ | **6/6** altri file con dimensione/SHA-256 corretti, **27/27** fonti ai pin esatti; manifest non autoreferenziale. `freeze_effective=false`, tag null, firma/pubblicazione false e review pending descrivono correttamente il candidato prima del presente verbale. La fonte conversazionale del mandato è dichiarata, senza un hash inventato. Report e vecchi residui restano fotografie storiche: non annullano il mandato successivo né la registrazione D9 ora attestata. |
| 9. Controlli locali | ✅ / ⚠️ | `git diff --check` sul delta esatto: exit 0, nessun output. Sei link Markdown locali del piano risolti nella copia del revisore, nessuno rotto; APERTURA non contiene link Markdown locali da risolvere. Verificati i riferimenti di sezione pertinenti. Guardiano rieseguito: **35 test, 14 fallimenti storici, 1 skip, 0 errori, exit 1**; identificativi e parametri dei subtest identici ai due controlli registrati. **Guardiano non PASS**, senza nuovi fallimenti osservati. Ricostruzione byte-esatta dei due log grezzi riuscita. |

## Raccordi controllati e storia conservata

Riferimenti puntuali nel candidato, per rendere rintracciabili le conclusioni:

- R1: `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md:380` e `:531` per nucleo/durate; `:578` per ledger e `:1239` per T5. La finestra del 17 settembre è ipotesi organizzativa da misurare, con sospensione e rinvio all'autore in caso di incompatibilità.
- R2: stesso file `:351`, `:408`, `:431`, `:437`, `:675`, `:1132` e `:1225`; APERTURA `:74` per il lotto tecnico futuro. Gli scenari E5 non fissano nuove mappe.
- R3: stesso file `:525`, `:1180` e `:1282`; APERTURA `:71` e `:74`. Pubblicazione R4 verificata nella fonte pinnata a main: tag `studio2-fase03-schema-insight-frozen-001`, oggetto annotato `4d15c4fb915ea9db9f7425225d231746778f0ba1`, commit `3c64390bc4dd58c48cc4e1e388a38989b32b3143`.
- R4: stesso file `:127`, `:1186` e `:1288`; intestazione APERTURA. «Parametri D9 da determinare» in §8.8 indica parametri tecnici ancora da qualificare, non una scelta dei ruoli da ripetere.

Le ricerche residue sono state interpretate nel contesto, non mediante sostituzioni globali: §2 tratta il piano originale; §8.2 qualifica il record interno; §8.8 marca la tabella 6/8 run e i vecchi tetti come ricostruzione storica, mentre 640/658 non sono residui correnti; D9 marca il vecchio piano B come superato e non prescrittivo. I numeri 1.296/132, le vecchie opzioni e le osservazioni Terra possono quindi restare come storia. Le vecchie fonti statistiche byte-preservate con «D9 aperta/non scelta» descrivono il momento della loro emissione.

## Aggiornamento D9: evidenza esterna e limite della review

Letto dagli oggetti Git il record `studio2/fase03/DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md` al commit **aaba893dff8c62f9f9281eec7423eee020235e03**: **9.083 byte**, SHA-256 `fcb113636de80cc87709905324436555e0ba103bd46de3ac079ce0ef7f60f1b8`. Conferma i ruoli del mandato, la libreria alternativa completa, il consumer fisso, Terra soltanto interno e l'assenza di firma/approvazione label/qualifica tecnica automatica.

Verificata anche l'identità dei due artefatti associati a quel commit: `CONSEGNA_RECEPIMENTO_D9_2026-09-14.md`, 13.282 byte, SHA-256 `3ea739065f1011ed2fd17bface11231f8857dc3f5256d26eff7abcc1d1ef2c77`; `IMPRONTE_DECISIONE_D9_2026-09-14.json`, 11.169 byte, SHA-256 `3b95d17ab3b467bebe5d0bda5fa84d8ab63f3ee13f87397e02caf396654af77b`. Questi controlli identificano l'evidenza esterna; non costituiscono una review integrale del lavoro D9.

Il commit aaba893 **non è antenato** del candidato e i tre file non sono presenti nel suo tree. Non sono stati copiati, applicati o cherry-picked. La formulazione preparatoria «registro in acquisizione nella finestra proprietaria» è temporalmente precedente all'aggiornamento dell'autore: **alla presente verifica il registro esiste localmente; l'acquisizione ancora da fare è nel ramo 03.8**. Tale raccordo futuro va documentato nella sua sede, senza riscrivere questo snapshot. Nessuna nuova decisione dell'autore sui ruoli è richiesta per dare OK alle correzioni R1–R4.

## Impronte del candidato e degli artefatti preservati

Tutti i percorsi della tabella sono relativi alla radice del worktree isolato. Valori calcolati dai byte del candidato:

| File | Byte | SHA-256 |
| --- | ---: | --- |
| `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` | 173448 | `56ba6d42ebddceed1a161b3cf3a54198568fec4f6e79f632250daa6d88c96111` |
| `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md` | 11822 | `93da783a9f2f335d9cbf9752d1cf82516327dd40706091dcd72e4b62106e3300` |
| `studio2/fase03/piano_statistico/REPORT_CORREZIONI_ALLINEAMENTI_03_8_REV10.md` | 12419 | `19d69fc5cb2d3deee514044ccb47e1e9b61eab2df996c0834e4594d03ac23dc4` |
| `studio2/fase03/piano_statistico/MANIFEST_CORREZIONI_ALLINEAMENTI_03_8_REV10.json` | 10112 | `d422279aa15c94cbafe5afb0a1b61fb105967804709762d7942a9cef53b55303` |
| `studio2/fase03/piano_statistico/CONTROLLI_CORREZIONI_ALLINEAMENTI_03_8_REV10.json` | 36542 | `deedf2961ba4a4d1a4a460fc32dff80c54d64208e9b8b8338308920c9a8db93e` |
| `studio2/fase03/piano_statistico/GUARDIANO_PRIMA_CORREZIONI_03_8_REV10.log` | 2582134 | `4619c04e4e0311c8b1b27057ee89933500d0b6d4a36b7385bb9ce75716012063` |
| `studio2/fase03/piano_statistico/GUARDIANO_DOPO_CORREZIONI_03_8_REV10.log` | 2582134 | `aee53378f6e23e9545d69cdaaebf6aa6ef075ea6b56db09869e3db9a22f78581` |
| `studio2/fase03/piano_statistico/PIANO_STATISTICO.md` | 81490 | `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a` |
| `studio2/fase03/piano_statistico/PIANO_STATISTICO_FREEZE.json` | 25894 | `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8` |
| `studio2/fase03/piano_statistico/VERIFICA_PIANO_STATISTICO_REV10.md` | 12478 | `d269e26d8cb4e23370577e1e193d90d9357d66f7c739e9d0669970edf71b0066` |
| `studio2/fase03/piano_statistico/DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md` | 4974 | `4a0a4e1fc2797ee7a81439110e164d43159c745007136c9dda7bed7759471cc8` |
| `studio2/fase03/piano_statistico/BUDGET_RISORSE_REV10.md` | 8528 | `8d909d8f851b8b9c633687989d3a9f3221230b48e1f0595278e075556d283887` |
| `studio2/fase03/piano_statistico/DELTA_HARNESS_03_10.md` | 7108 | `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e` |

## Guardiano: confronto indipendente

L'esecuzione del revisore ha prodotto gli stessi 14 identificativi completi di `guardian_before.failures` e `guardian_after.failures` nei controlli JSON. Elenco effettivamente confrontato, inclusi i subtest:

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

Skip identico:

```text
setUpClass (__main__.TutorialChecks) ... skipped 'legacy part-1 walkthrough is not present in this checkout'
```

Totale 35 test, 14 fallimenti, 1 skip, nessun errore, exit 1. La ripartizione 1/1/9/3 nei quattro metodi coincide. Questo attesta l'assenza di regressioni osservate dal guardiano nel perimetro confrontato; non sana i fallimenti storici e non prova la correttezza scientifica del piano.

Ricostruiti i log grezzi esclusivamente in memoria aggiungendo un solo spazio prima del newline alle righe 34, 41 e 52 di ogni log committato:

| Log ricostruito | Byte | SHA-256 coincidente con i controlli |
| --- | ---: | --- |
| Prima | 2582137 | `988bd10990492076fcfc85c5e9d37b2fcd16c3ea099a4d7f0ab71bac3f2d0bae` |
| Dopo | 2582137 | `47857d3eaf37d3df90b02ce1fc2c4d0a35bee3ff591e77444f00681ab444bf43` |

Nessun confronto di hash grezzi fra l'esecuzione del revisore e quelle del preparatore: i tempi stampati variano. I log committati restano intatti.

## Limiti e stato dopo l'OK

⚠️ L'OK riguarda soltanto gli allineamenti correttivi R1–R4 e la loro coerenza documentale risultante nel candidato esatto. Il precedente NON OK su 4503cb6 resta valido per quel candidato e non è sovrascritto; l'OK statistico rev.10 conserva il proprio perimetro. Nessuna riapertura di A/B, FAR, U3, margine o gerarchia; nessun ricalcolo di griglie, bootstrap, potenza o risultati e nessuna nuova review bibliografica.

⚠️ Restano separati il recepimento del record D9 in 03.8, le qualifiche e configurazioni tecniche, la documentazione di chiusura, la firma materiale, l'integrazione e il freeze. L'OK non certifica lavoro successivo, main futuro o l'effetto di un eventuale recepimento D9. Gli eventuali raccordi successivi devono essere verificati nel loro delta.

**03.8 e Fase 03 rimangono aperte.** Questo verbale non firma, pubblica, congela, approva l'ordine label, qualifica servizi né autorizza pilot, API, inferenze o simulazioni. Non sono state eseguite tali attività. Nessuna modifica al candidato o ai file di altri worktree; il verbale rimane l'unico nuovo file non tracciato della copia del revisore.

Data di emissione: 2026-09-15T00:27:55+02:00 (Europe/Rome).
