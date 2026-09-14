# Consegna del candidato locale raccordato — 03.6 → 03.12 R4 → letteratura

**Data:** 2026-09-14, Europe/Rome
**Perimetro:** studio 2 FoT-TEP, Fase 03 ancora aperta
**Esito:** candidato locale unico, committato e reviewabile; nessun push, tag o modifica a `main`.

Questo record documenta il raccordo Git e documentale effettuato. Non sostituisce le verifiche
scientifiche indipendenti dei tre pacchetti, non qualifica il servizio 122B e non chiude 03.8,
03.9 o la Fase 03.

## 1. Base, worktree e branch

- Repository: `https://github.com/sorrentinoluca/fot-phd.git`.
- Base remota effettiva, verificata prima di creare il worktree e ricontrollata prima di questo
  record: `origin/main` a `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`.
- Worktree dedicato: `/Users/luker/fot-tep-raccordo-036-0312-letteratura`.
- Branch: `codex/studio2-raccordo-036-0312-letteratura`.
- La copia principale `/Users/luker/fot-tep` è rimasta sul proprio branch, con le modifiche
  preesistenti intatte; nessun checkout è stato eseguito lì.
- I worktree sorgente 03.6, 03.12, letteratura e quello 03.15 non sono stati modificati.
- Nessun worktree, lock, file ignorato o non tracciato è stato rimosso.

## 2. Sequenza locale e riferimenti raggiungibili

Ordine applicato:

1. `7c99a8318cbe24bf864790566302f72614d963ed` — fast-forward al merge candidato 03.6;
   conserva come secondo genitore `c66bd8dddf8e2af9dd0665ee30afd36c248b93fb` e l'intera
   catena evidence.
2. `5806871a1e73b49e53a1869e7b9142b6fe4abfa8` — merge locale di
   `c9f83c6447a9963cd69531b14439a3ac5a5a72b2` sul risultato 03.6.
3. `903f37f74816ee893835fbb818cc53c0a0783810` — merge locale della storia bibliografica
   terminante in `40911d0e3e7b75960e6973f3fd8f609e65ab6e05`.
4. `601fb70c560b95e35a942a60b706785d28780ee7` — acquisizione byte-identica delle tre
   consegne operative storiche.
5. Il commit che contiene questo record — consegna corrente e stato effettivo del raccordo.

Sono antenati del candidato finale:

- 03.6: `7c99a83…`, `c66bd8d…` e i commit della catena
  `cf1f70f → daf5dc5 → d54fa4a → 2f6dd8d → 54bbd0c → bb6d9e7 → c66bd8d`;
- 03.12: target R4 `3c64390bc4dd58c48cc4e1e388a38989b32b3143`, evidenze
  `43b31afc1ff271594cb4bd21a39fa4469a8c83bc`, merge preparatorio `c0f4da0…`,
  acquisizione NON OK storico `9b1fac9…` e candidato `c9f83c6…`;
- letteratura: candidato `e37c3db66689325b703bb99f3750ca3b5b287aab` e verbale
  `40911d0e3e7b75960e6973f3fd8f609e65ab6e05`, rimasti due commit distinti.

## 3. Raccordi e conflitti

### 3.1 Evidence 03.6

Il fast-forward non ha introdotto nuovi conflitti. Sono state preservate la risoluzione già
presente nel candidato, la sezione walkthrough §4.6, le sezioni concorrenti già integrate e
`studio2/PROVENIENZA.md` §12. L'intera cartella scientifica evidence resta identica a `c66bd8d`;
l'unico file aggiunto successivamente è la consegna operativa storica.

### 3.2 Schema insight 03.12 R4

I tre conflitti effettivi sono stati risolti in:

- `studio2/PROVENIENZA.md`;
- `docs/fot_walkthrough_conversazione_studio2.md`;
- `docs/fot_walkthrough_conversazione_studio2.html`.

Il primo numero libero reale di PROVENIENZA dopo l'evidence era §13: §12 resta assegnato a 03.6
e 03.12 è stata rinumerata §13. Nei walkthrough sono stati conservati sia evidence §4.6 sia
schema R4 §4.12, inclusi indice, stato e rinvii correnti. La sezione scientifico-tecnica §4.12
è byte-identica al candidato 03.12; soltanto i raccordi condivisi sono stati composti.

La cartella `studio2/fase03/schema_insight/` è identica a `c9f83c6` salvo l'aggiunta successiva
della consegna storica. Contratto R4, manifest rev. 5, decisione, report storico, log e verbali
non sono stati modificati. L'adapter 03.10 non presenta delta rispetto alla base.

### 3.3 Letteratura

Il merge a tre vie non ha prodotto conflitti. Git ha applicato i soli hunk del candidato ai
quattro documenti condivisi, che sulla base effettiva coincidevano ancora con la base
bibliografica:

- `docs/letteratura.md`;
- `docs/letteratura.html`;
- `docs/paper/FoT_TEP_paper_blueprint.html`;
- `papers/README.md`.

I quattro risultati coincidono con il candidato verificato, ma sono stati ottenuti applicando il
delta al contenuto corrente, non sostituendo interi documenti. Gli altri 19 file del candidato
sono stati importati invariati; anche il verbale separato è invariato. I due PNG sono presenti
come file Git `100644` con le impronte dichiarate.

La discrepanza PHM F9–SPE resta nell'addendum: 5,6% nella tabella della fonte contro 6,6% nel
registro storico. Il registro congelato e la cartella `studio2/fase03/selection/` non sono stati
modificati.

## 4. Consegne storiche acquisite

Le tre consegne prima non tracciate sono state aggiunte byte-identiche in un commit distinto:

| File | SHA-256 |
| --- | --- |
| `studio2/fase03/evidence/CONSEGNA_INTEGRAZIONE_03_6.md` | `b57c41da7e5eff6d48ebb05b1f2c001e3c680a3f54d1880316a0aaa349a3162c` |
| `studio2/fase03/schema_insight/CONSEGNA_LOCALE_SCHEMA_INSIGHT_R4.md` | `9876d5ae8ac38f8c3cb1970a90f356f113a962b98595fe96156e6ffe75023f49` |
| `docs/lit_review/CONSEGNA_ACQUISIZIONE_LETTERATURA_FASE03_2026-09-14.md` | `7aba211c4b7eaf48bc6997eba5f1514abc43500d5835b135b26ffb4d41670b5e` |

I loro stati storici non sono stati riscritti per dichiarare integrazioni o pubblicazioni
successive. Il presente file registra separatamente ciò che questo raccordo ha completato.

## 5. Controlli ed esiti

### 5.1 Git, identità e pin

- Tutti i candidati e le evidenze elencati in §2 risultano antenati del candidato finale.
- 03.6: cartella scientifica identica a `c66bd8d`; `extract_evidence.py` SHA-256
  `46b451c2d6d8b1627993828ac9bac39532562f2fa1b27955b8a20f098ba24e97` e
  `leakage.py` SHA-256
  `c77ae5b11186c5b0df87b2f1df8800cb45fb25317e248fe8484d3e8283073887` coincidono con
  `extract_normal_evidence.py`, i freeze 03.9 rev. 2/rev. 3 e il verbale 03.9.
- 03.12: 18/18 voci del manifest rev. 5 verificate per byte e SHA-256 sui riferimenti storici
  corretti: 10 al target R4, 6 a `d815ce96…`, 2 a `a572d1c…`; queste ultime coincidono anche
  col commit congelato 03.7 `c16b533…`.
- Letteratura: 19/19 nuovi file del candidato identici a `e37c3db`; quattro documenti condivisi
  raccordati e, dato il mancato delta concorrente su quei file, finali byte-identici al candidato;
  verbale 30.107 byte, SHA-256
  `551f7da9de20096f3a21f6f9a19d2beecd4b03367bbf6cbe4d083f482637ddaf`.

### 5.2 Test

- Evidence: 4/4 PASS con `/opt/anaconda3/bin/python3`.
- Regressioni pertinenti 03.9: 10/10 PASS.
- Schema insight: 25 PASS, 0 FAIL/ERROR, 1 SKIP su 26 nel runtime locale disponibile; lo skip
  è soltanto il tokenizer Qwen pinnato assente. La prova server preesistente resta distinta:
  26/26 PASS senza skip secondo la trascrizione conservata, non rieseguita qui.
- Regressioni `studio2/fase03/tests`: 16/16 PASS con discovery esplicita. Una prima invocazione
  sul solo package aveva scoperto 0 test e non è stata usata come esito.
- Guardiano documentale sulla base, dopo 03.6, dopo 03.12 e dopo letteratura: ogni volta
  35 test, gli stessi 14 fallimenti storici e 1 skip. Identificativi e subtest coincidono; nessuna
  regressione del candidato.

### 5.3 Documentazione

- Sezioni evidence e schema nei walkthrough identiche ai candidati; ordine corrente
  §4.5 → §4.6 → §4.7 → §4.9 → §4.12.
- PROVENIENZA termina con §§11, 12 e 13 senza duplicazioni.
- 224 link locali nei tre HTML toccati controllati, zero percorsi o anchor mancanti; ID HTML
  univoci.
- Letteratura: 128 voci, 13 categorie, 182 righe tabellari equivalenti MD/HTML e 40 schede nello
  stesso ordine, secondo i controlli acquisiti e ancora applicabili perché i 23 file del candidato
  sono invariati.

`git diff --check` segnala whitespace già presente e intenzionalmente conservato nei log raw,
nelle conversioni raw, nel PDF interpretato come testo, nei due sorgenti evidence e in alcune
consegne storiche. Non è stato normalizzato perché avrebbe alterato le impronte verificate.

## 6. Limiti e delta da verificare indipendentemente

- Questo controllo prova storia, identità, riferimenti e coerenza documentale del raccordo; non
  ripete né estende le verifiche scientifiche indipendenti.
- Non sono stati rigenerati release, dati o evidence; non sono state ripetute simulazioni,
  inferenze o prove server.
- Nessun delta scientifico è stato introdotto nei pacchetti verificati. Il solo delta nuovo che
  richiede review del candidato di coordinamento è documentale: composizione dei tre conflitti
  03.12, numerazione PROVENIENZA §13 e questo record.
- Il test locale 03.12 con tokenizer assente non sostituisce la prova server già documentata.
- Le limitazioni bibliografiche su Yin, Maurer, Westfall e Kish restano quelle del verbale;
  l'OK bibliografico non decide OOD, fattibilità, generabilità o piano statistico.

## 7. Stato effettivo e passaggi residui

Stato effettivo: candidato unico completato sul branch dedicato; `origin/main` non modificato,
nessun push e nessun tag creato. 03.9, 03.8 e la Fase 03 restano aperte; il delta metriche ancora
in review non è stato integrato. 03.5, FAR, U3 e A/B non sono stati riaperti. Il servizio 122B
non è stato qualificato.

Per la futura pubblicazione, senza eseguirla in questo incarico:

1. ricontrollare `origin/main`; se è ancora `c486eee…`, integrare serialmente questo candidato
   nel solo `main` designato e pubblicare soltanto con autorizzazione esplicita;
2. verificare sul remoto la raggiungibilità dei candidati 03.6, 03.12, letteratura e delle prove;
3. soltanto dopo la pubblicazione, creare l'eventuale record di pubblicazione 03.12;
4. il futuro tag `studio2-fase03-schema-insight-frozen-001` deve puntare esclusivamente a
   `3c64390bc4dd58c48cc4e1e388a38989b32b3143`, mai al merge, a HEAD o a `43b31af…`; crearlo e
   pubblicarlo richiede un'autorizzazione separata;
5. aggiornare l'adapter 03.10 e i suoi pin soltanto in un'attività separata; completare poi i
   residui propri di 03.8 e 03.9 secondo le verifiche previste.

Se il remoto avanza dopo questo record, il candidato va dichiarato basato su `c486eee…` e
raccordato nuovamente: non va presentato come automaticamente aggiornato.

## 8. Aggiornamento di completezza per la finestra orchestratrice

### 8.1 Identificazione e riferimento corrente

- **ID operativo:** `FASE03-RACCORDO-03.6-03.12-LETTERATURA`; raccordo delle sottofasi
  scientifiche 03.6 e 03.12 con il supporto bibliografico non numerato della Fase 03.
- **Data:** 2026-09-14, Europe/Rome.
- **Attività ed esito:** integrazione locale seriale 03.6 → 03.12 R4 → letteratura,
  acquisizione delle consegne storiche e controllo di coerenza; **COMPLETATO LOCALMENTE**.
- **Worktree assoluto:** `/Users/luker/fot-tep-raccordo-036-0312-letteratura`.
- **Branch:** `codex/studio2-raccordo-036-0312-letteratura`.
- **Commit di riferimento:** `e82b5a08bf642ad45f77e71832958207beb1181c`.
- **Report corrente:** `/Users/luker/fot-tep-raccordo-036-0312-letteratura/studio2/fase03/CONSEGNA_RACCORDO_03_6_03_12_LETTERATURA_2026-09-14.md`.

### 8.2 Report, verbali e record pertinenti

- 03.6: `studio2/fase03/evidence/REPORT_EVIDENCE.md`,
  `studio2/fase03/evidence/VERIFICA_EVIDENCE.md`,
  `studio2/fase03/evidence/CONSEGNA_INTEGRAZIONE_03_6.md`.
- 03.12: `studio2/fase03/schema_insight/REPORT_SCHEMA_INSIGHT.md`,
  `studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004.md`,
  `studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004_NON_OK_STORICO.md`,
  `studio2/fase03/schema_insight/PREPARAZIONE_INTEGRAZIONE_SCHEMA_INSIGHT_R4.md`,
  `studio2/fase03/schema_insight/CONSEGNA_LOCALE_SCHEMA_INSIGHT_R4.md`.
- Letteratura: `docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md`,
  `docs/lit_review/VERIFICA_INDIPENDENTE_LETTERATURA_FASE03.md`,
  `docs/lit_review/CONSEGNA_ACQUISIZIONE_LETTERATURA_FASE03_2026-09-14.md`.
- Raccordo: questo report; non esiste un nuovo verbale scientifico perché il lavoro corrente è
  integrazione Git/documentale e non una nuova verifica scientifica.

### 8.3 Inventario completo rispetto alla base remota

I 64 percorsi creati o modificati fra la base `c486eee…` e il commit di riferimento
`e82b5a0…` sono:

- `M` `docs/fot_walkthrough_conversazione_studio2.html`
- `M` `docs/fot_walkthrough_conversazione_studio2.md`
- `M` `docs/letteratura.html`
- `M` `docs/letteratura.md`
- `A` `docs/lit_review/CONSEGNA_ACQUISIZIONE_LETTERATURA_FASE03_2026-09-14.md`
- `A` `docs/lit_review/VERIFICA_CORPUS_FASE03.json`
- `A` `docs/lit_review/VERIFICA_FONTI_FASE03.json`
- `A` `docs/lit_review/VERIFICA_INDIPENDENTE_LETTERATURA_FASE03.md`
- `A` `docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md`
- `M` `docs/paper/FoT_TEP_paper_blueprint.html`
- `A` `papers/Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.md`
- `A` `papers/Communication-Efficient_Learning_of_Deep_Networks_from_Decentralized_Data.pdf`
- `A` `papers/Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.md`
- `A` `papers/Equivalence_test_and_confidence_interval_for_the_difference_in_proportions_for_the_paired-sample_design.pdf`
- `A` `papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.md`
- `A` `papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder.pdf`
- `A` `papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/page-6.png`
- `A` `papers/Fault_Detection_and_Diagnosis_in_Tennessee_Eastman_Process_with_Deep_Autoencoder_images/page-7.png`
- `A` `papers/Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.md`
- `A` `papers/Probability_Inequalities_for_Sums_of_Bounded_Random_Variables_1963.pdf`
- `M` `papers/README.md`
- `A` `papers/Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.md`
- `A` `papers/Statistical_Principles_for_Clinical_Trials_ICH_E9_1998.pdf`
- `A` `papers/The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.md`
- `A` `papers/The_Nonexistence_of_Certain_Statistical_Procedures_in_Nonparametric_Problems.pdf`
- `A` `papers/The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.md`
- `A` `papers/The_use_of_confidence_or_fiducial_limits_illustrated_in_the_case_of_the_binomial.pdf`
- `M` `studio2/PROVENIENZA.md`
- `A` `studio2/fase03/CONSEGNA_RACCORDO_03_6_03_12_LETTERATURA_2026-09-14.md`
- `A` `studio2/fase03/evidence/.gitignore`
- `A` `studio2/fase03/evidence/ARTIFACT_STORAGE.json`
- `A` `studio2/fase03/evidence/CONSEGNA_INTEGRAZIONE_03_6.md`
- `A` `studio2/fase03/evidence/DIPENDENZE_EVIDENCE.md`
- `A` `studio2/fase03/evidence/MANIFEST_CONSERVAZIONE.csv`
- `A` `studio2/fase03/evidence/OUTPUT_CHECK.json`
- `A` `studio2/fase03/evidence/PACKAGING_V2_CHECK.json`
- `A` `studio2/fase03/evidence/REPORT_EVIDENCE.md`
- `A` `studio2/fase03/evidence/VERIFICA_EVIDENCE.md`
- `A` `studio2/fase03/evidence/__init__.py`
- `A` `studio2/fase03/evidence/extract_evidence.py`
- `A` `studio2/fase03/evidence/leakage.py`
- `A` `studio2/fase03/evidence/test_evidence.py`
- `A` `studio2/fase03/evidence/verify_output.py`
- `A` `studio2/fase03/schema_insight/CONSEGNA_LOCALE_SCHEMA_INSIGHT_R4.md`
- `A` `studio2/fase03/schema_insight/DECISIONE_SCHEMA_INSIGHT.md`
- `A` `studio2/fase03/schema_insight/PREPARAZIONE_INTEGRAZIONE_SCHEMA_INSIGHT_R4.md`
- `A` `studio2/fase03/schema_insight/PROPOSTA_TAG_SCHEMA_INSIGHT.md`
- `A` `studio2/fase03/schema_insight/REPORT_SCHEMA_INSIGHT.md`
- `A` `studio2/fase03/schema_insight/SCHEMA_FREEZE.json`
- `A` `studio2/fase03/schema_insight/TEST_RESULTS.txt`
- `A` `studio2/fase03/schema_insight/TEST_RESULTS_qwen.txt`
- `A` `studio2/fase03/schema_insight/TEST_RESULTS_qwen_rev003.txt`
- `A` `studio2/fase03/schema_insight/TEST_RESULTS_qwen_rev004.txt`
- `A` `studio2/fase03/schema_insight/TEST_RESULTS_rev004.txt`
- `A` `studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT.md`
- `A` `studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev003.md`
- `A` `studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004.md`
- `A` `studio2/fase03/schema_insight/VERIFICA_SCHEMA_INSIGHT_rev004_NON_OK_STORICO.md`
- `A` `studio2/fase03/schema_insight/insight_v1.schema.json`
- `A` `studio2/fase03/schema_insight/integrazione_tag_3_12_prompt.md`
- `A` `studio2/fase03/schema_insight/leakage_rules_v1.json`
- `A` `studio2/fase03/schema_insight/requirements.txt`
- `A` `studio2/fase03/schema_insight/test_validator.py`
- `A` `studio2/fase03/schema_insight/validator.py`

### 8.4 Stato Git al termine di questa richiesta documentale

- **HEAD:** `e82b5a08bf642ad45f77e71832958207beb1181c`; branch avanti di 28 commit rispetto
  a `origin/main` osservato a `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`.
- **File committati:** i 64 percorsi di §8.3, inclusa la versione del presente report contenuta
  in `e82b5a0…`.
- **File tracciati modificati e non committati:** soltanto il presente report, aggiornato per
  completezza in questa richiesta.
- **File staged:** nessuno.
- **File non tracciati:** nessuno.
- Nessun controllo scientifico è stato rieseguito e nessun commit, merge, push o tag è stato
  effettuato per questa richiesta.
- Stato effettivo invariato rispetto al §7: raccordo presente soltanto nel branch locale;
  integrazione/pubblicazione in `main` non eseguite; nessun congelamento o tag 03.12 creato.
- Operazioni residue, dipendenze, decisioni già acquisite e prossimo passo restano quelli del
  §7; in particolare il futuro tag 03.12 può puntare esclusivamente a `3c64390…`.
