OK — la Revisione 3 risolve integralmente il rilievo del verbale rev002 nel perimetro ristretto A3b.

# Riverifica indipendente della sotto-fase 03.4 — Revisione 3

| Campo | Valore |
| --- | --- |
| Data | 2026-09-13 |
| Modello verificatore | OpenAI `gpt-5.6-terra`, diverso da OpenAI Codex GPT-5 che ha prodotto la Revisione 3 |
| Ragionamento | basso |
| Finestra | A3b, riverifica indipendente nel worktree `/Users/luker/fot-tep-q8` |
| Oggetto | branch `codex/studio2-perimetro-q8`, commit del verbale rev002 `4339410de044c9024bbffcb2ae9566c581d155b2` e Revisione 3 `c2471f4884d37c150ba60c830e2495f7a8771e1d` |
| Profilo | sola lettura delle fonti; nessuna chiamata a modelli, simulazione, commit, tag o checkout; il solo file creato è questo verbale |

I dettagli precedono la conclusione, come prescrive `docs/prompts/Verifica_LLM.md`. Sono stati usati `git show <commit>:<percorso>` per proposta, report, verbale rev002 e codice; non sono stati ripetuti i controlli già positivi nei verbali precedenti.

## Esiti della riverifica ristretta

| Punto | Esito | Riscontro sulla fonte primaria |
| --- | :---: | --- |
| Rilievo rev002: `tep_features.py` e `test_features.py` | ✅ | In `PROPOSTA_PERIMETRO_Q8.md` §2.2 a `c2471f4`, `code/tep_features.py` è HC per i default `window_h=5.0` di `iter_time_windows` e `analyze_case_windows`; `code/test_features.py` è HC perché importa quel modulo al caricamento. Il codice a `c2471f4` conferma i due default alle righe 258 e 283 e l'import in `test_features.py` righe 15–20. |
| Coerenza frase nuova §1, §5.2 e classi | ✅ | §1 qualifica esplicitamente come costante incorporata ogni default operativo del primo studio, anche sovrascrivibile. §5.2 richiede che finestre e ogni default ereditato siano passati o dichiarati dalla configurazione di `studio2/`. La classe HC assegnata a `tep_features.py`, e quella transitiva di `test_features.py`, applicano esattamente questa regola senza contraddizioni. |
| Tutte le righe H rimaste | ✅ | L'inventario a `c2471f4` lascia H soltanto a `phase_b/evaluation/token_logging.py`. Il file è stato riletto integralmente: non importa file HC, riceve tokenizer, testi e conteggi come argomenti e non incorpora finestre, burn-in, soglie, orizzonti o altri valori operativi del primo studio. Il default `method="provider_not_available"` descrive solo l'assenza della misura del provider e non è un parametro operativo ereditato. |
| Diff `4339410..c2471f4` e dichiarazione «Revisione 3» | ✅ | `git diff --name-status` mostra soltanto `PROPOSTA_PERIMETRO_Q8.md` e `REPORT_PERIMETRO_Q8.md` (68 inserimenti, 13 eliminazioni). Le modifiche corrispondono alla sezione «Revisione 3»: nuova frase del criterio, due riclassificazioni HC, precisazione per 03.6 e registrazione coerente nel report (modello, test e stato A3b). `git diff --check` non segnala errori di spaziatura. |
| Perimetro dei cambiamenti | ✅ | Il diff fra i due commit non contiene alcun percorso esterno a `studio2/fase03/perimetro_q8/`; non risultano modificati `phase_b/`, `code/`, `docs/`, `studio2/PROVENIENZA.md`, artefatti congelati, tag o altri file dello studio. |
| `python3 docs/test_explanation.py` | ✅ | Rieseguito in questa finestra: `Ran 35 tests` — `FAILED (failures=14, skipped=1)`. Coincide con il baseline e con il risultato dichiarato; i 14 fallimenti sono preesistenti e il test non copre questa proposta. |

## Fonti e controlli eseguiti

- `docs/prompts/Prompt_LLM.md` e `docs/prompts/Verifica_LLM.md`, letti integralmente; prompt A3b in `sottofase_3_4_verifica_e_attuazione.md` letto integralmente.
- A `c2471f4`: proposta (§1, §2.2, §5.2 e §5.5), report e codice `phase_b/evaluation/token_logging.py`, `code/tep_features.py`, `code/test_features.py`.
- A `4339410`: `VERIFICA_PERIMETRO_Q8_rev002.md` integrale.
- Git: `git show`, `git diff --name-status`, `git diff --stat`, diff testuale e `git diff --check` fra i due commit.

## Conclusione

**OK.** La Revisione 3 applica uniformemente il criterio aggiornato: i due file segnalati dal rev002 sono HC e l'unica riga H restante regge alla frase nuova. Il diff è limitato alle modifiche dichiarate, resta interamente nel perimetro autorizzato e il test esplicativo conserva il baseline preesistente.

Percorso del verbale: `studio2/fase03/perimetro_q8/VERIFICA_PERIMETRO_Q8_rev003.md`.
