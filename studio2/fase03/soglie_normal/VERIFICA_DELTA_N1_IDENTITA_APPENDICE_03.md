OK

# Appendice 03 — verifica mirata dell’ultimo aggiornamento di stato del report

## Oggetto e identità

Verifica limitata al nuovo testo di stato in `REPORT_SOGLIE_NORMAL.md`: attribuzione del
verdetto NON OK di `VERIFICA_DELTA_N1_IDENTITA.md` e degli OK delle Appendici 01–02,
registrazione dell’apertura successiva del walkthrough, aggiornamento del fuori-perimetro e
storicizzazione della frase sul commit.

Non è stata svolta una nuova verifica scientifica della documentazione §4.4 o della sintesi.
Non sono stati rieseguiti calcoli, test, bootstrap, audit o simulazioni. Nessun file esistente
è stato modificato da questa verifica; l’unica scrittura è la presente appendice.

Worktree: `/Users/luker/fot-tep-correzione-soglie-normal`. Branch:
`codex/studio2-soglie-normal-correzioni`. HEAD/base:
`819b12e97fb94d501032655ec2f226139e6c5ca5`.

Verificatore: **`gpt-5.6-sol`**, reasoning **`high`**. Identificatori disponibili:
sessione Codex `01a0a03d-6daf-7540-947c-6f94ab12b2f5`, task/thread
`01a0a055-44a5-72d0-9b35-5549605786a1`. Data: 2026-09-14, Europe/Rome.

## Esiti

✅ Il report corrente ha SHA-256
`d6d1a533ecb4fe7c25096f05971b7ae73f47dd053a09a4f592e2265c17011756`.

✅ La nuova sezione di stato conserva il primo verdetto **NON OK** nel verbale originario e
descrive correttamente il rilievo: l’aggiornamento non necessario di `studio2/PROVENIENZA.md`.
Indica poi separatamente gli **OK** delle Appendici 01 e 02, rispettivamente sulle impronte e
sul supporto locale di riproducibilità.

✅ Identità attribuita alle Appendici 01–02: `gpt-5.6-sol`, reasoning `high`, sessione
`01a0a03d-6daf-7540-947c-6f94ab12b2f5`. Coincide con i metadati dichiarati nei verbali.
Il report non trasforma il NON OK storico in un OK retroattivo.

✅ Il report registra che l’aggiornamento coordinato del walkthrough è stato aperto soltanto
dopo gli OK. L’aggiornamento del walkthrough non compare più fra le attività fuori perimetro;
la frase sul commit è correttamente ancorata «al momento della redazione» e non dichiara un
commit già eseguito.

✅ N1 è invariata: il report conserva entrambi gli intervalli, le masse **95,38705407%** e
**96,89204510%**, il condizionamento ai 350 score osservati e la precisazione che non sono
garanzie di copertura del quantile della popolazione.

✅ Cinque dei sei file dello snapshot approvato mantengono le impronte precedenti; soltanto il
report ha il nuovo hash dovuto all’aggiornamento di stato:

| File | SHA-256 corrente | Esito |
|---|---|:---:|
| `studio2/PROVENIENZA.md` | `d0b59649ad307d3bb15c9b07015c106da8addba69be111fd8258503582f37585` | ✅ immutato |
| `REPORT_SOGLIE_NORMAL.md` | `d6d1a533ecb4fe7c25096f05971b7ae73f47dd053a09a4f592e2265c17011756` | ✅ unico cambiato |
| `THRESHOLD_UNCERTAINTY_PROTOCOL.json` | `711d9711587fd140dcb451ccbe48b42d35fdf1bc3043feb5fb5e6dea3921989b` | ✅ immutato |
| `complete_threshold_uncertainty.py` | `5fcbb2ede6f1fcea43e9c7fa6d6c9dc66a530ee9bafb8b2cc91658540ddffe57` | ✅ immutato |
| `THRESHOLD_UNCERTAINTY.json` | `70dbca42391a0eea6ca39e12dc2f4e81d1cbe9a527494aca09388ae74f153feb` | ✅ immutato |
| `tests/test_threshold_uncertainty.py` | `1fa8195d57dc090483db9d3c9c4391e4ec42365e579667d709d56f022be02f5a` | ✅ immutato |

✅ I verbali precedenti sono preservati con le stesse impronte:

- `VERIFICA_DELTA_N1_IDENTITA.md`:
  `0c48cc8d0300decb172cf24a6c93d3af0024bc4861e084302eb0baf02c28e7fd`;
- `VERIFICA_DELTA_N1_IDENTITA_APPENDICE_01.md`:
  `71e949e595e8702fce83de37efbbd632baada415e02a8ef79d985a05dddfec46`;
- `VERIFICA_DELTA_N1_IDENTITA_APPENDICE_02.md`:
  `d6778958e60700734cc0b3f40c50ad4e9e1006fee9232355b18e1ffa946ce0a4`.

✅ Il report dichiara esplicitamente in apertura «La Fase 03 non è chiusa», ribadisce che
nessuna chiusura è implicita e mantiene la chiusura della Fase 03 fra le attività fuori
perimetro. L’ultimo delta non dichiara chiusa né la sotto-fase per effetto automatico né la
Fase 03.

## Verdetto

**OK** sull’ultimo aggiornamento di stato del report. Attribuzioni, identità e sequenza dei
verdetti sono corrette; N1 e gli altri cinque file scientifici/documentali dello snapshot
restano invariati; la Fase 03 non viene dichiarata chiusa.

Questo OK riguarda soltanto il testo di stato del report e non costituisce una nuova verifica
scientifica del walkthrough, della sintesi o dell’intera Fase 03.
