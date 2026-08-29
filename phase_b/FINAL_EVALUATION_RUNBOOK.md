# Phase B independent final evaluation runbook

This runbook fixes the mandatory order for the future held-out evaluation. It
does not authorize or execute any held-out analysis by itself.

1. Check out tag `phase-b-protocol-frozen` and verify that it resolves to the
   intended protocol-freeze commit.
2. Verify all Phase A frozen hashes.
3. Run `phase_b/heldout/verify_heldout_integrity.py` against the isolated
   held-out data directory.
4. Confirm the manifest SHA-256 for all 15 frozen workbooks before reading their
   tabular contents.
5. Verbalize exactly those 15 cases with the frozen V2 verbalizer, features,
   baseline, thresholds, injection time, and windows.
6. Persist and expose to the diagnostic layer only neutral text; keep structured
   numerical data and evaluator metadata outside diagnostic prompts.
7. Never pass real fault labels, real fault IDs, source filenames, or the
   evaluator-side pseudolabel mapping to the diagnostic LLM.
8. Construct Conditions A, B, and E exclusively from the frozen templates,
   local examples, final insight library, peer libraries, and derangements.
9. Execute exactly `R = 3` repetitions for every agent–case–condition, using the
   frozen OpenAI model, reasoning effort, null temperature/seed, strict schema,
   local validator, and retry policy.
10. Save every raw provider attempt and complete run record, including hashes,
    provenance, model identity, response/request IDs where available, token
    accounting, parse status, and retry count.
11. Aggregate repetitions only by the frozen two-of-three valid-label majority
    rule; otherwise aggregate abstain.
12. Join evaluator-side truth and calculate diagnostic metrics only offline,
    after all inference records are immutable.
13. Run the paired, true-pseudolabel-stratified cluster bootstrap over the 12
    physical fault-run clusters with 10,000 draws and seed `20260829`.
14. Produce the final report without retroactively modifying prompts, insight
    content, mappings, settings, conditions, aggregation, metrics, hypotheses,
    or statistical procedure.
