NON OK

# Verifica indipendente del delta N1, identità dell’esecutore e decisione dell’autore — sotto-fase 03.5

## Oggetto esatto e identità della verifica

La verifica riguarda esclusivamente:

1. il delta successivo allo snapshot già approvato di `REPORT_SOGLIE_NORMAL.md`, SHA-256
   `5323438f8f2426f859537e12dee24139c3b8daa0b858b01934b4f7fc23308e32`: precisazione N1 e
   aggiornamenti di stato, evidenza e decisione;
2. l’identità dell’esecutore della correzione/C4 dichiarato come `gpt-6-astra`, reasoning
   `high`, sessione `01a09f81-e508-77e0-b510-872bdeba46e3`, controllata soltanto sui metadati
   pertinenti del rollout indicato;
3. la distinzione tra l’accettazione dell’autore in `DECISIONE_AUTORE_FAR.md` e le prove
   tecniche.

Worktree: `/Users/luker/fot-tep-correzione-soglie-normal`. Branch:
`codex/studio2-soglie-normal-correzioni`. HEAD e base:
`819b12e97fb94d501032655ec2f226139e6c5ca5`.

Verificatore: **`gpt-5.6-sol`**, reasoning **`high`**. Identificatori disponibili nel runtime:
sessione Codex `01a0a03d-6daf-7540-947c-6f94ab12b2f5`, task/thread di verifica
`01a0a055-44a5-72d0-9b35-5549605786a1`. Data: 2026-09-14, Europe/Rome.

Non sono stati ripetuti bootstrap completo, audit dei 500 workbook, simulazioni TEP,
calibrazione o riscaricamento della release. Nessun file oggetto è stato modificato. L’unica
scrittura è questo verbale; nessun commit, push, merge o tag.

Legenda: ✅ verificato sulla fonte primaria · ⚠️ limite o dipendenza residua · ❌ requisito
smentito.

## Esito determinante — le sei impronte dello snapshot approvato

❌ Il requisito «cinque impronte immutate e nuovo hash soltanto per il report» **non è
soddisfatto**. Sono rimasti byte-identici soltanto quattro dei cinque file diversi dal report:

| File | SHA-256 approvato | SHA-256 corrente | Esito |
|---|---|---|:---:|
| `studio2/PROVENIENZA.md` | `d0b59649ad307d3bb15c9b07015c106da8addba69be111fd8258503582f37585` | `f50dc640f66c84a095c4931e4a0fef7c500d9cb747f9b7ebe1be9f969e312941` | ❌ cambiato |
| `REPORT_SOGLIE_NORMAL.md` | `5323438f8f2426f859537e12dee24139c3b8daa0b858b01934b4f7fc23308e32` | `bac095b009ed50fd758ac5b613c582f82a5dc3253c67a6226b667688653b16c4` | ✅ nuovo hash atteso |
| `THRESHOLD_UNCERTAINTY_PROTOCOL.json` | `711d9711587fd140dcb451ccbe48b42d35fdf1bc3043feb5fb5e6dea3921989b` | uguale | ✅ |
| `complete_threshold_uncertainty.py` | `5fcbb2ede6f1fcea43e9c7fa6d6c9dc66a530ee9bafb8b2cc91658540ddffe57` | uguale | ✅ |
| `THRESHOLD_UNCERTAINTY.json` | `70dbca42391a0eea6ca39e12dc2f4e81d1cbe9a527494aca09388ae74f153feb` | uguale | ✅ |
| `tests/test_threshold_uncertainty.py` | `1fa8195d57dc090483db9d3c9c4391e4ec42365e579667d709d56f022be02f5a` | uguale | ✅ |

Il delta inatteso di `PROVENIENZA.md` sostituisce tre righe: la decisione prima lasciata
all’autore viene dichiarata approvata il 2026-09-14 e collegata a
`fase03/soglie_normal/DECISIONE_AUTORE_FAR.md`. La formulazione è semanticamente coerente con
la decisione e continua a distinguerla dalle prove tecniche, ma resta una modifica ulteriore
di uno dei cinque file che dovevano risultare immutati. Il suo diff snapshot→corrente ha
SHA-256 `519be99c66029123bdc535cf3ae30f63cab8f1b3020e9e2f4c90f19f127ad708`.

## Hash del delta verificato

Il diff Git `--no-index --full-index --binary --no-renames` tra snapshot approvato e report
corrente ha SHA-256
`ae8c0615806a814724aee76d3d931cffffe49cb3862cf01f7798a5754b4d0977`.

Hash correnti degli otto file che descrivono il delta N1/stato/evidenza/decisione:

| File | SHA-256 |
|---|---|
| `studio2/PROVENIENZA.md` | `f50dc640f66c84a095c4931e4a0fef7c500d9cb747f9b7ebe1be9f969e312941` |
| `REPORT_SOGLIE_NORMAL.md` | `bac095b009ed50fd758ac5b613c582f82a5dc3253c67a6226b667688653b16c4` |
| `DECISIONE_AUTORE_FAR.md` | `84520c63e75d49a4855ce02421df59c5a641612cafa9d82fdfc2e127ebcce58e` |
| `evidence/EXECUTOR_IDENTITY.json` | `dd7066c08e28c142e809393bad3a35373159ffd2b41078b79dc7d3ae10799166` |
| `evidence/REPORT_SOGLIE_NORMAL_SNAPSHOT_OK.md` | `5323438f8f2426f859537e12dee24139c3b8daa0b858b01934b4f7fc23308e32` |
| `evidence/VERIFICA_CORREZIONI_SOGLIE_NORMAL_OK.md` | `d98a2856647493b0e96fc1198ac32c457510fc10399538511373655e1b6f1c9e` |
| `evidence/VERIFICA_SOGLIE_NORMAL_NON_OK_819b12e.md` | `ccaec80994522ba5167fdf9ef6f3500d220c19f86977de53afdb2dee7be548bd` |
| `evidence/mc_vs_exact_container.json` | `44c64fe1746434bc7f9691c048aa8087adb48dd18a4ff68f64420df84d303ca4` |

La lista sopra, ordinata per percorso e serializzata come righe prodotte da `sha256sum`, ha
SHA-256 `c1c237cf90ccbd1041796aa04e92db3e0fc0c61c9e5057d60f48a5a2e4122d1c`.

## N1 — interpretazione e controllo numerico

✅ Il report conserva entrambi gli intervalli:

| Intervallo chiuso della soglia | Massa nella distribuzione bootstrap empirica |
|---|---:|
| Monte Carlo `[12,2632210962; 14,2087372188]` | **95,38705407%** |
| Inversa generalizzata `[12,2632210962; 14,4086543351]` | **96,89204510%** |

✅ Le quantità sono presentate correttamente come masse/probabilità nella distribuzione
bootstrap empirica **condizionata ai 350 score osservati**, non come garanzie di copertura del
quantile della popolazione. Il testo mantiene esplicitamente il risultato Monte Carlo e il
controllo tramite inversa generalizzata; non sostituisce la soglia operativa.

✅ Controllo autonomo senza ripetere il bootstrap: sugli score ordinati, usando
`P(T* ≤ x_j) = P(Binom(350, j/350) ≥ 334)`, risultano
`F(x_324)=0,020944132694359879`, `F(x_340)=0,9748146733586166` e
`F(x_341)=0,98986458371307851`. Quindi
`F(x_340)-F(x_324)=0,95387054066425669` e
`F(x_341)-F(x_324)=0,9689204510187186`, coerenti con le percentuali riportate. Le code
superiori sono rispettivamente `2,51853266413834%` e `1,01354162869215%`.

✅ Risultati teorici, stime empiriche e calcoli supplementari post-hoc restano distinti:
la Beta(17,334) è qualificata come legge teorica sotto continuità/IID/score fissato; bootstrap
e distribuzione esatta sul campione sono condizionati ai dati osservati; seed, 10.000 repliche
e convenzione percentile sono dichiarati post-hoc rispetto ai risultati ma fissati prima del
calcolo supplementare.

## Identità dell’esecutore

✅ È stato letto direttamente, limitatamente ai record pertinenti, il rollout
`/Users/luker/.codex/sessions/2026/09/14/rollout-2026-09-14T12-41-25-01a09f81-e508-77e0-b510-872bdeba46e3.jsonl`.
Il file corrente ha SHA-256
`45c71aca14e2f40818f394c29e7a52f160493c0c8c56759c62976075960f3aad` e dimensione
5.883.210 byte.

✅ Il record `session_meta` riporta id `01a09f81-e508-77e0-b510-872bdeba46e3`, origine
`Codex Desktop` e cwd `/Users/luker/fot-tep`. Tutti gli **otto** record `turn_context`
riportano `model = gpt-6-astra` ed `effort = high`; le otto marche UTC coincidono con
`evidence/EXECUTOR_IDENTITY.json`. Il JSON acquisito usa correttamente il campo concettuale
“reasoning efforts”; nel rollout il valore è materialmente nel campo `payload.effort`.

✅ Il rollout integrale non è stato copiato nel repository. È conservata soltanto la
trascrizione minima dei metadati. Limite: questi metadati identificano la configurazione
registrata, non costituiscono attestazione crittografica del modello effettivamente servito.

## Decisione dell’autore e prove tecniche

✅ `DECISIONE_AUTORE_FAR.md` separa nettamente i piani: l’autore accetta l’uso dei risultati
FAR e mantiene la soglia; il documento dichiara però che la decisione **non** prova la mancata
consultazione dei file prima del freeze, non riapprova metodo/soglia e non chiude la Fase 03.

✅ Il report descrive le tracce disponibili, il limite di segregazione e ciò che sigilli/log
non possono dimostrare; poi attribuisce separatamente all’autore l’accettazione del limite.
Anche il nuovo testo in `PROVENIENZA.md` dice che la decisione resta distinta dalle prove
tecniche. La distinzione sostanziale è corretta nonostante il difetto di impronta sopra.

⚠️ Per vincolo dell’oggetto sono stati letti nel rollout soltanto i metadati di identità, non
il contenuto conversazionale. Questa verifica valuta quindi la corretta registrazione e il
perimetro dell’accettazione nel documento autoriale, non una certificazione esterna della
risposta «ok».

## Integrità delle evidenze e degli artefatti congelati

✅ Confronti `cmp` byte per byte:

- il verbale NON OK acquisito coincide con
  `/Users/luker/fot-tep-verifica-soglie-normal/studio2/fase03/soglie_normal/VERIFICA_SOGLIE_NORMAL.md`;
- il verbale OK acquisito coincide con
  `/Users/luker/fot-tep/.worktrees/riverifica-soglie-normal/studio2/fase03/soglie_normal/VERIFICA_CORREZIONI_SOGLIE_NORMAL.md`;
- lo snapshot approvato coincide con il `REPORT_SOGLIE_NORMAL.md` dello stesso worktree di
  riverifica;
- `evidence/mc_vs_exact_container.json` coincide con
  `/Users/luker/tmp/riverifica-soglie-normal-support-tsO8AV/out/mc_vs_exact_container.json`.

✅ Gli indici esterni restano integri: `SUPPORT_SHA256.csv` WE8Qqc, 56/56 voci, hash
`c109c36e83413d6924ab4892b1756d96197833b8b8f572b4c005cdac8bab825b`; indice della
riverifica, 21/21 voci, hash
`f2022f9d10852332971df94e755e1310e56a9b39bfdf97fe8591c99abc2c29cc`.
Il vecchio `DELIVERY_SHA256.csv` ha hash
`497c7ad2fe6b5061e05f7c4b4a827426873ddc41d881257d9aa8cf5b82c51d39`: 14/16 riferimenti
correnti coincidono; i due mismatch sono precisamente il report, atteso, e
`PROVENIENZA.md`, inatteso.

✅ Soglia, score e artefatti congelati non sono cambiati rispetto a `819b12e`: nessun diff
per `CAL_THR_SCORES.csv`, `THRESHOLD_FREEZE.json`, `FAR_VERIFICATION.json`,
`MANIFEST_CONSERVAZIONE.csv` e `ARTIFACT_STORAGE.json`. Impronte principali: score
`a1c5991af1ee136372b1da7c63ab05027d9710fd99c228a549395964d5519191`; freeze
`ff5c27002a2548003e4bc5f54805cda3754fb19b9cb2559222996b9c7f7e14a9`; piano cal
`fae355fdfd6db17b25e55c72f174ee8c7bb9c8b298facfb9a8012908f921a3ad`; FAR
`458ded0f4300fea8ab77a962cb9ef6d38f903ff4241fada563029765521f82f8`.

## C4, riproducibilità e test

✅ Senza eseguire il bootstrap completo, codice, protocollo e risultato C4 corrispondono:
350 score/run, rango 334, PCG64 seed 20260914, 10.000 repliche, 334ª statistica d’ordine,
percentile lineare 95%, SE con `ddof=1`, fit fisso, controllo degli hash prima e dopo,
rifiuto della sovrascrittura. Il risultato incorpora gli hash correnti di protocollo, script
e input; n/rango/soglia/regola coincidono con il freeze. Il controllo esatto indipendente N1
conferma la parte interessata del risultato.

⚠️ Restano dipendenze temporanee per la riproduzione locale. Il Python di sistema non ha
`pytest`; gli 8 test sono stati eseguiti col venv esterno
`/Users/luker/verifica-soglie-normal-support-WE8Qqc/venv`. Lo script C4 importa SciPy, che non
è elencato nel `requirements.txt` radice; quel file fissa inoltre NumPy 2.5.2, mentre il
risultato registra NumPy 2.4.6 e SciPy 1.17.1. Il comando di riproduzione nel report punta
direttamente al venv esterno. Ambiente e versioni sono registrati e i piccoli artefatti
necessari sono presenti, ma l’ambiente esatto non è ricostruibile dal solo manifest delle
dipendenze del repository. È presente anche `tests/__pycache__/` ignorata, già osservata
prima dei test di questa verifica e non rimossa.

✅ Test della sotto-fase:

- `PYTHONDONTWRITEBYTECODE=1 .../venv/bin/python -m pytest -p no:cacheprovider studio2/fase03/soglie_normal/tests -q` → **8 passed**;
- `PYTHONDONTWRITEBYTECODE=1 python3 .../test_generation_plan_stdlib.py` → **PASS**.

✅ Guardiano documentale: `python3 docs/test_explanation.py` → **35 test, 14 fallimenti,
1 skip**. Le 14 identità, inclusi i parametri dei subtest, hanno SHA-256
`2b7822702c2a04114f5caa0fcbb95ae51425f7939c1fe351d843af623ba31c34`, identico a
`/tmp/fot-tep-035-docs-before.log`. I fallimenti sono quindi preesistenti e non peggiorati;
il guardiano non convalida C4.

## Verdetto e limiti

**NON OK**, limitatamente al delta N1/identità/decisione: N1 è numericamente e
interpretativamente corretta, l’identità `gpt-6-astra`/`high`/sessione è confermata dai
metadati, le evidenze acquisite sono byte-identiche e la decisione autoriale resta distinta
dalle prove tecniche. Tuttavia il vincolo esplicito sulle sei impronte è smentito: oltre al
nuovo hash obbligato del report è cambiato anche `studio2/PROVENIENZA.md`.

Il verdetto non rivaluta lo snapshot già approvato, non invalida automaticamente il contenuto
scientifico del delta, non decide per l’autore sul FAR e **non chiude la sotto-fase 03.5 né
l’intera Fase 03**.

Letture: integralmente `docs/MAINTENANCE.md`, `docs/prompts/Prompt_LLM.md`,
`docs/prompts/Verifica_LLM.md`; report corrente e snapshot, verbali ed evidenze acquisite,
decisione autoriale, delta di provenienza, protocollo/codice/risultato/test C4; metadati
pertinenti del rollout indicato; manifest e supporti esterni mirati. Costo stimato di lettura:
circa 20–25 mila token, non di fatturazione.
