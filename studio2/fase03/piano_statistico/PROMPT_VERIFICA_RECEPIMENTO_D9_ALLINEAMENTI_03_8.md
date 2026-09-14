# Prompt per verifica indipendente delle acquisizioni e del delta D9 — 03.8

Prima di modificare qualsiasi cosa leggi `docs/MAINTENANCE.md` e rispettalo.
Leggi i prompt pertinenti `docs/prompts/Verifica_LLM.md`, `Fase_LLM.md`,
`Documentazione_LLM.md` e `Commit_LLM.md`; il mandato circoscrive la review qui
richiesta e vieta qualsiasi integrazione/esecuzione scientifica.

## Oggetto esatto e indipendenza

Studio 2 FoT-TEP, Fase 03, sottofase 03.8. Data consegna: 2026-09-15.
Candidato **`8a20c125bd294191c67ebdbf571832b1e32ac0f1`**, tree **`f58eedf88d8c9c30767425c945b5ee5c421cf0b7`**.
Worktree preparatore: `/Users/luker/fot-tep-allineamenti-038-r1-r4`; branch
`codex/studio2-allineamenti-038-r1-r4`. Base immediata del recepimento:
`dc4d6560af73579300e33a0a81fc9c3b4316722d`. Base delle due acquisizioni: `16f227439357b07b7dc945f67ab5a4368c12b684`.
Fonte D9: `aaba893dff8c62f9f9281eec7423eee020235e03`. Main osservato dal preparatore:
`a00605862f627710347bd63c49f79a6d0a00135f`.

Esegui una nuova review indipendente dal preparatore, preferibilmente in una
nuova task senza il suo contesto e con un modello diverso. Registra **identità
effettiva del modello, provider, reasoning se esposto, task/sessione, worktree,
branch o detached HEAD**; non dedurli dal nome della finestra. Se un dato non è
esposto dichiaralo, senza inventarlo. Dichiarare eventuale contesto precedente
o altra limitazione dell'indipendenza.

Verifica preflight repository, HEAD/tree, branch, worktree, stato locale,
origin/main e main effettivo con `git ls-remote origin refs/heads/main`.
Se main è avanzato, registra la differenza e il suo impatto senza pull, merge o
rebase. Lavora in un worktree di review isolato detached al candidato esatto,
senza toccare principale, preparatore, sorgente D9 o cantiere harness. Se la
sessione ha solo `/Users/luker/fot-tep` collegato, recupera questo prompt e gli
altri documenti dal Git comune: per questo prompt usa
`git show codex/studio2-allineamenti-038-r1-r4:studio2/fase03/piano_statistico/PROMPT_VERIFICA_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md`;
per gli artefatti usa `git show 8a20c125bd294191c67ebdbf571832b1e32ac0f1:<path>`.
Poi verifica il candidato isolato.
La review è in sola lettura; unico output autorizzato:
`studio2/fase03/piano_statistico/VERIFICA_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md`
nel worktree del revisore. Nessun commit/push/merge/tag/firma/freeze.

## Limiti dell'OK pregresso

Il candidato R1–R4 `9a56d12d0633a0c9790c48792182f26fc6eb424a`, tree
`e35e5ca661325657715dce6723e4e8ec09540101`, ha **OK storico da preservare**.
`16f2274` è il successore di sola consegna/prompt, non un nuovo candidato R1–R4.
Non ripetere la vecchia review o verifiche statistiche/sottofasi chiuse: verifica
l'integrità dell'acquisizione e se il nuovo delta ne altera la coerenza.
Il verbale dichiara gpt-6-astra/openai/high, sessione
`01a0a1d9-8ccd-7893-b504-4fde93380ea0`: indipendente dal preparatore, ma medesima
sessione del precedente NON OK. Non trasformare tale esito in una review fresca
senza contesto o di altro modello. Il suo OK non certifica il delta D9 nuovo.

## Fonti e perimetro dei confronti

Leggi report, manifest e controlli del candidato:
- `REPORT_RECEPIMENTO_D9_ALLINEAMENTI_03_8.md` — 10773 byte; SHA-256 `97564d55fa400980b4c0a8106ab8074c226df7d4f0d9d09544956fb7f0856308`;
- `MANIFEST_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json` — 24446 byte; SHA-256 `bb5e4d9668f9714cead929bb575d44e497823376cda062c1443c0666dadc343a`;
- `CONTROLLI_RECEPIMENTO_D9_ALLINEAMENTI_03_8.json` — 32478 byte; SHA-256 `2f81b3d9d4da1864a485726f6a10ff9dcf3afd4213580197d0c34a8b795ee897`.

Sono nella cartella `studio2/fase03/piano_statistico/` del candidato.
Il manifest impronta sei file del delta, senza se stesso, e le fonti pinnate.
Questo prompt e la consegna successiva hanno funzione di reperimento, non sono
parte del tree candidato. Leggi le modifiche e le sezioni correnti pertinenti,
il record D9 e la sua consegna/matrice; usa i blob esatti, non HEAD mobili.

1. **Acquisizione OK**: `16f227439357b07b7dc945f67ab5a4368c12b684..5b784219b08de1249636536ac98e9a546b4d4577`,
   due file (verbale e record). Verifica provenienza, candidato/tree e
   byte-identità: 20.816 B,
   `9248c42572a20388ddf5af976840e68fdc908e545312a63234167778ce53a256`.
   Fonte originale:
   `/Users/luker/fot-tep-verifica-correzioni-allineamenti-03-8-rev10/studio2/fase03/piano_statistico/VERIFICA_CORREZIONI_ALLINEAMENTI_03_8_REV10.md`.
   Preserva anche il NON OK e la catena precedente.
2. **Acquisizione D9**: `5b784219b08de1249636536ac98e9a546b4d4577..dc4d6560af73579300e33a0a81fc9c3b4316722d`,
   tre blob selettivi da `aaba893dff8c62f9f9281eec7423eee020235e03` più record di provenienza;
   nessuna fusione del branch D9. Confronta i tre byte/hash/dimensioni con
   `git show aaba893dff8c62f9f9281eec7423eee020235e03:studio2/fase03/<file>` e le due voci artifacts del JSON.
   Il manifest D9 non si auto-impronta: il suo SHA è nel record di acquisizione.
3. **Recepimento documentale**: `dc4d6560af73579300e33a0a81fc9c3b4316722d..8a20c125bd294191c67ebdbf571832b1e32ac0f1`,
   solo piano generale, APERTURA e cinque nuovi record della cartella 03.8.
   Verifica matrice file→modifica→motivazione→controllo del report e coerenza
   risultante limitatamente alle conseguenze di D9, senza rifare R1–R4.

Limite dei link acquisiti: il record D9 rinvia a
`PROPOSTA_D9_RUOLI_MODELLI_2026-09-14.md`, volutamente non acquisita. Non correggere
il record byte-identico. Verifica recuperabilità con
`git show 95ff8571af02bab79094ed1a6be3f6a7b410c711:studio2/fase03/PROPOSTA_D9_RUOLI_MODELLI_2026-09-14.md`:
36.141 B, SHA-256 `a47f42dda7ee9702c292e34ada6b116ac3c85e42ec3a50e68af97c159f0d0f9d`.
Il suo percorso originale e il comando sono nel record di acquisizione D9.
Anche il rinvio assoluto alla vecchia proposta harness è storico, non prova
lo stato del candidato R01–R10 in correzione. Non importare documenti mancanti
né candidati harness; registra distintamente questa eccezione ereditata.

## Controlli richiesti

- Cinque stati distinti e coerenti: ruoli approvati; record acquisito;
  recepimento documentale locale preparato; recepimento eseguibile harness
  pendente; identità/configurazioni/qualificazioni/fattibilità pendenti.
- P=C=122B, P_alt=27B, **libreria completa di 16 insight**, consumer 122B fisso
  nello swap. Terra solo storico descrittivo interno, separato dalle nuove
  stime, senza nuove chiamate. Nessun 27B consumer fallback approvato.
- Le affermazioni correnti non chiedono nuovamente la scelta D9. Stati storici
  nei record verificati restano immutati; nessuna attribuzione retroattiva D9
  alla rev.10. Nomi nominali e operatività non diventano qualificazione.
- **Ordine label 1a non approvato**, firma materiale 03.8, dettagli operativi,
  qualificazione e autorizzazioni al pilot/chiamate restano separati.
  Nessun nuovo budget, calendario, revisione o metadato tecnico inventato.
  Nessuna selezione autonoma di quartetto swap, `a`, riusi o X/Q.
- Rev.10 e contabilità restano intatte; P=C non duplica richieste coincidenti
  né azzera il ledger. Contatore canonico R4 non sostituito dalla scelta C.
- A/B, FAR, U3, 03.5, 03.9 e 03.12 non riaperti; freeze statistico → 03.11/OOD
  resta nell'ordine vigente. Harness e 03.11 non diventano prerequisiti
  circolari del freeze statistico.
- Verifica byte-identità dei 47 file statistici preesistenti a 16f2274 e dei
  19 artefatti +6 input del manifest rev.10 contro hash e blob pinnati.
  Non rieseguire test scientifici. Rapporti, manifest e verbali storici,
  vecchia matrice e consegna tecnica restano intatti; successori espliciti.
- Nessuna modifica/importazione di codice, configurazioni o documenti harness
  R01–R10; nessuna modifica di paper_sections 03.15 o walkthrough MD/HTML.
- Verifica JSON, sei impronte del nuovo manifest, fonti e link introdotti
  (13 occorrenze al candidato); registra l'eccezione ereditata sopra.
  `git diff --check dc4d6560af73579300e33a0a81fc9c3b4316722d 8a20c125bd294191c67ebdbf571832b1e32ac0f1` e controllo acquisizioni.
- Riesegui soltanto il guardiano documentale `python3 docs/test_explanation.py`,
  catturando il log fuori dai documenti scientifici. Attesi **35 test,
  14 fallimenti storici, 1 skip, 0 errori, exit 1**. Confronta **identificativi
  e sottocasi** coi JSON prima/dopo, non solo i conteggi; non definirlo PASS.
  Nessuna API, inferenza, simulazione o pilot.

## Verbale di uscita

Prima riga **OK** oppure **NON OK**, con oggetto e limiti effettivi. Indica
identità reale del revisore, candidato/tree/base/main osservati, file e fonti,
esiti per acquisizione e nuovo delta, controlli eseguiti e mancati, eventuali
rilievi puntuali con fonte e conseguenza. Chiudi con byte/SHA-256 del verbale
comunicati all'orchestratrice **fuori dal file stesso**, evitando auto-hash.
Un eventuale OK non firma 03.8, non approva 1a, non qualifica servizi, non
integra/pubblica/congela e non autorizza chiamate. 03.8 e Fase 03 restano aperte.
