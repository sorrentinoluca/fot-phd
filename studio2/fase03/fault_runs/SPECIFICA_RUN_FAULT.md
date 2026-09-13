# Specifica pre-esecuzione dei run fault di sviluppo — §6.2

Stato: **pre-specificata, approvata dall'autore in questa conversazione prima di ogni
simulazione** (2026-09-13). Il commit della specifica precede implementazione e smoke.
Non è un tag di congelamento né una verifica indipendente. Base: `9ec8779`, branch
`codex/studio2-fault-runs`. Questa finestra prepara 40 run ed esegue soltanto uno smoke.

## 1. Fonti e invarianti

Il catalogo è F1/F2/F3/F8/F10/F13/F14/F15, dal tag
`studio2-fase03-catalogo-D1-frozen-001` (commit `ab43f0b20f45cdb475c0caf52c6f7afcbae50891`).
Il piano autorevole §6.2 prescrive otto fault × cinque batch = **40 simulazioni nuove**,
per insight e prototipi di sviluppo, mai valutazione. R1 resta respinto.
Origini, commit e SHA-256 verificati sono in [SOURCE_AUDIT.json](SOURCE_AUDIT.json)
e [PROVENIENZA.md](../../PROVENIENZA.md).

Si mantengono integralmente i parametri della [Fase 02](../../fase02/SPECIFICA_GENERAZIONE.md):
Mode 1, stato iniziale qualificato, solver `ode45`, `Ts_base=0.0005 h`, uscita `1/60 h`,
finestre da 5 h, burn-in 20 h, Philox4x32-10, chiave radice `0x464f545445503032`,
stream uguale all'indice uint64 del run, contatore iniziale 0. `MSFlag=0`, dunque bit
`0x20` spento. Nessun cambio di setpoint. I dieci segmenti utili dei Normal di Fase 02
non impongono dieci segmenti post-fault: riguardano quel diverso piano di generazione.

La strumentazione del MEX sarà una copia nuova sotto questa cartella, con sole letture e
registrazioni aggiunte a inizializzazione, output e arresto; nessuna modifica a equazioni,
controllori, rumore, `tefunc`, `tesub6_`, Philox o loro ordine di chiamata. Un test rimuoverà
le aggiunte marcate e ricostruirà byte per byte il sorgente qualificato. Verranno registrati
gli hash di entrambe le versioni. Non si attribuisce automaticamente alla nuova build una
qualifica numerica indipendente: lo smoke copre l'integrazione, non tutti i fault.

## 2. Fault e risoluzione della nota Downs & Vogel

Fonte della tassonomia: Downs e Vogel (1993), *A plant-wide industrial process control
problem*, tabella 8, p. 250; DOI `10.1016/0098-1354(93)80018-I`;
[PDF primario](https://users.abo.fi/~khaggblo/RS/Downs.pdf), pp. 250–251 consultate direttamente.
Per l'attivazione effettiva prevale il sorgente `temexd_philox.c` qualificato della Fase 02.
Gli IDV sono uno-based; gli array C sono zero-based.

| Fault | Ingresso dopo l'innesco | Meccanismo | Variabile e riscontro nel sorgente base |
| --- | --- | --- | --- |
| F1 | IDV(1)=1 | step | rapporto A/C nel flusso 4, B costante; `xst[24] -= .03`, compensazione in C, righe 2473–2479 |
| F2 | IDV(2)=1 | step | composizione B del flusso 4, rapporto A/C costante; contributi −.00243719 ad A e +.005 a B, righe 2473–2479 |
| F3 | IDV(3)=1 | step | temperatura alimentazione D, flusso 2; `tst[0] += 5`, righe 2480–2481 |
| F8 | IDV(8)=1 | random variation | composizione A/B/C del flusso 4; attiva i due cammini `idvwlk[0:1]`, C per complemento, righe 2207–2208 e 2473–2479 |
| F10 | IDV(10)=1 | random variation | temperatura alimentazione C (flusso 4, miscela A/C nel codice); `idvwlk[3]` e `tst[3]`, righe 2210 e 2482 |
| F13 | IDV(13)=1 | slow drift | cinetiche di reazione; `idvwlk[6:7]`, fattori `r1f/r2f`, righe 2213–2214 e 2487–2488 |
| F14 | IDV(14)=1 | sticking valve | acqua reattore, XMV(10); `ivst[9]=idv[13]`, riga 3569 |
| F15 | IDV(15)=1 | sticking valve | acqua condensatore, XMV(11); `ivst[10]=idv[14]`, riga 3570 |

Per F14/F15 il parametro `vst` è **2 punti percentuali di apertura**, inizializzato alla
riga 1797. Quando IDV=1 il comando interno `vcv` resta invariato finché lo scarto assoluto
dal comando XMV non supera strettamente 2; oltre la banda, `vcv` segue il nuovo comando.
La posizione fisica continua a seguire la dinamica della valvola. Non è una valvola
immobilizzata per sempre e non è un disturbo aggiuntivo di temperatura. Il sorgente non
accende automaticamente un altro IDV (righe 3569–3599).

Downs & Vogel raccomandano per IDV(14)–(20) l'uso con un altro disturbo o un cambio di
setpoint e suggeriscono 24–48 h per osservarne pienamente gli effetti. A p. 251 citano
specificamente IDV(12)+IDV(15). **Lo studio adotta invece un solo IDV per run**, tutti gli
altri 27 a zero, prima e dopo l'innesco come appropriato: nessuna perturbazione congiunta,
nessun cambio di setpoint. È una decisione dell'autore, non una prescrizione della fonte.
L'orizzonte post-innesco è 40 h; ricade nell'intervallo suggerito, ma nessuna fonte dimostra
che basti a rendere diagnosticabili questi due fault senza eccitazione aggiuntiva.

Regola preregistrata: **segnale debole o assente in F14/F15 è un esito da registrare**.
Dopo l'osservazione non si aggiungono disturbi, non si allunga l'orizzonte, non si cambiano
le finestre e non si sostituiscono run o fault.

## 3. Tempi, controllo interno e finestre

Decisione approvata: innesco a **25 h**, orizzonte post-innesco **40 h**, termine **65 h**.
IDV nullo in `[0,25)`, solo l'IDV prescritto attivo in `[25,65]`.

| Intervallo assoluto | Ruolo | Campioni previsti a 1 min | Uso sviluppo |
| --- | --- | ---: | --- |
| [0,20) | burn-in qualificato, scartato | 1200 | no |
| [20,25) | controllo negativo interno pre-fault | 300 | **no** |
| [25,30), [30,35), [35,40), [40,45) | W1–W4 post-fault | 300 ciascuna | sì |
| [45,50), [50,55), [55,60), [60,65) | W5–W8 post-fault | 300 ciascuna | sì |
| endpoint a 65 | conservato nel grezzo | 1 | no |

La finestra pre-fault serve al controllo pre/post della variabile perturbata e alla
diagnostica del regime prima dell'innesco; resta separata dalle otto finestre per insight
e prototipi, salvo successiva decisione pre-specificata. Non si fissa qui un test statistico
di stazionarietà, né si selezionano run in funzione del controllo. Regime qualificato
a livello di procedura non significa regime dimostrato per ciascuna traiettoria.

Il controllo tecnico legge IDV effettivamente consegnati al processo e tempo osservato
di attivazione. La diagnostica registra composizioni/temperature/fattori cinetici interni e
comandi/posizioni delle due valvole, distinta dalle XMEAS prompt-facing. La verifica del
segnale fisico pre/post non può essere sostituita dal solo flag; viceversa, una risposta
fisica debole non invalida un flag attivato correttamente. Questi segnali diagnostici
non entrano automaticamente nelle feature o nei prompt. Non si calcolano qui insight,
prototipi, separabilità o score per-fault del batch.

Nel primo studio la convenzione documentata era 10 h di pre-fault + 40 h post-fault,
otto finestre `[10,15)` … `[45,50)`, verificate in `code/tep_characterize_v2.py`, costanti
e chiamata `analyze_case_windows`; il modello storico locale contiene il ritardo di 10 h.
Si riusano **40 h, otto finestre e intervalli half-open**, non il vecchio burn-in o i dati.
Si trasla l'innesco a 25 h per rispettare le 20 h qualificate e il controllo interno
aggiunto dall'autore. La continuità è operativa, non una giustificazione di ottimalità.

## 4. Indici, flussi e seed

Il censimento legge tutti i 12 manifest di Fase 02, compresi tentativi preliminari e smoke,
e il suo generatore di piani. Intervalli inclusivi:

| Intervallo | Occupazione o prenotazione Fase 02 |
| --- | --- |
| 0–9 | burn-in, già usati |
| 100–109 | prefissi, già usati e ripetuti secondo quel piano |
| 200–209 | confronto Philox, già usati; anche ordinali delle coppie legacy |
| 1000–1009 | pilot R2, già usati |
| 2000–2099 | riservati a `baseline_fit_new`, fallback |
| 10000–10349 | riservati a `cal_thr` |
| 20000–20149 | riservati a `far_ver` |
| 999999 | smoke tecnici Fase 02, già usato |

I seed del vecchio generatore di confronto sono 1431655766–1431655775: non sono stream
Philox. Le ripetizioni documentate non creano nuovi indici; sono tutte censite.

**Riservati ora: 30000–30039, sviluppo; 30040, solo smoke.** Per posizione del fault
`k=0,…,7` nel catalogo congelato e batch `b=1,…,5`:
`run_index_uint64 = stream_id = 30000 + 5*k + (b-1)`.
ID `fault-dev-F<idv>-b<batch a due cifre>`. Nessuna estrazione o riestrazione.

Il seed riproducibile è la coppia `(chiave radice, stream_id)`: il piano ne registra
`seed_descriptor = 0x464f545445503032:<stream su 16 cifre hex>`, oltre a `stream_lo32`
e `stream_hi32` derivati per maschera e shift. **Non si deriva una chiave diversa per run**:
Philox costruisce il contatore `[draw//4 low32, draw//4 high32, stream low32, stream high32]`.
Questa è la derivazione effettiva dei flussi, non un seed legacy né un hash usato per un
secondo RNG. I valori passati all'interfaccia double del MEX sono tutti esatti (`<2^53`).
La separazione dei futuri run di test deve rispettare anche queste nuove prenotazioni;
non autorizza a inferire i seed mancanti dei dati storici.

## 5. Trip, errori e scrittura

Si applica integralmente §3 della Fase 02. Un **trip fisico prima di 65 h** conserva il
prefisso originale, tempo esatto della richiesta d'arresto `trip_time_h`, codice e messaggio;
stato `physical_trip`. Nessun padding, troncamento aggiuntivo o sostituzione. Si registrano
separatamente finestre complete e incomplete. Un trip prima dell'innesco resta un trip,
con `activation_observed=false`. Il lotto fault può proseguire sugli altri indici fissati.

Un errore tecnico produce `technical_failure`, manifest e log del tentativo; nessun
parziale è promosso a output scientifico. Il lotto si arresta, segnando esplicitamente
gli indici non eseguiti. Nessun retry automatico. Dopo una correzione un eventuale replay
deve usare lo stesso stream, una nuova destinazione e una procedura esplicita che conservi
tutti i tentativi e verifichi il prefisso; divergenze invalidano il run. Questa finestra
non autorizza né implementa una rigenerazione automatica.

Piano e destinazione sono obbligatori; destinazioni ammesse soltanto sotto
`fault_runs/runs/` per il batch e `fault_runs/smoke/` per lo smoke. Cartella campagna
nuova, acquisizione esclusiva, nessuna ripresa/sovrascrittura. Ogni output viene scritto
una volta, chiuso, poi sottoposto a SHA-256. I manifest per-run sono immutabili; il
manifest aggregato viene scritto una volta a fine campagna. Cache, log e temporanei
restano nel perimetro nuovo. Non si modifica il modello qualificato su disco.

## 6. Manifest e accettazione

Formato per-run JSON, aggregato CSV; contatori e indici uint64 sono stringhe decimali
nel JSON per evitare arrotondamenti nei lettori. Ogni manifest contiene almeno:

- identità: `schema_version`, `run_id`, `set_name`, `batch`, `run_index_uint64`, `stream_id`,
  `seed_descriptor`, `stream_lo32`, `stream_hi32`, `rng_algorithm`, `rng_key_hex`,
  `counter_start`, `counter_end`;
- disegno: `idv`, `onset_h`, `horizon_h`, `stop_time_h`, `burn_in_h`, `ts_base_h`,
  `output_interval_h`, `msflag`, `window_h`, `pre_fault_window`, `post_fault_windows`,
  `useful_windows_expected`, `useful_windows_complete`, `development_eligible` per finestra;
- esecuzione: `status`, `actual_end_h`, `trip_time_h` (null senza trip), `trip_code`,
  `message`, `activation_observed`, `observed_onset_h`, `idv_trace_valid`, `platform`,
  `matlab_version`, `started_at_utc`, `finished_at_utc`, `runtime_seconds`,
  `simulation_seconds`;
- impronte: `mex_sha256`, `model_sha256` (modello base su disco), `script_sha256`,
  `source_sha256`, `base_source_sha256`, `plan_sha256`, `spec_sha256`,
  `dependency_hashes`, `model_overrides` (configurazione effettiva), `git_commit`;
- artefatti: `output_path`, `sha256`, `data_rows`, `columns`, `diagnostic_path`,
  `diagnostic_sha256`, `simulation_log_path`, `simulation_log_sha256`.

Il grezzo è CSV numerico (tempo, 41 XMEAS, 12 XMV), invece del contenitore XLSX del launcher
Normal: conserva i valori double a 17 cifre e rende trasparente la verifica e la conservazione
dello smoke in Git. Il log contiene timestamp UTC ed eventi JSON `campaign_start`,
`run_start`, `run_end`, `campaign_end`. Il log del simulatore conserva le righe diagnostiche
`FOT_DIAG`, le transizioni `FOT_IDV` e gli eventuali `FOT_TRIP`; il parser rifiuta righe
strumentali malformate. Log e diagnostiche hanno hash nel manifest per-run.

Accettazione documentale: **40/40 manifest completi**, corrispondenza univoca col piano,
tutti gli hash verificati e nessun output modificato dopo scrittura. Accettazione tecnica
del batch: tutti i 40 tentativi `complete` o `physical_trip`, nessun `technical_failure`
o `not_run`; griglia, schema, IDV e tempi coerenti sui prefissi disponibili. Trip registrati
non diventano run completi da 65 h. Disponibilità scientifica: numero effettivo di finestre
complete riportato, mai assunto pari a 320. Il validatore ricalcola gli hash e produce un
esito distinto; la sola presenza di `campaign_end` non è un PASS. Un arresto prematuro
senza evento fisico strumentato è errore tecnico, mai classificato per supposizione.

## 7. Smoke prespecificato e costo

Unico run **F1**, primo del catalogo, stream **30040**, onset 25 h, burn-in 20 h,
controllo `[20,25)`, **orizzonte post-fault ridotto a 0.1 h**, stop 25.1 h. Tutti gli
altri invarianti rimangono identici. Zero finestre post-fault complete; nessun uso
scientifico. Destinazione `smoke/f1_short_001`, distinta dai 40 run. Si controllano
IDV nullo prima di 25 h, solo IDV(1) dopo, cambio interno della composizione prescritto,
manifest, hash, schema, griglia e assenza di trip/errore. Nessun altro run in questa finestra.

La Fase 02 registra circa 9.21 s mediani per simulazione Normal da 70 h, solo riferimento
di costo; non è una previsione misurata per questi fault. Dopo lo smoke si riportano
tempo simulazione e tempo totale reale (inclusa scrittura), più avvio MATLAB esterno.
Proiezione dichiaratamente grezza: `40 × runtime_seconds_smoke × 65/25.1`, con separata
proiezione della sola simulazione. L'avvio MATLAB si paga una volta nel batch sequenziale.
Fault diversi, diagnostiche, I/O e trip rendono la stima non un limite superiore né un SLA.

## 8. Limiti da dichiarare nel paper

- F14/F15 sono studiati singolarmente senza l'eccitazione congiunta raccomandata da
  Downs & Vogel, pp. 250–251. Quaranta ore post-innesco non garantiscono un segnale
  sufficiente. Segnale debole/assente resta un risultato; niente adattamenti post-hoc.
- Innesco a 25 h, burn-in 20 h, controllo interno `[20,25)` escluso dallo sviluppo,
  otto finestre da 5 h fino a 65 h: scelte progettuali approvate, non ottimizzate sui dati.
  Il controllo interno è descrittivo e non prova da solo regime o causalità.
- Finestre dello stesso run sono dipendenti, non repliche indipendenti. Questi 40 run
  servono a sviluppo, insight e prototipi, mai alla valutazione delle prestazioni.
- I trip possono ridurre il materiale disponibile; nessuna selezione sulle durate riuscite.
- Esposizione incidentale alla tabella narrativa storica per-fault della v2 dichiarata
  in PROVENIENZA; nessun suo valore usato. Non si rivendica cecità assoluta ai risultati
  storici. L'origine temporale è verificata sul codice, non sulle prestazioni storiche.
- Un solo smoke F1 non qualifica numericamente tutti gli otto fault o i loro trip;
  le aggiunte diagnostiche al MEX richiedono verifica indipendente del codice.

Non si aggiorna il walkthrough né si chiude la macro-Fase 03 prima della verifica
indipendente. Restano escluse le decisioni D2/D11/OOD, il batch e ogni chiamata LLM.
