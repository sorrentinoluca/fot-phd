# Verbale breve — replay indipendente FedAvg finale 03.14

**Esito: OK**, limitato al candidato immutabile:

- commit `8cb9a8bc62ddd207ed1ed7a287e0124ceae07999`
- tree `49b4b0d2286ad3ac54cf78ab14778cffc959eb90`
- verbale precedente SHA-256 `a43db064a337bb2b4f9e3b9f9edaaf0c3afa5ac7ff62c17bf89bf08fccf6e58e`
- verbale precedente, byte pre-marcatore SHA-256 `9b6ae3c2dcbd123265741b8300223203ca343b4fd052e106c3e9a8ba09988e9b`

Data: 2026-09-16 (Europe/Rome). Replay locale, senza Qwen/LLM, bootstrap, simulazioni,
tuning, confronto col braccio LLM, commit, merge, push o tag.

## Ambiente e isolamento

- Eseguibile: `/opt/anaconda3/bin/python3.13`; Python `3.13.9`; NumPy `2.3.5`.
- Candidato letto da clone detached temporaneo dell'esatto commit in
  `/private/tmp/fedavg-independent-replay-9YkEJi/candidate`.
- Output prodotti soltanto sotto `/private/tmp/fedavg-independent-replay-9YkEJi/`.
- Il gate congelato richiede per contratto `EXPECTED_PACKAGE_HEAD=546edd7a1544beae06b3544a9de2eb659dcedbee`
  e tree `07cab1de0e282a841ce70a4b777545eae2746d71`; è stato quindi fornito a `--repo` un clone
  temporaneo di quel package, mentre l'eseguibile e il confronto provengono dal candidato esatto.
  I file congelati verificati dal gate sono gli stessi byte registrati nel candidato.
- Il worktree canonico `/Users/luker/fot-tep/.worktrees/studio2-fedavg` non è stato modificato;
  `final/EXECUTION_STATE.json` è rimasto presente con SHA-256
  `a8be41223015f039a3be8a1e224fece4697831cb2f1c81eae757a59ef49c9211`.

## Comandi essenziali

```text
git clone --no-checkout /Users/luker/fot-tep <tmp>/candidate
git -C <tmp>/candidate checkout --detach 8cb9a8bc62ddd207ed1ed7a287e0124ceae07999
git clone --no-checkout /Users/luker/fot-tep <tmp>/package
git -C <tmp>/package checkout -b codex/studio2-fedavg 546edd7a1544beae06b3544a9de2eb659dcedbee
shasum -a 256 <input esterni 03.6/03.9/03.11>
/opt/anaconda3/bin/python3.13 <candidate>/studio2/fase03/fedavg/final_fedavg.py preflight <argomenti congelati>
/opt/anaconda3/bin/python3.13 <candidate>/studio2/fase03/fedavg/final_fedavg.py execute <argomenti congelati>
/opt/anaconda3/bin/python3.13 -m unittest -v test_fedavg.py test_final_fedavg.py
```

È stata eseguita una sola azione `execute`: `training_attempts=1`, `evaluation_attempts=1`,
`tuning=false`.

## Input ricalcolati

Tutti i digest coincidono col preflight canonico:

- sviluppo fault: manifest `5111d0c6…0020`, indice `b966cdd3…f69c`;
- sviluppo Normal: manifest `cc8d96c2…fdc1`, vista nominale temporanea dell'indice
  `27a53450…31ae`;
- estrattore `46b451c2…4e97`, leakage `c77ae5b1…3887`, baseline N1–N5
  `79883dd0…b2e6a`, guardia R2 `7df0cef2…f33f8`;
- 03.11: review `09994cf7…16f`, audit `420a61eb…b6e3`, manifest `e7c75d23…4780`,
  eventi `af4f659e…b1b55e`, piano `ef0b2852…79572`, log `73ce498d…6587c`, archivio
  `ac1e7c0c…18a55` di 141.191.097 byte.

Il preflight ha verificato direttamente anche gli hash dei 89 sorgenti 03.11 e ha riprodotto
`FINAL_SET_MANIFEST.csv` con SHA-256 `34a860e015c41411038eb1e8d05dad1e7a79aab505b9b42017a8e81674456122`.

## Confronto col candidato

Uguaglianza byte-per-byte:

- 624/624 firme, stessi nomi e contenuti;
- `FINAL_EVIDENCE_MANIFEST.csv` `7bf85719…58e`;
- `primary_cluster_metrics.csv` `f31d66c9…85de`;
- `ood_forced_attributions.csv` `804ce4c1…7fb`;
- `weight_hashes.json` `50af2a8f…fd3`;
- `PRIMARY_SUMMARY.json` `d6aeeb59…26e9`;
- `OOD_SUMMARY.json` `64faa3a9…1a8`;
- `FINAL_SUMMARY.json` `7ef542e806968346f3c38194f04d73f780b77c6972aa77e123272226628f9db1`.

Metriche ricalcolate: Local `897/4608 = 0.19466145833333334`; FedAvg
`434/576 = 0.7534722222222222`; centralizzato `443/576 = 0.7690972222222222`; zero
astensioni. OOD: 180 righe, 20 gruppi da 24 attribuzioni, nessun campo `accuracy` o `correct`.

Nessuna differenza tecnica negli output confrontati.

## Test e limiti residui

`15/15` test pertinenti superati nell'ambiente freeze: 11 core e 4 finali.

I due limiti di disponibilità degli input e dell'ambiente sono chiusi dal ri-hash diretto e dal
replay byte-identico. Resta soltanto il limite storico già dichiarato: la precedenza originaria
della decisione OOD è provata dal gate fail-closed e dal digest sigillato, non da un timestamp
indipendente. Questo replay conferma lo stesso protocollo (`5eaa0418…76f9a`) prima della nuova
estrazione e non trasforma tale limite temporale in una prova retrospettiva.

Conclusione: **OK** per il replay audit e per l'identità degli output dell'esatto candidato; il
replay non costituisce un nuovo risultato scientifico e non autorizza tuning o sostituzione degli
artefatti canonici.

<!-- VERBALE-SHA256 -->
SHA-256 del verbale (byte precedenti la riga marcatrice `<!-- VERBALE-SHA256 -->`):
`8d01b9666f62cf2bbcd8f6963c6e2c5a493e18317797624733251bd4abbbc1db`
