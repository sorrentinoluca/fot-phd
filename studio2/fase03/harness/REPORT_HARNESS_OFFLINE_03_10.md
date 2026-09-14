# Rapporto del candidato harness offline 03.10

Data: 2026-09-14. Stato: **candidato esatto da verificare
indipendentemente**. 03.10 e Fase 03 restano aperte; nessun GO del pilot.

## Identità del candidato

| Voce | Valore |
| --- | --- |
| Base `origin/main` osservata | `a00605862f627710347bd63c49f79a6d0a00135f` |
| Branch dedicato | `codex/studio2-harness-0310-offline` |
| Candidato offline assestato | `59b6b93cd9c215e8b687e540f7cd579804b7c66a` |
| Tree candidato | `cf08c14a8deb18145189afbe9722d7da46bc2f82` |
| Manifest candidato | `HARNESS_OFFLINE_CANDIDATE.json`, SHA-256 `751b95a8bce62c4f8acbf907ba1cbfcf01850538711ae9dfe6928f62ebd430d3` |
| Sorgente harness confrontata | `codex/studio2-harness` a `1ac06ebdc92f73d3b630ccca9bf75f413bea170b` |
| Effetti esterni | zero push, tag, chiamate API, inferenze e simulazioni |

Il manifest è interno al candidato e impronta i 21 file di contenuto senza
auto-improntarsi. Questo rapporto successivo registra commit, tree e SHA-256 del
manifest senza modificare il candidato.

## Inventario e importazione controllata

Dal package preesistente sono stati recuperati e adattati soltanto:

- canary e sampling deterministici;
- guardie di pin e compatibilità;
- assemblaggio degli input e adapter insight;
- prompt producer, rendering con local-first e logging forense;
- calcolo separato dell'ordine prompt-facing.

Non sono stati importati i vecchi `HARNESS_FREEZE.json`,
`INTEGRATION_STATUS.json`, report/consegne, manifest incompleti o documenti
destinati a sovrascrivere le pubblicazioni correnti. `guards.py`,
`logging_v1.py`, `producer.py` e `sampling.py` sono recuperati byte-identici;
gli altri cinque moduli sono adattati. Nessun vecchio byte è dichiarato
qualificato per la sola provenienza.

Le dipendenze obsolete eliminate dal percorso corrente erano evidence v1,
schema R3, Normal ancora dichiarati mancanti, modello/server Qwen-27B ereditato,
firma di divergenza a sei campi e riserva non persistente. Mancavano una fonte
contabile condivisa, l'evaluatore T3/T4/T6 rev.10, la distinzione fra input
producer e libreria prodotta, la validazione R4 per coppia e l'indipendenza fra
ordine canonico e ordine presentato.

Sono nuovi `ledger.py`, `gate_rules.py` e i test contrattuali offline. Sono
aggiornati `protocol.py`, `run_pilot.py`, `producer_probe.py`, preflight e
configurazione. `metric_adapter.py`, `metrics.py` e i test del raccordo minimo
non sono stati modificati.

## Pin e input collegati

Il candidato verifica insieme:

- evidence 03.6 a sorgente `c66bd8dddf8e2af9dd0665ee30afd36c248b93fb`,
  integrazione `7c99a8318cbe24bf864790566302f72614d963ed`, release
  `studio2-fase03-evidence-v2`, archivio
  `6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf`;
- R4 al target `3c64390bc4dd58c48cc4e1e388a38989b32b3143`, manifest
  `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`,
  tag object `4d15c4fb915ea9db9f7425225d231746778f0ba1` e peeled sul
  target;
- Normal handoff 03.9 a sorgente
  `6372cb3c457a30b39c838e066b613c61313c35db`, SHA-256
  `e2409c64ad4e36e0f3b597a5e0b9745d866af72f4da717fc7a128b25753c166a`;
- rev.10 a candidato `6aaa5b3eebfed4ba502c25c0443caabd0051af21`,
  piano `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`
  e manifest `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`;
- delta 03.10 blob `780e08ae9e176a819a745ab2054a2e6ae79a8a9a`,
  SHA-256 `e92661fe754bb12ac84578a03b6e6815beaade9731fed5dd608f5682ce2f355e`.

L'inventario contiene 320 finestre fault di sviluppo, sedici esempi fault
locali, otto esempi Normal reali e sedici contratti fissi. La libreria insight è
esplicitamente assente: le otto chiamate di conformità dovranno produrla e
validarla 16/16 contro R4. Il solo requisito mancante dell'inventario è quindi
`16 real schema-valid producer insights`; il suo stato resta `INCOMPLETE`.

## Regole rev.10 implementate

Il ledger SQLite registra l'intento prima del trasporto, sopravvive a directory,
riavvii e processi e impedisce duplicati concorrenti. Impone l'ordine
conformità → eventuale remediation → sonda → gate, outcome completi di stadio,
una remediation autorizzata su diff concreto, `8r+t<=15`, triplette di sonda
atomiche, massimo sette trasporti finché si preserva la remediation, nessun
retry del gate, massimi pianificati 152/160 e hard stop 200 separato.

Il gate usa validità più coppia `(abstain, predicted_label)`. Le differenze
forensi non producono divergenza; il troncamento resta T4 separato. Sono
implementati T3 ≥114/120 con astensione per condizione, T4=0, divergenza delle
triplette miste e T6 non valutabile per triplette tutte invalide. Un esito R3
resta `R3_REQUIRED_PENDING_FEASIBILITY`, mai GO finale. T5 è riportato come
`NOT_MEASURED_BY_OFFLINE_EVALUATION`.

## Conflitti e precedenze fra fonti

| Fonte e formulazione esatta | Fonte corrente e risoluzione |
| --- | --- |
| `1ac06eb:studio2/fase03/harness/SPECIFICA_HARNESS.md`: «evidence 03.6 dal commit `2f6dd8de...` e dalla release `studio2-fase03-evidence-v1`» | Le pubblicazioni successive fissano evidence v2, sorgente `c66bd8d...` e integrazione `7c99a83...`; il candidato usa i pin correnti. |
| Stesso file: «schema insight 03.12 esclusivamente nei byte del commit `e058cb07...`» | `schema_insight/PUBBLICAZIONE_SCHEMA_INSIGHT.md`: «Target R4 verificato e unico destinatario del tag» `3c64390...`; R4 prevale. |
| Stesso file: «`normal_dev` della 03.9 quando sarà specificato, prodotto e conservato» | `baseline_numerica/PUBBLICAZIONE_BASELINE_03_9.md`: «La baseline numerica 03.9 è congelata»; gli otto esempi dell'handoff vengono collegati. |
| Stesso file, §4: «ordine producer → gate — proposta 1c» e «La decisione resta dell'autore» | `piano_statistico/DELTA_HARNESS_03_10.md`: «Ordine obbligatorio: conformità producer → eventuale remediation → sonda budget → gate 40×3». L'ordine degli stadi non è più pending. |
| `PREFLIGHT_03_0.md`: «Il pilot resta preliminare su `Qwen/Qwen3.8-27B-FP8`» | L'handoff corrente dice «D9 resta una decisione distinta». La frase rimane come storia 03.0; l'addendum vieta di usarla come default. |
| Handoff rev02, §4.4: «revisione 10 approvata, firma e chiusura pendenti» | Il delta rev.10 è normativo per 03.10, ma non congela l'intero piano 03.8. Nessun file del piano o `APERTURA` è stato scritto. |
| Handoff rev02, tabella iniziale: 03.9 «Integrata e dati pubblicati, ma aperta» | La pubblicazione successiva 03.9 dice «è congelata» e lascia 03.10 aperta; viene adottato lo stato successivo senza estenderne l'OK all'harness. |

Non resta un conflitto implementativo irrisolto. Restano decisioni aperte, non
conflitti: D9 e approvazione dell'ordine prompt-facing.

## Test offline eseguiti

Comandi:

```text
python3 -m unittest -v \
  studio2.fase03.harness.test_harness_offline \
  studio2.fase03.harness.test_metric_raccordo \
  studio2.fase03.tests.test_execution_guard \
  studio2.fase03.tests.test_protocol

/opt/anaconda3/bin/python3 -m unittest discover -v studio2/fase03
python3 -m compileall -q studio2/fase03
git diff --check
```

Esiti: **45/45** mirati, **80/80** discovery Fase 03, compilazione OK e diff
check OK. I test coprono pin e tampering R4; Normal/input mancanti; assenza di
default D9; separazione dell'ordine label; persistenza, restart e due writer;
timeout con/senza prova zero token; remediation e relativo retry contabile;
triplette e quota; gate create-once senza retry; 114/113; differenze forensi;
triplette miste/tutte invalide; troncamento e T5 non misurato. I nove test del
raccordo metriche passano senza modificare il codice qualificato.

## Decisioni e dati ancora mancanti

Serve approvazione separata di:

1. ordine prompt-facing 1a già calcolato, senza rifare 03.7;
2. D9 proposta: 122B producer/consumer canonico, Terra solo producer alternativo,
   27B fallback condizionato e qualificato separatamente.

Servono inoltre identità/revisioni esatte, configurazione provider/server,
tokenizer e chat template, sedici insight reali R4, limiti e fingerprint,
calendario operativo e misura di fattibilità T5. La proposta è registrata in
`DECISIONE_D9_ORDINE_LABEL_PENDING.md`; la configurazione canonica resta
`UNDECIDED`.

## Protocollo delle future prove server

1. Congelare approvazioni, D9, revisioni, provider, tokenizer/chat template,
   limiti e fingerprint; scegliere un `pilot_id` e un percorso assoluto condiviso
   del ledger. Verificare tutti i pin prima di qualsiasi invio.
2. Eseguire otto conformità producer. Ogni intento entra nel ledger prima del
   trasporto; conservare raw, token, latenza e identità restituita. Richiedere
   16/16 insight R4 validi al primo tentativo.
3. Se e solo se si diagnostica una classe ammessa, sottoporre diff del solo
   prompt producer e approvazione scritta; autorizzare una sola remediation
   completa di otto richieste. Non riusare gli output precedenti.
4. Costruire libreria e 40 prompt reali; contare col tokenizer/chat template
   congelati. Eseguire sonde A/B-LF/E-LF in triplette complete su 2048, 3072,
   4096 finché passa il primo budget. Un trasporto si ripete solo con prova zero
   token e nei limiti della riserva. Congelare il risultato.
5. Eseguire una sola volta il gate 40×3, sequenziale secondo configurazione,
   senza retry. Applicare T3/T4/T6 e conservare forense separato.
6. Misurare chiamate e tempi per blocco/modello sulla configurazione effettiva,
   applicare il margine del 20% e decidere T5. Non usare proiezioni della vecchia
   fixture. R3, se attivato, resta subordinato a questa fattibilità e agli altri
   prerequisiti.

Queste prove potranno qualificare soltanto la combinazione realmente osservata.
Il candidato offline non qualifica tokenizer, capienza, stabilità, latenza,
servizio, producer, consumer o pilot.
