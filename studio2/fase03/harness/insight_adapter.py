"""Hash-pinned adapter for the independently developed 03.12 validator."""

from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any, Callable

from .common import HarnessError, canonical_json, require_sha256


SCHEMA_COMMIT = "3c64390bc4dd58c48cc4e1e388a38989b32b3143"
SCHEMA_MANIFEST_SHA256 = "d64e4d4be32afcf9bc35d78727c943e13d7d466320caab35451f40e624ddde12"
SCHEMA_TAG = "studio2-fase03-schema-insight-frozen-001"
SCHEMA_TAG_OBJECT = "4d15c4fb915ea9db9f7425225d231746778f0ba1"
EXPECTED = {
    "validator.py": "cd523d3105e02de99e7cc09bf0c2c4c052c1ae1776c8da37a9b57e869b1aa508",
    "insight_v1.schema.json": "15e0d29e033c1d699d4f1114b5fdf378ad1cea8398c89b133403a92983229de6",
    "leakage_rules_v1.json": "1cf035b5d5e7a7f4cc909dc0a04f6f0da6580284d32710f3ee6924533c706a7a",
    "SCHEMA_FREEZE.json": SCHEMA_MANIFEST_SHA256,
}
FIXED = ("insight_id", "source_agent", "pseudolabel", "evidence_scope", "variable_ids")


def load_validator(schema_dir: Path) -> ModuleType:
    for name, digest in EXPECTED.items():
        require_sha256(schema_dir / name, digest, role=f"03.12 {name}")
    # Resolve the actual R4 dependency before any provider request, including ABI errors.
    try:
        from jsonschema import Draft202012Validator
        import json
        Draft202012Validator.check_schema(json.loads((schema_dir / 'insight_v1.schema.json').read_bytes()))
    except Exception as exc:
        raise HarnessError(f'R4 validator runtime dependency unavailable or incompatible: {exc}') from exc
    spec = importlib.util.spec_from_file_location("studio2_schema_insight_v1", schema_dir / "validator.py")
    if spec is None or spec.loader is None:
        raise HarnessError("cannot construct the 03.12 validator module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if getattr(module, "VERSION", None) != "1.0.0":
        raise HarnessError("unexpected 03.12 validator version")
    return module


def context_from_inventory(inventory: dict[str, Any]) -> dict[str, Any]:
    contracts = inventory.get("fixed_insight_contracts")
    if not isinstance(contracts, list) or len(contracts) != 16:
        raise HarnessError("inventory must contain sixteen fixed insight contracts")
    owners: dict[str, str] = {}
    for row in contracts:
        owners[row["pseudolabel"]] = row["source_agent"]
    return {
        "owners": owners,
        "normal_label": "Normal",
        "fixed": [{key: row[key] for key in FIXED} for row in contracts],
    }


def assert_context_compatible(module: ModuleType, context: dict[str, Any]) -> None:
    try:
        module.context_check(context)
    except Exception as exc:
        raise HarnessError(
            f"03.12 R4 context validation failed at {SCHEMA_COMMIT}: {exc}"
        ) from exc


def validate_library(
    values: list[dict[str, Any]],
    *,
    inventory: dict[str, Any],
    token_count: Callable[[str], int],
    schema_dir: Path,
) -> list[dict[str, Any]]:
    validator = load_validator(schema_dir)
    context = context_from_inventory(inventory)
    assert_context_compatible(validator, context)
    return validator.validate_library(values, context=context, count=token_count)


def validate_produced_pair(
    values: list[dict[str, Any]],
    *,
    inventory: dict[str, Any],
    agent_id: str,
    token_count: Callable[[str], int],
    schema_dir: Path,
) -> list[dict[str, Any]]:
    """Validate one producer response without pretending the 16-item library exists."""
    if not isinstance(values, list) or len(values) != 2:
        raise HarnessError("producer conformance response must contain exactly two insights")
    validator = load_validator(schema_dir)
    context = context_from_inventory(inventory)
    fixed = validator.context_check(context)
    expected = sorted(
        (row for row in fixed.values() if row["source_agent"] == agent_id),
        key=lambda row: row["insight_id"],
    )
    if len(expected) != 2:
        raise HarnessError(f"{agent_id} must own exactly two fixed insight contracts")
    ordered = sorted(values, key=lambda row: row.get("insight_id", ""))
    if [row.get("insight_id") for row in ordered] != [row["insight_id"] for row in expected]:
        raise HarnessError("producer response does not match the two fixed insight IDs")
    return [
        validator.validate(value, fixed=fixed[value["insight_id"]], count=token_count)
        for value in ordered
    ]


def validate_be_diff(
    before: list[dict[str, Any]],
    after: list[dict[str, Any]],
    *,
    mapping: dict[str, str],
    agent_id: str,
    inventory: dict[str, Any],
    token_count: Callable[[str], int],
    schema_dir: Path,
) -> dict[str, Any]:
    validator = load_validator(schema_dir)
    context = context_from_inventory(inventory)
    assert_context_compatible(validator, context)
    return validator.diff_be(
        canonical_json(before).encode("utf-8"),
        canonical_json(after).encode("utf-8"),
        mapping=mapping,
        context=context,
        count=token_count,
        agent=agent_id,
    )
