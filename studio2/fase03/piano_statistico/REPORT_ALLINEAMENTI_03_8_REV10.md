# Report del candidato di allineamento 03.8 — rev.10

Data: 2026-09-14. Stato: **candidato locale, verifica indipendente pending**.
Non chiude 03.8 o Fase 03 e non autorizza esecuzioni.

## Perimetro e provenienza

Il lavoro parte da `origin/main`
`a00605862f627710347bd63c49f79a6d0a00135f` e acquisisce selettivamente la
catena statistica fino a `51782e8c40069c0a2310afafc36907a61d517ff6`,
senza usare il vecchio ramo come sostituto di main. Preparazione, approvazione
A/B, candidato rev.10 e verbale OK restano quattro passaggi distinti nella nuova
storia. `DELTA_HARNESS_03_10.md`, già pubblicato tramite 03.9, non è stato
riscritto.

Poiché i quattro commit finali presupponevano nove file delle revisioni 7–9 non
presenti nel main, il commit selettivo `70c84e3a573951171813add26a46167cbc6c7203`
li acquisisce dai blob della consegna rev.10. Sono copie byte-identiche; non
ricostruzioni e non nuove revisioni scientifiche. Questo rende risolvibili tutte
le voci del manifest corrente preservando i checkpoint originali registrati al
suo interno.

Sono preservati byte-identici rispetto alla sorgente:

- piano rev.10 `675dbbcc…032a`;
- manifest rev.10 `a69c4f68…f80f8`;
- verbale indipendente rev.10 `d269e26d…b0066`;
- atto non firmato `4a0a4e1f…1cc8`;
- allegato contabile `8d909d8f…3887`;
- specifica 03.10 `e92661fe…355e`.

## Delta predisposto

1. `FoT_TEP_Review_Piano_Sperimentale.md`: stato corrente delle decisioni,
   D2=8, conti 1.728/5.184 e formula completa, assenza del tetto 3.700,
   T3/T4/T5/T6/T9/T11, producer-swap e dipendenze D9. Le tabelle di costo
   precedenti restano etichettate come ricostruzione storica.
2. `APERTURA_SOTTOFASI_FASE03.md`: 03.5/03.9/03.12 aggiornate allo stato
   chiuso/pubblicato/congelato; 03.8 mantenuta aperta; 03.11 collocata dopo il
   freeze per i controlli tecnici OOD; catena del pilot e D9 rese non circolari.
3. Matrice dei residui, istruzioni per la firma e consegna tecnica alla 03.10,
   tutte separate dagli artefatti verificati.

Nessun file della coppia walkthrough MD/HTML è modificato: l'aggiornamento
documentale viene dopo l'OK indipendente del presente delta. Nessun file del
preflight/harness, nessun codice, test o dato è modificato.

## Stato delle dipendenze

La bibliografia non è più un residuo: 23/23 file e i due PNG coincidono con
l'inventario rev.10; il verbale e l'addendum hanno le impronte attese. 03.9 e
03.12 sono riscontrate con i rispettivi tag remoti annotati.

La firma resta materialmente assente. D9 resta esterna e non è scelta. T5,
fattibilità R=3 e controlli OOD sono condizioni operative future nei momenti
specificati, non prove prodotte qui.

## Controlli del preparatore

- manifest rev.10: 19/19 file e 6/6 input coincidono per SHA-256 e dimensione;
- confronto con la consegna `51782e8`: 19/19 file manifestati byte-identici;
- inventario bibliografico sul main corrente: 23/23 file coincidenti;
- manifest del presente delta: 6/6 file coincidenti; JSON valido;
- link locali nei file modificati/nuovi: 6/6 risolti;
- `git diff --check`: pulito;
- guardiano documentale: 35 test, gli stessi 14 fallimenti storici e 1 skip
  (1 `test_condition_c_contract_and_caveats`, 1
  `test_one_flow_and_ordered_step_headings`, 9
  `test_step27_qwen_frozen_results_and_limitations`, 3
  `test_step27_qwen_protocol_stable_facts`).

I 26/26 test statistici e gli altri controlli rev.10 non sono stati rieseguiti:
sono riusati dall'OK indipendente perché tutti i 19 file qualificati coincidono
byte per byte. Nessuna simulazione o rigenerazione della griglia è stata avviata.

## Sequenza residua

Verifica indipendente del candidato → firma/acquisizione (indipendente dagli
allineamenti già preparati) → documentazione di chiusura in coppia MD/HTML →
controlli finali → integrazione e pubblicazione in `origin/main` → manifest/tag
03.8 con prova remota. Ogni correzione normativa dopo la review costituisce un
nuovo candidato e richiede riverifica.
