OK

# Verifica indipendente R4-V — sotto-fase 03.12, Revisione 4 (`context_check` e label letterale `Normal`)

Data: 2026-09-14. Verdetto: **OK** sul delta R4 al commit `3c64390bc4dd58c48cc4e1e388a38989b32b3143`.
Il delta è confinato a `context_check`, fixture/test e documenti previsti; il contesto reale 03.7
ricostruito da Git è accettato e le varianti di `normal_label` sono rifiutate; le 18 impronte del
manifest rev. 5 e la catena `previous_manifest_sha256` sono integre; le suite rieseguite coincidono
con la baseline. L'OK non crea alcun tag, non rende efficace il freeze (stato `pending` preservato) e
non sostituisce l'autorizzazione dell'autore. Residui necessari alla chiusura in §9.

## 1. Verificatore, finestra, prova dell'indipendenza

| Voce | Valore | Natura della prova |
| --- | --- | --- |
| Verificatore | Claude, sessione Cowork (Anthropic); identificativo di modello configurato `claude-fable-5-1` | configurazione runtime esposta dalle istruzioni di sessione; il modello in servizio può differire dall'identificativo configurato e non è attestabile da qui con una prova API |
| Finestra | sessione Claude Code/Cowork `session_01Y11UC227qhEvrbQxjzRpzK`; VM locale della sessione `rcw-01y11uc227qhevrbqxjzrpzk` | identificativi esposti dal runtime della sessione |
| Esecutore R4 (dichiarazione nel report) | «Codex, agente basato su GPT-5, in questa finestra» (REPORT §R4); «Codex, agente basato su GPT-6» (REPORT §3, storico) | dichiarazione dell'autore/agente, senza identificativo di finestra né modello runtime |
| Esecutore R4 (prova runtime locale) | log Codex `/Users/luker/.codex/archived_sessions/rollout-2026-09-14T10-49-44-01a09f1b-a581-7c41-a1ec-87912c8896ef.jsonl` (3.891.770 byte, 362 righe, SHA-256 `24322fa1ce5183ba4c7c4a9598e6503a26b58d8594d655329048b4c21a6366a2`): riga 1 `session_meta` con `session_id 01a09f1b-a581-7c41-a1ec-87912c8896ef`, `originator "Codex Desktop"`, `model_provider "openai"`, `cwd /Users/luker/fot-tep`; riga 8 `turn_context` (unico della sessione) con `model "gpt-5.6-sol"`, `reasoning_effort "medium"`; riga 347 output del comando di commit `[codex/studio2-schema-insight 3c64390] … 7 files changed, 333 insertions(+), 32 deletions(-)` con timestamp `2026-09-14T08:59:38.873Z` | evidenza runtime locale, letta in sola lettura su indicazione dell'autore; il timestamp coincide con quello del commit in Git (`2026-09-14T10:59:38+02:00`); le stringhe `gpt-5.6-terra` e `claude-fable-5-1` presenti nel log sono contenuti di file del repository letti dall'agente, non modelli della sessione |
| Precedente verificatore | Codex/GPT-6, finestra `01a09f97-5041-7aa2-92b8-905cf228cd8d` (dichiarato nel suo verbale) | dichiarazione del precedente verbale; non riscontrata su log |

Distinzione accertata: l'esecutore R4 ha operato con provider OpenAI (modello runtime `gpt-5.6-sol`) in Codex
Desktop, finestra `01a09f1b-…`; questa verifica è una sessione Claude (Anthropic) con identificativo di
finestra diverso, e l'identità del provider non dipende dal fatto che il modello in servizio coincida
esattamente con l'identificativo configurato. Il precedente verificatore era a sua volta un agente Codex
(GPT-6, finestra `01a09f97-…`), diverso da questa sessione. Un nuovo worktree o una nuova finestra non
sono stati usati come prova di modello diverso: la prova è la coppia provider/modello nei metadati runtime.
Limite: la dicitura «GPT-5» del report R4 corrisponde al testo delle `base_instructions` del log
(«You are Codex, an agent based on GPT-5»), mentre il modello runtime registrato è `gpt-5.6-sol`; il report
non identifica la finestra. Rilievo documentale non bloccante (§9, R-3).

Metodo: sola lettura; nessuna chiamata a modelli, nessuna simulazione, nessun commit/push/merge/tag.
Unico file scritto: questo verbale, nel worktree del verificatore. Script di controllo propri tenuti fuori
dal repository (`$HOME/r4v/` della VM di sessione). Nessun file del candidato, del precedente verificatore
o dell'harness è stato modificato.

## 2. Oggetto, stato del candidato e worktree del verificatore

- Candidato: `/Users/luker/fot-tep-schema-insight`, branch `codex/studio2-schema-insight`, HEAD
  `3c64390bc4dd58c48cc4e1e388a38989b32b3143` (letto da `.git/worktrees/fot-tep-schema-insight/HEAD` e
  `rev-parse`). `git --no-optional-locks status --untracked-files=all`: nessuna modifica tracciata; non
  tracciati soltanto `studio2/fase03/schema_insight/TEST_RESULTS_qwen_rev004.txt` e
  `studio2/fase03/schema_insight/sottofase_3_12_verifica.md` (SHA-256
  `a477b9c3ece9457518054193dadcc61da2d9070b9c98af6f1a1456ea02a1da4f`), entrambi preservati.
- Basi: delta `a1bcf61f0ccf20d070e92b7e2580dfdce5e9ea87`, invarianti `e058cb07dceeefa8eb4a4b6d1f6fcab5aad483db`;
  `git merge-base --is-ancestor`: e058cb0 → a1bcf61 → 3c64390. `git log e058cb0..3c64390`: due commit
  (a1bcf61 «acquisisce OK del delta e proposta autorizzata del tag insight», 3c64390 R4).
- Manifest `SCHEMA_FREEZE.json` al commit R4: 12.323 byte, SHA-256
  `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`; identico nel candidato su disco.
- Worktree del verificatore: `/Users/luker/fot-tep/.worktrees/verifica-schema-insight-rev004-indipendente`,
  creato con `git worktree add --detach … 3c64390bc4dd58c48cc4e1e388a38989b32b3143` (percorso sotto
  `.worktrees/`, escluso da Git via `.git/info/exclude`, perché la shell della sessione vede solo la cartella
  collegata `fot-tep`). Il `gitdir` registrato è il percorso di mount della VM
  (`/sessions/rcw-01y11uc227qhevrbqxjzrpzk/mnt/fot-tep/.worktrees/…`), come già per altri worktree di
  verifica; in `.git/worktrees/verifica-schema-insight-rev004-indipendente/` restano i file vuoti
  `HEAD.lock`, `index.lock` e il marker `locked`, che il filesystem montato non ha permesso di rimuovere
  («Operation not permitted»): innocui, rimovibili dall'autore. Nessun branch o checkout altrui spostato;
  nessun `git worktree prune` eseguito (le voci `prunable` dell'elenco dipendono solo dal punto di vista
  della VM). Il worktree del precedente verificatore
  `/Users/luker/fot-tep-verifica-schema-insight-rev004` è stato solo letto.

## 3. Evidenza server acquisita (log della qualifica Qwen R4)

| File | Byte | SHA-256 |
| --- | ---: | --- |
| `/Users/luker/fot-tep-schema-insight/studio2/fase03/schema_insight/TEST_RESULTS_qwen_rev004.txt` | 7.459 | `a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972` |
| `/Users/luker/.codex/attachments/a5df2913-682f-46c0-99c7-1a58cf0f8162/pasted-text.txt` | 7.459 | `a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972` |

`cmp` senza differenze: byte-identici; nessuna riscrittura, nessuna normalizzazione di terminatori o spazi
(nessun CR presente, assenza di newline finale preservata). Provenienza: trascrizione del terminale fornita
dall'autore, non file scaricato dal server; l'hash attesta l'allegato acquisito, non l'identità con un file
remoto. È evidenza supplementare esterna alle 18 voci del manifest rev. 5 e non tracciata in Git (§9, R-1).

## 4. Controlli

### A. Perimetro — ✅

`git diff --name-status a1bcf61 3c64390`: 7 percorsi, tutti in `studio2/fase03/schema_insight/`:
`DECISIONE_SCHEMA_INSIGHT.md`, `PROPOSTA_TAG_SCHEMA_INSIGHT.md`, `REPORT_SCHEMA_INSIGHT.md`,
`SCHEMA_FREEZE.json`, `test_validator.py`, `validator.py` (M) e `TEST_RESULTS_rev004.txt` (A).
`git diff --check a1bcf61 3c64390`: pulito. Contro e058cb0 si aggiungono solo i due file già portati da
a1bcf61 (`PROPOSTA_TAG_SCHEMA_INSIGHT.md`, `VERIFICA_SCHEMA_INSIGHT_rev003.md`); `docs/`, `studio2/fase03/`
fuori da `schema_insight/`, `protocol.py`, `schemas/`, `config/`, `selection/`, harness: nessuna differenza.

`validator.py`: byte-identico fra e058cb0 e a1bcf61; il diff a1bcf61→3c64390 è un solo hunk (`@@ -143,9 +143,12 @@ def context_check`),
−3/+6 righe, interamente dentro `context_check`: la regex `LABEL` è applicata alle sole otto chiavi di `owners`;
`context['normal_label'] != 'Normal'` fallisce con codice `context`/campo `normal_label`; resta il controllo
di nove valori distinti (ridondante dato che `Normal` non soddisfa la regex, ma innocuo) e il controllo
biunivoco `agent_1…agent_8`. Tutto il resto del validatore (schema, cap, `LABEL`, `scan`, `scan_normalized`,
`validate`, `validate_library`, `peers`, `diff_be`, `conformity_metrics`, CLI) è byte-identico.
`insight_v1.schema.json` (`15e0d29e…`), `leakage_rules_v1.json` (`1cf035b5…`), `requirements.txt`
(`1e536721…`): identici a e058cb0. `test_validator.py`: aggiunge le costanti 03.7, `git()`/`contract_037()`,
tre metodi R4, l'asserzione `scan({'pseudolabel': 'Normal'}) == []`, sostituisce la nona label sintetica
con quella reale e adegua da `cardinality` a `schema` il codice atteso per un insight con pseudolabel
`Normal` (coerente: lo schema rifiuta prima della cardinalità).

### B. Contratto reale 03.7 — ✅ (ricostruito da Git, non dalla fixture)

- `main` e `origin/main` locali = `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155`; tag annotato
  `studio2-fase03-pseudolabel-frozen-001` oggetto `6854c49b4034c16b8df3b11d45dd759a343463e2`, peeled
  `c16b533016db4617deb1ba96853253f117e8e32b`, antenato di a572d1c.
- `PSEUDOLABEL_MAP.json`: 1.038 byte, `b0ce81d53f11038ddf51c9ec964a1e838a7045e2e57b8ac3368f05e9a215bbc6`;
  `AGENT_ASSIGNMENT.json`: 1.667 byte, `df7434230dcd1d5460cd19e0d27e909efd40289f64d89a4b3fee2a0e55b79fcf`;
  byte identici fra `a572d1c:` e `<tag>^{}:`. Il branch candidato non contiene `pseudolabel/`
  (diramato da d815ce9): corretto che la fixture li legga da Git al commit registrato.
- Owner ricavati da `assignment[agent_k].local_fault_label` e confrontati con la vista `agents`:
  agent_1 MHMU4, agent_2 QRCCB, agent_3 GSX3L, agent_4 HEW25, agent_5 FD3GZ, agent_6 3ZGWQ, agent_7 4AMS4,
  agent_8 TYFPG (prefisso `S2-CLS-`). Otto chiavi distinte conformi a `S2-CLS-[A-Z0-9]{5}`; le otto label di
  `label_by_identifier` (F1,F2,F3,F8,F10,F13,F14,F15) coincidono con gli owner;
  `label_space == sorted(fault) + ['Normal']`; `label_by_identifier['Normal'] == 'Normal'`.
- `protocol.py::_validate_label_space` (a572d1c, righe 191–199; file identico al commit R4): nove label
  uniche, `value[-1] == "Normal"`, otto opache prima — coerente con il nuovo `context_check`.
- Script proprio (`$HOME/r4v/ctx_check.py`, contesto costruito da `git show`, contatore iniettato, senza
  tokenizer): `context_check` → 16 contratti fissi; `validate_library` → 16 insight, esattamente 2 per
  ciascuna delle 8 owner, nessuno `Normal`; rifiutati con `ContractError` codice `context`:
  `normal_label` ∈ {`S2-CLS-ZZZZZ`, `normal`, `NORMAL`, `Normal `, ` Normal`, `Norma1`}, owner `Normal`
  (messaggio «eight distinct opaque fault labels required»), nove owner. Insight con `pseudolabel: 'Normal'`
  rifiutato dallo schema (`'Normal' does not match '^S2-CLS-[A-Z0-9]{5}$'`).
- Scanner: `scan` opera solo sui campi del record passato (mai sul contesto né sul `label_space`);
  `label_neutral` esclude il campo `pseudolabel` e vieta `Normal`/`Unknown`/label opache negli altri campi,
  inclusa `evidence_scope`; `scan({'pseudolabel':'Normal'}) == []`; `observed_pattern` con `Normal` o
  `normal` → finding. Distinzione contesto / metadata pseudolabel / narrativa confermata sul codice.

### C. Qualifica tokenizer nella trascrizione — ✅ documentale (non riesecuzione)

Estratto e analizzato con `json.loads` il JSON `QWEN_TOKENIZER_QUALIFICATION`:
revisione `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`, `revision_verified: true`, modello `Qwen/Qwen3.8-27B-FP8`;
`tokenizer.json` `0997f410c57a1f4e53b09e4be8f4a172d90edd9564368fb0847030937229b9f3` e
`tokenizer_config.json` `b11349aafa7cdc6a320767cf7ceb29ed82f7eda5d65e8e0819e76f0ce947bf27` coincidenti con
`validator.py` (righe 18, 60–61) e `config/pilot_preflight.json` (righe 15, 177–179); sonde `""`=0, `a`=1,
`XMEAS(7)`=6; 16 identificativi `S2-INS-001…016` ciascuno una sola volta; `record_tokens` 83 per 001–006 e
013–016, 84 per 007–012 (10×83, 6×84); `observed_pattern_tokens`=20 ed `evidence_scope_tokens`=4 per tutti.
I 26 nomi di metodo elencati coincidono esattamente con i 26 `def test_*` di `test_validator.py` al commit
R4; 26 esiti `ok` (quello di `test_real_offline_qwen` su riga separata dopo il JSON), 0 FAIL/ERROR/skip;
`Ran 26 tests in 4.264s`, `OK`; `Python 3.12.14`; `real 0m5,093s`; checkout
`/home/luca/fot-phd-schema-insight-rev004-qK8qdl`; `HEAD si trova ora a 3c64390…`, peeled tag
`c16b5330…` stampato. La riga `R4_TOKENIZER_QUALIFICATION: tests=26, skipped=0, qualified=True` è
prodotta dallo script di lancio dell'autore, non dal codice del repository: coerente col resto, ma dichiarata.
I conteggi token non sono stati rimisurati qui (nessun tokenizer pinnato disponibile, nessuna simulazione).
La qualifica riguarda fixture sintetiche col tokenizer reale: non prova la capienza dei prompt reali né
l'ottimalità scientifica dei cap; i confini esatti dei cap restano provati con contatore iniettato.

### D. Manifest rev. 5 — ✅ 18/18

Ricalcolo con `hashlib.sha256` e `len` su `git show 3c64390:<path>` (confrontato con i byte su disco del
worktree) per le 10 `files` e le prime 6 `source_files`; su `git show a572d1c:<path>` e `<tag>^{}:<path>`
per le 2 fonti 03.7: tutte le 18 impronte e dimensioni coincidono (tabella identica a quella del verbale
precedente, §D, qui non ripetuta; valori riportati integralmente in `SCHEMA_FREEZE.json`).
`manifest_revision` 5, `contract_revision` 4, `status frozen_pending_independent_verification`,
`tag_created false`, `source_commit null` con nota anti-circolarità, `revision_base_commit` a1bcf61,
`base_commit` d815ce9, `catalog_tag_commit` = peeled di `studio2-fase03-catalogo-D1-frozen-001`.
`excluded_from_self_hash` = manifest e report, entrambi assenti dalle voci; verbali e proposta anch'essi
esterni. `previous_manifest_sha256` `d6ef52de…` = SHA-256 del manifest a e058cb0 (identico ad a1bcf61),
che è rev. 4 / contratto 3 con `previous` `96457eb4…`. `git tag -l '*insight*'`: nessun tag. Esiti storici
(rev003 Qwen, verbali precedenti) preservati; stato pending e proposta sospesa non alterati.

### E. Test rieseguiti in questa finestra — ✅

Ambiente proprio: venv `$HOME/r4v-venv` nella VM Linux aarch64 della sessione, Python 3.10.12,
jsonschema 4.26.0 (versione di `requirements.txt`); `/tmp/fot-tep-schema-r4-venv` del Mac non è
raggiungibile da questa shell e non è stato toccato. `QWEN_TOKENIZER_SNAPSHOT` non impostato; nessun
tokenizer scaricato o simulato. Comandi dalla radice del worktree del verificatore, `PYTHONDONTWRITEBYTECODE=1`:

| Prova | Comando | Esito |
| --- | --- | --- |
| Suite 03.12 | `python -m unittest studio2.fase03.schema_insight.test_validator -v` | 26 test, **25 PASS, 0 FAIL/ERROR, 1 SKIP** (`test_real_offline_qwen`: «pinned Qwen tokenizer absent; real-budget qualification pending»), 1,168 s |
| Regressioni di fase | `python -m unittest discover -s studio2/fase03/tests -v` | **16 PASS**, 0 FAIL/SKIP |
| Documentazione | `python docs/test_explanation.py` | 35 test, **14 FAIL, 1 SKIP**, 0 ERROR |
| Controlli autonomi B | `$HOME/r4v/ctx_check.py` | tutti gli esiti attesi (§B) |

I tre test R4 (`test_context_uses_frozen_037_labels_and_literal_normal`, `test_context_rejects_nonliteral_normal_label`,
`test_context_rejects_normal_as_owner`) sono PASS e leggono davvero le fonti 03.7 da Git (il worktree
condivide gli oggetti del repository). Lo SKIP locale è distinto dai 26 PASS del server dell'autore (§3, §C).
Baseline documentale: `docs/` è byte-identico fra a1bcf61, e058cb0 e 3c64390 (`git diff --quiet`), quindi
la baseline è la stessa esecuzione; gli identificativi completi dei 14 fallimenti (`FAIL:` con subtest) sono
esattamente i 14 elencati dal precedente verbale (§E): `test_condition_c_contract_and_caveats` (phrase='non un
risultato empiricamente misurato'), `test_one_flow_and_ordered_step_headings`,
`test_step27_qwen_frozen_results_and_limitations` (senza subtest e con phrase 0.833333, 0.916667, 0.944444,
'36 aggregati B non cappati sono corretti', 'C1–C4: 4/4 PASS', 'budget nominale di 1024', 'controllo secondario
distinto', 'zero astensioni'), `test_step27_qwen_protocol_stable_facts` (senza subtest, doc='html', doc='md').
Nessuna regressione documentale; il test non copre §14 né i file v2.

### F. Interfaccia 03.10 — conseguenza, non rilievo

Letti senza modifiche in `/Users/luker/fot-tep/.worktrees/studio2-harness` (branch `codex/studio2-harness`,
HEAD 5116087): `insight_adapter.py` pinna `SCHEMA_COMMIT = e058cb0…`, `SCHEMA_MANIFEST_SHA256 = d6ef52de…` e
`EXPECTED['validator.py'] = ec24159b50dc745963ccf820ccbb8ae2ce05c3894d005239aaf5c960ad9f1228` (= SHA-256 di
`validator.py` a e058cb0, ricalcolato); schema e leakage rules hanno gli stessi hash di R4. Con i byte R4
(`validator.py` `cd523d31…`, manifest `d64e4d4b…`) `load_validator` fallirebbe chiuso su `require_sha256`
prima dell'import; `context_from_inventory` usa già `normal_label: "Normal"` e il messaggio speciale di
`assert_context_compatible` («03.12 validator at e058cb0 rejects…») diventerebbe obsoleto.
REPORT_HARNESS §1.4 descrive il rilievo che R4 risolve. Aggiornare pin, commit di riferimento e messaggio è
attività di 03.10 in un commit proprio dopo la pubblicazione del tag; nulla è stato modificato qui.

## 5. Rapporto con il precedente verbale NON OK

`/Users/luker/fot-tep-verifica-schema-insight-rev004/studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004.md`,
19.064 byte, SHA-256 `5bd196820f74b7fbd5ee6736df2b72afc64afbbfb26459dc69f1fe5e15dafd19`, redatto da Codex/GPT-6
nella finestra `01a09f97-…`: resta conservato e non è stato modificato né sovrascritto (questo verbale vive in
un worktree diverso). Il suo unico rilievo bloccante, R4-V-I «indipendenza non attestabile», è chiuso da §1:
l'esecutore R4 è identificato da evidenza runtime locale come Codex/OpenAI `gpt-5.6-sol`, e questa verifica è
una sessione Claude/Anthropic distinta. I suoi controlli tecnici A–F sono stati ricostruiti autonomamente e
gli esiti coincidono; non sono stati usati come prova sostitutiva. La scrittura del log
`TEST_RESULTS_qwen_rev004.txt` nel candidato è opera di quella finestra, qui solo verificata.

## 6. Limiti

- Identità del modello in servizio di questa sessione: attestata per configurazione, non per prova API.
- Qualifica Qwen: verificata sulla trascrizione, non rieseguita; i conteggi 83/84 non sono rimisurati.
- Nessuna valutazione scientifica: capienza dei prompt reali, supporto degli insight, copertura dello scanner
  contro parafrasi restano fuori perimetro, come dichiarato dai documenti del candidato.
- Non verificato che `origin/main` remoto sia ancora a a572d1c (nessun accesso di rete): il confronto usa il
  commit registrato, che è ciò che il contratto richiede.

## 7. Verdetto

**OK.** Il delta R4 regge tecnicamente ed è verificato da una finestra e da un modello distinti da quelli
dell'esecutore. Commit verificato `3c64390bc4dd58c48cc4e1e388a38989b32b3143`; manifest rev. 5
`d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12` (12.323 byte); log server
`a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972` (7.459 byte).

## 8. Preservazione

Nessun commit, push, merge, tag, simulazione o chiamata a modelli. Non aggiornati report, decisione,
manifest, proposta, walkthrough, PROVENIENZA, harness o altre sotto-fasi. Candidato invariato (HEAD, file
tracciati e i due non tracciati). Worktree del precedente verificatore invariato.

## 9. Residui necessari alla chiusura R4-V (nessuna correzione richiesta al delta)

- **R-1** `TEST_RESULTS_qwen_rev004.txt` è non tracciato e fuori dal manifest rev. 5, mentre
  `real_tokenizer_qualification` del manifest dichiara ancora «revision_4_skipped_locally». Se l'autore vuole
  che la qualifica R4 faccia parte dell'oggetto congelato, serve un commit dell'autore che registri il log (e,
  se lo si include nel manifest, una rev. 6 con `previous_manifest_sha256 = d64e4d4b…`), aggiornando di
  conseguenza commit destinatario e impronta nel prompt di integrazione/tag. In alternativa, dichiararlo
  evidenza esterna nella consegna. Decisione dell'autore, non del verificatore.
- **R-2** 03.10: aggiornare `SCHEMA_COMMIT`, `SCHEMA_MANIFEST_SHA256`, `EXPECTED['validator.py']` e il messaggio
  di `assert_context_compatible` dell'adapter dopo il tag (§F).
- **R-3** Documentazione: il report R4 attribuisce l'esecuzione a «GPT-5» senza finestra e il §3 storico a
  «GPT-6»; il modello runtime registrato è `gpt-5.6-sol`, finestra `01a09f1b-a581-7c41-a1ec-87912c8896ef`.
  Da riportare nella fase di documentazione, non da correggere qui.
- Restano all'autore l'autorizzazione al tag e l'aggiornamento di `integrazione_tag_3_12_prompt.md` con
  commit destinatario e manifest verificati.

Letture: MAINTENANCE, Prompt_LLM, Verifica_LLM, revisione4_normal_prompt; decisione, report, manifest,
proposta, verbali e log storici del candidato; validator/test/schema/rules; fonti Git 03.7 e `protocol.py`;
preflight; verbale precedente; adapter e REPORT_HARNESS §1.4; log di sessione Codex (righe 1, 8, 347 e
ricerche mirate). Costo indicativo: 60–80 mila token; nessuna ricerca web.
