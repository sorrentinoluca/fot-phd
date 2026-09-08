# EXP2 Qwen capability probe

Status: **FAIL**

- Scope: capability and plumbing only
- Model alias: `fot-exp2-consumer`
- Model root: `Qwen/Qwen3.8-27B-FP8`
- vLLM: `0.28.0`
- Context: `4096` tokens
- Temperature / seed / max tokens: `0` / `20260829` / `512`
- Unique frozen prompt hashes checked: `180`
- Maximum raw prompt tokens: `2340`
- Live fixture A/B/E attempts: `1` / `2` / `3`
- Deterministic B replay: `True`

## Gates

- vllm_version_matches: **PASS**
- model_alias_matches: **PASS**
- model_root_matches: **PASS**
- model_revision_matches_process: **PASS**
- required_paths_advertised: **PASS**
- frozen_prompt_hashes_match: **PASS**
- raw_prompt_budget_fits: **PASS**
- live_fixture_budget_fits: **PASS**
- all_outputs_schema_valid: **FAIL**
- no_length_truncation: **FAIL**
- returned_model_matches: **PASS**
- token_accounting_complete: **PASS**
- deterministic_replay: **PASS**

No held-out prediction, ground-truth join, accuracy, condition ranking, or full
540-call experiment was performed.
