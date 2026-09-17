# Contratto di esecuzione e ripresa — rev2, clausola del batch finale 7.4

18 settembre 2026. **Revisione tracciata, non modifica in luogo.**
`CONTRATTO_ESECUZIONE_E_RIPRESA.md` è congelato: `HARNESS_D9_CANDIDATE.json` ne pinna i byte
con SHA-256 `b4e822a300eaf1f1b23c8e76f9043374678ca3bbce84e8efd365167a998d48dc`, e questa
revisione lo lascia **byte-invariato**. Vale per i soli stage del profilo `final_batch`
(`final_batch_r1|r2|r3`, `final_canary`); per ogni stage del pilot il contratto congelato
resta integralmente in vigore, clausole sul journal comprese.

Motivo: rilievo **B3** della review finale `VERIFICA_FINALE_PROTOCOLLO_RUNNER_H3.md`
(SHA `a2fe4b6753cdbac04f0eaddd9902f735adeb0c201bc220d882532ec8f81fba6a`). Il contratto
congelato descrive una proiezione JSONL che il batch finale non scrive; il runner passava a
`execute_request` un journal no-op e costruiva comunque un `journal_path` inutilizzato. Qui la
proiezione effettiva viene nominata, e il codice è stato allineato togliendo il no-op, il
percorso e il commento che descriveva ciò che non avveniva.

## Clausola

**Proiezione durevole degli stage del batch finale.** Gli stage del profilo `final_batch`
non producono la proiezione `{stage}_journal.jsonl` del contratto congelato. La loro
proiezione durevole è, per ogni richiesta e nell'ordine in cui è scritta:

1. **SQLite** — fonte autorevole, invariata: intento prima del trasporto, raw con hash, ora di
   ricezione e latenza al ritorno, valutazione e suo hash prima di proseguire, sospensione per
   identità atomica col record. Nulla di questo cambia.
2. `results/{stage}_call_log.jsonl` — log forense §8.7 (`harness/logging_v1.py`), append-only
   con `fsync` per riga, un `CallRecord` per chiamata ricevuta.
3. `results/{stage}_record_<request_id>.json` — il record valutato della singola richiesta,
   scritto con `durable_write` (scrittura atomica con `fsync`).
4. `results/{stage}_summary.json` — riepilogo di fine tratto, riscritto a ogni tratto.

**Perché.** Il binding di una passata contiene 2.244 specifiche. La proiezione del contratto
congelato viene rigenerata per intero a ogni passo dello stadio: sul batch finale sarebbe
quadratica (≈15 milioni di letture per passata) senza aggiungere stato, perché ogni riga che
conterrebbe è già in SQLite e nei due artefatti per-richiesta qui sopra.

**Cosa resta identico.** Le righe della tabella «Punto del crash / Ripresa esplicita» del
contratto congelato valgono senza eccezioni, perché nessuna di esse dipende dalla proiezione:
la ripresa legge SQLite. In particolare «stadio chiuso, file finale assente → `--resume`
rigenera la proiezione dai record durevoli; nessun nuovo invio» si applica qui a
`{stage}_summary.json`, che `--resume` riscrive dai record durevoli senza alcun invio.
La separazione fra request, response e `transport_invalidity` che il contratto congelato
chiede al journal resta leggibile: le tre entità sono righe distinte del ledger e
`export_journal` continua a esporle per gli stage del pilot e su richiesta esplicita.

**Ambito di `journal_path`.** `runtime.execute_request` accetta `journal_path` opzionale.
Gli ingressi del pilot lo passano sempre e conservano la semantica del contratto congelato;
gli stage del batch finale non lo passano, e in quel caso nessuna proiezione viene scritta —
non un file vuoto, non un no-op silenzioso.

## Verifica

- `shasum -a 256 studio2/fase03/harness/CONTRATTO_ESECUZIONE_E_RIPRESA.md` deve restituire
  `b4e822a300eaf1f1b23c8e76f9043374678ca3bbce84e8efd365167a998d48dc`.
- `grep -rn 'journal' studio2/fase03/run_final_batch.py studio2/fase03/run_final_canary.py`
  non deve restituire nulla.
- `studio2/fase03/harness/test_final_batch.py` copre la ripresa, il resume identico e la
  scrittura del call log per gli stage del batch.
