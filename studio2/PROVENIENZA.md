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

**Nota di metodo sui workbook XLSX.** L'identità di contenuto di un workbook rigenerato si
verifica confrontando nomi e byte dei membri interni del contenitore ZIP, intestazioni, valori
IEEE-754 e, quando pertinente, stato o contatore finale del generatore. Non si richiede che il
contenitore XLSX rigenerato abbia lo stesso hash: i timestamp DOS degli entry ZIP cambiano a ogni
scrittura anche quando tutti i membri e i valori sono identici. La stessa distinzione vale per le
verifiche per riscaricamento della Fase 02: l'asset `.tar` scaricato deve conservare esattamente il
proprio SHA-256 pubblicato; per i workbook estratti, l'hash del file prova identità solo quando si
confronta la medesima copia pubblicata, mentre il confronto con una rigenerazione indipendente va
eseguito sul contenuto ZIP e sui valori. Il criterio è applicato e quantificato per il MEX fault in
[`fase03/fault_runs/MEX_RECORD.md`](fase03/fault_runs/MEX_RECORD.md).

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
| U2 / registrazione tardiva | `code/tep_features.py`; commit `3fd960a192bafacbaabce9471e3c3614d6b2d2db`; SHA-256 `cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c` | `studio2/fase02/analysis/tep_features.py` (commit `dec2010`, stessa impronta) | nessuna: copia byte-identica, inclusa in `fase02/validation/PRECALIBRATION_FREEZE.json` | feature per finestra dello score Normal | **pre-specificato** descrive l'uso originario in Fase 02; registrazione tardiva del 2026-09-13 nella sotto-fase 03.4; la copia congelata resta intatta come eccezione storica |

R1 non compare fra gli usi autorizzati perché la sostituzione proposta è stata respinta. I venti
file fault possono restare consultabili nel ruolo storico già dichiarato dal piano, senza essere
contati come nuove repliche del secondo studio.

U2 è registrato in §4, anziché fra i candidati, perché documenta un uso già avvenuto e congelato
nella Fase 02: questa registrazione tardiva non autorizza nuovi import, non modifica la copia e non
trasforma il valore operativo `window_h=5.0` in una decisione per le fasi successive.

## 5. Fase 03.0 — Provenienza degli adattamenti del capability pilot

Questo registro segue `docs/MAINTENANCE.md` §8.2. Gli artefatti elencati sono letti in sola
lettura; gli adattamenti vivono sotto `studio2/`.

| Origine | Commit | SHA-256 | Destinazione | Modifiche | Ruolo | Marca |
| --- | --- | --- | --- | --- | --- | --- |
| `phase_b/exp2/qwen/adapter.py` | `9e3d9031013788a583e348fbd7bfc40e14d3c68b` | `49de085165f9aad99b17fa7713c0aae5fffded535cccda5dd508d7b65fef6bcf` | `studio2/fase03/run_pilot.py` | adattamento a 8 agenti, 14 insight, logging di latenza/fingerprint e guardia esplicita di esecuzione | pattern dell'adapter OpenAI-compatible locale | pre-specificato |
| `phase_b/exp2/qwen/capability_probe.py` | `9e3d9031013788a583e348fbd7bfc40e14d3c68b` | `b383611d4c7c7bd55215c0458827efec63ca0261264ed737ee05c8ba2a5f9dcd` | `studio2/fase03/prepare_gate.py`, `studio2/fase03/run_pilot.py` | separazione obbligatoria fra controllo budget e gate; campione 40×3; nessun accesso al test | pattern di capability probe e contabilità richieste | pre-specificato |
| `phase_b/conditions/parser.py` | `9e3d9031013788a583e348fbd7bfc40e14d3c68b` | `bdddfe99ba6e4328a071ea94c221a91cc5942252865691a280bcd6687301eb99` | `studio2/fase03/protocol.py` | parser autonomo per nove label e massimo 14 insight | parsing JSON stretto | pre-specificato |
| `phase_b/insights/library.py` | `9e3d9031013788a583e348fbd7bfc40e14d3c68b` | `679f2074067f13c29f63237e25dd0c86a979d48232ecf0c333cf8e7e41fe93c9` | `studio2/fase03/protocol.py`, `studio2/fase03/producer_probe.py` | estensione a 8 agenti; campi fissi, identificatori di variabile e cap per elemento | validazione libreria, controllo E a campo singolo e sonda producer | pre-specificato |
| `phase_b/c06/prompts/B_LOCAL_FIRST_V1.txt` | `9e3d9031013788a583e348fbd7bfc40e14d3c68b` | `4e6cc81f87033f0b3bcddebff694e7f446e31c228c5ac1f7560b9552aada6192` | `studio2/fase03/protocol.py` | blocco decisionale riusato per B-LF ed E-LF; label e insight resi parametrici | politica local-first congelata | pre-specificato |
| `phase_b/exp2/qwen/config.json` e risultati congelati della sensitivity descritti in walkthrough v2 §10.1–10.2 | `9e3d9031013788a583e348fbd7bfc40e14d3c68b` | `3b58e321c5d09c8e1fdf2f5ddab6bac14f9b537b0febcc294909164f3febcbe9` | `studio2/fase03/config/pilot_preflight.json` | vecchi valori 4096/1024 non ereditati; usati solo per definire la scala 2048/3072/4096 da verificare prima del gate | precedente operativo sullo stesso Qwen-27B | pre-specificato |

Il rebase su `origin/main` `c6e19d646cfdb1fd73ad2d537c167656f0bd8038` ha sincronizzato il
report e la verifica di chiusura della Fase 02 e il freeze pre-calibrazione. Le rispettive impronte
sono registrate in `fase03/config/pilot_preflight.json`; il freeze dichiara
`source_head_commit=d472dc56c41f2b07563a362b81eed844460bf1c7`. Le sezioni 1–4 sopra sono
state conservate intatte nella risoluzione del rebase.

La pubblicazione sblocca quindi identità, manifest e hash degli artefatti che la Fase 02 dichiara
conclusi; non crea ciò che il report colloca in «Fuori dalla Fase02». Catalogo definitivo, 40 nuovi
run fault di sviluppo e relative feature/evidence restano prerequisiti scientifici futuri. Quando
esisteranno, ogni artefatto effettivamente usato dal pilot riceverà una riga autonoma con origine,
commit, impronta e destinazione. Il producer alternativo resta privo di configurazione e non può
ancora ricevere una riga di provenienza né superare la sonda di conformità.

## 6. Fase 03 — D1: fonti usate per l'estrazione del catalogo

L'estrazione D1 del 2026-09-13 non riusa dati, run o risultati del primo studio: la continuità
F1/F8/F10/F13 è un vincolo del piano, non un dato. Le fonti effettivamente usate sono le seguenti;
l'analisi è **pre-specificata** (procedura §5 del registro, congelata prima del sorteggio) e
nessun risultato per-fault dei nostri esperimenti è stato aperto.

| Fonte | Identità | SHA-256 | Ruolo in D1 | Marca |
| --- | --- | --- | --- | --- |
| `docs/lit_review/DECISIONE_CRITERI_SELEZIONE_FAULT_STUDIO2.md` (rev. 1) | tag `studio2-fase03-criteri-selezione-frozen-001`, commit `9faecaf`, source `9d0e191` | `d58a7606d69a560a626da44833c065ddbf1aa395ae8b2e523262daf8622231c7` | universo, attributi (tabella 8 trascritta in §2), strato H, vincoli §4, procedura §5 | pre-specificato |
| `studio2/fase03/selection/CRITERIA_FREEZE.json` (rev. 1) | idem | `ecae57172d6a83d8b0943f5a9f47b49a3966b96e2fb47f807a9ff61449755c9b` | attestazione del congelamento, `d1_draw_executed=false` al via | pre-specificato |
| `studio2/fase03/selection/FEASIBILITY.json` | idem | `ca830d054af19e27aa191fcb51f8e80d3c8444bb746dd9da486304490bd59810` | conteggio atteso 330/12, riprodotto indipendentemente | pre-specificato |
| Downs & Vogel 1993, tabella 8 p. 250 | copia primaria registrata in `SOURCE_CHECK.json` | `5f19b0bf7f0e5c052335943fff263769a28757066582c3166e16ac163e0e9538` (PDF) | meccanismo e variabile perturbata, **via la trascrizione del registro §2** (non riscaricato in D1) | esterno, preesistente |
| Xiao, Kordon & Sen, PHM 2023, tabella 2 e §4.3 | copia primaria registrata in `SOURCE_CHECK.json` | `e11310c44cebca7a6ebc368b3862dc2edc0003a4ee31cb9223feb6d5e0ae7b78` (PDF) | strato H nominale, **via il registro §3** (non riscaricato in D1) | esterno, preesistente |
| `docs/paper/FoT_TEP_Review_Piano_Sperimentale.md` | snapshot al source commit `9d0e191`, invariato a `9faecaf` | `7f9462c28eef7bc0cf74e201a1ffe283d68056359728fea62740e43a1bb1767a` | D1, §6.1, §0.1, §12.1–12.4 per contesto; §8.3/§8.6/D11 solo per la proposta non vincolante | pre-specificato |

Esito e impronte dell'estrazione: `fase03/selection/D1_DRAW_LOG.json`, `CATALOG_FREEZE.json`,
`CRITERIA_FREEZE_rev002.json` e `REPORT_CATALOGO_D1.md`. Il catalogo estratto è
{F1, F2, F3, F8, F10, F13, F14, F15}; il congelamento diventa efficace solo con verifica
indipendente, commit raggiungibile da `origin/main` e tag dedicato.


**Pubblicazione D1, 2026-09-13.** Le condizioni sono soddisfatte: il tag annotato
`studio2-fase03-catalogo-D1-frozen-001` (oggetto `b6828afc3062e1e6371376638c42eab529635e32`)
punta a `ab43f0b20f45cdb475c0caf52c6f7afcbae50891`, verificato su `origin/main`.
L'[attestazione](fase03/selection/CATALOG_PUBLICATION.json) conserva le impronte dei 16 file
della consegna nel tag. I manifest e i verbali restano intatti come snapshot precedente alla
pubblicazione; lo stato efficace è `catalog_frozen=true`. Non sono stati aggiunti dati riusati,
nuovi sorteggi o autorizzazioni per run, OOD e D11.


## 7. Fase 03 — specifica dei nuovi run fault (§6.2)

Data 2026-09-13; base verificata `9ec87791dd79b82893dc09568bd8c47fdd154c50`.
Riuso di convenzioni e codice, non dei workbook o risultati fault storici. La destinazione
è `fase03/fault_runs/`; ogni analisi e adattamento qui progettato è **pre-specificato**
rispetto ai nuovi run. Nessun uso post-hoc di valori per-fault per scegliere il protocollo.

| Origine | Commit verificato | SHA-256 | Adattamento e ruolo | Marca |
| --- | --- | --- | --- | --- |
| `docs/fot_walkthrough_conversazione.md` | `9ec87791dd79b82893dc09568bd8c47fdd154c50` | `fb9de573a903f3d8c599cc51fdfbf5d9f8df79b44d34617d95fdd68bd30fa3d6` | convenzione storica 40 h post-fault, otto finestre half-open; traslazione da 10 a 25 h | pre-specificato |
| `docs/fot_walkthrough_conversazione_v2.md` | `9ec87791dd79b82893dc09568bd8c47fdd154c50` | `ec64e1f5d754cafc144f54e5136bba86daa165b158f7957693187e2018fbda2b` | conferma narrativa della convenzione; esposizione incidentale dichiarata sotto | pre-specificato |
| `code/tep_characterize_v2.py` | `9ec87791dd79b82893dc09568bd8c47fdd154c50` | `440b2488b30144944e52ad27f21f53eede781550efdef5a1f6251cf8e2630560` | costanti 10/50/5 e chiamata analyze_case_windows verificate; nuovo onset 25 e stop 65 | pre-specificato |
| `studio2/fase02/simulator/matlab/generate_normal_runs.m` | `9ec87791dd79b82893dc09568bd8c47fdd154c50` | `923d657608f5bbf30869c8cdf2772dd5cacd2a98b4ef62dc85540dc812eda837` | launcher gemello con manifest per tentativo, protezione destinazione, gestione trip e log | pre-specificato |
| `studio2/fase02/build_generation_plan.py` | `9ec87791dd79b82893dc09568bd8c47fdd154c50` | `6d8f5c458eae0fe215d89bcc6564fe077c09187d1dd6a4863ef1269970772951` | generatore gemello con prenotazione 30000–30040 e seed descritti come coppia chiave/stream | pre-specificato |
| `studio2/fase02/simulator/source/temexd_philox.c` | `9ec87791dd79b82893dc09568bd8c47fdd154c50` | `230086e7712e753bf48f3e9108cd0ce2f68aba97d9590ebb3c7593a47f8b6d25` | copia strumentata per IDV, variabili perturbate e trip; equazioni e RNG preservati | pre-specificato |

Le ulteriori dipendenze di Fase 02, il catalogo al tag e tutti i manifest letti sono
identificati in [SOURCE_AUDIT.json](fase03/fault_runs/SOURCE_AUDIT.json), con SHA-256 e
commit. Sono riusati come input di configurazione e provenienza; marca **pre-specificato**.
Il modello e gli init restano invariati su disco; le sole modifiche operative del modello
sono registrate dal nuovo launcher. `auto_run.m`, `generate_phaseB_extra_runs.m` e il modello
storico in `tep_parent_a0413e16/` sono stati aperti: confermano il pattern di IDV singolo e
il ritardo configurato di 10 h. I loro hash locali sono nel medesimo audit; il collegamento
al commit dichiarato `a0413e16…` resta non verificabile perché l'oggetto non è disponibile.
Il sorgente di caratterizzazione tracciato alla base costituisce il riscontro verificabile
della convenzione 10/50/5. Nessuna simulazione storica è stata rieseguita.

**Esposizione incidentale, dichiarazione di processo.** Nella lettura iniziale della v2
§2, un intervallo troppo ampio ha incluso la tabella narrativa di risultati per-fault
(similarità intra-classe, margini e commenti). Nessun suo valore è stato usato per catalogo,
innesco, orizzonte, indici, finestre, criteri o smoke. Non sono stati aperti i corrispondenti
artefatti numerici per-fault. Le sezioni operative richieste della prima esposizione
contengono inoltre esempi numerici narrativi; l'output iniziale non filtrato del test
documentale ha incorporato estratti storici nei messaggi di assert. Anche questi valori
non hanno alimentato alcuna scelta. I successivi test documentali vengono letti soltanto
per nomi e conteggi. Si dichiara l'esposizione, senza rivendicare cecità assoluta.

**Decisioni dell'autore prima dei nuovi dati.** Approvati un solo IDV per run (anche
F14/F15), nessuna perturbazione aggiuntiva o variazione di setpoint; deviazione esplicita
dalla raccomandazione Downs & Vogel, pp. 250–251. Innesco 25 h, burn-in qualificato 20 h,
controllo negativo interno [20,25) escluso da insight/prototipi, 40 h post-fault e otto
finestre fino a 65 h. Segnale debole/assente e trip si conservano: niente estensioni,
perturbazioni o sostituzioni dopo osservazione. Lo smoke unico è F1/stream 30040,
25.1 h totali, senza finestre post-fault complete. Marca **pre-specificato**.
La specifica contiene anche i limiti da dichiarare nel futuro paper.

## 8. Fase 03 — run fault di sviluppo e conservazione

La campagna `fault_dev_001` contiene 40 nuove simulazioni: F1/F2/F3/F8/F10/F13/F14/F15,
cinque batch per fault, indici e stream Philox 30000–30039. Tutti i manifest riportano come
commit di esecuzione `49d58064efb25566e866ffdf9df8da3dd66116cf`; la specifica pre-esecuzione
era già registrata al commit `c02111d132f3cc1c047d5c4ed112398724138e3f`. Il piano eseguito
ha SHA-256 `583f4316f3788abd23f687e19ba9494aa44087a7ce2c6b0c8263eec9147aa178` e la
specifica originale SHA-256 `14d36742c158b1ca71b1adc848d13d6f7a85107530450b19a3e1d122eb063b2e`.

| Origine | Commit / identità | Impronta | Destinazione e ruolo | Marca |
| --- | --- | --- | --- | --- |
| Piano `fase03/fault_runs/plans/fault_dev.csv` e specifica pre-esecuzione | specifica `c02111d`; esecuzione registrata `49d5806` | piano `583f4316…`; specifica `14d36742…` | `fase03/fault_runs/runs/fault_dev_001/`; 40 run per sviluppo soltanto | pre-specificato |
| Manifest aggregato dei file conservati | derivato in sola lettura dai 40 manifest per-run | `MANIFEST_FAULT_DEV.csv` SHA-256 `9eaed0e901c6f06d5aa94b4e2d81d5afdd3464022ae6d2709b92f872789a6d9d` | controllo di 200 output/diagnostiche/log/manifest/attempt | documentazione post-esecuzione, nessuna selezione |
| MEX strumentato fault | sorgente base `230086e…`; sorgente strumentato `74bf641b…`; ambiente in `MEX_RECORD.md` | binario `834e2361915249402a1ec9074a4be04f22a6404deb841e5134bf34347dfde544` | diagnostica IDV, variabili interne e trip; uscite numeriche equivalenti al MEX base | strumentazione pre-specificata; equivalenza verificata post-esecuzione |
| Archivio pubblico della campagna | repository `sorrentinoluca/fot-tep-data`, commit release `6d238929285e57c6c70f4d563ef7e30b59da6ac5` | 208.257.536 byte; SHA-256 `6edd96711d2913953c6de81ce6dbb7c51e7677a2a7c1892b0676de5e7a9fd97c` | recuperabilità dei run, del tentativo abortito e delle prove MEX | conservazione, nessuna promozione analitica |
| Archivio pubblico della campagna, rev002 | repository `sorrentinoluca/fot-tep-data`, commit release `6d238929285e57c6c70f4d563ef7e30b59da6ac5` | 5.683.200 byte; SHA-256 `5940fd417149d3ff92ee4c3d4f7826b80cb2b58b066eb2213b4ce38ac32a2527` | sorgente e binario del MEX strumentato, log/pid del lancio riuscito, replay MATLAB F1/30000 (20 file, non nell'asset v1) | conservazione, nessuna promozione analitica |

La release pubblica è
[`studio2-fase03-fault-dev-v1`](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-fault-dev-v1);
l'asset diretto è
[`studio2-fase03-fault-dev-v1.tar`](https://github.com/sorrentinoluca/fot-tep-data/releases/download/studio2-fase03-fault-dev-v1/studio2-fase03-fault-dev-v1.tar).
La copia remota è stata verificata riscaricando l'asset in `/tmp`, fuori dal repository:
SHA-256 dell'archivio coincidente e 240/240 file estratti uguali per percorso, byte e SHA-256,
con zero mismatch. Il dettaglio machine-readable è in
[`fase03/fault_runs/ARTIFACT_STORAGE.json`](fase03/fault_runs/ARTIFACT_STORAGE.json); la mappa
dei file è `fase03/fault_runs/MANIFEST_CONSERVAZIONE.csv`.
La release [`studio2-fase03-fault-dev-v2`](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-fault-dev-v2), verificata allo stesso modo, aggiunge sorgente e binario del MEX strumentato, `matlab.log`/`matlab.pid` del lancio riuscito e la directory del replay, senza riscrivere l'asset v1 (`6edd…`); gli script MATLAB delle prove di equivalenza e del replay restano non recuperabili, dichiarati assenti. Dettaglio in `ARTIFACT_STORAGE.json` (`schema_version` 2, `releases[]`) e `fase03/fault_runs/MANIFEST_CONSERVAZIONE_rev002.csv`.

Il primo tentativo di lancio, terminato dalla sandbox mentre il processo era in background,
non ha prodotto run; il log vuoto e il PID sono conservati come evidenza separata. Il rilancio
da terminale esterno ha mantenuto invariati piano, indici e stream. L'esito è 40/40 `complete`,
zero trip e 320 finestre post-fault complete. Questi dati ricevono il solo ruolo di sviluppo:
non sono ancora stati trasformati in feature, evidence, verbalizzazioni, insight, prototipi o
calibrazione e non costituiscono materiale di test.

## 9. Fase 03 — sotto-fase 03.7: pseudolabel, assegnazione degli agenti e derangement di E (§6.5)

Questo registro segue `docs/MAINTENANCE.md` §8.2. L'unico elemento del primo studio riusato è un
**pattern di codice**, letto in sola lettura e riscritto in `studio2/`; nessun dato, soglia, insight
o risultato del primo studio entra in questa sotto-fase. Nessun import da `phase_b/`.

| Origine | Commit | SHA-256 | Destinazione | Modifiche | Ruolo | Marca |
| --- | --- | --- | --- | --- | --- | --- |
| `phase_b/config/protocol.py`, funzione `derive_opaque_pseudolabel` (SHA-256 di namespace+identificatore, base32, prefisso, 5 caratteri) | `c431cd87ee0ef563ad77cc6b0b330e6b61bf9735` | `fa2488d1d964c98682c3fc82d650bbe43d74a3f9f041e5745ca71a51331e7b2e` | `studio2/fase03/pseudolabel/pseudolabel_draw.py` (`label_message`, `candidate_suffix`, `derive_labels`) | prefisso `S2-CLS-` e regex di `studio2/fase03/protocol.py`; messaggio con separatori e contatore di collisione `namespace|label|identifier|counter`; guardia di opacità sulle cifre dell'idv; `Normal` letterale in ultima posizione; nessun import | pattern di derivazione delle label opache | pre-specificato (`SPECIFICA_PSEUDOLABEL.md` §3, scritta prima dell'esecuzione) |
| `phase_b/config/evaluator_side/condition_e_derangements.json` (forma dell'artefatto a 4 agenti, rotazione di un passo) | `c431cd87ee0ef563ad77cc6b0b330e6b61bf9735` | `e8a0bdbf5a0b7c04d1ba978fd7e18f55b933d8062125ea11c1fb117f9990b231` | `studio2/fase03/pseudolabel/CONDITION_E_DERANGEMENTS.json` | 8 agenti e 7 peer; la rotazione fissa è sostituita da un derangement campionato uniformemente fra i 1854 con seed dichiarato; forma `pseudolabel → pseudolabel` per agente coerente con `protocol._validate_derangements` | forma dell'artefatto evaluator-side | pre-specificato (`SPECIFICA_PSEUDOLABEL.md` §5) |

Input scientifico della sotto-fase: il catalogo D1 al tag `studio2-fase03-catalogo-D1-frozen-001`
(commit `ab43f0b20f45cdb475c0caf52c6f7afcbae50891`, `CATALOG_FREEZE.json` SHA-256
`68b8461a6382c93e1a5dd8dc6c9def66b26b2ec865f0bc0786dd88fa95acedda`), verificato dal generatore
prima di ogni derivazione. Artefatti, impronte e stato di congelamento sono in
`fase03/pseudolabel/PSEUDOLABEL_FREEZE.json` (`frozen_pending_independent_verification`, nessun
tag). Il mapping pseudolabel↔fault e l'assegnazione agli agenti sono evaluator-side e non entrano
in alcun prompt.

## 10. Fase 03 — soglie Normal (§6.3)

La sotto-fase 03.5 usa U1/R2 esclusivamente come `baseline_fit` N1–N5, con score A e parametri
congelati in `fase02/validation/score_fit_legacy.json`; guardia R2 superata e ricontrollata.
I nuovi lotti sono pre-specificati: `cal_thr` 350 run, stream 40000–40349, e `far_ver` 150 run,
stream 50000–50149. Il piano, il freeze e gli output sono identificati dai manifest e dalle
impronte in `fase03/soglie_normal/`.

Il freeze della soglia è stato eseguito prima dell'apertura analitica di `far_ver`, al commit
`9507143`: soglia `13.623626738268857`, rango 334, n=350, regola `S > threshold`. Il codice di
score è quello Fase 02; la soglia, il lotto e il sigillo dei 150 file sono in
`fase03/soglie_normal/THRESHOLD_FREEZE.json`. L'analisi FAR è stata eseguita dopo il freeze,
senza modifica della soglia: `11/150` primari e `108/1500` secondari.

| Artefatto | Identità | Ruolo | Marca |
| --- | --- | --- | --- |
| `fase03/soglie_normal/plans/cal_thr.csv` e `far_ver.csv` | piani SHA-256 nei manifest | allocazione e stream disgiunti | pre-specificato |
| `fase03/soglie_normal/CAL_THR_SCORES.csv` | SHA-256 `a1c5991af1ee136372b1da7c63ab05027d9710fd99c228a549395964d5519191` | calibrazione della soglia | pre-specificato |
| `fase03/soglie_normal/THRESHOLD_FREEZE.json` | commit `9507143`; soglia e sigillo `far_ver` | freeze prima della verifica | pre-specificato / post-esecuzione |
| `fase03/soglie_normal/FAR_VERIFICATION.json` | analisi a soglia immutata | FAR primario, secondario e diagnostica | pre-specificato |
| release `studio2-fase03-normal-v1` | archivio SHA-256 `bbcfd0c43a5fbda624deba62fea746150dda4a6d649e6372b8e118270277ac1d` | conservazione, 515 file | post-esecuzione |

L'archivio pubblico è stato riscaricato e verificato: 515/515 file, zero mismatch. Dettagli e
URL sono in `fase03/soglie_normal/ARTIFACT_STORAGE.json`. Il batch è stato lanciato prima del
freeze, come previsto dall'handoff operativo, che richiedeva il congelamento prima di aprire
le finestre `far_ver` e non vietava la loro generazione anticipata. Le tracce accessibili
documentano hash/manifest prima del freeze e apertura analitica successiva; gli score FAR
scientifici registrati compaiono dopo il freeze, mentre quelli precedenti rintracciati sono
degli smoke esclusi (stream 49900–49901). La disponibilità anticipata dei file è un limite di
segregazione operativa: sigilli e storia Git provano identità e sequenza registrata, non
escludono consultazioni umane o da processi non registrati. L'accettazione scientifica di questo
limite rimane una decisione dell'autore; non è implicita nella correzione del report.

### 10.1 Completamento C4 dopo la verifica del candidato 819b12e

Il 2026-09-14 l'autore ha richiesto di correggere il report e completare l'incertezza della
soglia. Il requisito C4 era pre-specificato nel registro rev. 19; seed, numero di repliche e
convenzione dell'intervallo sono invece scelte operative **post-hoc rispetto ai risultati**,
registrate prima di questo ricalcolo supplementare. Non si rivendica una scelta cieca e non
si modifica la soglia operativa. Esecutore: `gpt-6-astra`, finestra
`01a09f81-e508-77e0-b510-872bdeba46e3`, ora incaricata della correzione e non della sua
certificazione indipendente.

| Origine / identità | Destinazione | Ruolo e trasformazione | Marca |
|---|---|---|---|
| `CAL_THR_SCORES.csv`, candidato `819b12e97fb94d501032655ec2f226139e6c5ca5`, SHA-256 `a1c5991af1ee136372b1da7c63ab05027d9710fd99c228a549395964d5519191` | `fase03/soglie_normal/THRESHOLD_UNCERTAINTY.json` | diagnostica completa dei pareggi; 10.000 bootstrap di 350 run, rango 334, seed 20260914, percentile95%; score fit fisso | completamento C4 richiesto prima dei dati, dettagli operativi definiti dopo i risultati |
| `THRESHOLD_FREEZE.json`, introdotto in `950714389f92e559eac922a09404742a71c74346`, SHA-256 `ff5c27002a2548003e4bc5f54805cda3754fb19b9cb2559222996b9c7f7e14a9` | stesso risultato supplementare | controllo n/rango/soglia/regola e Beta(17,334) condizionata alle ipotesi; nessuna soglia sostitutiva | rendicontazione supplementare, nessuna nuova calibrazione operativa |
| `THRESHOLD_UNCERTAINTY_PROTOCOL.json`, SHA-256 `711d9711587fd140dcb451ccbe48b42d35fdf1bc3043feb5fb5e6dea3921989b` | `complete_threshold_uncertainty.py` e risultato JSON | parametri del nuovo bootstrap fissati prima del ricalcolo; impronte verificate prima/dopo | protocollo post-esito, non preregistrazione cieca |

Il risultato contiene impronte complete di codice, protocollo e input, ambiente e data.
Nuovi file piccoli destinati a Git nella revisione correttiva, ancora non committata;
non sono già inclusi nella release `studio2-fase03-normal-v1`. Il vecchio manifest e la
release restano invariati e descrivono i loro snapshot; il report conservato nell'asset è
quello pre-chiusura, non questa revisione. U1/R2 non riceve alcun nuovo ruolo e i suoi
parametri non sono rifittati.

### 10.2 Integrazione e consegna del 2026-09-14

Le descrizioni precedenti conservano il loro stato storico. La decisione FAR è ora
registrata in `fase03/soglie_normal/DECISIONE_AUTORE_FAR.md`; C4, verbali e report sono
integrati in `origin/main` con merge `98d958d870a10ada0d095893af9edb05a68ebc67`.
Tag di consegna pubblicato: `studio2-fase03-soglie-normal-frozen-001`. Il freeze storico
della soglia e la release normal-v1 restano invariati. La 03.5 è chiusa; la Fase 03 resta
aperta. Dettagli e distinzione fra tag di consegna e freeze scientifico in
`fase03/soglie_normal/INTEGRAZIONE_03_5.md`.

## 11. Fase 03 — sotto-fase 03.9: `normal_dev` e baseline numerica

Data 2026-09-14. Specifica, piano, stream, finestre, regola di selezione degli esempi locali e
algoritmo dei prototipi erano **pre-specificati** rispetto alla generazione. Audit, ispezione del
warning e decisione di accettazione sono invece documenti post-esecuzione, descrittivi e non
possono essere usati per retrodatare le scelte.

| Origine | Commit / identità | SHA-256 | Destinazione e modifiche | Ruolo | Marca |
| --- | --- | --- | --- | --- | --- |
| Piano rev. 7, §6.2 | `a572d1c8a9a1cecc7bf7a6abfe814a93ca19c155` | `f3959866f1b45e3ef91e8b924436408fa512ed610bea4684aedfd90f4d2bf3ca` | `fase03/baseline_numerica/SPECIFICA_NORMAL_DEV.md`, piano 40 run/60000–60039 e handoff storico; nessuna copia del piano | fonte della decisione `normal_dev` | pre-specificato; `origin/main` contiene ora la revisione, ma l'audit non attesta lo stato del ref remoto al momento del lancio e l'OK dell'autore non autorizza una deroga a quel prerequisito |
| Generatore Normal qualificato | `studio2/fase02/simulator/matlab/generate_normal_runs.m`, commit `dec201092b6404c7a2d83cdcfa5ed13cc03f7775` | `923d657608f5bbf30869c8cdf2772dd5cacd2a98b4ef62dc85540dc812eda837` | `generate_normal_dev_runs.m` (SHA-256 `ec169e76b05694d3ea038fd3eedcc2f92b28f56ac18c2cf383d85d37911b47ee`) delega senza cambiare modello, MEX, RNG o scrittura | generazione dei 40 Normal | codice e piano pre-specificati; comando effettivo/MATLABPATH non registrati dal manifest e accettati come limite di tracciabilità |
| Lotto `normal_dev_001` | 40 workbook; log MATLAB SHA-256 `983d4f3e54395078820df7b44d094823e99f2f856c47bb5d8a87df0ade2fb31d` | audit JSON `fb44c26ceaf3b045fe16902296bc3e01219acff7f7fac969c106369c7b48937f`; inventario conservazione `198b572ab1f0e600f34c182c2dba98427a3a3cbc56faf13f146187de4d914283` | `AUDIT_NORMAL_DEV.*`, `SIMULATOR_WARNING_CHECK.json`, candidato locale di conservazione | input reale Normal di sviluppo | post-esecuzione: integrità/configurazione **PASS** 40/40 e 320/320; l'autore ha accettato il pathname riusato e la lacuna comando/MATLABPATH, che restano registrati. Lo stato di `origin/main` al lancio non è attestato né coperto dall'OK |
| Modello Simulink qualificato | `studio2/fase02/simulator/matlab/MultiLoop_mode1.mdl` | `c58826748edd306b723da2f0199a0fb2dc193a51dc5c28dbde8ac821e39dfafd` | ispezione statica del blocco `Variable Time Delay` e del log; nessuna nuova simulazione | valutazione del warning di buffer | post-esecuzione: accettabile solo per questo lotto in modalità normal; nessuna estensione a ERT/GRT o validità scientifica generale |
| Evidence 03.6 | commit esterno `c66bd8dddf8e2af9dd0665ee30afd36c248b93fb`; release preferita `studio2-fase03-evidence-v2` | manifest scientifico `5111d0c61c2e93fe5071d7a85015673549af0bf9c1dc74e0d940719a8400e020`; archivio v2 `6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf` | `baseline.py` legge le 320 firme fault già pubblicate; l'estrattore Normal riusa le stesse funzioni verificate | firme fault e contratto di estrazione Normal | la v2 sostituisce il solo packaging v1 mantenendo identici 1283 file scientifici e manifest |
| Estrattore/leakage 03.6 | `extract_evidence.py` e `leakage.py` dalla worktree evidence | `46b451c2d6d8b1627993828ac9bac39532562f2fa1b27955b8a20f098ba24e97`; `c77ae5b11186c5b0df87b2f1df8800cb45fb25317e248fe8484d3e8283073887` | `extract_normal_evidence.py` verifica gli hash e scrive nella destinazione nuova `evidence/normal_dev_002` | riuso di codice congelato per 320 evidence Normal | post-esecuzione; la destinazione riuscita non sovrascrive il pathname accettato del lotto grezzo. Note di sessione menzionano due tentativi parziali rimossi, ma non ne è stata conservata una traccia primaria e il fatto non è usato come prova |
| N1–N5 + soglie V2, uso U3 | baseline SHA-256 `79883dd0aabbd034c15337b0be1ffca37e59ea7b32443a15d560b7feda2b2e6a`; guardia R2 `7df0cef2d7854c689b79eb911fa01d1ede1625e22f0d3636c0ea5d678c9f33f8` | manifest evidence Normal `cc8d96c2c60169afc99cb811cea194aa553afcc7cc51cad4a0092d44de38fdc1`; indice evaluator `4f340a0e24e809a5d16d783b561262826fae08afb143bde81d410ae103f55329` | nuova destinazione operativa U3: `normal_dev` → evidence Normal per prototipi ed esempi locali; nessun uso come osservazioni di sviluppo di N1–N5 | normalizzazione e flag V2 congelati | uso pre-specificato; estrazione post-esecuzione; se R2 decade, rigenerare; vietati fit, calibrazione, FAR e test |
| Pattern C02B `run_baseline.py` e freeze | commit d'origine `72af2a7ffa97544ec10cc6d0e6c65253e21de22c` | codice `5a0d4572ba8f8ac462abba3da1f72af780751fc3652c934cf8096f3dbb452bfa`; manifest `09c507a42417adb5c3dd88509bf8723d12a0599d4511ab50ab7b27ed73d8ca6c` | `baseline.py`: media su finestre fissate, L1 media, pareggio `1e-12`, separazione predizione/verità; estensione a 8 agenti e 9 classi | pattern implementativo, nessun dato o risultato riusato | pre-specificato |
| Prototipi numerici | `baseline.py` SHA-256 `b1fe2a83b29b25760dd32df00a2178c5235f714273a194feb6cfe8a12ac74f22` | `PROTOTYPES.json` `6d0b754065eb8a69d0657638deeef0756de0ec8e93a905c55aea18fadace2cb2`; manifest `8309a914d2141da38d1120606897bcead40142829ecd541b6b0423d0d9465751` | nove prototipi globali e sedici locali, tutti da development evidence | baseline numerica effettiva | post-esecuzione; ricalcolo Decimal(50), 25/25 vettori e differenza massima 0; nessun dato di test aperto |
| Piano statistico 03.8 e harness 03.10 | piano rev. 9 al commit `526561feabeb6b4083170b1817b8abdac1a2a4c7`, harness `51160872906feaa63c1fda5e9cf6e0fe8538fb16` | piano `e8059a8cc57c5727df63358cb2b3a8f8e7d231e18b4342f1caaa0ea9c1b49f03`; metriche harness `f3edc0719e8e2bf7aeca0a1e60e79c8365bf5cb633a31bd8a4f126cc93ddd1e9` | righe evaluator-side compatibili; handoff degli otto esempi Normal verificato sul parser 03.10; mapping dei nomi `accuracy`/`accuracy_all`, `n`/`total`, `abstentions`/`abstained` ancora da integrare | interoperabilità con braccio LLM | controllo post-esecuzione; integrazione 03.10 **pending**, nessuna modifica alla relativa branch |

Il lotto `normal_dev` separa le osservazioni Normal di sviluppo dai dati che definiscono la
trasformazione, ma non rende indipendente la trasformazione stessa: ogni nuova firma continua a
dipendere dalla coppia N1–N5/soglie V2 attraverso U3. I 320 Normal contro 40 finestre per ciascun
fault sono passati alla 03.14 come vincolo di sbilanciamento da risolvere prima
dell'addestramento, senza scegliere qui la soluzione. L'archivio di conservazione è verificato
localmente ma non è ancora pubblicato né riscaricato; `origin/main`, tag e freeze efficace restano
quindi pending.

### 11.1 Integrazione e conservazione del 2026-09-14

Aggiornamento successivo al candidato descritto sopra: il merge
`5bd1648c54a0673ebd66df3655cf8258dfa48d3b` è pubblicato in `origin/main`; la release
`studio2-fase03-normal-dev-v1` conserva l’archivio originale, senza rigenerarlo.
Riscaricamento: 1.336/1.336 file e 150.575.225 byte di contenuto, zero mismatch, extra,
AppleDouble o PAX. Impronta dell’archivio invariata: `eef69b42d8506c993ac45d77208df982d138b4354d7d4134bd67ba421dc91a03`.
I metadati aggiornati e la prova sono in `fase03/baseline_numerica/ARTIFACT_STORAGE.json`
e `VERIFICA_RISCARICAMENTO_NORMAL_DEV.json`. La rev. 3 del manifest mantiene
`effective=false`: restano raccordo con 03.10, raggiungibilità in main dei sorgenti
riusati di 03.6 e successivo tag della baseline. Il tag della release dati non li sostituisce.
## 12. Fase 03 — sotto-fase 03.12: schema degli insight (§6.10)

Data 2026-09-13. Uso **pre-specificato** prima di qualsiasi insight dello studio 2.
Confronto implementativo in sola lettura e riscrittura dei controlli in
`studio2/fase03/schema_insight/validator.py` e `leakage_rules_v1.json`; nessun import da phase_b,
nessun dato, insight o risultato sperimentale riusato. Il confronto storico non è fonte scientifica.
Lo schema del primo studio ha cinque campi e quattro agenti: non ne si ereditano cardinalità
né default. Lo scanner è riscritto per D1 e per meccanismi/identificatori fisici.

| Origine | Commit letto | SHA-256 |
| --- | --- | --- |
| `phase_b/insights/insight.schema.json` | `d815ce96d928254de79209f02e11a561445764cd` | `c3020aed97db6e9722661e04c2498c280f2d6cc10cdc6f364a14727200298fae` |
| `phase_b/insights/library.py` | `d815ce96d928254de79209f02e11a561445764cd` | `679f2074067f13c29f63237e25dd0c86a979d48232ecf0c333cf8e7e41fe93c9` |
| `phase_b/prompts/leakage.py` | `d815ce96d928254de79209f02e11a561445764cd` | `da1a39c72d36d7c04d276097d2de4c57fecb94642027870bd802b449b429ee76` |

Il tokenizer segue encode senza special token di `studio2/fase03/prepare_gate.py`,
riscritto localmente senza import; asset verificati contro le impronte del preflight.
Nessuna chiamata HTTP o a modelli; nessuna simulazione.
