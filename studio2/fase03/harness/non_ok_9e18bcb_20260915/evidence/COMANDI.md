# Comandi della verifica indipendente C01–C03

Tutti i test usano stub, nessun trasporto reale. Directory candidato:
`/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/candidate`.
Directory evidence sibling:
`/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence`.
Le impostazioni sotto sono state passate esplicitamente ai processi; il cwd candidato è necessario anche per i subprocess.

```bash
export PYTHONDONTWRITEBYTECODE=1
export FOT_HARNESS_TEST_EVIDENCE=/Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference/studio2/fase03/evidence/output
```

## Identità e isolamento, prima di scrivere

Letture su principale, sorgente e due review precedenti: `git rev-parse HEAD HEAD^{tree}`, `git status --short --branch`, `git worktree list --porcelain`, `git remote -v`. Lettura del candidato con `git show`, parent con `git rev-parse COMMIT^` e diff tecnico/documentale con `git diff --name-status`.

```bash
git ls-remote https://github.com/sorrentinoluca/fot-phd.git refs/heads/main
git clone --shared --no-checkout /Users/luker/fot-tep-harness-0310-c01-c03 /Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/candidate
git -C /Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/candidate checkout --detach 9e18bcbd06fa2c54202c8eeda079c112dbfcefcd
```

Il successore documentale è stato acquisito con `git show 52e13e1ed540e1ad076474398bf850445c9a4a00:studio2/fase03/harness/FILE`, per i quattro file elencati in documentary_paths.txt, senza checkout del successore.

## Suite, cwd candidato

```bash
/opt/anaconda3/bin/python3 -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol studio2.fase03.harness.test_revisions studio2.fase03.harness.test_c01_c03
/opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
/opt/anaconda3/bin/python3 docs/test_explanation.py
```

Output integrali rispettivamente targeted.log (96 OK), discovery.log (131 OK), documentation.log (35, 14 failure, 1 skip; NON PASS). Le suite si sovrappongono.

```bash
/opt/anaconda3/bin/python3 studio2/fase03/harness/correzioni_evidence/RUN_APPLICABLE_ORIGINAL.py --candidate /Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/candidate --original /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/negative_probes.py --reference /Users/luker/fot-tep-verifica-harness-0310-01a0a1ec/evidence/reference --sandbox /Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/applicable
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/additional_edges.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/x23_adapted/evidence/additional_edges.py
/opt/anaconda3/bin/python3 /Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/edge_probes.py
```

Output nei relativi JSON/log e nei console.log. Gli script del revisore scrivono risultati strutturati: leggere tests/failures/errors, non dedurre il successo dal solo exit code del wrapper Python. X23 letterale ha la failure prevista di attesa obsoleta; le due failure Y01/Y02 sono invece D01.

`edge_probes.py` genera fixture v2 con il vecchio codice esatto in un subprocess, cwd e PYTHONPATH impostati all'isolato 0c8157f, poi apre tali fixture con il nuovo codice. Non modifica la review precedente. Y03–Y07 coprono raw, journal, guardie, retry e denominatori; ogni trasporto è stub. I processi reali nei test del candidato eseguono os._exit soltanto nelle fixture.

## Integrità e matrici, cwd radice della review

```bash
/opt/anaconda3/bin/python3 evidence/audit.py
/opt/anaconda3/bin/python3 evidence/lineage_audit.py
/opt/anaconda3/bin/python3 evidence/build_matrices.py
/opt/anaconda3/bin/python3 evidence/package_review.py
```

audit.py è stato eseguito prima delle suite e crea i contenitori sacrificabili: non rieseguirlo sulla directory già popolata. lineage_audit.py ricontrolla fonti Git esatte, moduli, tag remoti, la prima evidence conservata, import/sintassi e ID documentali. build_matrices.py verifica per ogni riga dei 50 metodi la presenza di una prova corrente passata. package_review.py controlla Git/fonte finale e genera inventario/SHA256SUMS. Per una replica autonoma usare una nuova radice e adattare soltanto i percorsi di output negli script; conservare questa consegna immutata. Non eseguire script storici all'interno del candidato tracciato.

Comandi di mera lettura (`cat`, `sed`, `nl`, `rg`, estrazione JSON dei metadati runtime) sono serviti a localizzare le righe citate. Una ricerca ha usato il percorso inesistente preflight/PREFLIGHT_CONFIG.json; il file reale config/pilot_preflight.json è stato poi letto e verificato. Non si trattava di errore del candidato o di una prova comportamentale fallita.
