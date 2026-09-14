# Verifica indipendente della revisione 10 — incarico

Usare una sessione separata e **modello diverso da Codex GPT-6 preparatore**.
Registrare identità effettiva e sessione nel verbale. Sola lettura del candidato;
scrivere il solo nuovo verbale nella propria copia, senza correggere il candidato.

Leggere `docs/MAINTENANCE.md`, `docs/prompts/Prompt_LLM.md`, `Verifica_LLM.md`,
poi `studio2/fase03/piano_statistico/REPORT_PIANO_STATISTICO.md` e le fonti citate.
L'approvazione effettiva è il messaggio Luca trascritto nel record
`APPROVAZIONE_ADDENDUM_03_8.md`: A/B senza modifiche al commit `526561f`,
firma separata. Non chiedere di nuovo l'approvazione e non trasformarla in firma.

## Identificazione

Branch sorgente `codex/studio2-piano-statistico-fix`, worktree
`/Users/luker/fot-tep-piano-statistico-fix`. Baseline:
`526561feabeb6b4083170b1817b8abdac1a2a4c7`; approvazione:
`f37e7e00cbdd959ef6fdb7cc96ce42ed521075d6`.
Identificare il commit candidato che introduce la revisione 10 del manifest
corrente, registrare il SHA completo e il SHA-256 del manifest nel verbale.
Verificare che il manifest abbia `revision=10`. Se la sorgente avanza, usare una
copia esatta del commit comunicato nella consegna e indicare quello verificato.
Non assumere che un successivo HEAD abbia già lo stesso OK.

Manifest storico rev. 9: `2b6ad396307be634428d9355d4aa65144b4956d675ccb9e4b47536e4bdaf8d76`,
conservato anche in `PIANO_STATISTICO_FREEZE_REV9.json`; risolverne i file al
commit `0f1a9bae8b522f614720fa5efe7bd9d2577609ae`.
Manifest preparazione: `a570c0c91f3a45d4435d318e628cdad37ef7be0dceda17fcb62cf50350dead93`,
valido sullo snapshot `526561f`. Le sue righe pending sono storiche.
Verbale rev. 9: `289a74433d70e2bf911bdea893711ff7a294c75cf74d5e6fa0addbf3ede72a58`,
preservato in `29249a9305c44a44b96e6f49f94e978956ed0ac2`; non certifica il delta nuovo.

## Verifiche

1. Confrontare l'intero diff baseline→candidato con l'addendum esatto e la risposta
   autore: nessuna decisione ulteriore, nessuna nuova firma, data effettiva corretta.
2. A: tetto 3.700 solo storico, conteggio completo per blocco/modello/R, tempi
   misurati nel pilot e margine 20%; R3 soltanto da divergenza, sospensione
   organizzativa se non fattibile, nessuna riduzione automatica o scelta D9.
3. Conti: nucleo 1.728/5.184, swap misura 224R, ablation 148R, OOD 144R;
   audit 2k aggiuntivo solo R1; E5 R1 parametrico, FULL condizionato alle sei
   identità; canary 10/giorno; nessun doppio conteggio produzione/conformità,
   pilot/riserva/retry. Scenari 3.142/7.284 non sono totali definitivi approvati.
4. B: congelamento prima dei run di candidati/criteri/catene; controlli OOD
   03.11 prima delle chiamate, senza selezione su prestazioni/separabilità;
   sostituti verificati e distinti, casi non risolti sospesi; assenza ciclo.
5. Distinguere requisiti di freeze da operatività prima del pilot e delle chiamate
   test, senza eliminare input/schema/mapping/capienza, implementazione 03.10,
   T5, controlli OOD o pubblicazione. Segnalare se il recepimento eccede A/B.
6. Invarianti: ipotesi, m, alpha, gerarchia/reporting, DESIGN_RESOLUTION, algoritmi,
   test, campioni/scorte, criteri OOD, validità, remediation e gate. Riserva
   8r+t≤15, sonda solo quota 7 anche senza remediation e triplette complete,
   massimi 152/160, hard stop 200, nessun retry gate/reset; invariati.
7. Manifest: ricalcolare tutte le voci files/inputs_read, catena e storico;
   nessun auto-riferimento. Preparazione e verbali storici byte-identici.
8. Allineamenti esterni: verificare che siano dichiarati pending e che il delta
   predisposto richieda ora A/B approvate; nessuna falsa integrazione bibliografica,
   firma, pubblicazione o implementazione. F6 entro PHM non è GO OOD tecnico.
9. Eseguire `/Users/luker/fot-env/bin/python -m unittest
   studio2.fase03.piano_statistico.test_design_resolution` (26 test) e
   `python3 docs/test_explanation.py`: 35 test, 14 fallimenti e 1 skip,
   confrontare identità/subtest in CONTROLLI_REV10.json. `git diff --check`, link
   e JSON. Non eseguire la griglia completa, inferenze, simulatori o test di dati reali.

## Consegna

Scrivere `studio2/fase03/piano_statistico/VERIFICA_PIANO_STATISTICO_REV10.md`
nella copia separata, **OK** o **NON OK** in prima riga, con modello/sessione,
commit/manifest esatti, fonti e rilievi puntuali. L'OK può riguardare il
**recepimento A/B della revisione 10**, non chiusura/freeze se i residui mancano.
Non usare il precedente OK per certificare il nuovo delta. Il preparatore
conserverà il verbale byte per byte in un commit distinto, senza alterarlo.
Nessun push, merge, tag, walkthrough, modifica 03.5 o dichiarazione di Fase 03 chiusa.
