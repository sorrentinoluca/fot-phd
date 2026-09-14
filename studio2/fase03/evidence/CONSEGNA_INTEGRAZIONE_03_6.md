# Consegna del candidato locale d'integrazione — sotto-fase 03.6

**Data:** 2026-09-14, Europe/Rome  
**Sotto-fase:** studio 2 FoT-TEP, Fase 03, sotto-fase **03.6 — evidence 697-D e verbalizzazioni**  
**Esito:** **candidato locale d'integrazione pronto e controllato**. La sotto-fase scientifica era
già completata e verificata; questa attività non costituisce una nuova verifica scientifica.

## 1. Riferimenti Git e ambiente di lavoro

- Worktree assoluto: `/Users/luker/fot-tep-integrazione-evidence-036`.
- Branch: `codex/studio2-evidence-integrazione`.
- Commit del candidato locale: `7c99a8318cbe24bf864790566302f72614d963ed`.
- Messaggio: `studio2(fase03): integra le evidence 697-D verificate`.
- Genitori del merge:
  - base main: `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`;
  - candidato evidence: `c66bd8dddf8e2af9dd0665ee30afd36c248b93fb`.
- `origin/main` e `refs/heads/main` remoto sono stati verificati a
  `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1` prima del merge e ricontrollati dopo la
  preparazione.
- Il worktree `/Users/luker/fot-tep` non è stato usato come main aggiornato e non è stato
  modificato.

Il commit `7c99a83` è un merge reale: conserva come secondo genitore `c66bd8d` e rende
raggiungibile l'intera catena evidence
`cf1f70f → daf5dc5 → d54fa4a → 2f6dd8d → 54bbd0c → bb6d9e7 → c66bd8d`.

## 2. Attività svolte

1. Letti l'handoff operativo revisione 02, `docs/MAINTENANCE.md` e i prompt correnti di fase,
   verifica, documentazione e commit da `origin/main`.
2. Verificati branch, HEAD, remoti, worktree concorrenti e pulizia del candidato sorgente.
3. Letti report, verbale, dipendenze, storage, controllo packaging e sorgenti 03.6; letti sul
   main corrente la consegna 03.9 e i pin dei due sorgenti 03.6 da essa riusati.
4. Creato un worktree dedicato dalla base `c486eee` e fuso il candidato `c66bd8d` preservandone
   la storia.
5. Risolti i soli conflitti nei tre file condivisi, partendo dal target effettivo:
   - evidence in `studio2/PROVENIENZA.md` come primo numero libero, **§12**;
   - evidence nel walkthrough Markdown e HTML come **§4.6**;
   - preservate le sezioni già integrate §4.5, §4.7, §4.9 e PROVENIENZA §§9–11.
6. Verificata l'identità byte-per-byte dell'intera cartella evidence rispetto a `c66bd8d` e
   l'assenza di modifiche a `code/`, `phase_b/` e `studio2/fase03/baseline_numerica/`.

Non sono stati rigenerati dati o evidence, riscaricati asset, ripetuti batch, effettuate
simulazioni o inferenze, né riaperte le decisioni 03.5, FAR o A/B.

## 3. File nel commit locale

### File condivisi modificati nel raccordo

- `/Users/luker/fot-tep-integrazione-evidence-036/docs/fot_walkthrough_conversazione_studio2.md`
- `/Users/luker/fot-tep-integrazione-evidence-036/docs/fot_walkthrough_conversazione_studio2.html`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/PROVENIENZA.md`

### File evidence aggiunti, byte-identici al candidato `c66bd8d`

- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/.gitignore`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/ARTIFACT_STORAGE.json`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/DIPENDENZE_EVIDENCE.md`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/MANIFEST_CONSERVAZIONE.csv`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/OUTPUT_CHECK.json`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/PACKAGING_V2_CHECK.json`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/REPORT_EVIDENCE.md`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/VERIFICA_EVIDENCE.md`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/__init__.py`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/extract_evidence.py`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/leakage.py`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/test_evidence.py`
- `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/verify_output.py`

## 4. Report, verbali e record pertinenti

- Report scientifico storico, preservato byte-identico:
  `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/REPORT_EVIDENCE.md`,
  SHA-256 `24d861ab0506161786b4e8456e084fb8c12dd447dfc8ca74c337b9b81db52822`.
- Verbale indipendente **OK**, preservato byte-identico:
  `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/VERIFICA_EVIDENCE.md`,
  SHA-256 `a59399c7f1173d8ec59872f633b7b1cf2156d09dc0de8be37596aff080cc6820`.
- Dipendenze:
  `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/DIPENDENZE_EVIDENCE.md`.
- Storage e packaging:
  `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/ARTIFACT_STORAGE.json`
  e
  `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/evidence/PACKAGING_V2_CHECK.json`.
- Consegna 03.9 consultata come dipendenza:
  `/Users/luker/fot-tep-integrazione-evidence-036/studio2/fase03/baseline_numerica/CONSEGNA_INTEGRAZIONE_03_9.md`.

Il report scientifico conserva correttamente il proprio stato storico «in attesa di verifica»;
non è stato riscritto dopo l'OK. Il presente file è quindi la consegna operativa separata.

## 5. Controlli eseguiti ed esiti

### Identità e riferimenti

- `git diff c66bd8d..7c99a83 -- studio2/fase03/evidence`: nessuna differenza.
- `c66bd8d` e tutti i sette commit della catena evidence risultano antenati di `7c99a83`.
- I file del verbale e del packaging sono leggibili direttamente dal tree del commit finale.
- Nessun conflitto residuo nei tre file condivisi.

### Impronte

- `extract_evidence.py`:
  `46b451c2d6d8b1627993828ac9bac39532562f2fa1b27955b8a20f098ba24e97`.
- `leakage.py`:
  `c77ae5b11186c5b0df87b2f1df8800cb45fb25317e248fe8484d3e8283073887`.
- Entrambe coincidono con i pin presenti in `extract_normal_evidence.py`, nei freeze rev. 2/3
  della 03.9 e nel relativo verbale.
- Le quattro impronte frozen di `tep_features.py`, `tep_verbalize_v2.py`,
  `verbalizer_config_v2.json` ed `evaluate_verbalizer_v2.py` coincidono con
  `phase_b/PHASE_B_PROTOCOL_HASHES.json`.
- Guardia R2:
  `7df0cef2d7854c689b79eb911fa01d1ede1625e22f0d3636c0ea5d678c9f33f8`.

### Test

- `/opt/anaconda3/bin/python3 -m unittest -v studio2.fase03.evidence.test_evidence`:
  **4/4 PASS**.
- Test pertinenti 03.9 (`test_baseline`, `test_extract_normal_evidence`,
  `test_normal_dev_plan`): **10/10 PASS**.
- Il primo tentativo dei test evidence col Python di sistema non disponeva di NumPy; la suite è
  stata ripetuta col runtime dichiarato `/opt/anaconda3/bin/python3` e ha dato 4/4 PASS. È un
  limite dell'ambiente predefinito, non un errore del candidato.

### Manifest, link e documentazione

- `MANIFEST_CONSERVAZIONE.csv`: **1.283** percorsi unici, **61.208.618 byte**.
- `OUTPUT_CHECK.json`: 320 unità, firma 697-D, leakage PASS.
- Storage e packaging v2 coerenti: archivio **62.185.472 byte**, SHA-256
  `6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf`,
  1.283/1.283 file verificati nel record preesistente.
- Link relativi, percorsi e anchor MD/HTML: **PASS**; ID HTML univoci; sezione evidence con
  9 intestazioni e 13 link corrispondenti nei due formati.
- `docs/test_explanation.py` prima e dopo: **35 test, 14 failure, 1 skip**, invariato anche per
  identificativi e subtest. Restano gli stessi failure in:
  `test_condition_c_contract_and_caveats`, `test_one_flow_and_ordered_step_headings`,
  `test_step27_qwen_frozen_results_and_limitations` e
  `test_step27_qwen_protocol_stable_facts`; stesso skip `TutorialChecks.setUpClass`.

### Limiti

- Il controllo d'integrazione non ripete la verifica scientifica indipendente.
- Gli asset evidence-v2 non sono stati riscaricati di nuovo: si è verificata la coerenza dei
  record già prodotti e verificati.
- Il verbale documenta differenze floating-point circa `10^-13` nei file numerici grezzi fra
  versioni NumPy diverse; testo e firme restano byte-identici. Una futura rigenerazione
  bit-per-bit richiederebbe l'ambiente esatto o una politica esplicita di tolleranza.
- `git diff --check` segnala due blank line finali già presenti nel candidato, in `__init__.py`
  e `leakage.py`; sono state preservate per mantenere i byte verificati.

## 6. Stato Git finale dopo la creazione di questa consegna

- Branch: `codex/studio2-evidence-integrazione`, avanti di **8 commit** rispetto a
  `origin/main`.
- HEAD: `7c99a8318cbe24bf864790566302f72614d963ed`.
- File committati: i 16 file elencati in §3, inclusi nel merge commit `7c99a83`.
- File tracciati modificati ma non committati: **nessuno**.
- File non tracciati: **solo questo report**,
  `studio2/fase03/evidence/CONSEGNA_INTEGRAZIONE_03_6.md`.
- Il presente report non è incluso in `7c99a83`, conformemente alla richiesta di non effettuare
  commit per la sola redazione della consegna.

## 7. Stato effettivo

| Ambito | Stato |
| --- | --- |
| Completamento scientifico 03.6 | completato; verifica indipendente **OK** sul pacchetto dichiarato |
| Candidato d'integrazione | preparato e committato localmente in `7c99a83` |
| Integrazione in `main` | **non eseguita**; `origin/main` resta `c486eee` |
| Pubblicazione codice/documentazione | **non eseguita**; nessun push del candidato locale |
| Pubblicazione dati evidence | già completata prima di questo incarico: release v1 preservata e v2 preferita, pubblica e verificata per riscaricamento |
| Congelamento Git 03.6 | nessun nuovo tag creato o pubblicato da questo incarico; non viene dichiarato un freeze ulteriore |
| Macro-Fase 03 | aperta |

## 8. Residui, dipendenze e prossimo passo

1. Integrare serialmente `7c99a83` da un worktree pulito designato, dopo un nuovo
   `git fetch origin main` e soltanto se non esiste un writer concorrente sui file condivisi.
2. Se `origin/main` è ancora `c486eee`, l'integrazione può essere un fast-forward locale al
   commit `7c99a83`; push e qualunque tag richiedono un'autorizzazione separata.
3. Se `origin/main` è avanzato, creare un nuovo branch dalla nuova punta, fondere `7c99a83`,
   ricalcolare il primo numero libero di PROVENIENZA e la collocazione del walkthrough e
   ripetere i controlli di §5. Non sovrascrivere le sezioni integrate nel frattempo.
4. Dopo l'effettiva pubblicazione, aggiornare con un record di stato successivo la
   raggiungibilità dei sorgenti 03.6 richiesta dalla 03.9; non riscrivere report, verbale o
   manifest storici.
5. La chiusura effettiva 03.9 richiede ancora il raccordo delle metriche nella 03.10 e il
   successivo tag della baseline secondo le verifiche previste. L'integrazione 03.6 risolve solo
   la dipendenza di raggiungibilità dei sorgenti.

Decisione dell'autore già acquisita e da non riaprire: **U3**, estensione circoscritta di U1/R2
alla normalizzazione e ai flag del verbalizzatore V2. Se R2 decade o si passa a
`baseline_fit_new`, le evidence dipendenti sono invalide e vanno rigenerate. Non risultano nuove
decisioni autoriali necessarie per il solo fast-forward del candidato finché la base resta
invariata.

**Prossimo passo consigliato:** la finestra orchestratrice verifica nuovamente `origin/main` e,
se ancora a `c486eee`, dispone l'integrazione seriale locale di `7c99a83`; solo dopo decide
se autorizzare pubblicazione e relativo record di stato.
