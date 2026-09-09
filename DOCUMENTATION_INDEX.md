# Documentation index

Complete inventory of project documentation, organized by phase and function.
For the scientific reading path, start from [`README.md`](README.md).

## Entry points

| Document | Description |
|---|---|
| [`README.md`](README.md) | Project orientation: research objective, main result, project status, repository map |
| [`AUDIT_GUIDE.md`](AUDIT_GUIDE.md) | Independent verification path for all frozen results |

## Project planning and literature

| Document | Description |
|---|---|
| [`docs/lit_review/FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md`](docs/lit_review/FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md) | Pre-submission experiment plan for IEEE BigData 2026 (Rev. 2) |
| [`docs/lit_review/FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md`](docs/lit_review/FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md) | Targeted literature review for BigData 2026 positioning |
| [`docs/related_work_scan.md`](docs/related_work_scan.md) | Broader related-work scan beyond the targeted review |

## Walkthrough and explanatory material

| Document | Description |
|---|---|
| [`docs/fot_walkthrough_conversazione.html`](docs/fot_walkthrough_conversazione.html) | Primary scientific/didactic walkthrough (Italian, self-contained HTML) |
| [`docs/paper/FoT_TEP_paper_blueprint.html`](docs/paper/FoT_TEP_paper_blueprint.html) | Paper blueprint: planned structure for the BigData 2026 submission |

## Phase A — Methodology

| Document | Description |
|---|---|
| [`supporting_records/phase_a/VERBALIZER_V2_FREEZE.md`](supporting_records/phase_a/VERBALIZER_V2_FREEZE.md) | V2 verbalizer freeze record with frozen hashes |
| [`supporting_records/phase_a/PHASE_A_STATUS.md`](supporting_records/phase_a/PHASE_A_STATUS.md) | Phase A completion status |
| [`supporting_records/phase_a/INJECTION_TIME_VERIFICATION.md`](supporting_records/phase_a/INJECTION_TIME_VERIFICATION.md) | Injection-time verification report |
| [`code/tep_analysis_v2/threshold_calibration_report.md`](code/tep_analysis_v2/threshold_calibration_report.md) | Threshold calibration development report |

## Phase B — Experiment 1 (original held-out evaluation)

| Document | Description |
|---|---|
| [`phase_b/README.md`](phase_b/README.md) | Phase B framework overview, experiment map, and architecture |
| [`phase_b/PHASE_B_PROTOCOL_FREEZE.md`](phase_b/PHASE_B_PROTOCOL_FREEZE.md) | Experiment 1 protocol freeze record |
| [`phase_b/PROTOCOL_IMPLEMENTATION_STATUS.md`](phase_b/PROTOCOL_IMPLEMENTATION_STATUS.md) | Protocol implementation status |
| [`phase_b/FINAL_EVALUATION_RUNBOOK.md`](phase_b/FINAL_EVALUATION_RUNBOOK.md) | Step-by-step runbook for the final evaluation |
| [`phase_b/PHASE_B_PROTOCOL_AMENDMENT_001.md`](phase_b/PHASE_B_PROTOCOL_AMENDMENT_001.md) | Protocol amendment 001 |
| [`phase_b/final_evaluation/EVALUATION_REPORT.md`](phase_b/final_evaluation/EVALUATION_REPORT.md) | Experiment 1 frozen evaluation report with primary and secondary metrics |
| [`phase_b/heldout/HELDOUT_GENERATION_SUMMARY.md`](phase_b/heldout/HELDOUT_GENERATION_SUMMARY.md) | Held-out dataset generation summary |
| [`phase_b/heldout/PHASE_B_HELDOUT_FREEZE.md`](phase_b/heldout/PHASE_B_HELDOUT_FREEZE.md) | Held-out freeze record |
| [`phase_b/heldout/SIMULATOR_PARENT_AUDIT.md`](phase_b/heldout/SIMULATOR_PARENT_AUDIT.md) | MATLAB simulator parent commit audit |
| [`phase_b/insights/FINAL_INSIGHT_GENERATION_REPORT.md`](phase_b/insights/FINAL_INSIGHT_GENERATION_REPORT.md) | Insight generation report |
| [`phase_b/reports/LLM_CAPABILITY_PROBE.md`](phase_b/reports/LLM_CAPABILITY_PROBE.md) | LLM capability probe report |

## Phase B — Experiment 3 (closed incomplete)

| Document | Description |
|---|---|
| [`phase_b/exp3/EXP3_FRESH_RUN_PROTOCOL.md`](phase_b/exp3/EXP3_FRESH_RUN_PROTOCOL.md) | Exp3 prospective protocol (inherited by Exp3 V2) |
| [`phase_b/exp3/RNG_RUNTIME_VALIDATION.md`](phase_b/exp3/RNG_RUNTIME_VALIDATION.md) | MATLAB RNG runtime validation |
| [`phase_b/exp3/EXP3_POST_FREEZE_HOTFIX_001.md`](phase_b/exp3/EXP3_POST_FREEZE_HOTFIX_001.md) | Post-freeze hotfix 001 |
| [`phase_b/exp3/EXP3_POST_FREEZE_HOTFIX_002.md`](phase_b/exp3/EXP3_POST_FREEZE_HOTFIX_002.md) | Post-freeze hotfix 002 |
| [`phase_b/exp3/EXP3_POST_FREEZE_HOTFIX_003.md`](phase_b/exp3/EXP3_POST_FREEZE_HOTFIX_003.md) | Post-freeze hotfix 003 |

## Phase B — Experiment 3 V2 (confirmatory revision)

No canonical tracked documentation for this revision is present in the current
checkout.

## Phase B — Experiment 2 Qwen (cross-model consumer)

The Qwen lane is complete and frozen. Its bounded conclusion is consumer-side:
B's advantage persists with one open-weight consumer in the examined
configuration; the experiment does not establish universal portability or an
end-to-end open-weight replica.

| Document or artifact | Role | Frozen milestone |
|---|---|---|
| [`phase_b/exp2/qwen/evaluation/EVALUATION_REPORT.md`](phase_b/exp2/qwen/evaluation/EVALUATION_REPORT.md) | Human-readable canonical evaluation | `phase-b-exp2-qwen-results-frozen-001` |
| [`phase_b/exp2/qwen/evaluation/evaluation_results.json`](phase_b/exp2/qwen/evaluation/evaluation_results.json) | Canonical machine-readable metrics | `phase-b-exp2-qwen-results-frozen-001` |
| [`phase_b/exp2/qwen/evaluation/bootstrap_results.json`](phase_b/exp2/qwen/evaluation/bootstrap_results.json) | Frozen paired bootstrap intervals | `phase-b-exp2-qwen-results-frozen-001` |
| [`phase_b/exp2/qwen/evaluation/primary_metrics.csv`](phase_b/exp2/qwen/evaluation/primary_metrics.csv) | Primary locally-unseen metrics | `phase-b-exp2-qwen-results-frozen-001` |
| [`phase_b/exp2/qwen/evaluation/secondary_metrics.csv`](phase_b/exp2/qwen/evaluation/secondary_metrics.csv) | Secondary local-seen, Normal, and overall metrics | `phase-b-exp2-qwen-results-frozen-001` |
| [`docs/audits/EXP2_QWEN_EVALUATOR_REVIEW.md`](docs/audits/EXP2_QWEN_EVALUATOR_REVIEW.md) | Independent pre-evaluation review | Canonical audit |
| [`docs/audits/EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW_R2.md`](docs/audits/EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW_R2.md) | Independent scientific results review; `GO WITH LIMITATIONS` | Canonical audit |

Tag targets:

- `phase-b-exp2-qwen-protocol-frozen-001` → `d9bb95c31bdeb2f1608aaedc52f25b98de9bbf96`;
- `phase-b-exp2-qwen-predictions-frozen-001` → `a4f264c210873536c989ebd99aa2c6cf9857c85c`;
- `phase-b-exp2-qwen-evaluator-frozen-001` → `a8f9884dfe2150a89131ba604b34ff1f6914f6e9`;
- `phase-b-exp2-qwen-results-frozen-001` → `37195cf2c5076b5da724b857f10e157177654cac`.

## Condition C R10 — centralized pooled reference

Condition C is the **centralized full-information pooled ICL post-hoc
exploratory reference**. “Full-information” is limited to frozen prompt-facing
artifacts. Its source-of-truth chain is separate from the primary A/B/E result
and is frozen by the three Condition C R10 tags.

| Document or artifact | Role | Status and milestone | Source-of-truth tier |
|---|---|---|---|
| [`icl/PLAN_CENTRAL_POOLED_ICL.md`](icl/PLAN_CENTRAL_POOLED_ICL.md) | Design rationale, implementation plan, guardrails, and completion checklist | Completed under `condition-c-freeze-r10`; execution closure recorded after results review | Canonical scientific documentation |
| [`icl/full_evaluation/c_predictions_manifest.json`](icl/full_evaluation/c_predictions_manifest.json) | SHA-256, count, and schedule binding for 45 raw prediction records | Frozen by `condition-c-predictions-frozen-r10` | Frozen scientific artifact |
| [`icl/full_evaluation/c_aggregate_manifest.json`](icl/full_evaluation/c_aggregate_manifest.json) | Integral binding of 15 aggregates to raw records and schedule | Frozen by `condition-c-predictions-frozen-r10` | Frozen scientific artifact |
| [`icl/full_evaluation/evaluation_results_c.json`](icl/full_evaluation/evaluation_results_c.json) | Canonical metrics, descriptive C−B delta, bootstrap, and integrity record | Frozen by `condition-c-results-frozen-r10` | Frozen scientific artifact |
| [`docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md`](docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md) | Independent scientific and implementation review; verdict `GO WITH LIMITATIONS` | Commit `da64287a5c0d4f70a4fd8ae9abce3d313cd88fd0` | Canonical scientific documentation |

Tag targets:

- `condition-c-freeze-r10` → `60ccc7539714e909aae7318cc72031d7acdd4e78`;
- `condition-c-predictions-frozen-r10` → `8d6b7a0636e9a15f0ebbd32ed0f9e2ce4faea30a`;
- `condition-c-results-frozen-r10` → `89e4caebe635973ef438d4b601bb4f761417193a`.

## Audits

| Document | Description |
|---|---|
| [`docs/audits/README.md`](docs/audits/README.md) | Audit index |
| [`docs/audits/EXP3_FIRST_RUN_READINESS_AUDIT.md`](docs/audits/EXP3_FIRST_RUN_READINESS_AUDIT.md) | Exp3 first-run readiness audit |
| [`docs/audits/EXP3_PREFREEZE_AUDIT_REPORT.md`](docs/audits/EXP3_PREFREEZE_AUDIT_REPORT.md) | Exp3 pre-freeze audit report |
| [`docs/audits/EXP3_ATTEMPT_EXHAUSTION_AUDIT.md`](docs/audits/EXP3_ATTEMPT_EXHAUSTION_AUDIT.md) | Exp3 attempt-exhaustion audit (closure justification) |
| [`docs/audits/EXP3_HOTFIX_001_MICROAUDIT.md`](docs/audits/EXP3_HOTFIX_001_MICROAUDIT.md) | Hotfix 001 micro-audit |
| [`docs/audits/EXP3_HOTFIX_002_MICROAUDIT.md`](docs/audits/EXP3_HOTFIX_002_MICROAUDIT.md) | Hotfix 002 micro-audit |
| [`docs/audits/EXP3_HOTFIX_003_MICROAUDIT.md`](docs/audits/EXP3_HOTFIX_003_MICROAUDIT.md) | Hotfix 003 micro-audit |
| [`docs/audits/EXP3V2_FIRST_RUN_PREFLIGHT.md`](docs/audits/EXP3V2_FIRST_RUN_PREFLIGHT.md) | Exp3 V2 first-run preflight check |
| [`docs/audits/EXP3V2_FINAL_FREEZE_AUDIT.md`](docs/audits/EXP3V2_FINAL_FREEZE_AUDIT.md) | Exp3 V2 final freeze audit |
| [`docs/audits/EXP3V2_DOCUMENTATION_INVENTORY_2026-09-03.md`](docs/audits/EXP3V2_DOCUMENTATION_INVENTORY_2026-09-03.md) | Full documentation inventory (2026-09-03) |
| [`docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md`](docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md) | Independent review of the frozen Condition C R10 evaluation; `GO WITH LIMITATIONS` |
| [`docs/audits/EXP2_QWEN_EVALUATOR_REVIEW.md`](docs/audits/EXP2_QWEN_EVALUATOR_REVIEW.md) | Independent review of the corrected Qwen evaluator before offline evaluation |
| [`docs/audits/EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW_R2.md`](docs/audits/EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW_R2.md) | Canonical independent review of the frozen Qwen results; `GO WITH LIMITATIONS` |

## Operational prompts

| Document | Description |
|---|---|
| [`docs/prompts/README.md`](docs/prompts/README.md) | Prompts index |
| [`docs/prompts/PROJECT_HANDOFF_PROMPT.md`](docs/prompts/PROJECT_HANDOFF_PROMPT.md) | AI session handoff prompt |
| [`docs/prompts/CODEX_PROMPT_EXP3_CLOSE_AND_V2.md`](docs/prompts/CODEX_PROMPT_EXP3_CLOSE_AND_V2.md) | Exp3 closure and Exp3 V2 setup prompt |
| [`docs/prompts/FoT_setup_prompt_server.md`](docs/prompts/FoT_setup_prompt_server.md) | Server-side FoT execution setup prompt |

## Narratives and synthesis

| Document | Description |
|---|---|
| [`supporting_records/narratives/FOT_PROJECT_TECHNICAL_NARRATIVE.md`](supporting_records/narratives/FOT_PROJECT_TECHNICAL_NARRATIVE.md) | Comprehensive technical narrative of the FoT project |
| [`supporting_records/narratives/FOT_PROJECT_LLM_REFERENCE.md`](supporting_records/narratives/FOT_PROJECT_LLM_REFERENCE.md) | LLM reference guide for project context |
| [`supporting_records/narratives/FOT_TEP_POC_FINAL_SYNTHESIS.md`](supporting_records/narratives/FOT_TEP_POC_FINAL_SYNTHESIS.md) | Final synthesis of the TEP proof-of-concept |
| [`supporting_records/communication_characterization/COMMUNICATION_PAYLOAD_REPORT.md`](supporting_records/communication_characterization/COMMUNICATION_PAYLOAD_REPORT.md) | FoT communication payload characterization report |

## Historical (superseded)

| Document | Description |
|---|---|
| [`supporting_records/historical/PHASE_B_EXPERIMENT_DESIGN.md`](supporting_records/historical/PHASE_B_EXPERIMENT_DESIGN.md) | Phase B design spec V1 (superseded by V2) |
| [`supporting_records/historical/PHASE_B_EXPERIMENT_DESIGN_V2.md`](supporting_records/historical/PHASE_B_EXPERIMENT_DESIGN_V2.md) | Phase B design spec V2 (superseded by frozen protocol) |

## Papers

| Document | Description |
|---|---|
| [`papers/README.md`](papers/README.md) | Papers index |
| [`papers/Federation_Over_text_paper.pdf`](papers/Federation_Over_text_paper.pdf) | Yao et al. 2026 — Federation over Text (the method this project applies) |

## Figures

| Document | Description |
|---|---|
| [`docs/figures/FIGURE_MANIFEST.md`](docs/figures/FIGURE_MANIFEST.md) | Figure manifest with descriptions |
