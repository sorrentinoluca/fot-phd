# E5 — decisioni A–G da prendere prima di `exp5-protocol-frozen-001`

Documento unico, come chiede il gate G1 del piano rev2. Ogni voce ha: che cosa è in gioco,
la proposta con la sua motivazione, il costo, e che cosa comporta dire di no. Le proposte
sono già codificate nei file di questa cartella: approvarle significa congelarle, cambiarle
significa rilanciare gli script con parametri diversi. Nessuna decisione qui è presa: sono
proposte all'autore.

Riferimento autorevole: piano §8.12. Dove una proposta contraddice §8.12 è detto
esplicitamente, perché richiede una **revisione dichiarata** prima del freeze.

---

## A — Riceventi

**In gioco.** §8.12 prescrive *un ricevente per run fisico*, scelto fra i sette non
proprietari, bilanciato. Il batch finale però interroga **tutti e sette** i non proprietari
per ogni caso, tre volte: FULL esiste già per ogni ricevente.

**Proposta: (a) un ricevente per run, bilanciato.** Il file `RICEVENTI_E5.json` lo realizza
con un bilanciamento esatto: ciascuno degli otto agenti riceve esattamente 8 run (ogni agente
compare una volta in ciascuno dei sette fault non suoi, più un run extra assegnato da un
abbinamento perfetto fault→agente con agente ≠ proprietario).

**Motivazione.** L'unità di analisi resta il **run fisico**: interrogare sette riceventi
invece di uno aggiunge precisione sulla stima *del ricevente*, che è un fattore di disturbo
descrittivo, non potenza sull'endpoint. Costa sette volte le chiamate per guadagnare su una
dimensione che il disegno dichiara già non eliminabile. In più (a) non richiede revisione di
§8.12.

**Costo.** (a) 96 coppie PERM + 96 OMIT = **192 chiamate** a R=1 (≈ 53 min a 16,5 s).
(b) tutti e sette: 672 + 672 = **1.344 chiamate** a R=1 (≈ 6 h), e richiede revisione
dichiarata di §8.12.

**Se si sceglie (b):** rilanciare `build_e5_assignments.py --mode all`; la tabella dei
riceventi sparisce e con essa una fonte di arbitrarietà, ma va dichiarato che le sette
osservazioni per caso **non sono indipendenti** e che l'aggregazione le media prima del
bootstrap sul run.

---

## B — Ripetizioni, e **contro quale FULL**

**In gioco.** Non è solo «quante ripetizioni fa E5». È a quale FULL si confronta ciascun
braccio. Il batch finale gira a R=3 con r1 primario e maggioranza 2 su 3 in sensibilità; il
riuso di FULL, però, riguarda per default **solo B-LF r1**. Dichiarare E5 a R=3 con
maggioranza 2/3 senza dire contro che cosa si confronta quella maggioranza lascia la
decisione incompleta: la sensibilità confronterebbe una maggioranza 2/3 di PERM con un FULL a
una sola estrazione, che è un confronto asimmetrico.

**Le opzioni sono tre, e vanno scelte esplicitamente.**

| | Primario | Sensibilità | Slot FULL da riusare | Chiamate E5 (con A(a)) |
| --- | --- | --- | --- | ---: |
| **B1** | FULL r1 vs PERM/OMIT r1 | nessuna | 64 (r1) | 192 |
| **B2 — FISSATA** | FULL r1 vs PERM/OMIT r1 | maggioranza 2/3 **in entrambi i bracci**: FULL r1-r2-r3 riusati e verificati, PERM/OMIT r1-r2-r3 | 192 (r1, r2, r3) | 576 |
| **B3** | FULL r1 vs PERM/OMIT r1 | nessuna maggioranza; le tre ripetizioni di PERM servono solo a quantificare il rumore di decoding, riportato a parte | 64 (r1) | 576 |

**Decisione: B2**, cioè R=3 con l'aggregatore del batch **e** il contratto di riuso esteso alle
tre ripetizioni di B-LF. Motivazione: il pilot ha mostrato non-determinismo, e a R=1 il
contrasto include rumore di decoding non separabile dall'effetto; con B2 l'aggregatore di E5 è
identico a quello del batch e la maggioranza è confrontata con una maggioranza, non con una
singola estrazione. Il costo non è un vincolo dichiarato di questo studio.

**Che cosa comporta B2 in concreto.** Le sei identità di `VERIFICA_FULL_BLF.md` vanno
verificate **su tutte e tre le ripetizioni**, non solo su r1: `export_full_blf.py
--repetitions 1 2 3`. Se una ripetizione di FULL manca o fallisce l'identità, quella
sensibilità cade (o si riesegue quella ripetizione), mentre il primario su r1 resta valido.

**Se si sceglie B1:** il contrasto include il rumore di decoding e va scritto nel protocollo e
nel paper, ripetuto accanto alla tabella degli effetti. È l'opzione più pulita se il riuso
delle tre ripetizioni non si vuole aprire — meglio B1 che una maggioranza contro r1.

## C — Mappa famiglia–meccanismo, S_F e controlli

**In gioco.** È la decisione più delicata: assegnare un meccanismo a ogni famiglia **a priori**,
senza guardare quali descrittori si attivano — nemmeno sui dati di sviluppo. Guardare le
attivazioni sarebbe selezione sull'esito.

**Proposta** (codificata in `family_map.json`, assegnazione da Downs & Vogel 1993 §12.4):

| Famiglia | colonna | meccanismo bersaglio | controllo | motivazione a priori |
| --- | --- | --- | --- | --- |
| level | `shift_sigma` | step (F1, F2, F3) | random variation (F8) | il gradino sposta il livello medio e lo mantiene; il controllo è un meccanismo che a priori non sposta la media |
| trend | `slope_sigma_h` | slow drift (F13) | step (F1) | la pendenza descrive la deriva; il gradino sposta il livello senza pendenza sostenuta |
| residual | `residual_std_ratio` | random variation (F8, F10) | step (F1) | la variabilità residua dopo rimozione del trend è ciò che una variazione casuale produce; il gradino è deterministico |
| diff | `diff_std_ratio` | sticking valve (F14, F15) | step (F1) | il bloccaggio/rilascio produce discontinuità campione-campione ripetute; la discontinuità del gradino è singola |

**Citazione, per il freeze.** Il meccanismo non si cita come «Downs & Vogel 1993 §12.4»:
§12.4 è la sezione *del nostro piano* che prescrive di usare quella fonte. La fonte, per
esteso: Downs, J.J. & Vogel, E.F. (1993), *A plant-wide industrial process control problem*,
Computers & Chemical Engineering 17(3), 245–255, DOI `10.1016/0098-1354(93)80018-I`,
**tabella 8, p. 250, colonna «Type»** — ed è quella colonna, e solo quella, a dare il
meccanismo: Step per IDV(1)/(2)/(3), Random variation per IDV(8)/(10), Slow drift per
IDV(13), Sticking per IDV(14)/(15). L'accoppiamento famiglia↔meccanismo è invece un
**argomento dell'autore**, non un dato della fonte, e va firmato come tale. Il tutto è
registrato in `family_map.json` → `mechanism_map_proposal.bibliographic_source`, con la nota
su p. 251 (la raccomandazione di usare IDV(14)–(20) insieme a un altro disturbo, da cui la
specifica dei run dichiara di deviare: la deviazione riguarda la generazione, non l'etichetta
di meccanismo).

**Le due righe da guardare con attenzione sono `residual` e `diff`**: non sono ovvie come
`level`→step e `trend`→drift. La motivazione è testuale e a priori (descrizione del
meccanismo nella fonte), non empirica. Se l'autore non la condivide, va cambiata **adesso**.

**Conseguenze da dichiarare.** `trend` ha S_F a **due sole classi** (F13 + F1): l'evidenza del
bersaglio viene interamente dal controllo e viceversa — perturbazione specifica fra due
classi, non corruzione rappresentativa (§8.12 lo prevede e lo accetta per `slope_sigma_h`).

**Colonne fuori dalle famiglie.** `raw_std_ratio` (dispersione complessiva) non appartiene a
nessuna famiglia ablata: non si permuta e non si omette mai. Va dichiarato che una quota del
testo resta invariata in ogni braccio.

**Grandezze derivate inter-famiglia — aggiunta rispetto a §8.12.** §8.12 nomina solo `rapid`.
Il verbalizzatore ne ha altre tre che attraversano le famiglie e che il ricalcolo tocca:
episodi di **drift coerente** e `strict_global_drift` (pendenza + spostamento), il
**transitorio di assestamento** (residual + diff) e i **valori per fase** di residual e diff.
Vanno nominate nel protocollo E5 accanto a `rapid`, con la stessa regola: ricalcolate nel
braccio, cadenti con il genitore in OMIT. (Nel testo neutrale emergono come frasi solo `rapid`
e le frasi di famiglia; le altre vivono nell'evidenza strutturata.)

---

## D — E5-C2, soglia del controllo di lunghezza

**Proposta: confermare il 5 %, con la verifica fatta sui prompt completi e non per
sottrazione.** La misura di fattibilità è eseguita (`VERIFICA_E5_C2.md`): `|Δtoken|` sul testo
è ≤ 68 token su 13.500 coppie. Il criterio però è definito sul **prompt completo**, e con un
tokenizer BPE i conteggi non sono additivi ai confini fra prefisso, blocco del caso e
suffisso: nessuna soglia sulla «parte costante» ottenuta per sottrazione è una prova. La
verifica si fa componendo i prompt dei due bracci e contandoli interi —
`verifica_e5_c2_prompt.py`, che non somma e non sottrae nulla. Due passaggi:

1. **prima del freeze**, con i prompt B-LF già resi come portanti e i testi di sviluppo:
   chiude la fattibilità;
2. **a G3**, con i testi FULL/PERM effettivamente prodotti sul lotto test: è la misura reale.

Se la verifica del passo 1 fallisce, la soglia va rivista **prima** del freeze, registrando
misura e data in §8.12. Se fallisce al passo 2, si applica l'avvertenza di confondimento: non
si rigenera nulla.

**Troncamento:** zero differenze, strutturalmente (contesto 131.072, prompt massimo 5.284,
Δ massimo 68).

---

## E — Aggregazione e intervalli

**Proposta.**

1. **Endpoint per famiglia e meccanismo:** accuratezza top-1, unità = *run fisico*; la
   accuratezza per meccanismo è la **media sui run** del meccanismo. Con celle mancanti la
   media diventa pesata in modo diseguale: si usa la versione pesata, come già deciso per il
   batch (REVISIONE_003).
2. **Intervalli — e il limite vero del bootstrap sul run.** Ricampionare il run fisico non
   rende indipendenti le osservazioni: nella permutazione **ogni run è insieme ricevente e
   donatore**, quindi due coppie che condividono un caso sono legate. Il ricampionamento va
   fatto su blocchi che quel legame lo contengono:

   - **unità di ricampionamento = ciclo della permutazione.** Il derangement π_F si scompone
     in cicli disgiunti; dentro un ciclo i casi sono legati (ciascuno dona al successivo),
     fra cicli no. Ricampionare **cicli interi** con reimmissione, portandosi dietro tutte le
     coppie FULL/PERM del ciclo, rispetta la struttura di dipendenza invece di ignorarla.
   - la coppia FULL/PERM (e FULL/OMIT) resta **appaiata** e non si ricampiona mai separata:
     il contrasto è appaiato per costruzione.
   - **gli intervalli sono condizionati al derangement realizzato.** Il seme è unico, quindi
     l'incertezza riportata non copre la variabilità fra derangement possibili. Va scritto
     così, accanto agli intervalli, non solo nei limiti.
   - il bootstrap semplice sul run resta riportabile come confronto, dichiarato come
     approssimazione che ignora l'accoppiamento.

   Se un ciclo copre quasi tutto S_F — succede con S_F a due classi, dove il derangement è
   una bigezione fra le due classi e i cicli sono corti ma numerosi — il numero di blocchi va
   riportato: è la vera numerosità effettiva dell'intervallo, non il numero di coppie.
3. **Accoppiamento donatore–ricevente:** dichiarato in metodologia, con la matrice degli
   abbinamenti pubblicata (`DERANGEMENTS_E5.json` → `pairing_matrix_recipient_from_donor`).
4. **Coppie incomplete:** se uno slot della coppia manca o è invalido, la **coppia** esce dal
   primario ed è contata a parte con la causa. Slot invalido (output generato ma non conforme)
   = **non corretto**, non mancante. Slot abbandonato (fallimento di trasporto non osservato)
   = escluso e riportato a parte, con l'analisi di robustezza ai due estremi, come in
   REVISIONE_003.
5. **Scomposizione per ricevente:** descrittiva, mai un endpoint.

## F — Posizione temporale del donatore

**In gioco.** Con una finestra per run, donatore e ricevente possono avere posizioni temporali
diverse (la finestra 1 di un caso può donare alla finestra 7 di un altro).

**Proposta: nessun vincolo.** Il derangement resta uniforme sull'insieme ammissibile; la
posizione di donatore e ricevente entra nella matrice degli abbinamenti pubblicata, e una
stratificazione per differenza di posizione è riportabile **senza chiamate aggiuntive** come
lettura descrittiva.

**Motivazione.** Vincolare la posizione ridurrebbe l'insieme ammissibile senza una ragione
formulabile a priori, e renderebbe il campionamento meno trasparente. La posizione è un
fattore osservato: si documenta, non si controlla.

---

## G — Quando congelare

**Proposta: congelare `exp5-protocol-frozen-001` PRIMA di aprire l'analisi 7.5**, cioè prima
di vedere le accuratezze per fault del batch.

**Motivazione.** Mappa famiglia–meccanismo, S_F, riceventi, aggregazione e intervalli sono
tutte scelte che, prese dopo aver visto gli esiti di B-LF, diventano sospettabili di selezione
sull'esito — anche se prese in buona fede. Nessuna di esse dipende dal batch: G0, G1 e G2
sono già eseguibili oggi (G0 è fatto). L'unica cosa che dipende dal batch è G4, la verifica
delle sei identità di FULL, che è una **verifica**, non una scelta.

**Rischio aggiuntivo, da nominare:** l'identità del modello. FULL = B-LF richiede stesso
modello, configurazione e decoding. Se il gestore aggiorna vLLM dopo il batch, il riuso cade e
FULL va rieseguito. Conviene quindi eseguire E5 **subito dopo** la chiusura del batch, non
settimane dopo, e far partire E5 con il proprio canary (stessi dieci prompt) con STOP su
fingerprint diverso.

---

## Riepilogo dei costi secondo le scelte

| A | B | chiamate E5 | tempo a 16,5 s | slot FULL riusati |
| --- | --- | ---: | ---: | ---: |
| (a) un ricevente | B1 (R=1) | 192 | ≈ 53 min | 64 (r1) |
| (a) un ricevente | **B2 (R=3, fissata)** | 576 | ≈ 2,6 h | 192 (r1-r3) |
| (a) un ricevente | B3 (R=3, senza maggioranza) | 576 | ≈ 2,6 h | 64 (r1) |
| (b) sette riceventi | B1 | 1.344 | ≈ 6,2 h | 448 (r1) |
| (b) sette riceventi | B2 | 4.032 | ≈ 18,5 h | 1.344 (r1-r3) |

FULL non è in queste chiamate: è riusato dal batch, se e solo se le sei identità di
`VERIFICA_FULL_BLF.md` reggono — su r1 con B1/B3, su tutte e tre le ripetizioni con B2.
