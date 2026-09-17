**A — OK con rilievi. B — OK con rilievi. C — OK.** Esito §5 di H3: **TANGO MANTENUTO**.
Nessun rilievo bloccante. Il tag non va creato su `9edf31e`.

# VERIFICA_FINALE_PROTOCOLLO_RUNNER_H3 — review indipendente unica 7.3-R finale

Data: 2026-09-18. Sessione **Claude Cowork indipendente**, `claude-opus-5`, **in sostituzione
dichiarata** della finestra `b567`/`gpt-6-astra` a cui il mandato
(`PROMPT_7_3_R_FINALE_REVIEW_UNICA.md`) era indirizzato. Sola lettura: nessuna chiamata a
provider, nessuna modifica a codice, candidato, ledger o artefatti del runtime; nessun
push/merge/tag; nessuna materializzazione. `api_key.json` e `server_enea.json` non letti. Non
sono stati letti dati TEP, segnali o risposte di modelli oltre a quanto serviva per rendere i
prompt e per ricalcolare le latenze del gate.

## Ambiente e limiti dichiarati di questa review

- Runtime dei modelli **non collegato**; nessuna chiamata era comunque prevista.
- La suite **non è stata rieseguita sul Mac**. È stata rieseguita per intero nella VM Linux
  (Python 3.10.12, NumPy 2.2.6) e confrontata con l'esito acquisito sul Mac.
- `git` non funziona sulle worktree collegate perché `.git` punta a percorsi del Mac. Tutte le
  verifiche Git sono state fatte sull'object database di `/Users/luker/fot-tep/.git`
  (`GIT_DIR`), quindi `git show`, `git log`, `git diff` e `git merge-file` sono **reali**: non è
  stato necessario delegare comandi.
- Le librerie insight e il manifest di input congelato del pilot sono stati letti su richiesta
  esplicita di accesso alle sole cartelle `…/studio2-fase03-d9-pilot-03/results` e `…/execution`.
- Il ledger reale del pilot **non è stato aperto**; l'invarianza del ramo pilot è stata verificata
  sul codice, sui test e sul meccanismo di profilo (§B.2), non sulle righe del database.
- Riproduzioni eseguite in questa review: assegnazione finestre, inventario, schedule, i 2.244
  prompt, la griglia H3 completa (1.596 scenari × 100.000 repliche), le latenze del gate, tutti
  gli SHA-256 leggibili offline.

## Oggetti

| Oggetto | Riferimento | Esito |
| --- | --- | --- |
| A — protocollo | `codex/studio2-freeze-protocollo-finale`, `9edf31e56572aaa4cd36ac9307ad014c3a7a22e2` | **OK con rilievi** (A1–A3 prima del tag) |
| B — runner | `codex/studio2-riconciliazione-stop-contabile`, `9e0e086`→`7925124` | **OK con rilievi** (B1–B3 prima del tag) |
| C — verifica sintetica H3 | `b465f90` (pre-simulazione) e `d0cfeab` (risultati) | **OK** |

`PROTOCOLLO_FINALE_CANDIDATE.md` SHA `a66fbd7051e86bd4f2f8512ba204b588671147443d7ade0e5b43be97bf5155a9`;
`.json` SHA `c7a08412c18d46ee57aefc12759004ea6e913d070a3bd26ce9acb77a0895e319`;
`DECISIONI_AUTORE_7_3_REV3.md` SHA `235ab24ff254ed1e400033ff6ff65f302e91b3888001a9ec9a173095990e812a`;
`ADDENDUM_PIANO_STATISTICO_FINESTRE.md` SHA
`4a428d241981f4a70731398a67076df99f6c942f9536f6e82ac577cf6af06c05`;
`SPECIFICA_VERIFICA_SINTETICA_H3.md` SHA
`335fa789163c51cb36d6d557382eb8095e94e656d09ef5d3245a71e29d556272`.
Tutti i **1.647** file di `protocollo_finale/` al commit `9edf31e` coincidono byte per byte con
la worktree: nessuna differenza, nessun file mancante.

---

# A — Protocollo rev3

## A.1 Chiusura dei rilievi delle due review precedenti

`VERIFICA_PROTOCOLLO_FINALE.md` (`d0fe9d31…5261c`) e `VERIFICA_PROTOCOLLO_FINALE_claude.md`
(`2719650d…2990d`, ora **tracciato** in questa cartella).

| Rilievo | Stato | Evidenza di questa review |
| --- | --- | --- |
| R1 bloccante — batch non eseguibile | **chiuso** | Runner esistente e congelato: `run_final_batch.py`, `run_final_canary.py`, `materialize_final_target.py`, `harness/final_inventory.py`, `final_prompts.py`, `window_assignment.py`, `canary_marking.py`, `protocol_bnolf.py`, più 74 test nuovi tutti verdi. §7.1 lo dichiara parte del freeze. Dettaglio in B |
| R2 prima del tag — release non verificabili | **chiuso** | §2.1 dà coordinate immutabili di `evidence-v2` (release ID 388257324, commit dati `6d238929…`, asset, 62.185.472 byte) e la riverifica di `test-v1`. Ho **ricalcolato io** gli SHA dei tre archivi riscaricati: `ac1e7c0c…` (141.191.097 B), `242f689a…` (1.579.326 B), `16acf7c1…` (7.426.560 B): coincidono con `fault_runs/ARTIFACT_STORAGE.json`, la cui somma `bytes_verified` 150.196.983 è esatta |
| R3 nota — ordine di integrazione | **chiuso** in testo (§7.1 passo 2) e verificato meccanicamente (§Ordine di merge). Vedi però A1 |
| B1 bloccante — B-senza-LF non producibile | **chiuso** | `protocol_bnolf.py` al commit `a51ffd1`, SHA `b716200e6fdb34fa6dc0e7264612820306026f1851b188ef772016fc633fca8c`; `protocol.py` **intatto** (`791fa347…53d1e`, blob `f048b181` identico da `f0d0393` a `main` e a `9edf31e`). §3.1-bis dà token, definizione per sottrazione, file nuovo con SHA proprio, prova di diff. Verifica indipendente: ho reso i 2.244 prompt e **tutti i 148** B-noLF sono esattamente il B-LF di pari cella meno **un unico blocco contiguo di 406 byte** (`DECISION POLICY` + politica local-first), controparte B-LF trovata 148/148 |
| B2 bloccante — finestra del caso e input del lotto test | **chiuso** | §1.2 definisce l'assegnazione casuale bilanciata per posizione entro fault; committata in `7e497dc` (2026-09-17 20:44:49 UTC), **prima** di qualunque dato di test (archivi scaricati 21:13, estrazione 21:22). Riprodotta da me da soli identificativi: tabella `1ba7669a…836b` e file `c809e79d…a775`, **byte-identico** all'artefatto in worktree. §7.1 mette l'estrazione evidence come prerequisito a 0 chiamate; esempi locali, label space, agenti e derangement sono dichiarati dal manifest `84176888…` (SHA verificato sul file reale) |
| C1 — coppie tag↔file | **chiuso** | §2 cita ora i commit: `CRITERIA_FREEZE_rev002.json` a `ab43f0b2…` e `BASELINE_FREEZE_rev005.json` a `a0060586…`; entrambi ricalcolati e coincidenti |
| C2 — review pilot non tracciata | **chiuso** | `protocollo_finale/VERIFICA_PILOT_03_13.md` committata, SHA `944db3d7…abb2` invariato |
| C3 — stato di `test-v1` | **chiuso a metà** | `ARTIFACT_STORAGE.json` passa a `public_release_verified_by_redownload` senza inventare release ID, commit o timestamp (restano `null`); resta la contraddizione di A2 |
| C4 — marcatura canary ambigua | **chiuso** in testo (§6.5: primaria = giorno civile del piano §10.5, forense = intervallo, unione descrittiva); implementazione disallineata, vedi B2 |
| C5 — canary senza risposta valida | **chiuso** | §6.2–6.3 e implementazione: giorno né PASS né MARKED, slot consumato nei 70, nessuna rigenerazione, identità (`returned_model` **e** `system_fingerprint`) persistita per prompt nell'evento del giorno; tre test dedicati |
| C6 — `Q=0` sugli zero-token | **chiuso** da D7 | `Q=400` legato a prova zero-token, backoff 30/60/120/240 s fino a 900 s, STOP a 5 fallimenti tecnici consecutivi per servizio. Derivazione verificata: 8/156 = 5,128 %; 5,128 % di 6.802 = 348,8 ≈ 349. Vedi A4 |
| C7 — regola di maggioranza incompleta | **chiuso** da Q3/D4 | §7.3: tre esiti validi → maggioranza 2/3, altrimenti astensione per disaccordo, mai spareggio con repetition 1; meno di tre validi → `invalid_incomplete_triplet`, non corretto, distinto dalle astensioni |
| C8 — schedule sotto-determinata | **chiuso** | §7.1 fissa NumPy 2.2.6, `Generator.permutation(n)`, ordinamento come **tupla**, valori di `library_role`, definizione degli stage. Riprodotti da me: inventario `227e5e9c…df3f` e schedule `1acfc404…7819` |
| N1 — tabella canary assente dal JSON | **chiuso** | `PROTOCOLLO_FINALE_CANDIDATE.json` → `canaries.expected`: 10 voci con `prompt_text_sha256` e `expected_raw_response_sha256` (i 20 SHA). La tabella §6 del `.md` e `batch_finale/CANARY_ATTESI_7_4.json` coincidono su **tutti i 10 record e tutti i campi** (condizione, agente, SHA prompt, `abstain`, label, SHA risposta grezza) |
| N2 — rinvio a handoff non tracciato | **chiuso** | §7.2 cita `harness/ledger.py::reconcile_zero_token` (esiste, riga 2105) e `harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md`. Vedi però B3 |
| N3 — `X=100` inutilizzabile | **chiuso** da D6 | `TECHNICAL_VERIFICATION_QUOTA = 0`: lo stage esiste, non è legabile e nessuna richiesta è prenotabile su di esso; asserito in test |
| N4 — `d=7` e ore/giorno | **chiuso come regola** (§6.1: massimo sette giorni civili, non la finestra mobile; oltre → STOP). Aritmetica non esplicitata, vedi A5 |

## A.2 Conteggio rifatto da zero

Ricostruito dalle fonti (catalogo Q8 a `CATALOG_FREEZE.json`, proprietà 1:1 in
`AGENT_ASSIGNMENT.json`, sigillo 03.11: 64 primari + 8 Normal + 6 OOD + 11 scorte = 89), senza
leggere l'inventario del runner:

| Voce | Formula | Prompt | Richieste |
| --- | --- | ---: | ---: |
| Nucleo local-unseen | 8×8×7×3 | 1.344 | 4.032 |
| Nucleo local-seen | 8×8×1×3 | 192 | 576 |
| Nucleo Normal | 8×8×3 | 192 | 576 |
| Producer-swap | 4×8×7 (solo B-LF) | 224 | 672 |
| Ablation B-noLF | 8×8 + 4×3×7 | 148 | 444 |
| OOD | 2×3×8×3 | 144 | 432 |
| **Totale** | | **2.244** | **6.732** |

`6.732 + 70` canary = **6.802** base pianificata; `+ 400` retry = **7.202**. Coincide con §5.1,
con D9 e con `FINAL_BATCH_PROFILE` (`planned_maximum = hard_stop = Σ base_limits + retry_quota
= 7.202`). Delta dal totale storico 7.174: `−256 −16 −100 +400 = +28`, esatto. Superamento del
tetto storico 3.700: `6.802−3.700 = 3.102` (+83,84 %) e `7.202−3.700 = 3.502` (+94,65 %), esatti.
Il conteggio indipendente coincide inoltre con i conteggi resi: per blocco 1.728/224/148/144 e
per condizione A 624, B-LF 848, E-LF 624, B-noLF 148 (somma 2.244).

## A.3 T5

Ricalcolato dalle **120 righe** di `stability_records.jsonl` del gate, senza usare i valori
dichiarati: media **26,208619 s**, p95 per interpolazione lineare **36,660866 s** (sulle sole
119 righe con risposta ricevuta la media è 26,409324 s; una sola invalidità di trasporto,
1/120). Quindi `7.202 × 26,2086/3600 = 52,4318 h → ×1,20 = 62,9181 h` e
`7.202 × 36,6609/3600 = 73,3422 h → ×1,20 = 88,0106 h`, entrambi `< 168 h`. Coincide con §5.2 e
D9 alla quarta cifra. Il candidato dichiara correttamente che la seconda è una proiezione sulla
latenza p95 individuale e non il p95 del tempo complessivo.

## A.4 Addendum: correttezza delle derivazioni

Tutte verificate algebricamente, in modo indipendente:

1. **Hoeffding condizionale alla permutazione (§2).** Per 64 variabili indipendenti in
   `[−1,1]`, `exp(−2n²t²/Σ(b_i−a_i)²) = exp(−32t²)`, che è esattamente l'
   `exp(−64·t²/2)` scritto; da `exp(−32t²)=0,05` segue `t = sqrt(2·ln20/64) = 0,3059680…`.
   Corretta anche l'identità che rende la nulla condizionale uguale a quella sulla media
   uniforme: ogni posizione compare una volta entro fault, quindi
   `(1/64)Σ E[D_fr|π]` non dipende da π. Il **limite dichiarato** è giusto e non attenuato:
   con le 64 traiettorie fisse e casuale la sola assegnazione, i run dello stesso fault sono
   dipendenti per la permutazione senza reinserimento e la prova a N=64 non è design-based;
   l'alternativa a blocchi dà `t = sqrt(2·ln20/8) = 0,865406…`, coerente con «≈0,8654».
2. **`E[s²/n] = V + H/[n(n−1)]`.** Verificata: `E[Σ(X_j−X̄)²] = ((n−1)/n)Σσ_j² + H`, quindi
   `E[s²] = Σσ_j²/n + H/(n−1)` e `E[s²/n] = V + H/[n(n−1)]` con `V = Σσ_j²/n²`.
3. **`E[V_boot] = ((n−1)/n)·V + H/n²`.** Verificata: la varianza bootstrap ordinaria della
   media è `(1/n²)Σ(X_j−X̄)² = (n−1)s²/n²`, e
   `((n−1)/n²)·[Σσ_j²/n + H/(n−1)] = ((n−1)/n)V + H/n²`. Con `H=0` è 7/8 della vera varianza:
   la conclusione «il percentile a n=8 non è garantito conservativo» è corretta.
4. **Semiampiezza bilaterale ≈0,34.** `sqrt(2·ln(2/0,05)/64) = sqrt(2·ln40/64) = 0,339525…`,
   coerente con «≈0,34». Soglie Hoeffding H3: a α=0,05 `Dbar3 ≥ 0,3059680−0,125 = 0,1809680…`;
   a α=0,025 `Dbar3 ≥ 0,3395254−0,125 = 0,2145254…`, coerenti con i valori della specifica.

Le assunzioni e i limiti di §1 (fattori condivisi fissi condizionati, stream distinti,
deriva LLM non eliminata, correlazione residua entro fault non identificabile con una sola
osservazione per cella) sono dichiarati senza attenuazioni e ripresi nei threats.

## A.5 Segnaposto e SHA

**Nessun segnaposto residuo**: le occorrenze della parola sono tutte dichiarative
(«tutti i segnaposto documentali sono chiusi», «non restano segnaposto»).

SHA citati e **ricalcolati coincidenti**: i 28 riferimenti repository/tag di §2 verificabili
offline (piano consolidato, piano statistico al tag, budget rev.10, perimetro Q8, catalogo,
criteri rev002 al commit, soglie Normal, pseudolabel, baseline rev005 al commit, harness 03.10,
sigillo 03.11, schema insight, report e review pilot, esito tecnico pilot, i tre artefatti 7.2,
`protocol.py`, `sampling.py`, `B_LOCAL_FIRST_V1.txt`, derangement E, `protocol_bnolf.py`,
assegnazione finestre, FedAvg, ordine di presentazione, acquisizione 03.11, paper sections);
audit 03.11 `420a61eb…` e piano F5 `ef0b2852…` di §7.1; manifest di input congelato
`84176888…` e sorgenti `3099ad40…`; librerie `G_P` `1e97ddd3…` e `G_A` `c697e803…` **e i loro
SHA canonici** `c2469737…` e `f860063b…` (ricalcolati come SHA del JSON canonico di `library`);
template di remediation `4306c5da…`; script H3 `847bc294…` e Tango `25a648b9…`; inventario
`227e5e9c…`, schedule `1acfc404…`, mappa prompt `b8192003…`, tabella assegnazione `1ba7669a…`,
file assegnazione `c809e79d…`, manifest input test `67e7584a…`, suite Mac `50601686…`.

Non verificabili in questa review, e dichiarati tali: l'archivio `evidence-v2`
(`6d724ca2…`, esterno, documentato con asset e byte in `evidence/ARTIFACT_STORAGE.json`); il
template base del producer (`e7e80d59…`, attestato dalle evidenze T9 tracciate in `main`, non
dal file); il file `final_prompts.jsonl` (`f938604c…`) — vedi **A3**.

---

# B — Runner (`9e0e086` → `7925124`)

## B.1 `7e497dc` precede ogni accesso ai dati di test; assegnazione riprodotta

Catena e orari (UTC): `9e0e086` → `7e497dc` **20:44:49** → `1c70001` 21:08:52 → `a51ffd1`
21:31:05 → `7925124`. Gli archivi del lotto test (`fault_runs/test_batch/`, 150.196.983 byte
complessivi) hanno mtime **21:13** e l'estrazione `evidence/output_test/` **21:22**: nessun dato
di test era aperto quando l'assegnazione è stata congelata.

`build_window_assignment.py` legge **solo identificativi** dalla catena sigillata
SIGILLO → BATCH_AUDIT → piano CSV, autenticando i tre byte-set (`9bd02e90…`, `420a61eb…`,
`ef0b2852…`, tutti verificati da me su `main`), e non tocca segnali o evidence. Rieseguito nella
VM (NumPy 2.2.6, come l'ambiente di riferimento registrato nell'artefatto):
`assignment_sha256 = 1ba7669ae9715e4c6313b6746a05f8d390eeee2877d7f41cc554146c9e35836b` e file
`c809e79d2c03d74f4a5a37988eca809bda336468ab0060f794d3c214f9a6a775`, **byte-identico**
all'artefatto committato; 78 run assegnati, 11 scorte escluse, 9 gruppi da otto e 2 OOD da tre,
`useful_windows_check` PASS su 89 run e 712 finestre.

## B.2 Ledger: ramo pilot, quote, retry, `X=0`, hard stop

- **Ramo pilot invariato.** Il diff `f0d0393..a51ffd1` su `ledger.py` tocca il codice condiviso
  solo per parametrizzazione (`ACTIVE_STAGES` → `self.profile.stages`, `BASE_LIMITS[stage]` →
  `self.profile.base_limits[stage]`) con `profile="pilot"` come default, e **racchiude in un
  `if profile.name == 'pilot'`** la riserva condivisa `8r + t ≤ 15` e la regola del waiver sui
  trasporti oltre sette. `runtime.py` cambia di 16 righe: `journal=None` conserva
  `export_journal`. Conferma comportamentale: i **225 test preesistenti** danno esito identico,
  modulo per modulo, al commit base `f0d0393` e ad `a51ffd1` (vedi B.10).
- **Il pilot non è raggiungibile dal batch finale.** `_bind_profile` è create-once e
  `«a ledger with requests cannot adopt a new quota envelope»`: il ledger del pilot, che ha già
  richieste, **non può** essere aperto con profilo `final_batch`, e un ledger `final_batch` non
  può essere riaperto come `pilot`. Con il controllo di `pilot_id` e `require_pilot_ledger`,
  scrivere sul ramo pilot dai due entrypoint finali è impossibile per costruzione.
- **Quota per stage sulle sole richieste base.** `elif sum(r['stage'] == stage and
  r['retry_of'] is None for r in rows) >= limit` → un retry non consuma mai uno slot
  scientifico; asserito anche da `test_a_retry_never_consumes_a_scientific_stage_slot`.
- **Tetto retry proprio e cumulativo.** `quota_kind == 'transport'` conta su **tutte** le righe,
  non per stage: `used > profile.retry_quota (400)` → errore. `quota_kinds` del profilo finale è
  `{base, transport}`: `remediation`, `technical` e `requalification` non sono prenotabili.
- **`X = 0` non prenotabile.** `limit == 0` → rifiuto esplicito con rinvio a «declared protocol
  revision»; lo stage non è nemmeno legabile (`bind_stage` pretende `len(specs) == expected`).
- **Hard stop 7.202 atomico.** `_insert_intent` controlla
  `len(rows) + len(predecessors) >= profile.hard_stop` **e** `len(rows) >=
  profile.planned_maximum` dentro `_transaction()`, che apre `BEGIN IMMEDIATE` su una
  connessione con `PRAGMA synchronous=FULL`: la prenotazione è serializzata e durevole. Le
  costanti sono asserite in test (`7202 = 3×2244 + 70 + 0 + 400`). Vedi B6.

## B.3 Tabella D3 riga per riga

| Riga di §7.2 | Codice | Test |
| --- | --- | --- |
| errore tecnico con prova di non generazione → retry entro Q | solo `leaf['status'] == 'ZERO_TOKEN_PROVEN'` produce `retry_requests`; `_insert_intent` pretende originale `ZERO_TOKEN_PROVEN`, `_validated_reconciliation` e nessun retry preesistente | `test_proven_zero_token_is_retried_once_within_the_separate_quota` |
| timeout senza prova → sospendere, nessun reinvio | qualunque altro stato non terminale → `BatchStop` con rinvio a `ledger_cli reconcile-zero-token` | `test_uncertain_transport_is_suspended_and_never_resent_automatically` |
| risposta generata invalida o troncata → terminale | `leaf['status'] == 'COMPLETED'` → `progress.skip(); continue` | `test_terminal_invalid_response_is_never_replaced`, `test_an_invalid_canary_call_is_not_resent_when_the_day_is_retried` |
| risposta valida errata o astenuta → definitiva | stesso ramo `COMPLETED`: nessun percorso rigenera una risposta ricevuta | `test_complete_small_batch_records_every_slot_once` |
| STOP a 5 fallimenti consecutivi per servizio | `_consecutive_technical_failures` derivato dalla tabella `requests` in ordine di inserimento (persistente per costruzione), per `model`; `COMPLETED` azzera, `FAILED`/`ZERO_TOKEN_PROVEN` incrementano; blocco in `_prerequisites` | tre test: soglia, sopravvivenza alla riapertura del ledger, reset su completamento |
| backoff 30/60/120/240 → 15 min | `min(30·2^(n−1), 900)` | `test_retry_backoff_increases_and_is_capped` |

**Nessun percorso rigenera una risposta ricevuta**: confermato. Il contatore dei 5 è
persistente, per servizio e comprende i retry, come chiesto.

## B.4 Canary

Barriera: `require_canary_ok` è invocata prima del ciclo **e dentro il ciclo, prima di ogni
richiesta**; verifica assenza di STOP, almeno un giorno passato, meno di due giorni marcati e
PASS registrato per il giorno del lotto. `_prerequisites` la duplica a livello di ledger.
Identità: `returned_model` **e** `system_fingerprint` sono confrontati su ogni chiamata canary e
**persistiti per prompt** nell'evento del verdetto (`record_canary_day(..., identity=…)`), non
solo controllati in memoria; `record_canary_stop` crea `canary_stop:identity:<day>`.
`CANARY_MAX_DAYS = 7` e `CANARY_DAILY_CALLS = 10` sono imposti dal ledger, il verdetto è
create-once e si chiude solo su dieci chiamate complete. Il secondo giorno marcato genera lo
STOP nello stesso evento. Tabella §6 e `CANARY_ATTESI_7_4.json`: identiche su tutti i campi.
Rilievi B1 (giorno dichiarato) e B2 (maschere).

## B.5 Schedule e resume

`load_schedule` **ri-deriva** la schedule dal generatore committato e confronta l'intera lista
di `logical_id`, oltre a seed e namespace; `load_prompts` ricontrolla l'hash di ogni prompt sui
suoi byte; `load_target` autentica config, schedule, prompts e attese canary contro il
descrittore. Il resume è esplicito (`--resume`, altrimenti rifiuto se la passata ha già
richieste), scorre la **stessa** schedule persistita, salta gli slot terminali e non ne riusa
mai uno: il retry è un tentativo figlio della stessa richiesta logica
(`retry_of`), e `_insert_intent` rifiuta i duplicati logici
«across restart/alias/directory». La passata 2 non parte prima della chiusura della 1
(`outcome:final_batch_r1` richiesto). Riprodotti da me: inventario
`227e5e9c…df3f` e schedule `1acfc404…7819`, con un solo
`Generator(PCG64(20260913))` e `permutation(2244)` per passata 1→2→3, mai reinizializzato.

## B.6 `B-noLF`

Sottrazione letterale del solo blocco di politica, con tre controlli nel codice (una sola
occorrenza del blocco; differenza di byte pari esattamente alla lunghezza del blocco;
ricomposizione che deve restituire il B-LF originale) e `verify_frozen_renderer` che fallisce
se `protocol.py` non è più `791fa347…`. `protocol.py` è **byte-identico** su tutta la catena e su
`main`. Verifica indipendente sui byte resi: 148/148 corretti, blocco rimosso di 406 byte,
zero prompt di ablazione che conservano `DECISION POLICY`.

## B.7 Estrazione evidence del lotto test

`extract_test_lot_evidence.py` importa `extract_evidence` e ne riusa
`load_frozen_api`, `EXPECTED_BASELINE_SHA256`, `validate_r2_guard`,
`load_development_baseline`, `resolve_source`, `_write_json`, `_write_csv`, le costanti della
geometria (`ONSET_H=25`, `END_H=65`, `WINDOW_H=5`, `SIGNATURE_DIMENSION=697`). Il ciclo che
produce l'unità è **identico riga per riga** a quello di 03.6, chiave di ordinamento e
formattazioni comprese: le otto finestre sono calcolate su tutto l'orizzonte congelato e solo
dopo si conserva quella assegnata, quindi **a parità di run e finestra i quattro file dell'unità
sono byte-identici** a quelli che 03.6 produrrebbe; differiscono soltanto il prefisso del nome
(`EVT-` invece di `EVD-`) e la numerazione. Nessun contenuto di test entra in una scelta: la
selezione è la sola assegnazione, i controlli per-run leggono metadati del manifest (stato,
conteggio e geometria delle finestre) e ogni fallimento è **registrato** in `not_extracted`, mai
sostituito. Prima di aprire i dati il driver riconferma che l'assegnazione committata coincide
con il generatore. Risultato registrato: 78/78 unità, `not_extracted = []`, leakage PASS,
`INPUT_MANIFEST_TEST_7_4.json` `67e7584a…` (ricalcolato sul file reale).

## B.8 Rendering indipendente dei prompt

Non un campione: ho reso **tutti i 2.244** prompt nella VM, con il renderer congelato, il
manifest `84176888…`, le sorgenti `3099ad40…` e le due librerie reali, e la **mappa canonica
identificativo→SHA coincide esattamente**:
`b819200396da480d3ed9d4aa8f6b6aac8c135d97f0876b734a9b607b75736489`. Coincidono anche, ricavati
dagli stessi byte: 624 celle appaiate B↔E con **0** differenze fuori dal blocco `PEER INSIGHTS`
e 0 coppie identiche; 148 prompt di ablazione con 0 residui di politica; i conteggi per blocco e
per condizione; l'ordine di presentazione accettato delle nove label.
Lo SHA del **file** `final_prompts.jsonl` non è riproducibile in questa review perché senza lo
snapshot del tokenizer le righe non portano `prompt_tokens`: è la sostanza del rilievo **A3**.

## B.9 Suite

Rieseguita per intero nella VM Linux, modulo per modulo: **299 test, 3 failure, 49 error,
22 skip**, esattamente i numeri dichiarati in `REPORT_7_4_FIX.md` §6. I **74 test nuovi del
runner passano tutti**: `test_final_batch` 33, `test_bnolf` 12, `test_window_assignment` 11,
`test_final_prompts` 10, `test_test_lot_evidence` 8. Tutti i non-pass stanno in moduli
preesistenti.

Non li accetto per somiglianza: ho **estratto il commit base `f0d0393`** in una directory
separata e rieseguito la stessa suite. Esito per modulo **identico**, non-pass compresi
(`c01_c03` 1F/10E, `d01_replay` 0 test/1E, `d02` 1E, `d03` 2E, `d04` 2E, `d9` 7E,
`d9_corrections` 10E, `harness_offline` 1E, `history_reconciliation` 1E, `revisions` 2F/14E) —
225 test preesistenti, 3F/49E/22S in entrambi i casi. Le commit del runner quindi **non
introducono nessun non-pass** e non ne risolvono nessuno.

Cause, tutte ambientali e verificate a mano: 42 dei 49 error derivano da `jsonschema` troppo
vecchio nella VM (`cannot import name 'Draft202012Validator'`) e dalle cascate a valle; gli
altri da worktree che esistono solo sul Mac
(`git -C /Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate rev-parse` esce 128;
`/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/…` assente).

**306 contro 299.** Confermato per costruzione: `test_d01_replay.py` contiene **una sola classe**,
`ReplayPrerequisites`, con **esattamente sette** metodi `test_D01_*`; il suo `setUpClass`
solleva nella VM e `unittest` registra un errore di classe senza contare i metodi
(`Ran 0 tests … errors=1`, osservato). `306 − 7 = 299`. Stessa suite, una classe non eseguibile
dove manca la sua worktree di riferimento. Il log del Mac
(`batch_finale/SUITE_MAC_a51ffd1.txt`) ha SHA `50601686bc4ecd160820d0b2413eeecab63511b21477b579a760dd1c30f4b373`,
identico al blob committato in `7925124`, e riporta `Ran 306 tests in 485.662s / OK`; in testa
contiene la coda di una prima esecuzione interrotta, come dichiarato.
`7925124` non tocca codice: modifica `REPORT_7_4_FIX.md` e aggiunge il log.

---

# C — Verifica sintetica H3

## C.1 Provenienza e ordine dei commit

Tango viene dal piano congelato: tag `studio2-fase03-piano-statistico-frozen-001` → commit
`11f504b2bf45a39c1bc4746952f50d58c5022743`; `piano_statistico/design_resolution.py` blob
`1691e3b10d8a421eee66d69a33f612eb96b432c1`, SHA `25a648b9…613` — tutti e tre verificati, e il
file è byte-identico anche a `9edf31e` e a `main`. `b465f90` contiene **soltanto** record
pre-simulazione, script (`847bc294…`), manifest (`51711d6e…`) e test: **zero file di
risultato**; i risultati arrivano con `d0cfeab`. L'ordine «pre-simulazione prima dei risultati»
è quindi dimostrato dal contenuto dei due commit, non solo dalla loro sequenza.
`MANIFEST_SHA256.json` copre 1.631 file: **tutti verificati, 0 mancanti, 0 discordanti**.

## C.2 Implementazione di Tango = piano congelato

Le due funzioni nello script sono **matematicamente identiche** a quelle del blob congelato
(stessa radice positiva `2N p21² − [(b+c) − δ₀(2N − b + c)] p21 − c δ₀(1−δ₀) = 0`, stessa
varianza `N(2p21 + δ₀(1−δ₀))`, stesso `NaN` su varianza non positiva): differiscono solo per il
nome delle variabili locali e per i default. Orientamento corretto: `tango_score_z(plus, minus)`
con `b` = coppie B corretto/A errato, `δ₀ = −0,125`, rifiuto per `Z > z₀,₉₅`. I due valori di
riferimento pubblicati sono riprodotti analiticamente: con `b=c=0`, `p21 = 0,125`,
`Var = 7` e `Z = 8/√7 = √(64·0,125/0,875) = 3,023716…`; con `b=0, c=8`, `Z = 0` esatto.
La seconda via dello script (massimizzazione numerica 1-D della verosimiglianza vincolata,
con i casi degeneri 0, N, 8 da un lato e casi interni) è una verifica indipendente legittima.
Vedi la nota C1.

## C.3 Marginali, Δ3, calibrazione ICC, contabilità: rifatti da zero

Ho **riscritto** da solo, dalla specifica, gli assi, le formule di §2, la calibrazione di §3, la
statistica di Tango e le soglie di Hoeffding, senza importare il loro script, e ho ricostruito
la griglia:

- **1.620** scenari target, **108** punti al bordo a ICC=0, 540 al bordo, 1.080 di potenza;
- per ogni scenario: probabilità finite in [0,1], somma 1 entro 1e−12, `media d_fj = d` e
  `media delta_fj = Δ3` entro 1e−12, `|delta_fj| ≤ d_fj`: **tutti superati**, nessun clipping;
- **24** scenari `INFEASIBLE`, con gli **stessi indici** del loro `SCENARI_INFEASIBLE.csv`
  (631–634, 646–649, 661–664, 766–769, 781–784, 796–799): tutti nel blocco Δ3=0, quindi
  **nessun punto al bordo e nessun target ICC=0 è escluso**. La causa è verificata: per
  `d=0,15, a=1` i primi quattro fault hanno `d_fj = 0`, tutte le celle degeneri, `c_f` non
  definito, quindi solo ρ=0 è applicabile;
- la calibrazione della miscela è corretta: con gate Bernoulli(λ_f) fra «uniformi indipendenti»
  e «uniforme condiviso» le marginali sono conservate esattamente e la covarianza è
  `λ_f · Cov_shared`, quindi `λ_f = ρ/c_f` con `0 ≤ λ_f ≤ 1`; `E[X_iX_j]` sotto uniforme
  condiviso è la somma di `x·y·|I_i(x) ∩ I_j(y)|` sugli intervalli di CDF, con
  `Var = d − μ²`: coincide con la mia implementazione indipendente;
- inverse CDF nell'ordine −1, 0, +1, come da specifica;
- **contabilità delle repliche**: 1.596 scenari fattibili × 100.000 = **159.600.000** repliche,
  **0 errori numerici**, nessuna replica scartata dal denominatore. Coincide con `SUMMARY.json`.

## C.4 Replay: non solo gli estremi, l'intera tabella

Con il mio codice, il loro consumo RNG dichiarato
(`PCG64(SeedSequence([20260917, scenario_index]))`, batch 10.000, gate `(batch,8)` →
indipendenti `(batch,8,8)` → condivise `(batch,8)`, con consumo anche delle estrazioni non
selezionate) e NumPy 2.2.6 invece di 2.5.2, ho rieseguito **tutti i 1.596 scenari fattibili** e
riprodotto **ogni cella** della tabella di robustezza, indici degli scenari peggiori compresi:

| Procedura | ICC 0 | ICC 0,05 | ICC 0,10 | ICC 0,20 | ICC 0,40 | max ICC con tutti ≤0,055 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Tango H3 | 0,05128 (380) | 0,07976 (451) | 0,10565 (412) | 0,14699 (363) | 0,21383 (104) | **0** |
| Hoeffding H3 | 0,00505 (455) | 0,01533 (416) | 0,02696 (407) | 0,05143 (418) | 0,09651 (419) | **0,20** |
| Hoeffding H1/H2 | 0,00503 (945) | 0,01426 (1041) | 0,02542 (952) | 0,05025 (953) | 0,09696 (1049) | **0,20** |

Punti applicabili: 108 a ogni ICC per H3; 108 a ICC=0 e 102 agli ICC positivi per H1/H2 —
coincide, e le 6 famiglie che perdono gli ICC positivi sono esattamente quelle dei 24
`INFEASIBLE`. Il **punto peggiore al bordo** è riprodotto al singolo rifiuto: scenario **380**
(Δ3=−0,125, d=0,60, a=1, b=0,5, pattern tempo/interazione, ICC=0), **5.128/100.000**,
`phat = 0,05128`, `MCSE = 0,0006974981118254013`, identico a `SUMMARY.json` alla sedicesima
cifra. Tutti i **108/108** punti al bordo a ICC=0 hanno `phat ≤ 0,055`; il massimo è 0,05128,
a 0,00372 dal limite e a circa 5,3 MCSE. H1 e H2 coincidono e non sono contati come simulazioni
indipendenti.

## C.5 Esito §5 — che questa review rende vincolante

**TANGO MANTENUTO.** La regola di uscita chiede tre cose e le ha tutte: i 108 punti al bordo a
ICC=0 con `phat ≤ 0,055` (verificato indipendentemente, massimo 0,05128), implementazione
verificata (identità matematica con il blob congelato e riproduzione integrale) e review OK.
Il `PENDING` del report e di D11 era corretto **in assenza** di questa review; ora decade.
Restano vere, e vanno riportate senza attenuazioni, le limitazioni che il candidato già
dichiara: livello e FWER completo **approssimati**, non garantiti da una verifica finita; la
verifica è **locale a H3** e non simula il FWER congiunto H1→H2→H3; il fallback Hoeffding resta
quello deciso e richiede anch'esso l'indipendenza fra run.

**Robustezza all'ICC riportata correttamente.** Il massimo ICC testato con tutti i punti ≤0,055
è **0 per Tango H3** e **0,20 per Hoeffding H3 e H1/H2**: §9.2 lo riporta così, dice che H3 vale
sotto indipendenza fra run ed è sensibile anche a piccola correlazione entro fault, che H1/H2
sono descrittivamente robusti fino a correlazione moderata, che ciò non cambia la procedura e non
garantisce il FWER; D11 e §10 Q2 dicono lo stesso; l'addendum §1 e §3 dichiarano le assunzioni
e i limiti. **Nessuna attenuazione** e nessun uso dello stress per scegliere la procedura.

---

# Rilievi

**A1 — prima del tag — l'evidenza che chiude il punto G resterebbe fuori da `main`.**
§7.1 passo 2 e la riga «Runner finale 7.4» di §2 integrano rem6 **fino ad `a51ffd1`**, ma il log
della suite sul Mac che chiude il punto aperto G è committato solo in `7925124`. Integrando fino
ad `a51ffd1`, `SUITE_MAC_a51ffd1.txt` non è raggiungibile da `main`: è la stessa classe di
difetto del C2 già chiuso. Estendere l'ordine di integrazione a `7925124` (che non tocca codice)
oppure dichiarare esplicitamente dove vive quell'evidenza.

**A2 — prima del tag — C3 è chiuso solo su uno dei due documenti.**
`fault_runs/ACQUISIZIONE_OK_ESECUZIONE_03_11.md` (SHA `ddd986c1…`, citato in §2 ed evidenza di
S13) dice ancora «03.11 verificata localmente, **non pubblicata**» e «fino ad allora 03.11 non e
pubblicata», mentre `fault_runs/ARTIFACT_STORAGE.json` sullo stesso commit registra `test-v1`
come `public_release_verified_by_redownload`. Il rilievo C3 nominava entrambi i file; solo uno è
stato aggiornato. Due riferimenti congelati di §2 si contraddicono.

**A3 — prima del tag — §2 fissa lo SHA di un artefatto che non esiste.**
La riga «Prompt finali» pinna `final_prompts.jsonl` con SHA `f938604c…`, ma quel file non esiste
da nessuna parte: `batch_finale/build/` è in `.gitignore` e assente dal disco, e
`evidence/output_test/` è ignorata. Nessuno può autenticarlo, e la sua riproduzione dipende
dalla presenza dello snapshot del tokenizer (senza il quale le righe non portano
`prompt_tokens`, come ho constatato). La **mappa canonica** `b8192003…`, che è l'oggetto
scientificamente vincolante, è invece riproducibile e l'ho riprodotta esattamente. Conservare
l'artefatto con un record di conservazione, oppure dichiarare quello SHA un prodotto di 7.4-MAT
e togliere il pin da §2.

**B1 — prima del tag — il giorno civile è dichiarato dall'operatore e non è mai confrontato con
l'orologio.** In `run_final_batch.py` e `run_final_canary.py` l'opzione `--day` entra senza
alcun controllo: `require_canary_ok` usa `day or rome_day(now)`. Tutta la barriera di §6/D8
poggia quindi su un valore dichiarato: un canary passato per il giorno X e un lotto lanciato con
`--day X` un giorno diverso soddisfano il controllo. L'opzione serve (attraversamento della
mezzanotte), ma va resa verificabile: persistere **sia** il giorno dichiarato **sia**
`rome_day(now)` osservato nell'evento e nei record, e rifiutare quando differiscono fuori dal
caso di mezzanotte. Oggi la discrepanza è solo ricostruibile a posteriori dai timestamp.

**B2 — prima del tag — `canary_marking` presenta l'unione come la maschera, rev3 la vuole
descrittiva.** Il modulo dichiara «the rule applied here is the **union** of the two» ed espone
`marked_request_ids` = unione, `interval_only` e `civil_day_only`; la maschera **primaria** del
piano §10.5 (tutte le chiamate del giorno civile marcato) non è un campo proprio ed è solo
derivabile per differenza. §6.5 rev3 stabilisce l'opposto: primaria la maschera del giorno,
forense l'intervallo, unione descrittiva e separatamente etichettata, e vieta che l'unione
«sostituisca tacitamente la sensibilità del piano». Un consumatore a valle che prende
`marked_request_ids` fa esattamente ciò che §6.5 vieta. Nominare i campi
(`primary_mask_request_ids` §10.5, `forensic_mask_request_ids` §6.5, unione descrittiva) e
allineare la docstring. È analisi a valle, non esecuzione: non blocca.

**B3 — prima del tag — il batch finale non scrive alcun journal, e il contratto dichiarato
vincolante ne parla.** `run_final_batch.run_pass` passa a `execute_request` un
`journal=append_journal` che è un **no-op** (`pass`), e il canary un `lambda *_: None`, mentre
entrambi continuano a costruire `journal_path` e il commento afferma che «the journal is an
append-only forensic mirror». Non viene scritta una riga. `CONTRATTO_ESECUZIONE_E_RIPRESA.md`,
che §7.2 nomina come fonte operativa «nella versione del runner da rivedere», è **byte-invariato**
dalle commit del runner e contiene clausole sul journal (proiezione aggiornata durante lo stadio;
«stadio chiuso, file finale assente → `--resume` rigenera la proiezione»; «il journal espone
separatamente request, response e transport_invalidity»). Poiché SQLite è la fonte autorevole e
il runner scrive comunque `{stage}_call_log.jsonl` e un record durevole per richiesta, non c'è
perdita di stato: c'è una clausola contrattuale non implementata e un commento che descrive
qualcosa che non avviene. Scrivere il journal in append per la singola richiesta, oppure
aggiungere al contratto una clausola esplicita per il batch finale che nomini la proiezione
effettiva, e togliere `journal_path` se non si usa.

**B4 — nota — lo STOP di identità del canary è classificato per sottostringa.**
`run_final_canary` decide se registrare `canary_stop:identity:` con
`if "identity" not in str(exc) and "suspended" not in str(exc): raise`. Un cambio di formulazione
del messaggio in `runtime.execute_request` farebbe perdere l'evento durevole; la campagna si
fermerebbe comunque attraverso la sospensione non riconciliata, quindi il comportamento è
fail-closed, ma la classificazione dovrebbe poggiare su un tipo o un campo, non sul testo.

**B5 — nota — il fallback di `rome_day` sbaglia i confini dell'ora legale.**
Senza `zoneinfo`/tzdata, `canary_marking.rome_day` usa come confini fissi il 31 marzo e il 27
ottobre; nel 2026 sono il 29 marzo e il 25 ottobre. Fra il 25 e il 27 ottobre il fallback
attribuirebbe il giorno civile sbagliato, e il giorno civile è l'unità della barriera e della
maschera primaria. Il percorso è raggiungibile solo dove tzdata manca, ma il rimedio è una riga
(ultima domenica di marzo/ottobre) o un rifiuto esplicito in assenza di tzdata.

**B6 — nota — il tetto totale non è esercitato da alcun test.**
`test_technical_verification_is_closed_at_x_zero` asserisce `planned_maximum = hard_stop = 7.202`
e l'identità `Σ base_limits + retry_quota = 7.202`, e l'esaurimento **per stage** è eseguito; il
rifiuto sul **totale** 7.202 non viene mai percorso. Un test che porti il profilo al limite
complessivo chiuderebbe il punto.

**B7 — nota — i pin dipendono dalla versione di NumPy, e l'inventario cita ancora `e0db132`.**
`schedule_artifact` e l'artefatto dell'assegnazione includono `numpy_version` nel payload
hashato: `227e5e9c…`, `1acfc404…` e `c809e79d…` sono riproducibili solo sotto NumPy **2.2.6** —
che è l'ambiente di riferimento dichiarato in §7.1 e registrato negli artefatti (il Mac ha la
stessa versione), quindi la cosa è coerente, ma un aggiornamento futuro cambierebbe lo SHA
senza cambiare l'ordine: va spiegato, non sovrascritto, come §7.1 già prescrive. Inoltre
`inventory_artifact` fissa `protocol_reference: "PROTOCOLLO_FINALE_CANDIDATE.md e0db132 §4, §5,
§7.1"` **dentro** il payload hashato: cita ancora il candidato rev1 e non è aggiornabile senza
cambiare il pin. I contenuti di §4 e §5 richiamati non sono cambiati (2.244 e 6.732 sono
identici in rev1 e rev3), quindi è imprecisione documentale, non un errore di conteggio.

**A4 — nota — «arrotondamento prudenziale» a 400 è un arrotondamento per difetto.**
8/156 = 5,128 %; su 6.802 slot sono 348,8 ≈ 349 attesi; +15 % dà 401,35, arrotondato **a
scendere** a 400. Il tetto è quindi marginalmente più stretto del 15 % dichiarato: corretto come
cap, impreciso come aggettivo.

**A5 — nota — N4 resta vero e l'aritmetica non è scritta.**
§6.1 fissa la regola (massimo sette giorni civili, non la finestra mobile; oltre → STOP), ma il
candidato non dice che con la proiezione p95 di 88,0 h su sette giorni servono ≈12,6 h/giorno di
esecuzione sequenziale (≈9,0 h/giorno sulla media): oltre il settimo giorno la quota canary
ferma il batch. Una riga in §5.2 o §6 eviterebbe di scoprirlo in esecuzione.

**A6 — nota — le alternative illustrative di §1.2 si riproducono solo a base dichiarata.**
Le 377 h corrispondono a portare a otto finestre **il solo nucleo** (41.472 chiamate) lasciando
swap, ablation, OOD, canary e X ai valori a una finestra; «circa 106/148 h» per due finestre si
riproduce come ≈105/147 h da 2 × 7.202. Sono motivazioni, non numeri vincolanti, e tutti i
numeri vincolanti (6.802, 7.202, 62,918 h, 88,011 h) si riproducono esattamente; conviene però
dichiarare la base, perché così com'è il lettore non ritrova le cifre.

**C1 — nota — lo script H3 copia Tango invece di importarlo, e non verifica gli SHA che dichiara.**
`PLAN_FILE_SHA256`, `TANGO_FILE_BLOB` e `TANGO_FILE_SHA256` sono costanti mai controllate a
runtime, e le due funzioni sono trascritte anziché importate da `design_resolution.py`. Ho
verificato io che la trascrizione è matematicamente identica al blob congelato e che i due valori
di riferimento pubblicati sono riprodotti, quindi il risultato regge; ma la provenienza è
documentale e nulla impedirebbe a una futura revisione del piano di divergere in silenzio.
Un controllo dello SHA del file, o l'import diretto, renderebbe il legame automatico.

**N — nota minore.** Integrando rem6, `fault_runs/.gitignore` resterà con `/test_batch/`
duplicato: `main` lo ignora già da `ea90761` e `a51ffd1` ha aggiunto la stessa riga. Innocuo
per la semantica di `.gitignore`, da ripulire quando conviene.

---

# Ordine di merge

Confermato, e verificato meccanicamente sull'object database, non solo sulla documentazione:

1. **rem6 in `main`, fino a `7925124`** (vedi A1). Base di merge `540df7b`. Il ramo cambia 39
   file, `main` ne ha cambiati 691 dalla stessa base; l'**unica** sovrapposizione è
   `studio2/fase03/fault_runs/.gitignore`, e il merge a tre vie di quel file **riesce senza
   conflitto** (esito verificato con `git merge-file`, uscita 0; resta la riga duplicata della
   nota N).
2. **poi il branch del protocollo** (`9edf31e`). Base di merge `ea90761`, che è già in `main`.
   Il branch cambia 1.648 file e l'intersezione con i 39 di rem6 è **vuota**: nessun conflitto.
   Fuori da `protocollo_finale/` tocca un solo file, `fault_runs/ARTIFACT_STORAGE.json`, e il
   diff è esattamente il cambio di stato di `test-v1` più i fatti della riverifica, con
   `release_id`, `release_commit` e `published_at_utc` lasciati `null`: nessun dato inventato,
   come §2.1 dichiara.
3. **poi il tag annotato** sul commit in `main`, su mandato dell'autore.
4. **poi 7.4-MAT.** I tre prerequisiti di runtime, la configurazione eseguibile, il contratto di
   generazione e la copia autenticata dei dieci prompt canary restano dopo il tag, come D10.

`c284523` e `f0d0393` (librerie 7.2) stanno sullo stesso ramo rem6 e arrivano in `main` con il
passo 1: la loro raggiungibilità, che era R3, si risolve lì.

# Parere sul tag

Il nome `studio2-fase03-protocollo-finale-frozen-001` è conforme alla serie esistente e resta
`001`: nessun candidato è mai stato taggato.

**Non va creato su `9edf31e`.** Va creato, annotato, sul commit della revisione che chiude A1,
A2 e A3, quando quel commit e rem6 (fino a `7925124`) sono in `main`, e dopo una nuova review
dei **soli delta** — che per A1–A3 e B1–B3 è un controllo breve e circoscritto. Nessuno dei
rilievi è bloccante: il contenuto scientifico, contabile e di riproducibilità dei tre oggetti
regge, i due rilievi bloccanti della review precedente sono chiusi con evidenza, ed è la prima
volta che conteggio, assegnazione, inventario, schedule, i 2.244 prompt e l'intera griglia H3
sono stati riprodotti indipendentemente byte per byte e rifiuto per rifiuto.

Nessun merge, tag, materializzazione o chiamata è stato eseguito da questo incarico.
