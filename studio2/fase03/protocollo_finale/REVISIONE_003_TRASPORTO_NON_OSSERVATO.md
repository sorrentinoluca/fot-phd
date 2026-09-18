# Revisione 003 del protocollo finale — trasporto non osservato e dato mancante

**Decisione dell'autore (Luca), 2026-09-18**, presa durante il passaggio 1 dopo 58 chiamate
scientifiche, su un evento di rete e **senza aver guardato alcun risultato**. Si legge sopra
`PROTOCOLLO_FINALE_CANDIDATE.md`, l'addendum statistico e la
[Revisione 002](REVISIONE_002_NESSUN_LIMITE_DI_GIORNI.md), e prevale solo sui punti sotto.
Revisione **sovrapposta** al target materializzato e approvato sotto
`studio2-fase03-protocollo-finale-frozen-002`: **nessun tag `frozen-003`** e
`materialize_final_target.PROTOCOL_TAG` resta `-002`, perché target, schedule, prompt, pin e quote
non cambiano e l'approvazione li autentica invariati. La revisione entra nella storia con il tag del
runner che la integra (`studio2-fase03-runner-7-4-fix-003`) e va citata nel REPORT e nei metodi.
Tocca la regola di retry (D3 riga 2) e il trattamento del dato mancante in analisi. Dettaglio operativo e motivazioni:
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
diverso: lì il modello ha generato qualcosa, e quello è il suo esito. Lo slot è una **mancanza tecnica non osservata,
trattata come non informativa nell'analisi primaria**: «nessun byte ricevuto» prova che l'esito
non è stato osservato, non che la perdita sia indipendente da durata, carico o risposta latente.
La non-informatività è un'**assunzione dichiarata**, controllata dall'analisi di robustezza sotto
(il timeout, che correla con generazioni lunghe, resta fuori per lo stesso motivo).

- **Endpoint primario (repetition 1):** una coppia fault × posizione con uno slot abbandonato
  è **esclusa** dal contrasto. L'endpoint resta la media uniforme sulle 8 posizioni,
  `Â = (1/8) Σ_p (1/n_p) Σ_{i∈p} X_i` con `n_p` coppie presenti nella posizione `p`; con celle
  mancanti i pesi `w_i = 1/(8 n_p)` non sono uguali, quindi Hoeffding va nella forma pesata,
  `P(|Â − A| ≥ t) ≤ 2 exp(−2 t² / Σ_i w_i²)`, cioè semiampiezza `sqrt(ln(2/α) · Σ w_i² / 2)` con
  `n_eff = 1/Σ w_i²` (64 se nessuna manca; 62,9 con una posizione a 7 coppie). Bootstrap sulle
  coppie presenti, stratificato per posizione. Un trattamento solo: esclusa anche in ogni
  sensibilità.
- **Aggregatore R=3:** una tripletta con uno slot abbandonato è `technical_incomplete_triplet`,
  **esclusa** dall'aggregatore e riportata a parte con la causa. Resta distinta da
  `invalid_incomplete_triplet` (regola Q3), che continua a contare non corretto.
- **Frase sostituita** (candidato §10.4, addendum §5, decisioni Q1–Q3): «le triplette
  incomplete terminali derivano solo da risposte generate e invalide» → «derivano da risposte
  generate e invalide (`invalid_incomplete_triplet`) o da slot abbandonati per trasporto non
  osservato (`technical_incomplete_triplet`); i trasporti non risolti diversi da questi
  continuano a bloccare la chiusura».
- **Analisi di robustezza con esito imputato (metodi):** i risultati con ogni slot abbandonato
  imputato **non corretto** e, separatamente, imputato **corretto**: i due estremi entro cui cade
  qualunque scenario di perdita informativa. In un contrasto fra condizioni l'imputazione non
  corretta non è conservativa in generale (dipende dal braccio in cui manca il dato), per questo
  si riportano entrambi gli estremi. Non è l'endpoint; l'effetto di un singolo slot è dell'ordine
  di un punto percentuale ma dipende dal trattamento e dal braccio.
- **Reporting:** numero di retry per trasporto non osservato, di slot abbandonati per
  condizione, fault, posizione e ripetizione, con i `request_id`.

## Invariato

Tutto il resto di D3 (retry con prova zero-token, `Q` = 400, STOP a 5 consecutivi), §3.3 per
gli invalidi, regola Q3, maschere canary, H1–H3, margine, alpha, pin di Revisione 002.
