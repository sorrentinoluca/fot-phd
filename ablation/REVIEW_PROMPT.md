# External Review Prompt: Ablation Experiment Pipeline

## Istruzioni per il revisore

Sei un revisore esterno esperto di machine learning applicato a serie temporali industriali, experimental design e ingegneria del software. Ti viene chiesto di effettuare una review **completa** (logica + tecnica) della pipeline di esperimento ablativo descritto di seguito.

La review deve essere **strutturata in due sezioni** (Logica e Tecnica), ciascuna con findings classificati per severità (CRITICO / IMPORTANTE / SUGGERIMENTO). Per ogni finding, fornisci:
1. Cosa hai trovato
2. Perché è un problema
3. Soluzione proposta concreta

---

## Contesto del progetto

### FoT-TEP (Federation-of-Thoughts for Tennessee Eastman Process)

Un framework di diagnosi di fault industriali in cui agenti LLM specializzati analizzano descrizioni testuali di dati sensoriali del Tennessee Eastman Process (TEP). Il TEP è un benchmark chimico-industriale con 41 variabili di processo XMEAS campionate ogni minuto.

**Phase A** ha sviluppato un **verbalizer deterministico V2**: trasforma serie temporali grezze in testo neutro (senza etichette) tramite 5 feature statistiche per variabile per finestra temporale, confrontate con soglie conformali (α=0.05) calcolate su un baseline normale.

**Phase B** ha testato un protocollo federato (FoT) a 4 agenti specializzati con scambio di insight tra pari, ottenendo un miglioramento B−A = +0.8611, 95% CI [0.833, 0.917] sulla classification a 2 classi (fault locale + Normal).

### Scopo dell'ablazione

L'analisi critica del progetto ha identificato una debolezza: **non è mai stato dimostrato empiricamente che la rappresentazione V2 è superiore ad alternative**. Questo esperimento ablativo confronta 4 strategie di TS→text sugli stessi dati, stesso LLM, stessa struttura di prompt, per isolare l'effetto della rappresentazione.

---

## Design dell'esperimento

- **Bracci:** 4 (V2_TEXT, RAW_FEATURES, CGTIME_STATS, SAX_SYMBOLIC)
- **Casi:** 15 held-out (PBH-001..015): 3× F1, 3× F8, 3× F10, 3× F13, 3× Normal
- **Classificazione:** 5 classi centralizzata (tutti i 5 label visibili a ogni braccio)
- **Esempi nel prompt:** 10 (2 per classe), renderizzati nel formato del braccio
- **LLM:** GPT-5.6-terra, Responses API, structured output, reasoning_effort=medium
- **Ripetizioni:** 3 per braccio × caso = 180 inferenze totali
- **Metriche:** Accuracy (abstention=wrong), fault-only accuracy, recall per classe, majority vote, bootstrap 95% CI (10K resamples), McNemar pairwise, confusion matrix

### I quattro bracci

| Braccio | Approccio | ~Parole/caso | Ispirato da |
|---------|-----------|--------------|-------------|
| **V2_TEXT** | Verbalizer V2 conformal: 8 finestre × 5h, 5 feature/var/window, confronto soglie, linguaggio naturale | ~137 | FoT-TEP Phase A |
| **RAW_FEATURES** | Stesse 5 feature numeriche V2 ma in formato tabella CSV senza soglie, senza interpretazione temporale, senza linguaggio naturale | ~370 | LLMTime-style serialization |
| **CGTIME_STATS** | Profilo statistico a 3 famiglie: Direct (10 stat/var), Marginal (14 stat/var), Joint (29 stat sistema) = ~1014 statistiche totali, JSON strutturato | ~2312 | CGTime (Feng et al. 2026) |
| **SAX_SYMBOLIC** | Symbolic Aggregate approXimation: Z-norm → PAA (word_size=10) → 5-letter alphabet, per variabile per finestra | ~694 | SAX / HAR-LLM (Pappa 2026) |

---

## File da esaminare

### 1. `ablation_representations.py` (~719 righe)

Genera le 4 rappresentazioni. Funzioni chiave:

- `represent_v2_text()`: pass-through al verbalizer V2 esistente (frozen)
- `represent_raw_features()`: tabella CSV delle 5 feature numeriche senza soglie
- `represent_cgtime_stats()`: profilo statistico CGTime-aligned con sottofunzioni:
  - `_direct_stats(series)` → 10 statistiche level/scale per variabile
  - `_marginal_stats(series, dt_h)` → 14 statistiche temporali/strutturali per variabile
  - `_pca_stats(data_matrix)` → 11 statistiche PCA di sistema
  - `_correlation_stats(data_matrix)` → 6 statistiche di correlazione
  - `_mahalanobis_stats(data_matrix, ref_mean, ref_cov_inv)` → 4 indicatori di rischio
  - `_windowed_correlation_stability(d, start_h, end_h, window_h)` → 4 statistiche di stabilità
  - `_per_channel_sync_with_pca(data_matrix)` → 4 statistiche di sincronizzazione
- `represent_sax_symbolic()`: encoding SAX con breakpoints da distribuzione normale standard
- `ARMS` dict e `generate_all_representations()` come interfaccia unificata

### 2. `ablation_runner.py` (~600 righe)

Runner dell'inferenza. Struttura:

- `LABEL_SPACE = ["F1", "F8", "F10", "F13", "Normal"]`
- `EXAMPLE_SOURCES`: mappa classi → file development (batch 1-2), Normal → blocchi N1-N2 dal baseline 500h
- `OUTPUT_SCHEMA`: JSON schema strict per Responses API (predicted_label, abstain, reasoning_summary)
- `PROMPT_TEMPLATE`: prompt centralizzato con label space, 10 esempi, caso da diagnosticare
- `load_baseline()`: carica normal 500h, split in 5 blocchi da 50h, calcola baseline stats
- `prepare_example_representations()`: genera 10 esempi × 4 bracci
- `call_openai()`: OpenAI Responses API con structured output
- `build_inference_schedule()`: 15 × 4 × 3 = 180 inferenze
- `run_ablation()`: loop principale con pre-generazione, resume JSONL, retry con backoff
- CLI: `--project-root`, `--dry-run`, `--resume`, `--model`, `--repetitions`, `--reasoning-effort`

### 3. `ablation_evaluate.py` (~430 righe)

Valutazione statistica. Calcola:

- Accuracy overall e fault-only (abstention = wrong)
- Per-class recall per tutti e 5 i label
- Majority vote accuracy (plurality su 3 ripetizioni)
- Repetition agreement (frazione di casi con 3/3 consenso)
- Bootstrap 95% CI (10K resamples, seed=42) per accuracy
- Bootstrap paired accuracy difference CI per confronti pairwise
- McNemar's test con continuity correction su coppie (case_id, rep) matched
- Confusion matrix 5×5 + colonna ABSTAIN
- Token usage statistics
- Report markdown e JSON

### 4. `EXPERIMENT_DESIGN.md`

Documentazione del protocollo sperimentale.

---

## Aree di review richieste

### PARTE 1: REVIEW LOGICA (Experimental Design)

Valuta la correttezza e la solidità del design sperimentale:

1. **Validità del confronto:** I 4 bracci sono confrontabili equamente? Ci sono confound non controllati (es. lunghezza del prompt, densità informativa, formato di presentazione)?

2. **Equità della finestra temporale:** V2_TEXT usa 8 finestre × 5h (10-50h). RAW_FEATURES usa le stesse finestre. Ma CGTIME_STATS opera sull'intero periodo post-injection come vettore unico (nessuna windowing interna per le statistiche per-variabile, solo per `_windowed_correlation_stability`). SAX_SYMBOLIC usa le stesse 8 finestre. Questa asimmetria è problematica?

3. **Prompt bias per lunghezza:** V2_TEXT ~137 parole vs CGTIME_STATS ~2312 parole. Il modello potrebbe performare diversamente per puro effetto della lunghezza del contesto. Come si può controllare questo?

4. **Scelta degli esempi:** 10 esempi (2 per classe) sono sufficienti per 5-class classification? La scelta di batch 1-2 per gli esempi e batch 11-14 per i test è adeguata per evitare leakage temporale?

5. **Potenza statistica:** 15 casi × 3 ripetizioni = 45 osservazioni per braccio. È sufficiente per rilevare differenze significative? Qual è il minimum detectable effect dato N=45?

6. **Confrontabilità con Phase B:** Phase B usava 2-label per-agent (fault locale + Normal), 4 agenti specializzati, scambio di insight. Questa ablazione usa 5-label centralizzato. Quanto è informativo il confronto? Quali caveat servono?

7. **Rappresentatività del CGTime arm:** L'implementazione rispecchia fedelmente la filosofia CGTime di Feng et al.? Mancano componenti critiche (es. il PCA cross-channel description reduction O(rK) del paper originale)?

8. **Leakage e contamination:** Ci sono rischi di information leakage tra bracci (condividono lo stesso LLM, la stessa sessione API)? Le ripetizioni sono veramente indipendenti?

9. **Metriche:** Le metriche scelte catturano gli aspetti rilevanti? Manca qualcosa (es. calibrazione, analisi degli errori sistematici per tipo di fault, analisi della reasoning quality)?

10. **Generalizzabilità:** I risultati su 4 fault specifici (F1, F8, F10, F13) + Normal generalizzano? Perché proprio questi fault? Ci sono selection bias?

### PARTE 2: REVIEW TECNICA (Code Correctness)

Valuta la correttezza implementativa:

#### ablation_representations.py

11. **`_direct_stats`**: Il calcolo di `std` usa `ddof=1` (campionaria). È coerente con il baseline? `max_peak_prominence` con `prominence=0` in `find_peaks` — è corretto o cattura noise?

12. **`_marginal_stats`**: Il calcolo di R² usa lo slope calcolato in ore (`dt_h`) ma il vettore `t` per predicted usa indici moltiplicati per `dt_h`. Verificare la coerenza dimensionale. Lo `spectral_entropy` è normalizzato correttamente?

13. **`_pca_stats`**: Usa `eigvalsh` per gli eigenvalue e `eigh` separatamente per gli eigenvector. Perché non una sola chiamata? C'è rischio di mismatch nell'ordinamento? Il `pca_k` con `searchsorted` è corretto al boundary?

14. **`_correlation_stats`**: `volatility_sync_index` calcola correlazione su `abs(diff())`. È robusto per serie con varianza molto diversa? NaN handling?

15. **`_mahalanobis_stats`**: Usa `ref_cov_inv = diag(1/σ²)` (inversione diagonale). Il CGTime paper usa la full covariance inverse. Questo semplifica troppo perdendo le correlazioni cross-variable?

16. **`_windowed_correlation_stability`**: Usa `iter_time_windows` che richiede un DataFrame con `Time` column. Ma il DataFrame passato è `d` (pre-normalizzato). Verificare che i filtri temporali siano coerenti.

17. **`_sax_encode`**: La Z-normalization è per-window (locale). Sarebbe più appropriata una Z-norm rispetto al baseline? L'uso di `np.round` per i confini PAA potrebbe creare segmenti di lunghezza disuguale — è un problema?

18. **Normal example handling:** Per Normal, usa blocchi N1 (0-50h) e N2 (50-100h) dal file `mode1_normal_500.xlsx`. Il config viene modificato con `fault_injection_h = start`. Ma la V2 window analysis parte da `fault_injection_h` — quindi per N1 analizza 0-50h e per N2 analizza 50-100h. Questo è coerente con il fatto che i casi held-out Normal (PBH-001..003) hanno fault_injection_h=0 (dal config) e end=50h?

#### ablation_runner.py

19. **`_init_imports` e global state**: Il pattern con moduli globali `None` poi importati è fragile. Se `_init_imports` non viene chiamato prima dell'uso, si ottengono `AttributeError` su `None.ARMS`. C'è un guard?

20. **`call_openai`**: L'estrazione dell'output dal response object (`response.output`) usa un pattern di iterazione con `hasattr`. È robusto per la versione attuale della Responses API? Il campo `text=OUTPUT_SCHEMA` nella chiamata è la sintassi corretta per structured output?

21. **Retry logic**: `max_retries=2` con `for attempt in range(1, max_retries + 1)`. Il `for...else` clause si attiva solo se il loop completa senza `break`. Ma con `max_retries=2`, il loop fa solo 2 iterazioni, non 3 (original + 2 retry). È intenzionale?

22. **Resume correctness**: Il resume riapre il JSONL in append mode. Ma le rappresentazioni vengono ri-generate da zero (non salvate/caricate dal run precedente). Se il codice delle rappresentazioni cambia tra i run, i prompt_hash differiranno — è un problema?

23. **Example ordering**: Gli esempi vengono generati iterando `EXAMPLE_SOURCES.items()`. L'ordine dei dict in Python 3.7+ è garantito d'inserzione, ma l'ordine di presentazione degli esempi potrebbe influenzare il modello. È randomizzato? Dovrebbe esserlo?

#### ablation_evaluate.py

24. **`bootstrap_accuracy_diff_ci`**: Il p-value è calcolato come `(boot_diffs <= 0).mean()` quando `point >= 0`. Questo è un test one-sided. Ma il report lo presenta come generico "p(bootstrap)". È potenzialmente fuorviante?

25. **McNemar's test**: Usa `(abs(n_a_only - n_b_only) - 1)² / (n_a_only + n_b_only)` con continuity correction. Con N=45 per braccio, le celle discordanti potrebbero essere molto piccole. McNemar è appropriato o serve un test esatto (binomiale)?

26. **`majority_vote_accuracy`**: Con 3 ripetizioni e possibili 5 etichette diverse, il "majority" potrebbe essere una plurality di 1 voto. Serve un threshold minimo (es. almeno 2/3 concordi)?

27. **Bootstrap seed handling**: `rng` è creato una volta con `seed=42` e passato sequenzialmente. L'ordine di chiamata influenza la riproducibilità — se si aggiunge un braccio, tutti i CI cambiano. È accettabile?

#### Cross-cutting

28. **Determinismo delle rappresentazioni**: V2_TEXT è deterministico per design. RAW_FEATURES e SAX_SYMBOLIC lo sono (stesse operazioni NumPy). CGTIME_STATS: `_pca_stats` usa `eigh` che è deterministic su stessi input. Ma il floating point ordering nelle somme potrebbe variare? Verificare.

29. **NaN/Inf handling**: Cosa succede se un XMEAS ha valori costanti (std=0)? `_sax_encode` gestisce con `"c" * word_size`. `_marginal_stats` gestisce il `cv` con guard `abs(mean) > 1e-12`. Ma `_correlation_stats` con `corrcoef` su colonne costanti potrebbe produrre NaN. È gestito?

30. **Token context window**: CGTIME_STATS produce ~332K chars (~83K tokens). Con 10 esempi nello stesso formato, il prompt totale potrebbe superare il context window del modello. Il runner controlla questo? Qual è il context window di GPT-5.6-terra?

---

## Output atteso

Produci un report strutturato con:

1. **Summary Score**: valutazione complessiva (1-10) per solidità logica e correttezza tecnica
2. **Findings critici**: problemi che invaliderebbero i risultati se non corretti
3. **Findings importanti**: problemi che riducono l'affidabilità ma non invalidano
4. **Suggerimenti**: miglioramenti opzionali
5. **Checklist pre-esecuzione**: lista di verifiche da completare prima di lanciare il run reale
6. **Verdict**: GO / GO con riserve / NO-GO, con motivazione
