# Sotto-fase 3 della Fase 03 — run fault di sviluppo

**Batch completato e copia remota verificata**, 2026-09-13. Questa consegna chiude la
sotto-fase dei run fault di sviluppo, non la macro-Fase 03. La verifica indipendente del
codice, dei manifest e di questo verbale resta da svolgere in un'altra finestra prima
dell'integrazione in `main`.

## 1. Disegno eseguito

Il catalogo congelato è F1/F2/F3/F8/F10/F13/F14/F15. Sono stati eseguiti otto fault per
cinque batch, con un solo IDV per run, nessun cambio di setpoint, stream Philox uguale
all'indice e intervallo riservato 30000–30039. La specifica pre-esecuzione originale resta
in [SPECIFICA_RUN_FAULT.md](SPECIFICA_RUN_FAULT.md); la revisione tracciata che identifica
il MEX effettivo e chiarisce il criterio di equivalenza è
[SPECIFICA_RUN_FAULT_rev002.md](SPECIFICA_RUN_FAULT_rev002.md).

Per ogni run: burn-in 20 h, controllo interno [20,25) escluso dallo sviluppo, onset
nominale 25 h, 40 h post-fault, termine 65 h e otto finestre half-open da 5 h. F14/F15
restano fault singoli nonostante la cautela di Downs & Vogel; segnale debole o assente
non autorizza sostituzioni o modifiche post-hoc.

## 2. Esito del batch

| Controllo | Esito |
| --- | ---: |
| Manifest attesi / presenti | 40 / 40 |
| Run `complete` | 40 |
| Trip fisici | 0 |
| Errori tecnici / `not_run` | 0 / 0 |
| Finestre post-fault complete | 320 / 320 |
| Durata totale | 330,764 s |
| Righe del log eventi | 82 |
| SHA-256 `generation_manifest.csv` | `69a7f2f97568a656a96e8eeb0871a6295b087d44b2ae7306fd09a5365e1f4f23` |
| SHA-256 `MANIFEST_FAULT_DEV.csv` | `9eaed0e901c6f06d5aa94b4e2d81d5afdd3464022ae6d2709b92f872789a6d9d` |

Gli indici sono univoci e coprono esattamente 30000–30039; per tutti vale
`stream_id = run_index_uint64` e l'IDV corrisponde al piano. Gli onset osservati sono tra
25,00007946967903 h e 25,0005 h, quindi entro un passo `Ts_base=0,0005 h` dal nominale.
Tutti i run terminano a 65 h e dichiarano otto finestre complete. I 200 hash di output,
diagnostiche, log, manifest per-run e attempt nel manifest aggregato coincidono con i file
su disco.

## 3. Tentativo di lancio abortito

Il primo tentativo di avvio in background non ha prodotto run né output parziali. Il
processo in background è stato terminato dalla sandbox al termine della finestra di
esecuzione; `matlab.log` è rimasto vuoto e il PID registrato è 94590. Il batch è stato
quindi rilanciato da un terminale esterno, in un nuovo contesto di lancio, mantenendo
intatti piano, stream e destinazione scientifica. L'evidenza del tentativo abortito è
conservata in `runtime/batch_launch_failed_20260913T122247/` e nell'archivio pubblico.

## 4. MEX strumentato

I manifest registrano il MEX strumentato SHA-256
`834e2361915249402a1ec9074a4be04f22a6404deb841e5134bf34347dfde544`. Il MEX base della
Fase 02 ha SHA-256 `6ae7e7be5394773f1854f1c53eddbd778ad7557b61fb05a93b3edb0552b1d11e`.
Non devono avere lo stesso hash: il primo aggiunge diagnostiche prescritte prima del batch.

[MEX_RECORD.md](MEX_RECORD.md) conserva sorgenti, diff completo, ambiente di compilazione
e due prove complementari. Il Normal `burnin_qual-001` rigenerato col MEX strumentato ha
7/7 membri ZIP identici, zero celle diverse e lo stesso contatore Philox finale; F1/30000
rigenerato col MEX base produce un CSV byte-identico al run della campagna. Equazioni,
stato Philox, ordine delle estrazioni e XMEAS/XMV non sono modificati.

## 5. Conservazione

I dati ignorati da Git sono pubblicati nel repository
[`sorrentinoluca/fot-tep-data`](https://github.com/sorrentinoluca/fot-tep-data), release
[`studio2-fase03-fault-dev-v1`](https://github.com/sorrentinoluca/fot-tep-data/releases/tag/studio2-fase03-fault-dev-v1),
agganciata al commit `6d238929285e57c6c70f4d563ef7e30b59da6ac5`.

Asset: `studio2-fase03-fault-dev-v1.tar`, 208.257.536 byte, SHA-256
`6edd96711d2913953c6de81ce6dbb7c51e7677a2a7c1892b0676de5e7a9fd97c`. Contiene la
campagna `fault_dev_001`, il tentativo abortito e `runtime/mex_equivalence/`.
[MANIFEST_CONSERVAZIONE.csv](MANIFEST_CONSERVAZIONE.csv) registra 240 file.

La verifica non ha riusato la copia locale: l'asset è stato riscaricato in una directory
temporanea fuori dal repository, ne è stato verificato l'hash, quindi è stato estratto.
Percorsi, byte e SHA-256 di 240/240 file coincidono col manifest; mismatch: 0. Metadati e
URL dell'asset sono in [ARTIFACT_STORAGE.json](ARTIFACT_STORAGE.json), stato
`public_release_verified_by_redownload`.

## 6. Cosa questa sotto-fase non produce

I 40 run sono materiale di sviluppo, non valutazione. Questa sotto-fase non produce:

- insight o librerie di insight;
- feature, evidence o verbalizzazioni;
- prototipi diagnostici;
- soglie, score o calibrazione;
- selezione di prompt reali, gate LLM o inferenze;
- risultati di accuratezza, confronto federato o conclusioni per il paper.

Nessuna chiamata a modelli linguistici è stata effettuata durante generazione, audit,
equivalenza MEX, conservazione o documentazione.

## 7. Dipendenze aperte

Restano aperti:

1. verifica indipendente in un'altra finestra con un altro modello;
2. integrazione dei commit in `main`, solo su richiesta dell'autore;
3. estrazione pre-specificata di feature/evidence dai 40 run;
4. sviluppo degli insight e dei prototipi previsto dalle sotto-fasi successive;
5. costruzione del manifest scientifico autonomo dei futuri input reali del pilot;
6. nuovo controllo di capienza e autorizzazione esplicita prima di qualunque gate LLM;
7. decisioni ancora aperte D2, D11, OOD e producer alternativo.

Non sono stati creati tag nel repository principale e il branch di lavoro non è stato
pubblicato.
