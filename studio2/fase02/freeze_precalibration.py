#!/usr/bin/env python3
"""Create the content-addressed pre-calibration freeze candidate for Fase 02."""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    phase_dir = Path(__file__).resolve().parent
    repo_root = phase_dir.parents[1]
    output = args.output.resolve()
    try:
        output.relative_to(repo_root / "studio2")
    except ValueError:
        parser.error("output must remain below studio2/")
    if output.exists():
        parser.error(f"refusing to overwrite {output}")

    relative_paths = [
        "docs/lit_review/DECISIONE_calibrazione_soglie_fase_B.md",
        "docs/paper/FoT_TEP_Review_Piano_Sperimentale.md",
        "studio2/PROVENIENZA.md",
        "studio2/fase02/ARTIFACT_STORAGE.json",
        "studio2/fase02/MANIFEST_CONSERVAZIONE.csv",
        "studio2/fase02/QUALIFICAZIONE_RIUSO.md",
        "studio2/fase02/SIMULATOR_PROVENIENZA.md",
        "studio2/fase02/SPECIFICA_GENERAZIONE.md",
        "studio2/fase02/generation_spec.json",
        "studio2/fase02/preserve_legacy_data.py",
        "studio2/fase02/build_generation_plan.py",
        "studio2/fase02/freeze_precalibration.py",
        "studio2/fase02/analysis/combined_score.py",
        "studio2/fase02/analysis/tep_features.py",
        "studio2/fase02/analysis/validate_numerics.py",
        "studio2/fase02/tests/fixtures/runtime_smoke_plan.csv",
        "studio2/fase02/tests/test_combined_score.py",
        "studio2/fase02/tests/test_generation_plan.py",
        "studio2/fase02/validation/score_fit_legacy.json",
        "studio2/fase02/simulator/source/temexd_philox.c",
        "studio2/fase02/simulator/source/philox4x32.h",
        "studio2/fase02/simulator/source/philox_kat.c",
        "studio2/fase02/simulator/source/teprob_mod.h",
        "studio2/fase02/simulator/matlab/MultiLoop_mode1.mdl",
        "studio2/fase02/simulator/matlab/tesys.mdl",
        "studio2/fase02/simulator/matlab/TElib.mdl",
        "studio2/fase02/simulator/matlab/Mode_1_Init.m",
        "studio2/fase02/simulator/matlab/Mode1xInitial.mat",
        "studio2/fase02/simulator/matlab/TEplot.m",
        "studio2/fase02/simulator/matlab/compile_philox.m",
        "studio2/fase02/simulator/matlab/generate_normal_runs.m",
        "studio2/fase02/simulator/matlab/generate_legacy_normal_runs.m",
        "studio2/fase02/validation/plans/burnin_qual.csv",
        "studio2/fase02/validation/plans/philox_legacy_qual.csv",
        "studio2/fase02/validation/plans/legacy_generator_qual.csv",
        "studio2/fase02/validation/plans/prefix_qual.csv",
        "studio2/fase02/validation/plans/r2_pilot.csv",
        "studio2/fase02/validation/burn_in_result_v2.json",
        "studio2/fase02/validation/generator_comparison_result_v2.json",
        "studio2/fase02/validation/prefix_result_v2.json",
        "studio2/fase02/validation/r2_guard_result_v2.json",
    ]
    files = {}
    for relative in relative_paths:
        path = repo_root / relative
        if not path.is_file():
            raise FileNotFoundError(path)
        files[relative] = {"sha256": sha256(path), "bytes": path.stat().st_size}

    mex_path = phase_dir / "simulator/build/temexd_philox.mexmaca64"
    manifests = []
    for relative in [
        "studio2/fase02/validation/data_v2/burnin_qual/generation_manifest.csv",
        "studio2/fase02/validation/data_v2/philox_legacy_qual/generation_manifest.csv",
        "studio2/fase02/validation/data_v2/prefix_qual/generation_manifest.csv",
        "studio2/fase02/validation/data_v2/r2_pilot/generation_manifest.csv",
        "studio2/fase02/validation/data/legacy_generator_qual/generation_manifest.csv",
    ]:
        path = repo_root / relative
        manifests.append({"path": relative, "sha256": sha256(path)})

    payload = {
        "schema_version": 2,
        "status": "content_frozen_and_data_archived_pending_independent_reverification_and_commit",
        "source_head_commit": subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=repo_root, text=True
        ).strip(),
        "selected_burn_in_hours": 20,
        "score_variant": "A",
        "score_threshold": None,
        "calibration_rank": None,
        "calibration_size": None,
        "exceedance_rule_after_calibration": "S > threshold",
        "artifact_storage_record": "studio2/fase02/ARTIFACT_STORAGE.json",
        "files": files,
        "local_mex": {
            "path": "studio2/fase02/simulator/build/temexd_philox.mexmaca64",
            "sha256": sha256(mex_path),
            "tracked": False,
            "rebuild_required_on_other_platforms": True,
        },
        "executed_manifests": manifests,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"OK: {output.relative_to(repo_root)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
