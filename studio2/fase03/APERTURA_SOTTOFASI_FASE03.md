# Fase 03 — elenco di apertura delle sotto-fasi (proposta da confermare)

Data: **2026-09-13**. Stato: **proposta, non decisione** per tutte le righe non espressamente
confermate (`Fase_LLM.md`, «elencare non è decidere»). Redatto con modello capace e ragionamento
esteso, su repository a HEAD `b7f359f`, senza chiamate a modelli né simulazioni. Fonti lette: piano
§0.1, §6, §7, §8.4, D9; `Fase_LLM.md`; `MAINTENANCE.md` §8.6; walkthrough studio2 intestazione,
§0.1, §4.1–4.3 e tabella «Sintesi per sezione»; `PREFLIGHT_03_0.md`;
`IMPLEMENTATION_STATUS.md`; `PROVENIENZA.md` §4–§8; `PROPOSTA_OOD_D11.md`.

**Aggiornamento di coordinamento 2026-09-14.** Lo stato corrente prevale sulle
formulazioni storiche della proposta: 03.5 e 03.9 sono chiuse; 03.12 R4 è
pubblicata e congelata. Il piano statistico rev.10 al candidato
`6aaa5b3eebfed4ba502c25c0443caabd0051af21` ha verifica indipendente OK, ma
03.8 resta aperta per verifica del nuovo delta normativo, documentazione,
pubblicazione e freeze. Il delta respinto `4503cb6` è seguito dalle correzioni
R1–R4 a `9a56d12`, ora con OK indipendente acquisito. Il nuovo recepimento
D9 del 2026-09-15 ha ricevuto review distinta OK, acquisita byte-identica. Dal record dell’autore:
**122B producer principale e consumer; 27B producer alternativo con tutti i
16 insight; consumer 122B fisso nello swap; Terra solo storico descrittivo
interno separato dalle nuove stime, senza nuove chiamate Terra**. Il
[record D9](DECISIONE_AUTORE_D9_RUOLI_2026-09-14.md) e i due allegati sono
acquisiti byte-identici dal commit `aaba893dff8c62f9f9281eec7423eee020235e03`.
Ruoli approvati, record acquisito e recepimento documentale locale sono completati;
recepimento eseguibile nell'harness, identità/configurazioni, qualifiche e
fattibilità restano pendenti. Nessun 27B consumer fallback è approvato. Con la
[decisione procedurale del 2026-09-15](piano_statistico/DECISIONE_AUTORE_APPROVAZIONE_DOCUMENTATA_03_8_2026-09-15.md),
l'approvazione documentata dell'autore è sufficiente e la firma materiale non è
più richiesta; ordine label **1a** e autorizzazione alle chiamate restano separati.
La [matrice corrente](piano_statistico/MATRICE_RESIDUI_03_8_DOPO_D9.md) e la
[consegna tecnica successiva](piano_statistico/CONSEGNA_TECNICA_03_8_D9_PER_03_10.md)
aggiornano lo stato senza riscrivere le consegne già improntate.

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

## 3. Stato corrente delle sotto-fasi

Ordine del piano §6, con la dipendenza dichiarata: la colonna «pilot» dice se la sotto-fase è
un prerequisito del capability pilot (P) o ne è indipendente (—). Non è un riordino né
un'approvazione complessiva: è ciò che permette, con la data limite del 17 settembre, di decidere
cosa non può slittare.

| # | Sotto-fase (piano) | Profilo | Modello / ragionamento | Dipende da | Pilot | Congela / pubblica → ciclo §8.6 |
| :---: | --- | :---: | --- | --- | :---: | --- |
| 03.5 | **CHIUSA.** Score e soglie Normal secondo `DECISIONE_calibrazione_soglie_fase_B.md` rev. 19; FAR e U3 non sono riaperti da questo aggiornamento | I → B → A | ciclo completato nelle evidenze proprie | 03.3, freeze fase02 | — | completato nel proprio perimetro |
| 03.6 | **§6.4 Evidence 697-D e verbalizzazioni neutrali** dai 40 run di sviluppo; mapping a 9 label e assegnazione agenti come input di 03.7 | I | modello capace, ragionamento medio; estrazione pre-specificata, nessuna lettura del segnale per scegliere | 03.4, 03.3; per le soglie usa 03.5 solo se il verbalizzatore ne dipende (da dichiarare, altrimenti indipendente) | P | sì: lotto evidence/testi congelato → report + verifica |
| 03.7 | **§6.5 Nove pseudolabel opache (8 fault + Normal; `Unknown` = astensione, D10) e derangement zero-fixed-point di E** | I (combinatorio) con freeze | modello capace, ragionamento medio; basta un test che dimostri assenza di punti fissi e opacità; la sola scelta da congelare (seed, namespace) è mini-decisionale | 03.4, catalogo D1 | P | sì: freeze con seed → report breve + verifica |
| 03.8 | **APERTA.** Rev.10 verificata: D2=8; D11={F1,F2}/{F14,F15}; F6/F4 condizionati; m=0,125, alpha, gerarchia, A/B e politica R approvati. D9 è approvata e verificata; l'approvazione documentata dell'autore è sufficiente, senza firma materiale. Restano review del nuovo delta, documentazione, pubblicazione e tag | D | allineamento e chiusura documentale; nessuna esecuzione | 03.2; letteratura già pubblicata; 03.9 e 03.12 congelate | —; regole per il pilot consegnate a 03.10 | freeze solo dopo i residui espliciti |
| 03.9 | **CHIUSA, pubblicata e congelata.** Baseline numerica con tag `studio2-fase03-baseline-numerica-frozen-001` | I | verifiche e record di efficacia pubblicati | 03.4, 03.6 | — | completato nel proprio perimetro |
| 03.10 | **§6.8 Harness API**: 8 agenti, 14 insight, 9 pseudolabel con astensione, logging §8.7, set canary; già in gran parte in `studio2/fase03/` (`protocol.py`, `run_pilot.py`, `prepare_gate.py`, 16 test offline) — resta da collegare agli input reali e alla regola 03.4 | I (+ B minimo) | modello capace, ragionamento medio, test offline eseguiti; le eventuali chiamate sui ruoli effettivi vanno contate e autorizzate a parte, dopo configurazione e qualificazioni pertinenti | 03.4, 03.6, 03.7, 03.12 | P | report di sotto-fase; verifica sul gate 40×3 (03.13) |
| 03.11 | **§6.9 Run finali di test**: 72 primari (64 fault +8 Normal) +6 OOD +11 scorte tecniche =89 run del lotto; scorte senza nuove osservazioni. Dopo il freeze 03.8 e prima di chiamate sui test: generabilità, trip e ammissibilità F6/F4 e sostituti, senza selezione su prestazioni | B (spec I breve) | esecuzione non autorizzata qui | 03.8 congelata per criteri/catene; 03.3 | — | lotto sigillato futuro; nessun risultato 03.11 è prerequisito del tag 03.8 |
| 03.12 | **CHIUSA, R4 pubblicata e congelata.** Contratto schema insight taggato `studio2-fase03-schema-insight-frozen-001`; il pin nell'adapter resta 03.10 | D + I | ciclo R4 e pubblicazione completati | 03.2 | P | completato nel proprio perimetro |
| 03.13 | **Capability pilot, modello/i determinati da D9** — input/schema congelati → conformità (8 richieste/16 insight) → eventuale unica remediation autorizzata sul diff → prompt/capienza offline → sonda 3–9 → freeze configurazione → unico gate 40×3 → T3/T4/T6/T11 e latenza → T5 e altri bloccanti → GO/NO-GO | I → B → A → D | nessuna chiamata autorizzata da questo aggiornamento | 03.6, 03.7, 03.10, 03.12; D9 | P | massimi 152/160 con riserva inclusa; hard stop 200 |
| 03.14 | **§6.11 Baseline FedAvg** + pavimento locale e soffitto centralizzato (§9.3), specifica congelata prima di guardare il test | I (spec D breve) | specifica §9.2: capace, esteso; implementazione e run: capace, medio, test eseguiti; l'addestramento è CPU/GPU locale, non chiamate | 03.6 (evidence), 03.11 solo per l'esecuzione finale | — | sì: specifica congelata → report + verifica |
| 03.15 | **§6.12 Sezioni del paper indipendenti dal modello**: related work, metodo, verbalizzatore, threats to validity (comuni e indipendenti dalla qualificazione dei servizi; Terra resta storico interno) | D (redazione) | modello capace, ragionamento esteso; `letteratura.md` come unica fonte bibliografica | 03.2, 03.3, 03.12; `letteratura.md` | — | report di sotto-fase; verifica documentale |

Due record storici che non costituiscono una scelta D9 corrente:

1. **Quale pilot è 03.13.** Indicazione dell'autore (2026-09-13): il modello disponibile e usato
   finora è **Qwen-27B FP8 locale** (8001@16384); Qwen-2.4T non è disponibile. 03.13 è quindi il
   pilot sul 27B con la catena allora proposta (145 chiamate, €0). Per D9 ciò corrispondeva al «pilot breve»
   dell'opzione 2 se il 2.4T non arriva entro il 17; se arrivasse, la stessa catena andrebbe ripetuta
   su di esso come 03.13b, con endpoint e fingerprint propri. Il GO/NO-GO vale solo per la
   combinazione effettivamente verificata (PREFLIGHT, «Perimetro dell'eventuale GO»).
2. **Producer alternativo.** La nota storica associava Terra a una sola opzione.
   Il mandato corrente assegna i ruoli come sopra; le 8 richieste di
   conformità dell’alternativo restano differite fino alla configurazione
   effettiva e ai prerequisiti, senza assegnare Terra allo studio 2.

## 4. Solo per l'opzione B non adottata (Fasi 04–07 nell'opzione A)

| # | Fase / sotto-fase | Profilo | Modello / ragionamento |
| :---: | --- | :---: | --- |
| 7.2 | Produzione insight: libreria 8×2 dal producer principale e libreria completa dal producer alternativo (§8.4), entrambe validate contro lo schema 03.12 | B con gate D | batch **non qui**; accettazione della libreria: capace, esteso |
| 7.3 | Congelamento del protocollo finale | D | il più capace, esteso |
| 7.4 | Studio finale: A, B-LF, E-LF, swap, OOD, ablation e canary; conteggio completo parametrico da `BUDGET_RISORSE_REV10.md`, senza tetto rigido 3.700 | B | **non qui**; esecuzione subordinata a D9, T5 misurato +20% e tutti gli altri GO |
| 7.5 | Analisi e redazione | A + D | analisi: capace, medio, script riproducibili; redazione: capace, esteso |

## 5. Cammino critico verso il 17 settembre

Prerequisiti del pilot, in ordine vincolato: **03.4 → 03.12 → 03.7 → 03.6 → 03.10 → 03.13**.
La generazione 03.11 non è input del pilot. Le regole statistiche 03.8 devono
essere recepite e verificate in 03.10 prima del pilot; il freeze statistico segue
requisiti propri e non attende il completamento di 03.11. 03.6, 03.7, 03.12,
identità/configurazione e capienza restano prerequisiti del pilot. Ogni sotto-fase segue il ciclo
`Fase_LLM → Verifica_LLM (altra finestra, altro modello) → Documentazione_LLM → Commit_LLM`;
`REPORT_FASE03.md` e `VERIFICA_FASE03.md` si scrivono solo alla chiusura del perimetro confermato.
