# Consegna acquisizione letteratura — Fase 03

## 1. Identificazione ed esito

- **ID operativo:** supporto bibliografico Fase 03, dipendenza di chiusura della sottofase **03.8 — Piano statistico**. Non costituisce una nuova sottofase scientifica numerata.
- **Data:** 2026-09-14, Europe/Rome.
- **Attività:** acquisizione conservativa del candidato bibliografico già verificato, del verbale indipendente e dei due rendering PNG usati per la verifica delle tabelle PHM; preparazione della consegna per il successivo raccordo seriale con `main`.
- **Esito:** **COMPLETATO LOCALMENTE**. Le 23 impronte del candidato coincidono con l'inventario e con lo snapshot indipendente; il verbale è stato acquisito byte-identico in un commit separato. Nessun nuovo delta scientifico è emerso.
- **Limite del verdetto:** l'OK è esclusivamente bibliografico. Non approva il piano statistico 03.8, selezioni OOD, generabilità tecnica, fattibilità operativa, esecuzioni sperimentali o congelamenti.

Il rapporto scientifico preesistente era già incluso nell'inventario verificato e ne è stata preservata l'impronta; per questo non è stato riscritto. Il presente file è una consegna operativa successiva e separata.

## 2. Worktree e riferimenti Git

- **Worktree:** `/Users/luker/fot-tep-letteratura-fase03`
- **Branch:** `codex/studio2-letteratura-fase03`
- **Base originaria del candidato non committato:** `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155`
- **Commit candidato:** `e37c3db66689325b703bb99f3750ca3b5b287aab` — `studio2(letteratura): acquisisce candidato bibliografico verificato`
- **Commit verbale:** `40911d0e3e7b75960e6973f3fd8f609e65ab6e05` — `studio2(letteratura): acquisisce verbale indipendente`
- **HEAD finale prima della creazione di questa consegna:** `40911d0e3e7b75960e6973f3fd8f609e65ab6e05`
- **`origin/main` controllato localmente e sul remoto:** `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`
- **Divergenza del branch rispetto a `origin/main`:** 2 commit avanti e 30 indietro. Questa divergenza è attesa: non è stato eseguito rebase, merge o cherry-pick perché il raccordo deve preservare gli aggiornamenti degli altri cantieri già presenti in `main`.

## 3. File acquisiti

### 3.1 Commit del candidato `e37c3db`

Il commit contiene **esattamente 23 file**, per **6.407.129 byte** complessivi.

File tracciati preesistenti modificati:

- `/Users/luker/fot-tep-letteratura-fase03/docs/letteratura.md`
- `/Users/luker/fot-tep-letteratura-fase03/docs/letteratura.html`
- `/Users/luker/fot-tep-letteratura-fase03/docs/paper/FoT_TEP_paper_blueprint.html`
- `/Users/luker/fot-tep-letteratura-fase03/papers/README.md`

File nuovi di analisi e controllo:

- `/Users/luker/fot-tep-letteratura-fase03/docs/lit_review/VERIFICA_CORPUS_FASE03.json`
- `/Users/luker/fot-tep-letteratura-fase03/docs/lit_review/VERIFICA_FONTI_FASE03.json`
- `/Users/luker/fot-tep-letteratura-fase03/docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md`

Nuove coppie paper Markdown/PDF:

- `/Users/luker/fot-tep-letteratura-fase03/papers/Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.md`
- `/Users/luker/fot-tep-letteratura-fase03/papers/Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.pdf`
- `/Users/luker/fot-tep-letteratura-fase03/papers/Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.md`
- `/Users/luker/fot-tep-letteratura-fase03/papers/Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.pdf`
- `/Users/luker/fot-tep-letteratura-fase03/papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.md`
- `/Users/luker/fot-tep-letteratura-fase03/papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.pdf`
- `/Users/luker/fot-tep-letteratura-fase03/papers/Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.md`
- `/Users/luker/fot-tep-letteratura-fase03/papers/Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.pdf`
- `/Users/luker/fot-tep-letteratura-fase03/papers/Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.md`
- `/Users/luker/fot-tep-letteratura-fase03/papers/Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.pdf`
- `/Users/luker/fot-tep-letteratura-fase03/papers/The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.md`
- `/Users/luker/fot-tep-letteratura-fase03/papers/The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.pdf`
- `/Users/luker/fot-tep-letteratura-fase03/papers/The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.md`
- `/Users/luker/fot-tep-letteratura-fase03/papers/The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.pdf`

Rendering PHM esplicitamente inclusi nonostante la regola di ignore:

- `/Users/luker/fot-tep-letteratura-fase03/papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/page-6.png` — 286.075 byte — SHA-256 `0d4174ce35e88e941540b722ff1d632b5a0ed6527f66aeed7d2089eb6d4f2bf8`
- `/Users/luker/fot-tep-letteratura-fase03/papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/page-7.png` — 557.127 byte — SHA-256 `020f08386172d87c5ca45fecabc30a402904498bbb60754a745a4520104bed91`

Nessun'altra immagine o file ignorato è stato incluso. Dopo il commit, `git ls-files --others -i --exclude-standard` restituiva zero percorsi.

### 3.2 Commit del verbale `40911d0`

- `/Users/luker/fot-tep-letteratura-fase03/docs/lit_review/VERIFICA_INDIPENDENTE_LETTERATURA_FASE03.md`
- Dimensione: **30.107 byte**.
- SHA-256: `551f7da9de20096f3a21f6f9a19d2beecd4b03367bbf6cbe4d083f482637ddaf`.
- Il commit contiene un solo file; contenuto, dimensione e SHA sono identici alla sorgente `/Users/luker/fot-tep-verifica-letteratura-fase03/docs/lit_review/VERIFICA_INDIPENDENTE_LETTERATURA_FASE03.md`.

### 3.3 Rapporti, verbali e inventario pertinenti

- **Rapporto scientifico/addendum verificato e preservato:** `/Users/luker/fot-tep-letteratura-fase03/docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md`, 34.808 byte, SHA-256 `f2c29416664e27c2ecac7d439939f51f1a3f7313e2aba669bb39db7106cf0b8e`.
- **Verbale indipendente acquisito:** `/Users/luker/fot-tep-letteratura-fase03/docs/lit_review/VERIFICA_INDIPENDENTE_LETTERATURA_FASE03.md`.
- **Inventario autorevole letto in sola lettura:** `/Users/luker/fot-tep-piano-statistico-fix/studio2/fase03/piano_statistico/ACQUISIZIONE_LETTERATURA_03_8.json`.
- **Handoff orchestrativo letto in sola lettura:** `/Users/luker/fot-tep/studio2/fase03/HANDOFF_FASE03_2026-09-14_rev02.md`, soprattutto §4.12.
- **Questa consegna operativa:** `/Users/luker/fot-tep-letteratura-fase03/docs/lit_review/CONSEGNA_ACQUISIZIONE_LETTERATURA_FASE03_2026-09-14.md`.

Non è stato importato l'intero snapshot `/Users/luker/fot-tep-verifica-letteratura-fase03`: ne è stato acquisito soltanto il verbale indipendente. L'inventario 03.8 resta nella propria sede autorevole e non è stato duplicato nel branch bibliografico.

## 4. Controlli svolti e risultati

1. **Preflight Git e concorrenza.** Controllati branch, HEAD, worktree registrati, modifiche preesistenti, remoti e `main` remoto prima di scrivere. Il candidato risultava non committato su base `a572d1c`; `origin/main` risultava già a `c486eee`.
2. **Inventario candidato.** Ricalcolati dimensione e SHA-256 dei 23 percorsi nella sorgente e nello snapshot indipendente: **23/23 coincidenti**, totale **6.407.129 byte**, zero divergenze.
3. **Indice Git.** Prima del primo commit verificato che l'indice contenesse esattamente i 23 percorsi inventariati. Ricalcolati byte e SHA dai blob staged: **23/23 coincidenti**.
4. **Oggetto Git candidato.** Dopo il commit, ricalcolati byte e SHA leggendo direttamente `e37c3db:<percorso>`: **23/23 coincidenti**.
5. **PNG.** Verificati separatamente percorso, dimensione, SHA e modalità Git dei soli `page-6.png` e `page-7.png`; entrambi sono recuperabili dal commit `e37c3db` come file `100644`.
6. **Verbale.** Verificati con `cmp`, `wc -c`, SHA-256, blob staged e oggetto committato: **30.107 byte e SHA dichiarato coincidenti**. Il secondo commit contiene esattamente un percorso.
7. **Perimetro protetto.** Ricalcolate le 23 impronte protette elencate nell'inventario: **23/23 invariate**. Il registro congelato non è stato modificato; la discrepanza PHM F9–SPE resta documentata nell'addendum senza correzione retroattiva.
8. **Contenuto scientifico e coppia MD/HTML.** `docs/letteratura.md` e `.html`, blueprint, README, rapporto e JSON conservano esattamente le impronte dello snapshot verificato. La verifica indipendente documenta per la coppia 182 righe tabellari equivalenti, 40 schede nello stesso ordine e nessuna aggiunta sostanziale inversa.
9. **Guardiano documentale.** `python3 docs/test_explanation.py`: **35 test, 14 fallimenti, 1 skip, 0 errori**. Esito identico a base e verifica indipendente; i 14 fallimenti riguardano walkthrough preesistenti e il test non certifica §14.
10. **Raccordo con `main`.** Eseguita simulazione Git a tre vie, senza aggiornare ref o worktree, fra i due commit e `origin/main` `c486eee`: nessun conflitto. Il risultato simulato conserva i quattro documenti condivisi come modifiche e aggiunge i 20 nuovi file complessivi, verbale incluso.

### Limiti e rilievi non corretti

- `git diff --check` segnala whitespace già presente nelle conversioni raw di tre paper e in un PDF interpretato come testo. Non è stato normalizzato: una modifica avrebbe violato la richiesta di preservare le impronte del candidato verificato.
- La corrispondenza delle impronte dimostra che è stato committato il candidato verificato; non estende la verifica scientifica oltre il perimetro e i limiti dichiarati nel verbale.
- Yin resta verificato soltanto per metadati/abstract; Maurer, Westfall e Kish conservano i limiti di accesso dichiarati. Nessun numero non letto è stato promosso a prova.
- L'OK bibliografico non dimostra la generabilità di F6, non seleziona F6/F4 come OOD e non sostituisce la verifica statistica o tecnica delle sottofasi pertinenti.

## 5. Stato Git finale

Stato dopo la creazione di questa consegna, senza ulteriori commit:

- **Committati:** i 23 file del candidato in `e37c3db` e il verbale indipendente in `40911d0`.
- **Modificati ma non committati:** nessuno.
- **Non tracciati:** soltanto `/Users/luker/fot-tep-letteratura-fase03/docs/lit_review/CONSEGNA_ACQUISIZIONE_LETTERATURA_FASE03_2026-09-14.md`.
- **Staged:** nessuno.
- **Ignorati non tracciati:** nessuno nel worktree bibliografico dopo l'inclusione esplicita dei due PNG.
- **Branch:** `codex/studio2-letteratura-fase03`, HEAD `40911d0`, avanti 2 e indietro 30 rispetto a `origin/main`.

Questa richiesta di consegna non autorizza il commit del presente report; il file deve pertanto restare non tracciato finché l'orchestratore non deciderà come acquisirlo insieme al raccordo.

## 6. Integrazione, pubblicazione e congelamento

- **Integrazione in `main`: non eseguita.** I due commit sono locali sul branch bibliografico.
- **Pubblicazione remota: non eseguita.** Nessun push.
- **Tag/congelamento: non eseguito.** Nessun tag creato o spostato.
- **Stato effettivo:** acquisizione locale completata e pronta per il raccordo; non ancora raggiungibile da `origin/main`.
- **Fase 03:** resta aperta. Questa consegna non chiude 03.8 né la Fase 03.

## 7. Residui, dipendenze e prossimo passo

### Operazioni residue

1. In una finestra orchestratrice con un solo writer, raccordare i due commit al `main` allora corrente, senza usare il vecchio branch come sostituto del nuovo `main`.
2. Acquisire integralmente i 19 nuovi file del candidato e il verbale; raccordare sul contenuto corrente gli hunk dei quattro file condivisi:
   - `docs/letteratura.md`;
   - `docs/letteratura.html`;
   - `docs/paper/FoT_TEP_paper_blueprint.html`;
   - `papers/README.md`.
3. Dopo il raccordo reale, ricontrollare impronte dei file scientifici importati, parità MD/HTML, link, conteggi, stato Git e guardiano rispetto al `main` effettivo. La simulazione senza conflitti non sostituisce questi controlli post-integrazione.
4. Acquisire o committare questa consegna soltanto se l'orchestratore lo include esplicitamente nel proprio commit di coordinamento; non mescolarla retroattivamente nei due commit già separati.

### Dipendenze e decisioni

- La chiusura 03.8 dipende ancora dalla firma materiale dell'atto rev. 10, dagli allineamenti con piano generale/APERTURA/preflight/harness, dalla verifica indipendente del delta integrato, dalla documentazione e dal successivo processo di integrazione/pubblicazione/tag.
- Le decisioni A/B, D2, D11, margine, alpha, gerarchia e politica R risultano già approvate secondo l'handoff e non devono essere richieste nuovamente.
- L'interpretazione della distinzione meccanica F6/F4, la generabilità tecnica e l'esecuzione dei controlli OOD restano nei rispettivi perimetri; 03.11 opera dopo il freeze statistico secondo la regola B approvata.
- D9 e i ruoli dei modelli restano una decisione separata e non sono modificati dalla letteratura acquisita.

### Prossimo passo raccomandato

L'orchestratore deve integrare serialmente `e37c3db` e `40911d0` nel `main` corrente preservando gli aggiornamenti degli altri cantieri, quindi svolgere i controlli post-raccordo. Solo dopo tale acquisizione la bibliografia può essere considerata disponibile in `main` come dipendenza della chiusura 03.8.
