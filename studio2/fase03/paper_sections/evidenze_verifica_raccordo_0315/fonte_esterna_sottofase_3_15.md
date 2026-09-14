# Prompt — sotto-fase 03.15: sezioni del paper indipendenti dal modello (piano §6.12)

Parallelizzabile con 03.9, 03.10, 03.14: dipende solo da artefatti congelati (catalogo, run di
sviluppo, schema, pseudolabel, evidence) e da letteratura.md. Profilo: decisionale/redazionale.
Modello: il più capace, ragionamento esteso. Nessun risultato sperimentale esiste: le sezioni si
scrivono senza numeri di esito. Generato 2026-09-13.

---

Lavori la sotto-fase 03.15 della Fase 03 dello studio 2 FoT-TEP: le sezioni del paper
indipendenti dal modello (piano §6.12): related work, descrizione del metodo, verbalizzatore ed
evidence, protocollo/disegno per la parte già congelata, threats to validity. Sono le parti comuni
alla versione Q8 e alla versione Terra-only del piano B (D9 opzione 3) e vanno scritte in modo che
entrambe le versioni le riusino senza modifica. Cartella: studio2/fase03/paper_sections/. Branch:
codex/studio2-paper-sections. Segui docs/prompts/Prompt_LLM.md e Fase_LLM.md; regole in docs/MAINTENANCE.md (§1, §2, §8, in particolare §8.2 «Codice del primo studio» e §8.6). Nessuna chiamata a modelli linguistici, nessuna simulazione in questa finestra. Base: origin/main (≥ 46c0b62, che contiene 03.4 e 03.7). Worktree dedicato (git worktree add .worktrees/<nome> -b <branch> origin/main): altre sotto-fasi girano in parallelo. Disciplina per il merge: scrivi solo nella tua cartella e in file nuovi; non modificare protocol.py, run_pilot.py, prepare_gate.py, schemas/ esistenti (crea file nuovi e proponi il collegamento nel report); in studio2/PROVENIENZA.md aggiungi solo una sezione nuova in coda con il titolo della tua sotto-fase (la numerazione si allinea al merge); non toccare piano, walkthrough, MAINTENANCE, phase_b/, code/: la documentazione arriva dopo la verifica indipendente. Input di altre sotto-fasi non ancora in main si leggono dai loro branch e release per commit e impronta, mai copiandoli: 03.6 = branch codex/studio2-evidence (2f6dd8d) e release studio2-fase03-evidence-v1 (archivio 3e1eb87f…); 03.12 = branch codex/studio2-schema-insight, byte congelati a e058cb0 (manifest d6ef52de…), tag studio2-fase03-schema-insight-frozen-001 quando pubblicato; 03.7 = main, tag studio2-fase03-pseudolabel-frozen-001; 03.5 = branch codex/studio2-soglie-normal (THRESHOLD_FREEZE.json a 9507143); 03.8 = branch codex/studio2-piano-statistico (piano PROPOSTO, decisioni dell autore ancora aperte: si implementa la specifica marcandola pending, non la si assume congelata). Le bozze stanno in questa cartella; il report propone se e
quando spostarle in docs/paper/ (categoria «Materiale del paper», MAINTENANCE §1): non decidere tu.

Cosa leggere
- Piano: §8.10 (che cosa va nel paper, con le due avvertenze su conformità/EviFDD e related work
  obbligatoria), §8.1–8.4, §8.6, §8.9, §8.12, §9, §12.5–12.9 (prior art federato: affermazioni
  non sostenibili e novità difendibile), §13 (risposte alle 14 domande), §2 (critiche al piano
  originale), §5 (tabella critiche); §0.1 per sapere che cosa NON è ancora deciso.
- docs/paper/FoT_TEP_paper_blueprint.html (struttura prevista del paper) e docs/letteratura.md
  §14.1–14.6: è l'unica fonte bibliografica; ogni citazione porta la sigla §14.x e nessun lavoro
  entra se non è nel corpus (i sei riferimenti metodologici di 03.8 e McMahan per FedAvg vanno
  segnalati per Letteratura_LLM, non citati come se fossero già dentro).
- Artefatti congelati da descrivere per quello che sono: selection/ (criteri e catalogo D1, tag),
  fault_runs/SPECIFICA_RUN_FAULT.md e REPORT (40 run, innesco 25 h, orizzonte 40 h, otto finestre,
  Philox), 03.5 (allocazione 350/150, forma economica, regola S > soglia: la soglia numerica e il
  FAR NON si citano finché la verifica non è OK), 03.6 (pipeline feature → JSON → testo → 697-D,
  U3), 03.7 (pseudolabel opache, assegnazione, derangement), 03.12 (schema a sei campi, cap,
  parità fra producer, diff B→E, conformità), 03.8 come disegno PROPOSTO (H1–H3, m, bootstrap:
  descrivili come pre-specificati «al congelamento», con segnaposto per i valori che l'autore deve
  confermare).
- MAINTENANCE §8.2 «Provenienza interna, descrizione onesta nel paper»: i dati del primo studio si
  descrivono come configurazione, seed, data di generazione; niente narrazione del primo studio.
  docs/fot_walkthrough_conversazione_v2.md solo per i due numeri che §8.10 punto 1 ammette come
  motivazione (B = 86,1 %, replica 94,4 %), letti dagli artefatti che il walkthrough cita, con la
  frase esatta «dichiarato descrittivo».

Cosa fare
1. PIANO_SEZIONI.md: mappa delle sezioni comuni con, per ciascuna, fonti, che cosa può essere
   scritto ora e che cosa resta segnaposto (marcato «[RISULTATO]» o «[DECISIONE: …]»), e quali
   frasi differiscono fra versione Q8 e Terra-only (varianti in blocchi marcati, non due
   documenti).
2. Bozze in Markdown, una per sezione: related_work.md (P042, P041, P031, P030, P065, P001,
   FaultExplainer, EviFDD-Agent, Zhang 2026, Xu 2026 e il resto pertinente di §14, con le
   distinzioni di §12.7–12.9 e §8.10 punto 7: che cosa non si rivendica); method.md (FoT, agenti,
   insight, condizioni A/B-LF/E-LF, local-first, producer-swap, schema, astensione D10);
   verbalizer.md (pipeline congelata, 697-D, neutralità, anti-leakage, provenienza della baseline
   secondo §8.2); protocol.md (catalogo con criteri pre-specificati, run di sviluppo/test con
   separazione dei seed, calibrazione Normal, pseudolabel, endpoint e ipotesi con segnaposto);
   threats.md (le dodici di 03.8 §14 più quelle strutturali: simulatore, scala, scope FL CF1/CF5,
   validità esterna, R=1, dipendenza dal modello). Stile: sobrio, nessuna affermazione di novità
   oltre §12.9, nessun numero senza fonte, nessun numero di esito; ogni paragrafo con la fonte
   fra parentesi quadre da rimuovere in fase finale.
3. Controlli: script di lint minimale che segnala numeri privi di fonte, citazioni non presenti
   in letteratura.md, F-number accanto a pseudolabel, parole «novel/first/unique» non
   autorizzate; eseguito sulle bozze, esito nel report.
4. REPORT_PAPER_SECTIONS.md secondo Fase_LLM.md punti 1–7 (fuori perimetro: risultati, abstract,
   conclusioni, figure); test_explanation.py prima/dopo; commit separati (piano delle sezioni;
   bozze; lint e report). Nessuna modifica a letteratura.md: le segnalazioni bibliografiche vanno
   in una lista per Letteratura_LLM.

Riporta alla fine
La mappa delle sezioni con lo stato (scritta/segnaposto); la lista dei riferimenti da far entrare
nel corpus; le varianti Q8/Terra-only; esito del lint; commit creati; ciò che resta aperto e le
decisioni che richiedono il mio intervento (collocazione in docs/paper/ compresa).
