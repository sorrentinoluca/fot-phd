# Prompt per una nuova verifica indipendente del delta 03.8

Aprire una **sessione separata con modello diverso dal preparatore Codex GPT-6**;
registrare l'identificativo effettivo del modello e della sessione, senza dedurlo.
Questo file prepara l'incarico e non costituisce un verbale né un OK.

Prima di operare leggere `docs/MAINTENANCE.md`, `docs/prompts/Prompt_LLM.md` e
`Verifica_LLM.md`. Perimetro: sola lettura del candidato; scrivere soltanto il
nuovo verbale nella propria copia. Non correggere i file sottoposti a verifica.

## Oggetto concreto e prerequisiti

Sorgente `/Users/luker/fot-tep-piano-statistico-fix`, branch
`codex/studio2-piano-statistico-fix`; base
`0f1a9bae8b522f614720fa5efe7bd9d2577609ae`, revisione 9.
Pacchetto preparatorio: `studio2/fase03/piano_statistico/REPORT_PREPARAZIONE_CHIUSURA_03_8.md`
e `MANIFEST_PREPARAZIONE_CHIUSURA_03_8.json` nella stessa cartella.
Risolvere il commit che introduce il manifest con `git log -1 --format=%H --
studio2/fase03/piano_statistico/MANIFEST_PREPARAZIONE_CHIUSURA_03_8.json`,
registrarne il SHA completo e confrontare hash e diff; non assumere che HEAD
non sia avanzato. Il manifest non impronta sé stesso: calcolare il suo SHA-256
e registrarlo nel verbale insieme al commit candidato.

**Il pacchetto preparatorio contiene proposte A/B pending e non è una rev. 10.**
Una review adesso può verificare la preparazione, non autorizzare il freeze.
Per la verifica finale richiesta di 03.8, attendere esiti A/B realmente acquisiti
e il candidato di revisione successiva alla 9; registrare esattamente revisione,
commit, manifest e delta rispetto a questa base. Se non esistono, segnalarlo come
pending e non dare un OK di chiusura. Nessuna approvazione dedotta dalla richiesta.

La base rev. 9 ha manifest SHA-256
`2b6ad396307be634428d9355d4aa65144b4956d675ccb9e4b47536e4bdaf8d76`.
Il verbale rev. 9, preservato al commit
`29249a9305c44a44b96e6f49f94e978956ed0ac2`, ha SHA-256
`289a74433d70e2bf911bdea893711ff7a294c75cf74d5e6fa0addbf3ede72a58`.
Il suo OK ristretto non approva A/B o cambiamenti successivi.

## Controlli richiesti

1. Ricostruire fonti e impronte dalla copia esatta, inclusi manifest storico,
   bozza autore, verbali rev. 7/8/9, DESIGN_RESOLUTION JSON/MD, generatore e test.
   Nessuna alterazione dei file protetti, di H, D1, registro o addendum F9–SPE.
2. Separare approvazioni storiche, nuove decisioni con data/riferimento effettivi,
   firma materiale acquisita e condizioni operative. Una riga «Luca» non è firma.
3. Ricalcolare richieste per blocco/modello/R: nucleo 1.728/5.184; swap misura
   224R; ablation 148R; OOD 144R; audit aggiuntivo 346 solo a R=1 (campione finale
   da verificare); E5 R=1 parametrico; FULL riusabile solo sotto tutte le sei
   identità; canary 10/giorno; librerie e conformità non duplicate; retry fuori
   pilot separati dalle riserve già conteggiate. Controllare anche calendario e
   margine 20%, senza assumere prestazioni dal vecchio server o token illimitati.
4. Pilot: ordine conformità→remediation→sonda→gate; una remediation autorizzata
   sul diff, 8r+t≤15, massimi 152/160, hard stop cumulativo 200, nessun reset né
   retry gate; sonda limitata alla quota 7 anche senza remediation e solo per
   triplette complete; timeout senza prova zero token non è difetto prompt; T3 114/120,
   T4 zero, T6 non valutabile per tre invalidi, T11 descrittivo.
5. Se B approvata, verificare congelamento criteri/candidati/catene prima del
   primo run, controlli tecnici 03.11 prima delle chiamate, nessuna scelta su
   prestazioni/separabilità, sostituti verificati individualmente e distinti;
   casi non risolti sospesi. Dimostrare assenza del ciclo 03.8→03.11→03.8.
   Se B non approvata, non dare il ciclo per risolto.
6. Bibliografia: 23 impronte in ACQUISIZIONE_LETTERATURA_03_8.json e verbale OK
   `551f7da9de20096f3a21f6f9a19d2beecd4b03367bbf6cbe4d083f482637ddaf`;
   verificare commit effettivi di acquisizione e conservazione recuperabile dei
   due PNG ignorati. F6 soddisfatta entro PHM non equivale a GO tecnico OOD.
   Nessun vecchio docs/ deve sovrascrivere modifiche correnti.
7. Allineamenti: piano generale D2=8/conteggi/tetto o regola approvata;
   APERTURA ordine corretto; delta 03.10 verificato nel worktree proprietario
   se dichiarato implementato. Non eliminare prerequisiti prima del pilot per
   separarli dalle dipendenze del congelamento statistico. D9 resta esplicita.
8. Eseguire solo i 26 test con `/Users/luker/fot-env/bin/python -m unittest
   studio2.fase03.piano_statistico.test_design_resolution` e i controlli
   documentali. `python3 docs/test_explanation.py`: baseline 35 test,
   14 fallimenti e 1 skip; confrontare identità dei fallimenti. Nessuna griglia
   completa, simulazione TEP, inferenza o apertura di risultati sperimentali.
9. `git diff --check`, validità JSON, impronte, link; per coppie MD/HTML realmente
   toccate, parità sul contenuto. Manifest senza auto-riferimenti; storia delle
   impronte preservata. Non giudicare pubblicato un commit soltanto locale.

## Verbale e consegna

Scrivere `VERIFICA_DELTA_CHIUSURA_03_8.md` nella propria copia, con **OK** o
**NON OK** in prima riga, modello/sessione, commit/manifest esatti e perimetro
(preparazione oppure candidato revisionato). Ogni rilievo deve citare fonte,
esito e conseguenza. Un eventuale OK della sola preparazione lascia pending
nuova revisione, firma e freeze. Non certificare il lavoro dello stesso modello.
Solo dopo l'OK del candidato revisionato, passare a Documentazione_LLM per il
walkthrough in coppia e a Commit_LLM per la consegna seriale. Niente push, merge,
tag o modifica di 03.5; non dichiarare chiusa l'intera Fase 03.
