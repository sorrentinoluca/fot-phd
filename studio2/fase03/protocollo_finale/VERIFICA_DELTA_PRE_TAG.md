**Esito: OK al tag, con quattro rilievi di sola nota.** Nessun bloccante. I due commit da
integrare sono `74c5d3dca78fc22c3de1e675e50e7d0870f45ecc` (rem6) e
`d330aef6e54402c0093334ba31345ecce6c7274d` (protocollo), in quest'ordine; il tag va sul commit
di merge risultante in `main` dopo il secondo merge.

# VERIFICA_DELTA_PRE_TAG — review indipendente dei soli delta 7.3-R

Data: 2026-09-18. Sessione **Claude Cowork nuova e indipendente**, `claude-opus-5`, **in
sostituzione dichiarata** di `b567`/`gpt-6-astra`, a cui `PROMPT_7_3_R_DELTA_REVIEW.md` era
indirizzato. Non è la finestra di orchestrazione né una di quelle che hanno scritto i delta.

**Sola lettura, offline.** Nessuna chiamata a provider, nessuna modifica a codice, candidato,
ledger o artefatti; nessun push, merge, tag o materializzazione. `api_key.json` e
`server_enea.json` non letti. Cartelle collegate: `/Users/luker/fot-tep` e
`/Users/luker/fot-tep-pubblicazione-consolidamento-0315-metriche`; **`fot-tep-runtime` non è
stata collegata né letta**. Tutte le verifiche Git sono reali, sull'object database
`/Users/luker/fot-tep/.git` (`GIT_DIR`), come nella review precedente.

## Base

`protocollo_finale/VERIFICA_FINALE_PROTOCOLLO_RUNNER_H3.md`, SHA-256 ricalcolato da me:
`a2fe4b6753cdbac04f0eaddd9902f735adeb0c201bc220d882532ec8f81fba6a` — **coincide** con quello
del mandato. Lo stesso file è ora **tracciato** in `d330aef` ed è **byte-identico** alla copia
in worktree (`git show d330aef:… | diff -` senza differenze). Non ho rifatto ciò che quella
review ha già riprodotto: qui ci sono solo i due delta e la prova che non abbiano rotto il
resto.

## Delta esaminati

| Oggetto | Ramo | Delta | File toccati |
| --- | --- | --- | ---: |
| Runner | `codex/studio2-riconciliazione-stop-contabile` | `7925124..74c5d3d` (`7d58efd` codice, `74c5d3d` sola documentazione) | 12 |
| Protocollo | `codex/studio2-freeze-protocollo-finale` | `9edf31e..d330aef` (rev4) | 5 |

`74c5d3d` è **davvero di sola documentazione**: modifica `REPORT_7_4_FIX.md` e aggiunge
`batch_finale/SUITE_MAC_7d58efd.txt`, nient'altro.

L'unione dei due delta è di **17 file**: tre documenti 7.4, il log di suite, il record di
aggiornamento 03.11, il contratto rev2, quattro moduli di codice
(`canary_marking.py`, `ledger.py`, `runtime.py`, più i due entrypoint e
`query_canary_marking.py`), un modulo di test, e i quattro documenti di `protocollo_finale/`.

---

## 1. Invarianza

**I tre artefatti ricalcolati.** Ho estratto l'albero di `74c5d3d` in una directory separata e
rieseguito i generatori nella VM Linux (Python 3.10.12, **NumPy 2.2.6**, l'ambiente di
riferimento di §7.1):

| Artefatto | Atteso | Ricalcolato |
| --- | --- | --- |
| Inventario | `227e5e9c797dbfd8be746d85b77298f5dfb091846dc301f0b2e31ea1dbc6df3f` | **identico** |
| Schedule | `1acfc4044c53f113016ed0bfab58863291a9060a9edc9abadb68a21d30687819` | **identico** |
| Assegnazione finestre | `c809e79d2c03d74f4a5a37988eca809bda336468ab0060f794d3c214f9a6a775` | **identico**, e il file prodotto è **byte-identico** all'artefatto committato |

`build_window_assignment.py` ha riprodotto anche `useful_windows_check = PASS`,
`status = FROZEN_BEFORE_TEST_DATA`, 78 run assegnati.

**Le due catene non toccate.** Nessun file della catena del manifest di input
(`67e7584a…`) né della mappa dei prompt (`b8192003…`) è nel diff. Verificato blob per blob fra
`7925124` e `74c5d3d`: `build_final_inventory.py`, `build_final_prompts.py`,
`build_window_assignment.py`, `protocol.py`, `protocol_bnolf.py`, `harness/final_inventory.py`,
`harness/final_prompts.py`, `harness/window_assignment.py`, `harness/sampling.py`,
`harness/common.py`, `evidence/extract_evidence.py`,
`evidence/extract_test_lot_evidence.py`, `librerie/LIBRERIE_FINALI_CANDIDATE.json`,
`pseudolabel/CONDITION_E_DERANGEMENTS.json` e i tre artefatti di `batch_finale/` —
**tutti allo stesso blob**. Di `runtime.py` cambia solo `execute_request` (più la nuova
eccezione tipata), non `durable_write`, che è l'unica funzione che i due generatori importano
da lì. `protocol.py` resta `791fa347…` su tutta la catena.

**Ramo pilot del ledger: invariato.** Il diff di `ledger.py` è di sole aggiunte e tocca
esclusivamente il ramo `final_batch`:

- `record_canary_day` e `record_canary_stop` guadagnano `observed_day=None` — parametro
  opzionale, quindi firma retrocompatibile; entrambe agiscono su `final_canary`, stage che
  **non appartiene** a `PILOT_PROFILE.stages` (`ACTIVE_STAGES`), e `record_canary_stop`
  pretende già `profile.name == 'final_batch'`;
- `completion_instants` è nuovo, di **sola lettura** (`SELECT`), e rifiuta uno stage fuori dal
  profilo.

In `runtime.py` la firma di `execute_request` perde il parametro `journal` e `journal_path`
diventa opzionale: **nessun chiamante passava `journal=`**, e i due ingressi del pilot
(`run_pilot.py`, `producer_probe.py`) passano sempre `journal_path`, quindi la proiezione del
pilot è invariata. `IdentitySuspension` è sottoclasse di `HarnessError`: ogni `except
HarnessError` esistente continua a catturarla.

Prova comportamentale in §6: sulla stessa VM, i **291 test** della base e i **303** del delta
danno un insieme di non-pass **identico nome per nome**.

## 2. B1 — `--day` legato all'orologio

**Chiuso.** `run_final_batch.resolve_civil_day` confronta il giorno dichiarato con
`rome_day(now)` e restituisce `declared_day`, `observed_day`, `midnight_crossing`.

**Eccezione di mezzanotte, stretta.** Il giorno dichiarato può differire dall'osservato solo
se il giorno osservato è **quello immediatamente successivo** (`_is_next_day`) **e**
`crossing_evidence()` è vera; per il lotto scientifico l'evidenza è
`stage_began_on(ledger, stage, day)`, che cerca in `ledger.completion_instants(stage)` almeno
una richiesta **completata nel giorno dichiarato**. Per il canary `crossing_evidence` è `None`:
il canary **non attraversa mai**. Il ledger ripete il rifiuto in `record_canary_day`.

**Il controesempio chiesto dal mandato è respinto.** Ho eseguito una prova indipendente dai
loro test, chiamando direttamente il modulo:

| Caso | Esito osservato |
| --- | --- |
| canary PASS del giorno X, lotto in X+1 con `--day X`, **nessuna** richiesta completata in X | `BatchStop: declared day 2026-09-18 differs from the observed Europe/Rome day 2026-09-19…` |
| stesso caso **con** richieste completate in X | accettato, `midnight_crossing = True` |
| X+2 anche con evidenza | `BatchStop` |
| giorno osservato **precedente** al dichiarato | `BatchStop` |
| canary con giorni diversi (`crossing_evidence=None`) | `BatchStop` |
| `--day` assente | dichiarato = osservato, `midnight_crossing = False` |
| `--day 18-09-2026` | `BatchStop: … is not an ISO civil date` |
| `stage_began_on` su completamento alle 21:00Z del 18 | `True` |
| idem alle 23:30Z del 18 (= 01:30 di Roma del 19) | `False` — il fuso è applicato davvero |

**Persistenza.** Entrambi i valori finiscono: nell'evento canary (`detail` di
`record_canary_day`, campi `declared_day`/`observed_day`); nel record durevole di **ogni**
chiamata del batch e del canary, attraverso la closure `evaluate` — e il record valutato è un
payload opaco sigillato (`responses.record_json`), quindi i campi nuovi sono conservati e
improntati senza toccare il `DURABLE_FIELD_CONTRACT`; nel riepilogo di tratto, insieme alla
regola in chiaro (`midnight_crossing_rule`); e nell'artefatto del giorno invalido.

**Il controllo è rifatto prima di ogni richiesta**, non solo all'avvio: nel ciclo di `run_pass`
`resolve_civil_day` precede `require_canary_ok`, e con `now=None` rilegge l'orologio a ogni
giro. L'attraversamento a metà tratto è quindi deciso dalla regola, non subìto. Il runbook §5
scrive la regola in forma stretta, con l'esempio del tratto delle 22:00.

## 3. B2 — maschere

**Chiuso e coerente con §6.5 rev4.** `canary_marking.marking` espone ora
`primary_mask_request_ids` (piano §10.5, giorno civile marcato, con
`primary_mask_source`), `forensic_mask_request_ids` (§6.5, intervallo di esposizione, con
`forensic_mask_source`), `union_descriptive_request_ids` (con `union_scope` che ne dichiara la
natura descrittiva), più i due residui `primary_only_…`/`forensic_only_…`. La versione
dell'artefatto passa a `MARCATURA_CANARY_7_4_2` e la docstring del modulo riporta la gerarchia
invece dell'unione.

**Nessun campo generico residuo.** `marked_request_ids`, `marked_requests`, `interval_only` e
`civil_day_only` non compaiono più in alcun modulo, script o artefatto: le uniche due
occorrenze in tutto l'albero sono la riga di `REPORT_7_4_FIX.md` che ne dichiara la rimozione e
l'asserzione di test `assertNotIn("marked_request_ids", value)`.

**Coerenza documentale.** I tre nomi compaiono identici in `PROTOCOLLO_FINALE_CANDIDATE.md`
§6.5 punto 5, in `PROTOCOLLO_FINALE_CANDIDATE.json` (`canary_rules`), nel runbook §3 e nella
tabella degli STOP del runbook. `query_canary_marking.py` tronca ora i tre elenchi e calcola
`truncated` prima di troncare: corretto.

## 4. B3 — contratto e journal

**Contratto congelato byte-invariato.** `harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md` ha lo
stesso blob (`e52b1b34…`) su tutta la catena `f0d0393 → 9e0e086 → 7e497dc → a51ffd1 →
7925124 → 7d58efd → 74c5d3d`; SHA-256 del contenuto
`b4e822a300eaf1f1b23c8e76f9043374678ca3bbce84e8efd365167a998d48dc`, **identico al pin** di
`harness/HARNESS_D9_CANDIDATE.json`.

**Clausola nel file nuovo.** `harness/CONTRATTO_ESECUZIONE_E_RIPRESA_REV2_BATCH_FINALE.md`
(SHA `6dbaebd6329932defd560bb619ba884e23bbfe8e3a341bed44facb127dc3f9e5`) limita la deroga ai
soli stage del profilo `final_batch` e lascia il contratto storico integralmente in vigore per
il pilot. Le quattro voci della proiezione dichiarata **esistono nel codice**: SQLite
autorevole, `{stage}_call_log.jsonl` (`JsonlCallLogger`), `{stage}_record_<request_id>.json`
(`durable_write`) e `{stage}_summary.json` (`durable_write`). Le tre verifiche che il contratto
stesso prescrive le ho eseguite tutte e tre, tutte OK.

**Nessun riferimento a journal non scritto.** `grep -n journal run_final_batch.py
run_final_canary.py` non restituisce **nulla**: spariti il no-op `append_journal`, la lambda
del canary, le due variabili `journal_path` e il commento che descriveva ciò che non avveniva.

**Il protocollo cita la revisione giusta.** §7.2 rinvia ora a
`harness/CONTRATTO_ESECUZIONE_E_RIPRESA_REV2_BATCH_FINALE.md` per gli stage `final_batch` e
dichiara che «il contratto storico senza suffisso resta congelato per il pilot».

## 5. B4–B6 — i test esercitano davvero il ramo

**B4 (eccezione tipata).** `runtime.IdentitySuspension(HarnessError)` è sollevata nei due punti
in cui l'identità manca o cambia, con `field`, `observed`, `expected`; `run_final_canary` la
intercetta **per tipo** e il campo cambiato finisce nell'evento di STOP durevole. Il ramo
`except IdentitySuspension` è **realmente percorso** da due test
(`test_identity_change_stops_before_any_further_call` e
`test_a_fingerprint_change_stops_the_canary_and_is_persisted`): se l'eccezione non fosse quella
tipata, non verrebbe catturata e l'evento `canary_stop:identity:` non esisterebbe — i test lo
asseriscono. Vedi però il rilievo **1**.

**B5 (rifiuto senza tzdata).** `canary_marking.rome_day` ora solleva `HarnessError` se
`zoneinfo` non è importabile, invece di stimare con i confini fissi 31 marzo / 27 ottobre. Due
test lo esercitano davvero: il primo **sostituisce `builtins.__import__`** per far fallire
`import zoneinfo` e verifica il messaggio; il secondo verifica il cambio d'ora **reale** del
2026 (25 ottobre), cioè proprio il punto dove il vecchio fallback sbagliava —
`2026-10-25T23:30Z → 2026-10-26` e `2026-10-24T23:30Z → 2026-10-25`. Esiste ora **una sola**
definizione di `rome_day` in tutto l'albero, condivisa fra marcatura, barriera e runner: il
duplicato di `run_final_canary` è stato rimosso.

**B6 (tetto totale 7.202).** `test_the_total_ceiling_is_refused_on_its_own_path` asserisce
prima l'identità reale del profilo (`planned_maximum = hard_stop = 7.202 =
Σ base_limits + retry_quota`, ricalcolata sul `FINAL_BATCH_PROFILE` vero), poi **percorre
entrambi i rami del totale** su un profilo con quote per stage larghe e totale stretto:
`planned request maximum … reached` e `cumulative hard stop … reached`. Sono i due rami di
`_insert_intent` che con 7.202 si raggiungerebbero solo a campagna conclusa, e che prima non
erano mai eseguiti. Il rilievo è chiuso.

**B7.** Nessuna modifica, come il mandato chiedeva: la dipendenza dei pin da NumPy 2.2.6 e il
`protocol_reference: e0db132` dentro il payload hashato sono **dichiarati** in
`REPORT_7_4_FIX.md` §FIX-3/B7, nel candidato §7.1 e nel JSON (`pin_dependency_note`).

## 6. Suite

`batch_finale/SUITE_MAC_7d58efd.txt`, SHA-256 ricalcolato
`66c3492709f8aede6e7813c01e3feb2b5748bb9301acdeef4e4b0ed09969de66` — **coincide** con quello
del mandato e con il blob committato in `74c5d3d`. Il log riporta `Ran 318 tests in 475.815s`,
`OK`: zero failure, zero error, zero skip. Restano solo `ResourceWarning` di connessioni SQLite
chiuse dal garbage collector, che non incidono su alcun esito.

**318 = 306 + 12, dimostrato per costruzione.** Fra `7925124` e `74c5d3d` l'**unico** modulo di
test modificato è `harness/test_final_batch.py`, che passa da **33** a **45** metodi `test_`
(dodici aggiunti, nessuno rimosso): la nuova classe `CivilDayBinding` (**9** test di B1),
la nuova classe `RomeDayWithoutTzdata` (**2** test di B5) e
`test_the_total_ceiling_is_refused_on_its_own_path` (**1**, B6) dentro `BatchExecution`;
9 + 2 + 1 = 12. Le due modifiche a `CanaryBarrierAndMarking` per B2 cambiano asserzioni dentro
test esistenti, senza aggiungerne. Nessun altro file di test è toccato, quindi l'incremento del
conteggio della stessa esecuzione è esattamente 12. Da solo, nella VM, il modulo gira in **45 test, OK**.

**I non-pass della VM.** Ho rieseguito i **19 moduli** di `studio2/fase03/harness/test_*.py`
nella VM Linux su entrambe le revisioni, con lo stesso interprete e lo stesso ambiente:

| Esecuzione | Test | Failure | Error | Skip |
| --- | ---: | ---: | ---: | ---: |
| Base `7925124` | 291 | 3 | 49 | 22 |
| Delta `74c5d3d` | **303** | 3 | 49 | 22 |

L'insieme dei non-pass è **identico nome per nome** (63 righe, `diff` vuoto): il delta **non
introduce alcun non-pass e non ne risolve alcuno**. Le tre cifre coincidono con quelle che la
review precedente aveva osservato nella sua VM (3F/49E/22S).

Le cause sono tutte ambientali e le ho isolate a mano: **42 dei 49 error** sono
`ImportError: cannot import name 'Draft202012Validator'` — `jsonschema` 3.2.0 nella VM — e le
loro cascate a valle; gli altri sette e i tre failure vengono da worktree e percorsi che
esistono solo sul Mac (`git -C /Users/luker/fot-tep-riverifica-harness-…` esce 128,
`/Users/luker/fot-tep-verifica-harness-0310-…` assente). Controprova: `test_window_assignment`
dà 11 error quando l'object database non è raggiungibile e **11 test, OK** appena si esporta
`GIT_DIR`. Nessun non-pass sta nei moduli toccati dal delta.

## 7. A1–A3 e H3 nel rev4

**A1 — chiuso.** §7.1 passo 2 integra ora rem6 **fino a `74c5d3dca78fc22c3de1e675e50e7d0870f45ecc`**
e chiede esplicitamente che in `main` risultino raggiungibili **entrambi** i log:
`SUITE_MAC_a51ffd1.txt` (in `7925124`) e `SUITE_MAC_7d58efd.txt` (in `74c5d3d`). Verificato:
`7925124` è antenato di `74c5d3d` e i due file sono entrambi presenti nell'albero di
`74c5d3d`, con SHA `50601686…` e `66c34927…`. La riga «Runner finale 7.4» di §2, il JSON
(`runner_freeze.mac_suite_logs`, `integration_order`, `blocking_dependencies`,
`remaining_open`) e §7.2/§8 dicono la stessa cosa.

**A2 — chiuso nella forma richiesta.** Il verbale storico
`fault_runs/ACQUISIZIONE_OK_ESECUZIONE_03_11.md` è **non modificato in luogo**: stesso blob
`4a9f7706` a `9edf31e` e a `d330aef`, SHA `ddd986c1…` invariato. Accanto ad esso il delta
aggiunge il file nuovo `fault_runs/AGGIORNAMENTO_PUBBLICAZIONE_E_RIVERIFICA_03_11_2026-09-17.md`,
SHA ricalcolato `1c382fda87bc99d2177461c44fdef1ae50e977abfa9b5113a57587dab3e0bc2c`, che
registra pubblicazione e riverifica per riscaricamento — 3/3 asset OK, 150.196.983 byte, zero
mismatch, `release_id`/`release_commit`/`published_at_utc` lasciati `null`. È citato in **§2**
(riga «Lotto 03.11», con il proprio SHA), in **§2.1** e in **S13** di §8.2; nel JSON compare in
`repository_sources` e in `release_coordinates` con
`historical_acquisition_unchanged: true`. I tre SHA degli asset nel file nuovo coincidono con
quelli che §2.1 già dichiarava.

**A3 — chiuso.** La riga «Prompt finali» di §2 diventa «Mappa canonica dei prompt finali»: il
pin di `final_prompts.jsonl` è **rimosso**, la mappa `b8192003…` è dichiarata «vincolante» e lo
SHA del file è rinviato a 7.4-MAT. Nel JSON `final_prompts_file_sha256` è ora `null` con
`final_prompts_file_status: "product of 7.4-MAT; record its SHA at materialization"`, e
`prompts_canonical_status` dichiara la mappa riprodotta dalla review. Lo SHA `f938604c…` non
compare più in alcun documento di `protocollo_finale/`; sopravvive soltanto nella tabella
storica §3 di `REPORT_7_4_FIX.md` — vedi il rilievo **3**.

**A4, A5, A6, C1 — recepite, e le aritmetiche tornano.**

- A4: §5.1 dice ora «**arrotondato per difetto a 400 (401,35 al +15 %)**». Ricalcolato:
  349 × 1,15 = 401,35. Esatto.
- A5: §5.2 aggiunge «circa **9,0 h/giorno** sulla media e **12,6 h/giorno** sulla p95; oltre il
  settimo giorno la quota canary ferma il batch». Ricalcolato: 62,9181/7 = 8,988;
  88,0106/7 = 12,573. Esatto.
- A6: §1.2 dichiara ora la base delle alternative illustrative — «il **solo** nucleo» a otto
  finestre e «circa **105/147 h** … calcolati come `2 × 7.202`». Ricalcolato:
  1.728 × 3 × 8 = 41.472; 2 × 7.202 × 26,2086/3600 = 104,9 h e × 36,6609/3600 = 146,7 h; e le
  377 h si riottengono da 41.472 + 1.548 + 70 chiamate con margine 20 % (376,4 h). Tutto
  coerente.
- C1: §10 dichiara che «lo script trascrive Tango invece di importarlo e non verifica a runtime
  gli SHA dichiarati», che identità e SHA sono stati verificati dalla review finale e che lo
  script **non viene modificato** perché il suo SHA è pinnato nei risultati; il JSON porta
  `implementation_note` e `script_modified_for_rev4: false`. Corretto: lo script è infatti
  invariato nel delta.

**H3 — TANGO MANTENUTO con le limitazioni intatte.** §8.2 porta S6, S10 e S11 a
**TANGO MANTENUTO**; il JSON porta `synthetic_verification.status = "TANGO_MANTENUTO"` con il
record di review e il suo SHA, e `author_decisions_rev3.D11_outcome = "TANGO_MANTENUTO"`;
`DECISIONI_AUTORE_7_3_REV3.md` sostituisce il `PENDING` con l'aggiornamento datato. Le
limitazioni **non sono attenuate** e sono ripetute in tutti e quattro i luoghi: livello e FWER
completo **approssimati e non garantiti**, verifica **locale a H3** e non del FWER congiunto,
**indipendenza fra run assunta** anche dal fallback, e i valori di robustezza invariati —
massimo ICC con tutti i punti ≤0,055 pari a **0 per Tango H3** e **0,20 per Hoeffding H3 e
H1/H2** (§9.2, §10 Q2, D11). `decision_rule` sostituisce «incomplete => PENDING» con
«incomplete => no decision», coerente.

**Nessun segnaposto.** Nel candidato rev4 non restano occorrenze di segnaposto, TBD, TODO o
`PENDING` di stato: le uniche occorrenze delle parole sono dichiarative («Non restano
segnaposto», «un requisito bloccante `PENDING` impedisce…», e un riferimento storico a `b567`
come provenienza di una copia byte-identica).

**Ogni SHA citato coincide col file.** Ho estratto meccanicamente tutte le **68** coppie
`path`/`sha256` del JSON rev4 e le ho ricalcolate: **59 verificate dall'object database, 0
discordanze**. Delle nove restanti, tre sono percorsi assoluti a file non tracciati del
`main` collegato e le ho ricalcolate sul disco — `PROMPT_7_3_FREEZE_PROTOCOLLO_FINALE.md`
`1f60f7f6…`, `PROMPT_7_2_PREP_LIBRERIE_INSIGHT.md` `aa074abb…`,
`HANDOFF_FASE03_2026-09-17_rev07.md` `5ee95c19…`, tutte **coincidenti**; tre sono percorsi
assoluti alla worktree rem6 e corrispondono a file tracciati, verificati per quella via
(`235fb0de…`, `90e93923…`, `fce3b955…`); tre stanno in `fot-tep-runtime`, che il mandato
esclude — non verificate qui e dichiarate tali (la review precedente le aveva verificate).
Ho poi confrontato i **70** SHA a 64 cifre del `.md` rev4 con quelli del JSON: i due che non
compaiono nel JSON sono l'audit 03.11 `420a61eb…` e il piano F5 `ef0b2852…` di §7.1, che ho
ricalcolato su `main` (`fault_runs/BATCH_AUDIT_03_11.json` e
`fault_runs/plans/test_batch_f5.csv`): **coincidenti**. I SHA propri dei quattro documenti di
`protocollo_finale/` a `d330aef` sono `5d130dd4…` (candidato `.md`, che è quello che il JSON
dichiara), `cdf64c94…` (`.json`), `7826f7af…` (decisioni rev3, dichiarato nel JSON) e
`a2fe4b67…` (review finale).

## 8. Ordine di merge — ripetuto meccanicamente

**Passo 1 — rem6 `74c5d3d` in `main` (`ea90761d`).** Base di merge `540df7b`. Il ramo cambia
**41** file, `main` ne ha cambiati **691** dalla stessa base; l'**unica** sovrapposizione è
`studio2/fase03/fault_runs/.gitignore`. Il merge a tre vie di quel file **riesce senza
conflitto**: `git merge-file` esce **0** e `git merge-tree 540df7b main 74c5d3d` produce **zero**
marcatori di conflitto, con una sola voce `changed in both` che è appunto quel `.gitignore`.
Il risultato conserva la riga `/test_batch/` duplicata — la nota **N** della review precedente,
innocua per la semantica di `.gitignore`.

**Passo 2 — poi il protocollo `d330aef`.** Base di merge `ea90761d`, **già in `main`**. Il ramo
cambia **1.650** file; l'intersezione con i 41 di rem6 è **vuota** e l'intersezione con i file
cambiati da `main` dopo `ea90761` è **vuota** (`main` non si è mossa). `git merge-tree` produce
**zero** marcatori di conflitto. Fuori da `protocollo_finale/` il ramo tocca due soli file:
`fault_runs/AGGIORNAMENTO_PUBBLICAZIONE_E_RIVERIFICA_03_11_2026-09-17.md` (nuovo) e
`fault_runs/ARTIFACT_STORAGE.json` (già esaminato dalla review precedente, non toccato dal
delta rev3→rev4).

**Passo 3 — il tag annotato**, su mandato dell'autore. **Passo 4 — 7.4-MAT**, dopo il tag.

Nessuno dei due merge è un fast-forward (`main` non è antenata di `74c5d3d`; dopo il passo 1
`main` non è antenata di `d330aef`), quindi entrambi producono un commit di merge.

---

# Rilievi

Tutti di **sola nota**: nessuno impedisce il tag, nessuno tocca contabilità, riproducibilità o
contenuto scientifico.

**1 — nota — B4 chiude il ramo ma non la sua regressione.** La classificazione per tipo è
implementata e i due test esistenti la percorrono davvero; manca però un test che dimostri
**ciò che B4 chiedeva**, cioè che una **riformulazione del messaggio** in
`runtime.execute_request` non faccia più perdere l'evento durevole. Con la vecchia logica per
sottostringa quegli stessi due test passavano: non distinguono le due implementazioni. Un test
che sollevi `IdentitySuspension` con un messaggio arbitrario e verifichi che
`canary_stop:identity:` viene comunque scritto chiuderebbe il punto. Il comportamento resta
fail-closed in ogni caso.

**2 — nota — la prova di «lotto iniziato nel giorno dichiarato» poggia sui completamenti, non
sugli intenti.** `stage_began_on` legge `completed_utc`. Un tratto avviato negli ultimi minuti
del giorno X, la cui **prima** richiesta si completi dopo mezzanotte, non ha alcun
completamento nel giorno X: alla prima riverifica dentro il ciclo la regola lo rifiuta, pur
essendo un attraversamento legittimo. L'esito è fail-closed (mai permissivo) e il runbook
indirizza già l'operatore al canary di X+1, ma `intent_utc` sarebbe l'istante che prova
davvero l'inizio del lotto. Finestra stretta, nessuna conseguenza contabile.

**3 — nota — lo SHA di `final_prompts.jsonl` sopravvive nella tabella §3 di
`REPORT_7_4_FIX.md`.** Il pin normativo di §2 è stato tolto, ma il report — che viene integrato
in `main` insieme al resto — continua a presentare `f938604c…` come valore misurato di un file
che, per A3, non esiste in nessun luogo conservato. Non c'è contraddizione di forza vincolante
(il report è un record storico di 7.4-PREP e il candidato dichiara ora il file prodotto di
7.4-MAT), ma una riga che marchi quella cifra come storica eviterebbe di rimettere in
circolazione esattamente l'oggetto che A3 ha depinnato.

**4 — nota minore — «sedici moduli» nel report, diciannove nel comando.** `REPORT_7_4_FIX.md`
§FIX-3 dice che la suite sul Mac copre sedici moduli, ma il comando che riporta subito sotto,
`ls studio2/fase03/harness/test_*.py`, ne seleziona **diciannove** in quell'albero. Imprecisione
documentale: il conteggio 318 e l'esito `OK` non ne risentono. Nella stessa sezione la tabella
della VM Linux (2F/33E) descrive un ambiente diverso dal mio (3F/49E) — differenza di
`jsonschema` e di raggiungibilità dell'object database, non del codice; ciò che conta,
l'identità fra base e delta, è verificata sopra.

---

# Esito e istruzioni per il tag

**OK al tag, con i quattro rilievi di nota qui sopra. Nessun bloccante.**

I rilievi A1, A2, A3, A4, A5, A6 e C1 della review finale sono recepiti; B1, B2, B3, B4, B5 e
B6 sono chiusi con codice e test che percorrono davvero i rami interessati; B7 è dichiarato
come richiesto. I cinque pin invarianti reggono: i tre ricalcolabili sono stati ricalcolati e
coincidono, e nessun file delle due catene restanti è nel diff. Il ramo pilot del ledger è
invariato. L'esito §5 di H3 resta **TANGO MANTENUTO** con le limitazioni intatte.

**I due commit esatti da integrare, in quest'ordine:**

1. `74c5d3dca78fc22c3de1e675e50e7d0870f45ecc` — ramo `codex/studio2-riconciliazione-stop-contabile`;
2. `d330aef6e54402c0093334ba31345ecce6c7274d` — ramo `codex/studio2-freeze-protocollo-finale`.

**Il commit su cui va il tag** `studio2-fase03-protocollo-finale-frozen-001`: il **commit di
merge risultante in `main` dopo il secondo merge**, cioè la punta di `main` a integrazione
completata. Non è nominabile in anticipo perché nessuno dei due merge è un fast-forward: il
commit non esiste finché i due merge non sono eseguiti. Il tag va annotato, su mandato
dell'autore, e solo dopo si passa a 7.4-MAT.

Nessun merge, tag, materializzazione o chiamata è stato eseguito da questo incarico.
