# Verifica indipendente — sotto-fase 3 della Fase 03 (run fault di sviluppo): **OK, con condizioni**

Verdetto: **OK**. Nessun riscontro ❌. Tutti i sette controlli richiesti reggono sulle fonti
primarie; il replay MATLAB del punto 4 **non era eseguibile** dalla finestra di verifica (nessun
MATLAB raggiungibile) ed era la prima condizione di efficacia (§9): è stato poi eseguito dall'autore
e **verificato da me sugli artefatti** — esito positivo, vedi **Appendice A**. Le discrepanze
trovate (§8) sono di tracciabilità e non toccano catalogo, indici, stream, onset, orizzonte,
finestre, dati o conservazione.

| Campo | Valore |
| --- | --- |
| Data | 2026-09-13 |
| Oggetto | `studio2/fase03/fault_runs/` al commit `3b9ec1e`, branch `codex/studio2-fault-runs`; `studio2/fase03/IMPLEMENTATION_STATUS.md`; `studio2/PROVENIENZA.md` §7–§8; commit docs `6851bb6` (= `923ded1`, vedi §8.5) |
| Modello e finestra | Claude (Cowork), modello configurato `claude-fable-5-1`, finestra distinta da quella di lavoro (Codex); nessuna chiamata a modelli linguistici; nessuna simulazione nuova |
| Metodo | `docs/prompts/Verifica_LLM.md` e `docs/MAINTENANCE.md` §1, §2, §8; ogni numero risalito al file o all'oggetto git, mai al report |
| Ambiente | shell Linux con il repository montato in sola lettura logica (`/Users/luker/fot-tep`); contenitore cloud separato per il riscaricamento dell'asset |
| File scritti | soltanto questo file. Residui temporanei creati e rimossi dalla verifica stessa: `studio2/fase03/fault_runs/tmp_ghpr82g/`, `tmpg9qn2wnd/` (directory vuote lasciate dai test unitari, che le creano sotto `fault_runs/`) e `.git/index.lock` (vuoto, lasciato da `git status`); `git status --short` vuoto a fine verifica |

Legenda: ✅ verificato sulla fonte primaria · ⚠️ plausibile ma non verificabile con ciò che ho · ❌ smentito.

---

## 1. Coerenza con il catalogo congelato — ✅

Fonte: `git show studio2-fase03-catalogo-D1-frozen-001:studio2/fase03/selection/CATALOG_FREEZE.json`
(tag annotato `b6828af` → commit `ab43f0b`).

| Riscontro | Comando / valore |
| --- | --- |
| Catalogo al tag | `"catalog": [1, 2, 3, 8, 10, 13, 14, 15]` |
| Hash del file al tag = hash a HEAD = hash nei 40 manifest (`dependency_hashes`) | `68b8461a6382c93e1a5dd8dc6c9def66b26b2ec865f0bc0786dd88fa95acedda` in tutti e tre |
| `git diff --quiet <tag> HEAD -- …/CATALOG_FREEZE.json` | identico; in `selection/` dal tag a HEAD solo 3 file **aggiunti** (`CATALOG_PUBLICATION.json`, `PUBBLICAZIONE_CATALOGO_D1.md`, `VERIFICA_CATALOGO_D1_APPENDICE_01.md`), nessuno modificato |
| `plans/fault_dev.csv` | 40 righe; conteggio IDV `{1:5, 2:5, 3:5, 8:5, 10:5, 13:5, 14:5, 15:5}`; nessun IDV fuori catalogo |
| `MANIFEST_FAULT_DEV.csv` e 40 `*.manifest.json` | stessi conteggi; `run_id` univoci `fault-dev-F<idv>-b0<b>`; IDV e indice di ogni manifest uguali alla riga del piano |
| Formula `30000 + 5·k + (b−1)` con `k` = posizione nel catalogo | verificata vera per tutte le 40 righe |

Nota: il `CATALOG_FREEZE.json` al tag porta `catalog_frozen: false` e stato
`reviewed_pending_commit_and_publication`: è la forma prevista dal suo stesso `amendment_policy`
(il manifest non si modifica dopo il tag); lo stato efficace è attestato da `CATALOG_PUBLICATION.json`
e dal tag, come già registrato in PROVENIENZA §6. Non è una discrepanza.

## 2. Invarianti di Fase 02, indici, onset, orizzonte, finestra di controllo — ✅

Fonte degli invarianti: `studio2/fase02/SPECIFICA_GENERAZIONE.md` §1 (Ts_base 0,0005 h, uscita 1/60 h,
Philox4×32-10, chiave `0x464f545445503032`, flusso = indice uint64, contatore = indice dell'estrazione,
bit `0x20` di MSFlag spento) e `validation/PRECALIBRATION_FREEZE.json` (`selected_burn_in_hours: 20`).

Sui 40 manifest per-run (script Python, un solo valore distinto per campo):

| Campo | Valore unico sui 40 |
| --- | --- |
| `ts_base_h` / `output_interval_h` / `msflag` | `0.0005` / `0.016666666666666666` / `0` |
| `rng_algorithm` / `rng_key_hex` / `counter_start` | `Philox4x32-10` / `0x464f545445503032` / `"0"` |
| `burn_in_h` / `onset_h` / `horizon_h` / `stop_time_h` / `window_h` | `20` / `25` / `40` / `65` / `5` |
| `stream_id == run_index_uint64`; `seed_descriptor == 0x464f545445503032:<stream hex 16>`; `stream_lo32/hi32` | veri per tutti |
| `model_overrides` | `sfunction_name temexd_fault_philox`, `sfunction_parameters "[] fot_stream_id 0"` (identici a quelli del `.mdl` base, righe 2830–2831), `fault_delay_h 25`, `maximum_delay_h 25`, `solver ode45`, `setpoints_changed false` |
| `pre_fault_window` | `{start 20, end 25, development_eligible false, complete true}` |
| `post_fault_windows` | 8 finestre `[25,30)…[60,65)`, tutte `development_eligible true`, `complete true` |
| `status` / `trip_time_h` / `actual_end_h` / `useful_windows_complete` / `data_rows` / `columns` | `complete` / `null` / `65.0` / `8` / `3901` / `54` |

Indici: i 40 `stream_id` sono esattamente `30000…30039` (insieme verificato). Censimento Fase 02 su
tutti i CSV/JSON sotto `studio2/fase02/` (campi `stream_id`, `run_index_uint64`, `run_index`):
usati `0–9, 100–109, 200–209, 1000–1009, 999999`; prenotazioni in
`studio2/fase02/build_generation_plan.py` righe 28–30: `2000–2099, 10000–10349, 20000–20149`.
Intersezione con `30000–30040`: **vuota**. Lo smoke usa `30040` (`smoke/f1_short_001/smoke-F1-001.manifest.json`).

Onset: nei 40 `*.simulation.log` c'è **una sola** riga `FOT_IDV` per run, con maschera
`1 << (idv−1)` (verificata contro l'IDV del manifest) e tempo uguale a `observed_onset_h`.
Minimo `25.00007946967903` (F2-b03), massimo `25.0005` (F8-b05): tutti in `(25, 25 + Ts_base]`.
Nei 40 `*.diagnostics.csv` la colonna `idv_mask` è `0` per tutti i campioni con `t < 25.0005` e
`1<<(idv−1)` per tutti quelli successivi; griglia `0, 1/60, …, 65` con 3901 righe, uguale alla
griglia dei 40 CSV grezzi (passo massimo in valore assoluto da `1/60`: < 1e-9). `65·60+1 = 3901` ✓.
La finestra `[20,25)` è marcata `development_eligible=false` in tutti i manifest e il report la
dichiara esclusa dallo sviluppo.

Hash di dipendenza: tutti i 20 `dependency_hashes` del manifest coincidono con i file a HEAD
(inclusi `temexd_philox.c` `230086e…`, `MultiLoop_mode1.mdl` `c588267…`, `PRECALIBRATION_FREEZE.json`,
`Mode1xInitial.mat`).

## 3. MEX strumentato: diff ricostruito e hash — ✅

Hash ricalcolati (`shasum -a 256`):

| File | SHA-256 | Atteso (MEX_RECORD §1, PRECALIBRATION_FREEZE) |
| --- | --- | --- |
| `studio2/fase02/simulator/source/temexd_philox.c` | `230086e7712e753bf48f3e9108cd0ce2f68aba97d9590ebb3c7593a47f8b6d25` | uguale (anche al freeze, 195 583 byte) |
| `fault_runs/runtime/source/temexd_fault_philox.c` | `74bf641bcd16ce42093b3c78cf03887376d19561041f8746ccf01339042fb4c9` | uguale |
| `studio2/fase02/simulator/build/temexd_philox.mexmaca64` | `6ae7e7be5394773f1854f1c53eddbd778ad7557b61fb05a93b3edb0552b1d11e` | uguale |
| `fault_runs/runtime/build/temexd_fault_philox.mexmaca64` | `834e2361915249402a1ec9074a4be04f22a6404deb841e5134bf34347dfde544` | uguale; identico a `mex_sha256` dei 40 manifest, dello smoke e di `BATCH_SUMMARY.json` |

`philox4x32.h` e `teprob_mod.h` copiati in `runtime/source/` sono byte-identici agli originali (`cmp`).

Diff ricostruito da me con `diff -u` (non copiato dal record): **5 hunk, 34 righe aggiunte pure +
1 riga sostituita** (`#define S_FUNCTION_NAME`), cioè 35 inserimenti / 1 cancellazione come dichiarato.
Contenuto, giudicato sul sorgente:

1. `#define S_FUNCTION_NAME temexd_fault_philox` — solo il nome della S-function.
2. Due campi **appesi in coda** a `struct stModelData` (`fot_diag_last_t`, `fot_last_idv_mask`).
   La struct è allocata con `calloc(1, sizeof(struct stModelData))` (riga 1261): nessun offset
   dei campi esistenti cambia.
3. In `mdlInitializeConditions`: inizializzazione dei soli due nuovi campi, prima di `setidv(S)`.
4. In `mdlOutputs`, **dopo** `tefunc(...)`: blocco sotto `ssIsMajorTimeStep(S)` che **legge**
   `dvec_.idv[0..27]`, `pv_.xmeasdist[0..8]` (array di 21), `teproc_.vcv[9..10]` (array di 12),
   `rx[47..48]` (NX = 50) e **scrive** soltanto i due nuovi campi e `mexPrintf`. Nessuna chiamata a
   `tefunc`, `tesub6_`, `fot_philox_uniform` o funzioni che toccano stato del modello; nessuna
   scrittura su `y[]`, `rx`, `dx`, `idv`. Le porte di uscita `y[0]`, `y[1]` sono assegnate dopo, dal
   codice originale inalterato.
5. Nel ramo di arresto (`idv[28] != 0`): una `mexPrintf("FOT_TRIP…")` prima di `ssSetStopRequested`.

Giudizio: il diff **non tocca equazioni, stato Philox, ordine delle estrazioni né XMEAS/XMV**; è
strumentazione a sola lettura più stampa. Riscontro incrociato: con `prepare_simulator.py` importato
come modulo, `instrument(base) == sorgente strumentato su disco` → `True`;
`strip_instrumentation(strumentato) == base` → `True`. I 21 test di `tests/test_fault_runs.py`
passano (`Ran 21 tests … OK`; prima esecuzione fallita solo perché la sandbox impediva la cancellazione
delle directory temporanee, vedi intestazione).

## 4. Equivalenza — ✅ sul confronto conservato, ⚠️ sul replay MATLAB

**Confronto rieseguito da me** su `runtime/mex_equivalence/`:

| Prova | Riscontro |
| --- | --- |
| Normal `burnin_qual-001` col MEX strumentato vs copia Fase 02 `validation/data_v2/burnin_qual/burnin_qual-001.xlsx` | contenitori 2 386 697 byte entrambi; SHA-256 `c3409d14…` (riferimento) vs `30bfe18f…` (rigenerato); stessi 7 membri ZIP nello stesso ordine; **7/7 membri byte-identici** (quindi intestazioni, valori IEEE-754 e stringhe identici per costruzione); 42 byte diversi nel contenitore, spiegati dai soli timestamp DOS (`2026-09-12 18:55:40` vs `2026-09-13 12:54:32`); `dimension A1:BB4202` = 54 colonne × 4201 righe dati |
| Contatore Philox | `matlab.log`: `counter_end=423367045`; `generation_manifest.csv` di Fase 02 per `burnin_qual-001`: `counter_end 423367045`, `mex_sha256 6ae7…`, `stream_id 0` |
| Quale MEX ha girato | il log contiene 4201 righe `FOT_DIAG`, che solo il MEX strumentato stampa ✅ |
| Fault F1/30000 col MEX base vs `runs/fault_dev_001/fault-dev-F1-b01.csv` | `cmp` → **byte-identici**; 3 817 751 byte; SHA-256 `acb4c4ec62c267f089c7fab2799e18d26cf39f657b78dbef28246ff347f5c62c` per entrambi; `counter_end=383902344` nel log = `counter_end` del manifest del run |
| Quale MEX ha girato | il log **non** contiene alcuna riga `FOT_` (coerente col MEX base, che non le stampa): prova per assenza, non per registrazione ⚠️ (vedi §8.2) |

**Replay di un run con il MEX strumentato in directory temporanea: non eseguito.** La finestra di
verifica dispone solo di una shell Linux sul volume montato; MATLAB R2025b risiede sul Mac e non è
invocabile da qui. Nessuna simulazione è stata lanciata. Il replay resta la condizione §9.1; ho
indicato lì procedura e criterio così che chiunque con MATLAB possa chiuderla in pochi minuti.

Osservazione sui log di lancio: `runtime/build_preflight.log` documenta un primo `mex` fallito sotto
Rosetta (`ARCH = maci64`), poi la build nativa ARM in `build_preflight_arm.log` (= `tests/BUILD_LOG.txt`,
`cmp` identici). Coerente con MEX_RECORD §3.

## 5. Conservazione — ✅

Riscaricamento eseguito in un contenitore separato, fuori dal repository e senza riuso della copia locale:

```
curl -L -o studio2-fase03-fault-dev-v1.tar \
  https://github.com/sorrentinoluca/fot-tep-data/releases/download/studio2-fase03-fault-dev-v1/studio2-fase03-fault-dev-v1.tar
# 208257536 byte
sha256sum → 6edd96711d2913953c6de81ce6dbb7c51e7677a2a7c1892b0676de5e7a9fd97c   (= ARTIFACT_STORAGE.json, REPORT §5, PROVENIENZA §8)
tar -xf … ; 240 file estratti, 47 directory
```

Confronto con `MANIFEST_CONSERVAZIONE.csv` (240 righe dati, colonne `path,bytes,sha256`):
**240/240 file** con percorso, byte e SHA-256 coincidenti; mismatch **0**; byte totali
**207 757 349** = `verification.bytes_verified` di `ARTIFACT_STORAGE.json`. Nessun file nel manifest
assente dall'archivio, nessun file nell'archivio assente dal manifest. Contenuto: 213 file sotto
`runs/fault_dev_001/` (5 per run × 40 = 200, + `events.jsonl` + `generation_manifest.csv` + 11 file
di cache Simulink), 2 sotto `runtime/batch_launch_failed_20260913T122247/` (`matlab.log` da 0 byte,
hash `e3b0c442…` della stringa vuota; `matlab.pid` = `94590`), 25 sotto `runtime/mex_equivalence/`
(12 in `fault_base_30000/`, 13 in `normal_instrumented/`).

Copia locale: gli stessi 240 file in `/Users/luker/fot-tep` hanno byte e hash identici al manifest
(240/240); il `.tar` locale in `runtime/` ha lo stesso SHA-256 dell'asset remoto.

`ARTIFACT_STORAGE.json`: `release_tag`, `repository`, `release_commit 6d238929285e57c6c70f4d563ef7e30b59da6ac5`,
`published_at_utc 2026-09-13T11:06:10Z`, `bytes 208257536`, `sha256 6edd…`, `manifest_rows 240`,
`mismatches 0`, stato `public_release_verified_by_redownload`: tutti coerenti con quanto misurato.
Pagina della release letta direttamente: tag `studio2-fase03-fault-dev-v1`, commit
`6d238929285e57c6c70f4d563ef7e30b59da6ac5`, pubblicata il 13 settembre alle 11:06, descrizione con lo
stesso SHA-256. ⚠️ `release_id 387872892` non verificato (API GitHub non raggiungibile da questa
finestra): non incide su recuperabilità o integrità.

Nota: nell'archivio i percorsi sono relativi a `studio2/fase03/fault_runs/` (`runs/…`, `runtime/…`),
mentre il manifest li scrive dalla radice del repository; il prefisso va dedotto (§8.4).

## 6. Tracciabilità — ✅ con note

| Riscontro | Evidenza |
| --- | --- |
| Specifica originale invariata | `SPECIFICA_RUN_FAULT.md`: un solo commit nella storia (`git log --follow` → `c02111d`, 11:56 CEST); SHA-256 `14d36742…` a `c02111d`, a `49d5806` e a HEAD; identico a `spec_sha256` dei 40 manifest e dello smoke |
| rev002 tracciata | `SPECIFICA_RUN_FAULT_rev002.md`, commit `49f1229`; `diff` con l'originale = solo 4 blocchi aggiunti (intestazione con riferimento esplicito a `SPECIFICA_RUN_FAULT.md` e commit `c02111d`, identità del MEX strumentato, criterio MEX della revisione 2) e il titolo; nessuna riga dell'originale rimossa. La parola «supersedes» non compare ma la relazione è dichiarata in modo equivalente («La revisione pre-esecuzione originale resta intatta in …») |
| Codice eseguito = codice committato | hash a `49d5806` (commit registrato nei manifest) = hash a HEAD = hash nei manifest per `generate_fault_runs.m` `4e162d9e…`, `fault_protocol.py` `dd04ae52…`, `build_generation_plan.py` `d98eba73…`, `prepare_simulator.py` `3c18315d…`, `compile_fault_philox.m` `5fcc1f3b…`, `plans/fault_dev.csv` `583f4316…` |
| Artefatti congelati | `git diff --name-only origin/main HEAD -- phase_b icl ablation tep_*_v2 reproducibility papers/archive studio2/fase02` → vuoto; `merge-base origin/main HEAD = 9ec8779`; 8 commit sul branch; fuori da `studio2/fase03` cambiano solo `DOCUMENTATION_INDEX.md` (+1 riga), `docs/MAINTENANCE.md` (+6/−1), `docs/prompts/Commit_LLM.md` (+2), `studio2/PROVENIENZA.md` (+91); nessuna coppia MD/HTML toccata; tag `studio2-fase03-*` identici fra locale e `origin` |
| `MultiLoop_mode1.mdl` non salvato | `model_sha256 c588267…` uguale al file base a HEAD; gli override (delay 25/25, nome S-function) sono solo in memoria e registrati in `model_overrides` |
| PROVENIENZA §7–§8 | origine, commit (`c02111d`, `49d5806`, `6d238929…`), impronte (piano `583f4316…`, specifica `14d36742…`, manifest `9eaed0e9…`, sorgenti `230086e…`/`74bf641b…`, binario `834e…`, archivio `6edd…`), release, marche **pre-specificato** / «documentazione post-esecuzione» / «equivalenza verificata post-esecuzione», esposizione incidentale alla tabella narrativa della v2 dichiarata con la clausola «senza rivendicare cecità assoluta» — tutti presenti e coincidenti con gli artefatti |
| Commit separati e messaggi | `c02111d`, `55d442b`, `88eb34e`, `49d5806`, `fe771e5`, `49f1229`, `3b9ec1e` nel formato `studio2(<ambito>): <azione>`; ciascuno con perimetro omogeneo (specifica+provenienze / codice / test / smoke+consegna / manifest batch / conservazione+MEX / chiusura). Eccezione: `6851bb6 docs: Fix artifact publication/verif convention` (§8.5) |
| Tentativo di lancio abortito | REPORT §3, `BATCH_SUMMARY.json.failed_launch_attempts_recoverable` (pid `94590`, log vuoto), PROVENIENZA §8 ultimo paragrafo, directory conservata nell'archivio (2 file). Cronologia coerente: commit `49d5806` 12:16 CEST → tentativo 12:18:43 CEST (mtime dei file) → rinomina `…T122247` → `campaign_start 10:23:12.922Z` (12:23 CEST) → `FAULT_CAMPAIGN_COMPLETE 10:28:46Z`; `events.jsonl` 82 righe (1+40+40+1), timestamp monotòni |
| Batch: numeri del report | `MANIFEST_FAULT_DEV.csv` SHA-256 `9eaed0e9…` ✓; `generation_manifest.csv` `69a7f2f9…` ✓; 200 hash (manifest, output, diagnostiche, log, attempt × 40) ricalcolati ✓; somma `runtime_seconds` = **330,764 s** ✓ (simulazione pura 323,231 s); `generation_manifest.csv` coerente campo per campo (53 campi scalari) con i 40 manifest JSON |
| `docs/test_explanation.py` | `Ran 35 tests … FAILED (failures=14, skipped=1)`: 14 come la base dichiarata in MAINTENANCE §5, nessun peggioramento |

## 7. Perimetro del report — ✅

`REPORT_RUN_FAULT.md` letto per intero. Contiene solo: disegno eseguito, contatori tecnici (40/40,
0 trip, 320/320 finestre, onset, hash), il tentativo abortito, l'identità del MEX e le due prove di
equivalenza, la conservazione, l'elenco di ciò che la sotto-fase **non** produce e le dipendenze
aperte. Le uniche occorrenze di «segnale», «diagnostic*», «feature», «evidence», «insight», «score»
sono nella regola preregistrata su F14/F15 («segnale debole o assente non autorizza sostituzioni»),
nel riferimento alle *diagnostiche* strumentali del MEX e nella lista negativa §6. Nessun valore,
confronto, separabilità, trend o commento per-fault sui 40 run. Lo stesso vale per
`smoke/REPORT_SMOKE.md` (il controllo della composizione interna è il check di attivazione prescritto
dalla specifica §7, con tolleranza `1e-10`, e il report stesso nega che sia «un risultato di
separabilità»), `HANDOFF_BATCH.md`, `MEX_RECORD.md`, `IMPLEMENTATION_STATUS.md` e PROVENIENZA §8.

---

## 8. Discrepanze e osservazioni (nessuna bloccante)

1. **⚠️ Sorgente strumentato e binario non conservati.** `runtime/` è in `.gitignore` e i file
   `runtime/source/temexd_fault_philox.c` (+ i due header) e `runtime/build/temexd_fault_philox.mexmaca64`
   **non sono né in Git né nell'archivio** `studio2-fase03-fault-dev-v1.tar` (verificato: 11 file locali
   sotto `runtime/` assenti dal manifest di conservazione). Il sorgente è riproducibile byte per byte
   da `prepare_simulator.py` + sorgente base congelato (riprodotto in questa verifica) e il diff è nel
   record; il **binario** `834e…`, citato in tutti i 40 manifest, esiste solo sul disco dell'autore.
   È la stessa convenzione della Fase 02 (`PRECALIBRATION_FREEZE.local_mex.tracked=false`,
   «rebuild_required_on_other_platforms»; il manifest di conservazione di Fase 02 non contiene MEX),
   ma MAINTENANCE §8.5 ricorda che «gli hash da soli non bastano».
2. **⚠️ Prove di equivalenza senza script né manifest.** In `runtime/mex_equivalence/` ci sono output,
   `simulation.mat`, cache e `matlab.log`, ma non lo script MATLAB che ha prodotto le due rigenerazioni
   né un manifest con `mex_sha256` del binario usato. L'uso del MEX strumentato nel Normal è provato
   dalle 4201 righe `FOT_DIAG`; l'uso del MEX base per F1/30000 è dedotto dall'**assenza** di righe
   `FOT_`. La prova è convincente ma non autocontenuta. (`matlab_attempt1.log` documenta un primo
   tentativo fallito dello script con `Error using +`, poi corretto: anche questo senza script.)
3. **⚠️ Log del lancio riuscito non conservato.** `runtime/batch_launch/matlab.log` (40 run,
   `FAULT_CAMPAIGN_COMPLETE`, esito `accepted: true` dell'audit) e `matlab.pid` (`95187`) non sono né
   in Git né nell'archivio, mentre il tentativo fallito lo è. L'informazione è ridondante con
   `events.jsonl` e i 40 `*.simulation.log` conservati, ma l'asimmetria è da sanare al prossimo lotto.
   Stessa sorte per `runtime/build_preflight.log`, `build_preflight_arm.log`, `matlab_preflight.log`,
   `tests_initial.log` (gli ultimi tre hanno però copie committate identiche in `tests/`).
4. **⚠️ Prefisso dei percorsi.** `MANIFEST_CONSERVAZIONE.csv` usa percorsi dalla radice del repository
   (`studio2/fase03/fault_runs/…`), l'archivio usa percorsi relativi a `fault_runs/` (`runs/…`,
   `runtime/…`); `ARTIFACT_STORAGE.json` non dichiara la radice dell'archivio. Il verificatore deve
   dedurre il prefisso. Il manifest di Fase 02 ha inoltre uno schema diverso
   (`source_path,…,destination_sha256`): due formati per lo stesso ruolo.
5. **⚠️ Commit docs `923ded1` vs `6851bb6`.** Il commit citato nella richiesta, `923ded1`, **non è
   raggiungibile da alcun branch** (genitore `32acaf2`): sul branch la stessa patch è `6851bb6`
   (`git patch-id` identico `6bd51660…`, stesso autore, stessa data 12:41 CEST, genitore `fe771e5`).
   La documentazione deve citare `6851bb6`. Il messaggio `docs: Fix artifact publication/verif
   convention` non segue il formato `studio2(<ambito>): <azione>` di MAINTENANCE §8.3 ed è in
   inglese; tocca solo `docs/MAINTENANCE.md` §8.5 e `docs/prompts/Commit_LLM.md` §7, aggiungendo la
   convenzione di pubblicazione su `fot-tep-data` e l'obbligo di verifica per riscaricamento.
   Il contenuto è corretto e la sotto-fase vi si conforma.
6. **⚠️ Formato del tag di release.** MAINTENANCE §8.5 (dopo `6851bb6`) prescrive
   `studio2-fase<N>-v<k>` «per fase o lotto»; il tag effettivo `studio2-fase03-fault-dev-v1` inserisce
   il nome del lotto. Scelta ragionevole (la fase avrà più lotti), ma il formato scritto non la
   prevede letteralmente: va esplicitato il formato per lotto in MAINTENANCE, oppure accettata come
   eccezione dichiarata.
7. Osservazione, non discrepanza: `REPORT_RUN_FAULT.md` è stato committato una prima volta
   **prima** del batch (`49d5806`, 169 righe, commit registrato come `git_commit` nei manifest) e
   riscritto in luogo a `3b9ec1e`. È un report, non un artefatto congelato, quindi ammesso; chi
   legge i manifest deve sapere che il report a `49d5806` descrive la consegna pre-batch.
8. Osservazione: MEX_RECORD §3 afferma «Il log non registra un'identità più specifica dell'esecutore»
   e il `.mexmaca64` è compilato su Apple Silicon; su altre piattaforme il binario va ricompilato e
   il suo hash differirà per costruzione. Il criterio della rev002 (hash = `834e…`) vale quindi per
   **questa** campagna, non come criterio portabile: la portabilità è garantita dal sorgente e dalle
   prove di equivalenza, non dall'hash binario.

## 9. Condizioni di efficacia

1. **Replay con MATLAB** (punto 4, parte non eseguita). Chi dispone di MATLAB R2025b su Apple
   Silicon esegua **un** run a scelta fra i 40 con `runtime/build/temexd_fault_philox.mexmaca64`
   (SHA-256 `834e…`) in una directory temporanea fuori dal repository — ad esempio copiando
   `generate_fault_runs.m` e un piano di una sola riga presa da `plans/fault_dev.csv`, oppure
   rimuovendo temporaneamente il vincolo di destinazione nel solo copione temporaneo — e confronti
   con `runs/fault_dev_001/`: CSV grezzo byte-identico (stesso SHA-256 del manifest), `diagnostics.csv`
   byte-identico, `counter_end` uguale, una sola riga `FOT_IDV` con lo stesso tempo. Con il rilancio
   della campagna già rieseguito due volte (smoke `30040` e replica F1/30000 col MEX base identica), la
   probabilità di una sorpresa è bassa; ma la consegna chiede questa prova e non è stata fatta.
   Va annotato l'esito in un'appendice a questo file, non modificando quanto sopra.
2. **Conservare sorgente strumentato e binario** (§8.1) — come minimo `temexd_fault_philox.c`,
   i due header e `temexd_fault_philox.mexmaca64` con i loro SHA-256 — in un asset della stessa
   release o del prossimo lotto su `fot-tep-data`, aggiornando `MANIFEST_CONSERVAZIONE.csv` e
   `ARTIFACT_STORAGE.json` come **nuova revisione**, senza riscrivere l'asset `6edd…` già verificato.
   Nella stessa occasione conservare `runtime/batch_launch/matlab.log` e `matlab.pid` (§8.3) e,
   se recuperabile, lo script delle due prove di equivalenza (§8.2).
3. **Correggere i riferimenti al commit docs**: `6851bb6`, non `923ded1`, ovunque la documentazione
   di chiusura lo citi (§8.5).
4. **Dichiarare la radice dell'archivio** in `ARTIFACT_STORAGE.json` (`archive_root:
   studio2/fase03/fault_runs/`) o allineare i percorsi del manifest a quelli interni del `.tar`, nella
   revisione di cui al punto 2 (§8.4). Valutare un formato unico di `MANIFEST_CONSERVAZIONE.csv` per
   le fasi future.
5. **Formato del tag di lotto** (§8.6): esplicitarlo in MAINTENANCE §8.5 o registrare l'eccezione.
6. Restano fuori da questa verifica, come dichiarato dal report stesso: integrazione in `main`
   (solo su richiesta), estrazione di feature/evidence, insight, prototipi, capienza e gate LLM.

Le condizioni 2–5 sono correzioni documentali o di conservazione e non richiedono di toccare run,
manifest, piano, specifica originale o artefatti congelati. La condizione 1 è l'unica prova
sperimentale mancante e, se fallisse, riaprirebbe il punto 4 e con esso il verdetto.

---

## Appendice A — Replay MATLAB di F1/30000 col MEX strumentato (condizione §9.1) — ✅

Aggiunta il 2026-09-13, stessa finestra di verifica, dopo che l'autore ha eseguito il replay. Il
testo delle sezioni 1–9 è rimasto invariato; questa appendice registra la prova mancante.

Il riepilogo dell'autore **non è stato preso per buono**: ogni voce è stata ricontrollata sui file in
`studio2/fase03/fault_runs/runtime/mex_equivalence/fault_instrumented_30000_replay/` (5 file fuori
dalla cache, scritti alle 13:02–13:03 CEST).

| Riscontro | Comando / valore |
| --- | --- |
| CSV grezzo vs `runs/fault_dev_001/fault-dev-F1-b01.csv` | `cmp` → **byte-identici**; 3 817 751 byte; SHA-256 `acb4c4ec62c267f089c7fab2799e18d26cf39f657b78dbef28246ff347f5c62c` per entrambi (= `sha256` del manifest del run) |
| Quale MEX ha girato | `fault-dev-F1-b01.simulation.log` del replay contiene **3901 righe `FOT_DIAG` + 1 riga `FOT_IDV`**: stampe che esistono solo nel MEX strumentato `834e…` (§3). `matlab.log` riporta `mex_sha256_expected=834e2361…`, `counter_end=383902344`, `rows=3901 columns=54` |
| Diagnostiche | `diff` fra le 3902 righe `FOT_*` del log di replay e quelle del log originale della campagna → **nessuna differenza**: tempi, maschera IDV, composizioni/temperature/fattori cinetici interni e comandi/posizioni valvola identici campione per campione. Il log completo differisce dall'originale per **una sola riga** in più nell'originale: la traccia con link ipertestuale `In generate_fault_runs (line 95)` emessa dal launcher della campagna, assente perché il replay non usa quel launcher |
| Transizione IDV | unica: `FOT_IDV,25.000499999999999,1` (= `observed_onset_h 25.0005`, IDV(1)); nessuna riga `FOT_TRIP` |
| Contatore Philox | `383902344` nel `matlab.log` = `counter_end` del manifest = valore della prova col MEX base (§4) |
| Primo tentativo | `matlab_attempt1.log`: `Error using fopen — Invalid permission`; simulazione completata ma nessun output scritto; nessun file parziale promosso. Il rilancio ha usato la creazione esclusiva (`java.io.File.createNewFile`) del generatore originale |
| Perimetro | `git status --short` → solo `?? studio2/fase03/fault_runs/VERIFICA_RUN_FAULT.md`; HEAD ancora `3b9ec1e`; `runs/fault_dev_001/`, manifest, archivio `6edd…` e release non toccati (il replay sta in `runtime/`, ignorato da Git e **non** incluso nell'asset pubblicato) |

Esito: **il MEX strumentato `834e…` riproduce il run della campagna F1/30000 byte per byte, con le
stesse diagnostiche e lo stesso contatore Philox**. Con la prova §4.2 (MEX base → stesso CSV) il
triangolo è chiuso: campagna, MEX base e MEX strumentato coincidono sullo stesso stream.
La condizione §9.1 è soddisfatta e il verdetto **OK** resta senza riserve sperimentali.

Restano valide le condizioni documentali §9.2–§9.5, con due aggiunte: lo script MATLAB del replay
non è conservato accanto ai suoi output (stesso punto di §8.2, da sanare insieme); e la directory
del replay, come il resto di `runtime/mex_equivalence/` nuovo, andrà inclusa nella prossima
revisione di `MANIFEST_CONSERVAZIONE.csv`/`ARTIFACT_STORAGE.json` e nel relativo asset, senza
riscrivere l'asset già verificato.
