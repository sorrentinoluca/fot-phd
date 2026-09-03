# EXP3_V2 first-real-run preflight failure

The invocation of `EXP3V2-N-001`, attempt 0, stopped during external-runtime
inventory preflight, before either `rng` or `sim`. The wrapper passed
`EXP3_V2_FREEZE_MANIFEST.json` as `boundary_manifest_path`; the shared engine
therefore supplied that final manifest to `assert_exp3v2_runtime_bundle`, but
the original final manifest contains no `external_runtime_dependencies` field.

No attempt-log record or workbook was created. The only filesystem effects were
the empty directories `tep_exp3_v2_heldout/` and
`tep_exp3_v2_heldout/mode1/`. Primary seed `320001` was not consumed, so
`EXP3V2-N-001` attempt 0 remains eligible under the unchanged case plan.

This is a final-boundary packaging defect, not a simulator, scientific-plan, or
sentinel defect. Revision 002 adds the already frozen eight-file runtime
inventory to a new final manifest and changes only the real wrapper's selected
boundary. It does not alter the shared engine and does not justify rerunning the
successful Revision 004 sentinel.
