# FULL = B-LF — le sei identità e come si verificano (gate G4)

Verdetto in prima riga: **NON VERIFICABILE OGGI, PROCEDURA PRONTA.** Le sei identità si
verificano dopo la chiusura del batch finale, sul ledger del target, che sta fuori dal
repository. Lo script di export è `export_full_blf.py`, in **sola lettura**.

FULL non è una condizione nuova: coincide con B-LF **se e solo se** coincidono tutte e sei le
identità di §8.12. Se una sola fallisce, FULL si riesegue (+64 chiamate con un ricevente per
run e R=1, +448 con sette riceventi) e la decisione va presa esplicitamente, non per inerzia.

## Le sei identità e la loro prova documentale

| # | Identità | Prova | Dove si legge |
| --- | --- | --- | --- |
| 1 | **Caso** | `case_id` del lotto test + `neutral_text_sha256` del manifest di evidenza | `evidence/output_test/EVIDENCE_MANIFEST_TEST.csv` |
| 2 | **Ricevente** | `recipient_agent` dentro lo `stable_id` (`block\|condition\|case_id\|recipient_agent\|library_role`) | `RICEVENTI_E5.json` ↔ ledger |
| 3 | **Prompt completo** | `prompt_sha256` di `final_prompts.jsonl` **uguale** al prompt FULL rigenerato dal percorso E5 con mappa identità (byte per byte) | confronto locale, senza chiamate |
| 4 | **Modello e configurazione** | `returned_model` + `system_fingerprint` del record r1 **uguali** al canary E5 del giorno | export + canary E5 |
| 5 | **Decoding** | contratto di generazione del target (seme `20260829`, thinking budget 2048, `max_tokens` 2560) identico nel target E5 | `contract_sha256` dell'identità nel ledger |
| 6 | **Aggregazione** | stessa funzione di scoring del batch applicata a r1 | codice del batch, riusato non riscritto |

## Che cosa l'export **non** può dire

`export_full_blf.py` legge il ledger e nient'altro. Da lì può controllare che tutti gli slot
richiesti ci siano e che portino **un solo** `returned_model` e **un solo**
`system_fingerprint`: è una parte dell'identità 4. Riporta anche `prompt_sha256` e
`contract_sha256`, ma non sa a che cosa debbano essere uguali — il confronto è fuori.

Perciò il suo verdetto si chiama `partial_verdict` e vale `PARTIAL_OK` o `STOP`. **`PARTIAL_OK`
non è il via libera al riuso di FULL.** Le identità 1, 3, 5 e 6, e il completamento della 4 con
il canary del giorno, si verificano con i passi qui sotto; è questa checklist, non l'uscita
dello script, a dire se FULL si riusa.

## Procedura

1. **Export in sola lettura** dal ledger del target finale:

   ```bash
   python3 studio2/fase03/e5/export_full_blf.py \
     --ledger /Users/luker/fot-tep-runtime/<target-finale>/ledger.sqlite3 \
     --recipients studio2/fase03/e5/RICEVENTI_E5.json \
     --out studio2/fase03/e5/FULL_BLF_EXPORT.json
   ```

   Lo script apre il file con URI `mode=ro`, non scrive nulla nel ledger, non contatta
   nessun servizio, e non esporta prompt né testi: identificativi, hash, identità del
   modello, stato e etichetta predetta. Esce con codice 1 (verdetto `STOP`) se trova più di
   un modello, più di un `system_fingerprint`, o uno slot mancante; altrimenti `PARTIAL_OK`.

   **Con la decisione B2** (R=3 con maggioranza 2/3 in sensibilità) il contratto di riuso
   copre tutte e tre le ripetizioni di B-LF, e l'export va fatto su tutte e tre:
   `--repetitions 1 2 3`. Con B1 o B3 resta `--repetitions 1`. Una ripetizione di FULL
   mancante o non conforme fa cadere **la sensibilità**, non il primario su r1.

2. **Identità 3 — prompt byte-identico.** Rigenerare i prompt FULL dal percorso E5 (stesso
   manifest congelato, stessa libreria `G_P`, stesso testo neutrale del lotto test) e
   confrontare gli `prompt_sha256` con quelli di `final_prompts.jsonl`. Il confronto è fra
   hash: non serve rileggere i prompt.

3. **Identità 4 — canary E5.** E5 deve avere il **proprio** canary (gli stessi dieci prompt
   del batch), eseguito nel suo giorno di esecuzione, con STOP immediato se
   `system_fingerprint` o `returned_model` differiscono da quelli dell'export. Questo è il
   punto in cui il riuso di FULL si rompe davvero: se il gestore aggiorna vLLM fra batch ed
   E5, il riuso cade anche se tutto il resto coincide. Per questo E5 va eseguita **subito
   dopo** la chiusura del batch.

4. **Slot mancanti.** Slot ABANDONED (fallimento di trasporto non osservato) o invalidi: la
   regola di coppia è pre-specificata in `DECISIONI_AUTORE_E5.md` §E punto 4 — la **coppia**
   esce dal primario ed è contata a parte con la causa; l'invalido resta *non corretto*, non
   mancante.

5. **Identità 1, 5 e 6.** Caso: `case_id` e `neutral_text_sha256` confrontati con
   `EVIDENCE_MANIFEST_TEST.csv`. Decoding: `contract_sha256` dell'identità nel ledger
   confrontato con il contratto di generazione del target E5 (seme `20260829`, thinking
   budget 2048, `max_tokens` 2560). Aggregazione: la funzione di scoring del batch va
   **riusata**, non riscritta — l'identità 6 si verifica leggendo il codice che E5 importa,
   non confrontando numeri.

6. **Esito.** FULL si riusa se e solo se: `partial_verdict` = `PARTIAL_OK`, le identità 1, 3,
   5 e 6 verificate ai punti sopra, e il canary E5 concorde. Basta una a mancare e FULL si
   riesegue, con decisione esplicita registrata qui. Tabella di spunta da compilare alla
   chiusura:

   | Identità | Verificata da | Esito |
   | --- | --- | --- |
   | 1 caso | confronto con `EVIDENCE_MANIFEST_TEST.csv` | ⬜ |
   | 2 ricevente | `stable_id` dell'export ↔ `RICEVENTI_E5.json` | ⬜ |
   | 3 prompt | `prompt_sha256` ↔ prompt FULL rigenerato | ⬜ |
   | 4 modello/config | export (parziale) + canary E5 del giorno | ⬜ |
   | 5 decoding | `contract_sha256` ↔ contratto del target E5 | ⬜ |
   | 6 aggregazione | funzione di scoring del batch riusata | ⬜ |

## Che cosa questo documento NON fa

Non apre il ledger, non stima esiti, non anticipa accuratezze. L'export produce anche
`predicted_label`: **non va guardato prima del freeze del protocollo E5** — serve alla fase di
analisi, non alla verifica di identità. Se il freeze avviene prima dell'analisi 7.5, come
raccomandato, il problema non si pone.
