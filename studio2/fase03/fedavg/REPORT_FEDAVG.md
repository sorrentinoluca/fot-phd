# Report FedAvg — sotto-fase 03.14

## 1. Riassunto e risultati

La sotto-fase ha congelato prima dell’addestramento reale una baseline unica in tre modalità:
pavimento locale, FedAvg canonico e soffitto centralizzato. La ricetta è un MLP
`697 → 32 → 9`, z-score stimato esclusivamente sul fold di training di sviluppo, cross-entropy
con pesi di classe, SGD a learning rate 0,05, batch 32, 5 epoche locali e 40 round, seed
20260914. FedAvg usa tutti gli otto client a ogni round e media i parametri con peso pari alla
numerosità locale. Non esiste early stopping né tuning sul test.

Nel pavimento ogni client vede `Normal` e il proprio fault. I sette logit dei fault assenti sono
mascherati a `−∞` in inferenza: le classi non vengono inventate e un fault altrui è necessariamente
errato. La rete non si astiene; pertanto il secondo dei tre numeri è 0 per costruzione e il terzo
coincide col primo. L’output è una riga per cluster e ricevente per il pavimento, e una riga per
cluster col ricevente `shared` per FedAvg e centralizzato.

Il codice NumPy verifica SHA-256 dei due manifest, SHA-256 di ogni firma, dimensionalità 697,
finitudine, join uno-a-uno con l’indice evaluator-side e percorsi relativi sicuri. Una guardia
fail-closed rifiuta directory con componenti riservate a test o held-out, symlink per manifest,
indice o firme e ogni risoluzione fuori dalla radice del bundle. Ogni `run_id` deve appartenere a
un solo batch; lo split verifica inoltre che l’intersezione dei run fra training e validazione sia
vuota. Il digest dei pesi usa ordine, dtype e byte canonici.

Il loader è stato inoltre esercitato in sola lettura sull’intero bundle fault 03.6: 320/320 firme
verificate, forma `(320, 697)`, 40 cluster e gli otto client attesi. Non è seguito alcun training
reale, perché senza `normal_dev` ciascun client non avrebbe entrambe le classi prespecificate.

Undici test sintetici passano con `numpy==2.3.5`: apprendimento della fixture separabile, caso
nullo inferiore, determinismo, aggregazione pesata, maschera delle sette classi assenti, tre
metriche, verifica delle impronte, guardia contro i dati di test, run non attraversabili fra fold
e regressioni sui symlink di manifest, indice e directory delle firme.

Lo smoke leave-one-batch-out con la ricetta congelata è stato eseguito soltanto sulla fixture,
perché `normal_dev` non è ancora pubblicato. Esito tecnico: 128 campioni di training, 32 di
validazione in 16 cluster; accuratezza aggregata pavimento 0,5625, FedAvg 1,0, centralizzato 1,0;
astensione 0. Una seconda esecuzione ha prodotto tre file byte-identici. Questi numeri dimostrano
solo che il codice apprende un caso costruito e riproducibile: non stimano la prestazione sul TEP
e non sono confrontati col braccio LLM.

### Correzione dopo la prima verifica indipendente

La verifica del commit `b39b723` ha dato **NON OK** su due fixture avversarie: un `run_id` poteva
comparire in batch diversi e un symlink poteva aggirare il confinamento dei percorsi. Il commit
`e5d5a51` chiude entrambi i rilievi senza cambiare ricetta o artefatti dello smoke. Il loader reale
resta 320×697/40 cluster e i tre output dello smoke restano byte-identici. Il freeze rimane non
efficace e richiede una nuova verifica indipendente.

## 2. File toccati

- `studio2/fase03/fedavg/SPECIFICA_FEDAVG.md` — ricetta pre-addestramento, tre modalità, fold e dipendenze.
- `studio2/fase03/fedavg/__init__.py` — interfaccia minima del package.
- `studio2/fase03/fedavg/requirements.txt` — pin `numpy==2.3.5`.
- `studio2/fase03/fedavg/fedavg.py` — loader verificato, MLP, training, aggregazione, valutazione e hash.
- `studio2/fase03/fedavg/smoke_fedavg.py` — smoke LOBO su fixture o, quando disponibili, sui due bundle reali verificati.
- `studio2/fase03/fedavg/test_fedavg.py` — undici test unitari, avversari ed end-to-end.
- `studio2/fase03/fedavg/smoke_fixture/cluster_metrics.csv` — tre metriche per cluster dello smoke sintetico.
- `studio2/fase03/fedavg/smoke_fixture/weight_hashes.json` — digest canonici dei modelli dello smoke.
- `studio2/fase03/fedavg/smoke_fixture/SMOKE_SUMMARY.json` — esito machine-readable dello smoke.
- `studio2/fase03/fedavg/FEDAVG_FREEZE.json` — impronte, dipendenze e stato pending.
- `studio2/fase03/fedavg/REPORT_FEDAVG.md` — questo report.
- `studio2/PROVENIENZA.md` — nuova sezione in coda per firme 03.6 e dipendenze.

Non sono stati modificati piano, walkthrough, `MAINTENANCE.md`, `phase_b/`, `code/`,
`protocol.py`, `run_pilot.py`, `prepare_gate.py` o schemi esistenti.

## 3. Modello e profilo

Codex basato su GPT-5 ha eseguito la specifica con profilo **decisionale breve** e
l’implementazione, i test e lo smoke con profilo **implementativo**. Nessun sottoagente, modello
linguistico esterno, chiamata API o simulazione TEP è stato usato.

## 4. Cosa resta fuori

- smoke LOBO sui dati TEP reali, bloccato dall’assenza del bundle `normal_dev` di 03.9;
- addestramento definitivo e valutazione sui run di test, dopo 03.11;
- bootstrap e confronto appaiato, dopo congelamento/approvazione del piano 03.8 e integrazione 03.10;
- confronto col braccio LLM, esplicitamente escluso da questa finestra;
- verifica indipendente e successiva documentazione nel walkthrough;
- inserimento di McMahan et al. nel corpus: va proposto a una finestra `Letteratura_LLM`.

## 5. Decisioni ancora necessarie

Nessun iperparametro della ricetta richiede una decisione: non è stata aperta una griglia.
Restano decisioni esterne: approvazione e congelamento del piano statistico 03.8; completamento e
pubblicazione di `normal_dev` 03.9; completamento di 03.11. Se il formato finale 03.9/03.10 non
contiene i campi previsti (`agent_id`/client esclusivo, `run_id`, `batch`, label), va aggiunto un
adapter nuovo e verificato senza cambiare la ricetta.

## 6. Verifica documentale

`python3 docs/test_explanation.py` prima delle modifiche: `Ran 35 tests`, **14 failure**, 1 skipped.
Dopo le modifiche: `Ran 35 tests`, **14 failure**, 1 skipped. Il conteggio è invariato e
preesistente; nessun walkthrough è stato modificato. Il test non copre questa sotto-fase.

## 7. Commit

Commit già creati:

- `deed792` — `studio2(fedavg): congela la ricetta minimale`;
- `ab6ee5c` — `studio2(fedavg): implementa le tre modalita e i test`.
- `e5d5a51` — `studio2(fedavg): chiude guardie fold e symlink`.

Decisione: registrare l’aggiornamento di freeze e report con
`studio2(fedavg): registra remediation del NON OK` e sottoporre il nuovo HEAD a riverifica.

### Acquisizione della riverifica indipendente

Acquisito `studio2/fase03/fedavg/VERIFICA_FEDAVG.md`, SHA-256
`57784bf2ff7e8d7d8143bdf7efa29256f44384939a56139b5999f21b0281f11b`, relativo al commit
verificato `d56354934d2b5f88dace3f9b312fcf64ce3cf42b`. Il verificatore dichiara Codex basato su
GPT-6. Il verbale chiude R1 e R2 ed esprime OK esclusivamente per specifica, codice, loader,
test sintetici e smoke su fixture; non attesta training reale, smoke su `normal_dev`, valutazione
finale, confronto con il braccio LLM o congelamento efficace. Il manifest conserva lo stato
precedente alla riverifica: il nuovo verbale documenta l’OK del pacchetto, senza rendere efficace
il freeze e senza chiudere la sotto-fase 03.14.

## Fonti lette e costo

Letti i prompt operativi, `MAINTENANCE.md` §1/§2/§8, walkthrough studio 2 §0–§12, piano §6.11,
§8.5, §9 e D8, `letteratura.md` §14.1/§14.2 per P030/P041/P065 e i due comparatori TEP, il piano
statistico 03.8, gli indici e i manifest 03.6 e il prompt/spec in formazione di 03.9. Costo
approssimativo: 25–35 mila token di documentazione e codice; test e smoke sotto due secondi ciascuno.
