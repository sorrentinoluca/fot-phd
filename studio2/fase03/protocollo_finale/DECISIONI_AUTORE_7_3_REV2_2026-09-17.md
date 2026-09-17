# Decisioni dell'autore per il protocollo finale rev2 — 2026-09-17

Autore: Luca. Raccolte dalla finestra di orchestrazione dopo le due review 7.3-R del candidato
`e0db132` (`VERIFICA_PROTOCOLLO_FINALE.md` `d0fe9d31…`, `VERIFICA_PROTOCOLLO_FINALE_claude.md`
`2719650d…`) e il report 7.4-PREP (`9e0e086`). Prese **prima** di aprire i dati di test e prima
di qualunque chiamata del batch. Le motivazioni fanno parte della decisione e vanno riportate nel
protocollo e nei metodi del paper.

## D1 — Una finestra per run, assegnazione casuale bilanciata per fault

**Decisione.** Ogni run del lotto test 03.11 contribuisce **un solo caso**: una delle otto
finestre utili da 5 h. Per ciascun fault (e per `Normal`), le otto posizioni temporali sono
assegnate agli otto run con una **permutazione casuale**, riproducibile con seme congelato,
costruita sui **soli identificativi** dei run prima di osservare segnali o evidence di test.
L'assegnazione è identica fra condizioni (A, B-LF, E-LF, B-noLF), riceventi, libreria (`G_P`,
`G_A`) e ripetizioni. Per i fault OOD (3 run ciascuno): tre posizioni distinte estratte dallo
stesso generatore, con la stessa regola.

**Nome.** «Assegnazione casuale bilanciata per posizione, separatamente per fault». Non si chiama
quadrato latino a meno che il bilanciamento valga anche per colonna (fault × indice di run): non è
richiesto.

**Motivazione.**
- Budget: tutte le otto finestre portano il solo nucleo a ~41.000 chiamate (≈377 h con il 20 %)
  contro W = 168 h. Due finestre per run passano (≈106 h alla media, ≈148 h al p95) ma lasciano
  ~20 h di margine, e il p95 delle singole chiamate non è il p95 della durata della campagna.
- Quantità stimata: assegnando a caso le otto posizioni agli otto run di un fault, ogni run ha
  probabilità 1/8 di ricevere ciascuna finestra; mediando sulle assegnazioni possibili, la media
  osservata stima la **media uniforme delle otto posizioni temporali** degli otto run. Vale anche
  se le finestre hanno difficoltà diverse: non si assume che il guasto sia stazionario. Condizioni:
  assegnazione indipendente dai risultati; finestre mancanti o run interrotti **non sostituiti
  selettivamente**.
- Nessun intervallo temporale è privilegiato (una «finestra 1 per tutti» misurerebbe solo l'esordio
  del guasto).

**Conseguenze sul piano 03.8 (da verificare, non da assumere).** Restano un caso per run, lo
stesso numero di cluster e l'appaiamento fra condizioni. Ma la regola di campionamento diventa
parte del disegno: l'endpoint va dichiarato come media uniforme sulle otto posizioni, e il metodo
degli intervalli (bootstrap a cluster) va verificato rispetto al campionamento bilanciato senza
reinserimento. Integrazione esplicita come **nuova revisione tracciata / addendum** del piano
statistico, mai modifica in luogo.

**Analisi temporale.** Curva accuratezza-per-posizione: **secondaria e descrittiva**. Per posizione
e condizione ci sono 56 valutazioni local-unseen (8 fault × 7 riceventi) ma provenienti da **otto
run fisici**, con una sola osservazione run-finestra per fault: le sette valutazioni dello stesso
run condividono l'evidenza. Non separa la variabilità fra run dall'evoluzione temporale del
singolo fault. Un secondo schema di assegnazione (due finestre per run) si introduce solo se
l'evoluzione temporale diventa domanda centrale, con revisione preventiva del piano; due finestre
aumentano la copertura, non necessariamente la potenza (restano 64 run fault indipendenti; il
guadagno dipende dalla correlazione fra finestre).

**Appoggi in letteratura, con i loro limiti.**
- Downs & Vogel (tabella 8): 24–48 h per osservare gli effetti dei disturbi → orizzonte lungo. Non
  giustifica finestre da 5 h, il bilanciamento né l'equivalenza diagnostica fra posizioni.
- Kaur/CODiT (vedi `docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md`, r. 170): una
  finestra per traiettoria per non trattare finestre della stessa traiettoria come repliche
  indipendenti. Non trasferisce garanzie conformal al nostro test; il bilanciamento senza
  reinserimento richiede una giustificazione inferenziale propria.
- RBC-AD (`papers/RBC-AD-…Tennessee_Eastman_Process.md`, r. 115): distinguere valutazione su
  finestre campionate e sull'intero flusso → dichiarare esattamente quale prestazione si misura.
  Non dimostra che una finestra per run sia sufficiente.

**Testo per il paper (bozza dell'autore).**
> Per stimare la prestazione media lungo l'orizzonte post-guasto entro il budget computazionale
> disponibile, abbiamo selezionato una finestra per run mediante assegnazione casuale bilanciata
> sulle otto posizioni temporali, separatamente per fault. L'assegnazione è stata congelata prima
> dell'ispezione dei dati di test e mantenuta identica fra condizioni e riceventi. Il disegno non
> valuta il monitoraggio continuo né il ritardo di rilevazione; le analisi per posizione temporale
> sono descrittive.

Da presentare come scelta trasparente per stimare una quantità definita, senza attribuire alla
letteratura una validazione specifica che non offre.

## D2 — Condizione `B-noLF`

Token `B-noLF` = B con `G_P`, senza il blocco di politica local-first. Implementata come **file
nuovo / nuova revisione tracciata** del renderer; `protocol.py` congelato (`791fa347…`) non si
modifica in luogo. Lo SHA della schedule di 7.4-PREP non cambia per il token.

## D3 — Retry e STOP nel batch finale

| Esito | Regola |
| --- | --- |
| Errore tecnico **con prova** che non è avvenuta generazione | Retry ammesso entro quota |
| Timeout senza prova di mancata generazione | Sospendere e riconciliare; nessun reinvio automatico |
| Risposta generata ma invalida o troncata | Registrare il fallimento; nessuna rigenerazione |
| Risposta valida ma errata o astenuta | Esito scientifico definitivo |

«Zero token» = zero token **generati**, ragionamento incluso, con evidenza collegata alla
richiesta. Risposta vuota, contatore mancante o timeout **non** bastano. Coerente con
`piano_statistico/DECISIONI_AUTORE_03_8_bozza.md` (r. 433).

**Motivazione.** Il retry non deve diventare una seconda possibilità concessa selettivamente al
modello: rigenerare risposte malformate, troncate o insoddisfacenti fino a ottenerne una valida
misurerebbe un sistema con recupero selettivo, alterando costi e confrontabilità fra condizioni.
All'opposto, con `Q=0` assoluto i fallimenti di trasporto pre-generazione (8/156 nel pilot)
entrerebbero come «non corretti» senza ragione scientifica.

**STOP operativo.** Cinque tentativi tecnici consecutivi falliti **sullo stesso servizio**, retry
inclusi; attesa crescente fra tentativi; limite cumulativo dei retry separato; contatore
**persistente** (non si azzera riavviando); STOP = sospensione della campagna con risultati e
richieste pendenti conservati. Il 5 è una protezione da servizio indisponibile, senza significato
statistico. Errori permanenti, cambio d'identità del modello o consumo incerto → **STOP
immediato**. Vale per il batch finale; non estende i retry agli stadi che già li vietano.

## D4 — Uso delle tre ripetizioni

- **Primario: sempre la ripetizione 1**, anche quando le altre due concordano contro di lei
  (`DECISIONI_AUTORE_03_8_bozza.md`, r. 71). La maggioranza serve solo alla sensibilità.
- **Aggregatore di sensibilità: maggioranza 2 su 3, altrimenti astensione per disaccordo.**

| Tre esiti validi | Esito aggregato |
| --- | --- |
| F1, F1, F8 | F1 |
| F1, F8, F13 | Astensione per disaccordo |
| F1, F8, astensione | Astensione per disaccordo |
| Astensione, astensione, F1 | Astensione per maggioranza |

Registrare separatamente: astensione del modello, astensione per disaccordo, output invalido.
Nell'accuratezza primaria l'astensione resta non corretta; si riportano anche copertura e
accuratezza sui non astenuti, per rendere visibile il costo della scelta.

**Motivazione.** La self-consistency (Wang et al., ICLR 2023) sostiene l'aggregazione di risposte
campionate, su ragionamento aritmetico e commonsense, non sulla diagnosi TEP; non stabilisce che la
prima risposta sia più affidabile quando tutte discordano. «Vale la prima» sarebbe ammissibile se
pre-specificata, ma trasforma un disaccordo completo in una diagnosi senza consenso.

**Da verificare in rev2.** Il candidato applica la sensibilità al solo sottoinsieme audit del 10 %
(§10.4 del piano). Con R=3 su tutto lo studio, valutare se riportarla anche su tutti i prompt come
analisi descrittiva aggiuntiva dichiarata prima dei dati; va trattato il caso con ripetizioni
invalide (meno di tre esiti validi).

## D5 — Già registrate (richiamo)

`SWAP4` = F1/F8/F10/F13; librerie del pilot riusate a 0 chiamate con asimmetria di template
dichiarata (verbale 7.2-R `fce3b955…`, commit `f0d0393`); E5 (§8.12) fuori dal protocollo, da
eseguire dopo il batch come studio aggiuntivo con freeze proprio.
