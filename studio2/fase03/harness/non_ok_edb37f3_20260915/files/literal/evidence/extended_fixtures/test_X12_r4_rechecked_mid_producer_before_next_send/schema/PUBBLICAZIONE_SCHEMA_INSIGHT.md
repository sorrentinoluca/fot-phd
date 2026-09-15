# Pubblicazione della sotto-fase 03.12 — schema insight R4

Data: 2026-09-14, Europe/Rome. **Contratto R4 verificato, raggiungibile da `main`
e congelato con tag annotato pubblicato.** La Fase 03 resta aperta: questo record
non qualifica il futuro pilot, il servizio 122B o gli insight scientifici.

## Identità pubblicate

| Ruolo | Riferimento |
| --- | --- |
| `origin/main` osservato prima del tag | `4f98a2973d2e1ca7932f19c34e9dd4c0498b8b43` |
| Target R4 verificato e unico destinatario del tag | `3c64390bc4dd58c48cc4e1e388a38989b32b3143` |
| Commit che acquisisce log server, verbale OK e prompt | `43b31afc1ff271594cb4bd21a39fa4469a8c83bc` |
| Documentazione R4 già raggiungibile da `origin/main` | `c9f83c6447a9963cd69531b14439a3ac5a5a72b2` |
| Tag annotato | `studio2-fase03-schema-insight-frozen-001` |
| Oggetto tag remoto | `4d15c4fb915ea9db9f7425225d231746778f0ba1` |
| Commit peeled remoto | `3c64390bc4dd58c48cc4e1e388a38989b32b3143` |
| Record di pubblicazione | commit che contiene questo file, successore del `main` osservato |

Subito prima della creazione del tag, `git fetch origin main` e `git ls-remote`
hanno confermato `refs/heads/main` a `4f98a297…` e l'assenza del tag sia locale
sia remota. Target R4, commit delle evidenze e documentazione R4 risultavano tutti
antenati di `origin/main`. Il tag è stato creato sull'esatto `3c64390…`, non su
HEAD, sul commit delle evidenze, su un merge o sul record di pubblicazione.

È stato pubblicato esclusivamente il ref
`refs/tags/studio2-fase03-schema-insight-frozen-001`, con push ordinario e senza
`--tags`, `--all` o force. Il riscontro remoto successivo ha restituito l'oggetto
annotato `4d15c4fb…` e il peeled `3c64390…`. L'annotazione registra contratto
rev. 4, manifest rev. 5, allineamento letterale di `Normal` a 03.7, qualifica Qwen
R4 documentata, impronta del verbale, assenza di insight prodotti e Fase 03 aperta.

## Integrità e conservazione

Il manifest `SCHEMA_FREEZE.json` resta la fotografia storica della preparazione:
12.323 byte, SHA-256
`d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12`,
`manifest_revision=5`, `contract_revision=4`, stato
`frozen_pending_independent_verification` e `tag_created=false`. Non è stato
riscritto né è stata creata una revisione artificiale successiva; pubblicazione e
freeze effettivi sono attestati dal tag remoto, dal verbale OK e da questo record.

Le **18/18** voci del manifest sono state ricalcolate per SHA-256 e dimensione ai
riferimenti storici previsti:

- 10 artefatti del pacchetto al target R4 `3c64390…`, tutti byte-identici anche
  in `origin/main`;
- 6 fonti al commit base `d815ce96d928254de79209f02e11a561445764cd`;
- 2 fonti 03.7 al commit registrato
  `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155` e al tag annotato
  `studio2-fase03-pseudolabel-frozen-001` (oggetto `6854c49b…`, peeled
  `c16b533016db4617deb1ba96853253f117e8e32b`).

La catena `previous_manifest_sha256` coincide con il manifest rev. 4 al commit
`e058cb07dceeefa8eb4a4b6d1f6fcab5aad483db`: SHA-256
`d6ef52de0f573edf3e5d6eb5ad3530400c5f63e6bcfa6579a93f21fdfb8865b5`.
Contratto, codice, decisione, report storico e log inclusi nel pacchetto non sono
stati modificati.

| Evidenza successiva al target | Byte | SHA-256 |
| --- | ---: | --- |
| `TEST_RESULTS_qwen_rev004.txt` | 7.459 | `a653c69ceed8ac10b06d57a98049f7939270f61473adab5ca0dbb901be654972` |
| `VERIFICA_SCHEMA_INSIGHT_rev004.md` | 21.288 | `d0e69094953cac7966eda9d1f612b81f44cc8e646151fd2339dba0b7ca88ec8e` |
| `VERIFICA_SCHEMA_INSIGHT_rev004_NON_OK_STORICO.md` | 19.064 | `5bd196820f74b7fbd5ee6736df2b72afc64afbbfb26459dc69f1fe5e15dafd19` |

Il log e il verbale OK sono byte-identici ai blob acquisiti nel commit `43b31af…`.
Il precedente NON OK è conservato separatamente e byte-identico al blob acquisito
nel commit `9b1fac9808b92222f45b8b590db32a378d73c136`; il successivo OK chiude il
rilievo d'indipendenza senza cancellarne la cronologia. Il log server resta una
trascrizione del terminale fornita dall'autore e copiata byte per byte
dall'allegato, non un file originale scaricato dal server.

## Controlli riusati e limiti

Non sono state ripetute la review scientifica o le prove sul server, perché i byte
qualificati coincidono. Restano distinti:

- suite locale R4: **25 PASS, 0 FAIL/ERROR e 1 SKIP su 26**, con skip del
  tokenizer reale per assenza locale dello snapshot pinnato;
- trascrizione fornita dall'autore: **26 PASS su 26 senza skip** sul server con
  tokenizer Qwen pinnato;
- futuro pilot e servizio/modello 122B: **non qualificati** da queste prove.

Sono stati inoltre riusati, a byte invariati, i controlli già acquisiti su 16/16
regressioni di fase, guardiano documentale invariato a 35 test con 14 fallimenti
storici e 1 skip, parità 26/26 dei fatti della sezione 03.12 e 8/8 link risolti.
I conteggi 83/84 token qualificano fixture e implementazione, non la capienza dei
prompt reali, l'ottimalità dei cap o la validità scientifica degli insight. Lo
scanner lessicale non dimostra l'assenza universale di parafrasi o leakage
semantico.

Nessuna simulazione, inferenza, chiamata sperimentale, scelta D9 o modifica
dell'adapter 03.10 è stata eseguita. A/B, FAR e U3 non sono stati riaperti.
Restano separati il pin dello schema nell'adapter 03.10, l'ordine delle label, gli
input reali, la qualifica dell'endpoint e del 122B, la capienza dei prompt reali e
il pilot. La Fase 03 resta aperta.

## Isolamento operativo e pubblicazione del record

Il lavoro è stato svolto nel worktree dedicato
`/Users/luker/fot-tep-pubblicazione-schema-insight-0312`, branch
`codex/studio2-pubblicazione-schema-insight-0312`, creato da `origin/main` a
`4f98a297…`. La copia principale, il worktree `main` della pubblicazione 03.15 e
il worktree della chiusura 03.9 non sono stati modificati. Nessun lock, worktree
o file preesistente è stato eliminato.

Prima del push di questo record, `origin/main` viene ricontrollato. Il commit
documentale viene raccordato soltanto sul `main` aggiornato e pubblicato con push
ordinario del solo ref `main:main`; l'hash remoto finale è registrato nella
consegna dell'operazione, evitando un auto-riferimento nel contenuto del commit.
