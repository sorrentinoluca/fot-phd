# Completamento Gate B — qualifica tecnica 122B su `pilot-03`

Verdetto: **TECHNICAL PASS — READY FOR REVIEW (author)**.

Data: 17 settembre 2026, Europe/Rome. Questa evidenza completa il Gate B e supera lo STOP
pre-generativo registrato nel commit `8d8ac603eeeadcf7c92fd07ca33993f51580239c`. La disposizione
dell'autore ha richiesto esplicitamente di avviare il wrapper, produrre binding, response,
accounting e outcome e attestare il fingerprint 122B. Sono rimasti invariati i vincoli di una
sola richiesta tecnica, nessun retry, resume, T9, 27B o remediation.

## Interpretazione operativa della disposizione

Gli endpoint non generativi attestano modello e versione, ma non espongono il fingerprint opaco.
Il fingerprint completo è stato quindi verificato sulla singola risposta tecnica autorizzata,
prima di accettare l'esito come PASS. Il wrapper è fail-closed: un mismatch di modello,
fingerprint, schema, reasoning o finish reason avrebbe prodotto uno STOP durevole senza reinvio.

## Pre-condizioni

- HEAD di esecuzione `8d8ac603eeeadcf7c92fd07ca33993f51580239c`; i byte di
  `technical_qualification_122b.py` coincidono con il candidato autorizzato `59293f9`;
- config autorizzata SHA-256
  `0c3cd34ef137cae4388e7868e4aa1e8d9bf494ab563fcabbdbcdc66bc7fe0606`;
- authorization SHA-256
  `7dcec1055696fa26b9baad40f1937f4ca55dc450a9f277ca9b01271b6ff1c875`;
- provider 122B SHA-256
  `04b2c948c586c9ae4e38d9d0c50d36aad86a5b609a609d94c2d31fde7c2a8bf0`;
- ledger `pilot-03` prima della chiamata SHA-256
  `8af057b5e295a21a3aa178e414673f4fe6e76979670a2b74a5a487606b4e01f1`;
- ledger `pilot-001` SHA-256
  `4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`;
- conteggi iniziali `pilot-03`: 0 request, 0 response, 0 receipt, 0 stage, 1 evento;
- `lsof` iniziale vuoto sulle due famiglie SQLite; nessun sidecar `pilot-03`.

La sessione di completamento ha eseguito tre richieste non generative: `/v1/models` HTTP 200,
un URL di versione composto erroneamente HTTP 404 e il corretto `/version` HTTP 200. Il primo
ha confermato `qwen3.5-122b`, root `Qwen/Qwen3.5-122B-A10B-FP8` e capienza 131072; l'ultimo ha
confermato vLLM `0.27.1`. Il 404 non ha costruito alcun client OpenAI, non ha generato token e non
ha modificato il ledger.

## Esecuzione unica

Il wrapper è stato avviato una sola volta con `/opt/anaconda3/bin/python3`, CPython 3.13.9 arm64,
`max_retries=0` e l'ACK esatto `EXECUTE_PHASE03_122B_TECHNICAL_QUALIFICATION`. Inizio
`2026-09-16T22:41:48Z`, fine `2026-09-16T22:41:55Z`, exit code 0. La credenziale privata è stata
letta in memoria e passata esclusivamente tramite variabile d'ambiente; non è stata stampata né
inserita nell'argv.

Esito della risposta tecnica:

| Campo | Valore |
|---|---|
| request ID | `ad50077666b5504667ccbb63a5a84c5f6f151695aea1bd10619febcb2c779e62` |
| response ID | `chatcmpl-ad06852d4d862c38` |
| returned model | `qwen3.5-122b` |
| system fingerprint | `vllm-0.27.1-934a3247` |
| identity valid | `true` |
| schema valid al primo tentativo | `true` |
| reasoning assente | `true` |
| finish reason | `stop` |
| technical pass | `true` |
| token prompt/completion/total | `42 / 10 / 52` |

Il raw della risposta non è versionato. Il suo SHA-256 durevole è
`be93aab00d67415e6500bf80125f5b8bee6586756554cedb4850ba97181c2113`; lo SHA-256 del record
normalizzato è `40901f53e648dc56e83b61841442790af7140bb6ef9134615693167ca5ac8566`.

## Evidenza durevole e accounting

La verifica conclusiva è stata eseguita con SQLite `mode=ro&immutable=1`, senza costruire
`PilotLedger`:

| Oggetto | Esito |
|---|---|
| binding stage | 1, SHA-256 `c2be8e58efd7dc00ba4f2435af7ce7a36e97a50eca09a36f2c58fdcbec3f00ce` |
| request | 1, `COMPLETED`, quota `technical` |
| response | 1, record autenticato |
| receipt accounting | 1 |
| outcome | `PASS`, SHA-256 `cdf5247d6cd6aa5c36e254edf2dcdd3b919b375ec0343429f12c0e86f149b672` |
| richieste native locali | 1 |
| token prompt/completion/total | `42 / 10 / 52` |

Il summary `technical_qualification_122b_summary.json` è `PASS`, registra una richiesta provider
e ha SHA-256 `3a3eaf15b6208eb86a697dcc9683677c39bc02d161529317c1a8a3cf8b33210d`.
Il journal ha SHA-256 `f6e44bd4e7680eabdc17a2fc72a9afb376c78ba419bd3ca52e6182c4288be60b`.

La chiamata tecnica pianificata è ora consumata `1/1`. La lineage predecessore resta S=5,
addebitata una volta; il massimo cumulativo pianificato resta `166/200`, con margine 34.
Il ledger `pilot-03` finale ha SHA-256
`619a66c7bb81477e302a362ebbaf7bae96adb98411a532f9ae9b9465ab52c801`.
Il ledger `pilot-001` è invariato. `lsof` conclusivo è vuoto e `pilot-03` non ha sidecar.

## Limiti

Non è stato eseguito alcun retry o `--resume`. Nessuna chiamata T9, 27B o remediation. Il tunnel
27B dichiarato attivo dall'autore non è stato usato, interrogato, aperto, chiuso o modificato.
`server_enea.json` non è stato letto. Nessun raw provider e nessun segreto sono inclusi nel
repository. Questa è evidenza d'autore, non una review indipendente.

**VERDETTO: TECHNICAL PASS — READY FOR REVIEW (author)**
