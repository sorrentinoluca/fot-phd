#!/usr/bin/env python3
"""Run the minimum OpenAI capability probe and one synthetic A/B/E dry-run."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
from typing import Any

import openai

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from phase_b.conditions import render_diagnostic_prompt, render_peer_insight_block  # noqa: E402
from phase_b.config import load_protocol_config  # noqa: E402
from phase_b.execution.openai_adapter import OpenAIAdapter, UNSET  # noqa: E402
from phase_b.insights import Insight, build_fixed_derangements  # noqa: E402


EXECUTION_CONFIG_PATH = ROOT / "phase_b/config/execution_config.json"
PROTOCOL_CONFIG_PATH = ROOT / "phase_b/config/protocol_config.json"
SCHEMA_PATH = ROOT / "phase_b/conditions/diagnostic_output.openai.schema.json"
LOCAL_EXAMPLES_PATH = ROOT / "phase_b/local_knowledge/local_examples.json"
LOCAL_METADATA_PATH = ROOT / "phase_b/config/evaluator_side/local_example_sources.json"
REPORT_PATH = ROOT / "phase_b/reports/LLM_CAPABILITY_PROBE.md"
RAW_PATH = ROOT / "phase_b/reports/LLM_CAPABILITY_PROBE_RAW.json"
MODEL_DOCS = "https://developers.openai.com/api/docs/models/gpt-5.6-terra"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def error_record(exc: Exception) -> dict[str, Any]:
    return {
        "type": type(exc).__name__,
        "status_code": getattr(exc, "status_code", None),
        "request_id": getattr(exc, "request_id", None),
        "message": str(exc),
        "body": getattr(exc, "body", None),
    }


def is_parameter_rejection(exc: Exception, terms: tuple[str, ...]) -> bool:
    if getattr(exc, "status_code", None) != 400:
        return False
    rendered = json.dumps(error_record(exc), ensure_ascii=False).lower()
    return any(term.lower() in rendered for term in terms)


def fixture_insights(config: dict[str, Any]) -> list[Insight]:
    values: list[Insight] = []
    counter = 1
    for agent_id, agent in config["agents"].items():
        for index in (1, 2):
            values.append(
                Insight(
                    insight_id=f"INS-{counter:03d}",
                    source_agent=agent_id,
                    pseudolabel=agent["local_fault_label"],
                    evidence_scope="synthetic capability fixture",
                    observed_pattern=(
                        f"Synthetic observable pattern {index}: a threshold is active in "
                        "three of eight windows and inactive in the final two."
                    ),
                )
            )
            counter += 1
    return values


def examples_for_agent(agent_id: str) -> list[dict[str, str]]:
    prompt_facing = load_json(LOCAL_EXAMPLES_PATH)
    evaluator_side = load_json(LOCAL_METADATA_PATH)
    pack_id = evaluator_side["agent_to_pack"][agent_id]
    return prompt_facing["packs"][pack_id]


def render_fixture_prompts(config: dict[str, Any]) -> dict[str, Any]:
    agent_id = "agent_1"
    examples = examples_for_agent(agent_id)
    insights = fixture_insights(config)
    derangements = build_fixed_derangements(config)
    case_text = (
        "Intervallo sintetico osservato in otto finestre. XMEAS-4 supera una soglia "
        "in tre finestre, con due attivazioni iniziali e nessuna nelle ultime due."
    )
    prompts = {
        condition: render_diagnostic_prompt(
            agent_id=agent_id,
            condition=condition,
            case_text=case_text,
            local_examples=examples,
            config=config,
            global_insights=None if condition == "A" else insights,
            derangements=derangements if condition == "E" else None,
        )
        for condition in ("A", "B", "E")
    }
    peer_chars = {
        condition: len(
            render_peer_insight_block(
                agent_id=agent_id,
                condition=condition,
                config=config,
                global_insights=insights,
                derangements=derangements if condition == "E" else None,
            )
        )
        for condition in ("B", "E")
    }
    template = (ROOT / "phase_b/prompts/isolated_A.txt").read_text(encoding="utf-8")
    shell = template
    for placeholder in (
        "<<LABEL_SPACE>>",
        "<<LOCAL_EXAMPLES>>",
        "<<PEER_INSIGHTS_BLOCK>>",
        "<<CASE_TEXT>>",
    ):
        shell = shell.replace(placeholder, "")
    components = {
        "instruction_shell_characters": len(shell),
        "label_space_characters": len(json.dumps(config["label_space"], ensure_ascii=False)),
        "local_knowledge_characters": len(json.dumps(examples, ensure_ascii=False, indent=2)),
        "peer_insight_characters_B": peer_chars["B"],
        "peer_insight_characters_E": peer_chars["E"],
        "case_text_characters": len(case_text),
        "total_prompt_characters": {
            condition: prompts[condition].character_count for condition in prompts
        },
    }
    return {"agent_id": agent_id, "prompts": prompts, "components": components}


def diagnostic_summary(execution: Any) -> dict[str, Any]:
    return {
        "schema_valid": not execution.result.parse_failure,
        "parse_failure": execution.result.parse_failure,
        "structural_attempts": execution.result.attempts,
        "used_insight_id_count": len(execution.result.parsed_output["used_insight_ids"]),
        "provider_attempts": [item.to_dict() for item in execution.provider_attempts],
    }


def write_report(config: dict[str, Any], raw: dict[str, Any]) -> None:
    status = config["status"]
    if status != "COMPLETE":
        text = f"""# Phase B LLM capability probe

Status: **{status}**

No OpenAI API call was made. `OPENAI_API_KEY` was not present in the process
environment. The adapter reads credentials only from that environment variable;
it does not read `.env` or credential files.

- Provider: OpenAI
- Requested model: `gpt-5.6-terra`
- API family: Responses API (`/v1/responses`)
- Installed SDK: `openai {config['sdk_version']}`
- Requested reasoning effort: `medium`
- Structured output, temperature, seed, returned model, request ID, usage and
  provider token accounting: **unresolved until the authenticated probe runs**
- API calls made: 0

Official model documentation lists `medium` reasoning, Structured Outputs, a
1,050,000-token context window and 128,000 maximum output tokens:
{MODEL_DOCS}

No held-out data, definitive insight, diagnosis performance metric, or accuracy
was accessed or generated.
"""
    else:
        token = raw["token_equivalence"]
        budget = raw["prompt_budget"]
        dry = raw["dry_run"]
        text = f"""# Phase B LLM capability probe

Status: **COMPLETE — capability/plumbing only**

- Provider: OpenAI
- Requested model: `{config['requested_model']}`
- Returned model: `{config['returned_model']}`
- API family: {config['api_family']} (`{config['endpoint']}`)
- Execution date: `{config['execution_date']}`
- SDK: `openai {config['sdk_version']}`
- Reasoning requested/effective: `medium` / `{config['reasoning_effort_effective']}`
- Temperature supported/value: `{config['temperature_supported']}` / `{config['temperature']}`
- Seed supported/value: `{config['seed_supported']}` / `{config['seed']}`
- Structured Output exact-schema path: `{config['structured_output_supported']}` / `{config['structured_output_path']}`
- Token accounting: `{config['token_accounting_source']}`
- Context/max output constraints: {config['context_window_tokens']:,} / {config['max_output_tokens_model']:,} tokens ([official model documentation]({MODEL_DOCS}))

## B/E token equivalence

- Characters B/E: {token['B_characters']} / {token['E_characters']}
- Provider input tokens B/E: {token['B_input_tokens']} / {token['E_input_tokens']}
- Token difference E−B: {token['difference_E_minus_B']}

## Realistic prompt budget

- Instruction shell: {budget['instruction_shell_characters']} characters
- Local knowledge: {budget['local_knowledge_characters']} characters
- Peer block B/E: {budget['peer_insight_characters_B']} / {budget['peer_insight_characters_E']} characters
- Synthetic V2 case: {budget['case_text_characters']} characters
- Total input tokens A/B/E: {budget['input_tokens']}
- Output tokens A/B/E: {budget['output_tokens']}
- Smallest context margin: {budget['minimum_context_margin_tokens']:,} tokens

## Technical A/B/E dry-run

- A: schema valid `{dry['A']['schema_valid']}`, structural attempts `{dry['A']['structural_attempts']}`, used-insight count `{dry['A']['used_insight_id_count']}`
- B: schema valid `{dry['B']['schema_valid']}`, structural attempts `{dry['B']['structural_attempts']}`, used-insight count `{dry['B']['used_insight_id_count']}`
- E: schema valid `{dry['E']['schema_valid']}`, structural attempts `{dry['E']['structural_attempts']}`, used-insight count `{dry['E']['used_insight_id_count']}`

The dry-run used one synthetic neutral case. No correctness, true fault label,
accuracy, confusion, FoT delta, or condition ranking was calculated. Full raw
responses, request IDs and raw usage objects are preserved in
`LLM_CAPABILITY_PROBE_RAW.json`; no API key is stored.
"""
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(text, encoding="utf-8")


def update_protocol_after_probe(execution: dict[str, Any]) -> None:
    protocol = load_json(PROTOCOL_CONFIG_PATH)
    target = protocol["execution"]
    target.update(
        {
            "returned_model": execution["returned_model"],
            "model": execution["requested_model"],
            "model_version": execution["returned_model"],
            "sdk_version": execution["sdk_version"],
            "reasoning_effort": execution["reasoning_effort_effective"],
            "token_accounting_source": execution["token_accounting_source"],
            "capability_probe_status": "COMPLETE",
            "temperature": execution["temperature"],
            "seed": execution["seed"],
            "send_seed_if_supported": execution["seed_supported"],
        }
    )
    write_json(PROTOCOL_CONFIG_PATH, protocol)


def run_probe(adapter: OpenAIAdapter, execution: dict[str, Any]) -> dict[str, Any]:
    protocol = load_protocol_config()
    schema = load_json(SCHEMA_PATH)
    fixture = render_fixture_prompts(protocol)
    events: list[dict[str, Any]] = []

    reasoning_effective: str | None = "medium"
    try:
        response = adapter.create_response(
            prompt="Reply with exactly CAPABILITY_OK.",
            reasoning_effort="medium",
            max_output_tokens=64,
        )
    except Exception as exc:
        events.append({"probe": "reasoning_medium", "success": False, "error": error_record(exc)})
        if not is_parameter_rejection(exc, ("reasoning", "effort")):
            raise
        reasoning_effective = None
        response = adapter.create_response(
            prompt="Reply with exactly CAPABILITY_OK.",
            reasoning_effort=None,
            max_output_tokens=64,
        )
    events.append({"probe": "reasoning_medium", "success": reasoning_effective == "medium", "response": response.to_dict()})

    structured_supported = True
    structured_path = "responses.text.format.json_schema.strict"
    try:
        a_run = adapter.execute_diagnostic(
            prompt=fixture["prompts"]["A"].text,
            label_space=protocol["label_space"],
            allowed_insight_ids=fixture["prompts"]["A"].available_insight_ids,
            reasoning_effort=reasoning_effective,
            schema=schema,
        )
    except Exception as exc:
        events.append({"probe": "structured_output", "success": False, "error": error_record(exc)})
        if not is_parameter_rejection(exc, ("schema", "format", "structured", "text")):
            raise
        structured_supported = False
        structured_path = "prompt_json_plus_local_parser"
        a_run = adapter.execute_diagnostic(
            prompt=fixture["prompts"]["A"].text,
            label_space=protocol["label_space"],
            allowed_insight_ids=fixture["prompts"]["A"].available_insight_ids,
            reasoning_effort=reasoning_effective,
            schema=None,
        )

    temperature_supported = True
    try:
        b_run = adapter.execute_diagnostic(
            prompt=fixture["prompts"]["B"].text,
            label_space=protocol["label_space"],
            allowed_insight_ids=fixture["prompts"]["B"].available_insight_ids,
            reasoning_effort=reasoning_effective,
            schema=schema if structured_supported else None,
            temperature=0.0,
        )
    except Exception as exc:
        events.append({"probe": "temperature_zero", "success": False, "error": error_record(exc)})
        if not is_parameter_rejection(exc, ("temperature",)):
            raise
        temperature_supported = False
        b_run = adapter.execute_diagnostic(
            prompt=fixture["prompts"]["B"].text,
            label_space=protocol["label_space"],
            allowed_insight_ids=fixture["prompts"]["B"].available_insight_ids,
            reasoning_effort=reasoning_effective,
            schema=schema if structured_supported else None,
        )

    seed_supported = True
    try:
        e_run = adapter.execute_diagnostic(
            prompt=fixture["prompts"]["E"].text,
            label_space=protocol["label_space"],
            allowed_insight_ids=fixture["prompts"]["E"].available_insight_ids,
            reasoning_effort=reasoning_effective,
            schema=schema if structured_supported else None,
            seed=execution["seed_probe_value"],
        )
    except Exception as exc:
        events.append({"probe": "seed", "success": False, "error": error_record(exc)})
        if not is_parameter_rejection(exc, ("seed",)):
            raise
        seed_supported = False
        e_run = adapter.execute_diagnostic(
            prompt=fixture["prompts"]["E"].text,
            label_space=protocol["label_space"],
            allowed_insight_ids=fixture["prompts"]["E"].available_insight_ids,
            reasoning_effort=reasoning_effective,
            schema=schema if structured_supported else None,
        )

    dry = {"A": diagnostic_summary(a_run), "B": diagnostic_summary(b_run), "E": diagnostic_summary(e_run)}
    provider_attempts = [
        item for condition in dry.values() for item in condition["provider_attempts"]
    ]
    returned = {item["returned_model"] for item in provider_attempts} | {response.returned_model}
    if len(returned) != 1:
        raise RuntimeError(f"inconsistent returned model identifiers: {sorted(returned)}")
    if any(item["input_tokens"] is None or item["output_tokens"] is None for item in provider_attempts):
        raise RuntimeError("provider did not return complete input/output token accounting")

    b_first = dry["B"]["provider_attempts"][0]
    e_first = dry["E"]["provider_attempts"][0]
    input_tokens = {
        condition: dry[condition]["provider_attempts"][0]["input_tokens"]
        for condition in ("A", "B", "E")
    }
    output_tokens = {
        condition: sum(item["output_tokens"] for item in dry[condition]["provider_attempts"])
        for condition in ("A", "B", "E")
    }
    execution.update(
        {
            "status": "COMPLETE",
            "execution_date": utc_now(),
            "returned_model": returned.pop(),
            "sdk_version": adapter.sdk_version,
            "reasoning_effort_effective": reasoning_effective,
            "temperature_supported": temperature_supported,
            "temperature": 0.0 if temperature_supported else None,
            "seed_supported": seed_supported,
            "seed": execution["seed_probe_value"] if seed_supported else None,
            "structured_output_supported": structured_supported,
            "structured_output_path": structured_path,
            "token_accounting_source": "OpenAI Responses API response.usage",
        }
    )
    return {
        "status": "COMPLETE",
        "execution": execution,
        "capability_events": events,
        "reasoning_probe": response.to_dict(),
        "dry_run": dry,
        "token_equivalence": {
            "B_characters": fixture["prompts"]["B"].character_count,
            "E_characters": fixture["prompts"]["E"].character_count,
            "B_input_tokens": b_first["input_tokens"],
            "E_input_tokens": e_first["input_tokens"],
            "difference_E_minus_B": e_first["input_tokens"] - b_first["input_tokens"],
        },
        "prompt_budget": {
            **fixture["components"],
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "minimum_context_margin_tokens": execution["context_window_tokens"] - max(input_tokens.values()),
        },
        "performance_metrics_calculated": False,
        "heldout_accessed": False,
    }


def main() -> int:
    global RAW_PATH, REPORT_PATH
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=RAW_PATH)
    parser.add_argument("--report", type=Path, default=REPORT_PATH)
    args = parser.parse_args()
    RAW_PATH = args.output.resolve()
    REPORT_PATH = args.report.resolve()

    execution = load_json(EXECUTION_CONFIG_PATH)
    if not os.environ.get("OPENAI_API_KEY"):
        execution.update(
            {
                "status": "BLOCKED_NO_API_KEY",
                "execution_date": utc_now(),
                "sdk_version": openai.__version__,
            }
        )
        protocol = load_json(PROTOCOL_CONFIG_PATH)
        protocol["execution"]["sdk_version"] = openai.__version__
        protocol["execution"]["capability_probe_status"] = "BLOCKED"
        write_json(EXECUTION_CONFIG_PATH, execution)
        write_json(PROTOCOL_CONFIG_PATH, protocol)
        raw = {
            "status": "BLOCKED_NO_API_KEY",
            "api_calls_made": 0,
            "execution_date": execution["execution_date"],
            "sdk_version": openai.__version__,
            "heldout_accessed": False,
            "performance_metrics_calculated": False,
        }
        write_json(RAW_PATH, raw)
        write_report(execution, raw)
        print("Capability probe blocked: OPENAI_API_KEY is not present in the environment.")
        return 2

    adapter = OpenAIAdapter(requested_model=execution["requested_model"])
    raw = run_probe(adapter, execution)
    write_json(EXECUTION_CONFIG_PATH, raw["execution"])
    update_protocol_after_probe(raw["execution"])
    write_json(RAW_PATH, raw)
    write_report(raw["execution"], raw)
    print(f"Capability probe complete: {RAW_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
