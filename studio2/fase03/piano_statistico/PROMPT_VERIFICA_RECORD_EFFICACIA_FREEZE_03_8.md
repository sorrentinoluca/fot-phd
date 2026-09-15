# Prompt per la verifica indipendente del record post-tag 03.8

Proseguiamo Studio 2 FoT-TEP, Fase 03. Esegui una review indipendente e
read-only del solo record post-tag di efficacia del piano statistico 03.8. Non
correggere file, non pubblicare e non creare, spostare o sostituire tag.

Usa una finestra isolata dal preparatore, preferibilmente detached o su branch
`codex/studio2-*`. Modello suggerito: **gpt-6-astra**, reasoning **high**. Nel
verbale dichiara identità della sessione, modello, provider ed effort realmente
usati; non inventare dati assenti.

Prima dei controlli leggi integralmente `docs/MAINTENANCE.md` nella versione del
candidato e rispettalo. Leggi inoltre:

- `studio2/fase03/piano_statistico/CONSEGNA_RECORD_EFFICACIA_FREEZE_03_8.md`;
- `studio2/fase03/piano_statistico/PROVA_REMOTA_FREEZE_PIANO_STATISTICO_03_8_2026-09-15.json`;
- `studio2/fase03/piano_statistico/MANIFEST_FINALE_PRE_TAG_03_8.json`;
- `studio2/fase03/piano_statistico/VERIFICA_MANIFEST_FINALE_PRE_TAG_03_8.md`;
- `studio2/fase03/piano_statistico/ACQUISIZIONE_OK_MANIFEST_FINALE_PRE_TAG_03_8.md`.

## Identità vincolanti

- Base:
  `11f504b2bf45a39c1bc4746952f50d58c5022743`.
- Candidato:
  `0b0b2ee2a168d14dc6e46dd8334aebbab311a08e`.
- Tree candidato:
  `f2e6b67a0cc5d4420cbd08fc5c238c9c6860d237`.
- Genitore unico atteso:
  `11f504b2bf45a39c1bc4746952f50d58c5022743`.
- File candidato:
  `studio2/fase03/piano_statistico/PROVA_REMOTA_FREEZE_PIANO_STATISTICO_03_8_2026-09-15.json`.
- Dimensione attesa: **6.773 byte**.
- SHA-256 atteso:
  `2c011bba8b02e3c357cfe62ea90d63f75527d0690186846d5e385e8e79a44f97`.
- Tag:
  `studio2-fase03-piano-statistico-frozen-001`.
- Oggetto tag atteso:
  `bfcf6e5b3840c5b7dc3f7ace1085843d18cfddc7`.
- Target e peeled attesi:
  `11f504b2bf45a39c1bc4746952f50d58c5022743`.
- Remoto: `https://github.com/sorrentinoluca/fot-phd.git`.

La consegna e questo prompt sono successori del candidato e sono esclusi
dall'OK richiesto.

## Controlli richiesti

1. Verifica con gli oggetti Git che base e candidato esistano, che candidato,
   tree e unico genitore coincidano con le identità dichiarate e che il delta
   aggiunga esattamente il solo JSON, senza altri file.
2. Leggi integralmente il record dal blob candidato, valida il JSON e ricalcola
   dimensione e SHA-256.
3. Interroga il remoto effettivo: `refs/heads/main` deve contenere almeno
   `11f504b`; il tag deve restituire l'oggetto `bfcf6e5…ddc7` e il ref `^{}`
   deve restituire `11f504b…2743`. Se main è avanzato, registra il nuovo valore
   e verifica comunque la raggiungibilità del target; non imputare
   automaticamente l'avanzamento al candidato.
4. Verifica dal database Git locale che il ref sia di tipo `tag`, punti a un
   commit, abbia oggetto, target, tree, peeled, tagger, timestamp e messaggio
   identici al record. Confronta oggetto e peeled locali con quelli remoti.
5. Controlla che l'oggetto tag non contenga una firma PGP o SSH. Conferma che i
   metadati Git del tagger non siano presentati come firma materiale.
6. Verifica dai blob al commit taggato percorso, byte e SHA-256 di piano rev.10,
   manifest finale pre-tag, verbale OK e acquisizione, oltre ai due manifest
   storici elencati. Nessuno deve risultare modificato dopo la review o il tag.
7. Verifica la catena `a5798c6` → `ec807db` → `7a42bb6` → `11f504b`, i confini
   dei rispettivi OK e la raggiungibilità del manifest verificato e del verbale
   acquisito dal tag.
8. Verifica che `f944efd2872786d439c22b38302d33e91d08cfab` non sia antenato
   del candidato, di `origin/main` o del target taggato e non compaia nella
   storia candidata.
9. Valuta la semantica degli stati: `freeze_effective=true` descrive l'evento
   remoto già verificato; `record_verified=false`, `record_published=false`,
   chiusura 03.8 false e chiusura Fase 03 false devono impedire una chiusura
   anticipata.
10. Verifica l'assenza di auto-impronte e auto-commit: il record non deve
    contenere il proprio hash o il futuro commit candidato; l'identità è nella
    consegna successiva.
11. Conferma che nessun audit scientifico, decisione A/B/D9, harness, servizio,
    controllo OOD, inferenza, simulazione o pilot sia riaperto o implicato dal
    record.
12. Esegui `git diff --check`. Il delta non modifica coppie MD/HTML. Se applichi
    il guardiano, confronta base e candidato e non chiamarlo PASS in presenza
    dei 14 fallimenti storici attesi; riporta test, fallimenti e skip.

Non modificare manifest verificati, piano o tag. Non effettuare commit, push,
merge, tag, freeze aggiuntivi, firme, chiamate ai servizi, inferenze,
simulazioni o pilot.

## Verbale richiesto

Scrivi un solo file nuovo e non tracciato nel worktree del revisore:

`studio2/fase03/piano_statistico/VERIFICA_RECORD_EFFICACIA_FREEZE_03_8.md`

La prima riga deve essere `**Verdetto: OK.**` oppure
`**Verdetto: NON OK.**`. Riporta:

- base, candidato, tree, genitore e perimetro;
- identità dichiarata della sessione;
- controlli 1–12 con prove sintetiche;
- distinzione fra efficacia del tag, verifica/pubblicazione del record e
  chiusura della sottofase;
- rilievi bloccanti separati dalle osservazioni;
- conferma che il verdetto non modifica o ripubblica il tag.

Non committare il verbale. Consegna percorso assoluto, dimensione, SHA-256 e
stato Git per la successiva acquisizione byte-identica.
