# Indice degli audit

| Nome file | Descrizione |
| --- | --- |
| `EXP3V2_DOCUMENTATION_INVENTORY_2026-09-03.md` | Inventario read-only (2026-09-03) di tutti i file `.md`, `.pdf` e `.html` del repository, con posizione attuale e suggerimento di mantenimento, spostamento o cancellazione. |
| `EXP3V2_FINAL_FREEZE_AUDIT.md` | Audit indipendente di final-freeze e prontezza al primo run reale di EXP3_V2 (harness revisione 004): 12 controlli, tutti superati, nessun rilievo bloccante. |
| `EXP3V2_FIRST_RUN_PREFLIGHT.md` | Piano operativo di preflight per il primo run scientifico EXP3V2-N-001 attempt 0: stato di freeze confermato, comando MATLAB esatto e parametri, senza alcuna esecuzione. |
| `EXP3_ATTEMPT_EXHAUSTION_AUDIT.md` | Audit read-only dopo il fallimento di entrambi i tentativi ammessi per il caso EXP3-N-001: verdetto di blocco per esaurimento tentativi e analisi delle cause tecniche. |
| `EXP3_FIRST_RUN_READINESS_AUDIT.md` | Audit di prontezza al primo run fisico dell'Esperimento 3 (2026-09-02): verifica di HEAD, tag `exp3-heldout-frozen`, manifest di freeze, piano dei 30 casi e suite di test pre-freeze. Nessun blocco. |
| `EXP3_HOTFIX_001_MICROAUDIT.md` | Micro-audit read-only dell'hotfix post-freeze 001: accesso a campo su struct vuota non tipizzata in `assert_attempt_allowed`. Hotfix accettato. |
| `EXP3_HOTFIX_002_MICROAUDIT.md` | Micro-audit read-only dell'hotfix post-freeze 002: disallineamento semantico fra `version('-date')` e `ver('MATLAB').Date` nel campo congelato di data MATLAB. Hotfix accettato. |
| `EXP3_HOTFIX_003_MICROAUDIT.md` | Micro-audit read-only dell'hotfix post-freeze 003: gestione dei callback di plotting (`StopFcn`) in esecuzione headless. Hotfix accettato, nessun bloccante. |
| `EXP3_PREFREEZE_AUDIT_REPORT.md` | Audit pre-freeze del protocollo Esperimento 3 e dell'infrastruttura di generazione e verifica, precedente alla generazione dei 30 run fisici. Verdetto: pronto per il freeze. |
