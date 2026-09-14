# Prompt — sotto-fase 03.8: piano statistico completo (piano §6.6) con D2, OOD, D11, margine m

Parallelizzabile con 03.6, 03.7, 03.12: dipende dal catalogo D1 e dalla letteratura, non dai dati.
Profilo: decisionale. Modello: **il più capace disponibile, ragionamento esteso**. Si congela
prima del primo run di test (03.11) e non può essere rivisto dopo. Generato 2026-09-13.

---

Lavori la sotto-fase 03.8 della Fase 03 dello studio 2 FoT-TEP: piano statistico completo
(piano §6.6). Cartella: studio2/fase03/piano_statistico/. Branch: codex/studio2-piano-statistico.
Segui docs/prompts/Prompt_LLM.md e Fase_LLM.md; regole in docs/MAINTENANCE.md (§1, §2, §8, in particolare §8.2 «Codice del primo studio» e §8.6). Nessuna chiamata a modelli linguistici, nessuna simulazione. Base: origin/main se contiene già d815ce9 (attuazione 03.4), altrimenti il commit d815ce9 del branch codex/studio2-perimetro-q8. Lavora in un worktree dedicato (git worktree add ../fot-tep-<nome> -b <branch> d815ce9): altre tre sotto-fasi girano in parallelo su altri worktree e la copia principale ha un batch MATLAB in corso. Disciplina per il merge: scrivi solo nella tua cartella e in nuovi file; non modificare studio2/fase03/protocol.py, run_pilot.py, prepare_gate.py, schemas/ esistenti (crea file nuovi e proponi il collegamento); in studio2/PROVENIENZA.md aggiungi solo una sezione nuova in coda con il titolo della tua sotto-fase; non toccare piano, walkthrough, MAINTENANCE, phase_b/, code/: la documentazione arriva dopo la verifica indipendente. Divieto assoluto di guardare dati: non aprire gli output dei run fault
(studio2/fase03/fault_runs/runs/), i risultati di 03.5 (soglie_normal/runs/), evidence o firme
del primo studio, né i risultati per-fault di phase_b/ o dei walkthrough del primo studio oltre
alle definizioni delle metriche; ti servono solo conteggi e definizioni.

Cosa leggere
- Piano: §8.1, §8.3 (ablation local-first, D11), §8.5 (endpoint, tre numeri, H1–H3, margine m,
  gatekeeping, reporting stratificato), §8.6 (OOD e astensione), §8.7 (R=1, gate di stabilità,
  canary, rilevamento cambio modello), §8.8 (budget parametrico 6/8 run), §8.12 solo per E5-C3
  (criterio di successo dell'ablazione dei descrittori, se ricade qui), §9.3 (pavimento e
  soffitto), D2, D7, D11; §0.1 decisioni 2, 3, 4, 5, 11, 12.
- studio2/fase03/selection/CATALOG_FREEZE.json, PROPOSTA_OOD_D11.md (proposta non vincolante:
  le letture possibili di «meccanicamente distinto» e le coppie confondibili), il registro
  docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md §2 (tabella 8 di Downs & Vogel
  trascritta), piano §12.1–12.4 (rilevabilità documentata: gruppo H).
- docs/letteratura.md §14: le voci pertinenti a bootstrap a cluster, intervalli binomiali
  esatti/Wilson, gatekeeping, non inferiorità, open-set/astensione; cita per sigla §14.x.
- In sola lettura come pattern HC: phase_b/evaluation/metrics.py e bootstrap.py (definizioni di
  cluster fisico, strati, unità); docs/fot_walkthrough_conversazione_v2.md solo la sezione che
  definisce il bootstrap e le unità della replica (record del metodo, non risultati).
- docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md per la parte di FAR già congelata
  (03.5): la citi come vincolo, non la ridiscuti.

Cosa fare
1. PIANO_STATISTICO.md, pre-specificato, con per ogni voce la fonte o la dichiarazione «scelta di
   progetto»: popolazione primaria e strati (local-seen/local-unseen, continuità/nuovi, in
   catalogo/OOD); unità di analisi e cluster fisico (run×fault) con 8 agenti; i tre numeri
   dell'endpoint e quale è primario; H1, H2, H3 con forma, test, gerarchia di gatekeeping a 0,05,
   e il margine m con giustificazione operativa e verifica sulla risoluzione del disegno (calcolala
   analiticamente o per simulazione su dati sintetici nulli, senza dati reali); bootstrap a cluster
   stratificato per pseudolabel esteso a 9 classi + astensione, con numero di repliche, seed e
   trattamento delle astensioni; D2: 6 vs 8 run con i numeri di risoluzione a confronto e la tua
   raccomandazione motivata; OOD (decisione 3): la lettura di «meccanicamente distinto» che adotti,
   i due fault risultanti e i loro 6 run, l'analisi di astensione prevista in A/B-LF/E-LF con
   comparatore in-catalogo; D11: coppie confondibili dichiarate e metrica dell'ablation
   local-first; politica R (decisione 11: cosa attiva R=3) e canary (§8.7); regola GO/NO-GO del
   modello con soglie pre-specificate; reporting stratificato obbligatorio; analisi
   descrittive dichiarate tali; threats. Distingui in ogni punto ciò che proponi da ciò che il
   piano già impone.
2. Non decidere ciò che appartiene ad altre sotto-fasi: soglia e FAR (03.5), schema (03.12),
   valori delle pseudolabel (03.7), implementazione della terza metrica e del bootstrap (03.10):
   qui ne scrivi la specifica, il codice arriva dopo. Se una tua scelta le vincola, dichiaralo.
3. Codice minimo: uno script di risoluzione del disegno (potenza/semiampiezza attesa per H1–H3
   con 48 e 64 cluster, su dati sintetici) con test, così che i numeri del documento siano
   riproducibili; nessun accesso a dati reali, guardia esplicita nel codice.
4. PIANO_STATISTICO_FREEZE.json con impronte e stato «proposed_pending_author_decisions»: D2,
   OOD, D11 e m sono decisioni dell'autore e restano aperte finché non le conferma; il documento
   le presenta con la raccomandazione, non le chiude. Nessun tag.
5. REPORT_PIANO_STATISTICO.md secondo Fase_LLM.md punti 1–7; test_explanation.py prima e dopo;
   commit studio2(fase03): … (documento; script e test; freeze proposto).

Riporta alla fine
La tabella delle decisioni (D2, OOD, D11, m, politica R, GO/NO-GO) con raccomandazione e fonte; i
numeri di risoluzione per 6 e 8 run; ciò che il piano impone e ciò che è scelta di progetto; commit
creati; le decisioni che richiedono il mio intervento.
