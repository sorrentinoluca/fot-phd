#!/usr/bin/env python3
"""Reproducible communication-payload characterization from frozen FoT-TEP artifacts.

The script is deliberately standard-library only.  It reads the current frozen
Experiment 1 / Condition C / EXP2 artifacts and the tagged EXP3_V2 Git objects,
runs internal consistency tests, and writes CSV, JSON, and Markdown outputs next
to this file.  It never calls an LLM and never writes into a frozen artifact tree.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import csv
import hashlib
import io
import json
import math
from pathlib import Path
import re
import statistics
import subprocess
import sys
import tarfile
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = Path(__file__).resolve().parent
CSV_PATH = OUT_DIR / "communication_payload_metrics.csv"
JSON_PATH = OUT_DIR / "communication_payload_summary.json"
REPORT_PATH = OUT_DIR / "COMMUNICATION_PAYLOAD_CHARACTERIZATION.md"

EXP3_INFERENCE_REF = "exp3-v2-inference-frozen-001"
EXP3_RESULTS_REF = "exp3-v2-results-frozen-001"
EXP3_VERBALIZATION_REF = "5be0c3c14e7e1601708486d56c2cb4cee29658ab"

AGENTS = ("agent_1", "agent_2", "agent_3", "agent_4")
AGENT_PACK = {
    "agent_1": "LKP-001",
    "agent_2": "LKP-002",
    "agent_3": "LKP-003",
    "agent_4": "LKP-004",
}
AGENT_FAULT = {
    "agent_1": "F1",
    "agent_2": "F8",
    "agent_3": "F10",
    "agent_4": "F13",
}

WORD_RE = re.compile(r"\b[^\W_]+(?:[’'-][^\W_]+)*\b", re.UNICODE)

MAIN_SOURCES = [
    "docs/fot_walkthrough_conversazione.md",
    "docs/fot_walkthrough.html",
    "docs/paper/FOT_TEP_EXPERIMENT_PLAN_BIGDATA2026.md",
    "docs/lit_review/FOT_TEP_GAP_ANALYSIS_AND_RELATED_WORK.md",
    "docs/lit_review/FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md",
]


def read_text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def read_json(path: str) -> Any:
    return json.loads(read_text(path))


def read_jsonl(path: str) -> list[dict[str, Any]]:
    return [json.loads(line) for line in read_text(path).splitlines() if line.strip()]


def git_output(*args: str, binary: bool = False) -> bytes | str:
    return subprocess.check_output(
        ["git", *args], cwd=ROOT, text=not binary
    )


def git_read(ref: str, path: str) -> str:
    return str(git_output("show", f"{ref}:{path}"))


def git_json(ref: str, path: str) -> Any:
    return json.loads(git_read(ref, path))


def git_jsonl(ref: str, path: str) -> list[dict[str, Any]]:
    return [json.loads(line) for line in git_read(ref, path).splitlines() if line.strip()]


def git_json_directory(ref: str, path: str) -> list[dict[str, Any]]:
    """Read all JSON files below a tagged Git tree without checking them out."""
    archive = git_output("archive", ref, path, binary=True)
    assert isinstance(archive, bytes)
    with tarfile.open(fileobj=io.BytesIO(archive)) as bundle:
        members = sorted(
            (member for member in bundle.getmembers() if member.name.endswith(".json")),
            key=lambda member: member.name,
        )
        return [json.load(bundle.extractfile(member)) for member in members]  # type: ignore[arg-type]


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def file_sha256(path: str) -> str:
    return sha256_bytes((ROOT / path).read_bytes())


def measure_text(value: str) -> dict[str, Any]:
    return {
        "characters": len(value),
        "utf8_bytes": len(value.encode("utf-8")),
        "words_unicode_regex": len(WORD_RE.findall(value)),
        "lines": len(value.splitlines()) if value else 0,
        "sha256": sha256_text(value),
    }


def render_insight_block(insights: list[dict[str, Any]]) -> str:
    if not insights:
        return ""
    return "PEER INSIGHTS\n" + json.dumps(
        insights, ensure_ascii=False, indent=2
    ) + "\n\n"


def stats(values: Iterable[float | int]) -> dict[str, float | int | None]:
    data = list(values)
    if not data:
        return {"n": 0, "mean": None, "median": None, "min": None, "max": None, "pstdev": None}
    return {
        "n": len(data),
        "mean": statistics.fmean(data),
        "median": statistics.median(data),
        "min": min(data),
        "max": max(data),
        "pstdev": statistics.pstdev(data),
    }


def verify_hash_manifest(manifest_path: str, artifact_key: str) -> list[str]:
    manifest = read_json(manifest_path)
    checked: list[str] = []
    for path, expected in manifest[artifact_key].items():
        if file_sha256(path) != expected:
            raise RuntimeError(f"frozen hash mismatch: {path}")
        checked.append(path)
    return checked


def first_attempt_input_tokens(record: dict[str, Any]) -> int:
    attempt = record["provider_attempts"][0]
    response = attempt.get("response", attempt)
    value = response.get("input_tokens", response.get("prompt_tokens"))
    if not isinstance(value, int):
        raise RuntimeError("missing first-attempt input token count")
    return value


def record_input_tokens(record: dict[str, Any]) -> int:
    value = record.get("input_tokens", record.get("prompt_tokens"))
    if not isinstance(value, int):
        raise RuntimeError("missing cumulative input token count")
    return value


def record_output_tokens(record: dict[str, Any]) -> int:
    value = record.get("output_tokens", record.get("completion_tokens"))
    if not isinstance(value, int):
        raise RuntimeError("missing cumulative output token count")
    return value


def attempt_reasoning_tokens(attempt: dict[str, Any]) -> int | None:
    response = attempt.get("response", attempt)
    usage = response.get("usage_raw") or (response.get("response_raw") or {}).get("usage") or {}
    details = usage.get("output_tokens_details") or usage.get("completion_tokens_details") or {}
    value = details.get("reasoning_tokens")
    return value if isinstance(value, int) else None


def attempt_latency_seconds(attempt: dict[str, Any]) -> float | None:
    response = attempt.get("response", attempt)
    raw = response.get("response_raw") or {}
    created = raw.get("created_at")
    completed = raw.get("completed_at")
    if isinstance(created, (int, float)) and isinstance(completed, (int, float)):
        return float(completed - created)
    return None


def paired_token_deltas(records: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    keyed = {
        (r["physical_case_id"], r["agent_id"], r["repetition"], r["condition"]): r
        for r in records
    }
    result: dict[str, dict[str, int]] = {"B": {}, "E": {}}
    for condition in ("B", "E"):
        for agent in AGENTS:
            deltas: list[int] = []
            for key, record in keyed.items():
                if key[1] != agent or key[3] != condition:
                    continue
                baseline = keyed[key[:3] + ("A",)]
                deltas.append(first_attempt_input_tokens(record) - first_attempt_input_tokens(baseline))
            counts = Counter(deltas)
            if len(counts) != 1:
                raise RuntimeError(f"non-constant {condition}-A token delta for {agent}: {counts}")
            result[condition][agent] = next(iter(counts))
    return result


def fault_from_case(case_id: str, exp1_mapping: dict[str, str]) -> str:
    if case_id in exp1_mapping:
        return exp1_mapping[case_id]
    match = re.match(r"EXP3V2-(N|F1|F8|F10|F13)-", case_id)
    if match:
        return "Normal" if match.group(1) == "N" else match.group(1)
    return "unknown"


def summarize_usage(
    records: list[dict[str, Any]],
    exp1_mapping: dict[str, str],
) -> dict[str, Any]:
    def summarize_group(rows: list[dict[str, Any]]) -> dict[str, Any]:
        attempts = [attempt for row in rows for attempt in row["provider_attempts"]]
        reasoning = [value for attempt in attempts if (value := attempt_reasoning_tokens(attempt)) is not None]
        latencies = [value for attempt in attempts if (value := attempt_latency_seconds(attempt)) is not None]
        full_input = sum(record_input_tokens(row) for row in rows)
        first_input = sum(first_attempt_input_tokens(row) for row in rows)
        output = sum(record_output_tokens(row) for row in rows)
        return {
            "logical_calls": len(rows),
            "provider_calls": len(attempts),
            "input_tokens_all_attempts": full_input,
            "input_tokens_first_attempts": first_input,
            "retry_input_token_surcharge": full_input - first_input,
            "output_tokens_all_attempts": output,
            "reasoning_tokens_all_attempts": sum(reasoning) if len(reasoning) == len(attempts) else None,
            "reasoning_token_observations": len(reasoning),
            "latency_seconds": {
                "status": "measured_from_provider_created_at_and_completed_at"
                if latencies else "not_recorded",
                "n": len(latencies),
                "sum": sum(latencies) if latencies else None,
                "mean": statistics.fmean(latencies) if latencies else None,
                "median": statistics.median(latencies) if latencies else None,
                "min": min(latencies) if latencies else None,
                "max": max(latencies) if latencies else None,
            },
        }

    by_condition: dict[str, Any] = {}
    by_agent: dict[str, Any] = {}
    by_fault: dict[str, Any] = {}
    for condition in sorted({row["condition"] for row in records}):
        subset = [row for row in records if row["condition"] == condition]
        by_condition[condition] = summarize_group(subset)
        by_agent[condition] = {
            agent: summarize_group([row for row in subset if row["agent_id"] == agent])
            for agent in sorted({row["agent_id"] for row in subset})
        }
        faults = sorted({fault_from_case(row["physical_case_id"], exp1_mapping) for row in subset})
        by_fault[condition] = {
            fault: summarize_group(
                [row for row in subset if fault_from_case(row["physical_case_id"], exp1_mapping) == fault]
            )
            for fault in faults
        }
    return {"by_condition": by_condition, "by_agent": by_agent, "by_fault": by_fault}


def summarize_condition_c_usage(records: list[dict[str, Any]]) -> dict[str, Any]:
    attempts = [attempt for row in records for attempt in row["raw_attempts"]]
    prompt = [attempt["token_usage"]["prompt_tokens"] for attempt in attempts]
    completion = [attempt["token_usage"]["completion_tokens"] for attempt in attempts]
    return {
        "logical_calls": len(records),
        "provider_calls": len(attempts),
        "input_tokens_all_attempts": sum(prompt),
        "input_tokens_first_attempts": sum(row["raw_attempts"][0]["token_usage"]["prompt_tokens"] for row in records),
        "retry_input_token_surcharge": sum(prompt) - sum(
            row["raw_attempts"][0]["token_usage"]["prompt_tokens"] for row in records
        ),
        "output_tokens_all_attempts": sum(completion),
        "reasoning_tokens_all_attempts": None,
        "reasoning_token_observations": 0,
        "latency_seconds": {"status": "not_recorded", "n": 0, "sum": None, "mean": None, "median": None, "min": None, "max": None},
    }


def render_abe_prompt(
    *, agent: str, condition: str, case_text: str,
    config: dict[str, Any], local: dict[str, Any],
    libraries: dict[str, dict[str, list[dict[str, Any]]]],
) -> str:
    template = read_text({"A": "phase_b/prompts/isolated_A.txt", "B": "phase_b/prompts/fot_B.txt", "E": "phase_b/prompts/corrupted_E.txt"}[condition])
    insights = [] if condition == "A" else libraries[condition][agent]
    return (
        template.replace("<<LABEL_SPACE>>", json.dumps(config["label_space"], ensure_ascii=False))
        .replace("<<LOCAL_EXAMPLES>>", json.dumps(local["packs"][AGENT_PACK[agent]], ensure_ascii=False, indent=2))
        .replace("<<PEER_INSIGHTS_BLOCK>>", render_insight_block(insights))
        .replace("<<CASE_TEXT>>", case_text.strip())
    )


def render_c_prompt(case_text: str, examples: list[dict[str, Any]], insights: list[dict[str, Any]]) -> str:
    template = read_text("icl/prompts/pooled_C.txt")
    labels = ["CLS-ZOGAA", "CLS-OJNSG", "CLS-R463B", "CLS-Z3ISU", "Normal"]
    return (
        template.replace("<<LABEL_SPACE>>", json.dumps(labels, ensure_ascii=False))
        .replace("<<LOCAL_EXAMPLES>>", json.dumps(examples, ensure_ascii=False, indent=2))
        .replace("<<PEER_INSIGHTS_BLOCK>>", render_insight_block(insights))
        .replace("<<CASE_TEXT>>", case_text.strip())
    )


def prompt_metrics_abe(
    records: list[dict[str, Any]], case_texts: dict[str, str],
    config: dict[str, Any], local: dict[str, Any],
    libraries: dict[str, dict[str, list[dict[str, Any]]]],
) -> dict[str, Any]:
    cache: dict[tuple[str, str, str], str] = {}
    by_condition: dict[str, list[dict[str, int]]] = defaultdict(list)
    hashes: dict[str, set[str]] = defaultdict(set)
    for record in records:
        key = (record["physical_case_id"], record["agent_id"], record["condition"])
        if key not in cache:
            cache[key] = render_abe_prompt(
                agent=key[1], condition=key[2], case_text=case_texts[key[0]],
                config=config, local=local, libraries=libraries,
            )
        prompt = cache[key]
        if sha256_text(prompt) != record["prompt_hash"]:
            raise RuntimeError(f"prompt hash reconstruction mismatch: {key}")
        if len(prompt) != record["prompt_character_count"]:
            raise RuntimeError(f"prompt character count mismatch: {key}")
        by_condition[key[2]].append(measure_text(prompt))
        hashes[key[2]].add(record["prompt_hash"])
    return {
        condition: {
            "logical_calls": len(rows),
            "unique_prompts": len(hashes[condition]),
            "total_characters": sum(row["characters"] for row in rows),
            "total_utf8_bytes": sum(row["utf8_bytes"] for row in rows),
            "mean_characters": statistics.fmean(row["characters"] for row in rows),
            "mean_utf8_bytes": statistics.fmean(row["utf8_bytes"] for row in rows),
            "source": "deterministic reconstruction verified against every frozen prompt hash",
        }
        for condition, rows in sorted(by_condition.items())
    }


def prompt_metrics_c(
    records: list[dict[str, Any]], case_texts: dict[str, str],
    examples: list[dict[str, Any]], insights: list[dict[str, Any]],
) -> dict[str, Any]:
    cache: dict[str, str] = {}
    rows: list[dict[str, Any]] = []
    for record in records:
        case_id = record["physical_case_id"]
        cache.setdefault(case_id, render_c_prompt(case_texts[case_id], examples, insights))
        prompt = cache[case_id]
        if sha256_text(prompt) != record["prompt_sha256"]:
            raise RuntimeError(f"Condition C prompt hash reconstruction mismatch: {case_id}")
        rows.append(measure_text(prompt))
    return {
        "logical_calls": len(rows),
        "unique_prompts": len(cache),
        "total_characters": sum(row["characters"] for row in rows),
        "total_utf8_bytes": sum(row["utf8_bytes"] for row in rows),
        "mean_characters": statistics.fmean(row["characters"] for row in rows),
        "mean_utf8_bytes": statistics.fmean(row["utf8_bytes"] for row in rows),
        "source": "deterministic reconstruction verified against every frozen prompt hash",
    }


def exp1_case_fault_mapping() -> dict[str, str]:
    mapping = read_json("phase_b/final_evaluation/evaluator_side/heldout_source_mapping.json")
    result: dict[str, str] = {}
    for item in mapping["cases"]:
        name = item["source_filename"]
        if "normal" in name:
            result[item["physical_case_id"]] = "Normal"
        else:
            match = re.match(r"mode1_(\d+)_", name)
            if not match:
                raise RuntimeError(f"cannot derive fault from {name}")
            result[item["physical_case_id"]] = "F" + match.group(1)
    return result


def load_exp1_case_texts() -> dict[str, str]:
    manifest = read_json("phase_b/final_evaluation/heldout_verbalizations_manifest.json")
    return {item["physical_case_id"]: read_text(item["neutral_text_path"]) for item in manifest["cases"]}


def load_exp3_case_texts(records: list[dict[str, Any]]) -> dict[str, str]:
    case_ids = sorted({record["physical_case_id"] for record in records})
    return {
        case_id: git_read(EXP3_VERBALIZATION_REF, f"verbalization_outputs/neutral_text/{case_id}.txt")
        for case_id in case_ids
    }


def insight_metrics(insights: list[dict[str, Any]], gpt_rate: float, qwen_rate: float) -> dict[str, Any]:
    rows = []
    for insight in insights:
        serialized = json.dumps(insight, ensure_ascii=False, indent=2)
        measured = measure_text(serialized)
        measured.update({
            "insight_id": insight["insight_id"],
            "source_agent": insight["source_agent"],
            "pseudolabel": insight["pseudolabel"],
            "gpt56_terra_tokens_estimated": round(measured["utf8_bytes"] * gpt_rate),
            "qwen38_27b_tokens_estimated": round(measured["utf8_bytes"] * qwen_rate),
            "token_estimate_method": "receiver-block empirical token/UTF-8-byte rate; not standalone tokenizer output",
        })
        rows.append(measured)

    fields = ("characters", "utf8_bytes", "words_unicode_regex", "lines", "gpt56_terra_tokens_estimated", "qwen38_27b_tokens_estimated")
    return {
        "definition": "each complete insight JSON object serialized with ensure_ascii=False, indent=2, without array/header framing",
        "records": rows,
        "overall_stats": {field: stats(row[field] for row in rows) for field in fields},
        "by_source_agent": {
            agent: {
                "count": sum(row["source_agent"] == agent for row in rows),
                **{field: stats(row[field] for row in rows if row["source_agent"] == agent) for field in fields},
            }
            for agent in AGENTS
        },
    }


def producer_metrics(generation_runs: dict[str, Any]) -> dict[str, Any]:
    by_agent: dict[str, Any] = {}
    for generation in generation_runs["generations"]:
        attempts = generation["attempts"]
        input_tokens = output_tokens = reasoning_tokens = 0
        latency: list[float] = []
        for attempt in attempts:
            response = attempt["provider_response"]
            input_tokens += response["input_tokens"]
            output_tokens += response["output_tokens"]
            reasoning_tokens += (response.get("usage_raw", {}).get("output_tokens_details") or {}).get("reasoning_tokens", 0)
            raw = response.get("response_raw") or {}
            if isinstance(raw.get("created_at"), (int, float)) and isinstance(raw.get("completed_at"), (int, float)):
                latency.append(float(raw["completed_at"] - raw["created_at"]))
        by_agent[generation["source_agent"]] = {
            "fault": AGENT_FAULT[generation["source_agent"]],
            "calls": len(attempts),
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "reasoning_tokens": reasoning_tokens,
            "latency_seconds_sum": sum(latency) if latency else None,
            "latency_observations": len(latency),
            "insights_produced": len(generation["expected_insight_ids"]),
            "source": "phase_b/insights/generation_runs.json",
        }
    return {
        "one_time_frozen_production": True,
        "calls": sum(row["calls"] for row in by_agent.values()),
        "input_tokens": sum(row["input_tokens"] for row in by_agent.values()),
        "output_tokens": sum(row["output_tokens"] for row in by_agent.values()),
        "reasoning_tokens": sum(row["reasoning_tokens"] for row in by_agent.values()),
        "latency_seconds_sum": sum(row["latency_seconds_sum"] or 0 for row in by_agent.values()),
        "latency_observations": sum(row["latency_observations"] for row in by_agent.values()),
        "by_agent_and_fault": by_agent,
        "monetary_cost": None,
        "monetary_cost_status": "not_available: no applicable price snapshot or charged amount is frozen in the repository",
    }


def accuracy_data() -> dict[str, Any]:
    exp1 = read_json("phase_b/final_evaluation/evaluation_results.json")["condition_metrics"]
    qwen = read_json("phase_b/exp2/qwen/evaluation/evaluation_results.json")["condition_metrics"]
    exp3 = git_json(EXP3_RESULTS_REF, "evaluation_outputs/exp3v2_confirmatory_results.json")["condition_metrics"]
    c = read_json("icl/full_evaluation/evaluation_results_c.json")
    return {
        "experiment_1": {condition: exp1[condition]["unseen"] for condition in "ABE"},
        "exp3_v2": {condition: exp3[condition]["unseen"] for condition in "ABE"},
        "experiment_2_qwen": {condition: qwen[condition]["unseen"] for condition in "ABE"},
        "condition_c": {
            "overall": c["condition_c_metrics"]["overall"],
            "fault": c["condition_c_metrics"]["accuracy_C_fault"],
            "delta_c_minus_b": c["delta_c_minus_b"],
            "comparability": "post-hoc descriptive; centralized context differs in amount and form",
        },
    }


def per_agent_unseen_accuracy(
    aggregate_records: list[dict[str, Any]],
    case_fault: dict[str, str],
    real_to_opaque: dict[str, str],
) -> dict[str, dict[str, dict[str, Any]]]:
    result: dict[str, dict[str, dict[str, Any]]] = {}
    for condition in "ABE":
        result[condition] = {}
        for agent in AGENTS:
            rows = [
                row for row in aggregate_records
                if row["condition"] == condition
                and row["agent_id"] == agent
                and fault_from_case(row["physical_case_id"], case_fault) not in {"Normal", AGENT_FAULT[agent]}
            ]
            correct = 0
            for row in rows:
                fault = fault_from_case(row["physical_case_id"], case_fault)
                expected = real_to_opaque[fault]
                parsed = row["parsed_output"]
                correct += int(not parsed.get("abstain", False) and parsed.get("predicted_label") == expected)
            result[condition][agent] = {
                "n": len(rows), "correct": correct,
                "accuracy": correct / len(rows) if rows else None,
            }
    return result


def transfer_metrics(
    *, condition: str, logical_calls: int, calls_per_agent: int,
    block_metrics: dict[str, dict[str, Any]], token_deltas: dict[str, dict[str, int]],
    model_key: str,
) -> dict[str, Any]:
    if condition == "A":
        return {
            "knowledge_rounds": 0, "unique_directed_source_consumer_edges": 0,
            "prompt_block_transfers": 0, "repeated_source_consumer_transfers": 0,
            "insight_record_deliveries": 0, "total_utf8_bytes": 0,
            "total_payload_tokens_in_context": 0,
        }
    return {
        "knowledge_rounds": 1,
        "unique_directed_source_consumer_edges": 12,
        "prompt_block_transfers": logical_calls,
        "repeated_source_consumer_transfers": logical_calls * 3,
        "insight_record_deliveries": logical_calls * 6,
        "total_utf8_bytes": sum(block_metrics[agent]["utf8_bytes"] * calls_per_agent for agent in AGENTS),
        "total_payload_tokens_in_context": sum(token_deltas[condition][agent] * calls_per_agent for agent in AGENTS),
        "token_measurement_model": model_key,
        "token_measurement_status": "exact provider-recorded paired first-attempt prompt delta",
    }


def efficiency_metrics(
    experiment: str, accuracy: dict[str, Any], transfers: dict[str, Any],
    block_metrics: dict[str, dict[str, Any]], token_delta: dict[str, int],
    calls_per_agent_unseen: int, repetitions: int,
) -> dict[str, Any]:
    b = accuracy["B"]
    a = accuracy["A"]
    e = accuracy["E"]
    unseen_bytes = sum(block_metrics[agent]["utf8_bytes"] * calls_per_agent_unseen for agent in AGENTS)
    unseen_tokens = sum(token_delta[agent] * calls_per_agent_unseen for agent in AGENTS)
    gained = b["correct"] - a["correct"]
    delta_ba = b["accuracy"] - a["accuracy"]
    delta_be = b["accuracy"] - e["accuracy"]
    mean_extra_per_call = statistics.fmean(token_delta.values())
    return {
        "experiment": experiment,
        "scope": "locally-unseen aggregate agent-case predictions; R repeated LLM calls retained separately",
        "physical_fault_cases": 12 if experiment != "exp3_v2" else 24,
        "unseen_aggregate_predictions": b["n"],
        "llm_repetitions_per_prediction": repetitions,
        "B_correct_unseen": b["correct"],
        "B_minus_A_accuracy": delta_ba,
        "B_minus_E_accuracy": delta_be,
        "B_minus_A_percentage_points": 100 * delta_ba,
        "unseen_only_payload_utf8_bytes": unseen_bytes,
        "unseen_only_payload_tokens_in_context": unseen_tokens,
        "bytes_per_B_correct_unseen_prediction": unseen_bytes / b["correct"] if b["correct"] else None,
        "tokens_per_B_correct_unseen_prediction": unseen_tokens / b["correct"] if b["correct"] else None,
        "tokens_per_additional_correct_unseen_vs_A": unseen_tokens / gained if gained else None,
        "mean_B_minus_A_tokens_per_llm_call": mean_extra_per_call,
        "mean_B_minus_A_tokens_per_aggregate_prediction_R_calls": mean_extra_per_call * repetitions,
        "tokens_per_percentage_point_accuracy": (mean_extra_per_call * repetitions) / (100 * delta_ba) if delta_ba else None,
        "tokens_per_percentage_point_formula": "mean paired B-A input-token delta per LLM call × R / (100 × unseen accuracy delta)",
        "all_B_calls_payload_utf8_bytes": transfers["total_utf8_bytes"],
        "all_B_calls_payload_tokens_in_context": transfers["total_payload_tokens_in_context"],
    }


def build_csv_rows(
    experiments: dict[str, Any],
    libraries: dict[str, dict[str, list[dict[str, Any]]]],
    block_texts: dict[str, dict[str, str]],
    tokenizers: dict[str, Any],
    accuracy: dict[str, Any],
    c_context: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for experiment, meta in experiments.items():
        if experiment == "condition_c":
            m = c_context["metrics"]
            rows.append({
                "experiment": "experiment_1_condition_c", "condition": "C", "consumer_model": "gpt-5.6-terra",
                "consumer_agent": "central", "payload_kind": "pooled_examples_plus_all_insights_two_inserted_blocks",
                "source_agents": ";".join(AGENTS), "insight_ids": ";".join(f"INS-{i:03d}" for i in range(1, 9)),
                "insight_count": 8, "payload_characters": m["characters"], "payload_utf8_bytes": m["utf8_bytes"],
                "payload_words": m["words_unicode_regex"], "payload_lines": m["lines"],
                "gpt56_terra_tokens": c_context["gpt_estimated_tokens"], "gpt56_terra_token_status": "estimated",
                "qwen38_27b_tokens": c_context["qwen_estimated_tokens"], "qwen38_27b_token_status": "estimated_not_executed_for_C",
                "logical_prompt_calls": meta["usage"]["logical_calls"], "provider_calls": meta["usage"]["provider_calls"],
                "prompt_block_transfers": meta["usage"]["logical_calls"], "total_payload_utf8_bytes": m["utf8_bytes"] * meta["usage"]["logical_calls"],
                "total_payload_tokens_for_executed_model": None, "consumer_input_tokens": meta["usage"]["input_tokens_all_attempts"],
                "consumer_output_tokens": meta["usage"]["output_tokens_all_attempts"], "consumer_reasoning_tokens": None,
                "accuracy_scope": "all centralized aggregate physical cases", "accuracy_n": accuracy["condition_c"]["overall"]["n"],
                "accuracy_correct": accuracy["condition_c"]["overall"]["correct"], "accuracy": accuracy["condition_c"]["overall"]["accuracy"],
                "source_refs": ";".join(meta["source_refs"] + c_context["source_refs"]),
            })
            continue

        consumer_model = meta["consumer_model"]
        model_deltas = tokenizers[meta["tokenizer_key"]]["in_context_delta"]
        for condition in "ABE":
            usage = meta["usage"]["by_condition"][condition]
            calls_per_agent = usage["logical_calls"] // 4
            for agent in AGENTS:
                text = "" if condition == "A" else block_texts[condition][agent]
                m = measure_text(text)
                gpt_tokens = 0 if condition == "A" else tokenizers["gpt56_terra"]["in_context_delta"][condition][agent]
                qwen_tokens = 0 if condition == "A" else tokenizers["qwen38_27b"]["in_context_delta"][condition][agent]
                executed_tokens = 0 if condition == "A" else model_deltas[condition][agent]
                library = [] if condition == "A" else libraries[condition][agent]
                acc = meta["per_agent_unseen_accuracy"][condition][agent]
                payload_sources = (
                    ["phase_b/conditions/builders.py", f"phase_b/prompts/{'isolated_A' if condition == 'A' else ('fot_B' if condition == 'B' else 'corrupted_E')}.txt"]
                    if condition == "A"
                    else ["phase_b/conditions/builders.py", f"phase_b/insights/peer_libraries/{agent}_{condition}.json"]
                )
                rows.append({
                    "experiment": experiment, "condition": condition, "consumer_model": consumer_model,
                    "consumer_agent": agent, "payload_kind": "none" if condition == "A" else "peer_insight_block",
                    "source_agents": "" if condition == "A" else ";".join(sorted({item["source_agent"] for item in library})),
                    "insight_ids": "" if condition == "A" else ";".join(item["insight_id"] for item in library),
                    "insight_count": len(library), "payload_characters": m["characters"], "payload_utf8_bytes": m["utf8_bytes"],
                    "payload_words": m["words_unicode_regex"], "payload_lines": m["lines"],
                    "gpt56_terra_tokens": gpt_tokens, "gpt56_terra_token_status": "exact_in_context_delta",
                    "qwen38_27b_tokens": qwen_tokens, "qwen38_27b_token_status": "exact_in_context_delta",
                    "logical_prompt_calls": calls_per_agent, "provider_calls": meta["usage"]["by_agent"][condition][agent]["provider_calls"],
                    "prompt_block_transfers": 0 if condition == "A" else calls_per_agent,
                    "total_payload_utf8_bytes": m["utf8_bytes"] * calls_per_agent,
                    "total_payload_tokens_for_executed_model": executed_tokens * calls_per_agent,
                    "consumer_input_tokens": meta["usage"]["by_agent"][condition][agent]["input_tokens_all_attempts"],
                    "consumer_output_tokens": meta["usage"]["by_agent"][condition][agent]["output_tokens_all_attempts"],
                    "consumer_reasoning_tokens": meta["usage"]["by_agent"][condition][agent]["reasoning_tokens_all_attempts"],
                    "accuracy_scope": "locally-unseen aggregate agent-case", "accuracy_n": acc["n"],
                    "accuracy_correct": acc["correct"], "accuracy": acc["accuracy"],
                    "source_refs": ";".join(meta["source_refs"] + payload_sources),
                })
    return rows


def write_csv(rows: list[dict[str, Any]]) -> None:
    columns = [
        "experiment", "condition", "consumer_model", "consumer_agent", "payload_kind", "source_agents", "insight_ids",
        "insight_count", "payload_characters", "payload_utf8_bytes", "payload_words", "payload_lines",
        "gpt56_terra_tokens", "gpt56_terra_token_status", "qwen38_27b_tokens", "qwen38_27b_token_status",
        "logical_prompt_calls", "provider_calls", "prompt_block_transfers", "total_payload_utf8_bytes",
        "total_payload_tokens_for_executed_model", "consumer_input_tokens", "consumer_output_tokens",
        "consumer_reasoning_tokens", "accuracy_scope", "accuracy_n", "accuracy_correct", "accuracy", "source_refs",
    ]
    with CSV_PATH.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def fmt(value: Any, digits: int = 3) -> str:
    if value is None:
        return "non disponibile"
    if isinstance(value, float):
        return f"{value:.{digits}f}"
    return str(value)


def markdown_table(headers: list[str], rows: list[list[Any]]) -> str:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines.extend("| " + " | ".join(str(cell) for cell in row) + " |" for row in rows)
    return "\n".join(lines)


def build_report(summary: dict[str, Any]) -> str:
    p = summary["payload"]
    tok = summary["tokenization"]
    acc = summary["accuracy"]
    eff = summary["efficiency"]
    exps = summary["experiments"]
    producer = summary["producer_cost"]
    control = summary["b_e_structural_control"]

    receiver_rows = []
    for agent in AGENTS:
        bm = p["B_blocks"][agent]
        receiver_rows.append([
            agent, bm["insight_count"], bm["characters"], bm["utf8_bytes"], bm["words_unicode_regex"], bm["lines"],
            tok["gpt56_terra"]["in_context_delta"]["B"][agent],
            tok["qwen38_27b"]["in_context_delta"]["B"][agent],
        ])

    exp_rows = []
    for name in ("experiment_1", "exp3_v2", "experiment_2_qwen"):
        e = exps[name]
        for condition in "ABE":
            u = e["usage"]["by_condition"][condition]
            t = e["transfers"][condition]
            a = acc[e["accuracy_key"]][condition]
            exp_rows.append([
                name, condition, u["logical_calls"], u["provider_calls"], t["total_utf8_bytes"],
                t["total_payload_tokens_in_context"], u["input_tokens_all_attempts"], u["output_tokens_all_attempts"],
                fmt(u["reasoning_tokens_all_attempts"], 0), f"{a['correct']}/{a['n']}", fmt(a["accuracy"], 4),
            ])
    cu = exps["condition_c"]["usage"]
    exp_rows.append([
        "experiment_1_condition_c", "C", cu["logical_calls"], cu["provider_calls"],
        summary["condition_c_payload"]["metrics"]["utf8_bytes"] * cu["logical_calls"], "stima soltanto",
        cu["input_tokens_all_attempts"], cu["output_tokens_all_attempts"], "non disponibile",
        f"{acc['condition_c']['overall']['correct']}/{acc['condition_c']['overall']['n']}", fmt(acc["condition_c"]["overall"]["accuracy"], 4),
    ])

    eff_rows = []
    for name in ("experiment_1", "exp3_v2", "experiment_2_qwen"):
        row = eff[name]
        eff_rows.append([
            name, row["physical_fault_cases"], row["unseen_aggregate_predictions"], row["B_correct_unseen"],
            fmt(row["B_minus_A_accuracy"], 4), fmt(row["B_minus_E_accuracy"], 4),
            fmt(row["bytes_per_B_correct_unseen_prediction"], 2), fmt(row["tokens_per_B_correct_unseen_prediction"], 2),
            fmt(row["tokens_per_percentage_point_accuracy"], 2),
        ])

    insight_stats_rows = []
    for field, values in p["unique_insights"]["overall_stats"].items():
        insight_stats_rows.append([
            field, fmt(values["mean"], 2), fmt(values["median"], 2), values["min"], values["max"], fmt(values["pstdev"], 2),
        ])

    producer_rows = []
    for agent, row in producer["by_agent_and_fault"].items():
        producer_rows.append([
            agent, row["fault"], row["calls"], row["insights_produced"], row["input_tokens"], row["output_tokens"],
            row["reasoning_tokens"], fmt(row["latency_seconds_sum"], 1),
        ])

    be_rows = []
    for agent, row in control["by_receiver"].items():
        be_rows.append([
            agent, row["pseudolabel_substitutions"], row["differing_byte_positions"], row["B_utf8_bytes"], row["E_utf8_bytes"],
            tok["gpt56_terra"]["in_context_delta"]["B"][agent], tok["gpt56_terra"]["in_context_delta"]["E"][agent],
            tok["qwen38_27b"]["in_context_delta"]["B"][agent], tok["qwen38_27b"]["in_context_delta"]["E"][agent],
        ])

    prompt_ratio_rows = []
    for name in ("experiment_1", "exp3_v2", "experiment_2_qwen"):
        row = exps[name]["prompt_payload_ratio_B"]
        prompt_ratio_rows.append([name, fmt(row["utf8_byte_ratio"], 4), fmt(row["token_ratio"], 4)])
    c_ratio = exps["condition_c"]["prompt_payload_ratio_C"]
    prompt_ratio_rows.append(["experiment_1_condition_c", fmt(c_ratio["utf8_byte_ratio"], 4), "non disponibile (solo stima)"])

    federation_total_rows = []
    for name in ("experiment_1", "exp3_v2", "experiment_2_qwen"):
        row = exps[name]["federated_payload_total_B_plus_E"]
        federation_total_rows.append([
            name, row["knowledge_rounds"], row["prompt_block_transfers"],
            row["repeated_source_consumer_transfers"], row["insight_record_deliveries"],
            row["total_utf8_bytes"], row["total_payload_tokens_in_context"],
        ])

    prompt_inventory_rows = []
    for name in ("experiment_1", "exp3_v2", "experiment_2_qwen"):
        for condition in "ABE":
            row = exps[name]["prompt_metrics"][condition]
            prompt_inventory_rows.append([name, condition, row["unique_prompts"], row["logical_calls"], "hash SHA-256 verificati"])
    c_prompt = exps["condition_c"]["prompt_metrics"]["C"]
    prompt_inventory_rows.append(["experiment_1_condition_c", "C", c_prompt["unique_prompts"], c_prompt["logical_calls"], "hash SHA-256 verificati"])

    tokenizer_rows = [
        ["GPT-5.6-terra", "nome/versione tokenizer non frozen", "Responses API; openai 3.6.0; reasoning medium", p["all_receiver_unit_B"]["gpt_tokens"], "esatto in contesto"],
        ["Qwen3.8-27B-FP8", "server tokenizer della revisione 017b9c7…; file non frozen", "vLLM 0.28.0; SDK 3.8.0; temp 0; seed 20260829", p["all_receiver_unit_B"]["qwen_tokens"], "esatto in contesto"],
    ]

    agent_cost_rows = []
    fault_cost_rows = []
    latency_rows = []
    for name in ("experiment_1", "exp3_v2", "experiment_2_qwen"):
        for agent in AGENTS:
            row = exps[name]["usage"]["by_agent"]["B"][agent]
            agent_cost_rows.append([name, agent, row["provider_calls"], row["input_tokens_all_attempts"], row["output_tokens_all_attempts"], fmt(row["reasoning_tokens_all_attempts"], 0)])
        for fault, row in exps[name]["usage"]["by_fault"]["B"].items():
            fault_cost_rows.append([name, fault, row["logical_calls"], row["input_tokens_all_attempts"], row["output_tokens_all_attempts"], fmt(row["reasoning_tokens_all_attempts"], 0)])
        for condition in "ABE":
            row = exps[name]["usage"]["by_condition"][condition]["latency_seconds"]
            latency_rows.append([name, condition, row["n"], fmt(row["sum"], 1), fmt(row["mean"], 2), row["status"]])
    latency_rows.append(["experiment_1_condition_c", "C", 0, "non disponibile", "non disponibile", "not_recorded"])

    correct_mapping_rows = [[fault, label] for fault, label in summary["pseudolabel_mapping"]["real_to_opaque"].items()]
    derangement_rows = []
    for agent, mapping in summary["condition_e_derangements"].items():
        derangement_rows.append([agent, "; ".join(f"{old}→{new}" for old, new in mapping.items())])

    return f"""# Caratterizzazione del payload comunicativo FoT–TEP

Stato: **analisi derivata, riproducibile, senza nuove inferenze LLM**. I risultati sperimentali e gli artefatti frozen non sono stati modificati. “Costo” indica token e latenza registrati, non costo monetario; i prezzi applicabili non sono congelati nel repository.

## Metodologia

La misura primaria del payload federato è il blocco realmente inserito nel prompt: `PEER INSIGHTS\\n` + JSON UTF-8 indentato + due newline finali. Caratteri = code point Python; byte = UTF-8; parole = match Unicode dell’espressione `{WORD_RE.pattern}`; righe = `splitlines()`. La dimensione del singolo insight usa l’oggetto JSON completo (`ensure_ascii=False`, `indent=2`) senza framing di array/header; per questo la somma degli insight non coincide necessariamente con il blocco trasmesso.

I token A/B/E sono **misure esatte in contesto**: differenza tra `input_tokens`/`prompt_tokens` del primo tentativo di B (o E) e A per lo stesso caso fisico, agente e ripetizione. Il valore include gli effetti di tokenizzazione ai confini del blocco e non è una tokenizzazione standalone. Per GPT il nome/versione del tokenizer non è registrato; per Qwen sono congelati modello e revisione ma non i file del tokenizer. I token standalone per insight e per C sono quindi stime lineari esplicitamente etichettate, calibrate sul rapporto token-incrementali/byte dei quattro peer block frozen.

I prompt completi A/B/E e C sono stati ricostruiti deterministicamente dai template e dagli input frozen; ogni hash è stato verificato contro i prediction log. EXP3_V2 è letto direttamente dagli oggetti Git dei tag `{EXP3_INFERENCE_REF}` e `{EXP3_RESULTS_REF}`, senza checkout. Le unità sono mantenute separate: caso fisico, ripetizione LLM e predizione aggregata.

## Provenienza dei dati

- Insight e routing: `phase_b/insights/final_local_insights.json`, `phase_b/insights/peer_libraries/agent_*_B.json`, `agent_*_E.json`, `phase_b/conditions/builders.py`.
- Mapping: `phase_b/config/evaluator_side/pseudolabel_mapping.json` e `condition_e_derangements.json`.
- Experiment 1: `phase_b/final_evaluation/inference/*.json[l]` e `evaluation_results.json`.
- EXP3_V2: tag Git `{EXP3_INFERENCE_REF}` (`inference_outputs/records/*.json`), `{EXP3_RESULTS_REF}` (`evaluation_outputs/exp3v2_confirmatory_results.json`) e payload commit `{EXP3_VERBALIZATION_REF}` (`verbalization_outputs/neutral_text/*.txt`), registrato nel manifest di freeze. Gli artefatti non sono presenti nel working tree corrente ma restano frozen e indirizzabili negli oggetti Git.
- Experiment 2/Qwen: `phase_b/exp2/qwen/inference/*.json[l]`, `config.json` ed `evaluation/evaluation_results.json`.
- Condition C: `icl/pooled_libraries/*.json`, `icl/inference/c_records.jsonl`, `icl/full_evaluation/evaluation_results_c.json`.
- Inquadramento: {', '.join(f'`{x}`' for x in MAIN_SOURCES)}.

### Inventario operativo

| Oggetto | Artefatto primario | Stato |
|---|---|---|
| Insight per producer | `phase_b/insights/final_local_insights.json` e `generation_runs.json` | 8 record frozen, 2 per agente |
| Prompt finali A/B/E | template `phase_b/prompts/*.txt` + builder + case/local examples/peer library | non salvati come testo autonomo; ricostruiti esattamente e verificati contro i log |
| Prompt finali C | `icl/prompts/pooled_C.txt` + `icl/conditions/builder_c.py` + pooled libraries | ricostruiti esattamente e verificati contro i log |
| Prediction log/evaluator Experiment 1 | `phase_b/final_evaluation/inference/*.jsonl`, `evaluation_results.json` | frozen |
| Prediction log/evaluator EXP3_V2 | oggetti Git `inference_outputs/*`, `evaluation_outputs/*` ai ref frozen | frozen nei ref, separati dal working tree |
| Prediction log/evaluator EXP2 Qwen | `phase_b/exp2/qwen/inference/*.jsonl`, `evaluation/*.json` | frozen |
| Mapping corretto/derangiato | `pseudolabel_mapping.json`, `condition_e_derangements.json` | evaluator-side frozen |

{markdown_table(['esperimento','condizione','prompt unici','chiamate logiche','verifica'], prompt_inventory_rows)}

Mapping corretto:

{markdown_table(['fault','pseudolabel'], correct_mapping_rows)}

Derangement E:

{markdown_table(['receiver','rotazione frozen'], derangement_rows)}

## Payload prodotto e ricevuto

Sono presenti **8 insight unici**, 2 per ciascun producer. La libreria frozen completa occupa {p['unique_library_artifact']['characters']} caratteri e {p['unique_library_artifact']['utf8_bytes']} byte inclusa la newline terminale. Ogni consumer federato riceve 6 insight (due da ciascuno dei tre peer):

{markdown_table(['consumer','insight','caratteri','byte','parole','righe','token GPT esatti*','token Qwen esatti*'], receiver_rows)}

*Incremento in contesto B−A; non tokenizzazione standalone.*

Statistiche per insight serializzato:

{markdown_table(['metrica','media','mediana','min','max','dev. std. popolazione'], insight_stats_rows)}

Le due righe token sono **stime**, non misure del tokenizer del singolo insight.

### Tokenizzazione e configurazione

{markdown_table(['consumer','tokenizer','configurazione','token/unità 4 receiver','stato'], tokenizer_rows)}

La stima standalone usa rispettivamente {fmt(tok['gpt56_terra']['standalone_estimate_tokens_per_utf8_byte'], 6)} e {fmt(tok['qwen38_27b']['standalone_estimate_tokens_per_utf8_byte'], 6)} token/byte, calibrati sui peer block. Non è usata per i totali A/B/E.

## Costo producer, consumer e trasferimento

La produzione frozen è avvenuta una sola volta: {producer['calls']} chiamate, {producer['input_tokens']} input token, {producer['output_tokens']} output token, {producer['reasoning_tokens']} reasoning token e {fmt(producer['latency_seconds_sum'], 1)} s di latenza provider misurabile. Gli esperimenti successivi riusano gli stessi 8 insight; non si riaddebita la produzione.

{markdown_table(['producer','fault','chiamate','insight','input tok','output tok','reasoning tok','latenza s'], producer_rows)}

Il trasferimento non genera una chiamata separata: il relativo costo token è l’incremento nel prompt del consumer. Totali per esecuzione:

{markdown_table(['esperimento','cond.','chiamate logiche','chiamate provider','byte payload','token payload*','input tok','output tok','reasoning tok','corrette unseen','accuracy'], exp_rows)}

*Esatti in contesto per A/B/E; C non è isolabile esattamente.* Le chiamate provider possono superare quelle logiche in presenza di retry. I reasoning token sono un sottoinsieme degli output/completion token, non vanno sommati di nuovo. La latenza consumer è disponibile solo per i record GPT con `created_at` e `completed_at`; è `not_recorded` per Qwen e C. Il costo monetario è **non disponibile**.

Totale federato B+E per esperimento (A non aggiunge payload):

{markdown_table(['esperimento','round logici','blocchi trasferiti','source→consumer ripetuti','insight consegnati','byte','token in contesto'], federation_total_rows)}

Distribuzione della condizione B per consumer (token su tutti i tentativi):

{markdown_table(['esperimento','consumer','provider call','input tok','output tok','reasoning tok'], agent_cost_rows)}

Distribuzione della condizione B per fault reale del caso (include tutti i receiver e R=3; `Normal` resta separato):

{markdown_table(['esperimento','fault','chiamate logiche','input tok','output tok','reasoning tok'], fault_cost_rows)}

Latenza consumer disponibile:

{markdown_table(['esperimento','cond.','osservazioni','somma s','media s','stato'], latency_rows)}

## Controllo strutturale B vs E

B ed E hanno lo stesso numero di insight, stessi ID, fonti, ordine, chiavi JSON, observed pattern, caratteri, parole, righe e byte; hanno anche lo stesso conteggio token in contesto nei due consumer. **Non sono byte-identici**: E sostituisce esattamente il valore ASCII di `pseudolabel` in ciascuno dei 6 record secondo il derangement frozen. Tutte le etichette hanno 9 byte, quindi la lunghezza resta invariata.

{markdown_table(['consumer','sostituzioni','posizioni byte diverse','byte B','byte E','GPT B','GPT E','Qwen B','Qwen E'], be_rows)}

Nell’unità a quattro receiver le 24 sostituzioni cambiano {control['all_receiver_unit']['differing_byte_positions']} posizioni byte, senza inserimenti/cancellazioni. Il test strutturale complessivo è **{control['status']}**.

## Efficienza descrittiva

Le seguenti normalizzazioni usano soltanto le chiamate associate alla popolazione locally-unseen. Non dimostrano superiorità di communication efficiency rispetto a un’altra famiglia di metodi.

{markdown_table(['esperimento','casi fault fisici','pred. unseen aggregate','B corrette','B−A','B−E','byte/B corretta','token/B corretta','token per punto %'], eff_rows)}

“Token per punto %” = incremento medio B−A per chiamata × R=3 / incremento di accuracy espresso in punti percentuali. È normalizzato per predizione aggregata; i valori totali dipenderebbero linearmente dalla dimensione del campione.

Rapporto payload/prompt completo:

{markdown_table(['esperimento','rapporto byte','rapporto token'], prompt_ratio_rows)}

Per A il rapporto è zero. Per C il numeratore byte è la somma dei due blocchi inseriti (10 esempi pooled + 8 insight); il confronto con B non è isomorfo.

## Condizioni e unità sperimentali

- Experiment 1 e EXP2/Qwen: 15 casi fisici (12 fault + 3 Normal), 4 agenti, R=3; 60 predizioni aggregate per condizione, di cui 36 locally-unseen. Le 36 non sono 36 casi fisici indipendenti.
- EXP3_V2: 30 casi fisici (24 fault + 6 Normal), 4 agenti, R=3; 120 predizioni aggregate per condizione, di cui 72 locally-unseen.
- C: 15 casi fisici, un consumer centrale, R=3; 15 predizioni aggregate. C è post-hoc, solo su Experiment 1 e riceve 10 esempi più tutti gli 8 insight; C−B è descrittivo e non causale.
- Un payload federato statico corrisponde a un round logico, 12 archi diretti source→consumer, 4 blocchi receiver-specific, 24 consegne di insight. Operativamente il blocco viene reinserito a ogni chiamata: 180 trasferimenti di blocco per B in Experiment 1/Qwen e 360 in EXP3_V2; E replica gli stessi volumi.

## Paradigmi adiacenti

| Paradigma | Oggetto trasmesso | Unità naturale | Leggibilità | Dipendenza dal modello | Dati pubblici | Costo per round | Audit |
|---|---|---|---|---|---|---|---|
| FedMD / logit sharing | logit su esempi condivisi | scalari o byte | bassa | richiede spazio output compatibile, modelli eterogenei possibili | sì, nel FedMD canonico | `K × N_pub × C × b` uplink, più aggregazione/downlink; numeri non disponibili senza configurazione | medio: tensori e dataset sono ispezionabili ma non autoesplicativi |
| FedProto | prototipi medi per classe | scalari o byte | bassa–media | dipende dallo spazio embedding/proiezione | non necessariamente | `Σ_k C_k × d × b` uplink, più prototipi globali; numeri non disponibili | medio: vettori associati a classi, semantica indiretta |
| Adapter / LoRA federati | parametri trainabili dell’adapter | parametri o byte | bassa | alta: architettura, layer e rank devono essere compatibili | no in generale | `K × P_adapter × b` uplink per round più broadcast; `P_LoRA=Σ r(d_in+d_out)`; numeri non disponibili | medio-basso a livello semantico, alto a livello di provenienza binaria |
| FoT / insight testuali | record JSON in linguaggio naturale | caratteri, byte, token | alta per ispezione umana | consumer-dependent nella tokenizzazione e nell’uso semantico, non nei byte | no nel setup FoT–TEP | misurato qui come somma dei blocchi UTF-8/token per receiver e chiamata | alto per contenuto, ordine, mapping e hash; nessuna garanzia di correttezza o privacy |

Il confronto è concettuale: byte testuali, logit, prototipi e parametri non sono direttamente equivalenti. Non sono prodotti numeri FedMD/FedProto/LoRA perché mancano `K`, dimensioni, precisione, compressione e numero di round comparabili.

## Limiti

- Il tokenizer standalone di GPT-5.6-terra e i file tokenizer Qwen non sono frozen nel repository. I conteggi esatti riportati sono incrementi osservati in contesto; le stime per insight/C non devono essere citate come misure esatte.
- Le latenze GPT derivano da timestamp provider a risoluzione di un secondo e non includono necessariamente l’intero tempo end-to-end; Qwen e C non espongono una latenza utilizzabile.
- Nessun prezzo o addebito applicabile è congelato: non viene calcolato costo monetario.
- Il conteggio parole dipende dalla regola dichiarata; il conteggio byte dipende dalla serializzazione JSON frozen.
- B ed E hanno stessa lunghezza, non stessi byte. La parità di token è osservata per questi due modelli e questi prompt, non una proprietà universale delle stringhe derangiate.
- C cambia insieme esempi, insight, struttura del receiver e quantità di contesto; non è un comparatore causalmente isomorfo.
- Le metriche per predizione corretta sono descrittive e sample-size-dependent; non provano privacy, compressione lossless, efficienza di banda o superiorità rispetto a FL parametrico.

## Paper-ready wording

### Methods

We characterized communication directly from the frozen FoT–TEP artifacts, without re-running any LLM. The communicated object was the exact UTF-8 peer-insight block inserted into each receiver prompt. We measured Unicode characters, UTF-8 bytes, regex-defined words, lines, and model-specific in-context token increments. Token increments were obtained by pairing B/E and A prompts for the same physical case, receiver, and repetition and subtracting the provider-recorded first-attempt input-token counts. We separately retained physical runs, three LLM repetitions, and aggregate agent-case predictions, and verified every reconstructed prompt against its frozen SHA-256 hash.

### Results

The frozen library contains 8 unique insights, two per producer; each federated receiver obtains 6 peer-only insights. One four-receiver dissemination unit contains 24 insight deliveries and {p['all_receiver_unit_B']['utf8_bytes']} UTF-8 bytes. The exact in-context increment is {p['all_receiver_unit_B']['gpt_tokens']} tokens for GPT-5.6-terra and {p['all_receiver_unit_B']['qwen_tokens']} tokens for Qwen3.8-27B-FP8. B and E have identical counts, ordering, structure, byte length, and observed token length, while differing in exactly 24 pseudolabel values across the four receiver blocks. On locally-unseen aggregate predictions, B achieved 31/36 in Experiment 1, 68/72 in EXP3_V2, and 34/36 with the Qwen consumer, compared with 0 correct under A in all three executions; these gains should be interpreted together with the semantic corruption control E.

### Limitations

These measurements characterize the realized textual payload but do not establish communication optimality, privacy, or superiority over logit-, prototype-, or parameter-sharing methods. Standalone tokenizer artifacts were not frozen, so exact token claims are restricted to paired in-context increments recorded by the providers; per-insight and centralized-context token values are explicitly estimated. Monetary cost is unavailable, Condition C is structurally non-isomorphic and post-hoc, and aggregate agent-case observations sharing a physical run are not independent physical samples.

## Riproduzione e controlli

Eseguire dalla root del repository:

```bash
python analysis/communication_characterization/characterize_payload.py
```

Il comando esegue prima i test fixture e i conteggi noti, verifica i manifest frozen correnti, ricostruisce e controlla tutti i prompt hash, legge EXP3_V2 dai tag Git e rigenera CSV, JSON e questo report. Controlli: {', '.join(summary['validation']['checks'])}. Esito: **PASS**.
"""


def self_test() -> list[str]:
    checks: list[str] = []
    m = measure_text("a b\nç")
    assert m["characters"] == 5 and m["utf8_bytes"] == 6 and m["words_unicode_regex"] == 3 and m["lines"] == 2
    checks.append("minimal UTF-8/word/line fixture")

    toy_b = [{"insight_id": "I1", "source_agent": "a", "pseudolabel": "CLS-AAAAA", "evidence_scope": "x", "observed_pattern": "y"}]
    toy_e = [{**toy_b[0], "pseudolabel": "CLS-BBBBB"}]
    b = render_insight_block(toy_b)
    e = render_insight_block(toy_e)
    assert b != e and len(b) == len(e) and len(b.encode()) == len(e.encode())
    assert {k: v for k, v in toy_b[0].items() if k != "pseudolabel"} == {k: v for k, v in toy_e[0].items() if k != "pseudolabel"}
    checks.append("minimal equal-length semantic-derangement fixture")
    return checks


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test-only", action="store_true", help="run fixture tests without writing reports")
    args = parser.parse_args()
    checks = self_test()
    if args.self_test_only:
        print("PASS:", "; ".join(checks))
        return 0

    # Verify current frozen files used for numeric results.
    checked_files = []
    checked_files += verify_hash_manifest(
        "phase_b/final_evaluation/inference/inference_output_hash_manifest.json", "artifacts"
    )
    checked_files += verify_hash_manifest(
        "phase_b/exp2/qwen/inference/inference_output_hash_manifest.json", "artifacts"
    )
    checked_files += verify_hash_manifest("phase_b/PHASE_B_PROTOCOL_HASHES.json", "artifacts")
    checked_files += verify_hash_manifest(
        "phase_b/final_evaluation/evaluation_hash_manifest.json", "evaluation_artifacts"
    )
    checked_files += verify_hash_manifest(
        "phase_b/exp2/qwen/evaluation/evaluation_hash_manifest.json", "evaluation_artifacts"
    )
    checked_files += verify_hash_manifest("icl/full_evaluation/freeze_manifest_inference.json", "artifact_hashes")
    c_predictions_manifest = read_json("icl/full_evaluation/c_predictions_manifest.json")
    if file_sha256("icl/inference/c_records.jsonl") != c_predictions_manifest["c_records_sha256"]:
        raise RuntimeError("frozen Condition C repetition record hash mismatch")
    c_aggregate_manifest = read_json("icl/full_evaluation/c_aggregate_manifest.json")
    if file_sha256("icl/inference/c_aggregate_records.jsonl") != c_aggregate_manifest["c_aggregate_records_sha256"]:
        raise RuntimeError("frozen Condition C aggregate record hash mismatch")
    frozen_c_result = git_read("condition-c-results-frozen-r10", "icl/full_evaluation/evaluation_results_c.json").encode("utf-8")
    if (ROOT / "icl/full_evaluation/evaluation_results_c.json").read_bytes() != frozen_c_result:
        raise RuntimeError("Condition C evaluator result differs from frozen tag")
    checked_files += [
        "icl/inference/c_records.jsonl", "icl/inference/c_aggregate_records.jsonl",
        "icl/full_evaluation/evaluation_results_c.json",
    ]
    checks.append(f"current frozen inference hashes ({len(checked_files)} files)")

    config = read_json("phase_b/config/protocol_config.json")
    local = read_json("phase_b/local_knowledge/local_examples.json")
    insights = read_json("phase_b/insights/final_local_insights.json")
    generation_runs = read_json("phase_b/insights/generation_runs.json")
    libraries = {
        condition: {
            agent: read_json(f"phase_b/insights/peer_libraries/{agent}_{condition}.json")
            for agent in AGENTS
        }
        for condition in ("B", "E")
    }
    block_texts = {
        condition: {agent: render_insight_block(libraries[condition][agent]) for agent in AGENTS}
        for condition in ("B", "E")
    }
    block_metrics = {
        condition: {
            agent: {**measure_text(block_texts[condition][agent]), "insight_count": len(libraries[condition][agent])}
            for agent in AGENTS
        }
        for condition in ("B", "E")
    }
    assert len(insights) == 8
    assert all(len(libraries[c][a]) == 6 for c in ("B", "E") for a in AGENTS)
    for condition in ("B", "E"):
        delivery_counts: Counter[str] = Counter()
        for agent in AGENTS:
            assert all(item["source_agent"] != agent for item in libraries[condition][agent])
            assert len({item["insight_id"] for item in libraries[condition][agent]}) == 6
            delivery_counts.update(item["insight_id"] for item in libraries[condition][agent])
        assert set(delivery_counts.values()) == {3}
    assert sum(block_metrics["B"][a]["utf8_bytes"] for a in AGENTS) == 9438
    checks.append("known frozen routing: 8 unique, 6/receiver, no self, 3 deliveries/insight, 9438 B bytes/unit")

    # Structural B/E control.
    control_by_receiver: dict[str, Any] = {}
    for agent in AGENTS:
        b_lib, e_lib = libraries["B"][agent], libraries["E"][agent]
        assert [x["insight_id"] for x in b_lib] == [x["insight_id"] for x in e_lib]
        assert [x["source_agent"] for x in b_lib] == [x["source_agent"] for x in e_lib]
        substitutions = []
        for b_item, e_item in zip(b_lib, e_lib):
            assert list(b_item) == list(e_item)
            assert {k: v for k, v in b_item.items() if k != "pseudolabel"} == {
                k: v for k, v in e_item.items() if k != "pseudolabel"
            }
            assert b_item["pseudolabel"] != e_item["pseudolabel"]
            substitutions.append({
                "insight_id": b_item["insight_id"], "from": b_item["pseudolabel"], "to": e_item["pseudolabel"],
                "old_utf8_bytes": len(b_item["pseudolabel"].encode()), "new_utf8_bytes": len(e_item["pseudolabel"].encode()),
            })
        b_bytes, e_bytes = block_texts["B"][agent].encode(), block_texts["E"][agent].encode()
        assert len(b_bytes) == len(e_bytes)
        control_by_receiver[agent] = {
            "same_insight_count": True, "same_ids_sources_structure_order": True,
            "same_non_pseudolabel_content": True, "byte_identical": b_bytes == e_bytes,
            "same_byte_length": True, "B_utf8_bytes": len(b_bytes), "E_utf8_bytes": len(e_bytes),
            "pseudolabel_substitutions": len(substitutions),
            "differing_byte_positions": sum(x != y for x, y in zip(b_bytes, e_bytes)),
            "substitutions": substitutions,
        }
    b_e_control = {
        "status": "PASS",
        "by_receiver": control_by_receiver,
        "all_receiver_unit": {
            "pseudolabel_substitutions": sum(x["pseudolabel_substitutions"] for x in control_by_receiver.values()),
            "differing_byte_positions": sum(x["differing_byte_positions"] for x in control_by_receiver.values()),
            "B_utf8_bytes": sum(x["B_utf8_bytes"] for x in control_by_receiver.values()),
            "E_utf8_bytes": sum(x["E_utf8_bytes"] for x in control_by_receiver.values()),
        },
        "cause": "only six equal-length ASCII pseudolabel values per receiver are substituted by the frozen derangement",
        "source_refs": [
            "phase_b/config/evaluator_side/condition_e_derangements.json",
            "phase_b/insights/peer_libraries/agent_*_[BE].json",
        ],
    }
    checks.append("explicit B/E structural and byte-level control")

    exp1_records = read_jsonl("phase_b/final_evaluation/inference/repetition_records.jsonl")
    qwen_records = read_jsonl("phase_b/exp2/qwen/inference/repetition_records.jsonl")
    exp3_records = git_json_directory(EXP3_INFERENCE_REF, "inference_outputs/records")
    assert len(exp1_records) == 540 and len(qwen_records) == 540 and len(exp3_records) == 1080
    checks.append("frozen repetition record counts 540/1080/540")

    gpt_delta_exp1 = paired_token_deltas(exp1_records)
    gpt_delta_exp3 = paired_token_deltas(exp3_records)
    qwen_delta = paired_token_deltas(qwen_records)
    assert gpt_delta_exp1 == gpt_delta_exp3
    assert gpt_delta_exp1["B"] == gpt_delta_exp1["E"]
    assert qwen_delta["B"] == qwen_delta["E"]
    checks.append("paired exact token deltas constant and B/E-equal")

    gpt_rate = sum(gpt_delta_exp1["B"].values()) / sum(block_metrics["B"][a]["utf8_bytes"] for a in AGENTS)
    qwen_rate = sum(qwen_delta["B"].values()) / sum(block_metrics["B"][a]["utf8_bytes"] for a in AGENTS)
    tokenization = {
        "gpt56_terra": {
            "model": "gpt-5.6-terra", "api": "OpenAI Responses API /v1/responses", "sdk_version": "3.6.0",
            "tokenizer_name": None, "tokenizer_version": None,
            "tokenizer_status": "not frozen/identified; exact counts come from provider usage logs",
            "configuration": {"reasoning_effort": "medium", "temperature": None, "seed": None},
            "in_context_delta": gpt_delta_exp1,
            "standalone_estimate_tokens_per_utf8_byte": gpt_rate,
        },
        "qwen38_27b": {
            "model": "Qwen/Qwen3.8-27B-FP8", "model_revision": "017b9c7af6b5689d5dd426a76e0bc077eb5ca20a",
            "served_model": "fot-exp2-consumer", "server": "vLLM 0.28.0", "api": "OpenAI-compatible Chat Completions",
            "sdk_version": "3.8.0", "tokenizer_name": "server tokenizer for frozen model revision",
            "tokenizer_files_frozen_in_repository": False,
            "tokenizer_status": "exact prompt counts recorded by vLLM; tokenizer files/config are not repository artifacts",
            "configuration": {"temperature": 0.0, "seed": 20260829, "thinking_token_budget": 1024, "max_tokens": 1536},
            "in_context_delta": qwen_delta,
            "standalone_estimate_tokens_per_utf8_byte": qwen_rate,
        },
        "measurement_note": "B/E token values are exact paired first-attempt in-context deltas. Standalone per-insight and C values are estimates, never exact claims.",
    }

    insight_summary = insight_metrics(insights, gpt_rate, qwen_rate)
    unique_artifact = measure_text(read_text("phase_b/insights/final_local_insights.json"))
    payload = {
        "serialization": "PEER INSIGHTS\\n + json.dumps(records, ensure_ascii=False, indent=2) + \\n\\n",
        "word_rule": WORD_RE.pattern,
        "unique_library_artifact": unique_artifact,
        "unique_insights": insight_summary,
        "B_blocks": block_metrics["B"],
        "E_blocks": block_metrics["E"],
        "all_receiver_unit_B": {
            "insight_record_deliveries": 24,
            "characters": sum(block_metrics["B"][a]["characters"] for a in AGENTS),
            "utf8_bytes": sum(block_metrics["B"][a]["utf8_bytes"] for a in AGENTS),
            "gpt_tokens": sum(gpt_delta_exp1["B"].values()),
            "qwen_tokens": sum(qwen_delta["B"].values()),
        },
        "source_refs": ["phase_b/insights/final_local_insights.json", "phase_b/insights/peer_libraries/agent_*_[BE].json", "phase_b/conditions/builders.py"],
    }

    exp1_fault = exp1_case_fault_mapping()
    exp1_usage = summarize_usage(exp1_records, exp1_fault)
    qwen_usage = summarize_usage(qwen_records, exp1_fault)
    exp3_usage = summarize_usage(exp3_records, exp1_fault)

    exp1_texts = load_exp1_case_texts()
    exp3_texts = load_exp3_case_texts(exp3_records)
    exp1_prompts = prompt_metrics_abe(exp1_records, exp1_texts, config, local, libraries)
    qwen_prompts = prompt_metrics_abe(qwen_records, exp1_texts, config, local, libraries)
    exp3_prompts = prompt_metrics_abe(exp3_records, exp3_texts, config, local, libraries)
    assert exp1_prompts == qwen_prompts
    checks.append("all A/B/E prompt hashes reconstructed and verified")

    c_records = read_jsonl("icl/inference/c_records.jsonl")
    c_examples = read_json("icl/pooled_libraries/pooled_examples.json")
    c_insights = read_json("icl/pooled_libraries/pooled_insights.json")
    assert c_insights == insights
    c_usage = summarize_condition_c_usage(c_records)
    c_prompts = prompt_metrics_c(c_records, exp1_texts, c_examples, c_insights)
    checks.append("all Condition C prompt hashes reconstructed and verified")

    c_examples_text = json.dumps(c_examples, ensure_ascii=False, indent=2)
    c_insights_text = render_insight_block(c_insights)
    c_context_metrics = {
        key: measure_text(c_examples_text)[key] + measure_text(c_insights_text)[key]
        for key in ("characters", "utf8_bytes", "words_unicode_regex", "lines")
    }
    c_context_metrics["sha256"] = None
    c_context = {
        "definition": "sum of two non-contiguous inserted prompt regions: pooled examples JSON plus all-insight PEER INSIGHTS block",
        "metrics": c_context_metrics,
        "gpt_estimated_tokens": round(c_context_metrics["utf8_bytes"] * gpt_rate),
        "qwen_estimated_tokens": round(c_context_metrics["utf8_bytes"] * qwen_rate),
        "token_status": "estimated by model-specific empirical peer-block token/byte rate; not exact",
        "source_refs": ["icl/pooled_libraries/pooled_examples.json", "icl/pooled_libraries/pooled_insights.json", "icl/conditions/builder_c.py"],
    }

    accuracy = accuracy_data()
    real_to_opaque = read_json("phase_b/config/evaluator_side/pseudolabel_mapping.json")["real_to_opaque"]
    exp1_agent_accuracy = per_agent_unseen_accuracy(
        read_jsonl("phase_b/final_evaluation/inference/aggregate_records.jsonl"), exp1_fault, real_to_opaque
    )
    qwen_agent_accuracy = per_agent_unseen_accuracy(
        read_jsonl("phase_b/exp2/qwen/inference/aggregate_records.jsonl"), exp1_fault, real_to_opaque
    )
    exp3_agent_accuracy = per_agent_unseen_accuracy(
        git_jsonl(EXP3_INFERENCE_REF, "inference_outputs/aggregate_records.jsonl"), exp1_fault, real_to_opaque
    )
    for key, table in (
        ("experiment_1", exp1_agent_accuracy),
        ("exp3_v2", exp3_agent_accuracy),
        ("experiment_2_qwen", qwen_agent_accuracy),
    ):
        for condition in "ABE":
            assert sum(table[condition][agent]["n"] for agent in AGENTS) == accuracy[key][condition]["n"]
            assert sum(table[condition][agent]["correct"] for agent in AGENTS) == accuracy[key][condition]["correct"]
    checks.append("per-agent unseen accuracies reconcile to frozen totals")

    experiments: dict[str, Any] = {
        "experiment_1": {
            "consumer_model": "gpt-5.6-terra", "tokenizer_key": "gpt56_terra", "accuracy_key": "experiment_1",
            "physical_cases": 15, "physical_fault_cases": 12, "repetitions": 3, "aggregate_predictions_per_condition": 60,
            "usage": exp1_usage, "prompt_metrics": exp1_prompts, "per_agent_unseen_accuracy": exp1_agent_accuracy,
            "source_refs": ["phase_b/final_evaluation/inference/repetition_records.jsonl", "phase_b/final_evaluation/evaluation_results.json"],
        },
        "exp3_v2": {
            "consumer_model": "gpt-5.6-terra", "tokenizer_key": "gpt56_terra", "accuracy_key": "exp3_v2",
            "physical_cases": 30, "physical_fault_cases": 24, "repetitions": 3, "aggregate_predictions_per_condition": 120,
            "usage": exp3_usage, "prompt_metrics": exp3_prompts, "per_agent_unseen_accuracy": exp3_agent_accuracy,
            "source_refs": [f"git:{EXP3_INFERENCE_REF}:inference_outputs/records/*.json", f"git:{EXP3_RESULTS_REF}:evaluation_outputs/exp3v2_confirmatory_results.json"],
        },
        "experiment_2_qwen": {
            "consumer_model": "Qwen/Qwen3.8-27B-FP8", "tokenizer_key": "qwen38_27b", "accuracy_key": "experiment_2_qwen",
            "physical_cases": 15, "physical_fault_cases": 12, "repetitions": 3, "aggregate_predictions_per_condition": 60,
            "usage": qwen_usage, "prompt_metrics": qwen_prompts, "per_agent_unseen_accuracy": qwen_agent_accuracy,
            "source_refs": ["phase_b/exp2/qwen/inference/repetition_records.jsonl", "phase_b/exp2/qwen/evaluation/evaluation_results.json", "phase_b/exp2/qwen/config.json"],
        },
        "condition_c": {
            "consumer_model": "gpt-5.6-terra", "physical_cases": 15, "physical_fault_cases": 12, "repetitions": 3,
            "aggregate_predictions_per_condition": 15, "usage": c_usage, "prompt_metrics": {"C": c_prompts},
            "source_refs": ["icl/inference/c_records.jsonl", "icl/full_evaluation/evaluation_results_c.json"],
        },
    }

    for name in ("experiment_1", "exp3_v2", "experiment_2_qwen"):
        meta = experiments[name]
        calls_per_agent = meta["usage"]["by_condition"]["B"]["logical_calls"] // 4
        deltas = tokenization[meta["tokenizer_key"]]["in_context_delta"]
        meta["transfers"] = {
            condition: transfer_metrics(
                condition=condition,
                logical_calls=meta["usage"]["by_condition"][condition]["logical_calls"],
                calls_per_agent=calls_per_agent,
                block_metrics=block_metrics[condition] if condition != "A" else block_metrics["B"],
                token_deltas=deltas,
                model_key=meta["consumer_model"],
            )
            for condition in "ABE"
        }
        meta["federated_payload_total_B_plus_E"] = {
            "knowledge_rounds": 2,
            "prompt_block_transfers": sum(meta["transfers"][c]["prompt_block_transfers"] for c in "BE"),
            "repeated_source_consumer_transfers": sum(meta["transfers"][c]["repeated_source_consumer_transfers"] for c in "BE"),
            "insight_record_deliveries": sum(meta["transfers"][c]["insight_record_deliveries"] for c in "BE"),
            "total_utf8_bytes": sum(meta["transfers"][c]["total_utf8_bytes"] for c in "BE"),
            "total_payload_tokens_in_context": sum(meta["transfers"][c]["total_payload_tokens_in_context"] for c in "BE"),
            "note": "two analytical conditions, each using the same static one-round payload volume; this is not two iterative training rounds",
        }
        b_transfer = meta["transfers"]["B"]
        b_prompt = meta["prompt_metrics"]["B"]
        b_first_input = meta["usage"]["by_condition"]["B"]["input_tokens_first_attempts"]
        meta["prompt_payload_ratio_B"] = {
            "utf8_byte_ratio": b_transfer["total_utf8_bytes"] / b_prompt["total_utf8_bytes"],
            "token_ratio": b_transfer["total_payload_tokens_in_context"] / b_first_input,
            "formula_bytes": "total repeated peer-block UTF-8 bytes / total reconstructed full-prompt UTF-8 bytes",
            "formula_tokens": "total paired first-attempt B-A input-token delta / total B first-attempt input tokens",
        }
    experiments["condition_c"]["prompt_payload_ratio_C"] = {
        "utf8_byte_ratio": (c_context_metrics["utf8_bytes"] * c_usage["logical_calls"]) / c_prompts["total_utf8_bytes"],
        "token_ratio": None,
        "token_status": "not exactly isolable; C changes two context blocks and has no paired empty-context execution",
    }

    efficiency = {
        "experiment_1": efficiency_metrics(
            "experiment_1", accuracy["experiment_1"], experiments["experiment_1"]["transfers"]["B"],
            block_metrics["B"], gpt_delta_exp1["B"], calls_per_agent_unseen=27, repetitions=3,
        ),
        "exp3_v2": efficiency_metrics(
            "exp3_v2", accuracy["exp3_v2"], experiments["exp3_v2"]["transfers"]["B"],
            block_metrics["B"], gpt_delta_exp1["B"], calls_per_agent_unseen=54, repetitions=3,
        ),
        "experiment_2_qwen": efficiency_metrics(
            "experiment_2_qwen", accuracy["experiment_2_qwen"], experiments["experiment_2_qwen"]["transfers"]["B"],
            block_metrics["B"], qwen_delta["B"], calls_per_agent_unseen=27, repetitions=3,
        ),
    }

    producer = producer_metrics(generation_runs)
    git_refs = {
        EXP3_INFERENCE_REF: str(git_output("rev-parse", f"{EXP3_INFERENCE_REF}^{{}}" )).strip(),
        EXP3_RESULTS_REF: str(git_output("rev-parse", f"{EXP3_RESULTS_REF}^{{}}" )).strip(),
        "exp3_v2_verbalization_payload_commit": str(git_output("rev-parse", EXP3_VERBALIZATION_REF)).strip(),
    }

    summary = {
        "schema_version": "1.0",
        "analysis_status": "MEASURED_FROM_FROZEN_ARTIFACTS_NO_LLM_CALLS",
        "repository_root": str(ROOT),
        "git_head_observed": str(git_output("rev-parse", "HEAD")).strip(),
        "historical_frozen_refs": git_refs,
        "measurement_classes": {
            "measured": "characters, UTF-8 bytes, words, lines, provider usage, prompt hashes, accuracies",
            "exact_in_context": "paired A/B/E first-attempt input-token deltas",
            "estimated": "standalone per-insight and Condition C payload token counts",
            "interpretive": "cross-paradigm comparison and communication-round framing",
        },
        "payload": payload,
        "tokenization": tokenization,
        "producer_cost": producer,
        "experiments": experiments,
        "condition_c_payload": c_context,
        "b_e_structural_control": b_e_control,
        "pseudolabel_mapping": {
            "real_to_opaque": real_to_opaque,
            "source": "phase_b/config/evaluator_side/pseudolabel_mapping.json",
        },
        "condition_e_derangements": read_json("phase_b/config/evaluator_side/condition_e_derangements.json")["derangements"],
        "accuracy": accuracy,
        "efficiency": efficiency,
        "adjacent_paradigms": {
            "numeric_comparability": "not available without concrete matched configurations",
            "formulas": {
                "FedMD_uplink": "K * N_public * C * bytes_per_logit per round",
                "FedProto_uplink": "sum_k(C_k * embedding_dimension * bytes_per_scalar) per round",
                "federated_LoRA_uplink": "K * P_adapter * bytes_per_parameter per round; P_LoRA=sum r(d_in+d_out)",
                "FoT_realized": "sum over prompt calls of receiver-specific UTF-8 peer-block bytes/tokens",
            },
            "source_refs": ["docs/lit_review/FOT_TEP_GAP_ANALYSIS_AND_RELATED_WORK.md", "docs/lit_review/FOT_TEP_LITERATURE_REVIEW_BIGDATA2026.md"],
        },
        "missing_data": [
            "standalone GPT-5.6-terra tokenizer name/version/files",
            "repository-frozen Qwen tokenizer files/config (model revision is frozen)",
            "reasoning-token breakdown for Condition C",
            "usable latency for Qwen and Condition C",
            "applicable monetary prices or charged amounts",
            "concrete isomorphic FedMD/FedProto/LoRA configurations",
            "Condition C on EXP3_V2",
        ],
        "main_document_sources": MAIN_SOURCES,
        "validation": {"status": "PASS", "checks": checks, "hash_verified_current_files": checked_files},
    }

    rows = build_csv_rows(experiments, libraries, block_texts, tokenization, accuracy, c_context)
    write_csv(rows)
    JSON_PATH.write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(build_report(summary), encoding="utf-8")

    print(f"PASS: {len(checks)} validation checks")
    print(CSV_PATH.relative_to(ROOT))
    print(JSON_PATH.relative_to(ROOT))
    print(REPORT_PATH.relative_to(ROOT))
    return 0


if __name__ == "__main__":
    sys.exit(main())
