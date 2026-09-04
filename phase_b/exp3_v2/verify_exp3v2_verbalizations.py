#!/usr/bin/env python3
"""Portable mechanical verifier for EXP3_V2 verbalization outputs."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path, PurePosixPath
import sys
from typing import Any


OUTPUT_MANIFEST_NAME = "EXP3_V2_VERBALIZATION_OUTPUT_MANIFEST_001.json"
STRUCTURED_DIR_NAME = "structured_json"
NEUTRAL_DIR_NAME = "neutral_text"
HARNESS_ROOT = Path(__file__).resolve().parents[2]


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
        raise ValueError(f"JSON object required: {path}")
    return value


def relative(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if (
        path.is_absolute()
        or not path.parts
        or ".." in path.parts
        or str(path) != value
        or any(part in {"", "."} for part in path.parts)
    ):
        raise ValueError(f"non-canonical relative path: {value!r}")
    return path


def _check_file(path: Path, size: int, digest: str) -> str | None:
    if path.is_symlink() or not path.is_file():
        return f"missing, non-regular, or symlink file: {path}"
    if path.stat().st_size != int(size):
        return f"size mismatch: {path}"
    if sha256_file(path) != digest:
        return f"SHA-256 mismatch: {path}"
    return None


def _all_finite(value: Any) -> bool:
    if isinstance(value, float):
        return math.isfinite(value)
    if isinstance(value, dict):
        return all(_all_finite(item) for item in value.values())
    if isinstance(value, list):
        return all(_all_finite(item) for item in value)
    return True


def _load_hash_verified_render_text(harness_root: Path) -> Any:
    """Load render_text from the already hash-verified frozen source file."""
    module_path = harness_root / "code/tep_verbalize_v2.py"
    module_name = "_exp3v2_hash_verified_tep_verbalize_v2"
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise ValueError(f"cannot load frozen renderer: {module_path}")
    module = importlib.util.module_from_spec(spec)
    code_root = str(module_path.parent)
    inserted = code_root not in sys.path
    if inserted:
        sys.path.insert(0, code_root)
    try:
        spec.loader.exec_module(module)
    finally:
        if inserted:
            sys.path.remove(code_root)
    render_text = getattr(module, "render_text", None)
    if not callable(render_text):
        raise ValueError("frozen verbalizer does not expose callable render_text")
    return render_text


def verify_outputs(
    harness_manifest_path: Path, data_root: Path, output_root: Path
) -> list[str]:
    errors: list[str] = []
    try:
        if data_root.is_symlink():
            return ["data root must not be a symlink"]
        if output_root.is_symlink():
            return ["output root must not be a symlink"]
        harness_manifest_path = harness_manifest_path.resolve()
        harness_root = HARNESS_ROOT
        data_root = data_root.resolve()
        output_root = output_root.resolve()
        harness = load_json(harness_manifest_path)
        data_boundary = harness["boundaries"]["data"]
        data_manifest_path = data_root / relative(data_boundary["manifest_path"])
        error = _check_file(
            data_manifest_path,
            data_boundary["manifest_size_bytes"],
            data_boundary["manifest_sha256"],
        )
        if error:
            errors.append(error)
            return errors
        data_manifest = load_json(data_manifest_path)
        inputs = data_manifest["data_artifacts"]["workbook_inventory"]
        expected_ids = harness["inputs"]["canonical_case_ids"]

        for record in harness["frozen_assets"] + harness["harness_artifacts"]:
            path = harness_root / relative(record["path"])
            error = _check_file(path, record["size_bytes"], record["sha256"])
            if error:
                errors.append(error)

        if errors:
            return errors
        render_text = _load_hash_verified_render_text(harness_root)

        if (
            len(inputs) != 30
            or [row["physical_case_id"] for row in inputs] != expected_ids
        ):
            errors.append("input inventory identity/order mismatch")
        for row in inputs:
            try:
                path = data_root / relative(row["path"])
                error = _check_file(path, row["size_bytes"], row["sha256"])
                if error:
                    errors.append(error)
            except (KeyError, TypeError, ValueError) as exc:
                errors.append(f"invalid input record: {exc}")

        output_manifest_path = output_root / OUTPUT_MANIFEST_NAME
        if output_manifest_path.is_symlink() or not output_manifest_path.is_file():
            errors.append("output manifest is missing or not a regular file")
            return errors
        output = load_json(output_manifest_path)
        required_top = {
            "schema_version",
            "status",
            "harness_tag",
            "source_tag",
            "data_tag",
            "data_freeze_manifest_path",
            "data_freeze_manifest_sha256",
            "input_inventory_sha256",
            "runtime",
            "window_contract",
            "case_count",
            "structured_output_directory",
            "neutral_text_output_directory",
            "output_inventory_sha256",
            "cases",
        }
        if set(output) != required_top:
            errors.append("output manifest top-level contract mismatch")
        if output.get("status") != "COMPLETE_PENDING_VERBALIZATION_DATA_FREEZE":
            errors.append("output manifest status mismatch")
        if output.get("harness_tag") != harness["prospective_tag"]:
            errors.append("output manifest harness tag mismatch")
        if output.get("source_tag") != harness["boundaries"]["source"]["tag"]:
            errors.append("output manifest source tag mismatch")
        if output.get("data_tag") != data_boundary["tag"]:
            errors.append("output manifest data tag mismatch")
        if (
            output.get("data_freeze_manifest_sha256")
            != data_boundary["manifest_sha256"]
        ):
            errors.append("output manifest data-freeze hash mismatch")
        if (
            output.get("input_inventory_sha256")
            != data_manifest["data_artifacts"]["aggregate_digests"]["inventory_sha256"]
        ):
            errors.append("output manifest input inventory hash mismatch")
        if output.get("runtime") != {
            "python": harness["python_runtime"]["python_version"],
            **harness["python_runtime"]["packages"],
        }:
            errors.append("output manifest runtime mismatch")
        if output.get("window_contract") != harness["window_contract"]:
            errors.append("output manifest window contract mismatch")
        if output.get("case_count") != 30:
            errors.append("output manifest case count mismatch")
        if output.get("structured_output_directory") != STRUCTURED_DIR_NAME:
            errors.append("structured output directory contract mismatch")
        if output.get("neutral_text_output_directory") != NEUTRAL_DIR_NAME:
            errors.append("neutral text directory contract mismatch")

        entries = output.get("cases", [])
        if [entry.get("physical_case_id") for entry in entries] != expected_ids:
            errors.append("output case identity/order mismatch")
        if [entry.get("order") for entry in entries] != list(range(1, 31)):
            errors.append("output case order must be exactly 1..30")

        expected_files = {OUTPUT_MANIFEST_NAME}
        inventory_digest = hashlib.sha256()
        for input_row, entry in zip(inputs, entries):
            case_id = input_row["physical_case_id"]
            if entry.get("source_path") != input_row["path"]:
                errors.append(f"source path mismatch: {case_id}")
            if entry.get("source_size_bytes") != input_row["size_bytes"]:
                errors.append(f"source size mismatch: {case_id}")
            if entry.get("source_sha256") != input_row["sha256"]:
                errors.append(f"source hash mismatch: {case_id}")
            structured_rel = f"{STRUCTURED_DIR_NAME}/{case_id}.json"
            neutral_rel = f"{NEUTRAL_DIR_NAME}/{case_id}.txt"
            if entry.get("structured_path") != structured_rel:
                errors.append(f"structured relative path mismatch: {case_id}")
            if entry.get("neutral_text_path") != neutral_rel:
                errors.append(f"neutral relative path mismatch: {case_id}")
            expected_files.update({structured_rel, neutral_rel})

            structured_path = output_root / relative(structured_rel)
            neutral_path = output_root / relative(neutral_rel)
            error = _check_file(
                structured_path,
                entry.get("structured_size_bytes", -1),
                entry.get("structured_sha256", ""),
            )
            if error:
                errors.append(error)
                continue
            error = _check_file(
                neutral_path,
                entry.get("neutral_text_size_bytes", -1),
                entry.get("neutral_text_sha256", ""),
            )
            if error:
                errors.append(error)
                continue
            structured: dict[str, Any] | None = None
            try:
                structured = load_json(structured_path)
                if structured.get("time_range_h") != [10.0, 50.0]:
                    errors.append(f"time range mismatch: {case_id}")
                if structured.get("window_hours") != 5.0:
                    errors.append(f"window width mismatch: {case_id}")
                if structured.get("n_windows") != 8:
                    errors.append(f"window count mismatch: {case_id}")
                variables = structured.get("variables", {})
                if set(variables) != {f"XMEAS-{index}" for index in range(1, 42)}:
                    errors.append(f"variable identity mismatch: {case_id}")
                expected_starts = [10.0 + 5.0 * index for index in range(8)]
                expected_ends = [value + 5.0 for value in expected_starts]
                for variable in variables.values():
                    windows = variable.get("per_window", [])
                    if [row.get("start_h") for row in windows] != expected_starts:
                        errors.append(f"window starts mismatch: {case_id}")
                        break
                    if [row.get("end_h") for row in windows] != expected_ends:
                        errors.append(f"window ends mismatch: {case_id}")
                        break
                if not _all_finite(structured):
                    errors.append(f"non-finite structured output: {case_id}")
            except (OSError, ValueError, TypeError) as exc:
                errors.append(f"invalid structured output {case_id}: {exc}")
            if structured is not None:
                try:
                    expected_neutral = (render_text(structured) + "\n").encode("utf-8")
                    observed_neutral = neutral_path.read_bytes()
                    if observed_neutral != expected_neutral:
                        errors.append(
                            "neutral text differs from frozen render_text output: "
                            f"{case_id}"
                        )
                except (KeyError, OSError, TypeError, ValueError) as exc:
                    errors.append(f"cannot reproduce neutral text {case_id}: {exc}")
            inventory_digest.update(
                (
                    f"{case_id},{structured_rel},"
                    f"{entry['structured_size_bytes']},{entry['structured_sha256']},"
                    f"{neutral_rel},{entry['neutral_text_size_bytes']},"
                    f"{entry['neutral_text_sha256']}\n"
                ).encode("utf-8")
            )

        observed_files = {
            str(path.relative_to(output_root))
            for path in output_root.rglob("*")
            if path.is_file()
        }
        if observed_files != expected_files:
            errors.append(
                "output tree mismatch: "
                f"missing={sorted(expected_files - observed_files)}, "
                f"extra={sorted(observed_files - expected_files)}"
            )
        observed_directories = {
            str(path.relative_to(output_root))
            for path in output_root.rglob("*")
            if path.is_dir()
        }
        expected_directories = {STRUCTURED_DIR_NAME, NEUTRAL_DIR_NAME}
        if observed_directories != expected_directories:
            errors.append(
                "output directory tree mismatch: "
                f"missing={sorted(expected_directories - observed_directories)}, "
                f"extra={sorted(observed_directories - expected_directories)}"
            )
        if any(path.is_symlink() for path in output_root.rglob("*")):
            errors.append("output tree contains a symlink")
        if output.get("output_inventory_sha256") != inventory_digest.hexdigest():
            errors.append("output inventory digest mismatch")
    except (KeyError, OSError, TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = verify_outputs(args.manifest, args.data_root, args.output_root)
    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: EXP3_V2 portable verbalization verification succeeded.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
