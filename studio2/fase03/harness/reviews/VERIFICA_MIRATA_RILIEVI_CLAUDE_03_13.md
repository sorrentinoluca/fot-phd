# Verifica mirata indipendente dei rilievi Claude — Studio 2 FoT-TEP 03.13

Data: 16 settembre 2026. Review offline sul candidato locale; nessuna modifica al candidato.

## Verdetto

**NOT READY FOR SEPARATE FRESH-TARGET MATERIALIZATION.** Lo stato massimo attestabile è
`READY FOR AUTHOR DECISION AND SEPARATE CORRECTION`.

Il limite ambientale indicato dalla review Claude non si riproduce sul Mac pinnato: la regressione
dei 15 moduli passa 200/200. Restano tuttavia tre difetti tecnici dimostrati nel perimetro
principale:

1. il materializer non ha un gate operativo e una failure intermedia lascia un target parziale che
   il rilancio rifiuta;
2. il resume della qualifica tecnica su un ledger con eventi contabili producer e consumer applica
   un solo guard a contratti diversi e persiste uno STOP globale prima di controllare il leaf;
3. dopo un crash tra completamento del record tecnico e outcome, `resume=True` non ricostruisce
   deterministicamente il PASS, pur senza reinvio o duplicazione di quota.

La scelta metodologica sulla classificazione della prima osservazione, sul nuovo regime
`enable_thinking=false` e sulla comparabilità resta dell'autore. Questa review non la sostituisce.

## 1. Identità, base e ambiente

| Controllo | Atteso | Osservato |
|---|---|---|
| Sorgente | `/Users/luker/.codex/worktrees/dd86/fot-tep` | coincidente |
| HEAD | `a6bc817165fcab820b9c4bbe7209fc7ca53d7d1d` | coincidente |
| Tree | `e2c4ecadbadfbac15947cdaff589256f91ffe9d3` | coincidente |
| Parent | `72fb93c6d26ceb220ed2cece1dac2ef6614c791f` | coincidente |
| Worktree sorgente | pulita | pulita prima e dopo prove e ispezione |
| Review-base | `VERIFICA_TOTALE_INDIPENDENTE_03_13_QWEN_CODEGPT.md` | SHA-256 `a533308fd52a9920c8068357dcc34e57b91fa4d7fb7f07848b1498d2cb90577d` |
| Interprete | Mac pinnato | `/Users/luker/.venvs/fot-tep-condition-c-r10/bin/python` |
| Python | 3.13 | 3.13.9, Anaconda, Clang 20.1.8 |
| `jsonschema` | disponibile | 4.25.0 |
| Piattaforma | Mac locale | macOS 26.6.2 arm64 |

Sono state applicate le lezioni `fot-tep-harness-lessons` su inventario durevole, validazione
prima dell'effetto protetto, API diretta, restart, rollback atomico, prove discriminanti e lettura
del riepilogo effettivo del runner.

## 2. Suite nell'ambiente Mac pinnato

I conteggi delle suite sovrapposte restano separati e non vengono sommati.

| Suite | Moduli | Metodi | Subtest osservabili | Failure | Errori | Skip | Durata | Esito | SHA-256 log |
|---|---:|---:|---|---:|---:|---:|---:|---|---|
| Regressione pertinente completa | 15 | 200 | il runner non espone il totale dei subtest PASS; nessun subtest fallito | 0 | 0 | 0 | 459,506 s | OK | `e104ca81d454eb2b7b2a1afa048f2276aef206b8df2fed70b4b66e1be5699aad` |
| Successor mirata | 1 | 23 | il runner non espone il totale dei subtest PASS; nessun subtest fallito | 0 | 0 | 0 | 5,429 s | OK | `7f81498482dc82fe533b587a46b5f1036e30308e90e79364d7af21ac6e6f8801` |
| Guardian documentale storico | 1 | 35 | 9 failure di subtest visibili, più 5 failure a livello metodo | 14 | 0 | 1 | 0,098 s | NON PASS storico invariato | `c50620726581f4b1308e629196f01047300d167198360cc74c5f5bd009ae2a0e` |
| Sonde indipendenti temporanee | 1 | 8 | nessuno | 0 | 0 | 0 | 0,532 s | OK | `6b390399dcfa727be65f1836ce0dcc897f5e00e2e83fb1201b947c3063142ba5` |

I 15 moduli sono:

```text
studio2.fase03.harness.test_c01_c03
studio2.fase03.harness.test_d01_replay
studio2.fase03.harness.test_d02_predecessors
studio2.fase03.harness.test_d03_contract
studio2.fase03.harness.test_d04_open_quota
studio2.fase03.harness.test_d9
studio2.fase03.harness.test_d9_corrections
studio2.fase03.harness.test_harness_offline
studio2.fase03.harness.test_history_reconciliation
studio2.fase03.harness.test_metric_raccordo
studio2.fase03.harness.test_revisions
studio2.fase03.harness.test_successor_recovery
studio2.fase03.harness.test_tokenizer_accounting
studio2.fase03.tests.test_protocol
studio2.fase03.tests.test_execution_guard
```

I log sono stati prodotti con `PYTHONDONTWRITEBYTECODE=1`. I `ResourceWarning` SQLite già noti
compaiono durante regressione e sonde senza diventare failure o errori. Il guardian resta separato
e non viene riclassificato come PASS. P1-03 della review-base è quindi **NON RIPRODOTTO** nel suo
ambiente dichiarato ed è chiuso come limite ambientale.

## 3. P1-02 — successor e materializer

**Verdetto: DIFETTO DIMOSTRATO nel materializer; falso positivo per la validazione lineage.**

### Parte lineage verificata

Riferimenti: `studio2/fase03/harness/successor.py:30-39`, `85-184`, `187-226`, `229-292` e
`studio2/fase03/harness/ledger.py:362-406`.

Le sonde su predecessore sintetico confermano:

- apertura SQLite `mode=ro&immutable=1`;
- SHA-256 del predecessore invariato e nessun sidecar `-wal`/`-shm` creato;
- controllo completo di schema, pilot id, S=4, unica richiesta nativa sospesa, package, approval,
  decisione autoriale, inventario delle evidenze e target esatto;
- rifiuto di approval o target differenti;
- import exactly-once e comportamento invariato dopo restart;
- rollback totale quando una failure viene iniettata dopo l'inserimento delle cinque righe ma
  prima dell'evento: nessuna tabella lineage residua e `user_version` ancora 2;
- successivo import valido dopo riapertura.

Questa parte del rilievo Claude derivava dal suo perimetro ristretto: il codice lineage è
effettivamente fail-closed e atomico.

### Difetto operativo del materializer

Riferimenti: `studio2/fase03/materialize_successor_recovery.py:84-280`.

`main()` non analizza opzioni e non richiede `--execute`, ACK o altro consenso operativo. Importare
il modulo e chiamare `main()` con percorsi sintetici sufficienti crea immediatamente il target.
La sonda ha inoltre iniettato una failure durante la copia dei tokenizer, dopo la creazione della
radice e delle prime directory. Il target parziale è rimasto sul filesystem e ogni rilancio è stato
rifiutato dal controllo iniziale `TARGET_ROOT.exists()`.

Il materializer protegge correttamente questi aspetti:

- rifiuta qualunque target già esistente, anche vuoto o parziale;
- non copia né crea un'authorization;
- non contiene chiamate di rete o provider;
- conserva SHA e directory del predecessore nella prova sintetica;
- valida la configurazione prima di scrivere il summary finale.

Il rifiuto di un target parziale impedisce l'overwrite, ma non rende atomica l'operazione: una
failure lascia un target non utilizzabile e non rilanciabile. Servono un gate esplicito e una
materializzazione in staging con rename atomico, oppure cleanup controllato verificabile prima
della pubblicazione della radice finale.

## 4. P2-01 — rivalidazione accounting su ledger misto

**Verdetto: CONFERMATO.**

Riferimenti: `studio2/fase03/technical_qualification_122b.py:185-209` e
`studio2/fase03/harness/ledger.py:606-632`.

La fixture ha creato, nell'ordine:

1. lineage successor valido;
2. qualifica tecnica PASS con accounting `enable_thinking=false`;
3. otto richieste producer valide con lo stesso contratto e outcome PASS;
4. un evento consumer valido senza kwargs e un secondo consumer che dimostra anche l'accettazione
   della kwarg producer-only;
5. restart e `tq.run(..., resume=True)`.

`validate_tokenizer_accounting_evidence` itera tutti gli eventi `tokenizer_accounting:*` con il
singolo guard no-thinking costruito dal runner tecnico. Il guard non può coincidere
contemporaneamente con gli eventi producer/technical che richiedono la kwarg e con il consumer che
non la usa. Il primo mismatch viene convertito in `FATAL_ACCOUNTING_ERROR` e persiste
`stop:tokenizer_accounting` nella stessa transazione.

Il punto decisionale precede `bind_stage`, il recupero del leaf e il controllo del record già
completo. Risultato osservato: zero nuove chiamate, nessun nuovo intent, 11 richieste native
invariate, ma una nuova scrittura STOP globale. Lo STOP blocca le successive decisioni contabili e
non esiste una normale API di rimozione o recovery.

Controlli positivi:

- la normale acquisizione consumer senza kwargs riesce prima del rilancio tecnico;
- senza evento misto, prima esecuzione e resume tecnico chiuso effettuano una sola chiamata totale,
  non creano STOP e restituiscono il record persistito.

La correzione deve scegliere il guard in base al contratto autenticato di ciascun evento, oppure
far rivalidare ogni evento dal proprio binding persistito. Un mismatch non deve essere causato
dall'applicazione di un contratto appartenente a un altro ruolo.

## 5. P2-02 — record tecnico completo senza outcome dopo crash

**Verdetto: CONFERMATO.**

Riferimento: `studio2/fase03/technical_qualification_122b.py:247-263` e ramo resume
`technical_qualification_122b.py:194-209`.

È stata iniettata una failure esattamente quando il runner chiama `record_stage_outcome`, dopo che
raw, accounting, link record e request `COMPLETED` erano già durevoli. Dopo restart,
`resume=True`:

- rivalida accounting e record;
- non invoca il transport;
- non crea un nuovo intent;
- non duplica la quota, che resta una richiesta tecnica;
- chiama `verify_stage_success` e fallisce perché manca `outcome:technical_qualification_122b`;
- lascia il database logicamente invariato rispetto allo stato post-crash.

Il comportamento è fail-closed ma non recuperabile. Tutti i dati necessari a costruire lo stesso
summary deterministico sono presenti, ma il runner non ricrea outcome e file summary. Il controllo
positivo con outcome normalmente chiuso esegue prima corsa e resume con una sola chiamata totale.

La correzione minima deve ricostruire summary e outcome dai record durevoli già autenticati, senza
trasporto, nuovo intent o nuova quota, e rendere idempotente anche il confine tra outcome SQLite e
scrittura del summary su filesystem.

## 6. Triage P2-03–P2-10

| ID | Classificazione | Evidenza e impatto |
|---|---|---|
| P2-03 | **CONFERMATO** | `d9.validate_binding` ritorna subito quando manca `execution_config`. Una sonda ha importato lineage successor, chiuso il tecnico e aperto producer tramite binding diretti privi di D9. I runner ordinari allegano la config, ma l'API ledger pubblica resta più permissiva e può mescolare binding con diversa forza contrattuale. |
| P2-04 | **CONFERMATO, limitato** | `_validate_accounting_contract` accetta la forma esatta no-thinking anche quando non è richiesta. Una richiesta consumer 122B l'ha persistita con successo. Il ramo provider 27B la rifiuta già; il finding non si estende quindi indistintamente al 27B. |
| P2-05 | **CONFERMATO** | `authorize_remediation` verifica diff, template, approval e alcuni record, ma non applica il guard STOP/suspension né riconferma l'outcome con `_closed_outcome`. `waive_remediation` accetta soltanto una stringa hash e crea l'evento senza file approvativo o prerequisito di stato. Difetto preesistente, non introdotto dal successor. |
| P2-06 | **CONFERMATO** | Le regex congelate usano singolari con `\b`. La prova `reactors valves feeds steps` produce zero finding. Estendere il vocabolario modifica però una regola scientifica congelata e richiede decisione/review autoriale. |
| P2-07 | **SCELTA NORMATIVA/AUTORIALE** | Il materializer genera meccanicamente l'approval lineage, ma la lega alla decisione autoriale che autorizza esattamente recovery offline e import exactly-once. Occorre stabilire se quella decisione è sufficiente o se l'approval debba essere un secondo atto distinto; non è un difetto tecnico dimostrato. |
| P2-08 | **NON RIPRODOTTO** | Il divieto D9 riguarda migrazione/reset/backfill automatici del ledger esistente. Il contratto recovery successivo autorizza esplicitamente un ledger successor fresco con import lineage S=5 e versione 4. La prova mostra che il predecessore non viene migrato o copiato. |
| P2-09 | **NON RIPRODOTTO** per quote; **COPERTURA MANCANTE** per indipendenza fixture lineage | `test_revisions` verifica sia `planned request maximum` sia `hard stop 200`, e la suite completa li esegue con esito verde. Le fixture lineage restano costruite con lo stesso builder del candidato; le mutazioni indipendenti riducono ma non eliminano questa circolarità. |
| P2-10 | **CONFERMATO** | `_record_consumed_fields` riconteggia campi derivabili dal raw, ma non ricalcola flag semantici. Una prova diretta ha chiuso un PASS tecnico usando raw `{"fixture":"raw"}` e flag `technical_pass/schema_valid` forniti dal chiamante. I runner normali valutano il raw, ma l'API diretta può materializzare una decisione non derivata indipendentemente. |

## 7. Triage P3

| Rilievo P3 | Classificazione | Nota |
|---|---|---|
| Fingerprint pinnato da una singola osservazione | **SCELTA NORMATIVA/AUTORIALE** | Il supplemento dichiara esplicitamente valore opaco osservato una volta e fail-closed a ogni variazione. Adeguatezza e stabilità del pin sono una scelta metodologica. |
| `identity_sha256` sul file anziché sul digest canonico proposto | **CONFERMATO** | Il materializer usa SHA file `dd9c53…`; il JSON canonico corrente vale `79515f…`, mentre la proposta cita `d18006…`. Provenienza e semantica del digest non coincidono e devono essere riallineate prima della config finale. |
| Materializzazione non transazionale | **CONFERMATO** | Failure intermedia lascia target parziale e il rerun lo rifiuta; incluso in P1-02. |
| Storico v3 non riautenticato contro file sorgente | **CONFERMATO** | `_validated_external_history` autentica righe/evento persistiti e sintassi hash, ma non conserva/rilegge riferimenti assoluti a package e approval come il lineage successor. Difetto legacy, non necessario al target successor fresco. |
| Eventi orfani non controllati all'import successor | **CONFERMATO** | Un evento normativo `outcome:producer_conformity` inserito prima dell'import non lo blocca e sopravvive nel ledger v4. |
| Flag decisionali fidati in `_record_consumed_fields` | **CONFERMATO** | Stessa evidenza di P2-10. |
| Stage tecnico ammesso su config/ledger non successor | **CONFERMATO** | `_prerequisites` impone il tecnico prima del producer solo se il classifier dice successor, ma non vieta di aprire il tecnico su generic; l'API diretta senza D9 lo consente. |
| Request 122B `FAILED` con raw ma senza accounting | **CONFERMATO** | `complete_request(status="FAILED")` accetta raw presente, record assente e `transport_failure=False`; la sonda ha chiuso così una richiesta 122B senza evento accounting. |
| Alternate PENDING/`pilot` nel target futuro | **FUORI PERIMETRO** | Il materializer eredita `alternate_placement` dalla config privata del predecessore, che non è stata aperta. Dai soli byte pubblici non è possibile stabilire il valore finale. |
| `SCHEMA_FREEZE.tag_created=false` | **FUORI PERIMETRO** | Stato pubblico intenzionalmente pending e separato dal recovery successor; non determina la sicurezza della sola materializzazione fresca. |
| Authorization non legata al commit del codice | **CONFERMATO, senza authorization corrente** | Il formato pubblico storico lega la configurazione canonica, non il commit harness. Il materializer successor rimuove correttamente ogni authorization, quindi il rischio riguarda un successivo atto di esecuzione. |
| Import S4 reale rispetto al contratto §8 | **FUORI PERIMETRO** | Richiederebbe il ledger privato reale, esplicitamente escluso. Le sole fixture non dimostrano quella provenienza storica. |

## 8. P1-01 — matrice scientifica neutrale

| Voce | Contratto/fatto | Conseguenza da decidere |
|---|---|---|
| Contratto originario | Producer 122B senza controllo thinking inviato; `max_tokens=2560` motivato come 2048 thinking + 512 riserva; prima osservazione dentro `producer_conformity`. | È la baseline rispetto alla quale dichiarare ogni deviazione. |
| Osservazione reale | Una chiamata addebitata; fingerprint non nullo inatteso; `identity_valid=false`; `finish_reason=length`; 2560 completion token consumati nel reasoning; content nullo e zero insight validi. | STOP identità resta corretto e S passa a 5; il raw non è risultato scientifico. |
| Classificazione V2 | Cap classe 3 e output strutturalmente invalido classe 1; entrambe le classi erano comprese nel regime T9, pur con stage incompleto 1/8. | Supporta l'interpretazione “prima invalidità T9”, ma il contratto non chiariva il conflitto con la qualificazione identitaria antecedente. |
| Scelta autoriale acquisita | `ANTECEDENT_QUALIFICATION_CONFIGURATION_FAILURE`; successor con S=5; nuova conformità base completa; T9 invariata e prima chiamata fuori T9; remediation non consumata. | È una decisione esplicita, ma va dichiarata come deviazione post-osservazione se usata per claim scientifici. |
| `enable_thinking=false` | Nuovo controllo esatto sul solo producer 122B; consumer 122B e 27B restano nei regimi precedenti. | Cambia il processo generativo del producer e crea asimmetria fra ruoli/modelli. |
| Cap 2560 | Conservato anche se il thinking è disattivato e viene aggiunta una qualifica da 32 token. | La giustificazione originaria 2048+512 non è più quella operativa; serve una nuova motivazione prespecificata. |
| Trattamento fuori T9 | La chiamata resta nel cumulativo ma non nel denominatore della conformità; una nuova base 8 è disponibile e la remediation resta intatta. | Aumenta le opportunità dopo aver osservato l'esito; occorre dichiarare il rischio di optional stopping e il nuovo estimand. |
| Comparabilità P/C/27B | P e C condividono il servizio nominale 122B ma non la modalità thinking; P_alt 27B resta invariato. | I confronti non isolano più soltanto ruolo o modello. Vanno trattati come configurazioni role-specific, con claim comparativi limitati. |
| Claim ancora solidi | Contabilità della chiamata osservata, S=5, immutabilità del predecessore, zero retry, provenienza lineage e fail-closed del STOP. | Restano claim tecnici/forensi. |
| Claim limitati | Efficacia producer 122B, parità P/C, confronto producer 122B/27B, interpretazione della remediation e generalità cross-model end-to-end. | Richiedono dichiarazione della deviazione e formulazione compatibile con i regimi differenti. |

### Alternative realmente disponibili all'autore

| Alternativa | Dati e quote | Comparabilità e paper |
|---|---|---|
| Confermare il successor no-thinking fuori T9 | S=5 preservato; 1 tecnica; nuova base producer 8; remediation intatta; massimo cumulativo 166. | Dichiarare deviazione post-osservazione, regime producer specifico e limite dei confronti P/C e P/27B; fornire nuova ragione per cap 2560. |
| Classificare la prima osservazione dentro T9 | La prima resta invalida nel denominatore. Il semplice completamento delle sette residue non soddisfa il contratto di outcome; una remediation completa richiederebbe atto separato, otto nuove chiamate e aggiornamento quote. | Mantiene continuità con la classificazione V2, ma il difetto osservato riguarda configurazione/thinking e non è dimostrato come difetto del solo prompt previsto dalla remediation. |
| Mantenere thinking originario e riqualificare con un cap diverso | Richiede nuovo piano, nuovo cap, nuova qualifica e nuove autorizzazioni; la chiamata osservata resta S=5. | Conserva maggiore simmetria P/C, ma cambia un parametro congelato dopo osservazione e richiede una nuova giustificazione statistica. |
| Non proseguire il producer 122B | Zero nuove chiamate producer; si conserva soltanto l'evidenza forense. | Elimina il rischio di recovery selettiva, ma rinuncia ai claim producer 122B e ai confronti P/C e P/27B previsti. |

La review non seleziona una di queste alternative.

## 9. Finding ordinati

### P0

Nessuno.

### P1

- **P1-02a — materializer senza gate operativo.** `main()` materializza appena invocato; manca un
  consenso esplicito equivalente ai runner esecutivi.
- **P1-02b — pubblicazione non atomica del target.** Una failure intermedia lascia una radice
  parziale che il rilancio non può completare né sostituire.
- **P1-01 — decisione scientifica pendente.** La scelta già acquisita è tecnicamente implementata,
  ma la deviazione, il cap e i claim comparativi devono essere assunti esplicitamente dall'autore.

P1-03 ambientale è chiuso dalla regressione Mac 200/200.

### P2

- **P2-01 — STOP globale falso su ledger accounting misto**, confermato prima del controllo leaf.
- **P2-02 — PASS tecnico non ricostruibile dopo crash**, confermato senza reinvio o doppia quota.
- **P2-03, P2-04, P2-05, P2-06 e P2-10**, confermati con i limiti riportati nella tabella.
- **P2-09**, residua soltanto come copertura indipendente delle fixture lineage; quote e hard stop
  sono già testati.

### P3

Restano i rilievi confermati e circoscritti della sezione 7. Quelli legati a config privata,
S4 reale o freeze schema non sono stati trasformati in conclusioni senza evidenza autorizzata.

## 10. Readiness e prossimo passo minimo

La sola materializzazione fresca **non è pronta** finché P1-02a/b non viene corretto e riverificato
su target sintetico. P2-01 e P2-02 devono essere corretti prima di qualunque qualifica tecnica o
resume reale. P1-01 richiede poi una decisione scientifica esplicita prima di qualsiasi pilot.

Prossimo passo minimo, interamente offline:

1. aggiungere gate esplicito e staging atomico al materializer, con test su failure intermedie,
   target parziale, restart e assenza di authorization;
2. correggere la rivalidazione accounting per evento e il recovery dell'outcome tecnico;
3. aggiungere test discriminanti per P2-03/P2-04/P2-05/P2-10 e per gli eventi orfani;
4. ottenere la scelta autoriale documentata fra le alternative della sezione 8;
5. ripetere suite mirata, 15 moduli e guardian sui byte finali.

## 11. Limiti e assenza di autorizzazione

Sono stati usati soltanto sorgenti versionati, fixture sintetiche e directory temporanee. Il
materializer è stato eseguito esclusivamente con costanti reindirizzate a un predecessore e target
sintetici. Nessun ledger privato è stato aperto con codice applicativo; nessun target fresco reale è
stato creato o modificato. Non sono stati contattati servizi 122B/27B, rete sperimentale o tunnel.
Non sono stati generati token, authorization o risultati scientifici. Nessun commit, push, merge o
tag è stato eseguito.

**Verdetto finale: READY FOR AUTHOR DECISION AND SEPARATE CORRECTION; NOT READY FOR SEPARATE
FRESH-TARGET MATERIALIZATION.** Nessuna materializzazione o chiamata è autorizzata.
