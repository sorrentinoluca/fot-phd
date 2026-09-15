# D02 — comandi e riproducibilità, esclusivamente offline

Cwd tecnico: `/Users/luker/fot-tep-harness-0310-d02`.
Output di questa esecuzione: `/Users/luker/fot-tep-harness-0310-d02-checks`.
Python: `/opt/anaconda3/bin/python3`, con `PYTHONDONTWRITEBYTECODE=1`.
Non rieseguire script sulle directory di prove già popolate: usare una nuova radice.
Le fixture non sono input scientifici. I provider, tokenizer e server nelle prove sono stub.

## Acquisizione

`non_ok_edb37f3_20260915/acquire.py` registra gli stati Git prima della creazione del
worktree, verifica il candidato edb37f3, il suo successore documentale e i 62 membri del
manifest precedente; verifica 1.821 membri del manifest del revisore più SHA256SUMS.
100 file sono copiati byte-identici, 1.722 restano esterni con coordinate/hash/dimensioni;
cinque symlink sono inventariati senza seguire ricorsivamente i target.
Le fixture Z sono copiate; N/X/Y ripetute rimangono alla loro posizione recuperabile.
L’acquisizione è il commit separato `5b45cdcabe40aa64b0aecd1b5fe9d09c92ce5bb4`.

## Prove finali

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol studio2.fase03.harness.test_revisions studio2.fase03.harness.test_c01_c03 studio2.fase03.harness.test_d01_replay studio2.fase03.harness.test_d02_predecessors
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 docs/test_explanation.py
```

Log integrali: targeted.log, discovery.log, documentation_before.log e documentation_after.log.
Le nuove otto regressioni sono incluse nelle due suite finali. `d02.log` è una prova
preliminare 29/29: otto nuove più 21 fixture TestCase importate. L’import è stato
corretto prima delle suite finali; non contare quella esecuzione come 29 nuovi metodi.

Le prove Z si eseguono con copie byte-identiche di `chain_probes.py` in
`NUOVA_RADICE/evidence`, con symlink `NUOVA_RADICE/candidate` al checkout da valutare:

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 NUOVA_RADICE/evidence/chain_probes.py
```

`before/` punta al source documentale 7afbf41, il cui codice è il respinto edb37f3;
`after/` punta al nuovo worktree. Cwd e subprocess seguono il candidato corrispondente.
I confronti danno cinque metodi, tre failure prima e nessuna dopo, zero errori.
Lo script non restituisce necessariamente exit nonzero per assertion fallite: leggere
sempre tests/failures/errors nel JSON e il log unittest.

Per Y, X letterali e X23 già adattato si riproduce la stessa struttura con gli script
acquisiti. `extension_commands.json` conserva i comandi effettivi e i primi exit code;
`run_extensions.py` conserva il launcher usato. La prima esecuzione X23 adattata ha avuto
un errore di setup, ModuleNotFoundError sul modulo sibling `extended_probes.py`: il log
è conservato in `x23_adapted/setup_missing_dependency.log`. È stata poi copiata la
dipendenza byte-identica da `non_ok_edb37f3_20260915/files/x23_adapted/evidence/extended_probes.py`
e rieseguito soltanto `additional_edges.py` invariato nella stessa directory ancora
priva di fixture. Il risultato corretto è nel console log e nel JSON additional.json.
Per una nuova riproduzione copiare **entrambi** i moduli prima di eseguire X23 adattato.
Nessuna nuova modifica di assertion o adattamento. X23 letterale conserva una failure
obsoleta; il consolidamento è 23 X letterali più il solo X23 precedentemente adattato.

Originali applicabili:

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 studio2/fase03/harness/correzioni_evidence/RUN_APPLICABLE_ORIGINAL.py --candidate /Users/luker/fot-tep-harness-0310-d02 --original /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/negative_probes.py --reference /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference --sandbox NUOVA_DIRECTORY_APPLICABILI
```

14/14: 12 metodi letterali e due soli adattamenti fixture/argomento preesistenti (20/21).
La matrice nominativa acquisita documenta tutti i 50 metodi e gli accorpamenti, compreso
N48 equivalente al requisito C02. I totali non sono sommabili né 50/50 letterali.

## Controlli e limiti

`scope_audit.py` confronta 175 file protetti con la base documentale e compila in memoria
92 sorgenti live, escludendo acquisizioni/fixture/evidence. `scope.json`, `compile.json`
e `runtime.json` conservano esiti e metadati selezionati del task preparatore.
`documentation_comparison.json` confronta esattamente i 14 identificativi falliti fra
prima, dopo e la review acquisita: 35 test, 1 skip, zero errori, **NON PASS**.
`setup_notes.json` distingue gli inconvenienti di setup dai difetti del candidato.
Il whitespace presente nei file acquisiti e nei log è preservato byte-identico;
`git diff --check` viene applicato separatamente a codice e documenti nuovi.

`REPRODUCTION_INVENTORY.json` descrive ogni originale, copia e fixture esterna con hash,
dimensione e percorso recuperabile. `SHA256SUMS` copre le prove incluse in Git, escluso
sé stesso. `RESULTS.json` distingue risultati locali e review ancora richiesta.
Nessun push, merge, tag, freeze, GO, API provider, inferenza o simulazione scientifica.
