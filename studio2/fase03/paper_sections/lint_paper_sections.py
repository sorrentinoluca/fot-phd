#!/usr/bin/env python3
"""Lint minimale per le bozze comuni del paper FoT-TEP."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


DRAFTS = ("related_work.md", "method.md", "verbalizer.md", "protocol.md", "threats.md")
NUMBER = re.compile(r"(?<![A-Za-z_])(?:\d+(?:[.,]\d+)?|[A-Z]\d+)(?![A-Za-z_])")
FORBIDDEN_CLAIM = re.compile(r"(?<![-\w])(?:novel|first|unique)(?![-\w])", re.IGNORECASE)
F_PSEUDOLABEL = re.compile(
    r"(?:\bF\d+\b.{0,120}\bpseudolabel\b|\bpseudolabel\b.{0,120}\bF\d+\b)",
    re.IGNORECASE | re.DOTALL,
)
BIB_SOURCE = re.compile(r"\[Fonte bibliografica:[^\]]+\]", re.IGNORECASE)


def paragraphs(text: str) -> list[tuple[int, str]]:
    blocks: list[tuple[int, str]] = []
    current: list[str] = []
    start = 0
    in_fence = False
    for lineno, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
            if current:
                blocks.append((start, "\n".join(current)))
                current = []
            continue
        if in_fence:
            continue
        if not line.strip():
            if current:
                blocks.append((start, "\n".join(current)))
                current = []
            continue
        if not current:
            start = lineno
        current.append(line)
    if current:
        blocks.append((start, "\n".join(current)))
    return blocks


def is_source(block: str) -> bool:
    stripped = "\n".join(line.lstrip("> ") for line in block.splitlines()).strip()
    return stripped.startswith("[Fonte")


def lint_file(path: Path, corpus: str) -> list[str]:
    text = path.read_text(encoding="utf-8")
    issues: list[str] = []
    blocks = paragraphs(text)

    for index, (lineno, block) in enumerate(blocks):
        plain = "\n".join(line.lstrip("> ") for line in block.splitlines())
        if plain.startswith("#") or is_source(block):
            continue
        if NUMBER.search(plain):
            next_block = blocks[index + 1][1] if index + 1 < len(blocks) else ""
            if "[Fonte:" not in plain and "[Fonte bibliografica:" not in plain and not is_source(next_block):
                issues.append(f"{path.name}:{lineno}: numero privo di fonte nel paragrafo")

    for match in FORBIDDEN_CLAIM.finditer(text):
        lineno = text.count("\n", 0, match.start()) + 1
        issues.append(f"{path.name}:{lineno}: parola di primato non autorizzata: {match.group(0)!r}")

    for match in F_PSEUDOLABEL.finditer(text):
        lineno = text.count("\n", 0, match.start()) + 1
        issues.append(f"{path.name}:{lineno}: F-number accanto a pseudolabel")

    for match in BIB_SOURCE.finditer(text):
        marker = match.group(0)
        lineno = text.count("\n", 0, match.start()) + 1
        if "docs/letteratura.md" not in marker or not re.search(r"§14(?:\.\d+)?", marker):
            issues.append(f"{path.name}:{lineno}: citazione bibliografica fuori dal corpus o senza sigla §14.x")

    # Ogni nome di lavoro/autore usato come citazione deve comparire nel corpus locale.
    needles = {
        "Time-FFM": "Time-FFM",
        "Federation over Text": "Federation over Text",
        "FICAL": "FICAL",
        "Fed-ICL": "Fed-ICL",
        "FedTextGrad": "FedTextGrad",
        "FERA": "FERA",
        "ACE": "Agentic Context Engineering",
        "SYNAPSE": "SYNAPSE",
        "TRUCE": "Truth-Conditional Captions",
        "T2SP": "T2SP",
        "CGTime": "CGTime",
        "S2S-FDD": "S2S-FDD",
        "FedMD": "FedMD",
        "FedProto": "FedProto",
        "FedCKD": "FedCKD",
        "FedMeta-FFD": "FedMeta-FFD",
        "Zhang et al.": "Zhang et al., 2026",
        "Xu et al.": "Xu et al., 2026",
        "FaultExplainer": "FaultExplainer",
        "EviFDD-Agent": "EviFDD-Agent",
        "DP-FPL": "DP-FPL",
        "Downs & Vogel": "Downs, J.J. & Vogel",
    }
    for label, needle in needles.items():
        if label in text and needle not in corpus:
            issues.append(f"{path.name}: citazione {label!r} assente da docs/letteratura.md")
    return issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus", type=Path, required=True)
    parser.add_argument("drafts", nargs="*", type=Path)
    args = parser.parse_args()
    drafts = args.drafts or [Path(__file__).with_name(name) for name in DRAFTS]
    corpus = args.corpus.read_text(encoding="utf-8")
    issues = [issue for draft in drafts for issue in lint_file(draft, corpus)]
    for issue in issues:
        print(issue)
    print(f"Lint paper sections: {len(drafts)} file, {len(issues)} segnalazioni")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
