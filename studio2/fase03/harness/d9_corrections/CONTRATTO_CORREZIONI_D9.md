# Contratto prima del runtime — R-D9-01 e R-D9-02

Mandato corrente: acquisire il NON OK su6a8031b, correggere i due rilievi,
provare gli stessi test finali su respinto e corretto, riconsegnare alla stessa
finestra01a0a579-3fd7-7461-8c26-5449bd3d2b7a. Ruoli e decisioni scientifiche invariati.

R-D9-01: confrontare i sentinel PENDING/UNKNOWN/UNDECIDED dopo strip e upper,
soltanto per la validazione; non normalizzare o riscrivere i documenti acquisiti.
Positivi con metadato reale e rifiuto prima di client, riserva e invio.

R-D9-02: riconfermare i byte del tokenizer canonico R4 **e** del tokenizer/template
chat dello stadio con lo stesso verify_tokenizer usato all'ingresso. Nessuna cache
in memoria sostituisce il controllo. Il binding deve conservare tokenizer_snapshot
assoluto della chat autenticata dal runner, separato da execution_config.d9.r4_snapshot.
I pin chat derivano dal servizio del ruolo dello stadio, quelli R4 dal contratto comune.
Un binding D9 precedente privo del nuovo riferimento resta fail-closed, senza backfill.
Il ledger generico offline senza execution_config conserva il proprio perimetro.

| Decisione | Punto comune di controllo | Effetto da impedire |
| --- | --- | --- |
| Nuovo binding o rebind, aperto/chiuso | validate_binding in transazione del ledger | Inserimento/riuso senza asset recuperabili |
| Nuova riserva, retry, remediation, tripletta | _binding → validate_binding nelle transazioni esistenti D04 | Nuovo intento o consumo con file mancanti/alterati |
| execute_request, resume/export, librerie | binding riacquisito prima della decisione | Invio, journal o rimaterializzazione prima del controllo |
| Producer122B/27B | binding del runner con snapshot effettivo | Confusione fra contatore R4 e contatore chat |
| Sonda/gate122B | binding dal piano autenticato | Riuso di soli path o hash dichiarati |

Non si aggiungono lock sul filesystem del gestore: la verifica assicura i byte
letti al confine della decisione, non l'immutabilità globale contro un writer
esterno che li alteri dopo il controllo. Nessun servizio reale è contattato.
La lettura locale dei file non autentica autonomamente la provenienza dei pesi.

Prove: originali U01–U08 conservati byte-identici; test_d9_corrections finale
con positivi, sentinel con spazi/tab/NBSP, snapshot R4/chat in directory distinte,
file assenti/alterati, riserva diretta e restart, successo→nuovo guasto,
rebind/riuso, execute_request senza trasporto/journal, principale/alternativo.
Il confronto usa lo stesso SHA-256 di test sui due runtime; nessuna assertion
storica viene indebolita. Suite mirata/discovery complete dopo il fix.
Guardiano documentale storico NON PASS, confrontato per identificativi/subtest.
