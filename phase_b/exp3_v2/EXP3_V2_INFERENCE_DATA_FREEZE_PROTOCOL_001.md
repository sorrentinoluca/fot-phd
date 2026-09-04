# EXP3_V2 post-inference data-freeze protocol 001

Status: `REVIEW_ONLY_GOVERNANCE_EXTENSION`

Prospective annotated tag: `exp3-v2-inference-frozen-001`

This protocol implements the later inference-data freeze delegated by
`EXP3_V2_INFERENCE_PROTOCOL_001.md`. It does not authorize evaluation,
ground-truth loading, metric calculation, another provider call, or publication.

## Immutable input boundary

The authoritative source is
`/private/tmp/exp3v2-inference-run-001/output`. Its 3,248 regular files are
allowlisted individually by relative path, byte size, and SHA-256 in
`EXP3_V2_INFERENCE_DATA_FREEZE_MANIFEST_001.json`. The source absolute path is
host provenance only. Clone verification resolves only `inference_outputs/`
relative to the detached final-tag checkout.

Every output is included. Outcome-based exclusion, selective freezing,
renaming, path normalization, or rewriting is prohibited. Symlinks, missing
files, extra files, non-regular files, changed sizes, changed hashes, or Git LFS
pointers fail closed.

## Disconnected Git topology

The payload commit has zero parents and exactly 3,248 paths, all beneath
`inference_outputs/`. The governance commit has the payload commit as its sole
parent and adds exactly the five paths in the manifest's
`governance.file_allowlist`. It modifies or deletes no payload path. Its final
tree therefore has exactly 3,253 paths.

The annotated tag `exp3-v2-inference-frozen-001` points to the governance
commit. Only that tag ref may be pushed. No branch is published and no ref is
forced. Storage is ordinary Git without Git LFS.

Before the governance commit, a human-approved finalization changes only the
new draft manifest: `status` becomes `FROZEN_BEFORE_EVALUATION`, `tag_created`
becomes `true`, `governance.actual_payload_commit` is set to the zero-parent
payload commit, and `human_freeze_approval` records the explicit approval and
UTC timestamp. The manifest remains non-self-referential: it never records its
own SHA-256, the governance commit, or the tag object.

## Required verification dependencies

The final tag alone is not sufficient for full semantic verification. It
contains the payload, this protocol, its manifest/schema, and the portable
wrapper, but the frozen inference verifier and its exact prompt-building inputs
remain in the six upstream tags. Full verification requires detached clean
checkouts of all seven annotated tags and the already frozen 20-package Python
runtime.

The exact post-publication checkout sequence is:

```bash
test ! -e /private/tmp/exp3v2-inference-freeze-verify-001
mkdir -p /private/tmp/exp3v2-inference-freeze-verify-001
git init --bare /private/tmp/exp3v2-inference-freeze-verify-001/tags.git
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git remote add origin https://github.com/sorrentinoluca/fot-phd.git
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-heldout-frozen-002:refs/tags/exp3-v2-heldout-frozen-002
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-heldout-data-frozen-001:refs/tags/exp3-v2-heldout-data-frozen-001
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-verbalization-harness-frozen-001:refs/tags/exp3-v2-verbalization-harness-frozen-001
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-verbalizations-frozen-001:refs/tags/exp3-v2-verbalizations-frozen-001
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-inference-harness-frozen-001:refs/tags/exp3-v2-inference-harness-frozen-001
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-inference-execution-frozen-001:refs/tags/exp3-v2-inference-execution-frozen-001
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git fetch --no-tags origin refs/tags/exp3-v2-inference-frozen-001:refs/tags/exp3-v2-inference-frozen-001
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-inference-freeze-verify-001/source 'refs/tags/exp3-v2-heldout-frozen-002^{}'
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-inference-freeze-verify-001/data 'refs/tags/exp3-v2-heldout-data-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-inference-freeze-verify-001/verbalization-harness 'refs/tags/exp3-v2-verbalization-harness-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-inference-freeze-verify-001/verbalizations 'refs/tags/exp3-v2-verbalizations-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-inference-freeze-verify-001/inference-harness 'refs/tags/exp3-v2-inference-harness-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-inference-freeze-verify-001/authorization 'refs/tags/exp3-v2-inference-execution-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-inference-freeze-verify-001/tags.git worktree add --detach /private/tmp/exp3v2-inference-freeze-verify-001/frozen-output 'refs/tags/exp3-v2-inference-frozen-001^{}'
```

Every command above is exact; a verifier must reject any checkout whose
canonical root or peeled commit differs from the manifest.

The exact verifier invocation is:

```bash
/private/tmp/exp3v2-inference-runtime-001/bin/python3 \
  /private/tmp/exp3v2-inference-freeze-verify-001/frozen-output/phase_b/exp3_v2/verify_exp3v2_inference_data_freeze.py \
  --manifest /private/tmp/exp3v2-inference-freeze-verify-001/frozen-output/phase_b/exp3_v2/EXP3_V2_INFERENCE_DATA_FREEZE_MANIFEST_001.json \
  --freeze-root /private/tmp/exp3v2-inference-freeze-verify-001/frozen-output \
  --source-root /private/tmp/exp3v2-inference-freeze-verify-001/source \
  --data-root /private/tmp/exp3v2-inference-freeze-verify-001/data \
  --verbalization-harness-root /private/tmp/exp3v2-inference-freeze-verify-001/verbalization-harness \
  --verbalizations-root /private/tmp/exp3v2-inference-freeze-verify-001/verbalizations \
  --harness-root /private/tmp/exp3v2-inference-freeze-verify-001/inference-harness \
  --authorization-root /private/tmp/exp3v2-inference-freeze-verify-001/authorization
```

## Freeze execution gate

Publication requires a new explicit human approval. Before acting, verify the
prospective tag is absent locally and remotely, re-hash the authoritative
source, materialize only the manifest allowlist into an isolated repository,
construct the zero-parent payload commit, finalize the manifest with that
payload ID, add only the governance allowlist, run the portable verifier, and
push only `refs/tags/exp3-v2-inference-frozen-001`. Abort without force if any
source byte, upstream tag, schema, tree count, parentage, or remote rule differs.
