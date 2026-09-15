# Consegna del manifest finale pre-tag — 03.8

Data: 2026-09-15. Stato: **candidato locale in attesa di review indipendente**.

## Identità esatta

- Worktree preparatore: `/Users/luker/fot-tep-finalizzazione-038`.
- Branch: `codex/studio2-finalizzazione-038`.
- Base del delta:
  `a5798c667dedcb85d3b745258fbc992e0c05841a`.
- Candidato da verificare:
  `ec807dbaf2cb745ba96d397aac64a981f6fdeb7d`.
- Tree candidato:
  `58ffd0b057dee7c1a1c399aaadd6c256d8658e34`.
- Genitore unico:
  `a5798c667dedcb85d3b745258fbc992e0c05841a`.
- `origin/main` osservato durante la preparazione:
  `8dbd2b49176c16f9e100e5f181c729b99d406a35`.
- Remoto effettivo: `https://github.com/sorrentinoluca/fot-phd.git`.

La presente consegna e il prompt di review sono successori documentali del
candidato: non appartengono al suo tree e non saranno coperti dal relativo
verdetto.

## Delta candidato

Il diff `a5798c6..ec807db` aggiunge esattamente un file:

`studio2/fase03/piano_statistico/MANIFEST_FINALE_PRE_TAG_03_8.json`

Il file misura **14.768 byte** e ha SHA-256
`087d268d438ca6e98063346a5547849a05235a43712aebe56e007c46dcc1413d`.
Il delta contiene 338 inserimenti e nessuna cancellazione. Non modifica piano
rev.10, manifest storici, verbali, acquisizioni, walkthrough, harness,
configurazioni o risultati.

## Contenuto e confine dichiarato

Il manifest:

- registra la pubblicazione già verificata di `8dbd2b4`, tree `d1d2a0b`, come
  fast-forward non forzato da `a006058`;
- include 31 artefatti di confine con percorsi univoci, dimensioni e SHA-256;
- conserva il piano rev.10 a 81.490 byte e SHA-256 `675dbbcc…032a`;
- conserva `PIANO_STATISTICO_FREEZE.json` e
  `MANIFEST_CANDIDATO_FREEZE_03_8.json` come record storici immutati;
- registra i cinque checkpoint indipendenti già acquisiti, compreso l'OK sul
  candidato di finalizzazione `4c9e7a1`;
- distingue il commit pubblicato dal record locale di pubblicazione
  `a5798c6`;
- non include la propria impronta e rinvia a questa consegna per l'identità del
  candidato;
- mantiene `freeze_effective=false`, `subphase_03_8_closed=false` e
  `phase_03_closed=false`;
- mantiene nulli commit/tree del candidato nel proprio corpo e target, oggetto
  e peeled del tag;
- dichiara ancora pendenti review, acquisizione e pubblicazione del delta
  pre-tag.

Il tag pianificato
`studio2-fase03-piano-statistico-frozen-001` risultava assente dal remoto al
controllo finale. Il candidato non crea un freeze e non anticipa il futuro
target del tag.

## Controlli del preparatore

- JSON valido;
- 31/31 artefatti presenti, con dimensioni e SHA-256 conformi;
- 31/31 percorsi univoci;
- campi di non efficacia e valori nulli controllati meccanicamente;
- `origin/main` ancora uguale al commit pubblicato `8dbd2b4`;
- tag pianificato assente;
- `git diff --check` pulito;
- guardiano **NON PASS**: 35 test, 14 fallimenti storici e 1 skip; non
  classificato PASS e non influenzato dal delta JSON;
- worktree privo di modifiche preesistenti prima della preparazione.

Questi sono controlli del preparatore, non una review indipendente.

## Passi successivi

1. review indipendente del solo delta `a5798c6..ec807db`;
2. acquisizione byte-identica del verbale in un successore documentale;
3. autorizzazione e pubblicazione della catena pre-tag;
4. soltanto allora identificazione del commit pubblicato destinato al tag;
5. mandato separato per tag annotato e verifica remota di oggetto e peeled;
6. eventuale record post-tag di efficacia, con propria verifica se dichiara
   `freeze_effective=true`.

03.8 e la Fase 03 restano aperte. Non sono stati eseguiti push ulteriori, tag,
freeze, firme, chiamate ai servizi, inferenze, simulazioni o pilot.
