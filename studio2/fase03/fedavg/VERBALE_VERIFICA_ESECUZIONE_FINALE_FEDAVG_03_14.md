# Verbale di verifica indipendente — esecuzione finale FedAvg 03.14

**Esito: OK** — limitato all'esatto candidato:

- commit `8cb9a8bc62ddd207ed1ed7a287e0124ceae07999`
- tree `49b4b0d2286ad3ac54cf78ab14778cffc959eb90`
- parent `546edd7a1544beae06b3544a9de2eb659dcedbee`
- branch sorgente `codex/studio2-fedavg` (tip = commit candidato)

Verifica in sola lettura. Nessun commit, merge, rebase, push, tag, né modifica del candidato o
di walkthrough/manoscritto. Non eseguiti Qwen/LLM, simulazioni TEP, tuning, bootstrap o confronti
col braccio LLM. Le prestazioni non sono state usate per proporre modifiche alla ricetta.

Data verifica: 2026-09-15 (Europe/Rome). Verificatore: sessione indipendente, sola lettura.

---

## 1. Commit / tree / parent e delta sui file congelati — OK

- `git cat-file` sul candidato: `tree 49b4b0d2…`, `parent 546edd7a…` — coincidono con i valori attesi.
- `git rev-parse codex/studio2-fedavg` = `8cb9a8bc…` (il branch punta esattamente al candidato).
- Delta `parent..candidato` (`git diff --name-status`): **1 solo file modificato**,
  `studio2/fase03/fedavg/REPORT_FEDAVG.md` (append: +59 / −0; il contenuto del parent è prefisso
  esatto del candidato — verificato con `cmp`); tutti gli altri 637 percorsi sono **aggiunte**
  (`FINAL_PROTOCOL.json`, l'albero `final/` con 624 firme + manifest + summary + `weight_hashes.json`,
  `final_fedavg.py`, `test_final_fedavg.py`). Nessuna cancellazione.
- Otto file congelati dichiarati in `FEDAVG_FREEZE.json` / `INPUT_PREFLIGHT.json` → per ciascuno
  SHA-256 del blob del candidato **identico al parent e identico al valore dichiarato**:
  `SPECIFICA_FEDAVG.md`, `fedavg.py`, `requirements.txt`, `smoke_fedavg.py`, `test_fedavg.py`,
  `smoke_fixture/cluster_metrics.csv`, `smoke_fixture/weight_hashes.json`,
  `smoke_fixture/SMOKE_SUMMARY.json`.
- `package.tree 07cab1de…` = root tree del commit parent (`git rev-parse 546edd7^{tree}`) —
  coerente, nessuna discrepanza.

## 2. Provenienza pre-test della decisione OOD — OK (con limite temporale documentato)

- `FINAL_PROTOCOL.json`: `recorded_before_final_signature_extraction=true`,
  `author_decision_date=2026-09-15`; SHA-256 = `5eaa0418…76f9a` (ricalcolato, coincide con
  `INPUT_PREFLIGHT.ood.protocol_sha256` e con l'hash citato nel REPORT).
- Decisione materializzata: 72 run primari nelle metriche; 6 OOD **separati come sole attribuzioni
  forzate**; astensione strutturale 0; `accuracy_defined=false`; `included_in_primary_metrics=false`;
  `direct_comparison_with_llm_abstention=false`. Riscontro negli artefatti: `PRIMARY_SUMMARY.json`
  (`ood_included=false`, runs=72) e `OOD_SUMMARY.json` (accuracy non definita, esclusa dalle
  primarie, nessun confronto LLM); `ood_forced_attributions.csv` privo di colonne `accuracy`/`correct`.
- Ordine imposto dal codice (`final_fedavg.py`): `preflight()` scrive `INPUT_PREFLIGHT.json` con
  `execution_started=false` e **non** estrae firme né allena; `execute()` esige un preflight PASS
  non usato, verifica che l'hash del protocollo coincida con quello legato nel preflight e che il
  manifest non sia cambiato, e **solo dopo** estrae, allena e valuta. La decisione OOD è quindi
  legata (per hash) al preflight prima di estrazione/training/lettura metriche.
- **Limite**: essendo il pacchetto un unico commit, la precedenza è stabilita per costruzione
  (gating fail-closed + digest del protocollo legato al preflight), non da timestamp indipendenti.
  Come richiesto, il punto è segnalato come limite e non inferito oltre l'evidenza strutturale;
  non è un rilievo bloccante perché l'esclusione OOD dalle metriche primarie è dimostrata sugli
  artefatti.

## 3. Ricalcolo digest — OK

- SHA-256 ricalcolati e coincidenti per i 7 artefatti elencati in `FINAL_SUMMARY.artifacts`
  (`FINAL_EVIDENCE_MANIFEST.csv`, `FINAL_SET_MANIFEST.csv`, `OOD_SUMMARY.json`,
  `PRIMARY_SUMMARY.json`, `ood_forced_attributions.csv`, `primary_cluster_metrics.csv`,
  `weight_hashes.json`).
- `EXECUTION_STATE.final_summary_sha256` = SHA-256(`FINAL_SUMMARY.json`) — coincide
  (`7ef542e8…9db1`).
- `FINAL_PROTOCOL.json` → `5eaa0418…76f9a` coincide con `INPUT_PREFLIGHT.ood.protocol_sha256`.
- `INPUT_PREFLIGHT.final_set.manifest_sha256` = SHA-256(`FINAL_SET_MANIFEST.csv`) — coincide.
- **624 firme**: per ciascuna, byte e SHA-256 su disco = valori nel `FINAL_EVIDENCE_MANIFEST.csv`
  (0 discordanze); `signature_dimension=697` per tutte; l'insieme dei percorsi referenziati
  coincide 1:1 con i file presenti in `final/signatures/` (624 = 624).
- I quattro sorgenti congelati `code/*` (tep_features, tep_verbalize_v2, verbalizer_config_v2,
  evaluate_verbalizer_v2) hanno SHA-256 del candidato pari ai valori dichiarati in
  `pipeline.frozen_sources`.

## 4. Selezione e separazione — OK

- `FINAL_SET_MANIFEST.csv`: 78 run = **72 primari (64 fault + 8 Normal) + 6 OOD** (F4×3, F5×3);
  etichette primarie: F1,F2,F3,F8,F10,F13,F14,F15,Normal × 8 ciascuna. `windows=8` per ogni run
  (576 finestre primarie + 48 OOD). `run_id` unici; `source_sha256` unici nel set.
- **11 scorte escluse**: 89 generati − 78 selezionati = 11 (coerente con `role_counts.spare=11`,
  `spares_included=0`).
- `FINAL_EVIDENCE_MANIFEST.csv`: partizione `primary=576 / ood=48`; ogni run ha 8 finestre con
  ordinali 1..8; coppie `(run_id, window_ordinal)` uniche → **join evaluator-side uno-a-uno**;
  start finestre = {25,30,35,40,45,50,55,60} h. Join `evidence↔set-manifest` senza discordanze
  (source_sha256, source_manifest_sha256, true_label, scope).
- **697 valori finiti per firma**: verificato su tutte le 624 firme (nessun valore non finito).
- Separazione sviluppo↔test: `separation.development_final_run_overlap=0` e
  `development_final_source_hash_overlap=0`, imposti fail-closed nel codice; unicità dei
  `source_sha256` finali verificata direttamente. Vedi limite in §Limiti per la ri-derivazione
  indipendente rispetto ai bundle di sviluppo.

## 5. Riuso byte congelati 03.6 e training solo-sviluppo — OK (per costruzione; limite di ri-hash)

- `final_fedavg.py` è fail-closed: `load_verified_extractor` impone SHA-256 dell'estrattore 03.6
  (`46b451c2…`) e di `leakage.py` (`c77ae5b1…`); `require_hash` su baseline (`79883dd0…`) e su
  guardia R2 (`7df0cef2…`) più `validate_r2_guard`. I bundle di sviluppo sono caricati con hash di
  manifest/index attesi (fault `5111d0c6…`/`b966cdd3…`, normal `cc8d96c2…`/`27a53450…`, questi
  ultimi due cross-registrati in `FEDAVG_FREEZE.json`).
- Training/normalizzazione: `train_all_modes(development, Config())` con
  `development = fault ⊕ normal`, forma imposta `(640, 697)`, 80 cluster, otto client, batch
  {1..5}; normalizzazione z-score fittata solo sullo sviluppo (`normalization_scope=development_only`,
  `training_scope=development_03_6_and_03_9_only`). Nessun accesso ai test in training.
- **Limite**: i file dell'estrattore/leakage 03.6 e i bundle di sviluppo (fault/normal) **non sono
  presenti nella cartella montata** (`/Users/luker/fot-tep`); risiedono nel rilascio evidence 03.6
  e in altri worktree. Il riuso dei byte congelati è quindi verificato per costruzione (gate
  fail-closed + hash cross-registrati), non tramite ri-hash diretto dei sorgenti. Non bloccante.

## 6. Ricetta e ambiente — OK (ambiente di verifica ≠ freeze: vedi limite)

- Costanti in `fedavg.py` `class Config`: `input_dim=697`, `hidden_dim=32`, `output_dim=9`,
  `learning_rate=0.05`, `batch_size=32`, `local_epochs=5`, `rounds=40`, `seed=20260914`,
  `std_floor=1e-8` → MLP 697→32→9, nessun tuning. Coincide con `FINAL_SUMMARY.config` e con la
  ricetta di `FEDAVG_FREEZE.json`.
- Ambiente dichiarato negli artefatti: Python 3.13.9, NumPy 2.3.5, `tuning=false`,
  `training_attempts=1`, `evaluation_attempts=1`.
- **Limite**: la macchina di verifica esegue Python 3.10.12 / NumPy 2.2.6, **non** l'ambiente di
  freeze. Ininfluente su ricalcoli di hash/manifest/metriche (conteggi interi + SHA-256), ma
  impedisce un replay dei pesi byte-esatto (vedi §9).

## 7. Ricalcolo metriche dai CSV — OK

Aggregazione diretta di `primary_cluster_metrics.csv` (720 righe: local 576, fedavg 72,
centralized 72; `n_attempts=8` e `abstentions=0` su tutte), **senza fidarsi dei summary**:

| Modalità | Corretti / tentativi | Accuratezza | Astensioni |
| --- | ---: | ---: | ---: |
| Local (otto ricevitori) | 897 / 4608 | `0.19466145833333334` | 0 |
| FedAvg | 434 / 576 | `0.7534722222222222` | 0 |
| Centralizzato | 443 / 576 | `0.7690972222222222` | 0 |

Valori identici a quelli richiesti; denominatore Local = 576 × 8 ricevitori = 4608. OOD esclusi
dalle metriche primarie.

## 8. Righe OOD (180) — OK

- `ood_forced_attributions.csv`: **180 righe** = 10 combinazioni modello/ricevitore
  (8 Local F1..F8 + fedavg/shared + centralized/shared) × 2 fault (F4,F5) × 9 classi.
- 20 gruppi `(modello, ricevitore, fault)`, **ciascuno somma a 24 predizioni**; astensioni e
  `abstention_rate` a 0 su tutte le righe.
- Nessuna colonna `accuracy` o `correct` — attribuzioni non trasformate in accuratezza.

## 9. Flag di attempt e replay — OK (recompute completo; replay byte-esatto non applicabile)

- `EXECUTION_STATE.json`: `training_attempt=1`, `evaluation_attempt=1`, `rerun_allowed=false`,
  `status=completed`. `final_fedavg.execute()` rifiuta l'esecuzione se esiste già
  `EXECUTION_STATE.json` o se il preflight è già usato (single-pass imposto).
- Non è stato eseguito un replay indipendente byte-esatto: l'ambiente di freeze
  (Py 3.13.9 / NumPy 2.3.5) non è riproducibile sulla macchina di verifica e gli input scientifici
  esterni (estrattore/leakage 03.6, bundle di sviluppo, archivio/sorgenti test-batch 03.11 in
  `/Users/luker/fot-tep-wt-0311`) non sono nella cartella montata. Come previsto dal perimetro, in
  assenza di replay si è eseguito il **ricalcolo completo di manifest e metriche** (§3, §4, §7, §8),
  con esito coerente.

## 10. Test finali ed esecuzione — OK

- `test_final_fedavg.py` (suite introdotta dal delta): **4/4 test superati**
  (`test_preflight_and_execution_are_single_pass`, `test_final_evidence_partition`,
  `test_primary_denominators`, `test_ood_has_counts_but_no_accuracy`). La suite è di sola
  ispezione strutturale (csv/json, senza NumPy), quindi l'esito è valido anche sotto l'interprete
  non-freeze.
- Non è stata rilanciata `test_fedavg.py` (congelata, fuori dal delta) né alcun guardiano
  documentale non toccato dal delta, come da perimetro.

### Classificazione delle azioni svolte
- **Test eseguiti**: `test_final_fedavg.py` (4/4 OK).
- **Ricalcoli**: digest artefatti/protocollo/manifest, 624 firme (byte+SHA+dimensione+finitezza),
  metriche primarie dai CSV, gruppi/somme OOD, hash degli 8 file congelati e dei 4 sorgenti `code/*`.
- **Replay**: non eseguito (non necessario/non applicabile — vedi §9).
- **Sola ispezione**: `final_fedavg.py`, `fedavg.py` (Config/ordine pipeline), `FINAL_PROTOCOL.json`,
  `FEDAVG_FREEZE.json`, append del REPORT.

---

## Rilievi bloccanti

Nessuno.

## Limiti (non bloccanti)

1. Precedenza temporale della decisione OOD stabilita per costruzione (gating fail-closed + digest
   nel preflight), non da timestamp indipendenti — pacchetto in commit unico (§2).
2. Estrattore/leakage 03.6, bundle di sviluppo fault/normal e archivio+sorgenti test-batch 03.11
   non presenti nella cartella montata `/Users/luker/fot-tep`; le relative provenienze sono
   verificate per costruzione (hash attesi fail-closed, alcuni cross-registrati) ma non per
   ri-hash diretto dei sorgenti (§3, §4, §5).
3. Replay byte-esatto dei pesi non eseguibile: ambiente di verifica Python 3.10.12 / NumPy 2.2.6
   ≠ freeze Python 3.13.9 / NumPy 2.3.5 (§6, §9). I `weight_hashes.json` non sono stati
   ri-derivati; sono stati verificati come artefatto (digest, §3).

## Conclusione

Per l'esatto commit `8cb9a8bc62ddd207ed1ed7a287e0124ceae07999` / tree
`49b4b0d2286ad3ac54cf78ab14778cffc959eb90`: **OK**. Tutti i controlli del perimetro eseguibili in
sola lettura sulla cartella montata risultano coerenti; i punti non ricalcolabili localmente sono
elencati come limiti e coperti dai gate fail-closed del pacchetto. La chiusura formale di 03.14
resta comunque di competenza dell'autore.

<!-- VERBALE-SHA256 -->
SHA-256 del verbale (byte precedenti la riga marcatrice `<!-- VERBALE-SHA256 -->`): `9b6ae3c2dcbd123265741b8300223203ca343b4fd052e106c3e9a8ba09988e9b`
