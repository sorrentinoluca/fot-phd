#!/usr/bin/env python3
"""Fail-closed scanner for D1 evaluator-only leakage."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9])F(?:1|2|3|8|10|13|14|15)(?![A-Za-z0-9])", re.I),
    re.compile(r"\b(?:fault|guasto)\s*[-_:]?\s*(?:1|2|3|8|10|13|14|15)\b", re.I),
    re.compile(r"\bIDV\s*\(\s*(?:1|2|3|8|10|13|14|15)\s*\)", re.I),
    re.compile(r"\b(?:continuit[aà]|nuov[oaie])\b", re.I),
    re.compile(
        r"\b(?:ratio_ac_s4|composition_b_s4|temperature_d_s2|composition_abc_s4|"
        r"temperature_c_s4|reaction_kinetics|valve_cw_reactor|valve_cw_condenser)\b",
        re.I,
    ),
    re.compile(
        r"\b(?:rapporto A/C|composizione B|composizione A/B/C|"
        r"temperatura (?:di )?alimentazione [CD]|cinetica (?:di )?reazione|"
        r"valvola (?:dell['’ ]?acqua|acqua) (?:del )?(?:reattore|condensatore)|"
        r"random variation|slow drift|sticking valve)\b",
        re.I,
    ),
)


@dataclass(frozen=True)
class Finding:
    source: str
    pattern: str
    excerpt: str


def scan_text(text: str, *, source: str = "<memory>") -> list[Finding]:
    findings: list[Finding] = []
    for pattern in PATTERNS:
        for match in pattern.finditer(text):
            left = max(0, match.start() - 36)
            right = min(len(text), match.end() + 36)
            findings.append(
                Finding(source, pattern.pattern, text[left:right].replace("\n", " "))
            )
    return findings


def scan_json(value: object, *, source: str = "<json>") -> list[Finding]:
    return scan_text(
        json.dumps(value, ensure_ascii=False, sort_keys=True), source=source
    )


def scan_files(paths: Iterable[Path]) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(paths, key=lambda item: str(item)):
        if path.suffix.lower() not in {".json", ".txt"}:
            continue
        findings.extend(scan_text(path.read_text(encoding="utf-8"), source=str(path)))
    return findings


def assert_no_leakage(paths: Iterable[Path]) -> None:
    findings = scan_files(paths)
    if findings:
        sample = "; ".join(
            f"{finding.source}: {finding.excerpt!r}" for finding in findings[:8]
        )
        raise ValueError(f"Consumer-facing D1 leakage detected: {sample}")

