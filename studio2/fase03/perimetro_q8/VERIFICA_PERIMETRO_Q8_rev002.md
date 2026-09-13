NON OK — la Revisione 2 risolve i rilievi sul riuso di `signature_vector`, sulle righe `openai_adapter.py`/`guard.py` e sul glob, ma non applica uniformemente il proprio criterio file-level alle tre righe H rimaste: `code/tep_features.py` incorpora il default di finestra da 5 h e `code/test_features.py` importa quel modulo.

# Riverifica indipendente della sotto-fase 03.4 — Revisione 2

| Campo | Valore |
| --- | --- |
| Data | 2026-09-13 |
| Modello verificatore | OpenAI `gpt-5.6-sol`, diverso da OpenAI Codex GPT-5 che ha prodotto la Revisione 2 |
| Ragionamento | medio |
| Finestra | A3, riverifica indipendente nel worktree `/Users/luker/fot-tep-q8` |
| Oggetto | branch `codex/studio2-perimetro-q8`, HEAD `b4d35c30d472e3947e212fabc00d74495860a912`; verbale precedente `ac81b38` |
| Profilo | sola lettura delle fonti, nessuna chiamata a modelli e nessuna simulazione; il solo file creato è questo verbale |

I dettagli seguono prima del giudizio conclusivo, come richiesto da
`docs/prompts/Verifica_LLM.md`. Proposta, report e verbale precedente sono stati letti con
`git show <commit>:<percorso>` e non sono stati assunti come fonti primarie.

## Esiti della riverifica mirata

| Blocco | Esito | Riscontro sulla fonte primaria |
| --- | :---: | --- |
| Punto 8 — regola di riuso e import reale | ✅ | Il nuovo §5.2 elimina la regola module-level contestata e impone valutazione della funzione, dipendenze effettive, effetti del caricamento, provenienza e controllo SHA-256 prima dell'import. `code/evaluate_verbalizer_v2.py` righe 19–20 importa al caricamento `XMEAS` da `tep_features` e `load_config`/`verbalize_feature_table` da `tep_verbalize_v2`; la proposta ora classifica correttamente il file HC e precisa che la compatibilità di `signature_vector` non rende automaticamente importabile il modulo. Il corpo della funzione, righe 33–70, usa soltanto `XMEAS`, NumPy, `n_windows` e i campi del JSON strutturato: non legge baseline, soglie, finestre o configurazione del verbalizzatore. Il rilievo originario è risolto. |
| Applicabilità del nuovo §5.2 | ✅ | MAINTENANCE §1 vieta la modifica degli artefatti congelati, §2 vieta di toccare hash/freeze e §8.2 consente adattamenti nuovi sotto `studio2/`, identificando gli originali con commit e impronta. Il testo proposto non modifica gli originali, vieta import da `phase_b/`, colloca adattamenti e test in `studio2/` e rende espliciti baseline, finestre, soglie e default. Il controllo dell'impronta deve necessariamente avvenire prima dell'istruzione che carica il modulo, ma il testo lo dice già. Non emerge una contraddizione con il contratto vigente; §5.2 lo specifica senza allargarne il perimetro. |
| Punto 5 — criterio uniforme sulle righe H | ❌ | La Revisione 2 dichiara un criterio file-level: un file H non incorpora numeri del protocollo e non importa transitivamente un file HC. Sono state rilette una per una tutte le tre righe rimaste H. `phase_b/evaluation/token_logging.py` è coerentemente H: dipende solo da dataclass, `Protocol`, stringhe e contatori passati. `code/tep_features.py` non lo è secondo il criterio scritto: `iter_time_windows` e `analyze_case_windows` incorporano entrambe `window_h=5.0` (righe 253–259 e 277–284), esattamente una finestra/default ereditato che §5.2 richiede di rendere esplicito. La riga d'inventario dichiara invece «solo schema colonne TEP e 41 XMEAS». `code/test_features.py` importa direttamente `tep_features` (righe 15–20), che risulta HC applicando il criterio; ciò viola anche la clausola H «non importa transitivamente un file HC». Pertanto 1/3 righe H è coerente e 2/3 no. |
| Righe discutibili `openai_adapter.py` e `guard.py` | ✅ | `phase_b/execution/openai_adapter.py` è ora HC per ragioni presenti nel file: importa parser/retry HC (righe 13–14), fissa lo schema sotto `phase_b/` (17–20), il nome `phase_b_diagnostic_output` (116) e i default 512 token/2 retry (100, 158–159). `phase_b/guard.py` è ora HC: `project_guard` fissa `phase_b/heldout`, `tep_heldout/`, manifest e verificatore del primo studio (62–68). «Superato» e «riusabile come pattern» non determinano più la classe. Entrambi i rilievi sono risolti. |
| Punto 3i — glob e directory separate | ✅ | A HEAD, `ls -d tep_*_v2/` restituisce esattamente `tep_test_v2/` e `tep_validation_v2/`; `ls -d */tep_*_v2/` restituisce separatamente `code/tep_analysis_v2/`. `tep_exp3_v2_heldout/` è assente dal tree di HEAD e il tag `exp3-v2-heldout-data-frozen-001` contiene 32 file sotto quel percorso. `code/tep_analysis_v2/` contiene 12 file tracciati; rispetto a `phase-a-verbalizer-v2-complete` differisce soltanto `threshold_calibration_report.md` (una riga aggiunta). §3.1 descrive ora correttamente questi fatti e §5.1 presenta l'estensione come proposta, non come decisione già attuata. |
| Perimetro del diff `ac81b38..b4d35c3` | ✅ | `git diff --name-status` mostra soltanto `PROPOSTA_PERIMETRO_Q8.md` e `REPORT_PERIMETRO_Q8.md`; 137 inserimenti e 57 eliminazioni. Le variazioni della proposta ricadono nei tre blocchi dichiarati in «Revisione 2» — criterio/classificazioni, regola function-level e glob — e nelle conseguenti correzioni di §3, §4, §5.1, §5.5 e §6. Il report registra le stesse correzioni e il nuovo passaggio A3. Nessun file sorgente, contratto, artefatto o tag è cambiato. |
| Impronte §0/§2 dei file non cambiati | ⚠️ | A `b4d35c3`, tutte le **44/44** impronte dell'inventario §2 coincidono. In §0 coincidono **8/8** impronte dei file tracciati. Il nono elemento, `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md`, è intenzionalmente non tracciato, non esiste nel worktree Q8 e non è recuperabile con `git show`: non è quindi riverificabile in A3. Nessuno dei percorsi sorgente verificabili è cambiato tra `b7f359f` e `b4d35c3`. Totale riverificabile: **52/52 impronte coincidenti**, nessun mismatch. |
| `docs/test_explanation.py` | ✅ | Rieseguito a `b4d35c3`: **Ran 35 tests — FAILED (failures=14, skipped=1)**. Coincide con il risultato dichiarato e con il baseline preesistente. Il test non copre la proposta di studio 2 e il risultato invariato non sana il rilievo di classificazione. |

## Analisi delle tre righe H rimaste

| File | Classe proposta | Esito | Motivo |
| --- | :---: | :---: | --- |
| `phase_b/evaluation/token_logging.py` | H | ✅ | Nessun import HC, nessun percorso o cardinalità del primo studio; tokenizer e conteggi sono parametri o dati del record. Le occorrenze «B/E» sono descrittive e non cambiano il comportamento. |
| `code/tep_features.py` | H | ❌ | Le API `iter_time_windows` e `analyze_case_windows` hanno entrambe il default operativo `window_h=5.0`. È un valore della pipeline di Fase A e la stessa Revisione 2 include «finestre» e «ogni default ereditato» tra gli elementi che devono essere passati o dichiarati. Il file non contiene soltanto lo schema TEP. |
| `code/test_features.py` | H | ❌ | Numeri e seed delle fixture sono ammessi dal criterio, ma il file importa `tep_features` direttamente. Una volta applicato uniformemente il criterio al modulo importato, cade la condizione esplicita per H che vieta dipendenze transitive da HC. |

Il difetto non rimette in discussione l'opzione di perimetro (a′) né il testo function-level di
§5.2. Smentisce però l'affermazione della Revisione 2 e del report secondo cui tutte le righe H
sono state riclassificate coerentemente. Prima dell'OK occorre rendere coerenti criterio,
inventario e report per `tep_features.py` e `test_features.py`; questa finestra non modifica la
proposta.

## Fonti primarie e controlli eseguiti

- `docs/MAINTENANCE.md` a `b4d35c3`: §1, §2, §8, §8.1 e §8.2.
- Codice a `b4d35c3`, letto integralmente per le tre righe H e per le righe discusse:
  `phase_b/evaluation/token_logging.py`, `code/tep_features.py`, `code/test_features.py`,
  `phase_b/execution/openai_adapter.py`, `phase_b/guard.py`, `phase_b/conditions/parser.py`,
  `phase_b/conditions/retry.py`, `code/evaluate_verbalizer_v2.py` e
  `code/tep_verbalize_v2.py`.
- Tree e storia Git: `git diff ac81b38..b4d35c3`, `git show`, `git ls-tree`, confronto con
  `phase-a-verbalizer-v2-complete` e tag `exp3-v2-heldout-data-frozen-001`.
- Proposta e report a `b4d35c3`; verbale precedente a `ac81b38`; protocolli
  `Prompt_LLM.md` e `Verifica_LLM.md` letti integralmente; prompt A3 letto integralmente.
- Costo approssimativo: circa 25 mila token fra protocolli, proposta/diff, contratto e codice,
  oltre agli output meccanici di hash e test.

## Cosa non è stato possibile verificare

Soltanto l'impronta di `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md`: il file era non tracciato
nella finestra originaria, non appartiene a nessuno dei commit oggetto e non è presente nel
worktree Q8. Il limite è registrato come ⚠️ e non incide sul difetto bloccante, verificato invece
direttamente sul codice tracciato.

## Conclusione

**NON OK.** La Revisione 2 risolve i tre rilievi originari per §5.2, le righe espressamente
discutibili e il glob, ma fallisce il controllo richiesto su **tutte** le righe H rimaste:
`code/tep_features.py` e, per dipendenza, `code/test_features.py` non soddisfano il criterio
file-level scritto nella proposta. Il lavoro non è ancora pronto per l'attuazione B.

Percorso del verbale:
`studio2/fase03/perimetro_q8/VERIFICA_PERIMETRO_Q8_rev002.md`.
