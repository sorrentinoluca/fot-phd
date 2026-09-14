"""Controlli documentali/offline del pacchetto; nessuna chiamata o simulazione."""
import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    manifest = json.loads((BASE / "MANIFEST_PREPARAZIONE_CHIUSURA_03_8.json").read_text())
    errors = []
    checks = {}
    for category in ("files", "protected_inputs"):
        checks[category] = 0
        for entry in manifest[category]:
            path = ROOT / entry["path"]
            if not path.is_file() or digest(path) != entry["sha256"] or path.stat().st_size != entry["bytes"]:
                errors.append(f"Hash/bytes: {entry['path']}")
            else:
                checks[category] += 1
    own_path = str((BASE / "MANIFEST_PREPARAZIONE_CHIUSURA_03_8.json").relative_to(ROOT))
    if own_path in [entry["path"] for entry in manifest["files"]]:
        errors.append("Manifest self-reference")
    if manifest["protocol_revision_created"] is not None or manifest["author_decisions"] != {"A": "pending", "B": "pending"}:
        errors.append("Preparation state changed: requires new reviewed candidate/check specification")
    lit = json.loads((BASE / "ACQUISIZIONE_LETTERATURA_03_8.json").read_text())
    checks["literature_source"] = checks["literature_snapshot"] = 0
    for side, key in (("source", "source_root"), ("snapshot", "snapshot_root")):
        for entry in lit["files"]:
            path = Path(lit[key]) / entry["path"]
            if not path.is_file() or digest(path) != entry["sha256"] or path.stat().st_size != entry["bytes"]:
                errors.append(f"Literature {side}: {entry['path']}")
            else:
                checks[f"literature_{side}"] += 1
    if digest(Path(lit["review_path"])) != lit["review_sha256"]:
        errors.append("Literature review changed")
    for entry in lit["protected_files"]:
        for key in ("source_root", "snapshot_root"):
            if digest(Path(lit[key]) / entry["path"]) != entry["base_sha256"]:
                errors.append(f"Protected literature input: {key}/{entry['path']}")
    checks["local_markdown_links"] = 0
    for entry in manifest["files"]:
        path = ROOT / entry["path"]
        if path.suffix != ".md":
            continue
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
            if "://" in target or target.startswith("#"):
                continue
            target = target.split("#")[0]
            if not (path.parent / target).exists():
                errors.append(f"Broken link in {path.name}: {target}")
            checks["local_markdown_links"] += 1
    # Aritmetica indipendente dalle cifre del prospetto: enumera i blocchi.
    totals = {}
    for r in (1, 3):
        core = 8 * 8 * 7 * 3 * r + 8 * 8 * 3 * r + 8 * 8 * 3 * r
        measures = core + 4 * 8 * 7 * r + (8 * 8 + 4 * 3 * 7) * r + 2 * 3 * 8 * 3 * r
        totals[str(r)] = measures + (2 * 173 if r == 1 else 0) + 16 * 12 + 10 * 10 + 160 + 100
    if totals != {"1": 3142, "3": 7284}:
        errors.append(f"Budget arithmetic: {totals}")
    checks["budget_scenarios"] = totals
    maxima = []
    for alt in (0, 1):
        values = [128 + b + 8 * r + 8 * alt + t for b in (3, 6, 9)
                  for r in (0, 1) for t in range(16) if 8 * r + t <= 15]
        maxima.append(max(values))
    if maxima != [152, 160]:
        errors.append(f"Pilot arithmetic: {maxima}")
    checks["pilot_maxima"] = maxima
    checks["probe_repeat_triplets_max_without_prior_transport"] = 7 // 3
    result = subprocess.run(["git", "diff", "--check"], cwd=ROOT, capture_output=True, text=True)
    if result.returncode:
        errors.append(result.stdout + result.stderr)
    print(json.dumps({"scope": "local_preparer_checks_not_independent_review", "checks": checks,
                      "errors": errors, "ok": not errors}, ensure_ascii=False, indent=2))
    return bool(errors)


if __name__ == "__main__":
    raise SystemExit(main())
