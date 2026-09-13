Formato pseudolabel CONFERMATO: `S2-CLS-[A-Z0-9]{5}`; nessuna rigenerazione richiesta a 03.7.

# Decisione pre-specificata 03.12 — schema insight v1.0.0

Data 2026-09-13; base d815ce9. Stato: proposta implementata, in attesa di verifica indipendente.
Nessun insight scientifico prodotto o esaminato. Vale identicamente per entrambi i producer.

## Campi e budget

Tutti i sei campi sono obbligatori; proprietà ulteriori vietate. Caratteri = code point Unicode;
byte = UTF-8. Token = Qwen/Qwen3.8-27B-FP8, revisione
`017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`, encode(add_special_tokens=False), senza chat template.

| Campo | Tipo | Origine | Cap | Fonte |
| --- | --- | --- | --- | --- |
| insight_id | string | verbalizzatore | S2-INS- seguito da 3 cifre (10 caratteri) | preflight; scelta di progetto |
| source_agent | string | verbalizzatore | agent_1…agent_8 (7 caratteri) | preflight; piano §8.1 |
| pseudolabel | string | verbalizzatore | 12 caratteri, regex confermata | interfaccia preflight/03.7; D10 |
| evidence_scope | string non vuota | verbalizzatore | 240 caratteri, 64 token | 240: preflight; 64: scelta di progetto |
| variable_ids | array di stringhe uniche | verbalizzatore | 1–8 ID; XMEAS(1…41), XMV(1…12), massimo 9 caratteri/ID | preflight; limiti TEP, scelta di progetto |
| observed_pattern | string non vuota | producer | 800 caratteri e 192 token | PREFLIGHT_03_0, scelta di progetto motivata da §8.9 |

Per elemento completo: massimo **1400 caratteri e 384 token** sul JSON canonico
(`ensure_ascii=False`, chiavi ordinate, separatori virgola/due punti, nessuna newline).
Questi due limiti complessivi e il cap di evidence_scope sono scelte di progetto conservative,
non valori dedotti dai paper: rendono finito il budget del record oltre alla narrativa.
Non sono un risultato di capienza dei prompt: 03.10 deve misurarli col chat template reale.
I campi corti hanno cap strutturale e partecipano al limite complessivo, senza ulteriori cap token.

Cardinalità invariabile: **2 per fault, 16 nella libreria omogenea di un producer, 14 peer**
per ricevente (piano §6.10/§8.4, preflight). Normal non produce insight; Unknown è astensione,
non una label. Gli otto owner e la label Normal arrivano esplicitamente da 03.7:
nessuna assunzione sull'ultima posizione, nessuna assegnazione o permutazione scelta qui.

## Separazione delle responsabilità

03.6/03.10 producono i cinque campi fissi da evidence di sviluppo, conservati in un manifest
fidato separato; gli ID opachi non devono derivare dal numero reale del fault.
Il validatore confronta esattamente tutti i campi fissi col manifest per ogni record B.
La risposta completa del producer viene validata prima di qualsiasi ricomposizione: non si
riparano silenziosamente alterazioni dei campi fissi. Il serializer usa i valori deterministici
validati. Si conserva il raw per misurare la conformità effettiva. Il producer scrive solo la
narrativa; nessun retry automatico o taglio del testo (preflight: zero retry nel pilot).

Gli identificatori sono letterali, case-sensitive, senza spazi o zeri iniziali; nella narrativa
occorre almeno un ID e tutti gli ID citati devono appartenere a variable_ids. Parafrasi quali
“reactor temperature” e “temperatura del reattore” sono vietate. Lo scanner riconosce famiglie
lessicali di nomi fisici e varianti degli ID; non dimostra l'assenza di ogni possibile parafrasi
in linguaggio naturale. La verifica indipendente deve valutare questa copertura prima del tag.
Non si verifica qui che la narrativa sia scientificamente supportata dai run: validità non è EFT.

## Anti-leakage ed E

Tutti i campi visibili sono scansionati: numeri di fault F/IDV/fault/guasto, nomi di meccanismo
(step, random variation, slow drift, sticking valve e traduzioni), chiavi e descrizioni D1.
Fuori dal campo pseudolabel sono vietate anche pseudolabel, Normal e Unknown. Non si vietano
numeri di misura o descrittori neutrali solo perché coincidono con un numero di fault.
Dizionario locale versionato; nessun import da phase_b. Limite: uno scanner lessicale non è
una prova semantica universale; falsi positivi e parafrasi non elencate richiedono revisione.

E si applica **dopo** il filtro peer B. Il tool riceve da 03.7 una biiezione senza punti fissi
sulle sette label peer (oppure otto per audit della libreria globale). Non genera il mapping.
Confronta file già canonici byte per byte: rifiuta anche cambi di whitespace o ordine dei record.
Costruisce il byte atteso modificando solo pseudolabel e verifica l'uguaglianza col file E.
Registra hash B/E e gli offset dei byte diversi. Ownership si verifica su B: su E resta quella
originaria e non va rivalidata rispetto alla label corrotta.

## Metriche (§8.7) e interfaccia 03.10

`conformity_metrics` riceve log per insight e tentativo: producer, condition, insight_id,
attempt (1-based contiguo), raw (JSON originale), truncated (bool esplicito), prompt_tokens
(numero intero oppure null), request_id; i metadati restano fuori dai campi consumer.
Ricalcola validità con lo stesso validatore. Per producer/condizione riporta:
validi al primo tentativo / insight tentati, validi per tentativo / tentativi, numero totale di
retry, retry fino al primo valido per insight (null se mai valido), troncamenti dichiarati,
superamenti cap, token effettivi di narrativa e record per tentativo, somma dei token misurabili.
I token del prompt sono registrati per request_id senza duplicare chiamate con due insight.
Un JSON non parsabile ha token insight null, non zero; un cap raggiunto non prova troncamento.
Gli esiti successivi al primo valido sono vietati. Nessuna metrica sintetica è una misura del producer.

03.10 dovrà sostituire il riferimento allo schema, passare manifest fisso/owner/Normal,
validare ogni libreria producer integralmente, filtrare peer e usare il diff prima del rendering.
Dovrà conservare i raw, i metadati API §8.7 e questi log, aggiornare gli hash di preflight,
misurare la capienza locale reale e riverificare i 40 prompt. I file harness esistenti restano intatti.

## Differenze e motivazione bibliografica

Rispetto a schemas/insight.schema.json: stessi sei campi e namespace; range degli ID limitati
al TEP, stringhe non solo whitespace; aggiunti cap scope/record, controllo manifest, anti-leakage,
tracciabilità degli ID narrativi, metriche e prova E sui byte reali, non solo uguaglianza dei dict.
Lo schema JSON esprime i vincoli strutturali; i vincoli token/manifest/leakage sono nel validatore.

Fonti locali: piano §8.9 integrale, D12/D10, §8.1/8.4/8.7; docs/letteratura.md schede
EviFDD-Agent, ACE (P001), Fed-ICL (P041), SYNAPSE (P065). EviFDD motiva ID letterali e
serializzazione deterministica; la sua URR non equivale alla nostra validità producer.
P041 mostra un cap di 256 token nel proprio compito, non giustifica numericamente 192 qui;
P001 non dimostra superiorità della concisione; P065 delimita la novità e il consumer-swap.
Le schede storiche che parlano del “nostro insight” si riferiscono al primo studio.
Il confronto con phase_b (5 campi, 4 agenti) è solo implementativo/storico, non fonte scientifica.

Tag proposto `studio2-fase03-schema-insight-frozen-001`, NON creato. Condizioni: verifica
indipendente OK su decisione, scanner, test, tokenizer reale e impronte; chiusura delle eventuali
correzioni in nuova revisione; autorizzazione dell'autore al tag (MAINTENANCE §8.4).
