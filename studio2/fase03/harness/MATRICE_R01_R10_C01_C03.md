# Matrice R01–R10 — delta C01–C03

Implementazione successiva al NON OK del candidato `0c8157f`. Gli esiti sotto sono prove
locali della preparatrice, da verificare in una nuova finestra. Non costituiscono un OK
indipendente né un freeze. Tutti gli invii sono stub offline.

## Requisiti, modifiche e prove

| Rilievo | Delta corrente e requisito conservato | Prove locali | Esito e limite |
| --- | --- | --- | --- |
| R01 | Barriere storiche conservate; una HarnessError preventiva non viene convertita in invalidità di trasporto | test_R01_*; originali applicabili | Rifiuto storico e sospensione restano bloccanti; nessuna approvazione reale nuova |
| R02 | Pin e provenienza lungo producer, preparazione e consumer conservati | test_R02_*; X12, X14, originali applicabili | Attacchi verificati ancora respinti; nessuna nuova qualifica dei dati |
| R03 | label_space separato dall'ordine mostrato; renderer e approvazioni fixture conservati | test_R03_*; X17 | Ordine reale 1a ancora non approvato |
| R04 / C01 | `_ready` richiede PASS anche dall'alternativo già definito, nella transazione di binding/riserva/esito sonda e gate | X01, X02; test_C01_* (stati bound/INTENT/FAILED/ZERO/completed/FAIL, binding anticipato, gara tra processi, CLI e recupero alternativo) | Zero invii consumer con alternativo incompleto; opzionalità soltanto prima dell'avvio; PASS alternativo consente la sonda |
| R05 | Identità, unicità, quote e zero retry gate conservati | test_R05_*; X04, X06–09, X19, X21; C02 timeout/ripresa | 120 primi tentativi gate; nessuna spesa dalla riserva retry; 152/160 e hard stop 200 distinti |
| R06 | Diagnosi/diff/template/otto casi conservati; timeout producer non è difetto prompt | test_R06_*; X10, X20, X24 | Nessuna remediation implicita o seconda remediation |
| R07 / C02 | Timeout gate → FAILED + evento INVALID atomico, senza raw; completamento 120 e valutazione T3/T6; crash INTENT rimane bloccato finché provato | X03; X23 adattato esplicitamente; test_C02_* | N48 ripristinato: 119/120 e R3 con un timeout; 117/120 ma T6 non valutabile con tripletta tutta invalida; 113/120 fallisce T3; 120 timeout → 40 triplette invalide |
| R07 / C03 | Summary producer v4: provider_requests dal ledger dello stadio, evaluable_calls separato | X15; test_C03_*; recupero alternativo test_C01_* | Timeout + retry: ledger 9, stub 9, summary 9; 8 coppie T9 e 16 insight; replay identico senza invii |
| R08 | Legame byte/oggetto sonda→gate conservato | test_R08_*; X18 | Modifica o nuova serializzazione del freeze respinta |
| R09 | Risposta ricevuta con identità errata sospende; nessuna risposta resta identity_valid=null | test_R09_*; X13, X22; test_C02_response_identity_mismatch_cannot_be_masked_as_transport | Un timeout non fabbrica modello/fingerprint. Mismatch successivo al timeout conserva raw e sospende |
| R10 | Verifica campione 40×3, ID, ripetizioni e condizioni invariata; eventi trasporto soggetti agli stessi vincoli | GateRevisions; X11; test_C02_* | Invalidità conserva l'identità del primo tentativo; non sostituisce o duplica una tripletta |

## I 50 metodi originari e N48

La matrice nominativa dei 50 metodi è acquisita byte-identica in
[non_ok_0c8157f_20260915/evidence/MATRICE_50_METODI.md](non_ok_0c8157f_20260915/evidence/MATRICE_50_METODI.md)
e nel JSON omonimo. Le corrispondenze restano quelle verificate, salvo N48, per il quale
la precedente implementazione e la precedente dichiarazione di equivalenza sono respinte.

N48 originario (`test_48_tracked_transport_failure_remains_invalid_in_denominator`) richiede
parse_valid_first_attempt=false, parsed_output=null e contatore conservato. La nuova prova
ordinaria X03 e `test_C02_N48_single_timeout_is_119_of_120_and_replays_without_sends`
aggiungono l'intero percorso producer→prepare→sonda→120 tentativi: il record INVALID entra
nel denominatore, la tripletta mista diverge, l'outcome si lega ai record durevoli, il replay
non reinvia e la riconciliazione successiva non cancella l'invalidità. `return_error_record`
è eliminato dalla firma privata: la regola vale sempre nello stadio gate, non è facoltativa.
La fixture/API vecchia non è riscritta nell'acquisizione.

## X01–X24: conteggio e adattamento trasparente

- Sul vecchio candidato: X01–X18 letterali producono 4 failure (X01/X02/X03/X15), 0 errori;
  X19–X24 sono 6/6. Sono gli stessi quattro assert raggruppati in tre difetti.
- Sul nuovo codice: X01–X18 sono 18/18; X19–X22 e X24 sono 5/5 letterali.
- X23 letterale attendeva che il gate si interrompesse senza T3/T6: attestava il difetto.
  Dopo C02 la sua assertion `assertRaises` fallisce perché il gate completa. Il log
  **FAILED (failures=1)** è conservato; non viene rinominato PASS.
- X23 aggiornato conserva lo stub sempre fallito e richiede 120 INVALID, NO_GO tecnico,
  nessun raw inventato, identiche invalidità dopo prova zero-token e ripresa senza invio.
  È eseguito separatamente: 1/1. Il requisito normativo è quello del piano rev.10, non
  la precedente interruzione. Vedere l'adattamento in `c01_c03_evidence/x23_adapted/ADATTAMENTO.md`.

Consolidamento locale: **24 metodi distinti conformi, 23 letterali + 1 adattato**.
Non sono 24 nuove prove indipendenti emesse da questa finestra. Le 14 prove originarie
applicabili sono una suite distinta (12 metodi invariati, 2 con le fixture già adattate
nella precedente consegna); le 14 nuove regressioni C01–C03 non si sommano ai metodi X.

## Crash, contatori e limiti

La suite comprende rollback prima del commit dell'invalidità, interruzione dopo commit
prima del journal, arresto reale `os._exit(27)` e ripresa in un **secondo processo**:
13 intenti persistiti al crash (8+3+2), un raw gate e un INVALID; alla ripresa 118 nuovi
invii, 131 intenti totali, 119/120 valide e R3 pending. Un INTENT privo di osservazione
non viene reinviato: solo la prova zero-token approvata abilita il suo record INVALID,
lasciando proseguire i restanti originali.

SQLite resta la fonte; il journal è una proiezione. Gli intenti incerti conservano un
conteggio prudenziale anche quando non è dimostrabile che il provider li abbia ricevuti.
I token non osservati sono null; le prove successive sono eventi distinti. Questi test
non qualificano servizi, identità reali, capacità, T5 o output scientifici.
