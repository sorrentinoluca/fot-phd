# Review esterna — pipeline di ablazione TS→text

## Summary score

- Solidità logica: **4/10**
- Correttezza tecnica: **5/10**
- **Verdict: NO-GO** per il run reale finché non vengono corretti i problemi critici sotto.

La pipeline è leggibile, compilabile e ha una buona struttura di resume/artefatti, ma il confronto non isola ancora l’effetto della rappresentazione: CGTIME usa statistiche globali sul periodo post-iniezione, mentre gli altri bracci usano otto finestre; inoltre il controllo di validità numerica e di contesto è insufficiente.

## Findings critici

### Logica

**L1 — CRITICO — Confound temporale.** V2, RAW e SAX elaborano 8 finestre da 5 h; CGTIME calcola Direct, Marginal, PCA, correlazioni, Mahalanobis e sincronizzazione sull’intero intervallo post-iniezione (`ablation_representations.py:541-573`). Solo la stabilità delle correlazioni è windowed. Questo cambia informazione disponibile, aggregazione e perdita di fase, quindi una differenza di accuratezza non è attribuibile solo al formato. **Soluzione:** rendere tutti i bracci window-aligned, oppure dichiarare e testare esplicitamente due fattori separati: rappresentazione × aggregazione temporale.

**L2 — CRITICO — Prompt fortemente sbilanciato.** Il braccio CGTIME inserisce molte più statistiche e token; gli esempi sono anch’essi nel formato CGTIME. La lunghezza e il carico cognitivo sono dunque parte del trattamento. **Soluzione:** pre-registrare budget di token comparabili, oppure aggiungere controlli matched-length/troncati e riportare accuratezza stratificata per lunghezza/token.

**L3 — CRITICO — Potenza effettiva bassa.** Le 45 righe per braccio non sono 45 casi indipendenti: le tre ripetizioni condividono lo stesso caso e prompt. L’unità scientifica primaria è quindi circa **15 casi** (e solo 3 per classe). Con N=45, una differenza indipendente attorno a ~0.20–0.30 è già difficile da rilevare; clusterizzando per caso il MDE è sensibilmente maggiore. **Soluzione:** pre-registrare l’effetto minimo rilevante, usare bootstrap stratificato/cluster-by-case e aggiungere casi indipendenti, non solo ripetizioni.

**L4 — IMPORTANTE — Confronto con Phase B non diretto.** Phase B è 2-label, per-agent, specialistica e federata; qui è 5-label centralizzata. Il confronto di accuratezza assoluta non misura il delta FoT. **Soluzione:** usare solo il ranking relativo tra bracci come endpoint primario e dichiarare il caveat; aggiungere, se serve, una condizione V2 con il protocollo Phase B.

**L5 — IMPORTANTE — Campionamento dei fault non giustificato.** F1/F8/F10/F13 e tre casi per classe possono avere difficoltà molto diverse e non rappresentano il benchmark. **Soluzione:** motivare la selezione prima del run, includere almeno un campione bilanciato di fault e riportare intervalli per classe e una replica su fault non visti.

**L6 — IMPORTANTE — Esempi few-shot e ordine.** Due esempi per classe sono fragili; batch 1–2 vs held-out 11–14 riduce leakage diretto ma non prova indipendenza di generazione/simulazione. L’ordine dei 10 esempi è fisso (`EXAMPLE_SOURCES.items()`), quindi può introdurre recency/order bias. **Soluzione:** fissare un ordine pre-registrato e replicare con più permutazioni bilanciate, oppure randomizzare identicamente per arm e seed.

**L7 — SUGGERIMENTO — Metriche incomplete.** Aggiungere balanced accuracy/MCC, macro-F1, intervalli per classe, calibrazione/confidence (se disponibile), costo/latency, e codifica degli errori per fault e tempo di osservazione. La reasoning summary va valutata con rubriche cieche, non usata come evidenza di correttezza.

**L8 — IMPORTANTE — CGTime non è una replica fedele dimostrata.** Il codice è esplicitamente “CGTime-inspired” e implementa un sottoinsieme adattato; non implementa una dimostrazione completa dell’eventuale description reduction PCA O(rK) del paper. Non va presentato come replica di CGTime. **Soluzione:** chiamarlo baseline statistico ispirato a CGTime, elencare metriche incluse/escluse e aggiungere una verifica contro il paper o un’implementazione di riferimento.

### Tecnica

**T1 — CRITICO — NaN/Inf non gestiti end-to-end.** `np.corrcoef` può restituire NaN senza sollevare eccezione (`:357`, `:380`, `:448`, `:508`); anche mean/std/PCA/Mahalanobis possono propagare NaN. `json.dumps` può emettere `NaN`, non valido per JSON strict, o il prompt può contenere valori non finiti. **Soluzione:** validare input dopo `normalize_schema`, usare `np.isfinite`, gestire colonne costanti con correlazione 0, e rifiutare/registrare ogni profilo non finito prima del prompt.

**T2 — CRITICO — Nessun controllo del context budget.** Il runner calcola solo caratteri/word approximation (`ablation_runner.py:400-413`), non tokenizza né rifiuta prompt troppo grandi. La documentazione ufficiale indica per GPT-5.6-terra una context window di 1.050.000 token e max output 128.000; quindi ~83K token non supera quel limite, ma il codice non garantisce che la stima sia corretta né che un altro modello abbia lo stesso limite. [OpenAI model docs](https://developers.openai.com/api/docs/models/gpt-5.6-terra) **Soluzione:** usare tokenizer/API usage preflight, applicare un limite configurabile con margine e abortire prima delle chiamate se superato.

**T3 — IMPORTANTE — Mahalanobis semplificato.** `ref_cov_inv` è diagonale (`:546-551`), quindi elimina tutte le correlazioni cross-variable; non è il Mahalanobis full-covariance descritto come riferimento. Può cambiare molto il braccio CGTIME. **Soluzione:** usare la covariance completa regolarizzata (Ledoit–Wolf/shrinkage o pseudoinversa) stimata solo dal baseline e documentare la scelta.

**T4 — IMPORTANTE — `find_peaks(..., prominence=0)` cattura ogni massimo locale.** In dati rumorosi `max_peak_prominence` può essere guidato da rumore; inoltre non c’è smoothing/prominence minima (`:134`). **Soluzione:** rendere prominence/distance un iperparametro pre-registrato, calibrato sul baseline, o rimuovere la metrica dal confronto.

**T5 — IMPORTANTE — PCA duplicata e fallback incompleto.** `eigvalsh` e `eigh` sono ordinati coerentemente dopo `argsort`, quindi non c’è un mismatch ordinario, ma sono due decomposizioni inutili (`:273-282`). Il fallback può lasciare `total` non definito se `eigh` fallisce e poi viene usato a `:296`. **Soluzione:** una sola `eigh`, inizializzare sempre `total`, e testare casi degeneri. `searchsorted(...)+1` è corretto per il primo cumulativo >= .9, ma va testato su cumulative esattamente .9 e matrice a varianza zero.

**T6 — IMPORTANTE — Resume non protegge la provenienza.** In resume le rappresentazioni vengono rigenerate e il file JSONL è append-only; `prompt_hash` viene calcolato ma non confrontato con artefatti precedenti. Un cambio di codice/config può mescolare risultati incompatibili. **Soluzione:** salvare hash di codice, config, manifest, baseline, esempi e rappresentazioni; in resume verificare gli hash e abortire su mismatch.

**T7 — IMPORTANTE — Retry semantics ambigua.** `range(1, max_retries+1)` con default 2 produce due tentativi totali, non “2 retry + originale” (`:442`). Il comportamento è coerente col nome ma non con una lettura comune di max_retries. **Soluzione:** rinominare `max_attempts` oppure usare `max_retries + 1`, con test unitario.

**T8 — IMPORTANTE — Structured output e parsing troppo permissivi.** `text=OUTPUT_SCHEMA` è plausibile per Responses API, ma il parser manuale (`response.output`, `hasattr`) non verifica output vuoto, `refusal`, schema, coerenza `abstain/predicted_label`, né `reasoning_summary`. **Soluzione:** bloccare la versione SDK, testare un response fixture/refusal/truncation e validare con JSON Schema prima di registrare il record.

**T9 — IMPORTANTE — Majority vote è plurality.** `Counter.most_common(1)` accetta 1/3 come “majority” e i pareggi dipendono dall’ordine (`:264-270`). La documentazione di Phase B usa invece almeno 2/3 e altrimenti abstain. **Soluzione:** richiedere `count >= ceil(R/2)`; altrimenti abstain, e separare plurality da majority nel report.

**T10 — IMPORTANTE — Test statistici.** Il bootstrap usa differenze replicate-level e un RNG condiviso sequenzialmente; l’ordine dei confronti cambia i CI. Il p-value è chiamato genericamente ma è una proporzione one-sided non calibrata come test two-sided. McNemar asintotico è inaffidabile con poche celle discordanti. **Soluzione:** bootstrap clusterizzato per caso, RNG derivato deterministicamente per confronto, p-value paired permutation/exact binomial, correzione per molteplicità e CI simultanei.

**T11 — SUGGERIMENTO — Dettagli numerici.** `ddof=1` è coerente solo se il baseline usa lo stesso stimatore: va verificato esplicitamente. Il slope è dimensionalmente coerente perché `t` è in ore sia nel fit sia nella predizione (`:177-192`), ma il nome `robust_slope` è improprio: è OLS, non robust regression. Le somme/eigh sono deterministiche sullo stesso ambiente, ma versioni BLAS diverse possono alterare gli ultimi bit; arrotondare prima del rendering e registrare ambiente/versioni.

**T12 — IMPORTANTE — SAX non usa il baseline.** Il codice fa Z-normalization locale per finestra (`:630-638`), non rispetto al baseline come suggerisce il design. Questo rimuove shift assoluti utili alla diagnosi e rende il braccio non confrontabile con quella descrizione. Il PAA con `round` produce segmenti quasi bilanciati; tuttavia va garantito `end <= n` e gestito esplicitamente `n < word_size`. **Soluzione:** decidere e documentare local-vs-baseline normalization, aggiungere test sui bordi e verificare lunghezza dei segmenti.

**T13 — CRITICO — Normal examples non sono temporalmente equivalenti.** Per N1/N2 il runner imposta `fault_injection_h=start` (`:183-189`), quindi N1 è 0–50 h e N2 50–100 h; gli held-out Normal hanno invece config globale `fault_injection_h=10` e analisi 10–50 h. Questo rende gli esempi Normal diversi dai casi Normal e contraddice il design “8 finestre 10–50”. **Soluzione:** estrarre N1/N2 come finestre 10–50 relative al blocco oppure usare un’origine temporale coerente e testare il numero di finestre per ogni esempio/caso.

**T14 — IMPORTANTE — Validazione input insufficiente.** `load_held_out_manifest` verifica solo 15 righe (`:159-165`), non label, file, monotonicità, intervallo, sampling costante, 41 XMEAS e assenza di overlap. **Soluzione:** riusare/integrare `verify_heldout_integrity.py` e fallire prima di generare gli esempi.

**T15 — SUGGERIMENTO — Global state.** Il prompt descrive un pattern `_init_imports`, ma questo snapshot importa direttamente `ARMS`; il problema è quindi attenuato, non eliminato: import assoluti e path globali restano fragili. **Soluzione:** usare package imports/config object espliciti e testare l’invocazione delle funzioni senza passaggi CLI.

## Checklist pre-esecuzione

- [ ] Correggere o separare il confound temporale CGTIME.
- [ ] Definire budget token/equivalenza di lunghezza e preflight sul prompt.
- [ ] Correggere Normal N1/N2 e verificare esattamente le finestre prodotte per ogni braccio.
- [ ] Aggiungere validazione finite/constant columns e JSON Schema dell’output.
- [ ] Decidere full covariance vs diagonale e descriverlo senza chiamarlo full Mahalanobis.
- [ ] Congelare codice, config, baseline, manifest, SDK/model snapshot e hash degli esempi.
- [ ] Correggere resume, retry, majority vote e tie handling.
- [ ] Pre-registrare endpoint primario, MDE, bootstrap clusterizzato, test esatto e correzione multipla.
- [ ] Eseguire dry-run con fixture sintetiche: costanti, NaN/Inf, serie corte, boundary PCA/PAA, refusal/output vuoto.
- [ ] Verificare le 180 righe attese, 3 rep per caso/arm, prompt hash coerenti e nessuna duplicazione.
- [ ] Motivare la selezione dei quattro fault e limitare le claim a questo campione.

## Verdict

**NO-GO.** Il codice compila, ma l’esperimento attuale confonde rappresentazione con granularità temporale e presenta rischi concreti di profili non validi, esempi Normal non allineati e resume non riproducibile. Dopo le correzioni L1–L3, T1–T2 e T13, più i controlli della checklist, il protocollo può diventare **GO con riserve**.

## Follow-up review delle modifiche dichiarate

Le modifiche risultano presenti nei quattro file e `py_compile` continua a passare. Tuttavia il primo dry-run reale è ancora bloccato:

**F16 — CRITICO — regressione in `load_baseline()`.** In `ablation_runner.py:303` il codice esegue `baseline._cov_inv_regularised = cov_inv`, ma `BaselineStats` in `code/tep_features.py:27` è dichiarato `@dataclass(frozen=True)`. Il comando:

```text
python ablation/ablation_runner.py --project-root . --dry-run ...
```

termina con `dataclasses.FrozenInstanceError` prima della generazione delle rappresentazioni. **Soluzione:** non mutare il dataclass frozen; passare `cov_inv` esplicitamente a `represent_cgtime_stats`/`generate_all_representations`, oppure introdurre un contesto immutabile dedicato (alternativamente, aggiungere il campo al dataclass e costruirlo al momento della creazione, senza bypassare `frozen=True`).

**F17 — IMPORTANTE — validazione output non verifica i tipi.** `_validate_output()` assume che il parsed output sia un dict e non verifica che `abstain` sia booleano o che `reasoning_summary` sia stringa. Un payload malformato potrebbe quindi passare parzialmente o causare un errore non classificato. **Soluzione:** validare il tipo dell’oggetto e ogni proprietà con JSON Schema; convertire ogni violazione in un’abstention registrata con errore strutturato.

**F18 — SUGGERIMENTO — documentazione interna incoerente.** L’header di `ablation_runner.py` continua a dire “max_retries renamed”, mentre il codice usa `max_attempts`; va aggiornato per evitare ambiguità futura.

### Stato aggiornato

Il verdict resta **NO-GO**, non per i finding L1/T1/T2/T13/T3–T14 originari — le correzioni sono effettivamente visibili — ma per F16, che impedisce l’esecuzione stessa. Dopo la correzione di F16, va rilanciato il dry-run completo e va controllato che produca 180 record e prompt hash/provenance coerenti.

## Verification v2

F16 è stato corretto passando `ref_cov_inv` esplicitamente attraverso tutta la catena, senza mutare `BaselineStats`.

Verifiche eseguite:

- `py_compile` dei tre moduli: **OK**
- dry-run completo: **OK**, 180/180 record simulati
- covariance Ledoit–Wolf 41×41: **OK**
- manifest: **OK**, 15 casi e 3 per classe
- token preflight: **OK**, massimo osservato CGTIME ~342k sotto il limite di 900k
- valutazione completa: **OK**, JSON e report Markdown prodotti

Il finding F16 è quindi **RISOLTO**. Il verdict operativo passa a **GO con riserve**, mantenendo le cautele statistiche su campione piccolo, lunghezze molto diverse tra bracci e interpretazione del baseline CGTime-inspired.
