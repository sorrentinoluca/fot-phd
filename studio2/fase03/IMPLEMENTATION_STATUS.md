# Fase 03 — stato dell'implementazione

Questo file registra il codice predisposto oltre la ricognizione 03.0, il catalogo D1, i run
fault di sviluppo e la sola sonda sintetica esplicitamente autorizzata. Non è un report di
chiusura della macro-Fase 03 e non autorizza ulteriori chiamate al modello.

| Componente | Stato | Può essere eseguito ora? |
| --- | --- | --- |
| Catalogo D1 | congelato: F1/F2/F3/F8/F10/F13/F14/F15 | sì, come input già fissato |
| Run fault di sviluppo | 40/40 completi, zero trip; conservati e verificati per riscaricamento | sì, dopo verifica indipendente della consegna |
| MEX fault strumentato | hash identificato; equivalenza col MEX base dimostrata con due prove incrociate | sì, per audit; nessuna nuova simulazione autorizzata |
| Schemi insight, output diagnostico e manifest del pilot | implementati e validati offline | sì, solo validazione |
| Validatore libreria 16 insight / 14 peer | implementato e testato su fixture sintetiche | sì, solo offline |
| Controllo E-LF: cambia solo `pseudolabel` | implementato e testato | sì, solo offline |
| Renderer A/B-LF/E-LF | implementato e testato su fixture sintetiche | sì, solo offline |
| Selezione 40 prompt | implementata; catalogo e run esistono, ma feature/evidence reali mancano | no |
| Conteggio token col tokenizer locale | implementato; fixture rieseguite contro 16384 | sì, offline |
| Sonda di capienza e budget di generazione | prova sintetica provvisoria completata: 2048 passa A/B-LF/E-LF; ripetizione reale obbligatoria | **sospesa in attesa di input reali e nuovo OK** |
| Freeze della configurazione prima del gate | envelope tecnico congelato; prompt reali e budget reale pendenti; nessun `frozen_gate_config.json` | solo verifica offline |
| Gate di stabilità 40×3 | implementato con guardie fail-closed | **sospeso** |
| Logging modello/request/fingerprint/hash/latency/token | fingerprint esteso; 1 POST rifiutato e 3 inferenze sintetiche registrati | solo audit della sonda conclusa |
| Sonda producer Qwen e producer alternativo | implementata | **sospesa** |

## Separazione delle dipendenze

**Sincronizzati da `origin/main` `c6e19d6`:** report e verifica della Fase 02;
`validation/PRECALIBRATION_FREEZE.json` con `source_head_commit=d472dc5`; manifest, decisioni e
hash dichiarati da tali artefatti; sezioni Fase 02 di `studio2/PROVENIENZA.md`.

**Run fault disponibili:** campagna `fault_dev_001`, 40/40 run completi e 320 finestre
post-fault. Manifest aggregato SHA-256
`9eaed0e901c6f06d5aa94b4e2d81d5afdd3464022ae6d2709b92f872789a6d9d`; archivio pubblico
SHA-256 `6edd96711d2913953c6de81ce6dbb7c51e7677a2a7c1892b0676de5e7a9fd97c`, release
[`studio2-fase03-fault-dev-v1`](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-fault-dev-v1).
La copia è stata verificata riscaricando l'asset e confrontando 240/240 file, zero mismatch.
Questa disponibilità non produce automaticamente feature, evidence o insight.

**Endpoint canonico:** soltanto 8001@16384, PID server/EngineCore 690460/690661, vLLM 0.28.0,
GPU 0. Il fingerprint include la riga di comando e l'ambiente
`CUDA_VISIBLE_DEVICES=0`, `VLLM_USE_FLASHINFER_SAMPLER=0`. La 8001@7168 è superata e non più
disponibile; la KV cache da 34.133 token è telemetria dipendente dal contesto e non una chiave di
confronto. Record e launcher sono conservati in `env/`.

**Ancora da realizzare scientificamente:** feature/evidence/verbalizzazioni associate ai 40 run,
insight e prototipi, più il manifest autonomo dei veri input del pilot. I run sono materiale di
sviluppo, non valutazione, e non vengono promossi direttamente a prompt o risultati.

## Fixture sintetiche

Le fixture di `synthetic_fixture.py` hanno `status=SYNTHETIC_OFFLINE_FIXTURE`,
`provenance_kind=synthetic_offline_only` e un catalogo esplicitamente non scientifico. Il
percorso scientifico del preparatore le rifiuta. La sola eccezione è il percorso separato
`--synthetic-profile cap_stress`, protetto da acknowledgement dedicato e incapace di autorizzare
il gate. La sua prova conclusa è descritta in `PROVISIONAL_STRESS_PROBE.md`.

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
