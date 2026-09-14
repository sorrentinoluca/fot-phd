# Acquisizione della riverifica finale — sotto-fase 03.15

Data: 2026-09-14. Questo record è successivo al candidato verificato e al report
storico. Registra l'acquisizione del verbale finale senza modificare le bozze
scientifiche né riscrivere la richiesta di riverifica rimasta in
`REPORT_PAPER_SECTIONS.md`.

## Identità e acquisizione

- Branch destinatario: `codex/studio2-paper-sections`.
- Candidato verificato e HEAD prima dell'acquisizione:
  `cf79e81f917c7969dfd375e38db54315c28d4c07`.
- Base del candidato: `46c0b623f55154684f326a8523521fb28991fb09`.
- Verbale acquisito: `VERIFICA_PAPER_SECTIONS.md`.
- Dimensione: **13.949 byte**.
- SHA-256: `8faca80c87071d87bf66d97848c290a5724f6569be6f6040cfb6568bad022cb1`.
- Sorgente esterna: worktree detached
  `/Users/luker/fot-tep/.worktrees/verifica-paper-sections-esterna`, HEAD
  `cf79e81f917c7969dfd375e38db54315c28d4c07`.
- Metodo: copia byte per byte, verificata con confronto binario, dimensione e
  SHA-256 prima e dopo l'acquisizione.

Il verbale identifica esplicitamente `cf79e81f917c7969dfd375e38db54315c28d4c07`
come commit verificato e conclude **OK**, senza rilievi bloccanti. Conserva inoltre
nel proprio §B il primo passaggio NON OK su `e2f9aea948ac4bfc64089962c5357343f997621f`;
non sostituisce né cancella quella traccia storica. L'OK vale per il pacchetto
03.15 a `cf79e81`, non per un manoscritto finale né per modifiche successive.

## Stato effettivo

Il pacchetto scientifico corrente della 03.15 è **riverificato OK** e il verbale
finale è ora acquisito nel branch. La richiesta di un nuovo passaggio presente nel
report descrive lo stato storico precedente a questo record e non autorizza una
terza review dello stesso candidato.

La sotto-fase 03.15 resta **aperta prima dell'integrazione**: le fonti maturate dopo
la base `46c0b62` richiedono un delta separato di allineamento. Quel futuro delta
scientifico non erediterà l'OK di `cf79e81` e dovrà essere sottoposto a verifica
indipendente. D9, identità e ruoli dei modelli, producer alternativo D9.1,
risultati, abstract e conclusioni restano aperti; nessun pilot, inferenza o
simulazione è autorizzato da questa acquisizione. La Fase 03 resta aperta.

## Allineamenti futuri da preparare e poi verificare indipendentemente

Nessuno degli allineamenti seguenti è applicato in questo commit.

| Allineamento | Fonti esatte | File destinazione e delta futuro |
| --- | --- | --- |
| `normal_dev` reale della 03.9 | `origin/main` `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`: `studio2/fase03/baseline_numerica/SPECIFICA_NORMAL_DEV.md`, `REPORT_BASELINE_NUMERICA.md`, `DECISIONE_ACCETTAZIONE_NORMAL_DEV.md`, `CONSEGNA_INTEGRAZIONE_03_9.md`, `PROTOTYPES.json` e `PROTOTYPES_MANIFEST.json` | `protocol.md`: aggiungere il ruolo esclusivo di sviluppo, 40 run preassegnati (5 per agente), 320 finestre ma 40 cluster fisici, e i divieti di fit/calibrazione/FAR/test; dichiarare che 03.9 è integrata e i dati sono pubblicati ma il freeze resta inefficace finché persistono i raccordi registrati. `verbalizer.md`: registrare 320 evidence Normal da 697 componenti nella destinazione riuscita `evidence/normal_dev_002`, gli otto esempi locali pre-specificati, i prototipi (9 globali, 16 locali; 25 vettori) e la dipendenza U3 dalla coppia N1–N5/soglie V2 con rigenerazione fail-closed se R2 decade. Non trasformare le 320 finestre in repliche indipendenti né in risultati di performance. |
| Chiusura effettiva 03.5 | `origin/main` `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`: `studio2/fase03/soglie_normal/INTEGRAZIONE_03_5.md`, `THRESHOLD_FREEZE.json`, `FAR_VERIFICATION.json`, `FAR_VERIFICATION.md`, `DECISIONE_AUTORE_FAR.md` e `evidence/VERIFICA_CORREZIONI_SOGLIE_NORMAL_OK.md` | `verbalizer.md`: sostituire il residuo “finché la verifica indipendente di 03.5” con lo stato chiuso/pubblicato e riportare, con fonte, soglia `13.623626738268857`, rango 334 su 350 e regola stretta `S > threshold`; FAR primario 11/150 = 7,333% con IC Clopper–Pearson 95% [3,7175%; 12,7424%], distinto dal secondario 108/1500 = 7,2% con bootstrap per run 95% [5,7333%; 8,7333%]. `protocol.md`: aggiornare la descrizione temporale a freeze della soglia prima dell'apertura analitica di `far_ver`, preservando il limite approvato che il sigillo prova identità e ordine delle analisi ma non l'assenza assoluta di accessi precedenti. Non ricalibrare né reinterpretare la soglia. |
| Decisioni statistiche rev. 10 della 03.8 | Candidato verificato `6aaa5b3eebfed4ba502c25c0443caabd0051af21`, acquisizione `51782e8c40069c0a2310afafc36907a61d517ff6`: `studio2/fase03/piano_statistico/PIANO_STATISTICO.md`, `DECISIONI_AUTORE_03_8_DA_SOTTOSCRIVERE_REV10.md`, `BUDGET_RISORSE_REV10.md`, `CONSEGNA_REV10.md` e `VERIFICA_PIANO_STATISTICO_REV10.md` | `protocol.md`: sostituire i segnaposto statistici con D2=8 (64 cluster fault più 8 Normal primari); H1/H2 con Hoeffding sulle medie di cluster in [−1,1]; H3 con Tango score, margine `m=0,125`, α unilaterale 0,05 e sensibilità H3 separata a 0,025; sequenza H1→H2→H3; reporting guadagnati/persi/saldo e segnalazione descrittiva saldo≤−2 su 8; OOD F6/F4 condizionati con catene di sostituzione; D11 `{F1,F2}` e `{F14,F15}`, run 1–3; politica R basata su divergenza della coppia parsata o validità, con audit/canary e fattibilità R=3 ancora operativa. Conservare esplicitamente che firma materiale, freeze/tag statistico, controlli tecnici OOD, fattibilità T5 e D9 restano pending. `verbalizer.md`: solo raccordare la terminologia degli endpoint/conteggi e dell'astensione se necessario per coerenza con `protocol.md`; non aggiungere esiti osservati. |

Prima di applicare il delta, riallineare il branch sullo stato allora corrente senza
sovrascrivere lavoro concorrente, ricontrollare le fonti e limitare le modifiche ai
file effettivamente necessari. Dopo il delta: lint delle cinque sezioni,
`git diff --check`, guardiano documentale e nuova verifica indipendente del solo
delta più la sua coerenza con il pacchetto già approvato.

## Controlli di questa acquisizione

- Prima della scrittura il branch era pulito; `origin/main` locale e remoto erano
  entrambi `c486eee95fe24c1e7bf4135ed7cebf01ac2962f1`.
- Baseline documentale: 35 test, 14 fallimenti preesistenti e 1 skip.
- Lint del pacchetto scientifico: 5 file, 0 segnalazioni.
- Nessuna bozza scientifica, report storico, piano, walkthrough, letteratura,
  artefatto congelato o file fuori da `paper_sections/` è stato modificato.
- Nessun merge, push o tag; nessun nuovo giro di review su `cf79e81`.
