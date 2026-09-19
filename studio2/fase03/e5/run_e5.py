#!/usr/bin/env python3
"""Validate and plan E5; this adapter intentionally has no --execute option.

The eventual main-branch integration must map these rows to its fresh E5 target and reuse
the final runner's ledger/canary/scoring path.  This file proves the pre-send inventory only.
"""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
HERE = Path(__file__).resolve().parent
class E5RunError(RuntimeError): pass
def sha(s): return hashlib.sha256(s.encode()).hexdigest()
def plan(path: Path, repetitions: tuple[int,...], derangements=HERE/'DERANGEMENTS_E5.json', recipients=HERE/'RICEVENTI_E5.json'):
    value=json.loads(path.read_text(encoding="utf-8")); rows=value.get("rows", [])
    if value.get("status") != "OFFLINE_NOT_EXECUTED": raise E5RunError("unknown prompt manifest")
    if not rows or any(sha(r["text"]) != r["prompt_sha256"] for r in rows): raise E5RunError("missing or altered prompt")
    if any(p.get("status") != "PASS" for p in value.get("s18_case_block_diff", [])): raise E5RunError("S18 proof failed")
    inputs=value.get("inputs", {})
    if inputs.get("derangements_sha256") != hashlib.sha256(Path(derangements).read_bytes()).hexdigest(): raise E5RunError("derangement binding differs")
    if inputs.get("recipients_sha256") != hashlib.sha256(Path(recipients).read_bytes()).hexdigest(): raise E5RunError("recipient binding differs")
    arms={r["arm"] for r in rows}
    if arms != {"PERM", "OMIT"}: raise E5RunError(f"unexpected arms: {arms}")
    cells={(r.get("source_stable_id"),r.get("family"),r["arm"]) for r in rows}
    bases={(a,b) for a,b,_ in cells}
    if len(rows) != len(bases)*2 or any((a,b,"PERM") not in cells or (a,b,"OMIT") not in cells for a,b in bases): raise E5RunError("PERM/OMIT inventory is unpaired")
    return {"artifact_version":"E5_RUN_PLAN_1", "status":"PLAN_ONLY_NO_EXECUTE", "repetitions":list(repetitions),
            "unique_prompts":len(rows), "planned_calls":len(rows)*len(repetitions),
            "requires":"main runner adapter, new E5 target, E5 canary, and G4 identity checklist"}
def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__); p.add_argument("--prompts",type=Path,required=True); p.add_argument("--repetitions",type=int,nargs="+",default=[1,2,3]); p.add_argument("--derangements",type=Path,default=HERE/'DERANGEMENTS_E5.json'); p.add_argument("--recipients",type=Path,default=HERE/'RICEVENTI_E5.json'); a=p.parse_args(argv)
    print(json.dumps(plan(a.prompts,tuple(a.repetitions),a.derangements,a.recipients),indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
