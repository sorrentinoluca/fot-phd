# Decisione D9 e ordine label — richiesta di approvazione

Data: 2026-09-14. Stato: **pending author decision**. Questo documento formula
una decisione concreta; non è un'approvazione e non cambia la configurazione
canonica.

## Ordine prompt-facing proposto

Approvare la proposta 1a già pubblicata in `SPECIFICA_HARNESS.md`: ordine
deterministico `MHMU4, HEW25, FD3GZ, 3ZGWQ, GSX3L, 4AMS4, TYFPG, QRCCB`, con
`Normal` ultimo, identico per agenti e condizioni. Il calcolo è unico e non si
rifà il sorteggio 03.7. `label_space`, mapping, assignment, owner e derangement
evaluator-side restano byte-invariati. Spearman `-0.38095238095238093` è solo
descrittivo.

Motivo: separa l'ordine visibile dall'ordine di catalogo senza introdurre un
secondo sorteggio né alterare la verità evaluator-side; il renderer è già
parametrico e fail-closed finché manca l'approvazione.

## D9 proposta

Subordinatamente alla qualificazione e al gate della configurazione effettiva:

- `Qwen3.5-122B` assume i ruoli producer e consumer canonici;
- `gpt-5.6-terra` è producer alternativo soltanto nel braccio producer-swap;
- il 27B è fallback solo se il 122B fallisce qualificazione o fattibilità, dopo
  una propria qualificazione e un proprio gate;
- i risultati storici Terra/27B restano descrittivi e non sono aggregati a
  quelli del ruolo canonico.

Motivo: rende esplicita la gerarchia richiesta senza promuovere automaticamente
il modello storico della 03.0 né trasferire qualifica fra modelli, revisioni o
servizi.

## Approvazione richiesta

L'autore deve accettare o correggere separatamente:

1. l'ordine prompt-facing 1a;
2. i ruoli D9 proposti sopra, includendo identità e revisione esatte dei modelli.

Fino ad allora `pilot_preflight.json` mantiene
`"study_model_decision": "UNDECIDED"`, il renderer rifiuta l'ordine e gli
script non scelgono un provider/model default.
