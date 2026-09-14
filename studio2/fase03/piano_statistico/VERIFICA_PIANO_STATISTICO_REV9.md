OK

# Verifica indipendente della revisione 9 della sotto-fase 03.8 — piano statistico (ristretta al delta rev. 8 → 9)

Data: **2026-09-14** (14:57 CEST). Modello verificatore: **Claude (Cowork), identificativo
configurato `claude-fable-5-1`**, ragionamento esteso; stessa finestra della verifica rev. 8
(`session_01UbfhkXNGta2H9XdCvjfBk1`), distinta da quelle che hanno prodotto le revisioni 7, 8 e 9
(Codex). Su richiesta dell'autore la verifica è **ristretta** alle correzioni dichiarate dalla
revisione 9, alle impronte del manifest e ai controlli eseguibili; il merito scientifico e il
recepimento delle decisioni restano coperti dal settimo verbale (OK) e dal verbale rev. 8
(`VERIFICA_PIANO_STATISTICO_REV8.md`, §2–§5 tutti ✅). Poiché il diff completo
`75bd148..6015f8f` di piano, report e manifest è stato letto per intero, ogni modifica introdotta
dalla revisione 9 rientra nel perimetro di questa verifica.

Oggetto: commit **`6015f8fdb1b28e0adad50219466bf13cd988c137`** («corregge tracciabilità nella
revisione 9»), preceduto da **`f700326a096c7a79efd2feceb93939580f5057dc`** («registra verifica
indipendente rev8»), sul branch `codex/studio2-piano-statistico-fix`, worktree
`/Users/luker/fot-tep-piano-statistico-fix`.

Sola lettura: nessun file del candidato modificato; nessun commit, tag, push, merge, freeze o
modifica a `main`; nessun dato sperimentale aperto, nessuna chiamata a modelli, nessuna
rigenerazione della griglia. L'unico file nuovo è questo verbale.

---

## 0. Ambiente

| Controllo | Esito |
| --- | --- |
| Branch / HEAD | ✅ `codex/studio2-piano-statistico-fix`, HEAD `6015f8f`; `git log`: `6015f8f` → `f700326` → `75bd148` → `7f760b7` |
| Worktree | ✅ pulito (`git status --porcelain --untracked-files=all` vuoto, `GIT_OPTIONAL_LOCKS=0`) |
| `f700326` | ✅ aggiunge il solo `VERIFICA_PIANO_STATISTICO_REV8.md` (253 righe), SHA-256 `e7b0846e36b9b2328bb073f486921aacbf29e66337bcb53efe8ab1cdec7cdd11`, 32.614 B: byte-identico al verbale consegnato dal verificatore; invariato a HEAD |
| `6015f8f` | ✅ `git diff --name-status f700326..6015f8f`: soltanto `M PIANO_STATISTICO.md`, `M PIANO_STATISTICO_FREEZE.json`, `M REPORT_PIANO_STATISTICO.md` |
| Manifest rev. 9 | ✅ SHA-256 `586a26239862ed981bed35614486b9596b8f3931d638107ea214c7cb1d40121c`, 17.454 B, uguale al dichiarato |
| Immutati rispetto a `75bd148` | ✅ `VERIFICA_PIANO_STATISTICO.md` (`06c2a45b…`), `design_resolution.py`, `test_design_resolution.py`, `DESIGN_RESOLUTION.json` (`8bf79dc958…`), `DESIGN_RESOLUTION.md` (`9ed15d15e8…`), `DECISIONI_AUTORE_03_8_bozza.md` (`66e04dd2…`), `sottofase_3_8.md` (`git diff --quiet` per ciascuno) |

---

## 1. Correzioni dichiarate dalla revisione 9

| # | Correzione dichiarata | Esito | Fonte primaria |
| --- | --- | :---: | --- |
| 1.1 | Sostituite le due impronte DESIGN_RESOLUTION errate nel report (punto ❌ 7.1 del verbale rev. 8) | ✅ | report rev. 9 r. 166–167: `8bf79dc958e045598cf7538b72752caa902d2f8b134f642e54daaf0274fddbde` e `9ed15d15e8a6210e79573c9e4b3d073dfb8d8d9ed680735d83dc7c35358febb7`, uguali ai ricalcoli sul worktree e ai blob a `7f760b7`, `75bd148`, `6015f8f`; le stringhe errate non compaiono più in alcun file del pacchetto. L'errore è spiegato nel report §1 (nuovo paragrafo su `75bd148`/`f700326`) e §9, senza riscrivere `75bd148` |
| 1.2 | Ripristinati nel manifest `inputs_read` (6 fonti) e le mappe `imposed_by_plan`, `binds_other_subphases`, `does_not_decide` (⚠️ 1.9) | ✅ | manifest rev. 9 r. 26–85. Le sei voci `inputs_read` (percorso, SHA-256, byte) sono **identiche** a quelle del manifest rev. 7 letto da Git (`7f760b7`); `does_not_decide` identico alla rev. 7; `imposed_by_plan` e `binds_other_subphases` differiscono dalla rev. 7 solo per le formulazioni già confermate (sequenza H1→H2→H3 confermata; 8 run, 11 scorte e verifiche tecniche OOD per 03.11; 8 cluster per strato in 03.10; soglie confermate, ordine, remediation unica e riserva per 03.13), come dichiarato nel report §7 r. 150–154 |
| 1.3 | Chiarita la contabilità delle 7/15 chiamate di trasporto (⚠️ 4.7) | ✅ | piano rev. 9 r. 811–814: «Finché si preserva la possibilità di remediation, la sua quota di 8 lascia 7 richieste residue…; senza remediation la formula consente fino a 15 richieste di solo trasporto nella conformità, ma dopo l'ottava la remediation non sarebbe più finanziabile»; report §4 r. 101–105 nello stesso senso. Coerente con l'Allegato B, DECISIONI r. 379–383 (con 8 trasporti consumati restano 7 < 8) e con la formula `8×remediation + trasporto ≤ 15`, invariata |
| 1.4 | Aggiunta la provenienza dei valori Tango 0,8675/0,8075 (⚠️ 7.8) | ✅ | piano rev. 9 r. 283–284: «registrati nell'Allegato A delle decisioni autore e nel report storico al commit `7f760b7`». Riscontro: DECISIONI r. 257–258; `git show 7f760b7:…REPORT_PIANO_STATISTICO.md` r. 169 |
| 1.5 | Documentate le tre precisazioni derivate dall'addendum (⚠️ 2.14/3.15) | ✅ | report rev. 9 §3 r. 85–88: Bahadur–Savage (classe limitata comune), applicabilità IID/multinomiale di Tango come limite, esattezza di Clopper–Pearson non estesa a risposte correlate; dichiarate «non nuove decisioni». Il testo del piano su questi punti è invariato rispetto alla rev. 8 (già verificato conforme all'addendum r. 97, 106, 108) |
| 1.6 | Aggiunta l'integrazione bibliografica alle condizioni residue (⚠️ 5.5) | ✅ | manifest rev. 9 `remaining_conditions.bibliography_integration` r. 276; coerente con piano §16.4 e report §5 |
| 1.7 | Registrato lo storico NON OK della rev. 8 e riverifica rev. 9 pending | ✅ | manifest `revision_history.revision_8` r. 289–298 (`candidate_commit` 75bd148, `independent_review: NON_OK`, verbale con impronta `e7b0846e…dd11` e 32.614 B, `review_checkpoint_commit` f700326, `blocking_finding`), `revision_9` pending; `independent_review` r. 381–385 (`revision_7: OK`, `revision_8: NON_OK`, `revision_9: pending`); `effective_when` r. 6 aggiornato a `revision_9_independent_review_OK…`; `status` `decisions_recorded_pending_reverification`, `freeze_effective: false`, `freeze_tag: null`, `revision: 9`; piano r. 3–6, 31–38, 47–50; report r. 6–9, 122, 184–187 |

Nessuna decisione, formula, valore numerico, sorgente, test o artefatto DESIGN_RESOLUTION è
cambiato: il diff del piano tocca solo intestazioni di revisione (r. 3, 19, 922), la nota della
revisione 9 (r. 31–38), la coda della nota rev. 8 (r. 47–50), la provenienza Tango (r. 283–284),
il rinvio al «report corrente» (r. 518), la glossa della riserva (r. 811–814) e le letture (r.
1013–1014). Il diff del report e del manifest è interamente descritto nei punti 1.1–1.7.

---

## 2. Impronte e controlli eseguibili

| Controllo | Esito |
| --- | --- |
| Manifest: 10/10 `files` + 6/6 `inputs_read`, SHA-256 e byte contro il worktree | ✅ 16/16 (verifica automatica); nessun auto-riferimento (il manifest non contiene il proprio nome né la propria impronta) |
| Validità JSON | ✅ manifest (32 chiavi) e `DESIGN_RESOLUTION.json` |
| `git diff --check 75bd148..6015f8f` | ✅ nessun output, rc 0 |
| `python -m unittest studio2.fase03.piano_statistico.test_design_resolution` | ✅ **26/26 OK** su copia byte-identica dei file rev. 9 (impronte ricontrollate prima e dopo), Python 3.11.15 / numpy 2.4.4; soltanto i calcoli sintetici temporanei della suite, griglia non rigenerata, DESIGN_RESOLUTION immutati. (`/Users/luker/fot-env/bin/python` non è raggiungibile dalla shell isolata; il Python 3.10 locale dà 25/26 per il noto artefatto `pathlib`, vedi verbale rev. 8 §6) |
| `python3 docs/test_explanation.py` | ✅ 35 test, 14 fallimenti, 1 skip: `test_condition_c_contract_and_caveats` (1), `test_one_flow_and_ordered_step_headings` (1), `test_step27_qwen_frozen_results_and_limitations` (9), `test_step27_qwen_protocol_stable_facts` (3) — identici al baseline |
| Verbale rev. 8 nel manifest | ✅ voce `files` r. 331–336 con impronta e byte corretti, ruolo `historical_independent_review_revision_8_NON_OK_preserved_verbatim` |

---

## 3. Limiti di questa verifica

- Verifica ristretta, su richiesta dell'autore, alle correzioni dichiarate, alle impronte e ai
  controlli eseguibili. Non sono stati riletti per intero piano e report rev. 9; ne è stato letto
  per intero il **diff** rispetto alla rev. 8, che è l'unico contenuto nuovo. Per il resto valgono
  il settimo verbale (rev. 7, OK) e il verbale rev. 8 (§2–§5 ✅).
- Nota non bloccante, già segnalata: l'intestazione del piano (r. 3) conserva «Data: 2026-09-13»,
  mentre le note di revisione e il manifest portano 2026-09-14.
- Nessuna rigenerazione della griglia; nessun dato reale; nessuna analisi di potenza nuova.

---

## Conclusione

**OK.** La revisione 9 corregge il punto bloccante del verbale rev. 8 (impronte DESIGN_RESOLUTION
nel report) e recepisce i cinque rilievi raccomandati senza toccare decisioni, formule, codice,
test o artefatti; le 16 impronte del manifest sono corrette, i verbali precedenti sono preservati
byte per byte e i controlli eseguibili sono riprodotti.

La sotto-fase 03.8 **resta aperta**: `freeze_tag` è nullo e nessun freeze è stato creato. Restano
le condizioni residue di piano §16 e del manifest: firma materiale dell'autore, verifiche tecniche
di generabilità/trip/ammissibilità di F6/F4 e degli eventuali sostituti, decisione organizzativa
preventiva sul ramo R=3 (5.184 > 3.700, senza automatismi), integrazione bibliografica nel ramo
destinato a `main`, allineamenti esterni elencati nel report §6, commit raggiungibile da
`origin/main` e, solo dopo, manifest congelato e tag secondo MAINTENANCE §8.4, prima del primo run
di test (03.11) e del pilot.

Percorso di questo verbale:
`studio2/fase03/piano_statistico/VERIFICA_PIANO_STATISTICO_REV9.md`.
