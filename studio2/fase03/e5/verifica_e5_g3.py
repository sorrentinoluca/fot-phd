#!/usr/bin/env python3
"""G3 checks on the real E5 prompts, offline: carriers, byte identity, leakage, case texts.

Reads the E5 manifest of ``build_e5_prompts.py`` and the copy of the batch
``final_prompts.jsonl`` it was built from. Writes only ``--out`` and ``--case-texts``.

1. the carrier file is the batch one: every row hashes to its ``prompt_sha256``, 2,244 rows,
   848 B-LF, and the id->hash map is the canonical one pinned by the final protocol
   (``b8192003...``); its file SHA is printed to compare with the batch target descriptor;
2. every E5 prompt: its carrier is the B-LF/G_P nucleus cell of the same case and receiver,
   and only ``CASE TO DIAGNOSE`` differs (S18, re-proved);
3. leakage: the D1 scanner of the test lot on every E5 case block (the only bytes E5 adds);
4. ``--case-texts``, written **only when every check is PASS**: FULL/PERM case texts per (family, case) for
   ``verifica_e5_c2_prompt.py --case-texts ... --carrier-mode all``;
5. ``run_e5.plan``: 576 planned calls at R=3.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for _p in (ROOT, ROOT / "code", HERE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

from studio2.fase03.protocol import canonical_json, sha256_text  # noqa: E402
from studio2.fase03.evidence.leakage import scan_text  # noqa: E402
from build_e5_prompts import case_only_diff  # noqa: E402
from verifica_e5_c2_prompt import split_carrier  # noqa: E402
import run_e5  # noqa: E402

PROMPT_MAP_SHA256 = "b819200396da480d3ed9d4aa8f6b6aac8c135d97f0876b734a9b607b75736489"


def check(*, manifest: Path, full_prompts: Path, case_texts: Path | None) -> dict:
    rows = [json.loads(line) for line in full_prompts.read_text(encoding="utf-8").splitlines() if line]
    bad = [r["prompt_id"] for r in rows if sha256_text(r["text"]) != r["prompt_sha256"]]
    carriers = {r["stable_id"]: r for r in rows}
    value = json.loads(manifest.read_text(encoding="utf-8"))
    failures, leaks, pairs = [], [], {}
    for row in value["rows"]:
        carrier = carriers.get(row["source_stable_id"])
        if (carrier is None or (carrier["block"], carrier["condition"], carrier["library_role"]) != ("nucleus", "B-LF", "G_P")
                or (carrier["case_id"], carrier["agent_id"]) != (row["case_id"], row["agent_id"])):
            failures.append(f"carrier: {row['prompt_id']}")
            continue
        try:
            case_only_diff(carrier["text"], row["text"])
        except Exception as exc:  # noqa: BLE001 - reported, fail-closed below
            failures.append(f"S18 {row['prompt_id']}: {exc}")
        case_block = split_carrier(row["text"])[1].strip()
        leaks += [{"prompt_id": row["prompt_id"], "excerpt": f.excerpt} for f in scan_text(case_block)]
        if row["arm"] == "PERM":
            key = (row["family"], row["case_id"])
            if key in pairs:
                failures.append(f"two PERM rows for {key}")
            pairs[key] = {"family": row["family"], "case_id": row["case_id"],
                          "donor_case_id": row["donor_case_id"],
                          "full_text": split_carrier(carrier["text"])[1].strip(), "perm_text": case_block}
    plan = run_e5.plan(manifest, (1, 2, 3))
    prompt_map = sha256_text(canonical_json([[r["prompt_id"], r["prompt_sha256"]] for r in rows]))
    summary = {
        "artifact_version": "VERIFICA_E5_G3_1",
        "carriers": {"file": str(full_prompts),
                     "file_sha256": hashlib.sha256(full_prompts.read_bytes()).hexdigest(),
                     "rows": len(rows), "b_lf": sum(r["condition"] == "B-LF" for r in rows),
                     "rows_with_altered_bytes": bad, "prompt_map_sha256": prompt_map,
                     "prompt_map_is_canonical": prompt_map == PROMPT_MAP_SHA256},
        "manifest": {"file": str(manifest), "sha256": hashlib.sha256(manifest.read_bytes()).hexdigest(),
                     "prompts": len(value["rows"])},
        "s18_and_carrier_failures": failures,
        "leakage_findings_in_case_blocks": leaks,
        "perm_pairs_for_c2": len(pairs),
        "plan": plan,
    }
    ok = (not bad and not failures and not leaks and len(rows) == 2244
          and summary["carriers"]["b_lf"] == 848 and summary["carriers"]["prompt_map_is_canonical"]
          and plan["planned_calls"] == 576 and len(pairs) == 96)
    summary["status"] = "PASS" if ok else "FAIL"
    # C2 must never run on a subset G3 did not validate: the case texts exist only after PASS.
    if case_texts is not None:
        if ok:
            case_texts.write_text("".join(json.dumps(p, ensure_ascii=False) + "\n" for p in pairs.values()),
                                  encoding="utf-8")
            summary["case_texts"] = str(case_texts)
        else:
            summary["case_texts"] = "NOT WRITTEN: G3 failed"
    return summary


def main(argv=None) -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--full-prompts", type=Path, required=True)
    p.add_argument("--case-texts", type=Path)
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args(argv)
    summary = check(manifest=a.manifest, full_prompts=a.full_prompts, case_texts=a.case_texts)
    a.out.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "plan"} | {"planned_calls": summary["plan"]["planned_calls"]},
                     indent=2, ensure_ascii=False))
    return 0 if summary["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
