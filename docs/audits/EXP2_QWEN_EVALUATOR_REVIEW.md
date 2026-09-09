# Independent Review — EXP2 Qwen Evaluator

**Scope**: Read-only pre-ground-truth review of the EXP2 Qwen evaluator amendment.

**Reviewer**: Claude (independent session, no access to ground truth or pseudolabel mapping)

**Date**: 2026-09-08

---

## 1. Tag-to-commit dereferencing

| Tag | Expected commit | Actual commit | Type | Result |
|---|---|---|---|---|
| `phase-b-exp2-qwen-evaluator-frozen-001` | `a8f9884dfe2150a89131ba604b34ff1f6914f6e9` | `a8f9884dfe2150a89131ba604b34ff1f6914f6e9` | annotated | **PASS** |
| `phase-b-exp2-qwen-predictions-frozen-001` | `a4f264c210873536c989ebd99aa2c6cf9857c85c` | `a4f264c210873536c989ebd99aa2c6cf9857c85c` | annotated | **PASS** |

## 2. Diff scope

Diff `a4f264c..a8f9884` touches exactly three files (505 insertions, 12 deletions):

| File | Status |
|---|---|
| `phase_b/exp2/qwen/evaluate_qwen.py` | modified |
| `phase_b/exp2/qwen/tests/test_evaluator_provenance.py` | new |
| `phase_b/exp2/qwen/EVALUATOR_AMENDMENT_001.md` | new |

No other files are modified. **PASS**.

## 3. EXP1 evaluator core invariance

| File | Expected SHA-256 | Actual SHA-256 | Cross-commit | Result |
|---|---|---|---|---|
| `phase_b/final_evaluation/evaluate_frozen_predictions.py` | `fbbc159a...d567e` | `fbbc159a0e61e92723f46d4a97e59244a129741bffbf84acd433416bc74d567e` | identical at both `a4f264c` and `a8f9884` | **PASS** |

## 4. Frozen inference artefacts invariance

| Artefact | Expected SHA-256 | Actual SHA-256 | Cross-commit | Result |
|---|---|---|---|---|
| `repetition_records.jsonl` | `20fdc8e3...7372198` | `20fdc8e3fac4ac37f2d993bdcacd526bd5927d5c599cb1fcbeef6a08e7372198` | identical | **PASS** |
| `aggregate_records.jsonl` | `73ace466...9f9e0a` | `73ace46655ef1e3bce2b6491e489fd303780341eeadf7be2e972ce121c9f9e0a` | identical | **PASS** |
| `execution_metadata.json` | `7ec47192...082468e` | `7ec4719d6a7294440568273b6a2afd4abadf96f9283950857079db6fd082468e` | identical | **PASS** |
| `inference_output_hash_manifest.json` | `da0eb008...a4fd88b` | `da0eb0085ed42342b9d8fbabfbb9f50e3231e5311015fbbdfe6961c1aa4fd88b` | identical | **PASS** |

## 5. `verify_qwen_inference()` fail-closed analysis

Each check below is verified to raise `RuntimeError` on failure, blocking evaluation.

| # | Check | Line(s) | Guard pattern | Verdict |
|---|---|---|---|---|
| 1 | Tag dereferences to canonical commit | 69–72 | `git rev-parse` + `!=` comparison | **FAIL-CLOSED** |
| 2 | Freeze commit is ancestor of HEAD | 73–83 | `git merge-base --is-ancestor`, returncode ≠ 0 | **FAIL-CLOSED** |
| 3 | Manifest file hash | 90 | `sha256_file() != INFERENCE_MANIFEST_SHA256` | **FAIL-CLOSED** |
| 4 | Manifest `artifact_version` | 92 | `.get() != "1"` | **FAIL-CLOSED** |
| 5 | Manifest `status` | 94 | `.get() != INFERENCE_MANIFEST_STATUS` | **FAIL-CLOSED** |
| 6 | Manifest `ground_truth_included` | 96 | `.get() is not False` — rejects `None`, `True`, missing | **FAIL-CLOSED** |
| 7 | Repetition record count = 540 | 98 | `.get() != 540` | **FAIL-CLOSED** |
| 8 | Aggregate record count = 180 | 100 | `.get() != 180` | **FAIL-CLOSED** |
| 9 | Canonical artifact set + hashes | 102 | full dict `!=` CANONICAL_INFERENCE_ARTIFACTS | **FAIL-CLOSED** |
| 10 | Each artifact file hash on disk | 103–105 | `sha256_file() != expected` per file | **FAIL-CLOSED** |
| 11 | Schedule reference (path + hash) | 106–112 | dict `!=` expected_schedule | **FAIL-CLOSED** |
| 12 | Schedule file hash on disk | 113–114 | `sha256_file() != SCHEDULE_SHA256` | **FAIL-CLOSED** |
| 13 | Metadata `status` | 117 | `.get() != METADATA_STATUS` | **FAIL-CLOSED** |
| 14 | Metadata repetition count = 540 | 119 | `.get() != 540` | **FAIL-CLOSED** |
| 15 | Metadata aggregate count = 180 | 121 | `.get() != 180` | **FAIL-CLOSED** |
| 16 | Metadata schedule hash | 123 | `.get() != SCHEDULE_SHA256` | **FAIL-CLOSED** |
| 17 | Metadata `ground_truth_joined` | 125 | `.get() is not False` | **FAIL-CLOSED** |
| 18 | Metadata `metrics_calculated` | 127 | `.get() is not False` | **FAIL-CLOSED** |
| 19 | Evaluator core path resolution | 130 | `!= FROZEN_EVALUATOR_PATH.resolve()` | **FAIL-CLOSED** |
| 20 | Evaluator core file hash | 132 | `sha256_file() != FROZEN_EVALUATOR_SHA256` | **FAIL-CLOSED** |

The `git_output()` helper wraps `subprocess.CalledProcessError` and `OSError` into `RuntimeError`, so a missing git binary or missing tag also fail-closed.

**Overall: PASS** — all 20 checks are fail-closed with no silent-pass paths.

## 6. Future artefact provenance registration

The `verify_qwen_inference()` return dict is propagated to both `results["reproducibility"]` (via `.update(provenance)`) and the output `evaluation_hash_manifest.json` (via `**provenance`).

| Provenance field | Present in results | Present in manifest | Value |
|---|---|---|---|
| `qwen_predictions_freeze_tag` | ✅ | ✅ | `phase-b-exp2-qwen-predictions-frozen-001` |
| `qwen_predictions_freeze_commit` | ✅ | ✅ | `a4f264c210873536c989ebd99aa2c6cf9857c85c` |
| `qwen_inference_manifest_sha256` | ✅ | ✅ | `da0eb008...` |
| `aggregate_predictions_sha256` | ✅ | ✅ | computed from `sha256_file(AGGREGATE_PATH)` |
| `schedule_sha256` | ✅ | ✅ | `d30cdf6a...` |
| `frozen_evaluator_code_path` | ✅ | ✅ | `phase_b/final_evaluation/evaluate_frozen_predictions.py` |
| `frozen_evaluator_code_sha256` | ✅ | ✅ | `fbbc159a...` |
| `evaluator_binding` | ✅ | ✅ | `phase_b.final_evaluation.evaluate_frozen_predictions` |

**PASS**.

## 7. Future `EVALUATION_REPORT.md` template

The `render_qwen_report()` function (lines 147–170):

- Replaces the title `"# Phase B final offline evaluation"` → `"# Phase B EXP2 Qwen final offline evaluation"`. **Identifies EXP2 Qwen: ✅**
- Replaces the freeze line with `"EXP2 Qwen predictions freeze: phase-b-exp2-qwen-predictions-frozen-001 at a4f264c..."`. **Cites correct Qwen freeze: ✅**
- Pre-replacement guard: asserts each original string appears exactly once (line 157).
- Post-replacement guard (lines 165–170): asserts `frozen_evaluator.INFERENCE_TAG` (`phase-b-inference-frozen`) and `frozen_evaluator.INFERENCE_COMMIT` (`11c34358...`) are absent from the final report. **Rejects Terra attribution: ✅**

**PASS**.

## 8. Test and amendment coherence

### Amendment (`EVALUATOR_AMENDMENT_001.md`)

The amendment accurately describes: scope limited to provenance and guardrails; canonical Qwen freeze tag and commit; no ground truth or pseudolabel mapping consulted; no metrics calculated; no LLM/vLLM calls; frozen artifacts byte-for-byte unchanged. All claims verified by this review.

### Tests (`test_evaluator_provenance.py`)

- `test_pre_evaluation_verification_has_no_evaluator_side_data_access`: wraps the real `load_json` to assert only `INFERENCE_MANIFEST_PATH` and `METADATA_PATH` are accessed; source-level asserts that `MAPPING_PATH`, `HELDOUT_MANIFEST_PATH`, and `load_case_truth` are absent from `evaluate_qwen.py`. **No evaluator-side data access is masked.**
- `test_future_results_manifest_and_report_use_only_qwen_provenance`: injects a synthetic Terra report and verifies the evaluate pipeline transforms it to Qwen provenance, with explicit `assertNotIn(TERRA_FREEZE_TAG, report)` and `assertNotIn(TERRA_FREEZE_COMMIT, report)`.
- Mutation tests (`test_manifest_status_counts_paths_and_hashes_are_fail_closed`, `test_metadata_*`): each corrupt field triggers `RuntimeError`.
- No mock suppresses or bypasses a real guardrail.

**PASS**.

## 9. Test execution

**Environment note**: The specified Python path (`/home/luca/fot-exp2/env-vllm/bin/python`) is a Linux server path not available on the macOS device. System `python3` (3.10.12) was used instead. All tests use only the standard library (`unittest`, `unittest.mock`, `json`, `pathlib`, `subprocess`, `tempfile`), so no vllm dependencies were required. Results are valid.

A temporary read-only worktree was created at tag `phase-b-exp2-qwen-evaluator-frozen-001` and removed after testing.

### Provenance tests (9/9 PASS)

```
test_current_qwen_predictions_freeze_verifies .................. ok
test_future_results_manifest_and_report_use_only_qwen_provenance ok
test_git_output_converts_missing_tag_to_runtime_error .......... ok
test_manifest_status_counts_paths_and_hashes_are_fail_closed ... ok
test_metadata_ground_truth_or_metrics_declarations_are_rejected  ok
test_metadata_status_counts_and_schedule_are_rejected_when_incoherent ok
test_missing_or_wrong_freeze_tag_is_rejected ................... ok
test_non_ancestor_freeze_commit_is_rejected .................... ok
test_pre_evaluation_verification_has_no_evaluator_side_data_access ok
```

### Contract tests (8/8 PASS)

```
test_all_rendered_prompts_match_original_frozen_hashes ......... ok
test_entire_original_protocol_hash_manifest_is_unchanged ....... ok
test_frozen_hashes_are_unchanged ............................... ok
test_lane_does_not_shadow_frozen_artifacts ..................... ok
test_qwen_evaluator_binds_existing_evaluator ................... ok
test_qwen_execution_contract ................................... ok
test_runner_requires_explicit_full_run_acknowledgement ......... ok
test_schedule_cardinality_and_r3 ............................... ok
```

### Pre-run test classification

No test in the suite explicitly checks for the absence of the `evaluation/` output directory. The pre-run test requiring absence of outputs is classified as **NOT APPLICABLE** (not found in the suite, not modified).

## 10. Final state verification

| Check | Result |
|---|---|
| `phase_b/exp2/qwen/evaluation/` directory absent | **PASS** — `No such file or directory` |
| Working tree clean | **PASS** — `git status --porcelain` is empty |
| No Qwen metrics produced | **PASS** — no evaluation artifacts in `phase_b/exp2/qwen/` |
| All frozen outputs invariant | **PASS** — cross-commit SHA-256 match for all 5 files (4 artefacts + evaluator core) |

---

## Findings

### P3 — Non-blocking improvements

**P3-1: Manifest JSON parsed before hash verification**

- **File**: `phase_b/exp2/qwen/evaluate_qwen.py`, line 89–90
- **Description**: `load_json(INFERENCE_MANIFEST_PATH)` is called on line 89, and the SHA-256 hash of the same file is verified on line 90. The parsed content is not used for any security-sensitive decision before the hash check, so the function remains fail-closed. However, the idiomatic defensive pattern verifies the hash first.
- **Consequence**: None in practice — `RuntimeError` fires before the function returns if the hash mismatches. A corrupted file that fails JSON parsing would raise before the hash check, producing a less informative error.
- **Recommended fix**: Swap lines 89 and 90 so `sha256_file()` runs before `load_json()`.

**P3-2: Redundant aggregate hash key in output manifest**

- **File**: `phase_b/exp2/qwen/evaluate_qwen.py`, lines 140 and 205
- **Description**: The output `evaluation_hash_manifest.json` contains both `aggregate_predictions_sha256` (from `**provenance`, line 140 origin) and `input_aggregate_predictions_sha256` (explicit, line 205), both holding the SHA-256 of `AGGREGATE_PATH`. This is redundant.
- **Consequence**: Cosmetic — the manifest carries two keys with the same value. No functional impact.
- **Recommended fix**: Either remove `input_aggregate_predictions_sha256` from the manifest (it duplicates `aggregate_predictions_sha256` from provenance), or document the semantic distinction if intentional.

### P1 — Blockers

None.

### P2 — Important before evaluation

None.

---

## Session notes

- A stale `.git/worktrees/exp2-review` reference persists as "locked" in the repository due to VM mount permissions. The worktree directory itself (`/tmp/exp2-review`) has been deleted. Run `git worktree prune` from the native macOS environment to clean the reference.
- Five other stale worktree entries (worktree, worktree1–4) predate this session.

---

## Verdict

All 11 verification steps pass. The evaluator amendment is exclusively a provenance and guardrail correction. No ground truth was accessed, no metrics were calculated, no frozen artefact was modified, and no evaluation output was produced. The `verify_qwen_inference()` function is fail-closed across all 20 checks. The future report correctly identifies EXP2 Qwen and cites the Qwen freeze, with a fail-closed guard against Terra provenance leakage. Two non-blocking improvements were identified (P3 only).

## **GO FOR OFFLINE EVALUATION**
