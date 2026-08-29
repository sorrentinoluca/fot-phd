"""Scan prompt-facing text for evaluator-only real-class leakage."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


REAL_CLASS_PATTERNS = (
    re.compile(r"(?<![A-Za-z0-9])F(?:1|8|10|13)(?![A-Za-z0-9])", re.IGNORECASE),
    re.compile(r"\bfault\s*[-_:]?\s*(?:1|8|10|13)\b", re.IGNORECASE),
    re.compile(r"Tennessee\s+Eastman[^\n]{0,80}\bfault\b", re.IGNORECASE),
    re.compile(r"\bClass-[ABCD]\b", re.IGNORECASE),
)


@dataclass(frozen=True)
class LeakageFinding:
    source: str
    pattern: str
    excerpt: str


def scan_text(text: str, *, source: str = "<memory>") -> list[LeakageFinding]:
    findings: list[LeakageFinding] = []
    for pattern in REAL_CLASS_PATTERNS:
        for match in pattern.finditer(text):
            left, right = max(0, match.start() - 30), min(len(text), match.end() + 30)
            findings.append(
                LeakageFinding(source, pattern.pattern, text[left:right].replace("\n", " "))
            )
    return findings


def scan_files(paths: Iterable[str | Path]) -> list[LeakageFinding]:
    findings: list[LeakageFinding] = []
    for raw_path in paths:
        path = Path(raw_path)
        candidates = sorted(path.rglob("*")) if path.is_dir() else [path]
        for candidate in candidates:
            if candidate.is_file() and candidate.suffix.lower() in {".txt", ".md", ".json", ".jsonl"}:
                findings.extend(
                    scan_text(candidate.read_text(encoding="utf-8"), source=str(candidate))
                )
    return findings


def assert_no_leakage(paths: Iterable[str | Path]) -> None:
    findings = scan_files(paths)
    if findings:
        rendered = "; ".join(
            f"{finding.source}: {finding.excerpt!r}" for finding in findings[:8]
        )
        raise ValueError(f"Prompt-facing real-class leakage detected: {rendered}")


def scan_json_value(value: object, *, source: str = "<json>") -> list[LeakageFinding]:
    return scan_text(json.dumps(value, ensure_ascii=False), source=source)
