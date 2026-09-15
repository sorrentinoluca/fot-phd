**Verdetto: OK.**

Review indipendente e **read-only** del solo manifest finale pre-tag della
sottofase 03.8. L'OK è limitato al commit candidato
`ec807dbaf2cb745ba96d397aac64a981f6fdeb7d`, tree
`58ffd0b057dee7c1a1c399aaadd6c256d8658e34`, contro la base
`a5798c667dedcb85d3b745258fbc992e0c05841a`, e al solo file aggiunto
`studio2/fase03/piano_statistico/MANIFEST_FINALE_PRE_TAG_03_8.json`. Non si
estende ai successori (consegna e prompt), al commit pubblicato `8dbd2b4`, al
futuro tag né a byte successivi. Nessun file corretto, nessuna pubblicazione,
nessun tag, nessun push/merge/freeze/firma/chiamata/inferenza/simulazione/pilot.
Il verbale non è stato committato.

## Perimetro

- Base: `a5798c667dedcb85d3b745258fbc992e0c05841a`.
- Candidato: `ec807dbaf2cb745ba96d397aac64a981f6fdeb7d`.
- Tree candidato: `58ffd0b057dee7c1a1c399aaadd6c256d8658e34`.
- Genitore unico: `a5798c667dedcb85d3b745258fbc992e0c05841a`.
- File del delta: `studio2/fase03/piano_statistico/MANIFEST_FINALE_PRE_TAG_03_8.json`.
- Remoto: `https://github.com/sorrentinoluca/fot-phd.git`.

## Identità della sessione di review (dichiarata, non attestata da terzi)

- Modello effettivamente in esecuzione: **claude-opus-4-8** (famiglia Claude
  Opus 4.8). **Non** è il modello suggerito dal prompt (`gpt-6-astra`).
- Provider: **Anthropic**; esecuzione in una sessione **Claude (Cowork)**.
- Reasoning effort: non configurato come parametro separato «high»; non lo si
  dichiara per non inventare dati.
- Identità sessione: `https://claude.ai/code/session_01H6p2273pdNzgi85fei134V`.
- Ambiente: contenitore cloud Anthropic con accesso in sola lettura al
  repository dell'autore via bridge del dispositivo; analisi condotta leggendo
  gli oggetti Git direttamente dall'object database
  (`git --git-dir=<repo>/.git …`), senza fidarsi di alcun working tree; guardiano
  eseguito su archivi completi (`git archive`) dei due commit in directory
  isolate e scartabili. Nessun worktree Git creato nel repository dell'autore.

## Controlli 1–12

**1 — Oggetti, tree, genitore, perimetro.** `cat-file -t` conferma commit per
base e candidato e tree per `58ffd0b`. Il candidato ha `tree 58ffd0b` e **un
solo** genitore `a5798c6` (dichiarato). `diff --name-status a5798c6..ec807db`
restituisce **una sola** riga: `A studio2/fase03/piano_statistico/MANIFEST_FINALE_PRE_TAG_03_8.json`
(338 inserzioni, 0 cancellazioni). Nessun altro file.

**2 — Manifest: JSON, dimensione, SHA-256.** Blob del candidato: **14.768 byte**,
SHA-256 `087d268d438ca6e98063346a5547849a05235a43712aebe56e007c46dcc1413d`
(entrambi = attesi). JSON valido (`json.load`).

**3 — 31/31 boundary_artifacts.** Conteggio = **31**; percorsi **tutti univoci**;
per ciascuno dimensione e SHA-256 sono stati **ricalcolati dal blob nel tree
candidato** (non ereditati): **0 discrepanze su 31**. Il file del manifest non
compare fra gli artefatti di confine.

**4 — Byte-identità delle fonti citate.** Verificati byte per byte dal tree
candidato: piano rev.10 `PIANO_STATISTICO.md` 81.490 B /
`675dbbcc…032a`; `PIANO_STATISTICO_FREEZE.json` 25.894 B / `a69c4f68…80f8`;
manifest candidato precedente `MANIFEST_CANDIDATO_FREEZE_03_8.json` 12.382 B /
`bcc9ef18…4dc6`; le decisioni, i verbali e le acquisizioni citati (rev.10, R1–R4,
D9, approvazione documentata, finalizzazione) coincidono con le impronte
registrate. Il delta aggiunge **solo** il manifest: nessuno di questi file è
modificato. Anche `supersedes_for_future_freeze` e il `publication_record`
(ESITO) coincidono con i blob (2.982 B / `fcff6986…d922`, `published=false`).

**5 — Catena e identità della finalizzazione.** Verificata con Git la catena
lineare, ogni genitore riscontrato:
`6490af4` → `4c9e7a1` → `03a7d76` → `8dbd2b4` → `39a3e57` → `a5798c6` →
`ec807db`. Il commit pubblicato registrato è `8dbd2b4`, tree
`d1d2a0bb3b5247190340a9d091452e55099d6a18` (= genitore-tree verificato). Il
record distingue chiaramente il **commit pubblicato** `8dbd2b4` dal proprio
**commit locale non pubblicato**: `pre_tag_candidate.candidate_commit=null` (nel
corpo), `publication_record.published=false` per `a5798c6`, ed ESITO/CONSEGNA
dichiarano i successori locali (`39a3e57`, `a5798c6`, `ec807db`) non raggiungibili
dal main remoto.

**6 — Fonte remota effettiva.** `git ls-remote origin refs/heads/main` **live** =
`8dbd2b49176c16f9e100e5f181c729b99d406a35`: `refs/heads/main` **contiene**
`8dbd2b4` (ne è la punta) ed è raggiungibile; `merge-base --is-ancestor` conferma
`8dbd2b4` antenato di `origin/main`. Il remoto **non** è avanzato oltre il commit
pubblicato; `previous_main` registrato `a006058` è coerente con la pubblicazione
fast-forward (`a006058..8dbd2b4` = **23 avanti, 0 indietro**). Nessuna
contraddizione di provenienza, nessuna mancata raggiungibilità.

**7 — Tag `studio2-fase03-piano-statistico-frozen-001`.** Assente in locale
(`tag -l` vuoto) e sul remoto (`ls-remote --tags` vuoto per quel nome). Non
comparso dopo il candidato; verdetto non esteso ad alcun tag.

**8 — Flag di non efficacia e valori nulli.** `freeze_effective=false`,
`subphase_03_8_closed=false`, `phase_03_closed=false`; nel corpo
`candidate_commit=null`, `candidate_tree=null`; tag `target_commit=null`,
`tag_object=null`, `peeled_commit=null`, `remote_verified=false`;
`independent_review`, `review_acquisition` e `publication` = `pending`.

**9 — Nessuna auto-impronta o target inventato.** Il manifest **non** contiene la
propria dimensione/SHA e **non** si elenca fra gli artefatti; il proprio percorso
compare **solo** in `excluded_self_references` (con consegna, prompt e record
futuri), senza byte né SHA. L'identità del candidato è rinviata alla consegna
successiva `CONSEGNA_MANIFEST_FINALE_PRE_TAG_03_8.md`. Nessun target futuro
(commit tag/peeled) è anticipato.

**10 — Cinque checkpoint OK a perimetri distinti.** I `reviewed_checkpoints`
(rev.10, R1–R4, D9 documentale, approvazione documentata, delta di
finalizzazione) mantengono ciascuno il proprio ambito; le impronte dei rispettivi
verbali coincidono con i blob. In particolare l'OK di finalizzazione è
esplicitamente limitato a `6490af4..4c9e7a1`, tree `03b2159`, e agli **otto** file
allora verificati, con acquisizione a `8dbd2b4`; non è esteso al presente
manifest.

**11 — Filoni separati, non circolari.** `separate_pending_dependencies` marca
`false` e non-circolari: ordine label 1a, harness D9 runtime, identità/config e
qualifica servizi, T5/fattibilità operativa, controlli OOD 03.11. Firma materiale
non richiesta (nessun artefatto sottoscritto; `DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.*`
assente). Le proibizioni del manifest ribadiscono questi confini.

**12 — `git diff --check` e guardiano.** `git diff --check a5798c6..ec807db`:
**pulito**. Il delta è un solo file JSON e non tocca coppie MD/HTML né input del
guardiano. Guardiano `docs/test_explanation.py` eseguito su base e candidato:
**NON PASS in entrambi**, **35 test, 14 fallimenti (storici, preesistenti,
walkthrough v1), 1 skip**; flussi verbose e header di fallimento **identici** fra
base e candidato (nessuna regressione). Esito **non** classificato PASS.

## Rilievi

**Bloccanti:** nessuno.

**Osservazioni non bloccanti:**

1. I documenti di provenienza (ESITO/CONSEGNA/ACQUISIZIONE) annotano che il
   verbale di finalizzazione precedente non recava un'impronta pre-attestata dal
   revisore: l'impronta 11.988 B / `03cb0613…a763` è stata **calcolata in fase di
   acquisizione**. Riscontro: quell'impronta coincide con il blob attualmente nel
   tree candidato e con il valore registrato nei `reviewed_checkpoints`; coerente,
   nessuna azione richiesta.
2. Il presente verbale dichiara un'identità di sessione (modello Claude Opus 4.8,
   Anthropic) **diversa** dal modello suggerito nel prompt (`gpt-6-astra`, high).
   È una divergenza di esecuzione, non del candidato; segnalata per trasparenza.

## Portata e limiti

L'esito **non pubblica**, **non congela**, non chiude 03.8 né la Fase 03 e **non
certifica i successori** (consegna, prompt, futuri verbale/acquisizione/
pubblicazione/tag). Non riapre gli audit rev.10, R1–R4, D9 o le decisioni
dell'autore. Il NON PASS del guardiano è storico/preesistente. La verifica remota
vale al momento indicato: `origin/main` va ricontrollato prima di ogni
pubblicazione o creazione di tag successiva.

## Consegna per l'acquisizione byte-identica

File nuovo, non tracciato, non committato. Percorso assoluto, dimensione, SHA-256
e stato Git sono comunicati nella nota di consegna della sessione (l'hash non è
incluso nel corpo per evitare auto-riferimento), così che una finestra successiva
possa acquisirlo byte-identico.
