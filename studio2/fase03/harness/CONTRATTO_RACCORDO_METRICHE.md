# Contratto di raccordo metriche 03.9 → 03.10

Data: 2026-09-14. Stato: **implementato, in attesa di verifica indipendente**. Questo contratto
copre soltanto l'adattamento offline delle metriche della baseline numerica; non completa né
congela la 03.9 o la 03.10 e non autorizza chiamate, simulazioni o analisi sui run finali.

## Fonti fissate

La sorgente 03.9 è `origin/main` a
`c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`:

- `baseline.py`, SHA-256
  `b1fe2a83b29b25760dd32df00a2178c5235f714273a194feb6cfe8a12ac74f22`;
- `SPECIFICA_BASELINE_NUMERICA.md`, SHA-256
  `510b119ca54ac05225a7302dcf1b685cb4a778673a0f18d5a9a0e736078a6143`;
- `INTERFACE_CHECK.json`, SHA-256
  `77cf4d8d3620bc739f58f48782e6846345d922463d4d93e34d281ea85d62a4f9`;
- `BASELINE_FREEZE_rev003.json`, SHA-256
  `0312f416dfdbaf8984b2063df2c2e9d00e1737321b9a65dd7e32b0295a937ec8`.

Il destinatario è il contratto della §8 di `SPECIFICA_HARNESS.md` sul branch
`codex/studio2-harness`, partito da `51160872906feaa63c1fda5e9cf6e0fe8538fb16`.

## Semantica e mapping

| 03.9 | 03.10 | Regola |
| --- | --- | --- |
| `accuracy` | `accuracy_all` | `correct / total`; astensioni nel denominatore e non corrette |
| `n` | `total` | numero di righe valutate |
| `abstentions` | `abstained` | sole astensioni valide |
| `non_abstained` | `non_abstained` | preservato dopo la verifica `total - abstained` |
| assente | `invalid` | zero esplicito, soltanto perché 03.9 è valid-only e fallisce sugli input invalidi |

`abstention_rate` e `accuracy_non_abstained` conservano nome e valore. I denominatori sono:

- `accuracy_all = correct / total`;
- `abstention_rate = abstained / total`;
- `accuracy_non_abstained = correct / non_abstained`;
- `non_abstained = total - abstained`, quindi nell'harness generale comprende anche gli
  invalidi, perché un invalido non è un'astensione.

Con denominatore zero il valore è `null`. `correct` richiede una riga valida, non astenuta e con
label predetta uguale alla verità evaluator-side. `abstained` richiede una riga valida con
`abstain=true`. Una riga invalida resta non corretta e non astenuta, anche se il payload grezzo
contiene `abstain=true` o una label apparentemente corretta.

L'assenza del conteggio `invalid` nella 03.9 non è un dato mancante da indovinare: deriva dal suo
contratto, nel quale ogni riga scritta ha `valid=true` e un errore di input arresta la valutazione.
Per questo l'adapter accetta soltanto il formato 03.9 valid-only e produce `invalid=0`. Se la
sorgente espone un campo `invalid`, oppure conteggi o rapporti incoerenti, l'adapter rifiuta il
documento; non converte l'evento in astensione, errore ordinario o predizione valida.

## Punti di produzione, lettura e consumo

La ricognizione del codice trova questi punti effettivi:

1. `baseline_numerica/baseline.py::metric` produce ciascuna foglia 03.9; `evaluate` la usa per
   `summary` e `clusters` e scrive `metrics.json`;
2. `harness/metric_adapter.py::load_baseline_metrics` è l'unico ingresso ammesso per leggere un
   `metrics.json` 03.9 nel namespace 03.10: richiede l'impronta SHA-256 attesa prima di aprirlo;
   `adapt_baseline_metrics_document` visita tutte le foglie di `summary` e `clusters`;
3. `harness/metrics.py::three_numbers` produce nativamente lo stesso contratto 03.10 dalle righe
   del pilot, mentre `endpoint_statistic` ne consuma i tre endpoint per il bootstrap.

Prima di questo delta non esisteva nel codice 03.10 un lettore di `metrics.json` 03.9: era
presente soltanto il confronto documentale in `INTERFACE_CHECK.json`. L'adapter non viene
collegato a run finali in questo incarico.

## Guardie dell'adapter

L'adapter:

- accetta solo schema 03.9 v1, stato tecnico, unità `physical_case_id`,
  `independence_claim=false`, due condizioni e quattro popolazioni previste;
- verifica l'impronta del documento prima della lettura;
- verifica interi non negativi, identità dei conteggi, vincolo `correct <= non_abstained`, valori
  dei tre rapporti e `null` ai denominatori nulli;
- applica il mapping a tutte le foglie di `summary` e `clusters`, verificando anche unicità e
  metadati dei cluster;
- copia i tre valori numerici dalla sorgente dopo la validazione: non li arrotonda, non li
  ricalcola per l'output e non cambia la loro rappresentazione Python;
- aggiunge metadati machine-readable che dichiarano mapping, valid-only e origine di
  `invalid=0`.

## Fuori perimetro

Restano invariati D9, endpoint, configurazione canonica dei modelli, ordine delle label, pin
03.12, piano statistico generale e walkthrough. Il delta non dichiara performance, non apre dati
test, non rende efficace alcun freeze e non costituisce una verifica indipendente.
