#!/usr/bin/env python3
"""Prepare and hash the Phase 03 pilot without contacting a model server."""

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

from studio2.fase03.protocol import (  # noqa: E402
    PREFLIGHT_CONFIG_PATH,
    PHASE_DIR,
    build_pilot_sample,
    canonical_json,
    context_feasibility,
    load_json,
    sha256_file,
)
from studio2.fase03.synthetic_fixture import build_synthetic_manifest  # noqa: E402


DEFAULT_SNAPSHOT = Path(
    "/home/luca/fot-exp2/cache/huggingface/hub/"
    "models--Qwen--Qwen3.8-27B-FP8/snapshots/"
    "017b9c7af6b5689d5dd426a76e0bc077eb5ca20a"
)
DEFAULT_OUTPUT_DIR = PHASE_DIR / "prepared"
PROVISIONAL_PREPARE_ACK = "PREPARE_PHASE03_PROVISIONAL_CAP_STRESS"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def tokenized_length(tokens: Any) -> int:
    """Return token count for either a token-id list or a BatchEncoding-like value."""
    if hasattr(tokens, "get"):
        input_ids = tokens.get("input_ids")
        if input_ids is None:
            raise RuntimeError("tokenizer result has no input_ids")
        if input_ids and isinstance(input_ids[0], (list, tuple)):
            if len(input_ids) != 1:
                raise RuntimeError("expected exactly one tokenized prompt")
            input_ids = input_ids[0]
        return len(input_ids)
    return len(tokens)


def offline_token_counter(snapshot: Path, *, chat_template: bool = True):
    """Load local tokenizer assets for a full chat prompt or an unwrapped text field."""
    if not snapshot.is_dir():
        raise RuntimeError(f"local tokenizer snapshot not found: {snapshot}")
    try:
        from transformers import AutoTokenizer
    except ImportError as exc:
        raise RuntimeError(
            "transformers is required; use /home/luca/fot-exp2/env-vllm/bin/python"
        ) from exc
    tokenizer = AutoTokenizer.from_pretrained(
        str(snapshot), local_files_only=True, trust_remote_code=False
    )

    def count(prompt: str) -> int:
        if chat_template:
            try:
                tokens = tokenizer.apply_chat_template(
                    [{"role": "user", "content": prompt}],
                    tokenize=True,
                    add_generation_prompt=True,
                )
            except (TypeError, ValueError):
                tokens = tokenizer.encode(prompt, add_special_tokens=True)
        else:
            tokens = tokenizer.encode(prompt, add_special_tokens=False)
        # transformers 5 returns BatchEncoding here, whereas older releases
        # return the input-id list directly.  len(BatchEncoding) counts keys
        # (normally two), not tokens.
        return tokenized_length(tokens)

    count.snapshot = str(snapshot)  # type: ignore[attr-defined]
    count.chat_template = chat_template  # type: ignore[attr-defined]
    return count


def prepare(
    input_manifest_path: Path,
    snapshot: Path,
    output_dir: Path,
    *,
    allow_synthetic: bool = False,
) -> dict[str, Any]:
    config = load_json(PREFLIGHT_CONFIG_PATH)
    manifest = load_json(input_manifest_path)
    token_count = offline_token_counter(snapshot)
    prompts = build_pilot_sample(
        manifest,
        config,
        token_count=token_count,
        allow_synthetic=allow_synthetic,
    )
    feasibility = context_feasibility(prompts, config)
    prompt_path = output_dir / "pilot_prompts.jsonl"
    prompt_lines = "".join(canonical_json(item.to_dict()) + "\n" for item in prompts)
    write_atomic(prompt_path, prompt_lines)

    plan = {
        "artifact_version": "1",
        "status": (
            (
                "READY_FOR_PROVISIONAL_STRESS_BUDGET_PROBE"
                if allow_synthetic
                else "READY_FOR_PRE_GATE_GENERATION_PROBE"
            )
            if feasibility["static_context_gate"] == "PASS"
            else "NO_GO_STATIC_CONTEXT"
        ),
        "scope": (
            "SYNTHETIC_CAP_STRESS_TECHNICAL_PROBE_ONLY"
            if allow_synthetic
            else "PRE_GATE_ONLY_NOT_STABILITY"
        ),
        "provisional_synthetic": allow_synthetic,
        "prepared_at": utc_now(),
        "source_manifest": str(input_manifest_path.resolve()),
        "source_manifest_sha256": sha256_file(input_manifest_path),
        "source_commit": manifest["source_commit"],
        "catalog_id": manifest["catalog_id"],
        "preflight_config_sha256": sha256_file(PREFLIGHT_CONFIG_PATH),
        "tokenizer_snapshot": str(snapshot.resolve()),
        "tokenizer_config_sha256": sha256_file(snapshot / "tokenizer_config.json"),
        "tokenizer_json_sha256": sha256_file(snapshot / "tokenizer.json"),
        "prompt_file": str(prompt_path.resolve()),
        "prompt_count": len(prompts),
        "condition_counts": {
            condition: sum(item.condition == condition for item in prompts)
            for condition in ("A", "B-LF", "E-LF")
        },
        "context_feasibility": feasibility,
        "generation_budget_frozen": False,
        "stability_gate_authorized": False,
        "real_prompt_repeat_required": allow_synthetic,
    }
    plan_path = output_dir / "pre_gate_plan.json"
    write_atomic(plan_path, json.dumps(plan, indent=2, ensure_ascii=False) + "\n")
    hashes = {
        "artifact_version": "1",
        "files": {
            str(prompt_path.relative_to(ROOT)): sha256_file(prompt_path),
            str(plan_path.relative_to(ROOT)): sha256_file(plan_path),
            str(PREFLIGHT_CONFIG_PATH.relative_to(ROOT)): sha256_file(PREFLIGHT_CONFIG_PATH),
            str(input_manifest_path.resolve()): sha256_file(input_manifest_path),
        },
    }
    write_atomic(
        output_dir / "pre_gate_hashes.json",
        json.dumps(hashes, indent=2, ensure_ascii=False) + "\n",
    )
    return plan


def inventory() -> dict[str, Any]:
    config = load_json(PREFLIGHT_CONFIG_PATH)
    return {
        "status": config["status"],
        "model_calls": 0,
        "dependencies": config["dependencies"],
        "implementation_status": config["implementation_status"],
        "subordinated_checks": config["subordinated_checks"],
        "next_command_requires_independently_frozen_study2_pilot_inputs": True,
        "provisional_cap_stress_path_requires_separate_acknowledgement": True,
        "provisional_cap_stress_never_authorizes_stability_gate": True,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-manifest", type=Path)
    parser.add_argument("--synthetic-profile", choices=("cap_stress",))
    parser.add_argument("--model-snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--acknowledge")
    args = parser.parse_args()
    if args.input_manifest is not None and args.synthetic_profile is not None:
        raise SystemExit("choose either --input-manifest or --synthetic-profile")
    if args.synthetic_profile is not None:
        if args.acknowledge != PROVISIONAL_PREPARE_ACK:
            raise SystemExit(
                "synthetic preparation requires --acknowledge " + PROVISIONAL_PREPARE_ACK
            )
        manifest_path = args.output_dir / "synthetic_cap_stress_manifest.json"
        write_atomic(
            manifest_path,
            json.dumps(
                build_synthetic_manifest(args.synthetic_profile),
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
        )
        result = prepare(
            manifest_path,
            args.model_snapshot,
            args.output_dir,
            allow_synthetic=True,
        )
        print(canonical_json(result))
        return 0 if result["status"] == "READY_FOR_PROVISIONAL_STRESS_BUDGET_PROBE" else 2
    if args.input_manifest is None:
        print(json.dumps(inventory(), indent=2, ensure_ascii=False))
        return 3
    result = prepare(args.input_manifest, args.model_snapshot, args.output_dir)
    print(canonical_json(result))
    return 0 if result["status"] == "READY_FOR_PRE_GATE_GENERATION_PROBE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
