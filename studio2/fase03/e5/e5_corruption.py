#!/usr/bin/env python3
"""E5 PERM arm: family-column swap on the structured evidence, upstream of the renderer.

The corruption acts on the feature table that ``evidence/extract_test_lot_evidence.py``
writes for each case (``EVT-xxxx.features.csv``: 41 XMEAS x one assigned window x the
frozen descriptor columns) and **never** on the produced text. The frozen verbalizer
``code/tep_verbalize_v2.verbalize_feature_table`` is then called unchanged, so every
derived quantity -- ``rapid`` (E5-B), the coherent-drift episodes, the settling transient
and the phase values -- is recomputed from the evidence actually present in the arm.

Nothing here is modified in place: every function returns a new DataFrame.

Scope of the manipulation (piano 8.12): only the interrogated case. Local examples,
insight library, context and policy are untouched, and this module never sees them.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

MAP_PATH = Path(__file__).with_name("family_map.json")

#: Columns that are never swapped and never omitted (see ``family_map.json``).
NEVER_TOUCHED = ("window_start_h", "window_end_h", "variable", "raw_std_ratio")

REQUIRED_COLUMNS = {
    "window_start_h", "window_end_h", "variable", "shift_sigma", "slope_sigma_h",
    "raw_std_ratio", "diff_std_ratio", "residual_std_ratio",
}


class E5CorruptionError(RuntimeError):
    """Raised when a swap would violate the frozen contract of the evidence table."""


def load_family_map(path: Path | str = MAP_PATH) -> dict[str, Any]:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


def family_column(family: str, family_map: dict[str, Any] | None = None) -> str:
    families = (family_map or load_family_map())["families"]
    if family not in families:
        raise E5CorruptionError(f"unknown family: {family!r}; known: {sorted(families)}")
    return families[family]["column"]


def _check_unit(frame: pd.DataFrame, label: str) -> None:
    missing = sorted(REQUIRED_COLUMNS - set(frame.columns))
    if missing:
        raise E5CorruptionError(f"{label}: feature table is missing columns: {missing}")
    if frame["variable"].duplicated().any():
        raise E5CorruptionError(
            f"{label}: a variable appears twice; the swap is defined on a single-window unit"
        )
    if frame["window_start_h"].nunique() != 1:
        raise E5CorruptionError(
            f"{label}: {frame['window_start_h'].nunique()} windows; D1 assigns exactly one"
        )


def swap_family(
    recipient: pd.DataFrame,
    donor: pd.DataFrame,
    family: str,
    *,
    family_map: dict[str, Any] | None = None,
) -> pd.DataFrame:
    """Return the recipient's evidence with the column of ``family`` taken from the donor.

    Both frames must be single-window units carrying the same 41 XMEAS. The donor's
    values are aligned **by variable name**, never by row order, so the two tables may be
    sorted differently. The recipient's window geometry is kept: the donor supplies one
    descriptor column and nothing else.
    """
    mapping = family_map or load_family_map()
    column = family_column(family, mapping)
    _check_unit(recipient, "recipient")
    _check_unit(donor, "donor")
    if set(recipient["variable"]) != set(donor["variable"]):
        raise E5CorruptionError("donor and recipient do not carry the same XMEAS set")
    donor_values = donor.set_index("variable")[column]
    corrupted = recipient.copy(deep=True)
    corrupted[column] = corrupted["variable"].map(donor_values).to_numpy()
    if corrupted[column].isna().any():
        raise E5CorruptionError(f"donor column {column} has missing values after alignment")
    return corrupted


def swapped_columns_report(
    full: pd.DataFrame, permuted: pd.DataFrame, family: str,
    *, family_map: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Proof that exactly one descriptor column changed (used by the G2 diff test)."""
    mapping = family_map or load_family_map()
    column = family_column(family, mapping)
    changed: list[str] = []
    for name in full.columns:
        left = full.sort_values("variable")[name].to_numpy()
        right = permuted.sort_values("variable")[name].to_numpy()
        if not (left == right).all():
            changed.append(name)
    return {
        "family": family,
        "expected_changed_column": column,
        "observed_changed_columns": changed,
        "ok": changed == [column],
        "never_touched_intact": all(name not in changed for name in NEVER_TOUCHED),
    }
