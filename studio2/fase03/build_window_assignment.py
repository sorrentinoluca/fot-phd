#!/usr/bin/env python3
"""Build and verify the run->window assignment of the 03.11 test lot (author decision D1).

Offline, idempotent and identifier-only: it reads the sealed run plan of the test lot,
never a signal or an evidence unit, and writes
``batch_finale/ASSEGNAZIONE_FINESTRE_7_4.json``.  Running it twice produces byte-identical
output, so the recorded SHA-256 is reproducible by an independent reviewer from this
commit alone.

It stops -- and writes nothing -- if the lot does not carry eight useful windows per run.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from studio2.fase03.harness import window_assignment as module  # noqa: E402
from studio2.fase03.harness.common import HarnessError, canonical_json  # noqa: E402
from studio2.fase03.harness.runtime import durable_write  # noqa: E402

ARTIFACT_PATH = ROOT / "studio2/fase03/batch_finale/ASSEGNAZIONE_FINESTRE_7_4.json"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=ARTIFACT_PATH)
    parser.add_argument("--git-ref", default=module.IDENTIFIER_GIT_REF,
                        help="ref carrying the sealed 03.11 identifier files when this "
                             "branch does not check them out")
    parser.add_argument("--print-only", action="store_true")
    arguments = parser.parse_args(argv)

    try:
        artifact = module.assignment_artifact(git_ref=arguments.git_ref)
    except HarnessError as exc:
        print(json.dumps({"status": "STOP", "reason": str(exc)}, ensure_ascii=False, indent=2))
        return 3

    text = json.dumps(artifact, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if not arguments.print_only:
        durable_write(arguments.out, text)
    print(json.dumps({
        "status": artifact["status"],
        "path": str(arguments.out),
        "assignment_sha256": artifact["assignment_sha256"],
        "artifact_sha256": module.artifact_sha256(artifact),
        "namespace": artifact["namespace"],
        "seed": artifact["seed"],
        "numpy_version": artifact["numpy_version"],
        "counts": artifact["counts"],
        "useful_windows_check": artifact["useful_windows_check"]["status"],
        "position_table": artifact["position_table"],
    }, indent=2, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
