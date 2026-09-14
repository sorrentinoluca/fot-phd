VERDETTO: OK

# Verifica indipendente — sotto-fase 03.9 `normal_dev` e baseline numerica

**Modello:** OpenAI Codex, GPT-5  
**Sessione separata:** `/root/verifica_039`  
**Commit verificato:** `ba1a206e1fe31c062d5491b4fb821ff925149982`  
**Primo candidato, NON OK:** `fc927a663395fd88edecf69dc3f594c47c7b663e`  
**Secondo candidato, NON OK:** `4970134c319107b3058e084c263bc890a06838cc`  
**Branch osservato:** `codex/studio2-baseline-numerica`  
**Data:** 2026-09-14

Questa riverifica è stata svolta in sola lettura sul nuovo candidato e sugli artefatti ignorati
locali. L'unica modifica prodotta dalla sessione è l'aggiornamento di questo verbale. Non sono
stati eseguiti commit, push, merge, tag, release, simulazioni o valutazioni su dati test.

## Riscontri

| Esito | Punto | Fonte primaria e riscontro |
| :---: | --- | --- |
| ✅ | Identità e perimetro del candidato | `git rev-parse ba1a206e1fe31c062d5491b4fb821ff925149982` restituisce il commit completo sopra. Rispetto al secondo candidato, il commit corregge una sola riga di `studio2/PROVENIENZA.md` e registra il secondo verbale; nessun artefatto tecnico cambia. Il diff complessivo da `46c0b62` resta confinato a `studio2/`; nessun artefatto congelato di `phase_b/`, `icl/`, `ablation/`, `tep_*_v2/`, `reproducibility/` o `code/` è modificato. `BASELINE_FREEZE.json` è preservato byte per byte, SHA-256 `8ac1f1e72b23484395c2955c7d14ac333e61f8743d662dd92b933e37f90547c9`. |
| ✅ | Pre-specificazione | I commit `0a38e2c` e `8eed658` fissano rispettivamente lotto/regola dell'esempio e baseline prima dei timestamp del manifest di generazione (prima run `2026-09-14 09:01:43 UTC`). Il piano ha 40 righe, cinque per agente, stream 60000–60039 e SHA-256 `66382b3ecedd8be417656e56e97d38fc4815d0c857d2c6dd302d58d80a512a97`. |
| ✅ | Integrità tecnica `normal_dev` | Controllo indipendente con `openpyxl` su tutti i 40 workbook: manifest/piano in bijezione, SHA-256 di ogni workbook uguale al manifest, unico foglio `Sheet1`, 54 colonne, 3.901 righe dati, soli numeri finiti, griglia `i/60` con errore massimo `1.4210854715202004e-14 h`. Confermati 40/40 run e otto finestre da 300 campioni per run, quindi 320/320. Il manifest di generazione ha SHA-256 `aaacc96e8f95d62da639a8830f462a72efa55dce7cb6068bf1e7a2864bbd4e6d`. |
| ✅ | Separazione fra PASS e deviazioni | `AUDIT_NORMAL_DEV.json` (SHA-256 `fb44c26ceaf3b045fe16902296bc3e01219acff7f7fac969c106369c7b48937f`) conserva `technical_result=PASS` e `process_status=deviazioni`. `DECISIONE_ACCETTAZIONE_NORMAL_DEV.md` registra senza firma né retrodatazione le due autorizzazioni effettive dell'autore: riuso del pathname e sufficienza limitata della tracciabilità comando/`MATLABPATH`. Le deviazioni non sono convertite in conformità. |
| ✅ | Warning `Variable Time Delay`, ambito tecnico | SHA-256 verificati: modello `c58826748edd306b723da2f0199a0fb2dc193a51dc5c28dbde8ac821e39dfafd`, generatore qualificato `923d657608f5bbf30869c8cdf2772dd5cacd2a98b4ef62dc85540dc812eda837`, wrapper `ec169e76b05694d3ea038fd3eedcc2f92b28f56ac18c2cf383d85d37911b47ee`, log riuscito `983d4f3e54395078820df7b44d094823e99f2f856c47bb5d8a87df0ade2fb31d`. Ispezione statica indipendente con MATLAB R2025b (`-maca64`, nessuna `sim`) conferma `SimulationMode=normal`, `SolverType=Variable-step`, `Solver=ode45`, blocco `VariableTransportDelay`, `VariableDelayType=Variable time delay`, `MaximumDelay=20`, `MaximumPoints=1024`, `FixedBuffer=off`, `InitialOutput=0`. Il generatore cambia solo solver, `StopFcn` e `StopTime` e chiama `sim(modelName)`, senza code generation. Il log contiene 40 riallocazioni (8 a 63.488, 32 a 64.512 punti), un marcatore `Generated 40 runs` e nessun errore o messaggio di overwrite/extrapolazione/clipping. La conclusione resta correttamente limitata a questo lotto normal-mode; non si estende a ERT/GRT, embedded o validità scientifica generale. Il caricamento statico ha anche emesso un warning separato su `Mode_1_Init` non nel path della sessione di verifica, ma le proprietà sono state lette e il modello non è stato salvato o modificato. |
| ✅ | Evidence Normal e dipendenze U3/R2 | Verificati gli hash della 03.6: `extract_evidence.py` `46b451c2d6d8b1627993828ac9bac39532562f2fa1b27955b8a20f098ba24e97`, `leakage.py` `c77ae5b11186c5b0df87b2f1df8800cb45fb25317e248fe8484d3e8283073887`; baseline N1–N5 `79883dd0aabbd034c15337b0be1ffca37e59ea7b32443a15d560b7feda2b2e6a`; guardia R2 `7df0cef2d7854c689b79eb911fa01d1ede1625e22f0d3636c0ea5d678c9f33f8`, con `guard_pass=true`. Controllo di tutte le 320 righe e dei 1.280 file per-unità: path, byte e SHA-256 coincidono, firma 697-D, leakage JSON/testo assente, otto esempi locali esattamente `agent_run_index=1`, finestra `[25,30)`. Manifest Normal `cc8d96c2c60169afc99cb811cea194aa553afcc7cc51cad4a0092d44de38fdc1`; indice evaluator `4f340a0e24e809a5d16d783b561262826fae08afb143bde81d410ae103f55329`. |
| ✅ | Evidence fault 03.6 | Nella worktree evidence a `c66bd8dddf8e2af9dd0665ee30afd36c248b93fb`, `ARTIFACT_STORAGE.json` identifica `studio2-fase03-evidence-v2` come repackaging verificato della stessa base scientifica: 1.283 file, 61.208.618 byte, zero mismatch/AppleDouble/PAX. Il manifest effettivamente letto ha SHA-256 `5111d0c61c2e93fe5071d7a85015673549af0bf9c1dc74e0d940719a8400e020`; l'archivio v2 dichiarato ha SHA-256 `6d724ca2a06439129a11ff4a56648d550b3dd87d4e23a34197e88e6fca5b37cf`. Non sono stati confusi i due hash. |
| ✅ | Prototipi numerici | `verify_prototypes.py` è stato rieseguito sui soli indici/evidence di sviluppo con output temporaneo: esito byte-identico a `BASELINE_CHECK.json`. Ricalcolati con `Decimal(50)` nove prototipi globali e sedici locali, 25 vettori × 697 componenti; massimo scarto `0` contro tolleranza `2e-16`. Conteggi confermati: 40 firme per fault, 320 Normal globali e 40 Normal per agente. `PROTOTYPES.json` SHA-256 `6d0b754065eb8a69d0657638deeef0756de0ec8e93a905c55aea18fadace2cb2`; manifest `8309a914d2141da38d1120606897bcead40142829ecd541b6b0423d0d9465751`. Nessun F-number nei prototipi e nessun file test passato al ricalcolo. |
| ✅ | Handoff 03.10 e mapping metriche | Il parser reale `_normal_examples` del worktree harness a `51160872906feaa63c1fda5e9cf6e0fe8538fb16` accetta `NORMAL_DEV_HANDOFF.json`: 8 esempi, nessun requisito mancante. Testo, hash del testo, agenti, ID evidence e hash workbook sorgente coincidono 8/8 con l'indice Normal. Le righe baseline espongono i campi 03.8 richiesti. I nomi restano però non integrati: `accuracy`→`accuracy_all`, `n`→`total`, `abstentions`→`abstained`; `invalid` è aggiuntivo nel harness. `INTERFACE_CHECK.json` li marca correttamente pending. |
| ✅ | Conservazione locale e stato remoto | Ricalcolato l'archivio locale `studio2-fase03-normal-dev-v1.tar`: 151.500.800 byte, SHA-256 `eef69b42d8506c993ac45d77208df982d138b4354d7d4134bd67ba421dc91a03`. Tutti i 1.336 membri regolari coincidono per path, byte e SHA-256 con `MANIFEST_CONSERVAZIONE.csv` (150.575.225 byte di contenuto); zero PAX e AppleDouble. `ARTIFACT_STORAGE.json` dichiara correttamente `local_candidate_not_published_not_redownloaded`, URL/data null e `redownload_verified=false`. Non è stata fatta una verifica remota in questa sessione: pubblicazione e riscaricamento restano requisiti pending, come impone MAINTENANCE §8.5. |
| ✅ | Freeze e assenza di chiusura prematura | `BASELINE_FREEZE_rev002.json` ha `effective=false`, nessun tag e stato candidato. Conserva come pending: review indipendente, adozione mapping 03.10, pubblicazione+riscaricamento, raggiungibilità da `origin/main` e tag successivo. Il nuovo candidato non è contenuto in alcun branch remoto o tag. Il report distingue correttamente lotto tecnicamente accettato, baseline costruita/ricalcolata e freeze/integrazione ancora pending; non riporta accuracy, FAR o risultati test. |
| ✅ | Test | `python3 -m unittest studio2.fase03.baseline_numerica.test_baseline studio2.fase03.baseline_numerica.test_normal_dev_plan studio2.fase03.baseline_numerica.test_extract_normal_evidence -v`: 10/10 PASS. `python3 docs/test_explanation.py`: 35 test, 14 failure, 1 skip, invariati rispetto alla baseline dichiarata. Identificativi: `test_condition_c_contract_and_caveats` (1), `test_one_flow_and_ordered_step_headings` (1), `test_step27_qwen_frozen_results_and_limitations` (9), `test_step27_qwen_protocol_stable_facts` (3); skip `TutorialChecks.setUpClass` perché manca il walkthrough legacy part 1 nel checkout. Nessuna coppia MD/HTML è stata toccata nel candidato. |
| ✅ | Provenienza dell'autorizzazione | Le due formulazioni contestate sono ora entrambe corrette. La riga del piano dice che `origin/main` contiene oggi la revisione, che lo stato del ref al lancio non è attestato e che «3.9 - OK» non autorizza una deroga. La riga del lotto attribuisce all'autore soltanto l'accettazione del pathname riusato e della lacuna comando/`MATLABPATH`, poi precisa separatamente che lo stato di `origin/main` al lancio non è attestato né coperto dall'OK. Una ricerca sul candidato non trova più `piano non su origin/main` associato all'accettazione. Il secondo blocco è risolto senza inventare prova retroattiva. |
| ✅ | Nome della fonte leakage | Corretto in entrambi i documenti modificati: `studio2/PROVENIENZA.md` e il report citano ora `extract_evidence.py` e `leakage.py`. I due file esistono nella worktree evidence e mantengono gli hash verificati `46b451c2...24e97` e `c77ae5b1...3887`. Il primo blocco sul pathname inesistente è risolto. |
| ✅ | Storia dei tentativi parziali di estrazione | Report e provenienza qualificano ora esplicitamente la storia come nota di sessione senza log/traccia primaria, non verificabile e non usata come prova. Gli output riusciti restano sostenuti autonomamente dai 320 record e dai relativi hash. La precedente avvertenza è risolta senza inventare evidenza retroattiva. |

## Conclusione

La parte scientifico-tecnica verificabile regge: lotto **PASS 40/40 e 320/320**, warning accettabile
nel perimetro circoscritto, evidence e dipendenze U3/R2 integre, baseline ricalcolata senza dati test,
handoff compatibile e conservazione locale coerente. La baseline è quindi tecnicamente verificata.

Il candidato risolve tutti i rilievi delle due verifiche precedenti: limita l'autorizzazione alla
fonte primaria, usa il pathname reale `leakage.py` e qualifica come non probatoria la storia dei
tentativi parziali. Il lavoro regge e può procedere all'aggiornamento coordinato della
documentazione.

L'`OK` non rende efficace il freeze e non chiude la Fase 03. Pubblicazione e riscaricamento del
lotto, mapping 03.10, integrazione in `origin/main` e tag restano pending: il lotto è accettato e
la baseline è verificata, ma la sotto-fase non è ancora integrata né congelata efficacemente.

## Comandi principali rieseguiti

- confronto `4970134..ba1a206`, controllo del perimetro e ricerca globale delle formulazioni
  contestate, escludendo soltanto la loro citazione storica in questo verbale;
- ricalcolo SHA-256 di freeze storico/rev002, audit, warning check, prototipi, handoff, inventario,
  manifest Normal e manifest di generazione: artefatti tecnici invariati rispetto alla prima verifica;
- suite unitaria 03.9: 10/10 PASS;
- `python3 docs/test_explanation.py`: 35 test, 14 failure e 1 skip, stessi identificativi della
  prima verifica.

I controlli completi su 40 workbook, 320 evidence, 25 prototipi, parser harness, MATLAB statico e
1.336 membri del tar non sono stati ripetuti perché il nuovo commit modifica soltanto documenti e
il verbale e gli hash di tutti gli artefatti tecnici controllati sono invariati. Restano i riscontri
integrali della prima verifica, riportati sopra.

Fonti lette: `Prompt_LLM.md`, `Verifica_LLM.md`, `docs/MAINTENANCE.md` completo con §8.3–8.6,
specifiche/report/freeze/audit/codice 03.9, `studio2/PROVENIENZA.md` §10, artefatti ignorati
`runs/`, `runtime/`, `evidence/`, `conservation/`, fonti 03.6 nella worktree evidence, guardia R2
nel checkout primario, piano 03.8 al commit dichiarato e parser/metriche della worktree 03.10.
Costo aggiuntivo della terza riverifica: diff mirato di una riga scientifica, rilettura della
sezione di provenienza, 10 test unitari e 35 test documentali; i controlli massivi non sono stati
duplicati perché i relativi hash sono rimasti invariati.
