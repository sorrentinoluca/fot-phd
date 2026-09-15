# PROPOSTA — riconciliazione dello storico S esterno

**NON APPROVATA — NON IMPLEMENTATA — NON È UN RECORD `RECONCILED` — NESSUN GO.**

Questa proposta si applica soltanto se una successiva verifica conferma che i
quattro tentativi S1–S4 sono esterni al ledger autorizzato o che le identità ledger
originarie non sono recuperabili. Non sostituisce la ricerca di una fonte durevole
esistente e non autorizza un backfill automatico.

## Evidenza minima richiesta

Un pacchetto candidato dovrebbe contenere:

1. i tre file storici byte-identici, con percorso recuperabile, dimensione, SHA-256
   e commit di origine `4691acb`/`6a02927`;
2. una tabella esatta di quattro ordinali, senza duplicati, che colleghi ogni voce
   alla riga sorgente e, quando disponibile, a timestamp, prompt ID/hash, response
   ID, fingerprint, usage e raw-output hash;
3. l'identità del ledger autorizzato destinatario: percorso assoluto recuperabile,
   `pilot_id`, versione/schema e impronta della copia acquisita;
4. per ogni addebito, un `request_id` nuovo e stabile del record di importazione e
   i byte canonici dell'identità proposta, con SHA-256 ricalcolato; il record deve
   dichiarare che l'identità è stata assegnata durante la riconciliazione e non
   presentarla come ID storico recuperato;
5. un binding esplicito fonte↔record importato, con digest dei byte sorgente letti
   una volta, tipo di esito e campi non disponibili conservati come tali;
6. verbale indipendente del pacchetto e decisione dell'autore che autorizzi la
   procedura, il mapping esatto e l'eventuale mutazione controllata del ledger.

Per S1, un'eventuale qualifica `ZERO_TOKEN_PROVEN` richiede separatamente evidenza
e approvazione conformi al contratto D03: identità della richiesta, ricevuta/evidenza
provider, contatori prompt/completion/total semanticamente validi e pari a zero,
legame durevole fra evidenza, approvazione e riga. In loro assenza S1 resta un
tentativo addebitato con esito storico incerto rispetto allo zero-token. HTTP 400,
`inference_completed=false` e un digest calcolato oggi non bastano e non consentono retry.

## Validazione proposta

- Aprire ciascuna fonte una volta, conservare quei byte per parsing e hashing,
  ricalcolare SHA-256 e confrontarlo con commit, summary e inventario.
- Validare tipi, campi obbligatori, cardinalità quattro e unicità; non limitarsi a
  confrontare due stringhe hash persistite.
- Per S2–S4 ricalcolare raw-output hash e verificare uguaglianza con contenuto della
  risposta, response ID, fingerprint, finish reason e usage.
- Verificare che ogni mapping punti alla stessa identità canonica usata dal ledger,
  non a una ricostruzione parziale; distinguere identità importata da identità storica.
- Tenere validazione, confronto con il ledger, decisione e scrittura in una sola
  transazione. Dopo restart o resume, rileggere e riconfermare fonti, mapping,
  identità e contabilità prima di autorizzare nuove riserve.

## Stati e transizioni

Gli stati proposti per il pacchetto documentale sono:

`DISCOVERED` → `EVIDENCE_SEALED` → `MAPPING_REVIEWED` → `IMPORT_AUTHORIZED` →
`RECONCILED`.

- `DISCOVERED`: fonti localizzate, nessuna autorità.
- `EVIDENCE_SEALED`: byte, formati e impronte verificati; identità mancanti ancora esplicite.
- `MAPPING_REVIEWED`: revisore indipendente approva coerenza e limiti del mapping.
- `IMPORT_AUTHORIZED`: l'autore autorizza esattamente pacchetto, ledger e mutazione proposta.
- `RECONCILED`: una sola transazione registra quattro addebiti/identità e un evento
  di riconciliazione, poi una verifica post-commit conferma stato e impronte.

Da qualunque stato precedente, conflitto, fonte mutata, duplicato, ledger diverso,
ID non univoco, prova zero-token insufficiente o errore di I/O porta a `SUSPENDED`.
Nessuna transizione automatica parte da `SUSPENDED`; serve una nuova disposizione
revisionata. Un crash prima del commit lascia il ledger invariato; dopo un commit
riuscito il resume riconosce lo stesso evento e non importa/addebita di nuovo.

## Punto di gate e contabilità

La riconferma deve avvenire nel gate comune D9, nella stessa transazione che legge
il ledger, **prima della prima nuova riserva, intento, chiamata provider, journal o
materializzazione di output**. Deve valere per accesso diretto, runner/CLI, primo
avvio, resume, riuso nella stessa istanza e restart.

La decisione autoriale resta: **quattro tentativi provider addebitati una sola volta**.
Il record deve mostrare quattro contributori univoci alla quota cumulativa; S2–S4
sono tre risposte completate comprese nei quattro, non tre addebiti aggiuntivi.
S1 è addebitato anche senza prova zero-token. L'assenza della prova vieta soltanto
di trattarlo come quota retry riutilizzabile. Alias, directory, restart o rinomina
del pilot non azzerano né duplicano l'addebito.

Se il runtime corrente non può rappresentare onestamente queste proprietà, la
review deve respingere la proposta o richiedere una revisione esplicita dello schema;
non si devono piegare stati esistenti né creare righe che fingano di essere storiche.

## Prove future prima dell'implementazione

Il contratto test-first dovrà essere approvato prima del codice e includere almeno:

- rosso sul runtime corrente e verde sul candidato con gli stessi byte finali del test;
- mapping incompleto, duplicato, scambiato S2/S3, fonte alterata e hash apparentemente riallineato;
- ledger o `pilot_id` diverso, identità canonica diversa e record già importato;
- S1 con solo HTTP 400, falsi zeri, booleani al posto degli interi, ricevuta o approvazione mancante;
- restart/resume prima e dopo commit e seconda importazione che non addebita di nuovo;
- accesso diretto e runner che rifiutano prima della riserva e del trasporto;
- concorrenza fra due processi sul primo slot successivo alla riconciliazione;
- guasto dopo una precedente validazione nella stessa istanza, per escludere cache autorizzative.

Gli osservabili richiesti sono: zero chiamate client/server, zero nuovi intenti o
journal e database logico/artefatti invariati nei casi negativi; esattamente quattro
contributori storici e un solo evento nel positivo; rollback totale ai punti di
guasto; recupero idempotente dopo restart.

## Review e approvazioni necessarie

1. review indipendente di questa ricognizione e della proposta;
2. decisione esplicita dell'autore sul contratto per storico esterno;
3. eventuale contratto/test-first e implementazione in un commit tecnico separato;
4. review indipendente del candidato tecnico e acquisizione del verbale;
5. autorizzazione distinta per applicare la procedura al ledger reale;
6. solo dopo, nuova valutazione della readiness D9 insieme alle qualificazioni dei servizi.

Fino ad allora `history_reconciliation` resta nullo/sospeso. Questa proposta non
modifica runtime, ledger o configurazioni e non concede retry, chiamate o GO.
