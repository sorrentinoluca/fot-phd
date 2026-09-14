# VERDETTO: OK sul nuovo delta 03.15 (candidato 91a880b) e sulla coerenza risultante delle cinque sezioni

OK qualificato limitato al delta scientifico `bcb462d..91a880b` e alla coerenza delle bozze comuni
del paper che ne risultano, a base `origin/main = c486eee`. Questo OK **non** eredita né sostituisce
l'OK storico del pacchetto `cf79e81`, **non** chiude la sotto-fase 03.15 né la Fase 03, **non** firma
la revisione 10 del piano statistico, **non** sceglie D9 e **non** autorizza pilot, integrazione o
pubblicazione. La verifica è in sola lettura; nessuna correzione è stata applicata alle bozze.

## Identità effettiva del revisore

Documentata dai metadati a cui questa sessione ha accesso; nessun campo dedotto dallo stile.

- **Modello dichiarato dalla configurazione di sessione:** `claude-opus-4-8` (Claude Opus 4.8).
  Il modello che serve il singolo turno può differire dall'identificativo configurato e non è
  esposto al runtime; dichiaro l'identificativo configurato, non una marca dedotta.
- **Provider:** Anthropic.
- **Reasoning/effort:** non esposto alla sessione. Dichiarato «non verificabile».
- **Prodotto/canale:** Claude (Cowork), sessione cloud Anthropic collegata al dispositivo locale
  tramite bridge remote-devices.
- **ID sessione:** `https://claude.ai/code/session_0156FoAbkYa4cWpud246SqXC`;
  ID task/dispositivo osservato nei percorsi di mount: `rcw-0156foabkya4cwpud246sqxc`.
- **Ruolo:** verificatore indipendente del solo nuovo delta.
- **Dispositivo:** `macbook-pro-local` (darwin arm64), cartella collegata unica `/Users/luker/fot-tep`
  (da `get_device_info`).
- **Worktree usato (creato per questa verifica, isolato al candidato):**
  `/Users/luker/fot-tep/.worktrees/verifica-delta-0315-91a880b`, **detached HEAD**
  `91a880b136dee5d805b54040f5e32345be361eb2`. Il percorso esterno suggerito nel prompt
  (`/Users/luker/fot-tep-verifica-delta-0315-91a880b`) è fuori dalla cartella montata da questa
  sessione e non era scrivibile; ho registrato un percorso alternativo isolato dentro `.worktrees/`.
- **Fonte delle identificazioni e limiti di accesso:** system prompt della sessione (identificativo
  del modello, URL di sessione), `get_device_info` (dispositivo, cartelle), Git. Non ho accesso al
  worktree dell'esecutore `/Users/luker/fot-tep-paper-sections` (fuori dalla cartella montata): ho
  quindi letto il candidato e le fonti dagli **oggetti Git** del repository `/Users/luker/fot-tep`
  e verificato per impronta il report consegnato, che è più robusto di una lettura del checkout altrui.

**Grado di indipendenza.** Provider diverso (Anthropic vs OpenAI), modello diverso (Opus 4.8 vs
`gpt-6-astra`), sessione diversa (`rcw-0156foabkya4cwpud246sqxc` vs task esecutore
`01a0a0bb-1683-7dd0-b29b-edfffb83de56`). Non è una rilettura dell'esecutore.

## Candidato, genealogia e preflight

- Genealogia lineare verificata: `cf79e81 → 50f07a9 → 1d480fd → bcb462d → 91a880b`
  (`git rev-parse <c>^` per ciascuno). `dc6e30c` (consegna soli documenti) è figlio diretto di `91a880b`.
- Delta scientifico da valutare: **`bcb462d..91a880b`** (8 file). Correzione documentale separata
  **`1d480fd..bcb462d`**: un solo file, una sola riga — «parent diretto» → «figlio diretto» in
  `REPORT_ACQUISIZIONE_VERIFICA_PAPER_SECTIONS.md`; `50f07a9` è effettivamente **figlio** di `cf79e81`,
  quindi la correzione è corretta.
- `origin/main` locale e `git ls-remote origin refs/heads/main` coincidono su
  **`c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`**, come registrato dal preflight dell'esecutore. ✅
- ⚠️ Il ref locale `main` (branch) è a `a572d1c`, diverso da `origin/main`: irrilevante per il
  candidato e per le fonti (tutte pinnate a commit espliciti), ma segnalato per igiene del repo.

## Integrità delle fonti e dei record protetti

- **Verbale storico** `VERIFICA_PAPER_SECTIONS.md` a `91a880b`: **13.949 byte**, SHA-256
  `8faca80c87071d87bf66d97848c290a5724f6569be6f6040cfb6568bad022cb1`. ✅ Byte-identico.
  Conserva il NON OK del passaggio 1 e l'OK del passaggio 2 (non riaperti).
- **Report consegnato** `REPORT_DELTA_0315.md` (blob di `dc6e30c`): SHA-256
  `1f59eabf8070f1f4b7b77d89564d4e3593308469e8d8aee56676c93dbabd40f1`. ✅ Coincide con l'atteso.
  Assente dal candidato `91a880b` (documento successivo), come dichiarato.
- **`FONTI_DELTA_0315.json`: 54 fonti.** 52 con commit verificate byte/SHA-256 via `git show`
  (tutte OK); 2 senza commit (file non tracciati) verificate sui file vivi:
  `HANDOFF_FASE03_2026-09-14_rev02.md` (48.244 byte, `b7d47c75…abff`) e
  `sottofase_3_15.md` (6.783 byte, `1eca1053…0ac1`). ✅ 54/54.

## Controlli scientifici (letti sulle fonti primarie ai commit pinnati)

1. **normal_dev reale e provenienza — ✅.** `SPECIFICA_NORMAL_DEV.md@c486eee`: 40 run, cinque in
   esclusiva per agente, Mode 1 `Ts_base=0.0005 h`, Philox4x32-10, chiave `0x464f545445503032`,
   stream **60000–60039** (disgiunti dai fault 30000–30039), 65 h/run con `[0,20)` e `[20,25)` esclusi,
   otto finestre `[25,65)` → **320 finestre da 40 cluster**, dichiarate dipendenti. Divieti
   (normalizzazione, soglie, FAR, selezione protocollo, test) e destinazione `normal_dev_002`,
   otto esempi pre-specificati (`agent_run_index=1`, `[25,30)`) corrispondono a `protocol.md`/`verbalizer.md`.
   `BASELINE_FREEZE_rev003.json` `effective=false` riportato come tale; deviazioni accettate non
   convertite in conformità.
2. **Baseline numerica — ✅.** `PROTOTYPES_MANIFEST.json@c486eee`: `dimensions=697`,
   `normal_signatures_global=320`, conteggi 40. Bozza: **9 globali + 16 locali = 25 vettori**, media
   aritmetica (40/fault, 320 Normal globale, 40 Normal locale), L1 media
   `d_c=(1/697)Σ|x_j−p_cj|`, pareggi entro **1e-12** → astensione (`abstain=true`,
   `predicted_label=null`), nessuna soglia di distanza/ripiego globale, scarto massimo registrato **0**
   presentato come controllo storico. Nessuna nuova prestazione.
3. **03.5 chiusa — ✅.** `THRESHOLD_FREEZE.json@c486eee`: `n=350`, `rank=334`,
   `threshold=13.623626738268857`, `rule="S > threshold"`, `score_ties_at_threshold=1`.
   `FAR_VERIFICATION.json@c486eee`: primario **11/150 = 0,07333**, Clopper–Pearson 95%; secondario
   **108/1500 = 0,072**, `bootstrap_seed=20260913`, `replicates=10000`, `unit=run`,
   SE `0,007512512137130144`, intervallo [0,05733; 0,08733]. Freeze `9507143…`; limite di accessibilità
   pre-freeze dichiarato e accettato; nessuna riapertura/ricalibrazione.
4. **Rev. 10 — ✅.** `PIANO_STATISTICO.md@6aaa5b3`: **D2=8** (64 cluster fault + 8 Normal primari = 72),
   sequenza fissa **H1→H2→H3** unilaterale **α=0,05**, decisioni locali **Hoeffding** (H1/H2) e
   **Tango** (H3) con controllo complessivo **approssimato** per Tango; **m=0,125** come massima perdita
   media netta senza garanzia individuale; **H3 a 0,025** sola sensibilità, A2-bis non adottato;
   bootstrap 10.000/seed come intervallo, non decisione. Le bozze conservano i limiti (garanzia finita
   condizionata, Tango asintotico, indipendenza cluster ignota). Firma materiale e freeze/tag distinti
   e **pendenti**.
5. **A e contabilità — ✅.** `BUDGET_RISORSE_REV10.md@6aaa5b3`: nucleo **1.728** (R=1) / **5.184** (R=3)
   distinto dal totale `N=2244R+…`; `k≈173`; tetto rigido **3.700 sostituito** (nessun tetto vigente);
   massimi **152/160** con riserva `8r+t≤15`; **hard stop cumulativo 200** che non finanzia altre
   chiamate (40 fra 160 e 200 non spendibili). Corrisponde a `protocol.md`.
6. **B e OOD — ✅.** OOD **F6/F4** condizionati, catene **F6→F5→F12** e **F4→F11→F5** intatte,
   D11 **{F1,F2}** e **{F14,F15}** run 1–3; controlli tecnici 03.11 **dopo** il freeze statistico e
   **prima** delle chiamate; sospensione se collisione su F5; undici scorte distinte dalle catene;
   nessun ritorno al ciclo 03.8→03.11.
7. **D9 e paper — ✅.** Handoff `HANDOFF_FASE03_2026-09-14_rev02.md`: 122B **dichiarato operativo**,
   alias `qwen3.5-122b`, contesto **131.072**, output **16.384**, temperatura omessa; 27B sull'altro
   server; 2.4T non ospitabile — tutti riportati fedelmente. Identità/qualificazione del servizio
   **aperte**; nessun ruolo assegnato a 27B/122B/Terra; producer-swap e alternativo D9.1 preservati;
   storico Terra non promosso a braccio controllato. Otto fault opachi + `Normal` letterale (nona) +
   `Unknown`=astensione; `Normal` senza insight. Blocco `VARIANTE D9` **byte-identico** nei tre file
   (`db11b3c4…`). Nessun risultato diagnostico, abstract o conclusione.
8. **Raccordi e perimetro — ✅.** `related_work.md`: unica modifica è l'annotazione del riferimento
   FedAvg/McMahan «candidato esterno identificato», nessun claim nuovo. `method.md`: solo raccordo D9
   e pin schema R4 (`insight_v1.schema.json@3c64390`). `PROVENIENZA.md`: solo sezione nuova in coda
   (19 inserimenti, 0 cancellazioni). Fonti bibliografiche disponibili al pin **L=`40911d0`** senza
   dichiararle integrate nel branch. Walkthrough, corpus, artefatti congelati e verbale indipendente
   preservati.

## Test e controlli meccanici (rieseguiti nel worktree isolato al candidato)

- `lint_paper_sections.py --corpus docs/letteratura.md` → **5 file, 0 segnalazioni, exit 0**. ✅
- `git diff --check bcb462d..91a880b` → **nessuna segnalazione, exit 0**. ✅
- `python3 docs/test_explanation.py` → **Ran 35 tests, failures=14, skipped=1, errors=0, exit 1**. ✅
  I 14 fallimenti coincidono uno-a-uno con `CONTROLLI_DELTA_0315.json`
  (`failure_identifiers_with_subtests`): 1× `test_condition_c_contract_and_caveats`
  (phrase «non un risultato empiricamente misurato»), 1× `test_one_flow_and_ordered_step_headings`,
  9× `test_step27_qwen_frozen_results_and_limitations` (parent + otto phrase), 3×
  `test_step27_qwen_protocol_stable_facts` (parent + doc='html' + doc='md'). Sono **arretrati storici**
  del walkthrough/Qwen in `UnifiedConversationChecks`, **estranei** al delta 03.15: nessuna nuova
  regressione introdotta dal delta.
- ⚠️ Ambiente: guardiano eseguito con **Python 3.10.12** (questa sessione) vs 3.11.5 dell'esecutore;
  conteggi e identificativi/subtest identici.
- Scansione token proibiti (`novel/first/unique/state-of-the-art`, percentuali di esito): nessun
  riscontro; gli unici «first» sono il nome della politica *local-first*. Nessun numero di esito nelle
  bozze (solo segnaposto `[RISULTATO: …]`).

## Limiti e note di igiene

- ⚠️ **H e prompt storico 03.15 non tracciati:** verificati per byte/SHA-256, ma privi di commit Git;
  limite dichiarato, coerente con il report. L'inventario 122B è comunicazione dell'autore riportata
  dall'handoff, non una misura del servizio.
- ⚠️ **Accesso al worktree dell'esecutore assente** (fuori cartella montata): candidato e fonti letti
  dagli oggetti Git; report consegnato verificato per impronta.
- ⚠️ **Lock Git orfani:** la creazione del worktree `.worktrees/verifica-delta-0315-91a880b` ha lasciato
  `HEAD.lock` e il file `locked` non rimovibili da questa sessione (nessun permesso di cancellazione
  sul disco). Non incidono sulle letture; l'autore può rimuovere il worktree
  (`git worktree remove --force .worktrees/verifica-delta-0315-91a880b`) e i lock residui.
- Gli arretrati non bloccanti del verbale storico (O2, O4–O7, O9, fonte handoff non tracciata,
  indipendenza cluster/applicabilità Tango, seed/data N1–N5, limiti del lint) restano identificabili
  in `VERIFICA_PAPER_SECTIONS.md` e **non** sono stati riesaminati, come richiesto.

## Perimetro dell'OK

OK sul solo delta `bcb462d..91a880b` e sulla coerenza delle cinque sezioni comuni a base `c486eee`.
Restano fuori e aperti: firma materiale e freeze/tag di 03.8; decisione D9 (producer principale,
consumer, alternativo, configurazione) e identificazione di D9.1; fattibilità T5, ledger e calendario;
implementazione 03.10, qualificazione servizio, controlli tecnici OOD 03.11; risultati diagnostici,
abstract, conclusioni e promozione in `docs/paper/`. Nessun commit/merge/push/tag; nessuna simulazione,
inferenza o chiamata sperimentale eseguita.

---
Revisore: Claude Opus 4.8 (`claude-opus-4-8`), Anthropic — sessione `session_0156FoAbkYa4cWpud246SqXC`.
Data: 2026-09-14 (Europe/Rome). Verbale in sola lettura, unico file scritto da questa verifica.
