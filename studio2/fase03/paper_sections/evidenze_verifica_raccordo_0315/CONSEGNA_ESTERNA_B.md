# Consegna dell'integrazione locale e della documentazione 03.15

**ID della sotto-fase:** `S2-F03-0315` — Fase 03, sotto-fase 03.15
**Data:** 2026-09-14, Europe/Rome
**Attività svolta:** integrazione locale della storia verificata 03.15 sulla base comune,
acquisizione byte-identica della consegna operativa e documentazione coordinata MD/HTML.
**Esito:** candidato locale completato e committato; nessun merge in `main`, push, tag o freeze.
**Perimetro:** sotto-fase 03.15 e Fase 03 ancora aperte.

Questo record documenta un raccordo Git e documentale successivo all'OK indipendente. Non è un
nuovo verbale scientifico e non estende gli OK esistenti al merge o al walkthrough.

## 1. Riferimenti esatti

| Oggetto | Commit |
| --- | --- |
| `origin/main` e main remoto al preflight | `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` |
| Base comune richiesta | `e82b5a08bf642ad45f77e71832958207beb1181c` |
| Candidato scientifico storico, OK distinto | `cf79e81f917c7969dfd375e38db54315c28d4c07` |
| Nuovo candidato scientifico verificato | `91a880b136dee5d805b54040f5e32345be361eb2` |
| Pacchetto con verbale acquisito | `d35b684acbfd1f357bc34f3a21cebb18e8a6bea0` |
| Merge locale del pacchetto sulla base comune | `18aa3bbf1284a41e20bdc4fc521c98c315ca9614` |
| Acquisizione distinta della consegna 03.15 | `705f1c4ca61375d51bb69f20e0de613cfb39bf1a` |
| Walkthrough MD/HTML 03.15 | `532cc77bc3d5d046161b6334e1a7b24ac1e7019f` |

Worktree dedicato: `/Users/luker/fot-tep-raccordo-0315-local`; branch
`codex/studio2-raccordo-0315-local`. Il merge `18aa3bb` ha esattamente due genitori, nell'ordine
`e82b5a0` e `d35b684`. I worktree del raccordo seriale precedente, dell'harness e proprietario
paper-sections non sono stati modificati. Il commit di riferimento del candidato locale è
`9b6bd64c3e23f03d09272dda43c1a043305add50`.

## 2. Conflitto risolto e contenuti preservati

L'unico conflitto effettivo è stato `studio2/PROVENIENZA.md`. Sono state mantenute integralmente
le sezioni 1–13 della base; la 03.15 usa il primo numero libero effettivo, §14, e il suo delta di
allineamento è §14.1. Non è stata ereditata la numerazione non assegnata del vecchio ramo paper.

Al commit di merge, `studio2/fase03/paper_sections/` coincide con `d35b684`. Dopo il merge, le
sole aggiunte nella cartella sono la consegna operativa acquisita nel commit distinto `705f1c4`
e il presente record. Bozze scientifiche, report improntato, `FONTI_DELTA_0315.json` e verbali
non sono stati riscritti.

Impronte ricontrollate:

| File | Byte | SHA-256 |
| --- | ---: | --- |
| `VERIFICA_DELTA_0315.md` | 12.311 | `00553079e88a58a68762ba9a3400c04cb22b91f6a99f37f191b67cfd12ca9770` |
| `REPORT_DELTA_0315.md` | 15.498 | `1f59eabf8070f1f4b7b77d89564d4e3593308469e8d8aee56676c93dbabd40f1` |
| `VERIFICA_PAPER_SECTIONS.md` | 13.949 | `8faca80c87071d87bf66d97848c290a5724f6569be6f6040cfb6568bad022cb1` |
| `FONTI_DELTA_0315.json` | — | `dc01cd71e1b7bae0b65a56de0de50c6db8ac2db426cb471b5110fc7a8d694610` |
| `CONSEGNA_0315_2026-09-14.md` | 16.615 | `7469790613d644673bec6629ac7fb1ceae53aefdcbe45ae94239b687705aef2b` |

La consegna acquisita è byte-identica al file non tracciato del worktree proprietario. Il
registro `FONTI_DELTA_0315.json` conserva 54 fonti e il proprio stato storico.

## 3. Walkthrough e delta da riesaminare

La nuova §4.15 è collocata dopo §4.12 e prima della sintesi di Fase 03. Sono stati aggiornati
insieme indice/stato, sezione lunga, tabella riassuntiva e voce §6.12 in:

- `docs/fot_walkthrough_conversazione_studio2.md`;
- `docs/fot_walkthrough_conversazione_studio2.html`.

La sintesi divulgativa non è stata modificata: 03.15 è un passaggio redazionale interno e non
produce un esito da sintetizzare. Le bozze non sono state promosse in `docs/paper/`.

**Delta documentale per il prossimo raccordo seriale:**
`705f1c4ca61375d51bb69f20e0de613cfb39bf1a..532cc77bc3d5d046161b6334e1a7b24ac1e7019f`.
Va riesaminato per coerenza, parità, link, anchor e numerazione. Questa review documentale non
deve ripetere la review scientifica già conclusa sul candidato `91a880b`.

## 4. Controlli

- `lint_paper_sections.py --corpus docs/letteratura.md`: 5 file, 0 segnalazioni.
- Parità della nuova §4.15 dopo rendering: 4.132 caratteri normalizzati in entrambe le forme,
  confronto esatto positivo.
- HTML del walkthrough: 19 identificativi, tutti univoci; 186 link locali, 0 mancanti.
- `git diff --check`: nessuna segnalazione sui nuovi delta.
- Guardiano prima sulla base `e82b5a0`, dopo il merge e dopo il walkthrough: 35 test, gli stessi
  14 fallimenti storici, 1 skip, 0 errori. I 14 identificativi con relativi parametri dei subtest
  coincidono con `CONTROLLI_DELTA_0315.json`. Python 3.11.5.
- Ascendenze: `e82b5a0` e `d35b684` sono genitori del merge; `91a880b`, `cf79e81` e le storie
  03.6/03.12/letteratura restano raggiungibili dal candidato locale.

Il guardiano è un controllo di regressione documentale e non una prova del merito scientifico.
Non sono stati rieseguiti calcoli, bootstrap, simulazioni, inferenze o chiamate API.

## 5. Limiti e residui

L'OK storico su `cf79e81`, l'OK del nuovo delta su `91a880b` e l'acquisizione in `d35b684`
restano distinti. Il raccordo e la documentazione successiva non ricevono automaticamente quegli
OK. Se un futuro conflitto richiederà un cambiamento scientifico, dovrà essere separato e
verificato sul nuovo delta.

Restano irrisolti D9 e l'assegnazione dei ruoli dei modelli, identità e qualificazione del
servizio, firma materiale e freeze statistico della 03.8, fattibilità T5, ledger/calendario,
raccordi 03.10 e controlli tecnici OOD della 03.11. FAR e A/B non sono stati riaperti. Non sono
stati prodotti risultati diagnostici, abstract o conclusioni. Il candidato locale resta distinto
da una futura integrazione in `main`, pubblicazione o congelamento.

## 6. File creati o modificati e documenti pertinenti

Percorsi modificati rispetto alla base comune `e82b5a0`:

| Stato | Percorso |
| --- | --- |
| M | `docs/fot_walkthrough_conversazione_studio2.md` |
| M | `docs/fot_walkthrough_conversazione_studio2.html` |
| M | `studio2/PROVENIENZA.md` |
| A | `studio2/fase03/paper_sections/PIANO_SEZIONI.md` |
| A | `studio2/fase03/paper_sections/related_work.md` |
| A | `studio2/fase03/paper_sections/method.md` |
| A | `studio2/fase03/paper_sections/verbalizer.md` |
| A | `studio2/fase03/paper_sections/protocol.md` |
| A | `studio2/fase03/paper_sections/threats.md` |
| A | `studio2/fase03/paper_sections/lint_paper_sections.py` |
| A | `studio2/fase03/paper_sections/FONTI_DELTA_0315.json` |
| A | `studio2/fase03/paper_sections/CONTROLLI_DELTA_0315.json` |
| A | `studio2/fase03/paper_sections/PROMPT_VERIFICA_DELTA_0315.md` |
| A | `studio2/fase03/paper_sections/REPORT_PAPER_SECTIONS.md` |
| A | `studio2/fase03/paper_sections/REPORT_ACQUISIZIONE_VERIFICA_PAPER_SECTIONS.md` |
| A | `studio2/fase03/paper_sections/REPORT_DELTA_0315.md` |
| A | `studio2/fase03/paper_sections/VERIFICA_PAPER_SECTIONS.md` |
| A | `studio2/fase03/paper_sections/ACQUISIZIONE_VERIFICA_PAPER_SECTIONS.md` |
| A | `studio2/fase03/paper_sections/VERIFICA_DELTA_0315.md` |
| A | `studio2/fase03/paper_sections/ACQUISIZIONE_VERIFICA_DELTA_0315.md` |
| A | `studio2/fase03/paper_sections/CONSEGNA_0315_2026-09-14.md` |
| A | `studio2/fase03/paper_sections/CONSEGNA_INTEGRAZIONE_LOCALE_0315_2026-09-14.md` |

Report, verbali e record da leggere, con percorsi assoluti:

- report storico:
  `/Users/luker/fot-tep-raccordo-0315-local/studio2/fase03/paper_sections/REPORT_PAPER_SECTIONS.md`;
- verbale storico su `cf79e81`:
  `/Users/luker/fot-tep-raccordo-0315-local/studio2/fase03/paper_sections/VERIFICA_PAPER_SECTIONS.md`;
- acquisizione del verbale storico:
  `/Users/luker/fot-tep-raccordo-0315-local/studio2/fase03/paper_sections/ACQUISIZIONE_VERIFICA_PAPER_SECTIONS.md`;
- report del nuovo delta:
  `/Users/luker/fot-tep-raccordo-0315-local/studio2/fase03/paper_sections/REPORT_DELTA_0315.md`;
- verbale indipendente sul candidato `91a880b`:
  `/Users/luker/fot-tep-raccordo-0315-local/studio2/fase03/paper_sections/VERIFICA_DELTA_0315.md`;
- acquisizione del nuovo verbale:
  `/Users/luker/fot-tep-raccordo-0315-local/studio2/fase03/paper_sections/ACQUISIZIONE_VERIFICA_DELTA_0315.md`;
- consegna operativa acquisita:
  `/Users/luker/fot-tep-raccordo-0315-local/studio2/fase03/paper_sections/CONSEGNA_0315_2026-09-14.md`;
- presente consegna aggiornata:
  `/Users/luker/fot-tep-raccordo-0315-local/studio2/fase03/paper_sections/CONSEGNA_INTEGRAZIONE_LOCALE_0315_2026-09-14.md`.

## 7. Stato Git finale della presente richiesta

- **HEAD e commit di riferimento:** `9b6bd64c3e23f03d09272dda43c1a043305add50`.
- **Branch:** `codex/studio2-raccordo-0315-local`.
- **File committati:** i 22 percorsi della tabella in §6 sono raggiungibili dal commit di
  riferimento; il presente report è stato creato e committato in `9b6bd64`.
- **File tracciati modificati e non committati:** soltanto il presente report, aggiornato da
  questa richiesta per completezza.
- **File staged:** nessuno.
- **File non tracciati:** nessuno.
- Nessun altro file del worktree è stato modificato per questa richiesta.
- Nessun commit, merge, push o tag è stato eseguito per questo solo aggiornamento del report.

## 8. Integrazione, pubblicazione e congelamento effettivi

| Oggetto | Stato effettivo |
| --- | --- |
| Delta scientifico `bcb462d..91a880b` | OK indipendente acquisito; perimetro limitato al candidato verificato |
| Pacchetto `d35b684` | storia e verbale preservati nel candidato locale |
| Raccordo su `e82b5a0` | completato soltanto nel branch locale tramite merge `18aa3bb` |
| Walkthrough 03.15 | MD/HTML committati in `532cc77`; nuovo delta documentale da riesaminare |
| Integrazione in `main` | non eseguita; `origin/main` e main remoto restano a `c486eee` |
| Pubblicazione | nessun push; candidato disponibile soltanto nel repository locale |
| Congelamento | nessun tag o freeze creato; nessun OK esteso al merge o al walkthrough |
| Promozione in `docs/paper/` | non eseguita |
| Chiusura 03.15 / Fase 03 | entrambe aperte |

## 9. Dipendenze, decisioni e prossimo passo

Dipendenze ancora operative: firma e freeze statistico 03.8; raccordi e ledger 03.10;
controlli OOD 03.11; identità, tokenizer, configurazione e qualificazione del servizio; verifica
della fattibilità T5 e del calendario. D9 richiede ancora una decisione dell'autore sui ruoli di
producer principale, consumer e alternativo. Non vanno riaperte FAR o le decisioni A/B già
registrate.

Il prossimo passo è una review del solo delta documentale
`705f1c4ca61375d51bb69f20e0de613cfb39bf1a..532cc77bc3d5d046161b6334e1a7b24ac1e7019f`
nel successivo raccordo seriale, controllando parità MD/HTML, link, anchor, numerazione e
coerenza con i cantieri concorrenti. Non va ripetuta la review scientifica su `91a880b`.
Soltanto dopo tale raccordo e una futura autorizzazione potranno essere valutati integrazione in
`main` e pubblicazione; il congelamento resta separato e subordinato ai propri prerequisiti.
