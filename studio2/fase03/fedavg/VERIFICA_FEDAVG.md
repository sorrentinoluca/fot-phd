OK

# Riverifica indipendente della remediation — 03.14

**Verdetto corrente: OK**, esclusivamente per il pacchetto specifica/codice/loader/test sintetici/smoke su fixture al commit **d56354934d2b5f88dace3f9b312fcf64ce3cf42b**. **R1 e R2 sono chiusi**. Questo OK **non chiude 03.14**, non attesta training reale, smoke su `normal_dev`, valutazione finale, confronto con il braccio LLM o congelamento efficace.

**Modello:** Codex basato su **GPT-6**, identificazione disponibile nelle istruzioni della sessione; variante/backend non esposti, non inventati. Il report dell'esecutore continua a dichiarare Codex/GPT-5. Riverifica svolta nella stessa conversazione indipendente che ha prodotto il primo NON OK, distinta dall'esecuzione della remediation, senza sottoagenti.
**Finestra strumentale:** 14 settembre 2026, dalle **09:39:10 UTC** (11:39:10 Europe/Rome) a **2026-09-14 09:42:31 UTC** (Europe/Rome = UTC+2).
**Worktree:** `/Users/luker/fot-tep-verifica-fedavg`, ispezionato prima dell'uso: soltanto il precedente verbale non tracciato, nessuna modifica ai file tracciati. Avanzato in detached da `b39b723` a `d563549`, preservando il verbale. Il testo della prima verifica è conservato **integralmente nell'appendice storica** di questo stesso file. I suoi rilievi, linee e riferimenti allo stato del worktree valgono per `b39b723`, non per il nuovo HEAD.

L'unico file persistente scritto dalla riverifica è questo verbale. Nessuna modifica al worktree dell'esecutore, al codice, alla specifica, al report, al freeze o a PROVENIENZA. Nessun commit, push, merge, tag, walkthrough, simulazione TEP o chiamata sperimentale a modelli.

## Controlli effettivi e chiusura dei rilievi

✅ **Perimetro e sequenza.** `git diff --name-status b39b723 d563549` elenca solo cinque file: `fedavg.py`, `test_fedavg.py`, `FEDAVG_FREEZE.json`, `REPORT_FEDAVG.md` e la coda di `studio2/PROVENIENZA.md`. La specifica, la CLI smoke, requirements e tutti gli artefatti smoke sono invariati. Il diff completo di codice modifica esclusivamente guardie di dataset/split/loader; training, ricetta, loss, maschera, aggregazione e metriche non cambiano. Le verifiche numeriche dettagliate della prima revisione restano quindi pertinenti, integrate dalle riesecuzioni seguenti.

Catena verificata dai parent Git:

- `b39b723e059ba195240afad2c0b553d537f93298` → `e5d5a51c87d54561750e5217215d6ed19dcd7cb7`, guardie e test (14 settembre, 11:36:34 +02:00).
- `e5d5a51c87d54561750e5217215d6ed19dcd7cb7` → `d56354934d2b5f88dace3f9b312fcf64ce3cf42b`, freeze/report/provenienza (11:37:36 +02:00).

✅ **R1 chiuso — run→batch univoco e disgiunzione esplicita.** In `/Users/luker/fot-tep-verifica-fedavg/studio2/fase03/fedavg/fedavg.py:58` il costruttore raccoglie i batch per run e rifiuta quelli incoerenti. A riga 243 lo split controlla inoltre l'intersezione degli ID fra training e validazione. Rieseguito il controesempio originario: ora `ValueError: each physical run must map to one batch: ['fixture-normal-F1-b01']`. Esercitata separatamente la seconda guardia: costruita una fixture valida, modificato in seguito il suo array `clusters` (gli array restano mutabili), invocato lo split; ora `ValueError: physical runs cross training/validation folds: ['fixture-normal-F1-b01']`. Non si è dedotto il funzionamento della seconda guardia dal solo test del costruttore.

✅ **R2 chiuso — controlli su tutti gli input prima dell'apertura.** `_confined_regular_file` a `fedavg.py:100` rifiuta symlink in ogni componente sotto la radice, richiede risoluzione dentro la radice e file regolare, applica la guardia sviluppo al percorso risolto. `load_evidence_bundle:161–177` verifica radice, manifest e indice prima degli hash e delle aperture; la firma passa nello stesso controllo a righe 207–209 prima di `_read_signature`.

Nove prove aggiuntive su directory/CSV **esclusivamente fittizi**, tutte rifiutate con `ValueError`:

| Caso avversario | Risultato |
|---|---|
| Manifest symlink a CSV sotto una directory fittizia `test` | symlink rejected |
| Indice symlink a CSV sotto `test` fittizio | symlink rejected |
| Firma symlink a CSV sotto `test` fittizio | symlink rejected |
| Directory delle firme symlink a directory esterna al bundle | symlink rejected |
| Radice del bundle symlink | root symlink rejected |
| Manifest FIFO | not a regular file |
| Indice sostituito da directory | not a regular file |
| Firma FIFO | not a regular file |
| Firma symlink a un file regolare **interno** al bundle | symlink rejected |

Per manifest/indice/radice è stata sostituita temporaneamente **in memoria**, via `unittest.mock.patch.object`, `sha256_file` con una sentinella che avrebbe fallito se invocata; per le firme, sentinella su `_read_signature`. Sono arrivate le eccezioni delle guardie, non quelle delle sentinelle: il file vietato non raggiunge l'apertura/hash/parsing. Nessun vero test aperto e nessuna modifica persistente al codice.

✅ **Suite: 11/11**, `Ran 11 tests in 0.433s`, exit 0, NumPy 2.3.5. Inclusi i tre nuovi test di regressione. Restano distinti `FAST` della suite e `Config()` congelato dei due smoke CLI, come già documentato nella prima verifica.

✅ **Smoke sintetico con ricetta integrale: due riesecuzioni**, exit 0. Tutti e tre i file sono byte-identici (a) fra le due nuove esecuzioni, (b) agli artefatti registrati nel nuovo commit e (c) agli output indipendenti della prima verifica. Accuratezze **0,5625 / 1,0 / 1,0**, astensione 0, 128 campioni training, 32 validazione, 16 cluster. Pertanto anche gli hash dei dieci modelli coincidono. Sono controlli tecnici sintetici; non prestazioni reali.

✅ **Loader reale rieseguito senza training:** **320×697**, **40 cluster**, 256 campioni nel fold training e 64 nel fold validazione, intersezione dei run **vuota**. Usata la copia del bundle 03.6 **riscaricata dalla release durante la prima verifica di questa conversazione**: non si dichiara un secondo download. L'archivio è stato nuovamente sottoposto a SHA-256 (`3e1eb87f38ff3fc6dd3346476785d06c2b98944b209f7f58706b3c71c1676999`); il nuovo loader ha riverificato gli hash attesi di manifest, indice e tutte le firme prima del parsing. Il confronto completo dei 1283 payload con il manifest di conservazione resta quello documentato nella prima verifica. Non caricati Normal reali, né usati run per scelte di iperparametri.

✅ **Freeze: 8/8 hash ricalcolati e corrispondenti.** I due hash cambiati sono:

- `fedavg.py`: `57b580ec41f3b9f9591ae35cd34d1d68d2b29051b6e5b806d8b902325babed92`.
- `test_fedavg.py`: `ef25d3f56512971b75e0a1513c01e8bd49ff8943a4c2ea7efa21abf5ef4755f3`.

Gli altri sei coincidono con la tabella dell'appendice, anch'essi ricalcolati in questa riverifica. `implementation_commit` punta alla remediation `e5d5a51`; `review_history` conserva il NON OK precedente; `independent_review=pending_reverification_after_remediation` descrive correttamente lo stato prima di questo verbale. **effective=false**, `real_training_performed=false`; dipendenze 03.9/03.8/03.11 invariate e aperte. Non ho alterato il freeze per far recepire questo OK.

✅ **Report e PROVENIENZA allineati alla remediation:** registrano R1/R2, nuovi test e necessità di riverifica senza cambiare ricetta o ruoli dei dati. I numeri dichiarati sono confermati dalle prove, non assunti dal report.

✅ **Guardiano documentale rieseguito su `d563549`: 35 test, 14 failure, 1 skip**, exit 1 atteso. Il log completo è identico a quello della base `46c0b62` eseguita nella prima verifica, normalizzando soltanto le radici dei percorsi e il tempo: stessi failure/subtest e stessa diagnostica, non solo stesso totale. Le quattordici identità e l'hash della diagnostica normalizzata restano quelli elencati nell'appendice. Nessun peggioramento documentale. Rieseguito anche dopo la scrittura del verbale: stesso esito e stessa diagnostica completa, normalizzando il solo tempo.

⚠️ **Limiti ancora validi, non bloccanti per questo pacchetto:** non effettuati training/smoke reali o confronto LLM; integrazione statistica 03.8/03.10 non attestata come completata; il campo `PASS` dello smoke resta incondizionato nel runner e acquista significato qui dai controlli indipendenti sui risultati. Restano le precisazioni storiche sul richiamo alla revisione 7 e sul corpus, già documentate. Nessuno di questi punti amplia il mandato o riapre R1/R2.

## Ambiente, comandi e tracciabilità

Stesso ambiente isolato della prima verifica: `/tmp/fedavg-review-NKu7lF/venv/bin/python`, Python **3.13.9**, NumPy **2.3.5**, macOS 26.6.2 arm64, BLAS/LAPACK Accelerate. Guardiano documentale: `/usr/local/bin/python3`, **3.11.5**. Output nuovi soltanto in `/tmp/fedavg-review-NKu7lF/recheck/`.

Comandi effettivi, dalla radice del worktree di verifica:

```bash
git switch --detach d56354934d2b5f88dace3f9b312fcf64ce3cf42b
git diff --name-status b39b723 d563549
git log --format='%H %P %cI %s' b39b723..d563549
PYTHONDONTWRITEBYTECODE=1 /tmp/fedavg-review-NKu7lF/venv/bin/python -m unittest studio2.fase03.fedavg.test_fedavg -v
PYTHONDONTWRITEBYTECODE=1 /tmp/fedavg-review-NKu7lF/venv/bin/python -m studio2.fase03.fedavg.smoke_fedavg --out /tmp/fedavg-review-NKu7lF/recheck/smoke1
PYTHONDONTWRITEBYTECODE=1 /tmp/fedavg-review-NKu7lF/venv/bin/python -m studio2.fase03.fedavg.smoke_fedavg --out /tmp/fedavg-review-NKu7lF/recheck/smoke2
PYTHONDONTWRITEBYTECODE=1 python3 docs/test_explanation.py
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/Users/luker/fot-tep-verifica-fedavg /tmp/fedavg-review-NKu7lF/venv/bin/python /tmp/fedavg-review-NKu7lF/recheck/recheck.py
```

Lo script aggiuntivo temporaneo (exit 0) esercita i casi descritti, chiama il nuovo loader senza training, ricalcola gli otto hash, confronta i nove confronti byte dei file smoke e l'intera diagnostica documentale. Fonti lette in questa finestra: contratto e prompt di verifica riletti; `Prompt_LLM.md` e mandato specifico già letti e rispettati nella stessa conversazione; diff completo dei cinque file della remediation; linee pertinenti del nuovo codice/test; report, freeze e PROVENIENZA aggiornati; vecchio verbale e risultati delle nuove esecuzioni. Nessuna rilettura in blocco della letteratura. Costo aggiuntivo indicativo: **8–12 mila token** fra istruzioni, diff e risultati.

**Esito corrente: OK del solo pacchetto verificato; R1 e R2 risolti.** Il NON OK che segue è la registrazione storica integrale del precedente commit, superata esclusivamente nei rilievi chiusi sopra.

---

# Appendice storica — verbale originale su b39b723 (NON OK, superato dalla riverifica sopra)

Impronta SHA-256 del testo originale conservato qui sotto: `3e33b0fdc3b3ec1ae9e094288109308af8304cc647d4d20094e423a701c311d0`.

NON OK

# Verifica indipendente — 03.14, pacchetto FedAvg minimale

Commit verificato: **b39b723e059ba195240afad2c0b553d537f93298**, branch oggetto `codex/studio2-fedavg`.
Base dichiarata e confermata: `46c0b623f55154684f326a8523521fb28991fb09`.
Worktree di verifica creato ex novo, **detached**: `/Users/luker/fot-tep-verifica-fedavg`.
Worktree dell'esecutore: `/Users/luker/fot-tep/.worktrees/studio2-fedavg`, non modificato; HEAD confermato e stato finale pulito.

**Verificatore:** Codex basato su **GPT-6**, come identificato dalle istruzioni della sessione. Non è esposto un identificativo più specifico del modello/backend, né un identificativo verificabile della finestra dell'esecutore: non vengono inventati. Il report dell'esecutore dichiara Codex/GPT-5; tale dichiarazione è documentale, non un'attestazione del suo backend. Questa è la distinta conversazione di verifica richiesta dall'autore, senza sottoagenti.
**Finestra:** 14 settembre 2026, circa **11:12–11:22 Europe/Rome (09:12–09:22 UTC)**; primo timestamp esplicitamente registrato 09:13:22 UTC. L'inizio è approssimato, non un timestamp strumentale.

Il giudizio riguarda solo specifica, implementazione, loader, suite sintetica e smoke su fixture di questo commit. Non chiude 03.14, non attesta training reale, valutazione finale, confronto LLM o congelamento efficace. Nessuna simulazione TEP, chiamata sperimentale a modelli, operazione Git di pubblicazione o modifica al walkthrough. Nessun training o smoke su `normal_dev`, anche se divenuto disponibile altrove.

## Ambiente e comandi effettivi

- Suite, smoke e prove aggiuntive: Python **3.13.9**, Anaconda, Clang 20.1.8; NumPy **2.3.5** installato in un venv temporaneo; macOS **26.6.2**, arm64; BLAS/LAPACK **Accelerate**, versione non esposta da NumPy.
- Interprete: `/tmp/fedavg-review-NKu7lF/venv/bin/python`, derivato da `/Users/luker/fot-env/bin/python`.
- `python3` predefinito: `/usr/local/bin/python3`, **3.11.5**, privo di NumPy; usato per `docs/test_explanation.py`. L'ambiente condiviso aveva NumPy 2.5.2: non è stato modificato e non è stato usato per produrre i risultati FedAvg.
- Tutti gli output di lavoro sono sotto `/tmp/fedavg-review-NKu7lF`; `PYTHONDONTWRITEBYTECODE=1` ha evitato cache nel worktree. L'unico nuovo documento persistente è questo verbale.

Comandi principali realmente eseguiti (i comandi Python FedAvg dalla radice del worktree di verifica):

```bash
git worktree add --detach /Users/luker/fot-tep-verifica-fedavg b39b723e059ba195240afad2c0b553d537f93298
git diff --name-status 46c0b62 HEAD
git log --format='%H %P %cI %s' 46c0b62..HEAD
git diff 46c0b62 HEAD -- studio2/PROVENIENZA.md
/Users/luker/fot-env/bin/python -m venv /tmp/fedavg-review-NKu7lF/venv
/tmp/fedavg-review-NKu7lF/venv/bin/python -m pip install numpy==2.3.5
PYTHONDONTWRITEBYTECODE=1 /tmp/fedavg-review-NKu7lF/venv/bin/python -m unittest studio2.fase03.fedavg.test_fedavg -v
PYTHONDONTWRITEBYTECODE=1 /tmp/fedavg-review-NKu7lF/venv/bin/python -m studio2.fase03.fedavg.smoke_fedavg --out /tmp/fedavg-review-NKu7lF/smoke1
PYTHONDONTWRITEBYTECODE=1 /tmp/fedavg-review-NKu7lF/venv/bin/python -m studio2.fase03.fedavg.smoke_fedavg --out /tmp/fedavg-review-NKu7lF/smoke2
curl -fL --retry 2 -o /tmp/fedavg-review-NKu7lF/evidence.tar https://github.com/sorrentinoluca/fot-tep-data/releases/download/studio2-fase03-evidence-v1/studio2-fase03-evidence-v1.tar
PYTHONDONTWRITEBYTECODE=1 python3 docs/test_explanation.py
mkdir /tmp/fedavg-review-NKu7lF/base
git archive 46c0b62 | tar -x -C /tmp/fedavg-review-NKu7lF/base
(cd /tmp/fedavg-review-NKu7lF/base && PYTHONDONTWRITEBYTECODE=1 python3 docs/test_explanation.py)
```

Sono stati eseguiti anche `audit.py`, `extra.py` e `probes.py`, scritti esclusivamente nella directory temporanea, con `PYTHONDONTWRITEBYTECODE=1`, l'interprete del venv e `PYTHONPATH=/Users/luker/fot-tep-verifica-fedavg`. Esito 0 per suite, smoke, download e script aggiuntivi; esito 1 atteso per entrambe le esecuzioni documentali. I risultati necessari sono riportati qui: i log temporanei non costituiscono una dipendenza del verbale.

## Controlli e fonti primarie

I riferimenti `fedavg.py`, `SPECIFICA_FEDAVG.md`, `REPORT_FEDAVG.md`, `test_fedavg.py`, `smoke_fedavg.py` e `FEDAVG_FREEZE.json` nelle sezioni seguenti sono relativi a `/Users/luker/fot-tep-verifica-fedavg/studio2/fase03/fedavg/`, sempre al commit verificato.

### 1. Perimetro, provenienza e ordine

✅ Il diff contiene esattamente 12 file: 11 nuovi sotto `studio2/fase03/fedavg/` e 21 righe aggiunte in coda a `studio2/PROVENIENZA.md` (§10, righe 271–291). Nessun artefatto congelato né coppia MD/HTML modificati. La ricerca degli import non trova dipendenze da `phase_b/` o `code/`; codice NumPy/stdlib e import interni soltanto.

✅ Catena dei parent Git, senza commit intermedi estranei:

| Commit | Timestamp del commit | Contenuto |
|---|---|---|
| `deed792ba467826018a20907144e5577fbfbd85c` | 2026-09-14 00:14:52 +02:00 | Solo specifica, 93 righe |
| `ab6ee5c57b17acec009fad8942d6d2b7b10bece2` | 2026-09-14 00:32:31 +02:00 | Implementazione, loader, test e CLI smoke |
| `b39b723e059ba195240afad2c0b553d537f93298` | 2026-09-14 00:33:33 +02:00 | Artefatti smoke, freeze pending, report, provenienza |

La storia dimostra l'ordine delle registrazioni e che la specifica è invariata; non permette di attestare attività non registrate dell'esecutore. PROVENIENZA riporta origine, commit, SHA e marca pre-specificata, input Normal futuro e dipendenza indiretta U3/R2 delle firme 03.6; non vi è riuso diretto del primo studio nel codice FedAvg.

### 2. Ricetta e tre modalità

✅ Specifica righe 19–54 e codice `Config` righe 25–35, inizializzazione 218–227, SGD 241–277, training 295–345: MLP float64 **697→32→9**, ReLU, bias; Glorot uniforme/PCG64; seed **20260914**; z-score con std <1e-8 sostituita da 1; SGD **0,05**, senza momentum né weight decay; batch **32**, ultimo batch mantenuto; **5** epoche locali per **40** round; tutti gli **8** client; aggregazione per numerosità. Non risultano tuning, early stopping o astensione.

✅ Ricetta effettiva del pavimento: otto reti indipendenti, stesso seed iniziale, **200 epoche per client**, normalizzazione locale e pesi delle sole classi presenti. FedAvg: normalizzazione globale del training fornito, ogni round riparte dai medesimi parametri globali, pesi di classe stimati separatamente per client; aggregazione dei parametri dopo i cinque passaggi locali. Centralizzato: **200 epoche sull'unione del training**, normalizzazione e pesi globali. Lo shuffle ha seed derivati distinti per modalità/client/round/epoca. Il nome “soffitto” è correttamente dichiarato operativo, non una superiorità matematica garantita.

✅ `fit_normalizer` (206–210), `train_steps` (269–277) e chiamanti non ricevono la validazione dal runner: lo split precede `train_all_modes` (`smoke_fedavg.py:69`). Verificata numericamente l'uguaglianza delle medie salvate alle medie del solo training, locale per ogni client e globale per le altre modalità. Questa correttezza presuppone fold disgiunti: vedere R1.

✅ La specifica risponde a piano §6.11 e §9.2: output condiviso, sviluppo soltanto, ricetta unica e compatibilità dichiarata con 03.8/03.10. Non reimplementa il bootstrap e non anticipa decisioni statistiche. Il piano 03.8 è letto al commit referenziato `dd82cd1`, con stato proposto. La compatibilità è al livello delle unità/metriche; non attesta un'integrazione finale 03.10 già eseguita.

⚠️ Il mandato richiama una “revisione 7” del piano: nel file del piano incluso nello snapshot verificato non risultano tale intestazione o il testo sullo sbilanciamento. Il requisito sostanziale imposto dal mandato è comunque verificato positivamente sulla specifica e sulla formula sotto, senza attribuire allo snapshot un testo assente.

### 3. Fold, maschere, loss e metriche

✅ Fixture canonica: **128** esempi training, **32** validazione, **16** cluster validazione; intersezione degli ID di run vuota. Nel bundle fault reale: **256/64** esempi, **32/8** run, intersezione vuota. Ogni run reale ha un solo batch. La valutazione raggruppa per run (`fedavg.py:377–396`) e conserva il ricevente per il pavimento; negli input verificati gli ID sono univoci per run/fault.

❌ **R1 — lo split non garantisce il vincolo per run su input incoerenti accettati.** `fedavg.py:194–198` seleziona soltanto `dataset.batches`; `Dataset.__post_init__` (46–57) e il loader (170–177) non impongono run→batch univoco. La prova sotto produce lo stesso run in training e validazione senza errore. Contraddice la garanzia della specifica righe 64–65; può causare leakage fra finestre dello stesso run se l'indice contiene batch incoerenti. Non è leakage osservato nelle fixture canoniche o nel bundle 03.6: è una guardia mancante riprodotta. Prima dell'OK occorre rifiutare tale incoerenza/verificare la disgiunzione degli ID e coprirla con un test.

```python
from studio2.fase03.fedavg import fedavg as f
from studio2.fase03.fedavg.smoke_fedavg import synthetic_development_fixture
import numpy as np
d = synthetic_development_fixture()
c = d.clusters.copy()
c[np.flatnonzero(d.batches == '5')[0]] = c[0]
bad = f.Dataset(d.x, d.y, d.clients, c, d.batches)
train, validation = f.split_leave_one_batch_out(bad, '5')
print(set(train.clusters) & set(validation.clusters))
# {'fixture-normal-F1-b01'}; nessuna eccezione
```

✅ Maschera applicata in **inferenza**, `predict:348–355`: sette logit a −∞ per il pavimento. Test aggiuntivo con bias delle sette classi assenti = 1.000.000 e bias delle due visibili = 0: predizione ancora `Normal`. Sui fault altrui: **0 corretti per ciascuno degli otto client** nella fixture, coerente con la proprietà matematica, non una misura reale.

✅ Durante SGD la softmax resta sulle nove classi e **non** riceve −∞; la specifica richiede la maschera in inferenza, non nel training. Sottrazione del massimo, gradienti della CE pesata e nessun prodotto 0×−∞. Il codice non restituisce una loss scalare: è stata ricalcolata indipendentemente la CE finale con log-sum-exp, finita per tutti gli otto modelli locali; tutti i parametri finali sono finiti. Nessuna attestazione di loss su dati reali.

✅ I tre numeri sono accuracy complessiva, astensione=0, accuracy sui non astenuti uguale alla prima. Non confondere **astensione=0** con **accuracy local-unseen=0**: sono proprietà distinte. Ricalcolate tutte le 160 righe del CSV: locale 128 righe, 256 tentativi, **144 corretti**; ciascuno degli altri due modi 16 righe, 32 tentativi, **32 corretti**. Nessuna misura finale LLM o stima TEP implicata.

### 4. Verifiche numeriche di aggregazione e sbilanciamento

✅ `class_weights:234–238` usa **K = numero delle classi presenti**, zero per le assenti, e n/(K·n_k). `_sgd_epoch:255–259` normalizza la loss pesata per la somma dei pesi del minibatch. `train_steps` stima i pesi sull'intero training scope prima delle epoche, non sul lotto comprensivo della validazione.

| Fixture nota | Pesi restituiti |
|---|---|
| 40 Normal, 40 F1 | 1 e 1; altre classi 0 |
| 320 Normal, 40 per ciascuno degli 8 fault | 2/9 e 16/9: rapporto **1:8** |
| Fold fittizio 24 Normal, 32 F1 | **7/6** e **7/8**, non 1:1 |
| Parametri costanti 1 e 5, numerosità 1 e 3 | **4 esatto** per ogni elemento dei quattro tensori |

40/40 per client e 320/40 centralizzati sono attese del **lotto completo**. Il fault bundle verificato ha 40 finestre per fault, ma il fold batch=5 ne lascia **32 per fault nel training**. Non sono stati ipotizzati né caricati i conteggi Normal dei futuri fold reali. Il trattamento pre-training dello sbilanciamento è esplicito in specifica righe 40–43.

### 5. Suite e smoke sintetico

✅ **8/8 test**, 1,688 s. La suite usa `FAST` (`test_fedavg.py:27`) con LR 0,08, batch 16 e 2 epoche locali: non va confusa con la ricetta congelata. I due smoke CLI usano invece il `Config()` esatto e completo. Fixture separabile: FedAvg e centralizzato **1,0**; pavimento **0,5625**. Fixture nulla aggiuntiva con `Config()` completo: **0,5 in tutte e tre le modalità**. È il livello della classe maggioritaria Normal in questa fixture sbilanciata, non 1/9; nessuna superiorità al predittore maggioritario.

✅ Due smoke e tutti e tre gli artefatti registrati sono **byte-identici**; non solo metriche arrotondate. Determinismo quindi verificato anche per centralizzato e tutti i modelli locali, con normalizzatori inclusi nel digest. Nessun artefatto originale sovrascritto. Hash riportati nella sezione 7.

⚠️ `run_smoke` assegna `status="PASS"` senza soglie/assert sui risultati (`smoke_fedavg.py:80`). Il PASS dello smoke da solo non è una prova di apprendimento o di assenza di leakage; in questa verifica tali proprietà sono state controllate indipendentemente sui casi dichiarati. È una limitazione del significato del campo, non un fallimento dell'apprendimento osservato.

### 6. Loader, recuperabilità e sicurezza dei percorsi

✅ Release **realmente riscaricata**, non accettata sulla base del report: repository `sorrentinoluca/fot-tep-data`, tag `studio2-fase03-evidence-v1`, URL nel comando sopra, metadati letti da `2f6dd8d:studio2/fase03/evidence/ARTIFACT_STORAGE.json`. SHA dell'archivio verificato **prima dell'estrazione/caricamento**:
`3e1eb87f38ff3fc6dd3346476785d06c2b98944b209f7f58706b3c71c1676999`.

✅ Confrontati path, byte e SHA di **1283/1283** file con `MANIFEST_CONSERVAZIONE.csv` dello stesso commit: **61.208.618 byte**, nessuna discrepanza. Il tar contiene inoltre **1285 metadati AppleDouble `._*`**, non payload del manifest; non sono stati trattati come firme. Sono stati estratti per il loader solo indici e firme; gli altri payload sono stati letti come byte per l'hash, non interpretati come risultati.

✅ Hash manifest **5111d0c61c2e93fe5071d7a85015673549af0bf9c1dc74e0d940719a8400e020**, indice evaluator-side **b966cdd3d579efaf595fd48c4b9baa70747ba584522926520840a1e914dbf69c**; hash di ogni firma verificato prima del parsing (`fedavg.py:98–107,134–145,167`). Caricate **320 firme × 697 componenti finite**, 40 cluster, 8 client, 40 finestre per fault e 64 per batch. Join per evidence_id uno-a-uno, label/client da indice separato; nessun training reale eseguito dopo il caricamento, nessun uso dei run per scegliere iperparametri. Le condizioni scientifiche U3/R2 restano quelle della release 03.6, non sono state rivalutate in questa sotto-fase.

✅ Su dati **fittizi** sono stati rifiutati: manifest con hash errato; firma manomessa prima del parsing; evidence_id duplicati; join non corrispondente; firma con 696 componenti; NaN; leakage_pass=false; path assoluto; `..`; tutte le sette componenti vietate come radice e `test` nel percorso della firma. Sono errori effettivi, non sole ispezioni del codice.

❌ **R2 — guardia percorsi non fail-closed per tutti i file e mancato confinamento dei symlink.** In `fedavg.py:131–139` si controlla soltanto la radice: manifest e indice vengono aperti senza controllare i loro percorsi risolti. Un `EVALUATOR_INDEX.csv` oppure `EVIDENCE_MANIFEST.csv` symlink a un CSV fittizio sotto `/tmp/fedavg-review-NKu7lF/test/` viene **accettato e letto**, con hash corretti. Inoltre `fedavg.py:162–167` rifiuta assoluti e `..`, ma una firma `linked/signature.csv`, con `linked` symlink a una directory esterna al bundle senza nome vietato, è **accettata**. Il controllo di `resolve()` a righe 84–89 non impone che la destinazione resti dentro root.

Conseguenza: SHA corretto attesta i byte, non l'ammissibilità dello scope; la promessa di report righe 18–20 e specifica righe 80–82 è più forte del controllo implementato. Prima dell'OK occorre controllare tutti gli input prima della loro prima apertura e rifiutare i percorsi risolti esterni al bundle (o rifiutare esplicitamente i symlink), con test di regressione. La prova ha creato esclusivamente CSV sintetici e directory temporanee: **nessun vero percorso di test è stato aperto** per testare le guardie.

Riproduzione della vulnerabilità sull'indice: partire da un bundle fittizio valido come quello di `test_fedavg.py:87–125`; copiarne l'indice in `<temp>/test/index.csv`, sostituire l'originale con un symlink a quel file e chiamare `load_evidence_bundle` con i due hash corretti. Esito osservato: dataset valido anziché ValueError. Identica prova positiva sul manifest; distinta prova positiva sulla firma esterna tramite directory symlink. Queste prove non richiedono né autorizzano accesso a test reali.

### 7. Freeze e dipendenze

✅ Ricalcolate **8/8 impronte** elencate in `FEDAVG_FREEZE.json`, tutte corrispondenti:

| File sotto `studio2/fase03/fedavg/` | SHA-256 ricalcolato |
|---|---|
| `SPECIFICA_FEDAVG.md` | `62509115b60776c46ea803f131f2ea1a4aba5fe9fbc93b72f55975bfdff4f1e2` |
| `fedavg.py` | `96885a030627baf2eebe1537d7d358ca32f217ea8e3f0bc2c2877ced00ebf112` |
| `requirements.txt` | `7bd6b8946940b79948c548c8048e545684b91c8edc9444d8dfc0c8f76a97c0a7` |
| `smoke_fedavg.py` | `6d601bd869b185f61d808921b72208bf5b4320e5c43f76dc9a9cd56884a615e6` |
| `test_fedavg.py` | `1d4ee6bee686a82c6df6457ba20f92d09c3c7be4071628def7dda1c708f3b264` |
| `smoke_fixture/cluster_metrics.csv` | `1840ca6c5023d037f6797737f02f6ae425ef1756ffd3577597e219d716c37f1d` |
| `smoke_fixture/weight_hashes.json` | `7927b73afeb044f981b49627e9173c01d3228a9a633bd59231502a01019be2e5` |
| `smoke_fixture/SMOKE_SUMMARY.json` | `fcda9d12b3454bfc19cd56b252055e101a89862de07604718922fd052ab1b044` |

✅ Verificato anche l'hash del piano 03.8 tramite `git show dd82cd1:studio2/fase03/piano_statistico/PIANO_STATISTICO.md | shasum -a 256`: **c660db84474e54056ac623f51aceadcc771297b0af19870dc9c304c1dbf0bf96**. `requirements.txt` contiene il pin esatto NumPy 2.3.5.

✅ Stato `frozen_spec_and_code_pending_normal_dev_and_independent_verification`, **effective=false**, `real_training_performed=false`, `independent_review=pending`. Dipendenze 03.9 Normal, 03.8 proposto e 03.11 prima della valutazione finale esplicite (`FEDAVG_FREEZE.json:30–52`, specifica 86–93). La disponibilità successiva di un input non rende retroattivamente efficace il freeze. L'assenza del training reale è correttamente dichiarata e **non è un rilievo negativo**. Nessun iperparametro lasciato “da rivedere sui dati reali”.

### 8. Report, letteratura e regressione documentale

✅ Il report contiene i sette punti di `Fase_LLM.md`: sintesi, file, modello/profilo dichiarato, esclusioni, decisioni esterne, test documentale prima/dopo, commit e messaggio proposto. L'ultimo commit è il report stesso, pertanto la sua formulazione prospettica in §7 non è una discrepanza. La fonte primaria conferma i numeri sintetici e il caricamento reale; la pretesa di sicurezza dei percorsi è invece smentita da R2.

✅ McMahan è rinviato a `Letteratura_LLM`, senza inserimenti nel corpus né anticipazioni scientifiche. `docs/letteratura.md` contiene già menzioni nelle tabelle di contesto (§14.3 e successiva tabella, righe 523 e 598): “esterno al corpus corrente” nella specifica va letto come assenza di una nuova scheda integrale qui, non come assenza assoluta del nome nel documento. Non è stata svolta una nuova revisione bibliografica, fuori mandato.

✅ `docs/test_explanation.py`: **35 test, 14 failure, 1 skip** sia su HEAD sia sull'archivio temporaneo della base esatta. I 14 failure/subtest sono gli stessi per identità, riga di assertion e diagnostica; confrontati **gli interi log**, normalizzando soltanto la radice dei file (incluso `/private/tmp`) e il tempo di esecuzione. Log normalizzati identici, SHA-256 **ed9f11383b21a7da3d00a09efe87be85fe464ad1817614a288dda88430803d63**. Non si è dedotta la preesistenza dal solo totale. Rieseguito anche dopo la scrittura del verbale: 35 test, 14 failure, 1 skip (0,110 s), diagnostica identica a prima normalizzando il solo tempo.

Identità dei 14 failure, tutti della classe `UnifiedConversationChecks`:

1. `test_condition_c_contract_and_caveats (phrase='non un risultato empiricamente misurato')`
2. `test_one_flow_and_ordered_step_headings`
3. `test_step27_qwen_frozen_results_and_limitations (phrase='0.944444')`
4. `test_step27_qwen_frozen_results_and_limitations (phrase='0.916667')`
5. `test_step27_qwen_frozen_results_and_limitations (phrase='0.833333')`
6. `test_step27_qwen_frozen_results_and_limitations (phrase='zero astensioni')`
7. `test_step27_qwen_frozen_results_and_limitations (phrase='C1–C4: 4/4 PASS')`
8. `test_step27_qwen_frozen_results_and_limitations (phrase='controllo secondario distinto')`
9. `test_step27_qwen_frozen_results_and_limitations (phrase='budget nominale di 1024')`
10. `test_step27_qwen_frozen_results_and_limitations (phrase='36 aggregati B non cappati sono corretti')`
11. `test_step27_qwen_frozen_results_and_limitations`
12. `test_step27_qwen_protocol_stable_facts (doc='html')`
13. `test_step27_qwen_protocol_stable_facts (doc='md')`
14. `test_step27_qwen_protocol_stable_facts`

L'esecuzione del guardiano documentale legge i propri artefatti legacy come previsto dal test richiesto dall'autore: non sono stati usati per addestrare, scegliere iperparametri o confrontare FedAvg. Non è stata svolta un'analisi autonoma dei risultati per-fault del primo studio. Il test non copre questa sotto-fase; la sua stabilità non sostituisce R1/R2.

## Esito e cosa deve cambiare prima dell'OK

**NON OK per R1 e R2**, riprodotti su dati fittizi: mancano la garanzia run→fold e controlli completi dei percorsi prima dell'apertura. Le correzioni richieste sono nel perimetro già verificabile di loader/split, non richiedono dati reali né tuning. Nessun codice o documento dell'esecutore è stato corretto in questa finestra.

Gli esiti positivi restano validi per gli input provati: ricetta, pesi, aggregazione, maschera in inferenza, loss finale finita, apprendimento sintetico, determinismo byte-identico, loader del bundle recuperato e impronte del freeze. Non sono prestazioni reali e non chiudono la sotto-fase.

**Fonti lette:** i quattro documenti obbligatori (mandato specifico letto nella copia di lavoro fornita dall'autore, non presente nel commit oggetto); `Fase_LLM.md`; walkthrough studio2 §0/0.1; piano §6.11/§9 e ricerche mirate correlate; tutti i file del pacchetto FedAvg e relativo diff; PROVENIENZA §10; le sezioni pertinenti e l'impronta del piano 03.8 al commit dichiarato; metadati/storage/manifest 03.6 al commit dichiarato e archivio riscaricato; occorrenze McMahan nel corpus; codice e diagnostiche di `docs/test_explanation.py`. Non lette in blocco la letteratura o le repliche HTML; queste ultime sono state elaborate soltanto dal guardiano documentale. Costo approssimativo di lettura contestuale: **20–30 mila token**, senza conteggiare come lettura semantica i file attraversati solo per hashing.

**Unico file persistente nuovo:** `/Users/luker/fot-tep-verifica-fedavg/studio2/fase03/fedavg/VERIFICA_FEDAVG.md`. Nessun commit, push, merge, tag o aggiornamento del walkthrough.
