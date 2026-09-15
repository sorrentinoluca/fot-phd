# Acquisizione dell'OK indipendente — approvazione documentata 03.8

Data: 2026-09-15T16:48:16+02:00.

Copia byte-identica del verbale, senza modificare o estendere il verdetto.

- Fonte: `/tmp/fot-tep-review-038-FQlBQ3/studio2/fase03/piano_statistico/VERIFICA_APPROVAZIONE_DOCUMENTATA_03_8.md`.
- Destinazione: `/Users/luker/fot-tep-allineamenti-038-r1-r4/studio2/fase03/piano_statistico/VERIFICA_APPROVAZIONE_DOCUMENTATA_03_8.md`.
- Dimensione: **5.923 byte**.
- SHA-256: `17cc63875cb1ee1ad6b4e7b9689302c14b84b7cd3135d2701bfbd498a491fa42`.
- Base del delta verificato: `2af85459a14b9d9b567c6a0234154968b4d585d0`.
- Candidato verificato: `270bd2bb0c5f9ff4541d709052cdf144142b1d88`.
- Tree del candidato: `0cf2a5656059fb6d5521062227095c0eeede0f92`.
- Successore già presente prima dell'acquisizione: commit documentale del prompt
  `85a89da150dbd1f818051cc4ad8c0fa843819767`, non coperto dall'OK.
- Successore dell'acquisizione: il commit che contiene il verbale e il presente
  record, distinto dal candidato e non coperto dall'OK; il suo hash è omesso per
  evitare un riferimento autoreferenziale.

## Provenienza e identità

Prima della copia il worktree preparatore
`/Users/luker/fot-tep-allineamenti-038-r1-r4`, branch
`codex/studio2-allineamenti-038-r1-r4`, era pulito a `85a89da`. Il worktree del
revisore era isolato e detached sul candidato esatto `270bd2b`, con tree
coincidente; il verbale era il solo file non tracciato.

La dimensione e lo SHA-256 attesi sono stati verificati sulla fonte prima della
copia e sulla destinazione dopo la copia. `cmp` ha confermato l'identità byte per
byte. Il verbale non è stato normalizzato, corretto o integrato nel testo.

Al preflight `origin/main` e il main del remoto effettivo coincidevano a
`a00605862f627710347bd63c49f79a6d0a00135f`. Nessun worktree parallelo, file
congelato o artefatto storico è stato modificato.

Il verbale identifica il revisore come Codex in una task distinta dalla finestra
preparatrice. Dichiara che il modello disponibile è Codex basato su GPT-5 e che
backend e reasoning effettivi non sono attestabili dal repository; questa
acquisizione non aggiunge attribuzioni ulteriori.

## Portata del verdetto acquisito

Il verbale reca esito **OK** esclusivamente per il delta di sette file
`2af8545..270bd2b`. Conferma che la decisione dell'autore è recepita fedelmente:
per 03.8 l'approvazione documentata è sufficiente e non è richiesta una firma
materiale.

Di conseguenza Luca non deve compilare, firmare o restituire alcuna copia e non
deve essere creato `DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.*`. Il pacchetto
firma verificato e i suoi verbali restano record storici byte-identici; non sono
considerati errati retroattivamente.

Il guardiano registrato dal revisore è **NON PASS**: 35 test, 14 fallimenti
storici e 1 skip, con gli stessi identificativi e sottocasi della base e nessun
peggioramento. `git diff --check`, impronte, link e parità MD/HTML risultano
conformi nel candidato.

L'OK non si estende al prompt `85a89da`, al verbale, alla presente acquisizione o
a byte successivi. Non pubblica e non congela 03.8, non approva l'ordine label
1a, non qualifica servizi o configurazioni e non autorizza chiamate, inferenze,
simulazioni, pilot o run finali. 03.8 e Fase 03 restano aperte.
