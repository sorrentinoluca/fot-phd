#!/usr/bin/env python3
"""Render the 2,244 unique prompts of the final batch, offline (protocol §4-§5).

No model call, no ledger access, no materialization. It reads the frozen pilot input
manifest (local examples, label space, agents, derangements), the test-lot consumer input
manifest produced by ``evidence/extract_test_lot_evidence.py`` (one neutral text per case,
the window assigned by D1) and the two accepted insight libraries, then writes
``final_prompts.jsonl`` and a summary with the counts per block, the B<->E diff on the
sole ``pseudolabel`` and the token budget.

Without every input it prints exactly what is missing and exits 3, writing nothing.
"""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness import final_inventory, final_prompts  # noqa: E402
from studio2.fase03.harness.common import (  # noqa: E402
    HarnessError, canonical_json, load_json, sha256_file, sha256_text,
)
from studio2.fase03.harness.runtime import durable_write  # noqa: E402

PILOT_INPUT_MANIFEST_SHA256 = "8417688869b75bda8235387ac830018ecdc9030442a860d495418f195f2b4014"
LIBRARIES_PATH = ROOT / "studio2/fase03/librerie/LIBRERIE_FINALI_CANDIDATE.json"


def load_cases(manifest_dir: Path) -> dict:
    """One neutral text per case, read from the test-lot extraction under its own hashes."""
    summary = load_json(manifest_dir / "INPUT_MANIFEST_TEST_7_4.json")
    index = manifest_dir / "EVIDENCE_MANIFEST_TEST.csv"
    if sha256_file(index) != summary["evidence_manifest_sha256"]:
        raise HarnessError("the test-lot evidence manifest does not match its recorded hash")
    cases = {}
    with index.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            text_path = manifest_dir / row["text_path"]
            if sha256_file(text_path) != row["text_sha256"]:
                raise HarnessError(f"{row['evidence_id']}: neutral text bytes changed")
            neutral = text_path.read_text(encoding="utf-8").strip()
            cases[row["case_id"]] = {
                "case_id": row["case_id"], "neutral_text": neutral,
                "neutral_text_sha256": sha256_text(neutral),
                "evidence_id": row["evidence_id"],
                "window_ordinal": int(row["window_ordinal"]),
            }
    return cases, summary


def load_libraries() -> dict:
    candidate = load_json(LIBRARIES_PATH)
    libraries = {}
    for role in ("122B", "27B"):
        entry = candidate["producers"][role]
        path = Path(entry["library_path"])
        if sha256_file(path) != entry["library_file_sha256"]:
            raise HarnessError(f"{role} insight library file hash changed")
        libraries[role] = load_json(path)["library"]
    return libraries


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pilot-manifest", type=Path,
                        help="execution/PILOT_INPUT_MANIFEST.frozen.json of the pilot runtime")
    parser.add_argument("--test-input", type=Path,
                        help="directory produced by evidence/extract_test_lot_evidence.py")
    parser.add_argument("--out", type=Path, default=ROOT / "studio2/fase03/batch_finale/build")
    parser.add_argument("--tokenizer-snapshot", type=Path,
                        help="tokenizer snapshot used for the context arithmetic")
    parser.add_argument("--context-limit", type=int, default=131072)
    parser.add_argument("--reserved-output-tokens", type=int, default=2560)
    arguments = parser.parse_args(argv)

    missing = []
    if not arguments.pilot_manifest or not arguments.pilot_manifest.is_file():
        missing.append("frozen pilot input manifest (local examples, label space, agents, "
                       f"derangements), SHA-256 {PILOT_INPUT_MANIFEST_SHA256}")
    elif sha256_file(arguments.pilot_manifest) != PILOT_INPUT_MANIFEST_SHA256:
        missing.append("the supplied pilot input manifest is not the frozen one")
    if not arguments.test_input or not (arguments.test_input / "INPUT_MANIFEST_TEST_7_4.json").is_file():
        missing.append("test-lot consumer input manifest: run "
                       "evidence/extract_test_lot_evidence.py after downloading the "
                       "studio2-fase03-test-v1 release")
    if missing:
        print(json.dumps({"status": "BLOCKED_MISSING_PREREQUISITES", "missing": missing},
                         indent=2, ensure_ascii=False))
        return 3

    manifest = load_json(arguments.pilot_manifest)
    cases, test_summary = load_cases(arguments.test_input)
    inventory = final_inventory.build_inventory()
    token_count = None
    if arguments.tokenizer_snapshot:
        from studio2.fase03.prepare_gate import offline_token_counter

        token_count = offline_token_counter(arguments.tokenizer_snapshot)
    value = final_prompts.render_all(
        inventory=inventory, manifest=manifest, libraries=load_libraries(), cases=cases,
        presentation_label_space=manifest.get("presentation_label_space"),
        token_count=token_count, context_limit=arguments.context_limit,
        reserved_output_tokens=arguments.reserved_output_tokens)

    path = arguments.out / "final_prompts.jsonl"
    durable_write(path, "".join(canonical_json(row) + "\n" for row in value["rows"]))
    summary = dict(value["summary"],
                   prompts_path=str(path), prompts_file_sha256=sha256_file(path),
                   pilot_input_manifest_sha256=PILOT_INPUT_MANIFEST_SHA256,
                   test_input_assignment_sha256=test_summary.get("assignment_sha256"),
                   test_input_manifest_sha256=test_summary.get("evidence_manifest_sha256"),
                   cases=len(cases))
    durable_write(arguments.out / "PROMPT_FINALI_7_4.json",
                  json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True) + "\n")
    print(json.dumps(summary, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
