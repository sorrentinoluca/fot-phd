# Consegna — acquisizione OK e documentazione del raccordo metriche 03.9 → 03.10

> Report di **consegna** del lavoro di orchestrazione: acquisizione dell'OK indipendente del delta,
> registrazione dell'OK e preparazione della documentazione. È un documento distinto e separato dal
> verbale (`VERIFICA_RACCORDO_METRICHE.md`), dalla consegna del revisore
> (`CONSEGNA_VERIFICA_RACCORDO_METRICHE.md`), dalla consegna dell'esecutore
> (`CONSEGNA_RACCORDO_METRICHE_03_10.md`) e dal report implementativo già improntato
> (`REPORT_RACCORDO_METRICHE.md`), tutti preservati byte-identici. Autosufficiente: la finestra
> orchestratrice può proseguire senza leggere la conversazione che lo ha prodotto. Nessun
> commit/merge/push/tag è stato effettuato per produrre questa consegna.

## 1. Sottofase, data, attività, esito

- **Sottofase:** 03.10 — harness API e input pilot; delta circoscritto al **raccordo (adattamento
  offline) delle metriche** della baseline numerica 03.9 verso il contratto endpoint 03.10.
- **Data:** 2026-09-14, Europe/Rome.
- **Attività:** acquisizione dell'OK indipendente sul **solo delta** `5116087..caf5bfb` (senza
  rieseguire la review né modificare l'implementazione verificata): acquisizione byte-identica del
  verbale e delle due consegne, commit locale separato di acquisizione, nuovo record successivo che
  registra l'OK, preparazione degli hunk documentali MD/HTML e del piano d'integrazione selettiva.
- **Esito:** **OK, limitato al delta `5116087..caf5bfb`.** NON è un OK dell'intero harness, NON
  chiude 03.9 né 03.10, non rende efficace alcun freeze, non autorizza chiamate/simulazioni/analisi
  sui run finali.

## 2. Worktree, branch, commit di riferimento

- **Copia isolata di lavoro (percorso assoluto):**
  `/Users/luker/fot-tep/.worktrees/acquisizione-raccordo-ok`
  — creata dal candidato esatto `1ac06eb` perché il worktree proprietario
  `/Users/luker/fot-tep/.worktrees/studio2-harness` non è usabile da questa sessione montata (il suo
  `.git` punta a `/Users/luker/fot-tep/.git/worktrees/studio2-harness`, non risolvibile nel mount).
- **Branch locale nuovo:** `codex/studio2-harness-raccordo-ok` (tip `6c51330`).
- **Commit di riferimento:** base del delta `51160872906feaa63c1fda5e9cf6e0fe8538fb16`; candidato
  tecnico verificato `caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae`; commit di registrazione
  report/manifest `1ac06ebdc92f73d3b630ccca9bf75f413bea170b`; sorgente 03.9
  `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` (origin/main).
- **Catena risultante:** `caf5bfb` → `1ac06eb` → `51742bb` → `6c51330`.
- **Non toccati:** `codex/studio2-harness` (resta a `1ac06eb`), `origin/main` (`c486eee`), i worktree
  del revisore (`verifica-raccordo-caf5bfb`, `verifica-raccordo-main-c486eee`), del raccordo seriale
  e della 03.15.

Nota infrastrutturale: i due commit locali sono stati creati in un repo di lavoro isolato fuori dal
mount (dove i lockfile git funzionano) e trasferiti nel repository come **oggetti additivi**
(`git unpack-objects`); il ref locale `codex/studio2-harness-raccordo-ok` è stato poi puntato a
`6c51330`. Nessun oggetto o commit preesistente è stato modificato o rimosso.

## 3. File creati o modificati e report/verbali pertinenti

**Committati** (branch `codex/studio2-harness-raccordo-ok`), selezione esplicita:

- `51742bb` (acquisizione) — creati (A):
  - `studio2/fase03/harness/VERIFICA_RACCORDO_METRICHE.md` (verbale del revisore)
  - `studio2/fase03/harness/CONSEGNA_VERIFICA_RACCORDO_METRICHE.md` (consegna del revisore)
  - `studio2/fase03/harness/CONSEGNA_RACCORDO_METRICHE_03_10.md` (consegna dell'esecutore, prima non tracciata)
- `6c51330` (registro OK) — creato (A):
  - `studio2/fase03/harness/REGISTRO_OK_RACCORDO_METRICHE.md`

**Non committati** (questa consegna e i materiali di consegna, nella copia isolata):

- `studio2/fase03/harness/CONSEGNA_ACQUISIZIONE_OK_RACCORDO_METRICHE.md` (**questo report**)
- `_delivery/DELIVERY_README.md`, `_delivery/PIANO_INTEGRAZIONE_RACCORDO_METRICHE.md`,
  `_delivery/hunk_walkthrough_studio2_md.patch`, `_delivery/hunk_walkthrough_studio2_html.patch`,
  `_delivery/sezione_4_10.md.txt`

**Report/verbali pertinenti già esistenti nel repository (preservati byte-identici):**

- `studio2/fase03/harness/REPORT_RACCORDO_METRICHE.md` (in `1ac06eb`; SHA-256 `8ab3ac62…`, registrato nel manifest)
- `studio2/fase03/harness/CONTRATTO_RACCORDO_METRICHE.md` (in `caf5bfb`; SHA-256 `5c81586f…`)
- `studio2/fase03/harness/METRIC_INTERFACE_CANDIDATE.json` (in `1ac06eb`; `independent_verification: PENDING` conservato)
- `studio2/fase03/harness/PROMPT_VERIFICA_RACCORDO_METRICHE.md` (in `1ac06eb`)
- `studio2/fase03/baseline_numerica/INTERFACE_CHECK.json` (in `c486eee`)

## 4. Controlli eseguiti, risultati e limiti

Controlli di identità/coerenza svolti in questa finestra (in sola lettura sulle fonti, nessuna
riesecuzione della review):

- **Identità verbale sorgente = copia = blob Git:** SHA-256 del verbale
  `0d90779981871b8c9ceaf2a729f97b371abb7297fb804dc4335ddf0f1bec0e80`, **coincidente** con l'atteso;
  copia acquisita byte-identica; blob Git `dc3c835e` presente nel repository. Prima riga `VERDETTO: OK`.
- **Impronte delle fonti acquisite:** consegna revisore `9c8e01a3…` (8970 B); consegna esecutore
  `3945e9c6…` (8524 B).
- **Preservazione byte-identica** (blob invariati al tip `6c51330`): REPORT, CONTRATTO, MANIFEST,
  PROMPT, e codice verificato `metric_adapter.py`/`metrics.py`/`test_harness.py`/`SPECIFICA_HARNESS.md`.
- **Ambito dei commit:** `51742bb` tocca solo i 3 file di acquisizione; `6c51330` solo il registro OK.
- **Hunk documentali:** `git apply --check` dei due patch contro il candidato comune `e82b5a0`: OK;
  parità di contenuto MD/HTML della nuova §4.10; anchor `harness-raccordo-metriche-0310` presente.

Esiti dei test **riportati dal verbale/consegne** (non rieseguiti qui): MetricTests 9/9;
baseline 03.9 10/10; suite protocollo/guardie/harness 34 con **skipped=2** (revisore); guardiano
documentale 35 test, 14 failure, 1 skip; equivalenza 12.341 valid-only + 10.626 con invalidi PASS.

Limiti:

- L'OK vale **solo** per il commit/impronte/perimetro del delta `5116087..caf5bfb`, non per HEAD futuri.
- **Distinzione da mantenere:** i **due skip del revisore** (checkout esterni 03.12 e 03.6 non
  montati) sono cosa diversa dall'**unico errore locale dell'esecutore** sul vecchio pin 03.12.
  **Il problema del pin 03.12 resta APERTO e fuori incarico**: non convertito in PASS, non corretto.
- Dipendenza normativa non ancora integrata: la semantica invalidità/astensione/denominatori poggia
  su `studio2/fase03/piano_statistico/DELTA_HARNESS_03_10.md` della rev. 10, riferimento Git stabile
  `6aaa5b3` (blob `780e08ae`, contenuto SHA-256 `e92661fe…`); il piano statistico non è stato
  importato né modificato.
- Non sono stati aperti dati/run finali, non misurate prestazioni, nessuna chiamata API/simulazione.

## 5. Stato Git finale

Stato autorevole (osservato dal repository principale):

- **Committati** — branch `codex/studio2-harness-raccordo-ok`, tip `6c51330`:
  `51742bb` (3 file A: verbale + consegna revisore + consegna esecutore), `6c51330` (1 file A:
  registro OK). Nessun file tracciato **modificato** dai due commit (solo aggiunte).
- **Modificati (tracciati):** nessuno.
- **Non tracciati (`??`) nella copia isolata**, per esplicita richiesta non committati:
  - `studio2/fase03/harness/CONSEGNA_ACQUISIZIONE_OK_RACCORDO_METRICHE.md` (**questo report**);
  - `_delivery/` (README, piano d'integrazione, i due patch, anteprima §4.10).
- **Altri branch/ref:** `codex/studio2-harness` = `1ac06eb` (invariato); `origin/main` = `c486eee`
  (invariato). **Nessun** merge/push/tag.
- **Nota sull'indice della copia isolata:** poiché il ref di branch è stato avanzato tramite
  trasferimento di oggetti (e non con un commit eseguito dentro questo worktree), `git status` nella
  copia isolata mostra un artefatto cosmetico (`deleted: REGISTRO_OK_RACCORDO_METRICHE.md`) rispetto
  al tip: è dovuto all'indice/working-tree fermi alla base `1ac06eb`, non a una perdita di contenuto.
  Gli oggetti committati e il tip `6c51330` sono completi e verificati dal repository principale.
- **Residui di lock:** file `.lock` e `tmp_obj_*` sotto `.git` (il mount nega `unlink`): innocui in
  lettura, rimuovibili solo con permesso di cancellazione. **Lock del revisore non toccati.**

## 6. Stato effettivo di integrazione, pubblicazione, congelamento

- **Integrazione:** **non integrata.** Il delta e i commit di acquisizione/OK restano su branch
  locali; l'adapter non è collegato ai run finali; nessun merge in `main`.
- **Pubblicazione:** nulla pubblicato; nessun walkthrough aggiornato (gli hunk sono **preparati, non
  applicati**); nessun tag.
- **Congelamento:** **nessun freeze reso efficace.** `HARNESS_FREEZE.json` resta la fotografia
  *pending* del candidato precedente e non è il manifest di questo delta. `BASELINE_FREEZE_rev003.json`
  resta `effective=false`. **03.9, 03.10 e Fase 03 restano APERTE.**

## 7. Operazioni residue, dipendenze, decisioni dell'autore, prossimo passo

- **Residui/dipendenze:** integrazione della rev. 10 nel branch harness; raggiungibilità in
  `origin/main` dei sorgenti 03.6 (blocca il freeze 03.9); completamento di pin 03.12, ordine delle
  label, endpoint e qualificazione dei modelli; problema pin 03.12 aperto e separato.
- **Decisioni dell'autore/orchestratore:** il mapping delle metriche non richiede nuova decisione
  (fissato dalle specifiche). Da decidere se procedere all'integrazione selettiva del raccordo
  secondo il piano allegato; l'errore del pin 03.12 è materia separata.
- **Prossimo passo:** integrazione selettiva coordinata (un solo writer seriale) secondo
  `_delivery/PIANO_INTEGRAZIONE_RACCORDO_METRICHE.md`: portare i file del raccordo per path (non
  `git merge` del branch divergente), applicare i due hunk MD/HTML insieme, verificare
  `docs/test_explanation.py` non peggiore della baseline, preservare gli artefatti già improntati;
  nessun tag di freeze finché i prerequisiti 03.9 (sorgenti 03.6 in main, controlli previsti) non
  sono soddisfatti.
