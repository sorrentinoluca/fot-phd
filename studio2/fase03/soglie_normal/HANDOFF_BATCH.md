# Handoff batch soglie Normal

Il batch non è stato lanciato in questa finestra. Smoke completato e verificato in
`SMOKE_CHECK.json`; destinazione scientifica ancora assente.

## Comando esatto

```bash
cd /Users/luker/fot-tep
bash /Users/luker/fot-tep/studio2/fase03/soglie_normal/launch_normal_batch.sh batch
```

Il launcher esegue i piani immutabili `plans/cal_thr.csv` e `plans/far_ver.csv` in un solo
processo MATLAB R2025b ARM, scrive sotto `runs/normal_001/` e rifiuta destinazioni o launch
directory già esistenti. Attesi: 350 manifest `cal_thr`, 150 manifest `far_ver`, 500 workbook,
zero trip e zero fallimenti tecnici; ore totali 27.610.

## Arresto e ripresa

Un trip Normal o errore tecnico arresta il lotto. Non cancellare né rilanciare la destinazione;
conservare log, file parziali e manifest. La ripresa richiede revisione/autorizzazione e un nuovo
namespace, salvo il solo rerun dello stesso stream per verifica di riproducibilità. Dopo successo,
eseguire audit read-only e verificare completezza/hash prima di calcolare gli score.

Prima di aprire qualsiasi finestra `far_ver`, calcolare con il codice Fase 02 lo score su tutte le
350 finestre `cal_thr`, congelare soglia, rango, numerosità, regola `S > threshold` e impronte in
`THRESHOLD_FREEZE.json`. Solo dopo si apre `far_ver`; nessuna modifica post-hoc della soglia.
