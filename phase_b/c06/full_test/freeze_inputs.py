"""Freeze the complete C06 full-test protocol and artifact inventory."""

from __future__ import annotations

from datetime import datetime, timezone
import json

from phase_b.c06.constants import (
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
    SDK_VERSION,
    VARIANT,
    VERBALIZATION_GOVERNANCE_COMMIT,
    VERBALIZATION_PAYLOAD_COMMIT,
    VERBALIZATION_TAG,
)
from phase_b.c06.prompt_variant import canonical_json, sha256_bytes, sha256_file

from .constants import (
    FULL_TEST_ROOT,
    GATES,
    PLANNED_AGENT_CASES,
    PLANNED_CALLS,
    ROOT,
)


# All artifacts that must be frozen before inference
ARTIFACTS = (
    # Screening-layer dependencies (inherited)
    "phase_b/c06/C06_SCREENING_PROTOCOL.md",
    "phase_b/c06/__init__.py",
    "phase_b/c06/constants.py",
    "phase_b/c06/prompt_variant.py",
    "phase_b/c06/prompts/B_FROZEN_RECONSTRUCTED.txt",
    "phase_b/c06/prompts/B_LOCAL_FIRST_V1.diff",
    "phase_b/c06/prompts/B_LOCAL_FIRST_V1.txt",
    # Full-test-specific artifacts
    "phase_b/c06/full_test/__init__.py",
    "phase_b/c06/full_test/constants.py",
    "phase_b/c06/full_test/build_assets.py",
    "phase_b/c06/full_test/run_full_test.py",
    "phase_b/c06/full_test/evaluate.py",
    "phase_b/c06/full_test/freeze_inputs.py",
    "phase_b/c06/full_test/C06_FULL_TEST_PROTOCOL.md",
    "phase_b/c06/full_test/full_test_schedule.json",
    "phase_b/c06/full_test/full_test_prompt_hash_manifest.json",
    "phase_b/c06/full_test/evaluator_side/full_test_targets.json",
)


def main() -> None:
    inference_root = FULL_TEST_ROOT / "inference"
    if inference_root.exists() and any(inference_root.rglob("*")):
        raise RuntimeError("cannot freeze inputs after an inference artifact exists")

    artifacts = []
    for relative in ARTIFACTS:
        path = ROOT / relative
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"missing or symlinked artifact: {relative}")
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
        "scope": "full_test",
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
            "agent_case_count": PLANNED_AGENT_CASES,
            "repetitions": REPETITIONS,
            "planned_calls": PLANNED_CALLS,
            "max_output_tokens": MAX_OUTPUT_TOKENS,
            "max_structural_retries": MAX_STRUCTURAL_RETRIES,
            "temperature_sent": False,
            "seed_sent": False,
            "store": False,
            "stateless": True,
            "aggregation": "two-of-three label majority",
        },
        "gate": {
            **GATES,
            "description": (
                "local-seen >= 23/24, local-unseen >= 67/72, "
                "Normal = 24/24, parse failures = 0"
            ),
        },
        "screening_reference": {
            "screening_gate": "PASS",
            "screening_accuracy": "23/24",
            "screening_manifest": "phase_b/c06/C06_INPUT_FREEZE_MANIFEST.json",
        },
        "experiment_artifacts": artifacts,
    }

    path = FULL_TEST_ROOT / "C06_FULL_TEST_FREEZE_MANIFEST.json"
    content = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") != content:
        path.unlink()
    path.write_text(content, encoding="utf-8")
    print(canonical_json({"status": manifest["status"], "artifacts": len(artifacts)}))


if __name__ == "__main__":
    main()
