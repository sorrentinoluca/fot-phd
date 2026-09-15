OK

# Verifica indipendente dell'approvazione documentata — 03.8

Data: 2026-09-15 (Europe/Rome).

Revisore e finestra: Codex, task distinta dalla finestra preparatrice, in worktree
isolato e detached `/tmp/fot-tep-review-038-FQlBQ3`. Il modello disponibile è
Codex basato su GPT-5; l'identità del backend e il livello di reasoning effettivo
non sono attestabili dal repository.

## Verdetto e motivazioni

Il solo delta `2af85459a14b9d9b567c6a0234154968b4d585d0` →
`270bd2bb0c5f9ff4541d709052cdf144142b1d88` recepisce fedelmente la decisione
procedurale dell'autore del 2026-09-15: per 03.8 l'approvazione documentata è
sufficiente e non è richiesta una sottoscrizione materiale.

La fonte primaria verificata è
`DECISIONE_AUTORE_APPROVAZIONE_DOCUMENTATA_03_8_2026-09-15.md`, che trascrive
letteralmente il mandato dell'autore e ne limita l'effetto alla sostituzione del
residuo procedurale «firma materiale». Il nuovo record esclude espressamente
valore legale, editoriale o scientifico e vieta di richiedere o creare la copia
sottoscritta, una firma autografa, una scansione, un PDF o una firma digitale.

Il delta mantiene distinti approvazione dell'autore, review indipendente del
nuovo delta, documentazione, integrazione/pubblicazione e freeze. La matrice
corrente registra separatamente l'OK D9 già acquisito sul candidato `8a20c12` e
la review ancora pendente per il nuovo raccordo normativo. Né 03.8 né Fase 03
sono dichiarate chiuse.

Ordine label 1a, identità/configurazioni e qualifiche dei servizi, fattibilità,
chiamate, inferenze, simulazioni, pilot e run finali restano non approvati o non
autorizzati. Il delta non riapre né modifica A/B, FAR, U3, D2, D11, margine,
alpha, gerarchia, politica R o ruoli D9. Il piano statistico rev.10 resta
vincolato ai byte già verificati.

Il pacchetto firma e i relativi verbali restano record storici integri. Le loro
istruzioni di sottoscrizione non sono più operative, ma non vengono giudicate
errate retroattivamente e i checkpoint anteriori che indicavano la firma come
pendente conservano il proprio significato storico.

## Perimetro verificato

Il candidato è figlio diretto della base richiesta. Identità riscontrate:

- commit candidato: `270bd2bb0c5f9ff4541d709052cdf144142b1d88`;
- tree candidato: `0cf2a5656059fb6d5521062227095c0eeede0f92`;
- base e unico genitore: `2af85459a14b9d9b567c6a0234154968b4d585d0`;
- delta: esattamente i sette file indicati nel mandato, 120 inserimenti e 35
  cancellazioni; nessuna modifica a harness, configurazioni, paper 03.15 o
  artefatti congelati.

Sono stati letti integralmente, prima dei controlli, `docs/MAINTENANCE.md` del
candidato e le istruzioni FoT-TEP pertinenti. Sono stati esaminati il diff
integrale dei sette file, il nuovo record decisionale, la matrice corrente, il
coordinamento, APERTURA, il raccordo nel piano generale, la coppia walkthrough e
il verbale/inventario del pacchetto firma.

## Prove

`git diff --check 2af85459a14b9d9b567c6a0234154968b4d585d0
270bd2bb0c5f9ff4541d709052cdf144142b1d88` termina con exit 0 e senza output.

Le impronte richieste, ricalcolate sui file del candidato, coincidono:

- `PIANO_STATISTICO.md`:
  `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`;
- `PIANO_STATISTICO_FREEZE.json`:
  `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`;
- `DECISIONI_AUTORE_03_8_COPIA_FIRMA_REV10.md`:
  `d470a6ce477f31f85951df8d877d786429a56e2f34a369407ae590494c39f605`;
- `VERIFICA_PACCHETTO_FIRMA_03_8_REV10.md`:
  `37c155fb27d6e7abba6b42ff4af2cc7af6487f15af8967475f1ae46c44417de1`;
- `DECISIONE_AUTORE_APPROVAZIONE_DOCUMENTATA_03_8_2026-09-15.md`:
  `d5029e7f7a199658577c1b6579fb9d81c78ffba333f7c8c34dd5bc0570b0470e`.

Sono state ricontrollate le 11 voci con percorso, byte e SHA-256
dell'inventario del pacchetto firma, oltre a inventario, istruzioni materiali e
verbale del pacchetto: 14/14 coincidono con le impronte dichiarate e sono
byte-identiche alla base. L'assenza di tali file dal delta conferma inoltre la
preservazione di tutti gli altri artefatti tracciati del pacchetto. Non esiste
una nuova copia `DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.*` nel candidato e il
delta non aggiunge PDF, scansioni o contenitori di firma.

I quattro link relativi aggiunti o ritoccati dal delta risolvono tutti ai file
attesi: il record decisionale dai tre documenti 03.8 e la matrice corrente dal
piano generale. Il solo paragrafo modificato nella coppia walkthrough MD/HTML,
normalizzato rimuovendo markup ed entità HTML, è testualmente identico nei due
formati. Il controllo del guardiano sui link/anchor/markup termina `ok` per il
relativo metodo.

`python3 docs/test_explanation.py` sul candidato termina con exit 1 e va
classificato **NON PASS**: 35 test, 14 fallimenti storici e 1 skip. Il confronto
diretto con la base esatta mostra gli stessi identificativi e sottocasi:

- un sottocaso di `test_condition_c_contract_and_caveats`;
- `test_one_flow_and_ordered_step_headings`;
- otto sottocasi più l'esito aggregato di
  `test_step27_qwen_frozen_results_and_limitations`;
- i sottocasi `doc='html'` e `doc='md'` più l'esito aggregato di
  `test_step27_qwen_protocol_stable_facts`.

Non vi è quindi peggioramento rispetto alla base; la diversa durata stampata
dal runner non è un identificativo o un sottocaso.

## Limiti

La verifica non ripete gli audit scientifici rev.10, R1-R4 o D9 e non riesamina
il merito del pacchetto firma oltre a identità, preservazione e corretta
riclassificazione storica. Non qualifica servizi o configurazioni e non prova
fattibilità, ordine label, chiamate, simulazioni, pilot o run.

Non sono stati eseguiti push, merge, tag, freeze, firme, servizi o esperimenti.
Questo OK vale esclusivamente per il commit `270bd2b` e il tree sopra indicato,
nel perimetro dei sette file; non certifica il prompt di verifica, il presente
verbale, una sua futura acquisizione o byte successivi.
