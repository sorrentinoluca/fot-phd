# Riverifica indipendente R1 accounting BatchEncoding 122B — 03.13

Esito: **OK**. Data: 2026-09-16.

R1 è chiuso: lo stesso test finale riproduce entrambi i difetti sul parent e passa
sul candidato; il guard corretto accetta i conteggi esatti degli otto prompt 122B
e rifiuta il valore 2 in tutti gli otto casi. Le regressioni richieste passano:
**112 test distinti, zero failure, zero errori, zero skip**.

L'OK certifica l'intero candidato `d48477fdab12883eb71ebd2aef3293b56e9feb4a`
come pronto per la successiva decisione esplicita dell'autore sullo SHA canonico
`1305c158a98c40cb57e45b43e8d872d3d66e4d6d050d1d167c91b23e0a2fccc8`.
**Non autorizza Qwen, tunnel, pilot, gate o scritture nel ledger reale.**

## Perimetro verificato

- Commit: `d48477fdab12883eb71ebd2aef3293b56e9feb4a`.
- Tree: `6848a1e66d8ade56a3efa515eeb731260bdc5443`.
- Parent: `b83048af49f63657cc91c6ceb519299e6d61567c`.
- Sorgente: `/Users/luker/.codex/worktrees/dd86/fot-tep`, pulita prima e dopo,
  HEAD coincidente con il candidato. Nessuna modifica alla sorgente.
- Worktree indipendente: `/Users/luker/.codex/worktrees/b567/fot-tep`.
- Verbale NON OK originario conservato integralmente, SHA-256
  `2b1bad43e206560a71adc9e18cb15077d28c0a0419d6906f89f1f1eaed5cf11f`.

Il delta Git è esattamente quello richiesto, senza ulteriori file:

| Stato | File relativo a `studio2/fase03` |
| --- | --- |
| A | `harness/CORREZIONE_ACCOUNTING_BATCHENCODING_122B_03_13.manifest.json` |
| A | `harness/REPORT_CORREZIONE_ACCOUNTING_BATCHENCODING_122B_03_13.md` |
| M | `harness/common.py` |
| M | `harness/ledger.py` |
| M | `harness/test_tokenizer_accounting.py` |
| M | `prepare_gate.py` |
| M | `tests/test_protocol.py` |

SHA-256 ricalcolati:

| Artefatto | SHA-256 |
| --- | --- |
| Manifest correttivo | `4d1c98d7e623982b390438731cd5d1224daa8fffe7696b0911da89eeb4d7d420` |
| Rapporto correttivo | `891065e8b1c45fcf01d19906925075ce63875c1b73ef0bb272cd1f0060563fc6` |
| `harness/common.py` | `bd2636bc4f98f98c8a029ebcd08bd87c11917a31bf722e7c92849da4bffb56a0` |
| `harness/ledger.py` | `51987992378a9fcebe201ad9987c94066da65dd165531b93610c5d324e9c2bd6` |
| `prepare_gate.py` | `d9c85552959c73e95a47675d792969b532529e8c5baf659634dec8ad747a135d` |
| Test accounting finale | `90ac1bd393a52c6d6d50a7223cb7bee0961488f3b0ad65693ed065080371c52f` |
| Test protocol finale | `4e4b82650790fd69cf4f7f98f2f99097f6d700ab0ec94191c6867122cf9a79e5` |

## Implementazione condivisa e contratto fail-closed

`git grep` sul commit, limitato ai file Python, trova una sola definizione di
`tokenized_length`: `harness/common.py:16`. Il confronto a runtime conferma:

```python
common.tokenized_length is ledger.tokenized_length is prepare_gate.tokenized_length
```

Il guard durevole invoca questa funzione dopo `apply_chat_template`; anche
`offline_token_counter` la invoca sul risultato effettivo del tokenizer.
Il confronto AST con il parent mostra:

- in `common.py`, le funzioni preesistenti sono immutate; è aggiunto soltanto il
  contatore condiviso;
- in `prepare_gate.py`, le funzioni superstiti sono immutate; è rimossa la precedente
  definizione locale e importata quella condivisa;
- in `ledger.py`, l'unico metodo cambiato è
  `TokenizerAccountingGuard.validate_producer_response`.

Il contatore accetta liste e tuple piatte di interi non negativi, mapping con
`input_ids`, `BatchEncoding` e un singolo batch annidato. Le sequenze vuote valgono
zero. Rifiuta `input_ids` assenti o non sequenziali, batch multipli, forme miste o
annidate oltre un livello, booleani, negativi, float, stringhe e altri non interi.
Il guard converte le anomalie del tokenizer o della forma in `HarnessError` con
prefisso `FATAL_ACCOUNTING_ERROR`.

Oltre alle regressioni versionate, eseguiti controlli diretti in memoria:
9 forme valide accettate, 18 forme non valide rifiutate dal contatore; le stesse
18 forme sono rifiutate dal guard con il prefisso atteso. Questi controlli non
sono contati come ulteriori metodi unittest della suite da 112.

## Rosso sul parent e verde sul candidato

Test finale eseguito senza alterarne i byte:

```text
studio2.fase03.harness.test_tokenizer_accounting.TokenizerAccounting.test_A00_batch_encoding_counts_input_ids_not_mapping_keys
SHA-256 file: 90ac1bd393a52c6d6d50a7223cb7bee0961488f3b0ad65693ed065080371c52f
```

I due lanci sono processi Python separati, con Python **3.13.9 arm64** da
`/Users/luker/.venvs/fot-tep-condition-c-r10/bin/python`.
Sul parent, un import loader in memoria usa i byte ottenuti con
`git show b83048af49f63657cc91c6ceb519299e6d61567c:<percorso>` per `common.py`,
`ledger.py` e `prepare_gate.py`. Gli altri moduli di produzione sono identici nei
due commit; il modulo di test resta quello finale del candidato. Non è stata
riscritta o cambiata di checkout alcuna worktree. Sul candidato gli import sono
ordinari dalla sorgente `dd86`.

| Bersaglio | Risultato effettivo | Exit del processo di test |
| --- | --- | ---: |
| Parent `b83048a` | 1 metodo eseguito; 1 errore nel subtest positivo e 1 failure nel subtest negativo | 1 |
| Candidato `d48477f` | Lo stesso metodo e i due subtest passano; zero errori/failure/skip | 0 |

Il rosso è discriminante, non un errore di import o prerequisito:

```text
correct input_ids count is accepted:
HarnessError: FATAL_ACCOUNTING_ERROR: Mismatch contabilità token: locale=2, server=3

mapping key count is rejected:
AssertionError: HarnessError not raised
```

Il conteggio 3 proviene dai tre ID della fixture `BatchEncodingLike`; il parent
conta invece le due chiavi del mapping e accetta erroneamente 2. Entrambi i subtest
hanno raggiunto il validatore effettivo dopo il completamento del setup.
Il verde isolato è poi rieseguito come parte dei 112 test; non viene sommato a
questi come un 113esimo test distinto.

## Tokenizer 122B pin-nato e otto prompt reali

Ambiente del controllo reale: Python **3.13.15 x86_64**, Transformers **5.16.1**,
tokenizers **0.23.2**, Jinja2 **3.1.6**, stesso ambiente della riproduzione di R1.
Interprete `/private/tmp/fot-tep-schema-r4-venv/bin/python`; Jinja2 è la dipendenza
locale già disponibile tramite
`/Users/luker/Library/Python/3.11/lib/python/site-packages`, senza installazioni.
Il diverso interprete della suite è dichiarato: il test con `BatchEncoding` reale
non è sostituito dal solo mapping sintetico usato nella suite arm64.

Usati soltanto i prompt di sviluppo dell'inventario autenticato, ricostruiti con
`_conformance_inputs` e `build_producer_prompt`, e lo snapshot
`a099dee70ccfcd8d5dda56aaa0b60cb8ecadabc9`, verificato con `verify_tokenizer`.
`local_files_only=True`, `trust_remote_code=False`; nessun download o provider.
Confermata la restituzione di un vero `BatchEncoding` per ogni prompt. Contatore
offline e guard ricevono lo stesso template con generation prompt.

| Prompt | Token corretti | Guard con conteggio corretto | Guard con valore 2 |
| --- | ---: | --- | --- |
| agent_1 | 1395 | PASS | RIFIUTATO |
| agent_2 | 1016 | PASS | RIFIUTATO |
| agent_3 | 1385 | PASS | RIFIUTATO |
| agent_4 | 1329 | PASS | RIFIUTATO |
| agent_5 | 1394 | PASS | RIFIUTATO |
| agent_6 | 1066 | PASS | RIFIUTATO |
| agent_7 | 1199 | PASS | RIFIUTATO |
| agent_8 | 1385 | PASS | RIFIUTATO |

I dizionari `usage` passati al validatore sono sonde locali in memoria, non risposte
provider, receipt o prove di accounting server. Non sono stati persistiti.

## Regressioni strettamente dipendenti

Eseguiti esattamente i sette moduli dichiarati nel manifest, con
`unittest.defaultTestLoader.loadTestsFromName` e `TextTestRunner`. Letti sia l'esito
del runner sia `testsRun`, `failures`, `errors`, `skipped` e `wasSuccessful()`.

| Modulo relativo a `studio2.fase03` | Metodi eseguiti | Esito |
| --- | ---: | --- |
| `harness.test_tokenizer_accounting` | 10 | PASS |
| `tests.test_protocol` | 13 | PASS |
| `tests.test_execution_guard` | 4 | PASS |
| `harness.test_d9` | 17 | PASS |
| `harness.test_revisions` | 37 | PASS |
| `harness.test_d9_corrections` | 11 | PASS |
| `harness.test_harness_offline` | 20 | PASS |
| **Totale** | **112** | **PASS** |

Raccolti 112 ID distinti, nessuna duplicazione. Risultato osservato:

```text
Ran 112 tests in 67.999s
OK
tests=112, failures=0, errors=0, skipped=0, success=true
exit del processo unittest=0
```

Non è usato il solo exit del launcher esterno come prova. Nessuna suite ulteriore
o campagna scientifica eseguita.

Le regressioni accounting A01/A02 confermano il rifiuto di guard/messaggi mancanti
prima di intent e trasporto. A03/A04 verificano la riconferma delle evidenze al
riuso; A05 e le varianti di usage mantengono raw e STOP durevole senza record
valutato; A06 e il controllo positivo coprono resume/restart senza nuovi invii.
Le regressioni D9 e revisions coprono anche rifiuti prima del client, concorrenza,
crash reali dei processi di fixture e recupero.

La posizione del confronto con `usage` è descritta precisamente: su una nuova
risposta avviene **dopo** la cattura durevole del raw, ma **prima** di parsing,
record valutato e output scientifico. La disponibilità del guard e il binding dei
messaggi sono controllati prima della reservation/trasporto; al riuso l'accounting
viene riconfermato prima di restituire il record. Non si pretende che il confronto
con un usage ancora inesistente possa precedere la risposta. L'ordine in
`runtime.py` e i metodi durevoli di STOP/riuso in `ledger.py` sono invariati rispetto
al parent, e i test appena eseguiti ne confermano il comportamento.

## Riutilizzo motivato dei PASS precedenti

Non sono ripetute qualifiche, verifiche scientifiche o campagne già PASS. Il delta
non cambia servizi, producer, quote, piano consumer, approvazioni, mapping o
configurazione. Confrontati con i blob del parent anche `runtime.py`, `d9.py`,
`guards.py`, `producer_probe.py`, `run_pilot.py`, `protocol.py` e `inputs.py`:
tutti byte-identici. Gli helper preesistenti di hash/JSON sono identici per AST.

Documenti storici, cinque JSON privati, qualifiche, sei file tokenizer/template,
mapping e approvazione mantengono gli hash già verificati. Si conserva quindi
l'evidenza dei PASS precedenti su identità, segreti, 4608 come limite locale e
max-output server `NOT_EXPOSED`, budget 3/6/9 non congelato, S=4 conteggiato una
volta, cumulativo base 143–149, massimo 164, hard stop 200 e margine 36.
Il cambiamento del contatore è coperto dalle regressioni, dalle verifiche di forma
e dagli otto prompt 122B; sui risultati tokenizzati validi il nuovo helper conta
gli stessi ID del precedente contatore offline. Non modifica i token o il template.

## Immutabilità e isolamento

| Artefatto | SHA-256 confermato prima/dopo o rispetto al pin storico |
| --- | --- |
| Manifest storico integrazione | `699664d0f28ddb5a74563baa0289d4fc48d1eaab6461db7ae228bb117509ce30` |
| Rapporto storico integrazione | `09a6e07c75cd0d2b65531ff5aec047f6cff62f70d1a0a7c119bb854ac0e0c57d` |
| Configurazione privata, byte | `fcf4ec0bb3c77193f3aaaaa5204faf34b7c589ed8c558b4fac54601e1ce58710` |
| Configurazione canonica senza authorization | `1305c158a98c40cb57e45b43e8d872d3d66e4d6d050d1d167c91b23e0a2fccc8` |
| Service 122B privato | `94c6637f65e43d028483e1b12c7d3f14cd91058c8072f200fe3f6638225cd642` |
| Service 27B privato | `133807dfa57ddbd7a4319bfbdd2b851f0648928c12195422ee300b0e17d4f485` |
| Producer 122B privato | `b24275860a40062cca9cdce8639ff8e15936e6c17a37cde244c92ea7bea772aa` |
| Producer 27B privato | `fcecc53417d8c35319c11bf7a633b70456d3c85b90f51d7193490cae99baa4e4` |
| Ledger reale, byte prima/dopo | `02ce8df46d04300b9eb19b0fbc3345c5edd41e7ea17bd1391f22c53f7a6d9d61` |
| Ledger reale, stato logico prima/dopo | `e4f0f6bdf212696f31d11010b148fac34fac2228195e58b57f228c433bece44c` |

Directory privata 0700, esattamente cinque JSON 0600; authorization ancora assente.
Ledger reale aperto esclusivamente mediante `mode=ro&immutable=1` e
`PRAGMA query_only=ON`, dopo aver verificato WAL vuoto. `integrity_check`: `ok`.
Identità: `studio2-fase03-d9-pilot-001`. Stato invariato:

| Tabella/stato reale | Prima | Dopo |
| --- | ---: | ---: |
| external_history | 4 | 4 |
| requests / intent nativi | 0 | 0 |
| stages | 0 | 0 |
| receipts | 0 | 0 |
| responses | 0 | 0 |
| events, sola riconciliazione storica | 1 | 1 |
| hard-stop | 0 | 0 |

Anche WAL e SHM invariati: SHA-256 rispettivamente
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` e
`fd4c9fda9cd3f9ae7c962b0ddf37232294d55580e1aa165aa06129b8549389eb`.
Il digest logico usa lo stesso algoritmo del primo verbale: tabelle ordinate,
righe per `rowid`, JSON ordinato con separatori compatti e `ensure_ascii=False`.

Le regressioni richieste usano ledger, intent, stage, receipt e approvazioni
**sacrificabili di fixture**, confinati in una directory temporanea distinta,
rimossa al termine. Questi non sono artefatti del pilot reale e non autorizzano
alcuna esecuzione. Un audit hook limita scritture e connessioni SQLite a tale
directory, blocca rete e comandi esterni e consente soltanto i subprocessi Python
dei test. Il hook viene propagato anche ai subprocessi, inclusi quelli di crash.
Nessuna violazione del confine osservata durante rosso/verde e suite.

Il controllo con tokenizer reale usa invece un blocco completo delle scritture e
delle connessioni SQLite. L'unico tentativo negato è il noto `os.mkdir` della prova
di capacità temporanea di `filelock` all'importazione, gestito dalla libreria:
nessuna directory è creata. Bytecode disabilitato, modalità Hugging Face offline.

**Zero rete, tunnel, chiamate provider o token generati; zero nuovi intent, stage
o receipt nel ledger reale.** Nessuna lettura di dati final-test 03.11, OOD o scorte.
Nessuna modifica a configurazione server 27B o processo vLLM. Nessun segreto o URL
completo riportato. Il test che verifica il rifiuto di un final-test opera su una
fixture sintetica, non su dati final-test reali.

## Consegna

Il solo nuovo artefatto permanente è questo verbale nella worktree indipendente;
il NON OK originario resta immutato. Non sono stati effettuati commit, push, merge
o tag. Nessun candidato corretto dal revisore e nessuna approvazione reale aggiunta.

Lo SHA-256 integrale del verbale è comunicato nella risposta finale dopo la
scrittura, evitando un hash autoreferenziale nel documento. Ricalcolo:

```bash
shasum -a 256 /Users/luker/.codex/worktrees/b567/fot-tep/studio2/fase03/harness/VERIFICA_CORREZIONE_ACCOUNTING_BATCHENCODING_122B_03_13.md
```

**OK limitato alla readiness del candidato esatto e ai controlli offline sopra
documentati. R1 chiuso; esecuzione ancora subordinata alla distinta decisione
esplicita dell'autore sullo SHA canonico.**
