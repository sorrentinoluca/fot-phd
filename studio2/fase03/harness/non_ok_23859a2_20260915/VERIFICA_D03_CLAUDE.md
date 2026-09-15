OK (perimetro D03) — candidato tecnico 23859a29225ccd9cd6f47e4a0b6e36258831dbab, tree fe66025f4925e27676b0be16428475e3fcaee060. Il difetto D03 risulta corretto e l'invariante delle prove zero-token regge; nessun difetto riscontrato. Riserve ⚠️ dichiarate su conteggi e suite non eseguibili in questo ambiente (percorsi assoluti macOS e artefatti di riferimento non raggiungibili dalla VM cloud), non per problemi del candidato. Nessun freeze, nessun GO.

# Verbale autonomo D03 — 15 settembre 2026

## Nota di indipendenza e modello

Questa verifica è svolta in una finestra distinta **e da una famiglia di modello diversa** da quella di preparazione e delle review precedenti. Preparatore e revisori D01/D02: `gpt-6-astra` (xhigh/high). Questa verifica: sessione configurata `claude-opus-4-8` (famiglia Claude); il modello effettivamente servito non è dimostrabile dall'interno, ma la famiglia è diversa da gpt-6-astra. È la prima volta nel ciclo 03.10 che il criterio di diversità di modello di `Verifica_LLM.md` risulta soddisfatto. Come richiesto dal mandato, **non rivendico** che il cambio di modello elimini i difetti: verifico il presidio di contratto in modo indipendente dal modello.

- Finestra: sessione Cowork cloud (remota), sola lettura sul candidato.
- Runtime prove: **Python 3.10.12 / SQLite 3.37.2** in VM Linux (il preparatore usava 3.13.9 / 3.51.0 su macOS — vedi Limiti).
- Nessuna delega. Nessuna modifica al candidato, al repository principale, alle review o alle prove precedenti. Nessun commit/tag/push/merge/freeze/GO.

## Identità e stato Git

| Oggetto | Verifica |
| --- | --- |
| Candidato tecnico | `23859a29225ccd9cd6f47e4a0b6e36258831dbab` — presente nell'object store condiviso ✅ |
| Tree tecnico | `fe66025f4925e27676b0be16428475e3fcaee060` — coincide col `23859a2^{tree}` ✅ |
| Parent (contratti + prove rosse prima del runtime) | `567881abf06572812c00ccc0ed817d169b68fee6` ✅ |
| Acquisizione NON OK a219bd4 + mandato | `efa9f6f94194985104047d831c0b087dc460532d` ✅ |
| Base documentale | `e9b60c5db77edfd3c06a29857e6ba5f61ebe139a` ✅ |
| Successore documentale (solo 4 file di consegna) | `97868f9…` = CONSEGNA_D03.json, DELIVERY_AUDIT_D03.json, PROMPT_VERIFICA_D03.md, REPORT_CORREZIONE_D03.md ✅ |
| Main remoto effettivo | `git ls-remote …/fot-phd.git refs/heads/main` → `a00605862f627710347bd63c49f79a6d0a00135f` ✅ (coincide con l'atteso) |
| Cronologia | catena lineare acquisizione → **contratto/test-first (567881a)** → **runtime (23859a2)** → consegna. Il test-first **precede** il runtime ✅ |

Stato Git finale: repository principale e sorgenti invariati. Il lavoro di verifica è avvenuto in sandbox sacrificabili nello scratch della VM (`$HOME/d03chk`, fuori dalle cartelle montate) tramite `git archive` dei commit esatti; nessuna scrittura in `studio2/…`, nel candidato o nelle evidence. Confronto blob→sandbox: `ledger.py` estratto == blob (`23859a2` = `2dd9509…`; `a219bd4` = `872a47c…`).

## Integrità

| Oggetto | Verifica |
| --- | --- |
| Manifest tecnico | 20826 byte, SHA-256 `483c7db5ad4a763a8f41d084538c7a2cce6b2a7d799a5ba11d57da852cee3828`, **83 membri** — coincide con l'atteso ✅ |
| Campione membri manifest (6) | sha dichiarato == blob git (PREFLIGHT_03_0, pilot_preflight, CONTRATTO_D03_PRIMA_DEL_CODICE, CONTRATTO_ESECUZIONE_E_RIPRESA, DECISIONE_D9…, DURABLE_FIELD_CONTRACT) ✅ |
| Verbale precedente D02 (che apre D03) | SHA-256 `b88f046592ac9d1b0f784c1d127f83ea3cc609c93bd547bbc91c7541cfd0223f` — **verificato su disco** ✅ |
| SHA256SUMS precedente | `4ed360ee40d521e989e38fa2a2a68d5a5c461a5a6397c94dd34a598300141776` — **verificato su disco** ✅ |
| Inventario acquisito 1.869 file / 116 copie / 1.753 esterni | ⚠️ non ri-enumerato integralmente in questo ambiente (vedi Limiti) |

## Invariante D03 — analisi del codice (ledger.py @ 23859a2)

L'invariante richiesto («acquisizione e riuso applicano gli stessi controlli di contenuto; la riconferma autentica contenuti e legame durevole prima di qualsiasi server/stub») è implementato e **verificato sul sorgente**:

- ✅ **Validatore unico `_validate_zero_token_evidence(evidence, approval, row)`** con esattamente **11 controlli** (9 chiamate `require`, di cui una itera sui tre contatori): `request_id`, `request_identity_sha256`, `disposition='not_generated'`, `provider_request_id` non vuoto, `provider_evidence` non vuoto (str o dict), `prompt/completion/total_tokens` interi == 0, `approval.author`, `approval.decision='accepted'`, `approval.evidence_sha256==proof_sha256`. I contatori usano `type(x) is int`, che **esclude i bool** (`total_tokens=False` viene respinto). Ritorna il `frozenset` dei controlli superati, così la guardia può confrontare l'insieme effettivo e non la sola presenza della funzione.
- ✅ **Tre percorsi convergono sullo stesso contratto**: `reconcile_zero_token` (acquisizione) chiama il validatore direttamente; `_validate_attempts` lo richiama via `_validated_reconciliation` per **ogni** riga `ZERO_TOKEN_PROVEN` (non più solo gli antenati in `children`); `_gate_transport_record` chiama `_validated_reconciliation` quando lo stato è `ZERO_TOKEN_PROVEN`.
- ✅ **Impronta di contenuto ricalcolabile** distinta dall'hash del file: `_zero_token_content_digest = digest(canonical_json(value))`, memorizzata come `evidence_content_sha256`/`approval_content_sha256`, e un evento separato `reconciled_integrity:` lega i digest di contenuto, gli hash dei file, `request_id` e `previous_status`. In riconferma, `_validated_reconciliation` **ricalcola** i digest e verifica sia i contenuti sia il digest del legame (`marker['artifact_sha256']==digest(link)`), superando lo scoglio D02 dei confronti scalari auto-referenziali.
- ✅ **Byte letti una volta**: `reconcile_zero_token` legge i byte, poi `json.loads` e `sha256_bytes` **sugli stessi byte**; i due eventi (`reconciled:` + `reconciled_integrity:`) sono scritti nella stessa transazione `BEGIN IMMEDIATE`.
- ✅ **No-backfill storico**: una prova priva di `reconciled_integrity:` (o dei digest) è **rifiutata fail-closed** in riconferma/retry/gate; sblocco solo con riconciliazione revisionata separata, non inclusa.
- ✅ **quota_kind coerente col ruolo**: `_validate_attempts` calcola `expected_quota` (transport/remediation/base) e rifiuta i disallineamenti, senza toccare quote/contatori.

## Riproduzioni

### Test-contratto D03 del candidato (differenziale rosso/verde)

`test_d03_contract.py` eseguito col target selezionato via `FOT_HARNESS_TARGET`, dal sandbox del candidato, contro entrambi i codici:

- **Sul respinto a219bd4**: i **6** test dipendenti dal codice **falliscono** — `three_paths_invoke_the_same_content_control_set` (AssertionError «shared content validator absent»), `content_digests_and_independent_link_reject_valid_looking_changes`, `generated_symmetric_content_matrix`, `generated_reconciliation_envelope_matrix`, `generated_sql_field_matrix_and_forensic_positive_controls`, `missing_digest_is_fail_closed_without_backfill_even_before_retry`. ✅ (le prove **non sono tautologiche**)
- **Sul candidato 23859a2**: gli stessi 6 test **passano**, con **zero failure**; passa anche `inventory_covers_schema_and_new_fields_default_to_uncovered`. ✅
- Due metodi (`real_legacy_proofs…`, `real_runner_and_CLI…`) sono andati in **errore in entrambi** i miei run per dipendenze esterne assenti nella VM (checkout git di `0c8157f`; riferimenti del runner) — **non** failure di asserzione. Vedi Limiti.

### Sonda indipendente (mia, senza dipendenze esterne)

Ho costruito autonomamente una catena valida con retry (via API dei fixture), copiato in DB sacrificabile, alterato **solo** l'evento `reconciled:` e provato i cinque ingressi di conferma (gate_binding, gate_success, gate_outcome, frozen, producer_binding):

| Alterazione | Candidato 23859a2 | Respinto a219bd4 |
| --- | --- | --- |
| token positivi (prompt=1,total=1) | **rifiutato ×5**, DB invariato ✅ | **ACCETTATO ×5** (D03 riprodotto) |
| `total_tokens=False` (bool) | **rifiutato ×5** ✅ | **ACCETTATO ×5** |
| assenza di `reconciled_integrity:` (prova stile legacy) | **rifiutato ×5** (no-backfill) ✅ | **ACCETTATO ×5** |

Conferma indipendente e con modello diverso: D03 è reale su a219bd4 ed è **chiuso** su 23859a2 su tutte e tre le superfici, con database logico invariato.

## Suite (eseguite in questo ambiente)

| Suite | Esito osservato |
| --- | --- |
| `test_d03_contract` (differenziale) | **6/6** falliscono su a219bd4, **6/6+1** passano su 23859a2; 2 metodi env-bloccati ⚠️ ✅ |
| `test_harness_offline` | **20/20 OK** (dopo aver installato `jsonschema>=4.18` nella VM: la R4 `insight_adapter` richiede `Draft202012Validator`) ✅ |
| `test_metric_raccordo` | **9/9 OK** ✅ (raccordo metriche qualificato intatto) |
| `test_d02_predecessors` | **7/8** passano; l'8° (`runner_and_CLI_resume…`) solo env-bloccato (manca il manifest evidence 03.6) ⚠️ |
| `test_c01_c03` | env-bloccata: tutti gli errori derivano dal riferimento 03.6 assente (`…/reference/…/EVIDENCE_MANIFEST.csv`) ⚠️ |
| `test_d01_replay` | env-bloccata: `setUpClass` richiede il checkout git di `0c8157f` ⚠️ |
| Mirati **120/120**, discovery **155/155**, W/Y/Z/X, applicabili 14/14, guardiano | ⚠️ non ri-eseguiti integralmente in questo ambiente (vedi Limiti) |

Tutti i non-pass osservati sono **tracciati a riferimenti esterni assenti o a percorsi assoluti macOS irrisolvibili nella VM**, non a difetti del candidato. `test_harness_offline` e `test_metric_raccordo` (che non dipendono da quei riferimenti) passano al 100%.

## Perimetro e delta

- ✅ **Nessun file cambia fuori da `studio2/fase03/harness/`** tra base documentale `e9b60c5` e candidato `23859a2`.
- ✅ L'**unico modulo runtime** modificato è **`ledger.py`** (più il nuovo `test_d03_contract.py` e le directory evidence/acquisizione). Correzione **circoscritta**, come da piano.
- ✅ `metric_adapter.py`, `metrics.py`, `test_metric_raccordo.py`, `gate_rules.py` **byte-identici** ad a219bd4 (gate/raccordo intatti).
- ✅ Tutti i moduli live compilano (`py_compile`, exit 0).

## Matrice dei 50 metodi

La matrice nominativa dei 50 metodi (con corrispondenze, N48≡C02, adattamenti/accorpamenti) è quella acquisita e conservata byte-identica nelle evidence del candidato; **non si dichiara 50/50 letterali**. In questo ambiente ho ri-esercitato in modo probante il **nucleo D03** (contratto differenziale + sonda indipendente), `test_harness_offline` (20), `test_metric_raccordo` (9) e 7/8 D02. Le voci runner-dipendenti (C01/C02/C03, D01 legacy, W/Y/Z/X, applicabili) **restano ⚠️** perché richiedono i riferimenti esterni non raggiungibili dalla VM; non le converto in ✅ per cortesia.

## Confini

Guardiano documentale: dichiarato **NON PASS non bloccante** (35 test, gli stessi **14 fallimenti preesistenti** dei walkthrough v1, 1 skip) — non ri-eseguito qui (fuori dal sandbox `studio2`) e comunque **non** motivo di NON OK tecnico. D9 approvata (122B principale/consumer, 27B alternativo, Terra storico interno) resta separata: recepimento eseguibile D9, ordine label 1a, qualificazioni servizi/tokenizer/identità/capienza, T5 e autorizzazione pilot **fuori perimetro**. Preflight storico bloccato. **Nessun freeze, nessun GO.** 03.10 e Fase 03 restano aperte.

## Limiti di questa verifica

1. **Ambiente di esecuzione.** Le prove girano in una VM Linux (Python 3.10.12 / SQLite 3.37.2), non sul macOS del preparatore (3.13.9 / 3.51.0). I risultati del nucleo D03 sono robusti rispetto a questa differenza, ma i **conteggi pieni** (mirati 120, discovery 155, W/Y/Z/X, applicabili 14) **non** sono stati riprodotti qui.
2. **Riferimenti esterni non raggiungibili.** Molte suite runner (C01/C02/C03, D01, il runner di D02 e 2 metodi D03) leggono per impronta artefatti a **percorsi assoluti** `/Users/luker/…` (manifest evidence 03.6; checkout git di `0c8157f`) che non esistono nella VM: sono errori di riferimento, non difetti. Per riprodurli occorre eseguire sull'ambiente reale o montare quei riferimenti agli stessi percorsi.
3. **Dipendenza installata.** Ho installato `jsonschema>=4.18` nella VM (solo `~/.local`, nessuna scrittura nelle cartelle utente) per far girare la R4; sul macOS del preparatore la dipendenza è già presente.
4. **Matrice 50 metodi e inventari acquisiti** verificati per SHA e struttura dei campioni, non ri-enumerati integralmente (1.869 membri).
5. **Modello servito** non dimostrabile dall'interno; dichiaro la famiglia (Claude) diversa da gpt-6-astra.

## Conclusione

**OK sul candidato tecnico esatto `23859a2` limitatamente al perimetro D03**, con le riserve ⚠️ sopra. Il difetto D03 è corretto in modo dimostrato e indipendente (differenziale rosso/verde + sonda propria + ispezione del codice), l'invariante regge sui tre percorsi con impronte di contenuto ricalcolabili e no-backfill, il perimetro è pulito e la correzione è circoscritta a `ledger.py`. **Non ho riscontrato alcun difetto.** Le porzioni non verificate lo sono per limiti d'ambiente, non per problemi del candidato: prima della chiusura formale della verifica andrebbero rieseguite sull'ambiente di riferimento (mirati 120, discovery 155, C0x/D01 runner, W/Y/Z/X, guardiano, perimetro 176 file via scope_audit). Nessun freeze o GO.

---
*Verifica indipendente svolta in sola lettura. Sandbox e log conservati nello scratch della sessione; SHA-256 di questo verbale comunicato separatamente, senza autoreferenza.*
