# Evidenza esecuzione finale `pilot-03` — 03.13

Verdetto dell'evidenza: **REGISTRATA — SOLA LETTURA**. Nessuna chiamata, nessun `PilotLedger`, nessuna scrittura sul runtime.

Runtime: `/Users/luker/fot-tep-runtime/studio2-fase03-d9-pilot-03`. Ledger aperto soltanto con `sqlite3` su `file:…/ledger.sqlite3?mode=ro&immutable=1` il 2026-09-17, dopo la chiusura della review `b567` (verbale `VERIFICA_ESITO_PILOT_03_13.md`, SHA-256 `1ce0a466586a65993d1269476f9de8a4812b9f64a20eae71cd9aec7e8bee4b70`). Codice di riferimento: worktree `rem6-riconciliazione`, HEAD `d3f8f844e5be4244477fc294ca754528e6938b15`. Esecutore dell'evidenza: `claude-opus-5` (Claude Cowork), non `gpt-5.6-sol` indicato dal prompt.

## Ledger

| Momento | SHA-256 `ledger.sqlite3` | Fonte |
|---|---|---|
| Prima della revisione config (dopo la sospensione 27B) | `3872029001346913f3722928b350813c8daaef349c5d4fbe98b770200c893fa0` | lettura 03.13-ACC e 03.13-REV27B |
| Finale (dopo il gate, ricomputato ora) | `93ff83a5a4132800c2973fe6687c8e0ffcdb07d33f293a8517ca715ff8dc4089` | `sha256sum`, 4.808.704 byte, `user_version=4`, nessun `-wal`/`-shm` |

I passi eseguiti dal terminale dell'autore non hanno lasciato SHA intermedi del ledger: fra i due valori ci sono revisione, alternate, accettazioni (nessuna scrittura sul ledger), sonda e gate.

## Richieste per stage

| Stage | Modello | Righe | Stati | Quote | Token prompt / completion (completate) | Latenza media / mediana / p95 / max s (completate) | Primo intent → ultimo esito (UTC) |
|---|---|---:|---|---|---:|---|---|
| `technical_qualification_122b` | 122B | 1 | COMPLETED 1 | technical 1 | 42 / 10 | — | 2026-09-16T22:41:53 → 2026-09-16T22:41:54 |
| `producer_conformity` | 122B | 8 | COMPLETED 8 | base 8 | 10.185 / 3.482 | 3,465 / 3,495 / 3,780 / 3,820 | 2026-09-16T23:07:10 → 2026-09-16T23:07:42 |
| `producer_remediation` | 122B | 10 | COMPLETED 8, ZERO_TOKEN_PROVEN 2 | remediation 8, transport 2 | 10.713 / 3.810 | 3,787 / 3,810 / 4,279 / 4,344 | 2026-09-17T10:35:33 → 2026-09-17T10:47:03 |
| `alternate_conformity` | 27B | 14 | COMPLETED 9, ZERO_TOKEN_PROVEN 5 | base 8, requalification 1, transport 5 | 11.622 / 6.595 | 49,334 / 36,015 / 117,897 / 171,664 | 2026-09-17T10:51:43 → 2026-09-17T14:28:04 |
| `budget_probe` | 122B | 3 | COMPLETED 3 | base 3 | 11.868 / 6.411 | 17,206 / 17,410 / 17,783 / 17,824 | 2026-09-17T14:37:44 → 2026-09-17T14:38:38 |
| `stability_gate` | 122B | 120 | COMPLETED 119, FAILED 1 | base 120 | 507.148 / 259.850 | 26,409 / 24,913 / 36,663 / 39,158 | 2026-09-17T14:39:44 → 2026-09-17T15:53:23 |
| **Totale nativo** | | **156** | COMPLETED 148, FAILED 1, ZERO_TOKEN_PROVEN 7 | | | | |

Lineage successor: 5 righe (COMPLETED 3, COMPLETED_IDENTITY_INVALID_ANTECEDENT_CONFIGURATION 1, HISTORICAL_OUTCOME_UNCERTAIN 1). Cumulativo **156+5 = 161**; massimo pianificato 167, hard stop 200. Riserva `remediation`+`transport` = 8+7; `requalification` = 1.

Latenze del gate sulle **120** righe (inclusa la richiesta fallita, come nel verbale `b567`): media 26,209 s, mediana 24,912 s, p95 lineare 36,661 s, totale 3.145,034 s. La tabella sopra usa le sole 119 completate. Le latenze di `technical_qualification_122b` non sono registrate nella colonna `latency_ms`.

### Catene di tentativi

| Stage | Request | Caso | Quota | `retry_of` | Stato | Latenza s | Esito o prova |
|---|---|---|---|---|---|---:|---|
| `producer_remediation` | `7bbd56ff476c…` | agent_1 | remediation | — | ZERO_TOKEN_PROVEN | 0,435 | zero-token, evidenza `a9281b5dbf7e…`, approvazione `a07abcbc8efd…` |
| `producer_remediation` | `dde658fd333e…` | agent_1 | transport | `7bbd56ff…` | ZERO_TOKEN_PROVEN | 0,420 | zero-token, evidenza `186974aff32e…`, approvazione `1e5fca8d90f5…` |
| `producer_remediation` | `2f2d4f1d2c55…` | agent_1 | transport | `dde658fd…` | COMPLETED | 3,893 | finish `stop`, schema valido True, identità valida True |
| `alternate_conformity` | `20938b223df5…` | agent_1 | base | — | ZERO_TOKEN_PROVEN | 0,429 | zero-token, evidenza `2e5f64a1912a…`, approvazione `ab6789ab1867…` |
| `alternate_conformity` | `8e7d1e72f4a2…` | agent_1 | transport | `20938b22…` | ZERO_TOKEN_PROVEN | 0,412 | zero-token, evidenza `504eeb95bd88…`, approvazione `969a755a873e…` |
| `alternate_conformity` | `9bc178d99993…` | agent_1 | transport | `8e7d1e72…` | ZERO_TOKEN_PROVEN | 0,460 | zero-token, evidenza `2b4beb069e6e…`, approvazione `42f651dfca88…` |
| `alternate_conformity` | `39bc1b4c0e86…` | agent_1 | transport | `9bc178d9…` | ZERO_TOKEN_PROVEN | 0,496 | zero-token, evidenza `9e47b92f7d42…`, approvazione `ed20a03e883f…` |
| `alternate_conformity` | `446216bce69e…` | agent_1 | transport | `39bc1b4c…` | ZERO_TOKEN_PROVEN | 0,445 | zero-token, evidenza `28a881a6a849…`, approvazione `c3a19cc14267…` |
| `alternate_conformity` | `19a9b37269be…` | agent_1 | transport | `446216bc…` | COMPLETED | 171,664 | finish `length`, schema valido False, identità valida False |
| `alternate_conformity` | `26919ef29133…` | agent_1 | requalification | `19a9b372…` | COMPLETED | 31,897 | finish `stop`, schema valido True, identità valida True |

Le prove zero-token dei due tentativi remediation riportano HTTP 401 (chiave del producer assente); le cinque dell'alternate riportano `Connection refused` (2) e `Connection reset by peer` (3). Gli altri sette casi di ciascuno stage hanno un solo tentativo.

## Esiti per stage eseguiti dal terminale dopo 03.13-ACC

### Revisione della configurazione (runbook passo 2)

- `config_revision:1`, 2026-09-17T14:21:50 UTC, digest contenuto `4b3e3ae66df67bb33d69585412dc49305592365f97dac0a674ab016606264302`; config file `0c3cd34ef137…` → `c22dca7c70d7e4d8d6044ef9de0c1e4ec03c22059e31e830386b1161b7962075`; approvazione `a8fb92b11ff3e91832ffe260e6c68ace4602415371f1e8bfe639b099fd5b0c08`.
- Foglie cambiate (7): `approved_producer_config_sha256`, `d9.producer_configs.27B`, `d9.services.27B.documentation.path`, `d9.services.27B.documentation.sha256`, `d9.services.27B.expected_response.system_fingerprint`, `execution_authorization.path`, `execution_authorization.sha256`. Il runbook ne elencava 5 raggruppando `documentation` ed `execution_authorization` (rilievo E30 della review REV27B).
- `suspension_reconciled:19a9b37269be…`, 2026-09-17T14:21:50 UTC, approvazione `e5f277cbe7a950ec249d33e5ef6b06da88c5fa619b2eaab2c691e84ca9c8e5d7`, identità osservata `fot-exp2-consumer` / `vllm-0.28.0-5fc21ed4`.
- `stage_rebinding:alternate_conformity:1`, 2026-09-17T14:23:26 UTC, binding `812e18171c18…` → `7cb32fb9a09d17ea38ec8d0d41e5bd97504727d823951544dfbbe8a1a90129f5`.

### Alternate 27B

| Caso | Request | Quota | Latenza s | Token p/c/t | Schema valido | Finish | Reasoning token |
|---|---|---|---:|---|---|---|---:|
| agent_1 | `26919ef29133…` | requalification | 31,897 | 1.397/451/1.848 | True | stop | 0 |
| agent_2 | `7e72bbdc5d44…` | base | 28,611 | 1.018/426/1.444 | True | stop | 0 |
| agent_3 | `5a02c88f28a4…` | base | 37,245 | 1.387/569/1.956 | True | stop | 0 |
| agent_4 | `8d36d3589de7…` | base | 36,485 | 1.331/536/1.867 | True | stop | 0 |
| agent_5 | `06b52437f316…` | base | 34,596 | 1.396/499/1.895 | True | stop | 0 |
| agent_6 | `99397e926242…` | base | 30,469 | 1.068/455/1.523 | True | stop | 0 |
| agent_7 | `41cfce2389cf…` | base | 36,015 | 1.201/548/1.749 | True | stop | 0 |
| agent_8 | `3ee41d6f29f4…` | base | 37,022 | 1.387/551/1.938 | True | stop | 0 |

`outcome:alternate_conformity` PASS, 2026-09-17T14:28:04 UTC, `records_sha256` `baddd67043da38f1a3a176ea52f669564371c2e4618fe4bf3630e8a2695cc759`, 8/8 validi al primo tentativo, `provider_requests` 14.

### Accettazioni pre-gate

`author_acceptances.py --execute` (nessuna scrittura sul ledger): record `execution/PRE_GATE_ACCEPTANCE_03_13.private.json`, `recorded_utc` 2026-09-17T14:35:38Z, autore Luca, censimento senza voci bloccanti, config `c22dca7c…`, authorization rev2 `3d9f4dae…`, inventario congelato `3099ad40…`, manifest `84176888…`, 40 prompt (A/B-LF/E-LF = 8/16/16), piano `READY_FOR_PRE_GATE_GENERATION_PROBE`.

### Sonda budget (122B consumer)

| Prompt | Condizione | Token p/c | Finish | Parsing valido | Latenza s |
|---|---|---|---|---|---:|
| S2-P03-036 | A | 1.406/1.994 | stop | True | 16,385 |
| S2-P03-024 | B-LF | 5.231/2.185 | stop | True | 17,410 |
| S2-P03-025 | E-LF | 5.231/2.232 | stop | True | 17,824 |

Generazione selezionata: seed 20260829, `thinking_token_budget` 2048, `max_tokens` 2560 (primo candidato). `outcome:budget_probe` PASS `records_sha256` `0d94d1987c5a3a797ec8ed7b5ffd538b7a0e6b1beed8290cc1859a93cb389950`; `frozen_gate` `de1f59ceb28e50cd8b9027874f5d2d22cb1337ceab2e4dda8c2adda4b2dda6f2`.

### Gate 40×3

| Condizione | Risposte | Valide al primo tentativo | Astensioni | Token prompt medi | Token completion medi | Latenza media s |
|---|---:|---:|---:|---:|---:|---:|
| A | 24 | 24 | 6 | 1.201 | 2.076 | 24,379 |
| B-LF | 47 | 47 | 18 | 5.035 | 2.204 | 26,709 |
| E-LF | 48 | 48 | 12 | 5.035 | 2.217 | 27,131 |

Richiesta fallita: `28fe698d3d8a…`, `S2-P03-002:r2`, `APIConnectionError: Connection error.`, registrata come `transport_invalidity` (nessun retry). Finish reason delle 119 risposte: `stop` 119. `reasoning_tokens` non esposto nelle risposte del consumer.

`outcome:stability_gate` (2026-09-17T15:53:42 UTC): 120 richieste, 119 valide, 1 non valida, troncamenti 0, T3 True, T4 True, T6 valutabile True, divergenti ['S2-P03-002'], stato `R3_REQUIRED_PENDING_FEASIBILITY`, `go_final` False, `records_sha256` `bd9713eca7c3241c002d24a2ebf480f0255e5da82534289eb6cfb658d0e2f9a2`.

## Identità

- `qwen3.5-122b` / `vllm-0.27.1-934a3247`: 139 risposte
- `fot-exp2-consumer` / `vllm-0.28.0-5fc21ed4`: 9 risposte

## Eventi di riconciliazione e approvazioni

| Evento | UTC | `artifact_sha256` | SHA approvazione |
|---|---|---|---|
| `successor_lineage:ee5a2aa58b90e85a8482a6…` | 2026-09-16T21:18:22 | `ee5a2aa58b90e85a8482a66540b4c39f6c6e5229c054434ba3e750b9cd5b07e6` | `fbda6b463809ed309bcb933cf15cc0f2c01b03d15a783dfb1017df154fc58516` |
| `outcome:technical_qualification_122b` | 2026-09-16T22:41:54 | `cdf5247d6cd6aa5c36e254edf2dcdd3b919b375ec0343429f12c0e86f149b672` | — |
| `outcome:producer_conformity` | 2026-09-16T23:07:43 | `b75e42da4c700fb808cc23c6ff8a42e9927166d98f6a96277e629ef216d4e0f1` | — |
| `diagnosis:producer_conformity` | 2026-09-17T07:44:09 | `3bfba0d781dca4bb9d359d089cbd3948a4583ab99afc5df1ac0f8f7de32bb3e2` | `3bfba0d781dca4bb9d359d089cbd3948a4583ab99afc5df1ac0f8f7de32bb3e2` |
| `remediation_authorized` | 2026-09-17T07:45:47 | `5469d14c7f1462b2f4c606705d891f4e5dffad927cd79b2829ba9f61a6193b6f` | — |
| `stop:tokenizer_accounting` | 2026-09-17T07:58:20 | `d02464d2937cc7d5f31038b40478bfe0b547112c277371da5c1b2d3b37dbc54a` | — |
| `stop_reconciled:tokenizer_accounting` | 2026-09-17T10:33:55 | `d02464d2937cc7d5f31038b40478bfe0b547112c277371da5c1b2d3b37dbc54a` | `2b0f28dcf22a4d976a6ced1c0e1b12f617ca467352df2d8fd206817433d639bf` |
| `reconciled:7bbd56ff476ce612db13f6e43f8e9…` | 2026-09-17T10:42:19 | `a9281b5dbf7e3ff77e4dc36a3ae508cfbe0a4690a90a65868b0e8b539110bba8` | `a07abcbc8efd5ba6cf9e6cdcd55a28d545c3d5c2a90b93a1fb383712bef956f9` |
| `reconciled:dde658fd333ed614ab33a295f72af…` | 2026-09-17T10:45:13 | `186974aff32e914c47e2c85aeab6b7cfa644c5cfbb77614bdea3f919c2e4cbcb` | `1e5fca8d90f575a4d4a9e523ffb0213823abcfa64dce52ccae7378a207c25a88` |
| `outcome:producer_remediation` | 2026-09-17T10:47:03 | `3b2ec2da7ce52e3e38642b6991a96f29e9474316db98d80616a45322ac5f41a1` | — |
| `reconciled:20938b223df536de1a0d60db604de…` | 2026-09-17T10:53:47 | `2e5f64a1912a3b123df92f7e10575e4be72b854cc070a25860a3e2547bf1bc24` | `ab6789ab1867fd37e2a435444227dbbd298f09877751a9a376170e4bd0badfaf` |
| `reconciled:8e7d1e72f4a2751aa5d062e0e12e0…` | 2026-09-17T10:55:37 | `504eeb95bd888bfeb471e90b230ecec1ed2a9c55328a614dafff89afdbc831dc` | `969a755a873ea3feb89123b677f244b88a55701c766b8578dde3459b806ae38c` |
| `reconciled:9bc178d9999313704cd963e9b2c92…` | 2026-09-17T11:03:03 | `2b4beb069e6e6eb5b7a1abc93a051e464867c49f780333a33d1bb59b9cb3d43f` | `42f651dfca88ad7c09cb928f089991f8446cf92f54a2970c93cdc566f9d3b370` |
| `reconciled:39bc1b4c0e8688634fe9220780888…` | 2026-09-17T11:17:07 | `9e47b92f7d42bc62a99bb494af66279823d746b1577eb037ec30952a62df7b40` | `ed20a03e883fe1bda2dcd995c4d1dc943f5bc66de410d162212fa4b476596a40` |
| `reconciled:446216bce69e747d78de900d1f049…` | 2026-09-17T11:17:31 | `28a881a6a8498c8b919dec4faaa330f35c198735ae179f89f5b3c97cfaf8d849` | `c3a19cc14267227a734d3095b76179ce9e1f2369466a7b743c96173614535b6e` |
| `suspended:19a9b37269bede1b62799cf3ac5819…` | 2026-09-17T11:21:23 | `59de0821f1a92b114ac4fcf25e643ad7c6c261bdf6ea769a592e420a80993893` | — |
| `config_revision:1` | 2026-09-17T14:21:50 | `4b3e3ae66df67bb33d69585412dc49305592365f97dac0a674ab016606264302` | `a8fb92b11ff3e91832ffe260e6c68ace4602415371f1e8bfe639b099fd5b0c08` |
| `suspension_reconciled:19a9b37269bede1b62…` | 2026-09-17T14:21:50 | `59de0821f1a92b114ac4fcf25e643ad7c6c261bdf6ea769a592e420a80993893` | `e5f277cbe7a950ec249d33e5ef6b06da88c5fa619b2eaab2c691e84ca9c8e5d7` |
| `stage_rebinding:alternate_conformity:1` | 2026-09-17T14:23:26 | `7cb32fb9a09d17ea38ec8d0d41e5bd97504727d823951544dfbbe8a1a90129f5` | — |
| `outcome:alternate_conformity` | 2026-09-17T14:28:04 | `9d09c41540a6e3299a286fc76f551252cbe838674f0505144a442179621fe70e` | — |
| `outcome:budget_probe` | 2026-09-17T14:38:39 | `19a8306c3cb255bce6258084be45dd94bbaf0931ea78aedbbd18b7f76271284b` | — |
| `frozen_gate` | 2026-09-17T14:38:39 | `de1f59ceb28e50cd8b9027874f5d2d22cb1337ceab2e4dda8c2adda4b2dda6f2` | — |
| `outcome:stability_gate` | 2026-09-17T15:53:42 | `99cad68deab2bcd71d7766c1ec2e7dde76fe28bc4fdff973be69cc8bb86aad58` | — |

Conteggio eventi: 309 (`config_revision` 1, `diagnosis` 1, `frozen_gate` 1, `outcome` 6, `reconciled` 7, `reconciled_integrity` 7, `remediation_authorized` 1, `stage_rebinding` 1, `stop` 1, `stop_reconciled` 1, `successor_lineage` 1, `suspended` 1, `suspension_reconciled` 1, `tokenizer_accounting` 139, `tokenizer_accounting_record` 139, `transport_invalidity` 1).

## File del runtime (path e SHA-256, nessun contenuto)

Tutti i file tranne `tokenizers/` (asset pinnati altrove) e il ledger. Il contenuto resta fuori da Git.

| Path relativo al runtime | Byte | SHA-256 |
|---|---:|---|
| `MATERIALIZATION_SUMMARY.private.json` | 2.154 | `30021bc4d91a070058f268e99f1ef5c1df3afce61691e7e5aed86c040d7e2cee` |
| `execution/PILOT_INPUT_MANIFEST.frozen.json` | 327.061 | `8417688869b75bda8235387ac830018ecdc9030442a860d495418f195f2b4014` |
| `execution/PILOT_INPUT_SOURCES.frozen.json` | 195.164 | `3099ad40ed05d86dab9b69349a2e0a920eb8bbeb8006be3223db6f6438429bbf` |
| `execution/PRE_GATE_ACCEPTANCE_03_13.private.json` | 3.580 | `491fe5339cd4ba935ff43c9b78883714527c1120bbc471edd95766946c671649` |
| `execution/accounting_stop_reconciliation_03_13.private.json` | 417 | `2b0f28dcf22a4d976a6ced1c0e1b12f617ca467352df2d8fd206817433d639bf` |
| `execution/alternate_accounting_approval.private.json` | 120 | `05786ff7893491742bda7f135cf36e1ee3e19998afa155ba21a204b42a46b6d2` |
| `execution/config_revision_01_03_13.private.json` | 421 | `a8fb92b11ff3e91832ffe260e6c68ace4602415371f1e8bfe639b099fd5b0c08` |
| `execution/pilot_d9_successor_candidate_03_13.private.json` | 16.899 | `c22dca7c70d7e4d8d6044ef9de0c1e4ec03c22059e31e830386b1161b7962075` |
| `execution/pilot_d9_successor_candidate_03_13.private.json.pre_authorization` | 16.724 | `6f8d616c1f75596ddff480b6bd4c01481adb85343c99205ea2a51d129c99da4f` |
| `execution/pilot_d9_successor_candidate_03_13.private.json.pre_rev2` | 16.871 | `0c3cd34ef137cae4388e7868e4aa1e8d9bf494ab563fcabbdbcdc66bc7fe0606` |
| `execution/presentation_approval.private.json` | 116 | `5b1bf8b6f558e34c034c58773b82223f7a70a570195db863cecb08e50829cacb` |
| `execution/presentation_order_approval.private.json` | 1.009 | `0f9f7b7f4036bd4172467dba80673af5d9ec3abb2bb854d6239da7ccec2977d1` |
| `execution/producer_122b_successor_03_13.private.json` | 999 | `04b2c948c586c9ae4e38d9d0c50d36aad86a5b609a609d94c2d31fde7c2a8bf0` |
| `execution/producer_27b_successor_03_13.private.json` | 808 | `fcecc53417d8c35319c11bf7a633b70456d3c85b90f51d7193490cae99baa4e4` |
| `execution/producer_27b_successor_03_13.rev2.private.json` | 883 | `27295c25f6a2d08730781d8e24053be74ce593434cbe8c80e6324145469c34c0` |
| `execution/producer_failure_diagnosis_03_13.private.json` | 167 | `3bfba0d781dca4bb9d359d089cbd3948a4583ab99afc5df1ac0f8f7de32bb3e2` |
| `execution/producer_template_remediation_03_13.diff` | 1.192 | `7bbe19745179b90e57d8a80c2c362b1b0449d99474799f2273baae952a7a2f5f` |
| `execution/producer_template_remediation_03_13.txt` | 1.280 | `4306c5da6f0ebefcbce75d26d585caf82cc05ff85d5e7e6639e3f65b2d66de12` |
| `execution/remediation_approval_03_13.private.json` | 349 | `5469d14c7f1462b2f4c606705d891f4e5dffad927cd79b2829ba9f61a6193b6f` |
| `execution/service_122b_successor_03_13.private.json` | 3.320 | `714c24bf14e525c73c4ff839f3a102b5a9dbeb36a85be986a0439b91bd1b3469` |
| `execution/service_27b_successor_03_13.private.json` | 2.219 | `133807dfa57ddbd7a4319bfbdd2b851f0648928c12195422ee300b0e17d4f485` |
| `execution/service_27b_successor_03_13.rev2.private.json` | 2.237 | `7b3496a4b6e7d135f025175bf7204675830fc2aa528ed2494e84608c995e4ed6` |
| `execution/suspension_reconciliation_03_13.private.json` | 450 | `e5f277cbe7a950ec249d33e5ef6b06da88c5fa619b2eaab2c691e84ca9c8e5d7` |
| `execution/technical_execution_authorization_03_13.private.json` | 308 | `7dcec1055696fa26b9baad40f1937f4ca55dc450a9f277ca9b01271b6ff1c875` |
| `execution/technical_execution_authorization_03_13.rev2.private.json` | 400 | `3d9f4daec3a8fee7acd24d1a06ae81b91e8790b760671059b268f59cd4669a60` |
| `execution/zero_token_approval_20938b223df536de1a0d60db604de36cf548f9848316ad3d690bb8b3710726ac.private.json` | 138 | `ab6789ab1867fd37e2a435444227dbbd298f09877751a9a376170e4bd0badfaf` |
| `execution/zero_token_approval_39bc1b4c0e8688634fe922078088845629cb8a0588005cd438de68fa7839b5f8.private.json` | 138 | `ed20a03e883fe1bda2dcd995c4d1dc943f5bc66de410d162212fa4b476596a40` |
| `execution/zero_token_approval_446216bce69e747d78de900d1f0496e82d21ecc455e7b937d54c9a1863526eed.private.json` | 138 | `c3a19cc14267227a734d3095b76179ce9e1f2369466a7b743c96173614535b6e` |
| `execution/zero_token_approval_7bbd56ff476ce612db13f6e43f8e90492fe99d71378c053355f027cf14da426e.private.json` | 138 | `a07abcbc8efd5ba6cf9e6cdcd55a28d545c3d5c2a90b93a1fb383712bef956f9` |
| `execution/zero_token_approval_8e7d1e72f4a2751aa5d062e0e12e0899b6892f02fc60e3b4e942ada91f9ca14c.private.json` | 138 | `969a755a873ea3feb89123b677f244b88a55701c766b8578dde3459b806ae38c` |
| `execution/zero_token_approval_9bc178d9999313704cd963e9b2c92a1ecdf42dd21330f50ff57e35b2a103ab9d.private.json` | 138 | `42f651dfca88ad7c09cb928f089991f8446cf92f54a2970c93cdc566f9d3b370` |
| `execution/zero_token_approval_dde658fd333ed614ab33a295f72af3a3be7073aef4e7baeeec749abab07f1f71.private.json` | 138 | `1e5fca8d90f575a4d4a9e523ffb0213823abcfa64dce52ccae7378a207c25a88` |
| `execution/zero_token_evidence_20938b223df536de1a0d60db604de36cf548f9848316ad3d690bb8b3710726ac.private.json` | 410 | `2e5f64a1912a3b123df92f7e10575e4be72b854cc070a25860a3e2547bf1bc24` |
| `execution/zero_token_evidence_39bc1b4c0e8688634fe922078088845629cb8a0588005cd438de68fa7839b5f8.private.json` | 422 | `9e47b92f7d42bc62a99bb494af66279823d746b1577eb037ec30952a62df7b40` |
| `execution/zero_token_evidence_446216bce69e747d78de900d1f0496e82d21ecc455e7b937d54c9a1863526eed.private.json` | 422 | `28a881a6a8498c8b919dec4faaa330f35c198735ae179f89f5b3c97cfaf8d849` |
| `execution/zero_token_evidence_7bbd56ff476ce612db13f6e43f8e90492fe99d71378c053355f027cf14da426e.private.json` | 428 | `a9281b5dbf7e3ff77e4dc36a3ae508cfbe0a4690a90a65868b0e8b539110bba8` |
| `execution/zero_token_evidence_8e7d1e72f4a2751aa5d062e0e12e0899b6892f02fc60e3b4e942ada91f9ca14c.private.json` | 410 | `504eeb95bd888bfeb471e90b230ecec1ed2a9c55328a614dafff89afdbc831dc` |
| `execution/zero_token_evidence_9bc178d9999313704cd963e9b2c92a1ecdf42dd21330f50ff57e35b2a103ab9d.private.json` | 422 | `2b4beb069e6e6eb5b7a1abc93a051e464867c49f780333a33d1bb59b9cb3d43f` |
| `execution/zero_token_evidence_dde658fd333ed614ab33a295f72af3a3be7073aef4e7baeeec749abab07f1f71.private.json` | 428 | `186974aff32e914c47e2c85aeab6b7cfa644c5cfbb77614bdea3f919c2e4cbcb` |
| `lineage/SUCCESSOR_LINEAGE_S5_122B_QWEN_D9_03_13.approval.private.json` | 631 | `fbda6b463809ed309bcb933cf15cc0f2c01b03d15a783dfb1017df154fc58516` |
| `lineage/SUCCESSOR_LINEAGE_S5_122B_QWEN_D9_03_13.private.json` | 6.195 | `ee5a2aa58b90e85a8482a66540b4c39f6c6e5229c054434ba3e750b9cd5b07e6` |
| `prepared/pilot_prompts.jsonl` | 569.792 | `efd43620603b9c26dbbcc986ec80b663937fd48c05b82f2cb7406dadb61cf298` |
| `prepared/pre_gate_hashes.json` | 729 | `a80fb83501eaf5c0febc4a3bd8d64d9118c16ee6ac0d94d6e122b4b73a17d4a6` |
| `prepared/pre_gate_plan.json` | 3.764 | `b83c88ea1206efb22603691f04045f260ee4f5d64f0cdb7585a9de881b73e856` |
| `qualification/QUALIFICATION_SUPPLEMENT_122B_QWEN_D9_03_13.private.json` | 1.156 | `dd9c53f0e4262fffe592a04298f8d7a4cfd428ccf5c487faacfe68ca357decb7` |
| `qualification/technical_qualification_122b_journal.json` | 250 | `f6e44bd4e7680eabdc17a2fc72a9afb376c78ba419bd3ca52e6182c4288be60b` |
| `qualification/technical_qualification_122b_summary.json` | 240 | `3a3eaf15b6208eb86a697dcc9683677c39bc02d161529317c1a8a3cf8b33210d` |
| `results/alternate_20260917T125137.log` | 6.716 | `3a3dce5f237852aff1b610a684269521eb49c7a2c2d30fbe30526a8d41b230bd` |
| `results/alternate_20260917T125401.log` | 6.716 | `3a3dce5f237852aff1b610a684269521eb49c7a2c2d30fbe30526a8d41b230bd` |
| `results/alternate_20260917T125847.log` | 2.342 | `7a5ea6e5620d8fb17dfee42d1f77e540772031cf7949ef8b51fd33788b63dbf6` |
| `results/alternate_20260917T130137.log` | 7.186 | `51ec601a1e1299d6fe5131f1c4d22cf861684e0658d7c740702d56aa2139817d` |
| `results/alternate_20260917T130331.log` | 7.186 | `51ec601a1e1299d6fe5131f1c4d22cf861684e0658d7c740702d56aa2139817d` |
| `results/alternate_20260917T131707.log` | 7.186 | `51ec601a1e1299d6fe5131f1c4d22cf861684e0658d7c740702d56aa2139817d` |
| `results/alternate_20260917T131826.log` | 1.977 | `4ec50de572aa168b15d118d158a0f04c98251adb2c8b2cdddd571964ed3d9831` |
| `results/alternate_20260917T162321.log` | 464 | `2ab25de107bca6c388edfe38840660ad16c09dc2f73d0a2d1e4fb18d8b139428` |
| `results/budget_20260917T163729.log` | 580.853 | `0a66edbdeba2eb190b589432816310242061d4177a7126101cadd595da04772e` |
| `results/budget_probe_journal.jsonl` | 31.709 | `33d030228e3731f55fe16a69b497715d6134527d0db7f793e254b2b42897f2be` |
| `results/budget_probe_records.jsonl` | 5.206 | `975733a660f91d30963f79bba3319b7cc111cdc335a0ad2725918bda2d912959` |
| `results/frozen_gate_config.json` | 593.425 | `709ae3400238b3ecdf50ef5b7d377b0bea4fdf87fcec569994d24cace39fa8ac` |
| `results/producer_alternate_conformity_journal.jsonl` | 45.962 | `4d0e7c3c303f5ea59ad750820cbf0074d545d62c0e5688c9f0d73913e0938afb` |
| `results/producer_conformance_qwen_122b_primary_producer_conformity_summary.json` | 503 | `d38d51d8d5532869a05ee7c049b832ef7e7dcaf5e87028391e2c7ee384aaafd4` |
| `results/producer_conformance_qwen_122b_primary_producer_remediation_summary.json` | 505 | `b5a789a0e6a46a1c9b3b7779a88bedf163b3bf3774c22e9842df18c673bf6d9a` |
| `results/producer_conformance_qwen_27b_alternate_alternate_conformity_summary.json` | 505 | `90da146a3c44b870820db631896c32e14b97e718d167358081826ed14bee244b` |
| `results/producer_producer_conformity_journal.jsonl` | 44.735 | `bd367c14018838732ab99b968e55c32219f883db954911ad9f322abdabf10836` |
| `results/producer_producer_remediation_journal.jsonl` | 46.220 | `fc3f216d98c3dffe24ce5e6ccb4d11d16184daa30e941a757a146757f833082a` |
| `results/remediation_20260917T123528.log` | 3.452 | `9b985a8df83bbbcacb9262d4b9534a140204f126f9a6798d035d5294d6599940` |
| `results/remediation_20260917T123723.log` | 1.914 | `23a38ff77e3dffd93de150374107df635e1657036b144d7acc5322a9ff997d58` |
| `results/remediation_20260917T123804.log` | 1.928 | `ac1e027df7e19c601dc8a48fab281fe822bf5504537a88fb8d472f44538bf9b6` |
| `results/remediation_20260917T124316.log` | 3.452 | `9b985a8df83bbbcacb9262d4b9534a140204f126f9a6798d035d5294d6599940` |
| `results/remediation_20260917T124623.log` | 464 | `90a0316153cce3691998f0ce4fa52e4fca3314d762222e38035d4508fcd9c264` |
| `results/stability_20260917T163928.log` | 628 | `4081a03e0200a4cf004ec9700be5423587aa3f2d605aa8673f4e73a5b6a2d13b` |
| `results/stability_journal.jsonl` | 1.285.888 | `2f0a7b6f8bf433d063c719dd482e966d691439a77b2503f58446739b86e42e6c` |
| `results/stability_records.jsonl` | 235.143 | `dde3f7de3c88bdee4844d14d3dd82daedd5e8fe7df70c465f1d3708c6f440ea6` |
| `results/stability_summary.json` | 726 | `efa627413ee2838141fea4508a76974821cd50838db4137497f5590fbcb6a508` |
| `results/validated_insight_library_qwen_122b_primary_producer_remediation.json` | 13.755 | `1e97ddd3525c414f6d5ddd240e98d358720937e912edb4e27644374e8b2eea09` |
| `results/validated_insight_library_qwen_27b_alternate_alternate_conformity.json` | 13.479 | `c697e803be178235c37d37caf7ec1ef65a0761db44e097f2d422e7498eef73c9` |

## Log dei run

Copiati in `harness/logs_pilot_03_finale/`. Nessun segreto trovato (ricerca di chiavi, `Bearer`, `api_key`). Il log della sonda contiene il `frozen_gate_config` con i 40 testi dei prompt e `true_pseudolabel` lato valutatore: `prompt_sample` è stato sostituito da conteggio e digest canonico. Indice: `REDACTION_INDEX.json`.

| Log | Esito | Byte sorgente | SHA-256 sorgente | Redazione |
|---|---|---:|---|---|
| `alternate_20260917T125137.log` | connection refused, `20938b22` | 6.716 | `3a3dce5f237852aff1b610a684269521eb49c7a2c2d30fbe30526a8d41b230bd` | none (byte-identical) |
| `alternate_20260917T125401.log` | connection refused, `8e7d1e72` | 6.716 | `3a3dce5f237852aff1b610a684269521eb49c7a2c2d30fbe30526a8d41b230bd` | none (byte-identical) |
| `alternate_20260917T125847.log` | rifiuto pre-trasporto: byte della config producer cambiati, nessuna request | 2.342 | `7a5ea6e5620d8fb17dfee42d1f77e540772031cf7949ef8b51fd33788b63dbf6` | none (byte-identical) |
| `alternate_20260917T130137.log` | connection reset, `9bc178d9` | 7.186 | `51ec601a1e1299d6fe5131f1c4d22cf861684e0658d7c740702d56aa2139817d` | none (byte-identical) |
| `alternate_20260917T130331.log` | connection reset, `39bc1b4c` | 7.186 | `51ec601a1e1299d6fe5131f1c4d22cf861684e0658d7c740702d56aa2139817d` | none (byte-identical) |
| `alternate_20260917T131707.log` | connection reset, `446216bc` | 7.186 | `51ec601a1e1299d6fe5131f1c4d22cf861684e0658d7c740702d56aa2139817d` | none (byte-identical) |
| `alternate_20260917T131826.log` | sospensione per identità, `19a9b372` | 1.977 | `4ec50de572aa168b15d118d158a0f04c98251adb2c8b2cdddd571964ed3d9831` | none (byte-identical) |
| `alternate_20260917T162321.log` | PASS 8/8 dopo la revisione | 464 | `2ab25de107bca6c388edfe38840660ad16c09dc2f73d0a2d1e4fb18d8b139428` | none (byte-identical) |
| `budget_20260917T163729.log` | `FROZEN_FOR_STABILITY_GATE` | 580.853 | `0a66edbdeba2eb190b589432816310242061d4177a7126101cadd595da04772e` | prompt_sample redacted |
| `remediation_20260917T123528.log` | 401, prova zero-token `7bbd56ff` | 3.452 | `9b985a8df83bbbcacb9262d4b9534a140204f126f9a6798d035d5294d6599940` | none (byte-identical) |
| `remediation_20260917T123723.log` | rifiuto: serve `--resume` | 1.914 | `23a38ff77e3dffd93de150374107df635e1657036b144d7acc5322a9ff997d58` | none (byte-identical) |
| `remediation_20260917T123804.log` | rifiuto: intent incerto da riconciliare | 1.928 | `ac1e027df7e19c601dc8a48fab281fe822bf5504537a88fb8d472f44538bf9b6` | none (byte-identical) |
| `remediation_20260917T124316.log` | 401, prova zero-token `dde658fd` | 3.452 | `9b985a8df83bbbcacb9262d4b9534a140204f126f9a6798d035d5294d6599940` | none (byte-identical) |
| `remediation_20260917T124623.log` | PASS 8/8 | 464 | `90a0316153cce3691998f0ce4fa52e4fca3314d762222e38035d4508fcd9c264` | none (byte-identical) |
| `stability_20260917T163928.log` | `R3_REQUIRED_PENDING_FEASIBILITY` | 628 | `4081a03e0200a4cf004ec9700be5423587aa3f2d605aa8673f4e73a5b6a2d13b` | none (byte-identical) |

I passi di revisione (`revise_pilot_config.py`) e di accettazione (`author_acceptances.py`) non hanno un file di log nel runtime: sono documentati dagli eventi e dal record sopra.

## Limiti

- `lsof` non è eseguibile da questa sessione: la precondizione è coperta dal verbale `b567` (lsof vuoto al termine) e dall'assenza di `-wal`/`-shm`; il ledger ha lo stesso SHA del verbale.
- `pilot-001` e `pilot-002` non sono stati aperti: i loro SHA sono quelli del verbale `b567` §9.
- Latenze e token sono letti dal ledger; nessun valore è stato ricalcolato dalle risposte grezze oltre a identità e `reasoning_tokens`.
