# ACCEPT — riverifica indipendente accounting Qwen 122B (03.13)

**Verdetto:** `ACCEPT` sul commit successore `38db018ad6fac1dd598cc9cde82efa06b27ec06b`
(tree `006317bd775acf3c081fbb08dee0f8cdb295cb7c`), parent = candidato respinto
`6431612c632b4c46f87f3edec9d662c572a4996a`.

**Modello:** Claude (Opus 4.8, id configurato `claude-opus-4-8`; il modello che serve il turno
può differire).
**Finestra:** verifica in sola lettura, 2026-09-15, eseguita via bridge del dispositivo in una
VM Linux (`Python 3.10.12`). Nessun commit, merge, push, tag, chiamata provider/Qwen, sonda,
gate, pilot o modifica a ledger reali. Il candidato e il successore **non sono stati modificati**:
i test sono stati eseguiti su worktree isolati staccati (`git worktree --detach`) in area di
scratch, con i byte dei due commit intatti (verificati per SHA-256, vedi sotto).

---

## 1. Genealogia e perimetro del delta

- `git cat-file`/`git log` confermano: successore `38db018` → parent `6431612c` → nonno
  `15e56a89`. Il candidato respinto è **esattamente** il parent dichiarato dal prompt di
  riverifica. Nessuna divergenza genealogica.
- Delta `6431612c..38db018` — **7 file, tutti dentro `studio2/fase03/`, nessuna modifica
  estranea** (nessun artefatto congelato, nessun file fuori perimetro toccato):

  | File | +/- |
  | --- | --- |
  | `studio2/fase03/harness/ledger.py` | +233 aree modificate |
  | `studio2/fase03/harness/runtime.py` | +24/- |
  | `studio2/fase03/harness/test_tokenizer_accounting.py` | +263/- |
  | `studio2/fase03/run_pilot.py` | +25/- |
  | `studio2/fase03/producer_probe.py` | +12/- |
  | `studio2/fase03/harness/CONSEGNA_CONFIG_122B_SENZA_TOKENIZE_03_13.md` | +130/- |
  | `studio2/fase03/harness/PROMPT_RIVERIFICA_CONFIG_122B_ACCOUNTING_03_13.md` | nuovo |

- **Verifica precedente**: `studio2/fase03/VERIFICA_CONFIG_122B_ACCOUNTING_03_13.md`,
  SHA-256 ricalcolato = `c7209a3f8c93380422841c648741795a9e03d6851e4e2d9a3597e794bce17052`
  — **coincide** con l'atteso. Quella verifica dichiarava quattro blocker sul candidato
  `6431612c`; sotto se ne verifica indipendentemente la chiusura.
- `docs/MAINTENANCE.md` letto e applicato: il delta resta nel perimetro `studio2/`,
  non tocca coppie `.md`/`.html` in sync né valori/artefatti congelati; la contabilità
  documentale (`docs/test_explanation.py`) resta invariata (vedi §4).

---

## 2. Esito sulle quattro domande bloccanti

Tutte e quattro dimostrate chiuse. Per ogni blocco: **difetto nel candidato respinto**
(file:riga su `6431612c`) → **correzione nel successore** (file:riga su `38db018`) → **prova**.

### Q1 — Guard obbligatorio per ogni chiamata `qwen3.5-122b` (producer, consumer budget/gate, CLI, `execute_request` diretto); messaggi = quelli trasmessi; altri modelli compatibili
- **Candidato**: il guard era *opzionale e opt-in*. `runtime.py:96` lo attivava solo
  `if accounting_guard is not None`; `ledger.account_producer_response` accettava solo gli stage
  producer (`ledger.py:255`), lasciando budget probe, stability gate, CLI (`run_pilot`) e le
  invocazioni dirette di `execute_request` **senza alcuna contabilità**.
- **Successore**: l'obbligo è ancorato al **punto comune** `execute_request`
  (`runtime.py:45-54`): `accounting_required = spec.get('model') == 'qwen3.5-122b'`; se vero,
  richiede un `TokenizerAccountingGuard` e un unico messaggio `user` il cui contenuto eguaglia
  `spec['prompt_sha256']`, **prima di intent, riserva e trasporto**. Lo `spec['model']` è
  popolato in tutti gli stage (`run_pilot.request_spec` → `config['candidate']['requested_model']`
  a `run_pilot.py:315`; `producer_probe` → `provider['model']` a `producer_probe.py:137`); budget
  e stability costruiscono il guard quando `requested_model=='qwen3.5-122b'`
  (`run_pilot.py:385-387`, `458-460`); `Provider.call` verifica `messages == expected_messages`
  (`run_pilot.py:227`).
- **Prova**: `test_A01` (producer) e `test_A02` (consumer) rifiutano prima di intent/trasporto
  senza guard; `test_non_122b_remains_compatible_without_guard` conferma la compatibilità degli
  altri modelli. Sul candidato A01/A02 **falliscono** (HarnessError non sollevata).

### Q2 — Ricalcolo prima di riusare qualunque raw/record 122B (completed, resume, retry, restart) senza nuovo trasporto
- **Candidato**: `account_producer_response` esigeva `status=='INTENT'` e sollevava su record
  completato (`ledger.py:257`, "accounting must precede request completion"); la contabilità
  girava **dopo** il ramo di trasporto, mai prima di riusare uno `stored`. Un record già
  completato privo di evento contabile poteva essere riusato senza rivalidazione.
- **Successore**: `runtime.py:82-86` contabilizza **prima** di riusare `stored` e chiama
  `validate_tokenizer_accounting_record` quando esiste `stored['record']`; il trasporto avviene
  solo con `stored is None`. `account_producer_response` (`ledger.py:299`) rivalida l'evento
  esistente, oppure marca FATAL un record completato/legacy privo di evidenza (`ledger.py:322`);
  un PASS persistito senza record finale completa idempotentemente su resume.
- **Prova**: `test_A03` (record completato rivalida i messaggi senza trasporto),
  `test_A06` (PASS senza record → ripresa idempotente),
  `test_positive_..._first_resume_restart`. Sul candidato A03 fallisce e A06/positivo **errano**.

### Q3 — Evidenza durevole, semanticamente e indipendentemente ricalcolabile (identità richiesta, messaggi, snapshot, raw, campi consumati); alterazioni coerenti di raw e hash respinte
- **Candidato**: l'evento legava `artifact_sha256 = raw_sha256` e la rivalidazione controllava
  solo la coerenza *interna* degli hash (`sha256_text(raw_json)==raw_sha256`,
  `messages_sha256` autoconsistente): una riscrittura **coerente** di `raw_json`+`raw_sha256`
  (+`artifact_sha256`) superava i controlli, e nulla legava l'identità della richiesta o i campi
  consumati dal record.
- **Successore**: `_accounting_commitment` (`ledger.py:252`, `artifact_version
  TOKENIZER_ACCOUNTING_2`) lega `request_identity_sha256`, messaggi, snapshot, hash del raw e
  conteggi; il commitment è registrato **sia** nell'evento **sia** in `request.proof_sha256`, che
  è create-once — `complete_request` rifiuta la sovrascrittura (`ledger.py:761`). Un **secondo**
  legame `_accounting_record_link` (`ledger.py:396`, `TOKENIZER_ACCOUNTING_RECORD_1`) copre i
  campi consumati: `response_id`, `returned_model`, `system_fingerprint`, `prompt/completion/total
  tokens`, `finish_reason`, `raw_output`.
- **Prova**: `test_A04` (alterazione coerente di raw e hash interni respinta). Sul candidato A04
  **fallisce** (accettata).

### Q4 — Ogni eccezione del tokenizer/template (non solo `HarnessError`) crea uno STOP durevole; un PASS valido privo del record finale completa idempotentemente
- **Candidato**: `account_producer_response` catturava **solo** `except HarnessError`
  (`ledger.py:262`). Un `ValueError`/eccezione ordinaria da `json.loads` o dal template usciva
  dal blocco `with self._transaction()` → **rollback** → **nessuno STOP** persistito (fail-open).
- **Successore**: `except Exception as exc` (`ledger.py:332`) → `_persist_accounting_stop`
  **nella stessa transazione** che committa, poi rilancia dopo il `with`; anche
  `validate_tokenizer_accounting_evidence` avvolge in `except Exception` con STOP (`ledger.py:359-363`).
- **Prova**: `test_A05` (`ValueError` del tokenizer persiste raw e STOP prima del record),
  `test_A06`. Sul candidato A05 **erra** (STOP non persistito).

### Controlli aggiuntivi (tutti soddisfatti)
- **Validazione prima di parsing/decisioni/output/gate**: la contabilità precede `evaluate(raw)`
  (`runtime.py:110-111` prima di `runtime.py:112 evaluate`); lo STOP durevole è interrogato in
  `bind_stage`, `reserve_probe` e `_ready` (`_require_no_tokenizer_accounting_stop`).
- **Token interi, non booleani, non negativi**: `type(server_prompt_tokens) is not int or
  server_prompt_tokens < 0` (`ledger.py:54`) — `type(x) is int` rifiuta correttamente `bool`.
- **Errore post-trasporto non spacciabile per prevenzione della chiamata**: il guard su messaggi
  e presenza guard è al **vertice** di `execute_request` (`runtime.py:46-54`), prima di ogni
  trasporto; un `HarnessError` sollevato dentro `transport()` è rilanciato tale e qual
  (`runtime.py:97-98`) e non contato come osservazione di trasporto.

---

## 3. Test realmente eseguiti e risultati

Ambiente: VM Linux via bridge, `Python 3.10.12`; per le suite dipendenti da `jsonschema>=4.18`
è stato usato un **venv isolato** (`jsonschema 4.26.0`, `openai 3.14.0`) che **non modifica il
candidato né il sistema dell'utente**. `transformers`/`rpds`/`openai` non presenti nell'interprete
di sistema.

**Identità dei byte verificata** (worktree scratch):
- `test_tokenizer_accounting.py` @ successore =
  `b212c73ca0946dd10295bc482bb071d8b241db952d190a08ef94b8eb92bf1e50` — **coincide** con i byte
  finali documentati nella consegna.
- runtime base `ledger.py` @ `6431612c` =
  `3f88fd4f68e73f6c47b9878769bfa179e83ce6682c64518fa38519179bd7803b` (immutato durante la prova).

| Suite | Comando | Esito |
| --- | --- | --- |
| Accounting 122B (successore) | `python -m unittest studio2.fase03.harness.test_tokenizer_accounting -v` | **Ran 9, OK** |
| **Prova rossa discriminante** — byte finali del test vs runtime del candidato respinto `6431612c` | idem, con i byte `b212c73c…` sovrapposti al worktree base | **Ran 9, FAILED (failures=4, errors=3)** — A01/A02/A03/A04 falliscono, A05/A06/positivo errano; 7 discriminanti su 9, come dichiarato |
| Harness offline | `test_harness_offline` | **Ran 20, OK** |
| Riconciliazione storico | `test_history_reconciliation` | **Ran 10, OK** |
| Contratto D9 | `test_d9` | Ran 17 → **15 verdi**, 2 errori (fixture esterna assente, §5) |
| Correzioni D9 | `test_d9_corrections` | Ran 11 → **4 verdi**, 7 errori (stessa fixture) |
| Revisioni runner | `test_revisions` | Ran 37 → **25 verdi**, 1 fail + 11 errori (stessa fixture) |
| Concorrenza/crash | `test_c01_c03` | Ran 14 → **4 verdi**, 1 fail + 9 errori (stessa fixture) |
| Replay/predecessori/contratto/quota | `test_d01_replay`, `test_d02_predecessors`, `test_d03_contract`, `test_d04_open_quota` | errori di `setUpClass` per worktree legacy assente (§5) |
| **Guardiano documentale** | `python docs/test_explanation.py` | **Ran 35, FAILED (failures=14, skipped=1)** — **NON dichiarato PASS** |

**Guardiano documentale**: 14 failure + 1 skip **identici sul successore e sul parent
`6431612c`**. Sono le 14 divergenze documentali storiche dei walkthrough v1, preesistenti e fuori
dal perimetro del delta (baseline `docs/MAINTENANCE.md` §5). Il delta **non le aumenta né le
riduce**. Non conteggiate come verde.

---

## 4. Perché gli errori delle regressioni NON pesano sul delta

Tutti gli errori/failure delle suite `test_d9`, `test_d9_corrections`, `test_revisions`,
`test_c01_c03`, `test_d0x` hanno **una sola causa comune, ambientale**: l'assenza in questa VM di
fixture esterne prodotte su percorsi assoluti del Mac dell'autore, in particolare
`missing 03.6 evidence manifest:
/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/.../EVIDENCE_MANIFEST.csv`
e il worktree legacy `/Users/luker/fot-tep-riverifica-harness-…/candidate`
(`test_d01_replay:20`, `test_d03_contract:249`, `test_revisions:33`). Il manifesto di
riferimento **non è versionato** nel repository e i percorsi Mac non esistono qui. Nessun errore
proviene da un'asserzione di logica del delta; il singolo `AssertionError: 1 != 23`
(`test_R07`) è a valle dello stesso manifesto mancante (il sottoprocesso muore in `prepare()`).
Le suite indipendenti da quella fixture passano interamente (offline 20/20, riconciliazione
10/10) e la maggioranza dei casi in `test_d9`/`test_revisions` è verde. Non ho ricostruito né
fabbricato la fixture di riferimento (sarebbe una prova inventata).

---

## 5. Limiti e non eseguiti

- **Ambientali**: le regressioni che dipendono dal worktree legacy e dall'`EVIDENCE_MANIFEST.csv`
  di riferimento non sono eseguibili in questa VM; riportate come "verdi parziali / errori da
  fixture assente", non come PASS. Sono note e attribuibili all'ambiente, non al delta.
- **Non eseguiti per progetto/perimetro** (come da consegna e vincoli di riverifica): chat
  completion, `/models`, `/version`, `/tokenize`, sonda, gate, pilot, qualificazione del servizio,
  verifica dell'identità **byte-identica del tokenizer server**, riconciliazione/applicazione
  dello storico S, merge, push, tag. L'uguaglianza locale/server qualifica **solo** la singola
  risposta contabilizzata: **non prova il tokenizer server** e **non concede execution
  authorization**.
- **Osservazione (non bloccante)**: l'attivazione del guard è ancorata al `spec['model']` =
  modello *richiesto* nella config durevole (per la config 122B validata questo coincide con il
  modello effettivo, e `producer_probe.provider_config` impone `tokenizer_accounting` proprio per
  `model=='qwen3.5-122b'`). Il modello *restituito* dal server è comunque legato nell'evidenza
  (`returned_model` nel record link), ma non è il trigger del guard: l'identità
  endpoint/modello resta responsabilità dei guard D9 esistenti (`expected_response`,
  `identity_sha256`, `server_contract`). Coerente con il perimetro dichiarato del delta.

---

## 6. Conclusione

Il successore `38db018` chiude in modo **obbligatorio, fail-closed e durevole** i quattro blocker
della verifica precedente sul candidato `6431612c`, senza introdurre modifiche estranee né
regressioni logiche. La prova rossa discriminante è riprodotta in modo indipendente e i byte del
test coincidono con quelli documentati. Le uniche mancate esecuzioni sono ambientali (fixture
esterne assenti) o fuori perimetro per progetto, e sono dichiarate come tali.

**Verdetto: `ACCEPT`.**
