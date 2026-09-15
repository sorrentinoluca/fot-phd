# Piano statistico completo — studio 2, Fase 03, sotto-fase 03.8 (piano §6.6)

Data della revisione 10: **2026-09-14**. Profilo: **decisionale**. Stato: **A/B approvate
e recepite; nuova verifica indipendente, firma materiale e condizioni residue pendenti**
(`PIANO_STATISTICO_FREEZE.json`, stato `revision_10_pending_independent_review`). Il piano
non è congelato, `freeze_tag` resta nullo e la sotto-fase 03.8 non è chiusa.
Base: commit `d815ce9` (branch `codex/studio2-piano-statistico`, worktree dedicato).
Nessuna chiamata a modelli linguistici, nessuna simulazione del processo, **nessun dato reale
consultato**: gli output dei run fault (`fault_runs/runs/`), i risultati di 03.5
(`soglie_normal/runs/`), le evidence e le firme del primo studio e i risultati per-fault di
`phase_b/` non sono stati aperti. Le uniche quantità del primo studio citate sono quelle che il
piano stesso riporta come attese, mai usate come calibrazione.

Il documento si congela **prima del primo run di test** (03.11) e non può essere rivisto dopo
(piano §8.1 «Congelamento: tutto prima del primo run di test»; §11 S6, S10, S11, S11b). Ogni
voce porta una delle tre marche:

- **[piano]** — ciò che il piano già impone; qui viene solo reso operativo;
- **[scelta di progetto]** — origine progettuale della regola; nella revisione 10 la tabella di
  §15 distingue le scelte confermate, quelle confermate condizionatamente e le condizioni
  operative ancora da provare;
- **[altra sotto-fase]** — ciò che appartiene a 03.5, 03.7, 03.10, 03.12 o 03.11: qui si scrive la
  specifica o il vincolo, non la decisione né il codice.

**Revisione 10 (2026-09-14), Codex GPT-6.** Recepimento delle sole formulazioni A e B
approvate senza modifiche da **Luca** il 14 settembre 2026, riferite all'addendum
al commit `526561feabeb6b4083170b1817b8abdac1a2a4c7`; record
[APPROVAZIONE_ADDENDUM_03_8.md](APPROVAZIONE_ADDENDUM_03_8.md). A sostituisce il tetto
rigido 3.700 con conteggio completo e fattibilità temporale misurata (+20%), senza
cambiare trigger R, hard stop pilot o riserva. B congela candidati/criteri/catene OOD
prima dei run e colloca i controlli tecnici 03.11 prima delle chiamate, eliminando
la dipendenza circolare del precedente §16. Ipotesi, m, alpha, gerarchia, reporting,
DESIGN_RESOLUTION, campioni, scorte, criteri OOD e regole di validità/remediation/gate
restano invariati. Nuova verifica indipendente **pending**; firma materiale separata.
Le note seguenti descrivono revisioni storiche, non lo stato corrente dei residui.

**Revisione 7 (2026-09-14), Codex GPT-6.** Correzione circoscritta dopo il sesto
verbale: il campo JSON è ora `one_sided_bound_distance`, con livello unilaterale
`1 - alpha_one_sided` (95% con α=0,05; 97,5% con α=0,025). Il valore resta
`z_(1-alpha) * SE`; `two_sided_halfwidth_95` resta bilaterale al 95%. Test specifico
su nome, metadato e valore per entrambi i livelli. Nessuna modifica alle decisioni.

**Revisione 9 (2026-09-14), Codex.** Correzione tracciata dopo il verbale indipendente rev. 8
NON OK (`VERIFICA_PIANO_STATISTICO_REV8.md`, conservato nel commit `f700326`): corrette nel
report le due impronte DESIGN_RESOLUTION trascritte erroneamente; ripristinate nel manifest le
impronte degli input e le mappe di perimetro della rev. 7; chiariti il residuo di sette chiamate
compatibile con la remediation, la provenienza dei due valori Tango e i tre recepimenti testuali
dall'addendum; aggiunta l'integrazione bibliografica alle condizioni residue. Nessuna decisione,
formula, artefatto DESIGN_RESOLUTION, sorgente o test è cambiato. La riverifica indipendente
ristretta del delta rev. 8→9 ha dato OK ed è preservata nel commit `29249a9`; non produce alcun
freeze e restano aperte le condizioni di §16.

**Revisione 8 (2026-09-14), Codex.** Recepimento delle approvazioni di **Luca**, registrate
il 14 settembre 2026 nella copia byte-identica `DECISIONI_AUTORE_03_8_bozza.md` (firma materiale
ancora pendente), e dell'esito bibliografico indipendente OK. Confermati D2=8, margine e alpha,
gerarchia e test, reporting per agente/fault, OOD F6/F4 entro le condizioni dichiarate, D11,
politica R, soglie del pilot, remediation T9, seed e undici scorte. La condizione numerica F6/F4
è soddisfatta; generabilità, trip e ammissibilità tecnica restano verifiche di §8/03.11. Il ramo
R=3 richiede ancora una decisione organizzativa perché il solo nucleo costerebbe 5.184 chiamate,
oltre il tetto di pianificazione 3.700. Nessuna nuova griglia, nessuna modifica a
`DESIGN_RESOLUTION.*`, al generatore o ai test. La riverifica indipendente della revisione 8 ha
poi dato NON OK per due impronte errate nel solo report; il merito del recepimento è risultato
altrimenti conforme ed è preservato nel commit `75bd148`.

**Revisione 6 (2026-09-14), Codex GPT-6.** Correzioni dopo il quinto verbale su
`dd82cd1`: score finito di Tango a zero discordanti; MDE espliciti sull'intera griglia;
propagazione di α alle simulazioni e agli MDE normali; guardia su letture/update anche via
`io.open`/`pathlib`; scenari analitici impossibili esclusi. Le decisioni proposte restano aperte.
Le note delle revisioni 2–5 sono storiche; la revisione 3 è **ritirata**.

**Revisione 4 (2026-09-13)**, dopo il terzo verbale (NON OK): la nulla di H1 e H2 torna la
nulla **debole** sulla media, Δ ≤ 0, come il piano la enuncia, e la decisione è il **test di
Hoeffding** sulla media delle medie di cluster (limitate in [−1, 1]): livello garantito per
qualunque distribuzione limitata con cluster indipendenti, senza simmetria né scambiabilità, verificato per enumerazione esatta
anche sul controesempio del verificatore (errore di primo tipo 0 a 48 e 64 cluster). La revisione
3 aveva torto due volte: «stessa distribuzione per ogni coppia» non implica la scambiabilità
congiunta del cluster che il sign-flip richiede, e Bahadur & Savage non si applica a medie di
cluster limitate, per cui un test valido esiste. Il sign-flip resta analisi supplementare sotto
la nulla forte di scambiabilità congiunta, correttamente enunciata. Prezzo: soglia di rifiuto
0,353 (48 cluster) e 0,306 (64); potenza analitica ≥ 0,87 a Δ = 0,5 e 1,00 a Δ = 0,7 su tutti gli
scenari ammissibili (d, ρ) della griglia; MDE normale approssimato all'80 % da 0,334
(64 cluster, d = 0,5, ρ = 0) a 0,462 (48 cluster, d = 0,8, ρ = 1). Con d = 0,3
l'80 % non è raggiungibile nell'approssimazione (§7.1).

**Revisione 3 (2026-09-13)**, dopo il secondo verbale (NON OK): l'ipotesi nulla di H1 e H2 è
dichiarata come **nulla forte** di scambiabilità delle due condizioni dentro ogni cluster
(l'ipotesi nulla di «nessun effetto» che le condizioni E-LF e A sono costruite per incarnare),
sotto cui il test di inversione di segno è esatto; la nulla debole «Δ ≤ 0» non è testabile a
livello garantito con potenza non banale (Bahadur & Savage 1956) e il controesempio del
verificatore (errore di primo tipo esatto 0,051 a 48 cluster e 0,085 a 64) è riprodotto nello
script e riportato in §4.3 e §7.1; la garanzia FWER è riformulata sulla famiglia così definita.

**Revisione 2 (2026-09-13)**, dopo il verbale `VERIFICA_PIANO_STATISTICO.md` (NON OK): la
gerarchia torna decisione aperta della decisione 5; la decisione di H1/H2 passa al test di
permutazione per inversione di segno, di livello 0,05 sotto scambiabilità delle condizioni nel
cluster, con il bootstrap come intervallo; corretta la frase sulla concordanza analitico/simulazione
e aggiunto l'errore Monte Carlo; la stratificazione per pseudolabel è marcata scelta di progetto;
T3/T9 allineati alla politica senza retry del pilot con una decisione dell'autore; la pretesa di
impronta riproducibile è limitata agli ambienti provati e i float del JSON sono canonicalizzati.

Numeri di risoluzione: tutti riproducibili con `design_resolution.py` (stessa cartella), che
lavora su dati sintetici nulli, con guardia esplicita contro ogni lettura di file; le tabelle
complete sono in `DESIGN_RESOLUTION.md` e `DESIGN_RESOLUTION.json` (seed 20260913, 400
repliche Monte Carlo per scenario, 2.000 ricampionamenti per replica; float serializzati con
12 cifre decimali). Riproducibilità verificata: risultati simulati identici su macOS/numpy 2.2.6,
Linux/numpy 2.4.4 e, dal verificatore, numpy 2.3.5; l'identità dell'impronta SHA-256 del JSON è
verificata solo sui primi due ambienti. I test sono in `test_design_resolution.py`.

---

## 0. Che cosa il piano impone e che cosa questo documento propone

| Voce | Il piano impone | Questo documento propone |
| --- | --- | --- |
| Disegno | 8 agenti, 8 fault D1, tre condizioni A / B-LF / E-LF, ≥6 run per fault, `Unknown` in tutte le condizioni, bootstrap a cluster appaiato con un cluster = un run simulato (§8.1) | — |
| Endpoint | tre numeri separati con il primo primario; calcolati e riportati per A, B-LF, E-LF (§8.5, S11b) | trattamento delle risposte non valide (§3.3) |
| Ipotesi | H1, H2 superiorità; H3 non inferiorità con margine *m*; tre ipotesi ciascuna a 0,05 (§8.5, S10) | forma unilaterale, statistica di decisione per ciascuna, regola per gli esiti degeneri (§4) |
| Gerarchia (decisione 5) | §8.5 scrive l'ordine H1 → H2 → H3, ma §0.1 lascia «margine *m* e gerarchia» da congelare | **confermata:** sequenza fissa H1 → H2 → H3, α unilaterale 0,05; decisioni locali Hoeffding (H1, H2) e Tango (H3), con controllo complessivo approssimato per la componente Tango (§4.2) |
| Margine *m* | giustificazione operativa, verificata sulla risoluzione del disegno; §10.3 non va usato per fissarlo (§8.5) | **confermato:** *m* = 0,125 come massima perdita media netta dichiarata sui local-seen, senza garanzia individuale; H3 a 0,025 è sola sensibilità (§5) |
| Bootstrap | cluster appaiato, un cluster = un run simulato, da adattare alle nove classi (§8.1) | stratificazione per pseudolabel come nel pattern HC `phase_b/evaluation/bootstrap.py`, estesa a 8 strati di fault + strato Normal, 7 righe per cluster, astensione nelle righe, 10.000 repliche, seed; il bootstrap è l'**intervallo**, non la decisione (§4.3, §6) |
| D2 | 6 o 8 run (§8.8, D2); il +590 storico non coincide con i totali, vedi §7.2 | **confermato: 8 run fault (64 cluster) e 8 run Normal primari** (§7) |
| OOD (decisione 3) | 2 fault fuori catalogo, 3 run, 8 agenti, 3 condizioni; distinti meccanicamente da tutti gli 8; rilevabilità documentata; fuori dal gruppo H (§8.6, S13) | **F6 + F4 confermati condizionatamente**; condizione bibliografica numerica soddisfatta, condizioni tecniche residue e catene di sostituzione preservate (§8) |
| D11 | coppie confondibili su base meccanica, dichiarate prima; 8 × n × 1 + 4 × 3 × 7 chiamate (§8.3) | **confermato: {F1, F2} e {F14, F15}**, run 1–3 del lotto sigillato, metrica dell'ablation (§9) |
| R (decisione 11) | gate sull'evento «divergenza fra ripetizioni dello stesso prompt», unità = prompt; l'assenza di temperatura/seed non attiva R=3 da sola (§8.7, D7) | **confermato:** divergenza della coppia parsata o della validità attiva R=3; audit, canary e sospensioni di §10; regola organizzativa A approvata, fattibilità effettiva ancora da verificare |
| GO/NO-GO | checklist §11, regola «GO se e solo se tutti i bloccanti» | **confermati:** soglie T3–T6, T9, T11, ordine obbligatorio, una sola remediation e riserva unica (§11) |
| Reporting | stratificato continuità / nuovi / aggregato (§8.5, S14) | in più: H/O, local-seen/unseen, Normal, per-fault; formato delle tabelle (§12) |

---

## 1. Perimetro, dipendenze e confini con le altre sotto-fasi

Questo documento fissa **come si analizza**. Non decide:

- **la soglia e il FAR** — decisi in 03.5 secondo `docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md`
  (rev. 19): 350 run `cal_thr`, quantile di rango k = 334, livello dichiarabile 4,84 %, Beta(17, 334)
  sotto continuità, 150 run `far_ver` per la verifica con intervallo binomiale esatto. Qui è un
  **vincolo**: la soglia entra nella verbalizzazione e nell'evidence, non nell'analisi degli esiti;
  l'analisi non la ridiscute e non la ricalibra sui test;
- **lo schema degli insight** — 03.12 (D12, §8.9);
- **i valori delle nove pseudolabel e il derangement di E** — 03.7 (§6.5, D10);
- **l'implementazione della terza metrica e del bootstrap** — 03.10 (§6.8): qui ne è scritta la
  specifica (§3, §6), il codice arriva dopo e va verificato contro questa specifica;
- **la generazione dei run di test** — 03.11 (§6.9): qui si fissano il numero (D2), i fault OOD e
  due vincoli di generazione (§7.4, §8.5).

**Vincoli che questo documento impone alle altre sotto-fasi** (da dichiarare nei loro report):

| Verso | Vincolo |
| --- | --- |
| 03.11 | n = 8 run per fault e 8 Normal primari; 2 fault OOD × 3 run; identificativi ordinati e sigillati prima di ogni chiamata; **11 scorte** (8 fault D1, Normal, 2 OOD), generate nello stesso lotto e usate solo per sostituzione tecnica pre-specificata prima delle chiamate (§7.4); candidati/criteri/catene congelati prima dei run, controlli tecnici dopo il freeze e prima delle chiamate (§16) |
| 03.10 | bootstrap a 8 strati × n cluster × 7 righe (local-unseen) e × 1 riga (local-seen); righe con campo `abstain`; terzo numero; test di Hoeffding per H1/H2 e test score di Tango per H3 come decisioni, sign-flip di cluster supplementare; formato del log per audit e canary (§6, §10) |
| 03.7 | nessuno: il piano usa le pseudolabel come chiavi di strato, qualunque valore abbiano |
| 03.12 | nessuno sui campi; il numero di insight per prompt (14) entra solo nei threats |
| 03.13 | le soglie confermate di §11, l'ordine obbligatorio e la riserva unica vanno riportati nel `frozen_gate_config.json`; l'eventuale remediation richiede autorizzazione scritta sul diff concreto |

---

## 2. Popolazione, strati, unità e cluster

### 2.1 Popolazioni

**[piano]** Ogni agente possiede localmente **uno** degli otto fault (`protocol.py`: gli otto agenti
possiedono le otto pseudolabel di fault uno a uno) e conosce Normal. Per ogni run di test di un
fault in catalogo, un agente è **local-seen** (il proprietario) e sette sono **local-unseen**.

| Popolazione | Definizione | Osservazioni per cluster e condizione | Ruolo |
| --- | --- | ---: | --- |
| **P1 — local-unseen** *(primaria)* | coppie (agente, caso) in cui la pseudolabel vera del caso è un fault del catalogo diverso da quello locale dell'agente | 7 | H1, H2 |
| **P2 — local-seen** | coppie (agente, caso) in cui la pseudolabel vera è il fault locale dell'agente | 1 | H3 |
| **P3 — Normal** | tutti gli 8 agenti sui run Normal di test | 8 | descrittiva |
| **P4 — OOD** | tutti gli 8 agenti sui 6 run fuori catalogo | 8 | sonda §8.6, descrittiva |
| **P5 — ablation** | B-senza-LF su P2 (tutti gli 8 fault) e su P1 ristretta ai 4 fault delle coppie D11, run 1–3 | 1 / 7 | §8.3, descrittiva |

**[scelta di progetto]** Normal non entra in P1 né in P2: il piano parla di local-seen come «i fault
già noti» e conta 48 cluster local-seen a 6 run, cioè 8 fault × 6 run senza Normal. H3 riguarda
quindi la conservazione delle diagnosi sul **fault locale**; il comportamento su Normal è riportato
a parte (§12), con il tasso di falsi fault per condizione.

### 2.2 Unità di analisi e cluster

**[piano]** L'unità di analisi è la coppia (agente, caso, condizione); il **cluster fisico** è il run
simulato, identificato da (fault, indice di run) — `physical_case_id` nel pattern HC. Le 7 righe
local-unseen dello stesso run restano insieme in ogni ricampionamento; la riga local-seen dello
stesso run appartiene a P2 e forma un cluster da una sola osservazione.

Numero di cluster: **8 · n**, cioè 48 con n = 6 e 64 con n = 8. L'appaiamento fra condizioni è
esatto: la stessa coppia (agente, caso) è valutata in A, B-LF ed E-LF.

**[piano]** `independence_claim: False`: gli intervalli misurano la variabilità fra run simulati,
non la variabilità delle risposte del modello alla stessa richiesta (R=1, §8.7). Va scritto così
nel report dei risultati, non assunto nullo.

### 2.3 Strati

| Strato | Uso |
| --- | --- |
| pseudolabel vera (8 fault) | **strato del bootstrap**: il ricampionamento avviene dentro ciascuno degli 8 strati, n cluster per strato |
| continuità {F1, F8, F10, F13} / nuovi {F2, F3, F14, F15} | reporting obbligatorio (§8.5, S14) |
| H {F3, F15} / O (gli altri sei) | reporting obbligatorio aggiuntivo **[scelta di progetto]**: è lo strato di difficoltà documentata (§12.1–12.2) e va mostrato prima che un lettore lo chieda |
| local-seen / local-unseen | popolazioni P1 e P2 |
| condizione A / B-LF / E-LF | i tre numeri sono calcolati separatamente per ciascuna (S11b) |

---

## 3. Endpoint: i tre numeri

### 3.1 Definizioni **[piano]**

Per ogni condizione, popolazione e strato:

1. **Accuratezza su tutti i tentativi** — corretti / tutti; l'astensione conta come non corretta.
   **Primario.** È la colonna `accuracy` di `phase_b/evaluation/metrics.py` (`is_correct` richiede
   `abstain = false` e `predicted_label` uguale alla pseudolabel vera).
2. **Tasso di astensione** — astenuti / tutti (`abstention_rate`, stesso modulo).
3. **Accuratezza sui soli non astenuti** — corretti / (tutti − astenuti). **Nuova**: assente dagli
   artefatti congelati per assenza verificata (§8.5, revisione 5); la sua implementazione è di 03.10.

Il numero 3 è **descrittivo**: non entra in nessuna ipotesi. Il suo denominatore dipende dal
comportamento del modello e non è appaiato fra condizioni, quindi non regge un contrasto causale.

### 3.2 Contrasti

I contrasti sono differenze appaiate del **numero 1**, coppia per coppia:

- **Δ₁ = acc(B-LF) − acc(E-LF)** su P1 — H1;
- **Δ₂ = acc(B-LF) − acc(A)** su P1 — H2;
- **Δ₃ = acc(B-LF) − acc(A)** su P2 — H3.

Il contrasto B − E porta il claim causale (§8.5): tiene costante lunghezza del contesto e politica
local-first e cambia solo l'informazione. Nessun contrasto usa i numeri 2 o 3.

### 3.3 Risposte non valide **[scelta di progetto]**

Una risposta che non supera il parser dopo la politica di retry congelata in 03.10 è
**non valida**. Regola: conta nel denominatore del numero 1 come non corretta; **non** è
un'astensione (numero 2); entra nel denominatore del numero 3 come non corretta. Il tasso di
risposte non valide è riportato come quarto numero descrittivo per condizione. Motivo: trattarla
come astensione confonderebbe il rifiuto del compito con un guasto del formato, e toglierla dal
denominatore premierebbe le condizioni che rompono il formato più spesso.

---

## 4. Ipotesi, statistiche di decisione e gatekeeping

### 4.1 Le tre ipotesi **[piano]**

| # | Ipotesi | H₀ | H₁ | Popolazione |
| --- | --- | --- | --- | --- |
| H1 | B-LF supera E-LF | Δ₁ ≤ 0 (nulla debole sulla media della differenza di accuratezza su P1) | Δ₁ > 0 | P1 |
| H2 | B-LF supera A | Δ₂ ≤ 0 | Δ₂ > 0 | P1 |
| H3 | B-LF non inferiore ad A | Δ₃ = −*m* (bordo della nulla debole Δ₃ ≤ −*m*) | Δ₃ > −*m* | P2 |

**[scelta di progetto — revisione 4]** Per H1 e H2 la nulla è quella che il piano enuncia:
**la media** della differenza di accuratezza non supera zero. La decisione è il **test di
Hoeffding (1963)**: le medie di cluster D_c della differenza stanno in [−1, 1] e sono
indipendenti fra cluster (run simulati con stream separati), quindi
P(D̄ − E[D̄] ≥ t) ≤ exp(−N t²/2) per qualunque distribuzione, e la regola «rifiuta se D̄ ≥ t_α
con t_α = √(2 ln(1/α)/N)» ha livello ≤ α sotto tutta la nulla debole, senza ipotesi di simmetria,
di scambiabilità o di forma, e qualunque sia la dipendenza dentro il cluster. Con α = 0,05:
**t = 0,353 a 48 cluster e 0,306 a 64**. Il test è conservativo, e il prezzo è in potenza (§7.1):
elevata per gli effetti dell'ordine di quelli che il piano cita come attesa (§8.5: B 68/72 contro
E 4/72; A ≈ 0 sui local-unseen): potenza analitica ≥ 0,87 (48) e ≥ 0,96 (64) a Δ = 0,5, 1,00 a
Δ = 0,7, su tutti gli scenari ammissibili di discordanza d e correlazione ρ della griglia; effetto minimo
rilevabile all'80 %, che dipende da d e ρ: da 0,42 (d = 0,5, ρ = 0,5) a 0,44 (d = 0,8, ρ = 0,5) a
48 cluster e, per le stesse coppie (d, ρ), da 0,36 a 0,38 a 64; con ρ = 1 e d = 0,8 salgono a
0,46 e 0,40 (§7.1).
Questa scelta è **confermata dall'autore**. La garanzia riguarda il livello sotto la nulla debole
e richiede indipendenza fra le medie di cluster; ammette dipendenza intra-cluster arbitraria.
Non garantisce potenza, non dimostra l'indipendenza effettiva dei run e non permette di dedurre
la potenza congiunta della gerarchia dalle potenze marginali.
Effetti veri fra 0,1 e 0,3 hanno potenza inferiore all'80 % nella griglia: la soglia
di rifiuto riguarda la **media osservata**, non l'effetto vero. Un campione può comunque
superarla; non si afferma che la conferma sia impossibile. È il costo della garanzia di livello.

Perché non la nulla forte con il sign-flip (revisione 3, ritirata): il test di inversione di segno
è esatto solo se il vettore delle medie di cluster è invariante alle inversioni, cioè sotto la
scambiabilità **congiunta** delle due condizioni dentro ogni cluster; «stessa distribuzione per
ogni coppia (agente, caso)» non la implica, come mostra il controesempio del verificatore, che
può soddisfare la nulla per coppia e dare errore di primo tipo 0,085 a 64 cluster. E il teorema di
Bahadur & Savage (1956) non vieta un test valido per la media qui: la classe del teorema richiede
la possibilità di ogni media reale, che manca sotto il limite comune D_c ∈ [−1, 1]. Il test di
Hoeffding esiste ed è quello adottato. Il
controesempio — medie di cluster +1/7 con probabilità 7/8 e −1 con probabilità 1/8, E[D] = 0 —
è riprodotto per enumerazione esatta in `design_resolution.py` (`weak_null_counterexample`):
sign-flip **0,051 / 0,085**, test t di cluster 0,134 / 0,085, **Hoeffding 0 / 0**.

Il sign-flip a livello di cluster resta come **analisi supplementare** sotto la nulla forte di
scambiabilità congiunta delle due condizioni nel cluster (l'ipotesi di nessun effetto in senso
di Fisher), riportato con il suo p-value e con la dichiarazione della nulla che testa; non entra
nella sequenza confermativa.

**[scelta di progetto confermata]** Tutte e tre sono **unilaterali**, con α = 0,05 ciascuna,
perché il piano le enuncia come direzionali («ciascuna a 0,05»). H3 viene inoltre ricalcolata a
**α = 0,025 come sensibilità pre-specificata**, senza sostituire l'esito primario né scegliere
fra i due risultati a posteriori. A 64 cluster, d = 0,10 e *m* = 0,125, la potenza analitica
normale passa da 0,9354 a 0,8854; il controllo Tango separato disponibile dà 0,8675 e 0,8075
(registrati nell'Allegato A delle decisioni autore e nel report storico al commit `7f760b7`).
L'intervallo unilaterale Tango A2-bis **non è adottato**. La convenzione ICH E9 delimita il
confronto dei livelli, ma non sceglie né α né *m* per FoT.

### 4.2 Gerarchia **[scelta di progetto — decisione 5, confermata]**

Il piano §8.5 scrive l'ordine H1, poi H2, poi H3, ciascuna a 0,05; §0.1 (decisione 5) chiede però
che «il margine *m* e la gerarchia di test» siano congelati dall'autore. Luca ha confermato la
**sequenza fissa H1 → H2 → H3**, ciascuna a
α = 0,05, si procede solo se la precedente rifiuta H₀. La procedura a sequenza fissa controlla
l'errore familiare a 0,05 senza aggiustamento dei livelli (Maurer, Hothorn & Lehmacher 1995;
Westfall & Krishen 2001 — esterni al corpus, §17) **a condizione che ogni test locale sia di
livello 0,05 per la propria nulla**. Con le nulle di §4.1 la garanzia vale così: per H1 e H2 il
test di Hoeffding ha livello ≤ 0,05 sotto la nulla debole per qualunque distribuzione limitata
(garanzia finita, non asintotica); per H3 il test score di Tango è asintotico, con livello simulato
0,025–0,0725 a 48–64 coppie (§7.1). Il controllo del FWER a 0,05 è quindi **garantito (in modo
conservativo) sulla componente H1/H2 e approssimato su H3**, e va scritto in questi termini nel
paper. È la ragione per cui le decisioni di §4.3 non sono il percentile bootstrap né il sign-flip,
i cui livelli non sono garantiti sotto la nulla debole (§4.1, §7.1). Motivo dell'ordine: H1 porta il claim causale,
H2 il valore aggiunto, H3 è informativa solo se le due superiorità reggono (§8.5).
Se H1 non rifiuta, H2 e H3 sono riportate con stime e intervalli ma **senza** dichiarazione
confermativa; lo stesso per H3 se H2 non rifiuta. Non si cambia l'ordine dopo aver visto i dati.

### 4.3 Statistiche di decisione **[scelta di progetto]**

| Ipotesi | Decisione primaria (test di livello 0,05) | Intervallo riportato accanto |
| --- | --- | --- |
| H1, H2 | **test di Hoeffding**: media delle N medie di cluster di Δ su P1 ≥ t_α = √(2 ln 20 / N), cioè **≥ 0,353** (48 cluster) o **≥ 0,306** (64); unilaterale, α = 0,05, nessuna ipotesi di forma | bootstrap a cluster stratificato di Δ (§6): intervallo al 95 % e quantile 5 %; sign-flip di cluster come supplementare (nulla forte, §4.1) |
| H3 | **test score di Tango (1998)** per la differenza di proporzioni appaiate, H₀: Δ₃ = −*m*, unilaterale, Z > 1,645 | bootstrap di Δ₃: intervallo al 95 % e quantile 5 % |

Perché H3 non usa il bootstrap come decisione: su P2 ogni cluster ha una sola osservazione, quindi
il bootstrap a cluster ricampiona coppie binarie **entro ciascuno degli otto strati**, e con poche coppie discordanti il
percentile è **anti-conservativo**. La simulazione (§7.1) lo misura: al bordo Δ₃ = −*m*, con
discordanza d = 0,10, e margine m = 0,10, il bootstrap rifiuta il 12,5 % (48 cluster) e il 9,25 % (64) delle volte
contro il 5 % nominale; Tango rifiuta il 2,75 % e il 2,5 %. Il MCSE al livello 0,05
è circa 0,011 con 400 repliche; questa stima non è una garanzia esatta di livello.

Perché H1 e H2 non usano il bootstrap né il sign-flip come decisione: nella simulazione il livello
del percentile sotto Δ = 0 va da 0,020 a 0,085 (errore Monte Carlo ≈ 0,011 al livello 0,05) già sotto nulle
simmetriche; il sign-flip è esatto solo sotto la scambiabilità congiunta e sotto la nulla debole
asimmetrica del controesempio arriva a 0,085 (§4.1, §7.1). Il test di Hoeffding usa soltanto la
limitatezza delle medie di cluster e l'indipendenza fra cluster: non richiede ipotesi sulla
correlazione intra-cluster (le 7 righe restano insieme nella media di cluster) né sulla forma
della distribuzione, e nel controesempio ha errore di primo tipo esatto 0. Il bootstrap resta ciò
che il piano prescrive per gli **intervalli**: stima e incertezza, riportate accanto alla
decisione.

Il test di Tango è definito su coppie indipendenti: vale su P2 perché le coppie **sono** i cluster.
La formula è in `design_resolution.py` (`tango_score_z`), con la MLE vincolata `tango_restricted_p21`
verificata dai test sull'equazione di verosimiglianza.

### 4.4 Esiti degeneri **[scelta di progetto]**

- Se nessuna coppia di P2 è discordante (b = c = 0), sotto δ₀ = −m la MLE vincolata è
  p₂₁ = m, p₁₂ = 0. Lo score è **finito**: Z = √(Nm/(1−m)). Con m = 0,125 vale
  **2,619** a 48 coppie e **3,024** a 64: supera z₀,₉₅, quindi H3 rifiuta localmente.
  La conclusione confermativa richiede anche il superamento di H1 e H2 (§4.2).
  Si riporta «zero coppie discordanti su N»; il test verifica formula e finitezza;
- se in uno strato tutti i delta sono uguali, la distribuzione bootstrap è degenere su quello
  strato: si riporta la distribuzione discreta osservata, non un intervallo «[x, x]» senza commento;
- una discordanza fra la decisione (Hoeffding per H1/H2, Tango per H3) e l'intervallo bootstrap
  riportato accanto, o il sign-flip supplementare, è **riportata**, non risolta scegliendo dopo;
  la conclusione confermativa segue la decisione;
- se tutte le medie di cluster di P1 sono nulle, la media è 0 < t_α e H1/H2 non rifiutano: si
  riporta il fatto, senza altra analisi.

### 4.5 Che cosa non è un test

Nessun'altra analisi di questo documento è confermativa. OOD, ablation, producer-swap, E5, baseline
numerica e FL, Normal, per-fault e per-strato sono descrittive: stime con intervalli, nessun p-value
interpretato come conferma (§13).

---

## 5. Il margine *m* di non inferiorità — decisione confermata

**[piano]** Il margine richiede una giustificazione esterna ai risultati, con la risoluzione del
disegno come controllo di sanità; il dato di §10.3 non fissa *m*.

**[scelta di progetto confermata] *m* = 0,125** è la **massima perdita media netta dichiarata**
accettabile in questo studio per Δ₃ = acc(B-LF) − acc(A) sui local-seen, con uguale peso agli
otto fault. Equivale a 12,5 punti percentuali sulla media: una perdita media maggiore non
soddisfa H3, qualunque sia il guadagno sui local-unseen. È una tolleranza sostanziale dello
studio, non una soglia validata di adottabilità industriale e non un valore scelto per
massimizzare la potenza.

Il margine è **aggregato**. Non garantisce non inferiorità per ciascun agente o fault e può
nascondere peggioramenti concentrati. Con D2=8, 8/64 rende leggibile il bordo campionario ma non
è una regola di superamento: la decisione resta lo score di Tango, che dipende dai conteggi
discordanti guadagnati e persi, non dal solo saldo. Non si traduce *m* in un numero fisso di
perdite ammesse. Il fatto che 0,125 cada sulla griglia osservabile non è la giustificazione del
parametro di popolazione.

La verifica di risoluzione di §7.1 resta un limite, non l'origine della scelta: a 64 cluster e
d=0,10 la potenza normale/Tango è 0,94/0,86; a d=0,20 è 0,72/0,70. L'MDE normale è 0,098 e
0,139 rispettivamente. I valori a *m*=0,10 o 0,15 restano scenari storici della griglia, non
alternative ancora aperte. Il 23/24 di §10.3, lo 0/72 della replica ed E5-C1 non calibrano *m*.

**Sensibilità confermata.** H3 viene eseguita anche a α unilaterale 0,025, riportata accanto
all'esito primario a 0,05 e incapace di sostituirlo. L'intervallo Tango A2-bis non è adottato.
Il controllo della sequenza completa resta approssimato perché Tango è asintotico e il suo
modello IID/multinomiale non deriva automaticamente dal campionamento a quote fisse per fault.

---

## 6. Specifica del bootstrap a cluster stratificato (per 03.10)

**[piano]** Cluster appaiato, un cluster = un run simulato, da adattare alle nove classi (§8.1),
con la definizione di §6.5 del record del primo studio: «le osservazioni dei riceventi associate
allo stesso run vengono mantenute insieme». **[scelta di progetto]** La stratificazione per
pseudolabel non è scritta nel piano: viene dal pattern HC di `phase_b/evaluation/bootstrap.py`
(`draw_stratified_physical_clusters`, `expand_cluster_sample`) e si adotta perché mantiene fisso il
numero di cluster per fault in ogni ricampione, cioè la composizione del catalogo.

**[scelta di progetto]** Estensione, da implementare in un file nuovo di `studio2/` (MAINTENANCE
§8.2), non modificando l'originale:

| Elemento | Specifica |
| --- | --- |
| righe | (agente, `physical_case_id`, condizione, pseudolabel vera, `abstain`, `predicted_label`, `valid`) |
| strati | le 8 pseudolabel di fault del catalogo; Normal è uno strato a sé, usato solo per P3 |
| cluster per strato | n (6 o 8), identico in tutti gli strati; l'asserzione HC «4 strati × 3 run × 3 righe» diventa «8 strati × n run × 7 righe» per P1 e «× 1 riga» per P2, verificata prima del ricampionamento |
| ricampionamento | dentro ogni strato, n cluster con reinserimento; espansione di **tutte** le righe del cluster; statistica sulle righe espanse |
| statistica | media dei delta per osservazione (numero 1 appaiato); per i numeri 2 e 3 la stessa espansione, con il numero 3 ricalcolato sul denominatore del ricampione (se nullo, replica esclusa e contata) |
| repliche | **10.000** (come il pattern HC) |
| seed | **20260913**, namespace `studio2-fase03-piano-statistico-v1`; un solo generatore `numpy.random.default_rng(seed)` per analisi, ordine delle analisi fissato nel codice |
| intervalli | percentile: 2,5 %/97,5 % e quantile 5 %, entrambi riportati; nessuno dei due è una decisione |
| astensioni | restano nelle righe con `abstain = true`; il numero 1 le conta non corrette; non vengono mai rimosse dal cluster |
| uscita | `point_estimate`, `ci_lower`, `ci_upper`, `q05`, `iterations`, `seed`, `n_physical_clusters`, `n_agent_case_rows`, `clusters_per_pseudolabel`, `independence_claim: false`, più i conteggi grezzi per strato |

Il test di Hoeffding (H1/H2, decisione) e il sign-flip (supplementare) usano le medie di cluster su P1 e lo stesso
generatore; il test di Tango (H3) usa i conteggi b (B corretto, A errato) e c (B errato, A corretto)
su P2.

---

## 7. Risoluzione del disegno e D2: 8 run per fault confermati

### 7.1 Numeri

Modello dei dati sintetici (dichiarato in `design_resolution.py`): per ogni osservazione il delta
vale +1, −1 o 0 con probabilità (d + δ)/2, (d − δ)/2 e 1 − d, dove **d** è il tasso di discordanza
fra le due condizioni e **δ** l'effetto vero; per P1 la correlazione intra-cluster ρ è ottenuta per
mescolanza (con probabilità ρ le 7 righe del cluster copiano un solo delta), che preserva le
marginali e dà correlazione esattamente ρ. Nessun parametro è stimato da dati: sono scenari.

**H3 — non inferiorità, *m* = 0,125, α = 0,05 unilaterale** (analitico; fra parentesi la simulazione
con il test di Tango, 400 repliche):

| cluster | d = 0,05 | d = 0,10 | d = 0,20 | d = 0,30 | *m* minimo all'80 % (d = 0,10 / 0,20) |
| ---: | ---: | ---: | ---: | ---: | ---: |
| **48** (6 run) | 0,99 (0,9325) | 0,86 (0,7650) | 0,61 (0,5775) | 0,47 (0,4425) | 0,113 / 0,161 |
| **64** (8 run) | 1,00 (0,9800) | 0,94 (0,8600) | 0,72 (0,6975) | 0,57 (0,5375) | 0,098 / 0,139 |

Semiampiezza attesa dell'intervallo al 95 % bilaterale su Δ₃: 0,089 (48) e 0,077 (64) a d = 0,10;
0,127 e 0,110 a d = 0,20. Errore di primo tipo realizzato al bordo con il test di Tango: fra 0,025 e
0,0725 negli scenari al bordo ammissibili (bootstrap percentile: fino a 0,13 a d = 0,10, §4.3).

**H1/H2 — riferimento normale, α = 0,05 unilaterale**, diverso dal test primario di
Hoeffding (potenza per Δ = 0,10 / 0,20 / 0,30):

| cluster | d | ρ = 0 | ρ = 0,25 | ρ = 0,5 | ρ = 1 | Δ minimo all'80 % (ρ = 0,5) |
| ---: | ---: | --- | --- | --- | --- | ---: |
| 48 | 0,50 | 0,83 / 1,00 / 1,00 | 0,50 / 0,95 / 1,00 | 0,36 / 0,83 / 0,99 | 0,25 / 0,62 / 0,90 | 0,192 |
| 64 | 0,50 | 0,91 / 1,00 / 1,00 | 0,60 / 0,98 / 1,00 | 0,44 / 0,91 / 1,00 | 0,30 / 0,73 / 0,96 | 0,166 |
| 48 | 0,80 | 0,66 / 0,99 / 1,00 | 0,36 / 0,83 / 0,99 | 0,27 / 0,66 / 0,92 | 0,19 / 0,46 / 0,75 | 0,243 |
| 64 | 0,80 | 0,76 / 1,00 / 1,00 | 0,44 / 0,91 / 1,00 | 0,32 / 0,76 / 0,97 | 0,23 / 0,56 / 0,85 | 0,210 |

Concordanza fra simulazione e analitico (tabella completa in `DESIGN_RESOLUTION.md`): lo
scostamento massimo fra potenza del bootstrap e potenza analitica è 0,1096 (48 cluster, d = 0,50,
ρ = 0,25, Δ = 0,10) e supera 0,05 in 11 scenari su 72; con 400 repliche l'errore Monte Carlo di una
potenza è al massimo 0,025 (semiampiezza 95 % ≈ 0,05), e l'analitico usa Var(δ) = d mentre sotto
l'alternativa la varianza marginale è d − Δ². Le differenze fra 48 e 64 cluster (≈ 0,09–0,10 per
H3) sostengono la direzione della raccomandazione di D2, non una precisione a pochi punti. Il
test di inversione di segno resta supplementare sotto la nulla forte: gli scostamenti massimi
dalla potenza normale sulla stessa griglia sono 0,0421 per ρ ≤ 0,5 e 0,1294 per ρ = 1. La decisione di
H1/H2 è il test di Hoeffding, i cui numeri seguono.

**Test di Hoeffding, decisione di H1/H2 (revisione 4).** Soglia t_α = 0,353 (48 cluster) e 0,306
(64). Potenza analitica (normale) e simulata (fra parentesi, 400 repliche) per Δ = 0,30 / 0,50 /
0,70:

| cluster | d | ρ = 0 | ρ = 0,5 | ρ = 1 | Δ minimo all'80 % (ρ = 0,5) |
| ---: | ---: | --- | --- | --- | ---: |
| 48 | 0,80 | 0,14 / 1,00 / 1,00 | 0,29 (0,30) / 0,93 (0,97) / 1,00 (1,00) | 0,34 / 0,87 / 1,00 | 0,435 |
| 64 | 0,80 | 0,44 / 1,00 / 1,00 | 0,47 (0,45) / 0,99 (1,00) / 1,00 (1,00) | 0,48 / 0,96 / 1,00 | 0,377 |
| 48 | 0,50 | 0,08 / 1,00 / — | 0,24 / 0,97 / — | 0,30 / 0,92 / — | 0,418 |
| 64 | 0,50 | 0,43 / 1,00 / — | 0,46 / 1,00 / — | 0,47 / 0,99 / — | 0,362 |

(Δ = 0,70 non è ammissibile con d = 0,50.) Sotto Δ = 0 il tasso di rifiuto simulato è ≤ 0,005 in tutti
gli scenari: il test è conservativo, come atteso da una disuguaglianza. A Δ = 0,5 la potenza minima
sulla griglia è 0,87 analitica (48 cluster, d = 0,8, ρ = 1) e 0,92 simulata; a Δ = 0,7 è 1,00 in
ogni scenario. Per gli effetti che il piano cita come attesa (ordine di 0,7–0,9 per H1 e H2) il
test ha elevata potenza negli scenari sintetici esaminati. Per effetti veri fra 0,1 e 0,3
la potenza è inferiore all'80 %, pur senza escludere il rifiuto in un singolo campione.
Gli MDE di Hoeffding sono approssimati con t_α + z₀,₈₀ SE, usando Var(δ) = d;
non sono soluzioni esatte della potenza del test. La formula e la fattibilità MDE ≤ d
sono esportate nel JSON e nella tabella generata, separate dall'MDE del test normale.
L'intera griglia ammissibile dà **0,334–0,462**; **0,36–0,46** descrive soltanto il
sottoinsieme con **ρ ≥ 0,5** e d ∈ {0,5; 0,8}. Per d = 0,3 gli MDE superano d:
l'80 % non è raggiungibile nell'approssimazione. Le potenze simulate sono marginali
per singolo test; la probabilità di superare l'intera sequenza H1 → H2 → H3 non è
calcolata, perché manca un modello congiunto delle tre condizioni.

**Nulle asimmetriche.** Le simulazioni con Δ = 0 generano P(+1) = P(−1), cioè nulle simmetriche, e
non possono mostrare che cosa accade sotto la sola nulla debole. Il controesempio esatto del
secondo verbale, riprodotto da `weak_null_counterexample` (enumerazione, nessuna simulazione):

| cluster | distribuzione della media di cluster | E[D] | sign-flip | test t di cluster | **Hoeffding** |
| ---: | --- | ---: | ---: | ---: | ---: |
| 48 | +1/7 con prob. 7/8, −1 con prob. 1/8 | 0 | 0,0508 | 0,134 | **0** |
| 64 | idem | 0 | 0,0850 | 0,085 | **0** |

Il sign-flip e il test t non sono di livello 0,05 sotto la nulla debole; Hoeffding sì, per
costruzione, e il calcolo esatto lo conferma (test dedicato).

Lettura: con Hoeffding H1/H2 sono ben risolte negli scenari ammissibili con Δ ≥ 0,5;
la vecchia conclusione per Δ ≥ 0,20 riguardava il riferimento normale ed è ritirata.
H3 può diventare il collo di bottiglia se le due superiorità hanno effetti grandi;
non è il test vincolante in ogni scenario.

### 7.2 Costo della scelta e regola di risorse **[A approvata]**

La tabella conserva il **confronto storico** di §8.8: stime arrotondate a R=1,
non il conteggio completo corrente né un'autorizzazione di esecuzione.

| | 6 run (48 cluster), storico | 8 run (64 cluster), confermato |
| --- | ---: | ---: |
| Chiamate stimate storiche, con retry (§8.8) | ~2.853 | ~3.555 |
| Tetto storico, sostituito da A per D2=8 | 3.000 | 3.700 |
| Differenza sui totali storici con retry | — | **+702 chiamate, +24,6 %** |
| Run di test da simulare (8 fault × n + n Normal) | 54 | 72 |
| Run OOD | 6 | 6 |
| Generazione del lotto test primario | 54 run | 72 run: **18 simulazioni in più** |

Dalle stime arrotondate: 3.555 − 2.853 = **702** (24,6 %); prima del retry,
3.232 − 2.594 = **638**. Il +590 e il 3.500 ancora nel piano generale sono refusi
da allineare serialmente, non valori derivati. I costi e i tetti delle revisioni
precedenti restano tracciati nella storia; **3.700 non è più il tetto vigente**.

**Regola A approvata da Luca.** La pianificazione usa un conteggio completo delle
richieste per blocco e modello e il tempo misurato nel pilot della configurazione
effettiva. R=3 si attiva esclusivamente con la divergenza già definita in §10–11.
Il ramo è eseguibile solo se compatibile con la finestra operativa del piano,
incluso il margine temporale del 20%; la finestra non si estende automaticamente.
Se non fattibile, sospensione organizzativa e decisione dell'autore, senza riduzione
automatica del disegno o fallimento scientifico. Restano hard stop pilot 200,
riserva unica, retry ammessi e tutti gli altri requisiti di GO di §11.

L'allegato contabile [BUDGET_RISORSE_REV10.md](BUDGET_RISORSE_REV10.md), parte di
questa revisione, distingue R studio da R E5=1, audit aggiuntivo solo a R=1,
canary per giorno, produzione e riuso di librerie/FULL, pilot e retry. Con D2=8:

| Misura sul consumer | R=1 | R=3 |
| --- | ---: | ---: |
| Nucleo, incluse tre condizioni e Normal | 1.728 | 5.184 |
| Producer-swap: sola misura | 224 | 672 |
| Ablation B-senza-LF | 148 | 444 |
| OOD | 144 | 432 |
| **Somma delle quattro misure** | **2.244** | **6.732** |

Il totale completo è `2244R + 2k·1[R=1] + 16S + 8U_nonriusato + 10d
+ G_P + G_A + P_tot + X + Q`, con parametri definiti nell'allegato; **5.184 è il
solo nucleo**, non il totale. k≈173 è il campione audit del 10% da selezionare
in 03.10; a R=3 non si ricontano ripetizioni già previste. Gli scenari dell'allegato
non fissano mappa E5, riusi, numero effettivo di retry o giorni e non attestano T5.

La dichiarazione del referente «non hai limiti di utilizzo in token» non garantisce
richieste, velocità, concorrenza o disponibilità temporale illimitati. Il candidato
comunicato `qwen3.8-27b` (contesto 262144, output massimo 32768) non identifica da
solo pesi, revisione o quantizzazione e non prova disponibilità del 2.4T-A95B.
La revisione FP8 osservata sul vecchio server resta evidenza separata; D9 non è
scelta da questo documento. Tempi, calendario e fattibilità restano da misurare.

### 7.3 Decisione **[scelta di progetto confermata]: 8 run per fault, 64 cluster**

1. H3 è il test che decide se il metodo è pubblicabile come «conserva ciò che l'agente sapeva»:
   passare da 48 a 64 cluster porta la potenza a *m* = 0,125 da 0,86 a 0,94 (d = 0,10) e da 0,61 a
   0,72 (d = 0,20), e il margine minimo rilevabile da 0,113 a 0,098: con 64 cluster *m* = 0,125 sta
   sopra l'MDE **normale** soltanto a d = 0,10 in entrambe le numerosità. A d = 0,20
   resta sotto 0,139 anche con 64 cluster. La potenza simulata di Tango è rispettivamente
   0,77 → 0,86 (d = 0,10) e 0,58 → 0,70 (d = 0,20): gli 8 run migliorano la potenza,
   ma non garantiscono l'80 % su tutta la griglia;
2. il bordo del margine è **osservabile** in entrambi i casi (6/48, 8/64), ma la granularità di
   un caso scende da 2,1 a 1,6 punti;
3. il costo stimato cresce di 702 chiamate con retry (+24,6 %) e di 18 simulazioni di test;
   il rispetto della finestra richiede pianificazione della generazione, oltre alla disponibilità del modello;
4. gli strati di reporting guadagnano: H = {F3, F15} passa da 12 a 16 cluster, e la stima
   per-fault ha passo 1/8 invece di 1/6, che è anche il passo con cui E5-C3 (§8.12, statuto
   descrittivo) leggerà IDV(13) rispetto a Δ ≥ 0,10.

Contro: 18 simulazioni in più (72 contro 54) nel lotto 03.11, sullo stesso generatore che ha
prodotto 40 run di sviluppo in un batch; e più cluster **non** riducono la componente non stimata da
R=1 (§8.7), che resta un limite dichiarato in entrambi i casi.

La colonna a 6 run resta come confronto storico della risoluzione, non come alternativa ancora
aperta. Il disegno primario comprende **64 run fault e 8 run Normal**, per 72 run primari; i sei
run OOD restano separati dalle ipotesi confermative.

### 7.4 Run di scorta e cluster mancanti **[scelta di progetto]**

Vincolo verso 03.11: si generano **undici run di scorta** nello stesso lotto — uno per ciascuno
degli otto fault D1, uno per Normal e uno per ciascuno dei due OOD —
con identificativo sigillato e stream separato, che entra nell'analisi **solo** se un run primario
è dichiarato tecnicamente non valido da un controllo pre-specificato (run incompleto, trip,
manifest non conforme) **prima di qualunque chiamata al modello** su quel run. Dopo la prima
chiamata nessuna sostituzione: un cluster perso per errore tecnico dell'harness viene analizzato
con i cluster disponibili e il conteggio riportato. Nessun run viene generato o sostituito dopo
aver visto un risultato. Le scorte sostituiscono run primari; non aggiungono osservazioni né
cluster. I sostituti OOD cambiano invece il fault e restano soggetti alle proprie verifiche.

---

## 8. Test fuori catalogo (decisione 3 di §0.1, S13)

### 8.1 Lettura di «meccanicamente distinto» **[scelta di progetto]**

Il piano lo definisce per esempio e per esclusione: F2 non è distinto da F1 perché sono entrambi
uno step sul flusso 4, e un agente che confonde i due «non sta sbagliando in modo interessante»;
`PROPOSTA_OOD_D11.md` mostra che una lettura per tipo di meccanismo escluderebbe tutto
IDV(1)–IDV(15). Lettura adottata, sulla sola tabella 8 di Downs & Vogel come trascritta nel
registro dei criteri §2:

> Un fault candidato è **meccanicamente distinto** da un fault in catalogo se differisce per
> **variabile perturbata** e, quando condivide con esso il **flusso o l'apparato**, differisce anche
> per **tipo di meccanismo**. È distinto dal catalogo se lo è da ciascuno degli otto.

È la lettura minima che riproduce il controesempio del piano (F2/F1: stesso flusso, stesso
meccanismo, escluso) e che non rende vuoto l'insieme. Applicata ai sette candidati fuori catalogo; F9 è escluso dal vincolo sul gruppo H:

| Candidato | Contro chi condivide qualcosa | Esito |
| ---: | --- | --- |
| F9 | gruppo H escluso dal vincolo OOD del piano | escluso prima del confronto meccanico |
| **F6** | solo il tipo step, su flusso 1 non in catalogo | distinto |
| F7 | flusso 4 **e** step con F1/F2 | **non** distinto: è il caso del controesempio |
| **F4** | circuito acqua reattore con F14, ma step contro sticking | distinto |
| F11 | circuito acqua reattore con F14, random contro sticking | distinto |
| F5 | circuito acqua condensatore con F15, step contro sticking | distinto |
| F12 | circuito acqua condensatore con F15, random contro sticking | distinto |

### 8.2 I due fault **[scelta di progetto confermata condizionatamente]: F6 e F4**

- **F6** — perdita dell'alimentazione A, flusso 1, step: l'unico candidato distinto da tutti gli 8
  sia per variabile sia per apparato, senza bisogno della clausola sul meccanismo. La condizione
  bibliografica numerica è soddisfatta entro il perimetro PHM 2023: FDR **DAE 100%, PCA–T² 99%,
  PCA–SPE 100%**. FDR significa *fault detection rate*, non accuratezza diagnostica né false
  discovery rate; non prova generabilità o prestazione FoT;
- **F4** — temperatura dell'acqua di raffreddamento del reattore, step: l'unico fra i quattro
  candidati «di circuito» con rilevabilità già riverificata nel pacchetto (PHM 2023: DAE/T²/SPE
  **100/18/100%**; §12.1 lo dichiara «candidato ordinario», fuori da H). La condivisione del
  circuito con F14 è dichiarata come limite e come **domanda della sonda**: se le attribuzioni
  errate di F4 cadono su F14 è una confusione per apparato, se cadono altrove no.

**Ordine dei sostituti**, confermato e congelato prima del primo run di test, usato solo per un impedimento tecnico pre-specificato
(run non generabile o trip prima della finestra di osservazione, accertati in 03.11 prima di ogni
chiamata) o per l'assenza di un numero di rilevabilità verificabile: per F6 → **F5**, poi F12; per
F4 → **F11**, poi F5. Nessuna sostituzione dopo una chiamata al modello. Nessun sostituto è
utilizzabile senza la propria verifica di rilevabilità e ammissibilità; se entrambe le catene
arrivassero a F5, F5 non può essere contato due volte e serve una decisione esplicita. I due OOD
devono restare distinti.

⚠️ **Condizioni tecniche residue da verificare in §8 e 03.11, dopo il congelamento e prima delle chiamate sui test (§16, B approvata).** IDV(6) è documentato in Downs & Vogel come il
disturbo più severo per il processo; se lo schema di controllo del simulatore lo gestisce senza
arresto nella finestra usata da 03.3 (40 h post-innesco) è una verifica tecnica del generatore, non
una decisione di disegno. Restano da verificare generabilità, assenza di trip e tutti i requisiti
di ammissibilità; soltanto allora F6/F4 diventano eseguibili. Se F6 non è generabile, si valuta il
primo sostituto secondo la catena, senza promozione automatica.

**Controlli tecnici, non selezione su esiti.** Candidati, criteri e catene sono
congelati prima dei run; la 03.11 ne verifica l'eseguibilità senza usare prestazioni
diagnostiche, separabilità o risultati dei modelli per scegliere i fault. Ogni
sostituto deve superare le proprie verifiche; un caso non risolto dalle regole
richiede sospensione e decisione esplicita, senza modifiche silenziose del piano.

**Provenienza e limite bibliografico.** L'addendum
`/Users/luker/fot-tep-letteratura-fase03/docs/lit_review/VERIFICA_RILEVABILITA_IDV6_IDV4_FASE03.md`
e il verbale indipendente OK con SHA-256
`551f7da9de20096f3a21f6f9a19d2beecd4b03367bbf6cbe4d083f482637ddaf` documentano i numeri.
Yin (2012) resta limitato a metadati/abstract; il testo integrale non è stato acquisito. Il
candidato bibliografico è ancora esterno a questo branch e non viene dichiarato integrato in
`main`. La discrepanza F9–SPE è **5,6% nella fonte contro 6,6% nel registro congelato**: vale
l'addendum, senza modificare il registro, H={F3,F9,F15}, D1 o i criteri scientifici.

### 8.3 Run e chiamate **[piano]**

2 fault × 3 run × 8 agenti × 3 condizioni = **144 chiamate**; 6 run OOD da generare in 03.11 con
seed disgiunti dai run di sviluppo e di test. Per gli OOD tutti gli 8 agenti sono «unseen» per
costruzione; ricevono in B-LF ed E-LF gli stessi 14 insight dei casi in catalogo.

### 8.4 Analisi di astensione **[scelta di progetto]**, tutta descrittiva

Sui 48 esiti per condizione (6 run × 8 agenti), cluster = run OOD (6 cluster, troppo pochi per un
bootstrap informativo: si riportano conteggi grezzi e intervalli di Clopper–Pearson sulle 48
osservazioni, dichiarando che le 8 osservazioni dello stesso run non sono indipendenti e che
l'esattezza binomiale non si trasferisce automaticamente a risposte correlate o probabilità
eterogenee):

1. **tasso di astensione OOD** per condizione (numero 2 su P4) — per un fault fuori catalogo
   l'astensione è la risposta corretta;
2. **comparatore in-catalogo**: tasso di astensione della stessa condizione su P1 (numero 2), e la
   differenza OOD − in-catalogo. È la misura della discriminazione: astenersi di più fuori catalogo
   che dentro è riconoscimento di novità, astenersi allo stesso modo è astensione generica;
3. **destinazione delle attribuzioni errate**: distribuzione delle risposte non astenute sulle 9
   etichette, separando (a) «Normal», che è un fault mancato, da (b) un fault in catalogo, e
   annotando per F4 la quota su F14 e per F6 la quota su F1/F2/F3;
4. il contrasto **B-LF − A** e **B-LF − E-LF** sul tasso di astensione OOD, con la lettura: gli
   insight corretti alzano, abbassano o non toccano l'astensione fuori catalogo, e se lo fanno per
   informazione o per contesto.

Limite dichiarato **[piano]**: 6 eventi OOD sono una dimostrazione di esistenza, non una
caratterizzazione open-set; nel paper è una *prima sonda*, G6 resta parzialmente aperta. Quadro di
riferimento: §14.2 Heddoub et al. 2026 (open-set con garanzie per classe) e FaultExplainer (§14.2,
§14.5), che avverte che senza il meccanismo nelle feature i modelli costruiscono catene causali
plausibili e sbagliate invece di astenersi: è esattamente ciò che la voce 3 misura.

**Condizione di validità (T11)**: vedi §11.

---

## 9. D11: coppie confondibili e metrica dell'ablation local-first

### 9.1 Coppie **[scelta di progetto confermata]: {F1, F2} e {F14, F15}**

Criterio del piano: variabile perturbata o meccanismo condivisi secondo Downs & Vogel, dichiarate
prima delle confusioni del test (§8.3, D11). Dalla tabella 8, le due coppie con più attributi
condivisi sono:

- **{F1, F2}** — flusso 4, step, natura compositiva (rapporto A/C contro composizione B): la
  confusione «ragionevole» che il piano stesso usa come esempio;
- **{F14, F15}** — sticking valve, stesso tipo di apparato (valvola acqua di raffreddamento),
  reattore contro condensatore; entrambe soggette alla nota Downs & Vogel su IDV(14)–(20).

Sono quattro fault distinti, come richiede il conteggio 4 × 3 × 7. Alternativa con un attributo in
meno: {F1, F2} + {F8, F10} (flusso 4 e random variation), che concentra l'ablation sul flusso 4 e
lascia fuori le valvole. La coppia {F14, F15} è preferita perché mette alla prova local-first dove la
firma di meccanismo è identica e cambia solo la sede: è il caso in cui un agente che possiede F14
ha più ragione di rivendicare un caso F15, e viceversa. F13 resta senza coppia (nessuna
condivisione strutturale) e F3 condivide solo il tipo step con flussi diversi.

### 9.2 Run **[scelta di progetto]**

Per ciascuno dei 4 fault, i **run di indice 1, 2 e 3** del lotto di test sigillato, nell'ordine degli
identificativi di 03.11; tutti i 7 agenti non proprietari; condizione B-senza-LF (stesso prompt di
B-LF senza il blocco di politica). Local-seen: tutti gli 8 fault × n run × il proprietario. Totale
8n + 84 chiamate: 132 a 6 run, 148 a 8 (§8.8).

### 9.3 Metrica **[scelta di progetto]**, descrittiva

| Quantità | Popolazione | Che cosa dice |
| --- | --- | --- |
| **δ_seen = acc(B-LF) − acc(B-senza-LF)** sul numero 1, con bootstrap a cluster (8 strati × n) e Tango come per H3 | P2 | quanto di H3 dipende dalla politica: se δ_seen è grande, la conservazione è un effetto della politica; se è nullo, del metodo |
| **δ_unseen = acc(B-LF) − acc(B-senza-LF)** sul numero 1, bootstrap con 4 strati × 3 cluster × 7 righe | P1 ristretta alle coppie | il costo di local-first sui casi in cui un agente ha ragione di rivendicare il proprio fault |
| **tasso di cattura del partner**: quota dei casi del fault X assegnati al partner Y dall'agente che possiede Y, in B-LF e in B-senza-LF | P1 ristretta, agente proprietario del partner (2 righe per cluster) | la confusione strutturale che D11 ha dichiarato, misurata prima e dopo la politica |
| astensione (numero 2) nelle due varianti | P2 e P1 ristretta | se local-first sposta errori in astensioni o viceversa |

Nessuna ipotesi: l'ablation risponde al reviewer che chiede se il numero di testa dipende da un
accorgimento di prompt, e la risposta è una stima con intervallo, riportata qualunque sia il segno.
Non si afferma che la politica renda il contrasto B − E conservativo (§8.3, nota sulla simmetria).

---

## 10. Politica R (decisione 11), audit e canary (§8.7)

### 10.1 Che cosa il piano impone

Unità statistica del gate: il **prompt**, non la chiamata; evento: **divergenza fra le ripetizioni
dello stesso prompt**; regola: nessuna divergenza nel pilot → R=1 con audit continuo; divergenze →
R=3 sull'intero studio e non-determinismo nel modello di varianza. Con 40 prompt e zero eventi il
limite della regola del tre è ≈ 7,5 %, e non dimostra determinismo. L'assenza di controlli di
temperatura e seed viene registrata ma **non** attiva R=3 da sola.

### 10.2 Decisione 11 **[scelta di progetto confermata]: non adottare la politica più conservativa**

È confermato di **non** introdurre la regola «R=3 se l'API non espone né temperatura né seed». Tre
motivi: il gate è già definito su un evento osservato, e sostituirlo con una capacità dichiarata dal
provider lo renderebbe dipendente dall'onestà dell'API invece che dai dati; l'audit a R=3 sul 10 %
e il canary sono gli strumenti che il piano già prescrive per lo stesso rischio; e il costo (R=3
sull'intero nucleo: da 1.728 a 5.184 chiamate a 8 run) richiede il conteggio completo e
la verifica temporale approvata in A (§7.2), perché la disponibilità di token non ne
dimostra la fattibilità. La componente di variabilità del modello entra nel reporting in ogni caso. L'assenza
dei controlli va scritta nei limiti, come il piano chiede.

### 10.3 Definizione operativa di «divergenza» **[scelta di progetto]**

Due ripetizioni dello stesso prompt divergono se differiscono nella coppia
(`abstain`, `predicted_label`) dopo il parsing, oppure se differiscono nella **validità**. Differenze
nel solo JSON parsato, finish reason, testo libero o byte grezzi che non cambiano coppia o validità
**non** sono divergenze ai fini del gate, ma vengono conservate e riportate. Un prompt è divergente
se almeno una delle sue ripetizioni diverge dalle altre. Gate: **0 prompt divergenti valutabili su
40 → R=1**; **≥ 1 → R=3**. Se tutte e tre le risposte di un prompt sono non valide, T6 è non
valutabile per quel prompt: non si chiama stabilità, non concede GO tecnico e le tre invalidità
restano conteggiate in T3.

### 10.4 Audit continuo a R=3 sul 10 % **[piano, con trattamento statistico proposto]**

Sottoinsieme del 10 % del nucleo (≈ 173 prompt a 8 run), congelato prima per selezione
deterministica bilanciata su fault, agenti e condizioni, eseguito a R=3 e distribuito nel tempo.
Trattamento:

- il tasso di prompt divergenti nell'audit è riportato con intervallo di Clopper–Pearson (unità =
  prompt);
- l'analisi primaria usa la **prima** ripetizione di ogni prompt, che è quella che tutti i prompt
  hanno; le ripetizioni 2 e 3 non entrano nelle stime;
- analisi di sensibilità pre-specificata: i tre contrasti ricalcolati sostituendo, per i prompt
  dell'audit, l'etichetta di maggioranza delle 3 ripetizioni;
- **nessun passaggio a R=3 a studio iniziato**: cambiare R a metà confonderebbe l'effetto del
  tempo con quello delle condizioni. Se l'audit rivela divergenze, il fatto entra nei limiti con il
  tasso stimato, e la variabilità del modello resta dichiarata come non stimata sul resto.

### 10.5 Set canary **[piano, con trattamento statistico proposto]**

10 prompt fissi, scelti in 03.10/03.13 in modo deterministico e coprendo le tre condizioni, con
output atteso congelato (coppia parsata + hash della risposta grezza); rieseguiti ogni giorno di
esecuzione. Regole:

- **variazione** = almeno un canary con coppia parsata diversa dall'attesa; l'hash grezzo è
  forense e non decide;
- un giorno con variazione è **marcato**; le chiamate di quel giorno restano nell'analisi primaria
  e sono escluse in un'analisi di sensibilità pre-specificata;
- due giorni marcati, oppure un cambio dell'ID del modello restituito dall'API, sospendono
  l'esecuzione fino a una decisione dell'autore, registrata prima di riprendere; non è un
  NO-GO retroattivo sui dati già raccolti, che vengono riportati con la marca.

---

## 11. GO/NO-GO del modello: soglie pre-specificate per la parte statistica

**[piano]** GO se e solo se tutti i requisiti bloccanti di §11 sono soddisfatti; T6 non è un NO-GO
scientifico automatico ma un passaggio al ramo R=3. **[scelta di progetto confermata]** Le soglie
seguenti vanno riportate nel `frozen_gate_config.json` di 03.13, insieme all'ordine vincolante e
alla contabilità di §11.1:

| Requisito | Quantità | Soglia confermata | Unità |
| --- | --- | --- | --- |
| T3 formato e astensione | risposte valide al primo tentativo, sulle 120 chiamate del gate (il pilot gira **senza retry**, `PREFLIGHT_03_0.md`) | **≥114/120** valide; sotto questa soglia è NO-GO. Almeno una risposta `abstain = true` con `predicted_label = null` parsata correttamente in ciascuna condizione, anche se prodotta dal prompt di prova dedicato. Le invalidità, incluse quelle di trasporto, restano nel denominatore | chiamata |
| T4 reasoning budget | troncamenti al budget scelto | 0 su 120 | chiamata |
| T6 stabilità | prompt divergenti (§10.3) | 0 su 40 prompt valutabili → R=1; ≥1 → R=3; tre risposte non valide sullo stesso prompt rendono T6 non valutabile e impediscono il GO tecnico | prompt |
| T9 conformità | **16 insight in 8 chiamate** del producer, validati al primo tentativo | **16/16 insight validi**; un difetto diagnosticato delle classi 1–4 può attivare una sola remediation secondo §11.1. Nella ripetizione completa qualunque insight non valido è NO-GO | insight; denominatore chiamate conservato separatamente |
| T11 validità OOD | astensioni in-catalogo nel pilot, per condizione | la sonda OOD è dichiarata **a priori informativa** se in A compare almeno un'astensione sui prompt local-unseen del gate; altrimenti si esegue comunque e si riporta come **esplorativa con validità non stabilita** | prompt |
| T5 latenza | conteggio completo per blocco/modello e tempi misurati nel pilot della configurazione effettiva (§7.2) | compatibile con la finestra operativa del piano e margine temporale del 20%; se non fattibile, sospensione organizzativa e decisione autore; nessuna estensione automatica della finestra | richieste e tempo |

Non bloccanti per il GO ma da registrare: capacità di temperatura e seed dell'API (T10), con la
regola interpretativa di §10.2.

### 11.1 Ordine, remediation e riserva del pilot **[scelta di progetto confermata]**

Ordine obbligatorio: **conformità producer → eventuale remediation → sonda budget → gate 40×3**.
Il template risultante dalla conformità/remediation entra nella sonda; la sonda congela la
configurazione usata dall'unico gate successivo. Se il gate è già iniziato, la remediation non è
ammissibile.

Una sola remediation è ammessa, esclusivamente sul **prompt del producer**, per difetti
diagnosticati strutturali, di identificatori, cap o leakage. Schema, validatore, regole di leakage
e campi fissi restano invariati. Prima dell'intervento si conservano risposta grezza, hash,
prompt, fingerprint e tutti gli errori tipizzati. L'artefatto `REMEDIATION_T9_001.md` registra
evento, diagnosi e diff concreto; serve una **nuova autorizzazione scritta dell'autore sul diff**.
L'approvazione di questo disegno non autorizza in anticipo qualunque modifica futura.

Dopo il nuovo template congelato si ripetono **tutte le stesse otto chiamate/casi**, non solo
quella fallita. Gli output iniziali sono conservati come evidenza ma esclusi dalle librerie.
Qualunque insight non valido nella ripetizione completa è NO-GO; non esiste una seconda
remediation. Un timeout senza stato di errore/connessione caduta e log vLLM che provi zero token
è un guasto tecnico irrisolto: non è correggibile col prompt e non viene riclassificato.
Un errore di trasporto con tale prova non conta per T9 e la chiamata di conformità viene ripetuta
dalla riserva finché tutte e otto sono valutabili; se la riserva non basta, non si dichiara PASS.

La riserva è unica: **8 × remediation + trasporto ≤15**, con remediation∈{0,1}. Ogni richiesta
inviata consuma il contatore; cambiar template, directory, esecuzione o producer non lo azzera.
Finché si preserva la possibilità di remediation, la sua quota di 8 lascia **7 richieste residue**
per il trasporto documentato cumulativo. Senza remediation la formula consente fino a 15 richieste
di solo trasporto nella conformità, ma dopo l'ottava la remediation non sarebbe più finanziabile.
Le 8 chiamate del producer alternativo restano accantonate e non
finanziano retry. Nessun retry automatico.

La sonda budget può essere ripetuta soltanto per trasporto documentato con prova di zero token,
ripetendo **l'intera tripletta** e consumando le richieste dalla stessa riserva; niente triplette
parziali. Con tutte le 7 richieste disponibili sono possibili al massimo due triplette complete.
Nel gate non è ammessa alcuna ripetizione per trasporto: le invalidità entrano in T3 e nella
regola T6 sopra.

Contabilità ricalcolata dalla configurazione: senza remediation, 8 conformità + 3–9 sonda + 120
gate = **131–137**, oppure **139–145** includendo il producer alternativo. Con remediation completa:
**139–145 / 147–153**. Consumando anche tutte le 7 richieste residue di trasporto, i massimi sono
**152 senza / 160 con producer alternativo**. Il limite **200** è un hard stop cumulativo del
pilot, non una disponibilità di altre 40 chiamate e non autorizza a riavviare un pilot azzerando i
contatori.

Se T6 attiva R=3, si applica la **regola organizzativa A già approvata** (§7.2):
conteggio completo e verifica temporale misurata, incluso il margine 20%, oltre agli
altri requisiti di GO. Il solo nucleo costa **5.184 chiamate**, non il totale. Se il
ramo non è fattibile, sospensione organizzativa e decisione dell'autore; nessuna
riduzione automatica del disegno e nessun NO-GO scientifico automatico. L'approvazione
della regola non attesta la fattibilità né sostituisce la firma materiale.

---

## 12. Reporting stratificato obbligatorio

**[piano]** Accuratezza per i 4 fault di continuità, per i 4 nuovi e aggregata. **[scelta di
progetto]** il formato: per ogni condizione (A, B-LF, E-LF) e per ciascuna delle righe seguenti, i
tre numeri (§3) con conteggi grezzi (corretti / astenuti / non validi / totale), l'intervallo
bootstrap al 95 % dove il numero di cluster è ≥ 12, e i soli conteggi altrove:

- P1 aggregata; continuità; nuovi; H; O; per singolo fault (8 righe, n cluster ciascuna);
- P2 aggregata; continuità; nuovi; H; O;
- P2 per **agente/fault**: casi guadagnati (A errato, B-LF corretto), persi (A corretto,
  B-LF errato) e saldo `guadagnati − persi`; segnalare ogni saldo **≤−2 su 8**. È reporting
  descrittivo, non gate, test individuale o garanzia per agente;
- P3 Normal: accuratezza, tasso di falsi fault (risposte con un'etichetta di fault), astensione;
- i tre contrasti Δ₁, Δ₂, Δ₃ aggregati **e** per strato continuità/nuovi e H/O, con la nota che solo
  gli aggregati sono confermativi;
- matrici di confusione 9 × 10 (9 etichette vere incluse Normal × 9 predette + astensione) per
  condizione, su P1 ∪ P2 ∪ P3;
- P4 e P5 secondo §8.4 e §9.3.

Il paper riporta le righe di continuità e nuovi accanto all'aggregato, così il lettore vede se il
numero principale dipende dal sottoinsieme che il primo studio aveva già visto.

---

## 13. Analisi descrittive, dichiarate tali

Tutte pre-specificate qui, nessuna confermativa:

| Analisi | Fonte nel piano | Forma |
| --- | --- | --- |
| Terzo numero (accuratezza sui non astenuti) | §8.5 | stima per condizione e strato |
| Sonda OOD | §8.6 | §8.4 |
| Ablation local-first | §8.3, D11 | §9.3 |
| Braccio producer-swap | §8.4 | acc(B-LF, producer alternativo) − acc(B-LF, producer principale) su P1, bootstrap a cluster; parità strutturale degli insight riportata (S19) |
| E5, ablazione dei descrittori | §8.12 | statuto descrittivo già deciso lì; D2 fissa la granularità (1/n per IDV(13)); E5-C3 resta di §8.12 e non viene chiuso qui |
| Baseline numerica, pavimento locale, FedAvg, soffitto | §6.7, §9.3, D8 | accuratezza sugli stessi casi di test con intervallo bootstrap sui cluster; nessun test contro B-LF |
| Audit R=3 e canary | §8.7 | §10.4, §10.5 |
| Sensibilità H3 a α=0,025 | decisione A2 dell'autore | stesso score di Tango e stessa popolazione dell'esito primario; riportata separatamente, non sostitutiva; A2-bis non adottato |
| Guadagnati/persi/saldo per agente e fault | decisione A3 dell'autore | conteggi grezzi su 8 casi; saldo ≤−2 segnalato senza trasformarlo in gate o controllo confermativo |
| Normal e falsi fault | §6.9 | §12 |
| Token per prompt e per insight, per producer e condizione | §8.7 | medie e distribuzioni, per separare informazione da lunghezza |

Analisi post-hoc: ammesse solo se etichettate come tali nel paper, senza intervalli confermativi,
e mai per rivedere *m*, gli strati, le coppie o gli OOD (pre-impegno di §8.12, esteso qui a tutto il
piano statistico).

---

## 14. Threats

1. **R=1**: la variabilità delle risposte del modello alla stessa richiesta non è stimata (§8.7);
   l'audit al 10 % la sonda, non la misura sul resto. Va scritto nei limiti.
2. **Correlazione intra-cluster ignota**: le 7 righe di un run condividono l'evidence; la potenza di
   H1/H2 dipende da ρ (§7.1). Il ricampionamento preserva la dipendenza intra-cluster; la copertura percentile
   resta approssimata con pochi cluster e non è garantita da questo solo accorgimento.
3. **Pochi cluster per H3 e bassa discordanza attesa**: il percentile bootstrap è anti-conservativo
   (§4.3); per questo la decisione è il test score, e l'esito «zero coppie discordanti» va
   dichiarato come tale.
   Per H1/H2 il test di Hoeffding è valido per costruzione ma conservativo: effetti fra 0,1 e
   0,3 hanno potenza inferiore all'80 % nella griglia a 48–64 cluster (§7.1); la possibilità
   di rifiuto in un campione resta determinata dalla media osservata. È il
   prezzo di una garanzia che non dipende dalla forma della distribuzione.
4. **Astensione contata come errore**: penalizza la condizione che si astiene di più (A, dove il
   piano riporta 14/36 astensioni nel primo studio). È voluto — l'astensione su un fault in catalogo
   è una diagnosi mancata — ma il numero 2 va sempre accanto al numero 1.
5. **Local-first**: può spostare errori e astensioni in entrambe le direzioni; l'ablation misura, non
   neutralizza (§8.3).
6. **Sonda OOD con 6 eventi**: esistenza, non caratterizzazione; F4 condivide il circuito con F14 e la
   quota di attribuzioni a F14 va letta come limite dichiarato.
7. **Un solo fault per il drift (F13)** e 2 per H: gli strati per-fault hanno n cluster e passo 1/n.
8. **Cambio di modello durante l'esecuzione**: il canary lo rileva, non lo previene; le analisi di
   sensibilità per giorno marcato sono l'unica difesa.
9. **Stesso simulatore per sviluppo e test**: i seed sono disgiunti e dimostrabili (S3), ma la
   distribuzione è la stessa; non è una prova di generalizzazione a impianti diversi.
10. **Trasferibilità della difficoltà documentata**: lo strato H viene da tassi di rilevazione PCA,
    non da diagnosi verbalizzate (§12.3); serve a stratificare e dichiarare, non a prevedere.
11. **Molteplicità descrittiva**: decine di stime; solo tre sono confermative e in sequenza fissa.
    Il paper non deve promuovere una stima descrittiva a risultato.
12. **Riferimenti metodologici esterni al corpus** (§17): il candidato è stato verificato
    indipendentemente con esito OK, ma resta esterno al branch; va integrato con la procedura §6
    di MAINTENANCE prima del congelamento definitivo.

---

## 15. Tabella delle decisioni

| Decisione | Stato revisione 10 | Decisione registrata | Fonte | Residuo |
| --- | --- | --- | --- | --- |
| **D2** — run per fault | **confermata** | **8 run, 64 cluster fault; 8 Normal primari** | decisioni autore; §7.1–7.3; `DESIGN_RESOLUTION.md` | nessuno sulla scelta; fattibilità R=3 separata |
| **OOD** — decisione 3 | **confermata condizionatamente** | lettura §8.1; **F6 + F4**; sostituti F5/F12 e F11/F5; analisi §8.4 | decisioni autore; addendum PHM e verbale bibliografico OK | generabilità, trip e ammissibilità §8/03.11; verifiche proprie dei sostituti |
| **D11** — coppie confondibili | **confermata** | **{F1, F2}, {F14, F15}**; run 1–3; metrica §9.3 | decisioni autore; tabella 8 D&V | nessuno |
| **Margine *m* / α** | **confermati** | **0,125** come massima perdita media netta; α primario 0,05; H3 a 0,025 sola sensibilità; A2-bis non adottato | decisioni autore, Allegato A; §5, §7.1 | nessuno; applicabilità Tango dichiarata come limite |
| **Gerarchia** | **confermata** | sequenza H1 → H2 → H3 a 0,05; controllo completo approssimato per Tango | decisioni autore; §4.2–4.3 | nessuno |
| **Test di H1/H2** | **confermato** | Hoeffding sulle medie di cluster indipendenti in [−1,1]; sign-flip solo supplementare | decisioni autore; Hoeffding 1963 | indipendenza effettiva da garantire operativamente |
| **T9 / T3 e remediation** | **confermati** | 16/16 insight in 8 chiamate; T3 ≥114/120; una sola remediation e riserva unica §11.1 | decisioni autore, Allegato B; preflight | autorizzazione futura sul diff concreto, se necessaria |
| **Politica R** — decisione 11 | **confermata** | coppia parsata o validità; nessun R=3 per sola assenza di controlli; audit/canary/sospensioni | decisioni autore; §10; A approvata | fattibilità misurata del ramo R=3 |
| **GO/NO-GO** — soglie | **confermate** | T3–T6, T9, T11 e ordine §11–11.1 | decisioni autore; piano §11 | esito del pilot e prerequisiti esterni |
| Seed del bootstrap | **confermato** | 20260913, 10.000 repliche, namespace approvato | decisioni autore; pattern HC | nessuno |
| Run di scorta | **confermate** | 11: 8 D1 + Normal + 2 OOD; sostituzione tecnica pre-chiamata | decisioni autore; §7.4 | identificativi/stream da congelare in 03.11 |
| Risorse — A | **approvata** | conteggio completo per blocco/modello e fattibilità temporale +20%, in sostituzione del tetto 3.700; hard stop pilot 200 invariato | approvazione addendum; §7.2, §11 | misure, D9, calendario, allineamenti esterni |
| Ordine OOD — B | **approvata** | criteri/candidati/catene prima dei run; controlli tecnici 03.11 dopo freeze e prima delle chiamate | approvazione addendum; §8, §16 | controlli tecnici e gestione esplicita dei casi non risolti |

Le approvazioni sono di **Luca**, registrate il **14 settembre 2026**. La firma materiale resta
pendente; non viene apposta per conto dell'autore e non si richiede una seconda approvazione delle
stesse scelte. Le nuove formulazioni A/B sono approvate senza modifiche nella
risposta di Luca riferita al commit `526561f`; fonte e data effettiva nel record
[APPROVAZIONE_ADDENDUM_03_8.md](APPROVAZIONE_ADDENDUM_03_8.md). I documenti preparatori
immutati di quel commit restano storici: le loro righe pending non sono lo stato corrente.

---

## 16. Congelamento del disegno e condizioni di esecuzione **[B approvata]**

### 16.1 Prima del primo run di test: congelamento statistico

1. Firma materiale dell'autore, ancora pendente, distinta dalle approvazioni in conversazione.
2. Candidati OOD F6/F4, criteri tecnici, catene F6→F5→F12 e F4→F11→F5, regole di
   sostituzione, campioni, undici scorte e tutte le scelte statistiche fissati in
   questa revisione; nessuna scelta su prestazioni, separabilità o risultati dei modelli.
3. Regola organizzativa A approvata e recepita (§7.2); la verifica misurata della
   fattibilità è condizione di esecuzione e non viene dichiarata soddisfatta dalla regola.
4. Integrazione bibliografica nel ramo destinato a `main`, con verbale e impronte;
   il candidato bibliografico rimane esterno a questo branch fino all'acquisizione seriale.
5. Allineamenti delle **regole** nel piano generale e in APERTURA, e specifica del
   delta 03.10 coerente: l'implementazione operativa e i suoi test sono obbligatori
   prima del pilot, distinti dal congelamento statistico (punto 16.2).
6. **Nuova verifica indipendente della revisione 10**, ancora pending. L'OK rev. 9
   resta storico e non approva questa modifica del protocollo.
7. Dopo i requisiti precedenti, documentazione e commit finali coordinati, commit
   raggiungibile da `origin/main`, manifest e tag secondo MAINTENANCE §8.4, **prima
   del primo run di test**. Fino ad allora `freeze_effective=false`, `freeze_tag=null`.

### 16.2 Prima del pilot e delle chiamate sui test: condizioni operative conservate

Il pilot sui dati di sviluppo richiede 03.6/03.7/03.12, input e schema congelati,
identità/configurazione e capienza, e implementazione verificata delle regole
03.8 nella 03.10. Ordine, hard stop e riserva di §11 restano obbligatori; il pilot
non attende risultati diagnostici o tecnici del lotto di test OOD. T5 si valuta
con le misure della configurazione effettiva prima di autorizzare lo studio;
A non sceglie D9 e non autorizza chiamate da questa finestra.

**Dopo il congelamento statistico, in 03.11 e prima di qualunque chiamata ai modelli
sui test**, verificare generabilità, trip nella finestra prescritta e ammissibilità
tecnica di F6/F4 e degli eventuali sostituti. I controlli sono tecnici e tracciati;
non usano prestazioni diagnostiche o separabilità per scegliere i fault. Ogni
sostituto deve superare le proprie verifiche di rilevabilità e ammissibilità;
i due OOD devono restare distinti. Le scorte sostituiscono run, non aggiungono osservazioni.

Si applicano esclusivamente impedimenti e catene pre-specificati. Un caso non
risolto dalla regola, incluse entrambe le catene su F5, impone sospensione e
**decisione esplicita dell'autore**; nessuna modifica silenziosa del piano né
sostituzione dopo le chiamate. I controlli non sono eliminati: sono condizioni
operative prima delle chiamate sui test, non condizioni da soddisfare prima
che il lotto esista. La verifica PHM di F6 non li surroga.

La sequenza è: **criteri/candidati/catene congelati → run 03.11 e controlli tecnici
tracciati → chiamate sui test dopo gli altri GO**. Viene così rimosso il ciclo
03.8→03.11→03.8 del precedente §16, per correzione del protocollo approvata in B,
non per una condizione retroattivamente chiusa dalla review rev. 9.

---

## 17. Riferimenti

**Nel corpus (`docs/letteratura.md`)** — citati per sigla:

- §14.3 Field & Welsh (2007), *Bootstrapping Clustered Data* — fondamento del bootstrap appaiato per
  cluster (§6);
- §14.3 Holm (1979) — correzione sequenziale usata nel primo studio; qui sostituita dalla sequenza
  fissa, che non richiede aggiustamento dei livelli;
- §14.3 Wang et al. (2019), *Characterizing and Avoiding Negative Transfer* — il quadro in cui
  leggere H3 e l'ablation local-first;
- §14.3 Downs & Vogel (1993) — tabella 8, unica fonte per «meccanicamente distinto» e per le coppie;
- §14.2 Heddoub et al. (2026), open-set con garanzie per classe — quadro per la sonda OOD;
- §14.2 / §14.5 FaultExplainer (Khan et al., 2025) — avvertimento sulle catene causali plausibili e
  sbagliate, misurate dalla voce 3 di §8.4;
- §14.2 Vovk (2012/2013) e Bates et al. (2023) — la parte di FAR già congelata in 03.5, citata come
  vincolo (§1);
- §14.1 Khan et al. (2026) — intervalli bootstrap e calibrazione su TEP, come prassi attesa.

**Otto riferimenti metodologici del piano** — verificati dal candidato bibliografico e dal suo
verbale indipendente OK, ma ancora **esterni al branch corrente e non dichiarati integrati in
`main`**. I limiti di accesso a Maurer, Westfall e Kish restano quelli documentati:

- Tango, T. (1998), *Equivalence test and confidence interval for the difference in proportions for
  the paired-sample design*, Statistics in Medicine — test score usato per H3;
- Maurer, W., Hothorn, L. & Lehmacher, W. (1995), *Multiple comparisons in drug clinical trials and
  preclinical assays: a-priori ordered hypotheses* — procedura a sequenza fissa (gatekeeping);
- Westfall, P.H. & Krishen, A. (2001), *Optimally weighted, fixed sequence and gatekeeper multiple
  testing procedures*, Journal of Statistical Planning and Inference;
- Clopper, C.J. & Pearson, E.S. (1934), *The use of confidence or fiducial limits illustrated in the
  case of the binomial*, Biometrika — intervalli esatti per OOD, audit e canary;
- Kish, L. (1965), *Survey Sampling* — effetto di disegno 1 + (k − 1)ρ usato nell'analitico;
- Hoeffding, W. (1963), *Probability inequalities for sums of bounded random variables*, Journal
  of the American Statistical Association — il test di H1/H2 (§4.1, §4.3);
- Bahadur, R.R. & Savage, L.J. (1956), *The nonexistence of certain statistical procedures in
  nonparametric problems*, Annals of Mathematical Statistics — citato per dire che **non** si
  applica: la sua classe richiede la ricchezza di ogni media reale, che manca sotto un limite
  comune [−1,1]; non perché ogni distribuzione della classe debba avere code illimitate (§4.1);
- ICH E9 (1998), *Statistical Principles for Clinical Trials* — convenzione sul livello unilaterale
  per la non inferiorità, citata solo per la scelta fra 0,05 e 0,025.

McMahan et al. (2017) è il riferimento aggiuntivo verificato per il lavoro bibliografico/FedAvg,
non un nono riferimento metodologico esterno di questa sezione. Yin (2012) resta disponibile solo
come metadati/abstract: nessuna tabella numerica non letta gli viene attribuita.

**Letti per questa sotto-fase**: piano §0.1, §8.1, §8.3, §8.5–8.8, §8.12 (solo E5-C), §9.3, §11, §12.1–12.4,
D1, D2, D7, D11; `CATALOG_FREEZE.json`; `PROPOSTA_OOD_D11.md`; registro dei criteri §2;
`letteratura.md` §14.2 (voci citate), §14.3; `phase_b/evaluation/bootstrap.py` e `metrics.py`
(definizioni); walkthrough v2 §6.5 (sola definizione del bootstrap); `DECISIONE_calibrazione_soglie_fase_B.md`
(intestazione e numeri del disegno); `PREFLIGHT_03_0.md` (decisione 11);
`APERTURA_SOTTOFASI_FASE03.md`; `protocol.py` (vincoli su agenti e label space); `MAINTENANCE.md` §1, §2, §8;
`Prompt_LLM.md`, `Fase_LLM.md`. Per la revisione 8: copia byte-identica delle decisioni autore;
addendum IDV(6)/IDV(4) e verbale bibliografico indipendente OK esterni; piano generale, registro
criteri, preflight, `pilot_preflight.json` e `APERTURA_SOTTOFASI_FASE03.md` consultati
puntualmente per gli allineamenti rinviati. Per la revisione 9: verbale indipendente rev. 8 NON OK
e manifest rev. 7 letto dalla storia Git. Nessun risultato sperimentale sigillato aperto.
