# Prompt — verifica indipendente del requisito di approvazione 03.8

Modello suggerito: **gpt-6-astra**. Reasoning suggerito: **high**. Usare una
task e un worktree distinti dalla finestra preparatrice.

## Prompt da eseguire

Prosegui lo Studio 2 FoT-TEP, Fase 03, come revisore indipendente del solo delta
che sostituisce il requisito interno di firma materiale della sotto-fase 03.8
con l'approvazione documentata dell'autore.

Prima di qualsiasi controllo leggi integralmente `docs/MAINTENANCE.md` nella
versione del candidato. Lavora in una copia isolata, detached sul candidato; non
scrivere nel worktree preparatore.

Target esatto:

- base: `2af85459a14b9d9b567c6a0234154968b4d585d0`;
- candidato: `270bd2bb0c5f9ff4541d709052cdf144142b1d88`;
- tree candidato: `0cf2a5656059fb6d5521062227095c0eeede0f92`.

Il delta atteso comprende esattamente sette file:

1. `studio2/fase03/piano_statistico/DECISIONE_AUTORE_APPROVAZIONE_DOCUMENTATA_03_8_2026-09-15.md`;
2. `studio2/fase03/piano_statistico/MATRICE_RESIDUI_03_8_DOPO_D9.md`;
3. `studio2/fase03/piano_statistico/COORDINAMENTO_CHIUSURA_03_8.md`;
4. `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md`;
5. `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`;
6. `docs/fot_walkthrough_conversazione_studio2.md`;
7. `docs/fot_walkthrough_conversazione_studio2.html`.

Verifica sulla fonte primaria che il delta recepisca fedelmente la decisione
dell'autore del 2026-09-15: per 03.8 l'approvazione documentata è sufficiente e
non è richiesta una sottoscrizione materiale. Controlla in particolare che:

- non venga attribuito alla decisione valore legale, editoriale o scientifico;
- non venga richiesta o creata una copia sottoscritta, una scansione, un PDF o
  una firma digitale;
- approvazione, review del nuovo delta, pubblicazione e freeze restino distinti;
- 03.8 e Fase 03 restino aperte;
- ordine label 1a, qualifiche dei servizi, chiamate, pilot e run non risultino
  approvati o autorizzati;
- A/B, FAR, U3, D2, D11, margine, alpha, gerarchia, politica R e ruoli D9 non
  vengano riaperti o modificati;
- il pacchetto firma già verificato e i suoi verbali siano conservati come
  record storici, senza considerarli errati retroattivamente;
- il piano statistico rev.10, il manifest e tutti gli artefatti verificati del
  pacchetto firma siano byte-identici alla base;
- la matrice corrente distingua correttamente l'OK D9 già acquisito dal nuovo
  delta ancora sotto review;
- la coppia walkthrough MD/HTML riporti lo stesso contenuto e i nuovi link
  relativi risolvano.

Ricalcola almeno queste impronte preservate:

- `PIANO_STATISTICO.md`:
  `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`;
- `PIANO_STATISTICO_FREEZE.json`:
  `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`;
- `DECISIONI_AUTORE_03_8_COPIA_FIRMA_REV10.md`:
  `d470a6ce477f31f85951df8d877d786429a56e2f34a369407ae590494c39f605`;
- `VERIFICA_PACCHETTO_FIRMA_03_8_REV10.md`:
  `37c155fb27d6e7abba6b42ff4af2cc7af6487f15af8967475f1ae46c44417de1`;
- nuovo record decisionale:
  `d5029e7f7a199658577c1b6579fb9d81c78ffba333f7c8c34dd5bc0570b0470e`.

Esegui `git diff --check`, i controlli dei link pertinenti e
`python3 docs/test_explanation.py`. Il riferimento atteso del guardiano è 35
test, 14 fallimenti storici e 1 skip: non definirlo PASS; il criterio è nessun
peggioramento e stessi identificativi/subtest.

Non ripetere gli audit scientifici rev.10, R1-R4 o D9 e non riesaminare il
merito del pacchetto firma oltre la sua preservazione. Nessuna modifica a
harness, configurazioni, paper 03.15 o artefatti congelati. Nessun push, merge,
tag, freeze, firma, servizio, simulazione o pilot.

Scrivi il verdetto in prima riga (`OK` oppure `NON OK`) e poi motivazioni,
perimetro, prove e limiti in:

`studio2/fase03/piano_statistico/VERIFICA_APPROVAZIONE_DOCUMENTATA_03_8.md`

Lascia il verbale non tracciato nel worktree del revisore e comunica fuori dal
file dimensione e SHA-256 per la successiva acquisizione byte-identica. Un
eventuale OK vale soltanto per `270bd2b` e non per il presente prompt o per byte
successivi.
