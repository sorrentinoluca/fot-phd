OK — il lavoro della sotto-fase 03.6 regge: nessun file congelato toccato, guardia d'impronta reale e testata, conteggi/manifest/release riscaricata e verificata file per file, firme 697-D corrette e ricostruibili, leakage PASS verificato in negativo e in positivo, nessuna analisi vietata; un solo limite reale ma non invalidante su determinismo cross-ambiente (vedi §5).

# Verifica indipendente — sotto-fase 03.6 (evidence 697-D e verbalizzazioni)

Modello: Claude Sonnet 5 (diverso dal modello che ha eseguito la sotto-fase, dichiarato
in REPORT_EVIDENCE.md §3 come OpenAI Codex/GPT-5). Finestra: nuova, dedicata alla sola
verifica, nessuna esecuzione precedente su questo lavoro. Data: 2026-09-13T21:34Z.

Oggetto: branch `codex/studio2-evidence`, commit `cf1f70f` → `2f6dd8d`, base `d815ce9`.
Lettura tramite worktree dedicato in sola lettura (`.worktrees/verifica_evidence`,
checkout distaccato a `2f6dd8d`); nessun checkout nella copia principale. Runtime di
verifica: Python 3.10, NumPy 2.2.6, pandas 2.3.3, openpyxl 3.1.5 (diverso da quello
dichiarato nel report — vedi punto 5).

---

## 1. Perimetro

✅ `git diff --name-status d815ce9 2f6dd8d` mostra **solo**:
`studio2/PROVENIENZA.md` (modifica) e undici file nuovi sotto `studio2/fase03/evidence/`
(`.gitignore`, `ARTIFACT_STORAGE.json`, `DIPENDENZE_EVIDENCE.md`,
`MANIFEST_CONSERVAZIONE.csv`, `OUTPUT_CHECK.json`, `REPORT_EVIDENCE.md`, `__init__.py`,
`extract_evidence.py`, `leakage.py`, `test_evidence.py`, `verify_output.py`). Nessun file
di `protocol.py`, `run_pilot.py`, `prepare_gate.py`, `schemas/`, `phase_b/`, `code/` è
stato toccato. Il diff di `PROVENIENZA.md` è **solo aggiunta** (nuova §9 in coda, nessuna
riga preesistente modificata o rimossa). L'output (61.208.618 byte, 1.283 file) non è in
Git: `studio2/fase03/evidence/.gitignore` esclude `output/` e `git ls-files` sulla
cartella non elenca alcun file al suo interno; l'output è nella release pubblica
`studio2-fase03-evidence-v1` (verificato al punto 4).

## 2. Regola §8.2 «Codice del primo studio»

✅ Le quattro funzioni/moduli importati (`code/tep_features.py`,
`code/tep_verbalize_v2.py`, `code/verbalizer_config_v2.json`,
`code/evaluate_verbalizer_v2.py`) sono elencati con commit e impronta in
`DIPENDENZE_EVIDENCE.md` §1 e in `PROVENIENZA.md` §9. Ho ricalcolato io stesso lo
SHA-256 dei quattro file nel worktree e confrontato con
`phase_b/PHASE_B_PROTOCOL_HASHES.json`: **coincidono esattamente** con i valori
dichiarati e con quelli nel manifest congelato. Nel codice, `verify_frozen_sources()`
(righe 78–98 di `extract_evidence.py`) calcola l'hash **prima** di `sys.path.insert` e
di qualunque `importlib.import_module` (`load_frozen_api`, righe 101–103), e solleva
`RuntimeError` su mismatch. Ho eseguito il test `test_hash_guard_rejects_altered_source`
(altera un byte di `tep_features.py` in una copia temporanea): **fallisce come atteso**
(`ok` nell'esecuzione, vedi punto 8). `ONSET_H=25.0`, `END_H=65.0`, `WINDOW_H=5.0` sono
costanti di modulo passate esplicitamente come `start_h`/`end_h`/`window_h` a
`analyze_case_windows` (righe 283–288); ho verificato che nessun file di
`studio2/fase03/evidence/*.py` referenzia mai `10.0` o `fault_injection_h` — la funzione
`verbalize_case()` che userebbe il default legacy `fault_injection_h=10` (Fase A,
`code/verbalizer_config_v2.json`) **non è mai chiamata**: l'estrattore chiama invece
`verbalize_feature_table(unit, config)` su feature già calcolate con l'onset esplicito
a 25 h.

## 3. U3 in PROVENIENZA e recheck R2

✅ La riga U3 in `PROVENIENZA.md` §9 cita origine, commit (`309b944f…`) e impronta
(`79883dd0…`) **identici** a U1 (§4, riga `U1 / R2`); ho ricalcolato io lo SHA-256 di
`code/tep_cache/mode1_normal_500.xlsx` sul disco: coincide byte per byte. Destinazione
(normalizzazione + flag del verbalizzatore), marca **pre-specificato** e condizione di
validità legata a R2 sono dichiarate; l'autorizzazione è citata esplicitamente come
«Decisione dell'autore del 2026-09-13»; nessuna riga esistente di PROVENIENZA è stata
alterata (il diff è solo aggiunta, vedi punto 1), quindi nessun dato viene promosso a un
ruolo diverso da quello già autorizzato. La sezione «se R2 decade» esiste in
`REPORT_EVIDENCE.md` §5: invalidazione e rigenerazione obbligatoria, nessuna
sostituzione automatica della baseline.

Ho letto `R2_GUARD_RECHECK.json` al commit `d09e7ed189b4a068f6c094a34c6ad60937d13eb7`
(branch `codex/studio2-soglie-normal`, `git show`): `guard_pass: true`,
`parameters_and_code_current: true`,
`r2_guard_result_independent_byte_identical: true`; SHA-256 del blob ricalcolato da me
è `7df0cef2d7854c689b79eb911fa01d1ede1625e22f0d3636c0ea5d678c9f33f8` — **64 caratteri**,
identico a quello citato in `PROVENIENZA.md`, `DIPENDENZE_EVIDENCE.md` e
`ARTIFACT_STORAGE.json`. Ho verificato che alla punta attuale del branch
`codex/studio2-soglie-normal` il file ha ancora lo stesso hash: la condizione non è
decaduta.

## 4. Conteggi e release esterna

✅ Verificato sugli artefatti, non sul report. `MANIFEST_CONSERVAZIONE.csv`: 1.284 righe
incluso header → 1.283 righe dati; somma della colonna `bytes` = **61.208.618**,
identica al totale dichiarato. Suddivisione per suffisso: 320 × `.features.csv` + 320 ×
`.evidence.json` + 320 × `.signature.csv` + 320 × `.txt` = 1.280 file unitari (320 id
unici) + 3 file di controllo (`EVALUATOR_INDEX.csv`, `EVIDENCE_MANIFEST.csv`,
`EXTRACTION_SUMMARY.json`) = **1.283**. `EVALUATOR_INDEX.csv`: 320 righe, 8 fault × 40
run ciascuno (F1, F2, F3, F8, F10, F13, F14, F15 = i 40 run × 8 fault del piano D1).
`EXTRACTION_SUMMARY.json`: `run_count=40`, `windows_per_run=8`, `onset_h=25.0`,
`end_h=65.0`, `window_h=5.0`, `evidence_unit_count=320`, `signature_dimension=697` — tutti
coerenti.

Ho **scaricato io stesso** l'asset dalla release pubblica (non mi sono fidato della sola
autocertificazione in `ARTIFACT_STORAGE.json`), in una directory temporanea fuori dal
repository (`/tmp/verifica_evidence_dl`):
`https://github.com/sorrentinoluca/fot-tep-data/releases/download/studio2-fase03-evidence-v1/studio2-fase03-evidence-v1.tar`
→ 64.817.152 byte, SHA-256 `3e1eb87f38ff3fc6dd3346476785d06c2b98944b209f7f58706b3c71c1676999`
— **coincide** col valore dichiarato. Ho estratto l'archivio e confrontato **tutti e
1.283 i file** (non un campione) del manifest per percorso, byte e SHA-256 con lo script
`extract_evidence.py`/`MANIFEST_CONSERVAZIONE.csv`: **0 mismatch, 0 mancanti**, byte
totali verificati 61.208.618. Ho anche verificato a campione la provenienza dell'input:
lo `source_sha256` di `EVD-0001` in `EVALUATOR_INDEX.csv`
(`acb4c4ec62c267f089c7fab2799e18d26cf39f657b78dbef28246ff347f5c62c`) coincide con lo
SHA-256 reale di `studio2/fase03/fault_runs/runs/fault_dev_001/fault-dev-F1-b01.csv` nel
repository.

⚠️ Osservazione minore, non bloccante: l'archivio `.tar` contiene, oltre ai 1.283 file
del manifest, **1.285 file aggiuntivi** `._*` (metadati AppleDouble di macOS, prodotti
dal comando `tar` su quel sistema), non elencati in `MANIFEST_CONSERVAZIONE.csv` né in
`EVIDENCE_MANIFEST.csv`. Non contengono testo consumer-facing (sono binari di risorsa
macOS) e non incidono su conteggi, hash o contenuto dei file reali, ma un rilettore
ingenuo che facesse `glob("*.json")`/`glob("*.txt")` sull'archivio estratto senza
filtrarli otterrebbe un `UnicodeDecodeError` (mi è successo nello scanner di leakage,
punto 6, prima di escluderli esplicitamente). Suggerisco di ripackare l'archivio con
`COPYFILE_DISABLE=1 tar …` o `--exclude='._*'` alla prossima pubblicazione, per igiene,
non per correttezza scientifica.

## 5. Firme 697-D

✅ Aperte le 8 firme, una per fault (`EVD-0001`=F1, `EVD-0041`=F10, `EVD-0081`=F13,
`EVD-0121`=F14, `EVD-0161`=F15, `EVD-0201`=F2, `EVD-0241`=F3, `EVD-0281`=F8): tutte
esattamente 697 componenti, tutti i valori in `[0,1]`. La costruzione in
`signature_vector()` (`code/evaluate_verbalizer_v2.py`) itera le 41 `XMEAS` nell'ordine
fisso e per ciascuna appende 17 descrittori (livello, trend, residuo, diff, rapida
variabilità) → 41×17=697, e solleva `ValueError` se un valore esce da `[0,1]`: il
controllo è quindi strutturale, non solo osservato.

✅ Ho ricalcolato 3 firme (`EVD-0001`, `EVD-0121`, `EVD-0160`) importando
`signature_vector` dal commit e impronta dichiarati (stesso codice verificato al punto
2) e applicandola al JSON **pubblicato** (scaricato dalla release, non al mio ricalcolo):
il risultato è **identico byte per byte** (uguaglianza float esatta, non solo entro
tolleranza) al `signature.csv` pubblicato, per tutte e tre.

⚠️ **Determinismo cross-ambiente — limite reale, non invalidante.** Ho rieseguito
l'estrazione **completa** (le 40 run, non solo 2) in una directory temporanea, con lo
stesso `extract_evidence.py`, lo stesso `MANIFEST_FAULT_DEV.csv`, la stessa baseline
XLSX (hash verificato) e lo stesso `R2_GUARD_RECHECK.json` (16–20 secondi, come
dichiarato nel report). Risultato:

- `EVALUATOR_INDEX.csv` e tutti i 320 `.txt` e tutti i 320 `.signature.csv`: **identici
  byte per byte** alla release pubblicata;
- tutti i 320 `.features.csv` e tutti i 320 `.evidence.json`: **non identici** — la
  differenza è puramente di precisione in virgola mobile (massimo scarto assoluto
  osservato ≈4,5×10⁻¹³, scarto relativo massimo ≈1,5×10⁻¹³ su 287 celle confrontate
  su `EVD-0001`), non uno scostamento sistematico o di scala.

Ho isolato la causa: il mio ambiente ha NumPy 2.2.6 (dichiarato nel report: NumPy
2.3.5); una diversa versione di NumPy può cambiare l'ordine interno di somma/riduzione
e produrre queste differenze all'ultima cifra. Ho verificato che **non è un problema di
non-determinismo dello script**: ho rieseguito l'estrazione completa una seconda volta
nel mio stesso ambiente e confrontato con la prima mia esecuzione — **0 mismatch su
1.283 file**, quindi lo script è deterministico entro un ambiente fissato, com'è
verificato anche dal test sintetico `test_synthetic_end_to_end_dimension_and_determinism`
(due esecuzioni, stesso ambiente, byte-identiche — rieseguito da me, vedi punto 8).

Conclusione del punto: la firma 697-D e il testo neutrale — gli unici artefatti
consumer-facing e gli unici su cui si baseranno le fasi successive — sono riprodotti
esattamente anche cambiando ambiente/versione di libreria; i soli file che differiscono
(feature grezze e JSON strutturato) lo fanno per rumore di virgola mobile ininfluente su
qualunque soglia o decisione. Non degrado il verdetto a ❌ perché non c'è nessuna
evidenza di un bug (i valori non promuovono la soglia con score/rischio),
ma segnalo che `MANIFEST_CONSERVAZIONE.csv`/`EVIDENCE_MANIFEST.csv` non sono
riproducibili bit-per-bit su un ambiente NumPy diverso da quello dichiarato: se in
futuro serve rigenerazione bit-esatta dell'archivio, va fissata la versione esatta delle
librerie (o va introdotta una verifica per tolleranza sui soli file numerici grezzi).

## 6. Scanner anti-leakage

✅ Riletto `leakage.py`: le regex coprono esattamente gli 8 fault D1
(F1/F2/F3/F8/F10/F13/F14/F15), `IDV(n)` per lo stesso insieme, i nomi dei meccanismi
elencati nel prompt (`sticking valve`, `slow drift`, `random variation`, nomi dei
sensori/attuatori coinvolti) e le parole «continuità/nuovo». Test positivo eseguito da
me: `scan_text("Diagnosi F14 su IDV(3)")`, `scan_text("meccanismo sticking valve")` e
`scan_text("il segnale mostra continuità")` vengono **tutti rilevati** (non rifiutati
silenziosamente). Ho eseguito lo scanner su tutti i 320 testi e tutti i 320 JSON
pubblicati (esclusi i 1.285 file `._*` di metadati macOS del punto 4, che non sono testo
UTF-8 valido e non sono nel manifest): **0 rilevazioni**, coerente con `"leakage": "PASS"`
in `OUTPUT_CHECK.json` e con `EXTRACTION_SUMMARY.json`. L'indice
`EVALUATOR_INDEX.csv` (fault, batch/`stream_id`, run_id) è un file separato da
`units/*.txt` e `units/*.evidence.json`; la scansione confermando zero hit sui soli
file consumer-facing dimostra che l'indice non è duplicato al loro interno.

## 7. Nessuna decisione anticipata o analisi vietata

✅ Le uniche occorrenze di «separabilità/accuracy/rilevabilità» nel perimetro toccato
sono le frasi dichiarative di esclusione in `DIPENDENZE_EVIDENCE.md` §4 e
`REPORT_EVIDENCE.md` §4 («escluse per disegno»); nessun calcolo di separabilità,
accuratezza, margine o intensità del segnale è presente in codice o output (controllato
anche su `EXTRACTION_SUMMARY.json` ed `EVALUATOR_INDEX.csv`). Le quattro soglie di
`verbalizer_config_v2.json` sono lette dal file congelato e mai ricalcolate (nessuna
chiamata di calibrazione nello script). Nessuna scelta che appartenga a 03.7 o 03.12 è
presa: l'indice fault/batch resta evaluator-side e la sotto-fase non seleziona finestre
in base al contenuto.

## 8. Test

✅ Ho rieseguito io stesso, nel worktree di verifica:

- i 4 test di `test_evidence.py`
  (`test_synthetic_end_to_end_dimension_and_determinism`,
  `test_hash_guard_rejects_altered_source`, `test_r2_guard_rejects_noncanonical_file`,
  `test_leakage_detects_fault_id_mechanism_and_origin`): **`Ran 4 tests — OK`**, nessun
  fallimento;
- `python3 docs/test_explanation.py`: **`Ran 35 tests` → `FAILED (failures=14,
  skipped=1)`**, identico al numero atteso dichiarato nel prompt di verifica. Ho
  controllato l'elenco dei 14 fallimenti: riguardano tutti `UnifiedConversationChecks`
  su `step27_qwen_*`, `condition_c_contract_and_caveats` e
  `one_flow_and_ordered_step_headings` — pre-esistenti e non correlati a
  `studio2/fase03/evidence/` (nessun test relativo a questa sotto-fase è tra i
  fallimenti).

Il report segue i 7 punti di `Fase_LLM.md` (riassunto/risultati, file toccati, modello e
profilo, cosa è rimasto fuori, decisioni ancora necessarie, test_explanation.py
confrontato, commit con messaggio proposto): struttura confermata su
`REPORT_EVIDENCE.md` §§1–7.

---

## Conclusione

**OK.** Nessun file congelato toccato; guardia d'impronta reale e testata; parametri
temporali passati esplicitamente e nessun uso del default legacy `fault_injection_h=10`;
U3 tracciata correttamente e condizionata a un recheck R2 verificato PASS con impronta a
64 caratteri; conteggi, manifest e release esterna verificati file per file (1.283/1.283,
zero mismatch, riscaricata da me indipendentemente); firme 697-D dimensionalmente e
numericamente corrette e ricostruibili dal JSON pubblicato; scanner anti-leakage
verificato positivamente e negativamente su tutto il lotto; nessuna analisi vietata;
suite di test riprodotta con l'esito atteso. L'unico limite reale — differenze di
virgola mobile tra ambienti diversi nei soli file grezzi (feature/JSON, non
testo/firma) — è documentato al punto 5 e non richiede di rifare l'estrazione, ma
andrebbe considerato se in futuro si vuole una rigenerazione bit-esatta dell'archivio.

Si può procedere alla verifica di coerenza fra sotto-fasi in chiusura di Fase 03 e, dopo
quella, alla documentazione nel walkthrough (§N.6), che deve riportare esplicitamente
che la fase non è chiusa.
