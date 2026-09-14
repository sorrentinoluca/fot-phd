# Corrispondenza delle riproduzioni originali con il delta

Il verbale e negative_probes.py originali sono acquisiti byte-identici in
non_ok_20260915/evidence/. La nuova suite è test_revisions.py; le verifiche preesistenti
restano in test_harness_offline.py e negli altri moduli. Questo è un registro di
implementazione, non un nuovo verdetto indipendente.

**Riferimento riprodotto:** 50 metodi, 32 metodi non conformi, 34 failure di assertion
(inclusi sottocasi), zero errori. I dieci rilievi raggruppano questi difetti: non sono
il conteggio dei test. Confrontati anche gli identificativi dei 32 metodi, non solo i totali.

## Matrice R01–R10 → modifica → prove → esito locale

| Rilievo | Modifica eseguibile | Prove | Esito dell'esecutore |
| --- | --- | --- | --- |
| R01 | require_execution e require_pilot_ledger nei runner; guardie anche Provider/server_contract; ingresso sintetico storico disabilitato | N46; test_R01_*: Python diretto, CLI stub, UNDECIDED/SUSPENDED e diverso percorso ledger | Rifiuti con zero invii; configurazione storica invariata e bloccata |
| R02 | Pin 03.7/JSON evidence/Normal/inventario, dipendenza R4 prima del trasporto, tokenizer, handoff ricostruito dai raw e preparazione rigenerata | N30–33, N36–38, N41, N47, N49; test_R02_* | Tampering e autocertificazione rifiutati; mismatch preventivi a zero invii |
| R03 | label_space canonico separato; prepare_gate e API ordinaria usano renderer R4 con approvazione dell'ordine | N34–35, N39; test_R03_real_pipeline_labels_preserved_and_pending_rejected | Ordine evaluator preservato; pending rifiutato anche dalla preparazione ordinaria; accettazione solo fixture |
| R04 | Piano immutabile, transazioni BEGIN IMMEDIATE, eventi normativi interni, PASS vincolato a foglie risolte/record e stadi chiusi | N04–08, N18; test_R04_* | Nessun PASS su FAILED/zero-token non recuperato; nessuna riapertura |
| R05 | Unicità base indipendente da stage_run, identità completa, una sola foglia retry, triplette con originali distinti coerenti | N01–03, N11–17; test_R05_*, LedgerContractTests, test_reserve_15_waiver_and_maxima_152_160 | Concorrenza e quote esercitate; nessun ramo retry duplicato o furto quota |
| R06 | Diagnosi registrata, diff/approvazione/template concreti, invarianti degli otto casi e contratti; esclusione handoff iniziale dopo remediation | N09–10, N45; test_R06_* | Template non approvato e timeout rifiutati; ciclo fixture completo 8/8 riuscito solo sul template approvato |
| R07 | Raw/receipt/record SQLite durevoli, journal durante lo stadio, --resume e riconciliazione esplicita, retry selezionati | N01–02, N43–44, N48, N50–51; test_R07_* | Crash reali producer/sonda/gate e punti del lifecycle; raw e contatori conservati; nessun reinvio incerto |
| R08 | Evento frozen_gate legato a budget e record sonda; confronto oggetto e byte del file; campione e configurazione verificati | N52; test_R08_*, test_R07_probe_explicit_zero_token_triplet_retry | Primo gate rifiuta budget alterato con zero invii aggiuntivi; ripresa esplicita della tripletta testata |
| R09 | Controllo di returned_model/fingerprint su ogni risposta prima della prosecuzione; sospensione atomica con record | N42, N53; test_R09_* | Cambio d'identità interrompe producer e gate conservando raw e consumo; null esplicito non diventa fingerprint inventato |
| R10 | Campione atteso obbligatorio, hash/ID, 8 agenti, 8/16/16 e matched_transfer/context_stress, ripetizioni 1–3 e 120 richieste uniche | N20–24; GateRevisions e GateRuleContractTests | Triplette false rifiutate; T3/T4/T6, R3 pending e assenza GO preservati |

## Copertura delle 50 riproduzioni

Nxx indica test_xx_* del file originale. I prefissi test_Rnn_* indicano i metodi della
nuova suite; i nomi completi e gli esiti si trovano nei log consegnati.

| Metodi originali | Corrispondenza e adattamento |
| --- | --- |
| N01–02 | test_R07_real_crashes_intent_raw_and_completed_restart, test_R07_producer_and_consumer_real_process_crashes, test_two_writers_cannot_duplicate_one_logical_attempt e test_R05_two_processes_reserve_one_original_once: nuovo piano e nuova forma SQLite; processi reali, non soli mock. |
| N03 | test_R05_changed_alias_run_pilot_id_and_duplicate_original e test_R01_changed_ledger_directory_cannot_reset_pilot. |
| N04–05 | test_R04_failed_and_zero_token_cannot_pass: stesso requisito di esclusione degli esiti non valutabili. |
| N06–07 | test_R04_closed_stage_cannot_reopen_retry: ora il rifiuto avviene alla riserva tardiva, prima dell'intento che nel vecchio test veniva accettato. |
| N08 | test_R04_public_normative_event_forbidden: il rifiuto è all'inserimento dell'evento, prima dell'ingresso gate. |
| N09–10 | test_R06_same_case_cannot_replace_eight_and_non_template_contracts_immutable e test_R06_timeout_and_missing_concrete_approval_cannot_remediate: rifiuto anticipato al piano/approvazione. |
| N11–12 | test_R05_changed_alias_run_pilot_id_and_duplicate_original, test_R05_two_processes_reserve_one_original_once, test_R05_triplet_cannot_reuse_original_or_mix_budget. |
| N13 | test_probe_triplet_retry_is_atomic_and_capped: la seconda tripletta ora usa le tre foglie riconciliate della prima, non riusa originali ancora aperti. La terza deve essere rifiutata con rollback e consumo fermo a 6. |
| N14 | test_reserve_15_waiver_and_maxima_152_160: catena zero-token coerente, waiver e rifiuto della sedicesima. |
| N15 | test_gate_is_not_repeatable_and_has_no_retry e test_R04_closed_stage_cannot_reopen_retry. |
| N16–17 | test_reserve_15_waiver_and_maxima_152_160 e test_hard_200_on_explicit_imported_fixture: la sonda 9 è una fixture con i primi due budget troncati; 200 resta una prepopolazione SQL sacrificabile, non un'autorizzazione. |
| N18 | test_R04_outcome_atomic_with_real_concurrent_writer: verifica della chiusura con writer esterno e assenza del vecchio record_event separato. La transazione racchiude ora l'intera verifica e scrittura. |
| N20–21 | Metodi originali riutilizzati con il solo adattamento della fixture di identità/campione e del parametro expected_prompts. Assert su 114/113, assenza astensione, forense/semantica, troncamento e triplette invalide invariati. |
| N22–24 | GateRevisions.test_R10_repetition_condition_hash_uniqueness_and_distribution aggiunge anche hash, request_id duplicati e assenza del campione atteso. |
| N30–34 | Riutilizzati senza modifica dei metodi; ulteriori test_R02_* e test_R03_*. |
| N35 | test_R03_real_pipeline_labels_preserved_and_pending_rejected usa una libreria prodotta dal runner stub e autenticata dal ledger, non un handoff autocertificato. |
| N36–38 | Riutilizzati senza modifica dei metodi; test_R02_frozen_037_and_evidence_json_tamper conferma gli ingressi del builder. |
| N39 | test_R03_real_pipeline_labels_preserved_and_pending_rejected esercita prepare e load_prepared con ordine pending. La vecchia fixture di handoff è rifiutata già prima: viene sostituita solo nel test positivo con una libreria stub tracciata. |
| N40 | test_R06_real_runner_remediation_approved_bytes_and_old_handoff mantiene 8 risposte, una coppia malformata, 7/8 valide e assenza della libreria; poi esercita il secondo ciclo completo autorizzato di fixture. |
| N41 | test_R02_inventory_tamper_r4_and_tokenizer_zero_sends e test_R02_dependency_failure_is_pretransport_and_not_prompt_diagnosis. |
| N42 | test_R09_producer_identity_mismatch_preserves_raw_and_suspends; expected_response dichiarato nella fixture. |
| N43–44 | test_R07_producer_timeout_resume_no_resend_and_explicit_reconciliation, inclusa prova zero-token acquisita e consumo 9 dopo il recupero; crash reale anche nel runner. |
| N45 | test_R06_real_runner_remediation_approved_bytes_and_old_handoff: solo hash inventati non autorizzano più; il diff concreto è acquisito prima, poi il template diverso viene respinto a zero nuove chiamate. |
| N46 | Riutilizzato invariato; test_R01_* estende a CLI e agli ingressi storici diretti. |
| N47 | test_R02_source_manifest_and_prompt_rehash_cannot_bypass: aggiunge l'attacco che aggiorna anche gli hash nei file derivati; l'autenticazione delle sorgenti lo rifiuta. |
| N48 | test_timeout_without_zero_token_proof_never_retries e test_R04_failed_and_zero_token_cannot_pass; il timeout resta una richiesta contata FAILED e interrompe il gate incompleto. Non si fabbrica un raw vuoto né una valutazione completa 120/120. I 9 test del raccordo mantengono la distinzione invalidità/astensione/denominatore. |
| N49 | test_R02_inventory_tamper_r4_and_tokenizer_zero_sends e test_R02_handoff_cannot_self_certify_or_change_library. |
| N50–51 | test_R07_consumer_budget_crash_and_resume_preserve_raw, test_R07_gate_crash_retains_raw_and_blocks_uncertain_resume e test_R07_producer_and_consumer_real_process_crashes; estensione a os._exit(23). |
| N52 | test_R08_frozen_budget_tamper_first_gate_zero_additional_calls. |
| N53 | test_R09_consumer_identity_change_during_gate_suspends. |
| N60–62 | Riutilizzati invariati: canary/audit, logger storico e guardie tokenizer; non ne viene dedotta una qualifica del servizio. |

Le vecchie fixture positive di test_harness_offline.py sono state adattate ai prerequisiti
più forti: piano, raw, record, prove concrete di riconciliazione e campione esatto. Non sono
stati rimossi metodi, abbassate soglie o cambiati i tre file del raccordo metriche.
Le fixture non sono approvazioni di D9 o dell'ordine label reale.
