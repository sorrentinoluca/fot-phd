#!/usr/bin/env python3
"""Eight-call producer-schema probe; plan-only unless explicitly acknowledged."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import time
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.prepare_gate import DEFAULT_SNAPSHOT, offline_token_counter  # noqa: E402
from studio2.fase03.protocol import (  # noqa: E402
    AGENT_IDS,
    PREFLIGHT_CONFIG_PATH,
    canonical_json,
    load_json,
    sha256_text,
    validate_pilot_input_manifest,
    validate_produced_insights,
)


ACK = "EXECUTE_PHASE03_PRODUCER_CONFORMANCE"
DEFAULT_PREPARED = ROOT / "studio2/fase03/prepared"
DEFAULT_RESULTS = ROOT / "studio2/fase03/results"


def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(content, encoding="utf-8")
    os.replace(temporary, path)


def fixed_fields(insight: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    return {key: insight[key] for key in config["insight_contract"]["fixed_fields"]}


def build_producer_prompt(
    *, agent_id: str, manifest: dict[str, Any], config: dict[str, Any]
) -> tuple[str, list[dict[str, Any]]]:
    owned = sorted(
        (
            item
            for item in manifest["insights"]
            if item["source_agent"] == agent_id
        ),
        key=lambda item: item["insight_id"],
    )
    if len(owned) != 2:
        raise RuntimeError(f"{agent_id} must own exactly two insight contracts")
    fixed = [fixed_fields(item, config) for item in owned]
    skeletons = [dict(item, observed_pattern="FILL THIS FIELD ONLY") for item in fixed]
    prompt = f"""You are an insight producer. Return strict JSON only.

Use only the supplied local development examples. Return exactly two insights in the
given order. Copy every fixed field byte-for-byte. Fill only observed_pattern. Each
observed_pattern must be non-empty, at most {config['insight_contract']['observed_pattern_max_characters']}
characters and at most {config['insight_contract']['observed_pattern_max_tokens']} tokens.
Never paraphrase XMEAS(n) or XMV(n) identifiers.

LOCAL DEVELOPMENT EXAMPLES
{json.dumps(manifest['local_examples'][agent_id], ensure_ascii=False, indent=2)}

FIXED INSIGHT SKELETONS
{json.dumps(skeletons, ensure_ascii=False, indent=2)}

OUTPUT
{{"insights":[...two objects...]}}
"""
    return prompt, fixed


def response_schema(expected: list[dict[str, Any]], config: dict[str, Any]) -> dict[str, Any]:
    properties = []
    for fixed in expected:
        properties.append(
            {
                "type": "object",
                "additionalProperties": False,
                "required": [*config["insight_contract"]["fixed_fields"], "observed_pattern"],
                "properties": {
                    "insight_id": {"const": fixed["insight_id"]},
                    "source_agent": {"const": fixed["source_agent"]},
                    "pseudolabel": {"const": fixed["pseudolabel"]},
                    "evidence_scope": {"const": fixed["evidence_scope"]},
                    "variable_ids": {"const": fixed["variable_ids"]},
                    "observed_pattern": {
                        "type": "string",
                        "minLength": 1,
                        "maxLength": config["insight_contract"][
                            "observed_pattern_max_characters"
                        ],
                    },
                },
            }
        )
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["insights"],
        "properties": {
            "insights": {
                "type": "array",
                "minItems": 2,
                "maxItems": 2,
                "prefixItems": properties,
                "items": False,
            }
        },
    }


def provider_config(preflight: dict[str, Any], override: Path | None) -> dict[str, Any]:
    if override is not None:
        value = load_json(override)
        required = {
            "name",
            "base_url",
            "model",
            "temperature",
            "seed",
            "max_tokens",
            "thinking_token_budget",
            "expected_max_model_len",
        }
        if set(value) != required:
            raise RuntimeError(f"producer provider config keys must be {sorted(required)}")
        return value
    candidate = preflight["candidate"]
    return {
        "name": "qwen27b_preliminary",
        "base_url": candidate["base_url"],
        "model": candidate["requested_model"],
        "temperature": preflight["generation_budget"]["temperature"],
        "seed": preflight["generation_budget"]["seed"],
        "max_tokens": 1536,
        "thinking_token_budget": 1024,
        "expected_max_model_len": candidate["expected_max_model_len"],
    }


def run(
    *, prepared_dir: Path, results_dir: Path, override: Path | None, snapshot: Path
) -> dict[str, Any]:
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "openai SDK is required; use /home/luca/fot-exp2/env-vllm/bin/python"
        ) from exc
    preflight = load_json(PREFLIGHT_CONFIG_PATH)
    plan = load_json(prepared_dir / "pre_gate_plan.json")
    manifest = load_json(Path(plan["source_manifest"]))
    validate_pilot_input_manifest(manifest, preflight)
    provider = provider_config(preflight, override)
    count = offline_token_counter(snapshot, chat_template=False)
    prepared = []
    for agent_id in AGENT_IDS:
        prompt, fixed = build_producer_prompt(
            agent_id=agent_id, manifest=manifest, config=preflight
        )
        input_tokens = count(prompt)
        margin = (
            provider["expected_max_model_len"]
            - input_tokens
            - provider["max_tokens"]
        )
        if margin < preflight["generation_budget"]["context_safety_margin_tokens"]:
            raise RuntimeError(f"producer prompt does not fit context for {agent_id}")
        prepared.append((agent_id, prompt, fixed, input_tokens, margin))

    client = OpenAI(
        api_key=os.environ.get("STUDIO2_PRODUCER_API_KEY", "local-vllm"),
        base_url=provider["base_url"],
        max_retries=0,
        timeout=600.0,
    )
    records = []
    for agent_id, prompt, fixed, input_tokens, margin in prepared:
        kwargs: dict[str, Any] = {
            "model": provider["model"],
            "messages": [{"role": "user", "content": prompt}],
            "temperature": provider["temperature"],
            "seed": provider["seed"],
            "max_tokens": provider["max_tokens"],
            "response_format": {
                "type": "json_schema",
                "json_schema": {
                    "name": "study2_insight_pair",
                    "strict": True,
                    "schema": response_schema(fixed, preflight),
                },
            },
        }
        if provider["thinking_token_budget"] is not None:
            kwargs["extra_body"] = {
                "thinking_token_budget": provider["thinking_token_budget"]
            }
        begin = time.monotonic()
        response = client.chat.completions.create(**kwargs)
        latency = time.monotonic() - begin
        if len(response.choices) != 1:
            raise RuntimeError("provider must return exactly one choice")
        content = response.choices[0].message.content or ""
        validation_error = None
        try:
            validate_produced_insights(
                content,
                expected_fixed_fields=fixed,
                token_count=count,
                config=preflight,
            )
        except Exception as exc:  # recorded as conformance failure, never hidden by retry
            validation_error = str(exc)
        records.append(
            {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "producer": provider["name"],
                "agent_id": agent_id,
                "prompt_sha256": sha256_text(prompt),
                "input_tokens_offline": input_tokens,
                "context_margin_tokens": margin,
                "returned_model": response.model,
                "response_id": response.id,
                "system_fingerprint": getattr(response, "system_fingerprint", None),
                "finish_reason": response.choices[0].finish_reason,
                "latency_seconds": latency,
                "raw_output": content,
                "raw_output_sha256": sha256_text(content),
                "schema_valid_first_attempt": validation_error is None,
                "validation_error": validation_error,
                "retry_count": 0,
                "response_raw": response.model_dump(mode="json"),
            }
        )
    output = results_dir / f"producer_conformance_{provider['name']}.jsonl"
    write_atomic(output, "".join(canonical_json(item) + "\n" for item in records))
    summary = {
        "artifact_version": "1",
        "status": "PASS" if all(item["schema_valid_first_attempt"] for item in records) else "FAIL",
        "producer": provider,
        "provider_requests": len(records),
        "valid_first_attempts": sum(item["schema_valid_first_attempt"] for item in records),
        "records_path": str(output.resolve()),
        "records_sha256": sha256_text(output.read_text(encoding="utf-8")),
        "scope": "schema conformance only; no diagnostic or accuracy claim",
    }
    write_atomic(
        results_dir / f"producer_conformance_{provider['name']}_summary.json",
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
    )
    return summary


def print_plan(preflight: dict[str, Any]) -> None:
    print(
        json.dumps(
            {
                "status": "PLAN_ONLY_NO_PROVIDER_CALLS",
                "script": str(Path(__file__).resolve()),
                "calls_per_producer": 8,
                "insights_per_call": 2,
                "global_insights_checked": 16,
                "fixed_fields": preflight["insight_contract"]["fixed_fields"],
                "generated_field": preflight["insight_contract"]["producer_field"],
                "alternate_provider_requires_frozen_config": True,
            },
            indent=2,
            ensure_ascii=False,
        )
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--prepared-dir", type=Path, default=DEFAULT_PREPARED)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--provider-config", type=Path)
    parser.add_argument("--model-snapshot", type=Path, default=DEFAULT_SNAPSHOT)
    parser.add_argument("--execute", action="store_true")
    parser.add_argument("--acknowledge")
    args = parser.parse_args()
    preflight = load_json(PREFLIGHT_CONFIG_PATH)
    if not args.execute:
        print_plan(preflight)
        return 0
    if args.acknowledge != ACK:
        raise SystemExit(f"execution requires --acknowledge {ACK}")
    summary = run(
        prepared_dir=args.prepared_dir,
        results_dir=args.results_dir,
        override=args.provider_config,
        snapshot=args.model_snapshot,
    )
    print(canonical_json(summary))
    return 0 if summary["status"] == "PASS" else 2


if __name__ == "__main__":
    raise SystemExit(main())
