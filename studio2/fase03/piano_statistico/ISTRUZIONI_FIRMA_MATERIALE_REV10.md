# Consegna preparatoria per la firma materiale — piano statistico 03.8 rev.10

## Stato e ostacolo concreto

La firma materiale è assente. L'atto originario
`DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md` resta conservato byte-identico
(4.974 byte; SHA-256
`4a0a4e1fc2797ee7a81439110e164d43159c745007136c9dda7bed7759471cc8`),
ma **non va firmato nello stato attuale**: §2 e §3 descrivono ancora D9, review,
allineamenti e bibliografia come pendenti, mentre i successori acquisiti ne
documentano il nuovo stato.

È stata quindi predisposta una proposta corretta separata. Il file esatto da
firmare, **solo dopo un OK indipendente sul suo delta**, è:

`/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/DECISIONI_AUTORE_03_8_COPIA_FIRMA_REV10.md`

- dimensione: **6.585 byte**;
- SHA-256: `d470a6ce477f31f85951df8d877d786429a56e2f34a369407ae590494c39f605`;
- inventario delle fonti: `INVENTARIO_PACCHETTO_FIRMA_03_8_REV10.json`,
  6.622 byte, SHA-256
  `e83420d7d151bac88dea297bc880b8dc1dcde4d3999b61c32b96f76249ce00aa`.

La review deve verificare il confronto completo con l'atto originario, la catena
rev.10/R1–R4/D9 e tutte le impronte dell'inventario. Non deve modificare o firmare
la proposta. Un OK qualifica soltanto questi byte come copia utilizzabile per la
sottoscrizione; non firma, pubblica o congela il piano.

## Istruzioni essenziali per l'autore, dopo l'OK

1. Verificare che la copia presenti esattamente dimensione e SHA-256 indicati.
2. Creare una copia separata, senza sovrascrivere proposta e atto originario.
3. Compilare personalmente soltanto:
   - `Luogo e data effettiva`;
   - `Firma dell'autore` con una firma effettiva. La riga preesistente
     `Autore: Luca` identifica l'autore ma non è una sottoscrizione.
4. Non modificare testo, commit, dimensioni o impronte delle fonti.
5. Restituire normalmente il documento come:

   `/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.md`

Se la modalità materiale scelta produce invece un PDF, una scansione o un
contenitore di firma digitale, conservare la proposta sorgente e restituire
l'artefatto con lo stesso stem `DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10` e la
sua estensione reale; non ricostruirlo artificialmente come Markdown. Il formato
effettivo sarà registrato nel record di acquisizione.

La firma riguarda il piano rev.10 identificato nel documento. Non costituisce
nuova approvazione D9 o dell'ordine label 1a, qualifica dei servizi, fattibilità
T5, esito harness/03.11 o autorizzazione a chiamate, inferenze, simulazioni o
pilot.

## Controlli alla ricezione

- identificare percorso e formato effettivi dell'artefatto ricevuto;
- verificare la provenienza dalla proposta indipendentemente approvata;
- verificare che luogo/data e firma siano presenti e non siano segnaposto o dati
  inseriti dal preparatore;
- per la copia Markdown, confrontare il testo e ammettere differenze soltanto nei
  due campi dell'autore; per un formato firmato diverso, conservare anche la
  proposta sorgente e documentare la trasformazione;
- calcolare dimensione e SHA-256 dell'artefatto firmato;
- acquisire artefatto e record in un commit separato, senza auto-riferimenti;
- confermare che piano, manifest, verbali, acquisizioni e proposta non siano
  stati alterati.

## Residui successivi

Dopo l'acquisizione della firma restano il raccordo documentale applicabile,
l'integrazione/pubblicazione selettiva raggiungibile da `origin/main`, il manifest
finale non autoreferenziale e il tag di freeze. Harness e condizioni operative
restano prerequisiti dei rispettivi stadi; i controlli OOD 03.11 avvengono dopo
il freeze e prima delle chiamate sui test, senza dipendenza circolare.
