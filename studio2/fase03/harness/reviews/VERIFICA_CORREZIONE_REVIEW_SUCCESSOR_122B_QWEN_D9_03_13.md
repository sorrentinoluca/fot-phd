# Riverifica QA indipendente della correzione successor 122B — Qwen D9 03.13

## Verdetto

**NON OK**, limitato al commit `ef6d6ef550d59d11233f8f9dc4af6abd247dcff9`, tree
`47610aee32a3a1bfddc650edda4b81fc583a0155`, parent
`65dad03c7878b5ba1b3dc185861f93387bef78a0`.

Le correzioni chiudono i due esempi specifici F1 e F2 della review precedente: un lineage v4 già
importato viene autenticato campo per campo contro package, approval e predecessore; il numero JSON
`0` viene distinto dal booleano `false`, anche quando i digest della prova contabile vengono
riallineati. La riverifica estesa ha però trovato due nuovi percorsi incompleti:

1. il percorso D9 accetta un ledger v2 fresco che non ha ancora importato S=5 e permette una
   prenotazione conteggiata come 1 anziché 6;
2. il riuso diretto di una qualifica tecnica chiusa accetta modifiche semanticamente incoerenti
   della prova contabile quando i collegamenti interni vengono riallineati, e permette di creare il
   binding persistente dello stage successivo.

Il primo rilievo riguarda esattamente la futura inizializzazione fresca che un eventuale OK avrebbe
abilitato ed è sufficiente a bloccare il verdetto. Nessuna preparazione di target fresco e nessuna
esecuzione sono autorizzate da questo verbale.

## Perimetro e provenienza

Review eseguita nella worktree indipendente
`/Users/luker/.codex/worktrees/b567/fot-tep` sul sorgente locale
`/Users/luker/.codex/worktrees/dd86/fot-tep`. Applicate le lezioni
`fot-tep-harness-lessons` relative a rivalidazione semantica, stessi byte sul parent, controlli
positivi, restart e assenza di effetti prima del rifiuto.

Il prompt aggiornato limita la verifica a sorgenti, artefatti e test locali versionati. Non sono
stati aperti o letti artefatti runtime privati, non è stato creato un nuovo target e non sono stati
contattati servizi esterni. Nessuna execution authorization, chiamata provider, esecuzione
scientifica, modifica del candidato, commit, push, merge o tag.

Identità e artefatti:

| Controllo | Risultato |
|---|---|
| HEAD / tree / parent della worktree dd86 | coincidono con il mandato |
| Rapporto autore | SHA-256 `e0dfe425bf3d0383cb04afbf3c9550c703597842d489121240fab14f3be82a75` |
| Manifest | SHA-256 `7f81b29de49b01e2c2fe6bb01e010858de81908e38a06b2c918ad2e01eacaf50` |
| Review NON OK incorporata | byte-identica, SHA-256 `58ca090df717cbce192767c71679fc127047a2472cda0e722c6b7702a82857b5` |
| 10 `repository_artifacts` del manifest | tutti ricalcolati e coincidenti |
| `git diff --check` | PASS |
| worktree sorgente | pulita |

Il delta rispetto al parent contiene 7 file, 899 inserimenti e 51 rimozioni: quattro file runtime o
test modificati, rapporto/manifest aggiunti e copia della review precedente. L'ispezione del delta
non rileva modifiche a disegno scientifico, quote, ruoli, prompt scientifici o ordine degli stage.
Restano massimo cumulativo 166, hard stop 200 e margine 34.

## R1 — lineage richiesto accettato come assente su un target v2 fresco

Riferimenti: `studio2/fase03/harness/ledger.py:267-275`,
`studio2/fase03/harness/d9.py:356-365`, `studio2/fase03/harness/guards.py:132-139` e
`studio2/fase03/harness/ledger.py:814-826`.

`d9.validate_history` passa esplicitamente package e approval a
`PilotLedger._validated_predecessor_lineage`. Il validatore, tuttavia, restituisce immediatamente
`[]` quando non trova righe/eventi e `user_version` è 2 o 3. La condizione non distingue il normale
uso generico, nel quale l'assenza di lineage può essere lecita, dal percorso D9 che ha fornito due
riferimenti e quindi richiede l'import esatto S=5.

Prova indipendente con sole fixture versionate:

1. creato un `PilotLedger` v2 fresco e generati package/approval validi per quel target, senza
   chiamare `reconcile_successor_lineage`;
2. `_validated_predecessor_lineage(..., package_path=..., approval_path=...)` ha restituito `[]`;
3. `d9.validate_history` ha accettato lo stato; il dump logico è rimasto invariato perché questa
   validazione da sola non scrive;
4. binding e prenotazione tecnica diretta sono stati accettati: stato `INTENT`, `native_requests=1`,
   `requests_cumulative=1`, `predecessor_lineage_requests=0`.

Il percorso decisionale non è soltanto diagnostico. `require_pilot_ledger` chiama
`validate_history` e poi l'inventario nella stessa transazione; la prenotazione usa
`_quota_predecessors`, che su v2 ricade sullo storico esterno vuoto. In presenza della normale
authorization separata, lo stesso stato potrebbe quindi superare il preflight e sottocontare S=5.

Controlli positivi e di confine:

- un import fresco valido persiste una sola volta `package_reference` e `approval_reference`, conta
  5 predecessori e, dopo riapertura, continua a contare 5;
- una forma v4 cui sono stati rimossi entrambi i riferimenti viene rifiutata con
  `successor lineage event is corrupted`; dump logico invariato;
- non è stato osservato alcun backfill automatico;
- tutti i 12 campi dell'evento provati separatamente (nome, artifact SHA, status, count, tre SHA,
  path/SHA dei due riferimenti e chiave aggiuntiva) sono rifiutati dopo l'import, senza nuove
  scritture.

Quindi la scelta fail-closed per il vecchio v4 e la persistenza sul nuovo v4 sono corrette; manca
il requisito che il target destinato al successor sia realmente passato da v2 a v4 prima di ogni
operazione protetta. La correzione dovrà mantenere il ritorno `[]` per i ledger generici, ma
rifiutare l'assenza quando package/approval sono stati richiesti dal percorso D9. La regressione
deve coprire `require_pilot_ledger`, API diretta, riapertura e zero nuovi intent.

## R2 — riuso chiuso non rivalida semanticamente l'intera prova contabile

Riferimenti: `studio2/fase03/harness/ledger.py:430-466`,
`studio2/fase03/harness/ledger.py:561-595`, `studio2/fase03/harness/ledger.py:1058-1071` e
`studio2/fase03/harness/ledger.py:1211-1243`.

`_validate_accounting_event` ricostruisce correttamente il commitment atteso quando riceve guard e
messages. Il percorso di riuso chiuso passa invece da `_accounting_record_link`: ricalcola il digest
del dettaglio effettivamente persistito e verifica il tipo dei kwargs, ma non ricostruisce il
contratto completo di quel dettaglio. `_evaluated_record`, `_closed_outcome`,
`verify_stage_success` e la precondizione del producer riusano questo controllo più ristretto.

Prova indipendente su sette fixture, ciascuna partita da una qualifica tecnica valida e chiusa. È
stato modificato separatamente uno dei campi `messages`, `local_prompt_tokens`,
`server_prompt_tokens`, `snapshot`, `request_identity_sha256`, `artifact_version` e
`raw_response_sha256`; sono poi stati riallineati il digest dell'evento, `requests.proof_sha256` e
il link `tokenizer_accounting_record`. Per tutti i sette casi:

- `verify_stage_success(technical_qualification_122b)` ha accettato dopo restart;
- la sola verifica non ha scritto nulla;
- `bind_stage(producer_conformity, ...)` ha accettato e creato una riga persistente dello stage.

Il runner ordinario chiama anche `validate_tokenizer_accounting_evidence` con guard e messages e
offre quindi una barriera ulteriore. Il ledger espone però percorsi diretti e di riuso che vengono
consumati dalle precondizioni; un insieme di hash internamente coerente non deve sostituire la
rivalidazione semantica completa. La correzione dovrebbe riusare un unico contratto nei percorsi
di acquisizione e riuso, oppure rendere impossibile autorizzare lo stage successivo senza i dati
necessari alla ricostruzione.

## Chiusura dei rilievi originari F1/F2

Per un lineage v4 correttamente importato, il nuovo validatore riapre package, approval e
predecessore, confronta l'evento completo e tutti gli 11 campi di ciascuna riga approvata. Le 12
mutazioni di riga versionate passano su same-instance/restart; le 12 mutazioni aggiuntive
dell'evento sopra descritte sono state tutte rifiutate. F1 originario è quindi chiuso nel suo
scenario post-import, ma R1 lascia incompleto il lifecycle del target fresco.

Per F2, sono stati verificati rifiuti distinti di `enable_thinking=0` in:

- `producer_extra_body`;
- costruttore `TokenizerAccountingGuard`;
- contratto `technical_qualification_122b`;
- prova contabile persistita, anche riallineando event hash, request proof e record-link hash.

Quest'ultimo rifiuto avviene dopo restart senza modificare il dump logico. Omissione, `true` e
chiavi aggiuntive restano rifiutate dai test. F2 originario è chiuso; R2 riguarda gli altri campi
normativi della stessa prova.

## Test eseguiti

Suite finale `test_successor_recovery.py`, SHA-256
`bb643a43c8e670eb2b80461f04ad2fa8d2ce999b6b1277428221af618706b3ba`:

- candidato corretto: **12 metodi, 12 PASS**, 0 failure, 0 error;
- stessi byte sul parent respinto estratto dagli oggetti git: **12 metodi, 11 failure
  comportamentali, 0 error**.

Le failure parent includono `0` nel producer/guard, `false → 0` persistito, sei mutazioni D9 e il
riuso dell'ID predecessore con scrittura dell'intent. Non sono errori di import. I controlli
positivi dei test finali raggiungono import valido, prenotazione valida, D9 valido e stage successivo
valido. Le nuove prove R1/R2 non sono presenti nei 12 metodi, motivo per cui il verde mirato non è
sufficiente al verdetto.

Regressione completa prevista dal progetto, eseguita sui 15 moduli dichiarati nel manifest:
**189 test, 189 PASS, 0 failure, 0 error, 0 skip**, durata osservata **433,505 s**. Il risultato è
stato letto dal riepilogo finale del runner, non dedotto dal suo exit code.

Guardian documentale separato: **35 test, 14 failure, 0 error, 1 skip**, risultato storico NON PASS
invariato. Non viene riclassificato né sommato alle regressioni runtime.

## Stato v4 e conclusione

La forma v4 antecedente priva dei nuovi riferimenti fallisce in modo conservativo; il codice non
applica migrazioni o backfill. Una inizializzazione locale valida persiste i due riferimenti e li
rivalida dopo riapertura. Inizializzazione e authorization restano operazioni distinte.

Il ricorso futuro a un target fresco è una conseguenza corretta del contratto fail-closed per il
vecchio v4, ma il candidato corrente non impone che il target fresco completi l'import prima del
preflight D9. Pertanto il passo successivo non è ancora abilitato.

**Verdetto finale: NON OK.** Richiesta una nuova correzione e riverifica di R1 e R2 sugli stessi
byte finali, conservando i positivi esistenti e verificando zero effetti rispetto alla baseline già
incoerente. Nessuna esecuzione è stata autorizzata.
