# Registrazione avvio endpoint 8001 @ max-model-len 16384

Host: **albireo** — utente `luca`
Data/ora redazione: **2026-09-13 01:54 CEST** (`2026-09-13T01:53:49+02:00`)
Avvio processo: **dom 13 set 2026, 01:52:36 CEST** — "Application startup complete" alle **01:53:08**
Scopo: preflight Fase 03 (`studio2/fase03`) — fingerprint della configurazione.

---

## 1. Esito

**Endpoint 8001 ONLINE a 16384 token di contesto.** Nessuna chiamata di inferenza effettuata
(solo GET `/v1/models` e `/health`). L'endpoint sulla porta 8000 non è stato toccato.

## 2. Identificativi di processo

| Ruolo | PID | Note |
|---|---|---|
| API server (8001) | **690460** | avviato da `nohup /home/luca/fot-exp2/start_vllm_8001_16384.sh` |
| EngineCore (8001) | **690661** | figlio di 690460 |
| resource_tracker (8001) | 690660 | figlio di 690460, ausiliario |
| API server (8000) — **INTATTO** | 554919 | uptime 4d 16h, invariato |
| EngineCore (8000) — **INTATTO** | 555102 | invariato |

## 3. Riga di comando completa (da `/proc/690460/cmdline`)

```
/home/luca/fot-exp2/env-vllm/bin/python3 /home/luca/fot-exp2/env-vllm/bin/vllm serve Qwen/Qwen3.8-27B-FP8 --revision 017b9c7af6b5689d5dd426a76e0bc077eb5ca20a --served-model-name fot-exp2-consumer --host 127.0.0.1 --port 8001 --tensor-parallel-size 1 --max-model-len 16384 --max-num-seqs 1 --gpu-memory-utilization 0.97 --language-model-only --reasoning-parser qwen3 --seed 20260829 --generation-config vllm --enforce-eager --no-enable-prefix-caching --kernel-config {"enable_flashinfer_autotune":false,"enable_jit_warmup":false,"enable_cutedsl_warmup":false}
```

Variabili d'ambiente rilevanti del processo (da `/proc/690460/environ`):

```
CUDA_VISIBLE_DEVICES=0
VLLM_USE_FLASHINFER_SAMPLER=0
```

Differenze rispetto alla configurazione 8001 precedente (contesto 7168): **solo**
`--max-model-len 16384` (era `7168`). Tutti gli altri flag sono identici, verificati confrontando
la riga `non-default args` del log `vllm-7168.log` (run riuscito, APIServer pid 636846) con quella
del nuovo log. `VLLM_USE_FLASHINFER_SAMPLER=0` era presente anche nella configurazione precedente
(vedi §6).

## 4. Versione vLLM e modello

- vLLM: **0.28.0**
- Modello: `Qwen/Qwen3.8-27B-FP8`, revisione `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`
- Architettura risolta: `Qwen3_5ForConditionalGeneration`, quantizzazione fp8, dtype `torch.bfloat16`
- Modalità: text-only (`--language-model-only`; tutti i limiti multimodali a 0)
- Sampler: `topk_topp_sampler.py:46` — "FlashInfer top-p/top-k sampling disabled via VLLM_USE_FLASHINFER_SAMPLER=0"

## 5. GPU

| GPU | UUID | Occupazione | Processo |
|---|---|---|---|
| 0 | `GPU-25bae28c-82aa-771f-f2c8-0798a67f8bd1` | 31480 MiB / 32760 MiB | **EngineCore 690661 → 31222 MiB** (+ Xorg/gnome ~185 MiB) |
| 1 | `GPU-a1569a5c-f1c5-a99b-8bf7-e7b9a5dbd01b` | 31800 MiB / 32760 MiB | EngineCore 555102 → 31776 MiB (endpoint 8000, intatto) |

L'endpoint 8001 gira su **GPU 0**, UUID `GPU-25bae28c-82aa-771f-f2c8-0798a67f8bd1`.

### Riga KV cache (dal log)

```
(EngineCore pid=690661) INFO 09-13 01:53:04 [gpu_worker.py:578] Available KV cache memory: 2.42 GiB
(EngineCore pid=690661) INFO 09-13 01:53:04 [kv_cache_utils.py:1869] GPU KV cache size: 34,133 tokens, Maximum concurrency for 16,384 tokens per request: 2.08x
```

**Concorrenza 2.08x ≥ 1** → il contesto 16384 è servibile con `--max-num-seqs 1`.

Confronto con la configurazione precedente (7168): stessa `Available KV cache memory: 2.42 GiB`,
ma `GPU KV cache size` 27,569 token contro gli attuali 34,133. Vedi §8 (anomalia 2).

## 6. Causa accertata dell'errore `OSError: [Errno 98] Address already in use`

**Causa: le continuazioni di riga dello script `start_vllm_8001_16384.sh` erano interrotte da righe
vuote.** Il file conteneva `\` seguito da `\n\n`: in bash il backslash annulla il primo newline e
unisce la riga a quella successiva, che era **vuota**; il newline della riga vuota terminava quindi
il comando. Il risultato è che veniva eseguito soltanto:

```
exec /home/luca/fot-exp2/env-vllm/bin/vllm serve Qwen/Qwen3.8-27B-FP8
```

**senza nessun flag** (le righe successive non venivano mai eseguite perché `exec` sostituisce il
processo). Prova nel log fallito: `non-default args: {'model_tag': 'Qwen/Qwen3.8-27B-FP8', 'model':
'Qwen/Qwen3.8-27B-FP8'}` — nessuna traccia di `host`, `port`, `max_model_len`, ecc.

Mancando `--port`, vLLM ha usato il **default `port: int = 8000`**
(`vllm/entrypoints/openai/cli_args.py:248`) e ha tentato il bind sulla porta 8000, **occupata
dall'endpoint di produzione su GPU 1** (PID 554919). Da qui l'`Errno 98`.

Quindi:
- **NON** era un conflitto su una porta interna di vLLM (ZMQ/EngineCore/metriche).
- **NON** c'erano socket in `TIME_WAIT` né processi orfani: `ss -tlnp` non mostrava nulla in ascolto
  su 8001 proprio perché il processo non ci ha mai provato.
- Il motivo per cui `ss | grep ':8001 '` risultava vuoto era coerente con la diagnosi.

Nota di sicurezza: i tentativi falliti hanno provato a fare `bind()` sulla porta 8000, ma il bind è
**fallito** e il processo è uscito immediatamente; l'endpoint 8000 non è stato in alcun modo
disturbato (PID 554919 invariato, uptime continuo di 4d 16h, `/v1/models` risponde).

### Errore precedente e distinto (da `/home/luca/fot-exp2/nohup.out`)

Il primo tentativo "a riga lunga" lanciato direttamente da shell era fallito con un errore diverso:

```
usage: vllm serve [model_tag] [options]
vllm serve: error: argument --max-model-len: expected one argument
```

Anche questo è un problema di spezzatura/quoting della riga di comando, non di porta. Non ha
lasciato residui (processo terminato subito, nessun bind, nessuna allocazione GPU).

### Risoluzione applicata

Rimosse le righe vuote interposte fra le continuazioni dello script (nessun flag modificato,
aggiunto, rimosso o riordinato). Copia dello script originale rotto conservata in
`/tmp/claude-1004/-home-luca-fot-exp2/d150ba9f-4924-49ab-aa50-e2acf7492a4e/scratchpad/start_vllm_8001_16384.sh.orig-broken`
(directory temporanea di sessione, non persistente).

Prima del rilancio l'argv espanso è stato verificato a secco sostituendo `vllm` con `printf` in una
copia usa e getta: 29 argomenti, tutti corretti, `--port 8001` e `--max-model-len 16384` presenti.

## 7. Seconda correzione necessaria: `VLLM_USE_FLASHINFER_SAMPLER=0`

Lo script **non** esportava `VLLM_USE_FLASHINFER_SAMPLER=0`, che invece faceva parte della
configurazione originale funzionante. Evidenza dal log `vllm-7168.log`, che contiene **tre**
tentativi di avvio:

| Tentativo | APIServer | EngineCore | Riga sampler | Esito |
|---|---|---|---|---|
| 1 | 635696 | 635920 | `topk_topp_sampler.py:62` "Using FlashInfer for top-p & top-k sampling." | **crash**, build JIT FlashInfer fallita in `_dummy_sampler_run` |
| 2 | 636206 | 636432 | `topk_topp_sampler.py:62` idem | **crash** |
| 3 | **636846** | **637074** | `topk_topp_sampler.py:46` "FlashInfer top-p/top-k sampling disabled via VLLM_USE_FLASHINFER_SAMPLER=0" | **OK** — "Application startup complete" |

I PID 636846/637074 sono esattamente quelli dell'endpoint 8001 che era in produzione: la
configurazione di riferimento **includeva** quella variabile. Conferma indipendente: il processo
vivo sulla 8000 (PID 554919) ha nel proprio `environ` `VLLM_USE_FLASHINFER_SAMPLER=0`.

Aggiungere l'export **ripristina** la parità con la configurazione precedente invece di allontanarsene,
ed è condizione necessaria all'avvio: senza, l'EngineCore va in crash sulla compilazione JIT di
FlashInfer. Nessun flag della riga di comando è stato alterato.

## 8. Esito verifiche (nessuna inferenza)

**(a) KV cache** — OK, vedi §5: `GPU KV cache size: 34,133 tokens, Maximum concurrency for 16,384
tokens per request: 2.08x` (≥ 1).

**(b) `GET http://127.0.0.1:8001/v1/models`** — OK:

```json
{"object":"list","data":[{"id":"fot-exp2-consumer","object":"model","created":1789257201,
"owned_by":"vllm","root":"Qwen/Qwen3.8-27B-FP8","parent":null,"max_model_len":16384,
"permission":[{"id":"modelperm-b3bb27ccf846ad30","object":"model_permission","created":1789257201,
"allow_create_engine":false,"allow_sampling":true,"allow_logprobs":true,
"allow_search_indices":false,"allow_view":true,"allow_fine_tuning":false,
"organization":"*","group":null,"is_blocking":false}]}]}
```

`id` = `fot-exp2-consumer`, `max_model_len` = **16384**. `GET /health` → HTTP 200.

**(c) `nvidia-smi`** — OK, vedi §5: nuovo EngineCore 690661 su GPU 0; EngineCore 555102 della 8000
ancora vivo su GPU 1 con 31776 MiB invariati.

**Socket in ascolto:**

```
LISTEN 127.0.0.1:8000  users:(("vllm",pid=554919,fd=27))
LISTEN 127.0.0.1:8001  users:(("vllm",pid=690460,fd=27))
```

**Nessuna POST** a `/v1/chat/completions` o `/v1/completions`: il contatore delle chiamate del
pilot resta a 0.

## 9. Processi terminati in questa sessione

**Nessuno.** Non è stato inviato alcun segnale ad alcun processo. I PID 636846, 637074 (vecchia 8001),
689872 e 689989 (tentativi 16384 falliti) risultavano già inesistenti all'inizio della diagnosi;
non sono stati trovati processi orfani né allocazioni GPU residue (GPU 0 a 249 MiB, solo Xorg/gnome).

## 10. Percorsi

- Log del nuovo avvio: `/home/luca/fot-phd/phase_b/exp2/qwen/sensitivity/capped_followup/logs/vllm-16384.log` (sovrascritto)
- Log della configurazione precedente: `/home/luca/fot-phd/phase_b/exp2/qwen/sensitivity/capped_followup/logs/vllm-7168.log`
- Script di avvio: `/home/luca/fot-exp2/start_vllm_8001_16384.sh`
- Questo file: `/home/luca/fot-exp2/ENDPOINT_8001_16384_RECORD.md` (fuori da qualsiasi repository)

## 11. Anomalie / punti per decisione umana

1. **Lo script `start_vllm_8001_16384.sh` è stato modificato** (rimozione righe vuote fra le
   continuazioni + aggiunta `export VLLM_USE_FLASHINFER_SAMPLER=0`). Nessun flag della riga di
   comando è cambiato; la configurazione resta confrontabile con la 7168. Da validare se lo script
   debba essere versionato altrove.
2. **`GPU KV cache size` diverso a parità di `Available KV cache memory` (2.42 GiB):** 34,133 token
   ora contro 27,569 nella run a 7168. Non è un errore e non blocca nulla (la concorrenza resta
   2.08x ≥ 1), ma è una differenza da tenere presente nel fingerprint di Fase 03: il numero di token
   di KV cache **non** è invariante rispetto a `--max-model-len` su questo modello, quindi non va
   usato come chiave di confronto fra configurazioni con contesti diversi. Plausibilmente dipende
   da come vLLM dimensiona i gruppi di KV cache per l'architettura `Qwen3_5ForConditionalGeneration`
   al variare di `max_model_len`; non è stato indagato oltre perché fuori dallo scopo operativo.
3. **Margine di memoria su GPU 0:** 31480 MiB / 32760 MiB occupati, di cui ~185 MiB dal desktop
   (Xorg/gnome-shell/portal). Se la sessione grafica dovesse allocare altra memoria video,
   il margine è stretto. `--gpu-memory-utilization` è rimasto a 0.97 come richiesto.

---

# PARTE II — Completamento per il fingerprint di Fase 03

Aggiunta il **2026-09-13 02:05 CEST**, sessione successiva a quella di avvio. Nessun riavvio,
nessun segnale ai processi, nessuna chiamata di inferenza.

## 12. Riga di registrazione della sostituzione

> **configurazione 8001@7168 (PID 636846) sostituita il 2026-09-13 01:53 da 8001@16384
> (PID 690460); i due fingerprint non sono intercambiabili**

## 13. Health check di conferma (2026-09-13 02:02 CEST)

| Endpoint | `/health` | `/v1/models` → `max_model_len` | API server PID | EngineCore PID | Uptime API server |
|---|---|---|---|---|---|
| 8000 (GPU 1) | HTTP 200 | 4096 | 554919 | 555102 | 4d 16h 26m (avvio mar 8 set 09:36:17 2026) |
| 8001 (GPU 0) | HTTP 200 | **16384** | 690460 | 690661 | 10m (avvio dom 13 set 01:52:36 2026) |

Socket in ascolto invariati (`127.0.0.1:8000` → pid 554919, `127.0.0.1:8001` → pid 690460).
Occupazione GPU invariata: GPU 0 31480 MiB / 32760 MiB, GPU 1 31800 MiB / 32760 MiB;
EngineCore 690661 → 31222 MiB su GPU 0, EngineCore 555102 → 31776 MiB su GPU 1. Utilizzo 0% su
entrambe, temperature 41 °C / 39 °C. **Nessun cambiamento rispetto alla Parte I.**

Nota di lettura: i campi `created` e `permission[].id` restituiti da `/v1/models` cambiano a ogni
richiesta (vLLM li genera al momento della risposta) — **non** sono indizio di un riavvio. Gli
indicatori di identità stabili sono PID, `ELAPSED`/`lstart` e l'occupazione GPU.

## 14. Ambiente di processo completo (PID 690460, da `/proc/690460/environ`)

Variabili `VLLM_*` e `CUDA_*` **complete** (su 49 variabili totali nell'environ):

```
CUDA_VISIBLE_DEVICES=0
VLLM_USE_FLASHINFER_SAMPLER=0
```

Non è presente **nessun'altra** variabile `VLLM_*`, `CUDA_*`, `NVIDIA_*`, `TORCH_*`, `PYTORCH_*`
o `HF_*` nell'environ dell'API server.

Processo figlio EngineCore (PID 690661), variabili aggiunte da vLLM stesso:

```
VLLM_WORKER_MULTIPROC_METHOD=spawn
```

(`CUDA_VISIBLE_DEVICES` non compare nell'environ del figlio: vLLM lo gestisce internamente dopo
lo spawn. L'assegnazione a GPU 0 è comunque confermata da `nvidia-smi`, §13.)

### 14.1 Nota critica su `VLLM_USE_FLASHINFER_SAMPLER=0`

**`ps` da solo NON mostra questa variabile.** `ps -eo args` riporta unicamente `argv`, non
l'environment: chiunque ricostruisca la configurazione dalla sola riga di comando otterrebbe un
fingerprint **incompleto e non riproducibile**, perché senza questa variabile l'EngineCore va in
crash all'avvio sulla compilazione JIT di FlashInfer (§7). Per leggerla serve
`tr '\0' '\n' < /proc/<pid>/environ`.

La variabile **non è un'aggiunta di questa sessione**: era già presente
- nel processo 8001 precedente (PID 636846), come attestato dal log `vllm-7168.log` riga 2512:
  `[topk_topp_sampler.py:46] FlashInfer top-p/top-k sampling disabled via VLLM_USE_FLASHINFER_SAMPLER=0`;
- nel processo 8000 tuttora vivo (PID 554919), il cui `environ` contiene `VLLM_USE_FLASHINFER_SAMPLER=0`.

Mancava soltanto nello script `start_vllm_8001_16384.sh`, ed è stata reintrodotta lì per
ripristinare la parità con la configurazione precedente. La riga corrispondente nel nuovo log
(`vllm-16384.log`) conferma l'effetto: `[topk_topp_sampler.py:46] FlashInfer top-p/top-k sampling
disabled via VLLM_USE_FLASHINFER_SAMPLER=0`.

### 14.2 Divergenza rilevata: `HF_HOME` non impostata sulla 8001

| Processo | `HF_HOME` |
|---|---|
| 8000 (PID 554919) | `/home/luca/fot-exp2/cache/huggingface` |
| 8001 (PID 690460) | **non impostata** → default `~/.cache/huggingface` |

Conseguenza: i due endpoint caricano i pesi da **cache HuggingFace diverse**. Verifica di impatto
svolta in §15: i pesi effettivamente caricati sono **identici**. La divergenza riguarda solo il
percorso, non il contenuto.

## 15. Provenienza dei pesi e confronto fra le due cache HuggingFace

Entrambe le cache contengono lo stesso snapshot pinnato
`017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`:

| Cache | Percorso snapshot | N. file | Blob totali |
|---|---|---|---|
| repo-locale (usata dalla 8000) | `/home/luca/fot-exp2/cache/huggingface/hub/models--Qwen--Qwen3.8-27B-FP8/snapshots/017b9c7a…` | 80 | 81 blob, 29 GB |
| home (usata dalla 8001) | `/home/luca/.cache/huggingface/hub/models--Qwen--Qwen3.8-27B-FP8/snapshots/017b9c7a…` | 76 | 76 blob, 29 GB |

Confronto file-per-file dei **basename dei blob puntati** (nella cache HF il nome del blob è
l'hash del contenuto, quindi hash uguale ⇒ byte identici). Unica differenza, 4 file accessori
presenti solo nella cache repo-locale e **assenti** da quella home:

```
crc32.txt
LICENSE
README.md
safetensors-md5sum.txt
```

Tutti gli altri 76 file — `config.json`, `generation_config.json`, `chat_template.jinja`,
`layers-*.safetensors`, tokenizer e indici — sono presenti in **entrambe** con **hash di blob
identico**. Nessun file caricato dal motore di inferenza differisce fra le due cache.

**Conclusione:** i pesi e la configurazione effettivamente usati da 8001@16384 sono byte-identici
a quelli usati da 8000@4096 e da 8001@7168, nonostante il percorso di cache diverso.

Cronologia della cache home (`stat`): directory del modello creata il **2026-09-10 00:39:08**,
blob dei pesi scritti fino alle **00:43:44** dello stesso giorno — cioè **prima** della run 7168
(2026-09-10 14:41). La run 7168 disponeva quindi già di questa cache e, come la 16384, ha caricato
i pesi in ~3,5 s senza scaricare nulla (`Loading weights took 3.46 seconds` nella 7168,
`3.48 seconds` nella 16384). Entrambe registrano lo stesso warning
`You are sending unauthenticated requests to the HF Hub` (nessun `HF_TOKEN`): comportamento
identico fra la configurazione precedente e quella attuale.

## 16. Versioni dell'ambiente `/home/luca/fot-exp2/env-vllm`

| Componente | Versione |
|---|---|
| Python | **3.12.14** |
| vLLM | **0.28.0** |
| PyTorch | **2.13.0+cu132** (`torch.version.cuda` = **13.2**, git `cf30153c4c131c8164ee7798e5022d810682e2cb`) |
| Triton | 3.7.1 |
| Transformers | 5.16.1 |
| flashinfer-python | 0.6.16.post3 (presente ma **disattivato** per il sampling, §14.1) |
| Driver NVIDIA | **580.173.02** |
| CUDA runtime riportato da `nvidia-smi` | **13.0** |
| GPU | 2 × NVIDIA RTX 5000 Ada Generation, 32760 MiB ciascuna |

Nota: `torch` è compilato per CUDA **13.2** mentre il driver espone CUDA **13.0**; la
configurazione è funzionante (minor-version compatibility), ma è un dato da riportare tale e quale
nel fingerprint.

## 17. Hash SHA-256 al momento della registrazione

Calcolati il **2026-09-13 02:04:40 CEST**.

| File | SHA-256 | Byte |
|---|---|---|
| `/home/luca/fot-exp2/start_vllm_8001_16384.sh` | `fca8ea1c48bd640f28a944ae038e70cf896c3de7b231198e7c3474c374ffa36f` | 636 |
| `…/logs/vllm-16384.log` (file intero, istantanea) | `7230dfafb7e310cf7a348130a609a458cabffd2d526f7f699644f306bb91ca46` | 20442 |
| `…/logs/vllm-16384.log` — **blocco di avvio** (righe 1–120, fino a `Application startup complete` inclusa) | `c95c620cccac3447630c57a4667dd3f34b433cf919c1ad77bd81eeb6e31dad19` | 20031 |
| `…/logs/vllm-7168.log` (chiuso, stabile) | `c5d0bae0f40784eb3011020bd4a540025c763f40b41d4b8c708ac7dfe169c916` | 568203 |

**Avvertenza d'uso.** `vllm-16384.log` è un file **append-only di un processo vivo**: vLLM vi
registra una riga per ogni richiesta HTTP servita, quindi l'hash del file intero **cambia a ogni
richiesta** ed è valido solo come istantanea a 20442 byte. Per il fingerprint di Fase 03 usare
l'hash del **blocco di avvio** (`c95c620c…`), che è invariante finché il processo non viene
riavviato. L'hash di `vllm-7168.log` è invece stabile: quel processo è terminato.

Lo script ha `mtime` 2026-09-13 01:52:31, cioè **anteriore** all'avvio del processo (01:52:36):
il binario in esecuzione corrisponde al contenuto hashato.

### 17.1 Traffico HTTP registrato dall'avvio (prova dell'assenza di inferenza)

Conteggio completo delle richieste servite dalla 8001 dall'avvio a ora, estratte dal log:

```
      3 "GET /health HTTP/1.1" 200 OK
      2 "GET /v1/models HTTP/1.1" 200 OK
```

**Zero richieste POST.** Nessuna chiamata a `/v1/chat/completions`, `/v1/completions`,
`/v1/responses`, `/v1/messages` o `/inference/v1/generate`. Il contatore delle chiamate del pilot
resta a **0**.

## 18. KV cache — confronto 7168 vs 16384

| Configurazione | `Available KV cache memory` | `GPU KV cache size` | Concorrenza max |
|---|---|---|---|
| 8001 @ 7168 (PID 637074, 2026-09-10) | **2.42 GiB** | **27 569 token** | 3.85x per 7 168 token/richiesta |
| 8001 @ 16384 (PID 690661, 2026-09-13) | **2.42 GiB** | **34 133 token** | **2.08x** per 16 384 token/richiesta |

Righe originali:

```
(EngineCore pid=637074) INFO 09-10 14:43:45 [kv_cache_utils.py:1869] GPU KV cache size: 27,569 tokens, Maximum concurrency for 7,168 tokens per request: 3.85x
(EngineCore pid=690661) INFO 09-13 01:53:04 [kv_cache_utils.py:1869] GPU KV cache size: 34,133 tokens, Maximum concurrency for 16,384 tokens per request: 2.08x
```

**`GPU KV cache size` NON è invariante rispetto a `--max-model-len` e NON va usato come chiave di
confronto fra configurazioni.** A parità esatta di memoria disponibile (2.42 GiB in entrambi i
casi), di modello, di revisione, di `--gpu-memory-utilization` e di `--kv-cache-dtype`, il numero
di token passa da 27 569 a 34 133 (+23,8%) al solo variare del contesto massimo. Dipende da come
vLLM dimensiona i gruppi di KV cache per l'architettura `Qwen3_5ForConditionalGeneration` in
funzione di `max_model_len`; non è stato indagato oltre perché fuori dallo scopo operativo.

Per il fingerprint usare come chiavi di confronto stabili: `Available KV cache memory`, la riga
`non-default args`, l'environ del processo e gli hash di §17. `GPU KV cache size` va registrato
come **dato derivato**, valido solo entro una data configurazione di `--max-model-len`.

## 19. Permessi dei file di registrazione

Al termine di questa sessione, per prevenire modifiche accidentali:

```
chmod 444 /home/luca/fot-exp2/ENDPOINT_8001_16384_RECORD.md
chmod 444 /home/luca/fot-exp2/start_vllm_8001_16384.sh
```

I file **non sono stati spostati**: restano in `/home/luca/fot-exp2/`, fuori da ogni repository
Git (`/home/luca/fot-exp2` non è un repository), in attesa di essere copiati nel repository dello
studio 2 da un'altra sessione.

**Attenzione:** `chmod 444` rimuove anche il bit di esecuzione dallo script. Il processo 690460
attualmente in esecuzione non ne è toccato, ma un eventuale **rilancio futuro** dovrà usare
`bash /home/luca/fot-exp2/start_vllm_8001_16384.sh` oppure ripristinare prima il permesso con
`chmod 755`. Va tenuto presente per l'avvio della Fase 03.

## 20. Stato del versionamento

- `/home/luca/fot-exp2` — **non è un repository Git**. Vi risiedono lo script e questo RECORD:
  entrambi fuori da qualsiasi versionamento.
- `/home/luca/fot-phd` — **è** un repository Git, branch `codex/qwen-reasoning-cap-sensitivity`,
  ultimo commit `d4f4708` del 2026-09-10 15:21:47 (anteriore a questi interventi).
  **Nessun commit creato, nessun file tracciato modificato o in stage.**
  La directory dei log `phase_b/exp2/qwen/sensitivity/capped_followup/logs/` è **untracked** (`??`)
  e lo era già prima: `vllm-16384.log`, pur risiedendo nell'albero di lavoro del repository, non è
  noto a Git (`git ls-files --error-unmatch` fallisce).

## 21. Anomalie aperte — riepilogo aggiornato

1. **`HF_HOME` non impostata sulla 8001** (§14.2). Impatto sui pesi: **nullo**, verificato in §15.
   Da decidere se uniformare le due configurazioni impostando `HF_HOME=/home/luca/fot-exp2/cache/huggingface`
   anche sulla 8001 — comporterebbe però un riavvio, non eseguito in questa sessione.
   Effetto collaterale attuale: 29 GB di pesi duplicati su disco (739 GB liberi su 1,9 TB, non critico).
2. **`GPU KV cache size` non invariante** (§18). Non usarlo come chiave di fingerprint.
3. **`chmod 444` toglie il bit di esecuzione allo script** (§19). Rilanciare con `bash …` o
   ripristinare `chmod 755`.
4. **Margine di memoria su GPU 0**: 31480 / 32760 MiB, di cui ~185 MiB del desktop
   (Xorg, gnome-shell, xdg-desktop-portal). Se la sessione grafica allocasse altra VRAM il margine
   si assottiglia. `--gpu-memory-utilization` lasciato a 0.97 come richiesto.
5. **`torch` compilato per CUDA 13.2 su driver che espone CUDA 13.0** (§16). Funzionante, ma da
   riportare tale e quale nel fingerprint.
6. **Lo script `start_vllm_8001_16384.sh` è stato modificato** nella sessione di avvio
   (formattazione delle continuazioni + `export VLLM_USE_FLASHINFER_SAMPLER=0`). Nessun flag della
   riga di comando è cambiato. Hash del contenuto attuale in §17.

---

*Fine registrazione. File reso read-only (444) il 2026-09-13 alle 02:05 CEST.*
