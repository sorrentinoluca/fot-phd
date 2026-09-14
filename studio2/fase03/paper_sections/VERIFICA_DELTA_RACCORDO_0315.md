# Verifica indipendente del delta documentale 03.15 (raccordo locale)

**Delta verificato:** `9b6bd64c3e23f03d09272dda43c1a043305add50..10582798eb5a4b52672bfbcb1cc028adcb73e9f1`
**Data:** 2026-09-14, Europe/Rome
**Verificatore:** Claude Cowork, modello configurato `claude-opus-4-8` (Claude Opus 4.8), Anthropic — sessione `session_013BLwcitiaqnqjNBLvV2mhH`. Reasoning/effort non esposto.
**Esecutore del delta:** commit firmati `Luca Sorrentino <lucaso@elkjop.no>` (base e candidato). L'agente/modello esecutore non è stato identificato in modo indipendente: nessun log Codex locale accessibile da questa sessione (`~/.codex/archived_sessions/` vuoto o non leggibile). L'indipendenza poggia sul fatto che questa sessione ha riderivato ogni fatto dagli oggetti Git e dalle fonti primarie, senza fidarsi delle asserzioni del delta.

## Verdetto: **OK** sul solo delta `9b6bd64..10582798`

OK qualificato. Il delta è **puramente documentale**: corregge due passaggi della §4.15 del walkthrough (MD e HTML in parallelo) rendendoli più precisi e più prudenti. Le due nuove affermazioni sono **verificate vere** contro le fonti primarie. Questo OK non estende alcun OK scientifico storico (`cf79e81`, `91a880b`), non integra nulla in `main`, non pubblica, non firma alcuna revisione e non chiude 03.15 né la Fase 03.

## Perimetro e genealogia

- Delta = **un solo commit** `10582798`, il cui unico genitore è **esattamente** la base `9b6bd64`. Catena lineare.
- File toccati dal delta: **solo** `docs/fot_walkthrough_conversazione_studio2.md` e `docs/fot_walkthrough_conversazione_studio2.html` (2 file, +18/−14). Nessun altro file, nessun blob del pacchetto o delle fonti modificato.
- Ascendenza a monte (ricostruita): merge `18aa3bb` (due genitori nell'ordine `e82b5a0` base comune, `d35b684` pacchetto) → `705f1c4` (acquisizione consegna operativa) → `532cc77` (walkthrough §4.15) → `9b6bd64` (base) → `10582798` (candidato).
- `origin/main` al preflight = `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`.
- Il commit base `9b6bd64` ha introdotto `CONSEGNA_INTEGRAZIONE_LOCALE_0315_2026-09-14.md` (95 righe): è la fonte primaria del raccordo, ma **non** contiene lo split 44/8/2 — quel dato è stato verificato in modo indipendente (sotto).

## Contenuto del delta e sua veridicità

**Modifica 1 — raggiungibilità delle fonti.** Il testo precedente diceva genericamente che «storia, fonti, bozze e verbali» sono raggiungibili dal candidato locale. Il delta lo precisa in: «**44 delle 54 fonti** registrate raggiungibili nell'ascendenza; delle restanti, **8** su commit esterni non antenati e **2** fonti locali senza commit».

Verifica indipendente su `FONTI_DELTA_0315.json` (54 fonti; SHA-256 `dc01cd71e1b7bae0b65a56de0de50c6db8ac2db426cb471b5110fc7a8d694610`, coincide con l'impronta dichiarata nella CONSEGNA):

| Commit fonte | Fonti | Antenato di `10582798`? |
| --- | ---: | --- |
| `c486eee` (S05, S09, MAIN-provenienza) | 21 | **sì** |
| `c66bd8d` (S06) | 6 | **sì** |
| `3c64390` (S12) | 3 | **sì** |
| `40911d0` (L) | 3 | **sì** |
| `1d480fd` (BASE) | 11 | **sì** |
| `6aaa5b3` (S08) | 6 | **no** |
| `51782e8` (S08-consegna) | 2 | **no** |
| `None` (H, PROMPT-0315) | 2 | fonti locali senza commit |

Somma: **44 raggiungibili + 8 su commit esterni non antenati (S08 + S08-consegna) + 2 locali senza commit = 54**. Corrisponde **esattamente** al claim. Verificato con `git merge-base --is-ancestor` per ciascun commit.

**Modifica 2 — file del pacchetto e consegne.** Il testo precedente diceva che `paper_sections/` era identica a `d35b684` «salvo questa consegna aggiunta» (una sola). Il delta lo corregge in: «**17 file del pacchetto** invariati rispetto a `d35b684`; dopo il pacchetto aggiunte **due consegne**: la consegna operativa 03.15 e la consegna dell'integrazione locale».

Verifica indipendente:
- `paper_sections/` a `d35b684` = **17 file**; a `10582798` = **19 file**. Il `git diff d35b684 10582798` sulla cartella mostra **solo** le due consegne aggiunte (+343 righe), **zero** modifiche ai 17 file del pacchetto → «17 file invariati» confermato byte per byte.
- `CONSEGNA_0315_2026-09-14.md` aggiunta dal commit distinto `705f1c4`; SHA-256 `7469790613d644673bec6629ac7fb1ceae53aefdcbe45ae94239b687705aef2b` a `705f1c4` = al candidato → «acquisita byte-identica in un commit locale distinto dal merge» confermato.
- `CONSEGNA_INTEGRAZIONE_LOCALE_0315_2026-09-14.md` aggiunta dal commit base `9b6bd64`.
- Entrambi i link relativi nel walkthrough risolvono a file esistenti sotto `paper_sections/`.

## Integrità di tutte le 54 fonti

52 fonti committate: **tutte** con `path→sha256` corrispondente all'oggetto Git al commit dichiarato (52/52, 0 discrepanze, 0 mancanti). 2 fonti locali non tracciate (H `b7d47c75…`, PROMPT-0315 `1eca1053…`): impronte corrispondenti ai file vivi. **54/54 OK.**

## Parità MD/HTML

I due passaggi modificati sono, dopo normalizzazione (rimozione tag/marcatori/link), **parola per parola identici** tra `.md` e `.html`. Numeri, link e frasi coincidono nelle due forme.

## Controlli eseguiti al candidato

- `git diff --check` sul delta: **pulito**.
- Link nuovi: entrambi i target esistono nell'albero del candidato.
- **Guardiano** `python3 docs/test_explanation.py` in worktree distaccato al candidato: **35 test, 14 fallimenti, 1 skip, 0 errori** — coincide con `CONTROLLI_DELTA_0315.json` (`tests_after=35, failures_after=14, skips_after=1, errors_after=0`).
- **Non-regressione**: guardiano rieseguito anche alla base `9b6bd64`; l'insieme dei 14 fallimenti è **identico** (stessi identificativi e sottotest) tra base e candidato. Sono arretrati storici (step27/Qwen frozen results e stable facts), **non** regressioni introdotte dal delta, che non tocca le affermazioni testate su quei punti. Il delta non introduce né risolve alcun fallimento.
- Ambiente: venv Python **3.10.12** della VM di sessione (i `CONTROLLI_DELTA_0315.json` usano 3.11.5); esiti del guardiano identici, come già rilevato nella verifica 0315.

Il guardiano è un controllo di regressione documentale, non una prova del merito scientifico. Nessun calcolo, bootstrap, simulazione, inferenza o chiamata API è stato rieseguito.

## Limiti dichiarati

- Reasoning/effort del verificatore non esposto.
- Agente/modello esecutore non identificato in modo indipendente (log Codex non accessibili); verificata la sola identità del committer da metadati Git.
- Fonti, pacchetto e report letti dagli oggetti Git e verificati per impronta; nessun accesso al worktree proprietario dell'esecutore.
- Non riesaminati gli arretrati non bloccanti dei verbali storici; la review scientifica sul candidato `91a880b` non è stata ripetuta (fuori perimetro, per esplicita indicazione della CONSEGNA).
- Restano aperti, come dichiarato: D9 e ruoli dei modelli, identità/qualificazione del servizio, firma e freeze statistico 03.8, T5, ledger/calendario, raccordi 03.10, controlli OOD 03.11.

## Igiene

Creati due worktree distaccati di sola lettura per i test: `.worktrees/verifica-delta-raccordo-0315-10582798` (candidato) e `.worktrees/verifica-delta-raccordo-0315-base9b6bd64` (base). Restano in piedi (contengono log/ambiente dei test); l'autore può rimuoverli con `git worktree remove --force`. Nella VM di sessione restano lock Git orfani (`HEAD.lock`, `locked`) non rimovibili, innocui. Nessun commit, merge, push, tag o freeze.
