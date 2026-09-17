"""Balanced random assignment of one 5 h window per run of the 03.11 test lot (D1).

Normative source: ``DECISIONI_AUTORE_7_3_REV2_2026-09-17.md`` D1
(SHA-256 ``535939de1d8c1e6f8185fd838a6bd20caca85b5f09c7908f679f251761aaccb2``).

Every run of the test lot contributes exactly one case: one of the eight useful 5 h
windows of ``[25, 65)``.  For each fault, and for ``Normal``, the eight temporal
positions are assigned to the eight runs by a random permutation with a frozen seed;
for the two OOD faults (three runs each) three distinct positions are drawn from the
same generator with the same rule.

The assignment is built from **identifiers only** -- the sealed run plan of 03.11 --
and never reads a signal, an evidence unit or any test content (D1: the assignment
precedes opening the test data).  It is identical across conditions (A, B-LF, E-LF,
B-noLF), recipients, library role and repetitions.
"""

from __future__ import annotations

import csv
import io
import json
import subprocess
from pathlib import Path
from typing import Any, Iterable

from .common import HarnessError, canonical_json, sha256_text

ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = Path(__file__).resolve().parents[3]

# --- frozen generator (proposed by 7.4-FIX, mirrors the style of protocol Sec.7.1) ----
NAMESPACE = "studio2-fase03-window-assignment-v1"
SEED = 20260917
BIT_GENERATOR = "numpy.random.PCG64"
PERMUTATION_CALL = (
    "Generator.permutation(8) over the eight position indices, once per fault group, "
    "groups visited in ascending lexicographic order of the group key; for a three-run "
    "OOD group the first three values of the same permutation are used"
)

# --- frozen window geometry of 03.6 / 03.11 -------------------------------------------
ONSET_H = 25.0
WINDOW_H = 5.0
END_H = 65.0
POSITIONS = 8

# --- sealed identifier sources (03.11) -------------------------------------------------
# Chain: SIGILLO -> BATCH_AUDIT -> plan CSV. Only identifiers are read from them.
SEAL_PATH = "studio2/fase03/fault_runs/SIGILLO_LOTTO_03_11.json"
AUDIT_PATH = "studio2/fase03/fault_runs/BATCH_AUDIT_03_11.json"
PLAN_PATH = "studio2/fase03/fault_runs/plans/test_batch_f5.csv"
SEAL_SHA256 = "9bd02e900429e971c08cbb8fc81f5dec54b8dcfb30b90e19faf622bb8558739d"
AUDIT_SHA256 = "420a61eb65a47961092ee042f7fa08797a25b350f875cad76c0954f7f3eeb6e3"
PLAN_SHA256 = "ef0b28529b6a48932d6fb7483c1fef44e331db089f284cc3d7a06a6e20879572"
# The 03.11 lot was integrated into ``main`` after this branch forked at 540df7b; until
# the branches are joined the three sealed files are read from the local ``main`` ref.
IDENTIFIER_GIT_REF = "main"

SPARE_PREFIX = "test-spare-"


def _read_source(relative: str, expected_sha256: str, *, git_ref: str = IDENTIFIER_GIT_REF,
                 repo_root: Path = REPO_ROOT) -> tuple[str, str]:
    """Read one sealed identifier file and authenticate its bytes.

    The working tree is preferred; when the file is not checked out on this branch the
    blob is read from the local ``git_ref``.  Either way the SHA-256 must match, so the
    source never changes what is assigned.
    """
    path = repo_root / relative
    text: str | None = None
    source = ""
    if path.is_file():
        text = path.read_text(encoding="utf-8")
        source = f"worktree:{relative}"
    else:
        try:
            raw = subprocess.run(
                ["git", "show", f"{git_ref}:{relative}"],
                cwd=str(repo_root), check=True, capture_output=True,
            ).stdout
        except (OSError, subprocess.CalledProcessError) as exc:  # pragma: no cover
            raise HarnessError(
                f"sealed identifier source is unavailable: {relative} ({exc})") from exc
        text = raw.decode("utf-8")
        source = f"git:{git_ref}:{relative}"
    observed = sha256_text(text)
    if observed != expected_sha256:
        raise HarnessError(
            f"sealed identifier source changed: {relative} expected {expected_sha256}, "
            f"got {observed}")
    return text, source


def sealed_sources(*, git_ref: str = IDENTIFIER_GIT_REF, repo_root: Path = REPO_ROOT):
    """Return the seal, the batch audit and the run plan under a verified hash chain."""
    seal_text, seal_source = _read_source(SEAL_PATH, SEAL_SHA256, git_ref=git_ref, repo_root=repo_root)
    audit_text, audit_source = _read_source(AUDIT_PATH, AUDIT_SHA256, git_ref=git_ref, repo_root=repo_root)
    plan_text, plan_source = _read_source(PLAN_PATH, PLAN_SHA256, git_ref=git_ref, repo_root=repo_root)
    seal = json.loads(seal_text)
    audit = json.loads(audit_text)
    if seal["test_batch"]["audit"]["sha256"] != AUDIT_SHA256:
        raise HarnessError("the seal does not bind this batch audit")
    if audit["plan"]["sha256"] != PLAN_SHA256:
        raise HarnessError("the batch audit does not bind this run plan")
    rows = list(csv.DictReader(io.StringIO(plan_text)))
    return seal, audit, rows, {"seal": seal_source, "audit": audit_source, "plan": plan_source}


def verify_useful_windows(seal: dict[str, Any], audit: dict[str, Any],
                          rows: list[dict[str, str]]) -> dict[str, Any]:
    """D1 precondition: every run of the lot must carry eight useful windows.

    A run cannot exceed its declared window count -- the horizon [25, 65) at 5 h yields
    exactly eight half-open windows -- so when the lot declares eight per run, reports
    zero incomplete runs and the sealed total equals the expected total, every run has
    exactly eight.  Anything else is a STOP.
    """
    declared = {row["run_id"]: int(row["useful_windows_expected"]) for row in rows}
    off_spec = sorted(run for run, value in declared.items() if value != POSITIONS)
    counts = seal["test_batch"]["counts"]
    audit_counts = audit["generic_campaign_audit"]
    total_expected = sum(declared.values())
    problems: list[str] = []
    if off_spec:
        problems.append(f"{len(off_spec)} runs do not declare eight useful windows: {off_spec[:5]}")
    if counts["total"] != len(rows) or audit_counts["manifest_count"] != len(rows):
        problems.append("the sealed run count differs from the run plan")
    if counts["complete"] != counts["total"]:
        problems.append("the lot contains runs that are not complete")
    if counts["physical_trip"] or counts["technical_failure"] or counts["not_run"]:
        problems.append("the lot contains trips, technical failures or runs not executed")
    if counts["complete_windows"] != total_expected:
        problems.append(
            f"sealed useful windows {counts['complete_windows']} differ from the expected "
            f"{total_expected}")
    if audit_counts["useful_windows_complete"] != counts["complete_windows"]:
        problems.append("seal and batch audit disagree on the useful window count")
    if not audit_counts.get("hashes_verified") or not audit_counts.get("accepted"):
        problems.append("the batch audit is not an accepted, hash-verified campaign")
    return {
        "status": "PASS" if not problems else "STOP",
        "problems": problems,
        "runs": len(rows),
        "windows_per_run_declared": POSITIONS,
        "useful_windows_expected_total": total_expected,
        "useful_windows_sealed_total": counts["complete_windows"],
        "per_run_reverification": (
            "per-run counts are re-verified against generation_manifest.csv when the "
            "studio2-fase03-test-v1 release is downloaded (point 2); this check is the "
            "identifier-only precondition of D1"),
    }


def group_key(run_id: str) -> str:
    """``test-primary-F1-r03`` -> ``test-primary-F1``; the fault group of D1."""
    head, _, tail = run_id.rpartition("-")
    if not head or not tail.startswith("r"):
        raise HarnessError(f"unexpected run identifier: {run_id}")
    return head


def assignable_runs(rows: Iterable[dict[str, str]]) -> dict[str, list[str]]:
    """Group the assignable runs by fault, excluding the non-substitutive spares (D1)."""
    groups: dict[str, list[str]] = {}
    for row in rows:
        run_id = row["run_id"]
        if run_id.startswith(SPARE_PREFIX):
            continue
        groups.setdefault(group_key(run_id), []).append(run_id)
    for key, runs in groups.items():
        runs.sort()
        if len(runs) not in {POSITIONS, 3}:
            raise HarnessError(f"group {key} has {len(runs)} runs, expected eight or three")
        if len(set(runs)) != len(runs):
            raise HarnessError(f"group {key} repeats a run identifier")
    return dict(sorted(groups.items()))


def window_bounds(position: int) -> tuple[float, float]:
    start = ONSET_H + (position - 1) * WINDOW_H
    return start, start + WINDOW_H


def build_assignment(groups: dict[str, list[str]]) -> list[dict[str, Any]]:
    """One generator, one permutation per group, groups in lexicographic order."""
    import numpy

    generator = numpy.random.Generator(numpy.random.PCG64(SEED))
    assignment: list[dict[str, Any]] = []
    for key, runs in groups.items():
        order = generator.permutation(POSITIONS)
        positions = [int(value) + 1 for value in order[: len(runs)]]
        if len(set(positions)) != len(positions):
            raise HarnessError(f"group {key} received a repeated position")
        for run_id, position in zip(runs, positions):
            start, end = window_bounds(position)
            assignment.append({
                "case_id": run_id,
                "group": key,
                "window_ordinal": position,
                "window_start_h": start,
                "window_end_h": end,
            })
    assignment.sort(key=lambda row: row["case_id"])
    if len({row["case_id"] for row in assignment}) != len(assignment):
        raise HarnessError("a run received more than one window")
    return assignment


def position_table(assignment: Iterable[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """fault x position table; each position appears once per eight-run fault group."""
    table: dict[str, dict[str, Any]] = {}
    for row in assignment:
        table.setdefault(row["group"], {})[str(row["window_ordinal"])] = row["case_id"]
    for key, row in table.items():
        used = sorted(int(value) for value in row)
        if len(used) != len(set(used)):
            raise HarnessError(f"group {key} repeats a position")
        if len(used) == POSITIONS and used != list(range(1, POSITIONS + 1)):
            raise HarnessError(f"group {key} does not cover the eight positions exactly once")
    return dict(sorted(table.items()))


def assignment_artifact(*, git_ref: str = IDENTIFIER_GIT_REF,
                        repo_root: Path = REPO_ROOT) -> dict[str, Any]:
    import numpy

    seal, audit, rows, sources = sealed_sources(git_ref=git_ref, repo_root=repo_root)
    windows = verify_useful_windows(seal, audit, rows)
    if windows["status"] != "PASS":
        raise HarnessError("STOP: " + "; ".join(windows["problems"]))
    groups = assignable_runs(rows)
    assignment = build_assignment(groups)
    table = position_table(assignment)
    artifact = {
        "artifact_version": "ASSEGNAZIONE_FINESTRE_7_4_1",
        "status": "FROZEN_BEFORE_TEST_DATA",
        "decision": "DECISIONI_AUTORE_7_3_REV2_2026-09-17.md D1",
        "decision_sha256": "535939de1d8c1e6f8185fd838a6bd20caca85b5f09c7908f679f251761aaccb2",
        "name": "balanced random assignment by position, separately for each fault",
        "invariance": (
            "identical across conditions A, B-LF, E-LF, B-noLF, across recipient agents, "
            "library role G_P/G_A and the three repetitions"),
        "namespace": NAMESPACE,
        "seed": SEED,
        "bit_generator": BIT_GENERATOR,
        "permutation_call": PERMUTATION_CALL,
        "numpy_version": numpy.__version__,
        "group_order": list(groups),
        "window_geometry": {"onset_h": ONSET_H, "window_h": WINDOW_H, "end_h": END_H,
                            "positions": POSITIONS,
                            "position_1_is": "[25.0, 30.0) h, post-onset"},
        "sources": {
            "seal": {"path": SEAL_PATH, "sha256": SEAL_SHA256, "read_from": sources["seal"]},
            "batch_audit": {"path": AUDIT_PATH, "sha256": AUDIT_SHA256, "read_from": sources["audit"]},
            "run_plan": {"path": PLAN_PATH, "sha256": PLAN_SHA256, "read_from": sources["plan"]},
            "content_read": "run identifiers and declared window counts only; no signal, "
                            "no evidence, no test content",
        },
        "useful_windows_check": windows,
        "counts": {
            "assigned_runs": len(assignment),
            "groups": len(groups),
            "eight_run_groups": sum(1 for runs in groups.values() if len(runs) == POSITIONS),
            "three_run_groups": sum(1 for runs in groups.values() if len(runs) == 3),
            "excluded_spares": sum(1 for row in rows if row["run_id"].startswith(SPARE_PREFIX)),
        },
        "position_table": table,
        "assignment": assignment,
    }
    artifact["assignment_sha256"] = sha256_text(canonical_json(assignment))
    return artifact


def assignment_by_case(artifact: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {row["case_id"]: row for row in artifact["assignment"]}


def artifact_sha256(artifact: dict[str, Any]) -> str:
    return sha256_text(canonical_json(artifact))
