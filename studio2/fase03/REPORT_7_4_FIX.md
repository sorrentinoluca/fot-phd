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

**7.302 chiamate** = 6.732 scientifiche + 70 canary + 100 `X` (6.902, invariato) + **400**
di quota retry separata. Il 400 viene dal tasso del pilot, 8 fallimenti pre-generazione su
156 richieste (5,13 %): su 6.802 chiamate pianificate l'attesa è ~349, e 400 lascia ~15 % di
margine restando un ordine di grandezza sotto la campagna. Costo temporale a quota piena:
+2,9 h alla media e +4,1 h al p95, cioè 63,8 h / 89,3 h con il margine T5 del 20 %, contro
`W` = 168 h. Il margine temporale non crea quota.

## I quattro SHA

| Artefatto | SHA-256 | Stato |
| --- | --- | --- |
| Assegnazione finestre (tabella) | `1ba7669ae9715e4c6313b6746a05f8d390eeee2877d7f41cc554146c9e35836b` | committata |
| `batch_finale/ASSEGNAZIONE_FINESTRE_7_4.json` (file) | `c809e79d2c03d74f4a5a37988eca809bda336468ab0060f794d3c214f9a6a775` | committata |
| Inventario | `227e5e9c797dbfd8be746d85b77298f5dfb091846dc301f0b2e31ea1dbc6df3f` | **invariato** |
| Schedule | `1acfc4044c53f113016ed0bfab58863291a9060a9edc9abadb68a21d30687819` | **invariato** |
| Manifest di input del lotto test | — | **non producibile**: la copia locale verificata della release `studio2-fase03-test-v1` non esiste (punto aperto A) |

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

Riesecuzione richiesta sul Mac, da incollare qui:

```bash
cd /Users/luker/fot-tep/.worktrees/rem6-riconciliazione
/opt/anaconda3/bin/python3 -m unittest $(ls studio2/fase03/harness/test_*.py | sed 's|/|.|g; s|\.py$||') studio2.fase03.evidence.test_test_lot_evidence
```

`materialize_final_target.py` in dry-run gira e riporta `BLOCKED_MISSING_PREREQUISITES` con
`planned_maximum 7302`, `hard_stop 7302`, `retry_quota 400`, schedule `1acfc404…`: i
prerequisiti residui sono i cinque artefatti di runtime, e **non** più la condizione
`B-noLF`.
