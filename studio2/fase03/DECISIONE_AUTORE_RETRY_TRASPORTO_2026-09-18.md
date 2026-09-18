# Decisione d'autore — retry del trasporto non osservato (7.4-FIX-RETRY-RETE)

**Data:** 18 settembre 2026. **Autore:** Luca Sorrentino. Rivede D3 riga 2 per un insieme
chiuso di errori; il resto di D3 è invariato.

## Origine

Il 18 settembre il primo tratto del passaggio 1 si è fermato sullo slot
`test-primary-F3-r06` (`E-LF`, `agent_4`, request `93c15024…`): `APIConnectionError`,
"Server disconnected without sending a response" dopo 3,2 s, nessun byte ricevuto. Con D3
riga 2 lo slot si riprende solo con una prova del gestore del servizio che non siano stati
generati token, e i tempi di quella prova non dipendono da noi.

## Decisione

Un fallimento di trasporto in cui **non è stato ricevuto alcun byte di risposta** —
connessione caduta o rifiutata (`APIConnectionError`), errore del server
(`InternalServerError`, 5xx), `RateLimitError` (429) — si ritenta senza prova fino a **3
volte**, con l'attesa crescente già prevista (30, 60, 120 s) e a carico della quota retry.
Dopo il terzo retry fallito lo slot è un **fallimento tecnico definitivo**: dato mancante,
escluso dall'endpoint primario e dall'aggregatore R=3, riportato a parte (trattamento in
analisi: [Revisione 003](protocollo_finale/REVISIONE_003_TRASPORTO_NON_OSSERVATO.md) §2). Il
batch prosegue. Uno slot abbandonato vale quattro fallimenti consecutivi: il primo fallimento
dello slot successivo porta il contatore a cinque e ferma la campagna, quindi due slot
abbandonati di fila sono impossibili.

Restano invariati: timeout (`APITimeoutError`) → sospensione e riconciliazione; 401/403 e
altri 4xx → STOP; risposta ricevuta ma invalida o troncata → esito definitivo, mai
rigenerata; cambio d'identità → STOP; cinque fallimenti tecnici consecutivi → STOP.

## Motivazioni (per il metodo del paper)

- La regola D3 esisteva perché il retry non diventasse una seconda occasione selettiva per il
  modello. Questo rischio c'è solo se una risposta è stata osservata. Qui nessuno ha visto
  l'esito, quindi reinviare non seleziona nulla.
- Gli eventuali token consumati non hanno costo per lo studio.
- Il timeout è escluso perché correla con generazioni lunghe: ritentarlo favorirebbe le
  risposte brevi.
- Ogni tentativo resta nel ledger (catena `retry_of`, quota `transport`), con tipo d'errore,
  `status_code` e causa sottostante; il numero di retry e di slot abbandonati si riporta nei
  metodi.
- La perdita è MCAR per costruzione (nessun byte ricevuto): escluderla non distorce; contarla
  errata attribuirebbe al modello un guasto di rete. Robustezza: risultati con gli slot
  abbandonati contati come non corretti.
