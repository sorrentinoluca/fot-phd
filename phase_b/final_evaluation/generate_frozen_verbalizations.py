#!/usr/bin/env python3
"""Generate label-blind frozen V2 artifacts for the 15 Phase B held-out cases."""

from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import re
import sys
from typing import Any

import pandas as pd


ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "code"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

from phase_b.prompts.leakage import scan_text  # noqa: E402
from tep_features import XMEAS, load_case  # noqa: E402
from tep_verbalize_v2 import (  # noqa: E402
    load_config,
    load_development_baseline,
    render_text,
    verbalize_case,
)


PROTOCOL_FREEZE_COMMIT = "3d86f64d43e14e7e0de520cb047ca1043bf9c1c0"
MANIFEST_PATH = ROOT / "phase_b/heldout/phase_b_heldout_manifest.csv"
DATA_DIR = ROOT / "tep_heldout/mode1"
CONFIG_PATH = CODE / "verbalizer_config_v2.json"
VERBALIZER_PATH = CODE / "tep_verbalize_v2.py"
FEATURES_PATH = CODE / "tep_features.py"
EVALUATOR_PATH = CODE / "evaluate_verbalizer_v2.py"
BASELINE_PATH = CODE / "tep_cache/mode1_normal_500.xlsx"
OUTPUT_ROOT = ROOT / "phase_b/final_evaluation"
STRUCTURED_DIR = OUTPUT_ROOT / "verbalized/structured"
NEUTRAL_DIR = OUTPUT_ROOT / "verbalized/neutral_text"
EVALUATOR_DIR = OUTPUT_ROOT / "evaluator_side"
OUTPUT_MANIFEST_PATH = OUTPUT_ROOT / "heldout_verbalizations_manifest.json"
SOURCE_MAPPING_PATH = EVALUATOR_DIR / "heldout_source_mapping.json"
PHASE_A_HASHES = {
    "code/verbalizer_config_v2.json": "552a0b8a9cf9e416de77daa7aca2d8dee152a2700bbfaab4ae5e039081712519",
    "code/tep_verbalize_v2.py": "3a9129b6353cac6f8c9e02281282f137dd07885b1f882ca633ee9d6bf52393be",
    "code/evaluate_verbalizer_v2.py": "972e06fa29bee5a58d57ca757bd158c5cddaa2f4ed12eb5c739169c7fef79a92",
    "code/tep_features.py": "cbade7a295dfae6550df7ecbe35fa2be1f844b63c4c528ec194f95a20961040c",
}
PROMPT_FACING_FORBIDDEN = (
    re.compile(r"\bCLS-[A-Z0-9]{5}\b"),
    re.compile(r"\bmode1_", re.IGNORECASE),
)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def write_json(path: Path, value: Any) -> None:
    serialized = json.dumps(
        value,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        allow_nan=False,
    ) + "\n"
    write_text(path, serialized)


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT))


def verify_phase_a_hashes() -> None:
    for path_text, expected in PHASE_A_HASHES.items():
        path = ROOT / path_text
        if sha256_file(path) != expected:
            raise RuntimeError(f"Phase A frozen hash mismatch: {path_text}")


def load_heldout_rows() -> list[dict[str, str]]:
    with MANIFEST_PATH.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    case_ids = [row["case_id"] for row in rows]
    filenames = [row["filename"] for row in rows]
    if len(rows) != 15 or len(set(case_ids)) != 15 or len(set(filenames)) != 15:
        raise RuntimeError("held-out manifest must contain 15 unique cases and files")
    if case_ids != [f"PBH-{index:03d}" for index in range(1, 16)]:
        raise RuntimeError("held-out cases are not in the frozen PBH-001..PBH-015 order")
    return rows


def verify_all_inputs(rows: list[dict[str, str]]) -> dict[str, Path]:
    sources: dict[str, Path] = {}
    for row in rows:
        case_id = row["case_id"]
        source = DATA_DIR / row["filename"]
        if not source.is_file():
            raise RuntimeError(f"missing frozen held-out input for {case_id}")
        if source.stat().st_size != int(row["size_bytes"]):
            raise RuntimeError(f"held-out size mismatch for {case_id}")
        if sha256_file(source) != row["sha256"]:
            raise RuntimeError(f"held-out SHA-256 mismatch for {case_id}")
        sources[case_id] = source
    return sources


def assert_label_blind(text: str, *, case_id: str, source_filename: str) -> None:
    if scan_text(text, source=case_id):
        raise RuntimeError(f"real-class leakage in neutral text for {case_id}")
    if source_filename.lower() in text.lower():
        raise RuntimeError(f"source filename leakage in neutral text for {case_id}")
    if any(pattern.search(text) for pattern in PROMPT_FACING_FORBIDDEN):
        raise RuntimeError(f"evaluator-side token leakage in neutral text for {case_id}")


def validate_v2_result(result: dict[str, Any], config: dict[str, Any]) -> None:
    if set(result) != {"structured", "text"}:
        raise RuntimeError("V2 result keys differ from the frozen interface")
    structured = result["structured"]
    expected_keys = {
        "verbalizer_version",
        "dataset_commit",
        "time_range_h",
        "window_hours",
        "n_windows",
        "phase_definition",
        "phase_window_counts",
        "thresholds",
        "variables",
        "system_summary",
    }
    if not isinstance(structured, dict) or set(structured) != expected_keys:
        raise RuntimeError("structured V2 top-level schema mismatch")
    if structured["verbalizer_version"] != config["version"]:
        raise RuntimeError("structured V2 version mismatch")
    if structured["thresholds"] != config["thresholds"]:
        raise RuntimeError("structured V2 thresholds differ from frozen config")
    if structured["n_windows"] != 8 or structured["time_range_h"] != [10.0, 50.0]:
        raise RuntimeError("structured V2 held-out window geometry mismatch")
    if set(structured["variables"]) != set(XMEAS):
        raise RuntimeError("structured V2 output does not contain all 41 XMEAS")
    if not isinstance(result["text"], str) or not result["text"].strip():
        raise RuntimeError("neutral text is empty")
    if render_text(structured) != result["text"]:
        raise RuntimeError("neutral text is not the frozen renderer output")
    json.dumps(structured, ensure_ascii=False, allow_nan=False)


def assert_no_existing_outputs() -> None:
    protected = [OUTPUT_MANIFEST_PATH, SOURCE_MAPPING_PATH]
    protected.extend(STRUCTURED_DIR.glob("PBH-*.json"))
    protected.extend(NEUTRAL_DIR.glob("PBH-*.txt"))
    if any(path.exists() for path in protected):
        raise RuntimeError("held-out verbalization artifacts already exist; refusing overwrite")


def main() -> int:
    assert_no_existing_outputs()
    verify_phase_a_hashes()
    rows = load_heldout_rows()
    sources = verify_all_inputs(rows)

    config = load_config(CONFIG_PATH)
    baseline = load_development_baseline(BASELINE_PATH, config)
    generated_at = datetime.now(timezone.utc).isoformat()
    results: dict[str, dict[str, Any]] = {}

    for row in rows:
        case_id = row["case_id"]
        result = verbalize_case(
            load_case(sources[case_id]),
            baseline,
            config=config,
            end_h=50.0,
        )
        validate_v2_result(result, config)
        assert_label_blind(
            result["text"],
            case_id=case_id,
            source_filename=row["filename"],
        )
        results[case_id] = result

    source_mapping = {
        "artifact_version": "1",
        "scope": "EVALUATOR_SIDE_ONLY",
        "source_manifest": relative(MANIFEST_PATH),
        "source_manifest_sha256": sha256_file(MANIFEST_PATH),
        "cases": [
            {
                "physical_case_id": row["case_id"],
                "source_filename": row["filename"],
                "source_file_sha256": row["sha256"],
            }
            for row in rows
        ],
    }
    write_json(SOURCE_MAPPING_PATH, source_mapping)

    entries: list[dict[str, Any]] = []
    for row in rows:
        case_id = row["case_id"]
        structured_path = STRUCTURED_DIR / f"{case_id}.json"
        neutral_path = NEUTRAL_DIR / f"{case_id}.txt"
        write_json(structured_path, results[case_id]["structured"])
        write_text(neutral_path, results[case_id]["text"].strip() + "\n")
        entries.append(
            {
                "physical_case_id": case_id,
                "source_file_sha256": row["sha256"],
                "frozen_v2_hashes": dict(PHASE_A_HASHES),
                "structured_output_path": relative(structured_path),
                "structured_output_sha256": sha256_file(structured_path),
                "neutral_text_path": relative(neutral_path),
                "neutral_text_sha256": sha256_file(neutral_path),
                "generated_at_utc": generated_at,
            }
        )

    output_manifest = {
        "artifact_version": "1",
        "status": "FROZEN_V2_HELDOUT_VERBALIZATIONS_COMPLETE",
        "protocol_freeze_commit": PROTOCOL_FREEZE_COMMIT,
        "case_count": 15,
        "diagnostic_input_contract": "neutral_text_only",
        "structured_json_is_diagnostic_input": False,
        "input_manifest_path": relative(MANIFEST_PATH),
        "input_manifest_sha256": sha256_file(MANIFEST_PATH),
        "baseline_source_sha256": sha256_file(BASELINE_PATH),
        "evaluator_side_source_mapping_path": relative(SOURCE_MAPPING_PATH),
        "evaluator_side_source_mapping_sha256": sha256_file(SOURCE_MAPPING_PATH),
        "runtime": {
            "python": platform.python_version(),
            "pandas": pd.__version__,
        },
        "generated_at_utc": generated_at,
        "cases": entries,
    }
    write_json(OUTPUT_MANIFEST_PATH, output_manifest)

    for entry in entries:
        if sha256_file(ROOT / entry["structured_output_path"]) != entry[
            "structured_output_sha256"
        ]:
            raise RuntimeError("structured output hash verification failed")
        if sha256_file(ROOT / entry["neutral_text_path"]) != entry[
            "neutral_text_sha256"
        ]:
            raise RuntimeError("neutral text hash verification failed")

    print(
        json.dumps(
            {
                "cases_verbalized": len(entries),
                "structured_outputs": len(entries),
                "neutral_texts": len(entries),
                "leakage": "PASS",
                "input_sha256": "PASS",
                "frozen_v2_hashes": "PASS",
                "output_hashes": "PASS",
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
