# Matrice del residuo D01 / C01 / R04

Implementazione successiva al NON OK su `9e18bcbd06fa2c54202c8eeda079c112dbfcefcd`.
Gli esiti locali sotto richiedono una nuova verifica indipendente. C02/C03 sono stati
chiusi dal revisore nei percorsi descritti nel verbale acquisito; questo delta mantiene
il loro comportamento. Nessun freeze o GO.

## Requisiti e copertura

| Requisito | Delta corrente | Prove | Esito locale / limite |
| --- | --- | --- | --- |
| R01 | Le conferme verificano anche la sospensione tramite `_prerequisites` | test_R01_*; Y05; suite applicabile | Barriere eseguibili conservate; configurazione storica non approvata resta bloccata |
| R02 | Nessuna variazione a pin, handoff, renderer, tokenizer e sorgenti | test_R02_*; X12/X14/X17; suite applicabile | Attacchi precedenti nuovamente verificati, nessuna nuova qualifica scientifica |
| R03 | Nessuna variazione a label_space e ordine di presentazione | test_R03_*; X17 | Approvazioni solo fixture; ordine reale ancora separato |
| **R04 / C01 / D01** | Prerequisiti comuni per transizioni e riuso; binding identico, verifica del successo, replay outcome e autenticazione freeze ricontrollano i predecessori | **Y01/Y02 letterali; sette nuove regressioni test_d01_replay** | Stato storico non conforme rifiutato senza nuovi invii né modifiche a database/artefatti; catene valide ancora riprendibili |
| R05 | `_ready` conserva il divieto di riaprire richieste chiuse e le quote | test_R05_*; X04/X06–09/X19/X21; Y06; test_D01_valid_legacy_chain* | Replay valido senza nuove richieste; nessun azzeramento o retry gate |
| R06 | Catena producer attivo/remediation controllata anche dopo chiusura | test_R06_*; X10/X20/X24; test_D01_current_remediation* | Remediation approvata resta riprendibile, schema e otto casi invariati |
| R07 / C02 | Invalidità durevoli nel denominatore e ripresa senza reinvio conservate | test_C02_*; X03/X16/X23 adattato; Y03–Y06; test_D01_current_remediation* | Chiusura indipendente precedente preservata nel delta verificato |
| R07 / C03 | Contatori dello stadio ed evaluable_calls invariati | test_C03_*; X15; Y07 | 9 richieste dopo retry, 8 coppie T9; alternativo 9 contro 17 cumulativi pilot |
| R08 | `authenticate_frozen` esige ora anche la sonda conforme, nella stessa transazione | test_R08_*; X18; test_D01_* | Hash coincidente non sana predecessori non conformi; freeze valido rimaterializzabile |
| R09 | Nessuna variazione alla classificazione raw/assenza di risposta | test_R09_*; X13/X22; Y03/Y05 | Mismatch sospende; assenza resta INVALID senza identità inventata |
| R10 | Nessuna variazione ai criteri delle triplette; replay outcome riapplica le verifiche dei record | GateRevisions; X11; test_C02_*; test_D01_matching_outcome_hash* | 40×3 e 120 primi tentativi conservati; hash outcome uguale non salta il controllo dei raw |

## Nuove regressioni D01 (sette metodi)

| Metodo in test_d01_replay.py | Oggetto della prova |
| --- | --- |
| test_D01_legacy_nonpass_alternate_rejected_by_all_confirmation_entries | Sei stati alternativi (bound, INTENT, FAILED, ZERO_TOKEN_PROVEN, completed senza outcome, FAIL) × sette ingressi: binding/success/outcome della sonda e del gate, freeze. Motivo del rifiuto esplicito sull'alternativo; database logico immutato. |
| test_D01_valid_legacy_chain_replays_after_gate_without_reopening | Controlli positivi storici con alternativo assente o PASS: tutti i sette ingressi accettano, un nuovo originale gate è respinto. |
| test_D01_real_legacy_runner_and_cli_refuse_before_server_or_file_writes | Vecchio runner produce 132 intenti con alternativo FAILED; nuovo runner e CLI budget/stability rifiutano --resume, zero invii/interrogazioni server, byte degli artefatti e database logico invariati. |
| test_D01_valid_real_legacy_gate_rematerializes_without_transport | Vecchio runner con alternativo PASS; rimozione del solo summary nella fixture, replay sonda dopo gate e rigenerazione gate identici, zero nuovi invii. |
| test_D01_current_remediation_and_C02_invalidity_survive_checked_replay | Producer iniziale FAIL, remediation completa approvata di fixture, sonda e gate con un timeout: replay valido conserva INVALID, raw, contatori e zero retry. |
| test_D01_matching_outcome_hash_does_not_skip_durable_record_validation | Su fixture distinta il raw viene deliberatamente alterato via SQL; hash outcome originale uguale non deve evitare la verifica di corruzione. Questa alterazione non costruisce il difetto C01. |
| test_D01_confirmation_transaction_excludes_concurrent_writer | Processi reali: verifica del successo e autenticazione freeze mantengono un'unica transazione; lo scrittore della nota fixture termina soltanto dopo il rilascio. |

Le fixture storiche sono create con `0c8157f`, HEAD/tree e pulizia verificati nel setup,
tramite API pubbliche e runner del vecchio codice in subprocess. La radice del generatore
è configurabile con FOT_HARNESS_LEGACY_CANDIDATE; nessuna fixture scientifica viene prodotta.
I test correnti importano il nuovo codice con namespace assoluto, compatibile con discovery.

## Prove indipendenti conservate e riprodotte

Y01–Y07 sono copiati byte-identici in nuovi sandbox: sul respinto 9e18bcb Y01/Y02 falliscono,
Y03–Y07 passano; con la correzione tutti e sette passano. Nessun adattamento degli assert Y.
I due errori di precedenza restano un solo rilievo D01, non due nuovi difetti.

La matrice nominativa dei **50 metodi** rimane acquisita byte-identica in
[non_ok_9e18bcb_20260915/evidence/MATRICE_50_METODI.md](non_ok_9e18bcb_20260915/evidence/MATRICE_50_METODI.md)
e nel JSON omonimo. Le 50 corrispondenze, gli accorpamenti e l'equivalenza N48 verificata
nella precedente review non cambiano. La presente matrice aggiunge gli ingressi legacy
che mancavano alla copertura R04/C01, senza riclassificare i metodi precedenti.

X01–X24 mantengono la distinzione: 23 letterali più X23 adattato e già verificato dal
revisore. Il file X23 letterale continua a richiedere l'interruzione errata di C02 e la sua
failure resta visibile. Non si dichiara 24/24 sul file originale immutato. Le suite mirata,
discovery, i 14 applicabili, gli X e gli Y si sovrappongono: non si sommano.
