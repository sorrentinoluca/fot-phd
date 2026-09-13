NON OK — la proposta richiede correzioni prima dell'attuazione: il criterio di riuso di §5.2 non regge all'import reale di `signature_vector`, due classi H del campione violano il criterio dichiarato e l'elenco delle directory attribuito al glob `tep_*_v2/` non è esatto.

# Verifica indipendente della sotto-fase 03.4 — perimetro del codice Q8

| Campo | Valore |
| --- | --- |
| Data | 2026-09-13 |
| Modello verificatore | OpenAI Codex (GPT-5), diverso da Claude Fable 5.1 che ha prodotto la proposta |
| Finestra | finestra indipendente, copia di lavoro `codex/studio2-soglie-normal`; oggetto letto esclusivamente con `git show 53a3e92:<percorso>` |
| Oggetto | commit `53a3e9299ff7548fde30c54014a340d7113bf882`, parent `b7f359fc593b74cf756f3b407ddabe5027f91b0f` |
| Profilo | verifica indipendente, sola lettura delle fonti; nessuna chiamata a modelli e nessuna simulazione |

Questa verifica segue `docs/prompts/Verifica_LLM.md`, `Prompt_LLM.md` e le regole di
`docs/MAINTENANCE.md` §1, §2 e §8. Non assume corretti né la proposta né il report. Il solo file
scritto è questo verbale; non sono stati modificati file esistenti, non sono stati creati commit o
tag e non sono stati eseguiti checkout o stash.

## Esiti dei dieci punti

| # | Esito | Verifica sulla fonte primaria |
| :---: | :---: | --- |
| 1 | ✅ | `git diff --stat b7f359f 53a3e92` e `git diff --name-status` mostrano soltanto l'aggiunta di `PROPOSTA_PERIMETRO_Q8.md` e `REPORT_PERIMETRO_Q8.md`: 466 righe aggiunte, nessun altro percorso. Il parent di `53a3e92` è esattamente `b7f359f`. Nessun tag punta a questo cambiamento e il commit non contiene modifiche a `phase_b/`, `code/`, `docs/`, `studio2/PROVENIENZA.md` o artefatti congelati. |
| 2 | ✅ | Ricalcolate sul contenuto a `b7f359f`: **53/53 impronte SHA-256 coincidenti** — 9 righe di §0 e 44 righe dell'inventario, incluse le 2 di §2.3. Per le 44 righe dell'inventario, **44/44 commit di ultima modifica coincidenti** con `git log -1 b7f359f --format=%H -- <file>`; le abbreviazioni con ellissi sono prefissi corretti. `APERTURA_SOTTOFASI_FASE03.md` è l'unica riga non tracciata: non ha un commit di ultima modifica, ma la copia di lavoro conserva l'impronta dichiarata. |
| 3 | ❌ | I fatti 3a–3h sono confermati; il 3i è smentito nella parte relativa alle directory. Il dettaglio è nella tabella successiva. |
| 4 | ✅ | Il punto 2 del walkthrough §0.1 è stato letto e la sua premessa «richiedono tutti di scrivere dentro `phase_b/`» è citata testualmente e poi contestata con il codice. La lettura di MAINTENANCE §2 (hash e artefatti congelati non si toccano) e §8.2 (adattamenti nuovi in `studio2/`, originali identificati da commit e impronta) è corretta. Le fonti seguono §0 del walkthrough; il piano BIGDATA2026 non è usato. La prima esposizione è stata effettivamente usata nelle sezioni feature → flag → JSON → testo neutrale e firma 697-D, e il percorso è confermato dal codice. L'equivalenza «referenziare codice = importarlo» non è però imposta dal testo vigente di §8.2: la proposta la presenta correttamente come regola ancora da decidere, ma la formulazione concreta proposta non supera il punto 8. |
| 5 | ❌ | Il criterio è scritto prima dell'inventario, ma non è applicato coerentemente a tutte le righe. Nel campione richiesto, le due righe dichiarate H (`conditions/parser.py` e `conditions/retry.py`) incorporano assunzioni del protocollo e devono essere HC secondo lo stesso criterio. Le due HC e le due A campionate sono coerenti. Dettaglio sotto. |
| 6 | ✅ | §5.5 dichiara dipendenze e rinvia le scelte: non fissa le soglie del verbalizzatore, lo schema, seed/namespace delle pseudolabel, forma della terza metrica o bootstrap. §6 le elenca esplicitamente come decisioni dell'autore o di 03.5–03.12. L'organizzazione eventuale `studio2/harness/` è lasciata futura. |
| 7 | ❌ | Le conseguenze generali delle opzioni rispetto a MAINTENANCE §1, §2, §8.1, §8.4 e §8.5 sono fondate; la frase «Non elenca i file: gli elenchi marciscono» esiste in MAINTENANCE §1 e §5.1 rinvia dinamicamente al manifest invece di enumerare file. Tuttavia il testo di §5.2 non è applicabile senza contraddire la classificazione a livello di modulo e le dipendenze effettive descritte al punto 8. Inoltre la motivazione di §3.1 attribuisce al glob directory che esso non seleziona esattamente. §5.3 e §5.4 restano applicabili, ma non sanano questi difetti. |
| 8 | ❌ | Ambiguità reale e bloccante. `evaluate_verbalizer_v2.py`, classificato H, esegue al caricamento `from tep_features import XMEAS` e `from tep_verbalize_v2 import load_config, verbalize_feature_table`; dunque importare `signature_vector` carica anche il modulo HC `tep_verbalize_v2.py`. La funzione `signature_vector` in sé usa `XMEAS`, `structured["n_windows"]`, i campi strutturati e NumPy: non legge baseline, finestre, soglie o `verbalizer_config_v2.json` e contiene esattamente 17 componenti per ciascuna delle 41 XMEAS. La regola «modulo senza costanti di protocollo → importabile» è quindi troppo grossolana: confonde dipendenza della funzione, dipendenze transitive del modulo e configurazione usata dalle altre funzioni dello stesso modulo. Formulazione corretta sotto. |
| 9 | ✅ | `REPORT_PERIMETRO_Q8.md` ha le sette sezioni richieste da `Fase_LLM.md` «Chiusura della finestra», dichiara modello, ragionamento e profilo decisionale, elenca i due soli file del commit e mantiene l'esito come proposta. `python3 docs/test_explanation.py` è stato rieseguito: **Ran 35 tests — FAILED (failures=14, skipped=1)**, identico al dichiarato. I file tracciati della copia di lavoro coincidono con `b7f359f`; i file non tracciati non sono letti dal test. |
| 10 | ✅ | `git ls-files --error-unmatch studio2/fase03/APERTURA_SOTTOFASI_FASE03.md` fallisce a `b7f359f` e fallisce ancora nella copia di lavoro. `git status --short` lo mostra tuttora `??`; non è stato aggiunto né modificato da questa verifica. |

## Dettaglio del punto 3

| Sottopunto | Esito | Riscontro |
| :---: | :---: | --- |
| 3a | ✅ | `PHASE_B_PROTOCOL_HASHES.json` contiene **56** artefatti: **52** sotto `phase_b/` e **4** sotto `code/`; ricalcolo sul tree `b7f359f`: **56/56 coincidenti**, 0 mancanti e 0 mismatch. |
| 3b | ✅ | `phase_b/tests/test_phase_a_hashes.py::EXPECTED` contiene esattamente gli stessi quattro percorsi e le stesse quattro impronte del manifest: `verbalizer_config_v2.json`, `tep_verbalize_v2.py`, `evaluate_verbalizer_v2.py`, `tep_features.py`. |
| 3c | ✅ | Per ciascuno dei quattro file, `git show <tag>:<file>` ha la stessa SHA-256 del manifest sotto tutti e cinque i tag indicati: **20/20 confronti coincidenti**. |
| 3d | ✅ | Trovate **11** occorrenze letterali di `label_space[:-1]`: `evaluation/bootstrap.py` (1), `execution/generate_final_insights.py` (1), `insights/library.py` (2), `local_knowledge/build_local_examples.py` (2), `tests/test_config_and_examples.py` (1), `tests/test_final_insights.py` (1), `tests/test_insights_conditions.py` (3). Coincidono con D10, riga 1123 del piano. Il distinto `labels[:-1]` del validatore è in `config/protocol.py`. |
| 3e | ✅ | Nessun file Python sotto `studio2/` contiene `phase_b`: 0 risultati. Le occorrenze sotto `studio2/` sono in documentazione o configurazione, non import Python. |
| 3f | ✅ | `studio2/fase02/analysis/tep_features.py` e `code/tep_features.py` hanno entrambi SHA-256 `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c`. Né il percorso né l'impronta compaiono in `studio2/PROVENIENZA.md`; entrambi compaiono in `studio2/fase02/validation/PRECALIBRATION_FREEZE.json`. |
| 3g | ✅ | `phase_b/config/protocol.py` impone `agent_1`…`agent_4`, cinque label uniche e `Normal` ultima; `PHASE_B_PROTOCOL_FREEZE.md` dichiara esattamente quattro agenti. `signature_vector` estende una lista di 17 valori per ciascun elemento di `XMEAS`, definito con 41 elementi: **41 × 17 = 697**. |
| 3h | ✅ | `studio2/fase03/protocol.py` contiene `AGENT_IDS` 1…8, valida 8 pseudolabel più `Normal`, rappresenta l'astensione con `abstain`/`predicted_label`, valida per ogni agente un derangement su sette peer senza punti fissi e controlla che E-LF cambi solo `pseudolabel`. Non contiene una funzione di derivazione delle pseudolabel né un generatore scientifico dei derangement: c'è solo la regex `S2-CLS-[A-Z0-9]{5}` e la rotazione nella fixture sintetica `synthetic_fixture.py` riga 102. |
| 3i | ❌ | La barra finale esclude correttamente i moduli `code/tep_verbalize_v2.py` e `code/tep_characterize_v2.py`. Ma, interpretato come glob root-relative scritto in MAINTENANCE, `tep_*_v2/` seleziona soltanto `tep_test_v2/` e `tep_validation_v2/`. Non seleziona `tep_exp3_v2_heldout/` perché non termina in `_v2`, né `code/tep_analysis_v2/` senza il prefisso `code/`. La formulazione corretta deve distinguere il glob letterale dalle directory che si intende proteggere. |

## Impronte e commit

### Righe di §0

| File | SHA-256 | Ultima modifica a `b7f359f` |
| --- | :---: | --- |
| `docs/MAINTENANCE.md` | ✅ | `ca76f023ecc0e236f488ae339a6b8184c36031cc` |
| `docs/fot_walkthrough_conversazione_studio2.md` | ✅ | `8c38bef7db303be9126c3942430fc59219742ad5` |
| `docs/prompts/Fase_LLM.md` | ✅ | `ef2281b3bf1723a4f2ac5f18a2d6572a3fd1198f` |
| `docs/prompts/Prompt_LLM.md` | ✅ | `93f33fc932a0bf547483cb0d13c59373e274ae1a` |
| `studio2/PROVENIENZA.md` | ✅ | `8c38bef7db303be9126c3942430fc59219742ad5` |
| `studio2/fase03/IMPLEMENTATION_STATUS.md` | ✅ | `3b9ec1eb9a25d37792138384454d5e190483b331` |
| `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md` | ✅ | non tracciato; nessun commit |
| `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` | ✅ | `2f2b8e68ba7e4f0c5d01915d44734e84a46ef645` |
| `docs/fot_walkthrough_conversazione.md` | ✅ | `25889a023ab026e7116e42bca01b0519525ce480` |

### Conteggi complessivi

- §0: **9/9 SHA-256 coincidenti**.
- Inventario §2.1–§2.2: **42/42 SHA-256** e **42/42 commit** coincidenti.
- §2.3: **2/2 SHA-256** e **2/2 commit** coincidenti.
- Totale: **53/53 impronte** e, sulle righe che dichiarano un commit, **44/44 commit**; nessun mismatch.

## Campione del criterio di classificazione

| Riga della proposta | Classe dichiarata | Esito | Giudizio dalla lettura del file |
| --- | :---: | :---: | --- |
| `phase_b/conditions/parser.py` | H | ❌ | `parse_insight_generation_output` impone esattamente **due** oggetti e il modulo importa `Insight` e `validate_label_neutral_fields` da `phase_b.insights`, classificato HC. Con il criterio file-level di §1 è HC, non H. La sola funzione `parse_diagnostic_output` è invece parametrica. |
| `phase_b/conditions/retry.py` | H | ❌ | Accetta `max_retries` come argomento ma rifiuta ogni valore diverso da **2**; inoltre il suffisso di correzione fissa lo schema Phase B. È harness con costanti di protocollo, quindi HC. |
| `phase_b/evaluation/metrics.py` | HC | ✅ | Incorpora condizioni A/B/E, ripetizioni 1–3, `positive_at_least_3_of_4_agents`, 12 cluster e assunzioni seen/unseen del primo studio. |
| `phase_b/evaluation/bootstrap.py` | HC | ✅ | Impone quattro strati, tre cluster per strato, 12 cluster e tre righe agente per cluster, oltre a `label_space[:-1]`. |
| `phase_b/config/protocol_config.json` | A | ✅ | È la configurazione concreta del protocollo Exp1, quindi artefatto per definizione. |
| `phase_b/conditions/diagnostic_output.schema.json` | A | ✅ | È uno schema JSON; §1 include esplicitamente gli schemi nella classe artefatto. |

Un'altra riga discutibile è `phase_b/execution/openai_adapter.py`, classificata A perché «superata»:
essere superata non è un criterio di artefatto in §1. Va riclassificata H/HC in base alle costanti e
alle dipendenze effettive, oppure il criterio deve essere esteso esplicitamente. Anche `guard.py`
porta percorsi del primo studio e la notazione «H (pattern)» non coincide con la definizione H
file-level: come pattern può essere riusabile, ma il file concreto è almeno HC secondo il criterio.

## Punto 8 — formulazione corretta

La raccomandazione può conservare l'opzione (a′), ma §5.2 deve essere riscritta separando la
riusabilità di una funzione dalla classificazione del modulo che la contiene:

> Dal codice congelato si possono importare soltanto funzioni compatibili dopo aver verificato le
> loro dipendenze effettive e gli effetti del caricamento del modulo. Commit e SHA-256 del modulo di
> origine si registrano in `PROVENIENZA.md` e lo script verifica l'impronta prima dell'import,
> fermandosi se differisce. Configurazione e orchestrazione dello studio 2 restano esplicite sotto
> `studio2/`: baseline, finestre, soglie e default ereditati sono passati o dichiarati, non approvati
> implicitamente dal riuso della funzione. Se le assunzioni ereditate non sono eliminabili mediante
> parametri, la funzione si adatta riscrivendola in `studio2/` con la relativa riga di provenienza.
> Resta vietato importare da `phase_b/`; i test si riscrivono in `studio2/`.

Per `signature_vector` questo significa parlare della **funzione**, non dichiarare genericamente
importabile `evaluate_verbalizer_v2.py`. La funzione non dipende da soglie, baseline o finestre di
Fase A, ma il modulo che la ospita importa comunque il verbalizzatore HC al caricamento.

## Correzioni necessarie prima dell'OK

1. Riscrivere PROPOSTA §5.2 con una regola function-level e con verifica delle dipendenze transitive
   e dell'impronta prima dell'import; riformulare l'esempio di `signature_vector`.
2. Correggere nell'inventario almeno `conditions/parser.py` e `conditions/retry.py` da H a HC, e
   riesaminare `execution/openai_adapter.py` e `guard.py` applicando un solo criterio coerente.
3. Correggere PROPOSTA §3.1 sul glob `tep_*_v2/`: indicare ciò che il glob letterale seleziona e
   trattare separatamente `tep_exp3_v2_heldout/` e `code/tep_analysis_v2/` se si intendono coperti.

Queste correzioni non richiedono di cambiare la raccomandazione di perimetro (a′), ma impediscono
di applicare alla lettera il testo proposto. Dopo la correzione serve una nuova verifica del verbale
aggiornato prima dell'attuazione.

## Cosa non è stato possibile verificare

Nulla fra i controlli richiesti è rimasto non verificato. La storia passata dei riferimenti Git non è
contenuta in un commit, ma il perimetro del commit è determinato integralmente dal diff del tree e
nessun tag corrente punta a `53a3e92`; questo limite non cambia il giudizio sul contenuto del commit.

## Fonti lette

- Integrali: proposta e report da `53a3e92`; `Verifica_LLM.md`, `Prompt_LLM.md`, `Fase_LLM.md`;
  MAINTENANCE §1, §2, §8; i file di codice usati per manifest, pinning, import e campione.
- Mirate: walkthrough studio 2 §0–§0.1; piano D10; prima esposizione nelle sezioni feature → flag →
  JSON → testo neutrale, evaluator e payload; `PROVENIENZA.md` e freeze di Fase 02.
- Costo approssimativo: circa 25–30 mila token di testo sorgente e codice, esclusi gli output
  meccanici di hash e test.

## Conclusione

**NON OK.** Percorso del verbale:
`studio2/fase03/perimetro_q8/VERIFICA_PERIMETRO_Q8.md`. Il blocco principale è il punto 8; si
aggiungono l'incoerenza di classificazione del punto 5 e l'errore sul glob del punto 3i. Tutti gli
altri controlli richiesti risultano verificati sulla fonte primaria.
