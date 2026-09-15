# Consegna del candidato locale di finalizzazione — 03.8

Data: 2026-09-15.

## Identità esatta

- Worktree: `/Users/luker/fot-tep-finalizzazione-038`.
- Branch: `codex/studio2-finalizzazione-038`.
- Base del delta: `6490af4889fd679d491f63b9debdf2314eaf7aca`.
- Candidato da verificare: `4c9e7a1f1d8bd07b7d6be8df724f743986717da8`.
- Tree candidato: `03b215980ae170db2e1284dd7bd5eb07b830fb28`.
- Genitore unico: `6490af4889fd679d491f63b9debdf2314eaf7aca`.
- Main remoto osservato durante preparazione e controllo finale:
  `a00605862f627710347bd63c49f79a6d0a00135f`.
- Remoto effettivo: `https://github.com/sorrentinoluca/fot-phd.git`.

Questa consegna e il prompt successivo sono successori documentali del candidato
e non sono inclusi nel suo tree né in un futuro OK sul delta indicato.

## Perimetro del candidato

Il diff `6490af4..4c9e7a1` contiene esattamente otto file:

1. `docs/fot_walkthrough_conversazione_studio2.md`;
2. `docs/fot_walkthrough_conversazione_studio2.html`;
3. `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`;
4. `studio2/fase03/APERTURA_SOTTOFASI_FASE03.md`;
5. `studio2/fase03/piano_statistico/COORDINAMENTO_CHIUSURA_03_8.md`;
6. `studio2/fase03/piano_statistico/MATRICE_RESIDUI_03_8_DOPO_D9.md`;
7. `studio2/fase03/piano_statistico/MANIFEST_CANDIDATO_FREEZE_03_8.json`;
8. `studio2/fase03/piano_statistico/REPORT_FINALIZZAZIONE_03_8.md`.

Statistica: 436 inserimenti, 40 cancellazioni. Nessun file harness,
configurazione, `paper_sections/`, artefatto congelato, decisione, verbale,
acquisizione o risultato è modificato.

## Artefatti della consegna

- Manifest candidato: 12.382 byte, SHA-256
  `bcc9ef183190e2fd0997b2e600fc53498e4a6194993e997820255a4b6d124dc6`.
- Report: 7.198 byte, SHA-256
  `1d18e1b18568151aef095738d4a6dbbd34cd3ffa0e1cdb68c967e8c96a036baa`.
- Piano rev.10 preservato: 81.490 byte, SHA-256
  `675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`.
- Manifest storico preservato: 25.894 byte, SHA-256
  `a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8`.

Il manifest candidato dichiara `freeze_effective=false`; commit pubblicato,
target del tag, oggetto tag e peeled sono nulli. Non è una pubblicazione o un
freeze.

## Controlli conclusi

- 23/23 voci del manifest conformi per percorso, byte e SHA-256;
- 20/20 passaggi della catena con genitore Git corretto;
- dieci fonti sensibili byte-identiche alla base;
- JSON valido, `git diff --check` pulito;
- link/anchor validi e test mirato OK;
- sezioni walkthrough 4.8 e 4.15 testualmente pari fra MD e HTML dopo
  normalizzazione del markup;
- guardiano base/candidato **NON PASS**: 35 test, 14 fallimenti storici e 1
  skip, con gli stessi 14 identificativi e sottocasi;
- tag remoto `studio2-fase03-piano-statistico-frozen-001` assente;
- nessun `DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.*`.

## Stato e residui

03.8 è in finalizzazione locale e la Fase 03 resta aperta. Occorrono ancora:
review indipendente del candidato esatto, acquisizione byte-identica del
verbale, pubblicazione autorizzata su `origin/main`, eventuale delta e review
del manifest efficace, tag annotato sul commit futuro allora identificato e
verifica remota del relativo peeled.

Ordine label 1a, runtime harness D9, servizi/configurazioni, T5, pilot e
controlli OOD 03.11 restano separati. Il candidato harness `6a8031b` non è
importato e conserva il suo NON OK R-D9-01/R-D9-02.

Nessun push, merge su `main`, tag, firma, pubblicazione, chiamata, inferenza,
simulazione, pilot o run finale è stato eseguito.
