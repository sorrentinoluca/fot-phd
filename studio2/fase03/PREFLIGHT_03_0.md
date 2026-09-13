# Fase 03.0 — preflight del pilot preliminare Qwen-27B

Stato: **envelope tecnico 8001@16384 congelato; esecuzione sospesa sul catalogo definitivo,
sui suoi input derivati e sul producer alternativo**.

Questa sotto-fase non ha contattato endpoint HTTP, non ha tokenizzato tramite server, non ha
eseguito inferenze e non ha aperto dati finali. Predispone un pilot tecnico preliminare su
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
  Si congela il più piccolo budget provato senza troncamenti e senza errori di parsing su tutti
  e tre gli stress prompt. Se nessun candidato passa, il gate non parte.
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
local-first con hash; tre schemi; snapshot, configurazione e chat template del tokenizer;
temperatura, seed, candidati 2048/3072/4096, riserva output 512, margine 256 e zero retry
strutturali.

Non viene presentato come congelamento completo. Restano intenzionalmente nulli il manifest
scientifico, l'hash del file dei 40 prompt e il budget selezionato: i primi due dipendono dal
catalogo definitivo e dai dati di sviluppo; il terzo può essere scelto solo dalla sonda. Modello,
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

Lo script di esecuzione richiede insieme `--execute`, uno stage esplicito e l'acknowledgement
`EXECUTE_PHASE03_PRELIMINARY_PILOT`. Lo stage `stability` rifiuta di partire finché lo stage
`budget` non ha scritto una configurazione congelata valida.

Nel pilot i retry automatici sono disabilitati: un errore al primo tentativo è un risultato del
gate e non viene nascosto. La riserva di 15 chiamate è contabile ma non autorizzata; un suo uso
richiederebbe una decisione separata e produrrebbe un artefatto di remediation distinto.

## Implementazione già svolta oltre il solo preflight

Sono già implementati, ma non eseguiti: renderer A/B-LF/E-LF; selettore deterministico dei 40
prompt; calcolo offline della capienza; sonda di budget con freeze della configurazione; runner
sequenziale 40×3; logging forense; rilevazione delle divergenze; sonda di conformità per due
insight per agente e supporto a un producer alternativo configurabile. Lo stato puntuale è in
`IMPLEMENTATION_STATUS.md`. La presenza del codice non autorizza l'esecuzione.

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

Il precedente congelato di 540 chiamate ha richiesto 26.636 secondi, in media 49,4 secondi per
chiamata, con thinking budget 1024. Per pianificare senza una nuova inferenza, quel tempo è scalato
linearmente col cap e maggiorato del 25% per prompt fino a 9.875 token: la sonda completa da nove
chiamate richiede circa **25–40 minuti**; il gate 40×3 circa **4–5 ore** a 2048, **6–7,5 ore** a
3072 o **8–10 ore** a 4096. Sonda più gate: circa **4,5–10,7 ore sequenziali**. La vecchia stima
03.0 di 3–6 ore è quindi superata. Non si stimano varianti parallele, perché 8001@16384
sequenziale è l'unica sequenza verificata.

Il costo API diretto locale è **€0** sia per la sonda sia per il gate; energia e costo-opportunità
GPU non sono prezzati. Durata e costo del producer alternativo restano ignoti finché provider,
modello e tariffa non sono fissati.

## Perimetro dell'eventuale GO

Un GO potrà valere soltanto per la combinazione effettivamente verificata di: radice e revisione
del modello, processo/endpoint vLLM, 40 prompt e relativi hash, schema, tokenizer e configurazione
di generazione congelata. Non sceglierà il modello definitivo e non si estenderà per analogia a
un altro endpoint, budget, catalogo, producer o popolazione sperimentale.
