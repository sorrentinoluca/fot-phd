# Correzione accounting BatchEncoding 122B — 03.13

Esito: **READY_FOR_RE_REVIEW**. È stato corretto soltanto R1 del verbale indipendente
NON OK, SHA-256
`2b1bad43e206560a71adc9e18cb15077d28c0a0419d6906f89f1f1eaed5cf11f`.
Il precedente record `READY_FOR_INDEPENDENT_REVIEW` resta immutato come storico;
questo rapporto ne è il successore correttivo.

## Test-first e correzione

Il test finale `test_A00_batch_encoding_counts_input_ids_not_mapping_keys`, SHA-256
del file `90ac1bd393a52c6d6d50a7223cb7bee0961488f3b0ad65693ed065080371c52f`,
è stato eseguito con gli stessi byte sui due candidati:

- parent `b83048af49f63657cc91c6ceb519299e6d61567c`: **rosso**, exit 1;
  il conteggio corretto veniva rifiutato come `locale=2` e il valore 2 accettato;
- candidato corretto: **verde**, exit 0.

Ora esiste una sola definizione condivisa di `tokenized_length`, in
`harness/common.py`. `TokenizerAccountingGuard` e `prepare_gate.offline_token_counter`
la riusano entrambi. La funzione accetta una sequenza piatta di ID, un mapping o
`BatchEncoding` con `input_ids` piatti e un singolo batch annidato. Rifiuta input
mancanti, batch multipli, forme ambigue, booleani, ID negativi e tipi non interi.
Il guard conserva il prefisso fail-closed `FATAL_ACCOUNTING_ERROR`.

Non sono stati modificati l'ordine delle validazioni preventive, le quote, il
ledger, i contratti D9 o i cinque JSON privati.

## Verifiche

Con il tokenizer 122B pin-nato, gli otto prompt reali di sviluppo contano
esattamente `1395, 1016, 1385, 1329, 1394, 1066, 1199, 1385` token. I conteggi
corretti sono accettati 8/8 e `usage.prompt_tokens=2` è rifiutato 8/8.

Le regressioni offline direttamente dipendenti sono state eseguite con Python
3.13.9 arm64: **112 test, tutti PASS** nei moduli accounting, protocol,
execution guard, D9, revisions, D9 corrections e harness offline. Un lancio
preliminare con il Python x86_64 di sistema è stato scartato perché una dipendenza
`rpds` installata era arm64; non è contato come verifica del candidato.

La configurazione privata resta byte-identica, SHA-256
`fcf4ec0bb3c77193f3aaaaa5204faf34b7c589ed8c558b4fac54601e1ce58710`;
il suo hash canonico senza authorization resta
`1305c158a98c40cb57e45b43e8d872d3d66e4d6d050d1d167c91b23e0a2fccc8`.
Il ledger reale resta
`02ce8df46d04300b9eb19b0fbc3345c5edd41e7ea17bd1391f22c53f7a6d9d61`
prima e dopo.

Contabilità dell'attività: **zero chiamate provider, zero token generati, zero
nuovi intent, stage o receipt**. Nessun tunnel o authorization è stato creato.
