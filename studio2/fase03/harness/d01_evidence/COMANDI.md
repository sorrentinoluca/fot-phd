# Riproduzione del delta D01 / C01 / R04

Runtime `/opt/anaconda3/bin/python3` (3.13.9, SQLite 3.51.0); tutti i test usano
`PYTHONDONTWRITEBYTECODE=1`. Cwd corrente `/Users/luker/fot-tep-harness-0310-d01`.
Approvazioni, tokenizer e trasporti sono fixture/stub offline. Nessuna API/inferenza.

## Identità e acquisizione

Controllati HEAD/tree/branch/status, worktree e remoto effettivo prima di scrivere:
`git ls-remote https://github.com/sorrentinoluca/fot-phd.git refs/heads/main` →
`a00605862f627710347bd63c49f79a6d0a00135f`. Worktree nuovo dalla consegna documentale
`52e13e1ed540e1ad076474398bf850445c9a4a00`. Acquisizione separata con acquire.py:
1.788 membri del manifest + manifest verificati, 171 copie byte-identiche, 1.618 esterni.

## Y01–Y07: script originale byte-identico

La directory `before/` contiene `evidence/edge_probes.py` e un symlink `candidate` al
respinto 9e18bcb. `after/` ha la stessa struttura col codice corrente. Lo script usa
inoltre il vecchio 0c8157f SOLO per generare nuovi ledger v2 di fixture, in subprocess.
I suoi percorsi di input non sono modificati. Non lanciare le copie già eseguite o quelle
acquisite: creano nuove directory e log. Usare una nuova radice sacrificabile sibling.

```text
python before/evidence/edge_probes.py   # cwd candidato respinto: 7, 2 failure Y01/Y02
python after/evidence/edge_probes.py    # cwd candidato corretto: 7/7
```

Il wrapper stampa counts e non restituisce exit diverso da zero per le failure: verificare
sempre tests/failures/errors nel JSON, non il solo exit code.

## Suite

```text
python -m unittest -v studio2.fase03.harness.test_d01_replay
python -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol studio2.fase03.harness.test_revisions studio2.fase03.harness.test_c01_c03 studio2.fase03.harness.test_d01_replay
python -m unittest discover -v studio2/fase03
python docs/test_explanation.py
```

Log separati d01.log, targeted.log, discovery.log. I sette D01 sono inclusi nei totali
103 mirati e 138 discovery; non si sommano. FOT_HARNESS_LEGACY_CANDIDATE può indicare
un altro checkout pulito di 0c8157f; HEAD e tree sono verificati nel setup. Il default è
`/Users/luker/fot-tep-riverifica-harness-0c8157f-01a0a1ec/candidate`.

```text
python studio2/fase03/harness/correzioni_evidence/RUN_APPLICABLE_ORIGINAL.py --candidate /Users/luker/fot-tep-harness-0310-d01 --original /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/negative_probes.py --reference /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference --sandbox /Users/luker/fot-tep-harness-0310-d01-checks/applicable
python literal/evidence/extended_probes.py
python literal/evidence/additional_edges.py
python x23_adapted/evidence/additional_edges.py
```

Le copie X sono quelle acquisite dal terzo verbale. Nei contenitori literal e x23_adapted,
`candidate` punta al nuovo codice. X01–18: 18/18; X19–24 letterali: 5/6 (failure obsoleta
X23 conservata). Solo X23 nella versione adattata già verificata dal revisore: 1/1.
Nessun nuovo adattamento introdotto qui. I 14 applicabili comprendono 12 letterali e 2 con
la fixture/argomento già adattati nella consegna precedente; nessuna pretesa 50/50 letterali.

Guardiano prima/dopo: 35 test, stessi 14 ID falliti, 1 skip; NON PASS. scope.json confronta
perimetri protetti e codice C02/C03 con la base esatta. compile.json registra compilazione
senza bytecode dei soli Python live; esclusi alberi forensi e prove acquisite. Non sono
rigenerati artefatti scientifici. git diff --check si applica al delta redatto; le copie
forensi mantengono whitespace e newline originali per obbligo di acquisizione byte-identica.

Il primo controllo di perimetro aveva applicato alla base documentale la lista dei soli
file di correzione, includendo quindi anche l'acquisizione già autorizzata: si era fermato
prima dei confronti protetti. Corretto il punto di confronto al commit di acquisizione;
`scope_initial_issue.json` conserva la distinzione. Nessun difetto del candidato e nessun
file scientifico modificato. I controlli finali sono prodotti da scope_audit.py.
