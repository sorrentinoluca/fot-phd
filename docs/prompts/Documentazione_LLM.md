# Aggiornamento della documentazione — studio 2 FoT-TEP

**Si apre solo dopo l'OK di `Verifica_LLM.md`.** Se la verifica indipendente non è stata fatta, o
si è conclusa con NON OK, questa finestra non si apre: fermati e dillo.

**Leggi prima `Prompt_LLM.md`**. Poi `docs/fot_walkthrough_conversazione_studio2.md` §0 e §2–12,
per sapere quale sezione stai scrivendo e quali fonti valgono.

## Da dove prendi il contenuto

Non erediti il contesto della finestra che ha svolto il lavoro: leggi il **repository**.

1. `studio2/fase<N>/REPORT_FASE<N>.md` — il report di chiusura: è l'**indice**, dice quali file guardare;
2. `studio2/fase<N>/VERIFICA_FASE<N>.md` — il verdetto. Se non c'è, o non dice **OK**, fermati;
3. **i file che il report elenca** — codice, configurazioni, risultati, manifest, log. I numeri della
   sezione vengono da lì, non dal report: il report può contenere un errore di trascrizione.

Se una cifra del report non si ritrova nell'artefatto, **non scriverla**: segnalala.

## Che cosa si aggiorna

**Due documenti, con ruoli diversi.**

1. La **coppia** `docs/fot_walkthrough_conversazione_studio2.md` ↔ `.html`, nella sezione della
   fase conclusa. È il documento lungo, ed è qui che si scrive. Le due forme vanno sempre insieme,
   nella stessa sessione (MAINTENANCE §3).
2. La **sintesi divulgativa** `docs/fot_walkthrough_studio2.html` — solo HTML, non è una coppia.
   Va aggiornata **quando c'è qualcosa da sintetizzare**, cioè quando la fase ha prodotto un
   risultato leggibile da chi non apre il documento lungo. Regole sue:
   - **rimanda e non duplica**: una riga o due su cosa è stato fatto e il link alla sezione lunga.
     Non è una fonte, né per il disegno né per i numeri, e lo dichiara;
   - niente numeri che non siano già nella sezione lunga;
   - se la fase è interna — harness, congelamenti, preparazione — **non si tocca**: una sintesi
     divulgativa di un passaggio tecnico è rumore. Dillo invece di riempirla per completezza.

Alla prima fase che la aggiorna, va **rimosso l'avviso «scheletro al 2026-09-12»** che oggi dice
che non contiene ancora nulla.

Non si aggiorna il piano: il piano è la fonte del **disegno**, il walkthrough racconta l'**esito**.
Se durante la fase una decisione del piano è cambiata, questo va **segnalato**, non riscritto qui.

## Struttura della voce di menù dedicata

Ogni sezione di fase ha questa struttura, nell'ordine, con eventuali sotto-sezioni:

1. **Titolo** — la fase, con il numero di sezione che le spetta secondo §2–12.
2. **Riassunto e sintesi** — cosa è stato fatto e cosa ne è uscito, leggibile da solo. Se questa
   parte non si capisce senza il resto, è scritta male.
3. **Dettaglio** — il come: sotto-fasi eseguite nell'ordine, scelte operative, numeri con il
   riferimento all'artefatto che li contiene.
4. **Connessione alla letteratura** — quali lavori di `letteratura.md` sono pertinenti, e in che
   modo: sostengono la scelta, la delimitano, o vietano un claim. Usa le sigle §14.x.
5. **Eventuali connessioni a critiche** — quali critiche registrate la fase chiude, mitiga o lascia
   aperte. «Mitiga» e «chiude» non sono sinonimi: usa la parola esatta.
6. **Artefatti e riproducibilità** — dove stanno i file, quale manifest, quale commit, quale
   impronta. È la parte che rende la sezione verificabile a mesi di distanza, ed è quella che al
   primo studio è mancata.

## Regole di scrittura

- **Quello che non è dimostrato va scritto come non dimostrato.** Un risultato descrittivo non
  diventa un effetto perché è nella direzione giusta.
- **Niente numeri senza fonte.** Ogni cifra rimanda all'artefatto da cui viene.
- **La letteratura non si copia qui.** Si cita `letteratura.md` per sezione. Se la fase ha
  implicazioni bibliografiche nuove, si aggiornano §14.5 e §14.6 **là**, con `Letteratura_LLM.md`.
- **Se la fase ha riusato dati del primo studio**, la sezione dice quali e in che ruolo, senza
  raccontare il primo studio: configurazione, seed, data di generazione. E dice se l'analisi era
  **pre-specificata** o **post-hoc** (MAINTENANCE §8.2).
- Se una sezione precedente diventa falsa alla luce di questa, **correggila**: due sezioni che si
  contraddicono sono peggio di una sbagliata.

## Chiusura

1. Parità MD/HTML verificata **sul contenuto**, non sul diff.
2. Sintesi divulgativa: aggiornata se la fase lo giustificava, o **dichiarato perché no**.
3. Link risolti; `§0.1` aggiornato se un punto aperto si è chiuso.
4. `python3 docs/test_explanation.py` confrontato con il numero di partenza.
5. Elenco dei file toccati e **decisione se committare** con il messaggio proposto
   (`Commit_LLM.md`).
