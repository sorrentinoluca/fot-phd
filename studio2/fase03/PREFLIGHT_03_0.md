# Fase 03.0 — preflight del pilot preliminare Qwen-27B

## Addendum operativo 03.10 allineato alla rev.10 (2026-09-14)

La configurazione Qwen-27B descritta sotto è un record storico della 03.0, non
la decisione D9 corrente. Per l'harness 03.10 `study_model_decision` resta
`UNDECIDED`; nessuna esecuzione può ereditare quel modello, endpoint o tokenizer
come default. Prima di contattare un servizio servono D9 esplicita e freeze di
identità/revisione, ruolo, tokenizer, chat template, limiti, configurazione e
fingerprint effettivi.

Il candidato offline 03.10 collega i 320 input fault di sviluppo e gli otto
esempi Normal verificati. Distingue quegli input della conformità producer dalla
libreria di sedici insight R4 che le otto richieste di conformità dovranno
produrre: la libreria non esiste ancora e il manifest resta incompleto.

L'ordine rev.10 è vincolante: **conformità producer → eventuale unica
remediation → sonda budget → unico gate 40×3**. Un ledger persistente e
condiviso registra l'intento prima di ogni trasporto e conserva i conteggi fra
stadi, riavvii e directory. La riserva unica è
`8 × remediation + transport <= 15`; preservare la remediation lascia al
massimo sette richieste di trasporto. Non ci sono retry automatici; un timeout è
ripetibile soltanto con prova di zero token nei casi documentati, la sonda
budget ripete solo triplette A/B-LF/E-LF complete e il gate non si ripete.
Massimi pianificati: 152 senza producer alternativo, 160 con alternativo; 200 è
un hard stop cumulativo distinto.

La divergenza dipende dalla validità e dalla coppia
`(abstain, predicted_label)`, non da JSON/finish reason/testo/hash raw. T3
richiede almeno 114/120 valide e un'astensione valida per condizione; T4 zero
troncamenti; una tripletta tutta invalida rende T6 non valutabile e impedisce il
GO tecnico. Tokenizer/capienza, comportamento, stabilità, latenza e fattibilità
temporale T5 non sono attestabili offline. Questo addendum non modifica il
freeze del piano generale 03.8, non chiude 03.10 o Fase 03 e non concede GO.

Stato: **envelope tecnico 8001@16384 congelato e sonda sintetica provvisoria completata;
esecuzione scientifica sospesa sul catalogo definitivo, sui suoi input derivati e sul producer
alternativo**.

La verifica sotto-fase offline 03.0 non aveva contattato endpoint HTTP né aperto dati finali. Dopo
autorizzazione esplicita è stata eseguita una prova tecnica dichiaratamente provvisoria sulla
sola fixture sintetica di stress: 1 POST rifiutato prima dell'inferenza e 3 inferenze completate.
Non sono stati aperti dati finali e non è stato eseguito il gate. Il pilot resta preliminare su
`Qwen/Qwen3.8-27B-FP8`; non sceglie il modello definitivo dello studio.

L'ambiente riproducibile richiesto dagli script è fissato in `requirements.txt`; le versioni
corrispondono all'ambiente vLLM locale osservato.

## Correzioni incorporate

- **`D11` non è la decisione 11 di §0.1.** `D11` sceglierà il sottoinsieme di coppie
  confondibili per l'ablation local-first e dipende dal catalogo. La decisione 11 di §0.1
  riguarda invece la politica conservativa quando l'API non espone temperatura e seed.
  Per questo pilot vale la regola pre-specificata dal piano: l'assenza dei due controlli viene
  registrata ma non attiva R=3 da sola; una divergenza osservata fra ripetizioni sì.
- Sono stati aggiunti schema degli insight, schema diagnostico, validatore autonomo e harness.
  I campi `insight_id`, `source_agent`, `pseudolabel`, `evidence_scope` e `variable_ids` sono
  deterministici; il producer può generare soltanto `observed_pattern`, limitato a 800 caratteri
  e 192 token. La libreria contiene 16 insight, due per fault; ogni ricevente ne vede 14.
- La capienza verrà calcolata **offline** sui 40 prompt reali una volta disponibili, con il
  tokenizer della revisione locale. Per ogni candidato deve valere
  `input massimo + thinking budget + 512 output + 256 margine <= 16384`.
  Sul profilo sintetico nominale il candidato massimo richiede 9.467 token; sul profilo di
  stress ne richiede 14.739. Entrambi passano il gate statico, ma le fixture non sono
  rappresentative e non congelano il budget finale.
- Prima del gate 40×3 si esegue una sonda A/B-LF/E-LF sui soli candidati staticamente capienti.
  La prova sintetica provvisoria ha trovato il primo candidato, 2048, senza troncamenti né
  errori di parsing; il risultato deve essere ripetuto sui prompt reali e non congela il budget.
  Nella ripetizione reale si congelerà il più piccolo budget che passa tutti e tre gli stress
  prompt; se nessun candidato passa, il gate non parte.
- Lo script di stabilità rifiuta di partire se prompt, schema, processo vLLM o configurazione
  differiscono dalle impronte congelate dopo la sonda di budget.

## Endpoint canonico e fingerprint

L'unica sequenza operativa verificata è ora `http://127.0.0.1:8001/v1` con
`--max-model-len 16384`, concorrenza 1, API server PID `690460` ed EngineCore PID `690661` su
GPU 0. La precedente 8001@7168 (PID `636846`) è **superata e non più disponibile**: i suoi
record restano come storia, ma non sono intercambiabili col nuovo fingerprint.

Il fingerprint fail-closed comprende congiuntamente:

- riga di comando completa, SHA-256 `b1560330f54807c5396e03360e7938748a1e4c41bf63f427ff74b6661de499d7`;
- ambiente completo `VLLM_*`/`CUDA_*` del server — `CUDA_VISIBLE_DEVICES=0` e
  `VLLM_USE_FLASHINFER_SAMPLER=0` — SHA-256 canonico
  `de6e5d641edcdc8542fddadf5abfbbeae9054e08aa099cb2998150d274816793`;
- vLLM `0.28.0`, PID server/EngineCore e fingerprint composito
  `39b59324e643e892bfdd05beac763aa9ca80092941f28ce01f582f0f3a593017`.

`GPU KV cache size: 34.133 tokens` e concorrenza massima `2,08×` sono telemetria della
configurazione 16384, non chiavi di confronto: la dimensione in token della KV cache varia con
`--max-model-len`. Record e script copiati senza modifiche sono in `env/` e mantengono gli hash
delle sorgenti esterne.

## Origine futura dei 40 prompt

I prompt reali dovranno provenire esclusivamente da artefatti di sviluppo dello Studio 2 creati
dopo aver chiuso il catalogo, generato i 40 nuovi run fault e prodotto le relative
feature/evidence/verbalizzazioni. Il report della Fase 02 ora pubblicato colloca esplicitamente
questi tre elementi in «Fuori dalla Fase02»: non sono un suo manifest né un suo output.

Quando tali prerequisiti esisteranno, per ciascuno degli otto agenti:

1. un caso di sviluppo locally-unseen entra in A, B-LF ed E-LF;
2. il più lungo altro caso di sviluppo eleggibile, misurato dopo il rendering col tokenizer
   locale, entra in B-LF ed E-LF come stress del contesto.

Si ottengono 8 prompt A, 16 B-LF e 16 E-LF. Gli otto casi delle triplette devono coprire una
volta ciascuno gli otto fault del catalogo. La selezione bilancia i riceventi, copre tutte le
condizioni e sovracampiona intenzionalmente i prompt con 14 insight.

Non è un campione casuale né rappresentativo della popolazione finale. Non stima accuracy,
astensione generale, prestazione local-seen/Normal, OOD o test finale. Le 40 unità indipendenti
servono solo al gate tecnico; con zero divergenze la regola del tre dà circa 7,5%, non dimostra
determinismo né instabilità sotto l'1%.

## Artefatti della Fase 02 ora sincronizzati

Il rebase su `origin/main` `c6e19d6` ha reso disponibili e verificabili:

- `studio2/fase02/REPORT_FASE02.md`, SHA-256
  `fa555197b9421f073d65f9cfb34aa7f06762fc0377ab26bad76ef60da47641d2`;
- `studio2/fase02/VERIFICA_FASE02.md`, SHA-256
  `34c8df542c1ee6dc9b3169d4ef53aba9eca726f15a92547bd28065178b903183`;
- `studio2/fase02/validation/PRECALIBRATION_FREEZE.json`, SHA-256
  `be01fe4cccf6e9f3c9d82e8de69e426aa68b80d3e106bac81fa29dfb325bf085`, con
  `source_head_commit=d472dc56c41f2b07563a362b81eed844460bf1c7`;
- le sezioni Fase 02 di `studio2/PROVENIENZA.md`, mantenute intatte nella risoluzione del rebase.

Sono già disponibili e registrati: snapshot e tokenizer Qwen-27B, runtime vLLM osservato,
componenti congelati del primo studio usati come provenienza, e la nuova implementazione offline
in `studio2/fase03/`.

## Prerequisiti scientifici ancora da realizzare

Non sono attribuiti alla Fase 02 e non vengono realizzati in questa finestra:

- catalogo definitivo degli otto fault;
- 40 nuovi run fault di sviluppo;
- relative feature, evidence strutturate e verbalizzazioni neutrali;
- mapping reale a nove label, assegnazione degli agenti, derangement e universo dei prompt;
- selezione finale dei 40 prompt tecnici.

Restano quindi subordinate al catalogo definitivo:

- identità e copertura degli otto casi di trasferimento;
- spazio effettivo delle nove label e forma reale dei 14 insight peer;
- misura descrittiva dell'astensione in-catalogo;
- qualsiasi verifica local-seen, Normal o OOD.

Restano subordinate al producer alternativo, non ancora configurato:

- conformità dello stesso schema sull'altro producer;
- parità dei campi fissi e dei cap fra producer;
- prontezza del braccio producer-swap.

## Congelamento da sottoporre al gate

`config/pilot_preflight.json` congela l'envelope già determinabile: modello e revisione; endpoint;
PID, comando, ambiente e versione del processo vLLM; record e script di avvio; renderer e politica
local-first con hash; tre schemi canonici e la derivazione della grammatica vLLM con hash;
snapshot, configurazione e chat template del tokenizer;
temperatura, seed, candidati 2048/3072/4096, riserva output 512, margine 256 e zero retry
strutturali.

Non viene presentato come congelamento completo. Restano intenzionalmente nulli il manifest
scientifico, l'hash del file dei 40 prompt e il budget selezionato: i primi due dipendono dal
catalogo definitivo e dai dati di sviluppo; il terzo può essere scelto solo dalla sonda sui
prompt reali. Il valore 2048 osservato sulla fixture sintetica è soltanto provvisorio. Modello,
endpoint, tariffa e conformità del producer alternativo restano un blocco separato.

## Script e guardie

Preparazione offline dei prompt reali, possibile solo quando esiste un manifest autonomo dello
Studio 2 congelato per la pre-sonda della Fase 03:

```bash
/home/luca/fot-exp2/env-vllm/bin/python -m studio2.fase03.prepare_gate \
  --input-manifest /percorso/al/manifest_pilot_studio2.json
```

Presentazione del piano, sempre a zero chiamate:

```bash
python3 -m studio2.fase03.run_pilot
```

Presentazione della sonda di conformità del producer, anch'essa a zero chiamate:

```bash
python3 -m studio2.fase03.producer_probe
```

La sonda tecnica autorizzata sulla fixture `cap_stress` usa acknowledgement e directory
separati. È stata eseguita una sola volta e documentata in `PROVISIONAL_STRESS_PROBE.md`; il suo
percorso non può scrivere `frozen_gate_config.json`:

```bash
/home/luca/fot-exp2/env-vllm/bin/python -m studio2.fase03.run_pilot \
  --stage provisional-stress-budget \
  --prepared-dir studio2/fase03/prepared/provisional_cap_stress \
  --results-dir studio2/fase03/results/provisional_cap_stress \
  --execute --acknowledge EXECUTE_PHASE03_PROVISIONAL_STRESS_PROBE
```

Lo script di esecuzione richiede insieme `--execute`, uno stage esplicito e l'acknowledgement
`EXECUTE_PHASE03_PRELIMINARY_PILOT`. Lo stage `stability` rifiuta di partire finché lo stage
`budget` non ha scritto una configurazione congelata valida.

Nel pilot i retry automatici sono disabilitati: un errore al primo tentativo è un risultato del
gate e non viene nascosto. La riserva di 15 chiamate è contabile ma non autorizzata; un suo uso
richiederebbe una decisione separata e produrrebbe un artefatto di remediation distinto.

## Implementazione già svolta oltre il solo preflight

Sono implementati: renderer A/B-LF/E-LF; selettore deterministico dei 40 prompt; calcolo offline
della capienza; sonda di budget con freeze della configurazione; runner sequenziale 40×3; logging
forense; rilevazione delle divergenze; sonda di conformità per due insight per agente e supporto
a un producer alternativo configurabile. Solo il percorso provvisorio sintetico della sonda è
stato eseguito; gate e producer non lo sono stati. Lo stato puntuale è in
`IMPLEMENTATION_STATUS.md`. La presenza del codice non autorizza ulteriori esecuzioni.

## Stima preventiva

| Blocco | Chiamate pianificate |
| --- | ---: |
| Sonda pre-gate di budget | 3 per candidato, massimo 9 |
| Gate di stabilità, 40 × 3 | 120 |
| Conformità producer Qwen, due insight per agente | 8 |
| Conformità producer alternativo, differita | 8 |
| **Totale con entrambi i producer** | **145** |
| Riserva operativa | 15 |
| **Pianificato con riserva** | **160** |
| Hard stop | **200** |

La sonda sintetica a 2048 ha richiesto 247,7 secondi sommando le tre latenze: A 32,8 s, B-LF
152,5 s ed E-LF 62,3 s. La proiezione pesata sui 40 prompt e tre ripetizioni vale circa 3,08 ore,
ma deriva da sole tre osservazioni sintetiche ed è stata influenzata dalla compilazione JIT
tardiva. Per la ripetizione sui prompt reali si pianificano **4–7 minuti** se passa il primo
candidato e **20–35 minuti** se occorrono tutti e nove i tentativi. Per il gate si mantengono
intervalli cautelativi di **3–5 ore** a 2048, **4,5–7 ore** a 3072 e **6–9 ore** a 4096. La
vecchia stima unica 03.0 di 3–6 ore non copriva esplicitamente prompt fino a 9.875 token e thinking
massimo. Non si stimano varianti parallele, perché 8001@16384 sequenziale è l'unica sequenza
verificata.

Il costo API diretto locale è **€0** sia per la sonda sia per il gate; energia e costo-opportunità
GPU non sono prezzati. Durata e costo del producer alternativo restano ignoti finché provider,
modello e tariffa non sono fissati.

## Perimetro dell'eventuale GO

Un GO potrà valere soltanto per la combinazione effettivamente verificata di: radice e revisione
del modello, processo/endpoint vLLM, 40 prompt e relativi hash, schema, tokenizer e configurazione
di generazione congelata. Non sceglierà il modello definitivo e non si estenderà per analogia a
un altro endpoint, budget, catalogo, producer o popolazione sperimentale.
