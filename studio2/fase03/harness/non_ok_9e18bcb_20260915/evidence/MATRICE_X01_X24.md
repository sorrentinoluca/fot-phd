# Estensioni X01–X24 e sette nuove prove Y

24 metodi distinti: 23 letterali conformi; X23 letterale fallisce e il suo adattamento esplicito passa. Nessuna somma con le suite 96/131 o i 50 metodi mappati. Le copie letterali hanno gli hash dei due script indipendenti originali. L'adattamento è della preparatrice ed è stato letto, confrontato e rieseguito dal revisore.

X23 originario attestava il difetto C02 aspettando interruzione definitiva dopo un timeout. Questa attesa contrasta con il piano rev.10, righe 831/871–875. Il nuovo X23 mantiene lo stub che fallisce ogni invio, ma richiede 120 INVALID e 40 triplette non valutabili, NO_GO tecnico, raw/identità/token assenti, prova successiva immutabile e nessun reinvio. Diff in `X23_adaptation.diff`. Le sole modifiche sono il corpo X23 e la selezione per eseguire soltanto X23: nessun altro metodo è riscritto. L'adattamento è giustificato dal requisito; non certifica un comportamento reale del servizio.

| ID e codice | Run letterale | Consolidamento motivato |
| --- | --- | --- |
| [test_X01_incomplete_alternate_blocks_probe](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:33) | PASS | PASS letterale |
| [test_X02_failed_alternate_blocks_real_consumer](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:41) | PASS | PASS letterale |
| [test_X03_gate_transport_invalidity_remains_in_T3_T6](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:49) | PASS | PASS letterale |
| [test_X04_late_retry_is_rejected_before_and_after_restart](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:65) | PASS | PASS letterale |
| [test_X05_interrupted_primary_cannot_be_closed_or_skipped](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:74) | PASS | PASS letterale |
| [test_X06_real_concurrent_base_reservation_12_writers](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:83) | PASS | PASS letterale |
| [test_X07_outcome_transaction_excludes_writer_while_closing](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:95) | PASS | PASS letterale |
| [test_X08_retry_triplet_rollback_after_one_insertion_at_quota](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:124) | PASS | PASS letterale |
| [test_X09_zero_token_proof_rejects_positive_tokens_wrong_identity_missing_author](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:140) | PASS | PASS letterale |
| [test_X10_remediation_concrete_diff_diagnosis_template_coverage](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:150) | PASS | PASS letterale |
| [test_X11_gate_boolean_repetitions_bad_roles_and_frozen_text](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:158) | PASS | PASS letterale |
| [test_X12_r4_rechecked_mid_producer_before_next_send](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:170) | PASS | PASS letterale |
| [test_X13_changed_fingerprint_preserves_tokens_and_suspends](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:179) | PASS | PASS letterale |
| [test_X14_corrupted_durable_record_cannot_resume_or_pass](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:189) | PASS | PASS letterale |
| [test_X15_producer_summary_counts_retry_provider_requests](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:196) | PASS | PASS letterale |
| [test_X16_gate_raw_crash_and_closed_file_resume](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:202) | PASS | PASS letterale |
| [test_X17_approval_hash_and_presentation_order_binding](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:216) | PASS | PASS letterale |
| [test_X18_frozen_reformatted_bytes_rejected_without_call](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/extended_probes.py:225) | PASS | PASS letterale |
| [test_X19_alternate_base_quota_cannot_fund_transport](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/additional_edges.py:12) | PASS | PASS letterale |
| [test_X20_first_remediation_binding_rejects_changed_cases_and_contract](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/additional_edges.py:25) | PASS | PASS letterale |
| [test_X21_cli_reconciliation_and_real_restart_use_same_intent](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/additional_edges.py:35) | PASS | PASS letterale |
| [test_X22_identity_mismatch_in_budget_blocks_whole_pilot](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/additional_edges.py:46) | PASS | PASS letterale |
| [test_X23_failed_gate_resume_and_zero_token_do_not_erase_failure](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/additional_edges.py:52) | FAIL: vecchia attesa di interruzione | PASS adattato |
| [test_X24_primary_structure_envelope_defect_is_remediable](/Users/luker/fot-tep-riverifica-harness-9e18bcb-01a0a1ec/evidence/literal/evidence/additional_edges.py:64) | PASS | PASS letterale |

Prove nuove autonome (script `edge_probes.py`, JSON/log omonimi):

| ID | Requisito | Risultato |
| --- | --- | --- |
| Y01 | Ripresa runner del gate v2 chiuso con alternativo FAILED | FAIL — D01 residuo C01 |
| Y02 | Verifica successo e replay outcome con alternativo INTENT | FAIL — D01 residuo C01 |
| Y03 | Raw con modello errato non convertibile in assenza risposta | PASS |
| Y04 | Errore journal dopo commit INVALID: ripresa, 119/120 e R3 senza reinvio | PASS |
| Y05 | HarnessError preventiva resta INTENT bloccante, senza INVALID fittizio | PASS |
| Y06 | INVALID riconciliato resta immutabile e non abilita retry gate | PASS |
| Y07 | Alternativo: summary/outcome 9 richieste e 8 coppie, pilot 17; replay senza summary file | PASS |

Y01/Y02 costruiscono i vecchi ledger eseguendo soltanto codice 0c8157f in copie sacrificabili, poi li aprono con 9e18bcb. Nessuna manomissione SQL, nessuna modifica al vecchio candidato o alla vecchia review. I percorsi temporanei contenuti negli artefatti rimangono forensi; per riprodurre, creare nuove fixture dallo script.
