# Verifica indipendente — studio 2 FoT-TEP

**Da eseguire in una finestra diversa da quella che ha svolto il lavoro, e preferibilmente con un
altro modello.** Se la verifica la fa lo stesso modello che ha prodotto il lavoro non è una
verifica: è una rilettura, e tende a confermare.

**Leggi prima `Prompt_LLM.md`** per l'instradamento. **Sola lettura**: nessuna modifica ai file,
nessun commit, nessun tag. Il tuo compito è dire se il lavoro regge, non aggiustarlo.

## Cosa ti viene dato

Il percorso del report di chiusura prodotto da `Fase_LLM.md`, normalmente
`studio2/fase<N>/REPORT_FASE<N>.md`: sotto-fasi eseguite, risultati, file toccati, cosa è rimasto
fuori. **Non fidarti del report.** È l'oggetto della verifica, non la sua fonte: ogni sua
affermazione va risalita alla fonte primaria.

Se il report non esiste come file, fermati e chiedilo: un riassunto incollato a mano non è
verificabile, perché non sai se è ciò che la finestra di lavoro ha effettivamente prodotto.

## Come verificare

1. **Ricostruisci le fonti da zero.** Per ogni affermazione del riassunto, risali al documento o
   all'artefatto che la sostiene e leggilo. Un numero si verifica sull'artefatto, non sul report:
   `AUDIT_GUIDE.md` §5–§13 dice come.
2. **Controlla il perimetro.** Nulla di ciò che MAINTENANCE §1 e §2 dichiarano congelato deve
   risultare modificato, spostato o sovrascritto. Verificalo sui file, non sul racconto.
3. **Controlla le precedenze.** Le fonti usate sono quelle autorevoli secondo
   `docs/fot_walkthrough_conversazione_studio2.md` §0? In particolare: sulla calibrazione delle
   soglie prevale il registro `DECISIONE_calibrazione_soglie_fase_B.md`, non il piano; sui
   descrittori vale §5.1 di `criteri_scelta_descrittori.md` e **non** la §5.5; il piano
   `FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md` non è una fonte.
4. **Dati del primo studio.** Se ne sono stati riusati: sono stati **letti** o ipotizzati? Esiste
   la riga corrispondente in `studio2/PROVENIENZA.md`, con commit e impronta? L'analisi che li usa
   è marcata **pre-specificato** o **post-hoc**, e la marca è corretta?
5. **Sotto-fasi.** Sono state eseguite nell'ordine dichiarato? Ci sono decisioni prese in anticipo
   su sotto-fasi successive — cioè scelte che a quel punto non erano ancora lavorabili?
6. **Coppie e conteggi.** Ogni coppia MD/HTML toccata è allineata **sul contenuto**: stesse
   sezioni, stesso ordine, stessi numeri. I totali dichiarati coincidono con le righe effettive.
7. **Test.** Riesegui `python3 docs/test_explanation.py` e confronta con il numero dichiarato.

## Come rispondere

Non dare un giudizio complessivo prima dei dettagli. Per **ogni** punto:

| Esito | Significato |
| :---: | --- |
| ✅ | verificato sulla fonte primaria, che indichi |
| ⚠️ | plausibile ma non verificabile con ciò che hai — di' cosa manca |
| ❌ | smentito dalla fonte: cita la fonte e la formulazione corretta |

Poi, e solo poi, **una delle due conclusioni**:

- **OK** — il lavoro regge e si può procedere all'aggiornamento della documentazione;
- **NON OK** — con l'elenco puntuale di cosa va corretto prima.

**Scrivi l'esito in un file**: `studio2/fase<N>/VERIFICA_FASE<N>.md`, con il verdetto in prima
riga, i punti verificati con i loro esiti, e quale modello e finestra hanno svolto la verifica.
È ciò che la finestra di documentazione legge, e ciò che resta come traccia dell'indipendenza.
In chat lascia il percorso e il verdetto.

**Non dire OK per cortesia.** Un ❌ trovato adesso costa un'ora; trovato in review costa il paper.
Se non hai potuto verificare qualcosa, la risposta corretta è ⚠️ con il motivo, non ✅.
