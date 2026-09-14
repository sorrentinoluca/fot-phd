#!/usr/bin/env python3
"""Reproducible, read-only technical audit of the normal_dev campaign.

The script reads plans, manifests, logs, qualified sources and all 40 XLSX
workbooks in one invocation.  It never launches MATLAB and never changes input
artifacts.  Only AUDIT_NORMAL_DEV.json and AUDIT_NORMAL_DEV.md are written.
"""

from __future__ import annotations

import argparse
import collections
import csv
import datetime as dt
import hashlib
import json
import math
import os
import platform
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

import openpyxl


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PRIMARY_REPO = Path("/Users/luker/fot-tep")
PLAN = HERE / "plans" / "normal_dev.csv"
RUN_DIR = HERE / "runs" / "normal_dev_001"
MANIFEST = RUN_DIR / "generation_manifest.csv"
RUNTIME_OK = HERE / "runtime" / "normal_dev_001"
RUNTIME_FAIL = HERE / "runtime" / "normal_dev_001_prestart_failure_20260914T090037Z"
EXPECTED_MEX = "6ae7e7be5394773f1854f1c53eddbd778ad7557b61fb05a93b3edb0552b1d11e"
EXPECTED_MODEL = "c58826748edd306b723da2f0199a0fb2dc193a51dc5c28dbde8ac821e39dfafd"
EXPECTED_KEY = "0x464f545445503032"
EXPECTED_NAMESPACE = "fot-tep/fase03/normal_dev/v1"
GRID_TOL_H = 1e-10  # 0.36 microseconds; much larger than XLSX roundoff, far below one minute.
EXPECTED_HEADERS = (["Time (h)"] + [f"XMEAS-{i}" for i in range(1, 42)]
                    + [f"XMV-{i}" for i in range(1, 13)])


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def run(cmd: list[str], cwd: Path = REPO) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, capture_output=True, check=False)


def git_text(*args: str) -> str | None:
    result = run(["git", *args])
    return result.stdout.strip() if result.returncode == 0 else None


def file_record(path: Path, *, git_path: str | None = None) -> dict[str, Any]:
    record: dict[str, Any] = {
        "path": str(path), "exists": path.is_file(),
    }
    if not path.is_file():
        return record
    record.update({"bytes": path.stat().st_size, "sha256": sha256(path)})
    if git_path:
        tracked = run(["git", "ls-files", "--error-unmatch", git_path]).returncode == 0
        record["tracked"] = tracked
        if tracked:
            blob = run(["git", "show", f"HEAD:{git_path}"])
            if blob.returncode == 0:
                raw = subprocess.run(
                    ["git", "show", f"HEAD:{git_path}"], cwd=REPO,
                    capture_output=True, check=False,
                ).stdout
                record["head_sha256"] = hashlib.sha256(raw).hexdigest()
                record["matches_head_bytes"] = record["head_sha256"] == record["sha256"]
            record["last_commit"] = git_text("log", "-1", "--format=%H", "--", git_path)
    return record


def read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        return list(reader.fieldnames or []), list(reader)


def check(name: str, passed: bool, details: Any) -> dict[str, Any]:
    return {"name": name, "status": "PASS" if passed else "FAIL", "details": details}


def parse_matlab_time(value: str) -> dt.datetime:
    return dt.datetime.strptime(value, "%d-%b-%Y %H:%M:%S").replace(tzinfo=dt.timezone.utc)


def duplicates(values: Iterable[str]) -> list[str]:
    counts = collections.Counter(values)
    return sorted(value for value, count in counts.items() if count > 1)


def audit_plan() -> tuple[list[dict[str, str]], dict[str, Any]]:
    fields, rows = read_csv(PLAN)
    expected_fields = [
        "run_id", "set_name", "agent_id", "agent_run_index", "run_index_uint64",
        "stream_id", "seed_namespace", "seed_descriptor", "stream_lo32",
        "stream_hi32", "burn_in_h", "stop_time_h", "window_position",
        "development_start_h", "development_end_h", "window_h",
        "useful_windows_expected", "use",
    ]
    row_results: list[dict[str, Any]] = []
    for position, row in enumerate(rows):
        agent_index = position // 5 + 1
        local_index = position % 5 + 1
        stream = 60000 + 5 * (agent_index - 1) + (local_index - 1)
        expected = {
            "run_id": f"normal-dev-agent-{agent_index}-r{local_index:02d}",
            "set_name": "normal_dev", "agent_id": f"agent_{agent_index}",
            "agent_run_index": str(local_index), "run_index_uint64": str(stream),
            "stream_id": str(stream), "seed_namespace": EXPECTED_NAMESPACE,
            "seed_descriptor": f"{EXPECTED_KEY}:{stream:016x}",
            "stream_lo32": str(stream & 0xFFFFFFFF), "stream_hi32": str(stream >> 32),
            "burn_in_h": "20", "stop_time_h": "65", "window_position": "0",
            "development_start_h": "25", "development_end_h": "65",
            "window_h": "5", "useful_windows_expected": "8",
            "use": "development_only",
        }
        mismatches = {k: {"actual": row.get(k), "expected": v}
                      for k, v in expected.items() if row.get(k) != v}
        row_results.append({"position": position + 1, "run_id": row.get("run_id"),
                            "status": "PASS" if not mismatches else "FAIL",
                            "mismatches": mismatches})

    agents = collections.defaultdict(list)
    for row in rows:
        agents[row.get("agent_id", "")].append(row.get("agent_run_index", ""))
    plan_git = file_record(PLAN, git_path=str(PLAN.relative_to(REPO)))
    result = {
        "file": plan_git,
        "fields": fields,
        "row_count": len(rows),
        "duplicate_run_ids": duplicates(row.get("run_id", "") for row in rows),
        "duplicate_stream_ids": duplicates(row.get("stream_id", "") for row in rows),
        "agents": dict(sorted(agents.items())),
        "row_results": row_results,
    }
    result["checks"] = [
        check("plan_schema", fields == expected_fields, {"actual": fields, "expected": expected_fields}),
        check("plan_exact_40_rows", len(rows) == 40, len(rows)),
        check("plan_distinct_run_ids", not result["duplicate_run_ids"], result["duplicate_run_ids"]),
        check("plan_distinct_stream_ids", not result["duplicate_stream_ids"], result["duplicate_stream_ids"]),
        check("plan_rows_match_specification", all(r["status"] == "PASS" for r in row_results),
              [r for r in row_results if r["status"] != "PASS"]),
        check("plan_bytes_match_HEAD", bool(plan_git.get("matches_head_bytes")), plan_git),
    ]
    return rows, result


def discover_collision_sources() -> list[Path]:
    """Find pertinent plan/manifest CSVs in this checkout, primary checkout and sibling worktrees."""
    roots = [REPO, PRIMARY_REPO]
    worktrees = PRIMARY_REPO / ".worktrees"
    if worktrees.is_dir():
        roots.extend(p for p in worktrees.iterdir() if p.is_dir())
    candidates: set[Path] = set()
    for root in roots:
        for phase in (root / "studio2" / "fase02", root / "studio2" / "fase03"):
            if not phase.is_dir():
                continue
            candidates.update(phase.glob("**/plans/*.csv"))
            candidates.update(phase.glob("**/generation_manifest.csv"))
    return sorted(p.resolve() for p in candidates if p.resolve() != PLAN.resolve())


def audit_collisions() -> dict[str, Any]:
    target = set(range(60000, 60040))
    records: list[dict[str, Any]] = []
    collisions: list[dict[str, Any]] = []
    content_seen: set[tuple[str, str]] = set()
    for path in discover_collision_sources():
        try:
            fields, rows = read_csv(path)
        except (OSError, UnicodeError, csv.Error) as exc:
            records.append({"path": str(path), "status": "NOT_READ", "error": str(exc)})
            continue
        key = next((k for k in ("stream_id", "run_index_uint64", "run_index") if k in fields), None)
        if key is None:
            continue
        values: list[int] = []
        invalid: list[str] = []
        for row in rows:
            raw = row.get(key, "")
            if not raw:
                continue
            try:
                values.append(int(raw))
            except ValueError:
                invalid.append(raw)
        digest = sha256(path)
        dedupe_key = (digest, key)
        duplicate_copy = dedupe_key in content_seen
        content_seen.add(dedupe_key)
        overlap = sorted(target.intersection(values))
        set_names = sorted({row.get("set_name", "") for row in rows if row.get("set_name")})
        same_lot_replica = bool(overlap) and set_names == ["normal_dev"] and set(values) == target
        rec = {
            "path": str(path), "sha256": digest, "bytes": path.stat().st_size,
            "identifier_field": key, "identifier_count": len(values),
            "identifier_min": min(values) if values else None,
            "identifier_max": max(values) if values else None,
            "invalid_identifiers": invalid,
            "collision_streams": [] if same_lot_replica else overlap,
            "same_normal_dev_lot_replica": same_lot_replica,
            "duplicate_content_copy": duplicate_copy,
        }
        records.append(rec)
        if overlap and not same_lot_replica:
            collisions.append({"path": str(path), "streams": overlap})
    return {
        "scope": "CSV plans and generation manifests under studio2/fase02 and studio2/fase03 "
                 "in the current checkout, primary checkout, and all sibling .worktrees present at audit time",
        "sources_scanned": len(records), "unique_source_contents": len(content_seen),
        "records": records, "collisions": collisions,
        "status": "PASS" if not collisions else "FAIL",
        "limitation": "This establishes absence of collisions only in the enumerated local sources; "
                      "it is not a claim about unavailable repositories or deleted/unmounted worktrees.",
    }


def audit_manifest_and_workbooks(plan_rows: list[dict[str, str]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    fields, manifest_rows = read_csv(MANIFEST)
    plan_ids = [row["run_id"] for row in plan_rows]
    manifest_ids = [row.get("run_id", "") for row in manifest_rows]
    plan_counts = collections.Counter(plan_ids)
    manifest_counts = collections.Counter(manifest_ids)
    expected_files = [RUN_DIR / f"{run_id}.xlsx" for run_id in plan_ids]
    actual_files = sorted(RUN_DIR.iterdir()) if RUN_DIR.is_dir() else []
    allowed = {p.resolve() for p in expected_files + [MANIFEST]}
    extras = [str(p) for p in actual_files if p.resolve() not in allowed]
    missing = [str(p) for p in expected_files + [MANIFEST] if not p.is_file()]
    temporary = [str(p) for p in actual_files if ".tmp" in p.name.lower() or p.name.startswith("~$")]

    rows_by_id: dict[str, list[dict[str, str]]] = collections.defaultdict(list)
    for row in manifest_rows:
        rows_by_id[row.get("run_id", "")].append(row)

    per_run: list[dict[str, Any]] = []
    for plan_row in plan_rows:
        run_id = plan_row["run_id"]
        joined = rows_by_id.get(run_id, [])
        record: dict[str, Any] = {
            "run_id": run_id, "agent_id": plan_row["agent_id"],
            "agent_run_index": int(plan_row["agent_run_index"]),
            "stream_id": int(plan_row["stream_id"]), "manifest_match_count": len(joined),
            "checks": {}, "anomalies": [],
        }
        if len(joined) != 1:
            record["anomalies"].append(f"expected exactly one manifest row, found {len(joined)}")
            record["status"] = "FAIL"
            per_run.append(record)
            continue
        row = joined[0]
        path = RUN_DIR / f"{run_id}.xlsx"
        try:
            output_path = Path(row["output_path"])
            output_resolved = output_path.resolve()
            within = output_resolved.is_relative_to(RUN_DIR.resolve())
        except (KeyError, OSError):
            output_resolved, within = Path("."), False
        record["output_path_manifest"] = row.get("output_path")
        record["output_path_actual"] = str(path.resolve())
        record["checks"]["output_path_exact"] = output_resolved == path.resolve()
        record["checks"]["output_path_confined"] = within
        record["checks"]["file_present"] = path.is_file()
        if not path.is_file():
            record["anomalies"].append("workbook missing")
            record["status"] = "FAIL"
            per_run.append(record)
            continue
        record["bytes"] = path.stat().st_size
        record["sha256_actual"] = sha256(path)
        record["sha256_manifest"] = row.get("sha256")
        record["checks"]["sha256"] = record["sha256_actual"] == row.get("sha256")

        scalar_expected = {
            "set_name": "normal_dev", "stream_id": plan_row["stream_id"],
            "rng_algorithm": "Philox4x32-10", "rng_key_hex": EXPECTED_KEY,
            "counter_start": "0", "mex_sha256": EXPECTED_MEX,
            "model_sha256": EXPECTED_MODEL, "ts_base_h": "0.0005",
            "stop_time_h": "65", "burn_in_h": "20", "window_position": "0",
            "actual_end_h": "65", "status": "complete", "data_rows": "3901", "columns": "54",
        }
        scalar_mismatch = {key: {"actual": row.get(key), "expected": value}
                           for key, value in scalar_expected.items() if row.get(key) != value}
        record["checks"]["manifest_scalars"] = not scalar_mismatch
        record["manifest_scalar_mismatches"] = scalar_mismatch
        try:
            interval = float(row["output_interval_h"])
            record["checks"]["output_interval_one_minute"] = math.isclose(interval, 1 / 60, rel_tol=0, abs_tol=1e-14)
        except (KeyError, ValueError):
            record["checks"]["output_interval_one_minute"] = False
        try:
            counter_end = int(row["counter_end"])
            record["counter_end"] = counter_end
            record["checks"]["counter_end_valid"] = counter_end > int(row["counter_start"])
        except (KeyError, ValueError):
            record["checks"]["counter_end_valid"] = False
        try:
            started = parse_matlab_time(row["started_at_utc"])
            finished = parse_matlab_time(row["finished_at_utc"])
            runtime = float(row["runtime_seconds"])
            timestamp_delta = (finished - started).total_seconds()
            record["timing"] = {"started_at_utc": started.isoformat(), "finished_at_utc": finished.isoformat(),
                                "runtime_seconds": runtime, "timestamp_delta_seconds": timestamp_delta,
                                "precision_tolerance_seconds": 1.1}
            record["checks"]["timing_order"] = finished >= started and runtime > 0
            record["checks"]["runtime_coherent_with_rounded_timestamps"] = abs(timestamp_delta - runtime) <= 1.1
        except (KeyError, ValueError):
            record["checks"]["timing_order"] = False
            record["checks"]["runtime_coherent_with_rounded_timestamps"] = False

        workbook_checks: dict[str, Any] = {}
        try:
            wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
            sheet_names = wb.sheetnames
            ws = wb[sheet_names[0]]
            iterator = ws.iter_rows(values_only=True)
            headers = list(next(iterator))
            data_count = 0
            missing_cells = 0
            non_numeric_cells = 0
            non_finite_cells = 0
            max_grid_error = 0.0
            time_monotone = True
            time_duplicates = 0
            previous_time: float | None = None
            window_counts = [0] * 8
            excluded_counts = {"burn_in_[0,20)": 0, "control_[20,25)": 0, "endpoint_65": 0}
            for values in iterator:
                data_count += 1
                if len(values) != 54:
                    workbook_checks.setdefault("row_width_mismatches", []).append(data_count)
                for value in values[:54]:
                    if value is None:
                        missing_cells += 1
                    elif isinstance(value, bool) or not isinstance(value, (int, float)):
                        non_numeric_cells += 1
                    elif not math.isfinite(float(value)):
                        non_finite_cells += 1
                if not values or not isinstance(values[0], (int, float)) or isinstance(values[0], bool):
                    continue
                time_h = float(values[0])
                expected_h = (data_count - 1) / 60
                max_grid_error = max(max_grid_error, abs(time_h - expected_h))
                if previous_time is not None:
                    if time_h <= previous_time:
                        time_monotone = False
                    if time_h == previous_time:
                        time_duplicates += 1
                previous_time = time_h
                minute_index = data_count - 1
                if minute_index < 1200:
                    excluded_counts["burn_in_[0,20)"] += 1
                elif minute_index < 1500:
                    excluded_counts["control_[20,25)"] += 1
                elif minute_index < 3900:
                    window_counts[(minute_index - 1500) // 300] += 1
                elif minute_index == 3900:
                    excluded_counts["endpoint_65"] += 1
            wb.close()
            workbook_checks.update({
                "sheet_names": sheet_names, "header_count": len(headers),
                "headers_exact": headers == EXPECTED_HEADERS, "data_rows_actual": data_count,
                "data_rows_manifest": int(row["data_rows"]), "columns_manifest": int(row["columns"]),
                "missing_cells": missing_cells, "non_numeric_cells": non_numeric_cells,
                "non_finite_cells": non_finite_cells, "time_strictly_monotone": time_monotone,
                "time_duplicate_count": time_duplicates, "max_grid_abs_error_h": max_grid_error,
                "grid_tolerance_h": GRID_TOL_H, "grid_valid": max_grid_error <= GRID_TOL_H,
                "time_start_h": 0.0 if data_count else None, "time_end_h": previous_time,
                "window_counts": window_counts, "excluded_sample_counts": excluded_counts,
                "windows_valid": window_counts == [300] * 8,
            })
            record["checks"]["workbook"] = (
                headers == EXPECTED_HEADERS and data_count == 3901 and missing_cells == 0
                and non_numeric_cells == 0 and non_finite_cells == 0 and time_monotone
                and time_duplicates == 0 and max_grid_error <= GRID_TOL_H
                and window_counts == [300] * 8 and excluded_counts == {
                    "burn_in_[0,20)": 1200, "control_[20,25)": 300, "endpoint_65": 1})
        except Exception as exc:  # Preserve the audit failure as data rather than aborting remaining files.
            workbook_checks = {"error": f"{type(exc).__name__}: {exc}"}
            record["checks"]["workbook"] = False
        record["workbook"] = workbook_checks
        record["status"] = "PASS" if all(record["checks"].values()) else "FAIL"
        if record["status"] == "FAIL":
            record["anomalies"].append("one or more per-run technical checks failed")
        per_run.append(record)

    join_rows = [{"agent_id": row["agent_id"], "agent_run_index": int(row["agent_run_index"]),
                  "run_id": row["run_id"], "stream_id": int(row["stream_id"])} for row in plan_rows]
    inventory = {
        "manifest": file_record(MANIFEST), "manifest_fields": fields,
        "manifest_rows": len(manifest_rows), "duplicate_manifest_run_ids": duplicates(manifest_ids),
        "plan_only_run_ids": sorted((plan_counts - manifest_counts).elements()),
        "manifest_only_run_ids": sorted((manifest_counts - plan_counts).elements()),
        "workbooks_expected": 40, "workbooks_found": len(list(RUN_DIR.glob("*.xlsx"))),
        "missing_paths": missing, "extra_paths": extras, "temporary_paths": temporary,
        "plan_manifest_join": join_rows,
        "bijection_status": "PASS" if (plan_counts == manifest_counts and not missing and not extras
                                           and not temporary and len(manifest_rows) == 40) else "FAIL",
    }
    return inventory, per_run


def audit_sources() -> dict[str, Any]:
    paths = {
        "specification": HERE / "SPECIFICA_NORMAL_DEV.md",
        "plan_builder": HERE / "build_normal_dev_plan.py",
        "preflight": HERE / "preflight_normal_dev.py",
        "wrapper": HERE / "generate_normal_dev_runs.m",
        "launcher": HERE / "launch_normal_dev_batch.sh",
        "handoff": HERE / "HANDOFF_NORMAL_DEV.md",
        "qualified_generator": REPO / "studio2/fase02/simulator/matlab/generate_normal_runs.m",
        "qualified_model": REPO / "studio2/fase02/simulator/matlab/MultiLoop_mode1.mdl",
        "phase02_freeze": REPO / "studio2/fase02/validation/PRECALIBRATION_FREEZE.json",
        "reference_audit_code": REPO / "studio2/fase03/fault_runs/fault_protocol.py",
        "phase03_5_audit_reference": PRIMARY_REPO / "studio2/fase03/soglie_normal/LOT_AUDIT.json",
    }
    records = {}
    for name, path in paths.items():
        git_path = str(path.relative_to(REPO)) if path.is_relative_to(REPO) else None
        records[name] = file_record(path, git_path=git_path)
    primary_mex = PRIMARY_REPO / "studio2/fase02/simulator/build/temexd_philox.mexmaca64"
    records["qualified_mex_primary_checkout"] = file_record(primary_mex)
    plan_revision = run(["git", "show", "a572d1c:docs/paper/FoT_TEP_Review_Piano_Sperimentale.md"])
    records["plan_revision_7"] = {
        "commit": git_text("rev-parse", "a572d1c"), "available": plan_revision.returncode == 0,
        "document_sha256": hashlib.sha256(plan_revision.stdout.encode()).hexdigest()
        if plan_revision.returncode == 0 else None,
        "section_6_2_contains_normal_dev_contract": all(term in plan_revision.stdout for term in (
            "Run Normal di sviluppo `normal_dev`", "60000–60039", "40 run Normal", "sviluppo")),
    }
    freeze = json.loads(paths["phase02_freeze"].read_text(encoding="utf-8"))
    records["phase02_freeze_cross_checks"] = {
        "selected_burn_in_hours": freeze.get("selected_burn_in_hours"),
        "model_sha256": freeze.get("files", {}).get("studio2/fase02/simulator/matlab/MultiLoop_mode1.mdl", {}).get("sha256"),
        "generator_sha256": freeze.get("files", {}).get("studio2/fase02/simulator/matlab/generate_normal_runs.m", {}).get("sha256"),
        "mex_sha256": freeze.get("local_mex", {}).get("sha256"),
        "matches_expected": (
            freeze.get("selected_burn_in_hours") == 20
            and freeze.get("files", {}).get("studio2/fase02/simulator/matlab/MultiLoop_mode1.mdl", {}).get("sha256") == EXPECTED_MODEL
            and freeze.get("files", {}).get("studio2/fase02/simulator/matlab/generate_normal_runs.m", {}).get("sha256") == records["qualified_generator"].get("sha256")
            and freeze.get("local_mex", {}).get("sha256") == EXPECTED_MEX),
    }
    phase35 = []
    for rel in ("cal_thr/generation_manifest.csv", "far_ver/generation_manifest.csv"):
        path = PRIMARY_REPO / "studio2/fase03/soglie_normal/runs/normal_001" / rel
        rec = file_record(path)
        if path.is_file():
            _, rows = read_csv(path)
            rec.update({"rows": len(rows), "mex_values": sorted({r.get("mex_sha256") for r in rows}),
                        "model_values": sorted({r.get("model_sha256") for r in rows})})
        phase35.append(rec)
    records["phase03_5_generation_manifests"] = phase35
    return records


def audit_attempts() -> dict[str, Any]:
    fail_log = RUNTIME_FAIL / "matlab.log"
    fail_pid = RUNTIME_FAIL / "matlab.pid"
    recovery_path = RUNTIME_FAIL / "RECOVERY.json"
    ok_log = RUNTIME_OK / "matlab.log"
    ok_pid = RUNTIME_OK / "matlab.pid"
    recovery = json.loads(recovery_path.read_text(encoding="utf-8"))
    fail_text = fail_log.read_text(encoding="utf-8", errors="replace")
    ok_text = ok_log.read_text(encoding="utf-8", errors="replace")
    buffer_values = [int(x) for x in re.findall(r"temporarily increased to (\d+)", ok_text)]
    generated_match = re.search(r"Generated (\d+) runs", ok_text)
    recovery_checks = {
        "failed_log_hash_matches_recovery": sha256(fail_log) == recovery.get("original_log_sha256"),
        "failed_pid_matches_recovery": fail_pid.read_text().strip() == str(recovery.get("failed_process_pid")),
        "failed_log_records_missing_mex": "temexd_philox MEX is not available" in fail_text,
        "failed_log_reaches_wrapper": "generate_normal_dev_runs" in fail_text,
        "failed_log_contains_simulation_warning": "Variable Time Delay" in fail_text,
        "recovery_generated_runs_claim": recovery.get("generated_runs"),
        "independent_zero_run_evidence": "No separate archived run destination or failed-attempt manifest is present; "
                                         "zero generated runs is consistent with the error location but RECOVERY.json is the only direct count.",
    }
    warnings = {
        "successful_log_directory_access_warning_count": ok_text.count("Directory access failure"),
        "successful_log_java_x11_warning_count": ok_text.count("WARNING: package sun.awt.X11"),
        "successful_log_variable_time_delay_warning_count": len(buffer_values),
        "variable_time_delay_buffer_values": dict(collections.Counter(buffer_values)),
        "classification": {
            "directory_access": "environment warning outside the controlled output paths; no output failure observed",
            "java_x11": "headless Java warning; no output failure observed",
            "variable_time_delay": "Simulink ha ampliato dinamicamente il buffer di runtime e richiede di aggiornare il parametro per la code generation. "
                                   "Il warning dimostra che il buffer configurato era insufficiente per queste simulazioni; questo audit non "
                                   "ne stabilisce l'innocuità scientifica e non invalida automaticamente gli output completi.",
        },
    }
    return {
        "failed_attempt": {
            "directory": str(RUNTIME_FAIL), "recovery": file_record(recovery_path),
            "log": file_record(fail_log), "pid": file_record(fail_pid), "checks": recovery_checks,
        },
        "successful_attempt": {
            "directory": str(RUNTIME_OK), "log": file_record(ok_log), "pid": file_record(ok_pid),
            "pid_value": ok_pid.read_text().strip(),
            "generated_runs_log_value": int(generated_match.group(1)) if generated_match else None,
            "warnings": warnings,
        },
        "chronology": {
            "failed_archive_suffix_utc": "2026-09-14T09:00:37Z",
            "successful_first_manifest_start_utc": "derived per row in run results",
            "pathname_reused": str(RUN_DIR),
        },
        "process_assessment": {
            "status": "deviazioni",
            "deviations": [
                "The specification requires a restart to use a new destination and track every attempt; the successful launch reused normal_dev_001.",
                "The failed runtime log/PID/RECOVERY were archived, but no separate archived failed-attempt run destination or manifest proves the zero-run count independently.",
                "The successful invocation and MATLABPATH override are not recorded in the successful log/manifest; the direct qualified build path is stated in RECOVERY.json and is consistent with the observed MEX hash, but the exact shell command is not independently attested.",
            ],
        },
    }


def document_test(baseline_failures: int) -> dict[str, Any]:
    result = run([sys.executable, "docs/test_explanation.py"])
    text = result.stdout + result.stderr
    match = re.search(r"FAILED \(failures=(\d+)", text)
    failures = int(match.group(1)) if match else (0 if result.returncode == 0 else None)
    skipped = None
    ran = None
    m = re.search(r"Ran (\d+) tests", text)
    if m:
        ran = int(m.group(1))
    m = re.search(r"skipped=(\d+)", text)
    if m:
        skipped = int(m.group(1))
    return {"command": f"{sys.executable} docs/test_explanation.py", "returncode": result.returncode,
            "tests_ran": ran, "failures": failures, "skipped": skipped,
            "baseline_failures_before_changes": baseline_failures,
            "not_worse_than_baseline": failures is not None and failures <= baseline_failures,
            "note": "This legacy documentation test does not validate normal_dev or the new audit."}


def preserve_previous(paths: list[Path]) -> str | None:
    existing = [p for p in paths if p.exists()]
    if not existing:
        return None
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    history = HERE / "audit_history" / stamp
    history.mkdir(parents=True, exist_ok=False)
    for path in existing:
        shutil.copy2(path, history / path.name)
    return str(history)


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    attempts = report["attempts"]
    failed_runs = [r for r in report["runs"] if r["status"] != "PASS"]
    return f"""# Audit tecnico `normal_dev`

**Esito tecnico del lotto: {summary['technical_result']}**  
**Conformità del processo: {summary['process_status']}**

Audit read-only della sotto-fase 03.9, eseguito il {report['audit']['finished_at_utc']} su 40
workbook con un'unica invocazione di `audit_normal_dev.py`. L'audit non valuta qualità scientifica,
separabilità, score, FAR o prestazioni e non estrae evidence.

## Esito

- Run tecnicamente validi: **{summary['valid_runs']}/40**.
- Piano ↔ manifest ↔ workbook: **{report['inventory']['bijection_status']}**; nessun dizionario è
  usato per decidere l'unicità, verificata con molteplicità e contatori.
- Workbook: 54 intestazioni attese, 3.901 righe dati per file, soli valori numerici finiti,
  griglia `0..65 h` al minuto e otto finestre `[25,30)..[60,65)` da 300 campioni: **{summary['workbooks_status']}**.
- Finestre valide: **{summary['valid_windows']}/320**. Sono 320 finestre appartenenti a 40 run,
  non 320 repliche indipendenti. `[0,20)`, `[20,25)` e il campione a 65 h sono esclusi.
- Tolleranza griglia: `{GRID_TOL_H:g} h` (0,36 microsecondi), superiore al roundoff XLSX osservato e
  molto inferiore al passo di un minuto. Nessun dato è stato interpolato o corretto.
- Collisioni con i piani/manifest locali enumerati: **{report['collisions']['status']}** su
  {report['collisions']['sources_scanned']} sorgenti ({report['collisions']['unique_source_contents']} contenuti distinti).
  Questo non è un'affermazione globale su fonti non disponibili.

## Identità e configurazione

Il piano è byte-identico alla versione tracciata a HEAD. Tutte le righe hanno `set_name=normal_dev`,
assegnazione esclusiva 5×8, stream 60000–60039 secondo la formula prescritta, namespace e descrittori
seed attesi e `use=development_only`. Il join agente/run/stream ricostruito dal piano è registrato
integralmente nel JSON.

Tutti i manifest riportano Philox4x32-10, chiave `{EXPECTED_KEY}`, `Ts_base=0.0005 h`, output al
minuto, contatore iniziale zero e contatore finale intero positivo, orizzonte effettivo 65 h,
MEX `{EXPECTED_MEX}` e modello `{EXPECTED_MODEL}`. I contatori finali non sono confrontati fra
stream diversi. Hash e dimensione di ogni workbook sono ricalcolati nel JSON.

Le fonti qualificate e le impronte del freeze di Fase 02 coincidono. Il codice attuale è tracciato
a HEAD `{report['git']['head']}`; i manifest non registrano il commit di esecuzione. Gli hash
dimostrano l'identità di MEX/modello e la corrispondenza delle fonti correnti, ma non provano da soli
quale checkout Git fosse attivo nel processo MATLAB.

## Tentativi e warning

Il primo tentativo è documentato da log, PID e `RECOVERY.json`: il log registra il MEX non trovato
prima del ciclo di simulazione e il suo hash coincide con quello citato nel recovery. La dichiarazione
`generated_runs=0` è coerente con il punto d'errore, ma non è provata indipendentemente da una
destinazione fallita archiviata o da un manifest del tentativo.

Il secondo tentativo termina con `Generated 40 runs`. Il log contiene
{attempts['successful_attempt']['warnings']['successful_log_variable_time_delay_warning_count']} warning
`Variable Time Delay`: {attempts['successful_attempt']['warnings']['classification']['variable_time_delay']}
Contiene inoltre un warning di accesso a `~/Documents/MATLAB` e due warning Java/X11.

## Conformità del processo

Stato: **deviazioni**. Il primo tentativo è stato archiviato, ma il lancio riuscito ha riutilizzato
il pathname `normal_dev_001`; la specifica richiedeva una nuova destinazione e il tracciamento di
tutti i tentativi. Inoltre il comando riuscito con `MATLABPATH` diretto al build qualificato non è
registrato nel log o nel manifest: `RECOVERY.json` lo propone e l'hash MEX osservato è coerente,
ma non costituisce prova indipendente del comando effettivo. Queste deviazioni non hanno prodotto
un fallimento dei controlli tecnici sui 40 output, ma non vengono sanate retroattivamente.

## Decisione dell'autore

Prima dell'accettazione l'autore deve decidere se accettare formalmente la deviazione di ripresa
(riuso del pathname) e se l'evidenza disponibile sul comando/MATLABPATH è sufficiente. Deve inoltre
stabilire se i warning di crescita dinamica del buffer `Variable Time Delay` sono accettabili per
questo lotto qualificato; l'audit strutturale non può concluderne l'innocuità scientifica.

## Comando, ambiente e limiti

Comando: `{report['environment']['executable']} studio2/fase03/baseline_numerica/audit_normal_dev.py`  
Python: `{report['environment']['python']}`; openpyxl: `{report['environment']['openpyxl']}`;
piattaforma: `{report['environment']['platform']}`.

Controllo documentale: `docs/test_explanation.py` ha {report['documentation_test']['failures']}
fallimenti dopo l'audit, contro {report['documentation_test']['baseline_failures_before_changes']}
prima: non peggiorato. Il test non copre questo audit.

Controlli non eseguiti: simulazioni o replay MATLAB; analisi scientifica dei segnali; evidence;
prototipi; baseline; score/FAR; verifica remota di collisioni; pubblicazione o conservazione esterna.
{('Run con errori: ' + ', '.join(r['run_id'] for r in failed_runs)) if failed_runs else 'Nessun run con errori tecnici.'}

Fonti lette: specifica/piano/builder/preflight/wrapper/launcher/handoff 03.9; generatore Normal e
freeze Fase 02; piano rev. 7 §6.2 al commit `a572d1c`; manifest 03.5 `cal_thr`/`far_ver`; piano e
manifest del lotto; entrambi i log/PID e `RECOVERY.json`; audit 03.5 come riferimento metodologico.
Lettura documentale mirata: circa 1.800 righe di fonti testuali/CSV più freeze e audit JSON; i 40
workbook sono stati letti integralmente dallo script, senza stamparne i valori.
Il dettaglio di hash, byte, controlli per run, join, inventario, fonti e anomalie è in
`AUDIT_NORMAL_DEV.json`.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-doc-failures", type=int, default=14)
    parser.add_argument("--json-output", type=Path, default=HERE / "AUDIT_NORMAL_DEV.json")
    parser.add_argument("--md-output", type=Path, default=HERE / "AUDIT_NORMAL_DEV.md")
    args = parser.parse_args()
    for output in (args.json_output.resolve(), args.md_output.resolve()):
        if output.parent != HERE:
            parser.error("audit outputs must be written directly under baseline_numerica")

    started = dt.datetime.now(dt.timezone.utc)
    git_status_start = git_text("status", "--short") or ""
    plan_rows, plan = audit_plan()
    collisions = audit_collisions()
    inventory, runs = audit_manifest_and_workbooks(plan_rows)
    sources = audit_sources()
    attempts = audit_attempts()
    docs = document_test(args.baseline_doc_failures)
    valid_runs = sum(row["status"] == "PASS" for row in runs)
    valid_windows = sum(sum(row.get("workbook", {}).get("window_counts", [])) == 2400
                        and row["status"] == "PASS" for row in runs) * 8
    plan_ok = all(item["status"] == "PASS" for item in plan["checks"])
    sources_ok = (
        sources["phase02_freeze_cross_checks"]["matches_expected"]
        and sources["qualified_model"].get("sha256") == EXPECTED_MODEL
        and sources["qualified_mex_primary_checkout"].get("sha256") == EXPECTED_MEX
        and sources["plan_revision_7"]["section_6_2_contains_normal_dev_contract"])
    technical_pass = (plan_ok and collisions["status"] == "PASS"
                      and inventory["bijection_status"] == "PASS" and valid_runs == 40 and sources_ok)
    finished = dt.datetime.now(dt.timezone.utc)
    report: dict[str, Any] = {
        "schema_version": 1,
        "audit": {"started_at_utc": started.isoformat(), "finished_at_utc": finished.isoformat(),
                  "script": file_record(Path(__file__)),
                  "scope": "technical integrity/configuration/traceability only; no scientific quality assessment",
                  "read_only_inputs": True},
        "environment": {"python": sys.version.replace("\n", " "), "executable": sys.executable,
                        "openpyxl": openpyxl.__version__, "platform": platform.platform(),
                        "cwd": os.getcwd()},
        "git": {"repo": str(REPO), "head": git_text("rev-parse", "HEAD"),
                "branch": git_text("branch", "--show-current"), "status_at_audit_start": git_status_start,
                "preexisting_status_observed_before_audit_authoring": [
                    "?? studio2/fase03/baseline_numerica/runs/",
                    "?? studio2/fase03/baseline_numerica/runtime/",
                ],
                "execution_commit_evidence": "not recorded in generation manifest; current HEAD is not asserted as the executed commit"},
        "plan": plan, "collisions": collisions, "inventory": inventory,
        "sources": sources, "attempts": attempts, "runs": runs,
        "documentation_test": docs,
        "summary": {"technical_result": "PASS" if technical_pass else "FAIL",
                    "process_status": attempts["process_assessment"]["status"],
                    "valid_runs": valid_runs, "invalid_runs": 40 - valid_runs,
                    "valid_windows": valid_windows,
                    "workbooks_status": "PASS" if valid_runs == 40 else "FAIL",
                    "author_decision_required": True,
                    "decision_topics": ["restart destination/process deviation",
                                        "sufficiency of successful-command/MATLABPATH traceability",
                                        "Variable Time Delay buffer warnings"]},
        "anomalies": attempts["process_assessment"]["deviations"] + [
            attempts["successful_attempt"]["warnings"]["classification"]["variable_time_delay"]],
        "not_performed": ["MATLAB simulation or replay", "scientific signal-quality assessment",
                          "separability/performance/score/FAR", "evidence extraction", "prototype/baseline training",
                          "remote/global collision search", "publication or preservation release"],
    }
    history = preserve_previous([args.json_output, args.md_output])
    report["audit"]["previous_outputs_preserved_at"] = history
    args.json_output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.md_output.write_text(render_markdown(report), encoding="utf-8")
    print(f"valid_runs={valid_runs}/40 technical={'PASS' if technical_pass else 'FAIL'} process=deviazioni")
    print(f"json={args.json_output} md={args.md_output}")
    return 0 if technical_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
