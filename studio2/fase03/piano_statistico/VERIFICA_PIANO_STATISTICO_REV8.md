NON OK

# Verifica indipendente della revisione 8 della sotto-fase 03.8 — piano statistico

Data: **2026-09-14** (14:40 CEST). Modello verificatore: **Claude (Cowork), identificativo
configurato `claude-fable-5-1`**, ragionamento esteso, finestra/task distinta da quelle che hanno
prodotto le revisioni 7 e 8 e dal settimo verbale (Codex GPT-5/GPT-6). Sessione Cowork
`session_01UbfhkXNGta2H9XdCvjfBk1`, con il worktree letto sulla macchina dell'autore.

Oggetto: commit candidato **`75bd14898e43f03f849c5d248d6c2481da55e245`** sul branch
`codex/studio2-piano-statistico-fix`, worktree `/Users/luker/fot-tep-piano-statistico-fix`,
costruito sul checkpoint della revisione 7 **`7f760b7146cb858f5ef01ab3a1c61aef3a7577b3`**.

Sola lettura: nessun file del candidato è stato modificato; nessun commit, tag, push, merge o
modifica a `main`; nessun run TEP, training, inferenza o nuova analisi di potenza; nessun risultato
sperimentale sigillato aperto (`fault_runs/runs/`, `soglie_normal/runs/`, evidence, `phase_b/`
per-fault). L'unico file nuovo è questo verbale. `VERIFICA_PIANO_STATISTICO.md` (settimo verbale)
non è stato toccato.

Il report del candidato è stato trattato come oggetto della verifica: ogni affermazione è stata
risalita alla fonte primaria (file nel worktree, oggetti Git, documenti esterni con impronta).

---

## 0. Ambiente verificato e anomalie

| Controllo | Esito |
| --- | --- |
| Branch | ✅ `codex/studio2-piano-statistico-fix` |
| HEAD | ✅ `75bd14898e43f03f849c5d248d6c2481da55e245`, genitore `7f760b7146cb858f5ef01ab3a1c61aef3a7577b3` |
| Stato del worktree | ✅ nessuna modifica tracciata né file non tracciato (`git status --porcelain --untracked-files=all` vuoto); presente solo `__pycache__/` ignorato |
| Identità dei due commit | ✅ entrambi `commit`; autore Luca Sorrentino; 7f760b7 del 2026-09-14 13:12:15 +0200, 75bd148 del 2026-09-14 13:30:45 +0200; messaggi `studio2(piano-statistico): conserva revisione 7 verificata` e `studio2(piano-statistico): recepisce decisioni nella revisione 8` |
| SHA-256 del manifest rev. 8 | ✅ `def46d1982ac393b8c3eab68a78156d86aa2572533e748ccced20e1b1453889f` (13.373 byte), uguale all'atteso |
| `main` | non toccato (`a572d1c`); `merge-base main HEAD` = `d815ce9` |

Due note operative del verificatore, senza effetto sul candidato:

- il worktree è raggiungibile dalla shell locale solo tramite `GIT_DIR`/`GIT_WORK_TREE` espliciti
  (il file `.git` del worktree punta a un percorso assoluto non risolvibile nella shell isolata);
  i comandi Git sono stati tutti di lettura;
- un `git status` iniziale ha lasciato un `index.lock` vuoto (0 byte) in
  `.git/worktrees/fot-tep-piano-statistico-fix/`; è stato rimosso, con autorizzazione dell'autore,
  secondo `Commit_LLM.md` §1 (nessun processo git attivo). I comandi successivi hanno usato
  `GIT_OPTIONAL_LOCKS=0`. Il file `index` del worktree ha subito il solo aggiornamento della stat
  cache; contenuto dell'indice e dei file invariati (verificato con `git diff --stat HEAD`, vuoto).

---

## 1. Provenienza e perimetro

| # | Punto | Esito | Fonte primaria |
| --- | --- | :---: | --- |
| 1.1 | Il checkpoint 7f760b7 contiene esattamente gli otto file indicati nel report §1 | ✅ | `git show --stat 7f760b7`: 8 file, tutti in `studio2/fase03/piano_statistico/`: `DESIGN_RESOLUTION.json`, `DESIGN_RESOLUTION.md`, `PIANO_STATISTICO.md`, `PIANO_STATISTICO_FREEZE.json`, `REPORT_PIANO_STATISTICO.md`, `VERIFICA_PIANO_STATISTICO.md`, `design_resolution.py`, `test_design_resolution.py`; genitore `dd82cd1` come dichiarato (report r. 12–16) |
| 1.2 | Il commit 75bd148 contiene soltanto piano, report, manifest e copia delle decisioni | ✅ | `git diff --name-status 7f760b7..75bd148`: `A DECISIONI_AUTORE_03_8_bozza.md`, `M PIANO_STATISTICO.md`, `M PIANO_STATISTICO_FREEZE.json`, `M REPORT_PIANO_STATISTICO.md`; nessun altro percorso |
| 1.3 | Settimo verbale, codice, test e DESIGN_RESOLUTION immutati fra rev. 7 e rev. 8 | ✅ | SHA-256 identici a 7f760b7, a 75bd148 e nel worktree: verbale `06c2a45b…abbe` (8.471 B); `design_resolution.py` `25a648b9…e613` (31.905 B); `test_design_resolution.py` `569d63e6…f06f` (18.504 B); `DESIGN_RESOLUTION.json` `8bf79dc958e045598cf7538b72752caa902d2f8b134f642e54daaf0274fddbde` (126.303 B); `DESIGN_RESOLUTION.md` `9ed15d15e8a6210e79573c9e4b3d073dfb8d8d9ed680735d83dc7c35358febb7` (27.356 B); `sottofase_3_8.md` `ed6bb712…9afc` (5.942 B). Le impronte dei due DESIGN_RESOLUTION coincidono con quelle della rigenerazione indipendente del settimo verbale (r. 80–83) |
| 1.4 | Discrepanza storica del manifest rev. 7 documentata senza riscrivere la storia | ✅ | manifest rev. 7 (`git show 7f760b7:…FREEZE.json`, impronta `c4ad3ca8…67d8`): voce `VERIFICA_PIANO_STATISTICO.md` = `78dc30e6…97fe`, 11.297 B, ruolo `independent_review_6_NON_OK…`, mentre il file al checkpoint è il settimo verbale `06c2a45b…`. Il manifest rev. 8 lo registra in `revision_history.revision_7.historical_manifest_sha256` e `historical_manifest_review_mismatch` (r. 223–224); il report §1 r. 20–22 lo descrive; il commit 7f760b7 non è stato riscritto |
| 1.5 | Hash e dimensioni di ogni file dichiarato nel manifest | ✅ | 9/9 voci di `files` (r. 232–287) coincidono per SHA-256 e byte con i file del worktree e con i blob a HEAD (verifica automatica, §6) |
| 1.6 | Nessun auto-riferimento circolare nel manifest | ✅ | `PIANO_STATISTICO_FREEZE.json` non compare in `files` né altrove nel proprio testo; la propria impronta non è contenuta nel file |
| 1.7 | Copia delle decisioni byte-identica all'origine | ✅ | `cmp` fra `/Users/luker/fot-tep/studio2/fase03/piano_statistico/DECISIONI_AUTORE_03_8_bozza.md` e la copia nel pacchetto: identici; SHA-256 `66e04dd2…fafb`, 43.136 B per entrambi (manifest r. 19–21, report r. 28–29) |
| 1.8 | `git diff --check` sull'intervallo 7f760b7..75bd148 | ✅ | nessun output, rc 0 |
| 1.9 | Il manifest rev. 8 non conserva il blocco `inputs_read` del manifest rev. 7 (sei impronte: `CATALOG_FREEZE.json`, `PROPOSTA_OOD_D11.md`, registro dei criteri, `DECISIONE_calibrazione_soglie_fase_B.md`, `bootstrap.py`, `metrics.py`) né i blocchi `imposed_by_plan`, `binds_other_subphases`, `does_not_decide`; il report non dichiara la rimozione | ⚠️ | manifest rev. 7 (chiavi lette da Git) contro manifest rev. 8 (`schema_version` 2); report §7 r. 131 descrive il manifest solo come «stato, provenienza, condizioni e catena delle impronte». Il settimo verbale (r. 121–122) contava «14/14 impronte: otto file più sei input». È una perdita di provenienza non dichiarata, non una contraddizione |

---

## 2. Corrispondenza con le decisioni dell'autore

Confronto integrale della tabella (DECISIONI r. 62–76) e degli Allegati A (r. 193–303) e B
(r. 305–453) con `PIANO_STATISTICO.md` e `PIANO_STATISTICO_FREEZE.json`.

| # | Punto | Esito | Fonte primaria |
| --- | --- | :---: | --- |
| 2.1 | D2=8, 64 cluster fault, 8 Normal primari (72 run primari) | ✅ | DECISIONI r. 64, 95, 104–105; piano §0 r. 97, §7.3 r. 512, 534–535, §1 r. 126; manifest `D2_runs_per_fault` r. 25–31 |
| 2.2 | Hoeffding per H1/H2: ipotesi (medie di cluster in [−1,1], indipendenza fra cluster, dipendenza intra-cluster arbitraria), soglie 0,3533018 (48) / 0,3059684 (64), limiti (livello sotto la nulla debole, non potenza né indipendenza effettiva; bootstrap solo intervalli; sign-flip supplementare) | ✅ | DECISIONI r. 68; piano §4.1 r. 229–249, 263–266, §4.3 r. 299; manifest `H1_H2_decision_test` r. 32–40. Soglie ricalcolate: 2·√(ln 20 / 96) = 0,3533018; 2·√(ln 20 / 128) = 0,3059684 |
| 2.3 | Tango per H3, *m*=0,125 come massima perdita media netta, nessuna garanzia individuale | ✅ | DECISIONI r. 65, 195–231, 282–288; piano §4.1 r. 227, §4.3 r. 300, §5 r. 351–363; manifest `noninferiority_H3` r. 41–51 (`individual_guarantee: false`) |
| 2.4 | Gerarchia H1→H2→H3, α unilaterale 0,05 ciascuna | ✅ | DECISIONI r. 67; piano §4.2 r. 276–293; manifest `test_hierarchy_decision_5` r. 52–57 |
| 2.5 | Controllo complessivo dichiarato approssimato per la componente Tango | ✅ | piano §4.2 r. 286–289, §5 r. 372–373; manifest r. 55 `familywise_control` |
| 2.6 | Sensibilità H3 a 0,025 non sostitutiva; A2-bis non adottato | ✅ | DECISIONI r. 289–297; piano §4.1 r. 269–273, §5 r. 370–371, §13 r. 859; manifest r. 46–48 |
| 2.7 | Reporting agente/fault con guadagnati, persi, saldo; saldo ≤−2 su 8 solo descrittivo | ✅ | DECISIONI r. 66, 206–220, 298–303; piano §12 r. 831–833, §13 r. 860; manifest `agent_fault_reporting` r. 58–62 (`confirmatory_gate: false`) |
| 2.8 | D11 {F1,F2} e {F14,F15}, run sigillati 1–3; 8n+84 = 148 a n=8 | ✅ | DECISIONI r. 70; piano §9.1–9.2 r. 653–676; manifest r. 88–101. Aritmetica: 4×3×7 = 84; 64+84 = 148; 48+84 = 132 |
| 2.9 | Bootstrap: seed 20260913, 10.000 repliche, namespace `studio2-fase03-piano-statistico-v1` | ✅ | DECISIONI r. 74; piano §6 r. 396–397, §15 r. 919; manifest r. 145–150. Il piano distingue il seed del bootstrap dal seed dei run (DECISIONI r. 115) e dalle 400×2.000 repliche di DR |
| 2.10 | Undici scorte (8 D1 + Normal + 2 OOD) e politica d'uso (sostituzione solo tecnica, prima delle chiamate, senza aggiungere osservazioni) | ✅ | DECISIONI r. 75, 97; piano §1 r. 126, §7.4 r. 539–547; manifest `spare_runs` r. 151–156 |
| 2.11 | Tetto di pianificazione 3.700 distinto dall'hard stop 200 del pilot | ✅ | DECISIONI r. 76, 102, 112–113; piano §7.2 r. 504–510, §11.1 r. 812–814; manifest `planning_cap` r. 157–161 |
| 2.12 | Politica R (nessun R=3 per sola assenza di controlli; audit 10 %; prima ripetizione nell'analisi primaria; maggioranza in sensibilità; 10 canary/giorno; due giorni marcati o cambio ID sospendono; nessun cambio di R a studio iniziato) | ✅ | DECISIONI r. 71; piano §10.2–10.5 r. 703–752; manifest `R_policy_decision_11` r. 102–112 |
| 2.13 | Soglie GO/NO-GO T3 (≥114/120 e almeno un'astensione parsata per condizione), T4 (0/120), T6, T9, T11, T5 (margine 20 %, tetto 3.700, finestra non estesa automaticamente) | ✅ | DECISIONI r. 72–73; piano §11 r. 763–770; manifest `go_no_go_thresholds` r. 113–120. 0,95×120 = 114 coerente con «≥ 95 %» dell'Allegato B r. 407 |
| 2.14 | Nessuna interpretazione o decisione ulteriore rispetto alle decisioni dell'autore | ✅ con nota | Il diff 7f760b7..75bd148 del piano cambia solo le voci coperte dalla tabella e dagli allegati; tre precisazioni testuali derivano dall'addendum bibliografico e non dalle decisioni: (a) motivazione della non applicabilità di Bahadur–Savage riformulata («ricchezza di ogni media reale» invece di «code non limitate»), §4.1 r. 255–257 e §17 r. 979–982, come chiesto dall'addendum r. 97 e 108; (b) applicabilità del modello IID/multinomiale di Tango dichiarata come limite, §5 r. 372–373 (addendum r. 106); (c) esattezza di Clopper–Pearson non trasferita a risposte correlate, §8.4 r. 624–627 (addendum r. 106). Sono recepimenti fedeli alla fonte bibliografica, ma il report non li elenca (vedi ⚠️ 3.15) |
| 2.15 | Le approvazioni sono attribuite a Luca, 14 settembre 2026, firma materiale pendente, nessuna seconda approvazione richiesta | ✅ | DECISIONI r. 8–10, 185–189; piano r. 31–33, §15 r. 923–925; manifest `author_decision_source` r. 13–23 |

---

## 3. OOD ed evidenza bibliografica

Documenti esterni letti integralmente e improntati:

- addendum `/Users/luker/fot-tep-letteratura-fase03/docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md`:
  SHA-256 `f2c29416664e27c2ecac7d439939f51f1a3f7313e2aba669bb39db7106cf0b8e`, 34.808 B ✅ (manifest r. 167–169, report r. 63);
- verbale `/Users/luker/fot-tep-verifica-letteratura-fase03/docs/lit_review/VERIFICA_INDIPENDENTE_LETTERATURA_FASE03.md`:
  SHA-256 `551f7da9de20096f3a21f6f9a19d2beecd4b03367bbf6cbe4d083f482637ddaf`, 30.107 B ✅, uguale
  all'atteso del mandato (manifest r. 172–175, report r. 64).

| # | Punto | Esito | Fonte primaria |
| --- | --- | :---: | --- |
| 3.1 | IDV(6): FDR DAE/T²/SPE 100/99/100 % | ✅ | addendum r. 7, 51–53; verbale r. 40–42; piano §8.2 r. 582–583; manifest r. 177–181; report r. 66 |
| 3.2 | IDV(4): 100/18/100 % | ✅ | addendum r. 8, 54–56; verbale r. 43–45; piano §8.2 r. 586–587; manifest r. 182–186; report r. 66–67 |
| 3.3 | Condizione numerica F6 soddisfatta soltanto entro il perimetro PHM 2023 | ✅ | addendum r. 7, 11, 82 («PHM da sola soddisfa la verifica di presenza dei numeri»; nessuna soglia universale); piano §8.2 r. 581–582 «entro il perimetro PHM 2023»; manifest r. 79 `satisfied_within_PHM_2023_scope` |
| 3.4 | F6/F4 come scelta confermata condizionatamente | ✅ | DECISIONI r. 69; piano §0 r. 98, §8.2 r. 578, §15 r. 911; manifest r. 86 `confirmed_conditionally` |
| 3.5 | Verifiche tecniche aperte: generabilità, trip, ammissibilità (§8/03.11) | ✅ | piano §8.2 r. 599–604, §16 r. 932–933; manifest r. 80–84, 205; report r. 55–56, 108 |
| 3.6 | Catene F6→F5→F12 e F4→F11→F5 | ✅ | DECISIONI r. 69, 136–146; piano §8.2 r. 591–594; manifest r. 68–77 |
| 3.7 | Obbligo di verifica propria di ogni sostituto | ✅ | piano §8.2 r. 594–595, §7.4 r. 547, §16 r. 933; manifest r. 85 |
| 3.8 | I due OOD restano distinti (F5 non contabile due volte) | ✅ | DECISIONI r. 144–146; piano §8.2 r. 595–597; manifest r. 85 |
| 3.9 | Discrepanza F9–SPE 5,6 % (fonte) contro 6,6 % (registro), senza modifica di registro, H, D1 o criteri | ✅ | addendum r. 33; verbale r. 47; registro `docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md` r. 66–70 (riga F9: DAE 3,5 · T² 5,6 · SPE 6,6); piano §8.2 r. 612–613; manifest r. 187–191 |
| 3.10 | Limiti di accesso a Yin, Maurer, Westfall e Kish | ✅ | addendum r. 9, 70–82, 91–94, 110; verbale r. 24, 105–109; manifest r. 192–197; report r. 68–69; piano §8.2 r. 610, §17 r. 966, 987–988 |
| 3.11 | Otto riferimenti metodologici di §17 distinti da McMahan | ✅ | piano §17 r. 964–988 (Tango, Maurer–Hothorn–Lehmacher, Westfall–Krishen, Clopper–Pearson, Kish, Hoeffding, Bahadur–Savage, ICH E9 = otto; McMahan «non un nono»); DECISIONI r. 173–176; manifest r. 198–199; addendum §7 r. 84–98 (nove opere assegnate = otto + McMahan) |
| 3.12 | Corpus bibliografico ancora esterno al branch, non dichiarato integrato in `main` | ✅ | i 23 file candidati non sono nel diff 7f760b7..75bd148 né nel worktree; piano §8.2 r. 611–612, §14.12 r. 900–902, §16 r. 936–937; manifest r. 200; report r. 74–75 |
| 3.13 | Il verbale bibliografico OK non è presentato come approvazione statistica o tecnica degli OOD | ✅ | verbale r. 190–199, 213 («Non costituisce un verdetto favorevole automatico sulla fase 03.8…»); manifest r. 164–165 `does_not_approve_statistical_or_OOD_decisions: true`; report r. 64 «OK sul candidato bibliografico, non su 03.8 o freeze»; piano §15 r. 911 usa il verbale solo come fonte del numero |
| 3.14 | FDR = *fault detection rate*, non accuratezza diagnostica né false discovery rate | ✅ | addendum r. 64; piano §8.2 r. 583–584; report r. 67 |
| 3.15 | Il report non elenca i tre recepimenti testuali dall'addendum (Bahadur–Savage, Tango IID, Clopper–Pearson) di cui al punto 2.14 | ⚠️ | report §3 r. 59–75 e §7 r. 129 li coprono solo genericamente («evidenza … recepita»). Contenuto verificato conforme all'addendum r. 97, 106, 108; manca la dichiarazione esplicita nel report |

---

## 4. Remediation, sonda e gate (Allegato B)

| # | Punto | Esito | Fonte primaria |
| --- | --- | :---: | --- |
| 4.1 | Ordine: conformità producer → eventuale remediation → sonda budget → gate 40×3; remediation non ammissibile a gate iniziato | ✅ | DECISIONI r. 317–324; piano §11.1 r. 777–780; manifest `mandatory_order` r. 122–127; report r. 79–80 |
| 4.2 | 16 insight in 8 chiamate di conformità, denominatori distinti | ✅ | DECISIONI r. 314, 326–327; piano §11 r. 768; manifest r. 117; report r. 80 |
| 4.3 | Una sola remediation, sul solo prompt del producer, per le sole classi 1–4 (strutturale/identificatori/cap/leakage); schema, validatore, regole di leakage e campi fissi invariati | ✅ | DECISIONI r. 348–358, 402–404; piano §11.1 r. 782–784, 791–792; manifest r. 128 |
| 4.4 | Conservazione ed esclusione dalle librerie degli output iniziali | ✅ | DECISIONI r. 369–372; piano r. 790; manifest r. 129 |
| 4.5 | Ripetizione completa degli stessi otto casi col nuovo template congelato | ✅ | DECISIONI r. 364–366; piano r. 789–790; manifest r. 129 |
| 4.6 | Autorizzazione futura scritta sul diff concreto (artefatto `REMEDIATION_T9_001.md`) | ✅ | DECISIONI r. 360–361, 425–428; piano r. 785–787, §1 r. 130; manifest r. 130 |
| 4.7 | Riserva unica di 15: `8×remediation + trasporto ≤ 15`, quota 8 per remediation, trasporto cumulativo, nessuna ricostituzione | ✅ formula / ⚠️ glossa | formula identica in DECISIONI r. 383, piano r. 797 e manifest r. 131–133. ⚠️ La glossa del piano r. 799 («le altre 7 richieste coprono il trasporto documentato cumulativo») e del report r. 88–89 è più stretta dell'Allegato B r. 379–381, che senza remediation ammette fino a 15 ripetizioni di sola classe 5 nella conformità, al prezzo di rendere la remediation non finanziabile oltre 7 trasporti. La formula prevale ed è coerente; la glossa andrebbe resa esplicita («7» è il residuo compatibile con una remediation ancora possibile, non un tetto assoluto della conformità) |
| 4.8 | Sonda ripetibile soltanto con prova di zero token e per tripletta completa; al massimo due triplette con le 7 residue | ✅ | DECISIONI r. 391–398, 437–440; piano r. 803–805; manifest r. 134 |
| 4.9 | Nessuna ripetizione per trasporto nel gate | ✅ | DECISIONI r. 397–398, 441–442; piano r. 806–807; manifest r. 135 |
| 4.10 | Invalidità conteggiate in T3 | ✅ | DECISIONI r. 442; piano §11 r. 765, §10.3 r. 721–722, r. 806 |
| 4.11 | Divergenza definita esclusivamente dalla coppia parsata (`abstain`, `predicted_label`) o dalla validità; altri delta forensi | ✅ | DECISIONI r. 71, 78–85, 443; piano §10.3 r. 715–718; manifest r. 103 |
| 4.12 | Tre risposte non valide → T6 non valutabile, nessun GO tecnico, nessuna «stabilità» | ✅ | DECISIONI r. 444–447; piano §10.3 r. 720–722, §11 r. 767; manifest r. 116; report r. 101–102 |
| 4.13 | Nessun retry automatico, nessun reset dei contatori, nessun riuso delle 8 del producer alternativo | ✅ | DECISIONI r. 386–390; piano r. 798–801, 813–814; manifest r. 137–139 |
| 4.14 | Timeout senza prova di zero token = guasto tecnico irrisolto, non remediation | ✅ | DECISIONI r. 340–346, 433–436; piano r. 792–793; manifest r. 136; report r. 90–91 |
| 4.15 | Hard stop 200 non trattato come riserva spendibile né come autorizzazione a riavviare il pilot | ✅ | DECISIONI r. 389–390; piano r. 812–814; manifest r. 142; report r. 100; `PREFLIGHT_03_0.md` r. 199–201 (riserva 15, pianificato 160, hard stop 200) |
| 4.16 | Ricalcolo degli intervalli dalla configurazione (`pilot_preflight.json` `call_budget`: sonda max 9, gate 120, conformità Qwen 8, alternativo 8, riserva 15, hard stop 200; `PREFLIGHT_03_0.md` r. 194–201) | ✅ | 8+3+120 = 131 … 8+9+120 = 137; +8 remediation → 139–145; +8 alternativo → 147–153; 137+8+7 = **152** senza alternativo; 152+8 = **160** con alternativo. Coincidono con DECISIONI r. 374–378, piano r. 809–812, manifest r. 140–141, report r. 94–98 |

---

## 5. Residui e stato

| # | Punto | Esito | Fonte primaria |
| --- | --- | :---: | --- |
| 5.1 | Firma materiale dell'autore aperta | ✅ | manifest r. 16, 203; piano §16.1 r. 931; report r. 106 |
| 5.2 | Riverifica indipendente della rev. 8 aperta | ✅ | manifest r. 204, 228, 303; piano §16.5 r. 938–939; report r. 107 |
| 5.3 | Verifiche tecniche F6/F4 e sostituti aperte | ✅ | manifest r. 205; piano §16.2; report r. 108 |
| 5.4 | Gestione organizzativa preventiva del ramo R=3 aperta | ✅ | manifest r. 206–213; piano §16.3, §11.1 r. 816–818; report r. 111–112 |
| 5.5 | Integrazione bibliografica aperta | ✅ (⚠️ collocazione nel manifest) | piano §16.4 r. 936–937; report r. 109; manifest r. 200 (`integration_status`) — non compare però fra le `remaining_conditions` (r. 202–215), pur essendo condizione di §16 |
| 5.6 | Allineamenti esterni aperti e non eseguiti | ✅ | manifest r. 214; piano §7.2 r. 504–506, §16.6; report §6 r. 114–125. Formulazioni correnti verificate sulle fonti: piano generale (`/Users/luker/fot-tep/docs/paper/FoT_TEP_Review_Piano_Sperimentale.md`, checkout corrente; le stesse formulazioni sono su `main` a numerazione diversa: r. 102, 569, 1085, 1168, 1218) r. 94 D2 «aperta, +590, +24 %», r. 1062 «~2.450 a ~3.040, tetto 3.500», r. 1145 T5 e r. 1195 O2 «3.000 o 3.500», r. 547–548 «~2.853/~3.555, 3.000/3.700»; `APERTURA_SOTTOFASI_FASE03.md` r. 60 (sonda → gate → conformità); `PREFLIGHT_03_0.md` r. 177–179 (riserva contabile non autorizzata); `pilot_preflight.json` `call_budget.retry_reserve_authorized=false` e `determinism_policy.divergence_event` (include JSON parsato, finish reason, byte grezzi); `run_pilot.py` r. 510–519 (`divergence_signature` a sei campi) e r. 567–569 (`invalid or truncated → NO_GO_CONFIGURATION`), nessuna semantica «T6 non valutabile» né soglia 114/120. Tutte le righe della tabella del report §6 sono esatte |
| 5.7 | Configurazione ed esito del pilot aperti | ✅ | report r. 110; piano §15 r. 918 («esito del pilot e prerequisiti esterni»); nessun GO acquisito; il freeze 03.8 precede il pilot (DECISIONI r. 180–183) |
| 5.8 | Nucleo D2=8 a R=3 = 5.184 chiamate > 3.700; nessun aumento automatico del tetto, riduzione automatica del disegno o NO-GO scientifico automatico | ✅ | ricalcolo: 72 run × 8 agenti × 3 condizioni = 1.728 a R=1; ×3 = 5.184 (DECISIONI r. 99, 112, 449–453; piano §10.2 r. 708–709, §11.1 r. 816–818; manifest r. 206–213; report r. 111–112). Testo del piano e del manifest contiene le tre negazioni; nessun automatismo introdotto |
| 5.9 | Manifest: `status = decisions_recorded_pending_reverification`; `freeze_effective = false`; `freeze_tag = null`; rev. 7 storicamente OK; rev. 8 pending | ✅ | manifest r. 5, 7–8, 217–230, 301–304 |
| 5.10 | Nessuna dichiarazione di chiusura della sotto-fase, nessun freeze | ✅ | piano r. 3–6, 941–942; report r. 3–8, 168–169; manifest r. 306–308 |

---

## 6. Controlli eseguibili

| Comando | Dove | Esito |
| --- | --- | --- |
| `python -m unittest studio2.fase03.piano_statistico.test_design_resolution` | shell locale del worktree, `/usr/bin/python3` **3.10.12**, numpy 2.2.6 (l'interprete `/Users/luker/fot-tep/../fot-env/bin/python` non è raggiungibile dalla shell isolata) | **25/26**: fallisce `test_guard_blocks_update_modes_and_pathlib` sul solo sub-controllo `path.read_text()` (r. 89–90): in Python 3.10 `pathlib` chiama `io.open` catturato alla definizione della classe, quindi la guardia non intercetta; artefatto dell'interprete, non del candidato |
| stesso comando | copia byte-identica dei nove file (impronte ricontrollate) in ambiente isolato, **Python 3.11.15**, numpy 2.4.4 | **26/26 OK** in 1,5 s. Eseguiti soltanto i calcoli sintetici temporanei della suite (`--quick`, 4–20 repliche, output in directory temporanee); la griglia completa **non** è stata rigenerata; DESIGN_RESOLUTION non modificati (impronte invariate dopo i test) |
| `python3 docs/test_explanation.py` | worktree, Python 3.10 (file identico a HEAD e a `main`) | **35 test, 14 fallimenti, 1 skip**: `test_condition_c_contract_and_caveats` (1), `test_one_flow_and_ordered_step_headings` (1), `test_step27_qwen_frozen_results_and_limitations` (9), `test_step27_qwen_protocol_stable_facts` (3) — identici al report §8 r. 142–146 e al baseline |
| Validazione JSON | `json.load` su `PIANO_STATISTICO_FREEZE.json` (26 chiavi) e `DESIGN_RESOLUTION.json` (13 chiavi; α 0,05, 400 repliche, 2.000 bootstrap, seed 20260913, `quick: false`, 120 righe analitiche, 158 scenari) | ✅ |
| `git diff --check 7f760b7..75bd148` | worktree | ✅ nessun output |
| Verifica automatica hash/dimensioni | 9/9 voci del manifest; SHA-256 ai due commit e nel worktree | ✅ (§1.3, §1.5) |
| Confronto byte per byte delle decisioni | `cmp` origine/copia | ✅ identici |
| Controllo dell'aritmetica | Python | ✅ 131–137, 139–145, 147–153, 152/160; 5.184; 702 (24,6 %); 638; 148/132; 172,8 ≈ 173 prompt di audit; potenza normale 0,9354 (α 0,05) e 0,8854 (α 0,025) a N=64, d=0,10, m=0,125; Tango a zero discordanti 2,619/3,024; controesempio 0,0508/0,0850 e Hoeffding 0/0 |
| Valori del piano contro `DESIGN_RESOLUTION.json` | Python | ✅ H3 m=0,125: normale/Tango 0,86/0,7650 (48, d=0,10), 0,94/0,8600 (64, d=0,10), 0,72/0,6975 (64, d=0,20); m=0,10: 0,8119/0,7250; m=0,15: 0,9842/0,9525; MDE 0,098/0,139; MDE Hoeffding ammissibili 0,334085–0,461955 (48: 0,385768–0,461955; 64: 0,334085–0,400064). Tutti coincidono con piano §4.1, §5, §7.1 e con DECISIONI r. 122–125, 239–244 |
| Contenuto effettivo dei due commit | `git show --stat`, `git diff --name-status` | ✅ (§1.1, §1.2) |

---

## 7. Rilievi sul report del candidato

| # | Punto | Esito | Fonte primaria e formulazione corretta |
| --- | --- | :---: | --- |
| 7.1 | Report §8 r. 148–149: «immutabilità confermata per … `DESIGN_RESOLUTION.json` (`8bf79dc92c2af53fc93a1a36bd109e186950d241775c3aca19986237caec3e7a`), `DESIGN_RESOLUTION.md` (`9ed15d158c060a439b4b912a0f6ecde50295349c6043bd7779bf6f8d92755d90`)» | ❌ | Le due impronte non corrispondono ad alcun file: coincidono con quelle reali solo nei primi otto caratteri esadecimali. I valori corretti, ricalcolati sul worktree e sui blob ai commit 7f760b7 e 75bd148 e uguali a manifest r. 272 e 278, al settimo verbale r. 81 e 83 e a DECISIONI r. 50, sono `8bf79dc958e045598cf7538b72752caa902d2f8b134f642e54daaf0274fddbde` (JSON, 126.303 B) e `9ed15d15e8a6210e79573c9e4b3d073dfb8d8d9ed680735d83dc7c35358febb7` (MD, 27.356 B). L'immutabilità dei file è vera; l'attestazione nel report è falsa nel dato. Le stringhe errate compaiono solo nel report (grep su entrambi i repository) |
| 7.2 | Report §8 r. 147, 150–151: impronte del settimo verbale, di `design_resolution.py` e di `test_design_resolution.py` | ✅ | coincidono con i ricalcoli |
| 7.3 | Report §1 r. 12–16: HEAD iniziale `dd82cd1`, otto file, conservazione byte per byte in 7f760b7 | ✅ | `git log`, `git show --stat`; impronte rev. 7 (piano `3326e992…fba6`, manifest `c4ad3ca8…67d8`, DR JSON `8bf79dc958…`) uguali a DECISIONI r. 49–51 |
| 7.4 | Report §8 r. 139–141: 26/26 e nessuna rigenerazione della griglia | ✅ | riprodotto (§6) |
| 7.5 | Report §8 r. 152–155: aritmetica, `git diff --check`, JSON, impronte del manifest | ✅ | riprodotto (§6) |
| 7.6 | Report §6: tabella degli allineamenti esterni | ✅ | ogni «formulazione/stato corrente» verificata sui file esterni (§5.6) |
| 7.7 | Report §9 r. 162–166 e piano r. 25–45: cronologia delle revisioni | ⚠️ | `git log` del branch mostra i commit fino a `dd82cd1` (rev. 5) e poi 7f760b7/75bd148; le revisioni 6 e 7 non hanno commit propri e sono ricostruibili solo dal checkpoint 7f760b7 e dai verbali. Coerente con «revisione 7 non committata» del settimo verbale; nessuna incoerenza, solo assenza di commit intermedi |
| 7.8 | Piano §4.1 r. 271–272: «il controllo Tango separato disponibile dà 0,8675 e 0,8075» | ⚠️ | i due valori stanno nel report della revisione 7 (§6, r. 169, raggiungibile con `git show 7f760b7:…REPORT_PIANO_STATISTICO.md`) e in DECISIONI r. 257–258; il report rev. 8 non li contiene più e il piano non indica dove siano registrati. Tracciabilità garantita solo dalla storia Git |
| 7.9 | Piano r. 3 «Data: 2026-09-13» con nota di revisione 8 datata 2026-09-14; manifest `date` 2026-09-14 | nota | non è un errore (la data d'intestazione è quella del documento originario); segnalato per evitare letture ambigue |

---

## 8. Ambito di questa verifica e limiti

- Verifica ristretta al delta rev. 7 → rev. 8 e alla coerenza di piano, report, manifest e copia
  delle decisioni con le fonti primarie. Le conclusioni tecnico-scientifiche della revisione 7
  (Hoeffding, Tango, simulazioni, codice) non sono state rifatte: restano coperte dal settimo
  verbale OK, i cui artefatti sono immutati (§1.3).
- Non è stata eseguita alcuna rigenerazione completa di `DESIGN_RESOLUTION.*`; i valori usati dal
  piano sono stati letti dal JSON pubblicato e, dove possibile, ricalcolati in forma chiusa.
- L'interprete `/Users/luker/fot-env/bin/python` richiesto dal mandato non è eseguibile dalla shell
  isolata; il 26/26 è stato ottenuto su copia byte-identica con Python 3.11.15/numpy 2.4.4 (§6).
- Non è stato aperto alcun dato sperimentale; nessuna chiamata a modelli; nessuna analisi di potenza
  nuova.

Letti integralmente: `docs/MAINTENANCE.md`, `docs/prompts/Prompt_LLM.md`, `Verifica_LLM.md`,
`Fase_LLM.md`, `Commit_LLM.md`; `PIANO_STATISTICO.md`, `REPORT_PIANO_STATISTICO.md`,
`PIANO_STATISTICO_FREEZE.json`, `DECISIONI_AUTORE_03_8_bozza.md` (copia e origine),
`VERIFICA_PIANO_STATISTICO.md`, `DESIGN_RESOLUTION.md`, `design_resolution.py`,
`test_design_resolution.py`, `sottofase_3_8.md`; `DESIGN_RESOLUTION.json` letto per struttura e
valori interrogati; i due documenti bibliografici; il diff completo 7f760b7..75bd148 e il manifest
rev. 7 da Git. Consultati nei punti richiamati: piano generale (branch corrente e `main`), registro
dei criteri §3, `APERTURA_SOTTOFASI_FASE03.md` r. 60, `PREFLIGHT_03_0.md` r. 170–201,
`pilot_preflight.json`, `run_pilot.py` r. 510–585.

---

## Conclusione

**NON OK.** Il recepimento delle decisioni dell'autore e dell'evidenza bibliografica in piano e
manifest è fedele alle fonti in tutti i punti verificati (§2–§5), le impronte di manifest e
artefatti sono corrette, i controlli eseguibili sono riprodotti e nessun automatismo, decisione
ulteriore o chiusura della sotto-fase è stato introdotto. Il verdetto negativo dipende dal punto
❌ 7.1: `REPORT_PIANO_STATISTICO.md` attesta l'immutabilità di `DESIGN_RESOLUTION.json` e
`DESIGN_RESOLUTION.md` con due impronte SHA-256 inesistenti. In un pacchetto la cui provenienza si
regge sulle impronte (MAINTENANCE §2, §8.5), un report committato con attestazioni di impronta false
non può essere accettato così com'è.

Correzioni necessarie prima di una nuova riverifica:

1. **Obbligatoria.** Correggere in `REPORT_PIANO_STATISTICO.md` §8 r. 148–149 le impronte di
   `DESIGN_RESOLUTION.json` → `8bf79dc958e045598cf7538b72752caa902d2f8b134f642e54daaf0274fddbde`
   (126.303 B) e `DESIGN_RESOLUTION.md` → `9ed15d15e8a6210e79573c9e4b3d073dfb8d8d9ed680735d83dc7c35358febb7`
   (27.356 B), spiegando l'errore senza riscrivere il commit 75bd148 (nuova revisione tracciata,
   MAINTENANCE §8.4); aggiornare di conseguenza l'impronta del report nel manifest (r. 240–244) e
   la nota di revisione.
2. **Raccomandata, nella stessa revisione.** Dichiarare nel report la rimozione dal manifest del
   blocco `inputs_read` (sei impronte) e dei blocchi `imposed_by_plan`, `binds_other_subphases`,
   `does_not_decide` della rev. 7, oppure ripristinarli (⚠️ 1.9); elencare i tre recepimenti
   testuali derivati dall'addendum (⚠️ 2.14/3.15); precisare la glossa sui «7» di trasporto in piano
   r. 799 e report r. 88–89 in coerenza con l'Allegato B r. 379–381 (⚠️ 4.7); indicare in piano
   §4.1 dove sono registrati i valori 0,8675/0,8075 (⚠️ 7.8); valutare l'inserimento
   dell'integrazione bibliografica fra le `remaining_conditions` del manifest (⚠️ 5.5).

Nessuna di queste correzioni tocca le decisioni registrate, i valori numerici del piano, il codice,
i test o gli artefatti DESIGN_RESOLUTION. Anche dopo la correzione, la sotto-fase 03.8 resta aperta
finché non sono soddisfatte tutte le condizioni residue di piano §16 (firma materiale, verifiche
tecniche F6/F4 e sostituti, ramo R=3, integrazione bibliografica, riverifica indipendente della
revisione corretta, allineamenti esterni, commit raggiungibile da `origin/main`); `freeze_tag`
resta nullo e nessun freeze è stato creato da questa verifica.

Percorso di questo verbale:
`studio2/fase03/piano_statistico/VERIFICA_PIANO_STATISTICO_REV8.md`.
