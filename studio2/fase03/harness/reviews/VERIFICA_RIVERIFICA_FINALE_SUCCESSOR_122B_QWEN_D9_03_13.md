# Riverifica finale QA indipendente del successor 122B — Qwen D9 03.13

## Verdetto

**NON OK**, limitato al commit `66f3cbfc1e294c8250c6c2102120705a0c3771dc`, tree
`e44ed15f74123331ef2a103e69ffc8457a7f3e79`, parent
`ef6d6ef550d59d11233f8f9dc4af6abd247dcff9`.

R1 e C1 risultano chiusi. R2 chiude le sette incoerenze contabili della qualifica tecnica
indicate dal verbale precedente, ma il contratto condiviso resta incompleto per il producer
successor 122B. C2 è applicato alla configurazione provider, ma non all'acquisizione e al riuso
della prova contabile persistita del producer. Una richiesta `producer_conformity` 122B può quindi
essere contabilizzata senza `chat_template_kwargs.enable_thinking=false`; dopo riapertura, la
prova viene accettata e una nuova richiesta dello stesso stage può essere prenotata.

Il rilievo è bloccante perché il controllo richiesto deve sopravvivere alla persistenza ed essere
applicato prima di nuove operazioni persistenti. Il verde delle suite versionate non copre questo
percorso diretto. Il presente verbale non abilita la preparazione di un target fresco e non
autorizza alcuna chiamata.

## Perimetro, identità e provenienza

Review svolta nella worktree indipendente
`/Users/luker/.codex/worktrees/b567/fot-tep` sul sorgente locale
`/Users/luker/.codex/worktrees/dd86/fot-tep`. Sono state applicate le lezioni
`fot-tep-harness-lessons` su contratto semantico condiviso, riuso dopo restart, stessi byte sul
parent, positivi necessari e assenza di effetti prima del rifiuto.

| Controllo | Risultato osservato |
|---|---|
| HEAD | `66f3cbfc1e294c8250c6c2102120705a0c3771dc` |
| Tree | `e44ed15f74123331ef2a103e69ffc8457a7f3e79` |
| Parent | `ef6d6ef550d59d11233f8f9dc4af6abd247dcff9` |
| Rapporto autore | SHA-256 `7d505122ba67a88e00e0b44af59735480c2d488d53ac7de0cdbfccb843866881` |
| Manifest | SHA-256 `acee4b3c2f06f0f37b89be41901b98fa072858b36586fe845626e9adb3d2f844` |
| Review precedente incorporata | SHA-256 `790ceb1e49dde5fba926a8e7b6b450ce8600651c2f6b74b5cda013b5ddc853bc` |
| 10 `repository_artifacts` del manifest | tutti ricalcolati e coincidenti |
| `git diff --check` | PASS |
| Worktree sorgente | pulita |

Il delta parent-candidato contiene 7 file, 801 inserimenti e 15 rimozioni: quattro file runtime o
test modificati e tre artefatti documentali. Non sono emerse modifiche a disegno scientifico,
quote, ruoli, prompt scientifici, denominatori o ordine degli stage. Restano massimo cumulativo
166, hard stop 200 e margine non spendibile 34.

## Rilievo bloccante — il no-thinking del producer non è parte del contratto contabile obbligatorio

Riferimenti: `studio2/fase03/harness/ledger.py:404-422`,
`studio2/fase03/harness/ledger.py:424-476`,
`studio2/fase03/harness/ledger.py:484-520`,
`studio2/fase03/harness/ledger.py:522-557` e
`studio2/fase03/harness/ledger.py:622-669`.

`_accounting_commitment` aggiunge `chat_template_kwargs` soltanto quando il guard ne fornisce uno.
Il validatore unico ammette sia il set di campi con kwargs sia quello senza kwargs; rende poi
l'assenza fatale esclusivamente quando `request['stage'] == technical_qualification_122b`. Per
`producer_conformity` e `producer_remediation`, una prova senza kwargs è quindi formalmente valida.
Lo stesso validatore incompleto è richiamato sia dalla prima acquisizione sia da
`_accounting_record_link`, che alimenta binding del record, completamento e riuso.

Questo non è compensato da `d9.validate_provider`: il runner ordinario valida il provider prima
del trasporto, ma il ledger deve autenticare autonomamente la prova durevole che abilita resume e
prenotazioni successive. Hash e link interni coerenti attestano i byte persistiti, non dimostrano
che la chiamata producer successor abbia usato il controllo richiesto.

Prova indipendente costruita esclusivamente con `SuccessorFixture` e API versionate:

1. import S=5 valido e qualifica tecnica PASS;
2. binding `producer_conformity` con otto richieste 122B;
3. prima prenotazione, raw locale e accounting tramite `TokenizerAccountingGuard` senza kwargs;
4. binding del record e completamento della prima richiesta;
5. riapertura con una nuova istanza di `PilotLedger`;
6. rivalidazione del record e prenotazione dell'indice successivo.

Risultato osservato:

```text
{'persisted_kwargs': 'ABSENT', 'reuse': 'ACCEPTED',
 'next_request_status': 'INTENT', 'native_requests': 3}
```

Il conteggio 3 è coerente con una richiesta tecnica, il primo producer completato e il secondo
producer appena prenotato. L'omissione viene dunque acquisita, resa durevole, accettata dopo
restart e usata per consentire una nuova operazione persistente.

La correzione deve portare nel validatore contabile il contesto caller-specific del successor e
richiedere la forma esatta `{"enable_thinking":false}` anche per i producer 122B degli stage
`producer_conformity` e `producer_remediation`, senza cambiare ledger generici, consumer o 27B.
Servono negativi distinti per acquisizione iniziale e riuso dopo restart, con confronto dello stato
prima/dopo e zero nuovi intent sul rifiuto.

## Esito di R1, R2, C1 e C2

### R1 — chiuso

In `ledger.py:268-331`, l'assenza di lineage su v2/v3 fallisce quando il caller D9 fornisce package
o approval. I test coprono validazione diretta, preflight, restart, binding e prenotazione e
verificano zero richieste persistite. Il positivo importa S=5, riapre, prenota la qualifica e
osserva cumulativo 6. Un controllo indipendente su un ledger v2 generico, senza riferimenti
successor, ha restituito `rows=[]`, `native_requests=0`: il comportamento non-successor resta
distinto.

### R2 — chiuso per i campi precedentemente segnalati, incompleto nel lifecycle producer

`_validate_accounting_contract` è condiviso da acquisizione e riuso e rifiuta le sette mutazioni
versionate di `messages`, conteggi locale/server, snapshot, identità richiesta, versione artefatto e
hash raw, anche con digest e link riallineati. I test includono same-instance, restart, verifica
dello stage, binding successivo e positivo.

Il rilievo sopra mostra però che il contratto non incorpora tutta la semantica necessaria per il
producer successor: l'obbligo no-thinking è limitato allo stage tecnico. R2 non può quindi essere
considerato chiuso come proprietà generale di acquisizione e riuso della prova 122B.

### C1 — chiuso

Contratto tecnico e validazione provider rifiutano l'assenza di `extra_body` e accettano la sola
forma esatta. Il pin del file provider resta in uso.

### C2 — non chiuso end-to-end

`d9.validate_provider` richiede la forma esatta per qualifica tecnica, conformità e remediation
del successor 122B. I negativi versionati coprono assenza, `0`, `true`, chiave aggiuntiva e forma
errata; il positivo 122B passa, così come il controllo 27B senza `extra_body`. Consumer e 27B non
sono modificati dal delta. Manca però lo stesso obbligo nel ledger contabile durevole, come provato
dal percorso sopra.

I rilievi F1/F2 originari restano coperti: il lineage v4 importato viene riautenticato e
`false -> 0` nella prova persistita viene rifiutato. Questi positivi non coprono l'omissione
iniziale nello stage producer.

## Test e riepiloghi effettivi

`test_successor_recovery.py` ha SHA-256
`2c557b600ad3b5555479b1adaf928de28b850adce62046b88e71e312b581625e`.

| Esecuzione | Metodi del runner | Subtest | Failure | Errori | Skip | Durata/esito |
|---|---:|---|---:|---:|---:|---|
| Candidato, suite mirata | 16 | i subtest PASS non sono totalizzati separatamente da `unittest` | 0 | 0 | 0 | 3,502 s, OK |
| Stessi byte sul parent | 16 | 7 failure associate a subtest, incluse R1/R2/C2 | 10 totali | 0 | 0 | 3,514 s, behavioral red atteso |
| Regressione completa, 15 moduli | 193 | i subtest PASS non sono totalizzati separatamente da `unittest` | 0 | 0 | 0 | 421,001 s, OK |
| Guardian documentale storico | 35 | riepilogo separato | 14 | 0 | 1 | NON PASS storico invariato |

Le 10 failure sul parent comprendono 7 failure di subtest e 3 failure a livello di metodo; non
sono errori di import o ambiente. La regressione completa comprende C01-C03, D01-D04, D9 e
correzioni, runner offline, riconciliazione storica, raccordo metrico, revisioni, successor,
accounting tokenizer, protocollo ed execution guard. Il risultato è stato letto dal riepilogo
finale del runner, non inferito dal solo exit code.

Il guardian documentale resta separato dalle regressioni runtime e non viene riclassificato come
PASS.

## Limiti e assenza di esecuzione

La verifica ha usato soltanto sorgenti, artefatti, fixture e test locali versionati. Non sono stati
aperti, letti o hashati artefatti runtime privati; non è stato creato o materializzato un target
fresco. Non sono stati contattati provider o servizi esterni, non sono stati aperti tunnel e non è
stata eseguita attività scientifica. Nessuna authorization è stata creata o concessa. Il candidato
non è stato modificato e non sono stati eseguiti commit, push, merge o tag.

**Verdetto finale: NON OK.** È richiesta una correzione del contratto contabile producer e una
nuova riverifica sugli stessi byte finali. Nessuna chiamata è autorizzata.
