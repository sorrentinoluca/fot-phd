"""Freeze the complete C06 protocol and prompt-side artifact inventory."""

from __future__ import annotations

from datetime import datetime, timezone
import json

from .constants import (
    C06_ROOT,
    HARNESS_COMMIT,
    HARNESS_TAG,
    INFERENCE_GOVERNANCE_COMMIT,
    INFERENCE_PAYLOAD_COMMIT,
    INFERENCE_TAG,
    LOCAL_FIRST_BLOCK,
    MAX_OUTPUT_TOKENS,
    MAX_STRUCTURAL_RETRIES,
    MODEL,
    REASONING_EFFORT,
    REPETITIONS,
    ROOT,
    SDK_VERSION,
    VARIANT,
    VERBALIZATION_GOVERNANCE_COMMIT,
    VERBALIZATION_PAYLOAD_COMMIT,
    VERBALIZATION_TAG,
)
from .prompt_variant import canonical_json, sha256_bytes, sha256_file


ARTIFACTS = (
    "phase_b/c06/C06_SCREENING_PROTOCOL.md",
    "phase_b/c06/README.md",
    "phase_b/c06/__init__.py",
    "phase_b/c06/build_screening_assets.py",
    "phase_b/c06/constants.py",
    "phase_b/c06/evaluate_screening.py",
    "phase_b/c06/evaluator_side/screening_targets.json",
    "phase_b/c06/freeze_inputs.py",
    "phase_b/c06/prompt_hash_manifest.json",
    "phase_b/c06/prompt_variant.py",
    "phase_b/c06/prompts/B_FROZEN_RECONSTRUCTED.txt",
    "phase_b/c06/prompts/B_LOCAL_FIRST_V1.diff",
    "phase_b/c06/prompts/B_LOCAL_FIRST_V1.txt",
    "phase_b/c06/run_screening.py",
    "phase_b/c06/screening_schedule.json",
    "phase_b/c06/tests/__init__.py",
    "phase_b/c06/tests/test_c06_screening.py",
)


def main() -> None:
    inference_root = C06_ROOT / "inference"
    if inference_root.exists() and any(inference_root.rglob("*")):
        raise RuntimeError("cannot freeze inputs after an inference artifact exists")
    artifacts = []
    for relative in ARTIFACTS:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"missing or symlinked C06 artifact: {relative}")
        artifacts.append(
            {
                "path": relative,
                "size_bytes": path.stat().st_size,
                "sha256": sha256_file(path),
            }
        )
    manifest = {
        "schema_version": "1.0",
        "variant": VARIANT,
        "status": "FROZEN_BEFORE_INFERENCE",
        "frozen_at": datetime.now(timezone.utc).isoformat(),
        "analysis_kind": "post-hoc diagnostic; not an independent replication",
        "source_bindings": {
            "harness": {"tag": HARNESS_TAG, "commit": HARNESS_COMMIT},
            "inference": {
                "tag": INFERENCE_TAG,
                "governance_commit": INFERENCE_GOVERNANCE_COMMIT,
                "payload_commit": INFERENCE_PAYLOAD_COMMIT,
            },
            "verbalizations": {
                "tag": VERBALIZATION_TAG,
                "governance_commit": VERBALIZATION_GOVERNANCE_COMMIT,
                "payload_commit": VERBALIZATION_PAYLOAD_COMMIT,
            },
        },
        "intervention": {
            "exact_instruction": LOCAL_FIRST_BLOCK,
            "instruction_sha256": sha256_bytes(LOCAL_FIRST_BLOCK.encode("utf-8")),
            "only_change_from_frozen_B": "one insertion; see frozen unified diff",
        },
        "execution_contract": {
            "consumer_model": MODEL,
            "openai_sdk_version": SDK_VERSION,
            "runtime_python": "/Users/luker/fot-c06-env/bin/python",
            "reasoning_effort": REASONING_EFFORT,
            "agent_case_count": 24,
            "repetitions": REPETITIONS,
            "planned_calls": 24 * REPETITIONS,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "max_structural_retries": MAX_STRUCTURAL_RETRIES,
            "temperature_sent": False,
            "seed_sent": False,
            "store": False,
            "stateless": True,
            "aggregation": "two-of-three label majority",
        },
        "gate": {
            "original_errors_recovered_min": 4,
            "original_errors_n": 5,
            "new_errors_max": 0,
            "previously_correct_n": 19,
            "aggregate_correct_min": 23,
            "aggregate_n": 24,
            "parse_failures_max": 0,
            "forbidden_information_max": 0,
        },
        "experiment_artifacts": artifacts,
    }
    path = C06_ROOT / "C06_INPUT_FREEZE_MANIFEST.json"
    content = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") != content:
        path.unlink()
    path.write_text(content, encoding="utf-8")
    print(canonical_json({"status": manifest["status"], "artifacts": len(artifacts)}))


if __name__ == "__main__":
    main()
