# Phase B protocol implementation status

This status is pre-freeze. It records software readiness, not experimental
results and not approval to access the independent held-out.

## DONE

- Four-agent topology: one opaque fault pseudoclass plus Normal per agent.
- Deterministic opaque pseudolabel scheme and evaluator-only real mapping.
- Equal-length pseudolabels for B/E length control.
- Exact local-example rule: fault batch 1–2 and Normal N1–N2, two per class.
- Frozen V2 neutral rendering of ten unique development examples.
- Prompt-facing/evaluator-side metadata separation; no structured JSON in diagnostic inputs.
- Insight schema with provenance, opaque IDs, exact-two validation, deterministic ordering.
- Peer-only filter: six insights per receiver; no self and no Normal.
- Fixed per-agent three-label derangements for condition E.
- E invariant checks: same IDs/count/order/text/provenance; only label association changes.
- Byte-identical diagnostic templates for A/B/E and separate insight-generation template.
- Strict diagnostic and insight JSON parsing; no confidence field.
- Deterministic bounded invalid-output retry policy.
- Anti-leakage scanning of prompt-facing files and rendered prompts.
- Held-out path/manifest-filename guard with explicit verifier-only exception.
- Provider-neutral run-record schema with required provenance fields.
- Provider-reported token-count logging interface with character-count fallback.
- Offline accuracy, delta, transfer, abstention, recall, confusion, and insight-use metrics.
- Per-repetition counts and per-agent primary delta reporting.
- Paired, pseudolabel-stratified physical-cluster bootstrap infrastructure.
- Software tests for all requested invariants; Phase A frozen-hash regression test.

## NOT DONE

- No LLM/provider selected or called.
- No definitive local insight generated.
- No manual insight editing or selection performed.
- No batch 6–7 dry-run performed; it was unnecessary for current software tests.
- No original batch 8–10 opened by this implementation.
- No independent held-out workbook opened, verbalized, or inferred on.
- No A/B/E final run record exists.
- No Phase B performance result, table, plot, or claim calculated.
- No paper modified.
- No `phase-b-protocol-frozen` commit or tag created.

## REQUIRES RESEARCHER DECISION

- LLM provider and exact model/version; both are mandatory null fields and block execution.
- Confirmation that the selected API supports temperature 0 and the fixed seed;
  otherwise the supported fixed alternative must be recorded before freeze.
- Provider-specific tokenizer/accounting source and context/output-token limits.
- Final across-R rule: report repetitions separately/pooled as currently supported,
  or add a pre-specified deterministic majority aggregation before protocol freeze.
- Whether the implementation default of two retries is retained in the frozen protocol.
- Whether 10,000 bootstrap draws and seed `20260829` are retained for final reporting.
- Researcher review/approval of prompt wording before definitive insight generation.

None of these decisions authorizes tuning against diagnostic accuracy on batches
6–7 or any access to the independent held-out before the protocol freeze.
