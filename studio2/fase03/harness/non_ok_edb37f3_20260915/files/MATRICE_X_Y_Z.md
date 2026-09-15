# Estensioni X, Y e Z — candidato edb37f3

X: 24 metodi distinti, 23 letterali PASS e solo X23 adattato PASS. Il file originale X23 produce una failure, conservata. Attendeva l'interruzione difettosa del gate C02; l'adattamento già verificato nel terzo verbale mantiene sempre TimeoutError e richiede 120 INVALID, T3/T6 falliti, 40 triplette non valutabili, raw/identità/token sconosciuti null, riconciliazione immutabile e nessun reinvio. Nessun nuovo adattamento in questa review; copie letterali e adattata confrontate per hash con la precedente evidence. Il diff originario è acquisito in non_ok_9e18bcb_20260915/evidence/X23_adaptation.diff.

| Metodo X | Esito letterale | Consolidamento |
| --- | --- | --- |
| [test_X01_incomplete_alternate_blocks_probe](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:33) | PASS | PASS letterale |
| [test_X02_failed_alternate_blocks_real_consumer](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:41) | PASS | PASS letterale |
| [test_X03_gate_transport_invalidity_remains_in_T3_T6](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:49) | PASS | PASS letterale |
| [test_X04_late_retry_is_rejected_before_and_after_restart](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:65) | PASS | PASS letterale |
| [test_X05_interrupted_primary_cannot_be_closed_or_skipped](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:74) | PASS | PASS letterale |
| [test_X06_real_concurrent_base_reservation_12_writers](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:83) | PASS | PASS letterale |
| [test_X07_outcome_transaction_excludes_writer_while_closing](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:95) | PASS | PASS letterale |
| [test_X08_retry_triplet_rollback_after_one_insertion_at_quota](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:124) | PASS | PASS letterale |
| [test_X09_zero_token_proof_rejects_positive_tokens_wrong_identity_missing_author](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:140) | PASS | PASS letterale |
| [test_X10_remediation_concrete_diff_diagnosis_template_coverage](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:150) | PASS | PASS letterale |
| [test_X11_gate_boolean_repetitions_bad_roles_and_frozen_text](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:158) | PASS | PASS letterale |
| [test_X12_r4_rechecked_mid_producer_before_next_send](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:170) | PASS | PASS letterale |
| [test_X13_changed_fingerprint_preserves_tokens_and_suspends](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:179) | PASS | PASS letterale |
| [test_X14_corrupted_durable_record_cannot_resume_or_pass](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:189) | PASS | PASS letterale |
| [test_X15_producer_summary_counts_retry_provider_requests](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:196) | PASS | PASS letterale |
| [test_X16_gate_raw_crash_and_closed_file_resume](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:202) | PASS | PASS letterale |
| [test_X17_approval_hash_and_presentation_order_binding](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:216) | PASS | PASS letterale |
| [test_X18_frozen_reformatted_bytes_rejected_without_call](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/extended_probes.py:225) | PASS | PASS letterale |
| [test_X19_alternate_base_quota_cannot_fund_transport](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/additional_edges.py:12) | PASS | PASS letterale |
| [test_X20_first_remediation_binding_rejects_changed_cases_and_contract](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/additional_edges.py:25) | PASS | PASS letterale |
| [test_X21_cli_reconciliation_and_real_restart_use_same_intent](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/additional_edges.py:35) | PASS | PASS letterale |
| [test_X22_identity_mismatch_in_budget_blocks_whole_pilot](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/additional_edges.py:46) | PASS | PASS letterale |
| [test_X23_failed_gate_resume_and_zero_token_do_not_erase_failure](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/additional_edges.py:52) | FAIL: vecchia attesa di interruzione | PASS adattato |
| [test_X24_primary_structure_envelope_defect_is_remediable](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/literal/evidence/additional_edges.py:64) | PASS | PASS letterale |

| Metodo Y, script byte-identico | Esito corrente |
| --- | --- |
| [test_Y01_legacy_closed_unsafe_gate_is_rejected_by_real_resume](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/y_original/evidence/edge_probes.py:21) | PASS |
| [test_Y02_legacy_closed_unsafe_gate_verification_is_rejected](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/y_original/evidence/edge_probes.py:47) | PASS |
| [test_Y03_raw_identity_cannot_be_reclassified_as_absent](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/y_original/evidence/edge_probes.py:60) | PASS |
| [test_Y04_journal_io_failure_after_invalidity_commit_recovers](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/y_original/evidence/edge_probes.py:64) | PASS |
| [test_Y05_guard_failure_is_not_converted_to_gate_invalidity](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/y_original/evidence/edge_probes.py:76) | PASS |
| [test_Y06_gate_invalidity_same_identity_cannot_be_retried](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/y_original/evidence/edge_probes.py:82) | PASS |
| [test_Y07_alternate_summary_restart_preserves_stage_not_pilot_denominator](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/y_original/evidence/edge_probes.py:89) | PASS |

Y01/Y02 generano nuovi ledger con il codice esatto 0c8157f in subprocess, senza SQL alterato, e li riaprono sul candidato corrente. Le due failure precedenti sono ora rifiuti espliciti sull’alternativo; 132 intenti e zero nuovi invii. Y03–Y07 confermano raw/INVALID, guardie, journal, retry e denominatori producer. Nessuna somma con i sette test D01 già inclusi nelle suite 103/138.

| Nuova prova autonoma Z | Proprietà | Esito |
| --- | --- | --- |
| [test_Z01_corrupted_predecessor_raw_blocks_normative_confirmation](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/chain_probes.py:25) | Raw corrotto di primario/alternativo/sonda: quattro ingressi normativi | FAIL — D02 |
| [test_Z02_missing_predecessor_coverage_is_not_a_successful_chain](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/chain_probes.py:42) | Sette richieste alternative residue non possono attestare copertura di otto | FAIL — D02 |
| [test_Z03_real_runner_rejects_corrupted_alternate_predecessor](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/chain_probes.py:53) | Runner ordinario: raw alternativo corrotto dopo gate valido, riapertura senza invii | FAIL — D02 |
| [test_Z04_each_confirmation_holds_a_real_write_lock_for_all_predecessor_reads](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/chain_probes.py:66) | Quattro ingressi: vero processo BEGIN IMMEDIATE bloccato durante la verifica e ammesso dopo | PASS |
| [test_Z05_closed_failed_gate_replays_without_promoting_outcome](/Users/luker/fot-tep-riverifica-harness-edb37f3-01a0a1ec/evidence/chain_probes.py:88) | Gate tutto INVALID già FAIL: replay conserva 120 invalidità e non promuove a successo | PASS |

Z01–Z03 provocano fault SQL espliciti soltanto su copie sacrificabili già valide; non vengono confusi con le riproduzioni D01 generate senza SQL. Gli hash dei raw non sono ricalcolati e l’outcome non viene cambiato. Il parser ordinario ledger.response rileva la corruzione; è la conferma ricorsiva a non applicare quel controllo. Non viene rivendicata resistenza crittografica al proprietario del database.
