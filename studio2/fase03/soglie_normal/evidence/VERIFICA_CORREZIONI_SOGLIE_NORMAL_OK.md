OK

# Riverifica indipendente delle correzioni — sotto-fase 03.5 «soglie Normal», incluso il completamento C4

**Esito tecnico del delta: OK.** Le quattro non conformità D1–D4 del verbale NON OK sul candidato `819b12e` risultano risolte sulle fonti primarie; nessuna regressione numerica, documentale o di test; nessun artefatto congelato toccato. L'OK è limitato al delta non committato descritto sotto e **non chiude la sotto-fase né la Fase 03** (vedi §10): restano una decisione dell'autore sul limite di tracciabilità (D3) e i passi del ciclo (commit, documentazione, verifica di fase).

## 1. Oggetto esatto della riverifica

| Elemento | Valore |
|---|---|
| Worktree del candidato | `/Users/luker/fot-tep-correzione-soglie-normal` (letto, non modificato) |
| Branch del candidato | `codex/studio2-soglie-normal-correzioni` — punta a `819b12e97fb94d501032655ec2f226139e6c5ca5` (nessun commit nuovo) |
| Commit di base | `819b12e97fb94d501032655ec2f226139e6c5ca5` (`studio2(fase03): aggiunge confronto FAR e nota di processo`, 2026-09-14 08:53:32 UTC) |
| Stato Git del candidato (11:20 UTC) | ` M studio2/PROVENIENZA.md`, ` M studio2/fase03/soglie_normal/REPORT_SOGLIE_NORMAL.md`, `??` i quattro file nuovi; **nessun altro file modificato, non tracciato o ignorato** |
| Copia principale `/Users/luker/fot-tep` | HEAD `819b12e`, branch `codex/studio2-soglie-normal`, invariati |

SHA-256 dei sei file candidati **non committati** (identici in candidato e snapshot):

| File | SHA-256 |
|---|---|
| `studio2/PROVENIENZA.md` | `d0b59649ad307d3bb15c9b07015c106da8addba69be111fd8258503582f37585` |
| `studio2/fase03/soglie_normal/REPORT_SOGLIE_NORMAL.md` | `5323438f8f2426f859537e12dee24139c3b8daa0b858b01934b4f7fc23308e32` |
| `studio2/fase03/soglie_normal/THRESHOLD_UNCERTAINTY_PROTOCOL.json` | `711d9711587fd140dcb451ccbe48b42d35fdf1bc3043feb5fb5e6dea3921989b` |
| `studio2/fase03/soglie_normal/complete_threshold_uncertainty.py` | `5fcbb2ede6f1fcea43e9c7fa6d6c9dc66a530ee9bafb8b2cc91658540ddffe57` |
| `studio2/fase03/soglie_normal/THRESHOLD_UNCERTAINTY.json` | `70dbca42391a0eea6ca39e12dc2f4e81d1cbe9a527494aca09388ae74f153feb` |
| `studio2/fase03/soglie_normal/tests/test_threshold_uncertainty.py` | `1fa8195d57dc090483db9d3c9c4391e4ec42365e579667d709d56f022be02f5a` |

Le impronte coincidono con `DELIVERY_SHA256.csv` del supporto della correzione e il diff tracciato attuale è byte-identico a `correction-tracked.diff` conservato lì (`973f9287…`).

**Snapshot riverificato.** Worktree detached su `819b12e` creato in **`/Users/luker/fot-tep/.worktrees/riverifica-soglie-normal`** — *non* nel percorso richiesto `/Users/luker/fot-tep-riverifica-soglie-normal`, che dalla sessione non è creabile (la home dell'utente non è raggiungibile; stessa deviazione già adottata per la verifica esterna 03.15). I sei file sono stati copiati preservando i percorsi; hash verificati coincidenti; `git status` dello snapshot mostra esattamente le due modifiche e i quattro file nuovi. `.worktrees/` è escluso da Git (`.git/info/exclude`); la registrazione del worktree nei metadati condivisi è l'unica modifica alla copia principale.

## 2. Modello, finestra, ambiente

- **Verificatore:** `claude-fable-5-1` (identificatore configurato della sessione; il modello effettivamente servito può differire e non è attestato crittograficamente). Sessione Claude `session_01NfcCmkTeXtdvJZcykoHddT`, Cowork, 2026-09-14 dalle 11:19 UTC.
- **Indipendenza:** le correzioni sono dichiarate prodotte da `gpt-6-astra`, finestra Codex `01a09f81-e508-77e0-b510-872bdeba46e3` (la stessa del verbale NON OK). Il presente verificatore è un modello diverso, di altro fornitore, in altra finestra; nessuna chiamata ad altri modelli. ⚠️ Non ho potuto leggere il rollout locale di quella finestra (accesso a `~/.codex/sessions/2026/09/14` non concesso in tempo): identità e ruolo di `gpt-6-astra` per la correzione restano **dichiarati** dal report/provenienza e dal mandato, coerenti con il verbale precedente, non verificati da me sul file.
- **Ambiente 1 (VM locale, Cowork su macbook-pro-local):** Linux 6.8.0 aarch64, Python 3.10.12, NumPy 2.2.6, SciPy 1.15.3 (installata nel profilo utente della VM), pytest 9.1.1, git 2.34.1. **Ambiente 2 (container cloud):** Linux 6.18 x86_64, Python 3.11.15, NumPy 2.4.4, SciPy 1.17.1. Il candidato aveva usato macOS 26.6.2 x86_64, Python 3.11.5, NumPy 2.4.6, SciPy 1.17.1 (venv del supporto di verifica precedente). Nessuna esecuzione MATLAB, nessuna simulazione TEP.
- **Letto prima di operare:** `docs/MAINTENANCE.md`, `docs/prompts/Prompt_LLM.md`, `docs/prompts/Verifica_LLM.md` (versione `819b12e`, identica nel candidato: tutti i 2244 file tracciati diversi dai due dichiarati sono byte-identici alla base); registro `DECISIONE_calibrazione_soglie_fase_B.md` rev. 19 (requisiti iniziali, P0, C2–C4, «Formulazione corretta della garanzia, e controllo sui pareggi»); specifica, handoff, freeze, FAR, audit, manifest e log della 03.5; verbale precedente; i due supporti; i sei file candidati per intero.
- **Supporto esterno di questa riverifica:** `/Users/luker/tmp/riverifica-soglie-normal-support-tsO8AV` (§11). Comandi essenziali in `commands.txt` del supporto.

**Verbale precedente preservato:** `/Users/luker/fot-tep-verifica-soglie-normal/studio2/fase03/soglie_normal/VERIFICA_SOGLIE_NORMAL.md`, SHA-256 `ccaec80994522ba5167fdf9ef6f3500d220c19f86977de53afdb2dee7be548bd` (riscontrato). Il suo verdetto NON OK su `819b12e` resta valido per quel commit: questo documento verifica la risoluzione dei suoi rilievi, non lo sostituisce.

**Supporti precedenti riusati con impronte verificate:** `verifica-soglie-normal-support-WE8Qqc/SUPPORT_SHA256.csv` (56/56 voci coincidenti, indice `c109c36e…` come dichiarato nel verbale); `correzione-soglie-normal-support-XKCNMN/DELIVERY_SHA256.csv` (16/16). Sono stati riusati, senza ripetere l'audit integrale dei 500 workbook, i risultati di riscaricamento (`archive_result.json`: 515/515, 0 mismatch, 150/150 sigilli, 516 file ordinari, 514 AppleDouble/PAX), di cronologia (`history_result.json`) e di tracce (`traces_result.json`), perché gli input (freeze `ff5c2700…`, score `a1c5991a…`, piano `fae355fd…`) sono identici nel candidato e verificati qui.

Legenda: ✅ riscontro sulla fonte primaria · ⚠️ limite od osservazione non bloccante · ❌ smentito/requisito non soddisfatto.

## 3. Controllo 1 — integrità del candidato

✅ Confronto contenuto per contenuto (`git hash-object` di tutti i file tracciati vs `git ls-tree 819b12e`): 2244/2244 file, **solo** `studio2/PROVENIENZA.md` e `REPORT_SOGLIE_NORMAL.md` differiscono; nessun file mancante; nessun file ignorato. Quindi dati (`CAL_THR_SCORES.csv` `a1c5991a…`, `FAR_VERIFICATION.json`), soglia e freeze (`THRESHOLD_FREEZE.json` `ff5c2700…`), piani (`fae355fd…`, `084dcabf…`), fit e moduli di Fase 02 (`score_fit_legacy.json` `e679caf4…`, `combined_score.py`, `tep_features.py`, `validate_numerics.py`, `PRECALIBRATION_FREEZE.json` `be01fe4c…`), specifica, handoff, `MANIFEST_CONSERVAZIONE.csv`, `ARTIFACT_STORAGE.json`, `LOT_AUDIT.json` e `R2_GUARD_RECHECK.json` coincidono con la base. Nessuna coppia MD/HTML toccata.

✅ Il diff di `PROVENIENZA.md` è un solo hunk (`@@ -268,8 +268,34 @@`): riformulazione del paragrafo sul batch anticipato (limite di segregazione, decisione dell'autore) e nuova §9.1 «Completamento C4». Nessun'altra riga toccata; U1/R2 non riceve nuovi ruoli (§9.1: «non riceve alcun nuovo ruolo e i suoi parametri non sono rifittati»; lo script non carica né rifitta la baseline).

✅ Il report è riscritto per intero (402 righe cambiate) ma dichiara che report e addendum originali restano recuperabili a `819b12e`; l'elenco «File del pacchetto originale 53a3e92 → 819b12e» coincide con `git diff --name-only` (37/37 percorsi); i sei file della revisione sono elencati uno per riga.

## 4. Controllo 2 — D1, interpretazione del FAR

✅ Ricalcolo esatto in aritmetica razionale (e con SciPy), `X ~ Binomiale(150, p)`:

| p | P(3 ≤ X ≤ 12) | P(4 ≤ X ≤ 12) | P(X = 7) |
|---|---:|---:|---:|
| 17/351 = 0,048433048… | **0,9470465066** | 0,9046433773 | 0,1518 |
| 0,0484 | **0,9471050102** | 0,9045720331 | 0,1518 |
| 0,05 | **0,9433302578** | 0,9067145037 | 0,1499 |

I tre valori del report corretto e di `THRESHOLD_UNCERTAINTY.json` coincidono cifra per cifra; il registro (P0: «con FAR vero 4.84% … 0.947 … 4–12 copre 0.9046», moda 7 con P = 0,152) è riprodotto per il suo parametro. Il report attribuisce ora esplicitamente lo 0,947 allo scenario 17/351 e qualifica come errata l'associazione al 5% dell'addendum precedente.

✅ Distinzioni presenti e corrette: α nominale 5%; 17/351 ≈ 4,8433% come media di Beta(17,334) fra calibrazioni ripetute (sotto le ipotesi); `q(T)` FAR ignoto della soglia realizzata per la miscela uniforme delle dieci posizioni; 11/150 e 108/1500 come due stime di `q(T)`. Dichiarato che lo scenario binomiale a p fissato non identifica `q(T)` con la media della Beta.

✅ Secondario: il report afferma che stima «il FAR della miscela uniforme delle dieci posizioni, la stessa quantità coperta dalla garanzia» — conforme a P0 («è la miscela uniforme delle dieci posizioni a coincidere con la distribuzione di calibrazione»); che la dipendenza intra-run riguarda l'incertezza e si tratta ricampionando interi run («Non sono giustificati 1500 trial binomiali indipendenti»); e che l'IC95% percentile **esclude 4,8433% e 5%**. Ricalcolo dai 1500 score di `FAR_VERIFICATION.json` (container): primario **11/150 = 7,3333%**, Clopper–Pearson 95% **[3,7175%; 12,7424%]** (include entrambi); secondario **108/1500 = 7,2%**, bootstrap per run seed 20260913 × 10.000, SE **0,7512512 pp** (ddof=1), percentile 95% **[5,7333%; 8,7333%]**; per posizione **14,10,12,6,14,8,11,13,10,10**. Tutto coincide con gli artefatti.

✅ Nessuna prova indebita: il report dice che la compatibilità del primario «non dimostra uguaglianza del FAR, continuità, IID o una verifica stretta della Beta», che i 150 run controllano solo l'ordine di grandezza (limite P0), e che la posizione 1 (14 superamenti, come la 5) «non prova burn-in sufficiente e non autorizza interpretazioni causali». Nessuna modifica di burn-in, finestre o soglia.

## 5. Controllo 3 — D2 / C4, nuovo calcolo

**Dai 350 score congelati (ricalcolo autonomo, `independent_check.py`, senza le funzioni del candidato):**

✅ 350 righe, `run_id` univoci, coincidenti con il piano (id, stream, J); ordine del CSV = ordine del piano; tutti finiti. **350 valori distinti** sia come stringhe sia come float; zero gruppi di duplicati; gap minimo fra score ordinati 1,04·10⁻⁴; **molteplicità alla soglia 1**. Il nuovo script rende conto di *tutti* i pareggi (non solo della soglia) e ometterebbe la Beta in loro presenza: colma il ⚠️ D2 del verbale precedente. Report e JSON dichiarano che l'assenza di pareggi «è diagnostica, non dimostrazione di continuità o IID» (`continuity_proven_by_no_ties: false`).

✅ Rango `ceil(351·0,95) = 334` (anche in aritmetica esatta); 334° valore ordinato **13,623626738268857**, scarto **zero** dal freeze; regola `S > threshold`; 333 sotto, 1 uguale, 16 sopra.

✅ **Beta(17, 334)** (a = n+1−k = 17, b = k = 334): media **17/351 = 4,843304843%**; varianza esatta 2839/21.683.376, SD **1,144245586 pp**; intervallo centrale 90% **[3,118163613%; 6,860631796%]** (ppf SciPy, ricontrollata con la beta incompleta regolarizzata: I = 0,05/0,95). Coincide con report e JSON. Il report la presenta come «distribuzione teorica del FAR, non IC empirico della soglia realizzata», condizionata a continuità di S, IID dei run e score fissato — conforme al registro C4 e alla «Formulazione corretta della garanzia».

**Protocollo e codice del bootstrap** — ✅ tutti i parametri richiesti sono nel protocollo e nel codice: 350 score ricampionati con rimpiazzo per replica (`rng.integers(0, 350, size=(10000, 350))`), rango fisso 334 (`np.partition(..., 333)`, statistica d'ordine, nessun quantile interpolato), 10.000 repliche, `numpy.random.Generator(PCG64(20260914))`, SE con `ddof=1`, percentili 2,5/97,5 con `method='linear'`, fit fisso (lo script non carica né tocca `score_fit_legacy.json`). Il codice verifica gli hash degli input prima e dopo il calcolo, rifiuta output esistenti, controlla n/rango/soglia/regola contro il freeze.

**Riesecuzione dello script** — ✅ in VM (aarch64, NumPy 2.2.6/SciPy 1.15.3) e nel container (x86_64, NumPy 2.4.4/SciPy 1.17.1), output esterni al repository: **tutti i valori coincidono** con `THRESHOLD_UNCERTAINTY.json` — media 13,474095477009715, SE 0,5821769414145996, percentili [12,263221096235686; 14,208737218829068], hash dei 10.000 valori bootstrap `81914f81…` identico, Beta e binomiali identici, pareggi identici, `script_sha256` e `protocol_sha256` identici agli hash dei file. Differenze **solo** in `created_at_utc`, `environment` e nelle ultime cifre (≤ 4·10⁻¹⁵ relativo) di media/SD della legge esatta e dello z Monte Carlo (ordine di somma BLAS), più 7·10⁻¹⁸ sull'estremo inferiore Beta nella VM (SciPy 1.15 vs 1.17). Motivate, non sostanziali.

**Controllo numerico autonomo (mio, sort completo invece di partition; legge esatta per somma esplicita in razionali):**

✅ Bootstrap: stessi media/SE/percentili/hash; SE con ddof=0 = 0,58214783 (per riferimento); i 10.000 valori assumono **31 valori distinti**, tutti nel campione.

✅ Legge `P(T* ≤ x_(j)) = P(Binom(350, j/350) ≥ 334)`: scarto massimo fra il mio calcolo e `binom.sf` del candidato 1,7·10⁻¹⁵; Σpmf = 1; media **13,4758081742**, SD **0,5831861336** (coincidenti); z della media MC **−0,2937**; distanza massima ECDF–CDF sul supporto **0,0037190700** (coincide; è anche il sup a due lati). Inversa generalizzata: 2,5% → x₍₃₂₅₎ = **12,2632210962** (CDF(x₍₃₂₄₎) = 0,02094 < 0,025 ≤ CDF(x₍₃₂₅₎) = 0,03282); 97,5% → x₍₃₄₁₎ = **14,4086543351** (CDF(x₍₃₄₀₎) = 0,974815 < 0,975 ≤ CDF(x₍₃₄₁₎) = 0,989865). Coincide con il JSON.

**Differenza 14,208737 (MC) vs 14,408654 (inversa esatta)** — valutata esplicitamente:

- ✅ Non è un bug. L'estremo MC è x₍₃₄₀₎; il target 0,975 cade nel gap di **0,000185** sopra CDF(x₍₃₄₀₎) = 0,974815, mentre la dispersione Monte Carlo dell'ECDF in quel punto è 0,00157 (SD del conteggio 15,7 su 10.000). Il conteggio osservato di repliche ≤ x₍₃₄₀₎ è **9763** (atteso 9748,1; z = +0,95); il metodo `linear` richiede ≥ 9751 per restituire esattamente x₍₃₄₀₎. Sotto la legge esatta, con questo seed-indipendente calcolo, P(estremo MC = x₍₃₄₀₎) = **0,444** e P(estremo ≥ verso x₍₃₄₁₎) = **0,530**: l'esito è di fatto una moneta fra due atomi adiacenti distanti 0,1999 in unità dello score.
- ✅ Non è irrilevante: entrambi gli intervalli sono legittimi ma con coperture esatte diverse — **[x₍₃₂₅₎, x₍₃₄₀₎] copre 95,387%**, **[x₍₃₂₅₎, x₍₃₄₁₎] copre 96,892%**; la coda superiore oltre 14,2087 vale esattamente **2,5185%**, oltre 14,4087 **1,0135%**.
- ⚠️ **Adeguatezza del report (non bloccante, osservazione N1):** la spiegazione «la distribuzione è discreta e l'estremo superiore percentile può saltare fra score adiacenti; il risultato delle 10.000 repliche non viene sostituito scegliendo un altro seed» è corretta e la rinuncia allo shopping del seme è appropriata, ma non quantifica il fenomeno: il lettore della tabella vede 14,2087 come «percentile 95%» senza sapere che P(T* ≤ 14,2087) = 0,97481 e che il quantile discreto è indeterminato fra i due atomi. Suggerimento all'autore: riportare accanto ai due estremi le probabilità di coda/copertura esatte, o adottare come riferimento C4 l'intervallo esatto (calcolabile senza Monte Carlo) lasciando il MC come controllo. Il report dice già, correttamente, che il confronto esatto «non è un intervallo di confidenza esatto per il quantile della popolazione».

✅ Nessun seed o protocollo alterato in questa riverifica per avvicinare valori; i valori riportati sono stati trattati come affermazioni e sono risultati tutti riprodotti.

**Distinzione temporale** — ✅ C4 («bootstrap sui run per la soglia stessa») è nel registro dal commit `1b947dd` del 2026-09-12 09:41 UTC, e il registro non cambia dopo `7799cd7` (2026-09-12 19:14 UTC), cioè prima della specifica 03.5 (13-09 16:16 UTC) e dei dati (13-09 16:38–17:42 UTC): il *requisito* precede i dati. I dettagli tecnici (seed 20260914, 10.000 repliche, convenzione percentile) sono in `THRESHOLD_UNCERTAINTY_PROTOCOL.json` con `recorded_at_utc` 11:04:41 (mtime coerente), script finalizzato alle 11:06:14, risultato alle 11:06:16; supporto XKCNMN con `uncertainty.log` identico al risultato e una riesecuzione alle 11:13. Report, protocollo e §9.1 dichiarano che sono scelte **post-hoc rispetto ai risultati** e che «non si rivendica una scelta cieca»: **nessuna falsa preregistrazione**. ⚠️ La sequenza protocollo → script → risultato è sostenuta da marche temporali e log della stessa finestra, non da una registrazione esterna: è un'auto-dichiarazione onesta, non una prova.

## 6. Controllo 4 — D3, processo

✅ Testo corretto vs fonti: l'**handoff** (`HANDOFF_BATCH.md` r. 13–15) prevede «i piani immutabili `plans/cal_thr.csv` e `plans/far_ver.csv` in un solo processo MATLAB» e (r. 25–27) «Prima di aprire qualsiasi finestra `far_ver` … congelare soglia, rango, numerosità, regola … Solo dopo si apre `far_ver`»; il **registro** («Dopo la calibrazione e prima della verifica si congelano…») non contiene un divieto di generare/conservare `far_ver` prima del freeze; la specifica separa gli usi senza aggiungerlo. Il report corretto e `PROVENIENZA.md` §9 affermano esattamente questo e qualificano come errata l'attribuzione del divieto all'handoff fatta dall'addendum a `819b12e`. Risolta la contraddizione interna «come previsto dall'handoff» / «non rispetta l'ordine … dell'handoff».

✅ Distinzioni presenti: generazione e conservazione (manifest locali originali in `runs/normal_001`: `cal_thr` 13-09 **16:38:19–17:19:15** UTC, `far_ver` **17:19:17–17:42:24**); lettura dei byte FAR per SHA-256 e dei metadati di manifest nell'audit (`audit_lot.py`: `load_case` solo nel ramo `cal_thr`; `far_ver_scores_present: False` è un valore scritto dal codice, non un controllo del sistema); score `cal_thr` (`0127ef4`, 18:27:47); freeze (`9507143`, `frozen_at_utc` 18:28:19.798); apertura analitica e score FAR (`0b2aac5`, 18:34:53; prima invocazione registrata di `analyze_far_ver.py` dopo il freeze, versione intermedia del conteggio secondario corretta prima del commit — da `traces_result.json` del supporto precedente). Log MATLAB originale: 500 warning «Variable Time Delay», 0 errori/trip, «Generated 350 runs» / «Generated 150 runs».

✅ Limiti probatori dichiarati correttamente: «Il sigillo prova identità, non mancata lettura»; log e assenza di derivati Git «non escludono letture umane o da processi non registrati, né file poi rimossi»; la generazione anticipata «non assolve né invalida automaticamente il FAR»; «La decisione scientifica dell'autore di accettare questo livello di tracciabilità rimane distinta dalla presente correzione documentale; non è considerata acquisita dalla richiesta di correggere il report». Stessa formulazione in `PROVENIENZA.md`. Nessuna assoluzione né invalidazione del FAR è stata dedotta, né qui né dal candidato.

## 7. Controllo 5 — D4, report e provenienza

✅ Formulazione pre-batch contestualizzata: «**Solo in quella finestra di correzione** batch, soglia e FAR erano ancora fuori perimetro: furono prodotti successivamente». Rimossa la frase al presente «non è stata eseguita alcuna simulazione».

✅ Errata 24.500/35.000 h: `SPECIFICA_SOGLIE_NORMAL.md` r. 53 dice ancora «35.000 h piene per `cal_thr`» (350 × 70 h = 24.500 h; 35.000 h = 500 run pieni); il report la registra come errata **senza riscrivere la specifica** (file byte-identico alla base) né il suo snapshot nella release. La proiezione 27.610 h (17.110 + 10.500) è corretta.

✅ Release e report archiviato distinti dalla revisione corrente: asset `studio2-fase03-normal-v1` immutato (943.793.152 byte, `bbcfd0c4…`, 515/515), report nell'asset `b22acf0f…` = snapshot pre-chiusura presente da `d09e7ed` a `0802c31` (`history_result.json`); il report corretto e §9.1 dichiarano che i nuovi file «non sono già inclusi nella release» e che la revisione «è ancora non committata».

✅ Modelli, finestre, ruoli, commit: tabella per passo (`gpt-5.6-luna`, `01a09b8c-…`, specifica/piani/analisi; batch MATLAB con comando fornito all'autore; `gpt-6-astra`, `01a09f81-…`, verifica NON OK e correzione nella stessa finestra, «non verifica indipendente di sé stessa»). L'identità luna per l'esecutore è sostenuta da `executor_evidence.json` del supporto WE8Qqc (rollout `3f21bd04…`, 13 `turn_context` con `gpt-5.6-luna`); la cronologia dei commit 8ec3c38 → 819b12e coincide con `git log` (orari UTC = locali − 2 h). ⚠️ L'identità `gpt-6-astra` della finestra di correzione non è stata verificata da me sul rollout (vedi §2). ✅ Provenienza del completamento C4 in §9.1: origini, commit, impronte (`a1c5991a…`, `ff5c2700…`, `711d9711…` coincidenti), destinazioni, ruolo, marca «C4 richiesto prima dei dati, dettagli operativi definiti dopo i risultati»; nessun nuovo ruolo alla baseline U1/R2.

⚠️ Osservazione N2 (non bloccante): il report elenca lo stesso file (`REPORT_SOGLIE_NORMAL.md`, `PROVENIENZA.md`) sia fra i «File della presente revisione» sia fra quelli del pacchetto originale; è coerente ma ridondante. Nessuna correzione richiesta.

## 8. Controllo 6 — test e regressioni

✅ `pytest -p no:cacheprovider studio2/fase03/soglie_normal/tests -v` sullo snapshot: **8 passed** (2 `test_generation_plan`, 2 `test_r2_guard_recheck`, 4 `test_threshold_uncertainty`) — i 4 nuovi sono i 4 dichiarati (legge esatta vs enumerazione con pareggi, statistica d'ordine non interpolata, rifiuto input non validi, rifiuto impronta alterata). Nessun `__pycache__` lasciato nel worktree.

✅ `test_generation_plan_stdlib.py`: `PASS standard-library plan tests`.

✅ `python3 docs/test_explanation.py`: snapshot **35 test, 14 failure, 1 skip**; base `819b12e` estratta pulita con `git archive` nel supporto: **35 test, 14 failure, 1 skip**. Confronto delle **identità** dei fallimenti con parametri dei subtest: **identiche** (14/14) fra base e candidato e identiche all'elenco `docs_failures_identical` di `validation-summary.json` del candidato (differisce solo la forma del nome del metodo stampata da unittest in Python 3.10 vs 3.11). Skip: «legacy part-1 walkthrough is not present in this checkout». **Nessuna regressione.** Come avverte il contratto, questo test copre documenti storici e non convalida C4.

## 9. Matrice D1–D4

| Rilievo del verbale NON OK | Stato | Motivazione |
|---|---|---|
| **D1** — 0,947 attribuito al 5%; mancate distinzioni α / 17/351 / q(T) / stime; esclusione di 4,8433% non dichiarata; miscela e dipendenza intra-run | **Risolto** | Tre probabilità ricalcolate esatte e coincidenti; parametro corretto (17/351); quattro quantità distinte; esclusione di 4,8433% e 5% dichiarata; secondario descritto come stima della miscela con bootstrap per run; nessuna prova indebita (§4). |
| **D2** — pareggi rendicontati solo alla soglia; C4 non soddisfatto (mancavano Beta qualificata e bootstrap della soglia) | **Risolto** | Diagnostica di tutti i pareggi (350 distinti, molteplicità 1); Beta(17,334) media/SD/IC90 esatti e presentata come legge fra calibrazioni sotto ipotesi; bootstrap della soglia sui 350 run con protocollo completo, riprodotto in due ambienti e controllato con legge esatta (§5). Resta l'osservazione N1 sulla presentazione dell'estremo superiore, non bloccante. |
| **D3** — nota di processo in contrasto con handoff/registro; «nessuno li ha letti» non dimostrabile | **Risolto come rendicontazione** | Testo allineato a handoff r. 13–27 e registro; distinzione generazione / hash-metadati / apertura analitica / score; limiti del sigillo e delle tracce dichiarati; decisione dell'autore esplicitamente non presunta (§6). L'accettazione scientifica del limite **resta dell'autore**. |
| **D4** — frasi pre-batch al presente; errata 35.000 h; report archiviato ≠ candidato; modello/profilo e chiusura mancanti | **Risolto** | Storicizzazione, errata senza riscrittura della specifica, snapshot di release distinto, tabella modelli/finestre/ruoli, file uno per riga, stato di commit dichiarato (§7). ⚠️ Identità del modello correttore non verificata da me sul rollout. |

## 10. Difetti nuovi, limiti probatori, decisioni dell'autore, perimetro dell'OK

**Difetti nuovi bloccanti:** nessuno. **Regressioni:** nessuna (artefatti, freeze, fit, piani, specifica e manifest byte-identici alla base; test invariati).

**Osservazioni non bloccanti:** N1 estremo superiore MC vs esatto sotto-quantificato (§5); N2 ridondanza degli elenchi file (§7); N3 il report registra come ambiente della correzione un venv creato dalla verifica precedente (accoppiamento innocuo, ma da non riusare per la prossima verifica indipendente); N4 la ricostruzione integrale del report rende il diff difficile da leggere — l'originale resta in Git, quindi è accettabile.

**Limiti probatori di questa riverifica:** identità del modello della finestra di correzione dichiarata, non letta sul rollout; sequenza protocollo → risultato attestata da marche temporali della stessa finestra; audit dei 500 workbook, riscaricamento dell'asset e tracce pre-freeze **riusati** dal supporto WE8Qqc con indice verificato, non ripetuti (input identici); nessun accesso a MATLAB.

**Decisioni ancora dell'autore:** (a) accettare o meno il livello di tracciabilità del FAR (generazione fisica di `far_ver` prima del freeze), e come riportarlo nel paper; (b) scelta della presentazione dell'incertezza della soglia (intervallo MC, esatto, o entrambi con coperture — N1); (c) commit della revisione correttiva (`studio2(fase03): completa C4 e corregge il report soglie Normal`, proposto dal candidato) e ordine del ciclo `Documentazione_LLM` → `Commit_LLM`.

**Esito tecnico del delta vs chiusura della fase.** L'OK certifica che il delta non committato su base `819b12e` risolve D1–D4, che i numeri nuovi sono riproducibili e che nulla di congelato è cambiato. **Non** certifica: la chiusura della sotto-fase 03.5 (che richiede la decisione (a), il commit e la sezione di walkthrough dopo l'OK), la validità delle ipotesi della Beta (continuità/IID: dichiarate, non dimostrate), l'esattezza del FAR realizzato, né la chiusura della Fase 03 (report e verifica *di fase* in `origin/main`, MAINTENANCE §8.6).

## 11. Supporto esterno, manifest, preservazione

Directory: **`/Users/luker/tmp/riverifica-soglie-normal-support-tsO8AV`** (la home non è raggiungibile dalla sessione; `/Users/luker/tmp` è stato usato come sede esterna al repository, dichiarandolo). Contenuto: `commands.txt`, `environment.txt`, `independent_check.py`, `mc_vs_exact_and_far.py`, `out/` (riesecuzioni VM e container dello script candidato, controlli autonomi VM e container, MC vs esatto, ricalcolo FAR), `logs/` (pytest, stdlib, riesecuzioni, `docs-candidate.log`, `docs-base.log` e le identità dei fallimenti), `base-819b12e/` (estrazione pulita della base, non indicizzata).

Indice **`SUPPORT_SHA256.csv`**, **21 voci**, SHA-256 **`f2022f9d10852332971df94e755e1310e56a9b39bfdf97fe8591c99abc2c29cc`**. Impronte principali: `independent_check.py` `e207ed628a5f1fd0…`, `mc_vs_exact_and_far.py` `805a0934010cc09c…`, `out/independent_check_vm.json` `b1d0c34e718b4962…`, `out/independent_check_container.json` `1ca5ac2dfefc30aa…`, `out/THRESHOLD_UNCERTAINTY_rerun_vm.json` `bf92736e127db45e…`, `out/THRESHOLD_UNCERTAINTY_rerun_container.json` `1b21b49ae4df7500…`, `out/mc_vs_exact_container.json` `44c64fe1746434bc…`, `out/far_recheck_container.json` `828f9543c08ad574…`. L'impronta di questo verbale è registrata a parte in `VERBALE_SHA256.txt` del supporto (fuori dall'indice, per evitare circolarità).

**Preservazione.** Unico nuovo documento nel worktree di riverifica: questo `VERIFICA_CORREZIONI_SOGLIE_NORMAL.md`. Non modificati: i sei file candidati, il worktree del candidato e il suo branch, la copia principale e il suo branch, il worktree e il verbale della verifica precedente, i due supporti precedenti, dati, score, soglia, freeze, piani, fit, specifica, manifest, release. Nessun commit, push, merge, tag, pubblicazione o aggiornamento del walkthrough; nessuna simulazione, calibrazione o chiamata ad altri modelli. Igiene: un `index.lock` vuoto creato da un mio `git status --ignored` nei metadati del worktree candidato è stato rimosso (11:21 UTC); il worktree di riverifica è registrato in `.git/worktrees/riverifica-soglie-normal` della copia principale con percorsi macOS ripristinati a fine sessione. Nella VM locale è stata installata SciPy/pytest nel profilo utente della sessione, non nel repository.
