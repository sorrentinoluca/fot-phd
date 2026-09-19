#!/usr/bin/env python3
"""E5 prompt builder, revision 1: inert PERM pairs are kept (REVISIONE_E5_001).

The frozen ``build_e5_prompts.py`` stops when a PERM case block equals the FULL one (S18: "the
case block did not change"). G3 found 8 such pairs out of 96 on the test lot: swapping the
family column leaves the verbalized text unchanged. Author decision 2026-09-19: the derangement
is not regenerated (protocol E5 §7, §9); the pairs stay, are sent, and are marked ``inert``.

This file changes only that rule. Everything else is the frozen builder: same evidence check,
same verbalizer, same OMIT renderer, same carriers, same identifiers, and S18 still proves
that no byte outside ``CASE TO DIAGNOSE`` changed. An inert OMIT, or an inert row of any arm
other than PERM, is still an error. Never calls a model.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
for _p in (ROOT, ROOT / "code", HERE):
    if str(_p) not in sys.path:
        sys.path.insert(0, str(_p))

import build_e5_prompts as frozen  # noqa: E402
from build_e5_prompts import E5PromptError, sha  # noqa: E402
import e5_corruption  # noqa: E402
import protocol_omit  # noqa: E402
import tep_verbalize_v2 as verbalizer  # noqa: E402
from verifica_e5_c2_prompt import compose, split_carrier  # noqa: E402

ARTIFACT_VERSION = "E5_PROMPTS_2"
INERT_ARMS = {"PERM"}


def case_proof(full: str, altered: str, *, arm: str) -> dict:
    """S18 of the frozen builder, except that an unchanged PERM case block is recorded as inert."""
    fp, fc, fs = split_carrier(full)
    ap, ac, ass = split_carrier(altered)
    if (fp, fs) != (ap, ass):
        raise E5PromptError("S18: bytes outside CASE TO DIAGNOSE changed")
    if fc == ac:
        if arm not in INERT_ARMS:
            raise E5PromptError(f"S18: the {arm} case block did not change")
        return {"status": "PASS", "changed_only": "nothing: inert PERM (REVISIONE_E5_001)",
                "inert": True, "full_case_sha256": sha(fc.strip()), "altered_case_sha256": sha(ac.strip())}
    return dict(frozen.case_only_diff(full, altered), inert=False)


def build(*, full_prompts: Path, test_input: Path, derangements: Path, recipients: Path) -> dict:
    protocol_omit.verify_frozen_renderer()
    cases, carriers = frozen._manifest_cases(test_input), frozen._carriers(full_prompts)
    der, rec = frozen.load_json(derangements)["derangements"], frozen.load_json(recipients)["recipients"]
    rows, proofs = [], []
    for family, assignment in der.items():
        for recipient, donor in assignment["pairs"].items():
            if recipient not in cases or donor not in cases:
                raise E5PromptError(f"unknown E5 case {recipient}/{donor}")
            rframe, neutral = cases[recipient]
            dframe, _ = cases[donor]
            perm_case = verbalizer.verbalize_feature_table(e5_corruption.swap_family(rframe, dframe, family))["text"]
            omit_case = protocol_omit.render_omit(rframe, family)["text"]
            for agent in rec["assignments"].get(recipient, []):
                base = carriers.get((recipient, agent))
                if base is None:
                    raise E5PromptError(f"missing B-LF carrier: {recipient}/{agent}")
                prefix, observed, suffix = split_carrier(base["text"])
                if observed.strip() != neutral:
                    raise E5PromptError(f"carrier case bytes differ from evidence: {recipient}/{agent}")
                for arm, case_text in (("PERM", perm_case), ("OMIT", omit_case)):
                    text = compose(prefix, case_text, suffix)
                    proof = case_proof(base["text"], text, arm=arm)
                    prompt_id = "e5_{}_{}_{}_{}_{}".format(arm.lower(), family, recipient, agent, "gp")
                    rows.append({"prompt_id": prompt_id, "stable_id": prompt_id,
                                 "source_stable_id": base["stable_id"], "arm": arm, "family": family,
                                 "case_id": recipient, "donor_case_id": donor, "agent_id": agent,
                                 "text": text, "prompt_sha256": sha(text), "inert": proof["inert"]})
                    proofs.append({"prompt_id": prompt_id, **proof})
    if len({row["prompt_id"] for row in rows}) != len(rows):
        raise E5PromptError("E5 prompt identifiers are not unique")
    inert = sorted(row["prompt_id"] for row in rows if row["inert"])
    return {"artifact_version": ARTIFACT_VERSION, "status": "OFFLINE_NOT_EXECUTED",
            "revision": "REVISIONE_E5_001: inert PERM pairs kept, sent and marked",
            "inputs": {"derangements_sha256": hashlib.sha256(derangements.read_bytes()).hexdigest(),
                       "recipients_sha256": hashlib.sha256(recipients.read_bytes()).hexdigest()},
            "rows": rows, "s18_case_block_diff": proofs,
            "counts": {"prompts": len(rows), "proofs": len(proofs), "inert": len(inert),
                       "inert_by_family": {f: sum(r["inert"] and r["family"] == f for r in rows)
                                           for f in sorted(der)}},
            "inert_prompt_ids": inert}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--full-prompts", type=Path, required=True)
    p.add_argument("--test-input", type=Path, required=True)
    p.add_argument("--derangements", type=Path, default=HERE / "DERANGEMENTS_E5.json")
    p.add_argument("--recipients", type=Path, default=HERE / "RICEVENTI_E5.json")
    p.add_argument("--out", type=Path, required=True)
    a = p.parse_args(argv)
    value = build(full_prompts=a.full_prompts, test_input=a.test_input,
                  derangements=a.derangements, recipients=a.recipients)
    a.out.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in value.items() if k not in ("rows", "s18_case_block_diff")}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
