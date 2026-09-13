# Deterministic verbalizer and evidence layer

## Dalla traiettoria alle unità evidence

Ogni run fault di sviluppo usa un innesco a 25 h e un orizzonte di 40 h post-innesco. Il tratto
post-fault è suddiviso in otto finestre half-open complete da 5 h; per ciascuna finestra vengono
calcolate feature su 41 variabili misurate, senza selezionare finestre in base al loro contenuto.
[Fonte: `fault_runs/SPECIFICA_RUN_FAULT.md`; 03.6 `DIPENDENZE_EVIDENCE.md`]

La pipeline congelata è `serie → feature per finestra → JSON strutturato → testo neutrale → firma`.
Il JSON e il testo descrivono deviazioni, direzioni e dinamiche con vocabolario controllato; non
contengono identità del fault, IDV, meccanismo, pseudolabel o marca di provenienza del catalogo.
[Fonte: 03.6 `DIPENDENZE_EVIDENCE.md` §2–§4; codice congelato `tep_features.py` e `tep_verbalize_v2.py`]

La firma evaluator-side concatena diciassette componenti normalizzate per ciascuna delle
quarantuno XMEAS e ha quindi 697 dimensioni in `[0,1]`. Serve a rappresentare in modo deterministico
la struttura dell'evidence e ad alimentare comparator numerici; non è una predizione e la sua
separabilità non implica che un reasoner produca la diagnosi corretta.
[Fonte: 03.6 `DIPENDENZE_EVIDENCE.md`; `REPORT_EVIDENCE.md`; walkthrough operativo del primo studio §«Evaluator · signature vector»]

## Baseline di normalizzazione e soglie

Le statistiche di normalizzazione provengono dai cinque blocchi Normal N1–N5 del primo studio e
sono riusate sotto la decisione U3 soltanto insieme alle quattro soglie del verbalizzatore già
congelate. Questo riuso non rende i dati auto-generati per il nuovo studio e non autorizza a usarli
per calibrazione, verifica o test.
[Fonte: 03.6 `DIPENDENZE_EVIDENCE.md` §3; `studio2/PROVENIENZA.md` U1/R2 e U3; MAINTENANCE §8.2]

La soglia dello score Normal del nuovo studio è invece calibrata su 350 run `cal_thr` e verificata
su 150 run `far_ver`, con i due insiemi separati. La forma operativa è `S > soglia`; il valore della
soglia e il FAR osservato non sono riportati in questa bozza finché la verifica indipendente di
03.5 non è disponibile e approvata.
[Fonte: 03.5 `SPECIFICA_SOGLIE_NORMAL.md` e `THRESHOLD_FREEZE.json` a `9507143`; vincolo del prompt 03.15]

## Neutralità e anti-leakage

Fault, batch e stream sono conservati in un indice evaluator-side separato dagli artefatti
consumer-facing. Lo scanner fail-closed cerca identificatori, nomi di meccanismo, descrizioni del
catalogo e label fuori dai campi ammessi. Le violazioni arrestano la produzione; non vengono
corrette mediante riscrittura silenziosa.
[Fonte: 03.6 `DIPENDENZE_EVIDENCE.md` §4; 03.12 `DECISIONE_SCHEMA_INSIGHT.md`]

Il controllo lessicale è deliberatamente conservativo ma non costituisce una prova semantica
universale: parafrasi non previste possono sfuggire e parole innocue possono generare falsi
positivi. Per questo raw, esito di validazione e numero di tentativi sono conservati e la conformità
è riportata come misura distinta dalla fedeltà dell'evidence.
[Fonte: 03.12 `DECISIONE_SCHEMA_INSIGHT.md`; `VERIFICA_SCHEMA_INSIGHT.md` §3–§5]

## Provenienza e riproducibilità

Il codice del primo studio è letto al commit e all'impronta registrati e riusato per funzione,
senza modificare gli originali. I nuovi run, manifest, JSON, testi e firme vivono sotto `studio2/`;
la provenienza registra origine, commit, hash, trasformazioni, ruolo e marca pre-specificata o
post-hoc. Nel paper i dati riusati sono descritti mediante configurazione, seed e data di
generazione, senza una narrazione causale del primo studio.
[Fonte: MAINTENANCE §8.2; 03.6 `DIPENDENZE_EVIDENCE.md`; `studio2/PROVENIENZA.md`]

L'estrazione congelata di sviluppo comprende quaranta run, trecentoventi unità e, per ciascuna
unità, feature, JSON, testo e firma. Queste quantità descrivono il materiale di sviluppo e la sua
completezza, non un risultato diagnostico; accuracy, rilevabilità e separabilità sono escluse da
questa fase.
[Fonte: 03.6 `REPORT_EVIDENCE.md`]

La motivazione storica ammessa è limitata a due osservazioni: B = 86,1% nello studio esplorativo e
B = 94,4% nella replica, dichiarato descrittivo. Questi valori motivano il nuovo studio ma non
calibrano soglie, selezione, ipotesi o decisioni del protocollo.
[Fonte: piano §8.10 punto 1; walkthrough v2 §7.3 e §8.3]

