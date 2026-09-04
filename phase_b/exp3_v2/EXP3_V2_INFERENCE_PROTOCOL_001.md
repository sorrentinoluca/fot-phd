# EXP3_V2 Inference Protocol 001 — Frozen Harness

Status: `HARNESS_FROZEN_FOR_INFERENCE`

Prospective annotated tag: `exp3-v2-inference-harness-frozen-001`

This protocol prepares the diagnostic inference boundary and a single-call
synthetic transport sentinel. The harness freeze alone authorizes neither the
sentinel nor batch inference. A successful sentinel must be followed by a
separate human-approved execution-authorization freeze before any of the 1,080
jobs can run. This protocol never authorizes prediction evaluation, accuracy
calculation, evaluator mapping join, or inference-data freeze.

## Immutable upstream boundaries

The inference harness is bound to these four annotated tags and their exact
objects and peeled commits:

| Tag | Tag object | Peeled commit |
|---|---|---|
| `exp3-v2-heldout-frozen-002` | `eaddc2c0791febcccce6412c0a9cc2cf81b3cb21` | `6f88abdecc25e015064e5fc2c59000f8a1a0bc7e` |
| `exp3-v2-heldout-data-frozen-001` | `34319bbb28fcedadd15acc5dfa2183b3fe733ce3` | `7bcf309910920b52c485125312599d1ded9c4c74` |
| `exp3-v2-verbalization-harness-frozen-001` | `b2ac5c24835e1f5817baa0e1e8ba13d498777e7d` | `0ca1ebf339a49c78908e00f65093aeccccc1616f` |
| `exp3-v2-verbalizations-frozen-001` | `4eeb14e77c5d5b45395da0d88012bcf30cea83ea` | `4159fba5e4d23cbc9af62c2aad72f11eda1491db` |

The final verbalization tag supplies exactly thirty neutral-text files in its
canonical manifest order. Structured verbalizations and workbook data are not
inference inputs. Absolute source paths are never used.

## Schedule

No RNG and no schedule seed exist. Iterate cases in the frozen order, then
`agent_1` through `agent_4`, then repetitions 1 through 3. Each tuple is a
block. Select its condition order by `block_index mod 3`:

1. `0`: A, B, E
2. `1`: B, E, A
3. `2`: E, A, B

The immutable schedule has 360 blocks and 1,080 sequential jobs. Each
condition has 360 jobs and appears exactly 120 times at each position.

## Prompt and condition isolation

The runner reuses, unchanged and hash-checked, the frozen Experiment 1 Phase-B
prompt templates, local examples, insight library, B/E peer libraries,
derangements, strict parser, retry rule, aggregation rule and OpenAI adapter.

- Only the selected neutral-text bytes enter `CASE TO DIAGNOSE`.
- Case identifiers, paths, workbook names, real fault labels and evaluator
  mappings are forbidden in rendered prompts.
- A receives no insight library.
- B receives six peer-only insights.
- E receives the same peer observations with only opaque pseudolabels changed
  by the allowlisted derangement file.
- The runner never opens or imports the real-to-opaque evaluator mapping.
- Each request is independent: no stored response, conversation, session,
  thread, previous response ID, cross-condition state or cross-job state.

## Provider configuration

Requests are sequential with process concurrency one. The only permitted
provider settings are:

- OpenAI Responses API `/v1/responses`;
- requested and returned model `gpt-5.6-terra`;
- reasoning effort `medium`;
- temperature omitted;
- provider seed omitted;
- maximum output 512 tokens;
- strict JSON Schema output;
- `store=false`;
- 120-second SDK timeout;
- SDK automatic retries disabled.

The local structural policy permits the initial request plus no more than two
correction requests. A third invalid response becomes a recorded
`parse_failure` abstention. A provider or transport exception is not retried.

## Durable state machine

For every attempt, the runner atomically writes and fsyncs a request-intent
file before submission. Immediately after a provider response returns, it
atomically writes and fsyncs the complete response journal. Only then may it
validate and atomically record the repetition outcome.

An intent without a durable response is `AMBIGUOUS`. Every resume scans the
complete journal before constructing a production provider client. If any
ambiguous state exists, resume stops and cannot repeat the request. Resolution
requires a separate human-reviewed governance action; this harness provides no
automatic resolution or retry.

The external output root has an exclusive `O_EXCL` lock. An existing lock is
never removed automatically or treated as stale based on PID or age. The
process removes only the lock that it acquired, and only during an orderly
exit. A crash therefore leaves a lock requiring human review.

Resume skips only records that validate against schedule position, exact
prompt/input hashes, journal response bytes, provider/model identity, schema,
retry accounting and token accounting.

## Runtime

The exact runtime candidate is:

`/private/tmp/exp3v2-inference-runtime-001/bin/python3`

It resolves to Python 3.13.9 at `/opt/anaconda3/bin/python3.13`. The complete
environment and every compatible wheel hash are recorded in
`EXP3_V2_INFERENCE_RUNTIME_LOCK_001.json` and
`EXP3_V2_INFERENCE_REQUIREMENTS_001.txt`. Direct code requirements are
`openai==3.6.0`, `jsonschema==4.25.0`, and `numpy==2.3.5`; all transitive
distributions are exact and no unlisted distribution is accepted.

The runtime validator uses `importlib.metadata`, validates the entire
environment, and neither reads nor checks `OPENAI_API_KEY`. The frozen OpenAI
adapter accesses that variable only after all preflight and ambiguity checks.

## Exact checkout commands to freeze

The following operation is prospective and must not be executed before the
harness tag exists. Every target path must be absent.

```bash
git init --bare /private/tmp/exp3v2-inference-tags-001.git
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git remote add origin https://github.com/sorrentinoluca/fot-phd.git
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git fetch --no-tags origin refs/tags/exp3-v2-heldout-frozen-002:refs/tags/exp3-v2-heldout-frozen-002
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git fetch --no-tags origin refs/tags/exp3-v2-heldout-data-frozen-001:refs/tags/exp3-v2-heldout-data-frozen-001
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git fetch --no-tags origin refs/tags/exp3-v2-verbalization-harness-frozen-001:refs/tags/exp3-v2-verbalization-harness-frozen-001
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git fetch --no-tags origin refs/tags/exp3-v2-verbalizations-frozen-001:refs/tags/exp3-v2-verbalizations-frozen-001
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git fetch --no-tags origin refs/tags/exp3-v2-inference-harness-frozen-001:refs/tags/exp3-v2-inference-harness-frozen-001
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git worktree add --detach /private/tmp/exp3v2-inference-source-001/worktree 'refs/tags/exp3-v2-heldout-frozen-002^{}'
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git worktree add --detach /private/tmp/exp3v2-inference-data-001/worktree 'refs/tags/exp3-v2-heldout-data-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git worktree add --detach /private/tmp/exp3v2-inference-verbalization-harness-001/worktree 'refs/tags/exp3-v2-verbalization-harness-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git worktree add --detach /private/tmp/exp3v2-inference-verbalizations-001/worktree 'refs/tags/exp3-v2-verbalizations-frozen-001^{}'
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git worktree add --detach /private/tmp/exp3v2-inference-harness-001/worktree 'refs/tags/exp3-v2-inference-harness-frozen-001^{}'
```

## Exact future batch execution — locked until authorization freeze

The output parent may exist, but
`/private/tmp/exp3v2-inference-run-001/output` must not exist before the first
invocation. This command must not be run after the harness freeze alone. It
requires both sentinel PASS and the separate execution-authorization tag plus
its recorded explicit human approval.

```bash
/private/tmp/exp3v2-inference-runtime-001/bin/python3 \
  /private/tmp/exp3v2-inference-harness-001/worktree/phase_b/exp3_v2/run_exp3v2_inference.py \
  --manifest /private/tmp/exp3v2-inference-harness-001/worktree/phase_b/exp3_v2/EXP3_V2_INFERENCE_HARNESS_MANIFEST_001.json \
  --source-root /private/tmp/exp3v2-inference-source-001/worktree \
  --data-root /private/tmp/exp3v2-inference-data-001/worktree \
  --verbalization-harness-root /private/tmp/exp3v2-inference-verbalization-harness-001/worktree \
  --verbalizations-root /private/tmp/exp3v2-inference-verbalizations-001/worktree \
  --authorization-manifest /private/tmp/exp3v2-inference-authorization-001/worktree/phase_b/exp3_v2/EXP3_V2_INFERENCE_EXECUTION_AUTHORIZATION_MANIFEST_001.json \
  --authorization-root /private/tmp/exp3v2-inference-authorization-001/worktree \
  --output-root /private/tmp/exp3v2-inference-run-001/output
```

The command contains no credential. `OPENAI_API_KEY` must already be provided
to the process environment by an authorized operator and must never be read,
printed, hashed, copied or persisted by preparation or verification tools.

## One-call live API sentinel

After the harness tag exists, a separate explicit human approval may authorize
exactly one provider submission under sentinel identity
`EXP3V2-INFERENCE-SENTINEL-001`. The sentinel uses the hash-frozen synthetic
prompt and synthetic label space embedded in
`run_exp3v2_inference_sentinel.py`. It contains no EXP3_V2 case text or ID,
insight, derangement, evaluator mapping or real label.

It uses the unchanged frozen `OpenAIAdapter`, Responses API, strict diagnostic
schema, Python runtime, `gpt-5.6-terra`, reasoning effort `medium`, 512 output
tokens, `store=false`, no temperature, no provider seed, a 120-second timeout
and SDK retries zero. It has one call site and no correction or retry path.

The sentinel root is separate from the scientific job output root and must not
exist before invocation:

`/private/tmp/exp3v2-inference-sentinel-001`

The exact prospective command is:

```bash
/private/tmp/exp3v2-inference-runtime-001/bin/python3 \
  /private/tmp/exp3v2-inference-harness-001/worktree/phase_b/exp3_v2/run_exp3v2_inference_sentinel.py \
  --manifest /private/tmp/exp3v2-inference-harness-001/worktree/phase_b/exp3_v2/EXP3_V2_INFERENCE_HARNESS_MANIFEST_001.json \
  --sentinel-root /private/tmp/exp3v2-inference-sentinel-001
```

Before submission, the wrapper verifies the frozen annotated harness tag,
detached clean checkout, every harness artifact, the 20-package runtime, the
fixed prompt hash and root absence. It then writes and fsyncs
`sentinel_intent.json`. A returned provider response is immediately recorded
atomically and fsynced as `sentinel_receipt.json`, before semantic validation.
PASS or FAIL evidence is then written atomically as
`EXP3_V2_INFERENCE_SENTINEL_EVIDENCE_001.json`.

An intent without a receipt is `AMBIGUOUS`. It may never be retried
automatically. Any provider submission exhausts SENTINEL-001: transport
ambiguity, wrong returned model, invalid structured output or synthetic label,
invalid token accounting, or any later failure requires a newly reviewed
harness revision and new sentinel identity. A pre-submission preflight failure
that created no intent does not consume the sentinel.

PASS requires one and only one provider submission, a successful HTTP response,
returned model exactly `gpt-5.6-terra`, the exact synthetic result under the
strict diagnostic parser, and non-negative integer input/output/total tokens
with input plus output equal to total. The portable verifier command is:

```bash
/private/tmp/exp3v2-inference-runtime-001/bin/python3 \
  /private/tmp/exp3v2-inference-harness-001/worktree/phase_b/exp3_v2/verify_exp3v2_inference_sentinel.py \
  --manifest /private/tmp/exp3v2-inference-harness-001/worktree/phase_b/exp3_v2/EXP3_V2_INFERENCE_HARNESS_MANIFEST_001.json \
  --sentinel-root /private/tmp/exp3v2-inference-sentinel-001
```

No sentinel artifact may be written below
`/private/tmp/exp3v2-inference-run-001/output`, and the sentinel may not create
scientific request-journal, repetition, aggregate, metadata or hash-manifest
files.

## Post-sentinel execution authorization

Sentinel PASS still leaves the batch runner locked. A separate review must copy
the three sentinel artifacts byte-identically into
`phase_b/exp3_v2/inference_sentinel_001/`, create
`EXP3_V2_INFERENCE_EXECUTION_AUTHORIZATION_MANIFEST_001.json`, and obtain
explicit human approval. Its commit must have the exact harness commit as its
sole parent, add exactly those three evidence artifacts and the final
authorization manifest, and modify or delete no harness path.

The final authorization manifest must satisfy the frozen schema, use status
`FROZEN_BEFORE_INFERENCE`, bind the harness tag/commit/manifest, sentinel ID,
exactly one submission, evidence/intent/receipt hashes, returned model and
token-accounting PASS, and unchanged schedule, runner and runtime-lock hashes.
It is non-self-referential. Only then may the annotated tag
`exp3-v2-inference-execution-frozen-001` be created and published.

The authorization template frozen with the harness is never edited. The final
manifest is a new file in the authorization commit. A detached authorization
checkout is created prospectively with:

```bash
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git fetch --no-tags origin refs/tags/exp3-v2-inference-execution-frozen-001:refs/tags/exp3-v2-inference-execution-frozen-001
git --git-dir=/private/tmp/exp3v2-inference-tags-001.git worktree add --detach /private/tmp/exp3v2-inference-authorization-001/worktree 'refs/tags/exp3-v2-inference-execution-frozen-001^{}'
```

The batch runner checks this manifest and annotated tag, sole-parent
relationship, additions-only tree diff, copied sentinel evidence and all hashes
before runtime validation, neutral-text loading, credential access or provider
client creation.

## Exact post-inference verification

```bash
/private/tmp/exp3v2-inference-runtime-001/bin/python3 \
  /private/tmp/exp3v2-inference-harness-001/worktree/phase_b/exp3_v2/verify_exp3v2_inference.py \
  --manifest /private/tmp/exp3v2-inference-harness-001/worktree/phase_b/exp3_v2/EXP3_V2_INFERENCE_HARNESS_MANIFEST_001.json \
  --source-root /private/tmp/exp3v2-inference-source-001/worktree \
  --data-root /private/tmp/exp3v2-inference-data-001/worktree \
  --verbalization-harness-root /private/tmp/exp3v2-inference-verbalization-harness-001/worktree \
  --verbalizations-root /private/tmp/exp3v2-inference-verbalizations-001/worktree \
  --authorization-manifest /private/tmp/exp3v2-inference-authorization-001/worktree/phase_b/exp3_v2/EXP3_V2_INFERENCE_EXECUTION_AUTHORIZATION_MANIFEST_001.json \
  --authorization-root /private/tmp/exp3v2-inference-authorization-001/worktree \
  --output-root /private/tmp/exp3v2-inference-run-001/output
```

The verifier performs structural, journal, hash, ordering, token-accounting and
deterministic-finalization checks only. It cannot load evaluator truth or
calculate accuracy.

## Failure and later freeze

No output, journal, failure record or lock may be deleted automatically after
a failed or ambiguous execution. No API call may be repeated without a new
human decision consistent with the durable journal. Completed outputs remain
outside all clean source worktrees.

After successful portable verification, a separate review must define a
tag-only inference-data freeze, prospectively named
`exp3-v2-inference-frozen-001`. That later operation is not authorized here.
