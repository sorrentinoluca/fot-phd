NON OK

# Riverifica R4-V della sottofase 03.12 — 2026-09-14

Il delta supera i controlli tecnici eseguiti. Il verdetto NON OK riguarda la chiusura
come **verifica indipendente**: non è dimostrata la distinzione effettiva del modello e
della finestra rispetto all'esecutore R4. Non è stato trovato un difetto implementativo
che richieda correzione nei controlli A–F sotto descritti.

## Esecutore, finestra e oggetto

- Verificatore: Codex, agente basato su **GPT-6**, identità esposta dalle istruzioni runtime.
  Variante specifica e identificativo del backend non esposti: non attestati.
- Finestra effettiva: `01a09f97-5041-7aa2-92b8-905cf228cd8d`, letta da
  `CODEX_THREAD_ID`; questa sessione non ha implementato il delta durante la conversazione.
- Il report candidato, apertura R4, dichiara «Codex, agente basato su GPT-5, in questa
  finestra», ma non identifica quella finestra e non fornisce una prova runtime del modello.
  Le attribuzioni GPT-6 e Claude nelle sezioni precedenti riguardano revisioni storiche.
  Non uso tali attribuzioni per inventare l'identità dell'esecutore R4. Worktree separato
  e ricostruzione autonoma delle fonti non dimostrano da soli l'indipendenza richiesta.
- Candidato: `/Users/luker/fot-tep-schema-insight`, branch
  `codex/studio2-schema-insight`, HEAD verificato prima dell'acquisizione:
  `3c64390bc4dd58c48cc4e1e388a38989b32b3143`.
- Base delta: `a1bcf61f0ccf20d070e92b7e2580dfdce5e9ea87`;
  base degli invarianti: `e058cb07dceeefa8eb4a4b6d1f6fcab5aad483db`.
- Worktree di verifica nuovo, detached al commit R4:
  `/Users/luker/fot-tep-verifica-schema-insight-rev004`.
  Creato con `git worktree add --detach /Users/luker/fot-tep-verifica-schema-insight-rev004 3c64390bc4dd58c48cc4e1e388a38989b32b3143`;
  nessun branch o checkout altrui spostato.
- Manifest verificato: 12.323 byte, SHA-256
  `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`.

## Acquisizione documentale — OK

Fonte: `/Users/luker/.codex/attachments/a5df2913-682f-46c0-99c7-1a58cf0f8162/pasted-text.txt`.
Destinazione: `/Users/luker/fot-tep-schema-insight/studio2/fase03/schema_insight/TEST_RESULTS_qwen_rev004.txt`.
Entrambi: **7.459 byte**, SHA-256
`a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972`.

Lettura con `Path.read_bytes()`, verifica dell'hash atteso prima della scrittura,
creazione esclusiva `open('xb')` della destinazione prima assente, confronto integrale
`source.read_bytes() == destination.read_bytes()` e ricalcolo di dimensione/hash: OK.
Nessuna normalizzazione, intestazione o modifica dei terminatori; preservata anche
l'assenza di newline finale. La trascrizione dichiara il checkout
`/home/luca/fot-phd-schema-insight-rev004-qK8qdl` e il commit R4 esatto.

È una **trascrizione del terminale fornita dall'autore**, non un file originale scaricato
dal server. L'hash attesta i byte dell'allegato acquisito e non prova l'identità con un
file remoto. Nessun accesso al server né riesecuzione remota da questa finestra.
La copia è evidenza supplementare **esterna alle 18 voci del manifest rev. 5**.
Report, decisione, manifest e proposta del tag sono rimasti intatti, anche dove registrano
lo stato storico precedente all'acquisizione.

## A. Perimetro del delta — OK

`git diff --stat a1bcf61 3c64390` e `git diff --name-only a1bcf61 3c64390`:
sette file, tutti in `studio2/fase03/schema_insight/`: decisione, proposta del tag,
report, manifest, nuovo `TEST_RESULTS_rev004.txt`, `test_validator.py`, `validator.py`.
333 inserimenti, 32 eliminazioni. Nessun altro percorso modificato.

`git diff e058cb0 3c64390 -- studio2/fase03/schema_insight/validator.py`:
unico hunk funzionale in `context_check` (righe 146–154 del candidato). La regex è
applicata alle sole otto owner; `normal_label` deve essere esattamente `Normal`;
restano nove valori distinti. Il controllo biunivoco degli otto agenti è preservato.

Confronto addizionale dei byte del validatore, escludendo soltanto le righe della
funzione individuate tramite AST: identità completa, SHA-256 del resto in entrambe
le revisioni `9aa2c1bfea97ed604044f289eca2286ec3d9981df2269e837dc8a64bb24d67a9`.
Schema JSON, leakage rules e requirements byte-identici a e058cb0. Cap, regex,
scanner, normalizzazione di sola rilevazione e diff B/E sono quindi invariati.
Il diff dei test aggiunge le fonti Git 03.7 e tre metodi R4, aggiorna la fixture,
verifica lo scanner su metadata Normal e adegua l'errore Normal da cardinalità a schema.

`git merge-base --is-ancestor` conferma a1bcf61 → R4 ed e058cb0 → a1bcf61.
I due verbali precedenti non sono modificati dal delta e non approvano R4.

## B. Contratto reale 03.7 — OK

Fonti lette direttamente con `git show`, senza usare `fixture()` o `contract_037()`
come prova primaria:

- main registrato: `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155`;
- tag `studio2-fase03-pseudolabel-frozen-001`, oggetto
  `6854c49b4034c16b8df3b11d45dd759a343463e2`;
- peeled `c16b533016db4617deb1ba96853253f117e8e32b`, antenato del main registrato;
- `PSEUDOLABEL_MAP.json` e `AGENT_ASSIGNMENT.json`: byte identici fra tag e main,
  rispettivamente 1.038 e 1.667 byte, hash nella tabella D.

Il confronto usa il commit registrato, senza presumere che il ref mobile main sia
ancora fermo lì. Da `assignment[agent].identifier` è stata ricavata la label attraverso
`label_by_identifier`, poi confrontata con la vista `agents` dell'assegnazione:

| Agente | Owner |
| --- | --- |
| agent_1 | S2-CLS-MHMU4 |
| agent_2 | S2-CLS-QRCCB |
| agent_3 | S2-CLS-GSX3L |
| agent_4 | S2-CLS-HEW25 |
| agent_5 | S2-CLS-FD3GZ |
| agent_6 | S2-CLS-3ZGWQ |
| agent_7 | S2-CLS-4AMS4 |
| agent_8 | S2-CLS-TYFPG |

Otto chiavi distinte conformi a `S2-CLS-[A-Z0-9]{5}`, otto agenti esatti;
`label_space == sorted(owners) + ['Normal']` e `label_by_identifier['Normal'] == 'Normal'`.
Letto anche `protocol.py::_validate_label_space` al main registrato, righe 191–199:
richiede nove label uniche, Normal ultima e letterale, otto label opache prima.

Costruito in memoria un contesto proprio con due contratti sintetici per ogni owner,
ID S2-INS-001…016, scope `Development window.`, variabile `XMEAS(7)`.
**16 gruppi di controlli diretti riusciti**, senza tokenizer: contesto valido; nove valori
negativi di normal_label (`S2-CLS-ZZZZZ`, `normal`, `NORMAL`, `Normal `, `Normal\n`,
null, 0, array e oggetto); owner Normal; cardinalità 2×8; metadata Normal; narrativa
Normal in observed_pattern e in evidence_scope; schema positivo sui 16 record e negativo
su un insight con pseudolabel Normal. Tutti i negativi del contesto danno ContractError
con codice `context`. Nessuna fixture scientifica o inferenza generata.

Lo scanner `scan` opera sui campi dell'insight, non ricorsivamente sul contesto o sul
label_space. `scan({'pseudolabel':'Normal'}) == []`; il controllo `label_neutral` vieta
Normal fuori da pseudolabel, anche nello scope. Non si deve passare un intero prompt o
label_space a `scan` come se fosse un record. Lo schema dell'insight continua a rifiutare
Normal; la suite verifica 16 insight, due per fault, nessuno per Normal, e 14 peer.

## C. Qualificazione Qwen nella trascrizione — OK documentale

Estratto con regex ancorata alla riga `QWEN_TOKENIZER_QUALIFICATION` e analizzato con
`json.loads`. Verificati:

- revisione `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`, `revision_verified: true`;
- tokenizer.json: `0997f410c57a1f4e53b09e4be8f4a172d90edd9564368fb0847030937229b9f3`;
- tokenizer_config.json: `b11349aafa7cdc6a320767cf7ceb29ed82f7eda5d65e8e0819e76f0ce947bf27`;
- uguaglianza dei due hash con `offline_counter.expected_hashes` estratto dall'AST
  e con `config/pilot_preflight.json`, righe 177–179; revisione coincidente col preflight;
- sonde: stringa vuota 0, `a` 1, `XMEAS(7)` 6;
- 16 identificativi unici S2-INS-001…016, ciascuno presente una volta.

| Insight | record_tokens | observed_pattern_tokens | evidence_scope_tokens |
| --- | ---: | ---: | ---: |
| 001–006 | 83 | 20 | 4 |
| 007–012 | 84 | 20 | 4 |
| 013–016 | 83 | 20 | 4 |

Dieci record da 83 token e sei da 84: il conteggio uniforme 84 appartiene alla fixture
storica. I conteggi sopra sono verificati **nel log**, non rimisurati localmente.
I 26 nomi di test elencati coincidono esattamente con i metodi `test_*` del candidato;
26 esiti `ok`, compreso quello su riga separata dopo il JSON. Riepilogo `Ran 26 tests in
4.264s`, `OK`, `tests=26, skipped=0, qualified=True` coerenti. Python dichiarato 3.12.14;
durata complessiva `real 0m5,093s`, distinta dai 4,264 secondi unittest.

Il codice verifica gli hash prima del caricamento, usa `local_files_only=True`,
`trust_remote_code=False` ed `encode(add_special_tokens=False)`. Il test reale blocca
socket di rete. Questa verifica della trascrizione non è una riesecuzione indipendente
sul server. Il risultato qualifica fixture sintetiche con tokenizer reale: non prova
capienza dei prompt reali, supporto empirico degli insight o ottimalità scientifica dei cap.
Le prove di confine della suite usano contatori iniettati e non sono qualifica Qwen.

## D. Manifest — OK, 18/18

Ricalcolo tramite `hashlib.sha256(raw).hexdigest()` e `len(raw)`, confrontati con ogni
voce del manifest. Per i dieci file candidati: `git show 3c64390:<path>` e confronto
con il worktree. Per le prime sei source_files: byte verificati anche a
`d815ce96d928254de79209f02e11a561445764cd`, base dichiarata. Per le ultime due:
main a572d1c e tag 03.7 dichiarati, non il checkout R4 che non le contiene.

| File | Byte | SHA-256 ricalcolato | Esito |
| --- | ---: | --- | --- |
| `studio2/fase03/schema_insight/DECISIONE_SCHEMA_INSIGHT.md` | 9671 | `6923e8d428f1aee0fa2b8adc3584601ece123894b4c8b6b81ba60c79545c8520` | OK |
| `studio2/fase03/schema_insight/insight_v1.schema.json` | 1222 | `15e0d29e033c1d699d4f1114b5fdf378ad1cea8398c89b133403a92983229de6` | OK |
| `studio2/fase03/schema_insight/validator.py` | 17636 | `cd523d3105e02de99e7cc09bf0c2c4c052c1ae1776c8da37a9b57e869b1aa508` | OK |
| `studio2/fase03/schema_insight/test_validator.py` | 16516 | `b8f6d735fbd2f626e8bb75c36d06432e5d3bc59061bed4a936ffca25393267f7` | OK |
| `studio2/fase03/schema_insight/leakage_rules_v1.json` | 1184 | `1cf035b5d5e7a7f4cc909dc0a04f6f0da6580284d32710f3ee6924533c706a7a` | OK |
| `studio2/fase03/schema_insight/requirements.txt` | 131 | `1e53672145c42bd48e9e2f8540d89a224be2b6d8665599272ccb7506c238de86` | OK |
| `studio2/fase03/schema_insight/TEST_RESULTS.txt` | 3393 | `9c8c7d51149cb033e584166ced334ee233a27622314d99192b4b8649640ae0b0` | OK |
| `studio2/fase03/schema_insight/TEST_RESULTS_qwen.txt` | 2821 | `7113bf87d758e2dd0bbb3fed5fecfac7aa0a4629825db69c5046ebef5db233e0` | OK |
| `studio2/fase03/schema_insight/TEST_RESULTS_qwen_rev003.txt` | 5626 | `908cb77ee620e60afe42eae20c9723b91715037140f12ea2c75838c1da472a3c` | OK |
| `studio2/fase03/schema_insight/TEST_RESULTS_rev004.txt` | 1501 | `fc3bae8d48aa09ab0478e00a653fedffd366ac5c7a4994f9a7b76fb555b4b93b` | OK |
| `studio2/fase03/schemas/insight.schema.json` | 894 | `9d9de7dc9bd1795aea5f8fe323a2579eb2b5cc52ca8c753c594a292570fab9a1` | OK |
| `studio2/fase03/prepare_gate.py` | 8659 | `8ac42c805dd7d425c00f1715a284975c2b76af92139f6792997fcae24491ac04` | OK |
| `studio2/fase03/config/pilot_preflight.json` | 11636 | `6bf50982d2ba8040e18c468999a110c426e3b9be217d5d9be5f272df6515f5f5` | OK |
| `studio2/fase03/selection/CATALOG_FREEZE.json` | 6894 | `68b8461a6382c93e1a5dd8dc6c9def66b26b2ec865f0bc0786dd88fa95acedda` | OK |
| `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` | 161230 | `8d79b662ecc14358d2a2e29f699f6cab2ec6e41b584415ed2d93247a8df24ce1` | OK |
| `docs/letteratura.md` | 70392 | `a53b265a5df0c45c95d2cdfa7c0ed361af084ebcf5e658bd458814fa05f8c291` | OK |
| `studio2/fase03/pseudolabel/PSEUDOLABEL_MAP.json` | 1038 | `b0ce81d53f11038ddf51c9ec964a1e838a7045e2e57b8ac3368f05e9a215bbc6` | OK |
| `studio2/fase03/pseudolabel/AGENT_ASSIGNMENT.json` | 1667 | `df7434230dcd1d5460cd19e0d27e909efd40289f64d89a4b3fee2a0e55b79fcf` | OK |

Revisioni manifest 5 / contratto 4; source_commit null con nota anti-circolarità;
`excluded_from_self_hash` esclude manifest e report, entrambi assenti dalle voci.
La proposta e i verbali sono anch'essi esterni all'elenco. Stato
`frozen_pending_independent_verification`, verifica R4 pending, `tag_created: false`;
`git tag --list studio2-fase03-schema-insight-frozen-001` vuoto nella repository locale.
Il tag catalogo peeled coincide con `ab43f0b20f45cdb475c0caf52c6f7afcbae50891`.

Catena ricalcolata per ogni previous_manifest_sha256:

| Manifest contenuto a | Precedente a | SHA-256 del precedente |
| --- | --- | --- |
| 3c64390 | e058cb0 (identico ad a1bcf61) | d6ef52de0f573edf3e5d6eb5ad3530400c5f63e6bcfa6579a93f21fdfb8865b5 |
| e058cb0 | 44dae2f | 96457eb4f209335e5a2bc3c120245cea3a184f2c5fd741508f865f4e8a9a692e |
| 44dae2f | 30ba63b | 472f1b01b09f189e724a1fb11b96ab28b303b1914b4601b576cf5de91292428c |
| 30ba63b | 924ec3d | e99745a11679971d0ed1ba5db5aae55e33ae6c0966af0443aad6f5165320e28e |

Gli esiti storici restano tali: il nuovo log non modifica manifest o approvazioni precedenti.
Nessun verdetto rende automaticamente efficace il freeze o crea un tag.

## E. Prove rieseguite in questa finestra

Ambiente compatibile verificato: `/tmp/fot-tep-schema-r4-venv/bin/python`, Python
3.13.15 x86_64, jsonschema 4.26.0. Venv preesistente riusato senza modificarlo.
`QWEN_TOKENIZER_SNAPSHOT` non impostato; nessuno snapshot pinnato disponibile nei
percorsi cache controllati. Non sono stati scaricati tokenizer né simulati contatori reali.
Il precedente problema rpds arm64/x86_64 è storico; non si è verificato nell'ambiente usato.

Comandi dalla radice del worktree di verifica, con `PYTHONDONTWRITEBYTECODE=1`:

```bash
/tmp/fot-tep-schema-r4-venv/bin/python -m unittest studio2.fase03.schema_insight.test_validator -v
/tmp/fot-tep-schema-r4-venv/bin/python -m unittest discover -s studio2/fase03/tests -v
/tmp/fot-tep-schema-r4-venv/bin/python docs/test_explanation.py
```

| Prova | Esito effettivo |
| --- | --- |
| Suite 03.12 | 26 test, 25 PASS, 0 FAIL/ERROR, 1 SKIP; 4,120 s |
| Regressioni di fase | 16 PASS, 0 FAIL/ERROR/SKIP; 0,040 s |
| Controlli autonomi B | 16 gruppi riusciti; nessuna misurazione token |
| Documentazione | 35 test, 14 fallimenti, 0 errori, 1 skip |
| Server autore, solo evidenza acquisita | 26 PASS, 0 errori/skip; 4,264 s |

Skip locale: `test_real_offline_qwen`, «pinned Qwen tokenizer absent; real-budget
qualification pending». Distinto dai 26 PASS server documentati dall'autore.

Per la baseline documentale è stato letto `git show a1bcf61:docs/test_explanation.py`,
verificato byte-identico al file R4 ed eseguito in un subprocess con __file__ impostato
al percorso assoluto corrente. Tutti i file fuori da schema_insight sono byte-identici
tra base e R4; l'ispezione degli accessi del test conferma che non usa quella cartella.
Questa esecuzione verifica quindi gli stessi input della baseline senza spostare checkout.
Il confronto usa gli identificativi completi `FAIL:`, inclusi i subtest, non solo il numero.
La successiva esecuzione diretta R4 conferma gli stessi 14 esiti (0,117 / 0,123 s).

Identificativi (tutti in `__main__.UnifiedConversationChecks`):

1. test_condition_c_contract_and_caveats, phrase='non un risultato empiricamente misurato'
2. test_one_flow_and_ordered_step_headings
3. test_step27_qwen_frozen_results_and_limitations, phrase='0.944444'
4. test_step27_qwen_frozen_results_and_limitations, phrase='0.916667'
5. test_step27_qwen_frozen_results_and_limitations, phrase='0.833333'
6. test_step27_qwen_frozen_results_and_limitations, phrase='zero astensioni'
7. test_step27_qwen_frozen_results_and_limitations, phrase='C1–C4: 4/4 PASS'
8. test_step27_qwen_frozen_results_and_limitations, phrase='controllo secondario distinto'
9. test_step27_qwen_frozen_results_and_limitations, phrase='budget nominale di 1024'
10. test_step27_qwen_frozen_results_and_limitations, phrase='36 aggregati B non cappati sono corretti'
11. test_step27_qwen_frozen_results_and_limitations, metodo senza subtest
12. test_step27_qwen_protocol_stable_facts, doc='html'
13. test_step27_qwen_protocol_stable_facts, doc='md'
14. test_step27_qwen_protocol_stable_facts, metodo senza subtest

Skip: `TutorialChecks.setUpClass`, legacy part-1 walkthrough assente. Nessuna regressione.
Questa suite non copre §14 o i walkthrough v2 e non sostituisce la verifica del contratto.

## F. Interfaccia 03.10 — conseguenza verificata in sola lettura

Letti nel worktree `/Users/luker/fot-tep/.worktrees/studio2-harness`:
`studio2/fase03/harness/insight_adapter.py` e `REPORT_HARNESS.md` §1.4.
Il file effettivo è insight_adapter.py (il nome adapter_0312 nel prompt indica il ruolo).
`load_validator` controlla EXPECTED prima dell'import; pin corrente del validatore
`ec24159b50dc745963ccf820ccbb8ae2ce05c3894d005239aaf5c960ad9f1228`, diverso da R4
`cd523d3105e02de99e7cc09bf0c2c4c052c1ae1776c8da37a9b57e869b1aa508`.
Schema e leakage rules mantengono gli hash già pinnati. SCHEMA_COMMIT/SCHEMA_MANIFEST_SHA256
identificano ancora e058cb0 e d6ef52de…; il contesto dell'adapter contiene già Normal letterale.
L'adapter attuale rifiuterebbe dunque i nuovi byte al controllo hash. Aggiornare pin e
riferimenti dopo il passaggio previsto di pubblicazione è attività di 03.10, non un difetto
da correggere qui. Nessun file harness modificato o chiamata sperimentale eseguita.

## Rilievo bloccante e condizione di chiusura

**R4-V-I — indipendenza non attestabile.** Manca una prova verificabile dell'identità
runtime e della finestra dell'esecutore R4, distinta da questa. La sola autodichiarazione
nel report non basta a certificare il requisito esplicito della richiesta e del prompt R4-V.
Condizione di chiusura: documentare una distinzione effettiva di modello e finestra e
ottenere l'approvazione R4-V da un verificatore di cui tale distinzione sia dimostrabile.
Nessuna correzione implementativa proposta o eseguita; nessun ulteriore test server
è richiesto soltanto per ricopiare la trascrizione già verificata.

## Preservazione e letture

Unica scrittura nel candidato: il log supplementare sopra indicato. Unico nuovo documento
nel worktree di verifica: questo verbale. Il prompt preesistente
`studio2/fase03/schema_insight/sottofase_3_12_verifica.md` resta non tracciato, hash
`a477b9c3ece9457518054193dadcc61da2d9070b9c98af6f1a1456ea02a1da4f`.
Nessun commit, push, merge, tag, aggiornamento PROVENIENZA/walkthrough o altra sottofase;
nessuna simulazione o inferenza. Non sono stati sovrascritti verbali precedenti.

Letture: MAINTENANCE, Prompt_LLM, Verifica_LLM, revisione4_normal_prompt; decisione,
report, manifest, proposta, verbali e log storici; implementazione/test/schema/rules;
fonti Git 03.7, protocol, preflight; test documentale e adapter/report 03.10.
Piano e letteratura sono stati verificati per impronta, senza riaprire la rassegna:
il presente audit riguarda il delta R4. Costo indicativo delle letture mirate: 25–35 mila
token; nessuna ricerca web. Stato pending e Fase 03 aperta preservati.
