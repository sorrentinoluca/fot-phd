# Riproduzione D9 offline

Working directory: `/Users/luker/fot-tep-harness-d9`.
Python finale: `/opt/anaconda3/bin/python3`, dettagli in `runtime.json`.
`TESTED_BYTES.json` conserva i comandi delle suite e un inventario SHA-256 dei
file Python presenti al loro avvio. L'inventario include anche copie forensi:
non implica che ogni file inventariato sia stato importato o eseguito.
Il conteggio delle sorgenti live compilate separatamente è in `compile.json`.

## Suite sul delta

Comandi effettivi, con `PYTHONDONTWRITEBYTECODE=1` nell'ambiente:

```bash
/opt/anaconda3/bin/python3 -m unittest -v \
 studio2.fase03.harness.test_c01_c03 \
 studio2.fase03.harness.test_d01_replay \
 studio2.fase03.harness.test_d02_predecessors \
 studio2.fase03.harness.test_d03_contract \
 studio2.fase03.harness.test_d04_open_quota \
 studio2.fase03.harness.test_d9 \
 studio2.fase03.harness.test_harness_offline \
 studio2.fase03.harness.test_metric_raccordo \
 studio2.fase03.harness.test_revisions \
 studio2.fase03.tests.test_execution_guard \
 studio2.fase03.tests.test_protocol
/opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
/opt/anaconda3/bin/python3 -m unittest -v studio2.fase03.harness.test_d9
```

Output rispettivamente `targeted.log`, `discovery.log`, `d9_final.log`.
Le suite sono sovrapposte, non si sommano. Gli stadi nei test usano fixture
sacrificabili e trasporti fittizi; non sono un pilot scientifico.
Il supporto `test_revisions.py` vieta socket e sostituisce i confini esterni.
Le fixture legacy richiedono i percorsi locali descritti nei test originali:
non si nasconde questa dipendenza di ambiente.

## Stessi test D9 finali sull'antecedente esatto

```bash
FOT_D9_TARGET=/Users/luker/fot-tep-riverifica-harness-aae29a9-01a0a1ec/candidate \
 PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 \
 studio2/fase03/harness/test_d9.py -v
```

Target `aae29a908356e4a4842a214fdc3db9bff26ec3ca`, tree
`4e1f7f043725d64fb16b7d1c921c619bce8d1bb3`; nessuna modifica al checkout target.
Output `final_test_on_aae29a9.log`: 17 metodi, 3 fallimenti comportamentali e
14 errori per API D9 assenti. Non sono 17 regressioni D04.
Il file di test è esterno al target e seleziona il modulo tramite `FOT_D9_TARGET`.
Il rosso iniziale di quattro metodi è distinto: `test_first_red.log`.

## Manutenzione e conservazione

```bash
python3 docs/test_explanation.py
```

Eseguito prima e dopo; log `guardian_before.log` / `guardian_after.log`.
`guardian_comparison.json` confronta tutti i FAIL, inclusi subtest, con D04.
NON PASS storico resta NON PASS. Nessun nuovo walkthrough/HTML viene pubblicato.

`preservation_checks.json`: confronto byte con blob della base per i file harness
non modificati, fonti D9 con commit/dimensione/hash, verbali D04 con impronte note.
`compile.json`: compilazione in memoria, senza esecuzione o scrittura pyc.
I log intermedi falliti o interrotti sono conservati e non entrano nei risultati finali.
Nessun launcher storico V/W/Y/Z/X aggiuntivo è stato rilanciato per dichiarare
nuove chiusure; le suite coinvolte nel delta e la discovery sono le prove attuali.

Le tre CLI sono state anche invocate senza --execute con il config pending D9;
comandi ed exit code in `cli_plans.json`, output nei tre `*_plan.log`.
Run_pilot e producer_probe restituiscono 0 in modalità piano, prepare_gate 3
per inventario sospeso. Il test D9 verifica separatamente che un tentativo
esecutivo con quel config non crei il ledger.
