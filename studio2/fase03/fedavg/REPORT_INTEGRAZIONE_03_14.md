# Report di integrazione 03.14 in `main`

**Verdetto:** `READY FOR AUTHOR MERGE`

**Data:** 2026-09-17

**Finestra:** preparazione locale su `origin/main` `15e56a89b0f377e6d90eef28ed941d4d54b5b00c`

**Modello:** `gpt-5.6-sol`, reasoning medium

## 1. Stato e copertura delle review

Il branch sorgente `codex/studio2-fedavg` era a
`e1b46faf5aee27b2a1f98d4c568c3e276bf33ae4`, tree
`c938e07056951eec60ace9e3707f64a956a6e708`, con il solo file preesistente non tracciato
`studio2/fase03/PROMPT_VERIFICA_MINIMA_03_14.md`. Il file è rimasto escluso da ogni operazione.

La review principale e il replay indipendente esprimono `OK` sul commit scientifico
`8cb9a8bc62ddd207ed1ed7a287e0124ceae07999`. Il delta `8cb9a8b..e1b46fa` contiene soltanto:

- `ACQUISIZIONE_OK_FINALE_03_14.md`;
- `VERBALE_REPLAY_INDIPENDENTE_FEDAVG_03_14.md`;
- `VERBALE_VERIFICA_ESECUZIONE_FINALE_FEDAVG_03_14.md`.

Non vi sono quindi modifiche sostanziali successive al candidato verificato. Il commit
`e1b46fa` acquisisce i due verbali senza estendere il loro `OK` a codice, dati o risultati nuovi.
Sul branch di integrazione, il rebase produce le corrispondenze `8cb9a8b` → `6c5c05d` e
`e1b46fa` → `8196f22`; escluso questo report, il sottoalbero FedAvg resta byte-identico al branch
sorgente verificato.

## 2. Prova d'integrazione

La prima prova di merge, svolta in una worktree temporanea e senza commit, ha prodotto un solo
conflitto: `studio2/PROVENIENZA.md`. Le due linee di sviluppo avevano aggiunto contenuti alla
stessa coda del file a partire dal merge-base
`46c0b623f55154684f326a8523521fb28991fb09`:

- `origin/main` aveva aggiunto le sezioni 10–14;
- il branch FedAvg aveva aggiunto la propria sezione 10.

La risoluzione è puramente additiva: conserva integralmente le sezioni 10–14 di `origin/main`,
conserva integralmente il contenuto FedAvg e rinumera soltanto la sua intestazione come sezione
15. Il sottoalbero `studio2/fase03/fedavg/` resta byte-identico a `e1b46fa`.

Per mantenere intatta la storia del branch sorgente, la risoluzione e questo report sono stati
preparati sul branch separato `codex/studio2-fedavg-main`, ribasato sul commit esatto di
`origin/main`. Non è stato eseguito alcun merge, push o tag.

Controlli sulla risoluzione prospettica:

- `git diff --cached --check`: PASS;
- suite FedAvg core e finale con Python 3.13.9 / NumPy 2.3.5: **15/15 PASS**;
- `docs/test_explanation.py` prima e dopo: 35 test, 14 failure, 1 skip;
- le identità complete dei 14 failure sono invariate;
- nessun conflitto residuo;
- sottoalbero FedAvg identico al branch verificato.

## 3. Inventario degli artefatti

Non esistono artefatti FedAvg fuori Git. Tutti i 634 file di `final/` e tutti i 4 file di
`smoke_real/` presenti nel filesystem sono tracciati; i conteggi di file non tracciati e ignorati
in entrambe le directory sono zero. Le dimensioni logiche complessive sono:

| Directory | File | Byte |
| --- | ---: | ---: |
| `final/` | 634 | 2.915.061 |
| `smoke_real/` | 4 | 13.031 |

I 624 file di firma finali occupano complessivamente 2.637.884 byte e sono vincolati dal manifest
finale. Non sono conservati file binari di pesi: i dieci modelli di ciascuna esecuzione sono
identificati dai digest contenuti nei rispettivi `weight_hashes.json`.

### 3.1 Pesi, metriche e manifest tracciati

| File | Byte | SHA-256 |
| --- | ---: | --- |
| `final/weight_hashes.json` | 864 | `50af2a8f145009038c0c1cd8ef1530cb4bb5817059a77fbcf76b1618091fefd3` |
| `final/primary_cluster_metrics.csv` | 40.387 | `f31d66c9f79689b398c94beca46d0cf14527bdaffc4348bc684b09e3bcb485de` |
| `final/ood_forced_attributions.csv` | 6.165 | `804ce4c1b9c15fb5096477631771487c4544dd072dbeaff4fc00ba2c1be8f7fb` |
| `final/PRIMARY_SUMMARY.json` | 976 | `d6aeeb596f4a6b6785b551c82768307aaceeef4d8f53922a74c094a8074266e9` |
| `final/OOD_SUMMARY.json` | 357 | `64faa3a949a364b4393de59812a6313626d79baf482651bddbe62129ab3531a8` |
| `final/FINAL_SUMMARY.json` | 1.194 | `7ef542e806968346f3c38194f04d73f780b77c6972aa77e123272226628f9db1` |
| `final/FINAL_EVIDENCE_MANIFEST.csv` | 189.283 | `7bf857192a296ee8e21f60fa7379e221bbdb2d962b5eea7707c72561c918d58e` |
| `final/FINAL_SET_MANIFEST.csv` | 31.892 | `34a860e015c41411038eb1e8d05dad1e7a79aab505b9b42017a8e81674456122` |
| `final/INPUT_PREFLIGHT.json` | 5.836 | `fe48b162b1a0290a15bd2418d3c9ece2bc93908dcddfb74ccfbc776b613fbe3d` |
| `final/EXECUTION_STATE.json` | 223 | `a8be41223015f039a3be8a1e224fece4697831cb2f1c81eae757a59ef49c9211` |
| `smoke_real/weight_hashes.json` | 864 | `82bc7d012d330fe6e7f0bc5529f9e8051cf477deecc79c35ff163ffa0cad835f` |
| `smoke_real/cluster_metrics.csv` | 9.189 | `8ed7d8075c66b8a028a1842b6bcf3732db054c4bce2facde41d1d0ea8969079b` |
| `smoke_real/SMOKE_SUMMARY.json` | 758 | `53f9d16541e1f5225bf91984f0ddc5f0389de347cd074619ca3c2e6c5dc22f04` |
| `smoke_real/INPUT_PREFLIGHT.json` | 2.220 | `8b1e8125bda32beec8814e275517f0311fd7c386b6b2a795de71b875017daad5` |

Digest dei modelli finali: centralized
`3d59ab5cb606d615172f7d308e0c29d2caed6707ffc46aa8f292f596475d6a03`, FedAvg
`9532f633608dd7f5735a2758a35db9bb5fb9088ec28464acb238e0f462960614`; local F1
`9fc0e2c2cfcd2fd325a9eac935c6366df9a0a8ec8fdc37c0feae89317a30bfcf`, F2
`ad2e48d9799054638e03b66d754414ebb028719345f02521080e4da17a742bc2`, F3
`173341bd9ab5d555008adb8ef3ba16c8f8263fa4e02907876cf7757de3c9ec2b`, F8
`35856c20986076fc9722400db3410cd986ce0941e1c769680bb4524431b04db8`, F10
`c9eac2fe9b71653a83a394606960f368245e336d65d6a9b2851578d8e42cce92`, F13
`0797c79d309e741a2098bfb2c78d2985dbe6cc8b2c1e392c722ddcffced245ab`, F14
`0df00bc0b4dbf36df1c2e67f12bea08e818a8d08611cf812072d21951bafdb22`, F15
`c09fc0e62757ff0b558f569bc9446b60f84a8b34e93048368ec278df7ca906bf`.

Digest dei modelli dello smoke reale: centralized
`103bec11574bd9c1c43ae6c4e1a4a3fcaded3434d830f2fbf983954bfc3ecc6f`, FedAvg
`2c668d82df8336c1a64e604065c05ccbd0eff6fedc174973ff233755e4f5a299`; local F1
`8237603a7750d7dd62c8c5aa8d80e417b3bdc2818373686bb12a0a5541cb3c95`, F2
`8b7755a8e873555c611cecfe8cc997a234b002ffbd0739f98d9713b40a7f6cc5`, F3
`c8864ebac678d60aadd435bbc352dc2f562759ac8e70899b3c26e8eabcc7d219`, F8
`24a4a54b62980d9a4ebe79b8afa5b6a7a2a8447bae5d0ddfda07609e033549b0`, F10
`0a82f2c27f24485a034c2d0ed2f8213f74a3f441254d17fb7c65665ff4a5f157`, F13
`6d884ca447393ddba31785d575122002ae3b6d7d693cb1d7ddbb2020d97e73cb`, F14
`73555cad790b7ff19fd40f85424ea44450b8a2a21e7498d784374036a833613c`, F15
`7369f9ef6ef1a2f9ace86d611753b3f0f9c9192709da180c5ff53afc791f7ee2`.

### 3.2 Conservazione esterna

La condizione di `MAINTENANCE.md` §8.5 non si attiva: il lotto è interamente nella storia Git e
non dipende da dati voluminosi esclusi. Non è quindi corretto creare o aggiornare
`ARTIFACT_STORAGE.json` e `MANIFEST_CONSERVAZIONE.csv` con una release inesistente, né preparare
il tag `studio2-fase03-fedavg-v1`. Non vi sono comandi di caricamento per Luca.

## 4. Comandi per Luca

La prova è valida soltanto finché `origin/main` resta al commit indicato. Eseguire:

```bash
cd /Users/luker/fot-tep
git fetch origin
test "$(git rev-parse origin/main)" = "15e56a89b0f377e6d90eef28ed941d4d54b5b00c"
git switch main
git merge --ff-only origin/main
git merge --ff-only codex/studio2-fedavg-main
PYTHONDONTWRITEBYTECODE=1 /opt/anaconda3/bin/python3.13 -m unittest -v \
  studio2.fase03.fedavg.test_fedavg \
  studio2.fase03.fedavg.test_final_fedavg
PYTHONDONTWRITEBYTECODE=1 python3 docs/test_explanation.py
git diff --check 15e56a89b0f377e6d90eef28ed941d4d54b5b00c HEAD
git status --short --branch
```

Il guardiano documentale deve continuare a riportare gli stessi 14 failure preesistenti e 1 skip;
un semplice confronto del totale non è sufficiente. Se `origin/main` è avanzato, fermarsi e
rieseguire la prova d'integrazione sul nuovo commit.

## 5. Cosa resta fuori

- nessun push, merge o tag è stato eseguito; il solo branch di preparazione è stato ribasato
  sull'esatto `origin/main` richiesto;
- nessun runtime, ledger, training, replay scientifico o chiamata a modelli è stato eseguito;
- nessuna release `fot-tep-data` è necessaria per gli artefatti FedAvg già tracciati;
- il file non tracciato preesistente `PROMPT_VERIFICA_MINIMA_03_14.md` resta fuori;
- l'integrazione di 03.14 non chiude la Fase 03 ai sensi di `MAINTENANCE.md` §8.6 e
  `Commit_LLM.md` §7.
