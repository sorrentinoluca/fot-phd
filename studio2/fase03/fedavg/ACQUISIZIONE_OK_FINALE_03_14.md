# Acquisizione delle review finali — sotto-fase 03.14

**Stato:** sotto-fase 03.14 conclusa e verificata localmente; non pubblicata e non taggata.

## Candidato verificato

- commit: `8cb9a8bc62ddd207ed1ed7a287e0124ceae07999`
- tree: `49b4b0d2286ad3ac54cf78ab14778cffc959eb90`
- parent: `546edd7a1544beae06b3544a9de2eb659dcedbee`

## Verbali acquisiti

- `studio2/fase03/fedavg/VERBALE_VERIFICA_ESECUZIONE_FINALE_FEDAVG_03_14.md`
  - esito: `OK` sul candidato esatto;
  - SHA-256 integrale: `a43db064a337bb2b4f9e3b9f9edaaf0c3afa5ac7ff62c17bf89bf08fccf6e58e`;
  - SHA-256 dei byte precedenti la riga marcatrice: `9b6ae3c2dcbd123265741b8300223203ca343b4fd052e106c3e9a8ba09988e9b`.
- `studio2/fase03/fedavg/VERBALE_REPLAY_INDIPENDENTE_FEDAVG_03_14.md`
  - esito: `OK` sul medesimo candidato;
  - SHA-256 integrale: `dff0956203dc55b74bbe37b3d4fac26e0997d497165b21155621c71f3f0b4ac4`;
  - SHA-256 dei byte precedenti la riga marcatrice: `8d01b9666f62cf2bbcd8f6963c6e2c5a493e18317797624733251bd4abbbc1db`.

Il replay indipendente documentato nel secondo verbale è stato eseguito con Python `3.13.9` e NumPy `2.3.5`. Gli output rigenerati risultano byte-identici a quelli del candidato: tutte le `624/624` firme e tutti i file di risultato elencati nel verbale coincidono. Il replay chiude i limiti operativi della review principale relativi alla disponibilità degli input esterni, al ricalcolo diretto delle impronte e alla riproduzione byte-esatta nell'ambiente di freeze.

## Limite residuo

Resta il limite storico-temporale dichiarato nei verbali: la precedenza della decisione OOD originaria è vincolata strutturalmente dal gate fail-closed e dal digest del protocollo, ma non è attestata da una marcatura temporale indipendente. Il replay non trasforma tale vincolo in una prova retroattiva; il limite è documentato come non bloccante per l'esito `OK` sul candidato esatto.

## Chiusura locale

Con l'acquisizione byte-identica dei due verbali, la sotto-fase 03.14 è conclusa e verificata localmente. Questa acquisizione non costituisce pubblicazione, tag o avanzamento delle attività successive e non modifica risultati, firme, manifest, codice, ricetta, freeze storico o walkthrough.
