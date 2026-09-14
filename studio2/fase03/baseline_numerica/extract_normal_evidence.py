#!/usr/bin/env python3
"""Extract Normal evidence through the hash-verified Phase 03.6 implementation."""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Any


EXPECTED_EXTRACTOR_SHA256 = (
    "46b451c2d6d8b1627993828ac9bac39532562f2fa1b27955b8a20f098ba24e97"
)
EXPECTED_LEAKAGE_SHA256 = (
    "c77ae5b11186c5b0df87b2f1df8800cb45fb25317e248fe8484d3e8283073887"
)
EXPECTED_RUNS = 40
EXPECTED_WINDOWS_PER_RUN = 8
EXPECTED_DIMENSION = 697


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def load_verified_extractor(path: Path) -> ModuleType:
    path = path.resolve()
    leakage_path = path.with_name("leakage.py")
    expected = {
        path: EXPECTED_EXTRACTOR_SHA256,
        leakage_path: EXPECTED_LEAKAGE_SHA256,
    }
    mismatches = [
        f"{item}: expected {digest}, got {sha256_file(item) if item.is_file() else 'missing'}"
        for item, digest in expected.items()
        if not item.is_file() or sha256_file(item) != digest
    ]
    if mismatches:
        raise RuntimeError("Phase 03.6 extractor guard failed: " + "; ".join(mismatches))
    sys.path.insert(0, str(path.parent))
    try:
        spec = importlib.util.spec_from_file_location("fase03_6_extract_evidence", path)
        if spec is None or spec.loader is None:
            raise RuntimeError(f"cannot load extractor: {path}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        try:
            spec.loader.exec_module(module)
        except Exception:
            sys.modules.pop(spec.name, None)
            raise
        return module
    finally:
        sys.path.pop(0)


def validated_campaign(
    *,
    plan_path: Path,
    manifest_path: Path,
    runs_root: Path,
    audit_path: Path,
) -> list[dict[str, Any]]:
    plan = read_csv(plan_path)
    manifest = read_csv(manifest_path)
    if len(plan) != EXPECTED_RUNS or len(manifest) != EXPECTED_RUNS:
        raise RuntimeError("normal_dev requires exactly 40 plan and manifest rows")
    plan_by_run = {row["run_id"]: row for row in plan}
    manifest_by_run = {row["run_id"]: row for row in manifest}
    if len(plan_by_run) != EXPECTED_RUNS or set(plan_by_run) != set(manifest_by_run):
        raise RuntimeError("plan and generation manifest run_id sets differ")

    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    summary = audit.get("summary", {})
    if not (
        summary.get("technical_result") == "PASS"
        and summary.get("valid_runs") == EXPECTED_RUNS
        and summary.get("valid_windows") == EXPECTED_RUNS * EXPECTED_WINDOWS_PER_RUN
    ):
        raise RuntimeError("normal_dev technical audit is not PASS 40/40 and 320/320")
    audit_runs = {row["run_id"]: row for row in audit.get("runs", [])}
    if set(audit_runs) != set(plan_by_run):
        raise RuntimeError("audit and plan run_id sets differ")

    joined: list[dict[str, Any]] = []
    for run_id in sorted(plan_by_run):
        planned = plan_by_run[run_id]
        generated = manifest_by_run[run_id]
        audited = audit_runs[run_id]
        source = (runs_root / f"{run_id}.xlsx").resolve()
        expected_values = {
            "set_name": "normal_dev",
            "stream_id": planned["stream_id"],
            "status": "complete",
            "stop_time_h": "65",
        }
        mismatches = {
            key: (generated.get(key), value)
            for key, value in expected_values.items()
            if generated.get(key) != value
        }
        if mismatches:
            raise RuntimeError(f"{run_id}: plan/manifest mismatch: {mismatches}")
        actual_sha256 = sha256_file(source)
        if actual_sha256 != generated.get("sha256"):
            raise RuntimeError(f"{run_id}: workbook hash differs from generation manifest")
        if actual_sha256 != audited.get("sha256_actual") or audited.get("status") != "PASS":
            raise RuntimeError(f"{run_id}: workbook differs from technical audit")
        joined.append(
            {
                "run_id": run_id,
                "agent_id": planned["agent_id"],
                "agent_run_index": int(planned["agent_run_index"]),
                "stream_id": generated["stream_id"],
                "source": source,
                "source_sha256": actual_sha256,
            }
        )
    expected_agents = {f"agent_{index}" for index in range(1, 9)}
    if {row["agent_id"] for row in joined} != expected_agents:
        raise RuntimeError("normal_dev agent coverage differs from eight agents")
    for agent in expected_agents:
        local = [row for row in joined if row["agent_id"] == agent]
        if {row["agent_run_index"] for row in local} != set(range(1, 6)):
            raise RuntimeError(f"{agent}: expected local run indices 1..5")
    return joined


def extract_normal(
    *,
    repo_root: Path,
    extractor: ModuleType,
    campaign: list[dict[str, Any]],
    normal_path: Path,
    r2_guard_path: Path,
    output_dir: Path,
    source_release: str,
) -> dict[str, Any]:
    api = extractor.load_frozen_api(repo_root)
    config_path = repo_root / "code" / "verbalizer_config_v2.json"
    config = api.load_config(config_path)
    baseline_sha256 = extractor.sha256_file(normal_path)
    if baseline_sha256 != extractor.EXPECTED_BASELINE_SHA256:
        raise RuntimeError("legacy baseline hash mismatch")
    extractor.validate_r2_guard(r2_guard_path)
    baseline = api.load_development_baseline(normal_path, config)

    if output_dir.exists():
        raise FileExistsError(f"output directory already exists: {output_dir}")
    partial = output_dir.with_name(output_dir.name + ".partial")
    if partial.exists():
        raise FileExistsError(f"partial output directory already exists: {partial}")
    units_dir = partial / "units"
    units_dir.mkdir(parents=True)
    manifest_rows: list[dict[str, Any]] = []
    index_rows: list[dict[str, Any]] = []
    visible_paths: list[Path] = []
    counter = 0
    try:
        for row in campaign:
            case = api.load_case(row["source"])
            features = api.analyze_case_windows(
                case,
                baseline,
                start_h=extractor.ONSET_H,
                end_h=extractor.END_H,
                window_h=extractor.WINDOW_H,
            )
            starts = sorted(float(value) for value in features.window_start_h.unique())
            if len(starts) != EXPECTED_WINDOWS_PER_RUN:
                raise RuntimeError(f"{row['run_id']}: expected eight evidence windows")
            for ordinal, start_h in enumerate(starts, start=1):
                counter += 1
                evidence_id = f"NDEV-EVD-{counter:04d}"
                unit = features[features.window_start_h == start_h].copy()
                unit = unit.sort_values(
                    "variable",
                    key=lambda series: series.map(
                        {name: index for index, name in enumerate(api.xmeas)}
                    ),
                )
                result = api.verbalize_feature_table(unit, config)
                signature = api.signature_vector(result["structured"])
                if signature.shape != (EXPECTED_DIMENSION,):
                    raise RuntimeError(f"{evidence_id}: signature is not 697-D")

                stem = units_dir / evidence_id
                feature_path = stem.with_suffix(".features.csv")
                json_path = stem.with_suffix(".evidence.json")
                text_path = stem.with_suffix(".txt")
                signature_path = stem.with_suffix(".signature.csv")
                unit.to_csv(feature_path, index=False, lineterminator="\n")
                extractor._write_json(json_path, result["structured"])
                text_path.write_text(result["text"] + "\n", encoding="utf-8")
                extractor._write_csv(
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
                    relative, digest, size = extractor._artifact_record(partial, path)
                    artifacts[f"{label}_path"] = relative
                    artifacts[f"{label}_sha256"] = digest
                    artifacts[f"{label}_bytes"] = size
                manifest_rows.append(
                    {
                        "evidence_id": evidence_id,
                        "window_ordinal": ordinal,
                        "signature_dimension": len(signature),
                        "leakage_pass": "pending",
                        "baseline_sha256": baseline_sha256,
                        "r2_guard_sha256": extractor.sha256_file(r2_guard_path),
                        "regenerate_if_r2_fails": "true",
                        **artifacts,
                    }
                )
                index_rows.append(
                    {
                        "evidence_id": evidence_id,
                        "run_id": row["run_id"],
                        "agent_id": row["agent_id"],
                        "agent_run_index": row["agent_run_index"],
                        "class_identifier": "Normal",
                        "stream_id": row["stream_id"],
                        "window_ordinal": ordinal,
                        "window_start_h": format(start_h, ".1f"),
                        "window_end_h": format(start_h + extractor.WINDOW_H, ".1f"),
                        "local_example_03_10": str(
                            row["agent_run_index"] == 1 and ordinal == 1
                        ).lower(),
                        "source_path": str(row["source"].relative_to(repo_root)),
                        "source_sha256": row["source_sha256"],
                    }
                )

        extractor.assert_no_leakage(visible_paths)
        for item in manifest_rows:
            item["leakage_pass"] = "true"
        manifest_path = partial / "EVIDENCE_MANIFEST.csv"
        index_path = partial / "EVALUATOR_INDEX.csv"
        extractor._write_csv(manifest_path, list(manifest_rows[0]), manifest_rows)
        extractor._write_csv(index_path, list(index_rows[0]), index_rows)
        summary = {
            "run_count": len(campaign),
            "evidence_unit_count": counter,
            "files_per_unit": 4,
            "consumer_visible_json_text_leakage": "PASS",
            "signature_dimension": EXPECTED_DIMENSION,
            "onset_h": extractor.ONSET_H,
            "end_h": extractor.END_H,
            "window_h": extractor.WINDOW_H,
            "windows_per_run": EXPECTED_WINDOWS_PER_RUN,
            "local_example_rule": "agent_run_index=1 and window [25,30)",
            "local_example_count": sum(
                row["local_example_03_10"] == "true" for row in index_rows
            ),
            "reuse_destination": str(output_dir.relative_to(repo_root)),
            "phase03_6_extractor_sha256": EXPECTED_EXTRACTOR_SHA256,
            "phase03_6_leakage_sha256": EXPECTED_LEAKAGE_SHA256,
            "fault_evidence_preferred_release": source_release,
            "baseline_provenance": {
                "authorization": "U3 extension of U1/R2; extended to normal_dev by author 3.9 OK",
                "role": "normalization and frozen V2 verbalizer flags only",
                "baseline_sha256": baseline_sha256,
                "verbalizer_config_sha256": extractor.sha256_file(config_path),
                "r2_guard_sha256": extractor.sha256_file(r2_guard_path),
                "r2_guard_required": True,
            },
            "regeneration_rule": (
                "All Normal evidence is invalid and must be regenerated if the R2 guard "
                "fails or the study switches to baseline_fit_new."
            ),
            "evidence_manifest_sha256": extractor.sha256_file(manifest_path),
            "evaluator_index_sha256": extractor.sha256_file(index_path),
        }
        extractor._write_json(partial / "EXTRACTION_SUMMARY.json", summary)
        partial.rename(output_dir)
        return summary
    except Exception:
        shutil.rmtree(partial, ignore_errors=True)
        raise


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--extractor", type=Path, required=True)
    parser.add_argument("--plan", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--runs-root", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--normal", type=Path, required=True)
    parser.add_argument("--r2-guard", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-release", default="studio2-fase03-evidence-v2")
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[3]
    extractor = load_verified_extractor(args.extractor)
    campaign = validated_campaign(
        plan_path=args.plan,
        manifest_path=args.manifest,
        runs_root=args.runs_root,
        audit_path=args.audit,
    )
    summary = extract_normal(
        repo_root=repo_root,
        extractor=extractor,
        campaign=campaign,
        normal_path=args.normal,
        r2_guard_path=args.r2_guard,
        output_dir=args.output.resolve(),
        source_release=args.source_release,
    )
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
