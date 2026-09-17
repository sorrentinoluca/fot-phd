# Evidenza remediation producer 122B su `pilot-03` — 03.13-REM-3

Verdetto: **REMEDIATION FAIL — READY FOR REVIEW**.

Data: 17 settembre 2026, Europe/Rome. Il passo A offline è stato completato; il passo B ha
eseguito una sola invocazione del wrapper `producer_remediation`, senza retry o resume. Il
wrapper si è arrestato fail-closed durante la rivalidazione contabile, prima di creare il binding
dello stage, prima di riservare intent e prima di contattare l'endpoint chat completions.

## Passo A offline

La diagnosi `identifiers` è stata autenticata sui record T9 falliti e registrata in un unico
evento `diagnosis:producer_conformity`. L'outcome `producer_conformity` è rimasto byte-identico:
`FAIL`, `records_sha256`
`500c1c4f60ac7761514bb1311349210d7a9cfb3abf12b952fe4a2bc32ef7ad82` e diagnosi originaria
`null`.

Il template remediation deriva byte-per-byte dal template del binding
`83863085938bea35ee70cbec86e88365e7e94f95e6e17b576994635367ffd5be` e aggiunge una sola riga
di istruzioni sugli identificatori canonici e sulla corrispondenza bidirezionale con
`variable_ids`. Schema, otto casi, ordine, provider, cap e contratti restano invariati.

| Artefatto privato | SHA-256 |
|---|---|
| Approval diagnosi | `3bfba0d781dca4bb9d359d089cbd3948a4583ab99afc5df1ac0f8f7de32bb3e2` |
| Template remediation | `4306c5da6f0ebefcbce75d26d585caf82cc05ff85d5e7e6639e3f65b2d66de12` |
| Diff unificato | `7bbe19745179b90e57d8a80c2c362b1b0449d99474799f2273baae952a7a2f5f` |
| Approval remediation | `5469d14c7f1462b2f4c606705d891f4e5dffad927cd79b2829ba9f61a6193b6f` |

`require_execution` e `_prerequisites('producer_remediation')` hanno dato PASS. L'evento
`remediation_authorized` incorpora approval e template approvati.

Resta aperto il rilievo indipendente secondo cui l'evento diagnosi conserva soltanto path e hash
del proprio approval. Il file privato è presente, autenticato e con permessi `0600`; il rilievo
non è la causa del fallimento osservato in questo run.

## Endpoint e invocazione

La config esecutiva era invariata, SHA-256
`0c3cd34ef137cae4388e7868e4aa1e8d9bf494ab563fcabbdbcdc66bc7fe0606`; il provider config
aveva SHA-256 `04b2c948c586c9ae4e38d9d0c50d36aad86a5b609a609d94c2d31fde7c2a8bf0`.
La route congelata del provider è diretta, quindi non è stato aperto un tunnel SSH che avrebbe
richiesto di alterare il `base_url` autenticato. La route di rete attiva ha restituito:

- `/v1/models`: HTTP 200, `qwen3.5-122b`, root `Qwen/Qwen3.5-122B-A10B-FP8`, contesto 131072;
- `/version`: HTTP 200, vLLM 0.27.1;
- fingerprint qualificato atteso: `vllm-0.27.1-934a3247`.

La credenziale è stata letta in memoria, passata soltanto tramite variabile d'ambiente e non è
stata stampata né inserita nell'argv.

Il wrapper è iniziato alle `2026-09-17T07:58:14.529068Z` ed è terminato alle
`2026-09-17T07:58:21.053918Z`, con `/opt/anaconda3/bin/python3`, CPython 3.13.9 arm64 ed exit
code 1. L'argv non conteneva `--retry-request` o `--resume`; non è stata effettuata una seconda
invocazione.

## Arresto contabile

Prima di `bind_stage`, `producer_probe.run` chiama
`validate_tokenizer_accounting_evidence` passando i nuovi messaggi remediation indicizzati per
`logical_id`. Il validatore scorre anche gli eventi contabili durevoli T9. Poiché i due stage
riusano gli stessi logical ID `agent_1`–`agent_8`, il messaggio remediation di `agent_1` sostituisce
quello T9 durante la verifica dell'evento storico: il digest non può coincidere e il controllo
emette:

```text
FATAL_ACCOUNTING_ERROR: persisted accounting messages are invalid
```

Il ledger ha registrato fail-closed `stop:tokenizer_accounting`, legato alla request T9
`e6019d34669737981fec3174173a92c160df3e192924880226bfc7952a50bb67`, artifact SHA-256
`d02464d2937cc7d5f31038b40478bfe0b547112c277371da5c1b2d3b37dbc54a`.

La causa è quindi uno scoping stage/logical-ID nel preflight contabile, non una risposta del
provider e non il contenuto del template remediation.

## Esiti per caso

Nessun caso ha raggiunto il transport.

| Caso | Esito remediation | Prompt | Completion | Totale |
|---|---|---:|---:|---:|
| `agent_1` | NOT SENT | 0 | 0 | 0 |
| `agent_2` | NOT SENT | 0 | 0 | 0 |
| `agent_3` | NOT SENT | 0 | 0 | 0 |
| `agent_4` | NOT SENT | 0 | 0 | 0 |
| `agent_5` | NOT SENT | 0 | 0 | 0 |
| `agent_6` | NOT SENT | 0 | 0 | 0 |
| `agent_7` | NOT SENT | 0 | 0 | 0 |
| `agent_8` | NOT SENT | 0 | 0 | 0 |
| **Totale** | **0/8 inviate** | **0** | **0** | **0** |

Non esistono binding, request, response, outcome, journal, summary o validated library per
`producer_remediation`.

## Ledger, quota e chiusura

Il ledger `pilot-03` è passato da
`ce9e6724e64879edab02a8283526c451e4c0a4a94f4b4be12701083479c52522` a
`3690ccfac8a0807d20f1be581325748f392ed777a206ee7c2e8954106df19779` esclusivamente per il
nuovo stop contabile. Conserva 9 request native, 9 response, 9 receipt e 5 richieste di lineage:
il consumo cumulativo resta 14, non raggiunge l'atteso 22 dopo remediation e il massimo
pianificato rimane 166/200.

Il ledger `pilot-001` è invariato, SHA-256
`4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`.
Il controllo conclusivo `lsof` sui due ledger è vuoto; non restano sidecar `pilot-03` né listener
locali sulle porte 8000/8001. Nessun 27B, alternate, retry o resume è stato eseguito.
`server_enea.json` non è stato letto. Nessun raw o segreto viene versionato.

**VERDETTO: REMEDIATION FAIL — READY FOR REVIEW**
