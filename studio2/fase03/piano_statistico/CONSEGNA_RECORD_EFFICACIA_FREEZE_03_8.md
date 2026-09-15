# Consegna del record post-tag di efficacia — 03.8

Data: 2026-09-15. Stato: **candidato locale in attesa di review indipendente**.

## Identità esatta

- Worktree: `/Users/luker/fot-tep-efficacia-freeze-038`.
- Branch: `codex/studio2-efficacia-freeze-038`.
- Base e commit pubblicato/taggato:
  `11f504b2bf45a39c1bc4746952f50d58c5022743`.
- Candidato da verificare:
  `0b0b2ee2a168d14dc6e46dd8334aebbab311a08e`.
- Tree candidato:
  `f2e6b67a0cc5d4420cbd08fc5c238c9c6860d237`.
- Genitore unico:
  `11f504b2bf45a39c1bc4746952f50d58c5022743`.
- Remoto effettivo: `https://github.com/sorrentinoluca/fot-phd.git`.
- `origin/main` osservato:
  `11f504b2bf45a39c1bc4746952f50d58c5022743`.

La presente consegna e il prompt sono successori documentali e non fanno parte
del candidato.

## Delta candidato

Il diff `11f504b..0b0b2ee` aggiunge esattamente un file:

`studio2/fase03/piano_statistico/PROVA_REMOTA_FREEZE_PIANO_STATISTICO_03_8_2026-09-15.json`

Il file misura **6.773 byte** e ha SHA-256
`2c011bba8b02e3c357cfe62ea90d63f75527d0690186846d5e385e8e79a44f97`.
Il delta contiene 143 inserimenti e nessuna cancellazione. Nessun piano,
manifest, verbale, acquisizione, walkthrough, harness, configurazione o
risultato è modificato.

## Stato registrato

Il record riporta i valori osservati e verificati dopo la pubblicazione:

- tag annotato `studio2-fase03-piano-statistico-frozen-001`;
- oggetto tag locale e remoto:
  `bfcf6e5b3840c5b7dc3f7ace1085843d18cfddc7`;
- peeled locale e remoto:
  `11f504b2bf45a39c1bc4746952f50d58c5022743`;
- tree del target:
  `c4da62906fe434ea7e8f514dc72f9e0c4e7b4b71`;
- `origin/main` coincidente con il target;
- piano rev.10, manifest pre-tag, verbale OK e acquisizione presenti nel target
  con le impronte già registrate.

Il record dichiara `freeze_effective=true` perché pubblicazione, tag annotato e
peeled remoto sono fatti già avvenuti. Distingue però il proprio stato:
`record_verified=false`, `record_published=false`,
`subphase_03_8_closed=false` e `phase_03_closed=false`. La chiusura non è
anticipata.

Il tag non contiene firma crittografica. I campi `tagger` sono metadati Git
dell'oggetto annotato e non costituiscono né sostituiscono una firma materiale.

## Esclusione preservata

Il branch è stato creato direttamente da `11f504b`; il successore preparatorio
`f944efd2872786d439c22b38302d33e91d08cfab` non è nella storia del candidato,
non è raggiungibile da `origin/main` e non è raggiungibile dal tag.

## Controlli del preparatore

- JSON valido e campi di stato verificati meccanicamente;
- oggetto tag, tipo annotato, target, peeled e messaggio riscontrati dal tag
  Git locale;
- oggetto e peeled remoti ricalcolati con `git ls-remote`;
- `origin/main` ricalcolato e coincidente con il target;
- impronte dei quattro artefatti principali e dei due manifest storici
  ricalcolate dai blob del commit taggato;
- assenza di firma PGP/SSH nell'oggetto tag;
- esclusione di `f944efd` verificata con la relazione di antenato;
- `git diff --check` pulito;
- guardiano **NON PASS**: 35 test, 14 fallimenti storici e 1 skip; non
  classificato PASS e non influenzato dal delta JSON.

Questi controlli sono del preparatore e non sostituiscono la review
indipendente. Nessun push, tag, modifica del tag, firma, chiamata ai servizi,
inferenza, simulazione o pilot è stato eseguito nella preparazione del record.

## Passi successivi

1. review indipendente del solo delta `11f504b..0b0b2ee`;
2. acquisizione byte-identica del verbale in un successore;
3. pubblicazione non forzata e autorizzata della catena verificata;
4. verifica che il record sia raggiungibile da `origin/main`;
5. solo allora documentazione della chiusura 03.8, senza dichiarare chiusa la
   Fase 03.
