#!/usr/bin/env python3
"""Fail-closed, label-blind EXP3_V2 verbalization harness.

The production CLI is intentionally usable only after the harness manifest has
been frozen and the annotated harness tag exists at the checked-out HEAD.
"""

from __future__ import annotations

import argparse
import ast
import hashlib
import importlib.metadata
import json
import math
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "code"
if str(CODE) not in sys.path:
    sys.path.insert(0, str(CODE))

DEFAULT_MANIFEST = Path(__file__).with_name(
    "EXP3_V2_VERBALIZATION_HARNESS_MANIFEST_001.json"
)
OUTPUT_MANIFEST_NAME = "EXP3_V2_VERBALIZATION_OUTPUT_MANIFEST_001.json"
STRUCTURED_DIR_NAME = "structured_json"
NEUTRAL_DIR_NAME = "neutral_text"
FROZEN_STATUS = "HARNESS_FROZEN_FOR_VERBALIZATION"
PRODUCTION_KIND = "EXP3_V2_VERBALIZATION_HARNESS_FREEZE"
NETWORK_AUDIT_EVENTS = {
    "socket.__new__",
    "socket.bind",
    "socket.connect",
    "socket.connect_ex",
    "socket.getaddrinfo",
}
FORBIDDEN_IMPORT_ROOTS = {
    "aiohttp",
    "anthropic",
    "httpx",
    "openai",
    "random",
    "requests",
    "secrets",
    "socket",
    "urllib",
}
XMEAS = [f"XMEAS-{index}" for index in range(1, 42)]


class HarnessError(RuntimeError):
    """A fail-closed harness contract violation."""


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise HarnessError(f"JSON object required: {path}")
    return value


def canonical_json(value: Any) -> str:
    return (
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n"
    )


def safe_relative_path(value: str, *, label: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise HarnessError(f"{label} must be a canonical relative path: {value!r}")
    if str(path) != value or any(part in {"", "."} for part in path.parts):
        raise HarnessError(f"{label} is not canonical: {value!r}")
    return path


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    if completed.returncode:
        raise HarnessError(
            f"git {' '.join(args)} failed in {repo}: {completed.stderr.strip()}"
        )
    return completed.stdout.strip()


def _verify_annotated_tag(repo: Path, boundary: dict[str, Any]) -> None:
    tag = boundary["tag"]
    ref = f"refs/tags/{tag}"
    if _git(repo, "cat-file", "-t", ref) != "tag":
        raise HarnessError(f"{tag} must resolve to an annotated tag object")
    if _git(repo, "rev-parse", ref) != boundary["tag_object"]:
        raise HarnessError(f"annotated tag object mismatch: {tag}")
    if _git(repo, "rev-parse", f"{ref}^{{}}") != boundary["commit"]:
        raise HarnessError(f"peeled tag target mismatch: {tag}")


def _verify_production_checkout(
    manifest: dict[str, Any], manifest_path: Path, data_root: Path
) -> None:
    if manifest["status"] != FROZEN_STATUS or not manifest["tag_created"]:
        raise HarnessError("draft harness cannot execute; freeze approval is required")

    harness_root = Path(_git(manifest_path.parent, "rev-parse", "--show-toplevel"))
    harness_boundary = {
        "tag": manifest["prospective_tag"],
        "tag_object": _git(
            harness_root, "rev-parse", f"refs/tags/{manifest['prospective_tag']}"
        ),
        "commit": _git(
            harness_root, "rev-parse", f"refs/tags/{manifest['prospective_tag']}^{{}}"
        ),
    }
    _verify_annotated_tag(harness_root, harness_boundary)
    if _git(harness_root, "rev-parse", "HEAD") != harness_boundary["commit"]:
        raise HarnessError("harness worktree HEAD is not the frozen harness tag target")
    if _git(harness_root, "status", "--porcelain", "--untracked-files=all"):
        raise HarnessError("harness worktree must be completely clean")

    source = manifest["boundaries"]["source"]
    _verify_annotated_tag(harness_root, source)

    data_repository = Path(_git(data_root, "rev-parse", "--show-toplevel"))
    if data_repository.resolve() != data_root.resolve():
        raise HarnessError("data root must be the top level of its clean checkout")
    data = manifest["boundaries"]["data"]
    _verify_annotated_tag(data_root, data)
    if _git(data_root, "rev-parse", "HEAD") != data["commit"]:
        raise HarnessError("data checkout HEAD is not the frozen data tag target")
    if _git(data_root, "status", "--porcelain", "--untracked-files=all"):
        raise HarnessError("data-tag checkout must be completely clean")


def _verify_runtime(manifest: dict[str, Any]) -> dict[str, str]:
    runtime = manifest["python_runtime"]
    observed_executable = str(Path(sys.executable).resolve())
    if observed_executable != runtime["canonical_executable"]:
        raise HarnessError(
            "wrong Python executable: "
            f"expected {runtime['canonical_executable']}, got {observed_executable}"
        )
    observed = {"python": ".".join(map(str, sys.version_info[:3]))}
    for package in runtime["packages"]:
        try:
            observed[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError as exc:
            raise HarnessError(f"required package is missing: {package}") from exc
    expected = {"python": runtime["python_version"], **runtime["packages"]}
    if observed != expected:
        raise HarnessError(f"Python dependency mismatch: {observed!r} != {expected!r}")
    return observed


def _verify_file(path: Path, record: dict[str, Any], *, label: str) -> None:
    if path.is_symlink() or not path.is_file():
        raise HarnessError(f"{label} must be a regular non-symlink file: {path}")
    if path.stat().st_size != int(record["size_bytes"]):
        raise HarnessError(f"{label} size mismatch: {path}")
    if sha256_file(path) != record["sha256"]:
        raise HarnessError(f"{label} SHA-256 mismatch: {path}")


def _verify_frozen_assets(manifest: dict[str, Any], root: Path) -> None:
    source = manifest["boundaries"]["source"]
    for record in manifest["frozen_assets"]:
        relative = safe_relative_path(record["path"], label="frozen asset path")
        local_path = root / relative
        _verify_file(local_path, record, label="frozen asset")
        blob = subprocess.run(
            ["git", "-C", str(root), "show", f"{source['tag']}:{relative}"],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if (
            blob.returncode
            or hashlib.sha256(blob.stdout).hexdigest() != record["sha256"]
        ):
            raise HarnessError(f"source-tag blob mismatch: {relative}")

    for record in manifest["harness_artifacts"]:
        relative = safe_relative_path(record["path"], label="harness artifact path")
        _verify_file(root / relative, record, label="harness artifact")


def _verify_static_prohibitions(manifest: dict[str, Any], root: Path) -> None:
    paths = [record["path"] for record in manifest["frozen_assets"]]
    paths.append("phase_b/exp3_v2/run_exp3v2_verbalization.py")
    for relative in paths:
        path = root / safe_relative_path(relative, label="policy scan path")
        if path.suffix != ".py":
            continue
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            names: list[str] = []
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            for name in names:
                if name.split(".")[0] in FORBIDDEN_IMPORT_ROOTS:
                    raise HarnessError(f"prohibited import {name!r} in {relative}")

    runner_path = root / "phase_b/exp3_v2/run_exp3v2_verbalization.py"
    runner_tree = ast.parse(
        runner_path.read_text(encoding="utf-8"), filename=str(runner_path)
    )
    prohibited_call_names = {
        "compute_baseline_stats",
        "load_development_baseline",
        "calibrate_thresholds",
    }
    for node in ast.walk(runner_tree):
        if not isinstance(node, ast.Call):
            continue
        function = node.func
        name = function.id if isinstance(function, ast.Name) else None
        if name in prohibited_call_names:
            raise HarnessError(f"runner calls prohibited operation: {name}")
        if isinstance(function, ast.Attribute) and function.attr == "random":
            raise HarnessError("runner calls a prohibited random-number API")


def _install_network_block() -> None:
    def reject_network(event: str, _args: tuple[Any, ...]) -> None:
        if event in NETWORK_AUDIT_EVENTS:
            raise HarnessError(f"network operation prohibited by harness: {event}")

    sys.addaudithook(reject_network)


def _load_frozen_api() -> tuple[Any, Any, Any, Any]:
    from tep_features import load_case
    from tep_verbalize_v2 import load_config, render_text, verbalize_case

    return load_case, load_config, render_text, verbalize_case


def _load_baseline(manifest: dict[str, Any], root: Path) -> Any:
    record = manifest["baseline_statistics"]
    path = root / safe_relative_path(record["path"], label="baseline path")
    _verify_file(path, record, label="baseline statistics")
    value = load_json(path)
    if value["status"] != "FROZEN_DEVELOPMENT_BASELINE_STATISTICS":
        raise HarnessError("baseline statistics are not frozen")
    if value["variables"] != XMEAS:
        raise HarnessError("baseline variables differ from XMEAS-1..41")
    arrays: dict[str, list[float]] = {}
    for name in ("mean", "std", "diff_std", "residual_std"):
        observed = value[name]
        if len(observed) != len(XMEAS) or not all(
            isinstance(item, (int, float)) and math.isfinite(item) for item in observed
        ):
            raise HarnessError(f"invalid frozen baseline vector: {name}")
        arrays[name] = [float(item) for item in observed]
    for name in ("std", "diff_std", "residual_std"):
        if not all(item > 0 for item in arrays[name]):
            raise HarnessError(f"non-positive frozen baseline vector: {name}")

    import pandas as pd
    from tep_features import BaselineStats

    return BaselineStats(
        mean=pd.Series(arrays["mean"], index=XMEAS, dtype=float),
        std=pd.Series(arrays["std"], index=XMEAS, dtype=float),
        diff_std=pd.Series(arrays["diff_std"], index=XMEAS, dtype=float),
        residual_std=pd.Series(arrays["residual_std"], index=XMEAS, dtype=float),
    )


def _load_and_verify_inputs(
    manifest: dict[str, Any], data_root: Path
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    boundary = manifest["boundaries"]["data"]
    relative_manifest = safe_relative_path(
        boundary["manifest_path"], label="data-freeze manifest path"
    )
    freeze_path = data_root / relative_manifest
    _verify_file(
        freeze_path,
        {
            "size_bytes": boundary["manifest_size_bytes"],
            "sha256": boundary["manifest_sha256"],
        },
        label="data-freeze manifest",
    )
    freeze = load_json(freeze_path)
    rows = freeze["data_artifacts"]["workbook_inventory"]
    aggregate = freeze["data_artifacts"]["aggregate_digests"]
    if aggregate["inventory_sha256"] != manifest["inputs"]["input_inventory_sha256"]:
        raise HarnessError("frozen input inventory digest mismatch")
    if (
        aggregate["concatenated_workbook_bytes_sha256"]
        != manifest["inputs"]["concatenated_workbook_bytes_sha256"]
    ):
        raise HarnessError("frozen concatenated-workbook digest mismatch")
    expected_ids = manifest["inputs"]["canonical_case_ids"]
    if len(rows) != 30 or [row["physical_case_id"] for row in rows] != expected_ids:
        raise HarnessError("input identities or canonical order differ from the freeze")
    if [row["order"] for row in rows] != list(range(1, 31)):
        raise HarnessError("input order must be exactly 1..30")
    if any(row["attempt"] != 0 for row in rows):
        raise HarnessError("only attempt-0 inputs are eligible")
    if [row["seed"] for row in rows] != list(range(320001, 320031)):
        raise HarnessError("input seeds must be exactly 320001..320030")

    expected_paths: set[str] = set()
    expected_names: set[str] = set()
    for row in rows:
        relative = safe_relative_path(row["path"], label="workbook path")
        if relative.name != row["filename"]:
            raise HarnessError(f"filename/path mismatch for {row['physical_case_id']}")
        expected_filename = f"{row['physical_case_id']}__attempt-0.xlsx"
        if row["filename"] != expected_filename:
            raise HarnessError(f"non-canonical filename for {row['physical_case_id']}")
        if relative.name in expected_names or str(relative) in expected_paths:
            raise HarnessError("duplicate workbook identity")
        expected_names.add(relative.name)
        expected_paths.add(str(relative))
        _verify_file(data_root / relative, row, label="input workbook")

    input_directory = data_root / safe_relative_path(
        manifest["inputs"]["workbook_directory"], label="workbook directory"
    )
    if input_directory.is_symlink() or not input_directory.is_dir():
        raise HarnessError("workbook directory must be a regular directory")
    observed_entries = list(input_directory.iterdir())
    observed_names = {path.name for path in observed_entries}
    if observed_names != expected_names:
        raise HarnessError(
            "workbook directory is partial or contains extra files: "
            f"missing={sorted(expected_names - observed_names)}, "
            f"extra={sorted(observed_names - expected_names)}"
        )
    if any(path.is_symlink() or not path.is_file() for path in observed_entries):
        raise HarnessError(
            "non-regular entries are prohibited in the workbook directory"
        )
    return freeze, rows


def _validate_result(
    result: dict[str, Any], config: dict[str, Any], render_text: Any
) -> None:
    if set(result) != {"structured", "text"}:
        raise HarnessError("verbalizer interface changed")
    structured = result["structured"]
    contract = (10.0, 50.0, 5.0, 8)
    observed = (
        *map(float, structured["time_range_h"]),
        float(structured["window_hours"]),
        int(structured["n_windows"]),
    )
    if observed != contract:
        raise HarnessError(f"window contract mismatch: {observed!r} != {contract!r}")
    starts = [10.0 + 5.0 * index for index in range(8)]
    ends = [value + 5.0 for value in starts]
    if set(structured["variables"]) != set(XMEAS):
        raise HarnessError("structured output must contain exactly 41 XMEAS")
    for variable in XMEAS:
        windows = structured["variables"][variable]["per_window"]
        if [float(row["start_h"]) for row in windows] != starts:
            raise HarnessError(f"window starts changed for {variable}")
        if [float(row["end_h"]) for row in windows] != ends:
            raise HarnessError(f"window ends changed for {variable}")
    if structured["thresholds"] != config["thresholds"]:
        raise HarnessError("frozen thresholds changed")
    if render_text(structured) != result["text"]:
        raise HarnessError("neutral text is not the frozen renderer output")
    canonical_json(structured)


def _prepare_output_root(output_root: Path, data_root: Path) -> None:
    if output_root.exists() or output_root.is_symlink():
        raise HarnessError("output root must not exist; overwrite is prohibited")
    parent = output_root.parent
    if parent.is_symlink() or not parent.is_dir():
        raise HarnessError("output parent must be an existing non-symlink directory")
    resolved = output_root.resolve(strict=False)
    if resolved.is_relative_to(data_root.resolve()) or resolved.is_relative_to(
        ROOT.resolve()
    ):
        raise HarnessError("output root must be outside source and data worktrees")


def _write_text(path: Path, value: str) -> None:
    with path.open("x", encoding="utf-8", newline="\n") as stream:
        stream.write(value)


def execute_harness(
    manifest_path: Path,
    data_root: Path,
    output_root: Path,
    *,
    enforce_repository_boundaries: bool = True,
) -> dict[str, Any]:
    if data_root.is_symlink():
        raise HarnessError("data root must not be a symlink")
    manifest_path = manifest_path.resolve()
    data_root = data_root.resolve()
    output_root = output_root.resolve(strict=False)
    manifest = load_json(manifest_path)
    if manifest.get("manifest_kind") != PRODUCTION_KIND:
        raise HarnessError("unexpected harness manifest kind")
    if manifest.get("status") != FROZEN_STATUS:
        raise HarnessError("PRE_FREEZE_DRAFT is deliberately non-executable")
    if enforce_repository_boundaries:
        _verify_production_checkout(manifest, manifest_path, data_root)

    runtime = _verify_runtime(manifest)
    _verify_frozen_assets(manifest, ROOT)
    _verify_static_prohibitions(manifest, ROOT)
    load_case, load_config, render_text, verbalize_case = _load_frozen_api()
    config_record = next(
        record
        for record in manifest["frozen_assets"]
        if record["path"] == "code/verbalizer_config_v2.json"
    )
    config = load_config(ROOT / config_record["path"])
    baseline = _load_baseline(manifest, ROOT)
    freeze, rows = _load_and_verify_inputs(manifest, data_root)
    _prepare_output_root(output_root, data_root)

    pre_hashes = {row["path"]: sha256_file(data_root / row["path"]) for row in rows}
    created = False
    try:
        output_root.mkdir()
        created = True
        structured_root = output_root / STRUCTURED_DIR_NAME
        neutral_root = output_root / NEUTRAL_DIR_NAME
        structured_root.mkdir()
        neutral_root.mkdir()
        _install_network_block()

        entries: list[dict[str, Any]] = []
        inventory = hashlib.sha256()
        for row in rows:
            case_id = row["physical_case_id"]
            source = data_root / row["path"]
            result = verbalize_case(
                load_case(source),
                baseline,
                config=config,
                start_h=10.0,
                end_h=50.0,
            )
            _validate_result(result, config, render_text)
            structured = structured_root / f"{case_id}.json"
            neutral = neutral_root / f"{case_id}.txt"
            _write_text(structured, canonical_json(result["structured"]))
            _write_text(neutral, result["text"] + "\n")
            entry = {
                "order": row["order"],
                "physical_case_id": case_id,
                "source_path": row["path"],
                "source_size_bytes": row["size_bytes"],
                "source_sha256": row["sha256"],
                "structured_path": f"{STRUCTURED_DIR_NAME}/{structured.name}",
                "structured_size_bytes": structured.stat().st_size,
                "structured_sha256": sha256_file(structured),
                "neutral_text_path": f"{NEUTRAL_DIR_NAME}/{neutral.name}",
                "neutral_text_size_bytes": neutral.stat().st_size,
                "neutral_text_sha256": sha256_file(neutral),
            }
            inventory.update(
                (
                    f"{case_id},{entry['structured_path']},"
                    f"{entry['structured_size_bytes']},{entry['structured_sha256']},"
                    f"{entry['neutral_text_path']},"
                    f"{entry['neutral_text_size_bytes']},{entry['neutral_text_sha256']}\n"
                ).encode("utf-8")
            )
            entries.append(entry)

        post_hashes = {
            row["path"]: sha256_file(data_root / row["path"]) for row in rows
        }
        if post_hashes != pre_hashes:
            raise HarnessError("a source workbook changed during verbalization")

        output_manifest = {
            "schema_version": "1.0",
            "status": "COMPLETE_PENDING_VERBALIZATION_DATA_FREEZE",
            "harness_tag": manifest["prospective_tag"],
            "source_tag": manifest["boundaries"]["source"]["tag"],
            "data_tag": manifest["boundaries"]["data"]["tag"],
            "data_freeze_manifest_path": manifest["boundaries"]["data"][
                "manifest_path"
            ],
            "data_freeze_manifest_sha256": sha256_file(
                data_root / manifest["boundaries"]["data"]["manifest_path"]
            ),
            "input_inventory_sha256": freeze["data_artifacts"]["aggregate_digests"][
                "inventory_sha256"
            ],
            "runtime": runtime,
            "window_contract": manifest["window_contract"],
            "case_count": 30,
            "structured_output_directory": STRUCTURED_DIR_NAME,
            "neutral_text_output_directory": NEUTRAL_DIR_NAME,
            "output_inventory_sha256": inventory.hexdigest(),
            "cases": entries,
        }
        _write_text(output_root / OUTPUT_MANIFEST_NAME, canonical_json(output_manifest))

        from verify_exp3v2_verbalizations import verify_outputs

        errors = verify_outputs(manifest_path, data_root, output_root)
        if errors:
            raise HarnessError(
                "post-verbalization verification failed: " + "; ".join(errors)
            )
        return output_manifest
    except BaseException:
        if created and output_root.is_dir() and not output_root.is_symlink():
            shutil.rmtree(output_root)
        raise


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = execute_harness(args.manifest, args.data_root, args.output_root)
    print(
        canonical_json(
            {
                "result": "PASS",
                "cases": result["case_count"],
                "output_manifest": str(args.output_root / OUTPUT_MANIFEST_NAME),
                "output_inventory_sha256": result["output_inventory_sha256"],
            }
        ),
        end="",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
