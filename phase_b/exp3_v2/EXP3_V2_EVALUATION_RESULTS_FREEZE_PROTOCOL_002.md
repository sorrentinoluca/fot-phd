# EXP3_V2 evaluation-results freeze protocol 002

Status: `REVIEW_ONLY_GOVERNANCE_EXTENSION`

Prospective annotated tag: `exp3-v2-results-frozen-001`

This protocol closes the governance gaps deliberately left by Revision 001 of
the results-freeze protocol. It does not authorize another evaluator or
verifier execution, result interpretation, a public commit, tag creation, or
push.

## Immutable payload

The authoritative source is
`/private/tmp/exp3v2-evaluation-run-001/output`. Exactly these three byte
strings are included, without rewriting or normalization, beneath
`evaluation_outputs/`:

- `exp3v2_confirmatory_bootstrap.json`
- `exp3v2_confirmatory_results.json`
- `exp3v2_evaluation_output_hash_manifest.json`

The manifest and portable verifier bind their exact sizes and SHA-256 values.
Missing, extra, altered, symlinked, non-regular, or Git-LFS-pointer payloads
fail closed. Outcome-based exclusion and selective freezing are prohibited.

## Disconnected topology and finalization

The payload commit has zero parents and exactly three paths, all under
`evaluation_outputs/`. The governance commit has the payload commit as its
sole parent and adds exactly the five paths in
`governance.file_allowlist`. It modifies or deletes no payload path. The final
tree therefore has exactly eight paths.

The annotated tag `exp3-v2-results-frozen-001` targets the governance commit.
Only that tag ref may be published. No branch is published, no ref is forced,
and all files are ordinary Git blobs without Git LFS.

After a new explicit human approval, finalization changes only the draft
manifest:

1. `status` becomes `FROZEN_BEFORE_VERBALIZATION`;
2. `tag_created` becomes `true`;
3. `frozen_on` records the UTC finalization timestamp;
4. `human_freeze_approval` records the approval; and
5. `governance.actual_payload_commit` records the actual zero-parent payload
   commit.

The manifest is non-self-referential: it never records its own SHA-256, the
governance commit, or the final tag object. The four other governance artifact
hashes are recorded only after those bytes are fixed, forming an acyclic hash
dependency.

## Provenance boundary

The results-freeze manifest binds all seven upstream boundaries used by the
evaluator, Evaluation Harness Revisions 001 and 002, both Revision 001 failure
records, the frozen configuration, the Revision 002 evaluator and verifier,
the single authorized Revision 002 replay, and the separate verifier PASS.
Revision 001 remains exhausted. No second replay, retry, new bootstrap, or
outcome-based selection is permitted.

No scientific result value may be copied into this governance layer. The
payload bytes remain opaque to freeze reporting.

## Portability boundary

Fetching the final tag alone makes all payload and governance bytes reachable,
but is not sufficient for full semantic verification. Full verification needs
detached clean tag-only checkouts of the nine prior boundaries plus the final
tag and the pinned evaluation runtime.

The exact future checkout sequence is:

```bash
test ! -e /private/tmp/exp3v2-results-freeze-verify-001
mkdir -p /private/tmp/exp3v2-results-freeze-verify-001
git init --bare /private/tmp/exp3v2-results-freeze-verify-001/tags.git
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git remote add origin https://github.com/sorrentinoluca/fot-phd.git
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-heldout-frozen-002:refs/tags/exp3-v2-heldout-frozen-002
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-heldout-data-frozen-001:refs/tags/exp3-v2-heldout-data-frozen-001
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-verbalization-harness-frozen-001:refs/tags/exp3-v2-verbalization-harness-frozen-001
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-verbalizations-frozen-001:refs/tags/exp3-v2-verbalizations-frozen-001
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-inference-harness-frozen-001:refs/tags/exp3-v2-inference-harness-frozen-001
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-inference-execution-frozen-001:refs/tags/exp3-v2-inference-execution-frozen-001
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-inference-frozen-001:refs/tags/exp3-v2-inference-frozen-001
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-evaluation-harness-frozen-001:refs/tags/exp3-v2-evaluation-harness-frozen-001
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-evaluation-harness-frozen-002:refs/tags/exp3-v2-evaluation-harness-frozen-002
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-results-frozen-001:refs/tags/exp3-v2-results-frozen-001
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-results-freeze-verify-001/source 'refs/tags/exp3-v2-heldout-frozen-002^{}'
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-results-freeze-verify-001/data 'refs/tags/exp3-v2-heldout-data-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-results-freeze-verify-001/verbalization-harness 'refs/tags/exp3-v2-verbalization-harness-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-results-freeze-verify-001/verbalizations 'refs/tags/exp3-v2-verbalizations-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-results-freeze-verify-001/inference-harness 'refs/tags/exp3-v2-inference-harness-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-results-freeze-verify-001/authorization 'refs/tags/exp3-v2-inference-execution-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-results-freeze-verify-001/inference-output 'refs/tags/exp3-v2-inference-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-results-freeze-verify-001/evaluation-harness-rev001 'refs/tags/exp3-v2-evaluation-harness-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-results-freeze-verify-001/evaluation-harness-rev002 'refs/tags/exp3-v2-evaluation-harness-frozen-002^{}'
git --git-dir=/private/tmp/exp3v2-results-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-results-freeze-verify-001/results 'refs/tags/exp3-v2-results-frozen-001^{}'
```

The exact full verifier invocation is:

```bash
/private/tmp/exp3v2-evaluation-runtime-001/bin/python3 \
  /private/tmp/exp3v2-results-freeze-verify-001/results/phase_b/exp3_v2/verify_exp3v2_evaluation_results_freeze.py \
  --manifest /private/tmp/exp3v2-results-freeze-verify-001/results/phase_b/exp3_v2/EXP3_V2_EVALUATION_RESULTS_FREEZE_MANIFEST_001.json \
  --freeze-root /private/tmp/exp3v2-results-freeze-verify-001/results \
  --source-root /private/tmp/exp3v2-results-freeze-verify-001/source \
  --data-root /private/tmp/exp3v2-results-freeze-verify-001/data \
  --verbalization-harness-root /private/tmp/exp3v2-results-freeze-verify-001/verbalization-harness \
  --verbalizations-root /private/tmp/exp3v2-results-freeze-verify-001/verbalizations \
  --inference-harness-root /private/tmp/exp3v2-results-freeze-verify-001/inference-harness \
  --authorization-root /private/tmp/exp3v2-results-freeze-verify-001/authorization \
  --inference-root /private/tmp/exp3v2-results-freeze-verify-001/inference-output \
  --evaluation-harness-rev001-root /private/tmp/exp3v2-results-freeze-verify-001/evaluation-harness-rev001 \
  --evaluation-harness-rev002-root /private/tmp/exp3v2-results-freeze-verify-001/evaluation-harness-rev002
```

That invocation performs topology, payload, boundary, and semantic checks. The
semantic phase invokes the frozen Revision 002 verifier exactly once and does
not print scientific values.

## Rehearsal-only mode

An isolated rehearsal may use `--rehearsal-final` only when the copied manifest
contains approval scope `SYNTHETIC_ISOLATED_REHEARSAL_ONLY`. This mode checks
the final Git topology, constant-bound payload bytes, schema, ordinary blobs,
and governance hashes, but deliberately does not perform semantic
recomputation. It cannot accept an actual human-approved public manifest and is
not a substitute for the full verifier invocation above.

## Publication gate

Publication requires a new explicit human approval. Re-hash the authoritative
source, construct the zero-parent payload commit, finalize only the manifest,
add only the five governance paths, run full verification, create the annotated
tag, and push only `refs/tags/exp3-v2-results-frozen-001`. Abort without force
if any source byte, path, parent, tag, schema, or upstream binding differs.
