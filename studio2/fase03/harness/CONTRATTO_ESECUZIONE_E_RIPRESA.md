# Contratto eseguibile R01–R10 — D02 / R04 / R08

15 settembre 2026. Implementazione offline da sottoporre a nuova verifica indipendente.
Questo documento descrive il delta successivo al quarto NON OK (edb37f3): non ne cambia il verdetto.
D01 originario e C02/C03 risultano chiusi nella review acquisita. D02 riguarda l’autenticazione
delle prove durevoli e della copertura dei predecessori che conservano PASS/COMPLETED.
La formulazione precedente su N48 era errata: il piano rev.10 §§11–11.1 richiede le invalidità di trasporto in T3/T6.
La specifica e i report del candidato 59b6b93 restano storia, incluse le formulazioni D9
superate. La decisione D9 del record aaba893 è già acquisita (122B producer principale
 e consumer; 27B producer alternativo completo; Terra storico interno); il suo
recepimento eseguibile resta un delta successivo. Il preflight storico rimane
UNDECIDED/SUSPENDED e viene rifiutato. Nessuna approvazione reale è aggiunta.

## Barriere e sorgenti

Ogni ingresso di trasporto consumer, inclusi Provider e server_contract, esige una
configurazione APPROVED_FOR_PHASE03_EXECUTION con study_model_decision=APPROVED e un
record locale di approvazione dei contenuti esatti. Il record execution_authorization
ha path e sha256; i byte referenziati contengono author, decision=accepted e
configuration_sha256 del JSON canonico della configurazione senza quel riferimento.
Sono campi di un futuro contratto di esecuzione, non configurazioni approvate oggi.
L'approvazione copre anche pilot_ledger (path assoluto condiviso e pilot_id), pin tokenizer,
expected_response e configurazioni producer ammesse. Cambiare directory dei risultati
non cambia il ledger; una diversa coordinata del ledger viene rifiutata.

Il producer richiede un provider separato e improntato nell'approvazione; non eredita un
modello dal preflight. Tokenizer e template vengono verificati prima del conteggio,
R4 prima del trasporto; i controlli sono ripetuti lungo il ciclo producer. Il fallback
dal chat template al conteggio di testo senza template è rimosso. La qualifica del
contatore e della capienza reale resta futura, distinta dai contatori stub dei test.

Il builder confronta i byte 03.7 con pin costanti e tutti i JSON evidence con il manifest
03.6 prima dell'estrazione. L'inventario producer è confrontato con l'inventario development
improntato del candidato originale; i pin 03.7 e Normal vengono verificati anche dal
consumer di quell'inventario. Non occorre una libreria insight per la conformità.

Una libreria valida viene ricostruita dai raw persistiti del ciclo producer attivo,
con confronto di pilot, stadio, binding e record, e nuova validazione R4. Una dichiarazione
validated=true, anche con hash ricalcolati, non la sostituisce. L'avvio di una remediation
invalida l'handoff del ciclo iniziale. La preparazione ordinaria verifica sorgenti,
libreria e approvazione label, poi usa il renderer R4. Il caricamento prepared verifica
anche il manifest sorgente e rigenera i prompt dalle fonti per confrontarne i contenuti.
label_space resta nell'ordine canonico evaluator-side; l'ordine 1a è soltanto prompt-facing.
L'ordine 1a reale rimane pending. Le approvazioni nei test sono soltanto fixture.

## Ledger e transizioni

Il formato SQLite v2 appartiene a un solo pilot. Le richieste sono definite in un piano
immutabile per stadio: logical_id, modello/producer, prompt, caso, contratto, condizione,
gruppo e ripetizione. stage_run è l'hash canonico del piano, non un nuovo spazio di quota.
La riserva di un originale segue l'ordine del piano e resta unica tra processi e riavvii.
Un retry conserva tutta l'identità dell'originale: può partire soltanto dall'ultima foglia
con prova zero-token e non può creare rami concorrenti. Le triplette sonda richiedono tre
originali distinti dello stesso gruppo e condizioni A/B-LF/E-LF corrispondenti.

BEGIN IMMEDIATE racchiude verifica dei prerequisiti, dei contatori e transizione. Un esito
PASS producer/sonda richiede copertura completa, foglie COMPLETED, raw/record persistiti,
identità verificata e controlli specifici. Una conformità richiede otto coppie R4 valide;
la sonda seleziona la prima tripletta riuscita. FAILED e ZERO_TOKEN_PROVEN senza recupero
non soddisfano queste conformità. Il gate usa invece tutti i 120 primi tentativi:
una risposta autenticata o un evento durevole di invalidità di trasporto per ciascuno;
T3/T4/T6 determinano l'esito tecnico. Nessuna invalidità viene contata come risposta valida.

L'alternativo è opzionale prima del binding; una volta definito il suo piano, deve chiudere
PASS prima di sonda/gate. Il controllo vale nella stessa transazione di binding, riserva
ed esito. Un alternativo soltanto definito, incompleto, FAILED, ZERO_TOKEN_PROVEN o chiuso
FAIL non può essere ignorato. Nessun abbandono implicito è previsto. Gli eventi normativi non sono inseribili tramite record_event pubblico (solo note:).
Gli stadi chiusi non accettano nuove richieste; una replica identica dell'esito consente di
rigenerare file derivati dopo un crash, senza nuova transizione o nuovo invio.

Quote mantenute: una remediation completa di otto; 8r+t≤15; oltre sette trasporti solo con
rinuncia esplicita alla remediation e mai per la sonda; massimo due triplette sonda se la
quota è intatta; zero retry gate; 152/160 pianificati; 200 hard stop distinto. Gli intenti
restano conteggiati anche quando non si può stabilire se il provider abbia ricevuto l'invio.
Non si deduce una disponibilità ulteriore dalla soglia 200.

## Riconferma degli esiti dopo restart — D01

La validità della catena dei predecessori vale anche per uno stadio già chiuso.
`_prerequisites` controlla sospensione, autorizzazione della remediation, conformità
alternativa avviata e successo del producer attivo/sonda. `_successful` applica lo stesso
controllo ricorsivo quando il risultato viene riutilizzato. `_ready` aggiunge soltanto i
vincoli propri delle nuove transizioni: stadio aperto e divieto di ritornare a uno stadio
precedente dopo l'avvio dei successori.

Questa distinzione consente di rileggere un producer valido o rigenerare la sonda dopo
che il gate è già concluso, senza riaprire richieste o autorizzare nuovi invii. Non basta
che binding o hash dell'outcome coincidano: `bind_stage` su un piano esistente ricontrolla
i prerequisiti; il replay di `record_stage_outcome` ricontrolla prerequisiti, copertura,
record durevoli e criteri dell'esito prima di ritornare, senza inserire nuovi eventi.
Per la sonda PASS verifica anche che il freeze riproposto coincida con quello registrato.

`verify_stage_success` e `authenticate_frozen` verificano l'intera catena dentro una sola
transazione `BEGIN IMMEDIATE`, così uno scrittore concorrente non può cambiare lo stato
fra due letture. L'autenticazione del freeze richiede il successo conforme della sonda;
l'identità dei byte da sola non attesta la precedenza del producer alternativo.

Un ledger v2 creato dal vecchio 0c8157f, con sonda/gate PASS ma alternativo bound, INTENT,
FAILED, ZERO_TOKEN_PROVEN, completo senza outcome o FAIL, viene quindi rifiutato negli
ingressi di conferma. I runner/CLI sonda e gate lo rifiutano prima di interrogare il server
e prima di rigenerare journal o riepiloghi. Gli eventi storici non sono cancellati o
riscritti. `event`, `binding`, `request`, `stage_records` e `snapshot` restano letture
forensi: estrarre un dato non equivale a confermarne la validità normativa.

Il replay di una catena valida, anche storica, resta disponibile; conserva contatori,
raw e invalidità C02. Nessuna migrazione di schema o riscrittura automatica degli esiti.
Le prove generano ledger storici con il codice esatto 0c8157f in processi separati;
nessun SQL alterato viene usato per costruire il difetto di precedenza.

## Prove durevoli dei predecessori — D02

`_successful` non si limita ai flag: applica `_closed_outcome` a ciascun predecessore.
`_validate_outcome` è il validatore unico per nuova chiusura e riconferma: rilegge il
binding, la copertura delle basi nell’ordine previsto, tutti i tentativi e le catene di
retry, gli hash raw/record, l’identità dei record e i criteri di PASS dello stadio.
L’artefatto di chiusura deve coincidere con la propria impronta e con il digest dei record
attuali; anche `records_sha256` nell’evento deve corrispondere. Per la sonda si autenticano
i byte del freeze persistito e la prima tripletta riuscita. Rimane legittimo fermarsi al
primo gruppo riuscito di un piano a 3/6/9 richieste; eliminare un gruppo dopo la chiusura
non può essere legittimato da un conteggio ancora ammesso.

Il retry conserva identità, collegamento all’originale e prova zero-token registrata;
nessun tentativo orfano può sparire dalla verifica delle foglie. La riconferma di un
binding già chiuso verifica anche il proprio esito, oltre ai predecessori. FAIL/BLOCKED
possono essere riletti con gli stessi requisiti della loro chiusura, senza promozione a
PASS. Le 120 invalidità C02 rimangono record di tentativi, mai risposte inventate.

Tutti questi controlli usano la connessione e il `BEGIN IMMEDIATE` dell’ingresso;
nessuna connessione separata e nessuna cache valida fra transazioni. Il lock comprende
anche la lettura effettiva dei raw dei predecessori. Le letture forensi e la storia
rimangono disponibili; non vengono riparati dati, riscritti hash o azzerati contatori.

Le regressioni D02 iniettano guasti SQL espliciti in copie sacrificabili dopo una catena
valida: raw/record alterati, dati assenti, artefatti incoerenti, copertura ridotta e prova
di retry perduta. Non sono la costruzione di D01 né input scientifici. Non si rivendica
resistenza contro chi riscrive coerentemente l’intero database e tutte le impronte.

## Persistenza e punti di crash

SQLite con synchronous=FULL conserva l'intento prima del trasporto. Al ritorno dal trasporto,
il primo passaggio durevole salva la rappresentazione JSON restituita dall'SDK, con hash,
ora di ricezione e latenza misurata. Non si inventano metadati mancanti del provider. La
valutazione e il suo hash vengono salvati prima di proseguire; l'eventuale sospensione per
identità è atomica con il record e conserva consumo e raw. I journal JSONL sono proiezioni
aggiornate durante lo stadio, con fsync e sostituzione atomica; SQLite è la fonte autorevole.
Gli errori di trasporto conservano tipo, messaggio, latenza e intento, senza fabbricare raw.

| Punto del crash | Ripresa esplicita |
| --- | --- |
| Prima dell'intento | Nessuna richiesta registrata; il piano immutabile identifica il prossimo originale. |
| Dopo l'intento, prima/durante il trasporto | Esito incerto: nessun reinvio automatico. |
| Provider ha risposto, prima della persistenza del raw | La finestra non è transazionabile col servizio esterno. L'intento resta incerto; non si pretende di recuperare byte mai ricevuti su disco. |
| Raw persistito, valutazione non registrata | --resume rilegge e valuta gli stessi raw senza trasporto. |
| Esito della richiesta registrato | --resume salta quella richiesta e conserva contatori e identità. |
| Stadio chiuso, file finale assente | --resume rigenera la proiezione dai record durevoli; nessun nuovo invio. |

Un timeout interrompe il producer. Nella sonda si completano soltanto gli altri originali
della tripletta già pianificata; nessun retry né gruppo successivo automatico.
Nel gate, un'eccezione osservata dal trasporto viene registrata atomicamente con stato
FAILED ed evento `transport_invalidity:<request_id>`: tipo/messaggio, latenza, identità
della richiesta e metadati del campione congelato. L'evento conserva un record valutabile
come INVALID; non inserisce righe nella tabella responses. Raw, returned_model, fingerprint,
response_id e token restano null; identity_valid è null, non true. Le quote contano il
primo tentativo; la riserva retry non viene usata. Gli altri originali proseguono fino a 120.
Una failure preventiva delle barriere HarnessError e un crash BaseException non vengono
riclassificati come errori del modello: fermano il percorso. Una risposta con identità
mancante/errata resta una risposta ricevuta e sospende il pilot, con raw conservato.

Con un solo timeout e 119 risposte valide il denominatore è 120, T3=119/120 e la tripletta
mista è divergente (R3 pending fattibilità). Tre invalidità sullo stesso prompt impediscono
T6 valutabile; sette invalidità portano T3 sotto 114/120. Il raccordo metriche qualificato
resta intatto. Il journal espone separatamente request, response e transport_invalidity.
Un crash dopo il commit dell'invalidità ma prima del journal viene ripreso senza reinvio;
un INTENT senza risposta né osservazione durevole resta bloccato fino alla riconciliazione.

## Riconciliazione e retry espliciti

La riconciliazione zero-token acquisisce file evidence e approval dentro l'evento SQLite,
con hash e stato precedente. Evidence richiede request_id, request_identity_sha256,
provider_request_id, provider_evidence, disposition=not_generated e tutti e tre i contatori
prompt_tokens/completion_tokens/total_tokens esplicitamente zero. Approval deve indicare
author, decision=accepted e l'hash dei byte evidence. Un hash senza quei contenuti, un
originale diverso, token positivi o un raw già presente vengono rifiutati. Sono evidenze
esterne da acquisire realmente: un operatore non può attestare un esito mancante per comodità.
Il codice controlla struttura e collegamenti del record locale; non dispone di una firma
crittografica del provider e non ne fabbrica una. La revisione della prova resta necessaria.

Comandi locali, senza trasporto:

```text
python -m studio2.fase03.harness.ledger_cli --ledger /PERCORSO/CONDIVISO/pilot.sqlite3 --pilot-id ID status
python -m studio2.fase03.harness.ledger_cli --ledger /PERCORSO/CONDIVISO/pilot.sqlite3 --pilot-id ID reconcile-zero-token --request-id ID_RICHIESTA --evidence PROVA.json --approval APPROVAZIONE.json
python -m studio2.fase03.harness.ledger_cli --ledger /PERCORSO/CONDIVISO/pilot.sqlite3 --pilot-id ID authorize-remediation --diff DIFF.txt --template TEMPLATE.txt --approval APPROVAZIONE.json
```

Dopo riconciliazione, i runner richiedono --resume e --retry-request per gli originali
esplicitamente selezionati. La sonda richiede esattamente tre selezioni compatibili e riserva
la tripletta atomicamente. Il gate non accetta retry: una prova zero-token per un INTENT
senza risposta crea il record INVALID e consente --resume verso i soli originali ancora
non tentati. Una prova successiva a un timeout già registrato conserva byte e hash del
record INVALID originale e aggiunge l'evento di riconciliazione separato; non lo elimina
dal denominatore e non invalida il riepilogo già materializzato. Un retry nuovamente fallito richiede
nuova prova riferita a quel tentativo, non riuso dell'originale. --resume da solo non autorizza
mai un reinvio incerto. La sospensione per cambio d'identità non ha uno sblocco automatico.

I ledger del primo candidato 59b6b93 sono conservati e rifiutati come input v2: non esiste una
migrazione automatica che possa azzerare contatori o trasformare vecchi PASS non affidabili.
Una migrazione di un ledger realmente usato richiede un delta e una riconciliazione verificati;
nessun ledger reale è migrato in questo incarico. Lo schema v2 resta invariato: il delta
aggiunge eventi, non colonne e non migra dati preesistenti. Un FAILED v2 precedente senza
evento di invalidità non viene riclassificato automaticamente da --resume; occorre la
riconciliazione esplicita prevista, come per l'INTENT incerto. Un outcome di un candidato
precedente non viene riscritto automaticamente: se il nuovo artefatto differisce dal suo
hash registrato, il replay è rifiutato. Non si correggono in-place i riepiloghi della review
né stadi storici chiusi violando la precedenza dell'alternativo.

Il riepilogo producer v4 distingue provider_requests (tutti gli intenti dello stadio,
compresi errori e retry, come il contatore conservativo SQLite) da evaluable_calls (le otto
foglie valutabili T9) e valid_first_attempts. Dopo un timeout provato zero-token e un retry:
9 richieste, 8 coppie valutabili, 16 insight. Le cifre sono cumulative dello stadio, non del
singolo processo; la rigenerazione del riepilogo non le azzera. Nel caso di crash prima
dell'invio, il contatore conserva l'intento e non pretende di provare la ricezione remota.

## Remediation e sonda → gate

La diagnosi deve appartenere a structure/identifiers/cap/leakage e corrispondere a un difetto
registrato della conformità. Un timeout irrisolto non è una diagnosi del prompt. L'approvazione
lega diff unificato concreto (nomi before/after), byte del template, diagnosi e hash del piano
iniziale. Il nuovo piano conserva otto identità di caso, contratti, provider e tutte le
proprietà diverse dal template. La copertura non può essere ottenuta replicando un caso.

Il risultato sonda autentica la configurazione conservata nel ledger. Il gate confronta sia
l'oggetto con quel riferimento sia i byte esatti della serializzazione congelata; confronta
configurazione approvata, prompt, piano, schema, identità server e budget. Cambiare e ricalcolare
l'hash del file non basta. Le triplette gate devono corrispondere al campione congelato: 40
prompt distinti, 8 agenti, per agente 3 matched_transfer e 2 context_stress, distribuzione
8/16/16, ripetizioni esatte {1,2,3}, 120 request_id distinti, identità/hash/condizione coerenti.
T3/T4/T6 rimangono separati; divergenza semantica richiede R3 pending fattibilità. Nessun GO
finale è prodotto dall'evaluatore offline.

## Confine delle prove

Le fixture in offline_fixtures.py, test_revisions.py e non_ok_20260915/evidence/fixtures/
sono sacrificabili. Le prove eseguono stub e contatori token fittizi; non misurano capienza,
stabilità reale o latenza del servizio. Autenticazione qui significa confronto col riferimento
locale approvato e con gli artefatti conservati, non attestazione remota dei pesi del modello.
D9 eseguibile, ordine 1a, insight reali, servizi e identità osservate, tokenizzazione reale,
T5 con margine 20%, prerequisiti e pilot restano fuori da questa consegna.
