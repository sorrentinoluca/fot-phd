OK

# Appendice 02 — verifica del supporto locale di riproducibilità C4

## Oggetto e identità

Verifica strettamente limitata al delta documentale composto da:

- nuovo `requirements-c4.txt`;
- nuovo `REPRODUCIBILITY_C4.md`;
- aggiornamento di `REPORT_SOGLIE_NORMAL.md` che distingue il comando storico, dipendente
  dal venv esterno, dalla procedura locale ora conservata nel repository.

Sono stati inoltre ricontrollati soltanto gli hash degli oggetti già verificati e il testo N1
nel report. Non sono state installate dipendenze e non sono stati rieseguiti bootstrap, audit,
simulazioni o calcoli scientifici. I verbali precedenti sono stati preservati.

Worktree: `/Users/luker/fot-tep-correzione-soglie-normal`. Branch:
`codex/studio2-soglie-normal-correzioni`. HEAD/base:
`819b12e97fb94d501032655ec2f226139e6c5ca5`.

Verificatore: **`gpt-5.6-sol`**, reasoning **`high`**. Identificatori disponibili:
sessione Codex `01a0a03d-6daf-7540-947c-6f94ab12b2f5`, task/thread
`01a0a055-44a5-72d0-9b35-5549605786a1`. Data: 2026-09-14, Europe/Rome.

## Coerenza del supporto di riproducibilità

✅ `requirements-c4.txt`, SHA-256
`3771deff6e6212d2a58a49c137f23704664e1264d3fbc12344b3691c0ca6752f`, fissa le tre
dipendenze dirette necessarie al calcolo e ai test: NumPy 2.4.6, SciPy 1.17.1 e pytest
9.1.1. Le versioni coincidono con
`/Users/luker/verifica-soglie-normal-support-WE8Qqc/requirements.txt`, con
`environment.txt` dello stesso supporto e con i metadati dei pacchetti installati nel venv
storico. NumPy e SciPy coincidono anche con l’ambiente registrato in
`THRESHOLD_UNCERTAINTY.json`.

✅ `REPRODUCIBILITY_C4.md`, SHA-256
`e0ef4f2e1dbe042735f505312164f690b27aec0f57bbd27b1d4cb2fe5f8b1aea`, dichiara
CPython 3.11.5 e la piattaforma originale; rimanda al file di versioni; crea un venv in una
directory ottenuta con `mktemp -d`; installa le dipendenze fissate; produce un nuovo output
temporaneo anziché sovrascrivere `THRESHOLD_UNCERTAINTY.json`; disabilita bytecode e cache
pytest. Percorsi e riferimenti usati dai comandi esistono. `python3.11` è risolvibile
nell’ambiente corrente, ma i comandi non sono stati eseguiti, come richiesto.

✅ Le istruzioni distinguono correttamente i campi destinati a variare (`created_at_utc` e
ambiente corrente) dai valori scientifici. Ricordano che lo script controlla gli hash degli
input prima e dopo e rifiuta output esistenti. Non richiedono il rollout dell’esecutore per
la riproduzione numerica.

✅ Il report, SHA-256
`e25b45e16f00b588594557e09276e77f0321bcba37aebf8f096b423a2ae8b75f`, conserva il
comando originario come fatto storico e lo etichetta esplicitamente come tale; subito dopo
indica la nuova procedura locale e i due supporti. Non presenta il venv esterno come requisito
futuro. I due nuovi file sono elencati anche nella sezione dei file della revisione.

## N1 e impronte scientifiche

✅ N1 è invariata e mantiene entrambi gli intervalli e l’interpretazione già approvata:

- `[12,2632210962;14,2087372188]` con massa **95,38705407%**;
- `[12,2632210962;14,4086543351]` con massa **96,89204510%**.

Il report continua a descriverle come masse nella distribuzione bootstrap empirica
condizionata ai 350 score osservati, non come garanzie di copertura del quantile della
popolazione; non sostituisce soglia o risultato congelato.

✅ Fra i sei file dello snapshot approvato, cinque impronte sono immutate e soltanto il report
ha il nuovo hash richiesto dal delta documentale:

| File | SHA-256 corrente | Esito |
|---|---|:---:|
| `studio2/PROVENIENZA.md` | `d0b59649ad307d3bb15c9b07015c106da8addba69be111fd8258503582f37585` | ✅ immutato |
| `REPORT_SOGLIE_NORMAL.md` | `e25b45e16f00b588594557e09276e77f0321bcba37aebf8f096b423a2ae8b75f` | ✅ unico cambiato |
| `THRESHOLD_UNCERTAINTY_PROTOCOL.json` | `711d9711587fd140dcb451ccbe48b42d35fdf1bc3043feb5fb5e6dea3921989b` | ✅ immutato |
| `complete_threshold_uncertainty.py` | `5fcbb2ede6f1fcea43e9c7fa6d6c9dc66a530ee9bafb8b2cc91658540ddffe57` | ✅ immutato |
| `THRESHOLD_UNCERTAINTY.json` | `70dbca42391a0eea6ca39e12dc2f4e81d1cbe9a527494aca09388ae74f153feb` | ✅ immutato |
| `tests/test_threshold_uncertainty.py` | `1fa8195d57dc090483db9d3c9c4391e4ec42365e579667d709d56f022be02f5a` | ✅ immutato |

La lista corrente dei nove oggetti funzionali del delta — i sei sopra, decisione autoriale e
i due nuovi supporti — ordinata per percorso e serializzata come righe `sha256sum`, ha
SHA-256 `ffff085c37b848efbabd39937160b0b98e181528a19a7d95a1f7d361a955ea1e`.

✅ I verbali conservati hanno ancora le impronte già registrate:

- `VERIFICA_DELTA_N1_IDENTITA.md`:
  `0c48cc8d0300decb172cf24a6c93d3af0024bc4861e084302eb0baf02c28e7fd`;
- `VERIFICA_DELTA_N1_IDENTITA_APPENDICE_01.md`:
  `71e949e595e8702fce83de37efbbd632baada415e02a8ef79d985a05dddfec46`.

## Verdetto e limiti

**OK** sul delta documentale di riproducibilità: versioni e istruzioni sono coerenti con
l’ambiente originale, la futura riproduzione non dipende dal venv esterno nominato dal comando
storico, N1 resta corretta e il solo report tra i sei file approvati ha cambiato impronta.

Questo OK non attesta una nuova esecuzione e non rivaluta i calcoli scientifici già verificati.
Non chiude la sotto-fase 03.5 né la Fase 03.
