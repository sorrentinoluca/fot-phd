# D9 — decisione dell'autore acquisita; recepimento canonico pendente

**Studio 2 FoT-TEP, Fase 03. Ruoli APPROVATI dall'autore.**
Data effettiva di acquisizione in questa finestra: **14 settembre 2026, Europe/Rome**.
Riscontro dell'orologio durante l'acquisizione: `2026-09-14 21:57:40 UTC`
(23:57:40 Europe/Rome). È l'ora del riscontro tecnico della registrazione, **non il timestamp
delle parole dell'autore**. Non si attribuiscono date od orari alle dichiarazioni anteriori.
Preparatore del record: Codex; autore della decisione: Luca, identificato nel mandato.
Nessuna firma materiale dell'autore è apposta o acquisita con questo record.

## 1. Provenienza e perimetro dell'approvazione

Fonte primaria: **messaggio utente corrente**, che inizia «Prosegui nella finestra che ha
preparato la proposta D9 dello Studio 2 FoT-TEP» e contiene il blocco
«DECISIONE ESPLICITA DELL'AUTORE, trasmessa con questo mandato». Il blocco trasmette:

> 1. Qwen 122B è producer principale e consumer.
> 2. Qwen 27B è producer alternativo e produce una libreria completa di 16 insight conforme al contratto vigente.
> 3. Nello swap il consumer resta 122B, sui medesimi casi previsti dal disegno.
> 4. Terra è soltanto riferimento storico descrittivo interno, separato dalle stime del nuovo studio; nessuna nuova produzione Terra.

Il mandato riporta inoltre le dichiarazioni precedenti «Usiamo Terra solo come riferimento
storico descrittivo» e «Accetto il tuo suggerimento», specificando che la seconda si riferisce
all'assegnazione sopra. **La provenienza di queste due citazioni è il mandato corrente**:
non vengono presentate come estratte da un'altra sessione o da un log originario autonomamente
verificato. Non si inventano ID di messaggio/sessione, timestamp originali o firme.

La decisione corrisponde ai **ruoli dell'alternativa B** della proposta precedente, ma non
approva in blocco gli altri dettagli operativi di quella proposta. La registrazione è
completa per i ruoli: non occorre chiederne di nuovo l'approvazione, e l'assenza di metadati
tecnici o di una firma 03.8 non la rende una proposta ancora da scegliere.

## 2. Assegnazione acquisita

| Ruolo / elemento | Decisione acquisita | Limite operativo |
| --- | --- | --- |
| Producer principale P | **Qwen 122B** | Produzione della libreria principale secondo il contratto vigente; nessun insight prodotto da questa registrazione. |
| Consumer C | **Qwen 122B** | Consumer dello studio e di entrambe le librerie nel producer-swap. Identità e configurazione effettive da documentare e qualificare. |
| Producer alternativo P_alt | **Qwen 27B** | Libreria **interamente alternativa, completa di 16 insight**, conforme allo stesso contratto. Non una libreria mista o limitata ai fault misurati nello swap. |
| Producer-swap | C resta **122B**, sui medesimi casi previsti dal disegno | Cambia la libreria producer, non consumer, popolazione, condizioni, cap o numerosità. Restano schema comune, due insight per fault e 14 peer per ricevente. |
| Terra | **Solo riferimento storico descrittivo interno**, separato dalle stime del nuovo studio | Nessuna nuova produzione Terra, nessun nuovo braccio Terra, nessun pooling storico/nuovo o accesso Terra da predisporre per questa D9. |
| 27B come consumer di fallback | **Non approvato** | L'approvazione come producer alternativo non lo rende consumer di riserva, neppure automaticamente dopo un fallimento del 122B. Un eventuale cambio di ruoli richiede un'ulteriore decisione dell'autore. |

Lo swap resta il confronto fra librerie 27B/122B con consumer 122B fisso previsto dal disegno;
non dimostra da solo superiorità generale del 122B, indipendenza fra famiglie, effetto puro
dei pesi o portabilità end-to-end. Nessuna nuova ipotesi confermativa viene introdotta.

## 3. Formulazioni superate e preservazione della storia

- La raccomandazione iniziale **27B principale/consumer e 122B alternativo** in
  [PROPOSTA D9](PROPOSTA_D9_RUOLI_MODELLI_2026-09-14.md) è **superata dalla scelta dell'autore**.
  Il file resta interamente byte-identico al commit `95ff8571af02bab79094ed1a6be3f6a7b410c711`:
  **36141 byte**, SHA-256 `a47f42dda7ee9702c292e34ada6b116ac3c85e42ec3a50e68af97c159f0d0f9d`. Il titolo NON APPROVATA continua a descrivere
  correttamente quel documento storico, non lo stato dei ruoli acquisiti qui.
- La [proposta harness D9/label](/Users/luker/fot-tep-harness-0310-offline/studio2/fase03/harness/DECISIONE_D9_ORDINE_LABEL_PENDING.md)
  al pin `288dc1926bfd7ab4ce43bb4377a9a0064313ad69` è **superata nella parte D9** che nomina Terra alternativo e
  27B fallback. La richiesta separata sull'ordine label 1a resta invece aperta. Il file e il
  candidato harness in review sono preservati: il recepimento avverrà in un delta successivo.
- I rami storici con 2.4T, Terra alternativo o ritorno a Terra-only non diventano percorsi
  autorizzati dal presente mandato. Il 2.4T resta dichiarato non ospitabile; nessun fallback
  eseguibile viene dedotto dai rinvii ancora presenti nei documenti canonici.

## 4. Stati distinti: decisione, dati, qualifica e recepimento

| Ambito | Stato dopo questo record |
| --- | --- |
| Ruoli e trattamento Terra | **Approvati, acquisiti localmente** nei soli termini dei §§1–2. |
| Identità esatte/revisioni/quantizzazione | **Da documentare per l'esecuzione**. Nomi nominali e alias non provano identità dei pesi, revisione o quantizzazione effettiva. |
| Tokenizer, template, serving e configurazione | **Da documentare e verificare** per ciascun servizio/ruolo; nessuna eredità automatica dal vecchio preflight. |
| Qualificazione e fattibilità | **Pendenti**: conformità delle librerie, capienza reale, thinking/output, parsing, troncamenti, stabilità, latenza e T5. Nessun GO, pilot o qualifica conferiti. |
| Recepimento 03.8, 03.10, 03.15 | **Da eseguire serialmente** sui target allora correnti; questa registrazione non modifica file canonici o candidati in review. |
| Firma 03.8 / ordine label 1a | **Non approvati da questo mandato**. Firma materiale e decisione label restano separate. |

Inventario nominale già documentato, conservato senza promuoverlo a misura corrente:

- **122B:** nome annunciato `Qwen3.5-122B-A10B-FP8`, alias `qwen3.5-122b`, contesto
  dichiarato 131.072 e output massimo 16.384. Comunicazione tecnica preesistente:
  parametro temperatura da **omettere**, default server dichiarato 0,6; non inviare null,
  stringa vuota o copiare lo 0 storico del 27B. Queste dichiarazioni non sono una nuova
  approvazione/configurazione tecnica né attestano i limiti effettivi. Repository esatto,
  revisione pesi, quantizzazione reale, tokenizer/template e serving restano da acquisire.
- **27B:** identità storicamente dichiarata `Qwen/Qwen3.8-27B-FP8`, revisione
  `017b9c7af6b5689d5dd426a76e0bc077eb5ca20a`, alias `fot-exp2-consumer`.
  Nomi e revisione sono riportati letteralmente; l'alias contiene “consumer” ma il ruolo
  approvato ora è **producer alternativo**. I pin sono fonti storiche da riconfermare per
  l'istanza effettiva, non una qualifica corrente o un vincolo a usare il vecchio endpoint.
- **Contratto R4:** resta congelato al target
  `3c64390bc4dd58c48cc4e1e388a38989b32b3143`. Il contatore canonico 27B e i cap dello
  schema restano comuni ai due producer; la capienza reale delle richieste richiede anche
  tokenizer/template del rispettivo servizio. La scelta del consumer 122B non sostituisce
  automaticamente il contatore R4. Pin documentali e tokenizer storici sono nella proposta
  §3 e nelle fonti improntate della consegna, senza inventarne altri.

I dati tecnici si acquisiscono dai record del gestore/autore; i comportamenti richiedono prove
future autorizzate. Nessuna richiesta a terzi o prova è compiuta da questa finestra.

## 5. Cosa il mandato non approva e cosa resta invariato

Non approva ordine label 1a, firma materiale 03.8, endpoint/revisioni/configurazioni da
congelare, parametri di generazione ancora da scegliere, calendario, collocazione delle
chiamate alternative nel pilot (per esempio `a=1`), riusi o retry ulteriori. Non autorizza
chiamate sperimentali, pilot, inferenze, simulazioni, nuovi bracci o modifiche al budget.
Non autorizza push, merge su main, tag o comunicazioni a terzi.

Restano validi A/B della rev.10, FAR, U3, catalogo, pseudolabel, schema e freeze già pubblicati;
restano invariati H1–H3, D2, D11, R e la contabilità vigente. Per ruoli coincidenti P=C=122B
le richieste distinte si aggregano per modello senza doppi conteggi; P_alt è 27B. Questa
conseguenza contabile non stanzia richieste aggiuntive e non azzera il ledger. Se falliscono
qualifica o fattibilità, si sospende secondo le regole e si rimette all'autore l'eventuale
nuova scelta; non si attiva autonomamente il 27B consumer o Terra.

Le questioni residue sono classificate nella [consegna con matrice](CONSEGNA_RECEPIMENTO_D9_2026-09-14.md).
Non impediscono questa registrazione D9. Il record non firma 03.8, non chiude una sottofase
o la Fase 03 e non sostituisce la successiva verifica dei delta di recepimento.
