# Specifica della sotto-fase 03.10 — harness API e input reali del pilot

Data: **2026-09-14**. Profilo: **implementativo**. Base: `origin/main` a
`46c0b623f55154684f326a8523521fb28991fb09`. Nessuna chiamata a modelli e nessuna simulazione
sono autorizzate in questa sotto-fase. Gli artefatti eseguibili restano `pending` finché non sono
disponibili esempi Normal da `normal_dev`, sedici insight reali validi e il tokenizer pinnato sul
server.

## 1. Contratti e dipendenze

L'harness estende i moduli esistenti senza modificarli. Usa:

- pseudolabel, owner e derangement congelati in `origin/main`, tag
  `studio2-fase03-pseudolabel-frozen-001`;
- evidence 03.6 dal commit `2f6dd8de38b944e61853e605202c4c376a90585d` e dalla release
  `studio2-fase03-evidence-v1`, archivio SHA-256
  `3e1eb87f38ff3fc6dd3346476785d06c2b98944b209f7f58706b3c71c1676999`;
- schema insight 03.12 esclusivamente nei byte del commit
  `e058cb07dceeefa8eb4a4b6d1f6fcab5aad483db`, manifest SHA-256
  `d6ef52de0f573edf3e5d6eb5ad3530400c5f63e6bcfa6579a93f21fdfb8865b5`;
- piano statistico 03.8 dal branch `codex/studio2-piano-statistico` come specifica
  **proposta**, non congelata;
- `normal_dev` della 03.9 quando sarà specificato, prodotto e conservato. N1–N5, `cal_thr`,
  `far_ver` e i dieci Normal del pilot non sono esempi locali.

Ogni dipendenza è controllata per SHA-256 prima dell'uso. Un mismatch, un'origine non
scientifica, un input di test/OOD o una dipendenza mancante causa un arresto fail-closed.

## 2. Ordine di presentazione delle label — proposta 1a

Il mapping e il `label_space` evaluator-side di 03.7 non cambiano. Soltanto la presentazione nel
prompt usa l'ordine crescente di:

`SHA-256("studio2-fase03-presentation-v1|" + label)`.

L'ordine risultante, estratto una sola volta, è:

1. `S2-CLS-MHMU4`
2. `S2-CLS-HEW25`
3. `S2-CLS-FD3GZ`
4. `S2-CLS-3ZGWQ`
5. `S2-CLS-GSX3L`
6. `S2-CLS-4AMS4`
7. `S2-CLS-TYFPG`
8. `S2-CLS-QRCCB`

`Normal` è aggiunta in ultima posizione dove il contratto la impone. Rispetto all'ordine di
catalogo F1, F2, F3, F8, F10, F13, F14, F15, la correlazione di Spearman sulle otto label di fault
è **−0,38095238095238093** (`sum(d²)=116`). È un controllo descrittivo, non un criterio di
accettazione; non si rilancia il namespace per ottenere un'altra correlazione. L'autore deve
accettare o respingere questa proposta prima del freeze dei prompt.

## 3. Esempi locali

Per ogni agente il pacchetto contiene:

- due esempi del fault posseduto: **batch 1, finestra 1** e **batch 2, finestra 1** del lotto
  `fault_dev_001`;
- un esempio Normal dal lotto `normal_dev`, scelto con la regola congelata da 03.9. Finché quella
  specifica non è disponibile, la proposta di interfaccia è «primo run assegnato all'agente,
  finestra 1», ma 03.10 non la promuove a decisione.

Le scelte usano solo indici e metadati pre-specificati, mai il contenuto. Il testo è il `.txt`
neutrale di 03.6 o la sua estensione a `normal_dev`; nessun numero di fault, IDV o meccanismo entra
nei campi prompt-facing. Gli identificativi reali restano nel sidecar evaluator-side.

## 4. Insight del pilot e ordine producer → gate — proposta 1c

B-LF ed E-LF richiedono una libreria scientifica completa di **16 insight**, due per owner; ogni
ricevente vede i 14 peer. Non è possibile costruire i prompt reali con placeholder e chiamarli
scientifici.

Proposta all'autore: anticipare nella 03.13 le **8 chiamate della sonda di conformità del producer
Qwen** prima della sonda di budget. L'ordine diventa:

1. assemblaggio offline di evidence, esempi e cinque campi fissi;
2. 8 chiamate producer Qwen, zero retry automatici;
3. validazione integrale della libreria e diff B↔E con il validatore 03.12;
4. rendering e conteggio offline dei 40 prompt;
5. sonda di budget A/B-LF/E-LF, poi gate 40×3.

Le chiamate totali non cambiano. Senza questa inversione, la sonda di budget non può usare i 14
insight reali richiesti dal PREFLIGHT. La decisione resta dell'autore; questa finestra non esegue
alcuna delle otto chiamate.

Il prompt producer mostra i cinque campi serializzati dal verbalizzatore e permette di scrivere
solo `observed_pattern`. Elenca esplicitamente i falsi positivi conservativi accolti da 03.12:
`normal`, `unknown`, `valve`, `valvola`, `feed`, `step`, `A/B`, e qualunque sequenza `x` + spazi +
`mv`/`meas`, anche dentro parole comuni come `six MV values` ed `exmv`. Prima dell'accettazione si
applica il validatore 03.12 senza riparazioni, tagli o retry nascosti.

`variable_ids` è derivato senza giudizio manuale dal JSON evidence della finestra sorgente: per
ogni XMEAS si prende il massimo, sulle finestre disponibili, dei valori assoluti di shift e slope
divisi per le rispettive soglie e dei rapporti residual/diff divisi per le rispettive soglie; si
conservano gli otto ID col punteggio maggiore, tie-break numerico sull'ID. La regola resta definita
anche quando `dominant_variables` è vuoto e non usa il numero del fault.

## 5. Selezione deterministica dei 40 prompt

Namespace: `studio2-fase03-pilot-selection-v1`; nessun seed pseudo-casuale e nessun rilancio.

1. Fra le biiezioni agente→fault senza punti fissi rispetto all'owner locale, si sceglie quella
   con il minore SHA-256 del JSON canonico preceduto dal namespace.
2. Per ogni coppia agente/fault così fissata, il caso di trasferimento è il minimo SHA-256 di
   `namespace|transfer|agent_id|evidence_id`, fra tutte le finestre di sviluppo di quel fault.
3. Quel caso entra in A, B-LF ed E-LF.
4. Fra gli altri casi fault di sviluppo localmente unseen per l'agente, si sceglie quello col
   maggior conteggio token del prompt B-LF completo. Pareggio: `case_id` lessicograficamente
   maggiore, coerente col selettore 03.0. Entra in B-LF ed E-LF.

Il risultato deve avere 8 A, 16 B-LF, 16 E-LF, 40 prompt distinti, tutti gli agenti bilanciati e
gli otto fault coperti una volta nelle triplette. Il manifest eseguibile conserva il formato dello
schema esistente; un sidecar autonomo conserva, per ogni testo/esempio/insight, origine, commit,
release, percorso e SHA-256. Nessun manifest incompleto riceve lo stato
`FROZEN_FOR_PHASE03_PRE_GATE`.

## 6. Logging §8.7

Un record JSONL per tentativo contiene almeno: prompt/agente/caso/condizione/ripetizione,
timestamp UTC, provider e modello richiesto, **modello restituito**, request ID, system
fingerprint/versione, capacità dichiarate di temperatura e seed, configurazione di generazione,
SHA-256 e byte di prompt e risposta raw, latenza, token prompt/completion/total, finish reason,
troncamento, validità del parsing e dello schema, errore strutturato, numero di tentativo e retry.
La risposta raw è conservata. I record sono validati prima dell'append e la scrittura è protetta
da flush + `fsync`; non si sovrascrive un log esistente.

## 7. Canary e audit

Il set canary contiene 10 prompt: **2 A, 4 B-LF, 4 E-LF**. Il selettore deterministico minimizza,
in ordine, lo sbilanciamento marginale già accumulato su agente e fault e usa come tie-break
SHA-256 di `studio2-fase03-canary-v1|prompt_sha256`. L'output atteso, congelato al primo run,
contiene coppia (`abstain`, `predicted_label`) e hash raw. Cambia il comportamento solo la coppia;
l'hash raw è forense. Il file di aspettative è create-once.

L'audit prende `ceil(10% × N)` prompt del nucleo, con selezione deterministica bilanciata su fault,
agente e condizione e tie-break SHA-256 di `studio2-fase03-audit-v1|prompt_id`. È eseguito a R=3 e
distribuito nel tempo. L'analisi primaria usa sempre la prima ripetizione; la maggioranza R=3 è
una sensibilità separata. Nessun cambio a R=3 avviene a studio già iniziato.

## 8. Metriche e inferenza statistica

Per ogni condizione, popolazione e strato si producono:

1. `accuracy_all = correct / total`, con astensione e risposta non valida non corrette;
2. `abstention_rate = abstained / total`, senza trasformare i non validi in astensioni;
3. `accuracy_non_abstained = correct / (total - abstained)`, inclusi i non validi nel
   denominatore perché non sono astensioni; `null` soltanto con denominatore zero;
4. conteggi grezzi `correct`, `abstained`, `non_abstained`, `invalid`, `total`.

Il raccordo con `metrics.json` della baseline numerica 03.9 è un adapter fail-closed, non una
seconda definizione degli endpoint. Rinomina `accuracy` in `accuracy_all`, `n` in `total` e
`abstentions` in `abstained`; preserva `non_abstained` soltanto dopo aver verificato
`non_abstained = n - abstentions`. La 03.9 arresta l'esecuzione sugli input non validi e scrive
righe valutate con `valid=true`: solo dopo aver verificato l'intero contratto valid-only
l'adapter espone esplicitamente `invalid=0`. Un campo `invalid` inatteso, conteggi o rapporti
incoerenti e denominatori nulli rappresentati diversamente da `null` causano un arresto. Nessun
invalido viene convertito in astensione o predizione valida e i tre valori numerici sorgente sono
copiati, non ricalcolati.

Il bootstrap ricampiona con reinserimento i cluster fisici **dentro ciascuna delle otto
pseudolabel**, mantiene insieme le 7 righe local-unseen o la singola riga local-seen, usa 10.000
repliche, seed 20260913 e namespace `studio2-fase03-piano-statistico-v1`, e riporta percentile
2,5/97,5%, q05, repliche a denominatore nullo e `independence_claim=false`.

Come implementazione `pending` della proposta 03.8: H1/H2 usano la soglia di Hoeffding sulle
medie di cluster; H3 usa il test score di Tango con margine 0,125; il sign-flip è soltanto
supplementare. Questi risultati non diventano confermativi finché l'autore non congela piano,
gerarchia, livello e margine.

## 9. Guardie e capienza

Prima di qualunque chiamata si verificano insieme: impronte di pseudolabel/assignment/E, schema e
validatore 03.12, manifest evidence, manifest scientifico, tokenizer (`tokenizer.json`,
`tokenizer_config.json`, chat template/revisione) ed endpoint (modello/revisione, comando,
ambiente, vLLM e fingerprint). Un solo mismatch arresta tutto.

Sul server, per ogni prompt e candidato deve valere:

`input_tokens + thinking_token_budget + 512 + 256 <= 16384`.

Il conteggio usa il tokenizer pinnato e il chat template reale. Nessun conteggio per caratteri o
tokenizer sostitutivo può congelare la capienza.

## 10. Stato di questa specifica

Le proposte 1a e 1c richiedono decisione dell'autore. Le regole statistiche ereditate da 03.8
restano `pending`. Il manifest reale resta incompleto finché mancano `normal_dev` e la libreria di
16 insight; codice e fixture possono essere verificati offline senza attenuare queste guardie.
