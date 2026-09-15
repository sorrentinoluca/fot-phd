# Verifica indipendente del candidato di finalizzazione 03.8

**OK.**

Verdetto **OK** limitato esclusivamente al commit
`4c9e7a1f1d8bd07b7d6be8df724f743986717da8`, tree
`03b215980ae170db2e1284dd7bd5eb07b830fb28`, contro la base
`6490af4889fd679d491f63b9debdf2314eaf7aca` e ai soli otto file del delta
elencati sotto. L'OK **non** si estende ad altri byte, ad altri commit (in
particolare al successore `03a7d76` che aggiunge consegna e prompt), agli audit
scientifici già conclusi, né alla pubblicabilità sul `main` remoto corrente.

Data verifica: 2026-09-15. Natura: review **read-only e indipendente**. Non sono
stati eseguiti push, merge, tag, freeze, firma, chiamate a servizi, inferenze,
simulazioni, pilot o run. Non è stato modificato il candidato. Questo verbale
**non è stato committato**.

## Metodo e isolamento

La review è stata condotta leggendo gli oggetti direttamente dall'object database
Git reale al commit fissato, senza fidarsi di alcun working tree:

```
git --git-dir=<repo>/.git cat-file -p 4c9e7a1:<path>      # blob del candidato
git --git-dir=<repo>/.git diff --name-status 6490af4 4c9e7a1
git --git-dir=<repo>/.git ls-remote origin refs/heads/main   # remoto live
```

Il guardiano è stato eseguito su checkout completi e puliti di **entrambi** gli
alberi, estratti con `git archive <commit> | tar -x` in directory isolate e
scartabili (nessun worktree Git creato nel repository dell'autore, per non
lasciare riferimenti di percorso). L'indipendenza dal working tree del
preparatore è così garantita: ogni impronta e ogni confronto derivano dal commit
`4c9e7a1` e dalla base `6490af4`.

## Identità confermate

| Elemento | Atteso | Osservato | Esito |
| --- | --- | --- | --- |
| remoto | `https://github.com/sorrentinoluca/fot-phd.git` | idem (origin fetch/push) | OK |
| candidato | `4c9e7a1…717da8` | commit presente | OK |
| tree candidato | `03b2159…30fb28` | `rev-parse 4c9e7a1^{tree}` = idem | OK |
| genitore unico | `6490af4…af7aca` | un solo genitore = idem | OK |
| base delta | `6490af4…af7aca` | commit presente | OK |
| origin/main osservato | `a006058…00135f` | ref locale = idem; **`ls-remote` live = idem (non avanzato)** | OK |

`origin/main` risulta antenato della base; la base è **20 avanti, 0 indietro**
rispetto a `origin/main` (catena lineare di 20 commit). Al momento della verifica
il `main` remoto non è avanzato oltre `a006058`, quindi non è oggi necessario un
delta di integrazione; **la ricognizione va comunque ripetuta subito prima della
pubblicazione**, perché la raggiungibilità locale non prova la raggiungibilità su
`origin/main`.

## Perimetro del delta — esattamente 8 file

`diff --name-status 6490af4..4c9e7a1` (nessun file oltre questi):

```
M docs/fot_walkthrough_conversazione_studio2.html
M docs/fot_walkthrough_conversazione_studio2.md
M docs/paper/FoT_TEP_Review_Piano_Sperimentale.md
M studio2/fase03/APERTURA_SOTTOFASI_FASE03.md
M studio2/fase03/piano_statistico/COORDINAMENTO_CHIUSURA_03_8.md
A studio2/fase03/piano_statistico/MANIFEST_CANDIDATO_FREEZE_03_8.json
M studio2/fase03/piano_statistico/MATRICE_RESIDUI_03_8_DOPO_D9.md
A studio2/fase03/piano_statistico/REPORT_FINALIZZAZIONE_03_8.md
```

Totale: 8 file (6 M, 2 A), 436 inserzioni / 40 rimozioni. Nessuna cancellazione,
nessun file fuori dall'elenco atteso. `git diff --check 6490af4 4c9e7a1`: **pulito**.

## Esito dei controlli richiesti

**1 — Impronte preservate.** Nel tree candidato:
`PIANO_STATISTICO.md` = **81.490 byte**, SHA-256
`675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a` (atteso, OK);
`PIANO_STATISTICO_FREEZE.json` = **25.894 byte**, SHA-256
`a69c4f684d93b4d4665a3b3c58e96406ef5efbdc779c5a708ea7fe5a510f80f8` (atteso, OK).
Presenti e non toccati dal delta: `DELTA_HARNESS_03_10.md`, coppia
`DESIGN_RESOLUTION.{json,md}`, decisioni, verbali e acquisizioni (rev.10, R1–R4,
D9, approvazione documentata). Poiché il delta tocca solo gli 8 file sopra, ogni
altro artefatto è byte-identico alla base.

**2 — MANIFEST_CANDIDATO_FREEZE_03_8.json.** **12.382 byte**, SHA-256
`bcc9ef183190e2fd0997b2e600fc53498e4a6194993e997820255a4b6d124dc6` (atteso, OK).
JSON valido. **23/23** artefatti: ogni voce coincide per percorso, dimensione e
SHA-256 con il blob nel tree candidato (0 discrepanze, riverificate blob per blob).
**20/20** voci di catena: ogni `parent` dichiarato coincide con il genitore Git
reale del `commit`; catena contigua da `a006058` (origin/main) a `6490af4`
(base). Nessun auto-riferimento fra gli artefatti (manifest, report, consegna e
prompt sono elencati solo in `excluded_self_references`). `freeze_effective=false`,
`phase_03_closed=false`; `published_commit`, `candidate_commit`, `candidate_tree`,
`freeze_tag.target_commit`, `tag_object`, `peeled_commit` tutti **null**;
`remote_verified=false`.

**3 — Raccordo (COORDINAMENTO + APERTURA + piano generale) fedele.** D2=8
confermato (64 fault + 8 Normal = 72 primari; 6 OOD + 11 scorte tecniche = 89 del
lotto, scorte senza nuove osservazioni). D11 confermato ({F1,F2}/{F14,F15}).
OOD F6/F4 condizionati. Margine (m=0,125), alpha, gerarchia e politica R
approvati. **Tetto rigido 3.700 non vigente**: gli addendum A e B risultano
**APPROVATI senza modifiche** (`APPROVAZIONE_ADDENDUM_03_8.md`, commit
`526561f`, 2026-09-14), quindi vale il conteggio completo per blocco/modello e la
**fattibilità temporale misurata con margine 20% (1,20 × T ≤ W)**, con
sospensione organizzativa se non fattibile; 3.700 resta solo nota storica. Il
paper generale recepisce esattamente questo («il tetto rigido 3.700 non è
vigente… conteggio completo e fattibilità temporale misurata con margine 20%»).
Controlli OOD della 03.11 collocati **dopo il freeze e prima delle chiamate**.
Nessuna dipendenza circolare 03.8→03.11→03.8 sul tag (esplicitato in APERTURA:
«nessun risultato 03.11 richiesto prima del tag»).

**4 — D9 (senza riaprirla).** `MATRICE_RESIDUI_03_8_DOPO_D9.md` riporta
fedelmente: **P=C=122B**, **P_alt=27B** con libreria alternativa completa di **16
insight**, consumer 122B fisso nello swap; **Terra solo storico descrittivo
interno**, senza nuove chiamate. È marcato che l'OK documentale **non qualifica il
runtime** (recepimento eseguibile e qualifica servizi pendenti). Consumer 27B
fallback non approvato.

**5 — Approvazione documentata vs firma.**
`DECISIONE_AUTORE_APPROVAZIONE_DOCUMENTATA_03_8_2026-09-15.md` stabilisce che
l'approvazione documentata è sufficiente e **non** richiede firma materiale, e che
**non** deve essere creato o richiesto `DECISIONI_AUTORE_03_8_SOTTOSCRITTE_REV10.*`
(verificato **assente** dall'intero tree). Il pacchetto firma e il relativo
verbale OK restano **storici** (istruzioni di sottoscrizione non più operative,
byte preservati). La decisione **non** approva l'ordine label 1a e **non**
autorizza esecuzioni.

**6 — Stato.** 03.8 è dichiarata **«in finalizzazione locale»** in APERTURA
(riga tabella e header), matrice, report e coordinamento; **Fase 03 aperta**;
pubblicazione e freeze non anticipati (`freeze_effective=false`). Il candidato
harness **`6a8031b` resta esterno e NON OK per R-D9-01/R-D9-02** e non è stato
importato (nessuna sua traccia nel tree né nella catena).

**7 — Parità MD/HTML e markup.** Coppia
`docs/fot_walkthrough_conversazione_studio2.{md,html}` aggiornata insieme (nuova
§4.8 «Fase 03 — piano statistico (sotto-fase 03.8)»). Testo normalizzato della
§4.8: **HTML ⊆ MD = 100%**, **MD ⊆ HTML = 96,5%**; gli unici token solo-MD sono
nomi di file nei link (estensioni `.md`/`.json`, frammenti di percorso) che in
HTML stanno negli attributi `href`: la prosa visibile è identica. Anchor: **21
id, tutti unici**; **59 frammenti interni** risolvono; **201 link relativi**
risolvono; markup bilanciato. Non modificati il walkthrough divulgativo
(`fot_walkthrough_studio2.html`) né `paper_sections/` (fuori dal delta).

**8 — `git diff --check` e guardiano.** `diff --check`: pulito. Guardiano della
documentazione `docs/test_explanation.py` (invariato nel delta) eseguito su base
e candidato: **NON PASS in entrambi — Ran 35 tests, failures=14, skipped=1**. I
14 identificativi di fallimento e i relativi sottocasi sono **identici** fra base
e candidato (flusso verbose confrontato riga per riga: streams identici); sono
fallimenti **preesistenti** relativi ai walkthrough v1 (`UnifiedConversationChecks`:
`test_step27_qwen_frozen_results_and_limitations`,
`test_step27_qwen_protocol_stable_facts`,
`test_condition_c_contract_and_caveats`,
`test_one_flow_and_ordered_step_headings`), coerenti con la nota di
`docs/MAINTENANCE.md` §5 (14 preesistenti). **Nessuna regressione, nessuna nuova
firma di fallimento.** Questo esito **non** è dichiarato PASS.

**9 — Fonti e assenza tag remoto.** Tutte le fonti indicate dal manifest sono
recuperabili dal tree candidato (23/23 verificate) e le fonti D9
(`DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md`, `CONSEGNA_RECEPIMENTO_D9_2026-09-14.md`,
`IMPRONTE_DECISIONE_D9_2026-09-14.json`) sono nel tree con impronte conformi.
Nessuna dipendenza operativa da `/tmp` nei file del delta (grep: 0 occorrenze).
Il tag remoto previsto `studio2-fase03-piano-statistico-frozen-001` è **assente**
su `origin` (`ls-remote --tags` live: presenti altri `*-frozen-001`, non questo);
non creato.

**10 — Sequenza proposta.** Il report propone: review → acquisizione byte-identica
→ pubblicazione autorizzata con catena raggiungibile da `origin/main` →
eventuale manifest efficace come delta separato e sua review → tag annotato sul
commit finale allora identificato → verifica remota di oggetto tag e `^{}` peeled.
Coerente e non circolare. Nessun auto-riferimento, nessun target inventato,
nessun byte normativo pubblicato senza review: identità del candidato registrate
nel successore `CONSEGNA_FINALIZZAZIONE_03_8.md` (commit `03a7d76`, dopo il
candidato), così manifest e report non contengono la propria impronta.

## Rilievi

**Bloccanti:** nessuno.

**Non bloccanti (osservazioni):**

1. `COORDINAMENTO_CHIUSURA_03_8.md` §2 mantiene la formulazione **condizionale**
   del budget («finché A è pending o respinta, mantenere 3.700 … Se A è
   approvata, sostituire …»). Poiché A è approvata, il ramo vigente è «conteggio
   completo + fattibilità 20%», già applicato nel paper generale, in APERTURA e
   in matrice: il risultato è quindi coerente, ma il coordinamento resta scritto
   come guida-delta a due rami anziché asserire lo stato risolto. Non impatta il
   verdetto.
2. `COORDINAMENTO_CHIUSURA_03_8.md` §1 documenta una **futura** acquisizione
   bibliografica con percorsi locali esterni (`/Users/luker/fot-tep-letteratura-fase03`
   e uno snapshot «senza .git»). È uno step futuro, separato e verificabile a sé,
   non una dipendenza operativa del delta di finalizzazione: il candidato in sé
   non dipende da `/tmp` né da altri worktree. Da trattare nella propria finestra
   con provenienza e sede di conservazione concordate.

## Limiti del verdetto

- Circoscritto a `4c9e7a1` / tree `03b2159` contro `6490af4` e agli 8 file del
  delta; nessuna estensione ad altri byte o commit.
- Non ripete gli audit rev.10, R1–R4, D9 e approvazione documentata: ne verifica
  identità e portate, senza estenderne gli OK.
- Il NON PASS del guardiano è storico/preesistente (walkthrough v1); l'OK
  documentale non qualifica il runtime (harness D9, servizi, fattibilità).
- `origin/main` verificato non avanzato **a questo istante**; da ricontrollare
  prima della pubblicazione.
- La verifica non dichiara 03.8 pubblicata, chiusa o congelata, né chiusa la
  Fase 03.

## Consegna per l'acquisizione byte-identica

Questo verbale è un file nuovo, non tracciato e non committato. Percorso,
dimensione e SHA-256 sono comunicati nella nota di consegna della sessione per la
successiva acquisizione byte-identica in un commit documentale separato (l'hash
non è incluso nel corpo del file per evitare auto-riferimento).
