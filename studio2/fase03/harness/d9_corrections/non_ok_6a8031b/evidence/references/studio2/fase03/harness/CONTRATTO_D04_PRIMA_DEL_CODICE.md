# D04 — contratto delle decisioni negli stadi aperti

Scritto prima del runtime, dopo le due review indipendenti del tecnico 23859a2.
Claude conferma il nucleo D03 con limiti d’ambiente; Codex conferma D03 e apre D04 P2.

## Invariante

Ogni decisione di binding/ripresa e ogni nuova riserva deve validare gli stessi tentativi
durevoli che consumano le quote, nella stessa transazione della decisione. Il conteggio è
cumulativo fra stadi: non basta controllare la foglia scelta o lo stadio richiesto.
Identità, piano, ruolo base/remediation/retry, catena e prove zero-token devono essere
coerenti prima di autorizzare nuove righe o raggiungere client/server/stub.

`quota_kind` è normativo: una discordanza rispetto a retry_of/stadio invalida l’operazione,
non viene corretta, riclassificata o compensata. Il controllo strutturale dei tentativi è
riusato anche con copertura parziale: non richiede outcome né PASS e non impone la copertura
completa richiesta soltanto in chiusura. Nessuna seconda lista parziale di validazioni.

Restano invariati: 8r+t≤15, sette trasporti senza rinuncia, mai oltre sette nella sonda,
rinuncia incompatibile con remediation, retry gate vietato, massimi 152/160 e hard stop 200.
Snapshot resta una lettura diagnostica delle righe persistite, non un’attestazione di
validità né una fonte che autorizzi il trasporto: su DB deliberatamente corrotto può
mostrare la discordanza. Le decisioni devono rifiutarlo prima di usare quelle quote.

## Prove prima del codice

La matrice deriva da D04_DECISION_CONTRACT.json e dal campo requests.quota_kind già N
in DURABLE_FIELD_CONTRACT.json. Incrocia stadio, ruolo, stato del tentativo e ingresso.
Nuovi stadi/stati o ruoli non censiti devono rendere rossa la guardia del contratto;
nuovi campi restano DA_COPRIRE nel guardiano D03. Non si promette esaustività combinatoria.

- Tutti i ruoli leciti nei cinque stadi, quattro stati durevoli; tre valori quota errati
  per ciascun ruolo; binding/ripresa e nuova riserva, preceduti dal controllo positivo.
- V05/V06 originali byte-identici, ottavo retry senza rinuncia: rifiuto prima di inserimento
  e invio, anche dopo restart. Runner e CLI: client non costruito, server_mock non chiamato,
  zero nuovi invii, database logico/output invariati.
- Triplette: verifica prima della prima riserva e rollback completo; nessun consumo parziale.
- Tentativi di un altro stadio aperto compresi nella validazione cumulativa.
- Campi che determinano il ruolo confrontati con piano e catena; lock con vero scrittore
  concorrente e nuovo guasto dopo una precedente verifica sulla stessa istanza.
- Positivi con rinuncia esplicita, riserve legali e replay restano disponibili.

Il file di test definitivo deve essere rosso sul tecnico 23859a2 e verde sul corretto.
D01/D02/D03, W01–W04, V01–V06, Y/Z/X e applicabili vanno rieseguiti senza indebolimenti.
Nessun cambio al contenuto delle prove D03, ai digest o alla politica legacy/no-backfill.
Il guardiano documentale NON PASS resta non bloccante. Nessun freeze o GO; D9 eseguibile,
ordine label, qualificazioni, T5 e pilot sono separati.
