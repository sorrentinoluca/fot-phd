# Matrice R01–R10 → correzione D02 → prove

Implementazione successiva al NON OK sul candidato `edb37f359f29c461c5a507c1027c4bf411654130`.
La review acquisita chiude D01 originario e conferma C02/C03 nei percorsi verificati;
D02 richiede nuova verifica indipendente. Nessun freeze o GO.

| Requisito | Delta e comportamento | Prove correnti | Limite |
| --- | --- | --- | --- |
| R01 | `_prerequisites` mantiene il blocco della sospensione e dei preflight non approvati | test_R01_*, X17, Y05, applicabili | Nessuna autorizzazione reale aggiunta |
| R02 | Pin, sorgenti, tokenizer e validatore invariati; raw/record durabili dei predecessori riletti e autenticati | test_R02_*, X12/X14/X17; Z01/Z03; test_D02_raw_and_record* | D02 riguarda la coerenza locale del ledger, non una nuova qualifica dei servizi |
| R03 | label_space evaluator-side e ordine nei prompt invariati | test_R03_*, X17, applicabili | L’ordine reale resta separato dalle approvazioni delle fixture |
| **R04 / D02** | `_successful` usa `_closed_outcome` e il validatore condiviso `_validate_outcome`: copertura, piano, raw/record, criteri PASS e digest di chiusura | **Z01–Z03 letterali; otto test_D02_*; sette test_D01_* e Y01/Y02** | Flag PASS/COMPLETED e hash dell’outcome coincidenti non sostituiscono la prova durevole |
| R05 | Tutti i tentativi vengono confrontati con il piano; catene di retry complete, identità e prova zero-token conservate | test_R05_*, X06–09/X19/X21, Y06; test_D02_retry* | Nessun nuovo retry, azzeramento o cambiamento di quota |
| R06 | Il producer attivo, inclusa la remediation autorizzata, deve conservare raw/record e copertura verificabili | test_R06_*, X10/X20/X24; test_D02_remediation*; positivo D01 remediation | Otto casi, template e approvazione restano quelli del contratto |
| R07 / C02 | Il validatore comune conserva i record INVALID e il replay FAIL; non promuove FAIL a PASS | test_C02_*, X23 adattato, Y03–Y06, Z05, positivo D01 con invalidità | Nessuna risposta o identità inventata; T3/T6 invariati |
| R07 / C03 | Replay producer con retry conserva nove intenti e otto coppie | test_C03_*, X15, Y07, test_D02_retry* | Nove richieste nello stadio e diciassette cumulative nel caso Y07 restano distinti |
| **R08 / D02** | `authenticate_frozen` verifica la catena e l’hash dei byte frozen persistiti; sonda conforme e primo gruppo riuscito | test_R08_*, X18, Z01/Z02/Z04; test_D02_probe_cannot_shrink*, test_D02_record_digest* | Un prefisso 3/6 ammesso non legittima la perdita di record dopo la chiusura |
| R09 | Identità durabile del record confrontata con richiesta/piano; mismatch e sospensione conservati | test_R09_*, X13/X22, Y03/Y05; test_D02_record_digest* | Non si qualifica alcuna identità provider reale |
| R10 | Chiusura e riconferma riusano gli stessi criteri dei 120 tentativi e delle quaranta triplette | GateRevisions, X11, test_C02_*, D01 raw gate, Z05 | Nessuna modifica a gate_rules.py o al raccordo metriche |

## Otto regressioni aggiunte in test_d02_predecessors.py

| Metodo | Guasto o controllo |
| --- | --- |
| test_D02_raw_and_record_hash_faults_reject_all_confirmation_entries | Primario, alternativo e sonda: raw o record corrotti dopo controllo positivo. Binding/success/outcome propri e del gate, più freeze: rifiuto senza scritture. |
| test_D02_missing_coverage_raw_or_evaluation_rejects_predecessors | Richiesta, risposta o valutazione mancante in ciascun predecessore; restart e controlli normativi. |
| test_D02_probe_cannot_shrink_to_an_allowed_prefix_after_closure | Sonda valida a nove basi ridotta artificialmente a sei: il prefisso non può riconfermare il vecchio esito. |
| test_D02_record_digest_binding_and_frozen_evidence_are_reauthenticated | Record modificato con hash locale ricalcolato ma vecchio digest di chiusura; evento/digest/frozen e identità richiesta incoerenti. |
| test_D02_retry_replay_preserves_nine_attempts_and_rejects_missing_ancestor | Positivo con nove intenti, zero nuovi eventi; rimozione della prova di riconciliazione dell’antenato rifiutata. |
| test_D02_remediation_and_new_probe_validate_durable_active_producer | Raw della remediation corrotti; nuovo binding sonda rifiutato se il producer primario ha raw corrotti. |
| test_D02_runner_and_CLI_resume_refuse_before_server_calls_or_output_writes | Runner ordinario e CLI budget/stability --resume: corruzione alternativa rifiutata; 139 intenti, file e database invariati, zero nuovi invii/interrogazioni server. |
| test_D02_durable_predecessor_reads_hold_the_confirmation_lock | Processo concorrente realmente bloccato durante la lettura dei record alternativi per quattro ingressi; dopo il ritorno acquisisce il lock. |

Le prove Z01–Z05 sono acquisite e rieseguite byte-identiche: sul respinto tre failure,
con il delta nessuna. Z04 verifica quattro transazioni con un processo scrittore reale;
Z05 conserva il replay di un gate FAIL con 120 INVALID. I guasti SQL sono deliberati e
limitati a copie sacrificabili dopo un controllo positivo; non costruiscono D01.

La [matrice nominativa dei 50 metodi](non_ok_edb37f3_20260915/files/MATRICE_50_METODI.md)
e il JSON omonimo sono conservati byte-identici. Le corrispondenze vengono riesercitate
con le suite pertinenti: 12 originali letterali, due adattamenti di fixture/argomento,
35 accorpamenti/adattamenti e N48 equivalente al requisito C02. Nessun nuovo adattamento.
Non si dichiara 50/50 letterali. X mantiene **23 letterali + X23 già adattato**; la failure
X23 letterale obsoleta resta visibile. Y resta interamente letterale. Suite e sottocasi
si sovrappongono, non si sommano. Conteggi e log in [d02_evidence/RESULTS.json](d02_evidence/RESULTS.json).
