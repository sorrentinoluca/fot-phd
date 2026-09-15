# Consegna locale — sottofase 03.12, schema insight R4

**Data:** 2026-09-14, Europe/Rome  
**Sottofase:** studio 2 FoT-TEP, Fase 03, **03.12 — schema degli insight**  
**Esito del lavoro:** candidato locale di integrazione e documentazione **completato**; oggetto
scientifico R4 già verificato **R4-V OK**. Nessuna integrazione in `main`, pubblicazione o
creazione del tag è stata eseguita. La Fase 03 resta aperta.

Questo documento è autosufficiente per la finestra orchestratrice. Registra lo stato successivo
alla preparazione locale e non dichiara operazioni remote non avvenute.

## 1. Attività svolta

È stata applicata la procedura locale richiesta per la futura consegna dello schema insight R4:

1. verificati branch, worktree, modifiche preesistenti, `origin/main`, `main` remoto e assenza
   del tag prima della scrittura;
2. creato un worktree dedicato dal `origin/main` allora corrente;
3. integrata nel solo branch dedicato la storia del candidato 03.12, risolvendo l'unico conflitto
   effettivo in `studio2/PROVENIENZA.md` e conservando entrambe le sezioni concorrenti;
4. verificati riferimenti Git, 18/18 voci del manifest rev. 5, hash e dimensioni delle evidenze;
5. preservati i byte del contratto R4, del manifest rev. 5, della decisione e del report storico;
6. acquisito separatamente e byte-identico il precedente verbale NON OK;
7. aggiornata insieme la coppia walkthrough Markdown/HTML con la sezione §4.12;
8. creato il record di preparazione locale con annotazione proposta e procedura seriale residua;
9. eseguiti i controlli locali pertinenti, senza ripetere test sul server, simulazioni o inferenze.

Non sono stati modificati l'adapter 03.10, il servizio 122B, i dati sperimentali o gli artefatti
del primo studio. Non sono stati prodotti insight.

## 2. Worktree, branch e riferimenti

| Voce | Valore |
| --- | --- |
| Worktree dedicato | `/Users/luker/fot-tep-schema-insight-r4-integrazione` |
| Branch | `codex/studio2-schema-insight-r4-integrazione` |
| HEAD finale committato | `c9f83c6447a9963cd69531b14439a3ac5a5a72b2` |
| Base del worktree | `origin/main` a `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` |
| `origin/main` finale osservato | `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` |
| `main` remoto finale osservato | `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` |
| `main` locale, non modificato | `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155` |
| Target R4 verificato e futuro target del tag | `3c64390bc4dd58c48cc4e1e388a38989b32b3143` |
| Commit che acquisisce log, OK e prompt | `43b31afc1ff271594cb4bd21a39fa4469a8c83bc` |
| Tag proposto | `studio2-fase03-schema-insight-frozen-001` |
| Stato del tag | assente localmente e sul remoto; nessun oggetto/peeled da registrare |

Il branch finale risultava pulito e avanti di 14 commit rispetto a `origin/main` prima della
creazione di questo report. Il target R4, il commit delle evidenze e tutti i commit locali
elencati sotto sono antenati di `c9f83c6…`.

## 3. Commit locali preparati

| Commit | Ruolo | Esito |
| --- | --- | --- |
| `c0f4da01b7b68f21e717f3b52c2409cbe81c649d` | merge locale della storia `codex/studio2-schema-insight` nel branch dedicato | candidato d'integrazione creato; unico conflitto in `studio2/PROVENIENZA.md`, risolto preservando entrambi i contenuti |
| `9b1fac9808b92222f45b8b590db32a378d73c136` | acquisizione documentale del precedente NON OK R4-V | verbale storico conservato byte-identico con nome separato |
| `c9f83c6447a9963cd69531b14439a3ac5a5a72b2` | documentazione successiva alla verifica | walkthrough MD/HTML aggiornato insieme e record di preparazione creato |

Questi commit sono soltanto locali. Non sono stati applicati a `main` e non sono stati pubblicati.

## 4. File creati o modificati

### 4.1 Importati dalla storia del candidato nel commit locale d'integrazione

- Modificato: `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/PROVENIENZA.md`.
- Creati/importati in
  `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/`:
  `DECISIONE_SCHEMA_INSIGHT.md`, `PROPOSTA_TAG_SCHEMA_INSIGHT.md`,
  `REPORT_SCHEMA_INSIGHT.md`, `SCHEMA_FREEZE.json`, `TEST_RESULTS.txt`,
  `TEST_RESULTS_qwen.txt`, `TEST_RESULTS_qwen_rev003.txt`,
  `TEST_RESULTS_qwen_rev004.txt`, `TEST_RESULTS_rev004.txt`,
  `VERIFICA_SCHEMA_INSIGHT.md`, `VERIFICA_SCHEMA_INSIGHT_rev003.md`,
  `VERIFICA_SCHEMA_INSIGHT_rev004.md`, `insight_v1.schema.json`,
  `integrazione_tag_3_12_prompt.md`, `leakage_rules_v1.json`, `requirements.txt`,
  `test_validator.py`, `validator.py`.

### 4.2 Creati o modificati dalla preparazione documentale locale

- Creato e committato:
  `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004_NON_OK_STORICO.md`.
- Creato e committato:
  `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/PREPARAZIONE_INTEGRAZIONE_SCHEMA_INSIGHT_R4.md`.
- Modificati e committati come coppia:
  `/Users/luker/fot-tep-schema-insight-r4-integrazione/docs/fot_walkthrough_conversazione_studio2.md`
  e
  `/Users/luker/fot-tep-schema-insight-r4-integrazione/docs/fot_walkthrough_conversazione_studio2.html`.
- Creato da questa richiesta e lasciato intenzionalmente **non tracciato e non committato**:
  `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/CONSEGNA_LOCALE_SCHEMA_INSIGHT_R4.md`
  (questo file).

La sintesi divulgativa `docs/fot_walkthrough_studio2.html` non è stata modificata: 03.12 è un
passaggio tecnico di preparazione e `Documentazione_LLM.md` non richiede di duplicarlo lì.

## 5. Report, verbali e record pertinenti

| Ruolo | Percorso assoluto | Stato |
| --- | --- | --- |
| Report storico R4 | `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/REPORT_SCHEMA_INSIGHT.md` | byte-identico al target R4; conserva il proprio stato storico pending |
| Decisione R4 | `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/DECISIONE_SCHEMA_INSIGHT.md` | byte-identica al target R4 |
| Manifest rev. 5 | `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/SCHEMA_FREEZE.json` | byte-identico, pending, `tag_created=false` |
| Verbale indipendente OK R4-V | `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004.md` | committato nel commit evidenze `43b31af…` |
| Precedente NON OK | `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004_NON_OK_STORICO.md` | conservato separatamente e byte-identico |
| Log server R4 | `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/TEST_RESULTS_qwen_rev004.txt` | trascrizione del terminale fornita dall'autore; non file originale scaricato dal server |
| Prompt operativo | `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/integrazione_tag_3_12_prompt.md` | procedura futura, non autorizzazione automatica |
| Preparazione locale | `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/PREPARAZIONE_INTEGRAZIONE_SCHEMA_INSIGHT_R4.md` | committata; include annotazione proposta e sequenza residua |
| Consegna corrente | `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/CONSEGNA_LOCALE_SCHEMA_INSIGHT_R4.md` | non tracciata; creata per il passaggio all'orchestratore |

## 6. Controlli eseguiti e risultati

### 6.1 Riferimenti, manifest e impronte

- `origin/main` e `main` remoto verificati a `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`
  prima della scrittura e al controllo finale.
- Tag 03.12 assente localmente e sul remoto.
- Ascendenze: target `3c64390…`, evidenze `43b31af…`, merge locale `c0f4da0…` e
  acquisizione NON OK `9b1fac9…` tutti antenati del candidato finale `c9f83c6…`.
- Manifest rev. 5: **18/18** voci verificate per SHA-256 e dimensione:
  10 artefatti al target R4, 6 fonti al commit base
  `d815ce96d928254de79209f02e11a561445764cd`, 2 fonti 03.7 al commit registrato
  `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155` e al tag congelato 03.7.
- Tag 03.7 verificato: oggetto annotato `6854c49b4034c16b8df3b11d45dd759a343463e2`,
  peeled `c16b533016db4617deb1ba96853253f117e8e32b`, antenato del commit registrato.
- Catena `previous_manifest_sha256` verificata: rev. 5 → rev. 4.
- Contratto, manifest, decisione e report storico invariati dopo il merge locale.

| File | Byte | SHA-256 |
| --- | ---: | --- |
| `SCHEMA_FREEZE.json` | 12.323 | `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12` |
| `TEST_RESULTS_qwen_rev004.txt` | 7.459 | `a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972` |
| `VERIFICA_SCHEMA_INSIGHT_rev004.md` | 21.288 | `d0e69094953cac7966eda9d1f612b81f44cc8e646151fd2339dba0b7ca88ec8e` |
| `VERIFICA_SCHEMA_INSIGHT_rev004_NON_OK_STORICO.md` | 19.064 | `5bd196820f74b7fbd5ee6736df2b72afc64afbbfb26459dc69f1fe5e15dafd19` |

### 6.2 Test e documentazione

- Suite 03.12 nel venv qualificato locale, Python 3.13.15/jsonschema 4.26.0:
  **25 PASS, 0 FAIL/ERROR, 1 SKIP su 26**. Lo skip è il test del tokenizer reale perché lo
  snapshot pinnato non è disponibile localmente.
- Regressioni `studio2/fase03/tests`: **16 PASS**, zero fail/error/skip.
- `docs/test_explanation.py`, prima e dopo: 35 test, **14 FAIL storici e 1 SKIP**, con gli stessi
  identificativi e subtest; nessuna regressione.
- Nuova sezione walkthrough: parità **26/26** fatti fra MD/HTML, **8/8** link risolti, anchor e
  navigazione univoci.
- Primo lancio non qualificante col Python di sistema: 46 FAIL, 6 ERROR, 1 SKIP per
  incompatibilità x86_64/arm64 di `rpds`, già descritta nel report; non è stato interpretato
  come difetto del contratto.
- `git diff --check` sui nuovi documenti: pulito. Il diff complessivo segnala soltanto spazi
  finali nei log raw `TEST_RESULTS_qwen_rev003.txt` e `TEST_RESULTS_qwen_rev004.txt`, preservati
  intenzionalmente byte per byte.

### 6.3 Distinzione fra prova locale e prova server

La prova locale qualificata resta **25 PASS + 1 SKIP**. I **26 PASS su 26 senza skip** sul server
sono documentati dalla trascrizione del terminale fornita dall'autore, copiata byte per byte
dall'allegato; non sono stati rieseguiti in questa preparazione. Il log non è un file originale
scaricato dal server. I conteggi 83/84 token qualificano fixture e implementazione, non capienza
dei prompt reali, ottimalità dei cap o validità scientifica degli insight.

## 7. Limiti e attività deliberatamente non svolte

- Nessun test è stato rilanciato sul server.
- Nessuna qualifica del servizio o modello 122B.
- Nessuna simulazione, inferenza o produzione di insight.
- Nessuna modifica all'adapter o al branch 03.10.
- Nessuna modifica a `main`, nessun push, nessun tag.
- Nessun `PUBBLICAZIONE_SCHEMA_INSIGHT.md`: una pubblicazione non avvenuta non è stata registrata.
- Lo scanner lessicale non dimostra l'assenza universale di parafrasi o leakage semantico.
- La qualifica del tokenizer su fixture non dimostra capienza dei prompt reali né ottimalità
  scientifica dei cap.
- L'OK R4-V qualifica l'esatto commit `3c64390…`; non qualifica automaticamente HEAD,
  il commit evidenze, il merge locale o un futuro merge.

## 8. Stato Git finale dopo la creazione di questo report

Branch: `codex/studio2-schema-insight-r4-integrazione`, HEAD
`c9f83c6447a9963cd69531b14439a3ac5a5a72b2`, avanti di 14 commit rispetto a `origin/main`.

- **File committati:** tutti i file elencati nei §§4.1–4.2 salvo questo report; i tre commit
  locali sono `c0f4da0…`, `9b1fac9…`, `c9f83c6…`.
- **File tracciati modificati ma non committati:** nessuno.
- **File staged:** nessuno.
- **File non tracciati:** soltanto
  `studio2/fase03/schema_insight/CONSEGNA_LOCALE_SCHEMA_INSIGHT_R4.md` (questo report).

Per questa richiesta non è stato creato alcun commit. Il report deve essere riesaminato e
committato dall'orchestratore soltanto se rientra nel successivo incarico autorizzato.

## 9. Stato effettivo di integrazione, pubblicazione e congelamento

| Stato | Esito effettivo |
| --- | --- |
| Verifica scientifico-tecnica R4 | **R4-V OK** sul target esatto `3c64390…` |
| Integrazione nel branch dedicato | completata localmente nel commit `c0f4da0…` |
| Documentazione successiva | completata e committata localmente in `9b1fac9…` e `c9f83c6…` |
| Integrazione in `main` | **non eseguita** |
| Pubblicazione di `main` | **non eseguita** |
| Creazione del tag 03.12 | **non eseguita** |
| Pubblicazione del tag 03.12 | **non eseguita** |
| Freeze efficace/pubblicato | **non attestato**; manifest rev. 5 resta correttamente pending |
| Fase 03 | **aperta** |

Il futuro tag deve puntare esclusivamente a
`3c64390bc4dd58c48cc4e1e388a38989b32b3143`, non a `43b31af…`, `c0f4da0…`,
`c9f83c6…`, HEAD o al futuro merge.

## 10. Operazioni residue, dipendenze e decisioni

### Dipendenze

- coordinamento seriale con gli altri cantieri che modificano `main`, `studio2/PROVENIENZA.md`
  e il walkthrough condiviso;
- mantenimento della raggiungibilità delle fonti 03.7 congelate;
- successivo raccordo 03.10, separato da questa integrazione;
- Fase 03 complessivamente ancora aperta.

### Decisioni/autorizzazioni dell'autore

- La preparazione locale e i commit documentali erano autorizzati e sono completati.
- Push, integrazione effettiva in `main` e tag richiedono autorizzazione esplicita nel relativo
  incarico; questa consegna non la sostituisce.
- Il log server resta evidenza supplementare esterna alle 18 voci: nessun manifest rev. 6 è
  richiesto per questa acquisizione.
- Stato pending ed esiti storici, incluso il precedente NON OK, devono restare conservati.

### Prossimo passo per la finestra orchestratrice

1. Leggere questo report e
   `/Users/luker/fot-tep-schema-insight-r4-integrazione/studio2/fase03/schema_insight/PREPARAZIONE_INTEGRAZIONE_SCHEMA_INSIGHT_R4.md`.
2. Ricontrollare `origin/main` remoto, worktree concorrenti e assenza del tag.
3. Integrare serialmente il branch `codex/studio2-schema-insight-r4-integrazione` nel `main`
   corrente, preservando i byte R4 e risolvendo soltanto conflitti effettivi.
4. Ripetere ascendenze, 18/18 impronte, hash/dimensioni delle evidenze, suite locali, regressioni,
   guardiano documentale, parità e link.
5. Con autorizzazione esplicita, pubblicare `main` e verificare che target, evidenze e
   documentazione siano raggiungibili da `origin/main`.
6. Solo dopo, creare il tag annotato `studio2-fase03-schema-insight-frozen-001` sull'esatto
   `3c64390…`, pubblicare quel solo tag e verificarne oggetto e peeled remoti.
7. Soltanto dopo la pubblicazione effettiva, creare `PUBBLICAZIONE_SCHEMA_INSIGHT.md`.
8. In una successiva attività 03.10 aggiornare pin, manifest e messaggio dell'adapter, incluso
   l'hash di `validator.py` da
   `ec24159b50dc745963ccf820ccbb8ae2ce05c3894d005239aaf5c960ad9f1228` a
   `cd523d3105e02de99e7cc09bf0c2c4c052c1ae1776c8da37a9b57e869b1aa508`.
