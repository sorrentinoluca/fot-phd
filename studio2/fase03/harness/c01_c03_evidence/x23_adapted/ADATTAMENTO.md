# Adattamento X23 dopo la correzione C02

Lo script originale resta byte-identico nell'acquisizione e nel replay after. X23 originariamente certificava la persistenza del difetto C02: si aspettava l'interruzione del gate (nessuna valutazione). Dopo C02 tale assertion non può restare verde senza reintrodurre il difetto. Si conserva lo stub che fallisce ogni trasporto e si richiede ora: 120 INVALID, NO_GO_TECHNICAL, T3 e T6 false, nessun raw/identità/token inventato, ripresa senza reinvio anche dopo prova zero-token e stesso record/riepilogo. Eseguito solo X23, senza duplicare X19–22/X24. Le altre cinque prove restano letterali. Nessuna modifica al piano o al requisito N48.

Il crash con INTENT incerto, la prova necessaria e il successivo completamento senza retry sono coperti separatamente da test_C02_crash_INTENT_blocks_until_proof_then_enters_T3_without_retry. Il nuovo processo dopo crash su FAILED è coperto da test_C02_real_process_death_after_failure_commit_and_new_process_resume.
