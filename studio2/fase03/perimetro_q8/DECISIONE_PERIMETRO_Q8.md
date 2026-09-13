# Decisione della sotto-fase 03.4 — perimetro del codice Q8

Data: **2026-09-13**. Decisione dell'autore attuata dopo tre verifiche indipendenti:
`VERIFICA_PERIMETRO_Q8.md` (**NON OK**), `VERIFICA_PERIMETRO_Q8_rev002.md` (**NON OK**) e
`VERIFICA_PERIMETRO_Q8_rev003.md` (**OK**). Branch di attuazione:
`codex/studio2-perimetro-q8`; base dell'attuazione `6d4ddf4`.

## Decisione confermata

1. È adottata l'opzione **(a′)**: nessun nuovo perimetro e nessuna separazione
   harness/artefatto dentro `phase_b/`. Tutto il nuovo codice vive in `studio2/`; `phase_b/` e i
   file del nucleo di `code/` pinnati dal manifest restano congelati.
2. Il riuso è valutato a livello di **funzione**, non di modulo. Prima dell'import si verificano
   dipendenze, effetti del caricamento e SHA-256 del modulo di origine contro
   `studio2/PROVENIENZA.md`. Baseline, finestre, soglie e default ereditati sono passati o
   dichiarati esplicitamente; se un'assunzione non è eliminabile tramite parametri, la funzione si
   riscrive in `studio2/`. Restano vietati gli import da `phase_b/` e i test si riscrivono.
3. La copia byte-identica di `code/tep_features.py` usata nella Fase 02 è registrata tardivamente
   nella riga U2 di `studio2/PROVENIENZA.md`. La marca **pre-specificato** descrive l'uso originario;
   la copia congelata resta intatta come eccezione storica.
4. `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md` viene tracciato in un commit separato. Il file
   distingue le decisioni confermate — perimetro della Fase 03 opzione A e chiusura 03.4 — dalle
   restanti righe, che rimangono una proposta.

## Differenze rispetto alla proposta

- Il testo attuato in `MAINTENANCE.md` §8.2 incorpora la decisione function-level verificata nella
  Revisione 3; `signature_vector` è un esempio interpretativo della proposta e non viene inserito
  nel contratto.
- La tabella previsionale §5.5 della proposta non viene copiata: le sotto-fasi dipendenti leggono
  direttamente §8.2.
- La riga di provenienza aggiunge data e natura tardiva della registrazione, come richiesto
  dall'autore.
- `code/tep_analysis_v2/` **non viene aggiunta ora** alla categoria degli artefatti congelati: la
  copia a HEAD differisce dai tag Phase A e la scelta fra protezione a HEAD e sola copertura dei tag
  resta una decisione dell'autore. Lasciare invariato questo punto non equivale a scegliere una
  delle due alternative.

## File e impronte dell'attuazione

| File | SHA-256 prima | SHA-256 dopo | Modifica |
| --- | --- | --- | --- |
| `docs/MAINTENANCE.md` | `4a75b0677c5eb09d36274cb36be37a1ec73afb2ca86b274cc36193812465647b` | `77b4768c2b6ae1bc27d2e1aaaa56f9c38626add20b2f5e74f6a426eef7a66ec0` | §1 e nuovo capoverso §8.2 |
| `docs/fot_walkthrough_conversazione_studio2.md` | `f9c10c0082aed6ce6ce58c5be7ec74968140528bd6bd120a67cc5dc738e6c0ee` | `d0905e77c931ff326c20f0f4f421a7cccd2c792f99e967d8c64298449467f2ca` | chiusura §0.1, §4.4 e sintesi |
| `docs/fot_walkthrough_conversazione_studio2.html` | `a1bfee09584e8f3d4d2dcbdeb4e7d7e1b5cf3e39eda6245a0fc906916177fb5b` | `524d37d473df2cc747b75eb7a92456746407d3f34c90c3edef98476aa2fc004f` | replica web allineata |
| `studio2/PROVENIENZA.md` | `ce767320179bf722372cfa1deb00bb34354f39fbca71f7b9ee95784fe02e15de` | `950bbfa45ab67b9c60c07049e2ef710518add63bbbc3759780024cbd4bbad334` | riga U2 e motivazione |
| `studio2/fase03/perimetro_q8/DECISIONE_PERIMETRO_Q8.md` | assente | non auto-referenziale | questo registro |
| `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md` | assente dal worktree; copia principale non tracciata `9cceafa0e5094a6318b555025ebe057805dabd6f130c84463769e551ef1b7e2b` | `a56cff1e4080b8762ba7d6a34ec0f7bfabb34a0d874c729256b3cd75e3a583ff` | revisione mirata e tracciamento separato |

La sintesi divulgativa `docs/fot_walkthrough_studio2.html` non viene modificata: 03.4 è una
sotto-fase di processo e non produce un risultato divulgativo autonomo. Nessun tag, push o merge.

## Decisione ancora aperta

L'autore deve scegliere se `code/tep_analysis_v2/` vada protetta **a HEAD**, registrando quello
stato, oppure resti fuori dall'elenco di `MAINTENANCE.md` §1 e coperta soltanto dai tag Phase A.
Restano inoltre di competenza dell'autore l'integrazione del branch e la successiva rimozione del
worktree.
