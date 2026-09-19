#!/usr/bin/env python3
"""Build E5 PERM/OMIT prompts offline from B-LF carriers; never calls a model.

This is deliberately an adapter, not a second final renderer.  It reads B-LF nucleus
prompts rendered by ``main``, replaces only their ``CASE TO DIAGNOSE`` block, and fails
closed if any byte outside that block changes.  The output is an input manifest for
``run_e5.py``; it is not a target and contains no execution switch.
"""
from __future__ import annotations
import argparse, csv, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]; HERE = Path(__file__).resolve().parent
for p in (ROOT, ROOT / "code", HERE):
    if str(p) not in sys.path: sys.path.insert(0, str(p))
import pandas as pd
import tep_verbalize_v2 as verbalizer
import e5_corruption, protocol_omit
from verifica_e5_c2_prompt import split_carrier, compose

class E5PromptError(RuntimeError): pass
def sha(text: str) -> str: return hashlib.sha256(text.encode()).hexdigest()
def load_json(path): return json.loads(Path(path).read_text(encoding="utf-8"))

def case_only_diff(full: str, altered: str) -> dict:
    fp, fc, fs = split_carrier(full); ap, ac, ass = split_carrier(altered)
    if (fp, fs) != (ap, ass): raise E5PromptError("S18: bytes outside CASE TO DIAGNOSE changed")
    if fc == ac: raise E5PromptError("S18: the case block did not change")
    return {"status": "PASS", "changed_only": "CASE TO DIAGNOSE",
            "full_case_sha256": sha(fc.strip()), "altered_case_sha256": sha(ac.strip())}

def _manifest_cases(directory: Path) -> dict:
    out = {}
    with (directory / "EVIDENCE_MANIFEST_TEST.csv").open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            feature = directory / row["feature_path"]
            text = directory / row["text_path"]
            if not feature.is_file() or not text.is_file(): raise E5PromptError(f"missing evidence for {row['case_id']}")
            if hashlib.sha256(feature.read_bytes()).hexdigest() != row["feature_sha256"]: raise E5PromptError(f"feature hash mismatch: {row['case_id']}")
            if hashlib.sha256(text.read_bytes()).hexdigest() != row["text_sha256"]: raise E5PromptError(f"text hash mismatch: {row['case_id']}")
            out[row["case_id"]] = (pd.read_csv(feature), text.read_text(encoding="utf-8").strip())
    return out

def _carriers(path: Path) -> dict:
    found = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        if row.get("block") == "nucleus" and row.get("condition") == "B-LF" and row.get("library_role") == "G_P":
            found[(row["case_id"], row["agent_id"])] = row
    return found

def build(*, full_prompts: Path, test_input: Path, derangements: Path, recipients: Path) -> dict:
    protocol_omit.verify_frozen_renderer()
    cases, carriers = _manifest_cases(test_input), _carriers(full_prompts)
    der, rec = load_json(derangements)["derangements"], load_json(recipients)["recipients"]
    rows, proofs = [], []
    for family, assignment in der.items():
        for recipient, donor in assignment["pairs"].items():
            if recipient not in cases or donor not in cases: raise E5PromptError(f"unknown E5 case {recipient}/{donor}")
            rframe, neutral = cases[recipient]; dframe, _ = cases[donor]
            perm_case = verbalizer.verbalize_feature_table(e5_corruption.swap_family(rframe, dframe, family))["text"]
            omit_case = protocol_omit.render_omit(rframe, family)["text"]
            for agent in rec["assignments"].get(recipient, []):
                base = carriers.get((recipient, agent))
                if base is None: raise E5PromptError(f"missing B-LF carrier: {recipient}/{agent}")
                prefix, observed, suffix = split_carrier(base["text"])
                if observed.strip() != neutral: raise E5PromptError(f"carrier case bytes differ from evidence: {recipient}/{agent}")
                for arm, case_text in (("PERM", perm_case), ("OMIT", omit_case)):
                    text = compose(prefix, case_text, suffix)
                    proof = case_only_diff(base["text"], text)
                    # This is a new E5 identifier, not a field concatenation: it must remain
                    # admissible to final_inventory.stable_id (no embedded ``|``).
                    prompt_id = "e5_{}_{}_{}_{}_{}".format(
                        arm.lower(), family, recipient, agent, "gp")
                    rows.append({"prompt_id": prompt_id, "stable_id": prompt_id, "source_stable_id": base["stable_id"],
                                 "arm": arm, "family": family, "case_id": recipient, "donor_case_id": donor,
                                 "agent_id": agent, "text": text, "prompt_sha256": sha(text)})
                    proofs.append({"prompt_id": prompt_id, **proof})
    if len({row["prompt_id"] for row in rows}) != len(rows):
        raise E5PromptError("E5 prompt identifiers are not unique")
    return {"artifact_version": "E5_PROMPTS_1", "status": "OFFLINE_NOT_EXECUTED",
            "inputs": {"derangements_sha256": hashlib.sha256(derangements.read_bytes()).hexdigest(),
                       "recipients_sha256": hashlib.sha256(recipients.read_bytes()).hexdigest()}, "rows": rows,
            "s18_case_block_diff": proofs, "counts": {"prompts": len(rows), "proofs": len(proofs)}}

def main(argv=None):
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--full-prompts", type=Path, required=True); p.add_argument("--test-input", type=Path, required=True)
    p.add_argument("--derangements", type=Path, default=HERE/"DERANGEMENTS_E5.json")
    p.add_argument("--recipients", type=Path, default=HERE/"RICEVENTI_E5.json"); p.add_argument("--out", type=Path, required=True)
    a=p.parse_args(argv); value=build(full_prompts=a.full_prompts, test_input=a.test_input, derangements=a.derangements, recipients=a.recipients)
    a.out.write_text(json.dumps(value, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    print(json.dumps({k:v for k,v in value.items() if k not in ("rows", "s18_case_block_diff")}, indent=2)); return 0
if __name__ == "__main__": raise SystemExit(main())
