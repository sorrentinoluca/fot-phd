# Consegna del candidato di allineamento 03.8 rev.10

Data di preparazione: 2026-09-14

Repository isolato: `/Users/luker/fot-tep-piano-statistico-chiusura`

Branch: `codex/studio2-piano-statistico-chiusura`

## Oggetto immutabile della verifica

- baseline immediata: `70c84e3a573951171813add26a46167cbc6c7203`;
- candidato: `4503cb6f4fbc9942785c7d1fb74b4caf90cb83b8`;
- tree del candidato: `1eb1d7df58e55a546931711f0a1cf9d800e02e3e`;
- `origin/main` osservato alla preparazione:
  `a00605862f627710347bd63c49f79a6d0a00135f`;
- candidato statistico rev.10 preservato:
  `6aaa5b3eebfed4ba502c25c0443caabd0051af21`;
- acquisizione/consegna rev.10 preservata:
  `51782e8c40069c0a2310afafc36907a61d517ff6`.

La verifica deve riguardare esattamente il diff `70c84e3..4503cb6`. Il commit
che contiene questa consegna e il prompt di review è deliberatamente successivo
e non fa parte dell'albero normativo candidato.

## Contenuto del candidato

Il candidato modifica soltanto:

- `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`;
- `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md`.

E aggiunge:

- `studio2/fase03/piano_statistico/MATRICE_RESIDUI_CHIUSURA_03_8_REV10.md`;
- `studio2/fase03/piano_statistico/ISTRUZIONI_FIRMA_MATERIALE_REV10.md`;
- `studio2/fase03/piano_statistico/CONSEGNA_TECNICA_03_10_DA_REV10.md`;
- `studio2/fase03/piano_statistico/REPORT_ALLINEAMENTI_03_8_REV10.md`;
- `studio2/fase03/piano_statistico/MANIFEST_ALLINEAMENTI_03_8_REV10.json`.

Non modifica piano statistico rev.10, manifest rev.10, verbale rev.10, atto da
sottoscrivere, budget, preflight, harness, codice, test, dati o coppie MD/HTML.

## Impronte principali

- piano rev.10: `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`;
- manifest rev.10: `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`;
- verbale rev.10: `d269e26d8cb4e23370577e1e193d90d9357d66f7c739e9d0669970edf71b0066`;
- atto ancora non sottoscritto:
  `4a0a4e1fc2797ee7a81439110e164d43159c745007136c9dda7bed7759471cc8`;
- budget rev.10: `8d909d8f851b8b9c633687989d3a9f3221230b48e1f0595278e075556d283887`;
- consegna tecnica 03.10:
  `44e8be9a3647dcfbef3fa0197647a4c39a597e441bb488de334608dfe9b4aa95`;
- matrice dei residui:
  `2b59150d89f1da74a4f18784a0d0c7f0db191e9364c091cc3d3049e45eb17462`;
- istruzioni di firma:
  `4d3f3e02c9c5acf6867c8d946ef2cb991138f9a16ead95f5d618062e33414970`;
- report degli allineamenti:
  `237950fe9658e171efc6d8ebd020d56a2eaf7fd61a71e1f6115751390b38618c`;
- manifest degli allineamenti:
  `f2bfdd86b9e347da93372c9facadf3fb72f236bf7fc540944094ab37651e4d1f`;
- prompt di verifica indipendente:
  `04401004d2bcc0196725faca22d8c4ff2cc97e2903e833399628bffb0d7a33e5`.

## Firma materiale

L'atto pronto per la firma è:

`/Users/luker/fot-tep-piano-statistico-chiusura/studio2/fase03/piano_statistico/DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md`

Deve restare byte-identico. L'autore deve produrre, personalmente, la copia
separata `DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.md`, compilando luogo, data e
firma/nome verificabile come descritto nelle istruzioni. Nessuna approvazione
precedente vale come sottoscrizione materiale.

## Stato dei residui

Sono già provati e non vanno riaperti: decisioni A/B, D2, D11, margine, alpha,
gerarchia, politica R; acquisizione bibliografica; pubblicazione e freeze di
03.9 e 03.12 R4.

Prima del tag 03.8 restano necessari:

1. sottoscrizione materiale dell'autore e acquisizione verificata della copia;
2. verifica indipendente con esito OK del candidato `4503cb6`;
3. dopo l'OK, allineamento delle coppie documentali applicabili e relativa
   verifica di parità/link;
4. integrazione selettiva nel ramo pubblicabile, senza sostituire `main` con lo
   snapshot storico;
5. manifest finale congelato, documentazione di chiusura, commit raggiungibile
   da `origin/main` e solo allora tag annotato verificato.

D9 resta affidata alla finestra parallela: producer, consumer e alternativo non
sono stati scelti. I relativi pin nominali, T5 e le parti operative dipendenti
restano aperti, ma non impediscono di verificare ora il delta normativo e non
reintroducono il completamento di 03.11 come prerequisito del freeze statistico.

## Verifiche già eseguite dal preparatore

- manifest rev.10: 19/19 file e 6/6 input verificati;
- artefatti rev.10: 19/19 byte-identici alla consegna sorgente;
- inventario bibliografico: 23/23 file e impronte verificati nel `main` corrente;
- manifest del delta: JSON valido, 6/6 impronte, nessun autoriferimento;
- link locali nei file del delta: 6/6 risolti;
- `git diff --check`: pulito;
- guardiano: 35 test, 14 fallimenti e 1 skip, identici alla baseline dichiarata
  con ripartizione 1/1/9/3;
- nessuna coppia MD/HTML e nessun file 03.10 modificati.

Questi controlli non sostituiscono la review indipendente. Il prompt da usare è
`PROMPT_VERIFICA_ALLINEAMENTI_03_8_REV10.md`, raccomandato con `gpt-6-astra` e
reasoning `max` in una task e copia Git indipendenti.

Un eventuale esito OK qualifica soltanto il candidato indicato: non costituisce
firma, pubblicazione, freeze, chiusura di 03.8/Fase 03 né autorizzazione a
simulazioni, API, pilot o run finali.
