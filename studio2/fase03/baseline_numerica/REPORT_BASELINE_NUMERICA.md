# Sotto-fase 03.9 — report `normal_dev` e baseline numerica

**Esito candidato: lotto accettato e prototipi verificati; freeze efficace e chiusura della
sotto-fase ancora pending.** Data: 2026-09-14.

## 1. Stato per requisito

| Requisito | Evidenza | Stato |
| --- | --- | --- |
| Piano immutabile: 40 run, 5 per agente, stream 60000–60039 | `plans/normal_dev.csv`, SHA-256 `66382b3ecedd8be417656e56e97d38fc4815d0c857d2c6dd302d58d80a512a97` | completato |
| Integrità tecnica del lotto | `AUDIT_NORMAL_DEV.json`: 40/40 run, 320/320 finestre, bijezione piano–manifest–workbook, griglia e valori finiti PASS | completato |
| Decisione sulle deviazioni | `DECISIONE_ACCETTAZIONE_NORMAL_DEV.md`, provenienza «3.9 - OK» nella conversazione corrente | completato; deviazioni conservate |
| Decisione sul warning Simulink | `SIMULATOR_WARNING_CHECK.json`: accettabile solo per questo lotto normal-mode | completato e circoscritto |
| Estrazione Normal con contratto 03.6 e U3/R2 | 320 unità, 697 dimensioni, leakage PASS; manifest `cc8d96c2c60169afc99cb811cea194aa553afcc7cc51cad4a0092d44de38fdc1` | completato |
| Prototipi globali/locali | `PROTOTYPES.json` `6d0b754065eb8a69d0657638deeef0756de0ec8e93a905c55aea18fadace2cb2`; manifest `8309a914d2141da38d1120606897bcead40142829ecd541b6b0423d0d9465751` | completato |
| Ricalcolo indipendente dai metodi di `baseline.py` | `BASELINE_CHECK.json`: 25/25 vettori, 697 componenti, differenza massima 0 con Decimal(50) | completato |
| Handoff degli otto esempi Normal a 03.10 | regola pre-specificata: run locale 1, finestra `[25,30)`; controllo sul parser del harness | completato nel candidato |
| Nomi metriche/conteggi 03.9 ↔ 03.10 | semantica compatibile; restano `accuracy`/`accuracy_all`, `n`/`total`, `abstentions`/`abstained` | pending integrazione 03.10 |
| Conservazione remota verificata | archivio locale USTAR `eef69b42d8506c993ac45d77208df982d138b4354d7d4134bd67ba421dc91a03`, 1.336 file | pending pubblicazione e riscaricamento |
| Verifica indipendente del candidato | `VERIFICA_BASELINE_NUMERICA.md` | pending al momento di questo report |
| Raggiungibilità da `origin/main` e tag di freeze | nessuna operazione esterna autorizzata/eseguita | pending |

Questa tabella distingue tre livelli: il **lotto** è tecnicamente PASS e le deviazioni sono state
accettate; la **baseline** è costruita e ricalcolata; la **sotto-fase** non è ancora integrata né
congelata. Non sono state aperte osservazioni di test e non è stata misurata alcuna performance.

## 2. Lotto `normal_dev`

Il lotto contiene 40 workbook da 65 h, per 2.600 h simulate, e produce otto finestre utili da 5 h
per run dopo burn-in e gap. L'audit read-only ha verificato 54 colonne, 3.901 righe dati per file,
griglia al minuto `0..65 h`, valori numerici finiti, hash, MEX, modello, Philox, stream e
corrispondenza col piano. Le 320 finestre sono raggruppate in 40 run e non sono dichiarate 320
repliche indipendenti.

L'autore ha accettato separatamente tre limiti: riuso del pathname `normal_dev_001` dopo il
tentativo pre-start; assenza nel manifest del comando riuscito e del `MATLABPATH`; sufficienza
della tracciabilità residua, incluso l'hash MEX. L'accettazione non trasforma questi punti in
conformità e non attribuisce retroattivamente una firma o un commit di esecuzione. Log, recovery,
runtime e storia audit sono inclusi nell'inventario di conservazione.

Il log riuscito contiene 40 warning `Variable Time Delay`. Il modello congelato usa il blocco
`VariableTransportDelay` come `Variable time delay`, `FixedBuffer=off`, simulazione normal-mode e
solver `ode45`; il generatore non sovrascrive modalità o blocco e non invoca code generation.
L'ispezione documentale e statica conclude che, in questo contesto, il messaggio descrive crescita
dinamica della memoria e non perdita della storia. L'esito non vale per ERT/GRT, embedded, modelli
o hash diversi e non è una prova generale di validità scientifica. Non è stato modificato il
simulatore e non è servito un replay per questa conclusione circoscritta.

## 3. Evidence Normal e baseline

`extract_normal_evidence.py` verifica prima dell'uso gli hash dell'estrattore e del controllo
leakage della 03.6. La destinazione riuscita `evidence/normal_dev_002` è nuova: due tentativi
parziali, falliti per risoluzione dei path/import, sono stati rimossi senza alterare input o
risultati. L'output riuscito comprende 320 evidence da 697 componenti e un indice evaluator-side;
gli otto esempi locali sono `NDEV-EVD-0001`, `0041`, `0081`, `0121`, `0161`, `0201`, `0241` e
`0281`, sempre run locale 1 e finestra `[25,30)`.

Le evidence fault provengono dalla release preferita `studio2-fase03-evidence-v2`. Il suo
packaging corregge la v1, mentre i 1.283 file scientifici, 61.208.618 byte e
`EVIDENCE_MANIFEST.csv` restano identici; il manifest usato dalla baseline ha SHA-256
`5111d0c61c2e93fe5071d7a85015673549af0bf9c1dc74e0d940719a8400e020`.

La baseline contiene nove prototipi globali e, per ciascuno degli otto agenti, Normal più il fault
locale: 25 vettori totali. I fault contribuiscono 40 firme per classe; Normal contribuisce 320 firme
globali e 40 per agente. Ogni vettore è la media aritmetica per componente delle finestre fissate.
`verify_prototypes.py` non importa `baseline.py`: rilegge tutte le signature e ricalcola con
`decimal.Decimal`, precisione 50. Il massimo scarto sulle 17.425 componenti confrontate è zero,
contro una tolleranza assoluta di `2e-16`.

La dipendenza U3 resta esplicita: N1–N5 e soglie V2 sono usati solo per normalizzazione e flag del
verbalizer, non come esempi `normal_dev`; se la guardia R2 decade, tutte le evidence Normal vanno
rigenerate. Lo sbilanciamento 320 Normal contro 40 per ciascun fault resta un vincolo per 03.14,
non una scelta risolta qui.

## 4. Interfaccia 03.8/03.10

Le righe evaluator-side della baseline includono i campi richiesti da 03.8:
`agent_id`, `physical_case_id`, `condition`, pseudolabel vera, `abstain`, `predicted_label` e
`valid`. Le predizioni restano separate dalla verità fino alla valutazione e
`independence_claim=false`.

Il parser del harness 03.10 al commit `51160872906feaa63c1fda5e9cf6e0fe8538fb16` accetta la
forma stretta dell'handoff: stato `FROZEN_NORMAL_DEV_EXAMPLES`, commit sorgente, regola fissata e un
testo neutro con hash per ciascun agente. La compatibilità dei nomi delle metriche non è completa:
la baseline scrive `accuracy`, `n`, `abstentions`, `non_abstained`; il harness usa
`accuracy_all`, `total`, `abstained`, `invalid`. La semantica del primo, secondo e terzo numero è
allineata, ma il mapping deve essere adottato nella 03.10. Nessun file della branch 03.10 è stato
modificato.

## 5. Conservazione e freeze

`prepare_conservation.py` ha creato un archivio locale POSIX USTAR non compresso, con soli file
regolari e metadati deterministici. La verifica su estrazione fresca ha controllato 1.336 file e
150.575.225 byte: nessun mismatch, extra, AppleDouble, xattr o PAX header. L'archivio è solo un
candidato locale; la release proposta `studio2-fase03-normal-dev-v1` non esiste ancora. Prima del
freeze efficace occorrono pubblicazione su `fot-tep-data`, riscaricamento in una directory fresca
e nuovo confronto byte/hash.

`BASELINE_FREEZE.json` resta la fotografia storica pre-generazione e non viene riscritto.
`BASELINE_FREEZE_rev002.json` raccoglie gli artefatti reali ma resta intenzionalmente inefficace
finché non sono soddisfatti verifica indipendente, mapping 03.10, pubblicazione+riscaricamento,
integrazione in `origin/main` e tag.

## 6. Verifiche eseguite

- audit tecnico read-only del lotto: PASS 40/40 run e 320/320 finestre;
- controllo statico warning: accettabile nel solo ambito dichiarato;
- leakage consumer-visible delle 320 evidence: PASS;
- ricalcolo prototipi: PASS, differenza massima 0;
- test unitari baseline, piano ed estrazione: eseguiti sul candidato e riportati nel verbale di
  verifica;
- `docs/test_explanation.py` prima delle modifiche: 35 test, 14 failure e 1 skipped, tutti
  preesistenti; il confronto finale deve conservare esattamente conteggio e identificatori.

## 7. File prodotti o aggiornati

Codice: `audit_normal_dev.py`, `extract_normal_evidence.py`, `prepare_conservation.py`,
`verify_prototypes.py`, correzione fail-closed del preflight e relativi test. Evidenze tracciate:
`AUDIT_NORMAL_DEV.*`, `DECISIONE_ACCETTAZIONE_NORMAL_DEV.md`, `SIMULATOR_WARNING_CHECK.json`,
`PROTOTYPES*.json`, `BASELINE_CHECK.json`, `MANIFEST_CONSERVAZIONE.csv`,
`ARTIFACT_STORAGE.json`, freeze revisionato, controllo d'interfaccia e handoff 03.10. I dati
voluminosi sotto `runs/`, `runtime/`, `audit_history/`, `evidence/` e `conservation/` sono ignorati
da Git e identificati dagli inventari/hashing tracciati.

Non sono stati modificati piano, specifiche pre-osservazione, handoff storico, modello, generatore
qualificato, MEX, `phase_b/`, soglie V2, protocollo 03.8 o harness 03.10.

## 8. Modello, profilo e limiti

OpenAI Codex, modello GPT-5, profilo implementativo. La successiva verifica deve essere svolta da
un'altra sessione in ruolo revisore. Nessuna chiamata a modelli linguistici dello studio, nessun
fit, calibrazione, FAR, score o dato di test. Nessun push, merge, release o tag.

Fonti operative lette: prompt di fase/verifica/documentazione/commit; `docs/MAINTENANCE.md` §8;
piano rev. 7; specifiche 03.6–03.9; piano statistico rev. 9; codice del harness 03.10; freeze e
manifest citati. Costo indicativo cumulativo: decine di migliaia di token; lettura completa dei 40
workbook nell'audit e delle 640 signature di sviluppo nella costruzione/ricalcolo.
