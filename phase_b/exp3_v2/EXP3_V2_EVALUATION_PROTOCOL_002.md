# EXP3_V2 evaluation harness recovery protocol Revision 002

Status: `PRE_FREEZE_DRAFT`

Prospective harness tag: `exp3-v2-evaluation-harness-frozen-002`

Prospective results tag: `exp3-v2-results-frozen-001`

This review-only protocol corrects one infrastructure-ordering defect in
Revision 001. It does not authorize evaluation or deterministic replay.

## Revision 001 failure provenance

Revision 001, frozen at annotated tag
`exp3-v2-evaluation-harness-frozen-001`, received one authorized evaluator
invocation and no retry. The runner invoked `numpy.random.default_rng(320031)`
once and completed the in-memory evaluation and bootstrap. It then failed before
any output write because it called `output_root.mkdir(parents=False)` while the
dedicated parent `/private/tmp/exp3v2-evaluation-run-001` was absent.

No result, metric, interval, bootstrap distribution or other scientific value
from that invocation was persisted, inspected or reported. The output root
remained absent, the verifier was not run and no result tag was created. The
byte-identical JSON and Markdown failure records are frozen inputs to this
candidate.

Revision 001 is exhausted. It authorizes neither retry nor reuse of seed
`320031`.

## Invariant scientific contract

Revision 002 changes no scientific setting. It inherits byte-identically the
frozen Revision 001 configuration, runtime lock, requirements, result schemas
and result-freeze protocol. In particular, it preserves:

- all populations, denominators and label mappings;
- abstention treatment;
- the unseen `B-A` and `B-E` contrasts and success criteria;
- the paired physical-case cluster bootstrap stratified by true pseudolabel;
- exactly 10,000 draws using `numpy.random.default_rng(320031)`;
- the same RNG algorithm, stream, quantile method and three output files; and
- the same pinned Python runtime and dependencies.

No new seed or additional draw is introduced.

## Fail-closed output reservation order

Any future Revision 002 evaluator invocation must execute these phases in the
following order:

1. validate the frozen Revision 002 harness boundary and all upstream detached
   tagged checkouts;
2. validate the pinned runtime;
3. require the CLI output path to equal exactly the path authorized by the
   frozen Revision 002 manifest;
4. validate or create the dedicated parent safely, rejecting every symlink or
   non-directory component;
5. require the output root to be absent and reserve it with exclusive
   no-overwrite directory creation;
6. only after successful reservation, verify and read aggregate predictions,
   data manifest, case plan and evaluator mapping;
7. only then join truth, calculate metrics, invoke `default_rng(320031)` and run
   the bootstrap; and
8. write the same three outputs into the already-reserved directory without
   attempting to recreate it.

If the output root already exists, or if its path differs from the frozen
authorization, the invocation stops before scientific input or RNG access. If
any failure occurs after reservation, the output root remains present as
forensic evidence. There is no automatic cleanup or retry.

## Deterministic seed recovery governance

Revision 002 may prospectively define only a deterministic replay of the same
pre-specified stream from seed `320031`. This preserves the original bootstrap
estimand rather than selecting a new seed after failure. The draft does not
authorize that replay. Eligibility requires all of the following later events:

1. explicit human approval and freeze of this harness under annotated tag
   `exp3-v2-evaluation-harness-frozen-002`;
2. independent post-freeze verification of the exact tag, commit, artifact
   hashes, runtime and output-path preflight; and
3. a separate explicit human authorization for one Revision 002 replay.

No approval is implied by this protocol, its tests or a future harness freeze.

## Frozen execution paths

- Harness: `/private/tmp/exp3v2-evaluation-harness-002/worktree`
- Runtime: `/private/tmp/exp3v2-evaluation-runtime-001/bin/python3`
- Source: `/private/tmp/exp3v2-evaluation-source-001/worktree`
- Data: `/private/tmp/exp3v2-evaluation-data-001/worktree`
- Verbalization harness: `/private/tmp/exp3v2-evaluation-verbalization-harness-001/worktree`
- Verbalizations: `/private/tmp/exp3v2-evaluation-verbalizations-001/worktree`
- Inference harness: `/private/tmp/exp3v2-evaluation-inference-harness-001/worktree`
- Execution authorization: `/private/tmp/exp3v2-evaluation-authorization-001/worktree`
- Inference outputs: `/private/tmp/exp3v2-evaluation-inference-001/worktree`
- Dedicated output parent: `/private/tmp/exp3v2-evaluation-run-001`
- Output root: `/private/tmp/exp3v2-evaluation-run-001/output`

After both the Revision 002 freeze and a later independent execution approval,
the only prospective production command is:

```bash
/private/tmp/exp3v2-evaluation-runtime-001/bin/python3 \
  /private/tmp/exp3v2-evaluation-harness-002/worktree/phase_b/exp3_v2/evaluate_exp3v2_frozen_predictions.py \
  --harness-manifest /private/tmp/exp3v2-evaluation-harness-002/worktree/phase_b/exp3_v2/EXP3_V2_EVALUATION_HARNESS_MANIFEST_002.json \
  --source-root /private/tmp/exp3v2-evaluation-source-001/worktree \
  --data-root /private/tmp/exp3v2-evaluation-data-001/worktree \
  --verbalization-harness-root /private/tmp/exp3v2-evaluation-verbalization-harness-001/worktree \
  --verbalizations-root /private/tmp/exp3v2-evaluation-verbalizations-001/worktree \
  --inference-harness-root /private/tmp/exp3v2-evaluation-inference-harness-001/worktree \
  --authorization-root /private/tmp/exp3v2-evaluation-authorization-001/worktree \
  --inference-root /private/tmp/exp3v2-evaluation-inference-001/worktree \
  --output-root /private/tmp/exp3v2-evaluation-run-001/output
```

This command is recorded for later review and is not authorized for execution
by the draft or by the preparation operation.

## Regression and freeze requirements

Synthetic tests must prove missing-parent reservation, existing-root refusal,
symlink/non-directory refusal, forensic retention after post-reservation
failure, exact-path enforcement and a complete synthetic production CLI PASS
with an initially absent parent. Instrumented tests must establish the phase
order `boundary/upstream -> runtime -> reservation -> scientific input` and
must show no RNG call before reservation.

The canonical manifest-state test accepts both the current draft and its future
frozen transition, while independently synthesizing a draft to prove that
production remains blocked before freeze.

The future Revision 002 commit must have exact parent
`25dc65bba805f15836f09e9613505bf483199a4f` and may contain only the paths in
the manifest allowlist. The manifest is non-self-referential and records no
prospective commit or tag object. Only the annotated harness tag may eventually
be published; no branch publication is permitted.
