# Handoff — 40 run fault di sviluppo, da eseguire in un'altra finestra

La finestra di preparazione **non lancia questo batch**. Il piano approvato è
[plans/fault_dev.csv](plans/fault_dev.csv): 40 righe, stream 30000–30039, un solo IDV,
innesco 25 h, termine 65 h. Il controllo [20,25) è escluso dal materiale di sviluppo.
Segnale debole/assente e trip non autorizzano sostituzioni o estensioni.

## Ambiente e preparazione

Mac Apple Silicon, MATLAB **R2025b nativo ARM**, Simulink e Xcode/Clang; Python 3 standard.
La shell ospite può essere sotto Rosetta: usare `/usr/bin/arch -arm64` è necessario.
Nella consegna locale la build è già pronta sotto `runtime/build/`. Il report smoke registra
hash e versione. Non ricompilare per lanciare il batch sulla stessa macchina.
Su una nuova copia bisogna prima generare la copia strumentata e compilare:

```bash
cd /Users/luker/fot-tep
python3 studio2/fase03/fault_runs/prepare_simulator.py
/usr/bin/arch -arm64 /Applications/MATLAB_R2025b.app/bin/matlab -batch "addpath('/Users/luker/fot-tep/studio2/fase03/fault_runs'); compile_fault_philox"
```

Il preparatore rifiuta sorgenti base diversi e file generati difformi. Il compilatore rifiuta
un MEX già presente. Su altre piattaforme gli hash MEX possono differire: registrare il nuovo
ambiente e sottoporlo a verifica prima di un'esecuzione scientifica; lo smoke autorizzato
in questa finestra non autorizza ulteriori simulazioni di qualifica.

## Avvio esatto in background

Dal prompt MATLAB, senza caricare o eseguire il modello interattivamente:

```matlab
[status, msg] = system('/bin/bash /Users/luker/fot-tep/studio2/fase03/fault_runs/launch_fault_batch.sh');
fprintf('%s', msg);
assert(status == 0, 'Avvio batch rifiutato');
```

Lo script esegue il seguente comando `nohup`, dopo i controlli e la prenotazione esclusiva:

```bash
nohup /usr/bin/arch -arm64 /Applications/MATLAB_R2025b.app/bin/matlab -batch "addpath('/Users/luker/fot-tep/studio2/fase03/fault_runs'); generate_fault_runs('/Users/luker/fot-tep/studio2/fase03/fault_runs/plans/fault_dev.csv','/Users/luker/fot-tep/studio2/fase03/fault_runs/runs/fault_dev_001')" > /Users/luker/fot-tep/studio2/fase03/fault_runs/runtime/batch_launch/matlab.log 2>&1 < /dev/null &
```

Usare il launcher completo, che conserva anche il PID e rifiuta una seconda esecuzione.
La destinazione è **`studio2/fase03/fault_runs/runs/fault_dev_001/`**.
I 40 run vengono eseguiti **sequenzialmente in un unico processo MATLAB**. Non aprire più
worker sullo stesso piano: riutilizzerebbero gli stessi stream. La parallelizzazione richiede
un'estensione esplicita dei piani e della raccolta dei manifest, non è parte di questa consegna.

## Come riconoscere il completamento

Il log esterno è `runtime/batch_launch/matlab.log`, il registro strutturato è
`runs/fault_dev_001/events.jsonl`. Per ogni tentativo devono comparire `run_start` e `run_end`.
Il completamento tecnico riuscito stampa **`FAULT_CAMPAIGN_COMPLETE manifests=40`**, dopo
il controllo degli hash; i trip fisici sono ammessi e contati separatamente.

Eseguire poi il controllo in sola lettura:

```bash
python3 /Users/luker/fot-tep/studio2/fase03/fault_runs/fault_protocol.py audit /Users/luker/fot-tep/studio2/fase03/fault_runs/plans/fault_dev.csv /Users/luker/fot-tep/studio2/fase03/fault_runs/runs/fault_dev_001
```

L'esito richiesto è `manifest_count=40`, `hashes_verified=true`, `accepted=true`, zero
`technical_failure` e zero `not_run`. `physical_trip` conserva il prefisso e il tempo reale
strumentato: non equivale a 65 h completate. Riportare il conteggio effettivo delle finestre
complete, non assumere che siano 320. Il solo termine del processo o `campaign_end` non è PASS.

Un errore tecnico arresta il ciclo; gli indici successivi ricevono `not_run`, senza tempi o
risultati inventati. Un crash del processo può impedire anche questi manifest: log troncato,
manifest mancanti e assenza del marker finale rendono il batch incompleto. Conservare tutto
ed esaminare l'errore; nessuna ripresa o rigenerazione automatica. Non cancellare directory
per aggirare il rifiuto di sovrascrittura.

## Cosa non toccare durante l'esecuzione

Non modificare checkout/branch, piano, specifica, sorgenti, script, MEX, modello, init,
cache, file dati o manifest; non eseguire `prepare_simulator` o compilazioni concorrenti.
Non aprire e salvare CSV in Excel. Non spostare o cancellare la destinazione, il log o la
prenotazione del launcher. Leggere log e stato è consentito. Un secondo MATLAB non deve
scrivere nelle stesse directory. Nessuna chiamata LLM è richiesta.

I dati batch sono ignorati da Git; conservarli in una posizione recuperabile e verificarne
la copia prima di dichiarare soddisfatta MAINTENANCE §8.5. Nessun upload è autorizzato qui.
Lo smoke e i suoi CSV/log/manifest sono invece consegnati nel commit dedicato.

Tempo e proiezione misurati sono riportati in `smoke/REPORT_SMOKE.md` dopo l'unica esecuzione;
la formula pre-specificata è `40 × runtime_smoke × 65/25.1`, distinta dalla sola simulazione.
