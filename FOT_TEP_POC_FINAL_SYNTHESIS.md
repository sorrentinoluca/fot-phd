# FOT_TEP_POC_FINAL_SYNTHESIS.md

Sintesi conclusiva del proof-of-concept "Federation over Text su verbalizzazioni
diagnostiche del Tennessee Eastman Process". Documento di chiusura: raccoglie
l'intero arco Fase A → Fase B, con la gerarchia delle claim definitiva.

**Fonte:** repository `sorrentinoluca/fot-phd`, branch `phase-b-fot`, commit
`45ec4eed65b263a5803ced7d01064c4672e81e86`. Ogni numero è stato ricalcolato
indipendentemente dai record grezzi versionati, non ripreso da report intermedi.

---

## 1. Cosa è stato costruito e dimostrato, in una pagina

Il progetto ha testato se **Federation over Text (FoT)** — la condivisione di
insight testuali tra agenti invece di gradienti o pesi — trasferisca conoscenza
diagnostica utile in un dominio a serie temporali (diagnosi guasti industriali),
usando il Tennessee Eastman Process come banco a verità nota, come passo verso
l'obiettivo di lungo periodo sul fotovoltaico.

L'arco si è svolto in due fasi con un confine netto:

- **Fase A** ha costruito e congelato un *verbalizzatore*: trasforma serie
  temporali numeriche in testo diagnostico neutrale, senza classificare. Validata
  su held-out con separabilità descrittiva delle firme (F1/F10 stabili, F13
  intermedio, F8 più variabile).
- **Fase B** ha usato quel testo per far ragionare 4 agenti con conoscenza locale
  non-IID e ha misurato se la federazione di insight aiuta a diagnosticare classi
  mai viste localmente.

**Il risultato in una riga:** su un proof-of-concept a piccola scala, la
federazione di insight testuali corretti ha permesso agli agenti di diagnosticare
guasti mai osservati localmente, e un controllo di specificità pre-registrato
supporta fortemente l'interpretazione che il beneficio dipenda dalla correttezza
dell'informazione trasferita, non dal semplice volume di testo.

---

## 2. Risultati Fase B (numeri verificati a `45ec4ee`)

Primary unseen: 36 istanze appaiate, 12 fault-run fisici indipendenti.

| Condizione | Unseen accuracy | Descrizione |
|---|---|---|
| A — isolated | **0/36 = 0.000** | solo conoscenza locale |
| B — FoT | **31/36 = 0.861** | + insight peer corretti |
| E — corrupted | **3/36 = 0.083** | + insight peer con etichette permutate |

- **Metrica primaria pre-registrata — B−A = +0.861** (H1). Positiva per 4/4
  agenti (+1.00, +1.00, +0.667, +0.778). helped=31, harmed=0.
- **Contrasto di specificità pre-registrato — B−E = +0.778** (H3, criterio C4).
- I quattro criteri pre-registrati C1–C4 risultano PASS.

Seen sanity check (dai medesimi record frozen): A su fault locale = 12/12, A su
Normale = 12/12. L'agente isolato è pienamente competente quando ha
l'informazione; fallisce sull'unseen per assenza di informazione, non per
malfunzionamento.

---

## 3. Gerarchia delle claim (definitiva)

Questa gerarchia è vincolante per ogni uso successivo (paper, presentazioni).

**Primaria (H1): B−A = +0.861.** È la metrica primaria pre-registrata e resta
tale. Va sempre accompagnata dal contesto del §4 (floor strutturale di A), che la
caratterizza senza declassarla.

**Specificità / evidenza meccanicistica (H3): B−E = +0.778.** È il contrasto di
specificità pre-registrato. È l'evidenza interpretativamente **più diagnostica
del meccanismo**: poiché B ed E differiscono esclusivamente nel campo
`pseudolabel` degli insight (verificato nel codice — nessun altro campo, stessa
lunghezza, stesso volume), la differenza isola il trasferimento di informazione
*corretta* come causa. **B−E non va chiamata "metrica primaria"**: è il contrasto
di specificità, con ruolo distinto e complementare.

La formulazione canonica: *"La metrica primaria B−A mostra +0.861 sui casi
localmente non visti; il contrasto di specificità B−E = +0.778 supporta
l'interpretazione che il beneficio dipenda dalla correttezza dell'informazione
trasferita e non dal volume di testo."*

---

## 4. Caratterizzazione del floor di A (analisi descrittiva post-hoc)

Il baseline isolato opera vicino a un **floor strutturale** sulle classi unseen.
Descrizione, senza ripunteggio (l'abstention resta *incorrect* nella primary
accuracy, come da protocollo frozen):

- A unseen aggregate: 0/36 corretti;
- di cui **14/36 astensioni** e 22/36 tentativi di predizione;
- corretti tra i non-astenuti: **0/22**;
- a livello di ripetizione (108 tentativi): 78 contengono un reasoning che
  riconosce l'anomalia ma dichiara di non poterla mappare a un'etichetta; zero
  predizioni falsamente "Normal".

Lettura: il floor di A combina due comportamenti coerenti con l'assenza di
conoscenza class-semantica sulle classi unseen: in **14/36** casi l'agente
astiene, riconoscendo esplicitamente la propria insufficienza informativa; nei
restanti **22/36** tenta una classificazione, ma nessuna delle predizioni
committed è corretta (**0/22**). Questa caratterizzazione descrive come A
raggiunge il floor senza modificarne il punteggio: l'abstention resta incorrect
secondo il protocollo frozen.

Implicazione sulla lettura della magnitudine: poiché A parte da un floor vicino a
zero per costruzione sulle classi unseen, la magnitudine di B−A (+0.861) va letta
come "presenza vs assenza di informazione", mentre la qualità della federazione è
catturata da B−E. Le due metriche, insieme, danno il quadro corretto.

---

## 5. Cosa NON si può affermare

- **Non** "FoT porta +86 punti di accuratezza diagnostica in generale": la
  magnitudine primaria riflette un baseline a floor strutturale.
- **Non** "FoT è privo di negative transfer": harmed=0 è conseguenza aritmetica
  del floor di A (nessun caso unseen in cui A fosse corretto da peggiorare), non
  evidenza di sicurezza del trasferimento.
- **Non** generalizzazione: 12 fault-run fisici, un simulatore, un mode, 4 fault,
  un modello LLM. È un proof-of-concept che indica una direzione.
- **Non** "il verbalizzatore classifica": la Fase A misura separabilità
  descrittiva delle firme, non accuratezza di classificazione.

---

## 6. Integrità metodologica dell'intero arco

Elementi verificabili che sostengono la credibilità del risultato:

- **Fase A congelata e verificabile:** hash SHA-256 dei file frozen corrispondenti
  ai file reali; `git diff` = 0 righe sui file di protocollo tra freeze,
  validation e test; caveat chiusi (calibrazione soglie riproducibile, injection
  time verificato sia dal sorgente sia empiricamente).
- **Held-out Fase B indipendente:** 15 casi da simulatore *parent* del commit
  dataset (S-function byte-identica, stato iniziale identico), congelati prima di
  ogni verbalizzazione o inference.
- **Protocollo Fase B pre-registrato:** pseudolabel opache, peer-only federation,
  esempi e insight deterministici da development, condizioni A/B/E,
  no-structured-JSON nel prompt, held-out access guard fail-closed.
- **Schedule counterbalanced** deciso a 0/540 inference, senza modificare il
  protocollo, con verifica del bilanciamento globale e per-agente.
- **540 inference tracciate** una per una (prompt hash, input hash, output
  grezzo, model version); metriche rigenerabili dai record.
- **Scoring frozen rispettato:** l'abstention resta incorrect; la
  caratterizzazione epistemica è descrittiva, non un ripunteggio.

---

## 7. Limiti (dichiarati)

1. **Baseline a floor strutturale** sulle classi unseen: la magnitudine primaria
   B−A va letta con questo contesto; l'evidenza meccanicistica è B−E.
2. **Campione piccolo:** 12 fault-run fisici; 36 istanze appaiate non
   indipendenti (clustering per run obbligatorio in ogni intervallo di confidenza).
3. **F8/variabilità** ereditata dalla Fase A: un errore su quella classe può
   derivare dalla firma verbalizzata debole più che dalla federazione.
4. **Pseudonimizzazione** maschera il nome, non la firma: prior knowledge del
   benchmark non del tutto eliminabile.
5. **Un solo modello LLM**, non-determinismo del provider (temperature/seed non
   esposti), mitigato da R=3 e aggregazione congelata, non eliminato.
6. **Dominio proxy:** TEP simulato, non fotovoltaico reale. La transizione
   richiederà di riprogettare l'estrazione di feature del verbalizzatore sui
   segnali PV, riusando l'impianto metodologico.

---

## 8. Conclusione

Il proof-of-concept è chiuso con esito **positivo e onestamente delimitato**. Su
scala ridotta e in un dominio proxy, la federazione di insight testuali con
provenance trasferisce informazione diagnostica genuina tra agenti non-IID: gli
agenti diagnosticano guasti mai visti localmente quando ricevono insight peer
corretti (B−A = +0.861, primaria), e il beneficio svanisce quando le etichette
degli insight vengono permutate a parità di ogni altra cosa (B−E = +0.778,
specificità). Il contributo metodologico — separazione netta verbalizzazione/
reasoning, freeze verificabile, held-out indipendente, controllo di specificità
pre-registrato — è forte quanto il risultato numerico, e ne sostiene la
credibilità.

La direzione per il seguito (fuori dallo scope di questo PoC): portare il
verbalizzatore sui segnali fotovoltaici reali, ampliare il numero di run fisici
per irrobustire l'inferenza statistica, e testare la federazione su più fault e
più modelli.

---

## Nota di coerenza col repository

Verificato a `45ec4ee`: 540 repetition + 180 aggregate records presenti; numeri
primari e di specificità ricalcolati indipendentemente (A=0/36, B=31/36, E=3/36,
B−A=+0.8611, B−E=+0.7778, helped=31, harmed=0); seen sanity check A=12/12 su
fault locale e 12/12 su Normale. La gerarchia delle claim (B−A primaria, B−E
specificità) e il trattamento dell'abstention (incorrect nel punteggio,
caratterizzata descrittivamente) riflettono la decisione di chiusura del
progetto.
