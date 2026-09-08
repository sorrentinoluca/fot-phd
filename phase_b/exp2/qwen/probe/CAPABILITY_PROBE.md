# EXP2 Qwen capability probe

Status: **PASS**

- Scope: capability and plumbing only
- Model alias: `fot-exp2-consumer`
- Model root: `Qwen/Qwen3.8-27B-FP8`
- vLLM: `0.28.0`
- Context: `4096` tokens
- Temperature / seed / max tokens: `0.0` / `20260829` / `1536`
- Unique frozen prompt hashes checked: `180`
- Maximum raw prompt tokens: `2340`
- Maximum input plus output budget: `3876`
- Minimum context margin: `220` tokens
- Live fixture A/B/E attempts: `1` / `1` / `1`
- Deterministic B replay: `True`
- Exact provider requests / structural retries: `4` / `0`
- A requests/retries: `1` / `0`
- B requests/retries: `1` / `0`
- E requests/retries: `1` / `0`
- Deterministic B replay requests/retries: `1` / `0`

## A/B/E synthetic fixture checks

- A: finish_reason_stop=PASS, content_non_null=PASS, schema_valid=PASS, reasoning_preserved=PASS, no_length_truncation=PASS
- B: finish_reason_stop=PASS, content_non_null=PASS, schema_valid=PASS, reasoning_preserved=PASS, no_length_truncation=PASS
- E: finish_reason_stop=PASS, content_non_null=PASS, schema_valid=PASS, reasoning_preserved=PASS, no_length_truncation=PASS

## Local reasoning controls

- `reasoning_effort` advertised by local OpenAPI: `True`
- `thinking_token_budget` advertised by local OpenAPI: `True`
- Configured uniform `thinking_token_budget`: `1024`

## Gates

- vllm_version_matches: **PASS**
- model_alias_matches: **PASS**
- model_root_matches: **PASS**
- model_revision_matches_process: **PASS**
- max_model_len_matches: **PASS**
- required_paths_advertised: **PASS**
- reasoning_controls_inspected: **PASS**
- frozen_prompt_hashes_match: **PASS**
- raw_prompt_budget_fits: **PASS**
- live_fixture_budget_fits: **PASS**
- all_outputs_schema_valid: **PASS**
- all_finish_reasons_stop: **PASS**
- all_outputs_content_non_null: **PASS**
- parser_input_is_content: **PASS**
- all_reasoning_preserved: **PASS**
- no_length_truncation: **PASS**
- returned_model_matches: **PASS**
- token_accounting_complete: **PASS**
- deterministic_replay: **PASS**

No held-out prediction, ground-truth join, accuracy, condition ranking, or full
540-call experiment was performed.
