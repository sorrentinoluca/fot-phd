# EXP2 Qwen Evaluator Amendment 001

## Scope

After the EXP2 Qwen predictions were frozen, and before any offline evaluation
was run, a provenance defect was identified in
`phase_b/exp2/qwen/evaluate_qwen.py`. The Qwen adapter delegated report rendering
to the frozen Experiment 1 evaluator, whose report template identifies the
Experiment 1 Terra inference freeze. Without an adapter-level correction, a
future Qwen report would therefore attribute the Qwen predictions to the wrong
tag and commit.

The canonical EXP2 Qwen predictions freeze is:

- tag: `phase-b-exp2-qwen-predictions-frozen-001`;
- commit: `a4f264c210873536c989ebd99aa2c6cf9857c85c`.

## Amendment

This amendment changes only Qwen evaluator provenance and pre-evaluation
guardrails. It adds fail-closed checks for the predictions freeze tag and
ancestry, the inference manifest contract, record counts, the canonical
artifact set and hashes, the schedule reference and hash, execution metadata,
and the frozen Experiment 1 evaluator-core binding. Future Qwen results, hash
manifest, and human-readable report will record the Qwen freeze explicitly.

The frozen Experiment 1 evaluator core, its bootstrap implementation, and its
metric logic are unchanged and are not duplicated by the Qwen adapter.

## Pre-evaluation integrity statement

No ground truth or pseudolabel mapping was consulted while preparing this
amendment. No metric was calculated, and no offline evaluation was started.
There were no LLM or vLLM calls.

The frozen Qwen predictions and aggregates remained byte-for-byte unchanged,
as did all four inference artifacts:

- `repetition_records.jsonl`;
- `aggregate_records.jsonl`;
- `execution_metadata.json`;
- `inference_output_hash_manifest.json`.

This amendment is exclusively a provenance and guardrail correction made
before evaluation.
