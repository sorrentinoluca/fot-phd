# PROJECT_UNDERSTANDING.md

Documento didattico per ricostruire, con ordine, cosa è stato fatto finora nel
progetto FoT/TEP (Fase A), perché, come funziona e cosa resta aperto.

Fonte primaria: repository `sorrentinoluca/fot-phd`, HEAD
`0a45817fd783513e23d58a35c55489404c95feec` (tag `phase-a-verbalizer-v2-complete`).
Tutti i valori numerici e i riferimenti a file provengono da quel commit.
Dove qualcosa non è ricavabile dal repository, è scritto esplicitamente
"Non verificabile dal repository corrente".

Il documento ha due parti. La Parte I si legge senza aprire il codice. La
Parte II entra nel dettaglio matematico e sperimentale.

---
---

# PARTE I — SPIEGAZIONE GENERALE E STEP-BY-STEP

---

## 1. Qual era il problema iniziale?

Il **Tennessee Eastman Process (TEP)** è la simulazione di un impianto chimico
industriale. Non è un impianto reale: è un modello matematico molto studiato,
usato da decenni come banco di prova per algoritmi di diagnosi guasti. Produce
misure che evolvono nel tempo, e permette di iniettare guasti noti — quindi si
sa sempre "qual era la verità", il che lo rende ideale per validare un metodo.

Le misure si chiamano **XMEAS** (process **meas**urements). Ce ne sono 41, e
ciascuna è una **serie temporale**: un valore per ogni istante di campionamento
(qui, uno al minuto, per 50 ore → circa 3000 numeri per misura, per 41 misure).

> **Perché è importante?**
> Un guasto in questo tipo di impianto non è un singolo numero fuori posto. È
> un *pattern che evolve*: una misura che si sposta di livello, un'altra che
> inizia a variare in modo irregolare, un gruppo che deriva lentamente. La
> diagnosi vive nella forma temporale dei segnali, non in un valore isolato.

Ora il nodo centrale del progetto. L'obiettivo di lungo periodo è usare
**modelli linguistici (LLM)** per ragionare sulla diagnosi, e più avanti farli
collaborare tramite **Federation over Text (FoT)**. Ma un LLM non può ricevere
in ingresso 41 × 3000 = 123.000 numeri grezzi e "capirli": non è quello che sa
fare, e anche potendo, la rappresentazione sarebbe illeggibile e
non interpretabile.

Serve quindi un componente intermedio che traduca i numeri in **testo**. Lo
chiamiamo **verbalizzatore**. La pipeline completa è:

```
serie temporali numeriche        (41 XMEAS × migliaia di campioni)
        ↓
rappresentazione strutturata     (poche feature numeriche per misura/finestra)
        ↓
testo neutrale                   (descrizione fattuale in linguaggio naturale)
        ↓
LLM / reasoning diagnostico      (interpreta il testo → ipotesi di guasto)
        ↓
Federation over Text (futuro)    (più agenti si scambiano insight testuali)
```

> **Attenzione:**
> Fino a ora abbiamo lavorato **sui primi tre livelli**: dai numeri alla
> rappresentazione strutturata, e da questa al testo neutrale. Il quarto
> livello (un LLM che ragiona) è stato solo toccato nel V1 come proof-of-concept
> ed è stato poi accantonato per motivi metodologici. Il quinto livello (FoT)
> **non è ancora stato affrontato**. Tutta la "Fase A" riguarda la costruzione
> e la validazione del verbalizzatore, non la federazione.

Un punto che sarà ripetuto più volte, perché è la ragione di quasi tutte le
scelte fatte: **il verbalizzatore deve essere separato dal reasoning
diagnostico**. Deve descrivere cosa fanno i segnali, non decidere quale guasto
sia. Se il verbalizzatore già "sapesse" la risposta, non resterebbe nulla da
dimostrare per l'LLM né, in futuro, per la federazione.

---

## 2. Qual era il problema del V1?

Il primo tentativo (i file `code/tep_characterize.py` e `code/tep_verbalize.py`,
tuttora presenti nel repo come reperti) era un proof-of-concept esplorativo. Ha
funzionato nel senso che ha prodotto descrizioni testuali e un LLM le ha
classificate correttamente in un test iniziale. Ma proprio provandolo sono
emersi problemi metodologici che hanno motivato la riscrittura V2.

I principali:

- **Prototype library nel prompt.** Il prompt del V1 conteneva già la
  descrizione delle categorie di guasto (chiamate A/B/C/D). In pratica si dava
  all'LLM sia il caso sia le regole per classificarlo. Un risultato "corretto"
  in queste condizioni dimostra poco: la conoscenza discriminante era servita
  su un piatto.
- **Il "5/5" non era una prova di FoT.** Cinque casi classificati bene misurano
  che *la descrizione conteneva abbastanza informazione*, non che la federazione
  serva a qualcosa. Erano due cose diverse confuse in una.
- **Uso ambiguo di "oscillazione".** Il V1 chiamava "oscillazione" un aumento
  di deviazione standard. Ma una deviazione standard alta può venire da un
  gradino, da una deriva o da rumore: non è necessariamente oscillazione (vedi
  sezione 5).
- **"std ratio" chiamato erroneamente "variance ratio".** Un rapporto di
  deviazioni standard non è un rapporto di varianze (differiscono di un
  quadrato). Terminologia da correggere.
- **Aggregazione di tutto il post-fault.** Il V1 calcolava le firme sull'intero
  segmento successivo al guasto, mescolando il transitorio iniziale con il
  regime successivo.
- **Rischio di contaminare transiente e regime persistente.** Senza distinguere
  "cosa succede all'inizio" da "cosa resta", si rischia di descrivere come
  permanente qualcosa che è solo un assestamento iniziale.
- **Normal troppo vicino alla baseline.** Nel V1 lo stesso file normale poteva
  servire sia a definire il riferimento sia come caso "normale" da valutare:
  un confronto quasi con se stesso.
- **Onset/injection da chiarire.** Non era stabilito con certezza quando il
  guasto entra realmente nel processo.

> **Cosa NON significa:**
> Non significa che il V1 fosse "sbagliato". È stato l'esperimento esplorativo
> che ha reso visibili questi problemi. Senza il V1 non avremmo saputo cosa il
> V2 doveva risolvere.

---

## 3. Audit del dataset

Prima di ricostruire il metodo, abbiamo verificato il dataset stesso. I fatti
accertati (documentati nel repo in `VERBALIZER_V2_FREEZE.md` e nel config):

- **Commit upstream pinnato:** `309b944f35ac440ff0c70616947ffe723c766e14`. Il
  dataset è "congelato" a una revisione precisa, così i risultati sono
  riproducibili anche se l'upstream cambia.
- **21 fault** disponibili nel benchmark; noi ne usiamo quattro (F1, F8, F10,
  F13), scelti per avere firme diverse tra loro.
- **10 batch per fault** realmente presenti (batch = una simulazione
  indipendente dello stesso guasto). Verificato contando i file.
- **README upstream obsoleto** su questo punto: dichiara 5 batch, ma nella
  revisione pinnata ce ne sono 10. Discrepanza reale, segnalata.
- **Normal da 500 ore** (`mode1_normal_500.xlsx`), oltre a uno da 50 h.
- **Sampling ≈ 1 minuto** (verificato: intervallo 0.016666… h).
- **41 XMEAS** per file.
- **Schema XLSX leggermente inconsistente** tra file: il file normale ha header
  fuorvianti (colonne chiamate `xmv-*` che in realtà sono le misure), i file di
  fault hanno colonne aggiuntive (XMV, costo operativo). Il codice gestisce
  questa inconsistenza con validazione esplicita.
- **Il Normal da 500 h è diviso in 10 blocchi** da 50 h ciascuno (N1…N10),
  così da avere blocchi normali indipendenti allineati allo split dei fault.

Lo **split** scelto:

| Stadio | Fault | Normal |
|---|---|---|
| development | batch 1–5 | N1–N5 |
| validation | batch 6–7 | N6–N7 |
| test held-out | batch 8–10 | N8–N10 |

> **Perché è importante?**
> Questo split è il cuore dell'onestà dell'esperimento. Tutto ciò che "guarda i
> dati" per prendere decisioni (scegliere feature, fissare soglie, definire
> come si genera il testo) avviene **solo sul development**. La validation serve
> a controllare che il metodo regga su dati nuovi. Il test held-out si guarda
> **una volta sola**, alla fine, e non può più cambiare nulla. Se si toccasse il
> metodo dopo aver visto validation o test, si introdurrebbe *leakage*: il
> metodo verrebbe adattato ai dati su cui poi lo si giudica, e il giudizio
> sarebbe falsato.

---

## 4. Come abbiamo verificato quando inizia il fault?

Sembra un dettaglio, ma è cruciale: se non si sa quando il guasto entra, si
rischia di misurare le firme sul segmento sbagliato.

La catena ricostruita dal simulatore (documentata in `VERBALIZER_V2_FREEZE.md`):

```
auto_run.m: dist(faultNum) = 1        (il guasto viene "acceso")
        ↓
MultiLoop_mode1.mdl: quel vettore entra in un blocco VariableTransportDelay
        ↓
un blocco Constant con valore 10 alimenta l'ingresso "ritardo" del delay
        ↓
l'uscita ritardata va all'ingresso "Disturbances" del plant
```

L'effetto: il plant "vede" il disturbo **a partire da 10 ore**, non da subito.

> **Attenzione — un caveat onesto:**
> C'è un anello della catena che poggia su un default, non su un valore scritto
> esplicitamente. Il blocco delay ha un parametro `InitialOutput` che dice cosa
> emette *prima* che il ritardo sia trascorso; nel modello questo valore **non è
> serializzato esplicitamente**, e si assume il default di Simulink (zero). Se
> quel default fosse diverso, la conclusione cambierebbe. Il freeze doc lo dice
> apertamente.

Distinguiamo quindi due livelli di evidenza:
- **Evidenza dal simulatore:** la catena `dist → VariableTransportDelay(10) →
  plant` è verificata leggendo i sorgenti.
- **Evidenza empirica (da completare):** se le prime 10 ore di un file di fault
  fossero statisticamente identiche al Normale, l'assunzione `InitialOutput=0`
  sarebbe confermata dai dati. **Non verificabile dal repository corrente**: il
  confronto empirico non è tra gli artefatti versionati.

Cosa possiamo affermare con sicurezza: il meccanismo è un transport delay a
10 h, non un guasto attivo da t=0. Il caveat residuo riguarda solo il valore
esatto dell'uscita iniziale.

Infine, una distinzione concettuale che tornerà utile:

- **t_inject** = quando il guasto entra *davvero* (verità del simulatore, 10 h).
- **t_detected** = quando il *verbalizzatore* riesce a notare una deviazione dai
  soli segnali.

La differenza `t_detected − t_inject` è, in prospettiva, una misura della
qualità del verbalizzatore (quanto è pronto a cogliere il guasto). In questo
progetto le finestre sono da 5 h, quindi la risoluzione di `t_detected` è
grossolana e t_inject a 10 h coincide con l'inizio della prima finestra
analizzata.

---

## 5. Perché abbiamo cambiato le feature?

Il problema del V1 era riassumere ogni misura con troppo poche grandezze, e
per giunta ambigue. Il V2 usa **cinque descrittori numerici**, ciascuno con un
significato preciso. In una frase ciascuno:

- **shift_sigma** — di quanto si è spostato il *livello medio* della misura
  rispetto al normale (in "quante deviazioni standard").
- **slope_sigma_h** — quanto la misura sta *derivando* nel tempo (pendenza di
  una retta, per ora).
- **raw_std_ratio** — quanto è *dispersa* nel complesso, senza distinguere il
  perché (solo descrittivo).
- **residual_std_ratio** — quanta variabilità resta *dopo aver tolto la
  tendenza lineare* (cattura l'oscillazione lenta).
- **diff_std_ratio** — quanto salta *da un campione al successivo* (cattura le
  variazioni rapide / il rumore).

Perché servono tutte e cinque? Perché fenomeni diversi producono lo stesso
`raw_std_ratio` alto, ma si distinguono guardando gli altri descrittori:

| Cosa succede al segnale | shift | slope | residual | diff |
|---|---|---|---|---|
| **Gradino (step)** | alto | ~0 | basso | basso |
| **Deriva lenta (drift)** | medio | alto | basso | basso |
| **Oscillazione lenta** | ~0 | ~0 | alto | basso |
| **Variazioni rapide/rumore** | ~0 | ~0 | medio | alto |

> **Perché è importante?**
> Guarda la colonna "gradino" e "oscillazione lenta": entrambe possono avere una
> deviazione standard grezza alta, ma il gradino ha `residual` basso (una volta
> tolto il salto non resta variabilità) mentre l'oscillazione ha `residual`
> alto. **Una sola deviazione standard elevata non dice "oscillazione".** Serve
> separare "quanto è disperso" da "in che modo è disperso". Questo è il singolo
> insegnamento più importante del passaggio da V1 a V2.

---

## 6. Cosa ci hanno insegnato i test sintetici?

Prima di applicare le feature ai dati reali, sono stati costruiti segnali
*artificiali* a verità nota (in `code/test_features.py`): un normale, un
gradino, una deriva, un'oscillazione lenta, una veloce, un aumento di rumore, e
combinazioni. Su questi si sa esattamente cosa c'è dentro.

L'obiettivo **non era classificare** questi casi. Era verificare che ogni
feature misuri ciò che dice di misurare. Per esempio: il test controlla che una
deriva lineare pulita produca `residual` basso (perché tolta la retta non resta
nulla), che un'oscillazione lenta produca `residual` più alto di quanto faccia
`diff`, e che un gradino piazzato *al bordo* della finestra risulti uno
spostamento di livello e **non** una falsa variabilità.

> **Perché è importante?**
> È la differenza tra *test del software* e *prova scientifica*. Questi test
> dicono "il codice calcola le grandezze che intende calcolare". Non dicono
> nulla su quale guasto sia quale: quello è compito del reasoning, più avanti.

---

## 7. Come abbiamo calibrato le soglie?

Ogni feature ha bisogno di una **soglia**: sopra quel valore la consideriamo
"attiva" (anomala), sotto no. La domanda è: da dove viene la soglia?

Principio guida: **la soglia si decide guardando solo il comportamento
normale**, mai i fault. Si osserva quanto oscillano le feature quando *non c'è
nessun guasto*, e si mette la soglia appena sopra quel rumore di fondo.

Come, in concreto (dai file `code/tep_analysis_v2/threshold_calibration.json` e
`.../threshold_calibration_report.md`):

- si usano **solo i blocchi Normal di development** (N1–N5);
- si divide ciascun blocco in finestre da **5 ore** → 50 finestre in tutto;
- per la baseline si usa **leave-one-block-out**: si stima il riferimento su
  quattro blocchi e si guarda il quinto, a rotazione (così un blocco non è mai
  giudicato rispetto a se stesso);
- in ogni finestra si prende il **massimo sulle 41 misure** di ciascuna feature;
- la soglia è un **quantile alto** di questi massimi (stile conformal), scelto
  in modo che, sul normale, si superi la soglia solo raramente.

> **Perché è importante?**
> Non guardando mai i fault durante la calibrazione, la soglia non può essere
> stata "aggiustata" per far risaltare i guasti. È una proprietà del rumore
> normale, non dei guasti. Questo rende onesto tutto ciò che viene dopo.

Le soglie risultanti sono state poi **congelate** (sezione 10) e non più
toccate.

---

## 8. Cosa fa concretamente il Verbalizer V2?

Qui sta il cuore della Fase A. Il verbalizzatore (`code/tep_verbalize_v2.py`)
compie due passi.

**Passo 1 — rappresentazione strutturata.** Per ogni misura e ogni finestra
temporale, calcola le cinque feature e le confronta con le soglie, contando
*in quante finestre* ciascuna è attiva, con che segno, in che punti del tempo.
Il risultato è un insieme di conteggi, non ancora una frase.

**Passo 2 — testo neutrale.** Traduce quei conteggi in linguaggio naturale,
in modo puramente fattuale.

Ecco un **esempio reale** preso dal repository
(`tep_validation_v2/validation_neutral_text.txt`, case_05, che corrisponde a un
caso di F10):

> "Intervallo osservato 10.0–50.0 h in 8 finestre da 5.0 h. XMEAS-18 supera la
> soglia di spostamento in 8/8 finestre, con segno positivo in 3 e negativo in
> 5; il run più lungo con segno coerente comprende 4 finestre… XMEAS-18:
> variabilità residua dopo rimozione del trend lineare sopra soglia in 8/8
> finestre; 2/2 nella fase iniziale e 2/2 nelle ultime finestre. XMEAS-18:
> variazioni campione-campione sopra soglia in 8/8 finestre… La massima
> dispersione complessiva osservata è su XMEAS-18 (rapporto tra deviazioni
> standard 20.70)."

Nota cosa fa e cosa **non** fa questo testo. Dice: XMEAS-18 è la protagonista,
supera le soglie in tutte le finestre, la variabilità residua e quella rapida
sono entrambe alte e persistenti. **Non dice** "questo è il fault 10", non dice
"oscillazione", non dice "instabilità". Riporta fatti misurati.

> **Cosa NON significa:**
> Il V2 non nega che quello sia oscillazione; semplicemente non lo *afferma
> automaticamente*, perché quella è una conclusione interpretativa. Etichettare
> "residual alto" come "instabilità oscillatoria", o "slope alto" come "drift
> persistente", richiede reasoning. Il verbalizzatore fornisce le prove; il
> giudizio è di chi legge (l'LLM, in futuro). Il config
> (`code/verbalizer_config_v2.json`) elenca esplicitamente un vocabolario di
> termini *vietati in automatico*: "oscillazione", "instabilità oscillatoria",
> "periodicità", "aumento della varianza".

---

## 9. Come abbiamo trattato il tempo?

Dire "questa feature è alta" non basta, perché *quando* e *come a lungo* è alta
cambia il significato. Un picco in una sola finestra iniziale è un transitorio;
la stessa feature alta in tutte le finestre è un regime persistente.

Per questo il verbalizzatore, per ogni misura e feature, calcola grandezze come:

- **quante finestre** sono attive (su quante totali);
- il **segno** dell'attività (spostamento verso l'alto o verso il basso) e
  quanto è **coerente** nel tempo;
- il **run più lungo** con segno coerente (una sequenza ininterrotta);
- se l'attività è **presente all'inizio** e/o **nelle ultime finestre**.

Esempio intuitivo con **F1** (dai dati development, `development_top1.csv`):
XMEAS-1 ha uno **spostamento di livello enorme e stabilissimo** (circa 85
deviazioni standard, con lo stesso segno in tutte le finestre) — un livello che
si sposta e *resta* spostato. Ma la sua **variabilità dinamica** è più presente
all'inizio che alla fine.

> **Cosa NON significa:**
> Questa combinazione — livello spostato e stabile + variabilità soprattutto
> iniziale — **non** è "oscillazione persistente". È uno spostamento permanente
> con un transitorio di assestamento. Il V1, che aggregava tutto il post-fault,
> avrebbe potuto descriverlo come variabilità persistente. Il V2, distinguendo
> fase iniziale e fase tardiva, lo rappresenta correttamente. E lo fa **senza
> una regola speciale scritta per F1**: emerge dai conteggi temporali generali.

---

## 10. Freeze prima della validation

Prima di aprire i dati di validation, il metodo è stato **sigillato**. In
pratica:

- le soglie e i parametri sono stati scritti in un file di configurazione
  (`code/verbalizer_config_v2.json`) e dichiarati definitivi;
- di ogni file chiave è stato calcolato l'**hash SHA-256** (un'impronta digitale
  che cambia se anche un solo carattere cambia), registrato in
  `VERBALIZER_V2_FREEZE.md`;
- è stato creato un **commit Git con un tag** che marca il momento del freeze.

I tag realmente presenti nel repository (verificati):

```
verbalizer-v2-pre-validation        → freeze (commit 3fd960a)
verbalizer-v2-validation-complete   → dopo validation (commit 1d9c161)
verbalizer-v2-test-complete         → dopo test (commit 0a45817)
phase-a-verbalizer-v2-complete      → stesso commit del test (0a45817)
```

> **Perché è importante?**
> È un "sigillo sperimentale". L'ordine corretto è: *prima* si blocca il metodo,
> *poi* si guardano validation e test. Se il metodo cambiasse dopo aver visto
> quei dati, non si potrebbe più distinguere "il metodo funziona" da "il metodo
> è stato ritoccato finché non ha funzionato su quei dati". Gli hash rendono il
> sigillo verificabile da chiunque: bastano per dimostrare che i file non sono
> cambiati.

---

## 11. Cosa è successo in validation?

La validation (batch 6–7, N6–N7) serviva a vedere se le firme reggono su dati
non visti in development, **senza** poter più cambiare il metodo. In sintesi
intuitiva (numeri nella Parte II):

- **F1** e **F10**: firme rimaste **stabili** — molto simili a quelle di
  development.
- **F13** e **F8**: **parzialmente stabili** — riconoscibili, ma con più
  variabilità tra i casi.
- **Normal N6–N7**: qualche falso positivo in più rispetto al development (vedi
  Parte II), ma su soli due blocchi è un campione piccolo.

> **Attenzione:**
> Anche vedendo questi risultati, **il metodo non è stato modificato**. Questo è
> il punto: la validation informa, ma non deve retroagire sul metodo congelato,
> altrimenti si contamina il test successivo.

---

## 12. Cosa è successo nel test finale?

Il test held-out (batch 8–10, N8–N10) è la prova definitiva, guardata una volta
sola. In sintesi:

- **F1**: stabile sui tre batch.
- **F10**: stabile sui tre batch.
- **F13**: variazione moderata, ancora riconoscibile.
- **F8**: **la firma peggiora sensibilmente sul batch 10** (vedi sotto).
- **Normal**: falsi positivi bassi, in linea col development.

Il caso **F8** merita attenzione, perché è il risultato più istruttivo del test:

> **Cosa NON significa:**
> F8 che si degrada sul batch 10 **non è un bug da correggere**. È un
> *risultato*: mostra che la firma di F8 è più sensibile alla variabilità tra
> simulazioni indipendenti. Correggere il metodo ora per "sistemare" F8
> significherebbe adattarlo al test — esattamente ciò che il freeze serve a
> impedire. Il test è già stato consumato: F8 resta come limite noto e onesto.

---

## 13. Quindi cosa abbiamo realmente dimostrato?

Questa distinzione è la più importante del documento.

**Abbiamo evidenza che:**
- il verbalizzatore V2 produce firme strutturate che, per F1 e F10, restano
  coerenti su simulazioni indipendenti (development → validation → test);
- alcune firme (F1, F10) **generalizzano bene**; F13 in modo intermedio;
- **F8 è più variabile** e la sua firma si indebolisce nel test held-out;
- il rate di falsi positivi sul Normale generalizza (simile tra development e
  test);
- il metodo è stato **congelato prima** di guardare validation e test, e il
  congelamento è verificabile (hash + storia Git).

**NON abbiamo ancora dimostrato:**
- che un LLM classifichi *accuratamente* i guasti da queste descrizioni (la
  Fase A misura separabilità delle firme, non accuratezza di un LLM);
- che **Federation over Text migliori** la diagnosi (FoT non è stato eseguito);
- che un eventuale miglioramento sia **causato dalla federazione** e non da
  altro;
- che il metodo **generalizzi in senso universale** (poche classi, pochi batch,
  un solo mode del processo).

---

## 14. Dove siamo ora?

```
PHASE A:   numerico → strutturato → testo neutrale
           [ COMPLETATA e validata su held-out, con limiti noti ]

PHASE B:   agenti locali → insight locali → Federation over Text → valutazione
           [ DA PROGETTARE / ESEGUIRE ]
```

La Fase A ha costruito e verificato il *ponte* dai numeri al testo. La Fase B
userà quel ponte per far ragionare e collaborare più agenti.

---
---

# PARTE II — APPROFONDIMENTO TECNICO E METODOLOGICO

---

## 15. Dataset e unità sperimentale

Ogni workbook (`mode1_<fault>_<batch>.xlsx`) contiene una colonna `Time (h)`,
le 41 colonne `XMEAS-1..41`, e nei file di fault anche colonne `XMV-*`
(variabili manipolate dagli attuatori) e `operational_cost`. Il codice
(`code/tep_features.py`, funzione `normalize_schema`) tiene **solo Time + le 41
XMEAS**; le XMV e il costo sono scartati dopo la validazione dello schema.

Perché solo le XMEAS: sono le *misure osservate* del processo, l'analogo dei
sensori. Le XMV sono i comandi del controllore — informazione di natura diversa,
esclusa per tenere il problema pulito.

> **Attenzione — pseudo-replicazione:**
> L'**unità sperimentale indipendente è il batch (la simulazione)**, non la
> singola finestra temporale. Le 8 finestre di uno stesso batch non sono
> osservazioni indipendenti: vengono dallo stesso run e sono correlate.
> Trattarle come indipendenti gonfierebbe artificialmente la numerosità
> campionaria (pseudo-replicazione). Per questo i confronti tra classi si
> ragionano a livello di batch, con pochi batch per stadio.

---

## 16. Baseline Normal

La baseline (media, deviazione standard, e le statistiche per residui e
differenze) è calcolata **solo sui blocchi Normal di development** (N1–N5), con
due accortezze implementate in `compute_baseline_stats_from_blocks`
(`code/tep_features.py`):

- **block-aware, niente concatenazione ingenua.** Le differenze prime e i
  residui del detrend sono calcolati *dentro ciascun blocco* e poi messi
  insieme. Se si concatenassero i blocchi e poi si facesse la differenza, al
  confine tra due blocchi (che hanno medie diverse) nascerebbe un salto
  artificiale enorme, che falserebbe `diff_std`. Il test in
  `code/test_features.py` verifica proprio questo: la baseline concatenata
  ingenuamente produce `diff_std` >5× di quella corretta.
- **leave-one-block-out** per non giudicare mai un blocco rispetto a se stesso.

> **Distinzione da tenere presente:**
> "baseline statistics" (il riferimento del normale, stabile) e "observation
> window" (la finestra del caso in esame) sono cose diverse. Le feature del caso
> si misurano *rapportando* la finestra osservata alla baseline.

---

## 17. Definizione matematica delle feature

Notazione: per una finestra, `x` sono i valori di una misura, `t` i tempi (in
ore). Il pedice `b` indica la baseline normale.

**shift_sigma** — spostamento di livello.
- Formula: `(mean(x) − mean_b) / std_b`
- Unità: adimensionale (deviazioni standard del normale).
- Significato: di quanto il livello medio si è spostato.
- Rileva: gradini, spostamenti permanenti.
- NON permette di concludere: *come* è distribuito il segnale nel tempo (un
  segnale molto variabile può avere media spostata o no).

**slope_sigma_h** — tendenza locale.
- Formula: pendenza OLS di `x` contro `t`, divisa per `std_b` → `slope / std_b`.
- Unità: deviazioni standard del normale **per ora**.
- Significato: quanto il segnale deriva linearmente nel tempo.
- Rileva: derive lente, trend.
- NON permette di concludere: che ci sia un "drift" *diagnostico* — è solo
  evidenza di tendenza locale (lo dice esplicitamente il freeze doc).

**raw_std_ratio** — dispersione complessiva (solo descrittivo).
- Formula: `std(x) / std_b`
- Significato: quanto è dispersa la misura, senza distinguere il perché.
- NON permette di concludere: la *natura* della dispersione (vedi sezione 5).

**residual_std_ratio** — variabilità dopo detrend.
- Formula: si toglie da `x` la retta OLS, si prende la std dei residui, divisa
  per la corrispondente std residua della baseline.
- Rileva: oscillazione lenta / struttura che resta dopo aver rimosso la
  tendenza.
- NON permette di concludere: se è periodica (non è un'analisi in frequenza).

**diff_std_ratio** — variabilità campione-campione.
- Formula: `std(diff(x)) / diff_std_b`, dove `diff(x)` sono le differenze prime.
- Rileva: variazioni rapide, rumore ad alta frequenza.
- NON permette di concludere: oscillazioni lente (tra due campioni vicini una
  sinusoide lenta cambia poco → `diff` resta basso).

> **std ratio ≠ variance ratio.**
> Tutte le feature `*_std_ratio` sono rapporti di **deviazioni standard**. Il
> rapporto di **varianze** sarebbe il quadrato:
>
> `variance_ratio = (std_ratio)²`
>
> Esempio: `std_ratio = 20` significa deviazione standard 20× la norma, che
> corrisponderebbe a varianza 400× — un numero molto diverso. Chiamare "20×" un
> rapporto di varianze sarebbe un errore di un fattore quadratico. Il config
> lo chiarisce nella sezione `feature_semantics`.

---

## 18. Ambiguità fondamentali delle feature

Anche con cinque feature, restano ambiguità che nessuna singola grandezza
risolve del tutto:

- **oscillazione lenta vs transitorio non lineare:** entrambe alzano
  `residual`; distinguerle richiederebbe analisi in frequenza.
- **oscillazione veloce vs aumento di rumore stocastico:** entrambe alzano
  `diff`; la differenza (deterministica vs casuale) non è visibile a queste
  feature.
- **gradino interno alla finestra:** alza `residual` (il salto sopravvive al
  detrend lineare) pur non essendo variabilità continua.
- **mezza sinusoide nella finestra:** può assomigliare a una pendenza (slope)
  invece che a un'oscillazione.
- **gradino al bordo finestra:** se il salto cade appena fuori, l'intera
  finestra appare come livello spostato senza variabilità — comportamento
  desiderato e verificato nei test.

> **Perché non abbiamo (ancora) introdotto FFT/wavelet?**
> Analisi in frequenza risolverebbero alcune di queste ambiguità, ma
> aggiungerebbero complessità e iperparametri proprio mentre l'obiettivo è
> tenere il metodo semplice, interpretabile e congelabile. Il progetto è un
> proof-of-concept di FoT, non un nuovo algoritmo di time-series classification.
> Le ambiguità restano dichiarate come limiti, non nascoste.

---

## 19. Calibrazione delle soglie — dettaglio matematico

Protocollo esatto (da `threshold_calibration.json`):

- `n = 50` finestre normali di development (5 blocchi × 10 finestre da 5 h).
- `alpha = 0.05`.
- rango: `k = ceil((n + 1) * (1 − alpha)) = ceil(51 * 0.95) = ceil(48.45) = 49`.
- per ogni finestra si prende il **massimo sulle 41 XMEAS** della feature.
- la soglia è il **49° valore** in ordine crescente di questi 50 massimi.
- confronto di attivazione **stretto**: `score > threshold`.

Le soglie congelate (piena precisione, da `verbalizer_config_v2.json`):

| Feature | Soglia |
|---|---|
| `abs(shift_sigma)` | 1.9695333234149084 |
| `abs(slope_sigma_h)` | 0.7468621213669596 |
| `residual_std_ratio` | 1.3681613543196571 |
| `diff_std_ratio` | 1.4051245046201666 |

> **Attenzione — il bug dell'arrotondamento:**
> Il config nota che le soglie vanno usate a **piena precisione**. Se si
> arrotondasse la soglia (es. a poche cifre) e si usasse un confronto stretto
> `>`, un valore normale esattamente pari alla soglia arrotondata potrebbe
> risultare erroneamente "sopra soglia", creando falsi positivi. Usare il valore
> completo evita questo.

**Perché "3/50 any-primary" non contraddice il 5% per-feature.** Con `alpha =
0.05`, ogni singola feature attiva sul normale circa il 5% delle finestre (≈
1/50 per feature nei diagnostics). Ma "any-primary" (almeno una delle feature
attiva) unisce più feature, quindi il tasso sale. Come intuizione dell'unione,
se le feature fossero **indipendenti**:

`1 − (1 − 0.05)⁴ ≈ 0.185` → circa 18–19%.

Nel development si osservano 3/50 = 6% any-primary, **più basso** di quel 18%
proprio perché le feature **non sono indipendenti** (tendono ad attivarsi
insieme sulle stesse finestre rumorose). Quindi 3/50 e 5%-per-feature sono
coerenti, non in contraddizione.

> **Cosa NON significa:**
> Il `1 − (1 − 0.05)⁴` è solo un'intuizione del caso indipendente, non il
> valore atteso reale. Serve a capire la direzione (l'unione alza il tasso),
> non a predire il 6%.

---

## 20. Rappresentazione temporale

Per ogni misura e feature, il verbalizzatore (`code/tep_verbalize_v2.py`,
funzioni `_signed_summary`, `_unsigned_summary`, `_variable_signature`) calcola:

- **n_active_windows / active_fraction:** in quante finestre (frazione) la
  feature supera la soglia.
- **positive_count / negative_count:** per le feature *con segno* (shift,
  slope), quante attivazioni verso l'alto e quante verso il basso.
- **sign_consistency:** quanto il segno è coerente (tutte nello stesso verso vs
  alternato).
- **longest_same_sign_run / longest_run:** la più lunga sequenza ininterrotta di
  finestre attive (con segno coerente, per le feature con segno).
- **first_active_window / last_active_window:** dove inizia e finisce
  l'attività.
- **early_active / late_active:** se c'è attività nelle finestre iniziali e/o in
  quelle finali (le fasi sono definite nel config: 2 finestre iniziali, 2
  finali).
- **rapid variability:** un descrittore aggiuntivo di variabilità rapida.

> **Perché 2 finestre consecutive ≠ persistenza globale.**
> Il config (`temporal_logic.global_persistence`) impone una regola esplicita:
> due finestre attive consecutive indicano un *episodio sostenuto*, ma **non**
> bastano a dichiarare persistenza globale. La persistenza "stretta" richiede
> attività in *ogni* finestra, un solo segno, e attività anche nel regime
> tardivo. Questa è la correzione diretta del problema del V1, che descriveva
> come persistente ciò che poteva essere transitorio.

---

## 21. Structured signature a 697 dimensioni

L'evaluator (`code/evaluate_verbalizer_v2.py`, funzione `signature_vector`)
rappresenta ogni caso come un vettore di **41 XMEAS × 17 componenti = 697
dimensioni**, tutte in [0,1].

Le **17 componenti per misura** (verificate dal codice) sono, in ordine:

Per **level** (shift) e per **trend** (slope) — 4 ciascuno:
1. active_fraction
2. segno normalizzato: `(signed_count/n + 1) / 2` (porta il segno da [−1,1] a [0,1])
3. late_active_fraction
4. longest_same_sign_run / n

Per **residual**, **diff**, **rapid** — 3 ciascuno:
5. active_fraction
6. late_active_fraction
7. longest_run / n

Totale: 4 + 4 + 3 + 3 + 3 = **17**.

Tutte le componenti sono già naturalmente in [0,1] (frazioni, o run divisi per
`n`, o segno riscalato). Il codice **solleva un errore** se un valore esce da
[0,1], come guardia.

Concettualmente, il vettore di 697 numeri è la "firma" del caso: per ogni
misura, quanto e come ciascun tipo di anomalia è presente nel tempo.

---

## 22. Similarity evaluator

Due firme si confrontano con:

`similarity = 1 − mean(|a − b|)`

cioè uno meno la distanza media componente per componente. Poiché le componenti
sono in [0,1], la similarità è in [0,1]: 1 = identiche, 0 = massimamente diverse.

**Esempio numerico** (con 4 componenti, per capire):
```
a = [0.9, 0.2, 1.0, 0.5]
b = [0.8, 0.3, 0.9, 0.5]
|a − b| = [0.1, 0.1, 0.1, 0.0]   media = 0.075
similarity = 1 − 0.075 = 0.925
```

Da qui:
- **intra-class similarity:** quanto si somigliano i casi *dello stesso* fault
  (alta = firma stabile).
- **inter-class similarity:** quanto si somigliano casi di fault *diversi*
  (bassa = classi ben separate).
- **margin:** intra meno la massima inter (quanto la classe si distingue dalla
  più simile tra le altre). Positivo = separabile.
- **Jaccard top-4:** quanto coincidono gli insiemi delle 4 misure più coinvolte
  tra due casi (stabilità di *quali* variabili contano).
- **variable recurrence:** quanto ricorrono le stesse misure protagoniste tra
  batch.

> **Cosa NON significa — punto cruciale:**
> Queste sono metriche di **separabilità descrittiva**, non di **accuratezza di
> classificazione**. Dicono "le firme dello stesso guasto si somigliano e quelle
> di guasti diversi si distinguono", non "un classificatore azzecca l'X% dei
> casi". Nessun classificatore è stato addestrato o valutato. Confondere le due
> cose sarebbe l'errore interpretativo più grave possibile su questi risultati.

---

## 23. Risultati development

Pattern principali (da `code/tep_analysis_v2/development_top1.csv`, la misura
dominante per feature in ciascun batch):

- **F1:** dominato da **XMEAS-1**, con `shift_sigma ≈ +85` stabilissimo su tutti
  i 5 batch. `residual` alto (~19–20) ma `diff` basso (~1.2). Lettura: forte
  spostamento di livello permanente, con variabilità lenta ma senza forti
  variazioni rapide.
- **F8:** meno stabile. La variabile dominante per lo shift **cambia tra
  batch** (XMEAS-1, poi XMEAS-7, XMEAS-34, XMEAS-18): segno di una firma meno
  ancorata. `raw_std_ratio` alto (~22–35) su XMEAS-1, `diff` dominato da
  XMEAS-10. Questa instabilità già in development anticipa il problema di
  generalizzazione emerso nel test.
- **F10:** dominato da **XMEAS-18**, con `diff_std_ratio` costantemente ~2 e
  `residual` ~15–18. Ma lo `shift` di XMEAS-18 **varia molto tra batch** (da
  ~4 a ~0.47, con segno non sempre uguale): la firma di F10 è nella
  *variabilità* di XMEAS-18, non nel suo livello.
- **F13:** dominato da **XMEAS-7** con `shift` grande e **negativo** (da −24 a
  −43) e `raw_std_ratio` altissimo (40–70). Firma forte ma con ampiezza
  variabile tra batch.

Cosa ci hanno insegnato: le feature separano bene i *tipi* di firma (F1 =
livello; F10 = variabilità su una misura; F13 = grande dinamica multivariata su
XMEAS-7; F8 = diffuso e meno ancorato), e già qui F8 appare il più fragile.

---

## 24. Risultati validation

Dai `tep_validation_v2/validation_report.md` (mediane):

| Fault | intra sim. | val→dev | margin |
|---|---|---|---|
| F1 | 0.9892 | 0.9889 | 0.0751 |
| F10 | 0.9935 | 0.9922 | 0.0163 |
| F13 | 0.8970 | 0.8886 | 0.0450 |
| F8 | 0.8956 | 0.8983 | 0.0436 |
| Normal | 0.9984 | 0.9986 | — |

Lettura: F1 e F10 con intra molto alta (firme quasi identiche a development).
F13 e F8 più basse (~0.89–0.90). I margin restano **tutti positivi** (le classi
restano separabili), ma F10 ha il margine più stretto (0.016): stabile ma con
poco spazio dalla classe più simile.

**Normal N6–N7:** 4/20 finestre "any-primary" positive (20%), contro 6% del
development.

> **Attenzione — senza drammatizzare:**
> 20% su 20 finestre sono 4 finestre. Su un campione così piccolo (2 blocchi),
> qualche falso positivo in più è atteso e non indica che il metodo sia rotto.
> Il dato da tenere d'occhio, non un allarme. Nel test held-out (più blocchi) il
> tasso torna basso.

---

## 25. Risultati held-out test

Dai `tep_test_v2/test_report.md` e `test_split_comparison.csv`. La colonna
"test" mostra i tre batch (8, 9, 10) dove rilevante.

| Fault | dev intra | val intra | test intra (b8/b9/b10) |
|---|---|---|---|
| F1 | 0.9905 | 0.9892 | 0.9906 (stabile) |
| F10 | 0.9898 | 0.9935 | 0.9907 (stabile) |
| F13 | 0.8858 | 0.8970 | 0.8890 (moderata var.) |
| F8 | 0.9043 | 0.8956 | **0.8597** (calo) |

**Normal N8–N10:** 2/30 any-primary ≈ 6.7%, in linea col development (6%). Il
rate di falsi positivi generalizza.

### F8 batch 10 — sottoparagrafo dedicato

Il segnale di degrado di F8 è coerente su tre metriche indipendenti (dal
`test_split_comparison.csv`, valori sui tre split dev/val/test-batch10):

- **intra_similarity F8:** 0.9043 / 0.8956 / **0.8597** — crollo sul batch 10.
- **margin F8:** 0.0515 / 0.0436 / **0.0143** — il margine si assottiglia quasi
  a zero: F8 diventa a malapena separabile dalla classe più simile.
- **top4_jaccard_level F8:** 0.238 / 0.6 / 0.333 — l'insieme delle misure
  dominanti per il livello è instabile tra batch.

Poiché tre metriche diverse concordano, **non è un artefatto dell'evaluator**:
è variabilità distribuzionale reale di F8. Coerente con quanto già visto in
development (sezione 23), dove la variabile dominante di F8 cambiava tra batch.

---

## 26. Audit anti-leakage

Storia Git realmente osservata (4 commit lineari su `main`):

```
3fd960a  Freeze verbalizer V2 before validation   [tag: verbalizer-v2-pre-validation]
1d9c161  Record verbalizer V2 validation           [tag: verbalizer-v2-validation-complete]
b113046  Preserve development analysis artifacts
0a45817  Complete Verbalizer V2 final test          [tag: verbalizer-v2-test-complete,
                                                            phase-a-verbalizer-v2-complete]
```

Prove verificate direttamente:
- **`git diff` tra freeze e test** sui sette file di codice/config frozen:
  **0 righe di differenza** per ognuno. I file non sono cambiati.
- **hash SHA-256** dichiarati in `VERBALIZER_V2_FREEZE.md` **corrispondono** ai
  file reali all'HEAD (verificati con `sha256sum`).
- il diff freeze→validation aggiunge **solo output di validation**; il diff
  validation→test aggiunge **solo output di test e artefatti di development**.
  Nessun file di metodo toccato dopo il freeze.

> **Perché è importante scientificamente?**
> Questo trasforma "abbiamo congelato il metodo" da affermazione a fatto
> verificabile. Un revisore esterno può ripetere questi controlli e confermare
> che validation e test non hanno retroagito sul metodo. È la base che rende
> credibili i risultati delle sezioni 24–25.

> **Discrepanza segnalata:** il campo `status` in
> `code/verbalizer_config_v2.json` è ancora `"FROZEN_PENDING_VALIDATION"`
> all'HEAD (dopo il test). Coerente col fatto che il file non è stato toccato,
> ma il testo dello stato non riflette lo stadio reale. È un'imprecisione
> documentale, non un problema di metodo.

---

## 27. Limiti metodologici attuali

Distinguendo limiti *normali di un proof-of-concept* da limiti *gravi*:

Limiti normali (attesi, dichiarati):
- **Pochi batch:** 5 dev / 2 val / 3 test per fault. Campioni piccoli, intervalli
  ampi.
- **Dipendenza temporale tra finestre:** le finestre di uno stesso batch sono
  correlate (pseudo-replicazione); l'unità indipendente è il batch.
- **Metrica evaluator descrittiva:** misura separabilità, non accuratezza.
- **Nessuna analisi in frequenza:** ambiguità oscillazione/rumore non risolte
  per scelta.

Limiti da tenere in evidenza:
- **F8 distributional variation:** limite reale di generalizzazione, emerso nel
  test. Non correggibile ora (test consumato).
- **injection time caveat:** l'`InitialOutput=0` del delay è un default assunto,
  non verificato esplicitamente (sezione 4). **Non verificabile dal repository
  corrente** con evidenza empirica.
- **riproducibilità del calibratore:** lo script che *genera* le 4 soglie con il
  protocollo conformal **non è presente tra i file `.py` del repository**. I
  valori delle soglie sono documentati (config + calibration report), ma il
  codice che li produce non è versionato → un esterno non può rigenerarli. **Da
  risolvere prima della Fase B.**
- **assenza di `requirements.txt`:** le versioni delle dipendenze (numpy,
  pandas) non sono fissate nel repo.

Limite di scope (non un difetto, un confine):
- **nessun test FoT eseguito.** La Fase A non tocca la federazione.

---

## 28. Architettura concettuale della futura Fase B

La Fase A fornisce il mattone (testo neutrale per caso). La Fase B lo userà per
la federazione. Lo schema concettuale (non ancora un disegno sperimentale):

```
Agent 1:  conosce localmente  Normal + F1
Agent 2:  conosce localmente  Normal + F8
Agent 3:  conosce localmente  Normal + F10
Agent 4:  conosce localmente  Normal + F13
```

Ogni agente riceve **descrizioni V2 neutrali** dei propri casi, ragiona
localmente, ne distilla insight, e questi confluiscono in una **insight library
condivisa**. Il test della federazione è: un agente riesce a diagnosticare un
guasto che **non ha mai visto localmente**, grazie agli insight condivisi dagli
altri?

> **Perché NON dobbiamo rimettere una prototype library A/B/C/D nel prompt.**
> Se il prompt contenesse già le definizioni delle classi, l'agente avrebbe la
> conoscenza discriminante *prima* di qualsiasi federazione — e non resterebbe
> nulla da trasferire. È l'errore del V1 (sezione 2). In Fase B la conoscenza
> "quale firma corrisponde a quale guasto" deve arrivare **dalla insight
> library** (cioè dagli altri agenti), non dal prompt. Solo così si misura il
> valore *marginale* della federazione, che è l'obiettivo dell'intero progetto.

---

## 29. Glossario

- **TEP** — Tennessee Eastman Process: simulazione di impianto chimico usata come
  benchmark di diagnosi guasti.
- **XMEAS** — le 41 misure di processo (i "sensori") del TEP.
- **batch** — una singola simulazione indipendente di un guasto; l'unità
  sperimentale indipendente.
- **baseline** — statistiche di riferimento calcolate sul comportamento normale.
- **shift** — spostamento del livello medio di una misura, in deviazioni
  standard.
- **slope** — pendenza/tendenza lineare locale di una misura nel tempo.
- **residual** — variabilità che resta dopo aver rimosso la tendenza lineare
  (cattura oscillazione lenta).
- **diff** — variabilità tra campioni consecutivi (cattura variazioni rapide).
- **raw std ratio** — rapporto di deviazioni standard grezze; dispersione
  complessiva, solo descrittiva.
- **threshold (soglia)** — valore oltre il quale una feature è "attiva";
  calibrata sul solo normale.
- **calibration** — procedura che fissa le soglie guardando solo il normale di
  development.
- **development** — i dati (batch 1–5, N1–N5) su cui si prendono tutte le
  decisioni di metodo.
- **validation** — i dati (batch 6–7, N6–N7) per controllare la tenuta senza
  cambiare il metodo.
- **held-out test** — i dati (batch 8–10, N8–N10) guardati una volta sola, alla
  fine.
- **leakage** — contaminazione che avviene quando i dati di validation/test
  influenzano le scelte di metodo.
- **freeze** — congelamento verificabile (hash + tag Git) del metodo prima di
  validation/test.
- **neutral verbalization** — descrizione testuale fattuale che riporta misure,
  non diagnosi.
- **prototype library** — insieme di definizioni di classe fornite a priori;
  da evitare nel prompt perché regala la risposta.
- **structured signature** — il vettore di 697 componenti che riassume la firma
  di un caso.
- **intra-class similarity** — quanto si somigliano casi dello stesso guasto.
- **inter-class similarity** — quanto si somigliano casi di guasti diversi.
- **margin** — intra meno la massima inter; quanto una classe si distingue dalla
  più simile.
- **FoT (Federation over Text)** — paradigma in cui più agenti collaborano
  scambiandosi insight *testuali* invece di gradienti o pesi; oggetto della
  futura Fase B.

---

# Se ricordi solo 10 cose

1. **La pipeline è: numeri → rappresentazione strutturata → testo neutrale →
   (futuro) LLM → (futuro) FoT.** La Fase A copre i primi tre livelli.
2. **Il verbalizzatore descrive, non diagnostica.** Riporta fatti misurati; non
   dice "fault 10", "oscillazione" o "instabilità" — quelle sono conclusioni del
   reasoning.
3. **Cinque feature con significati distinti** (shift, slope, raw, residual,
   diff) servono perché *una sola deviazione standard alta non dice
   "oscillazione"*: bisogna separare quanto è disperso da come.
4. **std ratio ≠ variance ratio** (differiscono di un quadrato).
5. **Le soglie si calibrano solo sul Normale di development**, mai sui fault:
   così non possono essere adattate ai guasti.
6. **Lo split development / validation / test-held-out** è ciò che rende onesto
   l'esperimento; il test si guarda una volta sola.
7. **Il metodo è stato congelato prima di validation/test**, e il freeze è
   *verificabile* (hash SHA-256 + tag Git, `git diff` = 0 righe sui file
   frozen).
8. **Abbiamo evidenza di separabilità descrittiva** (F1, F10 stabili; F13
   intermedio; **F8 si degrada nel test**), **non** di accuratezza di un LLM né
   di alcun vantaggio di FoT.
9. **F8 non è un bug da correggere**: è un risultato reale di variabilità
   distribuzionale, e il test è già consumato.
10. **In Fase B non si rimette una prototype library A/B/C/D nel prompt**: la
    conoscenza "firma → guasto" deve arrivare dalla insight library condivisa,
    altrimenti non si misura il valore della federazione.

---

## Nota di coerenza col repository

Verifiche incrociate col repo (HEAD `0a45817`): tag, hash SHA-256, `git diff`
sui file frozen, soglie del config, struttura delle 17 componenti dell'evaluator,
testi neutrali di esempio (validation), e tabelle di development/validation/test
provengono tutti dagli artefatti versionati. Due elementi **non** ricavabili dal
repository, segnalati come tali nel testo: (a) la verifica *empirica*
dell'injection time (`InitialOutput=0`); (b) lo script che genera le soglie
conformal. Un terzo punto è una discrepanza documentale interna al repo: il
campo `status` del config resta `FROZEN_PENDING_VALIDATION` anche dopo il test.
