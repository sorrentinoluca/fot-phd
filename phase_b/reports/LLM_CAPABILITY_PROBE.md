# Phase B LLM capability probe

Status: **COMPLETE — capability and technical plumbing only**

- Provider: OpenAI
- Requested model: `gpt-5.6-terra`
- Returned model: `gpt-5.6-terra`
- API family: Responses API (`/v1/responses`)
- Installed SDK: `openai 3.6.0`
- Reasoning effort requested/effective: `medium` / `medium`
- Temperature supported/value: `false` / `null`
- Seed supported/value: `false` / `null`
- Structured Outputs supported: `true`
- Strict Structured Outputs: `true`
- Provider token accounting: supported, source `response.usage`

## Structured Output schema path

The provider request uses the separate OpenAI-compatible schema
`phase_b/conditions/diagnostic_output.openai.schema.json`. It is an explicit
derivation of the local Phase B schema and removes only the provider-unsupported
keywords `allOf`, `if`, `then`, `else`, and `uniqueItems`.

The local schema `phase_b/conditions/diagnostic_output.schema.json` is unchanged.
The local parser/validator is unchanged and remains authoritative for the
cross-field and uniqueness constraints:

- `abstain=false` requires `predicted_label` to be one valid supplied pseudolabel;
- `abstain=true` requires `predicted_label=null`;
- `used_insight_ids` must contain no duplicates.

A real minimal call with `gpt-5.6-terra`, reasoning effort `medium`, and
`strict=true` accepted the provider schema, generated an output, and that output
passed the local validator, including valid-label, abstention-coherence, and
unique-insight-ID checks.

## Technical A/B/E dry-run

Exactly one synthetic-fixture call was made per condition. No repetition set was
executed and no structural retry was observed.

| Condition | Prompt chars | Peer-block chars | Input tokens | Output tokens | Total tokens | Retries | Structured Output | Local validation |
|---|---:|---:|---:|---:|---:|---:|---|---|
| A | 4139 | 0 | 1365 | 189 | 1554 | 0 | PASS | PASS |
| B | 5909 | 1770 | 1850 | 162 | 2012 | 0 | PASS | PASS |
| E | 5909 | 1770 | 1850 | 134 | 1984 | 0 | PASS | PASS |

Condition A returned `used_insight_ids=[]`. For B and E, every returned insight
ID belonged to the corresponding prompt-visible set; the local validator also
accepted an empty list and rejected a synthetic unknown ID. No returned
prediction or diagnostic interpretation is recorded.

Provider-reported B/E input tokens were 1850/1850, with B−E difference 0.
**B/E provider-token equivalent for the validated dry-run.** Token accounting
comes directly from `response.usage`.

## Immutability and scope checks

The capability probe and dry-run did not modify any diagnostic prompt based on
a prediction. The local examples, pseudolabel values, and A/B/E condition
templates remained unchanged. In particular, neither B nor E was changed to
improve a generated output. The provider-compatible schema change was strictly
an API-compatibility transformation and did not alter the local schema or local
validator.

Official model documentation lists `medium` reasoning, Structured Outputs, a
1,050,000-token context window and 128,000 maximum output tokens:
https://developers.openai.com/api/docs/models/gpt-5.6-terra

No held-out data or definitive insight was accessed or generated. No accuracy,
correctness, confusion matrix, FoT delta, condition ranking, or diagnostic
performance metric was calculated.
