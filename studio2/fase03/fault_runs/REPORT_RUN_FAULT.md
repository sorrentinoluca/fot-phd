# Sotto-fase 3 della Fase 03 — preparazione dei run fault di sviluppo

**Consegna preparatoria completata**, 2026-09-13. Non è la chiusura della macro-Fase 03.
Specifica pre-esecuzione, piano, script, test e **un solo smoke** sono su disco.
**Il batch 8 × 5 = 40 run non è stato eseguito.** Nessuna chiamata a modelli linguistici,
nessun subagente, push, tag, merge o modifica degli artefatti della Fase 02.
Base `main=origin/main=9ec87791dd79b82893dc09568bd8c47fdd154c50`, branch
`codex/studio2-fault-runs`. La verifica indipendente resta da svolgere in un'altra finestra.

## 1. Specifica decisionale, completata prima dei dati

Catalogo al tag D1: F1/F2/F3/F8/F10/F13/F14/F15. L'autore ha approvato:

- un solo IDV per run, nessuna perturbazione aggiuntiva o variazione di setpoint;
- burn-in qualificato 20 h, controllo interno [20,25) escluso da insight/prototipi;
- onset nominale 25 h, 40 h post-fault, termine 65 h, otto finestre [25,30) … [60,65);
- F14/F15 con banda di sticking di 2 punti percentuali, riscontrata nel sorgente;
- deviazione esplicita dalla raccomandazione Downs & Vogel, pp. 250–251: un segnale debole
  o assente resta un esito, senza aggiunte, estensioni o sostituzioni post-hoc;
- trip registrati con tempo fisico e prefisso, mai sostituiti in silenzio.

Le due scelte scientifiche erano state sottoposte all'autore perché le fonti non le
risolvevano autonomamente. Sono nella [specifica](SPECIFICA_RUN_FAULT.md), inclusa la
sezione «Limiti da dichiarare nel paper». La convenzione storica 40 h/otto finestre è
verificata sul codice e registrata nella provenienza; i dati storici non sono riusati.
L'esposizione incidentale alla tabella narrativa per-fault della v2 e agli estratti
narrativi apparsi nelle letture/test è dichiarata: nessun valore ha alimentato le scelte.

## 2. Piano e script implementativi

Riservati **30000–30039** ai run di sviluppo e **30040** allo smoke. Indici uint64,
stream uguale all'indice, coppia seed chiave/stream e parole low/high esplicite. Tutti
sono disgiunti dagli indici usati o prenotati in Fase 02 (incluso 999999).
Le prenotazioni future devono rispettare anche questo intervallo.

Il generatore di piani rifiuta ogni alterazione di righe, ordine, durata o identità.
Il launcher MATLAB limita le destinazioni a campagne nuove sotto runs/ o smoke/,
impedisce sovrascritture e retry impliciti, conserva log ed eventi timestampati e produce
manifest per tentativo. I trip continuano il piano fisso; gli errori tecnici fermano il
lotto e gli indici successivi sono esplicitamente not_run. Un crash del processo resta
rilevabile come consegna incompleta, non viene mascherato da un manifest di successo.

Il MEX gemello aggiunge esclusivamente diagnostiche di IDV, variabili interne e trip.
La rimozione delle aggiunte ricostruisce esattamente il sorgente qualificato; equazioni e
RNG non sono stati modificati. Il MEX base e i file Fase 02 restano invariati.
Il grezzo CSV conserva double a 17 cifre, tempo + 41 XMEAS + 12 XMV. Diagnostiche interne
separate, escluse dai prompt. Gli hash sono ricalcolati in un audit in sola lettura.

Il comando esatto di avvio background da MATLAB, con nohup nativo ARM, è in
[HANDOFF_BATCH.md](HANDOFF_BATCH.md). Il launcher del batch **non è stato eseguito**.

## 3. Test e verifiche implementative

**21 test passati**, più compilazione C/MEX e preflight MATLAB senza simulazione.
Copertura: catalogo e 40 righe; collisioni con manifest e prenotazioni Fase 02; piani
alterati/duplicati/troncati; seed; destinazioni; ricostruzione del sorgente; parser
malformati, IDV anticipati/errati, eventi incompleti; manifest e invarianti; hash alterati;
trip sintetici, arresti senza trip, contatori mancanti, finestre e not_run.

Il test documentale `python3 docs/test_explanation.py` mantiene **35 test, 14 fallimenti,
1 skipped**, con gli stessi 14 nomi del baseline. L'output è stato filtrato dopo la prima
invocazione per evitare di riaprire estratti storici nei messaggi di assert. Questo test
non copre §14, v2 o il nuovo harness; non costituisce la loro validazione.
Nessuna coppia Markdown/HTML è stata modificata. Link relativi e controllo whitespace di codice/documenti: PASS. Il controllo completo
segnala sei spazi finali nei due log MATLAB originali: conservati senza normalizzazione
per rispettare l’immutabilità degli output; non sono errori del codice.
Le prove e i comandi sono in `tests/`, `BASELINE_CHECK.json` e `FINAL_CHECK.json`.

## 4. Smoke unico

**F1, stream 30040: PASS**, un solo run fino a 25.1 h, 1507 × 54 valori nel grezzo.
Nessun trip o errore, 300 campioni di controllo e zero finestre post-fault complete.
Il segnale IDV e la variazione interna A −3 / C +3 punti percentuali, B costante, sono
registrati. Nessuna analisi di separabilità o risultati F14/F15 è stata eseguita.

Onset osservato **25.000410376861183 h**, scarto **1.47736 s** dal nominale, prima riga
campionata attiva a 25.0166666667 h. Il parser già committato prima del run distingue il
campione di frontiera dalla prima osservazione attiva. Tutti i campioni sono conservati:
non si modifica retroattivamente il piano, non si trasla W1 e non si rivendica onset
osservato esattamente a 25 h. Dettaglio e limiti in [REPORT_SMOKE.md](smoke/REPORT_SMOKE.md).

Tempo run **9.599 s**, sola chiamata di simulazione **9.313331 s**, processo MATLAB
completo **33.043492 s**. Proiezione preregistrata `40 × 9.599 × 65/25.1`:
**994.32 s = 16.57 min**, circa **16.96 min con un overhead di processo**.
È una stima lineare da un solo F1 breve, non una misura dei quaranta run o un limite superiore.
Le impronte del manifest e degli output sono state riverificate senza modificare i file.

## 5. Handoff, commit e lavoro aperto

Commit separati, nell'ordine richiesto:

1. `c02111d` — specifica pre-esecuzione, fonti, provenienza e baseline documentale.
2. `55d442b` — piano, script, strumentazione e handoff.
3. `88eb34e` — 21 test e riscontri di compilazione/preflight.
4. Commit smoke — questo report, verifica, dati/log/manifest dello smoke e controlli finali;
   l'identificatore viene riportato dalla consegna Git, senza auto-referenza nel contenuto.

Il commit salva la preparazione; non costituisce congelamento scientifico o verifica
indipendente. Nessun push o tag. Nessun aggiornamento prematuro del walkthrough.

Restano: verifica indipendente, lancio dei 40 run in un'altra finestra, accettazione dei
40 manifest e conteggio delle finestre effettive, conservazione recuperabile dei dati
batch ignorati da Git, poi sviluppo di feature/insight/prototipi nelle fasi previste.
D2, D11, OOD e producer non sono stati decisi. Non è emersa una nuova decisione scientifica
obbligatoria oltre a quelle già approvate; l'avvio del batch e l'eventuale pubblicazione
dei dati appartengono alle finestre successive. La presenza di una finestra di controllo
non prova stazionarietà del processo; non è stata introdotta una selezione per regime.

## Profili, modello e fonti lette

Codex basato su GPT-6, come dichiarato dall'ambiente della sessione; nessuna delega o
invocazione di altri modelli. Sotto-attività 1: decisionale, con intervento dell'autore;
2–3: implementativo; 4: verifica implementativa singola; 5: consegna implementativa.
Il profilo esecutivo-batch è escluso da questa finestra.

Letti i prompt operativi e di commit; MAINTENANCE §§1/2/8; walkthrough studio2 §0/0.1 e
Fase 03; catalogo al tag, riga aperta D1; piano §6.2; specifica, configurazione, provenienza,
report, verifica, freeze, generatore, launcher, compilatore e manifest della Fase 02;
sorgente nelle sezioni RNG, attivazioni, grandezze perturbate, output e trip; walkthrough
storici nelle sezioni operative pertinenti e codice di caratterizzazione/generazione
verificato; fonte primaria Downs & Vogel pp. 250–251. Le impronte delle dipendenze
operative di Fase 02 coincidono con il freeze. Il limite dei commit storici non disponibili
rimane dichiarato. Ordine di grandezza: circa **35–45k token di letture utili**, oltre a
output tecnici; l'output iniziale non filtrato del test documentale è stato molto più ampio
e non è assunto come materiale scientifico da riusare. Nessuna lettura in blocco del corpus.

## File toccati

- `DOCUMENTATION_INDEX.md` — mappa della nuova cartella operativa.
- `studio2/PROVENIENZA.md` — riusi con impronte, decisioni approvate ed esposizioni incidentali.
- `studio2/fase03/fault_runs/.gitignore` — esclusione build/cache e futuri dati batch.
- `studio2/fase03/fault_runs/BASELINE_CHECK.json` — esito documentale prima delle modifiche.
- `studio2/fase03/fault_runs/FINAL_CHECK.json` — controlli conclusivi e confronto col baseline.
- `studio2/fase03/fault_runs/HANDOFF_BATCH.md` — comando MATLAB/nohup, destinazione, completamento e vincoli operativi.
- `studio2/fase03/fault_runs/REPORT_RUN_FAULT.md` — resoconto della sola sotto-fase preparatoria, senza chiudere Fase 03.
- `studio2/fase03/fault_runs/SOURCE_AUDIT.json` — fonti, commit, hash e censimento dei dodici manifest Fase 02.
- `studio2/fase03/fault_runs/SPECIFICA_RUN_FAULT.md` — specifica pre-esecuzione e limiti da dichiarare nel paper.
- `studio2/fase03/fault_runs/build_generation_plan.py` — generazione deterministica e rifiuto di piani o destinazioni difformi.
- `studio2/fase03/fault_runs/compile_fault_philox.m` — compilazione confinata del nuovo MEX senza sovrascrittura.
- `studio2/fase03/fault_runs/fault_protocol.py` — parser, finalizzazione immutabile, finestre e audit della campagna.
- `studio2/fase03/fault_runs/generate_fault_runs.m` — launcher MATLAB con piano e destinazione espliciti, log e gestione errori.
- `studio2/fase03/fault_runs/launch_fault_batch.sh` — avvio background esclusivo; consegnato ma non eseguito.
- `studio2/fase03/fault_runs/plans/fault_dev.csv` — 40 righe approvate, stream 30000–30039.
- `studio2/fase03/fault_runs/plans/smoke.csv` — unica riga F1 breve, stream 30040.
- `studio2/fase03/fault_runs/prepare_simulator.py` — copia C strumentata riproducibile; guardia sull’hash qualificato.
- `studio2/fase03/fault_runs/smoke/FINAL_TEST_LOG.txt` — log, misure o verifica dello smoke e della consegna.
- `studio2/fase03/fault_runs/smoke/LAUNCH_TIMING.json` — log, misure o verifica dello smoke e della consegna.
- `studio2/fase03/fault_runs/smoke/MATLAB_LAUNCH.log` — log, misure o verifica dello smoke e della consegna.
- `studio2/fase03/fault_runs/smoke/REPORT_SMOKE.md` — riscontro fisico, tempi, scarto di onset e limiti dello smoke.
- `studio2/fase03/fault_runs/smoke/SMOKE_CHECK.json` — log, misure o verifica dello smoke e della consegna.
- `studio2/fase03/fault_runs/smoke/f1_short_001/events.jsonl` — eventi timestampati della campagna smoke.
- `studio2/fase03/fault_runs/smoke/f1_short_001/generation_manifest.csv` — manifest aggregato della sola campagna smoke.
- `studio2/fase03/fault_runs/smoke/f1_short_001/smoke-F1-001.attempt.json` — metadati originali del tentativo MATLAB.
- `studio2/fase03/fault_runs/smoke/f1_short_001/smoke-F1-001.csv` — grezzo numerico dell’unico smoke, conservato senza modifiche.
- `studio2/fase03/fault_runs/smoke/f1_short_001/smoke-F1-001.diagnostics.csv` — diagnostiche interne e IDV campionati, separati dal grezzo.
- `studio2/fase03/fault_runs/smoke/f1_short_001/smoke-F1-001.manifest.json` — manifest immutabile dell’unico run.
- `studio2/fase03/fault_runs/smoke/f1_short_001/smoke-F1-001.simulation.log` — log, misure o verifica dello smoke e della consegna.
- `studio2/fase03/fault_runs/tests/BUILD_LOG.txt` — test o riscontro tecnico eseguito prima dello smoke.
- `studio2/fase03/fault_runs/tests/MATLAB_PREFLIGHT.txt` — test o riscontro tecnico eseguito prima dello smoke.
- `studio2/fase03/fault_runs/tests/TEST_LOG.txt` — test o riscontro tecnico eseguito prima dello smoke.
- `studio2/fase03/fault_runs/tests/TEST_REPORT.json` — test o riscontro tecnico eseguito prima dello smoke.
- `studio2/fase03/fault_runs/tests/test_fault_runs.py` — test o riscontro tecnico eseguito prima dello smoke.
- `studio2/fase03/fault_runs/verify_smoke.py` — verifica in sola lettura dell’unico smoke e proiezione dei tempi.

- `studio2/fase03/fault_runs/DELIVERY_MANIFEST.json` — impronte della consegna, escluse questa stessa impronta e cache/build ricostruibili.

File locali generati e ignorati: runtime/source (sorgente strumentato e due header),
runtime/build (MEX), log di preparazione e cache dello smoke. Ricostruibili con lo script;
le loro impronte effettive sono nei manifest e nel report test. Nessun dato batch presente.
