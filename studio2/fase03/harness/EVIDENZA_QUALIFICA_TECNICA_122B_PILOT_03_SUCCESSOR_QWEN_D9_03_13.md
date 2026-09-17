# Evidenza Gate B — qualifica tecnica 122B su `pilot-03`

Verdetto: **TECHNICAL STOP — READY FOR REVIEW (author)**.

Data: 17 settembre 2026, Europe/Rome. Il Gate B è stato disposto esplicitamente da Luca con
scope limitato a una sola qualifica tecnica 122B, senza retry, resume, T9, 27B o remediation.
Lo STOP è avvenuto durante la verifica non generativa dell'identità endpoint, prima del wrapper,
prima della costruzione del client e prima di qualunque intent nel ledger.

## Pre-condizioni

- worktree `/Users/luker/.codex/worktrees/dd86/fot-tep`, HEAD
  `59293f9c89c3c826b6c120239dd34b4bac69ae38`;
- mini-review indipendente `b567`: `AUTHORIZATION OK — GATE B MAY BE DISPOSED`; SHA-256 della
  regione dichiarata `32d520e52cb456d6e86027aacbe3458b3f55519bad6fb0e89ffcc45135f5fe89`;
- config autorizzata SHA-256
  `0c3cd34ef137cae4388e7868e4aa1e8d9bf494ab563fcabbdbcdc66bc7fe0606`;
- authorization SHA-256
  `7dcec1055696fa26b9baad40f1937f4ca55dc450a9f277ca9b01271b6ff1c875`;
- `require_execution(config)`: PASS offline;
- `lsof` iniziale vuoto sulle famiglie `ledger.sqlite3*` di `pilot-001` e `pilot-03`;
- ledger `pilot-03` SHA-256
  `8af057b5e295a21a3aa178e414673f4fe6e76979670a2b74a5a487606b4e01f1`;
- ledger `pilot-001` SHA-256
  `4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`;
- nessun sidecar in `pilot-03`; nessun processo SSH/autossh era visibile nella sessione locale.

Luca ha dichiarato che il tunnel 27B separato è attivo e funzionante. Tale tunnel non è stato
usato, interrogato, aperto, chiuso o modificato da questa esecuzione 122B.

I sidecar storici inattivi di `pilot-001` erano già presenti: WAL di 0 byte, mtime
`2026-09-16 03:29:15 +0200`, e SHM di 32768 byte, mtime `2026-09-16 03:31:41 +0200`.

## Gate A riassunto

Il Gate A aveva modificato esclusivamente `scope`, `status` e `study_model_decision`, rimosso
`execution_authorization_intentionally_absent` e aggiunto `execution_authorization`. Il JSON
canonico della config finale senza il riferimento all'authorization ha SHA-256
`7fc1871c390e12dbb052bdad96a796f05da9baaaa56349dbe978e87df1b33a76`.

## Identità endpoint e STOP

Il provider congelato richiede modello `qwen3.5-122b` e fingerprint opaco esatto
`vllm-0.27.1-934a3247`. La rotta 122B era raggiungibile direttamente sulla VPN ENEA preesistente
via `utun4`; non richiede il tunnel SSH locale. Il tunnel vincolato a `127.0.0.1` e inoltrato al
servizio remoto `127.0.0.1:8001` riguarda esclusivamente il 27B; è dichiarato attivo e funzionante
dall'autore, ma non è stato usato o modificato nel Gate B 122B.

Sono state effettuate dieci sole richieste HTTP non generative di verifica. I primi cinque
controlli hanno accertato raggiungibilità e comportamento della credenziale di fallback:

- `/health`: HTTP 200, corpo vuoto;
- `/version`: HTTP 200, `version=0.27.1`;
- `/v1/models`: tre controlli HTTP 401, due con la credenziale di fallback prevista dal runner
  e uno senza header di autorizzazione.

La credenziale privata in `/Users/luker/fot-tep/studio2/fase03/api_key.json` è stata quindi
letta in memoria senza stamparla né inserirla nell'argv. Con tale credenziale, altri cinque
controlli non generativi hanno prodotto:

- `/v1/models`: HTTP 200, modello esatto `qwen3.5-122b`, root
  `Qwen/Qwen3.5-122B-A10B-FP8`, `max_model_len=131072`, nessun fingerprint;
- `/version`: HTTP 200, `version=0.27.1`;
- `/health`: HTTP 200, corpo vuoto;
- `/metrics`: HTTP 200, nessun fingerprint completo né suffisso `934a3247`;
- `/openapi.json`: HTTP 200, nessun valore del fingerprint completo né suffisso `934a3247`.

Il modello e la versione sono dunque attestati, ma non lo è il fingerprint opaco esatto
`vllm-0.27.1-934a3247`. Il suffisso non può essere inferito dal solo numero di versione. È stato
perciò applicato lo STOP fail-closed prima del trasporto generativo. Il raw delle risposte HTTP
non è incluso nel repository; il log conserva soltanto status, metadati selezionati e SHA-256
dei corpi. Nessun segreto è versionato.

## Wrapper ed esecuzione tecnica

Interprete predisposto: `/opt/anaconda3/bin/python3`, CPython 3.13.9 arm64, con `openai 1.109.1`,
`transformers 4.57.6` e `jsonschema 4.25.0`. L'argv completo previsto è conservato nel log.

Il wrapper non è stato avviato e non esiste un exit code del comando tecnico. Di conseguenza:

- client costruiti: 0;
- richieste native/generative: 0;
- intent, request, response, receipt e stage nuovi: 0;
- retry e `--resume`: 0;
- chiamate T9, 27B o remediation: 0;
- summary e journal `technical_qualification_122b_*`: assenti.

## Evidenza durevole e accounting

Lettura SQLite conclusiva con URI `mode=ro&immutable=1`, senza `PilotLedger`:

| Oggetto | Conteggio |
|---|---:|
| schema `user_version` | 4 |
| requests | 0 |
| responses | 0 |
| receipts | 0 |
| stages | 0 |
| events | 1 (`successor_lineage`) |
| richieste native locali | 0 |

La lineage predecessore resta S=5, addebitata una volta. La qualifica tecnica non ha consumato
la chiamata pianificata: massimo cumulativo pianificato invariato `166/200`, margine invariato
`34`. Non esistono token prompt/completion/total né `returned_model` o `system_fingerprint`
osservati da una risposta generativa. Il modello osservato dall'endpoint non generativo è
`qwen3.5-122b`; `system_fingerprint` resta non attestato.

Gli SHA finali dei due ledger coincidono con quelli iniziali. `lsof` conclusivo è vuoto e
`pilot-03` non ha sidecar. Il listing di `pilot-03` differisce dalla materializzazione soltanto
per i due file già prodotti dal Gate A; il listing top-level e le mtime di `pilot-001` sono
invariati rispetto alla precondizione di questa esecuzione.

## Limiti

`server_enea.json` non è stato letto. Il file privato `api_key.json` è stato usato soltanto per
le verifiche di identità non generative ed è rimasto fuori dal repository. Il tunnel SSH 27B
(`127.0.0.1` locale verso
`127.0.0.1:8001` remoto), dichiarato attivo e funzionante da Luca, è rimasto fuori perimetro; il
server 27B non è stato interrogato, riavviato o riconfigurato. Nessun `--max-model-len` è stato
toccato. La VPN era una sessione utente
preesistente e non è stata aperta né chiusa da questa esecuzione. Non sono autorizzati retry,
resume o tentativi generativi successivi da questo verbale.

**VERDETTO: TECHNICAL STOP — READY FOR REVIEW (author)**
