# Evidenza T9 — conformità producer 122B su `pilot-03`

Verdetto: **T9 PRODUCER STOPPED AT 8 — READY FOR REVIEW**.

Data: 17 settembre 2026, Europe/Rome. È stata eseguita una sola invocazione del runner T9
`producer_conformity`, senza `--retry-request`, `--resume`, remediation, alternate o 27B.
L'harness ha completato e contabilizzato gli otto casi congelati: sei sono validi al primo
tentativo e due hanno fallito la validazione degli identificatori. L'outcome durevole è `FAIL`.

## Pre-condizioni

- HEAD `294f154fd4e2748d0083030278939eb8ac12bd55`, tree
  `2c4923b1414c737f0ca43473de00ee32d417f2bd`;
- review indipendente della qualifica tecnica: `TECHNICAL PASS CONFIRMED`, SHA-256
  `f4ee983b9c0f9f7974d06a39f955c67db88a9f57eb29a0a8d0e4182634101db0`;
- config autorizzata SHA-256
  `0c3cd34ef137cae4388e7868e4aa1e8d9bf494ab563fcabbdbcdc66bc7fe0606`;
- provider 122B SHA-256
  `04b2c948c586c9ae4e38d9d0c50d36aad86a5b609a609d94c2d31fde7c2a8bf0`;
- inventario degli otto casi SHA-256
  `7103482d6c7b8038944b0af63bac58548557c8d0b8f5d24e420346bd93fa304b`;
- template producer congelato SHA-256
  `e7e80d59b2def37bea8f20186fc297583e2c8b0dea390a3351c7843d841619e7`;
- manifest schema R4 SHA-256
  `d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`;
- ledger `pilot-03` iniziale SHA-256
  `619a66c7bb81477e302a362ebbaf7bae96adb98411a532f9ae9b9465ab52c801`;
- ledger `pilot-001` SHA-256
  `4802d7918dc063d198b799c367a9300c4ba11685cc37487c862e8a2f47bcc1eb`;
- `lsof` iniziale vuoto sulle due famiglie SQLite; nessun sidecar `pilot-03`.

Il preflight offline ha autenticato config, provider, inventario, schema, tokenizer e template;
ha costruito esattamente otto prompt. Il conteggio chat locale era compreso tra 1016 e 1395
token, con margine di contesto minimo 127117 token.

`/v1/models` ha confermato `qwen3.5-122b`, root `Qwen/Qwen3.5-122B-A10B-FP8` e capienza 131072;
`/version` ha confermato vLLM 0.27.1. Il fingerprint esatto
`vllm-0.27.1-934a3247` era legato alla qualifica tecnica durevole e revisionata ed è stato poi
osservato identico in tutte le otto risposte T9.

## Esecuzione unica

Il wrapper effettivo è iniziato alle `2026-09-16T23:07:05Z` ed è terminato alle
`2026-09-16T23:07:43Z`; `/opt/anaconda3/bin/python3`, CPython 3.13.9 arm64, exit code 2. Un primo
tentativo di costruire il comando è stato respinto localmente prima della creazione del processo,
dell'intent e del trasporto perché includeva una pulizia non ammessa: non costituisce
un'invocazione del runner né una richiesta provider.

La credenziale è stata letta in memoria e passata esclusivamente tramite variabile d'ambiente;
non è stata stampata né inserita nell'argv. Il template temporaneo conteneva esattamente i byte
congelati ed è stato eliminato automaticamente dal wrapper al termine.

## Esiti per caso

| Caso | Primo tentativo | Errore | Prompt | Completion | Totale |
|---|---|---|---:|---:|---:|
| `agent_1` | PASS | — | 1397 | 390 | 1787 |
| `agent_2` | FAIL | `identifiers`: malformed variable identifier | 1018 | 466 | 1484 |
| `agent_3` | FAIL | `identifiers`: literal references required and must be declared | 1387 | 478 | 1865 |
| `agent_4` | PASS | — | 1331 | 416 | 1747 |
| `agent_5` | PASS | — | 1396 | 413 | 1809 |
| `agent_6` | PASS | — | 1068 | 391 | 1459 |
| `agent_7` | PASS | — | 1201 | 486 | 1687 |
| `agent_8` | PASS | — | 1387 | 442 | 1829 |
| **Totale T9** | **6/8 PASS** | **2 FAIL** | **10185** | **3482** | **13667** |

Tutte le request sono `COMPLETED`, senza `retry_of`; tutte le risposte hanno modello
`qwen3.5-122b`, fingerprint `vllm-0.27.1-934a3247`, identità valida e finish reason `stop`.
Non si è verificato alcun errore di trasporto.

## Evidenza durevole e accounting

La verifica conclusiva è stata eseguita con SQLite `mode=ro&immutable=1`, senza costruire
`PilotLedger`:

- binding `producer_conformity` per otto request, SHA-256
  `83863085938bea35ee70cbec86e88365e7e94f95e6e17b576994635367ffd5be`;
- otto request, otto response e otto receipt T9;
- summary `FAIL`, 8 richieste provider, 8 risposte valutabili, 6 valide al primo tentativo;
- `records_sha256`
  `500c1c4f60ac7761514bb1311349210d7a9cfb3abf12b952fe4a2bc32ef7ad82`;
- outcome durevole `FAIL`, SHA-256
  `b75e42da4c700fb808cc23c6ff8a42e9927166d98f6a96277e629ef216d4e0f1`;
- nessuna validated insight library prodotta.

Il summary privato ha SHA-256
`d38d51d8d5532869a05ee7c049b832ef7e7dcaf5e87028391e2c7ee384aaafd4`; il journal privato
ha SHA-256 `bd367c14018838732ab99b968e55c32219f883db954911ad9f322abdabf10836`.
Il raw delle risposte non è versionato.

Il ledger contiene ora nove richieste native locali: una qualifica tecnica e otto T9. Insieme
alle cinque richieste della lineage predecessore, il consumo cumulativo ricostruito è 14
richieste provider. Il massimo cumulativo pianificato resta `166/200`, con margine pianificato
34; rispetto all'hard stop restano attualmente 186 richieste. Nessun retry è stato consumato.

Il ledger `pilot-03` finale ha SHA-256
`744b832fe43be66b57a70e5be587a9e566befbcce6f50321ea3e778db348c33b`.
Il ledger `pilot-001` è invariato. `lsof` conclusivo è vuoto e `pilot-03` non ha sidecar.

## Limiti e arresto

Come prescritto, dopo il `FAIL` non sono stati eseguiti `--retry-request`, `--resume` o
`producer_remediation`. Nessuna chiamata 27B o alternate. Il tunnel 27B preesistente, dichiarato
attivo dall'autore, non è stato usato o modificato; il 122B è stato raggiunto direttamente sulla
VPN. `server_enea.json` non è stato letto. Nessun segreto, raw response o insight privato è
incluso nel repository.

**VERDETTO: T9 PRODUCER STOPPED AT 8 — READY FOR REVIEW**
