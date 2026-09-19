#!/usr/bin/env python3
"""E5 OMIT arm: the neutral text minus one descriptor family, by literal subtraction.

Same contract as ``studio2/fase03/protocol_bnolf.py`` (MAINTENANCE 8.2): the frozen
verbalizer ``code/tep_verbalize_v2.py`` is **not** modified in place. This is a new,
separately hashed file that defines the omission arm by subtraction from the frozen
output, so the definition cannot drift:

    OMIT_F text  ==  FULL text  minus the sentences produced by family F,
                     minus the sentences produced by the derived quantities of F.

The subtraction is literal. Each removable sentence is regenerated with the frozen
helpers of the verbalizer, located in the frozen text, and removed once; a sentence that
does not appear exactly once is an error and the render fails closed.

What falls with each family (see ``family_map.json``):

* ``level``     -> the displacement sentence;
* ``trend``     -> the slope sentence;
* ``residual``  -> the residual-variability sentence **and** the ``rapid`` sentence (E5-B:
                   ``rapid`` is derived from residual AND diff and is not computable when a
                   parent is omitted);
* ``diff``      -> the sample-to-sample sentence **and** the ``rapid`` sentence.

The sentence on the overall dispersion (``raw_std_ratio``) and the opening sentence on the
observed interval are never removed: ``raw_std_ratio`` belongs to no ablated family.

The derived quantities ``coherent_drift_episodes``, ``strict_global_drift``,
``settling_transient`` and ``phase_values`` do not surface as sentences of the neutral
text; they fall in the structured evidence only, and ``omit_structured`` records that.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]
for candidate in (REPO_ROOT, REPO_ROOT / "code"):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

import tep_verbalize_v2 as verbalizer  # noqa: E402

FROZEN_VERBALIZER_SHA256 = (
    "3a9129b6353cac6f8c9e02281282f137dd07885b1f882ca633ee9d6bf52393be"
)
FROZEN_CONFIG_SHA256 = (
    "552a0b8a9cf9e416de77daa7aca2d8dee152a2700bbfaab4ae5e039081712519"
)
VERBALIZER_PATH = Path(verbalizer.__file__).resolve()
CONFIG_PATH = VERBALIZER_PATH.with_name("verbalizer_config_v2.json")

CONDITION_PREFIX = "E5-OMIT"
FAMILIES = ("level", "trend", "residual", "diff")
#: Families whose omission also removes the derived ``rapid`` sentence (E5-B).
RAPID_PARENTS = ("residual", "diff")

class E5OmitError(RuntimeError):
    """Raised when the subtraction cannot be performed exactly."""


def sha256_file(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def verify_frozen_renderer(
    verbalizer_path: Path | None = None, config_path: Path | None = None
) -> dict[str, str]:
    """Fail closed if the frozen verbalizer or its config has changed."""
    target = Path(verbalizer_path or VERBALIZER_PATH)
    config = Path(config_path or CONFIG_PATH)
    observed = {"verbalizer_sha256": sha256_file(target), "config_sha256": sha256_file(config)}
    if observed["verbalizer_sha256"] != FROZEN_VERBALIZER_SHA256:
        raise E5OmitError(
            "frozen verbalizer changed: expected "
            f"{FROZEN_VERBALIZER_SHA256}, got {observed['verbalizer_sha256']}"
        )
    if observed["config_sha256"] != FROZEN_CONFIG_SHA256:
        raise E5OmitError(
            "frozen verbalizer config changed: expected "
            f"{FROZEN_CONFIG_SHA256}, got {observed['config_sha256']}"
        )
    return observed


def _family_sentences(structured: dict[str, Any], family: str) -> list[str]:
    """Regenerate, with the frozen helpers, the sentences family ``family`` contributed."""
    variables = structured["variables"]
    system = structured["system_summary"]
    n = structured["n_windows"]
    initial_n = structured["phase_window_counts"]["initial"]
    late_n = structured["phase_window_counts"]["late"]
    sentences: list[str] = []

    if family == "level":
        names = system["dominant_variables"]["level"]
        sentences.append(
            verbalizer._signed_fact(names[0], "spostamento", variables[names[0]]["level"], n)
            if names else "Nessuna XMEAS supera la soglia di spostamento."
        )
    elif family == "trend":
        names = system["dominant_variables"]["trend"]
        sentences.append(
            verbalizer._signed_fact(names[0], "pendenza", variables[names[0]]["trend"], n)
            if names else "Nessuna XMEAS supera la soglia di pendenza."
        )
    elif family == "residual":
        names = system["dominant_variables"]["residual"]
        sentences.append(
            verbalizer._unsigned_fact(
                names[0],
                "variabilità residua dopo rimozione del trend lineare",
                variables[names[0]]["residual_variability"], n, initial_n, late_n,
            ) if names else "Nessuna XMEAS supera la soglia di variabilità residua."
        )
    elif family == "diff":
        names = system["dominant_variables"]["diff"]
        sentences.append(
            verbalizer._unsigned_fact(
                names[0], "variazioni campione-campione",
                variables[names[0]]["sample_to_sample_variation"], n, initial_n, late_n,
            ) if names
            else "Nessuna XMEAS supera la soglia delle variazioni campione-campione."
        )
    else:
        raise E5OmitError(f"unknown family: {family!r}")

    if family in RAPID_PARENTS:
        rapid_names = system["dominant_variables"]["rapid"]
        if rapid_names:
            lead = rapid_names[0]
            info = variables[lead]["rapid_variability"]
            sentences.append(
                f"Su {lead}, residual e diff superano simultaneamente le rispettive "
                f"soglie in {info['n_active_windows']}/{n} finestre, incluse "
                f"{info['late_active_count']}/{late_n} finestre finali."
            )
    return sentences


def omit_text(structured: dict[str, Any], family: str, *, full_text: str | None = None) -> str:
    """Return the frozen text minus the sentences of ``family`` and of its derived channel."""
    if family not in FAMILIES:
        raise E5OmitError(f"unknown family: {family!r}; known: {list(FAMILIES)}")
    text = verbalizer.render_text(structured) if full_text is None else full_text
    remaining = text
    for sentence in _family_sentences(structured, family):
        occurrences = remaining.count(sentence)
        if occurrences != 1:
            raise E5OmitError(
                f"sentence of family {family} appears {occurrences} times in the frozen "
                "text; the subtraction is not exact"
            )
        index = remaining.index(sentence)
        end = index + len(sentence)
        # The frozen renderer joins sentences with a single space: remove the separator
        # that precedes the sentence, or the one that follows it for the first sentence.
        if index > 0 and remaining[index - 1] == " ":
            index -= 1
        elif end < len(remaining) and remaining[end] == " ":
            end += 1
        remaining = remaining[:index] + remaining[end:]
    if remaining == text:
        raise E5OmitError(f"nothing was removed for family {family}")
    if "  " in remaining:
        raise E5OmitError("double space left by the subtraction")
    return remaining


def omit_structured(structured: dict[str, Any], family: str) -> dict[str, Any]:
    """The structured evidence with the family's blocks and its derived channels dropped.

    The model never sees this object -- only ``omit_text`` reaches a prompt. It is produced
    for the record: it makes explicit, and hashable, exactly which derived quantities fall
    with the family (``family_map.json`` -> ``derived_quantities``).
    """
    section_by_family = {
        "level": "level",
        "trend": "trend",
        "residual": "residual_variability",
        "diff": "sample_to_sample_variation",
    }
    dropped_variable_sections = [section_by_family[family]]
    dropped_derived = []
    if family in RAPID_PARENTS:
        dropped_variable_sections.append("rapid_variability")
        dropped_derived += ["rapid_variability", "settling_transient", "phase_values"]
    if family in ("level", "trend"):
        dropped_derived += ["coherent_drift_episodes", "strict_global_drift"]

    reduced = {key: value for key, value in structured.items()
               if key not in ("variables", "system_summary")}
    reduced["variables"] = {}
    for name, payload in structured["variables"].items():
        kept = {key: value for key, value in payload.items()
                if key not in dropped_variable_sections and key not in dropped_derived}
        if family in ("level", "trend"):
            trend = dict(kept.get("trend", {}))
            for key in ("coherent_drift_episodes", "strict_global_drift"):
                trend.pop(key, None)
            if trend:
                kept["trend"] = trend
        kept["per_window"] = [
            {key: value for key, value in window.items()
             if key not in _dropped_window_keys(family)}
            for window in payload["per_window"]
        ]
        reduced["variables"][name] = kept
    system = {key: value for key, value in structured["system_summary"].items()}
    system["window_activity"] = {
        key: value for key, value in system["window_activity"].items()
        if key not in _dropped_activity_keys(family)
    }
    system["dominant_variables"] = {
        key: value for key, value in system["dominant_variables"].items()
        if key not in _dropped_activity_keys(family)
    }
    reduced["system_summary"] = system
    reduced["e5_omitted_family"] = family
    reduced["e5_dropped_derived"] = sorted(set(dropped_derived))
    return reduced


def _dropped_window_keys(family: str) -> set[str]:
    keys = {
        "level": {"shift_sigma", "level_candidate"},
        "trend": {"slope_sigma_h", "trend_candidate"},
        "residual": {"residual_std_ratio", "residual_candidate", "rapid_candidate"},
        "diff": {"diff_std_ratio", "diff_candidate", "rapid_candidate"},
    }[family]
    return keys


def _dropped_activity_keys(family: str) -> set[str]:
    keys = {"level": {"level"}, "trend": {"trend"},
            "residual": {"residual", "rapid"}, "diff": {"diff", "rapid"}}[family]
    return keys


def render_omit(features, family: str, *, config: dict[str, Any] | None = None,
                verify: bool = True) -> dict[str, Any]:
    """Full pipeline for one unit: frozen verbalizer, then the literal subtraction."""
    if config is not None:
        raise E5OmitError("E5 OMIT accepts only the frozen default verbalizer config")
    if verify:
        verify_frozen_renderer()
    result = verbalizer.verbalize_feature_table(features, config)
    text = omit_text(result["structured"], family, full_text=result["text"])
    return {
        "condition": f"{CONDITION_PREFIX}-{family}",
        "family": family,
        "text": text,
        "full_text": result["text"],
        "structured": omit_structured(result["structured"], family),
        "removed_sentences": _family_sentences(result["structured"], family),
    }
