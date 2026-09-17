#!/usr/bin/env python3
"""Consumer input of the 03.11 test lot: one assigned 5 h window per run.

This is a **new driver over the frozen 03.6 pipeline**, not a new pipeline.  It imports
``extract_evidence`` unchanged and reuses, byte for byte, the same frozen sources
(``code/tep_features.py``, ``code/tep_verbalize_v2.py``, ``code/verbalizer_config_v2.json``,
``code/evaluate_verbalizer_v2.py``), the same legacy Normal baseline, the same four Phase A
thresholds, the same R2 guard, the same descriptors and the same neutral-text renderer.
Windows are computed over the whole frozen horizon ``[25, 65)`` exactly as 03.6 does, and
only afterwards is the window assigned by D1 kept: the retained unit is therefore identical
to the one 03.6 would produce for that window.

What is different, and only this: the run set is the 03.11 test lot instead of the 40
development runs, and exactly one window per run is written out -- the one frozen in
``batch_finale/ASSEGNAZIONE_FINESTRE_7_4.json`` before any test datum was opened (D1).

Scientific exclusions of 03.6 are kept: no separability, no per-fault statistic, no
preview, no selection on content.  Fault, run index and stream stay in the evaluator-side
index, out of the consumer-visible files.  A run that is missing, or whose assigned window
cannot be extracted, is **recorded and never substituted**.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from studio2.fase03.evidence import extract_evidence as frozen  # noqa: E402
from studio2.fase03.evidence.leakage import assert_no_leakage  # noqa: E402
from studio2.fase03.harness import window_assignment as assignment_module  # noqa: E402

ASSIGNMENT_PATH = REPO_ROOT / "studio2/fase03/batch_finale/ASSEGNAZIONE_FINESTRE_7_4.json"
# The frozen pilot input manifest supplies local examples, label space, agents and
# derangements; the test lot supplies only the cases to diagnose (review rilievo B2).
PILOT_INPUT_MANIFEST_SHA256 = "8417688869b75bda8235387ac830018ecdc9030442a860d495418f195f2b4014"
EVIDENCE_PREFIX = "EVT"
LOT_RELEASE = "studio2-fase03-test-v1"
LOT_ASSET = "test_batch_f5_001.tar.gz"
LOT_ASSET_SHA256 = "ac1e7c0c4575ab746ee24a8bb5ce7f09289919773bc4d8c61ba86f7a93218a55"
LOT_ASSET_URL = (
    "https://github.com/sorrentinoluca/fot-tep-data/releases/download/"
    f"{LOT_RELEASE}/{LOT_ASSET}"
)


def download_instructions(destination: Path) -> dict[str, Any]:
    """Exact commands for the author when the verified local copy is absent."""
    return {
        "release": LOT_RELEASE,
        "asset": LOT_ASSET,
        "asset_sha256": LOT_ASSET_SHA256,
        "commands": [
            f"mkdir -p {destination}",
            f"curl -fL -o {destination}/{LOT_ASSET} {LOT_ASSET_URL}",
            f"printf '%s  %s\\n' {LOT_ASSET_SHA256} {destination}/{LOT_ASSET} "
            f"> {destination}/{LOT_ASSET}.sha256",
            f"shasum -a 256 -c {destination}/{LOT_ASSET}.sha256",
            f"tar -xzf {destination}/{LOT_ASSET} -C {destination}",
        ],
        "note": "extract, then pass --lot-root <dir containing generation_manifest.csv>",
    }


def read_lot_manifest(path: Path) -> dict[str, dict[str, str]]:
    """Read the sealed generation manifest of the test lot and check every row's form.

    The campaign manifest names the run CSV hash ``sha256``; the 03.6 reader expects
    ``output_sha256``. Only the column name is normalised here -- no value is invented.
    """
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    by_run: dict[str, dict[str, str]] = {}
    for row in rows:
        run_id = (row.get("run_id") or "").strip()
        if not run_id:
            raise ValueError("generation manifest contains an empty run_id")
        if run_id in by_run:
            raise ValueError(f"duplicate run_id in the generation manifest: {run_id}")
        if not row.get("output_sha256") and row.get("sha256"):
            row["output_sha256"] = row["sha256"]
        by_run[run_id] = row
    return by_run


def expected_windows() -> list[dict[str, Any]]:
    """The eight half-open post-onset windows of the frozen horizon [25, 65)."""
    return [{"start_h": int(frozen.ONSET_H + index * frozen.WINDOW_H),
             "end_h": int(frozen.ONSET_H + (index + 1) * frozen.WINDOW_H),
             "complete": True}
            for index in range(frozen.EXPECTED_WINDOWS_PER_RUN)]


def per_run_window_check(row: dict[str, str]) -> str | None:
    """Per-run re-verification of the D1 precondition; returns a reason when it fails.

    The declared count is checked first, then -- when the campaign manifest carries the
    window table -- the geometry itself: eight complete half-open windows over [25, 65).
    ``development_eligible`` is **not** required here: the test lot is by construction not
    development-eligible, and that flag plays no part in the extraction.
    """
    if row.get("status") != "complete":
        return f"status is {row.get('status')!r}, not complete"
    try:
        windows = int(row.get("useful_windows_complete", "-1"))
    except ValueError:
        return "useful_windows_complete is not an integer"
    if windows != frozen.EXPECTED_WINDOWS_PER_RUN:
        return f"{windows} useful windows, expected {frozen.EXPECTED_WINDOWS_PER_RUN}"
    if not row.get("output_sha256"):
        return "missing output_sha256"
    declared = row.get("post_fault_windows")
    if declared:
        try:
            table = json.loads(declared)
        except (TypeError, json.JSONDecodeError):
            return "post_fault_windows is not readable JSON"
        observed = [{"start_h": int(item["start_h"]), "end_h": int(item["end_h"]),
                     "complete": bool(item.get("complete"))} for item in table]
        if observed != expected_windows():
            return f"post-onset window table is not the frozen eight: {observed}"
    for key, value in (("onset_h", frozen.ONSET_H), ("stop_time_h", frozen.END_H),
                       ("window_h", frozen.WINDOW_H)):
        if key in row and row[key] not in ("", None) and float(row[key]) != value:
            return f"{key} is {row[key]}, expected {value}"
    return None


def verify_lot_run_manifest(row: dict[str, str], source: Path) -> None:
    """Cross-check the immutable per-run manifest of the test lot, when it is present."""
    manifest_path = source.with_suffix(".manifest.json")
    if not manifest_path.is_file():
        return
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    expected_values = {
        "run_id": row["run_id"], "status": "complete", "stream_id": row["stream_id"],
        "idv": int(row["idv"]), "onset_h": frozen.ONSET_H,
        "horizon_h": frozen.END_H - frozen.ONSET_H, "stop_time_h": frozen.END_H,
        "window_h": frozen.WINDOW_H,
        "useful_windows_complete": frozen.EXPECTED_WINDOWS_PER_RUN,
        "sha256": row["output_sha256"],
    }
    mismatches = {key: (payload.get(key), value) for key, value in expected_values.items()
                  if payload.get(key) != value}
    observed = [{"start_h": int(item["start_h"]), "end_h": int(item["end_h"]),
                 "complete": bool(item.get("complete"))}
                for item in payload.get("post_fault_windows") or []]
    if observed != expected_windows():
        mismatches["post_fault_windows"] = (observed, expected_windows())
    if mismatches:
        raise RuntimeError(f"{row['run_id']}: per-run manifest mismatch: {sorted(mismatches)}")


def extract(*, api, assignment: list[dict[str, Any]], lot_rows: dict[str, dict[str, str]],
            baseline, output_dir: Path, runs_root: Path | None,
            baseline_provenance: dict[str, Any]) -> dict[str, Any]:
    if output_dir.exists():
        raise FileExistsError(f"Output directory already exists: {output_dir}")
    temp_dir = output_dir.with_name(output_dir.name + ".partial")
    if temp_dir.exists():
        raise FileExistsError(f"Partial output directory already exists: {temp_dir}")
    units_dir = temp_dir / "units"
    units_dir.mkdir(parents=True)
    config_path = REPO_ROOT / "code" / "verbalizer_config_v2.json"
    config = api.load_config(config_path)
    if float(config["window_hours"]) != frozen.WINDOW_H:
        raise RuntimeError("Frozen config window_hours is no longer 5.0")

    manifest_rows: list[dict[str, Any]] = []
    index_rows: list[dict[str, Any]] = []
    not_extracted: list[dict[str, str]] = []
    visible_paths: list[Path] = []
    counter = 0
    try:
        for assigned in assignment:
            case_id = assigned["case_id"]
            row = lot_rows.get(case_id)
            if row is None:
                not_extracted.append({"case_id": case_id, "reason": "run absent from the lot manifest"})
                continue
            reason = per_run_window_check(row)
            if reason is not None:
                not_extracted.append({"case_id": case_id, "reason": reason})
                continue
            try:
                source = frozen.resolve_source(row, runs_root=runs_root)
                verify_lot_run_manifest(row, source)
                case = api.load_case(source)
                features = api.analyze_case_windows(
                    case, baseline, start_h=frozen.ONSET_H, end_h=frozen.END_H,
                    window_h=frozen.WINDOW_H)
                starts = sorted(float(value) for value in features.window_start_h.unique())
                if len(starts) != frozen.EXPECTED_WINDOWS_PER_RUN:
                    raise RuntimeError(f"expected eight extracted windows, got {len(starts)}")
            except Exception as exc:
                not_extracted.append({"case_id": case_id, "reason": f"{type(exc).__name__}: {exc}"})
                continue

            ordinal = int(assigned["window_ordinal"])
            start_h = starts[ordinal - 1]
            if start_h != assigned["window_start_h"]:
                raise RuntimeError(
                    f"{case_id}: assigned window {ordinal} starts at {start_h} h, "
                    f"the assignment declares {assigned['window_start_h']} h")
            counter += 1
            evidence_id = f"{EVIDENCE_PREFIX}-{counter:04d}"
            unit = features[features.window_start_h == start_h].copy()
            unit = unit.sort_values(
                "variable",
                key=lambda series: series.map(
                    {name: index for index, name in enumerate(api.xmeas)}))
            result = api.verbalize_feature_table(unit, config)
            signature = api.signature_vector(result["structured"])
            if signature.shape != (frozen.SIGNATURE_DIMENSION,):
                raise RuntimeError(f"{evidence_id}: signature shape is {signature.shape}")

            stem = units_dir / evidence_id
            feature_path = stem.with_suffix(".features.csv")
            json_path = stem.with_suffix(".evidence.json")
            text_path = stem.with_suffix(".txt")
            signature_path = stem.with_suffix(".signature.csv")
            unit.to_csv(feature_path, index=False, lineterminator="\n")
            frozen._write_json(json_path, result["structured"])
            text_path.write_text(result["text"] + "\n", encoding="utf-8")
            frozen._write_csv(
                signature_path, ["component", "value"],
                ({"component": index, "value": format(float(value), ".17g")}
                 for index, value in enumerate(signature)))
            visible_paths.extend((json_path, text_path))

            artifacts: dict[str, Any] = {}
            for label, path in (("feature", feature_path), ("json", json_path),
                                ("text", text_path), ("signature", signature_path)):
                rel, dig, size = frozen._artifact_record(temp_dir, path)
                artifacts[f"{label}_path"] = rel
                artifacts[f"{label}_sha256"] = dig
                artifacts[f"{label}_bytes"] = size
            manifest_rows.append({
                "evidence_id": evidence_id,
                "case_id": case_id,
                "window_ordinal": ordinal,
                "signature_dimension": len(signature),
                "leakage_pass": "pending",
                "baseline_sha256": baseline_provenance["baseline_sha256"],
                "r2_guard_sha256": baseline_provenance["r2_guard_sha256"],
                "regenerate_if_r2_fails": "true",
                "neutral_text_sha256": frozen.sha256_file(text_path),
                **artifacts,
            })
            index_rows.append({
                "evidence_id": evidence_id,
                "run_id": case_id,
                "fault": f"F{int(row['idv'])}" if int(row["idv"]) else "Normal",
                "idv": int(row["idv"]),
                "run_index": case_id.rsplit("-r", 1)[1],
                "stream_id": row["stream_id"],
                "window_ordinal": ordinal,
                "window_start_h": format(start_h, ".1f"),
                "window_end_h": format(start_h + frozen.WINDOW_H, ".1f"),
                "source_path": row["output_path"],
                "source_sha256": row["output_sha256"],
                "source_manifest_sha256": row.get("manifest_sha256", ""),
            })

        findings = []
        try:
            assert_no_leakage(visible_paths)
        except ValueError as exc:
            findings.append(str(exc))
        if findings:
            raise RuntimeError("; ".join(findings))
        for item in manifest_rows:
            item["leakage_pass"] = "true"

        manifest_path = temp_dir / "EVIDENCE_MANIFEST_TEST.csv"
        index_path = temp_dir / "EVALUATOR_INDEX_TEST.csv"
        frozen._write_csv(manifest_path, list(manifest_rows[0]) if manifest_rows else [], manifest_rows)
        frozen._write_csv(index_path, list(index_rows[0]) if index_rows else [], index_rows)
        summary = {
            "artifact_version": "INPUT_MANIFEST_TEST_7_4_1",
            "lot": "03.11 test_batch_f5_001",
            "pipeline": "frozen 03.6 extraction, one assigned window per run (D1)",
            "assignment_sha256": None,  # filled by the caller
            "assigned_runs": len(assignment),
            "evidence_unit_count": counter,
            "not_extracted": not_extracted,
            "substitution_policy": "a missing run or a non-extractable window is recorded, never substituted",
            "files_per_unit": 4,
            "consumer_visible_json_text_leakage": "PASS",
            "signature_dimension": frozen.SIGNATURE_DIMENSION,
            "onset_h": frozen.ONSET_H, "end_h": frozen.END_H, "window_h": frozen.WINDOW_H,
            "windows_extracted_per_run": 1,
            "windows_computed_per_run": frozen.EXPECTED_WINDOWS_PER_RUN,
            "baseline_provenance": baseline_provenance,
            "frozen_pilot_input_manifest_sha256": PILOT_INPUT_MANIFEST_SHA256,
            "frozen_pilot_input_manifest_role":
                "local examples, label space, agents and derangements of the final batch",
            "regeneration_rule": (
                "All evidence is invalid and must be regenerated if the R2 guard fails "
                "or the study switches to baseline_fit_new."),
            "evidence_manifest_sha256": frozen.sha256_file(manifest_path),
            "evaluator_index_sha256": frozen.sha256_file(index_path),
        }
        frozen._write_json(temp_dir / "INPUT_MANIFEST_TEST_7_4.json", summary)
        temp_dir.rename(output_dir)
        return summary
    except Exception:
        shutil.rmtree(temp_dir, ignore_errors=True)
        raise


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lot-root", type=Path,
                        help="directory holding generation_manifest.csv of test_batch_f5_001")
    parser.add_argument("--runs-root", type=Path,
                        help="directory holding the per-run CSV files (default: --lot-root)")
    parser.add_argument("--normal", type=Path, help="legacy Normal baseline workbook")
    parser.add_argument("--r2-guard", type=Path, help="R2_GUARD_RECHECK.json of 03.5")
    parser.add_argument("--assignment", type=Path, default=ASSIGNMENT_PATH)
    parser.add_argument("--output", type=Path, help="output directory (must not exist)")
    parser.add_argument("--download-destination", type=Path,
                        default=REPO_ROOT / "studio2/fase03/fault_runs/test_batch")
    arguments = parser.parse_args(argv)

    artifact = json.loads(arguments.assignment.read_text(encoding="utf-8"))
    expected = assignment_module.assignment_artifact()
    if artifact["assignment"] != expected["assignment"]:
        raise SystemExit(json.dumps({"status": "STOP", "reason":
                                     "the committed assignment differs from the generator"}))

    missing = [name for name, value in (("--lot-root", arguments.lot_root),
                                        ("--normal", arguments.normal),
                                        ("--r2-guard", arguments.r2_guard),
                                        ("--output", arguments.output))
               if value is None]
    manifest_path = None if arguments.lot_root is None else arguments.lot_root / "generation_manifest.csv"
    if not missing and not manifest_path.is_file():
        missing.append(f"generation_manifest.csv under {arguments.lot_root}")
    if missing:
        print(json.dumps({
            "status": "BLOCKED_MISSING_VERIFIED_LOCAL_COPY",
            "missing": missing,
            "assignment_sha256": artifact["assignment_sha256"],
            "download": download_instructions(arguments.download_destination),
        }, indent=2, ensure_ascii=False))
        return 3

    api = frozen.load_frozen_api(REPO_ROOT)
    config_path = REPO_ROOT / "code" / "verbalizer_config_v2.json"
    baseline_hash = frozen.sha256_file(arguments.normal)
    if baseline_hash != frozen.EXPECTED_BASELINE_SHA256:
        raise SystemExit("Legacy baseline hash mismatch")
    frozen.validate_r2_guard(arguments.r2_guard)
    baseline = api.load_development_baseline(arguments.normal, api.load_config(config_path))
    lot_rows = read_lot_manifest(manifest_path)
    summary = extract(
        api=api, assignment=artifact["assignment"], lot_rows=lot_rows, baseline=baseline,
        output_dir=arguments.output,
        runs_root=arguments.runs_root or arguments.lot_root,
        baseline_provenance={
            "authorization": "U3 extension of U1/R2, author decision 2026-09-13",
            "role": "normalization and frozen V2 verbalizer flags only",
            "baseline_sha256": baseline_hash,
            "verbalizer_config_sha256": frozen.sha256_file(config_path),
            "r2_guard_sha256": frozen.sha256_file(arguments.r2_guard),
            "r2_guard_required": True,
            "score_threshold_source": "new Normal runs from phase 03.5; not this baseline",
        })
    summary["assignment_sha256"] = artifact["assignment_sha256"]
    frozen._write_json(arguments.output / "INPUT_MANIFEST_TEST_7_4.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
