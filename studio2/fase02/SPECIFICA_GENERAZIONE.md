# Fase 02 — Specifica pre-esecuzione della generazione

**Stato:** specifica fissata prima di compilazione, simulazioni e confronti numerici.

Questa specifica chiude le scelte operative necessarie a implementare e validare la generazione;
non certifica che i gate siano già superati. I valori machine-readable sono in
[`generation_spec.json`](generation_spec.json). Il registro di calibrazione resta autorevole per
allocazione, score e inferenza; questo documento rende eseguibili i suoi tre prerequisiti
operativi e il confronto dei prefissi.

## 1. Parametri invarianti

- `Ts_base = 0.0005 h` (**1,8 s**) per ogni nuovo run. È il periodo dei controllori discreti,
  non la frequenza di salvataggio. Il valore è coerente con gli init del simulatore; non viene
  inferito quale `Ts_base` sia stato usato storicamente per N1–N5.
- Campionamento dell'uscita: `1/60 h` (**1 min**).
- Finestra utile: **5 h**; un run pieno contiene dieci finestre utili dopo il burn-in.
- `cal_thr` e `far_ver` devono condividere modello, stato iniziale, `Ts_base`, burn-in, frequenza
  di uscita, versione del MEX e famiglia di chiavi. Cambiano soltanto identificatore di flusso e
  lunghezza prevista dal disegno.
- RNG: **Philox4×32-10**; chiave radice `0x464f545445503032`; identificatore di flusso uguale
  all'indice `uint64` del run; contatore uguale all'indice `uint64` dell'estrazione uniforme.
  Il bit `0x20` di `MSFlag` resta spento. `tesub6_` conserva la somma di dodici uniformi e la
  trasformazione `(somma − 6) · std`.

La chiave radice è un identificatore pubblico di protocollo, non un segreto. Philox separa i
flussi pseudocasuali; non dimostra indipendenza matematica o scambiabilità.

## 2. Procedura congelata per determinare il burn-in

Il burn-in non viene scelto guardando `cal_thr`, `far_ver`, fault o test. Si riservano dieci flussi
Normal diagnostici, indici 0–9, esclusi da ogni uso successivo. Per ciascuno si genera una
traiettoria di 70 h con la procedura definitiva. I candidati, fissati prima dell'esecuzione, sono
10, 20, 30 e 40 h; il riferimento tardivo è l'intervallo `[60,70)` h.

Per ogni candidato e per il riferimento si calcolano, sulle due finestre da 5 h e sui dieci run,
le quattro famiglie per-variabile che alimentano lo score:
`abs_shift_sigma`, `abs_slope_sigma_h`, `residual_std_ratio`, `diff_std_ratio`. La baseline usata
per questo solo confronto è la stessa baseline congelata prevista per lo score; il controllo è
descrittivo e non produce indipendenza.

Un candidato supera il controllo quando, per **ognuna delle quattro famiglie**, rispetto al
riferimento tardivo:

1. lo scarto assoluto fra le mediane aggregate non supera `0,5 · MAD_riferimento`;
2. il rapporto `MAD_candidato / MAD_riferimento` è in `[0,5; 2,0]`;
3. MAD nulla o non definibile produce fallimento, non una sostituzione silenziosa.

Si sceglie il primo candidato non inferiore a 20 h che supera insieme al candidato immediatamente
successivo; la richiesta di due candidati consecutivi evita di dichiarare regime sulla base di un
solo intervallo favorevole. Con i candidati fissati, 20 h viene scelto solo se passano 20 e 30 h;
30 h solo se passano 30 e 40 h. Se non esiste una coppia, la generazione operativa si arresta e la
qualifica viene estesa con candidati e riferimento più tardivi in una revisione pre-esecuzione.
Non si assume automaticamente 40 h e non si esaminano i set di calibrazione o verifica per decidere.

Il manifest di ogni run registra burn-in scelto e intervallo scartato. La posizione 1 del FAR
resta una diagnostica successiva: un eccesso può suggerire transitorio residuo, ma non riapre
automaticamente il burn-in né autorizza l'esclusione post-hoc di finestre.

## 3. Politica sui trip e sui fallimenti

Si classificano gli arresti prima di decidere il destino del run.

- **Trip fisico del processo:** si conserva il file fino all'arresto, lo si marca `physical_trip`
  con tempo e messaggio, e non lo si rilancia «finché passa». Non sono ammessi padding,
  troncamenti ulteriori o scelta della replica più favorevole. Per i fault il caso resta un esito
  fisico; l'eventuale non valutabilità a lunghezza fissa viene riportata, non sostituita.
- **Trip in un run Normal di qualifica, pilot, `cal_thr` o `far_ver`:** il lotto si arresta. Il run
  non viene scartato né sostituito, perché ciò condizionerebbe il campione al raggiungimento della
  durata richiesta. Si apre una revisione del generatore e si riparte, se autorizzato, con un nuovo
  namespace di flussi e con tutti i tentativi registrati.
- **Fallimento tecnico** (crash, I/O, MEX, spazio disco): nessun output parziale entra nei dati.
  Dopo la correzione si può rieseguire **lo stesso** stream ID soltanto per verificare la
  riproducibilità; ogni tentativo resta nel log. Se il prefisso precedente non è byte-identico,
  il run è invalidato e la causa va risolta prima di proseguire.

Queste regole distinguono un evento del processo da un errore dell'infrastruttura e impediscono
rerun selettivi basati sul contenuto.

## 4. Gate di accettazione di Philox

Prima dell'uso sperimentale sono tutti obbligatori:

1. compilazione pulita della copia versionata del simulatore e del MEX;
2. corrispondenza **esatta bit per bit** con i known-answer test ufficiali Random123 per
   Philox4×32-10;
3. replay della sequenza uniforme byte-identico a parità di chiave, stream e contatore;
4. stream ID e contatore osservati nel log senza riuso o regressione; il contatore diagnostico
   delle callback viene riportato separatamente;
5. misura del tempo su almeno cinque esecuzioni identiche, riportando mediana e intervallo min–max.

La prestazione è una misura, non un criterio scientifico di equivalenza: non si nasconde un
overhead elevato, ma nessuna soglia temporale sostituisce i gate di correttezza.

## 5. Gate di confronto Philox–legacy

Si generano dieci run Normal per generatore, separati da tutti gli altri set, con identica
configurazione e burn-in qualificato. Il confronto riguarda, separatamente, le quattro famiglie di
score e lo score combinato `S`. Per ogni metrica Philox è dichiarato compatibile col legacy solo se:

I run legacy usano, nell'ordine, i dieci seed espliciti `1431655766`–`1431655775`; i dieci run
Philox usano gli stream 200–209. I numeri condivisi 200–209 identificano soltanto le coppie del
confronto e non implicano una corrispondenza fra stato legacy e stream Philox.

- `|mediana_Philox − mediana_legacy| ≤ 0,5 · MAD_legacy`;
- `MAD_Philox / MAD_legacy ∈ [0,5; 2,0]`;
- mediane e MAD sono finite e `MAD_legacy > 0`.

Istogrammi ed ECDF, incluso KS a due campioni, sono descrittivi e non aggiungono un p-value gate.
Devono passare tutte e cinque le metriche. Un fallimento blocca l'uso sperimentale di Philox:
lo scostamento si dichiara e si indaga, senza assorbirlo nella calibrazione.

## 6. Gate per la forma economica e i prefissi

Dieci flussi diagnostici, esclusi dagli altri set, vengono eseguiti una volta fino a
`burn-in + 50 h` e, per ciascun `J = 1,…,10`, fino a `burn-in + 5·J h`. Si confrontano le uscite
sull'intervallo comune **escludendo il campione esattamente a `StopTime`**, che non appartiene alla
finestra half-open usata dallo score.

Per tutte le 100 coppie devono valere, con zero fallimenti:

- griglia temporale e numero di campioni identici;
- tutte le XMEAS entro `atol=1e-10`, `rtol=1e-9`;
- tutte le quattro feature per variabile entro `atol=1e-10`, `rtol=1e-8`;
- differenza assoluta dello score finale `S ≤ 1e-8`;
- identici stream ID, chiave e prefisso dei contatori RNG.

Il confronto viene eseguito con la variante A/A′ selezionata e i suoi parametri congelati. Se una
sola coppia fallisce, la forma economica è respinta e tutti i run `cal_thr` vengono generati a
lunghezza piena `burn-in + 50 h`; non si allentano le tolleranze dopo aver visto i risultati.

La concordanza delle 100 coppie sostiene l'uso operativo della forma economica ma non dimostra
equivalenza numerica generale. Una divergenza numerica, da sola, non dimostra una diversa
distribuzione degli score: il fallback a lunghezza piena è una scelta conservativa pre-specificata.

## 7. Campi minimi del manifest di generazione

Ogni tentativo registra almeno: ID e insieme del run; indice di stream; chiave Philox; intervallo
iniziale e finale del contatore; versione e SHA-256 del MEX; SHA-256 del modello; `Ts_base`;
intervallo di uscita; burn-in; durata richiesta ed effettiva; `J` e posizione della finestra;
stato completo/trip/fallimento; timestamp di inizio e fine; percorso e SHA-256 dell'output.

Prima della calibrazione vanno inoltre congelati codice di `S`, variante A/A′, riferimenti per
sensore e parametri robusti. Soglia, rango, numerosità e regola `S > soglia` vengono aggiunti dopo
la calibrazione e prima di `far_ver`, come richiesto dal registro autorevole.

La MAD è sempre `median(|x − median(x)|)` senza fattore di consistenza. Nei conteggi di dominanza
un pareggio esatto fra famiglie divide in parti uguali il peso della finestra. Applicata a N1–N5
come unico `baseline_fit`, la regola congelata seleziona A; i parametri eseguibili sono registrati
in `validation/score_fit_legacy.json`.

## 8. Guardia pre-calibrazione per il possibile riuso R2

Prima di generare il pilot si fissa anche il criterio che decide se N1–N5 può restare
`baseline_fit`. Si usano i dieci stream pilot 1000–1009, esclusi da ogni altro insieme, per run
Normal di `20 + 50 h`. Sulle 50 finestre storiche e sulle 100 finestre nuove si confrontano le
quattro famiglie per-variabile e `S`, usando N1–N5 come riferimento. Per ciascuna delle cinque
metriche valgono gli stessi limiti pre-specificati del confronto fra generatori:

- scarto delle mediane non superiore a `0,5 · MAD_N1–N5`;
- rapporto `MAD_pilot / MAD_N1–N5` in `[0,5; 2,0]`;
- quantità finite e `MAD_N1–N5 > 0`.

Devono passare tutte le metriche. Se una fallisce, R2 non è autorizzato e si attiva senza ulteriori
scelte il ramo `baseline_fit_new` da 100 run già fissato nel registro; `cal_thr` scende a 300. Se
passano tutte, R2 può essere autorizzato esclusivamente come baseline di sviluppo congelata: il
controllo non ricostruisce il `Ts_base` storico, non rende indipendenti i cinque blocchi contigui e
non li promuove a calibrazione o verifica.
