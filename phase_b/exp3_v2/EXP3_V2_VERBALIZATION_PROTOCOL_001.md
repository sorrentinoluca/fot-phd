# EXP3_V2 verbalization protocol — harness revision 001

## Review and execution boundary

Human approval froze this harness in a dedicated commit and the annotated tag
`exp3-v2-verbalization-harness-frozen-001`.
`EXP3_V2_VERBALIZATION_HARNESS_MANIFEST_001.json` therefore has status
`HARNESS_FROZEN_FOR_VERBALIZATION`, records the approval, and sets
`tag_created` to `true`; the manifest does not contain its own digest or the
commit that contains it.

Execution uses two new, clean, detached worktrees/checkouts:

- harness: `/private/tmp/exp3v2-verbalization-harness-001/worktree`, checked
  out exactly at `exp3-v2-verbalization-harness-frozen-001`;
- data: `/private/tmp/exp3v2-verbalization-data-001/worktree`, obtained by an
  exact fetch and detached checkout of
  `exp3-v2-heldout-data-frozen-001` only.

The harness consumes only the relative paths recorded in the data-freeze
manifest. Absolute `output_path` values in the attempt log are immutable
provenance and are never resolved or used.

Create and verify those checkouts with these exact commands (each destination
must be absent beforehand):

```bash
git init /private/tmp/exp3v2-verbalization-harness-001/worktree
git -C /private/tmp/exp3v2-verbalization-harness-001/worktree remote add origin https://github.com/sorrentinoluca/fot-phd.git
git -C /private/tmp/exp3v2-verbalization-harness-001/worktree fetch --no-tags origin refs/tags/exp3-v2-heldout-frozen-002:refs/tags/exp3-v2-heldout-frozen-002 refs/tags/exp3-v2-verbalization-harness-frozen-001:refs/tags/exp3-v2-verbalization-harness-frozen-001
git -C /private/tmp/exp3v2-verbalization-harness-001/worktree checkout --detach 'refs/tags/exp3-v2-verbalization-harness-frozen-001^{}'
test "$(git -C /private/tmp/exp3v2-verbalization-harness-001/worktree cat-file -t refs/tags/exp3-v2-verbalization-harness-frozen-001)" = tag
test "$(git -C /private/tmp/exp3v2-verbalization-harness-001/worktree rev-parse HEAD)" = "$(git -C /private/tmp/exp3v2-verbalization-harness-001/worktree rev-parse 'refs/tags/exp3-v2-verbalization-harness-frozen-001^{}')"
test -z "$(git -C /private/tmp/exp3v2-verbalization-harness-001/worktree status --porcelain --untracked-files=all)"

git init /private/tmp/exp3v2-verbalization-data-001/worktree
git -C /private/tmp/exp3v2-verbalization-data-001/worktree remote add origin https://github.com/sorrentinoluca/fot-phd.git
git -C /private/tmp/exp3v2-verbalization-data-001/worktree fetch --no-tags origin refs/tags/exp3-v2-heldout-data-frozen-001:refs/tags/exp3-v2-heldout-data-frozen-001
git -C /private/tmp/exp3v2-verbalization-data-001/worktree checkout --detach 'refs/tags/exp3-v2-heldout-data-frozen-001^{}'
test "$(git -C /private/tmp/exp3v2-verbalization-data-001/worktree cat-file -t refs/tags/exp3-v2-heldout-data-frozen-001)" = tag
test "$(git -C /private/tmp/exp3v2-verbalization-data-001/worktree rev-parse HEAD)" = "$(git -C /private/tmp/exp3v2-verbalization-data-001/worktree rev-parse 'refs/tags/exp3-v2-heldout-data-frozen-001^{}')"
test -z "$(git -C /private/tmp/exp3v2-verbalization-data-001/worktree status --porcelain --untracked-files=all)"
```

## Frozen computation contract

The byte-identical V2 verbalizer, feature implementation and configuration are
loaded from the harness checkout only after their size and SHA-256 have been
verified against `exp3-v2-heldout-frozen-002`. The downstream diagnostic schema
is hash-bound but is not used to reinterpret the neutral verbalization output.

Development baseline statistics are loaded verbatim from
`EXP3_V2_VERBALIZATION_BASELINE_STATS_001.json`. Before approval this artifact
was explicitly `PRE_FREEZE_DRAFT`; the approved harness freeze records it as
`FROZEN_DEVELOPMENT_BASELINE_STATISTICS` and binds its final bytes in the
manifest and annotated tag. The execution path refuses any non-frozen state,
never opens the development baseline workbook, and never calls
baseline-statistics or threshold-calibration functions. The analysis interval
is the left-closed,
right-open range `[10 h, 50 h)`, divided into the exact eight windows
`[10,15)`, `[15,20)`, `[20,25)`, `[25,30)`, `[30,35)`, `[35,40)`, `[40,45)`,
and `[45,50)` hours.

No LLM, model inference, network operation, random-number generation,
threshold refitting, baseline recomputation or raw-workbook write is permitted.
An audit hook rejects socket activity. Source hashes are checked both before
and after processing.

## Fail-closed input and output handling

Preflight completes before any workbook is opened. It verifies the exact
Python executable and package versions, both annotated boundary tags, clean
checkout state, all frozen implementation hashes, the data-freeze manifest,
all 30 canonical identities in order, attempt 0, every workbook size and hash,
and the exact contents of the workbook directory. Missing, altered, extra or
symlinked inputs fail closed.

The execution output is the absent path
`/private/tmp/exp3v2-verbalization-run-001/output`. Existing output roots,
including empty ones, are rejected. On success it contains exactly:

- `structured_json/EXP3V2-*.json` — 30 files;
- `neutral_text/EXP3V2-*.txt` — 30 files;
- `EXP3_V2_VERBALIZATION_OUTPUT_MANIFEST_001.json` — one deterministic
  manifest containing relative paths, sizes and SHA-256 hashes.

If any step fails after the harness creates the output root, the harness
deletes only that root and its own partial outputs. It never deletes or changes
the harness checkout, data checkout, attempt log, data manifest or workbooks.
There is no automatic retry. A new execution requires human review and a newly
absent output root.

## Exact future invocation

After freeze approval, create the output parent only, leaving `output` absent,
then invoke exactly:

```bash
/opt/anaconda3/bin/python3 \
  /private/tmp/exp3v2-verbalization-harness-001/worktree/phase_b/exp3_v2/run_exp3v2_verbalization.py \
  --manifest /private/tmp/exp3v2-verbalization-harness-001/worktree/phase_b/exp3_v2/EXP3_V2_VERBALIZATION_HARNESS_MANIFEST_001.json \
  --data-root /private/tmp/exp3v2-verbalization-data-001/worktree \
  --output-root /private/tmp/exp3v2-verbalization-run-001/output
```

Then invoke the verifier independently:

```bash
/opt/anaconda3/bin/python3 \
  /private/tmp/exp3v2-verbalization-harness-001/worktree/phase_b/exp3_v2/verify_exp3v2_verbalizations.py \
  --manifest /private/tmp/exp3v2-verbalization-harness-001/worktree/phase_b/exp3_v2/EXP3_V2_VERBALIZATION_HARNESS_MANIFEST_001.json \
  --data-root /private/tmp/exp3v2-verbalization-data-001/worktree \
  --output-root /private/tmp/exp3v2-verbalization-run-001/output
```

The verifier hash-checks the frozen verbalizer and feature implementation,
loads `render_text` directly from that verified verbalizer path, recomputes the
neutral text from every structured JSON, appends the protocol newline, and
requires byte-for-byte equality with the corresponding text file. Updating a
text file together with its recorded size, SHA-256 and aggregate digest does
not bypass this semantic binding.

## Final verbalization freeze

After a successful execution and verifier PASS, compute hashes mechanically
without diagnostic interpretation. Prepare
`EXP3_V2_VERBALIZATION_DATA_FREEZE_MANIFEST_001.json` with status
`PENDING_HUMAN_VERBALIZATION_FREEZE`, binding the harness tag, both source/data
tags, the deterministic output manifest, all 60 outputs and their aggregate
inventory digest. Stop for explicit human approval.

The approved immutable storage operation uses isolated temporary repositories:

1. create a parentless payload commit containing exactly the 61 output paths
   below the dedicated tree root `verbalization_outputs/`, preserving their
   paths relative to the execution output root;
2. create a governance child adding exactly the final data-freeze manifest;
3. create annotated tag `exp3-v2-verbalizations-frozen-001` at the governance
   child;
4. push only that tag, never a branch and never with force;
5. verify from three exact detached checkouts: the final tag, the frozen harness
   tag (plus its frozen source-boundary tag), and the frozen data tag.

Fetching only the final verbalization tag is **not** sufficient to rerun the
verifier: the hash-pinned renderer and the immutable raw-input identities live
in the separately frozen harness and data histories. Create the final checkout
and rerun verification with the following exact commands after recreating the
harness and data checkouts using the commands above:

```bash
git init /private/tmp/exp3v2-verbalization-final-verify-001/worktree
git -C /private/tmp/exp3v2-verbalization-final-verify-001/worktree remote add origin https://github.com/sorrentinoluca/fot-phd.git
git -C /private/tmp/exp3v2-verbalization-final-verify-001/worktree fetch --no-tags origin refs/tags/exp3-v2-verbalizations-frozen-001:refs/tags/exp3-v2-verbalizations-frozen-001
git -C /private/tmp/exp3v2-verbalization-final-verify-001/worktree checkout --detach 'refs/tags/exp3-v2-verbalizations-frozen-001^{}'
test "$(git -C /private/tmp/exp3v2-verbalization-final-verify-001/worktree cat-file -t refs/tags/exp3-v2-verbalizations-frozen-001)" = tag
test "$(git -C /private/tmp/exp3v2-verbalization-final-verify-001/worktree rev-parse HEAD)" = "$(git -C /private/tmp/exp3v2-verbalization-final-verify-001/worktree rev-parse 'refs/tags/exp3-v2-verbalizations-frozen-001^{}')"
test -z "$(git -C /private/tmp/exp3v2-verbalization-final-verify-001/worktree status --porcelain --untracked-files=all)"
/opt/anaconda3/bin/python3 /private/tmp/exp3v2-verbalization-harness-001/worktree/phase_b/exp3_v2/verify_exp3v2_verbalizations.py --manifest /private/tmp/exp3v2-verbalization-harness-001/worktree/phase_b/exp3_v2/EXP3_V2_VERBALIZATION_HARNESS_MANIFEST_001.json --data-root /private/tmp/exp3v2-verbalization-data-001/worktree --output-root /private/tmp/exp3v2-verbalization-final-verify-001/worktree/verbalization_outputs
```

The parentless payload tree contains exactly 61 paths below
`verbalization_outputs/` (30 structured JSON, 30 neutral text files and the
deterministic output manifest); the governance child contains exactly 62 paths
after adding its one manifest outside that output root. This separation lets
the verifier retain its exact-tree rejection policy while ignoring nothing.

The operation must abort if an input or output hash changes, the proposed tag
already exists, the verifier fails, or the remote rejects the tag.
