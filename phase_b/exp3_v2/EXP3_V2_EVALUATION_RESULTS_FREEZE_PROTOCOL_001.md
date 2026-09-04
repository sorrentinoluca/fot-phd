# EXP3_V2 confirmatory-results freeze protocol 001

Status: `PRE_FREEZE_DRAFT`

Prospective tag: `exp3-v2-results-frozen-001`

This protocol applies only after the frozen evaluation harness has produced and
the portable verifier has accepted exactly these three files:

- `exp3v2_confirmatory_results.json`
- `exp3v2_confirmatory_bootstrap.json`
- `exp3v2_evaluation_output_hash_manifest.json`

No outcome-based exclusion, selective freezing, recomputation or optional
analysis is permitted. The authoritative output root must remain byte-identical.

The proposed public history is disconnected and tag-only, using ordinary Git:

1. a parentless payload commit containing exactly the three output paths under
   `evaluation_outputs/`;
2. a governance child commit adding a non-self-referential results-freeze
   manifest and the portable verifier dependencies fixed during the later
   review;
3. annotated tag `exp3-v2-results-frozen-001` pointing to that governance
   commit; and
4. no published branch and no force update.

The exact governance allowlist, results-freeze manifest schema, actual payload
commit, final tree count and fresh-fetch command must be prepared after output
verification and approved before publication. This draft does not authorize
evaluation, commit, tag or push.
