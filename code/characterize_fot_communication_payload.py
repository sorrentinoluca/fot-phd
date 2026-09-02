#!/usr/bin/env python3
"""Characterize the frozen Experiment 1 FoT communication payload.

This script is descriptive only. It reads frozen Phase A/Phase B artifacts and
the local development workbooks used to create the insight-generation inputs.
It never calls a model, evaluates predictions, or mutates a frozen artifact.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / "code"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from phase_b.conditions.builders import (  # noqa: E402
    condition_peer_insights,
    render_peer_insight_block,
)
from phase_b.insights import validate_global_insights  # noqa: E402
from tep_features import XMEAS, iter_time_windows, normalize_schema, sampling_interval_hours  # noqa: E402


FROZEN_HASH_MANIFEST = ROOT / "phase_b" / "PHASE_B_PROTOCOL_HASHES.json"
FROZEN_PROTOCOL = ROOT / "phase_b" / "config" / "phase_b_protocol_frozen.json"
PROTOCOL_CONFIG = ROOT / "phase_b" / "config" / "protocol_config.json"
EXECUTION_CONFIG = ROOT / "phase_b" / "config" / "execution_config.json"
PSEUDOLABEL_MAPPING = (
    ROOT / "phase_b" / "config" / "evaluator_side" / "pseudolabel_mapping.json"
)
INSIGHT_LIBRARY = ROOT / "phase_b" / "insights" / "final_local_insights.json"
INPUT_BUNDLE_DIR = ROOT / "phase_b" / "insights" / "input_bundles"
PEER_LIBRARY_DIR = ROOT / "phase_b" / "insights" / "peer_libraries"
V2_CONFIG = ROOT / "code" / "verbalizer_config_v2.json"
DEFAULT_CACHE = ROOT / "code" / "tep_cache"
DEFAULT_SOURCE_REPO = ROOT / "tennessee-eastman-dataset"
DEFAULT_OUTPUT_DIR = ROOT / "supporting_records" / "communication_characterization"

TOKEN_UNAVAILABLE = "TOKEN COUNT NOT REPRODUCIBLY AVAILABLE FROM CURRENT ARTIFACTS"


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_output(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout


def verify_lfs_source(
    *, source_repo: Path, dataset_commit: str, repository_path: str, local_path: Path
) -> dict[str, Any]:
    """Match one local workbook to its Git-LFS pointer in the pinned commit."""
    pointer = git_output(source_repo, "show", f"{dataset_commit}:{repository_path}")
    match = re.fullmatch(
        r"version https://git-lfs\.github\.com/spec/v1\n"
        r"oid sha256:([0-9a-f]{64})\n"
        r"size ([0-9]+)\n?",
        pointer,
    )
    if match is None:
        raise RuntimeError(
            f"Pinned source entry is not an auditable Git-LFS pointer: {repository_path}"
        )
    expected_sha, expected_size_text = match.groups()
    expected_size = int(expected_size_text)
    observed_sha = sha256_file(local_path)
    observed_size = local_path.stat().st_size
    if observed_sha != expected_sha or observed_size != expected_size:
        raise RuntimeError(
            f"Local workbook does not match pinned dataset LFS object: {local_path}"
        )
    return {
        "dataset_repository_path": repository_path,
        "lfs_sha256": expected_sha,
        "lfs_size_bytes": expected_size,
        "local_match": True,
    }


def text_size(value: str) -> dict[str, int]:
    """Return Unicode-code-point and UTF-8 byte counts."""
    return {"chars": len(value), "utf8_bytes": len(value.encode("utf-8"))}


def ratio(numerator: int, denominator: int) -> dict[str, float]:
    if numerator <= 0 or denominator <= 0:
        raise ValueError("payload ratio inputs must be positive")
    return {
        "textual_to_raw": numerator / denominator,
        "reference_raw_to_text": denominator / numerator,
    }


def verify_frozen_artifacts() -> dict[str, str]:
    manifest = load_json(FROZEN_HASH_MANIFEST)["artifacts"]
    required = [
        "phase_b/config/phase_b_protocol_frozen.json",
        "phase_b/config/protocol_config.json",
        "phase_b/config/execution_config.json",
        "phase_b/config/evaluator_side/pseudolabel_mapping.json",
        "phase_b/insights/final_local_insights.json",
        "phase_b/insights/generation_runs.json",
        "phase_b/execution/generate_final_insights.py",
        "phase_b/conditions/builders.py",
        "code/verbalizer_config_v2.json",
        "code/tep_verbalize_v2.py",
        "code/tep_features.py",
    ]
    required.extend(
        f"phase_b/insights/input_bundles/agent_{index}.json" for index in range(1, 5)
    )
    required.extend(
        f"phase_b/insights/peer_libraries/agent_{index}_B.json"
        for index in range(1, 5)
    )
    verified: dict[str, str] = {}
    for relative in required:
        path = ROOT / relative
        expected = manifest.get(relative)
        if expected is None:
            raise RuntimeError(f"Frozen hash is unavailable for {relative}")
        observed = sha256_file(path)
        if observed != expected:
            raise RuntimeError(
                f"Frozen artifact hash mismatch for {relative}: {observed} != {expected}"
            )
        verified[relative] = observed
    return verified


def validate_insight_inputs(
    *, protocol: dict[str, Any], frozen: dict[str, Any], insights: list[dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    validated = validate_global_insights(insights, protocol)
    expected_total = int(frozen["insights"]["total"])
    if len(validated) != expected_total:
        raise RuntimeError(f"Expected {expected_total} insights, got {len(validated)}")

    bundles: dict[str, dict[str, Any]] = {}
    for agent_id in protocol["agents"]:
        bundle = load_json(INPUT_BUNDLE_DIR / f"{agent_id}.json")
        if bundle["source_agent"] != agent_id:
            raise RuntimeError(f"Input bundle source mismatch for {agent_id}")
        if bundle["contains_structured_numerical_json"] is not False:
            raise RuntimeError(f"Structured numerical JSON unexpectedly present for {agent_id}")
        texts = bundle["neutral_texts"]
        expected_batches = frozen["data_boundary"]["insight_and_local_knowledge_fault_batches"]
        if len(texts) != len(expected_batches) or any(not text.strip() for text in texts):
            raise RuntimeError(f"Invalid five-batch neutral-text bundle for {agent_id}")
        bundles[agent_id] = bundle
    return bundles


def characterize_payload(
    *, protocol: dict[str, Any], frozen: dict[str, Any], insights: list[dict[str, Any]]
) -> dict[str, Any]:
    receivers: list[dict[str, Any]] = []
    transmission_counts: Counter[str] = Counter()

    for agent_id in protocol["agents"]:
        peer = condition_peer_insights(
            agent_id=agent_id,
            condition="B",
            config=protocol,
            global_insights=insights,
        )
        block = render_peer_insight_block(
            agent_id=agent_id,
            condition="B",
            config=protocol,
            global_insights=insights,
        )
        artifact_path = PEER_LIBRARY_DIR / f"{agent_id}_B.json"
        artifact_text = artifact_path.read_text(encoding="utf-8")
        expected_block = "PEER INSIGHTS\n" + artifact_text.rstrip("\n") + "\n\n"
        if block != expected_block:
            raise RuntimeError(f"Rendered prompt block differs from {artifact_path.name}")
        if len(peer) != int(frozen["federation"]["peer_insights_per_agent"]):
            raise RuntimeError(f"Unexpected Condition-B insight count for {agent_id}")
        if any(item.source_agent == agent_id for item in peer):
            raise RuntimeError(f"Self insight routed to {agent_id}")
        if any(item.pseudolabel == "Normal" for item in peer):
            raise RuntimeError(f"Normal insight routed to {agent_id}")
        transmission_counts.update(item.insight_id for item in peer)
        receivers.append(
            {
                "receiver": agent_id,
                "n_insights": len(peer),
                "insight_ids": [item.insight_id for item in peer],
                "source_agents": sorted({item.source_agent for item in peer}),
                "rendered_prompt_block": text_size(block),
                "json_artifact_representation": {
                    **text_size(artifact_text),
                    "path": str(artifact_path.relative_to(ROOT)),
                    "includes_terminal_newline": artifact_text.endswith("\n"),
                },
            }
        )

    unique_ids = {item["insight_id"] for item in insights}
    if set(transmission_counts) != unique_ids:
        raise RuntimeError("At least one unique insight is not transmitted")
    if set(transmission_counts.values()) != {3}:
        raise RuntimeError(f"Expected each insight at three receivers: {transmission_counts}")

    total_chars = sum(row["rendered_prompt_block"]["chars"] for row in receivers)
    total_bytes = sum(row["rendered_prompt_block"]["utf8_bytes"] for row in receivers)
    library_text = INSIGHT_LIBRARY.read_text(encoding="utf-8")
    library_body = json.dumps(insights, ensure_ascii=False, indent=2)
    heldout_cases = int(frozen["data_boundary"]["independent_heldout_case_count"])
    repetitions = int(frozen["execution"]["repetitions"])
    repeated_rounds = heldout_cases * repetitions

    return {
        "primary_serialization": {
            "name": "rendered Condition-B peer block",
            "definition": "PEER INSIGHTS\\n + json.dumps(peer_insights, ensure_ascii=False, indent=2) + \\n\\n",
            "character_unit": "Unicode code points as counted by Python len(str)",
            "byte_unit": "UTF-8 encoded bytes",
        },
        "receivers": receivers,
        "all_receiver_unit": {
            "definition": "one Condition-B prompt invocation for each of the four receivers",
            "receiver_count": len(receivers),
            "total_insight_transmissions": sum(transmission_counts.values()),
            "per_unique_insight_receiver_count": dict(sorted(transmission_counts.items())),
            "chars": total_chars,
            "utf8_bytes": total_bytes,
        },
        "unique_knowledge_stored": {
            "n_unique_insights": len(unique_ids),
            "frozen_library_artifact": {
                **text_size(library_text),
                "path": str(INSIGHT_LIBRARY.relative_to(ROOT)),
                "includes_terminal_newline": library_text.endswith("\n"),
            },
            "prompt_compatible_json_body": text_size(library_body),
        },
        "full_frozen_condition_b_execution": {
            "definition": "15 held-out cases x 4 receivers x R=3 Condition-B calls",
            "heldout_cases": heldout_cases,
            "repetitions": repetitions,
            "prompt_calls": repeated_rounds * len(receivers),
            "total_insight_transmissions": repeated_rounds * sum(transmission_counts.values()),
            "chars": repeated_rounds * total_chars,
            "utf8_bytes": repeated_rounds * total_bytes,
            "note": "This is repeated transmission across frozen calls, not unique knowledge size.",
        },
    }


def inspect_fault_workbook(
    path: Path,
    *,
    source_repo: Path,
    source_repository_path: str,
    dataset_commit: str,
    injection_h: float,
    end_h: float,
    window_h: float,
) -> dict[str, Any]:
    if not path.is_file():
        raise FileNotFoundError(f"Required development workbook is unavailable: {path}")
    source_verification = verify_lfs_source(
        source_repo=source_repo,
        dataset_commit=dataset_commit,
        repository_path=source_repository_path,
        local_path=path,
    )
    raw = pd.read_excel(path)
    case = normalize_schema(raw, source=str(path))
    dt = sampling_interval_hours(case)
    windows = list(
        iter_time_windows(case, start_h=injection_h, end_h=end_h, window_h=window_h)
    )
    post_samples = sum(len(window) for _, _, window in windows)
    expected_post = int(round((end_h - injection_h) / dt))
    if post_samples != expected_post:
        raise RuntimeError(f"Unexpected post-injection sample count in {path.name}")
    if any(len(window) != int(round(window_h / dt)) for _, _, window in windows):
        raise RuntimeError(f"Unequal analysis-window sample count in {path.name}")
    return {
        "path": str(path.relative_to(ROOT)),
        "sha256": sha256_file(path),
        "xlsx_file_size_bytes": path.stat().st_size,
        "workbook_rows_loaded": len(case),
        "time_start_h": float(case["Time"].iloc[0]),
        "time_end_h": float(case["Time"].iloc[-1]),
        "sampling_interval_h": dt,
        "post_injection_samples_consumed": post_samples,
        "analysis_windows": len(windows),
        "samples_per_window": [len(window) for _, _, window in windows],
        "xmeas_variables": len(XMEAS),
        "normalized_xmeas_dtypes": sorted({str(case[name].dtype) for name in XMEAS}),
        "pinned_source_verification": source_verification,
    }


def characterize_evidence(
    *,
    cache_dir: Path,
    source_repo: Path,
    protocol: dict[str, Any],
    frozen: dict[str, Any],
    v2_config: dict[str, Any],
) -> dict[str, Any]:
    mapping = load_json(PSEUDOLABEL_MAPPING)["real_to_opaque"]
    opaque_to_real = {opaque: real for real, opaque in mapping.items()}
    batches = frozen["data_boundary"]["insight_and_local_knowledge_fault_batches"]
    if batches != [1, 2, 3, 4, 5]:
        raise RuntimeError(f"Unexpected frozen insight batches: {batches}")

    injection_h = float(v2_config["fault_injection_h"])
    dataset_commit = str(v2_config["dataset_commit"])
    try:
        commit_identity = git_output(
            source_repo, "show", "-s", "--format=%H%n%s", dataset_commit
        ).splitlines()
    except (subprocess.CalledProcessError, FileNotFoundError) as exc:
        raise RuntimeError(
            f"Pinned dataset commit is unavailable in {source_repo}: {dataset_commit}"
        ) from exc
    if commit_identity != [dataset_commit, "Add simulations with sp changes"]:
        raise RuntimeError(f"Unexpected pinned dataset identity: {commit_identity}")
    window_h = float(v2_config["window_hours"])
    end_h = 50.0
    feature_names = list(v2_config["feature_semantics"])
    expected_features = {
        "shift_sigma",
        "slope_sigma_h",
        "raw_std_ratio",
        "diff_std_ratio",
        "residual_std_ratio",
    }
    if set(feature_names) != expected_features:
        raise RuntimeError(f"Unexpected frozen feature semantics: {feature_names}")

    per_source_agent: list[dict[str, Any]] = []
    all_workbooks: list[dict[str, Any]] = []
    for agent_id, agent in protocol["agents"].items():
        pseudolabel = agent["local_fault_label"]
        real_label = opaque_to_real[pseudolabel]
        real_number = int(real_label.removeprefix("F"))
        workbook_rows = [
            inspect_fault_workbook(
                cache_dir / f"mode1_{real_number}_{batch}.xlsx",
                source_repo=source_repo,
                source_repository_path=(
                    f"simulations/mode_1/faults/mode1_{real_number}_{batch}.xlsx"
                ),
                dataset_commit=dataset_commit,
                injection_h=injection_h,
                end_h=end_h,
                window_h=window_h,
            )
            for batch in batches
        ]
        all_workbooks.extend(workbook_rows)
        post_samples = sum(row["post_injection_samples_consumed"] for row in workbook_rows)
        windows = sum(row["analysis_windows"] for row in workbook_rows)
        raw_values = post_samples * len(XMEAS)
        structured_values = windows * len(XMEAS) * len(feature_names)
        per_source_agent.append(
            {
                "source_agent": agent_id,
                "evaluator_side_real_fault": real_label,
                "development_batches": list(batches),
                "n_development_batches": len(batches),
                "workbook_rows_loaded_per_batch": sorted(
                    {row["workbook_rows_loaded"] for row in workbook_rows}
                ),
                "post_injection_samples_consumed_per_batch": sorted(
                    {row["post_injection_samples_consumed"] for row in workbook_rows}
                ),
                "post_injection_samples_consumed_total": post_samples,
                "xmeas_variables": len(XMEAS),
                "raw_observation_values": raw_values,
                "reference_dense_float64_bytes": raw_values * 8,
                "analysis_windows_total": windows,
                "numerical_feature_names": feature_names,
                "numerical_features_per_window_variable": len(feature_names),
                "structured_numerical_feature_values": structured_values,
                "workbooks": workbook_rows,
            }
        )

    normal_path = cache_dir / "mode1_normal_500.xlsx"
    if not normal_path.is_file():
        raise FileNotFoundError(f"Required Normal workbook is unavailable: {normal_path}")
    normal_source_verification = verify_lfs_source(
        source_repo=source_repo,
        dataset_commit=dataset_commit,
        repository_path="simulations/mode_1/mode1_normal_500.xlsx",
        local_path=normal_path,
    )
    samples_per_hour = 60 // int(v2_config["sampling_minutes"])
    normal_rows = 5 * 50 * samples_per_hour
    normal_raw = pd.read_excel(normal_path, nrows=normal_rows)
    normal = normalize_schema(normal_raw, source="Normal N1-N5 baseline")
    if len(normal) != normal_rows or float(normal["Time"].max()) >= 250.0:
        raise RuntimeError("Normal baseline does not match N1-N5 [0, 250 h)")
    normal_values = len(normal) * len(XMEAS)
    normal_reference = {
        "role": "shared frozen normalization/calibration reference; not peer fault-specific experience",
        "path": str(normal_path.relative_to(ROOT)),
        "blocks": ["N1", "N2", "N3", "N4", "N5"],
        "samples": len(normal),
        "xmeas_variables": len(XMEAS),
        "raw_observation_values": normal_values,
        "reference_dense_float64_bytes": normal_values * 8,
        "baseline_summary_scalars": 4 * len(XMEAS),
        "baseline_summary_fields": ["mean", "std", "diff_std", "residual_std"],
        "frozen_threshold_scalars": len(v2_config["thresholds"]),
        "xlsx_file_size_bytes": normal_path.stat().st_size,
        "note": "The file size covers the full 500 h workbook and is not used in a payload ratio.",
        "pinned_source_verification": normal_source_verification,
    }

    per_agent_by_id = {row["source_agent"]: row for row in per_source_agent}
    per_receiver: list[dict[str, Any]] = []
    for receiver in protocol["agents"]:
        peers = sorted(agent for agent in protocol["agents"] if agent != receiver)
        peer_raw_values = sum(per_agent_by_id[agent]["raw_observation_values"] for agent in peers)
        peer_structured = sum(
            per_agent_by_id[agent]["structured_numerical_feature_values"] for agent in peers
        )
        per_receiver.append(
            {
                "receiver": receiver,
                "peer_source_agents": peers,
                "peer_fault_raw_observation_values": peer_raw_values,
                "peer_fault_reference_dense_float64_bytes": peer_raw_values * 8,
                "peer_structured_numerical_feature_values": peer_structured,
                "peer_fault_plus_shared_normal_raw_values": peer_raw_values + normal_values,
                "peer_fault_plus_shared_normal_reference_dense_float64_bytes": (
                    peer_raw_values + normal_values
                )
                * 8,
            }
        )

    total_fault_values = sum(row["raw_observation_values"] for row in per_source_agent)
    total_structured = sum(
        row["structured_numerical_feature_values"] for row in per_source_agent
    )
    return {
        "dataset_source_snapshot_verification": {
            "repository": (
                str(source_repo.relative_to(ROOT))
                if source_repo.is_relative_to(ROOT)
                else str(source_repo)
            ),
            "commit": dataset_commit,
            "commit_subject": commit_identity[1],
            "development_workbooks_matching_lfs_pointers": len(all_workbooks) + 1,
            "status": "PASS",
        },
        "window_consumption_rule": {
            "source": "code/tep_features.py::iter_time_windows and code/tep_verbalize_v2.py::verbalize_case",
            "interval": "left-closed/right-open [10 h, 50 h)",
            "pre_injection_rows_loaded_but_not_feature-extracted": True,
            "time_coordinate_excluded_from_raw_observation_count": True,
        },
        "structured_evidence_definition": {
            "counted": "five base numerical descriptors per window and XMEAS",
            "feature_names": feature_names,
            "excluded": "abs_shift_sigma/abs_slope_sigma_h duplicates, threshold booleans, summaries, and text",
            "direct_insight_model_input": False,
            "note": "The insight-generation LLM received only the five neutral texts; structured numerical JSON was false in every bundle.",
        },
        "per_source_agent": per_source_agent,
        "per_receiver_peer_sources": per_receiver,
        "shared_normal_reference": normal_reference,
        "system_unique_source_evidence": {
            "fault_raw_observation_values": total_fault_values,
            "fault_reference_dense_float64_bytes": total_fault_values * 8,
            "fault_structured_numerical_feature_values": total_structured,
            "fault_plus_shared_normal_raw_observation_values": total_fault_values
            + normal_values,
            "fault_plus_shared_normal_reference_dense_float64_bytes": (
                total_fault_values + normal_values
            )
            * 8,
        },
        "reference_serialization": {
            "name": "theoretical dense float64 numerical payload",
            "formula": "number_of_raw_XMEAS_values * 8 bytes",
            "scope": "reference convention only; it is not the physical size of the XLSX files",
        },
    }


def add_ratios(report: dict[str, Any]) -> None:
    evidence_by_receiver = {
        row["receiver"]: row for row in report["local_evidence_reference"]["per_receiver_peer_sources"]
    }
    for payload_row in report["actual_fot_textual_payload"]["receivers"]:
        evidence = evidence_by_receiver[payload_row["receiver"]]
        text_bytes = payload_row["rendered_prompt_block"]["utf8_bytes"]
        payload_row["ratios"] = {
            "peer_fault_experience_only": {
                "formula": "rendered_peer_block_utf8_bytes / (peer_fault_raw_XMEAS_values * 8)",
                **ratio(text_bytes, evidence["peer_fault_reference_dense_float64_bytes"]),
            },
            "peer_fault_plus_shared_normal_once": {
                "formula": "rendered_peer_block_utf8_bytes / ((peer_fault_raw_XMEAS_values + shared_Normal_N1_N5_XMEAS_values) * 8)",
                **ratio(
                    text_bytes,
                    evidence[
                        "peer_fault_plus_shared_normal_reference_dense_float64_bytes"
                    ],
                ),
            },
        }

    payload = report["actual_fot_textual_payload"]
    evidence = report["local_evidence_reference"]["system_unique_source_evidence"]
    payload["unique_knowledge_stored"]["ratios"] = {
        "fault_experience_only": {
            "formula": "frozen_unique_library_artifact_utf8_bytes / (all_source_fault_raw_XMEAS_values * 8)",
            **ratio(
                payload["unique_knowledge_stored"]["frozen_library_artifact"]["utf8_bytes"],
                evidence["fault_reference_dense_float64_bytes"],
            ),
        },
        "fault_plus_shared_normal_once": {
            "formula": "frozen_unique_library_artifact_utf8_bytes / ((all_source_fault_raw_XMEAS_values + shared_Normal_N1_N5_XMEAS_values) * 8)",
            **ratio(
                payload["unique_knowledge_stored"]["frozen_library_artifact"]["utf8_bytes"],
                evidence["fault_plus_shared_normal_reference_dense_float64_bytes"],
            ),
        },
    }
    payload["all_receiver_unit"]["ratios"] = {
        "formula": "sum_of_four_rendered_peer_block_utf8_bytes / (all_source_fault_raw_XMEAS_values * 8)",
        **ratio(
            payload["all_receiver_unit"]["utf8_bytes"],
            evidence["fault_reference_dense_float64_bytes"],
        ),
        "note": "The numerator includes three deliveries per unique insight; the denominator counts unique fault-source evidence once.",
    }


def build_report(
    cache_dir: Path = DEFAULT_CACHE, source_repo: Path = DEFAULT_SOURCE_REPO
) -> dict[str, Any]:
    verified = verify_frozen_artifacts()
    protocol = load_json(PROTOCOL_CONFIG)
    frozen = load_json(FROZEN_PROTOCOL)
    execution = load_json(EXECUTION_CONFIG)
    v2_config = load_json(V2_CONFIG)
    insights = load_json(INSIGHT_LIBRARY)
    validate_insight_inputs(protocol=protocol, frozen=frozen, insights=insights)
    report: dict[str, Any] = {
        "schema_version": "1.0",
        "scope": "Experiment 1 frozen communication payload characterization",
        "status": "DESCRIPTIVE_ONLY",
        "dataset_source_commit": v2_config["dataset_commit"],
        "actual_fot_textual_payload": characterize_payload(
            protocol=protocol, frozen=frozen, insights=insights
        ),
        "token_count": {
            "status": TOKEN_UNAVAILABLE,
            "provider": execution["provider"],
            "requested_model": execution["requested_model"],
            "returned_model": execution["returned_model"],
            "sdk_package": execution["sdk_package"],
            "sdk_version": execution["sdk_version"],
            "token_accounting_source": execution["token_accounting_source"],
            "tokenizer_recorded": execution.get("tokenizer"),
            "reason": "response.usage records whole-prompt token totals, but the frozen artifacts do not identify a reproducible tokenizer for isolating the peer payload.",
        },
        "local_evidence_reference": characterize_evidence(
            cache_dir=cache_dir,
            source_repo=source_repo,
            protocol=protocol,
            frozen=frozen,
            v2_config=v2_config,
        ),
        "interpretation": "FoT communication in this experiment is limited to compact textual insight payloads rather than raw time-series observations.",
        "claim_boundary": "This is a payload characterization, not a demonstration of communication efficiency, compression efficiency, bandwidth optimality, or superior communication cost.",
        "assumptions": [
            "Characters are Python Unicode code points; bytes are UTF-8 bytes.",
            "The primary textual measure is the exact Condition-B peer block inserted by the frozen prompt builder.",
            "Raw observation counts include only the 41 XMEAS values in the post-injection [10 h, 50 h) windows actually feature-extracted; Time, XMV, cost, and the endpoint at 50 h are excluded.",
            "Dense float64 is an explicit theoretical reference serialization and is not the size of an XLSX file.",
            "The receiver-level primary denominator counts the fault-specific development experience of its three peers. The shared Normal N1-N5 normalization reference is reported separately and in an inclusive alternative denominator, counted once.",
            "Structured evidence counts the five non-duplicate numerical descriptors per window and XMEAS. It is upstream evidence; the insight-generation LLM directly received neutral text only.",
        ],
        "frozen_artifact_hash_verification": {
            "status": "PASS",
            "count": len(verified),
            "verified": verified,
        },
    }
    add_ratios(report)
    return report


def format_ratio(value: float) -> str:
    return f"{value:.12f}"


def render_markdown(report: dict[str, Any]) -> str:
    payload = report["actual_fot_textual_payload"]
    evidence = report["local_evidence_reference"]
    lines = [
        "# Communication Payload Characterization — Frozen Experiment 1",
        "",
        "Status: **descriptive only**. This report does not establish communication efficiency.",
        "",
        "## Actual FoT textual payload",
        "",
        "Primary measure: the exact Condition-B peer block inserted into a receiver prompt, serialized as `PEER INSIGHTS\\n` followed by indented UTF-8 JSON and two terminal newlines.",
        "",
        "| Receiver | Insights | Characters | UTF-8 bytes | Peer raw values | Dense float64 reference bytes | Text/raw | Raw/text |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    ev_by_receiver = {row["receiver"]: row for row in evidence["per_receiver_peer_sources"]}
    for row in payload["receivers"]:
        ev = ev_by_receiver[row["receiver"]]
        ratios = row["ratios"]["peer_fault_experience_only"]
        lines.append(
            f"| {row['receiver']} | {row['n_insights']} | {row['rendered_prompt_block']['chars']} | "
            f"{row['rendered_prompt_block']['utf8_bytes']} | {ev['peer_fault_raw_observation_values']} | "
            f"{ev['peer_fault_reference_dense_float64_bytes']} | {format_ratio(ratios['textual_to_raw'])} | "
            f"{ratios['reference_raw_to_text']:.2f} |"
        )

    unit = payload["all_receiver_unit"]
    full = payload["full_frozen_condition_b_execution"]
    unique = payload["unique_knowledge_stored"]
    lines.extend(
        [
            "",
            "An all-receiver Condition-B unit means one prompt invocation for each receiver: "
            f"{unit['total_insight_transmissions']} insight transmissions, {unit['chars']} characters, and {unit['utf8_bytes']} UTF-8 bytes. Each of the eight unique insights is delivered to exactly three receivers.",
            "",
            f"The frozen library stores {unique['n_unique_insights']} unique insights in "
            f"{unique['frozen_library_artifact']['utf8_bytes']} UTF-8 bytes as the exact JSON artifact. "
            "Stored unique knowledge and transmitted payload are therefore distinct quantities.",
            "",
            f"Across the complete frozen Condition-B execution ({full['heldout_cases']} cases × 4 receivers × R={full['repetitions']}), the peer blocks are transmitted in {full['prompt_calls']} calls: "
            f"{full['total_insight_transmissions']} insight transmissions and {full['utf8_bytes']} UTF-8 bytes. This is repetition across calls, not additional unique knowledge.",
            "",
            "## Token count",
            "",
            f"`{report['token_count']['status']}`",
            "",
            f"The frozen execution records `{report['token_count']['sdk_package']}=={report['token_count']['sdk_version']}` and whole-prompt accounting from `{report['token_count']['token_accounting_source']}`, but no payload tokenizer/encoding. Whole-prompt usage cannot be converted into an exact isolated peer-block token count without an identified tokenizer.",
            "",
            "## Local evidence reference",
            "",
            "Each source agent contributes five fixed development fault batches. A workbook contains 3001 rows from 0 to 50 h, but the frozen verbalizer feature-extracts only the left-closed/right-open post-injection interval [10 h, 50 h): 2400 samples, eight 5 h windows, and 41 XMEAS per batch.",
            "",
            "| Source agent | Batches | Consumed samples | XMEAS | Raw values | Dense float64 bytes | Structured feature values |",
            "|---|---:|---:|---:|---:|---:|---:|",
        ]
    )
    for row in evidence["per_source_agent"]:
        lines.append(
            f"| {row['source_agent']} | {row['n_development_batches']} | "
            f"{row['post_injection_samples_consumed_total']} | {row['xmeas_variables']} | "
            f"{row['raw_observation_values']} | {row['reference_dense_float64_bytes']} | "
            f"{row['structured_numerical_feature_values']} |"
        )
    shared = evidence["shared_normal_reference"]
    system = evidence["system_unique_source_evidence"]
    lines.extend(
        [
            "",
            "The structured count is `5 batches × 8 windows × 41 XMEAS × 5 descriptors = 8,200` per source agent. The five descriptors are `shift_sigma`, `slope_sigma_h`, `raw_std_ratio`, `diff_std_ratio`, and `residual_std_ratio`. Absolute-value duplicates, booleans, summaries, and text are not counted as independent numerical features.",
            "",
            f"The shared Normal N1-N5 reference contributes {shared['samples']} samples × {shared['xmeas_variables']} XMEAS = {shared['raw_observation_values']} raw values ({shared['reference_dense_float64_bytes']} dense-float64 reference bytes). It supplies normalization statistics and frozen calibration context; it is not peer fault-specific experience and is counted once in the inclusive alternative.",
            "",
            "Across all four source agents, unique fault-specific evidence is "
            f"{system['fault_raw_observation_values']} raw values ({system['fault_reference_dense_float64_bytes']} reference bytes) and {system['fault_structured_numerical_feature_values']} structured numerical feature values. Including shared Normal N1-N5 once gives "
            f"{system['fault_plus_shared_normal_raw_observation_values']} raw values ({system['fault_plus_shared_normal_reference_dense_float64_bytes']} reference bytes).",
            "",
            "## Ratios under the stated serialization convention",
            "",
            "Receiver-level primary formula:",
            "",
            "`rendered peer-block UTF-8 bytes / (three peers × five batches × 2400 samples × 41 XMEAS × 8 bytes)`",
            "",
            "This is the **textual-to-raw payload ratio under the stated serialization convention**. Its inverse is the **reference raw-to-text payload ratio**. It is not a lossless compression ratio.",
            "",
            "The shared-Normal-inclusive alternative adds `15000 × 41 × 8` bytes once to the receiver denominator; both variants are recorded in the machine-readable report.",
            "",
            "The unique-library formula is:",
            "",
            "`frozen final_local_insights.json UTF-8 bytes / (four agents × five batches × 2400 samples × 41 XMEAS × 8 bytes)`",
            "",
            f"Using fault-specific evidence only, this equals {format_ratio(unique['ratios']['fault_experience_only']['textual_to_raw'])}; the inverse is {unique['ratios']['fault_experience_only']['reference_raw_to_text']:.2f}. Including shared Normal N1-N5 once, it equals {format_ratio(unique['ratios']['fault_plus_shared_normal_once']['textual_to_raw'])}; the inverse is {unique['ratios']['fault_plus_shared_normal_once']['reference_raw_to_text']:.2f}.",
            "",
            "## Provenance and assumptions",
            "",
            "- Insight routing and serialization: `phase_b/conditions/builders.py`, `phase_b/insights/library.py`, and the four frozen `agent_*_B.json` peer libraries.",
            "- Insight sources: `phase_b/execution/generate_final_insights.py`, four `phase_b/insights/input_bundles/agent_*.json`, and `phase_b/insights/generation_runs.json`.",
            "- Batch scope and topology: `phase_b/config/phase_b_protocol_frozen.json` and `phase_b/PHASE_B_PROTOCOL_FREEZE.md`.",
            "- Windowing and variables: `code/tep_verbalize_v2.py`, `code/tep_features.py`, and `code/verbalizer_config_v2.json`.",
            "- Dataset source snapshot: `309b944f35ac440ff0c70616947ffe723c766e14`.",
            "- All 20 development fault workbooks and the Normal workbook were matched byte-for-byte to the SHA-256 and size recorded in their Git-LFS pointers at the pinned dataset commit.",
            "- Theoretical dense float64 payload is `raw XMEAS value count × 8 bytes`; XLSX file sizes are not used in any ratio.",
            "- Pre-injection samples, Time, XMV, and cost columns are not counted because the frozen feature pipeline does not consume them as XMEAS feature evidence for these insight texts.",
            "- The insight-generation LLM received neutral text only (`contains_structured_numerical_json=false`), not the upstream numerical JSON.",
            "",
            "## Interpretation",
            "",
            report["interpretation"],
            "",
            report["claim_boundary"],
            "",
            "## Validation",
            "",
            f"- Frozen artifact hashes verified: PASS ({report['frozen_artifact_hash_verification']['count']} artifacts).",
            "- Pinned dataset Git-LFS workbook matches: PASS (21/21).",
            "- Exactly 8 unique insights: PASS.",
            "- Exactly 6 peer insights per receiver: PASS.",
            "- No self or Normal insight routed: PASS.",
            "- Every unique insight delivered to exactly 3 receivers: PASS.",
            "",
        ]
    )
    return "\n".join(lines)


def write_outputs(report: dict[str, Any], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "communication_payload_report.json"
    md_path = output_dir / "COMMUNICATION_PAYLOAD_REPORT.md"
    json_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    md_path.write_text(render_markdown(report), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache-dir", type=Path, default=DEFAULT_CACHE)
    parser.add_argument("--source-repo", type=Path, default=DEFAULT_SOURCE_REPO)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument(
        "--stdout-json",
        action="store_true",
        help="print the report instead of writing output files",
    )
    args = parser.parse_args()
    report = build_report(args.cache_dir.resolve(), args.source_repo.resolve())
    if args.stdout_json:
        print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    else:
        write_outputs(report, args.output_dir.resolve())
        print(f"Wrote communication payload characterization to {args.output_dir.resolve()}")


if __name__ == "__main__":
    main()
