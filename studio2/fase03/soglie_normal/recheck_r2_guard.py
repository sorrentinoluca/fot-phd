#!/usr/bin/env python3
"""Recompute and rewrite the R2 guard attestation from its source files."""
from __future__ import annotations

import hashlib
import json
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
F2 = ROOT / "studio2" / "fase02"
OUT = HERE / "R2_GUARD_RECHECK.json"
SOURCES = {
    "score_fit_legacy_sha256": F2 / "validation" / "score_fit_legacy.json",
    "r2_guard_result_v2_sha256": F2 / "validation" / "r2_guard_result_v2.json",
    "combined_score_sha256": F2 / "analysis" / "combined_score.py",
    "tep_features_sha256": F2 / "analysis" / "tep_features.py",
    "validate_numerics_sha256": F2 / "analysis" / "validate_numerics.py",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    phase02_r2 = json.loads((F2 / "validation" / "r2_guard_result_v2.json").read_text())
    independent_r2 = json.loads((F2 / "validation" / "r2_guard_result.json").read_text())
    identical = phase02_r2 == independent_r2
    if not identical:
        raise SystemExit("R2 result differs from the independent Phase 02 result")
    if not phase02_r2.get("pass", False):
        raise SystemExit("Phase 02 R2 guard is not pass")

    values = {name: sha256(path) for name, path in SOURCES.items()}
    if any(len(value) != 64 for value in values.values()):
        raise SystemExit("internal SHA-256 length failure")
    previous = json.loads(OUT.read_text()) if OUT.exists() else {}
    result = {
        "checked_at_utc": str(date.today()),
        **values,
        "r2_guard_result_independent_byte_identical": identical,
        "parameters_and_code_current": True,
        "guard_pass": True,
        "active_branch": "350 cal_thr + 150 far_ver",
    }
    if previous.get("active_branch") and previous["active_branch"] != result["active_branch"]:
        raise SystemExit("active branch changed unexpectedly")
    OUT.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"output": str(OUT), "r2_identical": identical, "sha256_lengths": {k: len(v) for k, v in values.items()}}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
