# Audit tecnico `normal_dev`

**Esito tecnico del lotto: PASS**  
**Conformità del processo: deviazioni**

Audit read-only della sotto-fase 03.9, eseguito il 2026-09-14T10:38:57.765161+00:00 su 40
workbook con un'unica invocazione di `audit_normal_dev.py`. L'audit non valuta qualità scientifica,
separabilità, score, FAR o prestazioni e non estrae evidence.

## Esito

- Run tecnicamente validi: **40/40**.
- Piano ↔ manifest ↔ workbook: **PASS**; nessun dizionario è
  usato per decidere l'unicità, verificata con molteplicità e contatori.
- Workbook: 54 intestazioni attese, 3.901 righe dati per file, soli valori numerici finiti,
  griglia `0..65 h` al minuto e otto finestre `[25,30)..[60,65)` da 300 campioni: **PASS**.
- Finestre valide: **320/320**. Sono 320 finestre appartenenti a 40 run,
  non 320 repliche indipendenti. `[0,20)`, `[20,25)` e il campione a 65 h sono esclusi.
- Tolleranza griglia: `1e-10 h` (0,36 microsecondi), superiore al roundoff XLSX osservato e
  molto inferiore al passo di un minuto. Nessun dato è stato interpolato o corretto.
- Collisioni con i piani/manifest locali enumerati: **PASS** su
  202 sorgenti (31 contenuti distinti).
  Questo non è un'affermazione globale su fonti non disponibili.

## Identità e configurazione

Il piano è byte-identico alla versione tracciata a HEAD. Tutte le righe hanno `set_name=normal_dev`,
assegnazione esclusiva 5×8, stream 60000–60039 secondo la formula prescritta, namespace e descrittori
seed attesi e `use=development_only`. Il join agente/run/stream ricostruito dal piano è registrato
integralmente nel JSON.

Tutti i manifest riportano Philox4x32-10, chiave `0x464f545445503032`, `Ts_base=0.0005 h`, output al
minuto, contatore iniziale zero e contatore finale intero positivo, orizzonte effettivo 65 h,
MEX `6ae7e7be5394773f1854f1c53eddbd778ad7557b61fb05a93b3edb0552b1d11e` e modello `c58826748edd306b723da2f0199a0fb2dc193a51dc5c28dbde8ac821e39dfafd`. I contatori finali non sono confrontati fra
stream diversi. Hash e dimensione di ogni workbook sono ricalcolati nel JSON.

Le fonti qualificate e le impronte del freeze di Fase 02 coincidono. Il codice attuale è tracciato
a HEAD `3f260f4ad2e13fd5ba545945e0a288cc56ed5f49`; i manifest non registrano il commit di esecuzione. Gli hash
dimostrano l'identità di MEX/modello e la corrispondenza delle fonti correnti, ma non provano da soli
quale checkout Git fosse attivo nel processo MATLAB.

## Tentativi e warning

Il primo tentativo è documentato da log, PID e `RECOVERY.json`: il log registra il MEX non trovato
prima del ciclo di simulazione e il suo hash coincide con quello citato nel recovery. La dichiarazione
`generated_runs=0` è coerente con il punto d'errore, ma non è provata indipendentemente da una
destinazione fallita archiviata o da un manifest del tentativo.

Il secondo tentativo termina con `Generated 40 runs`. Il log contiene
40 warning
`Variable Time Delay`: Simulink ha ampliato dinamicamente il buffer di runtime e richiede di aggiornare il parametro per la code generation. Il warning dimostra che il buffer configurato era insufficiente per queste simulazioni; questo audit non ne stabilisce l'innocuità scientifica e non invalida automaticamente gli output completi.
Contiene inoltre un warning di accesso a `~/Documents/MATLAB` e due warning Java/X11.

## Conformità del processo

Stato: **deviazioni**. Il primo tentativo è stato archiviato, ma il lancio riuscito ha riutilizzato
il pathname `normal_dev_001`; la specifica richiedeva una nuova destinazione e il tracciamento di
tutti i tentativi. Inoltre il comando riuscito con `MATLABPATH` diretto al build qualificato non è
registrato nel log o nel manifest: `RECOVERY.json` lo propone e l'hash MEX osservato è coerente,
ma non costituisce prova indipendente del comando effettivo. Queste deviazioni non hanno prodotto
un fallimento dei controlli tecnici sui 40 output, ma non vengono sanate retroattivamente.

## Decisione dell'autore

Prima dell'accettazione l'autore deve decidere se accettare formalmente la deviazione di ripresa
(riuso del pathname) e se l'evidenza disponibile sul comando/MATLABPATH è sufficiente. Deve inoltre
stabilire se i warning di crescita dinamica del buffer `Variable Time Delay` sono accettabili per
questo lotto qualificato; l'audit strutturale non può concluderne l'innocuità scientifica.

## Comando, ambiente e limiti

Comando: `/Users/luker/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 studio2/fase03/baseline_numerica/audit_normal_dev.py`  
Python: `3.12.14 (main, Aug 25 2026, 13:50:33) [Clang 22.1.3 ]`; openpyxl: `3.1.5`;
piattaforma: `macOS-26.6.2-arm64-i386-64bit`.

Controllo documentale: `docs/test_explanation.py` ha 14
fallimenti dopo l'audit, contro 14
prima: non peggiorato. Il test non copre questo audit.

Controlli non eseguiti: simulazioni o replay MATLAB; analisi scientifica dei segnali; evidence;
prototipi; baseline; score/FAR; verifica remota di collisioni; pubblicazione o conservazione esterna.
Nessun run con errori tecnici.

Fonti lette: specifica/piano/builder/preflight/wrapper/launcher/handoff 03.9; generatore Normal e
freeze Fase 02; piano rev. 7 §6.2 al commit `a572d1c`; manifest 03.5 `cal_thr`/`far_ver`; piano e
manifest del lotto; entrambi i log/PID e `RECOVERY.json`; audit 03.5 come riferimento metodologico.
Lettura documentale mirata: circa 1.800 righe di fonti testuali/CSV più freeze e audit JSON; i 40
workbook sono stati letti integralmente dallo script, senza stamparne i valori.
Il dettaglio di hash, byte, controlli per run, join, inventario, fonti e anomalie è in
`AUDIT_NORMAL_DEV.json`.
