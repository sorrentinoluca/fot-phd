#!/usr/bin/env python3
"""Run schema, validator, harness and token checks on declared synthetic fixtures."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.prepare_gate import DEFAULT_SNAPSHOT, offline_token_counter  # noqa: E402
from studio2.fase03.protocol import (  # noqa: E402
    DIAGNOSTIC_SCHEMA_PATH,
    INSIGHT_SCHEMA_PATH,
    PREFLIGHT_CONFIG_PATH,
    build_pilot_sample,
    canonical_json,
    context_feasibility,
    load_json,
    parse_diagnostic_output,
    sha256_file,
    sha256_text,
    validate_pilot_input_manifest,
    validate_produced_insights,
)
from studio2.fase03.synthetic_fixture import build_synthetic_manifest  # noqa: E402


DEFAULT_OUTPUT = ROOT / "studio2/fase03/offline/OFFLINE_VERIFICATION.json"


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def check_json_schemas() -> list[dict[str, str]]:
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise RuntimeError(
            "jsonschema is required; use /home/luca/fot-exp2/env-vllm/bin/python"
        ) from exc
    paths = [
        DIAGNOSTIC_SCHEMA_PATH,
        INSIGHT_SCHEMA_PATH,
        ROOT / "studio2/fase03/schemas/pilot_input_manifest.schema.json",
    ]
    rows = []
    for path in paths:
        Draft202012Validator.check_schema(load_json(path))
        rows.append({"path": str(path.relative_to(ROOT)), "sha256": sha256_file(path)})
    return rows


def verify_profile(
    profile: str, config: dict[str, Any], prompt_token_count, narrative_token_count
) -> dict[str, Any]:
    manifest = build_synthetic_manifest(profile)
    validate_pilot_input_manifest(manifest, config, allow_synthetic=True)
    prompts = build_pilot_sample(
        manifest,
        config,
        token_count=prompt_token_count,
        allow_synthetic=True,
    )
    condition_counts = {
        condition: sum(item.condition == condition for item in prompts)
        for condition in ("A", "B-LF", "E-LF")
    }
    peer_counts = sorted(
        {len(item.available_insight_ids) for item in prompts if item.condition != "A"}
    )
    expected = manifest["insights"][:2]
    fixed = [
        {field: item[field] for field in config["insight_contract"]["fixed_fields"]}
        for item in expected
    ]
    validate_produced_insights(
        canonical_json({"insights": expected}),
        expected_fixed_fields=fixed,
        token_count=narrative_token_count,
        config=config,
    )
    parse_diagnostic_output(
        canonical_json(
            {
                "predicted_label": None,
                "abstain": True,
                "used_insight_ids": [],
                "reasoning_summary": "SYNTHETIC OFFLINE ONLY abstention fixture.",
            }
        ),
        label_space=manifest["label_space"],
        allowed_insight_ids=[],
    )
    prompt_digest = sha256_text("".join(item.prompt_sha256 for item in prompts))
    return {
        "profile": profile,
        "fixture_status": manifest["status"],
        "provenance_kind": manifest["provenance_kind"],
        "catalog_id": manifest["catalog_id"],
        "scientific_data": False,
        "fault_selection": False,
        "simulations_generated": 0,
        "model_calls": 0,
        "prompt_count": len(prompts),
        "condition_counts": condition_counts,
        "peer_insight_counts": peer_counts,
        "unique_prompt_hashes": len({item.prompt_sha256 for item in prompts}),
        "combined_prompt_hash": prompt_digest,
        "context": context_feasibility(prompts, config),
    }


def run(snapshot: Path) -> dict[str, Any]:
    config = load_json(PREFLIGHT_CONFIG_PATH)
    prompt_token_count = offline_token_counter(snapshot, chat_template=True)
    narrative_token_count = offline_token_counter(snapshot, chat_template=False)
    profiles = [
        verify_profile(name, config, prompt_token_count, narrative_token_count)
        for name in ("nominal", "cap_stress")
    ]
    return {
        "artifact_version": "1",
        "status": "PASS_OFFLINE_ONLY",
        "executed_at": datetime.now(timezone.utc).isoformat(),
        "scope": "synthetic schema, validator, renderer and offline token-count verification",
        "explicit_exclusions": [
            "model inference",
            "HTTP endpoint access",
            "40x3 stability gate",
            "producer calls",
            "fault selection",
            "simulation or scientific data generation",
            "complete configuration freeze for a real gate"
        ],
        "model_calls": 0,
        "http_calls": 0,
        "canonical_endpoint": {
            "base_url": config["candidate"]["base_url"],
            "max_model_len": config["candidate"]["expected_max_model_len"],
            "vllm_version": config["candidate"]["expected_vllm_version"],
            "expected_process": config["candidate"]["expected_process"],
            "gpu_kv_cache": config["candidate"]["gpu_kv_cache"],
            "supersedes": config["candidate"]["supersedes"],
            "runtime_contacted_by_this_verification": False,
        },
        "gate_submission_freeze": {
            "status": config["gate_submission_freeze"]["status"],
            "not_yet_frozen": config["gate_submission_freeze"]["not_yet_frozen"],
        },
        "schemas": check_json_schemas(),
        "preflight_config_sha256": sha256_file(PREFLIGHT_CONFIG_PATH),
        "tokenizer_snapshot": str(snapshot.resolve()),
        "tokenizer_json_sha256": sha256_file(snapshot / "tokenizer.json"),
        "token_counting": {
            "diagnostic_input": "Qwen chat template with generation prompt",
            "observed_pattern_cap": "raw field without special tokens"
        },
        "profiles": profiles,
        "interpretation": (
            "Synthetic token counts exercise the implementation and expose nominal/cap-bound "
            "arithmetic only. They neither establish representativeness nor authorize a real "
            "budget or stability gate; those require independently frozen Study 2 inputs."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    result = run(args.model_snapshot)
    write_atomic(args.output, json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(canonical_json(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
