# 7.4-PREP — runner e runbook del batch finale

Data: 2026-09-17. Branch `codex/studio2-riconciliazione-stop-contabile`, base `f0d0393`.
Sostituzione di modello dichiarata: mandato indirizzato a `gpt-5.6-sol`, eseguito da
`claude-opus-5` (Claude Cowork). **Nessuna chiamata a modelli, nessuna materializzazione,
nessun push/merge/tag.** Runtime esistenti aperti in sola lettura; `pilot-001`, `pilot-002`
e `pilot-03` intoccati; server 27B non toccato.

## Tocca quota / accounting / ledger: **SÌ**

Scatta quindi la review `b567` sul commit. Dove, esattamente:

1. **`harness/ledger.py` — profilo di quota.** Nuovo `LedgerProfile` immutabile e due
   profili: `pilot` (invariato: stage, `BASE_LIMITS`, massimo pianificato 152/160,
   hard stop 200, cinque quota kind) e `final_batch` (stage
   `final_batch_r1|r2|r3` da 2.244, `final_canary` 70, `technical_verification` 100;
   massimo pianificato e hard stop entrambi **6.902**; unico quota kind ammesso `base`,
   che è l'applicazione strutturale di `Q=0`). `PilotLedger.__init__` accetta
   `profile="pilot"` come default; il profilo è dichiarato **una volta sola** in un evento
   create-once alla creazione del ledger e ogni apertura successiva con un profilo diverso
   è rifiutata. Un ledger scritto prima di 7.4 non ha la dichiarazione ed è per definizione
   un ledger pilot: **non viene riscritto**.
2. **`harness/ledger.py` — `_insert_intent`.** Il ramo pilot è identico riga per riga. Il
   ramo `final_batch` applica §7.2: quota kind ammesso, hard stop cumulativo, massimo
   pianificato, quota per stage.
3. **`harness/ledger.py` — `_prerequisites`.** Solo sotto profilo `final_batch`: uno STOP
   canary blocca ogni chiamata; una passata scientifica richiede almeno un giorno canary
   PASS (§7.1 passo 3); la passata *k+1* non si apre prima della chiusura della *k*.
4. **`harness/ledger.py` — verdetti canary.** Nuovi `record_canary_day` e
   `record_canary_stop`: eventi normativi create-once, che chiudono un giorno solo su dieci
   chiamate complete, rifiutano un giorno già registrato, applicano il tetto di sette giorni
   e scrivono da soli lo STOP al secondo giorno marcato. Non passano da `record_event`
   (che resta riservato alle note non normative).
5. **`harness/ledger.py` — `bind_stage`, `snapshot` e i controlli di appartenenza stage**
   leggono il profilo invece delle costanti pilot. `snapshot()` espone `profile`,
   `stage_quota` e lo `hard_stop` del profilo.
6. **`harness/d9.py` — `STAGE_MODELS`**: i cinque stage del batch sono dichiarati `122B`,
   coerentemente con §5 (6.902 chiamate 122B, 0 chiamate 27B).
7. **`harness/runtime.py`**: `execute_request` accetta `journal_path` opzionale
   (7.4-FIX-3, rilievo B3: prima era un parametro `journal` con un no-op lato batch).
   Passandolo si ha il comportamento del pilot (ri-export completo del journal a ogni passo);
   il batch, che ha binding da 2.244 specifiche, non lo passa: la sua proiezione durevole è
   il call log più un record per richiesta, come dichiara la revisione tracciata
   `harness/CONTRATTO_ESECUZIONE_E_RIPRESA_REV2_BATCH_FINALE.md`. Nessuna regola di
   contabilità cambia: SQLite resta la fonte autoritativa.
8. **`run_pilot.py`**: `Provider.ALLOWED_STAGES` sostituisce l'insieme di stage letterale
   dentro `Provider.call`. Valore identico per il pilot; il runner del batch sottoclassa.

L'accounting del tokenizer 122B **non cambia**: il runner del batch carica lo stesso
`TokenizerAccountingGuard` e passa per lo stesso `execute_request`, quindi la guardia
contabile si applica a tutte le 6.902 chiamate esattamente come nel gate del pilot.

## Cosa è nuovo e cosa è riusato

Riusato senza modifiche funzionali: `PilotLedger` (macchina a stati, riconciliazioni,
zero-token, sospensioni, revisioni di configurazione), `execute_request`, `Provider`,
`consumer_record`, `vllm_grammar_schema`, `harness/canary.py` (`compare_run`),
`harness/sampling.py` (selettore congelato), `harness/logging_v1.py` (logging T7 §8.7),
`harness/guards.py`, `protocol.py` (renderer e parser).

Nuovo, il minimo necessario:

| File | Cosa fa |
| --- | --- |
| `harness/final_inventory.py` | Inventario logico dei 2.244 prompt unici e schedule delle tre passate (§4, §5, §7.1). |
| `build_final_inventory.py` | CLI offline e idempotente: genera, verifica i conteggi contro §5, rifà il diff strutturale B↔E e stampa gli SHA. |
| `materialize_final_target.py` | Dry-run e materializzazione del target fresco; fallisce chiusa sui prerequisiti mancanti. |
| `run_final_batch.py` | Runner per schedule, `--pass-index`, `--max-requests`, `--resume`, avanzamento/ETA, STOP §7.2, logging T7/T9. |
| `run_final_canary.py` | Comando canary giornaliero separato (§6), con PASS/MARKED/STOP. |
| `harness/test_final_batch.py` | 16 test offline con provider finto. |
| `batch_finale/INVENTARIO_SCHEDULE_7_4.json` | Riassunto committato con conteggi e SHA. |
| `batch_finale/CANARY_ATTESI_7_4.json` | Trascrizione della tabella §6 (dieci prompt, coppie attese, hash grezzi). |
| `RUNBOOK_7_4_BATCH_FINALE.md` | Comandi esatti per Luca. |

Gli artefatti completi (inventario 659 KB, schedule 2,4 MB) **non** sono committati: il
generatore è deterministico e byte-identico a ogni esecuzione, e i due SHA sono qui sotto.
`batch_finale/build/` è ignorato.

## Inventario, schedule e verifiche

| Voce | Valore |
| --- | --- |
| SHA-256 inventario | `227e5e9c797dbfd8be746d85b77298f5dfb091846dc301f0b2e31ea1dbc6df3f` |
| SHA-256 schedule | `1acfc4044c53f113016ed0bfab58863291a9060a9edc9abadb68a21d30687819` |
| ID stabile | `(block, condition, case_id, recipient_agent, library_role)` |
| Prima riga della schedule | `producer_swap\|B-LF\|test-primary-F10-r04\|agent_6\|G_A\|r1` |
| Ultima riga della schedule | `nucleus\|E-LF\|test-primary-F10-r02\|agent_6\|G_P\|r3` |

Conteggi per blocco, unici e richieste, **coincidenti con §5**:

| Blocco | Unici | Richieste (`R=3`) |
| --- | ---: | ---: |
| Nucleo | 1.728 | 5.184 |
| Producer-swap | 224 | 672 |
| Ablation B-senza-LF | 148 | 444 |
| OOD | 144 | 432 |
| **Totale** | **2.244** | **6.732** |

Con canary 70 e `X=100`: **6.902**, il totale futuro massimo di §5.

`case_id` è il `run_id` del lotto 03.11 (`test-primary-F<n>-rNN`, `test-primary-Normal-rNN`,
`test-ood-F{4,5}-rNN`), coerente con `PIANO_STATISTICO.md` §2.2, dove il caso è il run
simulato. La proprietà locale viene da `pseudolabel/AGENT_ASSIGNMENT.json`, riletto sotto
lo SHA del suo freeze.

Diff strutturale B↔E rifatto qui su entrambe le librerie reali: **112/112 record cambiano
nel solo campo `pseudolabel`**, `G_P` `c2469737…` e `G_A` `f860063b…`, coerente con §3.3.
L'appaiamento B-LF/E-LF è verificato su 624 celle (nucleo e OOD); producer-swap e ablation
non hanno braccio E, come da §4.

## Test

`python3 -m unittest studio2.fase03.harness.test_final_batch` → **Ran 16 tests, OK**.
Coprono: batch completo in piccolo; interruzione con `--max-requests` e resume identico che
non rispedisce nulla; resume mai implicito; risposta invalida terminale non sostituita;
zero-token riconciliato senza nuovo invio; sospensione d'identità che ferma il batch; quota
di stage esaurita; batch senza canary PASS rifiutato; secondo giorno marcato che blocca;
passata 2 che non parte prima della chiusura della 1; canary PASS che sblocca il batch;
deriva comportamentale che marca il giorno; cambio d'identità che ferma prima di altre
chiamate; determinismo e conteggi di inventario e schedule; condizione non producibile
rifiutata invece che reinterpretata.

Suite esistente, sedici moduli `studio2/fase03/harness/test_*.py`, confronto diretto in
questa VM Linux:

| Esecuzione | Test | Failure | Error | Skip |
| --- | ---: | ---: | ---: | ---: |
| Base (modifiche 7.4 stashate, senza `test_final_batch`) | 225 | 2 | 33 | 22 |
| Con le modifiche 7.4 e i 16 test nuovi | 241 | 2 | 33 | 22 |

L'insieme dei non-pass è **identico riga per riga** e i 16 test nuovi passano tutti. I 35
non-pass sono ambientali: dipendono dall'albero evidence di release
(`studio2/fase03/evidence/output/`, un asset di release non presente in questa VM) e dai
percorsi solo-Mac. Vanno rieseguiti sul Mac con `/opt/anaconda3/bin/python3`.

## Punti aperti, numerati

1. **(Bloccante) La condizione dell'ablation B-senza-LF non è producibile dall'harness
   congelato.** §4 prevede un quarto braccio «B, `G_P`, senza politica local-first», ma il
   renderer vincolante di §2 (`protocol.py`, SHA `791fa347…`) espone `CONDITIONS =
   ("A","B-LF","E-LF")` e costruisce la politica local-first come parte fissa di ogni
   condizione con insight; il contratto di logging §8.7 (`CallRecord.validate`) ammette solo
   `A`, `B-LF`, `E-LF`, `PRODUCER`. Non ho interpretato: l'inventario enumera il blocco con
   la stringa di condizione `B-noLF` e il runner **rifiuta** la schedule finché il punto non
   è chiuso. Chiudere il punto richiede una decisione dell'autore su: quale token di
   condizione, e se il renderer congelato va emendato (nuovo SHA, quindi nuova revisione del
   protocollo). **Qualsiasi altro token cambia lo SHA della schedule qui sopra.**
2. **(Bloccante) I prompt del batch non sono rendibili oggi.** Il renderer ha bisogno del
   manifest di input consumer del lotto **test** 03.11 (testi neutrali per caso ed esempi
   locali per agente). L'estrazione evidence 03.6 copre soltanto i 40 run **di sviluppo**
   (320 unità); per il lotto test non esiste un'estrazione registrata in repository. Finché
   non esiste, l'inventario resta logico e `materialize_final_target.py` si ferma con
   `BLOCKED_MISSING_PREREQUISITES`. Va inoltre fissata la regola che lega un run del lotto
   test alla sua unità di evidenza: 03.6 produce otto finestre utili per run, mentre §4 e
   §2.2 del piano statistico contano **un caso per run**; la regola di scelta della finestra
   non è scritta da nessuna parte.
3. **Il protocollo fissa generatore e seme della schedule, non la chiamata numpy.** §7.1
   prescrive un solo `numpy.random.Generator(PCG64(20260913))` e la permutazione
   dell'inventario ordinato lessicograficamente, per passate 1→2→3. Ho fissato e
   documentato `Generator.permutation(n)` sull'intervallo degli indici, una volta per
   passata, con numpy 2.2.6 registrato nell'artefatto. Una chiamata diversa
   (`permutation(array)`, `shuffle`) produce un ordine diverso e un altro SHA.
4. **Ordine lessicografico: su quale forma.** Ho ordinato sulla tupla canonica dei cinque
   campi; ordinare sulla stringa unita da `|` dà lo stesso risultato solo perché nessun
   campo contiene il separatore (verificato e imposto). Va confermato che la tupla è la
   forma intesa.
5. **`library_role` per la condizione A e per E-LF.** §4 assegna «nessuno / `G_P` / `G_P`
   permutata». Ho usato `none` per A e `G_P` per B-LF ed E-LF, lasciando che sia
   `condition` a distinguere B da E, e `G_A` solo per il producer-swap. Se l'autore vuole
   un quarto valore (`G_P_deranged`), cambia l'ID stabile e quindi entrambi gli SHA.
6. **Il totale 6.902 include `X=100`, che non è programmato.** Il profilo del ledger riserva
   uno stage `technical_verification` da 100 con quota propria, così che nessuna verifica
   tecnica possa finanziarsi sulla quota scientifica. §7.2 dice però che ogni chiamata `X`
   va identificata *prima* dell'esecuzione: l'elenco non esiste e nessun comando lo consuma
   in questa consegna.
7. **Le tre passate sono modellate come tre stage.** §7.2 parla di «quota per stage» senza
   definire gli stage del batch. Tre stage da 2.244 rendono verificabile l'ordine 1→2→3 e
   riducono di tre volte il costo per chiamata del binding. Se l'autore preferisce un unico
   stage da 6.732, cambia il profilo del ledger (non la schedule).
8. **Marcatura dei lotti fra due canary.** §6.5 richiede di marcare le chiamate scientifiche
   eseguite dopo l'ultimo canary PASS e prima del canary fallito. Gli eventi canary
   registrano giorno, indice e request_id del giorno, quindi l'intervallo è ricostruibile
   dai timestamp del ledger; **non** ho scritto il marcatore sulle singole richieste, perché
   ciò richiederebbe scrivere su record già terminali. La marcatura resta un'operazione di
   analisi a valle, da specificare in 7.5.
9. **Costo fisso per chiamata del binding.** Ogni riserva rilegge e ri-hasha il binding di
   passata (2.244 specifiche più la configurazione). È lineare nella dimensione del binding
   e trascurabile rispetto ai ~26 s per chiamata, ma va misurato sul Mac al primo tratto e
   riportato, perché entra nel conto T5 reale.
10. **Il canary usa i dieci prompt del pilot.** §6 congela `S2-P03-006`…`S2-P03-025`, che
    sono prompt del pilot: il target finale deve quindi conservarne i byte esatti. Il
    runner li autentica contro gli SHA della tabella §6, ma la loro disponibilità nel target
    fresco è un prerequisito di materializzazione, non qualcosa che questo lavoro produce.

## Cosa non è stato fatto, e perché

Nessuna materializzazione: la esegue Luca dopo il tag del protocollo (§7.1 passo 1-2).
Nessuna chiamata, nessun canary reale, nessuna quota consumata. La schedule qui prodotta è
un **candidato**: diventa la schedule del batch solo quando il protocollo è taggato, i punti
1 e 2 sono chiusi e `materialize_final_target.py` la congela nel target.
