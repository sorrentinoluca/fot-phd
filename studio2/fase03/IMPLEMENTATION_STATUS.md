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
| Conteggio token col tokenizer locale | implementato; fixture rieseguite contro 16384 | sì, offline |
| Sonda di capienza e budget di generazione | implementata e presentata, massimo 9 chiamate | **sospesa in attesa di input reali e OK** |
| Freeze della configurazione prima del gate | envelope tecnico congelato; prompt reali e budget selezionato pendenti | solo verifica offline |
| Gate di stabilità 40×3 | implementato con guardie fail-closed | **sospeso** |
| Logging modello/request/fingerprint/hash/latency/token | fingerprint esteso a comando, ambiente `VLLM_*`/`CUDA_*`, PID e vLLM | **sospeso** |
| Sonda producer Qwen e producer alternativo | implementata | **sospesa** |

## Separazione delle dipendenze

**Sincronizzati da `origin/main` `c6e19d6`:** report e verifica della Fase 02;
`validation/PRECALIBRATION_FREEZE.json` con `source_head_commit=d472dc5`; manifest, decisioni e
hash dichiarati da tali artefatti; sezioni Fase 02 di `studio2/PROVENIENZA.md`.

**Endpoint canonico:** soltanto 8001@16384, PID server/EngineCore 690460/690661, vLLM 0.28.0,
GPU 0. Il fingerprint include la riga di comando e l'ambiente
`CUDA_VISIBLE_DEVICES=0`, `VLLM_USE_FLASHINFER_SAMPLER=0`. La 8001@7168 è superata e non più
disponibile; la KV cache da 34.133 token è telemetria dipendente dal contesto e non una chiave di
confronto. Record e launcher sono conservati in `env/`.

**Ancora da realizzare scientificamente:** catalogo definitivo, 40 run fault di sviluppo,
feature/evidence/verbalizzazioni associate e manifest autonomo dei veri input del pilot. Questa
finestra non seleziona fault, non genera dati e non crea surrogati da promuovere a input reali.

## Fixture sintetiche

Le fixture di `synthetic_fixture.py` hanno `status=SYNTHETIC_OFFLINE_FIXTURE`,
`provenance_kind=synthetic_offline_only` e un catalogo esplicitamente non scientifico. Il
preparatore esecutivo le rifiuta; sono utilizzabili soltanto da `offline_verify.py` e dai test.

## Verifica offline eseguita

Il 13 settembre 2026 `offline_verify.py` ha riverificato tre schemi JSON, il manifest sintetico,
il contratto dei due insight, il parser diagnostico, il renderer e la forma esatta 8 A / 16 B-LF
/ 16 E-LF con 14 insight peer. Il conteggio usa esclusivamente il tokenizer dello snapshot locale
Qwen e non ha aperto connessioni HTTP.

Il test ha anche corretto una incompatibilità con `transformers` 5: `apply_chat_template`
restituisce un `BatchEncoding`, il cui `len` conta le chiavi e non gli ID. Una regressione ora
verifica il conteggio di `input_ids`.

Risultati sintetici, non rappresentativi:

- profilo nominale: 2.217–4.603 token di input;
- profilo di stress: 6.550–9.875 token di input;
- al candidato massimo 4096, fabbisogno incluso margine: nominale **9.467**, stress **14.739**;
- entrambi: gate statico di contesto `PASS` rispetto a 16.384 token e margine 256;
- configurazione di generazione congelata: `false`;
- chiamate modello/HTTP: 0/0.

Il PASS di capienza delle fixture non autorizza a scegliere fault né a promuovere dati sintetici.
La verifica della capienza reale resta sospesa fino al manifest scientifico autonomo e congelato.
Il risultato machine-readable è in `offline/OFFLINE_VERIFICATION.json`.
