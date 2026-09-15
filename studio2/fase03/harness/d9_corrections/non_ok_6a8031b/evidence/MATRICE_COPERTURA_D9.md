# Tracciamento indipendente dei campi D9

Questa matrice documenta lettura del codice e prove effettive; non è una prova esaustiva di tutti gli interleaving. Riferimenti di codice relativi allo snapshot tecnico 6a8031b, dentro studio2/fase03. I nomi `test_*` si riferiscono alle suite fornite rieseguite; U01–U08 sono sonde nuove del revisore.

| Campo normativo | Ingresso, persistenza e decisione | Evidenza e limite |
| --- | --- | --- |
| binding.execution_config | guards.require_execution → binding nei runner → ledger._binding/validate_binding → inventario cumulativo nelle riserve | Approvazione esatta e uguaglianza fra stadi; D9 mutations, document_changes, persisted_provider; R-D9-01/02 delimitano la completezza semantica |
| provider_reference | producer_probe costruisce path assoluto/hash; d9.read_reference rilegge byte e confronta provider persistito | test_persisted_provider_mutation_and_direct_reservation: contenuto mutato con hash binding riallineato rifiutato |
| provider_file_sha256 | confronto col ruolo in producer_configs, poi con provider_reference in validate_binding | test_swapped_provider_or_unapproved_alternate_is_rejected e test_primary_provider_cannot_execute_alternate_role |
| roles | confronto esatto ROLES; mapping di cinque stadi; modello richieste confrontato col servizio | test_fixed_roles, role_stage_mapping, configuration_mutations; nessun consumer 27B/fallback/Terra |
| services | due servizi esatti, limiti interi positivi, documenti referenziati e congruenti, metadati testuali | Positivo U01, negativo U02/U08, difetto U03: placeholder con spazi accettato |
| producer_configs | due digest per 122B/27B, allowlist uguale; validate_provider lega stadio a ruolo | Negativi su provider scambiato; alternativo completo positivo, otto richieste |
| alternate_placement | PENDING rifiutato; deferred vieta alternate_conformity; pilot esige successo alternativo prima sonda | test_alternate_pilot_full_library_and_same_case_swap; regressioni C01/D02 conservano stati aperti/FAIL/uncerti |
| presentation_order | require_presentation esige approvazione dei byte dell'ordine, separata da execution_authorization | R03 real_pipeline e test_protocol; mapping/label_space/derangement 03.7 non modificati |
| r4_tokenizer | costante canonica confrontata in validate_config; r4_counter verifica i file e crea contatore senza template | test_r4_counter_distinct_from_service_counter; fixture sostituisce pin esplicitamente |
| r4_snapshot | percorso assoluto in config persistita; file verificati da r4_counter nella produzione/preparazione/caricamento | U04–U07 e transport_snapshot_probe: controllo assente nel binding/riserva/trasporto diretto dopo perdita del file; R-D9-02 |
| history_reconciliation | file/hash → stato/reviewer/fonte S/4 mapping → richiesta presente e identity_json hash nel medesimo ledger, dentro transazione | test_history_mapping_cannot_reset_consumption; nei positivi runner fonte fittizia 0/0, non riconciliazione S reale |
| d9.status | DOCUMENTED_FOR_AUTHORIZED_STAGE richiesto, distinto da qualifica | Config pending non eseguibile; server_contract produce solo documento, nessun endpoint osservato |
| missing_requirements | deve essere lista vuota | test_configuration_mutations_refuse_before_client_and_intent; questo controllo non sostituisce validazione semantica metadati (U03) |
| server.scope | server_contract genera DOCUMENTED_NOT_LIVE_VERIFIED; server viene persistito nel freeze e confrontato nel gate | Lettura sorgente run_pilot.server_contract e invarianti del freeze; non esiste attestazione live dei pesi |
| accounting.by_role/by_nominal_model | inventario validato sotto BEGIN IMMEDIATE, ogni intento una volta; producer+consumer→122B | test_resume_counts_once_by_role_and_model, alternate swap: 19 intenti=11 122B+8 27B; non sommare i passaggi in memoria |
| raw/capture | schema D03/D04 invariato, digest/link/prove non sostituiti dalla documentazione dei servizi | test_d03_contract e test_d04_open_quota; null non trasformati in zero; no backfill |

## Percorsi trasversali

- Producer: sviluppo/schema R4 verificati prima della produzione. Otto coppie costruiscono la libreria; non occorre una libreria preesistente. Remediation solo sui medesimi otto casi con template autorizzato; confronto degli altri campi del binding resta integro.
- Consumer: prepare/load_prepared autenticano libreria primaria, fonti, prompt ricostruiti e capienza. Token chat e R4 restano distinti. Provider.call richiede un INTENT e congruenza di configurazione/prompt/generazione, ma non riapre i file tokenizer: R-D9-02.
- Swap: entrambe le librerie sono ricostruite dai raw con PASS dei rispettivi stadi; cambia solo insights in una copia del manifest. I casi forniti e consumer122B restano fissi. Nessuna selezione del campione definitivo.
- Quote: la modifica ledger aggiunge validazione D9 a bind_stage e _binding; le riserve D04 mantengono inventario cumulativo e transazione. Nessuna nuova colonna/evento, reset o quota viene introdotta.
- CLI: i piani non chiamano provider; require_execution precede la costruzione del ledger nei percorsi esecutivi. Le tre CLI sono rieseguite senza --execute; il test pending controlla due ingressi esecutivi con fixture.
