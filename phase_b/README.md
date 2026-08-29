# Phase B Federation-over-Text framework

Status: **implemented for development/plumbing, not protocol-frozen**.

This directory implements the experimental machinery for the Phase B FoT PoC.
It does not select an LLM, generate definitive insights, open the independent
held-out, or run the final A/B/E evaluation.

## Architecture

Four agents share one global opaque label space. Every agent owns two local
Normal examples and two examples of exactly one opaque fault pseudoclass. The
other three fault pseudoclasses are locally unseen.

```text
frozen V2 neutral text
       |
       +--> local labeled examples (two local + two Normal)
       |
       +--> A: no peer insights
       +--> B: six peer insights, two from each other agent
       +--> E: the same six patterns/IDs/order with one fixed label derangement
       |
       +--> strict JSON diagnosis
       +--> evaluator-side truth, paired metrics, physical-run cluster bootstrap
```

Relevant modules:

- `config/`: protocol schema and unresolved execution settings;
- `config/evaluator_side/`: real-to-opaque map, source metadata, fixed E maps;
- `local_knowledge/`: deterministic batch-1/2 V2 neutral examples;
- `prompts/`: insight and diagnosis templates plus anti-leakage scanner;
- `insights/`: exact-two schema, provenance validation, peer filtering, E corruption;
- `conditions/`: A/B/E rendering, strict parsers, bounded deterministic retry;
- `evaluation/`: run records, token logs, offline metrics, clustered bootstrap;
- `tests/`: software/fixture tests only;
- `heldout/`: already frozen independently; not an input to this framework task.

## Pseudolabel protection

The four prompt-facing pseudolabels are fixed equal-length opaque tokens:

```text
CLS-ZOGAA  CLS-OJNSG  CLS-R463B  CLS-Z3ISU
```

Their meaning exists only in
`config/evaluator_side/pseudolabel_mapping.json`. That file and other evaluator
metadata must never be concatenated into a prompt. `Normal` remains unchanged.
Insight IDs use the unrelated sequential form `INS-001` onward and contain no
class, pseudolabel, or agent-class relationship.

The leakage scanner covers prompt templates, local knowledge, and every rendered
prompt. It rejects real benchmark identifiers, numbered real-class terms,
benchmark-name/class combinations, and semantic `Class-A/B/C/D` aliases.

## Data boundaries

Allowed before protocol freeze:

- fault development batches 1–5 for local knowledge and future insight generation;
- deterministic local examples: batch 1 and batch 2 only;
- Normal N1–N5 for the frozen baseline/local reference;
- batches 6–7 only for parser, schema, rendering, retry, or dry-run plumbing.

Forbidden in development:

- original batches 8–10;
- Normal N8–N10;
- every workbook under `tep_heldout/`;
- every filename listed in the frozen held-out manifest, wherever copied.

`guard.py` is fail-closed for every new framework data path. The only modeled
exception is the already frozen integrity verifier, and only when its caller
sets both `purpose="integrity_verification"` and an explicit integrity flag.
Ordinary tests never invoke that exception and never open an held-out workbook.

## Local knowledge

`local_knowledge/build_local_examples.py` mechanically selects batch 1 and 2 for
each local pseudoclass and N1/N2 for Normal. It applies the frozen V2 config,
feature layer, and renderer. The prompt-facing JSON contains only:

```text
example_id, pseudolabel, neutral_text
```

No structured numerical JSON or evaluator-side source identity is included.
The source association is stored separately under `config/evaluator_side/`.

## Conditions

- **A — isolated:** label space, four local examples, neutral case text; no peer block.
- **B — FoT:** A plus exactly six peer insights: two from each other agent;
  no self insight and no Normal insight.
- **E — corrupted control:** the B list with identical IDs, provenance, scope,
  observed patterns, count, and order. Only `pseudolabel` changes through one
  fixed evaluator-side derangement per receiving agent. All opaque labels have
  equal length, so B and E have equal character count before provider tokenization.

The three diagnostic templates are intentionally byte-identical. The only
rendered difference is the peer-insight block: absent in A, genuine in B,
label-deranged in E.

No definitive insight library exists yet. Future generation must return exactly
two insights per local fault pseudoclass, with no confidence, ranking, merge,
deduplication, manual editing, or adaptive selection.

## Output and retry

The strict output keys are:

```json
{
  "predicted_label": "opaque label or Normal",
  "abstain": false,
  "used_insight_ids": [],
  "reasoning_summary": "..."
}
```

Unknown labels, extra keys, duplicated JSON keys, markdown fences, unavailable
insight IDs, invalid types, and empty reasoning are rejected. Abstention may use
`predicted_label: null`, but is always incorrect in primary accuracy. A fixed
correction suffix is used for at most two retries; no retry changes the examples,
insights, label space, case input, or schema.

## Metrics and statistical unit

The evaluator reports unseen, seen, and overall accuracy; paired B−A and E−A
deltas; helped/harmed/unchanged; abstention; recall by opaque pseudolabel;
confusion matrices; and insight-ID usage. Epsilon for the seen comparison is 0.

The primary unseen denominator is expected to be 36 agent-case observations per
condition and repetition: 12 physical fault runs, each unseen to three agents.
These 36 rows are **not 36 independent physical units**. Bootstrap code resamples
`physical_case_id` clusters within true opaque pseudolabel strata, retaining all
agent and repetition rows of every sampled physical run. On final data this is
12 physical fault clusters, three per fault pseudoclass. No post-hoc binary
success threshold or strong significance claim is implemented.

## Execution sequence

1. Keep Phase A hashes fixed.
2. Review the deterministic local examples and prompt plumbing on development.
3. Choose and record model/provider/version; confirm temperature/seed support.
4. Generate exactly two unedited local insights per agent from development only.
5. Validate global insights; build B and frozen E libraries.
6. If needed, use batches 6–7 only for non-accuracy plumbing dry-runs.
7. Decide the final across-R aggregation/reporting rule and freeze all protocol artifacts.
8. Create `phase-b-protocol-frozen` only after researcher approval.
9. Only then invoke the held-out integrity verifier and begin final evaluation.

Current tests:

```bash
python -m unittest discover -s phase_b/tests -v
```

This command uses committed neutral development examples and synthetic inference
fixtures. It does not read held-out workbooks or call an LLM.
