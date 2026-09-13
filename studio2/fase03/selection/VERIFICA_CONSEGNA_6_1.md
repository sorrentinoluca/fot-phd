OK

# Verifica finale di consegna — criteri di selezione §6.1

Data: **2026-09-13**. Verificatore: **Codex**; modello richiesto per il sottoagente dal tool:
**gpt-5.6-sol**; autoidentificazione disponibile nel contesto: **GPT-5**. Agente/finestra separata
`/root/verifica_criteri`.

Controllo mirato alla consegna successiva alla verifica scientifica già committata. Le fonti
primarie non sono state riesaminate; non è stato calcolato D1 e non sono stati aperti risultati
scientifici.

## 1. Commit sorgente e freeze dei criteri

| Esito | Riscontro |
| :---: | --- |
| ✅ | `source_commit` è `9d0e1911afd6c244f748f05f62934590f5314794`, coincide con l'HEAD esaminato e contiene registro, piano, `FEASIBILITY.json`, `SOURCE_CHECK.json`, report e verifica indipendente. Il commit ha messaggio `studio2(fase03): congela i criteri di selezione prima di D1`. |
| ✅ | L'ambito del manifest è `phase03_section6_1_selection_criteria_only`. I campi `d1_draw_executed=false`, `catalog_frozen=false`, `scientific_protocol_frozen=false` e `model_execution_authorized=false` impediscono di interpretarlo come freeze del catalogo, del protocollo generale o di un'esecuzione. |
| ✅ | Tutti i quattro record in `files` coincidono autonomamente per **SHA-256, dimensione e byte** sia col worktree sia col blob corrispondente in `source_commit`. Nessuna impronta è calcolata su una versione successiva del file. |

| File | Ruolo | SHA-256 verificato | Byte verificati |
| --- | --- | --- | ---: |
| `docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md` | `normative_criteria_revision` | `d58a7606d69a560a626da44833c065ddbf1aa395ae8b2e523262daf8622231c7` | 11.339 |
| `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` | `reference_snapshot` | `7f9462c28eef7bc0cf74e201a1ffe283d68056359728fea62740e43a1bb1767a` | 159.979 |
| `studio2/fase03/selection/FEASIBILITY.json` | `verification_record_snapshot` | `ca830d054af19e27aa191fcb51f8e80d3c8444bb746dd9da486304490bd59810` | 504 |
| `studio2/fase03/selection/SOURCE_CHECK.json` | `verification_record_snapshot` | `82c654d142ac0ab13f9b47d9648231bd3f1bfda4c5486a8399f510ff87165372` | 747 |

| Esito | Riscontro |
| :---: | --- |
| ✅ | `integrity_basis=source_commit_snapshot`, il ruolo `reference_snapshot` e la nota associata al piano chiariscono che l'hash fotografa la fonte al commit, senza congelare globalmente il piano vivo. Aggiornamenti futuri del piano estranei ai criteri non invalidano questa revisione; una modifica ai criteri richiede invece nuova revisione, verifica e tag. La stessa distinzione è riportata nella coppia walkthrough. |
| ✅ | Il nome del tag previsto è limitato ai criteri: `studio2-fase03-criteri-selezione-frozen-001`. Il manifest richiede un tag annotato e la raggiungibilità del commit sorgente da `origin/main` prima che il freeze sia effettivo. |

## 2. Parità della coppia walkthrough

| Esito | Riscontro |
| :---: | --- |
| ✅ | Confrontati tutti i blocchi modificati: avviso introduttivo, nuova §4.1, voce §6.1 nell'elenco dei cantieri e avvertenza sulle dipendenze dopo D1. Un rendering indipendente Markdown→HTML restituisce testo uguale per tutti e quattro i blocchi; nella §4.1 i collegamenti compaiono nello stesso ordine. |
| ✅ | La navigazione HTML contiene il collegamento a `#criteri-selezione-61` e la destinazione esiste. L'anchor esplicito Markdown e la sezione HTML usano lo stesso identificatore. |
| ✅ | La nuova §4.1 conserva contenuto, numeri e limiti della verifica: 330/12 e composizioni 5/7; F14/F15 forzati e uno fra F3/F9; quota progettuale non bibliografica; nessuna generalizzazione o potenza inferenziale derivata da due fault; Yin non riverificato; rilevazione distinta dalla diagnosi; raccomandazione Downs da risolvere prima dei run; D1, D11, OOD, D2, producer, dati/evidence reali e gate ancora aperti. |
| ✅ | La sezione non attribuisce una chiusura alla Fase 03 o a S1, non presenta un catalogo come selezionato e non promuove il pilot a risultato scientifico. Dichiara espressamente che i 16 test sono offline e che il gate reale resta sospeso. |
| ✅ | Gli SHA-256 correnti della coppia coincidono con `DELIVERY_CHECK.json`: Markdown `201ba1306553b09989061af1fbf2673aad2122083c6da9a319676be17239dd41`; HTML `561b241cf0d5f00388b120f51db68054366dfb6270e8a8defc252586a1ae3788`. `git diff --check` non segnala errori. |
| ✅ | `fot_walkthrough_studio2.html`, sintesi divulgativa, non risulta modificato. La motivazione del record — preparazione interna e freeze senza nuovo risultato scientifico — è coerente col contratto documentale. |

## 3. Controlli dichiarati in `DELIVERY_CHECK.json`

| Esito | Riscontro indipendente |
| :---: | --- |
| ✅ | Ricontati **145** collegamenti/anchor locali nei quattro file dichiarati: 66 nel walkthrough Markdown, 76 nella replica HTML, 1 nel registro e 2 nel piano. Tutti i file e gli anchor risolvono. |
| ✅ | `python3 -m unittest discover -s studio2/fase03/tests -v`: **16 test eseguiti, 16 passati**. |
| ✅ | `python3 docs/test_explanation.py`: **35 test, 14 fallimenti, 1 skipped**. Il numero coincide con la baseline dichiarata e non introduce nuovi fallimenti; il test non copre direttamente i nuovi criteri. |
| ✅ | I tre output di pianificazione riportano rispettivamente `PLAN_ONLY_NO_PROVIDER_CALLS`, `PLAN_ONLY_NO_PROVIDER_CALLS` e `GATE_ENVELOPE_FROZEN_EXECUTION_SUSPENDED`, come nel record. |
| ✅ | I **30** percorsi del pilot ereditato e `studio2/PROVENIENZA.md`, enumerati dall'albero `6a02927`, non hanno differenze rispetto a quel commit. |
| ✅ | `DELIVERY_CHECK.json` dichiara `d1_draw_executed=false` e `scientific_model_calls=0`. Nessuna operazione svolta in questa verifica ha eseguito D1, chiamato provider o aperto dati scientifici. |
| ⚠️ | Un record locale può attestare file, comandi e output conservati, ma non provare in assoluto l'assenza di attività esterne non registrate. Questo è un limite generale di audit e non emerge alcuna dipendenza concreta da tali attività. |

## 4. Verdetto e condizioni di efficacia

**OK — la consegna §6.1 è pronta per il commit documentale, il tag annotato dedicato e
l'integrazione già autorizzata in `origin/main`.**

Questo OK attesta la coerenza del pacchetto locale e la prontezza operativa. Non attesta ancora
la pubblicazione: il freeze diventa efficace solo quando walkthrough, `CRITERIA_FREEZE.json`,
`DELIVERY_CHECK.json` e questa verifica sono committati, il commit sorgente e questi record sono
raggiungibili da `origin/main`, il tag annotato dichiarato è pubblicato e i ref remoti sono
riverificati. Fino ad allora non va dichiarato efficace; dopo la pubblicazione l'attestazione
resta limitata ai criteri e non autorizza D1, simulazioni, inferenze o il freeze del protocollo
scientifico generale.
