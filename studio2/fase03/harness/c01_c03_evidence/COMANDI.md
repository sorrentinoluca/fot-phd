# Comandi — implementazione C01–C03

Runtime `/opt/anaconda3/bin/python3` (3.13.9, SQLite 3.51.0). Cwd per suite, import e
subprocess: `/Users/luker/fot-tep-harness-0310-c01-c03`. Ogni invocazione Python di test
usa `PYTHONDONTWRITEBYTECODE=1`. Socket bloccati dai builder fixture. Nessuna API/inferenza.

## Base e acquisizione

`git ls-remote https://github.com/sorrentinoluca/fot-phd.git refs/heads/main` osserva
`a00605862f627710347bd63c49f79a6d0a00135f`. Nuovo worktree dal successore documentale
`6268437b8b64288b50ad5f7c924e1fcab85b27d3`. Acquisizione separata con `acquire.py`, inventory
completo e verifica 3025 membri + manifest. Fonti precedenti sempre lette, mai eseguite in-place.

## Riproduzioni

Le directory `before/`, `after/` e `x23_adapted/` hanno ciascuna `evidence/` con copie degli
script e un symlink `candidate` al candidato pertinente. Lanciare solo in una nuova copia
sacrificabile; gli script creano directory e log. I symlink e gli output esterni sono
inventariati. Non eseguire le copie acquisite né le prove già eseguite.

```text
python before/evidence/extended_probes.py       # cwd candidato 0c8157f esatto: 18, 4 failure
python before/evidence/additional_edges.py     # 6/6
python after/evidence/extended_probes.py        # nuovo codice: 18/18
python after/evidence/additional_edges.py      # 5/6, X23 conserva l'attesa del difetto
python x23_adapted/evidence/additional_edges.py # solo X23, 1/1; adattamento esplicito
```

Comando prove originarie applicabili:

```text
python studio2/fase03/harness/correzioni_evidence/RUN_APPLICABLE_ORIGINAL.py --candidate /Users/luker/fot-tep-harness-0310-c01-c03 --original /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/negative_probes.py --reference /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference --sandbox /Users/luker/fot-tep-harness-0310-c01-c03-checks/applicable
```

## Suite

```text
python -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol studio2.fase03.harness.test_revisions studio2.fase03.harness.test_c01_c03
python -m unittest discover -v studio2/fase03
python docs/test_explanation.py
```

Log targeted/discovery separati. I test mirati comprendono 82 preesistenti + 14 C01–C03.
Discovery comprende i 117 preesistenti + 14 C01–C03. Un primo discovery è stato interrotto
per import relativi del nuovo modulo: caricava `harness.ledger` accanto a
`studio2.fase03.harness.ledger`, duplicando l'identità HarnessError. Allineati gli import
assoluti al resto della suite; log parziale `discovery_initial.log` conservato. Nessun
assert è stato indebolito. Il discovery finale include la versione corretta.

`first_regressions.log` (37/37) e `new_regressions_initial.log` (13/13, prima di aggiungere
il nuovo test di morte/ripresa tra processi) sono controlli intermedi, non la consegna finale.

Guardiano documentale prima e dopo: 35 metodi, 14 failure storiche con gli stessi ID,
1 skip; `documentation_comparison.json`. Non PASS. Compilazione senza emissione bytecode
tramite `compile` dei soli sorgenti live di fase03, escluse prove forensi/acquisite.

Controllo diff: `git diff --check`; file metriche e perimetri protetti confrontati byte
per byte con il successore documentale base. Il controllo whitespace sui commit esclude
soltanto acquisizioni/prove byte-identiche, che conservano gli spazi dei log unittest.
