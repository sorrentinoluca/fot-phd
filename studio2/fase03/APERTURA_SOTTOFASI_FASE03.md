# Fase 03 — elenco di apertura delle sotto-fasi (proposta da confermare)

Data: **2026-09-13**. Stato: **proposta, non decisione** per tutte le righe non espressamente
confermate (`Fase_LLM.md`, «elencare non è decidere»). Redatto con modello capace e ragionamento
esteso, su repository a HEAD `b7f359f`, senza chiamate a modelli né simulazioni. Fonti lette: piano
§0.1, §6, §7, §8.4, D9; `Fase_LLM.md`; `MAINTENANCE.md` §8.6; walkthrough studio2 intestazione,
§0.1, §4.1–4.3 e tabella «Sintesi per sezione»; `PREFLIGHT_03_0.md`;
`IMPLEMENTATION_STATUS.md`; `PROVENIENZA.md` §4–§8; `PROPOSTA_OOD_D11.md`.

**Decisioni confermate dall'autore il 2026-09-13.** Il perimetro della Fase 03 è l'opzione A:
cantieri §6.1–§6.12 più §7.1 fino al GO/NO-GO. La sotto-fase 03.4 ha inoltre chiuso il blocco sul
codice Q8 senza creare un nuovo perimetro: il riuso è disciplinato a livello di funzione da
`MAINTENANCE.md` §8.2 e tutto il nuovo codice vive in `studio2/`. Queste due conferme non approvano
l'elenco nel suo insieme: profili, dipendenze e questioni indicate come aperte restano proposte.

Legenda profili (`Fase_LLM.md`): **D** decisionale · **I** implementativo · **B** esecutivo-batch ·
**A** analisi (lettura di log/risultati già su disco: modello capace, ragionamento medio).
Modello e ragionamento sono indicati per **tipo di compito**, non per prodotto.

## 0. Decisione confermata: perimetro della Fase 03

L'autore ha confermato l'opzione A: Fase 03 = cantieri §6.1–§6.12 + §7.1 fino al GO/NO-GO.
`REPORT_FASE03.md` si scrive al GO/NO-GO; §7.2–§7.5 diventano Fasi 04–07 (§5–§8 del walkthrough).
L'opzione B — un'unica Fase 03 fino a §7.5 — non è adottata. La tabella «Sintesi per sezione» del
walkthrough è stata allineata senza promuovere le restanti sotto-fasi a piano approvato.

## 1. Sotto-fasi già chiuse (ciclo §8.6 completo)

| # | Sotto-fase | Profilo | Report / verifica | Walkthrough |
| :---: | --- | :---: | --- | :---: |
| 03.1 | Criteri di selezione (§6.1), tag `studio2-fase03-criteri-selezione-frozen-001` | D | `selection/REPORT_CRITERI_6_1.md` · `VERIFICA_CRITERI_6_1.md` (OK) | §4.1 |
| 03.2 | Catalogo D1 F1/F2/F3/F8/F10/F13/F14/F15, tag `studio2-fase03-catalogo-D1-frozen-001` | D + I | `REPORT_CATALOGO_D1.md` · `VERIFICA_CATALOGO_D1.md` + appendice 01 (OK) · `PUBBLICAZIONE_CATALOGO_D1.md` | §4.2 |
| 03.3 | Run fault di sviluppo (§6.2), release `fault-dev-v1`/`v2` | I + B | `fault_runs/REPORT_RUN_FAULT.md` · `VERIFICA_RUN_FAULT.md` (OK con condizioni, chiuse in rev002) | §4.3 |
| 03.4 | Perimetro del codice Q8: opzione (a′), riuso function-level | D | `perimetro_q8/REPORT_PERIMETRO_Q8.md` · tre verbali, `VERIFICA_PERIMETRO_Q8_rev003.md` (OK) | §4.4 |

Il preflight 03.0 (`PREFLIGHT_03_0.md`, `IMPLEMENTATION_STATUS.md`) è codice e ricognizione, non
una sotto-fase chiusa: gate reale sospeso, nessun `frozen_gate_config.json`.

## 2. Blocco a monte chiuso, non presente nel piano

| # | Sotto-fase | Profilo | Modello / ragionamento | Esito |
| :---: | --- | :---: | --- | --- |
| 03.4 | **Perimetro del codice Q8** | D (breve) | proposta e revisioni con modelli capaci; tre verifiche indipendenti fino all'OK | Evidence 697-D, verbalizzatore, 8 agenti, 9 pseudolabel e derangement richiedevano una regola esplicita di riuso, chiusa da 03.4: nessuna scrittura in `phase_b/`, funzioni compatibili verificate e nuovo codice in `studio2/` |

## 3. Sotto-fasi da eseguire

Ordine del piano §6, con la dipendenza dichiarata: la colonna «pilot» dice se la sotto-fase è
un prerequisito del capability pilot (P) o ne è indipendente (—). Non è un riordino né
un'approvazione complessiva: è ciò che permette, con la data limite del 17 settembre, di decidere
cosa non può slittare.

| # | Sotto-fase (piano) | Profilo | Modello / ragionamento | Dipende da | Pilot | Congela / pubblica → ciclo §8.6 |
| :---: | --- | :---: | --- | --- | :---: | --- |
| 03.5 | **§6.3 Score e soglie Normal** secondo `DECISIONE_calibrazione_soglie_fase_B.md` rev. 19 (prevale sul piano): guardia R2 su N1–N5 come sola `baseline_fit`; 350 `cal_thr` + 150 `far_ver`; fallback 100+300+150 se R2 decade; righe U1/R2 e nuovi lotti in `PROVENIENZA.md` | I → B → A | **I**: modello capace, ragionamento medio, test eseguiti (score A, guardia, verifica impronte fase02). **B**: 500 run Simulink → **non qui**: script dell'autore da terminale o finestra economica. **A**: soglia, rango, FAR dai risultati su disco: modello capace, ragionamento medio | 03.3 (stesso generatore Philox, stream disgiunti), freeze fase02 | — | sì: soglia congelata + lotto Normal su `fot-tep-data` → report + verifica |
| 03.6 | **§6.4 Evidence 697-D e verbalizzazioni neutrali** dai 40 run di sviluppo; mapping a 9 label e assegnazione agenti come input di 03.7 | I | modello capace, ragionamento medio; estrazione pre-specificata, nessuna lettura del segnale per scegliere | 03.4, 03.3; per le soglie usa 03.5 solo se il verbalizzatore ne dipende (da dichiarare, altrimenti indipendente) | P | sì: lotto evidence/testi congelato → report + verifica |
| 03.7 | **§6.5 Nove pseudolabel opache (8 fault + Normal; `Unknown` = astensione, D10) e derangement zero-fixed-point di E** | I (combinatorio) con freeze | modello capace, ragionamento medio; basta un test che dimostri assenza di punti fissi e opacità; la sola scelta da congelare (seed, namespace) è mini-decisionale | 03.4, catalogo D1 | P | sì: freeze con seed → report breve + verifica |
| 03.8 | **§6.6 Piano statistico completo**: popolazione, endpoint §8.5, contrasti, δ e margine *m* (decisione 5), bootstrap a 9 classi + astensione, cluster, run minimi per fault, regola GO/NO-GO; qui si chiudono anche **D2** (6/8 run), **OOD** (decisione 3, da `PROPOSTA_OOD_D11.md`) e **D11**, e si registra la politica R=3 (decisione 11) | D | **il modello più capace, ragionamento esteso**: si congela prima di ogni run di test | 03.2; letteratura §12; nessun risultato per-fault | — (ma la decisione 11 va pre-specificata prima del pilot: già coperta per il pilot preliminare dal PREFLIGHT) | sì: piano statistico congelato → report + verifica |
| 03.9 | **§6.7 Baseline numerica**: prototipi medi 697-D per classe dai dati di sviluppo, regola L1 congelata | I | modello capace, ragionamento medio, test eseguiti | 03.4, 03.6 | — | sì: freeze della regola → report + verifica |
| 03.10 | **§6.8 Harness API**: 8 agenti, 14 insight, 9 pseudolabel con astensione, logging §8.7, set canary; già in gran parte in `studio2/fase03/` (`protocol.py`, `run_pilot.py`, `prepare_gate.py`, 16 test offline) — resta da collegare agli input reali e alla regola 03.4 | I (+ B minimo) | modello capace, ragionamento medio, test offline eseguiti; le poche chiamate di prova su Qwen-27B surrogato vanno contate e autorizzate a parte | 03.4, 03.6, 03.7, 03.12 | P | report di sotto-fase; verifica sul gate 40×3 (03.13) |
| 03.11 | **§6.9 Run finali di test**: 54 (6/fault) o 72 (8/fault) + 6 OOD; seed diversi e dimostrabili dai run di sviluppo; ispezione solo tecnica e loggata | B (spec I breve) | **spec e piano**: modello capace, ragionamento medio, in questa finestra. **Esecuzione**: **non qui**, script dell'autore (MATLAB/Simulink) come per 03.3 | 03.8 (D2 e OOD fissati), 03.3 (generatore e MEX già qualificati) | — | sì: lotto sigillato + tag `studio2-fase03-test-v1` → report + verifica; **nessuna decisione di disegno dopo la generazione** |
| 03.12 | **§6.10 Schema degli insight (D12, §8.9)**: campi, cardinalità, cap per elemento, validatore; già implementato in `schemas/` ma **non congelato** | D (breve) + I | decisione: modello capace, ragionamento esteso (vincola entrambi i producer); congelamento: meccanico | 03.2 | P | sì: freeze schema + tag → report + verifica; **precede qualunque insight** (03.13 conformità e 7.2) |
| 03.13 | **§7.1 Capability pilot su Qwen-27B locale** (2.4T solo se disponibile, come 03.13b) — catena: manifest scientifico autonomo + selezione deterministica dei 40 prompt (I) → verifiche pre-sonda, capienza offline col tokenizer locale (I) → sonda budget 3–9 chiamate, freeze `frozen_gate_config.json` (B) → gate 40×3, 120 chiamate (B) → capacità, latenza, divergenze dai log (A) → conformità producer Qwen 8 chiamate + producer alternativo 8 chiamate, **solo dopo che D9 lo ha configurato** (B) → GO/NO-GO (D) | I → B → A → D | **I**: capace, medio. **B**: **non qui**: finestra economica o `run_pilot.py` dall'autore (3–5 h a 2048, fino a 6–9 h a 4096, sequenziale su 8001@16384). **A**: capace, medio. **GO/NO-GO**: il più capace, esteso | 03.6, 03.7, 03.10, 03.12; endpoint e fingerprint congelati | P | sì: `REPORT_PILOT`/`VERIFICA_PILOT` + report di fase |
| 03.14 | **§6.11 Baseline FedAvg** + pavimento locale e soffitto centralizzato (§9.3), specifica congelata prima di guardare il test | I (spec D breve) | specifica §9.2: capace, esteso; implementazione e run: capace, medio, test eseguiti; l'addestramento è CPU/GPU locale, non chiamate | 03.6 (evidence), 03.11 solo per l'esecuzione finale | — | sì: specifica congelata → report + verifica |
| 03.15 | **§6.12 Sezioni del paper indipendenti dal modello**: related work, metodo, verbalizzatore, threats to validity (≈60% del testo, comuni a Q8 e Terra-only) | D (redazione) | modello capace, ragionamento esteso; `letteratura.md` come unica fonte bibliografica | 03.2, 03.3, 03.12; `letteratura.md` | — | report di sotto-fase; verifica documentale |

Due ambiguità che l'elenco non risolve e che spettano all'autore:

1. **Quale pilot è 03.13.** Indicazione dell'autore (2026-09-13): il modello disponibile e usato
   finora è **Qwen-27B FP8 locale** (8001@16384); Qwen-2.4T non è disponibile. 03.13 è quindi il
   pilot sul 27B con la catena sopra (145 chiamate, €0). Per D9 ciò corrisponde al «pilot breve»
   dell'opzione 2 se il 2.4T non arriva entro il 17; se arrivasse, la stessa catena andrebbe ripetuta
   su di esso come 03.13b, con endpoint e fingerprint propri. Il GO/NO-GO vale solo per la
   combinazione effettivamente verificata (PREFLIGHT, «Perimetro dell'eventuale GO»).
2. **Producer alternativo.** È Terra **solo** nell'opzione 2 di D9 (§8.4); nell'opzione 1 non è
   configurato (modello, endpoint, tariffa ignoti — PREFLIGHT). Le 8 chiamate di conformità sul
   secondo producer restano differite finché D9 non lo nomina.

## 4. Solo per l'opzione B non adottata (Fasi 04–07 nell'opzione A)

| # | Fase / sotto-fase | Profilo | Modello / ragionamento |
| :---: | --- | :---: | --- |
| 7.2 | Produzione insight: libreria 8×2 dal producer principale e libreria completa dal producer alternativo (§8.4), entrambe validate contro lo schema 03.12 | B con gate D | batch **non qui**; accettazione della libreria: capace, esteso |
| 7.3 | Congelamento del protocollo finale | D | il più capace, esteso |
| 7.4 | Studio finale: A, B-LF, E-LF, swap, OOD, ablation, canary (~2.450–3.555 chiamate) | B | **non qui**; finestra economica o script dell'autore; canary/audit: capace, medio |
| 7.5 | Analisi e redazione | A + D | analisi: capace, medio, script riproducibili; redazione: capace, esteso |

## 5. Cammino critico verso il 17 settembre

Prerequisiti del pilot, in ordine vincolato: **03.4 → 03.12 → 03.7 → 03.6 → 03.10 → 03.13**.
Tutto il resto (03.5, 03.8, 03.9, 03.11, 03.14, 03.15) è indipendente dal pilot e può scorrere in
parallelo o dopo; 03.8 deve comunque precedere 03.11. Ogni sotto-fase segue il ciclo
`Fase_LLM → Verifica_LLM (altra finestra, altro modello) → Documentazione_LLM → Commit_LLM`;
`REPORT_FASE03.md` e `VERIFICA_FASE03.md` si scrivono solo alla chiusura del perimetro confermato.
