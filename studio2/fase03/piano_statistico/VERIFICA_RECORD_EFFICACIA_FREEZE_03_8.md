**Verdetto: OK.**

Review indipendente e **read-only** del solo record post-tag di efficacia del
piano statistico 03.8. L'OK è limitato al commit candidato
`0b0b2ee2a168d14dc6e46dd8334aebbab311a08e`, tree
`f2e6b67a0cc5d4420cbd08fc5c238c9c6860d237`, contro la base
`11f504b2bf45a39c1bc4746952f50d58c5022743`, e al solo file aggiunto
`studio2/fase03/piano_statistico/PROVA_REMOTA_FREEZE_PIANO_STATISTICO_03_8_2026-09-15.json`.
Non corregge file, non pubblica e non crea, sposta o sostituisce alcun tag.
Nessun commit, push, merge, tag, freeze aggiuntivo, firma, chiamata a servizi,
inferenza, simulazione o pilot. Il verbale non è committato.

## Perimetro

- Base: `11f504b2bf45a39c1bc4746952f50d58c5022743` (commit pubblicato e taggato).
- Candidato: `0b0b2ee2a168d14dc6e46dd8334aebbab311a08e` (branch
  `codex/studio2-efficacia-freeze-038`).
- Tree: `f2e6b67a0cc5d4420cbd08fc5c238c9c6860d237`; genitore unico `11f504b`.
- Delta (`diff --name-status 11f504b..0b0b2ee`): **un solo file aggiunto**, il
  record JSON; nessun altro file. `git diff --check`: pulito.

## Identità della sessione di review (dichiarata, non attestata da terzi)

- Modello effettivo: **claude-opus-4-8** (Claude Opus 4.8); provider **Anthropic**;
  sessione **Claude (Cowork)** `https://claude.ai/code/session_01H6p2273pdNzgi85fei134V`.
  Non è il modello suggerito (`gpt-6-astra`, reasoning high): divergenza di
  esecuzione dichiarata. Reasoning effort non configurato come parametro separato,
  quindi non attestato come «high».
- Indipendenza: finestra distinta dal preparatore; analisi condotta leggendo gli
  oggetti Git dall'object database e da archivi isolati dei due commit, senza
  modificare il worktree preparatore.

## Controlli 1–12

**1 — Identità e perimetro.** Base e candidato esistono; il candidato ha tree
`f2e6b67` e unico genitore `11f504b`, coincidenti con le identità dichiarate; il
delta aggiunge esattamente il solo JSON (143 inserzioni, 0 cancellazioni).

**2 — Record.** Blob del candidato: **6.773 byte**, SHA-256
`2c011bba8b02e3c357cfe62ea90d63f75527d0690186846d5e385e8e79a44f97` (= attesi).
JSON valido.

**3 — Remoto (live).** `git ls-remote`: `refs/heads/main` =
`11f504b…2743` (contiene ed è il target). Il tag restituisce l'oggetto
`bfcf6e5b3840c5b7dc3f7ace1085843d18cfddc7` e `^{}` = `11f504b…2743`. Main non è
avanzato oltre il target; raggiungibilità del target confermata.

**4 — Tag dal database locale.** Il ref è di tipo `tag` (annotato), punta a un
commit; oggetto `bfcf6e5`, target/peeled `11f504b`, target tree
`c4da62906fe434ea7e8f514dc72f9e0c4e7b4b71`, tagger «Luca Sorrentino
<lucaso@elkjop.no>» ts `1789491395 +0200`, messaggio: tutti **identici** ai campi
del record. Oggetto e peeled locali **coincidono** con i remoti.

**5 — Assenza di firma.** L'oggetto tag non contiene blocco PGP/SSH
(`-----BEGIN …` assente). I metadati `tagger` sono metadati Git dell'oggetto
annotato e il record li dichiara esplicitamente **non** una firma materiale.

**6 — Preservazione dei blob al commit taggato `11f504b`.** Ricalcolati dai blob:
piano rev.10 81.490 B / `675dbbcc…032a`; manifest finale pre-tag 14.768 B /
`087d268d…413d`; verbale OK 8.694 B / `5f6a600a…af8d`; acquisizione 4.160 B /
`293219f3…c6bd`; manifest storico FREEZE 25.894 B / `a69c4f68…80f8`; manifest
candidato finalizzazione 12.382 B / `bcc9ef18…4dc6`. **Tutti conformi**; nessuno
modificato dopo review o tag. `MAINTENANCE.md` invariato dal delta.

**7 — Catena e confini.** Verificata `a5798c6` → `ec807db` → `7a42bb6` →
`11f504b` (ogni genitore riscontrato). Il manifest pre-tag verificato (`ec807db`,
OK su `a5798c6..ec807db`) e il verbale acquisito (`5f6a600`) sono raggiungibili
dal tag. Gli OK precedenti restano ai propri perimetri e non sono estesi.

**8 — Esclusione di `f944efd`.** Il commit
`f944efd2872786d439c22b38302d33e91d08cfab` (proposta pre-pubblicazione) **non** è
antenato del candidato, del target `11f504b` né di `origin/main`, e **non**
compare nella storia candidata. È la punta di `codex/studio2-finalizzazione-038`,
ma il branch efficacia è stato creato direttamente da `11f504b`.

**9 — Semantica degli stati.** `freeze_effective=true` descrive l'evento remoto
già verificato (pubblicazione + tag annotato + peeled remoto). `record_verified=false`,
`record_published=false`, `subphase_03_8_closed=false`, `phase_03_closed=false`
impediscono una chiusura anticipata; `next_required_events` elenca review,
acquisizione, pubblicazione e verifica di raggiungibilità del record prima di
documentare la chiusura.

**10 — Nessuna auto-impronta/auto-commit.** Il record non contiene il proprio
SHA-256 né il futuro commit candidato (`record_candidate.candidate_commit=null`,
`candidate_tree=null`); l'identità è rinviata alla consegna successiva. Non ci
sono target futuri inventati.

**11 — Nessun filone riaperto.** Il record non riapre né implica audit
scientifici, decisioni A/B/D9, harness, servizi, controlli OOD, inferenze,
simulazioni o pilot; le proibizioni elencate lo ribadiscono. `operations_during_record_preparation`
riporta 0 push, 0 tag creati/modificati, 0 chiamate, 0 run.

**12 — `git diff --check` e guardiano.** `diff --check`: pulito. Guardiano
`docs/test_explanation.py` su base e candidato: **NON PASS in entrambi — 35 test,
14 fallimenti storici (walkthrough v1), 1 skip**, flussi per-test identici,
nessuna regressione. Non classificato PASS. Il delta è un solo JSON non letto dal
guardiano.

## Distinzione richiesta

- **Efficacia del tag:** il freeze statistico 03.8 **è effettivo** — la catena
  pre-tag revisionata è pubblicata e il tag annotato risolve, in locale e sul
  remoto, esattamente a quella catena (oggetto `bfcf6e5`, peeled `11f504b` =
  `origin/main`).
- **Verifica/pubblicazione del record:** questo record post-tag è ancora
  `record_verified=false` e `record_published=false`; il presente verbale è la
  sua review indipendente, ma la sua acquisizione byte-identica e la
  pubblicazione restano da compiere.
- **Chiusura della sottofase:** 03.8 **non** è chiusa e la Fase 03 **non** è
  chiusa; la chiusura è subordinata a verifica, pubblicazione e verifica di
  raggiungibilità del record.

## Rilievi

**Bloccanti:** nessuno, entro il perimetro del delta.

**Osservazioni non bloccanti:**

1. Divergenza fra modello suggerito (`gpt-6-astra`) e modello effettivo
   (`claude-opus-4-8`); dichiarata, non incide sul contenuto verificato.
2. La barriera di chiusura resta procedurale: `freeze_effective=true` non implica
   chiusura; i flag `record_*`/closures false vanno mantenuti finché il record
   non è verificato e pubblicato.

## Conferma

Il presente verdetto **non modifica e non ripubblica il tag**, non tocca piano,
manifest o commit taggato, e non dichiara chiusa la sottofase 03.8 né la Fase 03.
