# Consegna tecnica alla finestra 03.10 — regole rev.10

Data: 2026-09-14. Questa è una consegna di specifica, non una modifica del
worktree 03.10, un GO o un'autorizzazione al pilot.

## Sorgenti e pin da verificare prima di scrivere

| Fonte | Pin / impronta |
| --- | --- |
| Candidato statistico rev.10 | commit `6aaa5b3eebfed4ba502c25c0443caabd0051af21` |
| Piano rev.10 | `PIANO_STATISTICO.md`, SHA-256 `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a` |
| Regole operative 03.10 | `DELTA_HARNESS_03_10.md`, blob `780e08ae9e176a819a745ab2054a2e6ae79a8a9a`, SHA-256 `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e` |
| Budget completo | `BUDGET_RISORSE_REV10.md`, SHA-256 `8d909d8f851b8b9c633687989d3a9f3221230b48e1f0595278e075556d283887` |
| Verifica rev.10 | `VERIFICA_PIANO_STATISTICO_REV10.md`, SHA-256 `d269e26d8cb4e23370577e1e193d90d9357d66f7c739e9d0669970edf71b0066` |
| Schema insight R4 | tag `studio2-fase03-schema-insight-frozen-001`, peeled `3c64390bc4dd58c48cc4e1e388a38989b32b3143`; manifest storico SHA-256 `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12` |
| Baseline numerica 03.9 | tag `studio2-fase03-baseline-numerica-frozen-001`, peeled `38cb5f5eaa2e5a7dddfd53564a7d020b6b50fa1e` |
| Main remoto osservato | `a00605862f627710347bd63c49f79a6d0a00135f` |

Worktree 03.10 osservato in sola lettura:
`/Users/luker/fot-tep/.worktrees/studio2-harness`, branch
`codex/studio2-harness`, HEAD
`1ac06ebdc92f73d3b630ccca9bf75f413bea170b`, con il solo
`CONSEGNA_RACCORDO_METRICHE_03_10.md` non tracciato. Prima di qualunque intervento
la finestra proprietaria deve ricontrollare HEAD, stato e aggiornamenti concorrenti;
questa consegna non autorizza a rimuovere o inglobare quel file.

## Regole da implementare e verificare nel worktree proprietario

1. Ordine obbligatorio: conformità producer → eventuale unica remediation
   autorizzata sul diff → sonda 3/6/9 per triplette complete → unico gate 40×3.
2. T3: almeno 114/120 valide al primo tentativo e almeno un'astensione parsata
   correttamente per condizione; invalidità sempre nel denominatore.
3. T4: zero troncamenti `length` su 120 chiamate.
4. T6: divergenza solo su coppia parsata (`abstain`, `predicted_label`) o
   validità. Byte, testo, finish reason e JSON accessorio restano forensi. Tre
   risposte non valide rendono il prompt non valutabile e bloccano il GO tecnico.
5. R=3 non è attivato dalla sola assenza di temperatura/seed. Se attivato,
   richiede conteggio completo e T5 con margine temporale 20%; un esito non
   fattibile sospende e rinvia all'autore.
6. T9: 16/16 insight validi in 8 richieste. La remediation riguarda soltanto il
   prompt producer, richiede autorizzazione scritta sul diff e ripete gli stessi
   otto casi; schema, validatore e campi fissi non cambiano.
7. Riserva unica `8r+t≤15`; sonda ripetibile solo per trasporto a zero token
   provato e per triplette complete entro quota 7; nessun retry del gate, nessun
   reset del contatore, nessun uso della quota alternativo. Massimi 152/160,
   hard stop cumulativo 200 non spendibile per differenza.
8. Ledger persistente e atomico condiviso fra stadi, processi, directory e ruoli;
   ogni richiesta inviata conta. Crash/resume non può azzerare o duplicare.
9. T11: senza astensione A local-unseen, OOD resta esplorativa con validità non
   stabilita; non diventa un blocco tecnico automatico.
10. Nessuna libreria o output pre-remediation è riusabile. Riuso successivo solo
    con identità di casi, input, template, schema, modello/configurazione,
    decoding e provenienza.

## Separazione D9

Non selezionare producer, consumer o alternativo. D9 deve fornire identità,
revisioni/quantizzazione, endpoint, tokenizer, configurazione e disponibilità.
Solo dopo si possono allocare le richieste per modello, evitare doppi conteggi se
i ruoli coincidono e misurare latenze/capienza/T5. Il pin R4 dello schema, invece,
è già determinato e va allineato indipendentemente da D9.

Test offline minimi: tutti i casi comportamentali elencati nel file sorgente
`DELTA_HARNESS_03_10.md`, più verifica del pin R4, del ledger concorrente e dei
confini fra T3/T4/T6/T9/T11. Nessuna chiamata o pilot durante l'implementazione.
