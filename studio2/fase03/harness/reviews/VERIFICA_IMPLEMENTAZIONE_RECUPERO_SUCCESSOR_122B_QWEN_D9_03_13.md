# Verifica indipendente implementazione successor 122B — Qwen D9 03.13

## Verdetto finale: NON OK

Completamento del 16 settembre 2026 nella worktree indipendente
`/Users/luker/.codex/worktrees/b567/fot-tep`, HEAD `15e56a89b0f377e6d90eef28ed941d4d54b5b00c`.
Il verbale di partenza, non tracciato, aveva SHA-256
`e4d1623d832fbf63abf28e860680f7250551ad1f521633c3a23c9b1b3ac79f93`, verificato prima della modifica.
**Questo completamento sostituisce il precedente OK provvisorio.**

Candidato esatto: `65dad03c7878b5ba1b3dc185861f93387bef78a0`, tree
`2df08d333d8c7e887bc70986a2819135d8bcad09`, parent
`6e15fe59fe7b2f69c3e74e0bbf344985fa696c36`, sorgente
`/Users/luker/.codex/worktrees/dd86/fot-tep`.

La rivalidazione del lineage dopo l'import non autentica tutti i campi durevoli contro il package
approvato. Una mutazione dell'ID del predecessore supera i controlli e permette una nuova
prenotazione con l'ID originale, anche dopo restart. È un difetto bloccante del requisito
fail-closed/exactly-once, riprodotto con controllo positivo e prima dell'eventuale trasporto.
Un secondo difetto riguarda l'accettazione del numero JSON `0` al posto del booleano `false`,
anche nell'evidence durevole di accounting.

Le regressioni native sono **186/186 PASS**, ma non coprono queste mutazioni. Il candidato non
riceve certificazione di readiness nemmeno per la singola qualifica tecnica finché F1 non è
corretto e riverificato. Non è autorizzata alcuna esecuzione.

## 1. Metodo e tutela degli artefatti

Mandato: `PROMPT_VERIFICA_IMPLEMENTAZIONE_RECUPERO_SUCCESSOR_122B_QWEN_D9_03_13.md`.
Applicata la skill `fot-tep-harness-lessons`, in particolare rivalidazione semantica delle prove
persistite, controlli prima degli intent e distinzione fra errori d'import e regressioni dimostrate.

Review offline/read-only del candidato. Le prove hanno usato fixture temporanee, copie SQLite
in memoria e database sacrificabili. Nessun costruttore `PilotLedger` è stato invocato sui ledger
reali; accesso reale solo SQLite `mode=ro&immutable=1`. Un audit hook Python ha vietato rete,
shell e scritture fuori dalla directory temporanea, propagando la protezione ai sottoprocessi;
bytecode disabilitato e `GIT_OPTIONAL_LOCKS=0`. I sottoprocessi ammessi erano Python e interrogazioni
git di sola lettura. Nessun provider, tunnel, token remoto, execution authorization, correzione
al candidato, commit, push, merge o tag.

I test d'orchestrazione che devono superare il confine di autorizzazione lo simulano con mock su
fixture: ciò è dichiarato sotto e non dimostra un bypass dell'authorization reale. La configurazione
reale continua a rifiutare `require_execution` prima di costruire ledger/client.

## 2. F1 — P1: lineage durevole alterato accettato prima di una nuova prenotazione

Riferimenti:
[confronto D9 incompleto](/Users/luker/.codex/worktrees/dd86/fot-tep/studio2/fase03/harness/d9.py:355),
[validazione strutturale del lineage](/Users/luker/.codex/worktrees/dd86/fot-tep/studio2/fase03/harness/ledger.py:262),
[controllo riuso degli ID](/Users/luker/.codex/worktrees/dd86/fot-tep/studio2/fase03/harness/ledger.py:769).

`validate_history` rilegge e valida correttamente package, approval e predecessore, ma poi confronta
con il ledger soltanto il numero di righe e `package_sha256`. `_validated_predecessor_lineage`
controlla struttura, ordinali, unicità, digest locale dell'identità e forma degli altri hash;
non collega ogni contenuto durevole alla corrispondente riga approvata e non confronta
`approval_sha256` dell'evento con l'approval effettivamente validata. Il ramo storico S=4 dello
stesso `validate_history` contiene invece un confronto semantico riga per riga.

Prova indipendente su copie **in memoria** del successore reale, con configurazione, package,
approval e predecessore reali letti immutabilmente; nessun mock del validatore:

| Mutazione isolata | Esito di `d9.validate_history` |
|---|---|
| Nessuna: controllo positivo | accettato correttamente |
| `request_id` della riga 5 sostituito | accettato erroneamente |
| `source_binding_sha256` della riga 5 sostituito con altro SHA formalmente valido | accettato erroneamente |
| `raw_sha256` della riga 5 sostituito | accettato erroneamente |
| `record_sha256` della riga 5 sostituito | accettato erroneamente |
| `identity_json` della riga 5 sostituito, con il solo hash locale riallineato | accettato erroneamente |
| `approval_sha256` nell'evento di riconciliazione sostituito | accettato erroneamente |

Il package, il suo hash e i file approvati restano invariati: non è stata costruita una nuova
approvazione per giustificare le righe alterate.

**Effetto sulla decisione, non soltanto su una diagnostica:** su una fixture importata validamente,
il tentativo di prenotare lo stage tecnico con l'ID nativo del predecessore viene inizialmente
rifiutato con `predecessor lineage cannot be reused as a native request or retry`. Dopo un solo
`UPDATE predecessor_lineage SET request_id=... WHERE ordinal=5`, un nuovo oggetto `PilotLedger`
sullo stesso database accetta quel medesimo ID originale: viene scritto un `INTENT`, cumulativo 6.
Il conteggio S resta 5, ma perde autenticità l'insieme degli ID su cui si basa il divieto di riuso.

La stessa prenotazione è stata riprodotta su una copia in memoria con **binding tecnico D9
completo**, provider/configurazione/snapshot e riferimenti reali. È stato simulato soltanto
`require_execution`, per esercitare offline la decisione successiva all'authorization senza
crearne una. Nessun mock di `validate_history`, `validate_binding`, `_quota_predecessors` o
`_insert_intent`: controllo positivo rifiutato, mutazione accettata, `requests=1`, stato `INTENT`.
La prova non afferma che la configurazione reale non autorizzata possa inviare richieste.

Riproduzione minima con sole fixture, da eseguire sul candidato con bytecode disabilitato:

```python
from studio2.fase03.harness.test_successor_recovery import (
    SuccessorFixture, _binding, _reserve, TECHNICAL_STAGE,
)
from studio2.fase03.harness.ledger import PilotLedger
from studio2.fase03.harness.common import HarnessError

f = SuccessorFixture()
f.setUp()
try:
    ledger = f.imported()
    with ledger._transaction() as c:
        old_id = c.execute(
            "SELECT request_id FROM predecessor_lineage WHERE ordinal=5"
        ).fetchone()[0]
    ledger.bind_stage(TECHNICAL_STAGE, _binding(TECHNICAL_STAGE, 1))
    try:
        _reserve(ledger, TECHNICAL_STAGE, 0, request_id=old_id)
        raise AssertionError("manca il rifiuto del controllo positivo")
    except HarnessError as exc:
        assert "predecessor lineage cannot be reused" in str(exc)
    with ledger._transaction() as c:
        c.execute("UPDATE predecessor_lineage SET request_id='mutated-id' WHERE ordinal=5")
    ledger = PilotLedger(ledger.path, pilot_id=ledger.pilot_id)
    _reserve(ledger, TECHNICAL_STAGE, 0, request_id=old_id)
    assert ledger.request(old_id)["status"] == "INTENT"  # difetto osservato
finally:
    f.tearDown()
    f.doCleanups()
```

Correzione richiesta, **non implementata in questa review**: autenticare l'intero lineage durevole
e l'evento contro le prove approvate, riusando la stessa validazione semantica prima di ogni
prenotazione/reimpiego nella transazione della decisione. Coprire i campi sopra con prove successive
all'import, same-instance/restart e API diretta/D9; dopo la mutazione devono restare zero nuovi intent.

## 3. F2 — P2: `0` non viene distinto dal booleano `false`

Riferimenti:
[extra_body](/Users/luker/.codex/worktrees/dd86/fot-tep/studio2/fase03/harness/d9.py:249),
[guard kwargs](/Users/luker/.codex/worktrees/dd86/fot-tep/studio2/fase03/harness/ledger.py:49),
[rivalidazione accounting](/Users/luker/.codex/worktrees/dd86/fot-tep/studio2/fase03/harness/ledger.py:417).

I confronti fra dizionari Python considerano `0 == False`. Di conseguenza:

- `producer_extra_body({"chat_template_kwargs":{"enable_thinking":0}}, model_role="122B")`
  accetta la forma alterata e la normalizza a `false`;
- `TokenizerAccountingGuard(..., template_kwargs={"enable_thinking":0})` la accetta conservando `0`;
- nel template pin-nato Qwen, `false` produce **42** token per il prompt tecnico, mentre `0`
  produce **40**, come `true`: la differenza è stata misurata con il tokenizer reale;
- dopo un PASS tecnico simulato, sostituire soltanto `false` con `0` nei kwargs di `detail_json`
  dell'evento `tokenizer_accounting`, senza aggiornare l'hash dell'evento o il proof della richiesta,
  supera `validate_tokenizer_accounting_evidence` con guard corretto `false`.

Quest'ultima prova passa perché il confronto `detail != expected` non distingue i due tipi e
l'hash verificato è quello di `expected`, non un digest ricalcolato dal dettaglio persistito.
Le mutazioni di controllo — rimozione kwargs, `true`, chiave aggiuntiva — sono invece rifiutate
con STOP durevole `persisted accounting evidence binding is corrupted`.

Il normale percorso da file del provider materializzato usa già il vero booleano `false` e lo
passa coerentemente al guard: **non è stato osservato un invio scorretto da quella configurazione**.
Il difetto riguarda il contratto di rifiuto delle forme alterate e l'esattezza della prova durevole.
Richiesti controllo di tipo/valore booleano e verifica del digest del dettaglio effettivamente letto,
con regressione `false → 0`; nessuna correzione eseguita.

## 4. Commit, artefatti e configurazione materializzata

| Verifica rieseguita sul Mac | Risultato |
|---|---|
| HEAD/tree/parent dd86 | coincidono con il mandato; worktree pulita |
| Delta | 13 file, 10 aggiunti e 3 modificati; 2176 inserimenti, 35 rimozioni; `diff --check` PASS |
| 11 `repository_artifacts` del manifest | tutti gli SHA ricalcolati coincidenti |
| Manifest | `18dba5fc5f5241c50982ca2de4b176b7cceaeaf5d69f2ef26db23550e80eb691` |
| Rapporto autore | `089b988938fc79e04833d2d00f40236d6c0621050c18cfc2e284e8f784e23e9b` |
| Contratto | `143e709a534c6143efb8989dff85f0ba4a1f4b7139897e2d08f2556f1dd6f37a` |
| Configurazione successore | `f21b33a5e9a625ca8fa9f08711a09d456ee613b23b1f7f447faf6b26bd114067` |
| Package lineage / approval | `64b37439761d482d285baf5717fc50947dd4ca42afd745eb9a2224842fbee2a5` / `192a648f0acabc90406a8af6e45506cb635925bafb37a78437287a3c72faf03d` |
| Supplemento, producer/service 122B, summary privati | SHA coincidenti con il manifest |
| Permessi nativi | root e directory `0700`, tutti i file `0600`; nessuna difformità |
| Execution authorization | assente; `require_execution` reale rifiuta la configurazione |
| Segreti nel delta versionato | nessuna occorrenza nei pattern URL/IP/credenziali controllati; nessun valore privato riportato |
| Producer e service 27B | byte-identici ai corrispondenti del predecessore |
| Snapshot tokenizer | tutti i 7 file byte-identici fra predecessore e successore |

Il controllo della decisione autore eseguito dal validatore ricalcola il digest UTF-8 del testo e
verifica le selezioni: antecedente di qualificazione/configurazione, import S=5, controllo producer,
una qualifica tecnica, invarianti consumer/T9/remediation e budget. L'import approval non equivale
a execution authorization. Lo stato materializzato resta `READY_FOR_INDEPENDENT_REVIEW`.

Il supplemento conserva `vllm-0.27.1-934a3247` come valore opaco esatto, con non-inferenze su
versione, pesi, quantizzazione, parser e capability. Alias/fingerprint sono comuni al servizio
122B; no-thinking è specifico del producer. Consumer/sonda/gate e candidati di thinking budget
restano fuori dalla modifica; `run_pilot.py` non è nel delta.

## 5. Lineage reale, import e quote

Ricostruzione ripetuta dal predecessore immutabile con il validatore, quindi confronto indipendente
**di tutti i campi** di ciascuna riga materializzata: ordinal, request_id, source_kind, identità e
relativo digest, source_binding_sha256, disposizione, raw/record SHA, package e predecessore.
**5/5 coincidono prima delle mutazioni di prova.**

Le prime quattro righe corrispondono allo storico: una `HISTORICAL_OUTCOME_UNCERTAIN`, tre
`COMPLETED`. La quinta è l'unica richiesta nativa `producer_conformity`, `COMPLETED`,
`identity_valid=false`, con evento di sospensione e senza outcome; disposizione
`COMPLETED_IDENTITY_INVALID_ANTECEDENT_CONFIGURATION`. Il predecessore ha esattamente quattro
storiche e una nativa; i digest raw/record sono ricalcolati dal contenuto. Il successore ha
`user_version=4`, integrity `ok`, 5 righe di lineage e **0 requests/responses/stages**, nessuna tabella
`external_history`: è un ledger nuovo, non una copia del predecessore.

L'import iniziale usa `BEGIN IMMEDIATE`, richiede v2 fresco e valida gli artefatti prima di creare
la tabella/inserire righe. La suite finale copre import parziale/selettivo/tampered/transitivo,
exactly-once, riuso request/retry e restart. Prova aggiuntiva nativa: rimosso l'evento `suspended:`
da una fixture predecessore, riallineati tutti i riferimenti/hash della fixture per raggiungere
il controllo semantico, l'import rifiuta con `not the required suspended STOP` e il dump logico del
successore resta identico. Questi positivi non coprono la corruzione **successiva all'import** di F1.

Quote nel codice: i predecessori concorrono alle prenotazioni e al hard stop; `quota_kind=technical`
è esclusivo e separato dalla riserva `8r+t≤15`, ma conta fra i tentativi nativi. Nessun retry tecnico.

| Valore | Ricalcolo / osservazione |
|---|---|
| Lineage | 5 |
| Qualifica tecnica | 1 |
| Massimo futuro oltre la qualifica | 160 |
| Massimo cumulativo con alternativo | **166** = 5 + 1 + 160 |
| Senza alternativo | 158 = 5 + 1 + 152 |
| Hard stop / margine non spendibile | 200 / **34** |
| Remediation reale | 0, non autorizzata |

La race versionata con due processi sull'ultimo slot 165→166 passa: un solo vincitore, cumulativo
166. È compresa nei 186 test, non un conteggio aggiuntivo. Nessun cambiamento di budget proposto.

## 6. Qualifica tecnica, rendering e accounting

Prompt, schema con `status=NO_THINKING_OK`, risposta, cap **32**, extra_body, assenza di retry e
uso scientifico `FORBIDDEN` sono prespecificati. L'entrypoint verifica il contratto, conserva kwargs
nel binding/spec/commitment e costruisce un payload con `max_tokens=32` e JSON schema strict.
La quota limita lo stage a una richiesta; producer_conformity richiede il suo PASS. T9 non viene
consumato dalla qualifica tecnica, il suo output non è un insight.

Prove native d'orchestrazione di `technical_qualification_122b.run` su fixture:

| Scenario | Esito osservato |
|---|---|
| Risposta valida | PASS, outcome, resume senza reinvio; conformità successiva ammessa |
| Fingerprint diverso | STOP; nessuna seconda chiamata |
| Reasoning presente | STOP; nessuna seconda chiamata |
| Schema diverso | STOP; nessuna seconda chiamata |
| `finish_reason=length` | STOP; nessuna seconda chiamata |
| Accounting 42 locale / 40 server simulato | `FATAL_ACCOUNTING_ERROR`, STOP durevole |
| Eccezione trasporto | tentativo FAILED addebitato, nessun retry |

In ogni scenario: una sola invocazione del trasporto **finto**, cumulativo 6; reinvocazioni con e
senza resume non inviano di nuovo. Dopo restart, conformità rifiutata per tutti i casi non PASS.
Sono 7 scenari supplementari, non chiamate reali. In queste prove sono simulati autorizzazione,
plumbing config/provider, verifica snapshot e tokenizer; restano reali runner, ledger, riserva,
persistenza/accounting, valutatore e blocchi di lifecycle. La prova indipendente del tokenizer
reale e quella del binding D9 completo sono distinte, descritte rispettivamente sotto e in F1.
L'entrypoint diretto/CLI non autorizzato è inoltre coperto dalla suite versionata.

Rendering reale offline: Python **3.13.15 x86_64**, Transformers **5.16.1**, tokenizers **0.23.2**,
Jinja2 **3.1.6**, snapshot locale
`Qwen/Qwen3.5-122B-A10B-FP8@a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9`;
nessun download, caricamento dei soli tokenizer. `apply_chat_template` restituisce `BatchEncoding`.

- `enable_thinking=false`: **42** token; hash del testo renderizzato
  `44de03ff9eb8bc92b36039cc95d6cc5ded93937d8f91422f9b2b9470c8ee5daf`;
  suffisso `<think>\n\n</think>\n\n` presente; guard reale conferma 42/42.
- `true` oppure `0`: **40** token; hash
  `9fe2299f5da3b7e0810cd2892311f877a48121d4b63d2ebf3bf164060e5216ff`.
- Risposta canonica `{"status":"NO_THINKING_OK"}`: **9** token; 9 + riserva fissa 23 = cap 32.
- Omissione kwargs con conteggio atteso 42: mismatch 40/42; `true` e chiavi aggiuntive rifiutati
  dal guard. La mutazione numerica e quella dell'evidence durevole sono F2.

Questa prova chiude il limite della VM relativo all'assenza di Transformers. Non dimostra il
supporto del server: nessun server è stato contattato.

## 7. Suite e provenienza dei risultati

Regressione nativa eseguita con `/Users/luker/.venvs/fot-tep-condition-c-r10/bin/python`,
Python **3.13.9 arm64**: caricamento di tutti i 13 moduli `harness/test_*.py` di primo livello più
`tests.test_protocol` e `tests.test_execution_guard`, dal sorgente esatto dd86. Risultato letto dal
runner: **186 test, 0 failure, 0 error, 0 skip**, durata **451,059 s**.

| Modulo | Test PASS |
|---|---:|
| test_c01_c03 | 14 |
| test_d01_replay | 7 |
| test_d02_predecessors | 8 |
| test_d03_contract | 9 |
| test_d04_open_quota | 8 |
| test_d9 | 17 |
| test_d9_corrections | 11 |
| test_harness_offline | 20 |
| test_history_reconciliation | 10 |
| test_metric_raccordo | 9 |
| test_revisions | 37 |
| test_successor_recovery | 9 |
| test_tokenizer_accounting | 10 |
| tests.test_protocol | 13 |
| tests.test_execution_guard | 4 |
| **Totale** | **186** |

La suite discriminante finale mantiene SHA-256
`9c0b51b2c92b67f1f8bc4dd0bca13ae6261d2c3991fd571be25b9fa52c82b4be`:
**candidato 9/9 PASS**, inclusi nel totale; stessi byte sul parent estratto dagli oggetti git:
**9 test, 9 ERROR**, per interfacce/moduli assenti e parametro `template_kwargs` non supportato.
Non vengono chiamati «nove regressioni comportamentali»: gli errori di import non esercitano la
logica. Il confine del candidato è stato esercitato separatamente con controlli positivi, import,
orchestrazione, rendering reale e mutazioni F1/F2; queste ultime dimostrano difetti ancora presenti.

**10 iniziali → 9 finali:** il log git del file contiene soltanto il commit candidato; né contratto,
manifest né rapporto consegnano i byte della versione iniziale a 10 test o il suo diff. Non è
possibile stabilire quale test sia stato eliminato o certificare che non sia stato indebolito.
La copertura finale non include F1/F2. Serve conservare/rendere ispezionabile quella versione e
aggiungere regressioni dei difetti dimostrati; il solo confronto 10→9 dichiarato non è una prova.

Guardian separato `docs.test_explanation`: **35 test, 14 failure, 0 error, 1 skip**, NON PASS storico
atteso. Le failure riguardano i controlli documentali Condition C, struttura dei titoli e risultati/
fatti Qwen step 27; file guardian/documenti fuori dal delta. Non riclassificato PASS e non sommato
alle regressioni.

Il verbale iniziale riportava prove in VM, regressioni parzialmente bloccate e uno script aggiuntivo
a 40 casi. Sono evidenze della precedente fase, **non riesecuzioni native qui conteggiate**.
La regressione nativa a 186 supera il limite dei percorsi Mac della VM e comprende i test di questa
review; non va sommata ai 140 dichiarati dall'autore né ai conteggi precedenti.

## 8. Integrità finale e limiti residui

Ledger reali, SHA-256 prima e dopo:

- predecessore `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-001/ledger.sqlite3`:
  `4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`;
- successore `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-002/ledger.sqlite3`:
  `9c9101826d2cb39498c1e8d0b167921680c38f045aa156220a3a4ba077ed304b`.

Hash invariati; anche l'inventario dei 56 file privati, acquisito durante il completamento, non
presenta variazioni al controllo finale. I 11 hash di sorgente del manifest restano coincidenti,
worktree dd86 pulita. La sola consegna persistente di questa ripresa è questo verbale in b567,
ancora non tracciato; nessun commit.

Limiti distinti dai difetti: versione iniziale dei 10 test non disponibile; supporto server non
provato né richiesto offline; `json.loads` del valutatore tecnico non rifiuta chiavi duplicate,
come già annotato nella prima fase, senza farne la ragione del verdetto. Il rendering locale,
i permessi nativi e le regressioni Mac prima mancanti sono invece stati verificati.

**NON OK per il candidato esatto.** F1 è sufficiente al verdetto; F2 richiede anch'esso chiusura
per l'esattezza dichiarata del contratto. Necessaria una correzione separata con prove
comportamentali delle mutazioni e successiva review. Nessuna readiness o authorization per
qualifica tecnica, T9, 27B, consumer, sonda o gate viene rilasciata da questo verbale.
