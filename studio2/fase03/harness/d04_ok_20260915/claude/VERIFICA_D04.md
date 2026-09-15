OK — candidato tecnico `aae29a908356e4a4842a214fdc3db9bff26ec3ca`, tree `4e1f7f043725d64fb16b7d1c921c619bce8d1bb3`. Il difetto D04 (validazione del `quota_kind` di retry spostata al **momento della decisione** di riserva/invio, non solo in chiusura) risulta corretto; D03 resta invariato; il perimetro è circoscritto a `ledger.py` (+18/−3). Nessun difetto riscontrato. Questa volta le suite complete sono state **eseguite**, non solo ispezionate. Nessun freeze, nessun GO.

# Verbale autonomo D04 — 15 settembre 2026

## Indipendenza, modello, finestra

Verifica in finestra distinta dalla preparazione. Preparatrice: `gpt-6-astra/xhigh`. Review D03 precedenti: Claude (`bc3ee96…`, nucleo D03) e Codex `gpt-6-astra/high` (apre D04). Questa verifica: sessione configurata **`claude-opus-4-8`** (famiglia Claude; modello servito non dimostrabile dall'interno). Come il report D04 riconosce correttamente, la diversità di famiglia **non** dimostra di per sé l'assenza di difetti: la validazione qui è indipendente dal modello (differenziale rosso/verde + sonda propria + esecuzione delle suite).

- Runtime prove: **Python 3.10.12 / SQLite 3.37.2** in VM Linux (preparatrice: 3.13.9 / 3.51.0 su macOS).
- Sola lettura sul candidato. Sandbox e cloni in scratch sacrificabile; nessuna scrittura in sorgenti, review o worktree. Nessun commit/tag/push/merge/freeze/GO.

## Identità e stato Git

| Oggetto | Verifica |
| --- | --- |
| Candidato tecnico | `aae29a9…` — commit presente; `aae29a9^{tree}` = `4e1f7f04…` **coincide** ✅ |
| Base documentale | `97868f9…` "consegna il candidato D03 alla verifica indipendente" ✅ |
| Acquisizione | `f0dca4d2…` "acquisisce le due review D03 e il rilievo D04" ✅ |
| Contratto/test-first | `bf7774f2…` "fissa il contratto D04 e le prove rosse prima del runtime" ✅ |
| Cronologia | base → acquisizione → **test-first** → **runtime**: il test-first precede la modifica runtime ✅ |
| Successore documentale | `feaf1d3c…` aggiunge **solo 4 file** (CONSEGNA_D04.json, DELIVERY_AUDIT_D04.json, PROMPT_VERIFICA_D04.md, REPORT_CORREZIONE_D04.md); HEAD distinto dal tecnico ✅ |
| Branch | `codex/studio2-harness-0310-d04` ✅ |
| Main su GitHub reale | `git ls-remote https://github.com/sorrentinoluca/fot-phd.git refs/heads/main` → `a00605862f627710347bd63c49f79a6d0a00135f` **coincide** ✅ |
| Runtime cambiato | **solo `ledger.py`**, delta **+18 / −3** ✅; nulla cambia fuori da `studio2/fase03/harness/` ✅ |

Stato finale: repository e sorgenti invariati. Le prove girano in sandbox `git archive`/clone `--shared` nello scratch della VM (fuori dalle cartelle montate). Il verbale Claude D03 resta untracked e integro nel source D03.

## Integrità

| Oggetto | Verifica |
| --- | --- |
| Manifest tecnico | 24151 byte, SHA-256 `9fbad8c036075605a9bbdfdac84078259428b679fc33341ed98f21050a07efd6`, **98 membri**, artifact_version 7 — coincide ✅ |
| Campione 6 membri manifest | sha dichiarato == blob git (PREFLIGHT_03_0, pilot_preflight, CONTRATTO_D03/D04_PRIMA_DEL_CODICE, CONTRATTO_ESECUZIONE_E_RIPRESA, D04_DECISION_CONTRACT) ✅ |
| Verbale Claude D03 acquisito | `bc3ee96afb2bd890d0b326ca4965d03c46d241f288a30c5ee1455a0c8ec9a47f` ✅ |
| Verbale Codex D03 acquisito | `21e457af023a9a8fae3560f663784c55788408942f8c9e902b3d468764aceef9` ✅ |
| Manifest Codex (SHA256SUMS) | `9334c9c57b159cf14f047d28646544615c99aaf751298753e573f893dbbb86a1` ✅ |
| Riferimento evidence 03.6 | `EVIDENCE_MANIFEST.csv` = `5111d0c6…` == `EVIDENCE_MANIFEST_SHA256` del codice ✅ |
| Legacy `0c8157f` | clone self-contained: HEAD `0c8157f…`, tree `a1573b49…`, stato pulito ✅ |

## Invariante D04 — analisi del codice

Il difetto: su `23859a2` `_validate_attempts` validava `quota_kind` contro il ruolo solo in **chiusura/riconferma**; il binding dello stadio aperto ricontrollava solo le prove zero-token e la **nuova riserva** contava `quota_kind` senza quella validazione. Barriera nel punto sbagliato rispetto alla decisione.

La correzione (verificata sul sorgente):

- ✅ Nuovo `_validated_attempt_inventory(c)`: itera **tutti** gli stadi presenti in `requests`, rifiuta stadi ignoti (`stage not in STAGES`) e, per ciascuno, riesegue l'**intero** `_validate_attempts` contro il piano immutabile (identità, ruolo base/remediation/retry, catena `retry_of`, e — per righe `ZERO_TOKEN_PROVEN` — la riconciliazione D03). Ammette copertura parziale/stadi aperti: non impone outcome né completezza (quello resta in `_validate_outcome`, in chiusura).
- ✅ `_validate_attempts` è **byte-identico** alla versione già verificata in D03: la correzione riusa logica provata, cambiando solo **quando** scatta.
- ✅ Cablato in **tre punti di decisione** nella stessa transazione: binding ripreso (sostituisce la vecchia lista parziale che guardava solo lo zero-token), nuovo binding (dopo `_ready`), e **nuova riserva** (dopo hard-stop e `_ready`, prima dell'inserimento).
- ✅ **Precedenza diagnostica**: le guardie strutturali economiche (hard stop 200, `_ready`/prerequisito alternate) restano **prima** dell'inventario, così i due metodi diagnostici storici conservano la diagnosi attesa; l'inventario resta obbligatorio prima di ogni decisione positiva. Il report lo dichiara come iterazione intermedia (`pre_diagnostic_precedence`).
- ✅ D03 preservato: tre percorsi, 11 controlli, digest ricalcolabili, legame durevole, file letti una volta, no-backfill. Lo snapshot resta diagnostico e non autorizza richieste.

## Riproduzioni (eseguite)

### Test-contratto D04 differenziale
`test_d04_open_quota.py` (byte-identico su test-first `bf7774f2`, candidato e sandbox; ledger a test-first == `23859a2`), stesso file su entrambi i target via `FOT_HARNESS_TARGET`:

- **RED (23859a2)**: `Ran 8 tests … FAILED (failures=240)`, **0 errori**. Le 240 assertion cadono in **6 metodi** (`eighth_retry_and_new_fault`, `generated_quota_matrix` [216], `probe_triplet`, `role_dependencies` [14], `runner_and_CLI`, `shared_attempt_validation`); i 2 metodi positivi/guardia passano. Coincide con "8 metodi/240 assertion in 6 metodi/0 errori". ✅
- **GREEN (candidato)**: **8/8 OK**, zero failure, zero errori. ✅

### Sonda indipendente (mia, senza dipendenze esterne)
Stadio aperto con retry transport; `quota_kind` alterato `transport→base`; poi due decisioni (nuova riserva base = "nuovo invio"; nuovo retry transport = "ottavo"):

| Caso | Candidato `aae29a9` | Respinto `23859a2` |
| --- | --- | --- |
| catena **non** manomessa | nuova riserva + retry **ACCETTATI** (positivo preservato) | ACCETTATI |
| quota `transport→base` | **entrambi RIFIUTATI**, DB invariato ✅ | **entrambi ACCETTATI** (D04 riprodotto) |

Conferma indipendente e model-diverse: D04 reale su `23859a2`, chiuso su `aae29a9` a livello di **decisione** (riserva e retry), senza falsi rifiuti sul percorso legittimo.

## Suite (eseguite in questo ambiente)

Con `FOT_HARNESS_TEST_EVIDENCE` (riferimento 03.6 montato) e `FOT_HARNESS_LEGACY_CANDIDATE` (clone `0c8157f` self-contenuto) le suite runner, **bloccate in D03**, girano.

| Suite | Esito |
| --- | --- |
| `test_harness_offline`, `test_metric_raccordo`, `test_execution_guard`, `test_protocol`, `test_d02` (8), `test_d03` (8), `test_d04` (8) | **70/70** nel blocco, **0 failure**, 1 solo errore (sotto) |
| `test_revisions` | **37/37 OK** |
| `test_c01_c03` (C01/C02/C03, morte-processo/lock reali) | **14/14 OK** |
| `test_d01_replay` | **7/7 OK** (con legacy self-contenuto) |
| **Totale mirati** | **128** raccolti = risultato dichiarato; **127 verdi + 1 solo env-bloccato** |
| Compilazione live | **103** moduli compilati, **0 errori** (superset dei 94 "live" dichiarati) |
| Perimetro | unico runtime = `ledger.py`; **nulla** cambia fuori dall'harness; i 12 moduli scientifici sono **byte-identici** base↔candidato ✅ |

Unico non-verde: `test_D03_real_legacy_proofs_rejected_without_rewriting_history` — riga hard-coded `/Users/luker/…/0c8157f/candidate` (non parametrizzata via env) irrisolvibile nella VM. È un **limite d'ambiente**, non un difetto; il suo intento (rifiuto legacy senza digest/no-backfill) l'ho già verificato indipendentemente nella review D03, e il percorso di codice legacy `0c8157f` è comunque esercitato da `test_d01_replay` (verde).

**Discovery (163):** la porzione harness (rilevante per D04) è integralmente verde come sopra. I 12 moduli scientifici/di piano restanti (baseline_numerica, evidence, fault_runs, pseudolabel, schema_insight/validator, selection, soglie_normal) — 81 test — sono **byte-identici tra base e candidato** e tra respinto e corretto, quindi **non possono essere influenzati** dalla modifica di `ledger.py`; nella VM richiedono `scipy`/`pytest`/stack scientifico non installati. Non ne ho forzato l'esecuzione: sono fuori perimetro D04 e la loro identità byte lo dimostra. Non converto questo limite in PASS.

## Matrice dei 50 metodi

La matrice nominativa dei 50 metodi (N48≡C02, adattamenti dichiarati) è acquisita byte-identica; **non 50/50 letterali**, suite/sottocasi non si sommano. Ho rieseguito in modo probante: nucleo D04 (differenziale 8v/8 + 240-fail; sonda propria), l'intera batteria mirata harness (D01 7, D02 8, D03 8/9, D04 8, C01–C03 14, revisions 37, offline 20, metric 9, exec_guard/protocol). Le voci V/W/Y/Z/X e "applicabili" sono coperte, per il codice, dal differenziale e dalle suite harness sopra; i loro **launcher** dedicati (con copie byte-identiche e reference storiche) non li ho rilanciati uno per uno in questo ambiente — restano ⚠️ come esecuzione dei singoli launcher, non come esito del codice.

## Confini e limiti d'ambiente

- **1 test env-bloccato** (percorso `/Users/…` hard-coded in `test_d03_contract`), intento verificato altrove.
- **Moduli scientifici discovery**: env-dipendenti (scipy/pytest) ma **provati irrilevanti** per D04 (byte-identici, `ledger.py`-indipendenti).
- **Guardiano documentale** (`docs/test_explanation.py`): non eseguito (albero `docs/` fuori dal sandbox harness); dichiarato **NON PASS non bloccante**, stessi 14 identificativi, 1 skip — non motivo di NON OK tecnico.
- Runtime VM 3.10.12/SQLite 3.37.2 ≠ macOS 3.13.9/3.51.0 della preparazione; i risultati del nucleo sono robusti rispetto alla differenza.
- Modello servito non dimostrabile dall'interno; dichiaro la famiglia (Claude).

Confini invariati e verificati: solo `ledger.py` runtime; D01/D02/D03, gate_rules, metriche qualificate, producer/consumer, digest/no-backfill D03 intatti. D9 approvata (122B principale/consumer, 27B alternativo, Terra storico interno) resta separata: recepimento eseguibile D9, ordine label, qualificazioni, T5 e pilot fuori perimetro; preflight storico bloccato. **Nessun push/merge/tag/freeze/GO.** 03.10 e Fase 03 restano aperte.

## Conclusione

**OK sul candidato tecnico esatto `aae29a9`.** Il difetto D04 è corretto in modo dimostrato e indipendente: il controllo di `quota_kind` è ora applicato al momento della decisione di riserva/invio su tutti gli stadi contribuenti (differenziale rosso/verde 8-vs-240 e sonda propria che rifiuta sia il nuovo invio sia l'ottavo retry con quota manomessa, DB invariato, positivi preservati). D03 resta invariato, il perimetro è circoscritto a `ledger.py` (+18/−3) e le suite mirate harness sono verdi (128 raccolti; unico non-verde un test con percorso hard-coded, limite d'ambiente). **Non ho riscontrato alcun difetto.** Restano ⚠️, come limiti d'ambiente e non come problemi del candidato, l'esecuzione dei singoli launcher V/W/Y/Z/X, dei moduli scientifici della discovery (irrilevanti per D04) e del guardiano documentale: da rieseguire sull'ambiente di riferimento macOS prima della chiusura formale. Nessun freeze o GO.

---
*Verifica indipendente in sola lettura. SHA-256 di questo verbale comunicato separatamente, senza autoreferenza.*
