# Handoff — batch `normal_dev`

Il batch non è stato lanciato in questa finestra. Attesi 40 run, stream 60000–60039, 2.600 h
simulate e circa 8,96 min di sola simulazione secondo la misura 03.5. Release proposta:
`studio2-fase03-normal-dev-v1`.

## Blocco corrente

**Batch NON lanciabile finché il piano rev. 7 (`a572d1c`) non è in `origin/main`.** Al
2026-09-14 `git branch -r --contains a572d1c` non elenca `origin/main`. Il preflight applica lo
stesso controllo fail-closed.

## Lancio, dopo la pubblicazione del piano

```bash
cd /percorso/al/repository-integrato
bash studio2/fase03/baseline_numerica/launch_normal_dev_batch.sh
```

Il launcher convalida byte e ordine del piano, ricontrolla collisioni note e piani presenti,
rifiuta destinazioni già esistenti e avvia un solo processo MATLAB. Scrive in
`runs/normal_dev_001/` e `runtime/normal_dev_001/`.

## Esito da restituire

Non incollare il log completo. Restituire due righe: `completati/40`, `falliti/40`, percorso del
log. Conservare piano, log, PID, manifest, workbook e hash; poi eseguire audit read-only e
pubblicare l'archivio secondo `docs/MAINTENANCE.md` §8.5.

Un trip o errore tecnico arresta il lotto. Non cancellare né rilanciare la destinazione e non
sostituire selettivamente un run. Dopo successo, estrarre le evidence con le funzioni e le guardie
di 03.6, mantenendo U3/R2; produrre un indice evaluator-side che colleghi ogni evidence a
`agent_id`, `run_id`, finestra e classe `Normal`.
