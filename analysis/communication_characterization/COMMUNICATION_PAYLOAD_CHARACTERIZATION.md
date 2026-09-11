# Caratterizzazione del payload comunicativo FoT–TEP

Stato: **analisi derivata, riproducibile, senza nuove inferenze LLM**. I risultati sperimentali e gli artefatti frozen non sono stati modificati. “Costo” indica token e latenza registrati, non costo monetario; i prezzi applicabili non sono congelati nel repository.

## Metodologia

La misura primaria del payload federato è il blocco realmente inserito nel prompt: `PEER INSIGHTS\n` + JSON UTF-8 indentato + due newline finali. Caratteri = code point Python; byte = UTF-8; parole = match Unicode dell’espressione `\b[^\W_]+(?:[’'-][^\W_]+)*\b`; righe = `splitlines()`. La dimensione del singolo insight usa l’oggetto JSON completo (`ensure_ascii=False`, `indent=2`) senza framing di array/header; per questo la somma degli insight non coincide necessariamente con il blocco trasmesso.

I token A/B/E sono **misure esatte in contesto**: differenza tra `input_tokens`/`prompt_tokens` del primo tentativo di B (o E) e A per lo stesso caso fisico, agente e ripetizione. Il valore include gli effetti di tokenizzazione ai confini del blocco e non è una tokenizzazione standalone. Per GPT il nome/versione del tokenizer non è registrato; per Qwen sono congelati modello e revisione ma non i file del tokenizer. I token standalone per insight e per C sono quindi stime lineari esplicitamente etichettate, calibrate sul rapporto token-incrementali/byte dei quattro peer block frozen.

I prompt completi A/B/E e C sono stati ricostruiti deterministicamente dai template e dagli input frozen; ogni hash è stato verificato contro i prediction log. EXP3_V2 è letto direttamente dagli oggetti Git dei tag `exp3-v2-inference-frozen-001` e `exp3-v2-results-frozen-001`, senza checkout. Le unità sono mantenute separate: caso fisico, ripetizione LLM e predizione aggregata.

## Provenienza dei dati

- Insight e routing: `phase_b/insights/final_local_insights.json`, `phase_b/insights/peer_libraries/agent_*_B.json`, `agent_*_E.json`, `phase_b/conditions/builders.py`.
- Mapping: `phase_b/config/evaluator_side/pseudolabel_mapping.json` e `condition_e_derangements.json`.
- Experiment 1: `phase_b/final_evaluation/inference/*.json[l]` e `evaluation_results.json`.
- EXP3_V2: tag Git `exp3-v2-inference-frozen-001` (`inference_outputs/records/*.json`), `exp3-v2-results-frozen-001` (`evaluation_outputs/exp3v2_confirmatory_results.json`) e payload commit `5be0c3c14e7e1601708486d56c2cb4cee29658ab` (`verbalization_outputs/neutral_text/*.txt`), registrato nel manifest di freeze. Gli artefatti non sono presenti nel working tree corrente ma restano frozen e indirizzabili negli oggetti Git.
- Experiment 2/Qwen: `phase_b/exp2/qwen/inference/*.json[l]`, `config.json` ed `evaluation/evaluation_results.json`.
- Condition C: `icl/pooled_libraries/*.json`, `icl/inference/c_records.jsonl`, `icl/full_evaluation/evaluation_results_c.json`.
- Inquadramento: `docs/fot_walkthrough_conversazione.md`, `docs/fot_walkthrough.html`, `docs/paper/FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md`, `docs/lit_review/FOT_TEP_GAP_ANALYSIS_AND_RELATED_WORK.md`, `docs/lit_review/FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md`.

### Inventario operativo

| Oggetto | Artefatto primario | Stato |
|---|---|---|
| Insight per producer | `phase_b/insights/final_local_insights.json` e `generation_runs.json` | 8 record frozen, 2 per agente |
| Prompt finali A/B/E | template `phase_b/prompts/*.txt` + builder + case/local examples/peer library | non salvati come testo autonomo; ricostruiti esattamente e verificati contro i log |
| Prompt finali C | `icl/prompts/pooled_C.txt` + `icl/conditions/builder_c.py` + pooled libraries | ricostruiti esattamente e verificati contro i log |
| Prediction log/evaluator Experiment 1 | `phase_b/final_evaluation/inference/*.jsonl`, `evaluation_results.json` | frozen |
| Prediction log/evaluator EXP3_V2 | oggetti Git `inference_outputs/*`, `evaluation_outputs/*` ai ref frozen | frozen nei ref, separati dal working tree |
| Prediction log/evaluator EXP2 Qwen | `phase_b/exp2/qwen/inference/*.jsonl`, `evaluation/*.json` | frozen |
| Mapping corretto/derangiato | `pseudolabel_mapping.json`, `condition_e_derangements.json` | evaluator-side frozen |

| esperimento | condizione | prompt unici | chiamate logiche | verifica |
|---|---|---|---|---|
| experiment_1 | A | 60 | 180 | hash SHA-256 verificati |
| experiment_1 | B | 60 | 180 | hash SHA-256 verificati |
| experiment_1 | E | 60 | 180 | hash SHA-256 verificati |
| exp3_v2 | A | 120 | 360 | hash SHA-256 verificati |
| exp3_v2 | B | 120 | 360 | hash SHA-256 verificati |
| exp3_v2 | E | 120 | 360 | hash SHA-256 verificati |
| experiment_2_qwen | A | 60 | 180 | hash SHA-256 verificati |
| experiment_2_qwen | B | 60 | 180 | hash SHA-256 verificati |
| experiment_2_qwen | E | 60 | 180 | hash SHA-256 verificati |
| experiment_1_condition_c | C | 15 | 45 | hash SHA-256 verificati |

Mapping corretto:

| fault | pseudolabel |
|---|---|
| F1 | CLS-ZOGAA |
| F8 | CLS-OJNSG |
| F10 | CLS-R463B |
| F13 | CLS-Z3ISU |

Derangement E:

| receiver | rotazione frozen |
|---|---|
| agent_1 | CLS-OJNSG→CLS-R463B; CLS-R463B→CLS-Z3ISU; CLS-Z3ISU→CLS-OJNSG |
| agent_2 | CLS-ZOGAA→CLS-R463B; CLS-R463B→CLS-Z3ISU; CLS-Z3ISU→CLS-ZOGAA |
| agent_3 | CLS-ZOGAA→CLS-OJNSG; CLS-OJNSG→CLS-Z3ISU; CLS-Z3ISU→CLS-ZOGAA |
| agent_4 | CLS-ZOGAA→CLS-OJNSG; CLS-OJNSG→CLS-R463B; CLS-R463B→CLS-ZOGAA |

## Payload prodotto e ricevuto

Sono presenti **8 insight unici**, 2 per ciascun producer. La libreria frozen completa occupa 3108 caratteri e 3125 byte inclusa la newline terminale. Ogni consumer federato riceve 6 insight (due da ciascuno dei tre peer):

| consumer | insight | caratteri | byte | parole | righe | token GPT esatti* | token Qwen esatti* |
|---|---|---|---|---|---|---|---|
| agent_1 | 6 | 2289 | 2304 | 240 | 46 | 664 | 724 |
| agent_2 | 6 | 2327 | 2336 | 244 | 46 | 684 | 749 |
| agent_3 | 6 | 2410 | 2420 | 258 | 46 | 681 | 747 |
| agent_4 | 6 | 2361 | 2378 | 250 | 46 | 690 | 754 |

*Incremento in contesto B−A; non tokenizzazione standalone.*

Statistiche per insight serializzato:

| metrica | media | mediana | min | max | dev. std. popolazione |
|---|---|---|---|---|---|
| characters | 372.12 | 380.00 | 320 | 412 | 25.94 |
| utf8_bytes | 374.25 | 382.00 | 321 | 412 | 26.01 |
| words_unicode_regex | 41.00 | 40.00 | 33 | 46 | 4.03 |
| lines | 7.00 | 7.00 | 7 | 7 | 0.00 |
| gpt56_terra_tokens_estimated | 107.75 | 110.00 | 92 | 119 | 7.69 |
| qwen38_27b_tokens_estimated | 118.12 | 120.50 | 101 | 130 | 8.33 |

Le due righe token sono **stime**, non misure del tokenizer del singolo insight.

### Tokenizzazione e configurazione

| consumer | tokenizer | configurazione | token/unità 4 receiver | stato |
|---|---|---|---|---|
| GPT-5.6-terra | nome/versione tokenizer non frozen | Responses API; openai 3.6.0; reasoning medium | 2719 | esatto in contesto |
| Qwen3.8-27B-FP8 | server tokenizer della revisione 017b9c7…; file non frozen | vLLM 0.28.0; SDK 3.8.0; temp 0; seed 20260829 | 2974 | esatto in contesto |

La stima standalone usa rispettivamente 0.288091 e 0.315109 token/byte, calibrati sui peer block. Non è usata per i totali A/B/E.

## Costo producer, consumer e trasferimento

La produzione frozen è avvenuta una sola volta: 4 chiamate, 7954 input token, 820 output token, 0 reasoning token e 9.0 s di latenza provider misurabile. Gli esperimenti successivi riusano gli stessi 8 insight; non si riaddebita la produzione.

| producer | fault | chiamate | insight | input tok | output tok | reasoning tok | latenza s |
|---|---|---|---|---|---|---|---|
| agent_1 | F1 | 1 | 2 | 1961 | 220 | 0 | 2.0 |
| agent_2 | F8 | 1 | 2 | 2002 | 201 | 0 | 3.0 |
| agent_3 | F10 | 1 | 2 | 1996 | 204 | 0 | 2.0 |
| agent_4 | F13 | 1 | 2 | 1995 | 195 | 0 | 2.0 |

Il trasferimento non genera una chiamata separata: il relativo costo token è l’incremento nel prompt del consumer. Totali per esecuzione:

| esperimento | cond. | chiamate logiche | chiamate provider | byte payload | token payload* | input tok | output tok | reasoning tok | corrette unseen | accuracy |
|---|---|---|---|---|---|---|---|---|---|---|
| experiment_1 | A | 180 | 180 | 0 | 0 | 291567 | 28155 | 9733 | 0/36 | 0.0000 |
| experiment_1 | B | 180 | 180 | 424710 | 122355 | 413922 | 27888 | 8684 | 31/36 | 0.8611 |
| experiment_1 | E | 180 | 181 | 424710 | 122355 | 413970 | 28792 | 9874 | 3/36 | 0.0833 |
| exp3_v2 | A | 360 | 360 | 0 | 0 | 581670 | 55426 | 19156 | 0/72 | 0.0000 |
| exp3_v2 | B | 360 | 362 | 849420 | 244710 | 826476 | 57236 | 19378 | 68/72 | 0.9444 |
| exp3_v2 | E | 360 | 360 | 849420 | 244710 | 826380 | 59614 | 20365 | 4/72 | 0.0556 |
| experiment_2_qwen | A | 180 | 180 | 0 | 0 | 287205 | 101766 | 83838 | 0/36 | 0.0000 |
| experiment_2_qwen | B | 180 | 180 | 424710 | 133830 | 421035 | 150705 | 127833 | 34/36 | 0.9444 |
| experiment_2_qwen | E | 180 | 180 | 424710 | 133830 | 421035 | 151179 | 128271 | 1/36 | 0.0278 |
| experiment_1_condition_c | C | 45 | 45 | 570060 | stima soltanto | 209118 | 5869 | non disponibile | 15/15 | 1.0000 |

*Esatti in contesto per A/B/E; C non è isolabile esattamente.* Le chiamate provider possono superare quelle logiche in presenza di retry. I reasoning token sono un sottoinsieme degli output/completion token, non vanno sommati di nuovo. La latenza consumer è disponibile solo per i record GPT con `created_at` e `completed_at`; è `not_recorded` per Qwen e C. Il costo monetario è **non disponibile**.

Totale federato B+E per esperimento (A non aggiunge payload):

| esperimento | round logici | blocchi trasferiti | source→consumer ripetuti | insight consegnati | byte | token in contesto |
|---|---|---|---|---|---|---|
| experiment_1 | 2 | 360 | 1080 | 2160 | 849420 | 244710 |
| exp3_v2 | 2 | 720 | 2160 | 4320 | 1698840 | 489420 |
| experiment_2_qwen | 2 | 360 | 1080 | 2160 | 849420 | 267660 |

Distribuzione della condizione B per consumer (token su tutti i tentativi):

| esperimento | consumer | provider call | input tok | output tok | reasoning tok |
|---|---|---|---|---|---|
| experiment_1 | agent_1 | 45 | 102333 | 6462 | 1530 |
| experiment_1 | agent_2 | 45 | 103953 | 6308 | 1429 |
| experiment_1 | agent_3 | 45 | 103728 | 7369 | 2816 |
| experiment_1 | agent_4 | 45 | 103908 | 7749 | 2909 |
| exp3_v2 | agent_1 | 91 | 204348 | 13363 | 4122 |
| exp3_v2 | agent_2 | 90 | 207540 | 13514 | 3671 |
| exp3_v2 | agent_3 | 90 | 207090 | 14868 | 5385 |
| exp3_v2 | agent_4 | 91 | 207498 | 15491 | 6200 |
| experiment_2_qwen | agent_1 | 45 | 103740 | 34320 | 28833 |
| experiment_2_qwen | agent_2 | 45 | 105675 | 38310 | 32430 |
| experiment_2_qwen | agent_3 | 45 | 105945 | 38967 | 33237 |
| experiment_2_qwen | agent_4 | 45 | 105675 | 39108 | 33333 |

Distribuzione della condizione B per fault reale del caso (include tutti i receiver e R=3; `Normal` resta separato):

| esperimento | fault | chiamate logiche | input tok | output tok | reasoning tok |
|---|---|---|---|---|---|
| experiment_1 | F1 | 36 | 83790 | 4650 | 677 |
| experiment_1 | F10 | 36 | 83958 | 4605 | 486 |
| experiment_1 | F13 | 36 | 83958 | 6467 | 2439 |
| experiment_1 | F8 | 36 | 84042 | 8849 | 4877 |
| experiment_1 | Normal | 36 | 78174 | 3317 | 205 |
| exp3_v2 | F1 | 72 | 167580 | 9083 | 727 |
| exp3_v2 | F10 | 72 | 168084 | 8720 | 621 |
| exp3_v2 | F13 | 72 | 167880 | 14553 | 6951 |
| exp3_v2 | F8 | 72 | 168048 | 18707 | 11079 |
| exp3_v2 | Normal | 72 | 154884 | 6173 | 0 |
| experiment_2_qwen | F1 | 36 | 85131 | 25161 | 20460 |
| experiment_2_qwen | F10 | 36 | 85443 | 26505 | 21579 |
| experiment_2_qwen | F13 | 36 | 85347 | 38508 | 33687 |
| experiment_2_qwen | F8 | 36 | 85443 | 41910 | 36828 |
| experiment_2_qwen | Normal | 36 | 79671 | 18621 | 15279 |

Latenza consumer disponibile:

| esperimento | cond. | osservazioni | somma s | media s | stato |
|---|---|---|---|---|---|
| experiment_1 | A | 180 | 417.0 | 2.32 | measured_from_provider_created_at_and_completed_at |
| experiment_1 | B | 180 | 411.0 | 2.28 | measured_from_provider_created_at_and_completed_at |
| experiment_1 | E | 180 | 407.0 | 2.26 | measured_from_provider_created_at_and_completed_at |
| exp3_v2 | A | 360 | 1148.0 | 3.19 | measured_from_provider_created_at_and_completed_at |
| exp3_v2 | B | 360 | 1123.0 | 3.12 | measured_from_provider_created_at_and_completed_at |
| exp3_v2 | E | 360 | 1153.0 | 3.20 | measured_from_provider_created_at_and_completed_at |
| experiment_2_qwen | A | 0 | non disponibile | non disponibile | not_recorded |
| experiment_2_qwen | B | 0 | non disponibile | non disponibile | not_recorded |
| experiment_2_qwen | E | 0 | non disponibile | non disponibile | not_recorded |
| experiment_1_condition_c | C | 0 | non disponibile | non disponibile | not_recorded |

## Controllo strutturale B vs E

B ed E hanno lo stesso numero di insight, stessi ID, fonti, ordine, chiavi JSON, observed pattern, caratteri, parole, righe e byte; hanno anche lo stesso conteggio token in contesto nei due consumer. **Non sono byte-identici**: E sostituisce esattamente il valore ASCII di `pseudolabel` in ciascuno dei 6 record secondo il derangement frozen. Tutte le etichette hanno 9 byte, quindi la lunghezza resta invariata.

| consumer | sostituzioni | posizioni byte diverse | byte B | byte E | GPT B | GPT E | Qwen B | Qwen E |
|---|---|---|---|---|---|---|---|---|
| agent_1 | 6 | 28 | 2304 | 2304 | 664 | 664 | 724 | 724 |
| agent_2 | 6 | 28 | 2336 | 2336 | 684 | 684 | 749 | 749 |
| agent_3 | 6 | 26 | 2420 | 2420 | 681 | 681 | 747 | 747 |
| agent_4 | 6 | 30 | 2378 | 2378 | 690 | 690 | 754 | 754 |

Nell’unità a quattro receiver le 24 sostituzioni cambiano 112 posizioni byte, senza inserimenti/cancellazioni. Il test strutturale complessivo è **PASS**.

## Efficienza descrittiva

Le seguenti normalizzazioni usano soltanto le chiamate associate alla popolazione locally-unseen. Non dimostrano superiorità di communication efficiency rispetto a un’altra famiglia di metodi.

| esperimento | casi fault fisici | pred. unseen aggregate | B corrette | B−A | B−E | byte/B corretta | token/B corretta | token per punto % |
|---|---|---|---|---|---|---|---|---|
| experiment_1 | 12 | 36 | 31 | 0.8611 | 0.7778 | 8220.19 | 2368.16 | 23.68 |
| exp3_v2 | 24 | 72 | 68 | 0.9444 | 0.8889 | 7494.88 | 2159.21 | 21.59 |
| experiment_2_qwen | 12 | 36 | 34 | 0.9444 | 0.9167 | 7494.88 | 2361.71 | 23.62 |

“Token per punto %” = incremento medio B−A per chiamata × R=3 / incremento di accuracy espresso in punti percentuali. È normalizzato per predizione aggregata; i valori totali dipenderebbero linearmente dalla dimensione del campione.

Rapporto payload/prompt completo:

| esperimento | rapporto byte | rapporto token |
|---|---|---|
| experiment_1 | 0.3251 | 0.2956 |
| exp3_v2 | 0.3256 | 0.2961 |
| experiment_2_qwen | 0.3251 | 0.3179 |
| experiment_1_condition_c | 0.8810 | non disponibile (solo stima) |

Per A il rapporto è zero. Per C il numeratore byte è la somma dei due blocchi inseriti (10 esempi pooled + 8 insight); il confronto con B non è isomorfo.

## Condizioni e unità sperimentali

- Experiment 1 e EXP2/Qwen: 15 casi fisici (12 fault + 3 Normal), 4 agenti, R=3; 60 predizioni aggregate per condizione, di cui 36 locally-unseen. Le 36 non sono 36 casi fisici indipendenti.
- EXP3_V2: 30 casi fisici (24 fault + 6 Normal), 4 agenti, R=3; 120 predizioni aggregate per condizione, di cui 72 locally-unseen.
- C: 15 casi fisici, un consumer centrale, R=3; 15 predizioni aggregate. C è post-hoc, solo su Experiment 1 e riceve 10 esempi più tutti gli 8 insight; C−B è descrittivo e non causale.
- Un payload federato statico corrisponde a un round logico, 12 archi diretti source→consumer, 4 blocchi receiver-specific, 24 consegne di insight. Operativamente il blocco viene reinserito a ogni chiamata: 180 trasferimenti di blocco per B in Experiment 1/Qwen e 360 in EXP3_V2; E replica gli stessi volumi.

## Paradigmi adiacenti

| Paradigma | Oggetto trasmesso | Unità naturale | Leggibilità | Dipendenza dal modello | Dati pubblici | Costo per round | Audit |
|---|---|---|---|---|---|---|---|
| FedMD / logit sharing | logit su esempi condivisi | scalari o byte | bassa | richiede spazio output compatibile, modelli eterogenei possibili | sì, nel FedMD canonico | `K × N_pub × C × b` uplink, più aggregazione/downlink; numeri non disponibili senza configurazione | medio: tensori e dataset sono ispezionabili ma non autoesplicativi |
| FedProto | prototipi medi per classe | scalari o byte | bassa–media | dipende dallo spazio embedding/proiezione | non necessariamente | `Σ_k C_k × d × b` uplink, più prototipi globali; numeri non disponibili | medio: vettori associati a classi, semantica indiretta |
| Adapter / LoRA federati | parametri trainabili dell’adapter | parametri o byte | bassa | alta: architettura, layer e rank devono essere compatibili | no in generale | `K × P_adapter × b` uplink per round più broadcast; `P_LoRA=Σ r(d_in+d_out)`; numeri non disponibili | medio-basso a livello semantico, alto a livello di provenienza binaria |
| FoT / insight testuali | record JSON in linguaggio naturale | caratteri, byte, token | alta per ispezione umana | consumer-dependent nella tokenizzazione e nell’uso semantico, non nei byte | no nel setup FoT–TEP | misurato qui come somma dei blocchi UTF-8/token per receiver e chiamata | alto per contenuto, ordine, mapping e hash; nessuna garanzia di correttezza o privacy |

Il confronto è concettuale: byte testuali, logit, prototipi e parametri non sono direttamente equivalenti. Non sono prodotti numeri FedMD/FedProto/LoRA perché mancano `K`, dimensioni, precisione, compressione e numero di round comparabili.

## Limiti

- Il tokenizer standalone di GPT-5.6-terra e i file tokenizer Qwen non sono frozen nel repository. I conteggi esatti riportati sono incrementi osservati in contesto; le stime per insight/C non devono essere citate come misure esatte.
- Le latenze GPT derivano da timestamp provider a risoluzione di un secondo e non includono necessariamente l’intero tempo end-to-end; Qwen e C non espongono una latenza utilizzabile.
- Nessun prezzo o addebito applicabile è congelato: non viene calcolato costo monetario.
- Il conteggio parole dipende dalla regola dichiarata; il conteggio byte dipende dalla serializzazione JSON frozen.
- B ed E hanno stessa lunghezza, non stessi byte. La parità di token è osservata per questi due modelli e questi prompt, non una proprietà universale delle stringhe derangiate.
- C cambia insieme esempi, insight, struttura del receiver e quantità di contesto; non è un comparatore causalmente isomorfo.
- Le metriche per predizione corretta sono descrittive e sample-size-dependent; non provano privacy, compressione lossless, efficienza di banda o superiorità rispetto a FL parametrico.

## Paper-ready wording

### Methods

We characterized communication directly from the frozen FoT–TEP artifacts, without re-running any LLM. The communicated object was the exact UTF-8 peer-insight block inserted into each receiver prompt. We measured Unicode characters, UTF-8 bytes, regex-defined words, lines, and model-specific in-context token increments. Token increments were obtained by pairing B/E and A prompts for the same physical case, receiver, and repetition and subtracting the provider-recorded first-attempt input-token counts. We separately retained physical runs, three LLM repetitions, and aggregate agent-case predictions, and verified every reconstructed prompt against its frozen SHA-256 hash.

### Results

The frozen library contains 8 unique insights, two per producer; each federated receiver obtains 6 peer-only insights. One four-receiver dissemination unit contains 24 insight deliveries and 9438 UTF-8 bytes. The exact in-context increment is 2719 tokens for GPT-5.6-terra and 2974 tokens for Qwen3.8-27B-FP8. B and E have identical counts, ordering, structure, byte length, and observed token length, while differing in exactly 24 pseudolabel values across the four receiver blocks. On locally-unseen aggregate predictions, B achieved 31/36 in Experiment 1, 68/72 in EXP3_V2, and 34/36 with the Qwen consumer, compared with 0 correct under A in all three executions; these gains should be interpreted together with the semantic corruption control E.

### Limitations

These measurements characterize the realized textual payload but do not establish communication optimality, privacy, or superiority over logit-, prototype-, or parameter-sharing methods. Standalone tokenizer artifacts were not frozen, so exact token claims are restricted to paired in-context increments recorded by the providers; per-insight and centralized-context token values are explicitly estimated. Monetary cost is unavailable, Condition C is structurally non-isomorphic and post-hoc, and aggregate agent-case observations sharing a physical run are not independent physical samples.

## Riproduzione e controlli

Eseguire dalla root del repository:

```bash
python analysis/communication_characterization/characterize_payload.py
```

Il comando esegue prima i test fixture e i conteggi noti, verifica i manifest frozen correnti, ricostruisce e controlla tutti i prompt hash, legge EXP3_V2 dai tag Git e rigenera CSV, JSON e questo report. Controlli: minimal UTF-8/word/line fixture, minimal equal-length semantic-derangement fixture, current frozen inference hashes (104 files), known frozen routing: 8 unique, 6/receiver, no self, 3 deliveries/insight, 9438 B bytes/unit, explicit B/E structural and byte-level control, frozen repetition record counts 540/1080/540, paired exact token deltas constant and B/E-equal, all A/B/E prompt hashes reconstructed and verified, all Condition C prompt hashes reconstructed and verified, per-agent unseen accuracies reconcile to frozen totals. Esito: **PASS**.
