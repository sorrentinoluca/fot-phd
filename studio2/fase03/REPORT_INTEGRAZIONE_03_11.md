# 03.11-PUB — preparazione integrazione in main e consegna dati

Verdetto: **READY FOR AUTHOR MERGE**.

Data: 2026-09-17. Questo report prepara l'integrazione; non esegue merge, push, tag,
pubblicazione o runtime.

## Stato e copertura

Il branch `codex/studio2-esecuzione-0311` parte da `origin/main`
`15e56a89b0f377e6d90eef28ed941d4d54b5b00c` e l'HEAD iniziale e
`349ead315de575cf43977fdf807d43b64070546c`.

Il runtime e il lotto sono coperti dal verbale **OK**
`VERIFICA_ESECUZIONE_03_11_v2.md` sul candidato
`fd41fcf05aa6374d01b45b26b0881e2ffcc98062`, tree
`9010a6b3aab4029f20ff5355455c452bbefde1b5`; lo STOP F6 precedente e coperto dal
verbale **OK** `VERIFICA_ESECUZIONE_03_11.md` sul candidato
`1cdf597b9a95e7f1c9a3d6711c2f840c8b5ab6aa`, tree
`c3bcbe802f5c7fb6b9b5be55c1be88c87fef3b82`.

Delta non direttamente oggetto di un verdetto indipendente: `349ead3` aggiunge soltanto
le copie byte-identiche del verbale v2 e il suo record di acquisizione
`ACQUISIZIONE_OK_ESECUZIONE_03_11.md`; non cambia runtime, piani, audit, sigillo o dati.
La copia del verbale v2 e 2.339 byte con SHA-256
`09994cf7536166d4d4717eecd585ebe61c664fb5f388d58425cbc181e611f16f`.

## Rebase di prova

In una worktree temporanea esterna, il rebase di `349ead3` su
`origin/main` `15e56a89b0f377e6d90eef28ed941d4d54b5b00c` e risultato gia
allineato: nessun conflitto e HEAD invariato
`349ead315de575cf43977fdf807d43b64070546c`. `git diff --check` ha avuto esito
pulito e `python3 -m unittest discover -s studio2/fase03/fault_runs/tests -p
'test_*.py'` ha dato 27/27 OK. Non e necessario creare
`codex/studio2-esecuzione-0311-main`.

## Consegna archivi

I tre archivi locali sono registrati in `ARTIFACT_STORAGE.json` con stato
`publication_pending_author` e in `MANIFEST_CONSERVAZIONE.csv`:

| Asset | Byte | SHA-256 |
| --- | ---: | --- |
| `test_batch_f5_001.tar.gz` | 141191097 | `ac1e7c0c4575ab746ee24a8bb5ce7f09289919773bc4d8c61ba86f7a93218a55` |
| `chain_f5_001.tar.gz` | 1579326 | `242f689a8737739f51eb6b3acefaf34cea4c06e9ebd547beccbcf1760a473aec` |
| `ood_preflight_001.tar` | 7426560 | `16acf7c1e18923b606a47fe3fb0efaa83b99e8ee19024f11f4d8f3fd675929df` |

Comandi esatti per Luca, dalla root di questo worktree, per creare la release esterna
e il tag `studio2-fase03-test-v1`:

```bash
SUMS=$(mktemp /tmp/studio2-fase03-test-v1.SHA256SUMS.XXXXXX)
printf '%s  %s\n' \
  'ac1e7c0c4575ab746ee24a8bb5ce7f09289919773bc4d8c61ba86f7a93218a55' 'test_batch_f5_001.tar.gz' \
  '242f689a8737739f51eb6b3acefaf34cea4c06e9ebd547beccbcf1760a473aec' 'chain_f5_001.tar.gz' \
  '16acf7c1e18923b606a47fe3fb0efaa83b99e8ee19024f11f4d8f3fd675929df' 'ood_preflight_001.tar' > "$SUMS"
gh release create studio2-fase03-test-v1 \
  --repo sorrentinoluca/fot-tep-data \
  --title 'Studio 2 Fase 03 test batch v1' \
  studio2/fase03/fault_runs/test_batch/test_batch_f5_001.tar.gz \
  studio2/fase03/fault_runs/ood_chain_f5/chain_f5_001.tar.gz \
  studio2/fase03/fault_runs/ood_preflight/ood_preflight_001.tar \
  "$SUMS#SHA256SUMS"
```

Dopo la pubblicazione, Luca deve scaricare ogni asset in una directory esterna, confrontare
gli SHA-256, estrarre gli archivi e aggiornare `ARTIFACT_STORAGE.json` da
`publication_pending_author` a una verifica di riscaricamento reale.

## Merge per Luca

```bash
git fetch origin
git switch main
git pull --ff-only origin main
git merge --no-ff codex/studio2-esecuzione-0311 -m 'studio2(fase03): integra esecuzione 03.11'
git push origin main
```

## Fuori dal perimetro

Restano fuori l'effettiva pubblicazione e il riscaricamento degli asset su `fot-tep-data`,
l'aggiornamento post-pubblicazione dei metadati, il merge/push/tag di Luca, e qualsiasi
runtime, ledger, chiamata modello o guardian documentale.
