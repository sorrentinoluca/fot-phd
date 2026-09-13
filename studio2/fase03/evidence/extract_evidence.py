#!/usr/bin/env python3
"""Extract neutral, per-window 697-D evidence from the fault-development manifest."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib
import json
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

try:
    from .leakage import assert_no_leakage
except ImportError:  # Direct execution from this directory.
    from leakage import assert_no_leakage


EXPECTED_SOURCE_PATHS = (
    "code/tep_features.py",
    "code/tep_verbalize_v2.py",
    "code/verbalizer_config_v2.json",
    "code/evaluate_verbalizer_v2.py",
)
ONSET_H = 25.0
END_H = 65.0
WINDOW_H = 5.0
EXPECTED_RUNS = 40
EXPECTED_WINDOWS_PER_RUN = 8
SIGNATURE_DIMENSION = 697
EXPECTED_BASELINE_SHA256 = (
    "79883dd0aabbd034c15337b0be1ffca37e59ea7b32443a15d560b7feda2b2e6a"
)
EXPECTED_R2_GUARD_SHA256 = (
    "7df0cef2d7854c689b79eb911fa01d1ede1625e22f0d3636c0ea5d678c9f33f8"
)


@dataclass(frozen=True)
class FrozenApi:
    pd: Any
    xmeas: list[str]
    load_case: Any
    analyze_case_windows: Any
    compute_baseline_stats_from_blocks: Any
    load_config: Any
    load_development_baseline: Any
    verbalize_feature_table: Any
    signature_vector: Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def protocol_hashes(repo_root: Path) -> dict[str, str]:
    manifest_path = repo_root / "phase_b" / "PHASE_B_PROTOCOL_HASHES.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    artifacts = manifest.get("artifacts", {})
    missing = [path for path in EXPECTED_SOURCE_PATHS if path not in artifacts]
    if missing:
        raise RuntimeError(f"Protocol hash manifest is missing: {missing}")
    return {path: str(artifacts[path]) for path in EXPECTED_SOURCE_PATHS}


def verify_frozen_sources(
    repo_root: Path,
    *,
    code_dir: Path | None = None,
    expected: dict[str, str] | None = None,
) -> dict[str, str]:
    """Verify all frozen bytes before any frozen module is imported."""
    source_dir = code_dir if code_dir is not None else repo_root / "code"
    expected_hashes = protocol_hashes(repo_root) if expected is None else expected
    actual: dict[str, str] = {}
    mismatches: list[str] = []
    for relative in EXPECTED_SOURCE_PATHS:
        path = source_dir / Path(relative).name
        if not path.is_file():
            mismatches.append(f"{relative}: missing at {path}")
            continue
        digest = sha256_file(path)
        actual[relative] = digest
        if digest != expected_hashes.get(relative):
            mismatches.append(
                f"{relative}: expected {expected_hashes.get(relative)}, got {digest}"
            )
    if mismatches:
        raise RuntimeError("Frozen source guard failed: " + "; ".join(mismatches))
    return actual


def load_frozen_api(repo_root: Path) -> FrozenApi:
    verify_frozen_sources(repo_root)
    code_dir = repo_root / "code"
    if str(code_dir) not in sys.path:
        sys.path.insert(0, str(code_dir))
    features = importlib.import_module("tep_features")
    verbalizer = importlib.import_module("tep_verbalize_v2")
    evaluator = importlib.import_module("evaluate_verbalizer_v2")
    pd = importlib.import_module("pandas")
    return FrozenApi(
        pd=pd,
        xmeas=list(features.XMEAS),
        load_case=features.load_case,
        analyze_case_windows=features.analyze_case_windows,
        compute_baseline_stats_from_blocks=features.compute_baseline_stats_from_blocks,
        load_config=verbalizer.load_config,
        load_development_baseline=verbalizer.load_development_baseline,
        verbalize_feature_table=verbalizer.verbalize_feature_table,
        signature_vector=evaluator.signature_vector,
    )


def read_manifest(path: Path, *, require_full_campaign: bool = True) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if require_full_campaign and len(rows) != EXPECTED_RUNS:
        raise ValueError(f"Expected {EXPECTED_RUNS} manifest rows, got {len(rows)}")
    run_ids = [row.get("run_id", "") for row in rows]
    if len(run_ids) != len(set(run_ids)) or any(not value for value in run_ids):
        raise ValueError("Manifest run_id values must be non-empty and unique")
    for row in rows:
        if row.get("status") != "complete":
            raise ValueError(f"{row['run_id']}: status is not complete")
        if int(row.get("useful_windows_complete", "-1")) != EXPECTED_WINDOWS_PER_RUN:
            raise ValueError(f"{row['run_id']}: expected eight complete windows")
        if not row.get("output_sha256"):
            raise ValueError(f"{row['run_id']}: missing output_sha256")
    return sorted(rows, key=lambda row: row["run_id"])


def resolve_source(row: dict[str, str], *, runs_root: Path | None) -> Path:
    declared = Path(row["output_path"])
    path = runs_root / declared.name if runs_root is not None else declared
    if not path.is_file():
        raise FileNotFoundError(f"{row['run_id']}: source CSV not found: {path}")
    digest = sha256_file(path)
    if digest != row["output_sha256"]:
        raise RuntimeError(
            f"{row['run_id']}: source hash mismatch; expected "
            f"{row['output_sha256']}, got {digest}"
        )
    return path


def verify_run_manifest(row: dict[str, str], source: Path) -> None:
    """Cross-check the immutable per-run manifest when the aggregate declares it."""
    expected_hash = row.get("manifest_sha256")
    if not expected_hash:
        return
    manifest_path = source.with_suffix(".manifest.json")
    if not manifest_path.is_file():
        raise FileNotFoundError(
            f"{row['run_id']}: per-run manifest not found: {manifest_path}"
        )
    actual_hash = sha256_file(manifest_path)
    if actual_hash != expected_hash:
        raise RuntimeError(
            f"{row['run_id']}: per-run manifest hash mismatch; expected "
            f"{expected_hash}, got {actual_hash}"
        )
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_values = {
        "run_id": row["run_id"],
        "status": "complete",
        "stream_id": row["stream_id"],
        "idv": int(row["idv"]),
        "onset_h": ONSET_H,
        "horizon_h": END_H - ONSET_H,
        "stop_time_h": END_H,
        "window_h": WINDOW_H,
        "useful_windows_complete": EXPECTED_WINDOWS_PER_RUN,
        "sha256": row["output_sha256"],
    }
    mismatches = {
        key: (payload.get(key), value)
        for key, value in expected_values.items()
        if payload.get(key) != value
    }
    post_windows = payload.get("post_fault_windows")
    expected_windows = [
        {
            "start_h": int(ONSET_H + index * WINDOW_H),
            "end_h": int(ONSET_H + (index + 1) * WINDOW_H),
            "development_eligible": True,
            "complete": True,
        }
        for index in range(EXPECTED_WINDOWS_PER_RUN)
    ]
    if post_windows != expected_windows:
        mismatches["post_fault_windows"] = (post_windows, expected_windows)
    if mismatches:
        raise RuntimeError(f"{row['run_id']}: per-run manifest mismatch: {mismatches}")


def validate_r2_guard(path: Path) -> dict[str, Any]:
    digest = sha256_file(path)
    if digest != EXPECTED_R2_GUARD_SHA256:
        raise RuntimeError(
            f"R2 guard hash mismatch: expected {EXPECTED_R2_GUARD_SHA256}, got {digest}"
        )
    payload = json.loads(path.read_text(encoding="utf-8"))
    required_true = (
        "r2_guard_result_independent_byte_identical",
        "parameters_and_code_current",
        "guard_pass",
    )
    failed = [key for key in required_true if payload.get(key) is not True]
    if failed:
        raise RuntimeError(f"R2 guard is not valid: {failed}")
    if payload.get("tep_features_sha256") != protocol_hashes(
        Path(__file__).resolve().parents[3]
    )["code/tep_features.py"]:
        raise RuntimeError("R2 guard and frozen tep_features.py disagree")
    return payload


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(
            value,
            ensure_ascii=False,
            sort_keys=True,
            indent=2,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )


def _write_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def _artifact_record(root: Path, path: Path) -> tuple[str, str, int]:
    return str(path.relative_to(root)), sha256_file(path), path.stat().st_size


def extract_rows(
    *,
    repo_root: Path,
    api: FrozenApi,
    rows: list[dict[str, str]],
    baseline: Any,
    output_dir: Path,
    runs_root: Path | None = None,
    baseline_provenance: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if output_dir.exists():
        raise FileExistsError(f"Output directory already exists: {output_dir}")
    temp_dir = output_dir.with_name(output_dir.name + ".partial")
    if temp_dir.exists():
        raise FileExistsError(f"Partial output directory already exists: {temp_dir}")
    units_dir = temp_dir / "units"
    units_dir.mkdir(parents=True)
    config_path = repo_root / "code" / "verbalizer_config_v2.json"
    config = api.load_config(config_path)
    if float(config["window_hours"]) != WINDOW_H:
        raise RuntimeError("Frozen config window_hours is no longer 5.0")

    manifest_rows: list[dict[str, Any]] = []
    index_rows: list[dict[str, Any]] = []
    visible_paths: list[Path] = []
    evidence_counter = 0
    try:
        for row in rows:
            source = resolve_source(row, runs_root=runs_root)
            verify_run_manifest(row, source)
            case = api.load_case(source)
            features = api.analyze_case_windows(
                case,
                baseline,
                start_h=ONSET_H,
                end_h=END_H,
                window_h=WINDOW_H,
            )
            starts = sorted(float(value) for value in features.window_start_h.unique())
            if len(starts) != EXPECTED_WINDOWS_PER_RUN:
                raise RuntimeError(
                    f"{row['run_id']}: expected 8 extracted windows, got {len(starts)}"
                )
            for ordinal, start_h in enumerate(starts, start=1):
                evidence_counter += 1
                evidence_id = f"EVD-{evidence_counter:04d}"
                unit = features[features.window_start_h == start_h].copy()
                unit = unit.sort_values(
                    "variable",
                    key=lambda series: series.map(
                        {name: index for index, name in enumerate(api.xmeas)}
                    ),
                )
                result = api.verbalize_feature_table(unit, config)
                signature = api.signature_vector(result["structured"])
                if signature.shape != (SIGNATURE_DIMENSION,):
                    raise RuntimeError(
                        f"{evidence_id}: signature shape is {signature.shape}, not (697,)"
                    )

                stem = units_dir / evidence_id
                feature_path = stem.with_suffix(".features.csv")
                json_path = stem.with_suffix(".evidence.json")
                text_path = stem.with_suffix(".txt")
                signature_path = stem.with_suffix(".signature.csv")
                unit.to_csv(feature_path, index=False, lineterminator="\n")
                _write_json(json_path, result["structured"])
                text_path.write_text(result["text"] + "\n", encoding="utf-8")
                _write_csv(
                    signature_path,
                    ["component", "value"],
                    (
                        {"component": index, "value": format(float(value), ".17g")}
                        for index, value in enumerate(signature)
                    ),
                )
                visible_paths.extend((json_path, text_path))

                artifacts: dict[str, Any] = {}
                for label, path in (
                    ("feature", feature_path),
                    ("json", json_path),
                    ("text", text_path),
                    ("signature", signature_path),
                ):
                    rel, digest, size = _artifact_record(temp_dir, path)
                    artifacts[f"{label}_path"] = rel
                    artifacts[f"{label}_sha256"] = digest
                    artifacts[f"{label}_bytes"] = size
                manifest_rows.append(
                    {
                        "evidence_id": evidence_id,
                        "window_ordinal": ordinal,
                        "signature_dimension": len(signature),
                        "leakage_pass": "pending",
                        "baseline_sha256": (
                            baseline_provenance or {}
                        ).get("baseline_sha256", "synthetic"),
                        "r2_guard_sha256": (
                            baseline_provenance or {}
                        ).get("r2_guard_sha256", "synthetic"),
                        "regenerate_if_r2_fails": "true",
                        **artifacts,
                    }
                )
                index_rows.append(
                    {
                        "evidence_id": evidence_id,
                        "run_id": row["run_id"],
                        "fault": f"F{int(row['idv'])}",
                        "batch": int(row["run_id"].rsplit("b", 1)[1]),
                        "stream_id": row["stream_id"],
                        "window_ordinal": ordinal,
                        "window_start_h": format(start_h, ".1f"),
                        "window_end_h": format(start_h + WINDOW_H, ".1f"),
                        "source_path": str(
                            Path("studio2/fase03/fault_runs/runs/fault_dev_001")
                            / source.name
                        ),
                        "source_sha256": row["output_sha256"],
                        "source_manifest_sha256": row.get("manifest_sha256", ""),
                    }
                )

        findings = []
        try:
            assert_no_leakage(visible_paths)
        except ValueError as exc:
            findings.append(str(exc))
        if findings:
            raise RuntimeError("; ".join(findings))
        for item in manifest_rows:
            item["leakage_pass"] = "true"

        manifest_fields = list(manifest_rows[0]) if manifest_rows else []
        index_fields = list(index_rows[0]) if index_rows else []
        manifest_path = temp_dir / "EVIDENCE_MANIFEST.csv"
        index_path = temp_dir / "EVALUATOR_INDEX.csv"
        _write_csv(manifest_path, manifest_fields, manifest_rows)
        _write_csv(index_path, index_fields, index_rows)
        summary = {
            "run_count": len(rows),
            "evidence_unit_count": evidence_counter,
            "files_per_unit": 4,
            "consumer_visible_json_text_leakage": "PASS",
            "signature_dimension": SIGNATURE_DIMENSION,
            "onset_h": ONSET_H,
            "end_h": END_H,
            "window_h": WINDOW_H,
            "windows_per_run": EXPECTED_WINDOWS_PER_RUN,
            "baseline_provenance": baseline_provenance or {
                "scope": "synthetic_fixture_only"
            },
            "regeneration_rule": (
                "All evidence is invalid and must be regenerated if the R2 guard fails "
                "or the study switches to baseline_fit_new."
            ),
            "evidence_manifest_sha256": sha256_file(manifest_path),
            "evaluator_index_sha256": sha256_file(index_path),
        }
        _write_json(temp_dir / "EXTRACTION_SUMMARY.json", summary)
        temp_dir.rename(output_dir)
        return summary
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--normal", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--runs-root", type=Path)
    parser.add_argument("--r2-guard", type=Path, required=True)
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[3]
    api = load_frozen_api(repo_root)
    config_path = repo_root / "code" / "verbalizer_config_v2.json"
    config = api.load_config(config_path)
    baseline_hash = sha256_file(args.normal)
    if baseline_hash != EXPECTED_BASELINE_SHA256:
        raise RuntimeError(
            f"Legacy baseline hash mismatch: expected {EXPECTED_BASELINE_SHA256}, "
            f"got {baseline_hash}"
        )
    validate_r2_guard(args.r2_guard)
    baseline = api.load_development_baseline(args.normal, config)
    rows = read_manifest(args.manifest, require_full_campaign=True)
    summary = extract_rows(
        repo_root=repo_root,
        api=api,
        rows=rows,
        baseline=baseline,
        output_dir=args.output,
        runs_root=args.runs_root,
        baseline_provenance={
            "authorization": "U3 extension of U1/R2, author decision 2026-09-13",
            "role": "normalization and frozen V2 verbalizer flags only",
            "baseline_sha256": baseline_hash,
            "verbalizer_config_sha256": sha256_file(config_path),
            "r2_guard_sha256": sha256_file(args.r2_guard),
            "r2_guard_required": True,
            "score_threshold_source": "new Normal runs from phase 03.5; not this baseline",
        },
    )
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
