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
[Fonte: 03.6 `DIPENDENZE_EVIDENCE.md`; `REPORT_EVIDENCE.md`; S06, pin in `FONTI_DELTA_0315.json`]

## Baseline di normalizzazione e soglie

Le statistiche di normalizzazione provengono da cinque blocchi Normal contigui N1–N5
in `[0,250 h)` della configurazione Mode 1, snapshot identificato per commit e SHA-256.
Seed e data di generazione di questi blocchi non sono disponibili. L'uso U3 è limitato
alla normalizzazione e ai flag, insieme alle quattro soglie V2 come coppia indivisibile:
questa dipendenza è dichiarata e non costituisce un fit su nuovi dati. I blocchi non sono
esempi `normal_dev` né dati ammessi per calibrazione, FAR o test. Se R2 decade o si passa
a `baseline_fit_new`, tutte le evidence dipendenti, incluse le Normal, diventano invalide
e devono essere rigenerate secondo la guardia fail-closed.
[Fonte: S06 `DIPENDENZE_EVIDENCE.md` §3 e `studio2/PROVENIENZA.md` U3; S09 `SPECIFICA_NORMAL_DEV.md`; MAINTENANCE §8.2]

La soglia dello score Normal è invece calibrata su 350 run `cal_thr`: rango 334,
valore `13.623626738268857`, regola stretta `S > threshold`. Il freeze scientifico è
registrato in `950714389f92e559eac922a09404742a71c74346`; la consegna finale verificata
della 03.5 è chiusa, integrata e pubblicata. Il tag finale non retrodata quel freeze.
[Fonte: S05 `THRESHOLD_FREEZE.json`, `INTEGRAZIONE_03_5.md`]

La verifica FAR già prodotta sui 150 run separati riporta come primario 11/150 = 7,333%,
con IC Clopper–Pearson 95% [3,7175%; 12,7424%], su una finestra preassegnata per run.
Il secondario sulle dieci posizioni per run è 108/1500 = 7,2%, con intervallo bootstrap
per run 95% [5,7333%; 8,7333%]: descrive la miscela delle posizioni e preserva la dipendenza
intra-run, senza trattare le 1.500 finestre come indipendenti. Questi valori sono riscontri
della calibrazione Normal, non prestazioni diagnostiche dei modelli. Il limite di accessibilità
pre-freeze accettato dall'autore è dichiarato in `protocol.md`; soglia e decisione FAR restano invariati.
[Fonte: S05 `FAR_VERIFICATION.json`, `FAR_VERIFICATION.md`, `DECISIONE_AUTORE_FAR.md`; L `docs/letteratura.md` §14.2]

## Evidence Normal e prototipi reali

Le 320 unità Normal reali da 697 componenti sono conservate nella destinazione riuscita
`baseline_numerica/evidence/normal_dev_002`, derivate dai 40 run di sviluppo assegnati.
Attraversano le stesse funzioni e guardie 03.6, con la dipendenza U3/R2 esplicita. Gli
otto esempi Normal locali sono selezionati prima dell'osservazione: per ciascun agente,
run locale con `agent_run_index=1`, prima finestra `[25,30)`. Non si selezionano per qualità
o separabilità e non si producono insight per `Normal`.
[Fonte: S09 `SPECIFICA_NORMAL_DEV.md`, `NORMAL_DEV_HANDOFF.json`, `BASELINE_FREEZE_rev003.json`; S12 `DECISIONE_SCHEMA_INSIGHT.md`]

I prototipi costruiti sono nove globali e sedici locali, 25 vettori in tutto: la variante
globale comprende le otto label fault opache e `Normal`; ciascun agente locale dispone
del proprio fault e di `Normal`. Ogni componente è la media aritmetica di tutte le firme
di sviluppo predefinite: 40 per fault, 320 per Normal globale e 40 per Normal locale.
Le finestre usate nella media non sono repliche indipendenti; il ricalcolo già registrato
dei 25 vettori ha scarto massimo zero, senza una valutazione di prestazione.
[Fonte: S09 `SPECIFICA_BASELINE_NUMERICA.md`, `PROTOTYPES.json`, `PROTOTYPES_MANIFEST.json`, `BASELINE_CHECK.json`]

La distanza è L1 media, `d_c=(1/697) Σ_j |x_j−p_cj|`. Vince il minimo unico; due o più
distanze entro `1e-12` assoluto dal minimo danno astensione (`abstain=true`,
`predicted_label=null`). Non vi è soglia di distanza, tie-break lessicografico o ripiego
globale per classi assenti nel modello locale. `Unknown` designa solo l'astensione;
lo spazio delle label conserva otto fault opachi e `Normal` letterale.
[Fonte: S09 `SPECIFICA_BASELINE_NUMERICA.md`, `BASELINE_FREEZE_rev003.json`; 03.7 `SPECIFICA_PSEUDOLABEL.md`]

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

Le funzioni deterministiche sono identificate da commit e impronte, con parametri di
finestra espliciti. Run, manifest, JSON, testi e firme hanno provenienza tracciata:
origine, configurazione, stream quando disponibili, trasformazione e ruolo. La marca
pre-specificata riguarda l'uso fissato prima dell'osservazione pertinente, senza attribuire
cecità a dati già disponibili. Le lacune di seed/data dei blocchi N1–N5 restano dichiarate.
[Fonte: S06 `DIPENDENZE_EVIDENCE.md`, `studio2/PROVENIENZA.md`; S09 `SPECIFICA_NORMAL_DEV.md`; MAINTENANCE §8.2]

L'estrazione fault comprende 40 run e 320 unità, con feature, JSON, testo e firma per
unità; evidence-v2 conserva gli stessi file scientifici con packaging corretto. Il lotto
Normal aggiunge 40 run e 320 unità di sviluppo, pubblicati e riscaricati nella consegna
03.9. Queste quantità descrivono completezza e materiale disponibile, non accuracy,
rilevabilità o separabilità; il freeze della baseline rimane inefficace secondo S09.
[Fonte: S06 `REPORT_EVIDENCE.md`, `PACKAGING_V2_CHECK.json`; S09 `CONSEGNA_INTEGRAZIONE_03_9.md`, `BASELINE_FREEZE_rev003.json`]
