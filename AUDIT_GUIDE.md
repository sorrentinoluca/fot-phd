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
- the EXP2 Qwen protocol, predictions, evaluator, results, and independent
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

## 10. EXP2 Qwen — frozen consumer-portability result

EXP2 changes only the consumer to `Qwen/Qwen3.8-27B-FP8`; the insight producer
remains `gpt-5.6-terra`. The experiment reuses the same held-out cases, so this
is a bounded, descriptive cross-model comparison rather than an end-to-end
open-weight replica.

### 10.1 Frozen chain and canonical artifacts

```text
phase-b-exp2-qwen-protocol-frozen-001
d9bb95c31bdeb2f1608aaedc52f25b98de9bbf96
        ↓
phase-b-exp2-qwen-predictions-frozen-001
a4f264c210873536c989ebd99aa2c6cf9857c85c
        ↓
phase-b-exp2-qwen-evaluator-frozen-001
a8f9884dfe2150a89131ba604b34ff1f6914f6e9
        ↓
phase-b-exp2-qwen-results-frozen-001
37195cf2c5076b5da724b857f10e157177654cac
```

Canonical evaluation artifacts:

- [`EVALUATION_REPORT.md`](phase_b/exp2/qwen/evaluation/EVALUATION_REPORT.md);
- [`evaluation_results.json`](phase_b/exp2/qwen/evaluation/evaluation_results.json);
- [`bootstrap_results.json`](phase_b/exp2/qwen/evaluation/bootstrap_results.json);
- [`confusion_matrices.json`](phase_b/exp2/qwen/evaluation/confusion_matrices.json);
- [`per_agent_metrics.csv`](phase_b/exp2/qwen/evaluation/per_agent_metrics.csv);
- [`primary_metrics.csv`](phase_b/exp2/qwen/evaluation/primary_metrics.csv);
- [`secondary_metrics.csv`](phase_b/exp2/qwen/evaluation/secondary_metrics.csv);
- [`transfer_counts.csv`](phase_b/exp2/qwen/evaluation/transfer_counts.csv);
- [`evaluation_hash_manifest.json`](phase_b/exp2/qwen/evaluation/evaluation_hash_manifest.json).

The canonical reviews are the
[`evaluator review`](docs/audits/EXP2_QWEN_EVALUATOR_REVIEW.md) and the
[`independent results review R2`](docs/audits/EXP2_QWEN_RESULTS_INDEPENDENT_REVIEW_R2.md).
The results review verdict is **GO WITH LIMITATIONS**.

### 10.2 Verify frozen bytes

The following read-only check covers the four inference outputs and nine
evaluation outputs:

```bash
python - <<'PY'
import hashlib
from pathlib import Path

expected = {
    "phase_b/exp2/qwen/inference/repetition_records.jsonl": "20fdc8e3fac4ac37f2d993bdcacd526bd5927d5c599cb1fcbeef6a08e7372198",
    "phase_b/exp2/qwen/inference/aggregate_records.jsonl": "73ace46655ef1e3bce2b6491e489fd303780341eeadf7be2e972ce121c9f9e0a",
    "phase_b/exp2/qwen/inference/execution_metadata.json": "7ec4719d6a7294440568273b6a2afd4abadf96f9283950857079db6fd082468e",
    "phase_b/exp2/qwen/inference/inference_output_hash_manifest.json": "da0eb0085ed42342b9d8fbabfbb9f50e3231e5311015fbbdfe6961c1aa4fd88b",
    "phase_b/exp2/qwen/evaluation/EVALUATION_REPORT.md": "0c6f2b3d795961a660ff659ce5cb31620209d126d92bed11aea265587a436ba9",
    "phase_b/exp2/qwen/evaluation/bootstrap_results.json": "d421a30aea4a29aee9b30ec99d31dc97ea637322a7c16cc29ba4981ac0d3a9c2",
    "phase_b/exp2/qwen/evaluation/confusion_matrices.json": "c3b0beaf56ca2f455e0ed80e56dcaba5bad67e95ac74cfb2322679f0ef936061",
    "phase_b/exp2/qwen/evaluation/evaluation_hash_manifest.json": "d9f18d8804b8528c58029736b276356f0a34c59af69f27034eeab2f971472732",
    "phase_b/exp2/qwen/evaluation/evaluation_results.json": "5d499d63ff771343c402fc3ecc03b93862ae2cfb9719b231b985077c1e2257d3",
    "phase_b/exp2/qwen/evaluation/per_agent_metrics.csv": "842afff50b87d571ab6698e81b2791fbd30e4e4e775ef1c8dfb43f6ee9b993a8",
    "phase_b/exp2/qwen/evaluation/primary_metrics.csv": "89d1e52ec146d98d6bf45ab9b692a272e091cf08200fbd0966ed379d841b1d8e",
    "phase_b/exp2/qwen/evaluation/secondary_metrics.csv": "32d395f379c3c5d86a295705037aab53049e45c4887277cf35105f74d6462ca1",
    "phase_b/exp2/qwen/evaluation/transfer_counts.csv": "8c95d3141acdd99317f36c2c3d650cecf2ac9c8992f893325d4ce73b571eb4a2",
}
for relative, digest in expected.items():
    actual = hashlib.sha256(Path(relative).read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit(f"FAIL {relative}: {actual} != {digest}")
    print(f"PASS {relative}")
PY
```

### 10.3 Frozen result and interpretation boundary

For locally-unseen fault observations, A is 0/36 (0%), B is 34/36 (94.44%),
and E is 1/36 (2.78%). B−A is 0.944444 with bootstrap 95% CI
[0.916667, 1.0]; B−E is 0.916667 with CI [0.833333, 1.0]. There are 34
helped, 0 harmed, 2 unchanged-incorrect observations, zero abstentions, and
C1–C4 are 4/4 PASS. H2 is a separate secondary control and fails. Other
secondary results are local-seen A 100%, B 75%, E 100%; Normal 100% for all
three configurations; and overall A 40%, B 91.67%, E 41.67%.

Interpretation must retain the independent review's limitations: only one
open-weight consumer was tested; the producer remained proprietary; the same
held-out cases were reused; and the cross-model comparison is descriptive.
Deterministic decoding made the three repetitions byte-identical for every one
of the 180 aggregates, so majority vote does not measure variability. A is a
constant local-label classifier on faults and thus a structural unseen floor,
while errors show systematic `CLS-OJNSG` ↔ `CLS-Z3ISU` confusion.

The effective reasoning cap is 1023 tokens although the nominal budget is
1024. Every one of B's five aggregate errors has all three repetitions at the
cap, while all 36 uncapped B aggregates are correct. H2 is therefore confounded
with budget exhaustion and does not causally establish negative insight
interference. B and E have comparable prompt length, reasoning use, and
insight-citation rates: the large B−E supports content specificity but is not
definitive causal proof. No sensitivity analysis has been run.

The permissible conclusion is that B's advantage persists for a second,
open-weight consumer in this frozen configuration and mitigates the concern of
dependence on one proprietary consumer. It does not prove universal
portability, cross-model generality, or end-to-end proprietary-model
independence.

## 11. Condition A+ — local-only self-insight control

A+ is the fourth condition of the main study. The receiving agent is given
**self-generated insights only**, with no peer insights. It isolates a
confound the A/B/E design alone cannot settle: whether B's advantage comes
from *having insights at all* or specifically from their **peer origin**.

> **Freeze status differs from sections 9 and 10.** A+, C06 and C02B are frozen
> by **hash manifest**, not by annotated git tag. There is no entry for them in
> section 14. An auditor can verify byte integrity against the committed
> manifests, but cannot anchor them to a tagged commit.

### 11.1 Canonical artifacts

Everything lives under [`phase_b/final_evaluation_aplus/`](phase_b/final_evaluation_aplus):

- [`APLUS_EVALUATION_REPORT.md`](phase_b/final_evaluation_aplus/APLUS_EVALUATION_REPORT.md) — canonical report;
- [`APLUS_FREEZE_MANIFEST.json`](phase_b/final_evaluation_aplus/APLUS_FREEZE_MANIFEST.json) — freeze record;
- [`aplus_evaluation_hash_manifest.json`](phase_b/final_evaluation_aplus/aplus_evaluation_hash_manifest.json) — path-to-SHA256 map under key `evaluation_artifacts`;
- `aplus_primary_metrics.csv`, `aplus_secondary_metrics.csv`, `aplus_per_agent_metrics.csv`, `aplus_transfer_counts.csv`, `aplus_paired_rows.csv`;
- `aplus_evaluation_results.json`, `aplus_bootstrap_results.json`, `aplus_confusion_matrix.json`;
- `inference/` — `repetition_records.jsonl`, `aggregate_records.jsonl`, `execution_metadata.json`, `infrastructure_failures.jsonl`, `inference_output_hash_manifest.json`.

### 11.2 Verify frozen bytes

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path

manifest = json.loads(Path(
    "phase_b/final_evaluation_aplus/aplus_evaluation_hash_manifest.json"
).read_text())
for relative, digest in manifest["evaluation_artifacts"].items():
    actual = hashlib.sha256(Path(relative).read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit(f"FAIL {relative}: {actual} != {digest}")
    print(f"PASS {relative}")
PY
```

### 11.3 Frozen result and interpretation boundary

For locally-unseen fault observations (abstentions count as incorrect):

| Condition | Correct / n | Accuracy | Abstentions |
|---|---:|---:|---:|
| A — isolated | 0 / 36 | 0.00% | 14 |
| A+ — self-insight only | 0 / 36 | 0.00% | 21 |
| B — FoT | 31 / 36 | 86.11% | 0 |
| E — corrupted | 3 / 36 | 8.33% | 0 |

Deltas: A+−A is 0; B−A+ is 0.861111; E−A+ is 0.083333.

Self-generated insights **do not raise the floor**: A+ produces zero correct
observations on locally-unseen classes and *more* abstentions than A, 21
against 14. The permissible conclusion is that B's advantage is not explained
by the mere presence of insights in the context; the peer origin is what
carries discriminative information.

Interpretation limits: A+ is a control within the frozen main study, not an
independent experiment; it reuses the same held-out cases; and a floor of 0/36
for both A and A+ means the contrast cannot rank them against each other.

## 12. C06 — local-first decision policy, post-hoc mitigation

EXP3_V2 showed five local-seen errors under B: peer insights can displace
correct local knowledge. C06 is the variant `B_LOCAL_FIRST_V1`, a
decision-policy block that instructs the receiver to weigh local evidence
first. It is a **post-hoc mitigation**, and the artifact itself says so: the
field `analysis_kind` in the results file reads *"post-hoc diagnostic; not an
independent replication"*.

### 12.1 Canonical artifacts

Under [`phase_b/c06/`](phase_b/c06):

- [`C06_SCREENING_PROTOCOL.md`](phase_b/c06/C06_SCREENING_PROTOCOL.md) and [`C06_INPUT_FREEZE_MANIFEST.json`](phase_b/c06/C06_INPUT_FREEZE_MANIFEST.json) — screening stage;
- [`full_test/C06_FULL_TEST_PROTOCOL.md`](phase_b/c06/full_test/C06_FULL_TEST_PROTOCOL.md) and [`full_test/C06_FULL_TEST_FREEZE_MANIFEST.json`](phase_b/c06/full_test/C06_FULL_TEST_FREEZE_MANIFEST.json) — frozen **before** inference;
- [`full_test/inference/FULL_TEST_REPORT.md`](phase_b/c06/full_test/inference/FULL_TEST_REPORT.md) — canonical report;
- [`full_test/inference/full_test_results.json`](phase_b/c06/full_test/inference/full_test_results.json) — metrics, gate, per-case regressions and improvements;
- `full_test/inference/output_hashes.json` — filename-to-SHA256 map for the six inference outputs.

### 12.2 Verify frozen bytes

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path

base = Path("phase_b/c06/full_test/inference")
for name, digest in json.loads((base / "output_hashes.json").read_text()).items():
    actual = hashlib.sha256((base / name).read_bytes()).hexdigest()
    if actual != digest:
        raise SystemExit(f"FAIL {name}: {actual} != {digest}")
    print(f"PASS {name}")
PY
```

### 12.3 Frozen result and interpretation boundary

| Stratum | C06 | Frozen B | Improved | Regressed |
|---|---:|---:|---:|---:|
| local-seen | 23 / 24 (95.83%) | 19 / 24 (79.17%) | 4 | 0 |
| local-unseen | 68 / 72 (94.44%) | 68 / 72 (94.44%) | 1 | 1 |
| Normal | 24 / 24 (100%) | 24 / 24 (100%) | 0 | 0 |
| overall | 115 / 120 (95.83%) | — | — | — |

The gate is PASS and the recorded status is *"Risolta — trasferimento negativo
mitigato dal decision-policy block"*. There is one abstention and no parse
failure.

Interpretation limits, all mandatory:

- the policy was evaluated on the **same EXP3_V2 sample that motivated it**, so
  this is not an independent replication and the effect size is optimistic;
- local-unseen accuracy is **unchanged**: one improvement and one regression,
  net zero. C06 does not add transfer, it protects local knowledge;
- one local-unseen regression survives — agent 2 on case `EXP3V2-F13-002` —
  so the mitigation is not a proof of absence of individual regressions;
- no replication on independent data has been run.

## 13. C02B — same-task numerical baselines

C02B answers the question a reviewer asks immediately: on this same held-out,
how does a numerical method perform? It has two independent parts.

### 13.1 Canonical artifacts

- Shared numeric prototypes — [`phase_b/baselines/c02b_shared_numeric_prototypes/`](phase_b/baselines/c02b_shared_numeric_prototypes): [`C02B_PROTOCOL_FREEZE.md`](phase_b/baselines/c02b_shared_numeric_prototypes/C02B_PROTOCOL_FREEZE.md), [`results/C02B_BASELINE_REPORT.md`](phase_b/baselines/c02b_shared_numeric_prototypes/results/C02B_BASELINE_REPORT.md), `results/metrics.json`, `results/bootstrap_results.json`, `results/predictions.csv`, `results/prototypes.json`, `results/payloads/agent_[1-4].bin`, `results/output_hash_manifest.json`;
- Supervisor-requested centralized suite — [`phase_b/baselines/c02b_supervisor_model_suite/`](phase_b/baselines/c02b_supervisor_model_suite): [`PROTOCOL_FREEZE.md`](phase_b/baselines/c02b_supervisor_model_suite/PROTOCOL_FREEZE.md), [`results/SUPERVISOR_MODEL_SUITE_REPORT.md`](phase_b/baselines/c02b_supervisor_model_suite/results/SUPERVISOR_MODEL_SUITE_REPORT.md), `results/metrics.json`, `results/models/`, `results/output_hash_manifest.json`.

Both manifests use the same shape: an `artifacts` object mapping
repository-relative path to SHA256.

### 13.2 Verify frozen bytes

```bash
python - <<'PY'
import hashlib, json
from pathlib import Path

manifests = [
    "phase_b/baselines/c02b_shared_numeric_prototypes/results/output_hash_manifest.json",
    "phase_b/baselines/c02b_supervisor_model_suite/results/output_hash_manifest.json",
]
for manifest in manifests:
    for relative, digest in json.loads(Path(manifest).read_text())["artifacts"].items():
        actual = hashlib.sha256(Path(relative).read_bytes()).hexdigest()
        if actual != digest:
            raise SystemExit(f"FAIL {relative}: {actual} != {digest}")
        print(f"PASS {relative}")
PY
```

### 13.3 Frozen result and interpretation boundary

**Shared numeric prototypes.** Locally-unseen accuracy is 36/36, 100%, with a
stratified physical-case cluster bootstrap CI of [1.0, 1.0] over 10 000 draws,
12 physical clusters, seed 20260910. Communication payload is 3 peer
prototypes, 2 091 scalar values, 16 755 bytes per receiver. Recorded status:
`MITIGATA`.

**Centralized model suite.** Six models reach 15/15 — AdaBoost, k-NN, linear
elastic-net, causal LSTM with attention, MLP, random forest — each 12/12 on
fault cases and 3/3 on Normal. Two reach 14/15: BiLSTM with attention and the
multimodal BiLSTM with attention and TF-IDF, both 11/12 on fault cases.

The comparison anchors are recorded inside the artifact itself: FoT B
locally-unseen 31/36 (86.11%) against shared prototypes 36/36 (100%).

Interpretation limits, all mandatory:

- **the numerical baseline is more accurate than FoT B on this benchmark**, by
  13.9 points. No text in the paper or documentation may describe FoT as
  competitive or superior in accuracy. The residual value of FoT is auditable
  text and transfer without consumer training, and these properties do not
  compensate quantitatively;
- the centralized suite sees **all classes during training**. Its models are
  descriptive references, not federated evidence, and the projected
  locally-unseen figure does not make them federated;
- the multimodal model fuses the sequence and the verbalization of the **same**
  sensors, not two independent physical sources.

## 14. Frozen milestones

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
| EXP2 Qwen protocol | `phase-b-exp2-qwen-protocol-frozen-001` | `d9bb95c31bdeb2f1608aaedc52f25b98de9bbf96` |
| EXP2 Qwen predictions | `phase-b-exp2-qwen-predictions-frozen-001` | `a4f264c210873536c989ebd99aa2c6cf9857c85c` |
| EXP2 Qwen evaluator | `phase-b-exp2-qwen-evaluator-frozen-001` | `a8f9884dfe2150a89131ba604b34ff1f6914f6e9` |
| EXP2 Qwen results | `phase-b-exp2-qwen-results-frozen-001` | `37195cf2c5076b5da724b857f10e157177654cac` |

The Phase A verbalizer also has dedicated pre-validation and completion tags;
the table above lists the shortest cross-phase audit chain.

**Not tagged.** Condition A+ (section 11), C06 (section 12) and the C02B
baselines (section 13) have no annotated tag. They are frozen by hash
manifest only.

## 15. Expected audit conclusion

> The repository preserves the frozen experimental record needed to
> independently recompute the reported Phase B metrics from the original frozen
> predictions. Raw Phase B held-out workbooks are identified by cryptographic
> hashes and must be supplied separately for verification starting from the
> numerical simulator outputs. Condition C R10 is independently auditable as a
> post-hoc exploratory reference through its separate frozen tag chain. EXP2
> Qwen is auditable through its four-tag chain, frozen inference and evaluation
> artifacts, and independent R2 review, within the stated consumer-portability
> limitations.
>
> Condition A+, the C06 local-first mitigation and the C02B numerical
> baselines are auditable at the level of byte integrity against their
> committed hash manifests, but they carry no tagged commit chain, and C06 is
> a post-hoc analysis on the sample that motivated it.

An audit should separately report whether it verified:

1. the committed prediction-to-metric chain;
2. the integrity of separately supplied raw held-out workbooks; and
3. physical re-simulation, which is not bit-for-bit reproducible without the
   original unrecorded RNG state.
