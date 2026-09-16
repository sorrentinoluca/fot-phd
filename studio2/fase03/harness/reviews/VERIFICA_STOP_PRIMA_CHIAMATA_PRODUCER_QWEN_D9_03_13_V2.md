# Verifica indipendente STOP prima chiamata producer Qwen D9 — 03.13 (V2)

Verifica read-only e fail-closed del primo tentativo reale D9, eseguita nella worktree
indipendente `/Users/luker/.codex/worktrees/b567/fot-tep` (HEAD staccato `15e56a89`),
su sorgente `/Users/luker/.codex/worktrees/dd86/fot-tep`, ledger reale e artefatti privati
aperti esclusivamente in lettura (SQLite `mode=ro&immutable=1`; WAL/SHM non toccati).
Nessuna chiamata, retry, tunnel, remediation, modifica di configurazione o scrittura nel ledger.
Nessun raw, URL o credenziale è riportato. Questa V2 è indipendente dal verbale V1 già presente
nella stessa cartella (SHA-256 `ccd949280f9b1133b1f2599faf24cd6bdb68bd7fd93de1bc2d1b8f27e0778e5a`),
che non è stato letto.

## Verdetto

**OK.** Lo STOP è avvenuto correttamente alla prima e unica richiesta 122B, senza retry;
contabilità, catena documentale, hash e legami nel ledger sono coerenti e ricalcolati.

## 1. Catena commit/tree, delta, ACCEPT, configurazione

| Controllo | Atteso | Osservato |
|---|---|---|
| HEAD dd86 (`codex/studio2-config-122b-accounting`) | `0523c927…` | `0523c9279a3e760bd001daf399267c642deda02d` ✅ |
| tree di `0523c92` | `814c578f…` | `814c578f48e12f95fbfa0f19fd870881ac367958` ✅ |
| parent di `0523c92` | `b795e79f…` | `b795e79fee99f07d1c8bf267ed05203a5e54915b` ✅ |
| parent di `b795e79` | `d48477fd…` | `d48477fdab12883eb71ebd2aef3293b56e9feb4a` (tree `6848a1e6…`) ✅ |
| delta `b795e79..0523c92` | solo manifest + rapporto | 2 file aggiunti: manifest STOP (115 righe), rapporto STOP (56 righe) ✅ |
| delta `d484477..b795e79` | solo ACCEPT + copia review | 2 file aggiunti: record ACCEPT, `reviews/VERIFICA_CORREZIONE_ACCOUNTING_BATCHENCODING_122B_03_13.md` ✅ |
| file `.py` modificati in `d484477..0523c92` | 0 | 0 ✅ (codice eseguito = candidato autorizzato) |
| worktree dd86 vs tree `814c578` (tutti i `.py` di fase03, confronto `hash-object`) | identici | identici; nessun file non tracciato in `harness/` oltre `__pycache__` ✅ |
| manifest STOP SHA-256 (worktree e blob nel tree) | `23077180…` | `230771800b5cfa64bba2c9eeabc55b276dadf154441d26d05984299f9530386f` ✅ |
| rapporto STOP SHA-256 | `dd878110…` | `dd87811020b167f51d0a5f62610aea5f1a72bda50b6d819074814da3084f8ea2` ✅ |
| record ACCEPT SHA-256 | `bb1f5c28…` | `bb1f5c28924cffc42009325f64a1ecddfa464f9670b967bc57c07b1ee2d82cbe` ✅ |
| review indipendente (copia versionata e sorgente in b567) | `87966465…` | entrambe `87966465c5ec8fb5d36170b7b77d251b0086e795a97598d744e1c00c8cf8faa8`, decisione OK ✅ |
| testo ACCEPT `text_utf8_sha256` | `a3355a45…` | ricalcolato `a3355a4562466f6eb5ff5fe335e5aba558b12afb8f8d39b283f78526299a3eea` ✅ |
| configurazione privata (byte) | `3c29f8ff…` | `3c29f8ff414d27c36dcad3cf49e03ed02d8c944ed651c944e89f8df09eb30131` ✅ |
| canonico senza `execution_authorization` (ricalcolato con `canonical_json` di `common.py`, come in `guards.require_execution`) | `1305c158…` | `1305c158a98c40cb57e45b43e8d872d3d66e4d6d050d1d167c91b23e0a2fccc8` ✅ |
| autorizzazione privata (byte) | `4aa20117…` | `4aa201174e29d6b48922855ebabbfab456cd63d22be20dc391f2f6ef8a2a4040`; `decision=accepted`, autore presente, `configuration_sha256=1305c158…`, candidato `d484477`/`6848a1e6`, review `87966465…` ✅ |
| limiti autorizzati | 122B 8, 27B 8, retry 0, remediation/probe/gate non autorizzati, hard stop 200 | coincidono con il record ACCEPT ✅ |
| `expected_response` nel contratto autorizzato | alias `qwen3.5-122b`, fingerprint esplicitamente `null` | confermato in configurazione, provider 122B e binding di stage ✅ |
| `status` / `study_model_decision` | `APPROVED_FOR_PHASE03_EXECUTION` / `APPROVED` | confermati ✅ |

Il binding di stage nel ledger contiene l'`execution_config` byte-identico alla configurazione
privata completa (con `execution_authorization`), quindi l'esecuzione è avvenuta sotto la
configurazione canonica `1305c158…` con codice del candidato autorizzato.

## 2. Ledger e artefatti privati (sola lettura)

- SHA-256 ledger: `4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb` (atteso) ✅;
  ricontrollato invariato al termine della verifica; mtime ledger 01:28:45Z, WAL 0 byte (01:29:15Z).
- `PRAGMA integrity_check` = `ok`; header SQLite in modalità WAL; `user_version` 3 ✅.
- Conteggi: pilot 1 (`studio2-fase03-d9-pilot-001`), stages 1, requests 1, receipts 1,
  responses 1, events 4, external_history 4 ✅ (= manifest).
- Legami ricalcolati per l'unica richiesta `0fc7a507…`:
  - `request_id` = digest([pilot_id, `producer_conformity`, `agent_1`]) ✅;
  - `stage_run` = `binding_sha256` = digest(binding) `413aa66f…` ✅; `retry_of` = null, `quota_kind` = `base`;
  - `identity_json` coincide con lo spec `agent_1` del binding (case/contract/prompt sha, repetition 1) ✅;
  - `raw_sha256` = sha256(raw_json) = `e6489e73…` ✅; `record_sha256` = sha256(record_json) = `0136fe47…` ✅;
  - evento `tokenizer_accounting:…`: digest(detail) = `artifact_sha256` = `requests.proof_sha256` =
    `7d1d94b8…` ✅; `request_identity_sha256` = sha256(identity_json) ✅; `raw_response_sha256` = raw_sha256 ✅;
    `messages_sha256` ricalcolato ✅; snapshot tokenizer `Qwen/Qwen3.5-122B-A10B-FP8@a099dee7…` ✅;
  - evento `tokenizer_accounting_record:…`: digest(detail) = artifact ✅, lega commitment, raw e record ✅;
  - evento `suspended:…`: `artifact_sha256` = `record_sha256` ✅, motivo «response identity missing or changed»;
  - receipt: `received_utc` 01:28:45.236063Z, latenza 20 889,8 ms ✅; `raw.created` = 01:28:24Z = `intent_utc` ✅;
  - journal privato: 1 riga, SHA-256 `6c64e4412ab7c4ea8bea85ff40284869ee6bc703ec2a2b106034fd3399370d4b` ✅,
    coerente con request/receipt/raw del ledger; nessun altro file in `producer_results/`
    (nessun summary di stage, coerente con `stage_outcome_recorded=false`).
- Assenza di seconda chiamata: una sola riga in `requests`, nessun `INTENT` irrisolto, nessun
  `retry_of`, nessuna riga per stage diversi da `producer_conformity`, nessun evento
  `outcome:*`, `remediation_*`, `frozen_gate` ✅. Il record ACCEPT attesta lo stato pre-esecuzione
  (0 richieste native) con SHA `02ce8df4…` = `sha256_before` del manifest ✅.

## 3. Conferme puntuali

- **122B**: 1 richiesta tentata, 1 risposta certa e addebitabile (`status=COMPLETED`, raw e record durevoli) ✅.
- **Accounting**: `local_prompt_tokens` 1395 = `server_prompt_tokens` 1395; `completion_tokens` 2560;
  `total_tokens` 3955 = 1395 + 2560; `outcome=PASS`; stessi valori in `requests`, `record`, `raw.usage` ✅.
- **Alias**: `raw.model` = `record.returned_model` = `qwen3.5-122b` = atteso ✅.
- **Fingerprint**: atteso `null` (esplicito nel contratto autorizzato); osservato `vllm-0.27.1-934a3247`
  (non nullo) → `identity_valid=false` secondo `guards.response_identity_valid` (uguaglianza stretta su
  `returned_model` e `system_fingerprint`) ✅. STOP conforme al contratto effettivamente autorizzato.
- **Troncamento/output**: `finish_reason=length`; `completion_tokens` 2560 = `max_tokens` 2560;
  `message.content` = null, tutto il budget consumato nel campo `reasoning` (8 670 caratteri);
  `validation_error` «JSON value is empty or not text», `validation_class=structure`,
  `schema_valid_first_attempt=false`; zero coppie insight conformi ✅.
- **27B**: nessuna riga nel ledger, nessun journal `alternate_conformity`, nessuna richiesta con modello
  diverso da `qwen3.5-122b`; tunnel mai aperto per quanto verificabile dall'evidenza durevole ✅.

## 4. STOP senza retry e cumulativo

`automatic_retries`/`structural_retries` = 0 nell'autorizzazione; nessun `retry_of`; una sola riga.
Cumulativo = 4 storiche (external_history, evento `history_reconciliation`, stato `RECONCILED`,
count 4) + 1 nativa = **5** ✅. Nessun consumer, gate, remediation, final-test, OOD o scorta:
nessuna traccia nel ledger, nel journal o nel delta git. Ordine temporale coerente: ACCEPT 01:22:26Z →
intent 01:28:24Z → completamento 01:28:45Z → manifest 01:29:51Z → commit STOP 01:31:25Z.

## 5. Classificazione dei rilievi

**Fingerprint — nuova evidenza di identità/configurazione, non remediation del prompt.**
La qualificazione 122B (`QUALIFICATION_122B.json`, SHA `4e7e2b67…`, `PASS_NON_GENERATIVE`, 0 chiamate
generative) elenca `system_fingerprint`, `vllm_version`, `reasoning_parser` e `thinking_configuration`
fra i campi `not_exposed`; il contratto ha codificato `null`. La prima risposta generativa espone un
fingerprint non nullo (che incorpora una versione di serving) e un campo `reasoning` separato dal
`content`: entrambi sono fatti nuovi sull'identità e la configurazione del servizio, non difetti del
prompt. Il guard ha applicato correttamente il contratto; la riconciliazione richiede una
ri-qualificazione dell'identità osservata e una revisione di `expected_response` (e della
documentazione del servizio) nella configurazione privata, che cambia lo SHA canonico e quindi
richiede nuova review indipendente, nuovo ACCEPT e nuova autorizzazione scritta (`require_execution`
lega l'autorizzazione all'hash esatto). Inoltre l'evento `suspended:` blocca ogni stage
(`ledger._prerequisites`: «pilot suspended; requires a new reviewed disposition») e il codice non
prevede una via di ripresa: serve una disposizione riesaminata, esterna al harness.

**Troncamento — classe 3 (cap) con contemporaneo output strutturalmente non valido (classe 1).**
Secondo la classificazione prespecificata (DECISIONI_AUTORE_03_8 §«Classificazione», PIANO_STATISTICO
§11.1) si conservano entrambi gli errori: cap (`finish_reason=length` al `max_tokens` 2560 = 2048
thinking minimo + 512 riserva) e strutturale (`content` nullo, JSON non parsabile). Evidenza
forense: il cap è stato raggiunto interamente nel canale `reasoning`, con `response_format`
`json_schema strict` inviato e nessun controllo di thinking inviato dalla configurazione 122B
(documentato come `NOT_EXPOSED`). Il raw troncato non è un insight scientifico e non è stato usato
come tale.

**Ammissibilità di un unico diff del solo prompt.** Le regole prespecificate ammettono una sola
remediation, esclusivamente sul prompt del producer, per difetti diagnosticati delle classi 1–4;
classi 1 e 3 rientrano nel perimetro, quindi *preparare* l'artefatto `REMEDIATION_T9_001.md`
(evento, classe, evidenza, diff concreto) è ammissibile come proposta documentale. Non è però
ammissibile autorizzarlo o eseguirlo ora, perché: (a) prima di qualunque nuova chiamata vanno
riconciliate e riverificate l'identità osservata e la configurazione, con autorizzazione scritta sul
diff concreto e sulla configurazione riconciliata; (b) il ledger è sospeso e `authorize_remediation`
richiede un evento `outcome:producer_conformity` FAIL con diagnosi coincidente con una
`validation_class` registrata, evento che non esiste (stage interrotto a 1/8 chiamate,
`stage_outcome_recorded=false`); (c) la diagnosi deve dimostrare un difetto del prompt: l'evidenza
mostra il cap consumato nel canale di reasoning, la cui configurazione non è esposta né
controllata dal prompt; senza questa dimostrazione il diff sarebbe un'ipotesi, e le regole rinviano
a una revisione con riverifica indipendente quando l'errore non nasce dal prompt. Restano vietati
modifiche a schema, validatore, dati, parametri congelati (incluso il passaggio a un altro
candidato di budget, ammesso solo nella sonda) e selezione sulla qualità semantica.

## 6. Percorso scientificamente ammissibile successivo (non autorizzato da questo verbale)

1. Ri-qualificare l'identità 122B con l'evidenza generativa già acquisita (fingerprint, presenza
   del canale `reasoning`), aggiornare documentazione del servizio ed `expected_response` nella
   configurazione privata; nuova review indipendente, nuovo ACCEPT e nuova autorizzazione scritta
   sul nuovo hash canonico.
2. Disposizione riesaminata e scritta sul ledger sospeso (il harness non offre ripresa automatica),
   preservando la chiamata 5 come addebitata una volta e il raw come evidenza forense.
3. Solo dopo, decisione dell'autore fra: completamento/registrazione dell'esito della conformità
   secondo le regole T9, oppure preparazione di `REMEDIATION_T9_001.md` con un unico diff del solo
   prompt, autorizzazione scritta sul diff concreto e ripetizione di tutte le otto chiamate.
   Nessuna nuova chiamata prima dei punti 1–2.

## Note operative

- Effetto collaterale corretto: un `git status` iniziale ha lasciato un `index.lock` vuoto in
  `.git/worktrees/fot-tep/` (metadati git della worktree dd86); rimosso con permesso esplicito.
  Nessun oggetto, ref o file di lavoro è stato modificato. Le verifiche git successive hanno usato solo
  comandi sugli oggetti (`cat-file`, `diff-tree`, `ls-tree`, `hash-object`).
- Nessun commit, push, merge o tag. Questo file è l'unica scrittura, nella worktree b567, non tracciata.
- Limiti: il tokenizer non è stato ricaricato localmente (assenza di `tokenizers`/`transformers` nell'ambiente
  di verifica); l'accounting è verificato tramite uguaglianza locale/server registrata e commitment
  ricalcolato. L'assenza di chiamate 27B è verificata sull'evidenza durevole (ledger, journal, git).
