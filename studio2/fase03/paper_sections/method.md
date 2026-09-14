# Method: Federation over Text for class-disjoint fault diagnosis

## Problem setting

Consideriamo otto agenti logici che osservano lo stesso processo simulato ma possiedono esperienza
locale disgiunta: ciascun agente conosce il funzionamento Normal e una sola classe di fault. La
classe corretta di un caso remoto non è stata osservata localmente dal ricevente; il compito è
scegliere fra le otto etichette opache di fault, l'etichetta letterale `Normal` oppure astenersi con
`Unknown` (`abstain=true`, `predicted_label=null`).
[Fonte: piano §8.1, §8.5–§8.6; 03.7 `SPECIFICA_PSEUDOLABEL.md`]

Gli agenti sono processi logici, non nodi distribuiti su una rete reale. Le osservazioni grezze,
gli esempi locali e le feature per finestra non vengono trasferiti fra agenti nel protocollo FoT;
ogni ricevente ottiene invece record di conoscenza prodotti dai pari. Questa proprietà descrive il
flusso informativo, ma non costituisce una garanzia di privacy.
[Fonte: piano §5 G3/G7, §12.8; `docs/letteratura.md` §14.2, §14.6]

## Oggetto federato e ciclo a colpo singolo

Ogni owner usa evidence di sviluppo per produrre due insight relativi alla propria classe fault
locale. La libreria omogenea contiene sedici record per le sole otto classi fault; `Normal` non ha
insight. Un ricevente vede i quattordici record dei sette peer, mentre i propri due record restano
esclusi. Gli insight sono prodotti una volta, congelati e riutilizzati: non vi sono aggregazione
lato server, aggiornamento di parametri o raffinamento multi-round.
[Fonte: piano §8.1, §8.4, §8.9; 03.12 `DECISIONE_SCHEMA_INSIGHT.md`]

L'assenza di aggregazione è una scelta di perimetro. Mantiene origine e contenuto di ciascun record
ispezionabili e evita di introdurre un ulteriore fattore sperimentale; non dimostra che sintesi,
selezione o round multipli siano inefficaci in altri compiti.
[Fonte: piano §12.8; P031/FedTextGrad e P041/Fed-ICL in `docs/letteratura.md` §14.2]

## Condizioni informative

Nella condizione A il ricevente usa soltanto esempi e conoscenza locali. Nella condizione B-LF usa
la stessa conoscenza locale più i record corretti dei peer. Nella condizione E-LF riceve lo stesso
insieme di record di B-LF, ma l'associazione fra pattern e pseudolabel è corrotta mediante un
derangement evaluator-side. `Unknown` è disponibile in tutte le condizioni e conta come astensione,
non come label o classe; la nona e ultima label dello spazio è `Normal`.
[Fonte: piano §8.1, §8.5–§8.6; 03.7 `SPECIFICA_PSEUDOLABEL.md` §5]

B-LF ed E-LF condividono la politica local-first: prima di usare gli insight peer, il reasoner deve
verificare se l'evidence corrisponde in modo convincente alla propria classe locale. La politica è
parte del metodo maturo e viene tenuta costante nel contrasto B-LF−E-LF; l'ablazione senza local-first
è separata e descrittiva.
[Fonte: piano §8.2–§8.3, §8.5]

## Pseudolabel opache e controllo E

Le otto etichette di fault sono stringhe opache derivate deterministicamente con SHA-256 e assegnate
in biiezione agli agenti; `Normal` resta letterale e occupa la nona posizione dello spazio delle
label. La mappa verso le identità fisiche resta evaluator-side. Per ogni agente, E usa una
permutazione senza punti fissi e biiettiva delle sole etichette fault dei peer. Il sorteggio è
riproducibile da namespace e seed, ma ciò non prova segretezza o indipendenza statistica.
[Fonte: 03.7 `SPECIFICA_PSEUDOLABEL.md` §3–§7; `REPORT_PSEUDOLABEL.md`]

L'applicazione di E avviene dopo il filtraggio peer. Il validatore costruisce il byte atteso
modificando soltanto il valore `pseudolabel`, rifiuta cambi di ordine o whitespace e registra hash e
offset differenti. In questo modo il contrasto cambia l'associazione semantica lasciando invariati
schema, narrativa, provenienza e cardinalità.
[Fonte: piano §8.9; 03.12 `DECISIONE_SCHEMA_INSIGHT.md`, blocco «Anti-leakage ed E»]

## Schema degli insight e parità fra producer

Ogni insight contiene sei campi obbligatori: `insight_id`, `source_agent`, `pseudolabel`,
`evidence_scope`, `variable_ids` e `observed_pattern`. I primi cinque provengono dal percorso
deterministico e sono confrontati con un manifest fidato; il producer può scrivere soltanto la
narrativa `observed_pattern`. Proprietà ulteriori e riparazioni silenziose sono vietate.
[Fonte: 03.12 `DECISIONE_SCHEMA_INSIGHT.md`; S12 `insight_v1.schema.json` a `3c64390bc4dd58c48cc4e1e388a38989b32b3143`]

Lo schema impone cardinalità fissa, cap per campo e per record, identificatori di variabile
letterali e serializzazione canonica. Lo stesso contratto vale per producer principale e
alternativo. Validità al primo tentativo, retry, troncamenti e token vengono registrati per producer
e condizione; tali misure descrivono la conformità operativa, non la correttezza scientifica della
narrativa.
[Fonte: piano §8.4, §8.7, §8.9; 03.12 `DECISIONE_SCHEMA_INSIGHT.md`]

Il braccio producer-swap sostituisce l'intera libreria del producer principale con una libreria
completa del producer alternativo, mantenendo consumer, test, schema, numero di record e cap. Una
libreria mista confonderebbe identità del producer e composizione del prompt e non viene usata.
[Fonte: piano §8.4]

Q8 indica il disegno comune con otto agenti e otto fault, non l'identità del modello.
[Fonte: piano §8.1]

> **VARIANTE D9 — stato aperto, inventario al 14 settembre 2026.** Il servizio 122B è
> dichiarato operativo dall'autore, alias API `qwen3.5-122b`, contesto 131.072 e output
> massimo 16.384; il parametro temperatura va omesso secondo la comunicazione ricevuta.
> Il 27B resta sull'altro server. Identità completa di pesi/revisione/quantizzazione,
> tokenizer/template, serving, capienza e qualificazione del servizio restano da verificare.
> Questi dati comunicati non assegnano ruoli sperimentali a 27B, 122B o Terra. Il 2.4T
> risulta non ospitabile dalla macchina; le opzioni storiche sotto non sono rami attivati.
> `[DECISIONE: D9, producer principale, consumer, producer alternativo e configurazione]`.
> Il producer-swap resta nel disegno e la decisione sull'alternativo D9.1 resta mancante.
> I risultati storici Terra non costituiscono un braccio controllato dello studio 2.
>
> [Fonte: H §§4.9, 5, impronta in `FONTI_DELTA_0315.json`; piano D9; S08-consegna `CONSEGNA_REV10.md`]

> **VARIANTE D9.1 — Qwen-2.4T.** Se disponibile e promosso dal pilot entro la data prevista,
> Qwen-2.4T è producer principale e consumer. Il braccio producer-swap resta nel disegno; D9 non
> nomina il producer alternativo per questo ramo. `[DECISIONE: esito del gate, versione/API e
> producer alternativo del ramo D9.1]`.
>
> [Fonte: piano §8.4, §8.10 punto 3 e D9 opzione 1]

> **VARIANTE D9.2 — opzione storica Qwen-27B + Terra.** Il piano prevede, solo se
> l'autore attiva questo ramo e dopo pilot positivo, Qwen-27B come producer principale
> e consumer e Terra come producer alternativo nel solo swap. Qwen-27B non è un modello
> «nuovo». Il pilot 03.13 non è avviato; la disponibilità dichiarata del 122B richiede
> una decisione D9 esplicita e non sostituisce automaticamente il candidato storico.
>
> [Fonte: piano D9 opzione 2; H §§4.9, 5]

> **VARIANTE D9.3 — arresto dell'espansione.** Se Qwen-27B fallisce i criteri operativi, l'autore
> sceglie fra Terra-only e una submission successiva. L'eventuale Terra-only usa il medesimo metodo,
> non è presentato come replica cross-model e non eredita automaticamente un producer alternativo.
>
> [Fonte: piano D9 opzione 3; prompt 03.15]
