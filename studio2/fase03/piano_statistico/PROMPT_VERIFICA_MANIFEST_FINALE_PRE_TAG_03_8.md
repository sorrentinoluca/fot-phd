# Prompt per la verifica indipendente del manifest finale pre-tag 03.8

Proseguiamo Studio 2 FoT-TEP, Fase 03. Esegui una review indipendente e
read-only del solo manifest finale pre-tag della sottofase 03.8. Non correggere
file, non pubblicare e non creare tag.

Usa una finestra isolata dal preparatore, preferibilmente detached o su un
branch `codex/studio2-*`. Modello suggerito: **gpt-6-astra**, reasoning
**high**. Nel verbale dichiara modello, provider, effort e identità della
sessione realmente usati; non inventare dati non disponibili.

Prima di qualsiasi controllo leggi integralmente `docs/MAINTENANCE.md` nella
versione del candidato e rispettalo. Leggi inoltre:

- `studio2/fase03/piano_statistico/CONSEGNA_MANIFEST_FINALE_PRE_TAG_03_8.md`;
- `studio2/fase03/piano_statistico/MANIFEST_CANDIDATO_FREEZE_03_8.json`;
- `studio2/fase03/piano_statistico/CONSEGNA_PUBBLICAZIONE_03_8.md`;
- `studio2/fase03/piano_statistico/ESITO_PUBBLICAZIONE_03_8.md`;
- `studio2/fase03/piano_statistico/VERIFICA_FINALIZZAZIONE_03_8.md`;
- `studio2/fase03/piano_statistico/ACQUISIZIONE_OK_FINALIZZAZIONE_03_8.md`.

## Identità vincolanti

- Base:
  `a5798c667dedcb85d3b745258fbc992e0c05841a`.
- Candidato:
  `ec807dbaf2cb745ba96d397aac64a981f6fdeb7d`.
- Tree candidato:
  `58ffd0b057dee7c1a1c399aaadd6c256d8658e34`.
- Genitore unico atteso:
  `a5798c667dedcb85d3b745258fbc992e0c05841a`.
- File candidato:
  `studio2/fase03/piano_statistico/MANIFEST_FINALE_PRE_TAG_03_8.json`.
- Dimensione attesa: **14.768 byte**.
- SHA-256 atteso:
  `087d268d438ca6e98063346a5547849a05235a43712aebe56e007c46dcc1413d`.
- Commit pubblicato registrato:
  `8dbd2b49176c16f9e100e5f181c729b99d406a35`, tree
  `d1d2a0bb3b5247190340a9d091452e55099d6a18`.
- Remoto dichiarato: `https://github.com/sorrentinoluca/fot-phd.git`.

La consegna e questo prompt sono successori del candidato e sono esclusi
dall'OK richiesto.

## Perimetro della review

1. Verifica con gli oggetti Git che il candidato esista, abbia il tree e il
   solo genitore dichiarati e che `a5798c6..ec807db` aggiunga esattamente il
   solo manifest, senza altri file.
2. Leggi integralmente il manifest dal blob candidato, valida il JSON e
   ricalcola dimensione e SHA-256.
3. Verifica tutti i **31/31** `boundary_artifacts`: percorsi univoci, file
   presenti nel candidato, dimensioni e SHA-256. Non assumere corretti i valori
   ereditati dal manifest precedente.
4. Verifica che piano rev.10, manifest storico, manifest candidato precedente,
   decisioni, verbali e acquisizioni citati siano byte-identici alle impronte
   registrate. Il nuovo manifest non deve modificare nessuno di questi file.
5. Riscontra con Git la catena e le identità della finalizzazione:
   `6490af4` → `4c9e7a1` → `03a7d76` → `8dbd2b4`, quindi i successori locali
   `39a3e57` → `a5798c6` → `ec807db`. Verifica che il record locale distingua
   chiaramente il commit pubblicato dal proprio commit non pubblicato.
6. Controlla sulla fonte remota effettiva che `refs/heads/main` contenga almeno
   `8dbd2b4` e che tale commit sia raggiungibile. Se il remoto è avanzato dopo
   la preparazione, registra il nuovo valore senza imputarlo automaticamente a
   errore del candidato; è bloccante solo una contraddizione della provenienza
   dichiarata o la mancata raggiungibilità di `8dbd2b4`.
7. Verifica che il tag
   `studio2-fase03-piano-statistico-frozen-001` non sia già presente. Se è
   comparso dopo il candidato, documenta l'evento e non estendere il verdetto a
   quel tag.
8. Controlla che `freeze_effective`, chiusura 03.8 e chiusura Fase 03 siano
   `false`; che commit/tree del candidato interno, target, oggetto e peeled del
   tag siano nulli; che review, acquisizione e pubblicazione del delta pre-tag
   risultino pendenti.
9. Verifica che non esistano auto-impronte o target futuri inventati. Il
   manifest può elencare il proprio percorso solo fra le esclusioni, senza
   dimensione o SHA-256. La sua identità vive nella consegna successiva.
10. Controlla che i cinque checkpoint OK mantengano perimetri distinti e non
    vengano estesi al nuovo manifest. In particolare l'OK di finalizzazione è
    limitato a `6490af4..4c9e7a1` e agli otto file allora verificati.
11. Conferma che firma materiale non richiesta, ordine label 1a, harness D9,
    servizi, T5 e controlli OOD 03.11 restino filoni separati e non diventino
    dipendenze circolari del tag statistico.
12. Esegui `git diff --check`. Il candidato non modifica coppie MD/HTML. Se il
    contratto richiede il guardiano, confronta base e candidato: riporta
    separatamente numero di test, fallimenti storici e skip e non chiamarlo
    PASS in presenza dei 14 fallimenti preesistenti attesi.

Non riaprire audit scientifici rev.10, R1-R4, D9 o decisioni dell'autore. Non
modificare harness, configurazioni, paper, walkthrough o manifest storici. Non
effettuare push, merge, tag, freeze, chiamate ai servizi, inferenze,
simulazioni o pilot.

## Verbale richiesto

Scrivi un solo file nuovo e non tracciato nel worktree del revisore:

`studio2/fase03/piano_statistico/VERIFICA_MANIFEST_FINALE_PRE_TAG_03_8.md`

La prima riga deve essere `**Verdetto: OK.**` oppure
`**Verdetto: NON OK.**`. Il verbale deve riportare:

- base, candidato, tree, genitore e perimetro;
- identità dichiarata della sessione di review;
- controlli 1–12 con prova sintetica;
- dimensione e SHA-256 del verbale calcolati dopo la scrittura;
- eventuali rilievi bloccanti distinti dalle osservazioni non bloccanti;
- conferma che l'esito non pubblica, non congela e non certifica i successori.

Non fare commit del verbale. Consegna percorso assoluto, dimensione, SHA-256 e
stato Git, così che una finestra successiva possa acquisirlo byte-identico.
