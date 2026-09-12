# Studio 2 — Provenienza dei materiali riusati

Questo registro applica `docs/MAINTENANCE.md` §8.2. Distingue tre stati che non sono
intercambiabili:

- **conservato**: esiste una copia verificata, ma non ne deriva alcuna autorizzazione al riuso;
- **candidato al riuso**: il piano operativo ne valuta un possibile ruolo, ancora subordinato alle
  verifiche previste;
- **riuso autorizzato**: una decisione esplicita ha assegnato al materiale un uso nello studio 2.

Alla data del 2026-09-12 R1 e R2 hanno ricevuto decisioni separate: R1 è respinto come sostituzione
di nuove simulazioni fault, mentre R2 è autorizzato in modo condizionato e soltanto come
`baseline_fit`. Dettagli e limiti sono in `fase02/QUALIFICAZIONE_RIUSO.md`.

## 1. Copia conservata

I 74 contenuti distinti che la fase 01 non aveva trovato come blob Git sono stati copiati, senza
modifiche, sotto:

`studio2/fase02/patrimonio_conservato/contenuti/<sha256>.xlsx`

Il [manifest di conservazione](fase02/MANIFEST_CONSERVAZIONE.csv) collega tutte le 78 occorrenze
sorgente ai 74 contenuti unici e registra dimensione e SHA-256 sia della sorgente sia della
destinazione. Le quattro occorrenze duplicate condividono la stessa destinazione content-addressed.
La copia occupa 144.745.600 byte; il totale logico delle 78 sorgenti è 152.308.644 byte.

La copia è stata prodotta e verificata con
[`preserve_legacy_data.py`](fase02/preserve_legacy_data.py). Una seconda esecuzione ha verificato
tutti i contenuti e ha prodotto zero nuove copie. I file XLSX sono esclusi da Git per regola del
repository. I 74 workbook sono perciò conservati anche nell'archivio pubblico versionato
[`studio2-fase02-legacy-v1.tar`](https://github.com/sorrentinoluca/fot-tep-data/releases/download/studio2-fase02-v1/studio2-fase02-legacy-v1.tar),
release [`studio2-fase02-v1`](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase02-v1)
del repository `sorrentinoluca/fot-tep-data`. L'archivio misura 144.904.704 byte e ha SHA-256
`0669aae7106d91f96068c25bd215968343bbd3e9ddff1db982e27573de063d81`.

La stessa release conserva gli output necessari a riprodurre i risultati numerici nel file
[`studio2-fase02-validation-v1.tar`](https://github.com/sorrentinoluca/fot-tep-data/releases/download/studio2-fase02-v1/studio2-fase02-validation-v1.tar):
140 workbook Philox definitivi, 10 workbook legacy autorevoli e i cinque manifest eseguiti;
281.648.128 byte, SHA-256
`d4143bdd3fa0d67c4e0e9e81496b6716242e381575b19fd9358209d652233fc9`.
Entrambi gli archivi mantengono percorsi relativi alla radice del repository sorgente e possono
essere estratti direttamente in una nuova clone dopo la verifica dell'impronta.

La copia remota è stata verificata scaricando nuovamente entrambi gli asset in una directory
temporanea separata: gli SHA-256 degli asset coincidono; dopo l'estrazione, 78 righe/74 contenuti
legacy e 5 manifest/150 output coincidono individualmente con dimensioni e SHA-256 dichiarati,
con zero mismatch. Il record machine-readable completo è
[`fase02/ARTIFACT_STORAGE.json`](fase02/ARTIFACT_STORAGE.json).

Stato del repository al momento della copia: `043e05bb296871ac2a0413d7115fb784b9fefe93`.
Questo identificatore descrive il contesto della conservazione, non è un tag di congelamento e non
contiene i workbook ignorati.

## 2. Origine e metadati disponibili

| Gruppo | Contenuti distinti | Origine verificata | Commit pertinente | Data di generazione | Seed / stato RNG | Destinazione | Modifiche | Stato nello studio 2 |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Cache del dataset — sviluppo, validazione, test e Normal | 42 | snapshot `mv-per/tennessee-eastman-dataset`; 46 copie locali confrontate per dimensione e SHA-256 con i puntatori LFS | `309b944f35ac440ff0c70616947ffe723c766e14` | **mancante**; la data del commit non è assunta come data di generazione | **mancante** | per SHA-256, §1 | copia byte per byte; nessuna trasformazione | conservato; solo R1/R2 sono candidati, §3 |
| Held-out PBH e altri fault batch 11 | 32 | simulatore isolato pre-setpoint; `MultiLoop_mode1`, MATLAB/Simulink R2025b, solver `ode45`; provenienza descritta dal manifest PBH e dalla nota di generazione | simulatore `a0413e16c940f0fc8b554d6a86248020d7fb7527`; i workbook non sono mai stati committati | timestamp locali tra 2026-08-28 e 2026-08-29; **l'istante di generazione non è registrato in un log firmato** | nessun seed manuale; **stato RNG effettivo mancante** | per SHA-256, §1 | copia byte per byte; nessun padding, troncamento o rigenerazione di F6 | conservato; nessun riuso autorizzato |

Per i 15 casi PBH, `phase_b/heldout/phase_b_heldout_manifest.csv` registra inoltre caso, classe
offline, batch, gruppo di generazione, configurazione del simulatore, dimensione, SHA-256 e controlli
meccanici. I 17 fault batch 11 rimanenti sono il complemento dei PBH nella stessa raccolta, non
un'ulteriore raccolta. Il seed dei 17, il `Ts_base` storico di N1–N5 e la disponibilità remota degli
oggetti LFS non sono stati recuperati: restano dichiarati mancanti e non vanno dedotti.

Nemmeno il commit del simulatore `a0413e16c940f0fc8b554d6a86248020d7fb7527` è presente
nell'object database Git locale. La provenienza resta quindi verificabile sulle impronte dei byte
locali registrate in `fase02/SIMULATOR_PROVENIENZA.md`, ma il legame con quel commit dichiarato non
è verificabile da questo checkout finché l'oggetto non viene recuperato.

## 3. Candidati al riuso e decisioni

| ID | Materiale | Contenuti | Ruolo proposto | Analisi che potrebbe usarlo | Marca rispetto all'uso del dato | Stato e condizioni |
| --- | --- | ---: | --- | --- | --- | --- |
| R1 | F1/F8/F10/F13, batch 1–5 in `code/tep_cache/` | 20 | sviluppo dei fault al posto di nuove simulazioni equivalenti | verifiche di compatibilità; materiale storico per ipotesi e rappresentazione | **pre-specificata** nel nuovo studio, ma usa dati già osservati | **respinto come sostituzione**: seed, data, `Ts_base` e identità della configurazione eseguita non sono ricostruibili; resta il solo uso storico già dichiarato |
| R2 | `code/tep_cache/mode1_normal_500.xlsx`, limitatamente ai blocchi continui N1–N5 | 1 workbook, 5 blocchi contigui | `baseline_fit` dello score | riferimenti per sensore, scelta A/A′ e parametri robusti; mai soglia o verifica | **pre-specificata** nel nuovo studio, ma non cieca rispetto al dato | **autorizzato condizionatamente come sola baseline**: guardia su 10 nuovi run superata; i blocchi restano contigui e non scambiabili coi nuovi run |

La marca **pre-specificata** descrive quando l'analisi proposta è stata definita nello studio 2;
non rende nuovi, indipendenti o non osservati i dati. Qualunque analisi scelta dopo averne esaminato
il contenuto dovrà invece essere registrata come **post-hoc**.

I restanti materiali conservati — validation/test storici, file Normal da 50 ore, 15 PBH e 17 fault
batch 11 — non ricevono qui un ruolo sperimentale. La conservazione impedisce la perdita; non li
promuove a sviluppo, calibrazione o test.

## 4. Usi effettivamente autorizzati

| ID uso | Origine e identità | Destinazione operativa | Trasformazioni | Ruolo | Marca e limiti |
| --- | --- | --- | --- | --- | --- |
| U1 / R2 | `code/tep_cache/mode1_normal_500.xlsx`; snapshot dichiarato `309b944f35ac440ff0c70616947ffe723c766e14`; SHA-256 `79883dd0aabbd034c15337b0be1ffca37e59ea7b32443a15d560b7feda2b2e6a` | parametri in `fase02/validation/score_fit_legacy.json`; copia recuperabile per SHA sotto `fase02/patrimonio_conservato/contenuti/` | segmentazione half-open in N1–N5 da 50 h; statistiche per sensore; feature in finestre da 5 h; fit robusto A | `baseline_fit` soltanto | pre-specificato ma su dati osservati; nessuna indipendenza; vietati `cal_thr`, `far_ver` e test; fallback esplicito se il congelamento o la verifica decadono |

R1 non compare fra gli usi autorizzati perché la sostituzione proposta è stata respinta. I venti
file fault possono restare consultabili nel ruolo storico già dichiarato dal piano, senza essere
contati come nuove repliche del secondo studio.
