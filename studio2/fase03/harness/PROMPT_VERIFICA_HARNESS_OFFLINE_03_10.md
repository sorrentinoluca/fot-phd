# Prompt — verifica indipendente del delta harness offline 03.10

Verifica esclusivamente il candidato
`8185d79e3b744c18e18223bed4d9d349af44747f` (tree
`7c736f8a069821e5971c2a881bf6318bef6e6e48`) contro la base
`a00605862f627710347bd63c49f79a6d0a00135f`. Lavora in copia detached o
worktree isolato e pulito. Non modificare il candidato, non chiamare servizi,
non eseguire inferenze o simulazioni e non aggiornare walkthrough, piano 03.8 o
`APERTURA_SOTTOFASI_FASE03.md`.

## Fonti da leggere

1. `docs/MAINTENANCE.md`, handoff rev02 pubblicato e pubblicazioni successive in
   `main`;
2. `studio2/fase03/piano_statistico/DELTA_HARNESS_03_10.md` al commit
   `6aaa5b3eebfed4ba502c25c0443caabd0051af21`;
3. piano rev.10 e manifest agli SHA-256 dichiarati nel rapporto, più
   `CONSEGNA_REV10.md` nel worktree di consegna;
4. contratto/schema/manifest/pubblicazione R4 al target
   `3c64390bc4dd58c48cc4e1e388a38989b32b3143`;
5. manifest, handoff e pubblicazione finale 03.9;
6. raccordo metriche minimo già qualificato in `main`;
7. package sorgente `/Users/luker/fot-tep/.worktrees/studio2-harness`, branch
   `codex/studio2-harness`, commit
   `1ac06ebdc92f73d3b630ccca9bf75f413bea170b`; se non montato, leggere i blob
   dal repository principale al commit esatto.

Non assumere che codice assente da `main` fosse assente: confrontare il package
sorgente. Non fondere né promuovere in blocco i suoi documenti e freeze.

## Controlli richiesti

### Identità e perimetro

- confermare commit, tree e parent del candidato;
- verificare `HARNESS_OFFLINE_CANDIDATE.json`: 21 hash/dimensioni e SHA-256 del
  manifest `078fcebbbfa03d25936df07a3f73770c1860ba279668985a9356a74c2fe13e9e`;
- verificare che il delta non tocchi `metric_adapter.py`, `metrics.py`,
  `test_metric_raccordo.py`, piano 03.8, APERTURA o walkthrough;
- confrontare i nove moduli recuperati col commit `1ac06eb...` e accertare che
  vecchi freeze/report/manifest non siano stati ripristinati.

### Pin, input e R4

- ricalcolare tutti i pin evidence, pseudolabel, assignment, derangement,
  handoff Normal e R4; controllare tag object e peeled, non il solo nome;
- alterare in copia un byte di validatore/schema/manifest e verificare il rifiuto
  fail-closed;
- verificare 320 casi sviluppo, sedici esempi fault locali, otto Normal, sedici
  contratti fissi e nessun input test/OOD;
- accertare che gli input di conformità non dipendano dalla libreria insight e
  che la libreria resti assente finché non esistono 16/16 output reali R4;
- verificare che ogni coppia prodotta abbia un punto di validazione R4 autonomo.

### Label e D9

- confermare che ordine prompt-facing e `label_space` evaluator-side siano
  separati e che mapping/assignment/derangement 03.7 non cambino;
- verificare rifiuto prima di `author_decision=accepted`, permutazione esatta e
  `Normal` ultimo;
- confermare che `study_model_decision` resti `UNDECIDED`, senza default 27B,
  122B o Terra nel percorso eseguibile;
- trattare `DECISIONE_D9_ORDINE_LABEL_PENDING.md` come proposta da approvare,
  non come decisione già presa.

### Rev.10 e ledger

- verificare persistenza SQLite tra directory/riavvii, intent-before-transport,
  unicità concorrente e conteggio degli intenti irrisolti;
- esercitare l'ordine degli stadi e impedire conformità/remediation/sonda fuori
  sequenza o dopo il gate;
- verificare una sola remediation su diff e approvazione, otto richieste
  complete, nessuna seconda remediation e corretta imputazione di un retry di
  remediation alla quota trasporto;
- verificare `8r+t<=15`, massimo sette trasporti mentre si preserva la
  remediation, waiver esplicito, triplette di sonda atomiche e nessun uso della
  quota del producer alternativo per retry;
- verificare nessun retry automatico, timeout senza prova zero token bloccato,
  gate create-once senza retry, massimi pianificati 152/160 e hard stop 200
  distinto.

### Gate e metriche

- differenze di JSON, testo, finish reason o raw con stessa validità/coppia non
  divergono; validità o coppia diversa sì;
- 114/120 passa la sola soglia numerica T3, 113 no; serve astensione valida in
  ogni condizione;
- un troncamento fallisce T4 separatamente;
- una tripletta mista diverge; tre invalidi rendono T6 non valutabile e non
  concedono GO tecnico;
- R3 resta pending fattibilità e l'evaluatore offline non emette GO finale;
- rieseguire i test del raccordo metriche per dimostrare regressione assente,
  senza trasferirne l'OK all'harness completo.

## Comandi minimi

```text
python3 -m unittest -v \
  studio2.fase03.harness.test_harness_offline \
  studio2.fase03.harness.test_metric_raccordo \
  studio2.fase03.tests.test_execution_guard \
  studio2.fase03.tests.test_protocol

/opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
python3 -m compileall -q studio2/fase03
git diff --check a00605862f627710347bd63c49f79a6d0a00135f..8185d79e3b744c18e18223bed4d9d349af44747f
```

Attesi dal preparatore: 45/45 mirati e 80/80 discovery. Non limitarsi a
confermare questi numeri: ispezionare il contratto e produrre prove negative.

## Consegna del revisore

Produrre un verbale autonomo con:

- identità di candidato/base/tree e copia usata;
- matrice requisito → codice → test/prova;
- hash ricalcolati, comandi ed esiti;
- rilievi con severità e percorso/riga;
- elenco separato di capacità verificate offline e prove server ancora
  necessarie;
- verdetto limitato al delta.

Anche con esito OK, dichiarare esplicitamente: nessun freeze dell'harness,
nessuna approvazione D9/ordine label implicita, nessuna qualifica del servizio,
nessun GO del pilot; 03.10 e Fase 03 restano aperte. Non aggiornare il walkthrough
prima che il verbale sia acquisito e l'eventuale delta corretto sia riverificato.
