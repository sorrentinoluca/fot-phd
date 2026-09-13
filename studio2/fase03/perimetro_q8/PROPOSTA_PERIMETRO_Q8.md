# Sotto-fase 03.4 — Perimetro del codice Q8: proposta di decisione

**Stato: proposta, non decisione.** Chiude il punto 2 di `docs/fot_walkthrough_conversazione_studio2.md`
§0.1 solo se l'autore la conferma; la modifica a `docs/MAINTENANCE.md`, al walkthrough e a
`studio2/PROVENIENZA.md` va eseguita in un'altra finestra, dopo la conferma.

| Campo | Valore |
| --- | --- |
| Data | 2026-09-13 |
| Modello | Claude Fable 5.1 (`claude-fable-5-1`), ragionamento esteso — profilo **decisionale** (`Fase_LLM.md`) |
| Finestra | Cowork, branch `codex/studio2-perimetro-q8` creato da `origin/main` = `b7f359fc593b74cf756f3b407ddabe5027f91b0f` |
| Chiamate a modelli / simulazioni | nessuna |
| File modificati fuori da `studio2/fase03/perimetro_q8/` | nessuno; `phase_b/`, `code/`, `docs/`, artefatti congelati intatti (verificato con `git status` prima del commit) |

## 0. File letti, con impronte

Tutte le impronte sono SHA-256 sul contenuto a HEAD `b7f359f`, calcolate in questa finestra.

| File | Sezioni lette | SHA-256 |
| --- | --- | --- |
| `docs/MAINTENANCE.md` | §1, §2, §4, §5, §8.1–8.6 | `4a75b0677c5eb09d36274cb36be37a1ec73afb2ca86b274cc36193812465647b` |
| `docs/fot_walkthrough_conversazione_studio2.md` | §0, §0.1 (tabella, punto 2 testualmente), indice §4.1–4.3, «Lavoro che resta» di §4.3 | `f9c10c0082aed6ce6ce58c5be7ec74968140528bd6bd120a67cc5dc738e6c0ee` |
| `docs/prompts/Fase_LLM.md` | integrale | `6dbdcd271d60e35a9066c36a6e1183809d50a11c6ef2bfecc654bf155bcfb981` |
| `docs/prompts/Prompt_LLM.md` | nota operativa e regola di costo | `4c11026ba170667ae9b45bb363a07592499698d7a735302eb36eacf6d963fe20` |
| `studio2/PROVENIENZA.md` | §5 integrale; §4 righe R1/R2/U1; indice | `ce767320179bf722372cfa1deb00bb34354f39fbca71f7b9ee95784fe02e15de` |
| `studio2/fase03/IMPLEMENTATION_STATUS.md` | integrale | `a2be51a41a76fc27d34c8a1e4bbf36e5c45a66cc5ef6b2b8740f5da02383ecd5` |
| `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md` (**non tracciato** in Git a HEAD; letto dalla copia di lavoro) | §2, §3, §5 | `9cceafa0e5094a6318b555025ebe057805dabd6f130c84463769e551ef1b7e2b` |
| `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` | §6.4, §6.5, §6.7, §6.8 (righe 285–298), §8.5, §8.9, D10 (righe 1114–1132), changelog riga 65 | `8d79b662ecc14358d2a2e29f699f6cab2ec6e41b584415ed2d93247a8df24ce1` |
| `docs/fot_walkthrough_conversazione.md` (prima esposizione) | «Dalle feature ai flag», «Dai flag al JSON, fino al testo neutrale», «Evaluator · signature vector» (righe 253–345), «Caratterizzazione del payload comunicativo FoT–TEP» e «Payload e limiti» (1259–1300, 1421–1440) | `fb9de573a903f3d8c599cc51fdfbf5d9f8df79b44d34617d95fdd68bd30fa3d6` |
| Codice di `phase_b/` e `code/` | vedi inventario §2; letto integralmente `guard.py`, `config/protocol.py`, `insights/library.py`, `evaluation/metrics.py`, `tests/test_phase_a_hashes.py`, `tests/helpers.py`; per gli altri intestazione, import e punti citati da D10 | impronte in §2 |

La pipeline feature → flag → JSON → testo neutrale → firma 697-D è stata letta dalla prima
esposizione e riscontrata sul codice: la firma è `code/evaluate_verbalizer_v2.py::signature_vector`
(41 XMEAS × 17 componenti in `[0,1]`, ordine fisso `level/trend/residual/diff/rapid`), costruita sul
JSON strutturato di `code/tep_verbalize_v2.py::verbalize_feature_table`, a sua volta alimentato dalle
feature per finestra di `code/tep_features.py::analyze_window` e dalle soglie congelate in
`code/verbalizer_config_v2.json` (`abs_shift_sigma = 1.9695333234149084`, la stessa citata nel
worked example della prima esposizione). Il testo neutrale è `render_text` nello stesso modulo. La
baseline numerica del primo studio (prototipi medi 697-D, distanza L1) è
`phase_b/baselines/c02b_shared_numeric_prototypes/run_baseline.py`, che importa `signature_vector`
da `code/` via `sys.path`.

## 1. Criterio di classificazione, fissato prima di applicarlo

Un file è **harness riutilizzabile** se il suo comportamento è funzione dei soli argomenti (config,
record, tabelle) e non incorpora numeri, identità o esiti del primo studio se non attraverso
parametri; i suoi test devono poter girare su fixture sintetiche. È **artefatto** se è una
configurazione, un prompt, una predizione, un risultato, una libreria di insight, un mapping
evaluator-side, un manifest di freeze, o un test che verifica uno di questi per contenuto o impronta.

Il criterio produce una terza classe che va nominata, perché è quella che conta per questa decisione:
**harness con costanti di protocollo** — logica generale (validazione, derangement, metriche,
bootstrap, rendering) che però codifica dentro il sorgente le assunzioni del primo studio: quattro
agenti `agent_1..agent_4`, cinque label con `Normal` in ultima posizione, idioma posizionale
`label_space[:-1]`, due insight per fault, sei insight peer, dodici cluster fisici in quattro strati
da tre. Questi moduli sono riutilizzabili **come pattern** (contratti, invarianti, controlli
fail-closed) ma **non come import** né come copia letterale: una copia dovrebbe comunque riscrivere
le costanti, e un import trascinerebbe il validatore a quattro agenti dentro lo studio 2.

Un file classificato harness resta comunque **immodificabile** se è nel manifest
`phase_b/PHASE_B_PROTOCOL_HASHES.json` o è raggiunto da un tag: la classificazione dice se il
*pattern* è trasferibile, non se il *file* è scrivibile. Questo è il punto che il testo del punto 2
di §0.1 confonde, e da cui dipende tutto il resto.

Nota sulle assunzioni elencate nella richiesta: il primo studio ha **quattro** agenti e quattro
pseudolabel più `Normal` (`phase_b/config/protocol.py` righe 42–52; `PHASE_B_PROTOCOL_FREEZE.md` §B
«exactly four agents»), non sette. I «sette» compaiono solo nel piano §8.4 (riga 698) come «i sette
agenti diversi dal proprietario» nel disegno a otto dello studio 2. L'inventario usa i numeri del
codice.

## 2. Inventario

Colonne: percorso · commit dell'ultima modifica · SHA-256 · copertura (H = in
`PHASE_B_PROTOCOL_HASHES.json`; T = contenuto identico a HEAD sotto il tag indicato; P = pinnato da
`phase_b/tests/test_phase_a_hashes.py`) · funzione · assunzioni del primo studio incorporate ·
classe (**H** harness riutilizzabile, **HC** harness con costanti di protocollo, **A** artefatto) ·
sotto-fasi che lo richiedono come pattern o come input.

Verifiche eseguite in questa finestra: tutti i 56 file del manifest esistono e hanno l'impronta
dichiarata (0 mismatch); i quattro file `code/` pinnati da `test_phase_a_hashes.py` coincidono;
nessun modulo sotto `studio2/` importa da `phase_b` (grep su `*.py`: 0 occorrenze); le undici
occorrenze di `label_space[:-1]` di D10 sono esattamente quelle riportate qui sotto (più
`labels[:-1]` in `config/protocol.py`, che D10 conta a parte come validatore).

### 2.1 `phase_b/` — nucleo del protocollo (commit `70a736e`, `c431cd8`, `585e629`, `3d86f64` del 2026-08-29; tag `phase-b-protocol-frozen` = `3d86f64`, `phase-b-results-frozen` = `45ec4ee`, `phase-b-exp2-qwen-protocol-frozen-001` = `d9bb95c`)

| Percorso | Commit | SHA-256 | Copertura | Funzione | Assunzioni incorporate | Classe | Richiesto da |
| --- | --- | --- | --- | --- | --- | :---: | --- |
| `phase_b/config/protocol.py` | `c431cd87ee0ef563ad77cc6b0b330e6b61bf9735` | `fa2488d1d964c98682c3fc82d650bbe43d74a3f9f041e5745ca71a51331e7b2e` | H, T | validatore stretto della config; `derive_opaque_pseudolabel` (SHA-256 + base32, prefisso `CLS-`) | `len(labels) == 5`, `labels[-1] == "Normal"`, `labels[:-1]` opachi di pari lunghezza, `agent_1..agent_4`, 2 esempi/classe da batch 1–2, 2 insight/fault, provider `openai`, modello `gpt-5.6-terra`, R=3, bootstrap 10 000 | HC | 03.7 (derivazione delle pseudolabel: `studio2/fase03/protocol.py` oggi ne valida solo la forma `S2-CLS-[A-Z0-9]{5}`, la derivazione non è ancora scritta), 03.10 |
| `phase_b/config/protocol_config.json` | `c431cd8…` | `a67b721609647c9a428c9895de1f0d684547e9fc8cf91f0a626f823af094e135` | H, T | configurazione del protocollo Exp1 | tutte le precedenti, con i valori | A | — (solo lettura per confronto) |
| `phase_b/config/evaluator_side/condition_e_derangements.json` | `585e629…` | `e8a0bdbf5a0b7c04d1ba978fd7e18f55b933d8062125ea11c1fb117f9990b231` | H, T | derangement fissi di E per 4 agenti | 3 peer per agente | A | 03.7 (solo come forma dell'artefatto) |
| `phase_b/insights/library.py` | `70a736e0f7a0b18fc6c28a92fd789a73d1d25c22` | `679f2074067f13c29f63237e25dd0c86a979d48232ecf0c333cf8e7e41fe93c9` | H, T | `Insight` (5 campi), validazione globale, filtro peer-only, `build_fixed_derangements` (rotazione ciclica), `corrupt_peer_insights` con controllo «cambia solo `pseudolabel`» | `agent_[1-4]`, `INS-\d{3}`, `CLS-[A-Z0-9]{5}`, `label_space[:-1]` (righe 82, 120), `len(peers) == 6`, derangement = rotazione di un passo (zero punti fissi per costruzione, ma non l'unico possibile) | HC | 03.7 (derangement a 7 peer), 03.10, 03.12 (schema: già riscritto in `studio2/fase03/protocol.py` e `schemas/`) |
| `phase_b/insights/insight.schema.json` | `585e629…` | `c3020aed97db6e9722661e04c2498c280f2d6cc10cdc6f364a14727200298fae` | H, T | schema JSON a 5 campi | cardinalità e regex del primo studio | A | 03.12 (confronto) |
| `phase_b/conditions/builders.py` | `70a736e…` | `5a4906304e5ab09ad12cd004e8838dd337ac2f5544ac03d0c392f21ae2009bd9` | H, T | rendering deterministico dei prompt A/B/E, hash del prompt, blocco `PEER INSIGHTS` | 4 esempi locali (2+2), template in `phase_b/prompts/`, `INS-` numerati per agente | HC | 03.10 (già riscritto come `render_diagnostic_prompt` in `studio2/fase03/protocol.py`) |
| `phase_b/conditions/parser.py` | `70a736e…` | `bdddfe99ba6e4328a071ea94c221a91cc5942252865691a280bcd6687301eb99` | H, T | parser JSON stretto dell'output diagnostico | label nel `label_space` passato; `abstain`/`predicted_label` | H | 03.10 (già adattato: PROVENIENZA §5) |
| `phase_b/conditions/retry.py` | `70a736e…` | `ba144230e0e99111c7b6154acc7574aec32aeddb2146bf2a39ff8d6af5321b29` | H, T | retry deterministico limitato | `max_retries` da config | H | 03.10 |
| `phase_b/conditions/diagnostic_output.schema.json` | `70a736e…` | `5abed6a82be2ecd1a6654a32124338fe08c1dceae0c24b51e0ec9e6c99363b19` | H, T | schema dell'output diagnostico | — | A | 03.12 (confronto; `studio2/fase03/schemas/` ne ha già uno proprio) |
| `phase_b/evaluation/metrics.py` | `70a736e…` | `9aa8e6d12957c10e3059c95dcb93efa59679e97a7374500aea9e86ad26e9f0cb` | H, T | metriche offline: `accuracy` con astensione nel denominatore (numero 1 di §8.5), `abstention_rate` (numero 2), trasferimento appaiato B−A/E−A, recall per pseudolabel, confusione | scope `seen/unseen` da `local_fault_label`; `per_repetition` fisso a `(1, 2, 3)`; `positive_at_least_3_of_4_agents`; `unit_warning` «only 12 unseen physical fault-runs»; condizioni `A/B/E` | HC | 03.8 (endpoint a tre numeri; **il numero 3 manca**, come §8.5 dichiara), 03.10 (logging), 03.13 |
| `phase_b/evaluation/bootstrap.py` | `70a736e…` | `524751fede48e678ee66b9f783be8fdeaefe7bebe32772e5367ba9be9c3d9df5` | H, T | bootstrap a cluster fisici stratificato per pseudolabel | `label_space[:-1]` (riga 108), `set(strata.values()) == {3}`, `len(clusters) == 12`, 3 righe agente per cluster | HC | 03.8 (bootstrap a 9 classi + astensione) |
| `phase_b/evaluation/aggregation.py` | `70a736e…` | `ce44166fcb9f871d2b46073e8049a3d6ca6fca0aadfbcf49067d5af95f3bc212` | H, T | aggregazione R=3 per (agente, condizione, caso) | maggioranza 2 su 3, altrimenti astensione aggregata | HC | 03.8/03.10 (politica R, decisione 11) |
| `phase_b/evaluation/records.py` | `70a736e…` | `2dd9e98fe3b11f72cdb1f0a02b2dfec52292869b5e59a060edac7283594f67d4` | H, T | `RunRecord` e schema del record di run | campi del primo studio | H | 03.10 (logging §8.7) |
| `phase_b/evaluation/token_logging.py` | `70a736e…` | `70ece0a3700c1b3212c72d574f3b54511cf3bbf2044fc62cc310e113770c36fd` | H, T | contabilità token dai log del provider | fonte `token_accounting_source` | H | 03.10 |
| `phase_b/execution/generate_final_insights.py` | `3d86f64d43e14e7e0de520cb047ca1043bf9c1c0` | `3109f67fc3eb52e85fc51b61bb056a5026a7e6b37d6a93d6de7e28aaaf06a641` | H, T | generazione one-shot della libreria insight da development 1–5 | `label_space[:-1]` (riga 351), OpenAI Responses, bundle per 4 agenti | HC | 7.2 (fuori Fase 03), pattern per la sonda producer di 03.13 |
| `phase_b/execution/openai_adapter.py` | `c431cd8…` | `39d7317e3a0c7808d297617356dfc580120b0f32c58a5e6e71eb45bf9f3eee06` | H, T | adapter isolato OpenAI Responses | provider OpenAI | A (superato da `exp2/qwen/adapter.py`) | — |
| `phase_b/local_knowledge/build_local_examples.py` | `70a736e…` | `89cf043bc6ea199099384704ba6a636ecdb0f84cc5125ab48de4ff49d76bd1c9` | H, T | costruisce 2 esempi neutrali V2 per classe locale e agente, con guardia held-out | `label_space[:-1]` (righe 72, 85), batch 1–2, `code/tep_cache/`, importa `tep_verbalize_v2` da `code/` via `sys.path` | HC | 03.6 (pattern: come si producono gli esempi locali dai run e dal verbalizzatore congelato) |
| `phase_b/prompts/leakage.py` | `585e629…` | `da1a39c72d36d7c04d276097d2de4c57fecb94642027870bd802b449b429ee76` | H, T | scanner anti-leakage sul testo prompt-facing | regex su `F1/F8/F10/F13`, `Class-[ABCD]` | HC | 03.6, 03.10 (da riscrivere per gli 8 fault D1: F1/F2/F3/F8/F10/F13/F14/F15) |
| `phase_b/guard.py` | `585e629…` | `11be9b333286162ace362ba380a9fd4bbb7c0ff7b41c881e140d40a493d2d0d3` | — (tag T) | guardia fail-closed sull'accesso ai dati held-out | percorso `tep_heldout/` e manifest held-out del primo studio | H (pattern) | 03.11 (guardia sui run di test), 03.10 |
| `phase_b/exp2/qwen/adapter.py` | `d9bb95c31bdeb2f1608aaedc52f25b98de9bbf96` | `49de085165f9aad99b17fa7713c0aae5fffded535cccda5dd508d7b65fef6bcf` | T (`phase-b-exp2-qwen-*`) | adapter OpenAI-compatible locale; importa `phase_b.conditions.parser/retry` | provider vLLM, `label_space` come argomento | H | 03.10 (già adattato: PROVENIENZA §5) |
| `phase_b/exp2/qwen/capability_probe.py` | `d9bb95c…` | `b383611d4c7c7bd55215c0458827efec63ca0261264ed737ee05c8ba2a5f9dcd` | T | capability probe e contabilità richieste | endpoint 8000@4096 del tempo | H | 03.13 (già adattato: PROVENIENZA §5) |
| `phase_b/exp2/qwen/common.py` | `b4bb61fbf49ab30b6809c341df9d45a1c28e9e49` | `0cbf1b7f6f4af4ee55164245b5982d4ff7c8c4798b9b7cd557b979e070c19ef3` | T | glue Exp2: importa `load_protocol_config`, `render_diagnostic_prompt`, `validate_global_insights` da `phase_b` | `agent_1..agent_4` → `LKP-00n` | HC | — (dimostra che il riuso per import trascina il validatore a 4 agenti) |
| `phase_b/baselines/c02b_shared_numeric_prototypes/run_baseline.py` | `72af2a7ffa97544ec10cc6d0e6c65253e21de22c` | `5a0d4572ba8f8ac462abba3da1f72af780751fc3652c934cf8096f3dbb452bfa` | — (`protocol_freeze_manifest.json` proprio; protocollo `229f901a…`) | baseline numerica: prototipi medi 697-D per classe, distanza L1 minima, astensione su pareggio `1e-12`; importa `signature_vector`, `load_case`, `tep_verbalize_v2` da `code/` via `sys.path` | 5 casi development per prototipo, label letterali `CLS-ZOGAA…` + `Normal` (riga 573), `tep_heldout/mode1`, mapping evaluator-side del primo studio | HC | 03.9 (pattern della regola L1 e dell'astensione) |
| `phase_b/tests/helpers.py` | `70a736e…` | `01c86cce01a8f17f883cca7c755a2c0d000fdcb9486f717d6a001632e50b4502` | — | fixture: 2 insight per agente dalla config reale | legge `protocol_config.json` reale | HC | 03.10 (pattern delle fixture) |
| `phase_b/tests/test_insights_conditions.py` | `70a736e…` | `f3380f10eab2d535aad80aab5ecd066a6843ccef08df0447d177818fddc5cc39` | — | test di libreria, peer-only, derangement, rendering | `label_space[:-1]` ×3 (righe 39, 105, 119) | HC | 03.7, 03.10 (riscrivere: devono **verificare** la separazione fault/Normal, D10) |
| `phase_b/tests/test_config_and_examples.py` | `c431cd8…` | `9921752bfaff172266ab6fcb656fac088d3fd0b83f6649f25319ddec63777701` | — | test config e esempi locali | `label_space[:-1]` (riga 31) | HC | 03.10 |
| `phase_b/tests/test_final_insights.py` | `3d86f64…` | `1a49398c0c0663fa58a718bf4a3fe205449852fed962df078c3a82a3b9fb50de` | — | test sulla libreria insight **finale** | `label_space[:-1]` (riga 78); verifica un artefatto | A | — |
| `phase_b/tests/test_metrics_bootstrap_records.py` | `70a736e…` | `69932a837b8cc44f46f2636c86472cf48cf71f8468bb209479e7bcef2c8e94fb` | — | test metriche/bootstrap/record | 12 cluster, 4 strati | HC | 03.8 |
| `phase_b/tests/test_parser_retry_guard.py` | `70a736e…` | `b4f2d5b1a3fab36f60422da2349989ef18300ddcc806aa4db27e3215024fe1ad` | — | test parser, retry, guardia | — | H | 03.10 (pattern) |
| `phase_b/tests/test_phase_a_hashes.py` | `585e629…` | `1879f8bc1a39ba0ab43c8bf57a8661b06bd26ba0daf011a871eaa4f0a67ee8f8` | — | **pinna per impronta 4 file di `code/`** | impronte `552a0b8a…`, `3a9129b6…`, `972e06fa…`, `cbade7a2…` | A | — (prova che `code/` è congelato di fatto) |
| `phase_b/PHASE_B_PROTOCOL_FREEZE.md` | `3d86f64…` | `18bfde5636e3a8326f9665b4d14e72ab95c227afb184b412e9691284d113d969` | H | freeze del protocollo `phase-b-fot-1.0.0` | 4 agenti, batch 1–5, held-out 15 casi | A | — |
| `phase_b/PHASE_B_PROTOCOL_HASHES.json` | `3d86f64…` | `62de38497f6ab648b7af8d4cb182307b3504153674b96c05fd8b4f7231824570` | (è il manifest) | 56 impronte: 52 in `phase_b/`, **4 in `code/`** | — | A | — |
| `phase_b/README.md` | `e8011fa11cc23df18ec55572d2b1c7c74d2f0b0f` | `386a688522ef0c896481633d3e236ab0404761a6926b5f298ed5ee832d8d1294` | — | indice; «Frozen paths. … Do not rename or move them» | — | A | — |

### 2.2 `code/` — pipeline di Fase A (commit `3fd960a` 2026-08-28; tag `phase-a-verbalizer-v2-complete` = `0a45817`, `phase-a-reproducibility-complete` = `145b6b7`, identici a HEAD per i quattro file congelati)

| Percorso | Commit | SHA-256 | Copertura | Funzione | Assunzioni incorporate | Classe | Richiesto da |
| --- | --- | --- | --- | --- | --- | :---: | --- |
| `code/tep_features.py` | `3fd960a192bafacbaabce9471e3c3614d6b2d2db` | `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c` | H, P, T | `XMEAS` (41), `BaselineStats`, `analyze_window` (shift/slope/residual/diff/raw ratio), `iter_time_windows`, `analyze_case_windows` | nessuna label, nessun agente; solo schema colonne TEP e 41 XMEAS | H | 03.6 (già copiato byte-identico in `studio2/fase02/analysis/tep_features.py`, commit `dec2010`) |
| `code/tep_verbalize_v2.py` | `3fd960a…` | `3a9129b6353cac6f8c9e02281282f137dd07885b1f882ca633ee9d6bf52393be` | H, P, T | `load_config` (rifiuta versioni ≠ 2.0 e set di soglie diverso), `load_development_baseline` (N1–N5 in `[0,250)`), `_variable_signature`, `render_text`, `verbalize_feature_table`, `verbalize_case` | `fault_injection_h = 10`, finestre da 5 h, baseline 5 blocchi da 50 h, vocabolario italiano congelato; nessuna label | HC (costanti di Fase A, non di protocollo) | 03.6 (testo neutrale e JSON strutturato dai 40 run) |
| `code/verbalizer_config_v2.json` | `3fd960a…` | `552a0b8a9cf9e416de77daa7aca2d8dee152a2700bbfaab4ae5e039081712519` | H, P, T | soglie congelate (4), logica temporale, vocabolario; `dataset_commit 309b944f…` | soglie calibrate su N1–N5 del primo studio | A | 03.6 (**da decidere in 03.5/03.6** se le soglie restano queste o vengono ricalibrate: non qui) |
| `code/evaluate_verbalizer_v2.py` | `3fd960a…` | `972e06fa29bee5a58d57ca757bd158c5cddaa2f4ed12eb5c739169c7fef79a92` | H, P, T | `signature_vector` (**la 697-D**), `signature_similarity`, valutazione stabilità/separabilità | ordine e semantica delle 17 componenti; `n_windows` dal JSON | H | 03.6, 03.9 |
| `code/tep_characterize_v2.py` | `3fd960a…` | `440b2488b30144944e52ad27f21f53eede781550efdef5a1f6251cf8e2630560` | — (già in PROVENIENZA §7) | caratterizzazione con firme temporali | costanti 10/50/5 | HC | 03.6 (già letto per la specifica dei run §6.2) |
| `code/characterize_fot_communication_payload.py` | `430590001922b28d618b739b12e3471e7ebd0afa` | `d12b71d29152a4831e8cc10576ead51f6aaabbf6de87385a313dcaf74e36bb3c` | — | caratterizzazione del payload Exp1: importa `phase_b.conditions.builders`, `phase_b.insights`, `tep_features`; ricostruisce i prompt e ne verifica gli hash contro i prediction log | percorsi e impronte di Exp1, `agent_1..4`, 8 insight | HC (misura un artefatto) | 03.10/03.13 (pattern per le metriche di conformità §8.9: byte, token, retry) |
| `code/test_features.py` | `3fd960a…` | `28cf1c7de607fbeca84b383b7efbae0a491a970e7879575c36788d71e0364349` | — | unit test delle feature | — | H | 03.6 (pattern) |
| `code/test_verbalize_v2.py` | `3fd960a…` | `17e0ae0f9a09f52eae05ab8014fb8077edfd3347cf84b79339bd90a83c2ad672` | — | unit test del renderer V2 | vocabolario, soglie | HC | 03.6 (pattern) |
| `code/test_characterize_fot_communication_payload.py` | `4305900…` | `f0d896afe75f2fb0aacccf5fc7a434ed43d780cf79bfe1cb568a1db3e89eedd6` | — | test della caratterizzazione | artefatti Exp1 | A | — |

### 2.3 Che cosa è già dentro `studio2/` (per non contarlo due volte)

| Percorso | Commit | SHA-256 | Che cosa ha già assorbito | Assunzioni ereditate |
| --- | --- | --- | --- | --- |
| `studio2/fase03/protocol.py` | `55433a4fed016a4a6e5aca526c6b472488106340` | `39ea42b3c5da7c22974b80f79fa4b924274c75086ccaaf4365af580a5474bb55` | contratti a 8 agenti (`AGENT_IDS` 1..8), 9 label `S2-CLS-…` + `Normal`, 14 insight peer, validazione derangement a 7 peer senza punti fissi, rendering A/B-LF/E-LF, parser stretto, controllo E «cambia solo `pseudolabel`»; nessun import da `phase_b` | **l'idioma posizionale** `value[-1] == "Normal"` / `labels[:-1]` (righe 191–199, 273, 276, 326, 349, 420) è stato riprodotto, ma ora è **validato** da `_validate_label_space`; la generazione dei derangement è solo nella fixture sintetica (`synthetic_fixture.py` riga 102, rotazione di un passo) |
| `studio2/fase02/analysis/tep_features.py` | `dec201092b6404c7a2d83cdcfa5ed13cc03f7775` | `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c` (= `code/tep_features.py`) | copia byte-identica; inclusa nel `PRECALIBRATION_FREEZE.json` (riga 65); `REPORT_FASE02.md` riga 215 la chiama «copia adattabile» | **nessuna riga in `PROVENIENZA.md`** (grep su `tep_features` e `cbade7a2`: 0 in `PROVENIENZA.md`) |

## 3. Il punto 2 di §0.1 è ancora aperto?

**Operativamente no; testualmente sì.** In dettaglio.

**Che cosa §8.2 ha già chiuso.** La regola «gli adattamenti necessari allo studio 2 sono file nuovi
dentro il suo perimetro, non modifiche agli originali; gli originali si leggono nella versione
identificata da commit e impronta» è esattamente ciò che la sotto-fase 03.0 ha fatto per cinque file
(PROVENIENZA §5, commit `9e3d903`): `adapter.py`, `capability_probe.py`, `conditions/parser.py`,
`insights/library.py` e `B_LOCAL_FIRST_V1.txt` sono stati riscritti in `studio2/fase03/` a 8 agenti,
14 insight e 9 label, senza toccare `phase_b/` e senza importarne nulla. L'estensione a 8 agenti, le
9 pseudolabel con astensione e il controllo E a campo singolo — tre delle quattro voci che il punto 2
cita come «richiedono di scrivere dentro `phase_b/`» — sono **già in `studio2/fase03/protocol.py`**
(`IMPLEMENTATION_STATUS.md`: validatore 16/14, controllo E-LF, renderer, 16 test offline). Nessuna
di esse ha richiesto di scrivere in `phase_b/`.

**Perché il punto 2 dice il contrario.** La premessa «richiedono tutti di scrivere dentro
`phase_b/`» nasce dalla lettura del piano: §8.5 dice che la terza metrica «manca» da
`phase_b/evaluation/metrics.py`, D10 elenca le undici occorrenze di `label_space[:-1]` «in
`phase_b/`». Ma il piano descrive dove il codice **vive**, non dove va **modificato**; letto insieme
a §8.2, dice che il numero 3 va calcolato da codice nuovo in `studio2/` e che l'idioma posizionale
**non va toccato** perché D10 ha scelto `Unknown` = astensione proprio per non doverlo riscrivere. Il
punto 2 è quindi un'inferenza sbagliata tratta da un testo corretto: va chiuso come tale, con la
correzione scritta, non aggirato.

**Che cosa resta irrisolto, con precisione.** Quattro cose, nessuna delle quali richiede di aprire
`phase_b/`:

1. **Lo stato di `code/` in §1 è ambiguo, e la lettura corretta è «congelato per impronta».** §1
   elenca `code/` sotto «Codice e verifica», non fra gli artefatti congelati; il pattern
   `tep_*_v2/` della riga «Artefatti congelati» ha lo slash finale e nel repository corrisponde alle
   directory `tep_test_v2/`, `tep_validation_v2/`, `tep_exp3_v2_heldout/` e `code/tep_analysis_v2/`,
   non ai moduli `code/tep_verbalize_v2.py` e `code/tep_characterize_v2.py`. Però quattro file di
   `code/` (`tep_features.py`, `tep_verbalize_v2.py`, `verbalizer_config_v2.json`,
   `evaluate_verbalizer_v2.py`) sono nel manifest `PHASE_B_PROTOCOL_HASHES.json`, sono pinnati da
   `phase_b/tests/test_phase_a_hashes.py` e sono identici a HEAD sotto i cinque tag verificati (`phase-a-verbalizer-v2-complete`, `phase-a-reproducibility-complete`, `phase-b-protocol-frozen`, `phase-b-results-frozen`, `phase-b-exp2-qwen-protocol-frozen-001`);
   `build_local_examples.py` e `run_baseline.py` li importano da `code/` via `sys.path` e ne
   registrano le impronte. Modificarli romperebbe il manifest, un test e la catena di provenienza di
   Exp1, C02B ed Exp2. Sono artefatti congelati **di fatto** e §2 («hash… non si toccano mai») lo
   copre già; §1 non lo dice. Gli altri file di `code/` (`tep_characterize_v2.py`,
   `characterize_fot_communication_payload.py`, `calibrate_thresholds_v2.py`, i test, `tep_cache/`)
   non sono pinnati, ma sono codice del primo studio: modificarli non è vietato dalla lettera di §1 e
   non serve a nulla nello studio 2, che per §8.1 scrive solo in `studio2/`. La proposta è dirlo in §1
   (testo in §5).
2. **Copia o import.** §8.2 dice «gli artefatti non si duplicano se basta referenziarli», e per il
   codice il referenziare è l'import. Il repository ha entrambi i precedenti: `studio2/fase02/analysis/`
   contiene una **copia byte-identica** di `code/tep_features.py` (dentro il freeze pre-calibrazione,
   ma senza riga in PROVENIENZA), mentre `phase_b/local_knowledge/` e `c02b/` **importano** da `code/`
   via `sys.path`. Nessun modulo di `studio2/` importa da `phase_b/`. Una regola esplicita manca, e
   03.6 la incontra subito (feature, verbalizzatore e `signature_vector` servono invariati). La proposta
   è in §5 (importare in sola lettura ciò che non incorpora costanti di protocollo; copiare solo ciò
   che si deve cambiare; ogni copia con riga PROVENIENZA e impronta dell'originale). Questa è una
   scelta dell'autore: le due strade sono entrambe compatibili con §8.2.
3. **Test da riscrivere, non da copiare.** `phase_b/tests/` importa `phase_b.*`, legge
   `protocol_config.json` a 4 agenti e contiene cinque delle undici occorrenze posizionali; D10 chiede
   che i test nuovi **verifichino** la separazione fault/`Normal`/astensione invece di riprodurla.
   `studio2/fase03/tests/` esiste già (2 file); il pattern dei test del primo studio è riusabile, i
   file no. Non è una decisione: è una conseguenza di §8.2 che va detta in 03.10.
4. **L'idioma posizionale è entrato in `studio2/`.** `studio2/fase03/protocol.py` riproduce
   `labels[:-1]` con `Normal` in ultima posizione, ma lo **valida** (`_validate_label_space` fallisce se
   l'ultima non è `Normal`). Con D10 congelata (`Unknown` = astensione, fuori dallo spazio delle
   etichette) questo è coerente e non è un difetto. Lo registro perché la scelta fra idioma posizionale
   validato e categorie semantiche esplicite appartiene a 03.12 (schema) e 03.7 (pseudolabel), e non va
   chiusa qui.

## 4. Opzioni

### (a) Nessuna modifica a §1; si conferma §8.2 e si chiude il punto come «già coperto», con nota esplicativa

| Su | Conseguenza |
| --- | --- |
| §1 | invariato: `phase_b/` resta «non si modifica mai»; `code/` resta ambiguo (punto 3.1) |
| §8.2 | invariato; la regola copia/import resta implicita (punto 3.2) |
| PROVENIENZA | ogni adattamento continua a ricevere la riga di §5, come già fatto; il precedente della copia di `tep_features.py` senza riga resta non sanato |
| Test | riscritti in `studio2/`, per conseguenza di §8.2 |
| §8.5 verificabilità | intatta: tutto il nuovo è in `studio2/` e raggiungibile da `main`; gli originali restano verificabili per impronta e tag |
| Rischio | la stessa inferenza sbagliata del punto 2 può ripresentarsi alla prima sotto-fase che legge §8.5 o D10 senza §8.2; l'ambiguità su `code/` resta |

### (b) §1 separa dentro `phase_b/` l'harness riutilizzabile dall'artefatto, elencando i file

| Su | Conseguenza |
| --- | --- |
| §1 | contraddice la sua stessa regola («Non elenca i file: gli elenchi marciscono… L'unica enumerazione ammessa è quella delle coppie in sync»); e l'elenco sarebbe inerte, perché **tutti** i moduli che il criterio §1 classifica harness (`library.py`, `metrics.py`, `bootstrap.py`, `builders.py`, `parser.py`, `retry.py`, `records.py`, `token_logging.py`, `build_local_examples.py`, `leakage.py`, `config/protocol.py`) sono nel manifest `PHASE_B_PROTOCOL_HASHES.json` e sotto tag: dichiararli «harness» non li rende scrivibili senza rompere §2. L'unico harness fuori manifest è `guard.py`, coperto comunque dai tag |
| §8.2 | dovrebbe spiegare che «harness» significa «pattern trasferibile» e non «file modificabile», cioè la stessa precisazione dell'opzione (a′) ma in una sede più ambigua |
| PROVENIENZA | invariata |
| Test | invariati rispetto ad (a) |
| §8.5 | se «harness» venisse letto come «modificabile in luogo», si romperebbero manifest, `test_protocol_freeze.py`, `test_phase_a_hashes.py` e la catena di Exp1/Exp2/C02B; §8.4 vieta la modifica in luogo di un artefatto congelato |
| Giudizio | o inerte o pericolosa; è la strada indicata dalla colonna «Decisione da chiudere in» del punto 2, e la proposta è di non seguirla |

### (c) Nuovo perimetro `phase_b/q8/` **oppure** `studio2/harness/` con copie identificate per impronta

| Su | Conseguenza |
| --- | --- |
| `phase_b/q8/` | scrive sotto `phase_b/`: viola §1 e §8.1 («tutto il nuovo: codice… in `studio2/`») e la nota «Frozen paths» del README di `phase_b/`; mescola due studi nella stessa radice che il repository finale deve tenere «recuperabili e riconoscibili» (§8). Da escludere |
| `studio2/harness/` | è già, di fatto, `studio2/fase03/` (`protocol.py`, `run_pilot.py`, `prepare_gate.py`, `schemas/`, `tests/`). Un pacchetto trasversale alle fasi avrebbe senso solo se 03.6 (feature/verbalizzatore), 03.8 (metriche/bootstrap) e 03.9 (baseline) dovessero condividere codice con 03.10; è una scelta di **organizzazione interna** di `studio2/` (§8.1 non fissa la struttura sotto `studio2/`), non un cambiamento di perimetro, e non richiede §1 |
| §8.2 | copie «identificate per impronta» sono esattamente le righe di PROVENIENZA §5: nulla di nuovo |
| Test | come (a) |
| §8.5 | intatta nella variante `studio2/`; compromessa nella variante `phase_b/q8/` per la ragione sopra |
| Giudizio | la variante `studio2/harness/` può essere decisa più avanti, quando 03.6 e 03.8 mostreranno se c'è codice comune; non blocca nulla oggi |

### Perché `code/` non può essere trattato come «non congelato» solo perché §1 lo mette sotto «Codice e verifica»

La lettura va motivata sul testo, come richiesto. §1 dice di `code/` soltanto che
`test_explanation.py` «è il guardiano della documentazione». §2, che prevale per il suo oggetto,
dice «hash… non si toccano mai», e i quattro file `code/` sono quattro delle 56 impronte di un manifest
e di un test che le pinna. §8 aggiunge che «dati, risultati, codice e documentazione del primo
restano recuperabili e riconoscibili nella loro versione originale». La conclusione coerente è che
il nucleo di `code/` è artefatto congelato **per impronta** anche se la riga «Artefatti congelati»
non lo nomina; il pattern `tep_*_v2/` non lo copre (è un pattern di directory) e non va forzato a
farlo. L'unica correzione utile è testuale: dirlo in §1.

## 5. Raccomandazione: opzione (a′) — (a) più tre precisazioni testuali

**Nessun nuovo perimetro, nessuna separazione harness/artefatto dentro `phase_b/`, nessuna modifica
al codice congelato.** Il punto 2 si chiude dichiarando che §8.2 lo copre e correggendo tre testi.
La motivazione è che le quattro attività che il punto 2 cita sono già state fatte, o si fanno, in
`studio2/` senza toccare `phase_b/`; che l'unica lettura di «harness riutilizzabile» compatibile con
§2 e con il manifest è «pattern trasferibile», e questa lettura non ha bisogno di un elenco in §1;
e che ciò che manca davvero (stato di `code/`, regola copia/import, riga PROVENIENZA mancante) è
risolvibile con tre frasi.

### 5.1 Testo proposto per `docs/MAINTENANCE.md` §1 (da applicare in un'altra finestra)

Riga «Artefatti congelati», colonna *Dove*, da:

> `phase_b/`, `icl/`, `ablation/`, `tep_*_v2/`, `reproducibility/`, tag git

a:

> `phase_b/`, `icl/`, `ablation/`, `tep_*_v2/`, `reproducibility/`, tag git, e i file di `code/` elencati in `phase_b/PHASE_B_PROTOCOL_HASHES.json`

Riga «Codice e verifica», colonna *Regola*, da:

> `test_explanation.py` è il guardiano della documentazione: vedi §5.

a:

> `test_explanation.py` è il guardiano della documentazione: vedi §5. Il codice del primo studio in `code/` e `phase_b/` non si modifica per lo studio 2: si riusa come dice §8.2.

### 5.2 Testo proposto per `docs/MAINTENANCE.md` §8.2, nuovo capoverso dopo «Gli artefatti non si duplicano se basta referenziarli.»

> **Codice del primo studio.** `phase_b/` e `code/` sono harness solo come *pattern*: contratti,
> invarianti e controlli fail-closed si riprendono, i file no. Un modulo che non incorpora costanti
> del protocollo (per esempio `code/tep_features.py`, `signature_vector` in
> `code/evaluate_verbalizer_v2.py`) può essere **importato in sola lettura dal suo percorso
> congelato**, registrando in `PROVENIENZA.md` commit e impronta del modulo importato. Un modulo che
> incorpora costanti del primo studio (quattro agenti, cinque label, `label_space[:-1]`, sei peer,
> dodici cluster) **non si importa e non si copia alla lettera**: si riscrive dentro `studio2/` con le
> costanti dello studio 2, e la riga di `PROVENIENZA.md` dichiara origine, commit, impronta
> dell'originale e modifiche. I test si riscrivono in `studio2/` e verificano gli invarianti nuovi;
> `phase_b/tests/` non si esegue contro `studio2/`. Nessun modulo di `studio2/` importa da `phase_b/`.

### 5.3 Testo proposto per la chiusura del punto 2 in `docs/fot_walkthrough_conversazione_studio2.md` §0.1

Il punto va **tolto dalla tabella** (la nota in calce a §0.1 lo prescrive) e la chiusura registrata
nel capoverso introduttivo di §0.1, dopo la frase sul riuso dei dati:

> Il punto sul perimetro del codice della Q8 (registrato il 2026-09-12) è stato chiuso dalla
> sotto-fase 03.4 senza aprire un nuovo perimetro: la terza metrica di §8.5, il cap dello schema,
> l'estensione a 8 agenti e il derangement a 7 peer sono codice nuovo in `studio2/` secondo
> [`MAINTENANCE.md`](MAINTENANCE.md) §8.2, che ora dice esplicitamente come si riusa il codice del
> primo studio; `phase_b/` e il nucleo di `code/` restano congelati per impronta
> ([`MAINTENANCE.md`](MAINTENANCE.md) §1). La proposta e l'inventario sono in
> `studio2/fase03/perimetro_q8/`.

La coppia `.md`/`.html` del walkthrough va aggiornata insieme (§3). Dato che questo commit non tocca
il walkthrough, la coppia non è interessata qui.

### 5.4 Riga da aggiungere a `studio2/PROVENIENZA.md` (sanatoria del precedente di Fase 02)

| Origine | Commit | SHA-256 | Destinazione | Modifiche | Ruolo | Marca |
| --- | --- | --- | --- | --- | --- | --- |
| `code/tep_features.py` | `3fd960a192bafacbaabce9471e3c3614d6b2d2db` | `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c` | `studio2/fase02/analysis/tep_features.py` (commit `dec2010`, stessa impronta) | nessuna: copia byte-identica, inclusa in `PRECALIBRATION_FREEZE.json` | feature per finestra dello score Normal | pre-specificato |

Se l'autore sceglie la regola «importa, non copiare» di §5.2, la copia di Fase 02 resta com'è
(è dentro un freeze già verificato, §8.4) e la riga la documenta come eccezione storica.

### 5.5 Che cosa cambia per le sotto-fasi dipendenti

| Sotto-fase | Con (a′) |
| --- | --- |
| **03.6** evidence 697-D e testo neutrale | usa `code/tep_features.py`, `code/tep_verbalize_v2.py`, `code/verbalizer_config_v2.json` e `signature_vector` di `code/evaluate_verbalizer_v2.py` **invariati**, per import dal percorso congelato (o per copia con riga PROVENIENZA, se l'autore preferisce), registrando le quattro impronte `cbade7a2…`, `3a9129b6…`, `552a0b8a…`, `972e06fa…`; scrive in `studio2/fase03/<sottofase>/` lo script di estrazione sui 40 run, il manifest di output e i test. Lo scanner anti-leakage va riscritto per gli 8 fault D1 (pattern di `phase_b/prompts/leakage.py`). **Non decide** se le soglie V2 restano quelle di `verbalizer_config_v2.json` o se dipendono da 03.5: lo dichiara |
| **03.7** pseudolabel e derangement | riusa il pattern `derive_opaque_pseudolabel` (in `studio2/fase03/protocol.py` esiste solo la regex di forma `S2-CLS-`) e scrive il generatore dei derangement a 7 peer in `studio2/` (oggi esiste solo nella fixture sintetica); il test dimostra assenza di punti fissi e opacità; seed e namespace sono la decisione da congelare lì. Nessun file di `phase_b/` toccato; `condition_e_derangements.json` resta il riferimento di forma |
| **03.9** baseline numerica | riscrive il pattern di `c02b/run_baseline.py` (prototipi medi 697-D, L1, astensione su pareggio) in `studio2/` per 9 classi e 8 agenti, con riga PROVENIENZA su `run_baseline.py` (`5a0d4572…`) e sul protocollo C02B (`229f901a…`) |
| **03.10** harness API | `studio2/fase03/protocol.py`, `run_pilot.py`, `prepare_gate.py` sono già l'harness; restano da collegare gli input reali di 03.6/03.7 e da aggiungere logging §8.7 (pattern `records.py`, `token_logging.py`) e la **terza metrica** di §8.5 (accuratezza sui soli non astenuti), come codice nuovo accanto ai numeri 1 e 2 (pattern `metrics.py`); i test di `phase_b/tests/` si riscrivono. Se la terza metrica appartiene al piano statistico di 03.8 anziché all'harness, lo decide 03.8: qui si registra solo che è codice nuovo in `studio2/` |
| **03.8** (non dipendente, ma toccata) | il bootstrap a 9 classi + astensione è codice nuovo (pattern `bootstrap.py`, che pinna 12 cluster in 4 strati) |

## 6. Ciò che questa proposta non decide e che spetta all'autore

1. **Confermare (a′)** o scegliere (a), (b), (c); la colonna «Decisione da chiudere in» del punto 2
   indica §1 «separato tra harness riutilizzabile e artefatto», e la proposta si discosta da
   quell'indicazione per le ragioni di §4(b).
2. **Copia o import** per il codice congelato di `code/` (§5.2 propone: import in sola lettura per i
   moduli senza costanti di protocollo). La scelta vincola 03.6 e 03.9.
3. **Se sanare** il precedente di Fase 02 con la riga di §5.4.
4. **Nulla è deciso** su schema degli insight (03.12), seed/namespace delle pseudolabel (03.7), soglie
   del verbalizzatore (03.5/03.6), forma della terza metrica e del bootstrap (03.8): dove questa
   proposta li nomina, lo fa per dichiarare la dipendenza, non per fissarli. L'idioma posizionale
   ereditato da `studio2/fase03/protocol.py` (§3 punto 4) è un'osservazione per 03.12, non una
   richiesta di modifica.
5. `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md` è **non tracciato** a HEAD: questa finestra l'ha
   letto ma non lo committa (non è fra i due file autorizzati). Va deciso se e quando committarlo.
