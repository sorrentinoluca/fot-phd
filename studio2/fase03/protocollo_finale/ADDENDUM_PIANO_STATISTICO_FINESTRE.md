# Addendum al piano statistico 03.8 — finestre e ripetizioni

Revisione 1, 2026-09-17; allegato al candidato protocollo rev2. **PROPOSTA DA APPROVARE E
RIVEDERE, NON FREEZE.** Il piano al tag `studio2-fase03-piano-statistico-frozen-001`, SHA file
`675dbbcc96d9e1e3c153388b905291c3ece7930e563a2f78f37183b6194d032a`, rimane intatto.
Origine vincolante: D1 e D4 di `DECISIONI_AUTORE_7_3_REV2_2026-09-17.md` (copia byte-identica
accanto a questo file). Nessun dato di test, esito diagnostico o segnale è stato consultato.
Le derivazioni sotto sono verifiche algebriche, non risultati simulati né validazione empirica.

## 1. Disegno, quantità stimata e due fonti di casualità

Per ogni fault f: n=8 run, J=8 posizioni, una permutazione uniforme pi_f dei numeri 1..8,
indipendente dai segnali/esiti. Il caso del run r è (r, pi_f(r)); `case_id` resta il run_id.
Normal segue la stessa regola; ciascun fault OOD ha tre posizioni distinte fra otto e resta
puramente descrittivo. La matrice non è un quadrato latino: nessun bilanciamento fra colonne
è richiesto. La stessa assegnazione vale fra condizioni, riceventi, librerie e ripetizioni.

Sia Y_frj l'esito o il contrasto di interesse alla posizione j del run r (per P1 la media dei
sette riceventi, per P2 il proprietario). La media osservata per fault è
`hat_mu_f = (1/8) sum_r Y_fr,pi_f(r)` e
`E_pi[hat_mu_f | tutte le traiettorie] = (1/64) sum_r sum_j Y_frj`.
Questa è l'imparzialità **rispetto all'assegnazione** per la media finita run × posizione;
non è una garanzia sugli intervalli. Vale senza stazionarietà temporale, purché nessuna
finestra o run sia sostituito selettivamente. Per output LLM casuali la stessa identità vale
per le risposte potenziali/aspettative alla prima ripetizione, a regime del servizio fissato.

Per l'inferenza su **nuovi run**, la quantità è invece
`mu = (1/8) sum_f (1/8) sum_j E_run,LLM[Y_fj]`: media uniforme su fault e posizioni.
La media finita è stimata imparzialmente dal disegno, ma non si deve sostituire alla quantità
di superpopolazione nelle garanzie di §2–§4 senza dichiararlo.

Assunzioni aggiuntive esplicite per queste garanzie: traiettorie indipendenti e generate
con identica procedura **entro fault**; distribuzione non dipendente dall'identificativo
r a parità di fault/posizione; estrazione indipendente dagli esiti; librerie e configurazione
fissate; assenza di dipendenza condivisa fra run introdotta dal servizio LLM. Gli stream
separati sostengono, ma non dimostrano, queste assunzioni. Un seed congelato rende la
randomizzazione riproducibile, non dimostra indipendenza statistica. Canary e intercalazione
controllano parte del rischio di deriva, senza provarne l'assenza.

## 2. Appaiamento e H1/H2: quando Hoeffding resta valido

L'appaiamento del piano §§2.2, 3.2 e 6 è preservato: per ogni run si confrontano le stesse
finestre nelle condizioni, conservando insieme tutti i riceventi. Non si ricampionano le
sette righe come sette unità indipendenti; R=3 non triplica N. P1/P2 hanno N=64 cluster.

Condizionando alla permutazione congelata, i 64 contrasti di run D_fr sono indipendenti
sotto le assunzioni di §1, pur avendo distribuzioni diverse per posizione. Inoltre
`(1/64) sum_fr E[D_fr | pi] = (1/64) sum_fj mu_fj`, identico per ogni pi perché ogni posizione
compare una volta entro fault. Quindi la nulla sulla media uniforme coincide con la nulla
sulla media condizionale; Hoeffding per variabili indipendenti, non necessariamente identiche,
resta applicabile: `P(Dbar - mu >= t | pi) <= exp(-64*t*t/2)`.
La stessa disuguaglianza vale mediando su pi. H1/H2 mantengono alpha=0,05 e
`t=sqrt(2*ln(20)/64)=0,305968…`, senza assumere costanza della difficoltà nel tempo.

**Limite della conclusione:** se si considerano fisse le 64 traiettorie e casuale soltanto
l'assegnazione, i run nello stesso fault sono dipendenti per la permutazione senza
reinserimento. La prova a N=64 appena data non è una prova design-based per quella popolazione
finita. Né basta che i run siano indipendenti ma abbiano medie legate all'indice r: in quel
caso la media condizionale può dipendere da pi. La formulazione di superpopolazione e le
assunzioni di §1 devono entrare nel paper. In alternativa, trattare gli otto fault come
blocchi indipendenti consente un limite molto più debole (N=8, t≈0,8654), a permutazioni
indipendenti fra fault; non è la procedura confermata e non viene adottata tacitamente.

## 3. Bootstrap: non basta dire «conservativo»

Il bootstrap percentile del piano §6 pesca otto run con reinserimento entro fault. Mantiene
l'appaiamento, ma NON mantiene le quote per posizione. Non è il bootstrap esatto del nuovo
disegno. Stratificare ulteriormente per fault × posizione non risolve: c'è una sola
osservazione in ogni cella e il ricampionamento con quote esatte riproduce sempre il medesimo
campione, con varianza zero. Riassegnare nuove posizioni ai run osservati richiederebbe gli
esiti delle sette finestre non valutate e non è autorizzato. Pooling fra fault o modelli
additivi imporrebbero assunzioni nuove (per esempio assenza di interazione fault × tempo).

La differenza si vede algebricamente. Entro un fault, riordinati gli esiti per posizione,
si hanno X_j indipendenti con media mu_j e varianza sigma_j². Poniamo
`V = sum_j sigma_j² / n²` e `H = sum_j (mu_j - mu_bar)²`, n=8.
Per la varianza campionaria s² con denominatore n−1:

`E[s²/n] = V + H/[n(n−1)]`.

È un estimatore conservativo **in aspettativa della varianza** sotto queste assunzioni,
non una garanzia di copertura. Ma la varianza del bootstrap ordinario della media è
`V_boot = (n−1)*s²/n²`; dunque

`E[V_boot] = ((n−1)/n)*V + H/n²`.

Se H=0, è 7/8 della vera varianza; se le medie cambiano molto nel tempo, può invece
sovrastimarla. Quindi il percentile a n=8 non è garantito conservativo e non ha copertura
nominale dimostrata. La stessa derivazione si applica a ciascun contrasto medio di cluster;
non si estende automaticamente all'accuratezza condizionata ai non astenuti, che è un rapporto.

**Raccomandazione Q1:** conservare il bootstrap di §6 (10.000 repliche, seed e appaiamento
invariati) esclusivamente come intervallo descrittivo approssimato, dichiarando il limite;
affiancare per i contrasti medi limitati un intervallo bilaterale Hoeffding
`Dbar ± sqrt(2*ln(2/0,05)/64)` (intersecato con [−1,1]), sotto §1, senza usarlo per scegliere
post-hoc la procedura più favorevole. Il quantile bootstrap 5% non decide H1/H2/H3.
Alternativa Q1: sviluppare e validare prima del freeze un modello/ricampionamento che sfrutti
la struttura fault × tempo; non è giustificabile il semplice comando «preserva le quote».
La raccomandazione necessita accettazione come reporting aggiuntivo, non cambia m o alpha.

## 4. H3, margine e gerarchia: limite non eliminato

Il margine del piano §5 resta **m=0,125**, perdita media netta accettabile sui local-seen,
ora esplicitamente mediata uniformemente sulle posizioni. Non diventa una garanzia per ogni
fault/posizione. Non si ricalibra sui dati. La sensibilità alpha=0,025 resta pre-specificata.

Lo score di Tango di §§4.3–4.4 usa le 64 coppie binarie appaiate. L'appaiamento resta, ma
con una coppia per cella fault × posizione le probabilità di concordanza/discordanza possono
variare fra celle. I conteggi aggregati non hanno in generale il modello multinomiale IID
usato dalla verosimiglianza di Tango. L'indipendenza condizionale sufficiente per Hoeffding
non dimostra quindi il livello di Tango. Il piano §5 ammetteva già la limitazione dovuta
alle quote per fault; le quote per posizione la rendono più esplicita. I risultati di potenza
e livello simulati nel piano §7.1 non validano questo nuovo disegno eterogeneo.

**Q2 richiede l'autore.** Opzione A (raccomandata per continuità): mantenere Tango come
procedura approssimata, ma condizionare il freeze a una verifica sintetica indipendente,
pre-dati, del livello al bordo Δ3=−0,125 e della potenza, includendo eterogeneità fault ×
posizione e discordanza. La griglia, la tolleranza del livello e la regola in caso di esito
negativo vanno fissate prima della verifica; questo documento non autorizza quel lavoro e
non presume il suo esito. Non chiamare «garantito» il FWER completo.
Opzione B: sostituire H3 con il limite Hoeffding (nuova decisione, non attuata): rifiuto se
`Dbar3 + m >= sqrt(2*ln(20)/64)`, cioè `Dbar3 >= 0,180968…`. Dà livello ≤0,05 sotto §1,
ma richiede un miglioramento osservato di circa 18,1 punti per affermare non inferiorità:
è molto conservativo e perde potenza vicino a Δ3=0. A alpha=0,025 la soglia è circa 0,2145.
Non si adotta B dopo aver visto l'esito di A sul test.

La sequenza **H1→H2→H3** resta quella del piano §4.2. La prova del gatekeeping resta valida
se ogni test locale controlla il livello per la propria nulla. Con A, H1/H2 hanno la garanzia
condizionale sopra, H3 e FWER completo restano approssimati e da qualificare; con B, sotto §1,
la garanzia di livello riguarda l'intera sequenza. Nessun risultato del bootstrap modifica
l'ordine, alpha o il criterio di rifiuto. Sino alla decisione Q2/review: S6/S10/S11 PENDING.

## 5. D4, aggregatore e ambito: rinvii esatti e proposta Q3

Il piano §§3.3 e 10.3–10.4 mantiene la **prima ripetizione sempre primaria**, anche se
le altre due concordano contro di essa. L'audit deterministico del 10% del nucleo resta
quello di §10.4: solo in quella sensibilità le risposte dei prompt audit sono sostituite
dall'aggregazione; tutte le altre restano repetition 1. Nessuna chiamata aggiuntiva a R=3.

D4 completa l'aggregatore: tre risposte valide, voto sulla coppia (`abstain`, `predicted_label`),
almeno due identiche → tale esito; altrimenti astensione per disaccordo. L'astensione
maggioritaria del modello e quella indotta dall'aggregatore hanno cause distinte.

**Q3, raccomandazione da approvare:** aggiungere un reporting descrittivo separato su tutti
i prompt, disponibili a R=3, senza sostituire audit o primaria, senza nuovo test confermativo.
Per ciascun blocco/condizione riportare accuratezza, copertura, accuratezza sui non astenuti,
astensione del modello, astensione per disaccordo e invalidità aggregata. Non combinare i
blocchi in una singola popolazione nuova. Questa estensione richiede questo addendum a §10.4.
Alternativa: limitare la sensibilità all'audit già previsto, senza reporting aggregato globale.

**Meno di tre esiti validi, proposta comune alle due opzioni Q3:** dopo risoluzione di ogni
richiesta pendente, aggregato `invalid_incomplete_triplet`, anche se due risposte valide
concordano. Nessuna nuova chiamata per completare una risposta generata invalida. Non si
chiama astensione, non si vota una pseudolabel «errato» e non si usa repetition 1 come spareggio.
Si conserva il numero di risposte valide. L'aggregato invalido conta non corretto nel
denominatore totale e nel denominatore dei non astenuti, per coerenza con §3.3; resta
separato dalle due cause di astensione. Una richiesta ancora incerta/zero-token da recuperare
non è una invalidità terminale: la campagna resta sospesa, nessuna analisi finale selettiva.
Questa scelta evita di confrontare aggregatori con numeri diversi di votanti. Accettarla non
cambia la primaria; è una specificazione nuova della sensibilità da approvare prima del freeze.

La sensibilità canary di §10.5 resta distinta da entrambe: esclude le chiamate del giorno
marcato. La finestra fra ultimo PASS e canary fallito è riportata anche come maschera forense
separata (protocollo §6), senza sostituire implicitamente la maschera del piano.

## 6. Analisi temporale e limiti bibliografici

Curva per posizione: secondaria descrittiva, 56 valutazioni local-unseen per condizione ma
solo 8 run fisici indipendenti, uno per fault. Non è una curva longitudinale entro run, non
stima il ritardo di rilevazione e non consente una stima affidabile dell'interazione fault ×
posizione. Per le celle OOD le posizioni sono solo tre, senza copertura completa.

Gli appoggi e limiti in D1 restano quelli dell'autore: Downs & Vogel, tabella 8 (24–48 h,
non finestra da 5 h); Kaur/CODiT (una finestra per traiettoria, non garanzia conformal per
questo test); RBC-AD (finestre campionate vs flusso completo, non sufficienza di una finestra).
Rinvii: `docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md` C1;
`papers/RBC-AD-_conformal_anomaly_detection_with_explicit_false-alarm_control_for_the_Tennessee_Eastman_Process.md`,
introduzione; fonti Downs & Vogel già citate nel piano. La self-consistency di Wang et al.,
ICLR 2023, sostiene il voto su risposte campionate in altri compiti, non una garanzia TEP
né la scelta della prima in caso di disaccordo. Non è stata avviata ricerca online: mandato offline.

## 7. Esito della verifica documentale

Preservati: un caso per run, appaiamento, numerosità, primaria repetition 1, m, alpha e ordine.
Verificato con condizioni esplicite: H1/H2 Hoeffding per la media di superpopolazione.
Non dimostrati: copertura del percentile bootstrap, livello di Tango sotto il nuovo disegno,
indipendenza reale del servizio, potenza aggiornata. Q1–Q3 sono proposte, non autorizzazioni.
Il piano congelato e gli artefatti DESIGN_RESOLUTION restano byte-identici.
