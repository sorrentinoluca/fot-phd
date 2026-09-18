# Revisione 003 del protocollo finale — trasporto non osservato e dato mancante

**Decisione dell'autore (Luca), 2026-09-18**, presa durante il passaggio 1 dopo 58 chiamate
scientifiche, su un evento di rete e **senza aver guardato alcun risultato**. Si legge sopra
`PROTOCOLLO_FINALE_CANDIDATE.md`, l'addendum statistico e la
[Revisione 002](REVISIONE_002_NESSUN_LIMITE_DI_GIORNI.md), e prevale solo sui punti sotto.
Tag previsto: `studio2-fase03-protocollo-finale-frozen-003`. Target, schedule, prompt e pin
non cambiano: la revisione tocca la regola di retry (D3 riga 2) e il trattamento del dato
mancante in analisi. Dettaglio operativo e motivazioni:
[`DECISIONE_AUTORE_RETRY_TRASPORTO_2026-09-18.md`](../DECISIONE_AUTORE_RETRY_TRASPORTO_2026-09-18.md).

## 1. Esecuzione (sostituisce D3 riga 2 per un insieme chiuso)

Connessione caduta o rifiutata, 5xx, 429 **senza alcun byte di risposta ricevuto** → retry
senza prova fino a 3 volte (30/60/120 s, quota `Q` = 400). Dopo il terzo retry fallito lo slot
è `ABANDONED`: fallimento tecnico definitivo, dato mancante. Timeout, 401/403, altri 4xx,
risposte ricevute (valide, invalide o troncate), cambio d'identità: invariati.

Conseguenza del contatore D3 (invariato): uno slot abbandonato vale quattro fallimenti tecnici
consecutivi, quindi il primo fallimento dello slot successivo raggiunge cinque e ferma la
campagna. Due slot abbandonati di fila sono impossibili: una perdita che si ripete è trattata
come servizio indisponibile, non come dato mancante.

## 2. Analisi: lo slot abbandonato è escluso, non errato

Premessa: l'esito dello slot non è stato osservato da nessuno e non dice nulla sul modello.
Contarlo «non corretto» attribuirebbe al modello un guasto di rete. L'invalido di §3.3 è
diverso: lì il modello ha generato qualcosa, e quello è il suo esito. La perdita è **MCAR per
costruzione**: la connessione cade prima di qualunque byte, quindi non può dipendere dalla
risposta (per questo il timeout, che correla con generazioni lunghe, resta fuori).

- **Endpoint primario (repetition 1):** una coppia fault × posizione con uno slot abbandonato
  è **esclusa** dal contrasto. La media uniforme sulle 8 posizioni si calcola sulle celle
  presenti (una posizione può averne 7); Hoeffding usa l'`n` effettivo
  (`sqrt(2*ln(2/0,05)/n)`), bootstrap sulle coppie presenti. Un trattamento solo: esclusa
  anche in ogni sensibilità.
- **Aggregatore R=3:** una tripletta con uno slot abbandonato è `technical_incomplete_triplet`,
  **esclusa** dall'aggregatore e riportata a parte con la causa. Resta distinta da
  `invalid_incomplete_triplet` (regola Q3), che continua a contare non corretto.
- **Frase sostituita** (candidato §10.4, addendum §5, decisioni Q1–Q3): «le triplette
  incomplete terminali derivano solo da risposte generate e invalide» → «derivano da risposte
  generate e invalide (`invalid_incomplete_triplet`) o da slot abbandonati per trasporto non
  osservato (`technical_incomplete_triplet`); i trasporti non risolti diversi da questi
  continuano a bloccare la chiusura».
- **Robustezza (metodi):** «come analisi di robustezza, i risultati con gli slot abbandonati
  contati come non corretti». Non è l'endpoint; fornisce il limite conservativo. Con 64 coppie
  ogni slot sposta il contrasto di al più 1/64 ≈ 1,6 punti percentuali.
- **Reporting:** numero di retry per trasporto non osservato, di slot abbandonati per
  condizione, fault, posizione e ripetizione, con i `request_id`.

## Invariato

Tutto il resto di D3 (retry con prova zero-token, `Q` = 400, STOP a 5 consecutivi), §3.3 per
gli invalidi, regola Q3, maschere canary, H1–H3, margine, alpha, pin di Revisione 002.
