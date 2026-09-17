# Riverifica QA indipendente del contratto contabile producer successor 122B — Qwen D9 03.13

## Verdetto

**NON OK**, limitato al commit `72fb93c6d26ceb220ed2cece1dac2ef6614c791f`, tree
`08577a5d86c4b2731a0d48ccd83ca48d916c37fa`, parent
`66f3cbfc1e294c8250c6c2102120705a0c3771dc`.

La correzione chiude il difetto dichiarato quando il ledger conserva lo stato nominale v4: prima
acquisizione e riuso passano dallo stesso validatore e richiedono il booleano esatto `false` per
conformità e remediation del producer successor 122B. La riverifica estesa ha però trovato che i
tre discriminatori che attivano il requisito — versione ledger, stage e modello della richiesta —
sono letti prima di autenticarli contro lineage e binding. Una loro forma non attesa fa restituire
“non successor” senza validare lo stato che giustifica quella classificazione.

Una retrocessione durevole di `PRAGMA user_version` da 4 a 2, lasciando presenti cinque righe di
lineage e il relativo evento, permette di riusare una prova priva dei kwargs, riconfermare lo
stage e prenotare una nuova richiesta. Lo stesso stato riporta zero predecessori. Il rilievo
riapre quindi anche R1 nella variante di incoerenza tra discriminatore di versione e artefatti
successor persistiti.

## Perimetro e provenienza

Review svolta nella worktree indipendente
`/Users/luker/.codex/worktrees/b567/fot-tep` sul sorgente locale
`/Users/luker/.codex/worktrees/dd86/fot-tep`. Sono state applicate le lezioni
`fot-tep-harness-lessons` su inventario normativo, contratto condiviso, mutazioni con digest
riallineati, API diretta, restart e controllo degli effetti prima della decisione protetta.

| Controllo | Risultato osservato |
|---|---|
| HEAD | `72fb93c6d26ceb220ed2cece1dac2ef6614c791f` |
| Tree | `08577a5d86c4b2731a0d48ccd83ca48d916c37fa` |
| Parent | `66f3cbfc1e294c8250c6c2102120705a0c3771dc` |
| Rapporto autore | SHA-256 `029eb567ed0c8fa1fcbe8cdd0e62f71c563b0ddcc7a8a7b4cbd60e62bca9e32d` |
| Manifest | SHA-256 `e956ec2ed3b0ebe69cae80e903da48d3c09215ef4f33367fbab0f1212f8e2c04` |
| Review precedente incorporata | SHA-256 `a44d1ea92de25d5628f3b50ab7367ed4b9127a605fca556d1fe0fb1829a11e8e` |
| 10 `repository_artifacts` del manifest | tutti ricalcolati e coincidenti |
| `git diff --check` | PASS |
| Worktree sorgente | pulita |

Il delta contiene 5 file, 667 inserimenti e 8 rimozioni. I soli file runtime/test modificati sono
`ledger.py` e `test_successor_recovery.py`; gli altri tre sono rapporto, manifest e copia del
verbale precedente. Non risultano modifiche a disegno scientifico, quote, ruoli, prompt,
denominatori o ordine degli stage. Restano massimo cumulativo 166, hard stop 200 e margine 34.

## Rilievo bloccante — classificazione successor disattivabile prima dell'autenticazione

Riferimenti: `studio2/fase03/harness/ledger.py:268-339`,
`studio2/fase03/harness/ledger.py:424-439`,
`studio2/fase03/harness/ledger.py:441-496` e
`studio2/fase03/harness/ledger.py:1252-1279`.

`_successor_122b_producer_accounting` restituisce `False` se stage, modello o
`PRAGMA user_version` non hanno già i valori attesi. Soltanto dopo questi tre controlli legge il
binding e confronta `stage_run`, identità, modello e producer. Il ramo negativo usa quindi campi
durevoli non ancora autenticati per decidere di non applicare la regola.

Il problema di versione si combina con `_quota_predecessors`: questo dispatcher chiama il
validatore completo del lineage soltanto quando `user_version == 4`; con valore 2 passa al
validatore generico, che accetta l'assenza di storico esterno e non rileva le righe/eventi
successor ancora presenti. Il validatore di lineage saprebbe rifiutare la versione diversa da 4,
ma non viene raggiunto.

Prova indipendente, costruita esclusivamente con `SuccessorFixture` e API versionate:

1. import valido di S=5, qualifica tecnica PASS e binding della conformità 122B;
2. prima richiesta completata con prova contabile valida e `enable_thinking=false`;
3. rimozione di `chat_template_kwargs` con riallineamento di event digest, request proof e record
   link, come nelle prove R2 già ammesse dal perimetro;
4. modifica di `PRAGMA user_version` da 4 a 2, senza rimuovere lineage o evento;
5. riapertura del ledger, riuso del record, rebind dello stage e prenotazione dell'indice 1.

Risultato osservato:

```text
{'user_version': 2,
 'lineage_rows_still_present': 5,
 'lineage_events_still_present': 1,
 'missing_kwargs_reuse': 'ACCEPTED',
 'reuse_and_rebind_writes': False,
 'next_request': 'INTENT',
 'reported_predecessors': 0}
```

Riuso e rebind non scrivono, ma accettano la baseline incoerente; la prenotazione successiva crea
poi un nuovo `INTENT`. Il risultato non è quindi limitato a una funzione diagnostica e sottoconta
nuovamente S=5.

Una seconda prova, mantenendo v4 ma cambiando soltanto `requests.model` da 122B a 27B e rimuovendo
i kwargs con link riallineati, ha prodotto:

```text
direct_reuse=ACCEPTED_WITHOUT_KWARGS_AFTER_MODEL_DOWNGRADE
```

Il rebind successivo rifiuta correttamente la difformità dal piano, ma l'API pubblica di riuso
della prova l'ha già dichiarata valida. Questo conferma che il difetto è l'ordine della
classificazione, non soltanto il dispatcher della quota.

La correzione deve distinguere un v2 realmente generico da uno stato che conserva artefatti
successor e deve autenticare lineage e binding prima di usare versione, stage o modello per
escludere il requisito. I nuovi test dovrebbero mutare separatamente i discriminatori dichiarati
nel manifest, coprendo API diretta, same-instance, restart, rebind e prenotazione, con stato logico
invariato sul rifiuto e zero nuovi intent. I positivi generic v2, consumer e 27B devono restare.

## Contratto nominale e confini verificati

Nel percorso v4 non modificato, `_validate_accounting_contract` è effettivamente condiviso da
prima acquisizione, rivalidazione dell'evento e `_accounting_record_link`. Assenza, `0`, `true`,
chiavi aggiuntive e forma diversa sono rifiutate per la conformità; l'omissione è rifiutata anche
per la remediation. Un controllo indipendente aggiuntivo ha verificato il positivo remediation:

```text
{'remediation_exact_false': 'ACCEPTED', 'status': 'COMPLETED'}
```

I test versionati confermano inoltre i positivi per ledger generico v2, consumer 122B e producer
alternativo 27B. Questi percorsi restano invariati nel delta.

R1, C1, F1/F2 e i sette controlli R2 precedenti risultano verdi nello stato nominale coperto dai
20 metodi. R1 non può però essere dichiarato chiuso rispetto all'inventario durevole completo,
perché la discordanza versione/lineage sopra descritta riabilita il sottoconteggio. C1, F1/F2, i
sette campi R2 e la validazione provider C2 non mostrano nuove regressioni nei casi eseguiti.

## Test e riepiloghi effettivi

`test_successor_recovery.py` ha SHA-256
`82c0fa5c39231691697d5f87afc7dff0edbed85060dfb0878678e9ec363a4b93`; la copia eseguita sul
parent aveva lo stesso hash.

| Esecuzione | Metodi | Subtest/failure | Errori | Skip | Durata/esito |
|---|---:|---|---:|---:|---|
| Candidato, suite mirata | 20 | 0 failure; i subtest PASS non sono conteggiati separatamente | 0 | 0 | 3,780 s, OK |
| Stessi byte sul parent | 20 | 6 failure totali: 3 di subtest e 3 a livello metodo | 0 | 0 | 3,715 s, behavioral red atteso |
| Regressione completa, 15 moduli | 197 | 0 failure; i subtest PASS non sono conteggiati separatamente | 0 | 0 | 427,192 s, OK |
| Guardian documentale storico | 35 | 14 failure | 0 | 1 | 0,078 s, NON PASS invariato |

Le sei failure sul parent riguardano acquisizione conformity, riuso/rebind/prenotazione dopo
restart e acquisizione remediation; non sono errori d'importazione o ambiente. La regressione
completa comprende C01-C03, D01-D04, D9 e correzioni, runner offline, riconciliazione storica,
raccordo metrico, revisioni, successor recovery, accounting tokenizer, protocollo ed execution
guard. I risultati sono stati letti dai riepiloghi finali del runner.

Il guardian documentale resta separato dalle regressioni runtime e non viene riclassificato come
PASS.

## Limiti e assenza di esecuzione

La verifica ha usato soltanto sorgenti, artefatti, fixture e test locali versionati. Non sono stati
aperti, letti o hashati artefatti runtime privati; non è stato creato o materializzato un target
fresco. Non sono stati contattati provider o servizi esterni, non sono stati aperti tunnel e non è
stata eseguita attività scientifica. Nessuna execution authorization è stata creata o concessa.
Il candidato non è stato modificato e non sono stati eseguiti commit, push, merge o tag.

**Verdetto finale: NON OK.** È richiesta una correzione della classificazione durable
successor/generic e una nuova riverifica sugli stessi byte finali. Nessuna chiamata è autorizzata.
