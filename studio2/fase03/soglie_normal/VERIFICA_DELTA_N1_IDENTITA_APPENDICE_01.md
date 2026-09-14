OK

# Appendice 01 — riverifica mirata del rilievo sulle sei impronte

## Oggetto e identità

Questa appendice riverifica esclusivamente il rilievo bloccante registrato in
`VERIFICA_DELTA_N1_IDENTITA.md`: oltre al report era cambiato anche
`studio2/PROVENIENZA.md`, mentre cinque dei sei file dello snapshot approvato dovevano
restare byte-identici. Non rivaluta né sostituisce il verbale NON OK; documenta la correzione
successiva e il nuovo esito del solo rilievo.

Worktree: `/Users/luker/fot-tep-correzione-soglie-normal`. Branch:
`codex/studio2-soglie-normal-correzioni`. HEAD/base:
`819b12e97fb94d501032655ec2f226139e6c5ca5`.

Verificatore: **`gpt-5.6-sol`**, reasoning **`high`**. Identificatori disponibili:
sessione Codex `01a0a03d-6daf-7540-947c-6f94ab12b2f5`, task/thread
`01a0a055-44a5-72d0-9b35-5549605786a1`. Data: 2026-09-14, Europe/Rome.

## Impronte correnti

| File dello snapshot approvato | SHA-256 corrente | Esito rispetto all’impronta approvata |
|---|---|:---:|
| `studio2/PROVENIENZA.md` | `d0b59649ad307d3bb15c9b07015c106da8addba69be111fd8258503582f37585` | ✅ byte-identico |
| `REPORT_SOGLIE_NORMAL.md` | `bac095b009ed50fd758ac5b613c582f82a5dc3253c67a6226b667688653b16c4` | ✅ unico nuovo hash atteso |
| `THRESHOLD_UNCERTAINTY_PROTOCOL.json` | `711d9711587fd140dcb451ccbe48b42d35fdf1bc3043feb5fb5e6dea3921989b` | ✅ byte-identico |
| `complete_threshold_uncertainty.py` | `5fcbb2ede6f1fcea43e9c7fa6d6c9dc66a530ee9bafb8b2cc91658540ddffe57` | ✅ byte-identico |
| `THRESHOLD_UNCERTAINTY.json` | `70dbca42391a0eea6ca39e12dc2f4e81d1cbe9a527494aca09388ae74f153feb` | ✅ byte-identico |
| `tests/test_threshold_uncertainty.py` | `1fa8195d57dc090483db9d3c9c4391e4ec42365e579667d709d56f022be02f5a` | ✅ byte-identico |

`studio2/PROVENIENZA.md` coincide anche tramite confronto `cmp` con la copia dello snapshot
approvato in
`/Users/luker/fot-tep/.worktrees/riverifica-soglie-normal/studio2/PROVENIENZA.md`.
Il requisito è ora soddisfatto: cinque impronte approvate sono immutate e il solo report ha
il nuovo hash richiesto dal delta N1/stato/evidenza/decisione.

## Assenza di altro delta pertinente

Gli altri oggetti pertinenti conservano le impronte registrate dal verbale precedente:

| File | SHA-256 corrente |
|---|---|
| `VERIFICA_DELTA_N1_IDENTITA.md` | `0c48cc8d0300decb172cf24a6c93d3af0024bc4861e084302eb0baf02c28e7fd` |
| `DECISIONE_AUTORE_FAR.md` | `84520c63e75d49a4855ce02421df59c5a641612cafa9d82fdfc2e127ebcce58e` |
| `evidence/EXECUTOR_IDENTITY.json` | `dd7066c08e28c142e809393bad3a35373159ffd2b41078b79dc7d3ae10799166` |
| `evidence/REPORT_SOGLIE_NORMAL_SNAPSHOT_OK.md` | `5323438f8f2426f859537e12dee24139c3b8daa0b858b01934b4f7fc23308e32` |
| `evidence/VERIFICA_CORREZIONI_SOGLIE_NORMAL_OK.md` | `d98a2856647493b0e96fc1198ac32c457510fc10399538511373655e1b6f1c9e` |
| `evidence/VERIFICA_SOGLIE_NORMAL_NON_OK_819b12e.md` | `ccaec80994522ba5167fdf9ef6f3500d220c19f86977de53afdb2dee7be548bd` |
| `evidence/mc_vs_exact_container.json` | `44c64fe1746434bc7f9691c048aa8087adb48dd18a4ff68f64420df84d303ca4` |

La lista degli otto file del delta N1/stato/evidenza/decisione usata nel verbale precedente,
ora con `PROVENIENZA.md` ripristinato, ordinata per percorso e serializzata come righe
`sha256sum`, ha SHA-256
`e98568f4064df245779a9609932fc8a131e21057e1d61d91dd0b22277914f4a6`.

Non risultano nuovi file oggetto o ulteriori modifiche pertinenti rispetto allo stato già
verificato, oltre al ripristino di `PROVENIENZA.md` e alla presente appendice autorizzata.
Non sono stati rieseguiti bootstrap, audit dei workbook, simulazioni, test o guardiano
documentale: i controlli positivi del verbale precedente restano riferiti a oggetti con le
medesime impronte.

## Verdetto

**OK** sul rilievo delle impronte e, per conseguenza, sul delta mirato N1/identità/decisione:
la correzione ripristina `studio2/PROVENIENZA.md` byte-identico allo snapshot approvato senza
alterare gli altri oggetti già controllati. Restano validi i limiti e le dipendenze temporanee
segnalati nel verbale originario.

Questo OK è strettamente limitato al delta N1, all’identità e alla separazione della decisione
autoriale dalle prove tecniche. Non modifica il verdetto storico sullo stato precedente, non
rivaluta l’intera sotto-fase 03.5 e **non chiude la Fase 03**.
