# Registro OK indipendente — raccordo metriche 03.9 → 03.10

**AMBITO: OK limitato al solo delta `5116087..caf5bfb`.** Non è un OK dell'intero harness,
non chiude 03.9 né 03.10, non rende efficace alcun freeze e non autorizza chiamate, simulazioni
o analisi sui run finali.

Questo record registra — *dopo* l'implementazione (`caf5bfb`) e la registrazione del candidato
con report/manifest (`1ac06eb`) — l'esito **OK** della verifica indipendente. Non modifica il
verbale, il report né il manifest già improntati: li referenzia per impronta. È un record
successivo e additivo, non un aggiornamento in luogo del manifest pending.

## Delta verificato

- Base del delta: `51160872906feaa63c1fda5e9cf6e0fe8538fb16` (5116087).
- Candidato tecnico verificato: `caf5bfb0ff9b4fc974608f9bc432e0430d90b7ae`.
- Commit successivo (report/manifest, **fuori** dal delta verificato): `1ac06ebdc92f73d3b630ccca9bf75f413bea170b`.
- Sorgente 03.9: `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` (origin/main).
- Ambito diff: 5 file, +484 / −1, `git diff --check` pulito.

## Revisore indipendente

- Modello: Anthropic **Claude Opus 4.8** (identificativo configurato `claude-opus-4-8`),
  prodotto Claude in modalità Cowork (Claude Agent SDK). Livello di reasoning: non esposto.
- Sessione: `session_01WRDU2fmSdMwPx4ovj7npqU`; sandbox `rcw-01wrdu2fmsdmwpx4ovj7npqu`.
  ID task interno non esposto.
- Data: 2026-09-14 18:30 CEST (UTC+02:00), Europe/Rome.
- Copie isolate in sola lettura (finestra proprietaria non toccata):
  - candidato: `/Users/luker/fot-tep/.worktrees/verifica-raccordo-caf5bfb` (detached `caf5bfb`);
  - gemella main 03.9: `/Users/luker/fot-tep/.worktrees/verifica-raccordo-main-c486eee` (detached `c486eee`).
- Verdetto: **OK**, limitato al delta.

## Fonti acquisite in commit separato (byte-identiche)

Acquisite nel commit di acquisizione che precede questo record, con selezione esplicita dei file.

| File | Byte | SHA-256 | Origine |
|---|---:|---|---|
| `VERIFICA_RACCORDO_METRICHE.md` (verbale) | 12487 | `0d90779981871b8c9ceaf2a729f97b371abb7297fb804dc4335ddf0f1bec0e80` | copia isolata del revisore |
| `CONSEGNA_VERIFICA_RACCORDO_METRICHE.md` (consegna revisore) | 8970 | `9c8e01a3d7a3fdeef0f2da48c3813d713334a7b97619ddd803fce6d7ede3f79e` | copia isolata del revisore |
| `CONSEGNA_RACCORDO_METRICHE_03_10.md` (consegna esecutore, prima non tracciata) | 8524 | `3945e9c646e5f1512c0421c823c96c81b9ab06414fdad54b0d57aee4517de9d7` | finestra proprietaria `studio2-harness` |

Verbale: impronta attesa `0d90779981871b8c9ceaf2a729f97b371abb7297fb804dc4335ddf0f1bec0e80`,
**coincidente**; prima riga `VERDETTO: OK`. Sorgente, copia acquisita e blob Git coincidono.

## Artefatti già improntati, preservati byte-identici (non modificati)

- `REPORT_RACCORDO_METRICHE.md` — SHA-256 `8ab3ac62b9fc066259fb00afb1b8d96a6954d8355a4af1e40559d56b7d201c2e` (registrato nel manifest, commit `1ac06eb`).
- `CONTRATTO_RACCORDO_METRICHE.md` — SHA-256 `5c81586f30ddfe8f39f99b313a30e2dad84346821750e93c11f4d5eecc1e7480` (commit `caf5bfb`).
- `METRIC_INTERFACE_CANDIDATE.json` — manifest del candidato; stato `independent_verification: PENDING` **conservato** (non aggiornato in luogo: questo record è il successivo).
- Codice verificato: `metric_adapter.py` `967f998a6ac11f9afed516a154c4923b9e7b1192d4e04932b38d3344db318030`;
  `metrics.py` `97f0427434d3593a87eaf6885e6b997f40ea41be58b011724869358633ef1be7`;
  `test_harness.py` `6fce6bc4b8ac23bbdc97b9d99ae30ec04c6ed6a031b8776b375ab5f7740fd5d7`;
  `SPECIFICA_HARNESS.md` `f50fb290d2aaa89473da4ff10eddb7f275b541bae57cf98bb07328946999890d`.

## Esiti dei test — distinzione revisore / esecutore

Revisore (copia isolata):

- `MetricTests` @`caf5bfb`: **9/9 OK**.
- Suite baseline 03.9 @`c486eee`: **10/10 OK**.
- Suite protocollo/guardie/harness @`caf5bfb`: **34 test, esito OK, skipped=2**.
- Guardiano documentale `docs/test_explanation.py` @`caf5bfb`: **35 test, 14 failure, 1 skip,
  0 errori** (coincide con la baseline nota di MAINTENANCE §5; failure tutti nei walkthrough v1,
  estranei al delta, non convertiti in PASS).
- Equivalenza indipendente `baseline.py::metric` ↔ adapter ↔ `metrics.py::three_numbers`:
  **12.341** configurazioni valid-only (identità degli oggetti numerici) + **10.626** con invalidi
  + tutte le rotture fail-closed dell'adapter e del gate SHA-256: PASS.

**I due skip del revisore** (sandbox senza checkout esterni montati), da tenere distinti:

1. `test_real_0312_adapter_when_checkout_is_available` → **skip** (percorso assoluto
   `/Users/luker/fot-tep-schema-insight/...` non montato nella sandbox di verifica);
2. `test_real_036_release_inventory_when_checkout_is_available` → **skip** (checkout 03.6 non montato).

**Risultato locale dell'esecutore** (finestra proprietaria), da NON confondere con gli skip:
suite protocollo/guardie/harness **34 eseguiti, 33 PASS e 1 errore preesistente** in
`test_real_0312_adapter_when_checkout_is_available`, perché il checkout 03.12 corrente non coincide
più con il vecchio hash pinnato.

**Problema del vecchio pin 03.12: resta APERTO e fuori da questo incarico.** Non convertito in
PASS, non corretto; i pin 03.12 non sono stati toccati. È materia separata di 03.10/03.12.

## Dipendenza normativa (riferimento Git stabile)

La semantica invalidità / astensione / denominatori del raccordo poggia su
`studio2/fase03/piano_statistico/DELTA_HARNESS_03_10.md` della rev. 10 del piano statistico:
commit `6aaa5b3eebfed4ba502c25c0443caabd0051af21` (candidato rev. 10), blob
`780e08ae9e176a819a745ab2054a2e6ae79a8a9a`, contenuto SHA-256
`e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e`. Non importata né modificata
qui; il piano statistico non è stato toccato. Il branch mobile `codex/studio2-piano-statistico-fix`
non è un riferimento stabile e non va usato come tale.

## Cosa questo OK NON attesta

- Non è OK dell'intero harness 03.10 né chiusura di 03.9 / 03.10.
- Non rende efficace `HARNESS_FREEZE.json` (resta la fotografia *pending* del candidato precedente).
- Non integra l'adapter nei run finali; nessun merge, push o tag; nessuna chiamata API,
  simulazione, inferenza o analisi su run finali.
- Restano fuori incarico e da coordinare per l'harness complessivo: D9, endpoint e
  qualificazione/configurazione dei modelli, ordine di presentazione delle label, pin 03.12,
  input completi, piano statistico e autorizzazioni del pilot, oltre a raggiungibilità in
  `origin/main` dei sorgenti 03.6 e tag di freeze della baseline 03.9.
