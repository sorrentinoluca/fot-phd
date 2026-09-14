# Acquisizione della verifica del consolidamento 03.15 e raccordo metriche

Data: 2026-09-14, Europe/Rome. Questo record acquisisce il verbale `VERDETTO: OK`
del solo candidato tecnico `04dee86140b3ff18882f9d164beef5ab7bf33e00` e le prove
inventariate dal revisore. Non costituisce una nuova verifica e non amplia il verdetto.

## Riferimenti Git e acquisizione

| Voce | Valore |
| --- | --- |
| Candidato esatto qualificato | `04dee86140b3ff18882f9d164beef5ab7bf33e00` |
| Commit successivo di consegna | `380d162390048e8a7e9e9884b4e932867e63a821`, figlio diretto del candidato |
| Commit locale di acquisizione | `770d17ccfcc62d08be56be54c7f08e5b26ce40a9` |
| Branch destinatario | `codex/studio2-consolidamento-0315-metriche` |
| Worktree destinatario | `/Users/luker/fot-tep-consolidamento-0315-metriche` |
| `origin/main` al preflight | `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`, confermato con lettura remota |

Prima della scrittura il branch era pulito a `380d162`. Il commit aveva un unico
genitore, esattamente `04dee86`, e il suo delta conteneva soltanto la consegna e il
prompt di verifica. Il verbale nomina esplicitamente `04dee86` come candidato tecnico
verificato. Nessun checkout, lock o worktree altrui è stato spostato o riparato.

L'acquisizione è il solo commit `770d17c`: aggiunge il verbale e la directory
`evidenze_verifica_consolidamento_04dee86`, senza modificare file già tracciati. La
consegna precedente, il prompt, i pacchetti verificati, i manifest storici e i verbali
precedenti non sono stati riscritti.

## Identità attestate e limiti

Il verbale identifica il revisore come provider `openai`, prodotto Codex Desktop,
modello esposto `gpt-6-astra`, `effort=high`, sessione
`01a0a0e2-5a0b-7bc3-a111-b41f24734216`. Identifica l'esecutore del consolidamento
come provider `openai`, modello `gpt-5.6-sol`, `effort=high`, sessione
`01a0a0b9-fc72-79b1-81b4-a4d5daa38f94`. Il record conserva soltanto il livello di
identità attestato dal verbale e non deduce dati ulteriori per l'esecutore della presente
acquisizione.

Resta inoltre dichiarata l'identità incompleta del precedente revisore metriche E:
il documento E espone soltanto OpenAI Codex, modello basato su GPT-5; ID di
sessione/task, modello preciso ed effort non sono verificabili dalle fonti acquisite.
Il presente OK non certifica né completa tale identità.

## Perimetro dell'OK

L'OK è limitato a genealogia/raccordo, conservazione, acquisizioni e isolamento del
test mirato del candidato esatto. Non si estende all'harness completo, non ripete gli
OK scientifici precedenti e non chiude le sottofasi aperte. Il guardiano documentale
resta una suite con **14 failure storici e uno skip**, non una suite PASS.

La precisazione tipografica da conservare è: **tre siti di intervento, sei caratteri
U+0020 aggiunti, uno prima e uno dopo ciascuna freccia**. Questa formulazione precisa
la descrizione abbreviata della consegna senza riscriverla e senza introdurre un nuovo
delta nel candidato.

Non sono state eseguite integrazione in `main`, pubblicazione, push, tag o operazioni
di congelamento. 03.9, 03.10, 03.15 e Fase 03 restano aperte. Restano fuori perimetro
simulazioni, inferenze, chiamate API, una nuova decisione D9 e la riapertura di A/B,
FAR o U3.

## Inventario byte-identico

Sorgente:
`/Users/luker/fot-tep-verifica-consolidamento-04dee86/studio2/fase03`.
Destinazione:
`/Users/luker/fot-tep-consolidamento-0315-metriche/studio2/fase03`.
Per ogni percorso sono stati confrontati sorgente, copia e blob del commit di
acquisizione; dimensioni e SHA-256 coincidono.

| Percorso acquisito | Byte | SHA-256 |
| --- | ---: | --- |
| `studio2/fase03/VERIFICA_CONSOLIDAMENTO_0315_METRICHE.md` | 23510 | `253563fdaa10bb812af33500611251507146e362da2d753a0802d884fed21adc` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/CONSEGNA_CONSOLIDAMENTO_0315_METRICHE_2026-09-14.md` | 14350 | `279da29644a4109321064548bf3ea41c1984a2034be6dcb8f18714a9d117ace8` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/MANIFEST_EVIDENZE.json` | 6933 | `20ad6e2626741f93805cb75645d9a2465f4c8807a5be1f95be11f1c62d26ed7d` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/PROMPT_VERIFICA_CONSOLIDAMENTO_0315_METRICHE.md` | 6436 | `162e8538a7a82f35f8d18ceab1551f2c3972a7dc378cfa8b3010bb750e459161` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/check_documents.py` | 5986 | `7eab99f8307dbc51eb594da088f6ce49d38b9e6c20969db71c72b7f4c4f19132` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/check_integrity.py` | 8225 | `37e46589b09625fcf05dff84c4f853922aa1e191883e64bb72ac26aa6661af71` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/check_metadata.py` | 2365 | `b0a9b0975ab555df0fd8869798d27d323da7b44cff8dc85d442c4df3a19118e0` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/checks.json` | 7535 | `3dd0b97f49e1b2355ca45d1fb82f055f9518de1725fee6a4469707be344c5a33` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/delta_M.patch` | 24089 | `d6486aa6aa97dc74f0edb8060b7d502f749783a7c300241bef2589024bfc7f34` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/delta_P.patch` | 19904 | `1c19fa87ef809f910c1c45e00d2a10197069347ecb74b21cfb671d1e60e370b9` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/diff_check_new_record.log` | 259 | `e3ff592ab0e2f501f3ac8d8bd6d6ccb8c9ccf78c3cbd94a99102b51746e82a59` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/diff_check_pair.log` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/documents.json` | 77659 | `7db3e760e6e814e45ac80d997ee83edb1e36e87b0be6c77036819823dcddf079` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/final_preservation.json` | 2973 | `36f21df512a8fd39b1d97b769c5a129dc1db9ee95bd9be9b40164bed08e70128` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/guardiano_base.log` | 2582865 | `e1e1abbe911fa88384259c630d1412ccd1f94f471767971eef31bc87e72a6d5c` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/guardiano_candidate.log` | 2582935 | `4b8439b726314a921ea31142b167205f280c378906416687bbd56ff704267c16` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/integrity.json` | 85581 | `6a2f811ce123ca58e0aefaa6837d8c90cea4c6f34eaff9cac6ac463d39b610c1` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/lint.log` | 44 | `7863036d3116bda1194afa539cbb041d486d3a4771b68cd51b58001e95b3485f` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/metadata.json` | 10250 | `cc537e1ebc86dccbb2ee4d241778965798293d41b4b95e6e8ebd466314b4c996` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/metriche.log` | 1671 | `0e6ee7321688459b98f29d1da4d31268d57cb829d8cc9acb7ae7fe341e97890a` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/preflight.json` | 7400 | `55bb012659ad304cda5b02d7af8d4c77cd94484347663cb3b3a5569dcadd28ae` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/remote_final.log` | 57 | `2851a07a74e0461d5b5d467397a4c07fb29ee3fe6d2ff4ad9fdc8cdc1f0915a0` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/run_checks.py` | 2359 | `47ddce50261c400a76c63b184ea01db01f99548ab601d79e9808d522f00cb6a6` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/supplement.json` | 14848 | `0f0a5244965e9af280cafd14ef23949ad954529ad9efcc1eebe2d29566ce221c` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/typography.patch` | 1277 | `38c969ad6370b8950c56052ab6266ed1e042906783729cc2b0fac03b21036918` |
| `studio2/fase03/evidenze_verifica_consolidamento_04dee86/write_report.py` | 20532 | `6b157e5467f7727875fe8b1fe0eb392d0a3ae3e8cf04abb0f35a30cd4498aa41` |

Il manifest contiene 25 voci e tutte risultano presenti e conformi. Esclude sé
stesso per evitare auto-riferimento: inventaria il verbale esterno e gli altri 24
file della directory, mentre la directory acquisita contiene 25 file incluso il
manifest. I riferimenti assoluti del manifest sono stati mappati sostituendo la
radice sorgente con la radice destinataria e mantenendo invariato il suffisso
relativo; i byte del manifest non sono stati modificati.

Nessun file presente nella directory inventariata è stato escluso. Non sono stati
acquisiti i rollout completi di conversazione né le directory e i tar temporanei
citati dalle prove, perché non sono voci del manifest e il verbale dichiara che non
sono necessari alla conservazione del candidato.

## Controlli di chiusura

Sono pertinenti a questa acquisizione soltanto: completezza del manifest, confronto
sorgente/copia/blob, perimetro dei commit, collegamenti del presente record e
preservazione del candidato. Non sono state rilanciate suite scientifiche, review,
simulazioni o chiamate sperimentali. Il commit di acquisizione aggiunge 26 percorsi;
il commit successivo aggiunge soltanto questo record.
