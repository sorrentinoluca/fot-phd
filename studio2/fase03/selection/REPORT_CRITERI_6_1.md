# Fase 03 — report della sotto-fase criteri di selezione (§6.1)

Data: 2026-09-13. Autore: **Codex, GPT-6**, finestra di lavoro principale.
Profilo: **decisionale**. Perimetro autorizzato: criteri → verifica indipendente →
documentazione → commit → integrazione in `origin/main`. Non è la chiusura della macro-Fase 03.

## 1. Risultati nell'ordine di lavoro

1. **Ricognizione.** `origin/codex/studio2-capability-pilot` termina a `6a02927` e contiene
   **13**, non 12, commit con prefisso `studio2(fase03)` dopo `c6e19d6`. Il checkout iniziale
   era `main`, pulito e allineato a `origin/main`. Il lavoro procede sul nuovo branch
   `codex/studio2-criteri-selezione`, discendente dal pilot, senza riscriverne la storia.
2. **Verifica delle fonti.** Letti piano §§0.1, 2.2, 6.1, D1, passaggi 8.12 e 12.1–12.4,
   contratto e documenti operativi; letti i quattro MD del pilot indicati dall'autore e
   `studio2/PROVENIENZA.md`. Verificate visivamente la tabella 8 e la sua nota in Downs & Vogel,
   e la tabella 2 PHM 2023; letto il commento PHM §4.3. Metadati Yin verificati, testo integrale
   non accessibile: i range del piano restano esplicitamente non riverificati.
3. **Decisione.** Nuovo registro autorevole in `docs/lit_review/`: universo IDV(1)–IDV(15),
   continuità F1/F8/F10/F13, copertura minima 2 step / 2 random / 2 sticking / 1 drift,
   identità della variabile come divieto di duplicazione, almeno due membri dello strato
   nominale H={F3,F9,F15}. La quota per meccanismo è una scelta di progetto resa esplicita,
   non un risultato sperimentale. Quattro posti nuovi; F14/F15 forzati dai vincoli e uno
   solo fra F3/F9. D1 non eseguita.
4. **Correzione necessaria del piano.** Il §12.2 chiedeva FDR <10% in tutti i metodi ma §12.1
   riportava massimi superiori. Rimossa quella definizione incoerente; si usa lo strato
   nominale corroborato dalla PHM, senza nuova soglia numerica. Inserito il riferimento al
   registro in §6.1. Il disegno resta nel piano e nel registro, senza fonte concorrente
   sotto `studio2/`.
5. **Verifica preliminare.** Enumerate 330 quadruple dei soli attributi strutturali: **12
   ammissibili**, 5 con composizione 3/2/1/2 e 7 con 2/3/1/2 nell'ordine step/random/drift/sticking.
   Nessun catalogo selezionato, nessun digest del sorteggio calcolato. Seed, codifica,
   ordinamento e rejection sampling sono prespecificati nel registro per D1.
6. **Consegna alla verifica indipendente.** Il verificatore opera in contesto separato con
   un altro modello autorizzato dall'autore; scrive `VERIFICA_CRITERI_6_1.md`. Solo dopo OK si
   aggiorna il walkthrough, si committa, si attesta il freeze e si integra in `origin/main`.

## 2. File della sotto-fase

- `docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md`: decisione, fonti, limiti,
  divieti, criteri operativi e procedura futura di D1.
- `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`: riferimento in §6.1 e correzione in §12.2.
- `studio2/fase03/selection/FEASIBILITY.json`: conteggio combinatorio, senza catalogo estratto.
- `studio2/fase03/selection/SOURCE_CHECK.json`: URL, dimensioni e impronte dei due PDF
  consultati, più limite di verifica di Yin. Sono fonti esterne accessibili, non dati
  sperimentali da conservare nella release della Fase 02.
- `studio2/fase03/selection/REPORT_CRITERI_6_1.md`: questo report.
- Dopo il riesame: `VERIFICA_CRITERI_6_1.md`, attestazione `CRITERIA_FREEZE.json` e record
  `DELIVERY_CHECK.json`; aggiornamento congiunto della coppia walkthrough Studio 2.

Il freeze deve elencare le impronte del registro, del piano e dei due record di verifica
strutturale/fonti, con il commit che li contiene. Nessun file del pilot deve essere mutato
per effetto di questa sotto-fase. Report e verifica sono specifici di §6.1 per non attribuire
la chiusura a tutto il pilot o alla macro-fase.

## 3. Perimetro, riuso e limiti

Nessun nuovo run, analisi dei nostri risultati per-fault, inferenza modello o selezione D1.
Sono stati letti documenti di contesto che dichiarano il catalogo di continuità e il lavoro
precedente; non si sostiene che la conoscenza storica sia stata cancellata. Le nuove regole non
usano numeri di prestazione, dati o risultati del primo studio. Il suo registro di provenienza
resta invariato; la continuità è attribuita al piano, non trasformata in dati nuovi.

Non sono stati aperti i risultati grezzi della sonda: sono state lette le sue note tecniche.
La lettura dei risultati esterni PHM è consentita dal criterio bibliografico del piano;
il divieto riguarda i risultati dei propri esperimenti. Le identità bibliografiche non
predicono diagnosi, evidence vuota o prestazioni del futuro verbalizzatore.

La nota originale sulle valvole (perturbazioni congiunte e 24–48 ore) è dichiarata nel registro:
non si confonde la copertura nominale col segnale nel nostro disegno. Il rapporto fra quella
raccomandazione e la generazione a singolo fault va esplicitato nella specifica successiva,
prima dei nuovi run, senza selezionare guardando i risultati.

Restano aperti D1, D2, D11, OOD, producer alternativo, dati reali del pilot e gate 40×3.
S1 non è chiuso; non si crea un tag del protocollo sperimentale generale.

## 4. Verifiche e decisione di commit

`python3 docs/test_explanation.py`: **35 test, 14 fallimenti, 1 skipped**, prima e dopo la
stesura dei criteri. I 14 fallimenti sono preesistenti; il test non verifica questa nuova
sotto-fase, perciò servono anche audit delle fonti e verifica combinatoria indipendente.

La modifica è da committare dopo l'OK con messaggio
`studio2(fase03): congela i criteri di selezione prima di D1`.
La coppia walkthrough sarà salvata insieme in un commit di documentazione successivo.
L'autore ha richiesto esplicitamente integrazione in main: dopo le verifiche la consegna
comprende push di `main` e del tag dedicato ai soli criteri. Non si annuncia la chiusura finché
report e verifica non sono raggiungibili da `origin/main`.

## 5. Fonti lette e costo

Lettura mirata dei documenti elencati in §1, istruzioni di manutenzione e prompt del ciclo,
ricerche bibliografiche mirate e due pagine tabellari PDF, oltre al commento PHM. Nessuna lettura
in blocco del corpus o dei dati. Ordine di grandezza: alcune decine di migliaia di token di
contesto documentale; nessun costo d'inferenza scientifica e nessun batch sperimentale.
