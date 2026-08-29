#!/usr/bin/env python3
"""Generate the one-shot Phase B local insight library from development 1-5."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "code"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from phase_b.conditions.parser import (  # noqa: E402
    OutputValidationError,
    parse_insight_generation_output,
    strict_json_loads,
)
from phase_b.config import load_protocol_config  # noqa: E402
from phase_b.execution.openai_adapter import OpenAIAdapter  # noqa: E402
from phase_b.guard import project_guard  # noqa: E402
from phase_b.insights import (  # noqa: E402
    build_fixed_derangements,
    corrupt_peer_insights,
    peer_only_insights,
    validate_global_insights,
)
from phase_b.prompts.leakage import scan_files, scan_text  # noqa: E402
from tep_verbalize_v2 import (  # noqa: E402
    load_config as load_v2_config,
    load_development_baseline,
    verbalize_case,
)


INSIGHT_DIR = ROOT / "phase_b/insights"
INPUT_DIR = INSIGHT_DIR / "input_bundles"
PEER_DIR = INSIGHT_DIR / "peer_libraries"
TEMPLATE_PATH = ROOT / "phase_b/prompts/insight_generation.txt"
PROVIDER_SCHEMA_PATH = INSIGHT_DIR / "insight_generation.openai.schema.json"
LOCAL_SCHEMA_PATH = INSIGHT_DIR / "insight.schema.json"
EXECUTION_CONFIG_PATH = ROOT / "phase_b/config/execution_config.json"
MAPPING_PATH = ROOT / "phase_b/config/evaluator_side/pseudolabel_mapping.json"
DERANGEMENT_PATH = ROOT / "phase_b/config/evaluator_side/condition_e_derangements.json"
FINAL_LIBRARY_PATH = INSIGHT_DIR / "final_local_insights.json"
RUNS_PATH = INSIGHT_DIR / "generation_runs.json"
HASHES_PATH = INSIGHT_DIR / "final_insight_hashes.json"
REPORT_PATH = INSIGHT_DIR / "FINAL_INSIGHT_GENERATION_REPORT.md"
CACHE_DIR = CODE / "tep_cache"
NORMAL_PATH = CACHE_DIR / "mode1_normal_500.xlsx"
EVIDENCE_SCOPE = "five local development neutral-text examples"
DEVELOPMENT_BATCHES = [1, 2, 3, 4, 5]
CORRECTION_SUFFIX = """

CORRECTION REQUIRED
The previous response failed the structural validator. Return exactly two insight
objects using the supplied fixed IDs in the supplied order. Preserve source_agent,
pseudolabel, and evidence_scope verbatim. Do not add keys, markdown, confidence,
ranking, or commentary.
""".rstrip()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def prepare_input_bundles() -> tuple[dict[str, dict[str, Any]], dict[str, str]]:
    guard = project_guard(ROOT)
    protocol = load_protocol_config()
    mapping = load_json(MAPPING_PATH)["real_to_opaque"]
    opaque_to_real = {opaque: real for real, opaque in mapping.items()}
    v2_config = load_v2_config(CODE / "verbalizer_config_v2.json")
    baseline = load_development_baseline(guard.assert_allowed(NORMAL_PATH), v2_config)
    bundles: dict[str, dict[str, Any]] = {}
    hashes: dict[str, str] = {}
    input_counter = 1
    for agent_id, agent in protocol["agents"].items():
        pseudolabel = agent["local_fault_label"]
        real_number = int(opaque_to_real[pseudolabel][1:])
        neutral_texts: list[str] = []
        for batch in DEVELOPMENT_BATCHES:
            source = guard.assert_allowed(CACHE_DIR / f"mode1_{real_number}_{batch}.xlsx")
            result = verbalize_case(
                pd.read_excel(source), baseline, config=v2_config, end_h=50.0
            )
            neutral_texts.append(result["text"])
            input_counter += 1
        bundle = {
            "artifact_version": "1",
            "scope": "PROMPT_FACING_DEVELOPMENT_ONLY",
            "source_agent": agent_id,
            "pseudolabel": pseudolabel,
            "evidence_scope": EVIDENCE_SCOPE,
            "neutral_texts": neutral_texts,
            "contains_structured_numerical_json": False,
        }
        if len(neutral_texts) != 5 or any(not text.strip() for text in neutral_texts):
            raise RuntimeError(f"{agent_id} does not have five neutral texts")
        if scan_text(canonical_json(bundle), source=f"input_bundle:{agent_id}"):
            raise RuntimeError(f"leakage detected in {agent_id} input bundle")
        path = INPUT_DIR / f"{agent_id}.json"
        write_json(path, bundle)
        bundles[agent_id] = bundle
        hashes[agent_id] = sha256_file(path)
    if input_counter != 21:
        raise AssertionError("expected exactly twenty development fault inputs")
    return bundles, hashes


def render_prompt(bundle: dict[str, Any]) -> tuple[str, list[str]]:
    agent_id = bundle["source_agent"]
    agent_number = int(agent_id.split("_")[1])
    insight_ids = [f"INS-{2 * agent_number - 1:03d}", f"INS-{2 * agent_number:03d}"]
    prompt_examples = [
        {"pseudolabel": bundle["pseudolabel"], "neutral_text": text}
        for text in bundle["neutral_texts"]
    ]
    rendered = (
        TEMPLATE_PATH.read_text(encoding="utf-8")
        .replace("<<LOCAL_LABEL>>", bundle["pseudolabel"])
        .replace("<<LOCAL_EXAMPLES>>", json.dumps(prompt_examples, ensure_ascii=False, indent=2))
        .replace("<<SOURCE_AGENT>>", agent_id)
        .replace("<<EVIDENCE_SCOPE>>", bundle["evidence_scope"])
        .replace("<<INSIGHT_IDS>>", json.dumps(insight_ids))
    )
    if "<<" in rendered or ">>" in rendered:
        raise RuntimeError(f"unrendered insight prompt placeholder for {agent_id}")
    if scan_text(rendered, source=f"generation_prompt:{agent_id}"):
        raise RuntimeError(f"leakage detected in generation prompt for {agent_id}")
    return rendered, insight_ids


def parse_provider_output(
    raw: str,
    *,
    expected_ids: list[str],
    source_agent: str,
    pseudolabel: str,
    label_space: list[str],
) -> list[Any]:
    transport = strict_json_loads(raw)
    if not isinstance(transport, dict) or set(transport) != {"insights"}:
        raise OutputValidationError("provider transport must contain only insights")
    local_raw = json.dumps(transport["insights"], ensure_ascii=False)
    return parse_insight_generation_output(
        local_raw,
        expected_ids=expected_ids,
        source_agent=source_agent,
        pseudolabel=pseudolabel,
        evidence_scope=EVIDENCE_SCOPE,
        label_space=label_space,
    )


def write_partial_runs(journal: dict[str, Any]) -> None:
    write_json(RUNS_PATH, journal)


def generate(
    bundles: dict[str, dict[str, Any]], input_hashes: dict[str, str]
) -> tuple[list[Any], dict[str, Any], dict[str, str]]:
    protocol = load_protocol_config()
    execution = load_json(EXECUTION_CONFIG_PATH)
    provider_schema = load_json(PROVIDER_SCHEMA_PATH)
    adapter = OpenAIAdapter(requested_model="gpt-5.6-terra")
    journal: dict[str, Any] = {
        "status": "IN_PROGRESS",
        "policy": {
            "generation_count": 4,
            "insights_per_generation": 2,
            "max_structural_retries": 2,
            "first_structurally_valid_output_wins": True,
            "content_based_retry_or_selection": False,
        },
        "provider": "openai",
        "requested_model": "gpt-5.6-terra",
        "reasoning_effort": "medium",
        "temperature": None,
        "seed": None,
        "structured_outputs_strict": True,
        "development_scope": DEVELOPMENT_BATCHES,
        "generations": [],
    }
    parsed_all: list[Any] = []
    prompt_hashes: dict[str, str] = {}
    for agent_id in protocol["agents"]:
        bundle = bundles[agent_id]
        base_prompt, expected_ids = render_prompt(bundle)
        prompt_hashes[agent_id] = sha256_text(base_prompt)
        generation: dict[str, Any] = {
            "source_agent": agent_id,
            "pseudolabel": bundle["pseudolabel"],
            "development_scope": DEVELOPMENT_BATCHES,
            "requested_model": "gpt-5.6-terra",
            "reasoning_effort": "medium",
            "temperature": None,
            "seed": None,
            "prompt_hash": prompt_hashes[agent_id],
            "input_bundle_hash": input_hashes[agent_id],
            "expected_insight_ids": expected_ids,
            "attempts": [],
            "status": "IN_PROGRESS",
        }
        journal["generations"].append(generation)
        write_partial_runs(journal)
        parsed_final: list[Any] | None = None
        final_response: Any = None
        for attempt_index in range(1, 4):
            attempt_prompt = (
                base_prompt if attempt_index == 1 else base_prompt + "\n\n" + CORRECTION_SUFFIX
            )
            try:
                response = adapter.create_response(
                    prompt=attempt_prompt,
                    reasoning_effort="medium",
                    schema=provider_schema,
                    max_output_tokens=int(execution["dry_run_max_output_tokens"]),
                )
            except Exception as exc:
                generation["status"] = "BLOCKED_PROVIDER_ERROR"
                generation["provider_error"] = {
                    "type": type(exc).__name__,
                    "status_code": getattr(exc, "status_code", None),
                    "request_id": getattr(exc, "request_id", None),
                    "message": str(exc),
                }
                journal["status"] = "BLOCKED"
                write_partial_runs(journal)
                raise RuntimeError(f"provider error for {agent_id}") from exc
            timestamp = utc_now()
            attempt: dict[str, Any] = {
                "attempt": attempt_index,
                "attempt_prompt_hash": sha256_text(attempt_prompt),
                "timestamp": timestamp,
                "raw_output": response.raw_output,
                "raw_output_hash": sha256_text(response.raw_output),
                "provider_response": response.to_dict(),
                "structurally_valid": False,
                "validation_error": None,
            }
            generation["attempts"].append(attempt)
            write_partial_runs(journal)
            try:
                parsed = parse_provider_output(
                    response.raw_output,
                    expected_ids=expected_ids,
                    source_agent=agent_id,
                    pseudolabel=bundle["pseudolabel"],
                    label_space=protocol["label_space"],
                )
            except OutputValidationError as exc:
                attempt["validation_error"] = str(exc)
                write_partial_runs(journal)
                if attempt_index == 3:
                    generation["status"] = "BLOCKED_STRUCTURAL_FAILURE"
                    generation["retry_count"] = 2
                    journal["status"] = "BLOCKED"
                    write_partial_runs(journal)
                    raise RuntimeError(f"structural validation exhausted for {agent_id}") from exc
                continue
            attempt["structurally_valid"] = True
            parsed_final = parsed
            final_response = response
            generation.update(
                {
                    "status": "COMPLETE",
                    "parsed_final_response": [item.to_dict() for item in parsed],
                    "parsed_response_hash": sha256_text(
                        canonical_json([item.to_dict() for item in parsed])
                    ),
                    "raw_response_hash": attempt["raw_output_hash"],
                    "first_valid_attempt": attempt_index,
                    "attempt_count": attempt_index,
                    "retry_count": attempt_index - 1,
                    "first_structurally_valid_output_wins": True,
                    "returned_model": response.returned_model,
                    "response_id": response.response_id,
                    "request_id": response.request_id,
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                    "total_tokens": response.total_tokens,
                    "timestamp": timestamp,
                }
            )
            write_partial_runs(journal)
            break
        if parsed_final is None or final_response is None:
            raise AssertionError("generation loop ended without valid output or failure")
        parsed_all.extend(parsed_final)
    journal["status"] = "COMPLETE"
    journal["generation_completed"] = 4
    journal["final_insight_count"] = 8
    write_partial_runs(journal)
    return parsed_all, journal, prompt_hashes


def normalized_peer_bytes(path: Path, labels: list[str]) -> bytes:
    text = path.read_text(encoding="utf-8")
    for label in labels:
        text = text.replace(f'"{label}"', '"<LABEL>"')
    return text.encode("utf-8")


def build_peer_libraries(
    insights: list[Any], protocol: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, str]]:
    frozen = load_json(DERANGEMENT_PATH)["derangements"]
    if frozen != build_fixed_derangements(protocol):
        raise RuntimeError("frozen derangement differs from deterministic protocol")
    audit: dict[str, Any] = {}
    hashes: dict[str, str] = {}
    all_labels = protocol["label_space"][:-1]
    for agent_id in protocol["agents"]:
        b_items = peer_only_insights(insights, agent_id, protocol)
        e_items = corrupt_peer_insights(
            b_items, agent_id=agent_id, derangements=frozen
        )
        b_path = PEER_DIR / f"{agent_id}_B.json"
        e_path = PEER_DIR / f"{agent_id}_E.json"
        write_json(b_path, [item.to_dict() for item in b_items])
        write_json(e_path, [item.to_dict() for item in e_items])
        hashes[f"{agent_id}_B"] = sha256_file(b_path)
        hashes[f"{agent_id}_E"] = sha256_file(e_path)
        peer_labels = set(all_labels) - {protocol["agents"][agent_id]["local_fault_label"]}
        expected_counts = Counter({label: 2 for label in peer_labels})
        same_nonlabel_fields = all(
            (
                before.insight_id,
                before.source_agent,
                before.evidence_scope,
                before.observed_pattern,
            )
            == (
                after.insight_id,
                after.source_agent,
                after.evidence_scope,
                after.observed_pattern,
            )
            for before, after in zip(b_items, e_items)
        )
        zero_fixed_point = all(
            before.pseudolabel != after.pseudolabel
            for before, after in zip(b_items, e_items)
        )
        normalized_equal = normalized_peer_bytes(b_path, all_labels) == normalized_peer_bytes(
            e_path, all_labels
        )
        character_equal = len(b_path.read_text(encoding="utf-8")) == len(
            e_path.read_text(encoding="utf-8")
        )
        checks = {
            "B_count": len(b_items),
            "E_count": len(e_items),
            "same_ids": [item.insight_id for item in b_items]
            == [item.insight_id for item in e_items],
            "same_order": [item.insight_id for item in b_items]
            == [item.insight_id for item in e_items],
            "same_nonlabel_prompt_fields": same_nonlabel_fields,
            "B_label_multiset_valid": Counter(item.pseudolabel for item in b_items)
            == expected_counts,
            "E_label_multiset_valid": Counter(item.pseudolabel for item in e_items)
            == expected_counts,
            "zero_fixed_point": zero_fixed_point,
            "normalized_byte_identical": normalized_equal,
            "character_equivalent": character_equal,
        }
        if checks["B_count"] != 6 or checks["E_count"] != 6 or not all(
            value for key, value in checks.items() if key not in {"B_count", "E_count"}
        ):
            raise RuntimeError(f"B/E audit failed for {agent_id}")
        audit[agent_id] = checks
    return audit, hashes


def leakage_audit(journal: dict[str, Any]) -> dict[str, Any]:
    paths = [
        TEMPLATE_PATH,
        INPUT_DIR,
        FINAL_LIBRARY_PATH,
        PEER_DIR,
        PROVIDER_SCHEMA_PATH,
        LOCAL_SCHEMA_PATH,
    ]
    findings = scan_files(paths)
    for generation in journal["generations"]:
        for attempt in generation["attempts"]:
            findings.extend(
                scan_text(
                    attempt["raw_output"],
                    source=f"raw:{generation['source_agent']}:{attempt['attempt']}",
                )
            )
    filename_findings = []
    for path in [*INPUT_DIR.glob("*"), *PEER_DIR.glob("*"), FINAL_LIBRARY_PATH]:
        filename_findings.extend(scan_text(path.name, source=f"filename:{path.name}"))
    findings.extend(filename_findings)
    if findings:
        raise RuntimeError(f"leakage audit failed with {len(findings)} findings")
    return {
        "status": "PASS",
        "finding_count": 0,
        "generation_prompts_scanned": 4,
        "raw_attempts_scanned": sum(len(item["attempts"]) for item in journal["generations"]),
        "prompt_facing_artifacts_scanned": True,
        "filenames_scanned": True,
    }


def build_hash_manifest(
    journal: dict[str, Any],
    input_hashes: dict[str, str],
    prompt_hashes: dict[str, str],
    peer_hashes: dict[str, str],
) -> dict[str, Any]:
    raw_hashes = {
        f"{generation['source_agent']}_attempt_{attempt['attempt']}": attempt["raw_output_hash"]
        for generation in journal["generations"]
        for attempt in generation["attempts"]
    }
    return {
        "sha256": {
            "insight_generation_prompt_template": sha256_file(TEMPLATE_PATH),
            "input_bundles": input_hashes,
            "rendered_generation_prompts": prompt_hashes,
            "raw_generation_outputs": raw_hashes,
            "final_local_insights": sha256_file(FINAL_LIBRARY_PATH),
            "peer_libraries": peer_hashes,
            "pseudolabel_mapping": sha256_file(MAPPING_PATH),
            "derangement_config": sha256_file(DERANGEMENT_PATH),
            "execution_config": sha256_file(EXECUTION_CONFIG_PATH),
            "local_insight_schema": sha256_file(LOCAL_SCHEMA_PATH),
            "provider_insight_schema": sha256_file(PROVIDER_SCHEMA_PATH),
        }
    }


def write_report(
    journal: dict[str, Any],
    audit: dict[str, Any],
    leakage: dict[str, Any],
    hashes: dict[str, Any],
) -> None:
    attempts = {
        item["source_agent"]: (item["attempt_count"], item["retry_count"])
        for item in journal["generations"]
    }
    lines = [
        "# Phase B final local insight generation — structural report",
        "",
        "Status: **COMPLETE — content not evaluated**",
        "",
        "- Generation completed: 4/4",
        "- Final insight count: 8",
        "- Count per source agent: 2 each",
        "- First structurally valid output wins: PASS",
        "- Local schema validation: PASS",
        f"- Leakage audit: {leakage['status']} ({leakage['finding_count']} findings)",
        "- Held-out accessed: false",
        "- Definitive diagnosis or performance metric calculated: false",
        "",
        "## Attempts",
        "",
        "| Agent | Attempts | Structural retries |",
        "|---|---:|---:|",
    ]
    lines.extend(
        f"| {agent_id} | {values[0]} | {values[1]} |"
        for agent_id, values in attempts.items()
    )
    lines.extend(
        [
            "",
            "## Deterministic B/E libraries",
            "",
            "| Agent | B count | E count | Zero fixed point | Strong normalized invariance | Character equivalence |",
            "|---|---:|---:|---|---|---|",
        ]
    )
    lines.extend(
        f"| {agent_id} | {values['B_count']} | {values['E_count']} | PASS | PASS | PASS |"
        for agent_id, values in audit.items()
    )
    lines.extend(
        [
            "",
            "Provenance and required hashes are complete. Raw provider responses and",
            "every structural attempt are retained in `generation_runs.json`. This",
            "report intentionally contains no observed pattern, insight text, predicted",
            "label, qualitative assessment, or diagnostic interpretation.",
            "",
            f"Hash groups recorded: {len(hashes['sha256'])}.",
        ]
    )
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    if FINAL_LIBRARY_PATH.exists() or RUNS_PATH.exists():
        raise RuntimeError(
            "final insight artifacts already exist; refusing regeneration or overwrite"
        )
    bundles, input_hashes = prepare_input_bundles()
    insights, journal, prompt_hashes = generate(bundles, input_hashes)
    protocol = load_protocol_config()
    validated = validate_global_insights(insights, protocol)
    if len(validated) != 8:
        raise RuntimeError("final global insight library does not contain eight insights")
    write_json(FINAL_LIBRARY_PATH, [item.to_dict() for item in validated])
    audit, peer_hashes = build_peer_libraries(validated, protocol)
    leakage = leakage_audit(journal)
    hashes = build_hash_manifest(journal, input_hashes, prompt_hashes, peer_hashes)
    write_json(HASHES_PATH, hashes)
    journal["leakage_audit"] = leakage
    journal["B_E_audit"] = audit
    journal["hash_manifest"] = str(HASHES_PATH.relative_to(ROOT))
    write_partial_runs(journal)
    write_report(journal, audit, leakage, hashes)
    print(
        json.dumps(
            {
                "generation_completed": 4,
                "final_insight_count": 8,
                "attempts": {
                    item["source_agent"]: item["attempt_count"]
                    for item in journal["generations"]
                },
                "retries": {
                    item["source_agent"]: item["retry_count"]
                    for item in journal["generations"]
                },
                "schema": "PASS",
                "leakage": "PASS",
                "B_E_audit": "PASS",
                "hashes": "COMPLETE",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
