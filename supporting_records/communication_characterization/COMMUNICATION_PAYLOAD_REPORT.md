# Communication Payload Characterization — Frozen Experiment 1

Status: **descriptive only**. This report does not establish communication efficiency.

## Actual FoT textual payload

Primary measure: the exact Condition-B peer block inserted into a receiver prompt, serialized as `PEER INSIGHTS\n` followed by indented UTF-8 JSON and two terminal newlines.

| Receiver | Insights | Characters | UTF-8 bytes | Peer raw values | Dense float64 reference bytes | Text/raw | Raw/text |
|---|---:|---:|---:|---:|---:|---:|---:|
| agent_1 | 6 | 2289 | 2304 | 1476000 | 11808000 | 0.000195121951 | 5125.00 |
| agent_2 | 6 | 2327 | 2336 | 1476000 | 11808000 | 0.000197831978 | 5054.79 |
| agent_3 | 6 | 2410 | 2420 | 1476000 | 11808000 | 0.000204945799 | 4879.34 |
| agent_4 | 6 | 2361 | 2378 | 1476000 | 11808000 | 0.000201388889 | 4965.52 |

An all-receiver Condition-B unit means one prompt invocation for each receiver: 24 insight transmissions, 9387 characters, and 9438 UTF-8 bytes. Each of the eight unique insights is delivered to exactly three receivers.

The frozen library stores 8 unique insights in 3125 UTF-8 bytes as the exact JSON artifact. Stored unique knowledge and transmitted payload are therefore distinct quantities.

Across the complete frozen Condition-B execution (15 cases × 4 receivers × R=3), the peer blocks are transmitted in 180 calls: 1080 insight transmissions and 424710 UTF-8 bytes. This is repetition across calls, not additional unique knowledge.

## Token count

`TOKEN COUNT NOT REPRODUCIBLY AVAILABLE FROM CURRENT ARTIFACTS`

The frozen execution records `openai==3.6.0` and whole-prompt accounting from `response.usage`, but no payload tokenizer/encoding. Whole-prompt usage cannot be converted into an exact isolated peer-block token count without an identified tokenizer.

## Local evidence reference

Each source agent contributes five fixed development fault batches. A workbook contains 3001 rows from 0 to 50 h, but the frozen verbalizer feature-extracts only the left-closed/right-open post-injection interval [10 h, 50 h): 2400 samples, eight 5 h windows, and 41 XMEAS per batch.

| Source agent | Batches | Consumed samples | XMEAS | Raw values | Dense float64 bytes | Structured feature values |
|---|---:|---:|---:|---:|---:|---:|
| agent_1 | 5 | 12000 | 41 | 492000 | 3936000 | 8200 |
| agent_2 | 5 | 12000 | 41 | 492000 | 3936000 | 8200 |
| agent_3 | 5 | 12000 | 41 | 492000 | 3936000 | 8200 |
| agent_4 | 5 | 12000 | 41 | 492000 | 3936000 | 8200 |

The structured count is `5 batches × 8 windows × 41 XMEAS × 5 descriptors = 8,200` per source agent. The five descriptors are `shift_sigma`, `slope_sigma_h`, `raw_std_ratio`, `diff_std_ratio`, and `residual_std_ratio`. Absolute-value duplicates, booleans, summaries, and text are not counted as independent numerical features.

The shared Normal N1-N5 reference contributes 15000 samples × 41 XMEAS = 615000 raw values (4920000 dense-float64 reference bytes). It supplies normalization statistics and frozen calibration context; it is not peer fault-specific experience and is counted once in the inclusive alternative.

Across all four source agents, unique fault-specific evidence is 1968000 raw values (15744000 reference bytes) and 32800 structured numerical feature values. Including shared Normal N1-N5 once gives 2583000 raw values (20664000 reference bytes).

## Ratios under the stated serialization convention

Receiver-level primary formula:

`rendered peer-block UTF-8 bytes / (three peers × five batches × 2400 samples × 41 XMEAS × 8 bytes)`

This is the **textual-to-raw payload ratio under the stated serialization convention**. Its inverse is the **reference raw-to-text payload ratio**. It is not a lossless compression ratio.

The shared-Normal-inclusive alternative adds `15000 × 41 × 8` bytes once to the receiver denominator; both variants are recorded in the machine-readable report.

The unique-library formula is:

`frozen final_local_insights.json UTF-8 bytes / (four agents × five batches × 2400 samples × 41 XMEAS × 8 bytes)`

Using fault-specific evidence only, this equals 0.000198488313; the inverse is 5038.08. Including shared Normal N1-N5 once, it equals 0.000151229191; the inverse is 6612.48.

## Provenance and assumptions

- Insight routing and serialization: `phase_b/conditions/builders.py`, `phase_b/insights/library.py`, and the four frozen `agent_*_B.json` peer libraries.
- Insight sources: `phase_b/execution/generate_final_insights.py`, four `phase_b/insights/input_bundles/agent_*.json`, and `phase_b/insights/generation_runs.json`.
- Batch scope and topology: `phase_b/config/phase_b_protocol_frozen.json` and `phase_b/PHASE_B_PROTOCOL_FREEZE.md`.
- Windowing and variables: `code/tep_verbalize_v2.py`, `code/tep_features.py`, and `code/verbalizer_config_v2.json`.
- Dataset source snapshot: `309b944f35ac440ff0c70616947ffe723c766e14`.
- All 20 development fault workbooks and the Normal workbook were matched byte-for-byte to the SHA-256 and size recorded in their Git-LFS pointers at the pinned dataset commit.
- Theoretical dense float64 payload is `raw XMEAS value count × 8 bytes`; XLSX file sizes are not used in any ratio.
- Pre-injection samples, Time, XMV, and cost columns are not counted because the frozen feature pipeline does not consume them as XMEAS feature evidence for these insight texts.
- The insight-generation LLM received neutral text only (`contains_structured_numerical_json=false`), not the upstream numerical JSON.

## Interpretation

FoT communication in this experiment is limited to compact textual insight payloads rather than raw time-series observations.

This is a payload characterization, not a demonstration of communication efficiency, compression efficiency, bandwidth optimality, or superior communication cost.

## Validation

- Frozen artifact hashes verified: PASS (19 artifacts).
- Pinned dataset Git-LFS workbook matches: PASS (21/21).
- Exactly 8 unique insights: PASS.
- Exactly 6 peer insights per receiver: PASS.
- No self or Normal insight routed: PASS.
- Every unique insight delivered to exactly 3 receivers: PASS.
