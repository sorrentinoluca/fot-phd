# Fase 03 — stato dell'implementazione

Questo file registra il codice già predisposto oltre la ricognizione 03.0. Non è un report di
chiusura della fase e non autorizza chiamate al modello.

| Componente | Stato | Può essere eseguito ora? |
| --- | --- | --- |
| Schemi insight, output diagnostico e manifest del pilot | implementati e validati offline | sì, solo validazione |
| Validatore libreria 16 insight / 14 peer | implementato e testato su fixture sintetiche | sì, solo offline |
| Controllo E-LF: cambia solo `pseudolabel` | implementato e testato | sì, solo offline |
| Renderer A/B-LF/E-LF | implementato e testato su fixture sintetiche | sì, solo offline |
| Selezione 40 prompt | implementata, ma richiede catalogo e sviluppo reali | no |
| Conteggio token col tokenizer locale | implementato | sì, su fixture sintetiche dichiarate |
| Sonda di capienza e budget di generazione | implementata | **sospesa** |
| Freeze della configurazione prima del gate | implementato | **sospeso** |
| Gate di stabilità 40×3 | implementato con guardie fail-closed | **sospeso** |
| Logging modello/request/fingerprint/hash/latency/token | implementato | **sospeso** |
| Sonda producer Qwen e producer alternativo | implementata | **sospesa** |

## Separazione delle dipendenze

**Da sincronizzare perché già esistenti:** report della Fase 02 e soli artefatti che esso dichiara
conclusi; snapshot/runtime Qwen locale; fonti congelate del primo studio elencate in
`studio2/PROVENIENZA.md`.

**Ancora da realizzare scientificamente:** catalogo definitivo, 40 run fault di sviluppo,
feature/evidence/verbalizzazioni associate e manifest autonomo dei veri input del pilot. Questa
finestra non seleziona fault, non genera dati e non crea surrogati da promuovere a input reali.

## Fixture sintetiche

Le fixture di `synthetic_fixture.py` hanno `status=SYNTHETIC_OFFLINE_FIXTURE`,
`provenance_kind=synthetic_offline_only` e un catalogo esplicitamente non scientifico. Il
preparatore esecutivo le rifiuta; sono utilizzabili soltanto da `offline_verify.py` e dai test.

## Verifica offline eseguita

Il 12 settembre 2026 `offline_verify.py` ha verificato tre schemi JSON, il manifest sintetico,
il contratto dei due insight, il parser diagnostico, il renderer e la forma esatta 8 A / 16 B-LF
/ 16 E-LF con 14 insight peer. Il conteggio usa esclusivamente il tokenizer dello snapshot locale
Qwen e non ha aperto connessioni HTTP.

Il test ha anche corretto una incompatibilità con `transformers` 5: `apply_chat_template`
restituisce un `BatchEncoding`, il cui `len` conta le chiavi e non gli ID. Una regressione ora
verifica il conteggio di `input_ids`.

Risultati sintetici, non rappresentativi:

- profilo nominale: 2.217–4.603 token di input;
- profilo di stress: 6.550–9.875 token di input;
- entrambi: gate statico di contesto `FAIL` rispetto a 7.168 token e al margine richiesto;
- configurazione di generazione congelata: `false`;
- chiamate modello/HTTP: 0/0.

Il fallimento di capienza delle fixture non autorizza a scegliere fault, ridurre o rigenerare dati
per ottenere un PASS. La verifica della capienza reale resta sospesa fino al manifest scientifico
autonomo e congelato. Il risultato machine-readable è in `offline/OFFLINE_VERIFICATION.json`.
