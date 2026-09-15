# D04 — comandi eseguiti e riproducibilità

Worktree `/Users/luker/fot-tep-harness-0310-d04`.
Output `/Users/luker/fot-tep-harness-0310-d04-checks`.
Python `/opt/anaconda3/bin/python3`, `PYTHONDONTWRITEBYTECODE=1`.
Per riprodurre usare nuovi contenitori sacrificabili; non sovrascrivere i log/fixture conservati.

## Prima del runtime

1. Verificati tredici repository, branch/HEAD/tree/status/worktree e main sul remoto effettivo
   GitHub; il verbale Claude untracked nel source è registrato e preservato per hash.
2. Verificati i tre hash dell’autore, gli 83 membri del manifest tecnico e i 1.929 membri
   del manifest review Codex più il manifest stesso. Acquisite 133 copie; 1.797 file esterni
   con coordinate, impronte, dimensioni e motivazione; Claude acquisito separatamente.
3. Commit acquisizione `f0dca4d2d46a290d2ffeb1840abd46eb7664f0ae`.
4. V01–V06 byte-identici eseguiti in before/evidence contro il clone detached 23859a2:
   6 metodi, 2 failure (V05/V06), zero errori.
5. Contratto, matrice macchina e test D04 scritti/eseguiti prima della prima modifica runtime.
   8 metodi, 240 assertion fallite in sei metodi, zero errori. I sottocasi non sono 240 difetti.
6. Commit test-first `bf7774f2d153ecc50f27ba095f77b612933b4d26`: sei file. Ledger byte-identico
   al respinto; hash in d04_evidence/TEST_FIRST.json. Il file test non è stato poi modificato.

```bash
PYTHONDONTWRITEBYTECODE=1 FOT_HARNESS_TARGET=/Users/luker/fot-tep-riverifica-harness-23859a2-01a0a1ec/candidate FOT_D04_OBSERVATIONS=NUOVO_RED.json /opt/anaconda3/bin/python3 studio2/fase03/harness/test_d04_open_quota.py
PYTHONDONTWRITEBYTECODE=1 FOT_HARNESS_TARGET=/Users/luker/fot-tep-harness-0310-d04 FOT_D04_OBSERVATIONS=NUOVO_GREEN.json /opt/anaconda3/bin/python3 studio2/fase03/harness/test_d04_open_quota.py
```

Passare sempre il target nelle invocazioni dirette. Rosso: 8/240 failure/0 errori;
verde: 8/0/0. Red/green JSON contengono tutte le 216 mutazioni quota e le 14 dipendenze.
I 72 controlli positivi sono eseguiti prima delle varianti negative per stato/ingresso.

## Suite complete

```bash
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest -v studio2.fase03.harness.test_harness_offline studio2.fase03.harness.test_metric_raccordo studio2.fase03.tests.test_execution_guard studio2.fase03.tests.test_protocol studio2.fase03.harness.test_revisions studio2.fase03.harness.test_c01_c03 studio2.fase03.harness.test_d01_replay studio2.fase03.harness.test_d02_predecessors studio2.fase03.harness.test_d03_contract studio2.fase03.harness.test_d04_open_quota
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3 docs/test_explanation.py
```

Mirati e discovery sono due processi indipendenti con log targeted.log/discovery.log.
Includono tutti i D01/D02/D03/D04. Il guardiano è eseguito prima/dopo: confronto degli
identificativi ordinati con la review Codex, non solo conteggio; NON PASS non bloccante.

## Prove indipendenti conservate

before/evidence e after/evidence contengono copie byte-identiche di independent_d03_probes.py;
il sibling candidate punta rispettivamente al respinto e al nuovo worktree. Eseguire
`python CONTENITORE/evidence/independent_d03_probes.py` dal candidato. Il launcher storico
esce zero anche con assertion fallite: leggere JSON/log, non soltanto exit code.

run_extensions.py crea contenitori distinti per W/Y/Z/X e X23 già adattato; copia script
byte-identici dalla review 23859a2 e avvia i processi con log separati. extension_commands.json
registra comandi/cwd/exit code. X23 include anche il sibling extended_probes.py.
Il consolidamento X è 23 letterali + X23 già adattato: la failure letterale obsoleta
rimane nel log e non è cancellata né trasformata in PASS.

Gli applicabili usano RUN_APPLICABLE_ORIGINAL.py storico, negative_probes.py e reference della
prima review, con nuovo sandbox. Quattordici metodi: dodici letterali e due precedenti soli
adattamenti di fixture/argomento. La matrice dei 50 nomi è acquisita byte-identica, N48≡C02;
nessun conteggio di 50/50 letterali e nessuna somma fra suite sovrapposte.

## Matrice generata e perimetro

```bash
/opt/anaconda3/bin/python3 generate_decision_matrix.py --harness-dir /PERCORSO/harness --checks-dir /PERCORSO/NUOVE_PROVE --output-dir /PERCORSO/NUOVA_MATRICE
```

Il generatore usa il contratto e JSON rosso/verde; controlla identità e completezza delle
216 coordinate. Non importa il runtime e non modifica le fixture. La matrice D03 dei campi
rimane quella già verificata indipendentemente; i suoi nove test vengono rieseguiti integralmente.

scope_audit.py confronta 177 file protetti con 97868f9, inclusi i nove test D03 immutati;
compila in memoria 94 Python live. runtime.json registra il turn_context osservato di questa
preparazione, non una review indipendente. Nessuna delega o nuova diversità di modello rivendicata.
Il verbale Claude dichiara il proprio modello/ambiente/limiti: non ne sono disponibili qui i log scratch.

Log unittest e copie originali conservano i propri byte, incluse whitespace finali.
Nessun errore di setup nelle prove nuove. I controlli di whitespace del codice e dei documenti
sono separati dagli originali e dai log acquisiti.

Snapshot su quota deliberatamente manomessa rimane diagnostico: V05/V06 rifiutati conservano
otto intenti/sette retry reali; lo scalare SQL alterato continua a contare sei trasporti.
Non viene riparato, né usato per autorizzare un invio. Nessun cambiamento di quota, rinuncia,
digest D03, legacy/no-backfill, metriche o input scientifici.

Nessun push/merge/tag/freeze/GO, provider reale, inferenza o simulazione scientifica.
D9 eseguibile, ordine label, qualificazioni, T5 e pilot restano separati.

## Correzione della precedenza diagnostica

Le prime suite complete (128 e 163) produssero tre failure: i rifiuti avvenivano ma
superavano la diagnosi attesa del hard stop 200 e del prerequisito alternate. I due metodi
storici sono rimasti immutati. Spostati i rifiuti preliminari prima della validazione
dell’inventario, che rimane obbligatoria prima di ogni decisione positiva. Due metodi
di diagnosi e otto D04 verdi; suite complete e prove indipendenti rieseguite.
Log, fixture e delta intermedi in pre_diagnostic_precedence, senza sostituire le prove finali.
