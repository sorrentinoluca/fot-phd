# 7.4-FIX — finestre, `B-noLF`, retry/STOP, canary

Data: 2026-09-17. Branch `codex/studio2-riconciliazione-stop-contabile`, base `9e0e086`.
Sostituzione di modello dichiarata: mandato indirizzato a `gpt-5.6-sol`, eseguito da
`claude-opus-5` (Claude Cowork). **Nessuna chiamata a modelli, nessuna materializzazione,
nessun push/merge/tag.** `api_key.json` e `server_enea.json` non letti. Pilot e server 27B
intoccati. Normativa applicata: `DECISIONI_AUTORE_7_3_REV2_2026-09-17.md`
(`535939de1d8c1e6f8185fd838a6bd20caca85b5f09c7908f679f251761aaccb2`), D1–D4.

## Tocca quota / accounting / ledger: **SÌ** — scatta la review `b567`

In `harness/ledger.py`, **solo sotto profilo `final_batch`** (il ramo `pilot` è invariato
riga per riga, e un ledger scritto prima di 7.4 resta per definizione un ledger pilot):

1. `LedgerProfile` acquisisce `retry_quota` e `consecutive_failure_stop` (default 0: il
   pilot non cambia). `FINAL_BATCH_PROFILE` ammette il quota kind `transport` accanto a
   `base`, con `retry_quota=400` e soglia 5; `planned_maximum` e `hard_stop` passano da
   6.902 a **7.302**. La dichiarazione create-once del profilo registra i due nuovi campi.
2. `_insert_intent`: la quota per stage conta le sole richieste **base** (`retry_of IS
   NULL`), così un retry non consuma mai uno slot scientifico; i retry hanno il proprio
   tetto cumulativo; il vincolo di riserva del pilot `8r+t<=15` (e il limite `t>7`) è
   circoscritto al profilo `pilot`.
3. `_prerequisites`: cinque fallimenti tecnici consecutivi sullo stesso servizio bloccano
   ogni ulteriore chiamata del batch (campagna sospesa, risultati e richieste conservati).
4. Nuovi `_consecutive_technical_failures` / `technical_failure_stop` / `attempts`.
   Il contatore è **derivato dalle righe del ledger**: è persistente per costruzione, non si
   azzera riavviando, rinominando o riaprendo; si azzera solo con una chiamata che riceve
   risposta. Retry inclusi.
5. `record_canary_day` accetta e persiste l'identità osservata (`returned_model` **e**
   `system_fingerprint`) per ciascuno dei dieci prompt del giorno.
6. `snapshot()` espone `retry_quota`, `retry_quota_used`, `consecutive_technical_failures`,
   `consecutive_failure_stop`.

`harness/logging_v1.py`: il contratto §8.7 ammette il token `B-noLF` (costante `CONDITIONS`).
L'accounting del tokenizer 122B **non cambia**: stesso `TokenizerAccountingGuard`, stesso
`execute_request`, guardia applicata a tutte le chiamate.

## Nuovo totale massimo dichiarato

**7.202 chiamate** (valore di FIX-2; in FIX-1 era 7.302 con `X=100`) = 6.732 scientifiche +
70 canary + 0 `X` + **400** di quota retry separata. Il 400 viene dal tasso del pilot, 8
fallimenti pre-generazione su 156 richieste (5,13 %): su 6.802 chiamate pianificate l'attesa
è ~349, e 400 lascia ~15 % di margine restando un ordine di grandezza sotto la campagna.
T5 a 7.202: 52,4 h alla media e 73,3 h al p95, cioè **62,9 h** e **88,0 h** con il margine
del 20 %, contro `W` = 168 h. Il margine temporale non crea quota.

## I quattro SHA

| Artefatto | SHA-256 | Stato |
| --- | --- | --- |
| Assegnazione finestre (tabella) | `1ba7669ae9715e4c6313b6746a05f8d390eeee2877d7f41cc554146c9e35836b` | committata |
| `batch_finale/ASSEGNAZIONE_FINESTRE_7_4.json` (file) | `c809e79d2c03d74f4a5a37988eca809bda336468ab0060f794d3c214f9a6a775` | committata |
| Inventario | `227e5e9c797dbfd8be746d85b77298f5dfb091846dc301f0b2e31ea1dbc6df3f` | **invariato** |
| Schedule | `1acfc4044c53f113016ed0bfab58863291a9060a9edc9abadb68a21d30687819` | **invariato** |
| Manifest di input del lotto test | `67e7584a80d743efc06edc4c97019c20803cc4787c1d70c8d924ad23736612e8` | prodotto in FIX-2 |

Lo SHA della schedule non cambia perché il token `B-noLF` era già quello enumerato
dall'inventario 7.4-PREP: D2 ha confermato il token, non introdotto un valore nuovo.

## Cosa chiude ciascun rilievo

| Rilievo | Chiusura |
| --- | --- |
| **R1** (`VERIFICA_PROTOCOLLO_FINALE.md`) — manca l'esecutore finale | Chiuso da 7.4-PREP `9e0e086` e completato qui: barriera canary→lotto per giorno civile (`require_canary_ok(ledger, day)`, verificata prima di **ogni** richiesta), identità canary persistita, STOP di §7.2 con la contabilità di D3. |
| **B1** — `B-noLF` non producibile dal renderer congelato | Chiuso. `protocol_bnolf.py` è una revisione tracciata con SHA proprio; `protocol.py` (`791fa347…`) non è modificato in luogo ed è verificato fail-closed a ogni render. `B-noLF` è definito per sottrazione — prompt B-LF meno il blocco `DECISION POLICY`, nient'altro — e la sottrazione è verificata sui byte: rimozione letterale unica, reinserimento che ricostruisce esattamente B-LF, delta in byte pari al blocco. Diff allegato da `protocol_bnolf.policy_diff`. `CallRecord` ammette il token. |
| **B2** — quale finestra è «il caso», e input del lotto test inesistente | Prima metà chiusa: assegnazione D1 congelata e committata **prima** di aprire i dati (commit separato `7e497dc`, precedente a ogni lavoro sull'input). Seconda metà: strumento pronto e testato, esecuzione bloccata dalla release non scaricata (punto A). `evidence/extract_test_lot_evidence.py` dichiara che esempi locali, label space, agenti e derangement restano quelli del manifest congelato `84176888…`. |
| **C4** — marcatura canary ambigua | Chiusa come **dato derivabile**: `harness/canary_marking.py` + `query_canary_marking.py` calcolano l'**unione** fra l'intervallo §6.5 e l'insieme del giorno civile §10.5, in sola lettura sui timestamp del ledger. Nessun record terminale viene riscritto. Query SQL equivalente inclusa nell'artefatto. |
| **C5** — canary senza risposta valida | Chiusa secondo D3: risposta ricevuta ma invalida = fallimento registrato, mai rigenerato; il giorno non si chiude, resta senza verdetto, e la barriera §6 impedisce qualunque lotto scientifico in quel giorno finché l'autore non decide. Fallimento di trasporto: prova di zero token → retry in quota; senza prova → sospensione e riconciliazione. Le chiamate canary consumano i 70; i retry la quota separata. |
| **C6** — `Q=0` sugli zero-token | Chiusa da D3 e implementata: retry solo contro prova di zero token generati collegata alla richiesta (`reconcile_zero_token`), attesa crescente 30/60/120/240 s fino a 15 min, tetto cumulativo 400, STOP a 5 fallimenti tecnici consecutivi per servizio. |
| **C7** — regola di maggioranza incompleta | **Chiusa dall'autore in D4, non da questo lavoro**: primario = ripetizione 1 sempre; aggregatore di sensibilità = maggioranza 2 su 3, altrimenti astensione per disaccordo; astensione del modello, astensione per disaccordo e output invalido registrati separatamente. Nessun codice di aggregazione è richiesto prima del batch: l'aggregazione è a valle (7.5). Resta aperto il punto D4 «da verificare in rev2» (sensibilità sul solo audit 10 % o su tutti i prompt) — punto aperto C. |
| **C8** — schedule sotto-determinata | Chiusa: chiamata numpy `Generator.permutation(n)` una volta per passata, numpy 2.2.6 registrato, ordinamento sulla tupla canonica dei cinque campi, `library_role` `none`/`G_P`/`G_A`, tre stage da 2.244 come definizione di «quota per stage». Tutto già nell'artefatto 7.4-PREP e invariato; la quota per stage ora conta le sole richieste base. |
| **Prep 1** — ablation non producibile | Chiuso (vedi B1). Il runner non rifiuta più `B-noLF`; rifiuta qualunque token estraneo alle quattro condizioni. |
| **Prep 2** — prompt non rendibili | Chiuso per la parte di regola e di codice: regola run→finestra fissata (D1, punto 1), driver di estrazione e renderer pronti e testati. Resta il dato: punto aperto A. |
| **Prep 3, 4, 5, 7** — generatore/ordine/`library_role`/stage | Confermati dall'autore per silenzio normativo: nessuno dei quattro è toccato, gli SHA di inventario e schedule sono invariati. |
| **Prep 6** — `X=100` non programmato | Invariato: stage con quota propria, elenco delle verifiche ancora inesistente (punto aperto B). |
| **Prep 8** — marcatura fra due canary | Chiuso (vedi C4), e anticipato rispetto a 7.5. |
| **Prep 9** — costo per chiamata del binding | Invariato: da misurare sul Mac al primo tratto. |
| **Prep 10** — i dieci prompt canary vengono dal pilot | Invariato: prerequisito di materializzazione, non prodotto qui. |

## Punto 1 — assegnazione, in commit separato prima di ogni lavoro sull'input

Commit `7e497dc`, solo assegnazione. «Assegnazione casuale bilanciata per posizione,
separatamente per fault»: un generatore `numpy.random.Generator(PCG64(20260917))`, namespace
`studio2-fase03-window-assignment-v1`, una `permutation(8)` per gruppo di fault, gruppi
visitati in ordine lessicografico della chiave; per i due fault OOD i primi tre valori della
stessa permutazione. numpy 2.2.6 registrato. 78 run assegnati (64 primari + 8 `Normal` +
6 OOD), 11 scorte escluse e mai sostitutive. Ogni posizione compare una volta per ciascun
gruppo da otto. L'artefatto non contiene condizione, agente, libreria né ripetizione:
l'assegnazione è identica fra A, B-LF, E-LF, B-noLF, riceventi, `G_P`/`G_A` e le tre
ripetizioni.

Costruita sui **soli identificativi** del sigillo, con catena di hash verificata:
`SIGILLO_LOTTO_03_11.json` `9bd02e90…` → `BATCH_AUDIT_03_11.json` `420a61eb…` →
`plans/test_batch_f5.csv` `ef0b2852…`. I tre file sono in `main` e non su questo ramo (che
fork a `540df7b`, prima dell'integrazione 03.11): vengono letti dal ref `main` e autenticati
per SHA. **Prima** dell'integrazione in `main` va quindi rispettato l'ordine già indicato
dalle due review: ramo librerie fino a `f0d0393` → 03.11 → candidato 7.3 → tag.

Precondizione D1 verificata prima di assegnare: otto finestre utili per ciascuno degli 89 run
(712 sigillate = 89 × 8, zero run incompleti, zero trip, zero fallimenti tecnici, hash del
manifest di generazione verificati). L'orizzonte `[25, 65)` a 5 h dà esattamente otto
finestre mezze aperte, quindi un run non può superarne otto: uguaglianza dei totali e zero
run incompleti implicano otto per run. La riverifica **per-run** contro
`generation_manifest.csv` è implementata e scatta al punto 2, quando la release sarà
scaricata: se un run non porta otto finestre, si registra e non si sostituisce.

## Punti aperti

**A — bloccante, dato mancante.** La copia locale verificata della release
`studio2-fase03-test-v1` non esiste: senza di essa non si estrae l'input consumer, non si
rendono i 2.244 prompt e non si materializza il target. I comandi sono nel runbook §1-bis
(scarico, `shasum -a 256 -c`, estrazione). Nota di coerenza già rilevata da C3:
`ARTIFACT_STORAGE.json` in `main` dà la release `publication_pending_author` mentre il tag
remoto esiste; va registrata la verifica per riscaricamento.

**B — `X=100`.** L'elenco delle verifiche tecniche va scritto prima dell'esecuzione o `X`
resta inutilizzabile. Nessun comando la consuma.

**C — D4 «da verificare in rev2».** Se la sensibilità 2-su-3 vada riportata su tutti i prompt
oltre al sottoinsieme audit del 10 %, e come trattare i casi con meno di tre esiti validi,
resta una decisione d'autore da prendere **prima** dei dati. Non tocca il batch.

**D — barriera per giorno civile.** Il runner ora rifiuta un lotto in un giorno privo di
canary PASS proprio. È la lettura letterale di §6; il candidato §7.1 chiedeva solo «almeno un
giorno PASS». Se l'autore vuole la regola più debole, è una riga in `require_canary_ok`.

**E — riverifica per-run delle finestre.** Fatta sugli identificativi; la conferma sul
manifest di generazione arriva con il punto A.

## Test

Nuovi test offline, tutti passanti, uno per regola nuova:

| Modulo | Test | Copre |
| --- | ---: | --- |
| `harness/test_window_assignment.py` | 11 | riproducibilità byte per byte; una finestra per run; ogni posizione una volta per fault; scorte mai assegnate; sorgenti sigillate autenticate e concatenate; STOP se un run non ha otto finestre; STOP se il totale sigillato non torna; indipendenza da condizione/agente/libreria |
| `harness/test_bnolf.py` | 12 | B-noLF = B-LF meno il blocco di politica e nient'altro; la politica non sopravvive; sezioni restanti identiche; insight invariati; diff solo sul blocco; delta in byte esatto; stabilità sugli otto agenti; `protocol.py` non modificato; `CallRecord` ammette il token e rifiuta un token ignoto |
| `harness/test_final_prompts.py` | 10 | i 2.244 prompt renderizzati offline; conteggi per blocco e per condizione; diff B↔E solo sui pseudolabel (624 celle appaiate); 148 prompt di ablazione senza politica; identificativi e byte 1:1; determinismo; caso mancante = STOP; prompt oltre il contesto = STOP |
| `evidence/test_test_lot_evidence.py` | 8 | **unità byte-identica a quella prodotta da 03.6 per la stessa finestra**; una unità per run sulla finestra assegnata; run mancante registrato e non sostituito; run senza otto finestre registrato; determinismo; hash per caso nel manifest; il fault non raggiunge il manifest consumer; comando di scarico con `shasum -c` |
| `harness/test_final_batch.py` (esteso) | 32 | tabella D3 riga per riga: incerto sospeso senza reinvio, zero-token provato ritentato una volta in quota separata, retry che non consuma slot scientifico, ricevuto invalido terminale; cinque fallimenti consecutivi che fermano la campagna; contatore che sopravvive alla riapertura del ledger; reset su chiamata completata; attesa crescente e sua soglia; barriera canary→lotto per giorno; identità canary persistita; fingerprint cambiato = STOP; canary invalido che lascia il giorno non chiuso e non lo rispedisce; marcatura vuota con canary PASS; marcatura su giorno marcato; marcatura in sola lettura |

Confronto sull'intera suite `studio2/fase03/harness/test_*.py`, stessa VM Linux:

| Esecuzione | Test | Failure | Error | Skip |
| --- | ---: | ---: | ---: | ---: |
| Base `9e0e086` (export pulito) | 241 | 3 | 49 | 22 |
| Con 7.4-FIX | 290 | 3 | 49 | 22 |

L'insieme dei non-pass è **identico riga per riga** (52 voci, ambientali: dipendono
dall'albero evidence di release e da percorsi solo-Mac); i 49 test nuovi passano tutti.

Riesecuzione sul Mac: eseguita dopo FIX-2 sul commit `a51ffd1` — **306 test, OK, zero
non-pass**. Esito, comando e spiegazione della differenza 306/299 nella sezione FIX-2 §6.

`materialize_final_target.py` in dry-run gira e riporta `BLOCKED_MISSING_PREREQUISITES`: in
FIX-1 con `planned_maximum 7302` e cinque prerequisiti residui, in FIX-2 con
`planned_maximum 7202` e tre (vedi sotto). In nessuno dei due la condizione `B-noLF` è più
un blocco.

---

# FIX-2 — input del lotto test, prompt finali, `X = 0`

Data: 2026-09-17, stessa finestra e stesso branch, base `1c70001`. Offline: nessuna chiamata,
nessuna materializzazione, nessun push/merge/tag.

## Sblocco del punto A

La release `studio2-fase03-test-v1` è stata riscaricata da Luca; i tre SHA sono stati
**ricalcolati qui** e coincidono con `fault_runs/ARTIFACT_STORAGE.json` (ramo `main`):
`test_batch_f5_001.tar.gz` `ac1e7c0c…`, `chain_f5_001.tar.gz` `242f689a…`,
`ood_preflight_001.tar` `16acf7c1…`. Gli archivi sono stati spostati sotto
`studio2/fase03/fault_runs/test_batch/` (la loro sede naturale secondo `archive_root`) ed
estratti lì. `fault_runs/test_batch/` ed `evidence/output_test/` sono stati aggiunti ai
rispettivi `.gitignore`: né il lotto né le unità estratte entrano in repository, esattamente
come per il lotto di sviluppo.

## 1. Riverifica per-run delle otto finestre (punto E, chiuso)

`generation_manifest.csv` del lotto estratto ha SHA `e7c75d23…` ed `events.jsonl`
`af4f659e…`: coincidono con il sigillo. Sulle sue 89 righe: **89 `complete`, zero eccezioni,
`useful_windows_complete = 8` per ogni run, somma 712**. La verifica è ora anche geometrica:
per ciascun run la tabella `post_fault_windows` dichiara le otto finestre mezze aperte
`[25,30) … [60,65)` tutte complete, e il manifest immutabile per-run (`<run>.manifest.json`)
è confrontato campo per campo con la riga del manifest di campagna, hash del CSV incluso.
`development_eligible` è `false` in tutto il lotto test — corretto, e irrilevante per
l'estrazione, che non usa quel flag.

Il driver è stato adattato al manifest di campagna: la colonna `sha256` viene normalizzata in
`output_sha256` (solo il nome, nessun valore inventato) e la verifica del manifest per-run è
quella del lotto test, non quella di sviluppo che pretende `development_eligible: true`.

## 2. Estrazione evidence sulla finestra assegnata

`evidence/extract_test_lot_evidence.py` sull'assegnazione `c809e79d…` (tabella `1ba7669a…`):

| Voce | Valore |
| --- | --- |
| Run assegnati / unità estratte | 78 / **78** |
| `not_extracted` | **[]** |
| Finestre calcolate per run / estratte per run | 8 / **1** |
| Leakage sui file consumer-facing | **PASS** |
| Dimensione firma | 697 |
| `EVIDENCE_MANIFEST_TEST.csv` | `6be25786bb40951eb23f2b63e482572001ea8c68c7591327e720e23c9186af09` |
| `EVALUATOR_INDEX_TEST.csv` | `a415b4323320cc8497f7a4cbbdabf6f67954f02116dc6f39228006b4067c5578` |
| **`INPUT_MANIFEST_TEST_7_4.json`** | **`67e7584a80d743efc06edc4c97019c20803cc4787c1d70c8d924ad23736612e8`** |

Baseline e guardie sono quelle congelate: `mode1_normal_500.xlsx` `79883dd0…`,
`verbalizer_config_v2.json` `552a0b8a…`, `R2_GUARD_RECHECK.json` `7df0cef2…`. Rieseguendo
l'estrazione in una directory diversa i due SHA di manifest sono identici: deterministica.
Nessuna statistica per fault, nessuna anteprima, nessuna selezione sul contenuto; il fault
resta nell'indice evaluator-side e non compare nel manifest consumer.

## 3. Rendering dei 2.244 prompt

| Voce | Valore |
| --- | --- |
| Prompt unici | **2.244** (richieste a `R=3`: 6.732) |
| Per blocco | nucleo 1.728 · swap 224 · ablazione 148 · OOD 144 |
| Per condizione | A 624 · B-LF 848 · E-LF 624 · **B-noLF 148** |
| Diff B↔E | **PASS** — 624 celle appaiate, 0 coppie identiche, 0 differenze fuori dal blocco `PEER INSIGHTS` |
| Diff B-noLF | **PASS** — 148 prompt, 0 che conservano la politica |
| Casi | 78 |
| `prompts_sha256` (identificativo→hash) | `b819200396da480d3ed9d4aa8f6b6aac8c135d97f0876b734a9b607b75736489` |
| `final_prompts.jsonl` | `f938604c512394df0e149732e474eb7d17b02a8dd1ed72155b84f19579a1385d` |

Token per prompt, contati con il tokenizer congelato `a099dee7…` e il suo chat template,
contro un contesto qualificato di **131.072** con **2.560** riservati all'output:

| Insieme | n | min | p50 | p95 | max | media |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| tutti | 2.244 | 849 | 4.923 | 5.219 | **5.284** | 3.928,9 |
| A | 624 | 849 | 1.225 | 1.414 | 1.417 | 1.191,8 |
| B-LF | 848 | 4.594 | 5.028 | 5.222 | 5.284 | 5.000,6 |
| E-LF | 624 | 4.594 | 5.026 | 5.220 | 5.231 | 4.978,9 |
| B-noLF | 148 | 4.519 | 4.958 | 5.147 | 5.156 | 4.902,1 |

Il massimo è **5.284 token**, il 4,0 % del contesto: nessun prompt si avvicina al limite.
Solo conteggi: i testi non sono stati aperti né ispezionati.

Esempi locali, spazio di label, agenti e derangement vengono dal manifest congelato del pilot
`84176888…`. L'**ordine di presentazione** delle label è quello accettato dall'autore
(`studio2-fase03-presentation-v1`, letto da `PILOT_INPUT_SOURCES.frozen.json` `3099ad40…` e
accettato solo con `author_decision: accepted`): il batch finale mostra le label esattamente
come il pilot.

**Difetto trovato e aggirato senza riscrivere l'artefatto accettato.**
`librerie/LIBRERIE_FINALI_CANDIDATE.json` registra un `library_path` assoluto che apparteneva
alla macchina che lo ha prodotto e non è portabile: nessuna macchina diversa da quella può
leggere le librerie per quel percorso. L'artefatto è un record 7.2-R accettato e **non è
stato riscritto**; `build_final_prompts.py` e `build_final_inventory.py` accettano ora
`--libraries-root` e cercano la libreria per nome sotto quella radice, accettandola **solo**
se lo SHA coincide con `library_file_sha256`. Da correggere alla prossima revisione delle
librerie (punto aperto F).

## 4. `X = 0` e nuovo massimo

`TECHNICAL_VERIFICATION_QUOTA = 0`: lo stage resta definito ma la sua quota è zero, il che lo
chiude a doppia mandata — il piano di stage non può nemmeno essere legato (la copertura
eccede la quota) e una riserva diretta è rifiutata con `stage technical_verification has
quota 0 … requires a declared protocol revision`.

| Voce | FIX-1 | FIX-2 |
| --- | ---: | ---: |
| Scientifiche | 6.732 | 6.732 |
| Canary | 70 | 70 |
| `X` | 100 | **0** |
| Quota retry separata | 400 | 400 |
| **`planned_maximum` = `hard_stop`** | 7.302 | **7.202** |

T5 ricalcolato sulle 120 righe del gate (media 26,2086 s, p95 36,6609 s):

| Insieme | media | media × 1,20 | p95 | p95 × 1,20 |
| --- | ---: | ---: | ---: | ---: |
| 6.802 (scientifiche + canary) | 49,5 h | 59,4 h | 69,3 h | 83,1 h |
| **7.202 (con quota retry piena)** | 52,4 h | **62,9 h** | 73,3 h | **88,0 h** |

Contro `W` = 168 h: margine ampio in entrambi i casi.

## 5. Dry-run della materializzazione

`materialize_final_target.py` (dry-run, scrive nulla) → `BLOCKED_MISSING_PREREQUISITES`, con
`planned_maximum 7202`, `hard_stop 7202`, `retry_quota 400`, `consecutive_failure_stop 5`,
`stage_quota {r1 2244, r2 2244, r3 2244, canary 70, technical_verification 0}`, inventario
`227e5e9c…` e schedule `1acfc404…` invariati.

Prerequisiti residui, **tre**, tutti artefatti di runtime che non si producono qui:

1. configurazione eseguibile del target finale con l'identità 122B qualificata;
2. contratto di generazione congelato del target finale;
3. i dieci prompt canary congelati di §6.

I prompt renderizzati e lo snapshot del tokenizer **non** sono più fra i bloccanti.

## 6. Test

Suite `studio2/fase03/harness/test_*.py` più `evidence/test_test_lot_evidence.py`.
Un test nuovo in FIX-2: `X = 0` chiude `technical_verification` (profilo a 7.202 e stage non
legabile).

| Esecuzione | Test | Failure | Error | Skip | Esito |
| --- | ---: | ---: | ---: | ---: | --- |
| VM Linux (questa finestra) | 299 | 3 | 49 | 22 | non-pass **identico riga per riga** alla base `9e0e086` |
| **Mac, `/opt/anaconda3/bin/python3`** | **306** | **0** | **0** | **0** | **OK**, 485,662 s |

Esito del Mac acquisito da Luca in `batch_finale/SUITE_MAC_a51ffd1.txt`, SHA-256
`50601686bc4ecd160820d0b2413eeecab63511b21477b579a760dd1c30f4b373`, commit `a51ffd1`,
Python 3.13 di Anaconda. Il file contiene in testa la coda di una prima esecuzione
interrotta con `Ctrl-C` e poi l'esecuzione completa; è quest'ultima a fare fede.

**Sul Mac non c'è alcun non-pass.** I 52 non-pass e i 22 skip della VM erano tutti
ambientali, come dichiarato in 7.4-PREP: dipendono dall'albero evidence di release e da
percorsi che esistono solo sul Mac. La riesecuzione lo conferma.

### Perché 306 sul Mac e 299 nella VM

La differenza è di **sette test** ed è interamente
`harness/test_d01_replay.ReplayPrerequisites`. Il suo `setUpClass` esegue
`git -C /Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate rev-parse HEAD`
per pretendere che il generatore delle fixture legacy sia esattamente il candidato `0c8157f`
e sia pulito. Quella worktree esiste sul Mac; nella VM Linux non è montata, il comando esce
con stato 128 e `setUpClass` solleva.

Quando `setUpClass` fallisce, `unittest` registra **un errore di classe** e **non conta** i
metodi: la classe contribuisce `Ran 0 tests … errors=1`. I sette metodi
`test_D01_*` di quella classe spariscono quindi dal conteggio della VM:

    306 (Mac) − 7 (metodi di ReplayPrerequisites) = 299 (VM)

Non è una differenza di codice né di selezione dei test: è la stessa suite, con una classe
non eseguibile dove manca la sua worktree di riferimento.

Comando eseguito:

```bash
cd /Users/luker/fot-tep/.worktrees/rem6-riconciliazione
/opt/anaconda3/bin/python3 -m unittest $(ls studio2/fase03/harness/test_*.py | sed 's|/|.|g; s|\.py$||') studio2.fase03.evidence.test_test_lot_evidence
```

## 7. Stato dei punti aperti di FIX-1

| Punto | Stato |
| --- | --- |
| **A** — release non scaricata | **chiuso**: scaricata, verificata, estratta, 78/78 unità |
| **B** — `X=100` non programmato | **chiuso dall'autore**: `X = 0`, stage a quota zero |
| **C** — D4 «da verificare in rev2» | **chiuso dall'autore** (Q3): audit 10 % invariato più aggregatore descrittivo su tutti i prompt; triplette con meno di tre esiti validi = `invalid_incomplete_triplet`. È analisi a valle (7.5): nessun codice qui |
| **D** — barriera canary per giorno civile | **confermata dall'autore** come lettura letterale di §6 |
| **E** — riverifica per-run delle finestre | **chiuso**: 89/89 run, otto finestre ciascuno, geometria e manifest per-run verificati |

## 8. Punti ancora aperti

**F — `library_path` non portabile in `LIBRERIE_FINALI_CANDIDATE.json`.** Aggirato con
`--libraries-root` e verifica di SHA; va corretto alla prossima revisione tracciata delle
librerie, perché così com'è l'artefatto non è riusabile su nessuna macchina diversa da quella
che lo ha prodotto.

**G — suite sul Mac.** **Chiuso**: 306 test, OK, nessun non-pass; evidenza in
`batch_finale/SUITE_MAC_a51ffd1.txt` (`50601686…`). Vedi §6.

**H — prerequisiti di runtime del target.** I tre elencati al §5, più il tag annotato del
protocollo e l'approvazione di materializzazione, restano in capo a Luca.

**I — ordine di integrazione in `main`.** Invariato: ramo librerie fino a `f0d0393` → 03.11 →
candidato 7.3 corretto → tag. I file sigillati di 03.11 continuano a essere letti da `main`
perché questo ramo fork a `540df7b`.

**L — review `b567`.** Dovuta: FIX-2 tocca ancora quota e ledger (`TECHNICAL_VERIFICATION_QUOTA`,
nuovo massimo, rifiuto della quota zero).

---

# FIX-3 — rilievi B della review finale

Fonte: `VERIFICA_FINALE_PROTOCOLLO_RUNNER_H3.md`, SHA
`a2fe4b6753cdbac04f0eaddd9902f735adeb0c201bc220d882532ec8f81fba6a`, sezione «Rilievi»,
letta in sola lettura in `/Users/luker/fot-tep-pubblicazione-consolidamento-0315-metriche/`.
Esito della review su B: **OK con rilievi, nessun bloccante**. Base `7925124`. Offline:
nessuna chiamata, nessuna materializzazione, nessun push/merge/tag. Sostituzione di modello
dichiarata: mandato a `gpt-5.6-sol`, eseguito da `claude-opus-5` (Claude Cowork).

## I cinque SHA pinnati: **invariati**

| Artefatto | SHA-256 | Verifica in questa sessione |
| --- | --- | --- |
| Inventario | `227e5e9c797dbfd8be746d85b77298f5dfb091846dc301f0b2e31ea1dbc6df3f` | rigenerato con `build_final_inventory.py`, identico |
| Schedule | `1acfc4044c53f113016ed0bfab58863291a9060a9edc9abadb68a21d30687819` | rigenerata, identica |
| Assegnazione finestre | `c809e79d2c03d74f4a5a37988eca809bda336468ab0060f794d3c214f9a6a775` | `shasum` sul file committato, identico |
| Manifest di input del lotto test | `67e7584a80d743efc06edc4c97019c20803cc4787c1d70c8d924ad23736612e8` | nessun file della sua catena è nel diff |
| Mappa dei prompt | `b819200396da480d3ed9d4aa8f6b6aac8c135d97f0876b734a9b607b75736489` | nessun file della sua catena è nel diff |

Gli ultimi due si producono con `build_final_prompts.py`, che importa soltanto
`harness/final_inventory.py`, `harness/final_prompts.py`, `harness/common.py` e
`runtime.durable_write`: i primi tre non sono toccati da FIX-3 e di `runtime.py` cambia solo
`execute_request` (più la nuova eccezione tipata), non `durable_write`. Il diff di FIX-3
tocca nove file, nessuno dei quali entra nel rendering dei prompt o nell'estrazione evidence.

## Rilievo → chiusura

**B1 — `--day` non era mai confrontato con l'orologio. Chiuso.**
`resolve_civil_day` (in `run_final_batch.py`) lega il giorno dichiarato a `rome_day(now)` e
restituisce `declared_day`, `observed_day` e `midnight_crossing`. La regola
dell'attraversamento è stretta e vale solo se **tutte** e tre le condizioni sono vere: il
giorno osservato è il giorno di calendario immediatamente successivo a quello dichiarato; lo
stage possiede già almeno una richiesta completata nel giorno dichiarato (nuovo accesso di
sola lettura `PilotLedger.completion_instants`); si tratta di un lotto scientifico. **Il
canary non attraversa mai la mezzanotte**: apre il giorno a cui appartiene, quindi
`run_day` chiama `resolve_civil_day` senza prova di attraversamento e il ledger ripete il
rifiuto in `record_canary_day`, che accetta `observed_day` e lo rifiuta se diverso dal
dichiarato. Entrambi i valori sono persistiti: nell'evento canary (`declared_day`,
`observed_day`), nel record durevole di ogni chiamata del batch e del canary
(`declared_day`, `observed_day`, `midnight_crossing`), nel riepilogo di tratto e
nell'artefatto del giorno invalido. Il controllo è rifatto **prima di ogni richiesta**, non
solo all'avvio, così l'attraversamento della mezzanotte a metà tratto è deciso dalla regola e
non subìto. La regola è scritta nel runbook, §5, con l'esempio del tratto delle 22:00.
Test: `CivilDayBinding`, otto test.

**B2 — `canary_marking` presentava l'unione come la maschera. Chiuso.**
I campi sono ora `primary_mask_request_ids` (piano §10.5, giorno civile marcato: è la
maschera che esce dalla sensibilità pre-specificata), `forensic_mask_request_ids` (§6.5,
intervallo fra l'ultimo PASS e il canary fallito, **solo forense**) e
`union_descriptive_request_ids` (**solo descrittiva**, con `union_scope` che lo dichiara).
`marked_request_ids`, `interval_only` e `civil_day_only` non esistono più; la versione
dell'artefatto passa a `MARCATURA_CANARY_7_4_2` e la docstring del modulo riporta la
gerarchia di §6.5 rev3 invece dell'unione. `query_canary_marking.py` e il runbook §3 sono
allineati. Test: due test in `CanaryBarrierAndMarking`, che verificano anche l'assenza del
campo generico.

**B3 — journal dichiarato e mai scritto. Chiuso per via contrattuale, senza journal nuovo.**
`CONTRATTO_ESECUZIONE_E_RIPRESA.md` è **congelato** — `HARNESS_D9_CANDIDATE.json` ne pinna i
byte con SHA `b4e822a3…` — quindi non è stato modificato in luogo: la clausola vive in una
revisione tracciata, `harness/CONTRATTO_ESECUZIONE_E_RIPRESA_REV2_BATCH_FINALE.md`, che vale
per i soli stage del profilo `final_batch` e nomina la proiezione effettiva (SQLite
autorevole, `{stage}_call_log.jsonl`, un record durevole per richiesta, il riepilogo di
tratto). Nel codice sono spariti il no-op, la variabile `journal_path` dei due runner e il
commento che descriveva ciò che non avveniva; `execute_request` ha ora `journal_path`
opzionale, e senza di esso non scrive alcuna proiezione — non un file vuoto. Gli ingressi del
pilot lo passano sempre e restano identici. Verifica:
`grep -rn 'journal' run_final_batch.py run_final_canary.py` non restituisce nulla, e lo SHA
del contratto congelato è invariato.

**B4 — STOP d'identità classificato per sottostringa. Chiuso.**
`runtime.IdentitySuspension(HarnessError)` è la nuova eccezione tipata, sollevata nei due
punti in cui l'identità manca o cambia, con `field`, `observed` ed `expected`. Il canary la
intercetta per tipo (`except IdentitySuspension`) e non più con
`if "identity" not in str(exc)`: una riformulazione del messaggio non può più far perdere
l'evento durevole. Essendo sottoclasse di `HarnessError`, nessun percorso fail-closed
esistente cambia comportamento. Il campo che è cambiato finisce nell'evento di STOP.

**B5 — fallback di `rome_day` con confini d'ora legale sbagliati. Chiuso con il rifiuto.**
Senza `zoneinfo`/tzdata `rome_day` ora **rifiuta** con un `HarnessError` che dice cosa
installare, invece di stimare il giorno civile con il 31 marzo / 27 ottobre. Il giorno civile
è l'unità della barriera e della maschera primaria: una risposta approssimata è peggio di
nessuna risposta. Due test: il rifiuto in assenza di tzdata, e l'esattezza attorno al
cambio d'ora reale del 2026 (25 ottobre), dove il vecchio fallback sbagliava.

**B6 — il tetto totale non era esercitato. Chiuso.**
`test_the_total_ceiling_is_refused_on_its_own_path` afferma l'identità reale del profilo
(`planned_maximum = hard_stop = 7.202 = Σ base_limits + retry_quota`) e poi, su un profilo
con quote per stage larghe e totale stretto, percorre **entrambi** i rami del totale: il
rifiuto sul massimo pianificato e quello sull'hard stop cumulativo, che con 7.202 si
raggiungono solo a campagna conclusa.

**B7 — pin dipendenti da NumPy e `protocol_reference: e0db132`. Nessuna modifica, come chiesto.**
Si dichiara qui: `numpy_version` e `protocol_reference` stanno **dentro** il payload hashato
di `inventory_artifact`, `schedule_artifact` e dell'assegnazione. I tre pin `227e5e9c…`,
`1acfc404…` e `c809e79d…` sono quindi riproducibili solo sotto **NumPy 2.2.6**, che è
l'ambiente di riferimento di §7.1, registrato negli artefatti e presente sul Mac; un
aggiornamento futuro cambierebbe lo SHA senza cambiare l'ordine e **va spiegato, non
sovrascritto**. Il riferimento `PROTOCOLLO_FINALE_CANDIDATE.md e0db132 §4, §5, §7.1` cita il
candidato rev1: è imprecisione documentale e non errore di conteggio, perché i contenuti
richiamati di §4 e §5 (2.244 e 6.732) sono identici in rev1 e rev3. Correggerlo cambierebbe
i pin, che il mandato dichiara invarianti: resta com'è, dichiarato.

**N — riga `/test_batch/` duplicata in `fault_runs/.gitignore`.** Lasciata: si ripulisce al
merge, come indicato.

## Test

| Esecuzione | Test | Failure | Error | Skip |
| --- | ---: | ---: | ---: | ---: |
| Base `7925124` | 291 | 2 | 33 | 22 |
| Con FIX-3 | 303 | 2 | 33 | 22 |

Dodici test nuovi, tutti passanti; l'insieme dei non-pass è identico riga per riga ed è
ambientale (albero evidence di release assente in questa VM Linux, percorsi solo-Mac).
`studio2.fase03.harness.test_final_batch` da solo: **45 test, OK**.

Comando della suite per il Mac, da rieseguire e salvare in
`batch_finale/SUITE_MAC_<sha del commit>.txt`:

```bash
cd /Users/luker/fot-tep/.worktrees/rem6-riconciliazione
/opt/anaconda3/bin/python3 -m unittest $(ls studio2/fase03/harness/test_*.py \
  | sed 's#/#.#g; s#\.py$##') 2>&1 | tee \
  studio2/fase03/batch_finale/SUITE_MAC_<sha>.txt
```

## Note lasciate aperte

Restano aperti, invariati, i punti **F**, **H**, **I** e **L** del §8, e i rilievi **A1**,
**A2**, **A3**, **A4**, **A5**, **A6** e **C1** della review, che non sono di competenza di
questo fix: A1 e A2 riguardano l'ordine di merge e i due documenti di §2 che si
contraddicono, A3 la conservazione (o il depinnaggio) di `final_prompts.jsonl`, A4-A6 e C1
sono note documentali sul candidato e sullo script H3.
