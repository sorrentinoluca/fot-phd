# Decisione dell'autore sul requisito di approvazione — 03.8

Data della decisione: **2026-09-15**.

## Mandato ricevuto

Luca ha chiarito nella task corrente che la firma materiale non è un requisito
scientifico, editoriale o legale del paper e ha impartito questa istruzione:

> «l’approvazione documentata dell’autore è sufficiente; aggiorna la
> documentazione in merito.»

Il presente record trascrive quella decisione nel repository. Non è una firma e
non attribuisce alla frase un valore diverso da quello di decisione procedurale
dell'autore.

## Regola vigente

Per la chiusura documentale della sotto-fase 03.8:

1. le approvazioni dell'autore già registrate e collegate alle decisioni del
   piano statistico rev.10 costituiscono evidenza sufficiente dell'approvazione;
2. **non è richiesta una sottoscrizione materiale**, né in Markdown né mediante
   firma autografa, scansione, PDF o firma digitale;
3. non deve essere creato o richiesto
   `DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.*`;
4. il pacchetto preparato per la firma e il relativo verbale OK restano
   conservati come record storico del procedimento seguito fino a questa
   decisione, ma le loro istruzioni di sottoscrizione non sono più operative;
5. approvazione, verifica indipendente del presente delta, pubblicazione e
   freeze restano eventi distinti.

La regola sostituisce esclusivamente il residuo procedurale «firma materiale».
Non modifica i byte né il contenuto scientifico del piano rev.10, non riapre A/B,
FAR, U3, D2, D11, margine, alpha, gerarchia o politica R e non cambia i ruoli D9.

## Identità dei record preservati

- piano rev.10 `PIANO_STATISTICO.md`: SHA-256
  `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`;
- manifest storico `PIANO_STATISTICO_FREEZE.json`: SHA-256
  `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`;
- copia firma verificata: SHA-256
  `d470a6ce477f31f85951df8d877d786429a56e2f34a369407ae590494c39f605`;
- verbale sul pacchetto firma: SHA-256
  `37c155fb27d6e7abba6b42ff4af2cc7af6487f15af8967475f1ae46c44417de1`;
- acquisizione del verbale: commit
  `2af85459a14b9d9b567c6a0234154968b4d585d0`.

Questi file restano byte-identici. I riferimenti storici che descrivono la firma
come pendente restano veri per il checkpoint che documentano e non vengono
riscritti retroattivamente.

## Effetti e limiti

Il requisito di approvazione dell'autore è documentato e non richiede ulteriori
azioni personali di Luca. Prima che il nuovo stato possa essere usato per la
chiusura e il freeze, il delta che contiene questo record e i raccordi correnti
deve ricevere una verifica indipendente circoscritta.

Questa decisione non pubblica o congela 03.8, non approva l'ordine label 1a, non
qualifica servizi o configurazioni e non autorizza chiamate, inferenze,
simulazioni, pilot o run finali. 03.8 e Fase 03 restano aperte.
