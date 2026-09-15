**Verdetto: OK** — la sotto-fase 03.12 regge; il tag `studio2-fase03-schema-insight-frozen-001` può essere proposto all'autore. Restano quattro ⚠️ non bloccanti (§5, §4, §3), che l'autore può assorbire in una revisione successiva del contratto o nel prompt del producer in 03.10.

# Verifica indipendente — sotto-fase 03.12, schema degli insight (D12, §8.9)

Modello: Claude (Cowork, sessione `claude-fable-5-1`; il modello in servizio può differire dall'identificativo configurato). Finestra diversa da quella di lavoro (Codex/GPT-6). Data: 2026-09-13.
Oggetto: branch `codex/studio2-schema-insight`, base `d815ce9`, HEAD `30ba63b` (commit che registra `TEST_RESULTS_qwen.txt`); quattro commit `b6441e9`, `43eadb6`, `924ec3d`, `30ba63b`.
Metodo: sola lettura, worktree detached `.worktrees/verifica_schema_insight` a `30ba63b`; nessuna chiamata a modelli, nessun commit, nessun tag. Unico file scritto: questo. Fixture di prova mie in `$HOME/vfx/` (fuori dal repository), ambiente `jsonschema 4.26.0` in venv Python 3.10 sulla VM locale; `transformers 5.16.1`/`tokenizers 0.23.2` installati in un ambiente separato solo per controllare il tipo restituito da `encode` (lo snapshot Qwen non è raggiungibile da qui: Hugging Face bloccato dal proxy).

## 1. Perimetro del diff — ✅

`git diff --stat d815ce9 30ba63b`: 11 file, tutti in `studio2/fase03/schema_insight/` più `studio2/PROVENIENZA.md` (+20 righe, solo sezione nuova in coda dalla riga 251, titolo «Sotto-fase 03.12 — schema degli insight»). `schemas/`, `protocol.py`, `prepare_gate.py`, `run_pilot.py`, piano, walkthrough, MAINTENANCE, `phase_b/`, `code/` intatti. `git tag | grep insight`: nessun tag. `git diff --check`: pulito. `d815ce9` è antenato di HEAD.
Le tre impronte di PROVENIENZA (`insight.schema.json`, `library.py`, `leakage.py` a `d815ce9`) ricalcolate con `git show | sha256sum`: coincidono.

## 2. Decisione vs fonti — ✅

| Riga della tabella | Fonte primaria letta | Esito |
| --- | --- | --- |
| 2 per fault / 16 / 14 | piano §8.4 «il producer alternativo genera tutti gli 8×2 insight»; §7.1/§6.8 «14 insight»; PREFLIGHT_03_0 riga 26 | ✅ costanti del piano, non ridecise |
| `insight_id` `S2-INS-[0-9]{3}`, `source_agent` `agent_[1-8]` | `protocol.py` righe 25, 42; `schemas/insight.schema.json` | ✅ |
| `pseudolabel` `^S2-CLS-[A-Z0-9]{5}$` | `protocol.py` riga 43 | ✅ identica; il report e la decisione la dichiarano **confermata** in prima riga per 03.7 |
| `evidence_scope` 240 caratteri | `protocol.py` riga 154; schema corrente | ✅ |
| `evidence_scope` 64 token | nessuna fonte | ✅ dichiarato «scelta di progetto» |
| `variable_ids` 1–8, XMEAS(1…41)/XMV(1…12) | schema corrente (1–8); limiti TEP (41/12) | ✅ 41/12 dichiarati «limiti TEP, scelta di progetto»; 9 caratteri è la lunghezza di `XMEAS(41)` |
| `observed_pattern` 800 caratteri / 192 token | PREFLIGHT_03_0 §«Correzioni incorporate» righe 24–26 | ✅ la decisione lo attribuisce al preflight e lo qualifica come scelta di progetto motivata da §8.9, non validata |
| record 1400 caratteri / 384 token | nessuna fonte | ✅ dichiarato «scelta di progetto conservativa» |
| D10: Normal non produce insight, Unknown = astensione | piano D10, righe 1114–1125 | ✅ |
| E = permutazione del solo `pseudolabel`, diff byte | piano §8.9 punto 2; D12 | ✅ |
| Identificatori letterali, no parafrasi | piano §8.9 «Due riscontri di EviFDD»; D12 | ✅ |
| Metriche validità/retry/troncamenti/token per producer e condizione | piano §8.7 tabella logging (righe 505–513), §8.9 punto 3 | ✅ |
| Tokenizer Qwen rev. `017b9c7a…`, `encode(add_special_tokens=False)` | `config/pilot_preflight.json` righe 15, 176–179; `prepare_gate.py` riga 89 | ✅ |

Nessun valore nuovo presentato come validato: il report scrive «I valori nuovi sono scelte di progetto, non soglie validate empiricamente». Le schede citate (EviFDD-Agent, P001, P041, P065) esistono in `docs/letteratura.md` e la decisione le usa nel senso corretto (P041: 256 token nel proprio compito, non giustifica 192; P001: non dimostra superiorità della concisione, come dice il piano §8.9 ultimo capoverso).
Nota minore: `requirements.txt` dice «stesse versioni del preflight» per `transformers==5.16.1`/`tokenizers==0.23.2`; le versioni non stanno in `config/pilot_preflight.json` ma in `studio2/fase03/environment_observation.json` righe 49–50 e `env/ENDPOINT_8001_16384_RECORD.md`. Coincidono.

## 3. Validatore su fixture mie — ✅ (con due lacune minori dichiarate)

Suite dell'autore rieseguita qui: 20 test, 19 PASS, 1 SKIP (tokenizer assente), come `TEST_RESULTS.txt`; harness `studio2/fase03/tests`: 16 PASS. Poi 110 casi miei (libreria propria con label `S2-CLS-V0000…`, tre ID, testo italiano), tutti con esito atteso salvo dove indicato:

- Struttura: campo mancante, tipo errato, campo extra, `None`, ID a 4 cifre, pseudolabel minuscola, newline in coda a `pseudolabel`/`insight_id`/ID → rifiutati (`schema`/`cap`). ✅
- Identificatori in `variable_ids`: «reactor temperature», «xmeas 7», `XMEAS(42)`, `XMV(13)`, `XMEAS(0)`, `XMEAS( 7)`, spazi in coda/testa → rifiutati. ✅
- Identificatori nella narrativa: «reactor temperature» (leakage), «xmeas 7», `XMEAS(42)`, `XMV(13)`, `XMEAS-7`, `XMEAS (21)`, `XMEAS(021)`, `Xmeas(21)` → rifiutati (`variable`); ID valido ma non dichiarato in `variable_ids` → rifiutato; narrativa senza ID → rifiutata. ✅
  ⚠️ due varianti passano se accanto c'è almeno un ID valido dichiarato: `XMEAS7` (senza parentesi: la regex del residuo esige un confine di parola dopo `MEAS`) e `ＸＭＥＡＳ(21)` a caratteri fullwidth (`validate` non normalizza NFKC, lo fa solo `scan`). Sono varianti malformate non intercettate, non parafrasi: coerenti con il limite dichiarato nella decisione («non dimostra l'assenza di ogni possibile parafrasi»). Non bloccante.
- Cap: 800 code point accettati, 801 rifiutati; 800 virgolette → `record_characters` 1794 > 1400 (escaping JSON contato) ✅; 800 emoji accettati (code point, non byte, come dichiarato) ✅; `evidence_scope` 240/241 ✅; solo whitespace, solo `\n`, solo NBSP → rifiutati ✅; confini token 192/193, 64/65, 384/385 con contatore iniettato ✅.
- Campi fissi: alterazione di ciascuno dei cinque → `fixed`. ✅
- Diff B→E per gli 8 riceventi: accettato con offset dei byte cambiati; rifiutati: secondo campo alterato, un solo carattere di narrativa, riordino dei record (`diff`), chiavi non ordinate, pretty-print, spazio in coda, BOM (`bytes`), mapping identità, con un punto fisso, che include la label del ricevente o Normal (`mapping`), E applicata a metà dei record, B che contiene un insight proprio, agente sbagliato (`cardinality`); audit globale a 16 accettato. ✅
- Fail-closed senza tokenizer: percorso inesistente, cartella vuota, asset con hash diverso → `tokenizer`; il CLI esige `--tokenizer-snapshot`; nessun percorso di validazione senza `count`. ✅
- Metriche su log sintetico (3 insight, 6 tentativi: JSON troncato, cap superato, valido al terzo; valido al primo; leakage poi `null`): `first_attempt_valid_rate` 1/3, `retries` 3, `retries_to_valid` {2, 0, null}, `truncated_attempts` 1, `cap_failures` 1, `unmeasurable_insights` 2 (JSON non parsabile → null, non zero) ✅. Rifiutati: numero di tentativo duplicato, salto nella sequenza, tentativo dopo il primo valido, stesso `request_id` con `prompt_tokens` diversi, `truncated` intero; accettati: stesso `request_id` con stessi token (due insight per chiamata, contati una volta), `prompt_tokens` null; raw esattamente al cap non conta come troncamento ✅. Coerente con la tabella §8.7.
- Contesto: 7 owner, Normal uguale a una label di fault, `fixed` a sei campi → rifiutati. ✅

## 4. Scanner anti-leakage — ✅ copertura, ⚠️ falsi positivi da dichiarare al producer

Copertura verificata: F1…F15 anche con spazio e zeri (`F 13`, `F013`), IDV(n), «fault #3», «guasto-15», «idv 8»; step/gradino, sticking, random variation, slow drift, drift lento, cinetica di reazione, «rapporto A/C», chiavi (`ratio_ac_s4`) e descrittori italiani del catalogo (coincidono con `selection/CATALOG_FREEZE.json`: le otto righe `variable`); nomi fisici (reattore, feed, cooling); pseudolabel, Normal, Unknown fuori dal campo `pseudolabel`; scansione anche di `evidence_scope`; omoglifi `𝐅1`, `Ｆ1` presi grazie a NFKC. `F16` passa: fuori dall'universo IDV(1–15), quindi non è identità di catalogo.
Lacune (⚠️, minori): «variazione casuale» al singolare (la regex copre solo `variazioni? casual[ei]` con spazio dopo «variazion»); `F` + spazio a larghezza zero (`F​1`, NFKC non lo rimuove). Adversariali più che plausibili.
Falsi positivi su testo neutrale legittimo, da conoscere prima di scrivere il prompt del producer in 03.10: «normal»/«unknown» come aggettivi inglesi (`\b(?:Normal|Unknown)\b` è case-insensitive: «range normal» bocciato, «valori normali» passa); «valve»/«valvola» sempre vietati anche in senso generico (per costruzione: i nomi fisici sono banditi, quindi un insight su XMV(n) non può dire «valvola»); «feed» (ma «feedback» passa); «step» inglese anche come «step 3» («passo 3» e «stepwise» passano); «A/B testing» preso da `A\s*/\s*[BC]`. Numeri di XMV/XMEAS non generano falsi positivi (`XMV(1)`, «livello 1 e 2», «fase 1», «10 samples» passano). Il giudizio è che lo scanner sia volutamente conservativo: i falsi positivi costano un retry loggato, non un'invalidità silenziosa. Va detto al producer nel prompt.

## 5. Tokenizer — ✅ PASS e impronte, ⚠️ discriminatività del test

`TEST_RESULTS_qwen.txt`: 20 test, `test_real_offline_qwen … ok`, 4,107 s, zero skip ✅. Le impronte `0997f410…` e `b11349aa…` sono codificate in `validator.offline_counter` e coincidono con `config/pilot_preflight.json` righe 178–179; il contatore fallisce chiuso se differiscono (provato al §3) e se il nome della cartella non è la revisione pinnata ✅. Con `transformers 5.16.1` ho verificato che `tokenizer.encode(...)` restituisce una `list`, quindi `len()` conta token e non chiavi (il problema `BatchEncoding` di IMPLEMENTATION_STATUS riguarda solo `apply_chat_template`, che qui non è usato) ✅.
⚠️ Il log **non stampa** né le impronte né alcun conteggio: il test reale asserisce solo `revision_verified` e 16 insight validi, e passerebbe identico anche con un contatore che restituisse sempre 0 o 2. Le impronte «coincidenti» sono quindi dimostrate dal codice, non dal log. E i cap sono **misurati a runtime** dal tokenizer pinnato, ma il log non riporta alcuna misura (per esempio i `record_tokens` della fixture). Raccomandazione, non condizione: in una revisione futura far asserire al test un conteggio noto (`counter('XMEAS(7)') > 2`) e scrivere nel log i token della fixture. Il log è fornito dall'autore (checkout `924ec3d` su albireo); non è riproducibile da questa finestra e il manifest lo dichiara onestamente in `qwen_test_provenance.commit_evidence`.

## 6. Impronte — ✅

Ricalcolate tutte le 14 di `SCHEMA_FREEZE.json` (8 `files` + 6 `source_files`), SHA-256 e byte: **14/14 coincidono** al HEAD `30ba63b`. SHA-256 del manifest = `472f1b01…` come nel report; `previous_manifest_sha256` = SHA-256 di `SCHEMA_FREEZE.json` a `924ec3d` ✅. `source_commit` `924ec3d`: i sette file di contratto sono byte-identici fra `924ec3d` e `30ba63b`, quindi il commit sorgente è coerente; il manifest non contiene se stesso né il report ✅. `catalog_tag_commit` `ab43f0b` = `studio2-fase03-catalogo-D1-frozen-001` ✅. Stato `frozen_pending_independent_verification`, `tag_created: false` ✅.

## 7. Nessuna decisione anticipata — ✅

Le fixture usano label sintetiche (`S2-CLS-T0000…`); owner, Normal e mapping E sono input del contesto, non scelti; nessun derangement generato (`diff_be` lo riceve e lo verifica soltanto). 03.10: interfaccia descritta in DECISIONE e report, harness intatto. 7.2: nessun contenuto. ✅

## 8. Report e test di documentazione — ✅

`REPORT_SCHEMA_INSIGHT.md` ha le sette sezioni di `Fase_LLM.md` §«Chiusura» nell'ordine. `python3 docs/test_explanation.py` rieseguito: 35 test, **14 fallimenti, 1 skip**, uguali al valore dichiarato prima/dopo (MAINTENANCE §5 punto 4). Nessuna coppia MD/HTML toccata.

## Conclusione

**OK.** Perimetro, fonti, invarianti, diff B→E, fail-closed, metriche e impronte reggono alla verifica sulle fonti primarie e su fixture indipendenti. Le quattro ⚠️ sono raccomandazioni: (a) test Qwen non discriminante sul conteggio e log senza misure (§5); (b) varianti `XMEAS7`/fullwidth non intercettate nella narrativa (§3); (c) «variazione casuale» e spazio a larghezza zero (§4); (d) falsi positivi «normal/unknown/valve/feed/step/A-B» da dichiarare nel prompt del producer (§4). Nessuna smentisce il contratto; se l'autore vuole assorbire (a)–(c) prima del tag, è una nuova revisione del manifest (MAINTENANCE §8.4), altrimenti il tag `studio2-fase03-schema-insight-frozen-001` può essere proposto su `30ba63b` con test tokenizer PASS.
