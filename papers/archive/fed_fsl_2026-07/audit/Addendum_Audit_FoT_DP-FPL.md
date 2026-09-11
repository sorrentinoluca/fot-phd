# Addendum all'audit dei prior art Fed-FSL — Federation over Text (P067) e DP-FPL (P066)

**Data:** 28 luglio 2026
**Documento di riferimento:** `Audit_Nuovi_Prior_Art_Fed_FSL.md` (di seguito **Audit-1**)
**Oggetto:** i due lavori che Audit-1 aveva classificato come *«Paper non disponibile nella cartella: verifica non eseguibile sul testo integrale»* sono ora disponibili come `P066.md` e `P067.md`. Questo addendum applica le **stesse definizioni operative, le stesse colonne e le stesse regole di evidenza** di Audit-1 (§4.1 strict K totale, §4.2 aggiornamento parametrico, §4.3 contesto personalizzato, §4.4 federazione reale, §4.5 metrica rilevante del prompt di audit).

Nessuna sezione di Audit-1 è riscritta. La V3 non è aggiornata. Nessun esperimento è progettato.

---

## A.0 Identificazione e status

| ID | Titolo verificato | Autori | Anno | Venue/status dichiarato **nel file** | Status verificato su fonte ufficiale | File |
|---|---|---|---:|---|---|---|
| **P066** | Privacy-Preserving Personalized Federated Prompt Learning for Multimodal Large Language Models — metodo **DP-FPL** | Linh Tran¹, Wei Sun², Stacy Patterson¹, Ana Milanova¹ (¹Rensselaer Polytechnic Institute, ²IBM Research) | 2025 | «Published as a conference paper at ICLR 2025» (ricorrente su ogni pagina) | **Pubblicato — ICLR 2025** | `P066.md` |
| **P067** | Federation over Text: Insight Sharing for Multi-Agent Reasoning — **FoT** | Dixi Yao†, Tahseen Rabbani†, Manzil Zaheer‡, Tian Li† (†University of Chicago, ‡Google DeepMind) | 2026 | «**A PREPRINT**» (ricorrente su ogni pagina) | **Preprint arXiv:2604.16778**, v1 18 apr. 2026, v2 23 mag. 2026, *Comments* «46 pages»; nessun riferimento a venue | `P067.md` |

**Correzione ad Audit-1 §0.2 e §0.4.** Le due righe «Paper non disponibile nella cartella» decadono. Restano valide le correzioni bibliografiche già formulate:
- il titolo di **DP-FPL** non è «DP-FPL»: quello è il nome del metodo. Il titolo è quello riportato sopra ed è ora confermato dal testo integrale;
- **FoT non è un workshop paper**: il file stesso si dichiara «A PREPRINT». La dicitura della V3 «preprint/workshop 2026» resta `Formulazione troppo forte`.

---

## A.1 Audit paper per paper (stesse colonne di Audit-1 §1)

| ID e paper | Status verificato | Federazione reale | Strict K totale | Dati aggiuntivi o sintetici | Local-only equivalente | Payload client-server | Aggiornamenti parametrici | Sintesi multi-client | Personalizzazione per client | Persistenza | Metrica task-specifica | Evidenza |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **P067 — Federation over Text (FoT)** | Preprint arXiv 2604.16778 | **No — «federated-learning-like» per autodichiarazione** | **No** | **Sì (confondente)**: nel setting principale gli agenti «iteratively solve the **exact same** benchmark dataset in each round» | **Sì** — *Isolated Agents* è la baseline primaria, più RAG, Skills (52), ExpeL | **Traces testuali** (metacognitive summaries), puramente discreti | **No** | **Sì** — clustering + merge + distillazione via prompt curati | **No** — libreria globale identica in broadcast; la personalizzazione è **dichiarata come future work** | **Sì** — libreria evolutiva fra round, riusabile da agenti futuri | **Sì** — pass@1/accuracy, guidance rate, token, loop, TTS, tempo, costo USD | Abstract; §1; §2; §3 e §3.1 Tab. 1; App. B Alg. 2; App. C; App. D.1 Tab. 8; §4.3 Tab. 2; §6.1–6.5; App. D.3.2 Tab. 11–12; App. E.2 Tab. 19; App. F.4 Tab. 26–28 |
| **P066 — DP-FPL** | Pubblicato — ICLR 2025 | **Sì** | **No** | **No** | **No** — le baseline (PromptFL, FedOTP, FedPGP) sono **tutte federate**; nessun riferimento locale o zero-shot | **Gradienti** del prompt globale `∇_{G,i}L` (vettori continui, clippati e rumorosi); ritorno del prompt globale aggregato | **Sì** — soft prompt (`b=16 × d=512`), SGD, fattorizzazione low-rank via power method **a ogni round**, residuo `r_i` | **No** — media aritmetica dei gradienti + rumore gaussiano | **Sì** — `p_{L,i}` mai condiviso, persistente fra round | **Sì** | **Sì** (accuracy) ma **mediata su tutti i client**; nessuna metrica per-client | §3.1–3.4 Alg. 1; §3.5 Teor. 3.3; §4.1 Tab. 2–3; §4.2 Tab. 4; §4.3 Fig. 2; App. A.1–A.2 Tab. 5; App. A.3 Fig. 3; App. A.4 Tab. 6–9 |

---

## A.2 Verifica puntuale dei dodici aspetti richiesti

### A.2.1 P067 — Federation over Text

**1. Federazione reale oppure federated-learning-like → `federated-learning-like` (autodichiarato).**

Il paper non rivendica di essere Federated Learning e lo dichiara tre volte:
> «We propose **a federated learning-like framework**, *Federation over Text* (FoT)» (Abstract)
> «we propose *federation over text* (FoT), **a federated-like framework**» (§1)
> «the **first federated-like** multi-agent reasoning framework» (§7)

§3.1 e Tab. 1 costruiscono esplicitamente un mapping **analogico** fra FL e FoT (obiettivo, lavoro locale, minimizzazione dei dati, upload, aggregazione, download, personalizzazione), non un'identità.

Applicando la definizione §4.4 di Audit-1, FoT **non** soddisfa il criterio di federazione reale:
- non esistono organizzazioni con data silo privati: ogni «client» è un agente LLM a cui viene **assegnato** un benchmark o un task (8 agenti su 8 dataset matematici; 1 574 agenti su un paper ICLR ciascuno; 23 agenti su 23 task PinchBench);
- non esiste alcun vincolo istituzionale, regolatorio o di privacy che motivi la decentralizzazione: la protezione dei problem instance è una **proprietà emergente misurata a posteriori** (§5, App. E.2), non un requisito del setting;
- l'obiettivo non è servire client eterogenei ma «learn an insight library that improves the reasoning of agents» (Tab. 1).

È quindi la stessa categoria di **P014 — FORGE** e **P013 — FoA** di Audit-1 §3.8: sistema multi-agente con broadcast globale, non FL. Con una differenza rilevante: FoT è di gran lunga il più rigoroso dei tre nell'esplicitare l'analogia e i suoi limiti.

**2. Quantità effettiva di dati per client → molto piccola, ma non è un support set.**

Dalla Tab. 19 (App. E.2), con il numero di agenti dichiarato nelle rispettive sezioni:

| Applicazione | # problemi totali | # agenti | Problemi per agente |
|---|---:|---:|---:|
| Math (LiveMathBench, §4.1) | 300 | 8 | ~37 |
| Science+Math+Coding (§4.2) | 881 | 5 dataset | ~176 |
| HLE+Science+Math (§4.2) | 2 798 | — | — |
| Insight discovery, ICLR 2023 (§4.4) | 1 574 | **1 574** | **1** |
| Insight discovery, ICLR 2024 (§4.4) | 2 260 | 2 260 o 91 | **1** o 25 |
| PinchBench (§4.3) | 23 | **23** | **1** |

Il volume locale è quindi minimo — in tre applicazioni **un solo item per agente**. Questo è il dato più vicino a un regime di scarsità estrema fra tutti i lavori a payload testuale del corpus.

**3. Strict K-shot totale → `No`, e per una ragione categoriale, non quantitativa.**

Applicando la definizione §4.1, FoT **non** è strict K-shot perché **non esiste alcun support set etichettato**. I «dati locali» sono i **problemi da risolvere**, non dimostrazioni:
> «even **labels indicating whether an answer is correct are not required**» (§2)

Non c'è quindi né `S_i` né la distinzione `S_i ⊥ Q_i` su cui l'estimando `Δ_i` della proposta è definito. Registrazione separata come richiesto dal protocollo:
- esempi originali locali (supervisionati): **0**;
- esempi sintetici: **0**;
- validation set: **assente**;
- dati pubblici o ausiliari: **assenti** (i benchmark sono i task stessi);
- dimostrazioni inserite nel prompt: **nessuna** — nel prompt entra la *insight library*, che contiene principi astratti, non esempi (Jaccard 4-gram fra libreria e coppie problema-risposta = **0.000**, Tab. 19).

**4. Payload scambiato → testo discreto, verificato quantitativamente.**

Reasoning traces in linguaggio naturale, generate localmente per riflessione sul proprio processo di soluzione, mai le istanze grezze. Dimensioni dichiarate (§4.1, Tab. 19): DeepSeek 249 traces = 33K token → 11 insight = 3K token; Gemini 3.0 Pro 549 traces = 53K token → 37 insight = 12K token.

Il paper misura anche la separazione fra payload e dati grezzi (App. E.2): attacco di prompt-stealing multi-turn con F1 token-level `< 0.25`, nessuna PII ricostruita, Jaccard 4-gram trace↔problemi `0.000` in sei applicazioni su sette (`0.006` su PinchBench). **Nessuna garanzia formale di privacy**, coerentemente con la regola di rigore «non trattare privacy-by-locality come garanzia formale».

**5. Aggiornamenti parametrici → `No`.**

> «FoT operates at the **semantic** level **without any gradient optimization or supervision signal**» (Abstract)
> «without any **parameter optimization, fine-tuning, or reinforcement learning**» (§1)

Nessuna delle esclusioni §4.2 è violata: niente LoRA, adapter, soft prompt, embedding addestrati, generatori di prompt, router o gating. L'aggregazione server-side è realizzata **con prompt curati** (App. G), non con ottimizzazione numerica.

**6. Sintesi multi-client → `Sì`, e dimostrata necessaria.**

Il server «first **clusters** reasoning traces that share similar skills, and then **uncovers connections** among traces that solve the same problem using different skills and can potentially be **merged**» (§3). L'ablazione §6.2 mostra che la sintesi non è cosmetica: la **semplice concatenazione delle traces è la strategia peggiore** («simply concatenating all traces results in the worst accuracy»), e resta peggiore anche campionando il 75% o il 50% delle traces. Chain-of-Density e Context Compaction sono migliori della concatenazione ma inferiori ai prompt di aggregazione proposti.

Questo è il risultato più forte del corpus a sostegno dell'ipotesi «la sintesi aggiunge valore rispetto all'accumulo». È anche, per la stessa ragione, un risultato che **rende non nuova** l'affermazione generica «la sintesi batte la concatenazione».

**7. Persistenza → `Sì`, con transfer verificato.**

La libreria evolve fra round e sopravvive al processo: è riusabile da «existing and future agents» (§3), trasferibile a modelli diversi (Tab. 4: libreria costruita da DeepSeek che migliora Gemini 3.0 Pro, «weak-to-strong generalization … in the text space»), e a task mai visti (Tab. 5, Tab. 16–17; libreria da PinchBench che migliora 199 agenti su Claw-Eval, App. E.1 Tab. 14).

**8. Personalizzazione per client → `No`, e dichiarata esplicitamente come lavoro futuro.**

La libreria è **una sola**, in broadcast identico: «Broadcast the new library to agents» (App. B, Alg. 2, riga 10). La riga «Personalization» della Tab. 1 non descrive un meccanismo, ma un fatto del setting: «Addressing diverse local tasks across different domains».

La dichiarazione decisiva è in §3.1:
> «It is worth continuing to explore the design space of FoT, such as **personalization strategies** and handling other forms of distribution drifts across agents, **which we leave for future work**.»

Applicando la definizione §4.3: FoT ricade nella categoria «contesto globale identico per tutti». Non c'è né retrieval per query (la libreria intera entra nel prompt), né personalizzazione persistente per client, né sintesi client-conditioned.

**9. Baseline local-only → `Sì`, ed è la baseline primaria.**

*Isolated Agents* — ogni agente risolve il proprio task da solo, senza libreria — compare in **ogni** tabella e figura del paper (Fig. 2–4, Tab. 2, 3, 5, 6, 8, 9, 11, 12, 14–17, 20–27). Sono presenti anche tre baseline «locali potenziate»: RAG sulle trajectory grezze, 52 skill OpenClaw predefinite, ed ExpeL (Tab. 11–12).

Questo è il trattamento del local-only più completo dell'intero corpus esaminato, superiore a SYNAPSE (che riporta un solo numero: 0.46).

**10. Metriche task-specifiche e per-client → `Sì` per entrambe.**

Metriche oggettive: pass@1/accuracy (math, GPQA, coding, HLE), score PinchBench, guidance rate (insight discovery), più efficienza (token generati, loop di ripetizione, tool call, tempo wall-clock, costo USD) e true-thinking score.

**Reporting per-client: presente.** La Tab. 8 (App. D.1) riporta accuracy **per singolo agente** (AIME24, AIME25, AMC, CCEE, CNMO, WLPMC, V202412 Hard, V202505 Hard) sia per *Isolated Agent* sia per *FoT*. Le Tab. 26–27 (App. F.4) estendono il reporting a matrici 8×8 agente-contributore × agente-valutato. La Tab. 7 riporta `∆Isolated Agents` e `∆FoT` **per riga di agente**.

**Questo è il primo e unico caso, nell'intero corpus esaminato in Audit-1 e in questo addendum, in cui `Δ_i` per-client rispetto a un local-only è effettivamente calcolabile su un sistema a payload testuale senza aggiornamenti parametrici.**

**11. Harmed-client rate → `No` come metrica, ma i dati riportati lo rendono calcolabile — e non è nullo.**

Il paper non definisce, non nomina e non conta clienti danneggiati. Le Tab. 26–27 evidenziano in grassetto **soltanto i miglioramenti**.

Incrociando la baseline *Isolated Agent* di Tab. 8 (Gemini 3.0 Pro: AIME24 0.967, AIME25 0.933, AMC 0.935, CCEE 0.864, CNMO 0.889, WLPMC 0.727, V202412 Hard 0.762, V202505 Hard 0.690) con le Tab. 26–27, si ricavano casi di **peggioramento per-agente**:

| Tabella | Configurazione | Agente danneggiato | Isolated | FoT | Δ |
|---|---|---|---:|---:|---:|
| Tab. 27 (*Exclude One*) | esclude AIME24 | AMC | 0.935 | 0.913 | **−0.022** |
| Tab. 27 (*Exclude One*) | esclude CNMO | AMC | 0.935 | 0.913 | **−0.022** |
| Tab. 27 (*Exclude One*) | esclude V202505 Hard | AMC | 0.935 | 0.913 | **−0.022** |
| Tab. 26 (*Include One*) | solo AMC contribuisce | V202505 Hard | 0.690 | 0.680 | **−0.010** |
| Tab. 27 (*Exclude One*) | esclude CCEE | V202505 Hard | 0.690 | 0.680 | **−0.010** |
| Tab. 27 (*Exclude One*) | esclude WLPMC | V202505 Hard | 0.690 | 0.680 | **−0.010** |

*(Inferenza dell'auditor per differenza fra tabelle riportate dal paper, non affermazione degli autori.)*

Osservazione: nel risultato principale a **partecipazione piena** (Tab. 8) **nessun agente è danneggiato** — 7 migliorati e 1 invariato su 8 con Gemini 3.0 Pro; 2 migliorati e 6 invariati con DeepSeek. Il danno compare **solo** nei regimi di partecipazione parziale (*Include One* / *Exclude One*), cioè proprio nel regime in cui i contributi disponibili sono pochi ed eterogenei — che è il regime della proposta.

Questo è simultaneamente il risultato più utile e più scomodo del paper per la proposta: mostra che il trasferimento negativo esiste in un sistema federato-testuale a libreria globale, e che gli autori del lavoro più vicino **non lo hanno né misurato né trattato**.

**12. Sovrapposizione con il claim residuo → parziale ma sostanziale; il claim residuo sopravvive.**

Il claim residuo formulato in Audit-1 §6 è:

> Costruzione, sotto strict K totale per client e senza alcun aggiornamento parametrico, di un contesto testuale discreto `G_i` **diverso per ciascun client**, sintetizzato da contributi testuali di più client, valutata sull'utilità **per-client** rispetto al Local K-shot e al retrieval globale **a parità di token, chiamate e capacità dei modelli**, con la **percentuale di client danneggiati** come endpoint co-primario.

Scomposizione rispetto a FoT:

| Componente del claim residuo | Coperta da FoT? | Evidenza |
|---|---|---|
| Payload testuale discreto | **Sì** | §1, Tab. 19 |
| Nessun aggiornamento parametrico | **Sì** | Abstract, §1 |
| Sintesi (non concatenazione) di contributi di più client | **Sì**, e dimostrata necessaria | §3, §6.2 |
| Contesto persistente | **Sì**, con transfer cross-modello e cross-task | §5, Tab. 4–5, 14 |
| Confronto contro local-only | **Sì**, come baseline primaria | ovunque |
| Confronto contro retrieval globale | **Sì** — baseline RAG in §4.3, §4.4 e Tab. 11 | Tab. 3, Tab. 11, Fig. 7 |
| Reporting per-client | **Sì** | Tab. 7, 8, 26, 27 |
| **Contesto diverso per ogni client (`G_i`)** | **No — dichiarato future work** | §3.1 |
| **Strict K-shot totale supervisionato** | **No — nessun support set etichettato** | §2 |
| **Data silo federati** | **No — federated-learning-like** | Abstract, §1, §7 |
| **Harmed-client rate come metrica** | **No** — dati presenti, metrica assente | Tab. 26–27 |
| **Parità di token e chiamate fra condizioni** | **Parziale** — contabilità end-to-end esplicita (Tab. 10 separa «FoT (all)» da «FoT (inference)»; Tab. 12 riporta 0.67 vs 0.35 USD contro Isolated Agents), ma **nessuna equalizzazione** | App. D.3.1 Tab. 10; Tab. 12 |

**Sette elementi su dodici coperti** — più di qualunque altro paper del corpus, incluso SYNAPSE (sei).

---

### A.2.2 P066 — DP-FPL

**1. Federazione reale → `Sì`.**

Setting FPL standard: `N` client con dataset locale privato `D_i` di `n_i` campioni, server centrale, CLIP congelato lato client (§3.1). Split pathological (classi disgiunte fra client) su Caltech101/OxfordPets/OxfordFlowers/Food101 con `N = 10`; split Dirichlet `α = 0.3` su CIFAR-100 con `N = 25` e `N = 50` (App. A.2, Tab. 5). Modello di minaccia esplicito: client e server onesti, avversario = utente pubblico che riceve il prompt addestrato (§3.3).

**2. Quantità effettiva di dati per client → dataset pieni, nessun regime few-shot.**

Derivata dalle dimensioni dichiarate in App. A.1 divise per il numero di client di Tab. 5:

| Dataset | Train totale | Client | Train per client (media) |
|---|---:|---:|---:|
| Caltech101 | 4 128 | 10 | ~413 |
| Oxford Pets | 2 944 | 10 | ~294 |
| Oxford Flowers | 4 093 | 10 | ~409 |
| Food101 | 50 500 | 10 | ~5 050 |
| CIFAR-100 | 50 000 | 25 / 50 | ~2 000 / ~1 000 |

Il paper **non menziona mai** un setting few-shot o k-shot, né una curva sul numero di shot. Batch 32, `T = 100` round (200 su CIFAR-100).

**3. Strict K-shot totale → `No`.**

Nessun criterio della definizione §4.1 è soddisfatto: i client dispongono dell'intero split delle proprie classi. Registrazione separata: esempi originali locali = centinaia-migliaia; esempi sintetici = 0 (salvo i **50 shadow model** dell'esperimento MIA, App. A.3, che non entrano nel training del metodo); validation set = non riportato; dati pubblici = il CLIP pre-addestrato (congelato) e la sua conoscenza.

**4. Payload scambiato → gradienti continui.**

Ogni client invia al server `∇_{G,i}L`, il gradiente rispetto al prompt globale (Alg. 1, riga 13). Il server media, aggiunge rumore gaussiano `N(0, σ_G²)` e aggiorna `p_G` (righe 15–17). Il prompt locale `p_{L,i}` **non lascia mai il client**. Nessun testo, nessun artefatto discreto: il prompt è un tensore continuo `16 × 512` (App. A.2).

**5. Aggiornamenti parametrici → `Sì`, su tutti i criteri §4.2.**

Soft prompt continui ottimizzati con SGD (`η_G = η_L = 0.0001`), backbone CLIP congelato — che, per la regola di rigore di Audit-1, **non** rende il metodo weight-free. In aggiunta: fattorizzazione low-rank `p_{L,i} = u_i v_i + r_i` ricalcolata **a ogni round** via power method (Alg. 1, riga 6), ricostruzione del gradiente full-rank (Eq. 4), rank ∈ {1, 2, 4, 8}, `T = 100`–`200` round.

**6. Sintesi multi-client → `No`.**

L'aggregazione è una media aritmetica dei gradienti seguita da rumore gaussiano (Alg. 1, righe 15–16). Nessun clustering, nessuna risoluzione di conflitti, nessun contenuto semantico.

**7. Persistenza → `Sì`.**

`p_{L,i}` persiste fra round (`p^t_{L,i} ← p^{t−1}_{L,i}`, riga 4) e non viene mai sovrascritto dall'aggregazione. Il residuo `r_i` è ricalcolato ogni round.

**8. Personalizzazione per client → `Sì`, parametrica e persistente.**

Ogni client mantiene `p_i = p_{G,i} + u_i v_i + r_i`, con la componente locale mai condivisa. È lo stesso principio già coperto da pFedPG, pFedMoAP e DP²FL in Audit-1 §3.6. L'unica novità metodologica rispetto a FedPGP è che la fattorizzazione è ripetuta ogni round e che il **residuo** `r_i` recupera l'espressività persa — il paper dimostra che il residuo è ciò che salva la personalizzazione sotto rumore DP forte (Fig. 2, Tab. 6–9).

Applicando la definizione §4.3: personalizzazione **parametrica** persistente, non sintesi testuale client-conditioned.

**9. Baseline local-only → `No`.**

Le tre baseline sono PromptFL, FedOTP e FedPGP (§4.1, App. A.2), **tutte federate**. Non esiste alcun riferimento a un client isolato, né a CLIP zero-shot, né a CoOp addestrato localmente. È, su questo asse, **più debole di pFedMoAP** (che ha ZS-CLIP e CoOp locale) e di DP²FL (che ha «Local»).

Nota di rigore: per la regola «non dedurre una baseline che non sia esplicitamente riportata», la colonna resta `No`.

**10. Metriche task-specifiche e per-client → task-specifica `Sì`, per-client `No`.**

Metrica oggettiva: accuracy di classificazione, riportata su due test set distinti per ciascun client — *local classes* (personalizzazione) e *neighbor classes*, cioè le classi possedute dagli altri client (generalizzazione). È una scomposizione interessante e pertinente, ma:

> «The final test accuracy is obtained by **averaging the performance across all clients**» (§4.1)
> «The test accuracy is **averaged across all clients**» (App. A.2)

Ogni numero di ogni tabella (Tab. 2, 3, 4, 6, 7, 8, 9) è una media su 10, 25 o 50 client, su 5 seed. **Nessuna distribuzione, nessun quantile, nessun valore per singolo client.** Le deviazioni standard riportate sono sui seed, non sui client.

**11. Harmed-client rate → `No`.**

Assente, e non ricavabile: il livello di aggregazione dei risultati non lo consente.

**12. Sovrapposizione con il claim residuo → bassa.**

| Componente del claim residuo | Coperta da DP-FPL? |
|---|---|
| Data silo federati | **Sì** |
| Contesto diverso per ogni client | **Sì**, ma **parametrico** (soft prompt) |
| Contesto persistente | **Sì**, parametrico |
| Payload testuale discreto | **No** |
| Nessun aggiornamento parametrico | **No** |
| Sintesi multi-client | **No** |
| Strict K-shot totale | **No** |
| Confronto contro local-only | **No** |
| Confronto contro retrieval globale | **No** (non applicabile) |
| Reporting per-client | **No** |
| Harmed-client rate | **No** |
| Parità di token e chiamate | **No** (non applicabile) |

**Tre elementi su dodici**, tutti già coperti da pFedPG, pFedMoAP, DP²FL e pFedFSL in Audit-1.

---

## A.3 Effetto sulle classificazioni di Audit-1

### A.3.1 Correzioni alla tabella del gap residuo (Audit-1 §4)

Due righe cambiano stato in forza del solo P067.

| Elemento candidato | Stato in Audit-1 | Stato aggiornato | Motivo |
|---|---|---|---|
| **Reporting per-client** | *Parzialmente coperto* — «assente in tutti i sistemi a payload testuale» | **Parzialmente coperto**, ma la clausola cade: **P067 riporta `Δ_i` per agente contro un local-only** (Tab. 7, 8, 26, 27) | La frase «assente in tutti i sistemi a payload testuale» di Audit-1 era vera sul corpus allora disponibile; ora è **contraddetta** da P067 |
| **Harmed-client rate / negative transfer** | *Parzialmente coperto* — meccanismi in DP²FL/pFedFSL, osservazione in pFedMoAP | **Parzialmente coperto**, con aggiunta: **P067 produce dati da cui il danno per-agente è calcolabile** (6 casi identificati) **senza mai misurarlo** | Il fenomeno è ora documentato anche in regime federato-testuale non parametrico, che era il punto scoperto |

Le altre dieci righe restano invariate. In particolare:
- **Contesto diverso per ogni client** resta `Non identificato in forma testuale discreta`: P067 conferma la classificazione e la **rafforza**, perché gli autori dichiarano la personalizzazione come lavoro futuro (§3.1);
- **Strict K-shot totale per client** resta `Parzialmente coperto` con P023 come unico caso vicino: P067 non lo tocca perché non ha support set;
- **Parità di token e chiamate** resta `Non identificato` come *controllo sperimentale*, benché P067 sia il lavoro più rigoroso del corpus nella **contabilità** dei costi.

### A.3.2 Correzioni all'elenco dei lavori più vicini (Audit-1 §6)

| Voce | Audit-1 | Aggiornata |
|---|---|---|
| Paper complessivamente più vicino | P065 — SYNAPSE (6/12) | **P067 — FoT (7/12)**, con P065 — SYNAPSE secondo (6/12) |
| Paper più vicino sull'asse federato testuale | P065 — SYNAPSE, poi P009 — FedDTPT | **P067 — FoT**, poi P065 — SYNAPSE, poi P009 — FedDTPT |
| Paper più vicino sull'asse personalizzazione | P023 — pFedFSL | **Invariato.** P066 — DP-FPL si colloca accanto a pFedPG/pFedMoAP/DP²FL, ma **sotto** pFedFSL perché privo di local-only, di reporting per-client e di regime di scarsità |

Va però registrata una differenza qualitativa: **SYNAPSE resta più vicino di FoT sull'asse *federazione***. SYNAPSE ha data silo, gerarchia client–edge–server, garanzia (ε,0)-DP formale sui campi numerici e conflict resolution; FoT è dichiaratamente *federated-learning-like*. FoT è più vicino sull'asse **misurazione** (per-client, local-only, costi) e sull'asse **sintesi testuale pura**.

### A.3.3 Aggiunta all'elenco «claim da abbandonare» (Audit-1 §6)

Ai claim 1–8 già elencati si aggiungono due voci, entrambe per effetto di P067:

9. **«Reporting per-client in un sistema federato testuale senza parametri» come contributo** — realizzato da FoT nelle Tab. 7, 8, 26, 27.
10. **«La sintesi batte la concatenazione» come risultato** — dimostrato da FoT §6.2, dove la concatenazione è la strategia peggiore anche variando la frazione di traces incluse.

Resta difendibile la sola **operazionalizzazione dichiarata** del danno come endpoint co-primario pre-registrato, che nessuno dei due paper compie.

---

## A.4 Effetto sul verdetto

### Il verdetto `GO ALLA VALIDAZIONE` **non cambia.**

**P066 — DP-FPL: nessun impatto.** Conferma integralmente la caratterizzazione della famiglia parametrica già data in Audit-1 §3.6 e non tocca alcun elemento del claim residuo che non fosse già coperto. Su due assi è anzi **più debole** dei paper già esaminati: nessuna baseline local-only e nessun reporting per-client. Il suo unico contributo all'audit è confermare che la V3 descriveva correttamente il meccanismo (fattorizzazione low-rank + residuo personalizzato) pur non avendo letto il paper, e che lo status ICLR 2025 è corretto.

**P067 — FoT: impatto reale, ma non ribaltante.**

Ciò che FoT **chiude**:
- il payload testuale discreto puro, con misura quantitativa della separazione dai dati grezzi;
- la sintesi multi-client dimostrata superiore alla concatenazione;
- la persistenza con transfer cross-modello e cross-task verificato;
- il confronto sistematico contro local-only, RAG globale, skill predefinite ed ExpeL;
- il reporting per-agente di `Δ_i` contro il local-only — l'elemento che Audit-1 dava per assente in tutti i sistemi testuali.

Ciò che FoT **lascia aperto**, e che costituisce il claim residuo aggiornato:
- **non è Federated Learning**: nessun data silo, nessun vincolo di privacy, agenti assegnati a benchmark. La proposta opera in un setting diverso e più vincolato;
- **nessun contesto per client**: la libreria è una sola, e la personalizzazione è **esplicitamente rinviata** dagli autori a lavoro futuro (§3.1);
- **nessun regime K-shot supervisionato**: non esistono `S_i` etichettati né la separazione `S_i ⊥ Q_i` su cui `Δ_i` è definito. FoT non risponde alla domanda scientifica della proposta, perché non c'è un client che «impara dai propri K esempi»;
- **harmed-client rate mai misurato**, benché i dati mostrino danno per-agente in almeno sei configurazioni di partecipazione parziale;
- **nessuna equalizzazione di budget**: FoT costa più del doppio degli Isolated Agents in Tab. 12 (0.67 vs 0.35 USD) pur generando meno token, e il paper lo dichiara onestamente senza equalizzarlo;
- **confondente nel setting principale**: gli agenti «iteratively solve the exact same benchmark dataset in each round» (App. D.1), quindi la libreria è costruita sugli stessi problemi su cui si valuta. Il paper mitiga il problema solo nelle Tab. 5, 16, 17 e nelle ablazioni *Include/Exclude One*.

**Il claim residuo sopravvive, ancora più stretto.** Formulato ora:

> Costruzione, in un vero setting federato con data silo e sotto strict K totale **supervisionato** per client, di un contesto testuale discreto `G_i` **diverso per ciascun client** e sintetizzato da contributi di più client, senza aggiornamenti parametrici, valutata come `Δ_i` per-client contro Local K-shot e contro la **libreria/compendio globale** — non solo contro l'agente isolato — **a parità dichiarata di token e chiamate**, con la percentuale di client danneggiati come endpoint co-primario **pre-registrato**.

Le due parole che portano il peso sono ora **«diverso per ciascun client»** e **«pre-registrato»**. Tutto il resto è coperto.

### Motivazione del mancato cambio di verdetto

Non è `STOP` perché nessuno dei due paper costruisce un contesto client-specifico: DP-FPL lo fa parametricamente su dati abbondanti; FoT non lo fa affatto e lo dichiara lavoro futuro.

Non è `PIVOT` perché l'estimando `Δ_i` e la domanda scientifica restano ben posti — e FoT ne fornisce anzi la prima strumentazione parziale su un sistema testuale, mostrando che il tipo di misura richiesto è realizzabile.

Non è `GO ALL'IMPLEMENTAZIONE` perché FoT alza l'asticella della baseline obbligatoria: una libreria globale ben sintetizzata, con transfer verificato e reporting per-agente, batte gli agenti isolati **senza alcuna personalizzazione**. Il rischio di equivalenza, che Audit-1 identificava già come principale, cresce: non basta più superare un retrieval globale, occorre superare una **sintesi globale forte** — e FoT ne fornisce l'implementazione di riferimento.

### Modifica al profilo di rischio

Un rischio nuovo va registrato, di natura non scientifica ma pratica: **rischio di anticipazione**. Il lavoro più vicino sull'asse federato-testuale dichiara in §3.1, per iscritto, che la personalizzazione è la sua direzione futura dichiarata. Il gruppo che lo firma ha risorse rilevanti (University of Chicago e Google DeepMind), il preprint è già alla v2, e il codice è pubblico (`github.com/dixiyao/FoT`). La finestra temporale sul contributo residuo è verosimilmente stretta.

Va inoltre aggiornata la valutazione di Audit-1 sulla riga «Novità»: con sette elementi su dodici coperti da un singolo lavoro, e con la personalizzazione dichiarata come next step dagli autori di quel lavoro, la stima **2.5–3/5** proposta in Audit-1 §5 va portata verso il **2.5/5**, senza che questo modifichi la decisione.

---

## A.5 Sintesi in una riga per paper

- **P066 — DP-FPL (ICLR 2025):** ennesima conferma della famiglia parametrica personalizzata, su dati abbondanti, senza local-only e senza per-client. **Nessun impatto sul verdetto.**
- **P067 — Federation over Text (preprint arXiv:2604.16778):** il lavoro complessivamente più vicino del corpus (7/12), che chiude il payload testuale, la sintesi, la persistenza, il confronto local-only e — primo fra tutti — il reporting per-client; ma **non è Federated Learning, non ha strict K supervisionato, non personalizza il contesto e non misura il danno**, pur producendo dati che lo mostrano. **Restringe il claim residuo, non lo elimina.**

**Verdetto confermato: `GO ALLA VALIDAZIONE — gap plausibile, ancora da dimostrare`.**

---

*Fine dell'addendum. Come da istruzioni, l'audit principale non è stato riscritto, la V3 non è stata aggiornata e nessun esperimento è stato progettato.*
