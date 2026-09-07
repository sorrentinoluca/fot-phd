# Independent Audit Guide — Frozen TEP FoT Proof of Concept

## 1. Purpose

This guide provides the shortest independent verification path for the frozen
Tennessee Eastman Process (TEP) Federation over Text proof of concept and its
Condition C centralized pooled reference.

Two reproducibility claims must remain separate:

1. **Scientific verification of the frozen results** — the committed protocol,
   predictions, evaluator, bootstrap, and result artifacts permit independent
   recomputation of the reported Phase B metrics without a new LLM call.
2. **Bit-for-bit regeneration of the physical simulation realizations** — the
   15 raw held-out workbooks are identified cryptographically but are not
   committed, and the original MATLAB RNG state was not recorded. The exact
   random realizations therefore cannot be recreated from the generation
   scripts alone.

No command in this guide performs new LLM inference.

## 2. What can be independently verified

The repository preserves and exposes:

- the frozen Phase A verbalizer, feature implementation, configuration, and
  hashes;
- the Phase B protocol and its execution-order amendment;
- held-out filenames, provenance, size, SHA-256, and structural expectations;
- local examples and their evaluator-side provenance;
- eight final local insights (two per agent) and deterministic peer-only
  libraries;
- the corrupted E control and its zero-fixed-point derangements;
- the frozen 540-request execution schedule;
- 540 individual LLM repetition records;
- 180 `R=3` aggregate prediction records;
- provider/model, retry, token-accounting, and schedule metadata;
- primary, secondary, and per-agent metrics;
- paired helped/harmed counts;
- complete confusion matrices;
- the paired cluster bootstrap and its frozen seed;
- protocol, inference, evaluation, and held-out hash manifests;
- the annotated scientific freeze tags.
- the Condition C R10 code, prediction, aggregate, result, and independent
  review chain.

## 3. Canonical source-of-truth chain

```text
Frozen held-out identity
phase_b/heldout/phase_b_heldout_manifest.csv
        ↓
Frozen neutral verbalizations
phase_b/final_evaluation/heldout_verbalizations_manifest.json
phase_b/final_evaluation/verbalized/
        ↓
Frozen execution schedule
phase_b/final_evaluation/inference_schedule.json
        ↓
Individual provider records
phase_b/final_evaluation/inference/repetition_records.jsonl
        ↓
Frozen R=3 aggregates
phase_b/final_evaluation/inference/aggregate_records.jsonl
        ↓
Deterministic offline evaluator
phase_b/final_evaluation/evaluate_frozen_predictions.py
        ↓
Metrics and bootstrap
phase_b/final_evaluation/{primary_metrics.csv,secondary_metrics.csv,
per_agent_metrics.csv,transfer_counts.csv,confusion_matrices.json,
bootstrap_results.json,evaluation_results.json}
        ↓
Frozen report and evaluation hash manifest
phase_b/final_evaluation/EVALUATION_REPORT.md
phase_b/final_evaluation/evaluation_hash_manifest.json
```

`README.md` and `docs/fot_walkthrough_conversazione.html` explain and navigate
the work; they are not the numerical source of truth. Exact numerical claims
must resolve to the frozen chain above.

## 4. Primary endpoint

The primary analysis concerns fault classes locally unseen by the receiving
agent:

- 12 independent physical fault runs: four fault pseudoclasses × three runs;
- three locally-unseen agents evaluate each physical run;
- 36 correlated agent-case observations per condition;
- A = isolated, B = genuine peer FoT, E = corrupted pseudolabel associations;
- each agent-case-condition is the frozen aggregate of `R=3` repetitions;
- abstention is counted as incorrect;
- statistical uncertainty is clustered by physical case, not by agent-case row.

Expected frozen results:

```text
A = 0/36
B = 31/36
E = 3/36

B−A = +0.8611   preregistered primary contrast
B−E = +0.7778   preregistered specificity/mechanistic contrast
```

The full-precision frozen values are `0.861111111111...` and
`0.777777777777...`. B−E is not the primary endpoint.

## 5. Recalculate results from frozen predictions

### 5.1 Obtain the frozen results state

```bash
git clone https://github.com/sorrentinoluca/fot-phd.git
cd fot-phd
git fetch --tags
git checkout phase-b-results-frozen
```

`phase-b-results-frozen` is an annotated tag whose peeled target must be
`45ec4eed65b263a5803ced7d01064c4672e81e86`.

### 5.2 Install the reference dependencies

The reference runtime is CPython 3.13.9. The committed dependency file pins the
packages used by the Phase A and Phase B audit code.

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5.3 Run the frozen regression suite

```bash
python -m unittest discover -s phase_b/tests -v
```

These tests are local and deterministic. They do not invoke the OpenAI API or
read the excluded raw held-out workbooks.

### 5.4 Re-run the offline evaluator into a temporary directory

The evaluator accepts a real `--output-dir`; using a temporary directory avoids
writing into the committed frozen result directory.

```bash
AUDIT_OUT="$(mktemp -d)"
python phase_b/final_evaluation/evaluate_frozen_predictions.py \
  --output-dir "$AUDIT_OUT"
```

Expected terminal summary:

```text
{"aggregate_source_only": true, "integrity": "PASS", "physical_clusters": 12, "primary_n_per_condition": 36, "status": "COMPLETE"}
```

Compare every deterministic result artifact generated by the evaluator:

```bash
for name in \
  EVALUATION_REPORT.md \
  bootstrap_results.json \
  confusion_matrices.json \
  evaluation_results.json \
  per_agent_metrics.csv \
  primary_metrics.csv \
  secondary_metrics.csv \
  transfer_counts.csv
do
  cmp "$AUDIT_OUT/$name" "phase_b/final_evaluation/$name" || exit 1
done
echo "Offline evaluation artifacts: byte-identical"
```

The temporary `evaluation_hash_manifest.json` is not included in this byte
comparison because it records output paths; verify the committed manifest as
described below.

## 6. Verify artifact integrity

### 6.1 Scientific tag targets

```bash
git rev-parse phase-a-reproducibility-complete^{}
git rev-parse phase-b-heldout-frozen^{}
git rev-parse phase-b-protocol-frozen^{}
git rev-parse phase-b-execution-schedule-frozen^{}
git rev-parse phase-b-inference-frozen^{}
git rev-parse phase-b-results-frozen^{}
```

Expected peeled targets are listed in Section 9.

### 6.2 Protocol, inference, and evaluation manifests

The following standard-library check validates every path recorded in the
three committed manifests:

```bash
python - <<'PY'
import hashlib
import json
from pathlib import Path

root = Path.cwd()

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

manifests = [
    ("phase_b/PHASE_B_PROTOCOL_HASHES.json", "artifacts"),
    ("phase_b/final_evaluation/inference/inference_output_hash_manifest.json", "artifacts"),
    ("phase_b/final_evaluation/evaluation_hash_manifest.json", "evaluation_artifacts"),
]

for manifest_path, field in manifests:
    manifest = json.loads((root / manifest_path).read_text())
    for relative_path, expected in manifest[field].items():
        actual = digest(root / relative_path)
        if actual != expected:
            raise SystemExit(f"FAIL {relative_path}: {actual} != {expected}")
    print(f"PASS {manifest_path}: {len(manifest[field])} artifacts")
PY
```

The offline evaluator additionally checks that:

- `phase-b-inference-frozen` peels to the frozen inference commit;
- the current commit descends from that freeze;
- the inference manifest has immutable pre-evaluation status;
- all inference and protocol hashes match;
- the execution schedule hash matches;
- all 180 aggregate keys and all 15 ground-truth joins are complete;
- denominators, bootstrap strata, and confusion totals are internally
  consistent.

### 6.3 Phase A frozen hashes

```bash
python -m unittest phase_b.tests.test_phase_a_hashes -v
```

This checks the four Phase A files against their frozen SHA-256 values.

## 7. LLM execution provenance

The source of truth is
[`phase_b/final_evaluation/inference/execution_metadata.json`](phase_b/final_evaluation/inference/execution_metadata.json),
supported by
[`phase_b/config/execution_config.json`](phase_b/config/execution_config.json)
and the 540 repetition records.

The committed record states:

| Field | Frozen value |
|---|---|
| Provider | OpenAI |
| Requested/returned model | `gpt-5.6-terra` |
| Reasoning effort | `medium` |
| Temperature / seed | `null`; unsupported by the validated provider path |
| Structured Outputs | strict `true` |
| Repetitions | `R=3` |
| Completed records | 540 individual; 180 aggregate |
| Conditions | A=180, B=180, E=180 repetitions |
| Provider attempts | 541 |
| Structural retries | 1 total, in E |
| Network failures / resume attempts | 0 / 0 |
| Final parse failures | 0 |
| Schedule adherence / statelessness | `true` / `true` |
| Token accounting | complete, from provider usage records |
| Total tokens | 1,207,146 |

The record contains provider request/response identifiers where available, but
no API credentials or authorization headers.

## 8. Held-out data boundary

The 15 raw Phase B `.xlsx` workbooks are intentionally absent from standard
Git history. Their immutable identifiers are committed in
[`phase_b/heldout/phase_b_heldout_manifest.csv`](phase_b/heldout/phase_b_heldout_manifest.csv):
case ID, filename, byte size, SHA-256, workbook schema, and time-axis
expectations.

If the workbooks are supplied separately, verify them without modifying them:

```bash
python phase_b/heldout/verify_heldout_integrity.py \
  --manifest phase_b/heldout/phase_b_heldout_manifest.csv \
  --data-dir /absolute/path/to/the/15/workbooks
```

The verifier checks filename coverage, byte size, SHA-256, XLSX validity,
headers, dimensions, finite values, monotonic time, endpoints, and sampling. It
does not perform diagnostic feature analysis.

The retained MATLAB scripts and generation summary document the held-out
generation procedure, but not every original generation-script state was
preserved. In particular, the first F1 batch-11 script state and a separate
Normal-14 script were not retained; their recorded command sequences are
documented in `HELDOUT_GENERATION_SUMMARY.md`. In addition, the initial MATLAB
RNG state was not recorded, so the original random realizations cannot be
regenerated bit-for-bit. The macOS MEX binary is not itself a blob in the
parent upstream commit; its local hash/equality audit and the corresponding
C-source provenance are documented in `SIMULATOR_PARENT_AUDIT.md`.

Consequently:

- supplied frozen workbooks can be verified byte-for-byte;
- the reported metrics can be recomputed from committed frozen predictions;
- new simulator executions cannot be expected to reproduce the same random
  workbook bytes.

See
[`phase_b/heldout/PHASE_B_HELDOUT_FREEZE.md`](phase_b/heldout/PHASE_B_HELDOUT_FREEZE.md)
and
[`phase_b/heldout/HELDOUT_GENERATION_SUMMARY.md`](phase_b/heldout/HELDOUT_GENERATION_SUMMARY.md)
for the complete boundary.

## 9. Condition C R10 — centralized pooled reference

Condition C is a **centralized full-information pooled ICL post-hoc exploratory
reference**. “Full-information” is scoped to the union of frozen prompt-facing
examples and insights; it does not mean access to all source data or source
texts. No command in this section performs a new LLM call or recomputes the
evaluation metrics.

### 9.1 Frozen chain and artifacts

```text
Code and protocol freeze
condition-c-freeze-r10
        ↓
Raw and aggregate predictions freeze
condition-c-predictions-frozen-r10
icl/inference/{c_records.jsonl,c_aggregate_records.jsonl}
icl/full_evaluation/{c_predictions_manifest.json,c_aggregate_manifest.json}
        ↓
Offline results freeze
condition-c-results-frozen-r10
icl/full_evaluation/evaluation_results_c.json
        ↓
Independent interpretation audit
docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md
```

| Artifact | SHA-256 |
|---|---|
| `icl/inference/c_records.jsonl` | `d64725aee15f0c0c118648cfa74ec9251f711fd70e89ba9af618e49966a56251` |
| `icl/inference/c_aggregate_records.jsonl` | `3cd11f8bd9863976e7e224de28c9b1b22c0710b2dcfde1dee30df44ef2b1c95c` |
| `icl/full_evaluation/c_predictions_manifest.json` | `1513f3a69b10a439014201048367c1b03fc7a7c0e207094b3b73c6739e657985` |
| `icl/full_evaluation/c_aggregate_manifest.json` | `202d7e901f8985ff708f26eaf9bf511afeed856291f0ec4eafa5b624d3b00e1e` |
| `icl/full_evaluation/evaluation_results_c.json` | `1ea60e12ded77e5d7758d71d3d2e863d5f741c91d41a03511c81935061435cd5` |
| `docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md` | `fc9b3316723cd06a3326e35d7e481b5e46ac927b4ca52e1bbee35c9fb423a60a` |

The independent review was committed at
`da64287a5c0d4f70a4fd8ae9abce3d313cd88fd0` and records **GO WITH
LIMITATIONS**.

### 9.2 Verify tags, bytes, and freeze guards

Verify the three annotated tag targets:

```bash
git rev-parse condition-c-freeze-r10^{}
git rev-parse condition-c-predictions-frozen-r10^{}
git rev-parse condition-c-results-frozen-r10^{}
```

The expected targets are listed in Section 10. Verify the six canonical files
without relying on platform-specific checksum utilities:

```bash
python - <<'PY'
import hashlib
from pathlib import Path

expected = {
    "icl/inference/c_records.jsonl": "d64725aee15f0c0c118648cfa74ec9251f711fd70e89ba9af618e49966a56251",
    "icl/inference/c_aggregate_records.jsonl": "3cd11f8bd9863976e7e224de28c9b1b22c0710b2dcfde1dee30df44ef2b1c95c",
    "icl/full_evaluation/c_predictions_manifest.json": "1513f3a69b10a439014201048367c1b03fc7a7c0e207094b3b73c6739e657985",
    "icl/full_evaluation/c_aggregate_manifest.json": "202d7e901f8985ff708f26eaf9bf511afeed856291f0ec4eafa5b624d3b00e1e",
    "icl/full_evaluation/evaluation_results_c.json": "1ea60e12ded77e5d7758d71d3d2e863d5f741c91d41a03511c81935061435cd5",
    "docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md": "fc9b3316723cd06a3326e35d7e481b5e46ac927b4ca52e1bbee35c9fb423a60a",
}
for relative, digest in expected.items():
    actual = hashlib.sha256(Path(relative).read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit(f"FAIL {relative}: {actual} != {digest}")
    print(f"PASS {relative}")
PY
```

Run the fail-closed guards directly; this only validates committed files:

```bash
python - <<'PY'
from icl.evaluation.aggregation_c import verify_aggregate_freeze
from icl.evaluation.evaluate_c_predictions import (
    verify_c_predictions_freeze,
    verify_evaluator_freeze,
)
from icl.runner.run_c_inference import (
    FREEZE_MANIFEST_PATH,
    verify_inference_freeze,
)

verify_inference_freeze(FREEZE_MANIFEST_PATH)
verify_c_predictions_freeze()
verify_aggregate_freeze()
verify_evaluator_freeze()
print("Condition C R10 freeze guards: PASS")
PY
```

The inference-side guard covers only prompt-facing and execution dependencies.
Ground truth, pseudolabel mapping, and frozen B predictions remain
evaluator-side; this separation is part of the frozen firewall.

### 9.3 Frozen result and interpretation boundary

Condition C contains 45 repetition records (15 physical cases × `R=3`) and 15
aggregate predictions. It reports 15/15 overall, 12/12 fault, 3/3 Normal, and
zero abstentions. Relative to B's 31/36 unseen fault agent-case outcomes, the
descriptive C−B contrast is 5/36 = 0.138889 with stratified cluster-bootstrap
95% interval [0.083333, 0.166667].

This comparison is non-causal and does not use equal observational units: C
has one aggregate result for each of 12 physical fault cases, while B has 36
correlated unseen agent-case outcomes. C and B also differ in both amount and
form of information. The full 5/36 difference is concentrated in
`CLS-OJNSG`; the other nine fault cases have zero difference. The result does
not establish a general superiority of centralization or federation. See the
[`independent R10 review`](docs/audits/CONDITION_C_R10_INDEPENDENT_REVIEW.md)
for the full limitation analysis.

## 10. Frozen milestones

| Milestone | Annotated tag | Peeled target commit |
|---|---|---|
| Phase A reproducibility completion | `phase-a-reproducibility-complete` | `145b6b79c59c352e06028166185bad3c9fb49607` |
| Independent Phase B held-out | `phase-b-heldout-frozen` | `86baaa65e72cea22ecb89dd0e7b213aea5a1284b` |
| Phase B protocol | `phase-b-protocol-frozen` | `3d86f64d43e14e7e0de520cb047ca1043bf9c1c0` |
| Execution schedule | `phase-b-execution-schedule-frozen` | `eef0bc58e5ab14fb0cd2aece180fb5b1b5a7962b` |
| Held-out predictions | `phase-b-inference-frozen` | `11c34358e28e875cd5c7249061ac2b89ffcd42f4` |
| Offline results | `phase-b-results-frozen` | `45ec4eed65b263a5803ced7d01064c4672e81e86` |
| Condition C R10 code and protocol | `condition-c-freeze-r10` | `60ccc7539714e909aae7318cc72031d7acdd4e78` |
| Condition C R10 predictions | `condition-c-predictions-frozen-r10` | `8d6b7a0636e9a15f0ebbd32ed0f9e2ce4faea30a` |
| Condition C R10 results | `condition-c-results-frozen-r10` | `89e4caebe635973ef438d4b601bb4f761417193a` |

The Phase A verbalizer also has dedicated pre-validation and completion tags;
the table above lists the shortest cross-phase audit chain.

## 11. Expected audit conclusion

> The repository preserves the frozen experimental record needed to
> independently recompute the reported Phase B metrics from the original frozen
> predictions. Raw Phase B held-out workbooks are identified by cryptographic
> hashes and must be supplied separately for verification starting from the
> numerical simulator outputs. Condition C R10 is independently auditable as a
> post-hoc exploratory reference through its separate frozen tag chain.

An audit should separately report whether it verified:

1. the committed prediction-to-metric chain;
2. the integrity of separately supplied raw held-out workbooks; and
3. physical re-simulation, which is not bit-for-bit reproducible without the
   original unrecorded RNG state.
