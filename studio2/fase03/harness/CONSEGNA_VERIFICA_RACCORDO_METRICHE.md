# Consegna — Verifica indipendente del raccordo metriche 03.9 → 03.10

> Report di **consegna** del lavoro di verifica indipendente. È un documento distinto e separato
> dal verbale `VERIFICA_RACCORDO_METRICHE.md`, che resta preservato e verificato per impronta.
> Autosufficiente: la finestra orchestratrice può proseguire senza leggere la conversazione che
> lo ha prodotto. Nessun commit/merge/push/tag è stato effettuato per produrre questa consegna.

## 1. Sottofase, data, attività, esito

- **Sottofase:** raccordo (adattamento offline) delle metriche fra baseline numerica **03.9** e
  harness **03.10** — delta `5116087..caf5bfb` sul branch `codex/studio2-harness`.
- **Data:** 2026-09-14 18:35 CEST (UTC+02:00).
- **Attività:** verifica indipendente, in **sola lettura**, del solo delta implementativo
  `caf5bfb` (ricostruzione del contratto dalle fonti primarie, audit del diff, verifica autonoma
  dell'equivalenza metrica, riesecuzione delle suite di test e del guardiano documentale).
  Nessuna correzione del candidato, nessuna finestra condivisa con l'autore.
- **Esito:** **VERDETTO: OK**, limitato al delta `5116087..caf5bfb`. Non è un OK dell'intero
  harness né della sottofase 03.9/03.10.

## 2. Worktree, branch, commit di riferimento

- **Copia isolata di verifica (candidato):**
  `/Users/luker/fot-tep/.worktrees/verifica-raccordo-caf5bfb`
  — detached HEAD su `caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae` (origine: branch
  `codex/studio2-harness`).
- **Copia isolata gemella (main 03.9, per i test baseline):**
  `/Users/luker/fot-tep/.worktrees/verifica-raccordo-main-c486eee`
  — detached HEAD su `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`.
- **Worktree proprietario (NON toccato):**
  `/Users/luker/fot-tep/.worktrees/studio2-harness`, branch `codex/studio2-harness`.
- **Commit di riferimento:** base del delta
  `51160872906feaa63c1fda5e9cf6e0fe8538fb16`; candidato
  `caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae`; sorgente 03.9
  `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`. Il report/verbale dell'autore
  `REPORT_RACCORDO_METRICHE.md` è stato aggiunto nel commit successivo
  `1ac06eb` (fuori dal delta verificato).

## 3. File creati/modificati e report/verbali pertinenti

Creati da questa verifica (nella copia isolata candidata, **non committati**):

- **Verbale:** `/Users/luker/fot-tep/.worktrees/verifica-raccordo-caf5bfb/studio2/fase03/harness/VERIFICA_RACCORDO_METRICHE.md`
  — SHA-256 `0d90779981871b8c9ceaf2a729f97b371abb7297fb804dc4335ddf0f1bec0e80`
  (prima riga `VERDETTO: OK`).
- **Questa consegna:** `/Users/luker/fot-tep/.worktrees/verifica-raccordo-caf5bfb/studio2/fase03/harness/CONSEGNA_VERIFICA_RACCORDO_METRICHE.md`.
- **Script di equivalenza (scratch, fuori dal repository, effimero):** `~/verif_equiv.py` nella
  home della VM di sessione — non nel repository, non committato, cancellato con la sessione.

Nessun file tracciato è stato modificato dalla verifica. Il delta dell'autore (per riferimento,
non prodotto qui) tocca 5 file: `CONTRATTO_RACCORDO_METRICHE.md` (nuovo),
`SPECIFICA_HARNESS.md` (mod.), `metric_adapter.py` (nuovo), `metrics.py` (+1 riga),
`test_harness.py` (mod.: soli 6 metodi `MetricTests`).

Report/verbali pertinenti già esistenti nel repository:
`studio2/fase03/harness/CONTRATTO_RACCORDO_METRICHE.md` (in `caf5bfb`),
`studio2/fase03/harness/REPORT_RACCORDO_METRICHE.md` (in `1ac06eb`),
`studio2/fase03/baseline_numerica/INTERFACE_CHECK.json` (in `c486eee`).

## 4. Controlli eseguiti, risultati e limiti

Integrità fonti: i 4 SHA-256 pinnati nel contratto (baseline.py, SPECIFICA_BASELINE_NUMERICA.md,
INTERFACE_CHECK.json, BASELINE_FREEZE_rev003.json su `c486eee`) **coincidono**. Diff
`5116087..caf5bfb` = 5 file, +484/−1, `git diff --check` pulito.

Otto punti del prompt, tutti ✅ su fonte primaria:
1. mapping `accuracy→accuracy_all`, `n→total`, `abstentions→abstained` (metric_adapter +
   baseline.py::metric); 2. `non_abstained` preservato `= total−abstained`; 3. `invalid=0`
   solo per sorgente 03.9 valid-only (baseline scrive `valid="true"` e arresta sugli input non
   validi); 4. invalidi non corretti né astensioni, dentro il denominatore di
   `accuracy_non_abstained` (three_numbers); 5. `null` solo a denominatore zero + rifiuto
   fail-closed (campi/conteggi/rapporti/struttura/SHA-256); 6. tutte le foglie summary/clusters
   adattate, i tre valori numerici copiati per identità di oggetto (non ricalcolati); 7. nessun
   consumer omesso (unico lettore `metric_adapter.load_baseline_metrics`; unico consumatore del
   contratto a tre numeri `metrics.endpoint_statistic`); 8. nessuna modifica fuori perimetro.

Test rieseguiti:
- `MetricTests` @`caf5bfb`: **9/9 OK**.
- suite 03.9 (`test_baseline`, `test_normal_dev_plan`, `test_extract_normal_evidence`) nel
  checkout main `c486eee`: **10/10 OK**.
- suite protocollo/guardie/harness @`caf5bfb`: **34 test, OK, skipped=2**.
- guardiano documentale `docs/test_explanation.py` @`caf5bfb`: **35 test, 14 failure, 1 skip,
  0 errori** (coincide con la baseline nota di MAINTENANCE §5; failure tutti in
  `UnifiedConversationChecks`, walkthrough v1, estranei al delta).
- equivalenza indipendente `baseline.py::metric` ↔ adapter ↔ `three_numbers`: **12.341**
  configurazioni valid-only (con identità degli oggetti numerici) + **10.626** configurazioni con
  invalidi + tutte le rotture fail-closed e il gate SHA-256: PASS.

Limiti della verifica:
- Il test noto ed **estraneo** 03.12
  (`test_harness.AdapterAndGuardTests::test_real_0312_adapter_when_checkout_is_available`) qui
  **skippa** (percorso assoluto `/Users/luker/fot-tep-schema-insight/...` non montato nella
  sandbox), quindi non è stato riprodotto come errore; identificativo e causa coincidono con quanto
  dichiarato, non è stato trasformato in PASS né corretto. Idem
  `test_real_036_release_inventory_when_checkout_is_available` (checkout 03.6 non montato).
- `DELTA_HARNESS_03_10.md` è stato letto da `codex/studio2-piano-statistico-fix` (worktree non
  montato) via `git show`, limitatamente a astensione/invalidità/denominatori come richiesto.
- Verifica svolta interamente nella VM di sessione; i test dipendenti da checkout fratelli via
  percorso assoluto non sono eseguibili qui e restano skip.

## 5. Stato Git finale

- **Copia isolata candidata** (`/Users/luker/fot-tep/.worktrees/verifica-raccordo-caf5bfb`):
  HEAD detached su `caf5bfb`; **nessun commit** creato; **nessun file tracciato modificato**;
  **staged: nessuno**.
  - **Non tracciati (`??`):**
    `studio2/fase03/harness/VERIFICA_RACCORDO_METRICHE.md` (il verbale) e
    `studio2/fase03/harness/CONSEGNA_VERIFICA_RACCORDO_METRICHE.md` (**questo report**).
- **Copia isolata main** (`/Users/luker/fot-tep/.worktrees/verifica-raccordo-main-c486eee`):
  **pulita**, HEAD detached su `c486eee`, nessuna modifica.
- **Nessun commit, merge, push o tag** è stato eseguito in alcun worktree.
- **Nota infrastrutturale:** nei metadati `.git/worktrees/<nome>/` restano file di lock
  (`HEAD.lock`, `locked`, `index.lock`) non rimovibili perché il mount non concede la
  cancellazione; sono innocui e non intaccano `status`/`diff`/`log` né i test.

## 6. Stato di integrazione, pubblicazione, congelamento

- **Integrazione:** **non integrata.** L'adapter non è collegato ai run finali; il delta resta sul
  branch proprietario `codex/studio2-harness`. La verifica non integra nulla.
- **Pubblicazione:** nulla di pubblicato; nessun walkthrough aggiornato; nessun tag creato.
- **Congelamento:** **nessun freeze reso efficace.** `HARNESS_FREEZE.json` resta la fotografia
  *pending* del candidato precedente e non è il manifest di questo delta. **03.9/03.10 NON
  dichiarate chiuse.**

## 7. Operazioni residue, dipendenze, decisioni dell'autore, prossimo passo

- **Acquisizione del verbale:** la finestra proprietaria/orchestratrice deve acquisire il verbale
  separatamente (percorso e SHA-256 al §3), senza presentare il revisore come autore.
- **Dipendenza aperta:** la semantica invalidità/astensione dell'harness poggia su
  `DELTA_HARNESS_03_10.md` (rev.10, branch `codex/studio2-piano-statistico-fix`), non ancora
  integrato nel branch harness.
- **Decisione dell'autore/orchestratore:** dato il VERDETTO OK sul solo delta, decidere se
  procedere all'aggiornamento della documentazione e all'integrazione del raccordo; l'errore
  estraneo del pin 03.12 è materia separata, fuori da questo perimetro, e non va convertito in PASS
  in questa sede.
- **Pulizia opzionale:** `git worktree remove` delle due copie isolate
  (`verifica-raccordo-caf5bfb`, `verifica-raccordo-main-c486eee`) quando si disporrà del
  permesso di cancellazione; finché restano, sono coerenti con le altre `verifica-*` presenti.
- **Prossimo passo:** la finestra orchestratrice registra l'esito indipendente (OK sul delta) e
  prosegue secondo il proprio flusso; nessuna azione di commit/merge/push/tag è richiesta a questa
  finestra di verifica.
