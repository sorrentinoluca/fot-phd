# Fase 03.0 — preflight del pilot preliminare Qwen-27B

Stato: **implementazione offline disponibile; esecuzione sospesa sui prerequisiti scientifici
successivi alla Fase 02**.

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
  tokenizer della revisione locale. Per ogni candidato dovrà valere
  `input massimo + thinking budget + 512 output + 256 margine <= 7168`.
  In questa finestra lo stesso percorso è verificato soltanto su fixture sintetiche dichiarate,
  che non congelano alcuna configurazione.
- Prima del gate 40×3 si esegue una sonda A/B-LF/E-LF sui soli candidati staticamente capienti.
  Si congela il più piccolo budget provato senza troncamenti e senza errori di parsing su tutti
  e tre gli stress prompt. Se nessun candidato passa, il gate non parte.
- Lo script di stabilità rifiuta di partire se prompt, schema, processo vLLM o configurazione
  differiscono dalle impronte congelate dopo la sonda di budget.

## Origine futura dei 40 prompt

I prompt reali dovranno provenire esclusivamente da artefatti di sviluppo dello Studio 2 creati
dopo aver chiuso il catalogo, generato i 40 nuovi run fault e prodotto le relative
feature/evidence/verbalizzazioni. Il report della Fase 02 colloca esplicitamente questi tre
elementi in «Fuori dalla Fase02»: non sono un suo manifest né un suo output.

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

## Artefatti esistenti da sincronizzare

Il report di chiusura della Fase 02, incluso «Fuori dalla Fase02», è dichiarato esistente
dall'autore ma non compare nei riferimenti remoti fetchati al commit `9e3d903`; percorso e hash
restano quindi da sincronizzare. Quando sarà disponibile si importeranno soltanto decisioni e
artefatti che il report dichiara realmente conclusi, senza dedurre i deliverable esclusi.

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
| Sonda pre-gate di capienza e budget | massimo 9 |
| Gate di stabilità, 40 × 3 | 120 |
| Conformità producer Qwen, due insight per agente | 8 |
| Conformità producer alternativo, differita | 8 |
| **Totale con entrambi i producer** | **145** |
| Riserva operativa | 15 |
| **Pianificato con riserva** | **160** |
| Hard stop | **200** |

Il precedente congelato di 540 chiamate ha richiesto 26.636 secondi, in media 49,4 secondi per
chiamata, con thinking budget 1024. Poiché qui i prompt hanno 14 insight e i budget candidati
sono 2048–4096, la stima prudenziale per il solo Qwen è **3–6 ore sequenziali**. Il costo API
diretto locale è **€0**; consumo elettrico e costo-opportunità GPU non sono prezzati. Durata e
costo del producer alternativo restano ignoti finché provider, modello e tariffa non sono fissati.

## Perimetro dell'eventuale GO

Un GO potrà valere soltanto per la combinazione effettivamente verificata di: radice e revisione
del modello, processo/endpoint vLLM, 40 prompt e relativi hash, schema, tokenizer e configurazione
di generazione congelata. Non sceglierà il modello definitivo e non si estenderà per analogia a
un altro endpoint, budget, catalogo, producer o popolazione sperimentale.
